---
title: Math Translation Layer - Extraction from Existing Repo
version: 1.0
last_updated: 2025-01-15
status: active
tags: [#extraction, #math-layer, #implementation]
source_repo: https://github.com/YellowKidokc/Math-Translation-Layer
---

# Math Translation Layer - Extraction

**Source Repository**: https://github.com/YellowKidokc/Math-Translation-Layer  
**Status**: Working efficiently, well-developed  
**Integration Target**: Tab 7 - Math Interpretation Layer

---

## Overview

The Math Translation Layer is "The Rosetta Stone Between Mathematics and Theology" - an Obsidian plugin that translates LaTeX physics equations into human-readable "Theophysics Narrative" language.

**Example Translation**:
```
LaTeX: $\chi = \int G \cdot K$
Narrative: "The Logos Field equals the integral of Grace times Knowledge"
```

---

## Core Architecture

### Three-Layer Translation System

#### Layer 1: Full Equation Overrides
**Purpose**: Context-aware translations for complete equations  
**Priority**: Highest - ensures theological accuracy

**How It Works**:
- Matches complete equations before breaking them down
- Provides context-specific interpretations
- Preserves theological meaning

**Example**:
```typescript
// Full equation match
"\\chi = \\int G \\cdot K" → "The Logos Field equals the integral of Grace times Knowledge"
```

---

#### Layer 2: Math Structure Grammar
**Purpose**: Handles LaTeX syntax and mathematical relationships  
**Priority**: Medium - preserves mathematical structure

**Supported Structures**:
- Fractions: `\frac{numerator}{denominator}`
- Integrals: `\int expression`
- Derivatives: `\frac{d}{dx}`
- Square roots: `\sqrt{expression}`
- Summations: `\sum`
- Products: `\prod`

**Example**:
```typescript
// Structure grammar
"\\frac{G}{S}" → "Grace divided by Sin"
"\\int G" → "the integral of Grace"
```

---

#### Layer 3: Symbol Vocabulary
**Purpose**: Translates individual symbols and constants  
**Priority**: Lowest - fallback for unmatched symbols

**Core Theophysics Variables**:
- `χ` (chi) → "Logos Field" or "Coherence"
- `Ψ_S` (psi) → "Soul Field"
- `G` → "Grace"
- `S` → "Sin" or "Entropy"
- `K` → "Knowledge"
- `M` → "Mercy"
- `E` → "Faith Energy"
- `T` → "Truth"
- `R` → "Repentance"
- `Q` → "Quantum State"
- `F` → "Faith"
- `C` → "Consciousness"

---

## Key Features

### 1. Instant Translation (Works on Any Page)
**User Flow**:
1. User highlights any equation in any note
2. Right-click → "Translate to Narrative"
3. Beautiful modal appears showing:
   - Math Layer (original LaTeX)
   - Narrative Layer (English translation)
4. One-click copy to clipboard

**Implementation Notes**:
- Works universally across entire vault
- No need to be in specific note or folder
- Modal UI with side-by-side display
- Instant feedback

---

### 2. AA Math Translation Hub
**Purpose**: Comprehensive dashboard of all equations in vault

**Features**:
- **Multi-Folder Scanning**: Scans multiple configured folders
  - `_Term_Pages`
  - `data analytic`
  - `complete logos final papers`
- **Auto-Generated Dashboard**: Creates hub in data analytic folder
- **Clickable File Links**: Jump directly to source files
- **Master Glossary**: All unique equations in one searchable location
- **Statistics Dashboard**:
  - Total equations found
  - Files scanned
  - Folders covered
  - Unique translations
- **Auto-Update**: Re-run scan to refresh with new equations

**Dashboard Structure**:
```markdown
# AA Math Translation Hub

## Statistics
- Total Equations: 47
- Files Scanned: 23
- Folders: 3
- Unique Translations: 42

## Equations by File

### Paper01.md
1. $\chi = \int G \cdot K$ → "The Logos Field equals..."
2. $\frac{dS}{dt} = -G$ → "The rate of change of Sin..."

### Paper02.md
...
```

---

### 3. Batch Processing
**Features**:
- **Scan Current File**: Extract and translate all math in active note
- **Recursive Folder Scan**: Process entire folders of research papers
- **Smart Indexing**: Groups translations by file for easy navigation

**Use Cases**:
- Processing entire paper at once
- Scanning research folder for all equations
- Building comprehensive equation index

---

### 4. Smart Context-Aware Translation
**How It Works**:
1. First, check Layer 1 (Full Equation Overrides)
2. If no match, parse with Layer 2 (Structure Grammar)
3. For each symbol, check Layer 3 (Symbol Vocabulary)
4. Combine results into coherent narrative

**Example Flow**:
```
Input: $\frac{dG}{dt} = -S \cdot \chi$

Step 1: Check full equation overrides → No match
Step 2: Parse structure → "d/dt of [X] equals [Y]"
Step 3: Translate symbols:
  - G → "Grace"
  - S → "Sin"
  - χ → "Coherence"
Step 4: Combine → "The rate of change of Grace equals negative Sin times Coherence"
```

---

## File Structure

```
Math-Translation-Layer/
├── main.ts                           # Main plugin logic, commands, UI
├── theophysics-math-translator.ts    # Translation engine (Rosetta Stone)
├── styles.css                        # UI styling
├── manifest.json                     # Plugin metadata
├── package.json                      # Dependencies
└── tsconfig.json                     # TypeScript config
```

---

## Key Code Components

### Translation Engine (theophysics-math-translator.ts)

**Core Functions**:
1. `translateToNarrative(latex: string): string`
   - Main translation function
   - Applies three-layer system
   - Returns English narrative

2. `scanFileForMath(content: string): MathExpression[]`
   - Extracts all LaTeX from markdown
   - Returns array of expressions with positions

3. `buildTranslationHub(folders: string[]): Dashboard`
   - Scans multiple folders
   - Aggregates all equations
   - Generates dashboard markdown

**Data Structures**:
```typescript
interface MathExpression {
  latex: string;
  narrative: string;
  sourceFile: string;
  startOffset: number;
  endOffset: number;
}

interface TranslationRule {
  pattern: string | RegExp;
  replacement: string;
  priority: number;
}
```

---

### Main Plugin (main.ts)

**Commands**:
1. `Translate Selection` - Right-click menu command
2. `Scan Current File` - Extract all math from active note
3. `Build AA Hub` - Generate translation dashboard
4. `Scan Folder` - Recursive folder processing

**UI Components**:
1. **Translation Modal**:
   - Shows Math Layer and Narrative Layer
   - Copy button
   - Close button

2. **Settings Tab**:
   - Configure folders to scan
   - Manage translation rules
   - Set output location for hub

---

## Integration with Unified Plugin

### How It Fits

**Tab 7: Math Interpretation Layer**:
- This entire repo becomes Tab 7
- Translation engine is core functionality
- UI components integrate with Glass Box design

**Connections to Other Tabs**:
1. **Tab 6 (Ontology)**: Variables link to concept definitions
2. **Tab 10 (Coherence)**: Equations feed into Lowe Lagrangian calculation
3. **Tab 13 (Master Truth)**: Math dashboard is subfolder of master-truth
4. **Semantic Blocks**: Equations stored as annotations with `kind: "equation"`

---

## Semantic Block Integration

### Current Format (Math-Translation-Layer)
Equations are extracted but not stored in semantic blocks.

### Target Format (Unified Plugin)
Equations become annotations:

```json
{
  "uuid": "eq-a1b2c3d4...",
  "kind": "equation",
  "text": "$\\chi = \\int G \\cdot K$",
  "start": 1234,
  "end": 1256,
  "properties": {
    "latex": "\\chi = \\int G \\cdot K",
    "name": "Logos Field Definition",
    "english": "The Logos Field equals the integral of Grace times Knowledge",
    "variables": ["chi", "G", "K"],
    "undefinedVariables": [],
    "domain": "coherence-theory",
    "isAxiomatic": true
  }
}
```

---

## PostgreSQL Integration

### Current State
Math-Translation-Layer doesn't use PostgreSQL.

### Target State
Equations sync to `math_objects` table:

```sql
CREATE TABLE math_objects (
    uuid UUID PRIMARY KEY REFERENCES items(uuid),
    name VARCHAR(255),
    latex TEXT NOT NULL,
    english_summary TEXT,
    variables TEXT[],
    created_by VARCHAR(50)
);
```

---

## Dashboard Generation

### Current Dashboard (AA Hub)
Generated in `data analytic` folder with:
- Statistics section
- Equations grouped by file
- Clickable file links

### Target Dashboard (Master Truth)
Location: `/master-truth/math/math-dashboard.md`

Enhanced with:
- Coherence Pulse section
- Variables registry
- Lowe Lagrangian current computation
- Undefined variables list
- Math history tracking

---

## UI Integration

### Current UI
- Standalone modal for translations
- Separate settings tab
- Independent styling

### Target UI (Glass Box)
- **Coherence Pulse**: Shows math-specific metrics
- **Semantic Lattice**: Files color-coded by math density
- **Context Prism**: Math plugin shows equations in current note
- **Main Canvas**: Equations highlighted with visual indicators
- **Command Console**: "Translate equation" command

---

## Translation Rules to Preserve

### Symbol Vocabulary (Complete List)

**Greek Letters**:
- `\chi` → "Logos Field" / "Coherence"
- `\psi` → "Soul Field" / "Witness Field"
- `\rho` → "Information Substrate"
- `\phi` → "Phase"
- `\theta` → "Angle" / "Rotation"
- `\lambda` → "Wavelength" / "Scale"
- `\omega` → "Frequency"
- `\Omega` → "Universal State"

**Theophysics Variables**:
- `G` → "Grace"
- `S` → "Sin" / "Entropy"
- `K` → "Knowledge"
- `M` → "Mercy"
- `E` → "Faith Energy"
- `T` → "Truth"
- `R` → "Repentance"
- `Q` → "Quantum State"
- `F` → "Faith"
- `C` → "Consciousness"

**Mathematical Operators**:
- `\int` → "the integral of"
- `\frac{d}{dt}` → "the rate of change of"
- `\sum` → "the sum of"
- `\prod` → "the product of"
- `\nabla` → "the gradient of"
- `\partial` → "the partial derivative of"

**Constants**:
- `\pi` → "pi"
- `e` → "Euler's number"
- `c` → "the speed of light"
- `h` → "Planck's constant"

---

## Equation Overrides to Preserve

### Master Equation
```
\chi = \rho_{info} \otimes \psi \otimes G
→ "The Coherence Field equals the tensor product of Information Substrate, Witness Field, and Grace Function"
```

### Lowe Coherence Lagrangian
```
\mathcal{L}_{LC} = \chi(t)\Big(\frac{d}{dt}\Sigma\Big)^2 - S \cdot \chi(t)
→ "Coherence equals the squared rate of collective phase alignment minus entropy interference"
```

### Grace-Entropy Relationship
```
\frac{dG}{dt} = -S \cdot \chi
→ "The rate of change of Grace equals negative Sin times Coherence"
```

---

## Migration Checklist

### Code to Extract
- [ ] Translation engine core (`theophysics-math-translator.ts`)
- [ ] Symbol vocabulary mappings
- [ ] Equation override rules
- [ ] Structure grammar parsers
- [ ] LaTeX extraction logic
- [ ] Modal UI component
- [ ] Right-click menu handler
- [ ] Dashboard generation logic
- [ ] Folder scanning logic
- [ ] Settings interface

### Features to Preserve
- [ ] Three-layer translation system
- [ ] Instant translation via right-click
- [ ] AA Hub generation
- [ ] Multi-folder scanning
- [ ] Batch processing
- [ ] Context-aware translation
- [ ] Clickable file links in dashboard
- [ ] Statistics tracking

### Enhancements to Add
- [ ] Semantic block storage
- [ ] PostgreSQL sync
- [ ] UUID assignment
- [ ] Variable-concept linking
- [ ] Coherence contribution calculation
- [ ] Integration with Lowe Lagrangian
- [ ] Historical tracking
- [ ] Undefined variable detection

---

## Testing Strategy

### Unit Tests
- Translation engine with known equations
- Symbol vocabulary lookups
- Structure grammar parsing
- LaTeX extraction from markdown

### Integration Tests
- Right-click menu → translation modal
- Folder scan → dashboard generation
- Equation → semantic block → PostgreSQL
- Math dashboard regeneration

### User Acceptance Tests
- Translate equation in any note
- Build AA Hub from multiple folders
- View math dashboard
- Check variable definitions

---

## Performance Considerations

### Current Performance
- Instant translation for single equations
- Fast folder scanning (handles hundreds of files)
- Efficient caching of translation rules

### Optimizations to Maintain
- Cache compiled regex patterns
- Lazy load translation rules
- Incremental folder scanning (only changed files)
- Background processing for large folders

---

## Documentation to Create

1. **User Guide**:
   - How to translate equations
   - How to build AA Hub
   - How to customize translations

2. **Developer Guide**:
   - Translation engine architecture
   - Adding new symbol mappings
   - Adding equation overrides
   - Extending structure grammar

3. **Integration Guide**:
   - How math layer connects to other tabs
   - Data flow diagrams
   - API reference

---

## Related Documents
- [[Tab_07_Math_Layer|Math Layer Tab Specification]]
- [[00_VAULT_SYSTEM/Config/12_Plugins/Theophysics_Obsidian_Plugin/GITHUB_INTEGRATION_PLAN|GitHub Integration Plan]]
- [[Semantic_Block_Format|Semantic Block Specification]]
- [[00_VAULT_SYSTEM/Config/12_Plugins/Theophysics_Obsidian_Plugin/04_IMPLEMENTATION/Dashboard_Generation_Specification|Dashboard Generation]]

---

## Attribution

```
Original Implementation: Math-Translation-Layer
Repository: https://github.com/YellowKidokc/Math-Translation-Layer
Author: David Lowe (YellowKidokc)

Integrated into: Theophysics Semantic Research Engine
Integration: Tab 7 - Math Interpretation Layer
Date: 2025-01-15
```

---

**Status**: Ready for extraction and integration  
**Priority**: High - Core functionality, well-developed  
**Next Steps**: Extract code, adapt to semantic block format, integrate with unified plugin
