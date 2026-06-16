@echo off
set PYTHON=python
set TOOLKIT=%~dp0..\Scripts
set VAULT=C:\Path\To\Your\Vault
set DB=%~dp0..\Data\coherence.db

%PYTHON% "%TOOLKIT%\grace_vault_manager.py" --cli --vault "%VAULT%" --auto --db "%DB%"
