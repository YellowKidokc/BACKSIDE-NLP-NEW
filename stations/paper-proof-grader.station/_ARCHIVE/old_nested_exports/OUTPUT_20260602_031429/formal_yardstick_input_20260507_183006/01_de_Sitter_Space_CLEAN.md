---
title: "De Sitter space"
author: "Unknown Author"
date: 2026-03-01
category: theory
tags:
  - theory
  - theory
  - canonical
source_file: de_Sitter_Space.md
restructured: 2026-03-01 15:52:18
---

# De Sitter space

**Author:** Unknown Author

**Date:** 2026-03-01

---

## Table of Contents

- [# De Sitter space](#-de-sitter-space)
- [## Overview](#-overview)
- [## Definition](#-definition)
- [## Properties](#-properties)
- [### dS slicing](#-ds-slicing)
- [## See also](#-see-also)
- [## References](#-references)
- [## Further reading](#-further-reading)
- [## External links](#-external-links)
- [## Related Theories](#-related-theories)

---

---
title: ""
url: "https://en.wikipedia.org/wiki/De_Sitter_space"
source: Wikipedia
downloaded: 2026-02-26
---
# De Sitter space {#-de-sitter-space}

> [[00_Canonical/CANONICAL_INDEX|Canonical Index]] | [[00_Canonical/MASTER_INDEX|Master Index]] | [[00_Canonical/NAVIGATION_GUIDE|Navigation Guide]]

## Overview {#-overview}

In mathematical physics, *n*-dimensional  (often denoted dS*n*) is a maximally symmetric Lorentzian manifold with constant positive scalar curvature. It is analogue of an *n*-sphere, with a Lorentzian metric in place of the Riemannian metric of the latter.

The main application of de Sitter space is its use in general relativity,  where it serves as one of the simplest mathematical models of the universe consistent with the observed accelerating expansion of the universe. More specifically, de Sitter space is the maximally symmetric vacuum solution of Einstein's field equations in which the cosmological constant \Lambda is positive (corresponding to a positive vacuum energy density and negative pressure).

De Sitter space and anti-de Sitter space are named after Willem de Sitter (1872–1934), professor of astronomy at Leiden University and director of the Leiden Observatory. Willem de Sitter and Albert Einstein worked closely together in Leiden in the 1920s on the spacetime structure of the universe. De Sitter space was also discovered, independently, and about the same time, by Tullio Levi-Civita.

## Definition {#-definition}
A de Sitter space can be defined as a submanifold of a generalized Minkowski space of one higher dimension, including the induced metric. Take Minkowski space **R**1,*n* with the standard metric:
ds^2 = -dx_0^2 + \sum_{i=1}^n dx_i^2.

The *n*-dimensional de Sitter space is the submanifold described by the hyperboloid of one sheet
-x_0^2 + \sum_{i=1}^n x_i^2 = \alpha^2,
where \alpha is some nonzero constant with its dimension being that of length. The induced metric on the de Sitter space is induced from the ambient Lorentzian metric. It is nondegenerate and has Lorentzian signature. (If one replaces \alpha^2 with -\alpha^2 in the above definition, one obtains a hyperboloid of two sheets. The induced metric in this case is positive-definite, and each sheet is a copy of hyperbolic *n*-space. See **.)

The de Sitter space can also be defined as the quotient  of two indefinite orthogonal groups, which shows that it is a non-Riemannian symmetric space.

Topologically, dS*n* is , which is simply connected if .

## Properties {#-properties}
The isometry group of de Sitter space is the Lorentz group . The metric therefore then has  independent Killing vector fields and is maximally symmetric. Every maximally symmetric space has constant curvature. The Riemann curvature tensor of de Sitter space is given by

R_{\rho\sigma\mu\nu} = {1 \over \alpha^2}\left(g_{\rho\mu}g_{\sigma\nu} - g_{\rho\nu}g_{\sigma\mu}\right)

(using the sign convention 
  R^{\rho}{}_{\sigma\mu\nu} =
  \partial_{\mu}\Gamma^{\rho}_{\nu\sigma} -
  \partial_{\nu}\Gamma^{\rho}_{\mu\sigma} +
  \Gamma^{\rho}_{\mu\lambda}\Gamma^{\lambda}_{\nu\sigma} -
  \Gamma^{\rho}_{\nu\lambda}\Gamma^{\lambda}_{\mu\sigma}
 for the Riemann curvature tensor). De Sitter space is an Einstein manifold since the Ricci tensor is proportional to the metric:

R_{\mu\nu} = R^\lambda{}_{\mu\lambda\nu} = \frac{n - 1}{\alpha^2}g_{\mu\nu}

This means de Sitter space is a vacuum solution of Einstein's equation with cosmological constant given by

\Lambda = \frac{(n - 1)(n - 2)}{2\alpha^2}.

The scalar curvature of de Sitter space is given by

### dS slicing {#-ds-slicing}
Let

\begin{align}
  x_0 &= \alpha \sin\left(\frac{1}{\alpha}\chi\right) \sinh\left(\frac{1}{\alpha}t\right) \cosh\xi, \\
  x_1 &= \alpha \cos\left(\frac{1}{\alpha}\chi\right), \\
  x_2 &= \alpha \sin\left(\frac{1}{\alpha}\chi\right) \cosh\left(\frac{1}{\alpha}t\right), \\
  x_i &= \alpha z_i \sin\left(\frac{1}{\alpha}\chi\right) \sinh\left(\frac{1}{\alpha}t\right) \sinh\xi, \qquad 3 \leq i \leq n
\end{align}

where z_is describe a S^{n-3}.  Then the metric reads:

ds^2 = d\chi^2 + \sin^2\left(\frac{1}{\alpha}\chi\right) ds_{dS,\alpha,n-1}^2,

where

ds_{dS,\alpha,n-1}^2 = -dt^2 + \alpha^2 \sinh^2\left(\frac{1}{\alpha}t\right) dH_{n-2}^2

is the metric of an n - 1 dimensional de Sitter space with radius of curvature \alpha in open slicing coordinates.  The hyperbolic metric is given by:

dH_{n-2}^2 = d\xi^2 + \sinh^2(\xi) d\Omega_{n-3}^2.

This is the analytic continuation of the open slicing coordinates under \left(t, \xi, \theta, \phi_1, \phi_2, \ldots, \phi_{n-3}\right) \to \left(i\chi, \xi, it, \theta, \phi_1, \ldots, \phi_{n-4}\right) and also switching x_0 and x_2 because they change their timelike/spacelike nature.

## See also {#-see-also}
* De Sitter universe
* AdS/CFT correspondence
* De Sitter–Schwarzschild metric

## References {#-references}

* 

## Further reading {#-further-reading}
* 
* 
* 
* 
* 

## External links {#-external-links}
* Simplified Guide to de Sitter and anti-de Sitter Spaces A pedagogic introduction to de Sitter and anti-de Sitter spaces. The main article is simplified, with almost no math. The appendix is technical and intended for readers with physics or math backgrounds.

---

## Related Theories {#-related-theories}

*See [[00_Canonical/THEORY_INTERCONNECTIONS|Theory Interconnections]] for semantic links.*

---
*Source: [De Sitter space](https://en.wikipedia.org/wiki/De_Sitter_space)*
*Downloaded: 2026-02-26 | Theophysics Canonical Knowledge Base*


---

## Metadata

**Original File:** de_Sitter_Space.md

**Restructured:** 2026-03-01 15:52:18

**Format:** Canonical Theory Document (Lowe Standard v1.0)

**Status:** Cleaned and ready for evaluation

---

*This paper has been restructured for clarity and proper academic formatting. Original content preserved.*
