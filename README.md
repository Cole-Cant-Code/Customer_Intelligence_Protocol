# Customer Intelligence Protocol - Mantic Core MCP

This repository is the shared Mantic core for CIP domain MCP servers.

It is intentionally not a finished consumer product. It is a foundation:
the place where deterministic Mantic scoring, profile contracts, and runtime
guardrails live so that downstream domain MCPs can stay focused on domain
translation, context collection, and user-facing guidance.

## Why This Exists

Domain assistants are usually forced into one of two bad tradeoffs:

1. Purely probabilistic reasoning with weak structure and inconsistent outputs
2. Hardcoded deterministic systems that do not adapt to real-world context

This project sits between those extremes.

- The Mantic layer stays deterministic, bounded, and auditable.
- The LLM layer remains flexible and interpretive.
- Domain MCPs can compose both without re-implementing the core each time.

The goal is not to replace judgment with math, or replace math with prose.
The goal is to make both cooperate cleanly.

## What This Repo Is

This repo is a Mantic-first MCP core server that provides:

- Stable MCP tools for profile-based Mantic detection
- Canonical domain profile contract (YAML + Pydantic validation)
- Profile registry/loader/validator utilities
- Runtime wrapper around `mantic_thinking.tools.generic_detect.detect`
- Contract-stable response envelope with audit metadata
- SDK wrappers that downstream domain MCPs can import directly

## What This Repo Is Not

This repo does not try to be everything:

- It is not a multi-domain consumer application
- It is not a connector hub for personal data APIs
- It does not implement full auth + tenant storage boundaries
- It does not own domain-specific translation logic

Those concerns belong in downstream domain MCP repositories that use this core.

## How It Relates to `mantic-thinking`

Think of the relationship as:

- `mantic-thinking`: core engine, validators, kernel behavior, generic detector
- `cip-mantic-core` (this repo): MCP-oriented contract + governance wrapper

`mantic-thinking` is the deterministic foundation.
This project turns that foundation into a reusable MCP layer with explicit
domain profile contracts and stable integration surfaces.

## Core Design Principles

1. Deterministic scoring, contextual interpretation
2. Strong input constraints, explicit audit output
3. Reusable contracts over per-domain reinvention
4. Safe defaults over permissive defaults
5. Clear boundaries between core and domain responsibilities

## Repository Layout

```text
src/cip_core/
  server/           FastMCP app factory + entrypoint
  mantic/           Runtime wrapper over mantic-thinking generic_detect
  domain_profiles/  Canonical profile models, validation, loading, registry
  models/           Response contracts
  sdk/              Wrapper helpers for downstream domain MCPs
profiles/           Example profile + schema
tests/              Unit/integration/contract tests
docs/               Architecture, security model, profile spec, governance
```

## Tool Surface (Current)

The server exposes the following MCP tools:

- `health_check`
- `list_domain_profiles`
- `validate_domain_profile`
- `mantic_detect`
- `mantic_detect_friction`
- `mantic_detect_emergence`

### Detection Inputs

The detection tools support:

- `profile_name`
- `layer_values`
- `mode` (`friction`/`emergence` via `mantic_detect`, fixed in mode-specific tools)
- `f_time`
- `threshold_override`
- `temporal_config`
- `interaction_mode` (`dynamic`/`base`)
- `interaction_override`
- `interaction_override_mode` (`scale`/`replace`)

### Detection Output

Successful detection responses are wrapped in a stable envelope with:

- contract metadata (`status`, `contract_version`)
- profile descriptor (`domain_profile`)
- detection mode + normalized `layer_values`
- raw engine result (`result`)
- normalized audit block (`audit`)

Error responses use:

- `status: "error"`
- `error.code`
- `error.message`

## Domain Profiles

Domain behavior is defined by YAML profiles validated against the canonical
contract in `profiles/domain_profile.schema.yaml`.

A profile defines:

- `domain_name`, version, metadata
- ordered `layer_names`
- `weights`
- layer `hierarchy` mapping
- detection `thresholds`
- `temporal_allowlist`
- `interaction_rules`
- `guardrails`

### Important Runtime Note

Profiles are loaded at startup into an in-memory registry.
If profile files change on disk, restart the server to reload them.

## Security and Boundary Defaults

Security behavior in this core is intentionally conservative:

- Loopback bind by default (`127.0.0.1`)
- Non-loopback bind requires explicit `CIP_ALLOW_INSECURE_BIND=true`
- Layer values must be numeric; out-of-range values are clamped to `[0, 1]`
- Temporal kernels are constrained by profile allowlists
- Unknown threshold override keys are ignored by Mantic and surfaced in audit fields
- Bounded override behavior remains visible via `overrides_applied`

See `docs/SECURITY_MODEL.md` for the canonical summary.

## Quick Start

### 1) Environment setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

### 2) Validate and test

```bash
make validate-profiles
make lint
make test
```

### 3) Run the server

```bash
make run
```

By default the server runs on `127.0.0.1:8010` using streamable HTTP transport.

## Environment Variables

Defined in `.env.example`:

- `CIP_HOST` (default `127.0.0.1`)
- `CIP_PORT` (default `8010`)
- `CIP_LOG_LEVEL` (default `info`)
- `CIP_ALLOW_INSECURE_BIND` (default `false`)
- `CIP_PROFILES_DIR` (default `profiles`)

## Downstream SDK Usage

Downstream MCP repos can use the SDK wrappers:

- `load_registry(profiles_dir)`
- `safe_detect(...)`
- `detect_from_translator(...)`

This keeps downstream repos thin:
they translate domain context into layer values and delegate bounded detection
to the core.

## Testing Philosophy

Tests are intentionally split by responsibility:

- Unit tests for profile validation and runtime behavior
- Integration tests for MCP tool registration and end-to-end calls
- Contract tests for response envelope stability

This protects both deterministic behavior and integration reliability.

## Documentation

Core documentation lives in:

- `docs/ARCHITECTURE.md`
- `docs/SECURITY_MODEL.md`
- `docs/DOMAIN_PROFILE_SPEC.md`
- `docs/DOMAIN_MCP_BOOTSTRAP.md`
- `docs/RELEASE_GOVERNANCE.md`

## Current Scope and Intent

This core is intentionally narrow: it gives domain MCPs a trustworthy Mantic
base layer with explicit contracts and guardrails.

The value is not novelty for novelty’s sake.
The value is reducing repeated implementation mistakes across domains while
keeping the reasoning surface transparent, bounded, and usable.
