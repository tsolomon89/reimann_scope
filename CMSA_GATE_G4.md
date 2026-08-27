# Gate G4 Infinite-Regularization and Radial-Sign Theorem Report

**Repository**: `tsolomon89/reimann_scope`
**Classification**:
- `FAIL_RADIAL_POSITIVITY` (raw finite Fejér window response & zero-independent additive scalar-subtraction class)
- `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE` (full infinite/cofinal CMSA-1 & CMSA-2 functionals)
- `FINITE_IDENTITY_PROVED_G4_OPEN` (finite algebraic four-term quadratic expansion)
- `GRADE_COORDINATE_REDUNDANT` (grade-dilated completed logarithmic derivative)
- `CERTIFIED_NEGATIVE_ARB_BALL` (evidence/certificate status for canonical witness WIT-02)

**Status**: Gate G4 finite radial sign analyzed; Fejér WIT-02 certified strictly negative via outward-rounded Arb ball integration across full symmetric support $[-16.8, 16.8]$; WIT 1, 3, 4 supported by high-precision numerical evidence; additive scalar renormalizations closed by No-Go Theorem; full infinite/cofinal CMSA functionals classified as `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`; earliest open subgate and next live cofinal theorem obligation precisely defined.

---

## 1. Executive Summary & Frontier Statement

The Completed Mean-Square Anchor (CMSA) framework establishes an unconditional exact arithmetic vanishing anchor:
$$\mathcal A(\sigma) = \lim_{T \to \infty} \frac{1}{2T} \int_{-T}^T \left| A(\sigma + it) - \frac{\Xi'}{\Xi}\left(\sigma - \frac{1}{2} + it\right) \right|^2 dt - \sum_{n=2}^\infty \frac{\Lambda(n)^2}{n^{2\sigma}} = 0 \quad (\sigma > 1).$$

At any finite zero height cutoff $H$ and averaging parameter $T$, the finite windowed spectral expansion decomposes algebraically as:
$$S_{H, T}^{(W)}(\sigma) = I_{AA} - I_{AZ} - I_{ZA} + I_{ZZ},$$
with closed-form kernels $J_T(p,q), K_T(\lambda, \mu; a)$ (Rectangular) and $J_T^{\text{Fejér}}(p,q), K_T^{\text{Fejér}}(\lambda, \mu; a)$ (Fejér), and verified numerical quadrature for Abel-Poisson and Gaussian windows ($< 10^{-25}$).

### The Gate G4 Proof/Evidence Boundary & Earliest Open Subgate
1. **Exact Second-Order Radial Response**: Derived the exact symmetric second-order coefficient $C_W(\sigma, \gamma, T) = -2\Re \int_{\mathbb R} W_T(t) F_0(t) \overline{D_\gamma(\sigma - 1/2 + it)} dt$, governing the leading variation $\Delta S_W = \delta^2 C_W + O(\delta^4)$ under uniform domination hypotheses.
2. **Certified Outward-Rounded Arb Ball Witness (WIT-02)**: Across the full symmetric compact support $[-16.8, 16.8]$, the Fejér radial difference $\Delta S_{\text{Fejér}}$ for $(\sigma=5, \gamma=14, \delta=0.49, T=16.8)$ is certified strictly negative via outward-rounded Arb ball arithmetic with 50,000 subintervals:
   $$\Delta S_{\text{Fejér}} \in [-1.89473 \times 10^{-4}, -1.54203 \times 10^{-4}] \subset (-\infty, 0).$$
3. **High-Precision Numerical Evidence (WIT 1, 3, 4)**: Rectangular, Abel-Poisson, and Gaussian windows yield negative numerical estimates with mpmath estimated errors, providing strong numerical evidence.
4. **Additive-Reference Invariance No-Go Theorem**: Proved that for any scalar reference term $R_W(A)$ independent of the zero configuration, $(S_W(Z_\delta) - R) - (S_W(Z_0) - R) \equiv S_W(Z_\delta) - S_W(Z_0)$.
5. **Largest Proved Obstruction Class**:
   $$\boxed{\text{Any candidate family containing the stated finite Fejér functional and modified only by a zero-independent additive scalar reference fails unconditional radial positivity.}}$$
   *Scope Boundary*: This proved obstruction class does NOT cover non-additive operators, different pairings, or the complete infinite/cofinal limit.
6. **Earliest Open Subgate**:
   $$\boxed{\text{Subgate G4-Open: Prove a negative raw response analytically or with validated outward-rounded interval arithmetic on the general infinite/regularized limit.}}$$

Consequently:
- The **raw finite Fejér window response** and **every zero-independent additive scalar subtraction** of that finite Fejér response are classified strictly as `FAIL_RADIAL_POSITIVITY`.
- The **full infinite/cofinal CMSA-1 and CMSA-2 functionals** are classified as `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.
- The **compact Fejér WIT-02 certificate** has evidence status `CERTIFIED_NEGATIVE_ARB_BALL`.
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
Under uniform domination hypotheses, integrating against $W_T(t)$ yields:
$$\boxed{\Delta S_W(\sigma, \gamma, \delta, T) = \delta^2 C_W(\sigma, \gamma, T) + O(\delta^4)},$$
where
$$\boxed{C_W(\sigma, \gamma, T) = -2\Re \int_{\mathbb R} W_T(t) F_0(t) \overline{D_\gamma(\sigma - 1/2 + it)} dt}.$$

---

## 3. Certified Arb Ball Witness and Numerical Evidence Suite

The radial difference $\Delta S_W$ was evaluated across four window families:

| Witness ID | Window Type | Parameters ($\sigma, \gamma, \delta, T$) | Value $\Delta S_W$ | Enclosure / Estimated Error | Epistemic Status | Engine |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **WIT-02** | Fejér | $\sigma=5.0, \gamma=14.0, \delta=0.49, T=16.8$ | $-1.7183799 \times 10^{-4}$ | $[-1.89473\times 10^{-4}, -1.54203\times 10^{-4}]$ | **CERTIFIED_NEGATIVE_ARB_BALL** | python-flint (Arb) |
| **WIT-01** | Rectangular | $\sigma=2.0, \gamma=14.0, \delta=0.1, T=2.8$ | $-5.9067025 \times 10^{-7}$ | $\pm 1.0 \times 10^{-154}$ (est) | **NUMERICAL_EVIDENCE_NEGATIVE** | mpmath quad |
| **WIT-03** | Abel-Poisson | $\sigma=1.01, \gamma=21.0, \delta=0.49, T=1.05$ | $-3.4413949 \times 10^{-6}$ | $\pm 2.0 \times 10^{-6}$ (est) | **NUMERICAL_EVIDENCE_NEGATIVE** | mpmath quad |
| **WIT-04** | Gaussian | $\sigma=1.01, \gamma=14.0, \delta=0.49, T=1.4$ | $-7.2473271 \times 10^{-5}$ | $\pm 2.0 \times 10^{-19}$ (est) | **NUMERICAL_EVIDENCE_NEGATIVE** | mpmath quad |

### Rigorous Arb Ball Enclosure for Witness WIT-02
For Witness WIT-02, the complete symmetric support $[-16.8, 16.8]$ was partitioned into $N = 50,000$ subintervals in `certify_g4_fejer_witness_arb`. Every transcendental evaluation (`digamma`, `log`, `pi`, division, squaring, Riemann summation) was executed in certified outward-rounded Arb ball arithmetic directly over $[-16.8, 16.8]$ without assuming evenness reduction or reflection as an operational premise.
- Result: $\Delta S_{\text{Fejér}} \in [-1.89473 \times 10^{-4}, -1.54203 \times 10^{-4}]$, strictly bounded away from zero ($\text{upper bound} < -1.54 \times 10^{-4} < 0$).
- This provides a genuine, certified mathematical proof that the raw Fejér response achieves strictly negative values at this parameter point.

### Explanatory Note on Conjugation Symmetry
For any real $\sigma > 1$ and $t \in \mathbb R$:
1. The explicit meromorphic archimedean/pole term:
   $$A(\sigma + it) = \frac{1}{\sigma+it} + \frac{1}{\sigma-1+it} - \frac{1}{2}\log \pi + \frac{1}{2}\psi\left(\frac{\sigma+it}{2}\right)$$
   satisfies $\overline{1/(\sigma+it)} = 1/(\sigma-it)$, $\overline{1/(\sigma-1+it)} = 1/(\sigma-1-it)$, and $\overline{\psi(z)} = \psi(\bar z)$, hence $A(\sigma, -t) = \overline{A(\sigma, t)}$ directly from term-by-term conjugation (without invoking zeta conjugation or a general Schwarz reflection hypothesis).
2. For any discrete quadruplet $\rho = 1/2 \pm \delta \pm i\gamma$, pairing $+i\gamma$ with $-i\gamma$ yields:
   $$Z_\delta(\sigma, -t) = \frac{1}{\sigma - 1/2 - \delta - i(-t - \gamma)} + \frac{1}{\sigma - 1/2 - \delta - i(-t + \gamma)} = \overline{Z_\delta(\sigma, t)}.$$
3. Hence $A(\sigma, -t) - Z_\delta(\sigma, -t) = \overline{A(\sigma, t) - Z_\delta(\sigma, t)}$, which gives $|A(\sigma, -t) - Z_\delta(\sigma, -t)|^2 = |A(\sigma, t) - Z_\delta(\sigma, t)|^2$.
4. Because $W_T(-t) = W_T(t)$ is even, the integrand $f(t)$ is an exact even function of $t$.
*(Note: Direct certified integration over the full $[-T, T]$ domain does not rely on this symmetry as an operational premise).*

### Verified Sign Mechanism for Witness WIT-02
Direct point-by-point computation of the integrand distribution $f(t) = 2 W_T(t) (|A - Z_\delta|^2 - |A - Z_0|^2)$ on $[0, 16.8]$ reveals:
- **Low-Frequency Positive Mass ($t \in [0, 8]$)**:
  At $t = 0.0$, $f(0) = +8.43 \times 10^{-6} > 0$; at $t = 2.0$, $f(2) = +7.07 \times 10^{-6} > 0$; at $t = 5.0$, $f(5) = +8.83 \times 10^{-6} > 0$; at $t = 8.0$, $f(8) = +1.54 \times 10^{-6} > 0$.
- **Off-Resonance Dominant Negative Mass ($t \in [9, 14]$)**:
  At $t = 10.0$, $f(10) = -4.05 \times 10^{-5} < 0$; at $t = 12.0$, $f(12) = -1.03 \times 10^{-4} < 0$; at $t = 14.0$, $f(14) = -1.08 \times 10^{-6} < 0$.
- **High-Frequency Positive Mass ($t \in [15, 16.8]$)**:
  At $t = 16.0$, $f(16) = +3.21 \times 10^{-5} > 0$.
- **Total Balance**: The deep negative trough in $t \in [9, 14]$ (peaking around $t = 12$) heavily outweighs the positive low-frequency mass, driving the total integral to $-1.718 \times 10^{-4} < 0$.

### Diagnostic Note on Infinite-Domain Quadrature (WIT-03)
Independent panel integration for Witness WIT-03 on $[0, 60]$ yields approximately $-4.05240574800226 \times 10^{-6}$, whereas the unbounded range $[-\infty, \infty]$ under default mpmath transformation yields midpoint $-3.4413949 \times 10^{-6}$ with estimated error $2 \times 10^{-6}$. Both integrations confirm negative numerical evidence.

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
$$\tilde S_W(Z_\delta) - \tilde S_W(Z_0) = \left( S_W(Z_\delta) - R_W(A) \right) - \left( S_W(Z_0) - R_W(A) \right) \equiv S_W(Z_\delta) - S_W(Z_0).$$

**Sign Invariance & Scope**:
This proved identity shows that divisor-independent additive scalar subtraction cannot alter the raw radial difference. It proves that the additive class shares identically whatever sign behaviour the raw functional exhibits.

**Lean 4 Formalization**: Formally verified in `formal/RiemannScope/ArithmeticBridge.lean`:
- `RiemannScope.additive_reference_subtraction_invariance`: `(S z_delta - R) - (S z_0 - R) = S z_delta - S z_0`.

---

## 6. Hypotheses for Integrated Pointwise Expansions

To integrate the pointwise expansion $|A - Z_\delta|^2 - |A - Z_0|^2 = -2\delta^2 \Re(F_0 \overline{D_\gamma}) + O(\delta^4)$ against a window $W_T(t)$ and obtain a valid $O(\delta^4)$ remainder on the integral:
1. **Window Integrability**: $W_T(t) \ge 0$ with $W_T \in L^1(\mathbb R) \cap L^\infty(\mathbb R)$ and $\int_{\mathbb R} W_T(t) dt = 1$.
2. **Denominator Separation**: For all $\delta \in [0, \delta_0]$ with $\delta_0 < a = \sigma - 1/2$, the denominators of $Z_\delta(a+it)$ are separated from zero uniformly: $|a \pm \delta + i(t \pm \gamma)| \ge a - \delta_0 > 0$.
3. **Uniform Domination**: The Taylor remainder function $R_4(t, \delta) = \delta^{-4} (|A-Z_\delta|^2 - |A-Z_0|^2 + 2\delta^2 \Re(F_0 \overline{D_\gamma}))$ satisfies $|R_4(t, \delta)| \le g(t)$ for all $\delta \in [0, \delta_0]$, where $g \in L^1(\mathbb R, W_T(t)dt)$.
4. **Legitimacy of Limit Interchange**: Under hypotheses 1–3, the Dominated Convergence Theorem justifies exchanging the limit $\delta \to 0$ and the integral, establishing $\lim_{\delta\to 0} \frac{\Delta S_W}{\delta^2} = C_W(\sigma, \gamma, T)$.

---

## 7. Candidate Classification Matrix

| Candidate Class | Arithmetic Firewall | Finite Expansion | Remainder Control | Limit Order | Radial Positivity | Pair Isolation | Grade Covariance | Final Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Raw Finite Fejér Window Response** | PROVED | PROVED | OPEN | OPEN / CHAR | **CERTIFIED NEGATIVE (WIT-02 Arb)** | OPEN | REDUNDANT | `FAIL_RADIAL_POSITIVITY` |
| **Divisor-Independent Additive Class on Finite Fejér** | PROVED | PROVED | OPEN | OPEN | **INVARIANT TO RAW (No-Go)** | OPEN | REDUNDANT | `FAIL_RADIAL_POSITIVITY` |
| **Recomputed Exact-Remainder Candidate $S_T(Z_H; R_{H,\delta})$** | PROVED | PROVED | COLLAPSED | **COLLAPSED TO FULL (Algebraic Identity)** | OPEN | OPEN | COVARIANT | `FAIL_LIMIT_ORDER_DEPENDENCE` |
| **Fixed Finite Perturbation under Infinite Mean** | PROVED | PROVED | OPEN | **VANISHES (Invisibility Theorem)** | ZERO RESPONSE | OPEN | COVARIANT | `FAIL_LIMIT_ORDER_DEPENDENCE` |
| **Growing / Cofinal Perturbation $\Delta_{H(T)}$** | PROVED | PROVED | OPEN | OPEN (Infinite Bridge) | OPEN | OPEN | COVARIANT | `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE` |
| **Finite 4-Term Algebraic Expansion** | PROVED | **PROVED** | OPEN | OPEN | N/A (identity) | N/A | REDUNDANT | `FINITE_IDENTITY_PROVED_G4_OPEN` |
| **Dilated Completed Log-Derivative** | PROVED | PROVED | N/A | N/A | N/A | N/A | **PROVED REDUNDANT** | `GRADE_COORDINATE_REDUNDANT` |
| **Candidate CMSA-1 (Full Infinite/Cofinal)** | PROVED | PROVED | OPEN | OPEN | OPEN (infinite) | OPEN | REDUNDANT | `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE` |
| **Candidate CMSA-2 (Full Infinite/Cofinal)** | PROVED | PROVED | OPEN | OPEN | OPEN (infinite) | OPEN | REDUNDANT | `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE` |
| **Candidate CMSA-3** | PROVED | PROVED | N/A | N/A | N/A | N/A | PROVED REDUNDANT | `GRADE_COORDINATE_REDUNDANT` |

---

## 8. Formal Lean 4 Theorem Inventory (81 Compiled Declarations)

All compiled cleanly in Lean 4 (`formal/RiemannScope/ArithmeticBridge.lean`, 0 `sorry`, 0 `admit`, 0 warnings):
1. `RiemannScope.complex_finset_sum_mul_star`: $(\sum_{i \in s} b_i) \cdot \overline{(\sum_{j \in s} b_j)} = \sum_{i \in s} \sum_{j \in s} b_i \overline{b_j}$.
2. `RiemannScope.complex_finset_normSq_eq_double_sum_re`: $\operatorname{normSq}(\sum_{i \in s} b_i) = \Re(\sum_{i \in s} \sum_{j \in s} b_i \overline{b_j})$.
3. `RiemannScope.abstract_finite_kernel_decomposition`: $(\sum_{i \in s} \sum_{j \in s} K(i, j)) = (\sum_{i \in s} b_i) \cdot \overline{(\sum_{j \in s} b_j)}$ under hypothesis $K(i, j) = b_i \overline{b_j}$.
4. `RiemannScope.linear_operator_finite_double_sum_interchange`: $L(\sum_{i \in s} \sum_{j \in s} K(i, j)) = \sum_{i \in s} \sum_{j \in s} L(K(i, j))$ for additive maps $L : \mathbb C \to+ \mathbb C$.
5. `RiemannScope.abstract_windowed_kernel_expansion`: $L(\operatorname{normSq}(\sum_{i \in s} b_i)) = L((\sum_{i \in s} \sum_{j \in s} K(i, j)).\text{re})$.
6. `RiemannScope.linear_schedule_grade_covariant`: $\forall c, \tau \in \mathbb R$, the linear schedule $H_c(T) = cT$ is discrete grade-covariant ($H_c(\tau T) = \tau H_c(T)$).
7. `RiemannScope.grade_covariant_schedule_nonuniqueness`: Grade covariance alone does NOT uniquely determine a schedule; for any $c_1 \ne c_2$, both $H_{c_1}$ and $H_{c_2}$ are covariant and distinct for all $T > 0$.
8. `RiemannScope.periodic_modulated_schedule_covariant`: Any schedule $H(T) = T \cdot q(\log_\tau T)$ with 1-periodic $q$ satisfies grade covariance.
9. `RiemannScope.exact_remainder_cancellation`: $R = F - Z \implies Z + R = F$ identically over $\mathbb C$.
10. `RiemannScope.functional_decomposition_independence`: $\forall f, f(Z + R) = f(F)$ for any functional $f$ whenever $R = F - Z$.
11. `RiemannScope.complex_squared_norm_difference_expansion`: $Q(F, \Delta) = \operatorname{normSq}(F+\Delta) - \operatorname{normSq}(F) = \operatorname{normSq}(\Delta) + 2\Re(F\bar\Delta)$ over $\mathbb C$.
12. `RiemannScope.complex_squared_norm_difference_background_subtraction`: $Q(F, \Delta) - Q(G, \Delta) = 2\Re((F-G)\bar\Delta)$ over $\mathbb C$.
13. `RiemannScope.complex_squared_norm_difference_not_background_independent`: Counterexample $F=1, G=-1, \Delta=1 \implies Q(1, 1)=3 \ne -1=Q(-1, 1)$.
14. `RiemannScope.fixed_finite_energy_scaling_zero`: For any fixed finite energy $E \ge 0$, $\lim_{T\to\infty} \frac{E}{2T} = 0$ (normalized energy scaling vanishes).
15. `RiemannScope.additive_reference_subtraction_invariance`: $(S(Z_\delta) - R) - (S(Z_0) - R) = S(Z_\delta) - S(Z_0)$.
16. `RiemannScope.complex_radial_defect_difference_numerator`: $(u-d^2)u - ((u-d^2)^2 + 4d^2\gamma^2) = d^2(u - 4\gamma^2 - d^2)$ over $\mathbb C$.
17. `RiemannScope.complex_radial_second_order_numerator_decomposition`: $4z d^2(z^2-3\gamma^2-d^2) = 4z d^2(z^2-3\gamma^2) - 4z d^4$ over $\mathbb C$.
18. `RiemannScope.radial_defect_difference_numerator`: real specialization over $\mathbb R$.
19. `RiemannScope.radial_second_order_numerator_decomposition`: real specialization over $\mathbb R$.
20. `RiemannScope.tendsto_cofinal_fixed_zero`: `Tendsto (fun (n : ℕ) => H / ((n : ℝ) + 1)) atTop (𝓝 0)` (Mathlib Filter.Tendsto).
21. `RiemannScope.not_tendsto_cofinal_diagonal_zero`: `¬ Tendsto (fun (n : ℕ) => ((n : ℝ) + 1) / ((n : ℝ) + 1)) atTop (𝓝 0)` (Mathlib Filter.Tendsto).
22. `RiemannScope.finite_sum_tendsto_interchange`: `Tendsto (fun n => ∑ i in s, f i n) atTop (𝓝 (∑ i in s, g i))` (Mathlib Filter.Tendsto).
23. `RiemannScope.cofinal_sequence_fixed_limit_zero`: $\forall H \in \mathbb R, \forall \varepsilon > 0, \exists N, \forall n \ge N, |H / (n + 1)| < \varepsilon$ (elementary $\varepsilon$-$N$).
24. `RiemannScope.cofinal_diagonal_not_tendsto_zero`: $\neg (\forall \varepsilon > 0, \exists N, \forall n \ge N, |(n+1)/(n+1) - 0| < \varepsilon)$ (elementary $\varepsilon$-$N$).
25. `RiemannScope.cofinal_sequence_diagonal_witness`: $(n+1)/(n+1) = 1$ for all $n \in \mathbb N$.
26. `RiemannScope.cofinal_schedule_distinct_from_fixed_limit`: $(cT)/T = c \ne 0$ for $T \ne 0$.
27. `RiemannScope.ConditionalG4RegularizedBridge.all_defects_zero`: Rigidity theorem forcing all represented zero defects $d_j = 0$.

*(Formalization Boundary Note: Lean formalizes abstract finite-sum/kernel algebra, background-dependence expansions, and algebraic identities. The concrete continuous Dirichlet sinc-integral identity $\frac{1}{2T}\int_{-T}^T |P_N|^2 dt = \sum |a_n|^2 + \sum_{m\ne n} a_m \overline{a_n} \frac{\sin(T\log(n/m))}{T\log(n/m)}$ is retained as a rigorous internal paper derivation (§4), with its Mathlib continuous integration interface demarcated as an external formalization boundary).*

---

## 9. Schedule Covariance, Remainder Cancellation, Background Dependence, and Fixed-Finite Invisibility

### 9.1 Transcendental Continuation (TC) Origin Dilation & Schedule Covariance Law
In Transcendental Continuation (TC), the project uses **origin coordinate dilation**:
$$s_K = \tau^K s, \quad c_K = \frac{\tau^K}{2}, \quad z_K = s_K - c_K = \tau^K\left(s - \frac{1}{2}\right).$$
*(Note: $s \to 1/2 + \tau^K(s-1/2)$ is the centered coordinate dilation $z_K = \tau^K z$, not the origin coordinate transformation).*
On the imaginary axis, ordinate dilates as $t_K = \tau^K t$. For unit grade step $K=1$, the ordinate scaling is $t' = \tau t$.
Scale covariance between integration window width $T$ and zero truncation cutoff $H$ requires $H' = \tau H$, establishing the covariance law:
$$\boxed{H(\tau T) = \tau H(T), \quad \text{with } \tau = 2\pi.}$$

### 9.2 Complete Schedule Classification & Rigorous Proof Separation
- **Proved in Lean 4**:
  1. `RiemannScope.linear_schedule_grade_covariant`: Linear schedules $H_c(T) = cT$ ($c > 0$) satisfy $H_c(\tau T) = \tau H_c(T)$.
  2. `RiemannScope.grade_covariant_schedule_nonuniqueness`: For $c_1 \ne c_2$, $H_{c_1}(T) \ne H_{c_2}(T)$ for all $T > 0$, proving non-uniqueness.
  3. `RiemannScope.periodic_modulated_schedule_covariant`: $H(T) = T q(\log_\tau T)$ with 1-periodic $q$ is grade-covariant.
- **Paper Proofs Provided**:
  - **Theorem 1 (General Form)**: Every positive schedule $H:(0,\infty)\to(0,\infty)$ satisfying $H(\tau T) = \tau H(T)$ with $\tau > 1$ is of the form $H(T) = T q(\log_\tau T)$ where $q:\mathbb R \to (0,\infty)$ is 1-periodic.
    *Proof*: Define $\psi(T) = H(T)/T$. Then $\psi(\tau T) = \frac{H(\tau T)}{\tau T} = \frac{\tau H(T)}{\tau T} = \psi(T)$. Since $T \mapsto \log_\tau T$ is a bijection from $(0,\infty)$ to $\mathbb R$, define $q(u) = \psi(\tau^u)$. Then $q(u+1) = \psi(\tau^{u+1}) = \psi(\tau \cdot \tau^u) = \psi(\tau^u) = q(u)$, so $q$ is 1-periodic. Conversely, $H(T) = T \psi(T) = T q(\log_\tau T)$. $\blacksquare$
  - **Theorem 2 (Asymptotic Collapse)**: If $\lim_{T\to\infty} \frac{H(T)}{T} = c \in (0,\infty)$ exists and $\tau > 1$, then $q(u) \equiv c$ is constant, so $H(T) = cT$.
    *Proof*: Let $\lim_{T\to\infty} \psi(T) = c$. For any $u \in \mathbb R$, let $T_n = \tau^{u+n}$. Since $\tau > 1$, $T_n \to \infty$ as $n \to \infty$. Thus $\lim_{n\to\infty} \psi(T_n) = c$. But $\psi(T_n) = q(u+n) = q(u)$ for all $n$. Therefore $q(u) = c$ for all $u \in \mathbb R$, which gives $H(T) = cT$. $\blacksquare$
- **Unproved Assertion Downgraded**:
  - The claim that a sharp Hadamard remainder estimate forces $c \ge 1$ is **unproved** and is downgraded to an unproved heuristic remark (preventing omitted zeros from entering the averaging window).

**Falsified Premise**:
$$\boxed{\text{Falsified Premise: "Bilateral discrete grade covariance uniquely determines the cofinal schedule."}}$$

### 9.3 Background-Dependence Theorem and Scope of Additive Invariance

For any complex-valued background $F$ and perturbation $\Delta$, define the squared-norm difference (variation):
$$Q(F, \Delta) = |F + \Delta|^2 - |F|^2.$$

**Theorem (Pointwise Background Expansion)**:
$$Q(F, \Delta) = |\Delta|^2 + 2\Re(F\bar\Delta).$$
For two distinct backgrounds $F$ and $G$:
$$Q(F, \Delta) - Q(G, \Delta) = 2\Re((F - G)\bar\Delta).$$
*Proof*: $|F+\Delta|^2 - |F|^2 = (F+\Delta)(\bar F + \bar\Delta) - |F|^2 = |\Delta|^2 + F\bar\Delta + \bar F\Delta = |\Delta|^2 + 2\Re(F\bar\Delta)$. Subtracting the expression for $G$ gives $2\Re((F-G)\bar\Delta)$. Formally proved in Lean 4 (`complex_squared_norm_difference_expansion`, `complex_squared_norm_difference_background_subtraction`). $\blacksquare$

**Concrete Counterexample**:
Let $F = 1, G = -1, \Delta = 1$. Then:
$$Q(1, 1) = |1+1|^2 - |1|^2 = 3, \quad Q(-1, 1) = |-1+1|^2 - |-1|^2 = -1.$$
$$Q(1, 1) - Q(-1, 1) = 3 - (-1) = 4 \ne 0.$$
Formally proved in Lean 4 (`complex_squared_norm_difference_not_background_independent`).

**Why `additive_reference_subtraction_invariance` Does Not Apply Inside Squared Norms**:
The theorem `additive_reference_subtraction_invariance` applies exclusively to *outer* scalar reference subtractions:
$$(S(Z_\delta) - R) - (S(Z_0) - R) \equiv S(Z_\delta) - S(Z_0).$$
When a background $F_0$ is placed *inside* a squared norm $|F_0 + \Delta|^2$, it expands nonlinearly through the cross-term $2\Re(F_0\bar\Delta)$. Shifting the background from $-Z_0$ (the isolated zero model) to $F_0 - Z_0$ (the completed-function remainder model) shifts the variation by $2\Re(F_0\bar\Delta) \ne 0$.
**Correction**: The claim that Case B automatically reduces to the certified negative finite Fejér response is **withdrawn**. The sign of $Q(F_0, \Delta)$ depends explicitly on the completed-function background $F_0$.

### 9.4 Perturbation Semantics by Case

Terminology:
- **Conjugate pair**: $\{\delta + i\gamma, \delta - i\gamma\}$
- **Same-height functional-reflection pair**: $\{\delta + i\gamma, -\delta + i\gamma\}$
- **Symmetric quartet**: $\{\pm\delta \pm i\gamma\}$

Rigorous Distinction of Cases:
1. **Case A (Recomputed Exact Remainder $R_{H,\delta} = F_\delta - Z_{H,\delta}$)**:
   $$Z_{H,\delta} + R_{H,\delta} \equiv F_\delta.$$
   The truncation parameter $H$ cancels algebraically before taking any limit. The functional collapses to evaluating the full completed function $F_\delta$, entirely independent of $H$ and $H(T)$.
   *Classification*: `FAIL_LIMIT_ORDER_DEPENDENCE` (descriptive reason: `COLLAPSED_COFINAL_IDENTITY`).
2. **Case B (Fixed Actual Remainder with Fixed Finite Perturbation $\Delta$)**:
   $$Z_{H,\delta} + R_{H,0} = F_0 + \Delta \quad \text{once } H \ge \gamma.$$
   This becomes independent of $H$, but its response $Q(F_0, \Delta) = |\Delta|^2 + 2\Re(F_0\bar\Delta)$ is background-dependent. Furthermore, under normalized infinite averaging, it vanishes identically by the Invisibility Theorem below.
   *Classification*: `FAIL_LIMIT_ORDER_DEPENDENCE`.
3. **Case C (Fixed Actual Remainder with Growing / Cofinal Perturbation $\Delta_{H(T)}$)**:
   $$Z_{H(T),\delta} + R_{H(T),0} = F_0 + \Delta_{H(T)}.$$
   This does NOT reduce to a fixed finite perturbation. The number of perturbed terms grows with $T$, creating a genuine infinite convergence and boundary layer problem.
   *Classification*: `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.

### 9.5 Fixed Finite Perturbation Invisibility Theorem

**Theorem (Invisibility of Fixed Finite Divisor Perturbations)**:
Let $\sigma > 1$ and let $P_\sigma(t) = \sum_{n=2}^\infty \Lambda(n) n^{-\sigma-it}$ be the prime Dirichlet series.
Let $\Delta(t) = \sum_{j=1}^N \frac{c_j}{a_j + i(t - \gamma_j)}$ be any fixed finite linear combination of zero resolvents with $N < \infty, a_j > 0, c_j \in \mathbb C$.
Then:
1. $\Delta \in L^2(\mathbb R)$, with $\|\Delta\|_{L^2} \le \sum_{j=1}^N |c_j| \sqrt{\frac{\pi}{a_j}} < \infty$.
2. The normalized infinite mean-square variation vanishes identically:
$$\lim_{T\to\infty} \frac{1}{2T} \int_{-T}^T \left( |P_\sigma(t) - \Delta(t)|^2 - |P_\sigma(t)|^2 \right) dt = 0.$$

**Proof**:
1. *Uniform Bound on Arithmetic Background*: Since $\sigma > 1$, absolute convergence yields:
   $$|P_\sigma(t)| \le \sum_{n=2}^\infty \frac{\Lambda(n)}{n^\sigma} = -\frac{\zeta'}{\zeta}(\sigma) = M_\sigma < \infty.$$
2. *Finite Resolvent $L^2$ Norm*: For each constituent resolvent $r_j(t) = \frac{1}{a_j + i(t-\gamma_j)}$:
   $$\int_{-\infty}^\infty |r_j(t)|^2 dt = \int_{-\infty}^\infty \frac{dt}{a_j^2 + (t-\gamma_j)^2} = \frac{\pi}{a_j}.$$
   By Minkowski's triangle inequality on $L^2(\mathbb R)$, $\|\Delta\|_{L^2} \le \sum_{j=1}^N |c_j| \sqrt{\pi/a_j} < \infty$.
3. *Integral Decomposition*:
   $$\frac{1}{2T}\int_{-T}^T (|P_\sigma - \Delta|^2 - |P_\sigma|^2) dt = \frac{1}{2T}\int_{-T}^T |\Delta(t)|^2 dt - \frac{1}{T}\Re \int_{-T}^T P_\sigma(t)\overline{\Delta(t)} dt.$$
   - *Direct $\Delta^2$ Term*:
     $$\frac{1}{2T}\int_{-T}^T |\Delta(t)|^2 dt \le \frac{\|\Delta\|_{L^2}^2}{2T} \to 0 \quad \text{as } T \to \infty.$$
     (Formally proved in Lean 4: `fixed_finite_energy_scaling_zero`).
   - *Cross-Term*:
     By Cauchy-Schwarz on $[-T, T]$:
     $$\left| \frac{1}{T}\Re \int_{-T}^T P_\sigma(t)\overline{\Delta(t)} dt \right| \le \frac{1}{T} \left(\int_{-T}^T |P_\sigma|^2 dt\right)^{1/2} \left(\int_{-T}^T |\Delta|^2 dt\right)^{1/2} \le \frac{\sqrt{2T M_\sigma^2} \|\Delta\|_{L^2}}{T} = \frac{\sqrt{2} M_\sigma \|\Delta\|_{L^2}}{\sqrt{T}} \to 0.$$
     Alternatively, via $L^1$ resolvent growth:
     $$\int_{-T}^T |r_j(t)| dt = \int_{-T}^T \frac{dt}{\sqrt{a_j^2 + (t-\gamma_j)^2}} \le 2\log\left(\frac{2(T+|\gamma_j|)}{a_j} + 1\right) = O(\log T),$$
     yielding $\frac{1}{2T}\int_{-T}^T |P_\sigma| |\Delta| dt \le \frac{M_\sigma}{2T} O(\log T) = O\left(\frac{\log T}{T}\right) \to 0$.
Summing both terms establishes the limit $0$. $\blacksquare$

**Corollary (Extension to Zero Configurations)**:
The Invisibility Theorem applies to:
- Every single off-line zero resolvent;
- Every fixed finite conjugate pair $\{\delta \pm i\gamma\}$;
- Every fixed finite same-height functional-reflection pair $\{\pm\delta + i\gamma\}$;
- Every fixed finite symmetric quartet $\{\pm\delta \pm i\gamma\}$.

**Fundamental Conclusion**:
$$\boxed{\text{A fixed finite divisor perturbation cannot produce a nonzero normalized infinite mean response.}}$$

### 9.6 The Exact Open Growing-Perturbation Obligation

Because fixed finite perturbations are invisible under normalized infinite averaging, any non-trivial cofinal response requires an infinite growing perturbation $\Delta_{H(T)}(t)$ along a schedule $H(T) \to \infty$.

**The Live Obligation (`OBL-CMSA-003-G4-BOUNDARY`)**:
Formulate and evaluate the cofinal limit:
$$\mathcal D_{\mathrm{cofinal}} = \lim_{T\to\infty} \frac{1}{2T} \int_{-T}^T \left( \left| P_\sigma(t) - Z_{H(T),\delta}(t) + R_{H(T),0}(t) \right|^2 - \left| P_\sigma(t) - Z_{H(T),0}(t) + R_{H(T),0}(t) \right|^2 \right) dt,$$
which requires resolving:
1. **Uniform $L^2$ control on growing zero clusters**: $\sum_{|\gamma_j| \le H(T)} (\dots)$ as $H(T) \to \infty$.
2. **Unequal-height off-diagonal terms**: Phase cancellation $\sum_{j \ne k} \int_{-T}^T \frac{dt}{(a+i(t-\gamma_j))(a-i(t-\gamma_k))}$.
3. **Reflection-pair terms**: Exact symmetry preservation between $\gamma$ and $-\gamma$.
4. **Dependence on schedule $H(T)$**: Stability across grade-covariant schedules $H(T) = cT$ and periodic modulations.
5. **Arithmetic evaluation**: Exact non-zero coupling with the prime Dirichlet polynomial.
6. **Grade covariance**: Covariance under origin dilation $s_K = \tau^K s$.
7. **Global sign**: Determining whether the full infinite limit preserves strict radial positivity ($\Delta \mathcal S > 0 \iff \delta \ne 0$) without collapsing to 0 or reducing to the finite Fejér witness.
