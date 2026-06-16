---
title: Building your Quartz
uuid: 37666e19-eec8-5376-b522-8eebd616848d
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\build.md
uuid_generated_at: '2025-11-22T01:23:48.321848'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

Once you've [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Meta/Index#🪴 Get Started|initialized]] Quartz, let's see what it looks like locally:

```bash
npx quartz build --serve
```

This will start a local web server to run your Quartz on your computer. Open a web browser and visit `http://localhost:8080/` to view it.

> [!hint] Flags and options
> For full help options, you can run `npx quartz build --help`.
>
> Most of these have sensible defaults but you can override them if you have a custom setup:
>
> - `-d` or `--directory`: the content folder. This is normally just `content`
> - `-v` or `--verbose`: print out extra logging information
> - `-o` or `--output`: the output folder. This is normally just `public`
> - `--serve`: run a local hot-reloading server to preview your Quartz
> - `--port`: what port to run the local preview server on
> - `--concurrency`: how many threads to use to parse notes

> [!warning] Not to be used for production
> Serve mode is intended for local previews only.
> For production workloads, see the page on [[hosting]].
