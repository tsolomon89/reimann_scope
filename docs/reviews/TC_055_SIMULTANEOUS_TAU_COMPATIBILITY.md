# Mathematical Review & Proof Attempt Report: Simultaneous $\tau$-Compatibility, Pairing Bound Repair, Full-Space Operator Norm Obstruction, and Finite Arithmetic Energy Reconstruction (`TASK-TC-055` & `TASK-TC-055R`)

- **Task ID**: `TASK-TC-055` (`task/tc-055-simultaneous-tau-compatibility-and-signed-energy-cancellation`)
- **Repair Task ID**: `TASK-TC-055R` (`task/tc-055r-pairing-bound-operator-norm-and-finite-energy-repair`)
- **Parent Epic**: `EPIC-TC-042` (Canonical $\tau$-Adelic Theta-Correlation Bound and Hilbert-Schmidt Orbit Control)
- **Merged `main` Baseline (`TC-054R2` merge)**: `8a898c60b7c4cb56543a3d1e7960c39e00027c22`
- **Prior `TC-054R2` Implementation / Reviewed HEAD**: `27489f195d3313d9ee60773157e3a8240f5bcadd` / `f265042ab52cabda29e76859cebace21cfae9239`
- **Reviewed `TC-055` Implementation / Reviewed HEAD**: `c44df1ebfd10b8010e216214229a420ce8f3b5c2` / `07db77cf0ee62aa42e5c87b28a89a8f98eb3271e`
- **Initial Focused Closeout Commit (Section 2)**: `80d1c86408d39562b06b2c69d4b4f655a1677f82`
- **Primary Implementation Module**: [`tc/liouville_square_dilation.py`](../../tc/liouville_square_dilation.py)
- **Serialized 256-Bit Arb Certificate**: [`data/tc_liouville_square_dilation.json`](../../data/tc_liouville_square_dilation.json)
- **Formal Lean 4 Module**: [`formal/RiemannScope/LiouvilleSquareDilation.lean`](../../formal/RiemannScope/LiouvilleSquareDilation.lean) (`21` definitions, `12` public theorems, `16` private helper theorems = `49` declarations, `0` `sorry`, `0` custom `axiom`)
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
$$Q_a(X) = X^{5/2}\sum_{n\ge 1}\frac{a(n)}{n^3}e^{-X^2/n^2}, \qquad \bigl|Q_a(X)\bigr| \le \zeta(3)X^{5/2}, \qquad \bigl|R_{a, >T}(X)\bigr| \le \frac{X^{5/2}}{2\lfloor T \rfloor^2} \quad (T \ge 1).$$
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
   - **Square-divisor Möbius convolution $\sum_{d^2 \mid n}\mu(n/d^2) = \lambda(n)$ and exact pole/zero locations (`TASK-TC-055R` §5.3)**: Identifies the Dirichlet series $D_\lambda(s) = \sum_{n\ge 1}\lambda(n)n^{-s} = \frac{\zeta(2s)}{\zeta(s)}$ ($\operatorname{Re} s > 1$). Keeping its pole and zero locations strictly separate:
     - **Simple pole at $s = 1/2$**: Arises from the numerator $\zeta(2s)$ at $2s = 1$ ($s = 1/2$), since $\zeta(1/2) \ne 0$ in the denominator, with residue $\frac{1}{2\zeta(1/2)}$.
     - **Simple zero at $s = 1$**: Arises from the denominator factor $1/\zeta(s)$ at $s = 1$, where $\zeta(s)$ has a simple pole while the numerator $\zeta(2s)$ is analytic and nonzero ($\zeta(2) = \tau^2/24 \ne 0$). Consequently, $D_\lambda(1) = 0$, whereas every finite-prime parity control $a_S(n) = (-1)^{\sum_{p\in S}v_p(n)}$ has $D_{a_S}(s) = \zeta(s)\prod_{p\in S}\frac{1 - p^{-s}}{1 + p^{-s}}$ with a **simple pole at $s = 1$** (residue $\prod_{p\in S}\frac{p-1}{p+1} > 0$; see §7).

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
   with explicit floor-guarded truncation remainder bound for any real $M \ge 1$:
   $$\left|\sum_{\substack{m \in \mathcal{S}(P) \\ m > M}}\frac{\lambda(m)}{\sqrt{m}}\,Q_{\lambda, P}(X/m)\right| \le \zeta(3)X^{5/2}\sum_{m > M}m^{-3} \le \frac{\zeta(3)X^{5/2}}{2\lfloor M \rfloor^2}.$$

All 12 test pairs $(P, X) \in \{(2,), (2,3), (2,3,5)\} \times \{1, 2, \tau, 4\}$ in `section_8_tc055_simultaneous_compatibility_and_joint_identities` (explicitly labeled `"same_observable_operator_vs_series_consistency_check"`) enclose zero in both $Q_{\lambda, P}^{\mathrm{direct}}(X) - Q_{\lambda, P}^{\mathrm{operator}}(X)$ and $Q_\lambda^{\mathrm{direct}}(X) - Q_\lambda^{\mathrm{inverse}}(X)$.

---

## 4. Non-Integer Cutoff Counterexample Repair, Exact Full-Space Operator Norm Obstruction, and Off-Critical Modes (`TASK-TC-055R` §4 & §5.2)

### 4.1 Non-Integer Cutoff Counterexample ($u = 2.9$) and Exact Coprime Decomposition for $P_u = \{p \le u\}$

1. **Counterexample to unguarded $\sum_{n > u} n^{-3} \le \frac{1}{2u^2}$ at non-integer $u = 2.9$ (`TASK-TC-055R` §5.2)**:
   For a non-integer real cutoff $u \ge 1$, the first integer strictly exceeding $u$ is $\lfloor u \rfloor + 1$, so the integral comparison compares against $\int_{\lfloor u \rfloor}^\infty t^{-3}\,dt = \frac{1}{2\lfloor u \rfloor^2}$, **not** $\frac{1}{2u^2}$. At $u = 2.9$ ($\lfloor u \rfloor = 2$),
   $$\sum_{n > 2.9} n^{-3} = \sum_{n \ge 3} n^{-3} = \zeta(3) - 1 - \frac{1}{8} \in \bigl[0.07705690315959428539973816151144999076499 \pm 3.71 \times 10^{-42}\bigr],$$
   (indeed, the first three terms $3^{-3} + 4^{-3} + 5^{-3} = \frac{1}{27} + \frac{1}{64} + \frac{1}{125} \in [0.06066203703703703703703703703703703703704 \pm 2.97 \times 10^{-42}]$ already exceed $\frac{50}{841}$), which **strictly exceeds** the unguarded value
   $$\frac{1}{2(2.9)^2} = \frac{50}{841} \in \bigl[0.05945303210463733650416171224732461355529 \pm 1.32 \times 10^{-42}\bigr],$$
   while satisfying the repaired floor-guarded bound $\frac{1}{2\lfloor 2.9 \rfloor^2} = \frac{1}{8} = 0.125$.
2. **Repaired general and coprime tail bounds across integer and non-integer cutoffs**:
   - **General tail ($u \ge 1$ real)**: Since $\lfloor u \rfloor \ge 1$ and $n \ge \lfloor u \rfloor + 1 \implies n^{-3} \le \int_{n-1}^n t^{-3}\,dt$,
     $$\boxed{\sum_{n > u}\frac{1}{n^3} = \sum_{n \ge \lfloor u \rfloor + 1}\frac{1}{n^3} \le \int_{\lfloor u \rfloor}^\infty t^{-3}\,dt = \frac{1}{2\lfloor u \rfloor^2} \qquad (\forall u \ge 1).}$$
   - **Coprime tail ($u \ge 2$ real, $P_u = \{p \le u\}$, $N_u = \prod_{p \le u}p$)**: The smallest integer $n \ge 2$ coprime to $N_u$ is the least prime $q_{>u} > u$. Since $q_{>u}$ is an integer strictly exceeding $u$, we have $q_{>u} \ge \lfloor u \rfloor + 1 > u$, and hence $q_{>u} - 1 \ge \lfloor u \rfloor$. Moreover, for $u \ge 2$, the least prime $q_{>u} \ge 3$ satisfies $q_{>u} - 1 \ge u$ whenever $u \notin (q_{>u}-1, q_{>u})$, and unconditionally:
     $$\boxed{Q_{\lambda, P_u}(w) = w^{5/2}e^{-w^2} + R_{\lambda, P_u}(w), \qquad \bigl|R_{\lambda, P_u}(w)\bigr| \le w^{5/2}\sum_{n \ge q_{>u}}\frac{1}{n^3} \le \frac{w^{5/2}}{2(q_{>u} - 1)^2} \le \frac{w^{5/2}}{2\lfloor u \rfloor^2}.}$$
   *(Certified in 256-bit Arb across both sides of integer boundaries $u \in \{2.9, 3.0, 3.1, 4.9, 5.0, 5.1, 7.0, 11.0, 13.0\}$ and $w \in \{1, 2, 4\}$ in `section_9_tc055_coupled_cutoff_and_norm_obstruction`.)*
3. **Signed grade-interval energy expansion**:
   Expanding $Q_{\lambda, P_u}(X) = \sum_{d \mid N_u}\frac{|\mu(d)|}{\sqrt{d}}Q_\lambda(X/d)$ and integrating $|Q_{\lambda, P_u}(X)|^2\,\frac{dX}{X}$ over $[Y, \tau Y]$ gives the exact multi-scale energy relation retaining all diagonal ($d_1 = d_2$) and cross-scale ($d_1 \ne d_2$) terms:
   $$E_{\lambda, P_u}(Y) := \int_Y^{\tau Y}\bigl|Q_{\lambda, P_u}(X)\bigr|^2\,\frac{dX}{X} = \sum_{d \mid N_u}\frac{|\mu(d)|}{d}\,E_\lambda(Y/d) + 2\sum_{\substack{d_1, d_2 \mid N_u \\ d_1 < d_2}}\frac{|\mu(d_1)||\mu(d_2)|}{\sqrt{d_1 d_2}}\int_Y^{\tau Y}Q_\lambda(X/d_1)Q_\lambda(X/d_2)\,\frac{dX}{X}.$$

### 4.2 Exact Full-Space Operator Norm Obstruction on $\mathcal{H}_\eta$ (`TASK-TC-055R` §4)

**Theorem 4.1 (Exact Full-Space Operator Norm of the Inverse Prime-Exclusion Filter $\mathcal{P}_u^{-1}$).**
On the weighted Hilbert space $\mathcal{H}_\eta = L^2((0, \infty), X^{-2\eta}\,dX/X)$ ($\eta > 0$), for every finite prime cutoff $u \ge 2$, the inverse prime-exclusion operator $\mathcal{P}_u^{-1} = \prod_{p \le u}(I + p^{-1/2}S_p)^{-1}$ has **exact** operator norm equal to the unsigned Neumann product:
$$\boxed{\bigl\|\mathcal{P}_u^{-1}\bigr\|_{\mathcal{H}_\eta \to \mathcal{H}_\eta} = \sup_{b \in \mathbb{R}}\prod_{p \le u}\bigl|1 + p^{-1/2 - \eta}e^{-i b\log p}\bigr|^{-1} = \prod_{p \le u}\bigl(1 - p^{-1/2 - \eta}\bigr)^{-1}.}$$

*Proof.*
1. **Unitary logarithmic coordinate and Fourier–Plancherel multiplier isomorphism**:
   Define $U_\eta : \mathcal{H}_\eta \to L^2(\mathbb{R}, dt)$ by $(U_\eta F)(t) := e^{-\eta t}F(e^t)$. Then
   $$\|U_\eta F\|_{L^2(\mathbb{R})}^2 = \int_{-\infty}^\infty e^{-2\eta t}\bigl|F(e^t)\bigr|^2\,dt = \int_0^\infty \bigl|F(X)\bigr|^2 X^{-2\eta}\,\frac{dX}{X} = \|F\|_\eta^2,$$
   so $U_\eta$ is unitary, and $U_\eta S_p U_\eta^{-1}g(t) = e^{-\eta t}(U_\eta^{-1}g)(e^{t - \log p}) = p^{-\eta}g(t - \log p)$ is translation by $\log p$ scaled by $p^{-\eta}$. Under the unitary Fourier–Plancherel transform $\mathcal{F} : L^2(\mathbb{R}, dt) \to L^2(\mathbb{R}, \frac{db}{\tau})$, $\mathcal{F}(g(\cdot - \log p))(b) = e^{-i b\log p}\mathcal{F}[g](b)$. Hence $\mathcal{P}_u^{-1}$ is unitarily equivalent to multiplication on $L^2(\mathbb{R}, \frac{db}{\tau})$ by
   $$m_{u, \eta}(b) := \prod_{p \le u}\bigl(1 + p^{-1/2 - \eta}e^{-i b\log p}\bigr)^{-1}.$$
2. **Continuity of $m_{u,\eta}$ ($\operatorname*{ess\,sup} = \sup$) and upper bound**:
   For every $\eta > 0$, each factor satisfies $|1 + p^{-1/2-\eta}e^{-ib\log p}| \ge 1 - p^{-1/2-\eta} > 0$ by the reverse triangle inequality. Thus $m_{u,\eta} : \mathbb{R} \to \mathbb{C}$ is bounded and continuous on $\mathbb{R}$, so its $L^\infty(\mathbb{R})$ essential supremum equals its pointwise supremum:
   $$\bigl\|\mathcal{P}_u^{-1}\bigr\|_{\mathcal{H}_\eta \to \mathcal{H}_\eta} = \|m_{u, \eta}\|_{L^\infty(\mathbb{R})} = \sup_{b \in \mathbb{R}}\bigl|m_{u, \eta}(b)\bigr| \le \prod_{p \le u}\bigl(1 - p^{-1/2 - \eta}\bigr)^{-1}.$$
3. **Lower bound via $\mathbb{Q}$-linear independence of $\{\log p : p \le u\}$ and continuous Kronecker simultaneous approximation**:
   By the fundamental theorem of arithmetic (unique prime factorization in $\mathbb{Z}_{\ge 1}$), the real numbers $\{\log p : p \le u\}$ are linearly independent over $\mathbb{Q}$: if $\sum_{p \le u} c_p \log p = 0$ with $c_p \in \mathbb{Z}$, then $\prod_{p \le u} p^{c_p} = 1$, forcing $c_p = 0$ for all $p \le u$. By the continuous form of Kronecker's simultaneous approximation theorem (see e.g. T. Aoyama and T. Nakamura, *A generalization of carries processes and Euler products*, `arXiv:1204.4043`, p. 9; Hardy & Wright, *An Introduction to the Theory of Numbers*, Theorem 444), the flow $b \mapsto (b\log p \bmod \tau)_{p \le u}$ has dense image in the torus $(\mathbb{R}/\tau\mathbb{Z})^{\pi(u)}$. In particular, the target phase tuple $(\tau/2, \dots, \tau/2) \in (\mathbb{R}/\tau\mathbb{Z})^{\pi(u)}$ where $e^{-ib\log p} = -1$ simultaneously for all $p \le u$ lies in the closure of the trajectory: for every $\delta > 0$, there exists $b_\delta \in \mathbb{R}$ such that $|e^{-ib_\delta \log p} - (-1)| < \delta$ for all $p \le u$. Letting $\delta \to 0^+$ yields
   $$\sup_{b \in \mathbb{R}}\bigl|m_{u, \eta}(b)\bigr| \ge \prod_{p \le u}\bigl(1 - p^{-1/2 - \eta}\bigr)^{-1},$$
   establishing the exact equality. $\blacksquare$

> **Consequence (`TASK-TC-055R` §4)**: Because $\|\mathcal{P}_u^{-1}\|_{\mathcal{H}_\eta \to \mathcal{H}_\eta} = \prod_{p \le u}(1 - p^{-1/2-\eta})^{-1}$ is an **exact operator-norm identity** on the full weighted space $\mathcal{H}_\eta$ (certified at $u = 5, \eta = 1/4$ where $b_* = \frac{2513\tau}{2\log 2} \in [11389.82103641173804359436724258598369396 \pm 1.89 \times 10^{-36}]$ attains $99.912\%$ of the exact supremum $[6.264139038011680689993761243736081380159 \pm 3.91 \times 10^{-41}]$ vs. $[6.269653257665089643352758026278521806500 \pm 4.85 \times 10^{-40}]$), **no "signed improvement" of the full-space operator norm $\|\mathcal{P}_u^{-1}\|_{\mathcal{H}_\eta \to \mathcal{H}_\eta}$ exists**. Any cancellation below the unsigned product must restrict to the specific arithmetic observable $Q_\lambda$ (via $\mathcal{M}[Q_\lambda](\eta + ib)$ or the finite truncated observable $Q_{\lambda, T}(X)$ in §8), never via a universal operator norm on $\mathcal{H}_\eta$.

### 4.3 Off-Critical Mode Multiplier Bounds

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

### 5.3 Unconditional Near-Diagonal Band Inequality for Every $H \ge 0$

**Proposition 5.2 (Near-Diagonal Band Bound).**
For all $m, n \ge 1$ and $Y > 0$, $2 K_Y(m, n) \le K_Y(m, m) + K_Y(n, n)$, and for every integer $H \ge 0$:
$$\boxed{\left|\sum_{|m - n| \le H}\lambda(m)\lambda(n)K_Y(m, n)\right| \le \sum_{|m - n| \le H} K_Y(m, n) \le (2H + 1)D_E(Y).}$$
*(Algebraic core formalized in Lean 4 theorem `near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing` and certified in 256-bit Arb across $Y \in \{1, 2, 4\}$ and $H \in \{0, 1, 2, 4\}$.)*

> **Consequence for `SUBGATE-TC-043A`**: For any bandwidth $H = O(Y^\varepsilon)$, the entire diagonal and near-diagonal band $|m - n| \le H$ contributes at most $(2H + 1)D_E(Y) = O(Y^\varepsilon)$. Therefore, any violation of $E_\lambda(Y) \ll_\varepsilon Y^\varepsilon$ must arise exclusively from the **wide off-diagonal transition correlations** $|m - n| > H$ with $m, n \asymp Y$.

---

## 6. Counterexample to Retired Uniform Pairing Bound, Valid Replacement Theorems, and Unmatched Mass Separation (`TASK-TC-055R` §2, §3 & §5.3)

### 6.1 Reproduction and Retirement of False Uniform Pairing Bound (`TC-055` Lemma 6.1)

In the initial `TC-055` draft, Lemma 6.1 claimed that for all $Y > 0$, $p$ prime, $q r$ semiprime, and $m, n \ge 1$,
$$\bigl|K_Y(p m, n) - K_Y(q r m, n)\bigr| \stackrel{?}{\le} 3\,\frac{|q r - p|}{u_{\min}}\left(\frac{u_{\max}}{u_{\min}}\right)^3 K_Y(u_{\max} m, n), \qquad u_{\min} = \min(p, q r), \quad u_{\max} = \max(p, q r).$$

1. **Algebraic flaw in the original proof**:
   For $g_X(u) = u^{-3}e^{-X^2/u^2}$, the derivative is $g_X'(u) = u^{-4}(2 w^2 - 3)e^{-w^2}$ where $w = X/u$. The original draft used $\sup_{w > 0}|(2w^2 - 3)e^{-w^2}| = 3$ **and simultaneously** retained the Gaussian factor $e^{-X^2/u_2^2}$. However, bounding $|(2w^2 - 3)e^{-w^2}| \le 3$ **consumes** the exponential factor $e^{-w^2} = e^{-X^2/u^2}$! To retain $e^{-X^2/u_2^2}$ on $u \in [a, b]$ ($0 < a \le b$), one must bound $|2X^2/u^2 - 3|$ without consuming $e^{-X^2/u^2}$, which grows like $2X^2/a^2 + 3 \le 3 + 2\tau^2 Y^2/a^2$ when $Y/a$ is large.
2. **Certified 256-Bit Arb Counterexample at $Y = 33, p = 11, q = 2, r = 5, m = 1, n = 11$ ($q r = 10, u_{\min} = 10, u_{\max} = 11$)**:
   - Claimed normalized upper bound:
     $$3\,\frac{|10 - 11|}{10}\left(\frac{11}{10}\right)^3 = \frac{3 \times 1331}{10000} = \frac{3993}{10000} = 0.3993.$$
   - Certified 256-bit Arb evaluations:
     - $K_{33}(11, 11) \in [1.592023309024998299449474636863506932593 \times 10^{-8} \pm 3.21 \times 10^{-49}]$,
     - $K_{33}(10, 11) \in [2.874791627804215660779585852580865752679 \times 10^{-9} \pm 4.35 \times 10^{-50}]$,
     - $\bigl|K_{33}(11, 11) - K_{33}(10, 11)\bigr| \in [1.304544146244576733371516051605420357325 \times 10^{-8} \pm 2.66 \times 10^{-49}]$,
     - Normalized difference:
       $$\frac{\bigl|K_{33}(11, 11) - K_{33}(10, 11)\bigr|}{K_{33}(11, 11)} \in \bigl[0.8194252817117595423362805867661925634141 \pm 4.15 \times 10^{-41}\bigr] > 0.3993.$$
3. **Elementary Floating-Point-Free Proof of the Contradiction**:
   For every $X \in [33, 33\tau]$, $X^2 \ge 33^2 = 1089$, so
   $$X^2\left(\frac{1}{10^2} - \frac{1}{11^2}\right) = X^2 \cdot \frac{21}{12100} \ge \frac{1089 \times 21}{12100} = \frac{9 \times 21}{100} = \frac{189}{100}.$$
   Pointwise on $X \in [33, 33\tau]$, the ratio of the integrands of $K_{33}(10, 11)$ and $K_{33}(11, 11)$ satisfies
   $$\frac{10^{-3}e^{-X^2/10^2}}{11^{-3}e^{-X^2/11^2}} = \frac{1331}{1000}\,e^{-X^2(10^{-2} - 11^{-2})} \le \frac{1331}{1000}\,e^{-189/100}.$$
   Since $e^{189/100} > 1 + \frac{189}{100} = \frac{289}{100}$, we have $e^{-189/100} < \frac{100}{289}$, and integrating against the positive weight $X^4 \cdot 11^{-3}e^{-X^2/11^2}\,dX$ over $[33, 33\tau]$ gives
   $$\frac{K_{33}(10, 11)}{K_{33}(11, 11)} \le \frac{1331}{1000}\,e^{-189/100} < \frac{1331}{1000}\cdot\frac{100}{289} = \frac{1331}{2890}.$$
   Therefore,
   $$\frac{\bigl|K_{33}(11, 11) - K_{33}(10, 11)\bigr|}{K_{33}(11, 11)} > 1 - \frac{1331}{2890} = \frac{1559}{2890} = 0.53944636678\ldots > \frac{3993}{10000} = 0.3993,$$
   since $1559 \times 10000 = 15590000 > 11539770 = 3993 \times 2890$. *(Verified by `norm_num` in Lean 4 theorem `pairing_counterexample_replacement_and_finite_reconstruction_tc055r`.)*

Accordingly, the false uniform pairing inequality is **retired** from all repository theorems, while the exact arithmetic parity identity $\lambda(p m) + \lambda(q r m) = 0$ is preserved.

### 6.2 Proved Replacement Bounds and Their Useful Regimes (`TASK-TC-055R` §3)

**Theorem 6.1 (Two-Sided Integrand-Ratio Enclosure and Transition Relative-Gap Bound).**
Let $0 < a \le b$ be positive integers (e.g. $a = \min(p, q r)m$ and $b = \max(p, q r)m$), let $n \ge 1$, and let $Y > 0$. Define $r_0 := b/a \ge 1$ and $\Delta := a^{-2} - b^{-2} \ge 0$.
1. **Two-Sided Integrand-Ratio Enclosure (Valid for all $Y > 0$ and all $0 < a \le b$)**:
   $$\boxed{r_0^3 e^{-(\tau Y)^2 \Delta} K_Y(b, n) \le K_Y(a, n) \le r_0^3 e^{-Y^2 \Delta} K_Y(b, n),}$$
   and consequently
   $$\boxed{\bigl|K_Y(a, n) - K_Y(b, n)\bigr| \le \max\!\Bigl(\bigl|r_0^3 e^{-(\tau Y)^2 \Delta} - 1\bigr|,\;\bigl|r_0^3 e^{-Y^2 \Delta} - 1\bigr|\Bigr) K_Y(b, n).}$$
2. **Transition-Regime Relative-Gap Bound (Valid for all $Y > 0$ and $0 < a \le b$, with $O((b-a)/a)$ saving when $a \ge c Y$)**:
   $$\boxed{\bigl|K_Y(a, n) - K_Y(b, n)\bigr| \le \frac{b - a}{a}\left(\frac{b}{a}\right)^3\left(3 + \frac{2\tau^2 Y^2}{a^2}\right) K_Y(b, n).}$$
   In particular, in the transition/super-transition regime $a \ge c Y$ ($c > 0$), the factor $3 + \frac{2\tau^2 Y^2}{a^2} \le 3 + \frac{2\tau^2}{c^2}$ is uniformly bounded and yields an $O((b-a)/a)$ relative saving.

*Proof.*
1. For every $X \in [Y, \tau Y]$, $Y^2\Delta \le X^2(a^{-2} - b^{-2}) \le (\tau Y)^2\Delta$, so
   $$a^{-3}e^{-X^2/a^2} = r_0^3 b^{-3}e^{-X^2/b^2}e^{-X^2\Delta} \in \Bigl[r_0^3 e^{-(\tau Y)^2\Delta} b^{-3}e^{-X^2/b^2},\; r_0^3 e^{-Y^2\Delta} b^{-3}e^{-X^2/b^2}\Bigr].$$
   Multiplying by the positive weight $X^4 n^{-3}e^{-X^2/n^2}$ and integrating over $X \in [Y, \tau Y]$ yields part (1).
2. For fixed $X \in [Y, \tau Y]$ and $u \in [a, b]$, $g_X(u) = u^{-3}e^{-X^2/u^2}$ has derivative
   $$\bigl|g_X'(u)\bigr| = u^{-4}\left|\frac{2X^2}{u^2} - 3\right|e^{-X^2/u^2} \le a^{-4}\left(3 + \frac{2\tau^2 Y^2}{a^2}\right)e^{-X^2/b^2} = \frac{1}{a}\left(\frac{b}{a}\right)^3\left(3 + \frac{2\tau^2 Y^2}{a^2}\right) b^{-3}e^{-X^2/b^2},$$
   because $u \ge a \implies u^{-4} \le a^{-4}$ and $|2X^2/u^2 - 3| \le 3 + 2X^2/a^2 \le 3 + 2\tau^2 Y^2/a^2$, while $u \le b \implies e^{-X^2/u^2} \le e^{-X^2/b^2}$ without consuming the Gaussian factor. Integrating over $u \in [a, b]$ and then against $X^4 n^{-3}e^{-X^2/n^2}\,dX$ on $[Y, \tau Y]$ proves part (2). *(Algebraic core formalized in Lean 4 theorem `pairing_counterexample_replacement_and_finite_reconstruction_tc055r` and certified in 256-bit Arb across all 5 regimes in `section_11_tc055_opposite_parity_dilation_pairing`: comparable scales, large $Y/a$ at $(33, 10, 11, 11)$, unequal indices $m > 1$, tiny consecutive gaps, and zero gap $a = b$.)* $\blacksquare$

### 6.3 Separation of Fixed Finite Factor Set vs. Growing Cutoff Unmatched Mass (`TASK-TC-055R` §5.3)

When diagnosing the unmatched residual under opposite-parity pairing, the two cutoff regimes must be kept strictly separate:
1. **Regime A — Fixed finite factor set $P_1 \cup P_2$ ($u$ independent of $Y$)**:
   Let $N_{\mathrm{pair}} = \operatorname{lcm}(P_1 \cup P_2)$ be fixed. The integers $k \ge 1$ coprime to $N_{\mathrm{pair}}$ have strictly positive natural density $\prod_{p \mid N_{\mathrm{pair}}}(1 - 1/p) > 0$ (e.g. `101 / 240` for $P_1 = \{5, 7, 11\}, P_2 = \{4, 6, 10\}$), so the unmatched coprime transition integers $k \in [Y, \tau Y]$ contribute unsigned energy of order $Y$.
2. **Regime B — Growing factor cutoff $u = Y^\theta$ ($\theta \in (0, 1)$)**:
   If all primes $p \le Y^\theta$ are included, the integers $k \in [Y, \tau Y]$ having no prime factor $\le Y^\theta$ are the $Y^\theta$-rough numbers (density $\asymp 1/(\theta \log Y)$ by Buchstab's identity). In particular, the unmatched primes $p \in [Y, \tau Y]$ alone have count $\pi(\tau Y) - \pi(Y) \asymp Y/\log Y$; since each prime $p \in [Y, \tau Y]$ has $\lambda(p) = -1$ (coherent negative sign!), their prime-prime contribution to $Q_\lambda(X)$ has magnitude $\asymp \frac{\sqrt{Y}}{\log Y}$ and **prime-prime energy scale $\asymp \frac{Y}{(\log Y)^2}$** (rather than order $Y$, which comes from the composite $Y^\theta$-rough integers and the $Y^\theta$-smooth Dickman bulk).

---

## 7. Multiplicative Parity Controls $a_2(n) = (-1)^{v_2(n)}$ and $a_S(n)$ (`TASK-TC-055R` §5.1)

For any finite set of primes $S \subset \mathbb{P}$, define the completely multiplicative parity control
$$a_S(n) := (-1)^{\sum_{p \in S} v_p(n)}, \qquad a_2(n) := a_{\{2\}}(n) = (-1)^{v_2(n)}.$$

### 7.1 Repaired Unimodal Constant and Second-Order Euler–Maclaurin Proof for $Q_{a_2}(X)$ and $E_{a_2}(Y)$

1. **Correction of the unimodal constant (`TASK-TC-055R` §5.1)**:
   For $h_X(t) = t^{-3}e^{-X^2/t^2}$, the maximum occurs at $t_* = X\sqrt{2/3}$ with value $h_X(t_*) = (\frac{3}{2e})^{3/2}X^{-3}$. Therefore, the unimodal sum-integral bound $|Q_{\mathbf{1}}(X) - \frac{1}{2}\sqrt{X}| \le 2 X^{5/2} h_X(t_*)$ has exact constant
   $$\boxed{C_{1,\mathrm{uni}} := 2\left(\frac{3}{2e}\right)^{3/2} = \frac{1}{\sqrt{2}}\left(\frac{3}{e}\right)^{3/2} \in \bigl[0.8198325578837200767815820207595078237088 \pm 2.50 \times 10^{-41}\bigr],}$$
   which is **strictly smaller** than $\left(\frac{3}{e}\right)^{3/2} \in [1.159418322234182419789034443434222535151 \pm 3.86 \times 10^{-40}]$ by the factor $\frac{1}{\sqrt{2}}$ (retiring the false algebraic simplification in the `TC-055` draft).
2. **First-order unimodal dyadic sum vs. second-order Euler–Maclaurin dyadic sum**:
   - **Using the first-order unimodal bound $|Q_{\mathbf{1}}(w) - \frac{1}{2}\sqrt{w}| \le C_{1,\mathrm{uni}}w^{-1/2}$**: In $Q_{a_2}(X) = Q_{\mathbf{1}}(X) + 2\sum_{k\ge 1}(-1)^k 2^{-k/2}Q_{\mathbf{1}}(X/2^k)$, each dyadic scale $2^k \le X$ contributes an error bounded by $2 \cdot 2^{-k/2} C_{1,\mathrm{uni}}(X/2^k)^{-1/2} = 2 C_{1,\mathrm{uni}} X^{-1/2}$. Summing over the $\lfloor \log_2 X \rfloor$ scales $2^k \le X$ yields
     $$Q_{a_2}(X) = \frac{\sqrt{X}}{6} + O\bigl(X^{-1/2}\log X\bigr), \qquad E_{a_2}(Y) = \frac{\tau - 1}{36}\,Y + O(\log Y).$$
   - **Recovering $O(X^{-1/2})$ and $O(1)$ via second-order Euler–Maclaurin**:
     Since $h_w(0^+) = h_w'(0^+) = 0$ and $\frac{1}{12}\int_0^\infty |h_w''(t)|\,dt \le 3 w^{-4}$, second-order periodic Bernoulli Euler–Maclaurin gives the global bound
     $$\boxed{\left|Q_{\mathbf{1}}(w) - \frac{\sqrt{w}}{2}\right| \le 3\,w^{-3/2} \qquad (\forall w > 0).}$$
     Splitting $(I + 2^{-1/2}S_2)^{-1}(Q_{\mathbf{1}}(X) - 2^{-1/2}Q_{\mathbf{1}}(X/2))$ at $K_X = \lfloor \log_2 X \rfloor$ ($X \ge 1$) bounds the large-scale sum ($1 \le k \le K_X$) by $6\sqrt{2}X^{-1/2}$, the omitted main-term tail ($k > K_X$) by $\sqrt{2}X^{-1/2}$, and the small-scale tail ($k > K_X$) by $\frac{8\sqrt{2}\zeta(3)}{7}X^{-1/2}$, yielding the certified universal bound $\bigl|Q_{a_2}(X) - \frac{\sqrt{X}}{6}\bigr| \le C_{a_2}\,X^{-1/2}$ for all $X \ge 1$ with $C_{a_2} = 3 + 7\sqrt{2} + \frac{8\sqrt{2}}{7}\zeta(3) \in [14.84231227968880861907095700769835025024 \pm 4.79 \times 10^{-39}]$, which unconditionally recovers:
     $$\boxed{Q_{a_2}(X) = \frac{\sqrt{X}}{6} + O\bigl(X^{-1/2}\bigr), \qquad E_{a_2}(Y) = \frac{\tau - 1}{36}\,Y + O(1).}$$

### 7.2 Multi-Prime Parity Control $S = \{3, 5, 7\}$ (`TASK-TC-055R` §5.1)

For $S = \{3, 5, 7\}$, the Euler-factor mean of $a_{\{3,5,7\}}(n) = (-1)^{v_3(n)+v_5(n)+v_7(n)}$ is
$$\prod_{p \in \{3, 5, 7\}}\frac{p - 1}{p + 1} = \frac{2}{4}\cdot\frac{4}{6}\cdot\frac{6}{8} = \frac{1}{4}$$
(and **not** $\frac{1}{3}$, which is the mean $\frac{2-1}{2+1} = \frac{1}{3}$ for $S = \{2\}$). Multiplying by $\int_0^\infty t^{-3}e^{-1/t^2}\,dt = \frac{1}{2}$ yields the certified asymptotics:
$$\boxed{Q_{a_{\{3,5,7\}}}(X) = \frac{1}{8}\sqrt{X} + O\bigl(X^{-1/2}\bigr) \sim \frac{1}{8}\sqrt{X}, \qquad E_{a_{\{3,5,7\}}}(Y) = \frac{\tau - 1}{64}\,Y + O(1) \sim \frac{\tau - 1}{64}\,Y,}$$
where $\frac{\tau - 1}{64} \in [0.08254977042468103870195760572748446513115 \pm 5.29 \times 10^{-42}]$ (certified at $X = 64$, where $Q_{a_{\{3,5,7\}}}(64)/\sqrt{64} \in [0.125731 \pm 8.45 \times 10^{-4}] \approx \frac{1}{8} = 0.125$).

---

## 8. Noncircular Finite Arithmetic Proof Attempt via $T$-Truncated Observable $Q_{\lambda, T}(X)$ (`TASK-TC-055R` §6 & §7)

### 8.1 Exact Finite $T$-Truncation $P$-Smooth Reconstruction with $m$-Dependent Inner Cutoff

For any finite truncation $T \ge 1$ and any finite prime set $P \subset \mathbb{P}$ ($N_P = \prod_{p\in P}p$), define the finite observables
$$Q_{\lambda, T}(X) := X^{5/2}\sum_{1 \le n \le T}\frac{\lambda(n)}{n^3}e^{-X^2/n^2}, \qquad Q_{\lambda, P, L}(w) := w^{5/2}\sum_{\substack{1 \le r \le L \\ \gcd(r, N_P)=1}}\frac{\lambda(r)}{r^3}e^{-w^2/r^2}.$$

**Theorem 8.1 (Exact Finite $T$-Truncation Reconstruction and Tail Energy Transfer).**
1. **Exact $m$-dependent inner cutoff identity**: Every integer $1 \le n \le T$ factors uniquely as $n = m r$ with $m \in \mathcal{S}(P)$, $\gcd(r, N_P) = 1$, $1 \le m \le T$, and $1 \le r \le \lfloor T/m \rfloor$. Consequently, for all $X > 0$ and $T \ge 1$:
   $$\boxed{Q_{\lambda, T}(X) = \sum_{\substack{m \in \mathcal{S}(P) \\ m \le T}}\frac{\lambda(m)}{\sqrt{m}}\,Q_{\lambda, P, \lfloor T/m \rfloor}(X/m).}$$
   *(Note: Using an uncoupled inner cutoff $r \le T$ instead of $r \le \lfloor T/m \rfloor$ includes spurious products $n = m r \in (T, T^2]$ and strictly fails to equal $Q_{\lambda, T}(X)$; verified in `section_13_tc055r_finite_truncation_and_signed_energy_attempt` and formalized in Lean 4 theorem `pairing_counterexample_replacement_and_finite_reconstruction_tc055r`.)*
2. **Truncation tail energy bound and $T(Y) = \lceil Y^{5/4} \rceil$ scale**: For all $Y > 0$ and integer $T \ge 1$, since $|Q_\lambda(X) - Q_{\lambda, T}(X)| \le \frac{X^{5/2}}{2T^2}$,
   $$\boxed{\mathcal{R}_{\mathrm{tail}}(Y, T) := \int_Y^{\tau Y}\bigl|Q_\lambda(X) - Q_{\lambda, T}(X)\bigr|^2\,\frac{dX}{X} \le \frac{1}{4T^4}\int_Y^{\tau Y} X^4\,dX = \frac{(\tau^5 - 1)Y^5}{20\,T^4},}$$
   and by $\|f + g\|_{L^2}^2 \le 2\|f\|_{L^2}^2 + 2\|g\|_{L^2}^2$,
   $$\boxed{E_\lambda(Y) \le 2 E_{\lambda, T}(Y) + 2\mathcal{R}_{\mathrm{tail}}(Y, T) \le 2 E_{\lambda, T}(Y) + \frac{(\tau^5 - 1)Y^5}{10\,T^4}.}$$
   Choosing $T(Y) := \lceil Y^{5/4} \rceil$ makes $\mathcal{R}_{\mathrm{tail}}(Y, T(Y)) \le \frac{\tau^5 - 1}{20} \in [489.5814956564503252203860960694969703685 \pm 1.89 \times 10^{-38}] = O(1)$, reducing `SUBGATE-TC-043A` strictly to the **finite** double sum
   $$E_{\lambda, T(Y)}(Y) = \sum_{1 \le m, n \le T(Y)}\lambda(m)\lambda(n)K_Y(m, n).$$

### 8.2 Noncircular Signed Energy Decomposition of $E_{\lambda, T}(Y)$ and Exact Obstruction

Factoring each $1 \le n \le T(Y)$ uniquely as $n = m_n r_n$ with $m_n \in \mathcal{S}(P_u)$ and $\gcd(r_n, N_u) = 1$ ($r_n \le \lfloor T(Y)/m_n \rfloor$) decomposes the finite quadratic form $E_{\lambda, T}(Y)$ simultaneously by $P_u$-coprime cofactor ($r_1 = r_2$ vs. $r_1 \ne r_2$) and by $P_u$-smooth factor ($m_1 = m_2$ vs. $m_1 \ne m_2$):
$$\boxed{E_{\lambda, T}(Y) = E_{\mathrm{same}\text{-}r}(Y; T, P_u) + E_{\mathrm{diff}\text{-}r}(Y; T, P_u) = E_{\mathrm{smooth}\text{-}\mathrm{diag}}(Y; T, P_u) + E_{\mathrm{smooth}\text{-}\mathrm{cross}}(Y; T, P_u),}$$
where $E_{\mathrm{same}\text{-}r}(Y; T, P_u) = \sum_{\substack{1 \le r \le T \\ \gcd(r, N_u)=1}}\int_Y^{\tau Y}\bigl|Q_{\lambda, \mathcal{S}(P_u), \lfloor T/r \rfloor}(X/r)\bigr|^2\,\frac{dX}{X} \ge 0$ is a sum of squared pure $P_u$-smooth signed sums.

| $Y$ | $T(Y) = \lceil Y^{5/4} \rceil$ | $P_u$ | Signed $E_{\lambda, T(Y)}(Y)$ (256-Bit Arb) | Unsigned $E_{\mathrm{unsigned}, T(Y)}(Y)$ (256-Bit Arb) | $E_{\mathrm{same}\text{-}r}$ | $E_{\mathrm{diff}\text{-}r}$ | Ratio $E_{\lambda, T} / E_{\mathrm{unsigned}, T}$ |
| :---: | :---: | :---: | :--- | :--- | :---: | :---: | :---: |
| `4` | `6` | `{2, 3}` | `[0.004608633312722755964394753036415613296616 +/- 3.52e-43]` | `[0.2229338930925055337199205455198700527881 +/- 3.12e-42]` | `0.0487893` | `-0.0441806` | `0.0206726` |
| `8` | `14` | `{2, 3, 5}` | `[0.01628064423617857591478454843047804761284 +/- 2.05e-42]` | `[0.6133315943098280111202482635113438651676 +/- 2.45e-41]` | `0.0253668` | `-0.0090861` | `0.0265446` |
| `12` | `23` | `{2, 3, 5, 7}` | `[0.02008761677818477787815712162881096441858 +/- 2.74e-42]` | `[1.130968271229071832411352715272616235617 +/- 4.51e-40]` | `0.0460440` | `-0.0259564` | `0.0177614` |

**Diagnosis of the finite signed energy attempt**:
- Empirically on $(Y, T) \in \{(4, 6), (8, 14), (12, 23)\}$, the signed finite energy $E_{\lambda, T(Y)}(Y)$ is strictly smaller than the unsigned energy $E_{\mathrm{unsigned}, T(Y)}(Y)$ (cancellation ratio $1.78\% \text{--} 2.65\%$).
- Analytically, for any fixed finite prime set $P_u$, each pure $P_u$-smooth Dirichlet series $D_{\mathcal{S}(P_u)}(s) = \prod_{p \le u}(1 + p^{-s})^{-1}$ is holomorphic on $\operatorname{Re} s > 0$, giving a fixed-$u$ power saving $O_{u,\eta}(w^\eta)$ on individual untruncated smooth fibers. However, promoting this to an unconditional bound $E_{\lambda, T(Y)}(Y) \ll_\varepsilon Y^\varepsilon$ faces a two-part obstruction:
  1. For large $u \ge T(Y)$ (where $\gcd(r, N_u) = 1 \implies r = 1$ and $E_{\mathrm{diff}\text{-}r} = 0$), the finite Euler product on $\operatorname{Re}(1/2+z) = \eta \in (0, 1/2)$ has exact Kronecker supremum $\prod_{p \le u}(1 - p^{-\eta})^{-1} = \exp((1+o(1))\frac{u^{1-\eta}}{(1-\eta)\log u})$, which grows super-polynomially in $Y$, while the inner cutoff $\lfloor T/m \rfloor$ couples the Mellin transform to the hyperbolic boundary sum.
  2. For small $u(Y) \ll (\log Y)^{1/(1-\eta)}$ (where $\prod_{p \le u}(1 - p^{-\eta})^{-1} \le Y^\varepsilon$), almost all integers $n \le T(Y)$ have large $P_u$-coprime cofactors $r > u$, leaving the unfactored primes $p > u$ inside the off-diagonal coprime cofactor sum $E_{\mathrm{diff}\text{-}r}(Y; T(Y), P_u)$.

---

## 9. Summary of Verified Unconditional Results vs. Open Obstruction

1. **Surviving & Newly Proved Unconditional Results (`TASK-TC-055` & `TASK-TC-055R`)**:
   - **Removable trivial-zero cancellation**: $\lim_{z\to -(2m+1/2)}\frac{\zeta(1+2z)}{\zeta(1/2+z)} = \frac{2\zeta'(-4m)}{\zeta'(-2m)} \ne 0$, and $D_\lambda(s) = \zeta(2s)/\zeta(s)$ has a simple pole at $s = 1/2$ and a simple zero at $s = 1$.
   - **Finite-prime exclusion and floor-guarded coprime tail bounds**: Theorem 3.1 (`actual_finite_prime_exclusion_sieve_identity_nat`), plus the $u = 2.9$ counterexample and repaired bounds $\sum_{n > u}n^{-3} \le \frac{1}{2\lfloor u \rfloor^2}$ ($u \ge 1$) and $|R_{\lambda, P_u}(w)| \le \frac{w^{5/2}}{2(q_{>u}-1)^2} \le \frac{w^{5/2}}{2\lfloor u \rfloor^2}$ ($u \ge 2$).
   - **Exact full-space operator norm theorem**: $\|\mathcal{P}_u^{-1}\|_{\mathcal{H}_\eta \to \mathcal{H}_\eta} = \prod_{p \le u}(1 - p^{-1/2-\eta})^{-1}$ on $\mathcal{H}_\eta$ ($\eta > 0$) by $\mathbb{Q}$-linear independence of $\{\log p : p \le u\}$ and continuous Kronecker simultaneous approximation.
   - **Diagonal asymptotic and near-diagonal band bound**: $D_E(Y) = \frac{3\sqrt{\tau}}{64}\log\tau + O(Y^{-2})$ and $\sum_{|m-n|\le H}K_Y(m,n) \le (2H+1)D_E(Y)$ (`near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing`).
   - **Retirement of false uniform pairing bound & proved replacement bounds**: Counterexample at $(Y, p, q, r, m, n) = (33, 11, 2, 5, 1, 11)$ ($0.819425\dots > 0.3993$, elementary bound $1559/2890 > 3993/10000$), replaced by the two-sided integrand-ratio enclosure and the transition relative-gap bound $|K_Y(a, n) - K_Y(b, n)| \le \frac{b-a}{a}(\frac{b}{a})^3(3 + \frac{2\tau^2 Y^2}{a^2})K_Y(b, n)$ (`pairing_counterexample_replacement_and_finite_reconstruction_tc055r`).
   - **Repaired parity control asymptotics**: Exact unimodal constant $C_{1,\mathrm{uni}} = 2(3/(2e))^{3/2} = \frac{1}{\sqrt{2}}(3/e)^{3/2} < (3/e)^{3/2}$, second-order Euler–Maclaurin bound $|Q_{\mathbf{1}}(w) - \sqrt{w}/2| \le 3w^{-3/2}$ giving $Q_{a_2}(X) = \frac{\sqrt{X}}{6} + O(X^{-1/2})$ and $E_{a_2}(Y) = \frac{\tau-1}{36}Y + O(1)$, and $S = \{3, 5, 7\}$ control $Q_{a_{\{3,5,7\}}}(X) \sim \frac{1}{8}\sqrt{X}$, $E_{a_{\{3,5,7\}}}(Y) \sim \frac{\tau-1}{64}Y$.
   - **Exact finite $T$-truncation $m$-dependent reconstruction & tail transfer**: $Q_{\lambda, T}(X) = \sum_{m \in \mathcal{S}(P), m \le T}\frac{\lambda(m)}{\sqrt{m}}Q_{\lambda, P, \lfloor T/m \rfloor}(X/m)$ and $\mathcal{R}_{\mathrm{tail}}(Y, T) \le \frac{(\tau^5-1)Y^5}{20 T^4} = O(1)$ at $T(Y) = \lceil Y^{5/4} \rceil$.
2. **Remaining Open Obstruction**:
   - Proving $E_{\lambda, T(Y)}(Y) \ll_\varepsilon Y^\varepsilon$ requires overcoming the two-part obstruction between smooth-fiber Kronecker norm growth for large $u$ and the off-diagonal coprime cofactor sum $E_{\mathrm{diff}\text{-}r}(Y; T(Y), P_u)$ for small $u$. Accordingly, `SUBGATE-TC-043A` remains `OPEN` and `rh_proved` remains `false`.
