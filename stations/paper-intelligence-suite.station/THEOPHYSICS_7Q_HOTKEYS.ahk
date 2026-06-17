#Requires AutoHotkey v2.0+
; ============================================================
; THEOPHYSICS 7Q HOTKEY
; Ctrl+Alt+7  = Run 7Q analysis on selected paper path OR prompt for path
; Ctrl+Alt+8  = Run FULL pipeline (no OpenAI) on selected folder
; Ctrl+Alt+9  = Run FULL pipeline WITH OpenAI on selected folder
; ============================================================
; Drop this file in your AHK startup folder or #Include from hub_core.ahk
; ============================================================

PYTHON_EXE := "python"
SUITE_DIR  := "C:\Users\lowes\Desktop\THEOPHYSICS_PAPER_INTELLIGENCE"
RUNNER     := SUITE_DIR . "\00_ORCHESTRATOR\run_pipeline.py"
SEVEN_Q    := SUITE_DIR . "\04_OPENAI_7Q\seven_q_runner.py"

; ============================================================
; Ctrl+Alt+7 — 7Q on a single paper
; Select a file path first, or it will prompt you
; ============================================================
^!7:: {
    selected := ""
    savedClip := ClipboardAll()
    A_Clipboard := ""
    Send "^c"
    ClipWait 0.5
    selected := Trim(A_Clipboard)
    A_Clipboard := savedClip

    if (!selected or !FileExist(selected)) {
        selected := InputBox("Enter full path to paper .md file:", "7Q Analysis", "w600 h80").Value
        if (!selected)
            return
    }

    if (!FileExist(selected)) {
        MsgBox "File not found:`n" . selected, "7Q Error", "Icon!"
        return
    }

    ; Check API key
    apiKey := EnvGet("OPENAI_API_KEY")
    if (!apiKey or StrLen(apiKey) < 20) {
        result := MsgBox("OPENAI_API_KEY not set.`n`nRun SET_OPENAI_KEY.ps1 first.`n`nOpen setup script now?",
                         "API Key Missing", "YesNo Icon!")
        if (result = "Yes")
            Run "powershell -ExecutionPolicy Bypass -File `"" . "C:\Users\lowes\Desktop\THEOPHYSICS_PAPER_INTELLIGENCE\SET_OPENAI_KEY.ps1`""
        return
    }

    paperName := RegExReplace(selected, ".*\\", "")
    Toast("Running 7Q on: " . paperName)

    cmd := PYTHON_EXE . " `"" . SEVEN_Q . "`" --paper `"" . selected . "`""
    Run "powershell -WindowStyle Normal -Command `"" . cmd . "`""
}

; ============================================================
; Ctrl+Alt+8 — Full pipeline (no OpenAI) on a folder
; ============================================================
^!8:: {
    selected := ""
    savedClip := ClipboardAll()
    A_Clipboard := ""
    Send "^c"
    ClipWait 0.5
    selected := Trim(A_Clipboard)
    A_Clipboard := savedClip

    if (!selected or !DirExist(selected)) {
        selected := InputBox("Enter full path to series folder:", "Full Pipeline (No OpenAI)", "w600 h80").Value
        if (!selected)
            return
    }

    if (!DirExist(selected)) {
        MsgBox "Folder not found:`n" . selected, "Pipeline Error", "Icon!"
        return
    }

    Toast("Running pipeline on: " . selected)
    cmd := PYTHON_EXE . " `"" . RUNNER . "`" --series `"" . selected . "`""
    Run "powershell -WindowStyle Normal -Command `"" . cmd . "`""
}

; ============================================================
; Ctrl+Alt+9 — Full pipeline WITH OpenAI on a folder
; ============================================================
^!9:: {
    selected := ""
    savedClip := ClipboardAll()
    A_Clipboard := ""
    Send "^c"
    ClipWait 0.5
    selected := Trim(A_Clipboard)
    A_Clipboard := savedClip

    if (!selected or !DirExist(selected)) {
        selected := InputBox("Enter full path to series folder:", "Full Pipeline + OpenAI 7Q", "w600 h80").Value
        if (!selected)
            return
    }

    apiKey := EnvGet("OPENAI_API_KEY")
    if (!apiKey or StrLen(apiKey) < 20) {
        MsgBox "OPENAI_API_KEY not set. Run SET_OPENAI_KEY.ps1 first.", "API Key Missing", "Icon!"
        return
    }

    confirm := MsgBox("Run FULL pipeline + OpenAI 7Q on:`n" . selected . "`n`nCost: ~$0.03 per paper.",
                      "Confirm OpenAI Run", "YesNo")
    if (confirm != "Yes")
        return

    Toast("Running FULL pipeline + 7Q...")
    cmd := PYTHON_EXE . " `"" . RUNNER . "`" --series `"" . selected . "`" --openai"
    Run "powershell -WindowStyle Normal -Command `"" . cmd . "`""
}

; ============================================================
; Quick toast notification (no dependency on hub_core)
; ============================================================
Toast(msg, duration := 2000) {
    static toastGui := ""
    if IsObject(toastGui)
        toastGui.Destroy()
    toastGui := Gui("+AlwaysOnTop -Caption +ToolWindow")
    toastGui.BackColor := "0f0f0f"
    toastGui.SetFont("s10 cDDDDDD", "Segoe UI")
    toastGui.Add("Text", "xm ym", "  7Q  |  " . msg . "  ")
    toastGui.Show("NoActivate x10 y10")
    SetTimer(() => toastGui.Destroy(), -duration)
}
