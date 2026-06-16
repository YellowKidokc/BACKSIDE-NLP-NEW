---
title: FolderPage
tags:
- plugin/emitter
uuid: 15aff538-dd36-555d-b908-9303fbcbcb25
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\FolderPage.md
uuid_generated_at: '2025-11-22T01:23:48.707962'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

This plugin generates index pages for folders, creating a listing page for each folder that contains multiple content files. See [[folder and tag listings]] for more information.

Example: [[advanced/|Advanced]]

> [!note]
> For information on how to add, remove or configure plugins, see the [[configuration#Plugins|Configuration]] page.

The pages are displayed using the `defaultListPageLayout` in `quartz.layouts.ts`. For the content, the `FolderContent` component is used. If you want to modify the layout, you must edit it directly (`quartz/components/pages/FolderContent.tsx`).

This plugin accepts the following configuration options:

- `sort`: A function of type `(f1: QuartzPluginData, f2: QuartzPluginData) => number{:ts}` used to sort entries. Defaults to sorting by date and tie-breaking on lexographical order.

## API

- Category: Emitter
- Function name: `Plugin.FolderPage()`.
- Source: [`quartz/plugins/emitters/folderPage.tsx`](https://github.com/jackyzha0/quartz/blob/v4/quartz/plugins/emitters/folderPage.tsx).
