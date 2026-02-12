# Release Governance

## Versioning

- Semantic versioning for this repo.
- Breaking contract change requires major version bump.
- Contract additions without breakage require minor bump.
- Patches are bug/security-only, no contract breaks.

## Downstream Upgrade Policy

- Domain MCP repos pin an exact core version.
- Upgrade via explicit compatibility test runs.
- Do not float dependencies for this core in downstream repos.

## Pre-release Checklist

1. Lint and tests green.
2. Domain profile validation script passes.
3. Response contract tests unchanged or intentionally versioned.
4. Migration note added for any contract-impacting change.
