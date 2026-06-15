# paper-recommender.station

## Purpose
Given a paper, article, or set of claims, find related academic papers via Semantic Scholar API. Returns citation networks, related papers, and correlation candidates.

## Input
- Paper title, abstract, or claim set
- Optional: positive/negative paper IDs for preference-weighted recommendations
- Optional: preference engine bias signal

## Output
- Ranked list of related papers with metadata (title, authors, year, citation count, abstract, S2 ID)
- Citation graph snippet
- Correlation candidates for Theophysics cross-domain mapping

## Export Contract
- JSON recommendation exports go to `EXPORTS\json\`.
- Markdown recommendation reports go to `EXPORTS\reports\`.
- Source/provenance copies, if needed, go to `EXPORTS\source_copies\`.
- Do not leave active exports in child folders outside station-root `EXPORTS\`.

## Model Dependencies
- 16_paper_recommender (Semantic Scholar Python client — API, no local weights)
- 02_embedder (optional: local similarity pre-filter)

## Workflow Lanes
- 10_RIGOR (finding supporting/contradicting literature)
- Publication Layer (citation suggestions)

## Status: SKELETON — needs implementation

## Notes
Semantic Scholar API is free with rate limits. API key optional but recommended.
`pip install semanticscholar` — already installed in venv.
Key endpoints:
- get_paper(id) — full paper metadata
- search_paper(query) — keyword search
- get_recommended_papers(paper_id) — similar papers
- recommendations with positive/negative IDs — preference-weighted discovery
This is the station that answers "what existing research supports or challenges this claim?"
