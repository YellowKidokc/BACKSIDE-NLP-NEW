param([switch]$WhatIf)

$ErrorActionPreference = "Stop"
$ts = Get-Date -Format "yyyyMMdd_HHmmss"

# Update these two source paths when routing a new MDA batch.
$SourceMathGrader = "X:\apps\paper-intelligence-suite-python\OUTPUT\mda_math_translation_full61_20260530_053137"
$SourceNLP = "X:\apps\paper-intelligence-suite-python\OUTPUT\mda_full_local_nlp_after_mtl_20260530_053539"

# Permanent homes.
$BacksideMDA = "X:\Backside\MDA"
$CanonMDA = "Z:\_ __THEOPHYSICS_CANON\03_SERIES\MDA"

function Write-Step($Message, $Color = "Gray") {
    Write-Host $Message -ForegroundColor $Color
}

function Ensure-Directory($Path) {
    if (Test-Path -LiteralPath $Path) { return }
    if ($WhatIf) {
        Write-Step "  WOULD ENSURE DIR: $Path" "Yellow"
    } else {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Route-Files($Source, $Destination, $Filter) {
    if (-not (Test-Path -LiteralPath $Source)) {
        Write-Warning "SKIP missing source: $Source"
        return
    }

    if ($WhatIf) {
        $count = (Get-ChildItem -LiteralPath $Source -Filter $Filter -File -ErrorAction SilentlyContinue).Count
        Write-Step "  WOULD: $Filter from $(Split-Path $Source -Leaf) -> $(Split-Path $Destination -Leaf) ($count files)" "Yellow"
    } else {
        Copy-Item -Path (Join-Path $Source $Filter) -Destination $Destination -Force -ErrorAction SilentlyContinue
        $count = (Get-ChildItem -LiteralPath $Destination -Filter $Filter -File -ErrorAction SilentlyContinue).Count
        Write-Step "  OK: $(Split-Path $Destination -Leaf) ($count files)" "Green"
    }
}

function Route-Tree($Source, $Destination, $Label) {
    if (-not (Test-Path -LiteralPath $Source)) {
        Write-Warning "SKIP missing source: $Source"
        return
    }

    if ($WhatIf) {
        $count = (Get-ChildItem -LiteralPath $Source -Recurse -File -ErrorAction SilentlyContinue).Count
        Write-Step "  WOULD: $Label -> $(Split-Path $Destination -Leaf) ($count files)" "Yellow"
    } else {
        Copy-Item -Path (Join-Path $Source "*") -Destination $Destination -Recurse -Force -ErrorAction SilentlyContinue
        Write-Step "  OK: $Label" "Green"
    }
}

foreach ($source in @($SourceMathGrader, $SourceNLP)) {
    if (-not (Test-Path -LiteralPath $source)) {
        if ($WhatIf) {
            Write-Warning "Source not found during dry run: $source"
        } else {
            Write-Error "Source not found: $source"
            exit 1
        }
    }
}

$directories = @(
    "$BacksideMDA\01_OUTBOX_REPORTS",
    "$BacksideMDA\02_HTML_OUTPUTS",
    "$BacksideMDA\03_FINAL_READY",
    "$BacksideMDA\04_ARCHIVE_ORIGINALS",
    "$BacksideMDA\05_MANIFESTS",
    "$BacksideMDA\06_RIGOR_GATES",
    "$BacksideMDA\07_NLP_SCORECARDS",
    "$BacksideMDA\08_NLP_WORKBOOKS",
    "$BacksideMDA\09_NLP_SNAPSHOTS",
    "$BacksideMDA\_RUNS",
    "$BacksideMDA\_LOGS",
    "$CanonMDA\articles",
    "$CanonMDA\grades",
    "$CanonMDA\nlp",
    "$CanonMDA\claim-audits"
)

foreach ($directory in $directories) {
    Ensure-Directory $directory
}

Write-Step ""
Write-Step "=== MDA OUTPUT ROUTER - $ts ===" "Cyan"
if ($WhatIf) { Write-Step "  DRY RUN" "Yellow" }

# Math/grader outputs to Backside.
Route-Files "$SourceMathGrader\01_OUTBOX_REPORTS" "$BacksideMDA\01_OUTBOX_REPORTS" "*.*"
Route-Files "$SourceMathGrader\02_HTML_OUTPUTS" "$BacksideMDA\02_HTML_OUTPUTS" "*.*"
Route-Files "$SourceMathGrader\03_FINAL_READY" "$BacksideMDA\03_FINAL_READY" "*.*"
Route-Files "$SourceMathGrader\04_ARCHIVE_ORIGINALS" "$BacksideMDA\04_ARCHIVE_ORIGINALS" "*.*"
Route-Files "$SourceMathGrader\05_MANIFESTS" "$BacksideMDA\05_MANIFESTS" "*.*"
Route-Tree "$SourceMathGrader\06_RIGOR_GATES" "$BacksideMDA\06_RIGOR_GATES" "06_RIGOR_GATES"

# NLP outputs to Backside.
Route-Files "$SourceNLP\html_reports" "$BacksideMDA\07_NLP_SCORECARDS" "*.*"
Route-Files "$SourceNLP\grader" "$BacksideMDA\08_NLP_WORKBOOKS" "*.xlsx"
Route-Files "$SourceNLP\grader" "$BacksideMDA\08_NLP_WORKBOOKS" "*.json"
Route-Tree "$SourceNLP\grader\snapshots" "$BacksideMDA\09_NLP_SNAPSHOTS" "09_NLP_SNAPSHOTS"

# Canon vault routing.
Route-Files "$SourceMathGrader\04_ARCHIVE_ORIGINALS" "$CanonMDA\articles" "*.md"
Route-Files "$SourceMathGrader\03_FINAL_READY" "$CanonMDA\grades" "*.paper-grade.md"
Route-Files "$SourceNLP\html_reports" "$CanonMDA\nlp" "*.html"
Route-Files "$SourceMathGrader\03_FINAL_READY" "$CanonMDA\claim-audits" "*.claim-audit.csv"

if (-not $WhatIf) {
    $receipt = "Route receipt: $ts`nMath: $SourceMathGrader`nNLP: $SourceNLP"
    $receipt | Out-File "$BacksideMDA\_RUNS\route_receipt_$ts.md" -Encoding utf8
}

Write-Step ""
Write-Step "=== DONE ===" "Cyan"
Write-Step "  Backside: $BacksideMDA" "DarkGray"
Write-Step "  Canon:    $CanonMDA" "DarkGray"
