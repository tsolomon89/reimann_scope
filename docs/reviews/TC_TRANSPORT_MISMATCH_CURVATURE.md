# Infinitesimal Transport-Mismatch Curvature and Non-Scalar Arithmetic Descent (`TASK-TC-034`)

**Task ID:** `TASK-TC-034`  
**Starting Commit:** `90493831c9bd803526593691e7f39b55a7b9fb40`  
**Substantive Parent:** `1d777ea1bc7e962ee6ad03f3f72b83c731dfb186`  
**Audited Obligation:** `OBL-CT-001A`  
**Principal Classification:** `MISMATCH_CURVATURE_REDUCES_TO_OBL_CT_001A`  
**Triggered Outcome Codes:** `ARITHMETIC_CURVATURE_FLATNESS_NOT_IMPLIED`, `COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PROVED`, `SPECTRAL_CURVATURE_IS_SIGNED_OR_DOUBLE_SUM`, `CURVATURE_POSITIVITY_IS_RH_EQUIVALENT`, `MISMATCH_CURVATURE_REDUCES_TO_OBL_CT_001A`  
**Evidence Class:** `LEAN_PROVED` (algebraic curvature identities, Lagrange sum-of-squares decomposition, Euler-homogeneity flatness, $K$-independence of normalized mismatch curvature, even second-difference identity, centered pairing algebra, signed-weight countermodel, generic-base covariance) + `PROVED_PAPER_DERIVATION` (compact-support ODE homogeneity no-go, complete two-variable explicit formula spectral expansion, theta–Mellin non-scalar descent audit) + `EMPIRICAL` (certified finite-station evaluations in `data/tc_transport_mismatch_curvature.json`).

---

### A. TASK-TC-033 transport–moment incompatibility

In `TASK-TC-033` (`docs/reviews/TC_THREE_GRADE_HANKEL_CONSTRAINT.md`), the transported two-variable kernel family
$$F_{K,b}(x,y) = \tau^{aK} F_0\!\left(\tau^{-bK}x, \tau^{-bK}y\right), \qquad \tau = 2\pi,$$
was audited across grades $K \in \{-1, 0, +1\}$. That audit established the theorem **`TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED`**:
1. At the unique label-preserving transport $b = 1$, every grade samples the identical native prime-power stations $(n,m)$ with $F_{K,1}(\tau^K n, \tau^K m) = \tau^{aK} F_0(n,m)$, yielding an exact rank-one geometric sequence $M_K = \tau^{aK} M_0$ with vanishing three-grade Hankel determinant $\mathcal H_0(M) = M_{-1}M_1 - M_0^2 = 0$, **but** simultaneously canceling the zero-dependent spectral grade factor:
   $$\tau^{(b-1)K(\rho+\sigma)}\Big|_{b=1} = 1.$$
2. For any finite displacement $b \neq 1$, the spectral factor $\tau^{(b-1)K(\rho+\sigma)}$ retains grade variation, **but** the arithmetic side evaluates $F_0(\tau^{(1-b)K}n, \tau^{(1-b)K}m)$ at shifted stations across grades, destroying the rank-one arithmetic identity $\mathcal H_0(M) = 0$.

`TASK-TC-034` tests whether the missing constraint resides in the **infinitesimal second variation (curvature)** around the unique compatible transport $b = 1$ ($b = 1 + \eta$, $\eta \to 0$) rather than in finitely displaced transport values.

---

### B. Hypothesis versus implementation

In accordance with the Section 2 Hypothesis-Fidelity Rule, we maintain a strict separation between four levels:

1. **General TC Hypothesis:**
   $$\boxed{\text{The same arithmetic object across transcendental grades implies a constraint.}}$$
2. **Candidate Implementation (`TASK-TC-034`):**
   $$\boxed{\text{The constraint is the infinitesimal transport-mismatch curvature around } b = 1.}$$
3. **Admissible Test Space / Kernel Class:** Smooth compactly supported two-variable kernels $F_0 \in C_c^\infty((0,\infty)^2)$ (Phase I) and bilinear scale-mismatched theta–Mellin kernels $\Phi_0$ (Phase II).
4. **Scope of Negative Conclusions:** Failure of this infinitesimal mismatch-curvature candidate on compactly supported two-variable kernels and bilinear theta–Mellin forms refutes **this candidate implementation and kernel class**, **never** the general TC hypothesis.

---

### C. Relative transport parameter

Write the transport exponent around the unique label-preserving point $b = 1$ as
$$b = 1 + \eta, \qquad \eta \in \mathbb{R},$$
and define the mismatch-transported kernel
$$F_{K,\eta}(x,y) = \tau^{aK} F_0\!\left(\tau^{-(1+\eta)K}x, \tau^{-(1+\eta)K}y\right).$$
Pairing $F_{K,\eta}$ against the grade-$K$ prime-power measure $\mu_K = \sum_{n\ge 2}\Lambda(n)\delta_{\tau^K n}$ and normalizing out the scalar amplitude $\tau^{aK}$ yields the normalized equal-grade arithmetic mismatch energy:
$$\widehat{\mathcal M}_K(\eta) = \tau^{-aK}\langle \mu_K \otimes \mu_K, F_{K,\eta}\rangle = \sum_{n,m\ge 2}\Lambda(n)\Lambda(m)\,F_0\!\left(\tau^{-\eta K}n, \tau^{-\eta K}m\right).$$
At the compatibility point $\eta = 0$:
$$\widehat{\mathcal M}_K(0) = \sum_{n,m\ge 2}\Lambda(n)\Lambda(m)F_0(n,m) = \widehat{\mathcal M}_0(0) \qquad \forall K \in \mathbb{R},$$
recovering the exact value-level compatibility of `TASK-TC-033`.

---

### D. Arithmetic Euler derivatives

Define the two-variable Euler scaling generator:
$$\mathcal E = x\frac{\partial}{\partial x} + y\frac{\partial}{\partial y}.$$
Writing $u = -\eta K \log\tau$, the chain rule along the scaling ray $(e^u x, e^u y)$ gives
$$\left.\frac{\partial^j}{\partial \eta^j} F_0\!\left(\tau^{-\eta K}x, \tau^{-\eta K}y\right)\right|_{\eta=0} = (-K\log\tau)^j \bigl(\mathcal E^j F_0\bigr)(x,y) \qquad (j \ge 0).$$
When $F_0$ has compact support in $(0,\infty)^2$, only finitely many prime-power pairs $(n,m)$ lie in a neighborhood of $\operatorname{supp}(F_0)$ for $|\eta|$ sufficiently small, so differentiation under the sum is exact with no infinite-series tail issue. Defining the zero-independent arithmetic Euler moments
$$A_j(F_0) = \sum_{n,m\ge 2}\Lambda(n)\Lambda(m)\bigl(\mathcal E^j F_0\bigr)(n,m),$$
we obtain:
$$\widehat{\mathcal M}_K^{(j)}(0) = (-K\log\tau)^j A_j(F_0),$$
and in particular:
$$\widehat{\mathcal M}_K(0) = A_0(F_0), \qquad \widehat{\mathcal M}_K'(0) = -K\log\tau\,A_1(F_0), \qquad \widehat{\mathcal M}_K''(0) = K^2(\log\tau)^2 A_2(F_0).$$

---

### E. Arithmetic curvature determinant

The arithmetic transport curvature is defined by
$$\mathfrak C_{\mathrm{arith}}(F_0) = A_0(F_0)A_2(F_0) - A_1(F_0)^2.$$
For any nonzero grade $K \neq 0$, the $(-K\log\tau)$ factors cancel upon normalization (`mismatch_curvature_k_independent` in `formal/RiemannScope/TransportMismatchCurvature.lean`):
$$\mathfrak C_{\mathrm{arith}}(F_0) = \frac{\widehat{\mathcal M}_K(0)\widehat{\mathcal M}_K''(0) - \bigl(\widehat{\mathcal M}_K'(0)\bigr)^2}{K^2(\log\tau)^2}.$$
When $A_0(F_0) > 0$, the normalized log-curvature is
$$\kappa_{\mathrm{arith}}(F_0) = \frac{A_0(F_0)A_2(F_0) - A_1(F_0)^2}{A_0(F_0)^2} = \left.\frac{1}{K^2(\log\tau)^2}\frac{\partial^2}{\partial\eta^2}\log \widehat{\mathcal M}_K(\eta)\right|_{\eta=0}.$$

**Decisive Gate 1 Finding (`ARITHMETIC_CURVATURE_FLATNESS_NOT_IMPLIED`):**  
Preserving the same arithmetic labels at $\eta = 0$ makes $\widehat{\mathcal M}_K(0) = A_0(F_0)$ and $\mathfrak C_{\mathrm{arith}}(F_0)$ **independent of $K$**, but it does **not** force $\mathfrak C_{\mathrm{arith}}(F_0) = 0$. Furthermore, because $\mathcal E^2 F_0$ contains second radial derivatives of the kernel profile rather than first-order squared weights, $\mathfrak C_{\mathrm{arith}}(F_0)$ is **indefinite in sign** across nonnegative compactly supported kernels $F_0 \ge 0$ (`GENERAL_ARITHMETIC_MISMATCH_CURVATURE_INDEFINITE`):
- For the unimodal log-Gaussian $F_0(x,y) = \exp(-\frac{3}{2}(\log(xy/16))^2)$ ($n_{\max}=15$), $A_0 \approx 44.2894 > 0$ and $\mathfrak C_{\mathrm{arith}}(F_0) \approx -6442.343 < 0$.
- For the radially convex profile $F_0(x,y) = \cosh(1.2\log(xy/25))\exp(-0.08(\log(xy/25))^2)$ ($n_{\max}=15$), $A_0 \approx 292.8649 > 0$ and $\mathfrak C_{\mathrm{arith}}(F_0) \approx +191886.98 > 0$.
- For a flat-top plateau kernel covering active stations $\{2,3\}$ ($n_{\max}=3$), $\mathfrak C_{\mathrm{arith}}(F_0) = 0$, which breaks to $\mathfrak C_{\mathrm{arith}}(F_0) \approx -1192.087 \neq 0$ as soon as the window expands to $n_{\max}=5$ (`FINITE_ACCIDENTAL_ARITHMETIC_CURVATURE_ZERO`).

---

### F. Positive exponential curvature identity

For any finite exponential mixture with positive weights
$$M(\eta) = \sum_{j=1}^r w_j e^{\eta x_j}, \qquad w_j > 0, \; x_j \in \mathbb{R},$$
Lagrange's identity gives:
$$M(0)M''(0) - M'(0)^2 = \left(\sum_{i=1}^r w_i\right)\left(\sum_{j=1}^r w_j x_j^2\right) - \left(\sum_{i=1}^r w_i x_i\right)^2 = \frac{1}{2}\sum_{i,j=1}^r w_i w_j (x_i - x_j)^2 \ge 0.$$
This is machine-checked in Lean 4 (`single_exponential_log_curvature_zero`, `two_exponential_curvature_identity`, `two_exponential_positive_log_curvature`, `positive_finite_exponential_curvature_nonneg`, `three_exponential_curvature_nonneg`, and `reciprocal_pair_curvature_strict_pos` in `formal/RiemannScope/TransportMismatchCurvature.lean`):
1. For a single exponential ($r=1$), $M(0)M''(0) - M'(0)^2 = 0$.
2. For $w_j > 0$, $M(0)M''(0) - M'(0)^2 > 0$ if and only if at least two exponents $x_i \neq x_j$ are distinct.
3. For a symmetric/reciprocal pair $x_1 = x$, $x_2 = -x$ with $x \neq 0$ and $w_1, w_2 > 0$, the curvature determinant equals $4 w_1 w_2 x^2 > 0$.
4. When weights are allowed to be signed ($w_1 = 1, w_2 = -2, x_1 = 0, x_2 = 1$), $M(0)M''(0) - M'(0)^2 = -2 < 0$ (`signed_weight_curvature_negative`).

---

### G. Mellin-side mismatch derivatives

Under the repository's two-variable Mellin convention,
$$H_{K,\eta}(s,t) = \iint_{(0,\infty)^2} F_{K,\eta}(x,y)\,x^{s-1}y^{t-1}\,dx\,dy = \tau^{K(a + (1+\eta)(s+t))} H_0(s,t).$$
Combining $H_{K,\eta}(s,t)$ with the grade-$K$ prime-measure scaling factors $\tau^{-K(s+t)}$ and normalizing by $\tau^{-aK}$ yields the net spectral mismatch factor (`mellin_mismatch_net_exponent` in `TransportMismatchCurvature.lean`):
$$\tau^{\eta K(s+t)} = \exp\bigl(\eta K(s+t)\log\tau\bigr).$$
Its first and second $\eta$-derivatives at $\eta = 0$ are:
$$\left.\partial_\eta \tau^{\eta K(s+t)}\right|_{\eta=0} = K\log\tau\,(s+t), \qquad \left.\partial_\eta^2 \tau^{\eta K(s+t)}\right|_{\eta=0} = K^2(\log\tau)^2(s+t)^2.$$

---

### H. Centering and pairing audit

Let $\rho = \tfrac{1}{2} + \delta_\rho + i\gamma_\rho$ denote a nontrivial zero with radial displacement $\delta_\rho = \operatorname{Re}(\rho) - \tfrac{1}{2}$ and ordinate $\gamma_\rho = \operatorname{Im}(\rho)$.
- Under the **uncentered** Mellin convention, the exponent is $s + t$.
- Under the **half-density centered** convention (pulling out $(xy)^{-1/2}$ so $s \mapsto s - \tfrac{1}{2}$, $t \mapsto t - \tfrac{1}{2}$), the centered exponent is
  $$\bigl(s - \tfrac{1}{2}\bigr) + \bigl(t - \tfrac{1}{2}\bigr) = s + t - 1.$$

Auditing the three candidate zero pairings under centered coordinates:

| Pairing | Second Variable $t$ | Centered Exponent $(s-\tfrac{1}{2})+(t-\tfrac{1}{2})$ | Even Mismatch Defect $\tau^{\eta K E} + \tau^{-\eta K E} - 2$ | Second Variation at $\eta=0$ |
| :--- | :--- | :--- | :--- | :--- |
| **Conjugate Pairing** | $t = \bar\rho = \tfrac{1}{2} + \delta_\rho - i\gamma_\rho$ | $2\delta_\rho$ (real radial) | $2\bigl(\cosh(2\eta K\delta_\rho\log\tau)-1\bigr) \ge 0$ | $+4K^2(\log\tau)^2\delta_\rho^2 \ge 0$ |
| **FE Reflection Pairing** | $t = 1 - \bar\rho = \tfrac{1}{2} - \delta_\rho + i\gamma_\rho$ | $2i\gamma_\rho$ (purely imaginary ordinate) | $2\bigl(\cos(2\eta K\gamma_\rho\log\tau)-1\bigr) \le 0$ | $-4K^2(\log\tau)^2\gamma_\rho^2 \le 0$ |
| **General Zero-Zero Pairing** | $t = \sigma = \tfrac{1}{2} + \delta_\sigma + i\gamma_\sigma$ | $(\delta_\rho + \delta_\sigma) + i(\gamma_\rho + \gamma_\sigma)$ | Complex oscillatory cross-term | $K^2(\log\tau)^2\bigl((\delta_\rho+\delta_\sigma)+i(\gamma_\rho+\gamma_\sigma)\bigr)^2$ |

**Which pairing is naturally induced?**  
Because $\widehat{\mathcal M}_K(\eta) = \langle \mu_K \otimes \mu_K, F_{K,\eta}\rangle$ is a bilinear pairing of two independent prime-power sums, the explicit formula expands each $\mu_K$ into a full sum over all nontrivial zeros $\rho$ and $\sigma$, poles, trivial zeros, and Archimedean terms. It therefore naturally induces the **unrestricted general zero-zero double sum** over all pairs $(\rho,\sigma)$, **not** an isolated conjugate-diagonal sum.

---

### I. Homogeneous-kernel candidate

If a kernel $F_0$ satisfies the Euler homogeneity equation
$$\mathcal E F_0 = d F_0$$
for a scalar constant $d \in \mathbb{R}$, then $\mathcal E^2 F_0 = d^2 F_0$, which implies
$$A_1(F_0) = d A_0(F_0), \qquad A_2(F_0) = d^2 A_0(F_0),$$
and therefore (`homogeneous_arithmetic_curvature_zero` in `TransportMismatchCurvature.lean`):
$$\mathfrak C_{\mathrm{arith}}(F_0) = A_0(d^2 A_0) - (d A_0)^2 = 0.$$
Equivalently, $\widehat{\mathcal M}_K(\eta) = e^{-d\eta K\log\tau}\widehat{\mathcal M}_K(0)$ is a pure single-character response in $\eta$.

---

### J. Compact-support homogeneity obstruction

**Theorem (`NONZERO_COMPACT_SUPPORT_HOMOGENEOUS_KERNEL_IMPOSSIBLE` / `COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PROVED`):**
$$\left(F_0 \in C_c^\infty((0,\infty)^2) \;\wedge\; \mathcal E F_0 = d F_0\right) \Longrightarrow F_0 \equiv 0.$$

**Proof:** Fix any point $(x_0, y_0) \in (0,\infty)^2$ and define $g(r) = F_0(rx_0, ry_0)$ for $r > 0$. By the chain rule and $\mathcal E F_0 = d F_0$, $r g'(r) = (\mathcal E F_0)(rx_0, ry_0) = d\,g(r)$, whose unique solution on $(0,\infty)$ is $g(r) = r^d F_0(x_0, y_0)$. If $F_0(x_0, y_0) \neq 0$, then $F_0(rx_0, ry_0) = r^d F_0(x_0, y_0) \neq 0$ for every $r \in (0,\infty)$, so $\operatorname{supp}(F_0)$ contains the unbounded ray $\{(rx_0, ry_0) : r > 0\}$, contradicting compact support in $(0,\infty)^2$. $\square$

Consequently, no nonzero compactly supported smooth kernel can achieve structural Euler-homogeneous arithmetic flatness.

---

### K. Complete spectral curvature

On the spectral side, the second $\eta$-derivative at $\eta = 0$ of the normalized explicit-formula expansion of $\widehat{\mathcal M}_K(\eta)$ has the form:
$$\widehat{\mathcal M}_K''(0) = K^2(\log\tau)^2 \left[ \sum_{\rho,\sigma} H_0(\rho,\sigma)(\rho+\sigma)^2 + \mathcal B_{\mathrm{pole}}'' + \mathcal B_{\mathrm{triv}}'' + \mathcal B_{\mathrm{arch}}'' \right].$$
Even if $F_0$ is chosen to be Hermitian-positive in log-coordinates ($H_0(s,t) = G_0(s)\overline{G_0(\bar t)}$), the double sum over zeros simplifies to the square of a single linear zero sum:
$$\sum_{\rho,\sigma} G_0(\rho)\overline{G_0(\bar\sigma)}(\rho+\sigma)^2,$$
which contains off-diagonal products $(\rho+\sigma)^2 = \rho^2 + 2\rho\sigma + \sigma^2$ rather than a diagonal positive sum $\sum_\rho w_\rho \delta_\rho^2$. The complete spectral curvature is therefore classified as **`SPECTRAL_CURVATURE_IS_SIGNED_OR_DOUBLE_SUM`** (Outcome D).

---

### L. Off-diagonal and background terms

All mandatory firewalls from Sections 15–16 are enforced:
1. **Zero-zero cross terms:** Present for all pairs $(\rho,\sigma)$ with $\sigma \neq \bar\rho$.
2. **Pole terms:** At $s=1$ and $t=1$, contributing $(1+1)^2 H_0(1,1) = 4 H_0(1,1)$ and zero-pole cross terms $-2\sum_\rho (1+\rho)^2 H_0(\rho,1)$.
3. **Trivial-zero and Archimedean terms:** Nonzero derivatives from $s,t \in -2\mathbb{N}$ and logarithmic gamma factors.
4. **No diagonal projection or remainder subordination:** Projecting onto the conjugate diagonal $t = \bar\rho$ without an arithmetic mechanism is classified as `SELECTED_CURVATURE_BLOCK_ONLY`. Treating off-diagonal and background terms as a subordinate remainder is closed by `TASK-TC-032R` (`EXACT_CANCELLATION_BLOCKS_STRICT_SUBORDINATION_ROUTE`).

---

### M. Existing Curvature Transport reconciliation

In `CURVATURE_TRANSPORT.md` and `ARITHMETIC_RADIAL_BRIDGE.md`, the existing Curvature Transport detector on a centered conjugate pair is
$$B_\rho(k) = 2\bigl(\cosh(k\delta_\rho\log\tau) - 1\bigr), \qquad B_\rho''(0) = 2\delta_\rho^2(\log\tau)^2.$$
In `TASK-TC-034`, the symmetric mismatch difference $\Delta_{\eta,K} = \tau^{\eta K(2\delta_\rho)} + \tau^{-\eta K(2\delta_\rho)} - 2$ evaluated on a centered conjugate pair is:
$$2\bigl(\cosh(2\eta K\delta_\rho\log\tau) - 1\bigr) = B_\rho(2\eta K),$$
with second $\eta$-derivative at $\eta = 0$ equal to $(2K)^2 \cdot \tfrac{1}{2} B_\rho''(0) = 4K^2\delta_\rho^2(\log\tau)^2$. Thus, on the conjugate block, infinitesimal mismatch curvature reproduces **the exact same detector** $B_\rho(2\eta K)$ without providing an arithmetic descent that isolates that block or forces arithmetic flatness. We therefore classify:
$$\boxed{\texttt{MISMATCH\_CURVATURE\_REDUCES\_TO\_EXISTING\_OBL\_CT\_001A}.}$$

---

### N. Theta–Mellin fallback

Since compact support prevents Euler homogeneity (Outcome C), Phase II audits at most one canonical noncompact candidate from the repository's theta–Mellin scaling family:
- The scalar candidate $a^{1/2-s}\Lambda(s)$ remains frozen and rejected (`REJECTED_FROZEN_IDENTICALLY_ZERO_AT_ZEROS`) because it vanishes identically at every zero $\rho$ and has identically zero grade derivatives.
- The canonical **non-scalar bilinear theta–Mellin candidate** defined before zero evaluation is
  $$\mathcal Q_\Theta(\eta; \Phi_0) = \iint_{(0,\infty)^2} \Theta_1^+(t_1)\Theta_1^+(t_2)\,\Phi_0\!\left(\tau^{-\eta K}t_1, \tau^{-\eta K}t_2\right)\frac{dt_1}{t_1}\frac{dt_2}{t_2}, \qquad \Theta_1^+(t) = \sum_{n=1}^\infty e^{-\pi n^2 t}.$$
  Auditing $\mathcal Q_\Theta(\eta; \Phi_0)$ against the 8 criteria of Section 18:
  1. Purely theta/arithmetic-defined: **Yes**.
  2. Zero-independent definition: **Yes**.
  3. Exact scale-flatness law ($\mathfrak C_\Theta = 0$): **No** — $\Theta_1^+(t)$ is a multi-exponential sum $\sum_{n\ge 1} e^{-\pi n^2 t}$, not homogeneous, and any test kernel $\Phi_0$ making the integral convergent on $(0,\infty)^2$ cannot be Euler-homogeneous.
  4. Convergent (with rapid decay / pole-killing operator $(\mathcal E_t - \tfrac{1}{2})\mathcal E_t$): **Yes**.
  5. Second mismatch variation computable: **Yes** via $\mathcal E^2 \Phi_0$.
  6. Spectral curvature contains $\delta_\rho^2$: **Only inside a double Mellin contour integral** $\iint \Lambda(s)\Lambda(t)\widetilde{\Phi}_0(s,t)\tau^{\eta K(s+t)/2}\,ds\,dt$.
  7. Avoids assumed Weil positivity: **Yes** (positivity of the resulting Hermitian form is RH-equivalent, not unconditional).
  8. Avoids selected-zero construction: **Yes**.

Hence the bilinear theta–Mellin candidate reduces to the same double-Mellin / Weil-form dilemma and does not close `OBL-CT-001A`.

---

### O. Tau-specificity

Repeating the Euler-generator and mismatch-curvature derivation for an arbitrary scale base $q > 1$ (`generic_base_mismatch_curvature_scaling` in `TransportMismatchCurvature.lean` and `evaluate_generic_base_mismatch_control` in `tc/transport_mismatch_curvature.py`):
$$\widehat{\mathcal M}_K^{(j)}(0; q) = (-K\log q)^j A_j(F_0), \qquad \frac{\widehat{\mathcal M}_K(0;q)\widehat{\mathcal M}_K''(0;q) - \bigl(\widehat{\mathcal M}_K'(0;q)\bigr)^2}{K^2(\log q)^2} = A_0(F_0)A_2(F_0) - A_1(F_0)^2.$$
The normalized mismatch curvature is numerically and algebraically identical across all bases $q \in \{2, e, 2\pi, 10\}$ (spread $< 2 \times 10^{-12}$, machine precision). Because no step in the Euler mismatch-curvature algebra uses a $\tau$-specific theorem, this step is classified as **`GENERIC_SCALE_CURVATURE`**. The constant $\tau = 2\pi$ enters only when connecting to Fourier self-duality $e^{-2\pi i x \xi}$, Jacobi theta modularity $\Theta(1/t) = \sqrt{t}\,\Theta(t)$, the completed zeta factor $\pi^{-s/2}\Gamma(s/2)$, or Lindemann transcendence of $2\pi$ on rational prime-power lattices.

---

### P. Weil-equivalence audit

If one modifies the two-variable mismatch kernel into a reflected Hermitian convolution form and asserts that its complete spectral curvature is non-negative across all admissible test functions, that assertion is a special case of the Weil / Connes–Consani positivity criterion, which is known to be equivalent to the Riemann Hypothesis. We therefore classify any global spectral-positivity assumption as:
$$\boxed{\texttt{CURVATURE\_POSITIVITY\_IS\_RH\_EQUIVALENT}.}$$

---

### Q. Principal classification

Answering the Section 30 Governing Falsification Test:
> *Does infinitesimal variation away from the unique label-preserving transport $b=1$ produce a zero-independent arithmetic curvature that is flat, while an off-critical zero forces strictly positive spectral curvature?*

**No**, for four proved structural reasons corresponding to Outcomes B, C, D, and E, which converge on Principal Outcome G:
1. **Outcome B (`ARITHMETIC_CURVATURE_FLATNESS_NOT_IMPLIED`):** Preserving arithmetic labels at $b=1$ makes $\mathfrak C_{\mathrm{arith}}(F_0) = A_0 A_2 - A_1^2$ independent of $K$, but does not imply $\mathfrak C_{\mathrm{arith}}(F_0) = 0$; on nonnegative kernels $F_0 \ge 0$, $\mathfrak C_{\mathrm{arith}}(F_0)$ takes positive, zero, and negative values (`GENERAL_ARITHMETIC_MISMATCH_CURVATURE_INDEFINITE`).
2. **Outcome C (`COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PROVED`):** Structural arithmetic flatness requires Euler homogeneity $\mathcal E F_0 = d F_0$, which is impossible for any nonzero $F_0 \in C_c^\infty((0,\infty)^2)$ (`NONZERO_COMPACT_SUPPORT_HOMOGENEOUS_KERNEL_IMPOSSIBLE`).
3. **Outcome D (`SPECTRAL_CURVATURE_IS_SIGNED_OR_DOUBLE_SUM`):** The two-variable arithmetic energy induces an unrestricted double sum over all zero pairs $(\rho,\sigma)$ plus pole, trivial-zero, and Archimedean background terms, not a positive scalar radial moment $\sum_\rho w_\rho \delta_\rho^2$.
4. **Outcome E (`CURVATURE_POSITIVITY_IS_RH_EQUIVALENT`):** Global positivity of a reflected Hermitian spectral form is RH-equivalent.
5. **Principal Classification — Outcome G (`MISMATCH_CURVATURE_REDUCES_TO_OBL_CT_001A`):** On a centered conjugate pair, the even mismatch defect equals $B_\rho(2\eta K)$, reducing directly to the existing open obligation `OBL-CT-001A` (`MISMATCH_CURVATURE_REDUCES_TO_EXISTING_OBL_CT_001A`).

---

### R. Exact next theorem, if any

`OBL-CT-001A` remains **OPEN**. The exact remaining mathematical problem is:

> **Remaining Theorem (`OBL-CT-001A`):** Construct a zero-independent, non-scalar arithmetic or theta-side functional whose relative transport curvature around $b = 1$ obeys a kernel-independent arithmetic flatness or sign law, while its complete spectral expansion (including all off-diagonal, pole, trivial-zero, and Archimedean terms) isolates a positive radial moment in $\delta_\rho^2$ without assuming a Weil-equivalent positivity hypothesis.
