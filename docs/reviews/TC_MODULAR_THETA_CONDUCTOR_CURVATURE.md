# TASK-TC-036 / TASK-TC-036R — Modular-Covariant Theta–Conductor Curvature Audit and Pole-Regularization Repair

**Task ID:** `TASK-TC-036` (repaired in `TASK-TC-036R`)  
**Task Completion Status:** `TASK_TC_036_MODULAR_THETA_CONDUCTOR_AUDIT_COMPLETE` / `TASK_TC_036R_POLE_REGULARIZATION_REPAIR_COMPLETE`  
**Starting Commit:** `e3e967f5288e41e55e101e9d7e88f7f541e94d43` (`TASK-TC-036R` starting HEAD `ba339873f3fbdf27922c69ee22b200e9ab67d437`)  
**Substantive Parent Commit:** `a8d7ccd5bd72e7c0f9577befaf15b0dc11777f54` (`TASK-TC-036` substantive commit `13f8342a6484b14b3421bc996bd1ec74c7786716`)  
**Principal Classification:** `ONE_PRECISE_THETA_CONDUCTOR_SUBGATE_OPEN`  
**Open Obligation Status:** `OBL-CT-001A = OPEN`  
**Exact Remaining Subgate:** `SUBGATE-TC-036A` (*Zero-Independent Diagonal-Isolation and Sign-Incompatibility Identity*)

---

## Section A — Executive Classification and `OBL-CT-001A` Status

After `TASK-TC-035` established `NO_ZERO_INDEPENDENT_SINGLE_KERNEL_SELECTOR_FOUND_IN_STANDARD_ZETA_AXIOMS` across six standard single-kernel selector families, `TASK-TC-036` (together with the `TASK-TC-036R` pole-regularization repair) audits the canonical **operator-level functional** candidate defined by the intersection of:

1. Jacobi theta self-duality ($\theta(1/t) = \sqrt{t}\,\theta(t)$, weight $w = 1/2$ in 1D and $w = 1$ in 2D);
2. heat-kernel scaling ($\Theta_t(x,y) = e^{-\pi t(x^2+y^2)}$, $\mathcal E\Theta_t = 2\mathcal D\Theta_t$);
3. the completed-zeta Archimedean factor ($\pi^{-s/2}\Gamma(s/2)$);
4. the Burnol/Weil local conductor operator ($H_\nu = A + B = M_{\log|\cdot|_\nu} + \mathcal F M_{\log|\cdot|_\nu}\mathcal F^{-1}$);
5. multiplicative grade transport ($U(\tau^{-\eta K})$); and
6. second-order scale differentiation ($\mathcal L_{\mathrm{heat}} = \mathcal E(\mathcal E - 2)$ vs. $\mathcal H_{\mathrm{mod},w} = (\mathcal D + w/2)^2$).

### Governing Question Answer and Executive Summary

$$
\boxed{
\texttt{ONE\_PRECISE\_THETA\_CONDUCTOR\_SUBGATE\_OPEN}
\qquad
(\texttt{OBL-CT-001A} = \texttt{OPEN})
}
$$

The modular-covariant theta–conductor construction yields exact algebraic and certified numerical results at every stage, and isolates four coupled structural reasons why it does **not** close `OBL-CT-001A` unconditionally:

1. **Affine Heat-Drift Compensator vs. Modular Hessian Split (`HEAT_AND_MODULAR_HESSIANS_DIFFER_BY_FORCED_CONNECTION_TERMS`)**:
   On the two-dimensional Gaussian heat family $\Theta_t(x,y) = e^{-\pi t(x^2+y^2)}$, the spatial Euler operator $\mathcal E = x\partial_x + y\partial_y$ and heat dilation generator $\mathcal D = t\partial_t$ satisfy $\mathcal E\Theta_t = 2\mathcal D\Theta_t$ and $\mathcal E^2\Theta_t = 4t^2\partial_t^2\Theta_t + 4t\partial_t\Theta_t$. Among operators $\mathcal L_c = \mathcal E(\mathcal E - c)$, $c = 2$ uniquely removes the affine $t\partial_t$ heat drift:
   $$
   \mathcal L_{\mathrm{heat}} = \mathcal E(\mathcal E - 2) = 4(\mathcal D^2 - \mathcal D),
   \qquad
   \mathcal L_{\mathrm{heat}}\Theta_t = 4t^2\partial_t^2\Theta_t.
   $$
   However, for modular weight $w = 1$ ($\Theta_{1/t}^{\mathrm{mod}} = t\,\Theta_t^{\mathrm{mod}}$), the modularly covariant derivative is $\nabla_1 = \mathcal D + 1/2$ and the modular Hessian is $\mathcal H_{\mathrm{mod},1} = (\mathcal D + 1/2)^2$, giving
   $$
   4\mathcal H_{\mathrm{mod},1} = (\mathcal E + I)^2 = 4t^2\partial_t^2 + 8t\partial_t + I,
   \qquad
   4\mathcal H_{\mathrm{mod},1} - \mathcal L_{\mathrm{heat}} = 8\mathcal D + I = 4\mathcal E + I \neq 0.
   $$
   Thus the heat-drift compensator $\mathcal L_{\mathrm{heat}}$ and the modular Hessian $4\mathcal H_{\mathrm{mod},1}$ do not coincide (`MODULAR_HESSIAN_DIFFERS_FROM_HEAT_COMPENSATOR`).

2. **Conductor–Dilation Commutation (`CONDUCTOR_COMMUTES_WITH_DILATION`)**:
   In Burnol's primary sources (`math/9902080v1`, `math/0101068v1`), the local conductor operator $H_\nu = A + B = M_{\log|\cdot|_\nu} + \mathcal F M_{\log|\cdot|_\nu}\mathcal F^{-1}$ acts on the 1D Hilbert space $L^2(K_\nu, dx)$ with invariant core $\Delta(K_\nu)$. Under the unitary dilation group $(U(\lambda)\phi)(x) = \lambda^{-1/2}\phi(x/\lambda)$ with generator $\mathcal A = x\partial_x + 1/2$, the position and momentum logarithmic shifts cancel:
   $$
   [\mathcal A, A] = I,
   \qquad
   [\mathcal A, B] = -I,
   \qquad
   [\mathcal A, \mathcal C] = [\mathcal A, A + B] = 0,
   \qquad
   [\mathcal A, [\mathcal A, \mathcal C]] = 0.
   $$
   Consequently, $\mathcal C$ commutes with multiplicative grade transport $U(\tau^{-\eta K})$ and generates no new non-commuting scale curvature (`CONDUCTOR_DILATION_COMMUTATION_REMOVES_NEW_GRADE_SIGNAL`).

3. **Sign Reversal Eliminates Arithmetic–Spectral Incompatibility (`POSITIVE_ARITHMETIC_VARIANCE_HAS_NO_CONTRADICTORY_SPECTRAL_LAW`)**:
   Replacing $\mathcal E^2$ by the drift-compensated operator $\mathcal L_{\mathrm{heat}} = \mathcal E(\mathcal E - 2)$ flips the prime-only curvature at $t = 1$ from strictly negative ($\mathfrak C_{\mathrm{arith}}(\Theta_1) \approx -3.4322 \times 10^{-21} < 0$) to the strictly positive Cauchy–Schwarz / Bernstein variance
   $$
   \mathfrak C_{\mathrm{prime}}^{\mathrm{cov}}(1)
   = A_0(1)A_{2,\mathrm{cov}}(1) - A_1(1)^2
   = 4\pi^2\bigl(M_0(1)M_2(1) - M_1(1)^2\bigr)
   \in \bigl[+1.6097089323851242452337142816 \times 10^{-26} \pm 3.98 \times 10^{-55}\bigr] > 0.
   $$
   Because $\mathfrak C_{\mathrm{prime}}^{\mathrm{cov}}(t) \ge 0$ and a hypothetical positive spectral curvature also satisfies $\mathscr A_{\mathrm{spec}} \ge 0$, both sides have the **same sign** ($\ge 0$). There is no sign incompatibility of the form $\mathscr A_{\mathrm{arith}} \le 0$ vs. $\mathscr A_{\mathrm{spec}} > 0$.

4. **Repaired Pole Regularization and Unrestricted Double-Zero Sum vs. RH-Equivalent Weil Positivity (`CORRECTED_POLE_REGULARIZER_D_SQUARED_MINUS_ONE_SIXTEENTH` / `UNRESTRICTED_DOUBLE_ZERO_SUM` / `THETA_CONDUCTOR_POSITIVITY_IS_RH_EQUIVALENT`)**:
   On the weight-normalized 1D theta state $\widetilde g_t(u) = t^{1/4}e^{-\pi t u^2}$, whose Mellin transform $\mathcal M[\widetilde g_t](s) = \frac{1}{2}\pi^{-s/2}\Gamma(s/2)t^{1/4-s/2}$ scales as $t^{1/4-s/2} = t^{-z/2}$ ($z = s - 1/2$), $\mathcal D = t\partial_t$ acts by $\frac{1}{4} - \frac{s}{2}$ (so the unshifted operator $\mathcal D(\mathcal D - \frac{1}{2})$ used in `TASK-TC-036` has Mellin multiplier $\frac{s^2}{4} - \frac{1}{16}$ and nonzero origin value $-\frac{1}{16}t^{1/4} \ne 0$, failing to annihilate the poles at $s = 0, 1$; `UNSHIFTED_REGULARIZER_DOES_NOT_ANNIHILATE_POLES`). In `TASK-TC-036R`, this is repaired by the exact pole-annihilator
   $$
   \mathcal P_{\mathrm{reg}}(\mathcal D) := \mathcal D^2 - \frac{1}{16} = \left(\mathcal D - \frac{1}{4}\right)\left(\mathcal D + \frac{1}{4}\right),
   \qquad
   \Phi_t(u) := \left(\mathcal D^2 - \frac{1}{16}\right)\widetilde g_t(u) = t^{1/4}\left(\pi^2 t^2 u^4 - \frac{3}{2}\pi t u^2\right)e^{-\pi t u^2},
   $$
   whose Mellin multiplier is $\left(\frac{1}{4}-\frac{s}{2}\right)^2 - \frac{1}{16} = \frac{1}{4}s(s-1) = \frac{1}{4}\left(z^2 - \frac{1}{4}\right)$ and which satisfies $\Phi_t(0) = 0$, $\Phi_t'(0) = 0$, and $\int_0^\infty \Phi_t(u)\,du = 0$ (with squared companion $\Phi_t^{(2)} = (\mathcal D^2 - \frac{1}{16})^2\widetilde g_t$ vanishing at both $s = 0$ and $s = 1$ even after multiplying by $\Gamma(s/2)$). On the repaired state, the linear explicit-formula functional $\mathscr L_{\Theta,\mathcal C}^{\mathrm{cov}}(t)$ remains a signed single-zero sum (`SIGNED_SINGLE_ZERO_SUM`), while the quadratic variance functional $\mathscr A_{\Theta,\mathcal C}^{\mathrm{cov}}(t)$ expands into an unrestricted double sum over all ordered pairs $(\rho, \sigma)$ of nontrivial zeros (`UNRESTRICTED_DOUBLE_ZERO_SUM`, `THETA_CONDUCTOR_FUNCTIONAL_REMAINS_DOUBLE_SPECTRAL`), and global positivity of the convolution square $Z(g * g^*)$ remains equivalent to Weil's positivity criterion (`THETA_CONDUCTOR_POSITIVITY_IS_RH_EQUIVALENT`).

---

## Section B — `TASK-TC-035` Scope Repairs

Before auditing the operator-level theta–conductor functional, `TASK-TC-036` repairs four scope overstatements in the `TASK-TC-035` artifacts (`tc/canonical_selector_audit.py`, `data/tc_canonical_zeta_selector_audit.json`, and `docs/reviews/TC_CANONICAL_ZETA_SELECTOR_AUDIT.md`):

### 1. Distribution Characterization vs. Prime-Power Distribution (Section 3.1)
- The Dirichlet series $\zeta(s) = \sum_{n\ge 1} n^{-s}$ and the logarithmic derivative $-\frac{\zeta'(s)}{\zeta(s)} = \sum_{n\ge 2}\Lambda(n)n^{-s}$ are strictly distinguished and never identified as a single scalar ray.
- The valid three-step deductive chain is recorded explicitly:
  1. The functional equation plus growth/support assumptions (Hamburger 1921; Burnol `1106.4749v2`, `math/0407443v3`; Báez-Duarte `math/0207237v1`) characterizes the $\zeta$-side distribution.
  2. The Euler product and logarithmic differentiation determine the von Mangoldt prime-power distribution $\mu_{\mathrm{pp}} = \sum_{n\ge 2}\Lambda(n)\delta_n$.
  3. Neither theorem selects a unique test kernel $F_0$.

### 2. Gaussian Uniqueness Scope (Section 3.2)
- The full self-Fourier subspace $\{\psi \in \mathcal S(\mathbb R) : \mathcal F\psi = \psi\}$ is infinite-dimensional, spanned by all even $4k$-th Hermite functions $\psi_{4k}(x) = H_{4k}(\sqrt{2\pi}\,x)e^{-\pi x^2}$ ($k \ge 0$).
- Accordingly, Gaussian uniqueness is scoped to the exact mathematical statement:
  > *The Gaussian $g_1(x) = e^{-\pi x^2}$ is uniquely selected within the specified positive heat-semigroup, harmonic-oscillator ground-state, or minimum-uncertainty class.*

### 3. Canonical Theta Certificate Parameter Consistency (Section 3.3)
- All narrative references to uncommitted cutoff values (`N=60` or `10^{-3400}`) have been removed.
- Every document and JSON artifact matches the committed 128-bit Arb certificate parameters:
  $$
  N_{\mathrm{cutoff}} = 15,
  \qquad
  R_{\mathrm{tail}}(15) \in \bigl[4.90944663560190599562356800150073399 \times 10^{-347} \pm 5.10 \times 10^{-383}\bigr].
  $$

### 4. Selector Trilemma Scope (Section 3.4)
- The six standard selector families audited in `TASK-TC-035` are classified as `SIX_STANDARD_SELECTOR_FAMILIES_AUDITED` (paper/Arb/literature audit).
- The Lean theorem `selector_trilemma_status` in `formal/RiemannScope/CanonicalSelectorAudit.lean` is classified as `CONDITIONAL_COMPLEMENT_SIGN_DICHOTOMY_LEAN_PROVED` (proving the conditional algebraic dichotomy from explicit sign hypotheses, not that all conceivable selectors are exhausted in Lean).

---

## Section C — Exact Theta Heat-Scaling Identities

Let
$$
g_t(x) := e^{-\pi t x^2} \quad (t > 0),
\qquad
\Theta_t(x,y) := g_t(x)g_t(y) = e^{-\pi t(x^2+y^2)},
$$
and define the spatial Euler operator and heat-scale generator:
$$
\mathcal E := x\partial_x + y\partial_y,
\qquad
\mathcal D := t\partial_t.
$$

### Exact Derivation
Writing $r := x^2 + y^2$, we have $\Theta_t(x,y) = e^{-\pi t r}$. Since $(x\partial_x + y\partial_y)r = 2(x^2+y^2) = 2r$:
1. **First-Order Identity**:
   $$
   \mathcal E\Theta_t = (2r)(-\pi t)e^{-\pi t r} = -2\pi t(x^2+y^2)\Theta_t = 2t\partial_t\Theta_t = 2\mathcal D\Theta_t.
   $$
2. **Second-Order Identity**:
   Applying $\mathcal E$ a second time (and using $[\partial_t, x\partial_x + y\partial_y] = 0$, so $\mathcal E\mathcal D = \mathcal D\mathcal E$):
   $$
   \mathcal E^2\Theta_t = 4\mathcal D^2\Theta_t = 4t\partial_t(t\partial_t\Theta_t) = 4t^2\partial_t^2\Theta_t + 4t\partial_t\Theta_t
   = \bigl(4\pi^2 t^2(x^2+y^2)^2 - 4\pi t(x^2+y^2)\bigr)\Theta_t.
   $$

Thus $\mathcal E^2$ applied to $\Theta_t$ is **not** a pure second derivative in $t$; it contains the mandatory first-order affine heat drift $+4t\partial_t\Theta_t$.

---

## Section D — Unique Heat-Drift Compensator Theorem

Consider the one-parameter family of monic second-order spatial scale operators without constant term:
$$
\mathcal L_c := \mathcal E(\mathcal E - c) = \mathcal E^2 - c\mathcal E,
\qquad c \in \mathbb R.
$$

### Theorem (Unique Heat-Drift Compensator)
On the two-dimensional Gaussian heat family $\Theta_t(x,y) = e^{-\pi t(x^2+y^2)}$:
$$
\mathcal L_c\Theta_t
= \mathcal E^2\Theta_t - c\mathcal E\Theta_t
= \bigl(4t^2\partial_t^2 + 4t\partial_t\bigr)\Theta_t - c\bigl(2t\partial_t\bigr)\Theta_t
= 4t^2\partial_t^2\Theta_t + (4 - 2c)t\partial_t\Theta_t.
$$
The coefficient of the first-order drift term $t\partial_t\Theta_t$ is $4 - 2c$, which vanishes if and only if
$$
\boxed{c = 2.}
$$
At $c = 2$, the unique heat-drift compensator is
$$
\boxed{
\mathcal L_{\mathrm{heat}} := \mathcal E(\mathcal E - 2) = 4(\mathcal D^2 - \mathcal D),
\qquad
\mathcal L_{\mathrm{heat}}\Theta_t = 4t^2\partial_t^2\Theta_t = 4\pi^2 t^2(x^2+y^2)^2\Theta_t.
}
$$

- **Uniqueness Scope**: $\mathcal L_{\mathrm{heat}} = \mathcal E(\mathcal E - 2)$ is unique within the class of monic quadratic polynomials in $\mathcal E$ without constant term that annihilate the first-order $t\partial_t$ heat drift on the degree-two Gaussian family $\Theta_t$.
- **Non-$c=2$ Controls**: For $c \in \{0, 1, -1, 3\}$, the residual drift coefficient $4 - 2c \in \{4, 2, 6, -2\}$ is strictly nonzero.
- **Classifications**: `HEAT_DRIFT_COMPENSATOR_UNIQUELY_FORCED` and `HEAT_DRIFT_COMPENSATOR_UNIQUE_BUT_NOT_MODULAR_SELECTOR`.

---

## Section E — Modular Covariant Derivative and Hessian

Let $f(t)$ transform under the modular inversion $t \mapsto 1/t$ with weight $w \in \mathbb R$:
$$
f(1/t) = t^w f(t) \qquad (t > 0).
$$
- For the 1D Jacobi theta function $\theta(t) = \sum_{n\in\mathbb Z} e^{-\pi t n^2}$, $\theta(1/t) = t^{1/2}\theta(t)$, so $w = 1/2$.
- For the 2D product theta function $\Theta(t) = \theta(t)^2 = \sum_{(m,n)\in\mathbb Z^2} e^{-\pi t(m^2+n^2)}$, $\Theta(1/t) = t\,\Theta(t)$, so $w = 1$.

### Weight Normalization and Covariant Derivative
Define the weight-normalized state:
$$
\widetilde f(t) := t^{w/2}f(t).
$$
Then under $t \mapsto 1/t$:
$$
\widetilde f(1/t) = t^{-w/2}f(1/t) = t^{-w/2}t^w f(t) = t^{w/2}f(t) = \widetilde f(t).
$$
Conjugating the logarithmic derivative $\mathcal D = t\partial_t$ by $t^{w/2}$ defines the **modular covariant derivative of weight $w$**:
$$
\nabla_w f(t) := t^{-w/2}\mathcal D\bigl(t^{w/2}f(t)\bigr) = \left(\mathcal D + \frac{w}{2}\right)f(t) = \left(t\partial_t + \frac{w}{2}\right)f(t).
$$
Since $\mathcal D(g(1/t)) = -(\mathcal Dg)(1/t)$, $\widetilde f(1/t) = \widetilde f(t)$ implies $(\mathcal D\widetilde f)(1/t) = -(\mathcal D\widetilde f)(t)$, and therefore at the self-dual point $t = 1$:
$$
\boxed{\nabla_w f(1) = 0.}
$$
The **modular Hessian of weight $w$** is the square of $\nabla_w$:
$$
\boxed{
\mathcal H_{\mathrm{mod},w} := \nabla_w^2 = \left(\mathcal D + \frac{w}{2}\right)^2 = \mathcal D^2 + w\mathcal D + \frac{w^2}{4}.
}
$$
Since $(\mathcal D^2\widetilde f)(1/t) = +(\mathcal D^2\widetilde f)(t)$, $\mathcal H_{\mathrm{mod},w}$ preserves modular weight $w$ and is symmetric under $t \leftrightarrow 1/t$.

---

## Section F — Exact Comparison Between Heat Compensator and Modular Hessian

For the 2D theta state of weight $w = 1$, using $\mathcal E = 2\mathcal D$ on $\Theta_t$:
- **Affine Heat-Drift Compensator**:
  $$
  \mathcal L_{\mathrm{heat}} = \mathcal E(\mathcal E - 2) = 4(\mathcal D^2 - \mathcal D) = 4t^2\partial_t^2.
  $$
- **Scaled Modular Hessian of Weight $w = 1$**:
  $$
  4\mathcal H_{\mathrm{mod},1} = 4\left(\mathcal D + \frac{1}{2}\right)^2 = 4\mathcal D^2 + 4\mathcal D + I = (\mathcal E + I)^2 = 4t^2\partial_t^2 + 8t\partial_t + I.
  $$

Subtracting the two operators yields the exact identity (formalized as `heat_and_modular_hessian_difference` in `formal/RiemannScope/ModularThetaConductorCurvature.lean`):
$$
\boxed{
4\mathcal H_{\mathrm{mod},1} - \mathcal L_{\mathrm{heat}} = 8\mathcal D + I = 4\mathcal E + I.
}
$$

### Mathematical Explanation of the Split
- $\mathcal L_{\mathrm{heat}} = 4t^2\partial_t^2$ is the **flat affine second derivative** with respect to the additive coordinate $t \in (0,\infty)$. It annihilates functions linear in $t$ (hence removes the first-order $\partial_t$ drift in $\mathcal E^2\Theta_t = 4t^2\partial_t^2\Theta_t + 4t\partial_t\Theta_t$), but it is **not** covariant under the multiplicative inversion $t \mapsto 1/t$.
- $\mathcal H_{\mathrm{mod},1} = (\mathcal D + 1/2)^2$ is the **logarithmic/modular Levi-Civita Hessian** with respect to the Haar coordinate $\log t$ twisted by the half-weight bundle $t^{1/2}$. It is invariant under $t \mapsto 1/t$ and self-adjoint under Fourier/Mellin inversion, but when expanded in $\partial_t$ it retains the nonzero connection terms $8t\partial_t + I$ and **does not** remove the affine heat drift.

This establishes all four Section 8 classifications:
- `HEAT_AND_MODULAR_HESSIANS_DIFFER_BY_FORCED_CONNECTION_TERMS`
- `MODULAR_HESSIAN_DOES_NOT_REMOVE_HEAT_DRIFT`
- `HEAT_COMPENSATOR_NOT_MODULARLY_FORCED`
- `MODULAR_HESSIAN_DIFFERS_FROM_HEAT_COMPENSATOR`

---

## Section G — Primary-Source Burnol/Weil Conductor Operator Audit

Primary sources inspected via `literature-search-arxiv`:
- Jean-François Burnol, *The Explicit Formula and the conductor operator*, `arXiv:math/9902080v1` (1999, 28 pp.): Sections 2.2–2.3, 3.1 (Theorem C1), 4.1–4.3 (Theorems D1–D3), 5.1–5.3 (Theorem E2), 8.2 (Theorem H2), and 10.1–10.2 (Theorems J1–J2).
- Jean-François Burnol, *Spectral Analysis of the local Commutator Operators*, `arXiv:math/9812012v1` (1998, 16 pp.).
- Jean-François Burnol, *Sur les Formules Explicites I: analyse invariante*, `arXiv:math/0101068v1` (2000, C. R. Acad. Sci. Paris 331, 423–428): Sections 2–3, Theorems 3.3 and 3.7.

### Critical Notation Clarification ($x$ and $y$ in Burnol's Formula)
In Burnol's physicist shorthand (`math/9902080v1` Eq. (1), p. 4; `math/0101068v1` p. 3):
$$
H_\nu = \log|x|_\nu + \log|y|_\nu,
$$
$x$ and $y$ are **1D Fourier-conjugate variables on the same local field $K_\nu$**, meaning:
$$
A := M_{\log|x|_\nu},
\qquad
B := \mathcal F M_{\log|y|_\nu}\mathcal F^{-1},
\qquad
H_\nu := A + B \quad \text{on } L^2(K_\nu, dx).
$$
In particular, $y$ is **not** a second independent spatial coordinate in a 2D kernel $F_0(x_1, x_2)$.

### Dense Domain and Invariant Core
- **Initial Domain**: $\mathcal S_0(K_\nu) = C_c^\infty(K_\nu \setminus \{0\})$ (smooth functions compactly supported away from both $0$ and $\infty$).
- **Invariant Schwartz–Mellin Core** (`math/9902080v1` Theorem J1):
  $$
  \Delta(K_\nu) := \bigl\{\phi \in L^2(K_\nu, dx) : \text{its multiplicative Fourier transform belongs to } \mathcal S(\widehat{K_\nu^\times})\bigr\}.
  $$
  For $K_\nu = \mathbb R$, $\Delta(\mathbb R)$ consists of functions $\phi(x) = |x|^{-1/2}F(\log|x|)$ (split into even and odd parities) with $F \in \mathcal S(\mathbb R)$. By Burnol's Theorems E2 and J2 (`math/9902080v1`), $A$, $B$, and $H_\nu = A + B$ map $\Delta(K_\nu)$ into $\Delta(K_\nu)$ and are essentially self-adjoint on both $\mathcal S_0(K_\nu)$ and $\Delta(K_\nu)$.

### Required 5-Row Primary-Source Object Comparison Table (Section 9)

| Object | Hilbert / Test Space | Exact Definition | Self-Adjoint? | Fourier-Invariant? | Dilation Relation | Explicit-Formula Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Multiplication by $\log\|x\|_\nu$ ($A$)** | Dense domain $\mathcal S_0(K_\nu)$ or $\Delta(K_\nu) \subset L^2(K_\nu, dx)$ | $(A\phi)(x) = \log(\|x\|_\nu)\,\phi(x)$ | YES (essentially self-adjoint on $\mathcal S_0$ and $\Delta$) | NO ($\mathcal F A\mathcal F^{-1} = B \neq A$) | $U(\lambda)AU(\lambda)^{-1} = A - (\log\|\lambda\|_\nu)I$; $[\mathcal A, A] = I$ | Position-space logarithmic multiplier; generates $d/ds$ on character space |
| **Fourier-conjugate log operator ($B = \mathcal F A\mathcal F^{-1}$)** | Dense domain $\mathcal S_0(K_\nu)$ or $\Delta(K_\nu) \subset L^2(K_\nu, dx)$ | $B = \mathcal F M_{\log\|y\|_\nu}\mathcal F^{-1} = -\Gamma A\Gamma^{-1}$ | YES (unitarily conjugate to $A$ via $\mathcal F$) | NO ($\mathcal F B\mathcal F^{-1} = A \neq B$) | $U(\lambda)BU(\lambda)^{-1} = B + (\log\|\lambda\|_\nu)I$; $[\mathcal A, B] = -I$ | Additive convolution with Haran–Burnol kernel $G_\nu = \mathcal F(-\log\|y\|_\nu)$ |
| **Local conductor operator ($H_\nu = \mathcal C_\nu = A + B$)** | Invariant core $\Delta(K_\nu) \subset L^2(K_\nu, dx)$ (`math/9902080v1` Thm E2, J2) | $H_\nu = M_{\log\|\cdot\|_\nu} + \mathcal F M_{\log\|\cdot\|_\nu}\mathcal F^{-1}$; spectral multiplier $\frac{d}{ds}\log\Gamma_\nu(\chi_\nu, s)$ on $\operatorname{Re}(s)=1/2$ | YES (essentially self-adjoint on $\mathcal S_0$ and $\Delta$, bounded below) | YES ($\mathcal F H_\nu\mathcal F^{-1} = H_\nu$ and $\mathcal I H_\nu\mathcal I^{-1} = H_\nu$) | Completely dilation-invariant: $U(\lambda)H_\nu U(\lambda)^{-1} = H_\nu$; $[\mathcal A, H_\nu] = 0$ | Local Weil functional $W_\nu(g;\chi) = H_\nu(g_{\nu;\chi})(1)$ at place $\nu$ |
| **Global sum over places of local conductor evaluations** | $g \in C_c^\infty((0,\infty))$ lifted to $g_{\nu;\chi}(t) = g(\|t\|_\nu)\chi_\nu^{-1}(t)$ | $W(g;\chi) = \sum_\nu H_\nu(g_{\nu;\chi})(1)$ (`math/0101068v1` Thm 3.3) | Linear scalar functional (evaluation at $t=1$), not a Hilbert-space operator | Invariant under multiplicative inversion $g(u) \mapsto u^{-1}g(u^{-1})$ | Multiplicative shift $g_\lambda(u) = g(u/\lambda)$ multiplies Mellin integrand by $\lambda^{s-1/2}$ | Equals the full arithmetic side (prime-power + Archimedean local terms) of Weil's explicit formula |
| **Global explicit-formula distribution ($\mathcal W_\zeta$)** | Admissible test space $C_c^\infty(\mathbb R_+^\times)$ or $\Delta(\mathbb R_+^\times)$ | $\langle \mathcal W_\zeta, g\rangle = \sum_\rho \widehat g(\rho - 1/2) - (\widehat g(-1/2) + \widehat g(1/2)) = -\sum_\nu H_\nu(g_\nu)(1)$ | Distribution in $\mathcal D'(\mathbb R_+^\times)$; induces Hermitian Weil form $Z(g * g^*)$ | Symmetric under $g^*(u) = u^{-1}\overline{g(u^{-1})}$ | Dilation shifts zero-sum phases $\lambda^{\rho - 1/2}$ | Bridges global zero-pole sum to the sum over all places $\nu$ of local conductor evaluations |

---

## Section H — Conductor-Dilation Commutator Audit

On $L^2(\mathbb R, dx)$, let $(U(\lambda)\phi)(x) := \lambda^{-1/2}\phi(x/\lambda)$ ($\lambda > 0$) be the unitary dilation group, with infinitesimal generator
$$
\mathcal A := -\left.\frac{d}{d\lambda}\right|_{\lambda=1} U(\lambda) = x\partial_x + \frac{1}{2}I = \mathcal E_{\mathrm{1D}} + \frac{1}{2}I.
$$
On the common invariant core $\Delta(\mathbb R)$ (`math/9902080v1` Theorem J1):

1. **Position Logarithmic Multiplier $A = M_{\log|x|}$**:
   $$
   \bigl(U(\lambda)AU(\lambda)^{-1}\phi\bigr)(x) = \log|x/\lambda|\,\phi(x) = \bigl((A - (\log\lambda)I)\phi\bigr)(x)
   \implies
   [\mathcal A, A]\phi = \phi, \quad [\mathcal A, A] = I.
   $$
2. **Momentum Logarithmic Multiplier $B = \mathcal F A\mathcal F^{-1}$**:
   Since $\mathcal F U(\lambda) = U(\lambda^{-1})\mathcal F$:
   $$
   U(\lambda)BU(\lambda)^{-1} = \mathcal F U(\lambda^{-1})A U(\lambda)\mathcal F^{-1} = \mathcal F\bigl(A + (\log\lambda)I\bigr)\mathcal F^{-1} = B + (\log\lambda)I
   \implies
   [\mathcal A, B]\phi = -\phi, \quad [\mathcal A, B] = -I.
   $$
3. **Conductor Operator $\mathcal C = H_{\mathbb R} = A + B$**:
   Adding the two commutators on $\Delta(\mathbb R)$ (formalized algebraically as `dilation_conductor_commutator_cancellation` in `formal/RiemannScope/ModularThetaConductorCurvature.lean`):
   $$
   \boxed{
   [\mathcal A, \mathcal C] = [\mathcal A, A] + [\mathcal A, B] = I - I = 0,
   \qquad
   [\mathcal A, [\mathcal A, \mathcal C]] = 0,
   \qquad
   [\mathcal E, \mathcal C] = 0.
   }
   $$

### Consequence for Grade-Transport Curvature
Because $U(\tau^{-\eta K})\mathcal C = \mathcal C U(\tau^{-\eta K})$, the conductor $\mathcal C$ is already a function of the dilation generator $\mathcal A$ on each parity sector ($\mathcal C = \psi_0(\mathcal A)$ on $\Delta(\mathbb R)$, where $\psi_0(s) = \frac{d}{ds}\log(\pi^{-s/2}\Gamma(s/2))$). Therefore:
- Every commutator $[\mathcal E, \mathcal C]$ and $[\mathcal E, [\mathcal E, \mathcal C]]$ vanishes identically on $\Delta$.
- Applying $\mathcal C$ before or after grade transport $U(\tau^{-\eta K})$ merely replaces the state $\Phi$ by the fixed state $\mathcal C\Phi$ without introducing any new non-commuting grade-curvature operator.
- **Classifications**: `CONDUCTOR_COMMUTES_WITH_DILATION` and `CONDUCTOR_DILATION_COMMUTATION_REMOVES_NEW_GRADE_SIGNAL`.

---

## Section I — Operator-Selector Axiom System and Uniqueness / Non-Uniqueness Result

We test whether a second-order operator $\mathcal O$ in the algebra generated by $\{I, \mathcal E, \mathcal E^2, \mathcal C, \frac{1}{2}(\mathcal C\mathcal E + \mathcal E\mathcal C), [\mathcal E, \mathcal C], [\mathcal E, [\mathcal E, \mathcal C]]\}$ is uniquely selected (up to scalar multiple) by the eight candidate axioms in Section 11:

1. **Fourier Invariance**: $\mathcal F\mathcal O\mathcal F^{-1} = \mathcal O$;
2. **Self-Adjointness on $\Delta$**: $\mathcal O^* = \mathcal O$ on $\Delta$;
3. **Compatibility with Theta Modular Inversion**: $t \mapsto 1/t$ of weight $w = 1$ ($\mathcal E \mapsto -\mathcal E - 2I$);
4. **Degree-Two Heat Covariance**: exact removal of the first-order $t\partial_t$ drift on $\Theta_t$;
5. **Second Order in Scale Differentiation**: coefficient $c_2$ of $\mathcal E^2$ is nonzero;
6. **No Fitted Scalar Coefficients**;
7. **Compatibility with Completed-Zeta Archimedean Factor**;
8. **Non-Scalar Action**.

### Exact Algebraic Resolution of the Axiom System
Since $[\mathcal E, \mathcal C] = 0$ and $[\mathcal E, [\mathcal E, \mathcal C]] = 0$ on $\Delta$, the general degree-$\le 2$ ansatz reduces to:
$$
\mathcal O = c_2\mathcal E^2 + c_1\mathcal E + c_0 I + c_3\mathcal C + c_4\mathcal C\mathcal E + c_5\mathcal C^2.
$$
Writing $\mathcal A_2 := \mathcal E + I = 2(\mathcal D + 1/2)$ (so $\mathcal E = \mathcal A_2 - I$), under Fourier/modular inversion ($\mathcal A_2 \mapsto -\mathcal A_2$ and $\mathcal C \mapsto \mathcal C$), Axioms 1–3 require $\mathcal O$ to be even in $\mathcal A_2$, selecting on the pure scale sector the **two-parameter invariant subspace**:
$$
b_0 I + b_2\mathcal A_2^2 = b_0 I + b_2(\mathcal E + I)^2 = b_2\mathcal E^2 + 2b_2\mathcal E + (b_0 + b_2)I,
$$
which forces:
$$
c_2 = b_2,
\qquad
c_1 = 2c_2,
\qquad
c_0 = c_2 + b_0 \quad (\text{with independent scalar } b_0),
\qquad
c_4 = 0.
$$
Imposing vanishing on the dilation-invariant mode $\ker(\mathcal E + I)$ ($b_0 = 0$) restricts this two-parameter subspace to the single projective **modular Hessian ray**:
$$
\mathbb R^\times \cdot (\mathcal E + I)^2 = \mathbb R^\times \cdot 4\mathcal H_{\mathrm{mod},1} \qquad (c_0 = c_2).
$$
Conversely, Axiom 4 (exact removal of the $t\partial_t$ heat drift in $\mathcal E^2\Theta_t = 4t^2\partial_t^2\Theta_t + 4t\partial_t\Theta_t$) requires:
$$
c_1 = -2c_2,
\qquad
c_0 = 0,
$$
selecting the **heat-drift compensator ray**:
$$
\mathbb R^\times \cdot \mathcal E(\mathcal E - 2) = \mathbb R^\times \cdot \mathcal L_{\mathrm{heat}}.
$$
Imposing both constraints simultaneously gives (independently of the scalar offset $b_0$, and formalized as `heat_and_modular_hessian_incompatibility` in `formal/RiemannScope/ModularThetaConductorCurvature.lean`):
$$
2c_2 = c_1 = -2c_2 \implies 4c_2 = 0 \implies c_2 = 0, \quad c_1 = 0 \quad (\text{and } c_0 = b_0 = 0),
$$
which violates Axiom 5 ($c_2 \neq 0$). Thus the joint axiom system has **no nonzero second-order solution**; instead it splits cleanly into two distinct 1D projective rays (`Ray A`: $\mathcal L_{\mathrm{heat}} = \mathcal E(\mathcal E - 2)$ satisfying Axioms 4, 5, 6, 8; `Ray B`: $4\mathcal H_{\mathrm{mod},1} = (\mathcal E + I)^2$ satisfying Axioms 1, 2, 3, 5, 6, 8 at $b_0 = 0$).

---

## Section J — Linear vs Quadratic Functional Firewall

A strict firewall is enforced between linear explicit-formula evaluations and quadratic variance determinants:

1. **Linear Functional**:
   $$
   \mathscr L(\Phi) := \langle \mathcal W_\zeta, \mathcal O\Phi\rangle = \sum_\rho m_\rho \widehat{(\mathcal O\Phi)}(\rho - 1/2) - \text{poles}.
   $$
   - **Spectral Structure**: Single-zero linear sum (`SIGNED_SINGLE_ZERO_SUM`).
   - **Sign Property**: Has no Cauchy–Schwarz variance determinant structure; oscillatory zero phases $\gamma_\rho$ make individual terms signed.

2. **Quadratic Variance Functional**:
   $$
   \mathscr Q(\Phi) := \langle \mathcal W, \Phi\rangle\langle \mathcal W, \mathcal O\Phi\rangle - \langle \mathcal W, \mathcal E\Phi\rangle^2.
   $$
   - **Arithmetic Prime-Only Property**: When $\mathcal W = \mu_{\mathrm{pp}} \times \mu_{\mathrm{pp}}$ (positive measure) and $\mathcal O = \mathcal L_{\mathrm{heat}} = \mathcal E(\mathcal E - 2)$, $\mathscr Q(\Theta_t) = 4\pi^2 t^2(M_0 M_2 - M_1^2) \ge 0$ by Cauchy–Schwarz.
   - **Completed Spectral Structure**: When $\mathcal W = \mathcal W_{\mathrm{comp}}$ is the completed explicit-formula functional, $\mathscr Q(\Phi_t)$ is a **product of two global zero sums** and therefore expands over all ordered zero pairs $(\rho, \sigma)$ (`UNRESTRICTED_DOUBLE_ZERO_SUM`).

Positivity of the quadratic prime-only variance $\mathscr Q_{\mathrm{prime}}$ can **never** be transferred to the linear single-zero sum $\mathscr L$ (`LINEAR_QUADRATIC_FUNCTIONAL_CONFLATION` is explicitly blocked).

---

## Section K — Prime-Only Drift-Compensated Variance Certificate

For the positive prime-power product weight $w_{m,n} = \Lambda(m)\Lambda(n) \ge 0$ and $r_{m,n} = m^2 + n^2$, define the heat-weighted moments:
$$
M_k(t) := \sum_{m,n \ge 2} w_{m,n}\,r_{m,n}^k\,e^{-\pi t r_{m,n}} \qquad (k = 0, 1, 2).
$$
Using $\mathcal E\Theta_t = -2\pi t r\,\Theta_t$ and $\mathcal L_{\mathrm{heat}}\Theta_t = \mathcal E(\mathcal E - 2)\Theta_t = 4\pi^2 t^2 r^2\Theta_t$, the prime-only Euler moments are:
$$
A_0(t) = M_0(t),
\qquad
A_1(t) = \langle \mu_{\mathrm{pp}}^2, \mathcal E\Theta_t\rangle = -2\pi t\,M_1(t),
\qquad
A_{2,\mathrm{cov}}(t) = \langle \mu_{\mathrm{pp}}^2, \mathcal L_{\mathrm{heat}}\Theta_t\rangle = 4\pi^2 t^2 M_2(t).
$$
Therefore, the prime-only drift-compensated curvature satisfies the exact Bernstein / Cauchy–Schwarz variance identity (formalized as `covariant_prime_variance_identity` and `covariant_prime_variance_nonneg` in `formal/RiemannScope/ModularThetaConductorCurvature.lean`):
$$
\boxed{
\mathfrak C_{\mathrm{prime}}^{\mathrm{cov}}(t)
:= A_0(t)A_{2,\mathrm{cov}}(t) - A_1(t)^2
= 4\pi^2 t^2\bigl(M_0(t)M_2(t) - M_1(t)^2\bigr)
= 2\pi^2 t^2 \sum_{m,n,m',n'\ge 2} w_{m,n}w_{m',n'}(r_{m,n} - r_{m',n'})^2 e^{-\pi t(r_{m,n}+r_{m',n'})} > 0.
}
$$

### 128-Bit Arb Certified Enclosure at $t = 1$ ($N_{\mathrm{cutoff}} = 15$ plus Infinite Lattice Tail)
- $A_0(1) \in [5.84305936627826185128361183211138217 \times 10^{-12} \pm 5.86 \times 10^{-48}]$
- $A_1(1) \in [-2.93704285764878119747267934509396966 \times 10^{-10} \pm 1.52 \times 10^{-46}]$
- $A_{2,\mathrm{cov}}(1) \in [1.476319478655087792054211268220773819 \times 10^{-8} \pm 7.94 \times 10^{-45}]$
- $A_{2,\mathrm{uncomp}}(1) \in [1.41757862150211216810475768131889443 \times 10^{-8} \pm 5.02 \times 10^{-44}]$
- **Uncompensated Euler curvature**:
  $$
  \mathfrak C_{\mathrm{arith}}(\Theta_1) = A_0(1)A_{2,\mathrm{uncomp}}(1) - A_1(1)^2 \in \bigl[-3.432247058619752688206766472100430 \times 10^{-21} \pm 3.80 \times 10^{-55}\bigr] < 0.
  $$
- **Drift-compensated prime variance (finite $N \le 15$ and full infinite lattice $N = \infty$ with tail bound $\le 4.91 \times 10^{-347}$)**:
  $$
  \boxed{
  \mathfrak C_{\mathrm{prime}}^{\mathrm{cov}}(1)
  \in \bigl[+1.6097089323851242452337142816 \times 10^{-26} \pm 3.98 \times 10^{-55}\bigr] > 0.
  }
  $$
- **Status**: `PRIME_ONLY_COVARIANT_VARIANCE_POSITIVE_CERTIFIED` (explicitly labeled as a **prime-only control theorem**, NOT a completed-zeta constraint).

---

## Section L — No-Contradiction Sign Firewall

A mathematical contradiction between an arithmetic evaluation $\mathscr A_{\mathrm{arith}}$ and a spectral evaluation $\mathscr A_{\mathrm{spec}}$ of the **same** completed functional $\mathscr A_{\mathrm{arith}} = \mathscr A_{\mathrm{spec}}$ requires an **incompatible sign pair**:
1. $\mathscr A_{\mathrm{arith}} = 0$ vs. $\mathscr A_{\mathrm{spec}} > 0$;
2. $\mathscr A_{\mathrm{arith}} \le 0$ vs. $\mathscr A_{\mathrm{spec}} > 0$; or
3. $\mathscr A_{\mathrm{arith}} = C$ vs. $\mathscr A_{\mathrm{spec}} = C + \Delta$ with $\Delta > 0$.

When $\mathcal E^2$ is replaced by $\mathcal L_{\mathrm{heat}} = \mathcal E(\mathcal E - 2)$, the prime-only curvature flips sign from $\mathfrak C_{\mathrm{arith}}(\Theta_1) < 0$ to $\mathfrak C_{\mathrm{prime}}^{\mathrm{cov}}(1) > 0$. As proved formally in `arithmetic_sign_and_spectral_sign_no_contradiction` (`formal/RiemannScope/ModularThetaConductorCurvature.lean`), having $\mathscr A_{\mathrm{arith}} \ge 0$ and $\mathscr A_{\mathrm{spec}} \ge 0$ is **logically consistent** ($\mathscr A_{\mathrm{arith}} = \mathscr A_{\mathrm{spec}} = v \ge 0$) and produces **no contradiction**.
- **Classification**: `POSITIVE_ARITHMETIC_VARIANCE_HAS_NO_CONTRADICTORY_SPECTRAL_LAW`.

---

## Section M — Completed Theta–Conductor Functional and `TASK-TC-036R` Pole-Regularization Repair

### 1. Diagnosis of the Unshifted Regularizer Defect (`UNSHIFTED_REGULARIZER_DOES_NOT_ANNIHILATE_POLES`)
On the weight-normalized 1D theta Gaussian state
$$
\widetilde g_t(u) := t^{1/4}g_t(u) = t^{1/4}e^{-\pi t u^2} \qquad (t > 0),
$$
its raw Mellin transform is
$$
\mathcal M[\widetilde g_t](s) := \int_0^\infty \widetilde g_t(u)\,u^{s-1}\,du = \frac{1}{2}\pi^{-s/2}\Gamma(s/2)\,t^{1/4 - s/2} = \frac{1}{2}\pi^{-(z+1/2)/2}\Gamma\!\left(\frac{z+1/2}{2}\right)t^{-z/2},
\qquad z = s - \frac{1}{2}.
$$
Therefore $\mathcal D = t\partial_t$ acts on $\mathcal M[\widetilde g_t](s)$ by multiplication by
$$
\lambda(s) = \frac{1}{4} - \frac{s}{2} = -\frac{z}{2}.
$$
In `TASK-TC-036`, the unshifted operator $\mathcal D(\mathcal D - \frac{1}{2})$ (which applies to the unnormalized factor $t^{-s/2}$ rather than the weight-$1/2$ normalized factor $t^{1/4 - s/2}$) was mistakenly applied to $\widetilde g_t$. On $t^{1/4 - s/2}$, $\mathcal D(\mathcal D - \frac{1}{2})$ acts by the multiplier (formalized as `unshifted_regularizer_mellin_defect`):
$$
\left(\frac{1}{4} - \frac{s}{2}\right)\left(\frac{1}{4} - \frac{s}{2} - \frac{1}{2}\right) = \left(\frac{1}{4} - \frac{s}{2}\right)\left(-\frac{1}{4} - \frac{s}{2}\right) = \frac{s^2}{4} - \frac{1}{16},
$$
which equals $-\frac{1}{16} \neq 0$ at $s = 0$ and $+\frac{3}{16} \neq 0$ at $s = 1$, and in spatial coordinates ($r := \pi t u^2$) produces
$$
\mathcal D\left(\mathcal D - \frac{1}{2}\right)\widetilde g_t(u) = t^{1/4}\left(r^2 - r - \frac{1}{16}\right)e^{-r},
$$
whose value at $u = 0$ is $-\frac{1}{16}t^{1/4} \neq 0$ and whose half-line integral is $+\frac{3}{32}t^{-1/4} \neq 0$. Thus $\mathcal D(\mathcal D - \frac{1}{2})$ fails to annihilate either endpoint mode on $\widetilde g_t$.

### 2. Exact Pole-Regularizer Repair (`CORRECTED_POLE_REGULARIZER_D_SQUARED_MINUS_ONE_SIXTEENTH`)
Because the origin term $\widetilde g_t(0) = t^{1/4}$ has $\mathcal D$-eigenvalue $+1/4$ and the zero-frequency integral $\int_{\mathbb R}\widetilde g_t(u)\,du = t^{-1/4}$ has $\mathcal D$-eigenvalue $-1/4$, the unique monic second-order polynomial in $\mathcal D$ that annihilates both quarter-power modes on $\widetilde g_t(u) = t^{1/4}e^{-\pi t u^2}$ is (formalized as `corrected_pole_regularizer_mellin_identity`, `corrected_pole_regularizer_annihilates_quarter_powers`, and `corrected_pole_regularizer_spatial_jet`):
$$
\boxed{
\mathcal P_{\mathrm{reg}}(\mathcal D) := \left(\mathcal D - \frac{1}{4}\right)\left(\mathcal D + \frac{1}{4}\right) = \mathcal D^2 - \frac{1}{16}.
}
$$
On $\mathcal M[\widetilde g_t](s) \propto t^{1/4 - s/2}$, $\mathcal P_{\mathrm{reg}}(\mathcal D)$ multiplies by:
$$
\left(\frac{1}{4} - \frac{s}{2}\right)^2 - \frac{1}{16} = \frac{1}{4}s(s - 1) = \frac{1}{4}\left(z^2 - \frac{1}{4}\right),
\qquad z = s - \frac{1}{2},
$$
which vanishes at both $s = 0$ ($z = -1/2$) and $s = 1$ ($z = +1/2$), matching Riemann's completed factor $\xi(s) = \frac{1}{2}s(s - 1)\pi^{-s/2}\Gamma(s/2)\zeta(s)$.

### 3. Spatial Formula and Domain Verification for the Repaired State $\Phi_t$
Applying $\mathcal P_{\mathrm{reg}}(\mathcal D) = \mathcal D^2 - \frac{1}{16}$ to $\widetilde g_t(u) = t^{1/4}e^{-r}$ ($r = \pi t u^2$) yields the repaired state:
$$
\boxed{
\Phi_t(u) := \left(\mathcal D^2 - \frac{1}{16}\right)\!\bigl(t^{1/4}e^{-\pi t u^2}\bigr)
= t^{1/4}\left(r^2 - \frac{3}{2}r\right)e^{-r}
= \pi t^{5/4}u^2\left(\pi t u^2 - \frac{3}{2}\right)e^{-\pi t u^2}.
}
$$
We verify all endpoint, integral, and Mellin domain conditions explicitly:
1. **Vanishing at the Origin ($u = 0$)**: $\Phi_t(0) = 0$ and $\Phi_t'(0) = 0$ (in fact $\Phi_t(u) = -\frac{3}{2}\pi t^{5/4}u^2 + O(u^4)$ as $u \to 0$).
2. **Vanishing Half-Line Integral**:
   $$
   \int_0^\infty \Phi_t(u)\,du = \frac{t^{1/4}}{2\sqrt{\pi t}}\int_0^\infty \left(r^{3/2} - \frac{3}{2}r^{1/2}\right)e^{-r}\,dr = \frac{t^{-1/4}}{2\sqrt{\pi}}\left(\Gamma\!\left(\frac{5}{2}\right) - \frac{3}{2}\Gamma\!\left(\frac{3}{2}\right)\right) = 0.
   $$
3. **Analytic Mellin Transform and Pole Behavior at $s = 0, 1$**:
   Lifting $\Phi_t$ to the multiplicative half-density $(J\Phi_t)(u) := u^{1/2}\Phi_t(u) \in L^2(\mathbb R_+^\times, du/u)$, its centered Mellin transform $\widehat{J\Phi_t}(z) := \int_0^\infty (J\Phi_t)(u)u^z\,\frac{du}{u} = \mathcal M[\Phi_t](s)$ ($s = 1/2 + z$) is:
   $$
   \widehat{J\Phi_t}(z) = \mathcal M[\Phi_t](s) = \frac{1}{8}s(s - 1)\pi^{-s/2}\Gamma(s/2)\,t^{1/4 - s/2},
   $$
   which is holomorphic on $\operatorname{Re}(s) > -2$ ($\operatorname{Re}(z) > -5/2$). Because $\Gamma(s/2) = \frac{2}{s} + O(1)$ has a simple pole at $s = 0$, the single factor $\frac{1}{4}s(s-1)$ cancels the $\Gamma$-pole at $s = 0$ to leave the finite value $\mathcal M[\Phi_t](0) = -\frac{1}{4}t^{1/4}$ while vanishing at $s = 1$ ($\mathcal M[\Phi_t](1) = 0$). Applying $\mathcal P_{\mathrm{reg}}(\mathcal D)$ a second time produces the squared pole-vanishing state (spatial polynomial corrected in `TASK-TC-042` from the `TC-036R` display typo $r^4 - 6r^3 + \frac{45}{8}r^2 - \frac{3}{8}r$)
   $$
   \Phi_t^{(2)}(u) := \left(\mathcal D^2 - \frac{1}{16}\right)^2\widetilde g_t(u) = t^{1/4}\left(r^4 - 7r^3 + \frac{41}{4}r^2 - \frac{9}{4}r\right)e^{-r},
   $$
   whose Mellin transform $\mathcal M[\Phi_t^{(2)}](s) = \frac{1}{32}s^2(s-1)^2\pi^{-s/2}\Gamma(s/2)t^{1/4-s/2}$ vanishes at **both** $s = 0$ and $s = 1$: $\mathcal M[\Phi_t^{(2)}](0) = \mathcal M[\Phi_t^{(2)}](1) = 0$, so $W_{\mathrm{pole}}(J\Phi_t^{(2)}) = 0$.

### 4. Explicit Background Terms of the Repaired Completed Functional
For $\Psi = J\Phi_t$ (or $\Psi = J\Phi_t^{(2)}$), the zero-independent completed linear explicit-formula functional is
$$
W_{\mathrm{comp}}(\Psi) := W_{\mathrm{pole}}(\Psi) - \sum_{p} H_p(\Psi_p)(1) - H_\infty(\Psi_\infty)(1),
$$
where every background term converges absolutely and is explicitly included:
1. **Prime-Power Terms ($p < \infty$)**:
   $$
   W_{\mathrm{prim}}(J\Phi_t) = -\sum_{p} H_p(\Phi_{t,p})(1) = -\sum_{n\ge 2} \Lambda(n)\bigl(\Phi_t(n) + n^{-1}\Phi_t(n^{-1})\bigr).
   $$
   Because $\Phi_t(n^{-1}) = O(n^{-2})$ as $n \to \infty$, the reflected prime-power sum $\sum_{n\ge 2}\Lambda(n)n^{-1}\Phi_t(n^{-1}) = O(\sum_{n\ge 2}\Lambda(n)n^{-3})$ converges absolutely.
2. **Pole Terms at $s = 0$ and $s = 1$ ($z = \mp 1/2$)**:
   $$
   W_{\mathrm{pole}}(J\Phi_t) = \widehat{J\Phi_t}(-1/2) + \widehat{J\Phi_t}(1/2) = \mathcal M[\Phi_t](0) + \mathcal M[\Phi_t](1) = -\frac{1}{4}t^{1/4} + 0,
   \qquad
   W_{\mathrm{pole}}(J\Phi_t^{(2)}) = 0 + 0 = 0.
   $$
3. **Trivial-Zero / Archimedean Gamma & Local Real Conductor Term ($\nu = \infty$)**:
   By Burnol (`math/9902080v1` Theorem D3), the local conductor evaluation $-H_\infty(\Phi_{t,\infty})(1)$ encodes $\pi^{-s/2}\Gamma(s/2)$ and all trivial zeros $s = -2m$ ($m \ge 1$):
   $$
   W_\infty(J\Phi_t) = -H_\infty(\Phi_{t,\infty})(1) = \bigl(\log(2\pi) + \gamma_E\bigr)\Phi_t(1) + \int_{1/2}^\infty \frac{\Phi_t(1/u)u - \Phi_t(1)}{|1 - u|}\frac{du}{2u} + \int_{-\infty}^{1/2} \frac{\Phi_t(1/|u|)|u|}{|1 - u|}\frac{du}{2|u|}.
   $$
4. **Normalization Terms**: The multiplicative half-density lift $(J\Phi_t)(u) = u^{1/2}\Phi_t(u)$ centering the Mellin transform at $\operatorname{Re}(s) = 1/2$.
5. **Regularization at $0$ and $\infty$**: $\mathcal P_{\mathrm{reg}}(\mathcal D) = \mathcal D^2 - \frac{1}{16}$ (and $\mathcal P_{\mathrm{reg}}(\mathcal D)^2$) kills both quarter-power modes $t^{\pm 1/4}$ at $u = 0$ and $u = \infty$, with rapid vertical decay $|\widehat{J\Phi_t}(\delta + i\gamma)| \ll |\gamma|^A e^{-\pi|\gamma|/4}$.

From $W_{\mathrm{comp}}$, using $2\mathcal D\,(t^{1/4 - s/2}) = (1/2 - s)t^{1/4 - s/2} = -z\,t^{1/4 - s/2}$ and $\mathcal L_{\mathrm{heat}} = 4(\mathcal D^2 - \mathcal D) = 2\mathcal D(2\mathcal D - 2)$, the completed linear and quadratic functionals are:
$$
\mathscr L_{\Theta,\mathcal C}^{\mathrm{cov}}(t) := W_{\mathrm{comp}}(\mathcal L_{\mathrm{heat}}J\Phi_t),
\qquad
\mathscr A_{\Theta,\mathcal C}^{\mathrm{cov}}(t) := W_{\mathrm{comp}}(J\Phi_t^{(2)})W_{\mathrm{comp}}(\mathcal L_{\mathrm{heat}}J\Phi_t^{(2)}) - W_{\mathrm{comp}}(2\mathcal D J\Phi_t^{(2)})^2.
$$

---

## Section N — Complete Spectral Representation and Zero-Pairing Audit on the Repaired State

By the Riemann–Weil–Burnol explicit formula (`math/9902080v1` Theorem C1; `math/0101068v1` Theorem 3.3), for $\Psi = J\Phi_t^{(2)}$:
$$
W_{\mathrm{comp}}(\Psi) = \sum_\rho m_\rho\,\widehat\Psi(z_\rho),
\qquad
z_\rho := \rho - \frac{1}{2} = \delta_\rho + i\gamma_\rho.
$$
Since $\widehat{(2\mathcal D\,\Psi)}(z) = -z\,\widehat\Psi(z)$ and $\widehat{(\mathcal L_{\mathrm{heat}}\Psi)}(z) = z(z + 2)\widehat\Psi(z)$:

1. **Complete Spectral Transfer of the Linear Functional**:
   $$
   \mathscr L_{\Theta,\mathcal C}^{\mathrm{cov}}(t) = \sum_\rho m_\rho\,z_\rho(z_\rho + 2)\,\widehat{J\Phi_t}(z_\rho) - W_{\mathrm{pole}}(\mathcal L_{\mathrm{heat}}J\Phi_t)
   \qquad (\texttt{SIGNED\_SINGLE\_ZERO\_SUM}).
   $$
2. **Complete Spectral Transfer of the Quadratic Variance Functional**:
   $$
   \mathscr A_{\Theta,\mathcal C}^{\mathrm{cov}}(t)
   = \frac{1}{2}\sum_{\rho,\sigma} m_\rho m_\sigma\,\widehat{J\Phi_t^{(2)}}(z_\rho)\widehat{J\Phi_t^{(2)}}(z_\sigma)\bigl[(z_\rho - z_\sigma)^2 + 2(z_\rho + z_\sigma)\bigr]
   \qquad (\texttt{UNRESTRICTED\_DOUBLE\_ZERO\_SUM}).
   $$

### Natural Zero-Pairing Audit (Section 17)
We check how the spectral kernel $(z_\rho - z_\sigma)^2 + 2(z_\rho + z_\sigma)$ behaves on each pair type:
- **Conjugate pair $(\rho, \bar\rho)$** ($z_\rho = \delta_\rho + i\gamma_\rho$, $z_{\bar\rho} = \delta_\rho - i\gamma_\rho$):
  $$
  (z_\rho - z_{\bar\rho})^2 = (2i\gamma_\rho)^2 = -4\gamma_\rho^2 < 0,
  \qquad
  2(z_\rho + z_{\bar\rho}) = 4\delta_\rho.
  $$
  This is dominated by the negative ordinate square $-4\gamma_\rho^2$.
- **Reflection pair $(\rho, 1 - \bar\rho)$** ($z_\rho = \delta_\rho + i\gamma_\rho$, $z_{1-\bar\rho} = -\delta_\rho + i\gamma_\rho$):
  $$
  (z_\rho - z_{1-\bar\rho})^2 = (2\delta_\rho)^2 = +4\delta_\rho^2 \ge 0,
  \qquad
  2(z_\rho + z_{1-\bar\rho}) = 4i\gamma_\rho.
  $$
- **General ordered pair $(\rho, \sigma)$**:
  Because $\mathscr A_{\Theta,\mathcal C}^{\mathrm{cov}}(t)$ is the product of two global explicit-formula evaluations $W_{\mathrm{comp}}(\Psi_1)W_{\mathrm{comp}}(\Psi_2)$, **every ordered pair $(\rho, \sigma)$ is present**. Neither the conjugate diagonal nor the reflection diagonal is isolated by the completed variance functional (`THETA_CONDUCTOR_FUNCTIONAL_REMAINS_DOUBLE_SPECTRAL`).

---

## Section O — Complement Sign and Weil-Positivity Equivalence Audit

Writing the spectral decomposition in the form
$$
\mathscr A = S_{\mathrm{rad}} + R_{\mathrm{comp}},
$$
the conditional contradiction theorem `complement_nonnegativity_contradiction` in `formal/RiemannScope/ModularThetaConductorCurvature.lean` proves that $\mathscr A \le 0$, $S_{\mathrm{rad}} > 0$, and $R_{\mathrm{comp}} \ge 0$ are mutually incompatible. However:
- Neither $R_{\mathrm{comp}} = 0$ nor $R_{\mathrm{comp}} \ge 0$ holds unconditionally for the quadratic double-zero sum $\mathscr A_{\Theta,\mathcal C}^{\mathrm{cov}}(t)$.
- To eliminate off-diagonal zero-zero cross terms $(\rho, \sigma)$ ($\sigma \neq 1 - \bar\rho$) and form a single-zero sum over reflection pairs, one must replace the product of two global functionals $W_{\mathrm{comp}}(\Psi_1)W_{\mathrm{comp}}(\Psi_2)$ by the **single explicit-formula evaluation of a multiplicative convolution square** $Z(g * g^*) = \sum_\rho |\widehat g(\rho - 1/2)|^2$.
- As Burnol explicitly notes (`math/0101068v1` p. 2 and Theorem 3.7; `math/9902080v1` Theorem H2) and Connes–Consani confirm (`2006.13771v1`), the local Archimedean conductor is unconditionally positive/bounded below on $\operatorname{Re}(s) = 1/2$ (and $Z(g * g^*) \ge 0$ holds unconditionally when $\operatorname{supp}(g) \subset [1/\sqrt{2}, \sqrt{2}]$ so no primes $p \ge 2$ enter), **but global positivity across prime powers is equivalent to Weil's positivity criterion and therefore to RH** (`THETA_CONDUCTOR_POSITIVITY_IS_RH_EQUIVALENT`).

---

## Section P — Generic Scale-Base Control ($q \in \{2, e, \tau, 10\}$)

Replacing $\tau = 2\pi$ in the grade transport $q^{-\eta K}$ by any base $q > 1$ sets $\lambda = K\log q$. By the exact homogeneity identity (formalized as `generic_quadratic_heat_base_control` in `formal/RiemannScope/ModularThetaConductorCurvature.lean`):
$$
\left.\frac{d^2}{d\eta^2}\right|_{\eta=0}^{\mathrm{cov}} A(K, \eta; q) = (K\log q)^2 A_{2,\mathrm{cov}}(t),
$$
so the normalized covariant variance ratio
$$
\frac{A_0(t)\,A_{2,\mathrm{cov}}(t; q) - A_1(t; q)^2}{(K\log q)^2 A_0(t)^2}
= \frac{4\pi^2 t^2\bigl(M_0(t)M_2(t) - M_1(t)^2\bigr)}{M_0(t)^2}
\approx 4.7148377907472473 \times 10^{-4}
$$
is **identical across $q \in \{2, e, \tau = 2\pi, 10\}$** (maximum floating-point discrepancy $1.08 \times 10^{-19}$).
- **Classification**: `GENERIC_HEAT_VARIANCE_NOT_TC_CONSTRAINT`.
- **Where $\tau = 2\pi$ Specifically Enters**:
  1. The self-dual additive Fourier character $\lambda(x) = e^{-2\pi i xy} = e^{-i\tau xy}$ on $\mathbb R$;
  2. The Jacobi theta modular inversion $\theta(1/t) = \sqrt{t}\,\theta(t)$, which requires the Gaussian exponent $-\pi x^2 = -(\tau/2)x^2$;
  3. The completed-zeta Archimedean factor $\pi^{-s/2}\Gamma(s/2) = (\tau/2)^{-s/2}\Gamma(s/2)$; and
  4. The additive constant $\log(2\pi) + \gamma_E = \log\tau + \gamma_E$ in Burnol's real Archimedean conductor formula (`math/9902080v1` Theorem D3).

---

## Section Q — Primary-Source Literature Audit

### Required Literature Comparison Table (Section 21)

| Result / Primary Source | Exact Hypotheses | Selected Object | Operator Identity | Arithmetic Implication | Spectral Implication | RH-Equivalent? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Hamburger (1921); Burnol (`math/0407443v3`, `1106.4749v2`); Báez-Duarte (`math/0207237v1`)** | Tempered / co-Poisson distribution supported on $\mathbb Z$ with functional equation $\xi(s)=\xi(1-s)$ and polynomial growth | 1D $\zeta$-distribution ray $\mathbb C\cdot\zeta(s)$ (and via Euler product + log-derivative, $-\zeta'/\zeta = \sum \Lambda(n)n^{-s}$) | $\mathcal F\mathcal I = \Gamma(\chi, s)$ on multiplicative characters | Fixes integer / prime-power station weights, NOT a unique test kernel | Valid across all admissible test functions in the explicit formula | **NO** (unconditional characterization of $\zeta$) |
| **Burnol (`math/9812012v1`, `math/9902080v1`, `math/0101068v1`)** | Local completion $K_\nu$ with additive Haar measure $dx$, initial domain $\mathcal S_0(K_\nu)$ or invariant Schwartz–Mellin core $\Delta(K_\nu) \subset L^2(K_\nu, dx)$ | Local conductor operator $H_\nu = \log\|x\|_\nu + \mathcal F\log\|x\|_\nu\mathcal F^{-1}$ and bounded commutator $K_\nu = i[B,A]$ | $[\mathcal A, H_\nu] = 0$, $\mathcal F H_\nu\mathcal F^{-1} = H_\nu$, $\mathcal I H_\nu\mathcal I^{-1} = H_\nu$, multiplier $\frac{d}{ds}\log\Gamma_\nu(\chi,s)$ | $W(g;\chi) = \sum_\nu H_\nu(g_{\nu;\chi})(1)$ reproduces all local Weil terms uniformly | Reproduces linear explicit-formula sum over zeros and poles on $\operatorname{Re}(s)=1/2$ | **NO** for operator identity; **YES** for global positivity $Z(g*g^*)\ge 0$ (`math/0101068v1` Thm 3.7 proves local positivity only for $\operatorname{supp}(g)\subset[1/c,c]$, $c\le\sqrt{2}$) |
| **Jacobi (1829); Riemann (1859)** | Positive heat semigroup $g_t(x)=e^{-\pi t x^2}$ ($t>0$), Poisson summation on $\mathbb Z$, ground-state / minimum-uncertainty selection at $t=1$ | 1D Gaussian $g_1(x)=e^{-\pi x^2}$, 2D Gaussian $\Theta_1(x,y)=e^{-\pi(x^2+y^2)}$, and theta series $\theta(t)$ | $\mathcal E\Theta_t = 2\mathcal D\Theta_t$, $\mathcal L_{\mathrm{heat}}\Theta_t = \mathcal E(\mathcal E-2)\Theta_t = 4t^2\partial_t^2\Theta_t$, $\nabla_w = \mathcal D + w/2$, $\mathcal P_{\mathrm{reg}}(\mathcal D) = \mathcal D^2 - 1/16$ | Uncompensated Euler curvature $\mathfrak C_{\mathrm{arith}}(\Theta_1) < 0$ by drift; drift-compensated prime variance $\mathfrak C_{\mathrm{prime}}^{\mathrm{cov}}(t) \ge 0$ | Mellin transform of pole-regularized theta state $(\mathcal D^2 - 1/16)\widetilde g_t$ gives completed $\xi(s)$; quadratic variance yields double zero sum | **NO** (unconditional analytic continuation and functional equation) |
| **Weil (1952); Haran (1990)** | Smooth compactly supported / rapidly decaying test function $g$ on $\mathbb R_+^\times$ | Global explicit-formula distribution $\mathcal W_\zeta$ and sesquilinear form $Z(g * g^*)$ | $Z(g) = \sum_\rho \widehat g(\rho-1/2) - (\widehat g(-1/2)+\widehat g(1/2)) = -\sum_\nu W_\nu(g)$ | Prime-power plus Archimedean local functional | Single-zero sum for linear evaluation; reflection-paired Hermitian sum for convolution square $g*g^*$ | **YES**: $Z(g*g^*) \ge 0$ for all $g \in C_c^\infty(\mathbb R_+^\times) \iff \text{RH}$ |
| **Connes & Consani (`2006.13771v1`, `2106.01715v1`, `2112.08820v1`); Burnol (`math/0105120v1`, `math/0203120v7`)** | Compression of scaling operator to Sonin space (orthogonal to cutoff projections $P_\Lambda$, $\mathcal F P_\Lambda\mathcal F^{-1}$) | Prolate spheroidal wave function basis and compressed semi-local trace functional | Angle-operator / prolate differential operator commuting with time-and-band limiting | Archimedean compressed trace is positive by prolate/Toeplitz positivity | Semi-local trace formula over finite primes + archimedean place reduces global positivity to Weil positivity | **NO** at single archimedean place; **YES** for global semi-local Weil positivity across primes |

### Retrieved arXiv URLs (`literature-search-arxiv`)
1. `https://arxiv.org/abs/math/9902080v1` — Jean-François Burnol, *The Explicit Formula and the conductor operator* (1999)
2. `https://arxiv.org/abs/math/9812012v1` — Jean-François Burnol, *Spectral Analysis of the local Commutator Operators* (1998)
3. `https://arxiv.org/abs/math/0101068v1` — Jean-François Burnol, *Sur les Formules Explicites I: analyse invariante* (2000)
4. `https://arxiv.org/abs/math/0112254v6` — Jean-François Burnol, *On Fourier and Zeta(s)* (2001)
5. `https://arxiv.org/abs/1106.4749v2` — Jean-François Burnol, *Deux extensions de Théorèmes de Hamburger* (2012)
6. `https://arxiv.org/abs/math/0407443v3` — Jean-François Burnol, *Entrelacement de co-Poisson* (2007)
7. `https://arxiv.org/abs/math/0203120v7` — Jean-François Burnol, *Two complete and minimal systems associated with the zeros of the Riemann zeta function* (2004)
8. `https://arxiv.org/abs/math/0105120v1` — Jean-François Burnol, *Sur certains espaces de Hilbert de fonctions entières (Sonine spaces)* (2001)
9. `https://arxiv.org/abs/math/0207237v1` — Luis Báez-Duarte, *A general statement of the functional equation for the Riemann zeta-function* (2002)
10. `https://arxiv.org/abs/2006.13771v1` — Alain Connes & Caterina Consani, *Weil positivity and Trace formula, the archimedean place* (2020)
11. `https://arxiv.org/abs/2106.01715v1` — Alain Connes & Caterina Consani, *Spectral Triples and Zeta-Cycles* (2021)
12. `https://arxiv.org/abs/2112.08820v1` — Alain Connes & Caterina Consani, *BC-system, absolute cyclotomy and the quantized calculus* (2021)

---

## Section R — Exact Lean Coverage Map and Remaining Proof Frontier

### 1. Lean 4 Formalization Map (`formal/RiemannScope/ModularThetaConductorCurvature.lean`)
- **Module**: `formal/RiemannScope/ModularThetaConductorCurvature.lean`
- **Module Declarations**: `19` total (`2 def`s + `17 theorem`s)
- **Repository Compiled `theorem` Declarations**: `597` (`580` prior + `17` in `ModularThetaConductorCurvature.lean`)
- **Proof Hygiene**: `0 sorry, 0 admit, no nonstandard project axioms introduced`

| Declaration Identifier | Kind | Exact Statement Scope | Algebraic Only? | Paper Step Supported | External Dependency |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `heatDriftCoeff` | `def` | `heatDriftCoeff c := 4 - 2 * c` | Yes | First-order drift coefficient $4 - 2c$ in $\mathcal L_c\Theta_t$ | None |
| `poleRegMultiplier` | `def` | `poleRegMultiplier s := (1 / 4 - s / 2) ^ 2 - 1 / 16` | Yes | `TASK-TC-036R`: Mellin multiplier of $\mathcal P_{\mathrm{reg}}(\mathcal D) = \mathcal D^2 - 1/16$ on $t^{1/4 - s/2}$ | None |
| `theta_heat_euler_scaling` | `theorem` | `(x*(-2*p*t*x) + y*(-2*p*t*y))*theta = 2*(t*(-p*(x^2+y^2))*theta)` | Yes | Section 5: $\mathcal E\Theta_t = 2\mathcal D\Theta_t$ | None |
| `heat_drift_operator_expansion` | `theorem` | `(4*d2 + 4*d1) - c*(2*d1) = 4*d2 + heatDriftCoeff c * d1` | Yes | Section 6: $\mathcal L_c\Theta_t = 4t^2\partial_t^2\Theta_t + (4-2c)t\partial_t\Theta_t$ | None |
| `heat_drift_compensator_unique` | `theorem` | `(heatDriftCoeff c = 0 ↔ c = 2) ∧ ((4*d2 + 4*d1) - 2*(2*d1) = 4*d2)` | Yes | Section 6: Unique compensator $c = 2$ ($\mathcal L_{\mathrm{heat}} = \mathcal E(\mathcal E-2)$) | None |
| `modular_weight_normalization_involution` | `theorem` | `s ≠ 0 → f_inv = s^2 * f → s⁻¹ * f_inv = s * f` | Yes | Section 7: $\widetilde f(1/t) = \widetilde f(t)$ for $\widetilde f(t)=t^{w/2}f(t)$ | None |
| `modular_covariant_deriv_vanishes_at_self_dual` | `theorem` | `-(D1 + w/2) = D1 + w/2 → D1 + w/2 = 0` | Yes | Section 7: $\nabla_w f(1) = 0$ at self-dual point $t = 1$ | None |
| `heat_and_modular_hessian_difference` | `theorem` | `E = 2*D → 4*(D+1/2)^2 - 4*(D^2-D) = 8*D+1 ∧ (E+1)^2 - E*(E-2) = 4*E+1 ∧ 8*D+1 = 4*E+1` | Yes | Section 8: $4\mathcal H_{\mathrm{mod},1} - \mathcal L_{\mathrm{heat}} = 8\mathcal D + 1 = 4\mathcal E + 1$ | None |
| `heat_and_modular_hessian_incompatibility` | `theorem` | `c1 = 2*c2 → c1 = -2*c2 → c2 = 0 ∧ c1 = 0` | Yes | Section 11: Incompatibility of joint modular Hessian and heat-drift axioms at 2nd order | None |
| `dilation_conductor_commutator_cancellation` | `theorem` | `comm_A = 1 → comm_B = -1 → comm_A + comm_B = 0` | Yes | Section 10: $[\mathcal A, A] = I$ and $[\mathcal A, B] = -I \implies [\mathcal A, \mathcal C] = 0$ | None |
| `covariant_prime_variance_identity` | `theorem` | `curvatureDet M0 (-c*M1) (c^2*M2) = c^2 * curvatureDet M0 M1 M2` | Yes | Section 13: $\mathfrak C_{\mathrm{prime}}^{\mathrm{cov}}(t) = 4\pi^2 t^2(M_0 M_2 - M_1^2)$ | None |
| `covariant_prime_variance_nonneg` | `theorem` | `0 ≤ w1 → 0 ≤ w2 → C_prime_cov = c^2*w1*w2*(r1-r2)^2 ∧ 0 ≤ C_prime_cov` | Yes | Section 13: Nonnegativity of two-point covariant variance | None |
| `arithmetic_sign_and_spectral_sign_no_contradiction` | `theorem` | `0 ≤ v → ∃ A_arith A_spec, A_arith = v ∧ A_spec = v ∧ A_arith = A_spec ∧ 0 ≤ A_arith ∧ 0 ≤ A_spec` | Yes | Section 14: No-contradiction firewall when both sides are $\ge 0$ | None |
| `complement_nonnegativity_contradiction` | `theorem` | `A = S_rad + R_comp → A ≤ 0 → 0 < S_rad → 0 ≤ R_comp → False` | Yes | Section 18: Conditional complement-sign contradiction | None |
| `generic_quadratic_heat_base_control` | `theorem` | `curvatureDet M0 (-(L*c)*M1) ((L*c)^2*M2) = L^2 * (c^2 * curvatureDet M0 M1 M2)` | Yes | Section 20: Generic base $q > 1$ homogeneity control ($L = K\log q$) | None |
| `unshifted_regularizer_mellin_defect` | `theorem` | `(1/4 - s/2)*(1/4 - s/2 - 1/2) = s^2/4 - 1/16 ∧ value(0) = -1/16 ∧ value(1) = 3/16` | Yes | `TASK-TC-036R`: Unshifted $\mathcal D(\mathcal D - 1/2)$ fails to annihilate $s = 0, 1$ on $t^{1/4 - s/2}$ | None |
| `corrected_pole_regularizer_mellin_identity` | `theorem` | `z = s - 1/2 → poleRegMultiplier s = (1/4)*s*(s-1) ∧ poleRegMultiplier s = (1/4)*(z^2-1/4) ∧ poleRegMultiplier 0 = 0 ∧ poleRegMultiplier 1 = 0` | Yes | `TASK-TC-036R`: Repaired $\mathcal P_{\mathrm{reg}}(\mathcal D) = \mathcal D^2 - 1/16$ has Mellin multiplier $\frac{1}{4}s(s-1) = \frac{1}{4}(z^2-1/4)$ vanishing at $s = 0, 1$ | None |
| `corrected_pole_regularizer_annihilates_quarter_powers` | `theorem` | `((1/4)^2 - 1/16) * t_pos = 0 ∧ ((-1/4)^2 - 1/16) * t_neg = 0` | Yes | `TASK-TC-036R`: $\mathcal P_{\mathrm{reg}}(\mathcal D) = \mathcal D^2 - 1/16$ annihilates both $t^{1/4} = \widetilde g_t(0)$ and $t^{-1/4} = \int \widetilde g_t(u)\,du$ | None |
| `corrected_pole_regularizer_spatial_jet` | `theorem` | `((1/4 - r)^2 - r) - 1/16 = r^2 - (3/2)*r ∧ value_at_r_eq_0 = 0` | Yes | `TASK-TC-036R`: Spatial polynomial factor $r^2 - \frac{3}{2}r$ of $\Phi_t(u) = (\mathcal D^2 - 1/16)\widetilde g_t(u)$ vanishes at $u = 0$ | None |

**Not Formalized in Lean (Paper / Arb / Literature Scope)**:
- Burnol's functional-analytic conductor domain $\mathcal S_0(K_\nu) / \Delta(K_\nu)$ and essential self-adjointness theorems;
- The complete Riemann–Weil explicit formula and contour-shift residue calculus;
- Jacobi theta Poisson summation and modular transformation $\theta(1/t) = \sqrt{t}\,\theta(t)$;
- Global spectral positivity (Weil positivity criterion);
- Trace-class / Sonin-space operator properties; and
- `OBL-CT-001A`.

### 2. Exact Remaining Subgate (`SUBGATE-TC-036A`)
- **Subgate ID**: `SUBGATE-TC-036A`
- **Theorem Name**: *Zero-Independent Diagonal-Isolation and Sign-Incompatibility Identity*
- **Exact Statement**:
  > There exists a zero-independently defined operator pair $(\mathcal P, \mathcal Q)$ on the invariant domain $\Delta(\mathbb A_{\mathbb Q}^\times / \mathbb Q^\times)$ of the completed explicit-formula distribution $\mathcal W_\xi$ and a pole-regularized state $\Phi_t = (\mathcal D^2 - \frac{1}{16})\widetilde g_t$ (or $\Phi_t^{(2)} = (\mathcal D^2 - \frac{1}{16})^2\widetilde g_t$) in $\Delta$ such that:
  > 1. **Zero-Independent Arithmetic Nonpositivity**: The arithmetic evaluation $\mathscr A_{\mathrm{arith}}(\Phi_t)$ satisfies an unconditional nonpositivity law $\mathscr A_{\mathrm{arith}}(\Phi_t) \le 0$ from prime-power, Archimedean conductor, and pole terms alone; and
  > 2. **Diagonal-Isolated Spectral Positivity**: Its complete spectral transfer $\mathscr A_{\mathrm{spec}}(\Phi_t)$ eliminates off-diagonal zero-zero cross terms $(\rho, \sigma)$ ($\sigma \neq 1 - \bar\rho$) and signed ordinate phases $-4\gamma_\rho^2$ without invoking Weil positivity, reducing to $\sum_\rho w_\rho(t)\delta_\rho^2 + R_{\mathrm{comp}}(t)$ with $w_\rho(t) > 0$ and unconditionally certified $R_{\mathrm{comp}}(t) \ge 0$.
- **Status**: `OPEN` (`OBL-CT-001A = OPEN`).
