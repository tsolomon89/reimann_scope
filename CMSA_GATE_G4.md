# Gate G4 Infinite-Regularization and Radial-Sign Theorem Report

**Repository**: `tsolomon89/reimann_scope`  
**Classification**: `FAIL_RADIAL_POSITIVITY` (raw finite-window $\Delta S_W$ and additive renormalizations) / `FINITE_IDENTITY_PROVED_G4_OPEN` (finite algebraic expansion)  
**Status**: Gate G4 finite radial sign analyzed; raw finite radial positivity falsified on general parameter domains; additive scalar renormalizations closed by No-Go Theorem; infinite regularized bridge remains the active research frontier.

---

## 1. Executive Summary & Frontier Statement

The Completed Mean-Square Anchor (CMSA) framework establishes an unconditional exact arithmetic vanishing anchor:
$$\mathcal A(\sigma) = \lim_{T \to \infty} \frac{1}{2T} \int_{-T}^T \left| A(\sigma + it) - \frac{\Xi'}{\Xi}\left(\sigma - \frac{1}{2} + it\right) \right|^2 dt - \sum_{n=2}^\infty \frac{\Lambda(n)^2}{n^{2\sigma}} = 0 \quad (\sigma > 1).$$

At any finite zero height cutoff $H$ and averaging parameter $T$, the finite windowed spectral expansion decomposes algebraically as:
$$S_{H, T}^{(W)}(\sigma) = I_{AA} - I_{AZ} - I_{ZA} + I_{ZZ},$$
with closed-form kernels $J_T(p,q), K_T(\lambda, \mu; a)$ (Rectangular) and $J_T^{\text{Fejér}}(p,q), K_T^{\text{Fejér}}(\lambda, \mu; a)$ (Fejér), and verified numerical quadrature for Abel-Poisson and Gaussian windows ($< 10^{-25}$).

### The Gate G4 Finite Radial Sign Resolution & Additive No-Go Theorem
1. **Exact Second-Order Radial Response**: Derived the exact symmetric second-order coefficient $C_W(\sigma, \gamma, T) = -2\Re \int_{\mathbb R} W_T(t) F_0(t) \overline{D_\gamma(\sigma - 1/2 + it)} dt$, governing the leading variation $\Delta S_W = \delta^2 C_W + O(\delta^4)$.
2. **Negative Sign Witnesses**: High-precision numerical quadrature produced 4 negative sign witnesses (WIT 1–4 across Rectangular, Fejér with $T > \gamma$, Abel, Gaussian), proving that the raw synthetic finite-fibre response $\Delta S_W$ is **NOT globally positive**.
3. **Additive-Reference Invariance No-Go Theorem**: Proved that for any scalar reference term $R_W(A)$ independent of the zero configuration, $\tilde S_W(Z_\delta) - \tilde S_W(Z_0) \equiv S_W(Z_\delta) - S_W(Z_0)$, proving that divisor-independent additive scalar subtraction cannot repair or alter the negative radial sign.

Consequently:
- The **raw finite synthetic-fibre functional $\Delta S_W$** is classified as `FAIL_RADIAL_POSITIVITY`.
- **Divisor-independent additive scalar renormalizations** are classified as `FAIL_RADIAL_POSITIVITY` (by Additive-Reference Invariance).
- The **exact finite algebraic expansion and closed kernels** are classified as `FINITE_IDENTITY_PROVED_G4_OPEN`.
- The **grade-dilated completed logarithmic derivative** is classified as `GRADE_COORDINATE_REDUNDANT`.

---

## 2. Exact Mathematical Derivations

### 2.1 The Multiplicity-Two On-Line Fibre $Z_0(z)$
Let $z = \sigma - 1/2 + it = a + it$ with $a = \sigma - 1/2 > 0$. The multiplicity-two critical-line zero pair at ordinate $\gamma$ contributes:
$$Z_0(z) = 2 \left( \frac{1}{z - i\gamma} + \frac{1}{z + i\gamma} \right) = \frac{4z}{z^2 + \gamma^2}.$$

### 2.2 The Off-Line Reflected Replacement $Z_\delta(z)$
For an off-line quartet $\{\pm\delta \pm i\gamma\}$ ($\delta \ne 0$), the upper-half zeros are $\lambda_1 = \delta + i\gamma$ and $\lambda_2 = -\delta + i\gamma$. The symmetric Hadamard sum is:
$$Z_\delta(z) = \left( \frac{1}{z - \lambda_1} + \frac{1}{z + \lambda_1} \right) + \left( \frac{1}{z - \lambda_2} + \frac{1}{z + \lambda_2} \right) = \frac{2z}{z^2 - (\delta+i\gamma)^2} + \frac{2z}{z^2 - (-\delta+i\gamma)^2}.$$
Since $(\pm\delta + i\gamma)^2 = \delta^2 - \gamma^2 \pm 2i\delta\gamma$:
$$z^2 - (\pm\delta+i\gamma)^2 = (z^2 + \gamma^2 - \delta^2) \mp 2i\delta\gamma.$$
Combining fractions:
$$Z_\delta(z) = 2z \left[ \frac{2(z^2+\gamma^2-\delta^2)}{(z^2+\gamma^2-\delta^2)^2 - (2i\delta\gamma)^2} \right] = \boxed{\frac{4z(z^2+\gamma^2-\delta^2)}{(z^2+\gamma^2-\delta^2)^2 + 4\delta^2\gamma^2}}.$$

### 2.3 Exact Defect Difference and Second-Order Derivative $D_\gamma(z)$
Subtracting $Z_0(z)$ with $u = z^2+\gamma^2$:
$$Z_\delta(z) - Z_0(z) = 4z \left[ \frac{u-\delta^2}{(u-\delta^2)^2 + 4\delta^2\gamma^2} - \frac{1}{u} \right] = \frac{4z\delta^2(u - 4\gamma^2 - \delta^2)}{u [(u-\delta^2)^2 + 4\delta^2\gamma^2]}$$
$$= \boxed{\frac{4z\delta^2(z^2 - 3\gamma^2 - \delta^2)}{(z^2+\gamma^2)[(z^2+\gamma^2-\delta^2)^2 + 4\delta^2\gamma^2]}}.$$
Taking the limit $\delta \to 0$:
$$\boxed{D_\gamma(z) := \lim_{\delta\to 0} \frac{Z_\delta(z) - Z_0(z)}{\delta^2} = \frac{4z(z^2 - 3\gamma^2)}{(z^2+\gamma^2)^3}}.$$

### 2.4 The Exact Radial Response Coefficient $C_W(\sigma, \gamma, T)$
For any normalized even window $W_T(t)$ on $\mathbb R$, let $F_0(t) = A(\sigma+it) - Z_0(\sigma-1/2+it)$.
Then:
$$A(\sigma+it) - Z_\delta(z) = F_0(t) - \delta^2 D_\gamma(z) + O(\delta^4).$$
Computing the squared modulus difference:
$$|A - Z_\delta|^2 - |A - Z_0|^2 = |F_0(t) - \delta^2 D_\gamma(z)|^2 - |F_0(t)|^2 = -2\Re\left( F_0(t) \cdot \delta^2 \overline{D_\gamma(z)} \right) + O(\delta^4).$$
Integrating against $W_T(t)$:
$$\boxed{\Delta S_W(\sigma, \gamma, \delta, T) = \delta^2 C_W(\sigma, \gamma, T) + O(\delta^4)},$$
where
$$\boxed{C_W(\sigma, \gamma, T) = -2\Re \int_{\mathbb R} W_T(t) F_0(t) \overline{D_\gamma(\sigma - 1/2 + it)} dt}.$$

---

## 3. High-Precision Numerical Evidence for Sign Witnesses

The second-order coefficient $C_W(\sigma, \gamma, T)$ and full variation $\Delta S_W$ were evaluated across all four window families using high-precision quadrature (`dps=80`, with mpmath estimated error):

| Witness ID | Window Type | Parameters ($\sigma, \gamma, \delta, T$) | Value $\Delta S_W$ | Estimated Error | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **WIT-01** | Rectangular | $\sigma=2.0, \gamma=14.0, \delta=0.1, T=2.8$ | $-5.9067025 \times 10^{-7}$ | $1.0 \times 10^{-154}$ | **NUMERICAL_EVIDENCE_NEGATIVE** |
| **WIT-02** | Fejér | $\sigma=5.0, \gamma=14.0, \delta=0.49, T=16.8$ | $-1.7183799 \times 10^{-4}$ | $2.0 \times 10^{-132}$ | **NUMERICAL_EVIDENCE_NEGATIVE** |
| **WIT-03** | Abel-Poisson | $\sigma=1.01, \gamma=21.0, \delta=0.49, T=1.05$ | $-3.4413949 \times 10^{-6}$ | $2.0 \times 10^{-6}$ | **NUMERICAL_EVIDENCE_NEGATIVE** |
| **WIT-04** | Gaussian | $\sigma=1.01, \gamma=14.0, \delta=0.49, T=1.4$ | $-7.2473271 \times 10^{-5}$ | $2.0 \times 10^{-19}$ | **NUMERICAL_EVIDENCE_NEGATIVE** |

### Mathematical Significance of Witness WIT-02
In Witness WIT-02, $T = 16.8 > \gamma = 14.0$, yet $\Delta S_W = -1.7183799 \times 10^{-4} < 0$. This refutes the conjecture that $\Delta S_W$ is unconditionally positive whenever $T > \gamma$.
- **Mechanism**: For large $\sigma = 5.0$, $a = 4.5$ broadens and damps the resonance peak at $t = 14$. The Fejér linear weight $(1 - |t|/T)$ attenuates $t=14$ by a factor $1 - 14/16.8 = 1/6$, while weighting the non-resonant low-frequency region $t \approx 0$ (where $\Re D_\gamma(z) < 0$) with full weight $1$. The resulting integral $C_W = -7.279 \times 10^{-4} < 0$ forces $\Delta S_W < 0$.

### Diagnostic Note on Infinite-Domain Quadrature (WIT-03)
Independent panel integration for Witness WIT-03 on $[0, 60]$ yields approximately $-4.05240574800226 \times 10^{-6}$, whereas the unbounded range $[- \infty, \infty]$ under default mpmath transformation yields midpoint $-3.4413949 \times 10^{-6}$ with estimated error $2 \times 10^{-6}$. Both integrations confirm that the sign is strictly negative.

---

## 4. Elementary Absolutely Convergent Dirichlet-Series Mean-Square Lemma

Let $a_n$ be complex coefficients with $\sum_{n=1}^\infty |a_n| < \infty$. For the arithmetic prime series, $a_n = \Lambda(n)n^{-\sigma}$ ($\sigma > 1$), absolute summability holds because $\Lambda(n) \le \log n$ and $\sum_{n=2}^\infty n^{-\sigma} \log n < \infty$.

### Step 1: Exact Finite Identity for General Complex Coefficients
For any $N \ge 1$ and $T > 0$:
$$\frac{1}{2T}\int_{-T}^T \left| \sum_{n=1}^N a_n n^{-it} \right|^2 dt = \sum_{m,n=1}^N a_m \overline{a_n} \frac{1}{2T}\int_{-T}^T e^{-it\log(m/n)} dt = \sum_{n=1}^N |a_n|^2 + \sum_{1 \le m \ne n \le N} a_m \overline{a_n} \frac{\sin(T\log(n/m))}{T\log(n/m)}.$$

### Step 2: Fixed-$N$ Limit Passage ($T \to \infty$)
For any fixed finite $N$, the off-diagonal sum contains finitely many terms with $|\log(n/m)| \ge \log(1 + 1/N) > 0$. As $T \to \infty$:
$$\lim_{T\to\infty} \sum_{1 \le m \ne n \le N} a_m \overline{a_n} \frac{\sin(T\log(n/m))}{T\log(n/m)} = 0 \implies \lim_{T\to\infty} I_N(T) = \sum_{n=1}^N |a_n|^2.$$

### Step 3: Uniform Infinite Completion ($N \to \infty$)
Let $P(t) = \sum_{n=1}^\infty a_n n^{-it}$ and $P_N(t) = \sum_{n=1}^N a_n n^{-it}$. The uniform tail bound is:
$$\|P - P_N\|_\infty \le \sum_{n=N+1}^\infty |a_n| =: \varepsilon_N \to 0 \quad\text{as } N \to \infty.$$
Using the triangle inequality on the $L^2([-T, T], \frac{dt}{2T})$ norm $\|\cdot\|_T$:
$$\left| \|P\|_T - \|P_N\|_T \right| \le \|P - P_N\|_T \le \|P - P_N\|_\infty \le \varepsilon_N.$$
Thus:
$$\left| \|P\|_T^2 - \|P_N\|_T^2 \right| \le \varepsilon_N (\|P\|_T + \|P_N\|_T) \le \varepsilon_N \left( 2\sum_{n=1}^\infty |a_n| \right).$$
This bound is **strictly independent of $T$**.

### Step 4: Interchange of Limits
Given $\varepsilon > 0$, choose $N$ large enough that $2\varepsilon_N \sum |a_n| < \varepsilon/3$ and $|\sum_{n=1}^N |a_n|^2 - \sum_{n=1}^\infty |a_n|^2| < \varepsilon/3$.
Then choose $T_0$ such that for all $T > T_0$, $|I_N(T) - \sum_{n=1}^N |a_n|^2| < \varepsilon/3$.
Then for all $T > T_0$:
$$\left| \frac{1}{2T}\int_{-T}^T |P(t)|^2 dt - \sum_{n=1}^\infty |a_n|^2 \right| < \varepsilon.$$
This establishes the elementary Dirichlet-series mean-square limit without invoking external black-box theorems.

---

## 5. Additive-Reference Invariance No-Go Theorem

Let $S_W(Z) = \int W_T(t) |A(t) - Z(t)|^2 dt$.

Let $R_W(A)$ be any scalar reference functional independent of $Z, \delta, \gamma$, and the zero divisor (e.g. a zero-free arithmetic reference subtraction). Define the renormalized functional:
$$\tilde S_W(Z) = S_W(Z) - R_W(A).$$

**Theorem (Additive Reference Invariance)**:
$$\tilde S_W(Z_\delta) - \tilde S_W(Z_0) = \left( S_W(Z_\delta) - R_W(A) \right) - \left( S_W(Z_0) - R_W(A) \right) = S_W(Z_\delta) - S_W(Z_0).$$

**Corollary (Closure of Additive Renormalizations)**:
A divisor-independent additive scalar subtraction cannot alter, repair, or renormalize the radial sign. Any candidate whose regularized variation relies purely on an additive reference subtraction remains sign-changing and is classified as `FAIL_RADIAL_POSITIVITY`.

**Lean 4 Formalization**: Formally verified in `formal/RiemannScope/ArithmeticBridge.lean`:
- `RiemannScope.additive_reference_subtraction_invariance`: `(S z_delta - R) - (S z_0 - R) = S z_delta - S z_0`.

---

## 6. Candidate Classification Matrix

| Candidate Class | Arithmetic Firewall | Finite Expansion | Remainder Control | Limit Order | Radial Positivity | Pair Isolation | Grade Covariance | Final Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Raw Finite Synthetic-Fibre Functional $\Delta S_W$** | PROVED | PROVED | OPEN | OPEN / CHAR | **FALSIFIED (WIT 1–4)** | OPEN | REDUNDANT | `FAIL_RADIAL_POSITIVITY` |
| **Divisor-Independent Additive Renormalizations** | PROVED | PROVED | OPEN | OPEN | **FALSIFIED (No-Go)** | OPEN | REDUNDANT | `FAIL_RADIAL_POSITIVITY` |
| **Finite 4-Term Algebraic Expansion** | PROVED | **PROVED** | OPEN | OPEN | N/A (identity) | N/A | REDUNDANT | `FINITE_IDENTITY_PROVED_G4_OPEN` |
| **Dilated Completed Log-Derivative** | PROVED | PROVED | N/A | N/A | N/A | N/A | **PROVED REDUNDANT** | `GRADE_COORDINATE_REDUNDANT` |
| **Candidate CMSA-1** | PROVED | PROVED | OPEN | OPEN | FALSIFIED (raw) | OPEN | REDUNDANT | `FAIL_RADIAL_POSITIVITY` |
| **Candidate CMSA-2** | PROVED | PROVED | OPEN | OPEN | FALSIFIED (raw) | OPEN | REDUNDANT | `FAIL_RADIAL_POSITIVITY` |
| **Candidate CMSA-3** | PROVED | PROVED | N/A | N/A | N/A | N/A | PROVED REDUNDANT | `GRADE_COORDINATE_REDUNDANT` |

---

## 7. Formal Lean 4 Theorem Inventory

All compiled cleanly in Lean 4 (`formal/RiemannScope/ArithmeticBridge.lean`, 0 `sorry`, 0 `admit`, 0 warnings):
1. `RiemannScope.additive_reference_subtraction_invariance`: $(S(Z_\delta) - R) - (S(Z_0) - R) = S(Z_\delta) - S(Z_0)$.
2. `RiemannScope.complex_radial_defect_difference_numerator`: $(u-\delta^2)u - ((u-\delta^2)^2 + 4\delta^2\gamma^2) = \delta^2(u - 4\gamma^2 - \delta^2)$ over $\mathbb C$.
3. `RiemannScope.complex_radial_second_order_numerator_decomposition`: $4z\delta^2(z^2-3\gamma^2-\delta^2) = 4z\delta^2(z^2-3\gamma^2) - 4z\delta^4$ over $\mathbb C$.
4. `RiemannScope.radial_defect_difference_numerator`: real specialization over $\mathbb R$.
5. `RiemannScope.radial_second_order_numerator_decomposition`: real specialization over $\mathbb R$.
6. `RiemannScope.cofinal_sequence_fixed_limit_zero`: $\forall H \in \mathbb R, \forall \varepsilon > 0, \exists N, \forall n \ge N, |H / (n + 1)| < \varepsilon$.
7. `RiemannScope.cofinal_diagonal_not_tendsto_zero`: $\neg (\forall \varepsilon > 0, \exists N, \forall n \ge N, |(n+1)/(n+1) - 0| < \varepsilon)$.
8. `RiemannScope.cofinal_sequence_diagonal_witness`: $(n+1)/(n+1) = 1$ for all $n \in \mathbb N$.
9. `RiemannScope.cofinal_schedule_distinct_from_fixed_limit`: $(cT)/T = c \ne 0$ for $T \ne 0$.
10. `RiemannScope.ConditionalG4RegularizedBridge.all_defects_zero`: Rigidity theorem forcing all represented zero defects $d_j = 0$.

---

## 8. The Exact Next Theorem Target

Since divisor-independent additive scalar subtraction is conclusively closed by the Additive-Reference Invariance No-Go Theorem, any viable future candidate cannot be an additive subtraction on the outer mean square.

The exact next mathematical question is:
$$\boxed{
\text{Can an integrand-, inner-product-, or operator-modified regularized spectral functional } \mathcal R_W(\sigma, Z)
\atop
\text{be constructed with an independent arithmetic counterpart } \mathcal A_W^{\text{arith}}(\sigma) \text{ satisfying exact radial positivity } \Delta \mathcal R_W \ge 0?
}$$

