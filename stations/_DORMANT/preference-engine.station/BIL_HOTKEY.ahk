; BIL Quick Feedback Hotkey
; Ctrl+Shift+F = Pop up feedback window
; Put this in shell:startup alongside START_BIL.bat

#Requires AutoHotkey v2.0

^+f:: {
    feedbackPath := "X:\Backside\stations\preference-engine.station\feedback.html"
    Run feedbackPath
}
