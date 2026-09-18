import json
import os

from google import genai
from google.genai import types


MODEL = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")


def main() -> None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY is missing")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL,
        contents="Return exactly this JSON object: {\"status\":\"ok\"}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={"type": "OBJECT", "properties": {"status": {"type": "STRING"}}},
        ),
    )
    result = json.loads(response.text)
    if result.get("status") != "ok":
        raise SystemExit(f"Unexpected response: {result}")
    print(f"Gemini API: OK ({MODEL})")
    print(response.text)


if __name__ == "__main__":
    main()
