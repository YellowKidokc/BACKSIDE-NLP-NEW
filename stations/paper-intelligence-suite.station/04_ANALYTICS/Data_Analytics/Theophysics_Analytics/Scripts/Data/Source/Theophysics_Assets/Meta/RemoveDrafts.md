---
title: RemoveDrafts
tags:
- plugin/filter
uuid: e420aed3-99a8-536d-a46d-206edc499ba9
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: [[Theophysics_Glossary#Logos|Logos]] zright\Meta\RemoveDrafts.md
uuid_generated_at: '2025-11-22T01:23:49.187302'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

This plugin filters out content from your vault, so that only finalized content is made available. This prevents [[private pages]] from being published. By default, it filters out all pages with `draft: true` in the frontmatter and leaves all other pages intact.

> [!note]
> For information on how to add, remove or configure plugins, see the [[configuration#Plugins|Configuration]] page.

This plugin has no configuration options.

## API

- Category: Filter
- Function name: `Plugin.RemoveDrafts()`.
- Source: [`quartz/plugins/filters/draft.ts`](https://github.com/jackyzha0/quartz/blob/v4/quartz/plugins/filters/draft.ts).
