$names = @(
    "TAVILY_API_KEY",
    "GOOGLE_API_KEY",
    "OPENAI_API_KEY",
    "OPENROUTER_API_KEY"
)

foreach ($name in $names) {
    $process = [bool][Environment]::GetEnvironmentVariable($name, "Process")
    $user = [bool][Environment]::GetEnvironmentVariable($name, "User")
    $machine = [bool][Environment]::GetEnvironmentVariable($name, "Machine")
    "{0}: process={1} user={2} machine={3}" -f $name, $process, $user, $machine
}

if (-not [Environment]::GetEnvironmentVariable("TAVILY_API_KEY", "User") -and
    -not [Environment]::GetEnvironmentVariable("TAVILY_API_KEY", "Process") -and
    -not [Environment]::GetEnvironmentVariable("TAVILY_API_KEY", "Machine")) {
    ""
    "Missing TAVILY_API_KEY. Set it with:"
    '[Environment]::SetEnvironmentVariable("TAVILY_API_KEY", "PASTE_TAVILY_KEY", "User")'
}

