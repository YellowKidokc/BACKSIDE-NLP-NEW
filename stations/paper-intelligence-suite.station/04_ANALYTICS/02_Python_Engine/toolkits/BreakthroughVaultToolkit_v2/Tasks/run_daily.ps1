$python = "python"
$toolkit = Join-Path $PSScriptRoot "..\Scripts"
$vault = "C:\Path\To\Your\Vault"
$db = Join-Path $PSScriptRoot "..\Data\coherence.db"

& $python "$toolkit\grace_vault_manager.py" --cli --vault "$vault" --auto --db "$db"
