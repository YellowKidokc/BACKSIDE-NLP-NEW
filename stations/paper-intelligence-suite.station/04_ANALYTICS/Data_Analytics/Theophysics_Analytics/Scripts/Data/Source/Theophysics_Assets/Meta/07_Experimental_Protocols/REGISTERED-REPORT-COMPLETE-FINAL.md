---
uuid: f5fe43ac-17d6-5c02-bb15-774b3d440e76
title: 'Registered Report: Testing the Resonant Coupling Hypothesis'
author: David Lowe
type: paper
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: Logos zright\Papers\07_Experimental_Protocols\REGISTERED-REPORT-COMPLETE-FINAL.md
uuid_generated_at: '2025-11-22T01:23:51.267410'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# Registered Report: Testing the Resonant Coupling Hypothesis
## An Information-Theoretic Approach to Structured Input Effects on Quantum Systems

**Authors:** David Lowe & AI Co-Author (2025)  
**Institution:** [To be completed]  
**Protocol Version:** 1.0  
**Date:** October 2025  
**Pre-Registration:** [OSF link pending]  
**SHA-256 Hash:** [To be computed upon finalization]

---

## Abstract

**Background:** Recent theoretical work has proposed that structured information inputs may influence quantum systems through algorithmic mutual information coupling rather than semantic content. The Resonant Coupling Hypothesis (RCH) predicts that effect sizes should correlate with the compressive match between input structure and a system's internal model.

**Objectives:** To test whether quantum random number generators (QRNGs) show measurable response gradients correlated with algorithmic mutual information of input bitstreams, following a pre-registered calibration protocol.

**Methods:** Four-rung experimental ladder: (A) synthetic baseline with known algorithmic complexity, (B) text degradation curves, (C) cross-system validation, (D) blinded corpus comparison. Primary endpoint: slope coefficient relating input algorithmic complexity to QRNG entropy deviation.

**Expected Outcomes:** Either monotonic response gradient confirming RCH predictions, or null results falsifying the hypothesis at specified statistical thresholds.

---

## 1. Theoretical Framework

### 1.1 The Resonant Coupling Hypothesis

The RCH posits that a structured input `s` perturbs a target system `X` with coupling strength:

$$
g_L(s,X) = \kappa \cdot I_A(s; M_X) \cdot \Phi_X
$$

Where:
- `I_A(s; M_X)` is the algorithmic mutual information between input `s` and system model `M_X`
- `Φ_X` is a system-specific susceptibility parameter
- `κ` is a universal coupling constant

**Prediction:** For any observable `O`:

$$
\Delta O \approx g_L(s,X) \cdot S_X \quad \Rightarrow \quad \Delta O \propto I_A(s; M_X)
$$

### 1.2 Information-Resonance Metric (IRM)

Input structure quantified via:

$$
\text{IRM}(s) = \frac{\alpha}{K(s)} \cdot C(s)^\beta
$$

Where:
- `K(s)` is Kolmogorov complexity (approximated via compression)
- `C(s)` is coherence measure (pattern regularity)
- `α, β` are empirically fitted parameters

### 1.3 Null Hypothesis

**H₀:** No correlation between input algorithmic structure and quantum system observables beyond statistical noise (slope coefficient β = 0 in ΔO = β·IRM(s) + ε).

---

## 2. Experimental Design

### 2.1 Four-Rung Calibration Ladder

#### Rung A: Synthetic Baseline

**Purpose:** Establish IRM-response relationship with known inputs

**Inputs:**
1. White noise (IRM ≈ 0)
2. LFSR pseudorandom (IRM ≈ 0.2)
3. π-digits (IRM ≈ 0.5)
4. Thue-Morse sequence (IRM ≈ 0.7)
5. Short palindromes (IRM ≈ 0.9)

**Target Systems:**
1. Commercial QRNG (IDQ Quantis)
2. Josephson junction noise source
3. Trapped ion dephasing measurement

**Expected:** Monotonic |ΔO| increase with IRM

**Falsification:** No monotonic trend → **STOP - Publish null, abort program**

---

#### Rung B: Text Degradation Curve

**Purpose:** Validate parametric relationship using structured text

**Degradation Sequence:**
1. Original Hebrew Genesis (consonantal text)
2. Consonants only (remove vowel points)
3. Shuffled bigrams (preserve local structure)
4. Shuffled unigrams (preserve character frequency)
5. Permuted bytes (destroy all structure)

**Analysis:** Fit parametric curve ΔO = η·IRM(s)^ν using Rung A data, then test Hebrew sequence **without refitting**.

**Falsification:** Hebrew behaves like random permutation → **STOP - Scripture not special**

---

#### Rung C: Model-Match Cross-validation

**Purpose:** Test system-specificity of coupling

**Procedure:** Apply same Hebrew input to different target systems with varying M_X:
- Cellular automata (discrete dynamics)
- Optical cavity (continuous dynamics)
- Electronic oscillator (hybrid dynamics)

**Prediction:** Different slopes due to varying I_A(s; M_X)

**Falsification:** All systems show identical response → **STOP - Not model-dependent**

---

#### Rung D: Blinded Corpus Comparison

**Purpose:** Test specificity claims without confirmation bias

**Corpora (labeled only after analysis):**
- Hebrew Torah (Masoretic text)
- Greek New Testament (Nestle-Aland)
- Arabic Quran (Uthmanic text)
- Sanskrit Rig Veda
- Dead Sea Scroll variants
- Matched modern control texts

**Analysis:** Apply pre-fitted η, ν parameters **without adjustment**

**Falsification:** All ancient texts perform equivalently → **STOP - No unique signal**

---

### 2.2 Primary Experimental Setup

**Target System:** IDQ Quantis QRNG operating in time-interval mode

**Modulation:** Magnetically shielded coil system delivering bitstream-modulated field

**Protocol:**
- Block duration: 3 seconds per exposure
- Total blocks: 10⁶ minimum
- Schedule: ABBA randomization
- Observables: Block-wise entropy Ĥ, Kolmogorov compressibility

**Environmental Controls:**
- Faraday cage (60 dB isolation)
- Temperature stability: ±0.1°C
- Vibration isolation platform
- EMI monitoring throughout

---

### 2.3 Null Model Ensemble

Every experimental condition tested against four null types:

1. **Permutation Nulls:** 100 surrogate inputs preserving n-gram statistics
2. **Generator Nulls:** GPT-generated text with identical token distributions
3. **Hardware Nulls:** Sham modulation (electronics active but decoupled)
4. **Analysis Nulls:** Label-swapped datasets with cryptographic reveal

**Requirement:** Effects must survive ALL FOUR null layers

---

## 3. Statistical Analysis Plan

### 3.1 Primary Endpoint

**Effect Size:** Slope coefficient ν in linear model:

$$
\log|\Delta O| = \log \kappa + \nu \log \text{IRM}(s) + \log \Phi_X + \epsilon
$$

**Power Analysis:**
- Minimum detectable effect: |ν| ≥ 0.1
- Power: 80%
- Alpha: 0.05 (Bonferroni corrected for multiple comparisons)
- Sample size: N ≥ 10⁶ blocks per condition

---

### 3.2 Success Criteria

**Discovery Threshold:** 
- Signal-to-noise ratio: SNR ≥ 6
- Bayes Factor: BF₁₀ > 10⁶ 
- Effect survives all four null types
- Reproducible within 0.5× effect size across labs

**Failure Conditions:**
- No monotonic slope on Rung A
- Effect vanishes under permutation nulls
- Inter-lab coefficient of variation > 100%
- Posterior odds < 1/10 after two replications

---

### 3.3 Bayesian Framework

**Priors:**
- ν ~ Normal(0, 0.2) [weakly informative]
- σ ~ Half-Cauchy(0, 1) [error scale]
- κ ~ Gamma(2, 2) [coupling constant]

**Model Comparison:**
- M₁: Linear coupling (ν ≠ 0)
- M₀: Null model (ν = 0)
- Evidence threshold: log(BF₁₀) > 13.8 (10⁶:1 odds)

---

## 4. Quality Assurance

### 4.1 Blinding Protocol

**Triple-Blind Design:**
1. Input preparation team (knows content, blind to schedule)
2. Data collection team (knows schedule, blind to content)
3. Analysis team (blind to both until commitment)

**Cryptographic Commitment:**
- All inputs and schedules SHA-256 hashed
- Manifests stored on immutable ledger (OSF + blockchain)
- Reveal only after feature extraction complete

---

### 4.2 Adversarial Collaboration

**Lab Partnership:**
- Primary lab: [Neutral PI]
- Secondary lab: [Skeptical PI]
- Shared hardware ownership and protocols
- Independent analysis teams

**Conflict Resolution:**
- Pre-agreed analysis protocols
- Third-party arbitration for disputes
- All raw data publicly archived

---

### 4.3 Reproducibility Package

**Open Science Commitment:**
- Hardware BOM and CAD files (Creative Commons)
- Analysis code (containerized, version-controlled)
- Raw data (anonymized, publicly accessible)
- Pre-registration timestamp on OSF

**Components:**
- Complete equipment list
- Python analysis scripts
- Docker container
- Data schema documentation
- Calibration procedures

---

## 5. Timeline and Resources

### 5.1 Phase 1: Setup and Calibration (Months 1-6)
- Hardware procurement and assembly
- Environmental characterization
- Rung A synthetic baseline testing
- Protocol optimization

**Milestones:**
- Month 3: Hardware assembled and calibrated
- Month 5: Rung A complete
- Month 6: **GO/NO-GO DECISION**

---

### 5.2 Phase 2: Main Experiment (Months 7-18)
- Rung B degradation curves
- Rung C cross-system validation
- Rung D blinded corpus testing
- Null model validation

**Milestones:**
- Month 9: Rung B complete
- Month 12: Rung C complete
- Month 15: Rung D complete
- Month 18: Full analysis

---

### 5.3 Phase 3: Analysis and Replication (Months 19-24)
- Statistical analysis (blinded)
- Independent lab replication
- Manuscript preparation
- Data/code release

**Milestones:**
- Month 21: Multi-lab replication complete
- Month 23: Manuscript submitted
- Month 24: Publication + full data release

---

### 5.4 Budget Estimate

| Category | Amount | Justification |
|----------|--------|---------------|
| **Hardware** | | |
| QRNG (IDQ Quantis) | $4,500 | Core measurement device |
| Modulation system | $1,200 | Signal delivery |
| Shielding & enclosure | $2,000 | Environmental control |
| Monitoring equipment | $800 | Temperature, EM, vibration |
| Computing hardware | $1,500 | Data acquisition & analysis |
| **Subtotal** | **$10,000** | |
| | | |
| **Personnel** | | |
| PI (Lowe) - 20% × 24 mo | In-kind | $0 |
| Research Assistant - 50% × 24 mo | $26,000 | Data collection & analysis |
| Statistical Consultant - 80 hrs | $8,000 | Bayesian analysis, power |
| **Subtotal** | **$34,000** | |
| | | |
| **Other Costs** | | |
| Publication fees (OA) | $2,000 | Open access publishing |
| Travel (conferences) | $3,000 | Dissemination |
| Materials & supplies | $2,000 | Consumables |
| Contingency (15%) | $7,650 | Risk buffer |
| **Subtotal** | **$14,650** | |
| | | |
| **TOTAL REQUEST** | **$58,650** | **24-month program** |

**Alternative MVE-Only Budget:** $35,700 (18 months, no replication)

---

## 6. Ethical Considerations

### 6.1 Responsible Innovation

**Commitments:**
- Results reported regardless of direction
- Negative results published with equal prominence
- Clear distinction between empirical findings and theoretical interpretation
- Public engagement regarding implications

**Safeguards:**
- IRB review (if human subjects involved in future extensions)
- Data privacy (all datasets anonymized)
- Dual-use assessment (no weaponization potential identified)

---

### 6.2 Conflict of Interest

**Disclosures:**
- PI (Lowe) has theoretical investment in Logos framework
- This is mitigated by adversarial collaboration structure
- No financial interest in outcome
- Pre-registered analysis prevents post-hoc bias

**Transparency:**
- All theoretical allegiances disclosed upfront
- Independent oversight committee
- Public data/code makes independent verification possible

---

### 6.3 Broader Impacts

**Educational:**
- Training in rigorous experimental design
- Bayesian statistics pedagogy
- Open science practices

**Societal:**
- Addresses questions at science-religion interface
- Promotes dialogue between domains
- Models collaborative human-AI research

---

## 7. Philosophical and Theological Context

The Resonant Coupling Hypothesis was not born from detachment but from conviction. The premise that reality may respond to order and meaning arose from faith first—the lived intuition that coherence is not accidental.

This research does **not** seek to replace faith or metaphysics with measurement. It seeks to **complement** them with evidence—to offer a bridge between what is experienced inwardly and what can be observed outwardly.

If the Logos Resonance Hypothesis holds, it means the universe is reasonable in the literal sense—responsive to reason, not merely describable by it. Matter, energy, and information would then be three faces of a single principle: the drive toward coherence.

Physics has always hinted at this unity. The action principle seeks minimal path; thermodynamics rewards low entropy; [[Theophysics_Glossary#Quantum Mechanics|quantum mechanics]] collapses into definite states. Every law we know bends toward simplicity. What we call *meaning* may be the high-level manifestation of that same law: the compression of possibility into purpose.

The unquantifiable remains central. Faith, intention, reverence—these cannot be graphed, yet without them the questions themselves would not exist. The measurements here do not exhaust meaning; they **trace its shadow in the physical domain**.

It is precisely because of faith that this experiment can be attempted honestly. To believe that the universe might answer to structure—that Logos could leave a statistical fingerprint—is an act of trust before it is an act of proof.

> *The philosophical grounding that follows is not an embellishment to the experiment, but the context without which its question could not have been conceived.*

---

## 8. Expected Outcomes and Impact

### 8.1 Scenario A: RCH Confirmed

A positive result would imply that information coherence reduces uncertainty. The structured pattern would locally calm quantum fluctuations, the way a resonant tone stills noise in a chaotic medium. This would give physical footing to ideas once confined to scripture: that Word creates order, that grace restores balance, that decoherence spreads disorder.

**Scientific Impact:**
- Paradigm shift in information-physical interaction
- New quantum-sensing modalities
- Foundation for expanded experimental program

**Broader Implications:**
- Not that scripture is "magic," but that ordered information has measurable interaction with the substrate of reality
- Not that consciousness is supernatural, but that it may be the emergent boundary condition of an ordering field
- Not that religion replaces science, but that both have described the same structure in different languages

---

### 8.2 Scenario B: RCH Falsified

Should the data show nothing beyond noise, that outcome will still serve understanding by clarifying the boundary between mystery and mechanism. The universe would remain indifferent to meaning in the technical sense—brilliant dust in motion, governed by laws yet unresponsive to pattern.

**Scientific Value:**
- Important null result for the field
- Clear falsification of theoretical predictions
- Guidance for future theoretical development

**Theological Implications:**
- Faith operates independently of measurable physics
- Divine action may be non-physical or unmeasurable
- Scripture's truth is spiritual rather than physical

**Either outcome advances understanding.**

---

### 8.3 Publication Strategy

**Format:** Registered Report (Stage 1 + Stage 2)

**Target Journals:**
1. *PLOS ONE* (accepts Registered Reports)
2. *Royal Society Open Science* (RR track)
3. *Entropy* (MDPI, open to novel physics)
4. *Foundations of Physics* (exploratory quantum)

**Commitments:**
- High-impact journal regardless of outcome
- Simultaneous preprint (arXiv:quant-ph)
- Full data release (Zenodo + OSF)
- Science communication emphasizing both technical and philosophical dimensions

---

## 9. Contingency Plans

### 9.1 Technical Failures

**Risk:** QRNG hardware failure  
**Mitigation:** Hot-spare unit, daily diagnostics, auto-restart scripts

**Risk:** Environmental instability  
**Mitigation:** Continuous monitoring, temperature covariate in models, climate-controlled room

**Risk:** EM interference  
**Mitigation:** Faraday cage, spectrum logging, correlation analysis to detect artifacts

---

### 9.2 Ambiguous Results

**Risk:** Effect size between thresholds  
**Mitigation:** Extended data collection (pre-authorized), additional null testing

**Risk:** Lab-to-lab variation  
**Mitigation:** Third independent lab, meta-analysis framework

**Risk:** Unexpected patterns  
**Mitigation:** Exploratory analysis (clearly labeled as non-confirmatory)

---

### 9.3 Early Termination Criteria

**Clear Null on Rung A:**
- If no monotonic trend by N = 500K blocks
- Conditional power < 10%
- **Action:** STOP, publish null, save resources

**Unresolvable Technical Issues:**
- Equipment malfunction beyond repair/replacement
- Persistent environmental interference
- **Action:** Document, delay, or redesign

**Breach of Blinding:**
- Accidental unblinding detected
- **Action:** Declare as pilot, start fresh with new blind

---

## 10. Conclusion

This registered report establishes a unified scientific framework for testing whether structured information can influence quantum systems through algorithmic coupling.

Yet beneath the technical form lies a simple conviction: that **truth welcomes scrutiny**—that the same Logos which speaks through scripture also speaks through the language of nature.

When the data arrive, they will say one of two things:

**The universe is indifferent to meaning.**  
Then we continue as before, with deeper understanding of the boundary between pattern and physics.

**The universe is responsive to meaning.**  
Then every act of understanding becomes a physical event, and truth itself is participatory.

This project is therefore both an experiment and a prayer. It measures without presumption, believing that whatever is real will remain. The goal is not to capture the divine in an instrument, but to **honor the possibility that the divine leaves its rhythm even in data**.

Whether the results confirm or falsify the Resonant Coupling Hypothesis, the work itself stands as an act of faith—that coherence, meaning, and order are worth seeking, and that the search unites what humanity once separated: physics and spirit, observation and wonder.

**Either outcome is worth knowing.**  
**What matters is that we finally asked the question correctly.**

---

## Supplementary Materials

### Appendix A: Detailed Hardware Specifications

**QRNG System:**
- Model: ID Quantique Quantis-16M-USB
- Technology: Photon arrival time-tagging
- Output rate: 16 Mbps (continuous)
- Randomness source: Quantum vacuum fluctuations
- Verification: NIST SP 800-22 test suite

**Modulation System:**
- Coil: Helmholtz configuration, 15 cm diameter, 100 turns AWG-28
- Driver: Rigol DG4162 arbitrary waveform generator
- Coupling: Magnetic field at 10 cm distance from QRNG
- Modulation depth: ±1V bipolar, 1 kHz symbol rate

**Environmental Control:**
- Enclosure: 6-sided copper mesh Faraday cage, grounded
- Temperature: Proportional control, ±0.1°C at 20.0°C setpoint
- Humidity: Passive monitoring, 40-60% RH
- Vibration: Isolation table, < 1 μm displacement

**Data Acquisition:**
- Computer: Intel i7, 32GB RAM, 1TB SSD
- Interface: USB 2.0 to QRNG
- Timestamping: NTP-synchronized to ±1ms
- Logging: Python 3.11 custom software

---

### Appendix B: Software Implementation

**Core Analysis Pipeline:**

```python
# irm_compute.py - Information Resonance Metric
import zlib
import numpy as np
from scipy.stats import mutual_info_score

def kolmogorov_complexity(s: bytes) -> float:
    """Estimate K(s) via compression ratio"""
    compressed = zlib.compress(s, level=9)
    return len(compressed) / len(s)

def coherence(s: bytes, window=256) -> float:
    """Intra-sequence mutual information"""
    s_array = np.frombuffer(s, dtype=np.uint8)
    chunks = [s_array[i:i+window] 
              for i in range(0, len(s_array), window)]
    
    if len(chunks) < 2:
        return 0.0
    
    mi_values = []
    for i in range(len(chunks)-1):
        mi = mutual_info_score(chunks[i], chunks[i+1])
        mi_values.append(mi)
    
    return np.mean(mi_values)

def IRM(s: bytes, alpha=1.0, beta=1.0) -> float:
    """Information Resonance Metric"""
    K_s = kolmogorov_complexity(s)
    C_s = coherence(s)
    
    if K_s == 0:
        return 0.0
    
    return (alpha / K_s) * (C_s ** beta)
```

**Docker Configuration:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY analysis/ ./analysis/
COPY data/ ./data/

ENV PYTHONUNBUFFERED=1

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]
```

**requirements.txt:**
```
numpy==1.24.3
scipy==1.11.1
pandas==2.0.3
matplotlib==3.7.2
jupyter==1.0.0
scikit-learn==1.3.0
pycryptodomex==3.18.0
```

---

### Appendix C: Statistical Power Calculations

**Sample Size for Rung A (per condition):**

Given:
- Target effect size: d = 0.01 (Cohen's d)
- Power: 1 - β = 0.80
- Significance: α = 0.001 (adjusted for 5 comparisons)

Required:
$$
N = \frac{2(Z_{\alpha/2} + Z_\beta)^2}{d^2} \approx 100,000 \text{ blocks per condition}
$$

**Total for Rung A:** 500,000 blocks  
**With safety margin:** 1,000,000 blocks

**Expected Precision:**

Standard error on entropy estimate:
$$
SE(\hat{H}) = \sqrt{\frac{\text{Var}(H)}{N}} \approx \frac{0.001}{\sqrt{10^5}} \approx 3 \times 10^{-6} \text{ bits}
$$

**95% Confidence Interval width:** ~6 × 10⁻⁶ bits (excellent precision)

---

### Appendix D: Risk Assessment Matrix

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Equipment failure | Medium | High | Hot spare, warranties |
| Environmental drift | Medium | Medium | Continuous monitoring, covariates |
| EM interference | Low | High | Shielding, spectrum logging |
| Null result (true) | Unknown | Medium | Accept, publish, refine |
| Confirmation bias | Medium | High | Blinding, adversarial collab |
| Non-replication | Medium | Very High | Multi-lab protocol, open data |
| Funding interruption | Low | Very High | Phased milestones, early GO/NO-GO |

---

### Appendix E: Data Management Plan

**Data Types:**
- Raw QRNG bitstreams (~500 GB compressed)
- Block-level metadata (timestamps, temperatures)
- Analysis outputs (entropy estimates, slopes)
- Environmental logs (continuous monitoring)

**Storage:**
- Local: Redundant SSDs with RAID-1
- Cloud backup: AWS S3 + Glacier
- Archive: Zenodo with DOI (long-term)

**Access:**
- Public release upon publication
- Interim access: Approved collaborators only
- License: CC0 (public domain) for maximum reuse

**Versioning:**
- Git + Git-LFS for large files
- Semantic versioning (v1.0, v1.1, etc.)
- SHA-256 manifests for integrity verification

---

## Acknowledgments

This work emerged through collaborative synthesis between David Lowe and multiple AI language models (Claude from Anthropic, ChatGPT from OpenAI, Gemini from Google).

**David Lowe** originated the Logos framework, theological insights, and overall research direction.

**AI Partners** contributed formalization of mathematical structures, experimental design, methodological refinements, and technical documentation.

The collaborative process itself demonstrates the participatory nature of knowledge creation that the framework proposes.

We thank early reviewers and critics whose skepticism strengthened the design. We thank potential collaborators for considering this unconventional program. We thank funding agencies for supporting high-risk research.

---

## Author Contributions

**Conceptualization:** David Lowe  
**Methodology:** David Lowe, ChatGPT, Claude  
**Formal Analysis:** ChatGPT  
**Investigation:** [To be completed during data collection]  
**Resources:** David Lowe  
**Data Curation:** [To be assigned]  
**Writing - Original Draft:** David Lowe, ChatGPT, Claude, Gemini  
**Writing - Review & Editing:** David Lowe  
**Visualization:** Claude (Anthropic)  
**Supervision:** David Lowe  
**Funding Acquisition:** David Lowe  

---

## Competing Interests

The authors declare no competing financial interests. David Lowe has a theoretical commitment to the Logos framework, which is addressed through adversarial collaboration, pre-registration, and commitment to publish null results.

---

## Data Availability Statement

Upon publication, all data and code will be made publicly available through:
- GitHub repository (MIT license for code)
- Zenodo archive (CC0 for data, permanent DOI)
- OSF project page (pre-registration and protocols)

Interim access during peer review available to qualified researchers upon request.

---

## References

[To be completed with full citations for:]
- Wheeler's participatory universe
- Landauer's principle
- Algorithmic information theory (Kolmogorov, Chaitin)
- Global Consciousness Project studies
- PEAR laboratory work
- Quantum foundations literature
- Bayesian methodology references

---

**Document Version:** 1.0 - COMPLETE FINAL  
**Status:** ✅ READY FOR SUBMISSION  
**Next Step:** Pre-register on OSF, submit to journal  

**Date:** October 7, 2025  

---

*"In the beginning was the Word, and the Word was with God, and the Word was God."*  
— John 1:1

*Does the Word couple to the world?*  
**This experiment will measure and see.**

---

**END OF REGISTERED REPORT**


