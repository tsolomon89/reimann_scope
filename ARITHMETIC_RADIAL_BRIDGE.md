# Arithmetic Radial Bridge Specification and Candidate Evaluation

## 1. Executive Summary

This document establishes the canonical mathematical specification, obligation structure, candidate registry, and epistemic firewalls for the **Arithmetic Radial Bridge** in the Riemann Scope research program.

The objective of the arithmetic radial bridge is to construct an exact, divisor-independent bridge from the arithmetic structure of the Riemann zeta function (prime powers, the von Mangoldt function $\Lambda(n)$, the Euler product, the pole at $s=1$, the gamma factor, and transcendental continuation $\mathcal Z_\tau(s,K)=\zeta(\tau^{-K}s)$) to a positive radial-defect invariant ($D = -\log L_Q$, $T = \operatorname{Tr}\mathcal R$, or the weighted regularized target $T_a$).

Every candidate is evaluated against strict falsification controls:
- **No Circularity**: Arithmetic quantities must never be defined by reference to zero lists, projected ordinates, $\Xi^\flat$, $Q$, $L_Q$, or $\mathcal R$.
- **Covariance $\ne$ Rigidity**: Invariant transport under bilateral grades $K \in \mathbb Z$ is proved to be fully compatible with off-line zeros ($\delta \ne 0$) via the Covariance Countermodel (§6). Invariant transport alone cannot force $\delta = 0$ without an independent arithmetic zero-valued anchor.
- **Pair Isolation**: Any bilinear or quadratic arithmetic explicit formula must isolate reflection pairs $(\lambda, \lambda^\#)$ without contamination from unrestricted all-pairs cross-terms.

---

## 2. Spectral Targets and Definitions

For every nontrivial zero orbit of $\zeta(s)$, write the centered coordinates as:
$$\lambda_j = \delta_j + i\gamma_j, \qquad \lambda_j^\# = -\overline{\lambda_j} = -\delta_j + i\gamma_j, \qquad r_j = \frac{\delta_j^2}{\gamma_j^2} \ge 0,$$
with orbit multiplicity $n_j > 0$ and $\gamma_j > 0$.

The rational involution pairing kernel
$$\kappa_1(z, w) = \frac{4zw}{(z+w)^2} - 1$$
satisfies the exact algebraic identity
$$\kappa_1(\lambda_j, \lambda_j^\#) = \frac{4(-\delta_j^2 - \gamma_j^2)}{(2i\gamma_j)^2} - 1 = \frac{4(\delta_j^2+\gamma_j^2)}{4\gamma_j^2} - 1 = \frac{\delta_j^2}{\gamma_j^2} = r_j.$$

### 2.1 Determinant Target ($D$)
$$D := -\log L_Q = \log \det_{\mathrm F}(I + \mathcal R) = \sum_j 2n_j \log(1 + r_j) = \sum_j 2n_j \log\left(1 + \frac{\delta_j^2}{\gamma_j^2}\right).$$
The primary candidate bridge equality is:
$$\mathfrak A_{K,D}^{\mathrm{arith}} = D.$$

### 2.2 Trace Target ($T$)
$$T := \operatorname{Tr}\mathcal R = \sum_{\lambda \in \Lambda^+} \frac{\delta_\lambda^2}{\gamma_\lambda^2} = \sum_j 2n_j r_j = \sum_j 2n_j \frac{\delta_j^2}{\gamma_j^2}.$$
Its candidate bridge equality is:
$$\mathfrak A_{K,T}^{\mathrm{arith}} = T.$$

$T$ and $D$ are distinct positive spectral invariants with identical zero sets:
$$D = 0 \iff L_Q = 1 \iff \mathrm{RH}, \qquad T = 0 \iff \mathrm{RH}.$$

### 2.3 Regularized Weighted Target ($T_a$)
For $a > 0$, the weighted trace detector is:
$$T_a := \sum_{\lambda \in \Lambda^+} w_a(\lambda) \kappa_1(\lambda, \lambda^\#) = \sum_{\lambda \in \Lambda^+} w_a(\lambda) \frac{\delta_\lambda^2}{\gamma_\lambda^2}, \qquad w_a(\lambda) = m_\lambda e^{-a \gamma_\lambda^2} > 0.$$
Because $w_a(\lambda) > 0$ for all $\lambda \in \Lambda^+$, $T_a \ge 0$, and $T_a = 0 \iff \forall \lambda \in \Lambda^+, \delta_\lambda = 0 \iff \mathrm{RH}$.

### 2.4 Separated Sesquilinear Signal Target ($S_K$)
Instead of constructing projected divisors explicitly, the **Separated Sesquilinear Signal** direction begins with an arithmetic object and evaluates its frequency-projected spectral representation:
$$S_K(x,t) = \sum_{\lambda} a_K(\gamma_\lambda) e^{x\delta_\lambda} e^{it\gamma_\lambda},$$
or an equivalent two-slot quadratic form, where:
- $x$ probes radial amplitude displacement $\delta$;
- $t$ performs implicit frequency projection over ordinates $\gamma$;
- $a_K$ provides spectral decay;
- $K \in \mathbb Z$ is the transcendental continuation grade.

At a fixed ordinate $\gamma$, functional reflection yields a symmetric radial multiset $\Delta_\gamma = \{\delta_{\gamma,1}, \dots, \delta_{\gamma,N_\gamma}\}$ with $\sum_a \delta_{\gamma,a} = 0$.
When the coefficients satisfy $\sum_\lambda |a_K(\lambda)| < \infty$ ($\ell^1$ absolute summability), the double sum converges absolutely, and dominated convergence justifies the translation-average limit directly without requiring Montgomery pair correlation:
$$M_K(x) := \lim_{T\to\infty} \frac{1}{2T} \int_{-T}^T |S_K(x, t)|^2 dt = \sum_\gamma |a_K(\gamma)|^2 \left| \sum_{a=1}^{N_\gamma} e^{x\delta_{\gamma,a}} \right|^2.$$
Differentiating twice at $x=0$ yields the exact nonnegative curvature:
$$M_K''(0) = 2 \sum_\gamma |a_K(\gamma)|^2 N_\gamma \sum_{a=1}^{N_\gamma} \delta_{\gamma,a}^2 = \sum_\gamma W_K(\gamma) \sum_{a=1}^{N_\gamma} \delta_{\gamma,a}^2 \ge 0,$$
where $W_K(\gamma) = 2 |a_K(\gamma)|^2 N_\gamma > 0$.
Because $W_K(\gamma) > 0$ strictly:
$$M_K''(0) = 0 \iff \forall \lambda, \delta_\lambda = 0 \iff \mathrm{RH}.$$
This achieves implicit frequency projection without explicit projected-divisor construction.

---

## 3. Strict Arithmetic Input Firewall

A valid arithmetic bridge construction $\mathfrak A_{K,X}^{\mathrm{arith}}$ may use:
1. Prime powers and the von Mangoldt function $\Lambda(n)$;
2. The Euler product where $\Re(s) > 1$;
3. The pole of $\zeta(s)$ at $s=1$;
4. Archimedean gamma factors $\Gamma_{\mathbb R}(s) = \pi^{-s/2}\Gamma(s/2)$;
5. The functional equation $\xi(s) = \xi(1-s)$;
6. Proved reality and Schwarz reflection properties of $\xi$;
7. Admissible even test functions $H \in \mathcal S(\mathbb R)$;
8. Bilateral integer grades $K \in \mathbb Z$ and transcendental continuation $\mathcal Z_\tau(s,K) = \zeta(\tau^{-K} s)$.

**Strict Epistemic Firewall**:
The definition of $\mathfrak A_{K,X}^{\mathrm{arith}}$ MUST NOT use:
- Nontrivial zero lists or ordinates;
- Coordinates $\delta_j, \gamma_j$ or $\lambda_j^\#$;
- Projected ordinates $1/2 + i\gamma_j$ or the projected divisor $\mathcal P_0(\mathcal D_\zeta)$;
- The projected xi function $\Xi^\flat(z)$;
- The defect quotient $Q(z)$ or limiting invariant $L_Q$;
- The radial operator $\mathcal R$;
- Definitions by reference to $D$ or $T$;
- Any circular assumption equivalent to RH.

---

## 4. Baseline Mathematical Audit, Grade Centering, and Obstruction Scopes

### 4.1 Grade-Centering Geometry
Under coordinate dilation $s_K = \tau^K s$, the critical line $\Re(s) = 1/2$ maps to $\Re(s_K) = \tau^K / 2$.
The correct grade center is:
$$c_K := \frac{\tau^K}{2}.$$
With centered coordinate $z = s - 1/2$, the centered grade coordinate is:
$$z_K := s_K - c_K = \tau^K s - \frac{\tau^K}{2} = \tau^K \left(s - \frac{1}{2}\right) = \tau^K z.$$
The correctly centered completed xi function at grade $K$ is:
$$\Xi_K(z_K) := \xi\left(\frac{1}{2} + \tau^{-K} z_K\right),$$
which satisfies the exact pullback identity:
$$\Xi_K(\tau^K z) = \Xi_0(z) = \xi\left(\frac{1}{2} + z\right).$$
The normalized radial ratio is strictly grade-invariant:
$$\frac{(\tau^K \delta)^2}{(\tau^K \gamma)^2} = \frac{\delta^2}{\gamma^2} = r.$$
Therefore $D$, $T$, and the radial spectrum are identically invariant under bilateral grade transport.

### 4.2 Multiplicity Convention
Let $\Lambda^+$ denote the multiset of upper-half-plane zeros of $\zeta(s)$ ($\Im(s) > 0$).
At a distinct ordinate $\gamma_j > 0$:
- On-line zeros ($s = 1/2 + i\gamma_j$) have multiplicity $m_{0,j} \ge 0$.
- Off-line quartets $\{1/2 \pm \delta_j \pm i\gamma_j\}$ ($\delta_j > 0$) have quartet multiplicity $n_j \ge 0$.
- Total upper-half-plane multiplicity at height $\gamma_j$: $m_j = m_{0,j} + 2n_j$.
- In $L_Q = \prod_j (1 + r_j)^{-2n_j}$, the exponent $2n_j$ correctly reflects the two upper-half zeros in each quartet.
- In $T = \operatorname{Tr}\mathcal R = \sum_j 2n_j r_j$, on-line zeros contribute $r = 0$, while each off-line quartet contributes $2n_j r_j$.

### 4.3 Obstruction Scopes
1. **Classical 1-Point Weight Obstruction (Q-023)**:
   Excludes the weight-2 radial trace from the proved class of direct 1-point linear statistics $\sum_\rho H(\rho)$. It does not exclude nonlinear sesquilinear constructions.
2. **Cramér Mean-Square Obstruction**:
   The raw unsmoothed signal $x^{\rho-1/2} = e^{\delta \log x} e^{i\gamma \log x}$ uses a single parameter for both amplitude and frequency. If $\delta \ne 0$, its mean-square growth rate is governed by $\Theta = \sup_\rho \Re\rho$, rendering $\Theta$-dependent normalizations circular (`CRAMER_TYPE_OBSTRUCTION`).
3. **Pair Correlation Scope**:
   If spectral coefficients satisfy $\sum_\lambda |a_K(\lambda)| < \infty$, the double sum converges absolutely, and dominated convergence justifies the translation average limit directly. Montgomery-type pair correlation is relevant only when coefficients lack $\ell^1$ domination.

---

## 5. Formal Bridge Obligations

Stable obligation identifiers govern the formalization of the arithmetic radial bridge:

### Determinant Route
- $\mathrm{ARB\text{-}D1}$: Divisor-independent arithmetic construction $\mathfrak A_{K,D}^{\mathrm{arith}}$ [`OPEN`].
- $\mathrm{ARB\text{-}D2}$: Exact arithmetic/spectral identity $\mathfrak A_{K,D}^{\mathrm{arith}} = D$ [`OPEN`].
- $\mathrm{ARB\text{-}D3}$: Independent arithmetic vanishing $\mathfrak A_{K,D}^{\mathrm{arith}} = 0$ or grade boundary $\lim_{K\to+\infty}\mathfrak A_{K,D}^{\mathrm{arith}} = 0$ [`OPEN`].
- $\mathrm{ARB\text{-}D4}$: Rigidity implication $D = 0 \implies \forall j, r_j = 0$ [`FORMALLY_PROVED` in Lean 4].

### Trace Route
- $\mathrm{ARB\text{-}T1}$: Divisor-independent arithmetic construction $\mathfrak A_{K,T}^{\mathrm{arith}}$ [`OPEN`].
- $\mathrm{ARB\text{-}T2}$: Exact arithmetic/spectral identity $\mathfrak A_{K,T}^{\mathrm{arith}} = T$ [`OPEN`].
- $\mathrm{ARB\text{-}T3}$: Independent arithmetic vanishing $\mathfrak A_{K,T}^{\mathrm{arith}} = 0$ or grade boundary $\lim_{K\to+\infty}\mathfrak A_{K,T}^{\mathrm{arith}} = 0$ [`OPEN`].
- $\mathrm{ARB\text{-}T4}$: Rigidity implication $T = 0 \implies \forall j, r_j = 0$ [`FORMALLY_PROVED` in Lean 4].

### Separated Signal Route
- $\mathrm{ARB\text{-}SS1}$: Divisor-independent arithmetic signal $S_K^{\mathrm{arith}}(x, t)$ [`OPEN`].
- $\mathrm{ARB\text{-}SS2}$: Exact radial/frequency separation $a_K(\gamma) e^{x\delta} e^{it\gamma}$ [`FALSIFIED` for SS-1..SS-5].
- $\mathrm{ARB\text{-}SS3}$: Finite algebraic curvature identity $\left.\partial_x^2 |\sum e^{x\delta_a}|^2\right|_{x=0} = 2N\sum \delta_a^2$ [`FORMALLY_PROVED` in Lean 4].
- $\mathrm{ARB\text{-}SS4}$: Curvature rigidity $M_K''(0) = 0 \implies \forall \lambda, \delta_\lambda = 0$ [`FORMALLY_PROVED` in Lean 4].

### Structural Obligations
- $\mathrm{ARB\text{-}STRUCT\text{-}SUM}$: Infinite summability of $T$ and $D$ [`PROVED` under Hadamard order 1].
- $\mathrm{ARB\text{-}STRUCT\text{-}PAIR}$: Isolation of involution pairs $(\lambda, \lambda^\#)$ without off-diagonal contamination [`OPEN`].
- $\mathrm{ARB\text{-}STRUCT\text{-}NONRED}$: Grade non-redundancy (excluding coordinate pullback) [`PROVED`].
- $\mathrm{ARB\text{-}STRUCT\text{-}UNIF}$: Uniformity of grade limits and exclusion of raw coordinate compression [`PROVED`].
- $\mathrm{ARB\text{-}STRUCT\text{-}RH}$: Connection from $\forall j, \delta_j = 0$ to project RH predicate [`FORMALLY_PROVED` in Lean 4].

---

## 6. Covariance Countermodel (Covariance $\ne$ Rigidity)

To prove that coordinate covariance and functional equation symmetries alone do not force $\delta = 0$, we construct the **Covariance Countermodel**:
Consider an abstract off-line quartet:
$$\mathcal Q_{\delta, \gamma} = \left\{\frac{1}{2} + \delta + i\gamma, \, \frac{1}{2} - \delta + i\gamma, \, \frac{1}{2} + \delta - i\gamma, \, \frac{1}{2} - \delta - i\gamma\right\}, \qquad \delta \ne 0, \gamma > 0.$$

This quartet satisfies:
1. **Reflection symmetry**: $s \in \mathcal Q_{\delta,\gamma} \implies 1-s \in \mathcal Q_{\delta,\gamma}$.
2. **Complex conjugation**: $s \in \mathcal Q_{\delta,\gamma} \implies \bar s \in \mathcal Q_{\delta,\gamma}$.
3. **Involution pairing**: $s \in \mathcal Q_{\delta,\gamma} \implies (1-\bar s) \in \mathcal Q_{\delta,\gamma}$.
4. **Bilateral transport**: Under $s \mapsto \tau^K s$, the centered ratio $(\tau^K\delta)^2/(\tau^K\gamma)^2 = \delta^2/\gamma^2$ is preserved.
5. **Off-line existence**: $\exists s \in \mathcal Q_{\delta,\gamma}, \Re(s) \ne 1/2$.

**Conclusion**: Reflection laws and grade transport covariance are jointly compatible with $\delta \ne 0$. Invariant transport does not imply vanishing without an independent arithmetic anchor $\mathfrak A_K = 0$.

This countermodel is formalized and verified in Lean 4 (`RiemannScope.covariance_countermodel_offline_compatible`).

---

## 7. Candidate Registry and Falsification Matrix

### 7.1 Classical Bridge Candidates (A–G)

| Candidate ID | Name | Target | Derivation Status | Pair Isolation | Earliest Failure / Obstruction | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CANDIDATE_A** | Linear Grade Differences | None | `PROVED_COLLAPSE` | False | Collapses to native explicit formula $\mathcal C_0[H \circ \tau^K] - \mathcal C_0[H]$; produces only 1-point direct sums; no pair isolation. | `FALSIFIED_FOR_BRIDGE` |
| **CANDIDATE_B** | Bilinear Cross-Grade Explicit Formula | Trace / Det | `DERIVED_OBSTRUCTED` | False | $D_K(s)\overline{D_L(s)}$ produces an unrestricted double sum over all zero pairs $(\rho_1, \rho_2)$; off-diagonal cross-terms dominate. | `FALSIFIED_FOR_PAIR_ISOLATION` |
| **CANDIDATE_C** | Tensor-Square Trace Identity | Trace | `OBSTRUCTED` | False | Doubled explicit formula sums over all zero pairs; selecting diagonal involution pair requires zero-divisor projection. | `FALSIFIED_FOR_PAIR_ISOLATION` |
| **CANDIDATE_D** | Log-Derivative Contour Identity | Determinant | `OBSTRUCTED` | False | Contour residue expansion generates cross-terms; fails pair isolation without divisor subtraction. | `FALSIFIED_FOR_PAIR_ISOLATION` |
| **CANDIDATE_E** | Relative Determinant from Arithmetic Data | Determinant ($D$) | `UNPROVED_BRIDGE` | True | Operator on Dirichlet polynomials matching $\det_{\mathrm F}(I+\mathcal R)$ without zero-divisor input lacks construction. | `OPEN_UNPROVED` |
| **CANDIDATE_F** | Grade-Indexed Prime-Power Pairing | Trace ($T$) | `UNPROVED_BRIDGE` | True | Prime-power kernel producing $\delta^2/\gamma^2$ without cross-term contamination lacks closed-form derivation. | `OPEN_UNPROVED` |
| **CANDIDATE_G** | Weighted Regularized Radial Bridge | Weighted ($T_a$) | `SPECTRAL_PROVED_ARITH_OPEN` | True | Spectral detector $T_a > 0 \iff \delta \ne 0$ is rigorously proved; arithmetic realization $\mathfrak A_{K,a}^{\mathrm{arith}}$ remains open. | `LIVE_UNDERIVED` |

### 7.2 Separated Sesquilinear Signal Candidates (SS-1–SS-5)

| Candidate ID | Name | Target | Gate Status | Earliest Failed Gate | Structural Obstruction / Witness | Final Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CANDIDATE_SS1** | Conjugated Explicit-Formula Pair | Separated Signal | `FALSIFIED_GATE_2` | Gate 2 (Separation) | **Holomorphic Rigidity / Cramér Obstruction**: $\partial_\delta \Re(\log h) - \partial_\gamma \Im(\log h) = x - t \ne 0$ unless $x=t$. Holomorphic kernel $e^{(x+it)z}$ produces $e^{x\delta - t\gamma}$, inducing exponential translation divergence $\sinh(2T\gamma)/\gamma$. | `FAIL_CRAMER_TYPE_NORMALIZATION` |
| **CANDIDATE_SS2** | Two-Slot Logarithmic Derivative | Bilinear Form | `FALSIFIED_GATE_2_3` | Gate 2 & 3 (Cross-terms) | **Double-Sum Cross-Term Dominance**: $D_K(s_1)\overline{D_K(s_2)}$ yields double sum over all zero pairs $(\rho_1, \rho_2)$. Off-diagonal terms scale as $O((T\log T)^2)$ against $O(T\log T)$ diagonal and do not cancel under translation averaging. | `FAIL_OFF_DIAGONAL_CROSS_TERM_DOMINANCE` |
| **CANDIDATE_SS3** | Rapidly Smoothed Transform | Smoothed Signal | `FALSIFIED_GATE_2` | Gate 2 (Separation) | **Cramér-Type Translation Divergence**: Gaussian smoothing leaves $-t\gamma$ in the real exponential slot. Translation average $\int_{-T}^T e^{-2t\gamma}dt = \sinh(2T\gamma)/\gamma$ diverges exponentially as $T\to\infty$ ($>10^{240}$ for $\gamma \approx 14.13, T=20$). Normalization requires circular $\Theta = \sup \Re\rho$. | `FAIL_CRAMER_TYPE_NORMALIZATION` |
| **CANDIDATE_SS4** | Cross-Grade Sesquilinear Form | Cross-Grade Coupling | `FALSIFIED_GATE_5` | Gate 5 (Grade Nonredundancy) | **Transcendental Non-Resonance & Coordinate Pullback**: For $K \ne L$, $\tau^{-K}\log n \ne \tau^{-L}\log m$ because $\tau = 2\pi$ is transcendental, yielding zero cross-grade arithmetic resonance. Single-grade sums collapse to grade-zero pullbacks by coordinate covariance ($z_K = \tau^K z$). | `GRADE_COORDINATE_REDUNDANT` |
| **CANDIDATE_SS5** | Direct Positive Quadratic Kernel | Quadratic Form | `FALSIFIED_GATE_1_6` | Gate 1 & 6 (Holomorphy/Anchor) | **Non-Holomorphic Firewall / Identity Theorem**: Any holomorphic kernel vanishing on $\Re(s)=1/2$ vanishes identically everywhere on $\mathbb C^2$. Non-holomorphic pairing $\rho - \rho^\# = 2\delta$ couples $\rho$ with $1-\bar\rho$, which cannot be pulled back to Dirichlet series via Cauchy residue calculus. | `FAIL_NON_HOLOMORPHIC_ARITHMETIC_FIREWALL` |

---

## 8. Lean 4 Formalization Inventory

The formalization in `formal/RiemannScope/` contains the following compiled theorems (0 `sorry`, 0 axioms):

1. **`RiemannScope.centeredGradeCoord_eq_tau_pow_mul_z`**:
   Exact centered grade dilation: $z_K = s_K - c_K = \tau^K (s - 1/2)$.
2. **`RiemannScope.list_weighted_sum_nonneg_eq_zero_iff`**:
   General arbitrary-family weighted positivity firewall: for any positive weight list $w$ and non-negative defect list $l$, $\sum w_i l_i = 0 \iff \forall i, l_i = 0$.
3. **`RiemannScope.offlineQuartet_reflection`**:
   Off-line quartet is closed under functional equation reflection $s \mapsto 1-s$.
4. **`RiemannScope.offlineQuartet_conj`**:
   Off-line quartet is closed under complex conjugation $s \mapsto \bar s$.
5. **`RiemannScope.covariance_countermodel_offline_compatible`**:
   Proves covariance, reflection, and conjugation symmetries are jointly compatible with $\delta \ne 0$.
6. **`RiemannScope.ConditionalArithmeticRadialBridge.all_defects_zero`**:
   Rigidity theorem: under any valid conditional arithmetic bridge, all represented zero defects vanish ($r_j = 0 \implies \delta_j = 0$).
7. **`RiemannScope.sum_pairs_sq_two_terms` & `curvature_pair_symmetric`**:
   Exact 2-term algebraic curvature identity: $\sum_{a,b=1}^2 (\delta_a + \delta_b)^2 = 2 \cdot 2 \cdot (\delta_1^2 + \delta_2^2) = 4 (\delta_1^2 + \delta_2^2)$ under $\delta_1 + \delta_2 = 0$.
8. **`RiemannScope.sum_pairs_sq_four_terms` & `curvature_quartet_symmetric`**:
   Exact 4-term algebraic curvature identity: $\sum_{a,b=1}^4 (\delta_a + \delta_b)^2 = 2 \cdot 4 \cdot \sum_{a=1}^4 \delta_a^2 = 8 \sum_{a=1}^4 \delta_a^2$ under $\sum_{a=1}^4 \delta_a = 0$.
9. **`RiemannScope.offline_quartet_curvature_val`**:
   Off-line quartet exact curvature reduction to $32 \delta^2$, strictly positive for $\delta \ne 0$.
10. **`RiemannScope.ConditionalSeparatedSignalBridge.all_variances_zero`**:
    Separated Signal Bridge Rigidity Theorem: under any arithmetic-anchored separated signal bridge, all represented radial variances vanish, forcing $\delta = 0$.

---

## 9. Current Status and Research Protocol

- **`OBL-RDQ-001`**: Remains **OPEN**.
- **Separated Signal Sprint Outcome**:
  - The spectral side of the separated signal $S_K(x, t)$ rigorously detects off-line zeros with positive curvature $M_K''(0) > 0 \iff \delta \ne 0$ without requiring Montgomery pair correlation when $\ell^1$-summable.
  - However, Candidates SS-1 through SS-5 are rigorously falsified on the arithmetic side by Holomorphic Rigidity (SS-1), Double-Sum Cross-Term Dominance (SS-2), Cramér Translation Divergence (SS-3), Transcendental Grade Non-Resonance (SS-4), and the Non-Holomorphic Arithmetic Firewall (SS-5).
- **Announcement Protocol**: Adheres strictly to Rule 01 (Mathematical Rigor Protocol). No proof of RH is announced.
