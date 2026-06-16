---
uuid: f67003c6-9d64-5326-b3f0-b1c165722244
title: RSS Feed
author: David Lowe
type: note
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\RSS Feed.md
uuid_generated_at: '2025-11-22T01:23:49.241672'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

Quartz emits an RSS feed for all the content on your site by generating an `index.xml` file that RSS readers can subscribe to. Because of the RSS spec, this requires the `baseUrl` property in your [[configuration]] to be set properly for RSS readers to pick it up properly.

> [!info]
> After deploying, the generated RSS link will be available at `https://${baseUrl}/index.xml` by default.
>
> The `index.xml` path can be customized by passing the `rssSlug` option to the [[ContentIndex]] plugin.

## Configuration

This functionality is provided by the [[ContentIndex]] plugin. See the plugin page for customization options.
