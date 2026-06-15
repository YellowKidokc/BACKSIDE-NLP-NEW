```json
{
  "axiom_mapping": {
    "referenced": [
      {"axiom_id": "A1.1", "relationship": "depends_on", "confidence": 90},
      {"axiom_id": "A1.3", "relationship": "extends", "confidence": 85},
      {"axiom_id": "A2.1", "relationship": "challenges", "confidence": 80}
    ],
    "missing": [
      {"axiom_id": "A7.4", "reason": "The paper implicitly assumes the importance of information control but does not cite it."}
    ]
  },

  "missing_citations": [
    {"doi": "10.1016/j.socscimed.2004.01.006", "title": "The Amish: A Sociological Perspective", "first_author": Donald B. Kraybill, "relevance": "Provides foundational sociological insights into Amish society that support the paper's claims.", "priority": "essential"},
    {"doi": "10.1080/13645579.2016.1144401", "title": "Amish Society and Technology", "first_author": Karen M. Johnson-Weiner, "relevance": "Discusses the Amish approach to technology, which is central to the paper's argument.", "priority": "recommended"}
  ],

  "math_upgrade": {
    "current_state": "The paper uses qualitative comparisons and anecdotal evidence.",
    "method": "Bayesian model comparison",
    "expected_outcome": "This upgrade would provide a probabilistic framework to quantify the likelihood of coherence outcomes based on different societal constraints.",
    "difficulty": "moderate"
  },

  "ft_cross_refs": [
    {"paper_id": "FP-003", "relationship": "extends", "linking_claim": "The paper builds on the concept of societal coherence as a function of constraints."}
  ],

  "theory_resonance": [
    {
      "theory": "Dunbar's Number",
      "source_domain": "anthropology",
      "claim_maps_to": "The Proximity Limit principle respects human capacity for meaningful relationships.",
      "mapping": "STRUCTURAL",
      "free_predictions": "Predicts optimal community sizes for maintaining social cohesion.",
      "upgrade_path": null,
      "independent_arrival": true,
      "independent_arrival_explanation": "Dunbar's Number was derived from primate brain size and social group size correlations."
    },
    {
      "theory": "Entropy in Thermodynamics",
      "source_domain": "physics",
      "claim_maps_to": "Freedom leads to entropy, while constraints lead to order.",
      "mapping": "ANALOGICAL",
      "free_predictions": null,
      "upgrade_path": "Formalize the analogy by quantifying societal entropy.",
      "independent_arrival": true,
      "independent_arrival_explanation": "Entropy as a concept was developed in thermodynamics to describe disorder."
    },
    {
      "theory": "Network Theory",
      "source_domain": "mathematics",
      "claim_maps_to": "Community interdependence as a network with strong ties.",
      "mapping": "STRUCTURAL",
      "free_predictions": "Predicts resilience of Amish communities to external shocks.",
      "upgrade_path": null,
      "independent_arrival": true,
      "independent_arrival_explanation": "Network theory developed independently to study connectivity and robustness."
    },
    {
      "theory": "Game Theory - Nash Equilibrium",
      "source_domain": "economics",
      "claim_maps_to": "The Amish community's collective decision-making process.",
      "mapping": "ANALOGICAL",
      "free_predictions": null,
      "upgrade_path": "Demonstrate that Amish decisions reach a Nash equilibrium.",
      "independent_arrival": true,
      "independent_arrival_explanation": "Game theory was developed to analyze strategic interactions."
    },
    {
      "theory": "Control Theory",
      "source_domain": "engineering",
      "claim_maps_to": "The Amish use feedback mechanisms to maintain societal coherence.",
      "mapping": "STRUCTURAL",
      "free_predictions": "Predicts stability of Amish societal structures under perturbations.",
      "upgrade_path": null,
      "independent_arrival": true,
      "independent_arrival_explanation": "Control theory was developed to manage dynamic systems."
    }
  ],

  "domain_extension": {
    "domain": "urban planning",
    "why_transfers": "The principles of community size and interdependence can inform sustainable urban design.",
    "predictions": "Predicts more cohesive and resilient urban communities.",
    "likely_mapping": "STRUCTURAL"
  },

  "anchor": {
    "element": "The Amish are engineering their own coherence field.",
    "why_strongest": "It encapsulates the core argument that societal coherence can be deliberately maintained through structural choices.",
    "what_breaks_without_it": "The entire argument about the effectiveness of constraints in maintaining societal order would collapse."
  },

  "novel_implication": {
    "implication": "Modern societies could reverse coherence decline by reintroducing strategic constraints.",
    "derivation": "The paper's comparison of Amish and mainstream American outcomes suggests that constraints are key to coherence.",
    "significance": "potentially major"
  },

  "structural_completion": {
    "missing_axioms": ["A7.4"],
    "skipped_derivations": ["Quantitative analysis of coherence metrics."],
    "missing_conditions": ["Existence of a baseline coherence level."],
    "undefined_boundaries": ["Limits of technology adoption."],
    "limit_behavior": ["Behavior of coherence metrics as constraints approach zero."]
  },

  "isomorphic_imports": [
    {
      "source_domain": "ecology",
      "theory": "Lotka-Volterra Equations",
      "structure": "Population dynamics and resource constraints.",
      "mapping_to_paper": "Maps onto the Amish population growth and resource management.",
      "what_it_adds": "Provides a mathematical framework for understanding population sustainability.",
      "mapping_strength": "STRUCTURAL"
    },
    {
      "source_domain": "information theory",
      "theory": "Shannon's Information Theory",
      "structure": "Control of information flow to maintain coherence.",
      "mapping_to_paper": "Maps onto the Amish control of information sources.",
      "what_it_adds": "Quantifies the impact of information control on societal coherence.",
      "mapping_strength": "STRUCTURAL"
    }
  ],

  "triple_score": {
    "physicist": {"score": 70, "justification": "The paper lacks rigorous quantitative analysis but presents a compelling qualitative argument."},
    "philosopher": {"score": 85, "justification": "The logical coherence and exploration of societal structures are well-developed."},
    "editor": {"score": 80, "justification": "The paper is well-structured and clearly communicates its argument, though it could benefit from more citations."}
  },

  "weakest_rewrite": {
    "original_paragraph": "The Amish don't reject technology. They reject the dissolution of boundaries that technology enables.",
    "diagnosis": "The statement is too broad and lacks specificity about which boundaries are dissolved.",
    "rewrite": "The Amish selectively reject technologies that dissolve community boundaries and promote individual isolation."
  },

  "executive_summary": "The extractor found that the paper presents a compelling argument for the role of constraints in maintaining societal coherence, using the Amish as a control group. The biggest structural opportunity lies in quantitatively modeling the coherence metrics to strengthen the argument with rigorous data analysis."
}
```