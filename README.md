# Mantic Core MCP — Deterministic Signal Detection for AI Reasoning

The patterns underneath expert knowledge — signals at different scales agreeing or fighting — are structurally identical whether you're reading a patient chart, a balance sheet, or a geopolitical situation. Mantic exists because LLMs can see across those walls, but only if you give them structure that prevents hallucinated connections.

This is the MCP server that makes that structure available to any MCP-compatible client. You don't need to install a Python library or write adapter code. You connect, you call tools, you get bounded, auditable, deterministic scoring — and the LLM does what math can't: interpret what the score means in context.

No hallucinated confidence. No black-box risk scores. Every override is logged, every threshold is governed, every output is explainable.

**What it does:** Detects hidden risks (friction) and optimal windows (emergence) across any domain using a deterministic 4-layer scoring kernel.

**What it is:** An MCP server wrapping the [mantic-thinking](https://github.com/Cole-Cant-Code/mantic-thinking) engine with profile-based domain contracts, governance bounds, and a stable response envelope.

**What it enables:** Domain-specific MCP servers that inherit the kernel, the governance, and the audit trail — and stay focused on their own context translation.

---

## What It Looks Like

Call the `mantic_detect_emergence` tool with four layer scores (0-1):

```json
{
  "layer_values": [0.75, 0.50, 0.60, 0.50],
  "profile_name": "signal_core",
  "mode": "emergence"
}
```

Get back a structured detection:

```json
{
  "m_score": 0.60,
  "window_detected": true,
  "window_type": "FAVORABLE: Layers aligned above threshold",
  "limiting_factor": "meso",
  "layer_attribution": {
    "micro": 0.375,
    "meso": 0.208,
    "macro": 0.250,
    "meta": 0.167
  },
  "layer_coupling": {
    "coherence": 0.80,
    "tension_with": []
  },
  "dominant": "Micro",
  "overrides_applied": {
    "f_time": { "requested": 1.0, "used": 1.0, "clamped": false }
  }
}
```

The LLM interprets what it means. The kernel guarantees the numbers are honest.

---

## Why This Exists

Domain assistants usually get stuck between two bad options:

1. **Pure LLM reasoning** — flexible but inconsistent, no audit trail, confidence is vibes
2. **Hardcoded scoring systems** — consistent but rigid, can't adapt to real-world nuance

Mantic sits between them. The deterministic layer stays bounded and auditable. The LLM layer stays flexible and interpretive. Neither replaces the other — they cooperate.

---

## Core Formula (Immutable)

```
M = (sum(W * L * I)) * f(t) / k_n
```

This single line is the entire mathematical engine. Nothing in the framework changes it. Nothing can.

| Symbol | Role | Bounds |
|--------|------|--------|
| **W** | Weights — fixed per profile, encode domain theory | Sum to 1.0, immutable at runtime |
| **L** | Layer values — your situational inputs | [0, 1], clamped |
| **I** | Interaction coefficients — per-layer confidence | [0.1, 2.0], clamped + audited |
| **f(t)** | Temporal scaling — signal urgency/persistence | [0.1, 3.0], clamped + audited |
| **k_n** | Normalization constant | Default 1.0 |

The formula is content-agnostic. Swap the profile, change the domain. The kernel doesn't care if you're scoring churn risk, fusion commercialization readiness, geopolitical tension, or household dynamics.

**Why immutability matters:** When you see an M-score from any profile — customer signals, healthcare, finance — you know exactly what produced it. Same inputs, same output, regardless of which client called it or which model is interpreting it. If the formula could be modified per-domain, that guarantee breaks and every M-score becomes local and incomparable.

---

## How It Works

You describe a situation. The LLM maps it to layer values (0-1 each), picks a mode, and calls a tool. The kernel returns:

- **M-score** — How intense is this signal?
- **Alert/window** — Did it cross a detection threshold?
- **Layer attribution** — Which input drove the score?
- **Layer visibility** — Which hierarchical level (Micro/Meso/Macro/Meta) is dominant, and why?
- **Layer coupling** — Do the layers agree, or are they in tension?

The LLM doesn't replace the math. The math prevents reasoning from drifting. The LLM translates the situation into inputs, then interprets the structured output — explaining which signals matter, why they matter, and what to do in context.

Running Mantic without an LLM gives you numbers. Running it with one gives you answers.

---

## Example: Nuclear Fusion Commercialization

**Situation:** Fusion has been "30 years away" for 60 years. But NIF achieved ignition, Commonwealth Fusion hit magnet milestones, Helion signed delivery contracts, and billions are flowing from private capital. Meanwhile, regulatory frameworks barely exist and the "always 30 years away" meme persists.

**Layer mapping:**

| Layer | Signal | Value |
|-------|--------|-------|
| micro (Micro) | Breakneck startup pace, ignition milestones | 0.75 |
| meso (Meso) | Billions flowing, but no proven unit economics | 0.60 |
| macro (Macro) | NRC just starting fusion-specific rules, ITER delays | 0.50 |
| meta (Meta) | Climate urgency refreshed patience, but meme persists | 0.50 |

**Emergence detection result:**

```json
{
  "m_score": 0.60,
  "window_detected": true,
  "window_type": "FAVORABLE: Layers aligned above threshold",
  "limiting_factor": "meso",
  "layer_attribution": {
    "micro": 0.375,
    "meso": 0.208,
    "macro": 0.250,
    "meta": 0.167
  },
  "layer_coupling": { "coherence": 0.80 },
  "dominant": "Micro"
}
```

**What the LLM narrates:** The opportunity is real (window detected, coherence 0.80), but the bottleneck is institutional readiness — regulation, permitting, grid integration. The technology is outrunning the institutions. The biggest risk isn't "will fusion work?" — it's "will there be a regulatory on-ramp ready when it does?" The alpha isn't in better magnets. It's in whoever solves the institutional gap first.

That interpretation is where the value lives. The kernel provided the structure. The LLM provided the insight.

---

## MCP Tools

| Tool | Purpose |
|------|---------|
| `health_check` | Verify server status and loaded profiles |
| `list_domain_profiles` | See available detection profiles |
| `validate_domain_profile` | Validate a YAML profile against canonical schema |
| `mantic_detect` | Run detection (specify mode: friction or emergence) |
| `mantic_detect_friction` | Shortcut — friction (divergence) detection |
| `mantic_detect_emergence` | Shortcut — emergence (alignment) detection |

### Detection Parameters

**Required:**
- `profile_name` — Which domain profile to use
- `layer_values` — Array of floats (0-1), one per layer in profile order

**Optional (most detections don't need these):**

| Parameter | What It Does | Default |
|-----------|-------------|---------|
| `mode` | Detection interpretation mode (`friction` or `emergence`) | `friction` |
| `f_time` | Raw temporal multiplier | 1.0 |
| `temporal_config` | Kernel-based temporal scaling | None |
| `threshold_override` | Adjust detection sensitivity | None |
| `interaction_mode` | Interaction behavior (`dynamic` or `base`) | `dynamic` |
| `interaction_override` | Per-layer confidence adjustment (`dict` or ordered array) | None |
| `interaction_override_mode` | `scale` (multiply existing) or `replace` (use as-is) | `scale` |

### Detection Output Envelope

Every successful response includes this stable contract envelope:

```json
{
  "status": "ok",
  "contract_version": "1.0.0",
  "domain_profile": { "domain_name": "...", "version": "...", "layer_names": ["..."] },
  "mode": "friction|emergence",
  "layer_values": [0.0, 0.0, 0.0, 0.0],
  "result": {
    "m_score": 0.0,
    "spatial_component": 0.0,
    "layer_attribution": {},
    "layer_visibility": { "dominant": "Micro|Meso|Macro|Meta" },
    "layer_coupling": { "coherence": 0.0, "layers": {} },
    "overrides_applied": {}
  },
  "audit": {
    "overrides_applied": {},
    "clamped_fields": [],
    "rejected_fields": [],
    "calibration": {}
  }
}
```

Mode-specific fields are surfaced inside `result` by the underlying detector. Common additions include friction details (`alert`, `severity`, `mismatch_score`) and emergence details (`window_detected`, `window_type`, `confidence`, `limiting_factor`, `recommended_action`) depending on detector output.

---

## Loaded Profile: `signal_core`

| Layer | Hierarchy | Weight | Definition |
|-------|-----------|--------|------------|
| micro | Micro | 0.30 | Individual actions or localized effects. |
| meso | Meso | 0.25 | Group dynamics and regional coordination patterns. |
| macro | Macro | 0.25 | System-wide aggregate effects. |
| meta | Meta | 0.20 | Evolutionary change across time (paradigm or regime shifts). |

This is the base profile. It is deliberately general and domain-agnostic. The same kernel works for any domain. The profile sets the layer names, weights, thresholds, hierarchy mapping, and temporal allowlist. The analyst decides what Micro/Meso/Macro/Meta mean for the situation at hand, and provides that mapping in narration.

### Profile Example (YAML)

```yaml
domain_name: signal_core
version: "2.0.0"
layer_names:
  - micro
  - meso
  - macro
  - meta
weights:
  micro: 0.30
  meso: 0.25
  macro: 0.25
  meta: 0.20
thresholds:
  detection: 0.42
temporal_allowlist:
  - linear
  - memory
  - s_curve
```

Profiles are validated against `profiles/domain_profile.schema.yaml` and loaded at startup into an in-memory registry. Restart to pick up profile changes.

---

## Detection Modes

**Friction** looks for divergence — where layers disagree and risk is building.

**Emergence** looks for alignment — where layers converge and a window is opening.

Same M-score scale, opposite meaning:

| M-Score | Friction | Emergence |
|---------|----------|-----------|
| 0.1-0.3 | Low risk | Low opportunity — wait |
| 0.4-0.6 | Moderate friction | Favorable window forming |
| 0.7-0.9 | High risk — act | Optimal window — act now |
| >1.0 | Amplified by f(t) | Amplified by f(t) |

**Always check which mode produced the score.** M=0.7 in friction means danger. M=0.7 in emergence means opportunity.

---

## Reading the Output

### Layer Coupling (The Hidden Insight)

`coherence` (0-1): Do the layers agree? High coherence + high M in emergence means the window is real. Low coherence + friction alert means the tension is the insight. Read which layers disagree — that is often more valuable than the score itself.

`tension_with`: Names specific disagreeing layer pairs (agreement < 0.5). Only appears when tension exists.

**Coupling is computed from layer values (L) only.** Changing interaction coefficients will not change coupling. It reflects input reality, not tuning.

### Layer Visibility

`dominant`: Which hierarchy level drove the score. When the dominant layer doesn't match the highest weight, input strength overrode structural weight.

`layer_attribution`: Percentage contribution per layer. This shows which input actually mattered.

### Key Patterns

- **High coherence + emergence window:** Real opportunity. Signals converge.
- **Low coherence + friction alert:** The disagreement is the finding. Read tension pairs.
- **Dominant layer != highest weight:** The situation is overriding profile theory.
- **f_time > 1:** Signal amplification, urgency increasing.
- **f_time < 1:** Signal suppression, urgency fading.

---

## Temporal Kernels

Temporal kernels shape how signals evolve over time. The LLM selects the dynamic; the profile allowlist prevents nonsensical choices for a given domain.

| Kernel | Formula | Use When |
|--------|---------|----------|
| `exponential` | exp(n * alpha * t) | Viral/cascade dynamics |
| `linear` | max(0, 1 - alpha * t) | Simple signal decay |
| `logistic` | 1/(1 + exp(-n * alpha * t)) | Saturation/carrying capacity |
| `s_curve` | 1/(1 + exp(-alpha * (t - t0))) | Adoption onset, slow-then-sudden |
| `power_law` | (1+t)^(n * alpha * exponent) | Heavy-tailed, extreme events |
| `oscillatory` | exp(n*alpha*t) * 0.5 * (1 + 0.5*sin(freq*t)) | Cyclical patterns |
| `memory` | 1 + memory_strength * exp(-t) | Decaying persistent influence |

Typical temporal fields include `kernel_type`, `t`, `alpha`, `n`, `t0`, `exponent`, `frequency`, and `memory_strength`. Unknown or disallowed temporal fields are surfaced in `audit.rejected_fields`.

---

## Governance

Every parameter is bounded. Every override is logged. Nothing is hidden.

| Parameter | Bound | Enforcement |
|-----------|-------|-------------|
| Weights (W) | Fixed per profile | Immutable at runtime |
| Layer values (L) | [0, 1] | Clamped |
| Interaction (I) | [0.1, 2.0] | Clamped + audited |
| Thresholds | +/-20% of profile default | Clamped + audited |
| f_time | [0.1, 3.0] | Clamped + audited |
| Alpha | [0.01, 0.5] | Clamped |
| Novelty (n) | [-2.0, 2.0] | Clamped |

The `overrides_applied` block in every response shows exactly what was requested vs. what was used. The `audit` block captures clamped and rejected fields explicitly.

**Why this matters:** LLMs drift. Give an LLM complete freedom with a scoring engine and it will eventually produce extreme or incomparable inputs. These bounds preserve judgment while preventing runaway behavior. The LLM can adjust sensitivity, confidence, and temporal dynamics — but cannot break the engine or hide what it did.

---

## How to Work With This

This framework is scaffolding, not scripture. The goal is to get to good enough quickly, not perfectly optimized eventually.

**Approximate boldly.** 0.7 vs 0.73 rarely matters. The kernel tolerates reasonable variance. If someone says "things are going badly," assign a defensible directional value and move.

**Skip the knobs first.** Most detections need only layer values and a mode. Add temporal config or interaction overrides only when baseline output is ambiguous.

**Trust clamping.** If you push a threshold too far, governance handles it.

**Test before tuning.** Run defaults first. Then adjust when needed.

**The narrative matters more than the number.** M=0.63 means moderate signal. The value is explaining which layers drove it, why it matters, and what action follows.

**Anti-pattern:** Spending long token budgets micro-optimizing parameters when concise interpretation would serve users better.

**Success pattern:** Reach an M-score in a few reasoning steps with defensible inputs, then immediately interpret business or operational meaning.

---

## Cardinal Rule: Do Not Dismiss Before Testing

Assuming the framework or profile is inadequate before testing is a common failure mode. The profile encodes domain theory. Your task is situation-specific judgment, not rebuilding the scaffolding before standing on it.

The absence of a listed use case is not evidence of incapability. The four layers and the formula are content-agnostic. They do not care whether signals come from epidemiology, finance, household systems, or concert tour economics.

Test defaults first. Tune second. Never assume first.

---

## Beyond the Base Profile

The `signal_core` profile ships as default. The kernel works for any domain with multi-scale signals. The analyst decides what Micro/Meso/Macro/Meta mean for the situation.

| Domain | Micro | Meso | Macro | Meta |
|--------|-------|------|-------|------|
| Customer Churn | Usage patterns | Org integration | Budget health | Trust durability |
| Nuclear Fusion | Technical milestones | Regulatory readiness | Capital flows | Public patience |
| MMA Fight | Strike accuracy | Round control | Career trajectory | Rule/culture shifts |
| Household Dynamics | Individual mood | Family routines | Financial stability | Generational patterns |
| Startup Viability | Product velocity | Team/org readiness | Market conditions | Founder resilience |

When the default mapping is not ideal, create a new profile with domain-appropriate layer names, hierarchy, weights, thresholds, and temporal allowlist.

---

## Architecture

### Relationship to `mantic-thinking`

```
mantic-thinking (PyPI: pip install mantic-thinking)
  = Core engine: kernel, validators, temporal kernels, generic_detect
  = Direct Python import path

cip-mantic-core (this repo)
  = MCP server wrapping generic_detect with profile contracts
  = Governance envelope + stable response schema + audit metadata
  = SDK for downstream domain MCPs
```

`mantic-thinking` is the math. This repo turns it into a reusable MCP layer with explicit domain profile contracts and stable integration surfaces.

### Repo Layout

```
src/cip_core/
  server/           # FastMCP app factory + entrypoint
  mantic/           # Runtime wrapper over mantic-thinking generic_detect
  domain_profiles/  # Canonical profile models, validation, loading, registry
  models/           # Response contracts (stable envelope)
  sdk/              # Wrapper helpers for downstream domain MCPs
profiles/           # Domain profiles + validation schema
tests/              # Unit / integration / contract tests
docs/               # Architecture, security, profile spec, governance
```

### Downstream Domain MCPs

Domain-specific MCPs import the SDK and stay thin:

```python
from cip_core.sdk import load_registry, safe_detect, detect_from_translator
```

They translate domain context into layer values and call `safe_detect`.

---

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

Server starts on `127.0.0.1:8010` (streamable HTTP).

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CIP_HOST` | `127.0.0.1` | Bind address |
| `CIP_PORT` | `8010` | Port |
| `CIP_LOG_LEVEL` | `info` | Log verbosity |
| `CIP_ALLOW_INSECURE_BIND` | `false` | Allow non-loopback bind |
| `CIP_PROFILES_DIR` | `profiles` | Profile directory path |

### Security Defaults

- Loopback bind by default (`127.0.0.1`)
- Non-loopback requires explicit `CIP_ALLOW_INSECURE_BIND=true`
- Layer values clamped to [0, 1]
- Temporal kernels constrained by profile allowlists
- Unknown threshold keys ignored and surfaced in audit
- All overrides visible in response

---

## Scope and Intent

This is intentionally a foundation, not a finished product. It does not include multi-domain consumer UX, personal data connectors, auth/tenant boundaries, or domain-specific translation logic. Those belong in downstream domain MCPs.

The value is reducing repeated implementation mistakes across domains while keeping the reasoning surface transparent, bounded, and usable.

---

## Documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — System design and component relationships
- [`docs/SECURITY_MODEL.md`](docs/SECURITY_MODEL.md) — Boundary defaults and threat model
- [`docs/DOMAIN_PROFILE_SPEC.md`](docs/DOMAIN_PROFILE_SPEC.md) — Profile contract specification
- [`docs/DOMAIN_MCP_BOOTSTRAP.md`](docs/DOMAIN_MCP_BOOTSTRAP.md) — Guide for building domain MCPs on this core
- [`docs/RELEASE_GOVERNANCE.md`](docs/RELEASE_GOVERNANCE.md) — Versioning and release policy
- [`docs/SYSTEM_PROMPT.md`](docs/SYSTEM_PROMPT.md) — Optional system prompt for model-side usage conventions

---

## Version

0.1.0 — Initial release. Profile-based generic detection via MCP. Single bundled profile (`signal_core`). SDK wrappers for downstream domain MCPs.
