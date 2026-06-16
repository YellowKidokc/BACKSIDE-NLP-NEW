---
title: Roam Research Compatibility
tags:
- feature/transformer
uuid: 069834c0-7bb6-5c89-8930-4b1e889864d9
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\Roam Research compatibility.md
uuid_generated_at: '2025-11-22T01:23:49.216020'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

[Roam Research](https://roamresearch.com) is a note-taking tool that organizes your knowledge graph in a unique and interconnected way.

Quartz supports transforming the special Markdown syntax from Roam Research (like `{{[[components]]}}` and other formatting) into
regular Markdown via the [[RoamFlavoredMarkdown]] plugin.

```typescript title="quartz.config.ts"
plugins: {
  transformers: [
    // ...
    Plugin.RoamFlavoredMarkdown(),
    Plugin.ObsidianFlavoredMarkdown(),
    // ...
  ],
},
```

> [!warning]
> As seen above placement of `Plugin.RoamFlavoredMarkdown()` within `quartz.config.ts` is very important. It must come before `Plugin.ObsidianFlavoredMarkdown()`.

## Customization

This functionality is provided by the [[RoamFlavoredMarkdown]] plugin. See the plugin page for customization options.
