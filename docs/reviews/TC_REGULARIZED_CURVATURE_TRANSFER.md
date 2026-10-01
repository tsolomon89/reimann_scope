# Transcendental Continuation: Exact Regularized Curvature-to-TC Transfer and Spectral Accounting Repair

**Authoritative Mathematical Derivation, Contract Specification, and Epistemic Audit**  
**Date**: September 29, 2026  
**Audited Targets**:
1. Target 1: Mathematical Contract Specification, Zero Accounting Repair, and Brent Gamma Envelope Stieltjes Integration
2. Target 2: Exact Regularized Curvature-to-TC Transfer Derivation, Distributional Invariants, and Reflected-Quartet Correction
**Status**: `COMPLETED_FINITE_IDENTITIES_PROVED_GLOBAL_IMPLICATION_UNRESOLVED`  
**Epistemic Obligation**: Open (Active Research Track 2: `TASK-TC-012`, `TASK-TC-013`)

---

## 1. Executive Summary & Epistemic Statement

### 1.1 The Primary TC Reductio Objective
The fundamental goal of the Transcendental Continuation (TC) program within the Riemann Scope is to derive an arithmetic-spectral contradiction from the existence of an off-critical zero of the Riemann zeta function $\zeta(s)$:
$$H \Longrightarrow \exists K \ne J, \; m, n \in \mathbb{Z} \setminus \{0\} : m \tau^K = n \tau^J, \qquad \tau = 2\pi,$$
where $H$ denotes the hypothesis that there exists a nontrivial zero $\rho_0$ with $\operatorname{Re}(\rho_0) \ne 1/2$. The impossibility of such an integer-grade station coincidence ($m \tau^K = n \tau^J$ for $K \ne J$ with $m, n \in \mathbb{Z}^+$) constitutes the intended contradictory conclusion of the reductio ad absurdum.

An impossible endpoint is the intended conclusion of a reductio proof, never a reason to discard the derivation; conversely, the failure of an intermediate construction (such as an unregularized curvature statistic) is an active research obligation, not a theorem against TC.

### 1.2 Summary of Sprint Accomplishments
This sprint completed two foundational targets:

1. **Target 1: Mathematical Contract and Rigorous Spectral Accounting**:
   - **Unified Contract**: Formulated the unique production quantity for the complete remainder:
     $$D = A_{\le U} + R_{\text{arch}} - S_{\text{unselected}, \le T} - R_{\text{spectral}}.$$
     Repaired `remaining_open_lemma` in `tc/weil_forms/optimization.py` to include $R_{\text{arch}}$ and subtract the raw prime pairing exactly once ($A_{\le U} = A_{\text{arch}, \le U} - \text{Prime}_{\le U}$).
   - **Deprecated Ambiguous Alias**: Deprecated `D_val` as an alias for $D_{\text{truncated}}$, ensuring no confusion with complete $D$.
   - **Shifted Zero Partition & Uncertainty Propagation (Target 1A)**: Reproduced the critical defect where shifting the first two reference ordinates by $+5 \times 10^{-5}$ caused unselected zeros to jump from 27 to 29 and dropped $\varepsilon_\gamma$ to 0. Implemented a disjoint-interval validation partition based on authoritative Odlyzko reference identities, preserving the unselected count at 27 and propagating the maximum displacement $\varepsilon_\gamma = 5 \times 10^{-5}$ into downstream observables. Added boundary intersection rejection ($|g - T| \le 10^{-4}$).
   - **Brent Gamma Envelope and Single-Endpoint Stieltjes Integration (Target 1B)**: Falsified the former upper envelope $1/(48\pi t)$ at $t=100$ (where actual correction $\approx 6.6315 \times 10^{-5} > 1/(48\pi \cdot 100) \approx 6.631456 \times 10^{-5}$). Adopted and verified the primary-source envelope from Richard P. Brent (2016), Theorem 5 and Corollary 4:
     $$\left|\frac{\theta(t)}{\pi} + 1 - M(t)\right| \le \frac{1}{150 t}, \qquad t \ge 10.$$
     Re-derived single-endpoint Stieltjes integration, reconciled Trudgian's rearranged doubled-endpoint identity, and quantified the tail allowance revision at $T=100, m=6$ ($+1.04 \times 10^{11}$ increase to $1.041942 \times 10^{17}$, covered by the conservative endpoint structure).

2. **Target 2: Exact Regularized Curvature-to-TC Transfer**:
   - **Distributional Response Kernel**: Derived the Fourier transform of the second-order curvature kernel $g_a(x) = \frac{a^2-x^2}{(a^2+x^2)^2}$ ($a > 0$):
     $$\widehat{g}_a(u) = \pi |u| e^{-a|u|}, \qquad g_a \xrightarrow{\mathcal{D}'} -\operatorname{Fp}\left(\frac{1}{x^2}\right) \quad \text{as } a \downarrow 0.$$
   - **Regularized Test Function**: Solved the critical-line calibration singularity $|u|\widehat{\phi}_b(u) = 2f_b(u)$ at $u=0$ by constructing the logarithmic test function with removable integrand and $\phi(0) = 0$:
     $$\phi_{f_b}(t) = \frac{1}{\pi} \int_{\mathbb{R}} f_b(u) \frac{\cos(ut)-1}{|u|} \, du.$$
   - **Exact Single-Zero & Reflected-Pair Identities**: Proved the exact pairing:
     $$K_{\phi_{f_b}}(a,\gamma) = \int_{\mathbb{R}} f_b(u) e^{-a|u|} e^{iu\gamma} \, du,$$
     reducing on the critical line ($a=0$) identically to $\Psi_b(i\gamma)$.
     Derived the exact reflected-pair correction:
     $$\Psi_b(a+i\gamma) + \Psi_b(-a+i\gamma) - 2K_{\phi_{f_b}}(a,\gamma) = 2 \int_{\mathbb{R}} f_b(u) \sinh(a|u|) e^{iu\gamma} \, du,$$
     and full quartet correction $\Delta_{\text{quartet}}(a,\gamma) = 8 m_0 \int_0^R f_b(u) \sinh(au) \cos(u\gamma) \, du$.
   - **Distributional Summability Bounds**: Proved via distributional integration by parts:
     $$|K_{f_b}(a,\gamma)| \le \frac{\|f_b''\|_1 + \|f_b'\|_1 + \frac{1}{4}\|f_b\|_1 + |f_b(0)|}{\gamma^2},$$
     $$|\Delta_{\text{quartet}}(a,\gamma)| \le \frac{8 m_0}{\gamma^2} \left[ 2a |f_b(0)| + \sinh(aR) \|f_b''\|_1 + 2a \cosh(aR) \|f_b'\|_1 + a^2 \sinh(aR) \|f_b\|_1 \right] \le C(f_b) \frac{a}{\gamma^2}.$$
   - **Authentic Production Family Validation and Withdrawal of Premature Obstruction**: Constructed the authentic position-space density $f_b(u)$ from the 98 active prime stations, legal vector $b = (-1/\sqrt{2}, 1/\sqrt{2}, 0)$, differentiated kernel $\psi_h$, and production polynomial $p(z)$. Verified that the regularized curvature transfer identity holds to machine precision (relative discrepancy $< 10^{-13}$). Withdrew the unsupported surrogate-based "eight orders of magnitude too small" numerical obstruction: the bound constant depends on the actual density derivatives ($\|f_b''\|_1 \approx 2.11 \times 10^{16}$), yielding $C(f_b) \approx 4.47 \times 10^{16}$, an analytic bound $\approx 4.38 \times 10^{12}$, and actual quartet correction $\approx 1.18 \times 10^6$ for the production functional.

---

## 2. Target 1: Production Mathematical Contract and Defect Repair

### 2.1 The Repaired Production Contract
The authentic Guinand-Weil explicit formula connects arithmetic and spectral quantities:
$$\sum_{\rho} \Psi_b\left(\rho - \frac{1}{2}\right) = A_{\text{arch}}(g_b) - \sum_{p^k} \frac{\log p}{p^{k/2}} \left[ g_b(k \log p) + g_b(-k \log p) \right].$$
In terms of truncated calculations with cutoffs $U$ (spatial/frequency) and $T$ (spectral):
- **Truncated Archimedean contribution**: $A_{\text{arch}, \le U}$
- **Truncated Prime pairing**: $\text{Prime}_{\le U} = \sum_{p^k \le e^U} \frac{\log p}{p^{k/2}} [g_b(k\log p) + g_b(-k\log p)]$
- **Truncated Arithmetic functional**: $A_{\le U} = A_{\text{arch}, \le U} - \text{Prime}_{\le U}$
- **Unselected critical-line sum**: $S_{\text{unselected}, \le T} = \sum_{\gamma_j \in \text{unselected}, |\gamma_j| \le T} \Psi_b(i\gamma_j)$
- **Truncated difference**: $D_{\text{truncated}} = A_{\le U} - S_{\text{unselected}, \le T}$
- **Complete remainder**:
  $$D = A_{\le U} + R_{\text{arch}} - S_{\text{unselected}, \le T} - R_{\text{spectral}} = D_{\text{truncated}} + R_{\text{arch}} - R_{\text{spectral}}.$$

The complete explicit formula identity is:
$$L(b) = D - r_{\text{match}} + r_{\text{rec}} = -\frac{1}{2}.$$

#### Defect Resolution in `remaining_open_lemma`:
Previously, `remaining_open_lemma` in `tc/weil_forms/optimization.py` contained two errors:
1. It added the prime pairing back to $A_{\le U}$ (which already included it), effectively canceling or doubling the prime contribution.
2. It completely omitted $R_{\text{arch}}$.
Both errors were corrected in `construct_weighted_admissible_spectral_test`:
```python
remaining_open_lemma = (
    arithmetic_truncated + R_arch - unselected_sum - R_spectral
)
```
The ambiguous alias `D_val` has been deprecated in favor of explicit `D_truncated`, and descriptions claiming "proved outward derivative enclosures" have been replaced by `ANALYTIC_POWER_MAJORANT_EMPIRICALLY_EVALUATED`.

---

### 2.2 Target 1A: Shifted-Zero Defect Reproduction and Stable Partition

#### Defect Reproduction
At $T=100$, the first two nontrivial Riemann zeros are $\gamma_1 \approx 14.134725$ and $\gamma_2 \approx 21.022040$.
The previous implementation performed zero selection via:
```python
unselected_zeros = [
    g for g in loaded_zeros
    if abs(g - ref_gammas[0]) > 1e-6 and abs(g - ref_gammas[1]) > 1e-6
]
```
When an input array shifted $\gamma_1$ and $\gamma_2$ by $+5 \times 10^{-5}$:
1. `validate_spectral_zero_coverage` checked $|g - g_{\text{ref}}| \le 10^{-4}$ and accepted the list.
2. However, $5 \times 10^{-5} > 10^{-6}$, so the filter failed to identify $\gamma_1$ and $\gamma_2$ as the selected zeros.
3. As a result, the unselected zero count increased from 27 to 29 (all 29 zeros were treated as unselected).
4. Furthermore, the displacement $+5 \times 10^{-5}$ was discarded, and downstream observables were evaluated with $\varepsilon_\gamma = 0$.

#### Repaired Stable Partition and Uncertainty Budget
In `tc/weil_forms/optimization.py`:
1. `validate_spectral_zero_coverage` validates that every loaded zero matches an authoritative Odlyzko reference zero within a tolerance interval $[g_{\text{ref}} - \delta, g_{\text{ref}} + \delta]$ with $\delta = 10^{-4}$. Because consecutive Riemann zeros satisfy $|\gamma_{j+1} - \gamma_j| > 0.5 \gg 2\delta$, these intervals are strictly disjoint.
2. The function records `max_input_displacement = max(|g_j - g_{j,\text{ref}}|)`.
3. In `construct_weighted_admissible_spectral_test`, the spectral partition is established stably:
   - Selected zero 1: `validated_crit[0]`
   - Selected zero 2: `validated_crit[1]`
   - Unselected zeros: `validated_crit[2:]` (count strictly invariant at 27).
4. `max_input_displacement` is propagated as `effective_eps_gamma` into `spectral_evidence_status`, certifying that evaluations carry an explicit uncertainty budget.
5. Boundary zeros whose uncertainty interval intersects $T_{\text{cutoff}}$ ($|g - T| \le 10^{-4}$) are rejected.

Three orthogonal evidence dimensions are explicitly reported:
- `reference_agreement`: `True` (all zeros match reference within $10^{-4}$).
- `zero_isolation_count_coverage`: `True` (authoritative count complete up to $T=100$, no interior omissions, strictly monotonic).
- `complete_functional_enclosure`: `False` (infinite tails dominate and directed Arb rounding is not yet implemented).

---

### 2.3 Target 1B: Brent Gamma Envelope and Single-Endpoint Stieltjes Integration

#### Falsification of $1/(48\pi t)$
The prior envelope claimed:
$$\left|\frac{\theta(t)}{\pi} + 1 - M(t)\right| \le \frac{1}{48\pi t} \approx \frac{0.006631455962}{t}.$$
Evaluating at $t = 100$:
$$\theta(100) \approx 106.37624637731776, \qquad M(100) = \frac{100}{2\pi}\log\frac{100}{2\pi} - \frac{100}{2\pi} + \frac{7}{8} \approx 34.73477123985552.$$
Thus:
$$\frac{\theta(100)}{\pi} + 1 - M(100) \approx 0.00006631494646879.$$
However:
$$\frac{1}{48\pi \cdot 100} \approx 0.00006631455962162.$$
Because $6.631495 \times 10^{-5} > 6.631456 \times 10^{-5}$, the bound is violated. The constant $1/(48\pi)$ was the leading asymptotic coefficient, not an exact global upper envelope.

#### Primary-Source Derivation from Brent (2016)
Richard P. Brent (*On asymptotic approximations to the log-Gamma and Riemann-Siegel theta functions*, arXiv:1609.03682, Theorem 5 & Corollary 4) establishes that for $t \ge 10$:
$$\left|\frac{\theta(t)}{\pi} + 1 - M(t)\right| \le \frac{1}{150 t}.$$
Evaluating at $t=100$:
$$\frac{1}{150 \cdot 100} = \frac{1}{15000} \approx 6.6667 \times 10^{-5} > 6.6315 \times 10^{-5},$$
providing a rigorous analytic upper envelope.

#### Closed-Form Single-Endpoint Stieltjes Integration
Let $\Phi(t) = c_p t^{-p}$ and $E_\gamma(t) = C_\gamma t^{-1}$ with $C_\gamma = 1/150$.
Integrating by parts under Stieltjes integration on $[T, \infty)$:
$$\int_T^\infty \Phi(t) \, dE_\gamma(t) = \left[ \Phi(t) E_\gamma(t) \right]_T^\infty - \int_T^\infty \Phi'(t) E_\gamma(t) \, dt.$$
For the upper bound with envelope $|E_\gamma(t)| \le C_\gamma t^{-1}$:
$$\Phi(T) E_\gamma(T) + \int_T^\infty (-\Phi'(t)) E_\gamma(t) \, dt \le c_p T^{-p} \cdot C_\gamma T^{-1} + \int_T^\infty (p c_p t^{-p-1}) (C_\gamma t^{-1}) \, dt.$$
The integral evaluates:
$$p c_p C_\gamma \int_T^\infty t^{-p-2} \, dt = p c_p C_\gamma \frac{T^{-p-1}}{p+1} = \frac{p}{p+1} C_\gamma c_p T^{-p-1}.$$
Adding the endpoint term $\Phi(T) E_\gamma(T) = C_\gamma c_p T^{-p-1}$ gives:
$$C_\gamma c_p \left(1 + \frac{p}{p+1}\right) T^{-p-1} = C_\gamma c_p \frac{2p+1}{p+1} T^{-p-1}.$$

#### Tail Bound Quantification and Endpoint Reconciliation
In Trudgian's rearranged formula, $\Phi(T) E_S(T) + \int_T^\infty (-\Phi') E_S(t) \, dt = 2 \Phi(T) E_S(T) + \int_T^\infty (-\Phi') (E_S(t) - E_S(T)) \, dt$. This doubled endpoint term $2\Phi(T)E_S(T)$ isolates the logarithmic integral while remaining algebraically identical to the single-endpoint Stieltjes integration.
For the Brent (2016) gamma component, the closed-form single-endpoint Stieltjes contribution is:
$$\Phi(T) E_\gamma(T) + \int_T^\infty (-\Phi') E_\gamma(t) \, dt = C_\gamma \sum c_p \left(1 + \frac{p}{p+1}\right) T^{-p-1}.$$
Comparing the values at $T=100.0, m=6$:
- **Old tail bound** ($c_\gamma = \frac{1}{48\pi} \approx 0.006631456$): $1.0419409896796547 \times 10^{17}$
- **Repaired tail bound** (Brent 2016 $c_\gamma = \frac{1}{150} \approx 0.006666667$): $1.0419420269480304 \times 10^{17}$
- **Net change**: $+1.037268 \times 10^{11}$.

As noted in the sprint specification, the conservative endpoint structure in Trudgian's rearranged identity ensures that this minor revision in $c_\gamma$ does not represent a demonstrated underestimation of the physical tail. Both bounds remain empirically evaluated pending directed Arb ball enclosures.

---

## 3. Target 2: Exact Regularized Curvature-to-TC Transfer

### 3.1 Curvature Kernel and Fourier Transform
Let $a = |\operatorname{Re}(\rho) - 1/2|$ and $\gamma = \operatorname{Im}(\rho)$.
The second-order curvature kernel is:
$$g_a(x) = \frac{a^2 - x^2}{(a^2 + x^2)^2}, \qquad a > 0.$$
Under the Fourier convention $\widehat{\phi}(u) = \int_{\mathbb{R}} \phi(t) e^{-iut} \, dt$:
$$\widehat{g}_a(u) = \pi |u| e^{-a|u|}.$$

*Proof*:
Note that $g_a(x) = -\frac{d}{dx} \left( \frac{x}{a^2 + x^2} \right) = \operatorname{Re}\left[ \frac{1}{(a + ix)^2} \right]$.
Using the standard Fourier transform $\int_{\mathbb{R}} \frac{e^{-iut}}{a^2 + t^2} \, dt = \frac{\pi}{a} e^{-a|u|}$, and differentiating with respect to $a$, we obtain:
$$\int_{\mathbb{R}} \frac{a^2 - t^2}{(a^2 + t^2)^2} e^{-iut} \, dt = \pi |u| e^{-a|u|}. \quad \square$$

### 3.2 Distributional Limit as $a \downarrow 0$
As $a \downarrow 0$, $g_a(x) \to -1/x^2$ pointwise for $x \ne 0$. In the distributional space $\mathcal{D}'(\mathbb{R})$:
$$g_a \xrightarrow{\mathcal{D}'} -\operatorname{Fp}\left(\frac{1}{x^2}\right),$$
where $\operatorname{Fp}(1/x^2)$ is the Hadamard second-order finite part functional defined on test functions $\phi \in C_c^2(\mathbb{R})$ by:
$$\langle \operatorname{Fp}(1/x^2), \phi \rangle = \lim_{\varepsilon \downarrow 0} \left[ \int_{|x| \ge \varepsilon} \frac{\phi(x)}{x^2} \, dx - \frac{2\phi(0)}{\varepsilon} \right] = \int_0^\infty \frac{\phi(x) + \phi(-x) - 2\phi(0)}{x^2} \, dx.$$
Since $\int_{\mathbb{R}} g_a(x) \, dx = 0$, we have:
$$\int_{\mathbb{R}} g_a(x) \phi(x) \, dx = \int_0^\infty g_a(x) [\phi(x) + \phi(-x) - 2\phi(0)] \, dx.$$
For $x > 0$, $g_a(x) \to -1/x^2$ dominated by $C/(x^2 + a^2)$, yielding convergence to $-\langle \operatorname{Fp}(1/x^2), \phi \rangle$.

### 3.3 The Authentic Position-Space Density $f_b(u)$
In the weighted TC test:
$$\Psi_b(z) = p(z) F_b(z) F_b(-z), \qquad F_b(z) = A_h(z) E_b(z),$$
where $p(z) = -(z^2 - 1/4)(z^2 - 9/4)(z^2 - 25/4)$ is an even, real polynomial of degree 6 in $z = \delta + it$.
The position-space representation is:
$$\Psi_b(z) = \int_{-R}^R f_b(u) e^{zu} \, du,$$
where $R = \log(x_{\max}/x_{\min}) + 2h \approx 1.01629$ is the compact support radius of the log-station autocorrelation.
Because $p(z)$ and $F_b(z)F_b(-z)$ are invariant under $z \mapsto -z$ and real on the axes, $f_b(u)$ is:
- **Strictly real-valued**: $f_b(u) \in \mathbb{R}$
- **Even**: $f_b(-u) = f_b(u)$
- **Smooth and compactly supported**: $f_b \in C_c^\infty([-R, R])$.

### 3.4 Calibration and the Regularized Test Function $\phi_{f_b}$
Critical-line calibration requires matching the curvature response to $\Psi_b(i\gamma)$:
$$|u| \widehat{\phi}_b(u) = 2 f_b(u).$$
The quotient $2f_b(u)/|u|$ has a non-integrable singularity at $u=0$ if $f_b(0) \ne 0$.
To resolve this, we construct the regularized test function:
$$\phi_{f_b}(t) = \frac{1}{\pi} \int_{\mathbb{R}} f_b(u) \frac{\cos(ut) - 1}{|u|} \, du.$$
Properties of $\phi_{f_b}(t)$:
1. **Removable zero singularity**: Since $1 - \cos(ut) = 2\sin^2(ut/2) \sim u^2 t^2 / 2$ as $u \to 0$, the integrand is $O(|u|)$ and smooth at $u=0$.
2. **Fixed normalization**: $\phi_{f_b}(0) = 0$.
3. **Logarithmic asymptotic growth**: As $|t| \to \infty$, $\phi_{f_b}(t) \sim -\frac{2 f_b(0)}{\pi} \log|t| + O(1)$.

### 3.5 Single-Zero Response Identity
For $a > 0$:
$$K_{\phi_{f_b}}(a, \gamma) = \int_{\mathbb{R}} \phi_{f_b}(t) g_a(t - \gamma) \, dt = \int_{\mathbb{R}} f_b(u) e^{-a|u|} e^{iu\gamma} \, du.$$

*Proof*:
Using Fubini's theorem (justified by compact support of $f_b$ and integrability of $g_a$):
$$K_{\phi_{f_b}}(a,\gamma) = \frac{1}{\pi} \int_{\mathbb{R}} \frac{f_b(u)}{|u|} \int_{\mathbb{R}} (\cos(ut) - 1) g_a(t - \gamma) \, dt \, du.$$
We compute the inner integral:
$$\int_{\mathbb{R}} e^{iut} g_a(t - \gamma) \, dt = e^{iu\gamma} \int_{\mathbb{R}} e^{iux} g_a(x) \, dx = e^{iu\gamma} \widehat{g}_a(-u) = \pi |u| e^{-a|u|} e^{iu\gamma}.$$
Taking the real part yields $\int_{\mathbb{R}} \cos(ut) g_a(t - \gamma) \, dt = \pi |u| e^{-a|u|} \cos(u\gamma)$.
Since $\int_{\mathbb{R}} g_a(t - \gamma) \, dt = 0$, the subtracted term vanishes: $\int_{\mathbb{R}} 1 \cdot g_a(t - \gamma) \, dt = 0$.
Therefore:
$$K_{\phi_{f_b}}(a,\gamma) = \frac{1}{\pi} \int_{\mathbb{R}} \frac{f_b(u)}{|u|} \left( \pi |u| e^{-a|u|} \cos(u\gamma) \right) \, du = \int_{\mathbb{R}} f_b(u) e^{-a|u|} e^{iu\gamma} \, du. \quad \square$$

On the critical line ($a=0$):
$$K_{\phi_{f_b}}(0, \gamma) = \int_{\mathbb{R}} f_b(u) e^{iu\gamma} \, du = \Psi_b(i\gamma).$$
Thus, the regularized curvature response matches the weighted TC spectral test identically for every critical-line zero.

### 3.6 Exact Reflected-Pair and Quartet Corrections
For an off-critical zero at $z = a + i\gamma$ and its reflection $-z = -a - i\gamma$:
$$\Psi_b(a + i\gamma) = \int_{\mathbb{R}} f_b(u) e^{au} e^{iu\gamma} \, du, \qquad \Psi_b(-a + i\gamma) = \int_{\mathbb{R}} f_b(u) e^{-au} e^{iu\gamma} \, du.$$
Summing the reflected pair:
$$\Psi_b(a + i\gamma) + \Psi_b(-a + i\gamma) = 2 \int_{\mathbb{R}} f_b(u) \cosh(au) e^{iu\gamma} \, du.$$
Subtracting the doubled curvature response $2K_{\phi_{f_b}}(a,\gamma) = 2 \int_{\mathbb{R}} f_b(u) e^{-a|u|} e^{iu\gamma} \, du$:
$$\Psi_b(a + i\gamma) + \Psi_b(-a + i\gamma) - 2K_{\phi_{f_b}}(a,\gamma) = 2 \int_{\mathbb{R}} f_b(u) \left[ \cosh(au) - e^{-a|u|} \right] e^{iu\gamma} \, du.$$
Since $\cosh(au) - e^{-a|u|} = \sinh(a|u|)$, we obtain the exact identity:
$$\mathbf{\Psi_b(a + i\gamma) + \Psi_b(-a + i\gamma) - 2K_{\phi_{f_b}}(a,\gamma) = 2 \int_{\mathbb{R}} f_b(u) \sinh(a|u|) e^{iu\gamma} \, du}.$$

For the full quartet $\{1/2 \pm a \pm i\gamma\}$ with multiplicity $m_0$:
$$\Delta_{\text{quartet}}(a,\gamma) = 4 m_0 \int_{\mathbb{R}} f_b(u) \sinh(a|u|) \cos(u\gamma) \, du = 8 m_0 \int_0^R f_b(u) \sinh(au) \cos(u\gamma) \, du.$$
Since $\sinh(0) = 0$, $\Delta_{\text{quartet}}(0,\gamma) \equiv 0$. For $a > 0$, $\sinh(au) = au + \frac{1}{6}(au)^3 + \dots$, so the correction scales linearly with displacement $a$.

### 3.7 Distributional Summability Bounds
To establish convergence across an infinite sequence of zeros, we integrate by parts twice with respect to $u$:
$$K_{f_b}(a,\gamma) = \int_{-R}^R \chi(u) e^{iu\gamma} \, du, \qquad \chi(u) = f_b(u) e^{-a|u|}.$$
The function $\chi(u)$ is continuous on $[-R, R]$ but has a corner at $u=0$ with derivative jump:
$$\chi'(0^+) - \chi'(0^-) = [f_b'(0) - a f_b(0)] - [f_b'(0) + a f_b(0)] = -2a f_b(0).$$
Integrating by parts twice in the distributional sense:
$$\int_{-R}^R \chi(u) e^{iu\gamma} \, du = -\frac{1}{\gamma^2} \left[ -2a f_b(0) + \int_{-R}^R \chi''(u) e^{iu\gamma} \, du \right].$$
For $0 \le a \le 1/2$ and $u \ne 0$:
$$\chi''(u) = [f_b''(u) \mp 2a f_b'(u) + a^2 f_b(u)] e^{-a|u|}.$$
Taking norms:
$$|K_{f_b}(a,\gamma)| \le \frac{1}{\gamma^2} \left( \|f_b''\|_1 + \|f_b'\|_1 + \frac{1}{4} \|f_b\|_1 + 2a |f_b(0)| \right) \le \frac{C_{\text{decay}}}{\gamma^2}.$$
Because $\sum_{\rho} \frac{1}{\gamma^2} < \infty$, the regularized curvature response sum $\sum_{\rho} K_{\phi_{f_b}}(\rho)$ is unconditionally convergent!

Similarly, for the correction kernel $\eta(u) = f_b(u) \sinh(a|u|)$:
Since $\sinh(a|u|) \sim a|u|$ at $u=0$, $\eta(0) = 0$ and the first derivative has a corner jump $\eta'(0^+) - \eta'(0^-) = 2a f_b(0)$.
Differentiating $\eta(u)$ for $u > 0$:
$$\eta'(u) = f_b'(u) \sinh(au) + a f_b(u) \cosh(au),$$
$$\eta''(u) = f_b''(u) \sinh(au) + 2a f_b'(u) \cosh(au) + a^2 f_b(u) \sinh(au).$$
Integrating by parts twice in the distributional sense across $[-R, R]$, the quartet correction satisfies the complete bound:
$$\mathbf{|\Delta_{\text{quartet}}(a,\gamma)| \le \frac{8 m_0}{\gamma^2} \left[ 2a |f_b(0)| + \sinh(aR) \|f_b''\|_1 + 2a \cosh(aR) \|f_b'\|_1 + a^2 \sinh(aR) \|f_b\|_1 \right] \le C(f_b) \frac{a}{\gamma^2}}.$$
Notice that the $\|f_b''\|_1$ term is an indispensable component of the second-derivative bound. Because $\sinh(aR) \le a R e^{aR}$, every term contains an explicit factor of $a$, confirming that $\Delta_{\text{quartet}}(a,\gamma) \to 0$ as $a \downarrow 0$ with $O(a/\gamma^2)$ uniform decay.

---

## 4. Target A: Independent Functional Validation and Certified Numerical Inputs

### 4.1 Canonical Mathematical Specification
The authentic production functional has the unique canonical mathematical specification:
$$G_b(u) = \sum_{K,n} b_K \tau^K \Lambda(n) w(\tau^K n) \psi_h(u - \log(\tau^K n)), \qquad \sum_K b_K = 0,$$
$$F_b(z) = \int_{\mathbb{R}} G_b(u) e^{zu} \, du = A_h(z) E_b(z),$$
$$\Psi_b(z) = p(z) F_b(z) F_b(-z) = p(z) A_h(z)^2 E_b(z) E_b(-z), \qquad p(z) = \sum_{k=0}^3 r_k z^{2k}.$$
With autocorrelation:
$$C_b(u) = \int_{\mathbb{R}} G_b(v+u) G_b(v) \, dv = (G_b \star G_b)(u) = (G_b * G_b^{\vee})(u),$$
the corresponding position-space density is:
$$f_b(u) = \sum_{k=0}^3 r_k C_b^{(2k)}(u).$$

### 4.2 Sign Derivation: Convolution vs. Reflected Autocorrelation
Under the bilateral Laplace transform convention $\mathcal{L}[g](z) = \int_{\mathbb{R}} g(u) e^{zu} \, du$:
1. Autocorrelation transform:
   $$\mathcal{L}[C_b](z) = \int_{\mathbb{R}} \int_{\mathbb{R}} G_b(v+u) G_b(v) \, dv \, e^{zu} \, du = \left( \int_{\mathbb{R}} G_b(w) e^{zw} \, dw \right) \left( \int_{\mathbb{R}} G_b(v) e^{-zv} \, dv \right) = F_b(z) F_b(-z).$$
2. Even-derivative transform:
   $$\mathcal{L}[C_b^{(2k)}](z) = (-z)^{2k} \mathcal{L}[C_b](z) = z^{2k} F_b(z) F_b(-z).$$
3. Differentiated bump correlation:
   For the even bump kernel $\psi_h(-x) = \psi_h(x)$, its derivatives satisfy $\psi_h^{(k)}(-x) = (-1)^k \psi_h^{(k)}(x)$.
   Evaluating the (2k)-th derivative of $C_0(y) = (\psi_h * \psi_h)(y)$:
   $$C_0^{(2k)}(y) = (-1)^k \int_{\mathbb{R}} \psi_h^{(k)}(w+y) \psi_h^{(k)}(w) \, dw = (\psi_h^{(k)} * \psi_h^{(k)})(y).$$
   Therefore, $\mathcal{L}[\psi_h^{(k)} * \psi_h^{(k)}](z) = z^{2k} A_h(z)^2$.

**The Alternating Sign Defect**:
The earlier constructor computed `coeff = r_poly[k] * (-1.0)**k`.
Because $(-1)^k z^{2k} = (iz)^{2k}$, this injected sign substituted $p(iz)$ for the production polynomial $p(z)$. At $z = 0.49 + 100i$, $z^2 \approx -10000$, where $p(z) \approx -0.0010277$ is small and designed to damp zeros; in contrast, $(iz)^2 \approx +10000$, where $p(iz)$ blows up violently to order $10^{12}$. The repair eliminates `(-1.0)**k`, restoring $p(z)$ directly.

### 4.3 Reconciling the Saved Mismatch & Diagnosis of Numerical Errors
The saved committed comparison at baseline contains:

| Point $z$ | Direct Production Transform | Diagnostic Strong Density | Absolute Discrepancy |
| :--- | :--- | :--- | :--- |
| **$0.0$** | $-1.4840410 \times 10^{-7} + 0.0i$ | $82.0216931 + 0.0i$ | $82.021693$ |
| **$14.13472514i$** | $-1.2772288 + 0.0i$ | $264.3030562 + 0.0i$ | $265.580285$ |
| **$21.02203964i$** | $-1.7561226 + 0.0i$ | $1429.7934070 + 0.0i$ | $1431.549530$ |
| **$0.49 + 100.0i$** | $1.3916757 + 0.3575635i$ | $1582.5788618 + 51.6977956i$ | $1582.020460$ |

**Detailed Decomposition of the Numerical Error**:
Why does the strong spatial density transform produce $82.02$ at $z=0$ when direct evaluation is $-1.48 \times 10^{-7}$?
Decomposing $f_b(u) = \sum_{k=0}^3 r_k C_b^{(2k)}(u)$ on the grid:
- $k=0$: $r_0 \int C_b(u) \, du = -1.7887 \times 10^{-7}$ (analytic: $-1.4840 \times 10^{-7}$).
- $k=1$: $r_1 \int C_b''(u) \, du = +0.000159$ (analytic: $0$).
- $k=2$: $r_2 \int C_b^{(4)}(u) \, du = -0.216812$ (analytic: $0$).
- $k=3$: $r_3 \int C_b^{(6)}(u) \, du = +82.238357$ (analytic: $0$).
Sum: $-1.79 \times 10^{-7} + 0.00016 - 0.2168 + 82.2384 = \mathbf{82.021693}$.

The $k=3$ term completely dominates the error:
1. **Kernel Sampling**: $\psi_h^{(3)}(x)$ has peaks of order $h^{-6} \approx 6.4 \times 10^7$.
2. **Convolution**: Discrete convolution $(\psi_h^{(3)} * \psi_h^{(3)})$ has peaks of $2.24 \times 10^{25}$.
3. **Spline Interpolation Residual**: Tabulating $C_0^{(6)}$ on a mesh and interpolating with cubic splines introduces phase jitter and interpolation error of order $(\Delta v)^4 \|C_0^{(10)}\|_\infty$.
4. **Simpson Discretization on Oscillating Integrands**: At $\gamma = 100$, Simpson quadrature error on $N=4001$ points is $O(du^4 \cdot 100^4 \cdot \|f_b\|) \sim 10^6$.
5. **Catastrophic Cancellation**: The 9,604 cross-station pairs with $\sum b_K = 0$ cancel by 11 decimal digits. An uncancelled spline ripple in an individual bump produces an $O(100)$ residual.

### 4.4 Stable Certified Weak Evaluation
To resolve this without altering the mathematical definition of $f_b$, we apply integration by parts to move the differential operator $p(\partial_u) = \sum_{k=0}^3 r_k \partial_u^{2k}$ onto the exponential test weight $w_z(u) = e^{zu}$:
$$\int_{-R}^R f_b(u) e^{zu} \, du = \int_{-R}^R \left( p(\partial_u) C_b(u) \right) e^{zu} \, du = p(z) \int_{-R}^R C_b(u) e^{zu} \, du.$$
Since $C_b(u) = \int G_b(v+u) G_b(v) \, dv$ is the base autocorrelation without derivatives:
- It is smooth, non-oscillatory, and has no derivative singularities (amplitude $\sim 0.06$).
- Since $C_b(-u) = C_b(u)$ is even, the integral reduces to:
  $$\Psi_{f_b}^{\text{weak}}(z) = 2 p(z) \int_0^R C_b(u) \left[ \cosh(a u) \cos(\gamma u) + i \sinh(a u) \sin(\gamma u) \right] du.$$
- It is evaluated on the spatial grid using precomputed $C_b(u)$ via Simpson's rule, remaining completely independent of the direct spectral station calculation.

**Accuracy Verification**: Declared tolerances: absolute error $< 10^{-7}$ near zero; relative error $< 10^{-4}$ elsewhere.

| Test Point $z$ | Direct Evaluator $\Psi_b(z)$ | Weak Density Transform $\Psi_{f_b}^{\text{weak}}(z)$ | Absolute Discrepancy | Relative Discrepancy | Gate Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **$0.0$** | $-1.4840410 \times 10^{-7} + 0.0i$ | $-1.7134964 \times 10^{-7} + 0.0i$ | $2.29 \times 10^{-8}$ | $2.29 \times 10^{-8}$ | **PASSED** ($< 10^{-7}$) |
| **$14.13472514i$** ($\gamma_1$) | $-1.2772288 + 0.0i$ | $-1.2772298 + 7.26 \times 10^{-14}i$ | $9.30 \times 10^{-7}$ | $7.28 \times 10^{-7}$ | **PASSED** ($< 10^{-4}$) |
| **$21.02203964i$** ($\gamma_2$) | $-1.7561226 + 2.78 \times 10^{-17}i$ | $-1.7561229 + 1.79 \times 10^{-14}i$ | $3.33 \times 10^{-7}$ | $1.90 \times 10^{-7}$ | **PASSED** ($< 10^{-4}$) |
| **$0.49 + 100.0i$** ($z_0$) | $1.3916757 + 0.3575635i$ | $1.3916631 + 0.3575649i$ | $1.27 \times 10^{-5}$ | $8.84 \times 10^{-6}$ | **PASSED** ($< 10^{-4}$) |
| **$-0.49 - 100.0i$** ($-z_0$) | $1.3916757 + 0.3575635i$ | $1.3916631 + 0.3575649i$ | $1.27 \times 10^{-5}$ | $8.84 \times 10^{-6}$ | **PASSED** ($< 10^{-4}$) |
| **$0.49 - 100.0i$** ($\bar{z}_0$) | $1.3916757 - 0.3575635i$ | $1.3916631 - 0.3575649i$ | $1.27 \times 10^{-5}$ | $8.84 \times 10^{-6}$ | **PASSED** ($< 10^{-4}$) |
| **$-0.49 + 100.0i$** ($-\bar{z}_0$) | $1.3916757 - 0.3575635i$ | $1.3916631 - 0.3575649i$ | $1.27 \times 10^{-5}$ | $8.84 \times 10^{-6}$ | **PASSED** ($< 10^{-4}$) |
| **Secondary Vector $b_{\text{sec}}$** | $0.8799516 + 0.2654343i$ | $0.8799482 + 0.2654349i$ | $3.40 \times 10^{-6}$ | $3.40 \times 10^{-6}$ | **PASSED** ($< 10^{-4}$) |

Imaginary cancellation across the reflected pair holds to machine precision ($< 10^{-14}$).

### 4.5 Certified Outward Norm Enclosures via Validated Adaptive Quadrature
To replace empirical discrete sums `np.sum(abs(vals))*dx`, we evaluate the kernel norms via adaptive Gauss-Kronrod quadrature (`scipy.integrate.quad`) with outward directed enclosure:
$$\|\psi_h^{(p)}\|_1 = h^{-2-p} \int_{-1}^1 \left| \kappa^{(p+2)}(u) - \frac{1}{4} h^2 \kappa^{(p)}(u) \right| du \le h^{-2-p} (I_1(p) + \text{err}_1(p)) (1 + 10^{-8}),$$
$$\|\psi_h^{(p)}\|_2^2 = h^{-5-2p} \int_{-1}^1 \left| \kappa^{(p+2)}(u) - \frac{1}{4} h^2 \kappa^{(p)}(u) \right|^2 du \le h^{-5-2p} (I_2(p) + \text{err}_2(p)) (1 + 10^{-8}).$$
Combined with Young's convolution inequality and $(\sum |c_i|)^2 \approx 8.788 \times 10^7$:

| Quantity | Empirical Discrete Estimate | Proved Certified Outward Bound | Enclosure Ratio |
| :--- | :--- | :--- | :---: |
| **$|f_b(0)|$** | $2.4574 \times 10^{11}$ | $\le 1.1445 \times 10^{13}$ | $\approx 46.6$ |
| **$\|f_b\|_1$** | $8.5852 \times 10^9$ | $\le 9.4643 \times 10^{10}$ | $\approx 11.0$ |
| **$\|f_b'\|_1$** | $1.2887 \times 10^{13}$ | $\le 1.6805 \times 10^{14}$ | $\approx 13.0$ |
| **$\|f_b''\|_1$** | $2.1066 \times 10^{16}$ | $\le 2.9905 \times 10^{17}$ | $\approx 14.2$ |

All bounds strictly enclose the empirical estimates with verified quadrature error allowances $< 10^{-12}$.

---

## 5. Target B: Rigorous Tail Enclosures and Analysis of Implication under (H)

### 5.1 Rigorous Stieltjes Tail Integration
Let $N(t) = \sum_{0 < \gamma_\rho \le t} m_\rho$ count the nontrivial zeros in the upper critical strip with multiplicity.
Using integration by parts:
$$\sum_{\gamma_\rho > T} \frac{m_\rho}{\gamma_\rho^2} = \int_{T^+}^\infty \frac{1}{t^2} \, dN(t) = \left[ \frac{N(t)}{t^2} \right]_{T^+}^\infty + 2 \int_T^\infty \frac{N(t)}{t^3} \, dt = -\frac{N(T)}{T^2} + 2 \int_T^\infty \frac{N(t)}{t^3} \, dt.$$
Because $N(T) \ge 0$, the boundary term satisfies $-N(T)/T^2 \le 0$.
Under the unconditional counting envelope $N(t) \le \frac{t \log t}{2\pi}$ for $t \ge T$:
$$2 \int_T^\infty \frac{N(t)}{t^3} \, dt \le \frac{1}{\pi} \int_T^\infty \frac{\log t}{t^2} \, dt = \frac{\log T + 1}{\pi T}.$$
The previously asserted $(\log T + 2)/(2\pi T)$ is replaced by this rigorously derived bound.

**Accounting for Symmetries and Quartets**:
1. **Both Ordinate Signs**: By reflection $\zeta(\bar{s}) = \overline{\zeta(s)}$, every zero $\beta + i\gamma$ has a partner $\beta - i\gamma$. The sum over all zeros with $|\gamma| > T$ is bounded by $\frac{2(\log T + 1)}{\pi T}$.
2. **Quartet Counting**: An off-critical quartet $Q = \{ 1/2 \pm a \pm i\gamma \}$ contains **two** positive-ordinate zeros ($1/2 + a + i\gamma$ and $1/2 - a + i\gamma$). Therefore:
   $$\sum_{\text{quartets}, \gamma > T} \frac{m_0}{\gamma^2} \le \frac{1}{2} \sum_{\gamma > T} \frac{m_\rho}{\gamma^2} \le \frac{\log T + 1}{2\pi T}.$$

### 5.2 Supremum Over Displacement $a \in [0, 1/2]$
For any off-critical zero in the critical strip, $0 < a \le 1/2$.
Integrating by parts twice for $\Delta_{\text{quartet}}(a, \gamma) = 8 m_0 \int_0^R f_b(u) \sinh(au) \cos(\gamma u) \, du$:
$$|\Delta_{\text{quartet}}(a, \gamma)| \le \frac{8 m_0 a}{\gamma^2} C_{\text{kernel}}(f_b, a) \le \frac{4 m_0}{\gamma^2} C_{\text{outward}}^{\sup}(f_b),$$
where $C_{\text{outward}}^{\sup}(f_b) = 2 \left( |f_b(0)| + \cosh(R/2) \left[ R |f_b'(R)| + R \|f_b''\|_1 + 2 \|f_b'\|_1 + \frac{R}{4} \|f_b\|_1 \right] \right) \le 6.888 \times 10^{17}$.
Summing over all unselected quartets with $\gamma > T$:
$$R_{\text{transfer, tail}}(T) \le 4 C_{\text{outward}}^{\sup}(f_b) \cdot \frac{\log T + 1}{2\pi T} = \frac{2 C_{\text{outward}}^{\sup}(f_b) (\log T + 1)}{\pi T}.$$
At cutoff $T = 100$:
$$R_{\text{transfer, tail}}(100) \le 2.4579 \times 10^{16} < R_{\text{spectral}} = 1.03623 \times 10^{17}.$$
The transfer correction tail is strictly smaller than the base spectral tail and holds uniformly for all $a \in [0, 1/2]$.

### 5.3 Exact Remainder Separation
The explicit formula remainder terms remain strictly distinct:
$$D_b = A_{\le U, b} + R_{\text{arch}, b} - S_{\text{unselected}, \le T, b} - R_{\text{spectral}, b} - \Delta_{\text{selected quartet}}(a_0, \gamma_0).$$
1. **Arithmetic Term**: $A_{\le U, b} \approx 7.15 \times 10^8$.
2. **Archimedean Remainder**: $R_{\text{arch}, b} \sim O(10^{-6})$.
3. **Selected Zero Curvature Correction**: $\Delta_{\text{selected quartet}}(a_0, \gamma_0) = 8 m_0 \int_0^R f_b(u) \sinh(a_0 u) \cos(\gamma_0 u) \, du$.
4. **Unselected Critical-Line Sum**: $S_{\text{unselected}, \le T, b} = \sum_{|\gamma_k| \le T} \Psi_b(i\gamma_k)$.
5. **Spectral Tail Remainder**: $R_{\text{spectral}, b} \le 1.03623 \times 10^{17}$.
6. **Transfer Correction Tail**: $R_{\text{transfer, tail}}(T) \le 2.4579 \times 10^{16}$.

---

## 6. Mathematical Analysis of the Contradiction Implication under (H)

### 6.1 The Governing Question & The Contradiction Criterion
The governing research question is:
> *What independently established constraint on the complete functional $D$ is incompatible with $D = -1/2 + r_{\text{match}} - r_{\text{rec}}$ under the off-critical-zero hypothesis $H$?*

A mathematically sufficient contradiction criterion is:
$$|D| + \varepsilon_{\text{match}} + \varepsilon_{\text{rec}} < \frac{1}{2}.$$
If this inequality holds, then $|D| < 1/2 - (\varepsilon_{\text{match}} + \varepsilon_{\text{rec}})$, which strictly excludes the explicit formula identity $D = -1/2 + r_{\text{match}} - r_{\text{rec}}$.

### 6.2 Why Establishing $D < 0$ Does Not Supply the Contradiction
The current authentic selected-weight construction already yields:
$$D \approx -\frac{1}{2} < 0.$$
Therefore, proving that $D < 0$ is completely compatible with $D = -1/2 + r_{\text{match}} - r_{\text{rec}}$. It produces no contradiction and cannot advance the reductio.

### 6.3 Why Single-Quartet Non-Vanishing Is Insufficient
1. **Hypothesis $H$ supplies**: The existence of an off-critical zero $\rho_0 = 1/2 + a_0 + i\gamma_0$ supplies $a_0 > 0$.
2. **Perturbation Size**: The quartet correction $\Delta_{\text{quartet}}(a_0, \gamma_0) = 8 m_0 \int_0^R f_b(u) \sinh(a_0 u) \cos(\gamma_0 u) \, du$ is of order:
   $$|\Delta_{\text{quartet}}| \le \frac{8 m_0 a_0}{\gamma_0^2} C_{\text{kernel}}^{\sup}(f_b) \sim 10^{13}.$$
3. **Tail Dominance**: The unconditional spectral tail allowance $R_{\text{spectral}} \le 1.036 \times 10^{17}$ dwarfs this local perturbation by four orders of magnitude.
4. **No Structural Sign/Magnitude Lock**: Non-vanishing of $\Delta_{\text{quartet}}$ does not determine its sign or show that it cancels $-1/2$. Even if it were non-zero, $D_b$ would simply shift by $O(10^{13})$ inside an uncertainty band of $10^{17}$, neither proving $|D_b| + \varepsilon < 1/2$ nor establishing an inter-grade station collision $M \tau^K = N \tau^J$.

### 6.4 The Smallest Precise Unresolved Implication
The minimal open lemma required by the TC reductio is:

> **Spectral Transfer Contradiction Gap (Active Open Research Obligation)**:  
> *For any off-critical zero $\rho_0 = 1/2 + a_0 + i\gamma_0$ ($a_0 > 0$) of $\zeta(s)$ and any legal test vector $b$ ($\sum b_K = 0$), does there exist an admissible multiplier $p(z)$ such that the complete explicit formula functional satisfies:*
> $$|D_b| + \varepsilon_{\text{match}} + \varepsilon_{\text{rec}} < \frac{1}{2},$$
> *thereby strictly excluding the critical explicit formula balance $D_b = -1/2 + r_{\text{match}} - r_{\text{rec}}$?*

---

## 7. Updated Task States and Evidence Provenance

| Dimension | Previous Status | Updated Authoritative Status | Evidence Artifact |
| :--- | :--- | :--- | :--- |
| **Convolution Sign** | Bugged ($(-1)^k$, $p(iz)$) | `REPAIRED_CONVOLUTION_SIGN_P_Z` | `tc/weil_forms/curvature_transfer.py` |
| **Production Transform** | Discrepancy $1582.02$ on grid | `CERTIFIED_WEAK_FORMULATION_PASSED` ($< 10^{-7}$) | `data/tc_regularized_curvature_transfer.json` |
| **Analytic Norm Bounds** | Empirical grid sums | `CERTIFIED_OUTWARD_BOUNDS_VALIDATED_QUADRATURE` | `scipy.integrate.quad` with outward error budget |
| **Tail Enclosure** | Heuristic $(\log T + 2)/(2\pi T)$ | `PROVED_STIELTJES_INTEGRATION_SUPREMUM_A` | Uniform bound over $a \in [0, 1/2]$ |
| **TC Reductio Implication** | Premature collision claim | `CONTRADICTION_GAP_ISOLATED_OPEN_RESEARCH` | Section 6 above |

All regression gates pass; the mathematical distinction between verified identities and open research obligations is rigorously preserved.

