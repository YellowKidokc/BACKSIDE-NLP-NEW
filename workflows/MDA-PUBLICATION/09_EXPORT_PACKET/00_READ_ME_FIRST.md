# MDA Publication Export Packet

This folder is the handoff packet. If someone lands here cold, start here and do not guess.

## Current Truth

- The 61 Standard articles are present and are the source spine.
- The combined four-tab HTML shell exists for all 61 articles.
- Easy and Academic tabs are structurally wired, but only the articles that already have generated reading-level markdown are real. The rest fall back to Standard text.
- The Proof tab is structurally wired and includes metrics plus the two-lane report. It is not the same as a completed proof gate.
- The Axiom black snapshot view exists and is useful for inspection.
- The keyword graph overlay exists and explains paper-to-paper bridge terms.
- Claim promotion is still the weak link. Do not say "all proof tabs are complete" unless promoted claims have actually passed the gate.

## Folder Map

1. `01_LOSSLESS_SOURCE/articles`  
   The canonical Standard-voice Markdown spine. Treat these as source, not scratch.

2. `02_READING_LEVELS`  
   Generated Easy/Academic markdown where available. This is partial until every article has `_EASY.md`, `_ACADEMIC.md`, and `_TERM_INVENTORY.json`.

3. `03_READER_HTML`  
   Combined four-tab HTML pages: Easy / Standard / Academic / Proof. Open `index.html`.

4. `04_AXIOM_BLACK_SNAPSHOTS`  
   Human-readable black-panel snapshot view for every paper, plus individual pages.

5. `05_KEYWORD_GRAPH_OVERLAY`  
   Clean keyword and bridge-term overlay on the graph.

6. `06_PIPELINE_ANALYTICS`  
   Excel, JSON rows, graph JSON/GraphML, and raw per-paper snapshots.

7. `07_TWO_LANE_OPENAI_REPORTS`  
   Math + attention reports for all 61 papers.

8. `08_SCRIPTS_AND_RUNBOOKS`  
   Scripts needed to regenerate reading levels and rebuild HTML.

9. `09_PROMPTS_FOR_COLLABORATORS`  
   Copy-paste prompts for another AI collaborator or human editor.

## Next Commands

Generate all missing Easy/Academic files:

```powershell
powershell -ExecutionPolicy Bypass -File X:\WORKFLOWS\MDA-PUBLICATION\READING_LEVEL_GENERATOR\run_all_reading_levels.ps1 -UseMini
```

Rebuild the four-tab HTML after reading levels finish:

```powershell
python X:\WORKFLOWS\MDA-PUBLICATION\05_HTML_BUILD\combine_mda_reader_html.py
```

Then refresh this packet:

```powershell
Copy-Item -Path X:\WORKFLOWS\MDA-PUBLICATION\06_HTML_BUILD\reader_combined\* -Destination X:\WORKFLOWS\MDA-PUBLICATION\09_EXPORT_PACKET\03_READER_HTML -Recurse -Force
Copy-Item -Path X:\WORKFLOWS\MDA-PUBLICATION\05_READING_LEVELS\* -Destination X:\WORKFLOWS\MDA-PUBLICATION\09_EXPORT_PACKET\02_READING_LEVELS -Recurse -Force
```

## Hard Rule

Do not edit the source spine casually. If an edit is needed, put it in the edit queue or make a clear patch with provenance. This packet is for finishing the production surfaces, not inventing a new series.
