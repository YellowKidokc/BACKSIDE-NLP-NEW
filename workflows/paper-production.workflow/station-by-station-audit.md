# Paper Production Station Checklist

## Active stations (run order)

| order | station | output policy | expected outputs | status |
| ---: | --- | --- | --- | --- |
| 1 | `math-translation-layer` | stats / text | text: academic, lossless_summary | metrics: formula_complexity, token_counts, signal_quality | [ ] not run |
| 2 | `classify-documents` | stats | text: (none) | metrics: doc_type, reading_level, spine_mappings, tags, word_count | [ ] not run |
| 3 | `plain-language` | text | text: easy_reading, academic | metrics: readability_delta, word_count | [ ] not run |
| 4 | `claim-extraction` | stats / text | text: claim_list | metrics: claims_count, claims_by_type, quality_flags | [ ] not run |
| 5 | `claim-classification` | stats | text: (none) | metrics: maturity_distribution, domain_distribution, verification_signals | [ ] not run |
| 6 | `master-equation-canon` | stats / text | text: equation_summary | metrics: equation_count, equation_component_count, source_length | [ ] not run |
| 7 | `fruits-spirit-canon` | stats | text: spirit_summary | metrics: fruit_count, dominant_fruit, ranking_top_score | [ ] not run |
| 8 | `sbert-embedder` | stats | text: (none) | metrics: vector_count, embedding_dim, norm_stats | [ ] not run |
| 9 | `paper-intelligence-suite` | stats / text | text: analysis_summary | metrics: insight_count, evidence_density, coverage_flags | [ ] not run |
| 10 | `paper-proof-grader` | stats / text | text: quality_summary | metrics: grade, score, confidence, risk_flags | [ ] not run |

## Explicitly excluded from this workflow

`obsidian-export`, `youtube-fetch`, `youtube-qa`, `youtube-scrape`, `youtube-channel`, `whisper-transcribe`, `whisper-qa`

## Contract source
`station_output_contract.json`
