from __future__ import annotations

import json
import os
from typing import Any

from google import genai
from google.genai import types

from app.ai.provider import AIProvider


class GeminiProvider(AIProvider):
    """Gemini API provider. Uses the API key from GEMINI_API_KEY."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        self.client = genai.Client(api_key=self.api_key)

    def generate_json(self, *, instructions: str, input_text: str, schema: dict[str, Any]) -> dict[str, Any]:
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"{instructions}\n\nINPUT:\n{input_text}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )
        return json.loads(response.text)
