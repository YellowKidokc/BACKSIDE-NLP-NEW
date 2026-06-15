---
title: "Kolmogorov complexity"
author: "Unknown Author"
date: 2026-03-01
category: theory
tags:
  - theory
  - theory
  - canonical
source_file: Kolmogorov_Complexity.md
restructured: 2026-03-01 15:52:17
---

# Kolmogorov complexity

**Author:** Unknown Author

**Date:** 2026-03-01

---

## Table of Contents

- [# Kolmogorov complexity](#-kolmogorov-complexity)
- [## Overview](#-overview)
- [## Definition](#-definition)
- [### Intuition](#-intuition)
- [### Plain Kolmogorov complexity *C*](#-plain-kolmogorov-complexity-c)
- [### Prefix-free Kolmogorov complexity *K*](#-prefix-free-kolmogorov-complexity-k)
- [## Minimum message length](#-minimum-message-length)
- [## Kolmogorov randomness](#-kolmogorov-randomness)
- [## Relation to entropy](#-relation-to-entropy)
- [## Halting problem](#-halting-problem)
- [## Universal probability](#-universal-probability)
- [## Conditional versions](#-conditional-versions)
- [## Time-bounded complexity](#-time-bounded-complexity)
- [## See also](#-see-also)
- [## Notes](#-notes)

---

---
url: "https://en.wikipedia.org/wiki/Kolmogorov_complexity"
source: Wikipedia
downloaded: 2026-02-26
---
# Kolmogorov complexity {#-kolmogorov-complexity}

> [[00_Canonical/CANONICAL_INDEX|Canonical Index]] | [[00_Canonical/MASTER_INDEX|Master Index]] | [[00_Canonical/NAVIGATION_GUIDE|Navigation Guide]]

## Overview {#-overview}

fractal. Simply storing the 24-bit color of each pixel in this image would require 23 million bytes, but a small computer program can reproduce these 23 MB using the definition of the Mandelbrot set, the corner coordinates of the image and the parameters of the color mapping. Thus, the Kolmogorov complexity of this image is much less than 23 MB in any pragmatic model of computation. PNG's general-purpose image compression only reduces it to 1.6 MB, smaller than the raw data but much larger than the Kolmogorov complexity.]]

In algorithmic information theory (a subfield of computer science and mathematics), the **Kolmogorov complexity** of an object, such as a piece of text, is the length of a shortest computer program (in a predetermined programming language) that produces the object as output. It is a measure of the computational resources needed to specify the object, and is also known as **algorithmic complexity**, **Solomonoff–Kolmogorov–Chaitin complexity**, **program-size complexity**, **descriptive complexity**, or **algorithmic entropy**. It is named after Andrey Kolmogorov, who first published on the subject in 1963 and is a generalization of classical information theory.

The notion of Kolmogorov complexity can be used to state and prove impossibility results akin to Cantor's diagonal argument, Gödel's incompleteness theorem, and Turing's halting problem.
In particular, no program *P* computing a lower bound for each text's Kolmogorov complexity can return a value essentially larger than *P*'s own length (see section ); hence no single program can compute the exact Kolmogorov complexity for infinitely many texts.

## Definition {#-definition}

### Intuition {#-intuition}
Consider the following two strings of 32 lowercase letters and digits:

The first string has a short English-language description, namely "write ab 16 times", which consists of **17** characters. The second one has no obvious simple description (using the same character set) other than writing down the string itself, i.e., "write 4c1j5b2p0cv4w1x8rx2y39umgw5q85s7" which has **38** characters. Hence the operation of writing the first string can be said to have "less complexity" than writing the second.

More formally, the complexity of a string is the length of the shortest possible description of the string in some fixed universal description language (the sensitivity of complexity relative to the choice of description language is discussed below). It can be shown that the Kolmogorov complexity of any string cannot be more than a few bytes larger than the length of the string itself. Strings like the *abab* example above, whose Kolmogorov complexity is small relative to the string's size, are not considered to be complex.

The Kolmogorov complexity can be defined for any mathematical object, but for simplicity the scope of this article is restricted to strings. We must first specify a description language for strings.  Such a description language can be based on any computer programming language, such as Lisp, Pascal, or Java.  If **P** is a program which outputs a string *x*, then **P** is a description of *x*. The length of the description is just the length of **P** as a character string, multiplied by the number of bits in a character (e.g., 7 for ASCII).

We could, alternatively, choose an encoding for Turing machines, where an *encoding* is a function which associates to each Turing Machine **M** a bitstring . If **M** is a Turing Machine which, on input *w*, outputs string *x*, then the concatenated string  *w* is a description of *x*. For theoretical analysis, this approach is more suited for constructing detailed formal proofs and is generally preferred in the research literature. In this article, an informal approach is discussed.

Any string *s* has at least one description. For example, the second string above is output by the pseudo-code:

 **function** GenerateString2()
     **return** "4c1j5b2p0cv4w1x8rx2y39umgw5q85s7"

whereas the first string is output by the (much shorter) pseudo-code:

 **function** GenerateString1()
     **return** "ab" × 16

If a description *d*(*s*) of a string *s* is of minimal length (i.e., using the fewest bits), it is called a **minimal description** of *s*, and the length of *d*(*s*) (i.e. the number of bits in the minimal description) is the **Kolmogorov complexity** of *s*, written *K*(*s*). Symbolically,

The length of the shortest description will depend on the choice of description language; but the effect of changing languages is bounded (a result called the *invariance theorem*, see below).

### Plain Kolmogorov complexity *C* {#-plain-kolmogorov-complexity-c}
There are two definitions of Kolmogorov complexity: *plain* and *prefix-free*. The plain complexity is the minimal description length of any program, and denoted C(x) while the prefix-free complexity is the minimal description length of any program encoded in a prefix-free code, and denoted K(x). The plain complexity is more intuitive, but the prefix-free complexity is easier to study.

By default, all equations hold only up to an additive constant. For example, f(x) = g(x) really means that f(x) = g(x) + O(1), that is, \exists c, \forall x, |f(x) - g(x)| \leq c.

Let U: 2^* \to 2^* be a computable function mapping finite binary strings to binary strings. It is a universal function if, and only if, for any computable f: 2^* \to 2^*, we can encode the function in a "program" s_f, such that \forall x \in 2^*, U(s_fx) = f(x) . We can think of U as a program interpreter, which takes in an initial segment describing the program, followed by data that the program should process.

One problem with plain complexity is that C(xy) \not , because intuitively speaking, there is no general way to tell where to divide an output string just by looking at the concatenated string. We can divide it by specifying the length of x or y, but that would take O(\min(\ln x, \ln y)) extra symbols. Indeed, for any c > 0 there exists x, y such that C(xy) \geq C(x) + C(y) + c.

Typically, inequalities with plain complexity have a term like O(\min(\ln x, \ln y)) on one side, whereas the same inequalities with prefix-free complexity have only O(1).

The main problem with plain complexity is that there is something extra sneaked into a program. A program not only represents for something with its code, but also represents its own length. In particular, a program x may represent a binary number up to \log_2 |x|, simply by its own length. Stated in another way, it is as if we are using a termination symbol to denote where a word ends, and so we are not using 2 symbols, but 3. To fix this defect, we introduce the prefix-free Kolmogorov complexity.

### Prefix-free Kolmogorov complexity *K* {#-prefix-free-kolmogorov-complexity-k}

A **prefix-free universal Turing machine** is a universal partial computable function U:2^* \rightarrow 2^* whose domain is a prefix-free set of binary strings. 
Equivalently, no valid program for U is a prefix of any other, the domain satisfies the prefix property. For instance, if every valid program for a universal Turing machine U ended with a termination string that could not appear elsewhere in the program, U would be prefix-free.

The prefix-free Kolmogorov complexity of a string x is defined by
K(x) := \min\
This is a contradiction, Q.E.D.

As a consequence, the above program, with the chosen value of *n*0, must loop forever.

Similar ideas are used to prove the properties of Chaitin's constant.

## Minimum message length {#-minimum-message-length}

The minimum message length principle of statistical and inductive inference and machine learning was developed by C.S. Wallace and D.M. Boulton in 1968. MML is Bayesian (i.e. it incorporates prior beliefs) and information-theoretic. It has the desirable properties of statistical invariance (i.e. the inference transforms with a re-parametrisation, such as from polar coordinates to Cartesian coordinates), statistical consistency (i.e. even for very hard problems, MML will converge to any underlying model) and efficiency (i.e. the MML model will converge to any true underlying model about as quickly as is possible). C.S. Wallace and D.L. Dowe (1999) showed a formal connection between MML and algorithmic information theory (or Kolmogorov complexity).

## Kolmogorov randomness {#-kolmogorov-randomness}

*Kolmogorov randomness* defines a string (usually of bits) as being random if the shortest computer program that can produce that string is about as long as the string itself.  To make this precise, a string x of length n is called *Kolmogorov random* if

K(x) \ge n + O(1)
 where K is the prefix-free Kolmogorov complexity defined above.
A random string in this sense is *incompressible* in that it is impossible to "compress" the string into a program that is shorter than the string itself. There is at least one Kolmogorov random string of each length.

This definition can be extended to define a notion of randomness for *infinite* sequences from a finite alphabet. These algorithmically random sequences can be defined in three equivalent ways. One way uses an effective analogue of measure theory; another uses effective martingales.  The third way defines an infinite sequence to be random if the prefix-free Kolmogorov complexity of its initial segments grows quickly enough — there must be a constant *c* such that the complexity of an initial segment of length *n* is always at least *n*−*c*.

## Relation to entropy {#-relation-to-entropy}
For dynamical systems, entropy rate and algorithmic complexity of the trajectories are related by a theorem of Brudno, that the equality K(x;T) =  h(T) holds for almost all x.

It can be shown that for the output of Markov information sources, Kolmogorov complexity is related to the entropy of the information source. More precisely, the Kolmogorov complexity of the output of a Markov information source, normalized by the length of the output, converges almost surely (as the length of the output goes to infinity) to the entropy of the source.

**Theorem.** (Theorem 14.2.5 ) The conditional Kolmogorov complexity of a binary string x_{1:n} satisfies\frac 1n K(x_{1:n} | n) \leq H_b\left(\frac 1n \sum_i x_i\right) + \frac{\log n}{2n} + O(1/n)
where H_b is the binary entropy function (not to be confused with the entropy rate).

## Halting problem {#-halting-problem}
The Kolmogorov complexity function is equivalent to deciding the halting problem.

If we have a halting oracle, then the Kolmogorov complexity of a string can be computed by simply trying every halting program, in lexicographic order, until one of them outputs the string.

The other direction is much more involved. It shows that given a Kolmogorov complexity function, we can construct a function p, such that p(n) \geq BB(n) for all large n, where BB is the Busy Beaver shift function (also denoted as S(n)). By modifying the function at lower values of n we get an upper bound on BB, which solves the halting problem.

Consider this program p_K, which takes input as n, and uses K.

* List all strings of length \leq 2n + 1.
* For each such string x, enumerate all (prefix-free) programs of length K(x) until one of them does output x. Record its runtime n_x.
* Output the largest n_x.

We prove by contradiction that p_K(n) \geq BB(n) for all large n.

Let p_{n} be a Busy Beaver of length n. Consider this (prefix-free) program, which takes no input:

* Run the program p_{n}, and record its runtime length BB(n).
* Generate all programs with length \leq 2n. Run every one of them for up to BB(n) steps. Note the outputs of those that have halted.
* Output the string with the lowest lexicographic order that has not been output by any of those.

Let the string output by the program be x.

The program has length \leq n + 2\log_2 n + O(1), where n comes from the length of the Busy Beaver p_{n}, 2\log_2 n comes from using the (prefix-free) Elias delta code for the number n, and O(1) comes from the rest of the program. Therefore,K(x) \leq n + 2\log_2 n + O(1) \leq 2nfor all big n. Further, since there are only so many possible programs with length \leq 2n, we have l(x) \leq 2n + 1 by pigeonhole principle.
By assumption, p_K(n) , so every string of length \leq 2n + 1 has a minimal program with runtime . Thus, the string x has a minimal program with runtime . Further, that program has length K(x) \leq 2n. This contradicts how x was constructed.

## Universal probability {#-universal-probability}

Fix a universal Turing machine U, the same one used to define the (prefix-free) Kolmogorov complexity. Define the (prefix-free) universal probability of a string x to beP(x) = \sum_{U(p) = x} 2^{-l(p)}In other words, it is the probability that, given a uniformly random binary stream as input, the universal Turing machine would halt after reading a certain prefix of the stream, and output x.

Note. U(p) = x does not mean that the input stream is p000\cdots, but that the universal Turing machine would halt at some point after reading the initial segment p, without reading any further input, and that, when it halts, it has written x to the output tape.

**Theorem.** (Theorem 14.11.1 Considering the genome as a program that must solve a task or implement a series of functions, shorter programs would be preferred on the basis that they are easier to find by the mechanisms of evolution. An example of this approach is the eight-fold symmetry of the compass circuit that is found across insect species, which correspond to the circuit that is both functional and requires the minimum Kolmogorov complexity to be generated from self-replicating units.

## Conditional versions {#-conditional-versions}

The conditional Kolmogorov complexity of two strings K(x|y) is, roughly speaking, defined as the Kolmogorov complexity of *x* given *y* as an auxiliary input to the procedure. So while the (unconditional) Kolmogorov complexity K(x) of a sequence x is the length of the shortest binary program that outputs x on a universal computer and can be thought of as the minimal amount of information necessary to produce x, the conditional Kolmogorov complexity K(x|y) is defined as the length of the shortest binary program that computes x when y is given as input, using a universal computer.

There is also a length-conditional complexity K(x|L(x)), which is the complexity of *x* given the length of *x* as known/input.

## Time-bounded complexity {#-time-bounded-complexity}
Time-bounded Kolmogorov complexity is a modified version of Kolmogorov complexity where the space of programs to be searched for a solution is confined to only programs that can run within some pre-defined number of steps. It is hypothesised that the possibility of the existence of an efficient algorithm for determining approximate time-bounded Kolmogorov complexity is related to the question of whether true one-way functions exist.

## See also {#-see-also}
* Berry paradox
* Code golf
* Data compression
* Descriptive complexity theory
* Grammar induction
* Inductive reasoning
* Kolmogorov structure function
* Levenshtein distance
* Manifold hypothesis
* Solomonoff's theory of inductive inference
* Sample entropy
* Rayo's number

## Notes {#-notes}

## References {#-references}

## Further reading {#-further-reading}
* 
* 
* 
* 
* 
* 
* 
* 

## External links {#-external-links}
* The Legacy of Andrei Nikolaevich Kolmogorov
* Chaitin's online publications
* Solomonoff's IDSIA page
* Generalizations of algorithmic information by J. Schmidhuber
* 
*  Tromp's lambda calculus computer model offers a concrete definition of K()]
* Universal AI based on Kolmogorov Complexity  by M. Hutter:  
* David Dowe's Minimum Message Length (MML) and Occam's razor pages.
*

---

## Theophysics Applications {#-theophysics-applications}

- [[04_THEOPYHISCS/[6.6] LOGOS_V3/05_PUBLICATIONS/Logos_Papers/Paper 3 The Algorithm of Reality|Paper 3 The Algorithm of Reality]]
- [[04_THEOPYHISCS/[6.6] LOGOS_V3/05_PUBLICATIONS/Logos_Papers/PAPER-1-COMPLETE|Paper 1 Enhancement - COMPLETE ✅]]
- [[04_THEOPYHISCS/[6.6] LOGOS_V3/05_PUBLICATIONS/Logos_Papers/Papers_01-12_FINAL_SIMPLE|THE [[Theophysics_Glossary#Logos|LOGOS]] PAPERS]]
- [[04_THEOPYHISCS/[6.6] LOGOS_V3/05_PUBLICATIONS/Chapter Archive/Paper 11 - Protocols for Validation - FULL|Paper 11 - Protocols for Validation - FULL]]
- [[04_THEOPYHISCS/[6.6] LOGOS_V3/05_PUBLICATIONS/Chapter Archive/Paper 11 Protocols for Validation|Paper 11 Protocols for Validation]]
- [[04_THEOPYHISCS/[6.6] LOGOS_V3/05_PUBLICATIONS/Chapter Archive/Paper 12 The Decalogue of the Cosmos|Paper 12 The Decalogue of the Cosmos]]
- [[04_THEOPYHISCS/[6.6] LOGOS_V3/05_PUBLICATIONS/Chapter Archive/Paper 2 (Revised) The Quantum Bridge|Paper 2 (Revised) The Quantum Bridge]]
- [[04_THEOPYHISCS/[6.6] LOGOS_V3/05_PUBLICATIONS/Chapter Archive/Paper-02-Quantum-Bridge|Paper-02-Quantum-Bridge]]
- [[04_THEOPYHISCS/[6.6] LOGOS_V3/05_PUBLICATIONS/Chapter Archive/Paper-02-The-Quantum-Bridge-FINAL|Core Metadata]]
- [[04_THEOPYHISCS/[6.5] JS-SERIES/AXIOM_STATUS_REPORT|188 Axioms - Status Report]]
- [[04_THEOPYHISCS/[7.0] Paper_2_Quantum_Bridge/SESSION_SUMMARY|SESSION SUMMARY: PAPER 1 CRITIQUE RESPONSE]]
- [[04_THEOPYHISCS/[7.6] Protocols/14_David_Effect_Protocol|Protocol 4: The David Effect]]
- [[04_THEOPYHISCS/[7.6] Protocols/P11-Protocols-Validation Final ALL|P11-PROTOCOLS-VALIDATION: COMPLETE COLLECTION]]
- [[00_SYSTEM/00_ENGINE/01_ENGINE/scripts/Edge-TTS/input/00_DE REVOLUTIONIBUS VERITATIS|De Revolutionibus Veritatis — The Six Books]]
- [[01_DE_REVOLUTIONIBUS_VERITATIS_THE_ARCHITECTURE|01 DE REVOLUTIONIBUS VERITATIS THE ARCHITECTURE]]
- [[02_DE_REVOLUTIONIBUS_VERITATIS_THE_LOCK|02 DE REVOLUTIONIBUS VERITATIS THE LOCK]]
- [[04_DE_REVOLUTIONIBUS_VERITATIS_THE_KEY|BC1]]
- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/downloads|Download the Full Framework]]
- [[00_AI/04_SKILLS/antigravity-awesome-skills-main/README|Three Truths — Content Structure]]
- [[truth-one-self-reference-limits|Truth One: The Self-Reference Limits]]

## Related Theories {#-related-theories}

*See [[00_Canonical/THEORY_INTERCONNECTIONS|Theory Interconnections]] for semantic links.*

---
*Source: [Kolmogorov complexity](https://en.wikipedia.org/wiki/Kolmogorov_complexity)*
*Downloaded: 2026-02-26 | Theophysics Canonical Knowledge Base*


---

## Metadata

**Original File:** Kolmogorov_Complexity.md

**Restructured:** 2026-03-01 15:52:17

**Format:** Canonical Theory Document (Lowe Standard v1.0)

**Status:** Cleaned and ready for evaluation

---

*This paper has been restructured for clarity and proper academic formatting. Original content preserved.*
