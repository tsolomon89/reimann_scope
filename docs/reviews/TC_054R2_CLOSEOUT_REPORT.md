# TASK-TC-054R2 Closeout Report: Fourier Contour Proof, Arithmetic Lean Bridge, and Report Reconciliation

- **Task ID**: `TASK-TC-054R2`
- **Parent Tasks**: `TASK-TC-054` / `TASK-TC-054R`
- **Branch**: `task/tc-054r2-contour-proof-arithmetic-bridge-and-report-closeout`
- **Prior Merged `main` (`TC-053R`)**: `c82e439708b0b6031db6a77bf3977688d9f0758b`
- **Reviewed `TC-053R2` Implementation / Tip**: `cc303030138c670e8f01aaaab483bbeca6bc17d1` / `21576861ecd0dcbf874afec91b299fd6060f4f03`
- **Reviewed `TC-054` Implementation / Tip**: `8f6afcfb9161aa77c74bc40605ac4fabae8b432e` / `cdee197acc9c3e75a4c8cffc94c10bec1bcb97fa`
- **Reviewed `TC-054R` Implementation (Build-Producing Commit) / Reviewed HEAD**: `27489f195d3313d9ee60773157e3a8240f5bcadd` / `f265042ab52cabda29e76859cebace21cfae9239`
- **Subgate Status**: `SUBGATE-TC-043A: OPEN` (`rh_proved: false`)
- **Circle Constant & Coordinate Conventions**: $\tau = 2\pi$ is the sole circle constant throughout. Complex Mellin variables are written $z = a + ib$ ($a, b \in \mathbb{R}$) and nontrivial Riemann zeta zeros are written $\rho = x + iy$ ($x, y \in \mathbb{R}$) with critical coordinate $x = 1/2$. Transcendental Continuation grades remain real algebraic numbers $K \in \mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}$; auxiliary positive real scales ($X, Y, L, M > 0$) and real norm weights ($\eta > 0$) are explicitly distinguished from TC grades.

---

## 1. Complete Fourier Integral-to-Series Proof (§5.2 of `docs/reviews/TC_LIOUVILLE_SQUARE_DILATION.md`)

In the previous `TC-054R` draft of §5.2, the Mellin–Barnes justification contained four mathematical defects:
1. It asserted absolute Fubini integrability of $u^{z-1}\cos(\omega u)$ on $(0, \infty) \times \{z = a_0 + ib\}$, which fails because $|u^{a_0-1}\cos(\omega u)|$ is non-integrable as $u \to \infty$ for $a_0 \ge 0$;
2. It wrote the false reflection formula $\Gamma(1-z)\sin(\tau z/4) = \frac{\tau/2}{\Gamma(z)\cos(\tau z/4)}$, whereas Euler's reflection formula gives $\Gamma(z)\Gamma(1-z) = \frac{\tau/2}{\sin(\tau z/2)} = \frac{\tau/2}{2\sin(\tau z/4)\cos(\tau z/4)}$;
3. It claimed exponential decay of $\frac{1}{\sin(\tau z/4)\Gamma(1-z)}$ on vertical lines $z = a + ib$, whereas by Stirling's formula $|\Gamma(1 - a - ib)| \sim \sqrt{\tau}|b|^{1/2-a}e^{-\tau|b|/4}$ and $|\sin(\tau(a+ib)/4)| \sim \frac{1}{2}e^{+\tau|b|/4}$ cancel in exponential order, and on $a = 1/2$ the product has exact constant modulus $|\sin(\tau(1/2+ib)/4)\Gamma(1/2-ib)| = \frac{\sqrt{\tau}}{2}$;
4. It stated an even-series remainder bound at $m = 2$ whose signs did not match the tail terms for $m \ge 3$.

In `TASK-TC-054R2`, §5.2 of [`docs/reviews/TC_LIOUVILLE_SQUARE_DILATION.md`](file:///c:/Development/Projects/reimann_scope/docs/reviews/TC_LIOUVILLE_SQUARE_DILATION.md) and [`verify_mellin_contour_and_reflection_identities_arb`](file:///c:/Development/Projects/reimann_scope/tc/liouville_square_dilation.py) establish a complete, self-contained two-part derivation:

### 1.1 Real-Variable Integration by Parts for the Conditional Cosine Transform
Setting $u = 1/v$ and $\omega = \tau\xi > 0$,
$$\widehat{f}(\xi) = 2\int_0^\infty u^4 e^{-u^2}\cos(\omega u^{-1})\,du.$$
Writing $\cos(\omega u^{-1}) = -\frac{u^2}{\omega}\frac{d}{du}\!\left[\sin(\omega u^{-1})\right]$ and integrating by parts on $[\varepsilon, R]$ gives
$$\int_\varepsilon^R u^4 e^{-u^2}\cos(\omega u^{-1})\,du = \left[-\frac{u^6 e^{-u^2}\sin(\omega u^{-1})}{\omega}\right]_\varepsilon^R + \frac{1}{\omega}\int_\varepsilon^R (6u^5 - 2u^7)e^{-u^2}\sin(\omega u^{-1})\,du,$$
where boundary terms vanish as $\varepsilon \to 0^+$ and $R \to \infty$, proving $\widehat{f}(\xi) = +\frac{2}{\omega}\int_0^\infty (6u^5 - 2u^7)e^{-u^2}\sin(\omega u^{-1})\,du$. For the conditional cosine transform $\lim_{U\to\infty}\int_0^U u^{z-1}\cos(\omega u)\,du$ on $0 < a = \operatorname{Re}(z) < 1$, integrating by parts on $[\varepsilon, U]$ gives
$$\int_0^U u^{z-1}\cos(\omega u)\,du = \left[\frac{u^{z-1}\sin(\omega u)}{\omega}\right]_0^U + \frac{1-z}{\omega}\int_0^U u^{z-2}\sin(\omega u)\,du \xrightarrow{U\to\infty} \frac{1-z}{\omega}\int_0^\infty u^{z-2}\sin(\omega u)\,du = \Gamma(z)\cos\!\left(\frac{\tau z}{4}\right)\omega^{-z},$$
where $u^{z-1}\sin(\omega u) = O(u^a) \to 0$ as $u \to 0^+$ and $u^{z-2}\sin(\omega u) = O(u^{a-1}) \in L^1(0, 1) \cap L^1(1, \infty)$ for $0 < a < 1$. Because $g(u) := 2u^4 e^{-u^2} \in \mathcal{S}(\mathbb{R}_{>0})$ has rapidly decaying Mellin transform $\mathcal{M}[g](1-z) = \Gamma\!\left(\frac{5-z}{2}\right)$ on $a < 5$, Parseval's Mellin relation holds on $a_0 = 1/2$:
$$\widehat{f}(\xi) = \frac{1}{i\tau}\int_{1/2 - i\infty}^{1/2 + i\infty} \mathcal{M}H(z)\,\omega^{-z}\,dz, \qquad \mathcal{M}H(z) := \Gamma(z)\cos\!\left(\frac{\tau z}{4}\right)\Gamma\!\left(\frac{5+z}{2}\right).$$

### 1.2 Corrected Reflection Identities, DLMF 5.8.3 Lower Bound, and Shifted Contour Decay
By the Gamma reflection formula $\Gamma(w)\Gamma(1-w) = \frac{\tau/2}{\sin(\tau w/2)}$ applied at $w = \frac{5+z}{2}$ (using $\sin(\tau(5+z)/4) = \cos(\tau z/4)$) and at $w = z$:
$$\Gamma\!\left(\frac{5+z}{2}\right)\cos\!\left(\frac{\tau z}{4}\right) = \frac{\tau/2}{\Gamma\!\left(\frac{-3-z}{2}\right)}, \qquad \Gamma(z)\Gamma(1-z) = \frac{\tau/2}{\sin(\tau z/2)} = \frac{\tau/2}{2\sin(\tau z/4)\cos(\tau z/4)},$$
so $\mathcal{M}H(z)$ has the three equivalent exact representations:
$$\mathcal{M}H(z) = \Gamma(z)\cos\!\left(\frac{\tau z}{4}\right)\Gamma\!\left(\frac{5+z}{2}\right) = \frac{(\tau/2)\,\Gamma(z)}{\Gamma\!\left(\frac{-3-z}{2}\right)} = \frac{(\tau/2)^2}{\sin(\tau z/2)\,\Gamma(1-z)\,\Gamma\!\left(\frac{-3-z}{2}\right)}.$$
To bound the denominator on vertical lines and horizontal segments in the left half-plane without Stirling approximations, we use the explicit Weierstrass product inequality ([DLMF 5.8.3](https://dlmf.nist.gov/5.8#E3)) valid for all $R \ge 1/2$ and $y \in \mathbb{R}$:
$$\bigl|\Gamma(R + iy)\bigr| = \Gamma(R)\prod_{k=0}^\infty\left(1 + \frac{y^2}{(R + k)^2}\right)^{-1/2} \ge \Gamma(R)\prod_{k=0}^\infty\left(1 + \frac{y^2}{(1/2 + k)^2}\right)^{-1/2} = \frac{\Gamma(R)}{\sqrt{\cosh(\tau y/2)}} \ge \Gamma(R)\,e^{-\tau|y|/4}.$$
On the shifted vertical contour $z = a_M + ib$ at $a_M = -(2M + 3/2)$ for integer $M \ge 2$:
- Since $\frac{\tau a_M}{2} = -(M + 1)\tau + \frac{\tau}{4}$, we have $\sin(\tau(a_M + ib)/2) = \sin(\frac{\tau}{4} + i\frac{\tau b}{2}) = +\cosh(\tau b/2) > 0$, so $|\sin(\tau z/2)| = \cosh(\tau b/2) \ge \frac{1}{2}e^{\tau|b|/2}$;
- Applying DLMF 5.8.3 to $1 - z = (2M + 5/2) - ib$ ($R_1 = 2M + 5/2 \ge 13/2$) and $\frac{-3-z}{2} = (M - 3/4) - ib/2$ ($R_2 = M - 3/4 \ge 5/4$) yields
  $$|\Gamma(1-z)| \ge \Gamma(2M+5/2)e^{-\tau|b|/4}, \qquad \left|\Gamma\!\left(\frac{-3-z}{2}\right)\right| \ge \Gamma(M-3/4)e^{-\tau|b|/8}.$$
Combining the three factors shows that the exponential growth $e^{3\tau|b|/8}$ of $|\Gamma(1-z)\Gamma((-3-z)/2)|^{-1}$ is dominated by $|\sin(\tau z/2)| \ge \frac{1}{2}e^{\tau|b|/2}$ with net exponential decay $e^{-\tau|b|/8}$:
$$|\mathcal{M}H(a_M + ib)| \le \frac{(\tau/2)^2}{\cosh(\tau b/2)\,\Gamma(2M+5/2)\,\Gamma(M-3/4)\,e^{-3\tau|b|/8}} \le \frac{2(\tau/2)^2\,e^{-\tau|b|/8}}{\Gamma(2M+5/2)\,\Gamma(M-3/4)}.$$
Integrating along $z = a_M + ib$ ($b \in \mathbb{R}$) gives the explicit contour remainder bound:
$$|R_M(\omega)| = \left|\frac{1}{i\tau}\int_{a_M - i\infty}^{a_M + i\infty}\mathcal{M}H(z)\,\omega^{-z}\,dz\right| \le \frac{8\,\omega^{2M+3/2}}{\Gamma(2M+5/2)\,\Gamma(M-3/4)} \xrightarrow{M\to\infty} 0 \qquad (\forall\,\omega > 0),$$
and horizontal segments at height $|b| = T \to \infty$ vanish as $O(e^{-\tau T/8})$.

### 1.3 Corrected Even-Series Tail Sign Analysis
In the even subseries $\sum_{m=0}^\infty \frac{(-1)^m\Gamma(5/2-m)}{(2m)!}\omega^{2m}$:
- For $m = 0$: $(-1)^0\Gamma(5/2) = \frac{3\sqrt{\tau/2}}{4} > 0$;
- For $m = 1$: $(-1)^1\Gamma(3/2)\frac{\omega^2}{2!} = -\frac{\sqrt{\tau/2}}{4}\omega^2 < 0$;
- For every integer $m \ge 2$: $5/2 - m = -(m - 5/2) < 0$ lies in the interval $(-m + 2, -m + 3)$, where $\operatorname{sgn}\Gamma(5/2 - m) = (-1)^m$, so
  $$(-1)^m\Gamma\!\left(\frac{5}{2} - m\right) = \left|\Gamma\!\left(\frac{5}{2} - m\right)\right| = \frac{\sqrt{\tau/2}}{\prod_{j=1}^{m-2}\!\left(j - \frac{1}{2}\right)} > 0 \qquad (\forall\,m \ge 2).$$
In particular, the $m = 2, 3, 4, \dots$ even terms all have **strictly positive** coefficients (for example, at $m = 3$, $\frac{(-1)^3\Gamma(-1/2)\omega^6}{6!} = +\frac{2\sqrt{\tau/2}\,\omega^6}{6!} > 0$ does not alternate against $m = 2$). Both our geometric tail bound (`R_even(K_eff, omega) <= 1/2` for $K_{\mathrm{eff}} \ge 2$) and the non-negative lower bound for the positive even tail from $m = 2$ onward are therefore unconditionally valid.

---

## 2. Pairwise Counterexample to the Spurious $\frac{1}{2\sqrt{2}}$ Factor (§4.3)

In `tc/liouville_square_dilation.py` (`pairwise_spurious_factor_counterexample_regression`), we evaluate at $r = 1$, $s = 1$, $L = \frac{9}{5} = 1.8$, $X = \frac{L}{\sqrt{2}} = \frac{9}{5\sqrt{2}}$ (`D_cutoff = 1000` with tail $\sum_{d > 1000} d^{-6} < \frac{1}{5\cdot 1000^5} = 2\times 10^{-16}$ enclosed in the ball):
- Normalized Euler–Maclaurin remainder ratio:
  $$\frac{|E_{1,1}^{(\lambda)}(X)|}{C_2 X^{-2} (rs)^4 / (r^2+s^2)^{7/2}} = \frac{\left|\sum_{d=1}^\infty d^{-6}e^{-L^2/d^2} - c_0 L^{-5}\right|}{C_2 L^{-7}} = [0.4030344210273 \pm 4.02 \times 10^{-14}] > \frac{1}{2\sqrt{2}} = [0.3535533905932737622004221810524245196424 \pm 1.80 \times 10^{-41}],$$
  with certified strictly positive difference:
  $$\text{ratio} - \frac{1}{2\sqrt{2}} = [+0.04948103043406 \pm 6.81 \times 10^{-15}] > 0.$$
- Direct pairwise error vs. spurious and repaired bounds at $(r, s) = (1, 1)$:
  $$\bigl|E^\lambda_{1,1}(X)\bigr| = [0.04070886643302 \pm 1.98 \times 10^{-15}] > \frac{C_2}{2\sqrt{2}}X^{-2}\frac{1}{2^{7/2}} = [0.03571098894708638226950151155866800331098 \pm 2.90 \times 10^{-42}],$$
  while satisfying the repaired pairwise bound $C_2 X^{-2}\frac{1}{2^{7/2}} = [0.1010059297894505107100302740960207508287 \pm 7.19 \times 10^{-42}]$. This directly falsifies the old `TC-054` draft factor $\frac{1}{2\sqrt{2}}$ on the unreduced pairwise formula while confirming that $\frac{1}{2\sqrt{2}}$ arises only after applying AM–GM $r^2 + s^2 \ge 2rs$ in the summed coprime bound.

---

## 3. Separate Series and Quadrature Accuracy Fields & Enclosure Mode (§5.3)

Each of the 6 Fourier sign-change witnesses $\xi \in \{0, 1/2, 4/\tau, 1, 3/2, 2\}$ in `section_5_transition_poisson_summation.hat_f_sign_change_witnesses` records separate accuracy metadata for the power-series evaluation and the independent `acb.integral` quadrature cross-check:

| $\xi$ | $\widehat{f}(\xi)$ (256-bit Arb series) | `working_prec_bits` | $K_{\mathrm{eff}}$ | `series_total_radius` | `quadrature_interval` $[v_0, V_1]$ | `quadrature_right_tail_bound` $\frac{2}{5V_1^5}$ | `quadrature_total_radius` | `quadrature_contains_series` | `series_overlaps_quadrature` |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $0$ | `[1.329340388179137020473625612505858887098 +/- 1.63e-40]` | $512$ | $200$ | `1.56e-154` | `[1/7, 32]` | `1.1920928955e-8` | `1.1920928980e-8` | `True` | `True` |
| $1/2$ | `[-0.5628546550179851263755109492164491931001 +/- 4.04e-41]` | $525$ | $200$ | `5.41e-155` | `[1/7, 32]` | `1.1920928955e-8` | `1.1920928980e-8` | `True` | `True` |
| $4/\tau$ | `[-0.7757751802167744117629682956314216290713 +/- 2.04e-41]` | $529$ | $200$ | `7.63e-77` | `[1/7, 32]` | `1.1920928955e-8` | `1.1920928980e-8` | `True` | `True` |
| $1$ | `[-0.3668367826642069184644449070564857828859 +/- 4.03e-41]` | $538$ | $200$ | `4.20e-157` | `[1/7, 32]` | `1.1920928955e-8` | `1.1920928980e-8` | `True` | `True` |
| $3/2$ | `[0.2636171831500303372338138695632955698496 +/- 2.39e-41]` | $550$ | $200$ | `1.71e-159` | `[1/7, 32]` | `1.1920928955e-8` | `1.1920928980e-8` | `True` | `True` |
| $2$ | `[0.1247126116325928138362162976104693467978 +/- 9.77e-42]` | $563$ | $200$ | `8.59e-162` | `[1/7, 32]` | `1.1920928955e-8` | `1.1920928980e-8` | `True` | `True` |

In addition, `legacy_k1_fourier_counterexample_regression` checks both `.contains(...)` (`repaired_k4_contains_adaptive == True`, since the coarse $K=4$ enclosure `[-1e+0 +/- 0.605]` strictly contains the adaptive $K_{\mathrm{eff}}=200$ ball `[-0.7757751802167744117629682956314216290713 +/- 2.04e-41]`) and `.overlaps(...)` (`repaired_k4_overlaps_adaptive == True`).

---

## 4. Actual Flat Square-Divisor Sums & Finite Square Sum in Lean 4 (`formal/RiemannScope/LiouvilleSquareDilation.lean`)

In [`formal/RiemannScope/LiouvilleSquareDilation.lean`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/LiouvilleSquareDilation.lean), we expanded the formalization from 24 declarations to **35 declarations** (`15` definitions, `8` public theorems, `12` private helper theorems; `0` `sorry`, `0` custom `axiom`):
1. **Actual Flat Square-Divisor Sums**:
   - `squareDivisors (n : ℕ) : Finset ℕ := (Nat.divisors n).filter (fun d => d ^ 2 ∣ n)`
   - `actualFlatMoebiusSquareDivisorSum (n : ℕ) : ℤ := ∑ d ∈ squareDivisors n, (ArithmeticFunction.moebius (n / d ^ 2) : ℤ)`
   - `actualFlatInverseLiouvilleSquareDivisorSum (n : ℕ) : ℤ := ∑ d ∈ squareDivisors n, (ArithmeticFunction.moebius d : ℤ) * liouvilleLambda (n / d ^ 2)`
   - `actualFlatMoebiusSquareArith` and `actualFlatInverseLiouvilleSquareArith` as `ArithmeticFunction ℤ` instances.
2. **Unconditional Multiplicativity & Actual Integer Identities (`actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat`)**:
   - Removed the assumed multiplicative surrogate `S` from Theorem 4;
   - Proved `sum_squareDivisors_mul_of_coprime_aux` via `Finset.sum_bij` (establishing $(d_1, d_2) \mapsto d_1 d_2$ as a bijection `squareDivisors m ×ˢ squareDivisors n → squareDivisors (m * n)` for `Nat.Coprime m n` with exact division compatibility `(m * n) / (d_1 * d_2)^2 = (m / d_1^2) * (n / d_2^2)`), proving `actualFlatMoebiusSquareArith.IsMultiplicative` and `actualFlatInverseLiouvilleSquareArith.IsMultiplicative` unconditionally;
   - Proved `squareDivisors_prime_pow_aux` showing that on prime powers $p^k$, the flat Finset sum over `squareDivisors (p ^ k)` equals the exponent-index sum `primePowerActualMoebiusSquareSum p k` and `primePowerActualInverseLiouvilleSquareSum p k`;
   - Combined `ArithmeticFunction.IsMultiplicative.multiplicative_factorization` with our prime-power lemmas to prove unconditionally for **every** positive integer $n \ne 0$:
     $$\texttt{actualFlatMoebiusSquareDivisorSum } n = \lambda(n), \qquad \texttt{actualFlatInverseLiouvilleSquareDivisorSum } n = \mu(n).$$
3. **Finite Square Sum & Unequal-Block Coefficient Inequality (`abel_scaling_fourier_ratio_and_unequal_block_algebra`)**:
   - Proved `sum_range_sq_mul_six_aux` by induction on $n$: `6 * (∑ r ∈ Finset.range n, r ^ 2) = (n - 1) * n * (2 * n - 1)`;
   - Extended Theorem 8 to prove for all integers $A \ge 1$ over `Finset.Ico A (2 * A)`:
     $$6\sum_{r=A}^{2A-1} r^2 + (A - 1)A(2A - 1) = (2A - 1)(2A)(4A - 1), \qquad 6\sum_{r=A}^{2A-1} r^2 + 9A^2 = 14A^3 + A, \qquad 3\sum_{r=A}^{2A-1} r^2 < 7A^3.$$

---

## 5. Compact-Range Energy Bound & Corpus Formula Synchronization

- **Compact-Range & Global Energy Bounds (§6.1)**:
  - For $1 \le X \le 256$, $|Q_\lambda(X)| \le X^{5/2}\sum_{n\ge 1} n^{-3} = \zeta(3) X^{5/2}$, so for $1 \le Y \le 256$:
    $$\int_Y^{\tau Y} |Q_\lambda(X)|^2\,\frac{dX}{X} \le \zeta(3)^2\int_Y^{\tau Y} X^4\,dX = \frac{\zeta(3)^2(\tau^5 - 1)}{5}\,Y^5,$$
    with certified 256-bit Arb constant:
    $$\frac{\zeta(3)^2(\tau^5 - 1)}{5} = [2829.665108928656654314420748974452322268 \pm 2.09 \times 10^{-37}].$$
  - Consequently, the stretched-exponential bound $\int_Y^{\tau Y}|Q_\lambda(X)|^2\,\frac{dX}{X} \ll Y\exp(-2c_2\Phi(Y))$ holds for all $Y \ge 256$, and combining with the compact interval $[2, 256]$ yields $\int_Y^{\tau Y}|Q_\lambda(X)|^2\,\frac{dX}{X} \ll_D Y(\log Y)^{-D}$ for all $Y \ge 2$ and every $D > 0$.
- **Corpus Synchronization**:
  - Updated `RESEARCH_LEDGER.md`, `TRANSCENDENTAL_CONTINUATION.md`, `.agents/corpus_map/obligation_register.md`, `docs/reviews/TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md`, `formal/RiemannScope/README.md`, `.agents/research/queue.json`, and `.agents/research/state.json` to eliminate all stale `TC-054` draft formulas ($d^{-5/2}Q_\mu(X/d) \to d^{-1}Q_\mu(X/d^2)$, $\frac{C_2}{2\sqrt{2}} \to C_2$, $d^{-6}/e^{-6} \to d^{-1}/\mu(e)e^{-1}$, $Q_\lambda(X) + \frac{1}{8}Q_\lambda(X/2) \to Q_\lambda(X) + 2^{-1/2}Q_\lambda(X/2)$, $1 + 2^{-(2+z)} \to 1 + 2^{-\rho}$, `24` declarations $\to$ `35` declarations, `9` tests $\to$ `12` tests / `87` total tests).
