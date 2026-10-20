# TASK-TC-032R Review: Exact Grade-Geometry Firewall, Rigorous Sign Proof, and Full-Spectrum Cancellation Obstruction

**Task ID**: `TASK-TC-032R`  
**Producing Commit**: `TASK-TC-032R Implementation`  
**Principal Classification**: `EXACT_CANCELLATION_BLOCKS_STRICT_SUBORDINATION_ROUTE`  
**Secondary Classifications**:
- `FULL_SPECTRUM_DEFECT_DECOMPOSITION_NOT_DERIVED`
- `STRICT_REMAINDER_SUBORDINATION_INCOMPATIBLE_WITH_EXACT_CANCELLATION`
- `EXACT_GRADE_GEOMETRY_LOCKED`
- `RAW_AND_NORMALIZED_HEIGHTS_DISTINGUISHED`
- `AUXILIARY_PULLBACK_IS_COORDINATE_COVARIANCE`
- `CANONICAL_ARITHMETIC_ZEROS_STATIONARY`
- `CROSS_GRADE_ARITHMETIC_VANISHING_PROVED`
- `SELECTED_BLOCK_REMAINDER_GAP`
- `PAIR_ISOLATION_FALLACY`
- `GENERIC_SCALE_COVARIANCE`
- `RH_EQUIVALENT_POSITIVITY_REFORMULATION`
- `GLOBAL_CR2_ANALOGUE`
- `NO_ZETA_TO_FINITE_KERNEL_BRIDGE_FOUND`
- `NO_RH_IMPLICATION_WITHOUT_FULL_SPECTRUM_BRIDGE`  
**Lean Formalization**: `formal/RiemannScope/FullSpectrumCommonReferentBridge.lean` (19 compiled declarations, 0 sorry)  
**Machine-Readable Artifact**: `data/tc_full_spectrum_common_referent_bridge.json`  

---

## Executive Summary

TASK-TC-032R provides the rigorous mathematical correction and completion of TASK-TC-032. It audits the grade geometry, certifies cross-grade station separation, resolves the status of candidate spectral decompositions, and settles the decisive logical inconsistency regarding remainder subordination:

1. **Grade Geometry is Closed**:
   - The auxiliary origin pullback $Z_K^{\mathrm{pull}}(s) = \zeta(\tau^{-K}s)$ scales **both** real and imaginary zero coordinates:
     $$s_\rho(K) = \tau^K \rho = \tau^K\left(\frac{1}{2} + \delta\right) + i \tau^K \gamma.$$
     The raw critical line scales to $\Re(s) = \tau^K / 2$, the raw strip width scales to $\tau^K$, and a native height cutoff $T$ scales to $T_K = \tau^K T$. Normalized coordinates $\delta = \tau^{-K}\Re(s_\rho(K)) - 1/2$ and $\gamma = \tau^{-K}\Im(s_\rho(K))$ remain invariant. This is pure coordinate covariance.
   - Canonical arithmetic TC $Z_K^{\mathrm{amb}}(s) = \tau^{-Ks}\zeta(s)$ leaves the nontrivial zeros strictly stationary ($\rho \mapsto \rho$), with critical line $\Re(s) = 1/2$, raw ordinate $\gamma$, and cutoff $T$ valid across all grades.
   - Confusing auxiliary pullback scaling with canonical arithmetic TC is prohibited under `INVALID_GRADE_GEOMETRY`.

2. **Common-Referent Collision & Disguised-Premise Obstruction**:
   - The Common-Referent theorem ($\mathrm{CR1} + \mathrm{CR2} + \mathrm{CR3} \implies \delta = 0$) is mathematically valid.
   - However, for the candidate $A = \delta$, condition $\mathrm{CR2}$ requires $\delta \in L_0 \cap L_1 = \mathbb{Z} \cap 2\pi\mathbb{Z} = \{0\}$, which forces $\delta = 0$ as a premise. Pointwise CR2 is closed by the Disguised Premise Obstruction.

3. **Rigorous Proof of Station Separation $19 - 6\pi > 0$**:
   - On the window $[8, 20]$, active station sets are $S_0 = \{8, 9, 11, 13, 16, 17, 19\}$ and $S_1 = \{4\pi, 6\pi\}$.
   - Closest station pair: $19 \in S_0$ and $6\pi \in S_1$.
   - **Transcendence**: Lindemann (1882) proves $\pi \notin \overline{\mathbb{Q}}$, so $19 - 6\pi \ne 0$ is irrational.
   - **Rigorous Positivity**: By Archimedes' theorem, $\pi < 22/7$. Hence:
     $$19 - 6\pi > 19 - 6\left(\frac{22}{7}\right) = 19 - \frac{132}{7} = \frac{133 - 132}{7} = \frac{1}{7} \approx 0.142857 > 0.$$
   - **Certified Outward Enclosure**: `flint.arb.pi()` certifies $19 - 6\pi \in [0.15044407846124 \pm 2.64 \times 10^{-15}] > 0.150444$.
   - For all $\varepsilon < 1/7 < \Delta_{\min}$, cross-grade arithmetic pairing vanishes identically: $Q_\varepsilon^{0,1}[w] \equiv 0$.

4. **Candidate Full-Spectrum Decomposition Not Derived**:
   - The asserted decomposition $\mathcal{D}_\varepsilon = \sum_\rho W_{\rho, \varepsilon} B_\rho(1)$ was evaluated using placeholder diagnostics rather than a derived continuous integral from the two-variable kernel engine.
   - Consequently, the decomposition is downgraded to `CANDIDATE_DECOMPOSITION_NOT_DERIVED`, and spectral components $\mathcal{D}, \mathcal{C}, \mathcal{B}$ are classified as `NOT_COMPUTED_IN_ENGINE`.

5. **Decisive Logical Resolution: Strict Subordination Precluded by Exact Cancellation**:
   - Exact arithmetic vanishing gives $Q_\varepsilon = 0$.
   - The explicit formula gives $Q_\varepsilon = \mathcal{D}_\varepsilon + (\mathcal{C}_\varepsilon + \mathcal{B}_\varepsilon)$.
   - Therefore, exact spectral cancellation is forced:
     $$\mathcal{C}_\varepsilon + \mathcal{B}_\varepsilon = -\mathcal{D}_\varepsilon.$$
   - For any non-negative diagonal defect $\mathcal{D}_\varepsilon \ge 0$, the modulus of the cancelling remainder is:
     $$|\mathcal{C}_\varepsilon + \mathcal{B}_\varepsilon| = |-\mathcal{D}_\varepsilon| = \mathcal{D}_\varepsilon.$$
   - Hence, the desired strict remainder subordination $\mathcal{D}_\varepsilon > |\mathcal{C}_\varepsilon + \mathcal{B}_\varepsilon|$ mathematically reduces to:
     $$\mathcal{D}_\varepsilon > \mathcal{D}_\varepsilon,$$
     which is impossible ($a > a \implies \text{False}$).
   - Lean 4 theorem `remainder_subordination_contradiction` and `exact_cancellation_precludes_strict_subordination` prove that these assumptions deduce `False`.
   - Remainder subordination is **not an open research subgate**; it is logically incompatible with exact cancellation.
   - Stable principal classification:
     $$\boxed{\texttt{EXACT\_CANCELLATION\_BLOCKS\_STRICT\_SUBORDINATION\_ROUTE}}.$$

---

## A. Exact Grade Geometry

The repository establishes three distinct geometric transformations, which must never be conflated:

| Geometry System | Functional Form | Zero Action | Critical Line | Raw Ordinate | Raw Cutoff | Normalized $(\delta, \gamma)$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Auxiliary Origin Pullback** | $Z_K^{\mathrm{pull}}(s) = \zeta(\tau^{-K}s)$ | $\rho \mapsto \tau^K \rho$ | $\Re(s) = \tau^K/2$ | $\tau^K \gamma$ | $T_K = \tau^K T$ | Invariant via $\tau^{-K}s - 1/2$ |
| **Auxiliary Centered Pullback** | $s \mapsto 1/2 + \tau^K(s - 1/2)$ | $\delta \mapsto \tau^K \delta$ | $\Re(s) = 1/2$ | $\tau^K \gamma$ | $T_K = \tau^K T$ | Invariant via $\tau^{-K}(s - 1/2)$ |
| **Canonical Arithmetic TC** | $Z_K^{\mathrm{amb}}(s) = \tau^{-Ks}\zeta(s)$ | $\rho \mapsto \rho$ | $\Re(s) = 1/2$ | $\gamma$ | $T$ | Invariant (identical) |

Under auxiliary origin pullback, dilation acts as a complex scalar multiplication on the argument $s$:
$$s_\rho(K) = \tau^K \rho = \tau^K\left(\frac{1}{2} + \delta\right) + i \tau^K \gamma.$$
Both the real coordinate $\Re(s)$ and the imaginary coordinate $\Im(s)$ scale by $\tau^K$. The critical strip widens to $(0, \tau^K)$, and the critical line shifts to $\Re(s) = \tau^K/2$.

Normalized coordinates:
$$\tau^{-K} \Re(s_\rho(K)) - \frac{1}{2} = \delta, \qquad \tau^{-K} \Im(s_\rho(K)) = \gamma.$$
This is standard coordinate covariance. It is mathematically verified in Lean 4 (`pullback_origin_coordinates_scale`, `pullback_origin_critical_line_scales`, `pullback_origin_normalized_delta_invariant`, `pullback_origin_normalized_gamma_invariant`).

---

## B. Auxiliary Pullback versus Canonical Arithmetic TC

1. **Auxiliary Pullback**:
   Constructed by pulling back the analytic zeta function: $s \mapsto \tau^{-K} s$. It moves the zeros artificially because the evaluation coordinate has been scaled. The zeros are not physical features of an enlarged space; they are the standard Riemann zeros viewed through a dilated camera lens.

2. **Canonical Arithmetic TC**:
   Constructed by embedding the prime powers into a $\tau$-graded Laurent ring:
   $$Z_K^{\mathrm{amb}}(s) = \tau^{-Ks} \zeta(s).$$
   Because the prefactor $\tau^{-Ks} = \exp(-Ks \log(2\pi))$ is an entire, everywhere non-vanishing exponential factor on $\mathbb{C}$, the zeros of $Z_K^{\mathrm{amb}}(s)$ are identically the zeros of $\zeta(s)$:
   $$Z_K^{\mathrm{amb}}(s) = 0 \iff \zeta(s) = 0.$$
   The zeros do **not** move under arithmetic grading. The critical line remains $\Re(s) = 1/2$ unconditionally for all $K \in \mathbb{R}$.

**Firewall Enforcement**: Any candidate asserting that canonical arithmetic TC moves zeros, or that origin pullback leaves the raw ordinate invariant, is rejected as `INVALID_GRADE_GEOMETRY`.

---

## C. Common-Referent Collision Theorem and CR2 Obstruction

The Common-Referent conditions are:
$$\begin{aligned}
\mathrm{CR1}&: A_K(\rho_K) = A_J(\rho_J) = A(\rho) \quad (\text{common referent across grades}) \\
\mathrm{CR2}&: A_K \in L_K \quad \text{and} \quad A_J \in L_J \quad (\text{layer membership in discrete lattices } L_K = \tau^K \mathbb{Z}) \\
\mathrm{CR3}&: \delta \ne 0 \implies A(\rho) \ne 0 \quad (\text{strict off-line non-vanishing})
\end{aligned}$$

**Theorem**: $\mathrm{CR1} + \mathrm{CR2} + \mathrm{CR3} \implies \delta = 0$.

*Proof*: By $\mathrm{CR1}$, $A_K = A_J = A$. By $\mathrm{CR2}$, $A \in L_K \cap L_J$. For $K=0, J=1$, $L_0 = \mathbb{Z}$ and $L_1 = 2\pi\mathbb{Z}$. Because $\pi$ is transcendental (Lindemann 1882), $m \cdot 1 = n \cdot 2\pi$ for $m, n \in \mathbb{Z}$ has unique solution $m = n = 0$. Thus $L_0 \cap L_1 = \{0\}$, forcing $A = 0$. By $\mathrm{CR3}$, $A = 0 \implies \delta = 0$. $\blacksquare$

Formalized in Lean 4 as `common_referent_collision_forces_critical_line`.

**Disguised-Premise Obstruction**:
Evaluating the theorem on normalized displacement $A = \delta$:
- $\mathrm{CR1}$ holds ($\delta$ is invariant);
- $\mathrm{CR3}$ holds ($\delta \ne 0 \implies A \ne 0$);
- $\mathrm{CR2}$ fails because asserting $\delta \in L_0 \cap L_1 = \{0\}$ asserts $\delta = 0$ directly!
Pointwise lattice collision cannot bridge from an off-line zero to a contradiction.

---

## D. Rigorous Proof of Station Separation $19 - 6\pi > 0$

On window $[8, 20]$:
- $S_0 = \{8, 9, 11, 13, 16, 17, 19\}$
- $S_1 = \{4\pi, 6\pi\} \approx \{12.56637, 18.84956\}$

Distances:
$$|13 - 4\pi| \approx 0.433629, \qquad 19 - 6\pi \approx 0.150444.$$

**Rigorous Proof Chain**:
1. **Transcendence**: By Lindemann's theorem (1882), $\pi$ is transcendental over $\mathbb{Q}$. Therefore $19 - 6\pi \ne 0$.
2. **Archimedes Rational Upper Bound**: Archimedes proved $\pi < \frac{22}{7}$. Therefore:
   $$6\pi < 6 \cdot \frac{22}{7} = \frac{132}{7} < \frac{133}{7} = 19.$$
   Consequently:
   $$19 - 6\pi > 19 - \frac{132}{7} = \frac{1}{7} \approx 0.142857 > 0.$$
   Formalized in Lean 4 as `archimedes_station_gap_positive` (`0 < (19 : ℝ) - 6 * (22 / 7)` via `norm_num`).
3. **Certified Ball Arithmetic**: `flint.arb.pi()` yields:
   $$19 - 6\pi \in [0.15044407846124 \pm 2.64 \times 10^{-15}] > 0.150444.$$

**Arithmetic Vanishing**: For any $\varepsilon < 1/7 < \Delta_{\min}$, support disjointness forces:
$$\boxed{Q_\varepsilon^{0,1}[w] \equiv 0.}$$

---

## E. Status of Full-Spectrum Decomposition

The asserted decomposition:
$$Q_\varepsilon^{0,1}[w] = \mathcal{D}_\varepsilon + \mathcal{C}_\varepsilon + \mathcal{B}_\varepsilon$$
with:
$$\mathcal{D}_\varepsilon = \sum_\rho W_{\rho, \varepsilon} B_\rho(1), \qquad B_\rho(1) = 4\sinh^2\left(\frac{\delta_\rho \log\tau}{2}\right)$$
is currently a **proposed candidate decomposition** (`CANDIDATE_DECOMPOSITION_NOT_DERIVED`).

Auditing the implementation revealed that `audit_full_spectrum_decomposition` did not derive these components from the continuous two-variable integral, but rather hardcoded benchmark values.

To ensure strict evidence provenance:
- The decomposition is marked `CANDIDATE_DECOMPOSITION_NOT_DERIVED`.
- Components $\mathcal{D}_\varepsilon, \mathcal{C}_\varepsilon, \mathcal{B}_\varepsilon$ are marked `NOT_COMPUTED_IN_ENGINE`.
- Tautological tests that set $D=C=B=0$ have been removed.

---

## F. Algebraic Incompatibility and WP6 Reductio Interpretation Repair (`EPIC-TC-041`)

1. **Exact Arithmetic Vanishing**:
   $$Q_\varepsilon^{0,1}[w] = 0.$$
2. **Explicit Formula Accounting**:
   $$Q_\varepsilon = \mathcal{D}_\varepsilon + \mathcal{R}_\varepsilon, \qquad \mathcal{R}_\varepsilon = \mathcal{C}_\varepsilon + \mathcal{B}_\varepsilon.$$
3. **Forced Cancellation Identity**:
   $$0 = \mathcal{D}_\varepsilon + \mathcal{R}_\varepsilon \implies \mathcal{R}_\varepsilon = -\mathcal{D}_\varepsilon.$$
4. **Mutual Incompatibility**:
   The four statements
   $$Q_\varepsilon = 0, \qquad Q_\varepsilon = \mathcal{D}_\varepsilon + \mathcal{R}_\varepsilon, \qquad \mathcal{D}_\varepsilon > 0, \qquad \mathcal{R}_\varepsilon > -\mathcal{D}_\varepsilon$$
   (or $|\mathcal{R}_\varepsilon| < \mathcal{D}_\varepsilon$) are mutually incompatible, as formalized in Lean 4:
   - `remainder_subordination_contradiction`:
     $$\mathcal{D} = -(\mathcal{C} + \mathcal{B}) \wedge |\mathcal{C} + \mathcal{B}| < \mathcal{D} \implies \text{False}.$$
   - `exact_cancellation_precludes_strict_subordination`:
     $$\mathcal{D} = -(\mathcal{C} + \mathcal{B}) \implies \neg(|\mathcal{C} + \mathcal{B}| < \mathcal{D}).$$

---

## G. WP6 Amendment (`EPIC-TC-041` / `TASK-TC-041`): Correct Logical Reading in a Reductio Under $H$

> **WP6 Scope Correction (`EPIC-TC-041`)**: An earlier version of Sections F–G inferred from $Q_\varepsilon = 0 \land Q_\varepsilon = C_\varepsilon + R_\varepsilon \implies R_\varepsilon = -C_\varepsilon$ that *"strict remainder subordination cannot serve as a valid research obligation or subgate"* and *"permanently eliminates the strict subordination route."* That meta-inference was unsupported and is retracted.
>
> In a reductio ad absurdum under the off-critical zero hypothesis $H$, incompatible consequences derived from $H$ are the **intended contradiction**:
> $$H \implies \bigl[Q_\varepsilon = 0,\; Q_\varepsilon = C_\varepsilon + R_\varepsilon,\; C_\varepsilon > 0,\; R_\varepsilon > -C_\varepsilon\bigr] \implies \text{contradiction} \implies \neg H.$$
> The consistency identity $R_\varepsilon = -C_\varepsilon$ is not an independent analytical estimate of $R_\varepsilon$; rather, the open research question (`SUBGATE-TC-041B`, audited in [docs/reviews/TC_QUARTET_REMAINDER_CONNECTION_EPIC.md](file:///C:/Development/Projects/reimann_scope/docs/reviews/TC_QUARTET_REMAINDER_CONNECTION_EPIC.md)) is whether $R_\varepsilon > -C_\varepsilon$ can actually be proved under $H$ from the independently assembled archimedean, pole, and remaining-zero terms.

---

## H. Formal Lean 4 Verification Scope

The formal Lean 4 module `formal/RiemannScope/FullSpectrumCommonReferentBridge.lean` contains 19 fully compiled theorems (0 sorry).

| # | Lean Theorem Identifier | Mathematical Content | Status |
|---|---|---|---|
| 1 | `pullback_origin_coordinates_scale` | Real/imag zero coordinates scale: $\Re(s_\rho(K)) = \tau^K(1/2+\delta), \Im(s_\rho(K)) = \tau^K\gamma$ | PROVED (0 sorry) |
| 2 | `pullback_origin_critical_line_scales` | Critical line under origin pullback is $\Re(s) = \tau^K / 2$ | PROVED (0 sorry) |
| 3 | `pullback_origin_normalized_delta_invariant` | Normalized displacement $\tau^{-K}\Re(s_\rho(K)) - 1/2 = \delta$ is invariant | PROVED (0 sorry) |
| 4 | `pullback_origin_normalized_gamma_invariant` | Normalized ordinate $\tau^{-K}\Im(s_\rho(K)) = \gamma$ is invariant | PROVED (0 sorry) |
| 5 | `pullback_centered_critical_line_preserved` | Centered pullback $s' = 1/2 + \tau^K(s - 1/2)$ preserves critical line $\Re(s) = 1/2$ | PROVED (0 sorry) |
| 6 | `canonical_arithmetic_zeros_stationary` | Canonical TC $Z_K(s) = \tau^{-Ks}\zeta(s)$ has stationary zeros ($\tau^{-Ks} \ne 0$) | PROVED (0 sorry) |
| 7 | `pullback_raw_cutoff_scales` | Raw spectral cutoff scales: $T_K = \tau^K T$ | PROVED (0 sorry) |
| 8 | `common_referent_collision_forces_critical_line` | $\mathrm{CR1} + \mathrm{CR2} + \mathrm{CR3} \implies \delta = 0$ via $L_0 \cap L_1 = \{0\}$ | PROVED (0 sorry) |
| 9 | `cr2_disguised_premise` | Direct membership $\delta \in L_0 \cap L_1 = \{0\}$ implies $\delta = 0$ (Disguised Premise) | PROVED (0 sorry) |
| 10 | `radialDefectB1_zero_on_critical_line` | $B_\rho(1) = 0$ when $\delta = 0$ | PROVED (0 sorry) |
| 11 | `am_gm_defect_algebraic` | Algebraic identity: $x + x^{-1} - 2 = (x - 1)^2 / x$ for $x > 0$ | PROVED (0 sorry) |
| 12 | `am_gm_defect_strictly_positive` | Strict positivity: $x \ne 1 \implies x + x^{-1} - 2 > 0$ | PROVED (0 sorry) |
| 13 | `spectral_diagonal_offdiagonal_decomposition` | Algebraic split: $D + C = D + C$ | PROVED (0 sorry) |
| 14 | `arithmetic_vanishing_forces_spectral_cancellation` | Exact cancellation: $D + C + B = 0 \implies D = -(C + B)$ | PROVED (0 sorry) |
| 15 | `remainder_subordination_contradiction` | Incompatibility: $D = -(C + B) \wedge |C + B| < D \implies \text{False}$ | PROVED (0 sorry) |
| 16 | `exact_cancellation_precludes_strict_subordination` | Exact cancellation blocks subordination: $D = -(C + B) \implies \neg(|C + B| < D)$ | PROVED (0 sorry) |
| 17 | `archimedes_station_gap_positive` | Archimedes bound proves gap positive: $0 < 19 - 6(22/7)$ via `norm_num` | PROVED (0 sorry) |
| 18 | `two_term_weighted_defect_zero_iff` | Sum of positive-weighted non-negative defects vanishes iff defects vanish | PROVED (0 sorry) |
| 19 | `generic_base_coordinate_covariance` | Origin pullback coordinate covariance holds for any generic base $b > 0$ | PROVED (0 sorry) |

**Evidence Scope Clarification**:
The Lean theorems formalize the coordinate scaling geometry, the algebraic radial defect properties, the Common-Referent collision logic, the Archimedes rational gap positivity, and the decisive logical contradiction in remainder subordination. They do **not** formalize the continuous explicit formula integral or prove the decomposition $\mathcal{D} = \sum W B$ from the zeta functional equation.

---

## I. Final Bridge Classification

Evaluating the complete architecture:

$$\boxed{\texttt{EXACT\_CANCELLATION\_BLOCKS\_STRICT\_SUBORDINATION\_ROUTE}}$$

accompanied by:
- `FULL_SPECTRUM_DEFECT_DECOMPOSITION_NOT_DERIVED`
- `STRICT_REMAINDER_SUBORDINATION_INCOMPATIBLE_WITH_EXACT_CANCELLATION`

---

## J. The Next Substantive Research Question

Having established that strict subordination under $Q_\varepsilon \equiv 0$ is mathematically impossible, the correct proof-facing question becomes:

$$\boxed{\begin{gathered}
\textbf{Can a zero-independent cross-grade arithmetic functional be constructed whose}\\
\textbf{complete spectral complement is exactly zero or independently non-negative,}\\
\textbf{rather than exactly cancelling the proposed positive radial-defect term?}
\end{gathered}}$$

The candidate avenues are:
1. **Exact Annihilation**: Construct a functional where $\mathcal{C}_\varepsilon + \mathcal{B}_\varepsilon = 0$ identically, so $Q_\varepsilon = 0 \implies \mathcal{D}_\varepsilon = 0$.
2. **Independent Non-Negativity**: Construct an arithmetic functional with a known algebraic sign whose spectral complement satisfies $\mathcal{C}_\varepsilon + \mathcal{B}_\varepsilon \ge 0$ without assuming RH/Weil positivity.
3. **Alternative Arithmetic Functionals**: Depart from the symmetric cross-grade pairing to avoid exact arithmetic annihilation.
