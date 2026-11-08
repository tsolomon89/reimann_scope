# Mathematical Review & Proof Attempt Report: Simultaneous $\tau$-Compatibility, Finite-Prime Exclusion, Integrated Energy Kernel, and Multiplicative Parity Controls (`TASK-TC-055`)

- **Task ID**: `TASK-TC-055` (`task/tc-055-simultaneous-tau-compatibility-and-signed-energy-cancellation`)
- **Parent Epic**: `EPIC-TC-042` (Canonical $\tau$-Adelic Theta-Correlation Bound and Hilbert-Schmidt Orbit Control)
- **Merged `main` Baseline (`TC-054R2` merge)**: `8a898c60b7c4cb56543a3d1e7960c39e00027c22`
- **Prior `TC-054R2` Implementation / Reviewed HEAD**: `a4b30737013aa2e16d095b897fa6b97b08f451dc` / `e178497d7637b799ce6eda5ed0cb2486c841c577`
- **Initial Focused Closeout Commit (Section 2)**: `80d1c86408d39562b06b2c69d4b4f655a1677f82`
- **Primary Implementation Module**: [`tc/liouville_square_dilation.py`](../../tc/liouville_square_dilation.py)
- **Serialized 256-Bit Arb Certificate**: [`data/tc_liouville_square_dilation.json`](../../data/tc_liouville_square_dilation.json)
- **Formal Lean 4 Module**: [`formal/RiemannScope/LiouvilleSquareDilation.lean`](../../formal/RiemannScope/LiouvilleSquareDilation.lean) (`20` definitions, `11` public theorems, `16` private helper theorems, `0` `sorry`, `0` custom `axiom`)
- **Regression Suite**: [`tests/test_tc_liouville_square_dilation.py`](../../tests/test_tc_liouville_square_dilation.py)
- **Subgate Status**: `SUBGATE-TC-043A: OPEN` (`rh_proved: false`)

---

## 1. Mathematical Framework, Notation, and Dependency Chain to `SUBGATE-TC-043A`

Throughout this report:
- $\tau = 2\pi$ is the sole circle constant;
- Complex Mellin variables are written $z = a + i b$ with $a, b \in \mathbb{R}$, and Riemann zeta zeros are written $\rho = x + i y$ with $x, y \in \mathbb{R}$ and critical coordinate $x = 1/2$;
- Admissible TC grades are real algebraic numbers $K \in \mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}$ (including negative grades $K < 0$), with scale factor $a_K = \tau^K > 0$;
- Auxiliary multiplicative dilations $S_p F(X) := F(X/p)$ by primes $p$ and $S_{d^2} F(X) := F(X/d^2)$ by squares $d^2$ act on the continuum scale variable $X \in (0, \infty)$. A dilation by $p$ does **not** make $\log_\tau p$ an admissible TC grade, and we do **not** claim that $\log_\tau 2$ is transcendental: by Lindemann's theorem ($e^\alpha$ is transcendental for every nonzero algebraic $\alpha$, so $\tau = 2\pi$ is transcendental), $\log_\tau m$ is irrational for every integer $m \ge 2$ (since $\log_\tau m = p/q \implies \tau^p = m^q \in \mathbb{Q}$, impossible for $p \ne 0$).
- Discrete integer grade blocks $[\tau^k, \tau^{k+1}]$ ($k \in \mathbb{Z} \subset \mathbb{A}_{\mathbb{R}}$) cover every continuum window $[Y, \tau Y]$ ($Y \ge 1$) by at most two adjacent integer grade blocks $[\tau^k, \tau^{k+1}] \cup [\tau^{k+1}, \tau^{k+2}]$ with $k = \lfloor \log_\tau Y \rfloor$, incurring the exact two-block covering factor $1 + \tau^\varepsilon$.

### 1.1 Exact Dependency Chain to `SUBGATE-TC-043A`

1. **Stage 1 — Canonical Hilbert–Schmidt Orbit & Resonant-Band Isolation (`EPIC-TC-042` / `TC-043` / `TC-050R`)**:
   Across all real algebraic grades $K \in \mathbb{A}_{\mathbb{R}}$, the canonical Hilbert–Schmidt correlation splits as
   $$C_\tau(K) = P_\tau(K) + \mathcal{E}_{\tau,\mathrm{controlled}}(K) - \mathcal{R}_{\mu,\mathrm{band}}\bigl(\tau^{|K|}\bigr),$$
   where $|P_\tau(K)| \le P_\tau(0) < 2.55826$ and $|\mathcal{E}_{\tau,\mathrm{controlled}}(K)| < 17.987140$ are proved unconditionally, reducing uniform boundedness $\sup_{K \in \mathbb{A}_{\mathbb{R}}}|C_\tau(K)| < \infty$ to `SUBGATE-TC-043A` (bounding $\mathcal{R}_{\mu,\mathrm{band}}(\tau^{|K|})$).
2. **Stage 2 — Trivial-Zero Slope Recovery & Baez-Duarte / Riesz Gaussian Proxy $Q_\mu(X)$ (`TC-051` to `TC-053R2`)**:
   For $Z_{a_K}(s) := \zeta(s/a_K)$, differentiating at the transported trivial zeros $s_{m,K} = -2m a_K$ ($m \ge 1$) gives
   $$\frac{2(-1)^m \tau^{2m}}{(2m)!}\,a_K Z_{a_K}'(-2m a_K) = \zeta(2m + 1),$$
   recovering the odd-zeta reciprocal coefficients $c_j = \frac{(-1)^j}{j!\,\zeta(2j+3)}$ of the Gaussian proxy
   $$Q_\mu(X) := X^{5/2}\sum_{n\ge 1}\frac{\mu(n)}{n^3}e^{-X^2/n^2}, \qquad \mathcal{M}[Q_\mu](z) = \frac{\Gamma(5/4 - z/2)}{2\,\zeta(1/2 + z)} \quad \left(\frac{1}{2} < \operatorname{Re} z < \frac{5}{2}\right).$$
3. **Stage 3 — Reversible Square-Dilation Transfer & Weighted Norm Equivalence (`TC-054` / `TC-054R` / `TC-054R2`)**:
   The exact integer convolutions $\lambda(n) = \sum_{d^2 \mid n}\mu(n/d^2)$ and $\mu(n) = \sum_{d^2 \mid n}\mu(d)\lambda(n/d^2)$ (proved unconditionally on actual positive integers in Lean 4 theorem `actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat`) induce the reversible square-dilation transfers
   $$Q_\lambda(X) = \sum_{d\ge 1}\frac{1}{d}\,Q_\mu(X/d^2), \qquad Q_\mu(X) = \sum_{d\ge 1}\frac{\mu(d)}{d}\,Q_\lambda(X/d^2)$$
   and the two-sided weighted norm equivalence on $\mathcal{H}_\eta = L^2((0,\infty), X^{-2\eta}\,dX/X)$ for all $\eta > 0$:
   $$\|Q_\lambda\|_\eta \le \zeta(1 + 2\eta)\,\|Q_\mu\|_\eta, \qquad \|Q_\mu\|_\eta \le \frac{\zeta(1 + 2\eta)}{\zeta(2 + 4\eta)}\,\|Q_\lambda\|_\eta.$$
4. **Stage 4 — Simultaneous Joint System & Target Closure Estimate (`TASK-TC-055`)**:
   By Proposition 3.1 of [`TC_LIOUVILLE_SQUARE_DILATION.md`](./TC_LIOUVILLE_SQUARE_DILATION.md), closing `SUBGATE-TC-043A` through the Liouville/Mellin route is equivalent to proving the subpower grade-interval energy bound:
   $$\boxed{\forall \varepsilon > 0\;\exists C_\varepsilon < \infty\;\forall Y \ge 1, \qquad E_\lambda(Y) := \int_Y^{\tau Y}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} \le C_\varepsilon Y^\varepsilon.}$$

---

## 2. Initial Focused Closeout of Remaining `TC-054R2` Items (`80d1c86408d39562b06b2c69d4b4f655a1677f82`)

Before beginning the `TASK-TC-055` derivations, commit `80d1c86408d39562b06b2c69d4b4f655a1677f82` closed six narrow exposition and report items from `TC-054R2`:
1. **Vertical-contour Stirling exponent**: Recorded the exact polynomial exponent $|b|^{3a/2 + 3/2}e^{-\tau|b|/8}$ (since $|\Gamma(a + ib)| \asymp_a |b|^{a - 1/2}e^{-\tau|b|/4}$ and $|\Gamma(\frac{-3-a}{2} - i\frac{b}{2})| \asymp_a |b|^{-(a+4)/2}e^{-\tau|b|/8}$, whose quotient has polynomial exponent $(a - 1/2) - (-(a+4)/2) = \frac{3a}{2} + \frac{3}{2}$).
2. **Horizontal-contour DLMF 5.8.3 shift across the entire strip $a \in [a_M, c]$**: Since $c \in (0, 1)$, $\operatorname{Re}(1 - z) = 1 - a \in [1 - c, 2M + 5/2]$ drops below $1/2$ when $a \in (1/2, c]$. Applying the one-step shift $\Gamma(1 - z) = \frac{\Gamma(2 - z)}{1 - z}$ ($\operatorname{Re}(2 - z) = 2 - a > 1 \ge 1/2$) and the three-step shift $\Gamma(\frac{-3-z}{2}) = \frac{\Gamma((3-z)/2)}{((-3-z)/2)((-1-z)/2)((1-z)/2)}$ ($\operatorname{Re}(\frac{3-z}{2}) = \frac{3-a}{2} > 1 \ge 1/2$) places both Gamma arguments in $\operatorname{Re} w \ge 1/2$ across the entire strip $a \in [a_M, c]$ while retaining the polynomial factor $|1 - z|\,|(-3-z)(-1-z)(1-z)|/8 = O(B^4)$, giving $|\mathcal{M}[H](a \pm iB)| \le C_{M,c}\,B^4 e^{-\tau B/8} \to 0$.
3. **Residue sign attribution at $z = -2m$**: Stated explicitly that $\operatorname*{Res}_{z = -2m}\Gamma(z) = \frac{(-1)^{2m}}{(2m)!} = \frac{1}{(2m)!} > 0$, while the alternating sign $(-1)^m$ comes from $\cos(\frac{\tau(-2m)}{4}) = \cos(-m\frac{\tau}{2}) = (-1)^m$.
4. **Gamma recurrence for $m \ge 2$**: Replaced the ambiguous rising-product notation with the explicit product $\Gamma(5/2 - m) = \frac{(-1)^{m-2}\Gamma(1/2)}{\prod_{j=1}^{m-2}(j - 1/2)}$ for $m \ge 2$ (evaluating to $\Gamma(1/2)$ at $m = 2$ via the empty product and $-\Gamma(1/2)/(1/2) = -2\Gamma(1/2)$ at $m = 3$).
5. **Unweighted $L^2((0,\infty), dX/X)$ square-transfer qualification**: Qualified the $\eta = 0$ identity $\|S_{d^2}f\|_0 = \|f\|_0$ as holding on functions $f \in L^2((0,\infty), dX/X)$, where the triangle-inequality majorants $\sum_{d\ge 1}d^{-1}$ and $\sum_{d\ge 1}|\mu(d)|d^{-1}$ diverge, whereas $Q_\mu, Q_\lambda$ are analyzed on $\mathcal{H}_\eta = L^2((0,\infty), X^{-2\eta}\,dX/X)$ for $\eta \in (0, 5/2)$.
6. **Separated series vs. quadrature radius reporting**: Distinguished `series_truncation_radius`, `series_total_radius` (correcting $\xi = 2$ from `8.59e-162` to `1.65e-162`), and `quadrature_total_radius`.

---

## 3. Single Observable and Exact Joint Identities Across $\tau$-Grades, Square Dilations, and Prime-Parity Filters

### 3.1 Single Observable and Where Actual Prime Arithmetic Enters vs. Generic Commutation

Fix the single observable family for $X > 0$ and $a \in \{\mu, \lambda\}$:
$$Q_a(X) = X^{5/2}\sum_{n\ge 1}\frac{a(n)}{n^3}e^{-X^2/n^2}, \qquad \bigl|Q_a(X)\bigr| \le \zeta(3)X^{5/2}, \qquad \bigl|R_{a, >T}(X)\bigr| \le \frac{X^{5/2}}{2T^2}.$$
On functions $F : (0, \infty) \to \mathbb{R}$, define:
- **Admissible $\tau$-grade transport** ($K \in \mathbb{A}_{\mathbb{R}}$): $(U_K F)(X) := F(\tau^{-K}X)$;
- **Auxiliary prime/integer multiplicative shift** ($m \in \mathbb{N}_{\ge 1}$): $(S_m F)(X) := F(X/m)$;
- **Square-dilation transfer**: $(\mathcal{T}_{\mathrm{sq}}F)(X) := \sum_{d\ge 1}\frac{1}{d}F(X/d^2)$, $(\mathcal{T}_{\mathrm{sq}}^{-1}F)(X) := \sum_{d\ge 1}\frac{\mu(d)}{d}F(X/d^2)$;
- **Finite-prime parity filter** ($P \subset \mathbb{P}$ finite, $N_P := \prod_{p\in P}p$):
  $$\mathcal{P}_P := \prod_{p\in P}\bigl(I + p^{-1/2}S_p\bigr) = \sum_{d \mid N_P}\frac{|\mu(d)|}{\sqrt{d}}\,S_d.$$

**Distinction between generic commutation and actual prime arithmetic**:
1. **Generic commutation on $(0, \infty)$**: Because the multiplicative group $(0, \infty)^\times$ is abelian, $U_K$, $S_m$, $\mathcal{T}_{\mathrm{sq}}$, and $\mathcal{P}_P$ commute on *every* function $F : (0, \infty) \to \mathbb{R}$ for which the sums converge. Commutation of these external dilation operators alone is a generic group property and supplies **zero** arithmetic cancellation.
2. **Where actual prime arithmetic enters**:
   - **Prime-parity flip $\lambda(p n) = -\lambda(n)$**: For the specific observable $Q_\lambda(X)$, applying $p^{-1/2}S_p$ shifts the external scale $X \mapsto X/p$:
     $$p^{-1/2}(S_p Q_\lambda)(X) = p^{-1/2}(X/p)^{5/2}\sum_{m\ge 1}\frac{\lambda(m)}{m^3}e^{-X^2/(p m)^2} = X^{5/2}\sum_{m\ge 1}\frac{\lambda(m)}{(p m)^3}e^{-X^2/(p m)^2} = -X^{5/2}\sum_{\substack{n\ge 1 \\ p \mid n}}\frac{\lambda(n)}{n^3}e^{-X^2/n^2},$$
     where the last equality uses the actual arithmetic identity $\lambda(p m) = -\lambda(m)$. Adding $Q_\lambda(X)$ annihilates every index $n$ divisible by $p$.
   - **Square-divisor Möbius convolution $\sum_{d^2 \mid n}\mu(n/d^2) = \lambda(n)$**: Identifies the Dirichlet series $D_\lambda(s) = \sum_{n\ge 1}\lambda(n)n^{-s} = \frac{\zeta(2s)}{\zeta(s)}$, so that the pole of $\zeta(2s)$ at $s = 1/2$ is modulated by $1/\zeta(s)$ and, crucially, $D_\lambda(s)$ is analytic at $s = 1$ because $\zeta(1) = \infty$ in the denominator kills the $s = 1$ pole (whereas finite-prime parity controls $a_S$ retain a pole at $s = 1$; see §7).

### 3.2 Trivial-Zero Slope Transport and Exact Removable Cancellation in $\mathcal{M}[Q_\lambda](z)$

1. **Transported trivial-zero slope invariance**:
   For $Z_{a_K}(s) = \zeta(s/a_K)$ ($a_K = \tau^K$), the trivial zeros of $Z_{a_K}$ lie at $s_{m,K} = -2m a_K$ ($m \ge 1$). By the chain rule,
   $$a_K Z_{a_K}'(-2m a_K) = a_K \cdot \frac{1}{a_K}\zeta'(-2m) = \zeta'(-2m) = \frac{(-1)^m (2m)!}{2\,\tau^{2m}}\,\zeta(2m + 1).$$
   Thus varying the TC grade $K \in \mathbb{A}_{\mathbb{R}}$ transports the trivial-zero location $s_{m,K} = -2m\tau^K$ by scale covariance without generating new independent Dirichlet moments beyond $\{\zeta(2m+1)\}_{m\ge 1}$.
2. **Exact removable trivial-zero cancellation in $\mathcal{M}[Q_\lambda](z)$ at $z_m = -(2m + 1/2)$**:
   For $\frac{1}{2} < \operatorname{Re} z < \frac{5}{2}$ (and by meromorphic continuation to $\mathbb{C}$),
   $$\mathcal{M}[Q_\mu](z) = \frac{\Gamma(5/4 - z/2)}{2\,\zeta(1/2 + z)}, \qquad \mathcal{M}[Q_\lambda](z) = \frac{\Gamma(5/4 - z/2)\,\zeta(1 + 2z)}{2\,\zeta(1/2 + z)}.$$
   - In $\mathcal{M}[Q_\mu](z)$, the trivial zeros $1/2 + z = -2m$ ($z_m = -(2m + 1/2)$, $m \ge 1$) are genuine simple poles in the left half-plane $\operatorname{Re} z \le -5/2$ (since $\Gamma(5/4 - z_m/2) = \Gamma(m + 3/2) \ne 0$).
   - In $\mathcal{M}[Q_\lambda](z)$, at $z_m = -(2m + 1/2)$ we have simultaneously
     $$\frac{1}{2} + z_m = -2m \quad\text{and}\quad 1 + 2z_m = -4m,$$
     both of which are negative even integers (simple trivial zeros of $\zeta$). By L'Hôpital's rule and the functional equation derivative identity $\zeta'(-2k) = \frac{(-1)^k(2k)!\,\zeta(2k+1)}{2\tau^{2k}}$, the simple zero of $\zeta(1/2 + z)$ in the denominator is **exactly canceled** by the simple zero of $\zeta(1 + 2z)$ in the numerator:
     $$\boxed{\lim_{z \to -(2m + 1/2)}\frac{\zeta(1 + 2z)}{\zeta(1/2 + z)} = \frac{2\,\zeta'(-4m)}{\zeta'(-2m)} = \frac{2(-1)^m (4m)!\,\zeta(4m + 1)}{\tau^{2m}(2m)!\,\zeta(2m + 1)} \ne 0 \qquad (\forall m \ge 1).}$$
   - At the interleaved half-integers $z_m' = -(2m - 1/2)$ ($m \ge 1$), $1 + 2z_m' = -(4m - 2)$ is a trivial zero of $\zeta$ while $1/2 + z_m' = -(2m - 1)$ is a negative odd integer where $\zeta(1 - 2m) = -B_{2m}/(2m) \ne 0$, so $\mathcal{M}[Q_\lambda](z_m') = 0$.
   - Conversely, in the right-half strip $0 < \operatorname{Re} z < 5/2$ (which governs nontrivial zeros $\rho = 1/2 + z = x + iy$ with $1/2 < x < 1$), $\operatorname{Re}(1 + 2z) = 2x > 1$ lies strictly inside the absolute Euler-product half-plane where $\zeta(1 + 2z) \ne 0$, and $\operatorname{Re}(5/4 - z/2) = \frac{3 - x}{2} \in (1, 5/4)$ where $\Gamma(5/4 - z/2) \ne 0$. Hence **no Gamma or zeta factor cancels a hypothetical off-critical zero $\rho = x + iy$ ($x > 1/2$) in $\mathcal{M}[Q_\mu](z)$ or $\mathcal{M}[Q_\lambda](z)$**.

| $m$ | $z_m = -(2m + 1/2)$ | $\frac{2\zeta'(-4m)}{\zeta'(-2m)} = \frac{2(-1)^m(4m)!\,\zeta(4m+1)}{\tau^{2m}(2m)!\,\zeta(2m+1)}$ (256-Bit Arb) | Removable Limit $\mathcal{M}[Q_\lambda](z_m)$ (256-Bit Arb) | Zero in L'Hôpital $-$ Closed-Form Diff |
| :---: | :---: | :--- | :--- | :---: |
| `1` | `-5/2` | `[-0.5144510963486600656422829086943568176724 +/- 2.66e-41]` | `[-0.3419422678073680807479723646161602579969 +/- 4.21e-41]` | `True` |
| `2` | `-9/2` | `[21.25847859667896134410645873294890505167 +/- 1.54e-39]` | `[35.32494386681079092751481553482480852379 +/- 3.92e-39]` | `True` |
| `3` | `-13/2` | `[-3263.743375417369866468185349559130633219 +/- 2.94e-37]` | `[-18977.52906064245353345175340858697136976 +/- 1.29e-36]` | `True` |

### 3.3 Simultaneous Finite-Prime Exclusion Identity and Convergent $P$-Smooth Inverse

**Theorem 3.1 (Finite-Prime Exclusion Sieve Identity and $P$-Smooth Inverse Reconstruction).**
Let $P \subset \mathbb{P}$ be any finite set of primes, let $N_P := \prod_{p\in P}p$, and let $\mathcal{S}(P) := \{m \ge 1 : p \mid m \implies p \in P\}$ denote the set of $P$-smooth positive integers.
1. For every integer $n \ge 1$ and every divisor $d \mid \gcd(n, N_P)$, complete multiplicativity $\lambda(a b) = \lambda(a)\lambda(b)$ and $\lambda(d)^2 = 1$ give $\mu(d)^2\lambda(n/d) = \lambda(n)\mu(d)$, and therefore
   $$\sum_{d \mid \gcd(n, N_P)}\mu(d)^2\lambda(n/d) = \lambda(n)\sum_{d \mid \gcd(n, N_P)}\mu(d) = \begin{cases}\lambda(n), & \gcd(n, N_P) = 1,\\ 0, & \gcd(n, N_P) > 1.\end{cases}$$
   *(Formalized on actual positive integers in Lean 4 theorem `actual_finite_prime_exclusion_sieve_identity_nat`.)*
2. Applying the commutative product operator $\mathcal{P}_P = \prod_{p\in P}(I + p^{-1/2}S_p) = \sum_{d \mid N_P}\frac{\mu(d)^2}{\sqrt{d}}S_d$ to $Q_\lambda(X)$ for $X > 0$ yields the coprime-filtered observable:
   $$\boxed{Q_{\lambda, P}(X) := \prod_{p\in P}\bigl(I + p^{-1/2}S_p\bigr)Q_\lambda(X) = \sum_{d \mid N_P}\frac{|\mu(d)|}{\sqrt{d}}\,Q_\lambda(X/d) = X^{5/2}\sum_{\substack{n\ge 1 \\ \gcd(n, N_P)=1}}\frac{\lambda(n)}{n^3}e^{-X^2/n^2}.}$$
3. Every integer $n \ge 1$ factors uniquely as $n = m r$ with $m \in \mathcal{S}(P)$ and $\gcd(r, N_P) = 1$. Since $\lambda(m r) = \lambda(m)\lambda(r)$, $Q_{\lambda, P}$ reconstructs $Q_\lambda$ via the absolutely convergent $P$-smooth series:
   $$\boxed{Q_\lambda(X) = \sum_{m \in \mathcal{S}(P)}\frac{\lambda(m)}{\sqrt{m}}\,Q_{\lambda, P}(X/m),}$$
   with explicit truncation remainder bound for any $M \ge 1$:
   $$\left|\sum_{\substack{m \in \mathcal{S}(P) \\ m > M}}\frac{\lambda(m)}{\sqrt{m}}\,Q_{\lambda, P}(X/m)\right| \le \zeta(3)X^{5/2}\sum_{m > M}m^{-3} \le \frac{\zeta(3)X^{5/2}}{2 M^2}.$$

All 12 test pairs $(P, X) \in \{(2,), (2,3), (2,3,5)\} \times \{1, 2, \tau, 4\}$ in `section_8_tc055_simultaneous_compatibility_and_joint_identities` (explicitly labeled `"same_observable_operator_vs_series_consistency_check"`) enclose zero in both $Q_{\lambda, P}^{\mathrm{direct}}(X) - Q_{\lambda, P}^{\mathrm{operator}}(X)$ and $Q_\lambda^{\mathrm{direct}}(X) - Q_\lambda^{\mathrm{inverse}}(X)$.

---

## 4. Coupled Cutoff Analysis, Weighted Norm Neumann Obstruction, and Off-Critical Mode Test

### 4.1 Signed Energy Expansion and Exact Coprime Decomposition for $P_u = \{p \le u\}$

For a prime cutoff $u \ge 2$, let $P_u := \{p \le u\}$ and $N_u := \prod_{p \le u}p$.
1. **Signed grade-interval energy expansion**:
   Expanding $Q_{\lambda, P_u}(X) = \sum_{d \mid N_u}\frac{|\mu(d)|}{\sqrt{d}}Q_\lambda(X/d)$ and integrating $|Q_{\lambda, P_u}(X)|^2\,\frac{dX}{X}$ over $[Y, \tau Y]$ gives the exact multi-scale energy relation retaining all diagonal ($d_1 = d_2$) and cross-scale ($d_1 \ne d_2$) terms:
   $$E_{\lambda, P_u}(Y) := \int_Y^{\tau Y}\bigl|Q_{\lambda, P_u}(X)\bigr|^2\,\frac{dX}{X} = \sum_{d \mid N_u}\frac{|\mu(d)|}{d}\,E_\lambda(Y/d) + 2\sum_{\substack{d_1, d_2 \mid N_u \\ d_1 < d_2}}\frac{|\mu(d_1)||\mu(d_2)|}{\sqrt{d_1 d_2}}\int_Y^{\tau Y}Q_\lambda(X/d_1)Q_\lambda(X/d_2)\,\frac{dX}{X}.$$
2. **Exact coprime decomposition and unconditional remainder bound**:
   Because every prime $p \le u$ divides $N_u$, the smallest integer $n \ge 2$ satisfying $\gcd(n, N_u) = 1$ is the first prime $p > u$, so every coprime index $n \ge 2$ satisfies $n > u$. Separating the $n = 1$ Gaussian term gives the exact identity for all $w > 0$ and $u \ge 2$:
   $$\boxed{Q_{\lambda, P_u}(w) = w^{5/2}e^{-w^2} + R_{\lambda, P_u}(w), \qquad R_{\lambda, P_u}(w) := w^{5/2}\sum_{\substack{n > u \\ \gcd(n, N_u)=1}}\frac{\lambda(n)}{n^3}e^{-w^2/n^2},}$$
   with unconditional pointwise bound
   $$\boxed{\bigl|R_{\lambda, P_u}(w)\bigr| \le w^{5/2}\sum_{n > u}\frac{1}{n^3} \le \frac{w^{5/2}}{2 u^2} \qquad (\forall w > 0,\;u \ge 1).}$$
   *(Certified in 256-bit Arb across $u \in \{5, 7, 11, 13\}$ and $w \in \{1, 2, 4\}$ in `section_9_tc055_coupled_cutoff_and_norm_obstruction`.)*
3. **Diagnosis of the coupled cutoff regime $u = u(Y)$**:
   Substituting $Q_{\lambda, P_u}(X/m) = (X/m)^{5/2}e^{-X^2/m^2} + R_{\lambda, P_u}(X/m)$ into the inverse reconstruction $Q_\lambda(X) = \sum_{m \in \mathcal{S}(P_u)}\frac{\lambda(m)}{\sqrt{m}}Q_{\lambda, P_u}(X/m)$ splits $Q_\lambda(X)$ into the $P_u$-smooth sum plus the rough-cofactor sum:
   $$Q_\lambda(X) = X^{5/2}\sum_{m \in \mathcal{S}(P_u)}\frac{\lambda(m)}{m^3}e^{-X^2/m^2} + X^{5/2}\sum_{m \in \mathcal{S}(P_u)}\sum_{\substack{n > u \\ \gcd(n, N_u)=1}}\frac{\lambda(m)\lambda(n)}{(m n)^3}e^{-X^2/(m n)^2}.$$
   - If $u > \tau Y$, then every integer $k \le \tau Y$ is $P_u$-smooth, so the first sum contains the entire transition range $m \asymp X \in [Y, \tau Y]$ unmodified while the second sum only contains products $m n > u > \tau Y$ in the subtransition tail.
   - If $u = Y^\theta$ with fixed $\theta \in (0, 1)$, the $P_u$-smooth integers $m \asymp X$ have positive Dickman–de Bruijn density $\rho_{\mathrm{Dickman}}(1/\theta) > 0$, so the unsigned $P_u$-smooth transition sum has magnitude $\asymp \rho_{\mathrm{Dickman}}(1/\theta)\sqrt{Y}$ (energy $\asymp Y$), while the unsigned rough-cofactor sum over $m \in \mathcal{S}(P_u)$ and $n > u$ with $m n \asymp X$ has magnitude $\asymp (1 - \rho_{\mathrm{Dickman}}(1/\theta))\sqrt{Y}$. Thus coupling $u = u(Y)$ partitions the transition mass between $P_u$-smooth and $P_u$-rough factors without eliminating the order-$Y$ unsigned transition energy unless signed cancellation of $\lambda(m)$ on $\mathcal{S}(P_u)$ is independently proved.

### 4.2 Weighted Norm Obstruction and Off-Critical Mode Multiplier

1. **Weighted norm Neumann majorant on $\mathcal{H}_\eta = L^2((0,\infty), X^{-2\eta}\,dX/X)$ ($\eta > 0$)**:
   For $S_p F(X) = F(X/p)$, changing variables $X = p u$ gives $\|S_p F\|_\eta^2 = \int_0^\infty |F(u)|^2 (p u)^{-2\eta}\,\frac{du}{u} = p^{-2\eta}\|F\|_\eta^2$, so $\|S_p\|_{\mathcal{B}(\mathcal{H}_\eta)} = p^{-\eta}$. On each prime factor $(I + p^{-1/2}S_p)^{-1} = \sum_{k\ge 0}(-1)^k p^{-k/2}S_p^k$, the triangle-inequality Neumann majorant over $P_u = \{p \le u\}$ is
   $$M_{\mathrm{Neumann}}(u, \eta) := \prod_{p \le u}\bigl(1 - p^{-1/2 - \eta}\bigr)^{-1} = \sum_{m \in \mathcal{S}(P_u)} m^{-1/2 - \eta}.$$
   - For $\eta > 1/2$, $\frac{1}{2} + \eta > 1$, so $\lim_{u\to\infty} M_{\mathrm{Neumann}}(u, \eta) = \zeta(1/2 + \eta) < \infty$ is uniformly bounded;
   - For $0 < \eta \le 1/2$, $\frac{1}{2} + \eta \le 1$, so $M_{\mathrm{Neumann}}(u, \eta) \to \infty$ as $u \to \infty$ (as $e^\gamma \log u$ at $\eta = 1/2$ by Mertens' theorem, and as $\exp(\frac{(1+o(1))u^{1/2-\eta}}{(1/2-\eta)\log u})$ for $0 < \eta < 1/2$).
   - **What signed improvement would be needed**: Reaching $\eta \in (0, 1/2]$ (corresponding to $\operatorname{Re} s = 1/2 + \eta \in (1/2, 1]$) requires bounding the signed Mellin multiplier $\prod_{p\le u}(1 + p^{-1/2 - \eta - ib})^{-1} = \sum_{m \in \mathcal{S}(P_u)}\lambda(m)m^{-1/2 - \eta - ib}$ on the vertical line $z = \eta + ib$ without replacing $\lambda(m)m^{-ib}$ by $+1$.
2. **Off-critical mode test**:
   On an off-critical mode $F_\rho(X) := X^{\rho - 1/2}$ ($\rho = x + iy$, $x > 0$), $p^{-1/2}S_p F_\rho(X) = p^{-\rho}F_\rho(X)$, so
   $$\mathcal{P}_{P_u} F_\rho(X) = M_u(\rho)\,F_\rho(X), \qquad M_u(\rho) := \prod_{p \le u}\bigl(1 + p^{-\rho}\bigr),$$
   which satisfies the two-sided nonvanishing bounds for every finite $u \ge 2$ and every $x > 0$:
   $$\boxed{0 < \prod_{p \le u}\bigl(1 - p^{-x}\bigr) \le \bigl|M_u(\rho)\bigr| \le \prod_{p \le u}\bigl(1 + p^{-x}\bigr) < \infty.}$$
   Thus no finite prime exclusion filter $\mathcal{P}_{P_u}$ can annihilate an off-critical mode $X^{\rho - 1/2}$.

---

## 5. Integrated Energy Kernel $K_Y(m, n)$, Diagonal Asymptotic $D_E(Y)$, and Near-Diagonal Band Bound

### 5.1 Exact Kernel Representation and Closed-Form Gaussian Antiderivative

Expanding $|Q_\lambda(X)|^2$ and integrating term-by-term against $\frac{dX}{X}$ over $[Y, \tau Y]$ (justified by uniform convergence on compact intervals $[Y, \tau Y]$) gives
$$\boxed{E_\lambda(Y) = \int_Y^{\tau Y}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} = \sum_{m, n \ge 1}\lambda(m)\lambda(n)K_Y(m, n),}$$
where the symmetric positive kernel $K_Y(m, n)$ is
$$K_Y(m, n) := \frac{1}{(m n)^3}\int_Y^{\tau Y} X^4 \exp\!\left(-X^2\left(\frac{1}{m^2} + \frac{1}{n^2}\right)\right)dX > 0.$$
Setting $\alpha := m^{-2} + n^{-2} > 0$, integration by parts twice yields the exact closed-form antiderivative
$$\int X^4 e^{-\alpha X^2}\,dX = \frac{3\sqrt{\tau/2}}{8\,\alpha^{5/2}}\operatorname{erf}(\sqrt{\alpha}\,X) - \left(\frac{X^3}{2\alpha} + \frac{3X}{4\alpha^2}\right)e^{-\alpha X^2},$$
which is evaluated in 256-bit Arb in `evaluate_energy_kernel_K_Y_certified_arb` (using $\operatorname{erf}(u_2) - \operatorname{erf}(u_1)$ for $u_2 \le 1$ and $\operatorname{erfc}(u_1) - \operatorname{erfc}(u_2)$ for $u_2 > 1$).

### 5.2 Unconditional Diagonal Energy Asymptotic $D_E(Y)$ for All $Y > 0$

**Theorem 5.1 (Diagonal Energy Asymptotic with Explicit Euler–Maclaurin Error Constants).**
For every $Y > 0$, the diagonal energy sum $D_E(Y) := \sum_{n\ge 1} K_Y(n, n)$ satisfies
$$\boxed{D_E(Y) = \frac{3\sqrt{\tau}}{64}\log\tau + R_{D, E}(Y), \qquad \bigl|R_{D, E}(Y)\bigr| \le C_{D, 2}\,Y^{-2} \quad\text{and}\quad \bigl|R_{D, E}(Y)\bigr| \le C_{D, 4}\,Y^{-4} \qquad (\forall Y > 0),}$$
where:
- $\frac{3\sqrt{\tau}}{64}\log\tau \in [0.2159472478105097999629716116351322819076 \pm 3.24 \times 10^{-41}]$,
- $C_{D, 2} := \frac{C_2(1 - \tau^{-2})}{16\sqrt{2}} \in [0.07974240995631961059711944730929191094454 \pm 4.2 \times 10^{-44}]$,
- $C_{D, 4} := \frac{C_4(1 - \tau^{-4})}{64\sqrt{2}} \in [0.09663891408812621065182768769598639544928 \pm 1.86 \times 10^{-42}]$,
with $C_2 \in [1.851257667016958056850958359201349291641 \pm 2.00 \times 10^{-39}]$ and $C_4 \in [8.752371760035365551239039765015814873069 \pm 4.00 \times 10^{-39}]$ from Theorem 4.1 of [`TC_LIOUVILLE_SQUARE_DILATION.md`](./TC_LIOUVILLE_SQUARE_DILATION.md).

*Proof.* By Tonelli's theorem for nonnegative series,
$$D_E(Y) = \sum_{n\ge 1}\int_Y^{\tau Y} X^4 n^{-6}e^{-2X^2/n^2}\,dX = \int_Y^{\tau Y} X^4 \left(\sum_{n\ge 1} n^{-6}e^{-L_{1,1}(X)^2/n^2}\right)dX, \qquad L_{1,1}(X) := \sqrt{2}\,X.$$
By the fixed-order periodic Bernoulli Euler–Maclaurin theorem (Theorem 4.1 of `TC_LIOUVILLE_SQUARE_DILATION.md`) applied at $L = \sqrt{2}\,X > 0$, for every even $N \in \{2, 4\}$ and every $X > 0$:
$$\sum_{n\ge 1} n^{-6}e^{-2X^2/n^2} = c_0 (\sqrt{2}\,X)^{-5} + E_{1,1}(X), \qquad \bigl|E_{1,1}(X)\bigr| \le C_N (\sqrt{2}\,X)^{-5-N} = \frac{C_N}{2^{(5+N)/2}}\,X^{-5-N},$$
where $c_0 = \frac{3\sqrt{\tau/2}}{8}$. Since $c_0(\sqrt{2})^{-5} = \frac{3\sqrt{\tau/2}}{8 \cdot 4\sqrt{2}} = \frac{3\sqrt{\tau}}{64}$, multiplying by $X^4$ and integrating over $X \in [Y, \tau Y]$ gives
$$\int_Y^{\tau Y} X^4 \cdot c_0(\sqrt{2}\,X)^{-5}\,dX = \frac{3\sqrt{\tau}}{64}\int_Y^{\tau Y}\frac{dX}{X} = \frac{3\sqrt{\tau}}{64}\log\tau,$$
and
$$\bigl|R_{D, E}(Y)\bigr| \le \frac{C_N}{2^{(5+N)/2}}\int_Y^{\tau Y} X^{-1-N}\,dX = \frac{C_N(1 - \tau^{-N})}{N \cdot 2^{(5+N)/2}}\,Y^{-N}.$$
Setting $N = 2$ ($2 \cdot 2^{7/2} = 16\sqrt{2}$) and $N = 4$ ($4 \cdot 2^{9/2} = 64\sqrt{2}$) yields $C_{D, 2}Y^{-2}$ and $C_{D, 4}Y^{-4}$ for all $Y > 0$. $\blacksquare$

### 5.3 Unconditional Near-Diagonal Band Inequality for Every $H \ge 0$

**Proposition 5.2 (Near-Diagonal Band Bound).**
For all $m, n \ge 1$ and $Y > 0$, $2 K_Y(m, n) \le K_Y(m, m) + K_Y(n, n)$, and for every integer $H \ge 0$:
$$\boxed{\left|\sum_{|m - n| \le H}\lambda(m)\lambda(n)K_Y(m, n)\right| \le \sum_{|m - n| \le H} K_Y(m, n) \le (2H + 1)D_E(Y).}$$

*Proof.* For each $X > 0$, the integrand of $K_Y(m, n)$ is $X^4 \phi_X(m)\phi_X(n)$ with $\phi_X(m) := m^{-3}e^{-X^2/m^2} > 0$. Since $2\phi_X(m)\phi_X(n) \le \phi_X(m)^2 + \phi_X(n)^2$ with strict inequality for $m \ne n$, integrating against $X^4\,dX$ over $[Y, \tau Y]$ gives $2 K_Y(m, n) \le K_Y(m, m) + K_Y(n, n)$. For each integer offset $h \in \{1, \dots, H\}$, summing over $m \ge 1$ yields
$$2\sum_{m\ge 1} K_Y(m, m+h) \le \sum_{m\ge 1} K_Y(m, m) + \sum_{m\ge 1} K_Y(m+h, m+h) \le 2 D_E(Y).$$
Summing over $h = 0$ (which contributes $D_E(Y)$) and the $H$ symmetric pairs $\pm h$ ($1 \le h \le H$, each contributing at most $2 D_E(Y)$) proves $\sum_{|m - n| \le H} K_Y(m, n) \le (2H + 1)D_E(Y)$. *(Formalized in Lean 4 theorem `near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing` and certified in 256-bit Arb across $Y \in \{1, 2, 4\}$ and $H \in \{0, 1, 2, 4\}$.)* $\blacksquare$

> **Consequence for `SUBGATE-TC-043A`**: For any bandwidth $H = O(Y^\varepsilon)$, the entire diagonal and near-diagonal band $|m - n| \le H$ contributes at most $(2H + 1)D_E(Y) = O(Y^\varepsilon)$. Therefore, any violation of $E_\lambda(Y) \ll_\varepsilon Y^\varepsilon$ must arise exclusively from the **wide off-diagonal transition correlations** $|m - n| > H$ with $m, n \asymp Y$.

---

## 6. Opposite-Parity Prime–Semiprime Dilation Pairing and Exact Residual Diagnosis

### 6.1 Candidate Lemma: Pairwise Opposite-Parity MVT Kernel-Difference Bound

**Lemma 6.1 (Opposite-Parity Prime–Semiprime Dilation Pairing Bound).**
Let $p$ be a prime and let $s = q r$ be a semiprime ($q, r$ prime, not necessarily distinct). Then for every $m \ge 1$:
1. $\lambda(p m) = -\lambda(m)$ and $\lambda(q r m) = +\lambda(m)$, so $\lambda(p m) + \lambda(q r m) = 0$ and for every $n \ge 1$:
   $$\lambda(p m)\lambda(n)K_Y(p m, n) + \lambda(q r m)\lambda(n)K_Y(q r m, n) = \lambda(m)\lambda(n)\bigl(K_Y(q r m, n) - K_Y(p m, n)\bigr).$$
2. Setting $u_{\min} := \min(p, q r)$ and $u_{\max} := \max(p, q r)$, for all $m, n \ge 1$ and all $Y > 0$:
   $$\boxed{\bigl|K_Y(p m, n) - K_Y(q r m, n)\bigr| \le 3\,\frac{|q r - p|}{u_{\min}}\left(\frac{u_{\max}}{u_{\min}}\right)^3 K_Y(u_{\max} m, n).}$$

*Proof.* Part (1) follows from $\Omega(p m) = \Omega(m) + 1$ and $\Omega(q r m) = \Omega(m) + 2$ (proved on actual positive integers in Lean 4 theorem `near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing`). For part (2), fix $X > 0$ and define $g_X(u) := u^{-3}e^{-X^2/u^2}$ for $u > 0$. Differentiating gives
$$g_X'(u) = u^{-4}\left(\frac{2 X^2}{u^2} - 3\right)e^{-X^2/u^2}.$$
Let $w := X/u > 0$. For $w > 0$, the function $\psi(w) := (2w^2 - 3)e^{-w^2}$ has derivative $\psi'(w) = 2w(5 - 2w^2)e^{-w^2}$, so $\psi(0^+) = -3$, $\max_{w > 0}\psi(w) = \psi(\sqrt{5/2}) = 2e^{-5/2} \approx 0.164 < 3$, and $\sup_{w > 0}|2w^2 - 3|e^{-w^2} = 3$. Furthermore, for every $u \in [u_1, u_2]$ with $u_1 := u_{\min} m$ and $u_2 := u_{\max} m$, since $u^{-4} \le u_1^{-4}$ and $e^{-X^2/u^2}$ is strictly increasing in $u$ ($e^{-X^2/u^2} \le e^{-X^2/u_2^2}$):
$$\bigl|g_X(u_2) - g_X(u_1)\bigr| \le \int_{u_1}^{u_2}\bigl|g_X'(u)\bigr|\,du \le (u_2 - u_1)\cdot 3\,u_1^{-4} e^{-X^2/u_2^2} = 3\,\frac{|q r - p|}{u_{\min}}\left(\frac{u_{\max}}{u_{\min}}\right)^3 u_2^{-3}e^{-X^2/u_2^2}.$$
Multiplying by $X^4 n^{-3}e^{-X^2/n^2}$ and integrating over $X \in [Y, \tau Y]$ yields the stated bound. *(Certified in 256-bit Arb across all 12 test cases $(p, q r) \in \{(5, 4), (7, 6), (11, 10), (13, 15)\}$ and $(Y, m, n) \in \{(4, 2, 8), (8, 3, 15), (16, 4, 20)\}$ in `section_11_tc055_opposite_parity_dilation_pairing`.)* $\blacksquare$

### 6.2 Exact Obstruction to Closing `SUBGATE-TC-043A` by Opposite-Parity Pairing Alone

While Lemma 6.1 saves the relative factor $\frac{|q r - p|}{\min(p, q r)}$ (for instance $1/4$ for $(5, 4)$, $1/6$ for $(7, 6)$, $1/10$ for $(11, 10)$) on each matched pair $(p m, q r m)$, attempting to sum Lemma 6.1 over $m$ to bound the full transition sum $\sum_k \lambda(k)g_X(k)$ encounters three exact quantitative obstructions:
1. **Unmatched coprime integers of positive density**:
   Any linear combination of prime-dilated and semiprime-dilated sums $\sum_{p \in P_1}\alpha_p \sum_m \lambda(p m)g_X(p m) + \sum_{s \in P_2}\beta_s \sum_m \lambda(s m)g_X(s m)$ regroups by product index $k = p m$ or $s m$ with divisor weight $W_{\mathrm{pair}}(k) := \sum_{p \in P_1,\,p \mid k}\alpha_p + \sum_{s \in P_2,\,s \mid k}\beta_s$. Every integer $k$ coprime to $\prod_{p \in P_1}p \cdot \prod_{s \in P_2}s$ has $W_{\mathrm{pair}}(k) = 0$ (for $P_1 = \{5, 7, 11\}$ and $P_2 = \{4, 6, 10\}$, `101` of the `240` integers $1 \le k \le 240$ have $W_{\mathrm{pair}}(k) = 0$, and all `240` have $W_{\mathrm{pair}}(k) \ne \bar{w} = \frac{4391}{4620}$). In particular, if the active pairing factors satisfy $p, q r \le Y^\theta$ ($\theta < 1$), every prime $k \in [Y, \tau Y]$ has no factor in $P_1 \cup P_2$ and remains completely unmatched, contributing unsigned transition energy of order $Y$.
2. **Transition window boundary mismatch**:
   In a transition block $k \in [Y, \tau Y]$, the cofactor ranges $m \in [Y/p, \tau Y/p]$ and $m \in [Y/(q r), \tau Y/(q r)]$ differ at both endpoints by $\frac{|q r - p|}{p q r}Y$ terms, producing unmatched boundary sums of the same scale $\frac{|q r - p|}{p}Y$ as the interior MVT difference.
3. **Multiplicity fluctuation**:
   Because the indicator $1_{d \mid k}$ fluctuates around $1/d$, replacing the constant weight $1$ on $k$ by $W_{\mathrm{pair}}(k)/\bar{w}$ leaves the discrepancy $1 - W_{\mathrm{pair}}(k)/\bar{w}$, whose unsigned square has positive mean over $k \asymp Y$.

---

## 7. Multiplicative Parity Controls $a_2(n) = (-1)^{v_2(n)}$ and $a_S(n)$

To test whether any subset of the TC hypotheses (complete multiplicativity, unconstrained common-factor cancellation, transition Poisson summation, and finite-prime exclusion) could by itself imply $E_a(Y) = o(Y)$, define for any finite set of primes $S \subset \mathbb{P}$ the completely multiplicative parity control
$$a_S(n) := (-1)^{\sum_{p \in S} v_p(n)}, \qquad a_2(n) := a_{\{2\}}(n) = (-1)^{v_2(n)}.$$

### 7.1 Hypothesis-by-Hypothesis Comparison Against $\lambda(n)$

| Mathematical Property / Identity | Actual Liouville $\lambda(n) = (-1)^{\Omega(n)}$ | 2-Adic Control $a_2(n) = (-1)^{v_2(n)}$ | Finite-Prime Control $a_S(n)$ ($S$ finite) |
| :--- | :---: | :---: | :---: |
| Complete multiplicativity $a(m n) = a(m)a(n)$ and unit square $a(d)^2 = 1$ | **Holds** | **Holds** | **Holds** |
| Unconstrained common-factor cancellation $a(d r)a(d s) = a(r)a(s)$ ($\forall d, r, s \ge 1$) | **Holds** | **Holds** | **Holds** |
| Common-factor $d$-sum $\sum_{d\ge 1}d^{-6}e^{-L^2/d^2}$, Euler–Maclaurin bound, and Poisson summation | **Holds** | **Holds** | **Holds** |
| Parity flip $a(p n) = -a(n)$ and exclusion $(I + p^{-1/2}S_p)Q_a(X)$ for $p \in S$ | **Holds** | **Holds** ($S = \{2\}$) | **Holds** ($p \in S$) |
| Parity flip $a(p n) = -a(n)$ at **all** primes $p \in \mathbb{P}$ | **Holds** | **Fails** ($a_2(p) = +1$ for $p \ge 3$) | **Fails** ($a_S(p) = +1$ for $p \notin S$) |
| Square-divisor Möbius link $a(n) = \sum_{d^2 \mid n}\mu(n/d^2)$ and pole cancellation at $s = 1$ | **Holds** ($D_\lambda(s) = \frac{\zeta(2s)}{\zeta(s)}$) | **Fails** ($a_2(3) = +1 \ne -1 = \mu(3)$) | **Fails** ($D_{a_S}(s) = \zeta(s)\prod_{p\in S}\frac{1 - p^{-s}}{1 + p^{-s}}$) |

### 7.2 Unconditional Asymptotic Proofs for $Q_{a_2}(X)$ and $E_{a_2}(Y)$

**Theorem 7.1 (Asymptotic Linear Energy Growth for the 2-Adic Parity Control $a_2$).**
Let $Q_{\mathbf{1}}(X) := X^{5/2}\sum_{n\ge 1} n^{-3}e^{-X^2/n^2}$ and $Q_{a_2}(X) := X^{5/2}\sum_{n\ge 1}\frac{a_2(n)}{n^3}e^{-X^2/n^2}$. Then:
1. **Unimodal Euler–Maclaurin approximation for $Q_{\mathbf{1}}(X)$**: For all $X > 0$,
   $$\boxed{\left|Q_{\mathbf{1}}(X) - \frac{\sqrt{X}}{2}\right| \le \left(\frac{3}{e}\right)^{3/2} X^{-1/2}.}$$
2. **Exact dyadic exclusion and dyadic series identities**: For all $X > 0$,
   $$\bigl(I + 2^{-1/2}S_2\bigr)Q_{a_2}(X) = Q_{\mathrm{odd}}(X) = Q_{\mathbf{1}}(X) - 2^{-1/2}Q_{\mathbf{1}}(X/2) > 0,$$
   $$Q_{a_2}(X) = Q_{\mathbf{1}}(X) + 2\sum_{k\ge 1}(-1)^k 2^{-k/2}Q_{\mathbf{1}}(X/2^k).$$
3. **Pointwise and grade-interval energy asymptotics**: As $X, Y \to \infty$,
   $$\boxed{Q_{a_2}(X) = \frac{\sqrt{X}}{6} + O\bigl(X^{-1/2}\bigr) \sim \frac{\sqrt{X}}{6}, \qquad E_{a_2}(Y) := \int_Y^{\tau Y}\bigl|Q_{a_2}(X)\bigr|^2\,\frac{dX}{X} = \frac{\tau - 1}{36}\,Y + O(1) \sim \frac{\tau - 1}{36}\,Y,}$$
   where $\frac{1}{6} \in [0.1666666666666666666666666666666666666667 \pm 3.34 \times 10^{-41}]$ and $\frac{\tau - 1}{36} \in [0.1467551474216551799145912990710834935665 \pm 9.42 \times 10^{-42}]$. More generally, for any finite prime set $S$,
   $$Q_{a_S}(X) \sim \frac{1}{2}\left(\prod_{p \in S}\frac{p - 1}{p + 1}\right)\sqrt{X}, \qquad E_{a_S}(Y) \sim \frac{\tau - 1}{4}\left(\prod_{p \in S}\frac{p - 1}{p + 1}\right)^2 Y.$$

*Proof.*
1. For fixed $X > 0$, $h_X(t) := t^{-3}e^{-X^2/t^2}$ is unimodal on $(0, \infty)$, strictly increasing on $(0, X\sqrt{2/3}]$ and strictly decreasing on $[X\sqrt{2/3}, \infty)$, with maximum $\max_{t > 0}h_X(t) = h_X(X\sqrt{2/3}) = (\frac{3}{2e})^{3/2}X^{-3}$ and integral $\int_0^\infty t^{-3}e^{-X^2/t^2}\,dt = \frac{1}{2}X^{-2}$ (under $v = X^2/t^2$). By the unimodal sum-integral comparison $|\sum_{n\ge 1}h_X(n) - \int_0^\infty h_X(t)\,dt| \le 2\max_{t>0}h_X(t)$, multiplying by $X^{5/2}$ gives $|Q_{\mathbf{1}}(X) - \frac{1}{2}\sqrt{X}| \le 2(\frac{3}{2e})^{3/2}X^{-1/2} = (\frac{3}{e})^{3/2}X^{-1/2}$.
2. Since $a_2(n) = +1$ for odd $n$, $(I + 2^{-1/2}S_2)Q_{a_2}(X) = X^{5/2}\sum_{2\nmid n}n^{-3}e^{-X^2/n^2} = Q_{\mathbf{1}}(X) - 2^{-1/2}Q_{\mathbf{1}}(X/2)$. Writing $v_2(n) = k \ge 0$ gives $a_2(n) = (-1)^k = 1 + 2\sum_{j=1}^k (-1)^j$, so $\sum_{n\ge 1}a_2(n)\phi(n) = \sum_{n\ge 1}\phi(n) + 2\sum_{j\ge 1}(-1)^j\sum_{2^j \mid n}\phi(n)$, which yields $Q_{a_2}(X) = Q_{\mathbf{1}}(X) + 2\sum_{k\ge 1}(-1)^k 2^{-k/2}Q_{\mathbf{1}}(X/2^k)$.
3. For $2^k \le X$, part (1) gives $2^{-k/2}Q_{\mathbf{1}}(X/2^k) = \frac{1}{2}\sqrt{X}\,2^{-k} + O(X^{-1/2})$, while for $2^k > X$ the universal bound $Q_{\mathbf{1}}(w) \le \zeta(3)w^{5/2}$ gives $\sum_{2^k > X}2^{-k/2}Q_{\mathbf{1}}(X/2^k) \le \zeta(3)X^{5/2}\sum_{2^k > X}2^{-3k} = O(X^{-1/2})$. Since $1 + 2\sum_{k\ge 1}(-1)^k 2^{-k} = 1 - \frac{2}{3} = \frac{1}{3}$ (and $\sum_{2^k > X}2^{-k} = O(X^{-1})$), we obtain
   $$Q_{a_2}(X) = \frac{\sqrt{X}}{2}\left(1 + 2\sum_{k\ge 1}(-1)^k 2^{-k}\right) + O\bigl(X^{-1/2}\bigr) = \frac{\sqrt{X}}{6} + O\bigl(X^{-1/2}\bigr).$$
   Squaring gives $|Q_{a_2}(X)|^2 = \frac{X}{36} + O(1)$, and integrating against $\frac{dX}{X}$ over $[Y, \tau Y]$ gives $E_{a_2}(Y) = \frac{1}{36}\int_Y^{\tau Y}dX + O\!\left(\int_Y^{\tau Y}\frac{dX}{X}\right) = \frac{\tau - 1}{36}\,Y + O(1)$. $\blacksquare$

| $X$ / $Y$ | $Q_{a_2}(X)$ (256-Bit Arb) | $Q_{a_2}(X)/\sqrt{X}$ vs. $\frac{1}{6} \approx 0.166667$ | $E_{a_2}(Y)$ (256-Bit Arb) | $\frac{\tau - 1}{36}\,Y$ (256-Bit Arb) |
| :---: | :--- | :---: | :--- | :--- |
| `4` | `[0.4534 +/- 6.12e-5]` | `0.226725` | `[0.223961, 1.081398]` | `0.5870205897` |
| `8` | `[0.3853 +/- 9.17e-5]` | `0.136214` | `[0.398249, 1.953713]` | `1.1740411794` |
| `16` | `[0.727 +/- 8.25e-4]` | `0.181867` | `[0.781315, 4.112366]` | `2.3480823587` |
| `32` | `[0.90 +/- 2.96e-3]` | `0.158933` | `[1.184239, 8.228446]` | `4.6961647175` |
| `64` | `[1.36 +/- 6.76e-3]` | `0.170289` | — | — |

---

## 8. Summary of Surviving Unconditional Theorems vs. Open Obstruction

### 8.1 Surviving Unconditional Theorems Established in `TASK-TC-055`

1. **Exact Removable Trivial-Zero Cancellation in $\mathcal{M}[Q_\lambda](z)$**: At $z_m = -(2m + 1/2)$ ($m \ge 1$), $\lim_{z\to z_m}\frac{\zeta(1+2z)}{\zeta(1/2+z)} = \frac{2\zeta'(-4m)}{\zeta'(-2m)} = \frac{2(-1)^m(4m)!\,\zeta(4m+1)}{\tau^{2m}(2m)!\,\zeta(2m+1)} \ne 0$.
2. **Simultaneous Finite-Prime Exclusion Identity and $P$-Smooth Inverse**: $Q_{\lambda, P}(X) = \prod_{p\in P}(I + p^{-1/2}S_p)Q_\lambda(X) = \sum_{d \mid N_P}\frac{|\mu(d)|}{\sqrt{d}}Q_\lambda(X/d)$ and $Q_\lambda(X) = \sum_{m \in \mathcal{S}(P)}\frac{\lambda(m)}{\sqrt{m}}Q_{\lambda, P}(X/m)$, with coprime tail bound $|Q_{\lambda, P_u}(w) - w^{5/2}e^{-w^2}| \le \frac{w^{5/2}}{2u^2}$ ($u \ge 2$) and Lean 4 formalization `actual_finite_prime_exclusion_sieve_identity_nat`.
3. **Unconditional Diagonal Energy Asymptotic and Near-Diagonal Band Bound**: $D_E(Y) = \frac{3\sqrt{\tau}}{64}\log\tau + R_{D,E}(Y)$ with $|R_{D,E}(Y)| \le C_{D,2}Y^{-2}$ ($C_{D,2} \approx 0.07974241$) for all $Y > 0$, and $\sum_{|m - n| \le H}K_Y(m, n) \le (2H + 1)D_E(Y)$ for all $H \ge 0$ (formalized in Lean 4 theorem `near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing`).
4. **Opposite-Parity Prime–Semiprime Dilation Pairing Bound**: For prime $p$ and semiprime $q r$, $\lambda(p m) + \lambda(q r m) = 0$ and $|K_Y(p m, n) - K_Y(q r m, n)| \le 3\frac{|q r - p|}{\min(p, q r)}(\frac{\max(p, q r)}{\min(p, q r)})^3 K_Y(\max(p, q r)m, n)$.
5. **Multiplicative Parity Control Theorem**: For $a_2(n) = (-1)^{v_2(n)}$, $Q_{a_2}(X) = \frac{\sqrt{X}}{6} + O(X^{-1/2}) \sim \frac{\sqrt{X}}{6}$ and $E_{a_2}(Y) = \frac{\tau - 1}{36}Y + O(1) \sim \frac{\tau - 1}{36}Y$ (formalized in Lean 4 theorem `prime_parity_control_multiplicative_and_moebius_separation_nat`).

### 8.2 Exact Remaining Obstruction to `SUBGATE-TC-043A`

- Every finite-prime exclusion operator $\mathcal{P}_{P_u} = \prod_{p \le u}(I + p^{-1/2}S_p)$ is a bounded invertible multiplier on $\mathcal{H}_\eta$ ($\eta > 0$) whose off-critical mode multiplier $M_u(\rho) = \prod_{p \le u}(1 + p^{-\rho})$ satisfies $0 < \prod_{p \le u}(1 - p^{-x}) \le |M_u(\rho)| \le \prod_{p \le u}(1 + p^{-x})$ for $x > 0$, and whose triangle-inequality inverse majorant $\prod_{p \le u}(1 - p^{-1/2-\eta})^{-1}$ diverges as $u \to \infty$ for $0 < \eta \le 1/2$.
- Any finite-prime parity control $a_S(n) = (-1)^{\sum_{p\in S}v_p(n)}$ satisfies complete multiplicativity, unconstrained common-factor cancellation, transition Poisson summation, and finite-prime exclusion on $S$, yet has $E_{a_S}(Y) \asymp_S Y$ because $D_{a_S}(s)$ retains a pole at $s = 1$.
- Therefore, improving the unconditional global Stieltjes bound $E_\lambda(Y) \ll Y\exp(-2c_2(\log Y)^{3/5}(\log\log Y)^{-1/5}) \ll_D Y(\log Y)^{-D}$ (`TC-054R`) to a power saving $E_\lambda(Y) \ll Y^{1-\eta}$ or arbitrary subpower saving $E_\lambda(Y) \ll_\varepsilon Y^\varepsilon$ requires controlling the wide off-diagonal signed correlation $\sum_{|m - n| > H}\lambda(m)\lambda(n)K_Y(m, n)$ at $m, n \asymp Y$ using the parity flip $\lambda(p n) = -\lambda(n)$ across **infinitely many primes simultaneously** (equivalently, bounding the signed Euler-product inverse $\prod_{p \le u}(1 + p^{-1/2-\eta-ib})^{-1}$ on $0 < \eta \le 1/2$ without taking absolute values). Accordingly, `SUBGATE-TC-043A` remains `OPEN` and `rh_proved` remains `false`.
