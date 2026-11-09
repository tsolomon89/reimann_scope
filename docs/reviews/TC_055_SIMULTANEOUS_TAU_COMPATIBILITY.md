# Mathematical Review & Proof Attempt Report: Simultaneous $\tau$-Compatibility, Weighted Cofactor Energy Decomposition, Full Lean Finite Reconstruction, Exact Cutoff & Parity Constant Repairs (`TASK-TC-055`, `TASK-TC-055R` & `TASK-TC-055R2`)

- **Task ID**: `TASK-TC-055` (`task/tc-055-simultaneous-tau-compatibility-and-signed-energy-cancellation`)
- **Repair Task ID**: `TASK-TC-055R` (`task/tc-055r-pairing-bound-operator-norm-and-finite-energy-repair`)
- **Closeout Task ID**: `TASK-TC-055R2` (`task/tc-055r2-weighted-energy-finite-reconstruction-and-closeout`)
- **Parent Epic**: `EPIC-TC-042` (Canonical $\tau$-Adelic Theta-Correlation Bound and Hilbert-Schmidt Orbit Control)
- **Merged `main` Baseline (`TC-054R2` merge)**: `8a898c60b7c4cb56543a3d1e7960c39e00027c22`
- **Prior `TC-054R` / `TC-054R2` Implementation / Reviewed HEAD**: `27489f195d3313d9ee60773157e3a8240f5bcadd` / `f265042ab52cabda29e76859cebace21cfae9239` and `a4b30737013aa2e16d095b897fa6b97b08f451dc` / `e178497d7637b799ce6eda5ed0cb2486c841c577`
- **Reviewed `TC-055` Implementation / Reviewed HEAD**: `c44df1ebfd10b8010e216214229a420ce8f3b5c2` / `07db77cf0ee62aa42e5c87b28a89a8f98eb3271e`
- **Reviewed `TC-055R` Implementation / Reviewed Tip**: `35b55405708ae7480263afc93e422b5626b1e134` / `c6a685542c2dd584293b463272c4d95152907b3e`
- **Initial Focused Closeout Commit (Section 2)**: `80d1c86408d39562b06b2c69d4b4f655a1677f82`
- **Primary Implementation Module**: [`tc/liouville_square_dilation.py`](../../tc/liouville_square_dilation.py)
- **Serialized 256-Bit Arb Certificate**: [`data/tc_liouville_square_dilation.json`](../../data/tc_liouville_square_dilation.json)
- **Formal Lean 4 Module**: [`formal/RiemannScope/LiouvilleSquareDilation.lean`](../../formal/RiemannScope/LiouvilleSquareDilation.lean) (`33` definitions, `16` public theorems, `27` private helper theorems = `76` declarations, `0` `sorry`, `0` custom `axiom`)
- **Regression Suite**: [`tests/test_tc_liouville_square_dilation.py`](../../tests/test_tc_liouville_square_dilation.py)
- **Subgate Status**: `SUBGATE-TC-043A: OPEN` (`rh_proved: false`)

---

## 1. Mathematical Framework, Notation, and Dependency Chain to `SUBGATE-TC-043A`

Throughout this report:
- $\tau = 2\pi$ is the sole circle constant;
- Complex Mellin variables are written $z = a + i b$ with $a, b \in \mathbb{R}$, and Riemann zeta zeros are written $\rho = x + i y$ with $x, y \in \mathbb{R}$ and critical coordinate $x = 1/2$;
- Admissible TC grades are real algebraic numbers $K \in \mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}$ (including negative grades $K < 0$), with scale factor $a_K = \tau^K > 0$;
- Auxiliary multiplicative dilations $S_p F(X) := F(X/p)$ by primes $p$ and $S_{d^2} F(X) := F(X/d^2)$ by squares $d^2$ act on the continuum scale variable $X \in (0, \infty)$. A dilation by $p$ or $d^2$ is **not** automatically an admissible algebraic TC grade shift, and we do **not** infer unrestricted grade rigidity from any unproved transcendence claim about $\log_\tau n$: by Lindemann's theorem ($e^\alpha$ is transcendental for every nonzero algebraic $\alpha$, so $\tau = 2\pi$ is transcendental), $\log_\tau n$ is irrational for every integer $n \ge 2$ (since $\log_\tau n = p/q \implies \tau^p = n^q \in \mathbb{Q}$, impossible for $p \ne 0$).
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
4. **Stage 4 — Simultaneous Joint System & Finite Signed-Energy Target (`TASK-TC-055` / `TASK-TC-055R` / `TASK-TC-055R2`)**:
   By Proposition 3.1 of [`TC_LIOUVILLE_SQUARE_DILATION.md`](./TC_LIOUVILLE_SQUARE_DILATION.md) and the two-sided $L^2$ truncation transfer at exact integer-power cutoff $T(Y) = \lceil Y^{5/4} \rceil$ (§8.1), closing `SUBGATE-TC-043A` through the Liouville/Mellin route is equivalent to proving the subpower grade-interval energy bound for $Y \ge 1$:
   $$\boxed{\forall \varepsilon > 0\;\exists C_\varepsilon < \infty\;\forall Y \ge 1, \qquad 0 \le E_{\lambda, T(Y)}(Y) := \int_Y^{\tau Y}\bigl|Q_{\lambda, T(Y)}(X)\bigr|^2\,\frac{dX}{X} = \sum_{1 \le m, n \le T(Y)}\lambda(m)\lambda(n)K_Y(m, n) \le C_\varepsilon Y^\varepsilon.}$$

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

| $m$ | $z_m = -(2m + 1/2)$ | $\frac{2\zeta'(-4m)}{\zeta'(-2m)} = \frac{2(-1)^m(4m)!\,\zeta(4m+1)}{\tau^{2m}(2m)!\,\zeta(2m+1)}$ (256-Bit Arb) | Removable Limit $\mathcal{M}[Q_\lambda](z_m)$ (256-Bit Arb) | Consistency Check (Zero in Diff) |
| :---: | :---: | :--- | :--- | :---: |
| `1` | `-5/2` | `[-0.5244148453865806892464532872372081404637 +/- 3.84e-41]` <!-- tc-enclosure: observable="two_zeta_prime_neg_4m_over_zeta_prime_neg_2m" params="m=1;z_m_formula=-5/2" json_path="section_8_tc055_simultaneous_compatibility_and_joint_identities.trivial_zero_and_mellin_cancellation_audit.rows[m=1].two_zeta_prime_neg_4m_over_zeta_prime_neg_2m" --> | `[-0.3485629170665496481654383777471629852612 +/- 2.29e-41]` <!-- tc-enclosure: observable="removable_limit_M_Q_lambda_at_z_m" params="m=1;z_m_formula=-5/2" json_path="section_8_tc055_simultaneous_compatibility_and_joint_identities.trivial_zero_and_mellin_cancellation_audit.rows[m=1].removable_limit_M_Q_lambda_at_z_m" --> | `True` |
| `2` | `-9/2` | `[2.083256108289591626747725328833321282615 +/- 1.76e-40]` <!-- tc-enclosure: observable="two_zeta_prime_neg_4m_over_zeta_prime_neg_2m" params="m=2;z_m_formula=-9/2" json_path="section_8_tc055_simultaneous_compatibility_and_joint_identities.trivial_zero_and_mellin_cancellation_audit.rows[m=2].two_zeta_prime_neg_4m_over_zeta_prime_neg_2m" --> | `[3.461695604587805051981063197595605540342 +/- 3.23e-40]` <!-- tc-enclosure: observable="removable_limit_M_Q_lambda_at_z_m" params="m=2;z_m_formula=-9/2" json_path="section_8_tc055_simultaneous_compatibility_and_joint_identities.trivial_zero_and_mellin_cancellation_audit.rows[m=2].removable_limit_M_Q_lambda_at_z_m" --> | `True` |
| `3` | `-13/2` | `[-21.44853096621742898901566241644952752636 +/- 2.07e-39]` <!-- tc-enclosure: observable="two_zeta_prime_neg_4m_over_zeta_prime_neg_2m" params="m=3;z_m_formula=-13/2" json_path="section_8_tc055_simultaneous_compatibility_and_joint_identities.trivial_zero_and_mellin_cancellation_audit.rows[m=3].two_zeta_prime_neg_4m_over_zeta_prime_neg_2m" --> | `[-124.7417433522037657050719315781104093510 +/- 6.72e-39]` <!-- tc-enclosure: observable="removable_limit_M_Q_lambda_at_z_m" params="m=3;z_m_formula=-13/2" json_path="section_8_tc055_simultaneous_compatibility_and_joint_identities.trivial_zero_and_mellin_cancellation_audit.rows[m=3].removable_limit_M_Q_lambda_at_z_m" --> | `True` |

### 3.3 Simultaneous Finite-Prime Exclusion Identity and Convergent $P$-Smooth Inverse

**Theorem 3.1 (Finite-Prime Exclusion Sieve Identity and $P$-Smooth Inverse Reconstruction).**
Let $P \subset \mathbb{P}$ be any finite set of primes, let $N_P := \prod_{p\in P}p$, and let $\mathcal{S}(P) := \{m \ge 1 : p \mid m \implies p \in P\}$ denote the set of $P$-smooth positive integers.
1. For every integer $n \ge 1$ and every divisor $d \mid \gcd(n, N_P)$, complete multiplicativity $\lambda(a b) = \lambda(a)\lambda(b)$ and $\lambda(d)^2 = 1$ give $\mu(d)^2\lambda(n/d) = \lambda(n)\mu(d)$, and therefore
   $$\sum_{d \mid \gcd(n, N_P)}\mu(d)^2\lambda(n/d) = \lambda(n)\sum_{d \mid \gcd(n, N_P)}\mu(d) = \begin{cases}\lambda(n), & \gcd(n, N_P) = 1,\\ 0, & \gcd(n, N_P) > 1.\end{cases}$$
   *(Formalized on actual positive integers in Lean 4 theorem `actual_finite_prime_exclusion_sieve_identity_nat`.)*
2. Applying the commutative product operator $\mathcal{P}_P = \prod_{p\in P}(I + p^{-1/2}S_p) = \sum_{d \mid N_P}\frac{\mu(d)^2}{\sqrt{d}}S_d$ to $Q_\lambda(X)$ for $X > 0$ yields the coprime-filtered observable:
   $$\boxed{Q_{\lambda, P}(X) := \prod_{p\in P}\bigl(I + p^{-1/2}S_p\bigr)Q_\lambda(X) = \sum_{d \mid N_P}\frac{|\mu(d)|}{\sqrt{d}}\,Q_\lambda(X/d) = X^{5/2}\sum_{\substack{n\ge 1 \\ \gcd(n, N_P)=1}}\frac{\lambda(n)}{n^3}e^{-X^2/n^2}.}$$
3. Every integer $n \ge 1$ factors uniquely as $n = m r$ with $m \in \mathcal{S}(P)$ and $\gcd(r, N_P) = 1$ (proved unconditionally in Lean 4 theorem `smooth_coprime_positive_factorization_exists_unique_nat`). Since $\lambda(m r) = \lambda(m)\lambda(r)$, $Q_{\lambda, P}$ reconstructs $Q_\lambda$ via the absolutely convergent $P$-smooth series:
   $$\boxed{Q_\lambda(X) = \sum_{m \in \mathcal{S}(P)}\frac{\lambda(m)}{\sqrt{m}}\,Q_{\lambda, P}(X/m),}$$
   with explicit floor-guarded truncation remainder bound for any real $M \ge 1$:
   $$\left|\sum_{\substack{m \in \mathcal{S}(P) \\ m > M}}\frac{\lambda(m)}{\sqrt{m}}\,Q_{\lambda, P}(X/m)\right| \le \zeta(3)X^{5/2}\sum_{m > M}m^{-3} \le \frac{\zeta(3)X^{5/2}}{2\lfloor M \rfloor^2}.$$

All 12 test pairs $(P, X) \in \{(2,), (2,3), (2,3,5)\} \times \{1, 2, \tau, 4\}$ in `section_8_tc055_simultaneous_compatibility_and_joint_identities` are explicitly labeled as numerical consistency checks (`"same_observable_operator_vs_series_consistency_check"`): interval overlap / zero-in-residual checks confirm implementation agreement, while exact equality rests on the proved algebraic/analytic rearrangement and the finite Lean theorems of §8.1.

---

## 4. Exact Rational Cutoff Decisions, Distinct Coprime Tail Bounds, and Exact Full-Space Operator Norm Obstruction (`TASK-TC-055R` §4 & §5.2; `TASK-TC-055R2` §5)

### 4.1 Non-Integer Cutoff Counterexample ($u = 2.9$), Exact Dyadic Boundary Decisions, and Distinct Coprime Tail Bounds

1. **Counterexample to unguarded $\sum_{n > u} n^{-3} \le \frac{1}{2u^2}$ at non-integer $u = 2.9$ (`TASK-TC-055R` §5.2)**:
   For a non-integer real cutoff $u \ge 1$, the first integer strictly exceeding $u$ is $\lfloor u \rfloor + 1$, so the integral comparison compares against $\int_{\lfloor u \rfloor}^\infty t^{-3}\,dt = \frac{1}{2\lfloor u \rfloor^2}$, **not** $\frac{1}{2u^2}$. At $u = 2.9$ ($\lfloor u \rfloor = 2$),
   $$\sum_{n > 2.9} n^{-3} = \sum_{n \ge 3} n^{-3} = \zeta(3) - 1 - \frac{1}{8} \in \bigl[0.07705690315959428539973816151144999076499 \pm 3.71 \times 10^{-42}\bigr]$$ <!-- tc-enclosure: observable="exact_unrestricted_tail_at_2_9" params="counterexample_u=2.9 (29/10)" json_path="section_9_tc055_coupled_cutoff_and_norm_obstruction.non_integer_cutoff_counterexample_and_boundary_repair.exact_unrestricted_tail_at_2_9" -->
   (indeed, the first three terms $3^{-3} + 4^{-3} + 5^{-3} = \frac{1}{27} + \frac{1}{64} + \frac{1}{125} \in [0.06066203703703703703703703703703703703704 \pm 2.97 \times 10^{-42}]$ <!-- tc-enclosure: observable="three_term_lower_bound_n_3_4_5" params="counterexample_u=2.9 (29/10)" json_path="section_9_tc055_coupled_cutoff_and_norm_obstruction.non_integer_cutoff_counterexample_and_boundary_repair.three_term_lower_bound_n_3_4_5" --> already exceed $\frac{50}{841}$), which **strictly exceeds** the unguarded value
   $$\frac{1}{2(2.9)^2} = \frac{50}{841} \in \bigl[0.05945303210463733650416171224732461355529 \pm 1.32 \times 10^{-42}\bigr]$$ <!-- tc-enclosure: observable="claimed_1_over_2_u_sq_at_2_9" params="counterexample_u=2.9 (29/10)" json_path="section_9_tc055_coupled_cutoff_and_norm_obstruction.non_integer_cutoff_counterexample_and_boundary_repair.claimed_1_over_2_u_sq_at_2_9" -->
   by outward-endpoint margin $[0.01760387105495694889557644926412537720969 \pm 4.98 \times 10^{-42}]$ <!-- tc-enclosure: observable="violation_margin_exact_minus_claimed" params="counterexample_u=2.9 (29/10)" json_path="section_9_tc055_coupled_cutoff_and_norm_obstruction.non_integer_cutoff_counterexample_and_boundary_repair.violation_margin_exact_minus_claimed" -->, while satisfying the repaired floor-guarded bound $\frac{1}{2\lfloor 2.9 \rfloor^2} = \frac{1}{8} = 0.125$.
2. **Exact rational / dyadic cutoff decisions without IEEE-754 `float` conversion (`TASK-TC-055R2` §5)**:
   In `exact_floor_and_least_prime_strictly_above`, `float` inputs are rejected (`TypeError`), exact `int`/`Fraction` inputs use exact integer division `u.numerator // u.denominator`, and `arb` inputs extract exact dyadic rational endpoints $[u_{\mathrm{low}}, u_{\mathrm{high}}]$ directly from FLINT's binary mantissa/exponent representation. If an `arb` ball crosses an integer boundary ($\lfloor u_{\mathrm{low}} \rfloor \ne \lfloor u_{\mathrm{high}} \rfloor$), discrete classification raises `ValueError` rather than classifying by midpoint, while `enclose_unrestricted_tail_floor_bound_arb` returns the rigorous interval union covering every branch across $[u_{\mathrm{low}}, u_{\mathrm{high}}]$. Certified exact boundary outcomes in `boundary_cutoff_rows`:
   - $u = 3 - 2^{-100}$: $\lfloor u \rfloor = 2$, $q_{>u} = 3$;
   - $u = 3$ and $u = 3 + 2^{-100}$: $\lfloor u \rfloor = 3$, $q_{>u} = 5$;
   - $u = 5 - 2^{-100}$: $\lfloor u \rfloor = 4$, $q_{>u} = 5$;
   - $u = 5$ and $u = 5 + 2^{-100}$: $\lfloor u \rfloor = 5$, $q_{>u} = 7$.
3. **Distinct general and next-prime coprime tail bounds labeled by their exact formulas**:
   - **General floor-guarded tail ($u \ge 1$ real)**:
     $$\boxed{\sum_{n > u}\frac{1}{n^3} = \sum_{n \ge \lfloor u \rfloor + 1}\frac{1}{n^3} \le \int_{\lfloor u \rfloor}^\infty t^{-3}\,dt = \frac{1}{2\lfloor u \rfloor^2} \qquad (\forall u \ge 1).}$$
   - **Coprime tail ($u \ge 2$ real, $P_u = \{p \le u\}$, $N_u = \prod_{p \le u}p$, least prime $q_{>u} > u$)**: Keeping the three valid upper bounds explicitly labeled by their distinct formulas:
     $$\boxed{Q_{\lambda, P_u}(w) = w^{5/2}e^{-w^2} + R_{\lambda, P_u}(w), \qquad \bigl|R_{\lambda, P_u}(w)\bigr| \le w^{5/2}\!\left(\frac{1}{q_{>u}^3} + \frac{1}{2 q_{>u}^2}\right) \le \frac{w^{5/2}}{2(q_{>u} - 1)^2} \le \frac{w^{5/2}}{2\lfloor u \rfloor^2},}$$
     where splitting off the first coprime term $n = q_{>u}$ gives $\sum_{n \ge q_{>u}} n^{-3} = q_{>u}^{-3} + \sum_{n > q_{>u}} n^{-3} \le q_{>u}^{-3} + \frac{1}{2 q_{>u}^2}$, while integral comparison from $q_{>u} - 1 \ge \lfloor u \rfloor$ gives $\sum_{n \ge q_{>u}} n^{-3} \le \frac{1}{2(q_{>u} - 1)^2} \le \frac{1}{2\lfloor u \rfloor^2}$ (`coprime_bound_w_5_2_times_q_neg_3_plus_1_over_2_q_sq`, `coprime_bound_w_5_2_over_2_q_minus_1_sq`, and `coprime_bound_w_5_2_over_2_floor_u_sq`).
4. **Signed grade-interval energy expansion**:
   Expanding $Q_{\lambda, P_u}(X) = \sum_{d \mid N_u}\frac{|\mu(d)|}{\sqrt{d}}Q_\lambda(X/d)$ and integrating $|Q_{\lambda, P_u}(X)|^2\,\frac{dX}{X}$ over $[Y, \tau Y]$ ($Y \ge 1$) gives the exact multi-scale energy relation retaining all diagonal ($d_1 = d_2$) and cross-scale ($d_1 \ne d_2$) terms:
   $$E_{\lambda, P_u}(Y) := \int_Y^{\tau Y}\bigl|Q_{\lambda, P_u}(X)\bigr|^2\,\frac{dX}{X} = \sum_{d \mid N_u}\frac{|\mu(d)|}{d}\,E_\lambda(Y/d) + 2\sum_{\substack{d_1, d_2 \mid N_u \\ d_1 < d_2}}\frac{|\mu(d_1)||\mu(d_2)|}{\sqrt{d_1 d_2}}\int_Y^{\tau Y}Q_\lambda(X/d_1)Q_\lambda(X/d_2)\,\frac{dX}{X}.$$

### 4.2 Exact Full-Space Operator Norm Obstruction on $\mathcal{H}_\eta$ (`TASK-TC-055R` §4; `TASK-TC-055R2` §7)

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
   By unique prime factorization in $\mathbb{Z}_{\ge 1}$, $\{\log p : p \le u\}$ are linearly independent over $\mathbb{Q}$. By the continuous form of Kronecker's simultaneous approximation theorem (see e.g. T. Aoyama and T. Nakamura, `arXiv:1204.4043`, p. 9; Hardy & Wright, Theorem 444), the flow $b \mapsto (b\log p \bmod \tau)_{p \le u}$ has dense image in $(\mathbb{R}/\tau\mathbb{Z})^{\pi(u)}$, approaching $(\tau/2, \dots, \tau/2)$ where $e^{-ib\log p} = -1$ simultaneously for all $p \le u$. Thus $\sup_{b \in \mathbb{R}}|m_{u, \eta}(b)| \ge \prod_{p \le u}(1 - p^{-1/2 - \eta})^{-1}$. $\blacksquare$

> **Consequence & Near-Odd-Harmonic Witness (`TASK-TC-055R` §4; `TASK-TC-055R2` §1 & §7)**: The search over odd integers $k_{\mathrm{odd}} \in \{1, 3, \dots, 3999\}$ directly returns the odd harmonic integer $k_{\mathrm{odd}} = 2513$, giving the exact witness formula $b_* = \frac{2513\tau}{2\log 2}$ (never $(2\cdot 2513 + 1)\frac{\tau}{2\log 2}$). At $u = 5, \eta = 1/4$,
> - $b_* = \frac{2513\tau}{2\log 2} \in [11389.82103641173804359436724258598369396 \pm 1.89 \times 10^{-36}]$ <!-- tc-enclosure: observable="b_witness" params="odd_harmonic_index_k_odd=2513;b_witness_formula=2513 * tau / (2 * log 2)" json_path="section_9_tc055_coupled_cutoff_and_norm_obstruction.exact_full_space_operator_norm_obstruction.kronecker_phase_alignment_witness_P_2_3_5_eta_1_4.b_witness" -->,
> - $|m_{5, 1/4}(b_*)| \in [6.264139038011680689993761243736081380159 \pm 3.91 \times 10^{-41}]$ <!-- tc-enclosure: observable="abs_m_u_eta_at_b_witness" params="odd_harmonic_index_k_odd=2513" json_path="section_9_tc055_coupled_cutoff_and_norm_obstruction.exact_full_space_operator_norm_obstruction.kronecker_phase_alignment_witness_P_2_3_5_eta_1_4.abs_m_u_eta_at_b_witness" --> vs. exact supremum $\prod_{p \le 5}(1 - p^{-3/4})^{-1} \in [6.269653257665089643352758026278521806500 \pm 4.85 \times 10^{-40}]$ <!-- tc-enclosure: observable="exact_supremum_prod_1_minus_p_neg_3_4_inv" params="odd_harmonic_index_k_odd=2513" json_path="section_9_tc055_coupled_cutoff_and_norm_obstruction.exact_full_space_operator_norm_obstruction.kronecker_phase_alignment_witness_P_2_3_5_eta_1_4.exact_supremum_prod_1_minus_p_neg_3_4_inv" --> (ratio $[0.9991204904917720235746293874986996629006 \pm 1.52 \times 10^{-42}]$ <!-- tc-enclosure: observable="ratio_witness_to_exact_supremum" params="odd_harmonic_index_k_odd=2513" json_path="section_9_tc055_coupled_cutoff_and_norm_obstruction.exact_full_space_operator_norm_obstruction.kronecker_phase_alignment_witness_P_2_3_5_eta_1_4.ratio_witness_to_exact_supremum" -->).
> This closes any universal full-space inverse-filter norm strategy permanently and distinguishes full-space operator norms from estimates restricted to the actual arithmetic input $Q_{\lambda, T}(X)$.

### 4.3 Off-Critical Mode Multiplier Bounds

On an off-critical mode $F_\rho(X) := X^{\rho - 1/2}$ ($\rho = x + iy$, $x > 0$), $p^{-1/2}S_p F_\rho(X) = p^{-\rho}F_\rho(X)$, so
$$\mathcal{P}_{P_u} F_\rho(X) = M_u(\rho)\,F_\rho(X), \qquad M_u(\rho) := \prod_{p \le u}\bigl(1 + p^{-\rho}\bigr),$$
which satisfies the two-sided nonvanishing bounds for every finite $u \ge 2$ and every $x > 0$:
$$\boxed{0 < \prod_{p \le u}\bigl(1 - p^{-x}\bigr) \le \bigl|M_u(\rho)\bigr| \le \prod_{p \le u}\bigl(1 + p^{-x}\bigr) < \infty.}$$
Thus no finite prime exclusion filter $\mathcal{P}_{P_u}$ can annihilate an off-critical mode $X^{\rho - 1/2}$.

---

## 5. Integrated Energy Kernel $K_Y(m, n)$, Diagonal Asymptotic $D_E(Y)$, and Near-Diagonal Band Bound (`TASK-TC-055R2` §6)

### 5.1 Exact Kernel Representation and Closed-Form Gaussian Antiderivative

Expanding $|Q_\lambda(X)|^2$ and integrating term-by-term against $\frac{dX}{X}$ over $[Y, \tau Y]$ ($Y \ge 1$, justified by uniform convergence on compact intervals $[Y, \tau Y]$) gives
$$\boxed{E_\lambda(Y) = \int_Y^{\tau Y}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} = \sum_{m, n \ge 1}\lambda(m)\lambda(n)K_Y(m, n),}$$
where the symmetric positive kernel $K_Y(m, n)$ is
$$K_Y(m, n) := \frac{1}{(m n)^3}\int_Y^{\tau Y} X^4 \exp\!\left(-X^2\left(\frac{1}{m^2} + \frac{1}{n^2}\right)\right)dX > 0.$$
Setting $\alpha := m^{-2} + n^{-2} > 0$, integration by parts twice yields the exact closed-form antiderivative
$$\int X^4 e^{-\alpha X^2}\,dX = \frac{3\sqrt{\tau/2}}{8\,\alpha^{5/2}}\operatorname{erf}(\sqrt{\alpha}\,X) - \left(\frac{X^3}{2\alpha} + \frac{3X}{4\alpha^2}\right)e^{-\alpha X^2},$$
evaluated in 256-bit Arb in `evaluate_energy_kernel_K_Y_certified_arb`.

### 5.2 Unconditional Diagonal Energy Asymptotic $D_E(Y)$ for All $Y > 0$

**Theorem 5.1 (Diagonal Energy Asymptotic with Explicit Euler–Maclaurin Error Constants).**
For every $Y > 0$, the diagonal energy sum $D_E(Y) := \sum_{n\ge 1} K_Y(n, n)$ satisfies
$$\boxed{D_E(Y) = \frac{3\sqrt{\tau}}{64}\log\tau + R_{D, E}(Y), \qquad \bigl|R_{D, E}(Y)\bigr| \le C_{D, 2}\,Y^{-2} \quad\text{and}\quad \bigl|R_{D, E}(Y)\bigr| \le C_{D, 4}\,Y^{-4} \qquad (\forall Y > 0),}$$
where:
- $\frac{3\sqrt{\tau}}{64}\log\tau \in [0.2159472478105097999629716116351322819076 \pm 3.24 \times 10^{-41}]$ <!-- tc-enclosure: observable="leading_constant_3_sqrt_tau_over_64_log_tau" params="domain_of_validity=All Y > 0" json_path="section_10_tc055_integrated_energy_kernel_and_near_diagonal.leading_constant_3_sqrt_tau_over_64_log_tau" -->,
- $C_{D, 2} := \frac{C_2(1 - \tau^{-2})}{16\sqrt{2}} \in [0.07974240995631961059711944730929191094454 \pm 4.2 \times 10^{-44}]$ <!-- tc-enclosure: observable="explicit_N2_error_constant_C_D2" params="domain_of_validity=All Y > 0" json_path="section_10_tc055_integrated_energy_kernel_and_near_diagonal.explicit_N2_error_constant_C_D2" -->,
- $C_{D, 4} := \frac{C_4(1 - \tau^{-4})}{64\sqrt{2}} \in [0.09663891408812621065182768769598639544928 \pm 1.86 \times 10^{-42}]$ <!-- tc-enclosure: observable="explicit_N4_error_constant_C_D4" params="domain_of_validity=All Y > 0" json_path="section_10_tc055_integrated_energy_kernel_and_near_diagonal.explicit_N4_error_constant_C_D4" -->,
with $C_2 \in [1.851257667016958056850958359201349291641 \pm 3.54 \times 10^{-40}]$ <!-- tc-enclosure: observable="C_2" params="" json_path="section_4_unconstrained_common_factor_and_euler_maclaurin.euler_maclaurin_derivatives_and_constants.C_2" --> and $C_4 \in [8.752371760035365551239039765015814873069 \pm 1.09 \times 10^{-40}]$ <!-- tc-enclosure: observable="C_4" params="" json_path="section_4_unconstrained_common_factor_and_euler_maclaurin.euler_maclaurin_derivatives_and_constants.C_4" --> from Theorem 4.1 of [`TC_LIOUVILLE_SQUARE_DILATION.md`](./TC_LIOUVILLE_SQUARE_DILATION.md).

### 5.3 Unconditional Near-Diagonal Band Inequality and Full Complementary Off-Diagonal Domain (`TASK-TC-055R2` §6)

**Proposition 5.2 (Near-Diagonal Band Bound).**
For all $m, n \ge 1$ and $Y > 0$, $2 K_Y(m, n) \le K_Y(m, m) + K_Y(n, n)$, and for every integer $H \ge 0$:
$$\boxed{\left|\sum_{|m - n| \le H}\lambda(m)\lambda(n)K_Y(m, n)\right| \le \sum_{|m - n| \le H} K_Y(m, n) \le (2H + 1)D_E(Y).}$$
*(Algebraic core formalized in Lean 4 theorem `near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing` and certified in 256-bit Arb across $Y \in \{1, 2, 4\}$ and $H \in \{0, 1, 2, 4\}$.)*

> **Exact Complementary Domain (`TASK-TC-055R2` §6)**: Proposition 5.2 controls the near-diagonal band $|m - n| \le H$ (contributing at most $(2H + 1)D_E(Y) = O(Y^\varepsilon)$ when $H = O(Y^\varepsilon)$). It does **not** by itself localize the remaining sum exclusively to $m, n \asymp Y$: in the untruncated sum, the remaining obligation spans the **full complementary off-diagonal domain** $\{(m, n) \in \mathbb{N}_{\ge 1}^2 : |m - n| > H\}$ (including large-index tails and asymmetric cross regions), while after applying the explicit $L^2$ tail bound $\mathcal{R}_{\mathrm{tail}}(Y, T(Y)) \le \frac{\tau^5 - 1}{20}$ at $T(Y) = \lceil Y^{5/4} \rceil$ (§8.1) it spans the full finite complementary off-diagonal domain $\{(m, n) \in \{1, \dots, T(Y)\}^2 : |m - n| > H\}$.

---

## 6. Counterexample Synchronization, Relative-Gap Regime Qualification, and Density/Mass Separation (`TASK-TC-055R` §2–§3; `TASK-TC-055R2` §6–§7)

### 6.1 Synchronized Counterexample to Retired Uniform Pairing Bound (`TC-055` Lemma 6.1)

In the initial `TC-055` draft, Lemma 6.1 claimed that for all $Y > 0$, $p$ prime, $q r$ semiprime, and $m, n \ge 1$,
$$\bigl|K_Y(p m, n) - K_Y(q r m, n)\bigr| \stackrel{?}{\le} 3\,\frac{|q r - p|}{u_{\min}}\left(\frac{u_{\max}}{u_{\min}}\right)^3 K_Y(u_{\max} m, n), \qquad u_{\min} = \min(p, q r), \quad u_{\max} = \max(p, q r).$$

1. **Algebraic flaw in the original proof**:
   For $g_X(u) = u^{-3}e^{-X^2/u^2}$, $g_X'(u) = u^{-4}(2 w^2 - 3)e^{-w^2}$ ($w = X/u$). Bounding $|(2w^2 - 3)e^{-w^2}| \le 3$ **consumes** $e^{-w^2} = e^{-X^2/u^2}$ and forbids retaining a second Gaussian factor $e^{-X^2/u_2^2}$ afterward; retaining $e^{-X^2/b^2}$ on $u \in [a, b]$ requires bounding $|2X^2/u^2 - 3| \le 3 + 2\tau^2 Y^2/a^2$.
2. **Generator-Synchronized 256-Bit Arb Counterexample at $Y = 33, p = 11, q = 2, r = 5, m = 1, n = 11$ ($q r = 10, u_{\min} = 10, u_{\max} = 11$)**:
   - Claimed normalized upper bound:
     $$3\,\frac{|10 - 11|}{10}\left(\frac{11}{10}\right)^3 = \frac{3 \times 1331}{10000} = \frac{3993}{10000} = 0.3993.$$
   - Certified 256-bit Arb evaluations (synchronized directly with `retired_tc055_lemma61_counterexample` in `data/tc_liouville_square_dilation.json` and independently verified by `acb.integral` quadrature):
     - $K_{33}(11, 11) \in [1.014555194807418856767367389761759629841 \times 10^{-8} \pm 4.23 \times 10^{-48}]$ <!-- tc-enclosure: observable="K_33_11_11" params="Y=33;p=11;q=2;r=5;qr=10;m=1;n=11" json_path="section_11_tc055_opposite_parity_dilation_pairing.retired_tc055_lemma61_counterexample.K_33_11_11" -->,
     - $K_{33}(10, 11) \in [1.832030184902205780450441748645605924856 \times 10^{-9} \pm 3.04 \times 10^{-49}]$ <!-- tc-enclosure: observable="K_33_10_11" params="Y=33;p=11;q=2;r=5;qr=10;m=1;n=11" json_path="section_11_tc055_opposite_parity_dilation_pairing.retired_tc055_lemma61_counterexample.K_33_10_11" -->,
     - $\bigl|K_{33}(11, 11) - K_{33}(10, 11)\bigr| \in [8.313521763171982787223232148971990373549 \times 10^{-9} \pm 4.67 \times 10^{-49}]$ <!-- tc-enclosure: observable="abs_diff_K_33_11_11_minus_K_33_10_11" params="Y=33;p=11;q=2;r=5;qr=10;m=1;n=11" json_path="section_11_tc055_opposite_parity_dilation_pairing.retired_tc055_lemma61_counterexample.abs_diff_K_33_11_11_minus_K_33_10_11" -->,
     - Normalized difference ($\approx 0.8194252817117595 > 0.3993$) and outward-endpoint violation margin:
       $$0.3993 < \frac{\bigl|K_{33}(11, 11) - K_{33}(10, 11)\bigr|}{K_{33}(11, 11)} \in \bigl[0.8194252817117595423362805867661925634141 \pm 4.15 \times 10^{-41}\bigr],$$ <!-- tc-enclosure: observable="actual_normalized_difference" params="Y=33;p=11;q=2;r=5;qr=10;m=1;n=11" json_path="section_11_tc055_opposite_parity_dilation_pairing.retired_tc055_lemma61_counterexample.actual_normalized_difference" -->
       with normalized excess margin $[0.4201252817117595423362805867661925634141 \pm 4.15 \times 10^{-41}]$ <!-- tc-enclosure: observable="normalized_violation_margin_actual_minus_claimed" params="Y=33;p=11;q=2;r=5;qr=10;m=1;n=11" json_path="section_11_tc055_opposite_parity_dilation_pairing.retired_tc055_lemma61_counterexample.normalized_violation_margin_actual_minus_claimed" --> and absolute excess margin $[4.262402870305959292151134161653284171596 \times 10^{-9} \pm 4.26 \times 10^{-50}]$ <!-- tc-enclosure: observable="absolute_violation_margin_actual_minus_claimed" params="Y=33;p=11;q=2;r=5;qr=10;m=1;n=11" json_path="section_11_tc055_opposite_parity_dilation_pairing.retired_tc055_lemma61_counterexample.absolute_violation_margin_actual_minus_claimed" -->.
3. **Elementary Floating-Point-Free Proof of the Contradiction**:
   For every $X \in [33, 33\tau]$, $X^2(10^{-2} - 11^{-2}) \ge 1089 \cdot \frac{21}{12100} = \frac{189}{100}$ and $e^{-189/100} < \frac{1}{1 + 189/100} = \frac{100}{289}$, so
   $$\frac{K_{33}(10, 11)}{K_{33}(11, 11)} \le \frac{1331}{1000}\,e^{-189/100} < \frac{1331}{2890} \implies \frac{\bigl|K_{33}(11, 11) - K_{33}(10, 11)\bigr|}{K_{33}(11, 11)} > \frac{1559}{2890} > \frac{3993}{10000} = 0.3993,$$
   verified by `norm_num` in Lean 4 theorem `pairing_counterexample_replacement_and_finite_reconstruction_tc055r`.

### 6.2 Proved Replacement Bounds and Bounded-Ratio Qualification (`TASK-TC-055R` §3; `TASK-TC-055R2` §6)

**Theorem 6.1 (Two-Sided Integrand-Ratio Enclosure and Transition Relative-Gap Bound).**
Let $0 < a \le b$ be positive integers, let $n \ge 1$, and let $Y > 0$. Define $r_0 := b/a \ge 1$ and $\Delta := a^{-2} - b^{-2} \ge 0$.
1. **Two-Sided Integrand-Ratio Enclosure (Valid for all $Y > 0$ and all $0 < a \le b$)**:
   $$\boxed{r_0^3 e^{-(\tau Y)^2 \Delta} K_Y(b, n) \le K_Y(a, n) \le r_0^3 e^{-Y^2 \Delta} K_Y(b, n),}$$
   $$\boxed{\bigl|K_Y(a, n) - K_Y(b, n)\bigr| \le \max\!\Bigl(\bigl|r_0^3 e^{-(\tau Y)^2 \Delta} - 1\bigr|,\;\bigl|r_0^3 e^{-Y^2 \Delta} - 1\bigr|\Bigr) K_Y(b, n).}$$
2. **Transition-Regime Relative-Gap Bound (Retaining Full $(b/a)^3$ Factor)**:
   $$\boxed{\bigl|K_Y(a, n) - K_Y(b, n)\bigr| \le \frac{b - a}{a}\left(\frac{b}{a}\right)^3\left(3 + \frac{2\tau^2 Y^2}{a^2}\right) K_Y(b, n).}$$
   **Uniform $O((b - a)/a)$ regime qualification (`TASK-TC-055R2` §6)**: The exact coefficient retains the cubic ratio factor $(b/a)^3$ alongside $3 + \frac{2\tau^2 Y^2}{a^2}$. Consequently, a uniform $O((b - a)/a)\,K_Y(b, n)$ saving holds when **both** $a \ge c Y$ ($c > 0$, bounding $3 + \frac{2\tau^2 Y^2}{a^2} \le 3 + \frac{2\tau^2}{c^2}$) **and** $1 \le b/a \le R$ (or equivalently in a small relative-gap regime $0 \le \frac{b - a}{a} \le \delta_0$, where $(b/a)^3 \le (1 + \delta_0)^3 \le R^3$), with explicit constant $R^3(3 + \frac{2\tau^2}{c^2})$.

### 6.3 Exact Separation of Coprime Density (`16/77`) vs. Finite Sample Zero-Weight Frequency (`101/240`) and Smooth / Rough / Nonsmooth Classes (`TASK-TC-055R2` §6)

1. **Fixed Finite Factor Set $P_1 = \{5, 7, 11\}$, $P_2 = \{4, 6, 10\}$ ($N = \operatorname{lcm}(5, 7, 11, 4, 6, 10) = 4620$)**:
   Three distinct quantities must be kept strictly separate and named by their exact definitions:
   - **Natural coprime density modulo $N = 4620 = 2^2 \cdot 3 \cdot 5 \cdot 7 \cdot 11$**:
     $$\delta_{\mathrm{coprime}}(4620) := \frac{\varphi(4620)}{4620} = \prod_{p \mid 4620}\left(1 - \frac{1}{p}\right) = \frac{1}{2}\cdot\frac{2}{3}\cdot\frac{4}{5}\cdot\frac{6}{7}\cdot\frac{10}{11} = \frac{16}{77} \approx 0.2077922.$$
     On the finite test sample $1 \le k \le 240$, the finite sample coprime frequency is $\frac{50}{240} = \frac{5}{24} \approx 0.2083333$.
   - **Periodic natural density of zero pairing weight $\{k \ge 1 : W_{\mathrm{pair}}(k) = 0\}$ modulo $4620$**:
     Here $W_{\mathrm{pair}}(k) := \sum_{p \in P_1, p \mid k}\mathbf{1} + \sum_{s \in P_2, s \mid k}\mathbf{1}$ vanishes iff $k$ is divisible by none of $5, 7, 11$ (probability $\frac{4}{5}\cdot\frac{6}{7}\cdot\frac{10}{11} = \frac{48}{77}$, which already excludes $10 = 2 \cdot 5$) and by neither $4$ nor $6$ (8 residues out of 12 modulo $\operatorname{lcm}(4, 6) = 12$, namely $\{1, 2, 3, 5, 7, 9, 10, 11\}$, probability $\frac{8}{12} = \frac{2}{3}$). By the Chinese Remainder Theorem since $\gcd(12, 385) = 1$,
     $$\delta_{W_{\mathrm{pair}}=0}(4620) = \frac{2}{3}\cdot\frac{48}{77} = \frac{32}{77} \approx 0.4155844,$$
     strictly twice $\delta_{\mathrm{coprime}}(4620) = \frac{16}{77}$ because integers such as $k \equiv 2, 3, 9, 10 \pmod{12}$ (coprime to $385$) are not coprime to $4620$ yet still satisfy $4 \nmid k$ and $6 \nmid k$.
   - **Finite-sample zero-pairing-weight frequency on $1 \le k \le 240$**:
     $$f_{W_{\mathrm{pair}}=0}(240) := \frac{\#\{1 \le k \le 240 : W_{\mathrm{pair}}(k) = 0\}}{240} = \frac{101}{240} \approx 0.4208333.$$
     Thus $\frac{101}{240}$ is the finite-sample frequency of $W_{\mathrm{pair}}(k) = 0$ on $1 \le k \le 240$, **not** the natural coprime density $\frac{16}{77}$.
2. **Strict Separation of $P$-Smooth, $P$-Rough, and Nonsmooth Integers Under Growing Cutoff $u = Y^\theta$ ($0 < \theta < 1$)**:
   For $P = P_{Y^\theta} = \{p \le Y^\theta\}$ ($N_P = \prod_{p \le Y^\theta}p$), keep the three classes distinct:
   - **$P$-smooth integers**: $\mathcal{S}(P) = \{n \ge 1 : p \mid n \implies p \in P\}$, with Dickman asymptotic density $\rho_{\mathrm{Dickman}}(1/\theta) \in (0, 1)$ (on $P = \{2, 3, 5\}$, $1 \le n \le 120$: `36` integers).
   - **$P$-rough integers**: $\{n \ge 1 : \gcd(n, N_P) = 1\}$ (every prime factor $p \mid n$ satisfies $p > Y^\theta$, plus $n = 1$), whose density decays as $\frac{\omega_{\mathrm{Buchstab}}(1/\theta)}{\theta \log Y} = O(1/\log Y) \to 0$ (on $P = \{2, 3, 5\}$, $1 \le n \le 120$: `32` integers, including $n = 1$). Because all $Y^\theta$-rough integers (both primes and rough composites) have combined density $O(1/\log Y)$, **$Y^\theta$-rough composites do not have positive constant density and do not carry order-$Y$ unsigned transition mass**.
   - **Nonsmooth integers**: $\mathbb{Z}_{\ge 1} \setminus \mathcal{S}(P) = \{n \ge 1 : \exists p \mid n,\; p > Y^\theta\}$ (at least one prime factor outside $P$, comprising $P$-rough integers $n > 1$ *together with* mixed smooth–rough composites $n = m r$ with $m \in \mathcal{S}(P), m > 1$ and $\gcd(r, N_P) = 1, r > 1$; on $P = \{2, 3, 5\}$, $1 \le n \le 120$: `84` nonsmooth integers = `31` rough $>1$ + `53` mixed smooth–rough). Nonsmooth integers have strictly positive asymptotic density $1 - \rho_{\mathrm{Dickman}}(1/\theta) > 0$, and it is the **nonsmooth integers** (together with the $\mathcal{S}(P_{Y^\theta})$ smooth Dickman bulk) whose unsigned transition sum has order $Y$.
   - **Prime–prime sub-sum is NOT a lower bound for total signed energy**: Unmatched primes $p \in [Y, \tau Y]$ ($\lambda(p) = -1$) have count $\pi(\tau Y) - \pi(Y) \sim \frac{(\tau - 1)Y}{\log Y}$, so the restricted prime–prime quadratic sub-sum $\sum_{Y \le p, q \le \tau Y} K_Y(p, q) \asymp \frac{Y}{(\log Y)^2} > 0$ is positive. However, because prime–composite and composite–composite cross terms in $E_\lambda(Y) = \sum_{m, n \ge 1}\lambda(m)\lambda(n)K_Y(m, n)$ carry opposite signs, this restricted prime–prime energy is **never** a lower bound for the total signed energy $E_\lambda(Y)$.

---

## 7. Explicit $a_2$ Remainder Constant Repair ($C_{a_2} = 17 + \frac{16}{7}\zeta(3)$) and Scoped $S = \{3, 5, 7\}$ Asymptotics (`TASK-TC-055R` §5.1; `TASK-TC-055R2` §4)

For any finite set of primes $S \subset \mathbb{P}$, define $a_S(n) := (-1)^{\sum_{p \in S} v_p(n)}$ and $a_2(n) := a_{\{2\}}(n) = (-1)^{v_2(n)}$.

### 7.1 Complete Derivation of $C_{a_2} = 17 + \frac{16}{7}\zeta(3)$ and Derived Energy Remainder for $E_{a_2}(Y)$

1. **Exact unimodal constant $C_{1,\mathrm{uni}}$ (`TASK-TC-055R` §5.1)**:
   For $h_X(t) = t^{-3}e^{-X^2/t^2}$, $\max_{t > 0}h_X(t) = h_X(X\sqrt{2/3}) = (\frac{3}{2e})^{3/2}X^{-3}$, so $|Q_{\mathbf{1}}(X) - \frac{1}{2}\sqrt{X}| \le C_{1,\mathrm{uni}} X^{-1/2}$ with
   $$\boxed{C_{1,\mathrm{uni}} := 2\left(\frac{3}{2e}\right)^{3/2} = \frac{1}{\sqrt{2}}\left(\frac{3}{e}\right)^{3/2} \in \bigl[0.8198325578837200767815820207595078237088 \pm 2.50 \times 10^{-41}\bigr],}$$ <!-- tc-enclosure: observable="exact_C1_unimodal_2_times_3_over_2e_pow_3_2" params="" json_path="section_12_tc055_multiplicative_parity_controls.unimodal_and_second_order_euler_maclaurin_constants.exact_C1_unimodal_2_times_3_over_2e_pow_3_2" -->
   strictly smaller than $(3/e)^{3/2} \in [1.159418322234182419789034443434222535151 \pm 3.86 \times 10^{-40}]$ <!-- tc-enclosure: observable="strict_upper_3_over_e_pow_3_2" params="" json_path="section_12_tc055_multiplicative_parity_controls.unimodal_and_second_order_euler_maclaurin_constants.strict_upper_3_over_e_pow_3_2" -->.
2. **Exact dyadic expansion with coefficient $2$ (NOT $\sqrt{2}$)**:
   Since $a_2(n) = 1$ for odd $n$ and $a_2(2m) = -a_2(m)$, we have $(I + 2^{-1/2}S_2)Q_{a_2}(X) = Q_{\mathrm{odd}}(X) = (I - 2^{-1/2}S_2)Q_{\mathbf{1}}(X)$. Applying $(I + 2^{-1/2}S_2)^{-1} = \sum_{j \ge 0}(-1)^j 2^{-j/2}S_2^j$ gives, for every $X > 0$:
   $$\boxed{Q_{a_2}(X) = \sum_{j\ge 0}(-1)^j 2^{-j/2}\Bigl(Q_{\mathbf{1}}(X/2^j) - 2^{-1/2}Q_{\mathbf{1}}(X/2^{j+1})\Bigr) = Q_{\mathbf{1}}(X) + 2\sum_{k\ge 1}(-1)^k 2^{-k/2}Q_{\mathbf{1}}(X/2^k).}$$
   *(Checked directly in `Q_a2_rows`: `direct_minus_dyadic_coeff_2_consistency` encloses $0$ across all $X \in \{1, 2, 4, 8, 16, 32, 64\}$, whereas substituting $\sqrt{2}$ for $2$ fails with discrepancy $[0.061942 \pm 5.56 \times 10^{-7}]$ <!-- tc-enclosure: observable="erroneous_sqrt2_dyadic_series_discrepancy" params="X=1;L_eq_floor_log2_X=0" json_path="section_12_tc055_multiplicative_parity_controls.Q_a2_rows[X=1].erroneous_sqrt2_dyadic_series_discrepancy" --> already at $X = 1$.)*
3. **Complete four-part derivation of $C_{a_2} = 17 + \frac{16}{7}\zeta(3)$ for all $X \ge 1$ (including $L = 0$)**:
   Using the proved second-order Euler–Maclaurin remainder $R_{\mathbf{1}}(w) := Q_{\mathbf{1}}(w) - \frac{\sqrt{w}}{2}$ satisfying $|R_{\mathbf{1}}(w)| \le 3 w^{-3/2}$ for all $w > 0$, together with $|Q_{\mathbf{1}}(w)| \le \zeta(3)w^{5/2}$ for all $w > 0$, observe that $(-1)^k 2^{-k/2}\frac{\sqrt{X/2^k}}{2} = \frac{\sqrt{X}}{2}(-1)^k 2^{-k}$ and $\sum_{k\ge 1}(-1)^k 2^{-k} = \frac{-1/2}{1 - (-1/2)} = -\frac{1}{3}$, so the main terms sum to $\frac{\sqrt{X}}{2} + 2\cdot\frac{\sqrt{X}}{2}\left(-\frac{1}{3}\right) = \left(\frac{1}{2} - \frac{1}{3}\right)\sqrt{X} = \frac{\sqrt{X}}{6}$.
   Now fix any $X \ge 1$ and set $L := \lfloor \log_2 X \rfloor \ge 0$ (so $2^L \le X < 2^{L+1}$, meaning $2^{-L} \le 2/X$ and $2^{L+1} > X$; when $1 \le X < 2$, $L = 0$ and the sum over $1 \le k \le L$ is empty and equals $0$):
   $$Q_{a_2}(X) - \frac{\sqrt{X}}{6} = R_{\mathbf{1}}(X) + 2\sum_{k=1}^{L}(-1)^k 2^{-k/2}R_{\mathbf{1}}(X/2^k) - \sqrt{X}\sum_{k = L+1}^{\infty}(-1)^k 2^{-k} + 2\sum_{k = L+1}^{\infty}(-1)^k 2^{-k/2}Q_{\mathbf{1}}(X/2^k).$$
   Bounding each of the four pieces explicitly for every $X \ge 1$ (including $L = 0$):
   - **$k = 0$ error**:
     $$\bigl|R_{\mathbf{1}}(X)\bigr| \le 3 X^{-3/2} \le 3 X^{-1/2} \qquad (\text{since } X \ge 1 \implies X^{-3/2} \le X^{-1/2}).$$
   - **Large-scale error ($1 \le k \le L$)**: When $L = 0$, the sum is empty ($= 0 \le 12 X^{-1/2}$). When $L \ge 1$, $|R_{\mathbf{1}}(X/2^k)| \le 3(X/2^k)^{-3/2} = 3 \cdot 2^{3k/2} X^{-3/2}$, so with coefficient $2$:
     $$\left|2\sum_{k=1}^{L}(-1)^k 2^{-k/2}R_{\mathbf{1}}(X/2^k)\right| \le 6 X^{-3/2}\sum_{k=1}^{L} 2^k = 6 X^{-3/2}\bigl(2^{L+1} - 2\bigr) < 6 X^{-3/2}\cdot 2^{L+1} \le 12 X^{-1/2},$$
     since $2^L \le X \implies 2^{L+1} \le 2X$.
   - **Omitted main-term tail ($k \ge L + 1$)**: The alternating geometric series $\sum_{k=L+1}^\infty (-1)^k 2^{-k}$ has alternating terms of strictly decreasing magnitude, so its magnitude is bounded by its first term $2^{-(L+1)}$ (or even $\frac{2^{-(L+1)}}{1 + 1/2} = \frac{2}{3}2^{-(L+1)} \le 2^{-(L+1)}$; conservatively using $\sum_{k\ge L+1}2^{-k} = 2^{-L} \le 2/X$):
     $$\left|-\sqrt{X}\sum_{k = L+1}^{\infty}(-1)^k 2^{-k}\right| \le \sqrt{X}\sum_{k = L+1}^{\infty} 2^{-k} = \sqrt{X}\,2^{-L} \le \sqrt{X}\cdot\frac{2}{X} = 2 X^{-1/2} \qquad (\text{valid for all } L \ge 0,\text{ since } 2^L > X/2 \implies 2^{-L} < 2/X).$$
   - **Small-scale tail ($k \ge L + 1$)**: Using $|Q_{\mathbf{1}}(w)| \le \zeta(3)w^{5/2}$ at $w = X/2^k$ with coefficient $2$:
     $$\left|2\sum_{k = L+1}^{\infty}(-1)^k 2^{-k/2}Q_{\mathbf{1}}(X/2^k)\right| \le 2\zeta(3)X^{5/2}\sum_{k = L+1}^{\infty} 2^{-3k} = 2\zeta(3)X^{5/2}\,\frac{2^{-3(L+1)}}{1 - 2^{-3}} = \frac{16\zeta(3)}{7}\,X^{5/2}\,2^{-3(L+1)} < \frac{16\zeta(3)}{7}\,X^{-1/2},$$
     since $2^{L+1} > X \implies 2^{-3(L+1)} < X^{-3}$ for all $L \ge 0$ (including $L = 0$, where $2^1 = 2 > X \ge 1$).
   Adding all four bounds gives, for every real $X \ge 1$:
   $$\boxed{\left|Q_{a_2}(X) - \frac{\sqrt{X}}{6}\right| \le C_{a_2}\,X^{-1/2}, \qquad C_{a_2} := 3 + 12 + 2 + \frac{16}{7}\zeta(3) = 17 + \frac{16}{7}\zeta(3) \in \bigl[19.74755863579335836662797294059759997889 \pm 1.40 \times 10^{-39}\bigr],}$$ <!-- tc-enclosure: observable="explicit_C_a2_constant" params="" json_path="section_12_tc055_multiplicative_parity_controls.unimodal_and_second_order_euler_maclaurin_constants.second_order_euler_maclaurin_recovery.explicit_C_a2_constant" -->
   where $\frac{16}{7}\zeta(3) \in [2.747558635793358366627972940597599978891 \pm 3.98 \times 10^{-40}]$ <!-- tc-enclosure: observable="c_small_scale_tail_k_gt_L" params="" json_path="section_12_tc055_multiplicative_parity_controls.unimodal_and_second_order_euler_maclaurin_constants.second_order_euler_maclaurin_recovery.component_constants.c_small_scale_tail_k_gt_L" -->.
   *(Audit note: `TASK-TC-055R2` invalidates and retires the prior `TC-055R` derivation of `14.84231228`, which substituted $\sqrt{2}$ for the coefficient $2$ in the last three terms; this audit invalidates that derivation without claiming the numerical value `14.84231228` is false as an upper bound on $|Q_{a_2}(X) - \sqrt{X}/6|X^{1/2}$.)*
4. **Derived energy error for $E_{a_2}(Y)$ from the pointwise remainder (`TASK-TC-055R2` §4)**:
   Write $Q_{a_2}(X) = \frac{\sqrt{X}}{6} + R_{a_2}(X)$ with $|R_{a_2}(X)| \le C_{a_2} X^{-1/2}$ for all $X \ge 1$. Squaring and integrating against $\frac{dX}{X}$ over $[Y, \tau Y]$ for any $Y \ge 1$:
   $$\int_Y^{\tau Y}\left(\frac{\sqrt{X}}{6}\right)^2\frac{dX}{X} = \frac{\tau - 1}{36}\,Y, \qquad \left|E_{a_2}(Y) - \frac{\tau - 1}{36}\,Y\right| \le \int_Y^{\tau Y}\left(\frac{\sqrt{X}}{3}\,\bigl|R_{a_2}(X)\bigr| + \bigl|R_{a_2}(X)\bigr|^2\right)\frac{dX}{X}$$
   $$\le \frac{C_{a_2}}{3}\int_Y^{\tau Y}\frac{dX}{X} + C_{a_2}^2\int_Y^{\tau Y}X^{-2}\,dX = \frac{C_{a_2}\log\tau}{3} + C_{a_2}^2\bigl(1 - \tau^{-1}\bigr)Y^{-1} \le \frac{C_{a_2}\log\tau}{3} + C_{a_2}^2\bigl(1 - \tau^{-1}\bigr) \qquad (\forall Y \ge 1),$$
   with uniform $O(1)$ cap $\frac{C_{a_2}\log\tau}{3} + C_{a_2}^2(1 - \tau^{-1}) \in [339.9989057768068180181010280796024761158 \pm 1.72 \times 10^{-38}]$ <!-- tc-enclosure: observable="explicit_C_E_a2_uniform_O1_cap_for_Y_ge_1" params="" json_path="section_12_tc055_multiplicative_parity_controls.unimodal_and_second_order_euler_maclaurin_constants.second_order_euler_maclaurin_recovery.explicit_C_E_a2_uniform_O1_cap_for_Y_ge_1" --> and leading slope $\frac{\tau - 1}{36} \in [0.1467551474216551799145912990710834935665 \pm 9.42 \times 10^{-42}]$ <!-- tc-enclosure: observable="tau_minus_1_over_36" params="" json_path="section_12_tc055_multiplicative_parity_controls.asymptotic_formulas.tau_minus_1_over_36" -->, unconditionally proving:
   $$\boxed{Q_{a_2}(X) = \frac{\sqrt{X}}{6} + O\bigl(X^{-1/2}\bigr) \quad (X \ge 1), \qquad E_{a_2}(Y) = \frac{\tau - 1}{36}\,Y + O(1) \quad (Y \ge 1).}$$

### 7.2 Scoped Multi-Prime Parity Control $S = \{3, 5, 7\}$ (`TASK-TC-055R2` §4)

For $S = \{3, 5, 7\}$, the Euler-factor mean of $a_{\{3,5,7\}}(n) = (-1)^{v_3(n)+v_5(n)+v_7(n)}$ (residue of $D_{a_S}(s) = \zeta(s)\prod_{p \in S}\frac{1 - p^{-s}}{1 + p^{-s}}$ at its simple pole $s = 1$) is
$$\prod_{p \in \{3, 5, 7\}}\frac{p - 1}{p + 1} = \frac{2}{4}\cdot\frac{4}{6}\cdot\frac{6}{8} = \frac{1}{4}.$$
Multiplying by $\int_0^\infty t^{-3}e^{-1/t^2}\,dt = \frac{1}{2}$ yields the leading asymptotics as $X, Y \to \infty$:
$$\boxed{Q_{a_{\{3,5,7\}}}(X) \sim \frac{1}{8}\sqrt{X}, \qquad E_{a_{\{3,5,7\}}}(Y) \sim \frac{\tau - 1}{64}\,Y,}$$
where $\frac{\tau - 1}{64} \in [0.08254977042468103870195760572748446513116 \pm 1.55 \times 10^{-42}]$ <!-- tc-enclosure: observable="leading_E_aS_over_Y_coefficient" params="leading_Q_aS_over_sqrt_X_coefficient=1/8" json_path="section_12_tc055_multiplicative_parity_controls.asymptotic_formulas.control_S_3_5_7.leading_E_aS_over_Y_coefficient" --> (at the certified sample $X = 64$, $Q_{a_{\{3,5,7\}}}(64)/\sqrt{64} \in [0.122 \pm 6.06 \times 10^{-4}]$ <!-- tc-enclosure: observable="ratio_Q_a_357_over_sqrt_64" params="leading_Q_aS_over_sqrt_X_coefficient=1/8" json_path="section_12_tc055_multiplicative_parity_controls.asymptotic_formulas.control_S_3_5_7.ratio_Q_a_357_over_sqrt_64" -->).
*(Scope note: Unproved stronger $O(X^{-1/2})$ and $O(1)$ multi-prime error assertions have been removed everywhere; only the proved mean $\frac{1}{4}$ and leading asymptotics $Q_{a_{\{3,5,7\}}}(X) \sim \frac{1}{8}\sqrt{X}$, $E_{a_{\{3,5,7\}}}(Y) \sim \frac{\tau - 1}{64}Y$ are claimed.)*

---

## 8. Full Lean Finite Reconstruction, Repaired Weighted Cofactor Decomposition, and Independent Fiber Verification (`TASK-TC-055R2` §2, §3 & §8)

### 8.1 Full Finite Reconstruction and Exact Uncoupled-Cutoff Excess in Lean 4 (`TASK-TC-055R2` §3 & §8)

For $X > 0$, integer $T \ge 0$, finite prime set $P \subset \mathbb{P}$ ($N_P := \prod_{p\in P}p$, $\mathcal{S}(P) := \{m \ge 1 : p \mid m \implies p \in P\}$), and integer $L \ge 0$, define the finite observables explicitly:
$$Q_{\lambda, T}(X) := X^{5/2}\sum_{1 \le n \le T}\frac{\lambda(n)}{n^3}e^{-X^2/n^2}, \qquad Q_{\lambda, P, L}(w) := w^{5/2}\sum_{\substack{1 \le r \le L \\ \gcd(r, N_P)=1}}\frac{\lambda(r)}{r^3}e^{-w^2/r^2},$$
$$\boxed{Q_{\lambda, \mathcal{S}(P), L}(w) := w^{5/2}\sum_{\substack{1 \le m \le L \\ m \in \mathcal{S}(P)}}\frac{\lambda(m)}{m^3}e^{-w^2/m^2} \qquad (w > 0,\; L \in \mathbb{Z}_{\ge 0}).}$$
*(Convention at $T = 0$ or $L = 0$: the index range $\{1, \dots, 0\}$ is empty, so $Q_{\lambda, 0}(X) = Q_{\lambda, P, 0}(w) = Q_{\lambda, \mathcal{S}(P), 0}(w) = 0$.)*

**Theorem 8.1 (Lean-Formalized Smooth–Coprime Bijection, Arbitrary-Weight Reindexing, Exact Excess Sum, and Two-Sided $L^2$ Transfer).**
1. **Unique positive smooth–coprime factorization (`smooth_coprime_positive_factorization_exists_unique_nat`)**:
   For every finite prime set $P$ (including $P = \varnothing$, where $N_\varnothing = 1$ and $\mathcal{S}(\varnothing) = \{1\}$) and every integer $n \ge 1$, there exist unique positive integers $m, r \ge 1$ such that $m \in \mathcal{S}(P)$, $\gcd(r, N_P) = 1$, and $n = m r$ (constructed explicitly via $m = \prod_{p \in P} p^{v_p(n)}$).
2. **Finite cutoff indexing bijection (`finite_smooth_coprime_cutoff_indexing_bijection_nat`)**:
   For every $T \ge 0$ (including $T = 0$, $T = 1$, $P = \varnothing$, and empty inner sums), $(m, r) \mapsto m r$ is a bijection between $\{(m, r) : m \in \mathcal{S}(P),\; m \le T,\; 1 \le r \le \lfloor T/m \rfloor,\; \gcd(r, N_P) = 1\}$ and $\{1 \le n \le T\}$, with $m r \le T \iff r \le \lfloor T/m \rfloor$ for $m \ge 1$.
3. **Arbitrary-weight reindexed Liouville sum and exact uncoupled-cutoff excess (`finite_liouville_reindexed_sum_and_excess_cutoff_identity_nat`)**:
   For any real weight $w : \mathbb{N} \to \mathbb{R}$ and any $T \ge 0$,
   $$\boxed{\sum_{1 \le n \le T}\lambda(n)w(n) = \sum_{\substack{m \le T \\ m \in \mathcal{S}(P)}}\sum_{\substack{1 \le r \le \lfloor T/m \rfloor \\ \gcd(r, N_P)=1}}\lambda(m)\lambda(r)w(m r) = \sum_{\substack{1 \le r \le T \\ \gcd(r, N_P)=1}}\sum_{\substack{m \le \lfloor T/r \rfloor \\ m \in \mathcal{S}(P)}}\lambda(r)\lambda(m)w(m r).}$$
   Replacing the coupled inner cutoff $r \le \lfloor T/m \rfloor$ by the uncoupled cutoff $r \le T$ adds the **exact excess sum**
   $$\mathcal{E}_{\mathrm{uncoupled}}(T, P; w) := \sum_{\substack{m \le T \\ m \in \mathcal{S}(P)}}\sum_{\substack{\lfloor T/m \rfloor < r \le T \\ \gcd(r, N_P)=1}}\lambda(m)\lambda(r)w(m r),$$
   which is **not** universally nonzero: it vanishes identically when $P = \varnothing$, when $T \le 1$, or at $(P = \{2\}, T = 2)$ (where $m = 2 \implies \lfloor 2/2 \rfloor = 1$ and $r = 2$ has $\gcd(2, 2) = 2 \ne 1$, so the excess index set is empty), and can also vanish by sign cancellation on nonempty excess sets (e.g. at $T = 5, P = \{2\}, w \equiv 1$, where the 4 excess pairs $(2,3), (2,5), (4,3), (4,5)$ give $+1 + 1 - 1 - 1 = 0$), whereas at $(P = \{2\}, T = 3)$ it equals $+w(6) > 0$ for every strictly positive weight $w$ (and is certified strictly nonzero in 256-bit Arb for the Gaussian observable at $(T, P, X) \in \{(3, \{2\}, 4), (24, \{2,3\}, 4), (36, \{2,3,5\}, 6), (50, \{2,3,5,7\}, 8)\}$).
4. **Gaussian observable instantiation by $m$ and by $r$ (`finite_gaussian_observable_reconstruction_and_weighted_cofactor_square`)**:
   Deriving the scaling directly from $X^{5/2}$ and $(m r)^{-3}$ for $X > 0$, $m \ge 1$, $r \ge 1$:
   $$X^{5/2}\,\frac{\lambda(m r)}{(m r)^3}\,e^{-X^2/(m r)^2} = \frac{\lambda(m)}{\sqrt{m}}\left(\frac{X}{m}\right)^{5/2}\frac{\lambda(r)}{r^3}\,e^{-(X/m)^2/r^2} = \frac{\lambda(r)}{\sqrt{r}}\left(\frac{X}{r}\right)^{5/2}\frac{\lambda(m)}{m^3}\,e^{-(X/r)^2/m^2},$$
   because $m^{-1/2}(X/m)^{5/2}r^{-3} = X^{5/2}m^{-3}r^{-3} = r^{-1/2}(X/r)^{5/2}m^{-3}$. Summing over the bijection of part (2) gives both exact finite reconstructions:
   $$\boxed{Q_{\lambda, T}(X) = \sum_{\substack{m \le T \\ m \in \mathcal{S}(P)}}\frac{\lambda(m)}{\sqrt{m}}\,Q_{\lambda, P, \lfloor T/m \rfloor}(X/m) = \sum_{\substack{1 \le r \le T \\ \gcd(r, N_P)=1}} F_r(X), \qquad F_r(X) := \frac{\lambda(r)}{\sqrt{r}}\,Q_{\lambda, \mathcal{S}(P), \lfloor T/r \rfloor}(X/r).}$$
5. **Exact integer-power cutoff $T(Y) = \lceil Y^{5/4} \rceil$ and two-sided squared $L^2$ transfer (`TASK-TC-055R2` §5 & §8)**:
   For real $Y \ge 1$, `exact_ceil_five_fourths_power` characterizes $T(Y) := \lceil Y^{5/4} \rceil$ without floating-point exponentiation by the exact integer-power predicate
   $$(T - 1)^4 < Y^5 \le T^4 \qquad (Y \ge 1,\; T \in \mathbb{Z}_{\ge 1}),$$
   giving in particular $T(1) = 1$ (explicitly distinct from the companion prime-sieve schedule $M(Y) := \lceil \max(2, Y^{5/4}) \rceil = \max(2, T(Y))$ where $M(1) = 2$), and verified across exact fourth powers and $\pm 2^{-100}$ perturbations $Y \in \{1, 1 + 2^{-100}, 16 \pm 2^{-100}, 16, 81 \pm 2^{-100}, 81\}$. Since $|Q_\lambda(X) - Q_{\lambda, T}(X)| \le \frac{X^{5/2}}{2T^2}$ for integer $T \ge 1$,
   $$\boxed{\mathcal{R}_{\mathrm{tail}}(Y, T) := \int_Y^{\tau Y}\bigl|Q_\lambda(X) - Q_{\lambda, T}(X)\bigr|^2\,\frac{dX}{X} \le \frac{(\tau^5 - 1)Y^5}{20\,T^4},}$$
   which at $T = T(Y)$ satisfies $T(Y)^4 \ge Y^5$ and hence $\mathcal{R}_{\mathrm{tail}}(Y, T(Y)) \le \frac{\tau^5 - 1}{20} \in [489.5814956564503252203860960694969703685 \pm 1.89 \times 10^{-38}]$ <!-- tc-enclosure: observable="uniform_O1_cap_tau5_minus_1_over_20" params="Y=1;T=1" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.finite_truncation_tail_energy_and_L2_transfer.rows[Y=1,T=1].uniform_O1_cap_tau5_minus_1_over_20" --> $= O(1)$ for every $Y \ge 1$. By $\|f \pm g\|_{L^2}^2 \le 2\|f\|_{L^2}^2 + 2\|g\|_{L^2}^2$, **both directions** of the squared $L^2$ transfer hold for all $Y \ge 1$ and $T \ge 1$:
   $$\boxed{E_\lambda(Y) \le 2 E_{\lambda, T}(Y) + 2\mathcal{R}_{\mathrm{tail}}(Y, T) \quad\text{and}\quad E_{\lambda, T}(Y) \le 2 E_\lambda(Y) + 2\mathcal{R}_{\mathrm{tail}}(Y, T).}$$
   Hence $\bigl(\forall \varepsilon > 0,\; E_\lambda(Y) \ll_\varepsilon Y^\varepsilon\bigr) \Longleftrightarrow \bigl(\forall \varepsilon > 0,\; E_{\lambda, T(Y)}(Y) \ll_\varepsilon Y^\varepsilon\bigr)$.

### 8.2 Repaired Weighted Cofactor Energy Decomposition and Independent Smooth-Fiber Regression (`TASK-TC-055R2` §2)

**Theorem 8.2 (Weighted Cofactor Energy Decomposition $E_{\lambda, T} = E_{\mathrm{same}\text{-}r} + E_{\mathrm{diff}\text{-}r}$).**
For $X > 0$, $Y \ge 1$, integer $T \ge 1$, and finite prime set $P \subset \mathbb{P}$, all observables $Q_{\lambda, T}(X)$ and $Q_{\lambda, \mathcal{S}(P), \lfloor T/r \rfloor}(X/r)$ are **real-valued**. Squaring $Q_{\lambda, T}(X) = \sum_{\substack{1 \le r \le T \\ \gcd(r, N_P)=1}}\frac{\lambda(r)}{\sqrt{r}}\,Q_{\lambda, \mathcal{S}(P), \lfloor T/r \rfloor}(X/r)$ pointwise and using $\lambda(r)^2 = 1$ yields
$$\bigl|Q_{\lambda, T}(X)\bigr|^2 = \sum_{\substack{1 \le r \le T \\ \gcd(r, N_P)=1}}\frac{1}{r}\bigl|Q_{\lambda, \mathcal{S}(P), \lfloor T/r \rfloor}(X/r)\bigr|^2 + \sum_{\substack{r \ne s,\; 1 \le r, s \le T \\ \gcd(r s, N_P)=1}}\frac{\lambda(r)\lambda(s)}{\sqrt{r s}}\,Q_{\lambda, \mathcal{S}(P), \lfloor T/r \rfloor}(X/r)\,Q_{\lambda, \mathcal{S}(P), \lfloor T/s \rfloor}(X/s)$$
*(formalized pointwise in Lean 4 theorem `finite_gaussian_observable_reconstruction_and_weighted_cofactor_square`; note that $\gcd(r, N_P) = 1 \wedge \gcd(s, N_P) = 1 \iff \gcd(r s, N_P) = 1$)*. Integrating this finite sum over $X \in [Y, \tau Y]$ against $\frac{dX}{X}$ by finite linearity of the Riemann/Lebesgue integral gives:
$$\boxed{E_{\lambda, T}(Y) = E_{\mathrm{same}\text{-}r}(Y; T, P) + E_{\mathrm{diff}\text{-}r}(Y; T, P),}$$
where:
$$\boxed{E_{\mathrm{same}\text{-}r}(Y; T, P) := \sum_{\substack{1 \le r \le T \\ \gcd(r, N_P)=1}}\frac{1}{r}\int_Y^{\tau Y}\bigl|Q_{\lambda, \mathcal{S}(P), \lfloor T/r \rfloor}(X/r)\bigr|^2\,\frac{dX}{X} \ge 0,}$$
$$\boxed{E_{\mathrm{diff}\text{-}r}(Y; T, P) := \sum_{\substack{r \ne s,\; 1 \le r, s \le T \\ \gcd(r s, N_P)=1}}\frac{\lambda(r)\lambda(s)}{\sqrt{r s}}\int_Y^{\tau Y}Q_{\lambda, \mathcal{S}(P), \lfloor T/r \rfloor}(X/r)\,Q_{\lambda, \mathcal{S}(P), \lfloor T/s \rfloor}(X/s)\,\frac{dX}{X},}$$
with **ordered** coprime pairs $r \ne s$ in the displayed cross sum; written over **unordered** pairs $1 \le r < s \le T$ ($\gcd(r s, N_P) = 1$), symmetry of the real integrand introduces an explicit factor of $2$:
$$E_{\mathrm{diff}\text{-}r}(Y; T, P) = 2\sum_{\substack{1 \le r < s \le T \\ \gcd(r s, N_P)=1}}\frac{\lambda(r)\lambda(s)}{\sqrt{r s}}\int_Y^{\tau Y}Q_{\lambda, \mathcal{S}(P), \lfloor T/r \rfloor}(X/r)\,Q_{\lambda, \mathcal{S}(P), \lfloor T/s \rfloor}(X/s)\,\frac{dX}{X}$$
(for complex-valued generalizations, the summand uses $\overline{Q_r(X/r)}Q_s(X/s)$ for ordered pairs $r \ne s$, or $2\operatorname{Re}[\overline{Q_r(X/r)}Q_s(X/s)]$ for unordered pairs $r < s$).

**Independent Smooth-Fiber Quadrature Verification & Omitted-Weight Regression at $(Y = 4, T = 6, P = \{2, 3\})$**:
In `evaluate_weighted_cofactor_energy_independent_fibers_arb`, each fiber integral $\int_Y^{\tau Y} Q_{\lambda, \mathcal{S}(P), \lfloor T/r \rfloor}(X/r)\,Q_{\lambda, \mathcal{S}(P), \lfloor T/s \rfloor}(X/s)\,\frac{dX}{X}$ is integrated directly by certified `acb.integral` Gauss–Legendre quadrature of `evaluate_Q_lambda_S_P_smooth_finite_L_certified_arb` without referencing `K_Y(m, n)`. At $Y = 4, T = 6, P = \{2, 3\}$ (coprime cofactors $r \in \{1, 5\}$, where $r = 5$ carries weight $\frac{1}{5}$ in $E_{\mathrm{same}\text{-}r}$ and $-\frac{1}{\sqrt{5}}$ in $E_{\mathrm{diff}\text{-}r}$):
- **Correct weighted $E_{\mathrm{same}\text{-}r}(4; 6, \{2, 3\})$ (independent smooth-fiber quadrature)**:
  $$[0.04878927689438566504682432312715229376034 \pm 1.21 \times 10^{-42}]$$ <!-- tc-enclosure: observable="weighted_E_same_r_independent_fiber_quadrature" params="Y=4;T=6" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.weighted_cofactor_regression_Y4_T6_P_2_3.weighted_E_same_r_independent_fiber_quadrature" -->
  (matching kernel-matrix grouping $[0.04878927689438566504682432312715229376034 \pm 1.21 \times 10^{-42}]$ <!-- tc-enclosure: observable="weighted_E_same_r_kernel_grouping" params="Y=4;T=6" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.weighted_cofactor_regression_Y4_T6_P_2_3.weighted_E_same_r_kernel_grouping" --> with consistency residual `[+/- 5.67e-78]` <!-- tc-enclosure: observable="kernel_minus_independent_fiber_consistency" params="Y=4;T=6" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.weighted_cofactor_regression_Y4_T6_P_2_3.kernel_minus_independent_fiber_consistency" -->).
- **Erroneous unweighted expression omitting $\frac{1}{r}$**:
  $$\sum_{r \in \{1, 5\}}\int_4^{4\tau}\bigl|Q_{\lambda, \mathcal{S}(\{2,3\}), \lfloor 6/r \rfloor}(X/r)\bigr|^2\,\frac{dX}{X} \in [0.1209268815654658371618758542627537258713 \pm 4.43 \times 10^{-41}],$$ <!-- tc-enclosure: observable="erroneous_unweighted_E_same_r_omitting_1_over_r" params="Y=4;T=6" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.weighted_cofactor_regression_Y4_T6_P_2_3.erroneous_unweighted_E_same_r_omitting_1_over_r" -->
  differing from the true weighted value by outward-certified discrepancy $\frac{4}{5}\int_4^{4\tau}|Q_{\lambda,\mathcal{S}(\{2,3\}),1}(X/5)|^2\frac{dX}{X} \in [0.07213760467108017211505153113560143211091 \pm 4.59 \times 10^{-42}]$ <!-- tc-enclosure: observable="unweighted_minus_weighted_discrepancy" params="Y=4;T=6" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.weighted_cofactor_regression_Y4_T6_P_2_3.unweighted_minus_weighted_discrepancy" --> $> 0.0721$.
- **Correct weighted $E_{\mathrm{diff}\text{-}r}(4; 6, \{2, 3\})$ vs. erroneous unweighted cross sum omitting $\frac{1}{\sqrt{r s}}$**:
  $$[-0.04418064358166290908242957009073668046372 \pm 4.86 \times 10^{-42}]$$ <!-- tc-enclosure: observable="weighted_E_diff_r_ordered_independent_fiber" params="Y=4;T=6" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.weighted_cofactor_regression_Y4_T6_P_2_3.weighted_E_diff_r_ordered_independent_fiber" -->
  vs. erroneous unweighted cross sum $[-0.09879092233828804585072442756377431406783 \pm 2.98 \times 10^{-42}]$ <!-- tc-enclosure: observable="erroneous_unweighted_E_diff_r_omitting_1_over_sqrt_rs" params="Y=4;T=6" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.weighted_cofactor_regression_Y4_T6_P_2_3.erroneous_unweighted_E_diff_r_omitting_1_over_sqrt_rs" -->.

| $Y$ | $T(Y) = \lceil Y^{5/4} \rceil$ | $P_u$ | Signed $E_{\lambda, T(Y)}(Y)$ (256-Bit Arb) | Unsigned $E_{\mathrm{unsigned}, T(Y)}(Y)$ (256-Bit Arb) | Weighted $E_{\mathrm{same}\text{-}r}$ (Indep. Fiber Arb) | Weighted $E_{\mathrm{diff}\text{-}r}$ (Indep. Fiber Arb) |
| :---: | :---: | :---: | :--- | :--- | :--- | :--- |
| `4` | `6` | `{2, 3}` | `[0.004608633312722755964394753036415613296616 +/- 3.52e-43]` <!-- tc-enclosure: observable="E_signed_T_Y" params="Y=4;T_eq_ceil_Y_5_4=6" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.rows[Y=4].E_signed_T_Y" --> | `[0.2229338930925055337199205455198700527881 +/- 3.12e-42]` <!-- tc-enclosure: observable="E_unsigned_T_Y" params="Y=4;T_eq_ceil_Y_5_4=6" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.rows[Y=4].E_unsigned_T_Y" --> | `[0.04878927689438566504682432312715229376034 +/- 1.21e-42]` <!-- tc-enclosure: observable="E_same_r_independent_weighted_fiber_quadrature" params="Y=4;T_eq_ceil_Y_5_4=6" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.rows[Y=4].E_same_r_independent_weighted_fiber_quadrature" --> | `[-0.04418064358166290908242957009073668046372 +/- 4.86e-42]` <!-- tc-enclosure: observable="E_diff_r_independent_weighted_fiber_ordered" params="Y=4;T_eq_ceil_Y_5_4=6" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.rows[Y=4].E_diff_r_independent_weighted_fiber_ordered" --> |
| `8` | `14` | `{2, 3, 5}` | `[0.01628064423617857591478454843047804761284 +/- 2.05e-42]` <!-- tc-enclosure: observable="E_signed_T_Y" params="Y=8;T_eq_ceil_Y_5_4=14" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.rows[Y=8].E_signed_T_Y" --> | `[0.6133315943098280111202482635113438651676 +/- 2.45e-41]` <!-- tc-enclosure: observable="E_unsigned_T_Y" params="Y=8;T_eq_ceil_Y_5_4=14" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.rows[Y=8].E_unsigned_T_Y" --> | `[0.02536677420434105493102096192954450773955 +/- 7.11e-43]` <!-- tc-enclosure: observable="E_same_r_independent_weighted_fiber_quadrature" params="Y=8;T_eq_ceil_Y_5_4=14" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.rows[Y=8].E_same_r_independent_weighted_fiber_quadrature" --> | `[-0.009086129968162479016236413499066460126709 +/- 3.36e-43]` <!-- tc-enclosure: observable="E_diff_r_independent_weighted_fiber_ordered" params="Y=8;T_eq_ceil_Y_5_4=14" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.rows[Y=8].E_diff_r_independent_weighted_fiber_ordered" --> |
| `12` | `23` | `{2, 3, 5, 7}` | `[0.02008761677818477787815712162881096441858 +/- 2.74e-42]` <!-- tc-enclosure: observable="E_signed_T_Y" params="Y=12;T_eq_ceil_Y_5_4=23" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.rows[Y=12].E_signed_T_Y" --> | `[1.130968271229071832411352715272616235617 +/- 4.51e-40]` <!-- tc-enclosure: observable="E_unsigned_T_Y" params="Y=12;T_eq_ceil_Y_5_4=23" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.rows[Y=12].E_unsigned_T_Y" --> | `[0.04604404794761902815621552489743255339503 +/- 2.20e-42]` <!-- tc-enclosure: observable="E_same_r_independent_weighted_fiber_quadrature" params="Y=12;T_eq_ceil_Y_5_4=23" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.rows[Y=12].E_same_r_independent_weighted_fiber_quadrature" --> | `[-0.02595643116943425027805840326862158897645 +/- 4.93e-42]` <!-- tc-enclosure: observable="E_diff_r_independent_weighted_fiber_ordered" params="Y=12;T_eq_ceil_Y_5_4=23" json_path="section_13_tc055r_finite_truncation_and_signed_energy_attempt.signed_energy_attempt_on_finite_reconstruction.rows[Y=12].E_diff_r_independent_weighted_fiber_ordered" --> |

**Diagnosis & Preservation of the Combined Signed Target (`TASK-TC-055R2` §8)**:
- The three numerical rows above are finite certified sample evaluations (with kernel-vs-independent-fiber overlap serving strictly as a consistency check); they do **not** determine the sign of $E_{\mathrm{diff}\text{-}r}(Y; T(Y), P_u)$ for general $Y$, nor do they constitute a uniform cancellation theorem.
- Crucially, the surviving research target **retains the combined signed sum**
  $$\boxed{\forall \varepsilon > 0\;\exists C_\varepsilon < \infty\;\forall Y \ge 1, \qquad 0 \le E_{\lambda, T(Y)}(Y) = E_{\mathrm{same}\text{-}r}(Y; T(Y), P) + E_{\mathrm{diff}\text{-}r}(Y; T(Y), P) \le C_\varepsilon Y^\varepsilon,}$$
  without discarding cross-cofactor terms or replacing the sum by $|E_{\mathrm{same}\text{-}r}| + |E_{\mathrm{diff}\text{-}r}|$ (notice at $Y = 4$ that $E_{\mathrm{same}\text{-}r} \approx 0.04879$ and $E_{\mathrm{diff}\text{-}r} \approx -0.04418$ cancel by more than $90\%$ down to $E_{\lambda, 6}(4) \approx 0.00461$).
- For any fixed finite prime set $P_u$, $D_{\mathcal{S}(P_u)}(s) = \prod_{p \le u}(1 + p^{-s})^{-1}$ is holomorphic on $\operatorname{Re} s > 0$, giving a fixed-$u$ power saving $O_{u,\eta}(w^\eta)$ on individual untruncated smooth fibers with uncontrolled $u$-dependent constant. Promoting this to an unconditional bound in $Y$ encounters the exact two-part obstruction: (1) taking $u \ge T(Y)$ forces $r = 1$ ($E_{\mathrm{diff}\text{-}r} = 0$) but incurs the super-polynomial Kronecker supremum $\prod_{p \le u}(1 - p^{-\eta})^{-1}$ together with the coupled hyperbolic cutoff $\lfloor T(Y)/m \rfloor$; (2) taking $u(Y) \ll (\log Y)^{1/(1-\eta)}$ keeps the smooth Euler-product norm $\le Y^\varepsilon$ but leaves the unfactored primes $p > u$ inside the combined signed sum $E_{\mathrm{same}\text{-}r} + E_{\mathrm{diff}\text{-}r}$.

---

## 9. Five-Category Claim Classification Map and Unchanged Gate Status (`TASK-TC-055R2` §8 & §9)

1. **Unconditional Finite Arithmetic Theorems Proved in Lean 4 (`formal/RiemannScope/LiouvilleSquareDilation.lean`, `0` `sorry`, `0` custom `axiom`)**:
   - `smooth_coprime_positive_factorization_exists_unique_nat`: existence and uniqueness of $n = m r$ ($n \ge 1$) with $m \in \mathcal{S}(P)$ and $\gcd(r, N_P) = 1$ for arbitrary finite prime set $P$ (including $P = \varnothing$).
   - `finite_smooth_coprime_cutoff_indexing_bijection_nat`: finite cutoff bijection $\{1 \le n \le T\} \leftrightarrow \{(m, r) : m \in \mathcal{S}(P),\; m \le T,\; 1 \le r \le \lfloor T/m \rfloor,\; \gcd(r, N_P) = 1\}$ for all $T \ge 0$ (handling $T = 0$, $T = 1$, $P = \varnothing$, and empty inner sums).
   - `finite_liouville_reindexed_sum_and_excess_cutoff_identity_nat`: arbitrary-weight reindexed Liouville sum by $m$ and by $r$, plus the exact uncoupled-cutoff excess sum $\sum_{m \le T, m \in \mathcal{S}(P)}\sum_{\lfloor T/m \rfloor < r \le T, \gcd(r, N_P)=1}\lambda(m)\lambda(r)w(m r)$ (certifying vanishing at $P = \varnothing$, $T \le 1$, and $(P = \{2\}, T = 2)$, and $+w(6)$ at $(P = \{2\}, T = 3)$).
   - `finite_gaussian_observable_reconstruction_and_weighted_cofactor_square`: instantiation to `finiteQLambda`, `finiteQLambdaCoprime`, `finiteQLambdaSmooth`, and `cofactorFiberF` proving $Q_{\lambda, T}(X) = \sum_{m \le T, m \in \mathcal{S}(P)}\frac{\lambda(m)}{\sqrt{m}}Q_{\lambda, P, \lfloor T/m \rfloor}(X/m) = \sum_{1 \le r \le T, \gcd(r, N_P)=1}\frac{\lambda(r)}{\sqrt{r}}Q_{\lambda, \mathcal{S}(P), \lfloor T/r \rfloor}(X/r)$ and the pointwise weighted square identity $(Q_{\lambda, T}(X))^2 = \sum_r \frac{1}{r}Q_r^2 + \sum_{r \ne s}\frac{\lambda(r)\lambda(s)}{\sqrt{r s}}Q_r Q_s$.
   - Prior preserved integer & algebraic theorems (`actual_omega_factorization_and_liouville_common_factor_cancellation_nat`, `actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat`, `actual_finite_prime_exclusion_sieve_identity_nat`, `prime_parity_control_multiplicative_and_moebius_separation_nat`, `abel_scaling_fourier_ratio_and_unequal_block_algebra`, `near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing`, `pairing_counterexample_replacement_and_finite_reconstruction_tc055r`; note that continuous kernel-ratio hypotheses in the latter two remain explicit real-scalar assumptions because Gaussian integration over $[Y, \tau Y]$ is proved analytically outside Lean).
2. **Universal Analytic Proofs Supplied in Review Docs**:
   - Reversible weighted norm equivalence on $\mathcal{H}_\eta$ ($\eta > 0$), non-Schwartz $C^1(\mathbb{R}/\mathbb{Z})$ Poisson summation, Mellin–Barnes DLMF 5.8.3 contour shift, and global Stieltjes bound $E_\lambda(Y) \ll_D Y(\log Y)^{-D}$ ($Y \ge 2$).
   - Exact full-space inverse operator norm $\|\mathcal{P}_u^{-1}\|_{\mathcal{H}_\eta \to \mathcal{H}_\eta} = \prod_{p \le u}(1 - p^{-1/2-\eta})^{-1}$ via $\mathbb{Q}$-linear independence of $\{\log p : p \le u\}$ and continuous Kronecker simultaneous approximation.
   - Floor-guarded and least-prime coprime tail bounds (§4.1), diagonal asymptotic $D_E(Y)$ and near-diagonal band inequality (§5.2–§5.3), two-sided integrand-ratio and bounded-ratio transition relative-gap bounds (§6.2), explicit $C_{a_2} = 17 + \frac{16}{7}\zeta(3)$ pointwise and integrated remainder bounds and $S = \{3, 5, 7\}$ leading asymptotics (§7.1–§7.2), truncation tail energy $\mathcal{R}_{\mathrm{tail}}(Y, T) \le \frac{(\tau^5 - 1)Y^5}{20 T^4}$ with two-sided $L^2$ transfer (§8.1), and integrated weighted cofactor decomposition $E_{\lambda, T}(Y) = E_{\mathrm{same}\text{-}r} + E_{\mathrm{diff}\text{-}r}$ (§8.2).
3. **Certified Numerical Evaluations at Specified Inputs (Outward-Endpoint / Nonnegative-Margin Certified)**:
   - $u = 2.9$ counterexample and exact rational/dyadic boundary tests $u \in \{3 \pm 2^{-100}, 3, 5 \pm 2^{-100}, 5\}$ and $T(Y)$ boundaries $Y \in \{1, 1 + 2^{-100}, 16 \pm 2^{-100}, 16, 81 \pm 2^{-100}, 81\}$;
   - Kronecker witness $b_* = \frac{2513\tau}{2\log 2}$ at $(u = 5, \eta = 1/4)$;
   - Synchronized pairing counterexample $K_{33}(11, 11)$, $K_{33}(10, 11)$ ($0.819425\dots > 0.3993$);
   - Pointwise $C_{a_2}$ and derived $E_{a_2}(Y)$ remainder bounds across $X \in \{1, 2, 4, 8, 16, 32, 64\}$ and $Y \in \{1, 4, 8, 16, 32\}$;
   - Omitted-weight regression at $(Y = 4, T = 6, P = \{2, 3\})$ (`0.048789276894385665...` vs. `0.120926881565465837...`) and nonzero Gaussian excess witnesses.
4. **Algebraic and Numerical Consistency Checks**:
   - Residual-contains-zero / interval-overlap checks between operator products and direct coprime sums, direct $Q_{a_2}$ and its coefficient-$2$ dyadic series, finite reconstructions and direct $Q_{\lambda, T}$, and kernel-matrix cofactor grouping vs. independent `acb.integral` smooth-fiber quadrature (never treated by themselves as proofs of exact equality).
5. **Conditional Implications and Unresolved Target Estimate**:
   - Conditional equivalence: `SUBGATE-TC-043A` $\Longleftrightarrow \bigl(\forall \varepsilon > 0\;\exists C_\varepsilon < \infty\;\forall Y \ge 1,\; 0 \le E_{\lambda, T(Y)}(Y) = E_{\mathrm{same}\text{-}r} + E_{\mathrm{diff}\text{-}r} \le C_\varepsilon Y^\varepsilon\bigr) \Longleftrightarrow \mathrm{RH}$.
   - **Open research obligation**: Proving $\forall \varepsilon > 0\;\exists C_\varepsilon < \infty\;\forall Y \ge 1,\; E_{\lambda, T(Y)}(Y) = E_{\mathrm{same}\text{-}r}(Y; T(Y), P) + E_{\mathrm{diff}\text{-}r}(Y; T(Y), P) \le C_\varepsilon Y^\varepsilon$ uniformly in $Y$. Accordingly, `SUBGATE-TC-043A` remains `OPEN` and `rh_proved` remains `false`.
