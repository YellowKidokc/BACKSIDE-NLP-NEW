# Theophysics Paper Intelligence Variable Inventory

Purpose: document the suite folder by folder so the public snapshot, Excel workbook, and open-source scoring surface stay aligned.

## 00_ORCHESTRATOR

Role: traffic controller. This folder does not grade the paper directly. It assigns identity, calls every scoring layer, tracks layer health, builds run outputs, writes snapshots, and controls Excel column ordering.

Primary scripts:

- `run_pipeline.py` - main single-paper and series orchestrator.
- `run_drop_zone.py` - autonomous drop-zone runner for paper, brain, or both.
- `run_brain_alignment.py` - paper intelligence plus brain/vault alignment runner.
- `run_baseline.py` - baseline runner.
- `run_convergence_batch.py` - convergence batch runner.

### Public-Facing Variables

These should appear in the public snapshot or public report because they explain what was run and whether it can be trusted.

| Variable | Meaning | Public Use |
|---|---|---|
| `paper_id` | Stable hash-based paper identifier. | Identity strip. |
| `file` | Source filename. | Identity strip / audit trail. |
| `series_id` | Stable series/run grouping identifier. | Corpus comparison. |
| `run_id` | Timestamped run identifier. | Reproducibility. |
| `schema_version` | Scoring schema version. | Reproducibility / open-source audit. |
| `source_path` | Full source path used for scoring. | Internal audit; public version may redact/localize. |
| `analyzed_at` | Timestamp when analysis ran. | Audit trail. |
| `snapshot_path` | Path to generated snapshot JSON. | Links public card to machine-readable evidence. |
| `layer_status` / `_layer_status` | Per-layer status: `ok`, `error`, `skipped`, or `partial`. | Must be visible so readers know what ran. |

### Internal / Workbook Variables

These are mostly for Excel mechanics, not the one-screen public snapshot.

| Variable / Constant | Meaning |
|---|---|
| `SCHEMA_VERSION` | Current orchestrator schema marker: `2026.04.07-B`. |
| `LAYER_COLORS` | Excel header color map by layer prefix. |
| `IDENTITY_COLUMNS` | Columns pinned at the front of the Excel sheet. |
| `LAYER_ORDER` | Workbook order: `PA`, `L1`, `L2`, `L3`, `L4`, `L5`, `L6`, `L7`, `L8`, `L9`, `L10`, `L13`. |

### Folder-Level Output Types

| Output | Produced By | Meaning |
|---|---|---|
| `*_PAPER_INTELLIGENCE_*.xlsx` | `write_excel()` when `openpyxl` is available. | Full metric workbook. |
| `*_pipeline_results_*.json` | Single or series run. | Machine-readable full row data. |
| `*_run_summary_*.json` | Single or series run. | One-glance layer health and run metadata. |
| `snapshots/<paper_id>_snapshot.json` | Snapshot merge layer. | Public snapshot source data. |
| `knowledge_graph_*.json/html/graphml` | L7 graph builder. | Corpus relationship map. |

### Notes For The Public Snapshot

The orchestrator contributes the top and bottom rails of the snapshot:

- Identity Strip: `paper_id`, `file/title`, `series_id`, `schema_version`, `run_id`.
- Audit Health: `_layer_status`, especially whether OpenAI layers were skipped or local NLP layers errored.
- Machine Link: `snapshot_path`.

It should not decide the claim maturity, evidence bar, kill conditions, or not-claimed section. Those belong to the scoring/prompt layers.

### Current GTQ HTML Test Result

The real suite successfully ran GTQ HTML files through the single-paper path. Series mode currently scans numbered `.md` files only, so GTQ HTML batch runs need either:

1. A wrapper that calls `analyze_paper()` for each `gtq-*.html`, or
2. A small orchestrator update to let `analyze_series()` include `.html`.

The wrapper path is safer for now because it does not alter the existing suite.

Layer status from the two-page smoke test:

| Layer | Status |
|---|---|
| `PA` | ok |
| `L1` | ok |
| `L2` | ok |
| `L3` | ok |
| `L4` | skipped |
| `L5` | ok |
| `L6` | ok |
| `L8` | error - missing local dependency/model cache |
| `L9` | error - missing local packages |
| `L10` | error - missing local package |
| `L13` | skipped |

## 01_TEXT_ANALYTICS

Role: first real scoring folder. It contains two different text passes:

- `paper_analyzer.py` - the ground-up paper analyzer, exported with `PA_` prefixes.
- `text_analyzer.py` - readability / keywords / n-grams pass, exported with `L1_` prefixes.

Important note for GTQ HTML: this folder currently reads `.html` as raw text. It does not fully strip CSS, navigation, or markup before scoring. The suite can run HTML as-is, but public-facing text metrics should use a clean text extraction step first, otherwise keyword/n-gram metrics can be contaminated by page code such as `font size`, `color var`, and `div class`.

### PA - Paper Analyzer

Public name: **Paper Analyzer / Ground Truth Structure**

This is the first real grade-like layer. It measures structural baseline, grammar availability, semantic drift, information density, readability availability, argument structure, flow, and link topology.

#### PA Public-Facing Variables

These are good candidates for the public score page because they summarize whether the paper behaves like a serious argument.

| Variable | Meaning | Public Label |
|---|---|---|
| `PA_a_argument_grade` | Main argument grade from claims, evidence, evidence ratio, and falsifiability markers. | Argument Grade |
| `PA_sm_coherence_flag` | Topic drift classification: coherent/moderate/scattered. | Coherence Flag |
| `PA_d_density_label` | Compression-based information density class. | Density |
| `PA_f_flow_label` | Transition density / flow class. | Flow |
| `PA_a_claim_count` | Count of detected claim markers. | Claims |
| `PA_a_evidence_count` | Count of detected evidence markers. | Evidence Hooks |
| `PA_a_evidence_to_claim_ratio` | Evidence markers divided by claim markers. | Evidence-to-Claim Ratio |
| `PA_a_falsifiability_markers` | Count of falsification/test markers. | Falsifiability Hooks |
| `PA_lk_cross_domain_bridges` | Count of physics/theology/math/moral bridge markers. | Cross-Domain Bridges |
| `PA_lk_link_quality_score` | Link topology quality score. | Link Quality |
| `PA_lk_underlink_flag` | Whether the paper appears underlinked. | Underlinked? |
| `PA_lk_overlink_flag` | Whether the paper appears overlinked. | Overlinked? |

#### PA Workbook Variables

All PA variables should remain in Excel, but most do not belong on the one-screen snapshot.

| Group | Variables |
|---|---|
| Structural baseline | `PA_s_word_count`, `PA_s_unique_word_count`, `PA_s_ttr`, `PA_s_sentence_count`, `PA_s_paragraph_count`, `PA_s_header_count`, `PA_s_avg_words_per_sentence`, `PA_s_avg_sentences_per_paragraph` |
| Grammar | `PA_g_pos_note` or, when spaCy is available, POS / passive / modal / assertive metrics from `l2_grammar()` |
| Semantic drift | `PA_sm_topic_drift_avg`, `PA_sm_topic_drift_max`, `PA_sm_topic_drift_scores`, `PA_sm_coherence_flag` |
| Information density | `PA_d_compression_ratio`, `PA_d_density_label`, `PA_d_stopword_ratio`, `PA_d_trigram_redundancy`, `PA_d_signal_noise_ratio` |
| Readability | `PA_r_readability_note` or, when textstat is available, grade/load metrics from `l5_readability()` |
| Argument structure | `PA_a_claim_count`, `PA_a_claim_density_per1k`, `PA_a_evidence_count`, `PA_a_evidence_density_per1k`, `PA_a_evidence_to_claim_ratio`, `PA_a_falsifiability_markers`, `PA_a_argument_grade` |
| Flow | `PA_f_transition_density_pct`, `PA_f_transition_count`, `PA_f_flow_label` |
| Link topology | `PA_lk_total_links`, `PA_lk_link_density_per1k`, `PA_lk_link_citation`, `PA_lk_link_concept`, `PA_lk_link_dependency`, `PA_lk_link_evidence`, `PA_lk_link_navigation`, `PA_lk_internal_links`, `PA_lk_external_links`, `PA_lk_internal_external_ratio`, `PA_lk_cross_domain_bridges`, `PA_lk_link_quality_score`, `PA_lk_underlink_flag`, `PA_lk_overlink_flag`, `PA_lk_concept_nodes`, `PA_lk_concept_edges`, `PA_lk_avg_degree`, `PA_lk_clustering_coeff`, `PA_lk_most_central_paragraph`, `PA_lk_centralization`, `PA_lk_isolated_nodes` |

#### PA Test Value From GTQ Smoke Run

For `gtq-01-measurement-collapsed-reality.html`, the first real grade was:

| Variable | Value |
|---|---|
| `PA_a_argument_grade` | `A - Evidence-Rich` |
| `PA_sm_coherence_flag` | `SCATTERED` |
| `PA_d_density_label` | `HIGH` |
| `PA_f_flow_label` | `HIGH` |
| `PA_a_claim_count` | `7` |
| `PA_a_evidence_count` | `67` |
| `PA_a_evidence_to_claim_ratio` | `9.57` |
| `PA_a_falsifiability_markers` | `17` |

Interpretation caution: because the input was raw HTML, these values may include page chrome/code noise. They prove the engine runs, not that the final public grade is clean.

### L1 - Text Analytics

Public name: **Readability / Keyword Surface**

This pass measures simple text statistics, optional readability formulas, optional KeyBERT/YAKE keywords, and n-gram clusters.

#### L1 Public-Facing Variables

| Variable | Meaning | Public Label |
|---|---|---|
| `L1_word_count` | Total token count. | Word Count |
| `L1_unique_word_count` | Unique token count. | Unique Words |
| `L1_vocab_richness` | Unique words divided by total words. | Vocabulary Richness |
| `L1_paragraph_count` | Paragraph count. | Paragraphs |
| `L1_header_count` | Markdown header count. | Headers |
| `L1_avg_paragraph_words` | Average words per paragraph. | Avg Paragraph Length |
| `L1_flesch_reading_ease` | Readability score if `textstat` is installed. | Reading Ease |
| `L1_flesch_kincaid_grade` | Grade-level score if `textstat` is installed. | Grade Level |
| `L1_keybert_keywords` | Semantic keyword extraction if model/cache exists. | KeyBERT Keywords |
| `L1_yake_keywords` | YAKE keyword extraction if package exists. | YAKE Keywords |
| `L1_top_bigrams` | Most common 2-word phrases. | Top Bigrams |
| `L1_top_trigrams` | Most common 3-word phrases. | Top Trigrams |

#### L1 Workbook Variables

When optional packages are installed, `readability_suite()` may add:

- `L1_flesch_reading_ease`
- `L1_flesch_kincaid_grade`
- `L1_gunning_fog`
- `L1_smog_index`
- `L1_automated_readability`
- `L1_coleman_liau`
- `L1_dale_chall`
- `L1_text_standard`
- `L1_reading_time_min`
- `L1_syllable_count`
- `L1_lexicon_count`
- `L1_sentence_count`

#### L1 Test Value From GTQ Smoke Run

For `gtq-01-measurement-collapsed-reality.html`, the current raw HTML run produced:

| Variable | Value |
|---|---|
| `L1_word_count` | `12849` |
| `L1_unique_word_count` | `4171` |
| `L1_vocab_richness` | `0.3246` |
| `L1_paragraph_count` | `74` |
| `L1_header_count` | `0` |
| `L1_avg_paragraph_words` | `173.6` |
| `L1_top_bigrams` | `font size | color var | div class | div div | border radius | font family` |
| `L1_top_trigrams` | `font size color | color var highlight | div div class | serif font size` |

Interpretation: this confirms that HTML is not being cleaned enough for public text metrics. The next engineering fix should be a shared input normalizer used before `PA` and `L1`.

## 02_ACADEMIC_STANDARD

Role: academic-scoring layer. This folder measures citations, references, external theory signals, academic structure, claim/evidence/falsifiability density, hedging vs absolute language, equations, and a no-API publication-style rubric.

Primary script:

- `academic_scorer.py` - exported with `L2_` prefixes.

### Public-Facing Variables

These should be visible on a public score page because they explain whether the paper looks academically grounded, overclaimed, falsifiable, and structurally complete.

| Variable | Meaning | Public Label |
|---|---|---|
| `L2_academic_grade` | Top-level academic grade label. | Academic Grade |
| `L2_academic_rubric_total` | 0-25 academic rubric total. | Academic Rubric Score |
| `L2_academic_rubric_grade` | Rubric letter/category. | Rubric Grade |
| `L2_structure_score` | Presence of abstract, intro, methods, results, discussion, conclusion, references. | Structure Completeness |
| `L2_citation_count` | Total detected citation/reference markers. | Citations |
| `L2_citation_density_per1k` | Citation markers per thousand words. | Citation Density |
| `L2_external_theory_count` | Count of recognized external theory references. | External Theory Hooks |
| `L2_external_theories` | Which theory families were detected. | Theory References |
| `L2_claim_marker_count` | Claim markers detected. | Claim Markers |
| `L2_evidence_marker_count` | Evidence markers detected. | Evidence Markers |
| `L2_evidence_to_claim_ratio` | Evidence markers divided by claim markers. | Evidence-to-Claim Ratio |
| `L2_falsifiability_marker_count` | Falsifiability/test markers. | Falsifiability Markers |
| `L2_hedge_to_absolute_ratio` | Hedge language divided by absolute claim language. | Hedge-to-Absolute Ratio |
| `L2_counterargument_count` | Counterargument/objection markers. | Counterarguments |
| `L2_limitation_count` | Limitation/boundary markers. | Limitations |
| `L2_equation_count` | Equation/math markers. | Equations |
| `L2_equation_density_per1k` | Equation markers per thousand words. | Equation Density |

### Rubric Variables

The no-API academic rubric is scored out of 25 points:

| Variable | Meaning |
|---|---|
| `L2_rubric_structure_points` | Up to 5 points for academic section structure. |
| `L2_rubric_grounding_points` | Up to 5 points for citations, reference entries, and DOI grounding. |
| `L2_rubric_claim_points` | Up to 5 points for claim/evidence balance. |
| `L2_rubric_quantitative_points` | Up to 5 points for equations and quantitative markers. |
| `L2_rubric_falsifiability_points` | Up to 5 points for falsifiability, counterarguments, and limitations. |
| `L2_academic_rubric_total` | Sum of the five rubric areas. |
| `L2_academic_rubric_grade` | A/B/C/D/F label for the rubric total. |

### Workbook Variables

All L2 variables should remain in Excel:

- `L2_title_detected`
- `L2_citation_count`
- `L2_author_year_citation_count`
- `L2_numeric_citation_count`
- `L2_citation_density_per1k`
- `L2_external_theory_count`
- `L2_external_theories`
- `L2_academic_signal_count`
- `L2_academic_signal_density`
- `L2_structure_score`
- `L2_heading_count`
- `L2_reference_entry_count`
- `L2_has_abstract`
- `L2_has_introduction`
- `L2_has_methodology`
- `L2_has_results`
- `L2_has_discussion`
- `L2_has_conclusion`
- `L2_has_references_section`
- `L2_footnote_count`
- `L2_url_references`
- `L2_doi_references`
- `L2_claim_marker_count`
- `L2_claim_density_per1k`
- `L2_evidence_marker_count`
- `L2_evidence_density_per1k`
- `L2_evidence_to_claim_ratio`
- `L2_falsifiability_marker_count`
- `L2_falsifiability_density_per1k`
- `L2_hedge_count`
- `L2_hedge_density_per1k`
- `L2_absolute_claim_count`
- `L2_absolute_density_per1k`
- `L2_hedge_to_absolute_ratio`
- `L2_counterargument_count`
- `L2_limitation_count`
- `L2_novelty_marker_count`
- `L2_definition_marker_count`
- `L2_quantitative_marker_count`
- `L2_equation_count`
- `L2_equation_density_per1k`
- `L2_claim_candidate_1`
- `L2_claim_candidate_2`
- `L2_claim_candidate_3`
- `L2_evidence_candidate_1`
- `L2_evidence_candidate_2`
- `L2_rubric_structure_points`
- `L2_rubric_grounding_points`
- `L2_rubric_claim_points`
- `L2_rubric_quantitative_points`
- `L2_rubric_falsifiability_points`
- `L2_academic_rubric_total`
- `L2_academic_rubric_grade`
- `L2_academic_grade`

### GTQ Smoke Test Values

For `gtq-01-measurement-collapsed-reality.html`:

| Variable | Value |
|---|---|
| `L2_academic_grade` | `A (Publication Grade)` |
| `L2_academic_rubric_total` | `23.0` |
| `L2_academic_rubric_grade` | `A (Rigorous)` |
| `L2_structure_score` | `7/7` |
| `L2_citation_count` | `28` |
| `L2_external_theory_count` | `9` |
| `L2_claim_marker_count` | `6` |
| `L2_evidence_marker_count` | `69` |
| `L2_evidence_to_claim_ratio` | `11.5` |
| `L2_falsifiability_marker_count` | `11` |
| `L2_hedge_to_absolute_ratio` | `0.16` |
| `L2_equation_count` | `735` |

Interpretation caution: the raw HTML run inflated equation/quantitative markers and polluted claim/evidence candidates with JavaScript snippets. The grade engine runs, but public scoring needs clean article text.

## 03_THEOPHYSICS_METRICS

Role: framework-specific scoring layer. This folder measures whether a paper carries the Theophysics signal: CHI/coherence language, wisdom vs knowledge balance, fruits of the Spirit, Master Equation variable coverage, cross-domain bridges, scripture references, and CKG tier.

Primary script:

- `theophysics_scorer.py` - exported with `L3_` prefixes.

### Public-Facing Variables

These should be visible on the public score page because they explain how strongly the paper expresses the internal framework.

| Variable | Meaning | Public Label |
|---|---|---|
| `L3_chi_score` | Coherence/CHI term score, capped 0-10. | CHI Score |
| `L3_chi_status` | CHI tier: weak/moderate/strong/high. | CHI Status |
| `L3_wisdom_score` | Wisdom/theological language density. | Wisdom Score |
| `L3_knowledge_score` | Scientific/technical language density. | Knowledge Score |
| `L3_wk_ratio` | Wisdom score divided by knowledge score. | Wisdom / Knowledge Ratio |
| `L3_wk_status` | Wisdom-led, balanced, or knowledge-dominant. | W/K Status |
| `L3_fruits_composite` | Fruits of Spirit composite, 0-10. | Fruits Composite |
| `L3_dominant_fruit` | Highest detected fruit dimension. | Dominant Fruit |
| `L3_me_avg_score` | Average Master Equation variable coverage. | Master Equation Average |
| `L3_me_dominant_variable` | Strongest Master Equation variable. | Dominant ME Variable |
| `L3_cross_domain_bridges` | Bridge markers across domains. | Cross-Domain Bridges |
| `L3_scripture_refs` | Scripture/reference marker count. | Scripture References |
| `L3_ckg_raw` | CKG raw score, capped at 100. | CKG Raw |
| `L3_ckg_tier` | CKG grade/tier. | CKG Tier |

### Master Equation Variable Columns

These should be in Excel and can also become a visual bar chart in the public/internal score page.

| Variable | Meaning |
|---|---|
| `L3_me_G_gravity_belonging` | Gravity / belonging / binding language. |
| `L3_me_M_mass_meaning` | Mass / meaning / purpose / covenant language. |
| `L3_me_E_entropy_engagement` | Entropy / energy / work / decay language. |
| `L3_me_S_spacetime_structure` | Spacetime / geometry / structure language. |
| `L3_me_T_time_eternity` | Time / eternity / sequence / duration language. |
| `L3_me_K_knowledge_logos` | Knowledge / Logos / information language. |
| `L3_me_R_relationship` | Relationship / interaction / bond language. |
| `L3_me_Q_quantum_observer` | Quantum / observer / collapse language. |
| `L3_me_F_faith_coupling` | Faith / coupling / alignment language. |
| `L3_me_C_christ_coherence` | Christ / coherence / integration language. |

### Workbook Variables

All L3 variables should remain in Excel:

- `L3_chi_score`
- `L3_chi_status`
- `L3_wisdom_score`
- `L3_knowledge_score`
- `L3_wk_ratio`
- `L3_wk_status`
- `L3_fruits_composite`
- `L3_dominant_fruit`
- `L3_fruits_detail`
- `L3_me_avg_score`
- `L3_me_dominant_variable`
- `L3_cross_domain_bridges`
- `L3_scripture_refs`
- `L3_ckg_raw`
- `L3_ckg_tier`
- `L3_me_G_gravity_belonging`
- `L3_me_M_mass_meaning`
- `L3_me_E_entropy_engagement`
- `L3_me_S_spacetime_structure`
- `L3_me_T_time_eternity`
- `L3_me_K_knowledge_logos`
- `L3_me_R_relationship`
- `L3_me_Q_quantum_observer`
- `L3_me_F_faith_coupling`
- `L3_me_C_christ_coherence`

### GTQ Smoke Test Values

For `gtq-01-measurement-collapsed-reality.html`:

| Variable | Value |
|---|---|
| `L3_chi_score` | `10` |
| `L3_chi_status` | `HIGH` |
| `L3_wisdom_score` | `0.64` |
| `L3_knowledge_score` | `4.63` |
| `L3_wk_ratio` | `0.138` |
| `L3_wk_status` | `KNOWLEDGE-DOMINANT` |
| `L3_fruits_composite` | `1.14` |
| `L3_dominant_fruit` | `grace` |
| `L3_me_avg_score` | `2.97` |
| `L3_me_dominant_variable` | `Q_quantum_observer` |
| `L3_cross_domain_bridges` | `14` |
| `L3_scripture_refs` | `158` |
| `L3_ckg_raw` | `100` |
| `L3_ckg_tier` | `A - Publication Grade` |

Interpretation caution: this layer is term-frequency based. It is valuable for framework coverage, but it is not a truth claim by itself. Public copy should say "framework signal" or "coverage," not "proof."
