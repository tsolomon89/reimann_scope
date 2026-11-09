# TASK-TC-054 / TASK-TC-054R / TASK-TC-054R2 Mathematical Review: Liouville Square-Dilation Transfer, Unconstrained Common-Factor Expansion, Transition Poisson Summation, and Separable Gaussian Decoupling

- **Task ID**: `TASK-TC-054` (repaired in `TASK-TC-054R` and closed out in `TASK-TC-054R2`)
- **Parent Epic**: `EPIC-TC-042`
- **Branch**: `task/tc-054r2-contour-proof-arithmetic-bridge-and-report-closeout`
- **Prior Merged `main` Baseline (`TC-053R`)**: `c82e439708b0b6031db6a77bf3977688d9f0758b`
- **Reviewed `TC-053R2` Implementation Commit**: `cc303030138c670e8f01aaaab483bbeca6bc17d1`
- **Reviewed `TC-053R2` Tip**: `21576861ecd0dcbf874afec91b299fd6060f4f03`
- **Reviewed `TC-054` Implementation Commit**: `8f6afcfb9161aa77c74bc40605ac4fabae8b432e`
- **Reviewed `TC-054` Tip**: `cdee197acc9c3e75a4c8cffc94c10bec1bcb97fa`
- **Reviewed `TC-054R` Implementation Commit**: `27489f195d3313d9ee60773157e3a8240f5bcadd`
- **Reviewed `TC-054R` Tip**: `f265042ab52cabda29e76859cebace21cfae9239`
- **Subgate Status**: `SUBGATE-TC-043A: OPEN` (`rh_proved: false`)
- **Primary Implementation Module**: [`tc/liouville_square_dilation.py`](../../tc/liouville_square_dilation.py)
- **Certified Data Artifact**: [`data/tc_liouville_square_dilation.json`](../../data/tc_liouville_square_dilation.json)
- **Formal Lean 4 Module**: [`formal/RiemannScope/LiouvilleSquareDilation.lean`](../../formal/RiemannScope/LiouvilleSquareDilation.lean) (`21` definitions + `12` public theorems + `16` private helper theorems = `49` declarations; `0` `sorry`, `0` custom `axiom`)
- **Verification Test Suite**: [`tests/test_tc_liouville_square_dilation.py`](../../tests/test_tc_liouville_square_dilation.py)
- **Closeout Report**: [`docs/reviews/TC_054R2_CLOSEOUT_REPORT.md`](TC_054R2_CLOSEOUT_REPORT.md)

---

## 1. Executive Summary, Notation, & Mission Status

Throughout this document we preserve the project's native circle constant $\tau := 2\pi$ and declare complex coordinates explicitly:
- Mellin/Dirichlet complex variables are written $z = a + i b$ with $a, b \in \mathbb{R}$ ($a = \operatorname{Re} z$);
- Nontrivial zeros of $\zeta$ are written $\rho = x + i y$ with $x, y \in \mathbb{R}$ ($x = \operatorname{Re}\rho$), where the critical line is $x = 1/2$;
- Admissible TC grades $K \in \mathbb{A}_{\mathbb{R}} := \overline{\mathbb{Q}} \cap \mathbb{R}$ remain real algebraic, whereas positive real scales $X, Y, M > 0$ and the real norm weight $\eta > 0$ in $\|f\|_\eta := \bigl(\int_0^\infty |f(X)|^2 X^{-2\eta}\frac{dX}{X}\bigr)^{1/2}$ are auxiliary continuum parameters and do not automatically become TC grades.

In `TASK-TC-053R` and `TASK-TC-053R2`, the common-factor expansion of the Möbius Gaussian sum
$$Q_\mu(X) := X^{5/2}\sum_{n\ge 1}\frac{\mu(n)}{n^3}e^{-X^2/n^2}$$
encountered two coupled structural barriers when expanding $Q_\mu(X)^2$ over $m = d r$, $n = d s$ with $\gcd(r, s) = 1$:
1. **Common-Factor Coprimality Barrier ($A \le X^{1/3-\delta}$)**: Because $\mu(d r)\mu(d s) = \mu(d)^2 \mathbf{1}_{\gcd(d, r s)=1}\mu(r)\mu(s)$, the inner sum over $d$ is restricted to squarefree integers $d$ coprime to $q = r s$. Approximating $\sum_{\gcd(d, rs)=1} \mu(d)^2 d^{-6} e^{-L^2/d^2}$ by its continuous integral introduces the squarefree-coprime counting remainder $|R_q(t)| \le (2^{\omega(q)} + 2)\sqrt{t}$, producing an $O(L^{-11/2})$ pairwise error that restricts the asymptotic Gaussian kernel reduction to the sub-cubic range $A \le X^{1/3-\delta}$.
2. **Signed-Block Barrier**: On a single balanced block $[A, 2A)^2$, the decoupled convolution $f = (\mu \otimes \mu) * h$ combined with Korobov–Vinogradov–Walfisz yields the unconditional super-polynomial logarithmic saving $|S(A)| \ll A\exp(-c(\log A)^{3/5}(\log\log A)^{-1/5}) \ll_D A(\log A)^{-D}$ for every $D > 0$, but does not control the transition region $A \asymp X$ or provide a fixed power saving without a zero-free strip for $\zeta(s)$.

`TASK-TC-054` and its repair `TASK-TC-054R` reformulate the problem using **Liouville's completely multiplicative function** $\lambda(n) = (-1)^{\Omega(n)}$ ($\lambda(1) = 1$) and establish **six unconditional theorems**, while repairing the dyadic Abel scaling, Poisson summation regularity hypotheses, hypergeometric Fourier tail certification, exact rational block cutoffs, unequal-block upper bound, and Lean 4 positive-integer arithmetic linkage, and isolating the exact analytic obstruction that keeps `SUBGATE-TC-043A` `OPEN` (`rh_proved: false`):

1. **Theorem 1 (Reversible Square-Divisor Convolution & Gaussian Square-Dilation Transfer, §2–§3)**:
   For all $n \ge 1$,
   $$\lambda(n) = \sum_{d^2 \mid n}\mu\!\left(\frac{n}{d^2}\right), \qquad \mu(n) = \sum_{d^2 \mid n}\mu(d)\lambda\!\left(\frac{n}{d^2}\right).$$
   For $Q_a(X) = X^{5/2}\sum_{n\ge 1}\frac{a(n)}{n^3}e^{-X^2/n^2}$ ($a \in \{\mu, \lambda\}$), $|Q_a(X)| \le \zeta(3)X^{5/2}$, the $n > T$ truncation tail is bounded by $\frac{X^{5/2}}{2 T^2}$, and Fubini's theorem yields the exact reversible square-dilation transfer
   $$Q_\lambda(X) = \sum_{d\ge 1}\frac{Q_\mu(X/d^2)}{d}, \qquad Q_\mu(X) = \sum_{d\ge 1}\frac{\mu(d)\,Q_\lambda(X/d^2)}{d},$$
   with dilation tail ($d > D$) bounded in magnitude by $\frac{\zeta(3)X^{5/2}}{5 D^5}$.

2. **Theorem 2 (Reversible Weighted $L^2$ Norm Equivalence & Grade-Interval Criterion, §3)**:
   For the weighted norm $\|f\|_\eta := \bigl(\int_0^\infty |f(X)|^2 X^{-2\eta}\frac{dX}{X}\bigr)^{1/2}$ with $\eta > 0$, any dilation $a > 0$ satisfies $\|f(\cdot/a)\|_\eta = a^{-\eta}\|f\|_\eta$, and for every $\eta > 0$,
   $$\|Q_\lambda\|_\eta \le \zeta(1 + 2\eta)\,\|Q_\mu\|_\eta, \qquad \|Q_\mu\|_\eta \le \frac{\zeta(1 + 2\eta)}{\zeta(2 + 4\eta)}\,\|Q_\lambda\|_\eta.$$
   Consequently, for both $a = \mu$ and $a = \lambda$,
   $$\left(\forall \varepsilon > 0\;\exists C_\varepsilon < \infty\;\forall Y \ge 1,\;\int_Y^{\tau Y}|Q_a(X)|^2\,\frac{dX}{X} \le C_\varepsilon Y^\varepsilon\right) \Longleftrightarrow \bigl(\forall \eta \in (0, 5/2),\;\|Q_a\|_\eta < \infty\bigr).$$
   As $\eta \downarrow 0$, the Minkowski triangle-inequality upper-bound multipliers diverge as $\zeta(1+2\eta) \sim \frac{1}{2\eta}$ and $\frac{\zeta(1+2\eta)}{\zeta(2+4\eta)} \sim \frac{1}{2\zeta(2)\eta} = \frac{12}{\tau^2\eta}$, reflecting the simple pole of the Mellin symbol $\zeta(1 + 2z)$ at $z = 0$ on the unweighted line $\operatorname{Re} z = 0$.

3. **Theorem 3 (Unconstrained Common-Factor Expansion & Fixed-Order Euler–Maclaurin Bound up to $A \le X^{1-\delta}$, §4)**:
   By complete multiplicativity, $\lambda(d r)\lambda(d s) = \lambda(d)^2\lambda(r)\lambda(s) = \lambda(r)\lambda(s)$ for **every** integer $d \ge 1$, eliminating both the squarefree factor $\mu(d)^2$ and the coprimality condition $\gcd(d, r s) = 1$. Hence
   $$Q_\lambda(X)^2 = \sum_{\substack{r, s \ge 1 \\ \gcd(r, s) = 1}}\frac{\lambda(r)\lambda(s)\,X^5}{(r s)^3}\sum_{d\ge 1} d^{-6} e^{-L^2/d^2}, \qquad L = X\sqrt{r^{-2} + s^{-2}}.$$
   With $c_0 := \int_0^\infty v^{-6}e^{-1/v^2}\,dv = \frac{1}{2}\Gamma(5/2) = \frac{3\sqrt{\tau/2}}{8}$, for $f(v) = v^{-6}e^{-1/v^2}$ ($v > 0$, $f(0) = 0$) and every even integer $N \ge 2$, periodic Bernoulli integration by parts proves
   $$\left|\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} - c_0 L^{-5}\right| \le C_N L^{-5-N}, \qquad C_N := \frac{2\zeta(N)}{\tau^N}\int_0^\infty \bigl|f^{(N)}(v)\bigr|\,dv,$$
   with certified 256-bit Arb constants
   $$c_0 = \frac{3\sqrt{\tau/2}}{8} \in [0.6646701940895685102368128062529294435491 \pm 2.00 \times 10^{-40}],$$
   $$C_2 = \frac{f'(v_-) - f'(v_+)}{6} = [1.851257667016958056850958359201349291641 \pm 3.54 \times 10^{-40}], \qquad v_\pm = \sqrt{\frac{15 \pm \sqrt{57}}{42}},$$
   $$C_4 = \frac{1}{720}\int_0^\infty \bigl|f^{(4)}(v)\bigr|\,dv = [8.752371760035365551239039765015814873069 \pm 3.16 \times 10^{-39}].$$
   Summing over $1 \le r, s \le A$ ($\gcd(r, s) = 1$) gives
   $$\sum_{\substack{1 \le r, s \le A \\ \gcd(r, s) = 1}}\bigl|E^\lambda_{r,s}(X)\bigr| \le C_N 2^{-(N+5)/2}\frac{A^{N+1}}{X^N},$$
   which tends to $0$ throughout the **entire subtransition regime** $A \le X^{1-\delta}$ whenever $(N+1)\delta > 1$ (already reaching $A \le X^{2/3-\varepsilon}$ at $N = 2$ and $A \le X^{1-\delta}$ for arbitrary fixed $\delta \in (0, 1)$ by choosing $N = 2\lceil 1/(2\delta)\rceil$).

4. **Theorem 4 (Exact Transition Poisson Summation on $C^1(\mathbb{R}/\mathbb{Z})$ & Certified Non-Positivity of $\widehat{f}$, §5)**:
   The even extension $f(v) = |v|^{-6}e^{-1/v^2}$ ($v \ne 0$, $f(0) = 0$) is **not** in the Schwartz class $\mathcal{S}(\mathbb{R})$ because $v^6 f(v) = e^{-1/v^2} \to 1 \ne 0$ as $|v| \to \infty$, but $f \in C^\infty(\mathbb{R})$ is flat at $0$, satisfies $f^{(j)}(v) = O(|v|^{-6-j})$ as $|v| \to \infty$, has $f^{(j)} \in L^1(\mathbb{R})$ for all $j \ge 0$, and its periodization $\mathcal{P}_L(x) = \sum_{n\in\mathbb{Z}}f((n+x)/L)$ converges uniformly with its first derivative on $[0, 1]$ to a $C^1(\mathbb{R}/\mathbb{Z})$ function ([DLMF 1.8.14](https://dlmf.nist.gov/1.8#E14)). Poisson summation therefore yields the exact identity valid for **all** $L > 0$:
   $$\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} = L^{-5}\left[c_0 + \sum_{j\ge 1}\widehat{f}(j L)\right], \qquad \widehat{f}(\xi) := 2\int_0^\infty v^{-6}e^{-1/v^2}\cos(\tau\xi v)\,dv.$$
   Evaluating $\widehat{f}(\xi)$ via its certified Mellin–Barnes residue expansion (with monotonic tail ratio certification $R_{\mathrm{even}}, R_{\mathrm{odd}} \le 1/2$ and independent `acb.integral` quadrature cross-checks) in 256-bit Arb certifies sign changes:
   $$\widehat{f}(1/2) = [-0.5628546550179851263755109492164491931001 \pm 4.04 \times 10^{-41}] < 0,$$
   $$\widehat{f}(4/\tau) = [-0.7757751802167744117629682956314216290713 \pm 2.04 \times 10^{-41}] < 0,$$
   $$\widehat{f}(1) = [-0.3668367826642069184644449070564857828859 \pm 4.03 \times 10^{-41}] < 0,$$
   $$\widehat{f}(3/2) = [0.2636171831500303372338138695632955698496 \pm 2.39 \times 10^{-41}] > 0,$$
   $$\widehat{f}(2) = [0.1247126116325928138362162976104693467978 \pm 9.77 \times 10^{-42}] > 0.$$

5. **Theorem 5 (Exact Separable Gaussian Decoupling, Repaired Dyadic Abel Scaling, & Global Stieltjes Energy Saving, §6A)**:
   In Attack A, the bivariate coprime Dirichlet series
   $$\mathcal{D}_\lambda(u, v) := \sum_{\gcd(r, s)=1}\frac{\lambda(r)\lambda(s)}{r^u s^v} = \frac{\zeta(2u)\zeta(2v)}{\zeta(u)\zeta(v)\zeta(u+v)} \qquad (\operatorname{Re} u > 1,\;\operatorname{Re} v > 1)$$
   cannot cancel off-critical poles at $(u, v) = (\rho, \bar{\rho})$ ($\rho = x + i y$ with $x > 1/2$) because $2x > 1$ lies inside the Euler-product half-plane where $\zeta(2\rho) \ne 0$ and $\zeta(2x) > 1$. Retaining the **exact separable Gaussian kernel** $e^{-X^2(r^{-2}+s^{-2})/d^2} = e^{-X^2/(d^2 r^2)}e^{-X^2/(d^2 s^2)}$ and applying $\mathbf{1}_{\gcd(r,s)=1} = \sum_{e \mid \gcd(r,s)}\mu(e)$ ($r = e m$, $s = e n$) decouples every rectangular block $B_{A,B}(X)$ into 1D unweighted Liouville Gaussian sums:
   $$B_{A,B}(X) = \sum_{1 \le e < 2\min(A,B)}\frac{\mu(e)}{e}\sum_{d\ge 1}\frac{1}{d}\,U_\lambda\!\left(\frac{X}{d e}; \frac{A}{e}\right)U_\lambda\!\left(\frac{X}{d e}; \frac{B}{e}\right),$$
   where $U_\lambda(Y; M) := Y^{5/2}\sum_{M \le m < 2M}\frac{\lambda(m)}{m^3}e^{-Y^2/m^2}$ satisfies the **repaired** dyadic Abel bound (for $M \ge 16$)
   $$\bigl|U_\lambda(Y; M)\bigr| \;\ll\; M^{1/2}\min\!\left(\frac{M}{Y}, \left(\frac{Y}{M}\right)^{5/2}\right)\exp\bigl(-c\,\Phi(M)\bigr), \qquad \Phi(t) := (\log t)^{3/5}(\log\log t)^{-1/5}.$$
   Furthermore, global Stieltjes integration by parts directly on $Q_\lambda(X) = -X^{5/2}\int_1^\infty L_\lambda(t)\frac{d}{dt}(t^{-3}e^{-X^2/t^2})\,dt$ split at $t = \sqrt{X}$ ($X \ge 256$) proves $|Q_\lambda(X)| \ll \sqrt{X}\exp(-c_1\Phi(X))$ for $X \ge 256$, the stretched-exponential grade-interval energy bound for $Y \ge 256$ ($\log\log Y > 1$), and—combined with the explicit compact-range bound $E_\lambda(Y) \le \frac{\zeta(3)^2(\tau^5-1)}{5} Y^5$ on $2 \le Y < 256$—the unconditional super-polynomial logarithmic saving across all $Y \ge 2$:
   $$\boxed{E_\lambda(Y) := \int_Y^{\tau Y}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} \;\ll\; Y\exp\!\left(-2 c_2 (\log Y)^{3/5}(\log\log Y)^{-1/5}\right)\;\;(Y \ge 256), \qquad E_\lambda(Y) \;\ll_D\; \frac{Y}{(\log Y)^D}\;\;(\forall D > 0,\;Y \ge 2).}$$
   This proved super-polynomial logarithmic saving $Y(\log Y)^{-D}$ is strictly distinguished from both a fixed power saving $E_\lambda(Y) \ll Y^{1-\eta}$ ($\eta \in (0, 1)$) and the full `SUBGATE-TC-043A` target $\forall \varepsilon > 0,\;E_\lambda(Y) \le C_\varepsilon Y^\varepsilon$.

6. **Theorem 6 (Dyadic Parity Annihilation, Cross-Scale Energy Identity, and Off-Critical Mode Non-Vanishing, §6B)**:
   The dyadic parity combination
   $$Q_{\lambda,\mathrm{odd}}(X) := Q_\lambda(X) + 2^{-1/2}Q_\lambda(X/2) = X^{5/2}\sum_{\substack{m\ge 1 \\ 2 \nmid m}}\frac{\lambda(m)}{m^3}e^{-X^2/m^2}$$
   annihilates all even indices $n = 2^a m$ ($a \ge 1$) by canceling $\lambda(2^{a-1}m) + \lambda(2^a m) = 0$, admits the convergent dyadic inverse $Q_\lambda(X) = \sum_{j\ge 0}(-1)^j 2^{-j/2}Q_{\lambda,\mathrm{odd}}(X/2^j)$, satisfies the exact grade-interval energy identity
   $$\int_Y^{\tau Y}\bigl|Q_{\lambda,\mathrm{odd}}(X)\bigr|^2\,\frac{dX}{X} = \int_Y^{\tau Y}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} + \frac{1}{2}\int_{Y/2}^{\tau Y/2}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} + \sqrt{2}\int_Y^{\tau Y}Q_\lambda(X)Q_\lambda(X/2)\,\frac{dX}{X},$$
   and satisfies the two-sided weighted norm equivalence $(1 - 2^{-1/2-\eta})\|Q_\lambda\|_\eta \le \|Q_{\lambda,\mathrm{odd}}\|_\eta \le (1 + 2^{-1/2-\eta})\|Q_\lambda\|_\eta$ for all $\eta > -1/2$. On any off-critical mode $X^{\rho - 1/2}$ ($\rho = x + i y$ with $x > 0$), the multiplier $1 + 2^{-\rho}$ satisfies $0 < 1 - 2^{-x} \le |1 + 2^{-\rho}| \le 1 + 2^{-x} < 2$ and never vanishes.

---

## 2. Complete Multiplicativity & Square-Divisor Convolutions ($\mu \leftrightarrow \lambda$)

### 2.1 Definitions and Prime-Power Proofs

Let $\Omega(n) := \sum_{p^a \parallel n} a$ ($\Omega(1) = 0$) denote the total number of prime factors of $n \ge 1$ counted with multiplicity, and define Liouville's function by
$$\lambda(n) := (-1)^{\Omega(n)} \qquad (n \ge 1).$$
Since $\Omega(1) = 0$, $\Omega(p) = 1$ for every prime $p$, and $\Omega(m n) = \Omega(m) + \Omega(n)$ for all $m, n \ge 1$, we have immediately:
- $\lambda(1) = 1$ and $\lambda(p) = -1$ for every prime $p$;
- $\lambda(m n) = (-1)^{\Omega(m) + \Omega(n)} = \lambda(m)\lambda(n)$ for all $m, n \ge 1$ (complete multiplicativity);
- $\lambda(d)^2 = (-1)^{2\Omega(d)} = 1$ for every $d \ge 1$.

**Proposition 2.1 (Square-Divisor Convolutions).** *For every integer $n \ge 1$:*
$$\lambda(n) = \sum_{d^2 \mid n}\mu\!\left(\frac{n}{d^2}\right), \qquad \mu(n) = \sum_{d^2 \mid n}\mu(d)\,\lambda\!\left(\frac{n}{d^2}\right).$$

*Proof.* Define $g(n) := \mathbf{1}_{\text{$n$ is a square}}$ ($g(d^2) = 1$, $g(n) = 0$ otherwise) and $h(n) := \mu(d)$ if $n = d^2$ is a square ($h(n) = 0$ otherwise). Both $g$ and $h$ are multiplicative arithmetic functions, so the Dirichlet convolutions $(\mu * g)(n) = \sum_{d^2 \mid n}\mu(n/d^2)$ and $(\lambda * h)(n) = \sum_{d^2 \mid n}\mu(d)\lambda(n/d^2)$ are multiplicative. It therefore suffices to verify both identities on prime powers $n = p^k$ ($k \ge 0$):
1. **Forward identity on $p^k$**: The square divisors of $p^k$ are $d^2 = p^{2j}$ for $0 \le j \le \lfloor k/2\rfloor$, with quotient $p^k / d^2 = p^{k - 2j}$. Since $\mu(p^m)$ is $1$ for $m = 0$, $-1$ for $m = 1$, and $0$ for $m \ge 2$:
   - If $k = 2r$ is even, the only nonzero term in $\sum_{j=0}^r \mu(p^{2r-2j})$ is $j = r$, giving $\mu(1) = 1 = (-1)^{2r} = \lambda(p^{2r})$.
   - If $k = 2r + 1$ is odd, the only nonzero term in $\sum_{j=0}^r \mu(p^{2r+1-2j})$ is $j = r$, giving $\mu(p) = -1 = (-1)^{2r+1} = \lambda(p^{2r+1})$.
2. **Inverse identity on $p^k$**: In $\sum_{j=0}^{\lfloor k/2\rfloor} \mu(p^j)\lambda(p^{k-2j}) = \sum_{j=0}^{\lfloor k/2\rfloor}\mu(p^j)(-1)^{k-2j} = (-1)^k \sum_{j=0}^{\lfloor k/2\rfloor}\mu(p^j)$:
   - If $k = 0$: $\mu(1)(-1)^0 = 1 = \mu(1)$.
   - If $k = 1$: $\lfloor 1/2\rfloor = 0$, so $\mu(1)(-1)^1 = -1 = \mu(p)$.
   - If $k \ge 2$: $\lfloor k/2\rfloor \ge 1$ and $\mu(p^j) = 0$ for all $j \ge 2$, so only $j = 0$ and $j = 1$ survive, giving $(-1)^k(\mu(1) + \mu(p)) = (-1)^k(1 - 1) = 0 = \mu(p^k)$.
By multiplicativity across prime-power factors $n = \prod_p p^{v_p(n)}$, both identities hold for all $n \ge 1$. Notice the corresponding Dirichlet-series relation for $s \in \mathbb{C}$ with $\operatorname{Re} s > 1$:
$$\sum_{n\ge 1}\frac{\lambda(n)}{n^s} = \left(\sum_{d\ge 1}\frac{1}{d^{2s}}\right)\left(\sum_{m\ge 1}\frac{\mu(m)}{m^s}\right) = \frac{\zeta(2s)}{\zeta(s)}. \qquad \square$$

In [`formal/RiemannScope/LiouvilleSquareDilation.lean`](../../formal/RiemannScope/LiouvilleSquareDilation.lean), these results are proved both on exponent models (`liouville_complete_multiplicativity_and_common_factor_cancellation_nat`, `prime_power_square_divisor_moebius_liouville_inversion_nat`) and unconditionally on actual positive integers $n \ge 1$ connected to Mathlib's `ArithmeticFunction.cardFactors`, `Nat.factorization`, and `ArithmeticFunction.moebius` (`actual_omega_factorization_and_liouville_common_factor_cancellation_nat`, `actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat`), including the explicit flat square-divisor sums `actualFlatMoebiusSquareDivisorSum n = ∑ d ∈ squareDivisors n, ArithmeticFunction.moebius (n / d^2)` and `actualFlatInverseLiouvilleSquareDivisorSum n = ∑ d ∈ squareDivisors n, ArithmeticFunction.moebius d * liouvilleLambda (n / d^2)` over `squareDivisors n = (Nat.divisors n).filter (fun d => d^2 ∣ n)` (proved multiplicative via `sum_squareDivisors_mul_of_coprime_aux` with no assumed surrogate `S`), and verified in Python across all $1 \le n \le 200$ and all $1 \le d, r, s \le 30$ ($27{,}000$ triples).

---

## 3. Reversible Square-Dilation Transfer & Weighted Norm Equivalence

### 3.1 Pointwise Bounds, Truncation Tails, and Fubini Transfer

For $a \in \{\mu, \lambda\}$ and $X > 0$, define
$$Q_a(X) := X^{5/2}\sum_{n\ge 1}\frac{a(n)}{n^3}e^{-X^2/n^2}.$$
Since $|a(n)| \le 1$ and $e^{-X^2/n^2} \le 1$ for all $n \ge 1$ and $X > 0$:
1. **Absolute bound**:
   $$\bigl|Q_a(X)\bigr| \le X^{5/2}\sum_{n\ge 1}\frac{1}{n^3} = \zeta(3)\,X^{5/2}.$$
2. **Series truncation tail ($n > T$, $T \ge 1$)**:
   $$\bigl|R_{a, > T}(X)\bigr| := \left|X^{5/2}\sum_{n > T}\frac{a(n)}{n^3}e^{-X^2/n^2}\right| \le X^{5/2}\sum_{n = T+1}^\infty \frac{1}{n^3} \le X^{5/2}\int_T^\infty \frac{du}{u^3} = \frac{X^{5/2}}{2 T^2}.$$
3. **Reversible square-dilation transfer**:
   Substituting $\lambda(n) = \sum_{d^2 \mid n}\mu(n/d^2)$ with $n = d^2 m$ gives
   $$\sum_{d\ge 1}\sum_{m\ge 1} X^{5/2}\frac{|\mu(m)|}{(d^2 m)^3}e^{-X^2/(d^2 m)^2} \le X^{5/2}\left(\sum_{d\ge 1}d^{-6}\right)\left(\sum_{m\ge 1}m^{-3}\right) = \zeta(6)\zeta(3)X^{5/2} < \infty.$$
   By Fubini's theorem for absolutely convergent double series,
   $$Q_\lambda(X) = \sum_{d\ge 1} X^{5/2}\sum_{m\ge 1}\frac{\mu(m)}{d^6 m^3}e^{-(X/d^2)^2/m^2} = \sum_{d\ge 1}\frac{1}{d}\left(\frac{X}{d^2}\right)^{5/2}\sum_{m\ge 1}\frac{\mu(m)}{m^3}e^{-(X/d^2)^2/m^2} = \sum_{d\ge 1}\frac{Q_\mu(X/d^2)}{d}.$$
   Similarly, substituting $\mu(n) = \sum_{d^2 \mid n}\mu(d)\lambda(n/d^2)$ yields the exact inverse transfer
   $$Q_\mu(X) = \sum_{d\ge 1}\frac{\mu(d)\,Q_\lambda(X/d^2)}{d}.$$
4. **Dilation truncation tail ($d > D$, $D \ge 1$)**:
   Since $|Q_a(X/d^2)| \le \zeta(3)(X/d^2)^{5/2} = \zeta(3)X^{5/2} d^{-5}$, the omitted tail for $d > D$ in either transfer satisfies
   $$\left|\sum_{d > D}\frac{w(d)\,Q_a(X/d^2)}{d}\right| \le \zeta(3)X^{5/2}\sum_{d = D+1}^\infty d^{-6} \le \zeta(3)X^{5/2}\int_D^\infty u^{-6}\,du = \frac{\zeta(3)X^{5/2}}{5 D^5}.$$

| Scale $X$ | Direct $Q_\mu(X)$ ($T = 4000$) | Transfer $\sum_{d\le 80}\frac{\mu(d)Q_\lambda(X/d^2)}{d}$ | Direct $Q_\lambda(X)$ ($T = 4000$) | Transfer $\sum_{d\le 80}\frac{Q_\mu(X/d^2)}{d}$ | $0 \in \Delta$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $1/2$ | `[0.10948801 +/- 7.01e-9]` | `[0.10948801 +/- 7.44e-9]` | `[0.1119965 +/- 4.98e-8]` | `[0.1119965 +/- 5.03e-8]` | `True` |
| $1$ | `[0.2315739 +/- 6.85e-8]` | `[0.2315739 +/- 7.09e-8]` | `[0.2450723 +/- 5.75e-8]` | `[0.2450723 +/- 6.03e-8]` | `True` |
| $2$ | `[-0.319959 +/- 3.07e-7]` | `[-0.319959 +/- 3.22e-7]` | `[-0.257513 +/- 5.39e-7]` | `[-0.257513 +/- 5.55e-7]` | `True` |
| $\tau = 2\pi$ | `[-0.17310 +/- 5.05e-6]` | `[-0.17310 +/- 5.31e-6]` | `[-0.11075 +/- 3.55e-6]` | `[-0.11075 +/- 3.83e-6]` | `True` |
| $4$ | `[-0.37511 +/- 5.31e-6]` | `[-0.37511 +/- 5.40e-6]` | `[-0.22166 +/- 5.98e-6]` | `[-0.22166 +/- 6.07e-6]` | `True` |
| $8$ | `[-0.10406 +/- 8.84e-6]` | `[-0.1041 +/- 4.94e-5]` | `[-0.14527 +/- 6.97e-6]` | `[-0.14527 +/- 7.48e-6]` | `True` |

### 3.2 Weighted $L^2$ Dilation Norm Equivalence and $\eta \downarrow 0$ Scope Analysis

For real norm weight $\eta > 0$, define the weighted multiplicative $L^2$ norm on $(0, \infty)$:
$$\|f\|_\eta := \left(\int_0^\infty |f(X)|^2 X^{-2\eta}\,\frac{dX}{X}\right)^{1/2}.$$
Under the change of variables $X = a Y$ ($a > 0$, $\frac{dX}{X} = \frac{dY}{Y}$):
$$\|f(\cdot/a)\|_\eta^2 = \int_0^\infty |f(X/a)|^2 X^{-2\eta}\,\frac{dX}{X} = \int_0^\infty |f(Y)|^2 (a Y)^{-2\eta}\,\frac{dY}{Y} = a^{-2\eta}\|f\|_\eta^2 \implies \|f(\cdot/a)\|_\eta = a^{-\eta}\|f\|_\eta.$$
In particular, for $a = d^2$, $\|f(\cdot/d^2)\|_\eta = d^{-2\eta}\|f\|_\eta$. Applying Minkowski's integral inequality to $Q_\lambda(X) = \sum_{d\ge 1} d^{-1} Q_\mu(X/d^2)$ and $Q_\mu(X) = \sum_{d\ge 1}\mu(d) d^{-1} Q_\lambda(X/d^2)$ for any $\eta > 0$ yields:
$$\|Q_\lambda\|_\eta \le \sum_{d\ge 1}\frac{\|Q_\mu(\cdot/d^2)\|_\eta}{d} = \left(\sum_{d\ge 1} d^{-1-2\eta}\right)\|Q_\mu\|_\eta = \zeta(1 + 2\eta)\,\|Q_\mu\|_\eta,$$
$$\|Q_\mu\|_\eta \le \sum_{d\ge 1}\frac{|\mu(d)|\,\|Q_\lambda(\cdot/d^2)\|_\eta}{d} = \left(\sum_{d\ge 1}\mu(d)^2 d^{-1-2\eta}\right)\|Q_\lambda\|_\eta = \frac{\zeta(1 + 2\eta)}{\zeta(2 + 4\eta)}\,\|Q_\lambda\|_\eta.$$
- **Behavior as $\eta \downarrow 0$ and exact operator scope**: Since $\zeta(1 + 2\eta) = \frac{1}{2\eta} + \gamma + O(\eta)$ and $\zeta(2) = \frac{\tau^2}{24}$, the Minkowski series upper bounds diverge like $O(\eta^{-1})$ as $\eta \downarrow 0$:
  $$\lim_{\eta \to 0^+}\eta\,\zeta(1 + 2\eta) = \frac{1}{2} = 0.5, \qquad \lim_{\eta \to 0^+}\eta\,\frac{\zeta(1 + 2\eta)}{\zeta(2 + 4\eta)} = \frac{1}{2\zeta(2)} = \frac{12}{\tau^2} \in [0.3039635509270133143316383896291829167131 \pm 2.37 \times 10^{-41}].$$
  Positive-weight bounds ($\eta > 0$) do **not** establish boundedness of the ordinary boundary series $\sum_{d\ge 1} d^{-1}f(\cdot/d^2)$ on the full unweighted Hilbert space $L^2((0, \infty), \frac{dX}{X})$. By Mellin Plancherel along $z = i b$ ($b \in \mathbb{R}$, $a = 0$), the formal boundary multiplier is $m(i b) = \zeta(1 + 2 i b)$, which has a simple pole at $b = 0$ and is unbounded as $|b| \to \infty$, so the unweighted square-dilation transfer is not a bounded operator on $L^2((0, \infty), \frac{dX}{X})$. By contrast, for every fixed $\eta > 0$, the transfer is an unconditionally bounded, invertible linear isomorphism on $L^2((0, \infty), X^{-2\eta}\frac{dX}{X})$.

| $\eta$ | $\zeta(1 + 2\eta)$ | $\frac{\zeta(1 + 2\eta)}{\zeta(2 + 4\eta)}$ | $\eta\,\zeta(1 + 2\eta)$ | $\eta\,\frac{\zeta(1 + 2\eta)}{\zeta(2 + 4\eta)}$ |
| :--- | :--- | :--- | :--- | :--- |
| $1/20$ | `[10.58444846495080982638640079173552303995 +/- 1.55e-39]` | `[7.101067626682364959660319788279339842132 +/- 1.71e-40]` | `[0.5292224232475404913193200395867761519973 +/- 7.77e-41]` | `[0.3550533813341182479830159894139669921066 +/- 8.53e-42]` |
| $1/10$ | `[5.591582441177750776536563193423143277630 +/- 9.68e-41]` | `[4.042079955408588766460293600513948039645 +/- 3.91e-40]` | `[0.5591582441177750776536563193423143277630 +/- 1.07e-41]` | `[0.4042079955408588766460293600513948039645 +/- 4.01e-41]` |
| $1/4$ | `[2.612375348685488343348567567924071630571 +/- 2.00e-40]` | `[2.173254312519554138237089840438223722907 +/- 2.89e-40]` | `[0.6530938371713720858371418919810179076428 +/- 5.00e-41]` | `[0.5433135781298885345592724601095559307268 +/- 7.21e-41]` |
| $1/2$ | `[1.644934066848226436472415166646025189219 +/- 5.02e-41]` | `[1.519817754635066571658191948145914583565 +/- 3.82e-40]` | `[0.8224670334241132182362075833230125946093 +/- 2.51e-41]` | `[0.7599088773175332858290959740729572917825 +/- 1.91e-40]` |
| $1$ | `[1.202056903159594285399738161511449990765 +/- 1.38e-41]` | `[1.181564949010256912569399734160454260547 +/- 2.33e-41]` | `[1.202056903159594285399738161511449990765 +/- 1.38e-41]` | `[1.181564949010256912569399734160454260547 +/- 2.33e-41]` |

### 3.3 Grade-Interval Energy Equivalence, Mellin Continuation, and Lindemann Scope

**Proposition 3.1 (Equivalence of Grade-Interval Subpower Energy and Weighted Norm Finiteness).** *For $a \in \{\mu, \lambda\}$, the following two conditions are equivalent:*
1. *(Grade-interval subpower energy)*: $\forall \varepsilon > 0\;\exists C_\varepsilon < \infty\;\forall Y \ge 1,\;\int_Y^{\tau Y}|Q_a(X)|^2\,\frac{dX}{X} \le C_\varepsilon Y^\varepsilon$.
2. *(Weighted norm finiteness)*: $\forall \eta \in (0, 5/2),\;\|Q_a\|_\eta < \infty$.

*Proof.*
- **(1) $\implies$ (2)**: Fix $\eta \in (0, 5/2)$. On $(0, 1]$, $|Q_a(X)| \le \zeta(3)X^{5/2}$ gives
  $$\int_0^1 |Q_a(X)|^2 X^{-2\eta}\,\frac{dX}{X} \le \zeta(3)^2\int_0^1 X^{4-2\eta}\,dX = \frac{\zeta(3)^2}{5 - 2\eta} < \infty.$$
  On $[1, \infty) = \bigcup_{k=0}^\infty [\tau^k, \tau^{k+1})$, apply (1) with $\varepsilon = \eta > 0$ and $Y = \tau^k \ge 1$. Since $X^{-2\eta} \le \tau^{-2k\eta}$ on $[\tau^k, \tau^{k+1})$,
  $$\sum_{k=0}^\infty \int_{\tau^k}^{\tau^{k+1}}|Q_a(X)|^2 X^{-2\eta}\,\frac{dX}{X} \le \sum_{k=0}^\infty \tau^{-2k\eta} C_\eta \tau^{k\eta} = \frac{C_\eta}{1 - \tau^{-\eta}} < \infty.$$
  Hence $\|Q_a\|_\eta^2 \le \frac{\zeta(3)^2}{5 - 2\eta} + \frac{C_\eta}{1 - \tau^{-\eta}} < \infty$.
- **(2) $\implies$ (1)**: Given $\varepsilon > 0$, without loss of generality take $\varepsilon \in (0, 5)$ (since $Y^\varepsilon$ is increasing in $\varepsilon$ for $Y \ge 1$) and set $\eta = \varepsilon/2 \in (0, 5/2)$. For any $Y \ge 1$ and $X \in [Y, \tau Y]$, $X / (\tau Y) \le 1 \implies 1 \le (\tau Y)^{2\eta} X^{-2\eta} = \tau^\varepsilon Y^\varepsilon X^{-2\eta}$, so
  $$\int_Y^{\tau Y}|Q_a(X)|^2\,\frac{dX}{X} \le \tau^\varepsilon Y^\varepsilon \int_Y^{\tau Y}|Q_a(X)|^2 X^{-2\eta}\,\frac{dX}{X} \le \tau^\varepsilon \|Q_a\|_{\varepsilon/2}^2\,Y^\varepsilon. \qquad \square$$

**Analytic Mellin-to-RH Bridge, Lindemann Irrationality Scope, and Connection to `SUBGATE-TC-043A`**:
- For $z = a + i b \in \mathbb{C}$ with $\frac{1}{2} < a < \frac{5}{2}$, termwise Mellin integration (justified by $\sum_{n\ge 1} n^{-1/2 - a} < \infty$ and $\int_0^\infty X^{5/2 - z} e^{-X^2/n^2}\frac{dX}{X} = \frac{1}{2}n^{5/2 - z}\Gamma(5/4 - z/2)$) yields:
  $$\mathcal{M}[Q_\mu](z) := \int_0^\infty Q_\mu(X) X^{-z}\,\frac{dX}{X} = \frac{\Gamma(5/4 - z/2)}{2\,\zeta(1/2 + z)}, \qquad \mathcal{M}[Q_\lambda](z) := \int_0^\infty Q_\lambda(X) X^{-z}\,\frac{dX}{X} = \frac{\Gamma(5/4 - z/2)\,\zeta(1 + 2z)}{2\,\zeta(1/2 + z)}.$$
- If $\|Q_a\|_\eta < \infty$ for all $\eta \in (0, 5/2)$, then for any compact subset $\mathcal{K} \subset \{z = a + i b \in \mathbb{C} : 0 < a < 5/2\}$, splitting $\int_0^\infty = \int_0^1 + \int_1^\infty$ and applying Cauchy–Schwarz on $[1, \infty)$ with $\eta_0 = \frac{1}{2}\min_{z \in \mathcal{K}}\operatorname{Re} z > 0$:
  $$\left|\int_1^\infty Q_a(X) X^{-z}\,\frac{dX}{X}\right| \le \|Q_a\|_{\eta_0}\left(\int_1^\infty X^{-2(\operatorname{Re} z - \eta_0)}\,\frac{dX}{X}\right)^{1/2} = \frac{\|Q_a\|_{\eta_0}}{\sqrt{2(\operatorname{Re} z - \eta_0)}} < \infty,$$
  proving that $\mathcal{M}[Q_a](z)$ extends holomorphically to the entire strip $0 < \operatorname{Re} z < 5/2$. Since $\Gamma(5/4 - z/2)$ is nonvanishing on $\operatorname{Re} z < 5/2$ and $\zeta(1 + 2z)$ is nonvanishing on $\operatorname{Re} z > 0$ ($\operatorname{Re}(1 + 2z) > 1$), holomorphicity of $\mathcal{M}[Q_a](z)$ on $0 < \operatorname{Re} z < 5/2$ forces $\zeta(1/2 + z) \ne 0$ on $0 < \operatorname{Re} z < 1/2$, i.e., $\zeta(\rho) \ne 0$ for $\rho = x + i y$ in $1/2 < x < 1$ (and by the functional equation in $0 < x < 1/2$).
- **Arithmetic Scope of $\log_\tau 2$ and $\log_\tau(d^2)$**: By Lindemann's theorem ($e^{i\tau/2} = -1 \implies \tau = 2\pi$ is transcendental over $\mathbb{Q}$), for every integer $m \ge 2$ the logarithm $\log_\tau m$ is **irrational** ($\log_\tau m \notin \mathbb{Q}$): if $\log_\tau m = p/q$ with integers $p, q \ge 1$, then $\tau^p = m^q \in \mathbb{Z}$, contradicting transcendence of $\tau$. Note, however, that Lindemann's theorem alone does **not** settle whether $\log_\tau 2$ or $\log_\tau(d^2)$ is transcendental over $\mathbb{Q}$ (i.e., whether $\log_\tau 2 \notin \mathbb{A}_{\mathbb{R}}$). Crucially, Proposition 3.1 does **not** need to classify $\log_\tau 2$ or $\log_\tau(d^2)$ relative to $\mathbb{A}_{\mathbb{R}}$: the partition $[1, \infty) = \bigcup_{k=0}^\infty [\tau^k, \tau^{k+1})$ uses only rational integer grades $k \in \mathbb{Z} \subset \mathbb{A}_{\mathbb{R}}$, and the square-dilation and dyadic operators act as bounded linear isomorphisms on the ambient continuum space $L^2((0, \infty), X^{-2\eta}\frac{dX}{X})$ ($\eta > 0$).

---

## 4. Unconstrained Common-Factor Expansion & Fixed-Order Euler–Maclaurin Bounds

### 4.1 Complete Multiplicativity Common-Factor Expansion

Writing every pair $(m, n) \in \mathbb{Z}_{\ge 1}^2$ uniquely as $m = d r$, $n = d s$ with $d = \gcd(m, n) \ge 1$ and $\gcd(r, s) = 1$, complete multiplicativity of $\lambda$ gives
$$\lambda(m)\lambda(n) = \lambda(d r)\lambda(d s) = \lambda(d)^2\lambda(r)\lambda(s) = \lambda(r)\lambda(s) \qquad (\forall d, r, s \ge 1),$$
with **no squarefree restriction on $d$ and no coprimality restriction $\gcd(d, r s) = 1$**. Therefore:
$$Q_\lambda(X)^2 = X^5 \sum_{m, n \ge 1}\frac{\lambda(m)\lambda(n)}{(m n)^3}e^{-X^2(m^{-2}+n^{-2})} = \sum_{\substack{r, s \ge 1 \\ \gcd(r, s) = 1}}\frac{\lambda(r)\lambda(s)\,X^5}{(r s)^3}\sum_{d\ge 1} d^{-6} e^{-L^2/d^2}, \qquad L := X\sqrt{r^{-2} + s^{-2}}.$$
Since $\int_0^\infty t^{-6} e^{-L^2/t^2}\,dt = L^{-5}\int_0^\infty v^{-6}e^{-1/v^2}\,dv = \frac{1}{2}\Gamma(5/2)L^{-5} = c_0 L^{-5}$ where $c_0 = \frac{3\sqrt{\tau/2}}{8}$, the leading Gaussian term for each coprime pair $(r, s)$ is
$$L^\lambda_{r, s} := \frac{\lambda(r)\lambda(s)\,X^5}{(r s)^3}\cdot c_0 L^{-5} = c_0\,\lambda(r)\lambda(s)\frac{(r s)^2}{(r^2 + s^2)^{5/2}}, \qquad c_0 = \frac{3\sqrt{\tau/2}}{8},$$
which is completely independent of $X$.

### 4.2 Fixed-Order Euler–Maclaurin Bound for $f(v) = v^{-6}e^{-1/v^2}$

Let $f(v) := v^{-6}e^{-1/v^2}$ for $v > 0$ and $f(0) := 0$. Every derivative $f^{(k)}(v)$ is a polynomial in $v^{-1}$ multiplied by $e^{-1/v^2}$, so $\lim_{v \to 0^+} f^{(k)}(v) = 0$ and $\lim_{v \to \infty} f^{(k)}(v) = 0$ for all $k \ge 0$. Set $g(t) := t^{-6}e^{-L^2/t^2} = L^{-6}f(t/L)$, so $g^{(N)}(t) = L^{-6-N}f^{(N)}(t/L)$ with $g^{(k)}(0) = g^{(k)}(\infty) = 0$ for all $k \ge 0$.

For any even integer $N \ge 2$, the $N$-th order Euler–Maclaurin summation formula on $[0, \infty)$ with vanished endpoint derivatives gives
$$\sum_{d\ge 1} g(d) - \int_0^\infty g(t)\,dt = -\frac{1}{N!}\int_0^\infty \widetilde{B}_N(t)\,g^{(N)}(t)\,dt,$$
where $\widetilde{B}_N(t) = B_N(\{t\})$ is the $N$-th periodic Bernoulli function, whose Fourier expansion
$$\widetilde{B}_N(t) = (-1)^{N/2 - 1}\frac{2\,N!}{\tau^N}\sum_{j=1}^\infty \frac{\cos(j\tau t)}{j^N}$$
implies the sharp uniform supremum bound $\sup_{t \in \mathbb{R}}\frac{|\widetilde{B}_N(t)|}{N!} = \frac{2\zeta(N)}{\tau^N}$. Substituting $t = L v$ ($dt = L\,dv$) yields:
$$\left|\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} - c_0 L^{-5}\right| \le \frac{2\zeta(N)}{\tau^N}\int_0^\infty L^{-6-N}\bigl|f^{(N)}(t/L)\bigr|\,dt = C_N L^{-5-N}, \qquad C_N := \frac{2\zeta(N)}{\tau^N}\int_0^\infty \bigl|f^{(N)}(v)\bigr|\,dv.$$

**Exact Symbolic Derivatives and Certified Constants $C_2, C_4$**:
Using SymPy (`verify_euler_maclaurin_derivatives_and_constants_arb`), the first four derivatives of $f(v) = v^{-6}e^{-1/v^2}$ are:
$$f'(v) = 2(1 - 3v^2)v^{-9}e^{-1/v^2}, \qquad f''(v) = 2(21v^4 - 15v^2 + 2)v^{-12}e^{-1/v^2},$$
$$f^{(3)}(v) = 4(-84v^6 + 96v^4 - 27v^2 + 2)v^{-15}e^{-1/v^2}, \qquad f^{(4)}(v) = 4(6v^2 - 1)(126v^6 - 183v^4 + 60v^2 - 4)v^{-18}e^{-1/v^2}.$$
- **Evaluation of $C_2$ ($N = 2$)**: Since $21v^4 - 15v^2 + 2 = 0$ has positive roots
  $$v_- = \sqrt{\frac{15 - \sqrt{57}}{42}} \in [0.4211708612882846189067416640646506740997 \pm 2.00 \times 10^{-40}],$$
  $$v_+ = \sqrt{\frac{15 + \sqrt{57}}{42}} \in [0.7327351635395962094861244517470714998819 \pm 2.00 \times 10^{-40}],$$
  with $f'' > 0$ on $(0, v_-) \cup (v_+, \infty)$, $f'' < 0$ on $(v_-, v_+)$, and $f'(v_-) > 0 > f'(v_+)$, the fundamental theorem of calculus gives
  $$\int_0^\infty |f''(v)|\,dv = f'(v_-) - (f'(v_+) - f'(v_-)) + (-f'(v_+)) = 2\bigl(f'(v_-) - f'(v_+)\bigr),$$
  and since $\frac{2\zeta(2)}{\tau^2} = \frac{2(\tau^2/24)}{\tau^2} = \frac{1}{12}$,
  $$C_2 = \frac{f'(v_-) - f'(v_+)}{6} \in [1.851257667016958056850958359201349291641 \pm 2.00 \times 10^{-39}].$$
- **Evaluation of $C_4$ ($N = 4$)**: The four positive roots $0 < v_1 < v_2 = 1/\sqrt{6} < v_3 < v_4$ of $f^{(4)}(v) = 0$ satisfy $\int_0^\infty |f^{(4)}(v)|\,dv = 2[f^{(3)}(v_1) - f^{(3)}(v_2) + f^{(3)}(v_3) - f^{(3)}(v_4)]$, and since $\frac{2\zeta(4)}{\tau^4} = \frac{2(\tau^4/1440)}{\tau^4} = \frac{1}{720}$,
  $$C_4 = \frac{1}{720}\int_0^\infty \bigl|f^{(4)}(v)\bigr|\,dv \in [8.752371760035365551239039765015814873069 \pm 4.00 \times 10^{-39}].$$

### 4.3 Pairwise and Summed Subtransition Error Bounds ($A \le X^{1-\delta}$)

Multiplying the $d$-sum error bound by $\frac{X^5}{(r s)^3}$ with $L = X\frac{\sqrt{r^2+s^2}}{r s}$ yields the pairwise error bound
$$\bigl|E^\lambda_{r, s}(X)\bigr| \le \frac{X^5}{(r s)^3}\,C_N L^{-5-N} = C_N X^{-N}\frac{(r s)^{N+2}}{(r^2 + s^2)^{(N+5)/2}}.$$
- **Regression against the spurious $\frac{1}{2\sqrt{2}}$ pairwise factor (`pairwise_spurious_factor_counterexample_regression`)**:
  For $N = 2$, the exact pairwise bound is
  $$\bigl|E^\lambda_{r, s}(X)\bigr| \le C_2 X^{-2}\frac{(r s)^4}{(r^2 + s^2)^{7/2}},$$
  with no extra $2^{-3/2} = \frac{1}{2\sqrt{2}}$ factor (which only arises after applying AM–GM $r^2 + s^2 \ge 2 r s \implies (r^2 + s^2)^{-7/2} \le 2^{-7/2}(r s)^{-7/2}$). At $r = 1, s = 1, L = \frac{9}{5}, X = \frac{9}{5\sqrt{2}}$ (`D_cutoff = 1000`), certified 256-bit Arb evaluation gives:
  $$\frac{\left|\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} - c_0 L^{-5}\right|}{C_2 L^{-7}} = [0.4030344210273 \pm 4.02 \times 10^{-14}] > \frac{1}{2\sqrt{2}} = [0.3535533905932737622004221810524245196424 \pm 1.80 \times 10^{-41}],$$
  with certified positive gap $[0.04948103043406 \pm 6.81 \times 10^{-15}] > 0$, so at $(r, s) = (1, 1)$,
  $$\bigl|E^\lambda_{1,1}(X)\bigr| = [0.04070886643302 \pm 1.98 \times 10^{-15}] > \frac{C_2}{2\sqrt{2}}X^{-2}\frac{1}{2^{7/2}} = [0.03571098894708638226950151155866800331098 \pm 2.90 \times 10^{-42}],$$
  refuting the spurious extra $\frac{1}{2\sqrt{2}}$ factor on the unreduced pairwise formula while satisfying the true pairwise bound $C_2 X^{-2}\frac{1}{2^{7/2}} = [0.1010059297894505107100302740960207508287 \pm 7.19 \times 10^{-42}]$.

By AM–GM, $r^2 + s^2 \ge 2 r s \implies (r^2 + s^2)^{(N+5)/2} \ge 2^{(N+5)/2}(r s)^{(N+5)/2}$, so
$$\frac{(r s)^{N+2}}{(r^2 + s^2)^{(N+5)/2}} \le 2^{-(N+5)/2}(r s)^{(N+2) - (N+5)/2} = 2^{-(N+5)/2}(r s)^{(N-1)/2}.$$
Summing over $1 \le r, s \le A$ using $(r s)^{(N-1)/2} \le A^{N-1}$ on the $A^2$ pairs $(r, s) \in [1, A]^2$ gives:
$$\sum_{\substack{1 \le r, s \le A \\ \gcd(r, s) = 1}}\bigl|E^\lambda_{r,s}(X)\bigr| \le C_N 2^{-(N+5)/2} X^{-N}\sum_{r=1}^A \sum_{s=1}^A (r s)^{(N-1)/2} \le C_N 2^{-(N+5)/2}\frac{A^{N+1}}{X^N}.$$
Setting $A \le X^{1-\delta}$ ($\delta \in (0, 1)$), the exponent of $X$ is
$$(N + 1)(1 - \delta) - N = 1 - (N + 1)\delta < 0 \Longleftrightarrow (N + 1)\delta > 1.$$
- For $N = 2$: $(2 + 1)\delta > 1 \iff \delta > 1/3$, controlling $A \le X^{2/3 - \varepsilon}$ (already doubling the $TC\text{-}053R$ exponent $1/3 - \delta$).
- For $N = 4$: $(4 + 1)\delta > 1 \iff \delta > 1/5$, controlling $A \le X^{4/5 - \varepsilon}$.
- For any fixed $\delta \in (0, 1)$: choosing the even integer $N = 2\lceil 1/(2\delta)\rceil$ gives $(N + 1)\delta \ge 1 + \delta > 1$, so the summed Euler–Maclaurin error vanishes as $O(X^{1 - (N+1)\delta}) \to 0$ throughout $A \le X^{1-\delta}$.

| $L$ | Exact $\sum_{d\ge 1}d^{-6}e^{-L^2/d^2}$ | Gaussian Leading $c_0 L^{-5}$ | Absolute Error | $N = 2$ Bound $C_2 L^{-7}$ | $N = 4$ Bound $C_4 L^{-9}$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $1/2$ | `[0.79515495547440055 +/- 6.33e-18]` | `[21.26944621086619232757800980009374219357 +/- 5.94e-40]` | `[20.47429125539179178 +/- 8.60e-18]` | `[236.9609813781706312769226699777727093301 +/- 6.77e-39]` | `[4481.214341138107162234388359688097215011 +/- 2.73e-37]` |
| $1$ | `[0.3816038498680422 +/- 5.24e-17]` | `[0.6646701940895685102368128062529294435491 +/- 1.90e-41]` | `[0.2830663442215263 +/- 4.22e-17]` | `[1.851257667016958056850958359201349291641 +/- 3.54e-40]` | `[8.752371760035365551239039765015814873069 +/- 1.09e-40]` |
| $2$ | `[0.02522282217978698 +/- 6.66e-18]` | `[0.02077094356529901594490040019540404511091 +/- 1.22e-42]` | `[0.0044518786144880 +/- 4.26e-17]` | `[0.01446295052356998481914811218126054134095 +/- 1.93e-42]` | `[0.01709447609381907334226374954104651342396 +/- 2.68e-42]` |
| $4$ | `[0.00066833923524992 +/- 8.66e-18]` | `[0.0006490919864155942482781375061063764097159 +/- 5.43e-46]` | `[1.924724883433e-5 +/- 8.09e-18]` | `[0.0001129918009653905063995946264160979792262 +/- 4.32e-44]` | `[3.338764862074037762160888582235647153118e-5 +/- 2.90e-45]` |
| $8$ | `[2.028496883949e-5 +/- 7.27e-18]` | `[2.028412457548732025869179706582426280362e-5 +/- 1.86e-45]` | `[8.4426400e-10 +/- 7.92e-18]` | `[8.827484450421133312468330188757654627044e-7 +/- 4.99e-47]` | `[6.521025121238355004220485512178998345933e-8 +/- 2.93e-49]` |

---

## 5. Exact Poisson Summation Formula at the Transition ($A \asymp X$)

### 5.1 Non-Schwartz Regularity and Periodized $C^1(\mathbb{R}/\mathbb{Z})$ Justification

When $r, s \asymp A \asymp X$, the effective scale $L = X\sqrt{r^{-2} + s^{-2}} \asymp 1$ is of order unity, so $A^{N+1}/X^N \asymp_N X$ diverges for every fixed $N$. Extend $f(v) = v^{-6}e^{-1/v^2}$ evenly to $\mathbb{R}$ by $f(-v) := f(v)$ ($v \ne 0$) and $f(0) := 0$.

- **Correction of the false Schwartz premise**: In `TC-054`, $f$ was described as belonging to the Schwartz space $\mathcal{S}(\mathbb{R})$. That statement is **false**: a function $g \in \mathcal{S}(\mathbb{R})$ must satisfy $\sup_{v \in \mathbb{R}} |v^k g(v)| < \infty$ and $\lim_{|v|\to\infty} v^k g(v) = 0$ for **every** integer $k \ge 0$, whereas for $f(v) = |v|^{-6}e^{-1/v^2}$ we have
  $$\lim_{|v|\to\infty} v^6 f(v) = \lim_{|v|\to\infty} e^{-1/v^2} = 1 \ne 0, \qquad \lim_{|v|\to\infty} |v|^7 f(v) = +\infty,$$
  so $f$ has only algebraic decay $O(|v|^{-6})$ at infinity and $f \notin \mathcal{S}(\mathbb{R})$.
- **Rigorous $C^1(\mathbb{R}/\mathbb{Z})$ periodization proof of Poisson summation ([DLMF 1.8.14](https://dlmf.nist.gov/1.8#E14))**:
  1. At $v = 0$, $\lim_{v\to 0} v^{-m}e^{-1/v^2} = 0$ for every $m \ge 0$, so $f \in C^\infty(\mathbb{R})$ with $f^{(j)}(0) = 0$ for all $j \ge 0$.
  2. By induction, $f^{(j)}(v) = P_j(v^{-1})v^{-6-j}e^{-1/v^2}$ where $P_j$ is a polynomial with $P_j(0) \ne 0$, so $f^{(j)}(v) = O(|v|^{-6-j})$ as $|v| \to \infty$, and therefore $f^{(j)} \in L^1(\mathbb{R})$ for every $j \ge 0$.
  3. For any fixed $L > 0$, consider the $1$-periodic periodization $\mathcal{P}_L(x) := \sum_{n \in \mathbb{Z}} f\!\left(\frac{n + x}{L}\right)$ for $x \in [0, 1]$. Since $f(v) \le |v|^{-6}$ and $|f'(v)| \le 6(|v|^{-7} + |v|^{-9})e^{-1/v^2}$, for $|n| \ge 2$ and $x \in [0, 1]$ we have $|n + x| \ge |n| - 1$, so the series for $\mathcal{P}_L(x)$ and $\mathcal{P}_L'(x) = L^{-1}\sum_{n\in\mathbb{Z}}f'((n+x)/L)$ are dominated uniformly on $x \in [0, 1]$ by constant multiples of $\sum_{|n|\ge 2}(|n|-1)^{-6} < \infty$ and $\sum_{|n|\ge 2}(|n|-1)^{-7} < \infty$.
  4. By the Weierstrass M-test, $\mathcal{P}_L \in C^1(\mathbb{R}/\mathbb{Z})$, so its Fourier series $\sum_{j \in \mathbb{Z}} c_j e^{i\tau j x}$ with $c_j = \int_0^1 \mathcal{P}_L(x)e^{-i\tau j x}\,dx = L\widehat{f}(j L)$ converges absolutely and pointwise everywhere to $\mathcal{P}_L(x)$ (and also $|\widehat{f}(j L)| \le \frac{C_2}{\zeta(2)L^2 j^2}$ ensures $\sum_{j \in \mathbb{Z}}|\widehat{f}(j L)| < \infty$). Evaluating at $x = 0$ using $f(0) = 0$ and $f(-v) = f(v)$ gives:
     $$2\sum_{d=1}^\infty f(d/L) = \sum_{d \in \mathbb{Z}} f(d/L) = L\sum_{j \in \mathbb{Z}}\widehat{f}(j L) = L\left[\widehat{f}(0) + 2\sum_{j=1}^\infty \widehat{f}(j L)\right],$$
     where
     $$\widehat{f}(\xi) := \int_{\mathbb{R}} f(v)e^{-i\tau\xi v}\,dv = 2\int_0^\infty v^{-6}e^{-1/v^2}\cos(\tau\xi v)\,dv, \qquad \widehat{f}(0) = 2c_0 = \Gamma(5/2) = \frac{3\sqrt{\tau/2}}{4}.$$
     Dividing by $2 L^6$ yields the exact transition identity:
     $$\boxed{\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} = L^{-5}\left[c_0 + \sum_{j\ge 1}\widehat{f}(j L)\right], \qquad c_0 = \frac{3\sqrt{\tau/2}}{8} \qquad (\forall L > 0).}$$

### 5.2 Mellin Regularization, Corrected Reflection Kernel, Contour Remainder Decay, and Monotonic Tail Ratios

1. **Why naive absolute Fubini on the unregularized cosine Mellin–Barnes kernel fails on $\operatorname{Re} z \in (0, 1)$**:
   For $\xi = 0$, $\widehat{f}(0) = \Gamma(5/2) = \frac{3\sqrt{\tau/2}}{4}$. For $\xi \ne 0$, set $t = v^{-2}$ ($v = t^{-1/2}$, $dv = \frac{1}{2}t^{-3/2}dt$) and $\omega := \tau|\xi| > 0$, so $\widehat{f}(\xi) = H(\omega)$ where
   $$H(u) := \int_0^\infty t^{3/2}e^{-t}\cos(u t^{-1/2})\,dt \qquad (u > 0).$$
   In `TC-054R`, it was claimed that on $z = a + i b$ with $a \in (0, 1)$, $|\sin(\tau z/4)\Gamma(1-z)|^{-1} \ll |b|^{a - 1/2}e^{-\tau|b|/4}$, allowing direct absolute Fubini interchange. That decay claim is **false**: as $|b| \to \infty$, $|\sin(\tau(a+ib)/4)| \sim \frac{1}{2}e^{\tau|b|/4}$ grows exponentially while $|\Gamma(1 - a - ib)| \sim \sqrt{\tau}\,|b|^{1/2-a}e^{-\tau|b|/4}$ decays at the same exponential rate, so the two exponential factors $e^{\pm \tau|b|/4}$ **cancel** and $|\sin(\tau z/4)\Gamma(1-z)|^{-1} \asymp |b|^{a - 1/2}$ has no exponential decay in $b$. In particular, on the line $z = 1/2 + i b$ ($b \in \mathbb{R}$),
   $$\bigl|\sin(\tau(1/2+ib)/4)\bigr| = \sqrt{\frac{\cosh(\tau b/2)}{2}}, \qquad \bigl|\Gamma(1/2 - i b)\bigr| = \sqrt{\frac{\tau/2}{\cosh(\tau b/2)}} \implies \frac{1}{\bigl|\sin(\tau z/4)\Gamma(1-z)\bigr|} = \frac{2}{\sqrt{\tau}} = [0.7978845608028653558798921198687637369517 \pm 1.73 \times 10^{-41}],$$
   which is an exact constant independent of $b$ (certified in 256-bit Arb at $b \in \{0, 1/2, 1, 2, 4\}$ in `verify_mellin_contour_and_reflection_identities_arb`).

2. **Real-variable integration by parts, $\epsilon$-regularization, and corrected reflection simplification**:
   - **Real-variable integration by parts**: Setting $u = 1/v$ and $\omega = \tau|\xi| > 0$, $\widehat{f}(\xi) = 2\int_0^\infty u^4 e^{-u^2}\cos(\omega u^{-1})\,du$. Since $\frac{d}{du}[\sin(\omega u^{-1})] = -\omega u^{-2}\cos(\omega u^{-1})$, writing $\cos(\omega u^{-1}) = -\frac{u^2}{\omega}\frac{d}{du}[\sin(\omega u^{-1})]$ and integrating by parts on $[\varepsilon, R]$ gives
     $$\widehat{f}(\xi) = +\frac{2}{\omega}\int_0^\infty (6u^5 - 2u^7)e^{-u^2}\sin(\omega u^{-1})\,du.$$
     For the conditional cosine transform $\int_0^U t^{z-1}\cos t\,dt$ on $0 < a = \operatorname{Re} z < 1$, integrating by parts on $[\varepsilon, U]$ with $\int_0^U t^{z-1}\cos t\,dt = [t^{z-1}\sin t]_0^U + (1-z)\int_0^U t^{z-2}\sin t\,dt$ (where $t^{z-1}\sin t = O(t^a) \to 0$ as $t \to 0^+$ and $t^{z-2}\sin t = O(t^{a-1}) \in L^1(0, 1) \cap L^1(1, \infty)$ for $0 < a < 1$) yields the absolutely convergent representation $(1-z)\int_0^\infty t^{z-2}\sin t\,dt = \Gamma(z)\cos(\tau z/4)$ on $0 < a < 1$.
   - **Regularized Mellin transform ($\epsilon \downarrow 0$)**: Equivalently, for $\epsilon \in (0, 1)$ and $u > 0$, define
     $$H_\epsilon(u) := \int_0^\infty t^{3/2}e^{-t - \epsilon u t^{-1/2}}\cos(u t^{-1/2})\,dt = \operatorname{Re}\int_0^\infty t^{3/2}e^{-t - (\epsilon + i)u t^{-1/2}}\,dt.$$
     For any $z = a + i b \in \mathbb{C}$ with $a > 0$, substituting $u = w t^{1/2}$ ($du = t^{1/2}dw$) yields the double integral
     $$\int_0^\infty \int_0^\infty t^{3/2 + a/2}e^{-t}\,w^{a - 1}e^{-\epsilon w}\,dw\,dt = \Gamma\!\left(\frac{5 + a}{2}\right)\Gamma(a)\,\epsilon^{-a} < \infty,$$
     so Fubini's theorem applies with **exact absolute integrability** for every $\epsilon \in (0, 1)$ and $a > 0$:
     $$\mathcal{M}[H_\epsilon](z) := \int_0^\infty u^{z-1}H_\epsilon(u)\,du = \Gamma\!\left(\frac{5 + z}{2}\right)\int_0^\infty w^{z-1}e^{-\epsilon w}\cos w\,dw = \Gamma(z)\,\Gamma\!\left(\frac{5 + z}{2}\right)(1 + \epsilon^2)^{-z/2}\cos\bigl(z\arctan(1/\epsilon)\bigr).$$
     Passing to the limit $\epsilon \to 0^+$ (justified on $0 < a < 1$ by dominated convergence on $u \in (0, 1]$ where $|H_\epsilon(u)| \le \Gamma(5/2)$ and integration by parts in $t$ on $u \in [1, \infty)$ where $H_\epsilon(u) = O(u^{-2})$ uniformly in $\epsilon \in (0, 1]$) gives the exact Mellin transform of $H(u)$ on $0 < \operatorname{Re} z < 1$:
     $$\mathcal{M}H(z) := \int_0^\infty u^{z-1}H(u)\,du = \Gamma(z)\cos(\tau z/4)\,\Gamma\!\left(\frac{5 + z}{2}\right).$$
   - **Corrected reflection identities**:
     Applying Euler's reflection formula $\Gamma(z)\Gamma(1-z) = \frac{\tau/2}{\sin(\tau z/2)}$ and the double-angle identity $\sin(\tau z/2) = 2\sin(\tau z/4)\cos(\tau z/4)$ gives
     $$\Gamma(1-z)\sin(\tau z/4) = \frac{\tau/2}{\Gamma(z)\sin(\tau z/2)}\sin(\tau z/4) = \frac{\tau/2}{2\,\Gamma(z)\cos(\tau z/4)}$$
     (correcting the mistyped denominator $\sin(\tau z/2)\Gamma(z)$ in the `TC-054R` text). Next, applying Euler's reflection formula at $w = \frac{5 + z}{2}$ (so $1 - w = \frac{-3 - z}{2}$ and $\sin(\tau w/2) = \sin(\frac{5\tau}{4} + \frac{\tau z}{4}) = \cos(\tau z/4)$) eliminates $\cos(\tau z/4)$ directly:
     $$\Gamma\!\left(\frac{5 + z}{2}\right)\cos(\tau z/4) = \frac{\tau/2}{\Gamma\!\left(\frac{-3 - z}{2}\right)},$$
     yielding the three equivalent exact representations of the Mellin kernel (all certified in 256-bit Arb at $z \in \{1/2 + i,\; 3/4 + 2i,\; -5/2 + i,\; -11/2 + 3i/2\}$):
     $$\boxed{\mathcal{M}H(z) = \Gamma(z)\cos(\tau z/4)\,\Gamma\!\left(\frac{5 + z}{2}\right) = \frac{(\tau/2)\,\Gamma(z)}{\Gamma\!\left(\frac{-3 - z}{2}\right)} = \frac{(\tau/2)^2}{\sin(\tau z/2)\,\Gamma(1 - z)\,\Gamma\!\left(\frac{-3 - z}{2}\right)}.}$$

3. **Contour shifting, [DLMF 5.8.3](https://dlmf.nist.gov/5.8#E3) Gamma lower bound, and explicit remainder bound $|R_M(\omega)| \to 0$**:
   - **Exponential decay of $\mathcal{M}H(a + i b)$ in $|b|$**: By Stirling's formula, $|\Gamma(\sigma + i y)| \sim \sqrt{\tau}\,|y|^{\sigma - 1/2}e^{-\tau|y|/4}$ as $|y| \to \infty$, so for any fixed $a \in \mathbb{R}$ and $|b| \ge 1$ (since $|\Gamma(a + ib)| \asymp_a |b|^{a - 1/2}e^{-\tau|b|/4}$ and $|\Gamma(\frac{-3-a}{2} - i\frac{b}{2})| \asymp_a |b|^{-a/2 - 2}e^{-\tau|b|/8}$),
     $$\bigl|\mathcal{M}H(a + i b)\bigr| = \frac{(\tau/2)\,\bigl|\Gamma(a + i b)\bigr|}{\bigl|\Gamma(\frac{-3-a}{2} - i\frac{b}{2})\bigr|} \;\asymp_a\; |b|^{\frac{3a}{2} + \frac{3}{2}}\,\exp\!\left(-\frac{\tau|b|}{8}\right) \qquad (a \in \mathbb{R},\;|b| \to \infty),$$
     which is **exponentially decaying** in $|b|$ on every vertical line $\operatorname{Re} z = a$. Hence Mellin inversion holds unconditionally on $a = c \in (0, 1)$:
     $$\widehat{f}(\xi) = H(\omega) = \frac{1}{i\tau}\int_{c - i\infty}^{c + i\infty}\mathcal{M}H(z)\,\omega^{-z}\,dz \qquad (0 < c < 1,\;\omega = \tau|\xi| > 0).$$
   - **Explicit non-asymptotic [DLMF 5.8.3](https://dlmf.nist.gov/5.8#E3) lower bound, horizontal-strip estimate, and shifted contour remainder**:
     For any $R \ge 1/2$ and $y \in \mathbb{R}$, the Weierstrass product for $|\Gamma(R + i y)|$ gives ([DLMF 5.8.3](https://dlmf.nist.gov/5.8#E3))
     $$\bigl|\Gamma(R + i y)\bigr| = \Gamma(R)\prod_{k=0}^\infty\left(1 + \frac{y^2}{(R + k)^2}\right)^{-1/2} \ge \Gamma(R)\prod_{k=0}^\infty\left(1 + \frac{y^2}{(1/2 + k)^2}\right)^{-1/2} = \frac{\Gamma(R)}{\sqrt{\cosh(\tau y/2)}} \ge \Gamma(R)\,e^{-\tau|y|/4}.$$
     For any integer $M \ge 2$, choose the vertical abscissa $a_M := -(2M + 3/2) \le -11/2$, midway between the poles at $-2M - 1$ and $-2M - 2$.
     - *Horizontal contour segments across the entire strip $a \in [a_M, c]$ ($c \in (0, 1)$, $B \ge 1$)*: Note that $R_2 = \frac{-3-a}{2} \ge \frac{1}{2}$ holds directly only for $a \le -4$. To obtain a non-asymptotic DLMF 5.8.3 bound valid across the **entire fixed strip** $a \in [a_M, c]$ (including $(-4, c]$), apply the functional recurrence $\Gamma(1 - z) = \frac{\Gamma(2 - z)}{1 - z}$ and $\Gamma(\frac{-3 - z}{2}) = \frac{\Gamma(\frac{3 - z}{2})}{(\frac{-3 - z}{2})(\frac{-1 - z}{2})(\frac{1 - z}{2})}$, where $R_1^* := 2 - a \ge 2 - c > 1 \ge 1/2$ and $R_2^* := \frac{3 - a}{2} \ge \frac{3 - c}{2} > 1 \ge 1/2$ lie in $[1/2, \infty)$ for all $a \in [a_M, c]$. Applying DLMF 5.8.3 to $\Gamma(2 - z)$ and $\Gamma(\frac{3 - z}{2})$ on $z = a \pm i B$ ($a \in [a_M, c]$, $B \ge 1$) together with $|\sin(\tau(a \pm i B)/2)| \ge \sinh(\tau B/2) \ge \frac{1}{4}e^{\tau B/2}$ gives
       $$\bigl|\mathcal{M}H(a \pm i B)\,\omega^{-a \mp i B}\bigr| \le \frac{4(\tau/2)^2\,\max(\omega^{-a_M}, \omega^{-c})\,\bigl(|1 - a| + B\bigr)\prod_{k \in \{-3, -1, 1\}}\frac{|k - a| + B}{2}}{\min_{a \in [a_M, c]}\!\bigl[\Gamma(2 - a)\,\Gamma(\frac{3 - a}{2})\bigr]}\,e^{-\tau B/8} = O_{M, c, \omega}\!\left(B^4 e^{-\tau B/8}\right)$$
       (and by uniform Stirling on $a \in [a_M, c]$, $\ll_{M, c, \omega} B^{3c/2 + 3/2}e^{-\tau B/8}$), so the horizontal contour integrals over $a \in [a_M, c]$ vanish as $B \to \infty$.
     - *Shifted vertical line $z = a_M + i b$ ($a_M = -(2M + 3/2) \le -11/2 < -4$, $M \ge 2$)*: On $\operatorname{Re} z = a_M$, both $R_1 := 1 - a_M = 2M + 5/2 \ge 13/2 \ge 1/2$ and $R_2 := \frac{-3 - a_M}{2} = M - 3/4 \ge 5/4 \ge 1/2$ satisfy $R_1, R_2 \ge 1/2$ directly, so DLMF 5.8.3 at $(R_1, -b)$ and $(R_2, -b/2)$ gives
       $$\bigl|\Gamma(1 - z)\bigr|\,\left|\Gamma\!\left(\frac{-3 - z}{2}\right)\right| \ge \Gamma(2M + 5/2)\,\Gamma(M - 3/4)\,e^{-3\tau|b|/8},$$
       while $\frac{\tau a_M}{2} = -(M + 1)\tau + \frac{\tau}{4}$ gives $\sin(\tau(a_M + i b)/2) = \sin(\frac{\tau}{4} + i\frac{\tau b}{2}) = \cosh(\tau b/2) \ge \frac{1}{2}e^{\tau|b|/2}$. Therefore, on $\operatorname{Re} z = a_M$:
     $$\bigl|\mathcal{M}H(a_M + i b)\,\omega^{-a_M - i b}\bigr| \le \frac{2(\tau/2)^2\,\omega^{2M + 3/2}}{\Gamma(2M + 5/2)\,\Gamma(M - 3/4)}\,e^{-\tau|b|/8},$$
     and integrating over $b \in \mathbb{R}$ using $\frac{1}{\tau}\int_{-\infty}^\infty e^{-\tau|b|/8}\,db = \frac{16}{\tau^2}$ establishes the explicit remainder bound:
     $$\boxed{\bigl|R_M(\omega)\bigr| := \left|\frac{1}{i\tau}\int_{a_M - i\infty}^{a_M + i\infty}\mathcal{M}H(z)\,\omega^{-z}\,dz\right| \le \frac{8\,\omega^{2M + 3/2}}{\Gamma(2M + 5/2)\,\Gamma(M - 3/4)} \;\xrightarrow[M\to\infty]{}\; 0 \qquad (\forall \omega > 0,\;M \ge 2).}$$
     At $\omega = 4$ ($\xi = 4/\tau$), the certified upper bound $\frac{8\cdot 4^{2M+3/2}}{\Gamma(2M+5/2)\Gamma(M-3/4)}$ decreases from `62.7883975743...` ($M = 2$) to `1.5875425976e-7` ($M = 8$), `1.3726791297e-28` ($M = 16$), and `5.2186250706e-85` ($M = 32$).
   - **Residues at the two disjoint simple pole families in $\operatorname{Re} z \le 0$**:
     By Cauchy's residue theorem, shifting the contour from $\operatorname{Re} z = c \in (0, 1)$ to $\operatorname{Re} z = a_M$ and letting $M \to \infty$ expresses $\widehat{f}(\xi)$ as the sum of residues of $\mathcal{M}H(z)\omega^{-z} = \Gamma(z)\cos(\tau z/4)\Gamma(\frac{5+z}{2})\omega^{-z}$:
     - *Even poles at $z = -2m$ ($m \ge 0$)*: Here $\operatorname*{Res}_{z=-2m}\Gamma(z) = \frac{(-1)^{2m}}{(2m)!} = \frac{1}{(2m)!} > 0$, $\Gamma(\frac{5-2m}{2}) = \Gamma(5/2 - m)$ is finite because $5/2 - m \notin \mathbb{Z}_{\le 0}$, and the alternating sign $(-1)^m$ comes from $\cos(\tau(-2m)/4) = \cos(-m\tau/2) = (-1)^m$ (or equivalently, in the reflected representation $\frac{(\tau/2)\Gamma(z)}{\Gamma((-3-z)/2)}$, from $\frac{\tau/2}{\Gamma(m - 3/2)} = (-1)^m\Gamma(5/2 - m)$; while at odd negative integers $z = -(2m+1)$, $\cos(\tau z/4) = 0$ cancels the simple pole of $\Gamma(z)$). Thus the residue at $z = -2m$ is
       $$t_{\mathrm{even}}(m) = \frac{(-1)^m\Gamma(5/2 - m)}{(2m)!}\omega^{2m}.$$
     - *Odd poles at $z = -5 - 2m$ ($m \ge 0$)*: Here $\frac{5+z}{2} = -m$, so $\operatorname*{Res}_{z=-5-2m}\Gamma(\frac{5+z}{2}) = \frac{2(-1)^m}{m!}$. Using $\frac{(\tau/2)\Gamma(z)}{\Gamma((-3-z)/2)}$ or $\Gamma(-5-2m)\cos(\tau(-5-2m)/4) = \frac{\tau/2}{2(5+2m)!\sin(\tau(-5-2m)/4)}$ with $\sin(\tau(-5-2m)/4) = -\sin(\tau/4 + m\tau/2) = -(-1)^m$, the $(-1)^m$ signs cancel to give the strictly negative residue
       $$-t_{\mathrm{odd}}(m) = -\frac{\tau}{2}\frac{\omega^{5+2m}}{m!\,(5 + 2m)!}.$$
     Hence, for all $\xi \in \mathbb{R}$ ($\omega = \tau|\xi|$):
     $$\boxed{\widehat{f}(\xi) = \sum_{m=0}^\infty \frac{(-1)^m\Gamma(5/2 - m)}{(2m)!}\omega^{2m} - \frac{\tau}{2}\sum_{m=0}^\infty \frac{\omega^{5+2m}}{m!\,(5+2m)!}, \qquad \omega = \tau|\xi|.}$$

4. **Sign analysis of $t_{\mathrm{even}}(m)$, monotonic tail ratios, and certified truncation bounds**:
   Let $t_{\mathrm{even}}(m) := \frac{(-1)^m\Gamma(5/2-m)}{(2m)!}\omega^{2m}$ and $t_{\mathrm{odd}}(m) := \frac{\tau}{2}\frac{\omega^{5+2m}}{m!\,(5+2m)!}$.
   - **Correction of the even-series sign description and intermediate $\Gamma(5/2 - m)$ recurrence**:
     For $m = 0$, $t_{\mathrm{even}}(0) = \Gamma(5/2) > 0$; for $m = 1$, $t_{\mathrm{even}}(1) = -\frac{1}{2}\Gamma(3/2)\omega^2 < 0$; and for **every** integer $m \ge 2$, iterating $\Gamma(w) = \frac{\Gamma(w+1)}{w}$ from $w = \frac{5}{2} - m$ up to $\frac{1}{2}$ gives
     $$\Gamma\!\left(\frac{5}{2} - m\right) = \frac{\Gamma(1/2)}{\left(-\frac{1}{2}\right)\left(-\frac{3}{2}\right)\cdots\left(\frac{5}{2} - m\right)} = \frac{(-1)^{m-2}\Gamma(1/2)}{\prod_{j=1}^{m-2}\!\left(j - \frac{1}{2}\right)},$$
     which has $m - 2$ negative factors in the denominator and therefore has sign $(-1)^{m-2} = (-1)^m$. Multiplying by $(-1)^m$ gives
     $$(-1)^m\Gamma(5/2 - m) = \bigl|\Gamma(5/2 - m)\bigr| = \frac{\Gamma(1/2)}{\prod_{j=1}^{m-2}\!\left(j - \frac{1}{2}\right)} > 0 \qquad (\forall m \ge 2),$$
     so **every even-series term $t_{\mathrm{even}}(m)$ for $m \ge 2$ is strictly positive** (not negative and not alternating). In particular, at $m = 3$, $\Gamma(5/2 - 3) = \Gamma(-1/2) = -2\Gamma(1/2) < 0$ and
     $$t_{\mathrm{even}}(3) = \frac{(-1)^3\Gamma(-1/2)\omega^6}{6!} = \frac{\Gamma(1/2)\,\omega^6}{360} > 0,$$
     with certified 256-bit Arb difference $[ \pm 2.34 \times 10^{-79}]$ at $\omega = 1$.
     The consecutive magnitude ratio for $m \ge 2$ is
     $$r_{\mathrm{even}}(m) := \left|\frac{t_{\mathrm{even}}(m+1)}{t_{\mathrm{even}}(m)}\right| = \frac{\omega^2}{(m - 3/2)(2m + 1)(2m + 2)}.$$
     For all $m \ge K \ge 1$, the denominator $(m + 1 - 3/2)(2m + 3)(2m + 4) = (m - 1/2)(2m + 3)(2m + 4)$ is positive and strictly increasing in $m$ (formally proved in Lean 4 theorem `abel_scaling_fourier_ratio_and_unequal_block_algebra`), so for every $m \ge K + 1$:
     $$r_{\mathrm{even}}(m) \le R_{\mathrm{even}}(K, \omega) := \frac{\omega^2}{(K - 1/2)(2K + 3)(2K + 4)}.$$
   - For the odd series, $t_{\mathrm{odd}}(m) > 0$ has consecutive magnitude ratio (for $m \ge 0$)
     $$r_{\mathrm{odd}}(m) := \left|\frac{t_{\mathrm{odd}}(m+1)}{t_{\mathrm{odd}}(m)}\right| = \frac{\omega^2}{(m + 1)(2m + 6)(2m + 7)},$$
      whose denominator is positive and strictly increasing for $m \ge 0$, so for every $m \ge K + 1$:
     $$r_{\mathrm{odd}}(m) \le R_{\mathrm{odd}}(K, \omega) := \frac{\omega^2}{(K + 2)(2K + 8)(2K + 9)}.$$
   - **Certified truncation rule in `evaluate_hat_f_hypergeometric_certified_arb`**:
     - If $R_{\mathrm{even}}(K, \omega) \le 1/2$ and $R_{\mathrm{odd}}(K, \omega) \le 1/2$ are **both certified via outward-rounded Arb comparison** (`R_even.upper() <= 0.5` and `R_odd.upper() <= 0.5`), then the omitted tail is bounded by the geometric series $\frac{1}{1 - 1/2} = 2$ times the first omitted term:
       $$\left|\sum_{m = K+1}^\infty t_{\mathrm{even}}(m)\right| \le 2\,\bigl|t_{\mathrm{even}}(K + 1)\bigr|, \qquad \left|\sum_{m = K+1}^\infty t_{\mathrm{odd}}(m)\right| \le 2\,\bigl|t_{\mathrm{odd}}(K + 1)\bigr|.$$
     - If `strict_K=True` and $1/2 < \max(R_{\mathrm{even}}, R_{\mathrm{odd}}) < 1$ is certified (`upper() < 1`), the exact geometric bound $\frac{|t_{\mathrm{even}}(K+1)|}{1 - R_{\mathrm{even}}(K, \omega)} + \frac{|t_{\mathrm{odd}}(K+1)|}{1 - R_{\mathrm{odd}}(K, \omega)}$ is used; if $\max(R_{\mathrm{even}}, R_{\mathrm{odd}})$ is not certified $< 1$, `strict_K=True` raises `ValueError`.
     - In default adaptive mode (`strict_K=False`), $K$ is automatically increased until both $R_{\mathrm{even}}(K, \omega) \le 1/2$ and $R_{\mathrm{odd}}(K, \omega) \le 1/2$ and the omitted tail is below $2^{-\text{prec\_bits}}$, with adaptive internal working precision compensating for large-$\omega$ alternating cancellation and pure-Arb radius inflation (`inflate_arb_with_nonneg_bound`, zero `float` conversions).

### 5.3 Reproduction of the `K_terms=1`, $\xi = 4/\tau$ ($\omega = 4$) Counterexample and Separate Series vs. Quadrature Accuracy

In `TC-054`, `evaluate_hat_f_hypergeometric_certified_arb` accepted arbitrary `K_terms >= 1` and unconditionally bounded the tail by $2(|t_{\mathrm{even}}(K+1)| + |t_{\mathrm{odd}}(K+1)|)$ without checking whether $R_{\mathrm{even}}(K, \omega) \le 1/2$. At `K_terms = 1` and $\xi = 4/\tau$ ($\omega = \tau\xi = 4$):
- The even tail ratio at $K = 1$ is
  $$R_{\mathrm{even}}(1, 4) = \frac{4^2}{(1 - 1/2)\cdot 5 \cdot 6} = \frac{16}{15} = 1.0666666666666666\ldots > 1,$$
  so the $2\times$ geometric tail hypothesis $R_{\mathrm{even}} \le 1/2$ is violated (in fact $R_{\mathrm{even}} > 1$).
- The unguarded `TC-054` formula produced:
  $$\text{old\_mid} = [-42.78140177774550645752327365017146694295 \pm 1.17 \times 10^{-39}],$$
  $$\text{old\_rad} = [40.08183091968871459730675945023946474865 \pm 3.12 \times 10^{-39}],$$
  $$\text{old\_upper} = [-2.699570680142662219242023650171466942949 \pm 1.62 \times 10^{-40}].$$
- However, for every $\xi \in \mathbb{R}$, $|\cos(\tau\xi v)| \le 1$ implies $|\widehat{f}(\xi)| \le \widehat{f}(0) = \Gamma(5/2) \approx 1.32934038817913702047$, so $\widehat{f}(4/\tau) \ge -\Gamma(5/2) \approx -1.32934038817913702047$. The old upper endpoint satisfies
  $$\text{old\_upper} = -2.6995706801\ldots < -\Gamma(5/2) = -1.3293403881\ldots,$$
  with certified contradiction gap $-\Gamma(5/2) - \text{old\_upper} = [1.370230291963525198768398037665608055851 \pm 3.24 \times 10^{-40}] > 0$.
- Meanwhile, the true value certified by both the repaired adaptive evaluator (`K_eff = 200`, working precision $529$ bits, `series_total_radius` $\approx 7.63 \times 10^{-77}$) and independent `acb.integral` quadrature on $[1/7, 32]$ is
  $$\widehat{f}(4/\tau) = [-0.7757751802167744117629682956314216290713 \pm 2.04 \times 10^{-41}],$$
  which lies strictly outside the old `K_terms=1` enclosure. Under the repaired implementation, `strict_K=True` at `K_terms=1, xi=4/tau` raises `ValueError` because $R_{\mathrm{even}}(1, 4) = 16/15 > 1$, while at `K_terms=4, xi=4/tau` ($R_{\mathrm{even}}(4, 4) = \frac{16}{462} = \frac{8}{231} < 1/2$, $R_{\mathrm{odd}}(4, 4) = \frac{16}{1632} = \frac{1}{102} < 1/2$) the strict enclosure `[-1.6049111020..., -0.5122016128...]` rigorously contains (`repaired_k4_contains_adaptive == True`) and overlaps (`repaired_k4_overlaps_adaptive == True`) the adaptive 256-bit enclosure.
- **Separate accuracy budgets for series truncation, working-precision arithmetic, 256-bit output serialization, and quadrature (`hat_f_sign_change_witnesses`)**:
  - **Series-tail accuracy (`series_truncation_radius`)**: Evaluated at `K_eff = 200`, where $R_{\mathrm{even}}, R_{\mathrm{odd}} \le 4.87 \times 10^{-6} \ll 1/2$; the geometric truncation bound $2(|t_{\mathrm{even}}(201)| + |t_{\mathrm{odd}}(201)|)$ is $0$ at $\xi = 0$ and $\le 1.66 \times 10^{-803}$ across $\xi \in \{1/2, 4/\tau, 1, 3/2, 2\}$.
  - **Working-precision arithmetic radius (`series_total_radius`)**: Evaluated at adaptive working precision $512$–$563$ bits; for exact rational inputs $\xi \in \{0, 1/2, 1, 3/2, 2\}$, `series_total_radius` ranges from $1.56 \times 10^{-154}$ ($\xi = 0$) down to $1.65 \times 10^{-162}$ (`1.6469137023751385e-162` at $\xi = 2$), while at $\xi = 4/\tau$ (where the 256-bit input $\xi$ has radius $\approx 1.2 \times 10^{-77}$), Lipschitz propagation yields `series_total_radius` $= 7.63 \times 10^{-77}$ (all serialized to 256-bit / 40-digit output balls with radius $\le 1.63 \times 10^{-40}$).
  - **Independent `acb.integral` quadrature accuracy (`quadrature_total_radius`)**: Integrates $2 v^{-6}e^{-1/v^2}\cos(\tau\xi v)$ on $[v_0, V_1] = [1/7, 32]$ at 128-bit quadrature precision and adds the analytic left-tail bound $2 v_0^{-3}e^{-1/v_0^2} = 686 e^{-49} \approx 3.60 \times 10^{-19}$ and right-tail bound $\frac{2}{5\cdot 32^5} = \frac{1}{83886080} \approx 1.1920928955 \times 10^{-8}$, giving `quadrature_total_radius` $= 1.1920928980 \times 10^{-8}$ and rigorously containing the 256-bit series ball (`quadrature_contains_series == True`, `series_overlaps_quadrature == True`, `series_minus_quadrature_contains_zero == True`).

| $\xi$ | Repaired 256-Bit Residue Series Enclosure of $\widehat{f}(\xi)$ (`K_eff=200`) | `working_prec_bits` | `series_truncation_radius` | `series_total_radius` | `quadrature_total_radius` | Independent `acb.integral` Quadrature on $[1/7, 32]$ | $\widehat{f}_{\mathrm{series}} \subseteq \widehat{f}_{\mathrm{quad}}$ & $0 \in \Delta$ | Sign |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: |
| $0$ | `[1.329340388179137020473625612505858887098 +/- 1.63e-40]` | $512$ | `0` | `1.56e-154` | `1.1920928980e-8` | `[1.3293404 +/- 3.57e-8]` | `True` / `True` | $> 0$ (`True`) |
| $1/2$ | `[-0.5628546550179851263755109492164491931001 +/- 4.04e-41]` | $525$ | `1.56e-1045` | `5.41e-155` | `1.1920928980e-8` | `[-0.5628547 +/- 5.69e-8]` | `True` / `True` | $< 0$ (`True`) |
| $4/\tau$ | `[-0.7757751802167744117629682956314216290713 +/- 2.04e-41]` | $529$ | `2.32e-1003` | `7.63e-77` | `1.1920928980e-8` | `[-0.7757752 +/- 3.21e-8]` | `True` / `True` | $< 0$ (`True`) |
| $1$ | `[-0.3668367826642069184644449070564857828859 +/- 4.03e-41]` | $538$ | `1.61e-924` | `4.20e-157` | `1.1920928980e-8` | `[-0.3668368 +/- 2.93e-8]` | `True` / `True` | $< 0$ (`True`) |
| $3/2$ | `[0.2636171831500303372338138695632955698496 +/- 2.39e-41]` | $550$ | `9.89e-854` | `1.71e-159` | `1.1920928980e-8` | `[0.2636172 +/- 2.88e-8]` | `True` / `True` | $> 0$ (`True`) |
| $2$ | `[0.1247126116325928138362162976104693467978 +/- 9.77e-42]` | $563$ | `1.66e-803` | `1.65e-162` | `1.1920928980e-8` | `[0.1247126 +/- 2.36e-8]` | `True` / `True` | $> 0$ (`True`) |

Because $\widehat{f}(\xi)$ is strictly negative at $\xi = 1/2, 4/\tau, 1$ and strictly positive at $\xi = 3/2, 2$, the non-zero Poisson modes cannot be dismissed by a Bochner positivity argument.

---

## 6. Rectangular-Block Decomposition, Unequal-Block Bounds, & Transition Proof Attempts (Attacks A & B)

### 6.1 Repaired Widely Unequal Rectangular-Block Bound

Decomposing $(r, s) \in \mathbb{Z}_{\ge 1}^2$ into dyadic rectangles $[A, 2A) \times [B, 2B)$ with $A = 2^a$, $B = 2^b$ ($a, b \ge 0$) gives the exact partition
$$Q_\lambda(X)^2 = \sum_{a, b \ge 0} B_{2^a, 2^b}(X), \qquad B_{A, B}(X) := \sum_{\substack{A \le r < 2A,\; B \le s < 2B \\ \gcd(r, s) = 1}}\frac{\lambda(r)\lambda(s)\,X^5}{(r s)^3}\sum_{d\ge 1} d^{-6}e^{-X^2(r^{-2}+s^{-2})/d^2}.$$

- **Defect in the old $\zeta(6)$ unequal-block derivation**:
  In `TC-054`, the pairwise magnitude $\frac{X^5}{(r s)^3}\sum_{d\ge 1}d^{-6}e^{-L^2/d^2}$ ($L = X\sqrt{r^{-2}+s^{-2}}$) was bounded by writing $u = L/d$ and claiming $u^5 e^{-u^2} < 1 \implies \sum_{d\ge 1}d^{-6}e^{-L^2/d^2} \le \zeta(6)L^{-5}$, and then claiming $\sum_{A \le r < 2A} r^2 \sum_{B \le s < 2B} s^{-3} \le A^3 B^{-2}$. Both steps were defective:
  1. First, $u^5 e^{-u^2} = L^5 d^{-5} e^{-L^2/d^2} < 1$ implies $d^{-6}e^{-L^2/d^2} < L^{-5}d^{-1}$, whose sum over $d \ge 1$ is $L^{-5}\sum_{d\ge 1}d^{-1} = \infty$, **not** $\zeta(6)L^{-5}$! Conversely, for large $L$, $\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} \sim c_0 L^{-5}$, whereas for small $L \to 0^+$, $L^5\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} \sim \zeta(6)L^5 \to 0$, so $L^5\sum_{d\ge 1} d^{-6}e^{-L^2/d^2}$ is bounded by a uniform constant $C_*$, not $\zeta(6)$ on all of $L > 0$.
  2. Second, $\sum_{A \le r < 2A} r^2 = \frac{(2A-1)2A(4A-1) - (A-1)A(2A-1)}{6} = \frac{7}{3}A^3 - \frac{3}{2}A^2 + \frac{1}{6}A < \frac{7}{3}A^3$, which carries the factor $\frac{7}{3} > 1$ (e.g., at $A = 2$, $2^2 + 3^2 = 13 > 8 = 2^3$).

- **Repaired unconditional proof of the unequal-block bound**:
  1. **Unimodal $d$-sum bound**: For fixed $L > 0$, the continuous profile $\phi_L(t) := t^{-6}e^{-L^2/t^2}$ on $(0, \infty)$ has derivative $\phi_L'(t) = 2 t^{-7}(L^2/t^2 - 3)e^{-L^2/t^2}$, so $\phi_L(t)$ is strictly increasing on $(0, L/\sqrt{3})$ and strictly decreasing on $(L/\sqrt{3}, \infty)$, with unique global maximum at $t_* = L/\sqrt{3}$:
     $$\max_{t > 0}\phi_L(t) = \phi_L(L/\sqrt{3}) = 27 e^{-3} L^{-6}.$$
     By the standard unimodal integral comparison $\sum_{d\ge 1}\phi_L(d) \le \int_0^\infty \phi_L(t)\,dt + \max_{t > 0}\phi_L(t)$:
     $$\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} \le c_0 L^{-5} + 27 e^{-3} L^{-6} \qquad (\forall L > 0).$$
     For $L \ge 1$, multiplying by $L^5$ and using $L^{-1} \le 1$ gives $L^5\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} \le c_0 + 27 e^{-3}$. For $0 < L \le 1$, since $e^{-L^2/d^2} \le 1$ and $L^5 \le 1$, we have $L^5\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} \le \zeta(6)L^5 \le \zeta(6)$, where $\zeta(6) = \frac{\tau^6}{60480} \in [1.017343061984449139714517929790920527902 \pm 1.83 \times 10^{-40}]$. Therefore, for **all** $L > 0$:
     $$L^5\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} \le C_* := \max\bigl\{\zeta(6),\; c_0 + 27 e^{-3}\bigr\} = c_0 + 27 e^{-3} \in [2.008921040021894970679058028804597412605 \pm 2.00 \times 10^{-39}].$$
  2. **Finite block sums over $r$ and $s$**: For integers $A, B \ge 1$ (assuming $B \ge A$ by symmetry, and using $(r^2 + s^2)^{-5/2} \le s^{-5}$):
     $$\frac{X^5}{(r s)^3}\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} = \frac{(r s)^2}{(r^2 + s^2)^{5/2}}\,L^5\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} \le C_*\,\frac{r^2}{s^3}.$$
     Summing over $A \le r < 2A$ gives (formally proved in Lean 4 theorem `abel_scaling_fourier_ratio_and_unequal_block_algebra` via `sum_range_sq_mul_six_aux`):
     $$\sum_{r=A}^{2A-1} r^2 = \frac{(2A-1)2A(4A-1) - (A-1)A(2A-1)}{6} = \frac{7}{3}A^3 - \frac{3}{2}A^2 + \frac{1}{6}A < \frac{7}{3}A^3 \qquad (\forall A \ge 1).$$
     Summing over $B \le s < 2B$: for $B = 1$, $\sum_{s=1}^1 s^{-3} = 1 = B^{-2}$; for $B \ge 2$, isolating $s = B$ and bounding $\sum_{s=B+1}^{2B-1} s^{-3} \le \int_B^\infty u^{-3}\,du = \frac{1}{2 B^2}$ gives (formally proved in Lean 4 theorem `abel_scaling_fourier_ratio_and_unequal_block_algebra`)
     $$\sum_{s=B}^{2B-1} s^{-3} \le \frac{1}{B^3} + \frac{1}{2 B^2} = \frac{2 + B}{2 B^3} \le \frac{1}{B^2} \qquad (\forall B \ge 2).$$
     Combining these bounds yields the unconditional unequal-block theorem valid for all integers $A, B \ge 1$ and all $X > 0$:
     $$\boxed{\bigl|B_{A, B}(X)\bigr| \le \frac{7}{3}C_*\,\frac{\min(A, B)^3}{\max(A, B)^2}, \qquad \frac{7}{3}C_* \in [4.687482426717754931584468733877393962745 \pm 2.00 \times 10^{-39}].}$$

### 6.2 Attack A: Coprime Euler-Series, Off-Critical Non-Cancellation, and Exact Separable Gaussian Decoupling

1. **Bivariate Coprime Dirichlet Series**:
   For $u, v \in \mathbb{C}$ with $\operatorname{Re} u > 1$ and $\operatorname{Re} v > 1$, expanding $\mathbf{1}_{\gcd(r,s)=1} = \sum_{e \mid \gcd(r,s)}\mu(e)$ with $r = e m$, $s = e n$ gives
   $$\mathcal{D}_\lambda(u, v) := \sum_{\gcd(r,s)=1}\frac{\lambda(r)\lambda(s)}{r^u s^v} = \sum_{e\ge 1}\frac{\mu(e)\lambda(e)^2}{e^{u+v}}\left(\sum_{m\ge 1}\frac{\lambda(m)}{m^u}\right)\left(\sum_{n\ge 1}\frac{\lambda(n)}{n^v}\right) = \frac{\zeta(2u)\,\zeta(2v)}{\zeta(u)\,\zeta(v)\,\zeta(u+v)}.$$
2. **Boundary Pole at $z = 0$ and Off-Critical Non-Cancellation**:
   - In 1D Mellin coordinates $z = a + i b$, $\mathcal{M}[Q_\lambda](z) = \frac{\Gamma(5/4-z/2)\zeta(1+2z)}{2\zeta(1/2+z)}$ has a simple pole at $z = 0$ (from $\zeta(1+2z) \sim \frac{1}{2z}$) with nonvanishing residue
     $$\operatorname*{Res}_{z=0}\mathcal{M}[Q_\lambda](z) = \frac{\Gamma(5/4)}{4\,\zeta(1/2)} \in [-0.1551682265483492584272379814757961069612 \pm 2.00 \times 10^{-40}] \ne 0.$$
   - At any hypothetical off-critical conjugate pair $(u, v) = (\rho, \bar{\rho})$ with $\rho = x + i y$ and $x \in (1/2, 1)$, we have $\operatorname{Re}(2\rho) = \operatorname{Re}(2\bar{\rho}) = 2x > 1$ and $u + v = 2x > 1$. Because $\zeta(w)$ has an absolutely convergent nonvanishing Euler product on $\operatorname{Re} w > 1$ (with $|\zeta(2\rho)| \ge \frac{\zeta(4x)}{\zeta(2x)} > 0$ and $\zeta(2x) > 1$), **neither the numerator $\zeta(2u)\zeta(2v)$ nor the coprimality factor $1/\zeta(u+v)$ can vanish at $(\rho, \bar{\rho})$ to cancel the off-critical poles of $\frac{1}{\zeta(u)\zeta(v)}$**.
3. **Exact Separable Gaussian Decoupling and Exact Integer Cutoff Semantics**:
   Retaining the exact Gaussian kernel $e^{-X^2(r^{-2}+s^{-2})/d^2} = e^{-X^2/(d^2 r^2)}\,e^{-X^2/(d^2 s^2)}$ and substituting $\mathbf{1}_{\gcd(r,s)=1} = \sum_{e \mid \gcd(r,s)}\mu(e)$ with $r = e m$, $s = e n$ ($\lambda(e m)\lambda(e n) = \lambda(m)\lambda(n)$) into $B_{A,B}(X)$ gives the exact decoupled identity:
   $$\boxed{B_{A,B}(X) = \sum_{1 \le e < 2\min(A,B)}\frac{\mu(e)}{e}\sum_{d\ge 1}\frac{1}{d}\,U_\lambda\!\left(\frac{X}{d e}; \frac{A}{e}\right)U_\lambda\!\left(\frac{X}{d e}; \frac{B}{e}\right),}$$
   where for real $M > 0$,
   $$U_\lambda(Y; M) := Y^{5/2}\sum_{\substack{m \in \mathbb{Z}_{\ge 1} \\ M \le m < 2M}}\frac{\lambda(m)}{m^3}e^{-Y^2/m^2} = Y^{5/2}\sum_{m = \max(1, \lceil M \rceil)}^{\lceil 2M \rceil - 1}\frac{\lambda(m)}{m^3}e^{-Y^2/m^2}.$$
   - **Removal of ad-hoc `1e-12` cutoff tolerance and reproduction of the $M = 1 + 2^{-42}$, $Y = 1$ counterexample**:
     In `TC-054`, `evaluate_1d_dyadic_sum_U_lambda_arb` computed the integer range $[M, 2M)$ using `math.ceil(M - 1e-12)` and `math.ceil(2*M - 1e-12)`. For $M = 1 + 2^{-42} = \frac{4398046511105}{4398046511104}$ and $Y = 1$, since $0 < 2^{-42} \approx 2.2737 \times 10^{-13} < 10^{-12}$, the true half-open interval is $[1 + 2^{-42}, 2 + 2^{-41})$, which contains the single integer $\{2\}$ and yields
     $$U_\lambda(1; 1 + 2^{-42})_{\text{true}} = \frac{\lambda(2)}{2^3}e^{-1/4} = -\frac{1}{8}e^{-1/4} = [-0.09735009788392560853064628337229008091210 \pm 3.47 \times 10^{-42}] < 0,$$
     whereas subtracting $10^{-12}$ shifted the endpoints below $1$ and $2$, selecting the integer $\{1\}$ and returning
     $$U_\lambda(1; 1 + 2^{-42})_{\text{old}} = \frac{\lambda(1)}{1^3}e^{-1} = +e^{-1} = [0.3678794411714423215955237701614608674458 \pm 1.12 \times 10^{-41}] > 0,$$
     an $O(1)$ error of opposite sign ($|\Delta| = [0.4652295390553679301261700535337509483579 \pm 7.67 \times 10^{-42}]$).
     In `TASK-TC-054R`, all `1e-12` tolerance shifts are removed: rational/integer/float inputs use exact `fractions.Fraction` arithmetic (`_exact_ceil_fraction(M)` and `_exact_ceil_fraction(2*M)`), while `arb` ball inputs that straddle an integer cutoff either enclose the union of all candidate endpoint configurations via `.union(...)` (`on_ambiguous_ball="enclose"`, default) or raise `ValueError` (`on_ambiguous_ball="raise"`).

| $(A, B, X)$ | Direct Block $B_{A,B}(X)$ | Separable Decoupled Formula | $0 \in \Delta$ | Repaired Unequal Bound $\frac{7}{3}C_*\frac{\min(A,B)^3}{\max(A,B)^2}$ | Bound Holds |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $(1, 1, 2)$ | `[0.103693354236 +/- 5.01e-13]` | `[0.103693354236 +/- 5.01e-13]` | `True` | `[4.687482426717754931584468733877393962745 +/- 7.00e-41]` | `True` |
| $(2, 2, 4)$ | `[0.0735522917142 +/- 5.35e-14]` | `[0.0735522917142 +/- 9.83e-14]` | `True` | `[9.374964853435509863168937467754787925490 +/- 1.41e-40]` | `True` |
| $(2, 4, 4)$ | `[0.0258021302529 +/- 1.17e-14]` | `[0.0258021302529 +/- 1.88e-14]` | `True` | `[2.343741213358877465792234366938696981372 +/- 4.66e-40]` | `True` |
| $(4, 4, 4)$ | `[-0.09965512039735 +/- 1.59e-15]` | `[-0.09965512039735 +/- 2.86e-15]` | `True` | `[18.74992970687101972633787493550957585098 +/- 2.80e-40]` | `True` |
| $(1, 8, 4)$ | `[-0.0004608160896 +/- 3.95e-14]` | `[-0.0004608160896 +/- 3.95e-14]` | `True` | `[0.07324191291746492080600732396683428066789 +/- 4.70e-43]` | `True` |
| $(2, 16, 4)$ | `[0.002650623875497 +/- 6.13e-16]` | `[0.002650623875497 +/- 9.34e-16]` | `True` | `[0.1464838258349298416120146479336685613358 +/- 2.10e-41]` | `True` |
| $(1, 16, 1)$ | `[-0.00011297588019448 +/- 6.15e-18]` | `[-0.00011297588019448 +/- 6.15e-18]` | `True` | `[0.01831047822936623020150183099170857016697 +/- 2.39e-42]` | `True` |
| $(1, 16, 16)$ | `[-0.00019611953 +/- 7.99e-12]` | `[-0.00019611953 +/- 7.99e-12]` | `True` | `[0.01831047822936623020150183099170857016697 +/- 2.39e-42]` | `True` |
| $(4, 32, 8)$ | `[-0.001780445434487 +/- 8.92e-16]` | `[-0.00178044543449 +/- 3.68e-15]` | `True` | `[0.2929676516698596832240292958673371226716 +/- 4.19e-41]` | `True` |
| $(8, 1, 4)$ | `[-0.0004608160896 +/- 3.95e-14]` | `[-0.0004608160896 +/- 3.95e-14]` | `True` | `[0.07324191291746492080600732396683428066789 +/- 4.70e-43]` | `True` |

### 6.3 Repaired Dyadic Abel Scaling, Divisor Collapse Note, and Global Stieltjes Energy Proof

1. **Correction of the dyadic Abel scaling exponent ($M^{1/2}$ vs $M^{-1/2}$) and Mellin pole refutation**:
   - Let $L_\lambda(t) := \sum_{1 \le m \le t}\lambda(m)$ ($L_\lambda(t) = 0$ for $t < 1$) and $g_Y(t) := Y^{5/2}t^{-3}e^{-Y^2/t^2}$. On the half-open dyadic interval $[M, 2M)$ ($M \ge 16$, so $\log\log M > 1$), Stieltjes integration by parts gives
     $$U_\lambda(Y; M) = L_\lambda(2M^-)\,g_Y(2M) - L_\lambda(M^-)\,g_Y(M) - \int_M^{2M} L_\lambda(t)\,g_Y'(t)\,dt.$$
     On $[M, 2M]$, $\sup_{t \in [M, 2M]} g_Y(t) \ll Y^{5/2}M^{-3}e^{-Y^2/(4M^2)} \ll M^{-1/2}\min(M/Y, (Y/M)^{5/2})$ and $\int_M^{2M}|g_Y'(t)|\,dt \ll M^{-1/2}\min(M/Y, (Y/M)^{5/2})$. Multiplying by the Korobov–Vinogradov–Walfisz bound $\sup_{t \in [M, 2M]}|L_\lambda(t)| \ll M\exp(-c\,\Phi(M))$ ($\Phi(t) = (\log t)^{3/5}(\log\log t)^{-1/5}$, derived from the classical Walfisz bound $|M(y)| \ll y\exp(-c'\Phi(y))$ via $L_\lambda(t) = \sum_{d \le \sqrt{t}} M(t/d^2)$) produces $M \cdot M^{-1/2} = M^{1/2}$, not $M^{-1/2}$:
     $$\boxed{\bigl|U_\lambda(Y; M)\bigr| \;\ll\; M^{1/2}\min\!\left(\frac{M}{Y}, \left(\frac{Y}{M}\right)^{5/2}\right)\exp\bigl(-c\,\Phi(M)\bigr) \qquad (M \ge 16),}$$
     while on the finite initial range $1 \le M < 16$, $|U_\lambda(Y; M)| \le \frac{7}{2}M^{1/2}\min(M/Y, (Y/M)^{5/2})$.
   - **Why the old $M^{-1/2}$ exponent is analytically impossible**: If $|U_\lambda(X; 2^j)| \ll 2^{-j/2}\min(2^j/X, (X/2^j)^{5/2})$ held across $j \ge 0$, summing over $j \ge 0$ would imply $|Q_\lambda(X)| = O(X^{-1/2})$ as $X \to \infty$, hence $\int_1^\infty |Q_\lambda(X)|^2\frac{dX}{X} < \infty$ ($\|Q_\lambda\|_0 < \infty$) and absolute convergence of $\mathcal{M}[Q_\lambda](z) = \int_0^\infty Q_\lambda(X)X^{-z}\frac{dX}{X}$ on $-1/2 < \operatorname{Re} z < 5/2$, contradicting the proved simple pole of $\mathcal{M}[Q_\lambda](z) = \frac{\Gamma(5/4-z/2)\zeta(1+2z)}{2\zeta(1/2+z)}$ at $z = 0$ with residue $\frac{\Gamma(5/4)}{4\zeta(1/2)} \approx -0.1551682265 \ne 0$.
   - **Tautological collapse of the global divisor sum**: Summing the decoupled block identity over all $a, b \ge 0$ and setting $q = d e$ yields
     $$\sum_{e\ge 1}\frac{\mu(e)}{e}\sum_{d\ge 1}\frac{1}{d}\,Q_\lambda\!\left(\frac{X}{d e}\right)^2 = \sum_{q\ge 1}\frac{\sum_{e\mid q}\mu(e)}{q}\,Q_\lambda\!\left(\frac{X}{q}\right)^2 = Q_\lambda(X)^2,$$
     because $\sum_{e\mid q}\mu(e) = \mathbf{1}_{q=1}$ vanishes for every $q \ge 2$. Thus the global identity reduces to the $q = 1$ term $Q_\lambda(X)^2 = Q_\lambda(X)^2$ and is not by itself a cancellation mechanism.

2. **Unconditional Global Stieltjes Proof of $|Q_\lambda(X)| \ll \sqrt{X}e^{-c_1\Phi(X)}$ ($X \ge 256$), Stretched-Exponential Energy ($Y \ge 256$), and Super-Polynomial Logarithmic Saving ($Y \ge 2$)**:
   - **Global Stieltjes representation**: Since $L_\lambda(1^-) = 0$ and $|L_\lambda(T)| \le T \implies X^{5/2}|L_\lambda(T)|T^{-3}e^{-X^2/T^2} \le X^{5/2}T^{-2} \to 0$ as $T \to \infty$, Stieltjes integration by parts on $[1, \infty)$ gives the exact identity for all $X > 0$:
     $$Q_\lambda(X) = -X^{5/2}\int_1^\infty L_\lambda(t)\,\frac{d}{dt}\bigl(t^{-3}e^{-X^2/t^2}\bigr)\,dt, \qquad \frac{d}{dt}\bigl(t^{-3}e^{-X^2/t^2}\bigr) = \bigl(2X^2 t^{-6} - 3 t^{-4}\bigr)e^{-X^2/t^2}.$$
   - **Exact scaling check**: Substituting $u = X/t$ ($t = X/u$, $dt = -X u^{-2}\,du$) into the unsigned kernel weighted by $t$ yields (endpoint antiderivative algebra verified in Lean 4 theorem `abel_scaling_fourier_ratio_and_unequal_block_algebra` and certified in 256-bit Arb):
     $$\int_0^\infty X^{5/2} t\,\left|\frac{d}{dt}\bigl(t^{-3}e^{-X^2/t^2}\bigr)\right|\,dt = \sqrt{X}\int_0^\infty u\,\bigl|3 - 2u^2\bigr|e^{-u^2}\,du = \left(\frac{1}{2} + 2 e^{-3/2}\right)\sqrt{X},$$
     where $I_{\mathrm{scale}} := \frac{1}{2} + 2 e^{-3/2} \in [0.9462603202968596578665609415280250426843 \pm 2.00 \times 10^{-40}]$.
   - **Splitting at $t = \sqrt{X}$ for $X \ge 256$ ($\sqrt{X} \ge 16$)**:
     1. **Lower range $1 \le t \le \sqrt{X}$**: Here $|L_\lambda(t)| \le t$ and $2X^2/t^2 - 3 \ge 2X - 3 > 0$, so with $w = X^2/t^2 \in [X, X^2]$ ($dw = -2X^2 t^{-3}\,dt$):
        $$X^{5/2}\int_1^{\sqrt{X}}\bigl|L_\lambda(t)\bigr|\,\left|\frac{d}{dt}\bigl(t^{-3}e^{-X^2/t^2}\bigr)\right|\,dt \le 2 X^{9/2}\int_1^{\sqrt{X}} t^{-5}e^{-X^2/t^2}\,dt = \sqrt{X}\int_X^{X^2} w e^{-w}\,dw \le \sqrt{X}\,(X + 1)e^{-X}.$$
     2. **Upper range $t \ge \sqrt{X} \ge 16$**: Since $\Phi(t) = (\log t)^{3/5}(\log\log t)^{-1/5}$ is positive and strictly increasing on $[16, \infty)$ ($\log\log t \ge \log\log 16 > 1$), $|L_\lambda(t)| \le C_{\mathrm{KV}}\,t\exp(-c_0\Phi(t)) \le C_{\mathrm{KV}}\,t\exp(-c_0\Phi(\sqrt{X}))$, so
        $$X^{5/2}\int_{\sqrt{X}}^\infty \bigl|L_\lambda(t)\bigr|\,\left|\frac{d}{dt}\bigl(t^{-3}e^{-X^2/t^2}\bigr)\right|\,dt \le C_{\mathrm{KV}}\left(\frac{1}{2} + 2 e^{-3/2}\right)\sqrt{X}\exp\bigl(-c_0\Phi(\sqrt{X})\bigr).$$
     Since $\Phi(\sqrt{X}) \ge 2^{-3/5}\Phi(X)$ for $X \ge 256$ and $(X+1)e^{-X} \ll e^{-c_1\Phi(X)}$, combining (1) and (2) gives the pointwise bound on $[256, \infty)$:
     $$\bigl|Q_\lambda(X)\bigr| \;\ll\; \sqrt{X}\exp\bigl(-c_1\Phi(X)\bigr) \qquad (\forall X \ge 256).$$
   - **Domain reconciliation for $E_\lambda(Y) := \int_Y^{\tau Y}|Q_\lambda(X)|^2\,\frac{dX}{X}$ ($Y \ge 256$ vs. $2 \le Y < 256$)**:
     - For $Y \ge 256$, every $X \in [Y, \tau Y]$ satisfies $X \ge 256$ ($\log\log X \ge \log\log Y > 1$), so squaring $|Q_\lambda(X)| \ll \sqrt{X}\exp(-c_1\Phi(X))$ and integrating against $\frac{dX}{X}$ over $[Y, \tau Y]$ proves the stretched-exponential energy bound:
       $$\boxed{E_\lambda(Y) = \int_Y^{\tau Y}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} \;\ll\; Y\exp\!\left(-2 c_2 (\log Y)^{3/5}(\log\log Y)^{-1/5}\right) \qquad (\forall Y \ge 256).}$$
       (Note that the raw expression $(\log Y)^{3/5}(\log\log Y)^{-1/5}$ is not extended down to $Y = 2$ where $\log\log 2 < 0$, and is stated exclusively on $Y \ge 256$ where $\log\log Y > 1$.)
     - On the compact range $2 \le Y < 256$, the unconditional pointwise bound $|Q_\lambda(X)| \le \zeta(3)X^{5/2}$ gives the explicit elementary bound
       $$E_\lambda(Y) \le \zeta(3)^2\int_Y^{\tau Y} X^4\,dX = \frac{\zeta(3)^2(\tau^5 - 1)}{5}\,Y^5 \qquad (2 \le Y < 256),$$
       with certified 256-bit Arb coefficient $\frac{\zeta(3)^2(\tau^5 - 1)}{5} \in [2829.665108928656654314420748974452322268 \pm 2.09 \times 10^{-37}]$. Since $2 \le Y < 256$ is compact and $\log Y \ge \log 2 > 0$, combining the $Y \ge 256$ stretched-exponential bound (where $\exp(-2c_2\Phi(Y)) \ll_D (\log Y)^{-D}$) with the compact bound on $[2, 256]$ yields the unconditional super-polynomial logarithmic saving across all $Y \ge 2$:
       $$\boxed{E_\lambda(Y) = \int_Y^{\tau Y}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} \;\ll_D\; \frac{Y}{(\log Y)^D} \qquad (\forall D > 0,\;Y \ge 2).}$$
   - **Strict separation of the three energy regimes**:
     1. **Unconditional super-polynomial logarithmic saving** ($E_\lambda(Y) \ll_D Y(\log Y)^{-D}$ for all $D > 0$, $Y \ge 2$): **PROVED** unconditionally above from the Korobov–Vinogradov–Walfisz bound and global Stieltjes integration by parts;
     2. **Fixed power saving** ($E_\lambda(Y) \ll Y^{1-\eta}$ for a fixed $\eta \in (0, 1)$): corresponds to a zero-free strip $\operatorname{Re}\rho \le 1 - \eta/2$, **NOT** established unconditionally;
     3. **Arbitrary subpower energy saving (`SUBGATE-TC-043A` target)** ($\forall \varepsilon > 0\;\exists C_\varepsilon < \infty\;\forall Y \ge 1,\;E_\lambda(Y) \le C_\varepsilon Y^\varepsilon$): equivalent by Proposition 3.1 to $\|Q_\lambda\|_\eta < \infty$ and $\|Q_\mu\|_\eta < \infty$ for all $\eta \in (0, 5/2)$, and hence to the Riemann Hypothesis; remains **`OPEN` (`rh_proved: false`)**.

### 6.4 Attack B: Dyadic Parity Annihilation and Cross-Scale Correlation

Writing every $n \ge 1$ uniquely as $n = 2^a m$ with $a \ge 0$ and $2 \nmid m$, complete multiplicativity $\lambda(2^a m) = (-1)^a\lambda(m)$ gives
$$Q_\lambda(X) = \sum_{a\ge 0}(-1)^a 2^{-a/2} Q_{\lambda,\mathrm{odd}}(X/2^a), \qquad Q_{\lambda,\mathrm{odd}}(X) := X^{5/2}\sum_{\substack{m\ge 1 \\ 2 \nmid m}}\frac{\lambda(m)}{m^3}e^{-X^2/m^2}.$$
Hence
$$Q_{\lambda,\mathrm{odd}}(X) = Q_\lambda(X) + 2^{-1/2}Q_\lambda(X/2), \qquad Q_\lambda(X) = \sum_{j\ge 0}(-1)^j 2^{-j/2}Q_{\lambda,\mathrm{odd}}(X/2^j),$$
where the inverse series converges absolutely because $2^{-j/2}|Q_{\lambda,\mathrm{odd}}(X/2^j)| \le \zeta(3)X^{5/2} 2^{-3j}$. Squaring $Q_{\lambda,\mathrm{odd}}(X) = Q_\lambda(X) + 2^{-1/2}Q_\lambda(X/2)$ and integrating against $\frac{dX}{X}$ on $[Y, \tau Y]$ yields:
$$\int_Y^{\tau Y}\bigl|Q_{\lambda,\mathrm{odd}}(X)\bigr|^2\,\frac{dX}{X} = \int_Y^{\tau Y}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} + \frac{1}{2}\int_{Y/2}^{\tau Y/2}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} + \sqrt{2}\int_Y^{\tau Y}Q_\lambda(X)Q_\lambda(X/2)\,\frac{dX}{X}.$$
Moreover, for every $\eta > -1/2$ (where $2^{-1/2-\eta} < 1$, including $\eta = 0$), Minkowski's inequality gives the two-sided norm equivalence
$$(1 - 2^{-1/2-\eta})\,\|Q_\lambda\|_\eta \le \|Q_{\lambda,\mathrm{odd}}\|_\eta \le (1 + 2^{-1/2-\eta})\,\|Q_\lambda\|_\eta.$$
On any hypothetical off-critical mode $X^{\rho - 1/2}$ ($\rho = x + i y$ with $x > 0$), the operator $I + 2^{-1/2}D_2$ acts by multiplication by $1 + 2^{-\rho}$, which satisfies
$$0 < 1 - 2^{-x} \le \bigl|1 + 2^{-\rho}\bigr| \le 1 + 2^{-x} < 2,$$
and therefore never vanishes in $\operatorname{Re}\rho = x > 0$.

---

## 7. Formal Lean 4 Audit (`formal/RiemannScope/LiouvilleSquareDilation.lean`)

The module [`formal/RiemannScope/LiouvilleSquareDilation.lean`](../../formal/RiemannScope/LiouvilleSquareDilation.lean) contains `21` definitions, `12` public theorems, and `16` private helper theorems (`49` total declarations), compiles cleanly under `lake build` with `0` `sorry` and `0` custom `axiom` declarations, and has its live `#check` and `#print axioms` output captured directly from `lake env lean` in [`data/tc_liouville_square_dilation.json`](../../data/tc_liouville_square_dilation.json):

| Theorem Name | Live `#check` Signature (`lake env lean`) | Live `#print axioms` | Mathematical Scope & External Analytic Inputs |
| :--- | :--- | :--- | :--- |
| `liouville_complete_multiplicativity_and_common_factor_cancellation_nat` | `∀ (omega_d omega_r omega_s : ℕ), (liouvilleSignFromOmega 0 = 1 ∧ liouvilleSignFromOmega 1 = -1) ∧ liouvilleSignFromOmega (omega_d + omega_r) = liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_r ∧ liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_d = 1 ∧ liouvilleSignFromOmega (omega_d + omega_r) * liouvilleSignFromOmega (omega_d + omega_s) = liouvilleSignFromOmega omega_r * liouvilleSignFromOmega omega_s` | `[propext, Classical.choice, Quot.sound]` | Exponent-model arithmetic theorem over `ℕ` and `ℤ` for `liouvilleSignFromOmega`. |
| `prime_power_square_divisor_moebius_liouville_inversion_nat` | `∀ (k : ℕ), squareDivisorMoebiusSum k = liouvilleSignFromOmega k ∧ squareDivisorInverseLiouvilleSum k = primePowerMoebius k` | `[propext, Classical.choice, Quot.sound]` | Exponent-model induction theorem over `ℕ` and `ℤ` for prime-power exponents $k \in \mathbb{N}$. |
| `actual_omega_factorization_and_liouville_common_factor_cancellation_nat` | `∀ {p m n d r s : ℕ}, p.Prime → ∀ (k : ℕ), m ≠ 0 → n ≠ 0 → d ≠ 0 → r ≠ 0 → s ≠ 0 → (n.factorization.sum fun x e => e) = natOmega n ∧ (natOmega 1 = 0 ∧ natOmega p = 1 ∧ natOmega (p ^ k) = k) ∧ natOmega (m * n) = natOmega m + natOmega n ∧ (liouvilleLambda 1 = 1 ∧ liouvilleLambda p = -1) ∧ liouvilleLambda (m * n) = liouvilleLambda m * liouvilleLambda n ∧ liouvilleLambda d * liouvilleLambda d = 1 ∧ liouvilleLambda (d * r) * liouvilleLambda (d * s) = liouvilleLambda r * liouvilleLambda s ∧ liouvilleArith.IsMultiplicative` | `[propext, Quot.sound, Classical.choice]` | Actual positive-integer arithmetic theorem over `ℕ` and `ℤ` connected to Mathlib's `ArithmeticFunction.cardFactors` and `Nat.factorization`: proves $\Omega(n) = \sum_{p^e \parallel n} e$, $\Omega(p^k) = k$, $\Omega(mn) = \Omega(m)+\Omega(n)$, complete multiplicativity $\lambda(mn)=\lambda(m)\lambda(n)$, $\lambda(d)^2=1$, $\lambda(dr)\lambda(ds)=\lambda(r)\lambda(s)$, and `liouvilleArith.IsMultiplicative` for all $m,n,d,r,s \ge 1$. |
| `actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat` | `∀ {p n : ℕ}, p.Prime → ∀ (k : ℕ), n ≠ 0 → (ArithmeticFunction.moebius (p ^ k) = primePowerMoebius k ∧ liouvilleLambda (p ^ k) = liouvilleSignFromOmega k) ∧ (primePowerActualMoebiusSquareSum p k = liouvilleLambda (p ^ k) ∧ primePowerActualInverseLiouvilleSquareSum p k = ArithmeticFunction.moebius (p ^ k)) ∧ ((liouvilleLambda n = n.factorization.prod fun q e => primePowerActualMoebiusSquareSum q e) ∧ ArithmeticFunction.moebius n = n.factorization.prod fun q e => primePowerActualInverseLiouvilleSquareSum q e) ∧ actualFlatMoebiusSquareArith.IsMultiplicative ∧ actualFlatInverseLiouvilleSquareArith.IsMultiplicative ∧ actualFlatMoebiusSquareDivisorSum (p ^ k) = primePowerActualMoebiusSquareSum p k ∧ actualFlatInverseLiouvilleSquareDivisorSum (p ^ k) = primePowerActualInverseLiouvilleSquareSum p k ∧ actualFlatMoebiusSquareDivisorSum n = liouvilleLambda n ∧ actualFlatInverseLiouvilleSquareDivisorSum n = ArithmeticFunction.moebius n` | `[propext, Classical.choice, Quot.sound]` | Actual flat square-divisor positive-integer arithmetic theorem over `ℕ` and `ℤ` connected to Mathlib's `ArithmeticFunction.moebius` and `Nat.divisors`: proves unconditionally (with no assumed surrogate `S`) that `actualFlatMoebiusSquareDivisorSum n = ∑ d ∈ squareDivisors n, μ(n/d^2)` and `actualFlatInverseLiouvilleSquareDivisorSum n = ∑ d ∈ squareDivisors n, μ(d)λ(n/d^2)` over `squareDivisors n = (Nat.divisors n).filter (fun d => d^2 ∣ n)` are multiplicative (`IsMultiplicative`), agree with the prime-power models on $p^k$, and equal `liouvilleLambda n` and `ArithmeticFunction.moebius n` for all $n \ne 0$. |
| `reversible_weighted_dilation_norm_and_grade_interval_equivalence` | `∀ (norm_f_sq d_pow_neg_4eta norm_f_d2_sq norm_lambda norm_mu zeta_1_2eta zeta_2_4eta B_mu B_lam int_0_1 sum_tau_blocks Z3_sq eta C_eta tau_pow_neg_eta : ℝ), ... → norm_f_d2_sq = d_pow_neg_4eta * norm_f_sq ∧ (norm_mu ≤ B_mu → norm_lambda ≤ zeta_1_2eta * B_mu) ∧ (norm_lambda ≤ B_lam → norm_mu ≤ zeta_1_2eta / zeta_2_4eta * B_lam) ∧ int_0_1 + sum_tau_blocks ≤ Z3_sq / (5 - 2 * eta) + C_eta / (1 - tau_pow_neg_eta)` | `[propext, Classical.choice, Quot.sound]` | Scalar real-inequality lemma in weight variable $\eta$: proves the reversible weighted norm implications from explicit real hypotheses; Minkowski's integral inequality is proved analytically in §3.2. |
| `euler_maclaurin_c2_and_subtransition_growing_range_exponent` | `∀ (f_prime_v_minus f_prime_v_plus N delta : ℝ), 0 ≤ f_prime_v_minus → f_prime_v_plus ≤ 0 → 1 / 12 * (\|f_prime_v_minus\| + \|f_prime_v_plus - f_prime_v_minus\| + \|(-f_prime_v_plus)\|) = (f_prime_v_minus - f_prime_v_plus) / 6 ∧ (N + 1) * (1 - delta) - N = 1 - (N + 1) * delta ∧ (1 - (N + 1) * delta < 0 ↔ 1 < (N + 1) * delta)` | `[propext, Classical.choice, Quot.sound]` | Scalar real-algebra lemma: proves the piecewise $C_2$ integral reduction and the subtransition growing-range exponent equivalence $(N+1)(1-\delta) - N = 1 - (N+1)\delta < 0 \iff (N+1)\delta > 1$. |
| `dyadic_parity_energy_and_off_critical_mode_nonvanishing` | `∀ (Q_X Q_half_X sqrt2 two_pow_neg_x abs_one_plus_two_pow_neg_rho : ℝ), sqrt2 ^ 2 = 2 → sqrt2 ≠ 0 → two_pow_neg_x < 1 → 1 - two_pow_neg_x ≤ abs_one_plus_two_pow_neg_rho → (Q_X + 1 / sqrt2 * Q_half_X) ^ 2 = Q_X ^ 2 + 1 / 2 * Q_half_X ^ 2 + sqrt2 * Q_X * Q_half_X ∧ 0 < 1 - two_pow_neg_x ∧ 0 < abs_one_plus_two_pow_neg_rho` | `[propext, Classical.choice, Quot.sound]` | Scalar real-algebra lemma: proves the pointwise dyadic parity square expansion and off-critical mode nonvanishing $0 < 1 - 2^{-x} \le |1 + 2^{-\rho}|$ for $\rho = x + i y$ with $x > 0$. |
| `abel_scaling_fourier_ratio_and_unequal_block_algebra` | `∀ (e_neg_3_2 K m B : ℝ) (A : ℕ), 1 ≤ K → K + 1 ≤ m → 2 ≤ B → 1 ≤ A → 1 / 2 * ((2 * (3 / 2) - 1) * e_neg_3_2 - (2 * 0 - 1)) + 1 / 2 * (0 - -(2 * (3 / 2) - 1) * e_neg_3_2) = 1 / 2 + 2 * e_neg_3_2 ∧ (0 < (K - 1 / 2) * (2 * K + 3) * (2 * K + 4) ∧ (K - 1 / 2) * (2 * K + 3) * (2 * K + 4) ≤ (m - 3 / 2) * (2 * m + 1) * (2 * m + 2) ∧ 0 < (K + 2) * (2 * K + 8) * (2 * K + 9) ∧ (K + 2) * (2 * K + 8) * (2 * K + 9) ≤ (m + 1) * (2 * m + 6) * (2 * m + 7)) ∧ (6 * ∑ r ∈ Finset.Ico A (2 * A), r ^ 2 + (A - 1) * A * (2 * A - 1) = (2 * A - 1) * (2 * A) * (4 * A - 1) ∧ 6 * ∑ r ∈ Finset.Ico A (2 * A), r ^ 2 + 9 * A ^ 2 = 14 * A ^ 3 + A ∧ 3 * ∑ r ∈ Finset.Ico A (2 * A), r ^ 2 < 7 * A ^ 3) ∧ 1 / B ^ 3 + 1 / (2 * B ^ 2) ≤ 1 / B ^ 2` | `[propext, Classical.choice, Quot.sound]` | Endpoint antiderivative, denominator monotonicity, and finite square-sum theorem: proves (1) the Stieltjes scaling endpoint antiderivative combination $\frac{1}{2} + 2e^{-3/2}$ (endpoint algebra; analytic integration/change of variables is outside Lean), (2) strict positivity and monotonicity of the even/odd Fourier residue series ratio denominators for $m \ge K + 1 \ge 2$, (3) the exact finite square-sum identities $6\sum_{A\le r < 2A} r^2 + (A-1)A(2A-1) = (2A-1)(2A)(4A-1)$, $6\sum_{A\le r < 2A} r^2 + 9A^2 = 14A^3 + A$, and $3\sum_{A\le r < 2A} r^2 < 7A^3$ for $A \ge 1$, and (4) the unequal-block rational inequality $B^{-3} + \frac{1}{2}B^{-2} \le B^{-2}$ for $B \ge 2$. |
| `actual_finite_prime_exclusion_sieve_identity_nat` | `@actual_finite_prime_exclusion_sieve_identity_nat : ∀ {p n N_P d : ℕ}, p.Prime → n ≠ 0 → N_P ≠ 0 → d ∣ n.gcd N_P → (liouvilleLambda (p * n) = -liouvilleLambda n ∧ liouvilleLambda (p * n) + liouvilleLambda n = 0) ∧ ArithmeticFunction.moebius d ^ 2 * liouvilleLambda (n / d) = liouvilleLambda n * ArithmeticFunction.moebius d ∧ actualPrimeExclusionSieveSum N_P n = if n.Coprime N_P then liouvilleLambda n else 0` | `[propext, Classical.choice, Quot.sound]` | Actual positive-integer arithmetic sieve theorem (`TASK-TC-055` / `TASK-TC-055R`): proves prime-dilation parity flip $\lambda(p n) = -\lambda(n)$, divisor reduction $\mu(d)^2\lambda(n/d) = \lambda(n)\mu(d)$ for $d \mid \gcd(n, N_P)$, and the exact finite-prime exclusion identity `actualPrimeExclusionSieveSum N_P n` $= \sum_{d\mid \gcd(n, N_P)}\mu(d)^2\lambda(n/d) = \mathbf{1}_{\gcd(n, N_P)=1}\lambda(n)$ via Mathlib's `ArithmeticFunction.sum_divisors_moebius_eq_one_iff`. |
| `prime_parity_control_multiplicative_and_moebius_separation_nat` | `@prime_parity_control_multiplicative_and_moebius_separation_nat : ∀ {p q m n d r s : ℕ}, p.Prime → q.Prime → q ≠ p → m ≠ 0 → n ≠ 0 → d ≠ 0 → r ≠ 0 → s ≠ 0 → (primeParityControl p 1 = 1 ∧ primeParityControl p p = -1 ∧ primeParityControl p q = 1) ∧ primeParityControl p (m * n) = primeParityControl p m * primeParityControl p n ∧ primeParityControl p d * primeParityControl p d = 1 ∧ primeParityControl p (d * r) * primeParityControl p (d * s) = primeParityControl p r * primeParityControl p s ∧ (primeParityControl p (p * n) = -primeParityControl p n ∧ primeParityControl p (p * n) + primeParityControl p n = 0) ∧ twoAdicParityControl 1 = 1 ∧ twoAdicParityControl 2 = -1 ∧ twoAdicParityControl 3 = 1 ∧ liouvilleLambda 3 = -1 ∧ actualFlatMoebiusSquareDivisorSum 3 = -1 ∧ twoAdicParityControl 3 ≠ actualFlatMoebiusSquareDivisorSum 3` | `[propext, Quot.sound, Classical.choice]` | Actual positive-integer arithmetic control theorem (`TASK-TC-055` / `TASK-TC-055R`): proves complete multiplicativity, unit square, common-factor cancellation, and parity flip at $p$ for `primeParityControl p n` $= (-1)^{v_p(n)}$, while proving at $n = 3$ that `twoAdicParityControl 3` $= +1 \ne -1 =$ `actualFlatMoebiusSquareDivisorSum 3` $= \sum_{d^2\mid 3}\mu(3/d^2)$. |
| `near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing` | `near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing : ∀ (K : ℕ → ℕ → ℝ) (bandSum : ℕ → ℝ) (D_E K_pm K_qrm : ℝ) (M h H : ℕ) {p q r m : ℕ}, (∀ (a b : ℕ), 2 * K a b ≤ K a a + K b b) → (∀ j ∈ Finset.range (2 * H + 1), bandSum j ≤ D_E) → p.Prime → q.Prime → r.Prime → m ≠ 0 → (2 * ∑ a ∈ Finset.range M, K a (a + h) ≤ ∑ a ∈ Finset.range M, K a a + ∑ a ∈ Finset.range M, K (a + h) (a + h) ∧ ∑ j ∈ Finset.range (2 * H + 1), bandSum j ≤ (2 * ↑H + 1) * D_E) ∧ (liouvilleLambda (p * m) = -liouvilleLambda m ∧ liouvilleLambda (q * r * m) = liouvilleLambda m ∧ liouvilleLambda (p * m) + liouvilleLambda (q * r * m) = 0 ∧ ↑(liouvilleLambda (p * m)) * K_pm + ↑(liouvilleLambda (q * r * m)) * K_qrm = ↑(liouvilleLambda m) * (K_qrm - K_pm)) ∧ 3 / 8 * (1 / 8) = 3 / 64 ∧ 1 / 2 * (1 - 2 / 3) = 1 / 6 ∧ (1 / 6) ^ 2 = 1 / 36` | `[propext, Classical.choice, Quot.sound]` | Finite-sum kernel bound and actual-integer opposite-parity pairing theorem (`TASK-TC-055` / `TASK-TC-055R`): proves off-diagonal sum domination $2\sum_{a < M}K(a, a+h) \le \sum_{a < M}K(a, a) + \sum_{a < M}K(a+h, a+h)$, the $(2H+1)D_E$ band bound, opposite-parity prime-semiprime pairing $\lambda(p m) + \lambda(q r m) = 0$ and $\lambda(p m)K_{pm} + \lambda(q r m)K_{qrm} = \lambda(m)(K_{qrm} - K_{pm})$ for actual primes $p, q, r \in \mathbb{N}$, and the rational constant identities $\frac{3}{8}\cdot\frac{1}{8} = \frac{3}{64}$, $\frac{1}{2}(1 - \frac{2}{3}) = \frac{1}{6}$, and $(\frac{1}{6})^2 = \frac{1}{36}$. |
| `pairing_counterexample_replacement_and_finite_reconstruction_tc055r` | `@pairing_counterexample_replacement_and_finite_reconstruction_tc055r : ∀ (g : ℕ → ℝ) (X4 K_10 K_11 K_a K_b r3 E_low E_high a b tauY : ℝ) (m T : ℕ) (a_ idx_b : ℕ), 0 ≤ X4 → 0 < K_11 → K_10 / K_11 < 1331 / 2890 → 0 ≤ K_b → r3 * E_low * K_b ≤ K_a → K_a ≤ r3 * E_high * K_b → 0 < a → a ≤ b → 1 ≤ m → m ≤ T → 2 * kernelPointwiseIntegrand g X4 a_ idx_b ≤ kernelPointwiseIntegrand g X4 a_ a_ + kernelPointwiseIntegrand g X4 idx_b idx_b ∧ (1089 * (1 / 10 ^ 2 - 1 / 11 ^ 2) = 189 / 100 ∧ 1331 / 1000 * (100 / 289) = 1331 / 2890 ∧ 1 - 1331 / 2890 = 1559 / 2890 ∧ 3 * (1 / 10) * (11 / 10) ^ 3 = 3993 / 10000 ∧ 3993 / 10000 < 1559 / 2890 ∧ 3993 / 10000 < (K_11 - K_10) / K_11) ∧ (\|K_a - K_b\| ≤ max \|r3 * E_low - 1\| \|r3 * E_high - 1\| * K_b ∧ 0 ≤ (b - a) / a * (b / a) ^ 3 * (3 + 2 * tauY ^ 2 / a ^ 2) * K_b) ∧ (2 / 4 * (4 / 6) * (6 / 8) = 1 / 4 ∧ 1 / 2 * (1 / 4) = 1 / 8 ∧ (1 / 8) ^ 2 = 1 / 64 ∧ 1 / (2 * 29 / 10 ^ 2) = 50 / 841 ∧ 1 / (2 * 2 ^ 2) = 1 / 8 ∧ 50 / 841 < 1 / 8) ∧ (1 ≤ T / m ∧ T / m ≤ T ∧ ∀ (r : ℕ), r ≤ T / m ↔ m * r ≤ T)` | `[propext, Classical.choice, Quot.sound]` | `TASK-TC-055R` formal bridge theorem: proves (1) pointwise AM-GM $2 X_4 g(a)g(b) \le X_4 g(a)^2 + X_4 g(b)^2$ for `kernelPointwiseIntegrand`, (2) the floating-point-free rational inequalities refuting the retired `TC-055` Lemma 6.1 bound at $(Y, p, q, r, m, n) = (33, 11, 2, 5, 1, 11)$ ($1089(10^{-2}-11^{-2}) = 189/100$, $\frac{1559}{2890} > \frac{3993}{10000}$, and $K_{10}/K_{11} < \frac{1331}{2890} \implies \frac{K_{11}-K_{10}}{K_{11}} > \frac{3993}{10000}$), (3) the two-sided ratio enclosure $|K_a - K_b| \le \max(|r_0^3 E_{\mathrm{low}} - 1|, |r_0^3 E_{\mathrm{high}} - 1|)K_b$ and nonnegativity of the transition relative-gap factor, (4) the $S = \{3, 5, 7\}$ parity-control rational constants ($\frac{1}{4}, \frac{1}{8}, \frac{1}{64}$) and the $u = 2.9$ cutoff fraction inequality $\frac{50}{841} < \frac{1}{8}$, and (5) the finite $T$-truncation $m$-dependent inner cutoff equivalence $r \le \lfloor T/m \rfloor \iff m r \le T$ for $1 \le m \le T$. |

---

## 8. Simultaneous $\tau$-Compatibility, Pairing Bound Repair, Full-Space Operator Norm Obstruction, and Finite Energy Reconstruction (`TASK-TC-055` & `TASK-TC-055R`)

Full derivations, proofs, counterexamples, and 256-bit Arb certifications for `TASK-TC-055` and `TASK-TC-055R` are recorded in [`docs/reviews/TC_055_SIMULTANEOUS_TAU_COMPATIBILITY.md`](./TC_055_SIMULTANEOUS_TAU_COMPATIBILITY.md) and sections 8–13 of [`data/tc_liouville_square_dilation.json`](../../data/tc_liouville_square_dilation.json):

1. **Exact Removable Trivial-Zero Cancellation in $\mathcal{M}[Q_\lambda](z)$ and Pole/Zero Locations of $D_\lambda(s)$ (§3)**:
   At $z_m = -(2m + 1/2)$ ($m \ge 1$), $\lim_{z \to -(2m + 1/2)}\frac{\zeta(1 + 2z)}{\zeta(1/2 + z)} = \frac{2\zeta'(-4m)}{\zeta'(-2m)} = \frac{2(-1)^m(4m)!\,\zeta(4m + 1)}{\tau^{2m}(2m)!\,\zeta(2m + 1)} \ne 0$, while $D_\lambda(s) = \zeta(2s)/\zeta(s)$ has a simple pole at $s = 1/2$ (from $\zeta(2s)$) and a simple zero at $s = 1$ (from $1/\zeta(s)$).
2. **Simultaneous Finite-Prime Exclusion, $u = 2.9$ Cutoff Counterexample Repair, and Exact Full-Space Operator Norm Obstruction (§3.3–§4)**:
   From $\lambda(p n) = -\lambda(n)$, $Q_{\lambda, P}(X) = \prod_{p \in P}(I + p^{-1/2}S_p)Q_\lambda(X) = \sum_{d \mid N_P}\frac{|\mu(d)|}{\sqrt{d}}Q_\lambda(X/d)$ with $P$-smooth inverse $Q_\lambda(X) = \sum_{m \in \mathcal{S}(P)}\frac{\lambda(m)}{\sqrt{m}}Q_{\lambda, P}(X/m)$. At non-integer $u = 2.9$, $\sum_{n > 2.9}n^{-3} = \zeta(3) - 9/8 = 0.0770569\dots > \frac{1}{2(2.9)^2} = \frac{50}{841} = 0.059453\dots$, repaired by the floor-guarded bound $\sum_{n > u}n^{-3} \le \frac{1}{2\lfloor u \rfloor^2}$ ($u \ge 1$) and least-prime coprime bound $|R_{\lambda, P_u}(w)| \le \frac{w^{5/2}}{2(q_{>u}-1)^2} \le \frac{w^{5/2}}{2\lfloor u \rfloor^2}$ ($u \ge 2$). On the full weighted space $\mathcal{H}_\eta = L^2((0,\infty), X^{-2\eta}\,dX/X)$ ($\eta > 0$), $\mathbb{Q}$-linear independence of $\{\log p : p \le u\}$ and continuous Kronecker simultaneous approximation (Aoyama–Nakamura, `arXiv:1204.4043`, p. 9) prove the exact operator-norm identity $\|\mathcal{P}_u^{-1}\|_{\mathcal{H}_\eta \to \mathcal{H}_\eta} = \prod_{p \le u}(1 - p^{-1/2-\eta})^{-1}$, showing that no signed improvement of the full-space operator norm exists.
3. **Integrated Energy Kernel $K_Y(m, n)$, Diagonal Asymptotic $D_E(Y)$, and Near-Diagonal Band Bound (§5)**:
   $D_E(Y) = \frac{3\sqrt{\tau}}{64}\log\tau + R_{D, E}(Y)$ with $|R_{D, E}(Y)| \le C_{D, 2}Y^{-2}$ ($C_{D, 2} \approx 0.07974241$) for all $Y > 0$, and $\sum_{|m - n| \le H} K_Y(m, n) \le (2H + 1)D_E(Y)$ for every integer $H \ge 0$.
4. **Retirement of False Uniform Pairing Bound and Proved Replacement Theorems (§6)**:
   At $Y = 33, p = 11, q = 2, r = 5, m = 1, n = 11$ ($q r = 10$), the normalized kernel difference is $\frac{|K_{33}(11, 11) - K_{33}(10, 11)|}{K_{33}(11, 11)} \approx 0.81942528 > \frac{1559}{2890} > \frac{3993}{10000} = 0.3993$, refuting and retiring the uniform `TC-055` Lemma 6.1 bound (whose proof consumed $e^{-X^2/u^2}$ in $|(2w^2-3)e^{-w^2}| \le 3$ while also retaining $e^{-X^2/u_2^2}$). Theorem 6.1 replaces it with the unconditional two-sided integrand-ratio enclosure $r_0^3 e^{-(\tau Y)^2\Delta}K_Y(b, n) \le K_Y(a, n) \le r_0^3 e^{-Y^2\Delta}K_Y(b, n)$ and the transition relative-gap bound $|K_Y(a, n) - K_Y(b, n)| \le \frac{b-a}{a}(\frac{b}{a})^3(3 + \frac{2\tau^2 Y^2}{a^2})K_Y(b, n)$.
5. **Repaired Multiplicative Parity Controls $a_2(n)$ and $a_{\{3,5,7\}}(n)$ (§7)**:
   The unimodal constant for $Q_{\mathbf{1}}(X)$ is $C_{1,\mathrm{uni}} = 2(3/(2e))^{3/2} = \frac{1}{\sqrt{2}}(3/e)^{3/2} \approx 0.81983256 < (3/e)^{3/2}$, while the second-order Euler–Maclaurin bound $|Q_{\mathbf{1}}(w) - \sqrt{w}/2| \le 3w^{-3/2}$ proves $Q_{a_2}(X) = \frac{\sqrt{X}}{6} + O(X^{-1/2})$ and $E_{a_2}(Y) = \frac{\tau - 1}{36}Y + O(1)$. For $S = \{3, 5, 7\}$, the Euler-factor mean is $\frac{2}{4}\cdot\frac{4}{6}\cdot\frac{6}{8} = \frac{1}{4}$, giving $Q_{a_{\{3,5,7\}}}(X) \sim \frac{1}{8}\sqrt{X}$ and $E_{a_{\{3,5,7\}}}(Y) \sim \frac{\tau - 1}{64}Y$.
6. **Noncircular Finite Arithmetic Proof Attempt via $T$-Truncated Observable $Q_{\lambda, T}(X)$ (§8)**:
   For any finite truncation $T \ge 1$, $Q_{\lambda, T}(X) = \sum_{m \in \mathcal{S}(P), m \le T}\frac{\lambda(m)}{\sqrt{m}}Q_{\lambda, P, \lfloor T/m \rfloor}(X/m)$ holds with the exact $m$-dependent inner cutoff $\lfloor T/m \rfloor$, and the truncation tail energy satisfies $\mathcal{R}_{\mathrm{tail}}(Y, T) \le \frac{(\tau^5 - 1)Y^5}{20 T^4} = O(1)$ at $T(Y) = \lceil Y^{5/4} \rceil$. Decomposing $E_{\lambda, T(Y)}(Y) = E_{\mathrm{same}\text{-}r}(Y; T, P_u) + E_{\mathrm{diff}\text{-}r}(Y; T, P_u)$ shows that `SUBGATE-TC-043A` reduces to overcoming the two-part obstruction between smooth-fiber Kronecker norm growth for large $u$ and the off-diagonal coprime cofactor sum $E_{\mathrm{diff}\text{-}r}(Y; T(Y), P_u)$ for small $u$, keeping `SUBGATE-TC-043A: OPEN` (`rh_proved: false`).

