from bs4 import BeautifulSoup
import requests


class ArticleExtractionError(Exception):
    pass


def extract_article(url: str) -> tuple[str | None, str]:
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "CivicLens/0.1 (+https://github.com/serge-ocean/civiclens)"},
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ArticleExtractionError(f"Could not fetch URL: {exc}") from exc

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else None
    main = soup.find("article") or soup.find("main") or soup.body
    if main is None:
        raise ArticleExtractionError("No readable page body found")

    paragraphs = [
        p.get_text(" ", strip=True)
        for p in main.find_all(["p", "h1", "h2", "h3"])
    ]
    text = "\n\n".join(p for p in paragraphs if p)

    if not text:
        raise ArticleExtractionError("No article text found")

    return title, text
