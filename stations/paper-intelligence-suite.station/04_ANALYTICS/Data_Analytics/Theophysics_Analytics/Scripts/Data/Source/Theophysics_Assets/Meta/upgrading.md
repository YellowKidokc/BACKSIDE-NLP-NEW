---
title: Upgrading Quartz
uuid: f1d2b7b4-4b99-5dbf-95db-2ab4b516a033
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\upgrading.md
uuid_generated_at: '2025-11-22T01:23:49.417543'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

> [!note]
> This is specifically a guide for upgrading Quartz 4 version to a more recent update. If you are coming from Quartz 3, check out the [[migrating from Quartz 3|migration guide]] for more info.

To fetch the latest Quartz updates, simply run

```bash
npx quartz update
```

As Quartz uses [git](https://git-scm.com/) under the hood for versioning, updating effectively 'pulls' in the updates from the official Quartz GitHub repository. If you have local changes that might conflict with the updates, you may need to resolve these manually yourself (or, pull manually using `git pull origin upstream`).

> [!hint]
> Quartz will try to cache your content before updating to try and prevent merge conflicts. If you get a conflict mid-merge, you can stop the merge and then run `npx quartz restore` to restore your content from the cache.

If you have the [GitHub desktop app](https://desktop.github.com/), this will automatically open to help you resolve the conflicts. Otherwise, you will need to resolve this in a text editor like VSCode. For more help on resolving conflicts manually, check out the [GitHub guide on resolving merge conflicts](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line#competing-line-change-merge-conflicts).
