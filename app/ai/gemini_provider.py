from __future__ import annotations

import json
import os
from typing import Any

from google import genai

from app.ai.provider import AIProvider


class GeminiProvider(AIProvider):
    """Gemini provider using the Interactions API.

    Deliberately makes exactly one API request per generate_json() call.
    Retries and model fallbacks are avoided because they can consume
    additional quota and hide the original API failure.
    """

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        self.client = genai.Client(api_key=self.api_key)

    def generate_json(
        self,
        *,
        instructions: str,
        input_text: str,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        interaction = self.client.interactions.create(
            model=self.model,
            input=f"{instructions}\n\nINPUT:\n{input_text}",
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": schema,
            },
        )

        try:
            result = json.loads(interaction.output_text)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Gemini returned invalid JSON") from exc

        if not isinstance(result, dict):
            raise RuntimeError("Gemini returned JSON, but the top-level value is not an object")

        return result
