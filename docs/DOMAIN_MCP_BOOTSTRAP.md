# Domain MCP Bootstrap

## Thin Adapter Pattern

Domain MCP repos should remain thin and deterministic.

1. Add a domain profile YAML in your repo.
2. Implement a translator that maps domain context to ordered `layer_values`.
3. Import CIP core SDK wrappers.
4. Call detection wrappers from your domain tool handlers.
5. Feed core response into your scaffolded LLM explanation layer.

## Required Imports

```python
from cip_core.sdk import DomainTranslator, detect_from_translator, load_registry
```

## Minimal Integration Example

```python
registry = load_registry("profiles")
result = detect_from_translator(
    registry=registry,
    profile_name="signal_core",
    translator=my_translator,
    raw_context=context,
    mode="friction",
)
```

## Contract Rule

Do not bypass the core wrappers for custom detect logic in domain repos.
