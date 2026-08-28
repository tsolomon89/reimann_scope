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

At a fixed ordinate $\gamma > 0$, functional reflection yields a symmetric upper-half-plane radial multiset $\Delta_\gamma = \{\delta_{\gamma,1}, \dots, \delta_{\gamma,N_\gamma}\}$ with $\sum_a \delta_{\gamma,a} = 0$.
When the coefficients satisfy $\sum_\lambda |a_K(\lambda)| < \infty$ ($\ell^1$ absolute summability), the double sum converges absolutely, and dominated convergence justifies the translation-average limit directly without requiring Montgomery pair correlation:
$$M_K(x) := \lim_{T\to\infty} \frac{1}{2T} \int_{-T}^T |S_K(x, t)|^2 dt = \sum_\gamma |a_K(\gamma)|^2 \left| \sum_{a=1}^{N_\gamma} e^{x\delta_{\gamma,a}} \right|^2.$$
Differentiating twice at $x=0$ yields the exact nonnegative curvature:
$$M_K''(0) = 2 \sum_\gamma |a_K(\gamma)|^2 N_\gamma \sum_{a=1}^{N_\gamma} \delta_{\gamma,a}^2 = \sum_\gamma W_K(\gamma) \sum_{a=1}^{N_\gamma} \delta_{\gamma,a}^2 \ge 0,$$
where $W_K(\gamma) = 2 |a_K(\gamma)|^2 N_\gamma > 0$.
Because $W_K(\gamma) > 0$ strictly:
$$M_K''(0) = 0 \iff \forall \lambda, \delta_\lambda = 0 \iff \mathrm{RH}.$$
For an off-line quartet at positive height $\gamma > 0$ with multiplicity $n$, the upper fibre $\{\delta, -\delta\}$ has $N = 2n$, giving unnormalized curvature $M_\gamma''(0) = 8 n^2 \delta^2$.
The normalized fibre curvature is:
$$C_\gamma := \frac{M_\gamma''(0)}{2N_\gamma} = \sum_{a=1}^{N_\gamma} \delta_{\gamma,a}^2 = 2n\delta^2,$$
which recovers the trace defect $\sum_{\gamma > 0} C_\gamma / \gamma^2 = \operatorname{Tr}\mathcal R$.
However, normalizing by $2N_\gamma$ requires access to the spectral fibre multiplicity $N_\gamma$.

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
4. **Holomorphic Rigidity Scope**:
   Direct 1-point holomorphic parameter separation $h(\delta+i\gamma) = a(\gamma)e^{x\delta}e^{it\gamma}$ violates Cauchy-Riemann equations on open sets unless $x=t$ and $a'(\gamma)=0$.

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
- $\mathrm{ARB\text{-}SS3}$: Finite algebraic curvature identity $\left.\partial_x^2 |\sum e^{x\delta_a}|^2\right|_{x=0} = 2N\sum \delta_a^2 + 2(\sum \delta_a)^2$ [`FORMALLY_PROVED` in Lean 4].
- $\mathrm{ARB\text{-}SS4}$: Curvature rigidity $M_K''(0) = 0 \implies \forall \lambda, \delta_\lambda = 0$ [`FORMALLY_PROVED` in Lean 4].

### Completed Mean-Square Anchor (CMSA) Route
- $\mathrm{ARB\text{-}CMSA1}$: Exact completed log-derivative decomposition $P(u) = A(u) - \Xi'/\Xi(u-1/2)$ [`PROVED` on $\Re(u) > 1$].
- $\mathrm{ARB\text{-}CMSA2}$: Arithmetic mean-square vanishing anchor $\mathcal A(\sigma) = 0$ [`PROVED` for all $\sigma > 1$].
- $\mathrm{ARB\text{-}CMSA3}$: Complete spectral kernel evaluation without unconstrained cross-term cancellation [`OPEN`].
- $\mathrm{ARB\text{-}CMSA4}$: Rigidity to RH via positive spectral curvature [`OPEN`].

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
| **CANDIDATE_SS1** | Conjugated Explicit-Formula Pair | Separated Signal | `FALSIFIED_GATE_2` | Gate 2 (Separation) | **Direct Holomorphic Parameter Separation Failure**: Cauchy-Riemann equations force $x=t, a'(\gamma)=0$ on open sets. Holomorphic kernel $e^{(x+it)z}$ produces $e^{x\delta - t\gamma}$, inducing exponential translation divergence $\sinh(2T\gamma)/\gamma$. | `FAIL_DIRECT_HOLOMORPHIC_PARAMETER_SEPARATION` |
| **CANDIDATE_SS2** | Two-Slot Logarithmic Derivative | Bilinear Form | `FALSIFIED_GATE_2_3` | Gate 2 & 3 (Cross-terms) | **Unconstrained Double-Sum Resolution Failure**: $D_K(s_1)\overline{D_K(s_2)}$ yields an unrestricted double sum over all zero pairs $(\rho_1, \rho_2)$; involution-pair isolation is not obtained, and limiting off-diagonal cancellation remains unproved. | `FAIL_UNCONSTRAINED_DOUBLE_SUM_WITHOUT_PAIR_ISOLATION` |
| **CANDIDATE_SS3** | Rapidly Smoothed Transform | Smoothed Signal | `FALSIFIED_GATE_2` | Gate 2 (Separation) | **Ordinate Slot Exponential Growth**: Translation parameter enters real exponential slot as $-t\gamma$, causing translation average $\int_{-T}^T e^{-2t\gamma}dt = \sinh(2T\gamma)/\gamma$ to diverge exponentially as $T\to\infty$ ($>10^{240}$ for $\gamma \approx 14.13, T=20$). | `FAIL_ORDINATE_SLOT_EXPONENTIAL_GROWTH` |
| **CANDIDATE_SS4** | Cross-Grade Sesquilinear Form | Cross-Grade Coupling | `FALSIFIED_GATE_5` | Gate 5 (Grade Nonredundancy) | **Transcendental Cross-Grade Scope & Coordinate Redundancy**: Bounded frequency gap searches show no non-trivial resonances up to tested bounds (numerical evidence only; exact non-resonance for $2\pi$ is open). Single-grade sums collapse to grade-zero pullbacks by coordinate covariance ($z_K = \tau^K z$). | `GRADE_COORDINATE_REDUNDANT` |
| **CANDIDATE_SS5** | Direct Positive Quadratic Kernel | Quadratic Form | `FALSIFIED_GATE_1_6` | Gate 1 & 6 (Holomorphy/Anchor) | **Direct One-Point Holomorphic Realization Boundary**: Direct one-point holomorphic realization vanishing on $\Re(s)=1/2$ vanishes identically everywhere on $\mathbb C^2$. Non-holomorphic pairing cannot be directly evaluated via single-point Cauchy residue calculus; nonlinear sesquilinear constructions remain open. | `FAIL_DIRECT_ONE_POINT_HOLOMORPHIC_REALIZATION` |

### 7.3 Completed Mean-Square Anchor Candidates (CMSA-1–CMSA-3)

| Candidate ID | Name | Target | Gate Status | Earliest Failed Gate | Structural Obstruction / Witness | Final Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CANDIDATE_CMSA1** | Base Completed Mean-Square Anchor | $\mathcal A(\sigma) = 0$ | `LIVE_G3_CLOSED_G4_OPEN` | Gate 4 (Infinite Spectral Interchange) | **Non-Uniform Infinite Interchange Obstruction**: Exact finite spectral expansion $S_{N,T}(\sigma) = I_{AA} - I_{AZ} - I_{ZA} + I_{ZZ}$ is an exact 4-term algebraic decomposition with closed-form analytic kernels $J_T(p,q)$ and $K_T(\lambda,\mu;a)$, validated numerically with closure residual $< 10^{-15}$. However, every fixed finite collection of individual resolvents contributes 0 under $(1/2T)\int_{-T}^T$ as $T\to\infty$. The non-zero Besicovitch mean of the arithmetic side is carried by non-uniform infinite collective cancellation; termwise infinite limit interchange is unproved. | `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_GATE_G4` |
| **CANDIDATE_CMSA2** | Polarized Completed Mean-Square Anchor | $\mathcal A(\sigma_1, \sigma_2) = 0$ | `LIVE_G3_CLOSED_G4_OPEN` | Gate 4 (Infinite Spectral Interchange) | **Cross-Slot Non-Uniform Infinite Interchange**: Two-parameter polarization $\mathcal A(\sigma_1, \sigma_2)$ inherits exact finite paired kernel representation $K_T(\lambda,\mu; a_1, a_2)$, but termwise infinite limit interchange remains open at Gate G4. | `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_GATE_G4` |
| **CANDIDATE_CMSA3** | Grade-Normalized Completed Mean-Square Anchor | $\mathcal A_K(\sigma) = 0$ | `FALSIFIED_GATE_8` | Gate 8 (Grade Nonredundancy) | **Grade Covariance Redundancy**: The normalized completed logarithmic derivative $s D_s(su) = f(u)$ (formalized in Lean 4 for arbitrary scale $s > 0$) is strictly coordinate-redundant. Grade dilation yields no additional arithmetic constraints or non-redundant radial invariants beyond $K=0$. | `GRADE_COORDINATE_REDUNDANT` |

---

## 8. Lean 4 Formalization Mapping

| Mathematical Object | Mathematical Definition | Corpus Document | Lean 4 Theorem / Structure | Proof Content |
| :--- | :--- | :--- | :--- | :--- |
| $\sum_{i,j} (d_i+d_j)^2 = 2N\sum d_i^2 + 2(\sum d_i)^2$ | Arbitrary Algebraic Curvature | Proved Internally (Exact) | Formalized (`list_pairs_sq_sum_eq`) | Radial variation detector for arbitrary finite zero families |
| $J_T(p,q) = \frac{\log\frac{p+iT}{p-iT} + \log\frac{q+iT}{q-iT}}{2Ti(p+q)}$ | Exact Finite Zero Kernel | Proved Internally (Exact Analytic) | Verified in Python (`exact_finite_zero_kernel_J_T`) | Exact evaluation of finite spectral cross-terms |
| $K_T(\lambda,\mu; a) = m_\lambda m_\mu \sum_{\varepsilon,\eta} J_T(a-\varepsilon\lambda, a-\eta\bar\mu)$ | Exact Paired Zero-Zero Kernel | Proved Internally (Exact Analytic) | Verified in Python (`exact_finite_zero_zero_kernel_K_T`) | Exact evaluation of paired spectral self-interaction |
| $S_{N,T}(\sigma) = I_{AA} - I_{AZ} - I_{ZA} + I_{ZZ}$ | Complete Finite Spectral Expansion | Proved Internally (Algebraic Identity) | Verified in Python (`evaluate_complete_finite_spectral_expansion`) | Algebraic decomposition with numerical quadrature closure |
| $\Xi'/\Xi(z) = \sum \frac{2z}{z^2-\lambda^2}$ | Hadamard Log-Derivative | Standard Theorem (Hadamard 1893) | Unformalized Analytic | Exact spectral representation |
| $P(u) = A(u) - \Xi'/\Xi(u-1/2)$ | Completed Log-Derivative Identity | Proved Internally (Analytic, $\Re u > 1$) | Conditional Representation (`ConditionalCompletedLogDerivativeDecomposition`) | Arithmetic zero anchor foundation |
| $\lim_{T\to\infty} \frac{1}{2T}\int_{-T}^T \|P(\sigma+it)\|^2 dt = \sum \Lambda(n)^2 n^{-2\sigma}$ | Dirichlet Mean-Square | Proved Internally ($\ell^1$ Dirichlet Mean-Square, $\sum \|a_n\| < \infty$) / Carlson (1914) | Unformalized Analytic | Arithmetic zero anchor |
| $\mathcal A(\sigma) = 0$ | Completed Mean-Square Anchor | Proved Internally (Analytic) | Unformalized Analytic | Divisor-independent arithmetic anchor |
| $s D_s(su) = f(u)$ | Universal Scale Invariance | Proved Internally (Algebraic) | Formalized (`generic_scale_dilation_cancellation`) | Dilation coordinate redundancy exclusion |
| Single-grade coordinate pullback | Grade Covariance | Proved Internally (Algebraic) | Formalized (`coordinate_redundant`) | Coordinate redundancy exclusion |
| Gate G4: Infinite Spectral Interchange | Analytic Interchange Barrier | Identified Exact Open Obstruction | Open Analytic Gate | Earliest open gate in present CMSA derivation |
| $\mathrm{OBL\text{-}RDQ\text{-}001}$ | Arithmetic Radial Bridge | Open Research Obligation | Conditional Structure Only | Central Research Goal |

---

## 9. Dependency Ledger

| Dependency / Identity | Type | Mathematical Status | Lean Status | Role in Research |
| :--- | :--- | :--- | :--- | :--- |
| $\xi(s) = \xi(1-s)$ | Functional Equation | Standard Theorem (Riemann 1859) | External / Native | Root reflection symmetry |
| $z_K = \tau^K z$ | Coordinate Dilation | Proved Internally (Algebraic) | Formalized (`centeredGradeCoord_eq_tau_pow_mul_z`) | Transcendental grade transport |
| $\kappa_1(\lambda, \lambda^\#) = \delta^2/\gamma^2$ | Rational Involution Kernel | Proved Internally (Algebraic) | Formalized (`kappa1_val`) | Spectral defect conversion |
| $L_Q = 1 \iff \mathrm{RH}$ | Spectral Equivalence | Proved Internally (Analytic) | Formalized (`list_prod_one_plus_nonneg_eq_one_iff`) | Spectral target criterion |
| $\operatorname{Tr}\mathcal R = 0 \iff \mathrm{RH}$ | Spectral Equivalence | Proved Internally (Analytic) | Formalized (`list_sum_nonneg_eq_zero_iff`) | Spectral target criterion |
| $\sum_{i,j} (d_i+d_j)^2 = 2N\sum d_i^2 + 2(\sum d_i)^2$ | Arbitrary Algebraic Curvature | Proved Internally (Exact) | Formalized (`list_pairs_sq_sum_eq`) | Radial variation detector for arbitrary finite zero families |
| $J_T(p,q) = \frac{\log\frac{p+iT}{p-iT} + \log\frac{q+iT}{q-iT}}{2Ti(p+q)}$ | Exact Finite Zero Kernel | Proved Internally (Exact Analytic) | Verified in Python (`exact_finite_zero_kernel_J_T`) | Exact evaluation of finite spectral cross-terms |
| $J_T^{\text{Fejér}}(p,q) = \frac{I_T(p)+I_T(q)}{T(p+q)}$ | Exact Fejér Zero Kernel | Proved Internally (Exact Analytic) | Verified in Python (`exact_fejer_zero_kernel_J_T`) | Exact evaluation of Fejér windowed spectral kernel |
| $K_T(\lambda,\mu; a) = m_\lambda m_\mu \sum_{\varepsilon,\eta} J_T(a-\varepsilon\lambda, a-\eta\bar\mu)$ | Exact Paired Zero-Zero Kernel | Proved Internally (Exact Analytic) | Verified in Python (`exact_finite_zero_zero_kernel_K_T`) | Exact evaluation of paired spectral self-interaction |
| $S_{N,T}(\sigma) = I_{AA} - I_{AZ} - I_{ZA} + I_{ZZ}$ | Complete Finite Spectral Expansion | Proved Internally (Algebraic Identity) | Formalized (`finite_quadratic_four_term_decomposition`) | Closed exact finite spectral representation across windows |
| $\Xi'/\Xi(z) = \sum \frac{2z}{z^2-\lambda^2}$ | Hadamard Log-Derivative | Standard Theorem (Hadamard 1893) | Unformalized Analytic | Exact spectral representation |
| $P(u) = A(u) - \Xi'/\Xi(u-1/2)$ | Completed Log-Derivative Identity | Proved Internally (Analytic, $\Re u > 1$) | Conditional Representation (`ConditionalCompletedLogDerivativeDecomposition`) | Arithmetic zero anchor foundation |
| $\lim_{T\to\infty} \frac{1}{2T}\int_{-T}^T |P(\sigma+it)|^2 dt = \sum \Lambda(n)^2 n^{-2\sigma}$ | Dirichlet Mean-Square | Proved Internally (Exact $\ell^1$ Lemma) | CMSA_GATE_G4.md §4 | Arithmetic zero anchor |
| $\mathcal A(\sigma) = 0$ | Completed Mean-Square Anchor | Proved Internally (Analytic) | Unformalized Analytic | Divisor-independent arithmetic anchor |
| $s D_s(su) = f(u)$ | Universal Scale Invariance | Proved Internally (Algebraic) | Formalized (`generic_scale_dilation_cancellation`) | Dilation coordinate redundancy exclusion |
| Single-grade coordinate pullback | Grade Covariance | Proved Internally (Algebraic) | Formalized (`coordinate_redundant`) | Coordinate redundancy exclusion |
| $\forall H, \lim f(H, T) = 0 \centernot\implies \lim f(H(T), T) = 0$ | Cofinal Limit Distinction | Proved Internally (Countermodel) | Formalized (`cofinal_schedule_distinct_from_fixed_limit`) | Rigorous boundary layer limit separation |
| Gate G4: Infinite Spectral Regularization | Analytic Regularization Barrier | Characterized Across 4 Windows | `CMSA_GATE_G4.md` | Earliest open gate in present CMSA derivation |
| $\mathrm{OBL\text{-}RDQ\text{-}001}$ | Arithmetic Radial Bridge | Open Research Obligation | Conditional Structure (`ConditionalG4RegularizedBridge`) | Central Research Goal |

---

## 10. Completed Mean-Square Arithmetic Anchor (CMSA) Suite

### 10.1 Mathematical Definition
For $\Re(u) > 1$, let:
$$P(u) = \sum_{n=2}^\infty \frac{\Lambda(n)}{n^u} = -\frac{\zeta'}{\zeta}(u).$$
The Archimedean and pole logarithmic derivative is:
$$A(u) = \frac{1}{u} + \frac{1}{u-1} - \frac{1}{2}\log \pi + \frac{1}{2}\psi(u/2).$$
The fundamental completed logarithmic derivative identity is:
$$\boxed{P(u) = A(u) - \frac{\Xi'}{\Xi}\left(u - \frac{1}{2}\right)} \qquad (\Re u > 1).$$

### 10.2 Arithmetic Mean-Square Vanishing Anchor
For real $\sigma > 1$:
$$\mathcal P_\sigma(t) := A(\sigma + it) - \frac{\Xi'}{\Xi}\left(\sigma - \frac{1}{2} + it\right) = P(\sigma + it).$$
The completed mean-square anchor is:
$$\boxed{\mathcal A(\sigma) := \lim_{T\to\infty} \frac{1}{2T} \int_{-T}^T \left| A(\sigma+it) - \frac{\Xi'}{\Xi}\left(\sigma-\frac{1}{2}+it\right) \right|^2 dt - \sum_{n=2}^\infty \frac{\Lambda(n)^2}{n^{2\sigma}} = 0.}$$
This quantity:
1. Is completely divisor-independent on the arithmetic side;
2. Vanishes identically ($\mathcal A(\sigma) = 0$) unconditionally for all $\sigma > 1$;
3. Contains all nontrivial zeros via the symmetrically paired Hadamard logarithmic derivative $\Xi'/\Xi$.

### 10.3 Closed Finite Spectral Expansion & Exact Analytic Kernels
For any finite subset of zeros $\mathcal Z_N = \{\lambda_k = \delta_k + i\gamma_k\}_{k=1}^N$ ($z = a + it = \sigma - 1/2 + it$), the finite spectral approximant is:
$$Z_N(t) = \sum_{k=1}^N m_k \frac{2z}{z^2 - \lambda_k^2} = \sum_{k=1}^N m_k \left( \frac{1}{a - \lambda_k + it} + \frac{1}{a + \lambda_k + it} \right).$$
The finite mean square decomposes exactly into four algebraic terms across window families:
$$S_{N, T}^{(W)}(\sigma) := \int_{\mathbb R} W_T(t) |A(\sigma+it) - Z_N(t)|^2 dt = I_{AA} - I_{AZ} - I_{ZA} + I_{ZZ}.$$
1. **Rectangular Window**: $J_T(p,q) = \frac{\log\left(\frac{p+iT}{p-iT}\right) + \log\left(\frac{q+iT}{q-iT}\right)}{2Ti(p+q)}$.
2. **Fejér Window**: $J_T^{\text{Fejér}}(p,q) = \frac{I_T(p) + I_T(q)}{T(p+q)}$ where $I_T(w) = -\frac{(w+iT)\log(w+iT) + (w-iT)\log(w-iT) - 2w\log w}{T}$.

### 10.4 Gate G4 Infinite-Regularization and Radial-Sign Analysis
Detailed in [`CMSA_GATE_G4.md`](file:///c:/Development/Projects/reimann_scope/CMSA_GATE_G4.md):
1. **Asymptotic Regimes**: Characterized across $|\gamma| \ll T$ (plateau $\sim \pi/(2aT)$), $\gamma/T \to c$ (boundary transition $\frac{\arctan((T-\gamma)/a)+\arctan((T+\gamma)/a)}{2aT}$), and $|\gamma| \gg T$ (outer tail $\sim 1/(\gamma^2-T^2)$).
2. **Cofinal Limits**: Proved that fixed-cutoff vanishing $\lim_{T\to\infty} \sum_{|\gamma|\le H} J_T = 0$ does not imply cofinal vanishing $\lim_{T\to\infty} \sum_{|\gamma|\le cT} J_T$, which diverges as $\frac{c\log T}{4a}$. Formalized in Lean 4 with Mathlib `Filter.Tendsto` (`tendsto_cofinal_fixed_zero`, `not_tendsto_cofinal_diagonal_zero`, `finite_sum_tendsto_interchange`).
3. **Exact Radial Response Coefficient**:
   $$\Delta S_W = \delta^2 C_W(\sigma, \gamma, T) + O(\delta^4), \qquad C_W(\sigma, \gamma, T) = -2\Re \int_{\mathbb R} W_T(t) F_0(t) \overline{D_\gamma(\sigma - 1/2 + it)} dt,$$
   where $D_\gamma(z) = \frac{4z(z^2 - 3\gamma^2)}{(z^2+\gamma^2)^3}$.
4. **Certified Arb Ball Witness & Numerical Evidence**:
   - Witness WIT-02 (Fejér): Certified strictly negative across full symmetric support $[-16.8, 16.8]$ via outward-rounded Arb ball arithmetic (`certify_g4_fejer_witness_arb`), proving $\Delta S_{\text{Fejér}} \in [-1.89473 \times 10^{-4}, -1.54203 \times 10^{-4}] \subset (-\infty, 0)$.
   - Witnesses WIT 1, 3, 4: Negative numerical quadrature estimates with mpmath error estimates.
5. **Additive-Reference Invariance No-Go Theorem**:
   For any scalar reference $R_W(A)$ independent of $Z, \delta, \gamma$, $(S_W(Z_\delta) - R_W(A)) - (S_W(Z_0) - R_W(A)) \equiv S_W(Z_\delta) - S_W(Z_0)$. Thus, divisor-independent additive scalar subtractions cannot alter the raw radial difference. Formalized in Lean 4 (`additive_reference_subtraction_invariance`).
6. **Classifications**:
   - Raw Finite Fejér Window Response: `FAIL_RADIAL_POSITIVITY`.
   - Divisor-Independent Additive Class on Finite Fejér: `FAIL_RADIAL_POSITIVITY`.
   - Candidate CMSA-1 & CMSA-2 (Full Infinite/Cofinal): `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.
   - Complete Finite Algebraic Spectral Expansion: `FINITE_IDENTITY_PROVED_G4_OPEN`.
   - Dilated Completed Log-Derivative: `GRADE_COORDINATE_REDUNDANT`.
   - Witness WIT-02 Evidence Status: `CERTIFIED_NEGATIVE_ARB_BALL`.

### 10.5 Resolvent Algebra, Subcritical Norm Growth, and the Transcendental Continuation Activation Subgate
1. **Exact Single-Zero and Reflection Pair Resolvent Algebra**:
   For $a = \sigma - 1/2 > 0$, $w = a + i(t-\gamma)$, and $a - \delta > 0$:
   $$\int_{-\infty}^\infty |r_\delta(t)|^2 dt = \frac{\pi \delta^2}{a(a-\delta)(2a-\delta)} = \frac{\pi \delta^2}{2a^3} + \mathcal O(\delta^3),$$
   $$r_\delta(t) + r_{-\delta}(t) = \frac{2\delta^2}{w(w^2-\delta^2)}.$$
   Exact first-order cancellation suppresses symmetric functional-reflection pairs to $\mathcal O(\delta^2)$. Formalized in Lean 4 (`resolvent_difference_rational_identity`, `resolvent_reflection_pair_cancellation`).
2. **Fixed-Finite Invisibility Theorem** (`PROVED / EXACT / PARTIALLY_FORMALIZED`):
   For bounded prime background $P_\sigma$ ($\sigma > 1$) and any fixed finite resolvent perturbation $\Delta \in L^2(\mathbb R)$:
   $$\lim_{T\to\infty} \frac{1}{2T} \int_{-T}^T \left(|P_\sigma(t) - \Delta(t)|^2 - |P_\sigma(t)|^2\right) dt = 0.$$
   Lean 4 formalizes scalar energy scaling $E/(2T) \to 0$ (`fixed_finite_energy_scaling_zero`).
3. **Subcritical Cofinal Norm Growth Theorem** (`PROVED / EXACT / PARTIALLY_FORMALIZED`):
   For $P_T, \Delta_T \in L^2(-T, T)$ with $(1/(2T))\|P_T\|^2 \le M < \infty$ and $x_T = \|\Delta_T\|_{L^2}/\sqrt{T}$:
   $$|V_T| \le \frac{1}{2} x_T^2 + \sqrt{2M} x_T.$$
   If $\|\Delta_T\| = o(\sqrt{T})$, then $V_T \to 0$.
   Contrapositive (subsequential consequence): $\limsup |V_T| > 0 \implies \exists \varepsilon > 0, T_k \to \infty \text{ s.t. } \|\Delta_{T_k}\| \ge \varepsilon \sqrt{T_k}$. (Does NOT imply an eventual $\Omega(\sqrt{T})$ bound; counterexample $x_n = 1$ for even $n$, $1/(n+1)$ for odd $n$).
   Formalized in Lean 4: `subcritical_norm_response_bound_vanishes`, `subcritical_norm_response_tendsto_zero`, `subcritical_norm_contrapositive`, `not_tendsto_zero_subsequential_lower_bound`.
4. **Withdrawal of the Riemann–von Mangoldt Norm Asymptotic**:
   The claim $\|\Delta_{H(T)}\| \sim \sqrt{T\log T}$ is **WITHDRAWN** because:
   - On-line zeros contribute $r_j = 0$ identically;
   - Off-line zero count and distribution are unconstrained;
   - Defect displacements $\delta_j$ can vary or decay;
   - Off-diagonal inner products can cancel destructively;
   - Reflection partners cancel to first order ($\mathcal O(\delta^2)$);
   - Finite interval $[-T, T]$ boundary mode truncation.
5. **Finite Off-Line Quartet Invisibility & Zero-Rigidity Failure**:
   For any finite off-line zero configuration (such as a single quartet $\{1/2 \pm \delta \pm i\gamma\}$), $\Delta_{H(T)}(t) = \Delta(t) \in L^2(\mathbb R)$ for $H(T) \ge \gamma$, giving $\|\Delta_{H(T)}\| = \mathcal O(1) = o(\sqrt{T}) \implies V_T \to 0$.
   The normalized mean functional cannot distinguish a finite off-line quartet from RH.
   - Fixed / Subcritical Families: `FAIL_LIMIT_ORDER_DEPENDENCE`.
   - Growing Cofinal Families: `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.
6. **The Transcendental Continuation Activation Theorem (Earliest Open Subgate)**:
   $$\exists \rho \text{ with } \delta_\rho \ne 0 \implies \limsup_{T\to\infty} \frac{\|\Delta^{TC}_T\|_{L^2(-T, T)}}{\sqrt{T}} > 0.$$
   Requires 8 structural specifications (grade combination operation, non-double-counting proof, grade weights, bilateral convergence over $K \in \mathbb Z$, height truncation interaction, shift covariance, arithmetic representation, and non-pullback proof).
   Designated as the **earliest open subgate** logically preceding $E_T - C_T$ asymptotic evaluation.

### 10.6 Curvature-Transport Invariant and Descent Route

The **Curvature-Transport Framework** (`CURVATURE_TRANSPORT.md`) unifies:
1. Reciprocal circle geometry ($r_K \kappa_K = 1, C_1 = 1$) at integer checkpoints $K \in \mathbb Z$;
2. Fourier lattices ($L_K = \tau^K\mathbb Z$);
3. Radial unit recovery ($r(k) d_{\rho}(k) = \delta$) for continuous grade $k \in \mathbb R$;
4. Half-density dilation Mellin scaling ($a^{1/2-s}\Lambda(s) = \chi_s(k)^{-1}\Lambda(s)$ for $a = \tau^k$);
5. Reflection-pair defect $B_\rho(k) = 2(\cosh(k\delta\log\tau)-1) = 4\sinh^2(k\delta\log\tau/2) \ge 0$;
6. Continuous second grade variation $B_\rho''(0) = 2\delta^2(\log\tau)^2 \implies \mathscr K_\tau(\rho) = \delta^2$.

**Scalar-Transport No-Go Theorem & Holomorphic Obstruction**:
- For scalar multipliers $F_k = g_k L$, all grade derivatives at zeros vanish identically ($0 \equiv 0$), and logarithmic derivatives on $gL \ne 0$ supply zero divisor data.
- Scoped One-Point Holomorphic Obstruction proves no fixed holomorphic local kernel $H(z)$ can equal $(\Re z)^2$ on an open set ($\partial_{\bar z}(\Re z)^2 = \Re z = \delta \ne 0$), requiring non-scalar pairings, contour boundary terms, or regularized determinants.

Under the **Transcendental Curvature Rigidity Theorem**, any divisor-independent arithmetic functional $\mathscr A_\tau(\xi) = 0$ with spectral expansion $\mathscr A_\tau(\xi) = \sum W_\rho \delta_\rho^2$ ($W_\rho > 0$) implies RH.
Constructing such a functional without zero inputs is the program's canonical open obligation: the **Non-Scalar Arithmetic Functional Construction** (`OBL-CT-001A`). Curvature transport operates at the orbit level and bypasses fixed-finite $L^2$ translation invisibility at the spectral detector level ($B_\rho''(0) > 0$), but does NOT solve CMSA Gate G4; whether a non-scalar arithmetic functional avoids or reproduces the pair-isolation/infinite-limit barrier remains an open research problem.

### 10.6 Canonical Weil–Hermitian Curvature Bridge & GNS Barrier

The **Weil–Hermitian Curvature Bridge** (`CURVATURE_TRANSPORT.md` §14–15) connects continuous grade curvature to the arithmetic explicit formula:
1. **Geometric Discrepancy**: $|J(\rho) - C(\rho)|^2 = 4\delta_\rho^2$ for functional reflection $J(\rho) = 1-\rho$ and complex conjugation $C(\rho) = \bar\rho$.
2. **Pointwise Rational Identity**:
   $$\frac{1}{2}\left(\frac{1}{|\rho|^2} + \frac{1}{|1-\rho|^2}\right) - \Re\left(\frac{1}{\rho(1-\rho)}\right) = \frac{2\delta_\rho^2}{|\rho|^2|1-\rho|^2} = \frac{B_\rho''(0)}{(\log\tau)^2 |\rho|^2|1-\rho|^2} \ge 0.$$
3. **Discrete Summation & Hadamard Constant**:
   $$N_\xi - C_\xi = \sum_{\rho \in Z} \frac{2\delta_\rho^2}{|\rho|^2|1-\rho|^2} \ge 0, \qquad C_\xi = 2 + \gamma_{\text{Euler}} - \log(4\pi) \approx 0.0461914179322420...$$
4. **GNS Positive-Type Barrier**:
   Pure local prime distribution weights $-\frac{\Lambda(n)}{\sqrt{n}}$ are strictly negative-definite (all eigenvalues strictly negative). Defining an arithmetic Hilbert space norm via $Q_W(g * g^*) \ge 0$ without zero-independent positive factorization is logically circular, since $Q_W(g * g^*) \ge 0$ is globally equivalent to the Riemann Hypothesis (Weil 1952).

---

## 11. Current Status and Research Protocol

- **`OBL-CT-001A` (Non-Scalar Arithmetic Functional Construction)**: Canonical **EARLIEST OPEN OBLIGATION** (`CURVATURE_TRANSPORT.md` §15).
- **`OBL-CT-001B`–`OBL-CT-001D`**: Sequential open gates for spectral expansion, pair isolation, and conditional rigidity combination.
- **`OBL-RDQ-001`**: Remains **OPEN**.
- **`OBL-CMSA-003` (Gate G4)**: Remains **OPEN** (Earliest open gate in CMSA derivation).
- **Transcendental Continuation Activation Theorem (`OBL-TC-ACT`)**: Precise earliest open subgate for Gate G4.
- **Candidate Classification**: `EXACT_CURVATURE_IDENTITY_PROVED_ARITHMETIC_NORM_OPEN` (Weil–Hermitian Curvature Bridge) / `FAIL_RADIAL_POSITIVITY` (raw finite Fejér response & additive class) / `FAIL_LIMIT_ORDER_DEPENDENCE` (fixed and subcritical perturbation families) / `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE` (infinite cofinal CMSA-1/2) / `CERTIFIED_NEGATIVE_ARB_BALL` (Fejér WIT-02 certificate status) / `FINITE_IDENTITY_PROVED_G4_OPEN` (finite expansion).
- **Announcement Protocol**: Adheres strictly to Rule 01 (Mathematical Rigor Protocol). No proof of RH is announced.




