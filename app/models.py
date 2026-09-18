from pydantic import BaseModel, Field
from typing import Literal


ClaimStatus = Literal[
    "SUPPORTED",
    "PARTIALLY_SUPPORTED",
    "UNSUPPORTED",
    "CONTRADICTED",
    "INSUFFICIENT_EVIDENCE",
    "NOT_CHECKABLE",
]


class Evidence(BaseModel):
    source_name: str
    source_url: str | None = None
    source_type: Literal[
        "PRIMARY",
        "OFFICIAL",
        "MEDIA",
        "EXPERT",
        "DOCUMENT",
        "OTHER",
    ] = "OTHER"
    supports: bool | None = None
    relevance: Literal["HIGH", "MEDIUM", "LOW"] = "MEDIUM"
    note: str = ""


class Verification(BaseModel):
    status: ClaimStatus
    confidence: int = Field(ge=0, le=100)
    evidence: list[Evidence] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    reasoning: str = ""


class Context(BaseModel):
    relevant_context: list[str] = Field(default_factory=list)
    omitted_context: list[str] = Field(default_factory=list)
    uncertainty: list[str] = Field(default_factory=list)


class Contradiction(BaseModel):
    previous_statement: str
    previous_date: str | None = None
    current_statement: str
    current_date: str | None = None
    relationship: Literal["CONSISTENT", "POSSIBLE_CHANGE", "POSSIBLE_CONTRADICTION"]
    explanation_found: bool = False
    explanation: str | None = None


class ManipulationFinding(BaseModel):
    type: Literal[
        "SELECTIVE_CONTEXT",
        "UNSUPPORTED_CERTAINTY",
        "EMOTIONAL_FRAMING",
        "FALSE_DICHOTOMY",
        "CHERRY_PICKING",
        "APPEAL_TO_AUTHORITY",
        "MISLEADING_STATISTIC",
        "OTHER",
    ]
    severity: Literal["LOW", "MEDIUM", "HIGH"]
    explanation: str
    evidence: list[str] = Field(default_factory=list)


class ClaimAnalysis(BaseModel):
    claim: str
    status: ClaimStatus
    verification: Verification
    context: Context = Field(default_factory=Context)
    manipulation: list[ManipulationFinding] = Field(default_factory=list)


class VerificationReport(BaseModel):
    claims: list[ClaimAnalysis] = Field(default_factory=list)
    overall_uncertainties: list[str] = Field(default_factory=list)
    methodology_note: str = "Evidence strength and uncertainty are reported separately; absence of evidence is not treated as proof of falsity."
