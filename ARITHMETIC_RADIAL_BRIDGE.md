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

## 4. Baseline Mathematical Audit & Grade Centering

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

### 4.3 Scoped One-Point No-Go Theorem
For any even holomorphic test function $H$, direct one-point evaluations $\sum_\rho H(\rho)$ satisfy:
$$A_H(\delta, \gamma) = 2 \Re G(\delta + i\gamma), \qquad G = H + H \circ (-\mathrm{id}).$$
If $A_H(\delta, \gamma)$ is $\delta$-independent on any open interval $I \ni 0$ for a fixed ordinate $\gamma > 0$, Cauchy-Riemann equations force $G'(z) \equiv 0$, so $G$ is constant.
- **Closed Scope**: Fixed linear combinations and locally uniform limits of direct 1-point holomorphic evaluations.
- **Open Scope**: Nonlinear paired forms, sesquilinear forms, tensor-square traces, operator determinants, and comparison metrics.

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

## 7. Candidate Registry and Falsification Analysis

| Candidate ID | Name | Target | Derivation Status | Pair Isolation | Earliest Failure / Obstruction | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CANDIDATE_A** | Linear Grade Differences | None | `PROVED_COLLAPSE` | False | Collapses to native explicit formula $\mathcal C_0[H \circ \tau^K] - \mathcal C_0[H]$; produces only 1-point direct sums; no pair isolation. | `FALSIFIED_FOR_BRIDGE` |
| **CANDIDATE_B** | Bilinear Cross-Grade Explicit Formula | Trace / Det | `DERIVED_OBSTRUCTED` | False | $D_K(s)\overline{D_L(s)}$ produces an unrestricted double sum over all zero pairs $(\rho_1, \rho_2)$; off-diagonal cross-terms dominate. | `FALSIFIED_FOR_PAIR_ISOLATION` |
| **CANDIDATE_C** | Tensor-Square Trace Identity | Trace | `OBSTRUCTED` | False | Doubled explicit formula sums over all zero pairs; selecting diagonal involution pair requires zero-divisor projection. | `FALSIFIED_FOR_PAIR_ISOLATION` |
| **CANDIDATE_D** | Log-Derivative Contour Identity | Determinant | `OBSTRUCTED` | False | Contour residue expansion generates cross-terms; fails pair isolation without divisor subtraction. | `FALSIFIED_FOR_PAIR_ISOLATION` |
| **CANDIDATE_E** | Relative Determinant from Arithmetic Data | Determinant ($D$) | `UNPROVED_BRIDGE` | True | Operator on Dirichlet polynomials matching $\det_{\mathrm F}(I+\mathcal R)$ without zero-divisor input lacks construction. | `OPEN_UNPROVED` |
| **CANDIDATE_F** | Grade-Indexed Prime-Power Pairing | Trace ($T$) | `UNPROVED_BRIDGE` | True | Prime-power kernel producing $\delta^2/\gamma^2$ without cross-term contamination lacks closed-form derivation. | `OPEN_UNPROVED` |
| **CANDIDATE_G** | Weighted Regularized Radial Bridge | Weighted ($T_a$) | `SPECTRAL_PROVED_ARITH_OPEN` | True | Spectral detector $T_a > 0 \iff \delta \ne 0$ is rigorously proved; arithmetic realization $\mathfrak A_{K,a}^{\mathrm{arith}}$ remains open. | `LIVE_UNDERIVED` |

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

---

## 9. Current Status and Research Protocol

- **`OBL-RDQ-001`**: Remains **OPEN**.
- **Announcement Protocol**: Adheres strictly to Rule 01 (Mathematical Rigor Protocol). No proof of RH is announced.
- **Immediate Research Step**: Investigate whether Candidate G (weighted regularized bridge) admits an arithmetic realization via regularized Mellin transforms of $\left|\frac{\zeta'}{\zeta}\right|^2$.
