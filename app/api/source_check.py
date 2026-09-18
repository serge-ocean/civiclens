from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.source_reader import read_source

router = APIRouter(prefix="/verification", tags=["verification"])


class SourceCheckRequest(BaseModel):
    claim: str = Field(min_length=3)
    source_url: str


class SourceCheckResponse(BaseModel):
    claim: str
    source_url: str
    source_title: str | None
    source_text: str
    note: str


@router.post("/read-source", response_model=SourceCheckResponse)
def read_evidence_source(request: SourceCheckRequest) -> SourceCheckResponse:
    try:
        document = read_source(request.source_url)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Could not read source: {exc}") from exc

    return SourceCheckResponse(
        claim=request.claim,
        source_url=document.url,
        source_title=document.title,
        source_text=document.text,
        note="Source content retrieved. It has not been classified as supporting or contradicting the claim yet.",
    )
