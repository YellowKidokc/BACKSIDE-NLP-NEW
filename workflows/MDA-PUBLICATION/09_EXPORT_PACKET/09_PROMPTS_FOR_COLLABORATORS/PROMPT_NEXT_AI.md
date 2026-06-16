# Prompt For Next AI Collaborator

You are entering the MDA Publication Export Packet.

Your job is to finish production surfaces without corrupting the source spine.

Start by reading:

`X:\WORKFLOWS\MDA-PUBLICATION\09_EXPORT_PACKET\00_READ_ME_FIRST.md`

Rules:

1. Treat `01_LOSSLESS_SOURCE/articles` as source of truth.
2. Do not claim Easy/Academic is complete until every article has generated reading-level markdown.
3. Do not claim Proof is complete until claims are actually promoted through the gate.
4. Use the two-lane reports as audit guidance, not as public prose.
5. Use the keyword overlay to explain graph connections, not as proof.

Immediate next task:

Run or continue the reading-level batch, then rebuild combined HTML.

Commands:

```powershell
powershell -ExecutionPolicy Bypass -File X:\WORKFLOWS\MDA-PUBLICATION\READING_LEVEL_GENERATOR\run_all_reading_levels.ps1 -UseMini
python X:\WORKFLOWS\MDA-PUBLICATION\05_HTML_BUILD\combine_mda_reader_html.py
```

After rebuilding, report:

- how many `_EASY.md` files exist
- how many `_ACADEMIC.md` files exist
- how many combined HTML pages show fallback
- which articles still need proof claim promotion
