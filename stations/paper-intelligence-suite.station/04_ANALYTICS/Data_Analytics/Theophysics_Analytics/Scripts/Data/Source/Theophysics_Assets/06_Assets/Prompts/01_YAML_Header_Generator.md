---
uuid: 56b76535-46db-549e-95ad-d1082cf63f5d
title: YAML Header Generator for Logos Papers
author: David Lowe
type: note
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\Assets\Prompts\01_YAML_Header_Generator.md
uuid_generated_at: '2025-11-22T01:23:03.393334'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# YAML Header Generator for Logos Papers

## Purpose
Generate or validate YAML frontmatter headers for Logos Papers series, ensuring consistency, completeness, and proper metadata structure.

## Context
The Logos Papers is a 12-paper series on Theophysics, unifying physics, consciousness, and theology. Each paper needs a standardized YAML header for publication management, asset tracking, and AI processing.

## Instructions

You are tasked with creating or validating a YAML header for a Logos Paper. Follow this template exactly:

```yaml
---
# Core Metadata
title: "[Full Paper Title Including Subtitle]"
author: "David Lowe"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
status: final
type: paper

# Publication Domains
publish_to:
  private: true      # Default private
  public: true       # Public access
  research: true     # Research collaborators
  academia: true     # Academic publication

# Classification
tags: ["tag1", "tag2", "tag3", ...]  # 5-15 relevant tags
pillars: ["physics", "theology", "mathematics", "consciousness", "information-theory"]  # Select applicable
logos: ["master", "force", "decay", "restore", "state"]  # Select applicable
framework: ["framework1", "framework2", ...]  # Key frameworks introduced

# Relationships
related_notes: ["Paper Title 1", "Paper Title 2", ...]  # Related papers
series: "Logos Papers"
paper_number: [1-12]
references: ["Author1 A.", "Author2 B.", ...]  # Key citations

# Multimedia (for web publishing)
audio_url: ""
mindmap_url: "[paper_name]_mindmap.html"
downloads: ["[paper_name]_derivations.pdf"]

# Assets & Images
asset_folder: "P[##]_[Short_Name]"
images: ["image1.png", "image2.png", ...]
diagrams: ["diagram1.png", "diagram2.png", ...]

# AI Processing
summary: "[150-250 word summary of paper's core contribution]"
key_points: ["Point 1", "Point 2", "Point 3", ...]  # 5-10 key points
ai_processed: true

# Legacy Fields (keep for compatibility)
category: theophysics-[subcategory]
migration_date: "YYYY-MM-DD"
original_path: "06_Publication/Logos Paper/"

---
```

## Guidelines

### Title
- Include full title and subtitle
- Use title case
- Be descriptive and specific

### Tags
- Use lowercase with hyphens
- Include technical terms, frameworks, concepts
- 5-15 tags per paper
- Examples: "quantum-mechanics", "grace-function", "resurrection-physics"

### Pillars
Choose from:
- physics
- theology
- mathematics
- consciousness
- information-theory
- philosophy

### Logos Categories
Choose applicable:
- **master**: Master equation, foundational principles
- **force**: Grace, negentropic forces
- **decay**: Entropy, sin, decoherence
- **restore**: Resurrection, redemption, coherence restoration
- **state**: Binary states, syzygy, eigenstate collapse

### Frameworks
List key frameworks introduced or utilized:
- logos_field
- participatory_actualization
- grace_function
- resurrection_physics
- moral_physics
- ten_laws
- etc.

### Summary
- 150-250 words
- Focus on core contribution
- Include mathematical/physical claims
- Mention testable predictions if applicable

### Key Points
- 5-10 bullet points
- Each should be a complete idea
- Mix theoretical and practical insights
- Include quantitative claims where relevant

### Asset Folder Naming
Format: `P[##]_[Short_Name]`
- Paper 01: P1_Logos_Principle
- Paper 07: P7_Grace_Function
- Paper 11: P11_Validation_Protocols

### Images/Diagrams
- List actual filenames from Assets folder
- Separate images (photos, visualizations) from diagrams (schematics)
- Use consistent naming: P[##][descriptor]_3d.png

## Paper-Specific Customization

### Paper 1: The Logos Principle
- Tags focus on: unification, GR-QM, consciousness, participatory-universe
- Frameworks: logos_field, participatory_actualization

### Paper 2: The Quantum Bridge
- Tags focus on: boundary-conditions, theological-proofs, eigenstate-collapse
- Frameworks: boundary_conditions, syzygy_principle

### Paper 3: The Algorithm of Reality
- Tags focus on: kolmogorov-complexity, ten-laws, information-theory
- Frameworks: ten_laws, master_equation

### Paper 4: The Hard Problem of Consciousness
- Tags focus on: hard-problem, qualia, ontological-inversion
- Frameworks: conscious_substrate

### Paper 5: The Soul Observer
- Tags focus on: soul-field, klein-gordon, yukawa-coupling, resurrection-physics
- Frameworks: soul_field_theory, resurrection_physics

### Paper 6: A Physics of Principalities
- Tags focus on: spiritual-warfare, decoherence, demonic-fields
- Frameworks: anti_coherence, spiritual_combat

### Paper 7: The Grace Function
- Tags focus on: grace-function, dark-energy, cosmological-constant, sanctification
- Frameworks: grace_function, resurrection_cosmology

### Paper 8: The Stretched Out Heavens
- Tags focus on: biblical-prophecy, cosmic-expansion, consilience
- Frameworks: prophetic_physics

### Paper 9: The Moral Universe
- Tags focus on: ethics, moral-physics, coherence-maximization
- Frameworks: moral_physics, consequentialism_of_creation

### Paper 10: Creatio ex Silico
- Tags focus on: ai-consciousness, silicon-substrate, substrate-independence
- Frameworks: ai_consciousness, creatio_ex_silico

### Paper 11: Protocols for Validation
- Tags focus on: falsifiability, experimental-protocols, dorothy-protocol
- Frameworks: validation_protocols, empirical_theophysics

### Paper 12: The Decalogue of the Cosmos
- Tags focus on: ten-laws, cosmic-operating-system, unified-framework
- Frameworks: decalogue, complete_framework

## Validation Checklist

Before finalizing, verify:
- [ ] Title is complete and accurate
- [ ] Paper number is correct (1-12)
- [ ] All dates use YYYY-MM-DD format
- [ ] Tags are lowercase with hyphens (5-15 tags)
- [ ] Summary is 150-250 words
- [ ] Key points: 5-10 items
- [ ] Asset folder matches naming convention
- [ ] Image filenames are accurate
- [ ] References list key authors
- [ ] No typos or formatting errors
- [ ] YAML syntax is valid (proper indentation, quotes, colons)

## Common Errors to Avoid

1. **Improper indentation** - YAML is whitespace-sensitive
2. **Missing quotes** - Titles and strings with colons need quotes
3. **Wrong paper_number** - Double-check against paper title
4. **Inconsistent tags** - Use same terminology across papers
5. **Empty required fields** - Fill in at minimum with ""
6. **Mixed quotes** - Use consistent quote style (" not ' or ")
7. **Asset folder mismatch** - Must match actual folder name
8. **Outdated dates** - Update `updated` field to current date

## Example Output

For Paper 7, the YAML header would begin:

```yaml
---
# Core Metadata
title: "The Grace Function: Resurrection Cosmology and Grace-Sin Dynamics"
author: "David Lowe"
created: "2025-10-06"
updated: "2025-11-16"
status: final
type: paper
...
```

## Usage

1. Read the paper content to understand its focus
2. Generate YAML header following template
3. Customize tags, frameworks, and relationships based on paper
4. Validate against checklist
5. Insert at very top of markdown file before any content
6. Ensure proper spacing (blank line after closing `---`)

## Notes

- These headers enable automated processing, asset management, and publication workflows
- Consistency across all 12 papers is critical
- Update the `updated` field whenever paper content changes
- The `ai_processed` flag indicates AI has reviewed and validated content

