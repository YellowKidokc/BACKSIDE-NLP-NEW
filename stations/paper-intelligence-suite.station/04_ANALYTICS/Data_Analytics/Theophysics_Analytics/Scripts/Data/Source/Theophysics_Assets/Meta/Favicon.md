---
title: Favicon
tags:
- plugin/emitter
uuid: 86b56c60-40a4-55fe-b38a-5b86180ff4dc
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\Favicon.md
uuid_generated_at: '2025-11-22T01:23:48.669505'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

This plugin emits a `favicon.ico` into the `public` folder. It creates the favicon from `icon.png` located in the `quartz/static` folder.
The plugin resizes `icon.png` to 48x48px to make it as small as possible.

> [!note]
> For information on how to add, remove or configure plugins, see the [[configuration#Plugins|Configuration]] page.

This plugin has no configuration options.

## API

- Category: Emitter
- Function name: `Plugin.Favicon()`.
- Source: [`quartz/plugins/emitters/favicon.ts`](https://github.com/jackyzha0/quartz/blob/v4/quartz/plugins/emitters/favicon.ts).
