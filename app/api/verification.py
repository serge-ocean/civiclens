from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.models import Evidence
from app.services.evidence_search import SearchResult, search_web
from app.services.source_reader import read_source

router = APIRouter(prefix="/verification", tags=["verification"])


class EvidenceSearchRequest(BaseModel):
    claim: str = Field(min_length=3)
    limit: int = Field(default=5, ge=1, le=10)


class EvidenceSearchResponse(BaseModel):
    claim: str
    results: list[Evidence]


class SourceReadRequest(BaseModel):
    url: str


class SourceReadResponse(BaseModel):
    url: str
    title: str | None
    text: str


@router.post("/search", response_model=EvidenceSearchResponse)
def find_evidence(request: EvidenceSearchRequest) -> EvidenceSearchResponse:
    try:
        found: list[SearchResult] = search_web(request.claim, request.limit)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Evidence search failed: {exc}") from exc

    evidence = [
        Evidence(
            source_name=result.title,
            source_url=result.url,
            source_type="OTHER",
            relevance="MEDIUM",
            note=result.snippet,
        )
        for result in found
    ]
    return EvidenceSearchResponse(claim=request.claim, results=evidence)


@router.post("/read-source", response_model=SourceReadResponse)
def read_evidence_source(request: SourceReadRequest) -> SourceReadResponse:
    try:
        source = read_source(request.url)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Source could not be read: {exc}") from exc

    return SourceReadResponse(url=source.url, title=source.title, text=source.text)
