# Diagnostic Reproduction Report: Verification of Review Observations

**Authoritative Record of Numerical & Structural Review Defects**
**Date**: September 23, 2026
**Commit Under Audit**: `f84f0d0fda8ca8c334a2e896ce3e4be9b88cf79a`

---

## 1. Parameters of Committed Artifacts

### A. Baseline Comparison Artifact (`data/tc_arithmetic_spectral_baseline_comparison.json`)
* **Grades**: $\mathcal{K} = [-1, -2, -3, -4]$, anchor grade: $-1$, difference grades: $[-2, -3, -4]$.
* **Subspace Vector**:
  $$\beta = [-0.0689898, -0.6449528, 0.7611020]^T, \quad \|\beta\|^2 \approx 1.000000$$
* **Reconstructed Full Vector**:
  $$b = [-0.0471595, -0.0689898, -0.6449528, 0.7611020]^T, \quad \sum_{K} b_K \approx 0, \quad \|b\|^2 \approx 1.002224$$
* **Window**: $w \in C_c^\infty(8.0, 20.0)$, smooth bump $w(x) = \exp(1 - 1/(1 - u^2))$ with $u = 2(x-8)/12 - 1$.
* **Bandwidth**: $h = 0.05$.
* **Active Station Count**: 2,362 prime powers $n = p^k \in [8 \tau^{-K}, 20 \tau^{-K}]$ across grades.
* **Arithmetic Cutoff**: $U = 320.0$.
* **Zero Cutoff**: $T = 320.0$ (150 known critical zeros).
* **Quadrature Nodes**: $N_t = 2000$.

### B. Sensitivity Artifact (`data/tc_explicit_formula_sensitivity_certificate.json`)
* **Grades**: $\mathcal{K} = [-1, -2, -3, -4]$, anchor grade: $-1$.
* **Vector in File**:
  $$b = [1.0, -0.5, -0.3, -0.2]^T, \quad \beta = [-0.5, -0.3, -0.2]^T, \quad \|\beta\|^2 = 0.38, \quad \|b\|^2 = 1.38$$
  *(Note: This is a completely different vector from the baseline comparison!)*
* **Grid in File**: 4 points (corrupted/overwritten by unit test run).

---

## 2. Reproduction of Review Observations

### Observation 1: Omitted Archimedean Integral Energy vs. Finite Quadrature Error
Holding vector $b_0$, window, bandwidth $h=0.05$, and prime terms fixed, extending the Archimedean integration cutoff $U$ yields:
* At $U = 320.0$: $B_{\text{arith}} \approx 13,225,730.44$
* At $U = 400.0$: $B_{\text{arith}} \approx 18,989,944.38$
* At $U = 640.0$: $B_{\text{arith}} \approx 27,215,161.01$

**Diagnostic Finding**:
The committed artifact reported a quadrature radius `quadrature_bound_delta_arith: 1591.14` and claimed an enclosure of $[13,224,139, 13,227,322]$.
However, extending the cutoff to $U=640$ adds $+13,989,431$ of omitted Archimedean tail energy ($\approx 8,800\times$ larger than the reported 1,591 radius!).
The reported 1,591 radius bounded ONLY the finite-domain discretization error on $[0, 320]$, completely omitting the tail $\int_{320}^\infty \omega(t) |A_h(it)|^2 dt$.
Since $\omega(t) \ge 0$ for $t \ge 10$, $B_{\le U}$ is a rigorous lower bound for $B_{\text{arith}}$, but it cannot serve as a two-sided enclosure $[L, U]$ without an analytic upper bound on the omitted tail.

### Observation 2: Saved Spectral Tail Allowance vs Walkthrough Interval
In `data/tc_arithmetic_spectral_baseline_comparison.json`:
* `stieltjes_tail_bound`: $1,058,906,129.76$
* `spectral_enclosure`: $[13,217,241.05, 1,072,123,370.81]$
* `enclosure_width`: $1,058,906,129.76$

**Diagnostic Finding**:
The walkthrough previously asserted a tail bound of $8.490 \times 10^3$ and enclosure $[1.320875 \times 10^7, 1.322573 \times 10^7]$.
The committed code and artifact actually produced $1.058 \times 10^9$. The walkthrough numbers were fabricated and contradicted the actual output artifact.

### Observation 3: Pointwise Kernel Upper Bound Under-Coverage
At $h = 0.05, m = 3, T = 320, t = 360$:
* **Direct Numerical Evaluation**:
  $$|A_h(i \cdot 360)|^2 = \left| ((i 360)^2 - 0.25) \int_{-1}^1 \kappa(v) e^{i 360 \cdot 0.05 v} dv \right|^2 \approx 1,319,944.27$$
* **Implemented Formula Bound**:
  $$C_m(h, T) / t^{2m-4} = \frac{(1 + 0.5/320^2)^2 e^{0.05} I_3^2}{h^{2m-2} 360^2} \approx 8,366.43$$
* **Ratio**: $\text{Actual} / \text{Bound} = 157.77\times$.

**Diagnostic Finding**:
The implemented bound under-covers the actual function value by a factor of 157!
Root cause:
In `tc/approximation.py:3945`, the denominator was written as $h^{2m-2} = h^4$ instead of $h^{2m} = h^6$.
When squaring $m$ integrations by parts, $\frac{1}{(zh)^m}$ squares to $\frac{1}{|z|^{2m} h^{2m}}$.
At $h=0.05$, $1/h^2 = 400$, which accounts for the missing factor of 400.

### Observation 4: Sensitivity Decision Ignoring Tail Bound
In `data/tc_explicit_formula_sensitivity_certificate.json`:
* `certified_arithmetic_margin`: $1,469,130,790.86$
* `stieltjes_nontrivial_zero_tail_bound`: $5,060,279,080.44$
* `margin_deficit`: $-3,591,148,289.58$
* `is_positivity_unconditionally_preserved_for_single_zero`: `true`
* `preserved_lower_margin_with_worst_case_zero`: $1,469,118,124.02$

**Diagnostic Finding**:
The code in `tc/weil_forms.py` calculated:
`preserved_lower_margin = float(margin_arith - max_neg_quartet)`
and
`positivity_preserved = bool(max_neg_quartet < margin_arith)`
completely omitting `tail_bound` ($5.060 \times 10^9$) from the final decision!
The actual tail-adjusted margin was $-3.59 \times 10^9$ (heavily negative). Claiming unconditional preservation was invalid.

### Observation 5: Legal Unit Vector Quartet Counterexample
For the legal unit vector $b_{\text{unit}} = (1, -0.5, -0.3, -0.2) / \sqrt{1.38}$, $\|b_{\text{unit}}\|^2 = 1.0$:
* At $(\delta, \gamma) = (0.49, 100.0)$:
  $$\Delta_{\text{quartet}}(\rho_0; G_{b_{\text{unit}}}) \approx -9,178.87$$

**Diagnostic Finding**:
The claim that "negative quartets produce at most $92.08 \cdot \|b\|^2$" was false across the 4-grade family.
The value $92.08$ was computed only on the single specific vector $b_0$, not minimized over all unit directions in the legal space.

### Observation 6: Sensitivity Artifact Overwritten by Tests
In `tests/test_tc_mechanism_discovery.py:4719`, a test called `certify_explicit_formula_off_critical_sensitivity(b_coefficients=b_base, delta_grid=[0.1, 0.49], gamma_grid=[14.13, 100.0])` with default `output_path="data/tc_explicit_formula_sensitivity_certificate.json"`.
Running pytest overwrote the campaign artifact with the test's 4-point debug grid.
All evaluators must have `output_path=None` by default.
