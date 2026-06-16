## Consolidate the 26 Q-files into per-question folders with L6 spliced from Codex master.
$ErrorActionPreference = "Stop"

$base = "X:\knowledge-refinery\01_INTAKE\cannon_math_proof_vectorize_20260518"
$out  = Join-Path $base "question_chain"
$codexFile = Join-Path $base "LAYER6_MATHEMATICAL_LEAN_SKELETON_CODEX_Q02_Q25.md"

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
    @{n="Q22"; slug="why_not_teacher";          title="Why Couldnt God Just Teach Us to Be Good?"},
    @{n="Q23"; slug="why_death";                title="Why Did Jesus Have to Die?"},
    @{n="Q24"; slug="why_rise";                 title="Why Did Jesus Have to Rise?"},
    @{n="Q25"; slug="final_trust";              title="The Final Fork: Is Faith Rational?"}
)

# Parse Codex's L6 file into a hashtable: Qnn -> block text
$codexText = Get-Content $codexFile -Raw
$codexBlocks = @{}
$pattern = '## (Q\d{2}) - [^\r\n]+\r?\n(.*?)(?=(?:## Q\d{2} -)|(?:^## Summary)|\Z)'
$rxMatches = [regex]::Matches($codexText, $pattern, [Text.RegularExpressions.RegexOptions]::Singleline -bor [Text.RegularExpressions.RegexOptions]::Multiline)
foreach ($m in $rxMatches) {
    $qkey = $m.Groups[1].Value
    $body = $m.Groups[2].Value.TrimEnd("`r","`n"," ","-")
    $codexBlocks[$qkey] = $body
}

Write-Host "Parsed Codex blocks for: $($codexBlocks.Keys -join ', ')"

# Now process each question
foreach ($q in $questions) {
    $qn = $q.n
    $slug = $q.slug
    $title = $q.title
    $srcFile = Join-Path $base "${qn}_${slug}.md"
    $qFolder = Join-Path $out  "${qn}_${slug}"
    $paper   = Join-Path $qFolder "${qn}_PAPER.md"

    if (-not (Test-Path $srcFile)) {
        Write-Host "MISSING source file: $srcFile -- skipping"
        continue
    }

    New-Item -ItemType Directory -Path $qFolder -Force | Out-Null

    $content = Get-Content $srcFile -Raw

    # Inject Codex's L6 if a PENDING marker exists for that question.
    if ($codexBlocks.ContainsKey($qn)) {
        $codexBlock = $codexBlocks[$qn]
        $l6Pattern = '(## Layer 6[^\r\n]*\r?\n)(.*?)(\r?\n---)'
        if ($content -match $l6Pattern) {
            $existingBody = $Matches[2]
            if ($existingBody -match '\[PENDING:\s*Codex\]|placeholder|Likely targets') {
                $codexSection = "`n**Source:** Codex (forge) pass -- see ``LAYER6_MATHEMATICAL_LEAN_SKELETON_CODEX_Q02_Q25.md`` for full kernel mapping.`n`n" + $codexBlock + "`n"
                $newContent = [regex]::Replace($content, $l6Pattern, {
                    param($m)
                    return $m.Groups[1].Value + $codexSection + $m.Groups[3].Value
                }, [Text.RegularExpressions.RegexOptions]::Singleline)
                $content = $newContent
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

Layer-owners: open this file. If you can improve YOUR layer, do it. Replace, dont append. Mark with a single-line edit note at the top of your section: 'Polished by <name> on <date>'.
-->


"@
    $final = $statusHeader + $content
    Set-Content -Path $paper -Value $final -Encoding UTF8
    Write-Host "Wrote $paper"
}

# Build a master index
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
    $qn = $q.n
    $slug = $q.slug
    $title = $q.title
    $relPath = "${qn}_${slug}/${qn}_PAPER.md"
    $indexLines += "- [$qn -- $title]($relPath)"
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
Set-Content -Path (Join-Path $out "INDEX.md") -Value ($indexLines -join "`n") -Encoding UTF8
Write-Host "Wrote INDEX.md"
Write-Host "DONE."
