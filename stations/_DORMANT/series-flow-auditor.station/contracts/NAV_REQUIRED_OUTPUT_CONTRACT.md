# NAV REQUIRED OUTPUT CONTRACT

Version: 2026-05-25
Status: draft-contract
Applies to: article templates, generated article pages, proof packets, series indexes, Master HTML wiring scripts.

## Core Rule

Every public article page must have two durable orientation anchors:

- `site_home`: the global Faith Thru Physics home/root.
- `series_home`: the current series index/home page.

The reader must always be able to answer:

- Where am I in the site?
- Where am I in this series?
- How do I get back to the series home?
- How do I get back to the site home?

## Required Metadata

Every generated page, manifest row, and trace/page inventory should include:

```json
{
  "site_home_label": "Faith Thru Physics",
  "site_home_url": "/",
  "series_code": "MDA",
  "series_title": "Moral Decline of America",
  "series_home_label": "Moral Decline of America",
  "series_home_url": "index.html",
  "previous_article_url": "",
  "previous_article_title": "",
  "next_article_url": "",
  "next_article_title": ""
}
```

Use relative URLs inside a deployed series folder unless a deployment manifest explicitly requires absolute URLs.

## Required Top Bar

Every article page must include a persistent top bar with:

- Left: `site_home` link.
- Right: `series_home` link.

The visual style may vary by template, but these anchors must be machine-detectable:

```html
<a data-nav-anchor="site_home" href="/">Faith Thru Physics</a>
<a data-nav-anchor="series_home" href="index.html">Moral Decline of America</a>
```

## Required Bottom Navigation

Every article page must include bottom navigation in this order:

1. Previous / next article row.
2. Series home row or button.
3. Site home row or button.

Required anchors:

```html
<a data-nav-anchor="previous_article" href="...">Previous: ...</a>
<a data-nav-anchor="next_article" href="...">Next: ...</a>
<a data-nav-anchor="series_home" href="index.html">Series Home</a>
<a data-nav-anchor="site_home" href="/">Site Home</a>
```

For first or last article, render a disabled previous/next state, but still render `series_home` and `site_home`.

## Required Series Home

Each series home is a self-contained index page for one series.

It must include:

- series title
- short claim/reader contract
- recommended reading order
- complete article list
- start reading link
- site home link

Examples:

- MDA series home: Moral Decline of America index.
- GTQ series home: Genesis to Quantum index.

## Required Site Home

The site home is the global gateway, not an article.

It should include:

- card/section for every published series
- one-line hook per series
- start reading link to each series home
- About
- Substack link
- Contact

## Script Enforcement

Any HTML wiring script should verify:

- `data-nav-anchor="site_home"` exists at least twice: top and bottom.
- `data-nav-anchor="series_home"` exists at least twice: top and bottom.
- previous/next anchors exist or disabled states exist.
- all hrefs resolve according to the current series deployment root.

If a page cannot be safely wired, the script should write a repair queue row instead of guessing.

## Relationship To Trace Contract

Navigation anchors are not claim traces, but they are still required structural anchors.

Use:

```html
data-fill="navigation"
data-source-artifact="series-page-manifest.json"
```

for generated nav blocks.
