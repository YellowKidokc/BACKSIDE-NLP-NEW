---
title: Assets
tags:
- plugin/emitter
uuid: a908250e-9c99-5ec4-b0a6-d9a6245b1240
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\Assets.md
uuid_generated_at: '2025-11-22T01:23:48.237439'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

This plugin emits all non-Markdown static assets in your content folder (like images, videos, HTML, etc). The plugin respects the `ignorePatterns` in the global [[configuration]].

Note that all static assets will then be accessible through its path on your generated site, i.e: `host.me/path/to/static.pdf`

> [!note]
> For information on how to add, remove or configure plugins, see the [[configuration#Plugins|Configuration]] page.

This plugin has no configuration options.

## API

- Category: Emitter
- Function name: `Plugin.Assets()`.
- Source: [`quartz/plugins/emitters/assets.ts`](https://github.com/jackyzha0/quartz/blob/v4/quartz/plugins/emitters/assets.ts).
