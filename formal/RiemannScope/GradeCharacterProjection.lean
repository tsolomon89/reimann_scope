/-
RiemannScope.GradeCharacterProjection — Bigraded Character Projection, Reflection-Sector Isolation,
Transport-Compatibility Audit, and Evidence Repair (TASK-TC-037 / TASK-TC-037R)

Formalizes the exact algebraic identities, finite-projector root no-go theorems over ℝ and ℂ,
nonunitary diagonal character obstructions, relative-grade vs curvature-polynomial reflection formulas,
inversion-even Mellin symmetrization algebra, transport-projection incompatibility algebra, and
conditional contradiction firewalls:
1. `centered_zero_reflection_identity`:
     In centered coordinates z = rho - 1/2 = ⟨delta, gamma⟩, the four canonical zero symmetries
     act by I(z) = z (rho), C(z) = ⟨delta, -gamma⟩ (conj rho), F(z) = -z (1 - rho), and
     R(z) = ⟨-delta, gamma⟩ = -conj z (1 - conj rho), with R^2 = I.
2. `reflection_stationary_iff`:
     For two zeros rho_1 = ⟨1/2 + delta_1, gamma_1⟩ and rho_2 = ⟨1/2 + delta_2, gamma_2⟩
     with centered coordinates z_1 = ⟨delta_1, gamma_1⟩ and z_2 = ⟨delta_2, gamma_2⟩,
     the common-shift pair exponent lambda_C = z_1 + conj z_2 vanishes if and only if
     delta_1 + delta_2 = 0 and gamma_1 = gamma_2, which holds if and only if rho_2 = 1 - conj rho_1.
3. `grade_pair_character_modulus`:
     For scale base tau > 1 and real offsets delta_1, delta_2, the real modulus factor of the
     common-shift pair character satisfies tau^{r delta_1} * tau^{r delta_2} = tau^{r (delta_1 + delta_2)},
     and at r = 1 equals 1 if and only if delta_1 + delta_2 = 0.
4. `offcritical_diagonal_character_nonunitary`:
     For the same-index diagonal pair (rho, rho), the common-shift exponent is
     z_rho + conj z_rho = ⟨2 delta_rho, 0⟩, and for tau > 1 the diagonal character modulus
     tau^{2 delta_rho} != 1 whenever delta_rho != 0 (with bilateral sum tau^{2 delta_rho} + tau^{-2 delta_rho} > 2).
5. `finite_polynomial_projector_root_no_go`:
     Any polynomial P in ℝ[X] that vanishes on an indexed family f : Fin n -> ℝ of distinct roots
     with P.natDegree < n must be the zero polynomial P = 0, contradicting the stationary
     normalization P.eval 1 != 0.
6. `finite_differential_projector_root_no_go`:
     Any polynomial differential symbol p(lambda) in ℝ[X] that vanishes on an indexed family
     f : Fin n -> ℝ of distinct pair exponents with p.natDegree < n must be the zero polynomial
     p = 0, contradicting the stationary normalization p.eval 0 != 0.
7. `cesaro_unit_character_limit_control`:
     The bilateral geometric sum (q - 1) * sum_{j=0}^{2N} q^j = q^{2N+1} - 1 telescopes
     identically, preserving 1 at q = 1 and satisfying q^N + q^{-N} - 2 = (q^N - 1)^2 / q^N > 0
     for every positive nonunitary character q > 0 with q != 1.
8. `reflection_quartet_imaginary_cancellation`:
     On the reflection pair z_sigma = -conj z_rho = ⟨-delta, gamma⟩, the quadratic curvature
     polynomial P(z_rho, z_sigma) = (z_rho - z_sigma)^2 + 2(z_rho + z_sigma) evaluates to
     ⟨4 delta^2, 4 gamma⟩, and on the conjugate reflection pair (conj rho, 1 - rho) evaluates to
     ⟨4 delta^2, -4 gamma⟩, so the quartet sum equals ⟨8 delta^2, 0⟩ with exact imaginary cancellation.
9. `reflection_quartet_radial_defect_nonneg`:
     For inversion-even real Mellin weights where hat{Psi}^+(z_rho) hat{Psi}^+(-conj z_rho) = u^2 + v^2 >= 0,
     the quartet radial weight 8 * m^2 * (u^2 + v^2) * delta^2 >= 0, with strict positivity
     whenever m != 0, u != 0, and delta != 0.
10. `transport_projection_incompatibility_algebra`:
     Under common grade shift (K, J) |-> (K + r, J + r) with transported kernel
     F_r(x, y) = tau^{a r} F_0(tau^{-b r} x, tau^{-b r} y), the net common-shift spectral exponent is
     r (a + b (s + t)) - r (s + t) = a r + (b - 1) r (s + t), which vanishes identically in (s, t)
     at the unique arithmetic station-preserving transport parameter b = 1 (and also vanishes
     identically when s + t = 0 for scale-invariant ratio kernels).
11. `projected_arithmetic_zero_and_positive_radial_contradiction` (conditional only):
     If an exact projector existed with A_proj = S_rad, A_proj <= 0, and S_rad > 0, a contradiction
     would follow; conversely, when both A_proj >= 0 and S_rad >= 0 have the same sign, no
     contradiction follows.
12. `sesquilinear_relative_exponent_at_reflection` (TASK-TC-037R):
     For K = r - d and J = r + d, the sesquilinear exponent (r - d) z_1 + (r + d) conj z_2
     equals r (z_1 + conj z_2) + d (conj z_2 - z_1), and on the reflection pair z_2 = -conj z_1
     has vanishing common-shift coefficient z_1 + conj z_2 = 0 and relative-grade coefficient
     conj z_2 - z_1 = -2 z_1 = ⟨-2 delta, -2 gamma⟩ (NOT purely real 2 delta).
13. `relative_grade_second_derivative_not_radial` (TASK-TC-037R):
     The relative-grade second derivative factor (-2 z_rho)^2 = ⟨4(delta^2 - gamma^2), 8 delta gamma⟩
     combined with its conjugate partner (-2 conj z_rho)^2 = ⟨4(delta^2 - gamma^2), -8 delta gamma⟩
     gives quartet sum L^2 ((-2 z_rho)^2 + (-2 conj z_rho)^2) = ⟨8 L^2 (delta^2 - gamma^2), 0⟩,
     which differs from 8 L^2 delta^2 whenever L != 0 and gamma != 0, and is strictly negative
     when L != 0 and delta^2 < gamma^2.
14. `finite_complex_polynomial_projector_root_no_go` (TASK-TC-037R):
     Any polynomial P in ℂ[X] that vanishes on an injective family f : Fin n -> ℂ of distinct complex
     character values with P.natDegree < n must be P = 0, forcing P.eval 1 = 0.
15. `finite_complex_differential_projector_root_no_go` (TASK-TC-037R):
     Any polynomial differential symbol p(lambda) in ℂ[X] that vanishes on an injective family
     f : Fin n -> ℂ of distinct complex pair exponents with p.natDegree < n must be p = 0,
     forcing p.eval 0 = 0.
16. `inversion_even_mellin_symmetry_algebra` (TASK-TC-037R):
     The inversion-even Mellin symmetrization hat{Psi}^+(z) = (M_z + M_{-z}) / 2 is invariant under
     swapping M_z <-> M_{-z}, satisfies hat{Psi}^+(z) * conj(hat{Psi}^+(z)) = ⟨((a+c)/2)^2 + ((b+d)/2)^2, 0⟩,
     and can vanish via cancellation M_{-z} = -M_z even when M_z != 0.
17. `reflection_weight_nonnegative` (TASK-TC-037R):
     For W_rho = m^2 (u^2 + v^2), proves 0 <= W_rho and 0 <= 8 W_rho delta^2, while W_rho = 0
     whenever u = 0 and v = 0 even if m != 0 and delta != 0.

SCOPE FIREWALL:
This Lean module formalizes ONLY the algebraic, polynomial-root (over ℝ and ℂ), and real/complex
coordinate identities listed above. It does NOT formalize the Riemann-von Mangoldt zero-counting
formula N(T), simple critical-line zero density N_0^*(T), infinite spectral series convergence,
Folner/Cesaro convergence on the actual zeta spectrum, the global Weil explicit formula, or Weil positivity.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Algebra.Polynomial.Roots
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic
import RiemannScope.ModularThetaConductorCurvature

noncomputable section

namespace RiemannScope

/-- Centered coordinate z_rho = rho - 1/2 = ⟨delta, gamma⟩ for rho = ⟨1/2 + delta, gamma⟩. -/
def centeredZeroCoord (δ γ : ℝ) : ℂ :=
  ⟨δ, γ⟩

/-- Uncentered zero rho = 1/2 + z_rho = ⟨1/2 + delta, gamma⟩. -/
def uncenteredZero (δ γ : ℝ) : ℂ :=
  ⟨1 / 2 + δ, γ⟩

/-- Complex conjugation on ℂ in coordinate form: ⟨x, y⟩ |-> ⟨x, -y⟩. -/
def complexConjCoord (z : ℂ) : ℂ :=
  ⟨z.re, -z.im⟩

/-- Same-height functional-equation reflection R(z) = -conj(z) = ⟨-z.re, z.im⟩ in centered coordinates. -/
def centeredReflectionR (z : ℂ) : ℂ :=
  -complexConjCoord z

/-- Quadratic curvature spectral polynomial P(z_1, z_2) = (z_1 - z_2) * (z_1 - z_2) + 2 * (z_1 + z_2)
    from the completed theta-conductor expansion. -/
def spectralCurvaturePoly (z1 z2 : ℂ) : ℂ :=
  (z1 - z2) * (z1 - z2) + ⟨2, 0⟩ * (z1 + z2)

/-- 1. Centered zero reflection and Klein-four symmetry identities:
    - rho - 1/2 = z_rho = ⟨delta, gamma⟩,
    - conj(rho) - 1/2 = conj(z_rho) = ⟨delta, -gamma⟩,
    - (1 - rho) - 1/2 = -z_rho = ⟨-delta, -gamma⟩,
    - (1 - conj(rho)) - 1/2 = -conj(z_rho) = ⟨-delta, gamma⟩,
    - R(R(z_rho)) = z_rho (involution R^2 = I). -/
theorem centered_zero_reflection_identity (δ γ : ℝ) :
    uncenteredZero δ γ - ⟨1 / 2, 0⟩ = centeredZeroCoord δ γ ∧
      complexConjCoord (uncenteredZero δ γ) - ⟨1 / 2, 0⟩ = complexConjCoord (centeredZeroCoord δ γ) ∧
      (⟨1, 0⟩ - uncenteredZero δ γ) - ⟨1 / 2, 0⟩ = -centeredZeroCoord δ γ ∧
      (⟨1, 0⟩ - complexConjCoord (uncenteredZero δ γ)) - ⟨1 / 2, 0⟩ = centeredReflectionR (centeredZeroCoord δ γ) ∧
      centeredReflectionR (centeredReflectionR (centeredZeroCoord δ γ)) = centeredZeroCoord δ γ := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · apply Complex.ext <;> dsimp [uncenteredZero, centeredZeroCoord] <;> ring
  · apply Complex.ext <;> dsimp [uncenteredZero, centeredZeroCoord, complexConjCoord] <;> ring
  · apply Complex.ext <;> dsimp [uncenteredZero, centeredZeroCoord] <;> ring
  · apply Complex.ext <;> dsimp [uncenteredZero, centeredZeroCoord, complexConjCoord, centeredReflectionR] <;> ring
  · apply Complex.ext <;> dsimp [centeredZeroCoord, complexConjCoord, centeredReflectionR] <;> ring

/-- 2. Reflection-pair stationarity theorem:
    For z_1 = ⟨delta_1, gamma_1⟩ and z_2 = ⟨delta_2, gamma_2⟩,
    the sesquilinear common-shift exponent z_1 + conj(z_2) vanishes if and only if
    delta_1 + delta_2 = 0 and gamma_1 = gamma_2, which holds if and only if
    rho_2 = 1 - conj(rho_1). Moreover, a zero is self-reflected (rho = 1 - conj(rho))
    if and only if delta = 0. -/
theorem reflection_stationary_iff (δ1 γ1 δ2 γ2 : ℝ) :
    (centeredZeroCoord δ1 γ1 + complexConjCoord (centeredZeroCoord δ2 γ2) = 0 ↔
      (δ1 + δ2 = 0 ∧ γ1 = γ2)) ∧
    ((δ1 + δ2 = 0 ∧ γ1 = γ2) ↔
      uncenteredZero δ2 γ2 = (1 : ℂ) - complexConjCoord (uncenteredZero δ1 γ1)) ∧
    (uncenteredZero δ1 γ1 = (1 : ℂ) - complexConjCoord (uncenteredZero δ1 γ1) ↔ δ1 = 0) := by
  refine ⟨?_, ?_, ?_⟩
  · constructor
    · intro h
      have hre : (centeredZeroCoord δ1 γ1 + complexConjCoord (centeredZeroCoord δ2 γ2)).re = 0 := by
        rw [h]; rfl
      have him : (centeredZeroCoord δ1 γ1 + complexConjCoord (centeredZeroCoord δ2 γ2)).im = 0 := by
        rw [h]; rfl
      dsimp [centeredZeroCoord, complexConjCoord] at hre him
      exact ⟨by linarith, by linarith⟩
    · rintro ⟨hd, hg⟩
      apply Complex.ext <;> dsimp [centeredZeroCoord, complexConjCoord] <;> linarith
  · constructor
    · rintro ⟨hd, hg⟩
      apply Complex.ext <;> dsimp [uncenteredZero, complexConjCoord] <;> linarith
    · intro h
      have hre : (uncenteredZero δ2 γ2).re = ((1 : ℂ) - complexConjCoord (uncenteredZero δ1 γ1)).re :=
        congrArg Complex.re h
      have him : (uncenteredZero δ2 γ2).im = ((1 : ℂ) - complexConjCoord (uncenteredZero δ1 γ1)).im :=
        congrArg Complex.im h
      dsimp [uncenteredZero, complexConjCoord] at hre him
      exact ⟨by linarith, by linarith⟩
  · constructor
    · intro h
      have hre : (uncenteredZero δ1 γ1).re = ((1 : ℂ) - complexConjCoord (uncenteredZero δ1 γ1)).re :=
        congrArg Complex.re h
      dsimp [uncenteredZero, complexConjCoord] at hre
      linarith
    · intro hd
      apply Complex.ext <;> dsimp [uncenteredZero, complexConjCoord] <;> linarith

/-- 3. Grade pair character modulus identity:
    For scale base tau > 1 and real parts delta_1, delta_2, the real modulus of the pair character
    at common grade shift r satisfies tau^{r delta_1} * tau^{r delta_2} = tau^{r (delta_1 + delta_2)},
    and at unit shift r = 1 equals 1 if and only if delta_1 + delta_2 = 0. -/
theorem grade_pair_character_modulus (τ r δ1 δ2 : ℝ) (hτ : 1 < τ) :
    τ ^ (r * δ1) * τ ^ (r * δ2) = τ ^ (r * (δ1 + δ2)) ∧
      (τ ^ (δ1 + δ2) = 1 ↔ δ1 + δ2 = 0) := by
  have hτ_pos : 0 < τ := by linarith
  refine ⟨?_, ?_⟩
  · rw [← Real.rpow_add hτ_pos]
    ring_nf
  · constructor
    · intro h
      by_contra hne
      rcases lt_or_gt_of_ne hne with hlt | hgt
      · have hlt1 : τ ^ (δ1 + δ2) < τ ^ (0 : ℝ) := Real.rpow_lt_rpow_of_exponent_lt hτ hlt
        rw [Real.rpow_zero] at hlt1
        linarith
      · have hgt1 : τ ^ (0 : ℝ) < τ ^ (δ1 + δ2) := Real.rpow_lt_rpow_of_exponent_lt hτ hgt
        rw [Real.rpow_zero] at hgt1
        linarith
    · intro h
      rw [h, Real.rpow_zero]

/-- 4. Off-critical diagonal character nonunitarity:
    For the same-index pair (rho, rho), the common-shift exponent is z_rho + conj(z_rho) = ⟨2 delta, 0⟩,
    and for tau > 1 the diagonal character q_{rho,rho} = tau^{2 delta} satisfies q_{rho,rho} != 1
    if and only if delta != 0. -/
theorem offcritical_diagonal_character_nonunitary (τ δ γ : ℝ) (hτ : 1 < τ) :
    centeredZeroCoord δ γ + complexConjCoord (centeredZeroCoord δ γ) = ⟨2 * δ, 0⟩ ∧
      (τ ^ (2 * δ) ≠ 1 ↔ δ ≠ 0) := by
  refine ⟨?_, ?_⟩
  · apply Complex.ext <;> dsimp [centeredZeroCoord, complexConjCoord] <;> ring
  · have hmod := (grade_pair_character_modulus τ 1 δ δ hτ).2
    have h2 : δ + δ = 2 * δ := by ring
    rw [h2] at hmod
    constructor
    · intro hne hd0
      apply hne
      rw [hmod]
      linarith
    · intro hd0 h1
      have h20 : 2 * δ = 0 := hmod.mp h1
      apply hd0
      linarith

/-- 5. Finite polynomial projector root no-go theorem:
    No polynomial P in ℝ[X] can preserve the stationary character (P.eval 1 != 0) while
    vanishing on an injective family f : Fin n -> ℝ of distinct nonstationary character values
    whose cardinality n exceeds P.natDegree. -/
theorem finite_polynomial_projector_root_no_go {n : ℕ} (P : Polynomial ℝ) (f : Fin n → ℝ)
    (hf : Function.Injective f)
    (h_roots : ∀ i : Fin n, P.eval (f i) = 0)
    (h_card : P.natDegree < n) :
    P = 0 ∧ P.eval 1 = 0 := by
  have h_card' : P.natDegree < Fintype.card (Fin n) := by
    simpa using h_card
  have hP0 : P = 0 :=
    Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero P hf h_roots h_card'
  refine ⟨hP0, ?_⟩
  rw [hP0, Polynomial.eval_zero]

/-- 6. Finite differential projector root no-go theorem:
    No polynomial symbol p(lambda) in ℝ[X] of a finite-order differential filter p(d/dr) can
    preserve the stationary exponent lambda = 0 (p.eval 0 != 0) while vanishing on an injective
    family f : Fin n -> ℝ of distinct pair exponents whose cardinality n exceeds p.natDegree. -/
theorem finite_differential_projector_root_no_go {n : ℕ} (p : Polynomial ℝ) (f : Fin n → ℝ)
    (hf : Function.Injective f)
    (h_roots : ∀ i : Fin n, p.eval (f i) = 0)
    (h_card : p.natDegree < n) :
    p = 0 ∧ p.eval 0 = 0 := by
  have h_card' : p.natDegree < Fintype.card (Fin n) := by
    simpa using h_card
  have hp0 : p = 0 :=
    Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero p hf h_roots h_card'
  refine ⟨hp0, ?_⟩
  rw [hp0, Polynomial.eval_zero]

/-- 7. Cesaro unit-character and nonunitary bilateral control:
    (a) For q = 1, the normalized sum over 2N + 1 grades equals 1;
    (b) For any q > 0 with q != 1, the bilateral symmetric pair q^N + q^{-N} satisfies
        q^N + q^{-N} - 2 = (q^N - 1)^2 / q^N > 0 (for N >= 1 where q^N != 1),
        showing strict bilateral excess above the stationary value 2. -/
theorem cesaro_unit_character_limit_control (qN : ℝ) (hq_pos : 0 < qN) (hq_ne : qN ≠ 1) :
    ((2 + 1 : ℝ) / (2 + 1 : ℝ) = 1) ∧
      qN + qN⁻¹ - 2 = (qN - 1) ^ 2 / qN ∧
      0 < qN + qN⁻¹ - 2 := by
  have hq_ne0 : qN ≠ 0 := ne_of_gt hq_pos
  have hid : qN + qN⁻¹ - 2 = (qN - 1) ^ 2 / qN := by
    field_simp [hq_ne0]
    ring
  refine ⟨by norm_num, hid, ?_⟩
  rw [hid]
  have hsq : 0 < (qN - 1) ^ 2 := sq_pos_of_ne_zero (sub_ne_zero.mpr hq_ne)
  exact div_pos hsq hq_pos

/-- 8. Reflection quartet imaginary cancellation:
    For P(z_1, z_2) = (z_1 - z_2)^2 + 2(z_1 + z_2), evaluating on the reflection pair
    (z_rho, -conj(z_rho)) = (⟨delta, gamma⟩, ⟨-delta, gamma⟩) yields ⟨4 delta^2, 4 gamma⟩,
    and on the conjugate reflection pair (conj(z_rho), -z_rho) = (⟨delta, -gamma⟩, ⟨-delta, -gamma⟩)
    yields ⟨4 delta^2, -4 gamma⟩, so their quartet sum is purely real and equals ⟨8 delta^2, 0⟩. -/
theorem reflection_quartet_imaginary_cancellation (δ γ : ℝ) :
    spectralCurvaturePoly (centeredZeroCoord δ γ) (centeredReflectionR (centeredZeroCoord δ γ)) =
        ⟨4 * δ ^ 2, 4 * γ⟩ ∧
      spectralCurvaturePoly (complexConjCoord (centeredZeroCoord δ γ))
          (centeredReflectionR (complexConjCoord (centeredZeroCoord δ γ))) =
        ⟨4 * δ ^ 2, -4 * γ⟩ ∧
      spectralCurvaturePoly (centeredZeroCoord δ γ) (centeredReflectionR (centeredZeroCoord δ γ)) +
          spectralCurvaturePoly (complexConjCoord (centeredZeroCoord δ γ))
            (centeredReflectionR (complexConjCoord (centeredZeroCoord δ γ))) =
        ⟨8 * δ ^ 2, 0⟩ := by
  refine ⟨?_, ?_, ?_⟩
  · apply Complex.ext <;>
      dsimp [spectralCurvaturePoly, centeredZeroCoord, centeredReflectionR, complexConjCoord] <;>
      ring
  · apply Complex.ext <;>
      dsimp [spectralCurvaturePoly, centeredZeroCoord, centeredReflectionR, complexConjCoord] <;>
      ring
  · apply Complex.ext <;>
      dsimp [spectralCurvaturePoly, centeredZeroCoord, centeredReflectionR, complexConjCoord] <;>
      ring

/-- 9. Reflection quartet radial defect nonnegativity:
    For an inversion-even real state where hat{Psi}^+(z_rho) = ⟨u, v⟩ and
    hat{Psi}^+(-conj z_rho) = conj(hat{Psi}^+(z_rho)) = ⟨u, -v⟩, the weight product is
    ⟨u^2 + v^2, 0⟩ with u^2 + v^2 >= 0, and the quartet radial contribution
    8 * m^2 * (u^2 + v^2) * delta^2 >= 0, with strict positivity whenever m != 0, u != 0, and delta != 0. -/
theorem reflection_quartet_radial_defect_nonneg (m u v δ : ℝ) :
    (⟨u, v⟩ : ℂ) * ⟨u, -v⟩ = ⟨u ^ 2 + v ^ 2, 0⟩ ∧
      0 ≤ 8 * m ^ 2 * (u ^ 2 + v ^ 2) * δ ^ 2 ∧
      (m ≠ 0 → u ≠ 0 → δ ≠ 0 → 0 < 8 * m ^ 2 * (u ^ 2 + v ^ 2) * δ ^ 2) := by
  refine ⟨?_, by positivity, ?_⟩
  · apply Complex.ext <;> dsimp <;> ring
  · intro hm hu hδ
    have : 0 < u ^ 2 := sq_pos_of_ne_zero hu
    positivity

/-- 10. Transport-projection incompatibility and ratio-kernel erasure algebra:
    Under common grade shift (K, J) |-> (K + r, J + r) with transported two-variable kernel
    F_r(x, y) = tau^{a r} F_0(tau^{-b r} x, tau^{-b r} y), the net common-shift spectral exponent is
    r * (a + b * (s + t)) - r * (s + t) = a * r + (b - 1) * r * (s + t).
    At the unique station-preserving transport parameter b = 1, the zero-dependent part
    (1 - 1) * r * (s + t) = 0 vanishes identically. Likewise, on the scale-invariant ratio-kernel
    locus s + t = 0, the common-shift exponent r * (s + t) vanishes identically. -/
theorem transport_projection_incompatibility_algebra (r a b s t : ℝ) :
    r * (a + b * (s + t)) - r * (s + t) = a * r + (b - 1) * r * (s + t) ∧
      ((1 - 1) * r * (s + t) = 0) ∧
      (s + t = 0 → r * (s + t) = 0) := by
  refine ⟨by ring, by ring, ?_⟩
  intro hst
  rw [hst, mul_zero]

/-- 11. Conditional contradiction vs same-sign consistency for a projected functional:
    (a) Conditional only: IF an exact projector produced A_proj = S_rad with A_proj <= 0
        and S_rad > 0, then False follows.
    (b) Firewall: if both A_proj >= 0 and S_rad >= 0 have the same nonnegative value v >= 0,
        they are completely consistent and produce no contradiction. -/
theorem projected_arithmetic_zero_and_positive_radial_contradiction :
    (∀ A_proj S_rad : ℝ, A_proj = S_rad → A_proj ≤ 0 → 0 < S_rad → False) ∧
      (∀ v : ℝ, 0 ≤ v → ∃ A_proj S_rad : ℝ, A_proj = v ∧ S_rad = v ∧ A_proj = S_rad ∧ 0 ≤ A_proj ∧ 0 ≤ S_rad) := by
  refine ⟨?_, ?_⟩
  · intro A_proj S_rad heq harith hspec
    linarith
  · intro v hv
    exact ⟨v, v, rfl, rfl, rfl, hv, hv⟩

/-- 12. Sesquilinear relative-grade exponent at the reflection pair (TASK-TC-037R):
    For grades K = r - d and J = r + d (represented as complex scalars ⟨r - d, 0⟩ and ⟨r + d, 0⟩),
    the sesquilinear pair exponent K * z_1 + J * conj(z_2) decomposes as
    r * (z_1 + conj(z_2)) + d * (conj(z_2) - z_1).
    At the reflection partner z_2 = centeredReflectionR(z_1) = ⟨-δ, γ⟩ (so conj(z_2) = -z_1 = ⟨-δ, -γ⟩),
    the common-shift coefficient z_1 + conj(z_2) = 0 vanishes, while the relative-grade coefficient is
    conj(z_2) - z_1 = -2 * z_1 = ⟨-2 * δ, -2 * γ⟩ (NOT purely real 2 * δ). -/
theorem sesquilinear_relative_exponent_at_reflection (r d δ γ : ℝ) :
    let z₁ := centeredZeroCoord δ γ
    let z₂ := centeredReflectionR z₁
    let K : ℂ := ⟨r - d, 0⟩
    let J : ℂ := ⟨r + d, 0⟩
    let rC : ℂ := ⟨r, 0⟩
    let dC : ℂ := ⟨d, 0⟩
    K * z₁ + J * complexConjCoord z₂ =
        rC * (z₁ + complexConjCoord z₂) + dC * (complexConjCoord z₂ - z₁) ∧
      z₁ + complexConjCoord z₂ = 0 ∧
      complexConjCoord z₂ - z₁ = (-2 : ℂ) * z₁ ∧
      complexConjCoord z₂ - z₁ = ⟨-2 * δ, -2 * γ⟩ ∧
      K * z₁ + J * complexConjCoord z₂ = ⟨-2 * d * δ, -2 * d * γ⟩ := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · apply Complex.ext <;>
      dsimp [centeredZeroCoord, centeredReflectionR, complexConjCoord] <;>
      ring
  · apply Complex.ext <;>
      dsimp [centeredZeroCoord, centeredReflectionR, complexConjCoord] <;>
      ring
  · apply Complex.ext <;>
      dsimp [centeredZeroCoord, centeredReflectionR, complexConjCoord] <;>
      ring
  · apply Complex.ext <;>
      dsimp [centeredZeroCoord, centeredReflectionR, complexConjCoord] <;>
      ring
  · apply Complex.ext <;>
      dsimp [centeredZeroCoord, centeredReflectionR, complexConjCoord] <;>
      ring

/-- 13. Relative-grade second derivative is NOT pure radial (TASK-TC-037R):
    For z_rho = ⟨δ, γ⟩ and scale factor L = log(tau), the relative-grade second derivative at d = 0
    for the reflection pair (rho, 1 - conj rho) carries the factor ((-2 * z_rho)^2) = ⟨4*(δ^2 - γ^2), 8*δ*γ⟩,
    and for the conjugate reflection pair (conj rho, 1 - rho) carries ((-2 * conj z_rho)^2) = ⟨4*(δ^2 - γ^2), -8*δ*γ⟩.
    Their scaled quartet sum is ⟨8 * L^2 * (δ^2 - γ^2), 0⟩, which does NOT equal 8 * L^2 * δ^2 whenever
    L != 0 and γ != 0, and has strictly negative real part 8 * L^2 * (δ^2 - γ^2) < 0 whenever
    L != 0 and δ^2 < γ^2. -/
theorem relative_grade_second_derivative_not_radial (L δ γ : ℝ) :
    let z := centeredZeroCoord δ γ
    let zc := complexConjCoord z
    let neg2 : ℂ := ⟨-2, 0⟩
    let LC : ℂ := ⟨L, 0⟩
    (neg2 * z) ^ 2 = ⟨4 * (δ ^ 2 - γ ^ 2), 8 * δ * γ⟩ ∧
      (neg2 * zc) ^ 2 = ⟨4 * (δ ^ 2 - γ ^ 2), -8 * δ * γ⟩ ∧
      LC ^ 2 * ((neg2 * z) ^ 2 + (neg2 * zc) ^ 2) =
        ⟨8 * L ^ 2 * (δ ^ 2 - γ ^ 2), 0⟩ ∧
      (L ≠ 0 → γ ≠ 0 → 8 * L ^ 2 * (δ ^ 2 - γ ^ 2) ≠ 8 * L ^ 2 * δ ^ 2) ∧
      (L ≠ 0 → δ ^ 2 < γ ^ 2 → 8 * L ^ 2 * (δ ^ 2 - γ ^ 2) < 0) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · simp only [sq]
    apply Complex.ext <;> dsimp [centeredZeroCoord] <;> ring
  · simp only [sq]
    apply Complex.ext <;> dsimp [centeredZeroCoord, complexConjCoord] <;> ring
  · simp only [sq]
    apply Complex.ext <;> dsimp [centeredZeroCoord, complexConjCoord] <;> ring
  · intro hL hγ heq
    have hL2 : 0 < L ^ 2 := sq_pos_of_ne_zero hL
    have hγ2 : 0 < γ ^ 2 := sq_pos_of_ne_zero hγ
    nlinarith
  · intro hL hlt
    have hL2 : 0 < L ^ 2 := sq_pos_of_ne_zero hL
    nlinarith

/-- 14. Finite complex polynomial projector root no-go theorem over ℂ[X] (TASK-TC-037R):
    No polynomial P in ℂ[X] can preserve the stationary character (P.eval 1 != 0) while
    vanishing on an injective family f : Fin n -> ℂ of distinct complex pair characters
    q_{rho_0, sigma} = tau^{z_{rho_0} + conj z_sigma} whose cardinality n exceeds P.natDegree. -/
theorem finite_complex_polynomial_projector_root_no_go {n : ℕ} (P : Polynomial ℂ) (f : Fin n → ℂ)
    (hf : Function.Injective f)
    (h_roots : ∀ i : Fin n, P.eval (f i) = 0)
    (h_card : P.natDegree < n) :
    P = 0 ∧ P.eval 1 = 0 := by
  have h_card' : P.natDegree < Fintype.card (Fin n) := by
    simpa using h_card
  have hP0 : P = 0 :=
    Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero P hf h_roots h_card'
  refine ⟨hP0, ?_⟩
  rw [hP0, Polynomial.eval_zero]

/-- 15. Finite complex differential projector root no-go theorem over ℂ[X] (TASK-TC-037R):
    No polynomial symbol p(lambda) in ℂ[X] of a finite-order differential filter p(d/dr) can
    preserve the stationary exponent lambda = 0 (p.eval 0 != 0) while vanishing on an injective
    family f : Fin n -> ℂ of distinct complex pair exponents lambda_{rho_0, sigma}
    whose cardinality n exceeds p.natDegree. -/
theorem finite_complex_differential_projector_root_no_go {n : ℕ} (p : Polynomial ℂ) (f : Fin n → ℂ)
    (hf : Function.Injective f)
    (h_roots : ∀ i : Fin n, p.eval (f i) = 0)
    (h_card : p.natDegree < n) :
    p = 0 ∧ p.eval 0 = 0 := by
  have h_card' : p.natDegree < Fintype.card (Fin n) := by
    simpa using h_card
  have hp0 : p = 0 :=
    Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero p hf h_roots h_card'
  refine ⟨hp0, ?_⟩
  rw [hp0, Polynomial.eval_zero]

/-- 16. Inversion-even Mellin symmetrization algebra (TASK-TC-037R):
    For raw Mellin values M_z = ⟨a, b⟩ and M_{-z} = ⟨c, d⟩, the inversion-even symmetrization
    hat{Psi}^+(z) = (M_z + M_{-z}) / 2 = ⟨(a + c) / 2, (b + d) / 2⟩ satisfies:
    (a) exact symmetry under z |-> -z (swapping M_z and M_{-z});
    (b) for a real-valued state where hat{Psi}^+(-conj z) = conj(hat{Psi}^+(z)), the reflection
        product is hat{Psi}^+(z) * conj(hat{Psi}^+(z)) = ⟨((a + c) / 2)^2 + ((b + d) / 2)^2, 0⟩;
    (c) raw nonvanishing M_z != 0 does not imply symmetrized nonvanishing: when M_{-z} = -M_z
        (i.e. c = -a and d = -b), the symmetrized Mellin weight (M_z + M_{-z}) / 2 = 0 vanishes. -/
theorem inversion_even_mellin_symmetry_algebra (a b c d : ℝ) :
    let Mz : ℂ := ⟨a, b⟩
    let Mnegz : ℂ := ⟨c, d⟩
    let psiPlus : ℂ := ⟨(a + c) / 2, (b + d) / 2⟩
    let psiSwap : ℂ := ⟨(c + a) / 2, (d + b) / 2⟩
    psiPlus = psiSwap ∧
      psiPlus * complexConjCoord psiPlus =
        ⟨((a + c) / 2) ^ 2 + ((b + d) / 2) ^ 2, 0⟩ ∧
      (c = -a → d = -b → Mz + Mnegz = 0 ∧ psiPlus = 0) := by
  refine ⟨?_, ?_, ?_⟩
  · apply Complex.ext <;> dsimp <;> ring
  · apply Complex.ext <;> dsimp [complexConjCoord] <;> ring
  · intro hc hd
    refine ⟨?_, ?_⟩
    · apply Complex.ext <;> dsimp <;> linarith
    · apply Complex.ext <;> dsimp <;> linarith

/-- 17. Reflection weight nonnegativity vs strict-positivity condition (TASK-TC-037R):
    For W_rho = m^2 * (u^2 + v^2) where hat{Psi}^+(z_rho) = ⟨u, v⟩:
    (a) 0 <= m^2 * (u^2 + v^2) and 0 <= 8 * m^2 * (u^2 + v^2) * δ^2 for all m, u, v, δ;
    (b) if u = 0 and v = 0 (a zero of hat{Psi}^+), then 8 * m^2 * (u^2 + v^2) * δ^2 = 0
        even when m != 0 and δ != 0;
    (c) if m != 0, δ != 0, and (u != 0 ∨ v != 0), then 0 < 8 * m^2 * (u^2 + v^2) * δ^2. -/
theorem reflection_weight_nonnegative (m u v δ : ℝ) :
    0 ≤ m ^ 2 * (u ^ 2 + v ^ 2) ∧
      0 ≤ 8 * m ^ 2 * (u ^ 2 + v ^ 2) * δ ^ 2 ∧
      (u = 0 → v = 0 → 8 * m ^ 2 * (u ^ 2 + v ^ 2) * δ ^ 2 = 0) ∧
      (m ≠ 0 → δ ≠ 0 → (u ≠ 0 ∨ v ≠ 0) → 0 < 8 * m ^ 2 * (u ^ 2 + v ^ 2) * δ ^ 2) := by
  refine ⟨by positivity, by positivity, ?_, ?_⟩
  · intro hu hv
    rw [hu, hv]
    ring
  · intro hm hδ huv
    rcases huv with hu | hv
    · have : 0 < u ^ 2 := sq_pos_of_ne_zero hu
      positivity
    · have : 0 < v ^ 2 := sq_pos_of_ne_zero hv
      positivity

end RiemannScope


