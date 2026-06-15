---
title: GitHubFlavoredMarkdown
tags:
- plugin/transformer
uuid: 8962394c-f2f9-57f2-881c-f936d2f30c3a
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\GitHubFlavoredMarkdown.md
uuid_generated_at: '2025-11-22T01:23:48.756888'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

This plugin enhances Markdown processing to support GitHub Flavored Markdown (GFM) which adds features like autolink literals, footnotes, strikethrough, tables and tasklists.

In addition, this plugin adds optional features for typographic refinement (such as converting straight quotes to curly quotes, dashes to en-dashes/em-dashes, and ellipses) and automatic heading links as a symbol that appears next to the heading on hover.

> [!note]
> For information on how to add, remove or configure plugins, see the [[configuration#Plugins|Configuration]] page.

This plugin accepts the following configuration options:

- `enableSmartyPants`: When true, enables typographic enhancements. Default is true.
- `linkHeadings`: When true, automatically adds links to headings. Default is true.

## API

- Category: Transformer
- Function name: `Plugin.GitHubFlavoredMarkdown()`.
- Source: [`quartz/plugins/transformers/gfm.ts`](https://github.com/jackyzha0/quartz/blob/v4/quartz/plugins/transformers/gfm.ts).
