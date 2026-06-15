# Prompt For Reading-Level QA

You are reviewing Easy and Academic generated versions.

For each article, compare:

- Standard source
- Easy version
- Academic version

Check:

1. Easy preserves the claim but lowers reading burden.
2. Academic adds method/caveats without overclaiming.
3. Neither version changes the thesis.
4. Math terms are translated but not watered down.
5. No theological claim is converted into a fake scientific proof.

Return:

```markdown
Article:
Easy status: PASS / FIX / HOLD
Academic status: PASS / FIX / HOLD
Meaning drift:
Overclaim risk:
Missing definitions:
Recommended patch:
```
