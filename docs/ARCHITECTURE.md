# Architecture

## Purpose

`Customer_Intelligence_Protocol` is the Mantic-first core MCP that all domain MCPs build from.

## Core Responsibilities

- Own deterministic Mantic detection orchestration.
- Enforce the domain profile contract.
- Provide stable MCP tools and response schema.
- Provide SDK wrappers so domain repos stay thin.

## Downstream Domain Responsibilities

- Collect domain data from connectors.
- Translate raw context into ordered layer values.
- Call core wrappers (`safe_detect` / `detect_from_translator`).
- Use scaffolded LLM layer for explanation and action synthesis.

## Data Flow

1. Domain MCP gathers context.
2. Domain translator maps context to profile layer values.
3. Core wrapper validates profile + inputs.
4. Core calls `mantic_thinking.tools.generic_detect.detect`.
5. Core returns contract-stable response with strict audit envelope.
6. Domain MCP/LLM converts output into user-facing guidance.

## Driver Seat Model

The LLM drives strategy and interpretation; Mantic core enforces deterministic scoring and bounded controls.
