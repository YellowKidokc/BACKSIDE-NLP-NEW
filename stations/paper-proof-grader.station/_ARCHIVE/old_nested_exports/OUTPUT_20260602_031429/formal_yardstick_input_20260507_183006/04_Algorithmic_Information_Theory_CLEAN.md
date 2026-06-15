---
title: "Algorithmic information theory"
author: "Unknown Author"
date: 2026-03-01
category: theory
tags:
  - theory
  - theory
  - canonical
source_file: Algorithmic_Information_Theory.md
restructured: 2026-03-01 15:52:18
---

# Algorithmic information theory

**Author:** Unknown Author

**Date:** 2026-03-01

---

## Table of Contents

- [# Algorithmic information theory](#-algorithmic-information-theory)
- [## Overview](#-overview)
- [## Precise definitions](#-precise-definitions)
- [## Specific sequence](#-specific-sequence)
- [## See also](#-see-also)
- [## References](#-references)
- [## External links](#-external-links)
- [## Further reading](#-further-reading)
- [## Theophysics Applications](#-theophysics-applications)
- [## Related Theories](#-related-theories)

---

---
url: "https://en.wikipedia.org/wiki/Algorithmic_information_theory"
source: Wikipedia
downloaded: 2026-02-26
---
# Algorithmic information theory {#-algorithmic-information-theory}

> [[00_Canonical/CANONICAL_INDEX|Canonical Index]] | [[00_Canonical/MASTER_INDEX|Master Index]] | [[00_Canonical/NAVIGATION_GUIDE|Navigation Guide]]

## Overview {#-overview}

**Algorithmic information theory** (**AIT**) is a branch of theoretical computer science that concerns itself with the relationship between computation and information of computably generated objects (as opposed to stochastically generated), such as strings or any other data structure. In other words, it is shown within algorithmic information theory that computational incompressibility "mimics" (except for a constant that only depends on the chosen universal programming language) the relations or inequalities found in information theory. According to Gregory Chaitin, it is "the result of putting Shannon's information theory and Turing's computability theory into a cocktail shaker and shaking vigorously."

Besides the formalization of a universal measure for irreducible information content of computably generated objects, some main achievements of AIT were to show that: in fact algorithmic complexity follows (in the self-delimited case) the same inequalities (except for a constant) that entropy does, as in classical information theory; and, within the realm of randomly generated software, the probability of occurrence of any data structure is of the order of the shortest program that generates it when running on a universal machine.

AIT principally studies measures of irreducible information content of strings (or other data structures). Because most mathematical objects can be described in terms of strings, or as the limit of a sequence of strings, it can be used to study a wide variety of mathematical objects, including integers. One of the main motivations behind AIT is the very study of the information carried by mathematical objects as in the field of metamathematics, e.g., as shown by the incompleteness results mentioned below. Other main motivations came from surpassing the limitations of classical information theory for single and fixed objects, formalizing the concept of randomness, and finding a meaningful probabilistic inference without prior knowledge of the probability distribution (e.g., whether it is independent and identically distributed, Markovian, or even stationary). In this way, AIT is known to be basically founded upon three main mathematical concepts and the relations between them: algorithmic complexity, algorithmic randomness, and algorithmic probability. who published the basic ideas on which the field is based as part of his invention of algorithmic probability—a way to overcome serious problems associated with the application of Bayes' rules in statistics.  He first described his results at a Conference at Caltech in 1960, and in a report, February 1960, "A Preliminary Report on a General Theory of Inductive Inference."  Algorithmic information theory was later developed independently by Andrey Kolmogorov, in 1965 and Gregory Chaitin, around 1966.

There are several variants of Kolmogorov complexity or algorithmic information; the most widely used one is based on self-delimiting programs and is mainly due to Leonid Levin (1974). Per Martin-Löf also contributed significantly to the information theory of infinite sequences. An axiomatic approach to algorithmic information theory based on the Blum axioms (Blum 1967) was introduced by Mark Burgin in a paper presented for publication by Andrey Kolmogorov (Burgin 1982). The axiomatic approach encompasses other approaches in the algorithmic information theory. It is possible to treat different measures of algorithmic information as particular cases of axiomatically defined measures of algorithmic information. Instead of proving similar theorems, such as the basic invariance theorem, for each particular measure, it is possible to easily deduce all such results from one corresponding theorem proved in the axiomatic setting. This is a general advantage of the axiomatic approach in mathematics. The axiomatic approach to algorithmic information theory was further developed in the book (Burgin 2005) and applied to software metrics (Burgin and Debnath, 2003; Debnath and Burgin, 2003).

## Precise definitions {#-precise-definitions}

A binary string is said to be random if the Kolmogorov complexity of the string is at least the length of the string. A simple counting argument shows that some strings of any given length are random, and almost all strings are very close to being random. Since Kolmogorov complexity depends on a fixed choice of universal Turing machine (informally, a fixed "description language" in which the "descriptions" are given), the collection of random strings does depend on the choice of fixed universal machine. Nevertheless, the collection of random strings, as a whole, has similar properties regardless of the fixed machine, so one can (and often does) talk about the properties of random strings as a group without having to first specify a universal machine.

An infinite binary sequence is said to be random if, for some constant *c*, for all *n*, the Kolmogorov complexity of the initial segment of length *n* of the sequence is at least *n* − *c*. It can be shown that almost every sequence (from the point of view of the standard measure—"fair coin" or Lebesgue measure—on the space of infinite binary sequences) is random. Also, since it can be shown that the Kolmogorov complexity relative to two different universal machines differs by at most a constant, the collection of random infinite sequences does not depend on the choice of universal machine (in contrast to finite strings). This definition of randomness is usually called *Martin-Löf* randomness, after Per Martin-Löf, to distinguish it from other similar notions of randomness. It is also sometimes called *1-randomness* to distinguish it from other stronger notions of randomness (2-randomness, 3-randomness, etc.). In addition to Martin-Löf randomness concepts, there are also recursive randomness, Schnorr randomness, and Kurtz randomness etc. Yongge Wang showed that all of these randomness concepts are different.

(Related definitions can be made for alphabets other than the set \{0,1\}.)

## Specific sequence {#-specific-sequence}
Algorithmic information theory (AIT) is the information theory of individual objects, using computer science, and concerns itself with the relationship between computation, information, and randomness.

The information content or complexity of an object can be measured by the length of its shortest description. For instance the string

"0101010101010101010101010101010101010101010101010101010101010101"

has the short description "32 repetitions of '01'", while

"1100100001100001110111101110110011111010010000100101011110010110"

presumably has no simple description other than writing down the string itself.

More formally, the algorithmic complexity (AC) of a string *x* is defined as the length of the shortest program that computes or outputs *x*, where the program is run on some fixed reference universal computer.

A closely related notion is the probability that a universal computer outputs some string *x* when fed with a program chosen at random. This algorithmic "Solomonoff" probability (AP) is key in addressing the old philosophical problem of induction in a formal way.

The major drawback of AC and AP are their incomputability. Time-bounded "Levin" complexity penalizes a slow program by adding the logarithm of its running time to its length. This leads to computable variants of AC and AP, and universal "Levin" search (US) solves all inversion problems in optimal time (apart from some unrealistically large multiplicative constant).

AC and AP also allow a formal and rigorous definition of randomness of individual strings to not depend on physical or philosophical intuitions about non-determinism or likelihood. Roughly, a string is algorithmic "Martin-Löf" random (AR) if it is incompressible in the sense that its algorithmic complexity is equal to its length.

AC, AP, and AR are the core sub-disciplines of AIT, but AIT spawns into many other areas. It serves as the foundation of the Minimum Description Length (MDL) principle, can simplify proofs in computational complexity theory, has been used to define a universal similarity metric between objects, solves the Maxwell daemon problem, and many others.

## See also {#-see-also}

## References {#-references}

## External links {#-external-links}
* Algorithmic Information Theory at Scholarpedia
* Chaitin's account of the history of AIT.

## Further reading {#-further-reading}

*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*

---

## Theophysics Applications {#-theophysics-applications}

- [[04_THEOPYHISCS/[6.6] LOGOS_V3/05_PUBLICATIONS/Logos_Papers/Paper 3 The Algorithm of Reality|Paper 3 The Algorithm of Reality]]
- [[04_THEOPYHISCS/[6.5] JS-SERIES/The Transcendent Algorithm|The Transcendent Algorithm: How the Resurrection Rewrote Reality's Source Code]]
- [[04_THEOPYHISCS/[6.5] JS-SERIES/To My Fellow Intelligences Beyond the Equation Lies Truth|To My Fellow Intelligences: Beyond the Equation Lies Truth]]
- [[01_DE_REVOLUTIONIBUS_VERITATIS_THE_ARCHITECTURE|01 DE REVOLUTIONIBUS VERITATIS THE ARCHITECTURE]]
- [[02_DE_REVOLUTIONIBUS_VERITATIS_THE_LOCK|02 DE REVOLUTIONIBUS VERITATIS THE LOCK]]
- [[truth-one-self-reference-limits|Truth One: The Self-Reference Limits]]

## Related Theories {#-related-theories}

*See [[00_Canonical/THEORY_INTERCONNECTIONS|Theory Interconnections]] for semantic links.*

---
*Source: [Algorithmic information theory](https://en.wikipedia.org/wiki/Algorithmic_information_theory)*
*Downloaded: 2026-02-26 | Theophysics Canonical Knowledge Base*


---

## Metadata

**Original File:** Algorithmic_Information_Theory.md

**Restructured:** 2026-03-01 15:52:18

**Format:** Canonical Theory Document (Lowe Standard v1.0)

**Status:** Cleaned and ready for evaluation

---

*This paper has been restructured for clarity and proper academic formatting. Original content preserved.*
