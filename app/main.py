from fastapi import FastAPI, HTTPException

from app.ai.client import AIAnalysisError, analyze_article
from app.schemas import AnalyzeRequest, ArticleAnalysis, Statement
from app.services.article_extractor import ArticleExtractionError, extract_article

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
        result = analyze_article(title, text)
        statements = [Statement.model_validate(item) for item in result["statements"]]
        return ArticleAnalysis(
            url=request.url,
            title=title,
            text_length=len(text),
            statements=statements,
            status="EXTRACTED" if statements else "NO_STATEMENT_FOUND",
        )
    except ArticleExtractionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except AIAnalysisError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
