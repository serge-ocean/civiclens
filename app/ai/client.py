from __future__ import annotations

import json

from app.ai.factory import get_ai_provider


class AIAnalysisError(Exception):
    pass


SYSTEM_PROMPT = """
You are the extraction layer of CivicLens, an AI-assisted civic and political context analysis system.

Your task is to identify public political statements in a source article and break them into claims.
Do not decide whether a politician is good or bad. Do not infer motives. Do not fact-check yet.
Separate what is presented as a factual claim from assessment, prediction, opinion, or unclear wording.
Only use information present in the supplied article. Never invent a speaker, date, quotation, or fact.
If the article paraphrases a statement rather than quoting it, preserve the paraphrase and do not turn it into a quotation.
If speaker or date is not available in the article, return an empty string for that field.

Return valid JSON only, matching the requested structure.
""".strip()


# Gemini's structured-output schema does not accept JSON Schema union types such as
# ["string", "null"] in this configuration. Use empty strings for unknown optional
# text fields so the same schema works reliably across providers.
OUTPUT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "statements": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "speaker": {"type": "string"},
                    "date": {"type": "string"},
                    "text": {"type": "string"},
                    "claims": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "text": {"type": "string"},
                                "claim_type": {
                                    "type": "string",
                                    "enum": ["FACT", "ASSESSMENT", "PREDICTION", "OPINION", "UNCLEAR"],
                                },
                                "checkable": {"type": "boolean"},
                            },
                            "required": ["text", "claim_type", "checkable"],
                        },
                    },
                },
                "required": ["speaker", "date", "text", "claims"],
            },
        }
    },
    "required": ["statements"],
}


def analyze_article(title: str | None, text: str) -> dict:
    article = f"TITLE:\n{title or '(no title)'}\n\nARTICLE:\n{text}"
    try:
        provider = get_ai_provider()
        return provider.generate_json(
            instructions=SYSTEM_PROMPT,
            input_text=article,
            schema=OUTPUT_SCHEMA,
        )
    except Exception as exc:
        raise AIAnalysisError(f"AI analysis failed: {exc}") from exc
