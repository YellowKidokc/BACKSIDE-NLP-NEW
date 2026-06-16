---
title: Latex
tags:
- plugin/transformer
uuid: 6d1ffe9b-b2d9-583e-9a0f-bc5ca46dbea6
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: [[Theophysics_Glossary#Logos|Logos]] zright\Meta\Latex.md
uuid_generated_at: '2025-11-22T01:23:48.894079'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

This plugin adds LaTeX support to Quartz. See [[features/Latex|Latex]] for more information.

> [!note]
> For information on how to add, remove or configure plugins, see the [[configuration#Plugins|Configuration]] page.

This plugin accepts the following configuration options:

- `renderEngine`: the engine to use to render LaTeX equations. Can be `"katex"` for [KaTeX](https://katex.org/), `"mathjax"` for [MathJax](https://www.mathjax.org/) [SVG rendering](https://docs.mathjax.org/en/latest/output/svg.html), or `"typst"` for [Typst](https://typst.app/) (a new way to compose LaTeX equation). Defaults to KaTeX.
- `customMacros`: custom macros for all LaTeX blocks. It takes the form of a key-value pair where the key is a new command name and the value is the expansion of the macro. For example: `{"\\R": "\\mathbb{R}"}`

## API

- Category: Transformer
- Function name: `Plugin.Latex()`.
- Source: [`quartz/plugins/transformers/latex.ts`](https://github.com/jackyzha0/quartz/blob/v4/quartz/plugins/transformers/latex.ts).
