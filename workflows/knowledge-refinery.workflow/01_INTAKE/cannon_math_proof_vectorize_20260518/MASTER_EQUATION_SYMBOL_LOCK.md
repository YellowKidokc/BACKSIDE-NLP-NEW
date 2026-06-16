# Master Equation Symbol Lock

Run context: 2026-05-18  
Purpose: prevent symbol/operator drift before using the Master Equation inside the OT diagnostic derivation, Lane-4 proof, Axiom/7Q review, or Lean 4 preparation.

## Core Rule

Do not change symbol meanings between lanes.

If a symbol is used mathematically, the theological/narrative meaning must be marked as interpretation, mapping, or bridge — not silently folded into the formal definition.

## Working Equation

```text
dC/dt = O · G · (1-C) - S · C
```

Expanded covering variant:

```text
dC/dt = O · G · (1-C) - S · (1-α) · C
0 < α < 1
```

## Canonical Symbol Table

| Symbol | Formal Type | Formal Domain | Formal Function | Theological / Narrative Mapping | Lane |
|---|---|---|---|---|---|
| `C` | state variable | coherence dynamics | current coherence / integration level | creation coherence; later Christological completion only in NT fulfillment lane | `AUDITABLE-HOW` / `BRIDGE-CLAIM` |
| `χ` | output / integral measure | total system coherence | product/integrated coherence result | total coherence witness; do not collapse with `C` unless explicitly declared | `AUDITABLE-HOW` / `BRIDGE-CLAIM` |
| `S` | attenuation/decoherence term or operator | entropy/sin dynamics | degrades existing coherence | sin/corruption as parasitic degradation | `BRIDGE-CLAIM` |
| `G` | source term / restoration operator | coherence dynamics | non-self-generated coherence input | grace as external restoration | `BRIDGE-CLAIM` |
| `O` | coupling variable | observer / will posture | permits or blocks reception of `G` | openness, surrender, voluntary coupling | `BRIDGE-CLAIM` |
| `W` | agency variable | will / choice space | capacity for morally meaningful choice | free will; must not be collapsed into openness | `INTERPRETIVE-WHY` / `BRIDGE-CLAIM` |
| `α` | attenuation coefficient | covering/provisional restraint | dampens `S` without eliminating it | sacrificial covering / covenantal shielding | `BRIDGE-CLAIM` |
| `J` | constraint / objective component | justice condition | preserves standard / addresses wrong | divine justice | `INTERPRETIVE-WHY` / `BRIDGE-CLAIM` |
| `M` | constraint / objective component | mercy condition | permits restoration of person | divine mercy | `INTERPRETIVE-WHY` / `BRIDGE-CLAIM` |
| `T` | transformation condition | restoration dynamics | changes the person/system, not merely location | regeneration/sanctification preview | `BRIDGE-CLAIM` / `DEFERRED-NT` |
| `δ` | displacement / rupture term | moral conservation | nonzero moral displacement introduced by wrongdoing | guilt/rupture/cost that cannot be ignored | `BRIDGE-CLAIM` |
| `H_divine` | threshold function | holiness compatibility | tests unmediated compatibility with perfect holiness | divine holiness threshold | `INTERPRETIVE-WHY` / `BRIDGE-CLAIM` |
| `G_human` | graded evaluation function | human moral judgment | ranks harm/intent/consequence | human moral gradient | `INTERPRETIVE-WHY` |

## Non-Drift Rules

### 1. `C` and `χ`

Do not casually identify `C = χ`.

Allowed:

```text
In a specified model, χ may be defined as an integrated/product measure of coherence derived from component C_i terms.
```

Not allowed:

```text
C is χ is Christ is the equation
```

unless this is explicitly marked as narrative/theological interpretation, not formal identity.

### 2. `G` and Grace

`G` is formally a source/restoration term or operator.

The statement “`G` maps to grace” is a bridge claim.

Do not treat the symbol itself as proof of theological grace.

### 3. `S` and Sin

`S` formally degrades coherence.

The statement “`S` maps to sin/corruption” is a bridge claim.

If `S` is used as scalar in one row and operator in another, state which model is active.

### 4. `O` and `W`

Do not collapse openness into agency.

```text
W = capacity for meaningful choice
O = receptive posture / coupling to grace
```

A being may possess `W` and still set `O` near zero.

### 5. `α`

`α` is not atonement completion.

`α` is provisional attenuation/covering:

```text
0 < α < 1
```

If `α = 1`, the model has accidentally made covering equivalent to completion.

### 6. `J`, `M`, `T`

Justice, mercy, and transformation should be treated as constraints or objective requirements until a more precise formal model is chosen.

Do not present them as measured physical variables.

### 7. `H_divine` and `G_human`

Keep the two-register distinction:

```text
G_human = graded moral evaluation
H_divine = holiness compatibility threshold
```

This prevents the “all sins are identical” overclaim.

## Lane Discipline

Every use of a symbol should identify its lane:

| Lane | What The Symbol Can Do |
|---|---|
| `AUDITABLE-HOW` | formal mechanism, equation behavior, proof condition |
| `INTERPRETIVE-WHY` | theological meaning, teleology, purpose |
| `BRIDGE-CLAIM` | structural mapping between formal behavior and theological story |
| `HISTORICAL-WEIGHT` | relevance to historical claim, not mathematical proof |
| `NARRATIVE-REFRAIN` | rhetorical/story role, not proof |

## Publication Warning

Before public release, produce a clean notation table and use one symbol set throughout.

Known drift risks:

- older docs may use different law numbers
- `C`, `χ`, and Christ/coherence language may be over-identified
- `G` may alternate between scalar, source term, and operator
- `S` may alternate between scalar sin-pressure and decoherence operator
- `O` may be confused with free will instead of openness
- sacrifice covering `α` may be overstated as completion

## Review Checklist

Before using the Master Equation in any proof section, answer:

1. Is this symbol scalar, vector, operator, gate, coefficient, source term, or state variable?
2. Which lane is active?
3. Is the theological meaning formal definition or bridge interpretation?
4. Has this symbol been used differently elsewhere?
5. Does the argument depend on the formal behavior or the narrative mapping?

If those cannot be answered, pause and relabel before continuing.
