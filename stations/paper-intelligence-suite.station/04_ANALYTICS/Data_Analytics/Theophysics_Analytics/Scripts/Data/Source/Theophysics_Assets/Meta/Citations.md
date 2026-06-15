---
title: Citations
tags:
- plugin/transformer
uuid: 77d0b8eb-0f79-57ed-948e-d79b33a3cd41
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\Citations.md
uuid_generated_at: '2025-11-22T01:23:48.367712'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

This plugin adds Citation support to Quartz.

> [!note]
> For information on how to add, remove or configure plugins, see the [[configuration#Plugins|Configuration]] page.

This plugin accepts the following configuration options:

- `bibliographyFile`: the path to the bibliography file. Defaults to `./bibliography.bib`. This is relative to git source of your vault.
- `suppressBibliography`: whether to suppress the bibliography at the end of the document. Defaults to `false`.
- `linkCitations`: whether to link citations to the bibliography. Defaults to `false`.
- `csl`: the citation style to use. Defaults to `apa`. Reference [rehype-citation](https://rehype-citation.netlify.app/custom-csl) for more options.
- `prettyLink`: whether to use pretty links for citations. Defaults to `true`.

## API

- Category: Transformer
- Function name: `Plugin.Citations()`.
- Source: [`quartz/plugins/transformers/citations.ts`](https://github.com/jackyzha0/quartz/blob/v4/quartz/plugins/transformers/citations.ts).
