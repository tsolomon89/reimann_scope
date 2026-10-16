# TASK-TC-037 / TASK-TC-037R Review: Bigraded Character Projection, Reflection-Sector Isolation, Transport-Compatibility Audit, and Evidence Repair

**Task ID**: `TASK-TC-037R` (repairing `TASK-TC-037`)  
**Starting HEAD (`TASK-TC-037R`)**: `68fd5b66a941274c56d5d03a40b4c939ab24af3f`  
**Substantive Parent (`TASK-TC-037`)**: `799076f623f13b559fc4c6da7507caee2eb434c8`  
**Original Starting HEAD (`TASK-TC-037`)**: `02dce7dd62492605e88f72c05c9efb67a900f84e`  
**Principal Classification**: `GRADE_CHARACTER_PROJECTION_DOES_NOT_ESCAPE_TRANSPORT_MOMENT_INCOMPATIBILITY`  
**Tested Transport Classification**: `GRADE_CHARACTER_PROJECTION_INCOMPATIBLE_WITH_TESTED_TRANSPORT_ANSATZ`  
**Secondary / Følner Classification**: `OFF_CRITICAL_NONUNITARITY_BLOCKS_FOLNER_CHARACTER_PROJECTION` (`OFF_CRITICAL_NONUNITARITY_BLOCKS_GRADE_HAAR_PROJECTION`)  
**Obligation Status**: `OBL-CT-001A = OPEN` (`SUBGATE-TC-037A = OPEN`, refining `SUBGATE-TC-036A`)  
**Formal Assurance**: 0 `sorry`, 0 `admit`, no nonstandard project axioms introduced (`formal/RiemannScope/GradeCharacterProjection.lean`, 5 `def` + 17 `theorem` declarations).

---

## TASK-TC-037R Evidence Repair

### A. Preserved results from TASK-TC-037
- **Sesquilinear common-shift stationarity** (`reflection_stationary_iff`):
  $$z_\rho + \overline{z_\sigma} = 0 \iff \bigl(\delta_\rho + \delta_\sigma = 0 \;\land\; \gamma_\rho = \gamma_\sigma\bigr) \iff \sigma = 1 - \bar\rho.$$
- **Off-critical diagonal character nonunitarity** (`offcritical_diagonal_character_nonunitary`):
  For $\sigma = \rho$, $\lambda_{\rho,\rho} = z_\rho + \overline{z_\rho} = 2\delta_\rho$ and $q_{\rho,\rho} = \tau^{2\delta_\rho} \neq 1 \iff \delta_\rho \neq 0$.
- **Curvature-polynomial reflection quartet identity** (`reflection_quartet_imaginary_cancellation`):
  $$P(z_\rho, -\bar z_\rho) + P(\bar z_\rho, -z_\rho) = (4\delta_\rho^2 + 4i\gamma_\rho) + (4\delta_\rho^2 - 4i\gamma_\rho) = 8\delta_\rho^2.$$
- **Transport–projection incompatibility within tested ansatz** (`transport_projection_incompatibility_algebra`):
  Under $F_r(x, y) = \tau^{ar} F_0(\tau^{-br}x, \tau^{-br}y)$, preserving the prime-station gap at $(0, 1) \mapsto (r, 1+r)$ forces $b = 1$, which identically cancels $(b - 1)r(s + t) = 0$.

### B. Distinct-zero multiplicity repair
- **Multiplicity vs. distinct zeros**: $N(T) = \sum_{0 < \gamma_\rho < T} m_\rho$ counts zeros **with** multiplicity, whereas $N_{\mathrm{dist}}(T) = \#\{\rho = \beta + i\gamma : 0 < \gamma < T, \zeta(\rho) = 0\}$ counts **distinct** complex zeros without multiplicity.
- Because the vertical-progression fiber argument counts distinct complex zeros $\sigma$ satisfying $\tau^{z_{\rho_0} + \bar z_\sigma} = w_j$, comparing $O_M(T)$ against $N(T)$ alone left a multiplicity gap unless $N_{\mathrm{dist}}(T) \gg T\log T$ is cited.

### C. Primary literature citation for distinct / simple critical-line zeros
- By the unconditional simple critical-line zero density theorem of **H. M. Bui, B. Conrey, and M. P. Young (2011)**, *"More than 41% of the zeros of the zeta function are on the critical line"*, *Acta Arithmetica* **150** (2011), no. 1, 35–64, DOI `10.4064/aa150-1-3`, [arXiv:1002.4127v2](https://arxiv.org/abs/1002.4127v2), Theorem 1.1 (eq. (1.1), p. 1) & Section 2.2 (p. 3) (building on **J. B. Conrey 1989**, *J. Reine Angew. Math.* **399**, 1–26, $\kappa^* \ge 0.4013$, and **N. Levinson 1974 / D. R. Heath-Brown 1979**, *Bull. London Math. Soc.* **11**, 17–18, $\kappa^* \ge 1/3$; see also **K. Pratt, N. Robles, A. Zaharescu, and D. Zeindler 2020**, *Res. Math. Sci.* **7**, Paper No. 2, [arXiv:1802.10521v3](https://arxiv.org/abs/1802.10521v3)):
  $$N_0^*(T) = \#\left\{\rho = \tfrac12 + i\gamma : 0 < \gamma < T, \;\zeta(\rho) = 0, \;\zeta'(\rho) \neq 0\right\} \ge (0.4058 - o(1))N(T).$$
- Because every simple zero has multiplicity $m_\rho = 1$, distinct simple critical-line zeros form a subset of all distinct zeros in the strip:
  $$N_{\mathrm{dist}}(T) \ge N_0^*(T) \ge (0.4058 - o(1))\frac{T}{2\pi}\log\frac{T}{2\pi e} \gg T\log T.$$
- Any finite set $\{w_1, \dots, w_M\} \subset \mathbb{C}^\times$ of character values restricts $\sigma$ to $M$ vertical progressions of ordinate spacing $\frac{2\pi}{\log\tau}$, accounting for at most $M(\frac{\log\tau}{2\pi}T + O(1)) = O_M(T)$ distinct zeros up to height $T$, which is strictly dominated by $N_{\mathrm{dist}}(T) \gg T\log T$ (`DISTINCT_PAIR_CHARACTERS_PROVED_USING_DISTINCT_ZERO_DENSITY`).

### D. Complex finite Laurent and differential projector Lean theorems
- Formalized directly over $\mathbb{C}[X]$ (`Polynomial ℂ`) in `formal/RiemannScope/GradeCharacterProjection.lean`:
  - `finite_complex_polynomial_projector_root_no_go` (for $Q(q) = q^N P_N(q) \in \mathbb{C}[q]$ of degree $\le 2N$ vanishing on $> 2N$ distinct complex characters $q_{\rho_0,\sigma} \in \mathbb{C}^\times$);
  - `finite_complex_differential_projector_root_no_go` (for $p(X) \in \mathbb{C}[X]$ of degree $\le M$ vanishing on $> M$ distinct complex pair exponents $(\log\tau)\lambda_{\rho_0,\sigma} \in \mathbb{C}$).
- Classification: `FINITE_COMPLEX_GRADE_PROJECTOR_NO_GO_FORMALIZED`.

### E. Corrected relative-grade exponent on reflection pairs
- For $K = r - d$ and $J = r + d$, the sesquilinear exponent is
  $$K z_\rho + J \overline{z_\sigma} = r(z_\rho + \overline{z_\sigma}) + d(\overline{z_\sigma} - z_\rho).$$
- On the reflection pair $\sigma = 1 - \bar\rho$, $z_\sigma = -\bar z_\rho$ and $\overline{z_\sigma} = -z_\rho$, so $z_\rho + \overline{z_\sigma} = 0$ and
  $$\lambda_{\mathrm{relative}}(\rho, 1-\bar\rho) = \overline{z_\sigma} - z_\rho = -2z_\rho = -2\delta_\rho - 2i\gamma_\rho,$$
  giving $(r - d)z_\rho + (r + d)\overline{z_\sigma} = -2d z_\rho = -2d\delta_\rho - 2id\gamma_\rho$ (`sesquilinear_relative_exponent_at_reflection`, `RELATIVE_GRADE_REFLECTION_EXPONENT_REPAIRED`). Writing $2\delta_\rho$ confused $z_\rho - z_\sigma = 2\delta_\rho$ with $\overline{z_\sigma} - z_\rho = -2z_\rho$.

### F. Relative-grade second derivative vs. curvature-polynomial quartet
- Differentiating $\tau^{-2d z_\rho}$ twice with respect to $d$ at $d = 0$ yields $4(\log\tau)^2 z_\rho^2 = 4(\log\tau)^2((\delta_\rho^2 - \gamma_\rho^2) + 2i\delta_\rho\gamma_\rho)$. Combining $(\rho, 1-\bar\rho)$ and $(\bar\rho, 1-\rho)$ gives (`relative_grade_second_derivative_not_radial`):
  $$4(\log\tau)^2\left(z_\rho^2 + \bar z_\rho^2\right) = 8(\log\tau)^2\left(\delta_\rho^2 - \gamma_\rho^2\right) < 0 \qquad (|\delta_\rho| < |\gamma_\rho|),$$
  which is **not** pure radial (`RELATIVE_GRADE_DIFFERENTIATION_NOT_PURE_RADIAL`).
- By contrast, the fixed-grade curvature polynomial $P(z_\rho, z_\sigma) = (z_\rho - z_\sigma)^2 + 2(z_\rho + z_\sigma)$ from $\mathcal{L}_{\mathrm{TC}} = 4\mathcal{D}^2 + 2\mathcal{D}$ evaluates on the reflection quartet to $8\delta_\rho^2$ (`REFLECTION_QUARTET_RADIAL_IDENTITY_PRESERVED`).

### G. Fourier self-duality vs. multiplicative inversion-evenness
- $\widetilde{g}_1(u) = e^{-\pi u^2}$ is self-dual under the additive Fourier transform $(\mathcal{F}g)(u) = \int_{\mathbb{R}} g(x)e^{-2\pi i x u}\,dx$, **not** invariant under multiplicative inversion $(\mathcal{I}\Psi)(u) = u^{-1}\Psi(u^{-1})$ on $(\mathbb{R}_+, du/u)$.
- Even at $t = 1$, $\widehat{\Phi_1^{(2)}}(z) = \frac{1}{32}(z^2 - \frac14)^2 \pi^{-(1/2+z)/2}\Gamma(\frac{1/2+z}{2}) \neq \widehat{\Phi_1^{(2)}}(-z)$ for generic $z \neq 0$ (`raw_phi_t1_inversion_even = False`, `FOURIER_SELF_DUALITY_DISTINCT_FROM_MULTIPLICATIVE_INVERSION_EVENNESS`).

### H. Raw-state vs. symmetrized-state Mellin nonvanishing
- **Raw state $\Phi_t^{(2)}$**: $\widehat{\Phi_t^{(2)}}(z) \neq 0$ throughout $-\frac12 < \operatorname{Re} z < \frac12$ ($0 < \operatorname{Re} s < 1$).
- **Symmetrized state $\Psi_t^+ = \frac12(\Phi_t^{(2)} + \mathcal{I}\Phi_t^{(2)})$**: $\widehat{\Psi_t^+}(z) = \frac12(\widehat{\Phi_t^{(2)}}(z) + \widehat{\Phi_t^{(2)}}(-z)) = \widehat{\Psi_t^+}(-z)$ (`symmetrized_psi_plus_inversion_even = True`, `inversion_even_mellin_symmetry_algebra`). On $\operatorname{Re} z = 0$ at $t = 1$, $\widehat{\Psi_1^+}(i\gamma) = \operatorname{Re}\widehat{\Phi_1^{(2)}}(i\gamma)$ oscillates and changes sign (certified via 128-bit Arb ball arithmetic between $\gamma_a = 0.25$ where $\widehat{\Psi_1^+}(0.25i) \approx +0.005930018171819737 > 0$ and $\gamma_b = 1.0$ where $\widehat{\Psi_1^+}(1.0i) \approx -0.01007544310514176 < 0$), so $\widehat{\Psi_t^+}(z)$ is **not** zero-free in the critical strip (`INVERSION_EVEN_MELLIN_ZERO_FREE_STRIP_FALSE`).

### I. Repaired reflection-weight status
- $W_\rho(t) = m_\rho^2 |\widehat{\Psi_t^+}(z_\rho)|^2 \ge 0$ and $8 W_\rho(t)\delta_\rho^2 \ge 0$ are proved unconditionally (`reflection_weight_nonnegative`, `REFLECTION_WEIGHT_NONNEGATIVE_PROVED`).
- Strict positivity $W_\rho(t) > 0$ at a hypothetical off-critical zero requires $\widehat{\Psi_t^+}(z_\rho) \neq 0$ and is classified as `REFLECTION_WEIGHT_STRICT_POSITIVITY_NOT_YET_PROVED` (`STRICT_REFLECTION_WEIGHT_AT_ZETA_ZERO_ORDINATES_OPEN`).

### J. Følner / Cesàro nonunitarity terminology
- Because $(\mathbb{Z}, +)$ and $(\mathbb{R}, +)$ are noncompact locally compact abelian groups, their Haar measures are infinite; the bilateral averages $A_N(q)$ and $C_T(\lambda)$ are **Følner / Cesàro character averages** (approximate invariant means), which converge to the trivial-character indicator on the unitary dual $\mathbb{T}$ or $i\mathbb{R}$ and diverge exponentially on off-critical nonunitary characters $q_{\rho,\rho} = \tau^{2\delta_\rho} \neq 1$ (`OFF_CRITICAL_NONUNITARITY_BLOCKS_FOLNER_CHARACTER_PROJECTION`).

### K. Scoped transport-compatibility status
- The transport–projection incompatibility $(b - 1)r(s + t) = 0$ at $b = 1$ is scoped to the tested power-scaled homogeneous two-variable transport ansatz $F_r(x, y) = \tau^{ar}F_0(\tau^{-br}x, \tau^{-br}y)$ (`GRADE_CHARACTER_PROJECTION_INCOMPATIBLE_WITH_TESTED_TRANSPORT_ANSATZ`, `GRADE_CHARACTER_PROJECTION_DOES_NOT_ESCAPE_TRANSPORT_MOMENT_INCOMPATIBILITY`).

### L. Repaired `SUBGATE-TC-037A`
- Stated in Section W below with all four explicit requirements (including proving strict positivity of the reflection-sector weight for $\delta_\rho \neq 0$).

### M. Synchronized Lean theorem table
- All 5 `def` and 17 `theorem` declarations in `formal/RiemannScope/GradeCharacterProjection.lean` are catalogued in the Compact Evidence Table below.

---

### A. TASK-TC-036R starting point

`TASK-TC-036R` repaired the pole regularization of the completed theta–conductor functional by replacing the unshifted operator $\mathcal{D}(\mathcal{D} - \tfrac{1}{2})$ (which acts on $\widetilde{g}_t(u) = t^{1/4} e^{-\pi t u^2}$ by $\tfrac{s^2}{4} - \tfrac{1}{16}$ and fails to vanish at $s \in \{0, 1\}$) with the exact pole-killing polynomial in $\mathcal{D} = t\partial_t$:

$$\widetilde{g}_t(u) = t^{1/4} e^{-\pi t u^2}, \qquad \mathcal{P}_{\mathrm{reg}}(\mathcal{D}) = \mathcal{D}^2 - \frac{1}{16},$$

and the admissible states

$$\Phi_t = \mathcal{P}_{\mathrm{reg}}(\mathcal{D})\widetilde{g}_t, \qquad \Phi_t^{(2)} = \mathcal{P}_{\mathrm{reg}}(\mathcal{D})^2\widetilde{g}_t.$$

On the Mellin side ($s = \frac{1}{2} + z$), $\mathcal{D} = t\partial_t$ acts on $t^{1/4 - s/2}$ by $\frac{1}{4} - \frac{s}{2} = -\frac{z}{2}$, so $\mathcal{P}_{\mathrm{reg}}(\mathcal{D})$ acts by

$$\left(\frac{1}{4} - \frac{s}{2}\right)^2 - \frac{1}{16} = \frac{1}{4}s(s - 1) = \frac{1}{4}\left(z^2 - \frac{1}{4}\right),$$

and $\mathcal{P}_{\mathrm{reg}}(\mathcal{D})^2$ acts by $\frac{1}{16}s^2(s-1)^2 = \frac{1}{16}(z^2 - \frac{1}{4})^2$, vanishing to order $2$ at both completed pole locations $s = 0$ and $s = 1$ ($z = \mp \frac{1}{2}$). However, the completed quadratic functional remained an unrestricted double zero sum over all pairs $(\rho, \sigma)$, leaving `SUBGATE-TC-036A` and `OBL-CT-001A` open.

---

### B. Why grade projection is the next TC-native candidate

In the unrestricted double zero sum over $(\rho, \sigma)$, the radial displacement $\delta_\rho = \operatorname{Re}(\rho) - \frac{1}{2}$ appears cleanly inside the same-height functional-equation reflection pair $\sigma = 1 - \bar{\rho}$ (where $z_\rho + \overline{z_\sigma} = 0$, while in the fixed-grade curvature polynomial $z_\rho - z_\sigma = 2\delta_\rho$). Rather than searching for another privileged single test kernel (`TASK-TC-035`) or another heat/conductor differential commutator (`TASK-TC-036`), `TASK-TC-037` tests whether the **TC grade variable itself** can act as a zero-independent spectral selector that isolates the reflection sector $\sigma = 1 - \bar{\rho}$ as the stationary character of a bigraded common-shift action while preserving an incompatible arithmetic law.

> **Hypothesis-Fidelity Firewall**:
> - **General TC hypothesis**: One arithmetic object represented through all $\tau$-grades implies a compatibility constraint.
> - **Candidate mechanism**: Grade characters provide a zero-independent projector onto the reflection sector $(\rho, 1 - \bar{\rho})$.
> - **Scope**: Failure of this projector candidate does **not** refute the general TC hypothesis (`candidate_failure_refutes_tc = False`).

---

### C. Zero-symmetry group

For every nontrivial zero $\rho = \frac{1}{2} + \delta_\rho + i\gamma_\rho$, let the centered coordinate be

$$z_\rho = \rho - \frac{1}{2} = \delta_\rho + i\gamma_\rho.$$

The four canonical symmetries form a Klein four-group $V_4 = \{I, C, F, R\} \cong \mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}/2\mathbb{Z}$ with $I^2 = C^2 = F^2 = R^2 = I$ and $R = F \circ C = C \circ F$:

| Symmetry | Zero | Centered coordinate |
|---|---|---|
| $I$ (Identity) | $\rho = \frac{1}{2} + \delta_\rho + i\gamma_\rho$ | $z = \delta_\rho + i\gamma_\rho$ |
| $C$ (Schwarz conjugation) | $\bar{\rho} = \frac{1}{2} + \delta_\rho - i\gamma_\rho$ | $\bar{z} = \delta_\rho - i\gamma_\rho$ |
| $F$ (Functional-equation reflection) | $1 - \rho = \frac{1}{2} - \delta_\rho - i\gamma_\rho$ | $-z = -\delta_\rho - i\gamma_\rho$ |
| $R = F \circ C$ (Same-height reflection) | $1 - \bar{\rho} = \frac{1}{2} - \delta_\rho + i\gamma_\rho$ | $-\bar{z} = -\delta_\rho + i\gamma_\rho$ |

This table and the involution identity $R^2 = I$ are formalized in Lean 4 as `centered_zero_reflection_identity`.

---

### D. Exact grade character

Let $\tau = 2\pi$. Under the repository's prime-station grade scaling $x_K(n) = \tau^K n$ (which pairs the explicit-formula prime distribution against the inverse half-density dilated state $(U_{-K}\Psi)(u) = \tau^{-K/2}\Psi(\tau^{-K}u)$), the centered Mellin transform $\widehat{\Psi}(z) = \int_0^\infty \Psi(u) u^{z - 1/2}\,du$ transforms as

$$\widehat{U_{-K}\Psi}(z) = \int_0^\infty \tau^{-K/2}\Psi(\tau^{-K}u) u^{z - 1/2}\,du = \tau^{K z}\widehat{\Psi}(z)$$

(whereas under the forward half-density dilation $(U_K\Psi)(u) = \tau^{K/2}\Psi(\tau^K u)$, $\widehat{U_K\Psi}(z) = \tau^{-K z}\widehat{\Psi}(z)$). Recording the station-dilation convention $\chi_z(K) = \tau^{K z}$ explicitly:
- **Arithmetic station action**: $n \mapsto \tau^K n$ (test state $U_{-K}\Psi$);
- **Mellin action**: $\widehat{\Psi}(z) \mapsto \tau^{K z}\widehat{\Psi}(z)$;
- **Centered spectral character**: $\chi_z(K) = \tau^{K z} = e^{K(\delta + i\gamma)\log\tau}$;
- **Amplitude**: $|\chi_z(K)| = \tau^{K\delta}$;
- **Phase**: $\arg\chi_z(K) \equiv K\gamma\log\tau \pmod{2\pi}$.

For $K \neq 0$, unitarity satisfies the control equivalence

$$|\chi_z(K)| = 1 \iff \operatorname{Re}(z) = \delta = 0.$$

---

### E. Bigraded completed functional

Introducing two independent grade variables $(K, J)$ and the completed explicit-formula linear functional $W_{\mathrm{comp}}(\Psi) = \sum_\rho m_\rho \widehat{\Psi}(z_\rho)$, we construct the zero-independent bigraded completed correlation

$$\mathcal{G}_{\mathcal{S}}(K, J) = W_{\mathrm{comp}}(U_{-K}\Psi_t)\,\mathcal{S}\!\left[W_{\mathrm{comp}}(U_{-J}\Psi_t)\right], \qquad \mathcal{S} \in \{I, C, F, R\},$$

using the repaired state $\Psi_t = \Phi_t^{(2)}$ (or its inversion-even part $\Psi_t^+$):
- For $\mathcal{S} = I$: bilinear, zero-independent, convergent for all $t > 0$ and $(K, J) \in \mathbb{R}^2$.
- For $\mathcal{S} = C$: sesquilinear ($\mathcal{G}_C(K, J) = W_{\mathrm{comp}}(U_{-K}\Psi_t)\overline{W_{\mathrm{comp}}(U_{-J}\Psi_t)}$), zero-independent, convergent for all $t > 0$ and $(K, J) \in \mathbb{R}^2$.
- For $\mathcal{S} = F$: bilinear with second-leg multiplicative inversion $U_J = U_{-(-J)}$.
- For $\mathcal{S} = R = F \circ C$: sesquilinear with second-leg multiplicative inversion.

---

### F. Common-shift stationary-pair table

In common-shift and relative-grade coordinates

$$r = \frac{K + J}{2}, \qquad d = \frac{J - K}{2}, \qquad K = r - d, \qquad J = r + d,$$

each pair $(\rho, \sigma)$ transforms under the common shift $r$ by $e^{r \lambda_{\mathcal{S}}(\rho, \sigma)\log\tau}$, where:

| Second-leg structure $\mathcal{S}$ | Pair exponent $\lambda_{\mathcal{S}}(\rho, \sigma)$ | Relative exponent $\mu_{\mathcal{S}}(\rho, \sigma)$ | Stationary condition $\lambda_{\mathcal{S}} = 0$ | Selected zero relation |
|---|---|---|---|---|
| $I$ (bilinear) | $z_\rho + z_\sigma = (\delta_\rho + \delta_\sigma) + i(\gamma_\rho + \gamma_\sigma)$ | $z_\sigma - z_\rho$ | $\delta_\sigma = -\delta_\rho \;\land\; \gamma_\sigma = -\gamma_\rho$ | $\sigma = 1 - \rho$ ($F$-pair) |
| $C$ (sesquilinear conjugation) | $z_\rho + \bar{z}_\sigma = (\delta_\rho + \delta_\sigma) + i(\gamma_\rho - \gamma_\sigma)$ | $\bar{z}_\sigma - z_\rho$ | $\delta_\sigma = -\delta_\rho \;\land\; \gamma_\sigma = \gamma_\rho$ | $\sigma = 1 - \bar{\rho}$ ($R$-reflection pair) |
| $F$ (bilinear + inversion) | $z_\rho - z_\sigma = (\delta_\rho - \delta_\sigma) + i(\gamma_\rho - \gamma_\sigma)$ | $-z_\sigma - z_\rho$ | $\delta_\sigma = \delta_\rho \;\land\; \gamma_\sigma = \gamma_\rho$ | $\sigma = \rho$ (diagonal $I$-pair) |
| $R = F \circ C$ (sesquilinear + inversion) | $z_\rho - \bar{z}_\sigma = (\delta_\rho - \delta_\sigma) + i(\gamma_\rho + \gamma_\sigma)$ | $-\bar{z}_\sigma - z_\rho$ | $\delta_\sigma = \delta_\rho \;\land\; \gamma_\sigma = -\gamma_\rho$ | $\sigma = \bar{\rho}$ (conjugate $C$-pair) |

Thus the natural zero-independent sesquilinear correlation $\mathcal{G}_C(K, J)$ yields $\lambda_C(\rho, \sigma) = z_\rho + \bar{z}_\sigma$, selecting $\sigma = 1 - \bar{\rho}$ (`REFLECTION_PAIR_STATIONARY_FOR_SESQUILINEAR_CORRELATION`). On the stationary reflection pair $\sigma = 1 - \bar{\rho}$ ($\bar{z}_\sigma = -z_\rho$), the relative-grade exponent is $\mu_C(\rho, 1 - \bar{\rho}) = \bar{z}_\sigma - z_\rho = -2z_\rho = -2\delta_\rho - 2i\gamma_\rho$ (`sesquilinear_relative_exponent_at_reflection`, `RELATIVE_GRADE_REFLECTION_EXPONENT_REPAIRED`).

---

### G. Reflection-pair stationarity theorem

**Theorem (`reflection_stationary_iff` in Lean 4)**: For any two zeros $\rho = \frac{1}{2} + \delta_\rho + i\gamma_\rho$ and $\sigma = \frac{1}{2} + \delta_\sigma + i\gamma_\sigma$,

$$z_\rho + \bar{z}_\sigma = 0 \iff \bigl(\delta_\rho + \delta_\sigma = 0 \;\land\; \gamma_\rho = \gamma_\sigma\bigr) \iff \sigma = 1 - \bar{\rho}.$$

Moreover:
1. On the critical line ($\delta_\rho = 0$), $\rho = 1 - \bar{\rho}$ (the stationary relation is a diagonal self-reflection term of multiplicity weight $m_\rho^2$).
2. Off the critical line ($\delta_\rho \neq 0$), $\rho \neq 1 - \bar{\rho}$ (the stationary relation pairs two distinct off-critical zeros $(\rho, 1 - \bar{\rho})$ at the same height $\gamma_\rho$, and by functional-equation + Schwarz symmetry of $\xi(s)$, $m_{1 - \bar{\rho}} = m_\rho$, giving stationary block weight $m_\rho^2$).

---

### H. Inversion-even real state vs. Fourier self-duality (repaired in `TASK-TC-037R`)

For multiplicative inversion $(\mathcal{I}\Psi)(u) = u^{-1}\Psi(u^{-1})$ in half-density coordinates on $(\mathbb{R}_+, du/u)$, $\widehat{\mathcal{I}\Psi}(z) = \widehat{\Psi}(-z)$. Defining the real inversion-even state

$$\Psi_t^+ = \frac{1}{2}\left(\Phi_t^{(2)} + \mathcal{I}\Phi_t^{(2)}\right), \qquad \widehat{\Psi}_t^+(z) = \frac{1}{2}\left(\widehat{\Phi}_t^{(2)}(z) + \widehat{\Phi}_t^{(2)}(-z)\right),$$

its centered Mellin transform satisfies $\widehat{\Psi}_t^+(-z) = \widehat{\Psi}_t^+(z)$ (`symmetrized_psi_plus_inversion_even = True`) and, because $\Psi_t^+$ is real-valued on $(0, \infty)$, $\widehat{\Psi}_t^+(\bar{z}) = \overline{\widehat{\Psi}_t^+(z)}$. Consequently, on every reflection pair $(z, -\bar{z})$ (`inversion_even_mellin_symmetry_algebra` in Lean 4):

$$\widehat{\Psi}_t^+(z)\,\widehat{\Psi}_t^+(-\bar{z}) = \widehat{\Psi}_t^+(z)\,\overline{\widehat{\Psi}_t^+(z)} = \left|\widehat{\Psi}_t^+(z)\right|^2 \ge 0.$$

**Distinction between raw $\Phi_t^{(2)}$ and symmetrized $\Psi_t^+$ (`FOURIER_SELF_DUALITY_DISTINCT_FROM_MULTIPLICATIVE_INVERSION_EVENNESS`)**:
1. **Raw state $\Phi_t^{(2)}$**: Its centered Mellin transform is
   $$\widehat{\Phi}_t^{(2)}(z) = \frac{1}{32}\left(z^2 - \frac{1}{4}\right)^2 t^{-z/2}\pi^{-(1/2+z)/2}\Gamma\!\left(\frac{1/2+z}{2}\right),$$
   which is provably nonzero everywhere in the open critical strip $-\frac{1}{2} < \operatorname{Re}(z) < \frac{1}{2}$ ($0 < \operatorname{Re}(s) < 1$) because $\Gamma(s/2)$ has no zeros in $\mathbb{C}$ and $(z^2 - 1/4)^2$ vanishes only at $z = \pm 1/2$. However, even at $t = 1$, $\widetilde{g}_1(u) = e^{-\pi u^2}$ is self-dual under the **additive Fourier transform** $\mathcal{F}\widetilde{g}_1 = \widetilde{g}_1$, **not** invariant under multiplicative inversion $(\mathcal{I}\Psi)(u) = u^{-1}\Psi(u^{-1})$, because $\pi^{-(1/2+z)/2}\Gamma((1/2+z)/2) \neq \pi^{-(1/2-z)/2}\Gamma((1/2-z)/2)$ (`raw_phi_t1_inversion_even = False`).
2. **Symmetrized state $\Psi_t^+$**: On the critical line $z = i\gamma$ at $t = 1$, $\widehat{\Psi}_1^+(i\gamma) = \operatorname{Re}\widehat{\Phi}_1^{(2)}(i\gamma)$ oscillates through zero whenever $\arg\Gamma(\frac{1/2+i\gamma}{2}) - \frac{\gamma}{2}\log\pi \in \frac{\pi}{2} + \pi\mathbb{Z}$ (certified in 128-bit Arb between $\gamma_a = 0.25$ where $\widehat{\Psi}_1^+(0.25i) \approx +0.005930018171819737 > 0$ and $\gamma_b = 1.0$ where $\widehat{\Psi}_1^+(1.0i) \approx -0.01007544310514176 < 0$). Hence $\widehat{\Psi}_t^+(z)$ is **not** zero-free in the critical strip (`INVERSION_EVEN_MELLIN_ZERO_FREE_STRIP_FALSE`), while nonvanishing $\widehat{\Psi}_t^+(z_\rho) \neq 0$ at hypothetical off-critical zeta zeros remains open (`STRICT_REFLECTION_WEIGHT_AT_ZETA_ZERO_ORDINATES_OPEN`), so $W_\rho(t) = m_\rho^2|\widehat{\Psi}_t^+(z_\rho)|^2 \ge 0$ is proved (`REFLECTION_WEIGHT_NONNEGATIVE_PROVED`) while strict positivity $W_\rho(t) > 0$ is not yet proved (`REFLECTION_WEIGHT_STRICT_POSITIVITY_NOT_YET_PROVED`).

---

### I. Reflection-quartet radial identity vs. relative-grade differentiation (repaired in `TASK-TC-037R`)

Evaluating the fixed-grade quadratic curvature polynomial $P(z_\rho, z_\sigma) = (z_\rho - z_\sigma)^2 + 2(z_\rho + z_\sigma)$ from `TASK-TC-036` on the $R$-stationary reflection pair $z_\sigma = -\bar{z}_\rho = -\delta_\rho + i\gamma_\rho$ (where $z_\rho - z_\sigma = 2\delta_\rho$ and $z_\rho + z_\sigma = 2i\gamma_\rho$) gives

$$P(z_\rho, -\bar{z}_\rho) = (2\delta_\rho)^2 + 2(2i\gamma_\rho) = 4\delta_\rho^2 + 4i\gamma_\rho.$$

On the Schwarz-conjugate reflection pair $(\bar{\rho}, 1 - \rho)$ where $z_{\bar{\rho}} = \delta_\rho - i\gamma_\rho$ and $-\bar{z}_{\bar{\rho}} = -\delta_\rho - i\gamma_\rho$,

$$P(z_{\bar{\rho}}, -\bar{z}_{\bar{\rho}}) = 4\delta_\rho^2 - 4i\gamma_\rho.$$

Summing the two conjugate reflection pairs cancels the imaginary ordinate drift $\pm 4i\gamma_\rho$ identically (`reflection_quartet_imaginary_cancellation` in Lean 4, `REFLECTION_QUARTET_RADIAL_IDENTITY_PRESERVED`):

$$P_\rho + P_{\bar{\rho}} = 8\delta_\rho^2.$$

With the real inversion-even state $\Psi_t^+$, the formal stationary-sector quartet contribution is nonnegative (`reflection_quartet_radial_defect_nonneg`, `reflection_weight_nonnegative` in Lean 4):

$$8 m_\rho^2 \left|\widehat{\Psi}_t^+(z_\rho)\right|^2 \delta_\rho^2 \ge 0.$$

**Crucial distinction from relative-grade differentiation (`RELATIVE_GRADE_DIFFERENTIATION_NOT_PURE_RADIAL`)**:
In the sesquilinear correlation $\mathcal{G}_C(r - d, r + d)$, the factor on the reflection pair $\sigma = 1 - \bar{\rho}$ is $\tau^{-2d z_\rho}$, whose second derivative at $d = 0$ is $4(\log\tau)^2 z_\rho^2$ and whose conjugate-quartet sum is $8(\log\tau)^2(\delta_\rho^2 - \gamma_\rho^2)$ (`relative_grade_second_derivative_not_radial` in Lean 4), NOT $8(\log\tau)^2\delta_\rho^2$. The pure radial factor $8\delta_\rho^2$ comes from the fixed-grade scale operator $\mathcal{L}_{\mathrm{TC}} = 4\mathcal{D}^2 + 2\mathcal{D}$, not from $\partial_d^2|_{d=0}$.

---

### J. Finite Laurent projector no-go (repaired in `TASK-TC-037R`)

Consider any zero-independent finite discrete-grade filter

$$\Pi_N[f] = \sum_{K=-N}^{N} c_K f(K), \qquad P_N(q) = \sum_{K=-N}^{N} c_K q^K, \qquad c_K \in \mathbb{C}.$$

An exact reflection projector requires $P_N(1) \neq 0$ while $P_N(q_{\rho,\sigma}) = 0$ for every nonstationary pair character $q_{\rho,\sigma} = \tau^{z_\rho + \bar{z}_\sigma} \neq 1$.

**Repaired Distinct-Character Theorem (`DISTINCT_PAIR_CHARACTERS_PROVED_USING_DISTINCT_ZERO_DENSITY`)**: Fix one nontrivial zero $\rho_0$. Then $\{q_{\rho_0,\sigma} = \tau^{z_{\rho_0} + \bar{z}_\sigma} : \zeta(\sigma) = 0, \sigma \neq 1 - \bar{\rho}_0\}$ assumes infinitely many distinct complex values in $\mathbb{C}^\times$:
1. Distinguish $N(T) = \sum_{0 < \gamma_\sigma < T} m_\sigma$ (counted **with** multiplicity) from $N_{\mathrm{dist}}(T) = \#\{\sigma : 0 < \operatorname{Im}\sigma < T, \zeta(\sigma) = 0\}$ (counted **without** multiplicity).
2. Suppose $q_{\rho_0,\sigma}$ took only finitely many complex values $\{w_1, \dots, w_M\} \subset \mathbb{C}^\times$.
3. Since $e^{w \log\tau} = e^{w' \log\tau} \iff w - w' \in \frac{2\pi i}{\log\tau}\mathbb{Z}$, each $w_j$ restricts $\operatorname{Re}(\sigma)$ to a single value and $\gamma_\sigma = \operatorname{Im}(\sigma)$ to a single vertical arithmetic progression with spacing $\frac{2\pi}{\log\tau} \approx 3.4187$.
4. A finite union of $M$ vertical progressions with spacing $\frac{2\pi}{\log\tau}$ contains at most $M\bigl(\frac{\log\tau}{2\pi}T + O(1)\bigr) = O_M(T)$ **distinct** zeros $\sigma$ up to height $T$.
5. By the unconditional simple critical-line zero density theorem of **Bui, Conrey, and Young (2011, *Acta Arith.* 150, 35–64, Theorem 1.1 & Section 2.2, `arXiv:1002.4127v2`; cf. Conrey 1989; Levinson 1974 / Heath-Brown 1979)**, simple critical-line zeros satisfy $N_0^*(T) \ge (0.4058 - o(1))N(T)$. Because simple zeros have multiplicity $1$,
   $$N_{\mathrm{dist}}(T) \ge N_0^*(T) \ge (0.4058 - o(1))\frac{T}{2\pi}\log\frac{T}{2\pi e} \gg T\log T,$$
   contradicting $O_M(T)$ as $T \to \infty$.

Since $Q_{2N}(q) = q^N P_N(q) \in \mathbb{C}[q]$ is a complex polynomial of degree $\le 2N$ vanishing on infinitely many distinct nonzero complex points $q_{\rho_0,\sigma}$, it vanishes identically (`finite_complex_polynomial_projector_root_no_go` in Lean 4), forcing $P_N(1) = 0$.  
**Classifications**: `FINITE_GRADE_LAURENT_PROJECTOR_NO_GO`, `FINITE_COMPLEX_GRADE_PROJECTOR_NO_GO_FORMALIZED`.

---

### K. Finite differential projector no-go (repaired in `TASK-TC-037R`)

A finite-order common-grade differential operator $p(\partial_r) = \sum_{m=0}^M a_m \partial_r^m$ ($a_m \in \mathbb{C}$) acts on $\tau^{r\lambda}$ by $p((\log\tau)\lambda)\tau^{r\lambda}$. Unlike $q_{\rho_0,\sigma} = e^{(\log\tau)\lambda_{\rho_0,\sigma}}$, the map $\sigma \mapsto \lambda_{\rho_0,\sigma} = z_{\rho_0} + \bar{z}_\sigma$ is injective on distinct complex zeros $\sigma$ without any vertical-progression quotient. Since $\zeta(s)$ has infinitely many distinct zeros (Hardy 1914; Titchmarsh 1986, Theorem 10.1; and quantitatively $N_{\mathrm{dist}}(T) \ge N_0^*(T) \gg T\log T$), there are infinitely many distinct nonzero complex pair exponents $(\log\tau)\lambda_{\rho_0,\sigma} \in \mathbb{C}$. Any polynomial $p \in \mathbb{C}[X]$ of degree $\le M$ vanishing on $> M$ distinct complex exponents satisfies $p \equiv 0$, forcing $p(0) = 0$ (`finite_complex_differential_projector_root_no_go` in Lean 4). The same holds for any rational filter $R(\lambda) = p(\lambda)/q(\lambda)$ analytic at $\lambda = 0$.  
**Classifications**: `FINITE_ORDER_GRADE_DIFFERENTIAL_PROJECTOR_NO_GO`, `FINITE_COMPLEX_GRADE_PROJECTOR_NO_GO_FORMALIZED`.

---

### L. Discrete Følner / Cesàro audit

Because $(\mathbb{Z}, +)$ is noncompact, its counting Haar measure is infinite; character projection uses the bilateral Følner / Cesàro average

$$A_N(q) = \frac{1}{2N+1}\sum_{K=-N}^{N} q^K,$$

which satisfies (`cesaro_unit_character_limit_control` in Lean 4):
- **Stationary character ($q = 1$)**: $A_N(1) = 1$ for all $N \ge 0$.
- **Unitary nonstationary character ($|q| = 1, q \neq 1$)**: $|A_N(q)| = \frac{|q^{2N+1} - 1|}{(2N+1)|q - 1|} \le \frac{2}{(2N+1)|q - 1|} \to 0$ as $N \to \infty$.
- **Nonunitary character ($|q| \neq 1$)**: By bilateral symmetry $q^N + q^{-N} - 2 = \frac{(q^N - 1)^2}{q^N} > 0$ (for $q > 0, q \neq 1$), either the positive-grade ray ($|q| > 1$) or the negative-grade ray ($0 < |q| < 1$) grows exponentially as $\frac{\max(|q|, |q|^{-1})^N}{2N+1} \to +\infty$.

---

### M. Continuous Følner / Cesàro audit

Because $(\mathbb{R}, +)$ is noncompact, its Lebesgue Haar measure is infinite; character projection uses the continuous Følner / Cesàro average over $r \in [-T, T]$:

$$C_T(\lambda) = \frac{1}{2T}\int_{-T}^{T} e^{r\lambda}\,dr = \frac{\sinh(T\lambda)}{T\lambda}.$$

- If $\lambda = 0$: $C_T(0) = 1$.
- If $\lambda = i\omega \neq 0$ ($\omega \in \mathbb{R} \setminus \{0\}$): $C_T(i\omega) = \frac{\sin(T\omega)}{T\omega} \to 0$ as $T \to \infty$.
- If $\operatorname{Re}(\lambda) \neq 0$: $|C_T(\lambda)| \sim \frac{e^{T|\operatorname{Re}\lambda|}}{2T|\lambda|} \to +\infty$ exponentially as $T \to \infty$.

**Classifications**: `OFF_CRITICAL_NONUNITARITY_BLOCKS_FOLNER_CHARACTER_PROJECTION`, `CONTINUOUS_GRADE_HAAR_PROJECTION_REQUIRES_UNITARY_CHARACTERS`.

---

### N. Abel and Gaussian controls

1. **Abel / Poisson grade weighting** ($0 < r < 1$):
   $$A_r(q) = \frac{1 - r}{1 + r}\sum_{K \in \mathbb{Z}} r^{|K|} q^K = \frac{(1 - r)^2}{(1 - rq)(1 - r/q)}, \qquad r < |q| < \frac{1}{r}.$$
   The bilateral geometric series converges **if and only if** $r < |q| < 1/r$. As $r \uparrow 1$, the convergence annulus $(r, 1/r)$ collapses to the unit circle $|q| = 1$. Every nonunitary character $|q| \neq 1$ exits the convergence annulus once $r \ge \min(|q|, |q|^{-1}) < 1$ and diverges.
2. **Gaussian grade weighting**:
   $$G_T(\lambda) = \frac{\int_{\mathbb{R}} e^{-r^2/(2T^2)} e^{r\lambda}\,dr}{\int_{\mathbb{R}} e^{-r^2/(2T^2)}\,dr} = e^{T^2 \lambda^2 / 2}.$$
   For $\lambda = \alpha + i\omega$, $|G_T(\lambda)| = \exp\bigl(\frac{1}{2}T^2(\alpha^2 - \omega^2)\bigr)$. On any purely real nonunitary exponent $\lambda = \alpha \neq 0$ ($\omega = 0$), $G_T(\alpha) = e^{T^2\alpha^2/2} \to +\infty$ super-exponentially as $T \to \infty$.

---

### O. Off-critical nonunitarity obstruction

Consider the **same-index diagonal pair** $\sigma = \rho$ in the double spectral sum. Its common-shift exponent and character are (`offcritical_diagonal_character_nonunitary` in Lean 4):

$$\lambda_{\rho,\rho} = z_\rho + \bar{z}_\rho = 2\delta_\rho, \qquad q_{\rho,\rho} = \tau^{2\delta_\rho}.$$

Whenever an off-critical zero exists ($\delta_\rho \neq 0$):
1. $\lambda_{\rho,\rho} = 2\delta_\rho \neq 0$ is purely real and nonstationary;
2. $|q_{\rho,\rho}| = \tau^{2\delta_\rho} \neq 1$ is strictly nonunitary;
3. For the raw repaired state $\Phi_t^{(2)}$, the diagonal Mellin weight $|\widehat{\Phi}_t^{(2)}(z_\rho)|^2$ is strictly positive throughout the open critical strip $0 < \operatorname{Re}(\rho) < 1$ because $\Gamma(\rho/2)$ has no zeros and $\frac{1}{16}\rho^2(\rho - 1)^2$ vanishes only at $\rho \in \{0, 1\}$.
4. Consequently, discrete Følner/Cesàro $A_N(q_{\rho,\rho})$, continuous Følner/Cesàro $C_T(2\delta_\rho\log\tau)$, Abel $A_r(q_{\rho,\rho})$, and Gaussian $G_T(2\delta_\rho\log\tau)$ all diverge whenever $\delta_\rho \neq 0$.

Furthermore, rotating the grade contour to $K = v e^{i\theta}$ cannot unitarize the spectrum for any fixed zero-independent angle $\theta$: off-diagonal critical pairs ($\operatorname{Re}\lambda = 0, \operatorname{Im}\lambda \neq 0$) require $\sin\theta = 0$ for bilateral boundedness, whereas off-critical diagonal pairs ($\operatorname{Re}\lambda = 2\delta_\rho \neq 0, \operatorname{Im}\lambda = 0$) require $\cos\theta = 0$. Since $\sin^2\theta + \cos^2\theta = 1$, no fixed $\theta$ makes both bounded.  
**Classifications**: `OFF_CRITICAL_NONUNITARITY_BLOCKS_FOLNER_CHARACTER_PROJECTION`, `OFF_CRITICAL_NONUNITARITY_BLOCKS_GRADE_HAAR_PROJECTION`.

---

### P. Cross-grade arithmetic-zero compatibility

To obtain an arithmetic contradiction, the spectral projection would need to act on a family possessing an exact nonpositive or vanishing arithmetic law, such as the cross-grade overlap $Q_\varepsilon^{K, J}[w]$ at $(K, J) = (0, 1)$, where narrow support ($\varepsilon < \frac{1}{2}\Delta_{\min}(15, 1)$ with $\Delta_{\min}(15, 1) = 19 - 6\pi > 0$) gives $Q_\varepsilon^{0, 1}[w] = 0$. Under a common grade shift $(0, 1) \mapsto (r, 1 + r)$ with the tested power-scaled homogeneous two-variable transport ansatz

$$F_r(x, y) = \tau^{ar} F_0(\tau^{-br} x, \tau^{-br} y),$$

evaluating at the shifted prime-power stations $x_r(n) = \tau^r n$ and $y_{1+r}(m) = \tau^{1+r} m$ yields

$$F_r(\tau^r n, \tau^{1+r} m) = \tau^{ar} F_0\!\left(\tau^{(1-b)r} n, \,\tau^{(1-b)r} (\tau m)\right).$$

Preserving the unshifted station labels $(n, \tau m)$ and the uniform support-separation proof across all common shifts $r$ within this ansatz uniquely forces

$$1 - b = 0 \iff b = 1.$$

---

### Q. Transport–projection incompatibility within tested ansatz

Under the tested transported kernel $F_r(x, y) = \tau^{ar} F_0(\tau^{-br} x, \tau^{-br} y)$, the two-variable Mellin transform acquires the scaling factor $\tau^{r(a + b(s + t))}$, while the explicit-formula zero stations at grades $(r, 1 + r)$ contribute $\tau^{-r(s + t)}$. The net common-shift spectral exponent is (`transport_projection_incompatibility_algebra` in Lean 4):

$$r\bigl(a + b(s + t)\bigr) - r(s + t) = ar + (b - 1)r(s + t).$$

At the unique arithmetic station-preserving parameter $b = 1$:

$$(1 - 1)r(s + t) = 0,$$

so the zero-dependent common-shift spectral character is **erased identically** for every pair of zeros! Conversely, if $b \neq 1$ (for instance $b = 0$), the spectral common-shift character survives, but the dilated stations $\tau^{(1-b)r} n$ sweep across the fixed support of $F_0$ as $r$ varies, destroying the cross-grade arithmetic vanishing law.  
**Classifications**: `COMMON_SHIFT_PROJECTION_TRANSPORT_INCOMPATIBILITY`, `GRADE_CHARACTER_PROJECTION_INCOMPATIBLE_WITH_TESTED_TRANSPORT_ANSATZ`.

---

### R. Ratio-kernel control

For any common-scale-invariant ratio kernel

$$F(x, y) = \varphi(x / y) = \widetilde{\varphi}(\log x - \log y),$$

common scaling satisfies $F(\tau^r x, \tau^r y) = F(x, y)$ automatically. However, in two-variable Mellin coordinates ($u = x/y, v = y$),

$$\int_0^\infty \int_0^\infty \varphi(x/y) x^s y^t \frac{dx}{x}\frac{dy}{y} = \left(\int_0^\infty \varphi(u) u^s \frac{du}{u}\right)\left(\int_0^\infty v^{s + t} \frac{dv}{v}\right) = 2\pi \widehat{\varphi}(s)\,\delta\bigl(\operatorname{Im}(s + t)\bigr)$$

is distributionally supported on the locus $s + t = 0$. On $s + t = 0$, the common-shift exponent $r(s + t) = 0$ vanishes identically (`transport_projection_incompatibility_algebra` in Lean 4).  
**Classification**: `SCALE_INVARIANT_ARITHMETIC_KERNEL_ERASES_COMMON_GRADE_CHARACTER`.

---

### S. Relative-grade fallback

When common-shift projection is blocked, the single permitted fallback is the relative grade $d = (J - K)/2$ (or $J - K = 2d$).
1. **Spectral non-radiality on the sesquilinear correlation**: As proved in `sesquilinear_relative_exponent_at_reflection` and `relative_grade_second_derivative_not_radial`, on the reflection pair $\sigma = 1 - \bar\rho$ the sesquilinear factor is $\tau^{-2d z_\rho}$, so differentiating twice with respect to $d$ at $d = 0$ produces the quartet sum $8(\log\tau)^2(\delta_\rho^2 - \gamma_\rho^2) < 0$ rather than a positive radial term $8(\log\tau)^2\delta_\rho^2$ (`RELATIVE_GRADE_DIFFERENTIATION_NOT_PURE_RADIAL`).
2. **Diophantine gap shrinking on the prime spectrum**: Although $\tau^K \mathbb{Z} \cap \tau^J \mathbb{Z} = \{0\}$ holds pointwise for $K \neq J$ by Lindemann's transcendence theorem for $\tau = 2\pi$, $\min_{2 \le n, m \le M} |\log(n/m) - d\log\tau|$ shrinks toward $0$ as the station cutoff $M \to \infty$ (from $0.00807$ at $M = 15$ to $0.000188$ at $M = 200$ for $d = 1$), so no fixed positive bandwidth $\varepsilon > 0$ avoids cross-grade collisions on the full prime spectrum.

---

### T. Arithmetic contradiction gate

Comparing the arithmetic and spectral signs across both candidate families (`projected_arithmetic_zero_and_positive_radial_contradiction` in Lean 4):
1. For the untwisted sesquilinear correlation $\mathcal{G}_C(r, r) = |W_{\mathrm{comp}}(U_{-r}\Psi_t^+)|^2 \ge 0$, both the arithmetic side and the formal stationary-sector spectral sum $\sum_{\rho/\sim} 8 m_\rho^2 |\widehat{\Psi}_t^+(z_\rho)|^2 \delta_\rho^2 \ge 0$ are nonnegative; having $\ge 0$ on both sides yields **no contradiction** (`REFLECTION_PROJECTION_HAS_NO_ARITHMETIC_SIGN_CONTRADICTION`).
2. For the cross-grade narrow-support functional $Q_\varepsilon^{r, 1+r}[F_r]$ within the tested transport ansatz, preserving $Q_\varepsilon = 0$ requires $b = 1$, which erases the common-shift spectral character identically.
3. Under the Section 26 firewall, any filter whose coefficients depend on $\rho, \gamma_\rho, \delta_\rho$, a numerical zero list, $q_{\rho,\sigma}$, or a Weierstrass product over the zero spectrum is rejected (`ZERO_DEPENDENT_GRADE_FILTER_REJECTED`).

---

### U. Weil-equivalence firewall

The additive grade group $(\mathbb{R}, +)$ (or $(\mathbb{Z}, +)$) has unitary Pontryagin dual characters $e^{i r \omega}$ ($\omega \in \mathbb{R}$). A TC grade character $e^{r\lambda}$ is bounded on $\mathbb{R}$ if and only if $\operatorname{Re}(\lambda) = 0$.
- For a **single-zero character** $\chi_{z_\rho}(K) = \tau^{K z_\rho}$, unitarity holds iff $\delta_\rho = 0$ (which is RH for $\rho$).
- For the **sesquilinear pair character** $\tau^{r(z_\rho + \bar{z}_\sigma)}$, unitarity for all pairs—and specifically for the diagonal pair $\sigma = \rho$ where $z_\rho + \bar{z}_\rho = 2\delta_\rho$—holds iff every $\delta_\rho = 0$.

Therefore, invoking Pontryagin character orthogonality or an invariant mean on $\mathbb{Z}$ or $\mathbb{R}$ to annihilate nonstationary grade characters implicitly assumes $\delta_\rho = 0$:  
**Classification**: `GRADE_ORTHOGONALITY_OUTSIDE_UNITARY_AXIS_IS_DISGUISED_RH_PREMISE`.

---

### V. Principal classification

Following the repaired `TASK-TC-037` / `TASK-TC-037R` evidence:

$$\boxed{\texttt{GRADE\_CHARACTER\_PROJECTION\_DOES\_NOT\_ESCAPE\_TRANSPORT\_MOMENT\_INCOMPATIBILITY}}$$

with scoped transport and Følner/Cesàro classifications:

$$\boxed{\texttt{GRADE\_CHARACTER\_PROJECTION\_INCOMPATIBLE\_WITH\_TESTED\_TRANSPORT\_ANSATZ}}$$

$$\boxed{\texttt{OFF\_CRITICAL\_NONUNITARITY\_BLOCKS\_FOLNER\_CHARACTER\_PROJECTION}}$$

and obligation status:

$$\boxed{\texttt{OBL-CT-001A} = \texttt{OPEN}.}$$

Specifically, the three routes for grade-character reflection projection are closed by exact theorems:
1. **Projection failure (untransported $b = 0$)**: Finite complex Laurent and differential filters are ruled out over $\mathbb{C}[X]$ using the unconditional simple-zero density bound $N_{\mathrm{dist}}(T) \ge N_0^*(T) \ge (0.4058 - o(1))N(T) \gg T\log T$ (`DISTINCT_PAIR_CHARACTERS_PROVED_USING_DISTINCT_ZERO_DENSITY`, `FINITE_COMPLEX_GRADE_PROJECTOR_NO_GO_FORMALIZED`), and infinite Følner/Cesàro, Abel, and Gaussian grade averages diverge on off-critical diagonal terms $q_{\rho,\rho} = \tau^{2\delta_\rho} \neq 1$ (`OFF_CRITICAL_NONUNITARITY_BLOCKS_FOLNER_CHARACTER_PROJECTION`).
2. **Transport incompatibility within tested ansatz ($b = 1$)**: Preserving the cross-grade arithmetic vanishing law $Q_\varepsilon^{r, 1+r}[F_r] = 0$ under $F_r(x, y) = \tau^{ar}F_0(\tau^{-br}x, \tau^{-br}y)$ forces $b = 1$ (or scale-invariant ratio kernels $\varphi(x/y)$), which identically cancels $(b - 1)r(s + t) = 0$ (`GRADE_CHARACTER_PROJECTION_INCOMPATIBLE_WITH_TESTED_TRANSPORT_ANSATZ`).
3. **Absence of an arithmetic sign contradiction**: On the sesquilinear correlation $\mathcal{G}_C(r, r) = |W_{\mathrm{comp}}(U_{-r}\Psi_t^+)|^2 \ge 0$, both the arithmetic value and the formal stationary-sector radial sum are nonnegative (`REFLECTION_PROJECTION_HAS_NO_ARITHMETIC_SIGN_CONTRADICTION`), while relative-grade second differentiation on $\mathcal{G}_C(r-d, r+d)$ yields $8(\log\tau)^2(\delta_\rho^2 - \gamma_\rho^2)$ rather than a pure radial term (`RELATIVE_GRADE_DIFFERENTIATION_NOT_PURE_RADIAL`).

---

### W. Exact next theorem (`SUBGATE-TC-037A`)

Under `OBL-CT-001A`, the single remaining theorem target (`SUBGATE-TC-037A`, refining `SUBGATE-TC-036A`) is:

> **Subgate `SUBGATE-TC-037A`**: Determine whether there exists a zero-independent two-grade or multi-grade explicit-formula construction that:
> 1. is **not** of the power-scaled common-transport form $F_r(x,y) = \tau^{ar}F_0(\tau^{-r}x,\tau^{-r}y)$;
> 2. does **not** require Følner/Cesàro character averaging over nonunitary off-critical modes $\tau^{2r\delta_\rho}$;
> 3. has an explicit arithmetic identity with nonpositive value $\le 0$; and
> 4. has a complete spectral identity whose reflection-sector weight is provably strictly positive for $\delta_\rho \neq 0$ while its non-reflection complement is provably nonnegative $\ge 0$.

---

### Compact Evidence Table (Repaired in `TASK-TC-037R`)

| Result | Internal derivation | External theorem | Evidence class |
|---|---|---|---|
| Klein-four zero symmetries $V_4 = \{I, C, F, R\}$ and $R^2 = I$ | `centered_zero_reflection_identity` (`GradeCharacterProjection.lean`) | Functional equation $\xi(s) = \xi(1-s)$ & Schwarz reflection (Riemann 1859; Titchmarsh 1986) | `LEAN_PROVED` (algebraic coordinate identities) |
| Reflection-pair stationarity $z_\rho + \bar{z}_\sigma = 0 \iff \sigma = 1 - \bar{\rho}$ | `reflection_stationary_iff` (`GradeCharacterProjection.lean`) | Multiplicity symmetry $m_{1-\bar{\rho}} = m_\rho$ of $\xi(s)$ | `LEAN_PROVED` (iff & self-reflection) |
| Pair character modulus $\tau^{r\delta_1}\tau^{r\delta_2} = \tau^{r(\delta_1+\delta_2)}$ and off-critical diagonal $q_{\rho,\rho} = \tau^{2\delta_\rho} \neq 1$ | `grade_pair_character_modulus`, `offcritical_diagonal_character_nonunitary` (`GradeCharacterProjection.lean`) | Mellin dilation transform law (Titchmarsh 1948) | `LEAN_PROVED` (real power modulus & nonunitarity) |
| Infinitely many distinct complex pair characters $q_{\rho_0,\sigma} = \tau^{z_{\rho_0} + \bar{z}_\sigma}$ for fixed $\rho_0$ | Vertical progression bound $O_M(T)$ vs $N_{\mathrm{dist}}(T) \ge N_0^*(T) \gg T\log T$ (`verify_distinct_zero_density_justification`) | Bui, Conrey & Young (2011), *Acta Arith.* 150, 35–64, Thm 1.1 (`arXiv:1002.4127v2`, $\kappa^* \ge 0.4058$); Conrey (1989); Levinson (1974) / Heath-Brown (1979); von Mangoldt (1905) | `PROVED_PAPER_DERIVATION` from unconditional simple-zero density theorem |
| Finite Laurent & differential projector root no-go over $\mathbb{R}[X]$ and $\mathbb{C}[X]$ ($P \equiv 0$, $p \equiv 0$) | `finite_polynomial_projector_root_no_go`, `finite_differential_projector_root_no_go`, `finite_complex_polynomial_projector_root_no_go`, `finite_complex_differential_projector_root_no_go` (`GradeCharacterProjection.lean`) | Polynomial root bound over integral domains (`Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero` over $\mathbb{R}$ and $\mathbb{C}$) | `LEAN_PROVED` (root-count no-go over $\mathbb{R}$ and $\mathbb{C}$) + paper derivation (via $N_0^*(T)$) |
| Corrected sesquilinear relative-grade exponent $(r-d)z_\rho + (r+d)\bar z_\sigma = -2d z_\rho$ and non-radial second derivative $8(\log\tau)^2(\delta_\rho^2 - \gamma_\rho^2)$ | `sesquilinear_relative_exponent_at_reflection`, `relative_grade_second_derivative_not_radial` (`GradeCharacterProjection.lean`) & `verify_relative_grade_reflection_algebra` | None (exact complex coordinate algebra + 128-bit Arb check) | `LEAN_PROVED` + `CERTIFIED_FINITE` |
| Discrete/continuous Følner–Cesàro, Abel, and Gaussian divergence on nonunitary diagonal $q_{\rho,\rho} = \tau^{2\delta_\rho}$ | `cesaro_unit_character_limit_control` (`GradeCharacterProjection.lean`) & `audit_offcritical_diagonal_obstruction` | Harmonic analysis / Følner–Cesàro & Abel summability on $\mathbb{Z}, \mathbb{R}$ (Rudin 1962; Katznelson 2004; Folland 2016); nonvanishing of $\Gamma(s/2)$ | `LEAN_PROVED` (bilateral excess) + `PROVED_PAPER_DERIVATION` |
| Curvature-polynomial quartet identity $P_\rho + P_{\bar{\rho}} = 8\delta_\rho^2$, inversion-even symmetrization $\widehat{\Psi}_t^+(z)$, and nonnegativity $8 m_\rho^2 |\widehat{\Psi}_t^+(z_\rho)|^2 \delta_\rho^2 \ge 0$ | `reflection_quartet_imaginary_cancellation`, `reflection_quartet_radial_defect_nonneg`, `inversion_even_mellin_symmetry_algebra`, `reflection_weight_nonnegative` (`GradeCharacterProjection.lean`) & `verify_fourier_vs_multiplicative_inversion` | Weil explicit formula & Burnol conductor formalism (Weil 1952; Burnol `arXiv:math/9902080v1`, `arXiv:math/0101068v1`) | `LEAN_PROVED` (algebra & nonnegativity) + `CERTIFIED_FINITE` (critical-line sign change of $\widehat{\Psi}_1^+$) |
| Transport–projection incompatibility $(b - 1)r(s + t) = 0$ at $b = 1$ within tested ansatz and ratio-kernel erasure on $s + t = 0$ | `transport_projection_incompatibility_algebra` (`GradeCharacterProjection.lean`) & `audit_common_shift_transport_compatibility` | Two-variable Mellin convolution/scaling law | `LEAN_PROVED` (exponent cancellation algebra) |
| Conditional contradiction vs same-sign consistency firewall | `projected_arithmetic_zero_and_positive_radial_contradiction` (`GradeCharacterProjection.lean`) | None (pure first-order real arithmetic) | `LEAN_PROVED` |

