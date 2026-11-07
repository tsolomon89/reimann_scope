/-
RiemannScope.LiouvilleSquareDilation
TASK-TC-054 / TASK-TC-054R:
1. Actual arithmetic definitions and theorems over `ℕ` and `ℤ` using Mathlib's
   `ArithmeticFunction.cardFactors` (`Ω`), `Nat.factorization`, and `ArithmeticFunction.moebius` (`μ`):
   - Connection of `Ω(n)` to prime-factorization multiplicities `(n.factorization.sum fun _ e => e) = natOmega n`;
   - Additivity `natOmega (m * n) = natOmega m + natOmega n` for positive integers;
   - Actual Liouville function `liouvilleLambda n = (-1)^{Ω(n)}`, its `ArithmeticFunction ℤ` wrapper
     `liouvilleArith`, complete multiplicativity `liouvilleLambda (m * n) = liouvilleLambda m * liouvilleLambda n`,
     unit square `liouvilleLambda d * liouvilleLambda d = 1`, and unconstrained common-factor sign cancellation
     `liouvilleLambda (d * r) * liouvilleLambda (d * s) = liouvilleLambda r * liouvilleLambda s`;
   - Connection of `ArithmeticFunction.moebius (p ^ k)` and `liouvilleLambda (p ^ k)` to the prime-power
     exponent model, actual prime-power square-divisor sums
     `primePowerActualMoebiusSquareSum p k = liouvilleLambda (p ^ k)` and
     `primePowerActualInverseLiouvilleSquareSum p k = ArithmeticFunction.moebius (p ^ k)`,
     factored prime-power product formulas over `n.factorization.prod` for all `n ≠ 0`, and
     multiplicative uniqueness `ArithmeticFunction.IsMultiplicative.eq_iff_eq_on_prime_powers`.
2. Prime-power exponent models (`liouville_complete_multiplicativity_and_common_factor_cancellation_nat`
   and `prime_power_square_divisor_moebius_liouville_inversion_nat`).
3. Scalar real-algebra and real-inequality lemmas for weighted norm bounds, Euler-Maclaurin `C_2` and
   subtransition exponents, dyadic parity square expansion, Abel scaling antiderivative combine,
   Fourier tail ratio denominator monotonicity, and unequal-block sum bounds.
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

/-- **Theorem 4 (`TASK-TC-054R` §8, Actual Möbius & Square-Divisor Sums on Prime Powers and Factored Integers)**:
    Connects `primePowerMoebius` and `liouvilleSignFromOmega` to Mathlib's `ArithmeticFunction.moebius` (`μ`)
    and `liouvilleLambda` (`λ`), proves the actual prime-power square-divisor identities
    `∑_{0 ≤ j ≤ k/2} μ(p^{k - 2j}) = λ(p^k)` and `∑_{0 ≤ j ≤ k/2} μ(p^j) λ(p^{k - 2j}) = μ(p^k)`,
    proves the factored prime-power product identities for `λ(n)` and `μ(n)` over `n.factorization.prod`
    for all positive integers `n ≠ 0`, and proves that any multiplicative `S : ArithmeticFunction ℤ`
    agreeing with these square-divisor sums on prime powers equals `λ(n)` (resp. `μ(n)`) for all `n : ℕ`. -/
theorem actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat
    {p n : ℕ} (hp : p.Prime) (k : ℕ) (hn : n ≠ 0)
    (S : ArithmeticFunction ℤ) (hS : S.IsMultiplicative) :
    (ArithmeticFunction.moebius (p ^ k) = primePowerMoebius k ∧
      liouvilleLambda (p ^ k) = liouvilleSignFromOmega k) ∧
    (primePowerActualMoebiusSquareSum p k = liouvilleLambda (p ^ k) ∧
      primePowerActualInverseLiouvilleSquareSum p k = ArithmeticFunction.moebius (p ^ k)) ∧
    (liouvilleLambda n = n.factorization.prod (fun q e => primePowerActualMoebiusSquareSum q e) ∧
      ArithmeticFunction.moebius n = n.factorization.prod (fun q e => primePowerActualInverseLiouvilleSquareSum q e)) ∧
    (((∀ q e : ℕ, q.Prime → S (q ^ e) = primePowerActualMoebiusSquareSum q e) → S n = liouvilleLambda n) ∧
      ((∀ q e : ℕ, q.Prime → S (q ^ e) = primePowerActualInverseLiouvilleSquareSum q e) → S n = ArithmeticFunction.moebius n)) := by
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
  have h_ext_lam : (∀ q e : ℕ, q.Prime → S (q ^ e) = primePowerActualMoebiusSquareSum q e) → S n = liouvilleLambda n := by
    intro hS_pp
    have h_eq_fn : S = liouvilleArith := by
      rw [ArithmeticFunction.IsMultiplicative.eq_iff_eq_on_prime_powers S hS liouvilleArith h_mult_lam]
      intro q e hq
      rw [hS_pp q e hq, h_fwd_pp q e hq]
      rfl
    exact congrFun (congrArg DFunLike.coe h_eq_fn) n
  have h_ext_mu : (∀ q e : ℕ, q.Prime → S (q ^ e) = primePowerActualInverseLiouvilleSquareSum q e) → S n = ArithmeticFunction.moebius n := by
    intro hS_pp
    have h_eq_fn : S = ArithmeticFunction.moebius := by
      rw [ArithmeticFunction.IsMultiplicative.eq_iff_eq_on_prime_powers S hS ArithmeticFunction.moebius ArithmeticFunction.isMultiplicative_moebius]
      intro q e hq
      rw [hS_pp q e hq, h_inv_pp q e hq]
    exact congrFun (congrArg DFunLike.coe h_eq_fn) n
  exact ⟨⟨moebius_apply_prime_pow_eq_primePowerMoebius_aux hp k, liouvilleLambda_prime_pow_aux hp k⟩,
    ⟨h_fwd_pp p k hp, h_inv_pp p k hp⟩, ⟨h_prod_lam, h_prod_mu⟩, ⟨h_ext_lam, h_ext_mu⟩⟩

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

/-- **Theorem 8 (`TASK-TC-054R` §§2, 4, 6, Scalar Real-Algebra Lemma)**:
    1. Global Stieltjes variation antiderivative combination:
       `(1 / 2) * ((2 * (3 / 2) - 1) * e_neg_3_2 - (2 * 0 - 1)) + (1 / 2) * (0 - (-(2 * (3 / 2) - 1) * e_neg_3_2)) = 1 / 2 + 2 * e_neg_3_2`;
    2. Fourier residue tail denominator monotonicity: for `1 ≤ K` and `K + 1 ≤ m`,
       `0 < (K - 1 / 2) * (2 * K + 3) * (2 * K + 4) ≤ (m - 3 / 2) * (2 * m + 1) * (2 * m + 2)`;
    3. Unequal-block `s^{-3}` sum bound algebra: for `2 ≤ B`,
       `1 / B ^ 3 + 1 / (2 * B ^ 2) ≤ 1 / B ^ 2`. -/
theorem abel_scaling_fourier_ratio_and_unequal_block_algebra
    (e_neg_3_2 K m B : ℝ)
    (hK : 1 ≤ K)
    (hm : K + 1 ≤ m)
    (hB : 2 ≤ B) :
    ((1 / 2 : ℝ) * ((2 * (3 / 2 : ℝ) - 1) * e_neg_3_2 - (2 * 0 - 1)) +
      (1 / 2 : ℝ) * (0 - (-(2 * (3 / 2 : ℝ) - 1) * e_neg_3_2)) =
        (1 / 2 : ℝ) + 2 * e_neg_3_2) ∧
    (0 < (K - 1 / 2) * (2 * K + 3) * (2 * K + 4) ∧
      (K - 1 / 2) * (2 * K + 3) * (2 * K + 4) ≤ (m - 3 / 2) * (2 * m + 1) * (2 * m + 2) ∧
      0 < (K + 2) * (2 * K + 8) * (2 * K + 9) ∧
      (K + 2) * (2 * K + 8) * (2 * K + 9) ≤ (m + 1) * (2 * m + 6) * (2 * m + 7)) ∧
    (1 / B ^ 3 + 1 / (2 * B ^ 2) ≤ 1 / B ^ 2) := by
  refine ⟨by ring, ?_, ?_⟩
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
  · have hB_pos : 0 < B := by linarith
    have h_diff : 1 / B ^ 2 - (1 / B ^ 3 + 1 / (2 * B ^ 2)) = (B - 2) / (2 * B ^ 3) := by
      field_simp [ne_of_gt hB_pos]
      ring
    have h_nonneg : 0 ≤ (B - 2) / (2 * B ^ 3) :=
      div_nonneg (by linarith) (by positivity)
    linarith

end LiouvilleSquareDilation

end RiemannScope
