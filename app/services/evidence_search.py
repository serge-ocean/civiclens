from dataclasses import dataclass
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str


def search_web(claim: str, limit: int = 5) -> list[SearchResult]:
    """Small, dependency-light prototype search using DuckDuckGo HTML.

    This is deliberately a discovery layer, not a truth oracle. Every result
    must later be evaluated and attributed before it can affect verification.
    """
    query = quote_plus(claim)
    url = f"https://html.duckduckgo.com/html/?q={query}"
    response = requests.get(
        url,
        timeout=15,
        headers={"User-Agent": "CivicLens/0.1"},
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    results: list[SearchResult] = []

    for item in soup.select(".result")[:limit]:
        link = item.select_one(".result__a")
        snippet = item.select_one(".result__snippet")
        if not link:
            continue
        results.append(
            SearchResult(
                title=link.get_text(" ", strip=True),
                url=link.get("href", ""),
                snippet=snippet.get_text(" ", strip=True) if snippet else "",
            )
        )

    return results
