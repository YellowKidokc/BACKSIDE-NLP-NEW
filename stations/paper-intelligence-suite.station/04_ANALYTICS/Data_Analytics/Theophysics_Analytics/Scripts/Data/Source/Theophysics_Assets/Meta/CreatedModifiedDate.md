---
title: CreatedModifiedDate
tags:
- plugin/transformer
uuid: bba20400-bc44-530b-abd7-08371f7402fd
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\CreatedModifiedDate.md
uuid_generated_at: '2025-11-22T01:23:48.530628'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

This plugin determines the created, modified, and published dates for a document using three potential data sources: frontmatter metadata, Git history, and the filesystem. See [[authoring content#Syntax]] for more information.

> [!note]
> For information on how to add, remove or configure plugins, see the [[configuration#Plugins|Configuration]] page.

This plugin accepts the following configuration options:

- `priority`: The data sources to consult for date information. Highest priority first. Possible values are `"frontmatter"`, `"git"`, and `"filesystem"`. Defaults to `["frontmatter", "git", "filesystem"]`.

When loading the frontmatter, the value of [[Frontmatter#List]] is used.

> [!warning]
> If you rely on `git` for dates, make sure `defaultDateType` is set to `modified` in `quartz.config.ts`.
>
> Depending on how you [[hosting|host]] your Quartz, the `filesystem` dates of your local files may not match the final dates. In these cases, it may be better to use `git` or `frontmatter` to guarantee correct dates.

## API

- Category: Transformer
- Function name: `Plugin.CreatedModifiedDate()`.
- Source: [`quartz/plugins/transformers/lastmod.ts`](https://github.com/jackyzha0/quartz/blob/v4/quartz/plugins/transformers/lastmod.ts).
