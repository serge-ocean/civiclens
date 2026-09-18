from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class SourceDocument:
    url: str
    title: str | None
    text: str


def read_source(url: str, max_chars: int = 30000) -> SourceDocument:
    response = requests.get(
        url,
        timeout=15,
        headers={"User-Agent": "CivicLens/0.1"},
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "nav", "footer"]):
        tag.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else None
    main = soup.find("article") or soup.find("main") or soup.body
    if main is None:
        raise ValueError("No readable source body found")

    paragraphs = [
        p.get_text(" ", strip=True)
        for p in main.find_all(["p", "h1", "h2", "h3"])
    ]
    text = "\n\n".join(p for p in paragraphs if p)
    if not text:
        raise ValueError("No readable source text found")

    return SourceDocument(url=url, title=title, text=text[:max_chars])
