---
title: Private Pages
tags:
- feature/filter
uuid: 51f7a597-89b6-55b6-aa4d-b0168a13ecdb
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: [[Theophysics_Glossary#Logos|Logos]] zright\Meta\private pages.md
uuid_generated_at: '2025-11-22T01:23:49.131371'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

There may be some notes you want to avoid publishing as a website. Quartz supports this through two mechanisms which can be used in conjunction:

## Filter Plugins

[[making plugins#Filters|Filter plugins]] are plugins that filter out content based off of certain criteria. By default, Quartz uses the [[RemoveDrafts]] plugin which filters out any note that has `draft: true` in the frontmatter.

If you'd like to only publish a select number of notes, you can instead use [[ExplicitPublish]] which will filter out all notes except for any that have `publish: true` in the frontmatter.

> [!warning]
> Regardless of the filter plugin used, **all non-markdown files will be emitted and available publically in the final build.** This includes files such as images, voice recordings, PDFs, etc.

## `ignorePatterns`

This is a field in `quartz.config.ts` under the main [[configuration]] which allows you to specify a list of patterns to effectively exclude from parsing all together. Any valid [fast-glob](https://github.com/mrmlnc/fast-glob#pattern-syntax) pattern works here.

> [!note]
> Bash's glob syntax is slightly different from fast-glob's and using bash's syntax may lead to unexpected results.

Common examples include:

- `some/folder`: exclude the entire of `some/folder`
- `*.md`: exclude all files with a `.md` extension
- `!(*.md)` exclude all files that _don't_ have a `.md` extension. Note that negations _must_ parenthesize the rest of the pattern!
- `**/private`: exclude any files or folders named `private` at any level of nesting

> [!warning]
> Marking something as private via either a plugin or through the `ignorePatterns` pattern will only prevent a page from being included in the final built site. If your GitHub repository is public, also be sure to include an ignore for those in the `.gitignore` of your Quartz. See the `git` [documentation](https://git-scm.com/docs/gitignore#_pattern_format) for more information.
