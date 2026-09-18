import re

from app.schemas import ArticleAnalysis, Claim, Statement


POLITICAL_VERBS = (
    "заявил", "заявила", "сказал", "сказала", "сообщил", "сообщила",
    "отметил", "отметила", "утверждает", "утверждают", "по словам",
    "declarat", "a spus", "a afirmat", "potrivit",
)


def _looks_like_statement(paragraph: str) -> bool:
    lower = paragraph.lower()
    return any(verb in lower for verb in POLITICAL_VERBS) or '"' in paragraph or "«" in paragraph


def extract_statements(url: str, title: str | None, text: str) -> ArticleAnalysis:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    statements: list[Statement] = []

    for paragraph in paragraphs:
        if not _looks_like_statement(paragraph):
            continue

        quoted = re.findall(r'«([^»]+)»|“([^”]+)”|"([^"]+)"', paragraph)
        quotes = [next(part for part in match if part) for match in quoted]
        statement_text = " ".join(quotes).strip() if quotes else paragraph
        claim_type = "FACT" if any(char.isdigit() for char in statement_text) else "UNCLEAR"
        claims = [Claim(text=statement_text, claim_type=claim_type, checkable=True)]
        statements.append(Statement(text=statement_text, claims=claims))

    return ArticleAnalysis(
        url=url,
        title=title,
        text_length=len(text),
        statements=statements,
        status="EXTRACTED" if statements else "NO_STATEMENT_FOUND",
    )
