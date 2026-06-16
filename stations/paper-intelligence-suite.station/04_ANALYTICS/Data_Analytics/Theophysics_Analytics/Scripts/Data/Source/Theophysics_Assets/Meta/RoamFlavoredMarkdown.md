---
title: RoamFlavoredMarkdown
tags:
- plugin/transformer
uuid: 99954160-b6b4-5cfb-bf17-95bb418a97bf
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: [[Theophysics_Glossary#Logos|Logos]] zright\Meta\RoamFlavoredMarkdown.md
uuid_generated_at: '2025-11-22T01:23:49.230720'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

This plugin provides support for [Roam Research](https://roamresearch.com) compatibility. See [[Roam Research compatibility]] for more information.

> [!note]
> For information on how to add, remove or configure plugins, see the [[configuration#Plugins|Configuration]] page.

This plugin accepts the following configuration options:

- `orComponent`: If `true` (default), converts Roam `{{ or:ONE|TWO|THREE }}` shortcodes into HTML Dropdown options.
- `TODOComponent`: If `true` (default), converts Roam `{{[[TODO]]}}` shortcodes into HTML check boxes.
- `DONEComponent`: If `true` (default), converts Roam `{{[[DONE]]}}` shortcodes into checked HTML check boxes.
- `videoComponent`: If `true` (default), converts Roam `{{[[video]]:URL}}` shortcodes into embeded HTML video.
- `audioComponent`: If `true` (default), converts Roam `{{[[audio]]:URL}}` shortcodes into embeded HTML audio.
- `pdfComponent`: If `true` (default), converts Roam `{{[[pdf]]:URL}}` shortcodes into embeded HTML PDF viewer.
- `blockquoteComponent`: If `true` (default), converts Roam `{{[[>]]}}` shortcodes into Quartz blockquotes.

## API

- Category: Transformer
- Function name: `Plugin.RoamFlavoredMarkdown()`.
- Source: [`quartz/plugins/transformers/roam.ts`](https://github.com/jackyzha0/quartz/blob/v4/quartz/plugins/transformers/roam.ts).
