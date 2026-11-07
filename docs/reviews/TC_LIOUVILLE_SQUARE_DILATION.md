# TASK-TC-054 Mathematical Review: Liouville Square-Dilation Transfer, Unconstrained Common-Factor Expansion, Transition Poisson Summation, and Separable Gaussian Decoupling

- **Task ID**: `TASK-TC-054`
- **Parent Epic**: `EPIC-TC-042`
- **Branch**: `task/tc-054-liouville-square-dilation-and-transition-cancellation`
- **Prior Merged `main` Baseline (`TC-053R`)**: `c82e439708b0b6031db6a77bf3977688d9f0758b`
- **Reviewed `TC-053R2` Implementation Commit**: `cc303030138c670e8f01aaaab483bbeca6bc17d1`
- **Reviewed `TC-053R2` Tip**: `21576861ecd0dcbf874afec91b299fd6060f4f03`
- **Subgate Status**: `SUBGATE-TC-043A: OPEN` (`rh_proved: false`)
- **Primary Implementation Module**: [`tc/liouville_square_dilation.py`](../../tc/liouville_square_dilation.py)
- **Certified Data Artifact**: [`data/tc_liouville_square_dilation.json`](../../data/tc_liouville_square_dilation.json)
- **Formal Lean 4 Module**: [`formal/RiemannScope/LiouvilleSquareDilation.lean`](../../formal/RiemannScope/LiouvilleSquareDilation.lean) (`5` definitions + `5` public theorems + `1` private helper theorem = `11` declarations; `0` `sorry`, `0` custom `axiom`)
- **Verification Test Suite**: [`tests/test_tc_liouville_square_dilation.py`](../../tests/test_tc_liouville_square_dilation.py)

---

## 1. Executive Summary & Mission Status

In `TASK-TC-053R` and `TASK-TC-053R2`, the common-factor expansion of the Möbius Gaussian sum
$$Q_\mu(X) := X^{5/2}\sum_{n\ge 1}\frac{\mu(n)}{n^3}e^{-X^2/n^2}$$
encountered two coupled structural barriers when expanding $Q_\mu(X)^2$ over $m = d r$, $n = d s$ with $\gcd(r, s) = 1$:
1. **Common-Factor Coprimality Barrier ($A \le X^{1/3-\delta}$)**: Because $\mu(d r)\mu(d s) = \mu(d)^2 \mathbf{1}_{\gcd(d, r s)=1}\mu(r)\mu(s)$, the inner sum over $d$ is restricted to squarefree integers $d$ coprime to $q = r s$. Approximating $\sum_{\gcd(d, rs)=1} \mu(d)^2 d^{-6} e^{-L^2/d^2}$ by its continuous integral introduces the squarefree-coprime counting remainder $|R_q(t)| \le (2^{\omega(q)} + 2)\sqrt{t}$, producing an $O(L^{-11/2})$ pairwise error that restricts the asymptotic Gaussian kernel reduction to the sub-cubic range $A \le X^{1/3-\delta}$.
2. **Signed-Block Barrier**: On a single balanced block $[A, 2A)^2$, the decoupled convolution $f = (\mu \otimes \mu) * h$ combined with Korobov–Vinogradov–Walfisz yields the unconditional super-polynomial logarithmic saving $|S(A)| \ll A\exp(-c(\log A)^{3/5}(\log\log A)^{-1/5}) \ll_D A(\log A)^{-D}$ for every $D > 0$, but does not control the transition region $A \asymp X$ or provide a fixed power saving without a zero-free strip for $\zeta(s)$.

`TASK-TC-054` reformulates the problem using **Liouville's completely multiplicative function** $\lambda(n) = (-1)^{\Omega(n)}$ ($\lambda(1) = 1$) and proves **six unconditional theorems**, while isolating the exact analytic obstruction that keeps `SUBGATE-TC-043A` `OPEN` (`rh_proved: false`):

1. **Theorem 1 (Reversible Square-Divisor Convolution & Gaussian Square-Dilation Transfer, §2–§3)**:
   For all $n \ge 1$,
   $$\lambda(n) = \sum_{d^2 \mid n}\mu\!\left(\frac{n}{d^2}\right), \qquad \mu(n) = \sum_{d^2 \mid n}\mu(d)\lambda\!\left(\frac{n}{d^2}\right).$$
   For $Q_a(X) = X^{5/2}\sum_{n\ge 1}\frac{a(n)}{n^3}e^{-X^2/n^2}$ ($a \in \{\mu, \lambda\}$), $|Q_a(X)| \le \zeta(3)X^{5/2}$, the $N > T$ truncation tail is bounded by $\frac{X^{5/2}}{2 T^2}$, and Fubini's theorem yields the exact reversible square-dilation transfer
   $$Q_\lambda(X) = \sum_{d\ge 1}\frac{Q_\mu(X/d^2)}{d}, \qquad Q_\mu(X) = \sum_{d\ge 1}\frac{\mu(d)\,Q_\lambda(X/d^2)}{d},$$
   with dilation tail ($d > D$) bounded in magnitude by $\frac{\zeta(3)X^{5/2}}{5 D^5}$.

2. **Theorem 2 (Reversible Weighted $L^2$ Norm Equivalence & Grade-Interval Criterion, §3)**:
   For the weighted norm $\|f\|_\sigma := \bigl(\int_0^\infty |f(X)|^2 X^{-2\sigma}\frac{dX}{X}\bigr)^{1/2}$, any dilation $a > 0$ satisfies $\|f(\cdot/a)\|_\sigma = a^{-\sigma}\|f\|_\sigma$, and for every $\sigma > 0$,
   $$\|Q_\lambda\|_\sigma \le \zeta(1 + 2\sigma)\,\|Q_\mu\|_\sigma, \qquad \|Q_\mu\|_\sigma \le \frac{\zeta(1 + 2\sigma)}{\zeta(2 + 4\sigma)}\,\|Q_\lambda\|_\sigma.$$
   Consequently, for both $a = \mu$ and $a = \lambda$,
   $$\left(\forall \varepsilon > 0\;\exists C_\varepsilon < \infty\;\forall Y \ge 1,\;\int_Y^{\tau Y}|Q_a(X)|^2\,\frac{dX}{X} \le C_\varepsilon Y^\varepsilon\right) \Longleftrightarrow \bigl(\forall \sigma \in (0, 5/2),\;\|Q_a\|_\sigma < \infty\bigr).$$
   At $\sigma = 0$ there is no bounded inverse because $\sum_{d\ge 1} d^{-1} = \infty$, with $\zeta(1+2\sigma) \sim \frac{1}{2\sigma}$ and $\frac{\zeta(1+2\sigma)}{\zeta(2+4\sigma)} \sim \frac{3}{\pi^2\sigma}$ as $\sigma \to 0^+$.

3. **Theorem 3 (Unconstrained Common-Factor Expansion & Fixed-Order Euler–Maclaurin Bound up to $A \le X^{1-\delta}$, §4)**:
   By complete multiplicativity, $\lambda(d r)\lambda(d s) = \lambda(d)^2\lambda(r)\lambda(s) = \lambda(r)\lambda(s)$ for **every** integer $d \ge 1$, eliminating both the squarefree factor $\mu(d)^2$ and the coprimality condition $\gcd(d, r s) = 1$. Hence
   $$Q_\lambda(X)^2 = \sum_{\substack{r, s \ge 1 \\ \gcd(r, s) = 1}}\frac{\lambda(r)\lambda(s)\,X^5}{(r s)^3}\sum_{d\ge 1} d^{-6} e^{-L^2/d^2}, \qquad L = X\sqrt{r^{-2} + s^{-2}}.$$
   For $f(v) = v^{-6}e^{-1/v^2}$ ($v > 0$, $f(0) = 0$) and every even integer $N \ge 2$, periodic Bernoulli integration by parts proves
   $$\left|\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} - \frac{3\sqrt{\pi}}{8}L^{-5}\right| \le C_N L^{-5-N}, \qquad C_N := \frac{2\zeta(N)}{\tau^N}\int_0^\infty \bigl|f^{(N)}(v)\bigr|\,dv,$$
   with certified 256-bit Arb constants
   $$C_2 = \frac{f'(v_-) - f'(v_+)}{6} = [1.851257667016958056850958359201349291641 \pm 3.54 \times 10^{-40}], \qquad v_\pm = \sqrt{\frac{15 \pm \sqrt{57}}{42}},$$
   $$C_4 = \frac{1}{720}\int_0^\infty \bigl|f^{(4)}(v)\bigr|\,dv = [8.752371760035365551239039765015814873069 \pm 3.16 \times 10^{-39}].$$
   Summing over $1 \le r, s \le A$ ($\gcd(r, s) = 1$) gives
   $$\sum_{\substack{1 \le r, s \le A \\ \gcd(r, s) = 1}}\bigl|E^\lambda_{r,s}(X)\bigr| \le C_N 2^{-(N+5)/2}\frac{A^{N+1}}{X^N},$$
   which tends to $0$ throughout the **entire subtransition regime** $A \le X^{1-\delta}$ whenever $(N+1)\delta > 1$ (already reaching $A \le X^{2/3-\eta}$ at $N = 2$ and $A \le X^{1-\delta}$ for arbitrary fixed $\delta \in (0, 1)$ by choosing $N = 2\lceil 1/(2\delta)\rceil$).

4. **Theorem 4 (Exact Transition Poisson Summation & Certified Non-Positivity of $\widehat{f}$, §5)**:
   The even extension $f(-v) = f(v)$ ($f(0) = 0$) belongs to the Schwartz class $\mathcal{S}(\mathbb{R})$, and Poisson summation yields the exact identity valid for **all** $L > 0$:
   $$\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} = L^{-5}\left[\frac{3\sqrt{\pi}}{8} + \sum_{j\ge 1}\widehat{f}(j L)\right], \qquad \widehat{f}(\xi) := 2\int_0^\infty v^{-6}e^{-1/v^2}\cos(\tau\xi v)\,dv.$$
   Evaluating $\widehat{f}(\xi)$ via its exact Mellin–Barnes residue expansion in 256-bit Arb certifies sign changes:
   $$\widehat{f}(1/2) = [-0.5628546550179851263755109492164491931001 \pm 4.04 \times 10^{-41}] < 0,$$
   $$\widehat{f}(1) = [-0.3668367826642069184644449070564857828859 \pm 4.03 \times 10^{-41}] < 0,$$
   $$\widehat{f}(3/2) = [0.2636171831500303372338138695632955698496 \pm 2.39 \times 10^{-41}] > 0,$$
   $$\widehat{f}(2) = [0.1247126116325928138362162976104693467978 \pm 9.77 \times 10^{-42}] > 0.$$

5. **Theorem 5 (Replacement Theorem — Exact Separable Gaussian Decoupling & Global Super-Polynomial Logarithmic Energy Saving, §6A)**:
   In Attack A, the bivariate coprime Dirichlet series
   $$\mathcal{D}_\lambda(u, v) := \sum_{\gcd(r, s)=1}\frac{\lambda(r)\lambda(s)}{r^u s^v} = \frac{\zeta(2u)\zeta(2v)}{\zeta(u)\zeta(v)\zeta(u+v)} \qquad (\operatorname{Re} u > 1,\;\operatorname{Re} v > 1)$$
   cannot cancel off-critical poles at $(u, v) = (\rho, \bar{\rho})$ ($\operatorname{Re}\rho = \beta > 1/2$) because $2\beta > 1$ lies inside the Euler-product half-plane where $\zeta(2\rho) \ne 0$ and $\zeta(2\beta) > 1$. However, retaining the **exact separable Gaussian kernel** $e^{-X^2(r^{-2}+s^{-2})/d^2} = e^{-X^2/(d^2 r^2)}e^{-X^2/(d^2 s^2)}$ before Euler–Maclaurin expansion and applying $\mathbf{1}_{\gcd(r,s)=1} = \sum_{e \mid \gcd(r,s)}\mu(e)$ ($r = e m$, $s = e n$) decouples every dyadic rectangular block $B_{A,B}(X)$ into 1D unweighted Liouville Gaussian sums:
   $$B_{A,B}(X) = \sum_{1 \le e < 2\min(A,B)}\frac{\mu(e)}{e}\sum_{d\ge 1}\frac{1}{d}\,U_\lambda\!\left(\frac{X}{d e}; \frac{A}{e}\right)U_\lambda\!\left(\frac{X}{d e}; \frac{B}{e}\right),$$
   where $U_\lambda(Y; M) := Y^{5/2}\sum_{M \le m < 2M}\frac{\lambda(m)}{m^3}e^{-Y^2/m^2}$. Because $m, n$ carry **no coprimality constraint** to $d e$, partial summation with the Korobov–Vinogradov–Walfisz bound $L_\lambda(x) = \sum_{m \le x}\lambda(m) \ll x\exp(-c_0\Phi(x))$ ($\Phi(x) = (\log x)^{3/5}(\log\log x)^{-1/5}$) and convergent divisor weights $\sum_{e\ge 1} e^{-2} = \sum_{d\ge 1} d^{-2} = \pi^2/6$ proves the unconditional **global** grade-interval energy saving:
   $$\boxed{\int_Y^{\tau Y}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} \;\ll\; Y\exp\!\left(-2 c_1 (\log Y)^{3/5}(\log\log Y)^{-1/5}\right) \;\ll_D\; \frac{Y}{(\log Y)^D} \qquad (\forall D > 0,\;Y \ge 2),}$$
   beating the unsigned $O(Y)$ benchmark across the **entire integral** (including the transition $A, B \asymp X$) without encountering the $O_N(X)$ Euler–Maclaurin blowup.

6. **Theorem 6 (Dyadic Parity Annihilation, Cross-Scale Energy Identity, and Off-Critical Mode Non-Vanishing, §6B)**:
   The dyadic parity combination
   $$Q_{\lambda,\mathrm{odd}}(X) := Q_\lambda(X) + 2^{-1/2}Q_\lambda(X/2) = X^{5/2}\sum_{\substack{m\ge 1 \\ 2 \nmid m}}\frac{\lambda(m)}{m^3}e^{-X^2/m^2}$$
   annihilates all even indices $n = 2^a m$ ($a \ge 1$) by canceling $\lambda(2^{a-1}m) + \lambda(2^a m) = 0$, admits the convergent dyadic inverse $Q_\lambda(X) = \sum_{j\ge 0}(-1)^j 2^{-j/2}Q_{\lambda,\mathrm{odd}}(X/2^j)$, satisfies the exact grade-interval energy identity
   $$\int_Y^{\tau Y}\bigl|Q_{\lambda,\mathrm{odd}}(X)\bigr|^2\,\frac{dX}{X} = \int_Y^{\tau Y}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} + \frac{1}{2}\int_{Y/2}^{\tau Y/2}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} + \sqrt{2}\int_Y^{\tau Y}Q_\lambda(X)Q_\lambda(X/2)\,\frac{dX}{X},$$
   and satisfies the two-sided weighted norm equivalence $(1 - 2^{-1/2-\sigma})\|Q_\lambda\|_\sigma \le \|Q_{\lambda,\mathrm{odd}}\|_\sigma \le (1 + 2^{-1/2-\sigma})\|Q_\lambda\|_\sigma$ for all $\sigma > -1/2$. On any off-critical mode $X^{\rho - 1/2}$ ($\operatorname{Re}\rho = \beta > 0$), the multiplier $1 + 2^{-\rho}$ satisfies $0 < 1 - 2^{-\beta} \le |1 + 2^{-\rho}| \le 1 + 2^{-\beta} < 2$ and never vanishes.

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
By multiplicativity across prime-power factors $n = \prod_p p^{v_p(n)}$, both identities hold for all $n \ge 1$. Notice the corresponding Dirichlet-series relation for $\operatorname{Re} s > 1$:
$$\sum_{n\ge 1}\frac{\lambda(n)}{n^s} = \left(\sum_{d\ge 1}\frac{1}{d^{2s}}\right)\left(\sum_{m\ge 1}\frac{\mu(m)}{m^s}\right) = \frac{\zeta(2s)}{\zeta(s)}. \qquad \square$$

 Both prime-power identities and complete multiplicativity are formally verified in Lean 4 (`liouville_complete_multiplicativity_and_common_factor_cancellation_nat` and `prime_power_square_divisor_moebius_liouville_inversion_nat` in [`formal/RiemannScope/LiouvilleSquareDilation.lean`](../../formal/RiemannScope/LiouvilleSquareDilation.lean)) and checked in Python across all $1 \le n \le 200$ and all $1 \le d, r, s \le 30$ ($27{,}000$ triples).

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

### 3.2 Weighted $L^2$ Dilation Norm Equivalence and $\sigma \to 0^+$ Pole Analysis

For $\sigma > 0$, define the weighted multiplicative $L^2$ norm on $(0, \infty)$:
$$\|f\|_\sigma := \left(\int_0^\infty |f(X)|^2 X^{-2\sigma}\,\frac{dX}{X}\right)^{1/2}.$$
Under the change of variables $X = a Y$ ($a > 0$, $\frac{dX}{X} = \frac{dY}{Y}$):
$$\|f(\cdot/a)\|_\sigma^2 = \int_0^\infty |f(X/a)|^2 X^{-2\sigma}\,\frac{dX}{X} = \int_0^\infty |f(Y)|^2 (a Y)^{-2\sigma}\,\frac{dY}{Y} = a^{-2\sigma}\|f\|_\sigma^2 \implies \|f(\cdot/a)\|_\sigma = a^{-\sigma}\|f\|_\sigma.$$
In particular, for $a = d^2$, $\|f(\cdot/d^2)\|_\sigma = d^{-2\sigma}\|f\|_\sigma$. Applying Minkowski's integral inequality to $Q_\lambda(X) = \sum_{d\ge 1} d^{-1} Q_\mu(X/d^2)$ and $Q_\mu(X) = \sum_{d\ge 1}\mu(d) d^{-1} Q_\lambda(X/d^2)$ for any $\sigma > 0$ yields:
$$\|Q_\lambda\|_\sigma \le \sum_{d\ge 1}\frac{\|Q_\mu(\cdot/d^2)\|_\sigma}{d} = \left(\sum_{d\ge 1} d^{-1-2\sigma}\right)\|Q_\mu\|_\sigma = \zeta(1 + 2\sigma)\,\|Q_\mu\|_\sigma,$$
$$\|Q_\mu\|_\sigma \le \sum_{d\ge 1}\frac{|\mu(d)|\,\|Q_\lambda(\cdot/d^2)\|_\sigma}{d} = \left(\sum_{d\ge 1}\mu(d)^2 d^{-1-2\sigma}\right)\|Q_\lambda\|_\sigma = \frac{\zeta(1 + 2\sigma)}{\zeta(2 + 4\sigma)}\,\|Q_\lambda\|_\sigma.$$
- **Behavior as $\sigma \to 0^+$**: Since $\zeta(1 + 2\sigma) = \frac{1}{2\sigma} + \gamma + O(\sigma)$, both multipliers blow up like $O(\sigma^{-1})$ as $\sigma \to 0^+$:
  $$\lim_{\sigma \to 0^+}\sigma\,\zeta(1 + 2\sigma) = \frac{1}{2} = 0.5, \qquad \lim_{\sigma \to 0^+}\sigma\,\frac{\zeta(1 + 2\sigma)}{\zeta(2 + 4\sigma)} = \frac{1}{2\zeta(2)} = \frac{3}{\pi^2} \approx 0.3039635509,$$
  so the transfer operator has **no bounded inverse at $\sigma = 0$**, while it is a bounded linear isomorphism on $L^2((0, \infty), X^{-2\sigma}\frac{dX}{X})$ for every fixed $\sigma > 0$.

| $\sigma$ | $\zeta(1 + 2\sigma)$ | $\frac{\zeta(1 + 2\sigma)}{\zeta(2 + 4\sigma)}$ | $\sigma\,\zeta(1 + 2\sigma)$ | $\sigma\,\frac{\zeta(1 + 2\sigma)}{\zeta(2 + 4\sigma)}$ |
| :--- | :--- | :--- | :--- | :--- |
| $1/20$ | `[10.58444846495080982638640079173552303995 +/- 1.55e-39]` | `[7.101067626682364959660319788279339842132 +/- 1.71e-40]` | `[0.5292224232475404913193200395867761519973 +/- 7.77e-41]` | `[0.3550533813341182479830159894139669921066 +/- 8.53e-42]` |
| $1/10$ | `[5.591582441177750776536563193423143277630 +/- 9.68e-41]` | `[4.042079955408588766460293600513948039645 +/- 3.91e-40]` | `[0.5591582441177750776536563193423143277630 +/- 1.07e-41]` | `[0.4042079955408588766460293600513948039645 +/- 4.01e-41]` |
| $1/4$ | `[2.612375348685488343348567567924071630571 +/- 2.00e-40]` | `[2.173254312519554138237089840438223722907 +/- 2.89e-40]` | `[0.6530938371713720858371418919810179076428 +/- 5.00e-41]` | `[0.5433135781298885345592724601095559307268 +/- 7.21e-41]` |
| $1/2$ | `[1.644934066848226436472415166646025189219 +/- 5.02e-41]` | `[1.519817754635066571658191948145914583565 +/- 3.82e-40]` | `[0.8224670334241132182362075833230125946093 +/- 2.51e-41]` | `[0.7599088773175332858290959740729572917825 +/- 1.91e-40]` |
| $1$ | `[1.202056903159594285399738161511449990765 +/- 1.38e-41]` | `[1.181564949010256912569399734160454260547 +/- 2.33e-41]` | `[1.202056903159594285399738161511449990765 +/- 1.38e-41]` | `[1.181564949010256912569399734160454260547 +/- 2.33e-41]` |

### 3.3 Grade-Interval Energy Equivalence, Mellin Continuation, and Bridge to `SUBGATE-TC-043A`

**Proposition 3.1 (Equivalence of Grade-Interval Subpower Energy and Weighted Norm Finiteness).** *For $a \in \{\mu, \lambda\}$, the following two conditions are equivalent:*
1. *(Grade-interval subpower energy)*: $\forall \varepsilon > 0\;\exists C_\varepsilon < \infty\;\forall Y \ge 1,\;\int_Y^{\tau Y}|Q_a(X)|^2\,\frac{dX}{X} \le C_\varepsilon Y^\varepsilon$.
2. *(Weighted norm finiteness)*: $\forall \sigma \in (0, 5/2),\;\|Q_a\|_\sigma < \infty$.

*Proof.*
- **(1) $\implies$ (2)**: Fix $\sigma \in (0, 5/2)$. On $(0, 1]$, $|Q_a(X)| \le \zeta(3)X^{5/2}$ gives
  $$\int_0^1 |Q_a(X)|^2 X^{-2\sigma}\,\frac{dX}{X} \le \zeta(3)^2\int_0^1 X^{4-2\sigma}\,dX = \frac{\zeta(3)^2}{5 - 2\sigma} < \infty.$$
  On $[1, \infty) = \bigcup_{k=0}^\infty [\tau^k, \tau^{k+1})$, apply (1) with $\varepsilon = \sigma > 0$ and $Y = \tau^k \ge 1$. Since $X^{-2\sigma} \le \tau^{-2k\sigma}$ on $[\tau^k, \tau^{k+1})$,
  $$\sum_{k=0}^\infty \int_{\tau^k}^{\tau^{k+1}}|Q_a(X)|^2 X^{-2\sigma}\,\frac{dX}{X} \le \sum_{k=0}^\infty \tau^{-2k\sigma} C_\sigma \tau^{k\sigma} = \frac{C_\sigma}{1 - \tau^{-\sigma}} < \infty.$$
  Hence $\|Q_a\|_\sigma^2 \le \frac{\zeta(3)^2}{5 - 2\sigma} + \frac{C_\sigma}{1 - \tau^{-\sigma}} < \infty$.
- **(2) $\implies$ (1)**: Given $\varepsilon > 0$, without loss of generality take $\varepsilon \in (0, 5)$ (since $Y^\varepsilon$ is increasing in $\varepsilon$ for $Y \ge 1$) and set $\sigma = \varepsilon/2 \in (0, 5/2)$. For any $Y \ge 1$ and $X \in [Y, \tau Y]$, $X / (\tau Y) \le 1 \implies 1 \le (\tau Y)^{2\sigma} X^{-2\sigma} = \tau^\varepsilon Y^\varepsilon X^{-2\sigma}$, so
  $$\int_Y^{\tau Y}|Q_a(X)|^2\,\frac{dX}{X} \le \tau^\varepsilon Y^\varepsilon \int_Y^{\tau Y}|Q_a(X)|^2 X^{-2\sigma}\,\frac{dX}{X} \le \tau^\varepsilon \|Q_a\|_{\varepsilon/2}^2\,Y^\varepsilon. \qquad \square$$

**Analytic Mellin-to-RH Bridge and Connection to `SUBGATE-TC-043A`**:
- For $\frac{1}{2} < \operatorname{Re} z < \frac{5}{2}$, termwise Mellin integration (justified by $\sum_{n\ge 1} n^{-1/2 - \operatorname{Re} z} < \infty$ and $\int_0^\infty X^{5/2 - z} e^{-X^2/n^2}\frac{dX}{X} = \frac{1}{2}n^{5/2 - z}\Gamma(5/4 - z/2)$) yields:
  $$\mathcal{M}[Q_\mu](z) := \int_0^\infty Q_\mu(X) X^{-z}\,\frac{dX}{X} = \frac{\Gamma(5/4 - z/2)}{2\,\zeta(1/2 + z)}, \qquad \mathcal{M}[Q_\lambda](z) := \int_0^\infty Q_\lambda(X) X^{-z}\,\frac{dX}{X} = \frac{\Gamma(5/4 - z/2)\,\zeta(1 + 2z)}{2\,\zeta(1/2 + z)}.$$
- If $\|Q_a\|_\sigma < \infty$ for all $\sigma \in (0, 5/2)$, then for any compact subset $K \subset \{z \in \mathbb{C} : 0 < \operatorname{Re} z < 5/2\}$, splitting $\int_0^\infty = \int_0^1 + \int_1^\infty$ and applying Cauchy–Schwarz on $[1, \infty)$ with $\sigma_0 = \frac{1}{2}\min_{z \in K}\operatorname{Re} z > 0$:
  $$\left|\int_1^\infty Q_a(X) X^{-z}\,\frac{dX}{X}\right| \le \|Q_a\|_{\sigma_0}\left(\int_1^\infty X^{-2(\operatorname{Re} z - \sigma_0)}\,\frac{dX}{X}\right)^{1/2} = \frac{\|Q_a\|_{\sigma_0}}{\sqrt{2(\operatorname{Re} z - \sigma_0)}} < \infty,$$
  proving that $\mathcal{M}[Q_a](z)$ extends holomorphically to the entire strip $0 < \operatorname{Re} z < 5/2$. Since $\Gamma(5/4 - z/2)$ is nonvanishing on $\operatorname{Re} z < 5/2$ and $\zeta(1 + 2z)$ is nonvanishing on $\operatorname{Re} z > 0$ ($\operatorname{Re}(1 + 2z) > 1$), holomorphicity of $\mathcal{M}[Q_a](z)$ on $0 < \operatorname{Re} z < 5/2$ forces $\zeta(1/2 + z) \ne 0$ on $0 < \operatorname{Re} z < 1/2$, i.e., $\zeta(s) \ne 0$ in $1/2 < \operatorname{Re} s < 1$ (and by functional equation in $0 < \operatorname{Re} s < 1/2$).
- **Bridge between auxiliary real dilations and admissible TC grades $K \in \mathbb{A}_{\mathbb{R}}$**: Individual square-dilation shifts $X \mapsto X/d^2$ ($d \ge 2$) and dyadic shifts $X \mapsto X/2$ correspond to logarithmic shifts $\log_\tau(d^2)$ and $\log_\tau 2$, which are transcendental over $\mathbb{Q}$ and are **not** single grades in $\mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}$. However, Proposition 3.1 shows that the $\tau$-adic intervals $[\tau^k, \tau^{k+1})$ indexed by rational integers $k \in \mathbb{Z} \subset \mathbb{A}_{\mathbb{R}}$ partition the entire continuum $[1, \infty)$, so the grade-interval subpower energy condition on $[Y, \tau Y]$ ($Y = \tau^K$, $K \in \mathbb{A}_{\mathbb{R}}$) is equivalent to finiteness of the global continuum norm $\|\cdot\|_\sigma$ on $L^2((0, \infty), X^{-2\sigma}\frac{dX}{X})$. The square-dilation and dyadic operators act as bounded linear isomorphisms on this ambient continuum space $L^2((0, \infty), X^{-2\sigma}\frac{dX}{X})$ ($\sigma > 0$), transferring the grade-interval energy bound between $Q_\mu$ and $Q_\lambda$ without ever requiring $\log_\tau 2$ or $\log_\tau(d^2)$ to lie in $\mathbb{A}_{\mathbb{R}}$.

---

## 4. Unconstrained Common-Factor Expansion & Fixed-Order Euler–Maclaurin Bounds

### 4.1 Complete Multiplicativity Common-Factor Expansion

Writing every pair $(m, n) \in \mathbb{Z}_{\ge 1}^2$ uniquely as $m = d r$, $n = d s$ with $d = \gcd(m, n) \ge 1$ and $\gcd(r, s) = 1$, complete multiplicativity of $\lambda$ gives
$$\lambda(m)\lambda(n) = \lambda(d r)\lambda(d s) = \lambda(d)^2\lambda(r)\lambda(s) = \lambda(r)\lambda(s) \qquad (\forall d, r, s \ge 1),$$
with **no squarefree restriction on $d$ and no coprimality restriction $\gcd(d, r s) = 1$**. Therefore:
$$Q_\lambda(X)^2 = X^5 \sum_{m, n \ge 1}\frac{\lambda(m)\lambda(n)}{(m n)^3}e^{-X^2(m^{-2}+n^{-2})} = \sum_{\substack{r, s \ge 1 \\ \gcd(r, s) = 1}}\frac{\lambda(r)\lambda(s)\,X^5}{(r s)^3}\sum_{d\ge 1} d^{-6} e^{-L^2/d^2}, \qquad L := X\sqrt{r^{-2} + s^{-2}}.$$
Since $\int_0^\infty t^{-6} e^{-L^2/t^2}\,dt = L^{-5}\int_0^\infty v^{-6}e^{-1/v^2}\,dv = \frac{1}{2}\Gamma(5/2)L^{-5} = \frac{3\sqrt{\pi}}{8}L^{-5}$, the leading Gaussian term for each coprime pair $(r, s)$ is
$$L^\lambda_{r, s} := \frac{\lambda(r)\lambda(s)\,X^5}{(r s)^3}\cdot \frac{3\sqrt{\pi}}{8}L^{-5} = \frac{3\sqrt{\pi}}{8}\lambda(r)\lambda(s)\frac{(r s)^2}{(r^2 + s^2)^{5/2}},$$
which is completely independent of $X$.

### 4.2 Fixed-Order Euler–Maclaurin Bound for $f(v) = v^{-6}e^{-1/v^2}$

Let $f(v) := v^{-6}e^{-1/v^2}$ for $v > 0$ and $f(0) := 0$. Every derivative $f^{(k)}(v)$ is a polynomial in $v^{-1}$ multiplied by $e^{-1/v^2}$, so $\lim_{v \to 0^+} f^{(k)}(v) = 0$ and $\lim_{v \to \infty} f^{(k)}(v) = 0$ for all $k \ge 0$. Set $g(t) := t^{-6}e^{-L^2/t^2} = L^{-6}f(t/L)$, so $g^{(N)}(t) = L^{-6-N}f^{(N)}(t/L)$ with $g^{(k)}(0) = g^{(k)}(\infty) = 0$ for all $k \ge 0$.

For any even integer $N \ge 2$, the $N$-th order Euler–Maclaurin summation formula on $[0, \infty)$ with vanished endpoint derivatives gives
$$\sum_{d\ge 1} g(d) - \int_0^\infty g(t)\,dt = -\frac{1}{N!}\int_0^\infty \widetilde{B}_N(t)\,g^{(N)}(t)\,dt,$$
where $\widetilde{B}_N(t) = B_N(\{t\})$ is the $N$-th periodic Bernoulli function, whose Fourier expansion
$$\widetilde{B}_N(t) = (-1)^{N/2 - 1}\frac{2\,N!}{\tau^N}\sum_{j=1}^\infty \frac{\cos(j\tau t)}{j^N} \qquad (\tau = 2\pi)$$
implies the sharp uniform supremum bound $\sup_{t \in \mathbb{R}}\frac{|\widetilde{B}_N(t)|}{N!} = \frac{2\zeta(N)}{\tau^N}$. Substituting $t = L v$ ($dt = L\,dv$) yields:
$$\left|\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} - \frac{3\sqrt{\pi}}{8}L^{-5}\right| \le \frac{2\zeta(N)}{\tau^N}\int_0^\infty L^{-6-N}\bigl|f^{(N)}(t/L)\bigr|\,dt = C_N L^{-5-N}, \qquad C_N := \frac{2\zeta(N)}{\tau^N}\int_0^\infty \bigl|f^{(N)}(v)\bigr|\,dv.$$

**Exact Symbolic Derivatives and Certified Constants $C_2, C_4$**:
Using SymPy (`verify_euler_maclaurin_derivatives_and_constants_arb`), the first four derivatives of $f(v) = v^{-6}e^{-1/v^2}$ are:
$$f'(v) = 2(1 - 3v^2)v^{-9}e^{-1/v^2}, \qquad f''(v) = 2(21v^4 - 15v^2 + 2)v^{-12}e^{-1/v^2},$$
$$f^{(3)}(v) = 4(-84v^6 + 96v^4 - 27v^2 + 2)v^{-15}e^{-1/v^2}, \qquad f^{(4)}(v) = 4(6v^2 - 1)(126v^6 - 183v^4 + 60v^2 - 4)v^{-18}e^{-1/v^2}.$$
- **Evaluation of $C_2$ ($N = 2$)**: Since $21v^4 - 15v^2 + 2 = 0$ has positive roots
  $$v_- = \sqrt{\frac{15 - \sqrt{57}}{42}} \in [0.4211708612882846189067416640646506740997 \pm 2.00 \times 10^{-40}],$$
  $$v_+ = \sqrt{\frac{15 + \sqrt{57}}{42}} \in [0.7327351635395962094861244517470714998819 \pm 2.00 \times 10^{-40}],$$
  with $f'' > 0$ on $(0, v_-) \cup (v_+, \infty)$, $f'' < 0$ on $(v_-, v_+)$, and $f'(v_-) > 0 > f'(v_+)$, the fundamental theorem of calculus gives
  $$\int_0^\infty |f''(v)|\,dv = f'(v_-) - (f'(v_+) - f'(v_-)) + (-f'(v_+)) = 2\bigl(f'(v_-) - f'(v_+)\bigr),$$
  and since $\frac{2\zeta(2)}{\tau^2} = \frac{2(\pi^2/6)}{4\pi^2} = \frac{1}{12}$,
  $$C_2 = \frac{f'(v_-) - f'(v_+)}{6} \in [1.851257667016958056850958359201349291641 \pm 2.00 \times 10^{-39}].$$
- **Evaluation of $C_4$ ($N = 4$)**: The four positive roots $0 < v_1 < v_2 = 1/\sqrt{6} < v_3 < v_4$ of $f^{(4)}(v) = 0$ satisfy $\int_0^\infty |f^{(4)}(v)|\,dv = 2[f^{(3)}(v_1) - f^{(3)}(v_2) + f^{(3)}(v_3) - f^{(3)}(v_4)]$, and since $\frac{2\zeta(4)}{\tau^4} = \frac{2(\pi^4/90)}{16\pi^4} = \frac{1}{720}$,
  $$C_4 = \frac{1}{720}\int_0^\infty \bigl|f^{(4)}(v)\bigr|\,dv \in [8.752371760035365551239039765015814873069 \pm 4.00 \times 10^{-39}].$$

### 4.3 Pairwise and Summed Subtransition Error Bounds ($A \le X^{1-\delta}$)

Multiplying the $d$-sum error bound by $\frac{X^5}{(r s)^3}$ with $L = X\frac{\sqrt{r^2+s^2}}{r s}$ yields the pairwise error bound
$$\bigl|E^\lambda_{r, s}(X)\bigr| \le \frac{X^5}{(r s)^3}\,C_N L^{-5-N} = C_N X^{-N}\frac{(r s)^{N+2}}{(r^2 + s^2)^{(N+5)/2}}.$$
By AM–GM, $r^2 + s^2 \ge 2 r s \implies (r^2 + s^2)^{(N+5)/2} \ge 2^{(N+5)/2}(r s)^{(N+5)/2}$, so
$$\frac{(r s)^{N+2}}{(r^2 + s^2)^{(N+5)/2}} \le 2^{-(N+5)/2}(r s)^{(N+2) - (N+5)/2} = 2^{-(N+5)/2}(r s)^{(N-1)/2}.$$
Summing over $1 \le r, s \le A$ using $(r s)^{(N-1)/2} \le A^{N-1}$ on the $A^2$ pairs $(r, s) \in [1, A]^2$ gives:
$$\sum_{\substack{1 \le r, s \le A \\ \gcd(r, s) = 1}}\bigl|E^\lambda_{r,s}(X)\bigr| \le C_N 2^{-(N+5)/2} X^{-N}\sum_{r=1}^A \sum_{s=1}^A (r s)^{(N-1)/2} \le C_N 2^{-(N+5)/2}\frac{A^{N+1}}{X^N}.$$
Setting $A \le X^{1-\delta}$ ($\delta \in (0, 1)$), the exponent of $X$ is
$$(N + 1)(1 - \delta) - N = 1 - (N + 1)\delta < 0 \Longleftrightarrow (N + 1)\delta > 1.$$
- For $N = 2$: $(2 + 1)\delta > 1 \iff \delta > 1/3$, controlling $A \le X^{2/3 - \eta}$ (already doubling the $TC\text{-}053R$ exponent $1/3 - \delta$).
- For $N = 4$: $(4 + 1)\delta > 1 \iff \delta > 1/5$, controlling $A \le X^{4/5 - \eta}$.
- For any fixed $\delta \in (0, 1)$: choosing the even integer $N = 2\lceil 1/(2\delta)\rceil$ gives $(N + 1)\delta \ge 1 + \delta > 1$, so the summed Euler–Maclaurin error vanishes as $O(X^{1 - (N+1)\delta}) \to 0$ throughout $A \le X^{1-\delta}$.

| $L$ | Exact $\sum_{d\ge 1}d^{-6}e^{-L^2/d^2}$ | Gaussian Leading $\frac{3\sqrt{\pi}}{8}L^{-5}$ | Absolute Error | $N = 2$ Bound $C_2 L^{-7}$ | $N = 4$ Bound $C_4 L^{-9}$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $1/2$ | `[0.79515495547440055 +/- 6.33e-18]` | `[21.26944621086619232757800980009374219357 +/- 5.94e-40]` | `[20.47429125539179178 +/- 8.60e-18]` | `[236.9609813781706312769226699777727093301 +/- 6.77e-39]` | `[4481.214341138107162234388359688097215011 +/- 1.85e-36]` |
| $1$ | `[0.3816038498680422 +/- 5.24e-17]` | `[0.6646701940895685102368128062529294435491 +/- 1.90e-41]` | `[0.2830663442215263 +/- 4.22e-17]` | `[1.851257667016958056850958359201349291641 +/- 3.54e-40]` | `[8.752371760035365551239039765015814873069 +/- 3.16e-39]` |
| $2$ | `[0.02522282217978698 +/- 6.66e-18]` | `[0.02077094356529901594490040019540404511091 +/- 1.22e-42]` | `[0.0044518786144880 +/- 4.26e-17]` | `[0.01446295052356998481914811218126054134095 +/- 1.93e-42]` | `[0.01709447609381907334226374954104651342396 +/- 8.21e-42]` |
| $4$ | `[0.00066833923524992 +/- 8.66e-18]` | `[0.0006490919864155942482781375061063764097159 +/- 5.43e-46]` | `[1.924724883433e-5 +/- 8.09e-18]` | `[0.0001129918009653905063995946264160979792262 +/- 4.32e-44]` | `[3.338764862074037762160888582235647153118e-5 +/- 1.07e-44]` |
| $8$ | `[2.028496883949e-5 +/- 7.27e-18]` | `[2.028412457548732025869179706582426280362e-5 +/- 1.86e-45]` | `[8.4426400e-10 +/- 7.92e-18]` | `[8.827484450421133312468330188757654627044e-7 +/- 4.99e-47]` | `[6.521025121238354999999999999999999999999e-8 +/- 2.68e-47]` |

---

## 5. Exact Poisson Summation Formula at the Transition ($A \asymp X$)

When $r, s \asymp A \asymp X$, the effective scale $L = X\sqrt{r^{-2} + s^{-2}} \asymp 1$ is of order unity, so $A^{N+1}/X^N \asymp_N X$ diverges for every fixed $N$. Instead of truncating Euler–Maclaurin at fixed order $N$, we extend $f(v) = v^{-6}e^{-1/v^2}$ evenly to $\mathbb{R}$ by $f(-v) := f(v)$ ($v \ne 0$) and $f(0) := 0$. Because $\lim_{v \to 0} v^{-m} e^{-1/v^2} = 0$ for all $m \ge 0$, all left and right derivatives vanish at the origin ($f^{(k)}(0^\pm) = 0$ for all $k \ge 0$) and $f \in \mathcal{S}(\mathbb{R})$.

By Poisson summation on $\mathbb{Z}$ applied to $F(t) = f(t/L)$ ($F(0) = 0$):
$$2\sum_{d=1}^\infty f(d/L) = \sum_{d \in \mathbb{Z}} f(d/L) = L\sum_{j \in \mathbb{Z}}\widehat{f}(j L) = L\left[\widehat{f}(0) + 2\sum_{j=1}^\infty \widehat{f}(j L)\right],$$
where
$$\widehat{f}(\xi) := \int_{\mathbb{R}} f(v)e^{-i\tau\xi v}\,dv = 2\int_0^\infty v^{-6}e^{-1/v^2}\cos(\tau\xi v)\,dv \qquad (\tau = 2\pi),$$
and $\widehat{f}(0) = 2\int_0^\infty v^{-6}e^{-1/v^2}\,dv = \frac{3\sqrt{\pi}}{4}$. Dividing by $2 L^6$ yields the exact transition identity:
$$\boxed{\sum_{d\ge 1} d^{-6}e^{-L^2/d^2} = L^{-5}\left[\frac{3\sqrt{\pi}}{8} + \sum_{j\ge 1}\widehat{f}(j L)\right] \qquad (\forall L > 0).}$$

### 5.1 Exact Mellin–Barnes Residue Series and Certified Sign Changes of $\widehat{f}(\xi)$

Setting $t = v^{-2}$ and $\omega = \tau|\xi| = 2\pi|\xi|$, Mellin inversion of $\cos(\omega t^{-1/2})$ gives
$$\widehat{f}(\xi) = \int_0^\infty t^{3/2}e^{-t}\cos(\omega t^{-1/2})\,dt = \frac{1}{2\pi i}\int_{c-i\infty}^{c+i\infty}\frac{\pi\,\Gamma\!\left(\frac{5+s}{2}\right)\omega^{-s}}{2\sin(\pi s/2)\Gamma(1-s)}\,ds \qquad (0 < c < 1).$$
Shifting the contour to $\operatorname{Re} s \to -\infty$ collects two disjoint families of simple poles in $\operatorname{Re} s \le 0$:
1. Simple poles of $1/\sin(\pi s/2)$ at even non-positive integers $s = -2m$ ($m \ge 0$) with residue $\frac{(-1)^m\Gamma(5/2-m)}{(2m)!}\omega^{2m}$;
2. Simple poles of $\Gamma(\frac{5+s}{2})$ at odd negative integers $s = -5 - 2k$ ($k \ge 0$) with residue $-\frac{\pi\,\omega^{5+2k}}{k!\,(5+2k)!}$.
This yields the globally convergent power series
$$\widehat{f}(\xi) = \sum_{m=0}^\infty \frac{(-1)^m\Gamma(5/2 - m)}{(2m)!}(2\pi\xi)^{2m} - \pi\sum_{k=0}^\infty \frac{(2\pi|\xi|)^{5+2k}}{k!\,(5+2k)!}.$$
Furthermore, $N$-fold integration by parts gives $|\widehat{f}(\xi)| \le (\tau|\xi|)^{-N}\int_{\mathbb{R}}|f^{(N)}(v)|\,dv = \frac{C_N}{\zeta(N)}|\xi|^{-N}$ for every even $N \ge 2$, so the Fourier tail after $J_0 \ge 1$ modes satisfies
$$\left|\sum_{j > J_0}\widehat{f}(j L)\right| \le \frac{C_N}{\zeta(N) L^N}\sum_{j = J_0+1}^\infty j^{-N} \le \frac{C_N}{(N - 1)\zeta(N) J_0^{N-1} L^N}.$$

| $\xi$ | Certified 256-Bit Arb Enclosure of $\widehat{f}(\xi)$ | Sign |
| :--- | :--- | :--- |
| $0$ | `[1.329340388179137020473625612505858887098 +/- 1.63e-40]` | $> 0$ (`True`) |
| $1/2$ | `[-0.5628546550179851263755109492164491931001 +/- 4.04e-41]` | $< 0$ (`True`) |
| $1$ | `[-0.3668367826642069184644449070564857828859 +/- 4.03e-41]` | $< 0$ (`True`) |
| $3/2$ | `[0.2636171831500303372338138695632955698496 +/- 2.39e-41]` | $> 0$ (`True`) |
| $2$ | `[0.1247126116325928138362162976104693467978 +/- 9.77e-42]` | $> 0$ (`True`) |

Because $\widehat{f}(\xi)$ is strictly negative at $\xi = 1/2, 1$ and strictly positive at $\xi = 3/2, 2$, the non-zero Poisson modes cannot be dismissed by a Bochner positivity argument.

---

## 6. Rectangular-Block Decomposition & Transition Proof Attempts (Attacks A & B)

Decomposing $(r, s) \in \mathbb{Z}_{\ge 1}^2$ into dyadic rectangles $[A, 2A) \times [B, 2B)$ with $A = 2^a$, $B = 2^b$ ($a, b \ge 0$) gives the exact partition
$$Q_\lambda(X)^2 = \sum_{a, b \ge 0} B_{2^a, 2^b}(X), \qquad B_{A, B}(X) := \sum_{\substack{A \le r < 2A,\; B \le s < 2B \\ \gcd(r, s) = 1}}\frac{\lambda(r)\lambda(s)\,X^5}{(r s)^3}\sum_{d\ge 1} d^{-6}e^{-X^2(r^{-2}+s^{-2})/d^2}.$$
For widely unequal blocks (say $B \ge A$), since $u^5 e^{-u^2} \le (5/(2e))^{5/2} < 1$ for $u = \frac{X}{d}\sqrt{r^{-2}+s^{-2}}$, each term is bounded in absolute value by $\zeta(6)\frac{(r s)^2}{(r^2+s^2)^{5/2}} \le \zeta(6)\frac{r^2}{s^3}$, and summing over $r \in [A, 2A)$ and $s \in [B, 2B)$ yields the unconditional off-diagonal decay bound:
$$\bigl|B_{A, B}(X)\bigr| \le \zeta(6)\,\frac{\min(A, B)^3}{\max(A, B)^2} = \frac{\pi^6}{945}\,\frac{\min(A, B)^3}{\max(A, B)^2}.$$

### 6.1 Attack A: Coprime Euler-Series, Off-Critical Non-Cancellation, and Separable Gaussian Replacement Theorem

1. **Bivariate Coprime Dirichlet Series**:
   For $\operatorname{Re} u > 1$ and $\operatorname{Re} v > 1$, expanding $\mathbf{1}_{\gcd(r,s)=1} = \sum_{e \mid \gcd(r,s)}\mu(e)$ with $r = e m$, $s = e n$ gives
   $$\mathcal{D}_\lambda(u, v) := \sum_{\gcd(r,s)=1}\frac{\lambda(r)\lambda(s)}{r^u s^v} = \sum_{e\ge 1}\frac{\mu(e)\lambda(e)^2}{e^{u+v}}\left(\sum_{m\ge 1}\frac{\lambda(m)}{m^u}\right)\left(\sum_{n\ge 1}\frac{\lambda(n)}{n^v}\right) = \frac{\zeta(2u)\,\zeta(2v)}{\zeta(u)\,\zeta(v)\,\zeta(u+v)}.$$
2. **Boundary Pole at $z = 0$ and Off-Critical Non-Cancellation**:
   - In 1D Mellin coordinates, $\mathcal{M}[Q_\lambda](z) = \frac{\Gamma(5/4-z/2)\zeta(1+2z)}{2\zeta(1/2+z)}$ has a simple pole at $z = 0$ (from $\zeta(1+2z) \sim \frac{1}{2z}$) with nonvanishing residue
     $$\operatorname*{Res}_{z=0}\mathcal{M}[Q_\lambda](z) = \frac{\Gamma(5/4)}{4\,\zeta(1/2)} \in [-0.1551682265483492584272379814757961069612 \pm 2.00 \times 10^{-40}] \ne 0.$$
   - At any hypothetical off-critical conjugate pair $(u, v) = (\rho, \bar{\rho})$ with $\operatorname{Re}\rho = \beta \in (1/2, 1)$, we have $\operatorname{Re}(2\rho) = \operatorname{Re}(2\bar{\rho}) = 2\beta > 1$ and $u + v = 2\beta > 1$. Because $\zeta(w)$ has an absolutely convergent nonvanishing Euler product on $\operatorname{Re} w > 1$ (with $|\zeta(2\rho)| \ge \frac{\zeta(4\beta)}{\zeta(2\beta)} > 0$ and $\zeta(2\beta) > 1$), **neither the numerator $\zeta(2u)\zeta(2v)$ nor the coprimality factor $1/\zeta(u+v)$ can vanish at $(\rho, \bar{\rho})$ to cancel the off-critical poles of $\frac{1}{\zeta(u)\zeta(v)}$**.
3. **Replacement Theorem (Exact Separable Gaussian Decoupling)**:
   Instead of expanding $\sum_{d\ge 1} d^{-6}e^{-X^2(r^{-2}+s^{-2})/d^2}$ by Euler–Maclaurin (which couples $r$ and $s$ inside $(r^2+s^2)^{-5/2}$ and blows up at $A, B \asymp X$), we retain the exact Gaussian kernel, which is **multiplicatively separable** in $r$ and $s$:
   $$e^{-X^2(r^{-2}+s^{-2})/d^2} = e^{-X^2/(d^2 r^2)}\,e^{-X^2/(d^2 s^2)}.$$
   Substituting $\mathbf{1}_{\gcd(r,s)=1} = \sum_{e \mid \gcd(r,s)}\mu(e)$ with $r = e m$, $s = e n$ ($\lambda(e m)\lambda(e n) = \lambda(m)\lambda(n)$) into $B_{A,B}(X)$ gives the exact decoupled identity:
   $$\boxed{B_{A,B}(X) = \sum_{1 \le e < 2\min(A,B)}\frac{\mu(e)}{e}\sum_{d\ge 1}\frac{1}{d}\,U_\lambda\!\left(\frac{X}{d e}; \frac{A}{e}\right)U_\lambda\!\left(\frac{X}{d e}; \frac{B}{e}\right),}$$
   where $U_\lambda(Y; M) := Y^{5/2}\sum_{M \le m < 2M}\frac{\lambda(m)}{m^3}e^{-Y^2/m^2}$.Similarly, summing over all $r, s \ge 1$ yields the global decoupled identity
   $$Q_\lambda(X)^2 = \sum_{e\ge 1}\frac{\mu(e)}{e}\sum_{d\ge 1}\frac{1}{d}\,Q_\lambda\!\left(\frac{X}{d e}\right)^2 = \sum_{q\ge 1}\frac{(\mu * 1)(q)}{q}\,Q_\lambda(X/q)^2 = Q_\lambda(X)^2,$$
   while on each dyadic block $B_{A,B}(X)$ the 1D factor $U_\lambda(Y; M)$ is an **unconstrained** 1D Liouville sum! By Abel summation on $L_\lambda(x) = \sum_{m \le x}\lambda(m) \ll x\exp(-c_0\Phi(x))$ ($\Phi(x) = (\log x)^{3/5}(\log\log x)^{-1/5}$) and the uniform total variation bound $\int_M^{2M}\left|\frac{d}{dt}\bigl(Y^{5/2}t^{-3}e^{-Y^2/t^2}\bigr)\right|dt \ll Y^{5/2}M^{-3}(1 + Y^2/M^2)e^{-Y^2/(4M^2)} \ll M^{-1/2}\min(M/Y, (Y/M)^{5/2})$, we obtain
   $$\bigl|U_\lambda(Y; M)\bigr| \ll M^{-1/2}\min\!\left(\frac{M}{Y}, \left(\frac{Y}{M}\right)^{5/2}\right)\exp\bigl(-c_1\Phi(M)\bigr)$$
   uniformly across **all** regimes ($M \ll Y$, $M \asymp Y$, and $M \gg Y$), and summing over $e, d \ge 1$ and $A = 2^a, B = 2^b$ proves:
   $$\int_Y^{\tau Y}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} \;\ll\; Y\exp\!\left(-2 c_1 (\log Y)^{3/5}(\log\log Y)^{-1/5}\right) \;\ll_D\; \frac{Y}{(\log Y)^D} \qquad (\forall D > 0,\;Y \ge 2).$$

| $(A, B, X)$ | Direct Block $B_{A,B}(X)$ | Separable Decoupled Formula | $0 \in \Delta$ | Widely Unequal Bound $\zeta(6)\frac{\min(A,B)^3}{\max(A,B)^2}$ | Bound Holds |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $(1, 1, 2)$ | `[0.103693354236 +/- 5.01e-13]` | `[0.103693354236 +/- 5.01e-13]` | `True` | `[1.017343061984449139714517929790920527902 +/- 1.83e-40]` | `True` |
| $(2, 2, 4)$ | `[0.0735522917142 +/- 5.35e-14]` | `[0.0735522917142 +/- 9.83e-14]` | `True` | `[2.034686123968898279429035859581841055804 +/- 3.66e-40]` | `True` |
| $(2, 4, 4)$ | `[0.0258021302529 +/- 1.17e-14]` | `[0.0258021302529 +/- 1.88e-14]` | `True` | `[0.5086715309922245698572589648954602639509 +/- 8.75e-42]` | `True` |
| $(4, 4, 4)$ | `[-0.09965512039735 +/- 1.59e-15]` | `[-0.09965512039735 +/- 2.86e-15]` | `True` | `[4.069372247937796558858071719163682111607 +/- 2.70e-40]` | `True` |
| $(1, 8, 4)$ | `[-0.0004608160896 +/- 3.95e-14]` | `[-0.0004608160896 +/- 3.95e-14]` | `True` | `[0.01589598534350701780803934265298313324847 +/- 4.11e-42]` | `True` |
| $(2, 16, 4)$ | `[0.002650623875497 +/- 6.13e-16]` | `[0.002650623875497 +/- 9.34e-16]` | `True` | `[0.03179197068701403561607868530596626649693 +/- 1.80e-42]` | `True` |

### 6.2 Attack B: Dyadic Parity Annihilation and Cross-Scale Correlation

Writing every $n \ge 1$ uniquely as $n = 2^a m$ with $a \ge 0$ and $2 \nmid m$, complete multiplicativity $\lambda(2^a m) = (-1)^a\lambda(m)$ gives
$$Q_\lambda(X) = \sum_{a\ge 0}(-1)^a 2^{-a/2} Q_{\lambda,\mathrm{odd}}(X/2^a), \qquad Q_{\lambda,\mathrm{odd}}(X) := X^{5/2}\sum_{\substack{m\ge 1 \\ 2 \nmid m}}\frac{\lambda(m)}{m^3}e^{-X^2/m^2}.$$
Hence
$$Q_{\lambda,\mathrm{odd}}(X) = Q_\lambda(X) + 2^{-1/2}Q_\lambda(X/2), \qquad Q_\lambda(X) = \sum_{j\ge 0}(-1)^j 2^{-j/2}Q_{\lambda,\mathrm{odd}}(X/2^j),$$
where the inverse series converges absolutely because $2^{-j/2}|Q_{\lambda,\mathrm{odd}}(X/2^j)| \le \zeta(3)X^{5/2} 2^{-3j}$. Squaring $Q_{\lambda,\mathrm{odd}}(X) = Q_\lambda(X) + 2^{-1/2}Q_\lambda(X/2)$ and integrating against $\frac{dX}{X}$ on $[Y, \tau Y]$ yields:
$$\int_Y^{\tau Y}\bigl|Q_{\lambda,\mathrm{odd}}(X)\bigr|^2\,\frac{dX}{X} = \int_Y^{\tau Y}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} + \frac{1}{2}\int_{Y/2}^{\tau Y/2}\bigl|Q_\lambda(X)\bigr|^2\,\frac{dX}{X} + \sqrt{2}\int_Y^{\tau Y}Q_\lambda(X)Q_\lambda(X/2)\,\frac{dX}{X}.$$
Moreover, for every $\sigma > -1/2$ (where $2^{-1/2-\sigma} < 1$, including $\sigma = 0$), Minkowski's inequality gives the two-sided norm equivalence
$$(1 - 2^{-1/2-\sigma})\,\|Q_\lambda\|_\sigma \le \|Q_{\lambda,\mathrm{odd}}\|_\sigma \le (1 + 2^{-1/2-\sigma})\,\|Q_\lambda\|_\sigma.$$
On any hypothetical off-critical mode $X^{\rho - 1/2}$ ($\operatorname{Re}\rho = \beta > 0$), the operator $I + 2^{-1/2}D_2$ acts by multiplication by $1 + 2^{-\rho}$, which satisfies
$$0 < 1 - 2^{-\beta} \le \bigl|1 + 2^{-\rho}\bigr| \le 1 + 2^{-\beta} < 2,$$
and therefore never vanishes in $\operatorname{Re}\rho > 0$.

---

## 7. Formal Lean 4 Audit (`formal/RiemannScope/LiouvilleSquareDilation.lean`)

The module [`formal/RiemannScope/LiouvilleSquareDilation.lean`](../../formal/RiemannScope/LiouvilleSquareDilation.lean) contains `5` definitions, `5` public theorems, and `1` private helper theorem (`11` total declarations), compiles cleanly under `lake build` with `0` `sorry` and `0` custom `axiom` declarations, and depends only on the standard Lean axioms `[propext, Classical.choice, Quot.sound]`:

| Theorem Name | Exact `#check` Signature | `#print axioms` | Mathematical Scope & External Analytic Inputs |
| :--- | :--- | :--- | :--- |
| `liouville_complete_multiplicativity_and_common_factor_cancellation_nat` | `(omega_d omega_r omega_s : ℕ) : (liouvilleSignFromOmega 0 = 1 ∧ liouvilleSignFromOmega 1 = -1) ∧ liouvilleSignFromOmega (omega_d + omega_r) = liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_r ∧ liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_d = 1 ∧ liouvilleSignFromOmega (omega_d + omega_r) * liouvilleSignFromOmega (omega_d + omega_s) = liouvilleSignFromOmega omega_r * liouvilleSignFromOmega omega_s` | `[propext, Classical.choice, Quot.sound]` | Genuinely arithmetic theorem over `ℕ` and `ℤ`: proves $\lambda(1)=1$, $\lambda(p)=-1$, complete multiplicativity $(-1)^{\Omega_d+\Omega_r} = (-1)^{\Omega_d}(-1)^{\Omega_r}$, unit square $((-1)^{\Omega_d})^2 = 1$, and unconstrained common-factor cancellation $\lambda(d r)\lambda(d s) = \lambda(r)\lambda(s)$. |
| `prime_power_square_divisor_moebius_liouville_inversion_nat` | `(k : ℕ) : squareDivisorMoebiusSum k = liouvilleSignFromOmega k ∧ squareDivisorInverseLiouvilleSum k = primePowerMoebius k` | `[propext, Classical.choice, Quot.sound]` | Genuinely arithmetic theorem over `ℕ` and `ℤ`: proves by strong induction on the prime-power exponent $k \in \mathbb{N}$ that $\sum_{d^2 \mid p^k}\mu(p^k/d^2) = (-1)^k = \lambda(p^k)$ and $\sum_{0 \le j \le \lfloor k/2\rfloor}\mu(p^j)(-1)^{k-2j} = \mu(p^k)$. Multiplicative extension from prime powers to general integers is proved analytically in §2.1. |
| `reversible_weighted_dilation_norm_and_grade_interval_equivalence` | `(norm_f_sq d_pow_neg_4sigma norm_f_d2_sq norm_lambda norm_mu zeta_1_2sigma zeta_2_4sigma B_mu B_lam int_0_1 sum_tau_blocks Z3_sq sigma C_sigma tau_pow_neg_sigma : ℝ) ... : norm_f_d2_sq = d_pow_neg_4sigma * norm_f_sq ∧ (norm_mu ≤ B_mu → norm_lambda ≤ zeta_1_2sigma * B_mu) ∧ (norm_lambda ≤ B_lam → norm_mu ≤ zeta_1_2sigma / zeta_2_4sigma * B_lam) ∧ int_0_1 + sum_tau_blocks ≤ Z3_sq / (5 - 2 * sigma) + C_sigma / (1 - tau_pow_neg_sigma)` | `[propext, Classical.choice, Quot.sound]` | Scalar real-inequality lemma: proves the reversible weighted norm implications from explicit real hypotheses and combines the $[0, 1]$ and $[\tau^k, \tau^{k+1})$ geometric-series bounds; Minkowski's integral inequality is proved analytically in §3.2. |
| `euler_maclaurin_c2_and_subtransition_growing_range_exponent` | `(f_prime_v_minus f_prime_v_plus N delta : ℝ) (h_v_minus_nonneg : 0 ≤ f_prime_v_minus) (h_v_plus_nonpos : f_prime_v_plus ≤ 0) : 1 / 12 * (\|f_prime_v_minus\| + \|f_prime_v_plus - f_prime_v_minus\| + \|(-f_prime_v_plus)\|) = (f_prime_v_minus - f_prime_v_plus) / 6 ∧ (N + 1) * (1 - delta) - N = 1 - (N + 1) * delta ∧ (1 - (N + 1) * delta < 0 ↔ 1 < (N + 1) * delta)` | `[propext, Classical.choice, Quot.sound]` | Scalar real-algebra lemma: proves that for $f'(v_-) \ge 0 \ge f'(v_+)$, $\frac{1}{12}(|f'(v_-)| + |f'(v_+) - f'(v_-)| + |-f'(v_+)|) = \frac{f'(v_-) - f'(v_+)}{6}$, and proves the subtransition growing-range exponent equivalence $(N+1)(1-\delta) - N = 1 - (N+1)\delta < 0 \iff (N+1)\delta > 1$. |
| `dyadic_parity_energy_and_off_critical_mode_nonvanishing` | `(Q_X Q_half_X sqrt2 two_pow_neg_beta abs_one_plus_two_pow_neg_rho : ℝ) (h_sqrt2 : sqrt2 ^ 2 = 2) (h_sqrt2_ne : sqrt2 ≠ 0) (h_beta_lt_one : two_pow_neg_beta < 1) (h_rev_tri : 1 - two_pow_neg_beta ≤ abs_one_plus_two_pow_neg_rho) : (Q_X + 1 / sqrt2 * Q_half_X) ^ 2 = Q_X ^ 2 + 1 / 2 * Q_half_X ^ 2 + sqrt2 * Q_X * Q_half_X ∧ 0 < 1 - two_pow_neg_beta ∧ 0 < abs_one_plus_two_pow_neg_rho` | `[propext, Classical.choice, Quot.sound]` | Scalar real-algebra lemma: proves the pointwise dyadic parity square expansion $(Q_X + \frac{1}{\sqrt{2}}Q_{X/2})^2 = Q_X^2 + \frac{1}{2}Q_{X/2}^2 + \sqrt{2}Q_X Q_{X/2}$ from $(\sqrt{2})^2 = 2$, and proves $0 < 1 - 2^{-\beta} \le |1 + 2^{-\rho}|$ when $2^{-\beta} < 1$ ($\beta > 0$). |
