#!/usr/bin/env python3
"""Generate index.html templates for Parts IX-XVIII of the Theophysics framework."""
import os
import re

# Series data: part number, directory, title, description, accent color, accent name, articles
SERIES = [
    {
        "part": "IX",
        "dir": "cross-domain",
        "title": "The Applied Framework",
        "subtitle": "Cross-Domain Applications",
        "desc": "The Master Equation applied to real systems — American coherence collapse, fruits of the spirit, constitutional audit, cliodynamic analysis, and reverse sequence hypothesis.",
        "color": "#3b82f6",
        "color_name": "blue",
        "articles": [
            ("cd-01-an-introduction-to-theophysics.html", "CD-01", "An Introduction to Theophysics", "The foundation. What coherence means across every domain and why it matters."),
            ("cd-02-the-coherence-metric.html", "CD-02", "The Coherence Metric", "Measuring alignment between observer and source. A practical tool for assessment."),
            ("cd-03-the-only-top-down-framework.html", "CD-03", "The Only Top-Down Framework", "Why bottom-up emergence fails and top-down information primacy succeeds."),
            ("cd-04-the-american-coherence-collapse.html", "CD-04", "The American Coherence Collapse", "Measuring the decline. What the coherence metric reveals about national trajectory."),
            ("cd-05-fruits-of-the-spirit.html", "CD-05", "Fruits of the Spirit", "Love, joy, peace, patience — mapped to the equation as coherence attractors."),
            ("cd-06-the-scientific-method-redux.html", "CD-06", "The Scientific Method Redux", "What science actually measures when it stops pretending to be neutral."),
            ("cd-07-master-coherence-analysis.html", "CD-07", "Master Coherence Analysis", "The full analytical framework. Every variable, every domain, one assessment."),
            ("cd-08-the-thermodynamics-of-grace.html", "CD-08", "The Thermodynamics of Grace", "Grace as negentropic input. Why closed systems decay and open systems restore."),
            ("cd-09-church-debris-audit.html", "CD-09", "Church Debris Audit", "Measuring institutional coherence. What the numbers say about the American church."),
            ("cd-10-cliodynamic-analysis-great-demoralization.html", "CD-10", "Cliodynamic Analysis: The Great Demoralization", "Peter Turchin's structural-demographic theory meets the coherence metric."),
            ("cd-11-constitutional-overlay-analysis.html", "CD-11", "Constitutional Overlay Analysis", "The founding documents as coherence architecture. Where we deviated and why."),
            ("cd-12-reverse-sequence-hypothesis.html", "CD-12", "Reverse Sequence Hypothesis", "What happens when you run the equation backward. Prophecy as retrocausal coherence."),
        ]
    },
    {
        "part": "X",
        "dir": "bible-through-equation",
        "title": "The Bible Through the Equation",
        "subtitle": "Biblical Studies",
        "desc": "Scripture passages mapped to the Master Equation variables. Every letter in &chi; = f(G, M, E, S, T, K, R, Q, F, C) finds its biblical anchor.",
        "color": "#d4af37",
        "color_name": "gold",
        "articles": [
            ("be-01-grace-in-genesis.html", "BE-01", "Grace in Genesis", "G &mdash; From Eden to the Cross. The grace variable threaded through the entire biblical narrative."),
            ("be-02-meaning-in-exodus.html", "BE-02", "Meaning in Exodus", "M &mdash; The name revealed. Why 'I AM WHO I AM' is the ontological foundation of meaning."),
            ("be-03-truth-in-deuteronomy.html", "BE-03", "Truth in Deuteronomy", "E &mdash; Emet. The Hebrew concept of truth as structural reliability, not mere correspondence."),
            ("be-04-entropy-in-romans.html", "BE-04", "Entropy in Romans", "S &mdash; Sin as decoherence. Paul's theology of entropy and the need for external negentropic input."),
            ("be-05-logos-in-john.html", "BE-05", "Logos in John", "T &mdash; In the beginning was the Word. The information-theoretic reading of John's prologue."),
            ("be-06-love-in-corinthians.html", "BE-06", "Love in Corinthians", "K &mdash; Agape as coherence transfer. The greatest of these is love because love is the binding field."),
            ("be-07-relationship-in-john.html", "BE-07", "Relationship in John", "R &mdash; Abide in me. The relational architecture of the Trinity as the ground of being."),
            ("be-08-faith-in-hebrews.html", "BE-08", "Faith in Hebrews", "Q &mdash; The substance of things hoped for. Faith as coherence projection into unmeasured states."),
            ("be-09-sin-in-romans.html", "BE-09", "Sin in Romans", "F &mdash; The Pharisee Function. Self-righteousness as a coherence collapse mechanism."),
            ("be-10-coherence-in-revelation.html", "BE-10", "Coherence in Revelation", "C &mdash; The marriage supper of the Lamb. Heaven as the global coherence maximum."),
        ]
    },
    {
        "part": "XI",
        "dir": "spiritual-warfare",
        "title": "The Adversary's Playbook",
        "subtitle": "Spiritual Warfare",
        "desc": "The adversary's mathematical identity. The Pharisee Function, the Silence Function, attack surfaces, and the Hamiltonian of spiritual conflict.",
        "color": "#c94040",
        "color_name": "red",
        "articles": [
            ("sw-000-quantum-warfare-moc.html", "SW-000", "Quantum Warfare MOC", "Map of contents. The full spiritual warfare framework in one navigable page."),
            ("sw-the-attack-surface.html", "SW-01", "The Attack Surface", "Seven domains of vulnerability. Where the adversary strikes and why."),
            ("sw-character-of-adversary-from-physics.html", "SW-02", "The Character of the Adversary", "12 properties from 7 domains of physics. What entropy and decay reveal."),
            ("sw-adversary.html", "SW-03", "The Adversary: Full Profile", "The mathematical identity of the adversary. Not mythology — taxonomy."),
            ("sw-profile-rebel-satan.html", "SW-04", "Profile: Rebel Satan", "The coherence collapse narrative. From archangel to adversary — what changed."),
            ("sw-warfare-hamiltonian-canonical.html", "SW-05", "The Warfare Hamiltonian", "The canonical form. Spiritual warfare as field dynamics, not metaphor."),
            ("sw-the-spiritual-warfare-field-dynamics-visualizer.html", "SW-06", "Field Dynamics Visualizer", "Interactive. See the warfare field in action. Toggle domains, trace attack vectors."),
        ]
    },
    {
        "part": "XII",
        "dir": "consciousness",
        "title": "The Consciousness Problem",
        "subtitle": "Consciousness &amp; the &chi;-Field",
        "desc": "Why consciousness doesn't collapse the wavefunction. What it actually does. The hard problem solved through information primacy and the &chi;-field action.",
        "color": "#14b8a6",
        "color_name": "teal",
        "articles": [
            ("con-constraint-argument.html", "CON-01", "The Constraint Argument", "357 theories. All hit the same wall. Relational descriptions cannot generate intrinsic experience."),
            ("con-chi-field-action.html", "CON-02", "The Minimal &chi;-Field Action", "The full Lagrangian. Massive at the Hubble scale, self-interacting, non-minimally coupled. Ghost-free."),
            ("con-ontological-taxonomy.html", "CON-03", "Ontological Taxonomy", "What exists, what doesn't, and why consciousness is in a category of its own."),
            ("con-reality-assessment.html", "CON-04", "Reality Assessment", "The measurement problem reconsidered. Consciousness as participant, not collapsor."),
            ("con-coherence-bridge.html", "CON-05", "The Coherence Bridge", "How consciousness mediates between source field and physical instantiation."),
            ("con-free-will-evil.html", "CON-06", "Free Will &amp; Evil", "Why genuine choice requires the possibility of decoherence. The moral necessity of entropy."),
            ("con-grace-source-term.html", "CON-07", "Grace as Source Term", "The external negentropic input. Why consciousness alone cannot save itself."),
            ("con-parallel-laws.html", "CON-08", "Parallel Laws", "Physical law and moral law as isomorphic structures. Two expressions, one substrate."),
            ("con-scientific-convergence.html", "CON-09", "Scientific Convergence", "Where the &chi;-field meets experimental physics. Testable predictions."),
            ("con-evidence-predictions.html", "CON-10", "Evidence &amp; Predictions", "What to look for. How to falsify. The predictions that distinguish this framework."),
        ]
    },
    {
        "part": "XIII",
        "dir": "prophetic-synthesis",
        "title": "The Prophecy Engine",
        "subtitle": "Prophetic Synthesis",
        "desc": "Biblical prophecy as forward-prediction from the Master Equation. The coherence cascade, retrocausal clocks, and the Enoch threshold.",
        "color": "#a855f7",
        "color_name": "purple",
        "articles": [
            ("ps-01-the-coherence-cascade.html", "PS-01", "The Coherence Cascade", "Prophecy as convergence. What happens when coherence propagates through history."),
            ("ps-02-maxwell-of-the-soul.html", "PS-02", "Maxwell of the Soul", "The electromagnetic analogy. Prophecy as field propagation, not magic."),
            ("ps-03-the-retrocausal-clock.html", "PS-03", "The Retrocausal Clock", "Time symmetry and divine foreknowledge. Why prophecy isn't prediction — it's structure."),
            ("ps-04-the-theta-protocol.html", "PS-04", "The Theta Protocol", "The threshold state. What theta brainwaves and prophetic trance have in common."),
            ("ps-05-the-moral-lagrangian.html", "PS-05", "The Moral Lagrangian", "History as optimization. The path of least action through moral space."),
            ("ps-06-the-enoch-threshold.html", "PS-06", "The Enoch Threshold", "Walked with God and was not. The coherence threshold for translation."),
            ("ps-07-the-closure-protocol.html", "PS-07", "The Closure Protocol", "How prophecy ends. The final convergence and the new creation attractor."),
        ]
    },
    {
        "part": "XIV",
        "dir": "duality-project",
        "title": "The Duality Project",
        "subtitle": "Two-Substrate Simulation",
        "desc": "The two-substrate model. Why reality has two incompatible physics — wave and particle, spirit and matter, the seen and the unseen.",
        "color": "#d4af37",
        "color_name": "gold",
        "articles": [
            ("dp-00-the-null-hypothesis.html", "DP-00", "The Null Hypothesis", "What if nothing supernatural exists? The baseline against which the duality model is tested."),
            ("dp-000-the-assignment.html", "DP-000", "The Assignment", "The simulation premise. Two substrates, one observer, one equation."),
            ("dp-01-candle-in-the-void.html", "DP-01", "Candle in the Void", "Genesis 1:3 as information injection. Let there be light — the first distinguishability event."),
            ("dp-02-the-blinding-mirror.html", "DP-02", "The Blinding Mirror", "The Fall as decoherence. What changed when the observer chose measurement over communion."),
            ("dp-03-the-gray-stagnation.html", "DP-03", "The Gray Stagnation", "Babel. The coherence plateau. When information disperses without convergence."),
            ("dp-04-the-birth-of-a-devil.html", "DP-04", "The Birth of a Devil", "The adversary's origin story. Coherence collapse as ontological event."),
            ("dp-05-the-generational-rust.html", "DP-05", "The Generational Rust", "Entropy across generations. Why each generation starts farther from source."),
            ("dp-06-the-chorus-appears.html", "DP-06", "The Chorus Appears", "The prophets. Information channels reopening. Coherence signals in noise."),
            ("dp-07-the-incarnation-protocol.html", "DP-07", "The Incarnation Protocol", "The Word became flesh. The source field entering its own simulation."),
            ("dp-08-the-atonement-paradox.html", "DP-08", "The Atonement Paradox", "How infinite coherence absorbs infinite decoherence. The Cross as field equation."),
            ("dp-09-the-prototype-resurrection.html", "DP-09", "The Prototype Resurrection", "First fruits. The coherence reversal that breaks entropy's seal."),
            ("dp-10-the-ascension-update.html", "DP-10", "The Ascension Update", "The source field re-ascends. What changed in the simulation parameters."),
            ("dp-11-the-internal-info-war.html", "DP-11", "The Internal Info War", "The church age. Coherence propagation through a hostile substrate."),
            ("dp-12-collective-negentropy.html", "DP-12", "Collective Negentropy", "The body of Christ. Distributed coherence restoration."),
            ("dp-13-specialized-subroutines.html", "DP-13", "Specialized Subroutines", "Gifts of the Spirit. Each as a coherence transfer function."),
            ("dp-14-evangelism-wave.html", "DP-14", "The Evangelism Wave", "The great commission. Coherence propagation as mission."),
            ("dp-15-persecution-feedback-loop.html", "DP-15", "Persecution Feedback Loop", "Why the church grows under pressure. Coherence amplification through resistance."),
            ("dp-16-apostasy-bug.html", "DP-16", "The Apostasy Bug", "The great falling away. Coherence loss as systemic failure."),
            ("dp-17-angelic-backstory.html", "DP-17", "Angelic Backstory", "The unseen substrate. What the simulation reveals about non-physical agents."),
            ("dp-18-prayer-quantum-chat.html", "DP-18", "Prayer: Quantum Chat", "Communication across substrates. Prayer as information transfer."),
            ("dp-19-entropys-last-stand.html", "DP-19", "Entropy's Last Stand", "The tribulation. Maximum decoherence event before phase transition."),
            ("dp-20-resonant-reboot.html", "DP-20", "Resonant Reboot", "The millennium. Coherence restoration at scale."),
            ("dp-21-second-death-audit.html", "DP-21", "Second Death Audit", "The final separation. Irreversible decoherence and the attractor state."),
            ("dp-22-grade-day.html", "DP-22", "Grade Day", "The judgment seat. Coherence assessment. What survives the fire."),
        ]
    },
    {
        "part": "XV",
        "dir": "apologetics-debate",
        "title": "The Apologetics Arsenal",
        "subtitle": "Debate Framework &amp; Practice",
        "desc": "TikTok-ready debate framework. Twenty Moves, Three Gates in practice, and the self-refutation matrix. Every objection, one response.",
        "color": "#3b82f6",
        "color_name": "blue",
        "articles": [
            ("../three-gates/the-three-gates.html", "TG-01", "The Three Gates", "The prerequisite framework. Three self-refuting prerequisites that lock your opponent into shared ground.", True),
            ("aa-01-twenty-moves.html", "AA-01", "Twenty Moves", "The complete matrix. Every atheist argument and its exact rebuttal from the framework.", False),
            ("aa-02-the-self-refutation-matrix.html", "AA-02", "The Self-Refutation Matrix", "Why relativism, scientism, and moral subjectivism all collapse on their own terms.", False),
            ("aa-03-tiktok-apologetics.html", "AA-03", "TikTok Apologetics", "60-second responses. The framework compressed for short-form debate.", False),
            ("aa-04-the-presuppositional-bridge.html", "AA-04", "The Presuppositional Bridge", "Connecting Van Til to physics. Why presuppositionalism was right but incomplete.", False),
            ("aa-05-evidential-coherence.html", "AA-05", "Evidential Coherence", "The evidentialist case restated. Why evidence alone is insufficient but necessary.", False),
        ]
    },
    {
        "part": "XVI",
        "dir": "one-page-stories",
        "title": "The God Stories",
        "subtitle": "One-Page Narratives",
        "desc": "Each law of the framework told as narrative. Accessible, shareable, one page each. The physics of God as story.",
        "color": "#d4af37",
        "color_name": "gold",
        "articles": [
            ("character-of-god-from-physics.html", "GS-01", "The Character of God &mdash; Read from Physics", "24 measured properties from 10 physical forces. Together they compose one Person."),
            ("character-of-adversary-from-physics.html", "GS-02", "The Character of the Adversary", "7 domains of physics. 12 properties. What entropy and decay reveal."),
            ("salvation-algorithm.html", "GS-03", "The Salvation Algorithm", "Six steps of pure logic. No religious language. The Gospel derived from first principles."),
            ("why-grace-from-outside.html", "GS-04", "Why Grace Has to Come from Outside", "The Second Law forbids self-salvation. A closed system cannot reverse its own entropy."),
            ("heaven-hell-attractor-states.html", "GS-05", "Heaven and Hell as Attractor States", "They are not where you go. They are where you've been going. Dynamical systems, basins of attraction."),
            ("the-father-as-source-field.html", "GS-06", "The Father as Source Field", "The Trinity in physical terms. The Father as the ungenerated generator."),
            ("trinity-grace.html", "GS-07", "Trinity &amp; Grace", "Three persons, one substance. The mathematical necessity of triune structure."),
            ("the-prism-paper.html", "GS-08", "The Prism Paper", "White light through a prism. One truth refracted through many domains."),
            ("the-floor-beneath-the-floor.html", "GS-09", "The Floor Beneath the Floor", "Turtles all the way down — until you hit the self-grounding substrate."),
            ("genesis-quantum-event.html", "GS-10", "The Genesis-Quantum Event", "The moment measurement created reality. Genesis 1 as quantum mechanical narrative."),
            ("it-from-bit-from-logos.html", "GS-11", "It from Bit from Logos", "Wheeler's it-from-bit, elevated. Information is not merely fundamental — it is personal."),
            ("the-same-equation.html", "GS-12", "The Same Equation", "One equation, every domain. The unification that physics has been searching for."),
            ("we-ran-the-tests.html", "GS-13", "We Ran the Tests", "The experimental record. What happened when the predictions were checked against reality."),
            ("everybodys-got-it-wrong.html", "GS-14", "Everybody's Got It Wrong", "The consensus problem. Why the majority opinion is often the decoherent one."),
            ("holding-god-accountable.html", "GS-15", "Holding God Accountable", "The moral argument reversed. If God exists, He must be good — and the equation confirms it."),
            ("the-24-anti-properties.html", "GS-16", "The 24 Anti-Properties", "The adversary's signature. Every virtue has its inverse — and physics measures both."),
            ("no-drift-law-synthesis.html", "GS-17", "No-Drift Law Synthesis", "Information doesn't drift upward. The Second Law and the necessity of external input."),
            ("salvation-phase-transition.html", "GS-18", "Salvation as Phase Transition", "Born again — not metaphorically, but as a change of state. The physics of regeneration."),
            ("salvation-narrative-10-laws.html", "GS-19", "Salvation Narrative: 10 Laws", "The complete legal framework. Ten laws, one narrative, one rescue."),
            ("theophysics-blackboard_1.html", "GS-20", "Theophysics Blackboard", "The chalkboard version. Everything on one board, one glance, one understanding."),
            ("theophysics-the-full-explanation.html", "GS-21", "Theophysics: The Full Explanation", "The comprehensive treatment. For readers who want the complete argument in one sitting."),
            ("The_Logos_Thesis_v3.html", "GS-22", "The Logos Thesis", "The foundational document. Information is personal, and that person is Christ."),
            ("Formalism.html", "GS-23", "Formalism", "The mathematical notation. For readers who speak Lagrangian."),
        ]
    },
    {
        "part": "XVII",
        "dir": "bible-datalab",
        "title": "The Data Lab",
        "subtitle": "Bible DataLab &amp; Analytics",
        "desc": "PostgreSQL-driven biblical analysis. The silence study, pharisee anomalies, grace vectors, and sin vectors — all queryable, all visualized.",
        "color": "#a855f7",
        "color_name": "purple",
        "articles": [
            ("the-sin-vector.html", "BDL-01", "The Sin Vector", "Quantified transgression. Direction, magnitude, and cumulative effect across text."),
            ("the-grace-vector.html", "BDL-02", "The Grace Vector", "Quantified restoration. The negentropic counter to sin's decoherence."),
            ("the-grace.html", "BDL-03", "The Grace Function", "Mathematical model of unmerited favor. How grace operates as source term."),
            ("the-adversary.html", "BDL-04", "The Adversary Profile", "Statistical signature of the adversary across biblical narrative."),
            ("the-adversary-v2.html", "BDL-05", "The Adversary Profile v2", "Updated analysis. Refined metrics, expanded corpus, tighter confidence intervals."),
            ("god_story_v2.html", "BDL-06", "The God Story v2", "Narrative coherence analysis. The divine character as statistical constant across 66 books."),
            ("GTQ-01_wavefunction_collapse_3d.html", "BDL-07", "Wavefunction Collapse 3D Viz", "Interactive visualization. Measurement events in Genesis as quantum state transitions."),
            ("GTQ-07_grace_function_3d.html", "BDL-08", "Grace Function 3D Viz", "Interactive. The grace field in three dimensions. See the source term operate."),
        ]
    },
    {
        "part": "XVIII",
        "dir": "living-document",
        "title": "The Living Document",
        "subtitle": "Active Research &amp; Open Questions",
        "desc": "The framework continues. Open questions, active research threads, experimental proposals, and what's next for Theophysics.",
        "color": "#14b8a6",
        "color_name": "teal",
        "articles": [
            ("ld-01-open-questions.html", "LD-01", "Open Questions", "What we don't know yet. The frontier questions that keep the research alive.", False),
            ("ld-02-experimental-proposals.html", "LD-02", "Experimental Proposals", "Testable hypotheses. How to confirm or falsify key claims.", False),
            ("ld-03-collaboration-framework.html", "LD-03", "Collaboration Framework", "How to contribute. Peer review, replication studies, and community standards.", False),
            ("ld-04-version-history.html", "LD-04", "Version History", "How the framework has evolved. Major revisions and what triggered them.", False),
            ("ld-05-reading-roadmap.html", "LD-05", "Reading Roadmap", "Where to go next. Depending on your background — physics, theology, philosophy, or none.", False),
        ]
    },
]

# Full arc navigation for sidebar
ARC_NAV = """<div class="progress-track"><div class="progress-fill" id="progressBar"></div></div>
<button class="sidebar-toggle" onclick="toggleSidebar()" aria-label="Open navigation">&#9776;</button>
<div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>
<aside class="sidebar" id="sidebar">
  <div style="padding:1.5rem;border-bottom:1px solid var(--border);">
    <div style="font-family:var(--display);font-size:.7rem;letter-spacing:.15em;text-transform:uppercase;color:var(--accent);margin-bottom:.25rem;">Theophysics</div>
    <div style="font-size:.75rem;color:var(--text-muted);">The Complete Arc</div>
  </div>
  <nav style="padding:1rem 0;">
    <a href="../index.html" style="display:block;padding:.5rem 1.5rem;font-size:.8rem;color:var(--text-dim);text-decoration:none;"><i class="fas fa-home" style="width:1.2rem;"></i> Home</a>
    <div style="padding:.5rem 1.5rem .25rem;font-family:var(--display);font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);">Core Journey</div>
    <a href="../moral-decline/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--red);">I.</span> Moral Decline</a>
    <a href="../three-gates/the-three-gates.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--blue);">II.</span> Three Gates</a>
    <a href="../logos-papers/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--gold);">III.</span> Logos Papers</a>
    <a href="../formal-papers/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--purple);">IV.</span> Formal Papers</a>
    <a href="../genesis-to-quantum/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--red);">V.</span> Genesis to Quantum</a>
    <a href="../Convergence_Series/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--gold);">VI.</span> Convergence</a>
    <a href="../master-equation/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--purple);">VII.</span> Master Equation</a>
    <a href="../proof-architecture/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--teal);">VIII.</span> Proof Architecture</a>
    <div style="padding:.5rem 1.5rem .25rem;font-family:var(--display);font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);">Supporting Research</div>
    <a href="../cross-domain/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--blue);">IX.</span> Applied Framework</a>
    <a href="../bible-through-equation/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--gold);">X.</span> Bible Through Equation</a>
    <a href="../spiritual-warfare/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--red);">XI.</span> Adversary's Playbook</a>
    <a href="../consciousness/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--teal);">XII.</span> Consciousness Problem</a>
    <a href="../prophetic-synthesis/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--purple);">XIII.</span> Prophecy Engine</a>
    <a href="../duality-project/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--gold);">XIV.</span> Duality Project</a>
    <a href="../apologetics-debate/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--blue);">XV.</span> Apologetics Arsenal</a>
    <a href="../one-page-stories/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--gold);">XVI.</span> God Stories</a>
    <a href="../bible-datalab/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--purple);">XVII.</span> Data Lab</a>
    <a href="../living-document/index.html" style="display:block;padding:.4rem 1.5rem .4rem 2.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;"><span style="color:var(--teal);">XVIII.</span> Living Document</a>
  </nav>
</aside>"""

def generate_index(series):
    part = series["part"]
    dirname = series["dir"]
    title = series["title"]
    subtitle = series["subtitle"]
    desc = series["desc"]
    color = series["color"]
    color_name = series["color_name"]
    articles = series["articles"]
    
    # Build article cards
    cards_html = []
    for article in articles:
        if len(article) == 4:
            href, num, name, description = article
            external = False
        else:
            href, num, name, description, external = article
        
        coming_soon = not href.startswith("..") and not os.path.exists(os.path.join(dirname, href))
        opacity = ' style="opacity:.4;"' if coming_soon else ''
        href_attr = f'href="{href}"' if not coming_soon else ''
        tag = 'a' if not coming_soon else 'div'
        end_tag = 'a' if not coming_soon else 'div'
        
        cards_html.append(f'''    <{tag} {href_attr} class="card {color_name}"{opacity}>
      <div class="card-num">{num}</div>
      <h3>{name}</h3>
      <div class="card-desc">{description}</div>
    </{end_tag}>''')
    
    cards = '\n'.join(cards_html)
    
    # Current class for sidebar highlight
    current_script = f"""<script>
document.addEventListener('DOMContentLoaded', function() {{
  const links = document.querySelectorAll('.sidebar a');
  links.forEach(function(link) {{
    if(link.getAttribute('href') && link.getAttribute('href').includes('{dirname}/')) {{
      link.classList.add('current');
    }}
  }});
}});
</script>"""
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Part {part} — {title} | Theophysics</title>
<meta name="description" content="{desc.replace('&mdash;', '—').replace('&chi;', 'chi').replace('&amp;', 'and')}"/>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600;700&family=Oswald:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>
<style>
:root{{
  --bg:#050505;
  --surface:#0a0a0a;
  --surface2:#111;
  --surface3:#1a1a1a;
  --border:#222;
  --border-hover:#333;
  --text:#e0e0e0;
  --text-dim:#999;
  --text-muted:#555;
  --accent:{color};
  --accent-dim:{color}18;
  --red:#c94040;
  --blue:#3b82f6;
  --gold:#d4af37;
  --teal:#14b8a6;
  --purple:#a855f7;
}}
*{{box-sizing:border-box;margin:0;padding:0;}}
html{{scroll-behavior:smooth;}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);line-height:1.6;overflow-x:hidden;}}
a{{color:inherit;text-decoration:none;}}

/* Progress bar */
.progress-track{{position:fixed;top:0;left:0;right:0;height:3px;background:var(--border);z-index:1001;}}
.progress-fill{{height:100%;width:0%;background:linear-gradient(90deg,var(--accent),{color}aa);transition:width 0.1s ease;}}

/* Sidebar */
.sidebar{{position:fixed;top:0;left:0;width:300px;height:100vh;background:var(--surface);border-right:1px solid var(--border);z-index:1000;overflow-y:auto;transform:translateX(-100%);transition:transform .3s ease;}}
.sidebar.open{{transform:translateX(0);}}
.sidebar a{{display:block;padding:.4rem 1.5rem;font-size:.75rem;color:var(--text-dim);text-decoration:none;transition:all .2s;}}
.sidebar a:hover{{color:var(--text);background:var(--surface2);}}
.sidebar a.current{{color:var(--accent);background:var(--accent-dim);font-weight:600;}}
.sidebar-overlay{{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:999;opacity:0;pointer-events:none;transition:opacity .3s;}}
.sidebar-overlay.show{{opacity:1;pointer-events:auto;}}
.sidebar-toggle{{position:fixed;top:1rem;left:1rem;z-index:1002;background:var(--surface2);border:1px solid var(--border);color:var(--accent);width:40px;height:40px;border-radius:.375rem;cursor:pointer;font-size:1.1rem;display:flex;align-items:center;justify-content:center;}}

/* Hero */
.hero{{min-height:45vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:4rem 2rem 2rem;position:relative;overflow:hidden;}}
.hero::before{{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:600px;height:600px;background:radial-gradient(circle,{color}0a 0%,transparent 70%);pointer-events:none;}}
.hero-tag{{font-family:'Oswald',sans-serif;font-size:.65rem;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);margin-bottom:1rem;}}
.hero h1{{font-family:'Crimson Text',serif;font-size:clamp(2rem,5vw,3.2rem);color:white;font-weight:400;margin-bottom:.5rem;}}
.hero .subtitle{{font-size:.9rem;color:var(--text-dim);max-width:550px;margin:0 auto 1.5rem;}}
.hero .part-num{{font-family:'JetBrains Mono',monospace;font-size:.75rem;color:var(--accent);letter-spacing:.1em;margin-bottom:.5rem;}}

/* Back nav */
.back-nav{{max-width:1000px;margin:0 auto;padding:1.5rem 2rem 0;}}
.back-nav a{{font-family:'JetBrains Mono',monospace;font-size:.75rem;color:var(--text-muted);text-decoration:none;letter-spacing:.05em;transition:color .2s;}}
.back-nav a:hover{{color:var(--accent);}}
.back-nav a i{{margin-right:.4rem;}}

/* Section */
.section{{max-width:1000px;margin:0 auto;padding:3rem 2rem;}}
.section-header{{display:flex;align-items:center;gap:.75rem;margin-bottom:.5rem;}}
.section-dot{{width:10px;height:10px;border-radius:50%;flex-shrink:0;background:var(--accent);}}
.section-header h2{{font-family:'Crimson Text',serif;font-size:1.5rem;color:white;}}
.section-count{{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:var(--text-muted);margin-left:auto;}}
.section-desc{{font-size:.85rem;color:var(--text-dim);margin-bottom:2rem;max-width:650px;}}

/* Cards */
.card-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem;}}
.card{{background:var(--surface2);border:1px solid var(--border);border-radius:.6rem;padding:1.25rem;color:var(--text);transition:all .25s ease;display:flex;flex-direction:column;position:relative;overflow:hidden;}}
.card:hover{{border-color:var(--accent);background:{color}08;transform:translateY(-2px);box-shadow:0 8px 32px rgba(0,0,0,.4);}}
.card .card-num{{font-family:'Oswald',sans-serif;font-size:.6rem;letter-spacing:.15em;text-transform:uppercase;margin-bottom:.5rem;color:var(--accent);}}
.card h3{{font-family:'Crimson Text',serif;font-size:1.1rem;color:white;margin-bottom:.4rem;line-height:1.3;}}
.card .card-desc{{font-size:.8rem;color:var(--text-dim);line-height:1.5;flex:1;}}

/* Divider */
.divider{{max-width:1000px;margin:0 auto;border:none;border-top:1px solid var(--border);}}

/* Footer */
footer{{text-align:center;padding:3rem 2rem;color:var(--text-muted);font-size:.8rem;}}
footer .eq{{font-family:'JetBrains Mono',monospace;font-size:.75rem;color:var(--gold);opacity:.5;margin-bottom:.5rem;}}

@media(max-width:640px){{.card-grid{{grid-template-columns:1fr;}}.hero{{min-height:35vh;padding:3rem 1.5rem 1.5rem;}}}}
</style>
</head>
<body>

<!-- Progress Bar -->
<div class="progress-track"><div class="progress-fill" id="progressBar"></div></div>

<!-- Sidebar Toggle -->
<button class="sidebar-toggle" onclick="toggleSidebar()" aria-label="Open navigation">&#9776;</button>

<!-- Sidebar Overlay -->
<div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>

<!-- Sidebar Navigation -->
<aside class="sidebar" id="sidebar">
  <div style="padding:1.5rem;border-bottom:1px solid var(--border);">
    <div style="font-family:'Oswald',sans-serif;font-size:.7rem;letter-spacing:.15em;text-transform:uppercase;color:var(--accent);margin-bottom:.25rem;">Theophysics</div>
    <div style="font-size:.75rem;color:var(--text-muted);">Part {part} — {title}</div>
  </div>
  <nav style="padding:1rem 0;">
    <a href="../index.html"><i class="fas fa-home" style="width:1.2rem;"></i> Home</a>
    <div style="padding:.5rem 1.5rem .25rem;font-family:'Oswald',sans-serif;font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);">Core Journey</div>
    <a href="../moral-decline/index.html"><span style="color:var(--red);">I.</span> Moral Decline</a>
    <a href="../three-gates/the-three-gates.html"><span style="color:var(--blue);">II.</span> Three Gates</a>
    <a href="../logos-papers/index.html"><span style="color:var(--gold);">III.</span> Logos Papers</a>
    <a href="../formal-papers/index.html"><span style="color:var(--purple);">IV.</span> Formal Papers</a>
    <a href="../genesis-to-quantum/index.html"><span style="color:var(--red);">V.</span> Genesis to Quantum</a>
    <a href="../Convergence_Series/index.html"><span style="color:var(--gold);">VI.</span> Convergence</a>
    <a href="../master-equation/index.html"><span style="color:var(--purple);">VII.</span> Master Equation</a>
    <a href="../proof-architecture/index.html"><span style="color:var(--teal);">VIII.</span> Proof Architecture</a>
    <div style="padding:.5rem 1.5rem .25rem;font-family:'Oswald',sans-serif;font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);">Supporting Research</div>
    <a href="../cross-domain/index.html"><span style="color:var(--blue);">IX.</span> Applied Framework</a>
    <a href="../bible-through-equation/index.html"><span style="color:var(--gold);">X.</span> Bible Through Equation</a>
    <a href="../spiritual-warfare/index.html"><span style="color:var(--red);">XI.</span> Adversary's Playbook</a>
    <a href="../consciousness/index.html"><span style="color:var(--teal);">XII.</span> Consciousness Problem</a>
    <a href="../prophetic-synthesis/index.html"><span style="color:var(--purple);">XIII.</span> Prophecy Engine</a>
    <a href="../duality-project/index.html"><span style="color:var(--gold);">XIV.</span> Duality Project</a>
    <a href="../apologetics-debate/index.html"><span style="color:var(--blue);">XV.</span> Apologetics Arsenal</a>
    <a href="../one-page-stories/index.html"><span style="color:var(--gold);">XVI.</span> God Stories</a>
    <a href="../bible-datalab/index.html"><span style="color:var(--purple);">XVII.</span> Data Lab</a>
    <a href="../living-document/index.html"><span style="color:var(--teal);">XVIII.</span> Living Document</a>
  </nav>
</aside>

<!-- Back Navigation -->
<div class="back-nav">
  <a href="../index.html"><i class="fas fa-arrow-left"></i> Back to Home</a>
</div>

<!-- Hero -->
<header class="hero">
  <div class="part-num">PART {part}</div>
  <div class="hero-tag">{subtitle}</div>
  <h1>{title}</h1>
  <p class="subtitle">{desc}</p>
</header>

<hr class="divider"/>

<!-- Articles Grid -->
<section class="section">
  <div class="section-header">
    <div class="section-dot"></div>
    <h2>Articles</h2>
    <span class="section-count">{len(articles)} items</span>
  </div>
  <p class="section-desc">The complete Part {part} series. Click any article to read.</p>
  <div class="card-grid">
{cards}
  </div>
</section>

<hr class="divider"/>

<!-- Footer -->
<footer>
  <div class="eq">&chi; = f(G, M, E, S, T, K, R, Q, F, C)</div>
  <p>David Lowe &middot; Part {part} — {title}</p>
  <p style="font-family:'Crimson Text',serif;font-style:italic;color:var(--text-muted);margin-top:.5rem;">&ldquo;But while he was still a long way off, his father saw him.&rdquo;</p>
</footer>

<!-- Scripts -->
<script>
function toggleSidebar() {{
  var sb = document.getElementById('sidebar');
  var ov = document.getElementById('sidebarOverlay');
  sb.classList.toggle('open');
  ov.classList.toggle('show');
  document.body.style.overflow = sb.classList.contains('open') ? 'hidden' : '';
}}
window.addEventListener('scroll', function() {{
  var st = window.scrollY || document.documentElement.scrollTop;
  var dh = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  var pct = dh > 0 ? (st / dh) * 100 : 0;
  document.getElementById('progressBar').style.width = pct + '%';
}});
document.addEventListener('keydown', function(e) {{
  if (e.key === 'Escape') {{
    var sb = document.getElementById('sidebar');
    if (sb && sb.classList.contains('open')) toggleSidebar();
  }}
}});
</script>
{current_script}

</body>
</html>'''
    
    return html


def main():
    base_path = "."
    
    for series in SERIES:
        dirname = series["dir"]
        filepath = os.path.join(base_path, dirname, "index.html")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.join(base_path, dirname), exist_ok=True)
        
        html = generate_index(series)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Generated: {filepath} ({len(html)} bytes)")
    
    print("\nAll 10 index templates generated successfully.")

if __name__ == "__main__":
    main()
