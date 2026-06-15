$ErrorActionPreference = "Stop"
$Root = "D:\AI-RESEARCH-AGENTS\gpt-researcher"
$Python = Join-Path $Root ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    throw "Missing GPT Researcher venv at $Python"
}

if (-not $env:TAVILY_API_KEY) {
    $env:TAVILY_API_KEY = [Environment]::GetEnvironmentVariable("TAVILY_API_KEY", "User")
}
if (-not $env:OPENAI_API_KEY) {
    $env:OPENAI_API_KEY = [Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")
}
if (-not $env:GOOGLE_API_KEY) {
    $env:GOOGLE_API_KEY = [Environment]::GetEnvironmentVariable("GOOGLE_API_KEY", "User")
}

if (-not $env:TAVILY_API_KEY) {
    throw "TAVILY_API_KEY is not set. GPT Researcher defaults to Tavily search."
}

Set-Location $Root
& $Python -m uvicorn main:app --host 127.0.0.1 --port 8000

