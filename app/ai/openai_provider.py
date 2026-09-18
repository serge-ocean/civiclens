from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI

from app.ai.provider import AIProvider


class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        self.client = OpenAI(api_key=self.api_key)

    def generate_json(self, *, instructions: str, input_text: str, schema: dict[str, Any]) -> dict[str, Any]:
        response = self.client.responses.create(
            model=self.model,
            instructions=instructions,
            input=input_text,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "civiclens_output",
                    "strict": True,
                    "schema": schema,
                }
            },
        )
        return json.loads(response.output_text)
