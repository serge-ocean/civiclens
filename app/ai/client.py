import json
import os

from openai import OpenAI


class AIAnalysisError(Exception):
    pass


SYSTEM_PROMPT = """
You are the extraction layer of CivicLens, an AI-assisted civic and political context analysis system.

Your task is to identify public political statements in a source article and break them into claims.
Do not decide whether a politician is good or bad. Do not infer motives. Do not fact-check yet.
Separate what is presented as a factual claim from assessment, prediction, opinion, or unclear wording.
Only use information present in the supplied article. Never invent a speaker, date, quotation, or fact.
If the article paraphrases a statement rather than quoting it, preserve the paraphrase and do not turn it into a quotation.

Return valid JSON only, matching the requested structure.
""".strip()


OUTPUT_SCHEMA = {
    "type": "json_schema",
    "name": "civiclens_extraction",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "statements": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "speaker": {"type": ["string", "null"]},
                        "date": {"type": ["string", "null"]},
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
    },
}


def analyze_article(title: str | None, text: str) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise AIAnalysisError("OPENAI_API_KEY is not configured")

    model = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
    client = OpenAI(api_key=api_key)

    article = f"TITLE:\n{title or '(no title)'}\n\nARTICLE:\n{text}"

    try:
        response = client.responses.create(
            model=model,
            instructions=SYSTEM_PROMPT,
            input=article,
            text={"format": OUTPUT_SCHEMA},
        )
        return json.loads(response.output_text)
    except Exception as exc:
        raise AIAnalysisError(f"OpenAI analysis failed: {exc}") from exc
