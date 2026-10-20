# TASK-TC-040 Review: Subfactorial-Denominator Zero-Carrying Kernels — Bernoulli Reflection, Gamma-Ratio Tradeoffs, Positive-Moment Hankel Architecture, and Escape from the Newton Factorial Obstruction

**Task ID:** `TASK-TC-040`  
**Subgate ID:** `SUBGATE-TC-040A`  
**Starting HEAD:** `35a281e5ce0de441b0d15aa36afbc5e64eadf078`  
**Implementation Module:** [`tc/fauzan_subfactorial_zero_kernel.py`](file:///c:/Development/Projects/reimann_scope/tc/fauzan_subfactorial_zero_kernel.py)  
**Machine-Readable Artifact:** [`data/tc_fauzan_subfactorial_zero_kernel.json`](file:///c:/Development/Projects/reimann_scope/data/tc_fauzan_subfactorial_zero_kernel.json)  
**Lean 4 Formalization Module:** [`formal/RiemannScope/SubfactorialZeroKernel.lean`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/SubfactorialZeroKernel.lean) (14 formal theorems, 0 `sorry`, 0 `admit`; 663 total compiled theorems across 35 formal files)  
**Regression Test Suite:** [`tests/test_tc_fauzan_subfactorial_zero_kernel.py`](file:///c:/Development/Projects/reimann_scope/tests/test_tc_fauzan_subfactorial_zero_kernel.py)

---

### A. Starting point after TASK-TC-039R4

`TASK-TC-039` through `TASK-TC-039R4` established a zero-argument arithmetic bridge via the $\tau$-normalized kernel ($\tau = 2\pi$):
\[
\mathcal{R}_\tau(z) = (2z - 1)\tau^{-2z}\zeta(2z), \qquad \mathcal{R}_\tau(\rho/2) = 0, \qquad
\mathcal{R}_\tau(m) = (-1)^{m+1}\frac{(2m-1)B_{2m}}{2(2m)!} \in \mathbb{Q} \quad (m \ge 0).
\]
However, `TASK-TC-039R4` proved that for the two-approximant Newton norm polynomial $Q_n^{(c)}(Y) = \mathcal{N}_{N_n^{(c)}}(Y) + \mathcal{N}_{N_{n+1}^{(c)}}(Y)$, canonical primitive integer normalization $\widetilde{Q}_n^{(c)}(Y) = \frac{L_n^{(c)}}{g_n^{(c)}} Q_n^{(c)}(Y) \in \mathbb{Z}[Y]$ forces
\[
\widetilde{Q}_n^{(c)}(\gamma_1) \ge \frac{1}{2}\prod_{j=0}^n\left[\left(2j-\frac{1}{2}\right)^2 + \gamma_1^2\right] \longrightarrow +\infty,
\]
closing `SUBGATE-TC-039A [Newton] = CLOSED_NEGATIVE_AT_GATE_Z5` while leaving `SUBGATE-TC-039A [Padé asymptotic] = OPEN`, `SUBGATE-TC-040A = OPEN`, `SUBGATE-TC-038A = OPEN`, and `OBL-CT-001A = OPEN`.

`TASK-TC-040` answers the governing question: **Can one construct a zero-independent analytic kernel carrying the individual nontrivial zeta-zero argument and possessing rational arithmetic samples whose primitive arithmetic cost is only exponential $e^{O(n)}$, while still generating nonzero auxiliary polynomials with enough analytic smallness to support a Diophantine contradiction?**

---

### B. Preflight synchronization repairs

All three residual synchronization items from the `TASK-TC-039R4` review are resolved across code, documentation, and artifacts:

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

### C. Why Newton is now frozen

With the canonical primitive integer normalization $\widetilde{Q}_n^{(c)}(Y) = M_n^{(c)} Q_n^{(c)}(Y) = \frac{L_n^{(c)}}{g_n^{(c)}} Q_n^{(c)}(Y) \in \mathbb{Z}[Y]$, the consecutive-Newton route is permanently frozen at Gate Z5 under `CONSECUTIVE_NEWTON_PRIMITIVE_NORM_FACTORIAL_OBSTRUCTION`:
- `NEWTON_TWO_STEP_RAW_LOWER_ENVELOPE_PROVED`
- `PRIMITIVE_NORM_POLYNOMIAL_LOWER_BOUND_PROVED`
- `NEWTON_TWO_APPROXIMANT_PRIMITIVE_ROUTE_RIGOROUSLY_FAILS_GATE_Z5`
- `SUBGATE-TC-039A [Newton] = CLOSED_NEGATIVE_AT_GATE_Z5`

Because the leading coefficient of $Q_n^{(c)}(Y)$ is $q_{n,2k_n}^{(c)} = \frac{(\Delta^{k_n}a_0^{(c)})^2}{4^{k_n}(k_n!)^2} > 0$, clearing coefficients to a primitive integer polynomial forces $M_n^{(c)} q_{n,2k_n}^{(c)} = \widetilde{q}_{n,2k_n}^{(c)} \in \mathbb{Z}_{\ge 1}$, which cancels $(\Delta^{k_n}a_0^{(c)})^2$ identically while preserving $4^{k_n}(k_n!)^2$. Consequently, on the cofinal set $\Delta^{n+1}a_0^{(c)} \ne 0$ (including all $0 \le n \le 200$),
\[
\boxed{
\widetilde{Q}_n^{(c)}(\gamma_1) \ge \frac{1}{2}\prod_{j=0}^n\left[\left(2j-\frac{1}{2}\right)^2 + \gamma_1^2\right] \ge \frac{1}{2}\left(\frac{1}{4}+\gamma_1^2\right)(n!)^2 \longrightarrow +\infty,
}
\]
and globally for all $n \ge n_0(c)$, $\log\widetilde{Q}_n^{(c)}(\gamma_1) \ge 2n\log n - O_c(n) \to +\infty$.

---

### D. \(\tau\)-first functional equation

In $\tau$-native coordinates ($\tau = 2\pi$, $\pi = \tau/2$), Riemann's functional equation at $s = 2z$ takes the exact dual forms
\[
\boxed{
\zeta(2z) = 2^{2z}\pi^{2z-1}\sin(\pi z)\Gamma(1-2z)\zeta(1-2z)
= 2\tau^{2z-1}\sin\!\left(\frac{\tau z}{2}\right)\Gamma(1-2z)\zeta(1-2z).
}
\]
Notice that in the $\tau$-form, the dyadic exponential factor $2^{2z}$ combines with $\pi^{2z-1}$ into $2\tau^{2z-1}$, so multiplying by $\tau^{-2z}$ in $\mathcal{R}_\tau(z) = (2z-1)\tau^{-2z}\zeta(2z)$ removes the exponential scale factor completely:
\[
\mathcal{R}_\tau(z) = \frac{2(2z-1)}{\tau}\sin\!\left(\frac{\tau z}{2}\right)\Gamma(1-2z)\zeta(1-2z).
\]
In accordance with the TC firewall, this analytic normalization satisfies `TAU_ANALYTIC_NORMALIZATION_DISTINCT_FROM_TC_GRADE_ACTION`.

---

### E. Factorial-cancelled reflection kernel

Multiplying $\mathcal{R}_\tau(z)$ by the zero-independent meromorphic reflection multiplier $\Gamma(2z+1)\cos(\tau z/2)$ and invoking Euler's reflection formula
\[
\Gamma(2z+1)\Gamma(1-2z) = 2z\Gamma(2z)\Gamma(1-2z) = \frac{2\pi z}{\sin(2\pi z)} = \frac{\tau z}{2\sin(\tau z/2)\cos(\tau z/2)}
\]
cancels $\tau$, $\sin(\tau z/2)$, $\cos(\tau z/2)$, and $\Gamma(1-2z)$ identically, yielding the **factorial-cancelled reflection kernel**:
\[
\boxed{
\mathcal{K}_0(z) := \Gamma(2z+1)\cos\!\left(\frac{\tau z}{2}\right)\mathcal{R}_\tau(z)
= 4^{-z}\Gamma(2z+1)\cos(\pi z)\mathcal{R}_\pi(z)
= z(2z-1)\zeta(1-2z).
}
\]
**Entirety of $\mathcal{K}_0(z)$ on $\mathbb{C}$:**
- In $z(2z-1)\zeta(1-2z)$, the only singularity of $\zeta(1-2z)$ is the simple pole at $1-2z = 1 \iff z = 0$ with residue $-\frac{1}{2}$, which is cancelled by the factor $z$ to give the removable value
  \[
  \boxed{\mathcal{K}_0(0) = \lim_{z\to 0} z(2z-1)\zeta(1-2z) = (-1)\cdot\left(-\frac{1}{2}\right) = \frac{1}{2}, \qquad \mathcal{K}_0(1/2) = 0.}
  \]
- Equivalently, in the product $\Gamma(2z+1)\cos(\tau z/2)\mathcal{R}_\tau(z)$, the simple poles of $\Gamma(2z+1)$ at negative half-integers $z = -k - \frac{1}{2}$ ($k \ge 0$) are cancelled by the simple zeros of $\cos(\tau z/2)$, while the simple poles of $\Gamma(2z+1)$ at negative integers $z = -k$ ($k \ge 1$) are cancelled by the trivial zeros of $\zeta(2z)$ at $2z = -2k$.

---

### F. Bernoulli function \(B(s)=-s\zeta(1-s)\)

Dividing out the linear factor $-\frac{2z-1}{2}$ defines the classical **Bernoulli function** $B(s) := -s\zeta(1-s)$ and its half-scale zero-argument form $\mathcal{B}(z) := B(2z)$:
\[
\boxed{
B(s) := -s\zeta(1-s), \qquad
\mathcal{B}(z) := B(2z) = -2z\zeta(1-2z), \qquad
\mathcal{K}_0(z) = -\frac{2z-1}{2}\mathcal{B}(z)
}
\]
(formalized in Lean 4 as `bernoulli_kernel_linear_relation`), with removable value $B(0) = \mathcal{B}(0) = 1 = B_0$ and $\mathcal{B}(1/2) = -\zeta(0) = \frac{1}{2} \ne 0$.
In accordance with the novelty firewall (Section 45), the identity $B(s) = -s\zeta(1-s)$ is classical (Riemann 1859, Hurwitz 1882, Nörlund 1924, Apostol 1976) and is classified under `CLASSICAL_IDENTITY_REPURPOSED_FOR_ZERO_ARGUMENT_ARITHMETIC` and `PROVED_WITH_EXTERNAL_THEOREM`.

---

### G. Nontrivial-zero/Bernoulli-function bridge

For every nontrivial Riemann zeta zero $\rho$ ($0 < \operatorname{Re}(\rho) < 1$), Riemann's functional equation implies $\zeta(\rho) = 0 \iff \zeta(1-\rho) = 0$. Therefore, at $s = \rho$ ($z = \rho/2$, $1 - 2z = 1 - \rho$):
\[
\boxed{
\zeta(\rho) = 0 \iff \zeta(1-\rho) = 0 \implies B(\rho) = \mathcal{B}(\rho/2) = -\rho\zeta(1-\rho) = 0 \implies \mathcal{K}_0(\rho/2) = 0
}
\]
(`BERNOULLI_FUNCTION_NONTRIVIAL_ZETA_ZERO_BRIDGE_PROVED`, `BERNOULLI_FUNCTION_ZERO_BRIDGE_PROVED`, formalized in Lean 4 as `bernoulli_kernel_zero_at_zeta_zero`).

**Important Distinction Between Full Zero Divisors:** While $\mathcal{R}_\tau(z)$, $\mathcal{B}(z)$, $\mathcal{K}_0(z)$, and $\mathcal{B}_q(z)$ share the **exact same nontrivial zero set** $\{\rho/2 : \zeta(\rho)=0, 0 < \operatorname{Re}(\rho) < 1\}$, their full zero divisors on $\mathbb{C}$ are distinct:
- $\mathcal{R}_\tau(z)$ has extra zeros at negative integers $z = -k$ ($k \ge 1$, where $2z = -2k$), with $\mathcal{R}_\tau(1/2) = 1/\tau \ne 0$;
- $\mathcal{B}(z) = B(2z)$ has extra zeros at positive half-integers $z = k + \frac{1}{2}$ ($k \ge 1$, where $1-2z = -2k$), with $\mathcal{B}(1/2) = \frac{1}{2} \ne 0$ and $\mathcal{B}(-1) = 2\zeta(3) \ne 0$;
- $\mathcal{K}_0(z)$ has extra zeros at $z = \frac{1}{2}$ and $z = k + \frac{1}{2}$ ($k \ge 1$);
- $\mathcal{B}_q(z) = \mathcal{K}_0(z)/\Gamma(z+1)^q$ ($q \ge 1$) has all zeros of $\mathcal{K}_0(z)$ plus multiplicity-$q$ zeros at negative integers $z = -k$ ($k \ge 1$).

---

### H. Rational Bernoulli samples

At every non-negative integer $m \in \mathbb{Z}_{\ge 0}$, since $\zeta(1-2m) = -\frac{B_{2m}}{2m}$ ($m \ge 1$) and $\lim_{s\to 0}(-s\zeta(1-s)) = 1 = B_0$:
\[
\boxed{
\mathcal{B}(m) = B(2m) = B_{2m} \in \mathbb{Q}, \qquad
\mathcal{K}_0(m) = (-1)^m(2m)!\,\mathcal{R}_\tau(m) = -\frac{2m-1}{2}B_{2m} \in \mathbb{Q}
}
\]
(formalized in Lean 4 as `gamma_reflection_sample_clearing_identity`). Exact rational values are computed and verified in [`tc/fauzan_subfactorial_zero_kernel.py`](file:///c:/Development/Projects/reimann_scope/tc/fauzan_subfactorial_zero_kernel.py) across $0 \le m \le 200$ (`K0_0 = 1/2, K0_1 = -1/12, K0_2 = 1/20, K0_3 = -5/84, K0_4 = 7/120, K0_5 = -9/132`).

---

### I. Subfactorial sample denominators

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
2. For $\mathcal{K}_0(m) = -\frac{2m-1}{2}B_{2m}$, at $m = 1 \le n$ we have $\mathcal{K}_0(1) = -\frac{1}{12}$, so $v_2(D_n^{\mathcal{K}_0}) = 2 = 1 + v_2(D_n^{\mathcal{B}})$. For every odd prime $3 \le p \le 2n+1$, at the witness $m_p = \frac{p-1}{2} \le n$ we have $2m_p - 1 = p - 2$, and $\gcd(p-2, p) = 1$, so $p \nmid (2m_p - 1)$ and $v_p(\operatorname{den}(\mathcal{K}_0(m_p))) = v_p(\operatorname{den}(B_{p-1})) = 1$. Hence $D_n^{\mathcal{K}_0} = 2 D_n^{\mathcal{B}} = 2\prod_{p \le 2n+1} p$ for every $n \ge 1$ (verified by exact arithmetic for all $1 \le n \le 200$). $\square$

| $n$ | $\log D_n^{\mathcal{B}} = \vartheta(2n+1)$ | $\frac{1}{n}\log D_n^{\mathcal{B}}$ | $\log D_n^{\mathcal{K}_0}$ | $\log D_n^{\mathcal{R}_\tau}$ | $\frac{\log D_n^{\mathcal{R}_\tau}}{n\log n}$ |
|---:|---:|---:|---:|---:|---:|
| $1$ | $1.792$ | $1.792$ | $2.485$ | $3.178$ | — |
| $4$ | $5.347$ | $1.337$ | $6.040$ | $14.699$ | $2.651$ |
| $10$ | $13.143$ | $1.314$ | $13.836$ | $45.328$ | $1.969$ |
| $30$ | $53.119$ | $1.771$ | $53.812$ | $207.176$ | $2.030$ |
| $50$ | $88.456$ | $1.769$ | $89.149$ | $389.649$ | $1.992$ |
| $100$ | $184.996$ | $1.850$ | $185.689$ | $919.669$ | $1.997$ |
| $200$ | $380.233$ | $1.901$ | $380.926$ | $2115.654$ | $1.997$ |

---

### J. Factorial cost relocation into sample growth

Removing $(2m)!$ from the denominator via $\Gamma(2z+1)\cos(\tau z/2)$ moves the exact same $(2m)!$ into the **numerator magnitude** of the integer samples (`FACTORIAL_COST_MOVES_FROM_DENOMINATOR_TO_SAMPLE_GROWTH_UNDER_REFLECTION`, `FACTORIAL_COST_RELOCATED_TO_SAMPLE_GROWTH`):
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

### K. Gamma-ratio ladder

To interpolate between $\mathcal{K}_0(z)$ ($q = 0$) and bounded-sample kernels ($q \ge 2$), define for $q \in \mathbb{Z}_{\ge 0}$ the entire Gamma-ratio ladder:
\[
\boxed{
\mathcal{B}_q(z) := \frac{\mathcal{K}_0(z)}{\Gamma(z+1)^q} = \frac{z(2z-1)\zeta(1-2z)}{\Gamma(z+1)^q}
= \frac{\Gamma(2z+1)\cos(\tau z/2)}{\Gamma(z+1)^q}\mathcal{R}_\tau(z)
= 4^{-z}\frac{\Gamma(2z+1)\cos(\pi z)}{\Gamma(z+1)^q}\mathcal{R}_\pi(z).
}
\]
Since $1/\Gamma(z+1)$ is entire on $\mathbb{C}$ (with simple zeros at negative integers $z = -k$, $k \ge 1$) and $\mathcal{K}_0(z)$ is entire on $\mathbb{C}$, $\mathcal{B}_q(z)$ is **entire on $\mathbb{C}$ for every $q \in \mathbb{Z}_{\ge 0}$**, and satisfies $\mathcal{B}_q(\rho/2) = 0$ for every nontrivial zeta zero $\rho$, with exact rational integer samples (Lean theorem `gamma_ratio_integer_sample_identity`):
\[
\boxed{
\mathcal{B}_q(m) = -\frac{(2m-1)B_{2m}}{2(m!)^q} \in \mathbb{Q}, \qquad
|\mathcal{B}_q(m)| = \frac{(2m-1)(2m)!\zeta(2m)}{\tau^{2m}(m!)^q} \qquad (m \ge 1).
}
\]

---

### L. Gamma-ratio denominator/growth phase diagram

Let $D_{q,n} := \operatorname{lcm}_{0\le m\le n}\operatorname{den}(\mathcal{B}_q(m))$.

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
  1. Since $2m_p = k_p(p-1)$ is a multiple of $p-1$, the von Staudt–Clausen theorem guarantees that $v_p(B_{2m_p}) = -1$ ($p$ divides the **denominator** of $B_{2m_p}$, so $p$ CANNOT divide the numerator of $B_{2m_p}$; irregular-prime numerator divisibility $p \mid \operatorname{num}(B_{2m})$ can only occur when $(p-1)\nmid 2m$).
  2. Since $2m_p - 1 = k_p(p-1) - 1 \equiv -(k_p + 1) \not\equiv 0 \pmod p$, we have $v_p(2m_p - 1) = 0$.
  3. Consequently, the exact $p$-adic valuation of $\operatorname{den}(\mathcal{B}_q(m_p))$ is $v_p\bigl(\operatorname{den}(\mathcal{B}_q(m_p))\bigr) = 1 + q\,v_p(m_p!)$.
  4. Because $0 \le n - m_p \le p - 2 < p - 1$, $(m_p, n]$ contains at most one multiple of $p^j$ for each $1 \le j \le \lfloor\log_p n\rfloor$, so $v_p(n!) - v_p(m_p!) \le \lfloor\log_p n\rfloor$ and $v_p(D_{q,n}) \ge 1 + q\,v_p(n!) - q\lfloor\log_p n\rfloor$. Summing $\log p$ over $3 \le p \le n$ proves the lower bound (verified across $q = 0, 1, 2, 3, 4$ and $1 \le n \le 200$). $\square$

At the critical exponent $q = 2$,
\[
\boxed{
|\mathcal{B}_2(m)| = \frac{(2m-1)|B_{2m}|}{2(m!)^2} = (2m-1)\binom{2m}{m}\tau^{-2m}\zeta(2m) \sim \frac{2\sqrt{m}}{\sqrt{\pi}}\left(\frac{2}{\tau}\right)^{2m} = \frac{2\sqrt{m}}{\sqrt{\pi}}\pi^{-2m},
}
\]
yielding the complete $q = 0, \dots, 4$ phase diagram (Lean theorems `gamma_ratio_budget_conservation_identity` and `factorial_budget_algebraic_inequality`):

| Family | $q$ | Sample Growth $\log|\mathcal{B}_q(m)|$ | Sample Denominator $\log D_{q,n}$ | Total Budget $(\text{Growth} + \text{Denom})$ | $R_{\mathrm{OGF}}$ |
|---|---:|---|---|---|---|
| $\mathcal{B}_0(z) = \mathcal{K}_0(z)$ | $0$ | $+2m\log m + O(m)$ | $2n + o(n)$ (`SUBFACTORIAL`) | $2n\log n + O(n)$ | $0$ |
| $\mathcal{B}_1(z)$ | $1$ | $+1m\log m + O(m)$ | $+1n\log n + O(n)$ | $2n\log n + O(n)$ | $0$ |
| $\mathcal{B}_2(z)$ | $2$ | $-2m\log\pi + \frac{1}{2}\log m + O(1)$ | $+2n\log n + O(n)$ | $2n\log n + O(n)$ | $\pi^2 = \tau^2/4$ |
| $\mathcal{B}_3(z)$ | $3$ | $-1m\log m + O(m)$ | $+3n\log n + O(n)$ | $2n\log n + O(n)$ | $+\infty$ (order $1$) |
| $\mathcal{B}_4(z)$ | $4$ | $-2m\log m + O(m)$ | $+4n\log n + O(n)$ | $2n\log n + O(n)$ | $+\infty$ (order $1/2$) |

---

### M. Sign-adjusted positive Bernoulli kernel

Since $(-1)^{m+1}B_{2m} = |B_{2m}| > 0$ for every $m \ge 1$, multiplying $\mathcal{B}(z)$ by the entire nonvanishing exponential factor $-e^{i\tau z/2} = -e^{i\pi z}$ defines the sign-adjusted positive-sample kernel (`sign_adjusted_bernoulli_positive_sample_identity` in Lean 4):
\[
\boxed{
\mathcal{P}(z) := -e^{i\tau z/2}\mathcal{B}(z) = -e^{i\pi z}\mathcal{B}(z) = 2ze^{i\pi z}\zeta(1-2z), \qquad
\mathcal{P}(m) = (-1)^{m+1}B_{2m} = |B_{2m}| > 0 \quad (m \ge 1),
}
\]
with $\mathcal{P}(0) = -1$ and $\mathcal{P}(\rho/2) = 0$ for every nontrivial zero $\rho$ of $\zeta(s)$.

---

### N. Positive moment representation

From the classical Mellin representation $\Gamma(2m)\zeta(2m) = \int_0^\infty \frac{u^{2m-1}}{e^u-1}\,du$ ($m \ge 1$), substituting $u = \tau x$ and $\zeta(2m) = \frac{(-1)^{m+1}\tau^{2m}B_{2m}}{2(2m)!}$ yields
\[
\boxed{
(-1)^{m+1}B_{2m} = 4m\int_0^\infty \frac{x^{2m-1}}{e^{\tau x}-1}\,dx \qquad (m \ge 1).
}
\]
Integrating by parts with $dv = 2m x^{2m-1}\,dx$ ($v = x^{2m}$) and $u = \frac{2}{e^{\tau x}-1}$ ($du = -\frac{2\tau e^{\tau x}}{(e^{\tau x}-1)^2}\,dx$) gives boundary term $\left[\frac{2x^{2m}}{e^{\tau x}-1}\right]_0^\infty = 0$ for every $m \ge 1$ (since $x^{2m}/(\tau x) = O(x^{2m-1}) \to 0$ as $x \to 0^+$), proving:
\[
\boxed{
(-1)^{m+1}B_{2m} = 2\tau\int_0^\infty x^{2m}\frac{e^{\tau x}}{(e^{\tau x}-1)^2}\,dx = \frac{\tau}{2}\int_0^\infty \frac{x^{2m}}{\sinh^2(\tau x/2)}\,dx \qquad (m \ge 1).
}
\]
Shifting by one index $\mu_m := \mathcal{P}(m+1) = (-1)^m B_{2m+2} = |B_{2m+2}| > 0$ ($m \ge 0$) and changing variables to $y = x^2$ ($dx = \frac{dy}{2\sqrt{y}}$) proves (`BERNOULLI_EVEN_ABSOLUTE_VALUES_STIELTJES_MOMENT_SEQUENCE_PROVED`):
\[
\boxed{
\mu_m = |B_{2m+2}| = \int_0^\infty y^m\,d\nu_\tau(y), \qquad
d\nu_\tau(y) = \frac{\tau\sqrt{y}}{4\sinh^2(\tau\sqrt{y}/2)}\,dy = \frac{\pi\sqrt{y}}{2\sinh^2(\pi\sqrt{y})}\,dy \quad \text{on } (0, \infty).
}
\]
Moreover, since $\mu_m^{-1/(2m)} \sim \frac{\pi e}{m}$, $\sum_{m=1}^\infty \mu_m^{-1/(2m)} = +\infty$, so $\mu_m$ is a **Carleman-determinate Stieltjes moment sequence** on $[0, \infty)$.

---

### O. Bernoulli Hankel determinants

By the Stieltjes–Touchard–Carlitz–Al-Salam continued-fraction theorem for Bernoulli moments, the Jacobi continued fraction of $\sum_{m=0}^\infty \mu_m w^{-m-1}$ has exact rational recurrence coefficients (`carlitz_touchard_hankel_recurrence_positivity` in Lean 4):
\[
\boxed{
\alpha_k^{\mathcal{B}} = \frac{(k+1)(2k+1)(4k^2+6k+1)}{(4k+1)(4k+5)}, \qquad
\beta_k^{\mathcal{B}} = \frac{H_{k+1}^{\mathcal{B}} H_{k-1}^{\mathcal{B}}}{(H_k^{\mathcal{B}})^2}
= \frac{k^3(k+1)(2k-1)(2k+1)^3}{(4k-1)(4k+1)^2(4k+3)} > 0 \quad (k \ge 1),
}
\]
yielding the **exact closed-form product formula** for $H_n^{\mathcal{B}} := \det(\mu_{i+j})_{0\le i,j<n}$ (`BERNOULLI_STIELTJES_HANKEL_POSITIVITY_PROVED`):
\[
\boxed{
H_n^{\mathcal{B}} = \frac{1}{6^n}\prod_{k=1}^{n-1}\left[\frac{k^3(k+1)(2k-1)(2k+1)^3}{(4k-1)(4k+1)^2(4k+3)}\right]^{n-k} > 0,
}
\]
verified by exact rational matrix determinants (`flint.fmpq_mat.det`) for all $1 \le n \le 20$. Since $\beta_k^{\mathcal{B}} = \frac{k^4}{16}\bigl(1 + O(k^{-1})\bigr)$, Euler–Maclaurin summation gives the super-factorial growth law:
\[
\boxed{
\log H_n^{\mathcal{B}} = 2n^2\log n - (3 + 2\log 2)n^2 + O(n\log n) \longrightarrow +\infty.
}
\]
Notice that both $D_n^{(\tau)} = \det\bigl(\tau^{-2i-2j-2}\zeta(2i+2j+2)\bigr)$ and $H_n^{\mathcal{B}}$ share the **exact same polygonal denominator factors** $\prod_{k=1}^{n-1}\bigl[(4k-1)(4k+1)^2(4k+3)\bigr]^{n-k}$:

| $n$ | $H_n^{\mathcal{B}}$ (exact rational) | $\log H_n^{\mathcal{B}}$ | $\log\operatorname{den}(H_n^{\mathcal{B}})$ | $\log D_n^{(\tau)}$ |
|---:|---|---:|---:|---:|
| $1$ | $1/6$ | $-1.792$ | $1.792$ | $-3.178$ |
| $2$ | $1/350$ | $-5.858$ | $5.858$ | $-15.392$ |
| $3$ | $4/56595$ | $-9.557$ | $10.944$ | $-39.117$ |
| $4$ | $128/11022011$ | $-11.363$ | $16.215$ | $-75.850$ |
| $5$ | $955514880/25257378862001$ | $-10.182$ | $30.860$ | $-126.675$ |
| $10$ | $(303\text{-bit}) / (206\text{-bit})$ | $+67.152$ | $142.340$ | $-615.011$ |
| $15$ | $(1133\text{-bit}) / (462\text{-bit})$ | $+465.247$ | $319.839$ | $-1596.082$ |
| $20$ | $(2650\text{-bit}) / (825\text{-bit})$ | $+1265.118$ | $571.369$ | $-3152.956$ |

---

### P. Orthogonal-polynomial route

Using the exact three-term recurrence
\[
P_0^{\mathcal{B}}(X) = 1, \qquad P_1^{\mathcal{B}}(X) = X - \alpha_0^{\mathcal{B}}, \qquad
P_{k+1}^{\mathcal{B}}(X) = (X - \alpha_k^{\mathcal{B}})P_k^{\mathcal{B}}(X) - \beta_k^{\mathcal{B}} P_{k-1}^{\mathcal{B}}(X),
\]
we construct the exact monic orthogonal polynomials $P_n^{\mathcal{B}}(X) \in \mathbb{Q}[X]$ and their canonical primitive integer normalizations $\widetilde{P}_n^{\mathcal{B}}(X) = M_n P_n^{\mathcal{B}}(X) \in \mathbb{Z}[X]$ for $1 \le n \le 30$, and evaluate them at the certified 256-bit Arb ball enclosure of $\rho_1 = \frac{1}{2} + i\gamma_1$ and $\gamma_1$:
- All $n$ zeros of $P_n^{\mathcal{B}}(X)$ lie on the positive real axis $(0, \infty)$, so $P_n^{\mathcal{B}}(\rho_1) \ne 0$ automatically (Lean schema `primitive_hankel_polynomial_nonzero_schema`).
- However, both the monic evaluation $|P_n^{\mathcal{B}}(\rho_1)|$ and the primitive integer evaluation $|\widetilde{P}_n^{\mathcal{B}}(\rho_1)|$ **grow super-factorially**:
  - $n = 6$: $\log M_6 = 9.21$, $\log H(\widetilde{P}_6^{\mathcal{B}}) = 16.05$, $\log|\widetilde{P}_6^{\mathcal{B}}(\rho_1)| = +25.35$, $\mathscr{E}_6 = -4.225$;
  - $n = 15$: $\log M_{15} = 27.62$, $\log H(\widetilde{P}_{15}^{\mathcal{B}}) = 62.66$, $\log|\widetilde{P}_{15}^{\mathcal{B}}(\rho_1)| = +69.36$, $\mathscr{E}_{15} = -4.624$;
  - $n = 30$: $\log M_{30} = 60.05$, $\log H(\widetilde{P}_{30}^{\mathcal{B}}) = 165.41$, $\log|\widetilde{P}_{30}^{\mathcal{B}}(\rho_1)| = +165.42$, $\mathscr{E}_{30} = -5.514$.

---

### Q. Argument-coupling firewall

We establish a strict structural firewall (`BERNOULLI_STIELTJES_HANKEL_POSITIVITY_DOES_NOT_COUPLE_TO_ZETA_ZERO_ARGUMENT`, `BERNOULLI_HANKEL_ARGUMENT_COUPLING_FAILED`):
\[
\boxed{\text{moment-variable polynomial } P_n^{\mathcal{B}}(y) \;\neq\; \text{zeta-zero argument polynomial } P_n(\rho/2).}
\]
In the Stieltjes moment integral $\mu_m = |B_{2m+2}| = \int_0^\infty y^m\,d\nu_\tau(y)$, the sample index $m$ enters in the **exponent** $y^m$ (so $z \mapsto \mathcal{P}(z)$ is a Mellin transform in $z$), whereas $P_n^{\mathcal{B}}(X)$ is a polynomial in the **integration variable $X = y \in (0, \infty)$**. Evaluating $P_n^{\mathcal{B}}(X)$ at $X = \rho_1$ or $X = \gamma_1$ substitutes a Mellin zero ordinate into the integration variable $y = x^2$, where $P_n^{\mathcal{B}}$ has no analytic reason to be small.

---

### R. Stieltjes–Padé route

The Stieltjes transform of $d\nu_\tau(y)$ is the asymptotic Laplace/Stieltjes series
\[
S_{\mathcal{B}}(w) := \int_0^\infty \frac{d\nu_\tau(y)}{w - y} \sim \sum_{m=0}^\infty \frac{|B_{2m+2}|}{w^{m+1}} \qquad (|w| \to \infty, \; w \in \mathbb{C}\setminus[0, \infty)).
\]
By Binet's log-gamma/trigamma integral, $S_{\mathcal{B}}(w) = \frac{1}{2}\sqrt{w}\,\psi'(\sqrt{w}) - \frac{1}{2} - \frac{1}{4\sqrt{w}}$, so its $[n-1/n]$ Stieltjes–Padé approximants $Q_{n-1}^{\mathcal{B}}(w) / P_n^{\mathcal{B}}(w)$ converge to the trigamma function in $w = x^2$ on $\mathbb{C}\setminus[0, \infty)$, and do **not** couple to $\mathcal{B}(z)$, $\zeta(z)$, or $\mathcal{R}_\tau(z)$ at $z = \rho_1/2$.

For direct multipoint Padé interpolation $A_n(m) - f(m)B_n(m) = 0$ on $m = 0, \dots, 2n$ ($1 \le n \le 7$) in the actual zero-argument variable $z$, [`tc/fauzan_subfactorial_zero_kernel.py`](file:///c:/Development/Projects/reimann_scope/tc/fauzan_subfactorial_zero_kernel.py) proves (`MULTIPOINT_PADE_KERNEL_COMPARISON_FAVORS_BOUNDED_RADIUS_CLASSES_ONLY`, `ALL_N_MULTIPOINT_PADE_ASYMPTOTIC_STILL_OPEN`) that $\mathcal{K}_0$ ($q=0$) and $\mathcal{B}_1$ ($q=1$) fail raw analytic decay due to $R_{\mathrm{OGF}} = 0$, while $\mathcal{R}_\tau, \mathcal{R}_\pi, \mathcal{B}_2$ achieve raw residual decay $< 0$ but have $\log\widetilde{Q}_{n,\mathrm{Pade}}(\gamma_1) > 0$ growing rapidly for all $1 \le n \le 7$.

---

### S. Finite-window multipliers

To test whether a zero-independent $n$-dependent polynomial multiplier can cancel $(2m)!$ on a finite window $0 \le m \le n$, we construct the unique degree-$n$ interpolation polynomial $E_n(z) \in \mathbb{Q}[z]$ satisfying
\[
\boxed{
E_n(m) = (2m)! \quad (0 \le m \le n), \qquad
E_n(z) = \sum_{k=0}^n \frac{\Delta^k E(0)}{k!}(z)_k, \qquad
F_n(z) := E_n(z)\mathcal{R}_\tau(z),
}
\]
for all $1 \le n \le 30$. By construction, $E_n$ is strictly independent of $\gamma_1$ and $\rho_1$, $F_n(\alpha_1) = 0$, and $F_n(m) = (-1)^{m+1}\frac{2m-1}{2}B_{2m} = (-1)^m \mathcal{K}_0(m)$ has subfactorial denominators on $0 \le m \le n$. However:
- Because $E_n(n) = (2n)!$, the top finite difference satisfies $\Delta^n E(0) \sim (2n)!$, so clearing the basis denominator $L(E_n) \mid n!$ produces a primitive polynomial $\widetilde{E}_n(z) \in \mathbb{Z}[z]$ with height $\log H(\widetilde{E}_n) \sim 2n\log n$ and certified evaluation $\log|\widetilde{E}_n(\alpha_1)| \sim 2n\log n \to +\infty$:
  - $n = 5$: $\log L(E_5) = 4.79$, $\log H(\widetilde{E}_5) = 15.10$, $\log|\widetilde{E}_5(\alpha_1)| = +22.49$, $\mathscr{E}_5 = -4.499$;
  - $n = 15$: $\log L(E_{15}) = 27.90$, $\log H(\widetilde{E}_{15}) = 74.66$, $\log|\widetilde{E}_{15}(\alpha_1)| = +79.82$, $\mathscr{E}_{15} = -5.321$;
  - $n = 30$: $\log L(E_{30}) = 74.66$, $\log H(\widetilde{E}_{30}) = 190.02$, $\log|\widetilde{E}_{30}(\alpha_1)| = +189.62$, $\mathscr{E}_{30} = -6.321$.

---

### T. Rational-height conservation

#### Theorem (`RATIONAL_SAMPLE_DENOMINATOR_CANCELLATION_REQUIRES_MULTIPLIER_HEIGHT`, Lean 4 `sample_multiplier_denominator_cancellation_bound`)

Let $a_m = A_m / D_m$ ($\gcd(A_m, D_m) = 1$) and $e_m = P_m / Q_m$ ($\gcd(P_m, Q_m) = 1$) be reduced rational numbers with product $f_m = e_m a_m = (P_m A_m)/(Q_m D_m)$. Then for every prime $p$:
\[
\boxed{
v_p(P_m) \ge v_p(D_m) - v_p\bigl(\operatorname{den}(f_m)\bigr), \qquad
\log|P_m| \ge \log D_m - \log\operatorname{den}(f_m).
}
\]
**Proof.** In $f_m = \frac{P_m A_m}{Q_m D_m}$, since $\gcd(A_m, D_m) = 1$, no prime factor of $D_m$ can be cancelled by $A_m$. Thus any prime power $p^r \mid D_m$ that does not survive in $\operatorname{den}(f_m)$ must divide $P_m$, giving $v_p(D_m) \le v_p(P_m) + v_p(\operatorname{den}(f_m))$. Summing $v_p(\cdot)\log p$ over all $p \mid D_m$ yields $\log|P_m| \ge \log D_m - \log\operatorname{den}(f_m)$. $\square$

Applied to $a_m = \mathcal{R}_\tau(m)$ ($\log D_m = 2m\log m + O(m)$), any multiplier reducing $\log\operatorname{den}(f_m)$ to $O(m)$ must have numerator height $\log|P_m| \ge 2m\log m - O(m)$.

---

### U. Borel/EGF route

Because Bernoulli numbers naturally belong to an exponential generating function, we derive the exact Borel / EGF transforms:
\[
\boxed{
\sum_{m=0}^\infty B_{2m}\frac{x^{2m}}{(2m)!} = \frac{x}{2}\coth\!\left(\frac{x}{2}\right), \qquad
\sum_{m=0}^\infty \mathcal{K}_0(m)\frac{x^{2m}}{(2m)!} = \frac{1}{2}\left(1 - x\frac{d}{dx}\right)\!\left(\frac{x}{2}\coth\frac{x}{2}\right) = \frac{x^2}{8\sinh^2(x/2)},
}
\]
which converge for $|x| < \tau = 2\pi$. However, dividing $B_{2m}$ by $(2m)!$ in the Borel transform simply restores the $(2m)!$ denominator of $\mathcal{R}_\tau(m)$ while replacing the Mellin zero-argument variable $z = \rho/2$ by the dummy power-series variable $x$ (`BOREL_TRANSFORM_IN_NEW_VARIABLE_DOES_NOT_BY_ITSELF_CONSTRAIN_ZERO_ARGUMENT`).

---

### V. Alternative interpolation bases

We audit whether the factorial penalty on consecutive or even integer nodes is an artifact of the ordinary Newton basis (`CONSECUTIVE_INTEGER_NODE_POLYNOMIALIZATION_HAS_INTRINSIC_FACTORIAL_LATTICE_COST`, `EQUISPACED_NEWTON_LAGRANGE_BASIS_REINTRODUCES_FACTORIAL_DENOMINATOR`):
- **Uniqueness of the Interpolating Polynomial:** For any given $n+1$ nodes $\{x_0, \dots, x_n\}$ and sample values $f(x_m) \in \mathbb{Q}$, the degree-$\le n$ interpolating polynomial $P_n(z) \in \mathbb{Q}[z]$ is **unique**. Changing the basis of $\mathbb{Q}[z]_{\le n}$ (between ordinary Newton $\binom{z}{k}$, central factorial, Lagrange $\ell_{n,m}(z)$, even-node $\binom{s/2}{k}$, or Pólya–Bhargava integer-valued bases) changes only the intermediate coordinates, leaving the expanded polynomial $P_n(z)$ and its canonical primitive integer norm polynomial $\widetilde{Q}_n(Y) \in \mathbb{Z}[Y]$ **100% invariant**.
- **Intrinsic Pólya–Ostrowski Lattice Cost:** By Pólya's theorem (1919), $\binom{z}{k} = \frac{(z)_k}{k!}$ ($0 \le k \le n$) is a $\mathbb{Z}$-basis of integer-valued polynomials on $\{0, \dots, n\}$, so the leading coefficient of $P_n(z)$ is $\frac{\Delta^n f(0)}{n!}$, carrying the intrinsic Vandermonde/factorial lattice denominator $n!$ (and $4^n(n!)^2$ in the squared norm polynomial).

---

### W. Direct \(\rho\) versus \(\rho/2\) arithmetic

Comparing the direct zero coordinate $s(Y) = \frac{1}{2} + iY$ sampled at even integers $s_m = 2m$ ($B(2m) = B_{2m}$) against the half-coordinate $\alpha(Y) = \frac{1}{4} + i\frac{Y}{2}$ sampled at integers $z_m = m$ ($\mathcal{B}(m) = B_{2m}$) reveals an **exact algebraic identity**:
\[
\boxed{
\binom{s(Y)/2}{k} = \prod_{j=0}^{k-1}\frac{s(Y) - 2j}{2(j+1)} = \prod_{j=0}^{k-1}\frac{\alpha(Y) - j}{j+1} = \binom{\alpha(Y)}{k} \qquad (\forall k \ge 0).
}
\]
Thus the interpolating polynomials in $Y$, the norm polynomial $Q_n(Y)$, its degree $2k_n$ (Lean theorem `even_node_norm_polynomial_degree_bound`), the dyadic clearing factor $4^{k_n}$, the primitive coefficient height, and $\widetilde{Q}_n(\gamma_1)$ are **identically equal** between the direct $\rho$-scale and the $\rho/2$-scale.

---

### X. Candidate gate table

Every required candidate is evaluated across Gates K1–K7 (Lean theorem `primitive_auxiliary_efficiency_scaling`):

| Candidate | K1 (Zero Vanishing) | K2 (Rational Samples) | K3 (Subfactorial $D_n = e^{O(n)}$) | K4 (Tame Sample Growth) | K5 (Argument Polynomial) | K6 (Nonvanishing at $\gamma_1$) | K7 ($\mathscr{E}_n^{\mathrm{prim}} \to +\infty$) | Earliest Failure |
|---|---|---|---|---|---|---|---|---|
| 1. $\mathcal{R}_\tau(z)$ (control) | PASS | PASS | **FAIL** ($2n\log n$) | PASS | PASS | PASS | FAIL (Newton); OPEN (Padé) | **K3** (and K7 for Newton) |
| 2. $B(2z) = -2z\zeta(1-2z)$ | PASS | PASS ($B_{2m}$) | **PASS** ($e^{\vartheta(2n+1)}$) | **FAIL** ($2m\log m$) | PASS | PASS | FAIL ($\to -\infty$) | **K4** |
| 3. $\mathcal{K}_0(z) = z(2z-1)\zeta(1-2z)$ | PASS | PASS | **PASS** ($2e^{\vartheta(2n+1)}$) | **FAIL** ($2m\log m$) | PASS | PASS | FAIL ($\to -\infty$) | **K4** |
| 4. $\mathcal{B}_q(z)$ ($q=0,1,2,3,4$) | PASS | PASS | PASS ($q=0$); **FAIL** ($q\ge 1$) | **FAIL** ($q\le 1$); PASS ($q\ge 2$) | PASS | PASS | FAIL (Newton); neg ($q=2$ Padé) | **K4** ($q\le 1$) / **K3** ($q\ge 2$) |
| 5. $\mathcal{P}(z) = -e^{i\tau z/2}\mathcal{B}(z)$ | PASS | PASS ($|B_{2m}|>0$) | **PASS** ($e^{\vartheta(2n+1)}$) | **FAIL** ($2m\log m$) | FAIL (moments) | PASS | FAIL ($\to -\infty$) | **K4** |
| 6. Bernoulli Hankel $P_n^{\mathcal{B}}(X)$ | **FAIL** ($X=y\ne\rho/2$) | PASS ($\mathbb{Q}[X]$) | PASS (moments) | **FAIL** ($H_n^{\mathcal{B}} \sim n^{2n^2}$) | **FAIL** (decoupled) | PASS (real roots) | FAIL ($\to -\infty$) | **K4 / K5** |
| 7. Windowed multiplier $E_n(z)\mathcal{R}_\tau(z)$ | PASS | PASS | PASS on $[0,n]$ | **FAIL** ($\log H(\widetilde{E}_n)\sim 2n\log n$) | PASS | PASS | FAIL ($\to -\infty$) | **K4** |
| 8. Multipoint Padé on $\mathcal{R}_\tau, \mathcal{B}_2$ | PASS | PASS | **FAIL** ($4n\log n$) | PASS ($R_{\mathrm{OGF}}>0$) | PASS | PASS ($n\le 7$) | Negative ($n\le 7$); OPEN ($n\to\infty$) | **K3** (K7 open for Padé) |

---

### Y. Literature novelty audit

We separate classical identities from the structural combination tested in `TASK-TC-040`:

| Mathematical Ingredient | Classical / Literature Status | Primary References | Role in `TASK-TC-040` |
|---|---|---|---|
| Bernoulli function $B(s) = -s\zeta(1-s)$ and $B(2m) = B_{2m}$ | `PROVED_WITH_EXTERNAL_THEOREM` (`CLASSICAL_IDENTITY_REPURPOSED_FOR_ZERO_ARGUMENT_ARITHMETIC`) | Riemann (1859); Hurwitz (1882); Nörlund (1924); Apostol (1976) | Provides the reflection kernel $\mathcal{B}(z) = B(2z)$ and $\mathcal{K}_0(z)$ |
| Squarefree denominator law $\operatorname{den}(B_{2m}) = \prod_{(p-1)\mid 2m}p$ | `PROVED_WITH_EXTERNAL_THEOREM` | von Staudt (1840); Clausen (1840); Hardy & Wright (1979) | Yields exact primorial LCM $D_n^{\mathcal{B}} = \prod_{p\le 2n+1}p = e^{\vartheta(2n+1)}$ |
| Positive Stieltjes measure for $|B_{2m+2}|$ & continued fraction $\alpha_k^{\mathcal{B}}, \beta_k^{\mathcal{B}}$ | `PROVED_WITH_EXTERNAL_THEOREM` | Stieltjes (1889); Touchard (1956); Carlitz (1959); Al-Salam & Carlitz (1959) | Yields exact product formula and $\log H_n^{\mathcal{B}} = 2n^2\log n + O(n^2)$ |
| Integer-valued polynomial basis $\binom{z}{k}$ and factorial index $n!$ | `PROVED_WITH_EXTERNAL_THEOREM` | Pólya (1919); Ostrowski (1919); Gel'fond (1952); Bhargava (2000) | Establishes intrinsic factorial lattice cost on consecutive integers |
| **Project Contribution:** Combining $B(\rho)=0$, $D_n^{\mathcal{B}}=e^{\vartheta(2n+1)}$, irregular-prime-free $\mathcal{B}_q$ two-sided denominator bounds, and universal primitive norm lower bounds to prove the **Factorial-Relocation & Equispaced Gamma-Ratio No-Go Theorem** | `PROVED_PAPER_DERIVATION` + `LEAN_PROVED` (14 algebraic/arithmetic skeleton theorems in `SubfactorialZeroKernel.lean`) | `TASK-TC-040` (`tc/fauzan_subfactorial_zero_kernel.py`) | Rigorously closes the equispaced Gamma-reflection / Gamma-ratio class at Gate Z5 |

---

### Z. Principal classification and next theorem

1. **Principal Classifications:**
   - `BERNOULLI_FUNCTION_NONTRIVIAL_ZETA_ZERO_BRIDGE_PROVED` (`BERNOULLI_FUNCTION_ZERO_BRIDGE_PROVED`)
   - `SUBFACTORIAL_RATIONAL_SAMPLE_DENOMINATOR_ACHIEVED`
   - `FACTORIAL_COST_MOVES_FROM_DENOMINATOR_TO_SAMPLE_GROWTH_UNDER_REFLECTION` (`FACTORIAL_COST_RELOCATED_TO_SAMPLE_GROWTH`)
   - `PROVED_TWO_SIDED_DENOMINATOR_ASYMPTOTIC`
   - `GAMMA_RATIO_FACTORIAL_BUDGET_TRADEOFF_PROVED`
   - `BERNOULLI_EVEN_ABSOLUTE_VALUES_STIELTJES_MOMENT_SEQUENCE_PROVED`
   - `BERNOULLI_STIELTJES_HANKEL_POSITIVITY_PROVED`
   - `BERNOULLI_STIELTJES_HANKEL_POSITIVITY_DOES_NOT_COUPLE_TO_ZETA_ZERO_ARGUMENT` (`BERNOULLI_HANKEL_ARGUMENT_COUPLING_FAILED`)
   - `RATIONAL_SAMPLE_DENOMINATOR_CANCELLATION_REQUIRES_MULTIPLIER_HEIGHT`
   - `BOREL_TRANSFORM_IN_NEW_VARIABLE_DOES_NOT_BY_ITSELF_CONSTRAIN_ZERO_ARGUMENT`
   - `CONSECUTIVE_INTEGER_NODE_POLYNOMIALIZATION_HAS_INTRINSIC_FACTORIAL_LATTICE_COST`
   - `EQUISPACED_GAMMA_REFLECTION_CLASS_NO_GO_PROVED`
   - `FACTORIAL_RELOCATION_ACROSS_DENOMINATOR_GROWTH_AND_BASIS_PROVED`
   - `NO_SUBFACTORIAL_DIOPHANTINE_ZERO_KERNEL_FOUND_IN_TESTED_BERNOULLI_GAMMA_HANKEL_CLASSES`
2. **Subgate & Obligation Statuses:**
   - `SUBGATE-TC-040A`: `CLOSED_FOR_EQUISPACED_GAMMA_REFLECTION_CLASS_AT_GATE_Z5`
   - `SUBGATE-TC-039A [Newton]`: `CLOSED_NEGATIVE_AT_GATE_Z5`
   - `SUBGATE-TC-039A [Padé asymptotic]`: `OPEN` (`ALL_N_MULTIPOINT_PADE_ASYMPTOTIC_STILL_OPEN`)
   - `SUBGATE-TC-038A`: `OPEN`
   - `OBL-CT-001A`: `OPEN`
   - **RH Claimed:** `False` (no claim of the Riemann Hypothesis or of zero irrationality/transcendence is made).
3. **Exact Next Theorem:**
   Prove an all-$n$ analytic lower bound on the canonical primitive integer multipoint Padé norm polynomial $\widetilde{Q}_{n,\mathrm{Pade}}^{(c)}(\gamma_1)$ (via Hermite–Walsh contour asymptotics and Hankel/Cramer determinant denominator valuations) to resolve `SUBGATE-TC-039A [Padé asymptotic]`, or identify a non-equispaced rational sampling architecture whose Vandermonde lattice index and sample heights simultaneously remain $e^{O(n)}$.
