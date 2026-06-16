# 7Q In-House Pipeline

Canonical home:

```text
X:\knowledge-refinery\13_SOURCE_SYSTEMS\7Q
```

## 1-2-3-4-5 Route

```text
1. Source claim/article
   -> FAP lossless JSON + paper-proof-grader output

2. 7Q Method
   -> human/public explanation layer, examples, cards, evidence protocol

3. 7Q Engine
   -> Q0-Q7 scoring, reverse destruction pass, scored markdown, scored HTML

4. Treaties / proof-explorer handoff
   -> combines scorecard, axiom mapping, 7Q result, and math/falsification links

5. HTML report layer
   -> X:\knowledge-refinery\06_HTML_REPORTS\7Q
   -> \\dlowenas\brain\proof-explorer when promoted
```

## Folders

```text
engine\  executable 7Q scorer copied from \\dlowenas\theophysics\7q-engine
method\  specs, public HTML pages, presentations copied from \\dlowenas\theophysics\7Q Method
```

## Canary

Run:

```text
X:\knowledge-refinery\RUN_7Q_CANARY.bat
```

Expected output:

```text
X:\knowledge-refinery\06_HTML_REPORTS\7Q\<claim-id>_*.md
X:\knowledge-refinery\06_HTML_REPORTS\7Q\<claim-id>_*.html
```

## Boundary

The 7Q engine judges claims. It does not replace:

- paper-proof-grader
- axiom mapping
- Treaties/proof-explorer rendering
- Kimi production HTML promotion

Its job is to fill the Q0-Q7 part of the final HTML packet.
