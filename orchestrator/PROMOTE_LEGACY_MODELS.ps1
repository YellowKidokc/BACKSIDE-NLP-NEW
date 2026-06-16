# PROMOTE_LEGACY_MODELS.ps1
# Moves everything from legacy-model-layer up to _models root
# Run from PowerShell: powershell -ExecutionPolicy Bypass -File "X:\Backside\_models\PROMOTE_LEGACY_MODELS.ps1"

$legacy = "X:\Backside\_models\legacy-model-layer"
$target = "X:\Backside\_models"

Write-Host "=== PROMOTING LEGACY MODELS ===" -ForegroundColor Cyan

# Models to move
$modelDirs = @(
    "claim_extract",
    "contradiction_detect",
    "fact_verify",
    "math_verify",
    "NLI_Models",
    "paperqa2",
    "paper_review",
    "timeline_verify",
    "health_reports",
    "huggingface",
    "scripts",
    ".venv_science_nlp"
)

foreach ($dir in $modelDirs) {
    $src = Join-Path $legacy $dir
    $dst = Join-Path $target $dir
    if (Test-Path $src) {
        if (Test-Path $dst) {
            Write-Host "SKIP (already exists): $dir" -ForegroundColor Yellow
        } else {
            Move-Item -LiteralPath $src -Destination $dst
            Write-Host "MOVED: $dir" -ForegroundColor Green
        }
    } else {
        Write-Host "NOT FOUND: $dir" -ForegroundColor Red
    }
}

# Files to move
$files = @(
    "nlp_layer.py",
    "requirements.txt",
    "MODEL_REGISTRY.md",
    "MODEL_STATION_REGISTRY_CLEAN.md",
    "MODEL_DOWNLOAD_STATUS_20260511.md",
    "PAPER_RUBRIC_SCHEMA.md",
    "DOWNLOAD_NEW_MODELS.bat",
    "HEALTHCHECK_ALL_MODELS.bat",
    "RUN_NLP_HEALTHCHECK.bat",
    "NLP_HEALTHCHECK_README.md",
    "INSTALL_DAILY_NLP_HEALTHCHECK.bat",
    "INSTALL_LLM_WIKI.bat"
)

foreach ($f in $files) {
    $src = Join-Path $legacy $f
    $dst = Join-Path $target $f
    if (Test-Path $src) {
        if (Test-Path $dst) {
            Write-Host "SKIP (already exists): $f" -ForegroundColor Yellow
        } else {
            Move-Item -LiteralPath $src -Destination $dst
            Write-Host "MOVED: $f" -ForegroundColor Green
        }
    } else {
        Write-Host "NOT FOUND: $f" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== CLEANUP ===" -ForegroundColor Cyan

# Check if legacy is now empty (minus junk)
$remaining = Get-ChildItem -LiteralPath $legacy -Force | Where-Object { $_.Name -notin @("desktop.ini", "__pycache__") }
if ($remaining.Count -eq 0) {
    Remove-Item -LiteralPath $legacy -Recurse -Force
    Write-Host "DELETED empty legacy-model-layer" -ForegroundColor Green
} else {
    Write-Host "legacy-model-layer still has items:" -ForegroundColor Yellow
    $remaining | ForEach-Object { Write-Host "  - $($_.Name)" }
}

# Check if root X:\models\ still exists
if (Test-Path "X:\models") {
    Write-Host ""
    Write-Host "X:\models\ still exists at root. Delete it? (it's redundant)" -ForegroundColor Yellow
    Write-Host "Run: Remove-Item -LiteralPath 'X:\models' -Recurse -Force" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== DONE ===" -ForegroundColor Cyan
