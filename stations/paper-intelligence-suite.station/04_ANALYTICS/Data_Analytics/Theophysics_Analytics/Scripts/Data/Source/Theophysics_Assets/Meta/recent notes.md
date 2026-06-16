---
title: Recent Notes
tags: component
uuid: 245a994e-83d6-5682-8b61-c89f878f0bf2
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: [[Theophysics_Glossary#Logos|Logos]] zright\Meta\recent notes.md
uuid_generated_at: '2025-11-22T01:23:49.175129'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

Quartz can generate a list of recent notes based on some filtering and sorting criteria. Though this component isn't included in any [[layout]] by default, you can add it by using `Component.RecentNotes` in `quartz.layout.ts`.

## Customization

- Changing the title from "Recent notes": pass in an additional parameter to `Component.RecentNotes({ title: "Recent writing" })`
- Changing the number of recent notes: pass in an additional parameter to `Component.RecentNotes({ limit: 5 })`
- Display the note's tags (defaults to true): `Component.RecentNotes({ showTags: false })`
- Show a 'see more' link: pass in an additional parameter to `Component.RecentNotes({ linkToMore: "tags/components" })`. This field should be a full slug to a page that exists.
- Customize filtering: pass in an additional parameter to `Component.RecentNotes({ filter: someFilterFunction })`. The filter function should be a function that has the signature `(f: QuartzPluginData) => boolean`.
- Customize sorting: pass in an additional parameter to `Component.RecentNotes({ sort: someSortFunction })`. By default, Quartz will sort by date and then tie break lexographically. The sort function should be a function that has the signature `(f1: QuartzPluginData, f2: QuartzPluginData) => number`. See `byDateAndAlphabetical` in `quartz/components/PageList.tsx` for an example.
- Component: `quartz/components/RecentNotes.tsx`
- Style: `quartz/components/styles/recentNotes.scss`
