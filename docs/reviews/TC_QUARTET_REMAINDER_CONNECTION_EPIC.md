# EPIC-TC-041 / TASK-TC-041 & TASK-TC-041R: TC Arithmetic–Spectral Quartet Connection, Certification Repair, and Full Remainder Analysis

- **Epic ID**: `EPIC-TC-041`
- **Task IDs**: `TASK-TC-041` (initial implementation) / `TASK-TC-041R` (certification repair & remainder continuation)
- **Decisive Open Subgate**: `SUBGATE-TC-041B` (`TARGET_QUARTET_REMAINDER_LOWER_BOUND_SUBGATE` — `OPEN`)
- **Starting Repository Snapshot**: `0930f714e66f721c16a048ddaa100bae3180997c`
- **Audited Repair Baseline Commit**: `18e5aa32b137bf8a44077e5dc66ac15f403f66cb`
- **Repair Gate**: `REPAIR_GATE_PASSED_DEFECTS_FIXED_AND_REPRODUCED`
- **Construction Gate**: `CONSTRUCTION_GATE_PASSED_WITH_EXACT_REMAINDER_IDENTITY`
- **Research Gate**: `RESEARCH_GATE_OPEN_REMAINDER_INEQUALITY_UNPROVED`
- **RH Gate**: `RH_GATE_OPEN_PENDING_NONCIRCULAR_REMAINDER_DOMINANCE`
- **Independent Review Status**: `AWAITING_INDEPENDENT_REVIEW`

---

## 1. Executive Summary & Three-Gate Status Separation

This document records the complete mathematical derivation, computational certification, defect reproduction and repair (`TASK-TC-041R`), formal Lean 4 verification, and structural remainder analysis for `EPIC-TC-041`:

1. **Part (A) — Symmetrized Prime-Power Distribution & Exact Rational-Grade Separation (`COMPACT_WINDOW_RATIONAL_SEPARATION_PROVED`)**:
   For $\tau = 2\pi$, $L = \log\tau$, any rational grade difference $d = p/q \in \mathbb{Q}_{>0}$, any compactly supported even nonnegative window $w$ on $[-X_w, X_w]$, and any compactly supported even nonnegative unit-integral bump $\psi$ on $[-1, 1]$, the finite enlarged station set
   $$\mathcal{S}(X_w, d, \varepsilon_0) = \{\xi\log n : \xi \in \{\pm 1\},\; n = p^k \ge 2,\; \log n \le X_w + (1 + d/2)L + \varepsilon_0\}$$
   has a strictly positive minimum shifted separation $\Delta_{\min}(X_w, d, \varepsilon_0) > 0$ by the transcendence of $\tau = 2\pi$ (Lindemann 1882; Baker 1966). Whenever **both** $0 < 2\varepsilon < \Delta_{\min}(X_w, d, \varepsilon_0)$ **and** $0 < \varepsilon \le \varepsilon_0$ hold, opposite prime-power bumps in $Q_h$ ($h \in \{-1, 0, 1\}$) have disjoint supports, giving $Q_1 = Q_0 = Q_{-1} = 0$ and $D(P_\varepsilon, P_\varepsilon) = 0$ identically.
   - **WP1.1 Defect Reproduction & Repair**: In the initial `TASK-TC-041` run, `analyze_remainder_components_and_mechanisms` evaluated $\delta = 0.12, \gamma = 14.134725141734693, d = 1/20, x_0 = 0.25$ ($X_w \approx 0.41669546$) at $\varepsilon = 0.08$. However, on that window $\Delta_{\min} \approx 0.02588918233591618$ (attained between $-\log 9$ and $-\log 8$), so $\varepsilon_{\max} = \Delta_{\min}/2 \approx 0.01294459116795809$. At $\varepsilon = 0.08 > \varepsilon_{\max}$, the supports overlap and direct spatial quadrature on the constructed window gives $Q_{-1} \approx 1.10007473$, $Q_0 = 0.0$, $Q_1 \approx 1.10007473$, and $D(P_\varepsilon, P_\varepsilon) \approx 2.20014946 \ne 0$. `TASK-TC-041R` reproduces this exact violation, enforces both $2\varepsilon < \Delta_{\min}$ and $\varepsilon \le \varepsilon_0$ in `flint.arb` interval arithmetic, certifies boundary station inclusion via `flint.arb` upper/lower bounds, and evaluates the benchmark at admissible $\varepsilon = 0.01 < \varepsilon_{\max}$ where $Q_{-1} = Q_0 = Q_1 = D(P_\varepsilon, P_\varepsilon) = 0$ identically.

2. **Part (B) — Complete Smoothed Explicit-Formula Decomposition & Unconditional RvM Spectral Tail Bound (`SMOOTHED_EXPLICIT_FORMULA_SIGN_AND_SUBTRACTION_VERIFIED`)**:
   Retaining all pole, origin-constant ($\log(2\tau) = \log(4\pi)$), subtracted archimedean integral (with removable singularity $\frac{1}{2}\psi_\varepsilon(x)$ at $u = 0$), and reflected prime-power terms gives $P_\varepsilon(x) = A_\varepsilon(x) - S_\varepsilon(x)$.
   - **WP1.2 Counterexample Reproduction & Proved Tail Bound Repair**: The initial implementation used $|c_\varepsilon(i\gamma)| \le 36\pi^6 / (\varepsilon\gamma)^7$ for `cosine_power_6` and integrated against a heuristic $\frac{\log t}{2\pi}\,dt$ density. Because $c_\varepsilon(i\gamma) = \frac{36\pi^6\sin u}{u(\pi^2-u^2)(4\pi^2-u^2)(9\pi^2-u^2)}$ ($u = \varepsilon\gamma$), at $u = 39\pi/2 = 19.5\pi$, $|c_\varepsilon(i\gamma)|$ exceeds $36\pi^6/u^7$ by the exact factor
     $$\bigl[(1 - 1/19.5^2)(1 - 4/19.5^2)(1 - 9/19.5^2)\bigr]^{-1} \approx 1.0378607972028278 > 1.$$
     `TASK-TC-041R` reproduces this counterexample in `flint.arb`, replaces the naive asymptotic coefficient with the proved profile-specific upper envelope
     $$M_6(u_0, r) = \frac{36\pi^6}{\prod_{k=1}^3 \bigl(1 - \frac{k^2\pi^2 + r^2}{u_0^2}\bigr)} \qquad (u \ge u_0 > \sqrt{9\pi^2 + r^2},\; r = \varepsilon|\delta|),$$
     implements the general integration-by-parts bound
     $$|c_\varepsilon(\delta + i\gamma)| \le \frac{e^{\varepsilon|\delta|}\|\psi^{(N)}\|_1}{\varepsilon^N |\delta + i\gamma|^N}$$
     with $\varepsilon^N$ in the **denominator** (correcting the narrative typo $(\varepsilon/|z|)^N\|\psi^{(N)}\|_1$), and integrates against the unconditional Riemann–von Mangoldt theorem $N(t) = \frac{t}{2\pi}\log\frac{t}{2\pi e} + \frac{7}{8} + R(t)$ with explicit remainder $|R(t)| \le 0.112\log t + 0.278\log\log t + 2.510$ (Trudgian 2014) via Riemann–Stieltjes integration by parts, accounting for both ordinate signs $\pm\gamma_\rho$, zero multiplicities $m_\rho$, and shifted spatial growth $e^{|\delta_{\max}| X_{\mathrm{shift}}}$.

3. **Parts (C), (D) & (E) — Admissible 6-Translate Isolating Window & Certified 16-Pair Target Quartet Positivity (`SIXTEEN_PAIR_QUARTET_POSITIVITY_PROVED_UNDER_H`)**:
   For $a = \tau/(8\gamma)$, $b = \tau/(4\gamma)$, $\kappa = \cosh(2\delta b)$, the 6-point convolution window $w = w_0 * \mu_a * \nu_b$ is even, nonnegative, compactly supported on $[-X_w, X_w]$ ($X_w = X_0 + a + b$), and satisfies $W(\pm 2i\gamma) = 0$ and $W(\pm 2\delta \pm 2i\gamma) = 0$ while $W(2\delta) > 0$. Across all 16 ordered pairs of the target quartet $\{\frac{1}{2} \pm \delta \pm i\gamma\}$, the 4 opposite pairs vanish via $T(0) = 0$, the 4 self pairs vanish via $W(\pm 2\delta \pm 2i\gamma) = 0$, and the 4 vertical pairs vanish via $W(\pm 2i\gamma) = 0$, leaving the 4 horizontal conjugate pairs:
   $$C_\varepsilon = D(S_0, S_0) = 4 m^2 |c_\varepsilon(\delta + i\gamma)|^2 W(2\delta)\cos(d\gamma L)\bigl(\tau^\delta - \tau^{-\delta}\bigr)^2 > 0$$
   for rational $0 < d < \tau/(4\gamma L)$ and $0 < \varepsilon < \log(2)/|\delta + i\gamma|$.
   - **WP1.3 Genuine Interval Arithmetic & Symbolic Zero Proof Repair**: `TASK-TC-041R` replaces the `arb(str(abs(c_z1)**2))` and `arb(str(w_2delta))` conversions from `mpmath` with `evaluate_bump_laplace_transform_acb` and `evaluate_window_laplace_transform_acb` in pure `flint.acb`/`flint.arb` ball arithmetic from enclosed inputs, and proves $T(0) = 0$, $W(\pm 2i\gamma) = 0$, and $W(\pm 2\delta \pm 2i\gamma) = 0$ symbolically using `sympy`.

4. **WP2 & WP4 — Separation of Real-Zeta Checks from Synthetic Perturbed Controls & Remainder Analysis (`SUBGATE-TC-041B`)**:
   - **Category A (Actual Zeta Consistency Check)**: Using all 200 certified critical-line zeros ($T = 396.381854$) with NO synthetic zero replacement on a simultaneously separated and tail-convergent window ($d = 1/24, \gamma_{\mathrm{win}} = 35.0, x_0 = 0.04, X_w \approx 0.107320, \Delta_{\min} \approx 0.0765782, \varepsilon_{\max} \approx 0.0382891, \varepsilon = 0.036 < \varepsilon_{\max}, u_0 = \varepsilon T \approx 14.2697 > 3\pi$), arithmetic separation is certified ($D(P_\varepsilon, P_\varepsilon) = 0.0$), while the actual zeta right-hand side gives $D(A_\varepsilon, A_\varepsilon) \approx 87.201788$, $-2D(A_\varepsilon, S_T) \approx -160.364287$, $D(S_T, S_T) \approx 73.269450$, and total $D(A_\varepsilon - S_T, A_\varepsilon - S_T) \approx +0.106952$, cancelling to $99.9\%$ toward $0$ within the proved quadratic truncation error bound $4\|w\|_1(2(M_A + M)\eta + \eta^2) \approx 112.672$ ($\eta \approx 0.070025$).
   - **Category C (Synthetic Perturbed-Spectrum Control)**: When $\pm i\gamma_1$ is replaced by a synthetic 4-zero off-line quartet $S_0$ while holding $A_\varepsilon$, $S_{\mathrm{rest}}$, and $P_\varepsilon$ from actual $\zeta(s)$, the explicit formula is broken by the perturbation defect $\Delta P_{\mathrm{synth}}(x) = S_{\gamma_1,\mathrm{crit}}(x) - S_0(x) \ne 0$, which explains why $C_\varepsilon + R_\varepsilon^{\mathrm{perturbed}} \ne 0$ in synthetic replacement experiments.
   - **WP4 Regrouping & Multi-Ordinate Filter Obstruction (`SUBGATE_TC_041B_FINITE_FILTER_OBSTRUCTION_PROVED_WITHIN_SCOPE`)**: Under the regrouped identity $R_\varepsilon = D(A_\varepsilon - S_{\mathrm{rest}}, A_\varepsilon - S_{\mathrm{rest}}) - 2D(A_\varepsilon - S_{\mathrm{rest}}, S_0)$, substituting $A_\varepsilon - S_{\mathrm{rest}} = P_\varepsilon + S_0$ causes the linear cross term $2D(P_\varepsilon, S_0)$ to cancel identically between the two pieces, yielding $R_\varepsilon = D(P_\varepsilon, P_\varepsilon) - C_\varepsilon = -C_\varepsilon$. Furthermore, extending the window to annihilate $J$ background ordinates via $w_J = w_0 * \mu_a * \nu_b * \prod_{j=1}^J \mu_{a_j}$ ($a_j = \tau/(8\gamma_j)$) expands spatial support additively by $\sum_{j=1}^J \frac{\tau}{8\gamma_j}$, shrinking $\Delta_{\min}(X_w(J), d)$ and $\varepsilon_{\max}(J) = \Delta_{\min}/2$ while expanding the spectral passband $1/\varepsilon_{\max}(J)$. Consequently, `SUBGATE-TC-041B` remains genuinely `OPEN`.

---

## 2. WP1–WP2 Numerical Tables (Certified Artifact `data/tc_quartet_remainder_connection.json`)

### 2.1 WP1.1 Separation Violation Reproduction vs. Repaired Admissible Benchmark ($\delta = 0.12, \gamma = \gamma_1, d = 1/20, x_0 = 0.25$)

| Regime | $\varepsilon$ | $2\varepsilon$ | Certified $\Delta_{\min}$ | $\varepsilon_{\max} = \Delta_{\min}/2$ | $Q_{-1}$ | $Q_0$ | $Q_1$ | $D(P_\varepsilon, P_\varepsilon)$ | Certified Vanishing |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Legacy Invalid Benchmark | `0.08` | `0.16` | `0.02588918` | `0.01294459` | `1.10007473` | `0.0` | `1.10007473` | `2.20014946` | `False` (`OVERLAP_OR_COLLISION_DETECTED`) |
| Repaired Admissible Benchmark | `0.01` | `0.02` | `0.02588918` | `0.01294459` | `0.0` | `0.0` | `0.0` | `0.0` | `True` (`COMPACT_WINDOW_RATIONAL_SEPARATION_PROVED`) |

### 2.2 WP2 Category A (Actual Zeta Consistency) vs. Category C (Synthetic Perturbed Control)

| Category | Configuration | $\varepsilon$ | $D(P_\varepsilon, P_\varepsilon)$ | $D(A_\varepsilon, A_\varepsilon)$ | $-2D(A_\varepsilon, S_{\mathrm{crit/rest}})$ | $D(S_{\mathrm{crit/rest}}, S_{\mathrm{crit/rest}})$ | Total / Assembled | Interpretation |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Cat. A: Actual Zeta (Simultaneous Separated + Tail Regime)** | $d=1/24, x_0=0.04, N=200$ ($u_0 \approx 14.27 > 3\pi$) | `0.036` | `0.0` | `+87.201788` | `-160.364287` | `+73.269450` | `+0.106952` | Actual $\zeta(s)$ terms cancel to $99.9\%$ toward $D(P_\varepsilon,P_\varepsilon)=0$ within certified tail budget ($\eta \approx 0.0700$). |
| **Cat. C: Synthetic Perturbed Spectrum** | $d=1/20, x_0=0.25, N=25$ ($\pm i\gamma_1 \mapsto S_0$) | `0.01` | `0.0` | `+330.016258` | $+493.537562$ ($R_{AS_0}=+79.474781$) | $-123.619637$ ($R_{0,\mathrm{rest}}=+2.799334$) | $R_\varepsilon \approx +782.2083$ ($C_\varepsilon \approx +0.212254$) | Nonzero sum reflects synthetic explicit-formula defect $\Delta P_{\mathrm{synth}} = S_{\gamma_1,\mathrm{crit}} - S_0 \ne 0$ and passband truncation at $1/\varepsilon = 100$. |

### 2.3 WP4 Multi-Ordinate Filter Extension Sweep ($w_J = w_0 * \mu_a * \nu_b * \prod_{j=1}^J \mu_{a_j}$, $d = 1/24, x_0 = 0.04$)

| Filtered Background Ordinates $J$ | Window Half-Width $X_w(J)$ | Enlarged Cutoff $X_{\mathrm{shift}}(J)$ | Enlarged Stations $M(J)$ | Certified $\Delta_{\min}(J)$ | Max Admissible $\varepsilon_{\max}(J)$ | Passband $1/\varepsilon_{\max}(J)$ | Approx. Unfiltered Zeros in Passband | Max Residual $\max_{j \le J}|W_J(2i\gamma_j)|$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `0` | `0.206695` | `2.082862` | `12` | `0.05695318` | `0.02847659` | `35.12` | `4.03` | `0.0` |
| `1` | `0.244056` | `2.120222` | `12` | `0.05695318` | `0.02847659` | `35.12` | `4.03` | `2.75e-37` |
| `2` | `0.275458` | `2.151625` | `12` | `0.05695318` | `0.02847659` | `35.12` | `4.03` | `2.75e-37` |
| `4` | `0.325120` | `2.201286` | `14` | `0.04120482` | `0.02060241` | `48.54` | `8.07` | `2.75e-37` |
| `8` | `0.399698` | `2.275864` | `14` | `0.04120482` | `0.02060241` | `48.54` | `8.07` | `1.78e-36` |

---

## 3. WP3 Coordinate Bridge & Synchronized 5-Column Lean 4 Formalization Scope Table

### 3.1 Physical-to-Logarithmic Coordinate Bridge Repair (Contract Item 7 & WP3.1)

Under $y = e^x$ ($x = \log y$, $dy = e^x\,dx$, $dy/y = dx$):
1. **One-Variable Substitution**: For $y = e^x$ and $y' = \tau^{-d}y = e^{x - dL} = e^{x'}$, substituting $dy = e^x\,dx$ yields
   $$\frac{dy}{y^{1/2}(y')^{1/2}} = \frac{e^x\,dx}{e^{x/2}e^{x'/2}} = e^{(x - x')/2}\,dx = e^{dL/2}\,dx = \tau^{d/2}\,dx.$$
   (The earlier narrative expression $\frac{dy}{y^{1/2}(y')^{1/2}} = e^{-(x+x')/2}\,dx$ omitted the $dy = e^x\,dx$ Jacobian factor and has been corrected across all canonical documents.)
2. **Paired-Grade Half-Density Pullback**: For $\Phi(y) = y^{-1/2}F(\log y)$ and $\Psi(y) = y^{-1/2}G(\log y)$ evaluated at $y_+ = \tau^{-K_+}y = e^{x - K_+ L}$ and $y_- = \tau^{-K_-}y = e^{x - K_- L}$ with $K_\pm = h \pm d/2$ ($K_+ + K_- = 2h$),
   $$\Phi(y_+)\Psi(y_-)\,dy = e^{-(x-K_+ L)/2}e^{-(x-K_- L)/2}F(x-K_+ L)G(x-K_- L)e^x\,dx = \tau^h F\bigl(x-(h+d/2)L\bigr)G\bigl(x-(h-d/2)L\bigr)\,dx.$$
3. **Smoothing Family Distinction**: Additive logarithmic smoothing $\psi_\varepsilon(x \mp \log n)$ has constant width $\varepsilon$ in $x = \log y$ (corresponding to multiplicative width $[n e^{-\varepsilon}, n e^\varepsilon]$ in $y$), making it an auxiliary logarithmic explicit-formula family distinct from constant-width physical-coordinate smoothing on $[8, 20]$.

### 3.2 Synchronized 5-Column Lean 4 Coverage Table (`formal/RiemannScope/QuartetRemainderConnection.lean`, 0 `sorry`)

| Mathematical Claim | Exact Lean Declaration | Proved Hypotheses in Lean | External / Unproved Premises | Evidence Scope |
| :--- | :--- | :--- | :--- | :--- |
| Radial factor square identity $\tau^{2\delta} + \tau^{-2\delta} - 2 = (\tau^\delta - \tau^{-\delta})^2$ | `quartet_radial_factor_eq_sq` | `tau_delta * tau_delta_inv = 1` over $\mathbb{R}$ | Identification $\text{tau\_delta} = \tau^\delta$ | Exact real algebra (`PROVED_IN_LEAN`) |
| Strict positivity of off-critical radial factor $(\tau^\delta - \tau^{-\delta})^2 > 0$ | `quartet_radial_sq_pos`, `quartet_radial_factor_pos` | `tau_delta ≠ tau_delta_inv` (and `tau_delta * tau_delta_inv = 1`) | Monotonicity $\delta > 0 \implies \tau^\delta \ne \tau^{-\delta}$ | Exact real algebra (`PROVED_IN_LEAN`) |
| Equivalence of ordered-pair exponential sum and symmetrized $\cosh$ sum | `ordered_pair_symmetrized_cosh_equivalence` | `P_rs = P_sr` and `E_plus + E_minus = 2 * C_cosh` | Complex-conjugate symmetry of quartet summands | Exact finite algebra (`PROVED_IN_LEAN`) |
| Complete 16-pair quartet reduction to $4 c_{\mathrm{conj}}$ | `sixteen_pair_quartet_block_reduction`, `quartet_opposite_pair_sum_zero`, `quartet_vertical_pair_sum`, `quartet_horizontal_pair_sum_pos` | $O_i = 0$, $S_i = 0$, $V_i = 0$, $C_i = c_{\mathrm{conj}}$ | Analytic transform evaluations of $W(z)$ and $T(z)$ | Exact finite algebra (`PROVED_IN_LEAN`) |
| Quarter-period and half-period window transform zeros $W(\pm 2i\gamma)=0$, $W(\pm 2\delta \pm 2i\gamma)=0$ | `window_transform_vertical_zero`, `window_transform_self_zero`, `cosh_filter_factor_pos`, `nu_b_kappa_pos`, `prob_conv_nonneg`, `prob_conv_normalization` | `cosh_a_factor = 0` and `cosh_b_val = -kappa` | Trigonometric evaluations $\cos(\pi/2)=0$, $\cosh(x \pm i\pi) = -\cosh(x)$ (proved symbolically in SymPy & certified in Arb) | Real algebraic factorization (`PROVED_IN_LEAN` + SymPy/Arb) |
| Strict positivity $C_\varepsilon > 0$ under $H$, $m^2$ scaling, and $\delta=0$ vanishing | `sixteen_pair_target_quartet_pos`, `quartet_target_coeff_pos`, `quartet_block_pos_under_H`, `sixteen_pair_multiplicity_scaling`, `sixteen_pair_critical_line_vanishing`, `quartet_second_diff_pos` | $m > 0$, $c_{\mathrm{abs}} \ne 0$, $W(2\delta) > 0$, $\cos(d\gamma L) > 0$, $\tau^\delta \ne \tau^{-\delta}$ | Existence of off-line zero $H$ | Conditional finite algebra (`PROVED_CONDITIONAL`) |
| Elementary bump nonvanishing & IBP error bound nonnegativity | `elementary_bump_nonvanishing_from_bound`, `ibp_laplace_error_bound_nonneg`, `bump_laplace_error_bound_nonneg` | $1 - c_{\mathrm{abs}} \le B_{\mathrm{dev}} < 1$; positive factors | Integral inequality $|c_\varepsilon(z)-1| \le e^{\varepsilon|z|}-1$ | Real linear/positivity algebra (`PROVED_IN_LEAN`) |
| Imaginary-axis multiplier sign inversion $2\cos x - 2 = -4\sin^2(x/2) \le 0$ | `second_diff_multiplier_imag_eq`, `critical_line_multiplier_nonpos` | `cos_x = 1 - 2 * sin_half ^ 2` | Double-angle identity for $\cos$ | Exact real algebra (`PROVED_IN_LEAN`) |
| Quadratic truncation error propagation $4\|w\|_1(2M\eta + \eta^2)$ | `quadratic_truncation_error_bound` | Componentwise bounds `err_Bh <= w_l1 * (2*M*eta + eta^2)` | Pointwise tail bound $\|E\|_\infty \le \eta$ from RvM Stieltjes theorem | Real linear inequality (`PROVED_IN_LEAN`) |
| Bilinear expansion, regrouped identity $R_\varepsilon = D(A-S_{\mathrm{rest}},A-S_{\mathrm{rest}}) - 2D(A-S_{\mathrm{rest}},S_0)$, and consistency $C_\varepsilon + R_\varepsilon = 0$ | `arithmetic_spectral_second_diff_expansion`, `quartet_remainder_decomposition_identity`, `regrouped_remainder_algebraic_identity`, `arithmetic_second_diff_vanishes`, `exact_remainder_consistency_identity`, `quartet_remainder_identity_from_vanishing` | Bilinear expansion and $Q_\varepsilon = 0$, $Q_\varepsilon = C_\varepsilon + R_\varepsilon$ | Smoothed Weil explicit formula $P_\varepsilon = A_\varepsilon - S_\varepsilon$ and Lindemann transcendence of $\tau = 2\pi$ | Exact algebraic identity (`PROVED_IN_LEAN`) |
| Conditional remainder dominance contradiction & reductio schema $H \implies \bot \implies \neg H$ | `conditional_remainder_dominance_contradiction`, `quartet_subordination_contradiction`, `reductio_from_quartet_and_remainder_lower_bound`, `conditional_reductio_negates_offcritical_hypothesis`, `unconditional_subordination_contradiction`, `unconditional_subordination_contradiction_repaired` | $Q_\varepsilon = 0$, $Q_\varepsilon = C_\varepsilon + R_\varepsilon$, $C_\varepsilon > 0$, and **unproved hypothesis** $R_\varepsilon > -C_\varepsilon$ | **Open Subgate `SUBGATE-TC-041B`**: proving $R_\varepsilon > -C_\varepsilon$ for the complete zeta spectrum | Conditional deduction (`PROVED_CONDITIONAL` on `SUBGATE-TC-041B`) |

---

## 4. WP5 Literature Provenance & Novelty Calibration

### 4.1 Verified Literature References

- **Lindemann (1882)**: F. Lindemann, *Über die Zahl $\pi$*, Mathematische Annalen **20** (1882), 213–225. (Establishes transcendence of $\pi$ and $\tau = 2\pi$, guaranteeing $\Delta_{\min}(X_w, d, \varepsilon_0) > 0$ on every finite station set for $d \in \mathbb{Q}_{>0}$.)
- **Weil (1952)**: A. Weil, *Sur les "formules explicites" de la théorie des nombres premiers*, Comm. Sém. Math. Univ. Lund (1952), 252–265. (Establishes the distributional explicit formula in logarithmic coordinates.)
- **Baker (1966)**: A. Baker, *Linear forms in the logarithms of algebraic numbers*, Mathematika **13** (1966), 204–216.
- **Trudgian (2014)**: T. S. Trudgian, *An improved upper bound for the argument of the Riemann zeta-function on the critical line II*, J. Number Theory **134** (2014), 280–292. (Provides the unconditional explicit Riemann–von Mangoldt remainder bound $|R(T)| \le 0.112\log T + 0.278\log\log T + 2.510$ used in `compute_unconditional_rvm_spectral_tail_bound`.)
- **`arXiv:math/0101068` (Burnol 2001)**: J.-F. Burnol, *Sur les "formules explicites" I: analyse invariante* (2001). (Logarithmic-coordinate explicit-formula distributions and dilation-invariant pairings.)
- **`arXiv:2511.22755` (Connes, Consani, Moscovici 2025)**: A. Connes, C. Consani, H. Moscovici, *Zeta Spectral Triples* (2025). (Truncated Euler products, Weil explicit-formula quadratic forms, and spectral realizations.)
- **`arXiv:2609.04908` (Shi 2026)**: Yaoming Shi, *Construction of Finite Hilbert–Pólya Matrices from Weil's Explicit Formula* (2026). (Finite matrix truncations of explicit-formula kernels in logarithmic coordinates.)
- **`arXiv:2606.09096` (Suzuki 2026)**: M. Suzuki, *Weil's quadratic form via the screw function* (2026). (Representation of Weil's explicit-formula quadratic functional via translation differences.)

### 4.2 Structured Novelty Separation

- **Known Standard Ingredients**:
  1. Riemann–Weil explicit formula in logarithmic coordinates $x = \log y$ (Weil 1952; Burnol 2001).
  2. Transcendence of $\tau = 2\pi$ (Lindemann 1882) and linear forms in logarithms (Baker 1966).
  3. Trigonometric quarter-period and half-period convolution annihilators for finite exponential sums.
  4. Unconditional Riemann–von Mangoldt zero-counting remainder bounds (Trudgian 2014).
- **Project-Specific Combinations Established & Verified Here**:
  1. Pairing rational grade differences $d \in \mathbb{Q}_{>0}$ of $L = \log\tau$ with compactly supported prime-power bumps $\psi_\varepsilon$ to achieve certified support disjointness $Q_1 = Q_0 = Q_{-1} = D(P_\varepsilon, P_\varepsilon) = 0$ on finite enlarged windows (`COMPACT_WINDOW_RATIONAL_SEPARATION_PROVED`).
  2. Constructing the 6-translate nonnegative convolution window $w = w_0 * \mu_a * \nu_b$ that simultaneously annihilates opposite ($T(0)=0$), vertical ($W(\pm 2i\gamma)=0$), and self ($W(\pm 2\delta \pm 2i\gamma)=0$) pairs of a 4-zero off-line quartet while preserving $C_\varepsilon = D(S_0, S_0) > 0$ (`SIXTEEN_PAIR_QUARTET_POSITIVITY_PROVED_UNDER_H`).
  3. Quantifying the 4 structural remainder mechanisms and proving the scoped finite-filter support–separation–bandwidth trade-off on `SUBGATE-TC-041B` (`SUBGATE_TC_041B_FINITE_FILTER_OBSTRUCTION_PROVED_WITHIN_SCOPE`).
- **Open Unsolved Problem**:
  - Establishing an unconditional, non-circular lower bound $R_\varepsilon > -C_\varepsilon$ for the complete Riemann zeta spectrum (`SUBGATE-TC-041B`, status `OPEN`).

---

## 5. Reproducible Verification Commands

```powershell
python -m tc.quartet_remainder_connection
python -m pytest tests/test_tc_quartet_remainder_connection.py
python scripts/build_formal.py --allow-dirty
python scripts/workflow.py check-fast
python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --cross-check-register --repo-root .
```
