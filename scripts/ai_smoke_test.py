import json
import os
import time

from google import genai
from google.genai import types


MODELS = list(dict.fromkeys([
    os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
]))


def main() -> None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY is missing")

    client = genai.Client(api_key=api_key)
    last_error = None

    for model in MODELS:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents='Return exactly this JSON object: {"status":"ok"}',
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema={
                            "type": "OBJECT",
                            "properties": {"status": {"type": "STRING"}},
                        },
                    ),
                )
                result = json.loads(response.text)
                if result.get("status") != "ok":
                    raise SystemExit(f"Unexpected response: {result}")
                print(f"Gemini API: OK ({model})")
                print(response.text)
                return
            except Exception as exc:
                last_error = exc
                if "503" not in str(exc) and "UNAVAILABLE" not in str(exc):
                    raise
                if attempt == 0:
                    time.sleep(2)

    raise SystemExit(f"All Gemini models are temporarily unavailable. Last error: {last_error}")


if __name__ == "__main__":
    main()
