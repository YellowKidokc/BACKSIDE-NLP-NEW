# Canon Mapping Review Prompt

You are reviewing candidate canon mappings for one article.

Inputs:

- extracted paragraph list
- candidate Master Equation hits
- candidate operator hits
- candidate proof/axiom hits

For each paragraph that maps to canon, return:

- paragraph id
- strongest canon anchor
- mapping strength: STRONG / MEDIUM / WEAK / ANALOGY_ONLY / NONE
- exact phrase that triggered the mapping
- why it maps
- what would make the mapping false
- whether this belongs in public text, hidden metadata, or reviewer notes

Do not inflate weak hits. The public workflow becomes trustworthy by refusing fake precision.
