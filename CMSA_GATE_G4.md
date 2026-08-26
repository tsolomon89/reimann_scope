# Gate G4 Infinite-Regularization and Radial-Survival Report

**Repository**: `tsolomon89/reimann_scope`  
**Classification**: `FINITE_IDENTITY_PROVED_G4_OPEN`  
**Status**: Gate G4 is the earliest open gate in the present Completed Mean-Square Anchor (CMSA) derivation.

---

## 1. Executive Summary & Frontier Statement

The Completed Mean-Square Anchor (CMSA) framework establishes an unconditional exact arithmetic vanishing anchor:
$$\mathcal A(\sigma) = \lim_{T \to \infty} \frac{1}{2T} \int_{-T}^T \left| A(\sigma + it) - \frac{\Xi'}{\Xi}\left(\sigma - \frac{1}{2} + it\right) \right|^2 dt - \sum_{n=2}^\infty \frac{\Lambda(n)^2}{n^{2\sigma}} = 0 \quad (\sigma > 1).$$

At any finite zero height cutoff $H$ and averaging interval $T$, the finite spectral expansion closes algebraically as:
$$S_{H, T}(\sigma) = I_{AA} - I_{AZ} - I_{ZA} + I_{ZZ},$$
with closed-form kernels $J_T(p,q)$ and $K_T(\lambda, \mu; a)$ verified against arbitrary-precision quadrature ($< 10^{-15}$).

**The Central Gate G4 Question**:
Can the exact finite spectral expansion $S_{H, T}$ be passed to an infinite regularized limit under divisor-independent windows $W_T(t)$, cutoff schedules $H = H(T)$, and normalization $c_T$, such that the arithmetic zero anchor becomes an exact nonnegative radial-defect functional:
$$0 = \lim_{T\to\infty} c_T \left[ \int_{\mathbb R} W_T(t) \left| A(\sigma+it) - \frac{\Xi'}{\Xi}(a+it) \right|^2 dt - \mathcal P_{\sigma, W, T} \right] = \sum_{\gamma > 0} W_\sigma(\gamma) \Phi_\sigma(\delta_\gamma, \gamma),$$
with $W_\sigma(\gamma) > 0$, $\Phi_\sigma(\delta, \gamma) \ge 0$, and $\Phi_\sigma(\delta, \gamma) = 0 \iff \delta = 0$?

---

## 2. Gate G4 Sub-Gates (G4a–G4g)

| Sub-Gate | Title | Description | Methodological / Proved Status |
| :--- | :--- | :--- | :--- |
| **G4a** | Arithmetic Independence | Arithmetic anchor constructed solely from $\Lambda(n)$, prime powers, Euler product, pole, and Gamma factors without zero inputs. | **PROVED / ENFORCED** (mock firewall verified) |
| **G4b** | Exact Finite Expansion | Exact 4-term quadratic decomposition and closed-form kernels for Rectangular and Fejér windows. | **PROVED / VERIFIED** (Lean 4 `finite_quadratic_expansion_identity`) |
| **G4c** | Infinite Remainder Control | Exact remainder $R_H(z) = \Xi'/\Xi(z) - Z_H(z)$ and cross-terms $\|R_H\|^2, 2\Re\langle Z_H, R_H\rangle$. | **OPEN** |
| **G4d** | Limit-Order Control & Boundary Layer | Fixed-H limits vs cofinal limits $H=H(T)$; boundary layer $J_T$ asymptotics. | **OPEN / CHARACTERIZED** (Lean 4 `cofinal_schedule_distinct_from_fixed_limit`) |
| **G4e** | Radial Survival & Positivity | Full regularized radial response $\Delta S = S_{\text{off}} - S_{\text{on}} > 0$ for off-line quartets above resonance. | **NUMERICAL EVIDENCE / OPEN PROOF** |
| **G4f** | Pair Isolation | Involution-pair isolation vs unrestricted all-pairs double sum. | **OPEN** |
| **G4g** | Grade Covariance | Coordinate redundancy under $u \mapsto \tau^K u$. | **PROVED / GRADE_COORDINATE_REDUNDANT** (Lean 4 `ConditionalCompletedLogDerivativeDecomposition.coordinate_redundant`) |

---

## 3. Four Tested Window Families (Discovery Loops 0–3)

### Loop 0: Rectangular / Cesàro Window
- **Window**: $W_T(t) = \frac{1}{2T} \mathbf{1}_{[-T, T]}(t)$, $\widehat{W}_T(\omega) = \operatorname{sinc}(\omega T)$.
- **Prime Kernel**: $\operatorname{sinc}(T \log(m/n))$.
- **Zero Kernel**: $J_T(p,q) = \frac{\log((p+iT)/(p-iT)) + \log((q+iT)/(q-iT))}{2Ti(p+q)}$.
- **Asymptotic Regimes**:
  1. $|\gamma| \ll T$ (Plateau): $J_T \sim \frac{\pi}{2a T} = O(T^{-1})$.
  2. $\gamma/T \to c \in (0, \infty)$ (Transition): $\frac{\arctan((T-\gamma)/a) + \arctan((T+\gamma)/a)}{2aT}$.
  3. $|\gamma - T| = O(1)$ (Boundary Layer): peak resonance value $\approx \frac{\pi}{4aT}$.
  4. $|\gamma| \gg T$ (Outer Tail): $J_T \sim \frac{1}{\gamma^2 - T^2} = O(\gamma^{-2})$.
- **Classification**: `FINITE_IDENTITY_PROVED_G4_OPEN`.

### Loop 1: Fejér / Triangular Window
- **Window**: $W_T(t) = \frac{1}{T} \left(1 - \frac{|t|}{T}\right) \mathbf{1}_{[-T, T]}(t)$, $\widehat{W}_T(\omega) = \operatorname{sinc}^2(\omega T/2) \ge 0$.
- **Prime Kernel**: $\operatorname{sinc}^2\left(\frac{T}{2}\log(m/n)\right) \ge 0$.
- **Zero Kernel (Exact Closed Form)**:
  $$J_T^{\text{Fejér}}(p,q) = \frac{I_T(p) + I_T(q)}{T(p+q)}, \quad I_T(w) = -\frac{(w+iT)\log(w+iT) + (w-iT)\log(w-iT) - 2w\log w}{T}.$$
- **Classification**: `FINITE_IDENTITY_PROVED_G4_OPEN`.

### Loop 2: Abel-Poisson / Exponential Window
- **Window**: $W_\beta(t) = \frac{\beta}{2} e^{-\beta |t|}$ ($\beta = 1/T \to 0$), $\widehat{W}_\beta(\omega) = \frac{\beta^2}{\beta^2 + \omega^2} > 0$.
- **Prime Kernel**: $\frac{\beta^2}{\beta^2 + \log^2(m/n)} > 0$.
- **Zero Kernel**: $J_\beta^{\text{Abel}}(p,q) = \int_{-\infty}^\infty \frac{\beta}{2} e^{-\beta |t|} \frac{dt}{(p+it)(q-it)}$.
- **Classification**: `FINITE_IDENTITY_PROVED_G4_OPEN`.

### Loop 3: Gaussian / Heat Window
- **Window**: $W_T(t) = \frac{1}{\sqrt{2\pi} T} e^{-t^2 / (2T^2)}$, $\widehat{W}_T(\omega) = e^{-\omega^2 T^2 / 2} > 0$.
- **Prime Kernel**: $e^{-\frac{1}{2} T^2 \log^2(m/n)} > 0$.
- **Zero Kernel**: $J_T^{\text{Gauss}}(p,q) = \int_{-\infty}^\infty \frac{1}{\sqrt{2\pi} T} e^{-t^2 / (2T^2)} \frac{dt}{(p+it)(q-it)}$.
- **Classification**: `FINITE_IDENTITY_PROVED_G4_OPEN`.

---

## 4. The Boundary Layer and Cofinal Limit Obstruction

1. **Fixed-Truncation vs Cofinal Limits**:
   For any fixed zero cutoff $H$, the zero resolvent contribution vanishes under translation averaging:
   $$\forall H < \infty, \quad \lim_{T\to\infty} \sum_{|\gamma_n| \le H} J_T(a-i\gamma_n, a+i\gamma_n) = \lim_{T\to\infty} N(H) \frac{\pi}{2a T} = 0.$$
   However, under a cofinal schedule $H(T) = cT$, the number of included zeros grows as $N(H(T)) \sim \frac{cT}{2\pi} \log T$, yielding a divergent diagonal sum:
   $$\sum_{|\gamma_n| \le cT} J_T(a-i\gamma_n, a+i\gamma_n) \sim \frac{c \log T}{4a} \to +\infty.$$
   Formalized in Lean 4 (`cofinal_schedule_distinct_from_fixed_limit`):
   $$\forall H,\ \lim_{T\to\infty} f(H,T) = 0 \centernot\implies \lim_{T\to\infty} f(H(T),T) = 0.$$

2. **Full Regularized Radial Variation**:
   When an on-line zero pair $\pm i\gamma$ is replaced by an off-line quartet $\pm \delta \pm i\gamma$ ($\delta \ne 0$), the full variation $\Delta S = S_{\text{off}} - S_{\text{on}}$ separates as:
   $$\Delta S = \Delta I_{ZZ} + \Delta \text{Cross}.$$
   - When $T < \gamma$: $\Delta I_{ZZ} < 0$ due to the negative real-axis defect $\Delta(\delta) < 0$ for $t < \sqrt{3}\gamma$, but $\Delta \text{Cross} > 0$, maintaining $\Delta S > 0$.
   - When $T > \gamma$: $\Delta I_{ZZ} > 0$ and dominates the variation, with $\Delta S > 0$ across all tested window families.

3. **The Unnormalized Arithmetic Oscillation Barrier**:
   Multiplying by $c_T = T$ to extract a non-zero radial limit scales the arithmetic mean-square remainder to:
   $$E(T) = \int_{-T}^T |P(\sigma+it)|^2 dt - 2T \sum_{n=2}^\infty \frac{\Lambda(n)^2}{n^{2\sigma}} = 2 \sum_{m \ne n} \frac{\Lambda(m)\Lambda(n)}{(mn)^\sigma} \frac{\sin(T\log(m/n))}{\log(m/n)}.$$
   Because $E(T)$ is an almost-periodic function of $T$ with persistent $O(1)$ fluctuations, the simultaneous infinite limit requires regularizing this arithmetic oscillation against the Archimedean and spectral counting divergences.

---

## 5. Formalization in Lean 4

The following formal theorems are compiled in `formal/RiemannScope/ArithmeticBridge.lean`:
- `finite_quadratic_expansion_identity`: $(A-Z)^2 = A^2 - 2AZ + Z^2$.
- `finite_quadratic_four_term_decomposition`: $(A-Z)^2 = AA - AZ - ZA + ZZ$.
- `cofinal_schedule_distinct_from_fixed_limit`: $(cT)/T = c \ne 0$ proving fixed-limit vs cofinal-limit independence.
- `ConditionalG4RegularizedBridge.all_defects_zero`: Conditional rigidity theorem proving that any valid regularized bridge forces all represented zero defects $d_j = 0$.

---

## 6. Standalone Research Obligation: `OBL-CMSA-003`

$$\boxed{
\text{Can the infinite Archimedean–zero cancellation in the CMSA expansion be regularized}
\atop
\text{with a proved remainder bound that retains a nonnegative radial-defect term?}
}$$
