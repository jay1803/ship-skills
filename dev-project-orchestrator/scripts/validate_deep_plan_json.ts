#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const VERSION = "dev-project-orchestrator.deep-plan.mapper.v1";
const SOURCE_TYPES = new Set(["issue", "pr", "branch", "feature_slice", "parent_issue", "unknown"]);
const OPERATIONS = new Set(["read", "create", "modify", "delete", "rename", "generate"]);
const RISK = new Set(["low", "medium", "high"]);
const CONTRACT_KINDS = new Set(["api", "schema", "migration", "event", "ui", "config", "data", "other"]);
const CONTRACT_STATUS = new Set(["existing", "new", "changed", "unknown"]);
const MIGRATION_OPERATIONS = new Set(["create", "modify", "delete", "unknown"]);
const TEST_KINDS = new Set(["unit", "integration", "e2e", "manual", "contract", "other"]);
const DEP_KINDS = new Set(["api", "schema", "migration", "test", "runtime", "build", "config", "other"]);
const PRODUCT_KINDS = new Set(["scope", "ux", "copy", "rollout", "analytics", "permissions", "other"]);
const WAVES = new Set([0, 1, 2, 3]);
const PARALLEL_SAFETY = new Set(["safe", "conditional", "unsafe"]);

function usage() {
  console.error("Usage: node scripts/validate_deep_plan_json.ts <mapper-output.json> [more.json ...]");
}

function readJson(file) {
  const raw = fs.readFileSync(file, "utf8").trim();
  try {
    return JSON.parse(raw);
  } catch (error) {
    const fenced = raw.match(/```(?:json)?\s*([\s\S]*?)```/i);
    if (fenced) {
      return JSON.parse(fenced[1]);
    }
    throw error;
  }
}

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function hasText(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function requireText(errors, value, field) {
  if (!hasText(value)) errors.push(`${field} must be a non-empty string`);
}

function requireArray(errors, value, field) {
  if (!Array.isArray(value)) {
    errors.push(`${field} must be an array`);
    return [];
  }
  return value;
}

function requireStringArray(errors, value, field) {
  const arr = requireArray(errors, value, field);
  arr.forEach((item, index) => {
    if (typeof item !== "string") errors.push(`${field}[${index}] must be a string`);
  });
  return arr;
}

function requireEnum(errors, value, allowed, field) {
  if (!allowed.has(value)) errors.push(`${field} must be one of: ${Array.from(allowed).join(", ")}`);
}

function validateSource(errors, source) {
  if (!isObject(source)) {
    errors.push("source must be an object");
    return;
  }
  requireEnum(errors, source.type, SOURCE_TYPES, "source.type");
  requireText(errors, source.id, "source.id");
  if (source.url !== undefined && typeof source.url !== "string") errors.push("source.url must be a string when present");
}

function validateScope(errors, scope) {
  if (!isObject(scope)) {
    errors.push("scope must be an object");
    return;
  }
  requireStringArray(errors, scope.included, "scope.included");
  requireStringArray(errors, scope.excluded, "scope.excluded");
  requireStringArray(errors, scope.unknowns, "scope.unknowns");
}

function validateTouchpoints(errors, touchpoints) {
  requireArray(errors, touchpoints, "touchpoints").forEach((touchpoint, index) => {
    const prefix = `touchpoints[${index}]`;
    if (!isObject(touchpoint)) {
      errors.push(`${prefix} must be an object`);
      return;
    }
    requireText(errors, touchpoint.path, `${prefix}.path`);
    requireStringArray(errors, touchpoint.symbols, `${prefix}.symbols`);
    requireArray(errors, touchpoint.operations, `${prefix}.operations`).forEach((operation, opIndex) => {
      requireEnum(errors, operation, OPERATIONS, `${prefix}.operations[${opIndex}]`);
    });
    requireText(errors, touchpoint.reason, `${prefix}.reason`);
    requireEnum(errors, touchpoint.risk, RISK, `${prefix}.risk`);
  });
}

function validateContracts(errors, contracts) {
  requireArray(errors, contracts, "contracts").forEach((contract, index) => {
    const prefix = `contracts[${index}]`;
    if (!isObject(contract)) {
      errors.push(`${prefix} must be an object`);
      return;
    }
    requireText(errors, contract.name, `${prefix}.name`);
    requireEnum(errors, contract.kind, CONTRACT_KINDS, `${prefix}.kind`);
    requireText(errors, contract.provider, `${prefix}.provider`);
    requireStringArray(errors, contract.consumers, `${prefix}.consumers`);
    requireEnum(errors, contract.status, CONTRACT_STATUS, `${prefix}.status`);
    requireText(errors, contract.reason, `${prefix}.reason`);
  });
}

function validateMigrations(errors, migrations) {
  requireArray(errors, migrations, "migrations").forEach((migration, index) => {
    const prefix = `migrations[${index}]`;
    if (!isObject(migration)) {
      errors.push(`${prefix} must be an object`);
      return;
    }
    if (migration.path !== undefined && typeof migration.path !== "string") errors.push(`${prefix}.path must be a string when present`);
    requireEnum(errors, migration.operation, MIGRATION_OPERATIONS, `${prefix}.operation`);
    requireStringArray(errors, migration.entities, `${prefix}.entities`);
    requireText(errors, migration.reason, `${prefix}.reason`);
  });
}

function validateTests(errors, tests) {
  requireArray(errors, tests, "tests").forEach((test, index) => {
    const prefix = `tests[${index}]`;
    if (!isObject(test)) {
      errors.push(`${prefix} must be an object`);
      return;
    }
    requireText(errors, test.path, `${prefix}.path`);
    requireEnum(errors, test.kind, TEST_KINDS, `${prefix}.kind`);
    requireEnum(errors, test.operation, OPERATIONS, `${prefix}.operation`);
    requireStringArray(errors, test.covers, `${prefix}.covers`);
    requireStringArray(errors, test.depends_on, `${prefix}.depends_on`);
  });
}

function validateDependencies(errors, deps, field, allowedKinds) {
  requireArray(errors, deps, field).forEach((dep, index) => {
    const prefix = `${field}[${index}]`;
    if (!isObject(dep)) {
      errors.push(`${prefix} must be an object`);
      return;
    }
    if (dep.slice_id !== undefined && typeof dep.slice_id !== "string") errors.push(`${prefix}.slice_id must be a string when present`);
    requireEnum(errors, dep.kind, allowedKinds, `${prefix}.kind`);
    requireText(errors, dep.description, `${prefix}.description`);
  });
}

function validateSharedResources(errors, resources) {
  requireArray(errors, resources, "shared_resources").forEach((resource, index) => {
    const prefix = `shared_resources[${index}]`;
    if (!isObject(resource)) {
      errors.push(`${prefix} must be an object`);
      return;
    }
    requireText(errors, resource.name, `${prefix}.name`);
    requireText(errors, resource.kind, `${prefix}.kind`);
    requireText(errors, resource.reason, `${prefix}.reason`);
  });
}

function validateExecution(errors, execution) {
  if (!isObject(execution)) {
    errors.push("execution must be an object");
    return;
  }
  requireStringArray(errors, execution.can_start_without, "execution.can_start_without");
  requireStringArray(errors, execution.must_wait_for, "execution.must_wait_for");
  requireEnum(errors, execution.estimated_wave, WAVES, "execution.estimated_wave");
  requireEnum(errors, execution.parallel_safety, PARALLEL_SAFETY, "execution.parallel_safety");
  requireText(errors, execution.parallel_safety_reason, "execution.parallel_safety_reason");
  requireStringArray(errors, execution.validation, "execution.validation");
}

function validateEvidence(errors, evidence) {
  requireArray(errors, evidence, "evidence").forEach((entry, index) => {
    const prefix = `evidence[${index}]`;
    if (!isObject(entry)) {
      errors.push(`${prefix} must be an object`);
      return;
    }
    requireText(errors, entry.source, `${prefix}.source`);
    requireText(errors, entry.detail, `${prefix}.detail`);
  });
}

function validateMapperOutput(data) {
  const errors = [];
  if (!isObject(data)) return ["root must be a JSON object"];

  if (data.schema_version !== VERSION) errors.push(`schema_version must be ${VERSION}`);
  requireText(errors, data.slice_id, "slice_id");
  requireText(errors, data.title, "title");
  validateSource(errors, data.source);
  requireText(errors, data.implementation_hypothesis, "implementation_hypothesis");
  validateScope(errors, data.scope);
  validateTouchpoints(errors, data.touchpoints);
  validateContracts(errors, data.contracts);
  validateMigrations(errors, data.migrations);
  validateTests(errors, data.tests);
  validateDependencies(errors, data.runtime_dependencies, "runtime_dependencies", DEP_KINDS);
  validateDependencies(errors, data.product_dependencies, "product_dependencies", PRODUCT_KINDS);
  validateSharedResources(errors, data.shared_resources);
  validateExecution(errors, data.execution);
  validateEvidence(errors, data.evidence);
  requireEnum(errors, data.confidence, RISK, "confidence");

  return errors;
}

const files = process.argv.slice(2);
if (files.length === 0) {
  usage();
  process.exit(2);
}

let failed = false;
for (const file of files) {
  try {
    const resolved = path.resolve(file);
    const parsed = readJson(resolved);
    const outputs = Array.isArray(parsed) ? parsed : [parsed];
    outputs.forEach((output, index) => {
      const errors = validateMapperOutput(output);
      const label = outputs.length === 1 ? file : `${file}[${index}]`;
      if (errors.length > 0) {
        failed = true;
        console.error(`FAIL ${label}`);
        errors.forEach((error) => console.error(`  - ${error}`));
      } else {
        console.log(`OK ${label} (${output.slice_id})`);
      }
    });
  } catch (error) {
    failed = true;
    console.error(`FAIL ${file}`);
    console.error(`  - ${error.message}`);
  }
}

process.exit(failed ? 1 : 0);
