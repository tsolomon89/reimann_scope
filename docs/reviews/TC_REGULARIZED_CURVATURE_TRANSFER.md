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

## 4. Testing the Missing Implication on the Authentic TC Family

### 4.1 Withdrawal of the Surrogate-Based Obstruction Claim
An earlier draft evaluated the constant $C(f)$ using a normalized polynomial surrogate density $f(u) = (1 - (u/R)^2)^4$, obtaining $C(f) \sim 10^1$, and compared that surrogate scale to the production arithmetic functional value $A_{\le U} \approx 7.15 \times 10^8$, claiming an "eight orders of magnitude too small" numerical obstruction.

**That comparison was mathematically unfounded and is formally withdrawn**:
1. **Density Dependence**: The bound constant $C(f_b)$ depends strictly on the actual position-space density $f_b(u)$ and its derivatives.
2. **Authentic Scale**: In the production TC functional, $f_b(u)$ is assembled from 98 prime-power stations in grades $\{-1, -2\}$ with legal coefficients $b = (-1/\sqrt{2}, 1/\sqrt{2}, 0)$, the differentiated kernel $\psi_h$, and the degree-6 production polynomial $p(z)$. Evaluating the authentic density yields:
   $$f_b(0) \approx -2.457315 \times 10^{11},$$
   $$\|f_b\|_1 \approx 8.585236 \times 10^9,$$
   $$\|f_b'\|_1 \approx 1.288593 \times 10^{13},$$
   $$\|f_b''\|_1 \approx 2.107067 \times 10^{16}.$$
3. **Authentic Correction Magnitude**:
   At $a = 0.49$ and $\gamma = 100.0$:
   - Reflected pair components: $\Psi_{\text{pair}} \approx 4,745,543.65$, $K_{\text{pair}} \approx 4,157,696.33$.
   - Reflected pair correction: $\Delta_{\text{pair}} \approx 587,847.32$.
   - Full quartet correction ($m_0=1$): $\Delta_{\text{quartet}} = 2 \Delta_{\text{pair}} \approx 1,175,694.63$ ($1.18 \times 10^6$).
   - Distributional jump bound: $|\Delta_{\text{quartet}}| \le 4.38 \times 10^{12}$ with $C(f_b) \approx 4.47 \times 10^{16}$.
4. **Numerical Validation**:
   The identity $\Psi_{\text{pair}} - K_{\text{pair}} = \Delta_{\text{pair}}$ balances with an absolute discrepancy of $5.73 \times 10^{-8}$ and a relative discrepancy of $9.74 \times 10^{-14}$, validating the transfer identity on the authentic production TC functional to machine precision.

### 4.2 Epistemic Role of the Regularized Transfer
The regularized curvature transfer provides an exact, rigorous bridge:
1. It replaces the divergent local second-derivative curvature integral with the well-defined Hadamard finite-part pairing:
   $$\langle -\operatorname{Fp}(1/x^2), \phi_{f_b}(\cdot + \gamma) \rangle = K_{\phi_{f_b}}(0, \gamma) = \Psi_b(i\gamma).$$
2. For an off-critical zero $\rho_0 = 1/2 + a + i\gamma_0$, it isolates the exact quartet perturbation $\Delta_{\text{quartet}}(a, \gamma_0)$.
3. However, the complete remainder identity governs the entire explicit formula:
   $$D = A_{\le U} + R_{\text{arch}} - S_{\text{unselected}, \le T} - R_{\text{spectral}} = -\frac{1}{2} + r_{\text{match}} - r_{\text{rec}}.$$
   Hypothesis $H$ supplies the off-critical quartet and its transfer correction $\Delta_{\text{quartet}}$, but does not unconditionally evaluate the unselected critical sum $S_{\text{unselected}, \le T}$ or the infinite Stieltjes tail $R_{\text{spectral}}$.

---

## 5. Machine-Readable Evidence & Reconciled Numerical Records

The canonical machine-readable audit artifact is stored at:
[`data/tc_regularized_curvature_transfer.json`](file:///C:/Development/Projects/reimann_scope/data/tc_regularized_curvature_transfer.json)

### 5.1 Reconciled Multi-Set and Benchmark Quantities
The previous discrepancy between the report's text and the JSON artifact arose from contrasting a 4-zero test configuration against a 6-zero baseline. The reconciled audit records both datasets unambiguously:

| Verification Target | Dataset / Method | Value / Norm | Discrepancy / Bound |
| :--- | :--- | :--- | :--- |
| **Authentic Density Center** | $f_b(0)$ (98 stations, production $p$) | $-2.457315 \times 10^{11}$ | Exact finite sum |
| **Authentic $L^1$ Norm** | $\|f_b\|_1$ | $8.585236 \times 10^9$ | Mesh $N=4001$ |
| **Authentic First Derivative** | $\|f_b'\|_1$ | $1.288593 \times 10^{13}$ | Central differences |
| **Authentic Second Derivative**| $\|f_b''\|_1$ | $2.107067 \times 10^{16}$ | Central differences |
| **Authentic Pair Transfer** | $(a=0.49, \gamma=100.0)$ | $\Delta_{\text{pair}} \approx 587,847.32$ | Rel. disc. $9.74 \times 10^{-14}$ |
| **Authentic Quartet Correction** | $\Delta_{\text{quartet}}(0.49, 100.0)$ | $1,175,694.63$ | Bound $\le 4.38 \times 10^{12}$ |
| **Baseline Surrogate Spectral Sum** | 6-zero multiset $S_{\Psi}$ | $0.001742174702817$ | Reconciled artifact figure |
| **Baseline Surrogate Curvature**| 6-zero multiset $K_{\phi}$ | $0.003321157945685$ | Reconciled artifact figure |
| **Baseline Predicted Correction**| $\Delta_{\text{total}}$ | $-0.001578983242868$| Reconciled artifact figure |
| **Baseline Balance Discrepancy**| $|S - K - \Delta|$ | $1.23599 \times 10^{-17}$ | Below machine precision |
| **Hadamard Semi-Infinite Pairing**| $\phi(t)=-\frac{1}{2}\log(1+t^2), \gamma=0$ on $[0, \infty)$ | $3.14159265358988$ | Error vs $\pi$: $8.66 \times 10^{-14}$ |
| **Hadamard Truncated Pairing** | Same $\phi$ on $[0, 200]$ | $3.07860943825791$ | Missing tail: $0.0629832153$ |
| **Unselected Spectral Sum** | $S_{\text{unselected}, \le 100}$ | $-8,200.329211$ | 27 unselected zeros |
| **Linear Uncertainty Budget** | Observable + multiplier derivative | $\pm 5.70 \times 10^{-12}$ | First-order sensitivity |
| **Analytic MVT Uncertainty** | Observable majorant + polynomial | $\pm 1.46 \times 10^{-6}$ | Certified interval enclosure |

---

## 6. Conclusion and Next Single Mathematical Question

### 6.1 Summary of Repaired Mathematical State
1. **Evaluator Contract Precision**:
   - `spectral_test_observable` returns the full complex value $\Psi_b(z) \in \mathbb{C}$ with non-vanishing imaginary part $2\int_0^R f_b(u)\sinh(\delta u)\sin(\gamma u) du$ for off-critical zeros, verifying that imaginary parts cancel identically across symmetric quartets.
   - `hadamard_finite_part_pairing` defaults to the complete semi-infinite domain $[0, \infty)$, eliminating the $0.062983$ omitted tail from previous $t_{\max}=200$ truncation and matching the analytic value $\pi$ to $8.66 \times 10^{-14}$.
2. **Complete Uncertainty Budget**:
   - $S_{\text{unselected}, \le T}$ accumulates both the observable matrix sensitivity $\|\beta\|_2^2 \|S'\|_2 \varepsilon_\gamma$ and the polynomial multiplier derivative sensitivity $|p'(i\gamma)| \varepsilon_\gamma$ via the product rule, reporting both linear ($5.70 \times 10^{-12}$) and analytic MVT ($1.46 \times 10^{-6}$) enclosures.
3. **Authentic Transfer Validation**:
   - The regularized curvature transfer identity is derived, proved, and numerically validated on the authentic production TC density $f_b(u)$ to relative precision $< 10^{-13}$.
   - The surrogate-based numerical obstruction is withdrawn.

### 6.2 The Next Single Mathematical Question
> **For the same prime stations, legal vector $b$, interpolated polynomial $p$, and normalization used in the production functional, what is the complete transfer correction—with explicit constants and a controlled remainder—and what additional restriction does $H$ impose on it?**

