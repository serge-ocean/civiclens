from __future__ import annotations

import os

from app.ai.gemini_provider import GeminiProvider
from app.ai.local_provider import LocalOllamaProvider
from app.ai.openai_provider import OpenAIProvider
from app.ai.provider import AIProvider


def get_ai_provider() -> AIProvider:
    provider = os.getenv("AI_PROVIDER", "gemini").lower()
    if provider == "gemini":
        return GeminiProvider()
    if provider == "openai":
        return OpenAIProvider()
    if provider == "local":
        return LocalOllamaProvider()
    raise RuntimeError(f"Unsupported AI_PROVIDER: {provider}")
