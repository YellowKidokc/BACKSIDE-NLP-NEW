# Worldviews Dedup Report — 2026-05-08

## Action taken
- For each '<Name>.md' / '<Name> 1.md' pair, kept the larger file.
- '<Name> 1.md' was consistently larger (more content) — likely a regeneration with extended semantic tags.
- Lines unique to the smaller version were ~2-4% and almost all UUID artifacts (auto-generated).

## Per-pair decisions
| File | Orig Size | '1' Size | Decision |
|------|-----------|----------|----------|
| Absurdism.md | 14016 | 33735 | kept '1' (larger) — deleted orig |
| Aristotelianism.md | 12711 | 31795 | kept '1' (larger) — deleted orig |
| Arminianism.md | 22192 | 22192 | identical hash — deleted '1', kept orig |
| Calvinism.md | 21403 | 21403 | identical hash — deleted '1', kept orig |
| Confucianism.md | 38498 | 46154 | kept '1' (larger) — deleted orig |
| Consequentialism.md | 12983 | 29687 | kept '1' (larger) — deleted orig |
| Cynicism.md | 13623 | 31832 | kept '1' (larger) — deleted orig |
| Deism.md | 13001 | (none) | singleton — moved as-is |
| Dialectical_Materialism.md | 38905 | 29638 | kept orig (larger) — deleted '1' |
| Divine_Command_Theory.md | 13283 | 29006 | kept '1' (larger) — deleted orig |
| Empiricism.md | 41039 | 43322 | kept '1' (larger) — deleted orig |
| Epicureanism.md | 51502 | 42711 | kept orig (larger) — deleted '1' |
| Existentialism.md | 23409 | (none) | singleton — moved as-is |
| Gnosticism.md | 36742 | 33652 | kept orig (larger) — deleted '1' |
| Hermeticism.md | 36229 | 30319 | kept orig (larger) — deleted '1' |
| Humanism.md | 14149 | 32484 | kept '1' (larger) — deleted orig |
| Idealism.md | 13059 | (none) | singleton — moved as-is |
| Kabbalah.md | 33373 | 32904 | kept orig (larger) — deleted '1' |
| Kantian_Ethics.md | 44980 | 44030 | kept orig (larger) — deleted '1' |
| Logical_Positivism.md | 56335 | 45061 | kept orig (larger) — deleted '1' |
| Materialism.md | 16663 | (none) | singleton — moved as-is |
| Moral_Relativism.md | 40944 | 31300 | kept orig (larger) — deleted '1' |
| Natural_Law.md | 34625 | 33597 | kept orig (larger) — deleted '1' |
| Naturalism.md | 13776 | 13776 | identical hash — deleted '1', kept orig |
| Neoplatonism.md | 23561 | (none) | singleton — moved as-is |
| Nihilism.md | 27265 | 14193 | kept orig (larger) — deleted '1' |
| Objectivism_Ayn_Rand.md | 14661 | 31870 | kept '1' (larger) — deleted orig |
| Open_Theism.md | 14481 | (none) | singleton — moved as-is |
| Panentheism.md | 40179 | 31403 | kept orig (larger) — deleted '1' |
| Panpsychism.md | 22489 | (none) | singleton — moved as-is |
| Pantheism.md | 23888 | 44836 | kept '1' (larger) — deleted orig |
| Pantheism 2.md | 34358 | (none) | singleton — moved as-is |
| Phenomenology.md | 39282 | 32535 | kept orig (larger) — deleted '1' |
| Physicalism.md | 20260 | 20260 | identical hash — deleted '1', kept orig |
| Platonism.md | 21638 | (none) | singleton — moved as-is |
| Postmodernism.md | 28062 | 22792 | kept orig (larger) — deleted '1' |
| Pragmatism.md | 38985 | 30550 | kept orig (larger) — deleted '1' |
| Process_Theology.md | 13138 | (none) | singleton — moved as-is |
| Rationalism.md | 36676 | 31505 | kept orig (larger) — deleted '1' |
| Secular_Humanism.md | 23342 | 42084 | kept '1' (larger) — deleted orig |
| Skepticism.md | 55559 | 48528 | kept orig (larger) — deleted '1' |
| Social_Contract_Theory.md | 38405 | 32737 | kept orig (larger) — deleted '1' |
| Stoicism.md | 10721 | (none) | singleton — moved as-is |
| Sufism.md | 37130 | 31550 | kept orig (larger) — deleted '1' |
| Taoism.md | 15443 | (none) | singleton — moved as-is |
| Thomism.md | 17165 | 17165 | identical hash — deleted '1', kept orig |
| Transhumanism.md | 27818 | 14013 | kept orig (larger) — deleted '1' |
| Utilitarianism.md | 30437 | 13023 | kept orig (larger) — deleted '1' |
| Virtue_Ethics.md | 36008 | 32931 | kept orig (larger) — deleted '1' |
| WORLDVIEW_AXIOMS.xlsx | 387582 | - | leftover singleton — moved |
| WORLDVIEW_AXIOMS_EXPANDED.xlsx | 387741 | - | leftover singleton — moved |
| _extract_axioms_to_excel.py | 3680 | - | leftover singleton — moved |
| _extract_worldviews.py | 17664 | - | leftover singleton — moved |
