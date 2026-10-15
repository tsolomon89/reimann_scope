# TASK-TC-037 Review: Bigraded Character Projection, Reflection-Sector Isolation, and Transport-Compatibility Audit

**Task ID**: `TASK-TC-037`  
**Starting HEAD**: `02dce7dd62492605e88f72c05c9efb67a900f84e`  
**Substantive Parent (`TASK-TC-036R`)**: `fc549855377581ca325782831caef2cb75b0e20d`  
**Principal Classification**: `GRADE_CHARACTER_PROJECTION_DOES_NOT_ESCAPE_TRANSPORT_MOMENT_INCOMPATIBILITY`  
**Secondary Classification**: `OFF_CRITICAL_NONUNITARITY_BLOCKS_GRADE_HAAR_PROJECTION`  
**Obligation Status**: `OBL-CT-001A = OPEN` (`SUBGATE-TC-037A = OPEN`)  
**Formal Assurance**: 0 `sorry`, 0 `admit`, no nonstandard project axioms introduced (`formal/RiemannScope/GradeCharacterProjection.lean`).

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

In the unrestricted double zero sum over $(\rho, \sigma)$, the radial displacement $\delta_\rho = \operatorname{Re}(\rho) - \frac{1}{2}$ appears cleanly inside the same-height functional-equation reflection pair $\sigma = 1 - \bar{\rho}$, where $z_\rho - z_\sigma = 2\delta_\rho$. Rather than searching for another privileged single test kernel (`TASK-TC-035`) or another heat/conductor differential commutator (`TASK-TC-036`), `TASK-TC-037` tests whether the **TC grade variable itself** can act as a zero-independent spectral selector that isolates the reflection sector $\sigma = 1 - \bar{\rho}$ as the stationary character of a bigraded common-shift action while preserving an incompatible arithmetic law.

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

| Second-leg structure $\mathcal{S}$ | Pair exponent $\lambda_{\mathcal{S}}(\rho, \sigma)$ | Stationary condition $\lambda_{\mathcal{S}} = 0$ | Selected zero relation |
|---|---|---|---|
| $I$ (bilinear) | $z_\rho + z_\sigma = (\delta_\rho + \delta_\sigma) + i(\gamma_\rho + \gamma_\sigma)$ | $\delta_\sigma = -\delta_\rho \;\land\; \gamma_\sigma = -\gamma_\rho$ | $\sigma = 1 - \rho$ ($F$-pair) |
| $C$ (sesquilinear conjugation) | $z_\rho + \bar{z}_\sigma = (\delta_\rho + \delta_\sigma) + i(\gamma_\rho - \gamma_\sigma)$ | $\delta_\sigma = -\delta_\rho \;\land\; \gamma_\sigma = \gamma_\rho$ | $\sigma = 1 - \bar{\rho}$ ($R$-reflection pair) |
| $F$ (bilinear + inversion) | $z_\rho - z_\sigma = (\delta_\rho - \delta_\sigma) + i(\gamma_\rho - \gamma_\sigma)$ | $\delta_\sigma = \delta_\rho \;\land\; \gamma_\sigma = \gamma_\rho$ | $\sigma = \rho$ (diagonal $I$-pair) |
| $R = F \circ C$ (sesquilinear + inversion) | $z_\rho - \bar{z}_\sigma = (\delta_\rho - \delta_\sigma) + i(\gamma_\rho + \gamma_\sigma)$ | $\delta_\sigma = \delta_\rho \;\land\; \gamma_\sigma = -\gamma_\rho$ | $\sigma = \bar{\rho}$ (conjugate $C$-pair) |

Thus the natural zero-independent sesquilinear correlation $\mathcal{G}_C(K, J)$ yields $\lambda_C(\rho, \sigma) = z_\rho + \bar{z}_\sigma$, selecting $\sigma = 1 - \bar{\rho}$ (`REFLECTION_PAIR_STATIONARY_FOR_SESQUILINEAR_CORRELATION`).

---

### G. Reflection-pair stationarity theorem

**Theorem (`reflection_stationary_iff` in Lean 4)**: For any two zeros $\rho = \frac{1}{2} + \delta_\rho + i\gamma_\rho$ and $\sigma = \frac{1}{2} + \delta_\sigma + i\gamma_\sigma$,

$$z_\rho + \bar{z}_\sigma = 0 \iff \bigl(\delta_\rho + \delta_\sigma = 0 \;\land\; \gamma_\rho = \gamma_\sigma\bigr) \iff \sigma = 1 - \bar{\rho}.$$

Moreover:
1. On the critical line ($\delta_\rho = 0$), $\rho = 1 - \bar{\rho}$ (the stationary relation is a diagonal self-reflection term of multiplicity weight $m_\rho^2$).
2. Off the critical line ($\delta_\rho \neq 0$), $\rho \neq 1 - \bar{\rho}$ (the stationary relation pairs two distinct off-critical zeros $(\rho, 1 - \bar{\rho})$ at the same height $\gamma_\rho$, and by functional-equation + Schwarz symmetry of $\xi(s)$, $m_{1 - \bar{\rho}} = m_\rho$, giving stationary block weight $m_\rho^2$).

---

### H. Inversion-even real state

For multiplicative inversion $(\mathcal{I}\Psi)(u) = u^{-1}\Psi(u^{-1})$ in half-density coordinates, $\widehat{\mathcal{I}\Psi}(z) = \widehat{\Psi}(-z)$. Defining the real inversion-even state

$$\Psi_t^+ = \frac{1}{2}\left(\Phi_t^{(2)} + \mathcal{I}\Phi_t^{(2)}\right),$$

its centered Mellin transform satisfies $\widehat{\Psi}_t^+(-z) = \widehat{\Psi}_t^+(z)$ and, because $\Psi_t^+$ is real-valued on $(0, \infty)$, $\widehat{\Psi}_t^+(\bar{z}) = \overline{\widehat{\Psi}_t^+(z)}$. Consequently, on every reflection pair $(z, -\bar{z})$:

$$\widehat{\Psi}_t^+(z)\,\widehat{\Psi}_t^+(-\bar{z}) = \widehat{\Psi}_t^+(z)\,\overline{\widehat{\Psi}_t^+(z)} = \left|\widehat{\Psi}_t^+(z)\right|^2 \ge 0.$$

At the self-dual heat parameter $t = 1$, theta self-duality implies that $\Phi_1^{(2)}$ is already invariant under the completed functional-equation involution, and since $\Gamma(s/2)$ has no zeros in $\mathbb{C}$ while $\frac{1}{16}s^2(s-1)^2$ vanishes only at $s \in \{0, 1\}$, we have $\widehat{\Phi}_1^{(2)}(z) \neq 0$ for every $z$ in the open critical strip $-\frac{1}{2} < \operatorname{Re}(z) < \frac{1}{2}$ ($0 < \operatorname{Re}(s) < 1$).

---

### I. Reflection-quartet radial identity

Evaluating the quadratic curvature polynomial $P(z_\rho, z_\sigma) = (z_\rho - z_\sigma)^2 + 2(z_\rho + z_\sigma)$ from `TASK-TC-036` on the $R$-stationary reflection pair $z_\sigma = -\bar{z}_\rho = -\delta_\rho + i\gamma_\rho$ (where $z_\rho - z_\sigma = 2\delta_\rho$ and $z_\rho + z_\sigma = 2i\gamma_\rho$) gives

$$P(z_\rho, -\bar{z}_\rho) = (2\delta_\rho)^2 + 2(2i\gamma_\rho) = 4\delta_\rho^2 + 4i\gamma_\rho.$$

On the Schwarz-conjugate reflection pair $(\bar{\rho}, 1 - \rho)$ where $z_{\bar{\rho}} = \delta_\rho - i\gamma_\rho$ and $-\bar{z}_{\bar{\rho}} = -\delta_\rho - i\gamma_\rho$,

$$P(z_{\bar{\rho}}, -\bar{z}_{\bar{\rho}}) = 4\delta_\rho^2 - 4i\gamma_\rho.$$

Summing the two conjugate reflection pairs cancels the imaginary ordinate drift $\pm 4i\gamma_\rho$ identically (`reflection_quartet_imaginary_cancellation` in Lean 4):

$$P_\rho + P_{\bar{\rho}} = 8\delta_\rho^2.$$

With the real inversion-even state $\Psi_t^+$, the formal stationary-sector quartet contribution is (`reflection_quartet_radial_defect_nonneg` in Lean 4):

$$8 m_\rho^2 \left|\widehat{\Psi}_t^+(z_\rho)\right|^2 \delta_\rho^2 \ge 0.$$

This is strictly a **formal stationary-sector identity** unless an analytic zero-independent projector onto the stationary sector exists.

---

### J. Finite Laurent projector no-go

Consider any zero-independent finite discrete-grade filter

$$\Pi_N[f] = \sum_{K=-N}^{N} c_K f(K), \qquad P_N(q) = \sum_{K=-N}^{N} c_K q^K.$$

An exact reflection projector requires $P_N(1) \neq 0$ while $P_N(q_{\rho,\sigma}) = 0$ for every nonstationary pair character $q_{\rho,\sigma} = \tau^{z_\rho + \bar{z}_\sigma} \neq 1$.

**Distinct-Character Theorem**: Fix one nontrivial zero $\rho_0$. Then $\{q_\sigma = \tau^{z_{\rho_0} + \bar{z}_\sigma} : \zeta(\sigma) = 0\}$ assumes infinitely many distinct complex values:
1. Suppose $q_\sigma$ took only finitely many values $\{w_1, \dots, w_M\}$.
2. Since $e^{w \log\tau} = e^{w' \log\tau} \iff w - w' \in \frac{2\pi i}{\log\tau}\mathbb{Z}$, each $w_j$ restricts $\gamma_\sigma = \operatorname{Im}(\sigma)$ to a single vertical arithmetic progression with spacing $\frac{2\pi}{\log\tau} \approx 3.4187$.
3. A finite union of $M$ vertical progressions with spacing $\frac{2\pi}{\log\tau}$ contains at most $O(T)$ points up to height $T$.
4. This contradicts the Riemann–von Mangoldt zero-counting formula (von Mangoldt 1905; Titchmarsh 1986, Theorem 9.4; Trudgian 2014):
   $$N(T) = \frac{T}{2\pi}\log\frac{T}{2\pi} - \frac{T}{2\pi} + O(\log T) = \Omega(T\log T).$$

Since $q^N P_N(q)$ is a polynomial of degree $\le 2N$ vanishing on infinitely many distinct nonzero points $q_\sigma$, it vanishes identically (`finite_polynomial_projector_root_no_go` in Lean 4), forcing $P_N(1) = 0$.  
**Classification**: `FINITE_GRADE_LAURENT_PROJECTOR_NO_GO`.

---

### K. Finite differential projector no-go

A finite-order common-grade differential operator $p(\partial_r) = \sum_{m=0}^M a_m \partial_r^m$ acts on $e^{r\lambda}$ by $p(\lambda) e^{r\lambda}$. Since a fixed $\rho_0$ and varying $\sigma$ generate infinitely many distinct nonzero pair exponents $\lambda_{\rho_0, \sigma} = (z_{\rho_0} + \bar{z}_\sigma)\log\tau$, any polynomial $p$ vanishing on all nonstationary pair exponents satisfies $p \equiv 0$, contradicting $p(0) \neq 0$ (`finite_differential_projector_root_no_go` in Lean 4). The same holds for any rational filter $R(\lambda) = p(\lambda)/q(\lambda)$ analytic at $\lambda = 0$, since removing the finitely many poles of $q$ still leaves infinitely many distinct roots of the polynomial numerator $p$.  
**Classification**: `FINITE_ORDER_GRADE_DIFFERENTIAL_PROJECTOR_NO_GO`.

---

### L. Discrete Cesàro / Følner audit

For the bilateral discrete-grade Cesàro average

$$A_N(q) = \frac{1}{2N+1}\sum_{K=-N}^{N} q^K,$$

we have (`cesaro_unit_character_limit_control` in Lean 4):
- **Stationary character ($q = 1$)**: $A_N(1) = 1$ for all $N \ge 0$.
- **Unitary nonstationary character ($|q| = 1, q \neq 1$)**: $|A_N(q)| = \frac{|q^{2N+1} - 1|}{(2N+1)|q - 1|} \le \frac{2}{(2N+1)|q - 1|} \to 0$ as $N \to \infty$.
- **Nonunitary character ($|q| \neq 1$)**: By bilateral symmetry $q^N + q^{-N} - 2 = \frac{(q^N - 1)^2}{q^N} > 0$ (for $q > 0, q \neq 1$), either the positive-grade ray ($|q| > 1$) or the negative-grade ray ($0 < |q| < 1$) grows exponentially as $\frac{\max(|q|, |q|^{-1})^N}{2N+1} \to +\infty$.

---

### M. Continuous Cesàro audit

For continuous common shift $r \in [-T, T]$,

$$C_T(\lambda) = \frac{1}{2T}\int_{-T}^{T} e^{r\lambda}\,dr = \frac{\sinh(T\lambda)}{T\lambda}.$$

- If $\lambda = 0$: $C_T(0) = 1$.
- If $\lambda = i\omega \neq 0$ ($\omega \in \mathbb{R} \setminus \{0\}$): $C_T(i\omega) = \frac{\sin(T\omega)}{T\omega} \to 0$ as $T \to \infty$.
- If $\operatorname{Re}(\lambda) \neq 0$: $|C_T(\lambda)| \sim \frac{e^{T|\operatorname{Re}\lambda|}}{2T|\lambda|} \to +\infty$ exponentially as $T \to \infty$.

**Classification**: `CONTINUOUS_GRADE_HAAR_PROJECTION_REQUIRES_UNITARY_CHARACTERS`.

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
3. For the repaired state $\Phi_t^{(2)}$, the diagonal Mellin weight $|\widehat{\Phi}_t^{(2)}(z_\rho)|^2$ is strictly positive throughout the open critical strip $0 < \operatorname{Re}(\rho) < 1$ because $\Gamma(\rho/2)$ has no zeros and $\frac{1}{16}\rho^2(\rho - 1)^2$ vanishes only at $\rho \in \{0, 1\}$.
4. Consequently, discrete Cesàro $A_N(q_{\rho,\rho})$, continuous Cesàro $C_T(2\delta_\rho\log\tau)$, Abel $A_r(q_{\rho,\rho})$, and Gaussian $G_T(2\delta_\rho\log\tau)$ all diverge whenever $\delta_\rho \neq 0$.

Furthermore, rotating the grade contour to $K = v e^{i\theta}$ cannot unitarize the spectrum for any fixed zero-independent angle $\theta$: off-diagonal critical pairs ($\operatorname{Re}\lambda = 0, \operatorname{Im}\lambda \neq 0$) require $\sin\theta = 0$ for bilateral boundedness, whereas off-critical diagonal pairs ($\operatorname{Re}\lambda = 2\delta_\rho \neq 0, \operatorname{Im}\lambda = 0$) require $\cos\theta = 0$. Since $\sin^2\theta + \cos^2\theta = 1$, no fixed $\theta$ makes both bounded.  
**Classification**: `OFF_CRITICAL_NONUNITARITY_BLOCKS_GRADE_HAAR_PROJECTION`.

---

### P. Cross-grade arithmetic-zero compatibility

To obtain an arithmetic contradiction, the spectral projection would need to act on a family possessing an exact nonpositive or vanishing arithmetic law, such as the cross-grade overlap $Q_\varepsilon^{K, J}[w]$ at $(K, J) = (0, 1)$, where narrow support ($\varepsilon < \frac{1}{2}\Delta_{\min}(15, 1)$ with $\Delta_{\min}(15, 1) = 19 - 6\pi > 0$) gives $Q_\varepsilon^{0, 1}[w] = 0$. Under a common grade shift $(0, 1) \mapsto (r, 1 + r)$ with the transported-kernel ansatz

$$F_r(x, y) = \tau^{ar} F_0(\tau^{-br} x, \tau^{-br} y),$$

evaluating at the shifted prime-power stations $x_r(n) = \tau^r n$ and $y_{1+r}(m) = \tau^{1+r} m$ yields

$$F_r(\tau^r n, \tau^{1+r} m) = \tau^{ar} F_0\!\left(\tau^{(1-b)r} n, \,\tau^{(1-b)r} (\tau m)\right).$$

Preserving the unshifted station labels $(n, \tau m)$ and the uniform support-separation proof across all common shifts $r$ uniquely forces

$$1 - b = 0 \iff b = 1.$$

---

### Q. Transport–projection incompatibility

Under the transported kernel $F_r(x, y) = \tau^{ar} F_0(\tau^{-br} x, \tau^{-br} y)$, the two-variable Mellin transform acquires the scaling factor $\tau^{r(a + b(s + t))}$, while the explicit-formula zero stations at grades $(r, 1 + r)$ contribute $\tau^{-r(s + t)}$. The net common-shift spectral exponent is (`transport_projection_incompatibility_algebra` in Lean 4):

$$r\bigl(a + b(s + t)\bigr) - r(s + t) = ar + (b - 1)r(s + t).$$

At the unique arithmetic station-preserving parameter $b = 1$:

$$(1 - 1)r(s + t) = 0,$$

so the zero-dependent common-shift spectral character is **erased identically** for every pair of zeros! Conversely, if $b \neq 1$ (for instance $b = 0$), the spectral common-shift character survives, but the dilated stations $\tau^{(1-b)r} n$ sweep across the fixed support of $F_0$ as $r$ varies, destroying the cross-grade arithmetic vanishing law.  
**Classification**: `COMMON_SHIFT_PROJECTION_TRANSPORT_INCOMPATIBILITY`.

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

When common-shift projection is blocked, the single permitted fallback is the relative grade $d = J - K$. Although $\tau^K \mathbb{Z} \cap \tau^J \mathbb{Z} = \{0\}$ holds pointwise for $K \neq J$ by Lindemann's transcendence theorem for $\tau = 2\pi$, converting this into a smooth zero-independent explicit-formula functional over infinitely many relative grades $d$ faces a Diophantine dilemma:
1. On the full untruncated prime-power spectrum, $\min_{2 \le n, m \le M} |\log(n/m) - d\log\tau|$ shrinks toward $0$ as the station cutoff $M \to \infty$ (from $0.00807$ at $M = 15$ to $0.000188$ at $M = 200$ for $d = 1$), so no fixed positive bandwidth $\varepsilon > 0$ avoids cross-grade collisions on the full prime spectrum.
2. On a fixed compact support window $[2, N]^2$, as $d$ grows, $\tau^d [2, N]$ exits $[2, N]$ completely, producing trivial support disjointness without isolating the $R$-stationary reflection sector.

---

### T. Arithmetic contradiction gate

Comparing the arithmetic and spectral signs across both candidate families (`projected_arithmetic_zero_and_positive_radial_contradiction` in Lean 4):
1. For the untwisted sesquilinear correlation $\mathcal{G}_C(r, r) = |W_{\mathrm{comp}}(U_{-r}\Psi_t^+)|^2 \ge 0$, both the arithmetic side and the formal stationary-sector spectral sum $\sum_{\rho/\sim} 8 m_\rho^2 |\widehat{\Psi}_t^+(z_\rho)|^2 \delta_\rho^2 \ge 0$ are nonnegative; having $\ge 0$ on both sides yields **no contradiction** (`REFLECTION_PROJECTION_HAS_NO_ARITHMETIC_SIGN_CONTRADICTION`).
2. For the cross-grade narrow-support functional $Q_\varepsilon^{r, 1+r}[F_r]$, preserving $Q_\varepsilon = 0$ requires $b = 1$, which erases the common-shift spectral character identically.
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

Following the Section 27 decision tree and Section 37 governing falsification test:

$$\boxed{\texttt{GRADE\_CHARACTER\_PROJECTION\_DOES\_NOT\_ESCAPE\_TRANSPORT\_MOMENT\_INCOMPATIBILITY}}$$

with secondary classification:

$$\boxed{\texttt{OFF\_CRITICAL\_NONUNITARITY\_BLOCKS\_GRADE\_HAAR\_PROJECTION}}$$

and obligation status:

$$\boxed{\texttt{OBL-CT-001A} = \texttt{OPEN}.}$$

Specifically, the three possible routes for grade-character reflection projection are closed by exact theorems:
1. **Projection failure (untransported $b = 0$)**: Finite Laurent and differential filters are ruled out by Riemann–von Mangoldt zero counting (`FINITE_GRADE_LAURENT_PROJECTOR_NO_GO`, `FINITE_ORDER_GRADE_DIFFERENTIAL_PROJECTOR_NO_GO`), and infinite approximate-Haar averages (discrete Cesàro, continuous Cesàro, Abel, Gaussian) diverge on off-critical diagonal terms $q_{\rho,\rho} = \tau^{2\delta_\rho} \neq 1$ (`OFF_CRITICAL_NONUNITARITY_BLOCKS_GRADE_HAAR_PROJECTION`).
2. **Transport incompatibility ($b = 1$)**: Preserving the cross-grade arithmetic vanishing law $Q_\varepsilon^{r, 1+r}[F_r] = 0$ forces full coordinate transport $b = 1$ (or scale-invariant ratio kernels $\varphi(x/y)$), which identically cancels the common-shift spectral exponent $(b - 1)r(s + t) = 0$ (`COMMON_SHIFT_PROJECTION_TRANSPORT_INCOMPATIBILITY`, `SCALE_INVARIANT_ARITHMETIC_KERNEL_ERASES_COMMON_GRADE_CHARACTER`).
3. **Absence of an arithmetic sign contradiction**: On the sesquilinear correlation $\mathcal{G}_C(r, r) = |W_{\mathrm{comp}}(U_{-r}\Psi_t^+)|^2 \ge 0$, both the arithmetic value and the formal stationary-sector radial sum are nonnegative (`REFLECTION_PROJECTION_HAS_NO_ARITHMETIC_SIGN_CONTRADICTION`).

---

### W. Exact next theorem, if any

Under `OBL-CT-001A`, the single remaining theorem target (`SUBGATE-TC-037A`) is:

> **Subgate `SUBGATE-TC-037A`**: Determine whether there exists a zero-independent operator or kernel construction across $\tau$-grades that (a) does not rely on full common-scale coordinate transport $b = 1$ (which erases the common-shift spectral character) and (b) does not rely on unitary grade-character averaging (which diverges on off-critical diagonal terms $\tau^{2\delta_\rho} \neq 1$), yet still enforces a nonpositive arithmetic law paired with a nonnegative non-reflection spectral complement.

---

### Compact Evidence Table (Section 34)

| Result | Internal derivation | External theorem | Evidence class |
|---|---|---|---|
| Klein-four zero symmetries $V_4 = \{I, C, F, R\}$ and $R^2 = I$ | `centered_zero_reflection_identity` (`GradeCharacterProjection.lean`) | Functional equation $\xi(s) = \xi(1-s)$ & Schwarz reflection (Riemann 1859; Titchmarsh 1986) | `LEAN_PROVED` (algebraic coordinate identities) |
| Reflection-pair stationarity $z_\rho + \bar{z}_\sigma = 0 \iff \sigma = 1 - \bar{\rho}$ | `reflection_stationary_iff` (`GradeCharacterProjection.lean`) | Multiplicity symmetry $m_{1-\bar{\rho}} = m_\rho$ of $\xi(s)$ | `LEAN_PROVED` (iff & self-reflection) |
| Pair character modulus $\tau^{r\delta_1}\tau^{r\delta_2} = \tau^{r(\delta_1+\delta_2)}$ and off-critical diagonal $q_{\rho,\rho} = \tau^{2\delta_\rho} \neq 1$ | `grade_pair_character_modulus`, `offcritical_diagonal_character_nonunitary` (`GradeCharacterProjection.lean`) | Mellin dilation transform law (Titchmarsh 1948) | `LEAN_PROVED` (real power modulus & nonunitarity) |
| Infinitely many distinct pair characters $q_\sigma = \tau^{z_{\rho_0} + \bar{z}_\sigma}$ for fixed $\rho_0$ | Vertical progression count $O(T)$ vs $\Omega(T\log T)$ (`audit_finite_laurent_projector_no_go`) | Riemann–von Mangoldt zero-counting formula $N(T)$ (von Mangoldt 1905; Titchmarsh 1986, Thm 9.4; Trudgian 2014, `arXiv:1208.5846v2`) | `PROVED_CONDITIONAL` / paper derivation from classical theorem |
| Finite Laurent & differential projector root no-go ($P \equiv 0$, $p \equiv 0$) | `finite_polynomial_projector_root_no_go`, `finite_differential_projector_root_no_go` (`GradeCharacterProjection.lean`) | Polynomial root bound over integral domains (Mathlib `Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero`) | `LEAN_PROVED` (finite root-count bound) + paper derivation (via $N(T)$) |
| Discrete/continuous Cesàro, Abel, and Gaussian divergence on nonunitary diagonal $q_{\rho,\rho} = \tau^{2\delta_\rho}$ | `cesaro_unit_character_limit_control` (`GradeCharacterProjection.lean`) & `audit_offcritical_diagonal_obstruction` | Harmonic analysis / Følner–Cesàro & Abel summability on $\mathbb{Z}, \mathbb{R}$ (Rudin 1962; Katznelson 2004; Folland 2016); nonvanishing of $\Gamma(s/2)$ | `LEAN_PROVED` (bilateral excess) + `PROVED_PAPER_DERIVATION` |
| Formal stationary-sector quartet identity $P_\rho + P_{\bar{\rho}} = 8\delta_\rho^2$ and $8 m_\rho^2 |\widehat{\Psi}_t^+(z_\rho)|^2 \delta_\rho^2 \ge 0$ | `reflection_quartet_imaginary_cancellation`, `reflection_quartet_radial_defect_nonneg` (`GradeCharacterProjection.lean`) | Weil explicit formula & Burnol conductor formalism (Weil 1952; Burnol `arXiv:math/9902080v1`, `arXiv:math/0101068v1`) | `LEAN_PROVED` (formal stationary-sector algebra) |
| Transport–projection incompatibility $(b - 1)r(s + t) = 0$ at $b = 1$ and ratio-kernel erasure on $s + t = 0$ | `transport_projection_incompatibility_algebra` (`GradeCharacterProjection.lean`) & `audit_common_shift_transport_compatibility` | Two-variable Mellin convolution/scaling law | `LEAN_PROVED` (exponent cancellation algebra) |
| Conditional contradiction vs same-sign consistency firewall | `projected_arithmetic_zero_and_positive_radial_contradiction` (`GradeCharacterProjection.lean`) | None (pure first-order real arithmetic) | `LEAN_PROVED` |
