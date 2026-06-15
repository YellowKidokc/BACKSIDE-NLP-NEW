---
title: ExplicitPublish
tags:
- plugin/filter
uuid: 0637b208-0fd1-5141-9cc2-8a1236b642ef
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\ExplicitPublish.md
uuid_generated_at: '2025-11-22T01:23:48.636447'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

This plugin filters content based on an explicit `publish` flag in the frontmatter, allowing only content that is explicitly marked for publication to pass through. It's the opt-in version of [[RemoveDrafts]]. See [[private pages]] for more information.

> [!note]
> For information on how to add, remove or configure plugins, see the [[configuration#Plugins|Configuration]] page.

This plugin has no configuration options.

## API

- Category: Filter
- Function name: `Plugin.ExplicitPublish()`.
- Source: [`quartz/plugins/filters/explicit.ts`](https://github.com/jackyzha0/quartz/blob/v4/quartz/plugins/filters/explicit.ts).
