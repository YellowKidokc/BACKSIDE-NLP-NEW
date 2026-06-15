# LEXICON

Drop your enhanced Fruits lexicon workbook here, e.g.
`paper_grader_lexicons_master_enhanced.xlsx`.

`RUN_FRUITS_ENGINE.bat` auto-discovers the lexicon: it picks the **newest**
`.xlsx` in this folder, preferring filenames containing `lexicon`. No code edit
needed when you drop a new version — the newest one wins automatically.

Override with: `RUN_FRUITS_ENGINE.bat --lexicon "X:\path\to\some_lexicon.xlsx"`

Recognized sheets (others are ignored): `FRUITS_LEX` / `FRUITS` (key,value),
`ANTI_FRUITS` (key,value), and `Fruit Semantic Architecture`. If no workbook is
present, the engine runs on its built-in lexicon.
