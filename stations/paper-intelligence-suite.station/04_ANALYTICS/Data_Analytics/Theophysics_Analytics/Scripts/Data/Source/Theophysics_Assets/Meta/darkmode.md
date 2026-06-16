---
title: Darkmode
tags:
- component
uuid: d08c9b19-bc23-5166-8087-e102f8bd85e3
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\darkmode.md
uuid_generated_at: '2025-11-22T01:23:48.587819'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

Quartz supports darkmode out of the box that respects the user's theme preference. Any future manual toggles of the darkmode switch will be saved in the browser's local storage so it can be persisted across future page loads.

## Customization

- Removing darkmode: delete all usages of `Component.Darkmode()` from `quartz.layout.ts`.
- Component: `quartz/components/Darkmode.tsx`
- Style: `quartz/components/styles/darkmode.scss`
- Script: `quartz/components/scripts/darkmode.inline.ts`

You can also listen to the `themechange` event to perform any custom logic when the theme changes.

```js
document.addEventListener("themechange", (e) => {
  console.log("Theme changed to " + e.detail.theme) // either "light" or "dark"
  // your logic here
})
```
