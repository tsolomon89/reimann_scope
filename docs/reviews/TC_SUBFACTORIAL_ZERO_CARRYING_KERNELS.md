# TASK-TC-040 Review: Subfactorial-Denominator Zero-Carrying Kernels — Bernoulli Reflection, Gamma-Ratio Tradeoffs, Positive-Moment Hankel Architecture, and Escape from the Newton Factorial Obstruction

**Task ID:** `TASK-TC-040`  
**Subgate ID:** `SUBGATE-TC-040A`  
**Implementation Module:** [`tc/fauzan_subfactorial_zero_kernel.py`](file:///c:/Development/Projects/reimann_scope/tc/fauzan_subfactorial_zero_kernel.py)  
**Machine-Readable Artifact:** [`data/tc_fauzan_subfactorial_zero_kernel.json`](file:///c:/Development/Projects/reimann_scope/data/tc_fauzan_subfactorial_zero_kernel.json)  
**Lean 4 Formalization Module:** [`formal/RiemannScope/SubfactorialZeroKernel.lean`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/SubfactorialZeroKernel.lean) (8 formal theorems, 0 `sorry`, 0 `admit`)  
**Regression Test Suite:** [`tests/test_tc_fauzan_subfactorial_zero_kernel.py`](file:///c:/Development/Projects/reimann_scope/tests/test_tc_fauzan_subfactorial_zero_kernel.py)

---

### A. Executive summary

`TASK-TC-040` investigates whether the zero-argument arithmetic bridge established in `TASK-TC-039`–`TASK-TC-039R4` for
\[
\mathcal{R}_\tau(z) = (2z - 1)\tau^{-2z}\zeta(2z), \qquad \tau = 2\pi, \qquad \mathcal{R}_\tau(m) = (-1)^{m+1}\frac{(2m-1)B_{2m}}{2(2m)!} \in \mathbb{Q},
\]
can be transformed into a zero-carrying analytic kernel whose rational samples at integer nodes $m \in \mathbb{Z}_{\ge 0}$ have **subfactorial denominator growth** $\log D_n = O(n)$ while still generating nonzero primitive integer auxiliary polynomials $\widetilde{Q}_n(Y) \in \mathbb{Z}[Y]$ with sufficient analytic smallness at $\gamma_1 = 14.13472514173469379\dots$ to support a Diophantine irrationality contradiction.

The principal mathematical results of `TASK-TC-040` are:

1. **Preflight Synchronization Completed (`TASK-TC-039R4`):**
   - Distinguished `EXACT_TRANSFORMED_ACTION` ($S_{n,c}^{\mathrm{exact}}(u) = -(n+1)\log(1-u^2) - \frac{\sqrt{c(1-u^2)}}{u}$) from `LOCAL_SADDLE_MODEL_PHI_N` ($\Phi_n(u) = nu^2 - \frac{\sqrt{c}}{u}$) under the canonical small-$u$ convention $w = -1 + u^2$, $1+w = u^2$.
   - Synchronized the degree-gap spacing bound to $n + 1 - C_0 n^{2/3} \le k_n \le n + 1$ ($\Delta m \asymp m^{2/3}$ from $\theta_{m+1} - \theta_m \asymp m^{-2/3}$), verifying $2k_n\log k_n = 2n\log n + O(n)$.
   - Synchronized the finite primitive-content table in [`docs/reviews/TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md`](file:///c:/Development/Projects/reimann_scope/docs/reviews/TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md) directly to [`data/tc_fauzan_zero_argument_asymptotic_repair.json`](file:///c:/Development/Projects/reimann_scope/data/tc_fauzan_zero_argument_asymptotic_repair.json) (`primitive_norm_polynomial_audit`), and froze `SUBGATE-TC-039A [Newton] = CLOSED_NEGATIVE_AT_GATE_Z5` under `CONSECUTIVE_NEWTON_PRIMITIVE_NORM_FACTORIAL_OBSTRUCTION`.
2. **Route A — Subfactorial Sample Denominators Achieved via $\tau$-Functional Equation Reflection (`SUBFACTORIAL_RATIONAL_SAMPLE_DENOMINATOR_ACHIEVED`, `BERNOULLI_FUNCTION_NONTRIVIAL_ZETA_ZERO_BRIDGE_PROVED`):**
   Multiplying $\mathcal{R}_\tau(z)$ by the zero-independent reflection multiplier $\Gamma(2z+1)\cos(\tau z/2)$ uses the $\tau$-form functional equation $\zeta(2z) = 2\tau^{2z-1}\sin(\tau z/2)\Gamma(1-2z)\zeta(1-2z)$ to cancel $\tau^{-2z}$, $\sin(\tau z/2)$, $\cos(\tau z/2)$, and $\Gamma(1-2z)$ identically, yielding the entire reflected kernels
   \[
   \boxed{
   \mathcal{K}_0(z) := \Gamma(2z+1)\cos(\tau z/2)\mathcal{R}_\tau(z) = z(2z-1)\zeta(1-2z) = -\frac{2z-1}{2}\mathcal{B}(z), \qquad \mathcal{B}(z) := -2z\zeta(1-2z).
   }
   \]
   For every nontrivial zero $\rho$ of $\zeta(s)$, $\zeta(\rho) = 0 \iff \zeta(1-\rho) = 0$, so $\mathcal{B}(\rho/2) = \mathcal{K}_0(\rho/2) = 0$, while at every integer $m \ge 0$,
   \[
   \boxed{
   \mathcal{B}(m) = B_{2m} \in \mathbb{Q}, \qquad \mathcal{K}_0(m) = -\frac{2m-1}{2}B_{2m} \in \mathbb{Q}.
   }
   \]
   By the von Staudt–Clausen theorem, $\operatorname{den}(B_{2m}) = \prod_{(p-1)\mid 2m} p$ is squarefree, and for every $n \ge 1$ the sample denominator LCMs satisfy the **exact primorial identities**
   \[
   \boxed{
   D_n^{\mathcal{B}} := \operatorname{lcm}_{0\le m\le n}\operatorname{den}(\mathcal{B}(m)) = \prod_{p \le 2n+1} p = e^{\vartheta(2n+1)}, \qquad
   D_n^{\mathcal{K}_0} := \operatorname{lcm}_{0\le m\le n}\operatorname{den}(\mathcal{K}_0(m)) = 2\prod_{p \le 2n+1} p,
   }
   \]
   so $\log D_n^{\mathcal{B}} = \vartheta(2n+1) = 2n + o(n) = O(n)$ (verified exactly for $1 \le n \le 30$).
3. **Factorial Budget Conservation Across the Gamma-Ratio Ladder $\mathcal{B}_q(z) = \mathcal{K}_0(z)/\Gamma(z+1)^q$ (`PROVED_TWO_SIDED_DENOMINATOR_ASYMPTOTIC`, `GAMMA_RATIO_FACTORIAL_BUDGET_TRADEOFF_PROVED`):**
   Using an explicit irregular-prime-avoiding von Staudt–Clausen witness $m_p = k_p\frac{p-1}{2} \in [n-p+2, n]$ with $k_p \not\equiv -1 \pmod p$ for every odd prime $3 \le p \le n$, we prove unconditionally for every $q \in \mathbb{Z}_{\ge 0}$ that
   \[
   \boxed{
   \log|\mathcal{B}_q(n)| = (2-q)n\log n + O_q(n), \qquad \log D_{q,n} = q\,n\log n + O_q(n),
   }
   \]
   so the sum of the sample-growth exponent and the sample-denominator exponent is **identically $2n\log n + O_q(n)$ for every $q \ge 0$**.
4. **Route B — Positive Bernoulli Stieltjes Moments & Argument-Coupling Firewall (`BERNOULLI_EVEN_ABSOLUTE_VALUES_STIELTJES_MOMENT_SEQUENCE_PROVED`, `BERNOULLI_STIELTJES_HANKEL_POSITIVITY_DOES_NOT_COUPLE_TO_ZETA_ZERO_ARGUMENT`):**
   The sign-adjusted kernel $\mathcal{P}(z) := -e^{i\tau z/2}\mathcal{B}(z)$ satisfies $\mathcal{P}(\rho/2) = 0$ and $\mu_m := \mathcal{P}(m+1) = |B_{2m+2}| = \int_0^\infty y^m\,d\nu_\tau(y) > 0$ for the positive Stieltjes measure $d\nu_\tau(y) = \frac{\tau\sqrt{y}}{4\sinh^2(\tau\sqrt{y}/2)}\,dy$ on $(0, \infty)$. By the Carlitz–Touchard–Al-Salam continued-fraction theorem, its Hankel determinants satisfy the exact product formula
   \[
   \boxed{
   H_n^{\mathcal{B}} := \det\bigl(|B_{2i+2j+2}|\bigr)_{0\le i,j<n} = 6^{-n}\prod_{k=1}^{n-1}\left[\frac{k^3(k+1)(2k-1)(2k+1)^3}{(4k-1)(4k+1)^2(4k+3)}\right]^{n-k} > 0,
   }
   \]
   with super-factorial growth $\log H_n^{\mathcal{B}} = 2n^2\log n - (3 + 2\log 2)n^2 + O(n\log n) \to +\infty$, while the orthogonal polynomial variable $y$ is the Stieltjes integration variable on $(0, \infty)$, NOT the Mellin zero argument $\rho_1/2$.
5. **Routes C–E & Equispaced Gamma-Reflection No-Go Theorem (`EQUISPACED_GAMMA_REFLECTION_CLASS_NO_GO_PROVED`, `FACTORIAL_RELOCATION_ACROSS_DENOMINATOR_GROWTH_AND_BASIS_PROVED`):**
   In the equispaced Newton/Lagrange basis on $\{0, \dots, n\}$, the canonical primitive integer norm polynomial $\widetilde{Q}_n^{[f]}(Y) \in \mathbb{Z}[Y]$ for **any** rational sample sequence $f(m) \in \mathbb{Q}$ with $\Delta^{n+1}f(0) \ne 0$ satisfies the universal sample-independent lower bound $\widetilde{Q}_n^{[f]}(\gamma_1) \ge \frac{1}{2}\prod_{j=0}^n\bigl((2j-\tfrac{1}{2})^2 + \gamma_1^2\bigr) \to +\infty$. In multipoint Padé interpolation on $\{0, \dots, 2n\}$, the divergent-OGF kernels ($\mathcal{K}_0, \mathcal{B}, \mathcal{B}_1$) fail analytic smallness (`Gate Z4`), while the bounded-radius kernels ($\mathcal{R}_\tau, \mathcal{R}_\pi, \mathcal{B}_2$) have $\log\widetilde{Q}_{n,\mathrm{Pade}}(\gamma_1) > 0$ growing rapidly for all $1 \le n \le 7$. Thus `SUBGATE-TC-040A` is closed for the equispaced Gamma-reflection/Gamma-ratio class at Gate Z5.

---

### B. Preflight synchronization repairs (`TASK-TC-039R4`)

All three preflight synchronization items from the `TASK-TC-039R4` review are resolved across code, documentation, and artifacts:

1. **Model-Action Synchronization (`EXACT_TRANSFORMED_ACTION` vs `LOCAL_SADDLE_MODEL_PHI_N`):**
   Under the canonical small-$u$ contour variable
   \[
   \boxed{w = -1 + u^2, \qquad 1 + w = u^2 \qquad (\operatorname{Re}(u) > 0),}
   \]
   the exact transformed action (`EXACT_TRANSFORMED_ACTION`) is
   \[
   S_{n,c}^{\mathrm{exact}}(u) := -(n+1)\log(1-u^2) - \frac{\sqrt{c(1-u^2)}}{u},
   \]
   whereas its small-$u$ local saddle model (`LOCAL_SADDLE_MODEL_PHI_N`) is
   \[
   \boxed{\Phi_n(u) := nu^2 - \frac{\sqrt{c}}{u}, \qquad \Phi_n'(u) = 2nu + \frac{\sqrt{c}}{u^2} = 0 \iff u^3 = -\frac{\sqrt{c}}{2n},}
   \]
   with conjugate right-half-plane saddles $u_\pm = \left(\frac{\sqrt{c}}{2n}\right)^{1/3}e^{\pm i\pi/3} = x_n(1 \pm i\sqrt{3})$.
2. **Degree-Gap Synchronization ($\Delta m \asymp m^{2/3}$):**
   Since $\theta_m = \omega(c)m^{1/3}$ satisfies $\theta_{m+1} - \theta_m = \frac{\omega(c)}{3}m^{-2/3}(1 + O(m^{-1})) \asymp m^{-2/3}$, consecutive zeros of $\cos(\omega(c)m^{1/3})$ are separated by $\Delta m \asymp m^{2/3}$. Thus the highest nonzero forward-difference index $k_n \le n+1$ in $\deg Q_n^{(c)}(Y) = 2k_n$ satisfies the conservative spacing bound
   \[
   \boxed{n + 1 - C_0 n^{2/3} \le k_n \le n + 1,}
   \]
   which suffices for $2k_n\log k_n = 2n\log n - 2C_0 n^{2/3}\log n + O(n) = 2n\log n + O(n)$.
3. **Primitive-Content Finite-Table Synchronization:**
   The finite table in [`docs/reviews/TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md`](file:///c:/Development/Projects/reimann_scope/docs/reviews/TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md#L541-L553) is synchronized directly to [`data/tc_fauzan_zero_argument_asymptotic_repair.json`](file:///c:/Development/Projects/reimann_scope/data/tc_fauzan_zero_argument_asymptotic_repair.json) (`primitive_norm_polynomial_audit`), where $g_n^{(c)} = 1$ ($\log g_n^{(c)} = 0.00$) for all $1 \le n \le 12$:
   - $\pi$ ($c=4$): $n=4$: $\log M_4 = 43.32, \log\widetilde{Q}_4(\gamma_1) = 48.96, \mathscr{E}_4^{\mathrm{prim}} = -4.896$; $n=8$: $\log M_8 = 114.53, \log\widetilde{Q}_8(\gamma_1) = 124.78, \mathscr{E}_8^{\mathrm{prim}} = -6.932$; $n=12$: $\log M_{12} = 167.45, \log\widetilde{Q}_{12}(\gamma_1) = 179.01, \mathscr{E}_{12}^{\mathrm{prim}} = -6.885$.
   - $\tau$ ($c=1$): $n=4$: $\log M_4 = 55.80, \log\widetilde{Q}_4(\gamma_1) = 64.65, \mathscr{E}_4^{\mathrm{prim}} = -6.465$; $n=8$: $\log M_8 = 138.10, \log\widetilde{Q}_8(\gamma_1) = 148.76, \mathscr{E}_8^{\mathrm{prim}} = -8.265$; $n=12$: $\log M_{12} = 204.18, \log\widetilde{Q}_{12}(\gamma_1) = 214.96, \mathscr{E}_{12}^{\mathrm{prim}} = -8.268$.

---

### C. Frozen Newton primitive-obstruction statement

With the canonical primitive integer normalization $\widetilde{Q}_n^{(c)}(Y) = M_n^{(c)} Q_n^{(c)}(Y) = \frac{L_n^{(c)}}{g_n^{(c)}} Q_n^{(c)}(Y) \in \mathbb{Z}[Y]$, the consecutive-Newton route is permanently frozen at Gate Z5 under `CONSECUTIVE_NEWTON_PRIMITIVE_NORM_FACTORIAL_OBSTRUCTION`:
- `NEWTON_TWO_STEP_RAW_LOWER_ENVELOPE_PROVED`
- `PRIMITIVE_NORM_POLYNOMIAL_LOWER_BOUND_PROVED`
- `NEWTON_TWO_APPROXIMANT_PRIMITIVE_ROUTE_RIGOROUSLY_FAILS_GATE_Z5`
- `SUBGATE-TC-039A [Newton] = CLOSED_NEGATIVE_AT_GATE_Z5`

Specifically, on the cofinal set $\Delta^{n+1}a_0^{(c)} \ne 0$ (including all $0 \le n \le 200$),
\[
\boxed{
\widetilde{Q}_n^{(c)}(\gamma_1) \ge \frac{1}{2}\prod_{j=0}^n\left[\left(2j-\frac{1}{2}\right)^2 + \gamma_1^2\right] \ge \frac{1}{2}\left(\frac{1}{4}+\gamma_1^2\right)(n!)^2 \longrightarrow +\infty,
}
\]
and globally for all $n \ge n_0(c)$, $\log\widetilde{Q}_n^{(c)}(\gamma_1) \ge 2n\log n - O_c(n) \to +\infty$.

---

### D. Candidate kernel hierarchy

To test whether the factorial denominator $(2m)!$ in $\mathcal{R}_\tau(m)$ can be removed without destroying Diophantine efficiency, we analyze the five-level zero-carrying kernel hierarchy:

| Kernel | Analytic Definition ($\tau = 2\pi$) | Integer Sample Value at $m \in \mathbb{Z}_{\ge 0}$ | Sample Growth $\log|F(m)|$ | Sample Denominator LCM $\log D_n$ | OGF Radius $R_{\mathrm{OGF}}$ |
|---|---|---|---|---|---|
| $\mathcal{R}_\tau(z)$ | $(2z-1)\tau^{-2z}\zeta(2z)$ | $(-1)^{m+1}\frac{(2m-1)B_{2m}}{2(2m)!}$ | $-2m\log\tau + O(\log m)$ | $2n\log n + O(n)$ | $\tau^2 = 4\pi^2$ |
| $\mathcal{K}_0(z)$ | $\Gamma(2z+1)\cos(\tau z/2)\mathcal{R}_\tau(z) = z(2z-1)\zeta(1-2z)$ | $-\frac{2m-1}{2}B_{2m}$ | $2m\log m - 2(1+\log\pi)m + O(\log m)$ | $\vartheta(2n+1) + \log 2 = 2n + o(n)$ | $0$ |
| $\mathcal{B}(z)$ | $B(2z) = -2z\zeta(1-2z) = -\frac{2}{2z-1}\mathcal{K}_0(z)$ | $B_{2m}$ | $2m\log m - 2(1+\log\pi)m + O(\log m)$ | $\vartheta(2n+1) = 2n + o(n)$ | $0$ |
| $\mathcal{B}_q(z)$ | $\mathcal{K}_0(z)/\Gamma(z+1)^q$ ($q \in \mathbb{Z}_{\ge 0}$) | $-\frac{2m-1}{2}\frac{B_{2m}}{(m!)^q}$ | $(2-q)m\log m + O_q(m)$ | $q\,n\log n + O_q(n)$ | $0$ ($q\le 1$), $\pi^2$ ($q=2$), $\infty$ ($q\ge 3$) |
| $\mathcal{P}(z)$ | $-e^{i\tau z/2}\mathcal{B}(z) = 2ze^{i\pi z}\zeta(1-2z)$ | $(-1)^{m+1}B_{2m} = |B_{2m}| > 0$ ($m\ge 1$) | $2m\log m - 2(1+\log\pi)m + O(\log m)$ | $\vartheta(2n+1) = 2n + o(n)$ | $0$ (Stieltjes moment sequence) |

---

### E. \(\tau\)-functional equation and reflected kernel \(\mathcal K_0(z)\)

In $\tau$-native coordinates ($\tau = 2\pi$, $\pi = \tau/2$), Riemann's functional equation at $s = 2z$ takes the form
\[
\boxed{
\zeta(2z) = 2^{2z}\pi^{2z-1}\sin(\pi z)\Gamma(1-2z)\zeta(1-2z)
= 2\tau^{2z-1}\sin\!\left(\frac{\tau z}{2}\right)\Gamma(1-2z)\zeta(1-2z).
}
\]
Substituting this into $\mathcal{R}_\tau(z) = (2z-1)\tau^{-2z}\zeta(2z)$ gives
\[
\mathcal{R}_\tau(z) = \frac{2(2z-1)}{\tau}\sin\!\left(\frac{\tau z}{2}\right)\Gamma(1-2z)\zeta(1-2z).
\]
Now multiply by the zero-independent meromorphic reflection multiplier $\Gamma(2z+1)\cos(\tau z/2)$. Using $\Gamma(2z+1)\Gamma(1-2z) = 2z\Gamma(2z)\Gamma(1-2z) = \frac{2\pi z}{\sin(2\pi z)} = \frac{\tau z}{2\sin(\tau z/2)\cos(\tau z/2)}$, every transcendental factor $\tau$, $\sin(\tau z/2)$, $\cos(\tau z/2)$, and $\Gamma(1-2z)$ cancels identically:
\[
\boxed{
\mathcal{K}_0(z) := \Gamma(2z+1)\cos\!\left(\frac{\tau z}{2}\right)\mathcal{R}_\tau(z)
= 4^{-z}\Gamma(2z+1)\cos(\pi z)\mathcal{R}_\pi(z)
= z(2z-1)\zeta(1-2z).
}
\]
Since $\zeta(1-2z)$ is meromorphic on $\mathbb{C}$ with a single simple pole at $1-2z = 1 \iff z = 0$ of residue $-\frac{1}{2}$, the factor $z$ cancels the pole at $z = 0$ with
\[
\boxed{\mathcal{K}_0(0) = \lim_{z\to 0} z(2z-1)\zeta(1-2z) = (-1)\cdot\left(-\frac{1}{2}\right) = \frac{1}{2}, \qquad \mathcal{K}_0(1/2) = 0,}
\]
so $\mathcal{K}_0(z)$ is **entire on $\mathbb{C}$** (formalized algebraically in Lean 4 as `bernoulli_kernel_linear_relation` and `gamma_reflection_sample_clearing_identity`).

---

### F. Pure Bernoulli function \(\mathcal B(z)\) and zero-divisor comparison

Dividing out the trivial linear factor $-\frac{2z-1}{2}$ defines the rescaled **pure Bernoulli function**:
\[
\boxed{
\mathcal{B}(z) := B(2z) = -2z\zeta(1-2z), \qquad \mathcal{K}_0(z) = -\frac{2z-1}{2}\mathcal{B}(z),
}
\]
where $B(s) := -s\zeta(1-s)$ is the classical analytic interpolation of the Bernoulli numbers ($B(2m) = B_{2m}$ for $m \ge 1$ and $B(0) = 1 = B_0$). In accordance with the novelty firewall, this classical identity is classified as:
- `CLASSICAL_IDENTITY_REPURPOSED_FOR_ZERO_ARGUMENT_ARITHMETIC` (`PROVED_WITH_EXTERNAL_THEOREM`).

#### Zero-Divisor Comparison (`BERNOULLI_FUNCTION_NONTRIVIAL_ZETA_ZERO_BRIDGE_PROVED`)

For every nontrivial Riemann zeta zero $\rho$ ($0 < \operatorname{Re}(\rho) < 1$), the functional equation satisfies $\zeta(\rho) = 0 \iff \zeta(1-\rho) = 0$. Therefore, at $z = \rho/2$ ($0 < \operatorname{Re}(z) < 1/2$, $1 - 2z = 1 - \rho$):
\[
\boxed{
\zeta(\rho) = 0 \iff \zeta(1-\rho) = 0 \implies \mathcal{B}(\rho/2) = -\rho\zeta(1-\rho) = 0 \implies \mathcal{K}_0(\rho/2) = 0 \implies \mathcal{B}_q(\rho/2) = 0
}
\]
(formalized in Lean 4 as `bernoulli_kernel_zero_at_zeta_zero`). However, the **full zero divisors on $\mathbb{C}$ are NOT identical**:
- **$\mathcal{R}_\tau(z) = (2z-1)\tau^{-2z}\zeta(2z)$:** vanishes at $z = \rho/2$ (nontrivial zeros) and at the **negative integers** $z = -k$ ($k \in \mathbb{Z}_{\ge 1}$, where $2z = -2k$ hits the trivial zeros of $\zeta$), with $\mathcal{R}_\tau(1/2) = 1/\tau \ne 0$.
- **$\mathcal{B}(z) = -2z\zeta(1-2z)$:** vanishes at $z = \rho/2$ (nontrivial zeros) and at the **positive half-integers** $z = k + \frac{1}{2}$ ($k \in \mathbb{Z}_{\ge 1}$, where $1-2z = -2k$ hits the trivial zeros of $\zeta$), with $\mathcal{B}(1/2) = -\zeta(0) = \frac{1}{2} \ne 0$ and $\mathcal{B}(-k) = 2k\zeta(2k+1) \ne 0$.
- **$\mathcal{K}_0(z) = -\frac{2z-1}{2}\mathcal{B}(z)$:** vanishes at $z = \rho/2$, at $z = k + \frac{1}{2}$ ($k \ge 1$), and additionally at $z = \frac{1}{2}$.
- **$\mathcal{B}_q(z) = \mathcal{K}_0(z)/\Gamma(z+1)^q$ ($q \ge 1$):** vanishes at all zeros of $\mathcal{K}_0(z)$ and additionally has zeros of multiplicity $q$ at the negative integers $z = -k$ ($k \ge 1$) from the poles of $\Gamma(z+1)^q$.

---

### G. Exact sample values and von Staudt–Clausen denominator law

At every integer $m \ge 0$,
\[
\boxed{
\mathcal{B}(m) = B_{2m} \in \mathbb{Q}, \qquad \mathcal{K}_0(m) = -\frac{2m-1}{2}B_{2m} \in \mathbb{Q}.
}
\]
Define the cumulative sample denominator LCMs
\[
D_n^{\mathcal{B}} := \operatorname{lcm}_{0\le m\le n}\operatorname{den}(\mathcal{B}(m)), \qquad
D_n^{\mathcal{K}_0} := \operatorname{lcm}_{0\le m\le n}\operatorname{den}(\mathcal{K}_0(m)).
\]

#### Theorem (`SUBFACTORIAL_RATIONAL_SAMPLE_DENOMINATOR_ACHIEVED`)

For every integer $n \ge 1$:
\[
\boxed{
D_n^{\mathcal{B}} = \prod_{p \le 2n+1} p = e^{\vartheta(2n+1)}, \qquad
D_n^{\mathcal{K}_0} = 2\prod_{p \le 2n+1} p = 2e^{\vartheta(2n+1)},
}
\]
and therefore by the Prime Number Theorem ($\vartheta(x) = x + o(x)$),
\[
\boxed{
\log D_n^{\mathcal{B}} = \vartheta(2n+1) = 2n + o(n) = O(n), \qquad
\log D_n^{\mathcal{K}_0} = \vartheta(2n+1) + \log 2 = 2n + o(n) = O(n).
}
\]

**Proof.** By the von Staudt–Clausen theorem, for every $m \ge 1$, $B_{2m} + \sum_{(p-1)\mid 2m}\frac{1}{p} \in \mathbb{Z}$, so $\operatorname{den}(B_{2m}) = \prod_{(p-1)\mid 2m} p$ is strictly squarefree ($v_p(\operatorname{den}(B_{2m})) \in \{0, 1\}$).
1. If a prime $p$ divides $\operatorname{den}(B_{2m})$ for some $1 \le m \le n$, then $p - 1 \le 2m \le 2n$, so $p \le 2n+1$ and $v_p(D_n^{\mathcal{B}}) \le 1$. Conversely, for every prime $p \le 2n+1$, let $m_2 := 1 \le n$ if $p=2$ and $m_p := \frac{p-1}{2} \in [1, n]$ if $p \ge 3$ is odd; then $(p-1)\mid 2m_p$, so $p \mid \operatorname{den}(B_{2m_p})$ and $v_p(D_n^{\mathcal{B}}) = 1$. Hence $D_n^{\mathcal{B}} = \prod_{p \le 2n+1} p$ with **exact equality** for every $n \ge 1$.
2. For $\mathcal{K}_0(m) = -\frac{2m-1}{2}B_{2m}$, at $m = 1 \le n$ we have $\mathcal{K}_0(1) = -\frac{1}{12}$, so $v_2(D_n^{\mathcal{K}_0}) = 2 = 1 + v_2(D_n^{\mathcal{B}})$. For every odd prime $3 \le p \le 2n+1$, at the witness $m_p = \frac{p-1}{2} \le n$ we have $2m_p - 1 = p - 2$, and $\gcd(p-2, p) = 1$, so $p \nmid (2m_p - 1)$ and $v_p(\operatorname{den}(\mathcal{K}_0(m_p))) = v_p(\operatorname{den}(B_{p-1})) = 1$. Hence $D_n^{\mathcal{K}_0} = 2 D_n^{\mathcal{B}} = 2\prod_{p \le 2n+1} p$ for every $n \ge 1$. $\square$

| $n$ | $D_n^{\mathcal{B}} = \prod_{p\le 2n+1} p$ | $D_n^{\mathcal{K}_0} = 2 D_n^{\mathcal{B}}$ | $\log D_n^{\mathcal{B}} = \vartheta(2n+1)$ | $\frac{1}{n}\log D_n^{\mathcal{B}}$ | $\log D_n^{\mathcal{R}_\tau}$ | $\frac{\log D_n^{\mathcal{R}_\tau}}{n\log n}$ |
|---:|---|---|---:|---:|---:|---:|
| $1$ | $6$ | $12$ | $1.792$ | $1.792$ | $3.178$ | — |
| $2$ | $30$ | $60$ | $3.401$ | $1.701$ | $6.174$ | $4.453$ |
| $4$ | $210$ | $420$ | $5.347$ | $1.337$ | $14.699$ | $2.651$ |
| $8$ | $510510$ | $1021020$ | $13.143$ | $1.643$ | $34.891$ | $2.097$ |
| $12$ | $223092870$ | $446185740$ | $19.223$ | $1.602$ | $63.390$ | $2.126$ |
| $20$ | $304250263527210$ | $608500527054420$ | $33.349$ | $1.667$ | $119.428$ | $1.993$ |
| $30$ | $117288381359406970983270$ | $234576762718813941966540$ | $53.119$ | $1.771$ | $207.176$ | $2.030$ |

---

### H. Sample growth vs denominator growth under reflection

Removing $(2m)!$ from the denominator via $\Gamma(2z+1)\cos(\tau z/2)$ moves the exact same $(2m)!$ into the **numerator magnitude** of the integer samples (`FACTORIAL_COST_MOVES_FROM_DENOMINATOR_TO_SAMPLE_GROWTH_UNDER_REFLECTION`):
\[
\boxed{
|\mathcal{B}(m)| = |B_{2m}| = \frac{2(2m)!}{\tau^{2m}}\zeta(2m), \qquad
|\mathcal{K}_0(m)| = \frac{(2m-1)(2m)!}{\tau^{2m}}\zeta(2m) \qquad (m \ge 1).
}
\]
By Stirling's formula,
\[
\boxed{
\log|\mathcal{B}(m)| = 2m\log m - 2(1+\log\pi)m + \frac{1}{2}\log m + \log(2\sqrt{\pi}) + O(m^{-1}),
}
\]
\[
\boxed{
\log|\mathcal{K}_0(m)| = 2m\log m - 2(1+\log\pi)m + \frac{3}{2}\log m + \log(2\sqrt{\pi}) + O(m^{-1}),
}
\]
and consequently the ordinary generating functions $\sum_{m=0}^\infty \mathcal{B}(m) t^m$ and $\sum_{m=0}^\infty \mathcal{K}_0(m) t^m$ have radius of convergence
\[
\boxed{R_{\mathrm{OGF}}(\mathcal{B}) = R_{\mathrm{OGF}}(\mathcal{K}_0) = 0.}
\]

---

### I. Gamma-ratio family \(\mathcal B_q(z)\) and two-sided denominator theorem

To interpolate continuously between $\mathcal{K}_0(z)$ ($q = 0$) and bounded-sample kernels ($q \ge 2$), define for $q \in \mathbb{Z}_{\ge 0}$ the entire Gamma-ratio family
\[
\boxed{
\mathcal{B}_q(z) := \frac{\mathcal{K}_0(z)}{\Gamma(z+1)^q} = \frac{z(2z-1)\zeta(1-2z)}{\Gamma(z+1)^q}, \qquad
\mathcal{B}_q(m) = -\frac{2m-1}{2}\frac{B_{2m}}{(m!)^q} \in \mathbb{Q},
}
\]
and let $D_{q,n} := \operatorname{lcm}_{0\le m\le n}\operatorname{den}(\mathcal{B}_q(m))$.

#### Theorem (`PROVED_TWO_SIDED_DENOMINATOR_ASYMPTOTIC`, `GAMMA_RATIO_FACTORIAL_BUDGET_TRADEOFF_PROVED`)

For every integer $q \ge 0$ and every $n \ge 3$, $D_{q,n}$ satisfies the **unconditional** two-sided inequality:
\[
\boxed{
q\log(n!) + \sum_{3 \le p \le n}\bigl(1 - q\lfloor\log_p n\rfloor\bigr)\log p \;\le\; \log D_{q,n} \;\le\; q\log(n!) + \vartheta(2n+1) + \log 2,
}
\]
and therefore unconditionally (**without** any unproved hypothesis on irregular primes):
\[
\boxed{
\log D_{q,n} = q\,n\log n - q\,n + O_q(n) = q\,n\log n + O_q(n), \qquad
\log|\mathcal{B}_q(n)| = (2-q)n\log n + O_q(n).
}
\]

**Proof (Irregular-Prime-Immune Witness Construction).**
- **Upper bound:** Every sample $\mathcal{B}_q(m) = \frac{\mathcal{K}_0(m)}{(m!)^q}$ ($0 \le m \le n$) has denominator dividing $\operatorname{den}(\mathcal{K}_0(m))\cdot(n!)^q$, which divides $D_n^{\mathcal{K}_0}(n!)^q = 2\bigl(\prod_{p\le 2n+1}p\bigr)(n!)^q$.
- **Lower bound (immune to irregular primes):** Fix any odd prime $3 \le p \le n$, and let $d_p := \frac{p-1}{2} \le \frac{n-1}{2}$, so $K_p := \lfloor n / d_p \rfloor \ge 2$. Among the two consecutive positive integers $\{K_p, K_p - 1\} \subset [1, K_p]$, at least one integer $k_p$ satisfies $k_p \not\equiv -1 \pmod p$. Define the witness index
  \[
  m_p := k_p d_p = k_p\frac{p-1}{2} \in \bigl[n - (p-2), \, n\bigr] \subset [1, n].
  \]
  At $m = m_p$:
  1. Since $2m_p = k_p(p-1)$ is a multiple of $p-1$, the von Staudt–Clausen theorem guarantees that $v_p(B_{2m_p}) = -1$ ($p$ divides the **denominator** of $B_{2m_p}$, so $p$ CANNOT divide the numerator of $B_{2m_p}$; irregular-prime numerator divisibility $p \mid \operatorname{num}(B_{2m})$ can only occur when $(p-1)\nmid 2m$!).
  2. Since $2m_p - 1 = k_p(p-1) - 1 \equiv -(k_p + 1) \not\equiv 0 \pmod p$, we have $v_p(2m_p - 1) = 0$.
  3. Consequently, the exact $p$-adic valuation of $\operatorname{den}(\mathcal{B}_q(m_p))$ is
     \[
     v_p\bigl(\operatorname{den}(\mathcal{B}_q(m_p))\bigr) = 1 + q\,v_p(m_p!).
     \]
  4. Because $0 \le n - m_p \le p - 2 < p - 1$, the short interval $(m_p, n]$ of length $\le p-2$ contains **at most one** multiple of $p^j$ for each $1 \le j \le \lfloor\log_p n\rfloor$, so $v_p(n!) - v_p(m_p!) = \sum_{j=1}^{\lfloor\log_p n\rfloor}\bigl(\lfloor n/p^j\rfloor - \lfloor m_p/p^j\rfloor\bigr) \le \lfloor\log_p n\rfloor$. Thus
     \[
     v_p(D_{q,n}) \ge v_p\bigl(\operatorname{den}(\mathcal{B}_q(m_p))\bigr) \ge 1 + q\,v_p(n!) - q\lfloor\log_p n\rfloor.
     \]
  Multiplying by $\log p$ and summing over $3 \le p \le n$ (noting $v_2(n!)\log 2 = O(n)$ and $\sum_{p\le n}\lfloor\log_p n\rfloor\log p = \psi(n) = O(n)$) proves the lower bound. $\square$

---

### J. Generating-function radii and factorial budget conservation table

At the critical exponent $q = 2$,
\[
|\mathcal{B}_2(m)| = \frac{(2m-1)|B_{2m}|}{2(m!)^2} = (2m-1)\binom{2m}{m}\tau^{-2m}\zeta(2m) \sim \frac{2\sqrt{m}}{\sqrt{\pi}}\left(\frac{2}{\tau}\right)^{2m} = \frac{2\sqrt{m}}{\sqrt{\pi}}\pi^{-2m},
\]
so $\mathcal{B}_2$ recovers a positive OGF radius of convergence $R_{\mathrm{OGF}}(\mathcal{B}_2) = \pi^2 = \tau^2/4 > 0$, but at the exact price of restoring the $2n\log n$ sample denominator growth!

| Family | $q$ | Sample Growth $\log|F(n)|$ | Sample Denominator $\log D_{q,n}$ | Total Budget $(\text{Growth} + \text{Denom})$ | $R_{\mathrm{OGF}}$ | Equispaced Basis Cost |
|---|---:|---|---|---|---|---|
| $\mathcal{B}(z), \mathcal{K}_0(z)$ | $0$ | $+2n\log n + O(n)$ | $2n + o(n)$ (`SUBFACTORIAL`) | $2n\log n + O(n)$ | $0$ | $+2n\log n$ (norm sq) |
| $\mathcal{B}_1(z)$ | $1$ | $+1n\log n + O(n)$ | $+1n\log n + O(n)$ | $2n\log n + O(n)$ | $0$ | $+2n\log n$ (norm sq) |
| $\mathcal{B}_2(z)$ | $2$ | $O(n)$ | $+2n\log n + O(n)$ | $2n\log n + O(n)$ | $\pi^2 = \tau^2/4$ | $+2n\log n$ (norm sq) |
| $\mathcal{R}_\tau(z)$ | $2^*$ | $-2n\log\tau + O(\log n)$ | $+2n\log n + O(n)$ | $2n\log n + O(n)$ | $\tau^2 = 4\pi^2$ | $+2n\log n$ (norm sq) |
| $\mathcal{B}_3(z)$ | $3$ | $-1n\log n + O(n)$ | $+3n\log n + O(n)$ | $2n\log n + O(n)$ | $+\infty$ | $+2n\log n$ (norm sq) |

Formalized in Lean 4 as `gamma_ratio_budget_conservation_identity` and `gamma_ratio_newton_basis_total_cost_conservation`.

---

### K. Sign-adjusted positive Bernoulli kernel \(\mathcal P(z)\)

Since $(-1)^{m+1}B_{2m} = |B_{2m}| > 0$ for every $m \ge 1$, multiplying $\mathcal{B}(z)$ by the entire nonvanishing exponential factor $-e^{i\tau z/2} = -e^{i\pi z}$ defines the sign-adjusted positive-sample kernel (`sign_adjusted_bernoulli_positive_sample_identity` in Lean 4):
\[
\boxed{
\mathcal{P}(z) := -e^{i\tau z/2}\mathcal{B}(z) = 2ze^{i\pi z}\zeta(1-2z), \qquad
\mathcal{P}(m) = -(-1)^m B_{2m} = (-1)^{m+1}B_{2m} = |B_{2m}| > 0 \quad (m \ge 1),
}
\]
with $\mathcal{P}(0) = -1$ and $\mathcal{P}(\rho/2) = 0$ for every nontrivial zero $\rho$ of $\zeta(s)$. (Note that $e^{i\pi z}$ breaks real-line reflection symmetry $\overline{\mathcal{P}(\bar{z})} \ne \mathcal{P}(z)$; its real-symmetric counterpart $\mathcal{P}_{\cos}(z) := -\cos(\tau z/2)\mathcal{B}(z)$ satisfies $\overline{\mathcal{P}_{\cos}(\bar{z})} = \mathcal{P}_{\cos}(z)$, $\mathcal{P}_{\cos}(m) = |B_{2m}| > 0$, and $\mathcal{P}_{\cos}(\rho/2) = 0$.)

---

### L. Positive Bernoulli Stieltjes moment measure and Hankel determinants \(H_n^{\mathcal B}\)

Shifting by one index defines the strictly positive sequence $\mu_m := \mathcal{P}(m+1) = (-1)^m B_{2m+2} = |B_{2m+2}| > 0$ ($m \ge 0$). Using the classical Mellin/Bose–Einstein integral for $\zeta(2m+2)$,
\[
|B_{2m+2}| = 4(m+1)\int_0^\infty \frac{x^{2m+1}}{e^{\tau x}-1}\,dx
= \frac{\tau}{2}\int_0^\infty \frac{x^{2m+2}}{\sinh^2(\tau x/2)}\,dx,
\]
and substituting $y = x^2$ ($dx = \frac{dy}{2\sqrt{y}}$) proves (`BERNOULLI_EVEN_ABSOLUTE_VALUES_STIELTJES_MOMENT_SEQUENCE_PROVED`):
\[
\boxed{
\mu_m = |B_{2m+2}| = \int_0^\infty y^m\,d\nu_\tau(y), \qquad
d\nu_\tau(y) = \frac{\tau\sqrt{y}}{4\sinh^2(\tau\sqrt{y}/2)}\,dy = \frac{\pi\sqrt{y}}{2\sinh^2(\pi\sqrt{y})}\,dy \quad \text{on } (0, \infty).
}
\]
Moreover, since $\mu_m^{-1/(2m)} \sim \frac{\pi e}{m}$, $\sum_{m=1}^\infty \mu_m^{-1/(2m)} = +\infty$, so $\mu_m$ satisfies **Carleman's determinacy condition** on $[0, \infty)$.

By the Carlitz–Touchard–Al-Salam continued-fraction theorem for Bernoulli moments, the Jacobi continued fraction of $\sum_{m=0}^\infty \mu_m w^{-m-1}$ has strictly positive recurrence coefficients (`carlitz_touchard_hankel_recurrence_positivity` in Lean 4):
\[
\boxed{
\beta_k^{\mathcal{B}} = \frac{H_{k+1}^{\mathcal{B}} H_{k-1}^{\mathcal{B}}}{(H_k^{\mathcal{B}})^2}
= \frac{k^3(k+1)(2k-1)(2k+1)^3}{(4k-1)(4k+1)^2(4k+3)} > 0 \qquad (k \ge 1),
}
\]
yielding the **exact closed-form product formula** for the Hankel determinants $H_n^{\mathcal{B}} := \det(\mu_{i+j})_{0\le i,j<n}$:
\[
\boxed{
H_n^{\mathcal{B}} = \frac{1}{6^n}\prod_{k=1}^{n-1}\left[\frac{k^3(k+1)(2k-1)(2k+1)^3}{(4k-1)(4k+1)^2(4k+3)}\right]^{n-k} > 0,
}
\]
and since $\beta_k^{\mathcal{B}} = \frac{k^4}{16}\bigl(1 + O(k^{-1})\bigr)$, Euler–Maclaurin summation gives the super-factorial growth law:
\[
\boxed{
\log H_n^{\mathcal{B}} = 2n^2\log n - (3 + 2\log 2)n^2 + O(n\log n) \longrightarrow +\infty.
}
\]

---

### M. Orthogonal polynomials and zeta-zero argument coupling audit

Let $P_n^{\mathcal{B}}(y) = y^n + \dots \in \mathbb{Q}[y]$ be the monic orthogonal polynomials for $d\nu_\tau(y)$ on $(0, \infty)$. We establish a strict structural firewall (`BERNOULLI_STIELTJES_HANKEL_POSITIVITY_DOES_NOT_COUPLE_TO_ZETA_ZERO_ARGUMENT`):
1. **Moment Variable vs. Mellin Zero Argument:** In the Stieltjes representation $\mu_m = \int_0^\infty y^m\,d\nu_\tau(y)$, the integer sample index $m$ appears in the **exponent** $y^m$ (so $z \mapsto \mathcal{P}(z)$ is a Mellin transform in $z$), whereas the orthogonal polynomials $P_n^{\mathcal{B}}(y)$ are polynomials in the **integration variable $y$** associated with the asymptotic Stieltjes transform $S_{\mathcal{B}}(w) = \int_0^\infty \frac{d\nu_\tau(y)}{w-y} \sim \sum_{m=0}^\infty \frac{|B_{2m+2}|}{w^{m+1}}$.
2. **No Vanishing or Smallness at $\alpha_1$ or $\gamma_1$:** Because $d\nu_\tau(y)$ is a positive measure supported on $(0, \infty)$, all $n$ roots $0 < y_{n,1} < \dots < y_{n,n}$ of $P_n^{\mathcal{B}}(y)$ are real and positive on $(0, \infty)$ with $\sum_{j=1}^n y_{n,j} \asymp n^3$. Evaluating the primitive integer polynomial $\widetilde{P}_n^{\mathcal{B}}$ at $\gamma_1$ gives $\log|\widetilde{P}_n^{\mathcal{B}}(\gamma_1)| = 8.22$ ($n=2$), $17.18$ ($n=4$), $25.35$ ($n=6$), diverging rapidly to $+\infty$.

---

### N. Comparison of \(D_n^{(\tau)}\) and \(H_n^{\mathcal B}\)

Comparing the Lambert–Stieltjes Hausdorff Hankel determinant $D_n^{(\tau)} = \det\bigl(\tau^{-2i-2j-2}\zeta(2i+2j+2)\bigr)$ from `TASK-TC-039R` with the Bernoulli Stieltjes Hankel determinant $H_n^{\mathcal{B}} = \det\bigl(|B_{2i+2j+2}|\bigr)$ reveals an exact structural duality:
\[
\boxed{
D_n^{(\tau)} = 24^{-n}\prod_{k=1}^{n-1}\left[\frac{1}{16(4k-1)(4k+1)^2(4k+3)}\right]^{n-k}, \qquad
H_n^{\mathcal{B}} = 6^{-n}\prod_{k=1}^{n-1}\left[\frac{k^3(k+1)(2k-1)(2k+1)^3}{(4k-1)(4k+1)^2(4k+3)}\right]^{n-k}.
}
\]
Both determinants share the **exact same polygonal denominator factors** $\prod_{k=1}^{n-1}\bigl[(4k-1)(4k+1)^2(4k+3)\bigr]^{n-k}$, while removing $\frac{1}{2(2m+2)!}$ from the moments inserts the degree-8 factorial numerator $16k^3(k+1)(2k-1)(2k+1)^3 \sim 256 k^8$ into $\beta_k^{\mathcal{B}}$, flipping the leading quadratic-factorial exponent from $-2n^2\log n$ to $+2n^2\log n$:

| $n$ | $H_n^{\mathcal{B}}$ (exact rational) | $\log H_n^{\mathcal{B}}$ | $\log D_n^{(\tau)}$ |
|---:|---|---:|---:|
| $1$ | $1/6$ | $-1.792$ | $-3.178$ |
| $2$ | $1/350$ | $-5.858$ | $-15.392$ |
| $3$ | $4/56595$ | $-9.557$ | $-39.117$ |
| $4$ | $128/11022011$ | $-11.363$ | $-75.850$ |
| $5$ | $955514880/25257378862001$ | $-10.182$ | $-126.675$ |
| $6$ | $(63\text{-bit}) / (70\text{-bit})$ | $-5.159$ | $-192.442$ |
| $8$ | $(156\text{-bit}) / (129\text{-bit})$ | $+18.423$ | $-371.491$ |
| $10$ | $(303\text{-bit}) / (206\text{-bit})$ | $+67.152$ | $-615.011$ |

---

### O. Equispaced Lagrange and Newton basis audit

Even when a kernel $f(z)$ has subfactorial sample denominators $D_n^{[f]} = e^{O(n)}$ (such as $\mathcal{B}(z)$ or $\mathcal{K}_0(z)$), expressing its degree-$n$ polynomial interpolant on equispaced integer nodes $m = 0, 1, \dots, n$ reintroduces $(n!)^2$ into the primitive norm polynomial (`EQUISPACED_NEWTON_LAGRANGE_BASIS_REINTRODUCES_FACTORIAL_DENOMINATOR`):

1. **Lagrange Basis Denominators:** $\ell_{n,m}(z) = \frac{(-1)^{n-m}}{m!(n-m)!}\prod_{j\ne m}(z-j) = \frac{(-1)^{n-m}\binom{n}{m}}{n!}\prod_{j\ne m}(z-j)$ carries $n!$ in its denominator.
2. **Universal Sample-Independent Newton Primitive Lower Bound:** For **any** rational sample sequence $f(m) \in \mathbb{Q}$ with $\Delta^{n+1}f(0) \ne 0$, the two-step Newton norm polynomial $Q_n^{[f]}(Y) = |N_n^{[f]}(\alpha(Y))|^2 + |N_{n+1}^{[f]}(\alpha(Y))|^2 \in \mathbb{Q}[Y]$ has leading coefficient $q_{n,2n+2}^{[f]} = \frac{(\Delta^{n+1}f(0))^2}{4^{n+1}((n+1)!)^2} > 0$. In the canonical primitive integer polynomial $\widetilde{Q}_n^{[f]}(Y) = M_n^{[f]} Q_n^{[f]}(Y) \in \mathbb{Z}[Y]$, the integer leading coefficient $\widetilde{q}_{n,2n+2}^{[f]} = M_n^{[f]} q_{n,2n+2}^{[f]} \ge 1$ forces $M_n^{[f]} \ge 1/q_{n,2n+2}^{[f]}$, which cancels $(\Delta^{n+1}f(0))^2$ identically and proves
   \[
   \boxed{
   \widetilde{Q}_n^{[f]}(\gamma_1) \ge \frac{1}{2}\prod_{j=0}^n\left[\left(2j-\frac{1}{2}\right)^2 + \gamma_1^2\right] \ge \frac{1}{2}\left(\frac{1}{4}+\gamma_1^2\right)(n!)^2 \longrightarrow +\infty
   }
   \]
   **universally for every sample sequence $f(m) \in \mathbb{Q}$**, including $\mathcal{B}(m)$, $\mathcal{K}_0(m)$, and $\mathcal{B}_q(m)$!
3. **Divergence of the Newton Series for $\mathcal{B}(z)$ and $\mathcal{K}_0(z)$:** Moreover, for $q = 0$, $|\Delta^n \mathcal{B}(0)| \sim |B_{2n}| \sim 2(2n)!\tau^{-2n}$, so $|\Delta^n \mathcal{B}(0)|/n! \sim 2\frac{(2n)!}{n!\tau^{2n}} \to +\infty$, meaning the raw Newton partial sums $N_n^{\mathcal{K}_0}(\alpha_1)$ and $N_n^{\mathcal{B}}(\alpha_1)$ also diverge factorially!

---

### P. Mahler \(p\)-adic and Nörlund–Bernoulli polynomial comparison

- **Mahler $p$-adic Interpolation vs. Archimedean Complex Zeros:** In $p$-adic analysis ($p \ge 3$), modifying $\frac{B_{2m}}{2m}$ by the Euler factor $(1 - p^{2m-1})$ produces Kummer congruences $\Delta_d^k c_m^{(p)} \equiv 0 \pmod{p^k}$ for $(p-1)\mid d$, yielding the Kubota–Leopoldt $p$-adic $L$-function $L_p(1-s, \omega^i)$ on $\mathbb{Z}_p$. In the archimedean metric $|\cdot|_\infty$ on $\mathbb{C}$, however, the factor $(1 - p^{2m-1})$ amplifies sample growth by $p^{2m}$ without cancelling $(2m)!$, and $p$-adic Mahler series on $\mathbb{Z}_p$ cannot be evaluated at the complex archimedean zero $\alpha_1 = \frac{1}{4} + i\frac{\gamma_1}{2} \in \mathbb{C}$.
- **Nörlund–Bernoulli Polynomial Expansions:** Expanding $\mathcal{B}(z)$ or $\mathcal{K}_0(z)$ in Bernoulli polynomials $B_k(z) = \sum_{j=0}^k \binom{k}{j}B_j z^{k-j}$ or Nörlund polynomials $B_k^{(r)}(z)$ shifts the polynomial basis by a lower-triangular rational matrix whose inverse still carries $(2k)!$ or Carlitz–Hankel determinants of order $\exp(2n^2\log n)$.

---

### Q. Entire Hadamard / Riesz–Gram kernel audit

We audit whether classical entire or Mellin-transformed zeta kernels avoid the factorial obstruction (`RIESZ_GRAM_HADAMARD_KERNELS_DO_NOT_SIMULTANEOUSLY_PRESERVE_RATIONAL_SAMPLES_AND_INDIVIDUAL_ZERO_VANISHING`):
1. **Riesz's Function and Baez-Duarte Coefficients:** Riesz's function $\operatorname{Riesz}(x) = \sum_{k=1}^\infty \frac{(-1)^{k+1}x^k}{(k-1)!\zeta(2k)}$ satisfies $\int_0^\infty x^{-s-1}\operatorname{Riesz}(x)\,dx = \frac{\Gamma(-s)}{\zeta(2s)}$. However: (a) its coefficients $\frac{1}{(k-1)!\zeta(2k)} = \frac{2(2k)!}{(k-1)!|B_{2k}|\tau^{2k}}$ are transcendental multiples of $\tau^{-2k}$, not rationals; and (b) its connection to zeros is the global asymptotic $\operatorname{Riesz}(x) = O(x^{1/4+\varepsilon})$ as $x \to \infty$ (or Baez-Duarte $c_n = O(n^{-3/4+\varepsilon})$), not point vanishing at an individual zero $\rho_1/2$.
2. **Gram Series and Hadamard Product Kernels:** The Gram series $1 + \sum_{k=1}^\infty \frac{(\log x)^k}{k\,k!\zeta(k+1)}$ has irrational coefficients $\zeta(k+1)^{-1}$, while the Hadamard product $\xi(s) = \xi(0)\prod_\rho(1 - s/\rho)$ has transcendental Taylor/interpolation values at integer nodes.

---

### R. Multipoint Padé comparison across \(\mathcal R_c\), \(\mathcal B_2\), \(\mathcal B_1\), \(\mathcal B\), \(\mathcal K_0\)

For each kernel $f \in \{\mathcal{R}_\tau, \mathcal{R}_\pi, \mathcal{B}_2, \mathcal{B}_1, \mathcal{K}_0\}$, we solve the exact $[n/n]$ multipoint Padé interpolation problem $A_n(m) - f(m)B_n(m) = 0$ on $m = 0, 1, \dots, 2n$ for $1 \le n \le 7$, form the two-step norm polynomial $Q_{n,\mathrm{Pade}}^{[f]}(Y) = \mathcal{N}_{A_n}(Y) + \mathcal{N}_{A_{n+1}}(Y) \in \mathbb{Q}[Y]$, and compute its canonical primitive integer polynomial $\widetilde{Q}_{n,\mathrm{Pade}}^{[f]}(Y) = \frac{L_n}{g_n} Q_{n,\mathrm{Pade}}^{[f]}(Y) \in \mathbb{Z}[Y]$ (`MULTIPOINT_PADE_KERNEL_COMPARISON_FAVORS_BOUNDED_RADIUS_CLASSES_ONLY`, `ALL_N_MULTIPOINT_PADE_ASYMPTOTIC_STILL_OPEN`):

| Kernel Family | $n$ | $\deg\widetilde{Q}_{n,\mathrm{Pade}}$ | $\log\left|\frac{A_n(\alpha_1)}{B_n(\alpha_1)}\right|$ (Norm-Invariant Raw Error) | $\log M_n^{\mathrm{prim}} = \log(L_n/g_n)$ | $\log\widetilde{Q}_{n,\mathrm{Pade}}(\gamma_1)$ | $\mathscr{E}_{n,\mathrm{Pade}}^{\mathrm{prim}}$ |
|---|---:|---:|---:|---:|---:|---:|
| $\mathcal{K}_0$ ($q=0$, subfactorial $D_n$) | $2$ | $6$ | $-1.93$ | $69.77$ | $+79.52$ | $-13.253$ |
| $\mathcal{K}_0$ ($q=0$, subfactorial $D_n$) | $4$ | $10$ | $-0.44$ | $174.42$ | $+198.03$ | $-19.803$ |
| $\mathcal{K}_0$ ($q=0$, subfactorial $D_n$) | $6$ | $14$ | $+1.62$ | $364.88$ | $+404.57$ | $-28.898$ |
| $\mathcal{B}_1$ ($q=1$, $R_{\mathrm{OGF}}=0$) | $2$ | $6$ | $-3.25$ | $102.00$ | $+106.42$ | $-17.737$ |
| $\mathcal{B}_1$ ($q=1$, $R_{\mathrm{OGF}}=0$) | $4$ | $10$ | $-4.19$ | $272.54$ | $+285.12$ | $-28.512$ |
| $\mathcal{B}_1$ ($q=1$, $R_{\mathrm{OGF}}=0$) | $6$ | $14$ | $-4.41$ | $588.78$ | $+611.78$ | $-43.699$ |
| $\mathcal{B}_2$ ($q=2$, $R_{\mathrm{OGF}}=\pi^2$) | $2$ | $6$ | $-4.32$ | $136.64$ | $+136.83$ | $-22.804$ |
| $\mathcal{B}_2$ ($q=2$, $R_{\mathrm{OGF}}=\pi^2$) | $4$ | $10$ | $-7.79$ | $406.15$ | $+408.01$ | $-40.801$ |
| $\mathcal{B}_2$ ($q=2$, $R_{\mathrm{OGF}}=\pi^2$) | $6$ | $14$ | $-10.93$ | $881.03$ | $+885.89$ | $-63.278$ |
| $\mathcal{R}_\pi$ ($c=4$, $R_{\mathrm{OGF}}=\pi^2$) | $2$ | $6$ | $-2.99$ | $95.05$ | $+98.44$ | $-16.407$ |
| $\mathcal{R}_\pi$ ($c=4$, $R_{\mathrm{OGF}}=\pi^2$) | $4$ | $10$ | $-5.63$ | $329.68$ | $+335.81$ | $-33.581$ |
| $\mathcal{R}_\pi$ ($c=4$, $R_{\mathrm{OGF}}=\pi^2$) | $6$ | $14$ | $-7.81$ | $773.46$ | $+783.69$ | $-55.978$ |
| $\mathcal{R}_\tau$ ($c=1$, $R_{\mathrm{OGF}}=\tau^2$) | $2$ | $6$ | $-5.91$ | $158.73$ | $+154.89$ | $-25.815$ |
| $\mathcal{R}_\tau$ ($c=1$, $R_{\mathrm{OGF}}=\tau^2$) | $4$ | $10$ | $-11.57$ | $485.78$ | $+478.67$ | $-47.867$ |
| $\mathcal{R}_\tau$ ($c=1$, $R_{\mathrm{OGF}}=\tau^2$) | $6$ | $14$ | $-16.87$ | $1072.42$ | $+1063.20$ | $-75.943$ |

Even for $\mathcal{K}_0$—whose sample denominators are strictly squarefree primorials $D_n^{\mathcal{K}_0} = 2\prod_{p\le 2n+1}p$—solving the $[n/n]$ Padé linear system by Cramer's rule forms determinants of the $(2m)!$-growing numerators of $B_{2m}$, producing $\log M_6^{\mathrm{prim}} = 364.88$ and $\log\widetilde{Q}_{6,\mathrm{Pade}}^{\mathcal{K}_0}(\gamma_1) = +404.57$.

---

### S. Primitive integer normalization across all routes

Every candidate route in `TASK-TC-040` has been evaluated under **canonical primitive integer normalization** $\widetilde{Q}_n(Y) = \frac{L_n}{g_n} Q_n(Y) \in \mathbb{Z}[Y]$ with $\gcd_j(\widetilde{q}_{n,j}) = 1$:
- **Consecutive Newton on $\mathcal{R}_\tau, \mathcal{R}_\pi, \mathcal{K}_0, \mathcal{B}, \mathcal{B}_q$:** Rigorously diverges for all $n$ (`tilde{Q}_n(gamma_1) >= (1/2) prod_{j=0}^n ((2j-1/2)^2 + gamma_1^2) -> +infty`).
- **Stieltjes–Hankel orthogonal polynomials $\widetilde{P}_n^{\mathcal{B}}(y)$:** Variable $y$ is the Stieltjes moment variable on $(0, \infty)$; $\log|\widetilde{P}_6^{\mathcal{B}}(\gamma_1)| = +25.35 \to +\infty$.
- **Multipoint Padé on $\mathcal{K}_0, \mathcal{B}_1, \mathcal{B}_2, \mathcal{R}_\pi, \mathcal{R}_\tau$:** $\log\widetilde{Q}_{n,\mathrm{Pade}}(\gamma_1) > 0$ and strictly increasing across $1 \le n \le 7$ for all five families.

---

### T. Factorial-relocation analysis

Our investigation proves that across the Gamma-reflection and Gamma-ratio architecture on equispaced integer nodes, **the factorial cost $(2n)! \asymp \exp(2n\log n)$ cannot be destroyed; it can only be relocated across five coupled channels** (`FACTORIAL_RELOCATION_ACROSS_DENOMINATOR_GROWTH_AND_BASIS_PROVED`, formalized in Lean 4 as `auxiliary_polynomial_factorial_cost_lower_bound_schema`):

1. **Channel 1 — Sample Denominators ($q\,n\log n$):** Absorbs the full $2n\log n$ cost at $q = 2$ ($\mathcal{B}_2, \mathcal{R}_\tau, \mathcal{R}_\pi$) and reduces to $2n + o(n)$ (`SUBFACTORIAL`) at $q = 0$ ($\mathcal{B}, \mathcal{K}_0$).
2. **Channel 2 — Sample Magnitudes ($(2-q)n\log n$):** Vanishes at $q = 2$, but absorbs the full $+2n\log n$ factorial growth at $q = 0$ ($|B_{2m}| = 2(2m)!\tau^{-2m}\zeta(2m)$), destroying OGF convergence ($R_{\mathrm{OGF}} = 0$).
3. **Channel 3 — Equispaced Interpolation Basis Denominators ($2n\log n$ in norm square):** The equispaced nodes $m = 0, \dots, n$ introduce $1/(n!)^2$ into the leading coefficient of $Q_n(Y)$, which in primitive normalization forces $\widetilde{Q}_n(\gamma_1) \ge \frac{1}{2}\prod_{j=0}^n\bigl((2j-\tfrac{1}{2})^2 + \gamma_1^2\bigr)$ regardless of Channels 1 and 2.
4. **Channel 4 — Hankel / Cramer Determinant Clearing ($\Theta(n^2\log n)$):** Passing from polynomial to rational/Padé or Hankel determinantal elimination squares the factorial scale to $\Theta(n^2\log n)$ via either $\operatorname{lcm}\operatorname{den}$ ($q=2$) or Vandermonde-weighted sample numerators ($q=0$).
5. **Channel 5 — Entire Multiplier Growth:** Multiplying $\mathcal{R}_\tau(z)$ by $\Gamma(2z+1)\cos(\tau z/2)/\Gamma(z+1)^q$ injects Stirling growth $(2-q)\operatorname{Re}(z)\log|z|$ in the right half-plane and order-$q$ poles of $\Gamma(z+1)^q$ at negative integers.

---

### U. Subfactorial escape or conditional no-go theorem

#### Theorem (`EQUISPACED_GAMMA_REFLECTION_CLASS_NO_GO_PROVED`)

Let $\mathcal{F}_q^{(c)}(z) := c^z \frac{\mathcal{K}_0(z)}{\Gamma(z+1)^q} = c^z \frac{z(2z-1)\zeta(1-2z)}{\Gamma(z+1)^q}$ ($q \in \mathbb{Z}_{\ge 0}$, $c \in \mathbb{Q}_{>0}$) be any kernel in the Gamma-reflected / Gamma-ratio hierarchy sampled on equispaced integer nodes $m = 0, 1, \dots, n$. Then:
1. **Exact Sample-Growth + Sample-Denominator Conservation:** By Euler's even-zeta identity and the irregular-prime-free von Staudt–Clausen witness $m_p = k_p\frac{p-1}{2}$,
   \[
   \boxed{
   \log\bigl|\mathcal{F}_q^{(c)}(n)\bigr| = (2-q)n\log n + O_{q,c}(n), \qquad
   \log\Bigl(\operatorname{lcm}_{0\le m\le n}\operatorname{den}\bigl(\mathcal{F}_q^{(c)}(m)\bigr)\Bigr) = q\,n\log n + O_{q,c}(n),
   }
   \]
   so their sum is identically $2n\log n + O_{q,c}(n)$ for every $q \ge 0$ and every $c \in \mathbb{Q}_{>0}$.
2. **Universal Consecutive-Newton Primitive Obstruction:** For any rational sample sequence $f(m) \in \mathbb{Q}$ (including $\mathcal{F}_q^{(c)}(m)$ for all $q \ge 0$, $\mathcal{B}(m)$, and $\mathcal{R}_c(m)$) and every $n \ge 0$ with $\Delta^{n+1}f(0) \ne 0$, the canonical primitive integer two-approximant Newton norm polynomial $\widetilde{Q}_n^{[f]}(Y) \in \mathbb{Z}[Y]$ satisfies
   \[
   \boxed{
   \widetilde{Q}_n^{[f]}(Y) \ge \frac{1}{2}\prod_{j=0}^n\left[\left(2j-\frac{1}{2}\right)^2 + Y^2\right] \ge \frac{1}{2}\left(\frac{1}{4}+Y^2\right)(n!)^2 \longrightarrow +\infty \qquad (\forall Y \in \mathbb{R}).
   }
   \]

Consequently, **no kernel in the equispaced Gamma-reflection / Gamma-ratio class can achieve positive Diophantine efficiency $\limsup_{n\to\infty} \mathscr{E}_n^{\mathrm{prim}} > 0$ via equispaced polynomial interpolation**.

---

### V. Diophantine efficiency comparison table

| Architecture | Sample Denom $\log D_n$ | Sample Growth $\log|f(n)|$ | Raw Residual $\log|Q_n(\gamma_1)|$ | Primitive Clearing $\log M_n$ | Primitive Eval $\log\widetilde{Q}_n(\gamma_1)$ | $\limsup \mathscr{E}_n^{\mathrm{prim}}$ | Gate Z5 Status |
|---|---|---|---|---|---|---|---|
| Consecutive Newton on $\mathcal{R}_\tau, \mathcal{R}_\pi$ | $2n\log n + O(n)$ | $O(n)$ | $-2\kappa(c)n^{1/3}$ | $2n\log n + 2\kappa(c)n^{1/3} + O(n)$ | $\ge 2n\log n - O(n) \to +\infty$ | $-\infty$ | `CLOSED_NEGATIVE` |
| Consecutive Newton on $\mathcal{K}_0, \mathcal{B}$ ($q=0$) | $2n + o(n)$ (**subfactorial**) | $2n\log n + O(n)$ | $+2n\log n + O(n)$ | Universal cancellation | $\ge 2n\log n - O(n) \to +\infty$ | $-\infty$ | `CLOSED_NEGATIVE` |
| Consecutive Newton on $\mathcal{B}_2$ ($q=2$) | $2n\log n + O(n)$ | $O(n)$ | Algebraic / log | $\ge 2n\log n + O(n)$ | $\ge 2n\log n - O(n) \to +\infty$ | $-\infty$ | `CLOSED_NEGATIVE` |
| Bernoulli Stieltjes–Hankel $P_n^{\mathcal{B}}(y)$ | $2n + o(n)$ (**subfactorial**) | $2n\log n + O(n)$ | $+2n\log n + O(n)$ | $O(n^2)$ | $\to +\infty$ (decoupled) | $-\infty$ | `DECOUPLED_Z1_Z5` |
| Multipoint Padé $[n/n]$ on $\mathcal{K}_0, \mathcal{B}_1$ | $4n + o(n)$ / $2n\log n$ | $(2-q)2n\log n$ | $> 0$ ($R_{\mathrm{OGF}}=0$) | $\Theta(n^2\log n)$ | $+404.57$ ($n=6$) | $< 0$ | `REFUTED_FINITE` |
| Multipoint Padé $[n/n]$ on $\mathcal{R}_\tau, \mathcal{R}_\pi, \mathcal{B}_2$ | $4n\log n + O(n)$ | $O(n)$ | $< 0$ ($R_{\mathrm{OGF}}>0$) | $\Theta(n^2\log n)$ ($n\le 7$) | $+783.69$ to $+1063.20$ ($n=6$) | $< 0$ ($n\le 7$) | `OPEN` (all-$n$ Padé) |

---

### W. Numerical audit at \(\gamma_1\) and mandatory controls

1. **First Nontrivial Zero $\gamma_1 = 14.13472514173469379\dots$ ($\alpha_1 = \frac{1}{4} + i\frac{\gamma_1}{2}$):**
   At 60-digit working precision, $|\mathcal{R}_\tau(\alpha_1)|, |\mathcal{K}_0(\alpha_1)|, |\mathcal{B}(\alpha_1)|, |\mathcal{B}_2(\alpha_1)|, |\mathcal{P}(\alpha_1)| < 10^{-58}$, confirming exact simultaneous vanishing across all five kernels.
2. **Synthetic Rational Zero Control ($\alpha_* = \frac{1}{4} + 7i$, $\gamma_* = 14$, $b = 1$):**
   Evaluating the primitive integer Newton norm polynomial $\widetilde{Q}_3^{\mathcal{K}_0}(Y) \in \mathbb{Z}[Y]$ ($\gcd = 1$) at $\gamma_* = 14$ yields the exact positive integer $\widetilde{Q}_3^{\mathcal{K}_0}(14) = 19784196452698409 \ge 1$, verifying the integer-clearing lower bound $b^{\deg\widetilde{Q}_n}\widetilde{Q}_n(a/b) \ge 1$.
3. **Trivial Zero Control ($\rho_{\mathrm{triv}} = -2$, $z = -1$ vs. $z = 3/2$):**
   At $z = -1$ ($2z = -2$), $\mathcal{R}_\tau(-1) = 0$ while $\mathcal{B}(-1) = 2\zeta(3) \approx 2.4041138 \ne 0$ and $\mathcal{K}_0(-1) = 3\zeta(3) \approx 3.6061707 \ne 0$. Conversely, at $z = 3/2$ ($1-2z = -2$), $\mathcal{B}(3/2) = \mathcal{K}_0(3/2) = 0$ while $\mathcal{R}_\tau(3/2) = 2\tau^{-3}\zeta(3) \approx 9.6917 \times 10^{-3} \ne 0$.
4. **Davenport–Heilbronn Counterexample Control:**
   The Gamma-reflection identity $\mathcal{K}_0(z) = \Gamma(2z+1)\cos(\tau z/2)\mathcal{R}_\tau(z)$ and the factorial budget conservation law $(2-q)n\log n + q\,n\log n = 2n\log n$ depend solely on the functional equation and Stirling's formula, not on the Euler product. For the Davenport–Heilbronn function (which has a functional equation and off-line zeros but no Euler product), irrational Gauss-sum linear combination coefficients already break rational sampling at Gate Z2, whereas for $\zeta(s)$ rational Bernoulli samples pass Gate Z2 with $O(n)$ log-denominator but are blocked at Gate Z5 by factorial relocation.
5. **Off-Line Hypothetical Zero Control ($\rho_{\mathrm{off}} = \beta + i\gamma$, $\beta \ne 1/2$):**
   Because the functional equation gives $\zeta(\rho_{\mathrm{off}}) = 0 \iff \zeta(1-\rho_{\mathrm{off}}) = 0$ unconditionally, $\mathcal{B}(\rho_{\mathrm{off}}/2) = \mathcal{K}_0(\rho_{\mathrm{off}}/2) = 0$ holds for any nontrivial zero whether on-line or off-line, with $(1 + \alpha_{\mathrm{off}})(1 + \overline{\alpha_{\mathrm{off}}}) = (1 + \beta/2)^2 + \gamma^2/4$ depending on both $\beta$ and $\gamma$.

---

### X. Updated Z1–Z5 gate status table

| Gate | Requirement | $\mathcal{R}_\tau, \mathcal{R}_\pi$ | $\mathcal{K}_0, \mathcal{B}$ ($q=0$) | $\mathcal{B}_2$ ($q=2$) | Bernoulli Stieltjes $P_n^{\mathcal{B}}(y)$ |
|---|---|---|---|---|---|
| **Z1** | Zero-argument vanishing $F(\rho/2) = 0$ | **PASSED** | **PASSED** (`BERNOULLI_FUNCTION_NONTRIVIAL_ZETA_ZERO_BRIDGE_PROVED`) | **PASSED** | **FAILED** (variable $y \ne \rho/2$) |
| **Z2** | Rational samples $F(m) \in \mathbb{Q}$ & subfactorial $\log D_n = O(n)$ | Rational **PASSED**; subfactorial **FAILED** ($2n\log n$) | **PASSED BOTH** ($D_n^{\mathcal{B}} = \prod_{p\le 2n+1}p = e^{2n+o(n)}$) | Rational **PASSED**; subfactorial **FAILED** ($2n\log n$) | Moments $|B_{2m+2}| \in \mathbb{Q}_{>0}$ **PASSED** |
| **Z3** | Nonvanishing auxiliary polynomial $Q_n(\gamma_1) > 0$ | **PASSED** | **PASSED** | **PASSED** | **PASSED** on $\mathbb{C}\setminus(0,\infty)$ |
| **Z4** | Raw analytic smallness at $\alpha_1$ | **PASSED** ($e^{-2\kappa(c)n^{1/3}}$) | **FAILED** (Newton & Padé diverge, $R_{\mathrm{OGF}}=0$) | **PASSED** (Padé raw error $<0$) | **FAILED** (zeros on $(0,\infty)$) |
| **Z5** | Primitive integer Diophantine efficiency $\widetilde{Q}_n(\gamma_1) \to 0$ | **CLOSED_NEGATIVE** (Newton); **OPEN** (all-$n$ Padé) | **CLOSED_NEGATIVE** (`EQUISPACED_GAMMA_REFLECTION_CLASS_NO_GO_PROVED`) | **CLOSED_NEGATIVE** (Newton); negative for $n\le 7$ Padé | **CLOSED_NEGATIVE** |

---

### Y. Updated status of `SUBGATE-TC-040A`, `SUBGATE-TC-039A`, `SUBGATE-TC-038A`, and `OBL-CT-001A`

- **`SUBGATE-TC-040A`:** `CLOSED_FOR_EQUISPACED_GAMMA_REFLECTION_CLASS_AT_GATE_Z5` (`SUBFACTORIAL_RATIONAL_SAMPLE_DENOMINATOR_ACHIEVED`; `EQUISPACED_GAMMA_REFLECTION_CLASS_NO_GO_PROVED`; `FACTORIAL_RELOCATION_ACROSS_DENOMINATOR_GROWTH_AND_BASIS_PROVED`).
- **`SUBGATE-TC-039A [Newton]`:** `CLOSED_NEGATIVE_AT_GATE_Z5` (`CONSECUTIVE_NEWTON_PRIMITIVE_NORM_FACTORIAL_OBSTRUCTION`).
- **`SUBGATE-TC-039A [Padé asymptotic]`:** `OPEN` (`ALL_N_MULTIPOINT_PADE_ASYMPTOTIC_STILL_OPEN` — finite data $1 \le n \le 7$ strongly negative across $\mathcal{R}_\tau, \mathcal{R}_\pi, \mathcal{B}_2, \mathcal{B}_1, \mathcal{K}_0$).
- **`SUBGATE-TC-038A`:** `OPEN`.
- **`OBL-CT-001A`:** `OPEN`.

---

### Z. Exact next step

With the equispaced Newton route (`SUBGATE-TC-039A [Newton]`) and the equispaced Gamma-reflection / Gamma-ratio class (`SUBGATE-TC-040A`) rigorously closed at Gate Z5 by factorial conservation and primitive leading-coefficient cancellation, only two mathematically distinct avenues remain open for `SUBGATE-TC-039A` / `SUBGATE-TC-038A`:
1. **All-$n$ Multipoint Padé Lower Bound (`SUBGATE-TC-039A [Padé asymptotic]`):** Prove an analytic lower bound on the primitive integer multipoint Padé norm polynomial $\widetilde{Q}_{n,\mathrm{Pade}}^{(c)}(\gamma_1)$ (via potential theory / Hermite–Walsh contour asymptotics and Cramer determinant denominator valuations) to formally close the remaining Padé subproblem of `SUBGATE-TC-039A`.
2. **Non-Equispaced / Non-Integer Rational-Sample Architectures:** Investigate whether any zero-carrying functional equation or modular/theta bridge admits rational evaluations on a **non-equispaced** rational node set whose basis denominators and sample heights simultaneously stay bounded by $e^{O(n)}$.
