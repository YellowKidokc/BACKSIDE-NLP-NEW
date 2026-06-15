# MDA Workflow Test Results

Run: 20260604-190145
Root: `X:\WORKFLOWS\MDA-PUBLICATION`

| Station | Check | Status | Detail |
|---|---|---|---|
| 01_LOSSLESS | manifest_count_match | PASS | manifest=61; lossless_md=61; missing=[]; extra=[] |
| 02_CLASSIFIED | type_counts_and_manifest_coverage | PASS | classified_md=61; issues=[] |
| 03_SCORED | two_lane_report_coverage | PASS | reports=62; missing=[]; extra=[MDA-000-series-map] |
| 03_SCORED\series-flow | hard_gate | REVIEW | verdict=review_required; pass_ratio=0.6415; required=0.8; flagged=19 |
| 05_READING_LEVELS | variant_coverage | PASS | easy=61; academic=61; terms=61; missing_easy=[]; missing_academic=[]; missing_terms=[] |
| 06_HTML_BUILD | reader_html_coverage | PASS | reader_html=62; missing=[] |
| 06_HTML_BUILD | reader_mode_controls | PASS | missing_controls=[] |
| 08_DEPLOY_READY | manifest_page_coverage | PASS | deploy_html=63; missing=[] |
