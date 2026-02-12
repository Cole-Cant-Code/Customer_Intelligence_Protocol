# Mantic Core — Deterministic Signal Detection for AI Reasoning

Mantic is a scoring engine that pairs with LLMs to detect **hidden risks** (friction) and **optimal windows** (emergence) across any domain. You provide situational judgment as layer values; the kernel provides deterministic, auditable, bounded scoring.

No hallucinated confidence. No black-box risk scores. Every override is logged, every threshold is governed, every output is explainable.

This repo is the shared MCP server core. Domain-specific MCPs import it and stay focused on their own context — Mantic handles the math.

## What It Looks Like

Call the `mantic_detect_emergence` tool with four layer scores (0–1):

```json
{
  "layer_values": [0.75, 0.50, 0.60, 0.50],
  "profile_name": "customer_signal_core",
  "mode": "emergence"
}
```

Get back a structured detection:

```json
{
  "m_score": 0.60,
  "window_detected": true,
  "window_type": "FAVORABLE: Layers aligned above threshold",
  "limiting_factor": "institutional_readiness",
  "layer_attribution": {
    "behavioral_velocity": 0.375,
    "institutional_readiness": 0.208,
    "economic_capacity": 0.250,
    "trust_resilience": 0.167
  },
  "layer_coupling": {
    "coherence": 0.80,
    "tension_with": []
  },
  "dominant": "Micro",
  "overrides_applied": { "f_time": { "requested": 1.0, "used": 1.0, "clamped": false } }
}
```

The LLM interprets *what it means*. The kernel guarantees *the numbers are honest*.

## Why This Exists

Domain assistants usually get stuck between two bad options:

1. **Pure LLM reasoning** — flexible but inconsistent, no audit trail, confidence is vibes
2. **Hardcoded scoring systems** — consistent but rigid, can't adapt to real-world nuance

Mantic sits between them. The deterministic layer stays bounded and auditable. The LLM layer stays flexible and interpretive. Neither replaces the other — they cooperate.

## Core Formula

```
M = (Σ W × L × I) × f(t) / k_n
```

| Symbol | Role | Bounds |
|--------|------|--------|
| **W** | Weights — fixed per profile, encode domain theory | Sum to 1.0 |
| **L** | Layer values — your situational inputs | [0, 1] |
| **I** | Interaction coefficients — per-layer confidence | [0.1, 2.0] |
| **f(t)** | Temporal scaling — signal urgency/persistence | [0.1, 3.0] |
| **k_n** | Normalization constant | Default 1.0 |

The formula is content-agnostic. Swap the profile, change the domain. The kernel doesn't care if you're scoring churn risk, geopolitical tension, or fusion commercialization readiness.

## How Detection Works

**Friction mode** looks for divergence — where layers disagree and risk is building.

**Emergence mode** looks for alignment — where layers converge and a window is opening.

Same M-score scale, opposite meaning:

| M-Score | Friction | Emergence |
|---------|----------|-----------|
| 0.1–0.3 | Low risk | Low opportunity |
| 0.4–0.6 | Moderate friction | Favorable window forming |
| 0.7–0.9 | High risk — act | Optimal window — act now |
| >1.0 | Amplified by f(t) | Amplified by f(t) |

The layer coupling readout tells you *which* layers agree or disagree — that's often where the real insight lives.

## MCP Tool Surface

| Tool | Purpose |
|------|---------|
| `health_check` | Verify server + loaded profiles |
| `list_domain_profiles` | See available detection profiles |
| `validate_domain_profile` | Validate YAML profile against schema |
| `mantic_detect` | Run detection (specify mode) |
| `mantic_detect_friction` | Shortcut — friction detection |
| `mantic_detect_emergence` | Shortcut — emergence detection |

### Detection Parameters

**Required:** `profile_name`, `layer_values` (array of floats)

**Optional tuning:**

| Parameter | What It Does | Default |
|-----------|-------------|---------|
| `f_time` | Raw temporal multiplier | 1.0 |
| `temporal_config` | Kernel-based temporal scaling (exponential, logistic, s_curve, etc.) | None |
| `interaction_override` | Per-layer confidence adjustment | [1.0, 1.0, 1.0, 1.0] |
| `threshold_override` | Adjust detection sensitivity (±20% of profile default) | None |

Most detections need only layer values. Add overrides when the base result is ambiguous.

## Quick Start

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env

# Validate and test
make validate-profiles
make lint
make test

# Run
make run
```

Server starts on `127.0.0.1:8010` (streamable HTTP). Loopback-only by default — non-loopback requires explicit `CIP_ALLOW_INSECURE_BIND=true`.

## Domain Profiles

Profiles are YAML files that define detection behavior for a domain:

```yaml
domain_name: customer_signal_core
version: "1.0.0"
layer_names:
  - behavioral_velocity    # Micro — engagement speed, usage patterns
  - institutional_readiness # Meso — org alignment, process adoption
  - economic_capacity       # Macro — budget health, spending trajectory
  - trust_resilience        # Meta — relationship durability under stress
weights:
  behavioral_velocity: 0.30
  institutional_readiness: 0.25
  economic_capacity: 0.25
  trust_resilience: 0.20
thresholds:
  detection: 0.42
temporal_allowlist:
  - linear
  - memory
  - s_curve
```

Validated against `profiles/domain_profile.schema.yaml`. Loaded at startup into an in-memory registry — restart to pick up changes.

## Governance

Every parameter is bounded. Every override is logged. Nothing is hidden.

| Parameter | Bound | Enforcement |
|-----------|-------|-------------|
| Weights | Fixed per profile | Immutable at runtime |
| Layer values | [0, 1] | Clamped |
| Interaction coefficients | [0.1, 2.0] | Clamped + audited |
| Thresholds | ±20% of profile default | Clamped + audited |
| f_time | [0.1, 3.0] | Clamped + audited |

The `overrides_applied` block in every response shows exactly what was requested vs. what was used.

## Architecture

```
src/cip_core/
  server/           # FastMCP app factory + entrypoint
  mantic/           # Runtime wrapper over mantic-thinking generic_detect
  domain_profiles/  # Profile models, validation, loading, registry
  models/           # Response contracts
  sdk/              # Wrapper helpers for downstream domain MCPs
profiles/           # Domain profiles + schema
tests/              # Unit / integration / contract tests
docs/               # Architecture, security, profile spec, governance
```

### Relationship to `mantic-thinking`

- **`mantic-thinking`** — the core engine: validators, kernel math, generic detector
- **`cip-mantic-core`** (this repo) — MCP contract + governance wrapper around that engine

### Downstream SDK

Domain MCPs import the SDK wrappers and stay thin:

```python
from cip_core.sdk import load_registry, safe_detect, detect_from_translator
```

They translate domain context into layer values. This core handles bounded detection.

## Scope

This is intentionally a foundation, not a finished product. It does not include multi-domain consumer UX, personal data connectors, auth/tenant boundaries, or domain-specific translation logic. Those belong in downstream domain MCPs.

## Docs

- [`ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`SECURITY_MODEL.md`](docs/SECURITY_MODEL.md)
- [`DOMAIN_PROFILE_SPEC.md`](docs/DOMAIN_PROFILE_SPEC.md)
- [`DOMAIN_MCP_BOOTSTRAP.md`](docs/DOMAIN_MCP_BOOTSTRAP.md)
- [`RELEASE_GOVERNANCE.md`](docs/RELEASE_GOVERNANCE.md)

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CIP_HOST` | `127.0.0.1` | Bind address |
| `CIP_PORT` | `8010` | Port |
| `CIP_LOG_LEVEL` | `info` | Log verbosity |
| `CIP_ALLOW_INSECURE_BIND` | `false` | Allow non-loopback bind |
| `CIP_PROFILES_DIR` | `profiles` | Profile directory path |
