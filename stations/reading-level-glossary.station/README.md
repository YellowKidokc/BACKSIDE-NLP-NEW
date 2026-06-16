# reading-level-glossary.station

## Purpose

Scan article text for a target reading grade and create glossary support for
terms that are likely above that audience level.

Default target: **8th grade**.

This station does not rewrite article content. It produces reports that a
reading-level generator, editor, or HTML glossary injector can consume later.

## Input

Drop files here:

```text
X:\Backside\stations\reading-level-glossary.station\DROP_HERE
```

Supported file types:

```text
.txt
.md
.html
.htm
```

## Run

```powershell
X:\Backside\stations\reading-level-glossary.station\RUN.bat
```

Single-file override:

```powershell
X:\Backside\stations\reading-level-glossary.station\RUN.bat --file path\to\article.md
```

Target override:

```powershell
X:\Backside\stations\reading-level-glossary.station\RUN.bat --target-grade 6
```

## Output

Each run writes a timestamped folder under:

```text
X:\Backside\stations\reading-level-glossary.station\EXPORTS
```

Per file:

- `{file}.readability_glossary.md`
- `{file}.readability_glossary.json`
- `{file}.glossary.csv`

Run-level:

- `run_index.md`
- `run_index.json`

## Verdicts

- `PASS`: estimated document grade is at or under target.
- `REVIEW`: estimated document grade is above target.
- `TOO_SHORT`: not enough words for a stable reading estimate.

## Notes

This is the scanner/glossary feeder. The older
`readability-rewriter.station` remains the future rewrite/decompression lane.

The glossary definition column is conservative:

- known Theophysics and publication terms get a draft definition.
- unknown words are marked as needing one plain-context definition.

