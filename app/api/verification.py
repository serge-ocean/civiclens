from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.models import Evidence
from app.services.evidence_search import SearchResult, search_web

router = APIRouter(prefix="/verification", tags=["verification"])


class EvidenceSearchRequest(BaseModel):
    claim: str = Field(min_length=3)
    limit: int = Field(default=5, ge=1, le=10)


class EvidenceSearchResponse(BaseModel):
    claim: str
    results: list[Evidence]


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
