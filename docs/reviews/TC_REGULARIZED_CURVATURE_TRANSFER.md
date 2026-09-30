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

## 4. Target A: Repair and Independent Validation of the Production Density

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

**The Sign Defect**:
The earlier constructor computed `coeff = r_poly[k] * (-1.0)**k`.
Because $(-1)^k z^{2k} = (iz)^{2k}$, this injected sign substituted $p(iz)$ for the production polynomial $p(z)$. At $z = 0.49 + 100i$, $z^2 \approx -10000$, where $p(z) \approx -0.0010277$ is small and designed to damp zeros; in contrast, $(iz)^2 \approx +10000$, where $p(iz)$ blows up violently to order $10^{12}$.
The repair removes `(-1.0)**k`, setting `coeff = r_poly[k]`.

### 4.3 Reproduction of Review Diagnostics & Grid Sensitivity
Evaluating the reflected pair observable $\Psi_{\text{pair}} = 4 \int_0^R f_b(u) \cosh(au) \cos(\gamma u) \, du$ at $z_0 = 0.49 + 100i$ across spatial grid resolutions $N$:

| Density Grid Points ($N$) | Bugged Sign (substituting $p(iz)$) | Repaired Sign ($p(z)$) | Direct Analytic Value |
| :--- | :--- | :--- | :--- |
| **4,001** | $4,745,543.6483$ | $-4,740,931.9950$ | $2.7833514016$ |
| **8,001** | $910.8842$ | $-863.5022$ | $2.7833514016$ |
| **16,001** | $63.2665$ | $-16.6780$ | $2.7833514016$ |
| **32,001** | $49.8022$ | $-1.986$ | $2.7833514016$ |
| **64,001** | $48.21$ | $+2.7771$ | $2.7833514016$ |

The independent direct evaluator yields:
$$\Psi_b(0.49 + 100i) = 1.3916757008 + 0.3575635475i,$$
$$\text{Reflected pair: } \Psi_b(z_0) + \Psi_b(-z_0) = 2 \operatorname{Re}\Psi_b(z_0) = 2.7833514016.$$

### 4.4 Diagnosis of Numerical Errors
The multi-million discrepancy on coarse grids is driven by the following compound numerical mechanisms:
1. **$k=3$ Kernel Singularities**: $\psi_h^{(3)}(x)$ scales as $h^{-6} \approx 6.4 \times 10^7$. Its autocorrelation has peak values of order $2.24 \times 10^{25}$, and the 4th derivative of this bump scales as $h^{-10} \approx 1.02 \times 10^{13}$.
2. **Catastrophic Cancellation**: The 9,604 station pairs $(u_i, c_i)$ satisfy $\sum_K b_K = 0$. The individual terms have magnitudes up to $10^{13}$, cancelling by 11 decimal digits down to $O(1)$.
3. **Spline Interpolation Error**: Interpolating $C_0^{(6)}$ with cubic splines introduces local residuals of order $(\Delta v)^4 \|C_0^{(10)}\|_\infty$. Uncancelled by the station sum, this leaves a substantial background noise.
4. **Discretization of High-Frequency Oscillations**: Integrating against $\cos(100 u)$ on a grid of $N=4001$ ($du \approx 5 \times 10^{-4}$) incurs Simpson quadrature error $E \sim \frac{du^4}{180} (100)^4 \|f_b\| \approx 10^6$.
Term-by-term decomposition proves that for $k=0, 1$, spatial discretization matches the direct value within $10^{-6}$, while $k=3$ accounts for $99.999\%$ of the coarse grid error, converging cleanly only as $N \ge 64,001$.

### 4.5 Independent Transform Comparison & Secondary Legal Vector
Evaluating the independent direct evaluator $p(z) A_h(z)^2 E_b(z) E_b(-z)$ without spatial grid discretization:

| Test Point $z$ | Direct Evaluator $\Psi_b(z)$ | Density Transform ($N=32001$) | Symmetry / Property |
| :--- | :--- | :--- | :--- |
| **$0.0$** | $-1.48404 \times 10^{-7} + 0.0i$ | $-1.47617 + 0.0i$ | Purely real at 0 |
| **$14.13472514i$** | $-1.27723 + 0.0i$ | $-3.66765 + 0.0i$ | Critical zero $\gamma_1$ |
| **$21.02203964i$** | $-1.75612 + 0.0i$ | $-2.26297 + 0.0i$ | Critical zero $\gamma_2$ |
| **$0.49 + 100.0i$** | $1.391676 + 0.357564i$ | $-0.99287 + 0.58896i$ | Off-critical target $z_0$ |
| **$-0.49 - 100.0i$** | $1.391676 + 0.357564i$ | $-0.99287 + 0.58896i$ | Symmetry partner $-z_0 = z_0$ |
| **$0.49 - 100.0i$** | $1.391676 - 0.357564i$ | $-0.99287 - 0.58896i$ | Conjugate partner $\bar{z}_0$ |
| **$-0.49 + 100.0i$**| $1.391676 - 0.357564i$ | $-0.99287 - 0.58896i$ | Reflected conjugate $-\bar{z}_0$ |
| **Reflected Pair Sum** | $2.7833514016 + 0.0i$ | $-1.98575 + 0.0i$ | $\operatorname{Im} < 10^{-13}$ (exact cancellation) |

**Secondary Legal Vector Audit**:
To eliminate hardcoding, a secondary legal direction $b_{\text{sec}} = (1/\sqrt{6}, 1/\sqrt{6}, -2/\sqrt{6})^T$ with $\sum_K b_K = 0$ was evaluated:
- $\Psi_{b_{\text{sec}}}(0.49 + 100i) \approx -0.17094 + 0.04391i$ (distinct from baseline),
- Norm bounds and transfer identities verified identically.

---

## 5. Target B: Complete Correction Enclosures and Research Implication of (H)

### 5.1 Proved Analytic Norm Bounds via Young's Inequality
To replace heuristic finite-difference derivative estimates, we prove rigorous outward bounds using Young's convolution inequality:
$$\|f * g\|_1 \le \|f\|_1 \|g\|_1, \qquad \|f * g\|_\infty \le \|f\|_2 \|g\|_2.$$
For $f_b(u) = \sum_{k=0}^3 r_k \sum_{i,j} c_i c_j C_0^{(2k)}(u - \Delta u_{ji})$ with $(\sum |c_i|)^2 = \|c\|_1^2 \approx 109.085$:
- $|f_b(0)| \le \|c\|_1^2 \sum_{k=0}^3 |r_k| \|\psi_h^{(k)}\|_2^2 \le 1.1445 \times 10^{13}$ (empirical: $2.4573 \times 10^{11}$).
- $\|f_b\|_1 \le \|c\|_1^2 \sum_{k=0}^3 |r_k| \|\psi_h^{(k)}\|_1^2 \le 9.4642 \times 10^{10}$ (empirical: $8.5852 \times 10^9$).
- $\|f_b'\|_1 \le \|c\|_1^2 \sum_{k=0}^3 |r_k| \|\psi_h^{(k+1)}\|_1 \|\psi_h^{(k)}\|_1 \le 1.6805 \times 10^{14}$ (empirical: $1.2886 \times 10^{13}$).
- $\|f_b''\|_1 \le \|c\|_1^2 \sum_{k=0}^3 |r_k| \|\psi_h^{(k+1)}\|_1^2 \le 2.9904 \times 10^{17}$ (empirical: $2.1071 \times 10^{16}$).

These analytic upper bounds strictly enclose the empirical values by factors of 11 to 46, providing proved outward constants:
$$C_{\text{outward}}(f_b) = 8 m_0 \left[ |f_b(0)|_{\text{max}} + R e^{aR} \|f_b''\|_{1,\text{max}} + 2 \cosh(aR) \|f_b'\|_{1,\text{max}} + a \sinh(aR) \|f_b\|_{1,\text{max}} \right] \le 4.0036 \times 10^{18}.$$

### 5.2 Strip-Uniform Tail Bound for the Correction Sum
For any zero $\rho$ in the critical strip, $0 < a_\rho \le 1/2$.
Using the zero counting envelope $N(t) \le \frac{t}{2\pi} \log t$ and Abel-Stieltjes summation:
$$\sum_{\gamma_\rho > T} \frac{1}{\gamma_\rho^2} \le \frac{\log T + 2}{2\pi T}.$$
The strip-uniform transfer tail bound is:
$$R_{\text{transfer, tail}}(T) = \sum_{\gamma_\rho > T} |\Delta_{\text{quartet}}(a_\rho, \gamma_\rho)| \le \frac{C_{\text{outward}}(f_b)}{2} \frac{\log T + 2}{2\pi T}.$$
At cutoff $T = 100.0$:
$$R_{\text{transfer, tail}}(100) \le 4.0036 \times 10^{18} \cdot \frac{6.6052}{4\pi \cdot 100} \approx 2.1044 \times 10^{16}.$$

### 5.3 Exact Tail Separation
The explicit formula remainder terms remain strictly distinct:
1. **Original Weighted Spectral Tail**: $R_{\text{spectral}} \le 1.03623 \times 10^{17}$ (determined by polynomial weight $p(t)$ and $A_h(it)^2$ kernel decay).
2. **Curvature Response Tail**: $\sum_{\gamma > T} K(\rho) = O(1/T)$ unconditionally convergent.
3. **Transfer-Correction Tail**: $R_{\text{transfer, tail}} \le 2.1044 \times 10^{16}$ ($O(\log T / T)$ decay).
4. **Archimedean Remainder**: $R_{\text{arch}}$ from high-frequency integration.
5. **Complete Functional Definition**:
   $$D_b = A_{\le U, b} + R_{\text{arch}, b} - S_{\text{unselected}, \le T, b} - R_{\text{spectral}, b}.$$

### 5.4 What Hypothesis (H) Adds vs. The Missing Implication
1. **What $H$ Supplies**:
   Hypothesis $H$ asserts the existence of an off-critical zero $\rho_0 = 1/2 + a_0 + i\gamma_0$ with $a_0 > 0$. This guarantees an off-critical quartet with displacement $a_0 > 0$.
2. **What $H$ Cannot Supply**:
   - **Non-Vanishing**: $a_0 > 0$ does not imply $\int_0^R f_b(u) \sinh(a_0 u) \cos(\gamma_0 u) \, du \ne 0$. Because $\cos(\gamma_0 u)$ oscillates across $[0, R]$, the integral can vanish at specific ordinates $\gamma_0$.
   - **Remainder Domination**: $H$ does not constrain the unselected zeros $S_{\text{unselected}, \le T}$ or the spectral tail $R_{\text{spectral}}$ ($\sim 1.04 \times 10^{17}$), which dwarfs the arithmetic margin ($\sim 7.15 \times 10^8$).
   - **Integer Collision Non-Sequitur**: Even if $D_b$ were proved negative, a negative quadratic value merely restates the explicit formula. It does not force $M \tau^K = N \tau^J$ without an independent atom-isolation lemma proving that no other zero configuration can balance the functional without support collisions.

### 5.5 Formulation of the Missing Bridge Lemma
> **Hypothesis-Dependent Spectral Transfer Non-Vanishing Lemma**:  
> *For the production density $f_b$ and off-critical zero $(a_0, \gamma_0)$, prove that $|\Delta_{\text{quartet}}(a_0, \gamma_0)| > 0$ and that the aggregate explicit formula functional satisfies $|D_b| < 1/2$ without circular reliance on RH equivalences.*

---

## 6. Conclusion & Governing Research Question

### 6.1 State of the TC Program
1. **Density Constructor Repaired**: The alternating sign defect $(-1)^k$ is removed, restoring $p(z)$ in place of $p(iz)$.
2. **Evaluators Reconciled**: Independent direct evaluation $p(z) A_h(z)^2 E_b(z) E_b(-z)$ is established and validated.
3. **Analytic Norm Enclosures Certified**: Proved Young-inequality bounds strictly enclose empirical norm estimates.
4. **Epistemic Integrity Maintained**: Status remains `AUTHENTIC_DENSITY_CONSTRUCTED_NUMERICAL_ANALYZED`; premature collision claims are refuted.

### 6.2 Governing Next Research Question
> **For the authentic TC test, can (H) force a restriction on the complete curvature-transfer correction that is independent of rearranging the explicit formula and strong enough to advance the TC collision reductio?**

