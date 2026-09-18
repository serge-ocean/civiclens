from __future__ import annotations

import json
import os
import time
from typing import Any

from google import genai

from app.ai.provider import AIProvider


class GeminiProvider(AIProvider):
    """Gemini API provider using the current Interactions API with fallbacks."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        self.client = genai.Client(api_key=self.api_key)

    def generate_json(self, *, instructions: str, input_text: str, schema: dict[str, Any]) -> dict[str, Any]:
        models = [self.model]
        for fallback in ("gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite"):
            if fallback not in models:
                models.append(fallback)

        last_error: Exception | None = None
        for model in models:
            for attempt in range(2):
                try:
                    interaction = self.client.interactions.create(
                        model=model,
                        input=f"{instructions}\n\nINPUT:\n{input_text}",
                        response_format={
                            "type": "text",
                            "mime_type": "application/json",
                            "schema": schema,
                        },
                    )
                    return json.loads(interaction.output_text)
                except Exception as exc:
                    last_error = exc
                    error_text = str(exc)
                    transient = any(
                        marker in error_text
                        for marker in ("503", "UNAVAILABLE", "RemoteProtocolError", "Server disconnected")
                    )
                    if not transient:
                        raise
                    if attempt == 0:
                        time.sleep(3)

        raise RuntimeError(f"Gemini failed on all fallback models: {last_error}") from last_error
