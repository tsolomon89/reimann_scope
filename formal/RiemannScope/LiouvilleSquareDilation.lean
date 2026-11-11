/-
RiemannScope.LiouvilleSquareDilation
TASK-TC-054 / TASK-TC-054R / TASK-TC-054R2 / TASK-TC-055 / TASK-TC-055R / TASK-TC-055R2 / TASK-TC-056 / TASK-TC-057 / TASK-TC-057R:
1. Actual arithmetic definitions and theorems over `ℕ` and `ℤ` using Mathlib's
   `ArithmeticFunction.cardFactors` (`Ω`), `Nat.factorization`, `Nat.divisors`, and
   `ArithmeticFunction.moebius` (`μ`):
   - Connection of `Ω(n)` to prime-factorization multiplicities `(n.factorization.sum fun _ e => e) = natOmega n`;
   - Additivity `natOmega (m * n) = natOmega m + natOmega n` for positive integers;
   - Actual Liouville function `liouvilleLambda n = (-1)^{Ω(n)}`, its `ArithmeticFunction ℤ` wrapper
     `liouvilleArith`, complete multiplicativity `liouvilleLambda (m * n) = liouvilleLambda m * liouvilleLambda n`,
     unit square `liouvilleLambda d * liouvilleLambda d = 1`, and unconstrained common-factor sign cancellation
     `liouvilleLambda (d * r) * liouvilleLambda (d * s) = liouvilleLambda r * liouvilleLambda s`;
   - Explicit finite square-divisor set `squareDivisors n = (Nat.divisors n).filter (fun d => d ^ 2 ∣ n)` and
     actual flat square-divisor sums on `ℕ`:
       `actualFlatMoebiusSquareDivisorSum n = ∑ d ∈ squareDivisors n, μ(n / d^2)` and
       `actualFlatInverseLiouvilleSquareDivisorSum n = ∑ d ∈ squareDivisors n, μ(d) λ(n / d^2)`,
     with unconditional proofs of their multiplicativity (`IsMultiplicative`), prime-power evaluation,
     factored prime-power product formulas over `n.factorization.prod`, and full integer identities
     `actualFlatMoebiusSquareDivisorSum n = liouvilleLambda n` and
     `actualFlatInverseLiouvilleSquareDivisorSum n = ArithmeticFunction.moebius n` for all `n ≠ 0`;
   - Actual finite-prime exclusion sieve sum `actualPrimeExclusionSieveSum N_P n = ∑_{d ∣ gcd(n, N_P)} μ(d)^2 λ(n / d)`,
     proving `μ(d)^2 λ(n / d) = λ(n) μ(d)` for `d ∣ gcd(n, N_P)` and
     `actualPrimeExclusionSieveSum N_P n = if n.Coprime N_P then liouvilleLambda n else 0` (`TASK-TC-055` §3);
   - Multiplicative parity controls `primeParityControl p n = (-1)^{v_p(n)}` and `twoAdicParityControl n = (-1)^{v_2(n)}`,
     proving complete multiplicativity, common-factor cancellation, prime parity flip `a_p(p n) = -a_p(n)`,
     and exact separation from `liouvilleLambda` and `actualFlatMoebiusSquareDivisorSum` at odd prime `n = 3` (`TASK-TC-055` §7);
   - Full finite `P`-smooth / `P`-coprime factorization existence & uniqueness (`n = m * r`), finite cutoff indexing
     bijection for `1 ≤ n ≤ T` with inner cutoff `r ≤ ⌊T/m⌋`, arbitrary-weight reindexed Liouville sum and coprime-outer
     regrouping, exact uncoupled-cutoff (`r ≤ T`) excess sum with vanishing (`P = ∅`, `T ≤ 1`, `(P = {2}, T = 2)`) and
     nonvanishing (`(P = {2}, T = 3)`) witnesses, finite Gaussian observable `Q_{λ,T}(X)` reconstruction, and exact
     pointwise weighted cofactor square expansion with `1/r` and `λ(r)λ(s)/√(rs)` (`TASK-TC-055R2` §§2–3);
   - Pointwise finite prime filtration (`pointwiseGroupedEnergyV`), endpoints `V_∅ = D_T` and `V_{primes ≤ T} = Q_T^2`,
     prime-adjoining fiber reconstruction `F_{P ∪ {p}, s} = ∑_{s p^k ≤ T} F_{P, s p^k}`, exact pointwise increment
     `Δ_{P,p}` and ascending-prime telescoping, finite alternating-unimodal chain inequality `|∑ (-1)^k a_k| ≤ max_k a_k`
     and `(∑ (-1)^k a_k)^2 ≤ ∑ a_k^2` (with empty-safe max, zero chains, one-term chains, ties, zero extension, and
     quantitative two-term strict gap), unconditional Gaussian prime-chain unimodality and singleton contraction
     `V_{p} ≤ D_T` (strict `<` for `X > 0, T ≥ p`), and exact mixed-interaction decomposition `Δ_{P,p} = M_{P,p} - C_{P,p}`
     with `C_{P,p} ≥ 0`, `P`-independence `C_{P,p} = C_p = D_T - V_{p}` via `r = s m`, and exact alternating shift sum
     for `C_p` (`TASK-TC-056` §§3–6);
   - Monotone scale envelope `monotoneScaleEnvelope E Y = sSup (E '' Set.Icc 1 Y)` local boundedness without continuity,
     `E`-to-`F` envelope passage, `CONDITIONAL_ON_RECURSION` dyadic-height bootstrap descent to `F Y ≤ C_ε Y^ε` without
     requiring `B_η < 1`, weighted multi-scale contraction step & homogeneous lower-bound obstruction, general
     Möbius–rough prime-filtration descent (Route A) for arbitrary `U ≥ 2` with uniform Liouville sign `μ(d)λ(d) = 1`
     vs `a_2` sign alternation and super-`√T` prime reduction, exact logarithmic prime-power descent & scale-invariant
     kernel-shift hierarchy `Q_T^{[m]}` with `M`-step telescope (Route B, including `T = 0, 1`), exact quadratic
     prime-power diagonal/off-diagonal square expansion (Route D), and inherited-vs-canonical cutoff comparison
     `T(W) ≤ ⌊T(W d)/d⌋` (`d ≥ 16, W ≥ 1`), `(Y = 9/4, d = 2)` counterexample `⌊T(9/4)/2⌋ = 1 < 2 = T(9/8)`,
     unconditional small-scale positivity `finiteQLambda L w ≥ (1/24) w^{5/2} > 0` for all `L ≥ 1, w ∈ (0, 1]`,
     and `CONDITIONAL_ON_SIGNED_CORRELATION` finite-horizon same-scale absorption transfer via
     `normalizedScaleSupremum E eps R` (`conditional_signed_correlation_same_scale_absorption_transfer_tc057r`,
     preserving exact outer factor `2` and `θ_η ∈ [0, 1/2)` plus repaired Proposition 2.4 localization vs.
     `d_top ≥ Y/2` concentration negative control) (`TASK-TC-057` / `TASK-TC-057R` §§3–6).
2. Prime-power exponent models (`liouville_complete_multiplicativity_and_common_factor_cancellation_nat`
   and `prime_power_square_divisor_moebius_liouville_inversion_nat`).
3. Scalar real-algebra, real-inequality, and finite-sum lemmas for weighted norm bounds, Euler-Maclaurin `C_2`
   and subtransition exponents, dyadic parity square expansion, Stieltjes endpoint antiderivative algebra,
   Fourier tail ratio denominator monotonicity, exact dyadic block square sum `∑_{A ≤ r < 2A} r^2`,
   unequal-block reciprocal-cube bound algebra, finite near-diagonal kernel bound `(2H + 1) D_E` (conditional on
   `hK` and `hBand`), opposite-parity prime-semiprime dilation pairing `λ(p m) + λ(q r m) = 0`, `a_2` and `a_{3,5,7}`
   control constants, retired TC-055 Lemma 6.1 counterexample inequality, valid replacement kernel ratio enclosure,
   non-integer cutoff `u = 2.9` counterexample, and cutoff/scalar truncation algebra (`TASK-TC-055R`).
-/

import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.NumberTheory.ArithmeticFunction
import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.Tactic
import RiemannScope.Basic

open scoped ArithmeticFunction

namespace RiemannScope

namespace LiouvilleSquareDilation

/-- Prime-power Möbius value `mu(p^e)` on exponent `e : ℕ` (exponent model):
    `mu(p^0) = 1`, `mu(p^1) = -1`, and `mu(p^{e+2}) = 0`. -/
def primePowerMoebius : ℕ → ℤ
  | 0 => 1
  | 1 => (-1 : ℤ)
  | _ + 2 => 0

/-- Liouville sign `(-1)^{omega_n}` as a function of a natural-number exponent `omega_n : ℕ`. -/
def liouvilleSignFromOmega (omega_n : ℕ) : ℤ :=
  (-1 : ℤ) ^ omega_n

/-- Actual prime-factor multiplicity count `Ω(n) = ArithmeticFunction.cardFactors n` on `ℕ`. -/
def natOmega (n : ℕ) : ℕ :=
  ArithmeticFunction.cardFactors n

/-- Actual Liouville function `λ(n) = (-1)^{Ω(n)}` for `n ≥ 1` (`λ(0) = 0`) on `ℕ`. -/
def liouvilleLambda (n : ℕ) : ℤ :=
  if n = 0 then 0 else liouvilleSignFromOmega (natOmega n)

/-- `ArithmeticFunction ℤ` bundling of `liouvilleLambda` (`liouvilleLambda 0 = 0`). -/
def liouvilleArith : ArithmeticFunction ℤ :=
  ⟨liouvilleLambda, rfl⟩

/-- Finite range sum `sum_{0 <= j < m} f(j)` over `ℕ`. -/
def finRangeSum (f : ℕ → ℤ) : ℕ → ℤ
  | 0 => 0
  | m + 1 => finRangeSum f m + f m

/-- Recursive square-divisor Möbius sum `sum_{d^2 | p^k} mu(p^k / d^2)` on prime-power exponent `k : ℕ`
    (exponent model). -/
def squareDivisorMoebiusSum : ℕ → ℤ
  | 0 => primePowerMoebius 0
  | 1 => primePowerMoebius 1
  | k + 2 => primePowerMoebius (k + 2) + squareDivisorMoebiusSum k

/-- Indexed finite-sum representation `sum_{0 <= j <= k/2} mu(p^j) * (-1)^{k - 2j}` on exponent `k : ℕ`
    (exponent model). -/
def squareDivisorInverseLiouvilleSum (k : ℕ) : ℤ :=
  finRangeSum (fun j => primePowerMoebius j * ((-1 : ℤ) ^ (k - 2 * j))) (k / 2 + 1)

/-- Actual prime-power square-divisor Möbius sum `∑_{0 ≤ j ≤ k/2} μ(p^{k - 2j})` evaluated with
    Mathlib's `ArithmeticFunction.moebius`. -/
def primePowerActualMoebiusSquareSum (p k : ℕ) : ℤ :=
  finRangeSum (fun j => ArithmeticFunction.moebius (p ^ (k - 2 * j))) (k / 2 + 1)

/-- Actual prime-power inverse square-divisor sum `∑_{0 ≤ j ≤ k/2} μ(p^j) λ(p^{k - 2j})` evaluated with
    Mathlib's `ArithmeticFunction.moebius` and `liouvilleLambda`. -/
def primePowerActualInverseLiouvilleSquareSum (p k : ℕ) : ℤ :=
  finRangeSum (fun j => ArithmeticFunction.moebius (p ^ j) * liouvilleLambda (p ^ (k - 2 * j))) (k / 2 + 1)

/-- Finite set of positive divisors `d` of `n` whose square divides `n` (`d ^ 2 ∣ n`). -/
def squareDivisors (n : ℕ) : Finset ℕ :=
  (Nat.divisors n).filter (fun d => d ^ 2 ∣ n)

/-- Actual flat square-divisor Möbius sum `∑_{d^2 ∣ n} μ(n / d^2)` on `ℕ`. -/
def actualFlatMoebiusSquareDivisorSum (n : ℕ) : ℤ :=
  ∑ d ∈ squareDivisors n, ArithmeticFunction.moebius (n / (d ^ 2))

/-- Actual flat inverse Liouville square-divisor sum `∑_{d^2 ∣ n} μ(d) λ(n / d^2)` on `ℕ`. -/
def actualFlatInverseLiouvilleSquareDivisorSum (n : ℕ) : ℤ :=
  ∑ d ∈ squareDivisors n, ArithmeticFunction.moebius d * liouvilleLambda (n / (d ^ 2))

/-- `ArithmeticFunction ℤ` wrapper for `actualFlatMoebiusSquareDivisorSum`. -/
def actualFlatMoebiusSquareArith : ArithmeticFunction ℤ :=
  ⟨actualFlatMoebiusSquareDivisorSum, by simp [actualFlatMoebiusSquareDivisorSum, squareDivisors]⟩

/-- `ArithmeticFunction ℤ` wrapper for `actualFlatInverseLiouvilleSquareDivisorSum`. -/
def actualFlatInverseLiouvilleSquareArith : ArithmeticFunction ℤ :=
  ⟨actualFlatInverseLiouvilleSquareDivisorSum,
    by simp [actualFlatInverseLiouvilleSquareDivisorSum, squareDivisors]⟩

/-- Single-prime parity control `a_p(n) = (-1)^{v_p(n)}` for `n ≥ 1` (`a_p(0) = 0`) on `ℕ`,
    using `n.factorization p`. -/
def primeParityControl (p n : ℕ) : ℤ :=
  if n = 0 then 0 else (-1 : ℤ) ^ (n.factorization p)

/-- The 2-adic parity control `a_2(n) = (-1)^{v_2(n)}` (`TASK-TC-055` §7) on `ℕ`. -/
def twoAdicParityControl (n : ℕ) : ℤ :=
  primeParityControl 2 n

/-- `ArithmeticFunction ℤ` wrapper for `primeParityControl p`. -/
def primeParityControlArith (p : ℕ) : ArithmeticFunction ℤ :=
  ⟨primeParityControl p, by simp [primeParityControl]⟩

/-- Actual finite-prime exclusion sieve sum `∑_{d ∣ gcd(n, N_P)} μ(d)^2 λ(n / d)` (`TASK-TC-055` §3) on `ℕ`. -/
def actualPrimeExclusionSieveSum (N_P n : ℕ) : ℤ :=
  ∑ d ∈ Nat.divisors (Nat.gcd n N_P), (ArithmeticFunction.moebius d) ^ 2 * liouvilleLambda (n / d)

/-- Auxiliary `ArithmeticFunction ℤ` for `d ↦ μ(d)^2 λ(d)`. -/
def muSqTimesLambdaArith : ArithmeticFunction ℤ :=
  ⟨fun d => (ArithmeticFunction.moebius d) ^ 2 * liouvilleLambda d, by simp [liouvilleLambda]⟩

/-- Pointwise factorized kernel integrand `X4 * g a * g b` (representing `X^4 * g_X(a) * g_X(b)`
    inside `K_Y(a, b) = ∫_Y^{τ Y} X^4 g_X(a) g_X(b) dX`, where `g_X(u) = u^{-3} exp(-X^2 / u^2)`). -/
def kernelPointwiseIntegrand (g : ℕ → ℝ) (X4 : ℝ) (a b : ℕ) : ℝ :=
  X4 * g a * g b

/-- **Theorem 1 (`TASK-TC-054` §2–§4, Exponent Model)**: Complete multiplicativity and common-factor
    sign cancellation for `liouvilleSignFromOmega` on natural-number exponents `omega_d, omega_r, omega_s : ℕ`. -/
theorem liouville_complete_multiplicativity_and_common_factor_cancellation_nat
    (omega_d omega_r omega_s : ℕ) :
    (liouvilleSignFromOmega 0 = 1 ∧ liouvilleSignFromOmega 1 = -1) ∧
    liouvilleSignFromOmega (omega_d + omega_r) =
      liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_r ∧
    liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_d = 1 ∧
    liouvilleSignFromOmega (omega_d + omega_r) * liouvilleSignFromOmega (omega_d + omega_s) =
      liouvilleSignFromOmega omega_r * liouvilleSignFromOmega omega_s := by
  have h_base : liouvilleSignFromOmega 0 = 1 ∧ liouvilleSignFromOmega 1 = -1 := by decide
  have h_mul_dr :
      liouvilleSignFromOmega (omega_d + omega_r) =
        liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_r := by
    dsimp [liouvilleSignFromOmega]
    exact pow_add (-1 : ℤ) omega_d omega_r
  have h_mul_ds :
      liouvilleSignFromOmega (omega_d + omega_s) =
        liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_s := by
    dsimp [liouvilleSignFromOmega]
    exact pow_add (-1 : ℤ) omega_d omega_s
  have h_sq : liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_d = 1 := by
    dsimp [liouvilleSignFromOmega]
    rw [← pow_add]
    have h_even : omega_d + omega_d = 2 * omega_d := by omega
    rw [h_even, pow_mul]
    norm_num
  have h_cancel :
      liouvilleSignFromOmega (omega_d + omega_r) * liouvilleSignFromOmega (omega_d + omega_s) =
        liouvilleSignFromOmega omega_r * liouvilleSignFromOmega omega_s := by
    rw [h_mul_dr, h_mul_ds]
    calc
      (liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_r) *
          (liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_s) =
        (liouvilleSignFromOmega omega_d * liouvilleSignFromOmega omega_d) *
          (liouvilleSignFromOmega omega_r * liouvilleSignFromOmega omega_s) := by ring
      _ = 1 * (liouvilleSignFromOmega omega_r * liouvilleSignFromOmega omega_s) := by rw [h_sq]
      _ = liouvilleSignFromOmega omega_r * liouvilleSignFromOmega omega_s := by ring
  exact ⟨h_base, h_mul_dr, h_sq, h_cancel⟩

/-- Helper lemma: for any `k >= 2` and any tail length `r : ℕ`, adding `r` terms with index `j + 2`
    to `finRangeSum` contributes `0` because `primePowerMoebius (j + 2) = 0`. -/
private theorem finRangeSum_primePowerMoebius_tail_eq_two
    (k : ℕ) :
    ∀ r : ℕ,
      finRangeSum (fun j => primePowerMoebius j * ((-1 : ℤ) ^ (k - 2 * j))) (r + 2) =
        finRangeSum (fun j => primePowerMoebius j * ((-1 : ℤ) ^ (k - 2 * j))) 2 := by
  intro r
  induction r with
  | zero => rfl
  | succ r ih =>
    have h_step : r + 1 + 2 = (r + 2) + 1 := by omega
    rw [h_step]
    dsimp [finRangeSum]
    have h_pm : primePowerMoebius (r + 2) = 0 := rfl
    rw [h_pm, zero_mul, add_zero]
    exact ih

/-- Helper lemma: `natOmega (p ^ k) = k` for any prime `p` and exponent `k : ℕ`. -/
private theorem cardFactors_prime_pow_aux {p : ℕ} (hp : p.Prime) (k : ℕ) :
    natOmega (p ^ k) = k := by
  dsimp [natOmega]
  induction k with
  | zero => simp
  | succ k ih =>
    rw [pow_succ, ArithmeticFunction.cardFactors_mul (pow_ne_zero k hp.ne_zero) hp.ne_zero]
    have hp1 : ArithmeticFunction.cardFactors p = 1 :=
      ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr hp
    omega

/-- Helper lemma: Mathlib's `ArithmeticFunction.moebius (p ^ k)` agrees with `primePowerMoebius k`
    for every prime `p` and exponent `k : ℕ`. -/
private theorem moebius_apply_prime_pow_eq_primePowerMoebius_aux {p : ℕ} (hp : p.Prime) (k : ℕ) :
    ArithmeticFunction.moebius (p ^ k) = primePowerMoebius k := by
  rcases k with _ | _ | k'
  · simp [primePowerMoebius, ArithmeticFunction.moebius_apply_one]
  · simp [primePowerMoebius, ArithmeticFunction.moebius_apply_prime hp]
  · rw [ArithmeticFunction.moebius_apply_prime_pow hp (by omega)]
    simp [primePowerMoebius]

/-- Helper lemma: `liouvilleLambda (p ^ k) = liouvilleSignFromOmega k` for any prime `p` and `k : ℕ`. -/
private theorem liouvilleLambda_prime_pow_aux {p : ℕ} (hp : p.Prime) (k : ℕ) :
    liouvilleLambda (p ^ k) = liouvilleSignFromOmega k := by
  have hne : p ^ k ≠ 0 := pow_ne_zero k hp.ne_zero
  simp [liouvilleLambda, hne, cardFactors_prime_pow_aux hp k]

/-- Helper congruence lemma for `finRangeSum`. -/
private theorem finRangeSum_congr_aux {f g : ℕ → ℤ} (m : ℕ) (h : ∀ j < m, f j = g j) :
    finRangeSum f m = finRangeSum g m := by
  induction m with
  | zero => rfl
  | succ m ih =>
    dsimp [finRangeSum]
    rw [ih (fun j hj => h j (by omega)), h m (by omega)]

/-- Helper zero lemma for `finRangeSum`. -/
private theorem finRangeSum_eq_zero_of_lt_aux {f : ℕ → ℤ} (m : ℕ) (h : ∀ j < m, f j = 0) :
    finRangeSum f m = 0 := by
  induction m with
  | zero => rfl
  | succ m ih =>
    dsimp [finRangeSum]
    rw [ih (fun j hj => h j (by omega)), h m (by omega), add_zero]

/-- **Theorem 2 (`TASK-TC-054` §3, Exponent Model)**: Prime-power exponent model for square-divisor
    Möbius–Liouville inversion on `k : ℕ`:
    `squareDivisorMoebiusSum k = liouvilleSignFromOmega k` and
    `squareDivisorInverseLiouvilleSum k = primePowerMoebius k`. -/
theorem prime_power_square_divisor_moebius_liouville_inversion_nat :
    ∀ k : ℕ,
      squareDivisorMoebiusSum k = liouvilleSignFromOmega k ∧
      squareDivisorInverseLiouvilleSum k = primePowerMoebius k := by
  intro k
  constructor
  · induction' k using Nat.strong_induction_on with k ih
    rcases k with _ | _ | k'
    · decide
    · decide
    · have h_step : k' + 1 + 1 = k' + 2 := rfl
      rw [h_step]
      dsimp [squareDivisorMoebiusSum]
      have h_ih : squareDivisorMoebiusSum k' = liouvilleSignFromOmega k' :=
        ih k' (by omega)
      have h_pm : primePowerMoebius (k' + 2) = 0 := rfl
      rw [h_pm, zero_add, h_ih]
      dsimp [liouvilleSignFromOmega]
      rw [pow_add]
      norm_num
  · rcases k with _ | _ | k'
    · decide
    · decide
    · have h_step : k' + 1 + 1 = k' + 2 := rfl
      rw [h_step]
      dsimp [squareDivisorInverseLiouvilleSum]
      obtain ⟨r, hr⟩ : ∃ r, (k' + 2) / 2 + 1 = r + 2 := ⟨(k' + 2) / 2 - 1, by omega⟩
      rw [hr, finRangeSum_primePowerMoebius_tail_eq_two (k' + 2)]
      dsimp [finRangeSum, primePowerMoebius]
      have h_sub1 : k' + 2 - 2 = k' := by omega
      rw [h_sub1, pow_add]
      norm_num

/-- **Theorem 3 (`TASK-TC-054R` §8, Actual Arithmetic on `ℕ`)**:
    Connects `natOmega` (`ArithmeticFunction.cardFactors`) to prime-factorization multiplicities
    `n.factorization`, proves additivity `Ω(m n) = Ω(m) + Ω(n)`, and establishes actual Liouville
    multiplicativity `λ(m n) = λ(m) λ(n)`, unit square `λ(d)^2 = 1`, unconstrained common-factor
    cancellation `λ(d r) λ(d s) = λ(r) λ(s)` for all positive integers `m, n, d, r, s`, and
    `liouvilleArith.IsMultiplicative`. -/
theorem actual_omega_factorization_and_liouville_common_factor_cancellation_nat
    {p m n d r s : ℕ} (hp : p.Prime) (k : ℕ)
    (hm : m ≠ 0) (hn : n ≠ 0) (hd : d ≠ 0) (hr : r ≠ 0) (hs : s ≠ 0) :
    (n.factorization.sum fun _ e => e) = natOmega n ∧
    (natOmega 1 = 0 ∧ natOmega p = 1 ∧ natOmega (p ^ k) = k) ∧
    natOmega (m * n) = natOmega m + natOmega n ∧
    (liouvilleLambda 1 = 1 ∧ liouvilleLambda p = -1) ∧
    liouvilleLambda (m * n) = liouvilleLambda m * liouvilleLambda n ∧
    liouvilleLambda d * liouvilleLambda d = 1 ∧
    liouvilleLambda (d * r) * liouvilleLambda (d * s) = liouvilleLambda r * liouvilleLambda s ∧
    liouvilleArith.IsMultiplicative := by
  have h_fact : ∀ x : ℕ, x ≠ 0 → (x.factorization.sum fun _ e => e) = natOmega x := by
    intro x
    induction x using Nat.recOnPosPrimePosCoprime with
    | hp q e hq _ =>
      intro _
      rw [Nat.Prime.factorization_pow hq, Finsupp.sum_single_index rfl, cardFactors_prime_pow_aux hq e]
    | h0 => intro hx; exact absurd rfl hx
    | h1 => intro _; simp [natOmega]
    | h a b ha hb _ iha ihb =>
      intro _
      have ha0 : a ≠ 0 := by omega
      have hb0 : b ≠ 0 := by omega
      rw [Nat.factorization_mul ha0 hb0, Finsupp.sum_add_index' (fun _ => rfl) (fun _ _ _ => rfl)]
      rw [iha ha0, ihb hb0]
      exact (ArithmeticFunction.cardFactors_mul ha0 hb0).symm
  have h_omega_1 : natOmega 1 = 0 := ArithmeticFunction.cardFactors_one
  have h_omega_p : natOmega p = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr hp
  have h_omega_pk : natOmega (p ^ k) = k := cardFactors_prime_pow_aux hp k
  have h_omega_mul : ∀ a b : ℕ, a ≠ 0 → b ≠ 0 → natOmega (a * b) = natOmega a + natOmega b := by
    intro a b ha0 hb0
    exact ArithmeticFunction.cardFactors_mul ha0 hb0
  have h_lam_1 : liouvilleLambda 1 = 1 := by decide
  have h_lam_p : liouvilleLambda p = -1 := by
    simp [liouvilleLambda, hp.ne_zero, h_omega_p, liouvilleSignFromOmega]
  have h_lam_mul_gen : ∀ a b : ℕ, a ≠ 0 → b ≠ 0 →
      liouvilleLambda (a * b) = liouvilleLambda a * liouvilleLambda b := by
    intro a b ha0 hb0
    have hab : a * b ≠ 0 := mul_ne_zero ha0 hb0
    simp [liouvilleLambda, ha0, hb0, hab, h_omega_mul a b ha0 hb0, liouvilleSignFromOmega, pow_add]
  have h_lam_sq_gen : ∀ a : ℕ, a ≠ 0 → liouvilleLambda a * liouvilleLambda a = 1 := by
    intro a ha0
    simp only [liouvilleLambda, ha0, ↓reduceIte, liouvilleSignFromOmega]
    rw [← pow_add]
    have h_even : natOmega a + natOmega a = 2 * natOmega a := by omega
    rw [h_even, pow_mul]
    norm_num
  have h_cancel :
      liouvilleLambda (d * r) * liouvilleLambda (d * s) = liouvilleLambda r * liouvilleLambda s := by
    rw [h_lam_mul_gen d r hd hr, h_lam_mul_gen d s hd hs]
    calc
      (liouvilleLambda d * liouvilleLambda r) * (liouvilleLambda d * liouvilleLambda s) =
        (liouvilleLambda d * liouvilleLambda d) * (liouvilleLambda r * liouvilleLambda s) := by ring
      _ = 1 * (liouvilleLambda r * liouvilleLambda s) := by rw [h_lam_sq_gen d hd]
      _ = liouvilleLambda r * liouvilleLambda s := by ring
  have h_mult : liouvilleArith.IsMultiplicative := by
    refine ⟨by decide, ?_⟩
    intro a b _
    by_cases ha0 : a = 0
    · subst ha0; simp [liouvilleArith, liouvilleLambda]
    · by_cases hb0 : b = 0
      · subst hb0; simp [liouvilleArith, liouvilleLambda]
      · exact h_lam_mul_gen a b ha0 hb0
  exact ⟨h_fact n hn, ⟨h_omega_1, h_omega_p, h_omega_pk⟩, h_omega_mul m n hm hn,
    ⟨h_lam_1, h_lam_p⟩, h_lam_mul_gen m n hm hn, h_lam_sq_gen d hd, h_cancel, h_mult⟩

/-- Helper lemma characterizing membership in `squareDivisors n`. -/
private theorem mem_squareDivisors_iff_aux {n d : ℕ} :
    d ∈ squareDivisors n ↔ (d ∣ n ∧ n ≠ 0) ∧ d ^ 2 ∣ n := by
  simp [squareDivisors, Nat.mem_divisors]

/-- Helper lemma: `Finset.sum` over `Finset.range m` equals `finRangeSum f m`. -/
private theorem sum_range_eq_finRangeSum_aux (f : ℕ → ℤ) (m : ℕ) :
    (∑ j ∈ Finset.range m, f j) = finRangeSum f m := by
  induction m with
  | zero => rfl
  | succ m ih =>
    rw [Finset.sum_range_succ, ih]
    rfl

/-- Helper lemma: explicit characterization of `squareDivisors (p ^ k)` for prime `p`. -/
private theorem squareDivisors_prime_pow_aux {p : ℕ} (hp : p.Prime) (k : ℕ) :
    squareDivisors (p ^ k) =
      (Finset.range (k / 2 + 1)).map ⟨fun j => p ^ j, Nat.pow_right_injective hp.two_le⟩ := by
  ext d
  simp only [squareDivisors, Finset.mem_filter, Nat.divisors_prime_pow hp, Finset.mem_map,
    Finset.mem_range, Function.Embedding.coeFn_mk]
  constructor
  · rintro ⟨⟨j, _, rfl⟩, hdvd⟩
    refine ⟨j, ?_, rfl⟩
    have hpow : p ^ (2 * j) ∣ p ^ k := by
      have hsq : (p ^ j) ^ 2 = p ^ (2 * j) := by ring
      rwa [← hsq]
    have hle : 2 * j ≤ k := (Nat.pow_dvd_pow_iff_le_right hp.one_lt).mp hpow
    omega
  · rintro ⟨j, hj, rfl⟩
    refine ⟨⟨j, by omega, rfl⟩, ?_⟩
    have hsq : (p ^ j) ^ 2 = p ^ (2 * j) := by ring
    rw [hsq]
    exact Nat.pow_dvd_pow p (by omega)

/-- Helper lemma: `(d₁ * d₂).gcd m = d₁` when `m.Coprime n`, `d₁ ∣ m`, and `d₂ ∣ n`. -/
private theorem gcd_mul_left_of_coprime_of_dvd_aux {m n d₁ d₂ : ℕ}
    (cop : m.Coprime n) (hd₁ : d₁ ∣ m) (hd₂ : d₂ ∣ n) :
    (d₁ * d₂).gcd m = d₁ := by
  obtain ⟨k₁, rfl⟩ := hd₁
  rw [Nat.gcd_mul_left]
  have hcop : d₂.Coprime k₁ :=
    ((cop.coprime_mul_left).coprime_dvd_right hd₂).symm
  rw [hcop.gcd_eq_one, mul_one]

/-- Helper lemma: multiplicative factorization of sums over `squareDivisors (m * n)` for coprime `m, n`. -/
private theorem sum_squareDivisors_mul_of_coprime_aux {m n : ℕ} (cop : m.Coprime n)
    (F : ℕ → ℕ → ℤ)
    (hF : ∀ d₁ ∈ squareDivisors m, ∀ d₂ ∈ squareDivisors n,
      F (m * n) (d₁ * d₂) = F m d₁ * F n d₂) :
    (∑ d ∈ squareDivisors (m * n), F (m * n) d) =
      (∑ d₁ ∈ squareDivisors m, F m d₁) * (∑ d₂ ∈ squareDivisors n, F n d₂) := by
  rw [Finset.sum_mul_sum, ← Finset.sum_product']
  symm
  refine Finset.sum_nbij (fun x : ℕ × ℕ => x.1 * x.2) ?_ ?_ ?_ ?_
  · rintro ⟨d₁, d₂⟩ hmem
    rw [Finset.mem_product, mem_squareDivisors_iff_aux, mem_squareDivisors_iff_aux] at hmem
    rcases hmem with ⟨⟨⟨hd₁, hm⟩, hd₁sq⟩, ⟨⟨hd₂, hn⟩, hd₂sq⟩⟩
    rw [mem_squareDivisors_iff_aux]
    refine ⟨⟨mul_dvd_mul hd₁ hd₂, mul_ne_zero hm hn⟩, ?_⟩
    rw [mul_pow]
    exact mul_dvd_mul hd₁sq hd₂sq
  · rintro ⟨a₁, a₂⟩ ha ⟨b₁, b₂⟩ hb heq
    rw [Finset.mem_coe, Finset.mem_product, mem_squareDivisors_iff_aux, mem_squareDivisors_iff_aux] at ha hb
    rcases ha with ⟨⟨⟨ha₁, _⟩, _⟩, ⟨⟨ha₂, _⟩, _⟩⟩
    rcases hb with ⟨⟨⟨hb₁, _⟩, _⟩, ⟨⟨hb₂, _⟩, _⟩⟩
    dsimp at heq
    have h1 : a₁ = b₁ := by
      calc
        a₁ = (a₁ * a₂).gcd m := (gcd_mul_left_of_coprime_of_dvd_aux cop ha₁ ha₂).symm
        _ = (b₁ * b₂).gcd m := by rw [heq]
        _ = b₁ := gcd_mul_left_of_coprime_of_dvd_aux cop hb₁ hb₂
    have h2 : a₂ = b₂ := by
      have ha_comm : a₂ * a₁ = b₂ * b₁ := by linarith
      calc
        a₂ = (a₂ * a₁).gcd n := (gcd_mul_left_of_coprime_of_dvd_aux cop.symm ha₂ ha₁).symm
        _ = (b₂ * b₁).gcd n := by rw [ha_comm]
        _ = b₂ := gcd_mul_left_of_coprime_of_dvd_aux cop.symm hb₂ hb₁
    exact Prod.ext h1 h2
  · intro d hd
    rw [Finset.mem_coe, mem_squareDivisors_iff_aux] at hd
    rcases hd with ⟨⟨hd_dvd, hmn⟩, hd_sq⟩
    have hm : m ≠ 0 := left_ne_zero_of_mul hmn
    have hn : n ≠ 0 := right_ne_zero_of_mul hmn
    refine ⟨(d.gcd m, d.gcd n), ?_, ?_⟩
    · rw [Finset.mem_coe, Finset.mem_product, mem_squareDivisors_iff_aux, mem_squareDivisors_iff_aux]
      have hd₁_m : d.gcd m ∣ m := Nat.gcd_dvd_right d m
      have hd₂_n : d.gcd n ∣ n := Nat.gcd_dvd_right d n
      have hd₁_d : d.gcd m ∣ d := Nat.gcd_dvd_left d m
      have hd₂_d : d.gcd n ∣ d := Nat.gcd_dvd_left d n
      have hd₁_sq_mn : (d.gcd m) ^ 2 ∣ m * n :=
        dvd_trans (pow_dvd_pow_of_dvd hd₁_d 2) hd_sq
      have hd₂_sq_nm : (d.gcd n) ^ 2 ∣ n * m := by
        rw [mul_comm]
        exact dvd_trans (pow_dvd_pow_of_dvd hd₂_d 2) hd_sq
      have hcop₁ : ((d.gcd m) ^ 2).Coprime n :=
        (cop.coprime_dvd_left hd₁_m).pow_left 2
      have hcop₂ : ((d.gcd n) ^ 2).Coprime m :=
        (cop.symm.coprime_dvd_left hd₂_n).pow_left 2
      exact ⟨⟨⟨hd₁_m, hm⟩, hcop₁.dvd_of_dvd_mul_right hd₁_sq_mn⟩,
        ⟨⟨hd₂_n, hn⟩, hcop₂.dvd_of_dvd_mul_right hd₂_sq_nm⟩⟩
    · dsimp
      rw [← cop.gcd_mul d, Nat.gcd_eq_left hd_dvd]
  · rintro ⟨d₁, d₂⟩ hmem
    rw [Finset.mem_product] at hmem
    exact (hF d₁ hmem.1 d₂ hmem.2).symm

/-- **Theorem 4 (`TASK-TC-054R` §8 & `TASK-TC-054R2` §5, Unconditional Flat Square-Divisor Sums on `ℕ`)**:
    Connects `primePowerMoebius` and `liouvilleSignFromOmega` to Mathlib's `ArithmeticFunction.moebius` (`μ`)
    and `liouvilleLambda` (`λ`), proves the actual prime-power square-divisor identities
    `∑_{0 ≤ j ≤ k/2} μ(p^{k - 2j}) = λ(p^k)` and `∑_{0 ≤ j ≤ k/2} μ(p^j) λ(p^{k - 2j}) = μ(p^k)`,
    proves the factored prime-power product identities for `λ(n)` and `μ(n)` over `n.factorization.prod`
    for all positive integers `n ≠ 0`, and unconditionally proves that the explicit flat square-divisor sums
    `actualFlatMoebiusSquareDivisorSum n = ∑_{d^2 ∣ n} μ(n / d^2)` and
    `actualFlatInverseLiouvilleSquareDivisorSum n = ∑_{d^2 ∣ n} μ(d) λ(n / d^2)`
    are multiplicative (`IsMultiplicative`), agree with the prime-power sums on `p ^ k`, and satisfy
    `actualFlatMoebiusSquareDivisorSum n = liouvilleLambda n` and
    `actualFlatInverseLiouvilleSquareDivisorSum n = ArithmeticFunction.moebius n` for all `n : ℕ`. -/
theorem actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat
    {p n : ℕ} (hp : p.Prime) (k : ℕ) (hn : n ≠ 0) :
    (ArithmeticFunction.moebius (p ^ k) = primePowerMoebius k ∧
      liouvilleLambda (p ^ k) = liouvilleSignFromOmega k) ∧
    (primePowerActualMoebiusSquareSum p k = liouvilleLambda (p ^ k) ∧
      primePowerActualInverseLiouvilleSquareSum p k = ArithmeticFunction.moebius (p ^ k)) ∧
    (liouvilleLambda n = n.factorization.prod (fun q e => primePowerActualMoebiusSquareSum q e) ∧
      ArithmeticFunction.moebius n = n.factorization.prod (fun q e => primePowerActualInverseLiouvilleSquareSum q e)) ∧
    (actualFlatMoebiusSquareArith.IsMultiplicative ∧
      actualFlatInverseLiouvilleSquareArith.IsMultiplicative ∧
      actualFlatMoebiusSquareDivisorSum (p ^ k) = primePowerActualMoebiusSquareSum p k ∧
      actualFlatInverseLiouvilleSquareDivisorSum (p ^ k) = primePowerActualInverseLiouvilleSquareSum p k ∧
      actualFlatMoebiusSquareDivisorSum n = liouvilleLambda n ∧
      actualFlatInverseLiouvilleSquareDivisorSum n = ArithmeticFunction.moebius n) := by
  have h_fwd_pp : ∀ q e : ℕ, q.Prime → primePowerActualMoebiusSquareSum q e = liouvilleLambda (q ^ e) := by
    intro q e hq
    dsimp [primePowerActualMoebiusSquareSum]
    rw [finRangeSum_congr_aux (e / 2 + 1) (fun j _ => moebius_apply_prime_pow_eq_primePowerMoebius_aux hq (e - 2 * j))]
    dsimp [finRangeSum]
    have h_zero : finRangeSum (fun j => primePowerMoebius (e - 2 * j)) (e / 2) = 0 := by
      apply finRangeSum_eq_zero_of_lt_aux
      intro j hj
      obtain ⟨d, hd⟩ : ∃ d, e - 2 * j = d + 2 := ⟨e - 2 * j - 2, by omega⟩
      rw [hd]
      rfl
    rw [h_zero, zero_add, liouvilleLambda_prime_pow_aux hq e]
    rcases Nat.mod_two_eq_zero_or_one e with h_even | h_odd
    · have h_rem : e - 2 * (e / 2) = 0 := by omega
      obtain ⟨m, hm⟩ : ∃ m, e = 2 * m := ⟨e / 2, by omega⟩
      rw [h_rem, hm]
      dsimp [primePowerMoebius, liouvilleSignFromOmega]
      rw [pow_mul]
      norm_num
    · have h_rem : e - 2 * (e / 2) = 1 := by omega
      obtain ⟨m, hm⟩ : ∃ m, e = 2 * m + 1 := ⟨e / 2, by omega⟩
      rw [h_rem, hm]
      dsimp [primePowerMoebius, liouvilleSignFromOmega]
      rw [pow_add, pow_mul]
      norm_num
  have h_inv_pp : ∀ q e : ℕ, q.Prime → primePowerActualInverseLiouvilleSquareSum q e = ArithmeticFunction.moebius (q ^ e) := by
    intro q e hq
    have h_eq : primePowerActualInverseLiouvilleSquareSum q e = squareDivisorInverseLiouvilleSum e := by
      dsimp [primePowerActualInverseLiouvilleSquareSum, squareDivisorInverseLiouvilleSum]
      apply finRangeSum_congr_aux
      intro j _
      rw [moebius_apply_prime_pow_eq_primePowerMoebius_aux hq j, liouvilleLambda_prime_pow_aux hq (e - 2 * j)]
      rfl
    rw [h_eq, (prime_power_square_divisor_moebius_liouville_inversion_nat e).2,
      moebius_apply_prime_pow_eq_primePowerMoebius_aux hq e]
  have h_mult_lam : liouvilleArith.IsMultiplicative := by
    refine ⟨by decide, ?_⟩
    intro a b _
    by_cases ha0 : a = 0
    · subst ha0; simp [liouvilleArith, liouvilleLambda]
    · by_cases hb0 : b = 0
      · subst hb0; simp [liouvilleArith, liouvilleLambda]
      · have hab : a * b ≠ 0 := mul_ne_zero ha0 hb0
        simp [liouvilleArith, liouvilleLambda, ha0, hb0, hab, natOmega,
          ArithmeticFunction.cardFactors_mul ha0 hb0, liouvilleSignFromOmega, pow_add]
  have h_prod_lam : liouvilleLambda n = n.factorization.prod (fun q e => primePowerActualMoebiusSquareSum q e) := by
    change liouvilleArith n = _
    rw [ArithmeticFunction.IsMultiplicative.multiplicative_factorization liouvilleArith h_mult_lam hn]
    unfold Finsupp.prod
    apply Finset.prod_congr rfl
    intro q hq
    have hq_prime : q.Prime := by
      rw [Nat.support_factorization] at hq
      exact Nat.prime_of_mem_primeFactors hq
    exact (h_fwd_pp q (n.factorization q) hq_prime).symm
  have h_prod_mu : ArithmeticFunction.moebius n = n.factorization.prod (fun q e => primePowerActualInverseLiouvilleSquareSum q e) := by
    rw [ArithmeticFunction.IsMultiplicative.multiplicative_factorization ArithmeticFunction.moebius ArithmeticFunction.isMultiplicative_moebius hn]
    unfold Finsupp.prod
    apply Finset.prod_congr rfl
    intro q hq
    have hq_prime : q.Prime := by
      rw [Nat.support_factorization] at hq
      exact Nat.prime_of_mem_primeFactors hq
    exact (h_inv_pp q (n.factorization q) hq_prime).symm
  have h_flat_fwd_mult : actualFlatMoebiusSquareArith.IsMultiplicative := by
    refine ⟨by decide, ?_⟩
    intro a b cop
    change actualFlatMoebiusSquareDivisorSum (a * b) =
      actualFlatMoebiusSquareDivisorSum a * actualFlatMoebiusSquareDivisorSum b
    dsimp [actualFlatMoebiusSquareDivisorSum]
    apply sum_squareDivisors_mul_of_coprime_aux cop (fun m d => ArithmeticFunction.moebius (m / d ^ 2))
    intro d₁ hd₁ d₂ hd₂
    rw [mem_squareDivisors_iff_aux] at hd₁ hd₂
    have h_div : (a * b) / (d₁ * d₂) ^ 2 = (a / d₁ ^ 2) * (b / d₂ ^ 2) := by
      rw [mul_pow, Nat.div_mul_div_comm hd₁.2 hd₂.2]
    have h_cop_quot : (a / d₁ ^ 2).Coprime (b / d₂ ^ 2) :=
      (cop.coprime_dvd_left (Nat.div_dvd_of_dvd hd₁.2)).coprime_dvd_right (Nat.div_dvd_of_dvd hd₂.2)
    rw [h_div, ArithmeticFunction.isMultiplicative_moebius.2 h_cop_quot]
  have h_flat_inv_mult : actualFlatInverseLiouvilleSquareArith.IsMultiplicative := by
    refine ⟨by decide, ?_⟩
    intro a b cop
    change actualFlatInverseLiouvilleSquareDivisorSum (a * b) =
      actualFlatInverseLiouvilleSquareDivisorSum a * actualFlatInverseLiouvilleSquareDivisorSum b
    dsimp [actualFlatInverseLiouvilleSquareDivisorSum]
    apply sum_squareDivisors_mul_of_coprime_aux cop
      (fun m d => ArithmeticFunction.moebius d * liouvilleLambda (m / d ^ 2))
    intro d₁ hd₁ d₂ hd₂
    rw [mem_squareDivisors_iff_aux] at hd₁ hd₂
    have h_div : (a * b) / (d₁ * d₂) ^ 2 = (a / d₁ ^ 2) * (b / d₂ ^ 2) := by
      rw [mul_pow, Nat.div_mul_div_comm hd₁.2 hd₂.2]
    have h_cop_d : d₁.Coprime d₂ :=
      (cop.coprime_dvd_left hd₁.1.1).coprime_dvd_right hd₂.1.1
    have h_cop_quot : (a / d₁ ^ 2).Coprime (b / d₂ ^ 2) :=
      (cop.coprime_dvd_left (Nat.div_dvd_of_dvd hd₁.2)).coprime_dvd_right (Nat.div_dvd_of_dvd hd₂.2)
    have h_mu_mul : ArithmeticFunction.moebius (d₁ * d₂) =
        ArithmeticFunction.moebius d₁ * ArithmeticFunction.moebius d₂ :=
      ArithmeticFunction.isMultiplicative_moebius.2 h_cop_d
    have h_lam_mul : liouvilleLambda ((a / d₁ ^ 2) * (b / d₂ ^ 2)) =
        liouvilleLambda (a / d₁ ^ 2) * liouvilleLambda (b / d₂ ^ 2) :=
      h_mult_lam.2 h_cop_quot
    rw [h_div, h_mu_mul, h_lam_mul]
    ring
  have h_flat_fwd_pp : ∀ q e : ℕ, q.Prime →
      actualFlatMoebiusSquareDivisorSum (q ^ e) = primePowerActualMoebiusSquareSum q e := by
    intro q e hq
    dsimp [actualFlatMoebiusSquareDivisorSum, primePowerActualMoebiusSquareSum]
    rw [squareDivisors_prime_pow_aux hq e, Finset.sum_map, ← sum_range_eq_finRangeSum_aux]
    apply Finset.sum_congr rfl
    intro j hj
    rw [Finset.mem_range] at hj
    have hsq : (q ^ j) ^ 2 = q ^ (2 * j) := by ring
    rw [Function.Embedding.coeFn_mk, hsq, Nat.pow_div (by omega) hq.pos]
  have h_flat_inv_pp : ∀ q e : ℕ, q.Prime →
      actualFlatInverseLiouvilleSquareDivisorSum (q ^ e) = primePowerActualInverseLiouvilleSquareSum q e := by
    intro q e hq
    dsimp [actualFlatInverseLiouvilleSquareDivisorSum, primePowerActualInverseLiouvilleSquareSum]
    rw [squareDivisors_prime_pow_aux hq e, Finset.sum_map, ← sum_range_eq_finRangeSum_aux]
    apply Finset.sum_congr rfl
    intro j hj
    rw [Finset.mem_range] at hj
    have hsq : (q ^ j) ^ 2 = q ^ (2 * j) := by ring
    rw [Function.Embedding.coeFn_mk, hsq, Nat.pow_div (by omega) hq.pos]
  have h_flat_fwd_eq_fn : actualFlatMoebiusSquareArith = liouvilleArith := by
    rw [ArithmeticFunction.IsMultiplicative.eq_iff_eq_on_prime_powers
      actualFlatMoebiusSquareArith h_flat_fwd_mult liouvilleArith h_mult_lam]
    intro q e hq
    change actualFlatMoebiusSquareDivisorSum (q ^ e) = liouvilleLambda (q ^ e)
    rw [h_flat_fwd_pp q e hq, h_fwd_pp q e hq]
  have h_flat_inv_eq_fn : actualFlatInverseLiouvilleSquareArith = ArithmeticFunction.moebius := by
    rw [ArithmeticFunction.IsMultiplicative.eq_iff_eq_on_prime_powers
      actualFlatInverseLiouvilleSquareArith h_flat_inv_mult
      ArithmeticFunction.moebius ArithmeticFunction.isMultiplicative_moebius]
    intro q e hq
    change actualFlatInverseLiouvilleSquareDivisorSum (q ^ e) = ArithmeticFunction.moebius (q ^ e)
    rw [h_flat_inv_pp q e hq, h_inv_pp q e hq]
  have h_flat_fwd_n : actualFlatMoebiusSquareDivisorSum n = liouvilleLambda n :=
    congrFun (congrArg DFunLike.coe h_flat_fwd_eq_fn) n
  have h_flat_inv_n : actualFlatInverseLiouvilleSquareDivisorSum n = ArithmeticFunction.moebius n :=
    congrFun (congrArg DFunLike.coe h_flat_inv_eq_fn) n
  exact ⟨⟨moebius_apply_prime_pow_eq_primePowerMoebius_aux hp k, liouvilleLambda_prime_pow_aux hp k⟩,
    ⟨h_fwd_pp p k hp, h_inv_pp p k hp⟩, ⟨h_prod_lam, h_prod_mu⟩,
    ⟨h_flat_fwd_mult, h_flat_inv_mult, h_flat_fwd_pp p k hp, h_flat_inv_pp p k hp,
      h_flat_fwd_n, h_flat_inv_n⟩⟩

/-- **Theorem 5 (`TASK-TC-054` §3, Scalar Real-Inequality Lemma)**:
    Scalar real-inequality implications for positive-weight norm multipliers (`eta > 0`) and
    geometric block summation under explicit real hypotheses (Minkowski integral inequality and
    multiplicative change of variables are proved analytically outside Lean). -/
theorem reversible_weighted_dilation_norm_and_grade_interval_equivalence
    (norm_f_sq d_pow_neg_4eta norm_f_d2_sq
      norm_lambda norm_mu zeta_1_2eta zeta_2_4eta B_mu B_lam
      int_0_1 sum_tau_blocks Z3_sq eta C_eta tau_pow_neg_eta : ℝ)
    (h_dil : norm_f_d2_sq = d_pow_neg_4eta * norm_f_sq)
    (h_z1_pos : 0 < zeta_1_2eta)
    (h_z2_pos : 0 < zeta_2_4eta)
    (h_fwd : norm_lambda ≤ zeta_1_2eta * norm_mu)
    (h_rev : norm_mu ≤ (zeta_1_2eta / zeta_2_4eta) * norm_lambda)
    (h_01 : int_0_1 ≤ Z3_sq / (5 - 2 * eta))
    (h_blocks : sum_tau_blocks ≤ C_eta / (1 - tau_pow_neg_eta)) :
    norm_f_d2_sq = d_pow_neg_4eta * norm_f_sq ∧
    (norm_mu ≤ B_mu → norm_lambda ≤ zeta_1_2eta * B_mu) ∧
    (norm_lambda ≤ B_lam → norm_mu ≤ (zeta_1_2eta / zeta_2_4eta) * B_lam) ∧
    int_0_1 + sum_tau_blocks ≤ Z3_sq / (5 - 2 * eta) + C_eta / (1 - tau_pow_neg_eta) := by
  refine ⟨h_dil, ?_, ?_, by linarith⟩
  · intro hBmu
    have h_mul : zeta_1_2eta * norm_mu ≤ zeta_1_2eta * B_mu :=
      mul_le_mul_of_nonneg_left hBmu (le_of_lt h_z1_pos)
    linarith
  · intro hBlam
    have h_quot_pos : 0 ≤ zeta_1_2eta / zeta_2_4eta :=
      div_nonneg (le_of_lt h_z1_pos) (le_of_lt h_z2_pos)
    have h_mul :
        (zeta_1_2eta / zeta_2_4eta) * norm_lambda ≤
          (zeta_1_2eta / zeta_2_4eta) * B_lam :=
      mul_le_mul_of_nonneg_left hBlam h_quot_pos
    linarith

/-- **Theorem 6 (`TASK-TC-054` §4, Scalar Real-Algebra Lemma)**:
    Euler–Maclaurin `N = 2` inflection-root antiderivative combination
    `C_2 = (f'(v_-) - f'(v_+)) / 6` and subtransition growing-range exponent algebra
    `(N + 1)(1 - delta) - N = 1 - (N + 1) * delta < 0 ↔ 1 < (N + 1) * delta`. -/
theorem euler_maclaurin_c2_and_subtransition_growing_range_exponent
    (f_prime_v_minus f_prime_v_plus N delta : ℝ)
    (h_v_minus_nonneg : 0 ≤ f_prime_v_minus)
    (h_v_plus_nonpos : f_prime_v_plus ≤ 0) :
    (1 / 12 : ℝ) * (|f_prime_v_minus| + |f_prime_v_plus - f_prime_v_minus| + |-f_prime_v_plus|) =
      (f_prime_v_minus - f_prime_v_plus) / 6 ∧
    ((N + 1) * (1 - delta) - N = 1 - (N + 1) * delta ∧
      (1 - (N + 1) * delta < 0 ↔ 1 < (N + 1) * delta)) := by
  refine ⟨?_, ?_⟩
  · have h_abs1 : |f_prime_v_minus| = f_prime_v_minus := abs_of_nonneg h_v_minus_nonneg
    have h_diff_nonpos : f_prime_v_plus - f_prime_v_minus ≤ 0 := by linarith
    have h_abs2 : |f_prime_v_plus - f_prime_v_minus| = -(f_prime_v_plus - f_prime_v_minus) :=
      abs_of_nonpos h_diff_nonpos
    have h_neg_nonneg : 0 ≤ -f_prime_v_plus := by linarith
    have h_abs3 : |-f_prime_v_plus| = -f_prime_v_plus := abs_of_nonneg h_neg_nonneg
    rw [h_abs1, h_abs2, h_abs3]
    ring
  · refine ⟨by ring, ?_⟩
    constructor <;> intro h <;> linarith

/-- **Theorem 7 (`TASK-TC-054` §6B, Scalar Real-Algebra Lemma)**:
    Pointwise dyadic parity square identity and off-critical mode lower bound `0 < 1 - 2^{-x} <= |1 + 2^{-rho}|`. -/
theorem dyadic_parity_energy_and_off_critical_mode_nonvanishing
    (Q_X Q_half_X sqrt2 two_pow_neg_x abs_one_plus_two_pow_neg_rho : ℝ)
    (h_sqrt2 : sqrt2 ^ 2 = 2)
    (h_sqrt2_ne : sqrt2 ≠ 0)
    (h_x_lt_one : two_pow_neg_x < 1)
    (h_rev_tri : 1 - two_pow_neg_x ≤ abs_one_plus_two_pow_neg_rho) :
    (Q_X + (1 / sqrt2) * Q_half_X) ^ 2 =
      Q_X ^ 2 + (1 / 2 : ℝ) * Q_half_X ^ 2 + sqrt2 * Q_X * Q_half_X ∧
    (0 < 1 - two_pow_neg_x ∧ 0 < abs_one_plus_two_pow_neg_rho) := by
  constructor
  · field_simp [h_sqrt2_ne]
    calc
      (Q_X * sqrt2 + Q_half_X) ^ 2 * 2 =
          ((sqrt2 ^ 2) * Q_X ^ 2 + Q_half_X ^ 2 + 2 * sqrt2 * Q_X * Q_half_X) * 2 := by ring
      _ = (2 * Q_X ^ 2 + Q_half_X ^ 2 + 2 * sqrt2 * Q_X * Q_half_X) * 2 := by rw [h_sqrt2]
      _ = (Q_X ^ 2 * 2 + Q_half_X ^ 2 + sqrt2 * Q_X * Q_half_X * 2) * sqrt2 ^ 2 := by
        rw [h_sqrt2]
        ring
  · refine ⟨by linarith, by linarith⟩

/-- Helper lemma: `6 * ∑_{0 ≤ r < n} r^2 = (n - 1) * n * (2 * n - 1)`. -/
private theorem sum_range_sq_mul_six_aux (n : ℕ) :
    6 * (∑ r ∈ Finset.range n, r ^ 2) = (n - 1) * n * (2 * n - 1) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [Finset.sum_range_succ, mul_add, ih]
    rcases n with _ | m
    · rfl
    · simp only [Nat.add_sub_cancel]
      have h1 : 2 * (m + 1) - 1 = 2 * m + 1 := by omega
      have h2 : 2 * (m + 1 + 1) - 1 = 2 * m + 3 := by omega
      rw [h1, h2]
      ring

/-- **Theorem 8 (`TASK-TC-054R` §§2, 4, 6 & `TASK-TC-054R2` §5, Endpoint Antiderivative, Denominator Monotonicity,
    Exact Dyadic Block Square Sum, and Reciprocal-Cube Bound Algebra)**:
    1. Global Stieltjes variation endpoint antiderivative combination:
       `(1 / 2) * ((2 * (3 / 2) - 1) * e_neg_3_2 - (2 * 0 - 1)) + (1 / 2) * (0 - (-(2 * (3 / 2) - 1) * e_neg_3_2)) = 1 / 2 + 2 * e_neg_3_2`;
    2. Fourier residue tail denominator monotonicity: for `1 ≤ K` and `K + 1 ≤ m`,
       `0 < (K - 1 / 2) * (2 * K + 3) * (2 * K + 4) ≤ (m - 3 / 2) * (2 * m + 1) * (2 * m + 2)` and
       `0 < (K + 2) * (2 * K + 8) * (2 * K + 9) ≤ (m + 1) * (2 * m + 6) * (2 * m + 7)`;
    3. Exact dyadic block square sum on `Finset.Ico A (2 * A)` (`1 ≤ A`) and upper bound:
       `6 * (∑ r ∈ Finset.Ico A (2 * A), r ^ 2) + (A - 1) * A * (2 * A - 1) = (2 * A - 1) * (2 * A) * (4 * A - 1)`,
       `6 * (∑ r ∈ Finset.Ico A (2 * A), r ^ 2) + 9 * A ^ 2 = 14 * A ^ 3 + A`, and
       `3 * (∑ r ∈ Finset.Ico A (2 * A), r ^ 2) < 7 * A ^ 3`;
    4. Unequal-block `s^{-3}` sum bound algebra: for `2 ≤ B`,
       `1 / B ^ 3 + 1 / (2 * B ^ 2) ≤ 1 / B ^ 2`. -/
theorem abel_scaling_fourier_ratio_and_unequal_block_algebra
    (e_neg_3_2 K m B : ℝ) (A : ℕ)
    (hK : 1 ≤ K)
    (hm : K + 1 ≤ m)
    (hB : 2 ≤ B)
    (hA : 1 ≤ A) :
    ((1 / 2 : ℝ) * ((2 * (3 / 2 : ℝ) - 1) * e_neg_3_2 - (2 * 0 - 1)) +
      (1 / 2 : ℝ) * (0 - (-(2 * (3 / 2 : ℝ) - 1) * e_neg_3_2)) =
        (1 / 2 : ℝ) + 2 * e_neg_3_2) ∧
    (0 < (K - 1 / 2) * (2 * K + 3) * (2 * K + 4) ∧
      (K - 1 / 2) * (2 * K + 3) * (2 * K + 4) ≤ (m - 3 / 2) * (2 * m + 1) * (2 * m + 2) ∧
      0 < (K + 2) * (2 * K + 8) * (2 * K + 9) ∧
      (K + 2) * (2 * K + 8) * (2 * K + 9) ≤ (m + 1) * (2 * m + 6) * (2 * m + 7)) ∧
    (6 * (∑ r ∈ Finset.Ico A (2 * A), r ^ 2) + (A - 1) * A * (2 * A - 1) =
        (2 * A - 1) * (2 * A) * (4 * A - 1) ∧
      6 * (∑ r ∈ Finset.Ico A (2 * A), r ^ 2) + 9 * A ^ 2 = 14 * A ^ 3 + A ∧
      3 * (∑ r ∈ Finset.Ico A (2 * A), r ^ 2) < 7 * A ^ 3) ∧
    (1 / B ^ 3 + 1 / (2 * B ^ 2) ≤ 1 / B ^ 2) := by
  refine ⟨by ring, ?_, ?_, ?_⟩
  · have h1_pos : 0 < K - 1 / 2 := by linarith
    have h2_pos : 0 < 2 * K + 3 := by linarith
    have h3_pos : 0 < 2 * K + 4 := by linarith
    have h_pos : 0 < (K - 1 / 2) * (2 * K + 3) * (2 * K + 4) :=
      mul_pos (mul_pos h1_pos h2_pos) h3_pos
    have h1_le : K - 1 / 2 ≤ m - 3 / 2 := by linarith
    have h2_le : 2 * K + 3 ≤ 2 * m + 1 := by linarith
    have h3_le : 2 * K + 4 ≤ 2 * m + 2 := by linarith
    have h12_le : (K - 1 / 2) * (2 * K + 3) ≤ (m - 3 / 2) * (2 * m + 1) :=
      mul_le_mul h1_le h2_le (le_of_lt h2_pos) (by linarith)
    have h123_le :
        (K - 1 / 2) * (2 * K + 3) * (2 * K + 4) ≤
          (m - 3 / 2) * (2 * m + 1) * (2 * m + 2) :=
      mul_le_mul h12_le h3_le (le_of_lt h3_pos) (mul_nonneg (by linarith) (by linarith))
    have ho1_pos : 0 < K + 2 := by linarith
    have ho2_pos : 0 < 2 * K + 8 := by linarith
    have ho3_pos : 0 < 2 * K + 9 := by linarith
    have ho_pos : 0 < (K + 2) * (2 * K + 8) * (2 * K + 9) :=
      mul_pos (mul_pos ho1_pos ho2_pos) ho3_pos
    have ho1_le : K + 2 ≤ m + 1 := by linarith
    have ho2_le : 2 * K + 8 ≤ 2 * m + 6 := by linarith
    have ho3_le : 2 * K + 9 ≤ 2 * m + 7 := by linarith
    have ho12_le : (K + 2) * (2 * K + 8) ≤ (m + 1) * (2 * m + 6) :=
      mul_le_mul ho1_le ho2_le (le_of_lt ho2_pos) (by linarith)
    have ho123_le :
        (K + 2) * (2 * K + 8) * (2 * K + 9) ≤
          (m + 1) * (2 * m + 6) * (2 * m + 7) :=
      mul_le_mul ho12_le ho3_le (le_of_lt ho3_pos) (mul_nonneg (by linarith) (by linarith))
    exact ⟨h_pos, h123_le, ho_pos, ho123_le⟩
  · have hle : A ≤ 2 * A := by omega
    have hsplit := Finset.sum_range_add_sum_Ico (fun r => r ^ 2) hle
    have h6_split :
        6 * (∑ r ∈ Finset.range A, r ^ 2) + 6 * (∑ r ∈ Finset.Ico A (2 * A), r ^ 2) =
          6 * (∑ r ∈ Finset.range (2 * A), r ^ 2) := by
      rw [← mul_add, hsplit]
    have h6A := sum_range_sq_mul_six_aux A
    have h6_2A := sum_range_sq_mul_six_aux (2 * A)
    have h4A : 2 * (2 * A) - 1 = 4 * A - 1 := by omega
    rw [h4A] at h6_2A
    have h_diff_eq :
        6 * (∑ r ∈ Finset.Ico A (2 * A), r ^ 2) + (A - 1) * A * (2 * A - 1) =
          (2 * A - 1) * (2 * A) * (4 * A - 1) := by
      linarith
    obtain ⟨d, hd⟩ : ∃ d, A = d + 1 := ⟨A - 1, by omega⟩
    have h_poly :
        (2 * A - 1) * (2 * A) * (4 * A - 1) + 9 * A ^ 2 =
          (A - 1) * A * (2 * A - 1) + (14 * A ^ 3 + A) := by
      subst hd
      simp only [Nat.add_sub_cancel]
      have h1 : 2 * (d + 1) - 1 = 2 * d + 1 := by omega
      have h2 : 4 * (d + 1) - 1 = 4 * d + 3 := by omega
      rw [h1, h2]
      ring
    have h_expanded :
        6 * (∑ r ∈ Finset.Ico A (2 * A), r ^ 2) + 9 * A ^ 2 = 14 * A ^ 3 + A := by
      omega
    have h_A_le_A2 : A ≤ A ^ 2 := by
      rw [sq]
      exact Nat.le_mul_self A
    have h_strict : 3 * (∑ r ∈ Finset.Ico A (2 * A), r ^ 2) < 7 * A ^ 3 := by
      omega
    exact ⟨h_diff_eq, h_expanded, h_strict⟩
  · have hB_pos : 0 < B := by linarith
    have h_diff : 1 / B ^ 2 - (1 / B ^ 3 + 1 / (2 * B ^ 2)) = (B - 2) / (2 * B ^ 3) := by
      field_simp [ne_of_gt hB_pos]
      ring
    have h_nonneg : 0 ≤ (B - 2) / (2 * B ^ 3) :=
      div_nonneg (by linarith) (by positivity)
    linarith

/-- Helper lemma: `liouvilleLambda (a * b) = liouvilleLambda a * liouvilleLambda b` for `a ≠ 0`, `b ≠ 0`. -/
private theorem liouvilleLambda_mul_aux {a b : ℕ} (ha : a ≠ 0) (hb : b ≠ 0) :
    liouvilleLambda (a * b) = liouvilleLambda a * liouvilleLambda b := by
  have hab : a * b ≠ 0 := mul_ne_zero ha hb
  simp [liouvilleLambda, ha, hb, hab, natOmega, ArithmeticFunction.cardFactors_mul ha hb,
    liouvilleSignFromOmega, pow_add]

/-- Helper lemma: `liouvilleLambda d * liouvilleLambda d = 1` for `d ≠ 0`. -/
private theorem liouvilleLambda_sq_aux {d : ℕ} (hd : d ≠ 0) :
    liouvilleLambda d * liouvilleLambda d = 1 := by
  simp only [liouvilleLambda, hd, ↓reduceIte, liouvilleSignFromOmega]
  rw [← pow_add]
  have h_even : natOmega d + natOmega d = 2 * natOmega d := by omega
  rw [h_even, pow_mul]
  norm_num

/-- Helper lemma: for `d ∣ n` with `n ≠ 0`, `liouvilleLambda (n / d) = liouvilleLambda n * liouvilleLambda d`. -/
private theorem liouvilleLambda_div_of_dvd_aux {n d : ℕ} (hn : n ≠ 0) (hdvd : d ∣ n) :
    liouvilleLambda (n / d) = liouvilleLambda n * liouvilleLambda d := by
  have hd : d ≠ 0 := ne_zero_of_dvd_ne_zero hn hdvd
  have hq : n / d ≠ 0 := (Nat.div_ne_zero_iff hd).mpr (Nat.le_of_dvd (Nat.pos_of_ne_zero hn) hdvd)
  have hmul : d * (n / d) = n := Nat.mul_div_cancel' hdvd
  have h1 : liouvilleLambda n = liouvilleLambda d * liouvilleLambda (n / d) := by
    calc
      liouvilleLambda n = liouvilleLambda (d * (n / d)) := by rw [hmul]
      _ = liouvilleLambda d * liouvilleLambda (n / d) := liouvilleLambda_mul_aux hd hq
  calc
    liouvilleLambda (n / d) = 1 * liouvilleLambda (n / d) := by ring
    _ = (liouvilleLambda d * liouvilleLambda d) * liouvilleLambda (n / d) := by
      rw [liouvilleLambda_sq_aux hd]
    _ = (liouvilleLambda d * liouvilleLambda (n / d)) * liouvilleLambda d := by ring
    _ = liouvilleLambda n * liouvilleLambda d := by rw [← h1]

/-- Helper lemma: `(ArithmeticFunction.moebius d) ^ 2 * liouvilleLambda d = ArithmeticFunction.moebius d` for all `d : ℕ`. -/
private theorem moebius_sq_mul_liouvilleLambda_eq_moebius_aux (d : ℕ) :
    (ArithmeticFunction.moebius d) ^ 2 * liouvilleLambda d = ArithmeticFunction.moebius d := by
  have h_mult_lam : liouvilleArith.IsMultiplicative := by
    refine ⟨by decide, ?_⟩
    intro a b _
    by_cases ha0 : a = 0
    · subst ha0; simp [liouvilleArith, liouvilleLambda]
    · by_cases hb0 : b = 0
      · subst hb0; simp [liouvilleArith, liouvilleLambda]
      · exact liouvilleLambda_mul_aux ha0 hb0
  have h_mult_mu_sq_lam : muSqTimesLambdaArith.IsMultiplicative := by
    refine ⟨by decide, ?_⟩
    intro a b cop
    change (ArithmeticFunction.moebius (a * b)) ^ 2 * liouvilleLambda (a * b) =
      ((ArithmeticFunction.moebius a) ^ 2 * liouvilleLambda a) *
        ((ArithmeticFunction.moebius b) ^ 2 * liouvilleLambda b)
    have hmu : ArithmeticFunction.moebius (a * b) =
        ArithmeticFunction.moebius a * ArithmeticFunction.moebius b :=
      ArithmeticFunction.isMultiplicative_moebius.2 cop
    have hlam : liouvilleLambda (a * b) = liouvilleLambda a * liouvilleLambda b :=
      h_mult_lam.2 cop
    rw [hmu, hlam]
    ring
  have h_eq_fn : muSqTimesLambdaArith = ArithmeticFunction.moebius := by
    rw [ArithmeticFunction.IsMultiplicative.eq_iff_eq_on_prime_powers
      muSqTimesLambdaArith h_mult_mu_sq_lam
      ArithmeticFunction.moebius ArithmeticFunction.isMultiplicative_moebius]
    intro q e hq
    change (ArithmeticFunction.moebius (q ^ e)) ^ 2 * liouvilleLambda (q ^ e) =
      ArithmeticFunction.moebius (q ^ e)
    rw [moebius_apply_prime_pow_eq_primePowerMoebius_aux hq e, liouvilleLambda_prime_pow_aux hq e]
    rcases e with _ | _ | e
    · decide
    · decide
    · dsimp [primePowerMoebius, liouvilleSignFromOmega]
      ring
  exact congrFun (congrArg DFunLike.coe h_eq_fn) d

/-- **Theorem 9 (`TASK-TC-055` §3, Actual Integer Coprimality Sieve Identity on `ℕ`)**:
    Formal scope: finite integer divisor sieve identity on `ℕ` (does not formalize infinite Dirichlet-series or
    operator-norm convergence). Proves for any prime `p : ℕ` and positive integers `n N_P d : ℕ` with `d ∣ gcd(n, N_P)` that:
    1. `liouvilleLambda (p * n) = -liouvilleLambda n` and `liouvilleLambda (p * n) + liouvilleLambda n = 0`;
    2. For every divisor `d ∣ gcd(n, N_P)`, `μ(d)^2 λ(n / d) = λ(n) μ(d)`;
    3. The finite squarefree prime-exclusion sieve sum `actualPrimeExclusionSieveSum N_P n = ∑_{d ∣ gcd(n, N_P)} μ(d)^2 λ(n / d)`
       equals `λ(n)` if `Nat.Coprime n N_P` and `0` otherwise (`if n.Coprime N_P then liouvilleLambda n else 0`). -/
theorem actual_finite_prime_exclusion_sieve_identity_nat
    {p n N_P d : ℕ} (hp : p.Prime) (hn : n ≠ 0) (_hNP : N_P ≠ 0) (hd : d ∣ Nat.gcd n N_P) :
    (liouvilleLambda (p * n) = -liouvilleLambda n ∧
      liouvilleLambda (p * n) + liouvilleLambda n = 0) ∧
    (ArithmeticFunction.moebius d) ^ 2 * liouvilleLambda (n / d) =
      liouvilleLambda n * ArithmeticFunction.moebius d ∧
    actualPrimeExclusionSieveSum N_P n =
      (if n.Coprime N_P then liouvilleLambda n else 0) := by
  have h_lam_p : liouvilleLambda p = -1 := by
    have h_op : natOmega p = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr hp
    simp [liouvilleLambda, hp.ne_zero, h_op, liouvilleSignFromOmega]
  have h_pn : liouvilleLambda (p * n) = -liouvilleLambda n := by
    rw [liouvilleLambda_mul_aux hp.ne_zero hn, h_lam_p]
    ring
  have h_term : ∀ c : ℕ, c ∣ Nat.gcd n N_P →
      (ArithmeticFunction.moebius c) ^ 2 * liouvilleLambda (n / c) =
        liouvilleLambda n * ArithmeticFunction.moebius c := by
    intro c hc
    have hc_n : c ∣ n := dvd_trans hc (Nat.gcd_dvd_left n N_P)
    rw [liouvilleLambda_div_of_dvd_aux hn hc_n]
    calc
      (ArithmeticFunction.moebius c) ^ 2 * (liouvilleLambda n * liouvilleLambda c) =
        liouvilleLambda n * ((ArithmeticFunction.moebius c) ^ 2 * liouvilleLambda c) := by ring
      _ = liouvilleLambda n * ArithmeticFunction.moebius c := by
        rw [moebius_sq_mul_liouvilleLambda_eq_moebius_aux c]
  have h_sieve :
      actualPrimeExclusionSieveSum N_P n =
        (if n.Coprime N_P then liouvilleLambda n else 0) := by
    dsimp [actualPrimeExclusionSieveSum]
    have h_congr :
        (∑ c ∈ (Nat.gcd n N_P).divisors, (ArithmeticFunction.moebius c) ^ 2 * liouvilleLambda (n / c)) =
          ∑ c ∈ (Nat.gcd n N_P).divisors, liouvilleLambda n * ArithmeticFunction.moebius c := by
      apply Finset.sum_congr rfl
      intro c hc
      rw [Nat.mem_divisors] at hc
      exact h_term c hc.1
    rw [h_congr, ← Finset.mul_sum]
    have h_mu_sum :
        (∑ c ∈ (Nat.gcd n N_P).divisors, ArithmeticFunction.moebius c) =
          if Nat.gcd n N_P = 1 then 1 else 0 := by
      have h_mul_zeta :
          (ArithmeticFunction.moebius * (ArithmeticFunction.zeta : ArithmeticFunction ℤ)) (Nat.gcd n N_P) =
            (1 : ArithmeticFunction ℤ) (Nat.gcd n N_P) := by
        rw [ArithmeticFunction.moebius_mul_coe_zeta]
      rw [ArithmeticFunction.coe_mul_zeta_apply, ArithmeticFunction.one_apply] at h_mul_zeta
      exact h_mul_zeta
    rw [h_mu_sum]
    by_cases hcop : n.Coprime N_P
    · have h1 : Nat.gcd n N_P = 1 := hcop
      rw [if_pos h1, mul_one, if_pos hcop]
    · have hne1 : Nat.gcd n N_P ≠ 1 := hcop
      rw [if_neg hne1, mul_zero, if_neg hcop]
  exact ⟨⟨h_pn, by linarith⟩, h_term d hd, h_sieve⟩

/-- **Theorem 10 (`TASK-TC-055` §7, Single-Prime Parity Arithmetic and Concrete Separation on `ℕ`)**:
    Formal scope: integer arithmetic of `primeParityControl p n = (-1)^{v_p(n)}` and `twoAdicParityControl n = (-1)^{v_2(n)}`
    on `ℕ` (does not formalize infinite-series asymptotics of `Q_{a_2}(X)` or `E_{a_2}(Y)`).
    Proves on actual positive integers `p, q, m, n, d, r, s : ℕ` that:
    1. `primeParityControl p 1 = 1`, `primeParityControl p p = -1`, and `primeParityControl p q = 1` for prime `q ≠ p`;
    2. Complete multiplicativity `primeParityControl p (m * n) = primeParityControl p m * primeParityControl p n`;
    3. Unit square `primeParityControl p d * primeParityControl p d = 1` and unconstrained common-factor
       cancellation `primeParityControl p (d * r) * primeParityControl p (d * s) = primeParityControl p r * primeParityControl p s`;
    4. Exact parity flip at `p`: `primeParityControl p (p * n) = -primeParityControl p n` and
       `primeParityControl p (p * n) + primeParityControl p n = 0`;
    5. Exact separation from `liouvilleLambda` and `actualFlatMoebiusSquareDivisorSum` at odd prime `n = 3`:
       `twoAdicParityControl 3 = 1`, `liouvilleLambda 3 = -1`, `actualFlatMoebiusSquareDivisorSum 3 = -1`,
       and `twoAdicParityControl 3 ≠ actualFlatMoebiusSquareDivisorSum 3`. -/
theorem prime_parity_control_multiplicative_and_moebius_separation_nat
    {p q m n d r s : ℕ} (hp : p.Prime) (hq : q.Prime) (hpq : q ≠ p)
    (hm : m ≠ 0) (hn : n ≠ 0) (hd : d ≠ 0) (hr : r ≠ 0) (hs : s ≠ 0) :
    (primeParityControl p 1 = 1 ∧ primeParityControl p p = -1 ∧ primeParityControl p q = 1) ∧
    primeParityControl p (m * n) = primeParityControl p m * primeParityControl p n ∧
    primeParityControl p d * primeParityControl p d = 1 ∧
    primeParityControl p (d * r) * primeParityControl p (d * s) =
      primeParityControl p r * primeParityControl p s ∧
    (primeParityControl p (p * n) = -primeParityControl p n ∧
      primeParityControl p (p * n) + primeParityControl p n = 0) ∧
    (twoAdicParityControl 1 = 1 ∧ twoAdicParityControl 2 = -1 ∧ twoAdicParityControl 3 = 1 ∧
      liouvilleLambda 3 = -1 ∧ actualFlatMoebiusSquareDivisorSum 3 = -1 ∧
      twoAdicParityControl 3 ≠ actualFlatMoebiusSquareDivisorSum 3) := by
  have hp1 : primeParityControl p 1 = 1 := by
    simp [primeParityControl]
  have hpp : primeParityControl p p = -1 := by
    simp [primeParityControl, hp.ne_zero, hp.factorization_self]
  have hpq_val : primeParityControl p q = 1 := by
    have h_zero : q.factorization p = 0 := by
      rw [hq.factorization, Finsupp.single_apply, if_neg hpq]
    simp [primeParityControl, hq.ne_zero, h_zero]
  have h_mul_gen : ∀ a b : ℕ, a ≠ 0 → b ≠ 0 →
      primeParityControl p (a * b) = primeParityControl p a * primeParityControl p b := by
    intro a b ha hb
    have hab : a * b ≠ 0 := mul_ne_zero ha hb
    have hfact : (a * b).factorization p = a.factorization p + b.factorization p := by
      rw [Nat.factorization_mul ha hb, Finsupp.add_apply]
    simp [primeParityControl, ha, hb, hab, hfact, pow_add]
  have h_sq_gen : ∀ a : ℕ, a ≠ 0 → primeParityControl p a * primeParityControl p a = 1 := by
    intro a ha
    simp only [primeParityControl, ha, ↓reduceIte]
    rw [← pow_add]
    have h_even : a.factorization p + a.factorization p = 2 * (a.factorization p) := by omega
    rw [h_even, pow_mul]
    norm_num
  have h_cancel :
      primeParityControl p (d * r) * primeParityControl p (d * s) =
        primeParityControl p r * primeParityControl p s := by
    rw [h_mul_gen d r hd hr, h_mul_gen d s hd hs]
    calc
      (primeParityControl p d * primeParityControl p r) *
          (primeParityControl p d * primeParityControl p s) =
        (primeParityControl p d * primeParityControl p d) *
          (primeParityControl p r * primeParityControl p s) := by ring
      _ = 1 * (primeParityControl p r * primeParityControl p s) := by rw [h_sq_gen d hd]
      _ = primeParityControl p r * primeParityControl p s := by ring
  have h_flip : primeParityControl p (p * n) = -primeParityControl p n := by
    rw [h_mul_gen p n hp.ne_zero hn, hpp]
    ring
  have h_a2_1 : twoAdicParityControl 1 = 1 := by
    simp [twoAdicParityControl, primeParityControl]
  have h_a2_2 : twoAdicParityControl 2 = -1 := by
    have h2 : (2 : ℕ).Prime := Nat.prime_two
    dsimp [twoAdicParityControl]
    simp [primeParityControl, h2.factorization_self]
  have h_a2_3 : twoAdicParityControl 3 = 1 := by
    have h3 : (3 : ℕ).Prime := Nat.prime_three
    have h_z : (3 : ℕ).factorization 2 = 0 := by
      rw [h3.factorization, Finsupp.single_apply]
      decide
    dsimp [twoAdicParityControl]
    simp [primeParityControl, h_z]
  have h_lam_3 : liouvilleLambda 3 = -1 := by
    have h3 : (3 : ℕ).Prime := Nat.prime_three
    have h_o3 : natOmega 3 = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr h3
    simp [liouvilleLambda, h_o3, liouvilleSignFromOmega]
  have h_flat_3 : actualFlatMoebiusSquareDivisorSum 3 = -1 := by
    have h_thm4 := (actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat
      Nat.prime_three 1 (by decide : (3 : ℕ) ≠ 0)).2.2.2.2.2.2.2.1
    rw [h_thm4, h_lam_3]
  exact ⟨⟨hp1, hpp, hpq_val⟩, h_mul_gen m n hm hn, h_sq_gen d hd, h_cancel,
    ⟨h_flip, by linarith⟩, ⟨h_a2_1, h_a2_2, h_a2_3, h_lam_3, h_flat_3, by omega⟩⟩

/-- **Theorem 11 (`TASK-TC-055` §§5–7, Conditional Finite Band Inequalities, Opposite-Parity Sign Pairing, and Scalar Constants)**:
    Formal scope: finite sum inequalities conditional on `hK` and `hBand`, integer opposite-parity sign pairing
    `λ(p m) + λ(q r m) = 0`, and scalar rational constants (does not formalize infinite-series kernel asymptotics
    or analytic kernel difference bounds).
    1. Finite near-diagonal sum bound: for any kernel `K : ℕ → ℕ → ℝ` satisfying `hK : ∀ m n, 2 * K m n ≤ K m m + K n n`
       and any `M h : ℕ`,
       `2 * (∑ m ∈ Finset.range M, K m (m + h)) ≤ (∑ m ∈ Finset.range M, K m m) + (∑ m ∈ Finset.range M, K (m + h) (m + h))`,
       and if each of the `2 * H + 1` offset diagonals `bandSum j` (`j ∈ Finset.range (2 * H + 1)`) satisfies `hBand : bandSum j ≤ D_E`,
       then `∑ j ∈ Finset.range (2 * H + 1), bandSum j ≤ (2 * (H : ℝ) + 1) * D_E`;
    2. Opposite-parity prime–semiprime dilation sign pairing on actual integers: for primes `p, q, r : ℕ` and `m ≠ 0`,
       `liouvilleLambda (p * m) = -liouvilleLambda m`, `liouvilleLambda (q * r * m) = liouvilleLambda m`,
       `liouvilleLambda (p * m) + liouvilleLambda (q * r * m) = 0`, and for real kernel values `K_pm, K_qrm : ℝ`,
       `(liouvilleLambda (p * m) : ℝ) * K_pm + (liouvilleLambda (q * r * m) : ℝ) * K_qrm = (liouvilleLambda m : ℝ) * (K_qrm - K_pm)`;
    3. Diagonal energy and `a_2` control leading-coefficient rational algebra:
       `(3 / 8 : ℝ) * (1 / 8 : ℝ) = 3 / 64`, `(1 / 2 : ℝ) * (1 - 2 / 3) = 1 / 6`, and `(1 / 6 : ℝ) ^ 2 = 1 / 36`. -/
theorem near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing
    (K : ℕ → ℕ → ℝ) (bandSum : ℕ → ℝ) (D_E K_pm K_qrm : ℝ)
    (M h H : ℕ) {p q r m : ℕ}
    (hK : ∀ a b : ℕ, 2 * K a b ≤ K a a + K b b)
    (hBand : ∀ j ∈ Finset.range (2 * H + 1), bandSum j ≤ D_E)
    (hp : p.Prime) (hq : q.Prime) (hr : r.Prime) (hm : m ≠ 0) :
    (2 * (∑ a ∈ Finset.range M, K a (a + h)) ≤
        (∑ a ∈ Finset.range M, K a a) + (∑ a ∈ Finset.range M, K (a + h) (a + h)) ∧
      (∑ j ∈ Finset.range (2 * H + 1), bandSum j) ≤ (2 * (H : ℝ) + 1) * D_E) ∧
    (liouvilleLambda (p * m) = -liouvilleLambda m ∧
      liouvilleLambda (q * r * m) = liouvilleLambda m ∧
      liouvilleLambda (p * m) + liouvilleLambda (q * r * m) = 0 ∧
      (liouvilleLambda (p * m) : ℝ) * K_pm + (liouvilleLambda (q * r * m) : ℝ) * K_qrm =
        (liouvilleLambda m : ℝ) * (K_qrm - K_pm)) ∧
    ((3 / 8 : ℝ) * (1 / 8 : ℝ) = 3 / 64 ∧
      (1 / 2 : ℝ) * (1 - 2 / 3) = 1 / 6 ∧
      (1 / 6 : ℝ) ^ 2 = 1 / 36) := by
  refine ⟨?_, ?_, by norm_num⟩
  · constructor
    · rw [Finset.mul_sum, ← Finset.sum_add_distrib]
      exact Finset.sum_le_sum (fun a _ => hK a (a + h))
    · calc
        (∑ j ∈ Finset.range (2 * H + 1), bandSum j) ≤
          ∑ _ ∈ Finset.range (2 * H + 1), D_E := Finset.sum_le_sum hBand
        _ = ((2 * H + 1 : ℕ) : ℝ) * D_E := by
          rw [Finset.sum_const, Finset.card_range, nsmul_eq_mul]
        _ = (2 * (H : ℝ) + 1) * D_E := by push_cast; ring
  · have h_lp : liouvilleLambda p = -1 := by
      have h_op : natOmega p = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr hp
      simp [liouvilleLambda, hp.ne_zero, h_op, liouvilleSignFromOmega]
    have h_lq : liouvilleLambda q = -1 := by
      have h_oq : natOmega q = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr hq
      simp [liouvilleLambda, hq.ne_zero, h_oq, liouvilleSignFromOmega]
    have h_lr : liouvilleLambda r = -1 := by
      have h_or : natOmega r = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr hr
      simp [liouvilleLambda, hr.ne_zero, h_or, liouvilleSignFromOmega]
    have h_pm : liouvilleLambda (p * m) = -liouvilleLambda m := by
      rw [liouvilleLambda_mul_aux hp.ne_zero hm, h_lp]
      ring
    have h_qrm : liouvilleLambda (q * r * m) = liouvilleLambda m := by
      have hqr : q * r ≠ 0 := mul_ne_zero hq.ne_zero hr.ne_zero
      rw [liouvilleLambda_mul_aux hqr hm, liouvilleLambda_mul_aux hq.ne_zero hr.ne_zero, h_lq, h_lr]
      ring
    refine ⟨h_pm, h_qrm, by omega, ?_⟩
    rw [h_pm, h_qrm]
    push_cast
    ring

/-- **Theorem 12 (`TASK-TC-055R` §§2–7, Pairing Counterexample, Valid Kernel Ratio Replacement, Cutoff Counterexample, and Scalar Truncation Algebra)**:
    Formal scope (cutoff arithmetic, termwise multiplicativity, and scalar inequalities; see Theorems 13–16
    below for the full smooth/coprime factorization bijection, arbitrary-weight finite-sum reconstruction,
    uncoupled-cutoff excess formula, finite Gaussian observable reconstruction, and weighted cofactor square):
    1. Pointwise factorized kernel integrand AM-GM identity and inequality (discharging `hK` pointwise on
       `kernelPointwiseIntegrand g X4 a b = X4 * g a * g b` for `0 ≤ X4`);
    2. Exact arithmetic counterexample comparison refuting retired TC-055 Lemma 6.1 at
       `(Y, p, q, r, m, n) = (33, 11, 2, 5, 1, 11)`:
       `(3 : ℝ) * ((11 - 10 : ℝ) / 10) * ((11 : ℝ) / 10) ^ 3 = 3993 / 10000`,
       `(33 : ℝ) ^ 2 * ((1 : ℝ) / 10 ^ 2 - (1 : ℝ) / 11 ^ 2) = 189 / 100`,
       `1 + (189 : ℝ) / 100 = 2890 / 1000`, `1 - (1331 : ℝ) / 2890 = 1559 / 2890`,
       `(3993 : ℝ) / 10000 < 1559 / 2890`, and if `0 < K_11` and `K_10 < (1331 / 2890) * K_11` then
       `((3993 : ℝ) / 10000) * K_11 < K_11 - K_10`;
    3. Valid replacement two-sided kernel ratio enclosure implication: if `0 ≤ K_b`, `L_low * K_b ≤ K_a`, and
       `K_a ≤ L_high * K_b`, then `|K_a - K_b| ≤ max |L_low - 1| |L_high - 1| * K_b`;
    4. Non-integer cutoff counterexample at `u = 2.9` (`29 / 10`) and repaired parity-control constants:
       `1 / (2 * (29 / 10)^2) = 50 / 841 < 1 / 3^3 + 1 / 4^3 + 1 / 5^3 < 1 / (2 * 2^2) = 1 / 8`,
       `(2 : ℝ) * (3 / 2 : ℝ) ^ 3 = 27 / 4 < 3 ^ 3`, and for `S = {3, 5, 7}`,
       `((3 - 1 : ℝ) / (3 + 1)) * ((5 - 1 : ℝ) / (5 + 1)) * ((7 - 1 : ℝ) / (7 + 1)) = 1 / 4`,
       `(1 / 2 : ℝ) * (1 / 4 : ℝ) = 1 / 8`, `(1 / 8 : ℝ) ^ 2 = 1 / 64`;
    5. Pointwise cutoff equivalence `m * r ≤ T ↔ r ≤ T / m` (`0 < m`), termwise Liouville multiplicativity,
       truncation tail energy scalar identity `((1 : ℝ) / (2 * T_real ^ 2)) ^ 2 * ((tau5 - 1) * Y5 / 5) = (tau5 - 1) * Y5 / (20 * T_real ^ 4)`,
       and two-sided scalar square transfer `v_full ^ 2 ≤ 2 * v_T ^ 2 + 2 * (v_full - v_T) ^ 2 ∧ v_T ^ 2 ≤ 2 * v_full ^ 2 + 2 * (v_full - v_T) ^ 2`. -/
theorem pairing_counterexample_replacement_and_finite_reconstruction_tc055r
    (g w : ℕ → ℝ) (X4 K_10 K_11 K_a K_b L_low L_high T_real tau5 Y5 v_full v_T : ℝ)
    (a b m r T : ℕ)
    (hX4 : 0 ≤ X4)
    (hK11_pos : 0 < K_11) (hK10_lt : K_10 < (1331 / 2890 : ℝ) * K_11)
    (hKb_nonneg : 0 ≤ K_b) (hKa_low : L_low * K_b ≤ K_a) (hKa_high : K_a ≤ L_high * K_b)
    (hm_pos : 0 < m) (hr_ne : r ≠ 0) (_hT_ne : T_real ≠ 0) :
    (kernelPointwiseIntegrand g X4 a a + kernelPointwiseIntegrand g X4 b b -
        2 * kernelPointwiseIntegrand g X4 a b = X4 * (g a - g b) ^ 2 ∧
      2 * kernelPointwiseIntegrand g X4 a b ≤
        kernelPointwiseIntegrand g X4 a a + kernelPointwiseIntegrand g X4 b b) ∧
    ((3 : ℝ) * ((11 - 10 : ℝ) / 10) * ((11 : ℝ) / 10) ^ 3 = 3993 / 10000 ∧
      (33 : ℝ) ^ 2 * ((1 : ℝ) / 10 ^ 2 - (1 : ℝ) / 11 ^ 2) = 189 / 100 ∧
      1 + (189 : ℝ) / 100 = 2890 / 1000 ∧
      1 - (1331 : ℝ) / 2890 = 1559 / 2890 ∧
      (3993 : ℝ) / 10000 < 1559 / 2890 ∧
      ((3993 : ℝ) / 10000) * K_11 < K_11 - K_10) ∧
    |K_a - K_b| ≤ max |L_low - 1| |L_high - 1| * K_b ∧
    ((1 : ℝ) / (2 * (29 / 10 : ℝ) ^ 2) = 50 / 841 ∧
      (1 : ℝ) / (2 * (29 / 10 : ℝ) ^ 2) <
        (1 : ℝ) / 3 ^ 3 + (1 : ℝ) / 4 ^ 3 + (1 : ℝ) / 5 ^ 3 ∧
      (1 : ℝ) / 3 ^ 3 + (1 : ℝ) / 4 ^ 3 + (1 : ℝ) / 5 ^ 3 < 1 / (2 * (2 : ℝ) ^ 2) ∧
      (2 : ℝ) * (3 / 2 : ℝ) ^ 3 = 27 / 4 ∧
      (27 / 4 : ℝ) < 3 ^ 3 ∧
      ((3 - 1 : ℝ) / (3 + 1)) * ((5 - 1 : ℝ) / (5 + 1)) * ((7 - 1 : ℝ) / (7 + 1)) = 1 / 4 ∧
      (1 / 2 : ℝ) * (1 / 4 : ℝ) = 1 / 8 ∧
      (1 / 8 : ℝ) ^ 2 = 1 / 64) ∧
    ((m * r ≤ T ↔ r ≤ T / m) ∧
      (liouvilleLambda (m * r) : ℝ) * w (m * r) =
        (liouvilleLambda m : ℝ) * ((liouvilleLambda r : ℝ) * w (m * r)) ∧
      ((1 : ℝ) / (2 * T_real ^ 2)) ^ 2 * ((tau5 - 1) * Y5 / 5) =
        (tau5 - 1) * Y5 / (20 * T_real ^ 4) ∧
      v_full ^ 2 ≤ 2 * v_T ^ 2 + 2 * (v_full - v_T) ^ 2 ∧
      v_T ^ 2 ≤ 2 * v_full ^ 2 + 2 * (v_full - v_T) ^ 2) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · have h_id :
        kernelPointwiseIntegrand g X4 a a + kernelPointwiseIntegrand g X4 b b -
          2 * kernelPointwiseIntegrand g X4 a b = X4 * (g a - g b) ^ 2 := by
      dsimp [kernelPointwiseIntegrand]
      ring
    have h_nonneg : 0 ≤ X4 * (g a - g b) ^ 2 := mul_nonneg hX4 (sq_nonneg _)
    exact ⟨h_id, by linarith⟩
  · refine ⟨by norm_num, by norm_num, by norm_num, by norm_num, by norm_num, ?_⟩
    linarith
  · rw [abs_le]
    have h_max_l : -(max |L_low - 1| |L_high - 1|) ≤ L_low - 1 := by
      have h1 : -(L_low - 1) ≤ |L_low - 1| := neg_le_abs (L_low - 1)
      have h2 : |L_low - 1| ≤ max |L_low - 1| |L_high - 1| := le_max_left _ _
      linarith
    have h_max_r : L_high - 1 ≤ max |L_low - 1| |L_high - 1| :=
      le_trans (le_abs_self (L_high - 1)) (le_max_right _ _)
    constructor
    · have h_mul_l :
          -(max |L_low - 1| |L_high - 1| * K_b) ≤ (L_low - 1) * K_b := by
        have h_tmp := mul_le_mul_of_nonneg_right h_max_l hKb_nonneg
        linarith
      linarith
    · have h_mul_r :
          (L_high - 1) * K_b ≤ max |L_low - 1| |L_high - 1| * K_b :=
        mul_le_mul_of_nonneg_right h_max_r hKb_nonneg
      linarith
  · refine ⟨by norm_num, by norm_num, by norm_num, by norm_num, by norm_num, by norm_num, by norm_num, by norm_num⟩
  · refine ⟨?_, ?_, ?_, ?_, ?_⟩
    · rw [mul_comm, Nat.le_div_iff_mul_le hm_pos]
    · have hm_ne : m ≠ 0 := Nat.pos_iff_ne_zero.mp hm_pos
      rw [liouvilleLambda_mul_aux hm_ne hr_ne]
      push_cast
      ring
    · ring
    · nlinarith [sq_nonneg (v_full - 2 * v_T)]
    · nlinarith [sq_nonneg (v_T - 2 * v_full)]

/-! ### `TASK-TC-055R2` Section 3: Full Finite Smooth/Coprime Factorization Bijection, Reindexed Liouville Reconstruction, Uncoupled-Cutoff Excess Formula, and Weighted Cofactor Square Expansion -/

/-- Product modulus `N_P := ∏_{p ∈ P} p` of a finite prime set `P : Finset ℕ` (`N_∅ = 1`). -/
def primeProductModulus (P : Finset ℕ) : ℕ :=
  ∏ p ∈ P, p

/-- Predicate `m ∈ S(P)`: `m` is a positive integer all of whose prime divisors belong to `P`. -/
def isPSmooth (P : Finset ℕ) (m : ℕ) : Prop :=
  0 < m ∧ ∀ p : ℕ, p.Prime → p ∣ m → p ∈ P

/-- Constructive decidability instance for `isPSmooth P m` via `m.primeFactors`. -/
instance instDecidableIsPSmooth (P : Finset ℕ) (m : ℕ) : Decidable (isPSmooth P m) :=
  decidable_of_iff (0 < m ∧ ∀ p ∈ m.primeFactors, p ∈ P)
    ⟨fun ⟨hm, hpf⟩ =>
      ⟨hm, fun p hp hdvd => hpf p (Nat.mem_primeFactors.mpr ⟨hp, hdvd, Nat.pos_iff_ne_zero.mp hm⟩)⟩,
     fun ⟨hm, hall⟩ =>
      ⟨hm, fun p hp => hall p (Nat.prime_of_mem_primeFactors hp) (Nat.dvd_of_mem_primeFactors hp)⟩⟩

/-- Canonical `P`-smooth factor `m = ∏_{p ∣ n, p ∈ P} p^{v_p(n)}` of `n : ℕ`. -/
def pSmoothPart (P : Finset ℕ) (n : ℕ) : ℕ :=
  ∏ p ∈ n.primeFactors.filter (· ∈ P), p ^ (n.factorization p)

/-- Canonical `P`-coprime factor `r = ∏_{p ∣ n, p ∉ P} p^{v_p(n)}` of `n : ℕ`. -/
def pCoprimePart (P : Finset ℕ) (n : ℕ) : ℕ :=
  ∏ p ∈ n.primeFactors.filter (· ∉ P), p ^ (n.factorization p)

/-- Finite `P`-smooth index set `{1 ≤ m ≤ L : m ∈ S(P)}` (`= ∅` for `L = 0`). -/
def smoothCutoffFinset (P : Finset ℕ) (L : ℕ) : Finset ℕ :=
  (Finset.Icc 1 L).filter (fun m => isPSmooth P m)

/-- Finite `P`-coprime index set `{1 ≤ r ≤ L : gcd(r, N_P) = 1}` (`= ∅` for `L = 0`). -/
def coprimeCutoffFinset (P : Finset ℕ) (L : ℕ) : Finset ℕ :=
  (Finset.Icc 1 L).filter (fun r => Nat.Coprime r (primeProductModulus P))

/-- Coupled finite pair index set `{(m, r) : m ∈ smoothCutoffFinset P T, r ∈ coprimeCutoffFinset P (T / m)}`. -/
def smoothCoprimePairsUpTo (P : Finset ℕ) (T : ℕ) : Finset (ℕ × ℕ) :=
  (smoothCutoffFinset P T).biUnion (fun m =>
    (coprimeCutoffFinset P (T / m)).image (fun r => (m, r)))

/-- Uncoupled-cutoff excess index set `{⌊T/m⌋ + 1 ≤ r ≤ T : gcd(r, N_P) = 1}` when `r ≤ T` replaces `r ≤ ⌊T/m⌋`. -/
def excessCoprimeFinset (P : Finset ℕ) (m T : ℕ) : Finset ℕ :=
  (Finset.Icc (T / m + 1) T).filter (fun r => Nat.Coprime r (primeProductModulus P))

/-- Actual finite `T`-truncated Liouville Gaussian observable
    `Q_{λ,T}(X) := X^{5/2} ∑_{1 ≤ n ≤ T} λ(n) n^{-3} exp(-X^2 / n^2)` (`Q_{λ,0}(X) = 0`). -/
noncomputable def finiteQLambda (T : ℕ) (X : ℝ) : ℝ :=
  X ^ (5 / 2 : ℝ) *
    ∑ n ∈ Finset.Icc 1 T,
      (liouvilleLambda n : ℝ) * ((n : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (n : ℝ) ^ 2)

/-- Actual finite `P`-coprime Liouville Gaussian observable
    `Q_{λ,P,L}(w) := w^{5/2} ∑_{1 ≤ r ≤ L, gcd(r, N_P) = 1} λ(r) r^{-3} exp(-w^2 / r^2)`. -/
noncomputable def finiteQLambdaCoprime (P : Finset ℕ) (L : ℕ) (w : ℝ) : ℝ :=
  w ^ (5 / 2 : ℝ) *
    ∑ r ∈ coprimeCutoffFinset P L,
      (liouvilleLambda r : ℝ) * ((r : ℝ) ^ 3)⁻¹ * Real.exp (-(w ^ 2) / (r : ℝ) ^ 2)

/-- Actual finite `P`-smooth-only Liouville Gaussian observable
    `Q_{λ,S(P),L}(w) := w^{5/2} ∑_{m ≤ L, m ∈ S(P)} λ(m) m^{-3} exp(-w^2 / m^2)`. -/
noncomputable def finiteQLambdaSmooth (P : Finset ℕ) (L : ℕ) (w : ℝ) : ℝ :=
  w ^ (5 / 2 : ℝ) *
    ∑ m ∈ smoothCutoffFinset P L,
      (liouvilleLambda m : ℝ) * ((m : ℝ) ^ 3)⁻¹ * Real.exp (-(w ^ 2) / (m : ℝ) ^ 2)

/-- Weighted `r`-cofactor fiber `F_r(X) := (λ(r) / √r) · Q_{λ,S(P),⌊T/r⌋}(X / r)`. -/
noncomputable def cofactorFiberF (P : Finset ℕ) (T r : ℕ) (X : ℝ) : ℝ :=
  ((liouvilleLambda r : ℝ) / Real.sqrt (r : ℝ)) *
    finiteQLambdaSmooth P (T / r) (X / (r : ℝ))

/-- Helper: `pSmoothPart P n * pCoprimePart P n = n` for all `n > 0`. -/
private theorem pSmoothPart_mul_pCoprimePart_aux (P : Finset ℕ) {n : ℕ} (hn : 0 < n) :
    pSmoothPart P n * pCoprimePart P n = n := by
  have hn_ne : n ≠ 0 := Nat.pos_iff_ne_zero.mp hn
  dsimp [pSmoothPart, pCoprimePart]
  rw [Finset.prod_filter_mul_prod_filter_not n.primeFactors (· ∈ P) (fun p => p ^ (n.factorization p))]
  calc
    ∏ p ∈ n.primeFactors, p ^ (n.factorization p)
      = n.factorization.prod (fun p k => p ^ k) := by
          rw [Finsupp.prod, Nat.support_factorization]
    _ = n := Nat.factorization_prod_pow_eq_self hn_ne

/-- Helper: if a prime `q` divides a `Finset` product `∏ x ∈ s, g x`, it divides some factor `g x`. -/
private theorem prime_dvd_finset_prod_aux {α : Type*} [DecidableEq α] {q : ℕ} (hq : q.Prime)
    (s : Finset α) (g : α → ℕ) (hdvd : q ∣ ∏ x ∈ s, g x) : ∃ x ∈ s, q ∣ g x := by
  induction' s using Finset.induction_on with a s ha ih
  · rw [Finset.prod_empty] at hdvd
    exact False.elim (hq.not_dvd_one hdvd)
  · rw [Finset.prod_insert ha] at hdvd
    rcases hq.dvd_mul.mp hdvd with hqa | hqs
    · exact ⟨a, Finset.mem_insert_self a s, hqa⟩
    · obtain ⟨x, hx, hqx⟩ := ih hqs
      exact ⟨x, Finset.mem_insert_of_mem hx, hqx⟩

/-- Helper: `isPSmooth P (pSmoothPart P n)` for all `n : ℕ`. -/
private theorem isPSmooth_pSmoothPart_aux (P : Finset ℕ) (n : ℕ) :
    isPSmooth P (pSmoothPart P n) := by
  refine ⟨?_, ?_⟩
  · apply Finset.prod_pos
    intro p hp
    have hp_mem : p ∈ n.primeFactors := (Finset.mem_filter.mp hp).1
    exact pow_pos (Nat.prime_of_mem_primeFactors hp_mem).pos _
  · intro q hq hdvd
    rw [pSmoothPart] at hdvd
    obtain ⟨p, hp, hq_dvd_pow⟩ := prime_dvd_finset_prod_aux hq _ _ hdvd
    have hp_mem : p ∈ n.primeFactors := (Finset.mem_filter.mp hp).1
    have hp_in_P : p ∈ P := (Finset.mem_filter.mp hp).2
    have hp_prime : p.Prime := Nat.prime_of_mem_primeFactors hp_mem
    have hq_dvd_p : q ∣ p := hq.dvd_of_dvd_pow hq_dvd_pow
    have hqp : q = p := (Nat.dvd_prime hp_prime).mp hq_dvd_p |>.resolve_left hq.ne_one
    rwa [hqp]

/-- Helper: every prime dividing `pCoprimePart P n` lies outside `P`. -/
private theorem prime_dvd_pCoprimePart_not_mem_aux (P : Finset ℕ) (n : ℕ) {q : ℕ}
    (hq : q.Prime) (hdvd : q ∣ pCoprimePart P n) : q ∉ P := by
  rw [pCoprimePart] at hdvd
  obtain ⟨p, hp, hq_dvd_pow⟩ := prime_dvd_finset_prod_aux hq _ _ hdvd
  have hp_mem : p ∈ n.primeFactors := (Finset.mem_filter.mp hp).1
  have hp_not_P : p ∉ P := (Finset.mem_filter.mp hp).2
  have hp_prime : p.Prime := Nat.prime_of_mem_primeFactors hp_mem
  have hq_dvd_p : q ∣ p := hq.dvd_of_dvd_pow hq_dvd_pow
  have hqp : q = p := (Nat.dvd_prime hp_prime).mp hq_dvd_p |>.resolve_left hq.ne_one
  rwa [hqp]

/-- Helper: `Nat.Coprime (pCoprimePart P n) (primeProductModulus P)` whenever all elements of `P` are prime. -/
private theorem coprime_pCoprimePart_aux {P : Finset ℕ} (hP : ∀ p ∈ P, p.Prime) (n : ℕ) :
    Nat.Coprime (pCoprimePart P n) (primeProductModulus P) := by
  rw [Nat.coprime_iff_gcd_eq_one]
  by_contra h_ne
  obtain ⟨q, hq_prime, hq_dvd_gcd⟩ := Nat.exists_prime_and_dvd h_ne
  have hq_dvd_cop : q ∣ pCoprimePart P n := dvd_trans hq_dvd_gcd (Nat.gcd_dvd_left _ _)
  have hq_dvd_mod : q ∣ primeProductModulus P := dvd_trans hq_dvd_gcd (Nat.gcd_dvd_right _ _)
  have hq_not_P : q ∉ P := prime_dvd_pCoprimePart_not_mem_aux P n hq_prime hq_dvd_cop
  rw [primeProductModulus] at hq_dvd_mod
  obtain ⟨p, hp_in_P, hq_dvd_p⟩ := prime_dvd_finset_prod_aux hq_prime _ _ hq_dvd_mod
  have hp_prime : p.Prime := hP p hp_in_P
  have hqp : q = p := (Nat.dvd_prime hp_prime).mp hq_dvd_p |>.resolve_left hq_prime.ne_one
  exact hq_not_P (hqp ▸ hp_in_P)

/-- Helper: if `isPSmooth P m` and `Nat.Coprime r (primeProductModulus P)`, then `Nat.Coprime m r`. -/
private theorem coprime_of_isPSmooth_of_coprime_modulus_aux {P : Finset ℕ} {m r : ℕ}
    (hm : isPSmooth P m) (hr : Nat.Coprime r (primeProductModulus P)) :
    Nat.Coprime m r := by
  rw [Nat.coprime_iff_gcd_eq_one]
  by_contra h_ne
  obtain ⟨q, hq_prime, hq_dvd_gcd⟩ := Nat.exists_prime_and_dvd h_ne
  have hq_dvd_m : q ∣ m := dvd_trans hq_dvd_gcd (Nat.gcd_dvd_left _ _)
  have hq_dvd_r : q ∣ r := dvd_trans hq_dvd_gcd (Nat.gcd_dvd_right _ _)
  have hq_in_P : q ∈ P := hm.2 q hq_prime hq_dvd_m
  have hq_dvd_mod : q ∣ primeProductModulus P := Finset.dvd_prod_of_mem (fun x => x) hq_in_P
  have hq_dvd_one : q ∣ 1 := by
    rw [← hr.gcd_eq_one]
    exact Nat.dvd_gcd hq_dvd_r hq_dvd_mod
  exact hq_prime.not_dvd_one hq_dvd_one

/-- **Theorem 13 (`TASK-TC-055R2` §3a, Existence and Uniqueness of Smooth/Coprime Positive Factorization)**:
    For every finite set of primes `P : Finset ℕ` (`∀ p ∈ P, p.Prime`, including `P = ∅` where `N_∅ = 1`)
    and every positive integer `n > 0`:
    1. Canonical decomposition: `pSmoothPart P n * pCoprimePart P n = n`, `isPSmooth P (pSmoothPart P n)`,
       `Nat.Coprime (pCoprimePart P n) (primeProductModulus P)`, and `0 < pCoprimePart P n`;
    2. Uniqueness: any pair `(m, r)` satisfying `m * r = n`, `isPSmooth P m`, and
       `Nat.Coprime r (primeProductModulus P)` equals `(pSmoothPart P n, pCoprimePart P n)`;
    3. Exact `∃!` formulation on `ℕ × ℕ`. -/
theorem smooth_coprime_positive_factorization_exists_unique_nat
    {P : Finset ℕ} (hP : ∀ p ∈ P, p.Prime) {n : ℕ} (hn : 0 < n) :
    (pSmoothPart P n * pCoprimePart P n = n ∧
      isPSmooth P (pSmoothPart P n) ∧
      Nat.Coprime (pCoprimePart P n) (primeProductModulus P) ∧
      0 < pCoprimePart P n) ∧
    (∀ m r : ℕ,
      m * r = n → isPSmooth P m → Nat.Coprime r (primeProductModulus P) →
        m = pSmoothPart P n ∧ r = pCoprimePart P n) ∧
    (∃! mr : ℕ × ℕ,
      mr.1 * mr.2 = n ∧ isPSmooth P mr.1 ∧ Nat.Coprime mr.2 (primeProductModulus P)) := by
  have h_mul : pSmoothPart P n * pCoprimePart P n = n := pSmoothPart_mul_pCoprimePart_aux P hn
  have h_sm : isPSmooth P (pSmoothPart P n) := isPSmooth_pSmoothPart_aux P n
  have h_cop : Nat.Coprime (pCoprimePart P n) (primeProductModulus P) := coprime_pCoprimePart_aux hP n
  have h_rpos : 0 < pCoprimePart P n := by
    by_contra h_not_pos
    have hr0 : pCoprimePart P n = 0 := Nat.eq_zero_of_not_pos h_not_pos
    rw [hr0, mul_zero] at h_mul
    omega
  have h_uniq :
      ∀ m r : ℕ,
        m * r = n → isPSmooth P m → Nat.Coprime r (primeProductModulus P) →
          m = pSmoothPart P n ∧ r = pCoprimePart P n := by
    intro m r hmr hm_sm hr_cop
    have h_eq_prod : m * r = pSmoothPart P n * pCoprimePart P n := hmr.trans h_mul.symm
    have h_cop_m_r0 : Nat.Coprime m (pCoprimePart P n) :=
      coprime_of_isPSmooth_of_coprime_modulus_aux hm_sm h_cop
    have h_cop_m0_r : Nat.Coprime (pSmoothPart P n) r :=
      coprime_of_isPSmooth_of_coprime_modulus_aux h_sm hr_cop
    have hm_dvd_m0 : m ∣ pSmoothPart P n := by
      apply h_cop_m_r0.dvd_of_dvd_mul_right
      exact ⟨r, by rw [← h_eq_prod]⟩
    have hm0_dvd_m : pSmoothPart P n ∣ m := by
      apply h_cop_m0_r.dvd_of_dvd_mul_right
      exact ⟨pCoprimePart P n, h_eq_prod⟩
    have hm_eq : m = pSmoothPart P n := Nat.dvd_antisymm hm_dvd_m0 hm0_dvd_m
    have hr_eq : r = pCoprimePart P n := by
      rw [hm_eq] at h_eq_prod
      exact Nat.eq_of_mul_eq_mul_left h_sm.1 h_eq_prod
    exact ⟨hm_eq, hr_eq⟩
  refine ⟨⟨h_mul, h_sm, h_cop, h_rpos⟩, h_uniq, ?_⟩
  refine ⟨(pSmoothPart P n, pCoprimePart P n), ⟨h_mul, h_sm, h_cop⟩, ?_⟩
  rintro ⟨m, r⟩ ⟨hmr, hm_sm, hr_cop⟩
  obtain ⟨hm_eq, hr_eq⟩ := h_uniq m r hmr hm_sm hr_cop
  exact Prod.ext hm_eq hr_eq

/-- Helper: characterization of membership in `smoothCoprimePairsUpTo P T`. -/
private theorem mem_smoothCoprimePairsUpTo_iff_aux (P : Finset ℕ) (T m r : ℕ) :
    (m, r) ∈ smoothCoprimePairsUpTo P T ↔
      isPSmooth P m ∧ Nat.Coprime r (primeProductModulus P) ∧ 1 ≤ m * r ∧ m * r ≤ T := by
  simp only [smoothCoprimePairsUpTo, Finset.mem_biUnion, Finset.mem_image, Prod.mk.injEq,
    smoothCutoffFinset, coprimeCutoffFinset, Finset.mem_filter, Finset.mem_Icc]
  constructor
  · rintro ⟨m', ⟨⟨_, _⟩, hm'_sm⟩, r', ⟨⟨hr'1, hr'div⟩, hr'_cop⟩, rfl, rfl⟩
    have hm_pos : 0 < m' := hm'_sm.1
    have hmr_le : m' * r' ≤ T := by
      rw [mul_comm]
      exact (Nat.le_div_iff_mul_le hm_pos).mp hr'div
    have hmr_ge : 1 ≤ m' * r' := Nat.mul_pos hm_pos (by omega)
    exact ⟨hm'_sm, hr'_cop, hmr_ge, hmr_le⟩
  · rintro ⟨hm_sm, hr_cop, hmr_ge, hmr_le⟩
    have hm_pos : 0 < m := hm_sm.1
    have hr_pos : 0 < r := by
      by_contra h0
      have hr0 : r = 0 := Nat.eq_zero_of_not_pos h0
      rw [hr0, mul_zero] at hmr_ge
      omega
    have hm_le_mr : m ≤ m * r := Nat.le_mul_of_pos_right m hr_pos
    have hm_le_T : m ≤ T := le_trans hm_le_mr hmr_le
    have hr_le_div : r ≤ T / m := (Nat.le_div_iff_mul_le hm_pos).mpr (by rw [mul_comm]; exact hmr_le)
    exact ⟨m, ⟨⟨hm_pos, hm_le_T⟩, hm_sm⟩, r, ⟨⟨hr_pos, hr_le_div⟩, hr_cop⟩, rfl, rfl⟩

/-- Helper: `isPSmooth ∅ m ↔ m = 1`. -/
private theorem isPSmooth_empty_iff_aux (m : ℕ) :
    isPSmooth ∅ m ↔ m = 1 := by
  constructor
  · rintro ⟨_, hall⟩
    by_contra hm_ne1
    obtain ⟨p, hp_prime, hp_dvd⟩ := Nat.exists_prime_and_dvd hm_ne1
    exact Finset.not_mem_empty p (hall p hp_prime hp_dvd)
  · rintro rfl
    exact ⟨by omega, fun p hp hdvd => False.elim (hp.not_dvd_one hdvd)⟩

/-- **Theorem 14 (`TASK-TC-055R2` §3b, Finite Cutoff Indexing Bijection and Degenerate Boundary Cases)**:
    For every finite set of primes `P : Finset ℕ` (`∀ p ∈ P, p.Prime`) and every cutoff `T : ℕ`:
    1. Inner-cutoff equivalence `m * r ≤ T ↔ r ≤ T / m` (`0 < m`) and range-filter equivalence
       `(Finset.range (T + 1)).filter (isPSmooth P) = smoothCutoffFinset P T`;
    2. Exact membership characterization of `smoothCoprimePairsUpTo P T` and mutual two-sided inverse
       bijection between `Finset.Icc 1 T` and `smoothCoprimePairsUpTo P T` via
       `n ↦ (pSmoothPart P n, pCoprimePart P n)` and `(m, r) ↦ m * r`, with equal cardinalities;
    3. Explicit boundary and degenerate evaluations for `T = 0` (empty sets), `T = 1` (singletons),
       and `P = ∅` (`primeProductModulus ∅ = 1`, `coprimeCutoffFinset ∅ T = Finset.Icc 1 T`,
       `smoothCutoffFinset ∅ T = if 1 ≤ T then {1} else ∅`). -/
theorem finite_smooth_coprime_cutoff_indexing_bijection_nat
    {P : Finset ℕ} (hP : ∀ p ∈ P, p.Prime) (T : ℕ) :
    ((∀ {m r : ℕ}, 0 < m → (m * r ≤ T ↔ r ≤ T / m)) ∧
      (Finset.range (T + 1)).filter (fun m => isPSmooth P m) = smoothCutoffFinset P T) ∧
    ((∀ m r : ℕ,
        (m, r) ∈ smoothCoprimePairsUpTo P T ↔
          isPSmooth P m ∧ Nat.Coprime r (primeProductModulus P) ∧ 1 ≤ m * r ∧ m * r ≤ T) ∧
      (∀ n ∈ Finset.Icc 1 T,
        (pSmoothPart P n, pCoprimePart P n) ∈ smoothCoprimePairsUpTo P T ∧
          pSmoothPart P n * pCoprimePart P n = n) ∧
      (∀ mr ∈ smoothCoprimePairsUpTo P T,
        mr.1 * mr.2 ∈ Finset.Icc 1 T ∧
          (pSmoothPart P (mr.1 * mr.2), pCoprimePart P (mr.1 * mr.2)) = mr) ∧
      (smoothCoprimePairsUpTo P T).card = (Finset.Icc 1 T).card) ∧
    ((smoothCutoffFinset P 0 = ∅ ∧ coprimeCutoffFinset P 0 = ∅ ∧ smoothCoprimePairsUpTo P 0 = ∅) ∧
      (smoothCutoffFinset P 1 = {1} ∧ coprimeCutoffFinset P 1 = {1} ∧ smoothCoprimePairsUpTo P 1 = {(1, 1)}) ∧
      (primeProductModulus ∅ = 1 ∧
        coprimeCutoffFinset ∅ T = Finset.Icc 1 T ∧
        smoothCutoffFinset ∅ T = (if 1 ≤ T then {1} else ∅))) := by
  refine ⟨⟨?_, ?_⟩, ⟨?_, ?_, ?_, ?_⟩, ⟨?_, ?_, ?_⟩⟩
  · intro m r hm
    rw [mul_comm, Nat.le_div_iff_mul_le hm]
  · ext m
    simp only [smoothCutoffFinset, Finset.mem_filter, Finset.mem_range, Finset.mem_Icc]
    constructor
    · rintro ⟨hm_lt, hm_sm⟩
      exact ⟨⟨hm_sm.1, by omega⟩, hm_sm⟩
    · rintro ⟨⟨_, hm_le⟩, hm_sm⟩
      exact ⟨by omega, hm_sm⟩
  · exact mem_smoothCoprimePairsUpTo_iff_aux P T
  · intro n hn
    rw [Finset.mem_Icc] at hn
    have hn_pos : 0 < n := by omega
    obtain ⟨⟨h_mul, h_sm, h_cop, _⟩, _, _⟩ :=
      smooth_coprime_positive_factorization_exists_unique_nat hP hn_pos
    rw [mem_smoothCoprimePairsUpTo_iff_aux]
    exact ⟨⟨h_sm, h_cop, h_mul.symm ▸ hn.1, h_mul.symm ▸ hn.2⟩, h_mul⟩
  · rintro ⟨m, r⟩ hmr
    rw [mem_smoothCoprimePairsUpTo_iff_aux] at hmr
    rcases hmr with ⟨hm_sm, hr_cop, hmr_ge, hmr_le⟩
    have hmr_pos : 0 < m * r := by omega
    obtain ⟨_, h_uniq, _⟩ := smooth_coprime_positive_factorization_exists_unique_nat hP hmr_pos
    obtain ⟨hm_eq, hr_eq⟩ := h_uniq m r rfl hm_sm hr_cop
    exact ⟨Finset.mem_Icc.mpr ⟨hmr_ge, hmr_le⟩, Prod.ext hm_eq.symm hr_eq.symm⟩
  · apply Finset.card_bij (fun mr _ => mr.1 * mr.2)
    · rintro ⟨m, r⟩ hmr
      rw [mem_smoothCoprimePairsUpTo_iff_aux] at hmr
      exact Finset.mem_Icc.mpr ⟨hmr.2.2.1, hmr.2.2.2⟩
    · rintro ⟨m1, r1⟩ h1 ⟨m2, r2⟩ h2 h_eq
      rw [mem_smoothCoprimePairsUpTo_iff_aux] at h1 h2
      have h_pos : 0 < m1 * r1 := by omega
      obtain ⟨_, h_uniq, _⟩ := smooth_coprime_positive_factorization_exists_unique_nat hP h_pos
      obtain ⟨hm1, hr1⟩ := h_uniq m1 r1 rfl h1.1 h1.2.1
      obtain ⟨hm2, hr2⟩ := h_uniq m2 r2 h_eq.symm h2.1 h2.2.1
      exact Prod.ext (hm1.trans hm2.symm) (hr1.trans hr2.symm)
    · intro n hn
      rw [Finset.mem_Icc] at hn
      have hn_pos : 0 < n := by omega
      obtain ⟨⟨h_mul, h_sm, h_cop, _⟩, _, _⟩ :=
        smooth_coprime_positive_factorization_exists_unique_nat hP hn_pos
      refine ⟨(pSmoothPart P n, pCoprimePart P n), ?_, h_mul⟩
      rw [mem_smoothCoprimePairsUpTo_iff_aux]
      exact ⟨h_sm, h_cop, h_mul.symm ▸ hn.1, h_mul.symm ▸ hn.2⟩
  · simp [smoothCutoffFinset, coprimeCutoffFinset, smoothCoprimePairsUpTo]
  · have h1_sm : isPSmooth P 1 := ⟨by omega, fun p hp hdvd => False.elim (hp.not_dvd_one hdvd)⟩
    have h1_cop : Nat.Coprime 1 (primeProductModulus P) := Nat.coprime_one_left _
    have hs1 : smoothCutoffFinset P 1 = {1} := by
      ext m
      simp only [smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc, Finset.mem_singleton]
      constructor
      · rintro ⟨⟨hm1, hmle1⟩, _⟩; omega
      · rintro rfl; exact ⟨⟨by omega, by omega⟩, h1_sm⟩
    have hc1 : coprimeCutoffFinset P 1 = {1} := by
      ext r
      simp only [coprimeCutoffFinset, Finset.mem_filter, Finset.mem_Icc, Finset.mem_singleton]
      constructor
      · rintro ⟨⟨hr1, hrle1⟩, _⟩; omega
      · rintro rfl; exact ⟨⟨by omega, by omega⟩, h1_cop⟩
    refine ⟨hs1, hc1, ?_⟩
    simp [smoothCoprimePairsUpTo, hs1, hc1]
  · have hmod : primeProductModulus ∅ = 1 := rfl
    refine ⟨hmod, ?_, ?_⟩
    · ext r
      simp [coprimeCutoffFinset, hmod]
    · ext m
      by_cases hT : 1 ≤ T
      · simp [smoothCutoffFinset, hT, isPSmooth_empty_iff_aux]
        omega
      · simp [smoothCutoffFinset, hT]
        omega

/-- Helper: general reindexed finite sum over `Finset.Icc 1 T` into smooth-outer / coprime-inner nested sums. -/
private theorem sum_Icc_eq_smooth_outer_coprime_inner_aux
    {P : Finset ℕ} (hP : ∀ p ∈ P, p.Prime) (T : ℕ) (F : ℕ → ℝ) :
    ∑ n ∈ Finset.Icc 1 T, F n =
      ∑ m ∈ smoothCutoffFinset P T,
        ∑ r ∈ coprimeCutoffFinset P (T / m), F (m * r) := by
  have h_bij :
      ∑ mr ∈ smoothCoprimePairsUpTo P T, F (mr.1 * mr.2) =
        ∑ n ∈ Finset.Icc 1 T, F n := by
    apply Finset.sum_bij (fun mr _ => mr.1 * mr.2)
    · rintro ⟨m, r⟩ hmr
      rw [mem_smoothCoprimePairsUpTo_iff_aux] at hmr
      exact Finset.mem_Icc.mpr ⟨hmr.2.2.1, hmr.2.2.2⟩
    · rintro ⟨m1, r1⟩ h1 ⟨m2, r2⟩ h2 h_eq
      rw [mem_smoothCoprimePairsUpTo_iff_aux] at h1 h2
      have h_pos : 0 < m1 * r1 := by omega
      obtain ⟨_, h_uniq, _⟩ := smooth_coprime_positive_factorization_exists_unique_nat hP h_pos
      obtain ⟨hm1, hr1⟩ := h_uniq m1 r1 rfl h1.1 h1.2.1
      obtain ⟨hm2, hr2⟩ := h_uniq m2 r2 h_eq.symm h2.1 h2.2.1
      exact Prod.ext (hm1.trans hm2.symm) (hr1.trans hr2.symm)
    · intro n hn
      rw [Finset.mem_Icc] at hn
      have hn_pos : 0 < n := by omega
      obtain ⟨⟨h_mul, h_sm, h_cop, _⟩, _, _⟩ :=
        smooth_coprime_positive_factorization_exists_unique_nat hP hn_pos
      refine ⟨(pSmoothPart P n, pCoprimePart P n), ?_, h_mul⟩
      rw [mem_smoothCoprimePairsUpTo_iff_aux]
      exact ⟨h_sm, h_cop, h_mul.symm ▸ hn.1, h_mul.symm ▸ hn.2⟩
    · intros; rfl
  rw [← h_bij, smoothCoprimePairsUpTo, Finset.sum_biUnion]
  · apply Finset.sum_congr rfl
    intro m _
    rw [Finset.sum_image]
    intro r1 _ r2 _ h_eq
    exact (Prod.mk.inj h_eq).2
  · intro m1 _ m2 _ hne
    dsimp [Function.onFun]
    rw [Finset.disjoint_left]
    intro x hx1 hx2
    rw [Finset.mem_image] at hx1 hx2
    rcases hx1 with ⟨r1, _, rfl⟩
    rcases hx2 with ⟨r2, _, h_eq⟩
    exact hne (Prod.mk.inj h_eq).1.symm

/-- Helper: general reindexed finite sum over `Finset.Icc 1 T` into coprime-outer / smooth-inner nested sums. -/
private theorem sum_Icc_eq_coprime_outer_smooth_inner_aux
    {P : Finset ℕ} (hP : ∀ p ∈ P, p.Prime) (T : ℕ) (F : ℕ → ℝ) :
    ∑ n ∈ Finset.Icc 1 T, F n =
      ∑ r ∈ coprimeCutoffFinset P T,
        ∑ m ∈ smoothCutoffFinset P (T / r), F (m * r) := by
  rw [sum_Icc_eq_smooth_outer_coprime_inner_aux hP T F]
  let S_mr := (smoothCutoffFinset P T).sigma (fun m => coprimeCutoffFinset P (T / m))
  let S_rm := (coprimeCutoffFinset P T).sigma (fun r => smoothCutoffFinset P (T / r))
  rw [Finset.sum_sigma' (smoothCutoffFinset P T) (fun m => coprimeCutoffFinset P (T / m))
        (fun m r => F (m * r)),
      Finset.sum_sigma' (coprimeCutoffFinset P T) (fun r => smoothCutoffFinset P (T / r))
        (fun r m => F (m * r))]
  apply Finset.sum_bij (fun x _ => ⟨x.2, x.1⟩)
  · rintro ⟨m, r⟩ hmr
    simp only [S_mr, S_rm, Finset.mem_sigma, smoothCutoffFinset, coprimeCutoffFinset,
      Finset.mem_filter, Finset.mem_Icc] at hmr ⊢
    rcases hmr with ⟨⟨⟨hm1, _⟩, hm_sm⟩, ⟨⟨hr1, hr_div⟩, hr_cop⟩⟩
    have hmr_le : m * r ≤ T := by
      rw [mul_comm]
      exact (Nat.le_div_iff_mul_le (by omega)).mp hr_div
    have hr_le_T : r ≤ T := le_trans (Nat.le_mul_of_pos_left r (by omega)) hmr_le
    have hm_le_div : m ≤ T / r := (Nat.le_div_iff_mul_le (by omega)).mpr hmr_le
    exact ⟨⟨⟨hr1, hr_le_T⟩, hr_cop⟩, ⟨⟨hm1, hm_le_div⟩, hm_sm⟩⟩
  · rintro ⟨m1, r1⟩ _ ⟨m2, r2⟩ _ h_eq
    cases h_eq
    rfl
  · rintro ⟨r, m⟩ hrm
    simp only [S_mr, S_rm, Finset.mem_sigma, smoothCutoffFinset, coprimeCutoffFinset,
      Finset.mem_filter, Finset.mem_Icc] at hrm ⊢
    rcases hrm with ⟨⟨⟨hr1, _⟩, hr_cop⟩, ⟨⟨hm1, hm_div⟩, hm_sm⟩⟩
    have hmr_le : m * r ≤ T := (Nat.le_div_iff_mul_le (by omega)).mp hm_div
    have hm_le_T : m ≤ T := le_trans (Nat.le_mul_of_pos_right m (by omega)) hmr_le
    have hr_le_div : r ≤ T / m := (Nat.le_div_iff_mul_le (by omega)).mpr (by rw [mul_comm]; exact hmr_le)
    exact ⟨⟨m, r⟩, ⟨⟨⟨hm1, hm_le_T⟩, hm_sm⟩, ⟨⟨hr1, hr_le_div⟩, hr_cop⟩⟩, rfl⟩
  · intros; rfl

/-- **Theorem 15 (`TASK-TC-055R2` §3c, Arbitrary-Weight Reindexed Liouville Sum, Cofactor Regrouping, and Exact Uncoupled-Cutoff Excess)**:
    For every finite set of primes `P : Finset ℕ` (`∀ p ∈ P, p.Prime`), every `T : ℕ` (including `T = 0` and `T = 1`),
    and every real weight `w : ℕ → ℝ`:
    1. Smooth-outer / coprime-inner Liouville reconstruction:
       `∑_{1 ≤ n ≤ T} λ(n) w(n) = ∑_{m ≤ T, m ∈ S(P)} ∑_{1 ≤ r ≤ ⌊T/m⌋, gcd(r, N_P) = 1} λ(m) λ(r) w(m r)`;
    2. Regrouped coprime-outer / smooth-inner Liouville reconstruction:
       `∑_{1 ≤ n ≤ T} λ(n) w(n) = ∑_{1 ≤ r ≤ T, gcd(r, N_P) = 1} ∑_{m ≤ ⌊T/r⌋, m ∈ S(P)} λ(r) λ(m) w(m r)`;
    3. Exact uncoupled-cutoff excess sum when `r ≤ T` replaces `r ≤ ⌊T/m⌋`:
       `(∑_{m ≤ T, m ∈ S(P)} ∑_{1 ≤ r ≤ T, gcd(r, N_P) = 1} λ(m) λ(r) w(m r)) - (∑_{1 ≤ n ≤ T} λ(n) w(n))`
       `= ∑_{m ≤ T, m ∈ S(P)} ∑_{r ∈ excessCoprimeFinset P m T} λ(m) λ(r) w(m r)`;
    4. Vanishing vs. nonvanishing excess witnesses:
       - For `P = ∅` (any `T`), for `T ≤ 1` (any `P`), and even at `(P = {2}, T = 2)`, the excess sum is identically `0`
         (refuting any universal strict-inequality claim);
       - At `(P = {2}, T = 3)`, the excess sum equals `w 6` (strictly nonzero whenever `w 6 ≠ 0`). -/
theorem finite_liouville_reindexed_sum_and_excess_cutoff_identity_nat
    {P : Finset ℕ} (hP : ∀ p ∈ P, p.Prime) (T : ℕ) (w : ℕ → ℝ) :
    (∑ n ∈ Finset.Icc 1 T, (liouvilleLambda n : ℝ) * w n =
      ∑ m ∈ smoothCutoffFinset P T,
        ∑ r ∈ coprimeCutoffFinset P (T / m),
          (liouvilleLambda m : ℝ) * (liouvilleLambda r : ℝ) * w (m * r)) ∧
    (∑ n ∈ Finset.Icc 1 T, (liouvilleLambda n : ℝ) * w n =
      ∑ r ∈ coprimeCutoffFinset P T,
        ∑ m ∈ smoothCutoffFinset P (T / r),
          (liouvilleLambda r : ℝ) * (liouvilleLambda m : ℝ) * w (m * r)) ∧
    ((∑ m ∈ smoothCutoffFinset P T,
        ∑ r ∈ coprimeCutoffFinset P T,
          (liouvilleLambda m : ℝ) * (liouvilleLambda r : ℝ) * w (m * r)) -
      (∑ n ∈ Finset.Icc 1 T, (liouvilleLambda n : ℝ) * w n) =
      ∑ m ∈ smoothCutoffFinset P T,
        ∑ r ∈ excessCoprimeFinset P m T,
          (liouvilleLambda m : ℝ) * (liouvilleLambda r : ℝ) * w (m * r)) ∧
    ((∑ m ∈ smoothCutoffFinset ∅ T,
        ∑ r ∈ excessCoprimeFinset ∅ m T,
          (liouvilleLambda m : ℝ) * (liouvilleLambda r : ℝ) * w (m * r) = 0) ∧
      (T ≤ 1 →
        ∑ m ∈ smoothCutoffFinset P T,
          ∑ r ∈ excessCoprimeFinset P m T,
            (liouvilleLambda m : ℝ) * (liouvilleLambda r : ℝ) * w (m * r) = 0) ∧
      (∑ m ∈ smoothCutoffFinset {2} 2,
        ∑ r ∈ excessCoprimeFinset {2} m 2,
          (liouvilleLambda m : ℝ) * (liouvilleLambda r : ℝ) * w (m * r) = 0) ∧
      (∑ m ∈ smoothCutoffFinset {2} 3,
        ∑ r ∈ excessCoprimeFinset {2} m 3,
          (liouvilleLambda m : ℝ) * (liouvilleLambda r : ℝ) * w (m * r) = w 6)) := by
  have h_sm_out :
      ∑ n ∈ Finset.Icc 1 T, (liouvilleLambda n : ℝ) * w n =
        ∑ m ∈ smoothCutoffFinset P T,
          ∑ r ∈ coprimeCutoffFinset P (T / m),
            (liouvilleLambda m : ℝ) * (liouvilleLambda r : ℝ) * w (m * r) := by
    rw [sum_Icc_eq_smooth_outer_coprime_inner_aux hP T (fun n => (liouvilleLambda n : ℝ) * w n)]
    apply Finset.sum_congr rfl
    intro m hm
    have hm_ne : m ≠ 0 := by
      have hm_mem := (Finset.mem_filter.mp hm).1
      rw [Finset.mem_Icc] at hm_mem
      omega
    apply Finset.sum_congr rfl
    intro r hr
    have hr_ne : r ≠ 0 := by
      have hr_mem := (Finset.mem_filter.mp hr).1
      rw [Finset.mem_Icc] at hr_mem
      omega
    rw [liouvilleLambda_mul_aux hm_ne hr_ne]
    push_cast
    ring
  have h_cop_out :
      ∑ n ∈ Finset.Icc 1 T, (liouvilleLambda n : ℝ) * w n =
        ∑ r ∈ coprimeCutoffFinset P T,
          ∑ m ∈ smoothCutoffFinset P (T / r),
            (liouvilleLambda r : ℝ) * (liouvilleLambda m : ℝ) * w (m * r) := by
    rw [sum_Icc_eq_coprime_outer_smooth_inner_aux hP T (fun n => (liouvilleLambda n : ℝ) * w n)]
    apply Finset.sum_congr rfl
    intro r hr
    have hr_ne : r ≠ 0 := by
      have hr_mem := (Finset.mem_filter.mp hr).1
      rw [Finset.mem_Icc] at hr_mem
      omega
    apply Finset.sum_congr rfl
    intro m hm
    have hm_ne : m ≠ 0 := by
      have hm_mem := (Finset.mem_filter.mp hm).1
      rw [Finset.mem_Icc] at hm_mem
      omega
    rw [liouvilleLambda_mul_aux hm_ne hr_ne]
    push_cast
    ring
  refine ⟨h_sm_out, h_cop_out, ?_, ⟨?_, ?_, ?_, ?_⟩⟩
  · rw [h_sm_out, ← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro m hm
    have hm_mem := (Finset.mem_filter.mp hm).1
    rw [Finset.mem_Icc] at hm_mem
    have h_div_le : T / m ≤ T := Nat.div_le_self T m
    have h_union :
        coprimeCutoffFinset P T =
          coprimeCutoffFinset P (T / m) ∪ excessCoprimeFinset P m T := by
      ext r
      simp only [coprimeCutoffFinset, excessCoprimeFinset, Finset.mem_union, Finset.mem_filter,
        Finset.mem_Icc]
      constructor
      · rintro ⟨⟨hr1, hrT⟩, hcop⟩
        by_cases hr_le : r ≤ T / m
        · exact Or.inl ⟨⟨hr1, hr_le⟩, hcop⟩
        · exact Or.inr ⟨⟨by omega, hrT⟩, hcop⟩
      · rintro (⟨⟨hr1, hr_le⟩, hcop⟩ | ⟨⟨hr_gt, hrT⟩, hcop⟩)
        · exact ⟨⟨hr1, le_trans hr_le h_div_le⟩, hcop⟩
        · exact ⟨⟨le_trans (Nat.le_add_left 1 (T / m)) hr_gt, hrT⟩, hcop⟩
    have h_disj : Disjoint (coprimeCutoffFinset P (T / m)) (excessCoprimeFinset P m T) := by
      rw [Finset.disjoint_left]
      intro r hr1 hr2
      simp only [coprimeCutoffFinset, excessCoprimeFinset, Finset.mem_filter, Finset.mem_Icc] at hr1 hr2
      omega
    rw [h_union, Finset.sum_union h_disj]
    ring
  · apply Finset.sum_eq_zero
    intro m hm
    simp only [smoothCutoffFinset, Finset.mem_filter, isPSmooth_empty_iff_aux] at hm
    rcases hm with ⟨_, rfl⟩
    have hex_empty : excessCoprimeFinset ∅ 1 T = ∅ := by
      ext r
      simp [excessCoprimeFinset]
    rw [hex_empty, Finset.sum_empty]
  · intro hT_le1
    apply Finset.sum_eq_zero
    intro m hm
    have hm_mem := (Finset.mem_filter.mp hm).1
    rw [Finset.mem_Icc] at hm_mem
    have hm_eq1 : m = 1 := by omega
    have hT_eq1 : T = 1 := by omega
    subst hm_eq1; subst hT_eq1
    have hex_empty : excessCoprimeFinset P 1 1 = ∅ := by
      ext r
      simp [excessCoprimeFinset]
    rw [hex_empty, Finset.sum_empty]
  · have hs2 : smoothCutoffFinset {2} 2 = {1, 2} := by decide
    have hex1 : excessCoprimeFinset {2} 1 2 = ∅ := by decide
    have hex2 : excessCoprimeFinset {2} 2 2 = ∅ := by decide
    rw [hs2, Finset.sum_pair (by decide), hex1, hex2, Finset.sum_empty, Finset.sum_empty, add_zero]
  · have hs3 : smoothCutoffFinset {2} 3 = {1, 2} := by decide
    have hex1 : excessCoprimeFinset {2} 1 3 = ∅ := by decide
    have hex2 : excessCoprimeFinset {2} 2 3 = {3} := by decide
    have hl2 : liouvilleLambda 2 = -1 := by
      have ho2 : natOmega 2 = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr Nat.prime_two
      simp [liouvilleLambda, ho2, liouvilleSignFromOmega]
    have hl3 : liouvilleLambda 3 = -1 := by
      have ho3 : natOmega 3 = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr Nat.prime_three
      simp [liouvilleLambda, ho3, liouvilleSignFromOmega]
    rw [hs3, Finset.sum_pair (by decide), hex1, hex2, Finset.sum_empty, Finset.sum_singleton,
      zero_add, hl2, hl3]
    norm_num

/-- Helper: elementary `X^{5/2}` and `(n : ℝ)^{-3}` Gaussian scaling identity for `0 ≤ X` and `0 < a`, `0 < b`. -/
private theorem gaussian_term_scaling_aux {X : ℝ} (hX : 0 ≤ X) {a b : ℕ} (ha : 0 < a) :
    ((1 : ℝ) / Real.sqrt (a : ℝ)) *
        ((X / (a : ℝ)) ^ (5 / 2 : ℝ) *
          (((b : ℝ) ^ 3)⁻¹ * Real.exp (-((X / (a : ℝ)) ^ 2) / (b : ℝ) ^ 2))) =
      X ^ (5 / 2 : ℝ) *
        ((((a * b : ℕ) : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / ((a * b : ℕ) : ℝ) ^ 2)) := by
  have ha_real_pos : (0 : ℝ) < (a : ℝ) := Nat.cast_pos.mpr ha
  have ha_real_nonneg : (0 : ℝ) ≤ (a : ℝ) := le_of_lt ha_real_pos
  have ha_ne : (a : ℝ) ≠ 0 := ne_of_gt ha_real_pos
  have hsqrt_ne : Real.sqrt (a : ℝ) ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr ha_real_pos)
  have hrpow_div : (X / (a : ℝ)) ^ (5 / 2 : ℝ) = X ^ (5 / 2 : ℝ) / (a : ℝ) ^ (5 / 2 : ℝ) :=
    Real.div_rpow hX ha_real_nonneg (5 / 2 : ℝ)
  have hsqrt_mul_rpow : Real.sqrt (a : ℝ) * (a : ℝ) ^ (5 / 2 : ℝ) = (a : ℝ) ^ 3 := by
    rw [Real.sqrt_eq_rpow, ← Real.rpow_add ha_real_pos]
    have hexp : (1 / 2 : ℝ) + (5 / 2 : ℝ) = ((3 : ℕ) : ℝ) := by norm_num
    rw [hexp, Real.rpow_natCast]
  have hexp_arg : -((X / (a : ℝ)) ^ 2) / (b : ℝ) ^ 2 = -(X ^ 2) / ((a * b : ℕ) : ℝ) ^ 2 := by
    push_cast
    by_cases hb : (b : ℝ) = 0
    · simp [hb]
    · field_simp [ha_ne, hb]; left; ring
  rw [hrpow_div, hexp_arg]
  push_cast
  have hrpow_ne : (a : ℝ) ^ (5 / 2 : ℝ) ≠ 0 := ne_of_gt (Real.rpow_pos_of_pos ha_real_pos _)
  by_cases hb : (b : ℝ) = 0
  · simp [hb]
  · calc
      (1 / Real.sqrt (a : ℝ)) *
          (X ^ (5 / 2 : ℝ) / (a : ℝ) ^ (5 / 2 : ℝ) *
            (((b : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / ((a : ℝ) * (b : ℝ)) ^ 2)))
        = X ^ (5 / 2 : ℝ) *
            (((Real.sqrt (a : ℝ) * (a : ℝ) ^ (5 / 2 : ℝ)) * (b : ℝ) ^ 3)⁻¹ *
              Real.exp (-(X ^ 2) / ((a : ℝ) * (b : ℝ)) ^ 2)) := by
            field_simp [hsqrt_ne, hrpow_ne, hb]; left; ring
      _ = X ^ (5 / 2 : ℝ) *
            ((((a : ℝ) * (b : ℝ)) ^ 3)⁻¹ *
              Real.exp (-(X ^ 2) / ((a : ℝ) * (b : ℝ)) ^ 2)) := by
            rw [hsqrt_mul_rpow]
            ring

/-- **Theorem 16 (`TASK-TC-055R2` §2 & §3c, Finite Gaussian Observable Reconstruction and Weighted Cofactor Pointwise Square Expansion)**:
    For every finite set of primes `P : Finset ℕ` (`∀ p ∈ P, p.Prime`), every `T : ℕ`, and every `X : ℝ` with `0 ≤ X`:
    1. Smooth-outer reconstruction of `finiteQLambda T X`:
       `Q_{λ,T}(X) = ∑_{m ≤ T, m ∈ S(P)} (λ(m) / √m) · Q_{λ,P,⌊T/m⌋}(X / m)`;
    2. Regrouped coprime-outer `F_r(X)` reconstruction:
       `Q_{λ,T}(X) = ∑_{1 ≤ r ≤ T, gcd(r, N_P) = 1} cofactorFiberF P T r X`,
       where `cofactorFiberF P T r X = (λ(r) / √r) · Q_{λ,S(P),⌊T/r⌋}(X / r)`;
    3. Exact pointwise weighted cofactor square decomposition (with `1 / r` diagonal weight and
       `λ(r) λ(s) / √(r s)` ordered off-diagonal weight):
       `Q_{λ,T}(X)^2 = (∑_{1 ≤ r ≤ T, gcd(r, N_P) = 1} (1 / r) · Q_{λ,S(P),⌊T/r⌋}(X / r)^2)`
       `  + ∑_{1 ≤ r ≤ T, gcd(r, N_P) = 1} ∑_{s ∈ coprimeCutoffFinset P T \ {r}}`
       `      (λ(r) λ(s) / √(r s)) · Q_{λ,S(P),⌊T/r⌋}(X / r) · Q_{λ,S(P),⌊T/s⌋}(X / s)`;
    4. Degenerate conventions: `finiteQLambda 0 X = 0` and `finiteQLambdaCoprime ∅ T X = finiteQLambda T X`.
    *(Note: Integrating identity (3) against `dX / X` over `[Y, τ Y]` yields `E_{λ,T}(Y) = E_{same-r} + E_{diff-r}`
    by finite linearity of the Riemann/Bochner integral, derived analytically in the review.)* -/
theorem finite_gaussian_observable_reconstruction_and_weighted_cofactor_square
    {P : Finset ℕ} (hP : ∀ p ∈ P, p.Prime) (T : ℕ) {X : ℝ} (hX : 0 ≤ X) :
    (finiteQLambda T X =
      ∑ m ∈ smoothCutoffFinset P T,
        ((liouvilleLambda m : ℝ) / Real.sqrt (m : ℝ)) *
          finiteQLambdaCoprime P (T / m) (X / (m : ℝ))) ∧
    (finiteQLambda T X =
      ∑ r ∈ coprimeCutoffFinset P T, cofactorFiberF P T r X) ∧
    ((finiteQLambda T X) ^ 2 =
      (∑ r ∈ coprimeCutoffFinset P T,
        (1 / (r : ℝ)) * (finiteQLambdaSmooth P (T / r) (X / (r : ℝ))) ^ 2) +
      (∑ r ∈ coprimeCutoffFinset P T,
        ∑ s ∈ (coprimeCutoffFinset P T).erase r,
          ((liouvilleLambda r : ℝ) * (liouvilleLambda s : ℝ) / Real.sqrt ((r * s : ℕ) : ℝ)) *
            finiteQLambdaSmooth P (T / r) (X / (r : ℝ)) *
            finiteQLambdaSmooth P (T / s) (X / (s : ℝ)))) ∧
    (finiteQLambda 0 X = 0 ∧ finiteQLambdaCoprime ∅ T X = finiteQLambda T X) := by
  let w_gauss : ℕ → ℝ := fun n =>
    X ^ (5 / 2 : ℝ) * (((n : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (n : ℝ) ^ 2))
  have h_fQ_eq : finiteQLambda T X = ∑ n ∈ Finset.Icc 1 T, (liouvilleLambda n : ℝ) * w_gauss n := by
    dsimp [finiteQLambda, w_gauss]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro n _
    ring
  obtain ⟨h_sm_w, h_cop_w, _, _⟩ :=
    finite_liouville_reindexed_sum_and_excess_cutoff_identity_nat hP T w_gauss
  have h_part1 :
      finiteQLambda T X =
        ∑ m ∈ smoothCutoffFinset P T,
          ((liouvilleLambda m : ℝ) / Real.sqrt (m : ℝ)) *
            finiteQLambdaCoprime P (T / m) (X / (m : ℝ)) := by
    rw [h_fQ_eq, h_sm_w]
    apply Finset.sum_congr rfl
    intro m hm
    have hm_pos : 0 < m := ((Finset.mem_filter.mp hm).2).1
    dsimp [finiteQLambdaCoprime]
    rw [← mul_assoc, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro r _
    have h_sc := gaussian_term_scaling_aux (b := r) hX hm_pos
    dsimp [w_gauss]
    calc
      (liouvilleLambda m : ℝ) * (liouvilleLambda r : ℝ) *
          (X ^ (5 / 2 : ℝ) * ((((m * r : ℕ) : ℝ) ^ 3)⁻¹ *
            Real.exp (-(X ^ 2) / ((m * r : ℕ) : ℝ) ^ 2)))
        = (liouvilleLambda m : ℝ) * (liouvilleLambda r : ℝ) *
            (((1 : ℝ) / Real.sqrt (m : ℝ)) *
              ((X / (m : ℝ)) ^ (5 / 2 : ℝ) *
                (((r : ℝ) ^ 3)⁻¹ * Real.exp (-((X / (m : ℝ)) ^ 2) / (r : ℝ) ^ 2)))) := by
            rw [← h_sc]
      _ = (liouvilleLambda m : ℝ) / Real.sqrt (m : ℝ) *
            (X / (m : ℝ)) ^ (5 / 2 : ℝ) *
              ((liouvilleLambda r : ℝ) * ((r : ℝ) ^ 3)⁻¹ *
                Real.exp (-((X / (m : ℝ)) ^ 2) / (r : ℝ) ^ 2)) := by ring
  have h_part2 :
      finiteQLambda T X = ∑ r ∈ coprimeCutoffFinset P T, cofactorFiberF P T r X := by
    rw [h_fQ_eq, h_cop_w]
    apply Finset.sum_congr rfl
    intro r hr
    have hr_mem := (Finset.mem_filter.mp hr).1
    rw [Finset.mem_Icc] at hr_mem
    have hr_pos : 0 < r := by omega
    dsimp [cofactorFiberF, finiteQLambdaSmooth]
    rw [← mul_assoc, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro m _
    have h_sc := gaussian_term_scaling_aux (b := m) hX hr_pos
    have h_mr_comm : m * r = r * m := mul_comm m r
    dsimp [w_gauss]
    calc
      (liouvilleLambda r : ℝ) * (liouvilleLambda m : ℝ) *
          (X ^ (5 / 2 : ℝ) * ((((m * r : ℕ) : ℝ) ^ 3)⁻¹ *
            Real.exp (-(X ^ 2) / ((m * r : ℕ) : ℝ) ^ 2)))
        = (liouvilleLambda r : ℝ) * (liouvilleLambda m : ℝ) *
            (X ^ (5 / 2 : ℝ) * ((((r * m : ℕ) : ℝ) ^ 3)⁻¹ *
              Real.exp (-(X ^ 2) / ((r * m : ℕ) : ℝ) ^ 2))) := by
            rw [h_mr_comm]
      _ = (liouvilleLambda r : ℝ) * (liouvilleLambda m : ℝ) *
            (((1 : ℝ) / Real.sqrt (r : ℝ)) *
              ((X / (r : ℝ)) ^ (5 / 2 : ℝ) *
                (((m : ℝ) ^ 3)⁻¹ * Real.exp (-((X / (r : ℝ)) ^ 2) / (m : ℝ) ^ 2)))) := by
            rw [← h_sc]
      _ = (liouvilleLambda r : ℝ) / Real.sqrt (r : ℝ) *
            (X / (r : ℝ)) ^ (5 / 2 : ℝ) *
              ((liouvilleLambda m : ℝ) * ((m : ℝ) ^ 3)⁻¹ *
                Real.exp (-((X / (r : ℝ)) ^ 2) / (m : ℝ) ^ 2)) := by ring
  refine ⟨h_part1, h_part2, ?_, ?_⟩
  · rw [h_part2, sq, Finset.sum_mul_sum]
    have h_split :
        (∑ r ∈ coprimeCutoffFinset P T, ∑ s ∈ coprimeCutoffFinset P T,
            cofactorFiberF P T r X * cofactorFiberF P T s X) =
          (∑ r ∈ coprimeCutoffFinset P T, cofactorFiberF P T r X * cofactorFiberF P T r X) +
            ∑ r ∈ coprimeCutoffFinset P T, ∑ s ∈ (coprimeCutoffFinset P T).erase r,
              cofactorFiberF P T r X * cofactorFiberF P T s X := by
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro r hr
      exact (Finset.add_sum_erase (coprimeCutoffFinset P T)
        (fun s => cofactorFiberF P T r X * cofactorFiberF P T s X) hr).symm
    rw [h_split]
    congr 1
    · apply Finset.sum_congr rfl
      intro r hr
      have hr_mem := (Finset.mem_filter.mp hr).1
      rw [Finset.mem_Icc] at hr_mem
      have hr_ne : r ≠ 0 := by omega
      have hr_nonneg : (0 : ℝ) ≤ (r : ℝ) := Nat.cast_nonneg r
      have h_lam_sq : ((liouvilleLambda r : ℝ)) ^ 2 = 1 := by
        have h_int := liouvilleLambda_sq_aux hr_ne
        have h_cast : (liouvilleLambda r : ℝ) * (liouvilleLambda r : ℝ) = 1 := by exact_mod_cast h_int
        rw [sq, h_cast]
      have h_sqrt_sq : (Real.sqrt (r : ℝ)) ^ 2 = (r : ℝ) := Real.sq_sqrt hr_nonneg
      dsimp [cofactorFiberF]
      calc
        (liouvilleLambda r : ℝ) / Real.sqrt (r : ℝ) * finiteQLambdaSmooth P (T / r) (X / (r : ℝ)) *
            ((liouvilleLambda r : ℝ) / Real.sqrt (r : ℝ) * finiteQLambdaSmooth P (T / r) (X / (r : ℝ)))
          = (((liouvilleLambda r : ℝ)) ^ 2 / (Real.sqrt (r : ℝ)) ^ 2) *
              (finiteQLambdaSmooth P (T / r) (X / (r : ℝ))) ^ 2 := by ring
        _ = (1 / (r : ℝ)) * (finiteQLambdaSmooth P (T / r) (X / (r : ℝ))) ^ 2 := by
              rw [h_lam_sq, h_sqrt_sq]
    · apply Finset.sum_congr rfl
      intro r _
      apply Finset.sum_congr rfl
      intro s _
      have hr_nonneg : (0 : ℝ) ≤ (r : ℝ) := Nat.cast_nonneg r
      have h_sqrt_mul : Real.sqrt ((r * s : ℕ) : ℝ) = Real.sqrt (r : ℝ) * Real.sqrt (s : ℝ) := by
        push_cast
        exact Real.sqrt_mul hr_nonneg (s : ℝ)
      dsimp [cofactorFiberF]
      rw [h_sqrt_mul]
      ring
  · constructor
    · simp [finiteQLambda]
    · have hc_empty : coprimeCutoffFinset ∅ T = Finset.Icc 1 T := by
        ext r
        simp [coprimeCutoffFinset, primeProductModulus]
      simp [finiteQLambdaCoprime, finiteQLambda, hc_empty]

/-! ### `TASK-TC-056`: Finite Prime Filtration, Alternating-Unimodal Gaussian Chain Contraction, and `P`-Independent Mixed-Interaction Decomposition -/

/-- Positive single-integer Gaussian summand `φ_n(X) := X^{5/2} n^{-3} exp(-X^2 / n^2)` (`n : ℕ`). -/
noncomputable def gaussianTermPhi (n : ℕ) (X : ℝ) : ℝ :=
  X ^ (5 / 2 : ℝ) * (((n : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (n : ℝ) ^ 2))

/-- Pointwise grouped squared-fiber sum `v_P(X; T) := ∑_{1 ≤ r ≤ T, gcd(r, N_P) = 1} F_{P,r}(X)^2`
    (whose `dX / X` integral on `[Y, τ Y]` defines `V_P(Y, T)`). -/
noncomputable def pointwiseGroupedEnergyV (P : Finset ℕ) (T : ℕ) (X : ℝ) : ℝ :=
  ∑ r ∈ coprimeCutoffFinset P T, (cofactorFiberF P T r X) ^ 2

/-- Pointwise diagonal sum `d_T(X) := ∑_{1 ≤ n ≤ T} φ_n(X)^2`
    (whose `dX / X` integral on `[Y, τ Y]` defines `D_T(Y)`). -/
noncomputable def pointwiseDiagonalD (T : ℕ) (X : ℝ) : ℝ :=
  ∑ n ∈ Finset.Icc 1 T, (gaussianTermPhi n X) ^ 2

/-- Finite set of all primes `p ≤ T`. -/
def primesUpToFinset (T : ℕ) : Finset ℕ :=
  (Finset.Icc 2 T).filter Nat.Prime

/-- Strictly ascending list of all primes `p_1 < p_2 < ... < p_J ≤ T`. -/
def ascendingPrimesUpTo (T : ℕ) : List ℕ :=
  (List.range (T + 1)).filter Nat.Prime

/-- Prefix prime set `P_j := {p_1, ..., p_j}` (`P_0 = ∅`) of an ordered list of primes `ps`. -/
def prefixPrimeSet (ps : List ℕ) (j : ℕ) : Finset ℕ :=
  (ps.take j).toFinset

/-- Exact finite set of admissible prime exponents `{k ≥ 0 : s * p^k ≤ T}` for `s ≥ 1` and prime `p`. -/
def admissiblePrimeExponents (T p s : ℕ) : Finset ℕ :=
  (Finset.range (T + 1)).filter (fun k => s * p ^ k ≤ T)

/-- Pointwise prime-adjoining increment `δ_{P,p}(X; T) := v_{P ∪ {p}}(X; T) - v_P(X; T)`
    (whose `dX / X` integral on `[Y, τ Y]` defines `Δ_{P,p}(Y, T)`). -/
noncomputable def pointwiseDelta (P : Finset ℕ) (p T : ℕ) (X : ℝ) : ℝ :=
  pointwiseGroupedEnergyV (insert p P) T X - pointwiseGroupedEnergyV P T X

/-- Empty-safe finite maximum `max_{0 ≤ k < N} a_k` (`= 0` when `N = 0` or when all `a_k ≤ 0`). -/
noncomputable def chainMaxUpTo : ℕ → (ℕ → ℝ) → ℝ
  | 0, _ => 0
  | n + 1, a => max (chainMaxUpTo n a) (a n)

/-- Finite unimodality on `0, ..., N - 1`: there exists a peak index `k_peak ≤ N` up to which `a` is
    nondecreasing and from which `a` is nonincreasing (allowing ties, zero chains, `N = 0`, and `N = 1`). -/
def IsUnimodalChain (N : ℕ) (a : ℕ → ℝ) : Prop :=
  ∃ k_peak : ℕ, k_peak ≤ N ∧
    (∀ i j : ℕ, i ≤ j → j ≤ k_peak → j < N → a i ≤ a j) ∧
    (∀ i j : ℕ, k_peak ≤ i → i ≤ j → j < N → a j ≤ a i)

/-- Helper: `((-1 : ℝ) ^ m) * ((-1 : ℝ) ^ m) = 1`. -/
private theorem neg_one_pow_mul_self_real_aux (m : ℕ) :
    ((-1 : ℝ) ^ m) * ((-1 : ℝ) ^ m) = 1 := by
  rw [← pow_add]
  have h2 : m + m = 2 * m := by omega
  rw [h2, pow_mul]
  norm_num

/-- Helper: for `0 ≤ X` and `0 < r`, `cofactorFiberF P T r X` equals the coupled `P`-smooth sum
    `∑_{m ∈ S(P), m ≤ ⌊T/r⌋} λ(m r) φ_{m r}(X)`. -/
private theorem cofactorFiberF_eq_sum_gaussianTermPhi_aux
    (P : Finset ℕ) (T : ℕ) {r : ℕ} (hr : 0 < r) {X : ℝ} (hX : 0 ≤ X) :
    cofactorFiberF P T r X =
      ∑ m ∈ smoothCutoffFinset P (T / r),
        (liouvilleLambda (m * r) : ℝ) * gaussianTermPhi (m * r) X := by
  have hr_ne : r ≠ 0 := Nat.pos_iff_ne_zero.mp hr
  dsimp [cofactorFiberF, finiteQLambdaSmooth, gaussianTermPhi]
  rw [← mul_assoc, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro m hm
  have hm_pos : 0 < m := ((Finset.mem_filter.mp hm).2).1
  have hm_ne : m ≠ 0 := Nat.pos_iff_ne_zero.mp hm_pos
  have h_sc := gaussian_term_scaling_aux (a := r) (b := m) hX hr
  have h_comm : r * m = m * r := mul_comm r m
  rw [h_comm] at h_sc
  rw [liouvilleLambda_mul_aux hm_ne hr_ne]
  push_cast
  have h_lhs :
      (liouvilleLambda r : ℝ) / Real.sqrt (r : ℝ) * (X / (r : ℝ)) ^ (5 / 2 : ℝ) *
          ((liouvilleLambda m : ℝ) * ((m : ℝ) ^ 3)⁻¹ * Real.exp (-((X / (r : ℝ)) ^ 2) / (m : ℝ) ^ 2)) =
        (liouvilleLambda m : ℝ) * (liouvilleLambda r : ℝ) *
          (((1 : ℝ) / Real.sqrt (r : ℝ)) *
            ((X / (r : ℝ)) ^ (5 / 2 : ℝ) *
              (((m : ℝ) ^ 3)⁻¹ * Real.exp (-((X / (r : ℝ)) ^ 2) / (m : ℝ) ^ 2)))) := by ring
  rw [h_lhs]
  push_cast at h_sc
  rw [h_sc]

/-- Helper: exact characterization of `admissiblePrimeExponents T p s` for prime `p` and `1 ≤ s`. -/
private theorem mem_admissiblePrimeExponents_iff_aux {p s : ℕ} (hp : p.Prime) (hs : 1 ≤ s) (T k : ℕ) :
    k ∈ admissiblePrimeExponents T p s ↔ s * p ^ k ≤ T := by
  simp only [admissiblePrimeExponents, Finset.mem_filter, Finset.mem_range]
  constructor
  · exact And.right
  · intro h_le
    refine ⟨?_, h_le⟩
    have hk_lt_pow : k < p ^ k := Nat.lt_pow_self hp.one_lt k
    have hpow_le : p ^ k ≤ s * p ^ k := Nat.le_mul_of_pos_left (p ^ k) (by omega)
    omega

/-- Helper: `Nat.Coprime (a * b) c` from `Nat.Coprime a c` and `Nat.Coprime b c`. -/
private theorem coprime_mul_left_nat_aux {a b c : ℕ}
    (ha : Nat.Coprime a c) (hb : Nat.Coprime b c) : Nat.Coprime (a * b) c := by
  rw [Nat.coprime_iff_gcd_eq_one]
  by_contra h_ne
  obtain ⟨q, hq_prime, hq_dvd⟩ := Nat.exists_prime_and_dvd h_ne
  have hq_ab : q ∣ a * b := dvd_trans hq_dvd (Nat.gcd_dvd_left _ _)
  have hq_c : q ∣ c := dvd_trans hq_dvd (Nat.gcd_dvd_right _ _)
  rcases hq_prime.dvd_mul.mp hq_ab with hqa | hqb
  · exact hq_prime.not_dvd_one (ha.gcd_eq_one ▸ Nat.dvd_gcd hqa hq_c)
  · exact hq_prime.not_dvd_one (hb.gcd_eq_one ▸ Nat.dvd_gcd hqb hq_c)

/-- Helper: `pSmoothPart {p} n = p ^ (n.factorization p)` for prime `p` and `n > 0`. -/
private theorem pSmoothPart_singleton_eq_pow_aux {p n : ℕ} (hp : p.Prime) (hn : 0 < n) :
    pSmoothPart {p} n = p ^ (n.factorization p) := by
  have hn_ne : n ≠ 0 := Nat.pos_iff_ne_zero.mp hn
  dsimp [pSmoothPart]
  by_cases hp_mem_pf : p ∈ n.primeFactors
  · have hfilt : n.primeFactors.filter (· ∈ ({p} : Finset ℕ)) = {p} := by
      ext q
      simp only [Finset.mem_filter, Finset.mem_singleton]
      exact ⟨fun h => h.2, fun h => ⟨h ▸ hp_mem_pf, h⟩⟩
    rw [hfilt, Finset.prod_singleton]
  · have hfilt : n.primeFactors.filter (· ∈ ({p} : Finset ℕ)) = ∅ := by
      ext q
      simp only [Finset.mem_filter, Finset.mem_singleton, Finset.not_mem_empty, iff_false]
      rintro ⟨hq_pf, rfl⟩
      exact hp_mem_pf hq_pf
    have h_not_dvd : ¬ (p ∣ n) := by
      intro hdvd
      exact hp_mem_pf (Nat.mem_primeFactors.mpr ⟨hp, hdvd, hn_ne⟩)
    have hk0 : n.factorization p = 0 := Nat.factorization_eq_zero_of_not_dvd h_not_dvd
    rw [hfilt, Finset.prod_empty, hk0, pow_zero]

/-- Helper: `primeProductModulus (insert p P) = p * primeProductModulus P` when `p ∉ P`. -/
private theorem primeProductModulus_insert_aux {P : Finset ℕ} {p : ℕ} (hp_not_mem : p ∉ P) :
    primeProductModulus (insert p P) = p * primeProductModulus P := by
  dsimp [primeProductModulus]
  exact Finset.prod_insert hp_not_mem

/-- Helper: `Nat.Coprime a (primeProductModulus (insert p P)) ↔ Nat.Coprime a p ∧ Nat.Coprime a (primeProductModulus P)`
    when `p ∉ P`. -/
private theorem coprime_primeProductModulus_insert_iff_aux {P : Finset ℕ} {p : ℕ} (hp_not_mem : p ∉ P) (a : ℕ) :
    Nat.Coprime a (primeProductModulus (insert p P)) ↔
      Nat.Coprime a p ∧ Nat.Coprime a (primeProductModulus P) := by
  rw [primeProductModulus_insert_aux hp_not_mem, Nat.coprime_mul_iff_right]

/-- Helper: bijection partitioning `coprimeCutoffFinset P T` into `(s, k)` with
    `s ∈ coprimeCutoffFinset (insert p P) T` and `k ∈ admissiblePrimeExponents T p s` via `r = s * p^k`. -/
private theorem sum_coprimeCutoffFinset_insert_partition_aux
    {P : Finset ℕ} (hP : ∀ q ∈ P, q.Prime) {p : ℕ} (hp : p.Prime) (hp_not_mem : p ∉ P)
    (T : ℕ) (F : ℕ → ℝ) :
    ∑ r ∈ coprimeCutoffFinset P T, F r =
      ∑ s ∈ coprimeCutoffFinset (insert p P) T,
        ∑ k ∈ admissiblePrimeExponents T p s, F (s * p ^ k) := by
  have hp_set : ∀ q ∈ ({p} : Finset ℕ), q.Prime := by
    intro q hq
    rw [Finset.mem_singleton] at hq
    rwa [hq]
  have hp_cop_mod : Nat.Coprime p (primeProductModulus P) := by
    rw [hp.coprime_iff_not_dvd]
    intro hdvd
    obtain ⟨q, hq_in_P, hp_dvd_q⟩ := prime_dvd_finset_prod_aux hp P (fun x => x) hdvd
    have hq_prime : q.Prime := hP q hq_in_P
    have hpq : p = q := (Nat.dvd_prime hq_prime).mp hp_dvd_q |>.resolve_left hp.ne_one
    exact hp_not_mem (hpq ▸ hq_in_P)
  rw [Finset.sum_sigma' (coprimeCutoffFinset (insert p P) T) (fun s => admissiblePrimeExponents T p s)
        (fun s k => F (s * p ^ k))]
  symm
  apply Finset.sum_bij (fun sk _ => sk.1 * p ^ sk.2)
  · rintro ⟨s, k⟩ hsk
    simp only [Finset.mem_sigma, coprimeCutoffFinset, Finset.mem_filter, Finset.mem_Icc] at hsk ⊢
    rcases hsk with ⟨⟨⟨hs1, _⟩, hs_cop_ins⟩, hk_adm⟩
    have h_spk_le : s * p ^ k ≤ T := (mem_admissiblePrimeExponents_iff_aux hp hs1 T k).mp hk_adm
    have h_spk_ge : 1 ≤ s * p ^ k := Nat.mul_pos (by omega) (pow_pos hp.pos k)
    have hs_cop_P : Nat.Coprime s (primeProductModulus P) :=
      ((coprime_primeProductModulus_insert_iff_aux hp_not_mem s).mp hs_cop_ins).2
    have hpk_cop_P : Nat.Coprime (p ^ k) (primeProductModulus P) := hp_cop_mod.pow_left k
    exact ⟨⟨h_spk_ge, h_spk_le⟩, coprime_mul_left_nat_aux hs_cop_P hpk_cop_P⟩
  · rintro ⟨s1, k1⟩ h1 ⟨s2, k2⟩ h2 h_eq
    simp only [Finset.mem_sigma, coprimeCutoffFinset, Finset.mem_filter, Finset.mem_Icc] at h1 h2
    rcases h1 with ⟨⟨⟨hs1_ge, _⟩, hs1_cop⟩, _⟩
    rcases h2 with ⟨⟨⟨_, _⟩, hs2_cop⟩, _⟩
    have hs1_cop_p : Nat.Coprime s1 (primeProductModulus {p}) := by
      simpa [primeProductModulus] using ((coprime_primeProductModulus_insert_iff_aux hp_not_mem s1).mp hs1_cop).1
    have hs2_cop_p : Nat.Coprime s2 (primeProductModulus {p}) := by
      simpa [primeProductModulus] using ((coprime_primeProductModulus_insert_iff_aux hp_not_mem s2).mp hs2_cop).1
    have hpk1_sm : isPSmooth {p} (p ^ k1) := by
      refine ⟨pow_pos hp.pos k1, ?_⟩
      intro q hq hdvd
      have hq_dvd_p : q ∣ p := hq.dvd_of_dvd_pow hdvd
      have hqp : q = p := (Nat.dvd_prime hp).mp hq_dvd_p |>.resolve_left hq.ne_one
      exact Finset.mem_singleton.mpr hqp
    have hpk2_sm : isPSmooth {p} (p ^ k2) := by
      refine ⟨pow_pos hp.pos k2, ?_⟩
      intro q hq hdvd
      have hq_dvd_p : q ∣ p := hq.dvd_of_dvd_pow hdvd
      have hqp : q = p := (Nat.dvd_prime hp).mp hq_dvd_p |>.resolve_left hq.ne_one
      exact Finset.mem_singleton.mpr hqp
    have h_pos : 0 < p ^ k1 * s1 := Nat.mul_pos (pow_pos hp.pos k1) (by omega)
    obtain ⟨_, h_uniq, _⟩ := smooth_coprime_positive_factorization_exists_unique_nat hp_set h_pos
    obtain ⟨h_sm1, h_cp1⟩ := h_uniq (p ^ k1) s1 rfl hpk1_sm hs1_cop_p
    have h_eq_comm : p ^ k2 * s2 = p ^ k1 * s1 := by linarith [mul_comm s1 (p ^ k1), mul_comm s2 (p ^ k2)]
    obtain ⟨h_sm2, h_cp2⟩ := h_uniq (p ^ k2) s2 h_eq_comm hpk2_sm hs2_cop_p
    have hs_eq : s1 = s2 := h_cp1.trans h_cp2.symm
    have hpow_eq : p ^ k1 = p ^ k2 := h_sm1.trans h_sm2.symm
    have hk_eq : k1 = k2 := Nat.pow_right_injective hp.two_le hpow_eq
    exact Sigma.ext hs_eq (heq_of_eq hk_eq)
  · intro r hr
    simp only [coprimeCutoffFinset, Finset.mem_filter, Finset.mem_Icc] at hr
    rcases hr with ⟨⟨hr1, hrT⟩, hr_cop_P⟩
    let k := r.factorization p
    let s := pCoprimePart {p} r
    have hm_eq_pk : pSmoothPart {p} r = p ^ k := pSmoothPart_singleton_eq_pow_aux hp (by omega)
    obtain ⟨⟨h_mul_r, _, hs_cop_p, hs_pos⟩, _, _⟩ :=
      smooth_coprime_positive_factorization_exists_unique_nat hp_set (n := r) (by omega)
    rw [hm_eq_pk] at h_mul_r
    have hs_mul_pk : s * p ^ k = r := by rw [mul_comm]; exact h_mul_r
    have hs_dvd_r : s ∣ r := ⟨p ^ k, hs_mul_pk.symm⟩
    have hs_cop_P : Nat.Coprime s (primeProductModulus P) := hr_cop_P.coprime_dvd_left hs_dvd_r
    have hs_cop_p_plain : Nat.Coprime s p := by simpa [primeProductModulus] using hs_cop_p
    have hs_cop_ins : Nat.Coprime s (primeProductModulus (insert p P)) :=
      (coprime_primeProductModulus_insert_iff_aux hp_not_mem s).mpr ⟨hs_cop_p_plain, hs_cop_P⟩
    have hs_le_r : s ≤ r := by
      rw [← hs_mul_pk]
      exact Nat.le_mul_of_pos_right s (pow_pos hp.pos k)
    refine ⟨⟨s, k⟩, ?_, hs_mul_pk⟩
    simp only [Finset.mem_sigma, coprimeCutoffFinset, Finset.mem_filter, Finset.mem_Icc]
    refine ⟨⟨⟨by omega, le_trans hs_le_r hrT⟩, hs_cop_ins⟩, ?_⟩
    exact (mem_admissiblePrimeExponents_iff_aux hp (by omega) T k).mpr (hs_mul_pk.symm ▸ hrT)
  · intros; rfl

/-- Helper: bijection partitioning `smoothCutoffFinset (insert p P) L` into `(k, m)` with
    `k ∈ admissiblePrimeExponents L p 1` and `m ∈ smoothCutoffFinset P (L / p^k)` via `M = m * p^k`. -/
private theorem sum_smoothCutoffFinset_insert_partition_aux
    {P : Finset ℕ} (_ : ∀ q ∈ P, q.Prime) {p : ℕ} (hp : p.Prime) (hp_not_mem : p ∉ P)
    (L : ℕ) (F : ℕ → ℝ) :
    ∑ M ∈ smoothCutoffFinset (insert p P) L, F M =
      ∑ k ∈ admissiblePrimeExponents L p 1,
        ∑ m ∈ smoothCutoffFinset P (L / p ^ k), F (m * p ^ k) := by
  have hp_set : ∀ q ∈ ({p} : Finset ℕ), q.Prime := by
    intro q hq
    rw [Finset.mem_singleton] at hq
    rwa [hq]
  rw [Finset.sum_sigma' (admissiblePrimeExponents L p 1) (fun k => smoothCutoffFinset P (L / p ^ k))
        (fun k m => F (m * p ^ k))]
  symm
  apply Finset.sum_bij (fun km _ => km.2 * p ^ km.1)
  · rintro ⟨k, m⟩ hkm
    simp only [Finset.mem_sigma, smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc] at hkm ⊢
    rcases hkm with ⟨_, ⟨⟨hm1, hm_le_div⟩, hm_sm⟩⟩
    have hpk_pos : 0 < p ^ k := pow_pos hp.pos k
    have h_mpk_le : m * p ^ k ≤ L := (Nat.le_div_iff_mul_le hpk_pos).mp hm_le_div
    have h_mpk_ge : 1 ≤ m * p ^ k := Nat.mul_pos (by omega) hpk_pos
    refine ⟨⟨h_mpk_ge, h_mpk_le⟩, ⟨by omega, ?_⟩⟩
    intro q hq hdvd
    rcases hq.dvd_mul.mp hdvd with hqm | hqpk
    · exact Finset.mem_insert_of_mem (hm_sm.2 q hq hqm)
    · have hq_dvd_p : q ∣ p := hq.dvd_of_dvd_pow hqpk
      have hqp : q = p := (Nat.dvd_prime hp).mp hq_dvd_p |>.resolve_left hq.ne_one
      exact hqp ▸ Finset.mem_insert_self p P
  · rintro ⟨k1, m1⟩ h1 ⟨k2, m2⟩ h2 h_eq
    simp only [Finset.mem_sigma, smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc] at h1 h2
    rcases h1 with ⟨_, ⟨⟨hm1_ge, _⟩, hm1_sm⟩⟩
    rcases h2 with ⟨_, ⟨⟨_, _⟩, hm2_sm⟩⟩
    have hm1_cop_p : Nat.Coprime m1 (primeProductModulus {p}) := by
      simp only [primeProductModulus, Finset.prod_singleton]
      rw [Nat.coprime_comm, hp.coprime_iff_not_dvd]
      intro hdvd
      exact hp_not_mem (hm1_sm.2 p hp hdvd)
    have hm2_cop_p : Nat.Coprime m2 (primeProductModulus {p}) := by
      simp only [primeProductModulus, Finset.prod_singleton]
      rw [Nat.coprime_comm, hp.coprime_iff_not_dvd]
      intro hdvd
      exact hp_not_mem (hm2_sm.2 p hp hdvd)
    have hpk1_sm : isPSmooth {p} (p ^ k1) := by
      refine ⟨pow_pos hp.pos k1, ?_⟩
      intro q hq hdvd
      have hqp : q = p := (Nat.dvd_prime hp).mp (hq.dvd_of_dvd_pow hdvd) |>.resolve_left hq.ne_one
      exact Finset.mem_singleton.mpr hqp
    have hpk2_sm : isPSmooth {p} (p ^ k2) := by
      refine ⟨pow_pos hp.pos k2, ?_⟩
      intro q hq hdvd
      have hqp : q = p := (Nat.dvd_prime hp).mp (hq.dvd_of_dvd_pow hdvd) |>.resolve_left hq.ne_one
      exact Finset.mem_singleton.mpr hqp
    have h_pos : 0 < p ^ k1 * m1 := Nat.mul_pos (pow_pos hp.pos k1) (by omega)
    obtain ⟨_, h_uniq, _⟩ := smooth_coprime_positive_factorization_exists_unique_nat hp_set h_pos
    obtain ⟨h_sm1, h_cp1⟩ := h_uniq (p ^ k1) m1 rfl hpk1_sm hm1_cop_p
    have h_eq_comm : p ^ k2 * m2 = p ^ k1 * m1 := by linarith [mul_comm m1 (p ^ k1), mul_comm m2 (p ^ k2)]
    obtain ⟨h_sm2, h_cp2⟩ := h_uniq (p ^ k2) m2 h_eq_comm hpk2_sm hm2_cop_p
    have hm_eq : m1 = m2 := h_cp1.trans h_cp2.symm
    have hk_eq : k1 = k2 := Nat.pow_right_injective hp.two_le (h_sm1.trans h_sm2.symm)
    exact Sigma.ext hk_eq (heq_of_eq hm_eq)
  · intro M hM
    simp only [smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc] at hM
    rcases hM with ⟨⟨hM1, hML⟩, hM_sm_ins⟩
    let k := M.factorization p
    let m := pCoprimePart {p} M
    have hm_eq_pk : pSmoothPart {p} M = p ^ k := pSmoothPart_singleton_eq_pow_aux hp (by omega)
    obtain ⟨⟨h_mul_M, _, hm_cop_p, hm_pos⟩, _, _⟩ :=
      smooth_coprime_positive_factorization_exists_unique_nat hp_set (n := M) (by omega)
    rw [hm_eq_pk] at h_mul_M
    have hm_mul_pk : m * p ^ k = M := by rw [mul_comm]; exact h_mul_M
    have hm_sm_P : isPSmooth P m := by
      refine ⟨hm_pos, ?_⟩
      intro q hq hdvd
      have hq_dvd_M : q ∣ M := dvd_trans hdvd ⟨p ^ k, hm_mul_pk.symm⟩
      have hq_ins : q ∈ insert p P := hM_sm_ins.2 q hq hq_dvd_M
      have hq_ne_p : q ≠ p := by
        intro hqp
        subst hqp
        have hcop_plain : Nat.Coprime m q := by simpa [primeProductModulus] using hm_cop_p
        exact hq.not_dvd_one (hcop_plain.gcd_eq_one ▸ Nat.dvd_gcd hdvd (dvd_refl q))
      exact (Finset.mem_insert.mp hq_ins).resolve_left hq_ne_p
    have hpk_le_M : p ^ k ≤ M := by
      rw [← hm_mul_pk]
      exact Nat.le_mul_of_pos_left (p ^ k) hm_pos
    have hm_le_div : m ≤ L / p ^ k :=
      (Nat.le_div_iff_mul_le (pow_pos hp.pos k)).mpr (hm_mul_pk.symm ▸ hML)
    refine ⟨⟨k, m⟩, ?_, hm_mul_pk⟩
    simp only [Finset.mem_sigma, smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc]
    refine ⟨?_, ⟨⟨by omega, hm_le_div⟩, hm_sm_P⟩⟩
    exact (mem_admissiblePrimeExponents_iff_aux hp (by omega) L k).mpr (by simpa using le_trans hpk_le_M hML)
  · intros; rfl

/-- Helper: `prefixPrimeSet ps (m + 1) = insert (ps.getD m 0) (prefixPrimeSet ps m)` for `m < ps.length`. -/
private theorem prefixPrimeSet_succ_aux :
    ∀ (ps : List ℕ) (m : ℕ), m < ps.length →
      prefixPrimeSet ps (m + 1) = insert (ps.getD m 0) (prefixPrimeSet ps m)
  | [], _, hm => by simp at hm
  | x :: xs, 0, _ => by simp [prefixPrimeSet]
  | x :: xs, m + 1, hm => by
      have hm_xs : m < xs.length := by simpa using hm
      have ih := prefixPrimeSet_succ_aux xs m hm_xs
      dsimp [prefixPrimeSet, List.take, List.getD] at ih ⊢
      rw [List.toFinset_cons, List.toFinset_cons, ih]
      ext a
      simp only [Finset.mem_insert]
      tauto

/-- Helper: symmetric off-diagonal square expansion on any `Finset ℕ`:
    `(∑ k ∈ S, f k)^2 - ∑ k ∈ S, (f k)^2 = 2 * ∑ k ∈ S, ∑ l ∈ S.filter (fun l => k < l), f k * f l`. -/
private theorem sq_sum_sub_sum_sq_eq_two_sum_lt_aux (S : Finset ℕ) (f : ℕ → ℝ) :
    (∑ k ∈ S, f k) ^ 2 - (∑ k ∈ S, (f k) ^ 2) =
      2 * ∑ k ∈ S, ∑ l ∈ S.filter (fun l => k < l), f k * f l := by
  induction' S using Finset.induction_on with a s ha ih
  · simp
  · rw [Finset.sum_insert ha, Finset.sum_insert ha]
    have h_diff :
        (f a + ∑ k ∈ s, f k) ^ 2 - ((f a) ^ 2 + ∑ k ∈ s, (f k) ^ 2) =
          2 * f a * (∑ k ∈ s, f k) + ((∑ k ∈ s, f k) ^ 2 - ∑ k ∈ s, (f k) ^ 2) := by ring
    rw [h_diff, ih, Finset.sum_insert ha]
    have h_split_s :
        ∑ k ∈ s, f k =
          (∑ l ∈ s.filter (fun l => a < l), f l) +
            (∑ k ∈ s.filter (fun k => k < a), f k) := by
      have h_part := (Finset.sum_filter_add_sum_filter_not s (fun l => a < l) f).symm
      rw [h_part]
      congr 1
      apply Finset.sum_congr
      · ext k
        simp only [Finset.mem_filter]
        constructor
        · rintro ⟨hk, hnot⟩
          have hne : k ≠ a := fun h => ha (h ▸ hk)
          exact ⟨hk, by omega⟩
        · rintro ⟨hk, hlt⟩
          exact ⟨hk, by omega⟩
      · intros; rfl
    have h_filter_a :
        (insert a s).filter (fun l => a < l) = s.filter (fun l => a < l) := by
      ext l
      simp only [Finset.mem_filter, Finset.mem_insert]
      constructor
      · rintro ⟨rfl | hl, hlt⟩
        · omega
        · exact ⟨hl, hlt⟩
      · rintro ⟨hl, hlt⟩
        exact ⟨Or.inr hl, hlt⟩
    have h_sum_s_ins :
        ∑ k ∈ s, ∑ l ∈ (insert a s).filter (fun l => k < l), f k * f l =
          (∑ k ∈ s.filter (fun k => k < a), f k * f a) +
            ∑ k ∈ s, ∑ l ∈ s.filter (fun l => k < l), f k * f l := by
      rw [Finset.sum_filter]
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro k _
      by_cases hka : k < a
      · have h_ins_filt : (insert a s).filter (fun l => k < l) = insert a (s.filter (fun l => k < l)) := by
          ext l
          simp only [Finset.mem_filter, Finset.mem_insert]
          constructor
          · rintro ⟨rfl | hl, hlt⟩
            · exact Or.inl rfl
            · exact Or.inr ⟨hl, hlt⟩
          · rintro (rfl | ⟨hl, hlt⟩)
            · exact ⟨Or.inl rfl, hka⟩
            · exact ⟨Or.inr hl, hlt⟩
        have ha_not_filt : a ∉ s.filter (fun l => k < l) := by
          simp [ha]
        rw [if_pos hka, h_ins_filt, Finset.sum_insert ha_not_filt]
      · have h_ins_filt : (insert a s).filter (fun l => k < l) = s.filter (fun l => k < l) := by
          ext l
          simp only [Finset.mem_filter, Finset.mem_insert]
          constructor
          · rintro ⟨rfl | hl, hlt⟩
            · exact False.elim (hka hlt)
            · exact ⟨hl, hlt⟩
          · rintro ⟨hl, hlt⟩
            exact ⟨Or.inr hl, hlt⟩
        rw [if_neg hka, zero_add, h_ins_filt]
    rw [h_filter_a, h_sum_s_ins, h_split_s]
    have h_fa_lt : f a * ∑ l ∈ s.filter (fun l => a < l), f l =
        ∑ l ∈ s.filter (fun l => a < l), f a * f l := Finset.mul_sum _ _ _
    have h_fa_gt : f a * ∑ k ∈ s.filter (fun k => k < a), f k =
        ∑ k ∈ s.filter (fun k => k < a), f k * f a := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro k _; ring
    linarith

/-- **Theorem 17 (`TASK-TC-056` §3, Finite Prime Filtration Endpoints, Prime-Adjoining Fiber Identity, Pointwise Increment, and Ascending-Prime Telescoping)**:
    For every finite set of primes `P : Finset ℕ` (`∀ q ∈ P, q.Prime`), prime `p ∉ P`, cutoff `T : ℕ`,
    and `X : ℝ` with `0 ≤ X`:
    1. Exact filtration endpoints:
       `pointwiseGroupedEnergyV ∅ T X = pointwiseDiagonalD T X` and
       `pointwiseGroupedEnergyV (primesUpToFinset T) T X = (finiteQLambda T X) ^ 2`;
    2. Exact coupled prime-adjoining fiber identity (`s ∈ coprimeCutoffFinset (insert p P) T`):
       `∀ k, k ∈ admissiblePrimeExponents T p s ↔ s * p ^ k ≤ T`, and
       `cofactorFiberF (insert p P) T s X = ∑ k ∈ admissiblePrimeExponents T p s, cofactorFiberF P T (s * p ^ k) X`;
    3. Exact pointwise increment identity:
       `pointwiseDelta P p T X = 2 * ∑ s ∈ coprimeCutoffFinset (insert p P) T, ∑ k ∈ admissiblePrimeExponents T p s, ∑ l ∈ (admissiblePrimeExponents T p s).filter (fun l => k < l), cofactorFiberF P T (s * p ^ k) X * cofactorFiberF P T (s * p ^ l) X`;
    4. Exact ascending-prime filtration telescoping along `ps := ascendingPrimesUpTo T` (`p_1 < ... < p_J ≤ T`):
       `ps.Pairwise (· < ·)`, `ps.toFinset = primesUpToFinset T`, and
       `(finiteQLambda T X) ^ 2 = pointwiseDiagonalD T X + ∑ j ∈ Finset.range ps.length, pointwiseDelta (prefixPrimeSet ps j) (ps.getD j 0) T X`. -/
theorem finite_prime_adjoining_fiber_and_pointwise_telescoping_tc056
    {P : Finset ℕ} (hP : ∀ q ∈ P, q.Prime) {p : ℕ} (hp : p.Prime) (hp_not_mem : p ∉ P)
    (T : ℕ) {X : ℝ} (hX : 0 ≤ X) :
    (pointwiseGroupedEnergyV ∅ T X = pointwiseDiagonalD T X ∧
      pointwiseGroupedEnergyV (primesUpToFinset T) T X = (finiteQLambda T X) ^ 2) ∧
    (∀ s ∈ coprimeCutoffFinset (insert p P) T,
      (∀ k : ℕ, k ∈ admissiblePrimeExponents T p s ↔ s * p ^ k ≤ T) ∧
        cofactorFiberF (insert p P) T s X =
          ∑ k ∈ admissiblePrimeExponents T p s, cofactorFiberF P T (s * p ^ k) X) ∧
    (pointwiseDelta P p T X =
      2 * ∑ s ∈ coprimeCutoffFinset (insert p P) T,
        ∑ k ∈ admissiblePrimeExponents T p s,
          ∑ l ∈ (admissiblePrimeExponents T p s).filter (fun l => k < l),
            cofactorFiberF P T (s * p ^ k) X * cofactorFiberF P T (s * p ^ l) X) ∧
    ((ascendingPrimesUpTo T).Pairwise (· < ·) ∧
      (ascendingPrimesUpTo T).toFinset = primesUpToFinset T ∧
      (finiteQLambda T X) ^ 2 =
        pointwiseDiagonalD T X +
          ∑ j ∈ Finset.range (ascendingPrimesUpTo T).length,
            pointwiseDelta (prefixPrimeSet (ascendingPrimesUpTo T) j)
              ((ascendingPrimesUpTo T).getD j 0) T X) := by
  have h_end_empty : pointwiseGroupedEnergyV ∅ T X = pointwiseDiagonalD T X := by
    dsimp [pointwiseGroupedEnergyV, pointwiseDiagonalD]
    have hc_empty : coprimeCutoffFinset ∅ T = Finset.Icc 1 T := by
      ext r
      simp [coprimeCutoffFinset, primeProductModulus]
    rw [hc_empty]
    apply Finset.sum_congr rfl
    intro r hr
    rw [Finset.mem_Icc] at hr
    have hr_pos : 0 < r := by omega
    have hr_ne : r ≠ 0 := by omega
    rw [cofactorFiberF_eq_sum_gaussianTermPhi_aux ∅ T hr_pos hX]
    have hdiv_ge1 : 1 ≤ T / r := (Nat.le_div_iff_mul_le hr_pos).mpr (by omega)
    have hs_empty : smoothCutoffFinset ∅ (T / r) = {1} := by
      ext m
      simp only [smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc, isPSmooth_empty_iff_aux,
        Finset.mem_singleton]
      exact ⟨fun h => h.2, fun h => ⟨⟨by omega, by omega⟩, h⟩⟩
    rw [hs_empty, Finset.sum_singleton, one_mul]
    have h_lam_sq : ((liouvilleLambda r : ℝ)) ^ 2 = 1 := by
      have h_int := liouvilleLambda_sq_aux hr_ne
      have h_cast : (liouvilleLambda r : ℝ) * (liouvilleLambda r : ℝ) = 1 := by exact_mod_cast h_int
      rw [sq, h_cast]
    calc
      ((liouvilleLambda r : ℝ) * gaussianTermPhi r X) ^ 2
        = ((liouvilleLambda r : ℝ)) ^ 2 * (gaussianTermPhi r X) ^ 2 := by ring
      _ = (gaussianTermPhi r X) ^ 2 := by rw [h_lam_sq, one_mul]
  have h_primes_all : ∀ q ∈ primesUpToFinset T, q.Prime := by
    intro q hq
    exact (Finset.mem_filter.mp hq).2
  have h_end_all : pointwiseGroupedEnergyV (primesUpToFinset T) T X = (finiteQLambda T X) ^ 2 := by
    obtain ⟨_, h_rec_f, _, ⟨hf0, _⟩⟩ :=
      finite_gaussian_observable_reconstruction_and_weighted_cofactor_square h_primes_all T hX
    by_cases hT : 1 ≤ T
    · have hc_all : coprimeCutoffFinset (primesUpToFinset T) T = {1} := by
        ext r
        simp only [coprimeCutoffFinset, Finset.mem_filter, Finset.mem_Icc, Finset.mem_singleton]
        constructor
        · rintro ⟨⟨hr1, hrT⟩, hcop⟩
          by_contra hr_ne1
          obtain ⟨q, hq_prime, hq_dvd_r⟩ := Nat.exists_prime_and_dvd hr_ne1
          have hq_le_r : q ≤ r := Nat.le_of_dvd (by omega) hq_dvd_r
          have hq_mem : q ∈ primesUpToFinset T := by
            simp only [primesUpToFinset, Finset.mem_filter, Finset.mem_Icc]
            exact ⟨⟨hq_prime.two_le, le_trans hq_le_r hrT⟩, hq_prime⟩
          have hq_dvd_mod : q ∣ primeProductModulus (primesUpToFinset T) :=
            Finset.dvd_prod_of_mem (fun x => x) hq_mem
          exact hq_prime.not_dvd_one (hcop.gcd_eq_one ▸ Nat.dvd_gcd hq_dvd_r hq_dvd_mod)
        · rintro rfl
          exact ⟨⟨by omega, hT⟩, Nat.coprime_one_left _⟩
      dsimp [pointwiseGroupedEnergyV]
      rw [h_rec_f, hc_all, Finset.sum_singleton, Finset.sum_singleton]
    · have hT0 : T = 0 := by omega
      subst hT0
      simp [pointwiseGroupedEnergyV, coprimeCutoffFinset, hf0]
  have h_fiber_adj :
      ∀ s ∈ coprimeCutoffFinset (insert p P) T,
        (∀ k : ℕ, k ∈ admissiblePrimeExponents T p s ↔ s * p ^ k ≤ T) ∧
          cofactorFiberF (insert p P) T s X =
            ∑ k ∈ admissiblePrimeExponents T p s, cofactorFiberF P T (s * p ^ k) X := by
    intro s hs
    have hs_mem := (Finset.mem_filter.mp hs).1
    rw [Finset.mem_Icc] at hs_mem
    have hs_pos : 0 < s := by omega
    refine ⟨mem_admissiblePrimeExponents_iff_aux hp hs_mem.1 T, ?_⟩
    rw [cofactorFiberF_eq_sum_gaussianTermPhi_aux (insert p P) T hs_pos hX]
    rw [sum_smoothCutoffFinset_insert_partition_aux hP hp hp_not_mem (T / s)
          (fun M => (liouvilleLambda (M * s) : ℝ) * gaussianTermPhi (M * s) X)]
    have h_adm_eq : admissiblePrimeExponents (T / s) p 1 = admissiblePrimeExponents T p s := by
      ext k
      rw [mem_admissiblePrimeExponents_iff_aux hp (by omega) (T / s) k,
          mem_admissiblePrimeExponents_iff_aux hp hs_mem.1 T k, one_mul,
          Nat.le_div_iff_mul_le hs_pos, mul_comm]
    rw [h_adm_eq]
    apply Finset.sum_congr rfl
    intro k _
    have h_spk_pos : 0 < s * p ^ k := Nat.mul_pos hs_pos (pow_pos hp.pos k)
    rw [cofactorFiberF_eq_sum_gaussianTermPhi_aux P T h_spk_pos hX]
    have h_div_eq : (T / s) / p ^ k = T / (s * p ^ k) := Nat.div_div_eq_div_mul T s (p ^ k)
    rw [h_div_eq]
    apply Finset.sum_congr rfl
    intro m _
    have h_assoc : m * p ^ k * s = m * (s * p ^ k) := by ring
    rw [h_assoc]
  have h_delta :
      pointwiseDelta P p T X =
        2 * ∑ s ∈ coprimeCutoffFinset (insert p P) T,
          ∑ k ∈ admissiblePrimeExponents T p s,
            ∑ l ∈ (admissiblePrimeExponents T p s).filter (fun l => k < l),
              cofactorFiberF P T (s * p ^ k) X * cofactorFiberF P T (s * p ^ l) X := by
    dsimp [pointwiseDelta, pointwiseGroupedEnergyV]
    rw [sum_coprimeCutoffFinset_insert_partition_aux hP hp hp_not_mem T
          (fun r => (cofactorFiberF P T r X) ^ 2)]
    have h_ins_sq :
        ∑ s ∈ coprimeCutoffFinset (insert p P) T, (cofactorFiberF (insert p P) T s X) ^ 2 =
          ∑ s ∈ coprimeCutoffFinset (insert p P) T,
            (∑ k ∈ admissiblePrimeExponents T p s, cofactorFiberF P T (s * p ^ k) X) ^ 2 := by
      apply Finset.sum_congr rfl
      intro s hs
      rw [(h_fiber_adj s hs).2]
    rw [h_ins_sq, ← Finset.sum_sub_distrib, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro s _
    exact sq_sum_sub_sum_sq_eq_two_sum_lt_aux (admissiblePrimeExponents T p s)
      (fun k => cofactorFiberF P T (s * p ^ k) X)
  refine ⟨⟨h_end_empty, h_end_all⟩, h_fiber_adj, h_delta, ?_⟩
  let ps := ascendingPrimesUpTo T
  have h_pw : ps.Pairwise (· < ·) := by
    dsimp [ps, ascendingPrimesUpTo]
    exact List.Pairwise.filter _ (List.pairwise_lt_range (T + 1))
  have h_toFin : ps.toFinset = primesUpToFinset T := by
    ext q
    simp only [ps, ascendingPrimesUpTo, List.mem_toFinset, List.mem_filter, List.mem_range,
      primesUpToFinset, Finset.mem_filter, Finset.mem_Icc, decide_eq_true_eq]
    constructor
    · rintro ⟨hq_lt, hq_p⟩
      exact ⟨⟨hq_p.two_le, by omega⟩, hq_p⟩
    · rintro ⟨⟨_, hq_le⟩, hq_p⟩
      exact ⟨by omega, hq_p⟩
  refine ⟨h_pw, h_toFin, ?_⟩
  have h_tele :
      ∀ m : ℕ, m ≤ ps.length →
        pointwiseGroupedEnergyV (prefixPrimeSet ps m) T X =
          pointwiseGroupedEnergyV ∅ T X +
            ∑ j ∈ Finset.range m,
              pointwiseDelta (prefixPrimeSet ps j) (ps.getD j 0) T X := by
    intro m hm
    induction' m with m ih
    · simp [prefixPrimeSet]
    · have hm_lt : m < ps.length := Nat.lt_of_succ_le hm
      rw [Finset.sum_range_succ, ← add_assoc, ← ih (Nat.le_of_lt hm_lt)]
      rw [prefixPrimeSet_succ_aux ps m hm_lt]
      dsimp [pointwiseDelta]
      ring
  have h_full := h_tele ps.length (le_refl _)
  have h_pref_len : prefixPrimeSet ps ps.length = primesUpToFinset T := by
    dsimp [prefixPrimeSet]
    rw [List.take_length, h_toFin]
  rw [h_pref_len, h_end_all, h_end_empty] at h_full
  exact h_full

/-- Helper: alternating sum of a finite nonnegative antitone sequence is nonnegative. -/
private theorem alternating_sum_nonneg_of_antitone_aux :
    ∀ (L : ℕ) (b : ℕ → ℝ),
      (∀ k < L, 0 ≤ b k) →
      (∀ i j : ℕ, i ≤ j → j < L → b j ≤ b i) →
      0 ≤ ∑ k ∈ Finset.range L, (-1 : ℝ) ^ k * b k
  | 0, _, _, _ => by simp
  | 1, b, hb_nn, _ => by
      simp only [Finset.range_one, Finset.sum_singleton, pow_zero, one_mul]
      exact hb_nn 0 (by omega)
  | L + 2, b, hb_nn, hb_anti => by
      rw [Finset.sum_range_succ', Finset.sum_range_succ']
      have h_tail_eq :
          ∑ k ∈ Finset.range L, (-1 : ℝ) ^ (k + 1 + 1) * b (k + 1 + 1) =
            ∑ k ∈ Finset.range L, (-1 : ℝ) ^ k * b (k + 2) := by
        apply Finset.sum_congr rfl
        intro k _
        have hexp : (-1 : ℝ) ^ (k + 1 + 1) = (-1 : ℝ) ^ k := by
          rw [pow_add, pow_add]
          ring
        have hidx : k + 1 + 1 = k + 2 := by omega
        rw [hexp, hidx]
      rw [h_tail_eq]
      have h_ih := alternating_sum_nonneg_of_antitone_aux L (fun k => b (k + 2))
        (fun k _ => hb_nn (k + 2) (by omega))
        (fun i j hij hjL => hb_anti (i + 2) (j + 2) (by omega) (by omega))
      have h01 : b 1 ≤ b 0 := hb_anti 0 1 (by omega) (by omega)
      simp only [pow_zero, zero_add, pow_one]
      linarith

/-- Helper: alternating sum of a finite nonnegative antitone sequence lies in `[0, b 0]` (`= 0` if `L = 0`). -/
private theorem alternating_sum_bounds_of_antitone_aux (L : ℕ) (b : ℕ → ℝ)
    (hb_nn : ∀ k < L, 0 ≤ b k)
    (hb_anti : ∀ i j : ℕ, i ≤ j → j < L → b j ≤ b i) :
    0 ≤ (∑ k ∈ Finset.range L, (-1 : ℝ) ^ k * b k) ∧
      (∑ k ∈ Finset.range L, (-1 : ℝ) ^ k * b k) ≤ (if L = 0 then 0 else b 0) := by
  refine ⟨alternating_sum_nonneg_of_antitone_aux L b hb_nn hb_anti, ?_⟩
  rcases L with _ | M
  · simp
  · simp only [Nat.succ_ne_zero, ↓reduceIte]
    rw [Finset.sum_range_succ']
    have h_sub :
        ∑ k ∈ Finset.range M, (-1 : ℝ) ^ (k + 1) * b (k + 1) =
          -(∑ k ∈ Finset.range M, (-1 : ℝ) ^ k * b (k + 1)) := by
      rw [← Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro k _
      rw [pow_succ]
      ring
    rw [h_sub]
    have h_tail_nn := alternating_sum_nonneg_of_antitone_aux M (fun k => b (k + 1))
      (fun k hk => hb_nn (k + 1) (by omega))
      (fun i j hij hjM => hb_anti (i + 1) (j + 1) (by omega) (by omega))
    simp only [pow_zero, one_mul]
    linarith

/-- Helper: basic properties of `chainMaxUpTo`: nonnegativity, upper bound on `< N`, attainment when `N > 0`,
    and invariance under zero-extension. -/
private theorem chainMaxUpTo_props_aux (N : ℕ) (a : ℕ → ℝ) (ha_nn : ∀ k < N, 0 ≤ a k) :
    0 ≤ chainMaxUpTo N a ∧
      (∀ k < N, a k ≤ chainMaxUpTo N a) ∧
      (0 < N → ∃ k < N, a k = chainMaxUpTo N a) := by
  induction' N with n ih
  · refine ⟨le_refl 0, ?_, ?_⟩
    · intro k hk; omega
    · intro h0; omega
  · obtain ⟨h_nn, h_ub, h_att⟩ := ih (fun k hk => ha_nn k (by omega))
    refine ⟨le_trans h_nn (le_max_left _ _), ?_, ?_⟩
    · intro k hk
      by_cases hkn : k = n
      · rw [hkn]
        exact le_max_right (chainMaxUpTo n a) (a n)
      · exact le_trans (h_ub k (by omega)) (le_max_left _ _)
    · intro _
      rcases Nat.eq_zero_or_pos n with rfl | hn_pos
      · refine ⟨0, by omega, ?_⟩
        dsimp [chainMaxUpTo]
        exact (max_eq_right (ha_nn 0 (by omega))).symm
      · by_cases h_cmp : chainMaxUpTo n a ≤ a n
        · refine ⟨n, by omega, ?_⟩
          dsimp [chainMaxUpTo]
          exact (max_eq_right h_cmp).symm
        · obtain ⟨k, hk_lt, hk_eq⟩ := h_att hn_pos
          refine ⟨k, by omega, ?_⟩
          dsimp [chainMaxUpTo]
          rw [max_eq_left (le_of_not_ge h_cmp)]
          exact hk_eq

/-- **Theorem 18 (`TASK-TC-056` §4, Finite Alternating-Unimodal Chain Inequality, Squared Contraction, Zero-Extension, and Strict Gap)**:
    For every length `N : ℕ` and nonnegative finite sequence `a : ℕ → ℝ` (`∀ k < N, 0 ≤ a k`) satisfying
    `IsUnimodalChain N a` (allowing `N = 0`, `N = 1`, zero chains, and ties at the maximum):
    1. Alternating sum bounded by empty-safe maximum:
       `|∑ k ∈ Finset.range N, (-1)^k a_k| ≤ chainMaxUpTo N a`;
    2. Squared alternating contraction:
       `(∑ k ∈ Finset.range N, (-1)^k a_k)^2 ≤ ∑ k ∈ Finset.range N, a_k^2`;
    3. Quantitative two-term strict gap when `2 ≤ N`:
       `min (a 0 ^ 2) (a 1 ^ 2) ≤ (∑ k ∈ Finset.range N, a_k^2) - (∑ k ∈ Finset.range N, (-1)^k a_k)^2`
       (hence strict inequality `<` whenever `2 ≤ N`, `0 < a 0`, and `0 < a 1`);
    4. Degenerate & zero-extension properties: `chainMaxUpTo 0 a = 0`, `chainMaxUpTo 1 a = max 0 (a 0)`, and
       if `∀ k, N ≤ k → a k = 0` and `N ≤ M`, then `chainMaxUpTo M a = chainMaxUpTo N a`,
       `∑ k ∈ Finset.range M, (-1)^k a_k = ∑ k ∈ Finset.range N, (-1)^k a_k`, and `IsUnimodalChain M a`. -/
theorem finite_alternating_unimodal_chain_contraction_tc056
    (N : ℕ) (a : ℕ → ℝ) (ha_nn : ∀ k < N, 0 ≤ a k) (h_uni : IsUnimodalChain N a) :
    (|∑ k ∈ Finset.range N, (-1 : ℝ) ^ k * a k| ≤ chainMaxUpTo N a) ∧
    ((∑ k ∈ Finset.range N, (-1 : ℝ) ^ k * a k) ^ 2 ≤ ∑ k ∈ Finset.range N, (a k) ^ 2) ∧
    (2 ≤ N →
      min ((a 0) ^ 2) ((a 1) ^ 2) ≤
        (∑ k ∈ Finset.range N, (a k) ^ 2) - (∑ k ∈ Finset.range N, (-1 : ℝ) ^ k * a k) ^ 2) ∧
    (chainMaxUpTo 0 a = 0 ∧
      chainMaxUpTo 1 a = max 0 (a 0) ∧
      ∀ M : ℕ, N ≤ M → (∀ k : ℕ, N ≤ k → a k = 0) →
        chainMaxUpTo M a = chainMaxUpTo N a ∧
          (∑ k ∈ Finset.range M, (-1 : ℝ) ^ k * a k = ∑ k ∈ Finset.range N, (-1 : ℝ) ^ k * a k) ∧
          IsUnimodalChain M a) := by
  obtain ⟨hmax_nn, hmax_ub, _⟩ := chainMaxUpTo_props_aux N a ha_nn
  have h_peak_bound :
      0 < N →
        ∃ kp < N,
          |∑ idx ∈ Finset.range N, (-1 : ℝ) ^ idx * a idx| ≤ a kp := by
    intro hN_pos
    rcases h_uni with ⟨k_raw, hk_le_N, h_inc_raw, h_dec_raw⟩
    let kp := min k_raw (N - 1)
    have hkp_lt : kp < N := by omega
    have h_inc : ∀ i j : ℕ, i ≤ j → j ≤ kp → a i ≤ a j := by
      intro i j hij hjk
      exact h_inc_raw i j hij (le_trans hjk (min_le_left _ _)) (by omega)
    have h_dec : ∀ i j : ℕ, kp ≤ i → i ≤ j → j < N → a j ≤ a i := by
      intro i j hik hij hjN
      by_cases hk_lt : k_raw < N
      · have hkp_eq : kp = k_raw := min_eq_left (by omega)
        exact h_dec_raw i j (hkp_eq ▸ hik) hij hjN
      · have hkp_eq : kp = N - 1 := min_eq_right (by omega)
        have hij_eq : i = j := by omega
        rw [hij_eq]
    refine ⟨kp, hkp_lt, ?_⟩
    have h_split_N : N = kp + (N - kp) := by omega
    let S := ∑ idx ∈ Finset.range N, (-1 : ℝ) ^ idx * a idx
    let R_sum := ∑ j ∈ Finset.range (N - kp), (-1 : ℝ) ^ j * a (kp + j)
    let L_sum := ∑ j ∈ Finset.range kp, (-1 : ℝ) ^ j * a (kp - 1 - j)
    have h_S_decomp : (-1 : ℝ) ^ kp * S = R_sum - L_sum := by
      dsimp [S]
      conv_lhs => rw [h_split_N]
      rw [Finset.sum_range_add, mul_add]
      have h_right :
          (-1 : ℝ) ^ kp * (∑ j ∈ Finset.range (N - kp), (-1 : ℝ) ^ (kp + j) * a (kp + j)) = R_sum := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro j _
        rw [pow_add]
        calc
          (-1 : ℝ) ^ kp * ((-1 : ℝ) ^ kp * (-1 : ℝ) ^ j * a (kp + j))
            = (((-1 : ℝ) ^ kp) * ((-1 : ℝ) ^ kp)) * ((-1 : ℝ) ^ j * a (kp + j)) := by ring
          _ = (-1 : ℝ) ^ j * a (kp + j) := by rw [neg_one_pow_mul_self_real_aux kp, one_mul]
      have h_left :
          (-1 : ℝ) ^ kp * (∑ idx ∈ Finset.range kp, (-1 : ℝ) ^ idx * a idx) = -L_sum := by
        rw [← Finset.sum_range_reflect (fun idx => (-1 : ℝ) ^ idx * a idx) kp]
        rw [Finset.mul_sum, ← Finset.sum_neg_distrib]
        apply Finset.sum_congr rfl
        intro j hj
        rw [Finset.mem_range] at hj
        have hkp_split : kp = (kp - 1 - j) + j + 1 := by omega
        have h_pow_kp : (-1 : ℝ) ^ kp = -((-1 : ℝ) ^ (kp - 1 - j) * (-1 : ℝ) ^ j) := by
          conv_lhs => rw [hkp_split]
          rw [pow_add, pow_add, pow_one]
          ring
        rw [h_pow_kp]
        calc
          -((-1 : ℝ) ^ (kp - 1 - j) * (-1 : ℝ) ^ j) * ((-1 : ℝ) ^ (kp - 1 - j) * a (kp - 1 - j))
            = -((((-1 : ℝ) ^ (kp - 1 - j)) * ((-1 : ℝ) ^ (kp - 1 - j))) *
                ((-1 : ℝ) ^ j * a (kp - 1 - j))) := by ring
          _ = -((-1 : ℝ) ^ j * a (kp - 1 - j)) := by
                rw [neg_one_pow_mul_self_real_aux (kp - 1 - j), one_mul]
      rw [h_right, h_left]
      ring
    obtain ⟨hR_nn, hR_ub⟩ := alternating_sum_bounds_of_antitone_aux (N - kp) (fun j => a (kp + j))
      (fun j hj => ha_nn (kp + j) (by omega))
      (fun i j hij hjlen => h_dec (kp + i) (kp + j) (by omega) (by omega) (by omega))
    have hR_le_akp : R_sum ≤ a kp := by
      have hne0 : N - kp ≠ 0 := by omega
      simpa [R_sum, hne0] using hR_ub
    obtain ⟨hL_nn, hL_ub⟩ := alternating_sum_bounds_of_antitone_aux kp (fun j => a (kp - 1 - j))
      (fun j hj => ha_nn (kp - 1 - j) (by omega))
      (fun i j hij hjkp => h_inc (kp - 1 - j) (kp - 1 - i) (by omega) (by omega))
    have hL_le_akp : L_sum ≤ a kp := by
      by_cases hkp0 : kp = 0
      · have hL0 : L_sum = 0 := by simp [L_sum, hkp0]
        rw [hL0]
        exact ha_nn kp hkp_lt
      · have h_sub1 : L_sum ≤ a (kp - 1) := by simpa [L_sum, hkp0] using hL_ub
        exact le_trans h_sub1 (h_inc (kp - 1) kp (by omega) (le_refl kp))
    have h_abs_sign : |(-1 : ℝ) ^ kp * S| = |S| := by
      rw [abs_mul, abs_pow, abs_neg, abs_one, one_pow, one_mul]
    rw [← h_abs_sign, h_S_decomp, abs_le]
    constructor <;> linarith
  have h_part1 : |∑ k ∈ Finset.range N, (-1 : ℝ) ^ k * a k| ≤ chainMaxUpTo N a := by
    rcases Nat.eq_zero_or_pos N with rfl | hN_pos
    · simp [chainMaxUpTo]
    · obtain ⟨kp, hkp_lt, h_le_akp⟩ := h_peak_bound hN_pos
      exact le_trans h_le_akp (hmax_ub kp hkp_lt)
  have h_part2 : (∑ k ∈ Finset.range N, (-1 : ℝ) ^ k * a k) ^ 2 ≤ ∑ k ∈ Finset.range N, (a k) ^ 2 := by
    rcases Nat.eq_zero_or_pos N with rfl | hN_pos
    · simp
    · obtain ⟨kp, hkp_lt, h_le_akp⟩ := h_peak_bound hN_pos
      have hakp_nn : 0 ≤ a kp := ha_nn kp hkp_lt
      have h_sq_le : (∑ k ∈ Finset.range N, (-1 : ℝ) ^ k * a k) ^ 2 ≤ (a kp) ^ 2 := by
        have habs_nn := abs_nonneg (∑ k ∈ Finset.range N, (-1 : ℝ) ^ k * a k)
        have hsq_abs := sq_abs (∑ k ∈ Finset.range N, (-1 : ℝ) ^ k * a k)
        nlinarith
      have h_akp_in_sum : (a kp) ^ 2 ≤ ∑ k ∈ Finset.range N, (a k) ^ 2 :=
        Finset.single_le_sum (fun k _ => sq_nonneg (a k)) (Finset.mem_range.mpr hkp_lt)
      exact le_trans h_sq_le h_akp_in_sum
  have h_part3 :
      2 ≤ N →
        min ((a 0) ^ 2) ((a 1) ^ 2) ≤
          (∑ k ∈ Finset.range N, (a k) ^ 2) - (∑ k ∈ Finset.range N, (-1 : ℝ) ^ k * a k) ^ 2 := by
    intro hN2
    obtain ⟨kp, hkp_lt, h_le_akp⟩ := h_peak_bound (by omega)
    have hakp_nn : 0 ≤ a kp := ha_nn kp hkp_lt
    have h_sq_le : (∑ k ∈ Finset.range N, (-1 : ℝ) ^ k * a k) ^ 2 ≤ (a kp) ^ 2 := by
      have habs_nn := abs_nonneg (∑ k ∈ Finset.range N, (-1 : ℝ) ^ k * a k)
      have hsq_abs := sq_abs (∑ k ∈ Finset.range N, (-1 : ℝ) ^ k * a k)
      nlinarith
    let m := if kp = 0 then 1 else 0
    have hm_lt : m < N := by dsimp [m]; split_ifs <;> omega
    have hm_ne_kp : m ≠ kp := by dsimp [m]; split_ifs with h0 <;> omega
    have h_pair_sub : ({kp, m} : Finset ℕ) ⊆ Finset.range N := by
      intro x hx
      simp only [Finset.mem_insert, Finset.mem_singleton] at hx
      rw [Finset.mem_range]
      rcases hx with rfl | rfl <;> omega
    have h_pair_sum :
        (a kp) ^ 2 + (a m) ^ 2 ≤ ∑ k ∈ Finset.range N, (a k) ^ 2 := by
      calc
        (a kp) ^ 2 + (a m) ^ 2
          = ∑ k ∈ ({kp, m} : Finset ℕ), (a k) ^ 2 := by
              rw [Finset.sum_pair hm_ne_kp.symm]
        _ ≤ ∑ k ∈ Finset.range N, (a k) ^ 2 :=
              Finset.sum_le_sum_of_subset_of_nonneg h_pair_sub (fun k _ _ => sq_nonneg (a k))
    have h_min_le : min ((a 0) ^ 2) ((a 1) ^ 2) ≤ (a m) ^ 2 := by
      dsimp [m]
      split_ifs
      · exact min_le_right _ _
      · exact min_le_left _ _
    linarith
  refine ⟨h_part1, h_part2, h_part3, rfl, rfl, ?_⟩
  intro M hNM ha_zero
  have h_max_eq : chainMaxUpTo M a = chainMaxUpTo N a := by
    obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hNM
    induction' d with d ih
    · simp
    · have h_add_succ : N + (d + 1) = (N + d) + 1 := by omega
      rw [h_add_succ]
      dsimp [chainMaxUpTo]
      rw [ih (Nat.le_add_right N d), ha_zero (N + d) (by omega), max_eq_left hmax_nn]
  have h_sum_eq :
      ∑ k ∈ Finset.range M, (-1 : ℝ) ^ k * a k = ∑ k ∈ Finset.range N, (-1 : ℝ) ^ k * a k := by
    obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hNM
    rw [Finset.sum_range_add]
    have h_tail0 : ∑ x ∈ Finset.range d, (-1 : ℝ) ^ (N + x) * a (N + x) = 0 := by
      apply Finset.sum_eq_zero
      intro x _
      rw [ha_zero (N + x) (by omega), mul_zero]
    linarith
  have h_uni_M : IsUnimodalChain M a := by
    rcases Nat.eq_zero_or_pos N with rfl | hN_pos
    · refine ⟨0, by omega, ?_, ?_⟩
      · intro i j hij hj0 _
        have hi0 : i = 0 := by omega
        have hj0' : j = 0 := by omega
        rw [hi0, hj0']
      · intro i j _ _ _
        rw [ha_zero i (by omega), ha_zero j (by omega)]
    · rcases h_uni with ⟨k_raw, _, h_inc_raw, h_dec_raw⟩
      let kp := min k_raw (N - 1)
      refine ⟨kp, by omega, ?_, ?_⟩
      · intro i j hij hjk _
        exact h_inc_raw i j hij (le_trans hjk (min_le_left _ _)) (by omega)
      · intro i j hik hij _
        by_cases hjN : j < N
        · by_cases hk_lt : k_raw < N
          · have hkp_eq : kp = k_raw := min_eq_left (by omega)
            exact h_dec_raw i j (hkp_eq ▸ hik) hij hjN
          · have hkp_eq : kp = N - 1 := min_eq_right (by omega)
            have hij_eq : i = j := by omega
            rw [hij_eq]
        · rw [ha_zero j (by omega)]
          by_cases hiN : i < N
          · exact ha_nn i hiN
          · rw [ha_zero i (by omega)]
  exact ⟨h_max_eq, h_sum_eq, h_uni_M⟩

/-- Finite truncated Gaussian prime-power chain `a_{s,m,k}(X) := φ_{s m p^k}(X)` if `s m p^k ≤ T`, else `0`. -/
noncomputable def gaussianPrimeChain (T p s m : ℕ) (X : ℝ) (k : ℕ) : ℝ :=
  if s * m * p ^ k ≤ T then gaussianTermPhi (s * m * p ^ k) X else 0

/-- Alternating sum `A_{s,m}(X) := ∑_{0 ≤ k ≤ T} (-1)^k a_{s,m,k}(X)` along a single prime's powers. -/
noncomputable def gaussianAlternatingChainSum (T p s m : ℕ) (X : ℝ) : ℝ :=
  ∑ k ∈ Finset.range (T + 1), (-1 : ℝ) ^ k * gaussianPrimeChain T p s m X k

/-- Consecutive admissible Gaussian chain ratio
    `r_{p,s,m,X}(k) := p^{-3} exp[(X^2 / (s m)^2) p^{-2k} (1 - p^{-2})]`. -/
noncomputable def gaussianChainRatio (p s m : ℕ) (X : ℝ) (k : ℕ) : ℝ :=
  ((p : ℝ) ^ 3)⁻¹ *
    Real.exp ((X ^ 2 / ((s * m : ℕ) : ℝ) ^ 2) * ((p : ℝ) ^ (2 * k))⁻¹ * (1 - ((p : ℝ) ^ 2)⁻¹))

/-- Pointwise single-prime contraction term
    `c_{P,p}(X; T) := ∑_{s ∈ coprime(P ∪ {p}, T)} ∑_{m ∈ S(P), s m ≤ T} [∑_k a_{s,m,k}(X)^2 - A_{s,m}(X)^2]`. -/
noncomputable def pointwiseContractionC (P : Finset ℕ) (p T : ℕ) (X : ℝ) : ℝ :=
  ∑ s ∈ coprimeCutoffFinset (insert p P) T,
    ∑ m ∈ smoothCutoffFinset P (T / s),
      ((∑ k ∈ Finset.range (T + 1), (gaussianPrimeChain T p s m X k) ^ 2) -
        (gaussianAlternatingChainSum T p s m X) ^ 2)

/-- Pointwise ordered (`m ≠ n`) mixed-prime interaction term
    `m_{P,p}(X; T) := ∑_{s ∈ coprime(P ∪ {p}, T)} ∑_{m ≠ n ∈ S(P), s m, s n ≤ T} λ(m) λ(n) [A_{s,m}(X) A_{s,n}(X) - ∑_k a_{s,m,k}(X) a_{s,n,k}(X)]`
    (retaining `λ(m) λ(n)`, with `λ(s)^2 = 1` cancelled and NO extra factor of `2`). -/
noncomputable def pointwiseMixedM (P : Finset ℕ) (p T : ℕ) (X : ℝ) : ℝ :=
  ∑ s ∈ coprimeCutoffFinset (insert p P) T,
    ∑ m ∈ smoothCutoffFinset P (T / s),
      ∑ n ∈ (smoothCutoffFinset P (T / s)).erase m,
        (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
          (gaussianAlternatingChainSum T p s m X * gaussianAlternatingChainSum T p s n X -
            ∑ k ∈ Finset.range (T + 1),
              gaussianPrimeChain T p s m X k * gaussianPrimeChain T p s n X k)

/-- Helper: elementary monotonicity `x ^ a ≤ x ^ b` for `1 ≤ x` and `a ≤ b`. -/
private theorem real_pow_le_pow_of_one_le_aux {x : ℝ} (hx : 1 ≤ x) {a b : ℕ} (hab : a ≤ b) :
    x ^ a ≤ x ^ b := by
  obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hab
  induction' d with d ih
  · simp
  · rw [Nat.add_succ, pow_succ]
    have hpow_nn : 0 ≤ x ^ (a + d) := pow_nonneg (by linarith) _
    nlinarith [ih (Nat.le_add_right a d)]

/-- Helper: elementary peak-finding lemma from one-step descent `a (k + 1) ≤ a k → a (k + 2) ≤ a (k + 1)`
    and terminal inequality `a (B + 1) ≤ a B`. -/
private theorem exists_peak_of_one_step_descent_aux :
    ∀ (B : ℕ) (a : ℕ → ℝ),
      (∀ k : ℕ, a (k + 1) ≤ a k → a (k + 2) ≤ a (k + 1)) →
      a (B + 1) ≤ a B →
      ∃ kp ≤ B, (∀ j < kp, a j ≤ a (j + 1)) ∧ (∀ j : ℕ, kp ≤ j → a (j + 1) ≤ a j)
  | 0, a, h_desc, h_end => by
      refine ⟨0, le_refl 0, (fun j hj => by omega), ?_⟩
      suffices h_all : ∀ j : ℕ, a (j + 1) ≤ a j by
        intro j _
        exact h_all j
      intro j
      induction' j with j ih
      · exact h_end
      · exact h_desc j ih
  | B + 1, a, h_desc, h_end => by
      by_cases h0 : a 1 ≤ a 0
      · refine ⟨0, by omega, (fun j hj => by omega), ?_⟩
        suffices h_all : ∀ j : ℕ, a (j + 1) ≤ a j by
          intro j _
          exact h_all j
        intro j
        induction' j with j ih
        · exact h0
        · exact h_desc j ih
      · have h0_lt : a 0 ≤ a 1 := le_of_not_ge h0
        obtain ⟨kp', hkp'_le, h_up', h_dn'⟩ :=
          exists_peak_of_one_step_descent_aux B (fun k => a (k + 1))
            (fun k hk => h_desc (k + 1) hk) h_end
        refine ⟨kp' + 1, by omega, ?_, ?_⟩
        · intro j hj
          rcases j with _ | j'
          · exact h0_lt
          · exact h_up' j' (by omega)
        · intro j hj
          rcases j with _ | j'
          · omega
          · exact h_dn' j' (by omega)

/-- Helper: nonnegativity and positivity of `gaussianTermPhi n X`. -/
private theorem gaussianTermPhi_nonneg_and_pos_aux {n : ℕ} (hn : 0 < n) {X : ℝ} (hX : 0 ≤ X) :
    0 ≤ gaussianTermPhi n X ∧ (0 < X → 0 < gaussianTermPhi n X) := by
  have hn_pos : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr hn
  have hinv_pos : 0 < ((n : ℝ) ^ 3)⁻¹ := inv_pos.mpr (pow_pos hn_pos 3)
  have hexp_pos : 0 < Real.exp (-(X ^ 2) / (n : ℝ) ^ 2) := Real.exp_pos _
  refine ⟨?_, ?_⟩
  · dsimp [gaussianTermPhi]
    exact mul_nonneg (Real.rpow_nonneg hX _) (mul_nonneg (le_of_lt hinv_pos) (le_of_lt hexp_pos))
  · intro hX_pos
    dsimp [gaussianTermPhi]
    exact mul_pos (Real.rpow_pos_of_pos hX_pos _) (mul_pos hinv_pos hexp_pos)

/-- Helper: consecutive ratio identity and antitone property for `gaussianPrimeChain`. -/
private theorem gaussianPrimeChain_ratio_and_antitone_aux
    {T p s m : ℕ} (hp : p.Prime) (hs : 0 < s) (hm : 0 < m) (X : ℝ) :
    (∀ k : ℕ, 0 < X → s * m * p ^ (k + 1) ≤ T →
      0 < gaussianPrimeChain T p s m X k ∧
        gaussianPrimeChain T p s m X (k + 1) / gaussianPrimeChain T p s m X k =
          gaussianChainRatio p s m X k) ∧
    (∀ k l : ℕ, k ≤ l → gaussianChainRatio p s m X l ≤ gaussianChainRatio p s m X k) := by
  have hsm_pos : 0 < s * m := Nat.mul_pos hs hm
  have hp_real_pos : (0 : ℝ) < (p : ℝ) := Nat.cast_pos.mpr hp.pos
  have hp_ge2 : (2 : ℝ) ≤ (p : ℝ) := by exact_mod_cast hp.two_le
  refine ⟨?_, ?_⟩
  · intro k hX_pos hk1_le
    have hk_le : s * m * p ^ k ≤ T := by
      have h_pow_le : p ^ k ≤ p ^ (k + 1) := Nat.pow_le_pow_right hp.pos (by omega)
      exact le_trans (Nat.mul_le_mul_left (s * m) h_pow_le) hk1_le
    have h_ak_eq : gaussianPrimeChain T p s m X k = gaussianTermPhi (s * m * p ^ k) X := by
      simp [gaussianPrimeChain, hk_le]
    have h_ak1_eq : gaussianPrimeChain T p s m X (k + 1) = gaussianTermPhi (s * m * p ^ (k + 1)) X := by
      simp [gaussianPrimeChain, hk1_le]
    have h_ak_pos : 0 < gaussianTermPhi (s * m * p ^ k) X :=
      (gaussianTermPhi_nonneg_and_pos_aux (Nat.mul_pos hsm_pos (pow_pos hp.pos k)) (le_of_lt hX_pos)).2 hX_pos
    rw [h_ak_eq, h_ak1_eq]
    refine ⟨h_ak_pos, ?_⟩
    have hrpow_ne : X ^ (5 / 2 : ℝ) ≠ 0 := ne_of_gt (Real.rpow_pos_of_pos hX_pos _)
    have hsm_ne : ((s * m : ℕ) : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hsm_pos)
    have hp_ne : (p : ℝ) ≠ 0 := ne_of_gt hp_real_pos
    have hexp_ne : Real.exp (-(X ^ 2) / ((s * m * p ^ k : ℕ) : ℝ) ^ 2) ≠ 0 := ne_of_gt (Real.exp_pos _)
    dsimp [gaussianTermPhi, gaussianChainRatio]
    have hexp_diff :
        Real.exp (-(X ^ 2) / ((s * m * p ^ (k + 1) : ℕ) : ℝ) ^ 2) /
            Real.exp (-(X ^ 2) / ((s * m * p ^ k : ℕ) : ℝ) ^ 2) =
          Real.exp ((X ^ 2 / ((s * m : ℕ) : ℝ) ^ 2) * ((p : ℝ) ^ (2 * k))⁻¹ * (1 - ((p : ℝ) ^ 2)⁻¹)) := by
      rw [← Real.exp_sub]
      congr 1
      have h_cast_k : ((s * m * p ^ k : ℕ) : ℝ) ^ 2 = ((s * m : ℕ) : ℝ) ^ 2 * (p : ℝ) ^ (2 * k) := by
        rw [Nat.cast_mul (s * m) (p ^ k), Nat.cast_pow, Nat.mul_comm 2 k, pow_mul]
        ring
      have h_cast_k1 : ((s * m * p ^ (k + 1) : ℕ) : ℝ) ^ 2 =
          ((s * m : ℕ) : ℝ) ^ 2 * ((p : ℝ) ^ (2 * k) * (p : ℝ) ^ 2) := by
        rw [Nat.cast_mul (s * m) (p ^ (k + 1)), Nat.cast_pow, pow_add, pow_one, Nat.mul_comm 2 k, pow_mul]
        ring
      rw [h_cast_k, h_cast_k1]
      have hpk2_ne : (p : ℝ) ^ (2 * k) ≠ 0 := pow_ne_zero _ hp_ne
      field_simp [hsm_ne, hpk2_ne, hp_ne]
      ring
    have h_inv_div :
        (((s * m * p ^ (k + 1) : ℕ) : ℝ) ^ 3)⁻¹ / (((s * m * p ^ k : ℕ) : ℝ) ^ 3)⁻¹ =
          ((p : ℝ) ^ 3)⁻¹ := by
      push_cast
      have hpk_ne : (p : ℝ) ^ k ≠ 0 := pow_ne_zero _ hp_ne
      have hs_ne : (s : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hs)
      have hm_ne : (m : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hm)
      rw [pow_succ]
      field_simp [hs_ne, hm_ne, hpk_ne, hp_ne]
      ring
    calc
      X ^ (5 / 2 : ℝ) * ((((s * m * p ^ (k + 1) : ℕ) : ℝ) ^ 3)⁻¹ *
            Real.exp (-(X ^ 2) / ((s * m * p ^ (k + 1) : ℕ) : ℝ) ^ 2)) /
          (X ^ (5 / 2 : ℝ) * ((((s * m * p ^ k : ℕ) : ℝ) ^ 3)⁻¹ *
            Real.exp (-(X ^ 2) / ((s * m * p ^ k : ℕ) : ℝ) ^ 2)))
        = ((((s * m * p ^ (k + 1) : ℕ) : ℝ) ^ 3)⁻¹ / (((s * m * p ^ k : ℕ) : ℝ) ^ 3)⁻¹) *
            (Real.exp (-(X ^ 2) / ((s * m * p ^ (k + 1) : ℕ) : ℝ) ^ 2) /
              Real.exp (-(X ^ 2) / ((s * m * p ^ k : ℕ) : ℝ) ^ 2)) := by
            field_simp [hrpow_ne, hexp_ne]
            ring
      _ = ((p : ℝ) ^ 3)⁻¹ *
            Real.exp ((X ^ 2 / ((s * m : ℕ) : ℝ) ^ 2) * ((p : ℝ) ^ (2 * k))⁻¹ * (1 - ((p : ℝ) ^ 2)⁻¹)) := by
            rw [h_inv_div, hexp_diff]
  · intro k l hkl
    dsimp [gaussianChainRatio]
    have hp3_inv_nn : 0 ≤ ((p : ℝ) ^ 3)⁻¹ := inv_nonneg.mpr (pow_nonneg (le_of_lt hp_real_pos) 3)
    apply mul_le_mul_of_nonneg_left _ hp3_inv_nn
    rw [Real.exp_le_exp]
    have h_p2_ge4 : (4 : ℝ) ≤ (p : ℝ) ^ 2 := by nlinarith
    have hp2_pos : 0 < (p : ℝ) ^ 2 := by linarith
    have h_one_sub_nn : 0 ≤ 1 - ((p : ℝ) ^ 2)⁻¹ := by
      have h_inv_le1 : ((p : ℝ) ^ 2)⁻¹ ≤ 1 := by
        have h_mul1 : ((p : ℝ) ^ 2)⁻¹ * (p : ℝ) ^ 2 = 1 := by field_simp [ne_of_gt hp2_pos]
        nlinarith
      linarith
    have h_x_div_nn : 0 ≤ X ^ 2 / ((s * m : ℕ) : ℝ) ^ 2 := div_nonneg (sq_nonneg X) (sq_nonneg _)
    have h_pow_mono : (p : ℝ) ^ (2 * k) ≤ (p : ℝ) ^ (2 * l) :=
      real_pow_le_pow_of_one_le_aux (by linarith) (by omega)
    have hpk_pos : 0 < (p : ℝ) ^ (2 * k) := pow_pos hp_real_pos _
    have hpl_pos : 0 < (p : ℝ) ^ (2 * l) := pow_pos hp_real_pos _
    have h_inv_anti : ((p : ℝ) ^ (2 * l))⁻¹ ≤ ((p : ℝ) ^ (2 * k))⁻¹ := by
      have hu_pos : 0 < ((p : ℝ) ^ (2 * k))⁻¹ := inv_pos.mpr hpk_pos
      have hv_pos : 0 < ((p : ℝ) ^ (2 * l))⁻¹ := inv_pos.mpr hpl_pos
      have h1 : (p : ℝ) ^ (2 * k) * ((p : ℝ) ^ (2 * k))⁻¹ = 1 := by field_simp [ne_of_gt hpk_pos]
      have h2 : ((p : ℝ) ^ (2 * l))⁻¹ * (p : ℝ) ^ (2 * l) = 1 := by field_simp [ne_of_gt hpl_pos]
      calc
        ((p : ℝ) ^ (2 * l))⁻¹
          = ((p : ℝ) ^ (2 * l))⁻¹ * ((p : ℝ) ^ (2 * k) * ((p : ℝ) ^ (2 * k))⁻¹) := by rw [h1, mul_one]
        _ ≤ ((p : ℝ) ^ (2 * l))⁻¹ * ((p : ℝ) ^ (2 * l) * ((p : ℝ) ^ (2 * k))⁻¹) :=
              mul_le_mul_of_nonneg_left
                (mul_le_mul_of_nonneg_right h_pow_mono (le_of_lt hu_pos))
                (le_of_lt hv_pos)
        _ = (((p : ℝ) ^ (2 * l))⁻¹ * (p : ℝ) ^ (2 * l)) * ((p : ℝ) ^ (2 * k))⁻¹ := by ring
        _ = ((p : ℝ) ^ (2 * k))⁻¹ := by rw [h2, one_mul]
    have h_step1 := mul_le_mul_of_nonneg_left h_inv_anti h_x_div_nn
    exact mul_le_mul_of_nonneg_right h_step1 h_one_sub_nn

/-- Helper: unconditional unimodality `IsUnimodalChain (T + 1) (gaussianPrimeChain T p s m X)`. -/
private theorem gaussianPrimeChain_unimodal_aux
    (T : ℕ) {p s m : ℕ} (hp : p.Prime) (hs : 0 < s) (hm : 0 < m) {X : ℝ} (hX : 0 ≤ X) :
    (∀ k : ℕ, 0 ≤ gaussianPrimeChain T p s m X k) ∧
      (∀ k : ℕ, T + 1 ≤ k → gaussianPrimeChain T p s m X k = 0) ∧
      IsUnimodalChain (T + 1) (gaussianPrimeChain T p s m X) := by
  let a := gaussianPrimeChain T p s m X
  have hsm_pos : 0 < s * m := Nat.mul_pos hs hm
  have ha_nn : ∀ k : ℕ, 0 ≤ a k := by
    intro k
    dsimp [a, gaussianPrimeChain]
    split_ifs with hle
    · exact (gaussianTermPhi_nonneg_and_pos_aux (Nat.mul_pos hsm_pos (pow_pos hp.pos k)) hX).1
    · exact le_refl 0
  have ha_tail0 : ∀ k : ℕ, T + 1 ≤ k → a k = 0 := by
    intro k hk
    dsimp [a, gaussianPrimeChain]
    have h_gt : ¬ (s * m * p ^ k ≤ T) := by
      have hk_lt_pow : k < p ^ k := Nat.lt_pow_self hp.one_lt k
      have hpow_le : p ^ k ≤ s * m * p ^ k := Nat.le_mul_of_pos_left (p ^ k) hsm_pos
      omega
    exact if_neg h_gt
  refine ⟨ha_nn, ha_tail0, ?_⟩
  rcases eq_or_lt_of_le hX with rfl | hX_pos
  · refine ⟨0, by omega, ?_, ?_⟩
    · intro i j _ _ _
      have hz : ∀ n : ℕ, gaussianTermPhi n 0 = 0 := by
        intro n
        dsimp [gaussianTermPhi]
        rw [Real.zero_rpow (by norm_num : (5 / 2 : ℝ) ≠ 0), zero_mul]
      have hai : a i = 0 := by dsimp [a, gaussianPrimeChain]; split_ifs <;> simp [hz]
      have haj : a j = 0 := by dsimp [a, gaussianPrimeChain]; split_ifs <;> simp [hz]
      change a i ≤ a j
      rw [hai, haj]
    · intro i j _ _ _
      have hz : ∀ n : ℕ, gaussianTermPhi n 0 = 0 := by
        intro n
        dsimp [gaussianTermPhi]
        rw [Real.zero_rpow (by norm_num : (5 / 2 : ℝ) ≠ 0), zero_mul]
      have hai : a i = 0 := by dsimp [a, gaussianPrimeChain]; split_ifs <;> simp [hz]
      have haj : a j = 0 := by dsimp [a, gaussianPrimeChain]; split_ifs <;> simp [hz]
      change a j ≤ a i
      rw [hai, haj]
  · obtain ⟨h_rat_id, h_rat_anti⟩ := gaussianPrimeChain_ratio_and_antitone_aux (T := T) hp hs hm X
    have h_one_step : ∀ k : ℕ, a (k + 1) ≤ a k → a (k + 2) ≤ a (k + 1) := by
      intro k hk_le
      by_cases hk2_adm : s * m * p ^ (k + 2) ≤ T
      · have hk1_adm : s * m * p ^ (k + 1) ≤ T := by
          have h_pow : p ^ (k + 1) ≤ p ^ (k + 2) := Nat.pow_le_pow_right hp.pos (by omega)
          exact le_trans (Nat.mul_le_mul_left (s * m) h_pow) hk2_adm
        obtain ⟨hak_pos, h_div_k⟩ := h_rat_id k hX_pos hk1_adm
        obtain ⟨hak1_pos, h_div_k1⟩ := h_rat_id (k + 1) hX_pos hk2_adm
        have hrk_le1 : gaussianChainRatio p s m X k ≤ 1 := by
          rw [← h_div_k]
          exact (div_le_one hak_pos).mpr hk_le
        have hrk1_le1 : gaussianChainRatio p s m X (k + 1) ≤ 1 :=
          le_trans (h_rat_anti k (k + 1) (by omega)) hrk_le1
        rw [← h_div_k1] at hrk1_le1
        exact (div_le_one hak1_pos).mp hrk1_le1
      · have hak2_0 : a (k + 2) = 0 := by simp [a, gaussianPrimeChain, hk2_adm]
        rw [hak2_0]
        exact ha_nn (k + 1)
    have h_end : a (T + 1) ≤ a T := by
      rw [ha_tail0 (T + 1) (le_refl _)]
      exact ha_nn T
    obtain ⟨kp, hkp_le, h_up, h_dn⟩ := exists_peak_of_one_step_descent_aux T a h_one_step h_end
    refine ⟨kp, by omega, ?_, ?_⟩
    · intro i j hij hjk h_unused
      clear h_unused
      change a i ≤ a j
      obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hij
      clear hij
      revert hjk
      induction' d with d ih
      · intro _; exact le_refl _
      · intro h_id1
        rw [Nat.add_succ]
        exact le_trans (ih (by omega)) (h_up (i + d) (by omega))
    · intro i j hik hij h_unused
      clear h_unused
      change a j ≤ a i
      obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hij
      clear hij
      induction' d with d ih
      · exact le_refl _
      · rw [Nat.add_succ]
        exact le_trans (h_dn (i + d) (by omega)) ih

/-- Helper: express `cofactorFiberF P T (s * p^k) X` through `gaussianPrimeChain T p s m X k`
    for `s ∈ coprimeCutoffFinset (insert p P) T`. -/
private theorem cofactorFiberF_spk_eq_sum_gaussianPrimeChain_aux
    {P : Finset ℕ} {p : ℕ} (hp : p.Prime) (T : ℕ)
    {s : ℕ} (hs : s ∈ coprimeCutoffFinset (insert p P) T) (k : ℕ) {X : ℝ} (hX : 0 ≤ X) :
    (if s * p ^ k ≤ T then cofactorFiberF P T (s * p ^ k) X else 0) =
      (liouvilleLambda s : ℝ) * (-1 : ℝ) ^ k *
        ∑ m ∈ smoothCutoffFinset P (T / s),
          (liouvilleLambda m : ℝ) * gaussianPrimeChain T p s m X k := by
  have hs_mem := (Finset.mem_filter.mp hs).1
  rw [Finset.mem_Icc] at hs_mem
  have hs_pos : 0 < s := by omega
  have hs_ne : s ≠ 0 := by omega
  by_cases h_spk : s * p ^ k ≤ T
  · rw [if_pos h_spk]
    have h_spk_pos : 0 < s * p ^ k := Nat.mul_pos hs_pos (pow_pos hp.pos k)
    have h_spk_ne : s * p ^ k ≠ 0 := Nat.pos_iff_ne_zero.mp h_spk_pos
    rw [cofactorFiberF_eq_sum_gaussianTermPhi_aux P T h_spk_pos hX]
    rw [Finset.mul_sum]
    have h_sub : smoothCutoffFinset P (T / (s * p ^ k)) ⊆ smoothCutoffFinset P (T / s) := by
      intro m hm
      simp only [smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc] at hm ⊢
      rcases hm with ⟨⟨hm1, hm_le⟩, hm_sm⟩
      have h_div_le : T / (s * p ^ k) ≤ T / s := by
        rw [← Nat.div_div_eq_div_mul]
        exact Nat.div_le_self (T / s) (p ^ k)
      exact ⟨⟨hm1, le_trans hm_le h_div_le⟩, hm_sm⟩
    have h_zero_out :
        ∀ m ∈ smoothCutoffFinset P (T / s),
          m ∉ smoothCutoffFinset P (T / (s * p ^ k)) →
            (liouvilleLambda s : ℝ) * (-1 : ℝ) ^ k *
              ((liouvilleLambda m : ℝ) * gaussianPrimeChain T p s m X k) = 0 := by
      intro m hm hnot
      simp only [smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc] at hm hnot
      have h_not_le_div : ¬ (m ≤ T / (s * p ^ k)) := fun hle => hnot ⟨⟨hm.1.1, hle⟩, hm.2⟩
      have h_not_le_prod : ¬ (s * m * p ^ k ≤ T) := by
        intro hprod
        apply h_not_le_div
        rw [Nat.le_div_iff_mul_le h_spk_pos]
        linarith [show m * (s * p ^ k) = s * m * p ^ k by ring]
      simp [gaussianPrimeChain, h_not_le_prod]
    rw [← Finset.sum_subset h_sub h_zero_out]
    apply Finset.sum_congr rfl
    intro m hm
    simp only [smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc] at hm
    have hm_ne : m ≠ 0 := Nat.pos_iff_ne_zero.mp hm.1.1
    have h_prod_le : s * m * p ^ k ≤ T := by
      have h1 := (Nat.le_div_iff_mul_le h_spk_pos).mp hm.1.2
      linarith [show m * (s * p ^ k) = s * m * p ^ k by ring]
    have h_lam_factor :
        (liouvilleLambda (m * (s * p ^ k)) : ℝ) =
          (liouvilleLambda s : ℝ) * (-1 : ℝ) ^ k * (liouvilleLambda m : ℝ) := by
      have hpk_ne : p ^ k ≠ 0 := pow_ne_zero k hp.ne_zero
      rw [liouvilleLambda_mul_aux hm_ne h_spk_ne, liouvilleLambda_mul_aux hs_ne hpk_ne,
          liouvilleLambda_prime_pow_aux hp k]
      dsimp [liouvilleSignFromOmega]
      push_cast
      ring
    have h_mul_eq : m * (s * p ^ k) = s * m * p ^ k := by ring
    simp only [gaussianPrimeChain, h_prod_le, ↓reduceIte]
    rw [h_lam_factor, h_mul_eq]
    ring
  · rw [if_neg h_spk]
    symm
    rw [Finset.mul_sum]
    apply Finset.sum_eq_zero
    intro m hm
    simp only [smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc] at hm
    have h_not_prod : ¬ (s * m * p ^ k ≤ T) := by
      intro hprod
      have h_le : s * p ^ k ≤ s * m * p ^ k := by
        have h_sm : s ≤ s * m := Nat.le_mul_of_pos_right s hm.1.1
        exact Nat.mul_le_mul_right (p ^ k) h_sm
      exact h_spk (le_trans h_le hprod)
    simp [gaussianPrimeChain, h_not_prod]

/-- **Theorem 19 (`TASK-TC-056` §4, Actual Gaussian Prime-Chain Ratio, Unconditional Unimodality, and Singleton-Prime Contraction)**:
    For every prime `p`, positive integers `s, m > 0`, cutoff `T : ℕ`, and `X : ℝ` with `0 ≤ X`:
    1. Exact consecutive Gaussian chain ratio (`0 < X`, `s * m * p ^ (k + 1) ≤ T`):
       `0 < gaussianPrimeChain T p s m X k` and
       `gaussianPrimeChain T p s m X (k + 1) / gaussianPrimeChain T p s m X k = gaussianChainRatio p s m X k`,
       with `k ↦ gaussianChainRatio p s m X k` antitone (`k ≤ l → r(l) ≤ r(k)`);
    2. Unconditional unimodality and chain contraction of the concrete Gaussian chain (NOT assumed as a hypothesis):
       `IsUnimodalChain (T + 1) (gaussianPrimeChain T p s m X)`,
       `|gaussianAlternatingChainSum T p s m X| ≤ chainMaxUpTo (T + 1) (gaussianPrimeChain T p s m X)`, and
       `(gaussianAlternatingChainSum T p s m X) ^ 2 ≤ ∑ k ∈ Finset.range (T + 1), (gaussianPrimeChain T p s m X k) ^ 2`;
    3. Pointwise singleton-prime contraction:
       `pointwiseGroupedEnergyV {p} T X ≤ pointwiseDiagonalD T X`;
    4. Quantitative strict singleton-prime contraction when `0 < X` and `p ≤ T`:
       `min ((gaussianTermPhi 1 X) ^ 2) ((gaussianTermPhi p X) ^ 2) ≤ pointwiseDiagonalD T X - pointwiseGroupedEnergyV {p} T X`
       and `pointwiseGroupedEnergyV {p} T X < pointwiseDiagonalD T X`. -/
theorem gaussian_prime_chain_unimodal_and_singleton_contraction_tc056
    {p s m : ℕ} (hp : p.Prime) (hs : 0 < s) (hm : 0 < m) (T : ℕ) {X : ℝ} (hX : 0 ≤ X) :
    ((∀ k : ℕ, 0 < X → s * m * p ^ (k + 1) ≤ T →
        0 < gaussianPrimeChain T p s m X k ∧
          gaussianPrimeChain T p s m X (k + 1) / gaussianPrimeChain T p s m X k =
            gaussianChainRatio p s m X k) ∧
      (∀ k l : ℕ, k ≤ l → gaussianChainRatio p s m X l ≤ gaussianChainRatio p s m X k)) ∧
    (IsUnimodalChain (T + 1) (gaussianPrimeChain T p s m X) ∧
      |gaussianAlternatingChainSum T p s m X| ≤
        chainMaxUpTo (T + 1) (gaussianPrimeChain T p s m X) ∧
      (gaussianAlternatingChainSum T p s m X) ^ 2 ≤
        ∑ k ∈ Finset.range (T + 1), (gaussianPrimeChain T p s m X k) ^ 2) ∧
    (pointwiseGroupedEnergyV {p} T X ≤ pointwiseDiagonalD T X) ∧
    (0 < X → p ≤ T →
      min ((gaussianTermPhi 1 X) ^ 2) ((gaussianTermPhi p X) ^ 2) ≤
        pointwiseDiagonalD T X - pointwiseGroupedEnergyV {p} T X ∧
        pointwiseGroupedEnergyV {p} T X < pointwiseDiagonalD T X) := by
  have h_part1 := gaussianPrimeChain_ratio_and_antitone_aux (T := T) hp hs hm X
  obtain ⟨ha_nn, _, ha_uni⟩ := gaussianPrimeChain_unimodal_aux T hp hs hm hX
  obtain ⟨h_abs_max, h_sq_chain, _, _⟩ :=
    finite_alternating_unimodal_chain_contraction_tc056 (T + 1) (gaussianPrimeChain T p s m X)
      (fun k _ => ha_nn k) ha_uni
  have h_empty_prime : ∀ q ∈ (∅ : Finset ℕ), q.Prime := fun _ hq => False.elim (Finset.not_mem_empty _ hq)
  have hp_not_empty : p ∉ (∅ : Finset ℕ) := Finset.not_mem_empty p
  have h_Vp_eq :
      pointwiseGroupedEnergyV {p} T X =
        ∑ r ∈ coprimeCutoffFinset {p} T, (gaussianAlternatingChainSum T p r 1 X) ^ 2 := by
    obtain ⟨_, h_fib_adj, _, _⟩ :=
      finite_prime_adjoining_fiber_and_pointwise_telescoping_tc056 h_empty_prime hp hp_not_empty T hX
    dsimp [pointwiseGroupedEnergyV]
    apply Finset.sum_congr rfl
    intro r hr
    have hr_ins : r ∈ coprimeCutoffFinset (insert p ∅) T := hr
    have h_fib_r :
        cofactorFiberF {p} T r X =
          ∑ k ∈ admissiblePrimeExponents T p r, cofactorFiberF ∅ T (r * p ^ k) X :=
      (h_fib_adj r hr_ins).2
    rw [h_fib_r]
    have h_sum_adm :
        ∑ k ∈ admissiblePrimeExponents T p r, cofactorFiberF ∅ T (r * p ^ k) X =
          (liouvilleLambda r : ℝ) * gaussianAlternatingChainSum T p r 1 X := by
      dsimp [admissiblePrimeExponents, gaussianAlternatingChainSum]
      rw [Finset.sum_filter, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro k _
      have h_k := cofactorFiberF_spk_eq_sum_gaussianPrimeChain_aux (P := ∅) hp T hr_ins k hX
      rw [h_k]
      have hr_mem := (Finset.mem_filter.mp hr).1
      rw [Finset.mem_Icc] at hr_mem
      have hdiv_ge1 : 1 ≤ T / r := (Nat.le_div_iff_mul_le (by omega)).mpr (by omega)
      have hs_empty : smoothCutoffFinset ∅ (T / r) = {1} := by
        ext u
        simp only [smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc, isPSmooth_empty_iff_aux,
          Finset.mem_singleton]
        exact ⟨fun h => h.2, fun h => ⟨⟨by omega, by omega⟩, h⟩⟩
      have hl1 : (liouvilleLambda 1 : ℝ) = 1 := by simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
      rw [hs_empty, Finset.sum_singleton, hl1, one_mul]
      ring
    rw [h_sum_adm]
    have hr_mem := (Finset.mem_filter.mp hr).1
    rw [Finset.mem_Icc] at hr_mem
    have hr_ne : r ≠ 0 := by omega
    have h_lam_sq : ((liouvilleLambda r : ℝ)) ^ 2 = 1 := by
      have h_int := liouvilleLambda_sq_aux hr_ne
      have h_cast : (liouvilleLambda r : ℝ) * (liouvilleLambda r : ℝ) = 1 := by exact_mod_cast h_int
      rw [sq, h_cast]
    calc
      ((liouvilleLambda r : ℝ) * gaussianAlternatingChainSum T p r 1 X) ^ 2
        = ((liouvilleLambda r : ℝ)) ^ 2 * (gaussianAlternatingChainSum T p r 1 X) ^ 2 := by ring
      _ = (gaussianAlternatingChainSum T p r 1 X) ^ 2 := by rw [h_lam_sq, one_mul]
  have h_DT_eq :
      pointwiseDiagonalD T X =
        ∑ r ∈ coprimeCutoffFinset {p} T,
          ∑ k ∈ Finset.range (T + 1), (gaussianPrimeChain T p r 1 X k) ^ 2 := by
    obtain ⟨⟨h_end_empty, _⟩, _, _, _⟩ :=
      finite_prime_adjoining_fiber_and_pointwise_telescoping_tc056 h_empty_prime hp hp_not_empty T hX
    rw [← h_end_empty]
    dsimp [pointwiseGroupedEnergyV]
    rw [sum_coprimeCutoffFinset_insert_partition_aux h_empty_prime hp hp_not_empty T
          (fun n => (cofactorFiberF ∅ T n X) ^ 2)]
    apply Finset.sum_congr rfl
    intro r hr
    dsimp [admissiblePrimeExponents]
    rw [Finset.sum_filter]
    apply Finset.sum_congr rfl
    intro k _
    by_cases h_rpk : r * p ^ k ≤ T
    · rw [if_pos h_rpk]
      have hr_mem := (Finset.mem_filter.mp hr).1
      rw [Finset.mem_Icc] at hr_mem
      have h_rpk_pos : 0 < r * p ^ k := Nat.mul_pos (by omega) (pow_pos hp.pos k)
      have h_rpk_ne : r * p ^ k ≠ 0 := Nat.pos_iff_ne_zero.mp h_rpk_pos
      rw [cofactorFiberF_eq_sum_gaussianTermPhi_aux ∅ T h_rpk_pos hX]
      have hdiv_ge1 : 1 ≤ T / (r * p ^ k) := (Nat.le_div_iff_mul_le h_rpk_pos).mpr (by simpa using h_rpk)
      have hs_empty : smoothCutoffFinset ∅ (T / (r * p ^ k)) = {1} := by
        ext u
        simp only [smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc, isPSmooth_empty_iff_aux,
          Finset.mem_singleton]
        exact ⟨fun h => h.2, fun h => ⟨⟨by omega, by omega⟩, h⟩⟩
      rw [hs_empty, Finset.sum_singleton, one_mul]
      have h_lam_sq : ((liouvilleLambda (r * p ^ k) : ℝ)) ^ 2 = 1 := by
        have h_int := liouvilleLambda_sq_aux h_rpk_ne
        have h_cast : (liouvilleLambda (r * p ^ k) : ℝ) * (liouvilleLambda (r * p ^ k) : ℝ) = 1 := by
          exact_mod_cast h_int
        rw [sq, h_cast]
      have h_gchain : gaussianPrimeChain T p r 1 X k = gaussianTermPhi (r * p ^ k) X := by
        dsimp [gaussianPrimeChain]
        have h_cond : r * 1 * p ^ k ≤ T := by simpa using h_rpk
        rw [if_pos h_cond]
        simp
      rw [h_gchain]
      calc
        ((liouvilleLambda (r * p ^ k) : ℝ) * gaussianTermPhi (r * p ^ k) X) ^ 2
          = ((liouvilleLambda (r * p ^ k) : ℝ)) ^ 2 * (gaussianTermPhi (r * p ^ k) X) ^ 2 := by ring
        _ = (gaussianTermPhi (r * p ^ k) X) ^ 2 := by rw [h_lam_sq, one_mul]
    · rw [if_neg h_rpk]
      have h_gchain0 : gaussianPrimeChain T p r 1 X k = 0 := by
        dsimp [gaussianPrimeChain]
        have h_cond : ¬ (r * 1 * p ^ k ≤ T) := by simpa using h_rpk
        rw [if_neg h_cond]
      rw [h_gchain0]
      ring
  have h_r_nonneg :
      ∀ r ∈ coprimeCutoffFinset {p} T,
        0 ≤ (∑ k ∈ Finset.range (T + 1), (gaussianPrimeChain T p r 1 X k) ^ 2) -
              (gaussianAlternatingChainSum T p r 1 X) ^ 2 := by
    intro r hr
    have hr_mem := (Finset.mem_filter.mp hr).1
    rw [Finset.mem_Icc] at hr_mem
    obtain ⟨hr_nn, _, hr_uni⟩ := gaussianPrimeChain_unimodal_aux T hp (by omega : 0 < r) (by omega : 0 < 1) hX
    obtain ⟨_, hr_sq, _, _⟩ :=
      finite_alternating_unimodal_chain_contraction_tc056 (T + 1) (gaussianPrimeChain T p r 1 X)
        (fun k _ => hr_nn k) hr_uni
    dsimp [gaussianAlternatingChainSum]
    linarith
  have h_part3 : pointwiseGroupedEnergyV {p} T X ≤ pointwiseDiagonalD T X := by
    have h_diff_nn : 0 ≤ pointwiseDiagonalD T X - pointwiseGroupedEnergyV {p} T X := by
      rw [h_DT_eq, h_Vp_eq, ← Finset.sum_sub_distrib]
      exact Finset.sum_nonneg h_r_nonneg
    linarith
  refine ⟨h_part1, ⟨ha_uni, h_abs_max, h_sq_chain⟩, h_part3, ?_⟩
  intro hX_pos hp_le_T
  have hp2 := hp.two_le
  have h1_mem : (1 : ℕ) ∈ coprimeCutoffFinset {p} T := by
    simp only [coprimeCutoffFinset, Finset.mem_filter, Finset.mem_Icc]
    exact ⟨⟨by omega, by omega⟩, Nat.coprime_one_left _⟩
  obtain ⟨h1_nn, _, h1_uni⟩ := gaussianPrimeChain_unimodal_aux T hp (by omega : 0 < 1) (by omega : 0 < 1) hX
  obtain ⟨_, _, h1_gap, _⟩ :=
    finite_alternating_unimodal_chain_contraction_tc056 (T + 1) (gaussianPrimeChain T p 1 1 X)
      (fun k _ => h1_nn k) h1_uni
  have hT1_ge2 : 2 ≤ T + 1 := by omega
  have h_gap_1 := h1_gap hT1_ge2
  have ha0_eq : gaussianPrimeChain T p 1 1 X 0 = gaussianTermPhi 1 X := by
    unfold gaussianPrimeChain
    have h_le : 1 * 1 * p ^ 0 ≤ T := by simp; omega
    rw [if_pos h_le]
    simp
  have ha1_eq : gaussianPrimeChain T p 1 1 X 1 = gaussianTermPhi p X := by
    unfold gaussianPrimeChain
    have h_le : 1 * 1 * p ^ 1 ≤ T := by simpa using hp_le_T
    rw [if_pos h_le]
    simp
  rw [ha0_eq, ha1_eq] at h_gap_1
  have h_single_le_diff :
      ((∑ k ∈ Finset.range (T + 1), (gaussianPrimeChain T p 1 1 X k) ^ 2) -
          (gaussianAlternatingChainSum T p 1 1 X) ^ 2) ≤
        pointwiseDiagonalD T X - pointwiseGroupedEnergyV {p} T X := by
    rw [h_DT_eq, h_Vp_eq, ← Finset.sum_sub_distrib]
    exact Finset.single_le_sum h_r_nonneg h1_mem
  have h_min_le_diff :
      min ((gaussianTermPhi 1 X) ^ 2) ((gaussianTermPhi p X) ^ 2) ≤
        pointwiseDiagonalD T X - pointwiseGroupedEnergyV {p} T X :=
    le_trans h_gap_1 h_single_le_diff
  have h_phi1_pos : 0 < (gaussianTermPhi 1 X) ^ 2 :=
    sq_pos_of_pos ((gaussianTermPhi_nonneg_and_pos_aux (by omega) hX).2 hX_pos)
  have h_phip_pos : 0 < (gaussianTermPhi p X) ^ 2 :=
    sq_pos_of_pos ((gaussianTermPhi_nonneg_and_pos_aux hp.pos hX).2 hX_pos)
  have h_min_pos : 0 < min ((gaussianTermPhi 1 X) ^ 2) ((gaussianTermPhi p X) ^ 2) :=
    lt_min h_phi1_pos h_phip_pos
  exact ⟨h_min_le_diff, by linarith⟩

/-- Helper: diagonal + ordered off-diagonal expansion of `(∑ m ∈ S, (liouvilleLambda m : ℝ) * f m)^2`
    when every `m ∈ S` satisfies `m ≠ 0` (discharging `λ(m)^2 = 1`). -/
private theorem sq_sum_liouville_weighted_split_aux
    (S : Finset ℕ) (hS_pos : ∀ m ∈ S, m ≠ 0) (f : ℕ → ℝ) :
    (∑ m ∈ S, (liouvilleLambda m : ℝ) * f m) ^ 2 =
      (∑ m ∈ S, (f m) ^ 2) +
        ∑ m ∈ S, ∑ n ∈ S.erase m,
          (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * (f m * f n) := by
  rw [sq, Finset.sum_mul_sum]
  have h_split :
      (∑ m ∈ S, ∑ n ∈ S, ((liouvilleLambda m : ℝ) * f m) * ((liouvilleLambda n : ℝ) * f n)) =
        (∑ m ∈ S, ((liouvilleLambda m : ℝ) * f m) * ((liouvilleLambda m : ℝ) * f m)) +
          ∑ m ∈ S, ∑ n ∈ S.erase m,
            ((liouvilleLambda m : ℝ) * f m) * ((liouvilleLambda n : ℝ) * f n) := by
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro m hm
    exact (Finset.add_sum_erase S
      (fun n => ((liouvilleLambda m : ℝ) * f m) * ((liouvilleLambda n : ℝ) * f n)) hm).symm
  rw [h_split]
  congr 1
  · apply Finset.sum_congr rfl
    intro m hm
    have h_int := liouvilleLambda_sq_aux (hS_pos m hm)
    have h_cast : (liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ) = 1 := by exact_mod_cast h_int
    calc
      ((liouvilleLambda m : ℝ) * f m) * ((liouvilleLambda m : ℝ) * f m)
        = ((liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ)) * (f m) ^ 2 := by ring
      _ = (f m) ^ 2 := by rw [h_cast, one_mul]
  · apply Finset.sum_congr rfl
    intro m _
    apply Finset.sum_congr rfl
    intro n _
    ring

/-- Helper: exact finite alternating shift expansion for `D_T - V_{ {p} }` (`TASK-TC-056` §6). -/
private theorem singleton_contraction_alternating_shift_aux
    {p : ℕ} (hp : p.Prime) (T : ℕ) {X : ℝ} (hX : 0 ≤ X) :
    pointwiseDiagonalD T X - pointwiseGroupedEnergyV {p} T X =
      2 * ∑ h ∈ (Finset.Icc 1 T).filter (fun h => p ^ h ≤ T),
        (-1 : ℝ) ^ (h + 1) *
          ∑ n ∈ Finset.Icc 1 (T / p ^ h),
            gaussianTermPhi n X * gaussianTermPhi (n * p ^ h) X := by
  have h_empty_prime : ∀ q ∈ (∅ : Finset ℕ), q.Prime := fun _ hq => False.elim (Finset.not_mem_empty _ hq)
  have hp_not_empty : p ∉ (∅ : Finset ℕ) := Finset.not_mem_empty p
  obtain ⟨⟨h_end_empty, _⟩, _, h_delta_e, _⟩ :=
    finite_prime_adjoining_fiber_and_pointwise_telescoping_tc056 h_empty_prime hp hp_not_empty T hX
  have h_diff_eq_neg_delta :
      pointwiseDiagonalD T X - pointwiseGroupedEnergyV {p} T X = -pointwiseDelta ∅ p T X := by
    dsimp [pointwiseDelta]
    rw [h_end_empty]
    ring
  rw [h_diff_eq_neg_delta, h_delta_e]
  have h_ins_e : insert p (∅ : Finset ℕ) = {p} := rfl
  rw [h_ins_e]
  have h_neg_in :
      -(2 * ∑ s ∈ coprimeCutoffFinset {p} T,
          ∑ k ∈ admissiblePrimeExponents T p s,
            ∑ l ∈ (admissiblePrimeExponents T p s).filter (fun l => k < l),
              cofactorFiberF ∅ T (s * p ^ k) X * cofactorFiberF ∅ T (s * p ^ l) X) =
        2 * ∑ s ∈ coprimeCutoffFinset {p} T,
          ∑ k ∈ admissiblePrimeExponents T p s,
            ∑ l ∈ (admissiblePrimeExponents T p s).filter (fun l => k < l),
              (-(cofactorFiberF ∅ T (s * p ^ k) X * cofactorFiberF ∅ T (s * p ^ l) X)) := by
    have h_two_neg : ∀ x : ℝ, -(2 * x) = 2 * (-x) := fun _ => by ring
    rw [h_two_neg, ← Finset.sum_neg_distrib]
    apply congr_arg (2 * ·)
    apply Finset.sum_congr rfl
    intro s _
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro k _
    rw [← Finset.sum_neg_distrib]
  rw [h_neg_in]
  apply congr_arg (2 * ·)
  have h_rhs_pull :
      ∑ h ∈ (Finset.Icc 1 T).filter (fun h => p ^ h ≤ T),
          (-1 : ℝ) ^ (h + 1) *
            ∑ n ∈ Finset.Icc 1 (T / p ^ h),
              gaussianTermPhi n X * gaussianTermPhi (n * p ^ h) X =
        ∑ h ∈ (Finset.Icc 1 T).filter (fun h => p ^ h ≤ T),
          ∑ n ∈ Finset.Icc 1 (T / p ^ h),
            (-1 : ℝ) ^ (h + 1) * (gaussianTermPhi n X * gaussianTermPhi (n * p ^ h) X) := by
    apply Finset.sum_congr rfl
    intro h _
    exact Finset.mul_sum _ _ _
  rw [h_rhs_pull]
  have h_lhs_sig :
      (∑ s ∈ coprimeCutoffFinset {p} T,
        ∑ k ∈ admissiblePrimeExponents T p s,
          ∑ l ∈ (admissiblePrimeExponents T p s).filter (fun l => k < l),
            (-(cofactorFiberF ∅ T (s * p ^ k) X * cofactorFiberF ∅ T (s * p ^ l) X))) =
        ∑ skl ∈ ((coprimeCutoffFinset {p} T).sigma (fun s => admissiblePrimeExponents T p s)).sigma
            (fun sk => (admissiblePrimeExponents T p sk.1).filter (fun l => sk.2 < l)),
          -(cofactorFiberF ∅ T (skl.1.1 * p ^ skl.1.2) X * cofactorFiberF ∅ T (skl.1.1 * p ^ skl.2) X) := by
    rw [Finset.sum_sigma', Finset.sum_sigma']
  have h_rhs_sig :
      (∑ h ∈ (Finset.Icc 1 T).filter (fun h => p ^ h ≤ T),
        ∑ n ∈ Finset.Icc 1 (T / p ^ h),
          (-1 : ℝ) ^ (h + 1) * (gaussianTermPhi n X * gaussianTermPhi (n * p ^ h) X)) =
        ∑ hn ∈ ((Finset.Icc 1 T).filter (fun h => p ^ h ≤ T)).sigma (fun h => Finset.Icc 1 (T / p ^ h)),
          (-1 : ℝ) ^ (hn.1 + 1) * (gaussianTermPhi hn.2 X * gaussianTermPhi (hn.2 * p ^ hn.1) X) := by
    rw [Finset.sum_sigma']
  rw [h_lhs_sig, h_rhs_sig]
  have hp_set : ∀ q ∈ ({p} : Finset ℕ), q.Prime := by
    intro q hq
    rw [Finset.mem_singleton] at hq
    rwa [hq]
  apply Finset.sum_bij (fun skl _ => ⟨skl.2 - skl.1.2, skl.1.1 * p ^ skl.1.2⟩)
  · rintro ⟨⟨s, k⟩, l⟩ hskl
    simp only [Finset.mem_sigma, coprimeCutoffFinset, Finset.mem_filter, Finset.mem_Icc] at hskl ⊢
    rcases hskl with ⟨⟨⟨⟨hs1, _⟩, _⟩, _⟩, ⟨hl_adm, hkl_lt⟩⟩
    have hsl_le : s * p ^ l ≤ T := (mem_admissiblePrimeExponents_iff_aux hp hs1 T l).mp hl_adm
    have h_l_eq : l = k + (l - k) := by omega
    have h_prod_eq : (s * p ^ k) * p ^ (l - k) = s * p ^ l := by
      conv_rhs => rw [h_l_eq]
      rw [pow_add]
      ring
    have h_ph_le : p ^ (l - k) ≤ T := by
      have h1 : p ^ (l - k) ≤ (s * p ^ k) * p ^ (l - k) :=
        Nat.le_mul_of_pos_left _ (Nat.mul_pos (by omega) (pow_pos hp.pos k))
      exact le_trans h1 (h_prod_eq.symm ▸ hsl_le)
    have h_h_lt_ph : l - k < p ^ (l - k) := Nat.lt_pow_self hp.one_lt (l - k)
    have hn_ge1 : 1 ≤ s * p ^ k := Nat.mul_pos (by omega) (pow_pos hp.pos k)
    have hn_le_div : s * p ^ k ≤ T / p ^ (l - k) :=
      (Nat.le_div_iff_mul_le (pow_pos hp.pos (l - k))).mpr (h_prod_eq.symm ▸ hsl_le)
    exact ⟨⟨⟨by omega, by omega⟩, h_ph_le⟩, ⟨hn_ge1, hn_le_div⟩⟩
  · rintro ⟨⟨s1, k1⟩, l1⟩ h1 ⟨⟨s2, k2⟩, l2⟩ h2 h_eq
    simp only [Finset.mem_sigma, coprimeCutoffFinset, Finset.mem_filter, Finset.mem_Icc] at h1 h2
    rcases h1 with ⟨⟨⟨⟨hs1_ge, _⟩, hs1_cop⟩, _⟩, ⟨_, hkl1⟩⟩
    rcases h2 with ⟨⟨⟨⟨_, _⟩, hs2_cop⟩, _⟩, ⟨_, hkl2⟩⟩
    have hh_eq : l1 - k1 = l2 - k2 := (Sigma.mk.inj_iff.mp h_eq).1
    have hn_eq : s1 * p ^ k1 = s2 * p ^ k2 := eq_of_heq (Sigma.mk.inj_iff.mp h_eq).2
    have hpk1_sm : isPSmooth {p} (p ^ k1) := by
      refine ⟨pow_pos hp.pos k1, ?_⟩
      intro q hq hdvd
      have hqp : q = p := (Nat.dvd_prime hp).mp (hq.dvd_of_dvd_pow hdvd) |>.resolve_left hq.ne_one
      exact Finset.mem_singleton.mpr hqp
    have hpk2_sm : isPSmooth {p} (p ^ k2) := by
      refine ⟨pow_pos hp.pos k2, ?_⟩
      intro q hq hdvd
      have hqp : q = p := (Nat.dvd_prime hp).mp (hq.dvd_of_dvd_pow hdvd) |>.resolve_left hq.ne_one
      exact Finset.mem_singleton.mpr hqp
    have h_pos : 0 < p ^ k1 * s1 := Nat.mul_pos (pow_pos hp.pos k1) (by omega)
    obtain ⟨_, h_uniq, _⟩ := smooth_coprime_positive_factorization_exists_unique_nat hp_set h_pos
    obtain ⟨h_sm1, h_cp1⟩ := h_uniq (p ^ k1) s1 rfl hpk1_sm hs1_cop
    have h_comm : p ^ k2 * s2 = p ^ k1 * s1 := by linarith [mul_comm s1 (p ^ k1), mul_comm s2 (p ^ k2)]
    obtain ⟨h_sm2, h_cp2⟩ := h_uniq (p ^ k2) s2 h_comm hpk2_sm hs2_cop
    have hs_eq : s1 = s2 := h_cp1.trans h_cp2.symm
    have hk_eq : k1 = k2 := Nat.pow_right_injective hp.two_le (h_sm1.trans h_sm2.symm)
    have hl_eq : l1 = l2 := by omega
    subst hs_eq; subst hk_eq; subst hl_eq
    rfl
  · rintro ⟨h, n⟩ hhn
    simp only [Finset.mem_sigma, Finset.mem_filter, Finset.mem_Icc] at hhn
    rcases hhn with ⟨⟨⟨hh1, _⟩, _⟩, ⟨hn1, hn_div⟩⟩
    let k := n.factorization p
    let s := pCoprimePart {p} n
    have hm_eq_pk : pSmoothPart {p} n = p ^ k := pSmoothPart_singleton_eq_pow_aux hp (by omega)
    obtain ⟨⟨h_mul_n, _, hs_cop_p, hs_pos⟩, _, _⟩ :=
      smooth_coprime_positive_factorization_exists_unique_nat hp_set (n := n) (by omega)
    rw [hm_eq_pk] at h_mul_n
    have hs_mul_pk : s * p ^ k = n := by rw [mul_comm]; exact h_mul_n
    have hnph_le : n * p ^ h ≤ T := (Nat.le_div_iff_mul_le (pow_pos hp.pos h)).mp hn_div
    have hskh_le : s * p ^ (k + h) ≤ T := by
      have h_eq : s * p ^ (k + h) = n * p ^ h := by rw [pow_add, ← mul_assoc, hs_mul_pk]
      exact h_eq.symm ▸ hnph_le
    have hsk_le : s * p ^ k ≤ T := by
      rw [hs_mul_pk]
      exact le_trans (Nat.le_mul_of_pos_right n (pow_pos hp.pos h)) hnph_le
    have hs_le_T : s ≤ T := by
      have hs_le_n : s ≤ n := by rw [← hs_mul_pk]; exact Nat.le_mul_of_pos_right s (pow_pos hp.pos k)
      exact le_trans hs_le_n (hs_mul_pk ▸ hsk_le)
    refine ⟨⟨⟨s, k⟩, k + h⟩, ?_, ?_⟩
    · simp only [Finset.mem_sigma, coprimeCutoffFinset, Finset.mem_filter, Finset.mem_Icc]
      refine ⟨⟨⟨⟨hs_pos, hs_le_T⟩, hs_cop_p⟩, ?_⟩, ⟨?_, by omega⟩⟩
      · exact (mem_admissiblePrimeExponents_iff_aux hp hs_pos T k).mpr hsk_le
      · exact (mem_admissiblePrimeExponents_iff_aux hp hs_pos T (k + h)).mpr hskh_le
    · exact Sigma.ext (Nat.add_sub_cancel_left k h) (heq_of_eq hs_mul_pk)
  · rintro ⟨⟨s, k⟩, l⟩ hskl
    simp only [Finset.mem_sigma, coprimeCutoffFinset, Finset.mem_filter, Finset.mem_Icc] at hskl
    rcases hskl with ⟨⟨⟨⟨hs1, _⟩, _⟩, hk_adm⟩, ⟨hl_adm, hkl_lt⟩⟩
    have hsk_le : s * p ^ k ≤ T := (mem_admissiblePrimeExponents_iff_aux hp hs1 T k).mp hk_adm
    have hsl_le : s * p ^ l ≤ T := (mem_admissiblePrimeExponents_iff_aux hp hs1 T l).mp hl_adm
    have hsk_pos : 0 < s * p ^ k := Nat.mul_pos (by omega) (pow_pos hp.pos k)
    have hsl_pos : 0 < s * p ^ l := Nat.mul_pos (by omega) (pow_pos hp.pos l)
    have hf_empty : ∀ {r : ℕ}, 0 < r → r ≤ T →
        cofactorFiberF ∅ T r X = (liouvilleLambda r : ℝ) * gaussianTermPhi r X := by
      intro r hr_pos hr_le
      rw [cofactorFiberF_eq_sum_gaussianTermPhi_aux ∅ T hr_pos hX]
      have hdiv_ge1 : 1 ≤ T / r := (Nat.le_div_iff_mul_le hr_pos).mpr (by omega)
      have hs_empty : smoothCutoffFinset ∅ (T / r) = {1} := by
        ext u
        simp only [smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc, isPSmooth_empty_iff_aux,
          Finset.mem_singleton]
        exact ⟨fun h => h.2, fun h => ⟨⟨by omega, by omega⟩, h⟩⟩
      rw [hs_empty, Finset.sum_singleton, one_mul]
    rw [hf_empty hsk_pos hsk_le, hf_empty hsl_pos hsl_le]
    have h_l_eq : s * p ^ l = (s * p ^ k) * p ^ (l - k) := by
      have hl_add : l = k + (l - k) := by omega
      conv_lhs => rw [hl_add]
      rw [pow_add]
      ring
    rw [h_l_eq]
    have hsk_ne : s * p ^ k ≠ 0 := Nat.pos_iff_ne_zero.mp hsk_pos
    have hph_ne : p ^ (l - k) ≠ 0 := pow_ne_zero _ hp.ne_zero
    have h_lam_prod :
        (liouvilleLambda (s * p ^ k) : ℝ) * (liouvilleLambda (s * p ^ k * p ^ (l - k)) : ℝ) =
          (-1 : ℝ) ^ (l - k) := by
      rw [liouvilleLambda_mul_aux hsk_ne hph_ne, liouvilleLambda_prime_pow_aux hp (l - k)]
      have h_int := liouvilleLambda_sq_aux hsk_ne
      have h_cast : (liouvilleLambda (s * p ^ k) : ℝ) * (liouvilleLambda (s * p ^ k) : ℝ) = 1 := by
        exact_mod_cast h_int
      dsimp [liouvilleSignFromOmega]
      push_cast
      calc
        (liouvilleLambda (s * p ^ k) : ℝ) * ((liouvilleLambda (s * p ^ k) : ℝ) * (-1 : ℝ) ^ (l - k))
          = ((liouvilleLambda (s * p ^ k) : ℝ) * (liouvilleLambda (s * p ^ k) : ℝ)) * (-1 : ℝ) ^ (l - k) := by ring
        _ = (-1 : ℝ) ^ (l - k) := by rw [h_cast, one_mul]
    have h_lhs_rearr :
        -(((liouvilleLambda (s * p ^ k) : ℝ) * gaussianTermPhi (s * p ^ k) X) *
            ((liouvilleLambda (s * p ^ k * p ^ (l - k)) : ℝ) *
              gaussianTermPhi (s * p ^ k * p ^ (l - k)) X)) =
          -(((liouvilleLambda (s * p ^ k) : ℝ) * (liouvilleLambda (s * p ^ k * p ^ (l - k)) : ℝ)) *
              (gaussianTermPhi (s * p ^ k) X * gaussianTermPhi (s * p ^ k * p ^ (l - k)) X)) := by ring
    rw [h_lhs_rearr, h_lam_prod, pow_succ]
    ring

/-- **Theorem 20 (`TASK-TC-056` §5 & §6, Mixed-Interaction Decomposition, `P`-Independence of `C_{P,p}`, and Exact Alternating Shift Formula for `C_p`)**:
    For every finite set of primes `P : Finset ℕ` (`∀ q ∈ P, q.Prime`), prime `p ∉ P`, cutoff `T : ℕ`,
    and `X : ℝ` with `0 ≤ X`:
    1. Nonnegativity of contraction and empty-`P` mixed vanishing:
       `0 ≤ pointwiseContractionC P p T X` and `pointwiseMixedM ∅ p T X = 0`;
    2. Exact decomposition `δ_{P,p}(X; T) = m_{P,p}(X; T) - c_{P,p}(X; T)` (with `λ(s)^2 = 1` cancelled and
       ordered `m ≠ n` retaining `λ(m) λ(n)` without an extra factor of `2`):
       `pointwiseDelta P p T X = pointwiseMixedM P p T X - pointwiseContractionC P p T X`;
    3. Equivalence of `pointwiseMixedM` with the ordered `k ≠ l` exponent expansion:
       `pointwiseMixedM P p T X = ∑ s ∈ coprimeCutoffFinset (insert p P) T, ∑ m ∈ smoothCutoffFinset P (T / s), ∑ n ∈ (smoothCutoffFinset P (T / s)).erase m, (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * (∑ k ∈ Finset.range (T + 1), ∑ l ∈ (Finset.range (T + 1)).erase k, (-1 : ℝ) ^ (k + l) * gaussianPrimeChain T p s m X k * gaussianPrimeChain T p s n X l)`;
    4. `P`-independence of `C_{P,p}` via the `p`-free cofactor bijection `r = s * m`:
       `pointwiseContractionC P p T X = pointwiseContractionC ∅ p T X` and
       `pointwiseContractionC P p T X = pointwiseDiagonalD T X - pointwiseGroupedEnergyV {p} T X`;
    5. Exact finite alternating shift expansion for `C_p` (`TASK-TC-056` §6):
       `pointwiseDiagonalD T X - pointwiseGroupedEnergyV {p} T X = 2 * ∑ h ∈ (Finset.Icc 1 T).filter (fun h => p ^ h ≤ T), (-1 : ℝ) ^ (h + 1) * ∑ n ∈ Finset.Icc 1 (T / p ^ h), gaussianTermPhi n X * gaussianTermPhi (n * p ^ h) X`. -/
theorem mixed_interaction_decomposition_and_p_independence_tc056
    {P : Finset ℕ} (hP : ∀ q ∈ P, q.Prime) {p : ℕ} (hp : p.Prime) (hp_not_mem : p ∉ P)
    (T : ℕ) {X : ℝ} (hX : 0 ≤ X) :
    (0 ≤ pointwiseContractionC P p T X ∧ pointwiseMixedM ∅ p T X = 0) ∧
    (pointwiseDelta P p T X = pointwiseMixedM P p T X - pointwiseContractionC P p T X) ∧
    (pointwiseMixedM P p T X =
      ∑ s ∈ coprimeCutoffFinset (insert p P) T,
        ∑ m ∈ smoothCutoffFinset P (T / s),
          ∑ n ∈ (smoothCutoffFinset P (T / s)).erase m,
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
              (∑ k ∈ Finset.range (T + 1),
                ∑ l ∈ (Finset.range (T + 1)).erase k,
                  (-1 : ℝ) ^ (k + l) *
                    gaussianPrimeChain T p s m X k * gaussianPrimeChain T p s n X l)) ∧
    (pointwiseContractionC P p T X = pointwiseContractionC ∅ p T X ∧
      pointwiseContractionC P p T X = pointwiseDiagonalD T X - pointwiseGroupedEnergyV {p} T X) ∧
    (pointwiseDiagonalD T X - pointwiseGroupedEnergyV {p} T X =
      2 * ∑ h ∈ (Finset.Icc 1 T).filter (fun h => p ^ h ≤ T),
        (-1 : ℝ) ^ (h + 1) *
          ∑ n ∈ Finset.Icc 1 (T / p ^ h),
            gaussianTermPhi n X * gaussianTermPhi (n * p ^ h) X) := by
  have h_c_nn : 0 ≤ pointwiseContractionC P p T X := by
    dsimp [pointwiseContractionC]
    apply Finset.sum_nonneg
    intro s hs
    have hs_pos : 0 < s := ((Finset.mem_filter.mp hs).1 |> Finset.mem_Icc.mp).1
    apply Finset.sum_nonneg
    intro m hm
    have hm_pos : 0 < m := ((Finset.mem_filter.mp hm).1 |> Finset.mem_Icc.mp).1
    obtain ⟨_, ⟨_, _, h_sq_chain⟩, _, _⟩ :=
      gaussian_prime_chain_unimodal_and_singleton_contraction_tc056 hp hs_pos hm_pos T hX
    linarith
  have h_m_empty : pointwiseMixedM ∅ p T X = 0 := by
    dsimp [pointwiseMixedM]
    apply Finset.sum_eq_zero
    intro s _
    apply Finset.sum_eq_zero
    intro m hm
    have hm1 : m = 1 := (isPSmooth_empty_iff_aux m).mp (Finset.mem_filter.mp hm).2
    have h_er_empty : (smoothCutoffFinset ∅ (T / s)).erase m = ∅ := by
      ext n
      simp only [Finset.mem_erase, smoothCutoffFinset, Finset.mem_filter, isPSmooth_empty_iff_aux,
        Finset.not_mem_empty, iff_false]
      rintro ⟨hne, _, hn1⟩
      exact hne (hn1.trans hm1.symm)
    rw [h_er_empty, Finset.sum_empty]
  have h_delta_decomp_gen :
      ∀ {Q : Finset ℕ}, (∀ q ∈ Q, q.Prime) → p ∉ Q →
        pointwiseDelta Q p T X = pointwiseMixedM Q p T X - pointwiseContractionC Q p T X := by
    intro Q hQ hp_not_Q
    obtain ⟨_, h_fib_adj_Q, _, _⟩ :=
      finite_prime_adjoining_fiber_and_pointwise_telescoping_tc056 hQ hp hp_not_Q T hX
    dsimp [pointwiseDelta, pointwiseGroupedEnergyV, pointwiseMixedM, pointwiseContractionC]
    rw [sum_coprimeCutoffFinset_insert_partition_aux hQ hp hp_not_Q T
          (fun r => (cofactorFiberF Q T r X) ^ 2)]
    rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro s hs
    have hs_mem := (Finset.mem_filter.mp hs).1
    rw [Finset.mem_Icc] at hs_mem
    have hs_ne : s ≠ 0 := by omega
    have h_lam_s_sq : ((liouvilleLambda s : ℝ)) ^ 2 = 1 := by
      have h_int := liouvilleLambda_sq_aux hs_ne
      have h_cast : (liouvilleLambda s : ℝ) * (liouvilleLambda s : ℝ) = 1 := by exact_mod_cast h_int
      rw [sq, h_cast]
    let Sm := smoothCutoffFinset Q (T / s)
    have hSm_ne0 : ∀ m ∈ Sm, m ≠ 0 := by
      intro m hm
      have hm_mem := (Finset.mem_filter.mp hm).1
      rw [Finset.mem_Icc] at hm_mem
      omega
    have h_ins_sum :
        cofactorFiberF (insert p Q) T s X =
          (liouvilleLambda s : ℝ) * ∑ m ∈ Sm, (liouvilleLambda m : ℝ) * gaussianAlternatingChainSum T p s m X := by
      rw [(h_fib_adj_Q s hs).2]
      dsimp [admissiblePrimeExponents]
      rw [Finset.sum_filter]
      have h_each :
          ∑ k ∈ Finset.range (T + 1), (if s * p ^ k ≤ T then cofactorFiberF Q T (s * p ^ k) X else 0) =
            ∑ k ∈ Finset.range (T + 1),
              (liouvilleLambda s : ℝ) *
                ∑ m ∈ Sm, (liouvilleLambda m : ℝ) * ((-1 : ℝ) ^ k * gaussianPrimeChain T p s m X k) := by
        apply Finset.sum_congr rfl
        intro k _
        rw [cofactorFiberF_spk_eq_sum_gaussianPrimeChain_aux hp T hs k hX]
        dsimp only [Sm]
        rw [Finset.mul_sum, Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro m _
        ring
      rw [h_each, ← Finset.mul_sum, Finset.sum_comm]
      congr 1
      apply Finset.sum_congr rfl
      intro m _
      dsimp [gaussianAlternatingChainSum]
      rw [Finset.mul_sum]
    have h_ins_sq :
        (cofactorFiberF (insert p Q) T s X) ^ 2 =
          (∑ m ∈ Sm, (gaussianAlternatingChainSum T p s m X) ^ 2) +
            ∑ m ∈ Sm, ∑ n ∈ Sm.erase m,
              (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                (gaussianAlternatingChainSum T p s m X * gaussianAlternatingChainSum T p s n X) := by
      rw [h_ins_sum, mul_pow, h_lam_s_sq, one_mul]
      exact sq_sum_liouville_weighted_split_aux Sm hSm_ne0 (fun m => gaussianAlternatingChainSum T p s m X)
    have h_old_sq :
        ∑ k ∈ admissiblePrimeExponents T p s, (cofactorFiberF Q T (s * p ^ k) X) ^ 2 =
          (∑ m ∈ Sm, ∑ k ∈ Finset.range (T + 1), (gaussianPrimeChain T p s m X k) ^ 2) +
            ∑ m ∈ Sm, ∑ n ∈ Sm.erase m,
              (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                (∑ k ∈ Finset.range (T + 1), gaussianPrimeChain T p s m X k * gaussianPrimeChain T p s n X k) := by
      dsimp [admissiblePrimeExponents]
      rw [Finset.sum_filter]
      have h_each_sq :
          ∑ k ∈ Finset.range (T + 1), (if s * p ^ k ≤ T then (cofactorFiberF Q T (s * p ^ k) X) ^ 2 else 0) =
            ∑ k ∈ Finset.range (T + 1),
              ((∑ m ∈ Sm, (gaussianPrimeChain T p s m X k) ^ 2) +
                ∑ m ∈ Sm, ∑ n ∈ Sm.erase m,
                  (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                    (gaussianPrimeChain T p s m X k * gaussianPrimeChain T p s n X k)) := by
        apply Finset.sum_congr rfl
        intro k _
        have h_if_sq :
            (if s * p ^ k ≤ T then (cofactorFiberF Q T (s * p ^ k) X) ^ 2 else 0) =
              (if s * p ^ k ≤ T then cofactorFiberF Q T (s * p ^ k) X else 0) ^ 2 := by
          split_ifs <;> ring
        rw [h_if_sq, cofactorFiberF_spk_eq_sum_gaussianPrimeChain_aux hp T hs k hX]
        have h_unit_k : (((liouvilleLambda s : ℝ) * (-1 : ℝ) ^ k)) ^ 2 = 1 := by
          rw [mul_pow, h_lam_s_sq, one_mul, sq, neg_one_pow_mul_self_real_aux k]
        rw [mul_pow, h_unit_k, one_mul]
        exact sq_sum_liouville_weighted_split_aux Sm hSm_ne0 (fun m => gaussianPrimeChain T p s m X k)
      rw [h_each_sq, Finset.sum_add_distrib]
      congr 1
      · exact Finset.sum_comm
      · rw [Finset.sum_comm]
        apply Finset.sum_congr rfl
        intro m _
        rw [Finset.sum_comm]
        apply Finset.sum_congr rfl
        intro n _
        rw [Finset.mul_sum]
    rw [h_ins_sq, h_old_sq]
    have h_diff_cross :
        (∑ m ∈ Sm, ∑ n ∈ Sm.erase m,
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
              (gaussianAlternatingChainSum T p s m X * gaussianAlternatingChainSum T p s n X)) -
          (∑ m ∈ Sm, ∑ n ∈ Sm.erase m,
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
              (∑ k ∈ Finset.range (T + 1), gaussianPrimeChain T p s m X k * gaussianPrimeChain T p s n X k)) =
          ∑ m ∈ Sm, ∑ n ∈ Sm.erase m,
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
              (gaussianAlternatingChainSum T p s m X * gaussianAlternatingChainSum T p s n X -
                ∑ k ∈ Finset.range (T + 1), gaussianPrimeChain T p s m X k * gaussianPrimeChain T p s n X k) := by
      rw [← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro m _
      rw [← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro n _
      ring
    have h_diff_diag :
        (∑ m ∈ Sm, ∑ k ∈ Finset.range (T + 1), (gaussianPrimeChain T p s m X k) ^ 2) -
          (∑ m ∈ Sm, (gaussianAlternatingChainSum T p s m X) ^ 2) =
          ∑ m ∈ Sm,
            ((∑ k ∈ Finset.range (T + 1), (gaussianPrimeChain T p s m X k) ^ 2) -
              (gaussianAlternatingChainSum T p s m X) ^ 2) :=
      Finset.sum_sub_distrib.symm
    linarith
  have h_delta_decomp := h_delta_decomp_gen hP hp_not_mem
  have h_m_kl :
      pointwiseMixedM P p T X =
        ∑ s ∈ coprimeCutoffFinset (insert p P) T,
          ∑ m ∈ smoothCutoffFinset P (T / s),
            ∑ n ∈ (smoothCutoffFinset P (T / s)).erase m,
              (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                (∑ k ∈ Finset.range (T + 1),
                  ∑ l ∈ (Finset.range (T + 1)).erase k,
                    (-1 : ℝ) ^ (k + l) *
                      gaussianPrimeChain T p s m X k * gaussianPrimeChain T p s n X l) := by
    dsimp [pointwiseMixedM]
    apply Finset.sum_congr rfl
    intro s _
    apply Finset.sum_congr rfl
    intro m _
    apply Finset.sum_congr rfl
    intro n _
    congr 1
    dsimp [gaussianAlternatingChainSum]
    rw [Finset.sum_mul_sum]
    have h_split_kl :
        (∑ k ∈ Finset.range (T + 1), ∑ l ∈ Finset.range (T + 1),
            ((-1 : ℝ) ^ k * gaussianPrimeChain T p s m X k) *
              ((-1 : ℝ) ^ l * gaussianPrimeChain T p s n X l)) =
          (∑ k ∈ Finset.range (T + 1),
              ((-1 : ℝ) ^ k * gaussianPrimeChain T p s m X k) *
                ((-1 : ℝ) ^ k * gaussianPrimeChain T p s n X k)) +
            ∑ k ∈ Finset.range (T + 1), ∑ l ∈ (Finset.range (T + 1)).erase k,
              ((-1 : ℝ) ^ k * gaussianPrimeChain T p s m X k) *
                ((-1 : ℝ) ^ l * gaussianPrimeChain T p s n X l) := by
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro k hk
      exact (Finset.add_sum_erase (Finset.range (T + 1))
        (fun l => ((-1 : ℝ) ^ k * gaussianPrimeChain T p s m X k) *
          ((-1 : ℝ) ^ l * gaussianPrimeChain T p s n X l)) hk).symm
    rw [h_split_kl]
    have h_diag_kl :
        ∑ k ∈ Finset.range (T + 1),
            ((-1 : ℝ) ^ k * gaussianPrimeChain T p s m X k) *
              ((-1 : ℝ) ^ k * gaussianPrimeChain T p s n X k) =
          ∑ k ∈ Finset.range (T + 1),
            gaussianPrimeChain T p s m X k * gaussianPrimeChain T p s n X k := by
      apply Finset.sum_congr rfl
      intro k _
      calc
        ((-1 : ℝ) ^ k * gaussianPrimeChain T p s m X k) *
            ((-1 : ℝ) ^ k * gaussianPrimeChain T p s n X k)
          = (((-1 : ℝ) ^ k) * ((-1 : ℝ) ^ k)) *
              (gaussianPrimeChain T p s m X k * gaussianPrimeChain T p s n X k) := by ring
        _ = gaussianPrimeChain T p s m X k * gaussianPrimeChain T p s n X k := by
              rw [neg_one_pow_mul_self_real_aux k, one_mul]
    have h_off_kl :
        ∑ k ∈ Finset.range (T + 1), ∑ l ∈ (Finset.range (T + 1)).erase k,
            ((-1 : ℝ) ^ k * gaussianPrimeChain T p s m X k) *
              ((-1 : ℝ) ^ l * gaussianPrimeChain T p s n X l) =
          ∑ k ∈ Finset.range (T + 1), ∑ l ∈ (Finset.range (T + 1)).erase k,
            (-1 : ℝ) ^ (k + l) *
              gaussianPrimeChain T p s m X k * gaussianPrimeChain T p s n X l := by
      apply Finset.sum_congr rfl
      intro k _
      apply Finset.sum_congr rfl
      intro l _
      rw [pow_add]
      ring
    linarith
  have h_c_bij_r :
      pointwiseContractionC P p T X =
        ∑ r ∈ coprimeCutoffFinset {p} T,
          ((∑ k ∈ Finset.range (T + 1), (gaussianPrimeChain T p r 1 X k) ^ 2) -
            (gaussianAlternatingChainSum T p r 1 X) ^ 2) := by
    dsimp [pointwiseContractionC]
    rw [Finset.sum_sigma' (coprimeCutoffFinset (insert p P) T) (fun s => smoothCutoffFinset P (T / s))
          (fun s m => (∑ k ∈ Finset.range (T + 1), (gaussianPrimeChain T p s m X k) ^ 2) -
            (gaussianAlternatingChainSum T p s m X) ^ 2)]
    apply Finset.sum_bij (fun sm _ => sm.1 * sm.2)
    · rintro ⟨s, m⟩ hsm
      simp only [Finset.mem_sigma, coprimeCutoffFinset, smoothCutoffFinset,
        Finset.mem_filter, Finset.mem_Icc] at hsm ⊢
      rcases hsm with ⟨⟨⟨hs1, _⟩, hs_cop_ins⟩, ⟨⟨hm1, hm_le_div⟩, hm_sm_P⟩⟩
      have hsm_le : s * m ≤ T := by
        rw [mul_comm]
        exact (Nat.le_div_iff_mul_le (by omega)).mp hm_le_div
      have hsm_ge : 1 ≤ s * m := Nat.mul_pos (by omega) (by omega)
      have hs_cop_p : Nat.Coprime s p :=
        ((coprime_primeProductModulus_insert_iff_aux hp_not_mem s).mp hs_cop_ins).1
      have hm_cop_p : Nat.Coprime m p := by
        rw [Nat.coprime_comm, hp.coprime_iff_not_dvd]
        intro hdvd
        exact hp_not_mem (hm_sm_P.2 p hp hdvd)
      have hsm_cop_p : Nat.Coprime (s * m) (primeProductModulus {p}) := by
        simpa [primeProductModulus] using coprime_mul_left_nat_aux hs_cop_p hm_cop_p
      exact ⟨⟨hsm_ge, hsm_le⟩, hsm_cop_p⟩
    · rintro ⟨s1, m1⟩ h1 ⟨s2, m2⟩ h2 h_eq
      simp only [Finset.mem_sigma, coprimeCutoffFinset, smoothCutoffFinset,
        Finset.mem_filter, Finset.mem_Icc] at h1 h2
      rcases h1 with ⟨⟨⟨hs1_ge, _⟩, hs1_cop_ins⟩, ⟨⟨hm1_ge, _⟩, hm1_sm⟩⟩
      rcases h2 with ⟨⟨⟨_, _⟩, hs2_cop_ins⟩, ⟨⟨_, _⟩, hm2_sm⟩⟩
      have hs1_cop_P : Nat.Coprime s1 (primeProductModulus P) :=
        ((coprime_primeProductModulus_insert_iff_aux hp_not_mem s1).mp hs1_cop_ins).2
      have hs2_cop_P : Nat.Coprime s2 (primeProductModulus P) :=
        ((coprime_primeProductModulus_insert_iff_aux hp_not_mem s2).mp hs2_cop_ins).2
      have h_pos : 0 < m1 * s1 := Nat.mul_pos (by omega) (by omega)
      obtain ⟨_, h_uniq, _⟩ := smooth_coprime_positive_factorization_exists_unique_nat hP h_pos
      obtain ⟨hm1_eq, hs1_eq⟩ := h_uniq m1 s1 rfl hm1_sm hs1_cop_P
      have h_comm : m2 * s2 = m1 * s1 := by linarith [mul_comm s1 m1, mul_comm s2 m2]
      obtain ⟨hm2_eq, hs2_eq⟩ := h_uniq m2 s2 h_comm hm2_sm hs2_cop_P
      exact Sigma.ext (hs1_eq.trans hs2_eq.symm) (heq_of_eq (hm1_eq.trans hm2_eq.symm))
    · intro r hr
      simp only [coprimeCutoffFinset, Finset.mem_filter, Finset.mem_Icc] at hr
      rcases hr with ⟨⟨hr1, hrT⟩, hr_cop_p_mod⟩
      have hr_cop_p : Nat.Coprime r p := by simpa [primeProductModulus] using hr_cop_p_mod
      obtain ⟨⟨h_mul_r, hm_sm, hs_cop_P, hs_pos⟩, _, _⟩ :=
        smooth_coprime_positive_factorization_exists_unique_nat hP (n := r) (by omega)
      let s := pCoprimePart P r
      let m := pSmoothPart P r
      have hsm_eq_r : s * m = r := by dsimp [s, m]; rw [mul_comm]; exact h_mul_r
      have hs_dvd_r : s ∣ r := ⟨m, hsm_eq_r.symm⟩
      have hs_cop_p : Nat.Coprime s p := hr_cop_p.coprime_dvd_left hs_dvd_r
      have hs_cop_ins : Nat.Coprime s (primeProductModulus (insert p P)) :=
        (coprime_primeProductModulus_insert_iff_aux hp_not_mem s).mpr ⟨hs_cop_p, hs_cop_P⟩
      have hs_le_r : s ≤ r := by rw [← hsm_eq_r]; exact Nat.le_mul_of_pos_right s hm_sm.1
      have hm_le_div : m ≤ T / s := (Nat.le_div_iff_mul_le hs_pos).mpr (by rw [mul_comm]; exact hsm_eq_r.symm ▸ hrT)
      refine ⟨⟨s, m⟩, ?_, hsm_eq_r⟩
      simp only [Finset.mem_sigma, coprimeCutoffFinset, smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc]
      exact ⟨⟨⟨hs_pos, le_trans hs_le_r hrT⟩, hs_cop_ins⟩, ⟨⟨hm_sm.1, hm_le_div⟩, hm_sm⟩⟩
    · rintro ⟨s, m⟩ _
      have h_ch : ∀ k : ℕ, gaussianPrimeChain T p s m X k = gaussianPrimeChain T p (s * m) 1 X k := by
        intro k
        simp [gaussianPrimeChain]
      have h_alt : gaussianAlternatingChainSum T p s m X = gaussianAlternatingChainSum T p (s * m) 1 X := by
        dsimp [gaussianAlternatingChainSum]
        apply Finset.sum_congr rfl
        intro k _
        rw [h_ch k]
      rw [h_alt]
      congr 1
      apply Finset.sum_congr rfl
      intro k _
      rw [h_ch k]
  have h_empty_prime : ∀ q ∈ (∅ : Finset ℕ), q.Prime := fun _ hq => False.elim (Finset.not_mem_empty _ hq)
  have hp_not_empty : p ∉ (∅ : Finset ℕ) := Finset.not_mem_empty p
  obtain ⟨⟨h_end_empty, _⟩, _, _, _⟩ :=
    finite_prime_adjoining_fiber_and_pointwise_telescoping_tc056 h_empty_prime hp hp_not_empty T hX
  have h_c_empty_eq_diff :
      pointwiseContractionC ∅ p T X = pointwiseDiagonalD T X - pointwiseGroupedEnergyV {p} T X := by
    have h_de := h_delta_decomp_gen h_empty_prime hp_not_empty
    rw [h_m_empty, zero_sub] at h_de
    dsimp [pointwiseDelta] at h_de
    rw [h_end_empty] at h_de
    linarith
  have h_c_empty_sum1 :
      pointwiseContractionC ∅ p T X =
        ∑ r ∈ coprimeCutoffFinset {p} T,
          ((∑ k ∈ Finset.range (T + 1), (gaussianPrimeChain T p r 1 X k) ^ 2) -
            (gaussianAlternatingChainSum T p r 1 X) ^ 2) := by
    dsimp [pointwiseContractionC]
    apply Finset.sum_congr rfl
    intro r hr
    have hr_mem := (Finset.mem_filter.mp hr).1
    rw [Finset.mem_Icc] at hr_mem
    have hdiv_ge1 : 1 ≤ T / r := (Nat.le_div_iff_mul_le (by omega)).mpr (by omega)
    have hs_empty : smoothCutoffFinset ∅ (T / r) = {1} := by
      ext u
      simp only [smoothCutoffFinset, Finset.mem_filter, Finset.mem_Icc, isPSmooth_empty_iff_aux,
        Finset.mem_singleton]
      exact ⟨fun h => h.2, fun h => ⟨⟨by omega, by omega⟩, h⟩⟩
    rw [hs_empty, Finset.sum_singleton]
  have h_c_eq_empty : pointwiseContractionC P p T X = pointwiseContractionC ∅ p T X :=
    h_c_bij_r.trans h_c_empty_sum1.symm
  have h_c_eq_diff :
      pointwiseContractionC P p T X = pointwiseDiagonalD T X - pointwiseGroupedEnergyV {p} T X :=
    h_c_eq_empty.trans h_c_empty_eq_diff
  refine ⟨⟨h_c_nn, h_m_empty⟩, h_delta_decomp, h_m_kl, ⟨h_c_eq_empty, h_c_eq_diff⟩, ?_⟩
  exact singleton_contraction_alternating_shift_aux hp T hX

/-! ### `TASK-TC-057`: Monotone Scale-Envelope Bootstrap (`CONDITIONAL_ON_RECURSION`), General Möbius–Rough Filtration Descent (Route A), Logarithmic Prime-Power Descent & Shift Hierarchy (Route B), Quadratic Prime-Power Square Decomposition (Route D), and Inherited-vs-Canonical Cutoff Comparison -/

/-- Monotone scale envelope `F(Y) := sup_{1 ≤ Z ≤ Y} E(Z)` defined via conditional supremum `sSup` on `ℝ`. -/
noncomputable def monotoneScaleEnvelope (E : ℝ → ℝ) (Y : ℝ) : ℝ :=
  sSup (E '' Set.Icc 1 Y)

/-- General finite `T`-truncated Gaussian sum `Q_{a,T}(X) := ∑_{1 ≤ n ≤ T} a(n) φ_n(X)` for arbitrary real weights `a`. -/
noncomputable def finiteQGeneral (a : ℕ → ℝ) (T : ℕ) (X : ℝ) : ℝ :=
  ∑ n ∈ Finset.Icc 1 T, a n * gaussianTermPhi n X

/-- Finite set of primes strictly below `U`: `{2 ≤ p < U : p.Prime}`. -/
def smoothPrimeSetBelow (U : ℕ) : Finset ℕ :=
  (Finset.Ico 2 U).filter Nat.Prime

/-- Finite set of primes in the rough band `[U, T]`: `{U ≤ p ≤ T : p.Prime}`. -/
def roughPrimeSetBand (U T : ℕ) : Finset ℕ :=
  (Finset.Icc U T).filter Nat.Prime

/-- Smooth below-`U` finite Gaussian sum `S_{a,<U,T}(X) := ∑_{1 ≤ n ≤ T, n ∈ S(P_{<U})} a(n) φ_n(X)`. -/
noncomputable def finiteQSmoothBelow (a : ℕ → ℝ) (U T : ℕ) (X : ℝ) : ℝ :=
  ∑ n ∈ smoothCutoffFinset (smoothPrimeSetBelow U) T, a n * gaussianTermPhi n X

/-- Finite set of squarefree divisors `d ∣ N_{[U,T]}` satisfying `U ≤ d ≤ T`. -/
def roughSquarefreeDivisorsBand (U T : ℕ) : Finset ℕ :=
  ((primeProductModulus (roughPrimeSetBand U T)).divisors).filter (fun d => U ≤ d ∧ d ≤ T)

/-- Finite set of prime-power pairs `{(p, k) : p ∈ primesUpToFinset T, 1 ≤ k ≤ T, p^k ≤ T}`. -/
def primePowerPairsUpTo (T : ℕ) : Finset (ℕ × ℕ) :=
  (primesUpToFinset T ×ˢ Finset.Icc 1 T).filter (fun pk => pk.1 ^ pk.2 ≤ T)

/-- Scale-invariant logarithmic-shift Gaussian observable
    `Q_{a,L}^{[m]}(X) := ∑_{1 ≤ q ≤ L} a(q) (log(X / q))^m φ_q(X)` (`m = 0` gives `finiteQGeneral a L X`). -/
noncomputable def finiteQShifted (a : ℕ → ℝ) (m T : ℕ) (X : ℝ) : ℝ :=
  ∑ n ∈ Finset.Icc 1 T, a n * (Real.log (X / (n : ℝ))) ^ m * gaussianTermPhi n X

/-- Prime-power logarithmic descent sum at shift order `m`:
    `Σ_{a,pp}^{[m]}(X; T) := ∑_{(p,k) ∈ primePowerPairsUpTo T} a(p)^k log(p) p^{-k/2} Q_{a,⌊T/p^k⌋}^{[m]}(X / p^k)`. -/
noncomputable def primePowerLogDescentSum (a : ℕ → ℝ) (m T : ℕ) (X : ℝ) : ℝ :=
  ∑ pk ∈ primePowerPairsUpTo T,
    (a pk.1) ^ pk.2 * Real.log (pk.1 : ℝ) *
      (1 / Real.sqrt ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
      finiteQShifted a m (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ))

/-- Individual Liouville (`m = 0`) prime-power cofactor summand
    `(-1)^k log(p) p^{-k/2} Q_{λ,⌊T/p^k⌋}(X / p^k)`. -/
noncomputable def liouvillePrimePowerTerm (T : ℕ) (pk : ℕ × ℕ) (X : ℝ) : ℝ :=
  (-1 : ℝ) ^ pk.2 * Real.log (pk.1 : ℝ) *
    (1 / Real.sqrt ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
    finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ))

/-- Canonical upper cutoff `T(Y) := ⌈Y^{5/4}⌉₊`. -/
noncomputable def canonicalCutoffT (Y : ℝ) : ℕ :=
  Nat.ceil (Y ^ (5 / 4 : ℝ))

/-- Inherited cofactor cutoff `L_d(Y) := ⌊T(Y) / d⌋ = canonicalCutoffT Y / d`. -/
noncomputable def inheritedCutoffL (Y : ℝ) (d : ℕ) : ℕ :=
  canonicalCutoffT Y / d

/-- Helper: local boundedness, nonnegativity, linear upper bound, and monotonicity of `monotoneScaleEnvelope`
    without assuming continuity of `E`. -/
private theorem monotoneScaleEnvelope_basic_props_aux
    {E : ℝ → ℝ} {M_lin : ℝ}
    (hE_nn : ∀ Z : ℝ, 1 ≤ Z → 0 ≤ E Z)
    (hM_nn : 0 ≤ M_lin)
    (hE_lin : ∀ Z : ℝ, 1 ≤ Z → E Z ≤ M_lin * Z) :
    (∀ Y : ℝ, 1 ≤ Y →
      (E '' Set.Icc 1 Y).Nonempty ∧
        BddAbove (E '' Set.Icc 1 Y) ∧
        0 ≤ monotoneScaleEnvelope E Y ∧
        monotoneScaleEnvelope E Y ≤ M_lin * Y ∧
        (∀ Z ∈ Set.Icc 1 Y, E Z ≤ monotoneScaleEnvelope E Y)) ∧
    (∀ Y₁ Y₂ : ℝ, 1 ≤ Y₁ → Y₁ ≤ Y₂ → monotoneScaleEnvelope E Y₁ ≤ monotoneScaleEnvelope E Y₂) := by
  have h_pt : ∀ Y : ℝ, 1 ≤ Y →
      (E '' Set.Icc 1 Y).Nonempty ∧
        BddAbove (E '' Set.Icc 1 Y) ∧
        0 ≤ monotoneScaleEnvelope E Y ∧
        monotoneScaleEnvelope E Y ≤ M_lin * Y ∧
        (∀ Z ∈ Set.Icc 1 Y, E Z ≤ monotoneScaleEnvelope E Y) := by
    intro Y hY
    have h_ne : (E '' Set.Icc 1 Y).Nonempty := ⟨E 1, 1, ⟨le_refl 1, hY⟩, rfl⟩
    have h_bdd : BddAbove (E '' Set.Icc 1 Y) := by
      refine ⟨M_lin * Y, ?_⟩
      rintro _ ⟨Z, ⟨hZ1, hZY⟩, rfl⟩
      exact le_trans (hE_lin Z hZ1) (mul_le_mul_of_nonneg_left hZY hM_nn)
    have h_ub_Z : ∀ Z ∈ Set.Icc 1 Y, E Z ≤ monotoneScaleEnvelope E Y := by
      intro Z hZ
      exact le_csSup h_bdd ⟨Z, hZ, rfl⟩
    have h_nn : 0 ≤ monotoneScaleEnvelope E Y :=
      le_trans (hE_nn 1 (le_refl 1)) (h_ub_Z 1 ⟨le_refl 1, hY⟩)
    have h_le_lin : monotoneScaleEnvelope E Y ≤ M_lin * Y := by
      apply csSup_le h_ne
      rintro _ ⟨Z, ⟨hZ1, hZY⟩, rfl⟩
      exact le_trans (hE_lin Z hZ1) (mul_le_mul_of_nonneg_left hZY hM_nn)
    exact ⟨h_ne, h_bdd, h_nn, h_le_lin, h_ub_Z⟩
  refine ⟨h_pt, ?_⟩
  intro Y₁ Y₂ hY1 hY12
  obtain ⟨h_ne1, _, _, _, _⟩ := h_pt Y₁ hY1
  obtain ⟨_, _, _, _, h_ub2⟩ := h_pt Y₂ (le_trans hY1 hY12)
  apply csSup_le h_ne1
  rintro _ ⟨Z, ⟨hZ1, hZY1⟩, rfl⟩
  exact h_ub2 Z ⟨hZ1, le_trans hZY1 hY12⟩

/-- **Theorem 21 (`TASK-TC-057` §3, Monotone Scale-Envelope Boundedness, `E`-to-`F` Passage, `CONDITIONAL_ON_RECURSION` Polylog Bootstrap Descent, and Weighted Contraction/Obstruction Algebra)**:
    *Formal scope (`CONDITIONAL_ON_RECURSION`)*: Establishes unconditional local boundedness and monotonicity of
    `monotoneScaleEnvelope E Y = sup_{1 ≤ Z ≤ Y} E(Z)` without continuity of `E` (accommodating discontinuous
    `T(Z) = ⌈Z^{5/4}⌉`), the justified passage from a pointwise `E`-inequality to the envelope `F`-inequality,
    the abstract descent from `F(Y) ≤ A_η Y^η + B_η F(Y / U_η(Y))` (`B_η` NOT required `< 1`) to
    `F(Y) ≤ (F(Y_*) + 2 A_η) Y^ε` and `E(Y) ≤ (F(Y_*) + 2 A_η) Y^ε` for all `Y ≥ 1`, and the weighted multi-scale
    contraction step together with the homogeneous lower-bound obstruction explaining why `(log Y)^b` coefficient
    mass or positive base-scale energy blocks contraction below `b / a`. Does NOT assert the unproved arithmetic
    recursion for `E_{T(Y)}(Y)`. -/
theorem abstract_polylog_scale_bootstrap_and_weighted_contraction_tc057
    {E : ℝ → ℝ} {M_lin : ℝ}
    (hE_nn : ∀ Z : ℝ, 1 ≤ Z → 0 ≤ E Z)
    (hM_nn : 0 ≤ M_lin)
    (hE_lin : ∀ Z : ℝ, 1 ≤ Z → E Z ≤ M_lin * Z) :
    ((∀ Y : ℝ, 1 ≤ Y →
        BddAbove (E '' Set.Icc 1 Y) ∧
          0 ≤ monotoneScaleEnvelope E Y ∧
          monotoneScaleEnvelope E Y ≤ M_lin * Y ∧
          (∀ Z ∈ Set.Icc 1 Y, E Z ≤ monotoneScaleEnvelope E Y)) ∧
      (∀ Y₁ Y₂ : ℝ, 1 ≤ Y₁ → Y₁ ≤ Y₂ → monotoneScaleEnvelope E Y₁ ≤ monotoneScaleEnvelope E Y₂)) ∧
    (∀ (Y_0 η A_η B_η : ℝ) (U_η : ℝ → ℝ),
      1 ≤ Y_0 → 0 ≤ η → 0 ≤ A_η → 0 ≤ B_η →
      (∀ Z : ℝ, Y_0 ≤ Z → E Z ≤ A_η * Z ^ η + B_η * monotoneScaleEnvelope E (Z / U_η Z)) →
      (∀ Y Z : ℝ, Y_0 ≤ Z → Z ≤ Y → 1 ≤ Z / U_η Z ∧ Z / U_η Z ≤ Y / U_η Y) →
      ∀ Y : ℝ, Y_0 ≤ Y →
        monotoneScaleEnvelope E Y ≤
          max (monotoneScaleEnvelope E Y_0 * Y_0 ^ (-η)) A_η * Y ^ η +
            B_η * monotoneScaleEnvelope E (Y / U_η Y)) ∧
    (∀ (η ε A_η B_η Y_star : ℝ) (U_η : ℝ → ℝ),
      0 < η → η < ε → 0 ≤ A_η → 0 ≤ B_η → 1 ≤ Y_star →
      (∀ Y : ℝ, Y_star ≤ Y →
        monotoneScaleEnvelope E Y ≤ A_η * Y ^ η + B_η * monotoneScaleEnvelope E (Y / U_η Y)) →
      (∀ Y : ℝ, Y_star ≤ Y →
        2 ≤ U_η Y ∧ U_η Y ≤ Y ∧ B_η * (U_η Y) ^ (-ε) ≤ 1 / 2) →
      ∀ Y : ℝ, 1 ≤ Y →
        monotoneScaleEnvelope E Y ≤ (monotoneScaleEnvelope E Y_star + 2 * A_η) * Y ^ ε ∧
          E Y ≤ (monotoneScaleEnvelope E Y_star + 2 * A_η) * Y ^ ε) ∧
    (∀ (S : Finset ℕ) (w u : ℕ → ℝ) (Y η sig A C m_0 U_max : ℝ),
      ((1 ≤ Y → 0 ≤ η → η ≤ sig → 0 ≤ A → 0 ≤ C → 2 * A ≤ C →
          (∀ i ∈ S, 0 ≤ w i ∧ 0 < u i ∧ monotoneScaleEnvelope E (Y / u i) ≤ C * (Y / u i) ^ sig) →
          (∑ i ∈ S, w i * (u i) ^ (-sig)) ≤ 1 / 2 →
          A * Y ^ η + (∑ i ∈ S, w i * monotoneScaleEnvelope E (Y / u i)) ≤ C * Y ^ sig) ∧
        (0 ≤ Y → 0 ≤ sig → 0 ≤ m_0 → 1 ≤ U_max →
          (∀ i ∈ S, 0 ≤ w i ∧ 1 ≤ u i ∧ u i ≤ U_max ∧
            m_0 * (Y / u i) ^ sig ≤ monotoneScaleEnvelope E (Y / u i)) →
          m_0 * (∑ i ∈ S, w i) * U_max ^ (-sig) * Y ^ sig ≤
            ∑ i ∈ S, w i * monotoneScaleEnvelope E (Y / u i)))) := by
  obtain ⟨h_pt, h_mono⟩ := monotoneScaleEnvelope_basic_props_aux hE_nn hM_nn hE_lin
  refine ⟨⟨fun Y hY => (h_pt Y hY).2, h_mono⟩, ?_, ?_, ?_⟩
  · intro Y_0 η A_η B_η U_η hY0 hη hA hB hE_rec hU_cmp Y hYY0
    have hY1 : 1 ≤ Y := le_trans hY0 hYY0
    obtain ⟨h_ne, _, _, _, _⟩ := h_pt Y hY1
    let A_tilde := max (monotoneScaleEnvelope E Y_0 * Y_0 ^ (-η)) A_η
    have hWY1 : 1 ≤ Y / U_η Y := (hU_cmp Y Y hYY0 (le_refl Y)).1
    have hFW_nn : 0 ≤ monotoneScaleEnvelope E (Y / U_η Y) := (h_pt (Y / U_η Y) hWY1).2.2.1
    apply csSup_le h_ne
    rintro _ ⟨Z, ⟨hZ1, hZY⟩, rfl⟩
    by_cases hZY0 : Z ≤ Y_0
    · have hEZ_le_F0 : E Z ≤ monotoneScaleEnvelope E Y_0 :=
        (h_pt Y_0 hY0).2.2.2.2 Z ⟨hZ1, hZY0⟩
      have hY0_pos : 0 < Y_0 := by linarith
      have h_cancel : Y_0 ^ (-η) * Y_0 ^ η = 1 := by
        rw [← Real.rpow_add hY0_pos, neg_add_self, Real.rpow_zero]
      have hF0_eq : monotoneScaleEnvelope E Y_0 =
          (monotoneScaleEnvelope E Y_0 * Y_0 ^ (-η)) * Y_0 ^ η := by
        rw [mul_assoc, h_cancel, mul_one]
      have hY0_le_Y_pow : Y_0 ^ η ≤ Y ^ η :=
        Real.rpow_le_rpow (by linarith) hYY0 hη
      have h_first : (monotoneScaleEnvelope E Y_0 * Y_0 ^ (-η)) * Y_0 ^ η ≤ A_tilde * Y ^ η := by
        have h1 : monotoneScaleEnvelope E Y_0 * Y_0 ^ (-η) ≤ A_tilde := le_max_left _ _
        have hA_tilde_nn : 0 ≤ A_tilde := le_trans hA (le_max_right _ _)
        have hY0_pow_nn : 0 ≤ Y_0 ^ η := Real.rpow_nonneg (by linarith) η
        exact le_trans (mul_le_mul_of_nonneg_right h1 hY0_pow_nn)
          (mul_le_mul_of_nonneg_left hY0_le_Y_pow hA_tilde_nn)
      have h_nonneg_tail : 0 ≤ B_η * monotoneScaleEnvelope E (Y / U_η Y) := mul_nonneg hB hFW_nn
      linarith
    · have hY0Z : Y_0 ≤ Z := le_of_not_ge hZY0
      have hrecZ := hE_rec Z hY0Z
      obtain ⟨hWZ1, hWZ_le_WY⟩ := hU_cmp Y Z hY0Z hZY
      have hF_le : monotoneScaleEnvelope E (Z / U_η Z) ≤ monotoneScaleEnvelope E (Y / U_η Y) :=
        h_mono _ _ hWZ1 hWZ_le_WY
      have hZ_pow : Z ^ η ≤ Y ^ η := Real.rpow_le_rpow (by linarith) hZY hη
      have hA_le : A_η ≤ A_tilde := le_max_right _ _
      have hA_term : A_η * Z ^ η ≤ A_tilde * Y ^ η :=
        mul_le_mul hA_le hZ_pow (Real.rpow_nonneg (by linarith) η) (le_trans hA hA_le)
      have hB_term : B_η * monotoneScaleEnvelope E (Z / U_η Z) ≤
          B_η * monotoneScaleEnvelope E (Y / U_η Y) :=
        mul_le_mul_of_nonneg_left hF_le hB
      linarith
  · intro η ε A_η B_η Y_star U_η hη_pos hηε hA hB hY_star h_rec h_U Y hY1
    let F_star := monotoneScaleEnvelope E Y_star
    have hF_star_nn : 0 ≤ F_star := (h_pt Y_star hY_star).2.2.1
    let C_ε := F_star + 2 * A_η
    have hC_nn : 0 ≤ C_ε := by dsimp [C_ε]; linarith
    have hε_pos : 0 < ε := lt_trans hη_pos hηε
    have h_ind : ∀ k : ℕ, ∀ Z : ℝ, 1 ≤ Z → Z ≤ (2 : ℝ) ^ k * Y_star →
        monotoneScaleEnvelope E Z ≤ C_ε * Z ^ ε := by
      intro k
      induction' k with k ih
      · intro Z hZ1 hZ_le
        have hZ_le_star : Z ≤ Y_star := by simpa using hZ_le
        have hFZ_le : monotoneScaleEnvelope E Z ≤ F_star := h_mono Z Y_star hZ1 hZ_le_star
        have h1_le_Zpow : (1 : ℝ) ≤ Z ^ ε := Real.one_le_rpow hZ1 (le_of_lt hε_pos)
        have hF_le_C : F_star ≤ C_ε := by dsimp [C_ε]; linarith
        calc
          monotoneScaleEnvelope E Z ≤ F_star := hFZ_le
          _ ≤ C_ε * 1 := by linarith
          _ ≤ C_ε * Z ^ ε := mul_le_mul_of_nonneg_left h1_le_Zpow hC_nn
      · intro Z hZ1 hZ_le
        by_cases hZ_star : Z ≤ Y_star
        · have hFZ_le : monotoneScaleEnvelope E Z ≤ F_star := h_mono Z Y_star hZ1 hZ_star
          have h1_le_Zpow : (1 : ℝ) ≤ Z ^ ε := Real.one_le_rpow hZ1 (le_of_lt hε_pos)
          have hF_le_C : F_star ≤ C_ε := by dsimp [C_ε]; linarith
          calc
            monotoneScaleEnvelope E Z ≤ F_star := hFZ_le
            _ ≤ C_ε * 1 := by linarith
            _ ≤ C_ε * Z ^ ε := mul_le_mul_of_nonneg_left h1_le_Zpow hC_nn
        · have hY_star_le_Z : Y_star ≤ Z := le_of_not_ge hZ_star
          obtain ⟨hU2, hUZ, hBU⟩ := h_U Z hY_star_le_Z
          have hU_pos : 0 < U_η Z := by linarith
          have hZ_nn : 0 ≤ Z := by linarith
          let W := Z / U_η Z
          have hW1 : 1 ≤ W := (one_le_div hU_pos).mpr hUZ
          have hW_half : W ≤ Z / 2 := div_le_div_of_nonneg_left hZ_nn (by norm_num) hU2
          have hW_dyad : W ≤ (2 : ℝ) ^ k * Y_star := by
            have h_pow : (2 : ℝ) ^ (k + 1) * Y_star = 2 * ((2 : ℝ) ^ k * Y_star) := by
              rw [pow_succ']
              ring
            linarith
          have hFW := ih W hW1 hW_dyad
          have hW_pow : W ^ ε = Z ^ ε * (U_η Z) ^ (-ε) := by
            dsimp [W]
            rw [Real.div_rpow hZ_nn (le_of_lt hU_pos) ε, div_eq_mul_inv,
              Real.rpow_neg (le_of_lt hU_pos)]
          have hB_term : B_η * monotoneScaleEnvelope E W ≤ (1 / 2 : ℝ) * C_ε * Z ^ ε := by
            have h1 : B_η * monotoneScaleEnvelope E W ≤ B_η * (C_ε * (Z ^ ε * (U_η Z) ^ (-ε))) := by
              rw [← hW_pow]
              exact mul_le_mul_of_nonneg_left hFW hB
            have h2 : B_η * (C_ε * (Z ^ ε * (U_η Z) ^ (-ε))) =
                (C_ε * Z ^ ε) * (B_η * (U_η Z) ^ (-ε)) := by ring
            have hCZ_nn : 0 ≤ C_ε * Z ^ ε := mul_nonneg hC_nn (Real.rpow_nonneg hZ_nn ε)
            have h3 : (C_ε * Z ^ ε) * (B_η * (U_η Z) ^ (-ε)) ≤ (C_ε * Z ^ ε) * (1 / 2 : ℝ) :=
              mul_le_mul_of_nonneg_left hBU hCZ_nn
            calc
              B_η * monotoneScaleEnvelope E W
                ≤ B_η * (C_ε * (Z ^ ε * (U_η Z) ^ (-ε))) := h1
              _ = (C_ε * Z ^ ε) * (B_η * (U_η Z) ^ (-ε)) := h2
              _ ≤ (C_ε * Z ^ ε) * (1 / 2 : ℝ) := h3
              _ = (1 / 2 : ℝ) * C_ε * Z ^ ε := by ring
          have hZ_eta_le : Z ^ η ≤ Z ^ ε :=
            Real.rpow_le_rpow_of_exponent_le hZ1 (le_of_lt hηε)
          have hA_term : A_η * Z ^ η ≤ A_η * Z ^ ε :=
            mul_le_mul_of_nonneg_left hZ_eta_le hA
          have hrecZ := h_rec Z hY_star_le_Z
          have hZ_eps_nn : 0 ≤ Z ^ ε := Real.rpow_nonneg hZ_nn ε
          have h_coeff : A_η + (1 / 2 : ℝ) * C_ε ≤ C_ε := by dsimp [C_ε]; linarith
          have h_comb : (A_η + (1 / 2 : ℝ) * C_ε) * Z ^ ε ≤ C_ε * Z ^ ε :=
            mul_le_mul_of_nonneg_right h_coeff hZ_eps_nn
          dsimp [W] at hB_term
          calc
            monotoneScaleEnvelope E Z
              ≤ A_η * Z ^ η + B_η * monotoneScaleEnvelope E (Z / U_η Z) := hrecZ
            _ ≤ A_η * Z ^ ε + (1 / 2 : ℝ) * C_ε * Z ^ ε := add_le_add hA_term hB_term
            _ = (A_η + (1 / 2 : ℝ) * C_ε) * Z ^ ε := by ring
            _ ≤ C_ε * Z ^ ε := h_comb
    let k0 := Nat.ceil (Y / Y_star)
    have hY_star_pos : 0 < Y_star := by linarith
    have hk0_ge : Y / Y_star ≤ (k0 : ℝ) := Nat.le_ceil (Y / Y_star)
    have hk0_lt_pow_nat : k0 < 2 ^ k0 := Nat.lt_pow_self (by norm_num : 1 < 2) k0
    have hk0_le_pow : (k0 : ℝ) ≤ (2 : ℝ) ^ k0 := by
      exact_mod_cast le_of_lt hk0_lt_pow_nat
    have hY_div_le : Y / Y_star ≤ (2 : ℝ) ^ k0 := le_trans hk0_ge hk0_le_pow
    have hY_le_dyad : Y ≤ (2 : ℝ) ^ k0 * Y_star := (div_le_iff hY_star_pos).mp hY_div_le
    have hFY := h_ind k0 Y hY1 hY_le_dyad
    have hEY_le_FY : E Y ≤ monotoneScaleEnvelope E Y :=
      (h_pt Y hY1).2.2.2.2 Y ⟨hY1, le_refl Y⟩
    exact ⟨hFY, le_trans hEY_le_FY hFY⟩
  · intro S w u Y η sig A C m_0 U_max
    constructor
    · intro hY1 _ hησ hA hC h2AC h_terms h_theta
      have hY_nn : 0 ≤ Y := by linarith
      have hY_sig_nn : 0 ≤ Y ^ sig := Real.rpow_nonneg hY_nn sig
      have h_sum_le :
          ∑ i ∈ S, w i * monotoneScaleEnvelope E (Y / u i) ≤
            (C * Y ^ sig) * ∑ i ∈ S, w i * (u i) ^ (-sig) := by
        rw [Finset.mul_sum]
        apply Finset.sum_le_sum
        intro i hi
        obtain ⟨hwi_nn, hui_pos, hFi⟩ := h_terms i hi
        have h_pow_div : (Y / u i) ^ sig = Y ^ sig * (u i) ^ (-sig) := by
          rw [Real.div_rpow hY_nn (le_of_lt hui_pos) sig, div_eq_mul_inv,
            Real.rpow_neg (le_of_lt hui_pos)]
        calc
          w i * monotoneScaleEnvelope E (Y / u i)
            ≤ w i * (C * (Y / u i) ^ sig) := mul_le_mul_of_nonneg_left hFi hwi_nn
          _ = (C * Y ^ sig) * (w i * (u i) ^ (-sig)) := by rw [h_pow_div]; ring
      have hCY_nn : 0 ≤ C * Y ^ sig := mul_nonneg hC hY_sig_nn
      have h_sum_half : (C * Y ^ sig) * (∑ i ∈ S, w i * (u i) ^ (-sig)) ≤ (C * Y ^ sig) * (1 / 2 : ℝ) :=
        mul_le_mul_of_nonneg_left h_theta hCY_nn
      have hY_eta_le : Y ^ η ≤ Y ^ sig := Real.rpow_le_rpow_of_exponent_le hY1 hησ
      have hA_le : A * Y ^ η ≤ A * Y ^ sig := mul_le_mul_of_nonneg_left hY_eta_le hA
      have h_coeff : (A + (1 / 2 : ℝ) * C) * Y ^ sig ≤ C * Y ^ sig :=
        mul_le_mul_of_nonneg_right (by linarith) hY_sig_nn
      linarith
    · intro hY_nn hσ_nn hm0_nn hUmax1 h_terms
      have hUmax_pos : 0 < U_max := by linarith
      have h_lhs_sum :
          m_0 * (∑ i ∈ S, w i) * U_max ^ (-sig) * Y ^ sig =
            ∑ i ∈ S, w i * (m_0 * Y ^ sig * U_max ^ (-sig)) := by
        have h_rearr :
            m_0 * (∑ i ∈ S, w i) * U_max ^ (-sig) * Y ^ sig =
              (∑ i ∈ S, w i) * (m_0 * Y ^ sig * U_max ^ (-sig)) := by ring
        rw [h_rearr, Finset.sum_mul]
      rw [h_lhs_sum]
      apply Finset.sum_le_sum
      intro i hi
      obtain ⟨hwi_nn, hui1, hui_le_max, hFi_ge⟩ := h_terms i hi
      have hui_pos : 0 < u i := by linarith
      have h_u_pow_le : (u i) ^ sig ≤ U_max ^ sig :=
        Real.rpow_le_rpow (le_of_lt hui_pos) hui_le_max hσ_nn
      have h_neg_pow_ge : U_max ^ (-sig) ≤ (u i) ^ (-sig) := by
        rw [Real.rpow_neg hUmax_pos.le, Real.rpow_neg (le_of_lt hui_pos)]
        exact inv_le_inv_of_le (Real.rpow_pos_of_pos hui_pos sig) h_u_pow_le
      have h_div_pow : (Y / u i) ^ sig = Y ^ sig * (u i) ^ (-sig) := by
        rw [Real.div_rpow hY_nn (le_of_lt hui_pos) sig, div_eq_mul_inv,
          Real.rpow_neg (le_of_lt hui_pos)]
      have hmY_nn : 0 ≤ m_0 * Y ^ sig := mul_nonneg hm0_nn (Real.rpow_nonneg hY_nn sig)
      have h_step1 : m_0 * Y ^ sig * U_max ^ (-sig) ≤ m_0 * (Y / u i) ^ sig := by
        rw [h_div_pow, ← mul_assoc]
        exact mul_le_mul_of_nonneg_left h_neg_pow_ge hmY_nn
      exact mul_le_mul_of_nonneg_left (le_trans h_step1 hFi_ge) hwi_nn

/-- Helper: `(ArithmeticFunction.moebius d) ^ 2 = 1` for every divisor `d` of `primeProductModulus P` (`∀ p ∈ P, p.Prime`). -/
private theorem moebius_sq_eq_one_of_dvd_primeProductModulus_aux
    {P : Finset ℕ} (hP : ∀ p ∈ P, p.Prime) {d : ℕ} (hdvd : d ∣ primeProductModulus P) :
    (ArithmeticFunction.moebius d) ^ 2 = 1 := by
  induction' P using Finset.induction_on with p s hp_not_s ih generalizing d
  · have hmod1 : primeProductModulus ∅ = 1 := rfl
    rw [hmod1] at hdvd
    have hd1 : d = 1 := Nat.dvd_one.mp hdvd
    subst hd1
    simp [ArithmeticFunction.moebius_apply_one]
  · have hp : p.Prime := hP p (Finset.mem_insert_self p s)
    have hs_prime : ∀ q ∈ s, q.Prime := fun q hq => hP q (Finset.mem_insert_of_mem hq)
    have h_mod_ins : primeProductModulus (insert p s) = p * primeProductModulus s := by
      dsimp [primeProductModulus]
      exact Finset.prod_insert hp_not_s
    rw [h_mod_ins] at hdvd
    have hcop_ps : Nat.Coprime p (primeProductModulus s) := by
      rw [hp.coprime_iff_not_dvd]
      intro hp_dvd_mod
      obtain ⟨q, hq_in_s, hp_dvd_q⟩ := prime_dvd_finset_prod_aux hp s (fun x => x) hp_dvd_mod
      have hq_prime : q.Prime := hs_prime q hq_in_s
      have hpq : p = q := (Nat.dvd_prime hq_prime).mp hp_dvd_q |>.resolve_left hp.ne_one
      exact hp_not_s (hpq ▸ hq_in_s)
    by_cases hpd : p ∣ d
    · obtain ⟨k, rfl⟩ := hpd
      have hk_dvd_s : k ∣ primeProductModulus s :=
        (Nat.mul_dvd_mul_iff_left hp.pos).mp hdvd
      have hcop_pk : Nat.Coprime p k := hcop_ps.coprime_dvd_right hk_dvd_s
      have hmu_mul : ArithmeticFunction.moebius (p * k) =
          ArithmeticFunction.moebius p * ArithmeticFunction.moebius k :=
        ArithmeticFunction.isMultiplicative_moebius.2 hcop_pk
      have hmu_p : (ArithmeticFunction.moebius p) ^ 2 = 1 := by
        rw [ArithmeticFunction.moebius_apply_prime hp]
        norm_num
      have hmu_k : (ArithmeticFunction.moebius k) ^ 2 = 1 := ih hs_prime hk_dvd_s
      rw [hmu_mul, mul_pow, hmu_p, hmu_k, one_mul]
    · have hcop_dp : Nat.Coprime d p := (hp.coprime_iff_not_dvd.mpr hpd).symm
      have hd_dvd_s : d ∣ primeProductModulus s := hcop_dp.dvd_of_dvd_mul_left hdvd
      exact ih hs_prime hd_dvd_s

/-- **Theorem 22 (`TASK-TC-057` §4 Route A, General Möbius–Rough Prime-Filtration Descent, Uniform Liouville Sign, Parity-Control Contrast, and Super-`√T` Reduction)**:
    For every prime threshold `U ≥ 2`, cutoff `T : ℕ`, `X ≥ 0`, and completely multiplicative weight
    `a : ℕ → ℝ` (`∀ d q, 0 < d → 0 < q → a (d * q) = a d * a q`):
    1. Exact smooth/coprime equivalence on `[1, T]`:
       `smoothCutoffFinset (smoothPrimeSetBelow U) T = coprimeCutoffFinset (roughPrimeSetBand U T) T`;
    2. Exact general Möbius–rough descent identity across ALL `U ≥ 2` (including `U ≪ √T`, where composite
       squarefree products of primes in `[U, T]` enter):
       `finiteQGeneral a T X = finiteQSmoothBelow a U T X - ∑ d ∈ roughSquarefreeDivisorsBand U T, ((ArithmeticFunction.moebius d : ℝ) * a d / Real.sqrt (d : ℝ)) * finiteQGeneral a (T / d) (X / (d : ℝ))`;
    3. Liouville specialization (`λ(p) = -1` at ALL primes `p`):
       `∀ d ∈ roughSquarefreeDivisorsBand U T, (ArithmeticFunction.moebius d : ℝ) * (liouvilleLambda d : ℝ) = 1`, hence
       `finiteQLambda T X = finiteQSmoothBelow (fun n => (liouvilleLambda n : ℝ)) U T X - ∑ d ∈ roughSquarefreeDivisorsBand U T, (1 / Real.sqrt (d : ℝ)) * finiteQLambda (T / d) (X / (d : ℝ))`;
    4. Super-`√T` prime reduction (`T < U^2 → roughSquarefreeDivisorsBand U T = roughPrimeSetBand U T`) and
       explicit `2`-adic parity control contrast on `[3, 15]`: `μ(3) a_2(3) = -1` vs `μ(15) a_2(15) = +1`, whereas
       `μ(3) λ(3) = +1` and `μ(15) λ(15) = +1`. -/
theorem general_moebius_rough_prime_filtration_descent_tc057
    {U : ℕ} (hU : 2 ≤ U) (T : ℕ) {X : ℝ} (hX : 0 ≤ X)
    {a : ℕ → ℝ} (ha_mult : ∀ d q : ℕ, 0 < d → 0 < q → a (d * q) = a d * a q) :
    (smoothCutoffFinset (smoothPrimeSetBelow U) T =
      coprimeCutoffFinset (roughPrimeSetBand U T) T) ∧
    (finiteQGeneral a T X =
      finiteQSmoothBelow a U T X -
        ∑ d ∈ roughSquarefreeDivisorsBand U T,
          ((ArithmeticFunction.moebius d : ℝ) * a d / Real.sqrt (d : ℝ)) *
            finiteQGeneral a (T / d) (X / (d : ℝ))) ∧
    ((∀ d ∈ roughSquarefreeDivisorsBand U T,
        (ArithmeticFunction.moebius d : ℝ) * (liouvilleLambda d : ℝ) = 1) ∧
      finiteQLambda T X =
        finiteQSmoothBelow (fun n => (liouvilleLambda n : ℝ)) U T X -
          ∑ d ∈ roughSquarefreeDivisorsBand U T,
            (1 / Real.sqrt (d : ℝ)) * finiteQLambda (T / d) (X / (d : ℝ))) ∧
    ((T < U ^ 2 → roughSquarefreeDivisorsBand U T = roughPrimeSetBand U T) ∧
      (ArithmeticFunction.moebius 3 * twoAdicParityControl 3 = -1 ∧
        ArithmeticFunction.moebius 15 * twoAdicParityControl 15 = 1 ∧
        ArithmeticFunction.moebius 3 * liouvilleLambda 3 = 1 ∧
        ArithmeticFunction.moebius 15 * liouvilleLambda 15 = 1)) := by
  let P_rough := roughPrimeSetBand U T
  let N_rough := primeProductModulus P_rough
  have hP_rough_prime : ∀ p ∈ P_rough, p.Prime := fun p hp => (Finset.mem_filter.mp hp).2
  have hN_rough_pos : 0 < N_rough := by
    dsimp [N_rough, primeProductModulus]
    apply Finset.prod_pos
    intro p hp
    exact (hP_rough_prime p hp).pos
  have h_set_eq :
      smoothCutoffFinset (smoothPrimeSetBelow U) T = coprimeCutoffFinset P_rough T := by
    ext n
    simp only [smoothCutoffFinset, coprimeCutoffFinset, Finset.mem_filter, Finset.mem_Icc]
    constructor
    · rintro ⟨⟨hn1, hnT⟩, ⟨_, h_sm⟩⟩
      refine ⟨⟨hn1, hnT⟩, ?_⟩
      rw [Nat.coprime_iff_gcd_eq_one]
      by_contra h_ne
      obtain ⟨q, hq_prime, hq_dvd_gcd⟩ := Nat.exists_prime_and_dvd h_ne
      have hq_dvd_n : q ∣ n := dvd_trans hq_dvd_gcd (Nat.gcd_dvd_left _ _)
      have hq_dvd_mod : q ∣ N_rough := dvd_trans hq_dvd_gcd (Nat.gcd_dvd_right _ _)
      have hq_below : q ∈ smoothPrimeSetBelow U := h_sm q hq_prime hq_dvd_n
      have hq_lt_U : q < U := ((Finset.mem_filter.mp hq_below).1 |> Finset.mem_Ico.mp).2
      obtain ⟨p, hp_in_rough, hq_dvd_p⟩ := prime_dvd_finset_prod_aux hq_prime P_rough (fun x => x) hq_dvd_mod
      have hp_prime : p.Prime := hP_rough_prime p hp_in_rough
      have hqp : q = p := (Nat.dvd_prime hp_prime).mp hq_dvd_p |>.resolve_left hq_prime.ne_one
      have hp_ge_U : U ≤ p := ((Finset.mem_filter.mp hp_in_rough).1 |> Finset.mem_Icc.mp).1
      omega
    · rintro ⟨⟨hn1, hnT⟩, hcop⟩
      refine ⟨⟨hn1, hnT⟩, ⟨by omega, ?_⟩⟩
      intro q hq_prime hq_dvd_n
      simp only [smoothPrimeSetBelow, Finset.mem_filter, Finset.mem_Ico]
      refine ⟨⟨hq_prime.two_le, ?_⟩, hq_prime⟩
      by_contra h_not_lt
      have hq_le_n : q ≤ n := Nat.le_of_dvd (by omega) hq_dvd_n
      have hq_in_rough : q ∈ P_rough := by
        simp only [P_rough, roughPrimeSetBand, Finset.mem_filter, Finset.mem_Icc]
        exact ⟨⟨by omega, le_trans hq_le_n hnT⟩, hq_prime⟩
      have hq_dvd_mod : q ∣ N_rough := Finset.dvd_prod_of_mem (fun x => x) hq_in_rough
      exact hq_prime.not_dvd_one (hcop.gcd_eq_one ▸ Nat.dvd_gcd hq_dvd_n hq_dvd_mod)
  have h_div_rough_ge_U : ∀ d : ℕ, d ∣ N_rough → d ≠ 1 → U ≤ d := by
    intro d hdvd hd_ne1
    have hd_pos : 0 < d := Nat.pos_of_dvd_of_pos hdvd hN_rough_pos
    obtain ⟨q, hq_prime, hq_dvd_d⟩ := Nat.exists_prime_and_dvd hd_ne1
    have hq_dvd_mod : q ∣ N_rough := dvd_trans hq_dvd_d hdvd
    obtain ⟨p, hp_in_rough, hq_dvd_p⟩ := prime_dvd_finset_prod_aux hq_prime P_rough (fun x => x) hq_dvd_mod
    have hp_prime : p.Prime := hP_rough_prime p hp_in_rough
    have hqp : q = p := (Nat.dvd_prime hp_prime).mp hq_dvd_p |>.resolve_left hq_prime.ne_one
    have hp_ge_U : U ≤ p := ((Finset.mem_filter.mp hp_in_rough).1 |> Finset.mem_Icc.mp).1
    have hq_le_d : q ≤ d := Nat.le_of_dvd hd_pos hq_dvd_d
    omega
  have h_gen_id :
      ∀ b : ℕ → ℝ, (∀ d q : ℕ, 0 < d → 0 < q → b (d * q) = b d * b q) →
        finiteQGeneral b T X =
          finiteQSmoothBelow b U T X -
            ∑ d ∈ roughSquarefreeDivisorsBand U T,
              ((ArithmeticFunction.moebius d : ℝ) * b d / Real.sqrt (d : ℝ)) *
                finiteQGeneral b (T / d) (X / (d : ℝ)) := by
    intro b hb_mult
    have h_smooth_sieve :
        finiteQSmoothBelow b U T X =
          ∑ n ∈ Finset.Icc 1 T,
            (∑ d ∈ (Nat.gcd n N_rough).divisors, (ArithmeticFunction.moebius d : ℝ)) *
              (b n * gaussianTermPhi n X) := by
      dsimp [finiteQSmoothBelow]
      rw [h_set_eq, coprimeCutoffFinset, Finset.sum_filter]
      apply Finset.sum_congr rfl
      intro n _
      have h_mu_int :
          (∑ d ∈ (Nat.gcd n N_rough).divisors, ArithmeticFunction.moebius d) =
            if Nat.gcd n N_rough = 1 then 1 else 0 := by
        have h_mul_zeta :
            (ArithmeticFunction.moebius * (ArithmeticFunction.zeta : ArithmeticFunction ℤ))
                (Nat.gcd n N_rough) =
              (1 : ArithmeticFunction ℤ) (Nat.gcd n N_rough) := by
          rw [ArithmeticFunction.moebius_mul_coe_zeta]
        rw [ArithmeticFunction.coe_mul_zeta_apply, ArithmeticFunction.one_apply] at h_mul_zeta
        exact h_mul_zeta
      have h_mu_real :
          (∑ d ∈ (Nat.gcd n N_rough).divisors, (ArithmeticFunction.moebius d : ℝ)) =
            if Nat.Coprime n N_rough then 1 else 0 := by
        have h_cast :
            (∑ d ∈ (Nat.gcd n N_rough).divisors, (ArithmeticFunction.moebius d : ℝ)) =
              ((∑ d ∈ (Nat.gcd n N_rough).divisors, ArithmeticFunction.moebius d : ℤ) : ℝ) := by
          push_cast; rfl
        rw [h_cast, h_mu_int]
        by_cases hcop : Nat.Coprime n N_rough
        · have h1 : Nat.gcd n N_rough = 1 := hcop
          rw [if_pos h1, if_pos hcop]
          norm_num
        · have hne1 : Nat.gcd n N_rough ≠ 1 := hcop
          rw [if_neg hne1, if_neg hcop]
          norm_num
      rw [h_mu_real]
      split_ifs <;> ring
    have h_split_1 :
        ∀ n ∈ Finset.Icc 1 T,
          (∑ d ∈ (Nat.gcd n N_rough).divisors, (ArithmeticFunction.moebius d : ℝ)) *
              (b n * gaussianTermPhi n X) =
            b n * gaussianTermPhi n X +
              ∑ d ∈ (roughSquarefreeDivisorsBand U T).filter (fun d => d ∣ n),
                (ArithmeticFunction.moebius d : ℝ) * (b n * gaussianTermPhi n X) := by
      intro n hn
      rw [Finset.mem_Icc] at hn
      have hn_pos : 0 < n := by omega
      have h_gcd_pos : 0 < Nat.gcd n N_rough := Nat.gcd_pos_of_pos_left N_rough hn_pos
      have h1_mem : 1 ∈ (Nat.gcd n N_rough).divisors :=
        Nat.mem_divisors.mpr ⟨one_dvd _, ne_of_gt h_gcd_pos⟩
      have h_div_eq :
          (Nat.gcd n N_rough).divisors.erase 1 =
            (roughSquarefreeDivisorsBand U T).filter (fun d => d ∣ n) := by
        ext d
        simp only [Finset.mem_erase, Nat.mem_divisors, roughSquarefreeDivisorsBand, Finset.mem_filter]
        constructor
        · rintro ⟨hd_ne1, hd_gcd, _⟩
          have hd_n : d ∣ n := dvd_trans hd_gcd (Nat.gcd_dvd_left _ _)
          have hd_mod : d ∣ N_rough := dvd_trans hd_gcd (Nat.gcd_dvd_right _ _)
          have hd_le_T : d ≤ T := le_trans (Nat.le_of_dvd hn_pos hd_n) hn.2
          exact ⟨⟨⟨hd_mod, ne_of_gt hN_rough_pos⟩, ⟨h_div_rough_ge_U d hd_mod hd_ne1, hd_le_T⟩⟩, hd_n⟩
        · rintro ⟨⟨⟨hd_mod, _⟩, ⟨hd_ge_U, _⟩⟩, hd_n⟩
          exact ⟨by omega, Nat.dvd_gcd hd_n hd_mod, ne_of_gt h_gcd_pos⟩
      rw [← Finset.add_sum_erase _ _ h1_mem, h_div_eq, ArithmeticFunction.moebius_apply_one]
      push_cast
      rw [add_mul, one_mul, Finset.sum_mul]
    have h_sum_split :
        finiteQSmoothBelow b U T X =
          finiteQGeneral b T X +
            ∑ d ∈ roughSquarefreeDivisorsBand U T,
              ((ArithmeticFunction.moebius d : ℝ) * b d / Real.sqrt (d : ℝ)) *
                finiteQGeneral b (T / d) (X / (d : ℝ)) := by
      rw [h_smooth_sieve]
      have h_congr := Finset.sum_congr rfl h_split_1
      rw [h_congr, Finset.sum_add_distrib]
      congr 1
      have h_swap :
          (∑ n ∈ Finset.Icc 1 T,
            ∑ d ∈ (roughSquarefreeDivisorsBand U T).filter (fun d => d ∣ n),
              (ArithmeticFunction.moebius d : ℝ) * (b n * gaussianTermPhi n X)) =
            ∑ d ∈ roughSquarefreeDivisorsBand U T,
              ∑ n ∈ (Finset.Icc 1 T).filter (fun n => d ∣ n),
                (ArithmeticFunction.moebius d : ℝ) * (b n * gaussianTermPhi n X) := by
        simp only [Finset.sum_filter]
        rw [Finset.sum_comm]
      rw [h_swap]
      apply Finset.sum_congr rfl
      intro d hd
      simp only [roughSquarefreeDivisorsBand, Finset.mem_filter] at hd
      have hd_pos : 0 < d := by omega
      have h_inner_bij :
          (∑ n ∈ (Finset.Icc 1 T).filter (fun n => d ∣ n),
            (ArithmeticFunction.moebius d : ℝ) * (b n * gaussianTermPhi n X)) =
            ∑ q ∈ Finset.Icc 1 (T / d),
              (ArithmeticFunction.moebius d : ℝ) * (b (d * q) * gaussianTermPhi (d * q) X) := by
        symm
        apply Finset.sum_bij (fun q _ => d * q)
        · intro q hq
          rw [Finset.mem_Icc] at hq
          simp only [Finset.mem_filter, Finset.mem_Icc]
          have hdq_le : d * q ≤ T := by
            rw [mul_comm]
            exact (Nat.le_div_iff_mul_le hd_pos).mp hq.2
          exact ⟨⟨Nat.mul_pos hd_pos (by omega), hdq_le⟩, ⟨q, rfl⟩⟩
        · intro q1 _ q2 _ h_eq
          exact Nat.eq_of_mul_eq_mul_left hd_pos h_eq
        · intro n hn
          simp only [Finset.mem_filter, Finset.mem_Icc] at hn
          rcases hn with ⟨⟨hn1, hnT⟩, ⟨q, rfl⟩⟩
          have hq_pos : 0 < q := by
            by_contra h0
            have hq0 : q = 0 := Nat.eq_zero_of_not_pos h0
            rw [hq0, mul_zero] at hn1
            omega
          have hq_div : q ≤ T / d := (Nat.le_div_iff_mul_le hd_pos).mpr (by rw [mul_comm]; exact hnT)
          exact ⟨q, Finset.mem_Icc.mpr ⟨hq_pos, hq_div⟩, rfl⟩
        · intros; rfl
      rw [h_inner_bij]
      dsimp [finiteQGeneral]
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro q hq
      rw [Finset.mem_Icc] at hq
      have hq_pos : 0 < q := by omega
      have h_b_mul : b (d * q) = b d * b q := hb_mult d q hd_pos hq_pos
      have h_phi_sc : gaussianTermPhi (d * q) X =
          (1 / Real.sqrt (d : ℝ)) * gaussianTermPhi q (X / (d : ℝ)) := by
        dsimp [gaussianTermPhi]
        exact (gaussian_term_scaling_aux (b := q) hX hd_pos).symm
      rw [h_b_mul, h_phi_sc]
      ring
    linarith
  have h_lam_mult_real :
      ∀ d q : ℕ, 0 < d → 0 < q →
        (liouvilleLambda (d * q) : ℝ) = (liouvilleLambda d : ℝ) * (liouvilleLambda q : ℝ) := by
    intro d q hd hq
    rw [liouvilleLambda_mul_aux (ne_of_gt hd) (ne_of_gt hq)]
    push_cast; rfl
  have h_mu_lam_one :
      ∀ d ∈ roughSquarefreeDivisorsBand U T,
        (ArithmeticFunction.moebius d : ℝ) * (liouvilleLambda d : ℝ) = 1 := by
    intro d hd
    simp only [roughSquarefreeDivisorsBand, Finset.mem_filter, Nat.mem_divisors] at hd
    have hd_ne : d ≠ 0 := by omega
    have h_mu_sq : (ArithmeticFunction.moebius d) ^ 2 = 1 :=
      moebius_sq_eq_one_of_dvd_primeProductModulus_aux hP_rough_prime hd.1.1
    have h_int : ArithmeticFunction.moebius d * liouvilleLambda d = 1 := by
      calc
        ArithmeticFunction.moebius d * liouvilleLambda d
          = ((ArithmeticFunction.moebius d) ^ 2 * liouvilleLambda d) * liouvilleLambda d := by
              rw [moebius_sq_mul_liouvilleLambda_eq_moebius_aux d]
        _ = (ArithmeticFunction.moebius d) ^ 2 * (liouvilleLambda d * liouvilleLambda d) := by ring
        _ = 1 := by rw [h_mu_sq, liouvilleLambda_sq_aux hd_ne, one_mul]
    exact_mod_cast h_int
  have h_fQ_eq_gen : ∀ L : ℕ, ∀ w : ℝ,
      finiteQLambda L w = finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) L w := by
    intro L w
    dsimp [finiteQLambda, finiteQGeneral, gaussianTermPhi]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro n _; ring
  have h_lam_id :
      finiteQLambda T X =
        finiteQSmoothBelow (fun n => (liouvilleLambda n : ℝ)) U T X -
          ∑ d ∈ roughSquarefreeDivisorsBand U T,
            (1 / Real.sqrt (d : ℝ)) * finiteQLambda (T / d) (X / (d : ℝ)) := by
    rw [h_fQ_eq_gen T X, h_gen_id (fun n => (liouvilleLambda n : ℝ)) h_lam_mult_real]
    congr 1
    apply Finset.sum_congr rfl
    intro d hd
    rw [h_mu_lam_one d hd, ← h_fQ_eq_gen (T / d) (X / (d : ℝ))]
  have h_super_sqrt : T < U ^ 2 → roughSquarefreeDivisorsBand U T = P_rough := by
    intro hTU2
    ext d
    simp only [roughSquarefreeDivisorsBand, P_rough, roughPrimeSetBand,
      Finset.mem_filter, Nat.mem_divisors, Finset.mem_Icc]
    constructor
    · rintro ⟨⟨hd_dvd, _⟩, ⟨hdU, hdT⟩⟩
      refine ⟨⟨hdU, hdT⟩, ?_⟩
      have hd_ne1 : d ≠ 1 := by omega
      obtain ⟨p, hp_prime, hp_dvd_d⟩ := Nat.exists_prime_and_dvd hd_ne1
      obtain ⟨q, hq_in_rough, hp_dvd_q⟩ :=
        prime_dvd_finset_prod_aux hp_prime P_rough (fun x => x) (dvd_trans hp_dvd_d hd_dvd)
      have hq_prime : q.Prime := hP_rough_prime q hq_in_rough
      have hpq : p = q := (Nat.dvd_prime hq_prime).mp hp_dvd_q |>.resolve_left hp_prime.ne_one
      have hp_ge_U : U ≤ p := by
        have hqU := ((Finset.mem_filter.mp hq_in_rough).1 |> Finset.mem_Icc.mp).1
        omega
      obtain ⟨k, rfl⟩ := hp_dvd_d
      have hk_pos : 0 < k := by
        by_contra h0
        have hk0 : k = 0 := Nat.eq_zero_of_not_pos h0
        rw [hk0, mul_zero] at hdU
        omega
      by_cases hk1 : k = 1
      · rw [hk1, mul_one]
        exact hp_prime
      · have hk_ne1 : k ≠ 1 := hk1
        have hp_in_P : p ∈ P_rough := hpq ▸ hq_in_rough
        have h_erase :
            primeProductModulus (Finset.filter Nat.Prime (Finset.Icc U T)) =
              p * ∏ x ∈ P_rough.erase p, x := by
          dsimp [P_rough, roughPrimeSetBand, primeProductModulus] at hp_in_P ⊢
          exact (Finset.mul_prod_erase _ (fun x => x) hp_in_P).symm
        rw [h_erase] at hd_dvd
        have hk_dvd_er : k ∣ ∏ x ∈ P_rough.erase p, x :=
          (Nat.mul_dvd_mul_iff_left hp_prime.pos).mp hd_dvd
        obtain ⟨r, hr_prime, hr_dvd_k⟩ := Nat.exists_prime_and_dvd hk_ne1
        obtain ⟨s, hs_in_er, hr_dvd_s⟩ :=
          prime_dvd_finset_prod_aux hr_prime (P_rough.erase p) (fun x => x) (dvd_trans hr_dvd_k hk_dvd_er)
        have hs_in_rough : s ∈ P_rough := Finset.mem_of_mem_erase hs_in_er
        have hs_prime : s.Prime := hP_rough_prime s hs_in_rough
        have hrs : r = s := (Nat.dvd_prime hs_prime).mp hr_dvd_s |>.resolve_left hr_prime.ne_one
        have hr_ge_U : U ≤ r := by
          have hsU := ((Finset.mem_filter.mp hs_in_rough).1 |> Finset.mem_Icc.mp).1
          omega
        have hk_ge_U : U ≤ k := le_trans hr_ge_U (Nat.le_of_dvd hk_pos hr_dvd_k)
        have hpk_ge_U2 : U ^ 2 ≤ p * k := by
          rw [sq]
          exact Nat.mul_le_mul hp_ge_U hk_ge_U
        omega
    · rintro ⟨⟨hdU, hdT⟩, hd_prime⟩
      have hd_mem : d ∈ P_rough := by
        simp only [P_rough, roughPrimeSetBand, Finset.mem_filter, Finset.mem_Icc]
        exact ⟨⟨hdU, hdT⟩, hd_prime⟩
      exact ⟨⟨Finset.dvd_prod_of_mem (fun x => x) hd_mem, ne_of_gt hN_rough_pos⟩, ⟨hdU, hdT⟩⟩
  refine ⟨h_set_eq, h_gen_id a ha_mult, ⟨h_mu_lam_one, h_lam_id⟩, ⟨h_super_sqrt, ?_⟩⟩
  have hmu3 : ArithmeticFunction.moebius 3 = -1 := ArithmeticFunction.moebius_apply_prime Nat.prime_three
  have hmu5 : ArithmeticFunction.moebius 5 = -1 := ArithmeticFunction.moebius_apply_prime (by decide : Nat.Prime 5)
  have hmu15 : ArithmeticFunction.moebius 15 = 1 := by
    have h15 : (15 : ℕ) = 3 * 5 := rfl
    rw [h15, ArithmeticFunction.isMultiplicative_moebius.2 (by decide : Nat.Coprime 3 5), hmu3, hmu5]
    norm_num
  have ha2_3 : twoAdicParityControl 3 = 1 := by
    have h0 : (3 : ℕ).factorization 2 = 0 :=
      Nat.factorization_eq_zero_of_not_dvd (by decide : ¬ 2 ∣ 3)
    simp [twoAdicParityControl, primeParityControl, h0]
  have ha2_15 : twoAdicParityControl 15 = 1 := by
    have h0 : (15 : ℕ).factorization 2 = 0 :=
      Nat.factorization_eq_zero_of_not_dvd (by decide : ¬ 2 ∣ 15)
    simp [twoAdicParityControl, primeParityControl, h0]
  have hlam3 : liouvilleLambda 3 = -1 := by
    have ho3 : natOmega 3 = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr Nat.prime_three
    simp [liouvilleLambda, ho3, liouvilleSignFromOmega]
  have hlam5 : liouvilleLambda 5 = -1 := by
    have ho5 : natOmega 5 = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr (by decide : Nat.Prime 5)
    simp [liouvilleLambda, ho5, liouvilleSignFromOmega]
  have hlam15 : liouvilleLambda 15 = 1 := by
    have h15 : (15 : ℕ) = 3 * 5 := rfl
    rw [h15, liouvilleLambda_mul_aux (by decide) (by decide), hlam3, hlam5]
    norm_num
  refine ⟨by rw [hmu3, ha2_3]; norm_num, by rw [hmu15, ha2_15]; norm_num,
    by rw [hmu3, hlam3]; norm_num, by rw [hmu15, hlam15]; norm_num⟩

/-- Helper: for every integer `n ∈ [1, T]`, `log n = ∑_{(p,k) ∈ primePowerPairsUpTo T, p^k ∣ n} log p`. -/
private theorem log_nat_eq_sum_primePowerPairsUpTo_dvd_aux
    {T n : ℕ} (hn1 : 1 ≤ n) (hnT : n ≤ T) :
    Real.log (n : ℝ) =
      ∑ pk ∈ (primePowerPairsUpTo T).filter (fun pk => pk.1 ^ pk.2 ∣ n),
        Real.log (pk.1 : ℝ) := by
  have hn_ne : n ≠ 0 := by omega
  have h_prod_nat : (∏ p ∈ n.primeFactors, p ^ (n.factorization p)) = n := by
    calc
      ∏ p ∈ n.primeFactors, p ^ (n.factorization p)
        = n.factorization.prod (fun p k => p ^ k) := by
            rw [Finsupp.prod, Nat.support_factorization]
      _ = n := Nat.factorization_prod_pow_eq_self hn_ne
  have h_prod_real : (∏ p ∈ n.primeFactors, ((p : ℝ) ^ (n.factorization p))) = (n : ℝ) := by
    exact_mod_cast h_prod_nat
  have h_log_n :
      Real.log (n : ℝ) =
        ∑ p ∈ n.primeFactors, (n.factorization p : ℝ) * Real.log (p : ℝ) := by
    rw [← h_prod_real, Real.log_prod]
    · apply Finset.sum_congr rfl
      intro p _
      exact Real.log_pow (p : ℝ) (n.factorization p)
    · intro p hp
      have hp_prime : p.Prime := Nat.prime_of_mem_primeFactors hp
      exact pow_ne_zero _ (Nat.cast_ne_zero.mpr hp_prime.ne_zero)
  have h_expand :
      (∑ p ∈ n.primeFactors, (n.factorization p : ℝ) * Real.log (p : ℝ)) =
        ∑ pk ∈ n.primeFactors.sigma (fun p => Finset.Icc 1 (n.factorization p)),
          Real.log (pk.1 : ℝ) := by
    symm
    rw [Finset.sum_sigma]
    apply Finset.sum_congr rfl
    intro p _
    simp [Nat.card_Icc]
  rw [h_log_n, h_expand]
  apply Finset.sum_bij (fun pk _ => (pk.1, pk.2))
  · rintro ⟨p, k⟩ hpk
    simp only [Finset.mem_sigma, Finset.mem_Icc] at hpk
    rcases hpk with ⟨hp_mem, ⟨hk1, hk_le_fact⟩⟩
    have hp_prime : p.Prime := Nat.prime_of_mem_primeFactors hp_mem
    have hpk_dvd : p ^ k ∣ n := (hp_prime.pow_dvd_iff_le_factorization hn_ne).mpr hk_le_fact
    have hpk_le_n : p ^ k ≤ n := Nat.le_of_dvd (by omega) hpk_dvd
    have hpk_le_T : p ^ k ≤ T := le_trans hpk_le_n hnT
    have hp_le_pk : p ≤ p ^ k := by
      simpa using Nat.pow_le_pow_right hp_prime.pos hk1
    have hk_lt_pk : k < p ^ k := Nat.lt_pow_self hp_prime.one_lt k
    simp only [Finset.mem_filter, primePowerPairsUpTo, Finset.mem_product, primesUpToFinset,
      Finset.mem_Icc]
    exact ⟨⟨⟨⟨⟨hp_prime.two_le, le_trans hp_le_pk hpk_le_T⟩, hp_prime⟩, ⟨hk1, by omega⟩⟩, hpk_le_T⟩, hpk_dvd⟩
  · rintro ⟨p1, k1⟩ _ ⟨p2, k2⟩ _ h_eq
    cases h_eq
    rfl
  · rintro ⟨p, k⟩ hpk
    simp only [Finset.mem_filter, primePowerPairsUpTo, Finset.mem_product, primesUpToFinset,
      Finset.mem_Icc] at hpk
    rcases hpk with ⟨⟨⟨⟨_, hp_prime⟩, ⟨hk1, _⟩⟩, _⟩, hpk_dvd⟩
    have hk_le_fact : k ≤ n.factorization p :=
      (hp_prime.pow_dvd_iff_le_factorization hn_ne).mp hpk_dvd
    have hp_dvd_pk : p ∣ p ^ k := dvd_pow_self p (by omega)
    have hp_mem : p ∈ n.primeFactors :=
      Nat.mem_primeFactors.mpr ⟨hp_prime, dvd_trans hp_dvd_pk hpk_dvd, hn_ne⟩
    exact ⟨⟨p, k⟩, Finset.mem_sigma.mpr ⟨hp_mem, Finset.mem_Icc.mpr ⟨hk1, hk_le_fact⟩⟩, rfl⟩
  · intros; rfl

/-- Helper: `a (d ^ k) = (a d) ^ k` for `0 < d` and `a 1 = 1` when `a` is completely multiplicative on `ℕ_{>0}`. -/
private theorem pow_apply_of_pos_mul_aux {a : ℕ → ℝ} (ha1 : a 1 = 1)
    (ha_mult : ∀ d q : ℕ, 0 < d → 0 < q → a (d * q) = a d * a q)
    {p : ℕ} (hp : 0 < p) : ∀ k : ℕ, a (p ^ k) = (a p) ^ k
  | 0 => by simp [ha1]
  | k + 1 => by
      rw [pow_succ', ha_mult p (p ^ k) hp (pow_pos hp k), pow_apply_of_pos_mul_aux ha1 ha_mult hp k, pow_succ']

/-- **Theorem 23 (`TASK-TC-057` §4 Route B, Exact Logarithmic Prime-Power Descent, Scale-Invariant Kernel-Shift Hierarchy `Q_T^{[m]}`, `M`-Step Telescope, and `T = 0, 1` Boundary Cases)**:
    For every completely multiplicative weight `a : ℕ → ℝ` (`a 1 = 1` and `∀ d q > 0, a (d * q) = a d * a q`),
    cutoff `T : ℕ`, shift order `m : ℕ`, telescope depth `M : ℕ`, and `X > 0`:
    1. Exact general logarithmic prime-power identity at shift order `m`:
       `∑ n ∈ Finset.Icc 1 T, a n * Real.log (n : ℝ) * (Real.log (X / (n : ℝ))) ^ m * gaussianTermPhi n X = primePowerLogDescentSum a m T X`;
    2. Liouville specialization (`m = 0`, `λ(p)^k = (-1)^k`) and `T = 0, 1` vanishing:
       `∑ n ∈ Finset.Icc 1 T, (liouvilleLambda n : ℝ) * Real.log (n : ℝ) * gaussianTermPhi n X = ∑ pk ∈ primePowerPairsUpTo T, liouvillePrimePowerTerm T pk X`,
       with `primePowerPairsUpTo 0 = ∅` and `primePowerPairsUpTo 1 = ∅`;
    3. Exact scale-invariant shift recurrence (`log n = log X - log(X / n)`):
       `Real.log X * finiteQShifted a m T X = primePowerLogDescentSum a m T X + finiteQShifted a (m + 1) T X`;
    4. Exact `M`-step telescope (`Real.log X ≠ 0`):
       `finiteQGeneral a T X = (∑ j ∈ Finset.range M, primePowerLogDescentSum a j T X / (Real.log X) ^ (j + 1)) + finiteQShifted a M T X / (Real.log X) ^ M`. -/
theorem logarithmic_prime_power_descent_and_kernel_shift_tc057
    {a : ℕ → ℝ} (ha1 : a 1 = 1)
    (ha_mult : ∀ d q : ℕ, 0 < d → 0 < q → a (d * q) = a d * a q)
    (m M T : ℕ) {X : ℝ} (hX : 0 < X) :
    (∀ r : ℕ,
      ∑ n ∈ Finset.Icc 1 T,
        a n * Real.log (n : ℝ) * (Real.log (X / (n : ℝ))) ^ r * gaussianTermPhi n X =
        primePowerLogDescentSum a r T X) ∧
    ((∑ n ∈ Finset.Icc 1 T,
        (liouvilleLambda n : ℝ) * Real.log (n : ℝ) * gaussianTermPhi n X =
        ∑ pk ∈ primePowerPairsUpTo T, liouvillePrimePowerTerm T pk X) ∧
      primePowerPairsUpTo 0 = ∅ ∧ primePowerPairsUpTo 1 = ∅) ∧
    (Real.log X * finiteQShifted a m T X =
      primePowerLogDescentSum a m T X + finiteQShifted a (m + 1) T X) ∧
    (Real.log X ≠ 0 →
      finiteQGeneral a T X =
        (∑ j ∈ Finset.range M, primePowerLogDescentSum a j T X / (Real.log X) ^ (j + 1)) +
          finiteQShifted a M T X / (Real.log X) ^ M) := by
  have hX_nn : 0 ≤ X := le_of_lt hX
  have h_gen :
      ∀ (b : ℕ → ℝ), b 1 = 1 → (∀ d q : ℕ, 0 < d → 0 < q → b (d * q) = b d * b q) →
        ∀ r : ℕ,
          ∑ n ∈ Finset.Icc 1 T,
            b n * Real.log (n : ℝ) * (Real.log (X / (n : ℝ))) ^ r * gaussianTermPhi n X =
            primePowerLogDescentSum b r T X := by
    intro b hb1 hb_mult r
    have h_step1 :
        ∑ n ∈ Finset.Icc 1 T,
          b n * Real.log (n : ℝ) * (Real.log (X / (n : ℝ))) ^ r * gaussianTermPhi n X =
          ∑ n ∈ Finset.Icc 1 T,
            ∑ pk ∈ (primePowerPairsUpTo T).filter (fun pk => pk.1 ^ pk.2 ∣ n),
              Real.log (pk.1 : ℝ) * (b n * (Real.log (X / (n : ℝ))) ^ r * gaussianTermPhi n X) := by
      apply Finset.sum_congr rfl
      intro n hn
      rw [Finset.mem_Icc] at hn
      have h_rearr :
          b n * Real.log (n : ℝ) * (Real.log (X / (n : ℝ))) ^ r * gaussianTermPhi n X =
            Real.log (n : ℝ) * (b n * (Real.log (X / (n : ℝ))) ^ r * gaussianTermPhi n X) := by ring
      rw [h_rearr, log_nat_eq_sum_primePowerPairsUpTo_dvd_aux hn.1 hn.2, Finset.sum_mul]
    rw [h_step1]
    have h_swap :
        (∑ n ∈ Finset.Icc 1 T,
          ∑ pk ∈ (primePowerPairsUpTo T).filter (fun pk => pk.1 ^ pk.2 ∣ n),
            Real.log (pk.1 : ℝ) * (b n * (Real.log (X / (n : ℝ))) ^ r * gaussianTermPhi n X)) =
          ∑ pk ∈ primePowerPairsUpTo T,
            ∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
              Real.log (pk.1 : ℝ) * (b n * (Real.log (X / (n : ℝ))) ^ r * gaussianTermPhi n X) := by
      simp only [Finset.sum_filter]
      rw [Finset.sum_comm]
    rw [h_swap]
    dsimp [primePowerLogDescentSum]
    apply Finset.sum_congr rfl
    rintro ⟨p, k⟩ hpk
    simp only [primePowerPairsUpTo, Finset.mem_filter, Finset.mem_product, primesUpToFinset,
      Finset.mem_Icc] at hpk
    rcases hpk with ⟨⟨⟨_, hp_prime⟩, ⟨_, _⟩⟩, _⟩
    let pk_val := p ^ k
    have hpk_pos : 0 < pk_val := pow_pos hp_prime.pos k
    have h_bij :
        (∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk_val ∣ n),
          Real.log (p : ℝ) * (b n * (Real.log (X / (n : ℝ))) ^ r * gaussianTermPhi n X)) =
          ∑ q ∈ Finset.Icc 1 (T / pk_val),
            Real.log (p : ℝ) *
              (b (pk_val * q) * (Real.log (X / ((pk_val * q : ℕ) : ℝ))) ^ r *
                gaussianTermPhi (pk_val * q) X) := by
      symm
      apply Finset.sum_bij (fun q _ => pk_val * q)
      · intro q hq
        rw [Finset.mem_Icc] at hq
        simp only [Finset.mem_filter, Finset.mem_Icc]
        have h_le : pk_val * q ≤ T := by
          rw [mul_comm]
          exact (Nat.le_div_iff_mul_le hpk_pos).mp hq.2
        exact ⟨⟨Nat.mul_pos hpk_pos (by omega), h_le⟩, ⟨q, rfl⟩⟩
      · intro q1 _ q2 _ h_eq
        exact Nat.eq_of_mul_eq_mul_left hpk_pos h_eq
      · intro n hn
        simp only [Finset.mem_filter, Finset.mem_Icc] at hn
        rcases hn with ⟨⟨hn1, hnT⟩, ⟨q, rfl⟩⟩
        have hq_pos : 0 < q := by
          by_contra h0
          have hq0 : q = 0 := Nat.eq_zero_of_not_pos h0
          rw [hq0, mul_zero] at hn1
          omega
        have hq_div : q ≤ T / pk_val :=
          (Nat.le_div_iff_mul_le hpk_pos).mpr (by rw [mul_comm]; exact hnT)
        exact ⟨q, Finset.mem_Icc.mpr ⟨hq_pos, hq_div⟩, rfl⟩
      · intros; rfl
    rw [h_bij]
    dsimp [finiteQShifted]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro q hq
    rw [Finset.mem_Icc] at hq
    have hq_pos : 0 < q := by omega
    have hb_pkq : b (pk_val * q) = (b p) ^ k * b q := by
      rw [hb_mult pk_val q hpk_pos hq_pos,
        pow_apply_of_pos_mul_aux hb1 hb_mult hp_prime.pos k]
    have h_div_arg : X / ((pk_val * q : ℕ) : ℝ) = (X / (pk_val : ℝ)) / (q : ℝ) := by
      push_cast
      rw [div_div]
    have h_phi_sc : gaussianTermPhi (pk_val * q) X =
        (1 / Real.sqrt (pk_val : ℝ)) * gaussianTermPhi q (X / (pk_val : ℝ)) := by
      dsimp [gaussianTermPhi]
      exact (gaussian_term_scaling_aux (b := q) hX_nn hpk_pos).symm
    rw [hb_pkq, h_div_arg, h_phi_sc]
    ring
  have h_rec_all :
      ∀ r : ℕ,
        Real.log X * finiteQShifted a r T X =
          primePowerLogDescentSum a r T X + finiteQShifted a (r + 1) T X := by
    intro r
    rw [← h_gen a ha1 ha_mult r]
    dsimp [finiteQShifted]
    rw [Finset.mul_sum, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro n hn
    rw [Finset.mem_Icc] at hn
    have hn_pos : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr (by omega)
    have h_log_div : Real.log (X / (n : ℝ)) = Real.log X - Real.log (n : ℝ) :=
      Real.log_div (ne_of_gt hX) (ne_of_gt hn_pos)
    rw [pow_succ, h_log_div]
    ring
  have h_lam_1 : (liouvilleLambda 1 : ℝ) = 1 := by
    simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
  have h_lam_mult :
      ∀ d q : ℕ, 0 < d → 0 < q →
        (liouvilleLambda (d * q) : ℝ) = (liouvilleLambda d : ℝ) * (liouvilleLambda q : ℝ) := by
    intro d q hd hq
    rw [liouvilleLambda_mul_aux (ne_of_gt hd) (ne_of_gt hq)]
    push_cast; rfl
  have h_lam_id :
      ∑ n ∈ Finset.Icc 1 T,
        (liouvilleLambda n : ℝ) * Real.log (n : ℝ) * gaussianTermPhi n X =
        ∑ pk ∈ primePowerPairsUpTo T, liouvillePrimePowerTerm T pk X := by
    have h0 := h_gen (fun n => (liouvilleLambda n : ℝ)) h_lam_1 h_lam_mult 0
    have h_lhs :
        (∑ n ∈ Finset.Icc 1 T,
          (liouvilleLambda n : ℝ) * Real.log (n : ℝ) * gaussianTermPhi n X) =
          ∑ n ∈ Finset.Icc 1 T,
            (liouvilleLambda n : ℝ) * Real.log (n : ℝ) * (Real.log (X / (n : ℝ))) ^ 0 *
              gaussianTermPhi n X := by
      apply Finset.sum_congr rfl
      intro n _; simp
    rw [h_lhs, h0]
    dsimp [primePowerLogDescentSum, liouvillePrimePowerTerm]
    apply Finset.sum_congr rfl
    rintro ⟨p, k⟩ hpk
    simp only [primePowerPairsUpTo, Finset.mem_filter, Finset.mem_product, primesUpToFinset,
      Finset.mem_Icc] at hpk
    have hp_prime : p.Prime := hpk.1.1.2
    have h_lam_p : (liouvilleLambda p : ℝ) = -1 := by
      have hop : natOmega p = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr hp_prime
      simp [liouvilleLambda, hp_prime.ne_zero, hop, liouvilleSignFromOmega]
    have h_fQ0 : ∀ L : ℕ, ∀ w : ℝ,
        finiteQShifted (fun n => (liouvilleLambda n : ℝ)) 0 L w = finiteQLambda L w := by
      intro L w
      dsimp [finiteQShifted, finiteQLambda, gaussianTermPhi]
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro n _; simp; ring
    rw [h_lam_p, h_fQ0]
  have h_pp0 : primePowerPairsUpTo 0 = ∅ := by decide
  have h_pp1 : primePowerPairsUpTo 1 = ∅ := by decide
  refine ⟨h_gen a ha1 ha_mult, ⟨h_lam_id, h_pp0, h_pp1⟩, h_rec_all m, ?_⟩
  intro hlog_ne
  have h_fQ0_a : finiteQGeneral a T X = finiteQShifted a 0 T X := by
    dsimp [finiteQGeneral, finiteQShifted]
    apply Finset.sum_congr rfl
    intro n _; simp
  rw [h_fQ0_a]
  induction' M with k ih
  · simp
  · have h_step := h_rec_all k
    have h_div_step :
        finiteQShifted a k T X / (Real.log X) ^ k =
          primePowerLogDescentSum a k T X / (Real.log X) ^ (k + 1) +
            finiteQShifted a (k + 1) T X / (Real.log X) ^ (k + 1) := by
      calc
        finiteQShifted a k T X / (Real.log X) ^ k
          = (Real.log X * finiteQShifted a k T X) / (Real.log X * (Real.log X) ^ k) :=
              (mul_div_mul_left (finiteQShifted a k T X) ((Real.log X) ^ k) hlog_ne).symm
        _ = (primePowerLogDescentSum a k T X + finiteQShifted a (k + 1) T X) /
              (Real.log X) ^ (k + 1) := by
              rw [h_step, pow_succ']
        _ = primePowerLogDescentSum a k T X / (Real.log X) ^ (k + 1) +
              finiteQShifted a (k + 1) T X / (Real.log X) ^ (k + 1) := add_div _ _ _
    rw [ih, h_div_step, Finset.sum_range_succ]
    ring

/-- **Theorem 24 (`TASK-TC-057` §4 Route D, Exact Quadratic Prime-Power Diagonal/Off-Diagonal Square Expansion and Shifted-Kernel Domination)**:
    For every cutoff `T : ℕ` and `X > 0`:
    1. Exact pointwise square expansion of the prime-power descent sum into the positive cross-scale diagonal
       `∑_{(p,k) ∈ primePowerPairsUpTo T} ((log p)^2 / p^k) Q_{λ,⌊T/p^k⌋}(X / p^k)^2` and the ordered
       off-diagonal `pk_1 ≠ pk_2` correlation sum:
       `(Real.log X * finiteQLambda T X - finiteQShifted (fun n => (liouvilleLambda n : ℝ)) 1 T X) ^ 2 = (∑ pk ∈ primePowerPairsUpTo T, ((Real.log (pk.1 : ℝ)) ^ 2 / ((pk.1 ^ pk.2 : ℕ) : ℝ)) * (finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ))) ^ 2) + ∑ pk1 ∈ primePowerPairsUpTo T, ∑ pk2 ∈ (primePowerPairsUpTo T).erase pk1, liouvillePrimePowerTerm T pk1 X * liouvillePrimePowerTerm T pk2 X`;
    2. Exact Young upper bound when `Real.log X ≠ 0`:
       `(finiteQLambda T X) ^ 2 ≤ (2 / (Real.log X) ^ 2) * (∑ pk ∈ primePowerPairsUpTo T, liouvillePrimePowerTerm T pk X) ^ 2 + (2 / (Real.log X) ^ 2) * (finiteQShifted (fun n => (liouvilleLambda n : ℝ)) 1 T X) ^ 2`. -/
theorem quadratic_prime_power_diagonal_off_diagonal_decomposition_tc057
    (T : ℕ) {X : ℝ} (hX : 0 < X) :
    ((Real.log X * finiteQLambda T X -
        finiteQShifted (fun n => (liouvilleLambda n : ℝ)) 1 T X) ^ 2 =
      (∑ pk ∈ primePowerPairsUpTo T,
        ((Real.log (pk.1 : ℝ)) ^ 2 / ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
          (finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ))) ^ 2) +
      (∑ pk1 ∈ primePowerPairsUpTo T,
        ∑ pk2 ∈ (primePowerPairsUpTo T).erase pk1,
          liouvillePrimePowerTerm T pk1 X * liouvillePrimePowerTerm T pk2 X)) ∧
    (Real.log X ≠ 0 →
      (finiteQLambda T X) ^ 2 ≤
        (2 / (Real.log X) ^ 2) * (∑ pk ∈ primePowerPairsUpTo T, liouvillePrimePowerTerm T pk X) ^ 2 +
          (2 / (Real.log X) ^ 2) * (finiteQShifted (fun n => (liouvilleLambda n : ℝ)) 1 T X) ^ 2) := by
  have h_lam_1 : (liouvilleLambda 1 : ℝ) = 1 := by
    simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
  have h_lam_mult :
      ∀ d q : ℕ, 0 < d → 0 < q →
        (liouvilleLambda (d * q) : ℝ) = (liouvilleLambda d : ℝ) * (liouvilleLambda q : ℝ) := by
    intro d q hd hq
    rw [liouvilleLambda_mul_aux (ne_of_gt hd) (ne_of_gt hq)]
    push_cast; rfl
  obtain ⟨h_gen_r, ⟨h_lam_pp, _, _⟩, h_rec0, _⟩ :=
    logarithmic_prime_power_descent_and_kernel_shift_tc057
      (a := fun n => (liouvilleLambda n : ℝ)) h_lam_1 h_lam_mult 0 0 T hX
  have h_fQ0 : finiteQShifted (fun n => (liouvilleLambda n : ℝ)) 0 T X = finiteQLambda T X := by
    dsimp [finiteQShifted, finiteQLambda, gaussianTermPhi]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro n _; simp; ring
  have h_pp_eq :
      primePowerLogDescentSum (fun n => (liouvilleLambda n : ℝ)) 0 T X =
        ∑ pk ∈ primePowerPairsUpTo T, liouvillePrimePowerTerm T pk X := by
    rw [← h_gen_r 0, ← h_lam_pp]
    apply Finset.sum_congr rfl
    intro n _; simp
  have h_diff_eq :
      Real.log X * finiteQLambda T X -
          finiteQShifted (fun n => (liouvilleLambda n : ℝ)) 1 T X =
        ∑ pk ∈ primePowerPairsUpTo T, liouvillePrimePowerTerm T pk X := by
    rw [← h_fQ0, ← h_pp_eq]
    linarith
  refine ⟨?_, ?_⟩
  · rw [h_diff_eq, sq, Finset.sum_mul_sum]
    have h_split :
        (∑ pk1 ∈ primePowerPairsUpTo T, ∑ pk2 ∈ primePowerPairsUpTo T,
            liouvillePrimePowerTerm T pk1 X * liouvillePrimePowerTerm T pk2 X) =
          (∑ pk ∈ primePowerPairsUpTo T,
              liouvillePrimePowerTerm T pk X * liouvillePrimePowerTerm T pk X) +
            ∑ pk1 ∈ primePowerPairsUpTo T, ∑ pk2 ∈ (primePowerPairsUpTo T).erase pk1,
              liouvillePrimePowerTerm T pk1 X * liouvillePrimePowerTerm T pk2 X := by
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro pk1 hpk1
      exact (Finset.add_sum_erase (primePowerPairsUpTo T)
        (fun pk2 => liouvillePrimePowerTerm T pk1 X * liouvillePrimePowerTerm T pk2 X) hpk1).symm
    rw [h_split]
    congr 1
    apply Finset.sum_congr rfl
    rintro ⟨p, k⟩ _
    have hpk_nn : (0 : ℝ) ≤ ((p ^ k : ℕ) : ℝ) := Nat.cast_nonneg _
    have h_sqrt_sq : (Real.sqrt ((p ^ k : ℕ) : ℝ)) ^ 2 = ((p ^ k : ℕ) : ℝ) :=
      Real.sq_sqrt hpk_nn
    have h_sign_sq : ((-1 : ℝ) ^ k) * ((-1 : ℝ) ^ k) = 1 := neg_one_pow_mul_self_real_aux k
    dsimp [liouvillePrimePowerTerm]
    calc
      ((-1 : ℝ) ^ k * Real.log (p : ℝ) * (1 / Real.sqrt ((p ^ k : ℕ) : ℝ)) *
          finiteQLambda (T / p ^ k) (X / ((p ^ k : ℕ) : ℝ))) *
        ((-1 : ℝ) ^ k * Real.log (p : ℝ) * (1 / Real.sqrt ((p ^ k : ℕ) : ℝ)) *
          finiteQLambda (T / p ^ k) (X / ((p ^ k : ℕ) : ℝ)))
        = (((-1 : ℝ) ^ k) * ((-1 : ℝ) ^ k)) *
            ((Real.log (p : ℝ)) ^ 2 / (Real.sqrt ((p ^ k : ℕ) : ℝ)) ^ 2) *
            (finiteQLambda (T / p ^ k) (X / ((p ^ k : ℕ) : ℝ))) ^ 2 := by ring
      _ = ((Real.log (p : ℝ)) ^ 2 / ((p ^ k : ℕ) : ℝ)) *
            (finiteQLambda (T / p ^ k) (X / ((p ^ k : ℕ) : ℝ))) ^ 2 := by
            rw [h_sign_sq, one_mul, h_sqrt_sq]
  · intro hlog_ne
    let S_pp := ∑ pk ∈ primePowerPairsUpTo T, liouvillePrimePowerTerm T pk X
    let R_sh := finiteQShifted (fun n => (liouvilleLambda n : ℝ)) 1 T X
    have h_sum_eq : Real.log X * finiteQLambda T X = S_pp + R_sh := by
      dsimp [S_pp, R_sh]
      linarith [h_diff_eq]
    have h_young : (S_pp + R_sh) ^ 2 ≤ 2 * S_pp ^ 2 + 2 * R_sh ^ 2 := by
      have h_nonneg : 0 ≤ (S_pp - R_sh) ^ 2 := sq_nonneg (S_pp - R_sh)
      linarith
    have h_sq_prod : (Real.log X) ^ 2 * (finiteQLambda T X) ^ 2 ≤ 2 * S_pp ^ 2 + 2 * R_sh ^ 2 := by
      have h_lhs : (Real.log X) ^ 2 * (finiteQLambda T X) ^ 2 = (S_pp + R_sh) ^ 2 := by
        rw [← mul_pow, h_sum_eq]
      linarith
    have h_log_sq_pos : 0 < (Real.log X) ^ 2 := sq_pos_of_ne_zero hlog_ne
    have h_inv_pos : 0 ≤ 1 / (Real.log X) ^ 2 := le_of_lt (one_div_pos.mpr h_log_sq_pos)
    have h_div := mul_le_mul_of_nonneg_left h_sq_prod h_inv_pos
    have h_cancel_lhs : (1 / (Real.log X) ^ 2) * ((Real.log X) ^ 2 * (finiteQLambda T X) ^ 2) =
        (finiteQLambda T X) ^ 2 := by
      field_simp [hlog_ne]
    have h_rhs_rearr : (1 / (Real.log X) ^ 2) * (2 * S_pp ^ 2 + 2 * R_sh ^ 2) =
        (2 / (Real.log X) ^ 2) * S_pp ^ 2 + (2 / (Real.log X) ^ 2) * R_sh ^ 2 := by ring
    linarith

/-- Helper: telescoping reciprocal-cube sum `∑_{3 ≤ n ≤ L} 1 / n^3 ≤ 1 / 12` for all `L : ℕ`. -/
private theorem sum_inv_cube_Icc_three_le_one_twelfth_aux (L : ℕ) :
    (∑ n ∈ Finset.Icc 3 L, ((n : ℝ) ^ 3)⁻¹) ≤ (1 / 12 : ℝ) := by
  by_cases hL : 3 ≤ L
  · obtain ⟨K, rfl⟩ : ∃ K : ℕ, L = K + 3 := ⟨L - 3, by omega⟩
    have h_term_le :
        ∀ n ∈ Finset.Icc 3 (K + 3),
          ((n : ℝ) ^ 3)⁻¹ ≤
            (1 / 2 : ℝ) * (((((n - 1 : ℕ) : ℝ) * (n : ℝ))⁻¹) - (((n : ℝ) * ((n + 1 : ℕ) : ℝ))⁻¹)) := by
      intro n hn
      rw [Finset.mem_Icc] at hn
      have hn3 : 3 ≤ n := hn.1
      have hn_sub1 : ((n - 1 : ℕ) : ℝ) = (n : ℝ) - 1 := by
        rw [Nat.cast_sub (by omega : 1 ≤ n), Nat.cast_one]
      have hn_add1 : ((n + 1 : ℕ) : ℝ) = (n : ℝ) + 1 := by push_cast; ring
      rw [hn_sub1, hn_add1]
      have hn_pos : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr (by omega)
      have hn_m1_pos : (0 : ℝ) < (n : ℝ) - 1 := by
        have h3 : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn3
        linarith
      have hn_p1_pos : (0 : ℝ) < (n : ℝ) + 1 := by linarith
      have h_diff :
          (1 / 2 : ℝ) * ((((n : ℝ) - 1) * (n : ℝ))⁻¹ - ((n : ℝ) * ((n : ℝ) + 1))⁻¹) - ((n : ℝ) ^ 3)⁻¹ =
            1 / ((n : ℝ) ^ 3 * ((n : ℝ) - 1) * ((n : ℝ) + 1)) := by
        field_simp [ne_of_gt hn_pos, ne_of_gt hn_m1_pos, ne_of_gt hn_p1_pos]
        ring
      have h_pos_rhs : 0 ≤ 1 / ((n : ℝ) ^ 3 * ((n : ℝ) - 1) * ((n : ℝ) + 1)) := by positivity
      linarith
    have h_sum_le := Finset.sum_le_sum h_term_le
    have h_tele :
        ∀ m : ℕ,
          (∑ n ∈ Finset.Icc 3 (m + 3),
              (1 / 2 : ℝ) * (((((n - 1 : ℕ) : ℝ) * (n : ℝ))⁻¹) - (((n : ℝ) * ((n + 1 : ℕ) : ℝ))⁻¹))) =
            (1 / 12 : ℝ) - (1 / 2 : ℝ) * ((((m + 3 : ℕ) : ℝ) * ((m + 4 : ℕ) : ℝ))⁻¹) := by
      intro m
      induction' m with m ih
      · have h_single : Finset.Icc 3 3 = {3} := by decide
        rw [h_single, Finset.sum_singleton]
        norm_num
      · have h_ins : Finset.Icc 3 (m + 1 + 3) = insert (m + 4) (Finset.Icc 3 (m + 3)) := by
          ext x
          simp only [Finset.mem_Icc, Finset.mem_insert]
          omega
        have h_not_mem : (m + 4) ∉ Finset.Icc 3 (m + 3) := by
          simp only [Finset.mem_Icc]
          omega
        rw [h_ins, Finset.sum_insert h_not_mem, ih]
        have hm1 : m + 4 - 1 = m + 3 := by omega
        have hm2 : m + 4 + 1 = m + 1 + 4 := by omega
        have hm3 : m + 1 + 3 = m + 4 := by omega
        rw [hm1, hm2, hm3]
        ring
    rw [h_tele K] at h_sum_le
    have h_tail_nn : 0 ≤ (1 / 2 : ℝ) * ((((K + 3 : ℕ) : ℝ) * ((K + 4 : ℕ) : ℝ))⁻¹) := by positivity
    linarith
  · have h_empty : Finset.Icc 3 L = ∅ := by
      ext x
      simp only [Finset.mem_Icc, Finset.not_mem_empty, iff_false]
      omega
    rw [h_empty, Finset.sum_empty]
    norm_num

/-- **Theorem 25 (`TASK-TC-057` §5, Inherited-vs-Canonical Cutoff Comparison, `(Y = 9/4, d = 2)` Counterexample, and Unconditional Small-Scale Positivity on `(0, 1]`)**:
    1. Exact floor/ceiling and cofactor-cutoff inequalities:
       - `0 ≤ u → u + 1 ≤ (T : ℝ) / (d : ℝ) → 0 < d → Nat.ceil u ≤ T / d`;
       - For `1 ≤ W` and `16 ≤ d`, `canonicalCutoffT W ≤ inheritedCutoffL (W * (d : ℝ)) d`
         (`T(Y/d) ≤ ⌊T(Y)/d⌋`);
       - For ALL `1 ≤ W` and `2 ≤ d`,
         `(1 / 2 : ℝ) * W ^ (5 / 4 : ℝ) * (d : ℝ) ^ (1 / 4 : ℝ) ≤ (inheritedCutoffL (W * (d : ℝ)) d : ℝ)`;
    2. Explicit counterexample at `(Y = 9/4, d = 2)` (`W = 9/8 > 1`) refuting `T(Y/d) ≤ ⌊T(Y)/d⌋` for `d < 16`:
       `canonicalCutoffT (9 / 4 : ℝ) = 3`, `inheritedCutoffL (9 / 4 : ℝ) 2 = 1`,
       `canonicalCutoffT ((9 / 4 : ℝ) / 2) = 2`, `inheritedCutoffL (9 / 4 : ℝ) 2 < canonicalCutoffT ((9 / 4 : ℝ) / 2)`,
       and `0 < finiteQLambda 1 (9 / 8 : ℝ) - finiteQLambda 2 (9 / 8 : ℝ)`;
    3. Unconditional uniform small-scale positivity (`W = Y / p^k ≤ 1`): for EVERY `L ≥ 1` and EVERY `w ∈ (0, 1]`,
       `(1 / 24 : ℝ) * w ^ (5 / 2 : ℝ) ≤ finiteQLambda L w` and `0 < finiteQLambda L w`. -/
theorem inherited_vs_canonical_cutoff_comparison_and_counterexample_tc057 :
    ((∀ (u : ℝ) (T d : ℕ), 0 ≤ u → 0 < d → u + 1 ≤ (T : ℝ) / (d : ℝ) → Nat.ceil u ≤ T / d) ∧
      (∀ (W : ℝ) (d : ℕ), 1 ≤ W → 16 ≤ d →
        canonicalCutoffT W ≤ inheritedCutoffL (W * (d : ℝ)) d) ∧
      (∀ (W : ℝ) (d : ℕ), 1 ≤ W → 2 ≤ d →
        (1 / 2 : ℝ) * W ^ (5 / 4 : ℝ) * (d : ℝ) ^ (1 / 4 : ℝ) ≤
          (inheritedCutoffL (W * (d : ℝ)) d : ℝ))) ∧
    (canonicalCutoffT (9 / 4 : ℝ) = 3 ∧
      inheritedCutoffL (9 / 4 : ℝ) 2 = 1 ∧
      canonicalCutoffT ((9 / 4 : ℝ) / 2) = 2 ∧
      inheritedCutoffL (9 / 4 : ℝ) 2 < canonicalCutoffT ((9 / 4 : ℝ) / 2) ∧
      0 < finiteQLambda 1 (9 / 8 : ℝ) - finiteQLambda 2 (9 / 8 : ℝ)) ∧
    (∀ (L : ℕ) (w : ℝ), 1 ≤ L → 0 < w → w ≤ 1 →
      (1 / 24 : ℝ) * w ^ (5 / 2 : ℝ) ≤ finiteQLambda L w ∧ 0 < finiteQLambda L w) := by
  have h_ceil_le_div :
      ∀ (u : ℝ) (T d : ℕ), 0 ≤ u → 0 < d → u + 1 ≤ (T : ℝ) / (d : ℝ) → Nat.ceil u ≤ T / d := by
    intro u T d hu _ hu1
    by_cases hu0 : u = 0
    · subst hu0
      simp
    · rw [← Nat.floor_div_eq_div (α := ℝ) T d]
      apply Nat.le_floor
      have h_lt : (Nat.ceil u : ℝ) < u + 1 := Nat.ceil_lt_add_one hu
      exact le_of_lt (lt_of_lt_of_le h_lt hu1)
  have h_wd_ratio :
      ∀ (W : ℝ) (d : ℕ), 1 ≤ W → 0 < d →
        W ^ (5 / 4 : ℝ) * (d : ℝ) ^ (1 / 4 : ℝ) ≤
          (canonicalCutoffT (W * (d : ℝ)) : ℝ) / (d : ℝ) := by
    intro W d hW1 hd_pos
    have hd_real_pos : (0 : ℝ) < (d : ℝ) := Nat.cast_pos.mpr hd_pos
    have hW_nn : 0 ≤ W := by linarith
    have hd_nn : (0 : ℝ) ≤ (d : ℝ) := le_of_lt hd_real_pos
    have h_ceil_ge : (W * (d : ℝ)) ^ (5 / 4 : ℝ) ≤ (canonicalCutoffT (W * (d : ℝ)) : ℝ) :=
      Nat.le_ceil _
    have h_mul_rpow : (W * (d : ℝ)) ^ (5 / 4 : ℝ) = W ^ (5 / 4 : ℝ) * (d : ℝ) ^ (5 / 4 : ℝ) :=
      Real.mul_rpow hW_nn hd_nn
    have hd_split : (d : ℝ) ^ (5 / 4 : ℝ) / (d : ℝ) = (d : ℝ) ^ (1 / 4 : ℝ) := by
      have hd1 : (d : ℝ) ^ (5 / 4 : ℝ) = (d : ℝ) ^ (1 / 4 : ℝ) * (d : ℝ) ^ (1 : ℝ) := by
        rw [← Real.rpow_add hd_real_pos]
        norm_num
      rw [Real.rpow_one] at hd1
      rw [hd1, mul_div_cancel_right₀ _ (ne_of_gt hd_real_pos)]
    calc
      W ^ (5 / 4 : ℝ) * (d : ℝ) ^ (1 / 4 : ℝ)
        = (W * (d : ℝ)) ^ (5 / 4 : ℝ) / (d : ℝ) := by
            rw [h_mul_rpow, mul_div_assoc, hd_split]
      _ ≤ (canonicalCutoffT (W * (d : ℝ)) : ℝ) / (d : ℝ) :=
            div_le_div_of_nonneg_right h_ceil_ge hd_nn
  have h_d16 :
      ∀ (W : ℝ) (d : ℕ), 1 ≤ W → 16 ≤ d →
        canonicalCutoffT W ≤ inheritedCutoffL (W * (d : ℝ)) d := by
    intro W d hW1 hd16
    have hd_pos : 0 < d := by omega
    have h16_le_d : (16 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd16
    have h16_fourth : (16 : ℝ) ^ (1 / 4 : ℝ) = 2 := by
      have h16_eq : (16 : ℝ) = (2 : ℝ) ^ (4 : ℝ) := by norm_num
      rw [h16_eq, ← Real.rpow_mul (by norm_num : (0 : ℝ) ≤ 2)]
      norm_num
    have hd_fourth_ge2 : (2 : ℝ) ≤ (d : ℝ) ^ (1 / 4 : ℝ) := by
      rw [← h16_fourth]
      exact Real.rpow_le_rpow (by norm_num) h16_le_d (by norm_num)
    have hW54_ge1 : (1 : ℝ) ≤ W ^ (5 / 4 : ℝ) := Real.one_le_rpow hW1 (by norm_num)
    have hW54_nn : 0 ≤ W ^ (5 / 4 : ℝ) := by linarith
    have h_u1 : W ^ (5 / 4 : ℝ) + 1 ≤ W ^ (5 / 4 : ℝ) * (d : ℝ) ^ (1 / 4 : ℝ) := by
      have h2W : 2 * W ^ (5 / 4 : ℝ) ≤ W ^ (5 / 4 : ℝ) * (d : ℝ) ^ (1 / 4 : ℝ) := by
        nlinarith [mul_le_mul_of_nonneg_left hd_fourth_ge2 hW54_nn]
      linarith
    exact h_ceil_le_div (W ^ (5 / 4 : ℝ)) (canonicalCutoffT (W * (d : ℝ))) d
      hW54_nn hd_pos (le_trans h_u1 (h_wd_ratio W d hW1 hd_pos))
  have h_half_lb :
      ∀ (W : ℝ) (d : ℕ), 1 ≤ W → 2 ≤ d →
        (1 / 2 : ℝ) * W ^ (5 / 4 : ℝ) * (d : ℝ) ^ (1 / 4 : ℝ) ≤
          (inheritedCutoffL (W * (d : ℝ)) d : ℝ) := by
    intro W d hW1 hd2
    have hd_pos : 0 < d := by omega
    have h2_le_d : (2 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd2
    have hd_fourth_ge1 : (1 : ℝ) ≤ (d : ℝ) ^ (1 / 4 : ℝ) :=
      Real.one_le_rpow (by linarith) (by norm_num)
    have hW54_ge1 : (1 : ℝ) ≤ W ^ (5 / 4 : ℝ) := Real.one_le_rpow hW1 (by norm_num)
    let x := (canonicalCutoffT (W * (d : ℝ)) : ℝ) / (d : ℝ)
    have hx_ge_prod : W ^ (5 / 4 : ℝ) * (d : ℝ) ^ (1 / 4 : ℝ) ≤ x :=
      h_wd_ratio W d hW1 hd_pos
    have h_prod_ge1 : 1 ≤ W ^ (5 / 4 : ℝ) * (d : ℝ) ^ (1 / 4 : ℝ) := by nlinarith
    have hx_ge1 : (1 : ℝ) ≤ x := le_trans h_prod_ge1 hx_ge_prod
    have h_floor_eq : (inheritedCutoffL (W * (d : ℝ)) d : ℝ) = (Nat.floor x : ℝ) := by
      dsimp [inheritedCutoffL, x]
      rw [Nat.floor_div_eq_div (α := ℝ)]
    rw [h_floor_eq]
    have hfl_ge1_nat : 1 ≤ Nat.floor x := Nat.le_floor (by simpa using hx_ge1)
    have hfl_ge1 : (1 : ℝ) ≤ (Nat.floor x : ℝ) := by exact_mod_cast hfl_ge1_nat
    have hx_lt_succ : x < (Nat.floor x : ℝ) + 1 := Nat.lt_floor_add_one x
    linarith
  have h_ce_94 : canonicalCutoffT (9 / 4 : ℝ) = 3 := by
    dsimp [canonicalCutoffT]
    have h_pow4 : ((9 / 4 : ℝ) ^ (5 / 4 : ℝ)) ^ (4 : ℕ) = (9 / 4 : ℝ) ^ (5 : ℕ) := by
      rw [← Real.rpow_natCast _ 4, ← Real.rpow_mul (by norm_num : (0 : ℝ) ≤ 9 / 4)]
      norm_num
    have h_gt2 : (2 : ℝ) < (9 / 4 : ℝ) ^ (5 / 4 : ℝ) := by
      by_contra h_le2
      push_neg at h_le2
      have h_nn : 0 ≤ (9 / 4 : ℝ) ^ (5 / 4 : ℝ) := Real.rpow_nonneg (by norm_num) _
      have h2_le : ((9 / 4 : ℝ) ^ (5 / 4 : ℝ)) ^ (2 : ℕ) ≤ 4 := by nlinarith
      have h4_le : ((9 / 4 : ℝ) ^ (5 / 4 : ℝ)) ^ (4 : ℕ) ≤ 16 := by nlinarith
      rw [h_pow4] at h4_le
      norm_num at h4_le
    have h_le3 : (9 / 4 : ℝ) ^ (5 / 4 : ℝ) ≤ 3 := by
      by_contra h_gt3
      push_neg at h_gt3
      have h2_gt : (9 : ℝ) < ((9 / 4 : ℝ) ^ (5 / 4 : ℝ)) ^ (2 : ℕ) := by nlinarith
      have h4_gt : (81 : ℝ) < ((9 / 4 : ℝ) ^ (5 / 4 : ℝ)) ^ (4 : ℕ) := by nlinarith
      rw [h_pow4] at h4_gt
      norm_num at h4_gt
    have h_ceil_le3 : Nat.ceil ((9 / 4 : ℝ) ^ (5 / 4 : ℝ)) ≤ 3 :=
      Nat.ceil_le.mpr (by exact_mod_cast h_le3)
    have h_ceil_gt2 : 2 < Nat.ceil ((9 / 4 : ℝ) ^ (5 / 4 : ℝ)) :=
      Nat.lt_ceil.mpr (by exact_mod_cast h_gt2)
    omega
  have h_inh_94_2 : inheritedCutoffL (9 / 4 : ℝ) 2 = 1 := by
    dsimp [inheritedCutoffL]
    rw [h_ce_94]
  have h_ce_98 : canonicalCutoffT ((9 / 4 : ℝ) / 2) = 2 := by
    have h98 : (9 / 4 : ℝ) / 2 = (9 / 8 : ℝ) := by norm_num
    rw [h98]
    dsimp [canonicalCutoffT]
    have h_pow4 : ((9 / 8 : ℝ) ^ (5 / 4 : ℝ)) ^ (4 : ℕ) = (9 / 8 : ℝ) ^ (5 : ℕ) := by
      rw [← Real.rpow_natCast _ 4, ← Real.rpow_mul (by norm_num : (0 : ℝ) ≤ 9 / 8)]
      norm_num
    have h_gt1 : (1 : ℝ) < (9 / 8 : ℝ) ^ (5 / 4 : ℝ) :=
      Real.one_lt_rpow (by norm_num) (by norm_num)
    have h_le2 : (9 / 8 : ℝ) ^ (5 / 4 : ℝ) ≤ 2 := by
      by_contra h_gt2
      push_neg at h_gt2
      have h2_gt : (4 : ℝ) < ((9 / 8 : ℝ) ^ (5 / 4 : ℝ)) ^ (2 : ℕ) := by nlinarith
      have h4_gt : (16 : ℝ) < ((9 / 8 : ℝ) ^ (5 / 4 : ℝ)) ^ (4 : ℕ) := by nlinarith
      rw [h_pow4] at h4_gt
      norm_num at h4_gt
    have h_ceil_le2 : Nat.ceil ((9 / 8 : ℝ) ^ (5 / 4 : ℝ)) ≤ 2 :=
      Nat.ceil_le.mpr (by exact_mod_cast h_le2)
    have h_ceil_gt1 : 1 < Nat.ceil ((9 / 8 : ℝ) ^ (5 / 4 : ℝ)) :=
      Nat.lt_ceil.mpr (by exact_mod_cast h_gt1)
    omega
  have h_diff_pos_98 : 0 < finiteQLambda 1 (9 / 8 : ℝ) - finiteQLambda 2 (9 / 8 : ℝ) := by
    have hIcc1 : Finset.Icc 1 1 = {1} := by decide
    have hIcc2 : Finset.Icc 1 2 = {1, 2} := by decide
    have hl1 : liouvilleLambda 1 = 1 := by simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
    have hl2 : liouvilleLambda 2 = -1 := by
      have ho2 : natOmega 2 = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr Nat.prime_two
      simp [liouvilleLambda, ho2, liouvilleSignFromOmega]
    dsimp [finiteQLambda]
    rw [hIcc1, hIcc2, Finset.sum_singleton, Finset.sum_pair (by decide), hl1, hl2]
    push_cast
    have h_eq :
        (9 / 8 : ℝ) ^ (5 / 2 : ℝ) * (1 * ((1 : ℝ) ^ 3)⁻¹ * Real.exp (-((9 / 8 : ℝ) ^ 2) / (1 : ℝ) ^ 2)) -
          (9 / 8 : ℝ) ^ (5 / 2 : ℝ) *
            (1 * ((1 : ℝ) ^ 3)⁻¹ * Real.exp (-((9 / 8 : ℝ) ^ 2) / (1 : ℝ) ^ 2) +
              (-1) * ((2 : ℝ) ^ 3)⁻¹ * Real.exp (-((9 / 8 : ℝ) ^ 2) / (2 : ℝ) ^ 2)) =
          (9 / 8 : ℝ) ^ (5 / 2 : ℝ) * ((1 / 8 : ℝ) * Real.exp (-((9 / 8 : ℝ) ^ 2) / 4)) := by ring
    rw [h_eq]
    positivity
  refine ⟨⟨h_ceil_le_div, h_d16, h_half_lb⟩,
    ⟨h_ce_94, h_inh_94_2, h_ce_98, by omega, h_diff_pos_98⟩, ?_⟩
  intro L w hL1 hw_pos hw_le1
  have hw_pow_pos : 0 < w ^ (5 / 2 : ℝ) := Real.rpow_pos_of_pos hw_pos _
  have hw2_le1 : w ^ 2 ≤ 1 := by nlinarith
  have hexp_neg1_ge : (1 / 4 : ℝ) ≤ Real.exp (-1) := by
    have h_half : (1 / 2 : ℝ) ≤ Real.exp (-1 / 2 : ℝ) := by
      have h := Real.add_one_le_exp (-1 / 2 : ℝ)
      linarith
    have h_split : (-1 : ℝ) = (-1 / 2 : ℝ) + (-1 / 2 : ℝ) := by norm_num
    rw [h_split, Real.exp_add]
    nlinarith [Real.exp_pos (-1 / 2 : ℝ)]
  have hexp_w_ge : (1 / 4 : ℝ) ≤ Real.exp (-(w ^ 2)) :=
    le_trans hexp_neg1_ge (Real.exp_le_exp.mpr (by linarith))
  have h_lb : (1 / 24 : ℝ) * w ^ (5 / 2 : ℝ) ≤ finiteQLambda L w := by
    by_cases hL_eq1 : L = 1
    · subst hL_eq1
      have hIcc1 : Finset.Icc 1 1 = {1} := by decide
      have hl1 : liouvilleLambda 1 = 1 := by simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
      dsimp [finiteQLambda]
      rw [hIcc1, Finset.sum_singleton, hl1]
      push_cast
      have h_simp : w ^ (5 / 2 : ℝ) * (1 * ((1 : ℝ) ^ 3)⁻¹ * Real.exp (-(w ^ 2) / (1 : ℝ) ^ 2)) =
          w ^ (5 / 2 : ℝ) * Real.exp (-(w ^ 2)) := by ring
      rw [h_simp]
      nlinarith
    · have hL2 : 2 ≤ L := by omega
      have h_split_Icc : Finset.Icc 1 L = insert 1 (insert 2 (Finset.Icc 3 L)) := by
        ext n
        simp only [Finset.mem_Icc, Finset.mem_insert]
        omega
      have h1_not : (1 : ℕ) ∉ insert 2 (Finset.Icc 3 L) := by
        simp only [Finset.mem_insert, Finset.mem_Icc]
        omega
      have h2_not : (2 : ℕ) ∉ Finset.Icc 3 L := by
        simp only [Finset.mem_Icc]
        omega
      have hl1 : liouvilleLambda 1 = 1 := by simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
      have hl2 : liouvilleLambda 2 = -1 := by
        have ho2 : natOmega 2 = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr Nat.prime_two
        simp [liouvilleLambda, ho2, liouvilleSignFromOmega]
      have h_tail_lb :
          -(∑ n ∈ Finset.Icc 3 L, ((n : ℝ) ^ 3)⁻¹) ≤
            ∑ n ∈ Finset.Icc 3 L,
              (liouvilleLambda n : ℝ) * ((n : ℝ) ^ 3)⁻¹ * Real.exp (-(w ^ 2) / (n : ℝ) ^ 2) := by
        rw [← Finset.sum_neg_distrib]
        apply Finset.sum_le_sum
        intro n hn
        rw [Finset.mem_Icc] at hn
        have hn_ne : n ≠ 0 := by omega
        have h_lam_abs : |(liouvilleLambda n : ℝ)| = 1 := by
          have hsq : ((liouvilleLambda n : ℝ)) ^ 2 = 1 := by
            have h_int := liouvilleLambda_sq_aux hn_ne
            have h_cast : (liouvilleLambda n : ℝ) * (liouvilleLambda n : ℝ) = 1 := by exact_mod_cast h_int
            rw [sq, h_cast]
          exact sq_eq_one_iff.mp hsq |>.elim (fun h => by rw [h, abs_one]) (fun h => by rw [h, abs_neg, abs_one])
        have h_lam_ge : (-1 : ℝ) ≤ (liouvilleLambda n : ℝ) := (abs_le.mp (le_of_eq h_lam_abs)).1
        have hexp_le1 : Real.exp (-(w ^ 2) / (n : ℝ) ^ 2) ≤ 1 := by
          apply Real.exp_le_one_iff.mpr
          exact div_nonpos_of_nonpos_of_nonneg (by nlinarith) (sq_nonneg _)
        have hexp_pos : 0 ≤ Real.exp (-(w ^ 2) / (n : ℝ) ^ 2) := le_of_lt (Real.exp_pos _)
        have hn3_pos : 0 ≤ ((n : ℝ) ^ 3)⁻¹ := by positivity
        have h1 : -(((n : ℝ) ^ 3)⁻¹ * Real.exp (-(w ^ 2) / (n : ℝ) ^ 2)) ≤
            (liouvilleLambda n : ℝ) * ((n : ℝ) ^ 3)⁻¹ * Real.exp (-(w ^ 2) / (n : ℝ) ^ 2) := by
          have h_mul := mul_le_mul_of_nonneg_right h_lam_ge (mul_nonneg hn3_pos hexp_pos)
          linarith
        have h2 : -((n : ℝ) ^ 3)⁻¹ ≤ -(((n : ℝ) ^ 3)⁻¹ * Real.exp (-(w ^ 2) / (n : ℝ) ^ 2)) := by
          have h_mul := mul_le_mul_of_nonneg_left hexp_le1 hn3_pos
          linarith
        exact le_trans h2 h1
      have h_n2_lb :
          -(1 / 8 : ℝ) ≤ (-1 : ℝ) * ((2 : ℝ) ^ 3)⁻¹ * Real.exp (-(w ^ 2) / (2 : ℝ) ^ 2) := by
        have hexp2_le1 : Real.exp (-(w ^ 2) / (2 : ℝ) ^ 2) ≤ 1 :=
          Real.exp_le_one_iff.mpr (div_nonpos_of_nonpos_of_nonneg (by nlinarith) (sq_nonneg _))
        have h23 : (-1 : ℝ) * ((2 : ℝ) ^ 3)⁻¹ = -(1 / 8 : ℝ) := by norm_num
        rw [h23]
        linarith
      have h_cube_ub := sum_inv_cube_Icc_three_le_one_twelfth_aux L
      dsimp [finiteQLambda]
      rw [h_split_Icc, Finset.sum_insert h1_not, Finset.sum_insert h2_not, hl1, hl2]
      push_cast
      have h_t1 : (1 : ℝ) * ((1 : ℝ) ^ 3)⁻¹ * Real.exp (-(w ^ 2) / (1 : ℝ) ^ 2) = Real.exp (-(w ^ 2)) := by ring
      rw [h_t1]
      have h_bracket :
          (1 / 24 : ℝ) ≤
            Real.exp (-(w ^ 2)) +
              ((-1 : ℝ) * ((2 : ℝ) ^ 3)⁻¹ * Real.exp (-(w ^ 2) / (2 : ℝ) ^ 2) +
                ∑ n ∈ Finset.Icc 3 L,
                  (liouvilleLambda n : ℝ) * ((n : ℝ) ^ 3)⁻¹ * Real.exp (-(w ^ 2) / (n : ℝ) ^ 2)) := by
        linarith
      have h_mul := mul_le_mul_of_nonneg_left h_bracket (le_of_lt hw_pow_pos)
      linarith
  exact ⟨h_lb, lt_of_lt_of_le (by positivity) h_lb⟩

/-- Finite-horizon normalized energy supremum `G_ε(R) := sup_{1 ≤ Z ≤ R} (E(Z) / Z^ε)` (`TASK-TC-057R` §5). -/
noncomputable def normalizedScaleSupremum (E : ℝ → ℝ) (ε R : ℝ) : ℝ :=
  sSup ((fun Z => E Z / Z ^ ε) '' Set.Icc 1 R)

/-- Helper (`TASK-TC-057R` §5): local finiteness, nonnegativity, pointwise domination, and
    `monotoneScaleEnvelope` domination for `normalizedScaleSupremum E ε R` on `[1, R]`
    without assuming continuity of `E`, supremum attainment, or global normalized finiteness. -/
private theorem normalizedScaleSupremum_props_aux
    {E : ℝ → ℝ} {M_lin : ℝ}
    (hE_nn : ∀ Z : ℝ, 1 ≤ Z → 0 ≤ E Z)
    (hM_nn : 0 ≤ M_lin)
    (hE_lin : ∀ Z : ℝ, 1 ≤ Z → E Z ≤ M_lin * Z)
    {ε R : ℝ} (hε : 0 ≤ ε) (hR : 1 ≤ R) :
    ((fun Z => E Z / Z ^ ε) '' Set.Icc 1 R).Nonempty ∧
      BddAbove ((fun Z => E Z / Z ^ ε) '' Set.Icc 1 R) ∧
      0 ≤ normalizedScaleSupremum E ε R ∧
      normalizedScaleSupremum E ε R ≤ M_lin * R ∧
      (∀ Z ∈ Set.Icc 1 R,
        E Z / Z ^ ε ≤ normalizedScaleSupremum E ε R ∧
          E Z ≤ normalizedScaleSupremum E ε R * Z ^ ε) ∧
      (∀ W ∈ Set.Icc 1 R,
        monotoneScaleEnvelope E W ≤ normalizedScaleSupremum E ε R * W ^ ε) := by
  let S_norm := (fun Z => E Z / Z ^ ε) '' Set.Icc 1 R
  have h_ne : S_norm.Nonempty := ⟨E 1 / (1 : ℝ) ^ ε, 1, ⟨le_refl 1, hR⟩, rfl⟩
  have h_pt_lin : ∀ Z ∈ Set.Icc 1 R, E Z / Z ^ ε ≤ M_lin * R := by
    intro Z hZ
    rcases hZ with ⟨hZ1, hZR⟩
    have hZ_pow_ge1 : (1 : ℝ) ≤ Z ^ ε := Real.one_le_rpow hZ1 hε
    have h_div_le : E Z / Z ^ ε ≤ E Z := div_le_self (hE_nn Z hZ1) hZ_pow_ge1
    exact le_trans h_div_le (le_trans (hE_lin Z hZ1) (mul_le_mul_of_nonneg_left hZR hM_nn))
  have h_bdd : BddAbove S_norm := by
    refine ⟨M_lin * R, ?_⟩
    rintro _ ⟨Z, hZ, rfl⟩
    exact h_pt_lin Z hZ
  have h_ub_div : ∀ Z ∈ Set.Icc 1 R, E Z / Z ^ ε ≤ normalizedScaleSupremum E ε R := by
    intro Z hZ
    exact le_csSup h_bdd ⟨Z, hZ, rfl⟩
  have h_nn : 0 ≤ normalizedScaleSupremum E ε R := by
    have h1_div_nn : 0 ≤ E 1 / (1 : ℝ) ^ ε := by
      rw [Real.one_rpow, div_one]
      exact hE_nn 1 (le_refl 1)
    exact le_trans h1_div_nn (h_ub_div 1 ⟨le_refl 1, hR⟩)
  have h_le_MR : normalizedScaleSupremum E ε R ≤ M_lin * R := by
    apply csSup_le h_ne
    rintro _ ⟨Z, hZ, rfl⟩
    exact h_pt_lin Z hZ
  have h_ub_both : ∀ Z ∈ Set.Icc 1 R,
      E Z / Z ^ ε ≤ normalizedScaleSupremum E ε R ∧
        E Z ≤ normalizedScaleSupremum E ε R * Z ^ ε := by
    intro Z hZ
    have hZ_pos : 0 < Z := lt_of_lt_of_le zero_lt_one hZ.1
    have hZ_pow_pos : 0 < Z ^ ε := Real.rpow_pos_of_pos hZ_pos ε
    have h1 := h_ub_div Z hZ
    exact ⟨h1, (div_le_iff hZ_pow_pos).mp h1⟩
  have h_env : ∀ W ∈ Set.Icc 1 R,
      monotoneScaleEnvelope E W ≤ normalizedScaleSupremum E ε R * W ^ ε := by
    intro W hW
    rcases hW with ⟨hW1, hWR⟩
    obtain ⟨h_pt_F, _⟩ := monotoneScaleEnvelope_basic_props_aux hE_nn hM_nn hE_lin
    obtain ⟨hF_ne, _, _, _, _⟩ := h_pt_F W hW1
    apply csSup_le hF_ne
    rintro _ ⟨Z, ⟨hZ1, hZW⟩, rfl⟩
    have hZ_mem : Z ∈ Set.Icc 1 R := ⟨hZ1, le_trans hZW hWR⟩
    have hEZ := (h_ub_both Z hZ_mem).2
    have hZ_pow_le : Z ^ ε ≤ W ^ ε := Real.rpow_le_rpow (by linarith) hZW hε
    exact le_trans hEZ (mul_le_mul_of_nonneg_left hZ_pow_le h_nn)
  exact ⟨h_ne, h_bdd, h_nn, h_le_MR, h_ub_both, h_env⟩

/-- Helper (`TASK-TC-057R` §5): monotone decay of `Y ^ (-α)` for `0 ≤ α` and `1 ≤ Y_star ≤ Y`. -/
private theorem rpow_neg_antitone_of_one_le_aux
    {Y_star Y α : ℝ} (hY_star : 1 ≤ Y_star) (hYY : Y_star ≤ Y) (hα : 0 ≤ α) :
    Y ^ (-α) ≤ Y_star ^ (-α) := by
  have hY_star_pos : 0 < Y_star := lt_of_lt_of_le zero_lt_one hY_star
  have hY_nn : 0 ≤ Y := le_of_lt (lt_of_lt_of_le hY_star_pos hYY)
  have h_pos_pow : 0 < Y_star ^ α := Real.rpow_pos_of_pos hY_star_pos α
  have h_le_pow : Y_star ^ α ≤ Y ^ α := Real.rpow_le_rpow (le_of_lt hY_star_pos) hYY hα
  rw [Real.rpow_neg hY_nn, Real.rpow_neg (le_of_lt hY_star_pos)]
  exact inv_le_inv_of_le h_pos_pow h_le_pow

/-- **Theorem 26 (`TASK-TC-057R` §5, `CONDITIONAL_ON_SIGNED_CORRELATION` Route D Same-Scale Absorption Transfer and Repaired Coefficient-Mass Localization)**:
    *Formal scope (`CONDITIONAL_ON_SIGNED_CORRELATION`)*:
    1. Finite-horizon local finiteness and envelope domination of `normalizedScaleSupremum E ε R = sup_{1 ≤ Z ≤ R} (E(Z) / Z^ε)`
       from the local linear bound `E(Z) ≤ M_lin * Z`, without assuming continuity of `E`, supremum attainment,
       or a priori global normalized finiteness;
    2. Complete conditional Route D transfer preserving exact outer factor `2` in
       `E(Y) ≤ 2 * D_tilde(Y) + 2 * X_tilde(Y) + 2 * E_sh1(Y)`:
       if `0 < η < ε`, `0 ≤ θ_η < 1 / 2`, `2 * θ_η < q < 1`, `1 ≤ Y_star`, and for all `Y ≥ Y_star`
       both the Route D diagonal bound `D_tilde(Y) ≤ ∑_{pk ∈ S(Y)} w(Y, pk) F(Y / d(Y, pk)) + C_cut`
       and the open signed-correlation hypothesis `X_tilde(Y) + E_sh1(Y) ≤ A_η Y^η + θ_η F(Y)` hold
       with `2 * θ_η + 2 * ∑_{pk ∈ S(Y)} w(Y, pk) d(Y, pk)^{-ε} ≤ q`, then for every finite horizon `R ≥ Y_star`,
       `G_ε(R) ≤ max(G_ε(Y_star), K + q * G_ε(R))` with `K = 2 A_η Y_star^{η - ε} + 2 C_cut Y_star^{-ε}`,
       hence `G_ε(R) ≤ max(G_ε(Y_star), K / (1 - q))` and uniformly for all `Y ≥ 1`,
       `E(Y) ≤ max(G_ε(Y_star), K / (1 - q)) * Y^ε` and `F(Y) ≤ max(G_ε(Y_star), K / (1 - q)) * Y^ε`
       (together with sharpness of `θ_η < 1 / 2`: when `1 / 2 ≤ θ` and `0 ≤ Θ_diag`, `1 ≤ 2 * θ + 2 * Θ_diag`);
    3. Repaired Proposition 2.4 coefficient-mass algebra: total mass on `d ≥ U_Y` gives an upper bound on
       `∑ w_i d_i^{-σ}`, a lower bound requires quantitative mass localization on `d_i ≤ κ * U_Y`, and
       mass concentrated at `d_top ≥ Y / 2` satisfies `B_mass * d_top^{-σ} ≤ B_mass * (Y / 2)^{-σ}`.
    Does NOT prove the open arithmetic signed-correlation inequality for `Q_{λ,T(Y)}`. -/
theorem conditional_signed_correlation_same_scale_absorption_transfer_tc057r
    {E : ℝ → ℝ} {M_lin : ℝ}
    (hE_nn : ∀ Z : ℝ, 1 ≤ Z → 0 ≤ E Z)
    (hM_nn : 0 ≤ M_lin)
    (hE_lin : ∀ Z : ℝ, 1 ≤ Z → E Z ≤ M_lin * Z) :
    (∀ (ε R : ℝ), 0 ≤ ε → 1 ≤ R →
      BddAbove ((fun Z => E Z / Z ^ ε) '' Set.Icc 1 R) ∧
        0 ≤ normalizedScaleSupremum E ε R ∧
        normalizedScaleSupremum E ε R ≤ M_lin * R ∧
        (∀ W ∈ Set.Icc 1 R,
          monotoneScaleEnvelope E W ≤ normalizedScaleSupremum E ε R * W ^ ε)) ∧
    ((∀ (θ Θ_diag : ℝ), 1 / 2 ≤ θ → 0 ≤ Θ_diag → 1 ≤ 2 * θ + 2 * Θ_diag) ∧
      ∀ (D_tilde X_tilde E_sh1 : ℝ → ℝ)
        (S : ℝ → Finset (ℕ × ℕ)) (w d : ℝ → ℕ × ℕ → ℝ)
        (η ε A_η θ_η C_cut q Y_star : ℝ),
        0 < η → η < ε → 0 ≤ A_η → 0 ≤ C_cut →
        0 ≤ θ_η → θ_η < 1 / 2 → 2 * θ_η < q → q < 1 → 1 ≤ Y_star →
        (∀ Y : ℝ, Y_star ≤ Y →
          E Y ≤ 2 * D_tilde Y + 2 * X_tilde Y + 2 * E_sh1 Y) →
        (∀ Y : ℝ, Y_star ≤ Y →
          (∀ pk ∈ S Y, 0 ≤ w Y pk ∧ 1 ≤ d Y pk ∧ d Y pk ≤ Y) ∧
            D_tilde Y ≤
              (∑ pk ∈ S Y, w Y pk * monotoneScaleEnvelope E (Y / d Y pk)) + C_cut) →
        (∀ Y : ℝ, Y_star ≤ Y →
          X_tilde Y + E_sh1 Y ≤ A_η * Y ^ η + θ_η * monotoneScaleEnvelope E Y) →
        (∀ Y : ℝ, Y_star ≤ Y →
          2 * θ_η + 2 * (∑ pk ∈ S Y, w Y pk * (d Y pk) ^ (-ε)) ≤ q) →
        let K := 2 * A_η * Y_star ^ (η - ε) + 2 * C_cut * Y_star ^ (-ε)
        (∀ R : ℝ, Y_star ≤ R →
          normalizedScaleSupremum E ε R ≤
            max (normalizedScaleSupremum E ε Y_star)
              (K + q * normalizedScaleSupremum E ε R) ∧
          normalizedScaleSupremum E ε R ≤
            max (normalizedScaleSupremum E ε Y_star) (K / (1 - q))) ∧
        (∀ Y : ℝ, 1 ≤ Y →
          E Y ≤ max (normalizedScaleSupremum E ε Y_star) (K / (1 - q)) * Y ^ ε ∧
            monotoneScaleEnvelope E Y ≤
              max (normalizedScaleSupremum E ε Y_star) (K / (1 - q)) * Y ^ ε)) ∧
    (∀ (S_loc S_all : Finset ℕ) (w d : ℕ → ℝ) (U_Y κ sig B_mass d_top Y : ℝ),
      ((0 < U_Y → 0 ≤ sig → (∀ i ∈ S_all, 0 ≤ w i ∧ U_Y ≤ d i) →
          ∑ i ∈ S_all, w i * (d i) ^ (-sig) ≤ (∑ i ∈ S_all, w i) * U_Y ^ (-sig)) ∧
        (S_loc ⊆ S_all → 0 < U_Y → 1 ≤ κ → 0 ≤ sig →
          (∀ i ∈ S_all, 0 ≤ w i ∧ 0 < d i) →
          (∀ i ∈ S_loc, d i ≤ κ * U_Y) →
          (∑ i ∈ S_loc, w i) * (κ * U_Y) ^ (-sig) ≤ ∑ i ∈ S_all, w i * (d i) ^ (-sig)) ∧
        (0 ≤ B_mass → 0 ≤ sig → 0 < Y → Y / 2 ≤ d_top →
          B_mass * d_top ^ (-sig) ≤ B_mass * (Y / 2) ^ (-sig)))) := by
  refine ⟨?_, ⟨?_, ?_⟩, ?_⟩
  · intro ε R hε hR
    obtain ⟨_, h_bdd, h_nn, h_MR, _, h_env⟩ :=
      normalizedScaleSupremum_props_aux hE_nn hM_nn hE_lin hε hR
    exact ⟨h_bdd, h_nn, h_MR, h_env⟩
  · intro θ Θ_diag hθ hΘ
    linarith
  · intro D_tilde X_tilde E_sh1 S w d η ε A_η θ_η C_cut q Y_star
      hη_pos hηε hA_nn hC_nn hθ_nn _ _ hq_lt1 hY_star
      hE_decomp hD_bound hX_corr h_contract
    dsimp only
    let K := 2 * A_η * Y_star ^ (η - ε) + 2 * C_cut * Y_star ^ (-ε)
    have hε_pos : 0 < ε := lt_trans hη_pos hηε
    have hε_nn : 0 ≤ ε := le_of_lt hε_pos
    have h_horizon :
        ∀ R : ℝ, Y_star ≤ R →
          normalizedScaleSupremum E ε R ≤
            max (normalizedScaleSupremum E ε Y_star)
              (K + q * normalizedScaleSupremum E ε R) ∧
          normalizedScaleSupremum E ε R ≤
            max (normalizedScaleSupremum E ε Y_star) (K / (1 - q)) := by
      intro R hR_star
      have hR1 : 1 ≤ R := le_trans hY_star hR_star
      obtain ⟨h_ne_R, _, hG_nn, _, _, h_env_R⟩ :=
        normalizedScaleSupremum_props_aux hE_nn hM_nn hE_lin hε_nn hR1
      obtain ⟨_, _, _, _, h_ub_star, _⟩ :=
        normalizedScaleSupremum_props_aux hE_nn hM_nn hE_lin hε_nn hY_star
      let G := normalizedScaleSupremum E ε R
      have h_self_rec :
          G ≤ max (normalizedScaleSupremum E ε Y_star) (K + q * G) := by
        apply csSup_le h_ne_R
        rintro _ ⟨Y, ⟨hY1, hYR⟩, rfl⟩
        by_cases hY_le_star : Y ≤ Y_star
        · exact le_trans (h_ub_star Y ⟨hY1, hY_le_star⟩).1 (le_max_left _ _)
        · have hY_ge_star : Y_star ≤ Y := le_of_not_ge hY_le_star
          have hY_pos : 0 < Y := lt_of_lt_of_le zero_lt_one hY1
          have hY_nn : 0 ≤ Y := le_of_lt hY_pos
          have hY_eps_pos : 0 < Y ^ ε := Real.rpow_pos_of_pos hY_pos ε
          have hY_eps_nn : 0 ≤ Y ^ ε := le_of_lt hY_eps_pos
          obtain ⟨h_pk_cond, hD_Y⟩ := hD_bound Y hY_ge_star
          have h_sum_le :
              ∑ pk ∈ S Y, w Y pk * monotoneScaleEnvelope E (Y / d Y pk) ≤
                (G * Y ^ ε) * ∑ pk ∈ S Y, w Y pk * (d Y pk) ^ (-ε) := by
            rw [Finset.mul_sum]
            apply Finset.sum_le_sum
            intro pk hpk
            obtain ⟨hw_nn, hd1, hdY⟩ := h_pk_cond pk hpk
            have hd_pos : 0 < d Y pk := lt_of_lt_of_le zero_lt_one hd1
            have hd_nn : 0 ≤ d Y pk := le_of_lt hd_pos
            have hW1 : 1 ≤ Y / d Y pk := (one_le_div hd_pos).mpr hdY
            have hWY : Y / d Y pk ≤ Y := div_le_self hY_nn hd1
            have hWR : Y / d Y pk ≤ R := le_trans hWY hYR
            have hFW : monotoneScaleEnvelope E (Y / d Y pk) ≤ G * (Y / d Y pk) ^ ε :=
              h_env_R (Y / d Y pk) ⟨hW1, hWR⟩
            have h_pow_div : (Y / d Y pk) ^ ε = Y ^ ε * (d Y pk) ^ (-ε) := by
              rw [Real.div_rpow hY_nn hd_nn ε, div_eq_mul_inv, Real.rpow_neg hd_nn]
            rw [h_pow_div] at hFW
            have h_mul := mul_le_mul_of_nonneg_left hFW hw_nn
            linarith
          have hFY : monotoneScaleEnvelope E Y ≤ G * Y ^ ε := h_env_R Y ⟨hY1, hYR⟩
          have h_same_le : X_tilde Y + E_sh1 Y ≤ A_η * Y ^ η + θ_η * (G * Y ^ ε) := by
            have h1 := hX_corr Y hY_ge_star
            have h2 := mul_le_mul_of_nonneg_left hFY hθ_nn
            linarith
          have hE_raw :
              E Y ≤ (2 * A_η * Y ^ η + 2 * C_cut) +
                (2 * θ_η + 2 * ∑ pk ∈ S Y, w Y pk * (d Y pk) ^ (-ε)) * (G * Y ^ ε) := by
            have hE_Y := hE_decomp Y hY_ge_star
            linarith
          have hGY_nn : 0 ≤ G * Y ^ ε := mul_nonneg hG_nn hY_eps_nn
          have h_q_mul :
              (2 * θ_η + 2 * ∑ pk ∈ S Y, w Y pk * (d Y pk) ^ (-ε)) * (G * Y ^ ε) ≤
                q * (G * Y ^ ε) :=
            mul_le_mul_of_nonneg_right (h_contract Y hY_ge_star) hGY_nn
          have hE_q : E Y ≤ (2 * A_η * Y ^ η + 2 * C_cut) + (q * G) * Y ^ ε := by
            linarith
          have h_eta_div : Y ^ η / Y ^ ε = Y ^ (η - ε) := by
            rw [← Real.rpow_sub hY_pos]
          have h_eta_mono : Y ^ (η - ε) ≤ Y_star ^ (η - ε) := by
            have h_sub_eq : η - ε = -(ε - η) := by ring
            rw [h_sub_eq]
            exact rpow_neg_antitone_of_one_le_aux hY_star hY_ge_star (by linarith)
          have h_cut_div : (1 : ℝ) / Y ^ ε = Y ^ (-ε) := by
            rw [one_div, Real.rpow_neg hY_nn]
          have h_cut_mono : Y ^ (-ε) ≤ Y_star ^ (-ε) :=
            rpow_neg_antitone_of_one_le_aux hY_star hY_ge_star hε_nn
          have h_div_step : E Y / Y ^ ε ≤ K + q * G := by
            have h_div_raw :
                E Y / Y ^ ε ≤
                  ((2 * A_η * Y ^ η + 2 * C_cut) + (q * G) * Y ^ ε) / Y ^ ε :=
              div_le_div_of_nonneg_right hE_q hY_eps_nn
            have h_split :
                ((2 * A_η * Y ^ η + 2 * C_cut) + (q * G) * Y ^ ε) / Y ^ ε =
                  2 * A_η * (Y ^ η / Y ^ ε) + 2 * C_cut * ((1 : ℝ) / Y ^ ε) + q * G := by
              field_simp [ne_of_gt hY_eps_pos]
            rw [h_split, h_eta_div, h_cut_div] at h_div_raw
            have hA_step : 2 * A_η * Y ^ (η - ε) ≤ 2 * A_η * Y_star ^ (η - ε) :=
              mul_le_mul_of_nonneg_left h_eta_mono (by linarith)
            have hC_step : 2 * C_cut * Y ^ (-ε) ≤ 2 * C_cut * Y_star ^ (-ε) :=
              mul_le_mul_of_nonneg_left h_cut_mono (by linarith)
            dsimp [K]
            linarith
          exact le_trans h_div_step (le_max_right _ _)
      have h_abs :
          G ≤ max (normalizedScaleSupremum E ε Y_star) (K / (1 - q)) := by
        rcases le_max_iff.mp h_self_rec with h_left | h_right
        · exact le_trans h_left (le_max_left _ _)
        · have h1q_pos : 0 < 1 - q := by linarith
          have h_lin : G * (1 - q) ≤ K := by linarith
          have h_div : G ≤ K / (1 - q) := (le_div_iff h1q_pos).mpr h_lin
          exact le_trans h_div (le_max_right _ _)
      exact ⟨h_self_rec, h_abs⟩
    refine ⟨h_horizon, ?_⟩
    intro Y hY1
    let R := max Y Y_star
    have hR_star : Y_star ≤ R := le_max_right Y Y_star
    have hYR : Y ≤ R := le_max_left Y Y_star
    have hR1 : 1 ≤ R := le_trans hY_star hR_star
    obtain ⟨_, _, _, _, h_ub_R, h_env_R⟩ :=
      normalizedScaleSupremum_props_aux hE_nn hM_nn hE_lin hε_nn hR1
    have hG_bound := (h_horizon R hR_star).2
    have hY_eps_nn : 0 ≤ Y ^ ε := Real.rpow_nonneg (by linarith) ε
    have hEY_le : E Y ≤ normalizedScaleSupremum E ε R * Y ^ ε :=
      (h_ub_R Y ⟨hY1, hYR⟩).2
    have hFY_le : monotoneScaleEnvelope E Y ≤ normalizedScaleSupremum E ε R * Y ^ ε :=
      h_env_R Y ⟨hY1, hYR⟩
    have h_mult := mul_le_mul_of_nonneg_right hG_bound hY_eps_nn
    exact ⟨le_trans hEY_le h_mult, le_trans hFY_le h_mult⟩
  · intro S_loc S_all w d U_Y κ sig B_mass d_top Y
    refine ⟨?_, ?_, ?_⟩
    · intro hU_pos hσ h_all
      rw [Finset.sum_mul]
      apply Finset.sum_le_sum
      intro i hi
      obtain ⟨hwi, hdi⟩ := h_all i hi
      have hd_pos : 0 < d i := lt_of_lt_of_le hU_pos hdi
      have h_pow : (d i) ^ (-sig) ≤ U_Y ^ (-sig) := by
        rw [Real.rpow_neg (le_of_lt hd_pos), Real.rpow_neg (le_of_lt hU_pos)]
        exact inv_le_inv_of_le (Real.rpow_pos_of_pos hU_pos sig)
          (Real.rpow_le_rpow (le_of_lt hU_pos) hdi hσ)
      exact mul_le_mul_of_nonneg_left h_pow hwi
    · intro h_sub hU_pos hκ1 hσ h_all h_loc
      have hκU_pos : 0 < κ * U_Y := mul_pos (lt_of_lt_of_le zero_lt_one hκ1) hU_pos
      have h_loc_le :
          (∑ i ∈ S_loc, w i) * (κ * U_Y) ^ (-sig) ≤ ∑ i ∈ S_loc, w i * (d i) ^ (-sig) := by
        rw [Finset.sum_mul]
        apply Finset.sum_le_sum
        intro i hi
        obtain ⟨hwi, hdi_pos⟩ := h_all i (h_sub hi)
        have hdi_le := h_loc i hi
        have h_pow : (κ * U_Y) ^ (-sig) ≤ (d i) ^ (-sig) := by
          rw [Real.rpow_neg (le_of_lt hκU_pos), Real.rpow_neg (le_of_lt hdi_pos)]
          exact inv_le_inv_of_le (Real.rpow_pos_of_pos hdi_pos sig)
            (Real.rpow_le_rpow (le_of_lt hdi_pos) hdi_le hσ)
        exact mul_le_mul_of_nonneg_left h_pow hwi
      have h_sub_le :
          ∑ i ∈ S_loc, w i * (d i) ^ (-sig) ≤ ∑ i ∈ S_all, w i * (d i) ^ (-sig) := by
        apply Finset.sum_le_sum_of_subset_of_nonneg h_sub
        intro i hi _
        obtain ⟨hwi, hdi_pos⟩ := h_all i hi
        exact mul_nonneg hwi (Real.rpow_nonneg (le_of_lt hdi_pos) (-sig))
      exact le_trans h_loc_le h_sub_le
    · intro hB hσ hY_pos hd_top
      have hY2_pos : 0 < Y / 2 := half_pos hY_pos
      have hd_pos : 0 < d_top := lt_of_lt_of_le hY2_pos hd_top
      have h_pow : d_top ^ (-sig) ≤ (Y / 2) ^ (-sig) := by
        rw [Real.rpow_neg (le_of_lt hd_pos), Real.rpow_neg (le_of_lt hY2_pos)]
        exact inv_le_inv_of_le (Real.rpow_pos_of_pos hY2_pos sig)
          (Real.rpow_le_rpow (le_of_lt hY2_pos) hd_top hσ)
      exact mul_le_mul_of_nonneg_left h_pow hB

end LiouvilleSquareDilation

end RiemannScope
