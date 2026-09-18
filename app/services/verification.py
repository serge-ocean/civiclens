from app.models import (
    ClaimAnalysis,
    Context,
    ManipulationFinding,
    Verification,
)


def build_initial_verification(claim: str) -> ClaimAnalysis:
    """Create a conservative verification record before external evidence is collected.

    This module deliberately does not decide whether a claim is true or false.
    It records the current evidence state and what still needs to be checked.
    """
    return ClaimAnalysis(
        claim=claim,
        status="INSUFFICIENT_EVIDENCE",
        verification=Verification(
            status="INSUFFICIENT_EVIDENCE",
            confidence=0,
            evidence=[],
            missing_information=[
                "Find the primary source for the claim.",
                "Find independent or documentary evidence.",
                "Check relevant dates and surrounding context.",
            ],
            reasoning="No external evidence has been collected yet.",
        ),
        context=Context(
            relevant_context=[],
            omitted_context=[],
            uncertainty=["Verification has not yet been performed."],
        ),
        manipulation=[],
    )
