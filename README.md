# CivicLens

AI-assisted civic and political context analysis for Moldova.

## Beta v0.1

The first milestone is intentionally small: accept a source URL, extract the article text and public statements, identify verifiable claims, and return structured JSON for later review.

The system is designed to distinguish facts, claims, assessments, uncertainty, context, legal/procedural questions, manipulation indicators, and historical statements. It does not assign political preferences or determine whether a politician is good or bad.

## Planned pipeline

`Source → Extraction → Claims → Evidence → Context → History → Review → Telegram`

## Status

Architecture and methodology are being implemented incrementally. Automated publication is disabled until human review is in place.
