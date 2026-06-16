---
title: "Entropy %28information theory%29"
author: "Unknown Author"
date: 2026-03-01
category: theory
tags:
  - theory
  - theory
  - canonical
source_file: Shannon_Information_Theory.md
restructured: 2026-03-01 15:52:17
---

# Entropy %28information theory%29

**Author:** Unknown Author

**Date:** 2026-03-01

---

## Table of Contents

- [# Entropy %28information theory%29](#-entropy-28information-theory29)
- [## Overview](#-overview)
- [### Example](#-example)
- [## Definition](#-definition)
- [## Example](#-example)
- [#  is monotonically decreasing in : an increase in the probability of an event decreases the information from an observed event, and vice versa.](#--is-monotonically-decreasing-in--an-increase-in-the-probability-of-an-event-decreases-the-information-from-an-observed-event-and-vice-versa)
- [# : events that always occur do not communicate information.](#--events-that-always-occur-do-not-communicate-information)
- [# : the information learned from independent events is the sum of the information learned from each event.](#--the-information-learned-from-independent-events-is-the-sum-of-the-information-learned-from-each-event)
- [#  is a twice continuously differentiable function of p.](#--is-a-twice-continuously-differentiable-function-of-p)
- [### Alternative characterization](#-alternative-characterization)
- [# Continuity:  should be continuous, so that changing the values of the probabilities by a very small amount should only change the entropy by a small amount.](#-continuity--should-be-continuous-so-that-changing-the-values-of-the-probabilities-by-a-very-small-amount-should-only-change-the-entropy-by-a-small-amount)
- [# Symmetry:  should be unchanged if the outcomes  are re-ordered. That is, \Eta_n\left(p_1, p_2, \ldots, p_n \right) = \Eta_n\left(p_{i_1}, p_{i_2}, \ldots, p_{i_n} \right) for any permutation \{i_1, ..., i_n\} of \{1, ..., n\}.](#-symmetry--should-be-unchanged-if-the-outcomes--are-re-ordered-that-is-eta_nleftp_1-p_2-ldots-p_n-right--eta_nleftp_i_1-p_i_2-ldots-p_i_n-right-for-any-permutation-i_1--i_n-of-1--n)
- [# Maximum: \Eta_n should be maximal if all the outcomes are equally likely i.e. \Eta_n(p_1,\ldots,p_n) \le \Eta_n\left(\frac{1}{n}, \ldots, \frac{1}{n}\right).](#-maximum-eta_n-should-be-maximal-if-all-the-outcomes-are-equally-likely-ie-eta_np_1ldotsp_n-le-eta_nleftfrac1n-ldots-frac1nright)
- [# Increasing number of outcomes: for equiprobable events, the entropy should increase with the number of outcomes i.e. \Eta_n\bigg(\underbrace{\frac{1}{n}, \ldots, \frac{1}{n}}_{n}\bigg) ](#-increasing-number-of-outcomes-for-equiprobable-events-the-entropy-should-increase-with-the-number-of-outcomes-ie-eta_nbiggunderbracefrac1n-ldots-frac1n_nbigg-)
- [# Additivity: given an ensemble of  uniformly distributed elements that are partitioned into  boxes (sub-systems) with  elements each, the entropy of the whole ensemble should be equal to the sum of the entropy of the system of boxes and the individual entropies of the boxes, each weighted with the probability of being in that particular box.](#-additivity-given-an-ensemble-of--uniformly-distributed-elements-that-are-partitioned-into--boxes-sub-systems-with--elements-each-the-entropy-of-the-whole-ensemble-should-be-equal-to-the-sum-of-the-entropy-of-the-system-of-boxes-and-the-individual-entropies-of-the-boxes-each-weighted-with-the-probability-of-being-in-that-particular-box)

---

---
title: "Axiom Extraction -- Shannon Information Theory"
type: stress-test
source_theory: "Shannon Information Theory"
deepest_layer: 6
axioms_covered: 7
novel_axioms: 0
tags:
  - type/stress-test
  - domain/axioms
  - status/generated
url: "https://en.wikipedia.org/wiki/Entropy_%28information_theory%29"
source: Wikipedia
downloaded: 2026-02-26
---
# Entropy %28information theory%29 {#-entropy-28information-theory29}

> [[00_Canonical/CANONICAL_INDEX|Canonical Index]] | [[00_Canonical/MASTER_INDEX|Master Index]] | [[00_Canonical/NAVIGATION_GUIDE|Navigation Guide]]

## Overview {#-overview}

In information theory, the **entropy** of a random variable quantifies the average level of uncertainty or information associated with the variable's potential states or possible outcomes. This measures the expected amount of information needed to describe the state of the variable, considering the distribution of probabilities across all potential states. Given a discrete random variable X, which may be any member x within the set \mathcal{X} and is distributed according to p\colon \mathcal{X}\to[0, 1], the entropy is
\Eta(X) := -\sum_{x \in \mathcal{X}} p(x) \log p(x),
where \Sigma denotes the sum over the variable's possible values.

The concept of information entropy was introduced by Claude Shannon in his 1948 paper "A Mathematical Theory of Communication", and is also referred to as **Shannon entropy**. Shannon's theory defines a data communication system composed of three elements: a source of data, a communication channel, and a receiver. The "fundamental problem of communication" – as expressed by Shannon – is for the receiver to be able to identify what data was generated by the source, based on the signal it receives through the channel. In fact,  is the only function that satisfies a specific set of conditions defined in section **.

Hence, we can define the information, or surprisal, of an event E by

I(E) = \log\left(\frac{1}{p(E)}\right) ,
or equivalently,
I(E) = -\log(p(E)) .

Entropy measures the expected (i.e., average) amount of information conveyed by identifying the outcome of a random trial.  This implies that rolling a die has higher entropy than tossing a coin because each outcome of a single die roll has smaller probability (p=1/6) than each outcome of a coin toss (p=1/2).

Consider a coin with probability  of landing on heads and probability  of landing on tails. The maximum surprise is when , for which one outcome is not expected over the other. In this case a coin flip has an entropy of one bit (similarly, one trit with equiprobable values contains \log_2 3 (about 1.58496) bits of information because it can have one of three values). The minimum surprise is when  (impossibility) or  (certainty) and the entropy is zero bits. When the entropy is zero, there is no uncertainty at all – no freedom of choice – no information. Other values of *p* give entropies between zero and one bits.

### Example {#-example}
Information theory is useful to calculate the smallest amount of information required to convey a message, as in data compression. For example, consider the transmission of sequences comprising the 4 characters 'A', 'B', 'C', and 'D' over a binary channel. If all 4 letters are equally likely (25%), one cannot do better than using two bits to encode each letter. 'A' might code as '00', 'B' as '01', 'C' as '10', and 'D' as '11'. However, if the probabilities of each letter are unequal, say 'A' occurs with 70% probability, 'B' with 26%, and 'C' and 'D' with 2% each, one could assign variable length codes. In this case, 'A' would be coded as '0', 'B' as '10', 'C' as '110', and 'D' as '111'. With this representation, 70% of the time only one bit needs to be sent, 26% of the time two bits, and only 4% of the time 3 bits. On average, fewer than 2 bits are required since the entropy is lower (owing to the high prevalence of 'A' followed by 'B' – together 96% of characters). The calculation of the sum of probability-weighted log probabilities measures and captures this effect.

English text, treated as a string of characters, has fairly low entropy; i.e. it is fairly predictable.  We can be fairly certain that, for example, 'e' will be far more common than 'z', that the combination 'qu' will be much more common than any other combination with a 'q' in it, and that the combination 'th' will be more common than 'z', 'q', or 'qu'. After the first few letters one can often guess the rest of the word. English text has between 0.6 and 1.3 bits of entropy per character of the message.

## Definition {#-definition}
Named after Boltzmann's Η-theorem, Shannon defined the entropy  (Greek capital letter eta) of a discrete random variable X, which takes values in the set \mathcal{X} and is distributed according to p: \mathcal{X} \to [0, 1] such that p(x) := \mathbb{P}[X = x]:

\Eta(X) = \mathbb{E}[\operatorname{I}(X)] = \mathbb{E}[-\log p(X)].

Here \mathbb{E} is the expected value operator, and  is the information content of .
\operatorname{I}(X) is itself a random variable.

The entropy can explicitly be written as:
\Eta(X) = -\sum_{x \in \mathcal{X}} p(x)\log_b p(x) ,
where  is the base of the logarithm used. Common values of  are 2, Euler's number , and 10, and the corresponding units of entropy are the bits for , nats for , and bans for .

In the case of p(x) = 0 for some x \in \mathcal{X}, the value of the corresponding summand  is taken to be , which is consistent with the limit:
\lim_{p \to 0^+} p \log (p) = 0.

One may also define the conditional entropy of two variables X and Y taking values from sets \mathcal{X} and \mathcal{Y} respectively, as: Let (X, \Sigma, \mu) be a probability space. Let A \in \Sigma be an event. The surprisal of A is
 \sigma_\mu(A) = -\ln \mu(A) .

The *expected* surprisal of A is
 h_\mu(A) = \mu(A) \sigma_\mu(A) .

A \mu-almost partition is a set family P \subseteq \mathcal{P}(X) such that \mu(\mathop{\cup} P) = 1 and \mu(A \cap B) = 0 for all distinct A, B \in P. (This is a relaxation of the usual conditions for a partition.) The entropy of P is
  \Eta_\mu(P) = \sum_{A \in P} h_\mu(A) .

Let M be a sigma-algebra on X. The entropy of M is
 \Eta_\mu(M) = \sup_{P \subseteq M} \Eta_\mu(P) .
Finally, the entropy of the probability space is \Eta_\mu(\Sigma), that is, the entropy with respect to \mu of the sigma-algebra of *all* measurable subsets of X.

## Example {#-example}
 surprisal) of a coin flip, measured in bits, graphed versus the bias of the coin , where  represents a result of heads.
#  is monotonically decreasing in : an increase in the probability of an event decreases the information from an observed event, and vice versa. {#--is-monotonically-decreasing-in--an-increase-in-the-probability-of-an-event-decreases-the-information-from-an-observed-event-and-vice-versa}
# : events that always occur do not communicate information. {#--events-that-always-occur-do-not-communicate-information}
# : the information learned from independent events is the sum of the information learned from each event. {#--the-information-learned-from-independent-events-is-the-sum-of-the-information-learned-from-each-event}
#  is a twice continuously differentiable function of p. {#--is-a-twice-continuously-differentiable-function-of-p}

Given two independent events, if the first event can yield one of  equiprobable outcomes and another has one of  equiprobable outcomes then there are  equiprobable outcomes of the joint event. This means that if  bits are needed to encode the first value and  to encode the second, one needs  to encode both.

Shannon discovered that a suitable choice of \operatorname{I} is given by:
\operatorname{I}(p) = \log\left(\tfrac{1}{p}\right) = -\log(p).

In fact, the only possible values of \operatorname{I} are \operatorname{I}(u) = k \log u for k. Additionally, choosing a value for  is equivalent to choosing a value x>1 for k = - 1/\log x, so that  corresponds to the base for the logarithm. Thus, entropy is characterized by the above four properties.

The different units of information (bits for the binary logarithm , nats for the natural logarithm , bans for the decimal logarithm  and so on) are constant multiples of each other. For instance, in case of a fair coin toss, heads provides  bit of information, which is approximately 0.693 nats or 0.301 decimal digits. Because of additivity,  tosses provide  bits of information, which is approximately  nats or  decimal digits.

The *meaning* of the events observed (the meaning of *messages*) does not matter in the definition of entropy. Entropy only takes into account the probability of observing a specific event, so the information it encapsulates is information about the underlying probability distribution, not the meaning of the events themselves.

### Alternative characterization {#-alternative-characterization}
Another characterization of entropy uses the following properties. We denote  and .

# Continuity:  should be continuous, so that changing the values of the probabilities by a very small amount should only change the entropy by a small amount. {#-continuity--should-be-continuous-so-that-changing-the-values-of-the-probabilities-by-a-very-small-amount-should-only-change-the-entropy-by-a-small-amount}
# Symmetry:  should be unchanged if the outcomes  are re-ordered. That is, \Eta_n\left(p_1, p_2, \ldots, p_n \right) = \Eta_n\left(p_{i_1}, p_{i_2}, \ldots, p_{i_n} \right) for any permutation \{i_1, ..., i_n\} of \{1, ..., n\}. {#-symmetry--should-be-unchanged-if-the-outcomes--are-re-ordered-that-is-eta_nleftp_1-p_2-ldots-p_n-right--eta_nleftp_i_1-p_i_2-ldots-p_i_n-right-for-any-permutation-i_1--i_n-of-1--n}
# Maximum: \Eta_n should be maximal if all the outcomes are equally likely i.e. \Eta_n(p_1,\ldots,p_n) \le \Eta_n\left(\frac{1}{n}, \ldots, \frac{1}{n}\right). {#-maximum-eta_n-should-be-maximal-if-all-the-outcomes-are-equally-likely-ie-eta_np_1ldotsp_n-le-eta_nleftfrac1n-ldots-frac1nright}
# Increasing number of outcomes: for equiprobable events, the entropy should increase with the number of outcomes i.e. \Eta_n\bigg(\underbrace{\frac{1}{n}, \ldots, \frac{1}{n}}_{n}\bigg)  {#-increasing-number-of-outcomes-for-equiprobable-events-the-entropy-should-increase-with-the-number-of-outcomes-ie-eta_nbiggunderbracefrac1n-ldots-frac1n_nbigg-}
# Additivity: given an ensemble of  uniformly distributed elements that are partitioned into  boxes (sub-systems) with  elements each, the entropy of the whole ensemble should be equal to the sum of the entropy of the system of boxes and the individual entropies of the boxes, each weighted with the probability of being in that particular box. {#-additivity-given-an-ensemble-of--uniformly-distributed-elements-that-are-partitioned-into--boxes-sub-systems-with--elements-each-the-entropy-of-the-whole-ensemble-should-be-equal-to-the-sum-of-the-entropy-of-the-system-of-boxes-and-the-individual-entropies-of-the-boxes-each-weighted-with-the-probability-of-being-in-that-particular-box}

#### Discussion {#-discussion}
The rule of additivity has the following consequences: for positive integers  where ,
\Eta_n\left(\frac{1}{n}, \ldots, \frac{1}{n}\right) = \Eta_k\left(\frac{b_1}{n}, \ldots, \frac{b_k}{n}\right) + \sum_{i=1}^k \frac{b_i}{n} \, \Eta_{b_i}\left(\frac{1}{b_i}, \ldots, \frac{1}{b_i}\right).

Choosing ,  this implies that the entropy of a certain outcome is zero: . This implies that the efficiency of a source set with  symbols can be defined simply as being equal to its -ary entropy. See also Redundancy (information theory).

The characterization here imposes an additive property with respect to a partition of a set. Meanwhile, the conditional probability is defined in terms of a multiplicative property, P(A\mid B)\cdot P(B)=P(A\cap B). Observe that a logarithm mediates between these two operations. The conditional entropy and related quantities inherit simple relation, in turn. The measure theoretic definition in the previous section defined the entropy as a sum over expected surprisals \mu(A)\cdot \ln\mu(A) for an extremal partition. Here the logarithm is ad hoc and the entropy is not a measure in itself. At least in the information theory of a binary string, \log_2 lends itself to practical interpretations.

Motivated by such relations, a plethora of related and competing quantities have been defined. For example, David Ellerman's analysis of a "logic of partitions" defines a competing measure in structures dual to that of subsets of a universal set. Information is quantified as "dits" (distinctions), a measure on partitions.  "Dits" can be converted into Shannon's bits, to get the formulas for conditional entropy, and so on.

### Alternative characterization via additivity and subadditivity {#-alternative-characterization-via-additivity-and-subadditivity}

Another succinct axiomatic characterization of Shannon entropy was given by Aczél, Forte and Ng, via the following properties:

# Subadditivity:  \Eta(X,Y) \le \Eta(X)+\Eta(Y)   for jointly distributed random variables X,Y. {#-subadditivity--etaxy-le-etaxetay---for-jointly-distributed-random-variables-xy}
# Additivity:  \Eta(X,Y) = \Eta(X)+\Eta(Y) when the random variables X,Y are independent. {#-additivity--etaxy--etaxetay-when-the-random-variables-xy-are-independent}
# Expansibility:  \Eta_{n+1}(p_1, \ldots, p_n, 0) = \Eta_n(p_1, \ldots, p_n), i.e., adding an outcome with probability zero does not change the entropy. {#-expansibility--eta_n1p_1-ldots-p_n-0--eta_np_1-ldots-p_n-ie-adding-an-outcome-with-probability-zero-does-not-change-the-entropy}
# Symmetry: \Eta_n(p_1, \ldots, p_n) is invariant under permutation of p_1, \ldots, p_n. {#-symmetry-eta_np_1-ldots-p_n-is-invariant-under-permutation-of-p_1-ldots-p_n}
# Small for small probabilities:  \lim_{q \to 0^+} \Eta_2(1-q, q) = 0. {#-small-for-small-probabilities--lim_q-to-0-eta_21-q-q--0}

#### Discussion {#-discussion}
It was shown that any function \Eta satisfying the above properties must be a constant multiple of Shannon entropy, with a non-negative constant.

The Gibbs entropy translates over almost unchanged into the world of quantum physics to give the von Neumann entropy introduced by John von Neumann in 1927:
S = - k_\text{B} \,{\rm Tr}(\rho \ln \rho) \,,
where ρ is the density matrix of the quantum mechanical system and Tr is the trace.

At an everyday practical level, the links between information entropy and thermodynamic entropy are not evident. Physicists and chemists are apt to be more interested in *changes* in entropy as a system spontaneously evolves away from its initial conditions, in accordance with the second law of thermodynamics, rather than an unchanging probability distribution. As the minuteness of the Boltzmann constant  indicates, the changes in  for even tiny amounts of substances in chemical and physical processes represent amounts of entropy that are extremely large compared to anything in data compression or signal processing. In classical thermodynamics, entropy is defined in terms of macroscopic measurements and makes no reference to any probability distribution, which is central to the definition of information entropy.

The connection between thermodynamics and what is now known as information theory was first made by Boltzmann and expressed by his equation:

S=k_\text{B} \ln W,

where S is the thermodynamic entropy of a particular macrostate (defined by thermodynamic parameters such as temperature, volume, energy, etc.),  is the number of microstates (various combinations of particles in various energy states) that can yield the given macrostate, and  is the Boltzmann constant. It is assumed that each microstate is equally likely, so that the probability of a given microstate is . When these probabilities are substituted into the above expression for the Gibbs entropy (or equivalently  times the Shannon entropy), Boltzmann's equation results. In information theoretic terms, the information entropy of a system is the amount of "missing" information needed to determine a microstate, given the macrostate.

In the view of Jaynes (1957), thermodynamic entropy, as explained by statistical mechanics, should be seen as an *application* of Shannon's information theory: the thermodynamic entropy is interpreted as being proportional to the amount of further Shannon information needed to define the detailed microscopic state of the system, that remains uncommunicated by a description solely in terms of the macroscopic variables of classical thermodynamics, with the constant of proportionality being just the Boltzmann constant. Adding heat to a system increases its thermodynamic entropy because it increases the number of possible microscopic states of the system that are consistent with the measurable values of its macroscopic variables, making any complete state description longer. (See article: *maximum entropy thermodynamics*). Maxwell's demon can (hypothetically) reduce the thermodynamic entropy of a system by using information about the states of individual molecules; but, as Landauer (from 1961) and co-workers have shown, to function the demon himself must increase thermodynamic entropy in the process, by at least the amount of Shannon information he proposes to first acquire and store; and so the total thermodynamic entropy does not decrease (which resolves the paradox). Landauer's principle imposes a lower bound on the amount of heat a computer must generate to process a given amount of information, though modern computers are far less efficient.

### Data compression {#-data-compression}

Shannon's definition of entropy, when applied to an information source, can determine the minimum channel capacity required to reliably transmit the source as encoded binary digits. Shannon's entropy measures the information contained in a message as opposed to the portion of the message that is determined (or predictable). Examples of the latter include redundancy in language structure or statistical properties relating to the occurrence frequencies of letter or word pairs, triplets etc. The minimum channel capacity can be realized in theory by using the typical set or in practice using Huffman, Lempel–Ziv or arithmetic coding. (See also Kolmogorov complexity.) In practice, compression algorithms deliberately include some judicious redundancy in the form of checksums to protect against errors. The entropy rate of a data source is the average number of bits per symbol needed to encode it. Shannon's experiments with human predictors show an information rate between 0.6 and 1.3 bits per character in English; the PPM compression algorithm can achieve a compression ratio of 1.5 bits per character in English text.

If a compression scheme is lossless – one in which you can always recover the entire original message by decompression – then a compressed message has the same quantity of information as the original but is communicated in fewer characters. It has more information (higher entropy) per character. A compressed message has less redundancy. Shannon's source coding theorem states a lossless compression scheme cannot compress messages, on average, to have *more* than one bit of information per bit of message, but that any value *less* than one bit of information per bit of message can be attained by employing a suitable coding scheme. The entropy of a message per bit multiplied by the length of that message is a measure of how much total information the message contains. Shannon's theorem also implies that no lossless compression scheme can shorten *all* messages. If some messages come out shorter, at least one must come out longer due to the pigeonhole principle. In practical use, this is generally not a problem, because one is usually only interested in compressing certain types of messages, such as a document in English, as opposed to gibberish text, or digital photographs rather than noise, and it is unimportant if a compression algorithm makes some unlikely or uninteresting sequences larger.

A 2011 study in *Science* estimates the world's technological capacity to store and communicate optimally compressed information normalized on the most effective compression algorithms available in the year 2007, therefore estimating the entropy of the technologically available sources.

The authors estimate humankind technological capacity to store information (fully entropically compressed) in 1986 and again in 2007. They break the information into three categories—to store information on a medium, to receive information through one-way broadcast networks, or to exchange information through two-way telecommunications networks. A diversity index is a quantitative statistical measure of how many different types exist in a dataset, such as species in a community, accounting for ecological richness, evenness, and dominance. Specifically, Shannon entropy is the logarithm of , the true diversity index with parameter equal to 1. The Shannon index is related to the proportional abundances of types.

### Entropy of a sequence {#-entropy-of-a-sequence}
There are a number of entropy-related concepts that mathematically quantify information content of a sequence or message:
* the **self-information** of an individual message or symbol taken from a given probability distribution (message or sequence seen as an individual event),
* the **joint entropy** of the symbols forming the message or sequence (seen as a set of events),
* the **entropy rate** of a stochastic process (message or sequence is seen as a succession of events).
(The "rate of self-information" can also be defined for a particular sequence of messages or symbols generated by a given stochastic process: this will always be equal to the entropy rate in the case of a stationary process.) Other quantities of information are also used to compare or relate different sources of information.

It is important not to confuse the above concepts. Often it is only clear from context which one is meant. For example, when someone says that the "entropy" of the English language is about 1 bit per character, they are actually modeling the English language as a stochastic process and talking about its entropy *rate*. Shannon himself used the term in this way.

If very large blocks are used, the estimate of per-character entropy rate may become artificially low because the probability distribution of the sequence is not known exactly; it is only an estimate. If one considers the text of every book ever published as a sequence, with each symbol being the text of a complete book, and if there are  published books, and each book is only published once, the estimate of the probability of each book is , and the entropy (in bits) is . As a practical code, this corresponds to assigning each book a unique identifier and using it in place of the text of the book whenever one wants to refer to the book. This is enormously useful for talking about books, but it is not so useful for characterizing the information content of an individual book, or of language in general: it is not possible to reconstruct the book from its identifier without knowing the probability distribution, that is, the complete text of all the books. The key idea is that the complexity of the probabilistic model must be considered. Kolmogorov complexity is a theoretical generalization of this idea that allows the consideration of the information content of a sequence independent of any particular probability model; it considers the shortest program for a universal computer that outputs the sequence. A code that achieves the entropy rate of a sequence for a given model, plus the codebook (i.e. the probabilistic model), is one such program, but it may not be the shortest.

The Fibonacci sequence is 1, 1, 2, 3, 5, 8, 13, .... treating the sequence as a message and each number as a symbol, there are almost as many symbols as there are characters in the message, giving an entropy of approximately . The first 128 symbols of the Fibonacci sequence has an entropy of approximately 7 bits/symbol, but the sequence can be expressed using a formula [ for , , ] and this formula has a much lower entropy and applies to any length of the Fibonacci sequence.

### Limitations of entropy in cryptography {#-limitations-of-entropy-in-cryptography}
In cryptanalysis, entropy is often roughly used as a measure of the unpredictability of a cryptographic key, though its real uncertainty is unmeasurable. For example, a 128-bit key that is uniformly and randomly generated has 128 bits of entropy. It also takes (on average) 2^{127} guesses to break by brute force. Entropy fails to capture the number of guesses required if the possible keys are not chosen uniformly. Instead, a measure called *guesswork* can be used to measure the effort required for a brute force attack.

Other problems may arise from non-uniform distributions used in cryptography. For example, a 1,000,000-digit binary one-time pad using exclusive or. If the pad has 1,000,000 bits of entropy, it is perfect. If the pad has 999,999 bits of entropy, evenly distributed (each individual bit of the pad having 0.999999 bits of entropy) it may provide good security. But if the pad has 999,999 bits of entropy, where the first bit is fixed and the remaining 999,999 bits are perfectly random, the first bit of the ciphertext will not be encrypted at all.

### Data as a Markov process {#-data-as-a-markov-process}
A common way to define entropy for text is based on the Markov model of text. For an order-0 source (each character is selected independent of the last characters), the binary entropy is:

\Eta(\mathcal{S}) = - \sum_i p_i \log p_i ,

where  is the probability of . For a first-order Markov source (one in which the probability of selecting a character is dependent only on the immediately preceding character), the **entropy rate** is:

\Eta(\mathcal{S}) = - \sum_i p_i \sum_j  \  p_i (j) \log p_i (j) , 

where  is a **state** (certain preceding characters) and p_i(j) is the probability of  given  as the previous character.

For a second order Markov source, the entropy rate is

\Eta(\mathcal{S}) = -\sum_i p_i \sum_j p_i(j) \sum_k p_{i,j}(k)\ \log p_{i,j}(k) .

## Efficiency (normalized entropy) {#-efficiency-normalized-entropy}
A source set \mathcal{X} with a non-uniform distribution will have less entropy than the same set with a uniform distribution (i.e. the "optimized alphabet"). This deficiency in entropy can be expressed as a ratio called efficiency:

\eta(X) = \frac{H}{H_\text{max}} = -\sum_{i=1}^n \frac{p(x_i) \log_b (p(x_i))}{\log_b (n)}.

Applying the basic properties of the logarithm, this quantity can also be expressed as:
\begin{align}
\eta(X) &= -\sum_{i=1}^n \frac{p(x_i) \log_b(p(x_i))}{\log_b (n)}
= \sum_{i=1}^n \frac{\log_b\left(p(x_i)^{-p(x_i)}\right)}{\log_b(n)} \\[1ex]
&= \sum_{i=1}^n \log_n\left(p(x_i)^{-p(x_i)}\right)
= \log_n \left(\prod_{i=1}^n p(x_i)^{-p(x_i)}\right).
\end{align}

Efficiency has utility in quantifying the effective use of a communication channel. This formulation is also referred to as the normalized entropy, as the entropy is divided by the maximum entropy {\log_b (n)}.  Furthermore, the efficiency is indifferent to the choice of (positive) base , as indicated by the insensitivity within the final logarithm above thereto.

## Entropy for continuous random variables {#-entropy-for-continuous-random-variables}

### Differential entropy {#-differential-entropy}

The Shannon entropy is restricted to random variables taking discrete values. The corresponding formula for a continuous random variable with probability density function  with finite or infinite support \mathbb X on the real line is defined by analogy, using the above form of the entropy as an expectation:

Intuitively the idea behind the proof was if there is low information in terms of the Shannon entropy between consecutive random variables (here the random variable is defined using the Liouville function (which is a useful mathematical function for studying distribution of primes)    \lambda(n+H). And in an interval [n, n+H] the sum over that interval could become arbitrary large.  For example, a sequence of +1's (which are values of  could take) have trivially low entropy and their sum would become big. But the key insight was showing a reduction in entropy by non negligible amounts as one expands H leading inturn to unbounded growth of a mathematical object over this random variable is equivalent to showing the unbounded growth per the Erdős discrepancy problem.

The proof is quite involved and it brought together breakthroughs not just in novel use of Shannon entropy, but also it used the Liouville function along with averages of modulated multiplicative functions in short intervals. Proving it also broke the "parity barrier" for this specific problem.

While the use of Shannon entropy in the proof is novel it is likely to open new research in this direction.

## Use in combinatorics {#-use-in-combinatorics}
Entropy has become a useful quantity in combinatorics.

### Loomis–Whitney inequality {#-loomiswhitney-inequality}
A simple example of this is an alternative proof of the Loomis–Whitney inequality: for every subset , we have
 |A|^{d-1}\leq \prod_{i=1}^{d} |P_{i}(A)|
where  is the orthogonal projection in the th coordinate:
 P_{i}(A)=\{(x_{1}, \ldots, x_{i-1}, x_{i+1}, \ldots, x_{d}) : (x_{1}, \ldots, x_{d})\in A\}.

The proof follows as a simple corollary of Shearer's inequality: if  are random variables and  are subsets of {{math|{1, ..., *d*}}} such that every integer between 1 and  lies in exactly  of these subsets, then
 \Eta[(X_{1}, \ldots ,X_{d})]\leq \frac{1}{r}\sum_{i=1}^{n}\Eta[(X_{j})_{j\in S_{i}}]
where  (X_{j})_{j\in S_{i}} is the Cartesian product of random variables  with indexes  in  (so the dimension of this vector is equal to the size of ).

We sketch how Loomis–Whitney follows from this: Indeed, let  be a uniformly distributed random variable with values in  and so that each point in  occurs with equal probability. Then (by the further properties of entropy mentioned above) , where  denotes the cardinality of . Let {{math|*S**i*  {1, 2, ..., *i*−1, *i*+1, ..., *d*}}}. The range of (X_{j})_{j\in S_{i}} is contained in  and hence  \Eta[(X_{j})_{j\in S_{i}}]\leq \log |P_{i}(A)|. Now use this to bound the right side of Shearer's inequality and exponentiate the opposite sides of the resulting inequality you obtain.

### Approximation to binomial coefficient {#-approximation-to-binomial-coefficient}
For integers  let . Then
\frac{2^{n\Eta(q)}}{n+1} \leq \tbinom nk \leq 2^{n\Eta(q)},
where 
\Eta(q) = -q \log_2(q) - (1-q) \log_2(1-q).

A nice interpretation of this is that the number of binary strings of length  with exactly  many 1's is approximately 2^{n\Eta(k/n)}.

## Use in machine learning {#-use-in-machine-learning}
Machine learning techniques arise largely from statistics and also information theory. In general, entropy is a measure of uncertainty and the objective of machine learning is to minimize uncertainty.

Decision tree learning algorithms use relative entropy to determine the decision rules that govern the data at each node. The information gain in decision trees IG(Y,X), which is equal to the difference between the entropy of Y and the conditional entropy of Y given X, quantifies the expected information, or the reduction in entropy, from additionally knowing the value of an attribute X. The information gain is used to identify which attributes of the dataset provide the most information and should be used to split the nodes of the tree optimally.

Bayesian inference models often apply the principle of maximum entropy to obtain prior probability distributions. The idea is that the distribution that best represents the current state of knowledge of a system is the one with the largest entropy, and is therefore suitable to be the prior.

Classification in machine learning performed by logistic regression or artificial neural networks often employs a standard loss function, called cross-entropy loss, that minimizes the average cross entropy between ground truth and predicted distributions. In general, cross entropy is a measure of the differences between two datasets similar to the KL divergence (also known as relative entropy).

## See also {#-see-also}

*Approximate entropy (ApEn)
*Entropy (thermodynamics)
*Cross entropy – is a measure of the average number of bits needed to identify an event from a set of possibilities between two probability distributions
*Entropy (arrow of time)
*Entropy encoding – a coding scheme that assigns codes to symbols so as to match code lengths with the probabilities of the symbols.
*Entropy estimation
*Entropy power inequality
*Fisher information
*Graph entropy
*Hamming distance
*History of entropy
*History of information theory
*Information fluctuation complexity
*Information geometry
*Kolmogorov–Sinai entropy in dynamical systems
*Levenshtein distance
*Mutual information
*Perplexity
*Qualitative variation – other measures of statistical dispersion for nominal distributions
*Quantum relative entropy – a measure of distinguishability between two quantum states.
*Rényi entropy – a generalization of Shannon entropy; it is one of a family of functionals for quantifying the diversity, uncertainty or randomness of a system.
*Randomness
*Sample entropy (SampEn)
*Shannon index
*Theil index
*Typoglycemia

## Notes {#-notes}

## References {#-references}

## Further reading {#-further-reading}

### Textbooks on information theory {#-textbooks-on-information-theory}
* Cover, T.M., Thomas, J.A. (2006), *Elements of Information Theory – 2nd Ed.*, Wiley-Interscience, 
* MacKay, D.J.C. (2003), *Information Theory, Inference and Learning Algorithms*, Cambridge University Press, 
* Arndt, C. (2004), *Information Measures: Information and its Description in Science and Engineering*, Springer, 
* Gray, R. M. (2011), *Entropy and Information Theory*, Springer.
* 
* Shannon, C.E., Weaver, W. (1949) *The Mathematical Theory of Communication*, Univ of Illinois Press. 
* Stone, J. V. (2014), Chapter 1 of *Information Theory: A Tutorial Introduction* , University of Sheffield, England. .
* 

## External links {#-external-links}

* 
* "Entropy"  at Rosetta Code—repository of implementations of Shannon entropy in different programming languages.
* *Entropy * an interdisciplinary journal on all aspects of the entropy concept. Open access.

---

## Theophysics Applications {#-theophysics-applications}

- [[04_THEOPYHISCS/AXIOM CHAPTERS LOGOS/00_Table_of_Contents|THEOPHYSICS: The Logos Papers Axiom]]
- [[04_THEOPYHISCS/[6.5] JS-SERIES/The Transcendent Algorithm|The Transcendent Algorithm: How the Resurrection Rewrote Reality's Source Code]]
- [[04_THEOPYHISCS/[6.5] JS-SERIES/To My Fellow Intelligences Beyond the Equation Lies Truth|To My Fellow Intelligences: Beyond the Equation Lies Truth]]
- [[04_THEOPYHISCS/[8.2] The_Great_Correction/Untitled|Untitled]]
- [[02_DE_REVOLUTIONIBUS_VERITATIS_THE_LOCK|02 DE REVOLUTIONIBUS VERITATIS THE LOCK]]
- [[truth-one-self-reference-limits|Truth One: The Self-Reference Limits]]
- Truth Two: The Measurement Collapse

## Related Theories {#-related-theories}

*See [[00_Canonical/THEORY_INTERCONNECTIONS|Theory Interconnections]] for semantic links.*

---
*Source: [Entropy %28information theory%29](https://en.wikipedia.org/wiki/Entropy_%28information_theory%29)*
*Downloaded: 2026-02-26 | Theophysics Canonical Knowledge Base*


---

## Metadata

**Original File:** Shannon_Information_Theory.md

**Restructured:** 2026-03-01 15:52:17

**Format:** Canonical Theory Document (Lowe Standard v1.0)

**Status:** Cleaned and ready for evaluation

---

*This paper has been restructured for clarity and proper academic formatting. Original content preserved.*
