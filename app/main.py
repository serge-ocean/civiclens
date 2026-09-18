from fastapi import FastAPI, HTTPException

from app.schemas import AnalyzeRequest, ArticleAnalysis
from app.services.article_extractor import ArticleExtractionError, extract_article
from app.services.statement_extractor import extract_statements

app = FastAPI(title="CivicLens", version="0.1.0")


@app.get("/")
def root() -> dict[str, str]:
    return {"name": "CivicLens", "status": "ok", "version": "0.1.0"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/analyze", response_model=ArticleAnalysis)
def analyze(request: AnalyzeRequest) -> ArticleAnalysis:
    try:
        title, text = extract_article(str(request.url))
        return extract_statements(str(request.url), title, text)
    except ArticleExtractionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
