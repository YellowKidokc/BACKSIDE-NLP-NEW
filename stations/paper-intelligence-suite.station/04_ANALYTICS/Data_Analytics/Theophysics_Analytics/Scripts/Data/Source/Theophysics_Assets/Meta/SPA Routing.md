---
uuid: 4b03f119-bedd-5137-9172-486d703ee063
title: SPA Routing
author: David Lowe
type: note
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: [[Theophysics_Glossary#Logos|Logos]] zright\Meta\SPA Routing.md
uuid_generated_at: '2025-11-22T01:23:49.297145'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

Single-page-app style rendering. This prevents flashes of unstyled content and improves the smoothness of Quartz.

Under the hood, this is done by hijacking page navigations and instead fetching the HTML via a `GET` request and then diffing and selectively replacing parts of the page using [micromorph](https://github.com/natemoo-re/micromorph). This allows us to change the content of the page without fully refreshing the page, reducing the amount of content that the browser needs to load.

## Configuration

- Disable SPA Routing: set the `enableSPA` field of the [[configuration]] in `quartz.config.ts` to be `false`.
