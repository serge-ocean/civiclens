import json
import os

from openai import OpenAI


class EvidenceEvaluationError(Exception):
    pass


EVALUATION_SCHEMA = {
    "type": "json_schema",
    "name": "civiclens_evidence_evaluation",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "status": {"type": "string", "enum": ["SUPPORTED", "PARTIALLY_SUPPORTED", "UNSUPPORTED", "CONTRADICTED", "INSUFFICIENT_EVIDENCE", "NOT_CHECKABLE"]},
            "confidence": {"type": "integer", "minimum": 0, "maximum": 100},
            "reasoning": {"type": "string"},
            "supports": {"type": "boolean"},
            "missing_information": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["status", "confidence", "reasoning", "supports", "missing_information"],
    },
}


INSTRUCTIONS = """
You are the evidence evaluator for CivicLens.
Compare one claim against one source document. Do not decide whether a politician is good or bad.
Do not infer motives. Do not treat a source's assertion as independently proven merely because it is stated.
Evaluate only what the supplied source actually supports.
Distinguish absence of evidence from evidence of falsity.
Return JSON only.
""".strip()


def evaluate_claim_against_source(claim: str, source_text: str) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EvidenceEvaluationError("OPENAI_API_KEY is not configured")

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
    prompt = f"CLAIM:\n{claim}\n\nSOURCE DOCUMENT:\n{source_text}"

    try:
        response = client.responses.create(
            model=model,
            instructions=INSTRUCTIONS,
            input=prompt,
            text={"format": EVALUATION_SCHEMA},
        )
        return json.loads(response.output_text)
    except Exception as exc:
        raise EvidenceEvaluationError(f"Evidence evaluation failed: {exc}") from exc
