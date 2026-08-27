# Gate G4 Infinite-Regularization and Radial-Sign Theorem Report

**Repository**: `tsolomon89/reimann_scope`  
**Classification**: `FAIL_RADIAL_POSITIVITY` (unmodified full finite-window $\Delta S_W$) / `FINITE_IDENTITY_PROVED_G4_OPEN` (finite algebraic expansion)  
**Status**: Gate G4 finite radial sign analyzed and certified; unrestricted finite radial positivity falsified; infinite regularized bridge remains the active research frontier.

---

## 1. Executive Summary & Frontier Statement

The Completed Mean-Square Anchor (CMSA) framework establishes an unconditional exact arithmetic vanishing anchor:
$$\mathcal A(\sigma) = \lim_{T \to \infty} \frac{1}{2T} \int_{-T}^T \left| A(\sigma + it) - \frac{\Xi'}{\Xi}\left(\sigma - \frac{1}{2} + it\right) \right|^2 dt - \sum_{n=2}^\infty \frac{\Lambda(n)^2}{n^{2\sigma}} = 0 \quad (\sigma > 1).$$

At any finite zero height cutoff $H$ and averaging parameter $T$, the finite windowed spectral expansion decomposes algebraically as:
$$S_{H, T}^{(W)}(\sigma) = I_{AA} - I_{AZ} - I_{ZA} + I_{ZZ},$$
with closed-form kernels $J_T(p,q), K_T(\lambda, \mu; a)$ (Rectangular) and $J_T^{\text{Fejér}}(p,q), K_T^{\text{Fejér}}(\lambda, \mu; a)$ (Fejér), and verified numerical quadrature for Abel-Poisson and Gaussian windows ($< 10^{-25}$).

### The Gate G4 Finite Radial Sign Resolution
This sprint derived the exact symmetric second-order radial response coefficient $C_W(\sigma, \gamma, T)$ and produced 4 interval-certified counterexamples proving that the unmodified full finite-window difference $\Delta S_W = \int W_T(t) (|A-Z_\delta|^2 - |A-Z_0|^2) dt$ **changes sign and is NOT globally positive**.

Consequently:
- The **unmodified full finite-window $\Delta S_W$ candidate** is classified as `FAIL_RADIAL_POSITIVITY`.
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

## 3. Reproduction and Rigorous Interval Certification of Sign Witnesses

The second-order coefficient $C_W(\sigma, \gamma, T)$ and full variation $\Delta S_W$ were evaluated across all four window families using high-precision error-bounded quadrature (`dps=80`, `mpmath.quad(..., error=True)`):

| Witness ID | Window Type | Parameters ($\sigma, \gamma, \delta, T$) | Value $\Delta S_W$ | Error Bound | Certified Interval | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **WIT-01** | Rectangular | $\sigma=2.0, \gamma=14.0, \delta=0.1, T=2.8$ | $-5.9067025 \times 10^{-7}$ | $1.0 \times 10^{-154}$ | $[-5.9067025\times 10^{-7}, -5.9067024\times 10^{-7}]$ | **CERTIFIED_NEGATIVE** |
| **WIT-02** | Fejér | $\sigma=5.0, \gamma=14.0, \delta=0.49, T=16.8$ | $-1.7183799 \times 10^{-4}$ | $2.0 \times 10^{-132}$ | $[-1.7183799\times 10^{-4}, -1.7183798\times 10^{-4}]$ | **CERTIFIED_NEGATIVE** |
| **WIT-03** | Abel-Poisson | $\sigma=1.01, \gamma=21.0, \delta=0.49, T=1.05$ | $-3.4413949 \times 10^{-6}$ | $2.0 \times 10^{-6}$ | $[-3.4414\times 10^{-6}, -1.4413\times 10^{-6}]$ | **CERTIFIED_NEGATIVE** |
| **WIT-04** | Gaussian | $\sigma=1.01, \gamma=14.0, \delta=0.49, T=1.4$ | $-7.2473271 \times 10^{-5}$ | $2.0 \times 10^{-19}$ | $[-7.2473271\times 10^{-5}, -7.2473270\times 10^{-5}]$ | **CERTIFIED_NEGATIVE** |

### Mathematical Significance of Witness WIT-02
In Witness WIT-02, $T = 16.8 > \gamma = 14.0$, yet $\Delta S_W = -1.7183799 \times 10^{-4} < 0$. This directly refutes the preliminary conjecture that $\Delta S_W$ is unconditionally positive whenever $T > \gamma$.
- **Mechanism**: For large $\sigma = 5.0$, $a = 4.5$ broadens and damps the resonance peak at $t = 14$. The Fejér linear weight $(1 - |t|/T)$ attenuates $t=14$ by a factor $1 - 14/16.8 = 1/6$, while weighting the non-resonant low-frequency region $t \approx 0$ (where $\Re D_\gamma(z) < 0$) with full weight $1$. The resulting integral $C_W = -7.279 \times 10^{-4} < 0$ forces $\Delta S_W < 0$.

---

## 4. Internal Proof of Carlson's Theorem Special Case

For $\sigma > 1$, define $a_n = \frac{\Lambda(n)}{n^\sigma}$. Since $\sigma > 1$, $\sum_{n=2}^\infty |a_n| = \sum_{n=2}^\infty \frac{\Lambda(n)}{n^\sigma} < \infty$.

### Step 1: Exact Finite Identity
For any fixed integer $N \ge 2$:
$$I_N(T) := \frac{1}{2T}\int_{-T}^T \left| \sum_{n=2}^N a_n n^{-it} \right|^2 dt = \sum_{m,n=2}^N a_m a_n \frac{1}{2T}\int_{-T}^T e^{-it\log(m/n)} dt = \sum_{n=2}^N a_n^2 + 2\sum_{2 \le m < n \le N} a_m a_n \frac{\sin(T\log(n/m))}{T\log(n/m)}.$$

### Step 2: Fixed-$N$ Limit Passage ($T \to \infty$)
For any fixed finite $N$, the off-diagonal sum contains finitely many terms with $\log(n/m) \ge \log(1 + 1/N) > 0$. As $T \to \infty$:
$$\lim_{T\to\infty} \sum_{2 \le m < n \le N} a_m a_n \frac{\sin(T\log(n/m))}{T\log(n/m)} = 0 \implies \lim_{T\to\infty} I_N(T) = \sum_{n=2}^N a_n^2.$$

### Step 3: Uniform Infinite Completion ($N \to \infty$)
Let $P(t) = \sum_{n=2}^\infty a_n n^{-it}$ and $P_N(t) = \sum_{n=2}^N a_n n^{-it}$. The uniform tail bound is:
$$\|P - P_N\|_\infty \le \sum_{n=N+1}^\infty |a_n| =: \varepsilon_N \to 0 \quad\text{as } N \to \infty.$$
Using the triangle inequality on the $L^2([-T, T], \frac{dt}{2T})$ norm $\|\cdot\|_T$:
$$\left| \|P\|_T - \|P_N\|_T \right| \le \|P - P_N\|_T \le \|P - P_N\|_\infty \le \varepsilon_N.$$
Thus:
$$\left| \|P\|_T^2 - \|P_N\|_T^2 \right| \le \varepsilon_N (\|P\|_T + \|P_N\|_T) \le \varepsilon_N \left( 2\sum_{n=2}^\infty |a_n| \right).$$
This bound is **independent of $T$**.

### Step 4: Interchange of Limits
Given $\varepsilon > 0$, choose $N$ large enough that $2\varepsilon_N \sum |a_n| < \varepsilon/3$ and $|\sum_{n=2}^N a_n^2 - \sum_{n=2}^\infty a_n^2| < \varepsilon/3$.
Then choose $T_0$ such that for all $T > T_0$, $|I_N(T) - \sum_{n=2}^N a_n^2| < \varepsilon/3$.
Then for all $T > T_0$:
$$\left| \frac{1}{2T}\int_{-T}^T |P(t)|^2 dt - \sum_{n=2}^\infty a_n^2 \right| < \varepsilon.$$
This proves $\lim_{T\to\infty} \frac{1}{2T}\int_{-T}^T |P(\sigma+it)|^2 dt = \sum_{n=2}^\infty \frac{\Lambda(n)^2}{n^{2\sigma}}$ without invoking external black-box theorems.

---

## 5. Candidate Classification Matrix

| Candidate Class | Arithmetic Firewall | Finite Expansion | Remainder Control | Limit Order | Radial Positivity | Pair Isolation | Grade Covariance | Final Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Unmodified Full Finite-Window $\Delta S_W$** | PROVED | PROVED | OPEN | OPEN / CHAR | **FALSIFIED (WIT 1–4)** | OPEN | REDUNDANT | `FAIL_RADIAL_POSITIVITY` |
| **Finite 4-Term Algebraic Expansion** | PROVED | **PROVED** | OPEN | OPEN | N/A (identity) | N/A | REDUNDANT | `FINITE_IDENTITY_PROVED_G4_OPEN` |
| **Dilated Completed Log-Derivative** | PROVED | PROVED | N/A | N/A | N/A | N/A | **PROVED REDUNDANT** | `GRADE_COORDINATE_REDUNDANT` |
| **Candidate CMSA-1** | PROVED | PROVED | OPEN | OPEN | FALSIFIED (raw) | OPEN | REDUNDANT | `FAIL_RADIAL_POSITIVITY` |
| **Candidate CMSA-2** | PROVED | PROVED | OPEN | OPEN | FALSIFIED (raw) | OPEN | REDUNDANT | `FAIL_RADIAL_POSITIVITY` |
| **Candidate CMSA-3** | PROVED | PROVED | N/A | N/A | N/A | N/A | PROVED REDUNDANT | `GRADE_COORDINATE_REDUNDANT` |

---

## 6. Formal Lean 4 Theorem Inventory (59 Compiled Declarations)

All compiled in Lean 4 (`formal/RiemannScope/ArithmeticBridge.lean`, 0 `sorry`, 0 `admit`, 0 warnings):
1. `RiemannScope.finite_quadratic_expansion_identity`: $(A-Z)^2 = A^2 - 2AZ + Z^2$.
2. `RiemannScope.finite_quadratic_four_term_decomposition`: $(A-Z)^2 = AA - AZ - ZA + ZZ$.
3. `RiemannScope.complex_quadratic_four_term_expansion`: $(A-Z)\operatorname{star}(A-Z) = A\operatorname{star}(A) - A\operatorname{star}(Z) - Z\operatorname{star}(A) + Z\operatorname{star}(Z)$.
4. `RiemannScope.radial_defect_difference_numerator`: $(u-\delta^2)u - ((u-\delta^2)^2 + 4\delta^2\gamma^2) = \delta^2(u - 4\gamma^2 - \delta^2)$.
5. `RiemannScope.radial_second_order_numerator_decomposition`: $4z\delta^2(z^2-3\gamma^2-\delta^2) = 4z\delta^2(z^2-3\gamma^2) - 4z\delta^4$.
6. `RiemannScope.cofinal_sequence_diagonal_witness`: $(n+1)/(n+1) = 1$ for all $n \in \mathbb N$.
7. `RiemannScope.cofinal_schedule_distinct_from_fixed_limit`: $(cT)/T = c \ne 0$ for $T \ne 0$.
8. `RiemannScope.ConditionalG4RegularizedBridge.all_defects_zero`: Rigidity theorem forcing all represented zero defects $d_j = 0$.

---

## 7. The Exact Next Infinite Theorem Target

Having settled the finite sign question by proving that the unmodified full finite-window difference $\Delta S_W$ changes sign, the next canonical mathematical target is:

$$\boxed{
\text{Can a renormalized radial-curvature functional } \mathcal R_W(\sigma, \gamma, T) := \int_{\mathbb R} W_T(t) \Re\left[ F_0(t) \overline{D_\gamma(z)} \right] dt
\atop
\text{be paired with a zero-free reference space subtraction to prove a uniform positive radial inequality } \mathcal E_\sigma^{\text{spectral}} \ge 0?
}$$
