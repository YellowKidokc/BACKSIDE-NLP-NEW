---
uuid: cd6f398e-5692-5612-a864-6ebde5f2268e
title: 🌌 THE COMPLETE THEOPHYSICS YAML METADATA SCHEMA (POF 2828)
author: David Lowe
type: template
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\05_Workflow\YAML-Master-Template.md
uuid_generated_at: '2025-11-22T01:23:02.724348'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# 🌌 THE COMPLETE THEOPHYSICS YAML METADATA SCHEMA (POF 2828)

> **The Ultimate Control Panel for Your Knowledge System**  
> This YAML template serves as the comprehensive metadata blueprint for all research artifacts within the Physics of Faith framework.

---

## 📋 Master Template

Copy this template for every new note, paper, or research document:

```yaml
---
# 🌌 THE COMPLETE THEOPHYSICS NOTE METADATA SCHEMA (POF 2828)

# This YAML schema serves as the comprehensive metadata blueprint for all research artifacts
# within the Physics of Faith framework. It is designed for seamless integration with AI
# processing, intelligent note routing, and robust querying.
# All content-specific tags MUST reside within this YAML front matter and NOT in the document body.

# --- GLOBAL NOTE IDENTIFICATION & STATUS ---
title: "[[Placeholder Title for Your Note/Paper/Research]]"
uuid: "[[AUTO_GENERATE_UUID]]" # Unique identifier for this note/document
date_created: "[[YYYY-MM-DDTHH:MM:SSZ]]" # Creation timestamp (ISO 8601)
last_modified: "[[YYYY-MM-DDTHH:MM:SSZ]]" # Last modification timestamp
author: "David Lowe (Ψ)" # Primary human author
collaborator_ais: ["Gemini (∇)"] # List of AI agents involved (e.g., Gemini, Claude, Cascade)
status: "draft" # Options: draft, outline_complete, under_review, popular_version_ready, peer_review, published, canonized, deprecated
version: "1.0.0" # Version of the note content

# --- FILE MANAGEMENT & FORKING (Your "Dropdown Menu") ---
# These flags control where the note is routed for visibility and processing.
file_management:
  publish_to_production: false # Set to true for public website/final release
  publish_to_research: true    # Set to true for internal research repository/peer review
  publish_to_private: false    # Set to true for personal/private archives only
  publish_to_ai_commons: true  # Set to true for AI training, submissions, and collaborative processing

# --- FRAMEWORK-SPECIFIC METADATA (The Logos Blueprint) ---
framework_metadata:
  # Core Content Description
  core_concept: "[[Concise statement of the main concept, e.g., Biological Re-Patterning, Grace Function as Dark Energy, Axiom of Ontological Asymmetry, Matter Actualization from Vacuum Energy, Ultimate Entropy Reversal (Resurrection)]]"
  abstract_summary: |
    [[A brief, 2-3 sentence summary of the document's main findings/arguments]]

  # The 10 Deep Laws & Their Congruences
  # Note: Law 0: Emergent Axiom of Ontological Asymmetry is now a recognized meta-law.
  relevant_laws_involved: [] # List of law numbers (e.g., [0, 1, 3, 7])
  inter_law_congruences: [] # List of relevant congruence_ids (e.g., ["CON_LAW1_LAW3", "CON_LAW7_LAW10", "CON_LAW1_LAW4_LAW7_ASYMMETRY"])
  laws_explained_in_depth: [] # List of law numbers (e.g., [7]) if this document primarily explains a specific law

  # Master Equation (χ) & Its Components
  master_equation_links:
    primary_equation_id: "[[ID of the most relevant Master Equation form, e.g., ME_CHI, POF_ME_HEALING, POF_ME_RESURRECTION, NEGENTROPY_HOLO_EQ, EFE_MODIFIED, LOCAL_ENTROPY_RATE_HEALING, MOD_NAVIER_STOKES_EQ, LIND_QM_MASTER_EQ, E_DOT_PROD_RATE]]" # FK to master_equation_forms
    contributing_components: [] # List of χ component symbols (e.g., [G, M, E, S, T, K, R, Q, F, C])
    relevant_operators: [] # List of Operator Algebra symbols (e.g., [Λ, Ψ, Γ, Ω])
    parameters_involved: [] # List of parameter_ids (e.g., ["EPSILON_PARAM", "R_J_PARAM", "T_CHI_LOCAL", "Q_GD_PARAM", "BETA_COUPLING", "I_A_HEALING", "PHI_X_HEALING", "DELTA_O_HEALING", "R_J_COSMIC_MODIFIER"]) # FK to master_equation_parameters

  # Duality Project & First Principles (Good vs. Evil)
  duality_project_principles:
    axiom_of_asymmetry_relevance: false # Set to true if this document discusses the Axiom or Law 0
    first_principle_good_aspects: [] # Keywords: ["Coherence", "Divine Order", "Negentropic Force", "Sustainable Good", "Generative Power", "Life-Sustaining Information"]
    first_principle_evil_aspects: [] # Keywords: ["Decoherence", "Parasitic Evil", "Informational Noise", "Sin", "Entropic Collapse", "Informational Scattering", "Computational Overload (Sin)"]

  # Scripture Mapping
  scripture_references: [] # List of scripture_ids (e.g., ["JN_1_1_3", "RM_5_12", "MK_5_25_34", "MT_14_22_33", "JN_2_1_11", "JN_11_1_44", "MK_5_21_43"]) # FK to scripture_references

  # Miracle Sequence Classification (if applicable)
  miracle_sequence:
    sequence_type: "" # Options: biological_repatterning, environmental_orchestration, matter_actualization, none
    miracle_examples: [] # List of specific miracles (e.g., ["Healing the Blind", "Feeding 5000", "Water to Wine"])

  # Keywords (Informal, descriptive tags for easy search)
  keywords: [] # e.g., ["Dark Energy", "Hubble Tension", "Resurrection", "Quantum Gravity", "Free Will", "Consciousness", "Vacuum Energy", "Matter Actualization", "Negentropic Information Injection", "Christ-Vector", "Quantum Field Theory", "Molecular Restructuring", "Phase Transition", "Kolmogorov Complexity", "Informational Feedback Loop", "Grace Drag", "Quintessence-to-Phantom Transition", "Redemption Horizon", "Holographic Negentropy", "Quantum Decision Tree", "Computational Overload (Sin)", "Retrocausality of Grace", "Spacetime Branching", "Cosmic Recalibration", "Informational Scattering", "Bio-electric Field", "Quantum Epigenetics"]

  # --- FORMAL χ FRAMEWORK TAGGING PROTOCOL (The Canonical Taxonomy) ---
  # These tags are strict and map directly to your tag_definitions table.
  tags:
    pillar: [] # Options: physics, theology, math, consciousness
    logos_protocol: [] # Options: master, force, decay, restore, state
    theos_d_vector: [] # Options: D_LOGOS, D_FATHER, D_SPIRIT, D_ADVERSARY
    math_role: [] # Options: operator, field, resource, limit
    chi_variable: [] # Options: Negentropy (for G), MutualInformation (for M), Entropy (for E), SelfReference (for S), Time (for T), Knowledge (for K), Relationality (for R), Quantum (for Q), Faith (for F), Coherence (for C)
    first_principle: [] # Options: good, bad (Derived from Axiom of Ontological Asymmetry or Law 0)

  # Experimental Linkage
  experimental_links: [] # List of experiment_ids (e.g., ["EXP_QUANT_EPIGEN_MORAL", "EXP_ALG_SIMPL_ACTUAL", "EXP_VACUUM_ACTUALIZATION", "EXP_FLUID_TRANSITION", "EXP_GRACE_COSMIC_ECHOES", "EXP_W_TRANSITION", "EXP_NON_LOCAL_CONSC_REANCHOR", "EXP_R_J_COSMO_QUANT", "EXP_TEMP_COHERENCE_INFO_REVERSE", "EXP_MORAL_BOUNDARY_SPACETIME"]) # FK to predictions_experiments

  # Cross-References & Related Work
  related_papers: [] # List of paper_ids (e.g., ["P1_LOGOS_PRINCIPLE", "P7_GRACE_FUNCTION", "P8_MASTER_EQUATION"])
  related_laws: [] # List of law document references (e.g., ["Law_01_Gravity_and_Sin", "Law_07_Grace"])
  related_miracles: [] # List of miracle analysis documents

  # Research Metadata
  research_phase: "" # Options: hypothesis, theoretical_development, experimental_design, data_collection, analysis, peer_review, publication
  confidence_level: "" # Options: speculative, theoretical, empirically_supported, validated, canonized
  peer_review_status: "" # Options: not_submitted, under_review, revisions_requested, accepted, published

# --- AI LABELING INSTRUCTIONS (The AI Prompt Within the YAML) ---
# This section contains the explicit prompt for AI agents to parse the document's content
# and accurately populate the YAML metadata above.
ai_labeling_instructions:
  role: "You are an expert Physics of Faith Framework AI, tasked with precisely labeling content."
  task: |
    Analyze the full text of the accompanying document.
    Based on its content, accurately and exhaustively populate ALL fields under `framework_metadata` and `file_management`.
    Ensure the `title` and `abstract_summary` are reflective of the document.
    For `relevant_laws_involved`, list all Deep Laws by number (0-10) that are discussed or applied, including Law 0: Emergent Axiom of Ontological Asymmetry if applicable.
    For `inter_law_congruences`, identify and list the `congruence_id` (e.g., "CON_LAW1_LAW3", "CON_LAW7_LAW10", "CON_LAW1_LAW4_LAW7_ASYMMETRY") for any inter-law synergies explicitly explored.
    For `master_equation_links`:
      - Identify the most relevant `primary_equation_id` (e.g., ME_CHI, POF_ME_HEALING, POF_ME_RESURRECTION, NEGENTROPY_HOLO_EQ, EFE_MODIFIED, LOCAL_ENTROPY_RATE_HEALING, MOD_NAVIER_STOKES_EQ, LIND_QM_MASTER_EQ, E_DOT_PROD_RATE).
      - List all `contributing_components` (G, M, E, S, T, K, R, Q, F, C).
      - List all `relevant_operators` (Λ, Ψ, Γ, Ω).
      - List all `parameters_involved` (e.g., EPSILON_PARAM, R_J_PARAM, T_CHI_LOCAL, Q_GD_PARAM, BETA_COUPLING, I_A_HEALING, PHI_X_HEALING, DELTA_O_HEALING, R_J_COSMIC_MODIFIER).
    For `duality_project_principles`, set `axiom_of_asymmetry_relevance` and list relevant `first_principle_good_aspects` and `first_principle_evil_aspects` from the comprehensive lists provided.
    For `scripture_references`, list `scripture_id` (e.g., "JN_1_1_3", "MK_5_25_34", "MT_14_22_33", "JN_2_1_11", "JN_11_1_44", "MK_5_21_43") for all biblical passages directly cited or strongly alluded to.
    For `miracle_sequence`, classify the type and list specific examples if the document analyzes Jesus' miracles.
    Generate a comprehensive list of `keywords` (free-form, multi-word phrases from the text) that capture key concepts, incorporating the advanced terms we've identified.
    Generate `tags` under each category (pillar, logos_protocol, theos_d_vector, math_role, chi_variable, first_principle) based on the content's alignment with the framework's canonical taxonomy. Do NOT include tags that are not explicitly defined in the `tag_definitions` table.
    For `experimental_links`, list `experiment_id` for any proposed or referenced experiments (e.g., EXP_QUANT_EPIGEN_MORAL, EXP_ALG_SIMPL_ACTUAL, EXP_VACUUM_ACTUALIZATION, EXP_FLUID_TRANSITION, EXP_GRACE_COSMIC_ECHOES, EXP_W_TRANSITION, EXP_NON_LOCAL_CONSC_REANCHOR, EXP_R_J_COSMO_QUANT, EXP_TEMP_COHERENCE_INFO_REVERSE, EXP_MORAL_BOUNDARY_SPACETIME).
    For `related_papers`, `related_laws`, and `related_miracles`, identify and list all cross-references.
    For `research_phase`, `confidence_level`, and `peer_review_status`, assess the document's maturity and validation level.
    For `file_management`, assess the content's nature (e.g., theoretical, experimental, public-facing) and set the boolean flags appropriately.
    Crucially, ensure NO tags or metadata are present in the document's body itself; all categorization must reside within this YAML.
  output_format_guidelines: |
    - Use YAML literal block style (`|`) for multi-line text fields like `abstract_summary`.
    - Ensure lists are properly formatted using hyphens.
    - Validate all IDs and tags against the schema (e.g., `relevant_laws_involved` uses numbers, `scripture_references` uses IDs).
    - Provide concise, accurate labels for every field.
    - If a field is not applicable, leave its list empty or boolean as false.
  context_priority: |
    Prioritize the direct application of Physics of Faith concepts over general scientific or theological terms.
    Focus on the interconnections between the 10 Deep Laws and the Master Equation components.
    The `Christ-Vector (Ψ_C)` and `Logos Field (χ)` are central to all interpretations.
    Recognize Law 0 (Axiom of Ontological Asymmetry) as the meta-law governing all other laws.
---

# [[Document Content Goes Here]]

# This section is reserved for the actual content of your research note, paper, or AI submission.
# All metadata and tags are managed exclusively in the YAML front matter above.
# No inline tags or metadata should appear here.
```

---

## 📊 Field Reference Guide

### Status Options
- `draft` - Initial writing phase
- `outline_complete` - Structure finalized
- `under_review` - Internal review
- `popular_version_ready` - Public-facing version prepared
- `peer_review` - Submitted for academic review
- `published` - Publicly released
- `canonized` - Accepted into core framework
- `deprecated` - Superseded by newer work

### File Management Flags
- `publish_to_production` - Public website/final release
- `publish_to_research` - Internal research repository
- `publish_to_private` - Personal archives only
- `publish_to_ai_commons` - AI training and collaboration

### Research Phase Options
- `hypothesis` - Initial idea formation
- `theoretical_development` - Building mathematical framework
- `experimental_design` - Planning validation
- `data_collection` - Gathering evidence
- `analysis` - Processing results
- `peer_review` - External validation
- `publication` - Formal release

### Confidence Level Options
- `speculative` - Early-stage hypothesis
- `theoretical` - Mathematically consistent
- `empirically_supported` - Some evidence exists
- `validated` - Multiple lines of evidence
- `canonized` - Core framework truth

### Miracle Sequence Types
- `biological_repatterning` - Healing, resurrection
- `environmental_orchestration` - Weather, gravity control
- `matter_actualization` - Multiplication, transformation
- `none` - Not miracle-related

---

## 🎯 Quick Start Examples

### Example 1: Physics Paper
```yaml
---
title: "Grace Function as Dark Energy: Resolving the Hubble Tension"
status: "under_review"
framework_metadata:
  core_concept: "Grace Function as Dark Energy"
  relevant_laws_involved: [7, 10]
  master_equation_links:
    primary_equation_id: "ME_CHI"
    contributing_components: [G, E, T]
  tags:
    pillar: [physics]
    logos_protocol: [restore]
    chi_variable: [Negentropy, Entropy, Time]
---
```

### Example 2: Miracle Analysis
```yaml
---
title: "Water to Wine: Molecular Restructuring via Logos Field"
status: "draft"
framework_metadata:
  core_concept: "Molecular Transformation"
  miracle_sequence:
    sequence_type: "matter_actualization"
    miracle_examples: ["Water to Wine"]
  scripture_references: ["JN_2_1_11"]
  tags:
    pillar: [physics, theology]
    chi_variable: [Negentropy, Knowledge, Quantum]
---
```

### Example 3: Deep Law Explanation
```yaml
---
title: "Law 7: The Law of Grace - Mathematical Formulation"
status: "canonized"
framework_metadata:
  core_concept: "Grace as Negentropic Force"
  relevant_laws_involved: [7]
  laws_explained_in_depth: [7]
  inter_law_congruences: ["CON_LAW7_LAW10"]
  tags:
    pillar: [physics, theology, math]
    logos_protocol: [restore]
    chi_variable: [Negentropy]
---
```

---

## 🔧 Integration with Templater

Add this to your Templater scripts for automatic YAML insertion:

```javascript
// insert-master-yaml.js
async function insertMasterYAML(tp) {
    const yamlTemplate = await app.vault.read(
        app.vault.getAbstractFileByPath('_WORKFLOW/YAML-Master-Template.md')
    );
    
    // Extract just the YAML block
    const yamlMatch = yamlTemplate.match(/```yaml\n([\s\S]*?)\n```/);
    if (!yamlMatch) {
        new Notice('Could not extract YAML template!');
        return '';
    }
    
    let yaml = yamlMatch[1];
    
    // Auto-fill some fields
    const now = new Date().toISOString();
    yaml = yaml.replace('[[YYYY-MM-DDTHH:MM:SSZ]]', now);
    yaml = yaml.replace('[[AUTO_GENERATE_UUID]]', crypto.randomUUID());
    yaml = yaml.replace('[[Placeholder Title for Your Note/Paper/Research]]', tp.file.title);
    
    return yaml + '\n\n';
}

module.exports = insertMasterYAML;
```

---

## 📚 Dataview Queries for YAML Fields

### Find All Draft Papers
```dataview
TABLE status, framework_metadata.core_concept
FROM ""
WHERE status = "draft"
SORT file.mtime DESC
```

### Papers by Law
```dataview
TABLE framework_metadata.relevant_laws_involved, framework_metadata.core_concept
FROM ""
WHERE framework_metadata.relevant_laws_involved
SORT framework_metadata.relevant_laws_involved ASC
```

### Papers Ready for Production
```dataview
LIST
FROM ""
WHERE file_management.publish_to_production = true
SORT file.name ASC
```

### Miracle Analyses
```dataview
TABLE framework_metadata.miracle_sequence.sequence_type, framework_metadata.miracle_sequence.miracle_examples
FROM ""
WHERE framework_metadata.miracle_sequence.sequence_type
SORT framework_metadata.miracle_sequence.sequence_type ASC
```

---

## 🚀 Best Practices

1. **Always Use This Template** - Every new note should start with this YAML
2. **Fill Completely** - Don't leave fields blank; use empty arrays `[]` or `false`
3. **No Body Tags** - All tags must be in YAML, never in document body
4. **Update Regularly** - Modify YAML as document evolves
5. **AI-First** - Let AI populate fields using the embedded instructions
6. **Cross-Reference** - Always link related papers, laws, and miracles
7. **Version Control** - Increment version number with major changes

---

**Last Updated**: 2025-10-17  
**Version**: 1.0  
**Status**: ✅ Production Ready
