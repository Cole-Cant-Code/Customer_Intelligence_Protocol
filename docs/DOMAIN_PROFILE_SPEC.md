# Domain Profile Spec

## Contract Summary

Every domain profile is YAML and must include:

- `domain_name`
- `version`
- `layer_names`
- `weights`
- `hierarchy`
- `thresholds`
- `temporal_allowlist`
- `interaction_rules`
- `guardrails`

Canonical schema file: `profiles/domain_profile.schema.yaml`.

## Invariants

- `domain_name` cannot collide with reserved Mantic domains.
- `layer_names` length is 3-6 and unique.
- `weights` length must match `layer_names` and sum to 1.0.
- `hierarchy` keys must match `layer_names` exactly.
- `thresholds.detection` is required and must be in `(0, 1)`.
- `temporal_allowlist` values must be valid Mantic kernels.
- `interaction_rules` bounds stay within `[0.1, 2.0]`.

## Validation Interfaces

- MCP tool: `validate_domain_profile(profile_yaml)`
- Script: `python scripts/validate_profiles.py profiles`
- Python API: `cip_core.domain_profiles.validate_profile_yaml`
