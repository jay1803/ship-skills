# Claude Code Adapter

Use this adapter only after the Review routing contract resolves Claude Code.

## Binding

- Runtime role: `reviewer`.
- Standard depth: bind the configured balanced Claude Code reviewer model and
  normal reasoning effort.
- Deep depth: bind the configured highest-capability Claude Code reviewer model
  and high reasoning effort.
- Use only a configured runtime-native Claude Code session or worker entry. Do
  not launch an ad-hoc provider command.
- Create a clean context with no implementation-thread history. The assigned
  reviewer may inspect the exact repository target and surrounding code but may
  not dispatch another reviewer or provider.

Record the actual model, reasoning effort, runtime role, any fallback, and
independence result in the routing receipt. Never infer a runtime binding that
the environment did not report.
