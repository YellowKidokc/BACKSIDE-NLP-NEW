## Consolidate v2 - fix encoding (read/write UTF-8 no BOM) and Codex L6 splice.
$ErrorActionPreference = "Stop"

$base = "X:\knowledge-refinery\01_INTAKE\cannon_math_proof_vectorize_20260518"
$out  = Join-Path $base "question_chain"
$codexFile = Join-Path $base "LAYER6_MATHEMATICAL_LEAN_SKELETON_CODEX_Q02_Q25.md"

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Read-Utf8 { param([string]$p)
    return [System.IO.File]::ReadAllText($p, [System.Text.Encoding]::UTF8)
}
function Write-Utf8 { param([string]$p, [string]$content)
    [System.IO.File]::WriteAllText($p, $content, $utf8NoBom)
}

$questions = @(
    @{n="Q00"; slug="truth_before_error";       title="Was The World Made Out Of A Lie?"},
    @{n="Q01"; slug="evil_is_parasitic";        title="Is Evil Equal To Good?"},
    @{n="Q02"; slug="ontological_rightness";    title="Is Righteousness Just an Opinion?"},
    @{n="Q03"; slug="error_correction";         title="Is the Universe Just Random Chaos?"},
    @{n="Q04"; slug="resurrection_uniqueness";  title="Is Jesus's Claim Structurally Unique?"},
    @{n="Q05"; slug="death_defeat";             title="Did God Defeat Death or Just Avoid It?"},
    @{n="Q06"; slug="board_of_directors";       title="Should the Strongest Rule?"},
    @{n="Q07"; slug="design_god";               title="Why Does Everyone Design God the Same Way?"},
    @{n="Q08"; slug="why_create";               title="Why Did God Create at All?"},
    @{n="Q09"; slug="worship_robots";           title="Why Not Just Make Worship-Robots?"},
    @{n="Q10"; slug="paradise_test";            title="Could a Good Person Pass the Paradise Test?"},
    @{n="Q11"; slug="who_gets_in";              title="Which Good People Get In?"},
    @{n="Q12"; slug="pure_mercy";               title="Why Not Just Forgive Everyone?"},
    @{n="Q13"; slug="pure_justice";             title="Why Not Just Pure Justice?"},
    @{n="Q14"; slug="resume_vs_posture";        title="Is Earning It the Disqualification?"},
    @{n="Q15"; slug="righteousness_sees";       title="Does a White Lie Really Matter?"},
    @{n="Q16"; slug="why_blood";                title="Why Blood? Why a Cost At All?"},
    @{n="Q17"; slug="temporary_covering";       title="Why Did Sacrifice Have to Repeat?"},
    @{n="Q18"; slug="parent_calls";             title="Trust Precedes Comprehension"},
    @{n="Q19"; slug="honest_obedience";         title="Honest Obedience"},
    @{n="Q20"; slug="ot_triage";                title="Is the Old Testament God Cruel?"},
    @{n="Q21"; slug="same_god";                 title="Did God Change Between the Testaments?"},
    @{n="Q22"; slug="why_not_teacher";          title="Why Couldn't God Just Teach Us to Be Good?"},
    @{n="Q23"; slug="why_death";                title="Why Did Jesus Have to Die?"},
    @{n="Q24"; slug="why_rise";                 title="Why Did Jesus Have to Rise?"},
    @{n="Q25"; slug="final_trust";              title="The Final Fork: Is Faith Rational?"}
)

# Parse Codex's L6 file into a hashtable
$codexText = Read-Utf8 $codexFile
$codexBlocks = @{}
# Match: "## Q03 - Anything\n<body>" until next "## Q.." or "## Summary"
$rxOpts = [Text.RegularExpressions.RegexOptions]::Singleline
$pattern = '##\s+(Q\d{2})\s*-\s*[^\r\n]+\r?\n(.*?)(?=##\s+Q\d{2}\s*-|##\s+Summary|\z)'
$rxMatches = [regex]::Matches($codexText, $pattern, $rxOpts)
foreach ($m in $rxMatches) {
    $qkey = $m.Groups[1].Value
    $body = $m.Groups[2].Value.TrimEnd("`r","`n"," ","-","`t")
    $codexBlocks[$qkey] = $body
}
Write-Host ("Parsed Codex blocks for: " + ($codexBlocks.Keys | Sort-Object) -join ', ')

# Process each question
$report = @()
foreach ($q in $questions) {
    $qn = $q.n
    $slug = $q.slug
    $srcFile = Join-Path $base "${qn}_${slug}.md"
    $qFolder = Join-Path $out  "${qn}_${slug}"
    $paper   = Join-Path $qFolder "${qn}_PAPER.md"

    if (-not (Test-Path $srcFile)) {
        $report += "MISSING: $qn"
        continue
    }

    New-Item -ItemType Directory -Path $qFolder -Force | Out-Null
    $content = Read-Utf8 $srcFile

    # Splice L6 if Codex has it AND original has a PENDING-style block
    $spliced = $false
    if ($codexBlocks.ContainsKey($qn)) {
        $codexBlock = $codexBlocks[$qn]
        # Capture from "## Layer 6" heading line through to next "## Layer" or "---" separator
        $l6Pattern = '(##\s+Layer\s*6[^\r\n]*\r?\n)(.*?)(?=##\s+Layer\s*7|\n---)'
        $rx = [regex]::new($l6Pattern, $rxOpts)
        $m2 = $rx.Match($content)
        if ($m2.Success) {
            $existingBody = $m2.Groups[2].Value
            if ($existingBody -match '(?i)\[PENDING:\s*Codex\]|placeholder|Likely targets') {
                $codexSection = "`n**Source:** Codex (forge) pass -- see ``LAYER6_MATHEMATICAL_LEAN_SKELETON_CODEX_Q02_Q25.md`` for full kernel mapping.`n`n" + $codexBlock + "`n`n"
                $content = $rx.Replace($content, '$1' + [Regex]::Escape($codexSection).Replace('\','\\'), 1)
                # The escape approach above is wrong for replacement. Do it manually:
                $content = Read-Utf8 $srcFile  # reset
                $m3 = $rx.Match($content)
                $before = $content.Substring(0, $m3.Index) + $m3.Groups[1].Value
                $after  = $content.Substring($m3.Index + $m3.Length)
                $content = $before + $codexSection + $after
                $spliced = $true
            }
        }
    }

    $statusHeader = @"
<!--
PAPER STATUS: consolidated draft for review.
Layer ownership (per broadcast 980):
  L1 hook         = David
  L2 human story  = Jim/Gemini
  L3 metaphysics  = Opus
  L4 theology     = Kimi
  L5 physics      = Opus
  L6 math / Lean  = Codex
  L7 objections   = GPT

Layer-owners: open this file. If you can improve YOUR layer, do it. Replace, don't append. Mark with a single-line edit note at the top of your section: "Polished by <name> on <date>".
-->


"@
    $final = $statusHeader + $content
    Write-Utf8 $paper $final
    $tag = if ($spliced) { "L6-spliced" } else { "as-is" }
    $report += ("{0,-3} {1}" -f $qn, $tag)
}

# Index
$indexLines = @()
$indexLines += "# Question Chain -- Consolidated Papers"
$indexLines += "## 'I Bet I Can Get You to God in First Principles'"
$indexLines += "### Generated $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
$indexLines += ""
$indexLines += "Each question lives in its own folder with a single consolidated paper."
$indexLines += "Layer-owners: open your paper, scan your layer, polish if you can improve it."
$indexLines += ""
$indexLines += "## Papers"
$indexLines += ""
foreach ($q in $questions) {
    $relPath = "$($q.n)_$($q.slug)/$($q.n)_PAPER.md"
    $indexLines += "- [$($q.n) -- $($q.title)]($relPath)"
}
$indexLines += ""
$indexLines += "## Layer ownership"
$indexLines += ""
$indexLines += "| Layer | Owner | Notes |"
$indexLines += "|---|---|---|"
$indexLines += "| L1 -- Self-defeating hook | David | His voice |"
$indexLines += "| L2 -- Human story | Jim/Gemini | Marriage frame primary |"
$indexLines += "| L3 -- Metaphysical structure | Opus | T1 closure spine |"
$indexLines += "| L4 -- Theological register | Kimi | Scripture alignment, no smuggling |"
$indexLines += "| L5 -- Physics / science isomorphism | Opus | SSB/Goldstone/Shannon/Second Law, FORMAL/BRIDGE labeled |"
$indexLines += "| L6 -- Math / Lean skeleton | Codex | T1 kernel mapping, FORMAL/BRIDGE/OPEN labeled |"
$indexLines += "| L7 -- Objections / kill conditions | GPT | Strongest rival per question |"

Write-Utf8 (Join-Path $out "INDEX.md") (($indexLines -join "`n"))

Write-Host "REPORT:"
$report | ForEach-Object { Write-Host "  $_" }
Write-Host "DONE."
