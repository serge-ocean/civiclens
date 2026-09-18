import json
import os
import time

from google import genai


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
                interaction = client.interactions.create(
                    model=model,
                    input='Return exactly this JSON object: {"status":"ok"}',
                    response_format={
                        "type": "text",
                        "mime_type": "application/json",
                        "schema": {
                            "type": "object",
                            "properties": {"status": {"type": "string"}},
                            "required": ["status"],
                        },
                    },
                )
                result = json.loads(interaction.output_text)
                if result.get("status") != "ok":
                    raise SystemExit(f"Unexpected response: {result}")
                print(f"Gemini API: OK ({model})")
                print(interaction.output_text)
                return
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

    raise SystemExit(f"All Gemini models are temporarily unavailable. Last error: {last_error}")


if __name__ == "__main__":
    main()
