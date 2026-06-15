# 🔺 Trinity Coherence Heatmap (DataviewJS)
```dataviewjs
const rows = dv.pages().where(p => p.trinity_aspects && p.title).map(p => {
  const F = p.trinity_aspects.Father ?? 0;
  const S = p.trinity_aspects.Son ?? 0;
  const H = p.trinity_aspects.Spirit ?? 0;
  return {title: p.file.link, Father: Number(F), Son: Number(S), Spirit: Number(H)};
}).array();

dv.table(["Note","Father","Son","Spirit"],
  rows.map(r => [r.title, r.Father.toFixed(2), r.Son.toFixed(2), r.Spirit.toFixed(2)]));
```
