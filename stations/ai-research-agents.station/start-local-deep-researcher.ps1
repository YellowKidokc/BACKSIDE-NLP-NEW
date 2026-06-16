$ErrorActionPreference = "Stop"
$Root = "D:\AI-RESEARCH-AGENTS\local-deep-researcher"
$LangGraph = Join-Path $Root ".venv\Scripts\langgraph.exe"

if (-not (Test-Path $LangGraph)) {
    throw "Missing LangGraph executable at $LangGraph"
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

# Cheap default: DuckDuckGo search and local Ollama model. You can switch
# SEARCH_API to tavily after TAVILY_API_KEY is set.
if (-not $env:SEARCH_API) { $env:SEARCH_API = "duckduckgo" }
if (-not $env:LLM_PROVIDER) { $env:LLM_PROVIDER = "ollama" }
if (-not $env:OLLAMA_BASE_URL) { $env:OLLAMA_BASE_URL = "http://localhost:11434" }
if (-not $env:LOCAL_LLM) { $env:LOCAL_LLM = "llama3.1:8b" }

Set-Location $Root
& $LangGraph dev

