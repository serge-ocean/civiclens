import json
import os

from app.ai.client import analyze_article
from app.services.article_extractor import extract_article


URL = os.getenv(
    "CIVICLENS_TEST_URL",
    "https://point.md/ru/novosti/proisshestviya/vozle-kolonitsy-obnaruzhili-fragmenty-drona/",
)


def main() -> None:
    print(f"Fetching: {URL}")
    title, text = extract_article(URL)
    print(f"Title: {title}")
    print(f"Article characters: {len(text)}")

    result = analyze_article(title, text)
    statements = result.get("statements", [])
    print(f"Statements found: {len(statements)}")

    for index, statement in enumerate(statements, start=1):
        print(f"\nStatement {index}: {statement.get('speaker') or 'unknown speaker'}")
        print(statement.get("text", ""))
        for claim in statement.get("claims", []):
            print(
                "  - "
                f"[{claim.get('claim_type')}] "
                f"checkable={claim.get('checkable')}: {claim.get('text', '')}"
            )

    print("\nJSON result:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
