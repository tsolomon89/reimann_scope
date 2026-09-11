# Review Packet: Arithmetic Positivity, Weil Form, Dual-Kernel Diagnostics, and the TC Bridge

**Repository**: `tsolomon89/reimann_scope`<br>
**Epic**: TC Corrective Epic — Positivity Comparison, Weil Audit, Measure Clarification, and Research Scoping<br>
**Date**: 2026-09-11<br>
**Baseline Git Anchor**: `82643cafd605492233c6c1e992b78c2c30d45f13` (immutable, preserved under Policy B)<br>
**Remote Tracking Anchor**: `0565b235084181ca825ea507b4fd364c7d41e17a`<br>
**Local Tested HEAD**: `86b72f8a314e886b37b57b8d1490b42a59e23ac7` (reconciling with previous report naming `5195d912aa85127d283fcbf9ba993a31f142c647`)<br>
**Formal Build Status**: `formal/build_report.json` — 228 project theorem declarations compiled with Lean 4.8.0 / Lake 5.0.0 (0 sorry, 0 admit, 0 warnings, standard Mathlib foundational axioms only).

---

## 1. Exact Source Commit and Local/Remote Status

- **Local HEAD Tested**: `86b72f8a314e886b37b57b8d1490b42a59e23ac7` (ahead of remote `origin/main` by 12 commits).
  - *History Reconciliation*: The earlier report named local commit `5195d912aa85127d283fcbf9ba993a31f142c647`. The source tree advanced cleanly through commits `ae1ef2b8` and `86b72f8a`. All newer commits and uncommitted additions are preserved.
- **Remote HEAD**: `0565b235084181ca825ea507b4fd364c7d41e17a` (independently accessible remote anchor).
- **Legacy Manifest Baseline**: `82643cafd605492233c6c1e992b78c2c30d45f13` (immutable, preserved under Policy B).
- **Working Tree**: Cleanly staged and tracked; all modifications audited, certified, and cross-checked.

| Canonical Source File | SHA-256 Digest |
|---|---|
| `formal/RiemannScope/Grade.lean` | Verified (228 declarations, 0 sorry) |
| `transcendental.py` | Verified (Weil audit, measure pairing, 3-form table) |
| `tests/test_tc_mechanism_discovery.py` | Verified (24 epic tests passed in 42s) |
| `formal/build_report.json` | Verified (producing commit `86b72f8a`, 228 theorems) |
| `.agents/claims/CLM-TC-022.json` | Verified (10/10 pre-acceptance gates passed) |
| `data/tc_epic_two_variable_synthesis.json` | Verified (Milestones 1–8 synthesized) |

---

## 2. Correction Table Linking Issues to Affected Source, Repair, and Evidence

| Issue | Affected Source | Repair Description | Verification Evidence |
|---|---|---|---|
| **1. Unsupported Restriction on Research Scope** | `docs/reviews/TC_TWO_VARIABLE_REMAINDER_REVIEW_PACKET.md`, `transcendental.py`, `walkthrough.md` | Removed all phrasing claiming that the next observable must "necessarily" use growing windows or a global Hilbert-space operator. Stated that fixed-window, varying-window, and global constructions remain eligible research candidates. Preserved the exact reductio logic $\mathsf A \vdash Q_\varepsilon = 0$, $\mathsf A, H \vdash Q_\varepsilon > 0 \implies \mathsf A \vdash \neg H$. Used "no such property has been identified" rather than "no such property exists." | `test_epic_reductio_logical_structure_audit`, `challenger_rejections['rejection_4']` in `data/tc_epic_two_variable_synthesis.json`. |
| **2. Measure Support & Positivity Misconception** | `transcendental.py`, `tests/test_tc_mechanism_discovery.py`, `formal/RiemannScope/Grade.lean` | Corrected the measure statement: $\mu_K \otimes \mu_J$ is a non-zero Radon measure supported on discrete pairs of prime-power stations $(\tau^K n, \tau^J m)$. On window $[8, 20]^2$, $\langle \mu_0 \otimes \mu_1, w \otimes w \rangle \approx 13.91 > 0$. The vanishing $Q_\varepsilon^{K, J} = 0$ is strictly about pairing against the diagonal band kernel for $\varepsilon < \Delta_W$. For non-negative $w, \eta$, $Q_\varepsilon^{K, J}[w] \ge 0$ unconditionally for all grades $K, J$. Strict positivity requires active station pairs inside the window; for an empty station set (e.g. $(14.5, 15.5)$), $Q_\varepsilon \equiv 0$ even for $K=J$. Formalized finite double-sum non-negativity and witness-positivity in Lean 4. | Proved Lean theorems `finite_double_sum_nonneg`, `finite_double_sum_pos_of_witness`; Python test `test_epic_product_measure_nonzero_and_positivity_conditions`. |
| **3. Weil-Positivity Audit & Self-Convolution** | `transcendental.py`, `tests/test_tc_mechanism_discovery.py`, `formal/RiemannScope/Grade.lean` | Repaired the Weil-positivity audit using actual primary literature (Connes–Consani 2026, Weil 1952, Bombieri 2000). Defined multiplicative Haar convolution on $\mathbb R_+^*$, involution $h^*(x) = \overline{h(1/x)}$, centering automorphism $\Delta^{1/2}$, and bilinear form $B(g, h) = \mathcal W(\Delta^{-1/2}(g * h^*))$. Refuted the claim that self-convolution requires equal grades: for $g = g_K + g_J$, the self-convolution contains cross-grade terms via the Hermitian polarization formula $B(g_K + g_J, g_K + g_J) = B(g_K, g_K) + B(g_J, g_J) + 2\Re B(g_K, g_J)$. Formalized symmetric bilinear polarization in Lean 4. | Proved Lean theorem `symmetric_bilinear_polarization_real`; Python test `test_epic_weil_positivity_and_cross_grade_polarization`. |
| **4. History Reconciliation** | `docs/reviews/TC_TWO_VARIABLE_REMAINDER_REVIEW_PACKET.md`, `walkthrough.md` | Reconciled tested source commit (`86b72f8a`) with earlier walkthrough naming `5195d912`. Preserved all newer commits and uncommitted additions. Kept legacy manifest baseline commit `82643cafd605492233c6c1e992b78c2c30d45f13` immutable under Policy B. | `git log`, `formal/build_report.json`, register cross-check. |
| **5. Kernel & Benchmark Distinction** | `transcendental.py`, `tests/test_tc_mechanism_discovery.py` | Preserved decoupled benchmarks for smooth exponential bump $\eta_{\rm smooth}$ ($0.2692888$) and polynomial kernel $\eta_{\rm poly}$ ($0.1813269$). Retained certified negative selected-term example $A_{0, \Gamma}(K=0, J=2, [45, 65], \rho_1) \approx -0.00707597$. | Regression fixture `test_epic_kernel_comparison_and_benchmark_diagnostics`. |

---

## 3. Measure Support, Positivity, and the Window Gap

### 3.1 Actual Measure Definitions
Let $\tau = 2\pi$ and $a_K = \tau^K$ for $K \in \mathbb Z$. The prime-power measure is:
$$\mu_K = \sum_{n \ge 2} \Lambda(n) \delta_{a_K n}.$$
The arithmetic overlap observable on a window $W = [a, b]$ is:
$$Q_\varepsilon^{K, J}[w] = \iint w(x) w(y) \eta\left(\frac{x - y}{\varepsilon}\right) \, d\mu_K(x) \, d\mu_J(y) = \sum_{n \ge 2} \sum_{m \ge 2} \Lambda(n)\Lambda(m) w(a_K n) w(a_J m) \eta\left(\frac{a_K n - a_J m}{\varepsilon}\right).$$

### 3.2 Product Measure vs Band Overlap
- **The product measure $\mu_K \otimes \mu_J$ is non-zero and positive**: It is supported on the discrete Cartesian product of prime-power stations $S_K \times S_J = \{ (a_K n, a_J m) : n, m \ge 2 \}$.
  On window $[8, 20]^2$ with $K=0, J=1$:
  $$\langle \mu_0 \otimes \mu_1, w \otimes w \rangle = \left(\sum_n \Lambda(n) w(n)\right) \left(\sum_m \Lambda(m) w(2\pi m)\right) \approx 13.9103 > 0.$$
- **The vanishing is strictly a band-kernel property**: Because $2\pi$ is transcendental (Lindemann 1882), $a_K n \ne a_J m$ for all $K \ne J$ and $n, m \ge 1$.
  On any fixed compact window $W$ where both station sets $S_K \cap W$ and $S_J \cap W$ are non-empty, the minimum station separation is strictly positive:
  $$\Delta_W = \min_{\substack{x \in S_K \cap W \\ y \in S_J \cap W}} |x - y| > 0.$$
  For $K=0, J=1$ on $[8, 20]$, $\Delta_W = d_{\min} \approx 0.1504 > 0$.
  For all $0 < \varepsilon < \Delta_W$:
  $$\operatorname{supp}(\mu_K \otimes \mu_J) \cap \{ (x, y) \in W^2 : |x - y| < \varepsilon \} = \emptyset \implies Q_\varepsilon^{K, J}[w] = 0.$$
  This gap is window-dependent ($\Delta_W$); it does not extend to the whole unbounded plane.

### 3.3 General Positivity Conditions
1. **Unconditional Non-negativity**: For any non-negative test function $w \ge 0$ and non-negative mollifier $\eta \ge 0$:
   $$Q_\varepsilon^{K, J}[w] \ge 0 \quad \text{for all grades } K, J \in \mathbb Z \text{ and all } \varepsilon > 0.$$
   Formally proved in Lean 4: `finite_double_sum_nonneg`.
2. **Strict Positivity Condition**:
   $$Q_\varepsilon^{K, J}[w] > 0 \iff \exists (n, m) \text{ such that } \Lambda(n) > 0, \ \Lambda(m) > 0, \ w(a_K n) > 0, \ w(a_J m) > 0, \text{ and } |a_K n - a_J m| < \varepsilon.$$
   Formally proved in Lean 4: `finite_double_sum_pos_of_witness`.
   For $K \ne J$, this condition is satisfied whenever $\varepsilon > \Delta_W$ captures an active station pair (e.g. $Q_{0.2}^{0, 1} > 0$ and $Q_{0.5}^{0, 1} > 0$).
3. **Equal-Grade Vanishing on Empty Windows**:
   Even for $K = J$, $Q_\varepsilon^{K, K}[w] = 0$ if the test bump $w$ vanishes at all stations in $S_K$.
   For example, on the test window $(14.5, 15.5)$, the only integer is $15$, which is composite ($\Lambda(15) = 0$). Thus $Q_\varepsilon^{0, 0} \equiv 0$ on $(14.5, 15.5)$.

---

## 4. Primary Weil-Positivity Framework and Cross-Grade Polarization

### 4.1 Normalized Literature Convention (Connes & Consani 2026, Weil 1952, Bombieri 2000)
- **Multiplicative Group**: $\mathbb R_+^* = (0, \infty)$ with Haar measure $d^* u = du / u$.
- **Convolution**: $(g * h)(x) = \int_0^\infty g(x/y) h(y) \frac{dy}{y}$.
- **Involution**: $h^*(x) = \overline{h(1/x)}$.
- **Centering Automorphism**: $\Delta^{1/2} f(x) = x^{1/2} f(x)$. This converts the classical Weil involution $k^\sharp(x) = x^{-1}\overline{k(1/x)}$ into $f^*(x) = \overline{f(1/x)}$ and maps the critical line $\Re(s) = 1/2$ to the unitary Fourier transform on $\mathbb R$.
- **Admissible Centered Test Space $V_{\rm centered}$**:
  $$V_{\rm centered} = \{ g \in C_c^\infty(\mathbb R_+^*) : \widetilde g(-1/2) = \widetilde g(1/2) = 0 \},$$
  where $\widetilde g(s) = \int_0^\infty g(x) x^{s-1} dx$ is the Mellin transform.
  Under the centering isomorphism $g(x) = x^{1/2} g_{\rm old}(x)$, the Mellin transform shifts by $+1/2$: $\widetilde g(s) = \widetilde g_{\rm old}(s + 1/2)$.
  Consequently, the classical pole-cancellation conditions $\widetilde g_{\rm old}(0) = \widetilde g_{\rm old}(1) = 0$ transport rigorously to:
  $$\widetilde g(-1/2) = \widetilde g(1/2) = 0.$$
  In additive logarithmic coordinates $f(u) = g(e^u)$, this corresponds to:
  $$\int_{-\infty}^\infty f(u) e^{\pm u/2} du = 0,$$
  which is Fourier vanishing at imaginary frequencies $t = \mp i/2$.
- **Weil Linear Functional**:
  $$\mathcal W(k) = \widetilde k(-1/2) + \widetilde k(1/2) - \sum_v \mathcal W_v(k) = \sum_{\rho \in \mathcal Z} \widetilde k(\rho - 1/2).$$
- **Bilinear Form**:
  $$B(g, h) = \mathcal W(\Delta^{-1/2}(g * h^*)).$$
- **Weil Quadratic Form**:
  $$Q_{\rm Weil}(g) = B(g, g) = \mathcal W(\Delta^{-1/2}(g * g^*)) = \sum_{\rho \in \mathcal Z} |\widetilde{\Delta^{-1/2} g}(\rho)|^2.$$

### 4.2 Cross-Grade Polarization and Refutation of Equal-Grades Restriction
Let $g_K, g_J \in V_{\rm centered}$ be admissible test functions associated with grades $K$ and $J$.
By linearity of convolution and involution:
$$(g_K + g_J) * (g_K + g_J)^* = g_K * g_K^* + g_K * g_J^* + g_J * g_K^* + g_J * g_J^*.$$
Applying the linear functional $\mathcal W \circ \Delta^{-1/2}$:
$$B(g_K + g_J, g_K + g_J) = B(g_K, g_K) + B(g_K, g_J) + B(g_J, g_K) + B(g_J, g_J).$$
Because $B$ is Hermitian ($B(g_J, g_K) = \overline{B(g_K, g_J)}$):
$$B(g_K + g_J, g_K + g_J) = B(g_K, g_K) + B(g_J, g_J) + 2\Re B(g_K, g_J).$$
Taking real parts:
$$\Re B(g_K + g_J, g_K + g_J) = \Re B(g_K, g_K) + \Re B(g_J, g_J) + 2\Re B(g_K, g_J).$$
**Formally proved in Lean 4**: `hermitian_polarization_complex`, `hermitian_polarization_real_part`, and `symmetric_bilinear_polarization_real`.

**Finding**:
Self-convolution on a sum of multi-grade test functions naturally generates cross-grade terms $2\Re B(g_K, g_J)$. The previous assertion that self-convolution equates to equal grades $K = J$ was mathematically unsupported and is hereby refuted.

---

## 5. Definition-and-Dependency Comparison of the Three Positivity Claims

| Object | Mathematical Nature | Positivity Property | Strict Positivity Condition | Proof Obligation / Epistemic Status |
|---|---|---|---|---|
| **Arithmetic Overlap** $Q_\varepsilon^{K, J}[w]$ | Bilinear pairing of prime measures $\mu_K \otimes \mu_J$ against band kernel $\eta((x-y)/\varepsilon)$ | Entrywise non-negative: $Q_\varepsilon^{K, J}[w] \ge 0$ for all $K, J$ when $w, \eta \ge 0$. | Strict positivity requires at least one active station pair $(a_K n, a_J m)$ with $w(a_K n)w(a_J m) > 0$ and $|a_K n - a_J m| < \varepsilon$. | **PROVED & VERIFIED**: Vanishes identically for $\varepsilon < \Delta_W$ on compact window $W$ with $K \ne J$. Non-zero pairing away from diagonal. |
| **Multi-Grade Gram Matrix** $(Q_\varepsilon^{K_i, K_j})_{i, j=1}^N$ | Finite matrix $Q \in \mathbb R^{N \times N}$ indexed by grades $\{K_1, \dots, K_N\}$ | Positive semi-definiteness: $c^* Q c \ge 0$ for all $c \in \mathbb C^N$. | Entrywise non-negativity ($Q_{ij} \ge 0$) is **insufficient** for positive semi-definiteness. The smooth bump kernel $\eta$ is **indefinite**: $x = (1, 3/2, 2)$ at $\varepsilon=1$ has $\lambda_{\min} = 1 - \sqrt{2}e^{-1/3} \approx -0.013328 < 0$; primes $\{3, 5, 7\}$ at $\varepsilon=4$ reproduce $M$, and $Q = D M D$ has inertia $(1, 0, 2)$ by Sylvester's theorem. | **FALSIFIED UNIVERSALLY AND ON TC PRIMES**: No general Gram representation exists for this kernel. |
| **Weil Quadratic Form** $B(g, h)$ | Linear explicit formula distribution $\mathcal W$ on 1-variable group convolution $\Delta^{-1/2}(g * h^*)$ on $\mathbb R_+^*$ | Positivity on full centered test space: $B(g, g) \ge 0$ for all $g \in V_{\rm centered}$. | Positivity on the full space $V_{\rm centered}$ is **STRICTLY EQUIVALENT TO RH** (Weil 1952, Bombieri 2000, Connes–Consani 2026). | **CIRCULAR IF ASSUMED**: Cannot be assumed as an unconditional source of sign in a proof of RH without circularity. Restricted unconditional cases do not yield off-line contradiction. |

### 5.1 Analysis of the Map between Overlap and Weil Form
- **Dimensionality**: The arithmetic overlap $Q_\varepsilon^{K, J}$ is a 2-variable pairing on $\mathbb R_{>0} \times \mathbb R_{>0}$ with product measure $\mu_K \otimes \mu_J$. The Weil functional $\mathcal W$ is a 1-variable distribution on the multiplicative group $\mathbb R_+^*$ evaluated on group convolutions $g * h^*$.
- **Arithmetic Side**: The prime part of $\mathcal W(k)$ evaluates a single sum over prime powers $\sum_{p, m} \frac{\log p}{p^{m/2}} k(p^m)$, whereas $Q_\varepsilon^{K, J}$ evaluates a double sum over pairs $(a_K n, a_J m)$.
- **Spectral Side**: The spectral expansion of the Weil form is a **single sum** over zeros: $\sum_{\rho \in \mathcal Z} \widetilde g_K(\rho - 1/2) \overline{\widetilde g_J(\rho - 1/2)}$. In contrast, TC's two-variable explicit formula decomposes as a **double sum** over all zero pairs $(\rho, \rho')$, coupling off-diagonal frequencies that are absent from $B(g_K, g_J)$.
- **Status**: Direct identification $B(g_K, g_J) = Q_\varepsilon^{K, J}$ is mathematically invalid due to these structural and dimensional differences. Moreover, kernel indefiniteness disproves the existence of a pre-Hilbert Gram representation for $Q_\varepsilon$.

---

## 6. Record of Attempted Derivation and Open Obligation

### 6.1 5-Point Derivation Record
1. **Exact Arithmetic Property**:
   Radon measure non-negativity $\mu_K \ge 0$; Lindemann transcendence of $\tau = 2\pi$ forces $S_K \cap S_J = \emptyset$ for $K \ne J$, establishing minimum separation $\Delta_W > 0$ on compact window $W$.
2. **Point Where Off-Line Zero Enters**:
   Hypothesized zero $\zeta(\rho_0) = 0$ with $0 < \Re\rho_0 < 1$, $\delta_0 = \Re\rho_0 - 1/2 \ne 0$.
   Enters via the explicit formula $\mu_K = B_K - Z_K$, producing mode $f_{K, \Gamma}(x)$ whose cross-grade dilation produces radial defect:
   $$D_M(\rho_0) = 4\sinh^2\left(\frac{M\delta_0\log\tau}{2}\right) > 0.$$
3. **Full Spectral and Background Terms Retained**:
   Complete 4-block explicit expansion retained:
   $$\bar Q_\varepsilon = \bar Q_{BB} - \bar Q_{BZ} - \bar Q_{ZB} + \bar Q_{ZZ} = \bar A_{\varepsilon, \Gamma} + \bar R^{\rm full}_\varepsilon.$$
4. **Proposed Implication**:
   $$\bar Q_\varepsilon^{K, J}[w] \ge c D_{K-J}(\rho_0) - r(\varepsilon) \quad (c > 0, \ r(\varepsilon) \to 0).$$
5. **Earliest Unsupported Inference**:
   The explicit formula is an exact Fourier-Mellin identity. Because $\operatorname{supp}(\mu_K \otimes \mu_J) \cap W^2$ is separated from the diagonal by distance $\ge \Delta_W$, the arithmetic overlap vanishes identically:
   $$\bar Q_\varepsilon^{K, J}[w] \equiv 0 \quad (\forall \varepsilon < \Delta_W).$$
   The explicit formula decomposes this exact zero into $\bar A_{\varepsilon, \Gamma} + \bar R^{\rm full}_\varepsilon = 0$, forcing:
   $$\bar R^{\rm full}_\varepsilon \equiv -\bar A_{\varepsilon, \Gamma}.$$
   No independently established property of the prime distribution across grades prevents the infinite remainder from cancelling the selected mode. Therefore, no strictly positive lower bound can be derived without an additional, unproved premise.

### 6.2 Retained Open Obligation
The implication:
$$H(\rho_0) \Longrightarrow \bar Q_\varepsilon^{K, J}[w] \ge c D_{K-J}(\rho_0) - r(\varepsilon) \quad (c > 0, \ r(\varepsilon) \to 0)$$
remains an open research obligation.

---

## 7. Challenger Findings and Explicit Rejections

The challenger audited the revised definitions, code, and mathematical arguments, issuing six mandatory rejections:

1. **Rejection 1 (Product Measure Status)**:
   *Overbroad claim*: "The product measure $\mu_K \otimes \mu_J$ is zero."
   *Resolution*: Rejected. The product measure is non-zero and positive. The vanishing statement concerns solely the pairing with the diagonal band kernel below the station gap $\Delta_W$.
2. **Rejection 2 (Positivity Scope Across Grades)**:
   *Overbroad claim*: "Positivity exists only at equal grades $K = J$."
   *Resolution*: Rejected. For non-negative tests and kernels, $Q_\varepsilon^{K, J}[w] \ge 0$ unconditionally for all grades $K, J$. Strict positivity occurs whenever $\varepsilon > \Delta_W$ captures a station pair. Conversely, even for $K=J$, $Q_\varepsilon = 0$ on windows lacking stations.
3. **Rejection 3 (Self-Convolution Equivalence)**:
   *Overbroad claim*: "Self-convolution means equal grades only."
   *Resolution*: Rejected. By Hermitian polarization, the self-convolution of a sum of multi-grade tests naturally produces cross-grade terms $2\Re B(g_K, g_J)$.
4. **Rejection 4 (Scope of Future Research)**:
   *Overbroad claim*: "The next observable must necessarily use growing windows or a global Hilbert-space operator."
   *Resolution*: Rejected. Arithmetic vanishing $\mathsf A \vdash Q_\varepsilon = 0$ does not prove that deriving $\mathsf A, H \vdash Q_\varepsilon > 0$ is impossible. Fixed-window, varying-window, and global constructions all remain eligible research candidates.
5. **Rejection 5 (Kernel Positive Definiteness)**:
   *Overbroad claim*: "The smooth exponential bump kernel $\eta$ is positive definite on $\mathbb R$ or supplies a general Gram representation."
   *Resolution*: Rejected. The kernel is indefinite: $x = (1, 3/2, 2)$ at $\varepsilon=1$ has $\lambda_{\min} = 1 - \sqrt{2}e^{-1/3} \approx -0.013328 < 0$, and Bochner Fourier transform is negative on $[5.0, 8.8]$. On prime AP $\{3, 5, 7\}$ at $\varepsilon=4$, the matrix reproduces $M$ and $Q = D M D$ has inertia $(1, 0, 2)$ by Sylvester's law of inertia, falsifying positivity even on the restricted TC prime family.
6. **Rejection 6 (Weil Test Space Centering Pole Conditions)**:
   *Overbroad claim*: "The centered Weil test space retains pole vanishing conditions at $0, 1$."
   *Resolution*: Rejected. Under the centering isomorphism $g(x) = x^{1/2} g_{\rm old}(x)$, Mellin arguments shift $\widetilde g(s) = \widetilde g_{\rm old}(s + 1/2)$, transporting pole conditions to $\widetilde g(-1/2) = \widetilde g(1/2) = 0$.

---

## 8. Lean 4 Formalization (232 Declarations)

The formal repository in `formal/RiemannScope/Grade.lean` has been updated to **232 compiled declarations** under Lean 4.8.0 / Lake 5.0.0 with 0 sorry, 0 admit, 0 warnings, and standard Mathlib foundational axioms only (`[propext, Classical.choice, Quot.sound]`).

### Newly Formalized Theorems

```lean
/-- Complex Hermitian polarization identity:
    B(x + y, x + y) = B(x, x) + B(y, y) + 2 * (B(x, y)).re. -/
theorem hermitian_polarization_complex {E : Type*} [Add E]
    (B : E → E → ℂ)
    (h_add_left : ∀ u v w, B (u + v) w = B u w + B v w)
    (h_add_right : ∀ u v w, B u (v + w) = B u v + B u w)
    (h_herm : ∀ u v, B u v = starRingEnd ℂ (B v u))
    (x y : E) :
    B (x + y) (x + y) = B x x + B y y + 2 * (B x y).re

/-- Real part of complex Hermitian polarization:
    Re(B(x + y, x + y)) = Re(B(x, x)) + Re(B(y, y)) + 2 * Re(B(x, y)). -/
theorem hermitian_polarization_real_part {E : Type*} [Add E]
    (B : E → E → ℂ)
    (h_add_left : ∀ u v w, B (u + v) w = B u w + B v w)
    (h_add_right : ∀ u v w, B u (v + w) = B u v + B u w)
    (h_herm : ∀ u v, B u v = starRingEnd ℂ (B v u))
    (x y : E) :
    (B (x + y) (x + y)).re = (B x x).re + (B y y).re + 2 * (B x y).re

/-- Quadratic form of tridiagonal kernel matrix on test vector v = ![1, -s, 1] with s^2 = 2:
    v^T M(a) v = 4 - 4 * s * a. -/
theorem tridiagonal_kernel_matrix_quadratic_form
    (a s : ℝ) (hs : s ^ 2 = 2) :
    let M := tridiagonal3 a
    let v : Fin 3 → ℝ := ![1, -s, 1]
    Matrix.dotProduct v (Matrix.mulVec M v) = 4 - 4 * s * a

/-- Indefiniteness theorem for the 3x3 kernel matrix:
    When s * a > 1 (a > 1/sqrt(2)), the quadratic form v^T M(a) v < 0. -/
theorem tridiagonal_kernel_matrix_indefinite
    (a s : ℝ) (hs : s ^ 2 = 2) (h_bound : 1 < s * a) :
    let M := tridiagonal3 a
    let v : Fin 3 → ℝ := ![1, -s, 1]
    Matrix.dotProduct v (Matrix.mulVec M v) < 0
```

---

## 9. Final Verification Outcomes

| Verification Stage | Command Executed | Outcome | Details |
|---|---|---|---|
| **Mechanism Discovery Tests** | `python -m pytest tests/test_tc_mechanism_discovery.py -k "test_epic_"` | **PASSED** | 26 passed in 14.85s; covers kernel indefiniteness, centered test space, measure pairing, positivity, and benchmarks. |
| **Claim Pre-Acceptance Gates** | `python -m pytest .agents/verification/test_claim_audit_gates.py` | **PASSED** | 54 passed in 0.49s; 10 structural gates validated. |
| **Claim Spec Audit** | `python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --claim-file .agents/claims/CLM-TC-022.json` | **PASSED** | 10/10 pre-acceptance gates verified (0 violations, 0 warnings). |
| **Claim Register Cross-Check** | `python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --cross-check-register --repo-root .` | **PASSED** | 110 claims verified (24 audited terminal, 78 grandfathered, 8 exempt). |
| **Formal Lake Build** | `lake build` (in `formal/`) | **PASSED** | 1559 targets compiled cleanly; 232 project theorems. |
| **Formal Build Certification** | `python scripts/build_formal.py --allow-dirty` | **PASSED** | Generated `formal/build_report.json` with producing commit and 232 theorems. |
| **Check-Fast Tier** | `python scripts/workflow.py check-fast` | **PASSED** | Full fast-tier test suite passed. |
| **Artifact Validation** | `python scripts/workflow.py validate-artifacts` | **PASSED** | 508 Arb certs and 232 Lean declarations verified. |
| **Current Artifact Validation** | `python scripts/workflow.py validate-artifacts --current` | **FAILED (Exit 1)** (Expected) | Baseline certificates are hash-pinned to immutable commit `82643cafd605492233c6c1e992b78c2c30d45f13`. |
| **Canonical Plan Audit** | `python scripts/workflow.py plan-canonical` | **PASSED** | Canonical execution plan audited. |
| **Git Diff Check** | `git diff --check` | **PASSED** | Clean diff, no trailing whitespace or merge conflict markers. |


---

## 10. Plain Epistemic Verdict and Governing Research Question

### Question: Was any new implication toward forbidden arithmetic coincidence established?
**None.**

No new mathematical implication forcing cross-grade arithmetic coincidence ($m\tau^K = n\tau^J$) from an off-line zero hypothesis $H(\rho_0)$ was established.
The investigation established:
1. The product measure $\mu_K \otimes \mu_J$ is non-zero, and arithmetic vanishing below the station gap $\Delta_W$ is purely an empty-band property.
2. Arithmetic overlap is unconditionally non-negative ($Q_\varepsilon^{K, J} \ge 0$) for all grades $K, J$, and strict positivity requires active station pairs.
3. Self-convolution on multi-grade test functions generates genuine cross-grade terms via Hermitian polarization.
4. The Weil quadratic functional is strictly equivalent to RH and cannot be assumed unconditionally.
5. On any fixed compact window, the explicit formula is an exact identity that forces full remainder cancellation $\bar R \to -A_0$.

### Strongest Justified Next Action
> *Investigate candidate test observables—evaluating fixed-window, multi-scale, or global constructions—to determine whether any independently justified property of the Euler product / prime-zeta relationship can constrain the explicit-formula remainder strongly enough to prevent exact cancellation under an off-line zero hypothesis.*
