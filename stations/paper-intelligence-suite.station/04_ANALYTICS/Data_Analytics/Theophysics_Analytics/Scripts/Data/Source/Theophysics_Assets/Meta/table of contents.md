---
title: Table of Contents
tags:
- component
- feature/transformer
uuid: 9a6681df-82b9-5c3f-9225-41e2d24b1d36
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\table of contents.md
uuid_generated_at: '2025-11-22T01:23:49.372489'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

Quartz can automatically generate a table of contents (TOC) from a list of headings on each page. It will also show you your current scrolling position on the page by highlighting headings you've scrolled through with a different color.

You can hide the TOC on a page by adding `enableToc: false` to the frontmatter for that page.

By default, the TOC shows all headings from H1 (`# Title`) to H3 (`### Title`) and is only displayed if there is more than one heading on the page.

## Customization

The table of contents is a functionality of the [[TableOfContents]] plugin. See the plugin page for more customization options.

It also needs the `TableOfContents` component, which is displayed in the right sidebar by default. You can change this by customizing the [[layout]]. The TOC component can be configured with the `layout` parameter, which can either be `modern` (default) or `legacy`.
