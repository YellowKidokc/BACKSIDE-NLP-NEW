---
title: Static
tags:
- plugin/emitter
uuid: 415cd1cd-9c90-54c0-8615-31ad70327acb
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\Static.md
uuid_generated_at: '2025-11-22T01:23:49.309575'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

This plugin emits all static resources needed by Quartz. This is used, for example, for fonts and images that need a stable position, such as banners and icons. The plugin respects the `ignorePatterns` in the global [[configuration]].

> [!important]
> This is different from [[Assets]]. The resources from the [[Static]] plugin are located under `quartz/static`, whereas [[Assets]] renders all static resources under `content` and is used for images, videos, audio, etc. that are directly referenced by your markdown content.

> [!note]
> For information on how to add, remove or configure plugins, see the [[configuration#Plugins|Configuration]] page.

This plugin has no configuration options.

## API

- Category: Emitter
- Function name: `Plugin.Static()`.
- Source: [`quartz/plugins/emitters/static.ts`](https://github.com/jackyzha0/quartz/blob/v4/quartz/plugins/emitters/static.ts).
