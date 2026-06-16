---
title: Obsidian Compatibility
tags:
- feature/transformer
uuid: 4ed13042-e56f-510c-a9a7-6b851e0e2e11
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: [[Theophysics_Glossary#Logos|Logos]] zright\Obsidian\Obsidian compatibility.md
uuid_generated_at: '2025-11-22T01:23:49.941525'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

Quartz was originally designed as a tool to publish Obsidian vaults as websites. Even as the scope of Quartz has widened over time, it hasn't lost the ability to seamlessly interoperate with Obsidian.

By default, Quartz ships with the [[ObsidianFlavoredMarkdown]] plugin, which is a transformer plugin that adds support for [Obsidian Flavored Markdown](https://help.obsidian.md/Editing+and+formatting/Obsidian+Flavored+Markdown). This includes support for features like [[wikilinks]] and [[Mermaid diagrams]].

It also ships with support for [frontmatter parsing](https://help.obsidian.md/Editing+and+formatting/Properties) with the same fields that Obsidian uses through the [[Frontmatter]] transformer plugin.

Finally, Quartz also provides [[CrawlLinks]] plugin, which allows you to customize Quartz's link resolution behaviour to match Obsidian.

## Configuration

This functionality is provided by the [[ObsidianFlavoredMarkdown]], [[Frontmatter]] and [[CrawlLinks]] plugins. See the plugin pages for customization options.
