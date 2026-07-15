#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

function usage() {
  console.error("Usage: node scripts/build_deep_conflict_graph.ts <mapper-output.json> [more.json ...]");
}

function readJson(file) {
  const raw = fs.readFileSync(file, "utf8").trim();
  try {
    return JSON.parse(raw);
  } catch (error) {
    const fenced = raw.match(/```(?:json)?\s*([\s\S]*?)```/i);
    if (fenced) return JSON.parse(fenced[1]);
    throw error;
  }
}

function asArray(value) {
  return Array.isArray(value) ? value : [];
}

function normalizeName(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, " ");
}

function normalizePath(value) {
  return String(value || "").replace(/\\/g, "/").replace(/^\.\//, "");
}

function riskRank(value) {
  if (value === "high") return 3;
  if (value === "medium") return 2;
  return 1;
}

function severityRank(value) {
  if (value === "critical") return 4;
  if (value === "high") return 3;
  if (value === "medium") return 2;
  return 1;
}

function maxSeverity(values) {
  return values.sort((a, b) => severityRank(b) - severityRank(a))[0] || "low";
}

function isWriteOperation(operations) {
  return asArray(operations).some((operation) => operation !== "read");
}

function isHighChurnPath(filePath) {
  const base = path.basename(filePath);
  return [
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lockb",
    "Gemfile.lock",
    "Cargo.lock",
    "go.sum",
    "go.mod",
  ].includes(base) || /(^|\/)(migrations?|schema|generated|__generated__|dist|build)\//i.test(filePath);
}

function loadOutputs(files) {
  const outputs = [];
  for (const file of files) {
    const parsed = readJson(file);
    const values = Array.isArray(parsed) ? parsed : [parsed];
    for (const value of values) {
      outputs.push({ ...value, __file: path.resolve(file) });
    }
  }
  return outputs;
}

function addEdge(edges, edge) {
  const key = [
    edge.from,
    edge.to,
    edge.type,
    normalizeName(edge.reason),
    normalizeName(edge.evidence.join("|")),
  ].join("::");
  if (!edges.has(key)) edges.set(key, edge);
}

function directedDependencyEdges(edges, outputsById, output, deps, type, defaultSeverity) {
  for (const dep of deps) {
    if (!dep || !dep.slice_id || dep.slice_id === output.slice_id) continue;
    const dependency = outputsById.get(dep.slice_id);
    addEdge(edges, {
      from: dep.slice_id,
      to: output.slice_id,
      direction: "directed",
      type,
      severity: dependency ? defaultSeverity : "medium",
      blocking: true,
      reason: dep.description || `${output.slice_id} depends on ${dep.slice_id}`,
      evidence: dependency ? [`${dep.slice_id} is present in mapper outputs`] : [`${dep.slice_id} was referenced but not mapped`],
    });
  }
}

function edgeTypeForRuntimeDependency(dep) {
  if (dep.kind === "schema" || dep.kind === "migration") return "schema_or_migration_dependency";
  if (dep.kind === "test") return "test_dependency";
  if (dep.kind === "api") return "API_contract_dependency";
  return "product_scope_dependency";
}

function severityForRuntimeDependency(dep) {
  if (dep.kind === "schema" || dep.kind === "migration" || dep.kind === "api") return "high";
  return "medium";
}

function contractEdges(edges, outputs) {
  const byName = new Map();
  for (const output of outputs) {
    for (const contract of asArray(output.contracts)) {
      const name = normalizeName(contract.name);
      if (!name) continue;
      if (!byName.has(name)) byName.set(name, []);
      byName.get(name).push({ output, contract });
    }
  }

  for (const entries of byName.values()) {
    for (const entry of entries) {
      const providerId = entry.contract.provider;
      for (const consumerId of asArray(entry.contract.consumers)) {
        if (consumerId && consumerId !== providerId) {
          addEdge(edges, {
            from: providerId,
            to: consumerId,
            direction: "directed",
            type: "API_contract_dependency",
            severity: entry.contract.status === "changed" || entry.contract.status === "new" ? "high" : "medium",
            blocking: entry.contract.status !== "existing",
            reason: `${consumerId} consumes ${entry.contract.name} from ${providerId}`,
            evidence: [entry.contract.reason],
          });
        }
      }
    }

    for (let i = 0; i < entries.length; i += 1) {
      for (let j = i + 1; j < entries.length; j += 1) {
        const a = entries[i];
        const b = entries[j];
        if (a.output.slice_id === b.output.slice_id) continue;
        const changed = [a.contract.status, b.contract.status].some((status) => status === "changed" || status === "new" || status === "unknown");
        addEdge(edges, {
          from: a.output.slice_id,
          to: b.output.slice_id,
          direction: "undirected",
          type: "API_contract_dependency",
          severity: changed ? "high" : "medium",
          blocking: changed,
          reason: `Both slices reference contract ${a.contract.name}`,
          evidence: [a.contract.reason, b.contract.reason],
        });
      }
    }
  }
}

function fileAndSymbolEdges(edges, outputs) {
  const byPath = new Map();
  for (const output of outputs) {
    for (const touchpoint of asArray(output.touchpoints)) {
      const filePath = normalizePath(touchpoint.path);
      if (!filePath) continue;
      if (!byPath.has(filePath)) byPath.set(filePath, []);
      byPath.get(filePath).push({ output, touchpoint, filePath });
    }
  }

  for (const [filePath, entries] of byPath.entries()) {
    for (let i = 0; i < entries.length; i += 1) {
      for (let j = i + 1; j < entries.length; j += 1) {
        const a = entries[i];
        const b = entries[j];
        if (a.output.slice_id === b.output.slice_id) continue;
        if (!isWriteOperation(a.touchpoint.operations) && !isWriteOperation(b.touchpoint.operations)) continue;

        const highChurn = isHighChurnPath(filePath);
        const severity = highChurn ? "high" : maxSeverity([a.touchpoint.risk, b.touchpoint.risk].map((risk) => (riskRank(risk) >= 3 ? "high" : "medium")));
        addEdge(edges, {
          from: a.output.slice_id,
          to: b.output.slice_id,
          direction: "undirected",
          type: "same_file_conflict",
          severity,
          blocking: highChurn || severity === "high",
          reason: `Both slices expect to touch ${filePath}`,
          evidence: [a.touchpoint.reason, b.touchpoint.reason],
        });

        const symbolsA = new Set(asArray(a.touchpoint.symbols).map(normalizeName).filter(Boolean));
        const symbolsB = new Set(asArray(b.touchpoint.symbols).map(normalizeName).filter(Boolean));
        const overlap = Array.from(symbolsA).filter((symbol) => symbolsB.has(symbol));
        if (overlap.length > 0) {
          addEdge(edges, {
            from: a.output.slice_id,
            to: b.output.slice_id,
            direction: "undirected",
            type: "same_symbol_conflict",
            severity: "high",
            blocking: true,
            reason: `Both slices expect to touch ${overlap.join(", ")} in ${filePath}`,
            evidence: [a.touchpoint.reason, b.touchpoint.reason],
          });
        }
      }
    }
  }
}

function migrationEdges(edges, outputs) {
  const entries = [];
  for (const output of outputs) {
    for (const migration of asArray(output.migrations)) {
      for (const entity of asArray(migration.entities)) {
        entries.push({ output, migration, entity: normalizeName(entity) });
      }
      if (migration.path) {
        entries.push({ output, migration, entity: `path:${normalizePath(migration.path)}` });
      }
    }
  }

  for (let i = 0; i < entries.length; i += 1) {
    for (let j = i + 1; j < entries.length; j += 1) {
      const a = entries[i];
      const b = entries[j];
      if (a.output.slice_id === b.output.slice_id || !a.entity || a.entity !== b.entity) continue;
      addEdge(edges, {
        from: a.output.slice_id,
        to: b.output.slice_id,
        direction: "undirected",
        type: "schema_or_migration_dependency",
        severity: "high",
        blocking: true,
        reason: `Both slices affect migration/schema entity ${a.entity.replace(/^path:/, "")}`,
        evidence: [a.migration.reason, b.migration.reason],
      });
    }
  }
}

function testEdges(edges, outputs) {
  const byTestPath = new Map();
  const touchedFilesBySlice = new Map();
  for (const output of outputs) {
    touchedFilesBySlice.set(output.slice_id, new Set(asArray(output.touchpoints).map((t) => normalizePath(t.path)).filter(Boolean)));
    for (const test of asArray(output.tests)) {
      const testPath = normalizePath(test.path);
      if (!testPath) continue;
      if (!byTestPath.has(testPath)) byTestPath.set(testPath, []);
      byTestPath.get(testPath).push({ output, test, testPath });
    }
  }

  for (const [testPath, entries] of byTestPath.entries()) {
    for (let i = 0; i < entries.length; i += 1) {
      for (let j = i + 1; j < entries.length; j += 1) {
        const a = entries[i];
        const b = entries[j];
        if (a.output.slice_id === b.output.slice_id) continue;
        addEdge(edges, {
          from: a.output.slice_id,
          to: b.output.slice_id,
          direction: "undirected",
          type: "test_dependency",
          severity: "medium",
          blocking: false,
          reason: `Both slices expect to touch or rely on test ${testPath}`,
          evidence: [`${a.output.slice_id}: ${asArray(a.test.covers).join(", ")}`, `${b.output.slice_id}: ${asArray(b.test.covers).join(", ")}`],
        });
      }
    }
  }

  for (const output of outputs) {
    for (const test of asArray(output.tests)) {
      for (const covered of asArray(test.covers)) {
        const coveredPath = normalizePath(covered);
        for (const other of outputs) {
          if (other.slice_id === output.slice_id) continue;
          if (touchedFilesBySlice.get(other.slice_id)?.has(coveredPath)) {
            addEdge(edges, {
              from: other.slice_id,
              to: output.slice_id,
              direction: "directed",
              type: "test_dependency",
              severity: "medium",
              blocking: false,
              reason: `${output.slice_id} tests code touched by ${other.slice_id}`,
              evidence: [`${test.path} covers ${coveredPath}`],
            });
          }
        }
      }
    }
  }
}

function productEdges(edges, outputs) {
  for (const output of outputs) {
    for (const dep of asArray(output.product_dependencies)) {
      if (dep.slice_id && dep.slice_id !== output.slice_id) {
        addEdge(edges, {
          from: dep.slice_id,
          to: output.slice_id,
          direction: "directed",
          type: "product_scope_dependency",
          severity: "medium",
          blocking: true,
          reason: dep.description,
          evidence: [`${output.slice_id} product dependency kind: ${dep.kind}`],
        });
      }
    }
  }

  const entries = [];
  for (const output of outputs) {
    for (const dep of asArray(output.product_dependencies)) {
      entries.push({ output, dep, key: normalizeName(`${dep.kind}:${dep.description}`).slice(0, 120) });
    }
  }
  for (let i = 0; i < entries.length; i += 1) {
    for (let j = i + 1; j < entries.length; j += 1) {
      const a = entries[i];
      const b = entries[j];
      if (a.output.slice_id === b.output.slice_id || !a.key || a.key !== b.key) continue;
      addEdge(edges, {
        from: a.output.slice_id,
        to: b.output.slice_id,
        direction: "undirected",
        type: "product_scope_dependency",
        severity: "medium",
        blocking: true,
        reason: `Both slices share product dependency: ${a.dep.description}`,
        evidence: [a.dep.kind, b.dep.kind],
      });
    }
  }
}

function sharedResourceEdges(edges, outputs) {
  const byResource = new Map();
  for (const output of outputs) {
    for (const resource of asArray(output.shared_resources)) {
      const key = normalizeName(resource.name);
      if (!key) continue;
      if (!byResource.has(key)) byResource.set(key, []);
      byResource.get(key).push({ output, resource });
    }
  }

  for (const entries of byResource.values()) {
    for (let i = 0; i < entries.length; i += 1) {
      for (let j = i + 1; j < entries.length; j += 1) {
        const a = entries[i];
        const b = entries[j];
        if (a.output.slice_id === b.output.slice_id) continue;
        const high = ["lockfile", "migration", "schema", "generated", "build"].includes(normalizeName(a.resource.kind)) ||
          ["lockfile", "migration", "schema", "generated", "build"].includes(normalizeName(b.resource.kind));
        addEdge(edges, {
          from: a.output.slice_id,
          to: b.output.slice_id,
          direction: "undirected",
          type: high ? "schema_or_migration_dependency" : "same_file_conflict",
          severity: high ? "high" : "medium",
          blocking: high,
          reason: `Both slices use shared resource ${a.resource.name}`,
          evidence: [a.resource.reason, b.resource.reason],
        });
      }
    }
  }
}

function waveSummary(outputs, edges) {
  const blockingByTo = new Map();
  const conflicted = new Set();
  for (const edge of edges) {
    if (edge.direction === "directed" && edge.blocking) {
      if (!blockingByTo.has(edge.to)) blockingByTo.set(edge.to, []);
      blockingByTo.get(edge.to).push(edge.from);
    }
    if (edge.direction === "undirected" && edge.blocking) {
      conflicted.add(edge.from);
      conflicted.add(edge.to);
    }
  }

  return outputs.map((output) => {
    const requestedWave = output.execution?.estimated_wave;
    const waitsFor = Array.from(new Set([...(output.execution?.must_wait_for || []), ...(blockingByTo.get(output.slice_id) || [])])).filter(Boolean);
    const definesContractOrMigration = asArray(output.contracts).some((contract) =>
      contract.provider === output.slice_id &&
      (contract.status === "new" || contract.status === "changed" || contract.status === "unknown")
    ) ||
      asArray(output.migrations).length > 0;
    let recommendedWave = requestedWave;
    let reason = output.execution?.parallel_safety_reason || "";
    if (definesContractOrMigration) {
      recommendedWave = 0;
      reason = "Defines or changes a contract, schema, or migration.";
    } else if (waitsFor.length > 0 || output.execution?.parallel_safety === "unsafe") {
      recommendedWave = Math.max(2, Number.isInteger(requestedWave) ? requestedWave : 2);
      reason = `Waits for ${waitsFor.join(", ") || "a blocking dependency"}.`;
    } else if (conflicted.has(output.slice_id) || output.execution?.parallel_safety === "conditional") {
      recommendedWave = Math.max(2, Number.isInteger(requestedWave) ? requestedWave : 2);
      reason = reason || "Has conditional parallel safety or blocking conflict.";
    } else {
      recommendedWave = 1;
      reason = reason || "No blocking conflicts detected.";
    }
    return {
      slice_id: output.slice_id,
      requested_wave: requestedWave,
      recommended_wave: recommendedWave,
      parallel_safety: output.execution?.parallel_safety,
      waits_for: waitsFor,
      reason,
    };
  });
}

const files = process.argv.slice(2);
if (files.length === 0) {
  usage();
  process.exit(2);
}

try {
  const outputs = loadOutputs(files);
  const outputsById = new Map(outputs.map((output) => [output.slice_id, output]));
  const edges = new Map();

  for (const output of outputs) {
    for (const dep of asArray(output.runtime_dependencies)) {
      directedDependencyEdges(edges, outputsById, output, [dep], edgeTypeForRuntimeDependency(dep), severityForRuntimeDependency(dep));
    }
    for (const waitFor of asArray(output.execution?.must_wait_for)) {
      directedDependencyEdges(edges, outputsById, output, [{ slice_id: waitFor, description: `${output.slice_id} must wait for ${waitFor}` }], "product_scope_dependency", "medium");
    }
  }

  fileAndSymbolEdges(edges, outputs);
  contractEdges(edges, outputs);
  migrationEdges(edges, outputs);
  testEdges(edges, outputs);
  productEdges(edges, outputs);
  sharedResourceEdges(edges, outputs);

  const edgeList = Array.from(edges.values()).sort((a, b) => {
    const severity = severityRank(b.severity) - severityRank(a.severity);
    if (severity !== 0) return severity;
    return `${a.from}:${a.to}:${a.type}`.localeCompare(`${b.from}:${b.to}:${b.type}`);
  });

  const summaryByType = {};
  for (const edge of edgeList) {
    summaryByType[edge.type] = (summaryByType[edge.type] || 0) + 1;
  }

  const graph = {
    schema_version: "dev-project-orchestrator.deep-plan.graph.v1",
    nodes: outputs.map((output) => ({
      id: output.slice_id,
      title: output.title,
      source: output.source,
      confidence: output.confidence,
      mapper_output: output.__file,
      parallel_safety: output.execution?.parallel_safety,
    })),
    edges: edgeList,
    summary: {
      node_count: outputs.length,
      edge_count: edgeList.length,
      by_type: summaryByType,
      blocking_edges: edgeList.filter((edge) => edge.blocking).length,
    },
    wave_recommendations: waveSummary(outputs, edgeList),
  };

  console.log(JSON.stringify(graph, null, 2));
} catch (error) {
  console.error(`FAIL build_deep_conflict_graph: ${error.message}`);
  process.exit(1);
}
