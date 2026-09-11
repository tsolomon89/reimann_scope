# TC Corrective Epic: Evidence Completion, Constant Certification, and Arithmetic Compatibility Investigation

**Epic**: TC Corrective Epic  
**Harness**: `tsolomon89/reimann_scope`  
**Date**: 2026-09-11  
**Baseline Git Anchor**: `82643cafd605492233c6c1e992b78c2c30d45f13` (immutable, preserved)  
**Lean 4 Toolchain**: Lean 4.8.0 / Lake 5.0.0 (213 compiled project theorems, 0 sorry, 0 admit, 0 warnings)  
**Epistemic Classification**: EVIDENCE COMPLETED; EVALUATOR REPAIRED; FORMAL LIMITS PROVED; CONSTANTS CERTIFIED; ARBITRARY COMPENSATION REFUTED; TRANSCENDENTAL CONTINUATION BRIDGE STRICTLY OPEN.

---

## 1. Executive Summary and Epistemic Verdict

The TC Corrective Epic resolves the core deliverables and repairs identified following the review of the previous TC Arithmetic Bridge Epic. Specifically:

1. **Finite-Decomposition Recomputation**: The finite decomposition evaluator `evaluate_two_variable_finite_decomposition` genuinely recomputes all four tensor blocks ($Q_{BB}, Q_{BZ}, Q_{ZB}, Q_{ZZ}$) via 2D numerical quadrature across arbitrary cutoffs $T$ and epsilons $\varepsilon$. Dynamic zero filtering correctly handles cutoffs below the first zero ($T=10 < \gamma_1 \approx 14.13$, where $Q_{BZ}=Q_{ZB}=Q_{ZZ}=0$ and $Q_{\rm ret} = Q_{BB} \approx 0.168957$) through cutoffs including 1, 2, and 3 reference zeros ($T=18 \implies Q_{\rm ret} \approx 0.232622$, $T=23 \implies Q_{\rm ret} \approx 0.297505$, $T=30 \implies Q_{\rm ret} \approx 0.269459$). The retained remainder $R_{\varepsilon, T, \rm independent}$ is computed independently from its complementary terms and verified to agree with $Q_{\rm ret} - A_\varepsilon$ to $< 10^{-12}$.
2. **Constant Certification Semantics**: `audit_two_variable_truncation_bound` strictly validates $C_p > 0$ finite, integer order $p > 2$, and cutoff scaling $\alpha > p/(p-2)$. It enforces distinct epistemic tiers:
   - `BOUND_SHAPE_ILLUSTRATIVE`: Proves shape convergence without claiming constant certification;
   - `CALLER_UNVERIFIED_CONSTANT`: Correctly flags caller-supplied unverified constants (e.g. $C_p = 10^{-100}$) and refuses to mark them certified;
   - `ANALYTICALLY_DERIVED_CONSTANT`: Marks constants derived via verified analytic bounds;
   - `MACHINE_CHECKED_ENCLOSURE`: Validates machine-checked enclosures.
3. **Certified Arb Enclosure of $A_0$**: Using FLINT `acb.zeta_zero(1).imag` certified zero ordinate and outward interval rounding, $A_{0, \Gamma}(\rho_1) \in [0.543269, 0.545611] > 0.54 > 0$ is rigorously certified away from zero, definitively falsifying the conjectured identity $A_{0, \Gamma} = c D_M(\rho_0)$ on the critical line.
4. **Lean 4 Topological Limits**: Three new theorems were formalized in `formal/RiemannScope/Grade.lean` (bringing total compiled project theorems to 213 with 0 sorry/admit):
   - `explicit_formula_remainder_cancellation_tendsto`: Formalizes the topological limit $\lim \bar R_\varepsilon = -A_0$ via Mathlib `Filter.Tendsto.sub`.
   - `explicit_formula_remainder_cancellation_quantified`: Formalizes quantified $\varepsilon$-$\delta$ remainder cancellation.
   - `finite_spectral_perturbation_rigidity_2point`: Formalizes 2-point non-singular linear independence of distinct complex exponentials.
5. **Scoped Mode Extraction Obstruction**: With the smooth mollifier correctly normalized to $\int j = 1$, the finite-epsilon convolution norm $N_\varepsilon(f) = \sqrt{\varepsilon}\|j_\varepsilon * f\|_2$ is proved to scale as $O(\sqrt{\varepsilon}) \to 0$ (matching the asymptotic leading term within $0.11\%$ at $\varepsilon=0.2$ and $0.0003\%$ at $\varepsilon=0.01$). Any linear functional family satisfying $|P_\varepsilon(g)| \le C N_\varepsilon(g)$ with uniform $C$ forces $P_\varepsilon(f) \to 0$ on fixed modes, requiring divergent $C_\varepsilon = \Omega(\varepsilon^{-1/2}) \to \infty$ to isolate a fixed mode.
6. **Refutation of Arbitrary Compensation via Finite Spectral Perturbation Rigidity**: The previous report's unsupported claim that arbitrary perturbations of a zero can be absorbed by the remaining spectrum and background was refuted. By the **Finite Spectral Perturbation Rigidity Theorem**, the family $\{x^{\rho-1} : \rho \in S\}$ for distinct exponents $S$ is linearly independent on any open interval $I \subset (a_K, \infty)$. With the arithmetic measure and background fixed, a non-trivial finite spectral perturbation cannot vanish identically or be absorbed.
7. **Arithmetic Compatibility Investigation**: Four candidate arithmetic-compatibility relations were audited:
   - Weil positivity;
   - TC radial defect;
   - Theta modular inversion;
   - Vinogradov-Korobov zero-free density.
   The earliest unproved inference in every chain is the **spectral transfer step**: transferring individual radial defect $D_M(\rho_0) > 0$ to the collective cross-grade observable $\bar Q_\varepsilon$. On fixed compact windows, the explicit formula identity forces exact collective cancellation $\bar R_{\varepsilon, T} \to -A_0$, so the Transcendental Continuation bridge remains **strictly open**.

---

## 2. Answers to the 8 Core Questions

### Question 1: Which previously overstated claims were corrected?
1. **Arbitrary Spectral Compensation**: Corrected the assertion that arbitrary zero perturbations can be freely absorbed by the remaining spectrum and background. Proved the Finite Spectral Perturbation Rigidity Theorem establishing linear independence of distinct complex powers $\{x^{\rho-1}\}$ on any open interval.
2. **Lean Tail Bound Scope**: Corrected the description of `normalized_tail_subordination_bound` from a claimed "power/log asymptotic bound" to its actual content: an elementary transitivity inequality ($|E| \le B \wedge B < \delta \implies |E| < \delta$). Proved the actual topological convergence $\bar R_\varepsilon \to -A_0$ in Lean 4 via `Filter.Tendsto.sub`.
3. **Lean Contradiction Endpoint**: Corrected the description of `candidate_bridge_unproved_lower_bound_gap` from establishing off-line zero consistency to its actual content: an elementary algebraic identity ($Q = A + R \wedge R = -A \implies Q = 0$).
4. **Constant Certification**: Corrected the behavior where any numeric $C_p$ (such as $10^{-100}$) was classified as `PROVED_AND_VERIFIED`. Implemented strict separation of illustrative bound shapes from unverified and derived constants.
5. **Mollifier Normalization and Convolution**: Corrected the insertion of asymptotic leading terms as exact convolution values; normalized $\int j = 1$ and computed the exact finite convolution norm $N_\varepsilon(f) = \sqrt{\varepsilon}\|j_\varepsilon * f\|_2$.
6. **Finite Evaluator Recomputation**: Removed benchmark substitution from `evaluate_two_variable_finite_decomposition`, making all tensor blocks dynamically recompute from inputs.

### Question 2: Which calculations now genuinely recompute?
* `evaluate_two_variable_finite_decomposition` recomputes all four tensor blocks ($Q_{BB}, Q_{BZ}, Q_{ZB}, Q_{ZZ}$) via 2D numerical quadrature for arbitrary $T$, $\varepsilon$, and window:
  - $T=10.0 < 14.13$: Retained zeros $= \emptyset$, $Q_{BZ}=Q_{ZB}=Q_{ZZ}=0$, $Q_{\rm ret} = Q_{BB} \approx 0.168957$, $A_\varepsilon = 0$, $R_{\varepsilon, T} = Q_{BB}$.
  - $T=18.0$: 1 zero retained ($\gamma_1 \approx 14.1347$), $Q_{\rm ret} \approx 0.232622$.
  - $T=23.0$: 2 zeros retained ($\gamma_1, \gamma_2 \approx 21.0220$), $Q_{\rm ret} \approx 0.297505$.
  - $T=30.0$: 3 zeros retained ($\gamma_1, \gamma_2, \gamma_3 \approx 25.0109$), $Q_{\rm ret} \approx 0.269459$.
* Independent remainder calculation:
  $$R_{\varepsilon, T, \rm independent} = Q_{BB} - Q_{BZ} - Q_{ZB} + Q_{ZZ, \rm complement}$$
  agrees with $Q_{\rm ret} - A_\varepsilon$ to $< 10^{-12}$.
* Cache bypass on `recompute=True` is verified; regression benchmarks are strictly isolated in `BENCHMARK_K0_J1_EPS0p1_T30_REGRESSION_FIXTURE`.

### Question 3: Which quantities have rigorous certificates, and which do not?
* **Rigorously Certified**:
  - Selected contribution limit: FLINT Arb ball enclosure using `acb.zeta_zero(1).imag` with outward rounding proves $A_{0, \Gamma}(\rho_1) \in [0.543269, 0.545611] > 0.54 > 0$.
  - Arithmetic vanishing: $Q_\varepsilon^{0, 1} \equiv 0$ for all $\varepsilon < 0.150444$ on $[8, 20]$ via Lindemann transcendence ($2\pi$ transcendental).
  - 1-variable trivial zero background sum: agrees with $\frac{a_K^2}{x(x^2 - a_K^2)}$ to $< 10^{-15}$.
  - 2D tensor algebraic identity: verified to machine precision across all configurations.
* **Not Certified (Explicitly Identified)**:
  - Infinite spectral tail bound constant $C_p$: Unverified caller constants (e.g. $C_p = 10^{-100}$) are classified as `CALLER_UNVERIFIED_CONSTANT`; machine-checked enclosures of $C_p$ remain open for large $T$.
  - Complete zero enumeration at arbitrary heights: certified reference zeros are labeled as truncations unless complete enumeration is certified.

### Question 4: What did Lean actually prove?
Fourteen theorems in `formal/RiemannScope/Grade.lean` (213 total compiled project theorems, 0 sorry, 0 admit, 0 warnings):
1. `two_variable_tensor_decomposition_algebra`: Bilinear tensor expansion $(B_K - Z_K)(B_J - Z_J) = B_K B_J - B_K Z_J - Z_K B_J + Z_K Z_J$.
2. `two_variable_nine_term_expansion_algebra`: Exact signs for 9-term bilinear expansion.
3. `normalized_truncation_error_scaling`: $|E| \le B \implies |E|/\varepsilon \le B/\varepsilon$.
4. `power_cutoff_exponent_positivity`: $\alpha(p-2) - p > 0$ for $p > 2, \alpha > p/(p-2)$.
5. `candidate_bridge_with_remainder_contradiction`: $Q = A + R, Q \le 0, A \ge c D > 0, |R| < c D \implies \text{False}$.
6. `explicit_formula_remainder_cancellation_identity`: $Q = A + R + E \implies R - (-A_0) = Q - (A - A_0) - E$.
7. `explicit_formula_remainder_triangle_bound`: $|R - (-A_0)| \le |Q| + |A - A_0| + |E|$.
8. `explicit_formula_remainder_cancellation_eps`: Quantitative $\varepsilon$-$\delta$ convergence.
9. `normalized_tail_subordination_bound`: Elementary subordination $|E| \le B \wedge B < \delta \implies |E| < \delta$.
10. `candidate_bridge_gap_exact_cancellation`: $A_0 = c D \implies \neg(|-A_0| < c D)$.
11. `candidate_bridge_unproved_lower_bound_gap`: Algebraic identity $Q = A + R \wedge R = -A \implies Q = 0$.
12. `explicit_formula_remainder_cancellation_tendsto`: Topological filter convergence $\lim R = -A_0$ using Mathlib `Filter.Tendsto.sub`.
13. `explicit_formula_remainder_cancellation_quantified`: Quantified $\varepsilon$-$\delta$ limit for remainder convergence.
14. `finite_spectral_perturbation_rigidity_2point`: Non-singular 2-point evaluation determinant for distinct complex powers.

### Question 5: What is the precise scope of the extraction obstruction?
* **Statement**: For fixed $f \in C_c^\infty$ and $j \in C_c^\infty$, the normalized mollified norm is:
  $$N_\varepsilon(f) := \sqrt{\varepsilon}\|j_\varepsilon * f\|_2 = O(\sqrt{\varepsilon}) \longrightarrow 0 \quad (\varepsilon \to 0^+).$$
* **Obstruction**: Any linear functional family $P_\varepsilon$ satisfying a uniform continuity bound $|P_\varepsilon(g)| \le C N_\varepsilon(g)$ with $C$ independent of $\varepsilon$ must satisfy $P_\varepsilon(f) \to 0$ on fixed modes. To isolate a non-zero coefficient $P_\varepsilon(f) \to c_0 \ne 0$, the continuity constant must diverge as:
  $$C_\varepsilon \ge \frac{|P_\varepsilon(f)|}{N_\varepsilon(f)} = \Omega(\varepsilon^{-1/2}) \longrightarrow \infty.$$
* **Scope**: This is an obstruction to *uniformly bounded* linear extraction maps on fixed modes. It does not rule out $\varepsilon$-dependent test families, non-linear functionals, or multi-grade operator projections.

### Question 6: What did the arithmetic-compatibility investigation add?
* Audited 4 candidate chains connecting arithmetic structure to spectral restrictions:
  1. *Weil Positivity*: Guarantees positivity for test functions of convolution type $g * \tilde g$, but $F_\varepsilon(x, y) = w(x)w(y)\eta((x-y)/\varepsilon)$ is cross-grade and not positive-definite on the full spectrum.
  2. *TC Radial Defect*: Defines $D_M(\rho_0) = 4\sinh^2(M\delta_0\log\tau/2) > 0$ for $\delta_0 \ne 0$, but $A_{0, \Gamma} \ne c D_M(\rho_0)$ on the critical line ($A_0 > 0.54$ while $D_M = 0$).
  3. *Theta Modular Inversion*: Generates the completed zeta functional equation $\xi(s) = \xi(1-s)$, but this symmetry holds for Davenport-Heilbronn zeta functions with off-line zeros.
  4. *Vinogradov-Korobov Zero Density*: Rules out zeros very close to $\sigma = 1$ at large $t$, but does not exclude isolated off-line zeros at fixed moderate heights.
* **Key Finding**: Refuted the claim of arbitrary spectral compensation via the Finite Spectral Perturbation Rigidity Theorem.

### Question 7: Was the forbidden-coincidence bridge derived?
**No.** The implication:
$$\exists \rho_0 \ (\Re\rho_0 \ne 1/2) \Longrightarrow \exists K \ne J, m, n \in \mathbb Z \setminus \{0\}: m\tau^K = n\tau^J$$
was **not** derived. Arithmetic separation proves that $Q_\varepsilon^{K, J}[w] \equiv 0$ for $\varepsilon < d_{\min}$ on any fixed compact window. However, the explicit formula identity forces the remaining spectral and background terms to cancel the target zero ($\bar R_\varepsilon \to -A_0$), preventing the derivation of a strictly positive lower bound $\bar Q_\varepsilon \ge c D_M > 0$.

### Question 8: If not, what is the first remaining unproved implication?
The first unproved implication is the **spectral transfer step**:
$$\text{Individual radial defect } D_M(\rho_0) > 0 \Longrightarrow \bar Q_\varepsilon \ge c D_M(\rho_0) - r(\varepsilon) \quad (r(\varepsilon) \to 0).$$
On any fixed compact window, this inference is blocked by exact collective cancellation $\bar R_\varepsilon \to -A_{0, \Gamma}$. Any viable successor must avoid fixed-window scalar integration while preserving Lindemann arithmetic separation.

---

## 3. Verification Summary

| Gate / Command | Result | Notes |
|---|---|---|
| `python -m pytest tests/test_tc_mechanism_discovery.py` | **PASS** (92/92 passed in 2m 18s) | Full discovery & regression suite |
| `python -m pytest .agents/verification/test_claim_audit_gates.py` | **PASS** (54/54 passed in 0.41s) | All 10 pre-acceptance gates verified |
| `python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --claim-file .agents/claims/CLM-TC-022.json` | **PASS** (10/10 gates passed) | 0 schema violations, 0 warnings |
| `python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --cross-check-register --repo-root .` | **PASS** (110 claims verified) | 24 terminal, 78 legacy grandfathered, 8 open/exempt |
| `lake build` (in `formal/`) | **PASS** (213 compiled project declarations) | 0 sorry, 0 admit, 0 warnings |
| `python scripts/workflow.py plan-canonical` | **PASS** (17 canonical experiment runs planned) | Integrity validated |
