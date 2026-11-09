/-
RiemannScope.LiouvilleSquareDilation
TASK-TC-054 / TASK-TC-054R / TASK-TC-054R2 / TASK-TC-055 / TASK-TC-055R / TASK-TC-055R2:
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
     pointwise weighted cofactor square expansion with `1/r` and `λ(r)λ(s)/√(rs)` (`TASK-TC-055R2` §§2–3).
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

end LiouvilleSquareDilation

end RiemannScope
