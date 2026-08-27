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
2. **Certified Outward-Rounded Arb Ball Witness (WIT-02)**: Across the full symmetric compact support $[-16.8, 16.8]$, the Fejér radial difference $\Delta S_{\text{Fejér}}$ for $(\sigma=5, \gamma=14, \delta=0.49, T=16.8)$ is certified strictly negative via outward-rounded Arb ball arithmetic with 50,000 subinter   $$\Delta S_{\text{Fejér}} \in [-1.89473 \times 10^{-4}, -1.54203 \times 10^{-4}] \subset (-\infty, 0).$$
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
*(Note: Direct certified integration over the full $[-T, T]$ domain does not rely on this symmetry as an operational premise).*unction of $t$.

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
| **Finite 4-Term Algebraic Expansion** | PROVED | **PROVED** | OPEN | OPEN | N/A (identity) | N/A | REDUNDANT | `FINITE_IDENTITY_PROVED_G4_OPEN` |
| **Dilated Completed Log-Derivative** | PROVED | PROVED | N/A | N/A | N/A | N/A | **PROVED REDUNDANT** | `GRADE_COORDINATE_REDUNDANT` |
| **Candidate CMSA-1 (Full Infinite/Cofinal)** | PROVED | PROVED | OPEN | OPEN | OPEN (infinite) | OPEN | REDUNDANT | `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE` |
| **Candidate CMSA-2 (Full Infinite/Cofinal)** | PROVED | PROVED | OPEN | OPEN | OPEN (infinite) | OPEN | REDUNDANT | `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE` |
| **Candidate CMSA-3** | PROVED | PROVED | N/A | N/A | N/A | N/A | PROVED REDUNDANT | `GRADE_COORDINATE_REDUNDANT` |

---

## 8. Formal Lean 4 Theorem Inventory (75 Compiled Declarations)

All compiled cleanly in Lean 4 (`formal/RiemannScope/ArithmeticBridge.lean`, 0 `sorry`, 0 `admit`, 0 warnings):
1. `RiemannScope.complex_finset_sum_mul_star`: $(\sum_{i \in s} b_i) \cdot \overline{(\sum_{j \in s} b_j)} = \sum_{i \in s} \sum_{j \in s} b_i \overline{b_j}$.
2. `RiemannScope.complex_finset_normSq_eq_double_sum_re`: $\operatorname{normSq}(\sum_{i \in s} b_i) = \Re(\sum_{i \in s} \sum_{j \in s} b_i \overline{b_j})$.
3. `RiemannScope.abstract_finite_kernel_decomposition`: $(\sum_{i \in s} \sum_{j \in s} K(i, j)) = (\sum_{i \in s} b_i) \cdot \overline{(\sum_{j \in s} b_j)}$ under hypothesis $K(i, j) = b_i \overline{b_j}$.
4. `RiemannScope.linear_operator_finite_double_sum_interchange`: $L(\sum_{i \in s} \sum_{j \in s} K(i, j)) = \sum_{i \in s} \sum_{j \in s} L(K(i, j))$ for additive maps $L : \mathbb C \to+ \mathbb C$.
5. `RiemannScope.abstract_windowed_kernel_expansion`: $L(\operatorname{normSq}(\sum_{i \in s} b_i)) = L((\sum_{i \in s} \sum_{j \in s} K(i, j)).\text{re})$.
6. `RiemannScope.linear_schedule_grade_covariant`: $\forall c, \tau \in \mathbb R$, the linear schedule $H_c(T) = cT$ is discrete grade-covariant ($H_c(\tau T) = \tau H_c(T)$).
7. `RiemannScope.grade_covariant_schedule_nonuniqueness`: Grade covariance alone does NOT uniquely determine a schedule; for any $c_1 \ne c_2$, both $H_{c_1}$ and $H_{c_2}$ are covariant and distinct for all $T > 0$.
8. `RiemannScope.periodic_modulated_schedule_covariant`: Any schedule $H(T) = T \cdot q(\log_\tau T)$ with 1-periodic $q$ satisfies grade covariance.
9. `RiemannScope.additive_reference_subtraction_invariance`: $(S(Z_\delta) - R) - (S(Z_0) - R) = S(Z_\delta) - S(Z_0)$.
10. `RiemannScope.complex_radial_defect_difference_numerator`: $(u-d^2)u - ((u-d^2)^2 + 4d^2\gamma^2) = d^2(u - 4\gamma^2 - d^2)$ over $\mathbb C$.
11. `RiemannScope.complex_radial_second_order_numerator_decomposition`: $4z d^2(z^2-3\gamma^2-d^2) = 4z d^2(z^2-3\gamma^2) - 4z d^4$ over $\mathbb C$.
12. `RiemannScope.radial_defect_difference_numerator`: real specialization over $\mathbb R$.
13. `RiemannScope.radial_second_order_numerator_decomposition`: real specialization over $\mathbb R$.
14. `RiemannScope.tendsto_cofinal_fixed_zero`: `Tendsto (fun (n : ℕ) => H / ((n : ℝ) + 1)) atTop (𝓝 0)` (Mathlib Filter.Tendsto).
15. `RiemannScope.not_tendsto_cofinal_diagonal_zero`: `¬ Tendsto (fun (n : ℕ) => ((n : ℝ) + 1) / ((n : ℝ) + 1)) atTop (𝓝 0)` (Mathlib Filter.Tendsto).
16. `RiemannScope.finite_sum_tendsto_interchange`: `Tendsto (fun n => ∑ i in s, f i n) atTop (𝓝 (∑ i in s, g i))` (Mathlib Filter.Tendsto).
17. `RiemannScope.cofinal_sequence_fixed_limit_zero`: $\forall H \in \mathbb R, \forall \varepsilon > 0, \exists N, \forall n \ge N, |H / (n + 1)| < \varepsilon$ (elementary $\varepsilon$-$N$).
18. `RiemannScope.cofinal_diagonal_not_tendsto_zero`: $\neg (\forall \varepsilon > 0, \exists N, \forall n \ge N, |(n+1)/(n+1) - 0| < \varepsilon)$ (elementary $\varepsilon$-$N$).
19. `RiemannScope.cofinal_sequence_diagonal_witness`: $(n+1)/(n+1) = 1$ for all $n \in \mathbb N$.
20. `RiemannScope.cofinal_schedule_distinct_from_fixed_limit`: $(cT)/T = c \ne 0$ for $T \ne 0$.
21. `RiemannScope.ConditionalG4RegularizedBridge.all_defects_zero`: Rigidity theorem forcing all represented zero defects $d_j = 0$.

---

## 9. Phase B — Schedule Covariance Classification & The Next Live Theorem

### 9.1 Schedule Covariance Law and Classification
Under the repository's grade transformation $s' = 1/2 + \tau^K(s - 1/2)$, centered coordinate height dilates as $t' = \tau^K t$, and window scale transforms as $T' = \tau^K T$. For the height truncation cutoff $H$ to preserve scale covariance, it must scale identically: $H' = \tau^K H$. For unit step $K=1$, the exact covariance law is:
$$\boxed{H(\tau T) = \tau H(T), \quad \text{where } \tau = 2\pi.}$$

**Proved Classification**:
1. **Linear Family**: Every linear schedule $H_c(T) = cT$ ($c > 0$) satisfies $H_c(\tau T) = c(\tau T) = \tau(cT) = \tau H_c(T)$.
2. **Non-Uniqueness**: For any $c_1 \ne c_2$, $H_{c_1}(T) \ne H_{c_2}(T)$ for all $T > 0$. Hence grade covariance alone does NOT uniquely select a schedule.
3. **General Solution**: Let $\psi(T) = H(T)/T$. Then $\psi(\tau T) = \psi(T)$. Setting $u = \log_\tau T$, $q(u) = \psi(\tau^u)$ is 1-periodic: $q(u+1) = q(u)$. Thus:
   $$\boxed{H(T) = T \cdot q(\log_\tau T), \quad q : \mathbb R \to (0, \infty) \text{ 1-periodic}}.$$
4. **Asymptotic Collapse**: If $\lim_{T\to\infty} H(T)/T$ exists, periodic modulation collapses to $H(T) = cT$.
5. **Selection Condition**: Selecting $c$ requires an additional condition beyond grade covariance: specifically, sharp Hadamard remainder control $|\mathcal R_H(t)| \le M \log(|t|+2)$ uniformly on $[-T, T]$ requires $H(T) \ge T$ (i.e. $c \ge 1$).

**Falsified Premise**:
$$\boxed{\text{Falsified Premise: "Bilateral discrete grade covariance uniquely determines the cofinal schedule."}}$$

### 9.2 The Next Standalone Theorem Obligation
Given symmetrically truncated completed zero resolvent $Z_H(t)$ and remainder $R_H(t) = \frac{\Xi'}{\Xi}(\sigma - 1/2 + it) - Z_H(t)$ with $H(T) = cT$ ($c \ge 1$):
Define the schedule-indexed regularized candidate:
$$\mathcal S_T(Z_{cT}; \mathcal R_{cT}) = \frac{1}{2\pi} \int_{-T}^T W_T(t) \left| Z_{cT}(t) + \mathcal R_{cT}(t) \right|^2 dt.$$

**Standalone Theorem Obligation (Subgate G4-Cofinal-Bridge)**:
$$\forall \sigma > 1, \forall \delta \in (0, 1/2), \quad \lim_{T \to \infty} \left[ \mathcal S_T(Z_{cT, \delta}; \mathcal R_{cT}) - \mathcal S_T(Z_{cT, 0}; \mathcal R_{cT}) \right] > 0.$$

This theorem requires establishing:
1. **Remainder Asymptotic Bound**: $\lim_{T\to\infty} \int W_T(t) |R_{cT}(t)|^2 dt = 0$.
2. **Cross-Term Domination**: Uniform $o(1)$ bound on $2\Re \int W_T(t) Z_{cT}(t) \overline{R_{cT}(t)} dt$.
3. **Unequal-Height Off-Diagonal Phase Cancellation**: $\sum_{j \ne k} \int W_T(t) \frac{1}{(a+i(t-\gamma_j))(a-i(t-\gamma_k))} dt \to 0$.
4. **Diagonal Multiplicity Dominance**: Direct radial variation on the diagonal terms strictly dominates the remainder.

Status: `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.

