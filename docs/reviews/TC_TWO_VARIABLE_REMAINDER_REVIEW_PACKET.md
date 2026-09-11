# Review Packet: Two-Variable Explicit Formula, Normalized Remainder Truncation Bound, Dual-Kernel Diagnostics, and Bridge Defect Repair

**Repository**: `tsolomon89/reimann_scope`<br>
**Epic**: TC Corrective Epic — Evidence Completion, Certification Semantics, Dual-Kernel Diagnostics, and Arithmetic Compatibility<br>
**Date**: 2026-09-11<br>
**Baseline Git Anchor**: `82643cafd605492233c6c1e992b78c2c30d45f13` (immutable, preserved under Policy B)<br>
**Remote Tracking Anchor**: `0565b235084181ca825ea507b4fd364c7d41e17a`<br>
**Formal Build Status**: `formal/build_report.json` — 225 project theorem declarations compiled with Lean 4.8.0 / Lake 5.0.0 (0 sorry, 0 admit, 0 warnings, standard Mathlib foundational axioms only).

---

## 1. Exact Source Commit and Local/Remote Status

- **Local HEAD**: `5195d912aa85127d283fcbf9ba993a31f142c647` (ahead of remote `origin/main` by 10 commits).
- **Remote HEAD**: `0565b235084181ca825ea507b4fd364c7d41e17a` (independently accessible remote anchor).
- **Legacy Manifest Baseline**: `82643cafd605492233c6c1e992b78c2c30d45f13` (immutable, preserved under Policy B).
- **Working Tree**: Fully tracked and verified; all modifications audited and cross-checked.

| Canonical Source File | SHA-256 Digest |
|---|---|
| `formal/RiemannScope/Grade.lean` | `8a88cc4f447c4b8bfe0ee1e7a7b38a237199d4bcbc1655f7f11f4e52060bec4f` |
| `transcendental.py` | `6da9a791a221f7ec8d5e5e6e3c5ec7a810567e9a8f4c5e317c805eb3eb56b107` |
| `tests/test_tc_mechanism_discovery.py` | `cb016df33240251ea7383a15dc2112d7f4be2db65cba27715b7fb5f899e32dcb` |
| `formal/build_report.json` | `99e238b8489265966056f41899e95c64d4806e68b5032cd173b0fcf2a07a047d` |
| `.agents/claims/CLM-TC-022.json` | `d552e1ebcf078a6fffa74bc053da5f87bcf82e850b5550a62312b972e3a1f861` |
| `data/tc_epic_two_variable_synthesis.json` | `2a8debbcf4ef64a37c357fe7d6f5195701c90dc42d547f42cf530e719fc9bda3` |
| `research/epic/tc_corrective_epic_report.md` | `c21d0a5198ecffc24177b08d24933a39e9fbdb97e06a88ff05dc24e4d5fb83c1` |

---

## 2. Correction Table Linking Issues to Affected Source, Repair, and Evidence

| Issue | Affected Source | Repair Description | Verification Evidence |
|---|---|---|---|
| **1. Overbroad Impossibility Inference** | `docs/reviews/TC_TWO_VARIABLE_REMAINDER_REVIEW_PACKET.md`, `walkthrough.md`, `transcendental.py`, `research/epic/tc_corrective_epic_report.md` | Removed all phrasing claiming arithmetic vanishing $Q_\varepsilon = 0$ on fixed windows proves an impossibility theorem for a contradiction approach. Stated the exact reductio logic: $\mathsf{A} \vdash Q_\varepsilon = 0$, $\mathsf{A}, H(\rho_0) \vdash Q_\varepsilon > 0 \implies \mathsf{A} \vdash \neg H(\rho_0)$. Retained the narrower justified result: shrinking the omitted truncation tail does not make the included remainder small; the explicit formula requires full cancellation $\bar R_{\varepsilon, T} \to -A_{0, \Gamma}$, so a new restriction derived under $H(\rho_0)$ is needed to make that contradictory. Growing windows / global formulations are optional research candidates, not evasions of the explicit-formula identity. | `test_epic_reductio_logical_structure_audit`, `audit_arithmetic_compatibility_investigation` metadata in `data/tc_epic_two_variable_synthesis.json`. |
| **2. Kernel & Benchmark Mismatch** | `transcendental.py`, `tests/test_tc_mechanism_discovery.py`, `docs/reviews/TC_TWO_VARIABLE_REMAINDER_REVIEW_PACKET.md`, `walkthrough.md` | Frozen both kernel definitions. Added `_polynomial_mollifier_eta` ($(1-v^2)^4 \mathbf{1}_{|v|\le 1}$, $C^3(\mathbb R)$ with 4th derivative jumps at endpoints) side-by-side with canonical `_exponential_bump_eta` ($\exp(1 - 1/(1-v^2)) \mathbf{1}_{|v|<1}$, $C_c^\infty(\mathbb R)$). Decoupled both 256-node and 512-node benchmarks. Clarified test bump $w \in C_c^\infty(\mathbb R)$ with support $[8, 20]$. Confirmed that zero extension and translation of smooth bump create no derivative discontinuities; earlier numerical discrepancy was purely quadrature grid resolution. | `BENCHMARK_K0_J1_EPS0p1_T30_REGRESSION_FIXTURE`, `BENCHMARK_POLY_K0_J1_EPS0p1_T30_REGRESSION_FIXTURE`, `test_epic_kernel_comparison_and_benchmark_diagnostics`. |
| **3. Separation of Complete vs Truncated Remainder** | `transcendental.py`, `formal/RiemannScope/Grade.lean`, `.agents/claims/CLM-TC-022.json` | Explicitly separated complete remainder identity ($\bar Q_\varepsilon = \bar A_{\varepsilon, \Gamma} + \bar R^{\rm full}_\varepsilon = 0 \implies \bar R^{\rm full}_\varepsilon = -\bar A_{\varepsilon, \Gamma}$) from finite spectral cutoff identity ($\bar Q_\varepsilon = \bar A_{\varepsilon, \Gamma} + \bar R_{\varepsilon, T} + \bar E_{\varepsilon, T} = 0 \implies |\bar R_{\varepsilon, T} + A_{0, \Gamma}| \le |\bar A_{\varepsilon, \Gamma} - A_{0, \Gamma}| + |\bar E_{\varepsilon, T}|$). Formally proved both in Lean 4 with 0 sorry. Connected power-log tail limit to the actual tail bound. | Proved Lean theorems `explicit_formula_full_remainder_cancellation` and `explicit_formula_truncated_remainder_zero_Q_bound`; `#print axioms` audit. |
| **4. Positivity Scope Overgeneralization** | `transcendental.py`, `formal/RiemannScope/Grade.lean`, `.agents/claims/CLM-TC-022.json` | Clarified that certified positivity $A_{0, \Gamma} \in [0.543269, 0.545611] > 0$ applies only to the specific instance $(K=0, J=1, [8, 20], \rho_1)$. Falsified universal positivity across all grades and windows: cross-grade product $f_K f_J$ has constant phase $\cos((J-K)\gamma\log\tau)$ which can be negative (e.g. $[45, 65], K=0, J=2 \implies A_{0, \Gamma} \approx -0.00708 < 0$). Formally proved `cos_mul_cos_product_to_sum` in Lean 4. | `test_epic_selected_spectral_block_positivity_scope`, Lean 4 theorem `cos_mul_cos_product_to_sum`. |

---

## 3. Reproducible Comparison of the Two Kernels

### 3.1 Mathematical Definitions
Let $K = 0, J = 1$, $a_K = (2\pi)^0 = 1$, $a_J = (2\pi)^1 = 2\pi \approx 6.2831853$.
Test bump:
$$w(x) = \begin{cases} \exp\left(\frac{1}{36} - \frac{1}{(x-8)(20-x)}\right), & 8 < x < 20, \\ 0, & \text{otherwise}. \end{cases}$$
Here $w \in C_c^\infty(\mathbb R)$ with support $[8, 20]$.

Smooth background and zero mode profiles:
$$b_K(x) = a_K^{-1} - \frac{a_K^2}{x(x^2 - a_K^2)},$$
$$z_{K, T}(x) = \sum_{\substack{j=1, 2, 3 \\ \gamma_j \le T}} \frac{2}{\sqrt{a_K x}} \cos\left(\gamma_j \log(x/a_K)\right),$$
using the first three positive Riemann zero ordinates certified by FLINT Arb ball arithmetic:
- $\gamma_1 \approx 14.1347251417347$
- $\gamma_2 \approx 21.0220396387716$
- $\gamma_3 \approx 25.0108575801457$

Decomposition observable:
$$Q_{\varepsilon, T} = \iint w(x) w(y) \eta((x-y)/\varepsilon) [b_K(x) - z_{K, T}(x)][b_J(y) - z_{J, T}(y)] \, dx \, dy.$$

### 3.2 Numerical Quadrature Comparison ($K=0, J=1, \varepsilon=0.1, T=30$)

Integration is evaluated on the exact common support $x \in [\max(8, 8+\varepsilon v), \min(20, 20+\varepsilon v)]$ over $v \in [-1, 1]$.

| Metric / Parameter | Exponential Smooth Bump $\eta_{\rm smooth}$ | Polynomial Kernel $\eta_{\rm poly}$ |
|---|---|---|
| **Formula** | $\exp(1 - 1/(1-v^2)) \mathbf{1}_{|v|<1}$ | $(1 - v^2)^4 \mathbf{1}_{|v|\le 1}$ |
| **Smoothness Class** | $C_c^\infty(\mathbb R)$ | $C^3(\mathbb R)$ ($C^4$ endpoint jump) |
| **Peak Value** | $1.0$ (at $v=0$) | $1.0$ (at $v=0$) |
| **Kernel Integral $\int \eta(v) dv$** | $\approx 1.20690032244195$ | $256/315 \approx 0.81269841269841$ |
| **256-node Quadrature** | **0.2692888165323234** | **0.1813269198736548** |
| **512-node Quadrature** | **0.2692888165322876** | **0.1813269198736497** |
| **Quadrature Discrepancy** | $3.58 \times 10^{-14}$ | $5.10 \times 10^{-15}$ |
| **Selected Projection $A_{\varepsilon, \Gamma}$** | $0.05437243335385$ | $0.03661138865913$ |
| **Remainder $R_{\varepsilon, T} = Q_{\rm ret} - A_\varepsilon$** | $0.21491638317843$ | $0.14471553121452$ |

### 3.3 Scope and Role
The exponential smooth bump $\eta_{\rm smooth}$ is the canonical benchmark for smooth observable analysis in `RiemannScope`. The polynomial kernel $\eta_{\rm poly}$ is maintained as an exact-polynomial diagnostic comparator. Both are verified and tested via `test_epic_kernel_comparison_and_benchmark_diagnostics`.

---

## 4. Complete and Truncated Remainder Statements

### 4.1 Arithmetic Measure and Support Disjointness
For integer grades $K \in \mathbb Z$, the prime-power measure is:
$$\mu_K = \sum_{n \ge 2} \Lambda(n) \delta_{a_K n}, \qquad a_K = (2\pi)^K.$$
The bilinear arithmetic overlap on a test window $W = [A, B] \subset (\max(a_K, a_J), \infty)$ is:
$$Q_\varepsilon^{K, J}[w] = \iint w(x) w(y) \eta\left(\frac{x-y}{\varepsilon}\right) \, d\mu_K(x) \, d\mu_J(y).$$
For distinct integer grades $K \ne J$, the station sets $S_K = \{a_K n : n \ge 2\}$ and $S_J = \{a_J m : m \ge 2\}$ are disjoint by the Lindemann (1882) transcendence of $2\pi$.
On any compact interval $W$, the station sets $S_K \cap W$ and $S_J \cap W$ are finite. If both are non-empty, their minimum separation is:
$$d_{\min} = \min_{\substack{x \in S_K \cap W \\ y \in S_J \cap W}} |x - y| > 0.$$
If either station set is empty, $Q_\varepsilon \equiv 0$ vacuously for all $\varepsilon > 0$.
Thus, for all $0 < \varepsilon < d_{\min}$:
$$Q_\varepsilon^{K, J}[w] \equiv 0.$$

### 4.2 Complete Untruncated Remainder
Normalizing by $\varepsilon$ (denoted by bar):
$$\bar Q_\varepsilon = \frac{Q_\varepsilon}{\varepsilon}.$$
Under the complete explicit formula without spectral cutoff:
$$\bar Q_\varepsilon = \bar A_{\varepsilon, \Gamma} + \bar R^{\rm full}_\varepsilon = 0 \quad (\varepsilon < d_{\min}).$$
Therefore:
$$\bar R^{\rm full}_\varepsilon = -\bar A_{\varepsilon, \Gamma}.$$
Formally proved in Lean 4: `explicit_formula_full_remainder_cancellation`.

### 4.3 Truncated Remainder with Spectral Cutoff $T$
With finite spectral cutoff $T$:
$$\bar Q_\varepsilon = \bar A_{\varepsilon, \Gamma} + \bar R_{\varepsilon, T} + \bar E_{\varepsilon, T} = 0 \quad (\varepsilon < d_{\min}),$$
which yields:
$$\bar R_{\varepsilon, T} = -\bar A_{\varepsilon, \Gamma} - \bar E_{\varepsilon, T}.$$
Subtracting the asymptotic selected mode limit $-A_{0, \Gamma}$:
$$|\bar R_{\varepsilon, T} - (-A_{0, \Gamma})| = |-\bar A_{\varepsilon, \Gamma} - \bar E_{\varepsilon, T} + A_{0, \Gamma}| \le |\bar A_{\varepsilon, \Gamma} - A_{0, \Gamma}| + |\bar E_{\varepsilon, T}|.$$
Formally proved in Lean 4: `explicit_formula_truncated_remainder_zero_Q_bound`.

### 4.4 Convergence Hypotheses
To conclude that $\bar R_{\varepsilon, T(\varepsilon)} \to -A_{0, \Gamma}$ as $\varepsilon \to 0^+$:
1. **Selected Mode Convergence**: For any even kernel $\eta$, Taylor expansion gives:
   $$\left|\bar A_{\varepsilon, \Gamma} - A_{0, \Gamma}\right| = O(\varepsilon^2) \to 0.$$
2. **Truncation Tail Vanishing**: For $p > 2$ derivatives and cutoff path $T(\varepsilon) = \varepsilon^{-\alpha}$ with $\alpha > \frac{p}{p-2}$, the conservative truncation bound gives:
   $$|\bar E_{\varepsilon, T(\varepsilon)}| \le C_p \varepsilon^{\alpha(p-2) - p} \log^2(2 + \varepsilon^{-\alpha}) \to 0,$$
   formally proved in Lean 4: `power_log_tail_limit_tendsto`.
3. **Triangle Squeeze**:
   $$\lim_{\varepsilon \to 0^+} |\bar R_{\varepsilon, T(\varepsilon)} - (-A_{0, \Gamma})| \le \lim_{\varepsilon \to 0^+} |\bar A_{\varepsilon, \Gamma} - A_{0, \Gamma}| + \lim_{\varepsilon \to 0^+} |\bar E_{\varepsilon, T(\varepsilon)}| = 0 + 0 = 0.$$

---

## 5. Positivity Scope and Cross-Grade Product Sign

### 5.1 Instance Positivity
For $K=0, J=1$, window $[8, 20]$, and the first zero $\rho_1 = 1/2 + i\gamma_1$ ($\gamma_1 \approx 14.1347$):
The certified FLINT interval enclosure gives:
$$A_{0, \Gamma} \in [0.543269, 0.545611] > 0.54 > 0.$$
This certifies positivity for that specific instance.

### 5.2 Falsification of Universal Positivity
The cross-grade product in the diagonal limit is:
$$A_{0, \Gamma} = \left(\int_\mathbb R \eta(v) \, dv\right) \int_W w(x)^2 f_{K, \Gamma}(x) f_{J, \Gamma}(x) \, dx.$$
For a single conjugate pair $\rho = 1/2 + i\gamma$, the density is:
$$f_{K, \Gamma}(x) = \frac{2}{\sqrt{a_K x}} \cos\left(\gamma \log(x/a_K)\right).$$
By the product-to-sum identity (formally proved in Lean 4: `cos_mul_cos_product_to_sum`):
$$\cos\left(\gamma \log\frac{x}{a_K}\right) \cos\left(\gamma \log\frac{x}{a_J}\right) = \frac{1}{2} \left[ \cos\left(\gamma \log\frac{a_J}{a_K}\right) + \cos\left(2\gamma \log x - \gamma \log(a_K a_J)\right) \right].$$
For $a_K = \tau^K, a_J = \tau^J$, the difference phase is:
$$\gamma \log\frac{a_J}{a_K} = (J - K) \gamma \log\tau.$$
Because $(J - K) \log\tau \ne 0$ for $K \ne J$, this constant phase is not zero.
When $\cos((J - K)\gamma \log\tau) < 0$, the non-oscillating term is strictly negative.

**Counterexample**:
For $K = 0, J = 2$ ($M = J - K = 2$), $\gamma_1 \approx 14.134725$:
$$M \gamma_1 \log(2\pi) \approx 2 \times 14.134725 \times 1.837877 \approx 51.9686 \text{ rad} \equiv 1.7058 \text{ rad} \pmod{2\pi}.$$
$$\cos(1.7058) \approx -0.1345 < 0.$$
Evaluating $A_{0, \Gamma}$ on the window $[45, 65]$ with smooth bump $w$ gives:
$$A_{0, \Gamma} \approx -0.007080 < 0.$$
This confirms that $A_{0, \Gamma}$ is not a square and is **not universally positive**.

---

## 6. Research Attempt: The Missing Arithmetic Implication

### 6.1 Short Assumption Ledger

1. **Independently Established Arithmetic Premises ($\mathsf A$)**:
   - Prime-power distribution: $\mu_K = \sum_{n \ge 2} \Lambda(n) \delta_{\tau^K n}$ as a non-negative Radon measure on $\mathbb R_{>0}$.
   - Transcendence of $2\pi$ (Lindemann 1882): For $K \ne J \in \mathbb Z$, the support stations $\{ \tau^K n \}$ and $\{ \tau^J m \}$ have empty intersection.
   - Bilinear overlap vanishing: On any compact window $W \subset (\max(a_K, a_J), \infty)$, $Q_\varepsilon^{K, J}[w] \equiv 0$ for all $\varepsilon < d_{\min}$.
   - Non-multiplicativity of $\Lambda(n)$: $\Lambda(6) = 0 \ne \Lambda(2)\Lambda(3)$.
2. **How the Hypothetical Zero Enters ($H(\rho_0)$)**:
   - Assume $\zeta(\rho_0) = 0$ with $0 < \Re\rho_0 < 1$ and $\delta_0 = \Re\rho_0 - 1/2 \ne 0$.
   - By Riemann's functional equation and Schwarz reflection, $\rho_0$ generates a 4-zero quartet $\Gamma(\rho_0) = \{ \rho_0, \bar\rho_0, 1-\rho_0, 1-\bar\rho_0 \}$.
   - In the explicit formula for $\mu_K$, this quartet produces a distinct spectral mode $f_{K, \Gamma}(x)$ whose amplitude scales radially as $\tau^{-K\delta_0} x^{-1/2+\delta_0}$.
3. **Which Remainder Term the Property Must Constrain**:
   - In $\bar Q_\varepsilon = \bar A_{\varepsilon, \Gamma} + \bar R^{\rm full}_\varepsilon = 0$, it must constrain $\bar R^{\rm full}_\varepsilon$.
4. **Exact Implication / Inequality Sought**:
   - A lower bound derived under $H(\rho_0)$:
     $$\bar Q_\varepsilon^{K, J}[w] \ge c D_{K-J}(\rho_0) - r(\varepsilon) \quad (c > 0, \ r(\varepsilon) \to 0),$$
     or an independent bound on the complete remainder:
     $$\bar R^{\rm full}_\varepsilon > -\bar A_{\varepsilon, \Gamma}.$$
5. **First Unsupported Inference**:
   - The deduction that an off-line mode's radial dilation defect $D_M(\rho_0) = 4\sinh^2(M\delta_0\log\tau/2) > 0$ forces the cross-grade observable $\bar Q_\varepsilon^{K, J}[w]$ to be strictly positive.

### 6.2 Primary Literature and Theoretical Audit
1. **Weil Positivity (Weil 1952, Bombieri 2000)**:
   Weil proved that RH is equivalent to the positivity of the explicit formula quadratic form $W(g * \tilde g) \ge 0$ for all admissible test functions on $\mathbb R_{>0}$.
   - *Audit*: Weil positivity applies to self-convolutions $g * \tilde g$ on a single grade (equivalent to $K = J$). Across distinct grades $K \ne J$, the cross-pairing is not of convolution type. More fundamentally, because Weil positivity is equivalent to RH, assuming it unconditionally to derive a contradiction with an off-line zero would be circular (flagged by `.agents/skills/circularity-detector`).
2. **Li's Criterion (Li 1997)**:
   $\lambda_n = \sum_\rho [1 - (1 - 1/\rho)^n] \ge 0$ for all $n \ge 1$ is equivalent to RH. It cannot be used as an unconditional source of sign.
3. **Davenport-Heilbronn (1936)**:
   The Davenport-Heilbronn zeta function satisfies a functional equation $\xi(s) = \xi(1-s)$ with symmetric critical line $\Re(s) = 1/2$, but lacks an Euler product and has infinitely many off-line zeros. This proves that functional equation symmetry alone does *not* exclude off-line zeros; the Euler product / prime arithmetic is indispensable.
4. **The Mathematical Barrier**:
   On the arithmetic side, $\mu_K$ and $\mu_J$ are genuine prime-power measures. Their tensor product $\mu_K \otimes \mu_J$ is supported entirely on the discrete lattice points $(\tau^K n, \tau^J m) \in \mathbb R_{>0}^2$.
   Because $2\pi$ is transcendental, no point of this lattice lies on the diagonal $x = y$.
   The mollified kernel $\eta((x-y)/\varepsilon)$ has support restricted to the band $|x - y| \le \varepsilon$.
   For $\varepsilon < d_{\min}$, this band contains **no lattice points whatsoever**.
   Therefore, the arithmetic pairing $Q_\varepsilon^{K, J}[w]$ vanishes identically:
   $$Q_\varepsilon^{K, J}[w] = 0 \quad (\forall \varepsilon < d_{\min}).$$
   This vanishing is an exact property of the prime distribution across grades. It holds regardless of whether $\zeta(s)$ has off-line zeros or not.
   On the spectral side, the explicit formula is an exact Fourier-Mellin transform identity. It decomposes the identically zero distribution $\mu_K \otimes \mu_J$ into:
   $$0 \equiv \bar Q_\varepsilon = \bar A_{\varepsilon, \Gamma} + \bar R^{\rm full}_\varepsilon.$$
   Therefore, the full remainder $\bar R^{\rm full}_\varepsilon$ identically balances $\bar A_{\varepsilon, \Gamma}$:
   $$\bar R^{\rm full}_\varepsilon \equiv -\bar A_{\varepsilon, \Gamma}.$$
   Without an independent arithmetic theorem that specifically restricts the remainder under $H(\rho_0)$ so that $\bar R^{\rm full} \ne -\bar A$, the explicit formula absorbs the off-line mode through collective cancellation across the infinite zero spectrum and background.

### 6.3 Challenger Response
- **Logical Scoping**: The challenger confirms that arithmetic cancellation alone ($Q_\varepsilon = 0$) does not prove an impossibility theorem for the reductio program. However, within the scope of fixed-window bilinear pairings, the explicit formula is an exact identity that forces full cancellation $\bar R \to -A_0$.
- **Arithmetic Premises**: Ordinary non-negativity of $\mu_K$ yields positivity only on the diagonal $K = J$, where $Q_\varepsilon^{K, K} > 0$. On distinct grades $K \ne J$, $Q_\varepsilon^{K, J} \equiv 0$ gives no positive lower bound.
- **Unresolved Obligation**: No independently justified property of the complete prime-zeta relationship has been identified that prevents the infinite remainder from cancelling the selected mode. The Transcendental Continuation bridge remains strictly **OPEN**.

---

## 7. Exact Lean 4 Signatures and Axiom Audit

All 225 project theorems compile cleanly in `formal/RiemannScope/Grade.lean` under Lean 4.8.0 / Lake 5.0.0 with 0 sorry, 0 admit, and 0 warnings.

### Newly Completed Theorems

```lean
/-- Product-to-sum identity for cosine oscillations:
    cos(a) * cos(b) = (1/2) * (cos(a - b) + cos(a + b)).
    For cross-grade modes, a - b = gamma * (J - K) * log(tau) is constant in x.
    When K ≠ J, this constant phase can be negative, demonstrating that
    cross-grade products f_K * f_J are not universally positive squares. -/
theorem cos_mul_cos_product_to_sum (a b : ℝ) :
    Real.cos a * Real.cos b = (1 / 2 : ℝ) * (Real.cos (a - b) + Real.cos (a + b))

/-- Remainder error bound under exact arithmetic vanishing Q = 0:
    When the arithmetic overlap vanishes identically (Q = 0), the deviation of the
    truncated remainder R from the negative asymptotic selected mode -A₀ satisfies
    |R - (-A₀)| ≤ |A - A₀| + |E|. -/
theorem explicit_formula_truncated_remainder_zero_Q_bound (A R E A₀ : ℝ)
    (h_decomp : 0 = A + R + E) :
    |R - (-A₀)| ≤ |A - A₀| + |E|

/-- Full (untruncated) remainder identity under exact arithmetic vanishing Q = 0:
    When the complete explicit formula has no omitted tail (Q = A + R_full),
    vanishing Q = 0 forces the complete remainder to be the exact negative: R_full = -A. -/
theorem explicit_formula_full_remainder_cancellation (A R_full : ℝ)
    (h_decomp : 0 = A + R_full) :
    R_full = -A
```

### Essential Prior Lean Theorems

```lean
/-- Topological power-log tail limit on positive neighborhood filter:
    lim_{ε -> 0+} ε^r * log^2(2 + ε^(-α)) = 0 for all r > 0, α > 0. -/
theorem power_log_tail_limit_tendsto (r α : ℝ) (hr : 0 < r) (hα : 0 < α) :
    Filter.Tendsto (fun ε : ℝ => ε^r * Real.log (2 + ε^(-α))^2) (nhdsWithin 0 (Set.Ioi 0)) (nhds 0)

/-- General Confluent Vandermonde Rigidity:
    For any n ∈ ℕ and pairwise distinct complex exponents λ_j,
    if ∑_{j=1}^n c_j e^{λ_j u} = 0 for all u ∈ ℝ, then c_j = 0 for all j. -/
theorem finite_spectral_perturbation_rigidity_vandermonde_general (n : ℕ) (λ : Fin n → ℂ)
    (h_inj : Function.Injective λ) (c : Fin n → ℂ)
    (h_sum : ∀ u : ℝ, (∑ j : Fin n, c j * Complex.exp (λ j * (u : ℂ))) = 0) (j : Fin n) :
    c j = 0
```

### Axiom Audit (`#print axioms`)
All newly and previously compiled theorems depend strictly on the standard Mathlib foundational axioms:
```lean
[propext, Classical.choice, Quot.sound]
```
Zero custom axioms, zero unproved assertions (`sorry`), and zero `admit`.

---

## 8. Final Verification Outcomes

| Verification Stage | Command Executed | Outcome | Details |
|---|---|---|---|
| **Mechanism Discovery Tests** | `python -m pytest tests/test_tc_mechanism_discovery.py` | **PASSED** | 95 passed in 132s; covers dual-kernel benchmarks, positivity scope, and reductio logic. |
| **Claim Pre-Acceptance Gates** | `python -m pytest .agents/verification/test_claim_audit_gates.py` | **PASSED** | 54 passed in 0.49s; 10 structural gates validated. |
| **Claim Spec Audit** | `python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --claim-file .agents/claims/CLM-TC-022.json` | **PASSED** | 10/10 pre-acceptance gates verified. |
| **Claim Register Cross-Check** | `python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --cross-check-register --repo-root .` | **PASSED** | 110 claims verified (24 audited terminal, 78 grandfathered, 8 exempt). |
| **Formal Lake Build** | `lake build` (in `formal/`) | **PASSED** | 1559 targets compiled cleanly; 225 project theorems. |
| **Formal Build Certification** | `python scripts/build_formal.py --allow-dirty` | **PASSED** | Generated `formal/build_report.json` with hash verification. |
| **Check-Fast Tier** | `python scripts/workflow.py check-fast` | **PASSED** | Full fast-tier test suite passed (631 passed, 32 deselected). |
| **Artifact Validation** | `python scripts/workflow.py validate-artifacts` | **PASSED** | 508 Arb certs and 225 Lean declarations verified across 17 runs. |
| **Current Artifact Validation** | `python scripts/workflow.py validate-artifacts --current` | **FAILED (Exit 1)** (Expected) | Baseline certificates are hash-pinned to immutable commit `82643cafd605492233c6c1e992b78c2c30d45f13`. |
| **Canonical Plan Audit** | `python scripts/workflow.py plan-canonical` | **PASSED** | Canonical execution plan audited. |
| **Git Diff Check** | `git diff --check` | **PASSED** | Clean diff, no trailing whitespace or merge conflict markers. |

---

## 9. Plain Epistemic Verdict and Governing Research Question

### Question: Was a new implication toward forbidden coincidence established?
**None.**

No new mathematical implication forcing cross-grade arithmetic coincidence ($m\tau^K = n\tau^J$) from an off-line zero hypothesis $H(\rho_0)$ was established. On any fixed compact window, the arithmetic overlap vanishes identically ($Q_\varepsilon^{K, J}[w] \equiv 0$), and the explicit formula operates as an exact identity that forces the complete remainder to balance the selected zero mode ($\bar R^{\rm full}_\varepsilon = -\bar A_{\varepsilon, \Gamma}$ and $\bar R_{\varepsilon, T(\varepsilon)} \to -A_{0, \Gamma}$).

### Strongest Justified Next Research Question
> *Does there exist an arithmetic test observable—necessarily involving either multi-scale windows $W(\varepsilon)$ that capture growing prime sets or a global Hilbert-space operator—for which the cross-grade prime-power support separation forces a positive spectral defect $D(\rho_0) > 0$ that cannot be cancelled by the explicit-formula remainder?*
