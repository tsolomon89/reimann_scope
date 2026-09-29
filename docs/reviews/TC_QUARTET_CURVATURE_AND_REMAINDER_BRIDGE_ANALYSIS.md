# Transcendental Continuation: Reflected-Quartet Curvature and Spectral Remainder Bridge Analysis

**Authoritative Derivation, Defect Reopening, and Remainder Bridge Investigation**  
**Date**: September 29, 2026  
**Audited Target**: Target A (Complete Weighted Functional Certification & Defect Reopening) & Target B (Reflected-Quartet Curvature Control, Compensation Falsification, and Bridge Investigation)  
**Status**: `COMPLETED_EXPLORATORY_OBSTRUCTION_CLAIM_WITHDRAWN`  
**Epistemic Obligation**: Open (Active Research Track 2: `TASK-TC-012`)

---

## 1. Executive Summary & Epistemic Statement

### 1.1 The Primary TC Reductio Objective
The fundamental goal of the Transcendental Continuation (TC) program within the Riemann Scope is to derive an arithmetic-spectral contradiction from the existence of an off-critical zero of the Riemann zeta function $\zeta(s)$:
$$H \Longrightarrow \exists K \ne J, \; m, n \in \mathbb{Z} \setminus \{0\} : m \tau^K = n \tau^J, \qquad \tau = 2\pi,$$
where $H$ denotes the existence of a nontrivial zero $\rho_0$ with $\operatorname{Re}(\rho_0) \ne 1/2$. The impossibility of such an integer-grade station coincidence ($m \tau^K = n \tau^J$ for $K \ne J$ with $m, n \in \mathbb{Z}^+$) constitutes the intended reductio ad absurdum.

For concrete analysis, we adopt the parameterized hypothesis:
$$H(\rho_0, m_0): \quad \zeta(\rho_0) = 0, \quad \rho_0 = \frac{1}{2} + \delta + i\gamma, \quad 0 < |\delta| < \frac{1}{2}, \quad m_0 = \operatorname{mult}(\rho_0) \ge 1.$$

### 1.2 Reopened Claims and Critical Distinctions
Following independent red-team review, four key claims have been rigorously re-examined and corrected:

1. **Truncated Remainder vs. Complete Remainder (Issue 1 Reopened & Repaired)**:
   In the complete explicit formula identity:
   $$L(b) = D - r_{\text{match}} + r_{\text{rec}} = -\frac{1}{2},$$
   where $D$ is the *complete* infinite remainder:
   $$D = D_{\text{truncated}} + R_{\text{arch}} - R_{\text{spectral}}.$$
   The computed difference $714,651,998.4127$ is the *truncated* quantity:
   $$D_{\text{truncated}} = \text{arithmetic\_truncated} - S_{\text{unsel}, \le T}.$$
   The omitted infinite tails ($R_{\text{arch}}$ and $R_{\text{spectral}}$) have tail allowance $\sim 1.04 \times 10^{17}$ at $T=100$. Under hypothesis $H$, the complete remainder satisfies $D \approx -1/2$.
   Identifying $D$ with $D_{\text{truncated}} \sim 7.15 \times 10^8$ was an invalid conflation. Consequently, comparing local curvature $\approx 8.33$ against $7.15 \times 10^8$ did **not** establish an obstruction. That claim is withdrawn.

2. **Zero Coverage Certification (Issue 2 Reopened & Repaired)**:
   Checking solely $\max(\text{loaded\_zeros}) \ge T_{\text{cutoff}}$ was mathematically insufficient: synthetic lists such as `[101.0]` at $T=100$, as well as lists with omitted interior zeros or duplicate zeros, previously certified coverage.
   This has been replaced by the rigorous 7-point validation [`validate_spectral_zero_coverage`](file:///C:/Development/Projects/reimann_scope/tc/weil_forms/optimization.py#L56), checking strict monotonicity, zero counting against authoritative Odlyzko reference data, and bracketing above $T_{\text{cutoff}}$.
   Furthermore, `complete_spectral_enclosure_available` is strictly set to `False` because the infinite tails dominate and underlying evaluations lack certified Arb ball enclosures.

3. **Stieltjes Tail Certification & Stirling Gamma Correction (Issue 3 Reopened & Repaired)**:
   Total variation identities and closed-form Stieltjes integration are proved analytically. However, evaluation currently uses IEEE-754 floating point and `scipy.special.exp1` without directed outward rounding or certified root ball enclosures in Arb.
   Moreover, Trudgian (2014) Theorem 1 bounds $S(t)$; bounding the full counting remainder $|N(t) - M(t)|$ requires explicitly adding the Stirling gamma correction $\frac{c_\gamma}{t}$ with $c_\gamma = \frac{1}{48\pi} \approx 0.006631456$. This has been integrated in closed form. The epistemic status is classified as `ANALYTIC_POWER_MAJORANT_EMPIRICALLY_EVALUATED`.

4. **Compensation Falsification vs. General Obstruction (Issue 4 Reopened & Repaired)**:
   - **Valid Surviving Result**: The compensation control polynomial $X(t)$ proves that *quartet symmetry and a positive isolated quartet curvature $+2m_0/\delta^2$ do not force positive total local curvature*, because nearby critical-line zeros at $\gamma \pm \delta/2$ can dominate and keep $C_X(t) < -m/\delta^2 < 0$ across $|t-\gamma| \le \delta/4$.
   - **Withdrawn Claim**: The claim of a proved curvature-to-remainder obstruction is **withdrawn**. The support radius of the autocorrelation in log-space is $R_{\text{supp}} = \log(20/8) + 2h \approx 1.01629$ (not type 20), which does not forbid controlled approximate localization. Furthermore, an unregularized curvature integral diverges at critical zeros as $(t-\gamma_j)^{-2}$ and requires Hadamard finite-part regularization.
   - **Sharpened Next Question**: Construct the properly regularized single-zero response kernel connecting curvature to the weighted TC zero statistic, and test whether $H$ controls the resulting correction.

---

## 2. Target A: Contract Repair, Reproduction, and Numerical Rigor

### 2.1 A1: Prime Sign Derivation and Component Reproduction

In the Guinand-Weil explicit formula, the prime sum enters with a negative sign:
$$\sum_{\rho} \Psi_b\left(\rho - \frac{1}{2}\right) = A_{\text{arch}}(g_b) - \text{PrimePairing}(g_b).$$
Consequently, the truncated arithmetic functional is:
$$\text{arithmetic\_truncated} = \text{archimedean\_truncated} - \text{prime\_pairing\_raw}.$$

For the three-grade diagnostic direction $b = (-1, 1, 0)/\sqrt{2}$ with $h=0.05$ on $[8, 20]$:
- **Archimedean truncated value**: $+502,713,211.1461$
- **Raw prime pairing (position-space sum)**: $-211,930,586.9374$
- **Incorrect assembled diagnostic (addition)**: $+290,782,624.2087$
- **Correctly signed arithmetic truncated value (subtraction)**: $\mathbf{+714,643,798.0835}$

The near-resonant station pair in grade $K=-1$ ($x_1 = 53/(2\pi) \approx 8.4352$, $x_2 = 107/(2\pi) \approx 17.0296$) resonates with prime $q=2$:
$$|\log 2 - \log(107/53)| = \log(107/106) \approx 0.00938974 < 2h = 0.10.$$

### 2.2 A2: Complex Quartet Pairing and Metric Whitening

The full complex quartet contribution evaluates:
$$\mathcal{Q}(b) = m_0 \operatorname{Re}\left[ p(z_0) \mathcal{Q}_{\text{complex}} \right],$$
retaining the product $\operatorname{Im}[p(z_0)] \operatorname{Im}[\mathcal{Q}_{\text{complex}}]$.

The generalized eigenvalue problem $G_\beta v = \lambda M_\beta v$ against metric $M_\beta = P^T P$ is solved via symmetric inverse square root whitening:
$$W = (P^T P)^{-1/2} = V \Sigma^{-1/2} V^T, \qquad \widetilde{G} = W^T G_\beta W.$$
Its eigenvalues match `scipy.linalg.eigh(G_beta, M_beta)` to within $9.5 \times 10^{-30}$, eliminating the asymmetry defects of `inv(P^T P) @ G_beta`.

### 2.3 A3: Stieltjes Tail Envelope and Stirling Gamma Correction

For $z = \delta + it$ ($|\delta| \le 1/2$, $|t| \ge T$), the degree-six multiplier $p(z)$ and differentiated bump yield the power majorant:
$$|p(z) H_b(z)| \le \Phi_m(t) = \sum_{j=0}^5 c_{p_j} t^{-p_j}, \qquad p_j = 2m - 10 + 2j.$$
Convergence against $dN(t) \sim \frac{1}{2\pi} \log\frac{t}{2\pi} dt$ strictly requires $m \ge 6$.

Total variation bounds over derivative roots evaluate:
$$I_6 = \|\kappa^{(6)}\|_{L^1} \le 11,974,462.0, \qquad I_7 = \|\kappa^{(7)}\|_{L^1} \le 1,571,233,583.0.$$

The zero counting error envelope relative to $M(t) = \frac{t}{2\pi}\log\frac{t}{2\pi} - \frac{t}{2\pi} + \frac{7}{8}$ is:
$$|N(t) - M(t)| \le |S(t)| + \left| \frac{\theta(t)}{\pi} + 1 - M(t) \right| \le a \log t + b \log\log t + c + \frac{c_\gamma}{t},$$
where $a = 0.112$, $b = 0.278$, $c = 2.511$ (Trudgian 2014), and $c_\gamma = \frac{1}{48\pi} \approx 0.006631456$ accounts for the Stirling gamma remainder.

Integrating by parts yields the closed-form upper bound:
$$\int_T^\infty \Phi dN \le \int_T^\infty \Phi M'(t) dt + 2 \Phi(T) E(T) + \int_T^\infty (-\Phi') (E(t) - E(T)) dt.$$
- Smooth part per power: $\frac{c_p T^{1-p}}{2\pi} \left[ \frac{\log(T/2\pi)}{p-1} + \frac{1}{(p-1)^2} \right]$.
- Fluctuation part: $\sum c_p \left[ \frac{a T^{-p}}{p} + b E_1(p \log T) + c_\gamma \frac{p}{p+1} T^{-(p+1)} \right]$.

At $T=100.0$, for $m=6$, this returns the total tail allowance:
$$\text{TailBound}_{m=6}(T=100) \approx \mathbf{1.04194 \times 10^{17}}.$$
Because floating-point arithmetic and `scipy.special.exp1` are used without directed outward rounding, this is classified as an empirical evaluation of an analytic majorant.

### 2.4 A4: Focused Component Reproduction & Zero Coverage Repair

#### Component Reproduction Values
At frozen parameters $h=0.05, U=320, N_t=2000, T_{\text{cutoff}}=100, b = (-1, 1, 0)/\sqrt{2}$:
| Quantity | Symbol | Exact Reproduced Value |
| :--- | :--- | :--- |
| **Truncated Arithmetic Functional** | $\text{arithmetic\_truncated}$ | $+714,643,798.0835$ |
| **Unselected Zero Sum ($T \le 100$)** | $S_{\text{unsel}, \le 100}$ | $\mathbf{-8,200.3292}$ |
| **Truncated Difference** | $D_{\text{truncated}}$ | $\mathbf{+714,651,998.4127}$ |
| **Stieltjes Tail Allowance ($m=6, T=100$)** | $B_{\text{tail}}(T=100)$ | $\mathbf{1.04194 \times 10^{17}}$ |
| **Algebraic Target Scalar** | $L(b)$ | $-0.5000000000$ |
| **Selected Weight Mismatch** | $r_{\text{match}}$ | $\le 1.8 \times 10^{-14}$ |
| **Reconstruction Error** | $r_{\text{rec}}$ | $0.0000000000$ |

#### Repair of Zero Coverage Certification
The constructor now passes input zeros through [`validate_spectral_zero_coverage`](file:///C:/Development/Projects/reimann_scope/tc/weil_forms/optimization.py#L56):
- `[101.0]` at $T=100$ is rejected (`no_zeros_below_cutoff`).
- Omitted interior zeros (e.g. `[14.1347, 101.0]`) are rejected (`zero_count_mismatch_expected_29_got_1`).
- Duplicate zeros (e.g. `[14.1347, 14.1347, 101.0]`) are rejected (`duplicate_or_inverted_zeros`).
- Incomplete tables ($T=500 > 396.38$) are rejected (`reference_data_truncated_before_or_at_T`).
- Authoritative reference zeros at $T=100$: `spectral_coverage_certified = True`, while `complete_spectral_enclosure_available = False` because tail bounds ($\sim 1.04 \times 10^{17}$) dominate finite terms.

---

## 3. Target B: Reflected-Quartet Curvature and Bridge Re-examination

### 3.1 B1: Convergent Zero Representation of Curvature Observable

From the Hadamard factorization of $\xi(s) = e^{A + Bs} \prod_\rho (1 - s/\rho) e^{s/\rho}$:
$$\frac{\xi'}{\xi}(s) = B + \sum_\rho \left( \frac{1}{s - \rho} + \frac{1}{\rho} \right), \qquad \left( \frac{\xi'}{\xi} \right)'(s) = -\sum_\rho \frac{1}{(s - \rho)^2}.$$
Along the critical line $s = 1/2 + it$:
$$C(t) := \frac{d^2}{dt^2} \log |\xi(1/2 + it)| = \sum_\rho \operatorname{Re}\left[ \frac{1}{(1/2 + it - \rho)^2} \right].$$

1. **Midpoint Principal Part Cancellation**:
   For $\rho_0 = 1/2 + \delta + i\gamma$ and its reflection $\rho_0' = 1/2 - \delta + i\gamma$, setting $x = s - (1/2 + i\gamma)$:
   $$P_\delta(x) = -m_0 \left[ \frac{1}{x - \delta} + \frac{1}{x + \delta} \right] = -\frac{2 m_0 x}{x^2 - \delta^2}.$$
   At $x = 0$ ($s = 1/2 + i\gamma$), $P_\delta(0) = 0$. There is **no uncancelled pole or $m_0/\delta$ spike** at the midpoint.
2. **Individual Contributions**:
   - Critical-line zeros ($\beta = 1/2$):
     $$C_j(t) = -\frac{m_j}{(t - \gamma_j)^2} < 0 \quad (\forall t \ne \gamma_j).$$
   - Off-critical quartet ($\beta = 1/2 \pm \delta, \gamma_\rho = \pm \gamma$):
     $$C_{\text{quartet}}(t) = 2 m_0 \left[ \frac{\delta^2 - (t - \gamma)^2}{(\delta^2 + (t - \gamma)^2)^2} + \frac{\delta^2 - (t + \gamma)^2}{(\delta^2 + (t + \gamma)^2)^2} \right].$$
     At $t = \gamma$, $C_{\text{quartet}}(\gamma) = +2m_0/\delta^2 > 0$.

### 3.2 B2: Compensation Falsification Control (Valid Surviving Result)

Consider the even, real test polynomial:
$$X(t) = \left[ ((t - \gamma)^2 + \delta^2) ((t + \gamma)^2 + \delta^2) \right]^m \cdot \left[ (t^2 - (\gamma - a)^2) (t^2 - (\gamma + a)^2) \right]^m, \quad a = \frac{\delta}{2}, \; m \ge 1.$$
- It has an exact off-critical quartet at $t = \pm\gamma \pm i\delta$ (corresponding to $s = 1/2 \mp \delta \pm i\gamma$).
- It has critical-line zeros at $\gamma_1 = \gamma - \delta/2$ and $\gamma_2 = \gamma + \delta/2$.

#### Quantitative Evaluation
At $t = \gamma$:
$$C_{\text{quartet}}(\gamma) \approx \frac{2m}{\delta^2}, \qquad C_{\text{real}}(\gamma) \approx m \left( \frac{1}{(\delta/2)^2} + \frac{1}{(-\delta/2)^2} \right) = \frac{8m}{\delta^2}.$$
$$C_X(\gamma) \approx \frac{2m}{\delta^2} - \frac{8m}{\delta^2} = -\frac{6m}{\delta^2} < 0.$$
Across the entire neighborhood $|t - \gamma| \le \delta/4$, the critical zero contribution is $\ge 6.4 m / \delta^2$, yielding:
$$C_X(t) \le \frac{2m}{\delta^2} - \frac{6.4m}{\delta^2} = -\frac{4.4m}{\delta^2} < -\frac{m}{\delta^2} < 0.$$

#### Epistemic Conclusion
Quartet symmetry and a positive isolated quartet curvature $+2m_0/\delta^2$ do **not** force positive total local curvature. Critical-line zeros at distance $\delta/2$ completely overwhelm and reverse the sign. Concluding $C(t) > 0$ strictly requires an independent zero-free neighborhood hypothesis on the critical line ($\operatorname{dist}(\rho_0, \rho_j) \ge c\delta$), which does not follow from $H(\rho_0, m_0)$ alone.

### 3.3 B3: Transfer Analysis and Withdrawal of General Obstruction Claim

#### Re-evaluation of the Physical Support Coordinate
In physical space, stations are located at $x_{K,n} = \tau^K n$. The window $w$ is supported in $[8, 20]$ in the station coordinate $u = \tau^K n$.
The log-station coordinates are $x = \log u \in [\log 8, \log 20]$.
The maximum distance between log-stations is:
$$\Delta x_{\max} = \log 20 - \log 8 = \log(2.5) \approx 0.91629073.$$
With smoothing bump width $2h = 0.10$, the autocorrelation support radius is:
$$R_{\text{supp}} = \log(20/8) + 2h \approx \mathbf{1.01629073}.$$
The earlier report stated exponential type $20$, erroneously confusing the physical station coordinate $u \in [8, 20]$ with the log-station variable $x = \log u \in [\log 8, \log 20]$.
An entire function of exponential type $\approx 1.016$ is not forbidden from having controlled approximate localization.

#### Regularization Requirements
The curvature observable $C(t)$ has second-order poles $-m_j / (t - \gamma_j)^2$ at all critical-line zeros. An ordinary integral $\int \phi(t) C(t) dt$ is divergent without proper Hadamard finite-part regularization:
$$\text{p.v.} \int_{-\infty}^\infty \frac{\phi(t) - \phi(\gamma_j) - \phi'(\gamma_j)(t - \gamma_j)}{(t - \gamma_j)^2} dt.$$
No normalized regularized transfer operator connecting $C(t)$ to $\Psi_b$ was constructed in the previous sprint.

#### Conflation of Truncated and Complete Remainders
The comparison between local curvature $C(\gamma) \approx 8.33$ and remainder $D \sim 7.15 \times 10^8$ was based on equating complete $D$ with $D_{\text{truncated}}$.
Under hypothesis $H$, the complete identity forces:
$$D = L(b) + r_{\text{match}} - r_{\text{rec}} = -\frac{1}{2}.$$
The quantity $7.1465 \times 10^8$ is only the truncated difference before adding the large unclosed tails $R_{\text{arch}} - R_{\text{spectral}}$ ($\sim 10^{17}$).
Comparing local curvature against $D_{\text{truncated}}$ does **not** establish an obstruction to bounding complete $D$.

#### Withdrawal of Claim & Sharpened Research Question
The claim that a curvature-to-remainder obstruction is established is **withdrawn**.
The sharpened open question is:
> **Open Question (Track 2)**: Can a properly regularized curvature pairing $\mathcal{I}_{\text{reg}}(\phi, C)$ reproduce the weighted TC zero statistic $\sum_\rho \Psi_b(\rho - 1/2)$, with an explicit single-zero response kernel $K(z; t)$ and correction term? Does the actual off-critical zero hypothesis $H(\rho_0, m_0)$ provide sufficient quantitative control over the correction term to bound $D$?

---

## 4. Assumptions and Dependencies Table

| Claim / Component | Target | Evidence Class | Mathematical Scope | Dependencies & Provenance | Unresolved Obligations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Prime Sign Assembly** | A1 | `CERTIFIED_FINITE` | Truncated arithmetic functional on $[8, 20]$, $h=0.05$ | Guinand-Weil sign: $\text{Arith} = \text{Arch} - \text{Prime}$. Independent position-space sum reproduces $+714,643,798.0835$. | Infinite prime tail enclosure. |
| **Complex Quartet Pairing** | A2 | `CERTIFIED_FINITE` | Exact formula for $\mathcal{Q}(p, z_0)$ on $\mathbb{C}$ | Algebraic expansion $m_0 \operatorname{Re}[p(z_0) \mathcal{Q}_{\text{complex}}]$ preserving $\operatorname{Im} p(z_0)$. | None. |
| **Metric Whitening** | A2 | `CERTIFIED_FINITE` | Legal subspace $\mathcal{V}_{\text{legal}} \subset \mathbb{R}^3$ | Symmetric whitening $W = (P^T P)^{-1/2}$, $\widetilde{G} = W^T G_\beta W$. Eigenvalues match `scipy.linalg.eigh` to $10^{-29}$. | None. |
| **Stieltjes Derivative Bounds** | A3 | `EMPIRICAL` | Orders $m \in \{6, 7\}$ on $[-1, 1]$ | Total variation identity over roots. $I_6 \le 11,974,462.0$, $I_7 \le 1,571,233,583.0$. | Certified interval ball root isolation in Arb. |
| **Analytic Stieltjes Tail** | A3 | `ANALYTIC_POWER_MAJORANT_EMPIRICALLY_EVALUATED` | Ordinates $t \ge T$, Trudgian Theorem 1/2 + Stirling gamma correction | Closed-form smooth integral + fluctuation integral via $E_1(p \log T)$ and $c_\gamma / t$. | Directed outward rounding; certified interval ball arithmetic. |
| **Zero Coverage Validation** | A4 | `CERTIFIED_FINITE` | Validates reference zeros on $[0, T_{\text{cutoff}}]$ | Rigorous 7-point check `validate_spectral_zero_coverage`. Rejects `[101.0]`, gaps, duplicates. | Independent zero-counting certificate for full completeness. |
| **Curvature Zero Rep** | B1 | `PROVED_CONDITIONAL` | $C(t) = \frac{d^2}{dt^2}\log\|\xi(1/2+it)\|$ | Hadamard factorization of $\xi(s)$. Principal part $P_\delta(0) = 0$. | Conditional on convergence of Hadamard product. |
| **Compensation Control** | B2 | `REFUTED_WITHIN_SCOPE` | Curvature sign on $|t-\gamma| \le \delta/4$ for control $X(t)$ | Quantitative lower bound on real root curvature: $C_X(t) < -m/\delta^2 < 0$. | Falsifies claim that quartet curvature alone forces $C(t) > 0$. |
| **Curvature-Remainder Bridge** | B3 | `OPEN_RESEARCH_QUESTION` | Regularized response kernel and transfer to $D$ | Autocorrelation radius $R_{\text{supp}} \approx 1.01629$; Hadamard finite-part regularization required. | Derive single-zero regularized response kernel and critical-line limit. |

---

## 5. Verification Commands and Reproducibility

```bash
# 1. Run all focused numerical and span defect tests
python -m pytest tests/test_tc_numerical_and_span_defects.py -v

# 2. Run adversarial evidence controls
python -m pytest .agents/verification/test_adversarial_evidence_controls.py -v

# 3. Audit claim spec and register
python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --cross-check-register --repo-root .

# 4. Fast operational suite
python scripts/workflow.py check-fast
```
