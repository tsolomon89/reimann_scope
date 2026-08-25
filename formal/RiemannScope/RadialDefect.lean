/-
RiemannScope.RadialDefect
Radial projection operator, defect divisor, and second-order orbit energy.
Reference: MATH_CONTRACT.md §36, §37, §38
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Algebra.BigOperators.Group.List
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace RiemannScope

/-- Radial projection operator sending s = 1/2 + δ + iγ to 1/2 + iγ on the critical line. -/
noncomputable def radialProjection (s : ℂ) : ℂ :=
  ⟨1 / 2, s.im⟩

/-- Radial projection projects critical-line points to themselves. -/
theorem radialProjection_on_line (γ : ℝ) :
    radialProjection ⟨1 / 2, γ⟩ = ⟨1 / 2, γ⟩ := by
  dsimp [radialProjection]

/-- Radial defect of a complex point under a test function h : ℂ → ℂ. -/
noncomputable def radialPointDefect (h : ℂ → ℂ) (s : ℂ) : ℂ :=
  h s - h (radialProjection s)

/-- Pure radial defect for a symmetry-complete quartet {1/2 ± δ ± iγ} with respect to h.
    For an even function h(t), the 4-point sum evaluates to:
    h(γ + iδ) + h(-γ - iδ) + h(γ - iδ) + h(-γ + iδ) - 2(h(γ) + h(-γ)). -/
noncomputable def pureRadialDefectQuartet (h : ℂ → ℂ) (δ γ : ℝ) : ℂ :=
  h ⟨γ, δ⟩ + h ⟨-γ, -δ⟩ + h ⟨γ, -δ⟩ + h ⟨-γ, δ⟩ - 2 * (h ⟨γ, 0⟩ + h ⟨-γ, 0⟩)

/-- When δ = 0, pure radial quartet defect vanishes identically. -/
theorem pureRadialDefectQuartet_zero_delta (h : ℂ → ℂ) (γ : ℝ) :
    pureRadialDefectQuartet h 0 γ = 0 := by
  dsimp [pureRadialDefectQuartet]
  have h1 : (⟨γ, (0:ℝ)⟩ : ℂ) = ⟨γ, 0⟩ := rfl
  have h2 : (⟨-γ, (-0:ℝ)⟩ : ℂ) = ⟨-γ, 0⟩ := by simp
  have h3 : (⟨γ, (-0:ℝ)⟩ : ℂ) = ⟨γ, 0⟩ := by simp
  have h4 : (⟨-γ, (0:ℝ)⟩ : ℂ) = ⟨-γ, 0⟩ := rfl
  rw [h1, h2, h3, h4]
  ring

/-- Second-order orbit variable u = δ^2 is non-negative for any real displacement δ. -/
theorem second_order_orbit_variable_nonneg (δ : ℝ) :
    0 ≤ δ ^ 2 := by
  exact sq_nonneg δ

/-- Involution operator sending centered coordinate z = δ + iγ to z^# = -δ + iγ. -/
noncomputable def involutionSharp (z : ℂ) : ℂ :=
  ⟨-z.re, z.im⟩

/-- Rational pairing kernel kappa_1(z, w) = 4*z*w / (z+w)^2 - 1. -/
noncomputable def kappa1 (z w : ℂ) : ℂ :=
  (4 * z * w) / (z + w) ^ 2 - 1

/-- Rational involution pairing algebraic reduction on real components:
    (4 * (δ^2 + γ^2)) / (4 * γ^2) - 1 = δ^2 / γ^2 for any γ ≠ 0. -/
theorem kappa1_pairing_algebraic (δ γ : ℝ) (hγ : γ ≠ 0) :
    (4 * (δ ^ 2 + γ ^ 2)) / (4 * γ ^ 2) - 1 = δ ^ 2 / γ ^ 2 := by
  have h4 : (4 : ℝ) ≠ 0 := by norm_num
  have hγ2 : γ ^ 2 ≠ 0 := pow_ne_zero 2 hγ
  have h4γ2 : 4 * γ ^ 2 ≠ 0 := mul_ne_zero h4 hγ2
  calc (4 * (δ ^ 2 + γ ^ 2)) / (4 * γ ^ 2) - 1
    _ = (4 * δ ^ 2 + 4 * γ ^ 2) / (4 * γ ^ 2) - 1 := by ring_nf
    _ = (4 * δ ^ 2) / (4 * γ ^ 2) + (4 * γ ^ 2) / (4 * γ ^ 2) - 1 := by rw [add_div]
    _ = (4 * δ ^ 2) / (4 * γ ^ 2) + 1 - 1 := by rw [div_self h4γ2]
    _ = (4 * δ ^ 2) / (4 * γ ^ 2) := by ring
    _ = (4 / 4) * (δ ^ 2 / γ ^ 2) := by ring
    _ = 1 * (δ ^ 2 / γ ^ 2) := by rw [div_self h4]
    _ = δ ^ 2 / γ ^ 2 := by ring

/-- Exact complex involution pairing theorem:
    For any centered zero z with z.im ≠ 0, kappa_1(z, z^#) evaluates in ℂ to ⟨z.re^2 / z.im^2, 0⟩. -/
theorem kappa1_involutionSharp_eq_of_im_ne_zero (z : ℂ) (hz : z.im ≠ 0) :
    kappa1 z (involutionSharp z) = ⟨z.re ^ 2 / z.im ^ 2, 0⟩ := by
  dsimp [kappa1, involutionSharp]
  have h4 : (-4 : ℝ) ≠ 0 := by norm_num
  have hzim2 : z.im ^ 2 ≠ 0 := pow_ne_zero 2 hz
  have hdenom_nz : -4 * z.im ^ 2 ≠ 0 := mul_ne_zero h4 hzim2
  have h_sum : z + (⟨-z.re, z.im⟩ : ℂ) = ⟨0, 2 * z.im⟩ := by
    apply Complex.ext
    · dsimp; ring
    · dsimp; ring
  have h_denom : ((z + (⟨-z.re, z.im⟩ : ℂ)) ^ 2) = Complex.ofReal (-4 * z.im ^ 2) := by
    rw [h_sum, sq]
    apply Complex.ext
    · dsimp [Complex.ofReal]
      ring
    · dsimp [Complex.ofReal]
      ring
  have h_num : 4 * z * (⟨-z.re, z.im⟩ : ℂ) = Complex.ofReal (-4 * (z.re ^ 2 + z.im ^ 2)) := by
    apply Complex.ext
    · dsimp [Complex.ofReal]
      ring
    · dsimp [Complex.ofReal]
      ring
  rw [h_denom, h_num]
  have h_div : Complex.ofReal (-4 * (z.re ^ 2 + z.im ^ 2)) / Complex.ofReal (-4 * z.im ^ 2) =
      Complex.ofReal ((-4 * (z.re ^ 2 + z.im ^ 2)) / (-4 * z.im ^ 2)) := by
    exact (Complex.ofReal_div _ _).symm
  rw [h_div]
  have h_one : (1 : ℂ) = Complex.ofReal 1 := rfl
  rw [h_one]
  have h_sub : Complex.ofReal ((-4 * (z.re ^ 2 + z.im ^ 2)) / (-4 * z.im ^ 2)) - Complex.ofReal 1 =
      Complex.ofReal (((-4 * (z.re ^ 2 + z.im ^ 2)) / (-4 * z.im ^ 2)) - 1) := by
    exact (Complex.ofReal_sub _ _).symm
  rw [h_sub]
  have h_alg : (-4 * (z.re ^ 2 + z.im ^ 2)) / (-4 * z.im ^ 2) - 1 = z.re ^ 2 / z.im ^ 2 := by
    calc (-4 * (z.re ^ 2 + z.im ^ 2)) / (-4 * z.im ^ 2) - 1
      _ = (-4 * (z.re ^ 2 + z.im ^ 2)) / (-4 * z.im ^ 2) - 1 := rfl
      _ = (-4 * z.re ^ 2 + -4 * z.im ^ 2) / (-4 * z.im ^ 2) - 1 := by ring_nf
      _ = (-4 * z.re ^ 2) / (-4 * z.im ^ 2) + (-4 * z.im ^ 2) / (-4 * z.im ^ 2) - 1 := by rw [add_div]
      _ = (-4 * z.re ^ 2) / (-4 * z.im ^ 2) + 1 - 1 := by rw [div_self hdenom_nz]
      _ = (-4 * z.re ^ 2) / (-4 * z.im ^ 2) := by ring
      _ = (-4 / -4) * (z.re ^ 2 / z.im ^ 2) := by ring
      _ = 1 * (z.re ^ 2 / z.im ^ 2) := by rw [div_self h4]
      _ = z.re ^ 2 / z.im ^ 2 := by ring
  rw [h_alg]
  rfl

/-- Non-negativity lemma for list sum of non-negative reals. -/
lemma list_sum_nonneg (l : List ℝ) (hl : ∀ x ∈ l, 0 ≤ x) : 0 ≤ l.sum := by
  induction l with
  | nil => simp
  | cons head tail ih =>
    simp only [List.sum_cons]
    have h_head : 0 ≤ head := hl head (List.Mem.head _)
    have h_tail : ∀ x ∈ tail, 0 ≤ x := fun x hx => hl x (List.Mem.tail _ hx)
    have h_tail_sum : 0 ≤ tail.sum := ih h_tail
    exact add_nonneg h_head h_tail_sum

/-- Arbitrary finite-family sum vanishing firewall:
    For any finite list of non-negative reals, their sum is zero if and only if every element is zero. -/
theorem list_sum_nonneg_eq_zero_iff (l : List ℝ) (hl : ∀ x ∈ l, 0 ≤ x) :
    l.sum = 0 ↔ ∀ x ∈ l, x = 0 := by
  induction l with
  | nil =>
    simp
  | cons head tail ih =>
    simp only [List.sum_cons, List.mem_cons, forall_eq_or_imp]
    have h_head : 0 ≤ head := hl head (List.Mem.head _)
    have h_tail : ∀ x ∈ tail, 0 ≤ x := fun x hx => hl x (List.Mem.tail _ hx)
    have ih' := ih h_tail
    have h_tail_sum_nonneg : 0 ≤ tail.sum := list_sum_nonneg tail h_tail
    constructor
    · intro h_sum
      have h_zeroes : head = 0 ∧ tail.sum = 0 := by
        constructor <;> linarith
      have h_tail_all_zero := ih'.mp h_zeroes.2
      exact ⟨h_zeroes.1, h_tail_all_zero⟩
    · intro ⟨h_head_zero, h_tail_zero⟩
      rw [h_head_zero]
      have h_tail_sum_zero : tail.sum = 0 := ih'.mpr h_tail_zero
      rw [h_tail_sum_zero, add_zero]

/-- Lower bound lemma for product of (1 + x) over non-negative reals. -/
lemma list_prod_one_plus_ge_one (l : List ℝ) (hl : ∀ x ∈ l, 0 ≤ x) : 1 ≤ (l.map (fun x => 1 + x)).prod := by
  induction l with
  | nil => simp
  | cons head tail ih =>
    simp only [List.map_cons, List.prod_cons]
    have h_head : 0 ≤ head := hl head (List.Mem.head _)
    have h_tail : ∀ x ∈ tail, 0 ≤ x := fun x hx => hl x (List.Mem.tail _ hx)
    have ih' := ih h_tail
    have h1head : 1 ≤ 1 + head := by linarith
    have h_prod_ge : 1 * 1 ≤ (1 + head) * (tail.map (fun x => 1 + x)).prod :=
      mul_le_mul h1head ih' (by linarith) (by linarith)
    rw [one_mul] at h_prod_ge
    exact h_prod_ge

/-- Arbitrary finite-family Fredholm determinant product firewall:
    For any finite list of non-negative reals, the product of (1 + x) is one if and only if every element is zero. -/
theorem list_prod_one_plus_nonneg_eq_one_iff (l : List ℝ) (hl : ∀ x ∈ l, 0 ≤ x) :
    (l.map (fun x => 1 + x)).prod = 1 ↔ ∀ x ∈ l, x = 0 := by
  induction l with
  | nil =>
    simp
  | cons head tail ih =>
    simp only [List.map_cons, List.prod_cons, List.mem_cons, forall_eq_or_imp]
    have h_head : 0 ≤ head := hl head (List.Mem.head _)
    have h_tail : ∀ x ∈ tail, 0 ≤ x := fun x hx => hl x (List.Mem.tail _ hx)
    have ih' := ih h_tail
    have h_tail_prod_ge_one : 1 ≤ (tail.map (fun x => 1 + x)).prod := list_prod_one_plus_ge_one tail h_tail
    constructor
    · intro h_prod
      have h1head : 0 ≤ 1 + head := by linarith
      have h_prod_ge : (1 + head) * 1 ≤ (1 + head) * (tail.map (fun x => 1 + x)).prod :=
        mul_le_mul_of_nonneg_left h_tail_prod_ge_one h1head
      rw [mul_one] at h_prod_ge
      rw [h_prod] at h_prod_ge
      have h_head_zero : head = 0 := by linarith
      rw [h_head_zero, add_zero, one_mul] at h_prod
      have h_tail_all_zero := ih'.mp h_prod
      exact ⟨h_head_zero, h_tail_all_zero⟩
    · intro ⟨h_head_zero, h_tail_zero⟩
      rw [h_head_zero, add_zero, one_mul]
      exact ih'.mpr h_tail_zero

/-- Finite non-negative sum vanishing firewall: r1 ≥ 0 ∧ r2 ≥ 0 ∧ r1 + r2 = 0 ⟹ r1 = 0 ∧ r2 = 0. -/
theorem nonneg_sum_two_eq_zero (r1 r2 : ℝ) (h1 : 0 ≤ r1) (h2 : 0 ≤ r2) (h : r1 + r2 = 0) :
    r1 = 0 ∧ r2 = 0 := by
  constructor <;> linarith

/-- Finite non-negative sum vanishing firewall for 3 terms. -/
theorem nonneg_sum_three_eq_zero (r1 r2 r3 : ℝ) (h1 : 0 ≤ r1) (h2 : 0 ≤ r2) (h3 : 0 ≤ r3) (h : r1 + r2 + r3 = 0) :
    r1 = 0 ∧ r2 = 0 ∧ r3 = 0 := by
  refine ⟨by linarith, by linarith, by linarith⟩

/-- Finite non-negative sum vanishing firewall for 4 terms. -/
theorem nonneg_sum_four_eq_zero (r1 r2 r3 r4 : ℝ) (h1 : 0 ≤ r1) (h2 : 0 ≤ r2) (h3 : 0 ≤ r3) (h4 : 0 ≤ r4) (h : r1 + r2 + r3 + r4 = 0) :
    r1 = 0 ∧ r2 = 0 ∧ r3 = 0 ∧ r4 = 0 := by
  refine ⟨by linarith, by linarith, by linarith, by linarith⟩

/-- Finite Fredholm determinant product firewall: (1 + r1)(1 + r2) = 1 ⟹ r1 = 0 ∧ r2 = 0 for non-negative r_i. -/
theorem nonneg_prod_two_eq_one (r1 r2 : ℝ) (h1 : 0 ≤ r1) (h2 : 0 ≤ r2) (h : (1 + r1) * (1 + r2) = 1) :
    r1 = 0 ∧ r2 = 0 := by
  have h_exp : (1 + r1) * (1 + r2) = 1 + r1 + r2 + r1 * r2 := by ring
  rw [h_exp] at h
  have h_sum : r1 + r2 + r1 * r2 = 0 := by linarith [h]
  have h_mul_nonneg : 0 ≤ r1 * r2 := mul_nonneg h1 h2
  have hr1 : r1 = 0 := by linarith [h1, h2, h_mul_nonneg, h_sum]
  have hr2 : r2 = 0 := by linarith [h1, h2, h_mul_nonneg, h_sum]
  exact ⟨hr1, hr2⟩

/-- Finite Fredholm determinant product firewall for 3 terms. -/
theorem nonneg_prod_three_eq_one (r1 r2 r3 : ℝ) (h1 : 0 ≤ r1) (h2 : 0 ≤ r2) (h3 : 0 ≤ r3) (h : (1 + r1) * (1 + r2) * (1 + r3) = 1) :
    r1 = 0 ∧ r2 = 0 ∧ r3 = 0 := by
  have h12_nonneg : 0 ≤ r1 + r2 + r1 * r2 := by
    have hm : 0 ≤ r1 * r2 := mul_nonneg h1 h2
    linarith
  have h_pair : (1 + (r1 + r2 + r1 * r2)) * (1 + r3) = 1 := by
    calc (1 + (r1 + r2 + r1 * r2)) * (1 + r3)
      _ = (1 + r1) * (1 + r2) * (1 + r3) := by ring
      _ = 1 := h
  have h_two := nonneg_prod_two_eq_one (r1 + r2 + r1 * r2) r3 h12_nonneg h3 h_pair
  have h12 := h_two.1
  have hr3 := h_two.2
  have h_exp : (1 + r1) * (1 + r2) = 1 := by
    calc (1 + r1) * (1 + r2)
      _ = 1 + (r1 + r2 + r1 * r2) := by ring
      _ = 1 + 0 := by rw [h12]
      _ = 1 := by ring
  have h_sub := nonneg_prod_two_eq_one r1 r2 h1 h2 h_exp
  exact ⟨h_sub.1, h_sub.2, hr3⟩

end RiemannScope
