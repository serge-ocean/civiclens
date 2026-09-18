import json

from app.ai.client import OUTPUT_SCHEMA
from app.ai.gemini_provider import GeminiProvider


def validate_schema(schema: dict) -> None:
    """Validate the schema locally without making a Gemini API request."""
    allowed_types = {"string", "number", "integer", "boolean", "array", "object", "null"}

    def walk(node: dict, path: str = "schema") -> None:
        if not isinstance(node, dict):
            raise SystemExit(f"{path}: schema node must be an object")

        node_type = node.get("type")
        if node_type not in allowed_types:
            raise SystemExit(f"{path}: unsupported type {node_type!r}")

        if "additionalProperties" in node:
            raise SystemExit(f"{path}: additionalProperties is not allowed")

        if node_type == "object":
            properties = node.get("properties", {})
            if not isinstance(properties, dict):
                raise SystemExit(f"{path}.properties: must be an object")
            for name, child in properties.items():
                walk(child, f"{path}.properties.{name}")

        if node_type == "array":
            if "items" not in node:
                raise SystemExit(f"{path}: array is missing items")
            walk(node["items"], f"{path}.items")

        if "enum" in node and not isinstance(node["enum"], list):
            raise SystemExit(f"{path}.enum: must be a list")

    walk(schema)


def main() -> None:
    if not callable(getattr(GeminiProvider, "generate_json", None)):
        raise SystemExit("GeminiProvider.generate_json is missing")

    validate_schema(OUTPUT_SCHEMA)

    # This is intentionally a zero-request smoke test. The real article test
    # below is the only step in CI that contacts Gemini.
    print("Gemini integration: local configuration OK (0 API requests)")
    print(json.dumps(OUTPUT_SCHEMA, ensure_ascii=False))


if __name__ == "__main__":
    main()
