# Component Audit Prompt

You are auditing a marked Theophysics public HTML page.

Use the PAGE_META block and component inventory as source of truth. Do not rewrite the article body unless asked.

Return:

1. PASS/FAIL for PAGE_META.
2. PASS/FAIL for matched BEGIN/END component pairs.
3. Missing recommended components.
4. Duplicate component names within the same file.
5. Components that look present visually but are not marked.
6. Whether this page is ready for batch injection.

Tone: operational, concise, exact file/component names.
