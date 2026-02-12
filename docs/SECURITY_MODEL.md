# Security Model

## Boundaries

- Server binds loopback by default.
- Non-loopback bind requires explicit `CIP_ALLOW_INSECURE_BIND=true`.
- No secret-bearing MCP tools or resources are exposed.
- Domain profile validation blocks malformed or collision-prone contracts.

## Input Controls

- Layer values must be numeric; values outside `[0, 1]` are clamped.
- Unknown threshold override keys are ignored by Mantic runtime and surfaced in audit fields.
- Temporal kernel use is constrained by profile allowlist.
- Mantic runtime bounded overrides remain active (`overrides_applied`).

## Non-goals

- This core does not implement auth or multi-tenant data storage.
- This core does not host domain-specific personal data connectors.
