# backup_models.ps1 — weekly mirror of the local model cache to the NAS archive tier.
# Runtime copy lives at D:\nlp_models (fast, local). This keeps a recoverable mirror
# at \\192.168.2.50\brain\13_ARCHIVE so a D: failure never costs more than a re-copy.
# Note: the master models also live on the NAS at 05_MODELS; this is an extra archive tier.
$src = 'D:\nlp_models'
$dst = '\\192.168.2.50\brain\13_ARCHIVE\nlp_models'
$log = 'D:\nlp_models\_backup.log'

New-Item -ItemType Directory -Force -Path $dst | Out-Null
# /MIR keeps the archive in sync with the cache; _* scratch files/dirs are excluded.
robocopy $src $dst /MIR /XF "_*" /XD "_*" /MT:16 /R:1 /W:1 /NP /NDL /LOG:$log
"Backup finished $(Get-Date -Format s); robocopy rc=$LASTEXITCODE" | Add-Content $log
