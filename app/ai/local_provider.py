from __future__ import annotations

import json
import os
from typing import Any

import requests

from app.ai.provider import AIProvider


class LocalOllamaProvider(AIProvider):
    """Free local provider using an Ollama server on the user's machine."""

    def __init__(self, base_url: str | None = None, model: str | None = None) -> None:
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")
        self.model = model or os.getenv("OLLAMA_MODEL", "qwen3:8b")

    def generate_json(self, *, instructions: str, input_text: str, schema: dict[str, Any]) -> dict[str, Any]:
        prompt = (
            f"{instructions}\n\n"
            "Return JSON only. It must conform to this JSON schema:\n"
            f"{json.dumps(schema, ensure_ascii=False)}\n\n"
            f"INPUT:\n{input_text}"
        )
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False, "format": "json"},
            timeout=120,
        )
        response.raise_for_status()
        body = response.json()
        return json.loads(body["response"])
