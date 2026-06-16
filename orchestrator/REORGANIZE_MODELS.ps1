# REORGANIZE_MODELS.ps1
# Consolidates all model folders into X:\Backside\_models\
# Run from PowerShell as: .\REORGANIZE_MODELS.ps1

$target = "X:\Backside\_models"
$rootModels = "X:\models"
$legacy = "$target\legacy-model-layer"
$downloaded = "$target\downloaded"

Write-Host "=== THEOPHYSICS MODEL CONSOLIDATION ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Move legacy-model-layer contents up to _models root
Write-Host "STEP 1: Promoting legacy-model-layer contents to _models root..." -ForegroundColor Yellow
