/-
RiemannScope.ZeroArithmeticInvariants
TASK-TC-038: Arithmetic Nature of Nontrivial Zeros, Exact Zero-Sum Invariants,
and Special-Value Transfer Audit.

Formalizes the exact algebraic identities of TASK-TC-038:
1. `shifted_ordinate_rational_iff`: γ is rational iff γ + 1/2 is rational.
2. `shifted_ordinate_algebraic_iff`: for any subfield A ≤ ℝ (such as Q̄ ∩ ℝ), γ ∈ A ↔ γ + 1/2 ∈ A.
3. `shifted_ordinate_transcendental_iff`: for any subfield A ≤ ℝ, γ ∉ A ↔ γ + 1/2 ∉ A.
4. `complex_zero_re_im_algebraicity`: exact conjugation reconstruction of real/imaginary parts
   (ρ + conj ρ)/2 = β and (ρ - conj ρ)/(2i) = γ, subfield equivalence, and RH specialization.
5. `reflection_reciprocal_identity`: 1/(ρ(1 - ρ)) = 1/ρ + 1/(1 - ρ) and ρ(1 - ρ) = 1/4 - z^2.
6. `centered_quartet_polynomial_identity`: (X - z)(X + z)(X - conj z)(X + conj z)
   = X^4 - 2(δ^2 - γ^2)X^2 + (δ^2 + γ^2)^2.
7. `centered_quartet_coefficients_real`: z^2 + (conj z)^2 = 2(δ^2 - γ^2),
   z^2(conj z)^2 = (δ^2 + γ^2)^2, and nonnegativity (δ^2 + γ^2)^2 ≥ 0.
8. `li_first_coefficient_finite_algebra_identity`: 1 - (1 - 1/ρ)^1 = 1/ρ and reflection-pair sum
   [1 - (1 - 1/ρ)] + [1 - (1 - 1/(1 - ρ))] = 1/(ρ(1 - ρ)).
9. `reciprocal_power_log_derivative_sign_identity`: sign normalization of reciprocal-power terms
   and centered odd-power cancellation z^{-(2k+1)} + (-z)^{-(2k+1)} = 0 vs even-power doubling.

Scope firewall:
Does NOT claim to formalize Hadamard factorization of ξ(s), transcendence status of zeta zeros,
Bui–Conrey–Young zero density, Li's criterion, or Voros superzeta analytic continuation.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Algebra.Field.Subfield
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

namespace RiemannScope

open Complex

/-! ### 1. Shifted-Ordinate Redundancy (`γ` vs `γ + 1/2`) -/

/-- 1. Rationality equivalence under shift by `1/2`:
    A real ordinate `γ` is rational (`∃ q : ℚ, (q : ℝ) = γ`) if and only if
    the shifted ordinate `γ + 1/2` is rational (`∃ q' : ℚ, (q' : ℝ) = γ + 1/2`). -/
theorem shifted_ordinate_rational_iff (γ : ℝ) :
    (∃ q : ℚ, (q : ℝ) = γ) ↔ (∃ q' : ℚ, (q' : ℝ) = γ + 1 / 2) := by
  constructor
  · rintro ⟨q, rfl⟩
    refine ⟨q + 1 / 2, ?_⟩
    push_cast
    ring
  · rintro ⟨q', hq'⟩
    refine ⟨q' - 1 / 2, ?_⟩
    push_cast
    linarith

/-- Helper lemma: every subfield `A : Subfield ℝ` contains `1 / 2`. -/
theorem half_mem_subfield (A : Subfield ℝ) : (1 / 2 : ℝ) ∈ A := by
  have h1 : (1 : ℝ) ∈ A := A.one_mem
  have h2 : (2 : ℝ) ∈ A := by
    have h11 : (1 : ℝ) + (1 : ℝ) ∈ A := A.add_mem h1 h1
    norm_num at h11 ⊢
    exact h11
  exact A.div_mem h1 h2

/-- 2. Subfield / algebraicity equivalence under shift by `1/2`:
    For any subfield `A : Subfield ℝ` (in particular `A = Q̄ ∩ ℝ`),
    `γ ∈ A ↔ γ + 1 / 2 ∈ A`. -/
theorem shifted_ordinate_algebraic_iff (A : Subfield ℝ) (γ : ℝ) :
    γ ∈ A ↔ γ + 1 / 2 ∈ A := by
  have h_half : (1 / 2 : ℝ) ∈ A := half_mem_subfield A
  constructor
  · intro hγ
    exact A.add_mem hγ h_half
  · intro h_shift
    have h_sub : (γ + 1 / 2) - 1 / 2 ∈ A := A.sub_mem h_shift h_half
    have h_eq : (γ + 1 / 2) - 1 / 2 = γ := by ring
    rwa [h_eq] at h_sub

/-- 3. Transcendence (subfield-complement) equivalence under shift by `1/2`:
    For any subfield `A : Subfield ℝ` (in particular `A = Q̄ ∩ ℝ`),
    `γ ∉ A ↔ γ + 1 / 2∉ A`. -/
theorem shifted_ordinate_transcendental_iff (A : Subfield ℝ) (γ : ℝ) :
    γ ∉ A ↔ γ + 1 / 2 ∉ A := by
  exact not_iff_not.mpr (shifted_ordinate_algebraic_iff A γ)

/-! ### 2. Full Complex Zero vs. Real and Imaginary Parts -/

/-- 4. Complex zero real/imaginary reconstruction and subfield algebraicity equivalence:
    For `ρ = β + i γ` and `ρ_conj = β - i γ`, the symmetric combinations recover `β` and `γ`:
    `(ρ + ρ_conj) / 2 = β` and `(ρ - ρ_conj) / (2i) = γ`.
    Moreover, for any subfield `A : Subfield ℝ`, under the critical-line hypothesis `β = 1/2`,
    `β ∈ A ∧ γ ∈ A ↔ γ ∈ A`. -/
theorem complex_zero_re_im_algebraicity (A : Subfield ℝ) (β γ : ℝ) :
    ((((β : ℂ) + (γ : ℂ) * I) + ((β : ℂ) - (γ : ℂ) * I)) / 2 = (β : ℂ)) ∧
    ((((β : ℂ) + (γ : ℂ) * I) - ((β : ℂ) - (γ : ℂ) * I)) / (2 * I) = (γ : ℂ)) ∧
    ((β = 1 / 2) → ((β ∈ A ∧ γ ∈ A) ↔ γ ∈ A)) := by
  refine ⟨by ring, ?_, ?_⟩
  · have hI : (2 * I : ℂ) ≠ 0 := mul_ne_zero two_ne_zero I_ne_zero
    field_simp [hI]
    ring
  · intro hβ
    subst hβ
    have h_half : (1 / 2 : ℝ) ∈ A := half_mem_subfield A
    exact ⟨fun h => h.2, fun hγ => ⟨h_half, hγ⟩⟩

/-! ### 3. Functional-Equation Reflection Reciprocal Identity -/

/-- 5. Partial-fraction decomposition of the reflection-invariant reciprocal product:
    For `ρ ≠ 0` and `1 - ρ ≠ 0`,
    `1 / (ρ * (1 - ρ)) = 1 / ρ + 1 / (1 - ρ)`,
    and in centered coordinates `ρ = 1/2 + z`, `ρ * (1 - ρ) = 1/4 - z^2`. -/
theorem reflection_reciprocal_identity (ρ z : ℂ) (hρ : ρ ≠ 0) (h1ρ : 1 - ρ ≠ 0) :
    (1 / (ρ * (1 - ρ)) = 1 / ρ + 1 / (1 - ρ)) ∧
    ((1 / 2 + z) * (1 - (1 / 2 + z)) = (1 / 4 : ℂ) - z ^ 2) := by
  refine ⟨?_, by ring⟩
  field_simp [hρ, h1ρ]

/-! ### 4. Centered Quartet Polynomial and Real Symmetric Coordinates -/

/-- 6. Centered quartet monic polynomial identity:
    For `z = δ + i γ` and `z_bar = δ - i γ`, the four centered quartet roots `{z, -z, z_bar, -z_bar}`
    have monic degree-4 polynomial
    `(X - z)(X + z)(X - z_bar)(X + z_bar) = X^4 - 2(δ^2 - γ^2)X^2 + (δ^2 + γ^2)^2`. -/
theorem centered_quartet_polynomial_identity (δ γ : ℝ) (X : ℂ) :
    (X - ((δ : ℂ) + (γ : ℂ) * I)) * (X + ((δ : ℂ) + (γ : ℂ) * I)) *
      (X - ((δ : ℂ) - (γ : ℂ) * I)) * (X + ((δ : ℂ) - (γ : ℂ) * I)) =
      X ^ 4 - 2 * ((δ : ℂ) ^ 2 - (γ : ℂ) ^ 2) * X ^ 2 +
        ((δ : ℂ) ^ 2 + (γ : ℂ) ^ 2) ^ 2 := by
  have hI2 : (I : ℂ) ^ 2 = -1 := I_sq
  calc
    (X - ((δ : ℂ) + (γ : ℂ) * I)) * (X + ((δ : ℂ) + (γ : ℂ) * I)) *
        (X - ((δ : ℂ) - (γ : ℂ) * I)) * (X + ((δ : ℂ) - (γ : ℂ) * I))
      = X ^ 4 - 2 * ((δ : ℂ) ^ 2 + (γ : ℂ) ^ 2 * I ^ 2) * X ^ 2 +
          ((δ : ℂ) ^ 2 - (γ : ℂ) ^ 2 * I ^ 2) ^ 2 := by ring
    _ = X ^ 4 - 2 * ((δ : ℂ) ^ 2 - (γ : ℂ) ^ 2) * X ^ 2 +
          ((δ : ℂ) ^ 2 + (γ : ℂ) ^ 2) ^ 2 := by
      rw [hI2]
      ring

/-- 7. Real symmetric quartet coordinates:
    For `z = δ + i γ` and `z_bar = δ - i γ`,
    `z^2 + z_bar^2 = 2(δ^2 - γ^2)`, `z^2 * z_bar^2 = (δ^2 + γ^2)^2`,
    and the constant term `(δ^2 + γ^2)^2` is nonnegative over `ℝ`. -/
theorem centered_quartet_coefficients_real (δ γ : ℝ) :
    ((((δ : ℂ) + (γ : ℂ) * I) ^ 2 + ((δ : ℂ) - (γ : ℂ) * I) ^ 2 =
      2 * ((δ : ℂ) ^ 2 - (γ : ℂ) ^ 2)) ∧
    (((δ : ℂ) + (γ : ℂ) * I) ^ 2 * ((δ : ℂ) - (γ : ℂ) * I) ^ 2 =
      ((δ : ℂ) ^ 2 + (γ : ℂ) ^ 2) ^ 2) ∧
    (0 ≤ (δ ^ 2 + γ ^ 2) ^ 2)) := by
  have hI2 : (I : ℂ) ^ 2 = -1 := I_sq
  refine ⟨?_, ?_, sq_nonneg (δ ^ 2 + γ ^ 2)⟩
  · calc
      ((δ : ℂ) + (γ : ℂ) * I) ^ 2 + ((δ : ℂ) - (γ : ℂ) * I) ^ 2
        = 2 * ((δ : ℂ) ^ 2 + (γ : ℂ) ^ 2 * I ^ 2) := by ring
      _ = 2 * ((δ : ℂ) ^ 2 - (γ : ℂ) ^ 2) := by rw [hI2]; ring
  · calc
      ((δ : ℂ) + (γ : ℂ) * I) ^ 2 * ((δ : ℂ) - (γ : ℂ) * I) ^ 2
        = ((δ : ℂ) ^ 2 - (γ : ℂ) ^ 2 * I ^ 2) ^ 2 := by ring
      _ = ((δ : ℂ) ^ 2 + (γ : ℂ) ^ 2) ^ 2 := by rw [hI2]; ring

/-! ### 5. First Li Coefficient and Reciprocal-Power Sign/Parity Identities -/

/-- 8. Finite algebraic identity for the first Li coefficient (`n = 1`):
    Each zero term satisfies `1 - (1 - 1 / ρ)^1 = 1 / ρ`, and pairing `ρ` with `1 - ρ`
    gives `[1 - (1 - 1 / ρ)] + [1 - (1 - 1 / (1 - ρ))] = 1 / (ρ * (1 - ρ))`. -/
theorem li_first_coefficient_finite_algebra_identity (ρ : ℂ) (hρ : ρ ≠ 0) (h1ρ : 1 - ρ ≠ 0) :
    (1 - (1 - 1 / ρ) ^ (1 : ℕ) = 1 / ρ) ∧
    ((1 - (1 - 1 / ρ) ^ (1 : ℕ)) + (1 - (1 - 1 / (1 - ρ)) ^ (1 : ℕ)) =
      1 / (ρ * (1 - ρ))) := by
  refine ⟨by ring, ?_⟩
  field_simp [hρ, h1ρ]

/-- 9. Reciprocal-power logarithmic-derivative sign and centered parity identity:
    In the Taylor expansion `-d/ds log(1 - s/ρ) = ∑_{m≥1} s^{m-1} / ρ^m`, the double minus sign
    cancels (`-(-1 / ρ^m) = 1 / ρ^m`), and for a centered reflection pair `{z, -z}`,
    odd powers cancel (`z^{2k+1} + (-z)^{2k+1} = 0`)
    while even powers double (`z^{2k} + (-z)^{2k} = 2 * z^{2k}`). -/
theorem reciprocal_power_log_derivative_sign_identity (ρ z : ℂ) (m k : ℕ) :
    (-(-(1 / ρ ^ m)) = 1 / ρ ^ m) ∧
    (z ^ (2 * k + 1) + (-z) ^ (2 * k + 1) = 0) ∧
    (z ^ (2 * k) + (-z) ^ (2 * k) = 2 * z ^ (2 * k)) := by
  have h_even : (-z) ^ (2 * k) = z ^ (2 * k) := by
    rw [pow_mul, neg_sq, ← pow_mul]
  refine ⟨by ring, ?_, ?_⟩
  · calc
      z ^ (2 * k + 1) + (-z) ^ (2 * k + 1)
        = z ^ (2 * k) * z + (-z) ^ (2 * k) * (-z) := by rw [pow_succ, pow_succ]
      _ = z ^ (2 * k) * z + z ^ (2 * k) * (-z) := by rw [h_even]
      _ = 0 := by ring
  · rw [h_even]
    ring

end RiemannScope
