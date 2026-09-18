from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

from app.models import ClaimAnalysis


class AnalyzeRequest(BaseModel):
    url: HttpUrl


class Claim(BaseModel):
    text: str
    claim_type: Literal["FACT", "ASSESSMENT", "PREDICTION", "OPINION", "UNCLEAR"]
    checkable: bool


class Statement(BaseModel):
    speaker: str | None = None
    date: str | None = None
    text: str
    claims: list[Claim] = Field(default_factory=list)


class ArticleAnalysis(BaseModel):
    url: HttpUrl
    title: str | None = None
    text_length: int
    statements: list[Statement] = Field(default_factory=list)
    status: Literal["EXTRACTED", "NO_STATEMENT_FOUND", "ERROR"]
    verification: list[ClaimAnalysis] = Field(default_factory=list)
