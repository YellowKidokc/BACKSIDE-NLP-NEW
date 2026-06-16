---
title: "Church-Turing Thesis"
author: "Logic to the Computer"
date: 2026-03-01
category: theory
tags:
  - theory
  - theory
  - canonical
source_file: Church-Turing_Thesis.md
restructured: 2026-03-01 15:52:18
---

# Church-Turing Thesis

**Author:** Logic to the Computer

**Date:** 2026-03-01

---

## Table of Contents

- [# Church-Turing Thesis](#-church-turing-thesis)
- [## Overview](#-overview)
- [## Definitions](#-definitions)
- [### Core Concepts](#-core-concepts)
- [## 1. The 1936 Thesis and its Context](#-1-the-1936-thesis-and-its-context)
- [## 1. The 1936 Thesis and its Context](#-1-the-1936-thesis-and-its-context)
- [### 1.2 Making the informal concept of an effective method precise](#-12-making-the-informal-concept-of-an-effective-method-precise)
- [### 1.7 The *Entscheidungsproblem*](#-17-the-entscheidungsproblem)
- [### 1.7 The *Entscheidungsproblem*](#-17-the-entscheidungsproblem)
- [## 2. Backstory: Emergence of the concepts of *effective method* and *decision method*](#-2-backstory-emergence-of-the-concepts-of-effective-method-and-decision-method)
- [### 2.1 From simple rules-of-thumb to Siri and beyond](#-21-from-simple-rules-of-thumb-to-siri-and-beyond)
- [### 3.1 Gödel](#-31-gödel)
- [### 3.2 Post](#-32-post)
- [### 4.3 Turing’s argument I](#-43-turings-argument-i)
- [### 4.4 Turing’s argument II](#-44-turings-argument-ii)

---

# Church-Turing Thesis {#-church-turing-thesis}

<!-- SEMANTIC INLINE LABELS START -->
<details class="semantic-ai-inline-labels">
<summary><strong>Semantic Labels</strong> (click to show/hide)</summary>

Total tags: 19

**Axiom (2)**
- `Axiom` Effective Method Definition
- `Axiom` Principles of Effective Computability

**Claim (13)**
- `Claim` Church-Turing Thesis
- `Claim` Every effective computation can be carried out by a Turing machine -> parent: Church-Turing Thesis
- `Claim` Some modern theses are distant relatives of the original Church-Turing thesis -> parent: Church-Turing Thesis
- `Claim` An effective method must be systematic and mechanical -> parent: Effective Method Definition
- `Claim` Effective methods can be expressed as finite instructions -> parent: Effective Method Definition
- `Claim` Turing's analysis of computability is superior to Church's
- `Claim` Gödel found Turing's analysis satisfactory -> parent: Turing's analysis of computability is superior to Church's
- `Claim` All effectively calculable functions are Turing-machine computable -> parent: Equivalence of Church and Turing's Theses
- `Claim` There are no functions in S other than those obtained by effective methods -> parent: Equivalence of Church and Turing's Theses
- `Claim` Effective calculability is equivalent to recursiveness -> parent: Principles of Effective Computability
- `Claim` Turing's thesis is about human computation
- `Claim` The Entscheidungsproblem is unsolvable
- `Claim` Turing's machines can simulate any effective procedure

**EvidenceBundle (3)**
- `EvidenceBundle` Historical Context of Church-Turing Thesis -> parent: Church-Turing Thesis
- `EvidenceBundle` Gödel's Acceptance of Turing's Thesis -> parent: Gödel found Turing's analysis satisfactory
- `EvidenceBundle` Historical Development of Effective Methods

**Relationship (1)**
- `Relationship` Equivalence of Church and Turing's Theses

</details>

<!-- SEMANTIC INLINE LABELS END -->
## Overview {#-overview}
Source: [SEP](https://plato.stanford.edu/entries/church-turing/)

## Definitions {#-definitions}

### Core Concepts {#-core-concepts}
The Church-Turing thesis (or Turing-Church thesis) is a fundamental
claim in the theory of computability. It was advanced independently by
Church and Turing in the mid 1930s. There are various equivalent
formulations of the thesis. A common one is that every effective
computation can be carried out by a Turing machine (i.e., by
Turing’s abstract computing machine, which in its universal form
encapsulates the fundamental logical principles of the stored-program
all-purpose digital computer). Modern reimaginings of the
Church-Turing thesis transform it, extending it to fundamental
physics, complexity theory, exotic algorithms, and cognitive science.
encapsulates the fundamental logical principles of the stored-program
all-purpose digital computer). Modern reimaginings of the
Church-Turing thesis transform it, extending it to fundamental
physics, complexity theory, exotic algorithms, and cognitive science.
It is important to be aware though that some of the theses nowadays
referred to as the Church-Turing thesis are at best *very*
distant relatives of the thesis advanced by Church and Turing.

## 1. The 1936 Thesis and its Context {#-1-the-1936-thesis-and-its-context}

Church-Turing thesis transform it, extending it to fundamental
physics, complexity theory, exotic algorithms, and cognitive science.
It is important to be aware though that some of the theses nowadays
referred to as the Church-Turing thesis are at best *very*
distant relatives of the thesis advanced by Church and Turing.

## 1. The 1936 Thesis and its Context {#-1-the-1936-thesis-and-its-context}

The Church-Turing thesis concerns the concept of an *effective*
or *systematic* or *mechanical* method, as used in
The Church-Turing thesis concerns the concept of an *effective*
or *systematic* or *mechanical* method, as used in
logic, mathematics and computer science. “Effective” and
its synonyms “systematic” and “mechanical” are
terms of art in these disciplines: they do not carry their everyday
meaning. A method, or procedure, \(M\), for achieving some desired
result is called “effective” (or “systematic”
or “mechanical”) just in case:

1. \(M\) is set out in terms of a finite number of exact instructions
### 1.2 Making the informal concept of an effective method precise {#-12-making-the-informal-concept-of-an-effective-method-precise}

The notion of an effective method or procedure is an informal one, and
attempts to characterize effectiveness, such as the above, lack rigor,
for the key requirement that the method must demand no insight,
intuition or ingenuity is left unexplicated.

One of Alan Turing’s achievements, in his famous paper of 1936,
was to present a formally exact predicate with which the informal
predicate “can be done by means of an effective method”
concept proposed by Turing, it is appropriate to refer to the thesis
also as “Turing’s thesis”; and as
“Church’s thesis” when expressed in terms of one or
another of the formal replacements proposed by Church.

The formal concept proposed by Turing was that of *computability by
Turing machine*. He argued for the claim—Turing’s
thesis—that whenever there is an effective method for obtaining
the values of a mathematical function, the function can be computed by
a Turing machine.
The formal concept proposed by Turing was that of *computability by
Turing machine*. He argued for the claim—Turing’s
thesis—that whenever there is an effective method for obtaining
the values of a mathematical function, the function can be computed by
a Turing machine.

The converse claim—amounting to the claim mentioned above, that
there are no functions in \(S\) *other than* ones whose values
can be obtained by an effective method—is easily established,
since a Turing machine program is itself a specification of an
Church gave two alternative analyses, one in terms of the concept of
*recursion* and the other in terms of
*lambda-definability* (λ-definability). He proposed that
we

> define the notion … of an effectively calculable function of
> positive integers by identifying it with the notion of a recursive
> function of positive integers (or of a λ-definable function of
> positive integers). (Church 1936a: 356)

The concept of a λ-definable function was due to Church and
Kleene, with contributions also by Rosser (Church 1932, 1933, 1935c,
1936a; Church & Rosser 1936; Kleene 1934, 1935a,b, 1936a,b; Kleene
& Rosser 1935; Rosser 1935a,b). A function is said to be
λ-definable if the values of the function can be obtained by a
certain process of repeated substitution. The concept of a recursive
function had emerged over time through the work of, among others,
Grassmann, Peirce, Dedekind, Peano, Skolem, Hilbert—and his
“assistants” Ackermann and Bernays—Sudan,
Péter (née Politzer), Herbrand, Kleene, and
certain process of repeated substitution. The concept of a recursive
function had emerged over time through the work of, among others,
Grassmann, Peirce, Dedekind, Peano, Skolem, Hilbert—and his
“assistants” Ackermann and Bernays—Sudan,
Péter (née Politzer), Herbrand, Kleene, and
pre-eminently Gödel (Gödel 1931, 1934). The class of
λ-definable functions (of positive integers) and the class of
recursive functions (of positive integers) are identical; this was
proved by Church and Kleene (Church 1936a; Kleene 1936a,b).

paper for publication), he quickly established that the concept of
λ-definability and his concept of computability are equivalent
(by proving the “theorem that all … λ-definable
sequences … are computable” and its converse; Turing 1936
[2004: 88ff]). Thus, in Church’s proposal, the words
“λ-definable function of positive integers” (and
equally the words “recursive function of positive
integers”) can be replaced by “function of positive
integers that is computable by Turing machine”. What Turing
proved is called an *equivalence result*. There is further
λ-definability and his concept of computability are equivalent
(by proving the “theorem that all … λ-definable
sequences … are computable” and its converse; Turing 1936
[2004: 88ff]). Thus, in Church’s proposal, the words
“λ-definable function of positive integers” (and
equally the words “recursive function of positive
integers”) can be replaced by “function of positive
integers that is computable by Turing machine”. What Turing
proved is called an *equivalence result*. There is further
discussion of equivalence results in
Church for masking this hypothesis as a *definition*:

> [T]o mask this identification under a definition … blinds us to
> the need of its continual verification. (Post 1936: 105)

This, then, is the “working hypothesis” that, in effect,
Church proposed:

> **Church’s thesis**:
>   
> [T]o mask this identification under a definition … blinds us to
> the need of its continual verification. (Post 1936: 105)

This, then, is the “working hypothesis” that, in effect,
Church proposed:

> **Church’s thesis**:
>   
> A function of positive integers is effectively calculable only if
> λ-definable (or, equivalently, recursive).
“definition”).

If attention is restricted to functions of positive integers,
Church’s thesis and Turing’s thesis are
*extensionally* equivalent. “Extensionally
equivalent” means that the two theses are about one and the same
class of functions: In view of the previously mentioned results by
Church, Kleene and Turing, the class of λ-definable functions
(of positive integers) is identical to the class of recursive
functions (of positive integers) and to the class of computable
> proposal to use λ-definability as a definition of effective
> calculability. … It seems that only after Turing’s
> formulation appeared did Gödel accept Church’s thesis.
> (Kleene 1981: 59, 61)

Gödel described Turing’s analysis of computability as
“most satisfactory” and “correct … beyond any
doubt” (Gödel 1951: 304 and 193?: 168). He remarked:

> We had not perceived the sharp concept of mechanical procedures
> We had not perceived the sharp concept of mechanical procedures
> sharply before Turing, who brought us to the right perspective.
> (Quoted in Wang 1974: 85)

Gödel also said:

> The resulting definition of the concept of mechanical by the sharp
> concept of “performable by a Turing machine” is both
> correct and unique. (Quoted in Wang 1996: 203)

> The resulting definition of the concept of mechanical by the sharp
> concept of “performable by a Turing machine” is both
> correct and unique. (Quoted in Wang 1996: 203)

And:

> Moreover it is absolutely impossible that anybody who understands the
> question and knows Turing’s definition should decide for a
> different concept. (Ibid.)

> concept of “performable by a Turing machine” is both
> correct and unique. (Quoted in Wang 1996: 203)

And:

> Moreover it is absolutely impossible that anybody who understands the
> question and knows Turing’s definition should decide for a
> different concept. (Ibid.)

Even the modest young Turing agreed that his analysis was
> question and knows Turing’s definition should decide for a
> different concept. (Ibid.)

Even the modest young Turing agreed that his analysis was
“possibly more convincing” than Church’s (Turing
1937: 153).

### 1.7 The *Entscheidungsproblem* {#-17-the-entscheidungsproblem}

Both Turing and Church introduced their respective versions of the
> different concept. (Ibid.)

Even the modest young Turing agreed that his analysis was
“possibly more convincing” than Church’s (Turing
1937: 153).

### 1.7 The *Entscheidungsproblem* {#-17-the-entscheidungsproblem}

Both Turing and Church introduced their respective versions of the
Church-Turing thesis in the course of attacking the so-called
definitions of the calculus, using only the rules of the calculus.)
For example, if such a method for the classical propositional calculus
is used to test the formula \(A \rightarrow A\) (\(A\) implies \(A\)),
the output will be “Yes, provable”, and if the
contradiction \(A \amp \neg A\) is tested, the output will be
“Not provable”. Such a method is called a *decision
method* or *decision procedure*.

Church and Turing took on the *Entscheidungsproblem* for a
fundamentally important logical system called the (first-order)
fundamentally important logical system called the (first-order)
*functional calculus*. The functional calculus consists of
standard propositional logic plus standard quantifier logic. The
functional calculus is also known as the *classical predicate
calculus* and as *quantification theory* (and Church
sometimes used the German term *engere Funktionenkalkül*).
They each arrived at the same negative result, arguing on the basis of
the Church-Turing thesis that, in the case of the functional calculus,
the *Entscheidungsproblem* is *unsolvable*—there
can be *no* decision method for the calculus. The two
## 2. Backstory: Emergence of the concepts of *effective method* and *decision method* {#-2-backstory-emergence-of-the-concepts-of-effective-method-and-decision-method}

Effective methods are the subject matter of the Church-Turing thesis.
How did this subject matter evolve and how was it elaborated prior to
Church and Turing? This section looks back to an earlier era, after
which
[Section 3](#OtheApprComp)
turns to modern developments.

### 2.1 From simple rules-of-thumb to Siri and beyond {#-21-from-simple-rules-of-thumb-to-siri-and-beyond}
goodness, and other fundamental issues. Three hundred years later, in
the seventeenth century, Hobbes was asserting that human reasoning
processes amount to nothing more than (essentially arithmetical)
effective procedures:

> By reasoning I understand computation. (Hobbes 1655 [1839]: ch. 1
> sect. 2)

Nowadays, effective methods—algorithms—are the basis for
every job that electronic computers do. According to some computer
glimpsed the concept of a general question-answering method, writing
in approximately 1300 of a general art (“*ars*”),
or technique, “by means of which one may know in regard to all
natural things” (*Lo Desconhort*, line 8, in Llull 1986:
99). He dreamed of an *ars generalis* (general technique) that
could mechanize the “one general science, with its own general
principles in which the principles of other sciences would be
implicit” (Preface to *Ars Generalis Ultima*, in Llull
1645 [1970: 1]). Llull used circumscribed fields of knowledge to
illustrate his idea of a mechanical question-answerer, designing small
mechanical methods led him to an even grander conception, inspired in
part by Llull’s unclear but provocative speculations about a
general-purpose question-answering mechanism. Leibniz said that Llull
“had scraped the skin off” this idea, but “did not
see its inmost parts” (Leibniz 1671 [1926: 160]). Leibniz
envisaged a method, just as mechanical as multiplication or division,
whereby

> when there are disputes among persons, we can simply say: Let us
> calculate, without further ado, in order to see who is right. (Leibniz
The modern concept of a decision method for a logical calculus did not
develop until the twentieth century. But earlier logicians, including
Leibniz, certainly had the concept of a method that is
*mechanical* in the literal sense that it could be carried out
by a machine constructed from mechanical components of the sort
familiar to them—discs, pins, rods, springs, levers, pulleys,
rotating shafts, gear wheels, weights, dials, mechanical switches,
slotted plates, and so forth.

In 1869, Jevons designed a pioneering machine known as the
Leibniz, certainly had the concept of a method that is
*mechanical* in the literal sense that it could be carried out
by a machine constructed from mechanical components of the sort
familiar to them—discs, pins, rods, springs, levers, pulleys,
rotating shafts, gear wheels, weights, dials, mechanical switches,
slotted plates, and so forth.

In 1869, Jevons designed a pioneering machine known as the
“logic piano” (Jevons 1870; Barrett & Connell 2005).
The name arose because of the machine’s piano-like keyboard for
Venn, like Jevons, was well aware of the concept of a literally
mechanical method. He pointed out that diagrammatic methods such as
his “readily lend themselves to mechanical performance”
(Venn 1880: 15). Venn went on to describe what he called a
“logical-diagram machine”. This simple machine displayed
wooden segments corresponding to the component areas of a Venn
diagram; each wooden segment represented one of four terms. A
finger-operated release mechanism allowed any segment selected by the
user to drop downwards. This represented “the destruction of any
class” (1880: 18). Venn reported that he constructed this
Peirce anticipated the concept of a decision method in his extensive
notes for a series of lectures he delivered in Boston in 1903. There
he developed a method (Peirce 1903b,c) that, if applied to any given
formula of the propositional calculus, would, he said,
“determine” (or “positively ascertain”)
whether the alpha-graphs system demonstrates that the formula is
satisfiable (is “alpha-possible”, in Peirce’s
terminology), or whether, on the other hand, the system demonstrates
that it is unsatisfiable (“alpha-impossible”). (See the
supplement on
and two definitions). This statement of Peirce’s, made almost
four decades before Turing introduced Turing machines into
mathematics, was well ahead of its time.

As to whether *all* mathematical reasoning can be performed by
a machine, as Leibniz seems to have thought, Peirce was fiercely
skeptical. He formulated the hypothesis that, in the future,
mathematical reasoning

> might conceivably be left to a machine—some Babbage’s
he emphasized the need to study the concept of “decidability by
a finite number of operations”,
saying—accurately—that this would be “an important
new field of research to develop” (Hilbert 1917: 415). The
lecture considered a number of what he called “most challenging
epistemological problems of a specifically mathematical
character” (1917: 412). Pre-eminent among these was the
“problem of the decidability [*Entscheidbarkeit*] of a
mathematical question” because the problem “touches
profoundly upon the nature of mathematical thinking” (1917:
symbolic language, in conception akin to languages used in
mathematical logic and computer science today. Hilbert and Ackermann
acknowledged Leibniz’s influence on the first page of their
*Grundzüge der Theoretischen Logik*, saying “The
idea of a mathematical logic was first put into a clear form by
Leibniz” (Hilbert & Ackermann 1928: 1). Cassirer said that
in Hilbert’s work “the fundamental idea of Leibniz’s
‘universal characteristic’ is taken up anew and attains a
succinct and precise expression” (Cassirer 1929: 440). It was in
the writings of the Göttingen group that Leibniz’s idea of
in Hilbert’s work “the fundamental idea of Leibniz’s
‘universal characteristic’ is taken up anew and attains a
succinct and precise expression” (Cassirer 1929: 440). It was in
the writings of the Göttingen group that Leibniz’s idea of
an effective method for answering any specified mathematical or
scientific question found its fullest development (see further the
supplement on
[The Rise and Fall of the *Entscheidungsproblem*](decision-problem.html)).

Hilbert’s earliest publication to mention what we would now call
Hilbert expressed the concept of a decision method more clearly the
following year, in his famous turn-of-the-century speech in Paris, to
the International Congress of Mathematicians. He presented
twenty-three unsolved problems, “from the discussion of which an
advancement of science may be expected”. The tenth on his list
(now known universally as Hilbert’s Tenth Problem) was:

> Given a diophantine equation with any number of unknown quantities and
> with rational integral numerical coefficients: *To devise a process
> according to which it can be determined by a finite number of
mathematical logic (1928: 1). Like Peirce, Behmann used the concept of
a machine to clarify the nature of the *Entscheidungsproblem*.
“It is essential to the character” of the problem, Behmann
said, that “only entirely mechanical calculation according to
given instructions” is involved. The decision whether the
statement is true or false becomes “a mere exercise in
computation”; there is “an elimination of thinking in
favor of mechanical calculation”. Behmann continued:

> One might, if one wanted to, speak of mechanical or machine-like
problem of analyzing the concept of effectiveness. This section
surveys some other important proposals made during the twentieth and
twenty-first centuries.

### 3.1 Gödel {#-31-gödel}

Gödel was led to the problem of analyzing effectiveness by his
search for a means to *generalize* his 1931 incompleteness
results (which in their original form applied specifically to the
formal system set out by Whitehead and Russell in their *Principia
generalized concept of recursion—about a year before Church
first publicly announced his thesis that “the notion of an
effectively calculable function of positive integers should be
identified with that of a recursive function” (Church 1935a;
Gödel 1934, fn. 3; Davis 1982).

But Gödel was doubtful: “I was, at the time … not at
all convinced that my concept of recursion comprises all possible
recursions” (Gödel 1965b). It was Turing’s analysis,
Gödel emphasized, that finally enabled him to generalize his
all convinced that my concept of recursion comprises all possible
recursions” (Gödel 1965b). It was Turing’s analysis,
Gödel emphasized, that finally enabled him to generalize his
incompleteness theorems:

> due to A. M. Turing’s work, a precise and unquestionably
> adequate definition of the general concept of formal system can now be
> given. (Gödel 1965a: 71)

He explained:
> adequate definition of the general concept of formal system can now be
> given. (Gödel 1965a: 71)

He explained:

> Turing’s work gives an analysis of the concept of
> “mechanical procedure” (alias “algorithm” or
> “computation procedure” or “finite combinatorial
> procedure”). This concept is shown to be equivalent with that of
> a “Turing machine”. A formal system can simply be defined
> Turing’s work gives an analysis of the concept of
> “mechanical procedure” (alias “algorithm” or
> “computation procedure” or “finite combinatorial
> procedure”). This concept is shown to be equivalent with that of
> a “Turing machine”. A formal system can simply be defined
> to be any mechanical procedure for producing formulas, called provable
> formulas. (Gödel 1965a: 71–72)

Armed with this definition, incompleteness can, Gödel said,
“be proved rigorously for *every* consistent formal
> procedure”). This concept is shown to be equivalent with that of
> a “Turing machine”. A formal system can simply be defined
> to be any mechanical procedure for producing formulas, called provable
> formulas. (Gödel 1965a: 71–72)

Armed with this definition, incompleteness can, Gödel said,
“be proved rigorously for *every* consistent formal
system containing a certain amount of finitary number theory”
(1965a: 71).

Armed with this definition, incompleteness can, Gödel said,
“be proved rigorously for *every* consistent formal
system containing a certain amount of finitary number theory”
(1965a: 71).

### 3.2 Post {#-32-post}

By 1936, Post had arrived independently at an analysis of
effectiveness that was substantially the same as Turing’s (Post
1936; Davis & Sieg 2015). Post’s idealized human
“rule-governed”. Hilbert and Bernays offered the concept
of the *rule-governed evaluation* of a numerical function as a
“sharpening of the concept of computable” (1939: 417).

The basic idea is this: To evaluate a numerical function (such as
addition or multiplication) in a rule-governed way is to calculate the
values of the function, step by logical step, in a suitable deductive
logical system. On this approach, effective calculability is analysed
as *calculability in a logic*. (Both Church and Turing had
previously discussed the approach—see
“sharpening of the concept of computable” (1939: 417).

The basic idea is this: To evaluate a numerical function (such as
addition or multiplication) in a rule-governed way is to calculate the
values of the function, step by logical step, in a suitable deductive
logical system. On this approach, effective calculability is analysed
as *calculability in a logic*. (Both Church and Turing had
previously discussed the approach—see
[Section 4.4](#TuriArguII).)

when it was still wide open how the intuitive concept of effective
calculability should be formalized (probably during 1934). Gödel
suggested that

> it might be possible, in terms of effective calculability as an
> undefined notion, to state a set of axioms which would embody the
> generally accepted properties of this notion, and to do something on
> that basis. (Church 1935b)

Logicians frequently analyse a concept of interest, e.g., universal
Logicians frequently analyse a concept of interest, e.g., universal
quantification, not by defining it in terms of other concepts, but by
stating a set of axioms that collectively embody the generally
accepted properties of (say) universal quantification. To follow this
approach in the case of effectiveness, we would “write down some
axioms about computable functions which most people would agree are
evidently true” (Shoenfield 1993: 26). Shoenfield continued,
“It might be possible to prove Church’s Thesis from such
axioms”, but added: “However, despite strenuous efforts,
no one has succeeded in doing this”.
quantification, not by defining it in terms of other concepts, but by
stating a set of axioms that collectively embody the generally
accepted properties of (say) universal quantification. To follow this
approach in the case of effectiveness, we would “write down some
axioms about computable functions which most people would agree are
evidently true” (Shoenfield 1993: 26). Shoenfield continued,
“It might be possible to prove Church’s Thesis from such
axioms”, but added: “However, despite strenuous efforts,
no one has succeeded in doing this”.

* Engeler axiomatized the concept of an algorithmic function by using
  *combinators* (Engeler 1983: ch. III). Combinators were
  originally introduced by Schönfinkel in 1924, in a paper that a
  recent book on combinators described as “presenting a formalism
  for universal computation for the very first time”
  (Schönfinkel 1924; Wolfram 2021: 214). Schönfinkel’s
  combinators were extensively developed by Curry (Curry 1929, 1930a,b,
  1932; Curry & Feys 1958). Examples of combinators are the
  “permutator” \(\mathrm{C}\) and the
  “cancellator” \(\mathrm{K}\). These produce the following
  characterization of “the concept ‘mechanical
  procedure’”, and he observed that his system
  “substantiates Gödel’s remarks” (above) that
  one should try to find a set of axioms embodying the generally
  accepted properties of the concept of effectiveness (Sieg 2008:
  150).
* Dershowitz and Gurevich (2008) stated three very general axioms,
  treating computations as discrete, deterministic,
  sequentially-evolving structures of states. They called these
  structures “state-transition systems”, and called the
  accepted properties of the concept of effectiveness (Sieg 2008:
  150).
* Dershowitz and Gurevich (2008) stated three very general axioms,
  treating computations as discrete, deterministic,
  sequentially-evolving structures of states. They called these
  structures “state-transition systems”, and called the
  three axioms the “Sequential Postulates”. They also used a
  fourth axiom, stipulating that “Only undeniably computable
  operations are available in initial states” (2008: 306). From
  their four axioms, they proved a proposition they called
version of Church’s thesis does not even mention the key concept
of effective calculability. The entire project of trying to prove
Church’s (or Turing’s) actual thesis has its share of
philosophical difficulties. For example, suppose someone were to lay
down some axioms expressing claims about effective calculability (as
Sieg for instance has done), and suppose it is possible to prove from
these axioms that a function of positive integers is effectively
calculable only if recursive. Church’s thesis would have been
proved from the axioms, but whether the axioms form a satisfactory
account of effective calculability is a *further* question. If
the correct accurate rendering” of the informal concept of
effectiveness.

In 1936, both Church and Turing gave various grounds for accepting
their respective theses. Church argued:

> The fact … that two such widely different and (in the opinion
> of the author) equally natural definitions of effective calculability
> [i.e., in terms of λ-definability and recursion] turn out to be
> *equivalent* adds to the strength of the reasons adduced below
> of the author) equally natural definitions of effective calculability
> [i.e., in terms of λ-definability and recursion] turn out to be
> *equivalent* adds to the strength of the reasons adduced below
> for believing that they constitute as general a characterization of
> this notion as is consistent with the usual intuitive understanding of
> it. (Church 1936a: 346, emphasis added)

Church’s “reasons adduced below” comprised two not
wholly convincing arguments. Both suffered from the same weakness,
discussed in
The equivalence argument may be summed up by saying that the concept
of effective calculability—or the concept of computability
simpliciter—has turned out to be
*formalism-transcendent*, or even “formalism-free”
(Kennedy 2013: 362), in that all these different formal approaches
pick out exactly the *same* class of functions.

Indeed, there is not even a need to distinguish, within any given
formal approach, systems of different orders or types. Gödel
noted in an abstract published in 1936 that the concept
of effective calculability—or the concept of computability
simpliciter—has turned out to be
*formalism-transcendent*, or even “formalism-free”
(Kennedy 2013: 362), in that all these different formal approaches
pick out exactly the *same* class of functions.

Indeed, there is not even a need to distinguish, within any given
formal approach, systems of different orders or types. Gödel
noted in an abstract published in 1936 that the concept
“computable” is *absolute*, in the sense that all
noted in an abstract published in 1936 that the concept
“computable” is *absolute*, in the sense that all
the computable functions are specifiable in one and the same system,
there being no need to introduce a hierarchy of systems of different
orders—as is done, for example, in Tarskian analyses of the
concept “true”, and standardly in the case of the concept
“provable” (Gödel 1936: 24). Ten years later,
commenting on Turing’s work, Gödel emphasized that
“the great importance … [of] Turing’s
computability” is
concept “true”, and standardly in the case of the concept
“provable” (Gödel 1936: 24). Ten years later,
commenting on Turing’s work, Gödel emphasized that
“the great importance … [of] Turing’s
computability” is

> largely due to the fact that with this concept one has for the first
> time succeeded in giving an absolute definition of an interesting
> epistemological notion, i.e., one not depending on the formalism
> chosen. In all other cases treated previously, such as demonstrability
> largely due to the fact that with this concept one has for the first
> time succeeded in giving an absolute definition of an interesting
> epistemological notion, i.e., one not depending on the formalism
> chosen. In all other cases treated previously, such as demonstrability
> or definability, one has been able to define them only relative to a
> given language…. (Gödel 1946: 150)

In his 1952 survey, Kleene also developed Turing’s inductive
argument (1952: 319–320). To summarize:

> time succeeded in giving an absolute definition of an interesting
> epistemological notion, i.e., one not depending on the formalism
> chosen. In all other cases treated previously, such as demonstrability
> or definability, one has been able to define them only relative to a
> given language…. (Gödel 1946: 150)

In his 1952 survey, Kleene also developed Turing’s inductive
argument (1952: 319–320). To summarize:

* Every effectively calculable function that has been investigated
> It is conceivable that all the equivalent notions define a concept
> that is related to, but not identical with, effective computability.
> (Mendelson 1990: 228)

Clearly, what is required is a direct argument for the thesis from
first principles. Turing’s argument I fills this role.

### 4.3 Turing’s argument I {#-43-turings-argument-i}

The logico-philosophical arguments that Turing gave in Section 9 of
fundamental nature of *effective methods*?

Turing’s argument I is a towering landmark and there is now a
sizable literature on these and other questions concerning it. For
more about this important argument see, for starters, Sieg 1994, 2008;
Shagrir 2006; and Copeland & Shagrir 2013.

### 4.4 Turing’s argument II {#-44-turings-argument-ii}

#### 4.4.1 Calculating in a logic {#-441-calculating-in-a-logic}
involves derivability in one or another symbolic logic: The concept of
effective calculability (or of computability) is characterized in
terms of *calculability within the logic* (see
[Section 3.3](#HilbBern)).
Schematically, the characterization is of the form: A function is
effectively calculable (or computable) if each successive value of the
function is derivable within the logic. The next step of the argument
is then to establish that the new characterization (whatever it is) is
equivalent to the old. In Church’s case, this amounts to arguing
that the new characterization is equivalent to his characterization in
new method produces “no more general definition of effective
calculability than that proposed”, i.e., in terms of
recursiveness (1936a: 358).

#### 4.4.3 Turing’s variant {#-443-turings-variant}

Turing’s prefatory remarks to argument II bring out its broad
similarity to Church’s argument. Turing described II as being a
“proof of the equivalence of two definitions”,
adding—“in case the new definition has a greater intuitive
“proof of the equivalence of two definitions”,
adding—“in case the new definition has a greater intuitive
appeal” (1936 [2004: 75]).

Turing’s argument, unlike Church’s, does involve a
specific symbolic logic, namely Hilbert’s first-order predicate
calculus. Argument II hinges on a proposition that can be called

> **Turing’s provability theorem**:
>   
adding—“in case the new definition has a greater intuitive
appeal” (1936 [2004: 75]).

Turing’s argument, unlike Church’s, does involve a
specific symbolic logic, namely Hilbert’s first-order predicate
calculus. Argument II hinges on a proposition that can be called

> **Turing’s provability theorem**:
>   
> Every formula provable in Hilbert’s first-order predicate
alternative definition is also computable according to the
Turing-machine definition (i.e., the digits of the number can be
written out progressively by a Turing machine), and vice versa (Turing
1936 [2004: 78]). In other words, he proved the equivalence of the two
definitions, as promised.

#### 4.4.4 Comparing the Church and Turing arguments {#-444-comparing-the-church-and-turing-arguments}

Returning to Church’s step-by-step argument, there is an air of
jiggery-pokery about it. Church wished to conclude that functions
Turing-machine definition (i.e., the digits of the number can be
written out progressively by a Turing machine), and vice versa (Turing
1936 [2004: 78]). In other words, he proved the equivalence of the two
definitions, as promised.

#### 4.4.4 Comparing the Church and Turing arguments {#-444-comparing-the-church-and-turing-arguments}

Returning to Church’s step-by-step argument, there is an air of
jiggery-pokery about it. Church wished to conclude that functions
“calculable within the logic” are recursive, and, in the
definitions, as promised.

#### 4.4.4 Comparing the Church and Turing arguments {#-444-comparing-the-church-and-turing-arguments}

Returning to Church’s step-by-step argument, there is an air of
jiggery-pokery about it. Church wished to conclude that functions
“calculable within the logic” are recursive, and, in the
course of arguing for this, he found it necessary to assert that each
rule of the logic is a recursive operation, on the basis that each
rule is required to be an effectively calculable operation. In a
logical notation for expressing all such deductions (Turing 1936).

(In fact, the successful execution of *any* string of
instructions can be represented deductively in this
fashion—Kripke has not drawn attention to a feature special to
computation. The instructions do not need to be ones that a computer
can carry out.)

The second step of Kripke’s argument is to appeal to what he
refers to as *Hilbert’s thesis*: this is the thesis that
> fundamentally, appeals to intuition, and for this reason rather
> unsatisfactory mathematically. (Turing 1936 [2004: 74])

Indeed, Turing might have regarded “Hilbert’s
thesis” as itself an example of a proposition that can be
justified only by appeals to intuition.

Turing discussed a thesis closely related to Turing’s thesis,
namely *for every systematic method there is a corresponding
substitution-puzzle* (where “substitution-puzzle”,
defined concept). He said:

> The statement is … one which one does not attempt to prove.
> Propaganda is more appropriate to it than proof, for its status is
> something between a theorem and a definition. (Turing 1954 [2004:
> 588])

Probably Turing would have taken this remark to apply equally to the
thesis (Turing’s thesis) that *for every systematic method
there is a corresponding Turing machine*.
> something between a theorem and a definition. (Turing 1954 [2004:
> 588])

Probably Turing would have taken this remark to apply equally to the
thesis (Turing’s thesis) that *for every systematic method
there is a corresponding Turing machine*.

Turing also said (in handwritten material published in 2004) that the
phrase “systematic method”

definition”, then the definition is presumably Church’s
proposal to “define the notion … of an effectively
calculable function”
([Section 1.5](#MeanCompCompTuriThes))
and the theorem is Turing’s computation theorem
([Section 4.3.5](#TuriTheo)),
i.e., that given Turing’s account of the essential features of
human computation, Turing’s thesis is true. This theorem is
demonstrable, but to prove the thesis itself from the theorem, it
would be necessary to show, with mathematical certainty, that
are of the concept of an effective method: The equivalence of the
analyses bears only on the question of the extent of what is
*humanly* computable, not on the further question whether
functions generatable by *machines* could extend beyond what is
in principle humanly computable.

### 5.3 Watching our words {#-53-watching-our-words}

It may be helpful at this point to survey some standard technical
terminology that could set traps for the unwary.
systems) may illustrate a concept of computation that is wider than
effective computation. Since “equilibrating can be so easily,
reproducibly, and mindlessly accomplished”, Doyle said, we may
“take the operation of equilibrating” to be a
computational operation, even if the functions computable in principle
using Turing-machine operations *plus* equilibrating include
functions that are not computable by an unaided Turing machine (Doyle
2002: 519).

#### 5.3.4 The word “mechanical” {#-534-the-word-mechanical}
obscure the conceptual possibility that not all machine-generatable
functions are Turing-machine computable. The question “Can a
*machine* implement a procedure that is not mechanical?”
may appear self-answering—yet this is what is being asked if
Thesis M and the maximality thesis are questioned.

### 5.4 The strong maximality thesis {#-54-the-strong-maximality-thesis}

The maximality thesis has two interpretations, depending whether the
phrase “can be generated by machine” is taken in the sense
concept of human computation lay at the heart of Turing’s and
Church’s analyses.

The variety of algorithms studied by modern computer science eclipses
the field as it was in Turing’s day. There are now parallel
algorithms, distributed algorithms, interactive algorithms, analog
algorithms, hybrid algorithms, quantum algorithms, enzymatic
algorithms, bacterial foraging algorithms, slime-mold algorithms and
more (see e.g., Gurevich 2012; Copeland & Shagrir 2019). The
universal Turing machine cannot even perform the atomic steps of
Given the extent to which the concept of an algorithm has evolved
since the 1930s—from the step-by-step labors of human computers
to the growth of slime mold—interesting questions arise. Will
the concept continue to evolve? What are the limits, if any, on this
evolution? Could the concept evolve in such that a way that the
algorithmic version of the Church-Turing thesis is no longer
universally true? Returning to Doyle’s suggestions about
equilibrating systems (in
[Section 5.3.3](#BeyoEffe)),
Doyle’s claim is essentially that the operation of
the concept continue to evolve? What are the limits, if any, on this
evolution? Could the concept evolve in such that a way that the
algorithmic version of the Church-Turing thesis is no longer
universally true? Returning to Doyle’s suggestions about
equilibrating systems (in
[Section 5.3.3](#BeyoEffe)),
Doyle’s claim is essentially that the operation of
equilibrating could reasonably be regarded as a basic step of some
effective procedures or algorithms—*whether or not* the
resulting algorithms satisfy the algorithmic version of the
evolution? Could the concept evolve in such that a way that the
algorithmic version of the Church-Turing thesis is no longer
universally true? Returning to Doyle’s suggestions about
equilibrating systems (in
[Section 5.3.3](#BeyoEffe)),
Doyle’s claim is essentially that the operation of
equilibrating could reasonably be regarded as a basic step of some
effective procedures or algorithms—*whether or not* the
resulting algorithms satisfy the algorithmic version of the
Church-Turing thesis. (See Copeland & Shagrir 2019 for further
“something between” a theorem and a definition) ECT is
neither a logico-mathematical theorem nor a definition. If it is true,
then its truth is a consequence of the laws of physics—and it
might not be true. (Although it is trivial if, contrary to a standard
but unproved assumption in computer science, P = NP.)

The second complexity-theoretic version of the thesis involves the
concept of a *probabilistic Turing machine* (due to Rabin &
Scott 1959). Vazirani and Aharonov state the thesis:

neither a logico-mathematical theorem nor a definition. If it is true,
then its truth is a consequence of the laws of physics—and it
might not be true. (Although it is trivial if, contrary to a standard
but unproved assumption in computer science, P = NP.)

The second complexity-theoretic version of the thesis involves the
concept of a *probabilistic Turing machine* (due to Rabin &
Scott 1959). Vazirani and Aharonov state the thesis:

> [T]he extended Church-Turing thesis … asserts that any
concept of a *probabilistic Turing machine* (due to Rabin &
Scott 1959). Vazirani and Aharonov state the thesis:

> [T]he extended Church-Turing thesis … asserts that any
> reasonable computational model can be simulated efficiently by the
> standard model of classical computation, namely, a probabilistic
> Turing machine. (Aharonov & Vazirani 2013: 329)

These two related theses differ considerably from the original
Church-Turing thesis, not least in that both extended theses are
went on to introduce the important concept of a universal quantum
computer, saying (but without proof) that this is “capable of
perfectly simulating every finite, realizable physical system”
(1985: 102).

The following formulation differs in its details from both
Wolfram’s and Deutsch’s theses, but arguably captures the
spirit of both. In view of the Deutsch-Gandy point about continuous
systems, the idea of perfect simulation is replaced by the concept of
simulation *to any desired degree of accuracy*:
systems, the idea of perfect simulation is replaced by the concept of
simulation *to any desired degree of accuracy*:

> **Deutsch-Wolfram Thesis**:
>   
> Every finite physical system can be simulated to any specified degree
> of accuracy by a universal Turing machine. (Copeland & Shagrir
> 2019)

Related physical theses were advanced by Earman 1986, Pour-El and
realism into the concept of a Turing machine, it is—as in
Turing’s case—unknown whether Church would, if queried,
have assented to the
[Deutsch-Wolfram thesis](#deutschwolframthesis)
or any cognate thesis. There seems to be no textual evidence either
way. Church was simply silent about such matters.

> Supplementary Document:
> [The Rise and Fall of the *Entscheidungsproblem*](decision-problem.html).

* Davis, Martin and Wilfried Sieg, 2015, “Conceptual
  Confluence in 1936: Post and Turing”, in *Turing’s
  Revolution*, Giovanni Sommaruga and Thomas Strahm (eds), Cham:
  Birkhäuser, 3–27. doi:10.1007/978-3-319-22156-4\_1
* Dawson, John W., 2006, “Gödel and the Origins of
  Computer Science”, in *Logical Approaches to Computational
  Barriers*, Arnold Beckmann, Ulrich Berger, Benedikt Löwe, and
  John V. Tucker (eds), (Lecture Notes in Computer Science 3988),
  Berlin/Heidelberg: Springer, 133–136.
  doi:10.1007/11780342\_14
  Machine: Conceptual Analysis”, in *Reflections on the
  Foundations of Mathematics: Essays in Honor of Solomon Feferman*,
  Wilfried Sieg, Richard Sommer, and Carolyn Talcott (eds), Urbana, IL:
  Association for Symbolic Logic, 390–409.
* –––, 2008, “Church Without Dogma: Axioms
  for Computability”, in *New Computational Paradigms*, S.
  Barry Cooper, Benedikt Löwe, and Andrea Sorbi (eds), New York,
  NY: Springer New York, 139–152.
  doi:10.1007/978-0-387-68546-5\_7
* Siegelmann, Hava T., 2003, “Neural and Super-Turing

## Key Equations {#-key-equations}

### Fundamental Formulations {#-fundamental-formulations}
formulations of the thesis. A common one is that every effective
computation can be carried out by a Turing machine (i.e., by
Turing’s abstract computing machine, which in its universal form
encapsulates the fundamental logical principles of the stored-program
all-purpose digital computer). Modern reimaginings of the
Church-Turing thesis transform it, extending it to fundamental
physics, complexity theory, exotic algorithms, and cognitive science.
It is important to be aware though that some of the theses nowadays
referred to as the Church-Turing thesis are at best *very*
distant relatives of the thesis advanced by Church and Turing.
could apply this test successfully to any formula of the propositional
calculus—given sufficient time, tenacity, paper, and pencils
(although in practice the test is unworkable for any formula
containing more than a few propositional variables).

### 1.1 Note on terminology {#-11-note-on-terminology}

Statements that there is an effective method for achieving
such-and-such a result are commonly expressed by saying that there is
an effective method for obtaining the values of such-and-such a
(although in practice the test is unworkable for any formula
containing more than a few propositional variables).

### 1.1 Note on terminology {#-11-note-on-terminology}

Statements that there is an effective method for achieving
such-and-such a result are commonly expressed by saying that there is
an effective method for obtaining the values of such-and-such a
mathematical *function*.

mathematical *function*.

For example, that there is an effective method for determining whether
or not any given formula of the propositional calculus is a tautology
(such as the truth-table method) is expressed in function-speak by
saying there is an effective method for obtaining the values of a
function, call it \(T\), whose domain is the set of formulae of the
propositional calculus and whose value for any given formula \(x\),
written \(T(x)\), is 1 or 0 according to whether \(x\) is, or is not,
a tautology.
or not any given formula of the propositional calculus is a tautology
(such as the truth-table method) is expressed in function-speak by
saying there is an effective method for obtaining the values of a
function, call it \(T\), whose domain is the set of formulae of the
propositional calculus and whose value for any given formula \(x\),
written \(T(x)\), is 1 or 0 according to whether \(x\) is, or is not,
a tautology.

### 1.2 Making the informal concept of an effective method precise {#-12-making-the-informal-concept-of-an-effective-method-precise}

function, call it \(T\), whose domain is the set of formulae of the
propositional calculus and whose value for any given formula \(x\),
written \(T(x)\), is 1 or 0 according to whether \(x\) is, or is not,
a tautology.

### 1.2 Making the informal concept of an effective method precise {#-12-making-the-informal-concept-of-an-effective-method-precise}

The notion of an effective method or procedure is an informal one, and
attempts to characterize effectiveness, such as the above, lack rigor,
for the key requirement that the method must demand no insight,
propositional calculus and whose value for any given formula \(x\),
written \(T(x)\), is 1 or 0 according to whether \(x\) is, or is not,
a tautology.

### 1.2 Making the informal concept of an effective method precise {#-12-making-the-informal-concept-of-an-effective-method-precise}

The notion of an effective method or procedure is an informal one, and
attempts to characterize effectiveness, such as the above, lack rigor,
for the key requirement that the method must demand no insight,
intuition or ingenuity is left unexplicated.
each picks out the same set (call it \(S\)) of mathematical functions.
The Church-Turing thesis is the assertion that this set \(S\) contains
*every* function whose values can be obtained by a method or
procedure satisfying the above conditions for effectiveness.

Since it can also be shown that there are no functions in \(S\)
*other than* ones whose values can be obtained by a method
satisfying the above conditions for effectiveness, the Church-Turing
thesis licenses replacing the informal claim “There is an
effective method for obtaining the values of function \(f\)” by
the values of a mathematical function, the function can be computed by
a Turing machine.

The converse claim—amounting to the claim mentioned above, that
there are no functions in \(S\) *other than* ones whose values
can be obtained by an effective method—is easily established,
since a Turing machine program is itself a specification of an
effective method. Without exercising any insight, intuition, or
ingenuity, a human being can work through the instructions in the
program and carry out the required operations.
rigor. The following formulation is one of the most accessible:

> **Turing’s thesis**:
>   
> L.C.M.s [logical computing machines: Turing’s expression for
> Turing machines] can do anything that could be described as
> “rule of thumb” or “purely mechanical”.
> (Turing 1948 [2004: 414])

He adds:
### 1.3 Formulations of Turing’s thesis in terms of numbers {#-13-formulations-of-turings-thesis-in-terms-of-numbers}

In his 1936 paper, which he titled “On Computable Numbers, with
an Application to the *Entscheidungsproblem*”, Turing
wrote:

> Although the subject of this paper is ostensibly the computable
> numbers, it is almost equally easy to define and investigate
> computable functions … I have chosen the computable numbers for
> explicit treatment as involving the least cumbrous technique. (1936
As well as formulations of Turing’s thesis like the one given
above, Turing also formulated his thesis in terms of numbers:

> [T]he “computable numbers” include all numbers which would
> naturally be regarded as computable. (Turing 1936 [2004: 58])

and

> It is my contention that these operations [the operations of an
> L.C.M.] include all those which are used in the computation of a
above, Turing also formulated his thesis in terms of numbers:

> [T]he “computable numbers” include all numbers which would
> naturally be regarded as computable. (Turing 1936 [2004: 58])

and

> It is my contention that these operations [the operations of an
> L.C.M.] include all those which are used in the computation of a
> number. (Turing 1936 [2004: 60])
In the first of these two formulations, Turing is stating that every
number which is able to be calculated by an effective method (that is,
“all numbers which would naturally be regarded as
computable”) is included among the numbers whose decimal
representations can be written out progressively by one or another
Turing machine. In the second, Turing is saying that the operations of
a Turing machine include all those that a human mathematician needs to
use when calculating a number by means of an effective method.

### 1.4 The meaning of “computable” and “computation” in Turing’s thesis {#-14-the-meaning-of-computable-and-computation-in-turings-thesis}
thesis until he saw Turing’s formulation:

> According to a November 29, 1935, letter from Church to me, Gödel
> “regarded as thoroughly unsatisfactory” Church’s
> proposal to use λ-definability as a definition of effective
> calculability. … It seems that only after Turing’s
> formulation appeared did Gödel accept Church’s thesis.
> (Kleene 1981: 59, 61)

Gödel described Turing’s analysis of computability as
> formulation appeared did Gödel accept Church’s thesis.
> (Kleene 1981: 59, 61)

Gödel described Turing’s analysis of computability as
“most satisfactory” and “correct … beyond any
doubt” (Gödel 1951: 304 and 193?: 168). He remarked:

> We had not perceived the sharp concept of mechanical procedures
> sharply before Turing, who brought us to the right perspective.
> (Quoted in Wang 1974: 85)
deciding whether or not a given formula—any formula—is
provable in the calculus. (Here “provable” means that the
formula can be derived, step by logical step, from the axioms and
definitions of the calculus, using only the rules of the calculus.)
For example, if such a method for the classical propositional calculus
is used to test the formula \(A \rightarrow A\) (\(A\) implies \(A\)),
the output will be “Yes, provable”, and if the
contradiction \(A \amp \neg A\) is tested, the output will be
“Not provable”. Such a method is called a *decision
method* or *decision procedure*.
formula can be derived, step by logical step, from the axioms and
definitions of the calculus, using only the rules of the calculus.)
For example, if such a method for the classical propositional calculus
is used to test the formula \(A \rightarrow A\) (\(A\) implies \(A\)),
the output will be “Yes, provable”, and if the
contradiction \(A \amp \neg A\) is tested, the output will be
“Not provable”. Such a method is called a *decision
method* or *decision procedure*.

Church and Turing took on the *Entscheidungsproblem* for a
is used to test the formula \(A \rightarrow A\) (\(A\) implies \(A\)),
the output will be “Yes, provable”, and if the
contradiction \(A \amp \neg A\) is tested, the output will be
“Not provable”. Such a method is called a *decision
method* or *decision procedure*.

Church and Turing took on the *Entscheidungsproblem* for a
fundamentally important logical system called the (first-order)
*functional calculus*. The functional calculus consists of
standard propositional logic plus standard quantifier logic. The
minds of early twentieth-century mathematical logic, including
Gödel, Herbrand, Post, Ramsey, and Hilbert and his assistants
Ackermann, Behmann, Bernays, and Schönfinkel. Herbrand described
the *Entscheidungsproblem* as “the most general problem
of mathematics” (Herbrand 1931b: 187). But it was Hilbert who
had brought the *Entscheidungsproblem* for the functional
calculus into the limelight. In 1928, he and Ackermann called it
“das Hauptproblem der mathematischen
Logik”—“the main problem of mathematical
logic” (Hilbert & Ackermann 1928: 77).
Logik”—“the main problem of mathematical
logic” (Hilbert & Ackermann 1928: 77).

Hilbert knew that the propositional calculus (which is a fragment of
the functional calculus) is decidable, having found with Bernays a
decision procedure based on what are called “normal forms”
(Bernays 1918; Behmann 1922; Hilbert & Ackermann 1928: 9–12;
Zach 1999), and he also knew from the work of Löwenheim that the
*monadic* functional calculus is decidable (Löwenheim
1915). (The monadic functional calculus is the fragment involving only
The challenge, the main problem of mathematical logic, was to find it.
As he and Ackermann wrote in 1928, in their famous book
*Grundzüge der Theoretischen Logik* (Principles of
Mathematical Logic):

> [I]t is to be expected that a systematic, so to speak computational
> treatment of the logical formulae is possible …. (Hilbert &
> Ackermann 1928: 72)

However, their expectations were frustrated by the Church-Turing
Mathematical Logic):

> [I]t is to be expected that a systematic, so to speak computational
> treatment of the logical formulae is possible …. (Hilbert &
> Ackermann 1928: 72)

However, their expectations were frustrated by the Church-Turing
result of 1936. Hilbert and Ackermann excised the quoted statement
from a revised edition of their book. Published in 1938, the new
edition was considerably watered down to take account of
> treatment of the logical formulae is possible …. (Hilbert &
> Ackermann 1928: 72)

However, their expectations were frustrated by the Church-Turing
result of 1936. Hilbert and Ackermann excised the quoted statement
from a revised edition of their book. Published in 1938, the new
edition was considerably watered down to take account of
Turing’s and Church’s monumental result.

Hilbert knew, of course, that some mathematical problems have
Hilbert knew, of course, that some mathematical problems have
*no* solution, for example the problem of finding a finite
binary numeral \(n\) (or unary numeral, in Hilbert’s version of
the problem) such that \(n^2 = 2\) (Hilbert 1926: 179). He was
nevertheless very fond of saying that *every mathematical problem
can be solved*, and by this he meant that

> every definite mathematical problem must necessarily be susceptible of
> an exact settlement, either in the form of an actual answer to the
> question asked, or by the proof of the impossibility of its solution
nevertheless very fond of saying that *every mathematical problem
can be solved*, and by this he meant that

> every definite mathematical problem must necessarily be susceptible of
> an exact settlement, either in the form of an actual answer to the
> question asked, or by the proof of the impossibility of its solution
> and therewith the necessary failure of all attempts. (Hilbert 1900:
> 261 [trans. 1902: 444])

It seems never to have crossed his mind that his “Hauptproblem
> every definite mathematical problem must necessarily be susceptible of
> an exact settlement, either in the form of an actual answer to the
> question asked, or by the proof of the impossibility of its solution
> and therewith the necessary failure of all attempts. (Hilbert 1900:
> 261 [trans. 1902: 444])

It seems never to have crossed his mind that his “Hauptproblem
der mathematischen Logik” falls into the second of these two
categories—until, that is, Church and Turing unexpectedly proved
“the impossibility of its solution”.
mathematical) statement \(S\), and the machine would eventually
respond (correctly) with either “\(S\) is true” or
“\(S\) is false”. As the groundbreaking developments in
1936 by Church and Turing made clear, if the *ars inveniendi*
is supposed to work by means of an effective method, then there can be
no universal *ars inveniendi*—and not even an *ars
inveniendi* that is restricted to all mathematical statements,
since these include statements of the form “\(p\) is
provable”, or even to all purely logical statements.

inveniendi* that is restricted to all mathematical statements,
since these include statements of the form “\(p\) is
provable”, or even to all purely logical statements.

### 2.3 Logic machines {#-23-logic-machines}

The modern concept of a decision method for a logical calculus did not
develop until the twentieth century. But earlier logicians, including
Leibniz, certainly had the concept of a method that is
*mechanical* in the literal sense that it could be carried out
inputting logical formulae. The formulae were drawn from a syllogistic
calculus involving four positive terms, such as “iron” and
“metal” (Jevons 1870). Turing’s colleague Mays, who
himself designed an influential electrical logic machine (Mays &
Prinz 1950), described the logic piano as “the first working
machine to perform logical inference without the intervention of human
agency” (Mays & Henry 1951: 4).

The logic piano implemented a method for determining which
combinations drawn from eight terms—the four positive terms and
etc.)—were consistent with the inputted formulae and which not
(although in fact not all consistent combinations were taken into
account). The machine displayed the consistent formulae by means of
lettered strips of wood, with upper-case letters representing positive
terms and lower-case negative. Jevons exhibited the logic piano in
Manchester at Owens College, now Manchester University, where he was
professor of logic (Mays & Henry 1953: 503). His piano, Jevons
claimed with considerable exaggeration, made it “evident that
mechanism is capable of replacing for the most part the action of
thought required in the performance of logical deduction”
account). The machine displayed the consistent formulae by means of
lettered strips of wood, with upper-case letters representing positive
terms and lower-case negative. Jevons exhibited the logic piano in
Manchester at Owens College, now Manchester University, where he was
professor of logic (Mays & Henry 1953: 503). His piano, Jevons
claimed with considerable exaggeration, made it “evident that
mechanism is capable of replacing for the most part the action of
thought required in the performance of logical deduction”
(Jevons 1870: 517).

result” (Quine 1950: 74). Not all formulae of the functional
calculus are Venn-diagrammable, and Venn’s original method is
limited to testing syllogisms. In the twentieth century, Massey showed
that Venn’s method can be stretched to give a decision procedure
for the monadic functional calculus (Massey 1966).

Venn, like Jevons, was well aware of the concept of a literally
mechanical method. He pointed out that diagrammatic methods such as
his “readily lend themselves to mechanical performance”
(Venn 1880: 15). Venn went on to describe what he called a
term-combinations consistent with the inputted formulae. A lettered
plate with sixteen mechanical dials was used to display the
combinations.

### 2.4 Peirce {#-24-peirce}

In 1886, in a letter to Marquand, Peirce famously suggested that
Marquand consider an electrical version of his machine, and he
sketched simple switching circuits implementing (what we would now
call) an AND-gate and an OR-gate—possibly the earliest proposal
mathematical problems”. Much later, Church discovered a detailed
diagram of an electrical relay-based form of Marquand’s machine
among Marquand’s papers at Princeton (reproduced in Ketner &
Stewart 1984: 200). Whoever worked out the design in this
diagram—Marquand, Peirce, or an unknown third person—has a
claim to be an important early pioneer of electromechanical
computing.

Peirce, with his interest in logic machines, seems to have been the
first to consider the decision problem in roughly the form in which
diagrammatic formulation of the propositional calculus, and his system
of *beta-graphs* is a version of the first-order functional
calculus (Peirce 1903a; Roberts 1973). Roberts (1973) proved that the
beta-graphs system contains the axioms and rules of Quine’s 1951
formulation of the first-order functional calculus, in which only
closed formulae are asserted (Quine 1951: 88).

Peirce anticipated the concept of a decision method in his extensive
notes for a series of lectures he delivered in Boston in 1903. There
he developed a method (Peirce 1903b,c) that, if applied to any given
formulation of the first-order functional calculus, in which only
closed formulae are asserted (Quine 1951: 88).

Peirce anticipated the concept of a decision method in his extensive
notes for a series of lectures he delivered in Boston in 1903. There
he developed a method (Peirce 1903b,c) that, if applied to any given
formula of the propositional calculus, would, he said,
“determine” (or “positively ascertain”)
whether the alpha-graphs system demonstrates that the formula is
satisfiable (is “alpha-possible”, in Peirce’s
closed formulae are asserted (Quine 1951: 88).

Peirce anticipated the concept of a decision method in his extensive
notes for a series of lectures he delivered in Boston in 1903. There
he developed a method (Peirce 1903b,c) that, if applied to any given
formula of the propositional calculus, would, he said,
“determine” (or “positively ascertain”)
whether the alpha-graphs system demonstrates that the formula is
satisfiable (is “alpha-possible”, in Peirce’s
terminology), or whether, on the other hand, the system demonstrates
formula of the propositional calculus, would, he said,
“determine” (or “positively ascertain”)
whether the alpha-graphs system demonstrates that the formula is
satisfiable (is “alpha-possible”, in Peirce’s
terminology), or whether, on the other hand, the system demonstrates
that it is unsatisfiable (“alpha-impossible”). (See the
supplement on
[The Rise and Fall of the *Entschedungsproblem*](decision-problem.html)
for an explanation of “satisfiable”.) Peirce said his
method “is such a comprehensive routine that it would be easy to
whether the alpha-graphs system demonstrates that the formula is
satisfiable (is “alpha-possible”, in Peirce’s
terminology), or whether, on the other hand, the system demonstrates
that it is unsatisfiable (“alpha-impossible”). (See the
supplement on
[The Rise and Fall of the *Entschedungsproblem*](decision-problem.html)
for an explanation of “satisfiable”.) Peirce said his
method “is such a comprehensive routine that it would be easy to
define a machine that would perform it”—although the
“complexity of the case”, he continued, “renders any
> are inadequate to the performance of mathematical deductions. There
> is, however, a modern Exact Logic which, although yet in its infancy,
> is already far enough advanced to render it a mere question of expense
> to construct a machine that would grind out all the known theorems of
> arithmetic and advance that science still more rapidly than it is now
> progressing. (Peirce *n.d.*, quoted in Stjernfelt 2022)

Here Peirce seems to be asserting—quite correctly—that a
machine can be devised to grind out all the theorems of
Dedekind’s (1888) axiomatisation of arithmetic (which consisted
As to whether *all* mathematical reasoning can be performed by
a machine, as Leibniz seems to have thought, Peirce was fiercely
skeptical. He formulated the hypothesis that, in the future,
mathematical reasoning

> might conceivably be left to a machine—some Babbage’s
> analytical engine or some logical machine. (Peirce 1908: 434)

However, he placed this hypothesis alongside others he deemed
“logical heresies”, calling it “malignant”
skeptical. He formulated the hypothesis that, in the future,
mathematical reasoning

> might conceivably be left to a machine—some Babbage’s
> analytical engine or some logical machine. (Peirce 1908: 434)

However, he placed this hypothesis alongside others he deemed
“logical heresies”, calling it “malignant”
(ibid.). His skeptical attitude, if perhaps not his reasons for it,
was arguably vindicated by Turing’s subsequent results (Turing
mathematical reasoning

> might conceivably be left to a machine—some Babbage’s
> analytical engine or some logical machine. (Peirce 1908: 434)

However, he placed this hypothesis alongside others he deemed
“logical heresies”, calling it “malignant”
(ibid.). His skeptical attitude, if perhaps not his reasons for it,
was arguably vindicated by Turing’s subsequent results (Turing
1936, 1939). But before that, a quite different view of matters took
lecture he gave in Zurich in 1917, to the Swiss Mathematical Society,
he emphasized the need to study the concept of “decidability by
a finite number of operations”,
saying—accurately—that this would be “an important
new field of research to develop” (Hilbert 1917: 415). The
lecture considered a number of what he called “most challenging
epistemological problems of a specifically mathematical
character” (1917: 412). Pre-eminent among these was the
“problem of the decidability [*Entscheidbarkeit*] of a
mathematical question” because the problem “touches
epistemological problems of a specifically mathematical
character” (1917: 412). Pre-eminent among these was the
“problem of the decidability [*Entscheidbarkeit*] of a
mathematical question” because the problem “touches
profoundly upon the nature of mathematical thinking” (1917:
413).

Hilbert and his Göttingen group looked back on Leibniz as the
originator of their approach to logic and the foundations of
mathematics. Behmann, a prominent member of the group, said that
mathematical question” because the problem “touches
profoundly upon the nature of mathematical thinking” (1917:
413).

Hilbert and his Göttingen group looked back on Leibniz as the
originator of their approach to logic and the foundations of
mathematics. Behmann, a prominent member of the group, said that
Leibniz had anticipated modern symbolic logic (Behmann 1921:
4–5). Leibniz’s hypothesized “universal
characteristic” or universal symbolistic was a universal
profoundly upon the nature of mathematical thinking” (1917:
413).

Hilbert and his Göttingen group looked back on Leibniz as the
originator of their approach to logic and the foundations of
mathematics. Behmann, a prominent member of the group, said that
Leibniz had anticipated modern symbolic logic (Behmann 1921:
4–5). Leibniz’s hypothesized “universal
characteristic” or universal symbolistic was a universal
symbolic language, in conception akin to languages used in
mathematical logic and computer science today. Hilbert and Ackermann
acknowledged Leibniz’s influence on the first page of their
*Grundzüge der Theoretischen Logik*, saying “The
idea of a mathematical logic was first put into a clear form by
Leibniz” (Hilbert & Ackermann 1928: 1). Cassirer said that
in Hilbert’s work “the fundamental idea of Leibniz’s
‘universal characteristic’ is taken up anew and attains a
succinct and precise expression” (Cassirer 1929: 440). It was in
the writings of the Göttingen group that Leibniz’s idea of
an effective method for answering any specified mathematical or
idea of a mathematical logic was first put into a clear form by
Leibniz” (Hilbert & Ackermann 1928: 1). Cassirer said that
in Hilbert’s work “the fundamental idea of Leibniz’s
‘universal characteristic’ is taken up anew and attains a
succinct and precise expression” (Cassirer 1929: 440). It was in
the writings of the Göttingen group that Leibniz’s idea of
an effective method for answering any specified mathematical or
scientific question found its fullest development (see further the
supplement on
[The Rise and Fall of the *Entscheidungsproblem*](decision-problem.html)).
an effective method for answering any specified mathematical or
scientific question found its fullest development (see further the
supplement on
[The Rise and Fall of the *Entscheidungsproblem*](decision-problem.html)).

Hilbert’s earliest publication to mention what we would now call
a decision problem is his 1899 book *Grundlagen der Geometrie*
[Foundations of Geometry]. He said that in the course of his
investigations of Euclidean geometry he was

> Given a diophantine equation with any number of unknown quantities and
> with rational integral numerical coefficients: *To devise a process
> according to which it can be determined by a finite number of
> operations whether the equation is solvable in rational integers*.
> (Hilbert 1900: 276 [trans. 1902: 458])

The *Entscheidungsproblem* was coming into even clearer focus
by the time Hilbert’s student Behmann published a landmark
article in 1922, “Contributions to the Algebra of Logic, in
particular to the *Entscheidungsproblem*”. It was
> operations whether the equation is solvable in rational integers*.
> (Hilbert 1900: 276 [trans. 1902: 458])

The *Entscheidungsproblem* was coming into even clearer focus
by the time Hilbert’s student Behmann published a landmark
article in 1922, “Contributions to the Algebra of Logic, in
particular to the *Entscheidungsproblem*”. It was
probably Behmann who coined the term
“*Entscheidungsproblem*” (Mancosu & Zach 2015:
166–167). In a 1921 lecture to the Göttingen group, Behmann
> If a logical or mathematical statement is given, the required
> procedure should give complete instructions for determining whether
> the statement is correct or false by a deterministic calculation after
> finitely many steps. The problem thus formulated I want to call the
> *allgemeine Entscheidungsproblem* [general decision problem].
> (Behmann 1921: 6 [trans. 2015: 176])

Peirce, as we saw, spoke of a procedure’s forming “such a
comprehensive routine that it would be easy to define a machine that
would perform it”. His work was well-known in Göttingen:
> finitely many steps. The problem thus formulated I want to call the
> *allgemeine Entscheidungsproblem* [general decision problem].
> (Behmann 1921: 6 [trans. 2015: 176])

Peirce, as we saw, spoke of a procedure’s forming “such a
comprehensive routine that it would be easy to define a machine that
would perform it”. His work was well-known in Göttingen:
Hilbert and Ackermann said that Peirce “especially”, and
also Jevons, had “enriched the young science” of
mathematical logic (1928: 1). Like Peirce, Behmann used the concept of
mathematical logic (1928: 1). Like Peirce, Behmann used the concept of
a machine to clarify the nature of the *Entscheidungsproblem*.
“It is essential to the character” of the problem, Behmann
said, that “only entirely mechanical calculation according to
given instructions” is involved. The decision whether the
statement is true or false becomes “a mere exercise in
computation”; there is “an elimination of thinking in
favor of mechanical calculation”. Behmann continued:

> One might, if one wanted to, speak of mechanical or machine-like
given by Newman. Newman, a mathematical logician and topologist, was
very familiar with the ideas emanating from Göttingen. As early
as 1923 he gave a left-field discussion of some of Hilbert’s
ideas, himself proposing an approach to the foundations of mathematics
that, while radical and new, nevertheless had a strongly Hilbertian
flavor (Newman 1923). In 1928, Newman attended an international
congress of mathematicians in the Italian city of Bologna, where
Hilbert talked about the *Entscheidungsproblem* while lecturing
on his proof theory (Hilbert 1930a; Zanichelli 1929). Hilbert’s
leading works in mathematical logic—Hilbert and Ackermann (1928)
leading works in mathematical logic—Hilbert and Ackermann (1928)
and Hilbert and Bernays (1934)—were both recommended reading for
Newman’s own lectures on the Foundations of Mathematics
(Smithies 1934; Copeland and Fan 2022).

Speaking in a tape-recorded interview about Turing’s engagement
with the *Entscheidungsproblem*, Newman said “I believe
it all started because he attended a lecture of mine on foundations of
mathematics and logic”:

1964)—presented a series of results to the American Mathematical
Society not long after his return to Harvard, in effect solving a
number of special cases of the *Entscheidungsproblem* (Langford
1926a, 1927).

The Cambridge logician Ramsey, like Turing a Fellow of King’s
College, also worked on the *Entscheidungsproblem* in the
latter part of the 1920s. He died in 1930 (the year before Turing
arrived in Cambridge as an undergraduate), but not before completing a
key paper solving the *Entscheidungsproblem* in special cases
> which enabled us to say whether any given formula was demonstrable or
> not. (Hardy 1929: 16)

Hardy foresaw what Turing, and Church, would soon prove, telling his
audience that such a system of rules “is not to be
expected”.

What Turing showed is that there will never be, and can never be, a
computing machine satisfying the following specification: When the
user types in a formula—any formula—of the functional
user types in a formula—any formula—of the functional
calculus, the machine carries out a finite number of steps and then
outputs the correct answer, either “This formula is provable in
the functional calculus” or “This formula is not provable
in the functional calculus”, as the case may be. Given,
therefore, Turing’s thesis that *if an effective method
exists then it can be carried out by one of his machines*, it
follows that there is no effective method for deciding the full
first-order functional calculus.

outputs the correct answer, either “This formula is provable in
the functional calculus” or “This formula is not provable
in the functional calculus”, as the case may be. Given,
therefore, Turing’s thesis that *if an effective method
exists then it can be carried out by one of his machines*, it
follows that there is no effective method for deciding the full
first-order functional calculus.

## 3. Other Approaches to Computability {#-3-other-approaches-to-computability}

the functional calculus” or “This formula is not provable
in the functional calculus”, as the case may be. Given,
therefore, Turing’s thesis that *if an effective method
exists then it can be carried out by one of his machines*, it
follows that there is no effective method for deciding the full
first-order functional calculus.

## 3. Other Approaches to Computability {#-3-other-approaches-to-computability}

Turing and Church were certainly not the only people to tackle the
> to be any mechanical procedure for producing formulas, called provable
> formulas. (Gödel 1965a: 71–72)

Armed with this definition, incompleteness can, Gödel said,
“be proved rigorously for *every* consistent formal
system containing a certain amount of finitary number theory”
(1965a: 71).

### 3.2 Post {#-32-post}

> formulas. (Gödel 1965a: 71–72)

Armed with this definition, incompleteness can, Gödel said,
“be proved rigorously for *every* consistent formal
system containing a certain amount of finitary number theory”
(1965a: 71).

### 3.2 Post {#-32-post}

By 1936, Post had arrived independently at an analysis of
an *equational calculus*, reminiscent of a calculus that
Gödel had detailed in lectures he gave in Princeton in 1934
(Gödel 1934). The theorems of an equational calculus are (as the
name says) *equations*—for example \(2^3 = 8\) and \(x^2
+ 1 = x(x + 1) - (x - 1),\) or in general \(\mathrm{f}(m) = n.\) The
Hilbert-Bernays equational calculus contains no logical symbols (such
as negation, conjunction, implication, or quantifiers), and every
formula is simply an equation between terms. Three types of equation
are permitted as the initial formulae (or premisses) of deductions in
the system; and the system is required to satisfy three general
(Gödel 1934). The theorems of an equational calculus are (as the
name says) *equations*—for example \(2^3 = 8\) and \(x^2
+ 1 = x(x + 1) - (x - 1),\) or in general \(\mathrm{f}(m) = n.\) The
Hilbert-Bernays equational calculus contains no logical symbols (such
as negation, conjunction, implication, or quantifiers), and every
formula is simply an equation between terms. Three types of equation
are permitted as the initial formulae (or premisses) of deductions in
the system; and the system is required to satisfy three general
conditions that Hilbert and Bernays called “recursivity
conditions”. The rules of the calculus concern substitutions
name says) *equations*—for example \(2^3 = 8\) and \(x^2
+ 1 = x(x + 1) - (x - 1),\) or in general \(\mathrm{f}(m) = n.\) The
Hilbert-Bernays equational calculus contains no logical symbols (such
as negation, conjunction, implication, or quantifiers), and every
formula is simply an equation between terms. Three types of equation
are permitted as the initial formulae (or premisses) of deductions in
the system; and the system is required to satisfy three general
conditions that Hilbert and Bernays called “recursivity
conditions”. The rules of the calculus concern substitutions
within equations and are very simple, allowing steps such as:
Hilbert-Bernays equational calculus contains no logical symbols (such
as negation, conjunction, implication, or quantifiers), and every
formula is simply an equation between terms. Three types of equation
are permitted as the initial formulae (or premisses) of deductions in
the system; and the system is required to satisfy three general
conditions that Hilbert and Bernays called “recursivity
conditions”. The rules of the calculus concern substitutions
within equations and are very simple, allowing steps such as:

\[ a = b, f(a) \vdash f(b) \]
formula is simply an equation between terms. Three types of equation
are permitted as the initial formulae (or premisses) of deductions in
the system; and the system is required to satisfy three general
conditions that Hilbert and Bernays called “recursivity
conditions”. The rules of the calculus concern substitutions
within equations and are very simple, allowing steps such as:

\[ a = b, f(a) \vdash f(b) \]

On the basis of this calculus (which they called \(Z^0\)) Hilbert and
are permitted as the initial formulae (or premisses) of deductions in
the system; and the system is required to satisfy three general
conditions that Hilbert and Bernays called “recursivity
conditions”. The rules of the calculus concern substitutions
within equations and are very simple, allowing steps such as:

\[ a = b, f(a) \vdash f(b) \]

On the basis of this calculus (which they called \(Z^0\)) Hilbert and
Bernays established an equivalence result: The numerical functions
within equations and are very simple, allowing steps such as:

\[ a = b, f(a) \vdash f(b) \]

On the basis of this calculus (which they called \(Z^0\)) Hilbert and
Bernays established an equivalence result: The numerical functions
that are capable of rule-governed evaluation coincide with the
(primitive) recursive functions (1939: 403 and 393*n*).

It is perhaps unsurprising that Hilbert, the founder of proof theory,
Moving on a few years, a meeting on *The Prospects for Mathematical
Logic in the Twenty-First Century*, held at the turn of the
millennium, included the following among leading open problems:

> “Prove” the Church-Turing thesis by finding intuitively
> obvious or at least clearly acceptable properties of computation that
> suffice to guarantee that any function so computed is recursive [and
> therefore can be computed by a Turing machine]. (Shore in Buss et al.
> 2001: 174–175)

  mechanical devices*. (He formulated the axioms in terms of
  hereditarily finite sets.) Gandy was then able to prove that every
  device satisfying these axioms can be simulated by a Turing machine:
  Discrete deterministic mechanical devices, even massively parallel
  ones, are no more powerful than Turing machines, in the sense that
  whatever computations such a device is able to perform can also be
  done by the universal Turing machine. (For more on Gandy’s
  analysis, see
  [Section 6.4.2](#GandArgu).)
* Engeler axiomatized the concept of an algorithmic function by using
> Every formula provable in Hilbert’s first-order predicate
> calculus can be proved by the universal Turing machine. (See Turing
> 1936 [2004: 77].)

The alternative method considered by Turing (which is similar to
Church’s) characterizes a computable number (or sequence) in
terms of statements each of which supplies the next digit of the
number (or sequence). The number (sequence) is said to be computable
if each such statement is provable in Hilbert’s calculus (the
idea being that, if this is so, then Hilbert’s calculus may be
formulae of the calculus”, so making it indubitable that
functions calculable in the logic are Turing-machine computable
(Turing 1936 [2004: 77]). For this reason, Turing’s argument II
is to be preferred to Church’s step-by-step argument.

### 4.5 Kripke’s version of argument II {#-45-kripkes-version-of-argument-ii}

A significant recent contribution to the area has been made by Kripke
(2013). A conventional view of the status of the Church-Turing thesis
is that, while “very considerable intuitive evidence” has
issue to be itself susceptible to mathematical treatment”
(Kripke 2013: 77). Kleene gave an early expression of this now
conventional view:

> Since our original notion of effective calculability of a function
> … is a somewhat vague intuitive one, the thesis cannot be
> proved. … While we cannot prove Church’s thesis, since
> its role is to delimit precisely an hitherto vaguely conceived
> totality, we require evidence …. (Kleene 1952: 318)

contrary, the Church-Turing thesis is susceptible to mathematical
proof. Furthermore, he canvasses the idea that Turing himself sketched
an argument that serves to prove the thesis.

Kripke attempts to build a mathematical demonstration of the
Church-Turing thesis around Turing’s argument II. He claims that
his demonstration is “very close” to Turing’s
(Kripke 2013: 80). However, this is debatable, since, in its detail,
the Kripke argument differs considerably from argument II. But one can
at least say that Kripke’s argument was inspired by
Kripke attempts to build a mathematical demonstration of the
Church-Turing thesis around Turing’s argument II. He claims that
his demonstration is “very close” to Turing’s
(Kripke 2013: 80). However, this is debatable, since, in its detail,
the Kripke argument differs considerably from argument II. But one can
at least say that Kripke’s argument was inspired by
Turing’s argument II, and belongs in Kleene’s category
“D” (along with II and Church’s step-by-step
argument).

> [A] computation is a special form of mathematical argument. One is
> given a set of instructions, and the steps in the computation are
> supposed to follow—follow deductively—from the
> instructions as given. *So a computation is just another
> mathematical deduction, albeit one of a very specialized form*.
> (Kripke 2013: 80)

The following two-line program in pseudo-code illustrates
Kripke’s claim. The symbol “\(\rightarrow\)” is read
“becomes”, and “=” as usual means identity.
> mathematical deduction, albeit one of a very specialized form*.
> (Kripke 2013: 80)

The following two-line program in pseudo-code illustrates
Kripke’s claim. The symbol “\(\rightarrow\)” is read
“becomes”, and “=” as usual means identity.
The first instruction in the program is \(r \rightarrow 2\). This
tells the computer to place the value 2 in storage location \(r\)
(assumed to be initially empty). The second instruction \(r
\rightarrow r + 3\) tells the computer to add 3 to the content of
the steps of any mathematical argument can be expressed “in a
language based on first-order logic (with identity)” (Kripke
2013: 81). The practice of calling this claim “Hilbert’s
thesis” originated in Barwise (1977: 41), but it should be noted
that since Hilbert regarded second-order logic as indispensable (see,
e.g., Hilbert & Ackermann 1928: 86), the name
“Hilbert’s thesis” is potentially misleading.

Applying “Hilbert’s thesis” to Kripke’s above
quoted claim that “a computation is just another mathematical
quoted claim that “a computation is just another mathematical
deduction” (2013: 80) yields:

> every (human) computation can be formalized as a valid deduction
> couched in the language of first-order predicate calculus with
> identity.

Now, applying Gödel’s completeness theorem to this yields
in turn:

> well-known mathematical premises, or premises concerning numbers that
> are supplied to the computer at the start of the computation).

Finally, applying Turing’s provability theorem to this
intermediate conclusion yields the Church-Turing thesis:

> every (human) computation can be done by Turing machine.

### 4.6 Turing on the status of the thesis {#-46-turing-on-the-status-of-the-thesis}

Church-Turing thesis is susceptible to mathematical proof (Dershowitz
& Gurevich 2008). They offer “a proof of Church’s
Thesis, as Gödel and others suggested may be possible”
(2008: 299), and they add:

> In a similar way, but with a different set of basic operations, one
> can prove Turing’s Thesis, … . (Dershowitz & Gurevich
> 2008: 299)

Yet Turing’s own view of the status of his thesis is very
According to Turing, his thesis is not susceptible to mathematical
proof. He did not consider either argument I or argument II to be a
mathematical demonstration of his thesis: he asserted that I and II,
and indeed “[a]ll arguments which can be given” for the
thesis, are

> fundamentally, appeals to intuition, and for this reason rather
> unsatisfactory mathematically. (Turing 1936 [2004: 74])

Indeed, Turing might have regarded “Hilbert’s
mathematical demonstration of his thesis: he asserted that I and II,
and indeed “[a]ll arguments which can be given” for the
thesis, are

> fundamentally, appeals to intuition, and for this reason rather
> unsatisfactory mathematically. (Turing 1936 [2004: 74])

Indeed, Turing might have regarded “Hilbert’s
thesis” as itself an example of a proposition that can be
justified only by appeals to intuition.
> unsatisfactory mathematically. (Turing 1936 [2004: 74])

Indeed, Turing might have regarded “Hilbert’s
thesis” as itself an example of a proposition that can be
justified only by appeals to intuition.

Turing discussed a thesis closely related to Turing’s thesis,
namely *for every systematic method there is a corresponding
substitution-puzzle* (where “substitution-puzzle”,
like “computable by Turing machine”, is a rigorously
“vegetable”, and unlike mathematically precise terms such
as “λ-definable”, “Turing-machine
computable”, and “substitution-puzzle”. Kleene
claimed that, since terms like “systematic method” and
“effectively calculable” are not exact, theses involving
them cannot be proved (op. cit.). Turing however did not voice a
similar argument (perhaps because he saw a difficulty). The fact that
the term “systematic method” is inexact is *not*
enough to show that there could be no mathematically acceptable proof
of a thesis involving the term. Mendelson gave a graphic statement of
enough to show that there could be no mathematically acceptable proof
of a thesis involving the term. Mendelson gave a graphic statement of
this point, writing about what is called above “*the converse
of Church’s thesis*”
([Section 1.5](#MeanCompCompTuriThes)):

> The assumption that a proof connecting intuitive and precise
> mathematical notions is impossible is patently false. In fact, half of
> CT (the “easier” half), the assertion that all
> partial-recursive functions are effectively computable, is
> mathematical notions is impossible is patently false. In fact, half of
> CT (the “easier” half), the assertion that all
> partial-recursive functions are effectively computable, is
> acknowledged to be obvious in all textbooks in recursion theory. A
> straightforward argument can be given for it…. This simple
> argument is as clear a proof as I have seen in mathematics, and it is
> a proof in spite of the fact that it involves the intuitive notion of
> effective computability. (Mendelson 1990: 232–233)

Yet the point that the “intuitive” nature of some of its
would be necessary to show, with mathematical certainty, that
Turing’s account of the essential features of human computation
is correct. So far, no one has done this. Propaganda does seem more
appropriate than proof.

## 5. The Church-Turing Thesis and the Limits of Machines {#-5-the-church-turing-thesis-and-the-limits-of-machines}

### 5.1 Two distinct theses {#-51-two-distinct-theses}

Can the universal Turing machine perfectly simulate the behavior of
> That there exists a most general formulation of machine and that it
> leads to a unique set of input-output functions has come to be called
> *Church’s thesis*. (Newell 1980: 150)

Yet the Church-Turing thesis is a thesis about the extent of
*effective* methods (therein lies its mathematical importance).
Putting this another way, the thesis concerns what a *human
being* can achieve when calculating by rote, using paper and
pencil (absent contingencies such as boredom, death, or insufficiency
of paper). What a human rote-worker can achieve, and what a machine
*effective* methods (therein lies its mathematical importance).
Putting this another way, the thesis concerns what a *human
being* can achieve when calculating by rote, using paper and
pencil (absent contingencies such as boredom, death, or insufficiency
of paper). What a human rote-worker can achieve, and what a machine
can achieve, may be different.

Gandy was perhaps the first to distinguish explicitly between
Turing’s thesis and the very different proposition that
*whatever can be calculated by a machine can be calculated by a
> all attempts to … formulate … general notions of
> mechanism … lead to classes of machines that are equivalent in
> that they encompass *in toto* exactly the same set of
> input-output functions. (Newell 1980: 150)

The various equivalent analyses, said Newell, constitute a

> large zoo of different formulations of maximal classes of machines.
> (ibid.)

> large zoo of different formulations of maximal classes of machines.
> (ibid.)

Arguably there is a fallacy here. The analyses Newell is discussing
are of the concept of an effective method: The equivalence of the
analyses bears only on the question of the extent of what is
*humanly* computable, not on the further question whether
functions generatable by *machines* could extend beyond what is
in principle humanly computable.

fact formulate it. The Halting Problem originated with Davis in the
early 1950s (Davis 1958: 70).)

#### 5.3.3 Beyond effective {#-533-beyond-effective}

Some authors use phrases such as “computation in a broad
sense”, or simply “computation”, to refer to
computation of a type that potentially transcends effective
computation (e.g., Doyle 2002; MacLennan 2003; Shagrir & Pitowsky
2003; Siegelmann 2003; Andréka, Németi, &
many computer science textbooks formulate the Church-Turing thesis
without mentioning human computers (e.g., Hopcroft & Ullman 1979;
Lewis & Papadimitriou 1981). This is despite the fact that the
concept of human computation lay at the heart of Turing’s and
Church’s analyses.

The variety of algorithms studied by modern computer science eclipses
the field as it was in Turing’s day. There are now parallel
algorithms, distributed algorithms, interactive algorithms, analog
algorithms, hybrid algorithms, quantum algorithms, enzymatic
following (famous) formulation of the algorithmic version of the
thesis:

> any algorithmic problem for which we can find an algorithm that can be
> programmed in some programming language, *any* language,
> … is also solvable by a Turing machine. This statement is one
> version of the so-called Church/Turing thesis. (Harel 1992: 233)

Given the extent to which the concept of an algorithm has evolved
since the 1930s—from the step-by-step labors of human computers
neither a logico-mathematical theorem nor a definition. If it is true,
then its truth is a consequence of the laws of physics—and it
might not be true. (Although it is trivial if, contrary to a standard
but unproved assumption in computer science, P = NP.)

The second complexity-theoretic version of the thesis involves the
concept of a *probabilistic Turing machine* (due to Rabin &
Scott 1959). Vazirani and Aharonov state the thesis:

> [T]he extended Church-Turing thesis … asserts that any
> enough to be describable by … mathematical relationships
> … we know that some specific version of a Turing machine will
> be able to mimic them. (Guttenplan 1994: 595)

Andréka, Németi and Németi state a more general
thesis about the power of Turing machines to simulate other
systems:

> [T]he Physical Church-Turing Thesis … is the conjecture that
> whatever physical computing device (in the broader sense) or physical
thesis they state here “was formulated and generally accepted in
the 1930s” (ibid.).

Yet it was *not* a thesis about the simulation of physical
systems that Church and Turing formulated in the 1930s, but rather a
completely different thesis concerning human computation—and it
was the latter thesis that became generally accepted during the 1930s
and 1940s.

It certainly muddies the waters to call a thesis about simulation
systems that Church and Turing formulated in the 1930s, but rather a
completely different thesis concerning human computation—and it
was the latter thesis that became generally accepted during the 1930s
and 1940s.

It certainly muddies the waters to call a thesis about simulation
“Church’s thesis” or the “Church-Turing
thesis”, because the arguments that Church and Turing used to
support their actual theses go no way at all towards supporting the
theses set out in the several quotations above. Nevertheless, what can
> mathematical relationships (Guttenplan) can be simulated by a Turing
> machine.

If the Simulation thesis is intended to cover all possible systems
then it is surely false, since Doyle’s envisaged equilibrating
systems falsify it
([Section 5.3.3](#BeyoEffe)).
If, on the other hand, the thesis is intended to cover only actual
physical systems, including brains, then the Simulation thesis is,
like the Extended Church-Turing thesis, an *empirical*
In 1985, Wolfram formulated a thesis that he described as “a
physical form of the Church-Turing hypothesis”:

> [U]niversal computers are as powerful in their computational
> capacities as any physically realizable system can be, so that they
> can simulate any physical system. (Wolfram 1985: 735)

Deutsch (who laid the foundations of quantum computation)
independently stated a similar thesis, again in 1985, and also
described it as a “physical version” of the Church-Turing
> means”. This formulation is both better defined and more
> physical than Turing’s own way of expressing it. (Deutsch 1985:
> 99)

This thesis is certainly “more physical” than
Turing’s thesis. It is, however, a completely *different*
claim from Turing’s own, so it is potentially confusing to
present it as a “better defined” version of what Turing
said. As already emphasized, Turing was talking about *effective
methods*, whereas the theses presented by Deutsch and Wolfram
The following formulation differs in its details from both
Wolfram’s and Deutsch’s theses, but arguably captures the
spirit of both. In view of the Deutsch-Gandy point about continuous
systems, the idea of perfect simulation is replaced by the concept of
simulation *to any desired degree of accuracy*:

> **Deutsch-Wolfram Thesis**:
>   
> Every finite physical system can be simulated to any specified degree
> of accuracy by a universal Turing machine. (Copeland & Shagrir
three-dimensional wave equation is capable of exhibiting behavior that
falsifies the Deutsch-Wolfram thesis. However, now as then, it is an
open question whether these initial conditions are physically
possible.

#### 6.4.2 The “Gandy argument” {#-642-the-gandy-argument}

Gandy (1980) gave a profound discussion of whether there could be
deterministic, discrete systems whose behavior cannot be calculated by
a universal Turing machine. The now famous “Gandy
set-theoretic derivation that makes very general physical assumptions
(namely, the four axioms mentioned in
[Section 3.4](#ModeAxioAnal)).
These assumptions include, for instance, a lower bound on the
dimensions of a mechanism’s components, and an upper bound on
the speed of propagation of effects and signals. (The argument aims to
cover only mechanisms obeying the principles of Relativity.) Gandy
expressed his various physical assumptions set-theoretically, by means
of precise axioms, which he called Principles I – IV. Principle
III, for example, captures the idea that there is a bound on the
> mathematical problems … and in general any problem which
> concerns the discovery of an algorithm. (Church 1937a: 43)

### 7.4 Turing’s use of “machine” {#-74-turings-use-of-machine}

It is important to note that, when Turing used the word
“machine”, he often meant not machine-in-general but, as
we would now say, Turing machine. At one point he explicitly drew
attention to this usage:

which a casual reader might mistake for a formulation of the
maximality thesis:

> The importance of the universal machine is clear. We do not need to
> have an infinity of different machines doing different jobs. A single
> one will suffice. The engineering problem of producing various
> machines for various jobs is replaced by the office work of
> “programming” the universal machine to do these jobs.
> (Turing 1948 [2004: 414])

physical” than any of Turing’s formulations of the thesis.
Church’s finiteness requirements are in some respects
reminiscent of Gandy’s idea that the states of a discrete
deterministic calculating machine must be built up iteratively from a
bounded number of types of basic components, the dimensions of which
have a lower bound (see
[Section 6.4.2](#GandArgu)).
Although, as explained there, Gandy imposes further requirements on a
discrete deterministic calculating machine, and these go far beyond
Church’s finiteness requirements.
  Logic”, in Jon Barwise (ed.), *Handbook of Mathematical
  Logic*, Amsterdam: North-Holland, 5–46.
* Bausch, Johannes, Toby S. Cubitt, Angelo Lucia, and David
  Perez-Garcia, 2020, “Undecidability of the Spectral Gap in One
  Dimension”, *Physical Review X*, 10(3): 031038.
  doi:10.1103/PhysRevX.10.031038
* Bausch, Johannes, Toby S. Cubitt, and James D. Watson, 2019,
  “Uncomputability of Phase Diagrams”,
  arXiv:1910.01631.
* –––, 2021, “Uncomputability of Phase
  Mathematical Society. In Mancosu and Zach 2015: 177–187, with a
  partial translation by Richard Zach in the same (2015:
  173–177).
* –––, 1922, “Beiträge zur Algebra der
  Logik, insbesondere zum Entscheidungsproblem”, *Mathematische
  Annalen*, 88(1–2): 168–168.
  doi:10.1007/BF01448447
* Bernays, Paul, 1918, “Beiträge zur axiomatischen
  Behandlung des Logik-Kalküls”, Habilitationsschrift,
  University of Göttingen. Bernays Papers, ETH Zurich (Hs
  A. Shore, 2001, “The Prospects for Mathematical Logic in the
  Twenty-First Century”, *Bulletin of Symbolic Logic*,
  7(2): 169–196. doi:10.2307/2687773
* Calude, Cristian S. and Karl Svozil, 2008, “Quantum
  Randomness and Value Indefiniteness”, *Advanced Science
  Letters*, 1(2): 165–168. doi:10.1166/asl.2008.016
* Calude, Cristian S., Michael J. Dinneen, Monica Dumitrescu, and
  Karl Svozil, 2010, “Experimental Evidence of Quantum Randomness
  Incomputability”, *Physical Review A*, 82(2): 022102.
  doi:10.1103/PhysRevA.82.022102
  *Bulletin of the American Mathematical Society*, 41(6):
  332–333. Full paper in Church 1936b.
* –––, 1935b, letter to Kleene, 29 November 1935.
  Excerpt in Davis 1982: 9.
* –––, 1935c, “A Proof of Freedom from
  Contradiction”, *Proceedings of the National Academy of
  Sciences*, 21(5): 275–281. doi:10.1073/pnas.21.5.275
* –––, 1936a, “An Unsolvable Problem of
  Elementary Number Theory”, *American Journal of
  Mathematics*, 58(2): 345–363. doi:10.2307/2371045
  of Conversion”, *Transactions of the American Mathematical
  Society*, 39(3): 472–482.
  doi:10.1090/S0002-9947-1936-1501858-0
* Copeland, B. Jack, 1998a, “Even Turing Machines Can Compute
  Uncomputable Functions”, in *Unconventional Models of
  Computation, Proceedings of the 1st International Conference, New
  Zealand*, Christian S. Calude, John Casti, and Michael J. Dinneen
  (eds), London: Springer-Verlag, 150–164.
* –––, 1998b, “Super Turing-Machines”,
  *Complexity*, 4(1): 30–32.
  Gödel’s Shoulders?”, *The Mathematical
  Intelligencer*, 44: 308–319.
  doi:10.1007/s00283-022-10177-y
* –––, 2023, “Turing and von Neumann: From
  Logic to the Computer”, *Philosophies*, 8(2):
  1–30.
* Copeland, B. Jack, Carl J. Posy, and Oron Shagrir (eds), 2013,
  *Computability: Turing, Gödel, Church, and Beyond*,
  Cambridge, MA: The MIT Press.
* Copeland, B. Jack and Oron Shagrir, 2007, “Physical
  Series A. Mathematical and Physical Sciences*, 400(1818):
  97–117. doi:10.1098/rspa.1985.0070
* Doyle, Jon, 1982, “What is Church’s Thesis? An
  Outline”, Laboratory for Computer Science, MIT.
* –––, 2002, “What Is Church’s Thesis?
  An Outline”, *Minds and Machines*, 12(4): 519–520.
  doi:10.1023/A:1021126521437
* Earman, John, 1986, *A Primer on Determinism*, Dordrecht:
  Reidel.
* Eisert, Jens, Markus P. Müller, and Christian Gogolin, 2012,
  Propositions of Formal Mathematical Systems”, Lecture notes
  taken by Stephen Kleene and J. Barkley Rosser at the Institute for
  Advanced Study, in Davis 1965: 39–74.
* –––, 1936, “Über die Länge von
  Beweisen”, *Ergebnisse eirtes mathematischen
  Kolloquiums*, 7: 23–24.
* –––, 193?, “Undecidable Diophantine
  Propositions”, in Gödel 1995: 164–175.
* –––, 1946, “Remarks Before the Princeton
  Bicentennial Conference”, in Gödel 1990:
* Hardy, G. H., 1929, “Mathematical Proof”,
  *Mind*, 38(149): 1–25.
  doi:10.1093/mind/XXXVIII.149.1
* Harel, David, 1992, *Algorithmics: The Spirit of
  Computing*, second edition, Reading, MA: Addison-Wesley.
* Herbrand, Jacques, 1930a, *Recherches sur la Théorie de
  la Démonstration*, doctoral thesis, University of Paris. In
  Herbrand 1968.
* –––, 1930b, “Les bases de la logique
  Hilbertienne”, *Revue de Métaphysique et de
  “Mathematical Problems”, Mary Winston Newson (trans.),
  *Bulletin of the American Mathematical Society*, 8(10):
  437–480. doi:10.1090/S0002-9904-1902-00923-3
* –––, 1917, “Axiomatisches Denken”,
  *Mathematische Annalen*, 78(1–4): 405–415.
  doi:10.1007/BF01457115
* –––, 1922, “Neubegründung der
  Mathematik. Erste Mitteilung”, *Abhandlungen aus dem
  Mathematischen Seminar der Universität Hamburg*, 1:
  157–177. doi:10.1007/BF02940589
  *Bulletin of the American Mathematical Society*, 8(10):
  437–480. doi:10.1090/S0002-9904-1902-00923-3
* –––, 1917, “Axiomatisches Denken”,
  *Mathematische Annalen*, 78(1–4): 405–415.
  doi:10.1007/BF01457115
* –––, 1922, “Neubegründung der
  Mathematik. Erste Mitteilung”, *Abhandlungen aus dem
  Mathematischen Seminar der Universität Hamburg*, 1:
  157–177. doi:10.1007/BF02940589
* –––, 1926 [1967], “Über das
  Recursiveness”, *Duke Mathematical Journal*, 2(2):
  340–353. doi:10.1215/S0012-7094-36-00227-2
* –––, 1952, *Introduction to
  Metamathematics*, Amsterdam: North-Holland.
* –––, 1967, *Mathematical Logic*, New
  York: Wiley.
* –––, 1981, “Origins of Recursive Function
  Theory”, *IEEE Annals of the History of Computing*, 3(1):
  52–67. doi:10.1109/MAHC.1981.10004
* –––, 1986, “Introductory Note to
* –––, 1967, *Mathematical Logic*, New
  York: Wiley.
* –––, 1981, “Origins of Recursive Function
  Theory”, *IEEE Annals of the History of Computing*, 3(1):
  52–67. doi:10.1109/MAHC.1981.10004
* –––, 1986, “Introductory Note to
  *1930b*, *1931* and *1932b*”, in Gödel
  1986: 126–141.
* –––, 1987, “Reflections on Church’s
  Thesis”, *Notre Dame Journal of Formal Logic*, 28(4):
* Kreisel, Georg, 1965, “Mathematical Logic”, in
  *Lectures on Modern Mathematics, Volume 3*, Thomas L. Saaty
  (ed.), New York: Wiley, 95–195.
* –––, 1967, “Mathematical Logic: What Has
  it Done For the Philosophy of Mathematics?”, in *Bertrand
  Russell: Philosopher of the Century*, Ralph Schoenman (ed.),
  London: George Allen and Unwin: 201–272.
* –––, 1974, “A Notion of Mechanistic
  Theory”, *Synthese*, 29(1–4): 11–26.
  doi:10.1007/BF00484949
* –––, 1967, “Mathematical Logic: What Has
  it Done For the Philosophy of Mathematics?”, in *Bertrand
  Russell: Philosopher of the Century*, Ralph Schoenman (ed.),
  London: George Allen and Unwin: 201–272.
* –––, 1974, “A Notion of Mechanistic
  Theory”, *Synthese*, 29(1–4): 11–26.
  doi:10.1007/BF00484949
* –––, 1982, Review of Pour-El and Richards 1979
  and 1981, *The Journal of Symbolic Logic*, 47(4):
  900–902. doi:10.2307/2273108
  of Postulates”, *Proceedings of the London Mathematical
  Society*, second series 25: 115–142.
  doi:10.1112/plms/s2-25.1.115
* –––, 1927, “Theorems on Deducibility
  (Second Paper)”, *Annals of Mathematics*, second series
  28(1/4): 459–471. doi:10.2307/1968390
* Langton, Christopher G., 1989, “Artificial Life”, in
  *Artificial Life: The Proceedings of An Interdisciplinary Workshop
  on the Synthesis and Simulation of Living Systems, Held September,
  1987 in Los Alamos, New Mexico*, Christopher G. Langton (ed.),
  Algorithms”, *American Mathematical Society
  Translations*, Series 2, 15: 1–14.
* Marquand, Allan, 1881, “On Logical Diagrams for *n*
  Terms”, *The London, Edinburgh, and Dublin Philosophical
  Magazine and Journal of Science*, fifth series, 12(75):
  266–270. doi:10.1080/14786448108627104
* –––, 1883, “A Machine for Producing
  Syllogistic Variations”, in *Studies in Logic*, Charles
  S. Peirce (ed.), Boston: Little, Brown, 12–15.
  doi:10.1037/12811-002
* –––, 1964, *Introduction to Mathematical
  Logic*, Princeton, NJ: Van Nostrand.
* –––, 1990, “Second Thoughts about
  Church’s Thesis and Mathematical Proofs”, *The Journal
  of Philosophy*, 87(5): 225–233. doi:10.2307/2026831
* Montague, Richard, 1960, “Towards a General Theory of
  Computability”, *Synthese*, 12(4): 429–438.
  doi:10.1007/BF00485427
* Németi, István and Gyula Dávid, 2006,
  “Relativistic Computers and the Turing Barrier”,
  Church’s Thesis and Mathematical Proofs”, *The Journal
  of Philosophy*, 87(5): 225–233. doi:10.2307/2026831
* Montague, Richard, 1960, “Towards a General Theory of
  Computability”, *Synthese*, 12(4): 429–438.
  doi:10.1007/BF00485427
* Németi, István and Gyula Dávid, 2006,
  “Relativistic Computers and the Turing Barrier”,
  *Applied Mathematics and Computation*, 178(1): 118–142.
  doi:10.1016/j.amc.2005.09.075
* Newell, Allen, 1980, “Physical Symbol Systems”,
  Mathematical Mind”, in *The Once and Future Turing: Computing
  the World*, S. Barry Cooper and Andrew Hodges (eds), Cambridge:
  Cambridge University Press, 361–378.
  doi:10.1017/CBO9780511863196.022
* Péter, Rózsa, 1935, “Über den
  Zusammenhang der verschiedenen Begriffe der rekursiven
  Funktion”, *Mathematische Annalen*, 110(1):
  612–632. doi:10.1007/BF01448046
* Pitowski, Itamar, 1990, “The Physical Church Thesis and
  Physical Computational Complexity”, *Iyyun*, 39:
  Processes—Formulation 1”, *The Journal of Symbolic
  Logic*, 1(3): 103–105. doi:10.2307/2269031
* –––, 1943, “Formal Reductions of the
  General Combinatorial Decision Problem”, *American Journal of
  Mathematics*, 65(2): 197–215. doi:10.2307/2371809
* –––, 1946, “A Variant of a Recursively
  Unsolvable Problem”, *Bulletin of the American Mathematical
  Society*, 52(4): 264–268.
  doi:10.1090/S0002-9904-1946-08555-9
* –––, 1965, “Absolutely Unsolvable Problems
  Unsolvable Problem”, *Bulletin of the American Mathematical
  Society*, 52(4): 264–268.
  doi:10.1090/S0002-9904-1946-08555-9
* –––, 1965, “Absolutely Unsolvable Problems
  and Relatively Undecidable Propositions—Account of an
  Anticipation”, in Davis 1965: 340–433.
* Pour-El, Marian Boykan and Ian Richards, 1979, “A Computable
  Ordinary Differential Equation Which Possesses No Computable
  Solution”, *Annals of Mathematical Logic*, 17(1–2):
  61–90. doi:10.1016/0003-4843(79)90021-4
  Ordinary Differential Equation Which Possesses No Computable
  Solution”, *Annals of Mathematical Logic*, 17(1–2):
  61–90. doi:10.1016/0003-4843(79)90021-4
* –––, 1981, “The Wave Equation with
  Computable Initial Data Such That Its Unique Solution Is Not
  Computable”, *Advances in Mathematics*, 39(3):
  215–239. doi:10.1016/0001-8708(81)90001-3
* –––, 1989, *Computability in Analysis and
  Physics*, Berlin: Springer.
  [[Pour-El and Richards 1989 available online](https://projecteuclid.org/eBooks/perspectives-in-logic/Computability-in-Analysis-and-Physics/toc/pl/1235422916)]
  Solution”, *Annals of Mathematical Logic*, 17(1–2):
  61–90. doi:10.1016/0003-4843(79)90021-4
* –––, 1981, “The Wave Equation with
  Computable Initial Data Such That Its Unique Solution Is Not
  Computable”, *Advances in Mathematics*, 39(3):
  215–239. doi:10.1016/0001-8708(81)90001-3
* –––, 1989, *Computability in Analysis and
  Physics*, Berlin: Springer.
  [[Pour-El and Richards 1989 available online](https://projecteuclid.org/eBooks/perspectives-in-logic/Computability-in-Analysis-and-Physics/toc/pl/1235422916)]
* Quine, Willard Van Orman, 1950, *Methods of Logic*, New
* –––, 1981, “The Wave Equation with
  Computable Initial Data Such That Its Unique Solution Is Not
  Computable”, *Advances in Mathematics*, 39(3):
  215–239. doi:10.1016/0001-8708(81)90001-3
* –––, 1989, *Computability in Analysis and
  Physics*, Berlin: Springer.
  [[Pour-El and Richards 1989 available online](https://projecteuclid.org/eBooks/perspectives-in-logic/Computability-in-Analysis-and-Physics/toc/pl/1235422916)]
* Quine, Willard Van Orman, 1950, *Methods of Logic*, New
  York: Holt.
* –––, 1951, *Mathematical Logic*, revised
* –––, 1951, *Mathematical Logic*, revised
  edition, Cambridge, MA: Harvard University Press.
* Rabin, Michael O. and Dana S. Scott, 1959, “Finite Automata
  and Their Decision Problems”, *IBM Journal of Research and
  Development*, 3(2): 114–125. doi:10.1147/rd.32.0114
* Ramsey, Frank P., 1930, “On a Problem of Formal
  Logic”, *Proceedings of the London Mathematical Society*,
  second series 30(1): 264–286. doi:10.1112/plms/s2-30.1.264
* Roberts, Don D., 1973, *The Existential Graphs of Charles S.
  Peirce*, Hague: Mouton.
  Logic”, *Proceedings of the London Mathematical Society*,
  second series 30(1): 264–286. doi:10.1112/plms/s2-30.1.264
* Roberts, Don D., 1973, *The Existential Graphs of Charles S.
  Peirce*, Hague: Mouton.
* –––, 1997, “A Decision Method for
  Existential Graphs”, in Houser, Roberts, & Van Evra 1997:
  387–401.
* Rosser, J. Barkley, 1935a, “A Mathematical Logic Without
  Variables. I”, *Annals of Mathematics*, second series
  36(1): 127–150. doi:10.2307/1968669
* Rosser, J. Barkley, 1935a, “A Mathematical Logic Without
  Variables. I”, *Annals of Mathematics*, second series
  36(1): 127–150. doi:10.2307/1968669
* –––, 1935b, “A Mathematical Logic without
  Variables. II”, *Duke Mathematical Journal*, 1(3):
  328–355. doi:10.1215/S0012-7094-35-00123-5
* Scarpellini, Bruno, 1963, “Zwei Unentscheidbare Probleme Der
  Analysis”, *Zeitschrift für Mathematische Logik und
  Grundlagen der Mathematik*, 9(18–20): 265–289.
  doi:10.1002/malq.19630091802
* –––, 1935b, “A Mathematical Logic without
  Variables. II”, *Duke Mathematical Journal*, 1(3):
  328–355. doi:10.1215/S0012-7094-35-00123-5
* Scarpellini, Bruno, 1963, “Zwei Unentscheidbare Probleme Der
  Analysis”, *Zeitschrift für Mathematische Logik und
  Grundlagen der Mathematik*, 9(18–20): 265–289.
  doi:10.1002/malq.19630091802
* –––, 2003, “Comments on ‘Two
  Undecidable Problems of Analysis’”, *Minds and
  Machines*, 13(1): 79–85. doi:10.1023/A:1021364916624
  Variables. II”, *Duke Mathematical Journal*, 1(3):
  328–355. doi:10.1215/S0012-7094-35-00123-5
* Scarpellini, Bruno, 1963, “Zwei Unentscheidbare Probleme Der
  Analysis”, *Zeitschrift für Mathematische Logik und
  Grundlagen der Mathematik*, 9(18–20): 265–289.
  doi:10.1002/malq.19630091802
* –––, 2003, “Comments on ‘Two
  Undecidable Problems of Analysis’”, *Minds and
  Machines*, 13(1): 79–85. doi:10.1023/A:1021364916624
* Schiemer, Georg, Richard Zach, and Erich Reck, 2017,
  Mathematical Experience”, in *Mathematics and Mind*,
  Alexander George (ed.), Oxford: Oxford University Press:
  71–117.
* –––, 2002, “Calculations by Man and
  Machine: Conceptual Analysis”, in *Reflections on the
  Foundations of Mathematics: Essays in Honor of Solomon Feferman*,
  Wilfried Sieg, Richard Sommer, and Carolyn Talcott (eds), Urbana, IL:
  Association for Symbolic Logic, 390–409.
* –––, 2008, “Church Without Dogma: Axioms
  for Computability”, in *New Computational Paradigms*, S.
  the London Mathematical Society*, 1936, second series, 42(1):
  230–265. Reprinted in Copeland 2004: 58–90 (ch. 1).
  doi:10.1112/plms/s2-42.1.230
* –––, 1937, “Computability and
  λ-Definability”, *The Journal of Symbolic Logic*,
  2(4): 153–163. doi:10.2307/2268280
* –––, 1939 [2004], “Systems of Logic Based
  on Ordinals”, *Proceedings of the London Mathematical
  Society*, second series, 45(1): 161–228. Reprinted in
  Copeland 2004: 146–204 (ch. 3).
  on Ordinals”, *Proceedings of the London Mathematical
  Society*, second series, 45(1): 161–228. Reprinted in
  Copeland 2004: 146–204 (ch. 3).
  doi:10.1112/plms/s2-45.1.161
* –––, c.1940 [2004], letter to Newman, n.d., in
  Copeland 2004: 214–216 (ch. 4).
* –––, 1945 [2005], “Proposed Electronic
  Calculator”, National Physical Laboratory Report, in Copeland
  2005: 369–454 (ch. 20).
  doi:10.1093/acprof:oso/9780198565932.003.0021
  Automatic Computing Engine”, London Mathematical Society, in
  Copeland 2004: 378–394 (ch. 9).
* –––, 1948 [2004], “Intelligent
  Machinery”, National Physical Laboratory Report, in Copeland
  2004: 410–432 (ch. 10).
* –––, 1950a [2004], “Computing Machinery
  and Intelligence”, *Mind*, 59(236): 433–460.
  Reprinted in Copeland 2004: 441–464 (ch. 11).
  doi:10.1093/mind/LIX.236.433
* –––, 1950b, “The Word Problem in
  Book in Mathematical Logic, 1879–1931*, Cambridge, MA:
  Harvard University Press.
* Venn, John, 1880, “On the Diagrammatic and Mechanical
  Representation of Propositions and Reasonings”, *The London,
  Edinburgh, and Dublin Philosophical Magazine and Journal of
  Science*, fifth series, 10(59): 1–18.
  doi:10.1080/14786448008626877
* von Neumann, John, 1927, “Zur Hilbertschen
  Beweistheorie”, *Mathematische Zeitschrift*, 26(1):
  1–46. doi:10.1007/BF01475439

## Assumptions & Principles {#-assumptions--principles}

### Core Postulates {#-core-postulates}
encapsulates the fundamental logical principles of the stored-program
all-purpose digital computer). Modern reimaginings of the
Church-Turing thesis transform it, extending it to fundamental
physics, complexity theory, exotic algorithms, and cognitive science.
It is important to be aware though that some of the theses nowadays
referred to as the Church-Turing thesis are at best *very*
distant relatives of the thesis advanced by Church and Turing.

## 1. The 1936 Thesis and its Context {#-1-the-1936-thesis-and-its-context}

3. \(M\) can (in practice or in principle) be carried out by a human
   being unaided by any machinery except paper and pencil;
4. \(M\) demands no insight, intuition, or ingenuity, on the part of
   the human being carrying out the method.

A well-known example of an effective method is the truth-table test
for tautologousness. In principle, a human being who works by rote
could apply this test successfully to any formula of the propositional
calculus—given sufficient time, tenacity, paper, and pencils
(although in practice the test is unworkable for any formula
for tautologousness. In principle, a human being who works by rote
could apply this test successfully to any formula of the propositional
calculus—given sufficient time, tenacity, paper, and pencils
(although in practice the test is unworkable for any formula
containing more than a few propositional variables).

### 1.1 Note on terminology {#-11-note-on-terminology}

Statements that there is an effective method for achieving
such-and-such a result are commonly expressed by saying that there is
proved is called an *equivalence result*. There is further
discussion of equivalence results in
[Section 4.1](#InduEquiArgu).

Post referred to Church’s identification of effective
calculability with recursiveness and λ-definability as a
“working hypothesis”, and he quite properly criticized
Church for masking this hypothesis as a *definition*:

> [T]o mask this identification under a definition … blinds us to
discussion of equivalence results in
[Section 4.1](#InduEquiArgu).

Post referred to Church’s identification of effective
calculability with recursiveness and λ-definability as a
“working hypothesis”, and he quite properly criticized
Church for masking this hypothesis as a *definition*:

> [T]o mask this identification under a definition … blinds us to
> the need of its continual verification. (Post 1936: 105)
formula can be derived, step by logical step, from the axioms and
definitions of the calculus, using only the rules of the calculus.)
For example, if such a method for the classical propositional calculus
is used to test the formula \(A \rightarrow A\) (\(A\) implies \(A\)),
the output will be “Yes, provable”, and if the
contradiction \(A \amp \neg A\) is tested, the output will be
“Not provable”. Such a method is called a *decision
method* or *decision procedure*.

Church and Turing took on the *Entscheidungsproblem* for a
*Grundzüge der Theoretischen Logik* (Principles of
Mathematical Logic):

> [I]t is to be expected that a systematic, so to speak computational
> treatment of the logical formulae is possible …. (Hilbert &
> Ackermann 1928: 72)

However, their expectations were frustrated by the Church-Turing
result of 1936. Hilbert and Ackermann excised the quoted statement
from a revised edition of their book. Published in 1938, the new
principles in which the principles of other sciences would be
implicit” (Preface to *Ars Generalis Ultima*, in Llull
1645 [1970: 1]). Llull used circumscribed fields of knowledge to
illustrate his idea of a mechanical question-answerer, designing small
domain-specific machines consisting of superimposed discs; possibly
his machines took the form of a parchment *volvelle*, a
relative of the metal astrolabe.

In early modern times, Llull’s idea of the *ars
generalis* received a sympathetic discussion in Leibniz’s
beta-graphs system contains the axioms and rules of Quine’s 1951
formulation of the first-order functional calculus, in which only
closed formulae are asserted (Quine 1951: 88).

Peirce anticipated the concept of a decision method in his extensive
notes for a series of lectures he delivered in Boston in 1903. There
he developed a method (Peirce 1903b,c) that, if applied to any given
formula of the propositional calculus, would, he said,
“determine” (or “positively ascertain”)
whether the alpha-graphs system demonstrates that the formula is
> assumptions about number. The logical machines hitherto constructed
> are inadequate to the performance of mathematical deductions. There
> is, however, a modern Exact Logic which, although yet in its infancy,
> is already far enough advanced to render it a mere question of expense
> to construct a machine that would grind out all the known theorems of
> arithmetic and advance that science still more rapidly than it is now
> progressing. (Peirce *n.d.*, quoted in Stjernfelt 2022)

Here Peirce seems to be asserting—quite correctly—that a
machine can be devised to grind out all the theorems of
Dedekind’s (1888) axiomatisation of arithmetic (which consisted
of six “primary assumptions” in the form of of four axioms
and two definitions). This statement of Peirce’s, made almost
four decades before Turing introduced Turing machines into
mathematics, was well ahead of its time.

As to whether *all* mathematical reasoning can be performed by
a machine, as Leibniz seems to have thought, Peirce was fiercely
skeptical. He formulated the hypothesis that, in the future,
mathematical reasoning
of six “primary assumptions” in the form of of four axioms
and two definitions). This statement of Peirce’s, made almost
four decades before Turing introduced Turing machines into
mathematics, was well ahead of its time.

As to whether *all* mathematical reasoning can be performed by
a machine, as Leibniz seems to have thought, Peirce was fiercely
skeptical. He formulated the hypothesis that, in the future,
mathematical reasoning

> guided by the principle of discussing each given question in such a
> way that we examined both whether it can or cannot be answered by
> means of prescribed steps using certain limited resources. (Hilbert
> 1899: 89)

Concerning a specific example, he wrote:

> Suppose a geometrical construction problem that can be carried out
> with a compass is presented; we will attempt to lay down a criterion
> that enables us to determine [*beurteilen*] immediately, from
> axioms, and a general method reached for attacking the problem of
> whether a given process terminates or not. (Newman 1923: 12)

Newman did not mention the *Entscheidungsproblem* in his 1923
paper—let alone moot its unsolvability (there is no evidence
that, pre-Turing, he thought the problem unsolvable)—yet, with
hindsight, he certainly laid some suggestive groundwork for an attack
on the problem. He wrote:

> The information of the first importance to be obtained about a process
Bernays established an equivalence result: The numerical functions
that are capable of rule-governed evaluation coincide with the
(primitive) recursive functions (1939: 403 and 393*n*).

It is perhaps unsurprising that Hilbert, the founder of proof theory,
ultimately selected an analysis of effective calculability as
calculability *within a logic*, even though Church and Turing
had already presented their analyses in terms of recursive functions
and Turing machines respectively. Hilbert and Bernays went on to use
their analysis to give a new proof of the unsolvability of the
### 3.4 Modern axiomatic analyses {#-34-modern-axiomatic-analyses}

Church reported a discussion he had had with Gödel at the time
when it was still wide open how the intuitive concept of effective
calculability should be formalized (probably during 1934). Gödel
suggested that

> it might be possible, in terms of effective calculability as an
> undefined notion, to state a set of axioms which would embody the
> generally accepted properties of this notion, and to do something on
> undefined notion, to state a set of axioms which would embody the
> generally accepted properties of this notion, and to do something on
> that basis. (Church 1935b)

Logicians frequently analyse a concept of interest, e.g., universal
quantification, not by defining it in terms of other concepts, but by
stating a set of axioms that collectively embody the generally
accepted properties of (say) universal quantification. To follow this
approach in the case of effectiveness, we would “write down some
axioms about computable functions which most people would agree are
stating a set of axioms that collectively embody the generally
accepted properties of (say) universal quantification. To follow this
approach in the case of effectiveness, we would “write down some
axioms about computable functions which most people would agree are
evidently true” (Shoenfield 1993: 26). Shoenfield continued,
“It might be possible to prove Church’s Thesis from such
axioms”, but added: “However, despite strenuous efforts,
no one has succeeded in doing this”.

Moving on a few years, a meeting on *The Prospects for Mathematical
axioms about computable functions which most people would agree are
evidently true” (Shoenfield 1993: 26). Shoenfield continued,
“It might be possible to prove Church’s Thesis from such
axioms”, but added: “However, despite strenuous efforts,
no one has succeeded in doing this”.

Moving on a few years, a meeting on *The Prospects for Mathematical
Logic in the Twenty-First Century*, held at the turn of the
millennium, included the following among leading open problems:

axioms”, but added: “However, despite strenuous efforts,
no one has succeeded in doing this”.

Moving on a few years, a meeting on *The Prospects for Mathematical
Logic in the Twenty-First Century*, held at the turn of the
millennium, included the following among leading open problems:

> “Prove” the Church-Turing thesis by finding intuitively
> obvious or at least clearly acceptable properties of computation that
> suffice to guarantee that any function so computed is recursive [and
The axiomatic type of approach sketched by Gödel has by now been
developed in a number of quite different ways. These axiomatic
frameworks go a long way toward countering Montague’s complaint
of over 60 years ago that “Discussion of Church’s thesis
has suffered for lack of a precise general framework within which it
could be conducted” (Montague 1960: 432). Some examples of the
axiomatic approach are as follows (in chronological order):

* Gandy (Turing’s only PhD student) pointed out that
  Turing’s analysis of human computation does not immediately
developed in a number of quite different ways. These axiomatic
frameworks go a long way toward countering Montague’s complaint
of over 60 years ago that “Discussion of Church’s thesis
has suffered for lack of a precise general framework within which it
could be conducted” (Montague 1960: 432). Some examples of the
axiomatic approach are as follows (in chronological order):

* Gandy (Turing’s only PhD student) pointed out that
  Turing’s analysis of human computation does not immediately
  apply to computing machines strongly dissimilar from Turing machines.
axiomatic approach are as follows (in chronological order):

* Gandy (Turing’s only PhD student) pointed out that
  Turing’s analysis of human computation does not immediately
  apply to computing machines strongly dissimilar from Turing machines.
  (See
  [Section 4.3](#TuriArguI)
  below for details of Turing’s analysis.) For example,
  Turing’s analysis does not obviously apply to parallel machines
  which, unlike a Turing machine, are able to process an arbitrary
  and massively parallel machines, Gandy (1980) stated four axioms
  governing the behaviour of what he called *discrete deterministic
  mechanical devices*. (He formulated the axioms in terms of
  hereditarily finite sets.) Gandy was then able to prove that every
  device satisfying these axioms can be simulated by a Turing machine:
  Discrete deterministic mechanical devices, even massively parallel
  ones, are no more powerful than Turing machines, in the sense that
  whatever computations such a device is able to perform can also be
  done by the universal Turing machine. (For more on Gandy’s
  analysis, see
  mechanical devices*. (He formulated the axioms in terms of
  hereditarily finite sets.) Gandy was then able to prove that every
  device satisfying these axioms can be simulated by a Turing machine:
  Discrete deterministic mechanical devices, even massively parallel
  ones, are no more powerful than Turing machines, in the sense that
  whatever computations such a device is able to perform can also be
  done by the universal Turing machine. (For more on Gandy’s
  analysis, see
  [Section 6.4.2](#GandArgu).)
* Engeler axiomatized the concept of an algorithmic function by using
  device satisfying these axioms can be simulated by a Turing machine:
  Discrete deterministic mechanical devices, even massively parallel
  ones, are no more powerful than Turing machines, in the sense that
  whatever computations such a device is able to perform can also be
  done by the universal Turing machine. (For more on Gandy’s
  analysis, see
  [Section 6.4.2](#GandArgu).)
* Engeler axiomatized the concept of an algorithmic function by using
  *combinators* (Engeler 1983: ch. III). Combinators were
  originally introduced by Schönfinkel in 1924, in a paper that a
* Engeler axiomatized the concept of an algorithmic function by using
  *combinators* (Engeler 1983: ch. III). Combinators were
  originally introduced by Schönfinkel in 1924, in a paper that a
  recent book on combinators described as “presenting a formalism
  for universal computation for the very first time”
  (Schönfinkel 1924; Wolfram 2021: 214). Schönfinkel’s
  combinators were extensively developed by Curry (Curry 1929, 1930a,b,
  1932; Curry & Feys 1958). Examples of combinators are the
  “permutator” \(\mathrm{C}\) and the
  “cancellator” \(\mathrm{K}\). These produce the following
  of four axioms (Sieg 2008). The result, Sieg said, is an axiomatic
  characterization of “the concept ‘mechanical
  procedure’”, and he observed that his system
  “substantiates Gödel’s remarks” (above) that
  one should try to find a set of axioms embodying the generally
  accepted properties of the concept of effectiveness (Sieg 2008:
  150).
* Dershowitz and Gurevich (2008) stated three very general axioms,
  treating computations as discrete, deterministic,
  sequentially-evolving structures of states. They called these
  one should try to find a set of axioms embodying the generally
  accepted properties of the concept of effectiveness (Sieg 2008:
  150).
* Dershowitz and Gurevich (2008) stated three very general axioms,
  treating computations as discrete, deterministic,
  sequentially-evolving structures of states. They called these
  structures “state-transition systems”, and called the
  three axioms the “Sequential Postulates”. They also used a
  fourth axiom, stipulating that “Only undeniably computable
  operations are available in initial states” (2008: 306). From
* Dershowitz and Gurevich (2008) stated three very general axioms,
  treating computations as discrete, deterministic,
  sequentially-evolving structures of states. They called these
  structures “state-transition systems”, and called the
  three axioms the “Sequential Postulates”. They also used a
  fourth axiom, stipulating that “Only undeniably computable
  operations are available in initial states” (2008: 306). From
  their four axioms, they proved a proposition they called
  Church’s thesis: “Every numeric function computed by a
  state-transition system satisfying the Sequential Postulates, and
  three axioms the “Sequential Postulates”. They also used a
  fourth axiom, stipulating that “Only undeniably computable
  operations are available in initial states” (2008: 306). From
  their four axioms, they proved a proposition they called
  Church’s thesis: “Every numeric function computed by a
  state-transition system satisfying the Sequential Postulates, and
  provided initially with only basic arithmetic, is partial
  recursive” (2008: 327).

Returning to the *very idea* of proving the Church-Turing
  fourth axiom, stipulating that “Only undeniably computable
  operations are available in initial states” (2008: 306). From
  their four axioms, they proved a proposition they called
  Church’s thesis: “Every numeric function computed by a
  state-transition system satisfying the Sequential Postulates, and
  provided initially with only basic arithmetic, is partial
  recursive” (2008: 327).

Returning to the *very idea* of proving the Church-Turing
thesis, it is important to note that the proposition Dershowitz and
  their four axioms, they proved a proposition they called
  Church’s thesis: “Every numeric function computed by a
  state-transition system satisfying the Sequential Postulates, and
  provided initially with only basic arithmetic, is partial
  recursive” (2008: 327).

Returning to the *very idea* of proving the Church-Turing
thesis, it is important to note that the proposition Dershowitz and
Gurevich call Church’s thesis is in fact *not* the thesis
stated by Church, viz. “A function of positive integers is
  state-transition system satisfying the Sequential Postulates, and
  provided initially with only basic arithmetic, is partial
  recursive” (2008: 327).

Returning to the *very idea* of proving the Church-Turing
thesis, it is important to note that the proposition Dershowitz and
Gurevich call Church’s thesis is in fact *not* the thesis
stated by Church, viz. “A function of positive integers is
effectively calculable only if recursive”. Crucially, their
version of Church’s thesis does not even mention the key concept
down some axioms expressing claims about effective calculability (as
Sieg for instance has done), and suppose it is possible to prove from
these axioms that a function of positive integers is effectively
calculable only if recursive. Church’s thesis would have been
proved from the axioms, but whether the axioms form a satisfactory
account of effective calculability is a *further* question. If
they do not, then this “proof” of Church’s thesis
could carry no conviction. Which is to say, a proof of this sort will
be convincing only to one who accepts another thesis, namely that the
axioms are indeed a satisfactory account of effective calculability.
these axioms that a function of positive integers is effectively
calculable only if recursive. Church’s thesis would have been
proved from the axioms, but whether the axioms form a satisfactory
account of effective calculability is a *further* question. If
they do not, then this “proof” of Church’s thesis
could carry no conviction. Which is to say, a proof of this sort will
be convincing only to one who accepts another thesis, namely that the
axioms are indeed a satisfactory account of effective calculability.
This is a Churchian meta-thesis. Church’s thesis would have been
proved, but only at the expense of throwing up another, unproved,
proved from the axioms, but whether the axioms form a satisfactory
account of effective calculability is a *further* question. If
they do not, then this “proof” of Church’s thesis
could carry no conviction. Which is to say, a proof of this sort will
be convincing only to one who accepts another thesis, namely that the
axioms are indeed a satisfactory account of effective calculability.
This is a Churchian meta-thesis. Church’s thesis would have been
proved, but only at the expense of throwing up another, unproved,
thesis seemingly of the same nature.

axioms are indeed a satisfactory account of effective calculability.
This is a Churchian meta-thesis. Church’s thesis would have been
proved, but only at the expense of throwing up another, unproved,
thesis seemingly of the same nature.

There is further discussion of difficulties associated with the idea
of proving the Church-Turing thesis in
[Section 4.3.5](#TuriTheo),
[Section 4.5](#KripVersArguII), and
[Section 4.6](#TuriStatThes).
### 4.1 The inductive and equivalence arguments {#-41-the-inductive-and-equivalence-arguments}

Although there have from time to time been attempts to call the
Church-Turing thesis into question (for example by Kalmár in
his 1959; Mendelson replied in his 1963), the summary of the situation
that Turing gave in 1948 is no less true today: “it is now
agreed amongst logicians that ‘calculable by L.C.M.’ is
the correct accurate rendering” of the informal concept of
effectiveness.

bolstered Church’s just quoted *equivalence argument*,
pointing out that “Several other characterizations … have
turned out to be equivalent” (1952: 320). As well as the
characterizations mentioned by Church, Kleene included computability
by Turing machine, Post’s canonical and normal systems (Post
1943, 1946), and Gödel’s notion of reckonability
(Gödel 1936). (Turing’s student and lifelong friend Robin
Gandy picturesquely called Church’s equivalence argument the
“argument by confluence” [Gandy 1988: 78].)

Gandy picturesquely called Church’s equivalence argument the
“argument by confluence” [Gandy 1988: 78].)

In modern times, the equivalence argument can be presented even more
forcefully: All attempts to give an exact characterization of the
intuitive notion of an effectively calculable function have turned out
to be *equivalent*, in the sense that each characterization
offered has been proved to pick out the same class of functions,
namely those that are computable by Turing machine. The equivalence
argument is often considered to be very strong evidence for the
In modern times, the equivalence argument can be presented even more
forcefully: All attempts to give an exact characterization of the
intuitive notion of an effectively calculable function have turned out
to be *equivalent*, in the sense that each characterization
offered has been proved to pick out the same class of functions,
namely those that are computable by Turing machine. The equivalence
argument is often considered to be very strong evidence for the
thesis, because of the *diversity* of the various formal
characterizations involved. Apart from the many different
characterizations already mentioned in
namely those that are computable by Turing machine. The equivalence
argument is often considered to be very strong evidence for the
thesis, because of the *diversity* of the various formal
characterizations involved. Apart from the many different
characterizations already mentioned in
[Section 1](#ThesHist)
and
[Section 3](#OtheApprComp),
there are also analyses in terms of register machines (Shepherdson
& Sturgis 1963), Markov algorithms (Markov 1951), and other
The equivalence argument may be summed up by saying that the concept
of effective calculability—or the concept of computability
simpliciter—has turned out to be
*formalism-transcendent*, or even “formalism-free”
(Kennedy 2013: 362), in that all these different formal approaches
pick out exactly the *same* class of functions.

Indeed, there is not even a need to distinguish, within any given
formal approach, systems of different orders or types. Gödel
noted in an abstract published in 1936 that the concept
### 4.2 Skepticism about the inductive and equivalence arguments {#-42-skepticism-about-the-inductive-and-equivalence-arguments}

It is a general feature of inductive arguments that, while they may
supply strong evidence, they nevertheless do not establish their
conclusions with certainty. A stronger argument for the Church-Turing
thesis is to be desired. Gandy said that the inductive argument

> cannot settle the philosophical (or foundational) question. It might
> happen that one day some genius established an entirely new sort of
> calculation. (Gandy 1988: 79)
The equivalence argument has also been deemed unsatisfactory.
Dershowitz and Gurevich call it “weak” (2008: 304). After
all, the fact that a number of statements are equivalent does not show
the statements are true, only that if one is true, all are—and
if one is false, all are. Kreisel wrote:

> The support for Church’s thesis … certainly does not
> consist in … the equivalence of different characterizations:
> what excludes the case of a *systematic* error? (Kreisel 1965:
> 144)
> consist in … the equivalence of different characterizations:
> what excludes the case of a *systematic* error? (Kreisel 1965:
> 144)

Mendelson put the point more mildly, saying that the equivalence
argument is “not conclusive”:

> It is conceivable that all the equivalent notions define a concept
> that is related to, but not identical with, effective computability.
> (Mendelson 1990: 228)
Mendelson put the point more mildly, saying that the equivalence
argument is “not conclusive”:

> It is conceivable that all the equivalent notions define a concept
> that is related to, but not identical with, effective computability.
> (Mendelson 1990: 228)

Clearly, what is required is a direct argument for the thesis from
first principles. Turing’s argument I fills this role.

first principles. Turing’s argument I fills this role.

### 4.3 Turing’s argument I {#-43-turings-argument-i}

The logico-philosophical arguments that Turing gave in Section 9 of
“On Computable Numbers” are outstanding among the reasons
for accepting the thesis.

He introduced argument I as “only an elaboration” of
remarks at the beginning of his 1936 paper—such as:
(1936a: 357). These included the stipulations that the list of axioms
of the logic must be either finite or enumerably infinite, and that
each rule of the logic must specify an “effectively calculable
operation” (the latter is necessary, he said, if the logic
“is to serve at all the purposes for which a system of symbolic
logic is usually intended”). Having introduced this alternative
method of characterizing effective calculability, Church then went on
to argue that every function (of one positive integer) that is
“calculable within the logic” in this way is also
recursive. He concluded, in support of Church’s thesis, that the
“proof of the equivalence of two definitions”,
adding—“in case the new definition has a greater intuitive
appeal” (1936 [2004: 75]).

Turing’s argument, unlike Church’s, does involve a
specific symbolic logic, namely Hilbert’s first-order predicate
calculus. Argument II hinges on a proposition that can be called

> **Turing’s provability theorem**:
>   
1936 [2004: 78]). In other words, he proved the equivalence of the two
definitions, as promised.

#### 4.4.4 Comparing the Church and Turing arguments {#-444-comparing-the-church-and-turing-arguments}

Returning to Church’s step-by-step argument, there is an air of
jiggery-pokery about it. Church wished to conclude that functions
“calculable within the logic” are recursive, and, in the
course of arguing for this, he found it necessary to assert that each
rule of the logic is a recursive operation, on the basis that each
> The assumption that a proof connecting intuitive and precise
> mathematical notions is impossible is patently false. In fact, half of
> CT (the “easier” half), the assertion that all
> partial-recursive functions are effectively computable, is
> acknowledged to be obvious in all textbooks in recursion theory. A
> straightforward argument can be given for it…. This simple
> argument is as clear a proof as I have seen in mathematics, and it is
> a proof in spite of the fact that it involves the intuitive notion of
> effective computability. (Mendelson 1990: 232–233)

### 5.2 The “equivalence fallacy” {#-52-the-equivalence-fallacy}

A common argument for the maximality thesis, or an equivalent, cites
the fact, noted above, that many different attempts to analyse the
informal notion of computability in precise terms—attempts by
Turing, Church, Post, Markov, and others—turned out to be
*equivalent* to one another, in the sense that each analysis
provably picks out the same class of functions, namely those functions
computable by Turing machines.

equivalence argument for the
thesis—[Section 4.1](#InduEquiArgu)).
Some go further and take this convergence to be evidence also for the
maximality thesis. Newell, for example, presented the convergence of
the analyses given by Turing, Church, Post, Markov, et al., as showing
that

> all attempts to … formulate … general notions of
> mechanism … lead to classes of machines that are equivalent in
> that they encompass *in toto* exactly the same set of
are of the concept of an effective method: The equivalence of the
analyses bears only on the question of the extent of what is
*humanly* computable, not on the further question whether
functions generatable by *machines* could extend beyond what is
in principle humanly computable.

### 5.3 Watching our words {#-53-watching-our-words}

It may be helpful at this point to survey some standard technical
terminology that could set traps for the unwary.
in principle humanly computable.

### 5.3 Watching our words {#-53-watching-our-words}

It may be helpful at this point to survey some standard technical
terminology that could set traps for the unwary.

#### 5.3.1 The word “computable” {#-531-the-word-computable}

As already emphasized, when Turing talks about computable numbers, he
computational operation, even if the functions computable in principle
using Turing-machine operations *plus* equilibrating include
functions that are not computable by an unaided Turing machine (Doyle
2002: 519).

#### 5.3.4 The word “mechanical” {#-534-the-word-mechanical}

There is a world of difference between the technical and everyday
meanings of “mechanical”. In the technical literature,
“mechanical” and “effective” are usually used
> at least in principle, to make future computers more efficient, one
> only needs to focus on improving the implementation technology of
> present-day computer designs. (2003: 101)

Unlike the original Church-Turing thesis (whose status is
“something between” a theorem and a definition) ECT is
neither a logico-mathematical theorem nor a definition. If it is true,
then its truth is a consequence of the laws of physics—and it
might not be true. (Although it is trivial if, contrary to a standard
but unproved assumption in computer science, P = NP.)
but unproved assumption in computer science, P = NP.)

The second complexity-theoretic version of the thesis involves the
concept of a *probabilistic Turing machine* (due to Rabin &
Scott 1959). Vazirani and Aharonov state the thesis:

> [T]he extended Church-Turing thesis … asserts that any
> reasonable computational model can be simulated efficiently by the
> standard model of classical computation, namely, a probabilistic
> Turing machine. (Aharonov & Vazirani 2013: 329)
> I can now state the physical version of the Church-Turing principle:
> “Every finitely realizable physical system can be perfectly
> simulated by a universal model computing machine operating by finite
> means”. This formulation is both better defined and more
> physical than Turing’s own way of expressing it. (Deutsch 1985:
> 99)

This thesis is certainly “more physical” than
Turing’s thesis. It is, however, a completely *different*
claim from Turing’s own, so it is potentially confusing to
assumptions, the behavior of *every* discrete deterministic
mechanism is calculable by Turing machine. In some respects, the Gandy
argument resembles and extends Turing’s argument I, and Gandy
regarded it as an improved and more general alternative to
Turing’s I (1980: 145). He emphasized that (unlike
Turing’s argument), his argument takes “parallel working
into account” (1980: 124–5); and it is this that accounts
for much of the additional complexity of Gandy’s analysis as
compared to Turing’s.

set-theoretic derivation that makes very general physical assumptions
(namely, the four axioms mentioned in
[Section 3.4](#ModeAxioAnal)).
These assumptions include, for instance, a lower bound on the
dimensions of a mechanism’s components, and an upper bound on
the speed of propagation of effects and signals. (The argument aims to
cover only mechanisms obeying the principles of Relativity.) Gandy
expressed his various physical assumptions set-theoretically, by means
of precise axioms, which he called Principles I – IV. Principle
III, for example, captures the idea that there is a bound on the
(namely, the four axioms mentioned in
[Section 3.4](#ModeAxioAnal)).
These assumptions include, for instance, a lower bound on the
dimensions of a mechanism’s components, and an upper bound on
the speed of propagation of effects and signals. (The argument aims to
cover only mechanisms obeying the principles of Relativity.) Gandy
expressed his various physical assumptions set-theoretically, by means
of precise axioms, which he called Principles I – IV. Principle
III, for example, captures the idea that there is a bound on the
number of types of basic parts (atoms) from which the states of the
These assumptions include, for instance, a lower bound on the
dimensions of a mechanism’s components, and an upper bound on
the speed of propagation of effects and signals. (The argument aims to
cover only mechanisms obeying the principles of Relativity.) Gandy
expressed his various physical assumptions set-theoretically, by means
of precise axioms, which he called Principles I – IV. Principle
III, for example, captures the idea that there is a bound on the
number of types of basic parts (atoms) from which the states of the
machine are uniquely assembled; and Principle IV—which Gandy
called the “principle of local causation”—captures
cover only mechanisms obeying the principles of Relativity.) Gandy
expressed his various physical assumptions set-theoretically, by means
of precise axioms, which he called Principles I – IV. Principle
III, for example, captures the idea that there is a bound on the
number of types of basic parts (atoms) from which the states of the
machine are uniquely assembled; and Principle IV—which Gandy
called the “principle of local causation”—captures
the idea that each state-transition must be determined by the
*local environments* of the parts of the mechanism that change
in the transition.
expressed his various physical assumptions set-theoretically, by means
of precise axioms, which he called Principles I – IV. Principle
III, for example, captures the idea that there is a bound on the
number of types of basic parts (atoms) from which the states of the
machine are uniquely assembled; and Principle IV—which Gandy
called the “principle of local causation”—captures
the idea that each state-transition must be determined by the
*local environments* of the parts of the mechanism that change
in the transition.

of precise axioms, which he called Principles I – IV. Principle
III, for example, captures the idea that there is a bound on the
number of types of basic parts (atoms) from which the states of the
machine are uniquely assembled; and Principle IV—which Gandy
called the “principle of local causation”—captures
the idea that each state-transition must be determined by the
*local environments* of the parts of the mechanism that change
in the transition.

Gandy was very clear that his argument does not apply to continuous
machine are uniquely assembled; and Principle IV—which Gandy
called the “principle of local causation”—captures
the idea that each state-transition must be determined by the
*local environments* of the parts of the mechanism that change
in the transition.

Gandy was very clear that his argument does not apply to continuous
systems—analogue machines, as he called them—and
non-relativistic systems. (Extracts from unpublished work by Gandy, in
which he attempted to develop a companion argument for analogue
called the “principle of local causation”—captures
the idea that each state-transition must be determined by the
*local environments* of the parts of the mechanism that change
in the transition.

Gandy was very clear that his argument does not apply to continuous
systems—analogue machines, as he called them—and
non-relativistic systems. (Extracts from unpublished work by Gandy, in
which he attempted to develop a companion argument for analogue
machines, are included in Copeland & Shagrir 2007.) However, the
outside the scope of Gandy’s principles (Gurevich 2012; Copeland
& Shagrir 2007). Gurevich concludes that Gandy has not shown
“that his axioms are satisfied by all discrete mechanical
devices”, and Shagrir says there is no “basis for claiming
that Gandy characterized finite machine computation” (Gurevich
2012: 36, Shagrir 2002: 234). It will be useful to give some examples
of discrete deterministic systems that, in one way or another, evade
Gandy’s conclusion that the behavior of every such system is
calculable by Turing machine.

“that his axioms are satisfied by all discrete mechanical
devices”, and Shagrir says there is no “basis for claiming
that Gandy characterized finite machine computation” (Gurevich
2012: 36, Shagrir 2002: 234). It will be useful to give some examples
of discrete deterministic systems that, in one way or another, evade
Gandy’s conclusion that the behavior of every such system is
calculable by Turing machine.

First, it is relatively trivial that mechanisms *satisfying*
Gandy’s four principles may nevertheless produce uncomputable
Gandy’s four principles may nevertheless produce uncomputable
output from computable input if embedded in a universe whose physical
laws have Turing-uncomputability built into them, e.g., via a temporal
variable (Copeland & Shagrir 2007). Moreover, some asynchronous
algorithms fall outside the scope of Gandy’s principles
(Gurevich 2012; Copeland & Shagrir 2007). Second, certain
(notional) discrete deterministic “relativistic computers”
also fall outside the scope of Gandy’s principles. Relativistic
computers were described in a 1987 lecture by Pitowsky (Pitowsky
1990), and in Hogarth 1994 and Etesi & Németi 2002. The
algorithms fall outside the scope of Gandy’s principles
(Gurevich 2012; Copeland & Shagrir 2007). Second, certain
(notional) discrete deterministic “relativistic computers”
also fall outside the scope of Gandy’s principles. Relativistic
computers were described in a 1987 lecture by Pitowsky (Pitowsky
1990), and in Hogarth 1994 and Etesi & Németi 2002. The
idea is outlined in the entry on
[computation in physical systems](../computation-physicalsystems/);
for further discussion see Shagrir and Pitowsky 2003, Copeland and
Shagrir 2020.
also fall outside the scope of Gandy’s principles. Relativistic
computers were described in a 1987 lecture by Pitowsky (Pitowsky
1990), and in Hogarth 1994 and Etesi & Németi 2002. The
idea is outlined in the entry on
[computation in physical systems](../computation-physicalsystems/);
for further discussion see Shagrir and Pitowsky 2003, Copeland and
Shagrir 2020.

The Németi relativistic computer makes use of gravitational
time-dilation effects in order to compute (in a broad sense) a
with presently accepted scientific principles” and that, in
particular, “the principles of quantum mechanics are not
violated”. They suggest moreover that humans might “even
build” a relativistic computer “sometime in the
future” (Andréka, Németi, & Németi
2009: 501).

According to Gandy,

1. “A discrete deterministic mechanical device satisfies
particular, “the principles of quantum mechanics are not
violated”. They suggest moreover that humans might “even
build” a relativistic computer “sometime in the
future” (Andréka, Németi, & Németi
2009: 501).

According to Gandy,

1. “A discrete deterministic mechanical device satisfies
   principles I-IV” (he called this “Thesis P”; Gandy
   principles I-IV” (he called this “Thesis P”; Gandy
   1980: 126), and
2. “What can be calculated by a device satisfying principles
   I-IV is computable” (he labelled this
   “Theorem”).

1 and 2 together yield: *What can be calculated by a discrete
deterministic mechanical device is (Turing-machine)
computable*.

2. “What can be calculated by a device satisfying principles
   I-IV is computable” (he labelled this
   “Theorem”).

1 and 2 together yield: *What can be calculated by a discrete
deterministic mechanical device is (Turing-machine)
computable*.

However, the Németi computer is a discrete, deterministic
mechanical device, and yet is able to calculate functions that are not
specified in Gandy’s Principles
(“Gandy-deterministic”) is narrower than the intuitive
sense of “deterministic”, where a deterministic system is
one obeying laws that involve no randomness or stochasticity.
Relativistic computers are deterministic but not Gandy-deterministic.
(For a fuller discussion, see Copeland, Shagrir, & Sprevak
2018.)

In conclusion, Gandy’s analysis has made a considerable
contribution to the current understanding of machine computation. But,
Copeland & Shagrir 2020 for discussion of this assumption). This
is because there is no algorithm for calculating whether a universal
Turing machine halts on every given input—i.e., there is no
algorithm for calculating that aspect of the machine’s behavior.
The question remains, however, whether the Total thesis is infringed
by any systems that are “more physical” than the universal
machine. (Notice that such systems, if any exist, do not necessarily
also infringe the Deutsch-Wolfram thesis, since it is possible that,
even though answers to certain physical questions about the system are
uncomputable, the system is nevertheless able to be simulated by a
* Bernays, Paul, 1918, “Beiträge zur axiomatischen
  Behandlung des Logik-Kalküls”, Habilitationsschrift,
  University of Göttingen. Bernays Papers, ETH Zurich (Hs
  973.192).
* Bernays, Paul and Moses Schönfinkel, 1928, “Zum
  Entscheidungsproblem der mathematischen Logik”,
  *Mathematische Annalen*, 99(1): 342–372.
  doi:10.1007/BF01459101
* Bernstein, Ethan and Umesh Vazirani, 1997, “Quantum
  Complexity Theory”, *SIAM Journal on Computing*, 26(5):
* Church, Alonzo, 1932, “A Set of Postulates for the
  Foundation of Logic”, *Annals of Mathematics*, second
  series 33(2): 346–366. doi:10.2307/1968337
* –––, 1933, “A Set of Postulates For the
  Foundation of Logic (2)”, *Annals of Mathematics*, second
  series 34(4): 839–864. doi:10.2307/1968702
* –––, 1935a, “An Unsolvable Problem of
  Elementary Number Theory, Preliminary Report” (abstract),
  *Bulletin of the American Mathematical Society*, 41(6):
  332–333. Full paper in Church 1936b.
* –––, 1933, “A Set of Postulates For the
  Foundation of Logic (2)”, *Annals of Mathematics*, second
  series 34(4): 839–864. doi:10.2307/1968702
* –––, 1935a, “An Unsolvable Problem of
  Elementary Number Theory, Preliminary Report” (abstract),
  *Bulletin of the American Mathematical Society*, 41(6):
  332–333. Full paper in Church 1936b.
* –––, 1935b, letter to Kleene, 29 November 1935.
  Excerpt in Davis 1982: 9.
* –––, 1935c, “A Proof of Freedom from
  Computation: How General Are Gandy’s Principles for
  Mechanisms?”, *Minds and Machines*, 17(2): 217–231.
  doi:10.1007/s11023-007-9058-2
* –––, 2011, “Do Accelerating Turing
  Machines Compute the Uncomputable?”, *Minds and
  Machines*, 21(2): 221–239.
  doi:10.1007/s11023-011-9238-y
* –––, 2013, “Turing versus Gödel on
  Computability and the Mind”, in Copeland, Posy, and Shagrir
  2013: 1–33 (ch. 1).
  Axiomatization of Computability and Proof of Church’s
  Thesis”, *Bulletin of Symbolic Logic*, 14(3):
  299–350. doi:10.2178/bsl/1231081370
* Deutsch, David, 1985, “Quantum Theory, the
  Church–Turing Principle and the Universal Quantum
  Computer”, *Proceedings of the Royal Society of London.
  Series A. Mathematical and Physical Sciences*, 400(1818):
  97–117. doi:10.1098/rspa.1985.0070
* Doyle, Jon, 1982, “What is Church’s Thesis? An
  Outline”, Laboratory for Computer Science, MIT.
  Church–Turing Principle and the Universal Quantum
  Computer”, *Proceedings of the Royal Society of London.
  Series A. Mathematical and Physical Sciences*, 400(1818):
  97–117. doi:10.1098/rspa.1985.0070
* Doyle, Jon, 1982, “What is Church’s Thesis? An
  Outline”, Laboratory for Computer Science, MIT.
* –––, 2002, “What Is Church’s Thesis?
  An Outline”, *Minds and Machines*, 12(4): 519–520.
  doi:10.1023/A:1021126521437
* Earman, John, 1986, *A Primer on Determinism*, Dordrecht:
* Gandy, Robin, 1980, “Church’s Thesis and Principles
  for Mechanisms”, in *The Kleene Symposium*, Jon Barwise,
  H. Jerome Keisler, and Kenneth Kunen (eds), Amsterdam: North-Holland,
  123–148. doi:10.1016/S0049-237X(08)71257-6
* –––, 1988, “The Confluence of Ideas in
  1936”, in *The Universal Turing Machine: A Half-Century
  Survey*, Rolf Herken (ed.), New York: Oxford University Press,
  51–102.
* Geroch, Robert and James B. Hartle, 1986, “Computability and
  Physical Theories”, *Foundations of Physics*, 16(6):
* Gödel, Kurt, 1930, “Die Vollständigkeit der Axiome
  des logischen Funktionenkalküls”, *Monatshefte für
  Mathematik und Physik*, 37: 349–360.
  doi:10.1007/BF01696781
* –––, 1931, “Über formal
  unentscheidbare Sätze der Principia Mathematica und verwandter
  Systeme I”, *Monatshefte für Mathematik und Physik*,
  38: 173–198. doi:10.1007/BF01700692
* –––, 1933, “Zum Entscheidungsproblem des
  logischen Funktionenkalküls”, *Monatshefte für
* –––, 1917, “Axiomatisches Denken”,
  *Mathematische Annalen*, 78(1–4): 405–415.
  doi:10.1007/BF01457115
* –––, 1922, “Neubegründung der
  Mathematik. Erste Mitteilung”, *Abhandlungen aus dem
  Mathematischen Seminar der Universität Hamburg*, 1:
  157–177. doi:10.1007/BF02940589
* –––, 1926 [1967], “Über das
  Unendliche”, *Mathematische Annalen*, 95(1):
  161–190. Translated as “On the Infinite” in van
  of Postulates”, *Proceedings of the London Mathematical
  Society*, second series 25: 115–142.
  doi:10.1112/plms/s2-25.1.115
* –––, 1927, “Theorems on Deducibility
  (Second Paper)”, *Annals of Mathematics*, second series
  28(1/4): 459–471. doi:10.2307/1968390
* Langton, Christopher G., 1989, “Artificial Life”, in
  *Artificial Life: The Proceedings of An Interdisciplinary Workshop
  on the Synthesis and Simulation of Living Systems, Held September,
  1987 in Los Alamos, New Mexico*, Christopher G. Langton (ed.),
* –––, 2008, “Church Without Dogma: Axioms
  for Computability”, in *New Computational Paradigms*, S.
  Barry Cooper, Benedikt Löwe, and Andrea Sorbi (eds), New York,
  NY: Springer New York, 139–152.
  doi:10.1007/978-0-387-68546-5\_7
* Siegelmann, Hava T., 2003, “Neural and Super-Turing
  Computing”, *Minds and Machines*, 13(1): 103–114.
  doi:10.1023/A:1021376718708
* Siegelmann, Hava T. and Eduardo D. Sontag, 1992, “On the
  Computational Power of Neural Nets”, in *Proceedings of the

## Key Implications {#-key-implications}

### Predictions & Phenomena {#-predictions--phenomena}
formulations of the thesis. A common one is that every effective
computation can be carried out by a Turing machine (i.e., by
Turing’s abstract computing machine, which in its universal form
encapsulates the fundamental logical principles of the stored-program
all-purpose digital computer). Modern reimaginings of the
Church-Turing thesis transform it, extending it to fundamental
physics, complexity theory, exotic algorithms, and cognitive science.
It is important to be aware though that some of the theses nowadays
referred to as the Church-Turing thesis are at best *very*
distant relatives of the thesis advanced by Church and Turing.
The Church-Turing thesis concerns the concept of an *effective*
or *systematic* or *mechanical* method, as used in
logic, mathematics and computer science. “Effective” and
its synonyms “systematic” and “mechanical” are
terms of art in these disciplines: they do not carry their everyday
meaning. A method, or procedure, \(M\), for achieving some desired
result is called “effective” (or “systematic”
or “mechanical”) just in case:

1. \(M\) is set out in terms of a finite number of exact instructions
logic, mathematics and computer science. “Effective” and
its synonyms “systematic” and “mechanical” are
terms of art in these disciplines: they do not carry their everyday
meaning. A method, or procedure, \(M\), for achieving some desired
result is called “effective” (or “systematic”
or “mechanical”) just in case:

1. \(M\) is set out in terms of a finite number of exact instructions
   (each instruction being expressed by means of a finite number of
   symbols);
result is called “effective” (or “systematic”
or “mechanical”) just in case:

1. \(M\) is set out in terms of a finite number of exact instructions
   (each instruction being expressed by means of a finite number of
   symbols);
2. \(M\) will, if carried out without error, produce the desired
   result in a finite number of steps;
3. \(M\) can (in practice or in principle) be carried out by a human
   being unaided by any machinery except paper and pencil;
A well-known example of an effective method is the truth-table test
for tautologousness. In principle, a human being who works by rote
could apply this test successfully to any formula of the propositional
calculus—given sufficient time, tenacity, paper, and pencils
(although in practice the test is unworkable for any formula
containing more than a few propositional variables).

### 1.1 Note on terminology {#-11-note-on-terminology}

Statements that there is an effective method for achieving
Statements that there is an effective method for achieving
such-and-such a result are commonly expressed by saying that there is
an effective method for obtaining the values of such-and-such a
mathematical *function*.

For example, that there is an effective method for determining whether
or not any given formula of the propositional calculus is a tautology
(such as the truth-table method) is expressed in function-speak by
saying there is an effective method for obtaining the values of a
function, call it \(T\), whose domain is the set of formulae of the
an effective method for obtaining the values of such-and-such a
mathematical *function*.

For example, that there is an effective method for determining whether
or not any given formula of the propositional calculus is a tautology
(such as the truth-table method) is expressed in function-speak by
saying there is an effective method for obtaining the values of a
function, call it \(T\), whose domain is the set of formulae of the
propositional calculus and whose value for any given formula \(x\),
written \(T(x)\), is 1 or 0 according to whether \(x\) is, or is not,
For example, that there is an effective method for determining whether
or not any given formula of the propositional calculus is a tautology
(such as the truth-table method) is expressed in function-speak by
saying there is an effective method for obtaining the values of a
function, call it \(T\), whose domain is the set of formulae of the
propositional calculus and whose value for any given formula \(x\),
written \(T(x)\), is 1 or 0 according to whether \(x\) is, or is not,
a tautology.

### 1.2 Making the informal concept of an effective method precise {#-12-making-the-informal-concept-of-an-effective-method-precise}
saying there is an effective method for obtaining the values of a
function, call it \(T\), whose domain is the set of formulae of the
propositional calculus and whose value for any given formula \(x\),
written \(T(x)\), is 1 or 0 according to whether \(x\) is, or is not,
a tautology.

### 1.2 Making the informal concept of an effective method precise {#-12-making-the-informal-concept-of-an-effective-method-precise}

The notion of an effective method or procedure is an informal one, and
attempts to characterize effectiveness, such as the above, lack rigor,
### 1.2 Making the informal concept of an effective method precise {#-12-making-the-informal-concept-of-an-effective-method-precise}

The notion of an effective method or procedure is an informal one, and
attempts to characterize effectiveness, such as the above, lack rigor,
for the key requirement that the method must demand no insight,
intuition or ingenuity is left unexplicated.

One of Alan Turing’s achievements, in his famous paper of 1936,
was to present a formally exact predicate with which the informal
predicate “can be done by means of an effective method”
The notion of an effective method or procedure is an informal one, and
attempts to characterize effectiveness, such as the above, lack rigor,
for the key requirement that the method must demand no insight,
intuition or ingenuity is left unexplicated.

One of Alan Turing’s achievements, in his famous paper of 1936,
was to present a formally exact predicate with which the informal
predicate “can be done by means of an effective method”
may be replaced (Turing 1936). Alonzo Church, working independently,
did the same (Church 1936a).
attempts to characterize effectiveness, such as the above, lack rigor,
for the key requirement that the method must demand no insight,
intuition or ingenuity is left unexplicated.

One of Alan Turing’s achievements, in his famous paper of 1936,
was to present a formally exact predicate with which the informal
predicate “can be done by means of an effective method”
may be replaced (Turing 1936). Alonzo Church, working independently,
did the same (Church 1936a).

predicate “can be done by means of an effective method”
may be replaced (Turing 1936). Alonzo Church, working independently,
did the same (Church 1936a).

The replacement predicates that Church and Turing proposed were, on
the face of it, very different from one another. However, these
predicates turned out to be *equivalent*, in the sense that
each picks out the same set (call it \(S\)) of mathematical functions.
The Church-Turing thesis is the assertion that this set \(S\) contains
*every* function whose values can be obtained by a method or
procedure satisfying the above conditions for effectiveness.

Since it can also be shown that there are no functions in \(S\)
*other than* ones whose values can be obtained by a method
satisfying the above conditions for effectiveness, the Church-Turing
thesis licenses replacing the informal claim “There is an
effective method for obtaining the values of function \(f\)” by
the formal claim “\(f\) is a member of \(S\)”—or by
any other formal claim equivalent to this one.

satisfying the above conditions for effectiveness, the Church-Turing
thesis licenses replacing the informal claim “There is an
effective method for obtaining the values of function \(f\)” by
the formal claim “\(f\) is a member of \(S\)”—or by
any other formal claim equivalent to this one.

When the Church-Turing thesis is expressed in terms of the replacement
concept proposed by Turing, it is appropriate to refer to the thesis
also as “Turing’s thesis”; and as
“Church’s thesis” when expressed in terms of one or
effective method for obtaining the values of function \(f\)” by
the formal claim “\(f\) is a member of \(S\)”—or by
any other formal claim equivalent to this one.

When the Church-Turing thesis is expressed in terms of the replacement
concept proposed by Turing, it is appropriate to refer to the thesis
also as “Turing’s thesis”; and as
“Church’s thesis” when expressed in terms of one or
another of the formal replacements proposed by Church.

thesis—that whenever there is an effective method for obtaining
the values of a mathematical function, the function can be computed by
a Turing machine.

The converse claim—amounting to the claim mentioned above, that
there are no functions in \(S\) *other than* ones whose values
can be obtained by an effective method—is easily established,
since a Turing machine program is itself a specification of an
effective method. Without exercising any insight, intuition, or
ingenuity, a human being can work through the instructions in the
can be obtained by an effective method—is easily established,
since a Turing machine program is itself a specification of an
effective method. Without exercising any insight, intuition, or
ingenuity, a human being can work through the instructions in the
program and carry out the required operations.

If Turing’s thesis is correct, then talk about the existence and
non-existence of effective methods and procedures can be replaced
throughout mathematics, logic and computer science by talk about the
existence or non-existence of Turing machine programs.
effective method. Without exercising any insight, intuition, or
ingenuity, a human being can work through the instructions in the
program and carry out the required operations.

If Turing’s thesis is correct, then talk about the existence and
non-existence of effective methods and procedures can be replaced
throughout mathematics, logic and computer science by talk about the
existence or non-existence of Turing machine programs.

Turing stated his thesis in numerous places, with varying degrees of
non-existence of effective methods and procedures can be replaced
throughout mathematics, logic and computer science by talk about the
existence or non-existence of Turing machine programs.

Turing stated his thesis in numerous places, with varying degrees of
rigor. The following formulation is one of the most accessible:

> **Turing’s thesis**:
>   
> L.C.M.s [logical computing machines: Turing’s expression for
number which is able to be calculated by an effective method (that is,
“all numbers which would naturally be regarded as
computable”) is included among the numbers whose decimal
representations can be written out progressively by one or another
Turing machine. In the second, Turing is saying that the operations of
a Turing machine include all those that a human mathematician needs to
use when calculating a number by means of an effective method.

### 1.4 The meaning of “computable” and “computation” in Turing’s thesis {#-14-the-meaning-of-computable-and-computation-in-turings-thesis}

use when calculating a number by means of an effective method.

### 1.4 The meaning of “computable” and “computation” in Turing’s thesis {#-14-the-meaning-of-computable-and-computation-in-turings-thesis}

Turing introduced his machines with the intention of providing an
idealized description of a certain human activity, the tedious one of
*numerical computation*. Until the advent of automatic
computing machines, this was the occupation of many thousands of
people in business, government, and research establishments. These
human rote-workers were in fact called “computers”. Human
computers used effective methods to carry out some aspects of the work
nowadays done by electronic computers. The Church-Turing thesis is
about computation *as this term was used in 1936*, viz. human
computation (to read more on this, turn to
[Section 7](#SomeKeyRemaTuriChur)).

For instance, when Turing says that the operations of an L.C.M.
include all those needed “in the computation of a number”,
he means “in the computation of a number by a human
being”, since that is what computation was in those days.
accordance with an effective method.

### 1.5 Church’s thesis {#-15-churchs-thesis}

Where Turing used the term “purely mechanical”, Church
used “effectively calculable” to indicate that there is an
effective method for obtaining the values of the function; and where
Turing offered an analysis in terms of computability by an L.C.M.,
Church gave two alternative analyses, one in terms of the concept of
*recursion* and the other in terms of
used “effectively calculable” to indicate that there is an
effective method for obtaining the values of the function; and where
Turing offered an analysis in terms of computability by an L.C.M.,
Church gave two alternative analyses, one in terms of the concept of
*recursion* and the other in terms of
*lambda-definability* (λ-definability). He proposed that
we

> define the notion … of an effectively calculable function of
> positive integers by identifying it with the notion of a recursive
effective method for obtaining the values of the function; and where
Turing offered an analysis in terms of computability by an L.C.M.,
Church gave two alternative analyses, one in terms of the concept of
*recursion* and the other in terms of
*lambda-definability* (λ-definability). He proposed that
we

> define the notion … of an effectively calculable function of
> positive integers by identifying it with the notion of a recursive
> function of positive integers (or of a λ-definable function of
> define the notion … of an effectively calculable function of
> positive integers by identifying it with the notion of a recursive
> function of positive integers (or of a λ-definable function of
> positive integers). (Church 1936a: 356)

The concept of a λ-definable function was due to Church and
Kleene, with contributions also by Rosser (Church 1932, 1933, 1935c,
1936a; Church & Rosser 1936; Kleene 1934, 1935a,b, 1936a,b; Kleene
& Rosser 1935; Rosser 1935a,b). A function is said to be
λ-definable if the values of the function can be obtained by a
effectiveness with λ-definability (while preparing his own
paper for publication), he quickly established that the concept of
λ-definability and his concept of computability are equivalent
(by proving the “theorem that all … λ-definable
sequences … are computable” and its converse; Turing 1936
[2004: 88ff]). Thus, in Church’s proposal, the words
“λ-definable function of positive integers” (and
equally the words “recursive function of positive
integers”) can be replaced by “function of positive
integers that is computable by Turing machine”. What Turing
Post referred to Church’s identification of effective
calculability with recursiveness and λ-definability as a
“working hypothesis”, and he quite properly criticized
Church for masking this hypothesis as a *definition*:

> [T]o mask this identification under a definition … blinds us to
> the need of its continual verification. (Post 1936: 105)

This, then, is the “working hypothesis” that, in effect,
Church proposed:
This, then, is the “working hypothesis” that, in effect,
Church proposed:

> **Church’s thesis**:
>   
> A function of positive integers is effectively calculable only if
> λ-definable (or, equivalently, recursive).

The reverse implication, that every λ-definable function of
positive integers is effectively calculable, is commonly referred to
> A function of positive integers is effectively calculable only if
> λ-definable (or, equivalently, recursive).

The reverse implication, that every λ-definable function of
positive integers is effectively calculable, is commonly referred to
as *the converse of Church’s thesis,* although Church
himself did not so distinguish (bundling both theses together in his
“definition”).

If attention is restricted to functions of positive integers,
The reverse implication, that every λ-definable function of
positive integers is effectively calculable, is commonly referred to
as *the converse of Church’s thesis,* although Church
himself did not so distinguish (bundling both theses together in his
“definition”).

If attention is restricted to functions of positive integers,
Church’s thesis and Turing’s thesis are
*extensionally* equivalent. “Extensionally
equivalent” means that the two theses are about one and the same
positive integers is effectively calculable, is commonly referred to
as *the converse of Church’s thesis,* although Church
himself did not so distinguish (bundling both theses together in his
“definition”).

If attention is restricted to functions of positive integers,
Church’s thesis and Turing’s thesis are
*extensionally* equivalent. “Extensionally
equivalent” means that the two theses are about one and the same
class of functions: In view of the previously mentioned results by
the proposition that every effectively calculable function (on the
natural numbers) is recursive (Kleene 1952: 300, 301, 317). The term
“Church-Turing thesis” also seems to have originated with
Kleene—with a flourish of bias in favor of his mentor
Church:

> So Turing’s and Church’s theses are equivalent. We shall
> usually refer to them both as *Church’s thesis*, or in
> connection with that one of its … versions which deals with
> “Turing machines” as the *Church-Turing thesis*.
universal machine can carry out any and every effective procedure,
assuming Turing’s thesis is true. The functional parts of the
abstract universal machine are:

1. the memory in which instructions and data are stored, and
2. the instruction-reading-and-obeying control mechanism.

In that respect, the universal Turing machine is a bare-bones logical
model of almost every modern electronic digital computer.

Turing’s analysis of effectiveness over his own:

> computability by a Turing machine … has the advantage of making
> the identification with effectiveness in the ordinary (not explicitly
> defined) sense evident immediately. (Church 1937a: 43)

He also said that Turing’s analysis has “a more immediate
intuitive appeal” than his own (Church 1941: 41).

Gödel found Turing’s analysis superior to Church’s.
> the identification with effectiveness in the ordinary (not explicitly
> defined) sense evident immediately. (Church 1937a: 43)

He also said that Turing’s analysis has “a more immediate
intuitive appeal” than his own (Church 1941: 41).

Gödel found Turing’s analysis superior to Church’s.
Kleene related that Gödel was unpersuaded by Church’s
thesis until he saw Turing’s formulation:

> proposal to use λ-definability as a definition of effective
> calculability. … It seems that only after Turing’s
> formulation appeared did Gödel accept Church’s thesis.
> (Kleene 1981: 59, 61)

Gödel described Turing’s analysis of computability as
“most satisfactory” and “correct … beyond any
doubt” (Gödel 1951: 304 and 193?: 168). He remarked:

> We had not perceived the sharp concept of mechanical procedures
logical calculus is the problem of devising an effective method for
deciding whether or not a given formula—any formula—is
provable in the calculus. (Here “provable” means that the
formula can be derived, step by logical step, from the axioms and
definitions of the calculus, using only the rules of the calculus.)
For example, if such a method for the classical propositional calculus
is used to test the formula \(A \rightarrow A\) (\(A\) implies \(A\)),
the output will be “Yes, provable”, and if the
contradiction \(A \amp \neg A\) is tested, the output will be
“Not provable”. Such a method is called a *decision
## 2. Backstory: Emergence of the concepts of *effective method* and *decision method* {#-2-backstory-emergence-of-the-concepts-of-effective-method-and-decision-method}

Effective methods are the subject matter of the Church-Turing thesis.
How did this subject matter evolve and how was it elaborated prior to
Church and Turing? This section looks back to an earlier era, after
which
[Section 3](#OtheApprComp)
turns to modern developments.

### 2.1 From simple rules-of-thumb to Siri and beyond {#-21-from-simple-rules-of-thumb-to-siri-and-beyond}
Effective methods are the subject matter of the Church-Turing thesis.
How did this subject matter evolve and how was it elaborated prior to
Church and Turing? This section looks back to an earlier era, after
which
[Section 3](#OtheApprComp)
turns to modern developments.

### 2.1 From simple rules-of-thumb to Siri and beyond {#-21-from-simple-rules-of-thumb-to-siri-and-beyond}

Effective methods are extremely helpful in carrying out many practical
Effective methods are extremely helpful in carrying out many practical
tasks, and their use stretches back into the mists of antiquity,
although it was not until the twentieth century that interest began to
build in analysing their nature. Perhaps the earliest effective
methods to be utilized were rules-of-thumb (as Turing called them) for
arithmetical calculations of various sorts, but whatever their humble
beginnings, the scope of effective methods has widened dramatically
over the centuries. In the Middle Ages, the Catalan philosopher
[Llull](../llull/)
envisaged an effective method for posing and answering questions
build in analysing their nature. Perhaps the earliest effective
methods to be utilized were rules-of-thumb (as Turing called them) for
arithmetical calculations of various sorts, but whatever their humble
beginnings, the scope of effective methods has widened dramatically
over the centuries. In the Middle Ages, the Catalan philosopher
[Llull](../llull/)
envisaged an effective method for posing and answering questions
about the attributes of God, the nature of the soul, the nature of
goodness, and other fundamental issues. Three hundred years later, in
the seventeenth century, Hobbes was asserting that human reasoning
beginnings, the scope of effective methods has widened dramatically
over the centuries. In the Middle Ages, the Catalan philosopher
[Llull](../llull/)
envisaged an effective method for posing and answering questions
about the attributes of God, the nature of the soul, the nature of
goodness, and other fundamental issues. Three hundred years later, in
the seventeenth century, Hobbes was asserting that human reasoning
processes amount to nothing more than (essentially arithmetical)
effective procedures:

envisaged an effective method for posing and answering questions
about the attributes of God, the nature of the soul, the nature of
goodness, and other fundamental issues. Three hundred years later, in
the seventeenth century, Hobbes was asserting that human reasoning
processes amount to nothing more than (essentially arithmetical)
effective procedures:

> By reasoning I understand computation. (Hobbes 1655 [1839]: ch. 1
> sect. 2)

effective procedures:

> By reasoning I understand computation. (Hobbes 1655 [1839]: ch. 1
> sect. 2)

Nowadays, effective methods—algorithms—are the basis for
every job that electronic computers do. According to some computer
scientists, advances in the design of effective methods will soon
usher in human-level artificial intelligence, followed by superhuman
intelligence. Already, virtual assistants such as Siri, Cortana and
Nowadays, effective methods—algorithms—are the basis for
every job that electronic computers do. According to some computer
scientists, advances in the design of effective methods will soon
usher in human-level artificial intelligence, followed by superhuman
intelligence. Already, virtual assistants such as Siri, Cortana and
ChatGPT implement effective methods that produce useful answers to a
wide range of questions.

In its most sublimely general form, the *Entscheidungsproblem*
is the problem of designing an effective general-purpose
scientists, advances in the design of effective methods will soon
usher in human-level artificial intelligence, followed by superhuman
intelligence. Already, virtual assistants such as Siri, Cortana and
ChatGPT implement effective methods that produce useful answers to a
wide range of questions.

In its most sublimely general form, the *Entscheidungsproblem*
is the problem of designing an effective general-purpose
question-answerer, an effective method that is capable of giving the
correct answer, yes or no, to *any* meaningful scientific
ChatGPT implement effective methods that produce useful answers to a
wide range of questions.

In its most sublimely general form, the *Entscheidungsproblem*
is the problem of designing an effective general-purpose
question-answerer, an effective method that is capable of giving the
correct answer, yes or no, to *any* meaningful scientific
question, and perhaps even ethical and metaphysical questions too. The
idea of such a method is almost jaw-dropping. Llull seems to have
glimpsed the concept of a general question-answering method, writing
is the problem of designing an effective general-purpose
question-answerer, an effective method that is capable of giving the
correct answer, yes or no, to *any* meaningful scientific
question, and perhaps even ethical and metaphysical questions too. The
idea of such a method is almost jaw-dropping. Llull seems to have
glimpsed the concept of a general question-answering method, writing
in approximately 1300 of a general art (“*ars*”),
or technique, “by means of which one may know in regard to all
natural things” (*Lo Desconhort*, line 8, in Llull 1986:
99). He dreamed of an *ars generalis* (general technique) that
question-answerer, an effective method that is capable of giving the
correct answer, yes or no, to *any* meaningful scientific
question, and perhaps even ethical and metaphysical questions too. The
idea of such a method is almost jaw-dropping. Llull seems to have
glimpsed the concept of a general question-answering method, writing
in approximately 1300 of a general art (“*ars*”),
or technique, “by means of which one may know in regard to all
natural things” (*Lo Desconhort*, line 8, in Llull 1986:
99). He dreamed of an *ars generalis* (general technique) that
could mechanize the “one general science, with its own general
represent all sorts of truths and consequences by Numbers” and
“then all the results of reasoning can be determined in
numerical fashion” (Leibniz 1685 [1951: 50–51]). He hoped
the method would apply to “Metaphysics, Physics, and
Ethics” just as well as it did to mathematics (1685 [1951: 50]).
This conjectured method could, he thought, be implemented by what he
called a *machina combinatoria*, a combinatorial machine
(Leibniz *n.d.*1; Leibniz 1666). However, there was never much
progress towards his dreamed-of method, and in a letter two years
before his death he wrote:
is supposed to work by means of an effective method, then there can be
no universal *ars inveniendi*—and not even an *ars
inveniendi* that is restricted to all mathematical statements,
since these include statements of the form “\(p\) is
provable”, or even to all purely logical statements.

### 2.3 Logic machines {#-23-logic-machines}

The modern concept of a decision method for a logical calculus did not
develop until the twentieth century. But earlier logicians, including
set out for an effective method in
[Section 1](#ThesHist).
The user first diagrams the premisses of a syllogism and then, as
Quine put it, “we inspect the diagram to see whether the content
of the conclusion has automatically appeared in the diagram as a
result” (Quine 1950: 74). Not all formulae of the functional
calculus are Venn-diagrammable, and Venn’s original method is
limited to testing syllogisms. In the twentieth century, Massey showed
that Venn’s method can be stretched to give a decision procedure
for the monadic functional calculus (Massey 1966).
precise analysis of the idea of an effective decision method. In a
lecture he gave in Zurich in 1917, to the Swiss Mathematical Society,
he emphasized the need to study the concept of “decidability by
a finite number of operations”,
saying—accurately—that this would be “an important
new field of research to develop” (Hilbert 1917: 415). The
lecture considered a number of what he called “most challenging
epistemological problems of a specifically mathematical
character” (1917: 412). Pre-eminent among these was the
“problem of the decidability [*Entscheidbarkeit*] of a
an effective method for answering any specified mathematical or
scientific question found its fullest development (see further the
supplement on
[The Rise and Fall of the *Entscheidungsproblem*](decision-problem.html)).

Hilbert’s earliest publication to mention what we would now call
a decision problem is his 1899 book *Grundlagen der Geometrie*
[Foundations of Geometry]. He said that in the course of his
investigations of Euclidean geometry he was

He described what would now be called an effective method for
determining this, and his term “*beurteilen*”
could, with a trace of anachronism, be translated as
“decide”.

Hilbert expressed the concept of a decision method more clearly the
following year, in his famous turn-of-the-century speech in Paris, to
the International Congress of Mathematicians. He presented
twenty-three unsolved problems, “from the discussion of which an
advancement of science may be expected”. The tenth on his list
Society not long after his return to Harvard, in effect solving a
number of special cases of the *Entscheidungsproblem* (Langford
1926a, 1927).

The Cambridge logician Ramsey, like Turing a Fellow of King’s
College, also worked on the *Entscheidungsproblem* in the
latter part of the 1920s. He died in 1930 (the year before Turing
arrived in Cambridge as an undergraduate), but not before completing a
key paper solving the *Entscheidungsproblem* in special cases
(Ramsey 1930). His work, too, was prominent in the recommended reading
therefore, Turing’s thesis that *if an effective method
exists then it can be carried out by one of his machines*, it
follows that there is no effective method for deciding the full
first-order functional calculus.

## 3. Other Approaches to Computability {#-3-other-approaches-to-computability}

Turing and Church were certainly not the only people to tackle the
problem of analyzing the concept of effectiveness. This section
surveys some other important proposals made during the twentieth and
follows that there is no effective method for deciding the full
first-order functional calculus.

## 3. Other Approaches to Computability {#-3-other-approaches-to-computability}

Turing and Church were certainly not the only people to tackle the
problem of analyzing the concept of effectiveness. This section
surveys some other important proposals made during the twentieth and
twenty-first centuries.

problem of analyzing the concept of effectiveness. This section
surveys some other important proposals made during the twentieth and
twenty-first centuries.

### 3.1 Gödel {#-31-gödel}

Gödel was led to the problem of analyzing effectiveness by his
search for a means to *generalize* his 1931 incompleteness
results (which in their original form applied specifically to the
formal system set out by Whitehead and Russell in their *Principia
Gödel was led to the problem of analyzing effectiveness by his
search for a means to *generalize* his 1931 incompleteness
results (which in their original form applied specifically to the
formal system set out by Whitehead and Russell in their *Principia
Mathematica*). In 1934, he considered an analysis in terms of his
generalized concept of recursion—about a year before Church
first publicly announced his thesis that “the notion of an
effectively calculable function of positive integers should be
identified with that of a recursive function” (Church 1935a;
Gödel 1934, fn. 3; Davis 1982).
effectively calculable function of positive integers should be
identified with that of a recursive function” (Church 1935a;
Gödel 1934, fn. 3; Davis 1982).

But Gödel was doubtful: “I was, at the time … not at
all convinced that my concept of recursion comprises all possible
recursions” (Gödel 1965b). It was Turing’s analysis,
Gödel emphasized, that finally enabled him to generalize his
incompleteness theorems:

effectiveness that was substantially the same as Turing’s (Post
1936; Davis & Sieg 2015). Post’s idealized human
“worker”—or “problem
solver”—operated in a “symbol space”
consisting of “a two way infinite sequence of spaces or
boxes”. A box admitted

> of but two possible conditions, i.e., being empty or unmarked, and
> having a single mark in it, say a vertical stroke. (Post 1936:
> 103)
proposed a logic-based analysis of effectiveness. According to this
analysis, effectively calculable numerical functions are numerical
functions that can be evaluated in what they called a
“*regelrecht*” manner (Hilbert & Bernays 1939:
392–421). In this context, the German word
“*regelrecht*” can be translated
“rule-governed”. Hilbert and Bernays offered the concept
of the *rule-governed evaluation* of a numerical function as a
“sharpening of the concept of computable” (1939: 417).

analysis, effectively calculable numerical functions are numerical
functions that can be evaluated in what they called a
“*regelrecht*” manner (Hilbert & Bernays 1939:
392–421). In this context, the German word
“*regelrecht*” can be translated
“rule-governed”. Hilbert and Bernays offered the concept
of the *rule-governed evaluation* of a numerical function as a
“sharpening of the concept of computable” (1939: 417).

The basic idea is this: To evaluate a numerical function (such as
logical system. On this approach, effective calculability is analysed
as *calculability in a logic*. (Both Church and Turing had
previously discussed the approach—see
[Section 4.4](#TuriArguII).)

The logical system Hilbert and Bernays used to flesh out this idea was
an *equational calculus*, reminiscent of a calculus that
Gödel had detailed in lectures he gave in Princeton in 1934
(Gödel 1934). The theorems of an equational calculus are (as the
name says) *equations*—for example \(2^3 = 8\) and \(x^2
as negation, conjunction, implication, or quantifiers), and every
formula is simply an equation between terms. Three types of equation
are permitted as the initial formulae (or premisses) of deductions in
the system; and the system is required to satisfy three general
conditions that Hilbert and Bernays called “recursivity
conditions”. The rules of the calculus concern substitutions
within equations and are very simple, allowing steps such as:

\[ a = b, f(a) \vdash f(b) \]

ultimately selected an analysis of effective calculability as
calculability *within a logic*, even though Church and Turing
had already presented their analyses in terms of recursive functions
and Turing machines respectively. Hilbert and Bernays went on to use
their analysis to give a new proof of the unsolvability of the
*Entscheidungsproblem* (Hilbert & Bernays 1939:
416–421). This proof quietly marks what must have been an
unsettling, even painful, shift of perspective for them. The idea of a
decision procedure for mathematics had until the Church-Turing result
been central to their thinking, and in Volume 1 of the
when it was still wide open how the intuitive concept of effective
calculability should be formalized (probably during 1934). Gödel
suggested that

> it might be possible, in terms of effective calculability as an
> undefined notion, to state a set of axioms which would embody the
> generally accepted properties of this notion, and to do something on
> that basis. (Church 1935b)

Logicians frequently analyse a concept of interest, e.g., universal
> it might be possible, in terms of effective calculability as an
> undefined notion, to state a set of axioms which would embody the
> generally accepted properties of this notion, and to do something on
> that basis. (Church 1935b)

Logicians frequently analyse a concept of interest, e.g., universal
quantification, not by defining it in terms of other concepts, but by
stating a set of axioms that collectively embody the generally
accepted properties of (say) universal quantification. To follow this
approach in the case of effectiveness, we would “write down some
approach in the case of effectiveness, we would “write down some
axioms about computable functions which most people would agree are
evidently true” (Shoenfield 1993: 26). Shoenfield continued,
“It might be possible to prove Church’s Thesis from such
axioms”, but added: “However, despite strenuous efforts,
no one has succeeded in doing this”.

Moving on a few years, a meeting on *The Prospects for Mathematical
Logic in the Twenty-First Century*, held at the turn of the
millennium, included the following among leading open problems:
  effects: \(\mathrm{C}xyz = xzy\) and \(\mathrm{K}xy = x\).
* Sieg formalized Turing’s analysis of human computation by means
  of four axioms (Sieg 2008). The result, Sieg said, is an axiomatic
  characterization of “the concept ‘mechanical
  procedure’”, and he observed that his system
  “substantiates Gödel’s remarks” (above) that
  one should try to find a set of axioms embodying the generally
  accepted properties of the concept of effectiveness (Sieg 2008:
  150).
* Dershowitz and Gurevich (2008) stated three very general axioms,
  accepted properties of the concept of effectiveness (Sieg 2008:
  150).
* Dershowitz and Gurevich (2008) stated three very general axioms,
  treating computations as discrete, deterministic,
  sequentially-evolving structures of states. They called these
  structures “state-transition systems”, and called the
  three axioms the “Sequential Postulates”. They also used a
  fourth axiom, stipulating that “Only undeniably computable
  operations are available in initial states” (2008: 306). From
  their four axioms, they proved a proposition they called
effectively calculable only if recursive”. Crucially, their
version of Church’s thesis does not even mention the key concept
of effective calculability. The entire project of trying to prove
Church’s (or Turing’s) actual thesis has its share of
philosophical difficulties. For example, suppose someone were to lay
down some axioms expressing claims about effective calculability (as
Sieg for instance has done), and suppose it is possible to prove from
these axioms that a function of positive integers is effectively
calculable only if recursive. Church’s thesis would have been
proved from the axioms, but whether the axioms form a satisfactory
of effective calculability. The entire project of trying to prove
Church’s (or Turing’s) actual thesis has its share of
philosophical difficulties. For example, suppose someone were to lay
down some axioms expressing claims about effective calculability (as
Sieg for instance has done), and suppose it is possible to prove from
these axioms that a function of positive integers is effectively
calculable only if recursive. Church’s thesis would have been
proved from the axioms, but whether the axioms form a satisfactory
account of effective calculability is a *further* question. If
they do not, then this “proof” of Church’s thesis
down some axioms expressing claims about effective calculability (as
Sieg for instance has done), and suppose it is possible to prove from
these axioms that a function of positive integers is effectively
calculable only if recursive. Church’s thesis would have been
proved from the axioms, but whether the axioms form a satisfactory
account of effective calculability is a *further* question. If
they do not, then this “proof” of Church’s thesis
could carry no conviction. Which is to say, a proof of this sort will
be convincing only to one who accepts another thesis, namely that the
axioms are indeed a satisfactory account of effective calculability.
these axioms that a function of positive integers is effectively
calculable only if recursive. Church’s thesis would have been
proved from the axioms, but whether the axioms form a satisfactory
account of effective calculability is a *further* question. If
they do not, then this “proof” of Church’s thesis
could carry no conviction. Which is to say, a proof of this sort will
be convincing only to one who accepts another thesis, namely that the
axioms are indeed a satisfactory account of effective calculability.
This is a Churchian meta-thesis. Church’s thesis would have been
proved, but only at the expense of throwing up another, unproved,
account of effective calculability is a *further* question. If
they do not, then this “proof” of Church’s thesis
could carry no conviction. Which is to say, a proof of this sort will
be convincing only to one who accepts another thesis, namely that the
axioms are indeed a satisfactory account of effective calculability.
This is a Churchian meta-thesis. Church’s thesis would have been
proved, but only at the expense of throwing up another, unproved,
thesis seemingly of the same nature.

There is further discussion of difficulties associated with the idea
axioms are indeed a satisfactory account of effective calculability.
This is a Churchian meta-thesis. Church’s thesis would have been
proved, but only at the expense of throwing up another, unproved,
thesis seemingly of the same nature.

There is further discussion of difficulties associated with the idea
of proving the Church-Turing thesis in
[Section 4.3.5](#TuriTheo),
[Section 4.5](#KripVersArguII), and
[Section 4.6](#TuriStatThes).
effectiveness.

In 1936, both Church and Turing gave various grounds for accepting
their respective theses. Church argued:

> The fact … that two such widely different and (in the opinion
> of the author) equally natural definitions of effective calculability
> [i.e., in terms of λ-definability and recursion] turn out to be
> *equivalent* adds to the strength of the reasons adduced below
> for believing that they constitute as general a characterization of
> of the author) equally natural definitions of effective calculability
> [i.e., in terms of λ-definability and recursion] turn out to be
> *equivalent* adds to the strength of the reasons adduced below
> for believing that they constitute as general a characterization of
> this notion as is consistent with the usual intuitive understanding of
> it. (Church 1936a: 346, emphasis added)

Church’s “reasons adduced below” comprised two not
wholly convincing arguments. Both suffered from the same weakness,
discussed in
intuitive notion of an effectively calculable function have turned out
to be *equivalent*, in the sense that each characterization
offered has been proved to pick out the same class of functions,
namely those that are computable by Turing machine. The equivalence
argument is often considered to be very strong evidence for the
thesis, because of the *diversity* of the various formal
characterizations involved. Apart from the many different
characterizations already mentioned in
[Section 1](#ThesHist)
and
of effective calculability—or the concept of computability
simpliciter—has turned out to be
*formalism-transcendent*, or even “formalism-free”
(Kennedy 2013: 362), in that all these different formal approaches
pick out exactly the *same* class of functions.

Indeed, there is not even a need to distinguish, within any given
formal approach, systems of different orders or types. Gödel
noted in an abstract published in 1936 that the concept
“computable” is *absolute*, in the sense that all
* Every effectively calculable function that has been investigated
  in this respect has turned out to be computable by Turing
  machine.
* All known methods or operations for obtaining new effectively
  calculable functions from given effectively calculable functions are
  paralleled by methods for constructing new Turing machines from given
  Turing machines.

Inductive evidence for the thesis has continued to accumulate. For
example, Gurevich points out that
* All known methods or operations for obtaining new effectively
  calculable functions from given effectively calculable functions are
  paralleled by methods for constructing new Turing machines from given
  Turing machines.

Inductive evidence for the thesis has continued to accumulate. For
example, Gurevich points out that

> As far as the input-output relation is concerned, synchronous parallel
> algorithms and interactive sequential algorithms can be simulated by
  calculable functions from given effectively calculable functions are
  paralleled by methods for constructing new Turing machines from given
  Turing machines.

Inductive evidence for the thesis has continued to accumulate. For
example, Gurevich points out that

> As far as the input-output relation is concerned, synchronous parallel
> algorithms and interactive sequential algorithms can be simulated by
> Turing machines. This gives additional confirmation of the
> have elapsed since Church proposed identifying effectiveness with
> recursiveness, but still those physical theories were eventually found
> lacking. (Dershowitz & Gurevich 2008: 304)

Dershowitz and Gurevich presented a highly relevant example of delayed
discovery (following Barendregt 1997: 187): Any hope that the
effectively calculable functions could be identified with the
*primitive* recursive functions—introduced in 1923
(Skolem 1923; Péter 1935)—evaporated a few years later,
when Ackermann described an effectively calculable function that is
effectively calculable functions could be identified with the
*primitive* recursive functions—introduced in 1923
(Skolem 1923; Péter 1935)—evaporated a few years later,
when Ackermann described an effectively calculable function that is
not primitive recursive (Ackermann 1928).

The equivalence argument has also been deemed unsatisfactory.
Dershowitz and Gurevich call it “weak” (2008: 304). After
all, the fact that a number of statements are equivalent does not show
the statements are true, only that if one is true, all are—and
when Ackermann described an effectively calculable function that is
not primitive recursive (Ackermann 1928).

The equivalence argument has also been deemed unsatisfactory.
Dershowitz and Gurevich call it “weak” (2008: 304). After
all, the fact that a number of statements are equivalent does not show
the statements are true, only that if one is true, all are—and
if one is false, all are. Kreisel wrote:

> The support for Church’s thesis … certainly does not
> that is related to, but not identical with, effective computability.
> (Mendelson 1990: 228)

Clearly, what is required is a direct argument for the thesis from
first principles. Turing’s argument I fills this role.

### 4.3 Turing’s argument I {#-43-turings-argument-i}

The logico-philosophical arguments that Turing gave in Section 9 of
“On Computable Numbers” are outstanding among the reasons
> simulated by effective string manipulations? (Dershowitz &
> Gurevich 2008: 305)

Progressing to the other features on Turing’s list: 2, 3, 4 and
5 are straightforwardly duplicated in the machine.
[Features 6 and 7](#feature6)
are simulated, by letting the machine’s \(m\)-configurations do
duty for the computer’s states of mind (more on that below).
[Feature 8](#feature8)
is duplicated in the machine: the machine’s complex operations
note is in effect a tiny computer program, which both carries out a
single step of the computation and also writes the program that is to
be used at the next step.

Once instruction notes are in the picture, there is no need to refer
to the human computer’s states of mind:

> the state of progress of the computation at any stage is completely
> determined by the note of instructions and the symbols on the tape.
> (Turing 1936 [2004: 79])
fundamental nature of *effective methods*?

Turing’s argument I is a towering landmark and there is now a
sizable literature on these and other questions concerning it. For
more about this important argument see, for starters, Sieg 1994, 2008;
Shagrir 2006; and Copeland & Shagrir 2013.

### 4.4 Turing’s argument II {#-44-turings-argument-ii}

#### 4.4.1 Calculating in a logic {#-441-calculating-in-a-logic}
characterizing effectively calculable functions (or, in Turing’s
case, computable functions or numbers). The alternative method
involves derivability in one or another symbolic logic: The concept of
effective calculability (or of computability) is characterized in
terms of *calculability within the logic* (see
[Section 3.3](#HilbBern)).
Schematically, the characterization is of the form: A function is
effectively calculable (or computable) if each successive value of the
function is derivable within the logic. The next step of the argument
is then to establish that the new characterization (whatever it is) is
effective calculability (or of computability) is characterized in
terms of *calculability within the logic* (see
[Section 3.3](#HilbBern)).
Schematically, the characterization is of the form: A function is
effectively calculable (or computable) if each successive value of the
function is derivable within the logic. The next step of the argument
is then to establish that the new characterization (whatever it is) is
equivalent to the old. In Church’s case, this amounts to arguing
that the new characterization is equivalent to his characterization in
terms of either recursiveness or λ-definability. Finally, the
effectively calculable (or computable) if each successive value of the
function is derivable within the logic. The next step of the argument
is then to establish that the new characterization (whatever it is) is
equivalent to the old. In Church’s case, this amounts to arguing
that the new characterization is equivalent to his characterization in
terms of either recursiveness or λ-definability. Finally, the
conclusion that the new and previous characterizations are equivalent
is claimed as further evidence in favor of the Church-Turing
thesis.

with defining effective calculability:

> a function \(F\) (of one positive integer) [is defined] to be
> effectively calculable if, for every positive integer \(m\), there
> exists a positive integer \(n\) such that \(F(m) = n\) is a provable
> theorem. (Church 1936a: 358)

Church did not specify any particular symbolic logic. He merely
stipulated a number of general conditions that the logic must satisfy
(1936a: 357). These included the stipulations that the list of axioms
> effectively calculable if, for every positive integer \(m\), there
> exists a positive integer \(n\) such that \(F(m) = n\) is a provable
> theorem. (Church 1936a: 358)

Church did not specify any particular symbolic logic. He merely
stipulated a number of general conditions that the logic must satisfy
(1936a: 357). These included the stipulations that the list of axioms
of the logic must be either finite or enumerably infinite, and that
each rule of the logic must specify an “effectively calculable
operation” (the latter is necessary, he said, if the logic
each rule of the logic must specify an “effectively calculable
operation” (the latter is necessary, he said, if the logic
“is to serve at all the purposes for which a system of symbolic
logic is usually intended”). Having introduced this alternative
method of characterizing effective calculability, Church then went on
to argue that every function (of one positive integer) that is
“calculable within the logic” in this way is also
recursive. He concluded, in support of Church’s thesis, that the
new method produces “no more general definition of effective
calculability than that proposed”, i.e., in terms of
method of characterizing effective calculability, Church then went on
to argue that every function (of one positive integer) that is
“calculable within the logic” in this way is also
recursive. He concluded, in support of Church’s thesis, that the
new method produces “no more general definition of effective
calculability than that proposed”, i.e., in terms of
recursiveness (1936a: 358).

#### 4.4.3 Turing’s variant {#-443-turings-variant}

new method produces “no more general definition of effective
calculability than that proposed”, i.e., in terms of
recursiveness (1936a: 358).

#### 4.4.3 Turing’s variant {#-443-turings-variant}

Turing’s prefatory remarks to argument II bring out its broad
similarity to Church’s argument. Turing described II as being a
“proof of the equivalence of two definitions”,
adding—“in case the new definition has a greater intuitive
rule is required to be an effectively calculable operation. In a
different context, he might have supported this assertion by appealing
to Church’s thesis (which says, after all, that what is
effectively calculable is recursive). But in the present context, such
an appeal would naturally be question-begging.

Nor did Church make any such appeal. (Sieg described Church’s
reasoning as “semi-circular”, but this seems too
harsh—there is nothing circular about it; Sieg 1994: 87, 2002:
394.) But nor did Church offer any compelling reasons in support of
effectively calculable is recursive). But in the present context, such
an appeal would naturally be question-begging.

Nor did Church make any such appeal. (Sieg described Church’s
reasoning as “semi-circular”, but this seems too
harsh—there is nothing circular about it; Sieg 1994: 87, 2002:
394.) But nor did Church offer any compelling reasons in support of
his assertion. He merely gave examples of systems whose rules
*are* recursive operations; and also said—having
stipulated that each rule of procedure must be an effectively
stipulated that each rule of procedure must be an effectively
calculable operation—that he will “*interpret this to
mean* that … each rule of procedure must be a recursive
operation” (1936: 357, italics added.) In short, a crucial step
of Church’s argument for Church’s thesis receives
inadequate support. Sieg famously dubbed this step the
“stumbling block” in Church’s argument (Sieg 1994:
87).

There is no such difficulty in Turing’s argument. Having
> Since our original notion of effective calculability of a function
> … is a somewhat vague intuitive one, the thesis cannot be
> proved. … While we cannot prove Church’s thesis, since
> its role is to delimit precisely an hitherto vaguely conceived
> totality, we require evidence …. (Kleene 1952: 318)

Rejecting the conventional view, Kripke suggests that, on the
contrary, the Church-Turing thesis is susceptible to mathematical
proof. Furthermore, he canvasses the idea that Turing himself sketched
an argument that serves to prove the thesis.
“effectively calculable” are not exact, theses involving
them cannot be proved (op. cit.). Turing however did not voice a
similar argument (perhaps because he saw a difficulty). The fact that
the term “systematic method” is inexact is *not*
enough to show that there could be no mathematically acceptable proof
of a thesis involving the term. Mendelson gave a graphic statement of
this point, writing about what is called above “*the converse
of Church’s thesis*”
([Section 1.5](#MeanCompCompTuriThes)):

> partial-recursive functions are effectively computable, is
> acknowledged to be obvious in all textbooks in recursion theory. A
> straightforward argument can be given for it…. This simple
> argument is as clear a proof as I have seen in mathematics, and it is
> a proof in spite of the fact that it involves the intuitive notion of
> effective computability. (Mendelson 1990: 232–233)

Yet the point that the “intuitive” nature of some of its
terms does not rule out the thesis’s being provable is not to
say that the thesis *is* provable. If the status of the
> effective computability. (Mendelson 1990: 232–233)

Yet the point that the “intuitive” nature of some of its
terms does not rule out the thesis’s being provable is not to
say that the thesis *is* provable. If the status of the
Church-Turing thesis is “something between a theorem and a
definition”, then the definition is presumably Church’s
proposal to “define the notion … of an effectively
calculable function”
([Section 1.5](#MeanCompCompTuriThes))
proposal to “define the notion … of an effectively
calculable function”
([Section 1.5](#MeanCompCompTuriThes))
and the theorem is Turing’s computation theorem
([Section 4.3.5](#TuriTheo)),
i.e., that given Turing’s account of the essential features of
human computation, Turing’s thesis is true. This theorem is
demonstrable, but to prove the thesis itself from the theorem, it
would be necessary to show, with mathematical certainty, that
Turing’s account of the essential features of human computation
to the effect that the universal Turing machine is the most general
machine possible (and so the answer to the question just posed is
*yes*.) For example:

> That there exists a most general formulation of machine and that it
> leads to a unique set of input-output functions has come to be called
> *Church’s thesis*. (Newell 1980: 150)

Yet the Church-Turing thesis is a thesis about the extent of
*effective* methods (therein lies its mathematical importance).
*effective* methods (therein lies its mathematical importance).
Putting this another way, the thesis concerns what a *human
being* can achieve when calculating by rote, using paper and
pencil (absent contingencies such as boredom, death, or insufficiency
of paper). What a human rote-worker can achieve, and what a machine
can achieve, may be different.

Gandy was perhaps the first to distinguish explicitly between
Turing’s thesis and the very different proposition that
*whatever can be calculated by a machine can be calculated by a
> All functions that can be generated by machine are effectively
> computable.

“Effectively computable” is a commonly used term: A
function is said to be effectively computable if (and only if) there
is an effective method for obtaining its values. When phrased in terms
of effective computability, the Church-Turing thesis says: All
effectively computable functions are Turing-machine computable.

Clearly the Church-Turing thesis and the maximality thesis are
“Effectively computable” is a commonly used term: A
function is said to be effectively computable if (and only if) there
is an effective method for obtaining its values. When phrased in terms
of effective computability, the Church-Turing thesis says: All
effectively computable functions are Turing-machine computable.

Clearly the Church-Turing thesis and the maximality thesis are
different theses.

### 5.2 The “equivalence fallacy” {#-52-the-equivalence-fallacy}
function is said to be effectively computable if (and only if) there
is an effective method for obtaining its values. When phrased in terms
of effective computability, the Church-Turing thesis says: All
effectively computable functions are Turing-machine computable.

Clearly the Church-Turing thesis and the maximality thesis are
different theses.

### 5.2 The “equivalence fallacy” {#-52-the-equivalence-fallacy}

is an effective method for obtaining its values. When phrased in terms
of effective computability, the Church-Turing thesis says: All
effectively computable functions are Turing-machine computable.

Clearly the Church-Turing thesis and the maximality thesis are
different theses.

### 5.2 The “equivalence fallacy” {#-52-the-equivalence-fallacy}

A common argument for the maximality thesis, or an equivalent, cites
of effective computability, the Church-Turing thesis says: All
effectively computable functions are Turing-machine computable.

Clearly the Church-Turing thesis and the maximality thesis are
different theses.

### 5.2 The “equivalence fallacy” {#-52-the-equivalence-fallacy}

A common argument for the maximality thesis, or an equivalent, cites
the fact, noted above, that many different attempts to analyse the
effectively computable functions are Turing-machine computable.

Clearly the Church-Turing thesis and the maximality thesis are
different theses.

### 5.2 The “equivalence fallacy” {#-52-the-equivalence-fallacy}

A common argument for the maximality thesis, or an equivalent, cites
the fact, noted above, that many different attempts to analyse the
informal notion of computability in precise terms—attempts by
are of the concept of an effective method: The equivalence of the
analyses bears only on the question of the extent of what is
*humanly* computable, not on the further question whether
functions generatable by *machines* could extend beyond what is
in principle humanly computable.

### 5.3 Watching our words {#-53-watching-our-words}

It may be helpful at this point to survey some standard technical
terminology that could set traps for the unwary.
the effect that such-and-such functions are uncomputable are
accordingly about human computers. Turing should not be construed as
intending to state results about the limitations of machinery. Gandy
wrote:

> it is by no means obvious that the limitations described in
> [[Section 4.3](#TuriArguI)
> above] apply to mechanical devices; Turing does not claim this.
> (Gandy 1988: 84)

is usually used to mean “effectively computable” (although
not always—see
[Section 5.3.3](#BeyoEffe)).
(“Effectively computable” was defined in
[Section 5.1](#TwoDistThes).)
Since Boolos and Jeffrey are using “computable” to mean
“effectively computable”, what they are saying in this
quotation comes down to the statement that the functions in question
are *not effectively computable* by any past, present, or
future real machine—which is true, since the functions are,
(“Effectively computable” was defined in
[Section 5.1](#TwoDistThes).)
Since Boolos and Jeffrey are using “computable” to mean
“effectively computable”, what they are saying in this
quotation comes down to the statement that the functions in question
are *not effectively computable* by any past, present, or
future real machine—which is true, since the functions are,
*ex hypothesi*, *not* effectively computable. However,
to a casual reader of the literature, this statement (and others like
it) might appear to say more than it in fact does. That a function is
“effectively computable”, what they are saying in this
quotation comes down to the statement that the functions in question
are *not effectively computable* by any past, present, or
future real machine—which is true, since the functions are,
*ex hypothesi*, *not* effectively computable. However,
to a casual reader of the literature, this statement (and others like
it) might appear to say more than it in fact does. That a function is
*uncomputable* (i.e., is effectively uncomputable), by any
past, present, or future real machine, does not entail *per se*
that the function in question cannot be *generated* by some
are *not effectively computable* by any past, present, or
future real machine—which is true, since the functions are,
*ex hypothesi*, *not* effectively computable. However,
to a casual reader of the literature, this statement (and others like
it) might appear to say more than it in fact does. That a function is
*uncomputable* (i.e., is effectively uncomputable), by any
past, present, or future real machine, does not entail *per se*
that the function in question cannot be *generated* by some
real machine.

*ex hypothesi*, *not* effectively computable. However,
to a casual reader of the literature, this statement (and others like
it) might appear to say more than it in fact does. That a function is
*uncomputable* (i.e., is effectively uncomputable), by any
past, present, or future real machine, does not entail *per se*
that the function in question cannot be *generated* by some
real machine.

The second quotation:

*uncomputable* (i.e., is effectively uncomputable), by any
past, present, or future real machine, does not entail *per se*
that the function in question cannot be *generated* by some
real machine.

The second quotation:

> FORMAL LIMITS OF MACHINE BEHAVIORS … There are certain
> behaviors that are “uncomputable”—behaviors for
> which *no* formal specification can be given for a machine that
#### 5.3.3 Beyond effective {#-533-beyond-effective}

Some authors use phrases such as “computation in a broad
sense”, or simply “computation”, to refer to
computation of a type that potentially transcends effective
computation (e.g., Doyle 2002; MacLennan 2003; Shagrir & Pitowsky
2003; Siegelmann 2003; Andréka, Németi, &
Németi 2009; Copeland & Shagrir 2019).

Doyle, for instance, suggested that *equilibrating systems*
computation of a type that potentially transcends effective
computation (e.g., Doyle 2002; MacLennan 2003; Shagrir & Pitowsky
2003; Siegelmann 2003; Andréka, Németi, &
Németi 2009; Copeland & Shagrir 2019).

Doyle, for instance, suggested that *equilibrating systems*
with discrete spectra (e.g., molecules or other quantum many-body
systems) may illustrate a concept of computation that is wider than
effective computation. Since “equilibrating can be so easily,
reproducibly, and mindlessly accomplished”, Doyle said, we may
effective computation. Since “equilibrating can be so easily,
reproducibly, and mindlessly accomplished”, Doyle said, we may
“take the operation of equilibrating” to be a
computational operation, even if the functions computable in principle
using Turing-machine operations *plus* equilibrating include
functions that are not computable by an unaided Turing machine (Doyle
2002: 519).

#### 5.3.4 The word “mechanical” {#-534-the-word-mechanical}

“mechanical” and “effective” are usually used
interchangeably: A “mechanical” procedure is simply an
effective procedure. Gandy 1988 outlines the history of this use of
the word “mechanical”.

Statements like the following occur in the literature:

> Turing proposed that a certain class of abstract machines [Turing
> machines] could perform any “mechanical” computing
> procedure. (Mendelson 1964: 229)
effective procedure. Gandy 1988 outlines the history of this use of
the word “mechanical”.

Statements like the following occur in the literature:

> Turing proposed that a certain class of abstract machines [Turing
> machines] could perform any “mechanical” computing
> procedure. (Mendelson 1964: 229)

This could be mistaken for Thesis M. However, “mechanical”
> perform any effective computing procedure.

The technical usage of “mechanical” has a tendency to
obscure the conceptual possibility that not all machine-generatable
functions are Turing-machine computable. The question “Can a
*machine* implement a procedure that is not mechanical?”
may appear self-answering—yet this is what is being asked if
Thesis M and the maximality thesis are questioned.

### 5.4 The strong maximality thesis {#-54-the-strong-maximality-thesis}
that is not effectively computable. A single example will be provided
here; further examples may be found in Andréka et al. 2009,
Davies 2001, Hogarth 1994, Pitowsky 1990, Siegelmann 2003, and other
papers mentioned below.

#### 5.4.1 Accelerating Turing machines {#-541-accelerating-turing-machines}

Accelerating Turing machines (ATMs) are exactly like standard Turing
machines except that their speed of operation accelerates as the
computation proceeds (Stewart 1991; Copeland 1998a,b, 2002a; Copeland
thesis, these functions are not effectively computable).

One example of such a function is the *halting function \(h\)*.
\(h(n) = 1\) if the \(n\)th Turing machine halts, and \(h(n) = 0\) if
the \(n\)th Turing machine runs on endlessly. It is well known that no
standard Turing machine can compute this function (Davis 1958); but an
ATM can produce any of the function’s values in a finite period
of time.

When computing \(h(n)\), the ATM’s first step is write
In modern computer science, algorithms and effective procedures are
associated not primarily with humans but with machines. Accordingly,
many computer science textbooks formulate the Church-Turing thesis
without mentioning human computers (e.g., Hopcroft & Ullman 1979;
Lewis & Papadimitriou 1981). This is despite the fact that the
concept of human computation lay at the heart of Turing’s and
Church’s analyses.

The variety of algorithms studied by modern computer science eclipses
the field as it was in Turing’s day. There are now parallel
effective procedures or algorithms—*whether or not* the
resulting algorithms satisfy the algorithmic version of the
Church-Turing thesis. (See Copeland & Shagrir 2019 for further
discussion.)

In summary, the algorithmic version of the Church-Turing thesis is
broader than the original thesis, in that Church and Turing considered
essentially only a single type of algorithm, effective step-by-step
calculations on paper. The algorithmic version is also perhaps less
secure than the original thesis.
essentially only a single type of algorithm, effective step-by-step
calculations on paper. The algorithmic version is also perhaps less
secure than the original thesis.

### 6.2 Computational complexity: the Extended Church-Turing thesis {#-62-computational-complexity-the-extended-church-turing-thesis}

The Turing machine now holds a central place not only in computability
theory but also in complexity theory. Quantum computation researchers
Bernstein and Vazirani say:

Yao points out that ECT has a powerful implication:

> at least in principle, to make future computers more efficient, one
> only needs to focus on improving the implementation technology of
> present-day computer designs. (2003: 101)

Unlike the original Church-Turing thesis (whose status is
“something between” a theorem and a definition) ECT is
neither a logico-mathematical theorem nor a definition. If it is true,
then its truth is a consequence of the laws of physics—and it
then its truth is a consequence of the laws of physics—and it
might not be true. (Although it is trivial if, contrary to a standard
but unproved assumption in computer science, P = NP.)

The second complexity-theoretic version of the thesis involves the
concept of a *probabilistic Turing machine* (due to Rabin &
Scott 1959). Vazirani and Aharonov state the thesis:

> [T]he extended Church-Turing thesis … asserts that any
> reasonable computational model can be simulated efficiently by the
It is sometimes said that the Church-Turing thesis has implications
concerning the scope of computational simulation. For example, Searle
writes:

> Can the operations of the brain be simulated on a digital computer?
> … The answer seems to me … demonstrably
> “Yes” … That is, naturally interpreted, the
> question means: Is there some description of the brain such that under
> that description you could do a computational simulation of the
> operations of the brain. But given Church’s thesis that anything
said. As already emphasized, Turing was talking about *effective
methods*, whereas the theses presented by Deutsch and Wolfram
concern all (finitely realizable) physical systems—no matter
whether or not the system’s activity is effective.

In the wake of this early work by Deutsch and Wolfram, the phrases
“physical form of the Church-Turing thesis”,
“physical version of the Church-Turing thesis”—and
even “*the* physical Church-Turing
thesis”—are now quite common in the current literature.
whether or not the system’s activity is effective.

In the wake of this early work by Deutsch and Wolfram, the phrases
“physical form of the Church-Turing thesis”,
“physical version of the Church-Turing thesis”—and
even “*the* physical Church-Turing
thesis”—are now quite common in the current literature.
However, such terms are probably better avoided, since these physical
theses are very distant from Turing’s thesis and Church’s
thesis.
the speed of propagation of effects and signals. (The argument aims to
cover only mechanisms obeying the principles of Relativity.) Gandy
expressed his various physical assumptions set-theoretically, by means
of precise axioms, which he called Principles I – IV. Principle
III, for example, captures the idea that there is a bound on the
number of types of basic parts (atoms) from which the states of the
machine are uniquely assembled; and Principle IV—which Gandy
called the “principle of local causation”—captures
the idea that each state-transition must be determined by the
*local environments* of the parts of the mechanism that change
time-dilation effects in order to compute (in a broad sense) a
function that provably cannot be computed by a universal Turing
machine (e.g., the halting function). Németi and his colleagues
emphasize that the Németi computer is “not in conflict
with presently accepted scientific principles” and that, in
particular, “the principles of quantum mechanics are not
violated”. They suggest moreover that humans might “even
build” a relativistic computer “sometime in the
future” (Andréka, Németi, & Németi
2009: 501).
#### 6.4.3 Quantum effects and the “Total” thesis {#-643-quantum-effects-and-the-total-thesis}

There is a stronger form of the
[Deutsch-Wolfram thesis](#deutschwolframthesis),
dubbed the “Total thesis” in Copeland and Shagrir
2019.

> **The Total Thesis**:
>   
> Every physical aspect of the behavior of any physical system can be
*human being* calculating in accordance with an effective
method.

Wittgenstein put this point in a striking way:

> Turing’s “Machines”. These machines are
> *humans* who calculate. (Wittgenstein 1947 [1980: 1096])

It is a point that Turing was to emphasize, in various forms, again
and again. For example:
> discipline, is in effect a universal machine. (Turing 1948 [2004:
> 416])

In order to understand Turing’s “On Computable
Numbers” and later texts, it is essential to keep in mind that
when he used the words “computer”,
“computable” and “computation”, he employed
them not in their modern sense as pertaining to machines, but as
pertaining to human calculators. For example:

“effective calculability”, taking it for granted his
readers would understand this term to be referring to *human*
calculation. He also used the term “effective method”,
again taking it for granted that readers would understand him to be
speaking of a humanly executable method.

Church also used the term “algorithm”, saying

> It is clear that for any recursive function of positive integers there
> exists an algorithm using which any required particular value of the
calculation. He also used the term “effective method”,
again taking it for granted that readers would understand him to be
speaking of a humanly executable method.

Church also used the term “algorithm”, saying

> It is clear that for any recursive function of positive integers there
> exists an algorithm using which any required particular value of the
> function can be effectively calculated. (Church 1936a: 351)

> function can be effectively calculated. (Church 1936a: 351)

He said further that the notion of effective calculability could be
spelled out as follows:

> by defining a function to be effectively calculable if there exists an
> algorithm for the calculation of its values. (Church 1936a: 358)

It was in Church’s review of Turing’s 1936 paper that he
brought the human computer out of the shadows. He wrote:
He said further that the notion of effective calculability could be
spelled out as follows:

> by defining a function to be effectively calculable if there exists an
> algorithm for the calculation of its values. (Church 1936a: 358)

It was in Church’s review of Turing’s 1936 paper that he
brought the human computer out of the shadows. He wrote:

> [A] human calculator, provided with pencil and paper and explicit
> by defining a function to be effectively calculable if there exists an
> algorithm for the calculation of its values. (Church 1936a: 358)

It was in Church’s review of Turing’s 1936 paper that he
brought the human computer out of the shadows. He wrote:

> [A] human calculator, provided with pencil and paper and explicit
> instructions, can be regarded as a kind of Turing machine. It is thus
> immediately clear that computability, so defined [i.e., computability
> by a Turing machine], can be identified with (especially, is no less
> general than) the notion of effectiveness as it appears in certain
> mathematical problems … and in general any problem which
> concerns the discovery of an algorithm. (Church 1937a: 43)

### 7.4 Turing’s use of “machine” {#-74-turings-use-of-machine}

It is important to note that, when Turing used the word
“machine”, he often meant not machine-in-general but, as
we would now say, Turing machine. At one point he explicitly drew
attention to this usage:
In consequence, Church’s version of Turing’s thesis is
subtly different from Turing’s own:

> **Church’s Turing’s thesis**:
>   
> An infinite sequence of digits is “computable” if (and
> only if) it is possible to devise a computing machine, occupying a
> finite space and with working parts of a finite size, that will write
> down the sequence to any desired number of terms if allowed to run for
> a sufficiently long time.
  Foundations of Mathematics and Their Implications”, in
  Gödel 1995: 304–323.
* –––, 1965a, “Postscriptum” to
  Gödel 1934, in Davis 1965: 71–73.
* –––, 1965b, letter to Davis, 15 February 1965.
  Excerpt in Davis 1982: 8.
* –––, *Kurt Gödel: Collected Works*,
  5 volumes, Solomon Feferman et al. (eds), Oxford: Clarendon Press.
  + 1986, *Volume 1: Publications 1929–1936*
  + 1990, *Volume 2: Publications 1938–1974*
* Shagrir, Oron, 2002, “Effective Computation by Humans and
  Machines”, *Minds and Machines*, 12(2): 221–240.
  doi:10.1023/A:1015694932257
* –––, 2006, “Gödel on Turing on
  Computability”, in Olszewski, Wolenski, and Janusz 2006:
  393–419. doi:10.1515/9783110325461.393
* Shagrir, Oron and Itamar Pitowsky, 2003, “Physical
  Hypercomputation and the Church–Turing Thesis”, *Minds
  and Machines*, 13(1): 87–101.
  doi:10.1023/A:1021365222692

## Historical Context {#-historical-context}

### Development & Discovery {#-development--discovery}
*First published Wed Jan 8, 1997; substantive revision Mon Dec 18, 2023*

The Church-Turing thesis (or Turing-Church thesis) is a fundamental
claim in the theory of computability. It was advanced independently by
Church and Turing in the mid 1930s. There are various equivalent
formulations of the thesis. A common one is that every effective
computation can be carried out by a Turing machine (i.e., by
Turing’s abstract computing machine, which in its universal form
encapsulates the fundamental logical principles of the stored-program
all-purpose digital computer). Modern reimaginings of the
discovered this result independently of one another, both publishing
it in 1936 (Church a few months earlier than Turing). Church’s
proof, which made no reference to computing machines, is for that
reason sometimes considered to be of less interest than
Turing’s.

The *Entscheidungsproblem* had attracted some of the finest
minds of early twentieth-century mathematical logic, including
Gödel, Herbrand, Post, Ramsey, and Hilbert and his assistants
Ackermann, Behmann, Bernays, and Schönfinkel. Herbrand described
from a revised edition of their book. Published in 1938, the new
edition was considerably watered down to take account of
Turing’s and Church’s monumental result.

Hilbert knew, of course, that some mathematical problems have
*no* solution, for example the problem of finding a finite
binary numeral \(n\) (or unary numeral, in Hilbert’s version of
the problem) such that \(n^2 = 2\) (Hilbert 1926: 179). He was
nevertheless very fond of saying that *every mathematical problem
can be solved*, and by this he meant that
turns to modern developments.

### 2.1 From simple rules-of-thumb to Siri and beyond {#-21-from-simple-rules-of-thumb-to-siri-and-beyond}

Effective methods are extremely helpful in carrying out many practical
tasks, and their use stretches back into the mists of antiquity,
although it was not until the twentieth century that interest began to
build in analysing their nature. Perhaps the earliest effective
methods to be utilized were rules-of-thumb (as Turing called them) for
arithmetical calculations of various sorts, but whatever their humble
“\(S\) is false”. As the groundbreaking developments in
1936 by Church and Turing made clear, if the *ars inveniendi*
is supposed to work by means of an effective method, then there can be
no universal *ars inveniendi*—and not even an *ars
inveniendi* that is restricted to all mathematical statements,
since these include statements of the form “\(p\) is
provable”, or even to all purely logical statements.

### 2.3 Logic machines {#-23-logic-machines}

A decade later, Venn published the technique we now call *Venn
diagrams* (Venn 1880). This technique satisfies the four criteria
set out for an effective method in
[Section 1](#ThesHist).
The user first diagrams the premisses of a syllogism and then, as
Quine put it, “we inspect the diagram to see whether the content
of the conclusion has automatically appeared in the diagram as a
result” (Quine 1950: 74). Not all formulae of the functional
calculus are Venn-diagrammable, and Venn’s original method is
limited to testing syllogisms. In the twentieth century, Massey showed
three inches deep” (1880: 17). When Venn published his
description of it, Jevons quickly wrote to him saying that the
logical-diagram machine “is exceedingly ingenious & seems to
represent the relations of four terms very well” (Jevons 1880).
Venn himself however was less enthusiastic, saying in his article
“I have no high estimate myself of the interest or importance of
what are sometimes called logical machines” (1880: 15). Baldwin,
commenting on Venn’s machine in 1902, complained that it was
“merely a more cumbersome diagram” (1902: 29). This is
quite true—it would be at least as easy to draw the Venn diagram
mathematical problems”. Much later, Church discovered a detailed
diagram of an electrical relay-based form of Marquand’s machine
among Marquand’s papers at Princeton (reproduced in Ketner &
Stewart 1984: 200). Whoever worked out the design in this
diagram—Marquand, Peirce, or an unknown third person—has a
claim to be an important early pioneer of electromechanical
computing.

Peirce, with his interest in logic machines, seems to have been the
first to consider the decision problem in roughly the form in which
scientific question found its fullest development (see further the
supplement on
[The Rise and Fall of the *Entscheidungsproblem*](decision-problem.html)).

Hilbert’s earliest publication to mention what we would now call
a decision problem is his 1899 book *Grundlagen der Geometrie*
[Foundations of Geometry]. He said that in the course of his
investigations of Euclidean geometry he was

> guided by the principle of discussing each given question in such a
by the time Hilbert’s student Behmann published a landmark
article in 1922, “Contributions to the Algebra of Logic, in
particular to the *Entscheidungsproblem*”. It was
probably Behmann who coined the term
“*Entscheidungsproblem*” (Mancosu & Zach 2015:
166–167). In a 1921 lecture to the Göttingen group, Behmann
said:

> If a logical or mathematical statement is given, the required
> procedure should give complete instructions for determining whether
subtitled “Account of an Anticipation”, published in 1965
but written in about 1941, he explained that during the early 1920s he
had devised a system—he called it the “complete normal
system”, because “in a way, it contains all normal
systems”—and this, he said, “correspond[ed]”
to Turing’s universal machine (Post 1965: 412). Furthermore, he
argued during the same period that the decision problem is unsolvable
in the case of his “normal systems” (1965: 405ff). But it
seems he did not extend this argument to anticipate the Church-Turing
result that the decision problem for the predicate calculus is
*Grundlagen*, published in 1934, they had assumed the
*Entscheidungsproblem* to be solvable.

### 3.4 Modern axiomatic analyses {#-34-modern-axiomatic-analyses}

Church reported a discussion he had had with Gödel at the time
when it was still wide open how the intuitive concept of effective
calculability should be formalized (probably during 1934). Gödel
suggested that

noted in an abstract published in 1936 that the concept
“computable” is *absolute*, in the sense that all
the computable functions are specifiable in one and the same system,
there being no need to introduce a hierarchy of systems of different
orders—as is done, for example, in Tarskian analyses of the
concept “true”, and standardly in the case of the concept
“provable” (Gödel 1936: 24). Ten years later,
commenting on Turing’s work, Gödel emphasized that
“the great importance … [of] Turing’s
computability” is
> History is full of examples of delayed discoveries. Aristotelian and
> Newtonian mechanics lasted much longer than the seventy years that
> have elapsed since Church proposed identifying effectiveness with
> recursiveness, but still those physical theories were eventually found
> lacking. (Dershowitz & Gurevich 2008: 304)

Dershowitz and Gurevich presented a highly relevant example of delayed
discovery (following Barendregt 1997: 187): Any hope that the
effectively calculable functions could be identified with the
*primitive* recursive functions—introduced in 1923
Turing also said (in handwritten material published in 2004) that the
phrase “systematic method”

> is a phrase which, like many others e.g., “vegetable” one
> understands well enough in the ordinary way. But one can have
> difficulties when speaking to greengrocers or microbiologists or when
> playing “twenty questions”. Are rhubarb and tomatoes
> vegetables or fruits? Is coal vegetable or mineral? What about coal
> gas, marrow, fossilised trees, streptococci, viruses? Has the lettuce
> I ate at lunch yet become animal? … The same sort of difficulty
effective procedure. Gandy 1988 outlines the history of this use of
the word “mechanical”.

Statements like the following occur in the literature:

> Turing proposed that a certain class of abstract machines [Turing
> machines] could perform any “mechanical” computing
> procedure. (Mendelson 1964: 229)

This could be mistaken for Thesis M. However, “mechanical”
non-relativistic systems. (Extracts from unpublished work by Gandy, in
which he attempted to develop a companion argument for analogue
machines, are included in Copeland & Shagrir 2007.) However, the
scope of the Gandy argument is also limited in other ways, not noted
by Gandy himself. For example, some asynchronous algorithms fall
outside the scope of Gandy’s principles (Gurevich 2012; Copeland
& Shagrir 2007). Gurevich concludes that Gandy has not shown
“that his axioms are satisfied by all discrete mechanical
devices”, and Shagrir says there is no “basis for claiming
that Gandy characterized finite machine computation” (Gurevich
  + 1995, *Volume 3: Unpublished Essays and Lectures*
* Gurevich, Yuri, 2012, “What Is an Algorithm?”, in
  *SOFSEM 2012: Theory and Practice of Computer Science*,
  Mária Bieliková, Gerhard Friedrich, Georg Gottlob,
  Stefan Katzenbeisser, and György Turán (eds), (Lecture
  Notes in Computer Science 7147), Berlin/Heidelberg: Springer,
  31–42. doi:10.1007/978-3-642-27660-6\_3
* Guttenplan, Samuel D. (ed.), 1994, *A Companion to the
  Philosophy of Mind*, Oxford/Cambridge, MA: Blackwell Reference.
  doi:10.1002/9781405164597.
  History of Computer Design: Charles Sanders Peirce and
  Marquand’s Logical Machines”, *The Princeton University
  Library Chronicle*, 45(3): 187–224.
  doi:10.2307/26402393
* Kieu, Tien D., 2004, “Hypercomputation with Quantum
  Adiabatic Processes”, *Theoretical Computer Science*,
  317(1–3): 93–104. doi:10.1016/j.tcs.2003.12.006
* Kleene, Stephen C., 1934, “Proof by Cases in Formal
  Logic”, *Annals of Mathematics*, second series 35(3):
  529–544. doi:10.2307/1968749
  Theory”, *IEEE Annals of the History of Computing*, 3(1):
  52–67. doi:10.1109/MAHC.1981.10004
* –––, 1986, “Introductory Note to
  *1930b*, *1931* and *1932b*”, in Gödel
  1986: 126–141.
* –––, 1987, “Reflections on Church’s
  Thesis”, *Notre Dame Journal of Formal Logic*, 28(4):
  490–498. doi:10.1305/ndjfl/1093637645
* Kleene, Stephen C. and J. Barkley Rosser, 1935, “The
  Inconsistency of Certain Formal Logics”, *Annals of
  Oral History of Computing”, London: Science Museum;
  transcription by Copeland in Copeland 2004: 206.
* Olszewski, Adam, Jan Woleński, and Robert Janusz (eds), 2006,
  *Church’s Thesis after 70 Years*, Frankfurt/New
  Brunswick, NJ: Ontos. doi:10.1515/9783110325461
* Peirce, Charles S., 1886, letter to Marquand, 30 December 1886, in
  Peirce 1993: item 58, pp. 422–424.
* –––, 1887, “Logical Machines”,
  *The American Journal of Psychology*, 1(1): 165–170.
* –––, 1903a, “The 1903 Lowell Institute
  Development*, 3(2): 114–125. doi:10.1147/rd.32.0114
* Ramsey, Frank P., 1930, “On a Problem of Formal
  Logic”, *Proceedings of the London Mathematical Society*,
  second series 30(1): 264–286. doi:10.1112/plms/s2-30.1.264
* Roberts, Don D., 1973, *The Existential Graphs of Charles S.
  Peirce*, Hague: Mouton.
* –––, 1997, “A Decision Method for
  Existential Graphs”, in Houser, Roberts, & Van Evra 1997:
  387–401.
* Rosser, J. Barkley, 1935a, “A Mathematical Logic Without
  Oldenbourg. Published in English as *Philosophy of Mathematics and
  Natural Science*, Princeton, NJ: Princeton University Press,
  1949.
* Wittgenstein, Ludwig, 1947 [1980], *Bemerkungen über die
  Philosophie der Psychologie*. Translated as *Remarks on the
  Philosophy of Psychology*, Volume 1, Anscombe, G. Elizabeth M. and
  Georg Henrik von Wright (eds), Oxford: Blackwell, 1980.
* Wolfram, Stephen, 1985, “Undecidability and Intractability
  in Theoretical Physics”, *Physical Review Letters*,
  54(8): 735–738. doi:10.1103/PhysRevLett.54.735
  Hilbert, and the Development of Propositional Logic”,
  *Bulletin of Symbolic Logic*, 5(3): 331–366.
  doi:10.2307/421184
* –––, 2003, “The Practice of Finitism:
  Epsilon Calculus and Consistency Proofs in Hilbert’s
  Program”, *Synthese*, 137(1/2): 211–259.
  doi:10.1023/A:1026247421383
* Zanichelli, Nicola (ed.), 1929, *Atti del Congresso
  Internazionale dei Matematici, Bologna, 3–10 Settembre 1928,
  Volume 1: Rendiconto del Congresso Conferenze*, Bologna:
* [The Turing Archive for the History of Computing](http://www.alanturing.net/)
* Kieu, Tien D., 2006,
  “[Reply to Andrew Hodges](https://arxiv.org/pdf/quant-ph/0602214v2.pdf)”,
  arXiv:quant-ph/0602214v2.

## Related Entries {#-related-entries}

[Church, Alonzo](../church/) |
[computability and complexity](../computability/) |
[computation: in physical systems](../computation-physicalsystems/) |
[computing: modern history of](../computing-history/) |
[Gödel, Kurt: incompleteness theorems](../goedel-incompleteness/) |
[Llull, Ramon](../llull/) |
[mind: computational theory of](../computational-mind/) |
[Turing, Alan](../turing/) |
[Turing machines](../turing-machine/)

Canonical Hub:

## Theophysics Applications {#-theophysics-applications}

- [[04_THEOPYHISCS/[7.6] Protocols/14_David_Effect_Protocol|Protocol 4: The David Effect]]

## Related Theories & Extensions {#-related-theories--extensions}

*No related theories found in canonical index*

## Other Internet Resources {#-other-internet-resources}

* [The Turing Archive for the History of Computing](http://www.alanturing.net/)
* Kieu, Tien D., 2006,
  “[Reply to Andrew Hodges](https://arxiv.org/pdf/quant-ph/0602214v2.pdf)”,
  arXiv:quant-ph/0602214v2.

## Related Entries {#-related-entries}

[Church, Alonzo](../church/) |
[computability and complexity](../computability/) |
[computation: in physical systems](../computation-physicalsystems/) |
[computer science, philosophy of](../computer-science/) |
[computing: modern history of](../computing-history/) |
[Gödel, Kurt: incompleteness theorems](../goedel-incompleteness/) |
[Llull, Ramon](../llull/) |
[mind: computational theory of](../computational-mind/) |

---
*This theory has been restructured for clarity and organization.*

%%--- SEMANTIC TAGS ---%%
%%tag::Claim::e5f3dc88-f101-425f-8465-a440301741b0::"Church-Turing Thesis"::null%%
%%tag::Claim::0da9f7f9-19ce-48f5-a19d-2fbf127bf1e9::"Every effective computation can be carried out by a Turing machine"::e5f3dc88-f101-425f-8465-a440301741b0%%
%%tag::Claim::c3d0e245-d2ce-463d-8ea3-f3356ea47661::"Some modern theses are distant relatives of the original Church-Turing thesis"::e5f3dc88-f101-425f-8465-a440301741b0%%
%%tag::Axiom::95c2ae79-d74f-485f-b16f-d511b34ffad6::"Effective Method Definition"::null%%
%%tag::Claim::90aa9598-d650-412e-8b88-854bb61ca1ee::"An effective method must be systematic and mechanical"::95c2ae79-d74f-485f-b16f-d511b34ffad6%%
%%tag::Claim::bf052899-068b-4db6-a280-d805e0fb58e1::"Effective methods can be expressed as finite instructions"::95c2ae79-d74f-485f-b16f-d511b34ffad6%%
%%tag::EvidenceBundle::c229331c-539e-44ac-aa04-43965c280ad7::"Historical Context of Church-Turing Thesis"::e5f3dc88-f101-425f-8465-a440301741b0%%
%%tag::Claim::774696fa-1f33-4d5b-95db-601a782ae858::"Turing's analysis of computability is superior to Church's"::null%%
%%tag::Claim::a97c27d1-8027-4736-88e1-13aef1bb3d80::"Gödel found Turing's analysis satisfactory"::774696fa-1f33-4d5b-95db-601a782ae858%%
%%tag::EvidenceBundle::71a960eb-1769-4cad-8765-fecb785f091e::"Gödel's Acceptance of Turing's Thesis"::a97c27d1-8027-4736-88e1-13aef1bb3d80%%
%%tag::Relationship::f1460d63-3447-4241-a91f-dffbeb0480d7::"Equivalence of Church and Turing's Theses"::null%%
%%tag::Claim::26890d5a-dbcc-4eee-b780-b75d1e8f51c6::"All effectively calculable functions are Turing-machine computable"::f1460d63-3447-4241-a91f-dffbeb0480d7%%
%%tag::Claim::1fd1e907-e486-4335-a9c7-553a97d8d024::"There are no functions in S other than those obtained by effective methods"::f1460d63-3447-4241-a91f-dffbeb0480d7%%
%%tag::Axiom::dafbe4d2-7cc9-4ce3-abbf-62e13ba6e7a9::"Principles of Effective Computability"::null%%
%%tag::Claim::2d86a481-44e5-45fd-aa13-b835138cd704::"Effective calculability is equivalent to recursiveness"::dafbe4d2-7cc9-4ce3-abbf-62e13ba6e7a9%%
%%tag::Claim::db27faa0-f59c-443b-a5b8-46a955bce3e9::"Turing's thesis is about human computation"::null%%
%%tag::EvidenceBundle::f6594c11-4eda-40b5-aea6-fbfe9d8d4b0c::"Historical Development of Effective Methods"::null%%
%%tag::Claim::27f081c7-1ff9-4fc2-a395-c3c334008b08::"The Entscheidungsproblem is unsolvable"::null%%
%%tag::Claim::0941c533-efbd-4ab9-b88c-a9d13ee53f53::"Turing's machines can simulate any effective procedure"::null%%
%%--- END SEMANTIC TAGS ---%%

---

## Metadata

**Original File:** Church-Turing_Thesis.md

**Restructured:** 2026-03-01 15:52:19

**Format:** Canonical Theory Document (Lowe Standard v1.0)

**Status:** Cleaned and ready for evaluation

---

*This paper has been restructured for clarity and proper academic formatting. Original content preserved.*
