import os

from openai import OpenAI


MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")


def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is missing")

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=MODEL,
        input="Return exactly this JSON object: {\"status\":\"ok\"}",
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
