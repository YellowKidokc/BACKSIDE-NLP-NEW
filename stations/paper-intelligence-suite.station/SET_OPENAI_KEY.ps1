# OPENAI API KEY SETUP
# Run this once. Sets OPENAI_API_KEY permanently in your user environment.

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " OPENAI API KEY — PERMANENT SETUP" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host " This sets OPENAI_API_KEY in your Windows" -ForegroundColor Gray
Write-Host " user environment variables permanently." -ForegroundColor Gray
Write-Host " You only need to do this once." -ForegroundColor Gray
Write-Host ""

$key = Read-Host "Paste your OpenAI API key (sk-...)" -AsSecureString
$plain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($key)
)

if ($plain.Length -lt 20 -or -not $plain.StartsWith("sk-")) {
    Write-Host "" 
    Write-Host " ERROR: That doesn't look like a valid key." -ForegroundColor Red
    Write-Host " Keys start with sk- and are 50+ characters." -ForegroundColor Red
    pause
    exit
}

[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", $plain, "User")

Write-Host ""
Write-Host " KEY SET." -ForegroundColor Green
Write-Host " Variable: OPENAI_API_KEY" -ForegroundColor Green
Write-Host " Scope:    User (permanent)" -ForegroundColor Green
Write-Host ""
Write-Host " Restart any open terminals/scripts for it to take effect." -ForegroundColor Yellow
Write-Host ""
pause
