---
uuid: 020d3698-a857-526d-b8de-b3b48bdbaee3
title: 'Paper 11: Pre-Registration Specifications'
author: David Lowe
type: paper
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: Logos zright\Papers\07_Experimental_Protocols\PAPER-11-PRE-REGISTRATION-SPECS.md
uuid_generated_at: '2025-11-22T01:23:51.208987'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# Paper 11: Pre-Registration Specifications

**Insert these detailed specifications into each protocol in Paper 11**

---

## Protocol 1: The Dorothy Protocol - PRE-REGISTRATION DETAILS

### **Primary Endpoint**
Change in interference pattern visibility (V) correlated with observer coherence index (OCI).

**Formula:**
```
V = (I_max - I_min)/(I_max + I_min)
Where I_max, I_min = intensity at maxima and minima
```

### **Effect Size Target**
- **Minimum detectable effect:** Cohen's d ≥ 0.4 (medium effect)
- **Expected correlation:** r ≥ 0.35 between OCI and ΔV

### **Statistical Design**
- **α (significance level):** 0.01 (two-tailed)
- **β (Type II error):** 0.20 (80% power)
- **Sample size:** N = 85 participants (calculated via G*Power)
- **Replications:** 10 independent labs
- **Final threshold:** 6-sigma cumulative (z ≥ 6.0, p < 10⁻⁹)

### **Observer Coherence Index (OCI)**
Composite measure from physiological proxies:
- **EEG coherence:** Alpha band (8-12 Hz) inter-hemispheric coherence
- **HRV coherence:** Heart rate variability LF/HF ratio
- **Formula:** OCI = 0.6·C_EEG + 0.4·C_HRV (normalized [0,1])

### **Analysis Plan**
1. **Primary:** Pearson correlation between OCI and ΔV
2. **Secondary:** Mixed-effects regression (participant as random effect)
3. **No optional stopping:** Data collection continues to N=85 regardless of interim results
4. **One-tailed:** Prediction is directional (positive correlation)

### **Exclusion Criteria (Pre-Specified)**
- OCI < 0.2 (participant not engaged)
- Technical malfunction (>5% photon loss)
- Participant reports external distraction during trial

### **Negative Control**
- **Sham intervention:** Participants told to "intend" but listen to white noise (disrupts coherence)
- **Prediction:** Sham condition shows r ≈ 0

### **Stop/Go Table**

| Outcome | Interpretation | Action |
|---------|---------------|--------|
| \|z\| ≥ 6.0, p < 10⁻⁹ | Strong evidence for framework | Publish, replicate |
| 3.0 ≤ \|z\| < 6.0 | Suggestive but inconclusive | Increase N, re-test |
| \|z\| < 2.5 | No effect detected | **Reject claim**, publish null |

---

## Protocol 2: APCT - PRE-REGISTRATION DETAILS

### **Primary Endpoint**
Difference in Shannon entropy (H) between QRNG outputs under low-K vs high-K seed conditions.

**Formula:**
```
H = -Σ p(x) log₂ p(x)
Where p(x) = probability of bit sequence x
```

### **Effect Size Target**
- **Minimum detectable:** ΔH ≥ 0.15 bits per byte
- **Expected reduction:** H_lowK < H_highK by ≥ 10%

### **Statistical Design**
- **α:** 0.01 (two-tailed)
- **Power:** 85%
- **Sample size:** 1,000 blocks per condition (2,000 total)
- **Block length:** 10,000 bits each
- **Threshold:** 5-sigma (z ≥ 5.0, p < 10⁻⁶)

### **Seed Conditions**
**Low-K (ordered):**
- Gospel of John (English text)
- Gregorian chant recording (spectral data)
- Fibonacci sequence
- **K(seed):** < 100 bits (highly compressible)

**High-K (random):**
- Cryptographic white noise
- Atmospheric noise recording
- True random number stream
- **K(seed):** ≈ length (incompressible)

### **Analysis Plan**
1. **Primary:** Two-sample t-test on mean H per condition
2. **Secondary:** Kolmogorov-Smirnov test on bit distributions
3. **Tertiary:** Runs test for randomness
4. **Blinding:** Operator does not know which seed is which (automated randomization)

### **Exclusion Criteria**
- QRNG failure rate >1%
- Seed file corruption
- Environmental EM interference detected

### **Negative Controls**
- **Neutral seed:** Mathematical constant (π digits) - should show intermediate H
- **Sham low-K:** Random data mislabeled as "ordered" - should show H_high

### **Stop/Go Table**

| Outcome | Interpretation | Action |
|---------|---------------|--------|
| z ≥ 5.0, ΔH ≥ 0.15 bits | Logos bias confirmed | Publish, mechanism study |
| 2.5 ≤ z < 5.0 | Weak signal | Triple sample size |
| z < 2.5 | No Logos bias | **Reject APCT claim** |
| z < -2.5 | Reverse effect! | Investigate confound |

---

## Protocol 3: Temporal Decoherence Delay - PRE-REGISTRATION DETAILS

### **Primary Endpoint**
Change in coherence lifetime (τ) of entangled photon pairs with vs without focused observer.

**Measure:**
```
τ = time for visibility to decay to 1/e of initial value
V(t) = V₀·e^(-t/τ)
```

### **Effect Size Target**
- **Minimum detectable:** Cohen's d ≥ 0.5 (medium-large effect)
- **Expected increase:** Δτ ≥ 15% in observed condition

### **Statistical Design**
- **α:** 0.01 (two-tailed)
- **Power:** 90%
- **Sample size:** N_systems = 200 per condition
- **Observer sessions:** N_obs = 50 independent observers
- **Threshold:** 5-sigma (z ≥ 5.0, p < 10⁻⁶)

### **Conditions**
1. **Focused observer:** Trained meditator focuses intent on "preserving coherence"
2. **Control:** No observer present (automated measurement only)
3. **Sham observer:** Observer present but engaged in unrelated cognitive task

### **Analysis Plan**
1. **Primary:** Paired t-test (observed vs control τ)
2. **Secondary:** ANOVA across all 3 conditions
3. **Covariate:** Observer coherence (EEG α-power during session)
4. **Blinding:** Observer does not know when measurement is active

### **Exclusion Criteria**
- System visibility V₀ < 0.85 (poor initial entanglement)
- Environmental decoherence spike (τ_background < 50% of baseline)
- Observer reports inability to maintain focus

### **Negative Controls**
- **Dead system:** Pre-decohered photons (should show τ ≈ 0 regardless)
- **Automated "observer":** Computer program "intending" preservation (should match control)

### **Stop/Go Table**

| Outcome | Interpretation | Action |
|---------|---------------|--------|
| z ≥ 5.0, d ≥ 0.5 | Observer effect real | Publish, replicate |
| 3.0 ≤ z < 5.0 | Possible signal | Add N=100, re-test |
| \|z\| < 2.5 | No observer effect | **Reject Protocol 3 claim** |

---

## Universal Pre-Registration Commitments

### **Data Management**
- **Escrow:** Raw data sent to adversarial collaborator before analysis
- **Open access:** All data published regardless of outcome
- **No cherry-picking:** Report all pre-specified analyses

### **Adversarial Team**
- Minimum 1 skeptical physicist + 1 skeptical statistician
- Full veto power over protocol design
- Co-authorship on null results

### **Stopping Rules**
- **No optional stopping:** Complete pre-specified N before looking at results
- **Interim analyses:** Only if pre-registered with Bonferroni correction
- **Publication commitment:** Publish null results with equal rigor

### **Replication Plan**
- All protocols registered on OSF (Open Science Framework)
- Materials, code, and protocols publicly available
- Encourage independent replication with adversarial teams

---

## Master Falsification Table

| Framework Claim | Test Protocol | Disconfirmer | Decision Rule |
|-----------------|---------------|--------------|---------------|
| Intent biases collapse | Dorothy | \|z\| < 2.5 across all sites | Withdraw claim, publish null |
| Logos favors low-K info | APCT | ΔH ≤ 0 or within noise | Reject APCT hypothesis |
| Observation extends coherence | Temporal | d < 0.3, p > 0.05 | Withdraw Protocol 3 |
| Scripture has low K | Text analysis | K(Bible) ≥ K(controls) | Re-evaluate consilience claim |
| Prayer reduces QRNG H | Field study | Bayes Factor < 3 | Treat as inconclusive |

**No equivocation. Pre-specified. Falsifiable.**

---

**Insert these specifications into Paper 11 to transform it from concept to pre-registered, publication-ready protocol.**


