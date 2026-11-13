/-
RiemannScope.DyadicPowerLiftPrimitiveCorrelation
TASK-TC-059: Dyadic Power-Lift Arithmetic and Primitive Coprime Correlations toward SUBGATE-TC-043A.

Formalizes in Lean 4 (with 0 sorry, 0 admit, and 0 custom axioms):
1. `window_integrability_and_kernel_scaling_tc059`:
   Concrete Mathlib `intervalIntegral` window pairing `⟨f, g⟩_u = ∫ X in u..(τ * u), f X * g X / X`,
   integrated Gaussian kernel `K_u(m, n)`, continuity and `IntervalIntegrable` on `[u, τ u]` for all
   `u > 0` (including `0 < u < 1`), nonnegativity, exact Gaussian term dilation
   `φ_{g r}(X) = g^{-1/2} φ_r(X / g)`, integrated kernel scaling `K_u(g r, g s) = g^{-1} K_{u / g}(r, s)`,
   and exact finite bilinear expansion of `⟨Q_{a,T}, Q_{b,T}⟩_u`.
2. `dyadic_power_lift_divisor_prime_power_and_stabilization_tc059`:
   Actual arithmetic dyadic power-step `a_j`, iterated Dirichlet convolution `b_J = a_0 * ⋯ * a_{J-1}`,
   prime-local telescoping polynomial identity `(1 - t) ∏_{0 ≤ j < J} (1 + t^{2^j}) = 1 - t^{2^J}`,
   exact power-divisor Möbius formula `b_J(n) = ∑_{r^{2^J} ∣ n} μ(n / r^{2^J})`, prime-power residue
   evaluation mod `2^J`, stabilization `b_J(n) = μ(n)` for `1 ≤ n < 2^{2^J}` with exact boundary witness
   `b_J(2^{2^J}) = 1 ≠ 0 = μ(2^{2^J})`, squarefree agreement `Squarefree n → b_J(n) = μ(n)`, stabilization
   depth `J_T = min {J ≥ 1 : 2^{2^J} > T}`, and `J = 2` prime-sign control characterization
   `b_{a,2}(p^2) = a(p)(a(p) + 1)`.
3. `gaussian_power_lift_increment_telescope_and_coherent_tail_tc059`:
   Exact finite Gaussian lift `Q_{b_J,T}(X) = ∑_{r^{d_J} ≤ T} r^{-d_J/2} Q_{μ,⌊T/r^{d_J}⌋}(X / r^{d_J})`
   (handling `T = 0, 1` and `X = 0`), increment support `Δ_J(n) = 0` for `1 ≤ n < 2^{2^J}` and
   `Δ_J(2^{2^J}) = -1`, exact non-square power-divisor representation of `Δ_J` and `Q_{Δ_J,T}`, finite
   telescoping `Q_{λ,T} = Q_{μ,T} - ∑_{1 ≤ J < J_T} Q_{Δ_J,T}`, full integrated window quadratic
   expansion retaining the `Q_μ` baseline and all cross/increment terms, and the stabilized-tail
   coherent Gram negative control (`J₁, J₂ ≥ J_T`).
4. `primitive_coprime_expansion_moebius_inversion_and_dyadic_block_tc059`:
   Exact ordered primitive-pair expansion of `E_T(Y)` over `gcd(r, s) = 1` and `1 ≤ g ≤ ⌊T / max(r, s)⌋`,
   reciprocal finite synthesis and Möbius inversion `E_T(Y) ↔ Π_T(Y)` on the `g = 1` primitive coprime
   correlation functional, exact dyadic magnitude-shell decomposition, separable window-pairing Möbius
   factorization on each primitive dyadic block `(j_r, j_s)`, and `m = n` coefficient-diagonal extraction
   and Möbius collapse to `K_Y(1, 1)`.
5. `parity_uniqueness_turn_chart_defect_and_log_saving_closure_tc059`:
   Finite parity-constraint uniqueness (`a(1) = 1` and `a(p m) + a(m) = 0` for `p m ≤ T` uniquely force
   `a(n) = λ(n)` on `1 ≤ n ≤ T`), auxiliary turn-chart symmetry `Re(q) = 1/4` and trivial zeros `q = -(m+1)`
   via Mathlib's `riemannZeta`, prime-local defect `D_p(δ) = (p^{δ/2} - p^{-δ/2})^2` with phase-plus-radial
   lower bound `|p^δ e^{iθ} - 1|^2 = p^δ (D_p(δ) + 4 sin^2(θ / 2)) ≥ p^δ D_p(δ)`, concrete window-integrated
   `E(Y) = D_tilde(Y) + S_comb(Y)` identity on `Y ≥ 2`, and the conditional logarithmic-saving diagonal
   closure transfer corollary via finite-horizon `normalizedScaleSupremum` absorption.
-/

import Mathlib.MeasureTheory.Integral.IntervalIntegral
import RiemannScope.Grade
import RiemannScope.TrivialZero
import RiemannScope.LiouvilleSquareDilation

open scoped ArithmeticFunction BigOperators Classical
open MeasureTheory intervalIntegral

namespace RiemannScope

namespace DyadicPowerLiftPrimitiveCorrelation

open RiemannScope.LiouvilleSquareDilation

/-! ### Section 1: Concrete Window-Integral Pairing, Kernel `K_u(m, n)`, Integrability, and Scaling -/

/-- Logarithmic window inner product `⟨f, g⟩_u := ∫_u^{τ u} f(X) g(X) dX / X` using canonical circle constant `τ`. -/
noncomputable def windowPairing (u : ℝ) (f g : ℝ → ℝ) : ℝ :=
  ∫ X in u..(RiemannScope.tau * u), f X * g X / X

/-- Window `L^2([u, τ u], dX / X)` norm squared `‖f‖_u^2 := ⟨f, f⟩_u`. -/
noncomputable def windowEnergyNormSq (u : ℝ) (f : ℝ → ℝ) : ℝ :=
  windowPairing u f f

/-- Integrated Gaussian energy kernel `K_u(m, n) := ∫_u^{τ u} φ_m(X) φ_n(X) dX / X` defined for all `u > 0`
    (including `0 < u < 1`). -/
noncomputable def windowKernelK (u : ℝ) (m n : ℕ) : ℝ :=
  windowPairing u (gaussianTermPhi m) (gaussianTermPhi n)

/-- Actual window-integrated finite energy `E_{a,T}(Y) := ‖Q_{a,T}‖_Y^2 = ∫_Y^{τ Y} Q_{a,T}(X)^2 dX / X`. -/
noncomputable def actualWindowEnergyE (a : ℕ → ℝ) (T : ℕ) (Y : ℝ) : ℝ :=
  windowEnergyNormSq Y (finiteQGeneral a T)

/-- Canonical Liouville window energy `E(Y) := ‖Q_{λ, T(Y)}‖_Y^2` at `T(Y) = ⌈Y^{5/4}⌉`. -/
noncomputable def canonicalLiouvilleEnergyE (Y : ℝ) : ℝ :=
  actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) (canonicalCutoffT Y) Y

private theorem tau_gt_one_aux : (1 : ℝ) < RiemannScope.tau := by
  dsimp [RiemannScope.tau]
  linarith [Real.two_le_pi]

private theorem uIcc_subset_Ioi_of_pos_aux {u : ℝ} (hu : 0 < u) :
    ∀ X ∈ Set.uIcc u (RiemannScope.tau * u), 0 < X := by
  have htau : (1 : ℝ) < RiemannScope.tau := tau_gt_one_aux
  have hle : u ≤ RiemannScope.tau * u := by nlinarith
  intro X hX
  rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX
  linarith

private theorem continuousOn_gaussianTermPhi_Ici_aux (m : ℕ) :
    ContinuousOn (gaussianTermPhi m) (Set.Ici 0) := by
  unfold gaussianTermPhi
  have h_rpow : ContinuousOn (fun X : ℝ => X ^ (5 / 2 : ℝ)) (Set.Ici 0) := by
    apply ContinuousOn.rpow_const continuousOn_id
    intro X _
    right
    norm_num
  have h_exp : Continuous (fun X : ℝ => (((m : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (m : ℝ) ^ 2))) := by
    continuity
  exact h_rpow.mul h_exp.continuousOn

private theorem continuousOn_gaussianTermPhi_uIcc_aux {u : ℝ} (hu : 0 < u) (m : ℕ) :
    ContinuousOn (gaussianTermPhi m) (Set.uIcc u (RiemannScope.tau * u)) := by
  apply (continuousOn_gaussianTermPhi_Ici_aux m).mono
  intro X hX
  exact le_of_lt (uIcc_subset_Ioi_of_pos_aux hu X hX)

private theorem continuousOn_finiteQGeneral_uIcc_aux {u : ℝ} (hu : 0 < u) (a : ℕ → ℝ) (T : ℕ) :
    ContinuousOn (finiteQGeneral a T) (Set.uIcc u (RiemannScope.tau * u)) := by
  unfold finiteQGeneral
  apply continuousOn_finset_sum
  intro n _
  exact continuousOn_const.mul (continuousOn_gaussianTermPhi_uIcc_aux hu n)

private theorem intervalIntegrable_window_of_continuousOn_aux
    {u : ℝ} (hu : 0 < u) {f g : ℝ → ℝ}
    (hf : ContinuousOn f (Set.uIcc u (RiemannScope.tau * u)))
    (hg : ContinuousOn g (Set.uIcc u (RiemannScope.tau * u))) :
    IntervalIntegrable (fun X => f X * g X / X) volume u (RiemannScope.tau * u) := by
  apply ContinuousOn.intervalIntegrable
  apply ContinuousOn.div (hf.mul hg) continuousOn_id
  intro X hX
  exact ne_of_gt (uIcc_subset_Ioi_of_pos_aux hu X hX)

private theorem gaussianTermPhi_mul_scale_aux {g : ℕ} (hg : 0 < g) (r : ℕ) {X : ℝ} (hX : 0 ≤ X) :
    gaussianTermPhi (g * r) X =
      (1 / Real.sqrt (g : ℝ)) * gaussianTermPhi r (X / (g : ℝ)) := by
  unfold gaussianTermPhi
  have hg_pos : (0 : ℝ) < (g : ℝ) := Nat.cast_pos.mpr hg
  have hg_nn : (0 : ℝ) ≤ (g : ℝ) := le_of_lt hg_pos
  have hrpow_div : (X / (g : ℝ)) ^ (5 / 2 : ℝ) = X ^ (5 / 2 : ℝ) / (g : ℝ) ^ (5 / 2 : ℝ) :=
    Real.div_rpow hX hg_nn (5 / 2 : ℝ)
  have hsqrt_mul_rpow : Real.sqrt (g : ℝ) * (g : ℝ) ^ (5 / 2 : ℝ) = (g : ℝ) ^ 3 := by
    rw [Real.sqrt_eq_rpow, ← Real.rpow_add hg_pos]
    have hexp : (1 / 2 : ℝ) + (5 / 2 : ℝ) = ((3 : ℕ) : ℝ) := by norm_num
    rw [hexp, Real.rpow_natCast]
  have hexp_arg : -((X / (g : ℝ)) ^ 2) / (r : ℝ) ^ 2 = -(X ^ 2) / ((g * r : ℕ) : ℝ) ^ 2 := by
    push_cast
    by_cases hr : (r : ℝ) = 0
    · simp [hr]
    · rw [mul_pow, div_pow, neg_div, div_div, neg_div]
  rw [hrpow_div, hexp_arg]
  push_cast
  by_cases hr : (r : ℝ) = 0
  · simp [hr]
  · symm
    calc
      (1 / Real.sqrt (g : ℝ)) *
          (X ^ (5 / 2 : ℝ) / (g : ℝ) ^ (5 / 2 : ℝ) *
            (((r : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / ((g : ℝ) * (r : ℝ)) ^ 2)))
        = X ^ (5 / 2 : ℝ) *
            (((Real.sqrt (g : ℝ) * (g : ℝ) ^ (5 / 2 : ℝ)) * (r : ℝ) ^ 3)⁻¹ *
              Real.exp (-(X ^ 2) / ((g : ℝ) * (r : ℝ)) ^ 2)) := by
            rw [mul_inv_rev, mul_inv_rev]
            ring
      _ = X ^ (5 / 2 : ℝ) *
            ((((g : ℝ) * (r : ℝ)) ^ 3)⁻¹ *
              Real.exp (-(X ^ 2) / ((g : ℝ) * (r : ℝ)) ^ 2)) := by
            rw [hsqrt_mul_rpow]
            ring

private theorem intervalIntegrable_finset_sum_fn_aux {α : Type*} (s : Finset α)
    {a b : ℝ} {f : α → ℝ → ℝ}
    (hf : ∀ i ∈ s, IntervalIntegrable (f i) volume a b) :
    IntervalIntegrable (fun X => ∑ i ∈ s, f i X) volume a b := by
  have h_eq : (fun X => ∑ i ∈ s, f i X) = (∑ i ∈ s, f i) := by
    ext X
    simp [Finset.sum_apply]
  rw [h_eq]
  exact IntervalIntegrable.sum s hf

/-- **Theorem 1 (`TASK-TC-059` §1 & §3, Concrete Window Integrability, Kernel Scaling, and Finite Bilinear Expansion)**:
    *Formal scope (`CONCRETE_ANALYTIC_IN_LEAN`)*:
    For every window base `u > 0` (including `0 < u < 1`):
    1. Every continuous pair `f, g` on `Set.uIcc u (τ u)` (and in particular every `gaussianTermPhi m, gaussianTermPhi n`)
       is `IntervalIntegrable` against `dX / X` on `[u, τ u]`;
    2. `windowKernelK u m n = windowKernelK u n m` and `0 ≤ windowKernelK u m n`;
    3. Exact Gaussian dilation: for `g > 0`, `r : ℕ`, and `X ≥ 0`,
       `gaussianTermPhi (g * r) X = g^{-1/2} * gaussianTermPhi r (X / g)`;
    4. Exact integrated kernel scaling: for `g > 0` and `r, s : ℕ`,
       `windowKernelK u (g * r) (g * s) = (1 / g) * windowKernelK (u / g) r s`;
    5. Exact finite bilinear window expansion: for `T : ℕ` and `a, b : ℕ → ℝ`,
       `windowPairing u (finiteQGeneral a T) (finiteQGeneral b T) = ∑_{1 ≤ m ≤ T} ∑_{1 ≤ n ≤ T} a(m) b(n) K_u(m, n)`. -/
theorem window_integrability_and_kernel_scaling_tc059
    {u : ℝ} (hu : 0 < u) :
    ((∀ {f g : ℝ → ℝ},
        ContinuousOn f (Set.uIcc u (RiemannScope.tau * u)) →
        ContinuousOn g (Set.uIcc u (RiemannScope.tau * u)) →
        IntervalIntegrable (fun X => f X * g X / X) volume u (RiemannScope.tau * u)) ∧
      (∀ m n : ℕ,
        IntervalIntegrable (fun X => gaussianTermPhi m X * gaussianTermPhi n X / X)
          volume u (RiemannScope.tau * u))) ∧
    (∀ m n : ℕ, windowKernelK u m n = windowKernelK u n m ∧ 0 ≤ windowKernelK u m n) ∧
    (∀ {g : ℕ}, 0 < g → ∀ (r : ℕ) {X : ℝ}, 0 ≤ X →
      gaussianTermPhi (g * r) X =
        (1 / Real.sqrt (g : ℝ)) * gaussianTermPhi r (X / (g : ℝ))) ∧
    (∀ {g : ℕ}, 0 < g → ∀ r s : ℕ,
      windowKernelK u (g * r) (g * s) =
        (1 / (g : ℝ)) * windowKernelK (u / (g : ℝ)) r s) ∧
    (∀ (T : ℕ) (a b : ℕ → ℝ),
      windowPairing u (finiteQGeneral a T) (finiteQGeneral b T) =
        ∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T, a m * b n * windowKernelK u m n) := by
  have htau : (1 : ℝ) < RiemannScope.tau := tau_gt_one_aux
  have hle_u : u ≤ RiemannScope.tau * u := by nlinarith
  refine ⟨⟨fun hf hg => intervalIntegrable_window_of_continuousOn_aux hu hf hg, ?_⟩, ?_, ?_, ?_, ?_⟩
  · intro m n
    exact intervalIntegrable_window_of_continuousOn_aux hu
      (continuousOn_gaussianTermPhi_uIcc_aux hu m)
      (continuousOn_gaussianTermPhi_uIcc_aux hu n)
  · intro m n
    constructor
    · unfold windowKernelK windowPairing
      congr 1
      ext X
      ring
    · unfold windowKernelK windowPairing
      apply intervalIntegral.integral_nonneg hle_u
      intro X hX
      rw [Set.mem_Icc] at hX
      have hX_pos : 0 < X := by linarith
      have hphi_nn : ∀ k : ℕ, 0 ≤ gaussianTermPhi k X := by
        intro k
        unfold gaussianTermPhi
        positivity
      exact div_nonneg (mul_nonneg (hphi_nn m) (hphi_nn n)) (le_of_lt hX_pos)
  · intro g hg r X hX
    exact gaussianTermPhi_mul_scale_aux hg r hX
  · intro g hg r s
    have hg_pos : (0 : ℝ) < (g : ℝ) := Nat.cast_pos.mpr hg
    have hg_ne : (g : ℝ) ≠ 0 := ne_of_gt hg_pos
    have hsqrt_sq : Real.sqrt (g : ℝ) * Real.sqrt (g : ℝ) = (g : ℝ) :=
      Real.mul_self_sqrt (le_of_lt hg_pos)
    unfold windowKernelK windowPairing
    have h_congr :
        ∫ X in u..(RiemannScope.tau * u),
          gaussianTermPhi (g * r) X * gaussianTermPhi (g * s) X / X =
        ∫ X in u..(RiemannScope.tau * u),
          ((1 / ((g : ℝ) ^ 2)) *
            ((fun w => gaussianTermPhi r w * gaussianTermPhi s w / w) (X / (g : ℝ)))) := by
      apply intervalIntegral.integral_congr
      intro X hX
      dsimp only
      have hX_pos : 0 < X := uIcc_subset_Ioi_of_pos_aux hu X hX
      have hX_ne : X ≠ 0 := ne_of_gt hX_pos
      rw [gaussianTermPhi_mul_scale_aux hg r (le_of_lt hX_pos),
        gaussianTermPhi_mul_scale_aux hg s (le_of_lt hX_pos)]
      calc
        ((1 / Real.sqrt (g : ℝ)) * gaussianTermPhi r (X / (g : ℝ))) *
            ((1 / Real.sqrt (g : ℝ)) * gaussianTermPhi s (X / (g : ℝ))) / X
          = (1 / (Real.sqrt (g : ℝ) * Real.sqrt (g : ℝ))) *
              gaussianTermPhi r (X / (g : ℝ)) * gaussianTermPhi s (X / (g : ℝ)) / X := by ring
        _ = (1 / (g : ℝ)) *
              gaussianTermPhi r (X / (g : ℝ)) * gaussianTermPhi s (X / (g : ℝ)) / X := by
              rw [hsqrt_sq]
        _ = (1 / (g : ℝ) ^ 2) *
              (gaussianTermPhi r (X / (g : ℝ)) * gaussianTermPhi s (X / (g : ℝ)) / (X / (g : ℝ))) := by
              field_simp [hg_ne, hX_ne]
              ring
    rw [h_congr, intervalIntegral.integral_const_mul,
      intervalIntegral.integral_comp_div (fun w => gaussianTermPhi r w * gaussianTermPhi s w / w) hg_ne]
    have h_upper : RiemannScope.tau * u / (g : ℝ) = RiemannScope.tau * (u / (g : ℝ)) :=
      mul_div_assoc RiemannScope.tau u (g : ℝ)
    rw [h_upper, smul_eq_mul, ← mul_assoc]
    congr 1
    field_simp [hg_ne]
    ring
  · intro T a b
    unfold windowPairing finiteQGeneral
    have h_int_mn : ∀ m n : ℕ,
        IntervalIntegrable
          (fun X => (a m * b n) * (gaussianTermPhi m X * gaussianTermPhi n X / X))
          volume u (RiemannScope.tau * u) :=
      fun m n =>
        (intervalIntegrable_window_of_continuousOn_aux hu
          (continuousOn_gaussianTermPhi_uIcc_aux hu m)
          (continuousOn_gaussianTermPhi_uIcc_aux hu n)).const_mul (a m * b n)
    have h_expand :
        (fun X => (∑ m ∈ Finset.Icc 1 T, a m * gaussianTermPhi m X) *
          (∑ n ∈ Finset.Icc 1 T, b n * gaussianTermPhi n X) / X) =
        (fun X => ∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T,
          (a m * b n) * (gaussianTermPhi m X * gaussianTermPhi n X / X)) := by
      ext X
      rw [Finset.sum_mul]
      simp_rw [Finset.mul_sum, Finset.sum_div]
      apply Finset.sum_congr rfl
      intro m _
      apply Finset.sum_congr rfl
      intro n _
      ring
    have h_inner : ∀ m : ℕ,
        IntervalIntegrable
          (fun X => ∑ n ∈ Finset.Icc 1 T,
            (a m * b n) * (gaussianTermPhi m X * gaussianTermPhi n X / X))
          volume u (RiemannScope.tau * u) :=
      fun m => intervalIntegrable_finset_sum_fn_aux (Finset.Icc 1 T) (fun n _ => h_int_mn m n)
    rw [h_expand,
      intervalIntegral.integral_finset_sum (fun m _ => h_inner m)]
    apply Finset.sum_congr rfl
    intro m _
    rw [intervalIntegral.integral_finset_sum (fun n _ => h_int_mn m n)]
    apply Finset.sum_congr rfl
    intro n _
    rw [intervalIntegral.integral_const_mul]
    rfl

/-! ### Section 2: Exact Finite Dyadic Power-Lift Arithmetic, Stabilization, and Control Separation -/

/-- General `d`-th power lift of an `ArithmeticFunction ℤ`: maps `m^d ↦ f(m)` for `m ≥ 1` and `0` otherwise. -/
def powerLiftArith (f : ArithmeticFunction ℤ) (d : ℕ) : ArithmeticFunction ℤ :=
  ⟨fun n => if n = 0 then 0 else ∑ m ∈ (Nat.divisors n).filter (fun m => m ^ d = n), f m, by simp⟩

/-- Dyadic step arithmetic function `a_j(n) = a(m)` if `n = m^{2^j}` and `0` otherwise (`j ≥ 0`). -/
def dyadicPowerStepArith (a : ArithmeticFunction ℤ) (j : ℕ) : ArithmeticFunction ℤ :=
  powerLiftArith a (2 ^ j)

/-- Canonical Liouville dyadic step `a_j(n) = λ(m)` if `n = m^{2^j}` and `0` otherwise. -/
def liouvilleDyadicStepArith (j : ℕ) : ArithmeticFunction ℤ :=
  dyadicPowerStepArith liouvilleArith j

/-- Iterated Dirichlet convolution `b_{a,J} = a_0 * a_1 * ⋯ * a_{J-1}` (`b_{a,0} = δ_1`, `b_{a,1} = a_0`). -/
def dyadicPowerLiftIterConv (a : ArithmeticFunction ℤ) : ℕ → ArithmeticFunction ℤ
  | 0 => 1
  | J + 1 => dyadicPowerLiftIterConv a J * dyadicPowerStepArith a J

/-- Canonical Liouville dyadic power-lift `b_J = a_0 * a_1 * ⋯ * a_{J-1}` (`J ≥ 1`, `d_J = 2^J`). -/
def liouvillePowerLiftB (J : ℕ) : ArithmeticFunction ℤ :=
  dyadicPowerLiftIterConv liouvilleArith J

/-- Finite set of positive integers `r` whose `d`-th power divides `n`: `{1 ≤ r ≤ n : r^d ∣ n}`. -/
def powerDivisors (d n : ℕ) : Finset ℕ :=
  (Finset.Icc 1 n).filter (fun r => r ^ d ∣ n)

/-- Power-divisor Möbius sum `∑_{r^d ∣ n} μ(n / r^d)`. -/
def moebiusPowerDivisorSum (d n : ℕ) : ℤ :=
  ∑ r ∈ powerDivisors d n, ArithmeticFunction.moebius (n / r ^ d)

/-- `d`-th power indicator `ArithmeticFunction ℤ`: `1` if `n = r^d` for some `r ≥ 1`, else `0`. -/
def powerIndicatorArith (d : ℕ) : ArithmeticFunction ℤ :=
  powerLiftArith (ArithmeticFunction.zeta : ArithmeticFunction ℤ) d

private theorem exists_stabilization_depth_aux (T : ℕ) : ∃ J : ℕ, 1 ≤ J ∧ T < 2 ^ (2 ^ J) := by
  refine ⟨T + 1, by omega, ?_⟩
  have h1 : T + 1 < 2 ^ (T + 1) := Nat.lt_pow_self (by norm_num : 1 < 2) (T + 1)
  have h2 : T + 1 ≤ 2 ^ (2 ^ (T + 1)) := by
    have h3 : 2 ^ (T + 1) ≤ 2 ^ (2 ^ (T + 1)) :=
      Nat.pow_le_pow_right (by norm_num : 0 < 2) (le_of_lt h1)
    omega
  omega

/-- Least stabilization depth `J_T := min {J ≥ 1 : 2^{2^J} > T}`. -/
noncomputable def stabilizationDepthJ (T : ℕ) : ℕ :=
  Nat.find (exists_stabilization_depth_aux T)

/-- Power-lift increment `Δ_J(n) := b_{J+1}(n) - b_J(n)`. -/
def powerLiftIncrementDelta (J n : ℕ) : ℤ :=
  liouvillePowerLiftB (J + 1) n - liouvillePowerLiftB J n

private theorem pow_eq_inj_pos_aux {d : ℕ} (hd : 0 < d) {x y : ℕ} (_hx : 0 < x) (_hy : 0 < y)
    (heq : x ^ d = y ^ d) : x = y := by
  rcases lt_trichotomy x y with hlt | rfl | hgt
  · exfalso
    have : x ^ d < y ^ d := Nat.pow_lt_pow_left hlt (by omega)
    omega
  · rfl
  · exfalso
    have : y ^ d < x ^ d := Nat.pow_lt_pow_left hgt (by omega)
    omega

private theorem powerLiftArith_apply_pow_aux (f : ArithmeticFunction ℤ) {d m : ℕ} (hd : 0 < d) (hm : 0 < m) :
    powerLiftArith f d (m ^ d) = f m := by
  have hmd_pos : 0 < m ^ d := Nat.pow_pos hm
  have hmd_ne : m ^ d ≠ 0 := by omega
  have hm_dvd : m ∣ m ^ d := dvd_pow_self m (by omega)
  have h_filt : (Nat.divisors (m ^ d)).filter (fun x => x ^ d = m ^ d) = {m} := by
    ext x
    simp only [Finset.mem_filter, Nat.mem_divisors, Finset.mem_singleton]
    constructor
    · rintro ⟨⟨hxdvd, _⟩, hxpow⟩
      have hx_pos : 0 < x := Nat.pos_of_dvd_of_pos hxdvd hmd_pos
      exact pow_eq_inj_pos_aux hd hx_pos hm hxpow
    · rintro rfl
      exact ⟨⟨hm_dvd, hmd_ne⟩, rfl⟩
  simp [powerLiftArith, hmd_ne, h_filt]

private theorem powerLiftArith_apply_not_pow_aux (f : ArithmeticFunction ℤ) {d n : ℕ}
    (hnot : ∀ m : ℕ, 0 < m → m ^ d ≠ n) :
    powerLiftArith f d n = 0 := by
  by_cases hn : n = 0
  · simp [powerLiftArith, hn]
  · have hn_pos : 0 < n := Nat.pos_of_ne_zero hn
    simp only [powerLiftArith, ArithmeticFunction.coe_mk, hn, ↓reduceIte]
    apply Finset.sum_eq_zero
    intro m hm
    rw [Finset.mem_filter, Nat.mem_divisors] at hm
    have hm_pos : 0 < m := Nat.pos_of_dvd_of_pos hm.1.1 hn_pos
    exact False.elim (hnot m hm_pos hm.2)

private theorem powerLiftArith_one_exp_eq_self_aux (f : ArithmeticFunction ℤ) :
    powerLiftArith f 1 = f := by
  ext n
  by_cases hn : n = 0
  · subst hn; simp [powerLiftArith]
  · have h1 := powerLiftArith_apply_pow_aux f (by omega : 0 < 1) (Nat.pos_of_ne_zero hn)
    simpa using h1

private theorem powerLiftArith_mul_hom_aux (f g : ArithmeticFunction ℤ) {d : ℕ} (hd : 0 < d) :
    powerLiftArith f d * powerLiftArith g d = powerLiftArith (f * g) d := by
  ext n
  by_cases hn : n = 0
  · subst hn; simp [powerLiftArith]
  · rw [ArithmeticFunction.mul_apply]
    by_cases hex : ∃ z : ℕ, 0 < z ∧ z ^ d = n
    · obtain ⟨z, hz_pos, rfl⟩ := hex
      rw [powerLiftArith_apply_pow_aux (f * g) hd hz_pos, ArithmeticFunction.mul_apply]
      let S_pow := (Nat.divisorsAntidiagonal (z ^ d)).filter
        (fun uv => (∃ x, 0 < x ∧ x ^ d = uv.1) ∧ (∃ y, 0 < y ∧ y ^ d = uv.2))
      have h_trim :
          ∑ uv ∈ Nat.divisorsAntidiagonal (z ^ d),
            powerLiftArith f d uv.1 * powerLiftArith g d uv.2 =
          ∑ uv ∈ S_pow, powerLiftArith f d uv.1 * powerLiftArith g d uv.2 := by
        rw [← Finset.sum_subset
          (Finset.filter_subset
            (fun uv : ℕ × ℕ => (∃ x, 0 < x ∧ x ^ d = uv.1) ∧ (∃ y, 0 < y ∧ y ^ d = uv.2))
            (Nat.divisorsAntidiagonal (z ^ d)))]
        intro uv huv hnot
        rw [Finset.mem_filter] at hnot
        push_neg at hnot
        have hn1 : ¬ (∃ x, 0 < x ∧ x ^ d = uv.1) ∨ ¬ (∃ y, 0 < y ∧ y ^ d = uv.2) := by
          by_cases h1 : ∃ x, 0 < x ∧ x ^ d = uv.1
          · exact Or.inr (fun ⟨y, hy, hyu⟩ => hnot huv h1 y hy hyu)
          · exact Or.inl h1
        rcases hn1 with h1 | h2
        · push_neg at h1
          rw [powerLiftArith_apply_not_pow_aux f h1, zero_mul]
        · push_neg at h2
          rw [powerLiftArith_apply_not_pow_aux g h2, mul_zero]
      rw [h_trim]
      symm
      apply Finset.sum_bij (fun xy _ => (xy.1 ^ d, xy.2 ^ d))
      · rintro ⟨x, y⟩ hxy
        rw [Nat.mem_divisorsAntidiagonal] at hxy
        have hx_pos : 0 < x := Nat.pos_of_ne_zero (fun hx0 => by simp [hx0] at hxy; omega)
        have hy_pos : 0 < y := Nat.pos_of_ne_zero (fun hy0 => by simp [hy0] at hxy; omega)
        refine Finset.mem_filter.mpr ⟨?_, ⟨x, hx_pos, rfl⟩, ⟨y, hy_pos, rfl⟩⟩
        rw [Nat.mem_divisorsAntidiagonal]
        refine ⟨?_, ne_of_gt (Nat.pow_pos hz_pos)⟩
        rw [← mul_pow, hxy.1]
      · rintro ⟨x1, y1⟩ h1 ⟨x2, y2⟩ h2 heq
        rw [Nat.mem_divisorsAntidiagonal] at h1 h2
        have hx1 : 0 < x1 := Nat.pos_of_ne_zero (fun h0 => by simp [h0] at h1; omega)
        have hy1 : 0 < y1 := Nat.pos_of_ne_zero (fun h0 => by simp [h0] at h1; omega)
        have hx2 : 0 < x2 := Nat.pos_of_ne_zero (fun h0 => by simp [h0] at h2; omega)
        have hy2 : 0 < y2 := Nat.pos_of_ne_zero (fun h0 => by simp [h0] at h2; omega)
        injection heq with heq1 heq2
        exact Prod.ext (pow_eq_inj_pos_aux hd hx1 hx2 heq1) (pow_eq_inj_pos_aux hd hy1 hy2 heq2)
      · rintro ⟨u, v⟩ huv
        rw [Finset.mem_filter, Nat.mem_divisorsAntidiagonal] at huv
        obtain ⟨⟨huv_mul, _⟩, ⟨x, hx_pos, rfl⟩, ⟨y, hy_pos, rfl⟩⟩ := huv
        have hxy_eq : x * y = z := by
          apply pow_eq_inj_pos_aux hd (Nat.mul_pos hx_pos hy_pos) hz_pos
          rw [mul_pow, huv_mul]
        refine ⟨(x, y), ?_, rfl⟩
        rw [Nat.mem_divisorsAntidiagonal]
        exact ⟨hxy_eq, by omega⟩
      · rintro ⟨x, y⟩ hxy
        rw [Nat.mem_divisorsAntidiagonal] at hxy
        have hx_pos : 0 < x := Nat.pos_of_ne_zero (fun h0 => by simp [h0] at hxy; omega)
        have hy_pos : 0 < y := Nat.pos_of_ne_zero (fun h0 => by simp [h0] at hxy; omega)
        rw [powerLiftArith_apply_pow_aux f hd hx_pos, powerLiftArith_apply_pow_aux g hd hy_pos]
    · push_neg at hex
      rw [powerLiftArith_apply_not_pow_aux (f * g) hex]
      apply Finset.sum_eq_zero
      rintro ⟨u, v⟩ huv
      rw [Nat.mem_divisorsAntidiagonal] at huv
      by_cases hu_pow : ∃ x, 0 < x ∧ x ^ d = u
      · by_cases hv_pow : ∃ y, 0 < y ∧ y ^ d = v
        · obtain ⟨x, hx_pos, rfl⟩ := hu_pow
          obtain ⟨y, hy_pos, rfl⟩ := hv_pow
          exfalso
          apply hex (x * y) (Nat.mul_pos hx_pos hy_pos)
          rw [mul_pow, huv.1]
        · push_neg at hv_pow
          rw [powerLiftArith_apply_not_pow_aux g hv_pow, mul_zero]
      · push_neg at hu_pow
        rw [powerLiftArith_apply_not_pow_aux f hu_pow, zero_mul]

private theorem powerLiftArith_comp_aux (f : ArithmeticFunction ℤ) {d1 d2 : ℕ} (hd1 : 0 < d1) (hd2 : 0 < d2) :
    powerLiftArith (powerLiftArith f d1) d2 = powerLiftArith f (d1 * d2) := by
  ext n
  by_cases hn : n = 0
  · subst hn; simp [powerLiftArith]
  · by_cases hex : ∃ m : ℕ, 0 < m ∧ m ^ (d1 * d2) = n
    · obtain ⟨m, hm_pos, rfl⟩ := hex
      rw [powerLiftArith_apply_pow_aux f (Nat.mul_pos hd1 hd2) hm_pos]
      have hpow_mul : m ^ (d1 * d2) = (m ^ d1) ^ d2 := pow_mul m d1 d2
      rw [hpow_mul, powerLiftArith_apply_pow_aux _ hd2 (Nat.pow_pos hm_pos),
        powerLiftArith_apply_pow_aux f hd1 hm_pos]
    · push_neg at hex
      rw [powerLiftArith_apply_not_pow_aux f hex]
      by_cases hex2 : ∃ y : ℕ, 0 < y ∧ y ^ d2 = n
      · obtain ⟨y, hy_pos, rfl⟩ := hex2
        rw [powerLiftArith_apply_pow_aux _ hd2 hy_pos]
        apply powerLiftArith_apply_not_pow_aux f
        intro m hm hmy
        apply hex m hm
        rw [pow_mul, hmy]
      · push_neg at hex2
        exact powerLiftArith_apply_not_pow_aux _ hex2

private theorem moebius_mul_powerIndicator_apply_aux {d n : ℕ} (hd : 0 < d) (hn : 0 < n) :
    (ArithmeticFunction.moebius * powerIndicatorArith d) n = moebiusPowerDivisorSum d n := by
  rw [ArithmeticFunction.mul_apply]
  unfold moebiusPowerDivisorSum
  let S_ind := (Nat.divisorsAntidiagonal n).filter (fun uv => ∃ r, 0 < r ∧ r ^ d = uv.2)
  have h_trim :
      ∑ uv ∈ Nat.divisorsAntidiagonal n,
        ArithmeticFunction.moebius uv.1 * powerIndicatorArith d uv.2 =
      ∑ uv ∈ S_ind, ArithmeticFunction.moebius uv.1 * powerIndicatorArith d uv.2 := by
    rw [← Finset.sum_subset
      (Finset.filter_subset (fun uv : ℕ × ℕ => ∃ r, 0 < r ∧ r ^ d = uv.2) (Nat.divisorsAntidiagonal n))]
    intro uv _ hnot
    rw [Finset.mem_filter] at hnot
    have hnot2 : ∀ r : ℕ, 0 < r → r ^ d ≠ uv.2 := by
      intro r hr heq
      exact hnot ⟨by assumption, ⟨r, hr, heq⟩⟩
    rw [powerIndicatorArith, powerLiftArith_apply_not_pow_aux _ hnot2, mul_zero]
  rw [h_trim]
  symm
  apply Finset.sum_bij (fun r _ => (n / r ^ d, r ^ d))
  · intro r hr
    rw [powerDivisors, Finset.mem_filter, Finset.mem_Icc] at hr
    refine Finset.mem_filter.mpr ⟨?_, ⟨r, hr.1.1, rfl⟩⟩
    rw [Nat.mem_divisorsAntidiagonal]
    exact ⟨Nat.div_mul_cancel hr.2, by omega⟩
  · intro r1 hr1 r2 hr2 heq
    rw [powerDivisors, Finset.mem_filter, Finset.mem_Icc] at hr1 hr2
    injection heq with _ heq2
    exact pow_eq_inj_pos_aux hd hr1.1.1 hr2.1.1 heq2
  · rintro ⟨u, v⟩ huv
    rw [Finset.mem_filter, Nat.mem_divisorsAntidiagonal] at huv
    obtain ⟨⟨huv_mul, _⟩, ⟨r, hr_pos, rfl⟩⟩ := huv
    have hrd_pos : 0 < r ^ d := Nat.pow_pos hr_pos
    have hu_eq : u = n / r ^ d := by
      rw [← huv_mul, Nat.mul_div_cancel u hrd_pos]
    have hr_le_n : r ≤ n := by
      have hrd_le : r ^ d ≤ n := by
        rw [← huv_mul]
        exact Nat.le_mul_of_pos_left (r ^ d)
          (Nat.pos_of_ne_zero (fun hu0 => by rw [hu0, zero_mul] at huv_mul; omega))
      exact le_trans (Nat.le_self_pow (by omega) r) hrd_le
    refine ⟨r, ?_, Prod.ext hu_eq.symm rfl⟩
    rw [powerDivisors, Finset.mem_filter, Finset.mem_Icc]
    exact ⟨⟨hr_pos, hr_le_n⟩, ⟨u, by rw [← huv_mul, mul_comm]⟩⟩
  · intro r hr
    rw [powerDivisors, Finset.mem_filter, Finset.mem_Icc] at hr
    have hz : (ArithmeticFunction.zeta : ArithmeticFunction ℤ) r = 1 := by
      have hr_ne : r ≠ 0 := by omega
      simp [hr_ne]
    rw [powerIndicatorArith, powerLiftArith_apply_pow_aux _ hd hr.1.1, hz, mul_one]

private theorem powerDivisors_two_eq_squareDivisors_aux {n : ℕ} (hn : 0 < n) :
    powerDivisors 2 n = squareDivisors n := by
  ext r
  simp only [powerDivisors, squareDivisors, Finset.mem_filter, Finset.mem_Icc, Nat.mem_divisors]
  constructor
  · rintro ⟨⟨_, _⟩, hrsq⟩
    exact ⟨⟨dvd_trans ⟨r, sq r⟩ hrsq, ne_of_gt hn⟩, hrsq⟩
  · rintro ⟨⟨hr_dvd, _⟩, hrsq⟩
    exact ⟨⟨Nat.pos_of_dvd_of_pos hr_dvd hn, Nat.le_of_dvd hn hr_dvd⟩, hrsq⟩

private theorem zeta_mul_liouville_eq_powerIndicator_two_aux :
    (ArithmeticFunction.zeta : ArithmeticFunction ℤ) * liouvilleArith = powerIndicatorArith 2 := by
  have h1 : liouvilleArith = ArithmeticFunction.moebius * powerIndicatorArith 2 := by
    ext n
    by_cases hn : n = 0
    · subst hn; simp
    · have hn_pos : 0 < n := Nat.pos_of_ne_zero hn
      rw [moebius_mul_powerIndicator_apply_aux (by omega : 0 < 2) hn_pos]
      obtain ⟨_, _, _, _, _, _, _, h_sq, _⟩ :=
        actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat
          Nat.prime_two 0 hn
      unfold actualFlatMoebiusSquareDivisorSum at h_sq
      unfold moebiusPowerDivisorSum
      rw [powerDivisors_two_eq_squareDivisors_aux hn_pos, h_sq]
      rfl
  rw [h1, ← mul_assoc, ArithmeticFunction.coe_zeta_mul_moebius, one_mul]

private theorem liouvillePowerLiftB_eq_moebius_mul_powerIndicator_aux (J : ℕ) (hJ : 1 ≤ J) :
    liouvillePowerLiftB J = ArithmeticFunction.moebius * powerIndicatorArith (2 ^ J) := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le' hJ
  induction' k with k ih
  · simp only [liouvillePowerLiftB, dyadicPowerLiftIterConv, dyadicPowerStepArith, one_mul,
      pow_zero, powerLiftArith_one_exp_eq_self_aux, zero_add, pow_one]
    ext n
    by_cases hn : n = 0
    · subst hn; simp
    · have hn_pos : 0 < n := Nat.pos_of_ne_zero hn
      rw [moebius_mul_powerIndicator_apply_aux (by omega : 0 < 2) hn_pos]
      obtain ⟨_, _, _, _, _, _, _, h_sq, _⟩ :=
        actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat
          Nat.prime_two 0 hn
      unfold actualFlatMoebiusSquareDivisorSum at h_sq
      unfold moebiusPowerDivisorSum
      rw [powerDivisors_two_eq_squareDivisors_aux hn_pos, h_sq]
      rfl
  · have hk1 : 1 ≤ k + 1 := by omega
    have h_prev := ih hk1
    change liouvillePowerLiftB (k + 1) * dyadicPowerStepArith liouvilleArith (k + 1) =
      ArithmeticFunction.moebius * powerIndicatorArith (2 ^ (k + 2))
    rw [h_prev, mul_assoc]
    congr 1
    unfold powerIndicatorArith dyadicPowerStepArith
    have hd_pos : 0 < 2 ^ (k + 1) := Nat.pos_pow_of_pos _ (by omega)
    rw [powerLiftArith_mul_hom_aux _ _ hd_pos, zeta_mul_liouville_eq_powerIndicator_two_aux]
    unfold powerIndicatorArith
    rw [powerLiftArith_comp_aux _ (by omega : 0 < 2) hd_pos]
    congr 1
    ring

/-- **Theorem 2 (`TASK-TC-059` §2 & §6, Dyadic Power-Lift Convolution, Prime-Power Evaluation, Stabilization, and Control Separation)**:
    *Formal scope (`UNCONDITIONAL_FINITE_ARITHMETIC`)*:
    1. Prime-local polynomial telescoping over any commutative ring `R`:
       `(1 - t) * ∏_{0 ≤ j < J} (1 + t^{2^j}) = 1 - t^{2^J}`;
    2. Exact divisor-sum formula for all `J ≥ 1` and `n ≥ 1`:
       `b_J(n) = ∑_{r^{2^J} ∣ n} μ(n / r^{2^J})` and `b_1(n) = λ(n)`;
    3. Exact prime-power evaluation for every prime `p`, `e : ℕ`, and `J ≥ 1`:
       `b_J(p^e) = 1` if `e % 2^J = 0`, `-1` if `e % 2^J = 1`, and `0` otherwise;
    4. Exact stabilization and boundary witness (`J ≥ 1`):
       - `∀ n, 1 ≤ n → n < 2^{2^J} → b_J(n) = μ(n)`;
       - `b_J(2^{2^J}) = 1 ∧ μ(2^{2^J}) = 0`;
       - `∀ n, 1 ≤ n → Squarefree n → b_J(n) = μ(n) ∧ Δ_J(n) = 0`;
       - `J_T := stabilizationDepthJ T` satisfies `1 ≤ J_T`, `T < 2^{2^{J_T}}`, `(1 < J_T → 2^{2^{J_T - 1}} ≤ T)`,
         and `∀ J ≥ J_T, ∀ n ∈ Finset.Icc 1 T, b_J(n) = μ(n)`;
    5. Prime-sign control separation at `J = 2`: for any multiplicative `a : ArithmeticFunction ℤ` with
       `a(p^2) = a(p)^2` at prime `p`, `b_{a,2}(p^2) = a(p) * (a(p) + 1)` (vanishing for `a(p) ∈ {-1, 1}` iff `a(p) = -1`,
       and equaling `2` when `a(p) = 1`). -/
theorem dyadic_power_lift_divisor_prime_power_and_stabilization_tc059 :
    (∀ {R : Type} [CommRing R] (t : R) (J : ℕ),
      (1 - t) * (∏ j ∈ Finset.range J, (1 + t ^ (2 ^ j))) = 1 - t ^ (2 ^ J)) ∧
    ((∀ n : ℕ, 1 ≤ n → liouvillePowerLiftB 1 n = liouvilleLambda n) ∧
      (∀ (J n : ℕ), 1 ≤ J → 1 ≤ n →
        liouvillePowerLiftB J n = moebiusPowerDivisorSum (2 ^ J) n)) ∧
    (∀ {p : ℕ}, p.Prime → ∀ (J e : ℕ), 1 ≤ J →
      liouvillePowerLiftB J (p ^ e) =
        if e % (2 ^ J) = 0 then 1 else if e % (2 ^ J) = 1 then -1 else 0) ∧
    ((∀ (J n : ℕ), 1 ≤ J → 1 ≤ n → n < 2 ^ (2 ^ J) →
        liouvillePowerLiftB J n = ArithmeticFunction.moebius n) ∧
      (∀ J : ℕ, 1 ≤ J →
        liouvillePowerLiftB J (2 ^ (2 ^ J)) = 1 ∧
          ArithmeticFunction.moebius (2 ^ (2 ^ J)) = 0) ∧
      (∀ (J n : ℕ), 1 ≤ J → 1 ≤ n → Squarefree n →
        liouvillePowerLiftB J n = ArithmeticFunction.moebius n ∧
          powerLiftIncrementDelta J n = 0) ∧
      (∀ T : ℕ,
        1 ≤ stabilizationDepthJ T ∧
          T < 2 ^ (2 ^ stabilizationDepthJ T) ∧
          (1 < stabilizationDepthJ T → 2 ^ (2 ^ (stabilizationDepthJ T - 1)) ≤ T) ∧
          (∀ J : ℕ, stabilizationDepthJ T ≤ J → ∀ n ∈ Finset.Icc 1 T,
            liouvillePowerLiftB J n = ArithmeticFunction.moebius n))) ∧
    (∀ (a : ArithmeticFunction ℤ) {p : ℕ}, p.Prime → a 1 = 1 → a (p ^ 2) = (a p) ^ 2 →
      dyadicPowerLiftIterConv a 2 (p ^ 2) = a p * (a p + 1) ∧
      (a p = 1 → dyadicPowerLiftIterConv a 2 (p ^ 2) = 2) ∧
      (a p = -1 → dyadicPowerLiftIterConv a 2 (p ^ 2) = 0)) := by
  have h_bJ_div : ∀ (J n : ℕ), 1 ≤ J → 1 ≤ n →
      liouvillePowerLiftB J n = moebiusPowerDivisorSum (2 ^ J) n := by
    intro J n hJ hn
    rw [liouvillePowerLiftB_eq_moebius_mul_powerIndicator_aux J hJ]
    exact moebius_mul_powerIndicator_apply_aux (Nat.pos_pow_of_pos J (by omega)) hn
  have h_bJ_lt : ∀ (J n : ℕ), 1 ≤ J → 1 ≤ n → n < 2 ^ (2 ^ J) →
      liouvillePowerLiftB J n = ArithmeticFunction.moebius n := by
    intro J n hJ hn hlt
    rw [h_bJ_div J n hJ hn]
    have hpdiv1 : powerDivisors (2 ^ J) n = {1} := by
      ext r
      simp only [powerDivisors, Finset.mem_filter, Finset.mem_Icc, Finset.mem_singleton]
      constructor
      · rintro ⟨⟨hr1, _⟩, hdvd⟩
        by_contra hne
        have hr2 : 2 ≤ r := by omega
        have hpow_ge : 2 ^ (2 ^ J) ≤ r ^ (2 ^ J) := Nat.pow_le_pow_left hr2 (2 ^ J)
        have hrd_le : r ^ (2 ^ J) ≤ n := Nat.le_of_dvd hn hdvd
        omega
      · rintro rfl
        exact ⟨⟨le_refl 1, hn⟩, by simp⟩
    simp [moebiusPowerDivisorSum, hpdiv1]
  refine ⟨?_, ⟨?_, h_bJ_div⟩, ?_, ⟨h_bJ_lt, ?_, ?_, ?_⟩, ?_⟩
  · intro R _ t J
    induction' J with J ih
    · simp
    · rw [Finset.prod_range_succ, ← mul_assoc, ih]
      have hpow : t ^ (2 ^ (J + 1)) = (t ^ (2 ^ J)) ^ 2 := by
        rw [pow_succ, pow_mul]
      rw [hpow]
      ring
  · intro n _
    simp only [liouvillePowerLiftB, dyadicPowerLiftIterConv, dyadicPowerStepArith, one_mul,
      pow_zero, powerLiftArith_one_exp_eq_self_aux]
    rfl
  · intro p hp J e hJ
    have hpe_pos : 1 ≤ p ^ e := Nat.one_le_pow e p hp.pos
    rw [h_bJ_div J (p ^ e) hJ hpe_pos]
    unfold moebiusPowerDivisorSum
    have hd_ge2 : 2 ≤ 2 ^ J := by
      have h1 : 2 ^ 1 ≤ 2 ^ J := Nat.pow_le_pow_right (by omega) hJ
      simpa using h1
    have hd_pos : 0 < 2 ^ J := by omega
    have he_decomp : (e / (2 ^ J)) * (2 ^ J) + e % (2 ^ J) = e := by
      have h := Nat.div_add_mod e (2 ^ J)
      rwa [mul_comm] at h
    have hqd_le : (e / (2 ^ J)) * (2 ^ J) ≤ e := by omega
    have hp_q_mem : p ^ (e / (2 ^ J)) ∈ powerDivisors (2 ^ J) (p ^ e) := by
      rw [powerDivisors, Finset.mem_filter, Finset.mem_Icc]
      have hpq_pos : 1 ≤ p ^ (e / (2 ^ J)) := Nat.one_le_pow _ p hp.pos
      have hpq_le : p ^ (e / (2 ^ J)) ≤ p ^ e :=
        Nat.pow_le_pow_right hp.pos (le_trans (Nat.le_mul_of_pos_right _ hd_pos) hqd_le)
      have hpqd_dvd : (p ^ (e / (2 ^ J))) ^ (2 ^ J) ∣ p ^ e := by
        rw [← pow_mul]
        exact Nat.pow_dvd_pow p hqd_le
      exact ⟨⟨hpq_pos, hpq_le⟩, hpqd_dvd⟩
    have h_other_zero :
        ∀ r ∈ powerDivisors (2 ^ J) (p ^ e), r ≠ p ^ (e / (2 ^ J)) →
          ArithmeticFunction.moebius (p ^ e / r ^ (2 ^ J)) = 0 := by
      intro r hr hne
      rw [powerDivisors, Finset.mem_filter, Finset.mem_Icc] at hr
      have hrd_dvd : r ^ (2 ^ J) ∣ p ^ e := hr.2
      have hr_dvd : r ∣ p ^ e := dvd_trans (dvd_pow_self r (by omega)) hrd_dvd
      obtain ⟨k, _, rfl⟩ := (Nat.dvd_prime_pow hp).mp hr_dvd
      have hk_ne_q : k ≠ e / (2 ^ J) := fun hkq => hne (by rw [hkq])
      have hkd_le : k * (2 ^ J) ≤ e := by
        rw [← pow_mul] at hrd_dvd
        exact (Nat.pow_dvd_pow_iff_le_right hp.one_lt).mp hrd_dvd
      have hk_lt_q : k < e / (2 ^ J) := by
        by_contra hnot
        have hq1 : e / (2 ^ J) + 1 ≤ k := by omega
        have h1 : (e / (2 ^ J) + 1) * (2 ^ J) ≤ k * (2 ^ J) := Nat.mul_le_mul_right (2 ^ J) hq1
        have hrem_lt : e % (2 ^ J) < 2 ^ J := Nat.mod_lt e hd_pos
        nlinarith
      have he_sub_ge2 : 2 ≤ e - k * (2 ^ J) := by
        have hq1 : k + 1 ≤ e / (2 ^ J) := by omega
        have h1 : (k + 1) * (2 ^ J) ≤ (e / (2 ^ J)) * (2 ^ J) := Nat.mul_le_mul_right (2 ^ J) hq1
        have h2 : k * (2 ^ J) + 2 ^ J ≤ e := by linarith
        omega
      have hdiv_pow : p ^ e / (p ^ k) ^ (2 ^ J) = p ^ (e - k * (2 ^ J)) := by
        rw [← pow_mul]
        exact Nat.pow_div hkd_le hp.pos
      rw [hdiv_pow, ArithmeticFunction.moebius_apply_prime_pow hp (by omega), if_neg (by omega)]
    rw [← Finset.add_sum_erase _ _ hp_q_mem]
    have h_er_zero :
        ∑ r ∈ (powerDivisors (2 ^ J) (p ^ e)).erase (p ^ (e / (2 ^ J))),
          ArithmeticFunction.moebius (p ^ e / r ^ (2 ^ J)) = 0 := by
      apply Finset.sum_eq_zero
      intro r hr
      exact h_other_zero r (Finset.mem_of_mem_erase hr) (Finset.ne_of_mem_erase hr)
    rw [h_er_zero, add_zero]
    have hdiv_pq : p ^ e / (p ^ (e / (2 ^ J))) ^ (2 ^ J) = p ^ (e % (2 ^ J)) := by
      rw [← pow_mul, Nat.pow_div hqd_le hp.pos]
      congr 1
      omega
    rw [hdiv_pq]
    rcases e % (2 ^ J) with _ | _ | rem'
    · simp [ArithmeticFunction.moebius_apply_one]
    · simp [ArithmeticFunction.moebius_apply_prime hp]
    · rw [ArithmeticFunction.moebius_apply_prime_pow hp (by omega), if_neg (by omega)]
      simp
  · intro J hJ
    have h2 : 1 ≤ (2 ^ (2 ^ J)) := Nat.one_le_pow _ 2 (by omega)
    have hd_ge2 : 2 ≤ 2 ^ J := by
      have h1 : 2 ^ 1 ≤ 2 ^ J := Nat.pow_le_pow_right (by omega) hJ
      simpa using h1
    have hmu0 : ArithmeticFunction.moebius (2 ^ (2 ^ J)) = 0 := by
      rw [ArithmeticFunction.moebius_apply_prime_pow Nat.prime_two (by omega), if_neg (by omega)]
    refine ⟨?_, hmu0⟩
    rw [h_bJ_div J (2 ^ (2 ^ J)) hJ h2]
    have hpdiv_pair : powerDivisors (2 ^ J) (2 ^ (2 ^ J)) = {1, 2} := by
      ext r
      simp only [powerDivisors, Finset.mem_filter, Finset.mem_Icc, Finset.mem_insert,
        Finset.mem_singleton]
      constructor
      · rintro ⟨⟨_, _⟩, hdvd⟩
        by_cases hr2 : r ≤ 2
        · omega
        · exfalso
          have hlt : 2 ^ (2 ^ J) < r ^ (2 ^ J) := Nat.pow_lt_pow_left (by omega : 2 < r) (by omega)
          have hle : r ^ (2 ^ J) ≤ 2 ^ (2 ^ J) := Nat.le_of_dvd h2 hdvd
          omega
      · rintro (rfl | rfl)
        · exact ⟨⟨le_refl 1, by omega⟩, by simp⟩
        · exact ⟨⟨by omega, le_trans hd_ge2 (le_of_lt (Nat.lt_pow_self (by omega : 1 < 2) (2 ^ J)))⟩, dvd_refl _⟩
    unfold moebiusPowerDivisorSum
    rw [hpdiv_pair, Finset.sum_pair (by decide)]
    simp [hmu0, Nat.div_self h2]
  · intro J n hJ hn hsqf
    have hd_ge2 : 2 ≤ 2 ^ J := by
      have h1 : 2 ^ 1 ≤ 2 ^ J := Nat.pow_le_pow_right (by omega) hJ
      simpa using h1
    have hpdiv_sqf : ∀ d : ℕ, 2 ≤ d → powerDivisors d n = {1} := by
      intro d hd2
      ext r
      simp only [powerDivisors, Finset.mem_filter, Finset.mem_Icc, Finset.mem_singleton]
      constructor
      · rintro ⟨⟨_, _⟩, hdvd⟩
        have hr2_dvd : r * r ∣ n := by
          obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le' hd2
          have : r ^ 2 ∣ r ^ (k + 2) := Nat.pow_dvd_pow r (by omega)
          simpa [sq] using dvd_trans this hdvd
        exact Nat.isUnit_iff.mp (hsqf r hr2_dvd)
      · rintro rfl
        exact ⟨⟨le_refl 1, hn⟩, by simp⟩
    have hbJ : liouvillePowerLiftB J n = ArithmeticFunction.moebius n := by
      rw [h_bJ_div J n hJ hn]
      simp [moebiusPowerDivisorSum, hpdiv_sqf (2 ^ J) hd_ge2]
    have hbJ1 : liouvillePowerLiftB (J + 1) n = ArithmeticFunction.moebius n := by
      rw [h_bJ_div (J + 1) n (by omega) hn]
      have hd1_ge2 : 2 ≤ 2 ^ (J + 1) := by
        have : 2 ^ 1 ≤ 2 ^ (J + 1) := Nat.pow_le_pow_right (by omega) (by omega)
        simpa using this
      simp [moebiusPowerDivisorSum, hpdiv_sqf (2 ^ (J + 1)) hd1_ge2]
    exact ⟨hbJ, by unfold powerLiftIncrementDelta; omega⟩
  · intro T
    have hspec := Nat.find_spec (exists_stabilization_depth_aux T)
    refine ⟨hspec.1, hspec.2, ?_, ?_⟩
    · intro hgt1
      by_contra hlt
      push_neg at hlt
      have hmin := Nat.find_min (exists_stabilization_depth_aux T)
        (by omega : stabilizationDepthJ T - 1 < stabilizationDepthJ T)
      exact hmin ⟨by omega, hlt⟩
    · intro J hJ n hn
      rw [Finset.mem_Icc] at hn
      have hJ1 : 1 ≤ J := le_trans hspec.1 hJ
      have hpow_mono : 2 ^ (2 ^ stabilizationDepthJ T) ≤ 2 ^ (2 ^ J) :=
        Nat.pow_le_pow_right (by omega) (Nat.pow_le_pow_right (by omega) hJ)
      exact h_bJ_lt J n hJ1 hn.1 (lt_of_le_of_lt hn.2 (lt_of_lt_of_le hspec.2 hpow_mono))
  · intro a p hp ha1 hap2
    have h_conv :
        dyadicPowerLiftIterConv a 2 (p ^ 2) = (a * dyadicPowerStepArith a 1) (p ^ 2) := by
      simp only [dyadicPowerLiftIterConv, dyadicPowerStepArith, one_mul, pow_zero,
        powerLiftArith_one_exp_eq_self_aux, pow_one]
    rw [h_conv, ArithmeticFunction.mul_apply]
    have hp2_antidiag :
        Nat.divisorsAntidiagonal (p ^ 2) = {(1, p ^ 2), (p, p), (p ^ 2, 1)} := by
      ext ⟨u, v⟩
      simp only [Nat.mem_divisorsAntidiagonal, Finset.mem_insert, Finset.mem_singleton, Prod.mk.injEq]
      have hp2_ne : p ^ 2 ≠ 0 := pow_ne_zero 2 hp.ne_zero
      constructor
      · rintro ⟨huv, _⟩
        have hu_dvd : u ∣ p ^ 2 := ⟨v, huv.symm⟩
        obtain ⟨k, hk_le, rfl⟩ := (Nat.dvd_prime_pow hp).mp hu_dvd
        interval_cases k
        · left; simp at huv ⊢; exact huv
        · right; left
          have hv : v = p := by
            apply Nat.eq_of_mul_eq_mul_left hp.pos
            simpa [sq] using huv
          simp [hv]
        · right; right
          have hv : v = 1 := by
            apply Nat.eq_of_mul_eq_mul_left (Nat.pow_pos hp.pos)
            simpa using huv
          exact ⟨rfl, hv⟩
      · rintro (⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩)
        · exact ⟨by ring, hp2_ne⟩
        · exact ⟨by ring, hp2_ne⟩
        · exact ⟨by ring, hp2_ne⟩
    have h12 : (1, p ^ 2) ∉ ({(p, p), (p ^ 2, 1)} : Finset (ℕ × ℕ)) := by
      have h1_lt_p2 : 1 < p ^ 2 := one_lt_pow hp.one_lt (by omega)
      simp [ne_of_lt hp.one_lt, ne_of_lt h1_lt_p2]
    have h23 : (p, p) ≠ (p ^ 2, 1) := by
      intro h
      injection h with _ hp1
      exact hp.ne_one hp1
    rw [hp2_antidiag, Finset.sum_insert h12, Finset.sum_pair h23]
    have ha1_step_p2 : dyadicPowerStepArith a 1 (p ^ 2) = a p := by
      unfold dyadicPowerStepArith
      rw [pow_one]
      exact powerLiftArith_apply_pow_aux a (by omega : 0 < 2) hp.pos
    have ha1_step_p : dyadicPowerStepArith a 1 p = 0 := by
      unfold dyadicPowerStepArith
      rw [pow_one]
      apply powerLiftArith_apply_not_pow_aux a
      intro m _ hmp
      have hm_dvd : m ∣ p := ⟨m, by rw [← hmp, sq]⟩
      rcases hp.eq_one_or_self_of_dvd m hm_dvd with rfl | hmp_eq
      · simp at hmp; exact hp.ne_one hmp.symm
      · subst hmp_eq
        have : m * 1 < m * m := Nat.mul_lt_mul_of_pos_left hp.one_lt hp.pos
        rw [sq] at hmp
        omega
    have ha1_step_1 : dyadicPowerStepArith a 1 1 = a 1 := by
      unfold dyadicPowerStepArith
      rw [pow_one]
      simpa using powerLiftArith_apply_pow_aux a (by omega : 0 < 2) (by omega : 0 < 1)
    rw [ha1_step_p2, ha1_step_p, ha1_step_1, ha1, hap2]
    refine ⟨by ring, ?_, ?_⟩
    · intro hp_pos1; rw [hp_pos1]; norm_num
    · intro hp_neg1; rw [hp_neg1]; norm_num

/-! ### Section 3: Finite Gaussian Power-Lift, Non-Square Increment Stratification, and Coherent Tail -/

private theorem power_divisor_gaussian_sum_reindexing_aux
    {d : ℕ} (hd_even : Even d) (_hd_pos : 0 < d) (T : ℕ) {X : ℝ} (hX : 0 ≤ X) :
    finiteQGeneral (fun n => (moebiusPowerDivisorSum d n : ℝ)) T X =
      ∑ r ∈ (Finset.Icc 1 T).filter (fun r => r ^ d ≤ T),
        (1 / (((r ^ (d / 2)) : ℕ) : ℝ)) *
          finiteQGeneral (fun m => (ArithmeticFunction.moebius m : ℝ))
            (T / r ^ d) (X / (((r ^ d) : ℕ) : ℝ)) := by
  obtain ⟨h, rfl⟩ := hd_even
  have _hh_pos : 0 < h := by omega
  have h2h : (h + h) / 2 = h := by omega
  rw [h2h]
  rcases eq_or_lt_of_le hX with rfl | _hX_pos
  · have hz : (0 : ℝ) ^ (5 / 2 : ℝ) = 0 := Real.zero_rpow (by norm_num)
    have hphi0 : ∀ m : ℕ, gaussianTermPhi m 0 = 0 := fun m => by simp [gaussianTermPhi, hz]
    unfold finiteQGeneral
    simp only [zero_div, hphi0, mul_zero, Finset.sum_const_zero]
  · unfold finiteQGeneral
    have h_expand :
        ∑ n ∈ Finset.Icc 1 T, (moebiusPowerDivisorSum (h + h) n : ℝ) * gaussianTermPhi n X =
        ∑ n ∈ Finset.Icc 1 T,
          ∑ r ∈ ((Finset.Icc 1 T).filter (fun r => r ^ (h + h) ≤ T)).filter (fun r => r ^ (h + h) ∣ n),
            (ArithmeticFunction.moebius (n / r ^ (h + h)) : ℝ) * gaussianTermPhi n X := by
      apply Finset.sum_congr rfl
      intro n hn
      rw [Finset.mem_Icc] at hn
      unfold moebiusPowerDivisorSum
      push_cast
      rw [Finset.sum_mul]
      apply Finset.sum_congr
      · ext r
        simp only [powerDivisors, Finset.mem_filter, Finset.mem_Icc]
        constructor
        · rintro ⟨⟨hr1, hrn⟩, hdvd⟩
          have hrd_le : r ^ (h + h) ≤ n := Nat.le_of_dvd hn.1 hdvd
          exact ⟨⟨⟨hr1, le_trans hrn hn.2⟩, le_trans hrd_le hn.2⟩, hdvd⟩
        · rintro ⟨⟨⟨hr1, _⟩, _⟩, hdvd⟩
          have hrd_le : r ^ (h + h) ≤ n := Nat.le_of_dvd hn.1 hdvd
          have hr_le : r ≤ r ^ (h + h) := Nat.le_self_pow (by omega) r
          exact ⟨⟨hr1, le_trans hr_le hrd_le⟩, hdvd⟩
      · intros; rfl
    rw [h_expand, Finset.sum_sigma']
    symm
    have h_rhs_in :
        ∑ r ∈ (Finset.Icc 1 T).filter (fun r => r ^ (h + h) ≤ T),
          (1 / (((r ^ h) : ℕ) : ℝ)) *
            ∑ m ∈ Finset.Icc 1 (T / r ^ (h + h)),
              (ArithmeticFunction.moebius m : ℝ) *
                gaussianTermPhi m (X / (((r ^ (h + h)) : ℕ) : ℝ)) =
        ∑ r ∈ (Finset.Icc 1 T).filter (fun r => r ^ (h + h) ≤ T),
          ∑ m ∈ Finset.Icc 1 (T / r ^ (h + h)),
            (ArithmeticFunction.moebius m : ℝ) * gaussianTermPhi (r ^ (h + h) * m) X := by
      apply Finset.sum_congr rfl
      intro r hr
      rw [Finset.mem_filter, Finset.mem_Icc] at hr
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro m _
      have hrd_pos : 0 < r ^ (h + h) := Nat.pow_pos hr.1.1
      have hsqrt_rd : Real.sqrt (((r ^ (h + h)) : ℕ) : ℝ) = (((r ^ h) : ℕ) : ℝ) := by
        have hsq : r ^ (h + h) = (r ^ h) ^ 2 := by rw [pow_add, sq]
        rw [hsq]
        push_cast
        exact Real.sqrt_sq (by positivity)
      rw [gaussianTermPhi_mul_scale_aux hrd_pos m hX, hsqrt_rd]
      ring
    rw [h_rhs_in, Finset.sum_sigma']
    apply Finset.sum_bij (fun rm _ => ⟨rm.1 ^ (h + h) * rm.2, rm.1⟩)
    · rintro ⟨r, m⟩ hrm
      simp only [Finset.mem_sigma, Finset.mem_filter, Finset.mem_Icc] at hrm ⊢
      rcases hrm with ⟨⟨⟨hr1, hrT⟩, hrdT⟩, ⟨hm1, hm_div⟩⟩
      have hrd_pos : 0 < r ^ (h + h) := Nat.pow_pos hr1
      have h_mul_le : r ^ (h + h) * m ≤ T := by
        rw [mul_comm]
        exact (Nat.le_div_iff_mul_le hrd_pos).mp hm_div
      exact ⟨⟨Nat.mul_pos hrd_pos hm1, h_mul_le⟩, ⟨⟨hr1, hrT⟩, hrdT⟩, ⟨m, rfl⟩⟩
    · rintro ⟨r1, m1⟩ h1 ⟨r2, m2⟩ _ heq
      simp only [Finset.mem_sigma, Finset.mem_filter, Finset.mem_Icc] at h1
      have hr_eq : r1 = r2 := eq_of_heq (Sigma.mk.inj_iff.mp heq).2
      subst hr_eq
      have hprod_eq : r1 ^ (h + h) * m1 = r1 ^ (h + h) * m2 := (Sigma.mk.inj_iff.mp heq).1
      have hm_eq : m1 = m2 := Nat.eq_of_mul_eq_mul_left (Nat.pow_pos h1.1.1.1) hprod_eq
      subst hm_eq
      rfl
    · rintro ⟨n, r⟩ hnr
      simp only [Finset.mem_sigma, Finset.mem_filter, Finset.mem_Icc] at hnr
      rcases hnr with ⟨⟨hn1, hnT⟩, ⟨⟨hr1, hrT⟩, hrdT⟩, ⟨m, rfl⟩⟩
      have hrd_pos : 0 < r ^ (h + h) := Nat.pow_pos hr1
      have hm1 : 1 ≤ m := by
        by_contra h0
        have hm0 : m = 0 := by omega
        rw [hm0, mul_zero] at hn1
        omega
      have hm_div : m ≤ T / r ^ (h + h) :=
        (Nat.le_div_iff_mul_le hrd_pos).mpr (by rw [mul_comm]; exact hnT)
      refine ⟨⟨r, m⟩, ?_, rfl⟩
      simp only [Finset.mem_sigma, Finset.mem_filter, Finset.mem_Icc]
      exact ⟨⟨⟨hr1, hrT⟩, hrdT⟩, ⟨hm1, hm_div⟩⟩
    · rintro ⟨r, m⟩ hrm
      simp only [Finset.mem_sigma, Finset.mem_filter, Finset.mem_Icc] at hrm
      have hrd_pos : 0 < r ^ (h + h) := Nat.pow_pos hrm.1.1.1
      rw [Nat.mul_div_cancel_left m hrd_pos]

private theorem powerLiftIncrementDelta_eq_neg_nonsquare_sum_aux
    {J n : ℕ} (hJ : 1 ≤ J) (hn : 1 ≤ n) :
    powerLiftIncrementDelta J n =
      - ∑ s ∈ (powerDivisors (2 ^ J) n).filter (fun s => ¬ IsSquare s),
          ArithmeticFunction.moebius (n / s ^ (2 ^ J)) := by
  obtain ⟨_, ⟨_, h_bJ_div⟩, _, _, _⟩ := dyadic_power_lift_divisor_prime_power_and_stabilization_tc059
  unfold powerLiftIncrementDelta
  rw [h_bJ_div (J + 1) n (by omega) hn, h_bJ_div J n hJ hn]
  unfold moebiusPowerDivisorSum
  have hd_pos : 0 < 2 ^ J := Nat.pos_pow_of_pos J (by omega)
  have h_sq_bij :
      ∑ r ∈ powerDivisors (2 ^ (J + 1)) n, ArithmeticFunction.moebius (n / r ^ (2 ^ (J + 1))) =
        ∑ s ∈ (powerDivisors (2 ^ J) n).filter (fun s => IsSquare s),
          ArithmeticFunction.moebius (n / s ^ (2 ^ J)) := by
    apply Finset.sum_bij (fun r _ => r ^ 2)
    · intro r hr
      simp only [powerDivisors, Finset.mem_filter, Finset.mem_Icc] at hr ⊢
      have hr2_pow : (r ^ 2) ^ (2 ^ J) = r ^ (2 ^ (J + 1)) := by
        rw [← pow_mul, pow_succ']
      have hr2_dvd : (r ^ 2) ^ (2 ^ J) ∣ n := by
        rw [hr2_pow]
        exact hr.2
      have hr2_le_pow : r ^ 2 ≤ (r ^ 2) ^ (2 ^ J) := Nat.le_self_pow (by omega) (r ^ 2)
      have hr2_le_n : r ^ 2 ≤ n := le_trans hr2_le_pow (Nat.le_of_dvd hn hr2_dvd)
      exact ⟨⟨⟨Nat.pow_pos hr.1.1, hr2_le_n⟩, hr2_dvd⟩, ⟨r, sq r⟩⟩
    · intro r1 hr1 r2 hr2 heq
      simp only [powerDivisors, Finset.mem_filter, Finset.mem_Icc] at hr1 hr2
      exact pow_eq_inj_pos_aux (by omega : 0 < 2) hr1.1.1 hr2.1.1 heq
    · intro s hs
      simp only [powerDivisors, Finset.mem_filter, Finset.mem_Icc] at hs
      rcases hs with ⟨⟨⟨hs1, _⟩, hsdvd⟩, ⟨r, rfl⟩⟩
      have hr_pos : 0 < r := by
        by_contra h0
        have hr0 : r = 0 := by omega
        rw [hr0] at hs1
        omega
      have hr2_eq : r * r = r ^ 2 := (sq r).symm
      rw [hr2_eq] at hsdvd ⊢
      have hrd1_dvd : r ^ (2 ^ (J + 1)) ∣ n := by
        have hpow : (r ^ 2) ^ (2 ^ J) = r ^ (2 ^ (J + 1)) := by rw [← pow_mul, pow_succ']
        rwa [← hpow]
      have hr_le_n : r ≤ n :=
        le_trans (Nat.le_self_pow (by positivity) r) (Nat.le_of_dvd hn hrd1_dvd)
      refine ⟨r, ?_, rfl⟩
      simp only [powerDivisors, Finset.mem_filter, Finset.mem_Icc]
      exact ⟨⟨hr_pos, hr_le_n⟩, hrd1_dvd⟩
    · intro r _
      have hpow : (r ^ 2) ^ (2 ^ J) = r ^ (2 ^ (J + 1)) := by rw [← pow_mul, pow_succ']
      rw [hpow]
  rw [h_sq_bij]
  have h_split :=
    Finset.sum_filter_add_sum_filter_not (powerDivisors (2 ^ J) n) (fun s => IsSquare s)
      (fun s => ArithmeticFunction.moebius (n / s ^ (2 ^ J)))
  linarith [h_split]

/-- **Theorem 3 (`TASK-TC-059` §2 & §4A, Finite Gaussian Power-Lift, Non-Square Increment Stratification, Full Window Expansion, and Coherent Stabilized-Tail Negative Control)**:
    *Formal scope (`CONCRETE_ANALYTIC_IN_LEAN` & `UNCONDITIONAL_FINITE_ARITHMETIC`)*:
    1. Exact finite Gaussian power-lift for all `J ≥ 1`, all cutoffs `T : ℕ` (including `T = 0, 1`), and all `X ≥ 0` (including `X = 0`):
       `Q_{b_J, T}(X) = ∑_{1 ≤ r ≤ T, r^{2^J} ≤ T} r^{-(2^J)/2} Q_{μ, ⌊T / r^{2^J}⌋}(X / r^{2^J})`
       (given in both integer-exponent `1 / (r^{2^{J-1}} : ℝ)` and real-rpow `(r : ℝ)^{-(2^J : ℝ) / 2}` forms, with explicit
       checks `Q_{b_J, 0}(X) = 0`, `Q_{b_J, 1}(X) = φ_1(X)`, and `Q_{b_J, T}(0) = 0`);
    2. Increment support, boundary witness, and exact non-square divisor & Gaussian stratification (`J ≥ 1`):
       - `∀ n, 1 ≤ n → n < 2^{2^J} → Δ_J(n) = 0`, and `Δ_J(2^{2^J}) = -1`;
       - `∀ n ≥ 1, Δ_J(n) = - ∑_{s ∈ powerDivisors (2^J) n, ¬ IsSquare s} μ(n / s^{2^J})`;
       - `∀ T : ℕ, ∀ X ≥ 0, Q_{Δ_J, T}(X) = - ∑_{2 ≤ s ≤ T, s^{2^J} ≤ T, ¬ IsSquare s} s^{-2^{J-1}} Q_{μ, ⌊T / s^{2^J}⌋}(X / s^{2^J})`;
    3. Exact finite coefficient and Gaussian telescoping up to `J_T := stabilizationDepthJ T`:
       - `∀ T : ℕ, ∀ n ∈ Finset.Icc 1 T, μ(n) = λ(n) + ∑_{1 ≤ J < J_T} Δ_J(n)`;
       - `∀ T : ℕ, ∀ X : ℝ, Q_{λ, T}(X) = Q_{μ, T}(X) - ∑_{1 ≤ J < J_T} Q_{Δ_J, T}(X)`;
    4. Exact window-integrated quadratic expansion for all `u > 0` and `T : ℕ` retaining the `Q_μ` baseline, all baseline–increment
       cross terms, and all increment–increment cross terms:
       `E_{λ, T}(u) = E_{μ, T}(u) - 2 ∑_{1 ≤ J < J_T} ⟨Q_{μ, T}, Q_{Δ_J, T}⟩_u + ∑_{1 ≤ J_1 < J_T} ∑_{1 ≤ J_2 < J_T} ⟨Q_{Δ_{J_1}, T}, Q_{Δ_{J_2}, T}⟩_u`;
    5. Decisive stabilized-tail negative control (`u > 0`, `T : ℕ`, `J_1, J_2 ≥ J_T`):
       `Q_{b_{J_1}, T} = Q_{μ, T}` and `⟨Q_{b_{J_1}, T}, Q_{b_{J_2}, T}⟩_u = E_{μ, T}(u)` (coherent Gram tail). -/
theorem gaussian_power_lift_increment_telescope_and_coherent_tail_tc059 :
    ((∀ (J T : ℕ) {X : ℝ}, 1 ≤ J → 0 ≤ X →
        finiteQGeneral (fun n => (liouvillePowerLiftB J n : ℝ)) T X =
          (∑ r ∈ (Finset.Icc 1 T).filter (fun r => r ^ (2 ^ J) ≤ T),
            (1 / (((r ^ (2 ^ (J - 1))) : ℕ) : ℝ)) *
              finiteQGeneral (fun m => (ArithmeticFunction.moebius m : ℝ))
                (T / r ^ (2 ^ J)) (X / (((r ^ (2 ^ J)) : ℕ) : ℝ))) ∧
        finiteQGeneral (fun n => (liouvillePowerLiftB J n : ℝ)) T X =
          (∑ r ∈ (Finset.Icc 1 T).filter (fun r => r ^ (2 ^ J) ≤ T),
            ((r : ℝ) ^ (-(((2 ^ J : ℕ) : ℝ) / 2))) *
              finiteQGeneral (fun m => (ArithmeticFunction.moebius m : ℝ))
                (T / r ^ (2 ^ J)) (X / (((r ^ (2 ^ J)) : ℕ) : ℝ)))) ∧
      (∀ (J : ℕ) (X : ℝ), 1 ≤ J →
        finiteQGeneral (fun n => (liouvillePowerLiftB J n : ℝ)) 0 X = 0 ∧
        finiteQGeneral (fun n => (liouvillePowerLiftB J n : ℝ)) 1 X = gaussianTermPhi 1 X) ∧
      (∀ (J T : ℕ), 1 ≤ J →
        finiteQGeneral (fun n => (liouvillePowerLiftB J n : ℝ)) T 0 = 0)) ∧
    ((∀ (J n : ℕ), 1 ≤ J → 1 ≤ n → n < 2 ^ (2 ^ J) → powerLiftIncrementDelta J n = 0) ∧
      (∀ J : ℕ, 1 ≤ J → powerLiftIncrementDelta J (2 ^ (2 ^ J)) = -1) ∧
      (∀ (J n : ℕ), 1 ≤ J → 1 ≤ n →
        powerLiftIncrementDelta J n =
          - ∑ s ∈ (powerDivisors (2 ^ J) n).filter (fun s => ¬ IsSquare s),
              ArithmeticFunction.moebius (n / s ^ (2 ^ J))) ∧
      (∀ (J T : ℕ) {X : ℝ}, 1 ≤ J → 0 ≤ X →
        finiteQGeneral (fun n => (powerLiftIncrementDelta J n : ℝ)) T X =
          - ∑ s ∈ (Finset.Icc 2 T).filter (fun s => s ^ (2 ^ J) ≤ T ∧ ¬ IsSquare s),
              (1 / (((s ^ (2 ^ (J - 1))) : ℕ) : ℝ)) *
                finiteQGeneral (fun m => (ArithmeticFunction.moebius m : ℝ))
                  (T / s ^ (2 ^ J)) (X / (((s ^ (2 ^ J)) : ℕ) : ℝ)))) ∧
    ((∀ (T : ℕ), ∀ n ∈ Finset.Icc 1 T,
        ArithmeticFunction.moebius n =
          liouvilleLambda n +
            ∑ J ∈ Finset.Ico 1 (stabilizationDepthJ T), powerLiftIncrementDelta J n) ∧
      (∀ (T : ℕ) (X : ℝ),
        finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) T X =
          finiteQGeneral (fun n => (ArithmeticFunction.moebius n : ℝ)) T X -
            ∑ J ∈ Finset.Ico 1 (stabilizationDepthJ T),
              finiteQGeneral (fun n => (powerLiftIncrementDelta J n : ℝ)) T X)) ∧
    (∀ {u : ℝ}, 0 < u → ∀ T : ℕ,
      actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) T u =
        actualWindowEnergyE (fun n => (ArithmeticFunction.moebius n : ℝ)) T u -
          2 * (∑ J ∈ Finset.Ico 1 (stabilizationDepthJ T),
            windowPairing u
              (finiteQGeneral (fun n => (ArithmeticFunction.moebius n : ℝ)) T)
              (finiteQGeneral (fun n => (powerLiftIncrementDelta J n : ℝ)) T)) +
          ∑ J1 ∈ Finset.Ico 1 (stabilizationDepthJ T),
            ∑ J2 ∈ Finset.Ico 1 (stabilizationDepthJ T),
              windowPairing u
                (finiteQGeneral (fun n => (powerLiftIncrementDelta J1 n : ℝ)) T)
                (finiteQGeneral (fun n => (powerLiftIncrementDelta J2 n : ℝ)) T)) ∧
    (∀ {u : ℝ}, 0 < u → ∀ (T J1 J2 : ℕ),
      stabilizationDepthJ T ≤ J1 → stabilizationDepthJ T ≤ J2 →
      (∀ X : ℝ,
        finiteQGeneral (fun n => (liouvillePowerLiftB J1 n : ℝ)) T X =
          finiteQGeneral (fun n => (ArithmeticFunction.moebius n : ℝ)) T X) ∧
      windowPairing u
          (finiteQGeneral (fun n => (liouvillePowerLiftB J1 n : ℝ)) T)
          (finiteQGeneral (fun n => (liouvillePowerLiftB J2 n : ℝ)) T) =
        actualWindowEnergyE (fun n => (ArithmeticFunction.moebius n : ℝ)) T u) := by
  obtain ⟨_, ⟨hb1_eq, hbJ_div⟩, _, ⟨hbJ_lt, hbJ_bdry, _, hJT_props⟩, _⟩ :=
    dyadic_power_lift_divisor_prime_power_and_stabilization_tc059
  have h_tele_coeff :
      ∀ (T : ℕ), ∀ n ∈ Finset.Icc 1 T,
        ArithmeticFunction.moebius n =
          liouvilleLambda n +
            ∑ J ∈ Finset.Ico 1 (stabilizationDepthJ T), powerLiftIncrementDelta J n := by
    intro T n hn
    rw [Finset.mem_Icc] at hn
    obtain ⟨hJT1, _, _, hJT_stab⟩ := hJT_props T
    have h_sum_ico :
        ∀ K : ℕ, 1 ≤ K →
          liouvillePowerLiftB 1 n + ∑ J ∈ Finset.Ico 1 K, powerLiftIncrementDelta J n =
            liouvillePowerLiftB K n := by
      intro K hK
      obtain ⟨m, rfl⟩ := Nat.exists_eq_add_of_le' hK
      induction' m with m ih
      · simp
      · have h_ico_succ : Finset.Ico 1 (m + 2) = insert (m + 1) (Finset.Ico 1 (m + 1)) := by
          ext x; simp only [Finset.mem_Ico, Finset.mem_insert]; omega
        have h_not_mem : (m + 1) ∉ Finset.Ico 1 (m + 1) := by simp
        rw [h_ico_succ, Finset.sum_insert h_not_mem]
        have h_ih_m := ih (by omega)
        have h_del :
            powerLiftIncrementDelta (m + 1) n =
              liouvillePowerLiftB (m + 2) n - liouvillePowerLiftB (m + 1) n := rfl
        rw [h_del]
        linarith [h_ih_m]
    have hK := h_sum_ico (stabilizationDepthJ T) hJT1
    rw [hb1_eq n hn.1, hJT_stab (stabilizationDepthJ T) (le_refl _) n (Finset.mem_Icc.mpr hn)] at hK
    exact hK.symm
  have h_tele_Q :
      ∀ (T : ℕ) (X : ℝ),
        finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) T X =
          finiteQGeneral (fun n => (ArithmeticFunction.moebius n : ℝ)) T X -
            ∑ J ∈ Finset.Ico 1 (stabilizationDepthJ T),
              finiteQGeneral (fun n => (powerLiftIncrementDelta J n : ℝ)) T X := by
    intro T X
    unfold finiteQGeneral
    rw [Finset.sum_comm]
    have h_rhs :
        (∑ n ∈ Finset.Icc 1 T, (ArithmeticFunction.moebius n : ℝ) * gaussianTermPhi n X) -
            ∑ n ∈ Finset.Icc 1 T,
              ∑ J ∈ Finset.Ico 1 (stabilizationDepthJ T),
                (powerLiftIncrementDelta J n : ℝ) * gaussianTermPhi n X =
          ∑ n ∈ Finset.Icc 1 T,
            ((ArithmeticFunction.moebius n : ℝ) -
              ∑ J ∈ Finset.Ico 1 (stabilizationDepthJ T), (powerLiftIncrementDelta J n : ℝ)) *
              gaussianTermPhi n X := by
      rw [← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro n _
      rw [← Finset.sum_mul, sub_mul]
    rw [h_rhs]
    apply Finset.sum_congr rfl
    intro n hn
    have hc := h_tele_coeff T n hn
    have hc_real :
        (ArithmeticFunction.moebius n : ℝ) =
          (liouvilleLambda n : ℝ) +
            ∑ J ∈ Finset.Ico 1 (stabilizationDepthJ T), (powerLiftIncrementDelta J n : ℝ) := by
      exact_mod_cast hc
    rw [hc_real]
    ring
  refine ⟨⟨?_, ?_, ?_⟩, ⟨?_, ?_, ?_, ?_⟩, ⟨h_tele_coeff, h_tele_Q⟩, ?_, ?_⟩
  · intro J T X hJ hX
    have hd_even : Even (2 ^ J) := by
      obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le' hJ
      rw [pow_succ']
      exact ⟨2 ^ k, two_mul _⟩
    have hd_pos : 0 < 2 ^ J := Nat.pos_pow_of_pos J (by omega)
    have hd_div2 : (2 ^ J) / 2 = 2 ^ (J - 1) := by
      obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le' hJ
      simp [pow_succ']
    have h_eq_div :
        finiteQGeneral (fun n => (liouvillePowerLiftB J n : ℝ)) T X =
          finiteQGeneral (fun n => (moebiusPowerDivisorSum (2 ^ J) n : ℝ)) T X := by
      unfold finiteQGeneral
      apply Finset.sum_congr rfl
      intro n hn
      dsimp only
      rw [Finset.mem_Icc] at hn
      rw [hbJ_div J n hJ hn.1]
    have h1 :
        finiteQGeneral (fun n => (liouvillePowerLiftB J n : ℝ)) T X =
          ∑ r ∈ (Finset.Icc 1 T).filter (fun r => r ^ (2 ^ J) ≤ T),
            (1 / (((r ^ (2 ^ (J - 1))) : ℕ) : ℝ)) *
              finiteQGeneral (fun m => (ArithmeticFunction.moebius m : ℝ))
                (T / r ^ (2 ^ J)) (X / (((r ^ (2 ^ J)) : ℕ) : ℝ)) := by
      rw [h_eq_div, power_divisor_gaussian_sum_reindexing_aux hd_even hd_pos T hX, hd_div2]
    refine ⟨h1, ?_⟩
    rw [h1]
    apply Finset.sum_congr rfl
    intro r hr
    rw [Finset.mem_filter, Finset.mem_Icc] at hr
    congr 1
    have hr_pos : (0 : ℝ) < (r : ℝ) := Nat.cast_pos.mpr hr.1.1
    have hexp_eq : -(((2 ^ J : ℕ) : ℝ) / 2) = -((2 ^ (J - 1) : ℕ) : ℝ) := by
      obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le' hJ
      simp [pow_succ']
    rw [hexp_eq, Real.rpow_neg (le_of_lt hr_pos), Real.rpow_natCast, one_div]
    push_cast
    rfl
  · intro J X hJ
    constructor
    · simp [finiteQGeneral]
    · have hIcc1 : Finset.Icc 1 1 = {1} := by decide
      unfold finiteQGeneral
      rw [hIcc1, Finset.sum_singleton]
      have hb1_1 : liouvillePowerLiftB J 1 = 1 := by
        rw [hbJ_lt J 1 hJ (le_refl 1)]
        · simp
        · have hd2 : 2 ≤ 2 ^ J := by
            have : 2 ^ 1 ≤ 2 ^ J := Nat.pow_le_pow_right (by omega) hJ
            simpa using this
          have h4_le : 4 ≤ 2 ^ (2 ^ J) := by
            calc
              4 = 2 ^ 2 := by norm_num
              _ ≤ 2 ^ (2 ^ J) := Nat.pow_le_pow_right (by omega) hd2
          omega
      simp [hb1_1]
  · intro J T _
    have hz : (0 : ℝ) ^ (5 / 2 : ℝ) = 0 := Real.zero_rpow (by norm_num)
    unfold finiteQGeneral gaussianTermPhi
    simp [hz]
  · intro J n hJ hn hlt
    have hlt1 : n < 2 ^ (2 ^ (J + 1)) := by
      have hle : 2 ^ (2 ^ J) ≤ 2 ^ (2 ^ (J + 1)) :=
        Nat.pow_le_pow_right (by omega) (Nat.pow_le_pow_right (by omega) (by omega))
      omega
    unfold powerLiftIncrementDelta
    rw [hbJ_lt (J + 1) n (by omega) hn hlt1, hbJ_lt J n hJ hn hlt, sub_self]
  · intro J hJ
    have hn_pos : 1 ≤ 2 ^ (2 ^ J) := Nat.one_le_pow _ 2 (by omega)
    have hlt_next : 2 ^ (2 ^ J) < 2 ^ (2 ^ (J + 1)) := by
      apply Nat.pow_lt_pow_right (by omega : 1 < 2)
      apply Nat.pow_lt_pow_right (by omega : 1 < 2)
      omega
    unfold powerLiftIncrementDelta
    rw [hbJ_lt (J + 1) (2 ^ (2 ^ J)) (by omega) hn_pos hlt_next,
      (hbJ_bdry J hJ).1, (hbJ_bdry J hJ).2]
    norm_num
  · intro J n hJ hn
    exact powerLiftIncrementDelta_eq_neg_nonsquare_sum_aux hJ hn
  · intro J T X hJ hX
    have hd_pos : 0 < 2 ^ J := Nat.pos_pow_of_pos J (by omega)
    have hh_eq : 2 ^ (J - 1) + 2 ^ (J - 1) = 2 ^ J := by
      obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le' hJ
      simp [pow_succ', two_mul]
    rcases eq_or_lt_of_le hX with rfl | _
    · have hz : (0 : ℝ) ^ (5 / 2 : ℝ) = 0 := Real.zero_rpow (by norm_num)
      have hphi0 : ∀ m : ℕ, gaussianTermPhi m 0 = 0 := fun m => by simp [gaussianTermPhi, hz]
      unfold finiteQGeneral
      simp only [zero_div, hphi0, mul_zero, Finset.sum_const_zero, neg_zero]
    · unfold finiteQGeneral
      have h_lhs :
          ∑ n ∈ Finset.Icc 1 T, (powerLiftIncrementDelta J n : ℝ) * gaussianTermPhi n X =
            - ∑ n ∈ Finset.Icc 1 T,
                ∑ s ∈ ((Finset.Icc 2 T).filter (fun s => s ^ (2 ^ J) ≤ T ∧ ¬ IsSquare s)).filter
                    (fun s => s ^ (2 ^ J) ∣ n),
                  (ArithmeticFunction.moebius (n / s ^ (2 ^ J)) : ℝ) * gaussianTermPhi n X := by
        rw [← Finset.sum_neg_distrib]
        apply Finset.sum_congr rfl
        intro n hn
        rw [Finset.mem_Icc] at hn
        rw [powerLiftIncrementDelta_eq_neg_nonsquare_sum_aux hJ hn.1]
        push_cast
        rw [neg_mul, Finset.sum_mul]
        congr 1
        apply Finset.sum_congr
        · ext s
          simp only [powerDivisors, Finset.mem_filter, Finset.mem_Icc]
          constructor
          · rintro ⟨⟨⟨hs1, hsn⟩, hsdvd⟩, hnsq⟩
            have hs_ne1 : s ≠ 1 := fun hs_eq1 => hnsq (by subst hs_eq1; exact ⟨1, by ring⟩)
            have hsd_le : s ^ (2 ^ J) ≤ n := Nat.le_of_dvd hn.1 hsdvd
            exact ⟨⟨⟨by omega, le_trans hsn hn.2⟩, le_trans hsd_le hn.2, hnsq⟩, hsdvd⟩
          · rintro ⟨⟨⟨hs2, _⟩, _, hnsq⟩, hsdvd⟩
            have hsd_le : s ^ (2 ^ J) ≤ n := Nat.le_of_dvd hn.1 hsdvd
            have hs_le : s ≤ s ^ (2 ^ J) := Nat.le_self_pow (by omega) s
            exact ⟨⟨⟨by omega, le_trans hs_le hsd_le⟩, hsdvd⟩, hnsq⟩
        · intros; rfl
      rw [h_lhs]
      congr 1
      rw [Finset.sum_sigma']
      symm
      have h_rhs_in :
          ∑ s ∈ (Finset.Icc 2 T).filter (fun s => s ^ (2 ^ J) ≤ T ∧ ¬ IsSquare s),
              (1 / (((s ^ (2 ^ (J - 1))) : ℕ) : ℝ)) *
                ∑ m ∈ Finset.Icc 1 (T / s ^ (2 ^ J)),
                  (ArithmeticFunction.moebius m : ℝ) *
                    gaussianTermPhi m (X / (((s ^ (2 ^ J)) : ℕ) : ℝ)) =
            ∑ s ∈ (Finset.Icc 2 T).filter (fun s => s ^ (2 ^ J) ≤ T ∧ ¬ IsSquare s),
              ∑ m ∈ Finset.Icc 1 (T / s ^ (2 ^ J)),
                (ArithmeticFunction.moebius m : ℝ) * gaussianTermPhi (s ^ (2 ^ J) * m) X := by
        apply Finset.sum_congr rfl
        intro s hs
        rw [Finset.mem_filter, Finset.mem_Icc] at hs
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro m _
        have hs_pos : 0 < s := by omega
        have hsd_pos : 0 < s ^ (2 ^ J) := Nat.pow_pos hs_pos
        have hsqrt_sd : Real.sqrt (((s ^ (2 ^ J)) : ℕ) : ℝ) = (((s ^ (2 ^ (J - 1))) : ℕ) : ℝ) := by
          have hsq : s ^ (2 ^ J) = (s ^ (2 ^ (J - 1))) ^ 2 := by rw [← hh_eq, pow_add, sq]
          rw [hsq]
          push_cast
          exact Real.sqrt_sq (by positivity)
        rw [gaussianTermPhi_mul_scale_aux hsd_pos m hX, hsqrt_sd]
        ring
      rw [h_rhs_in, Finset.sum_sigma']
      apply Finset.sum_bij (fun sm _ => ⟨sm.1 ^ (2 ^ J) * sm.2, sm.1⟩)
      · rintro ⟨s, m⟩ hsm
        simp only [Finset.mem_sigma, Finset.mem_filter, Finset.mem_Icc] at hsm ⊢
        rcases hsm with ⟨⟨⟨hs2, hsT⟩, hsdT, hnsq⟩, ⟨hm1, hm_div⟩⟩
        have hsd_pos : 0 < s ^ (2 ^ J) := Nat.pow_pos (by omega)
        have h_mul_le : s ^ (2 ^ J) * m ≤ T := by
          rw [mul_comm]
          exact (Nat.le_div_iff_mul_le hsd_pos).mp hm_div
        exact ⟨⟨Nat.mul_pos hsd_pos hm1, h_mul_le⟩, ⟨⟨hs2, hsT⟩, hsdT, hnsq⟩, ⟨m, rfl⟩⟩
      · rintro ⟨s1, m1⟩ h1 ⟨s2, m2⟩ _ heq
        simp only [Finset.mem_sigma, Finset.mem_filter, Finset.mem_Icc] at h1
        have hs_eq : s1 = s2 := eq_of_heq (Sigma.mk.inj_iff.mp heq).2
        subst hs_eq
        have hprod_eq : s1 ^ (2 ^ J) * m1 = s1 ^ (2 ^ J) * m2 := (Sigma.mk.inj_iff.mp heq).1
        have hm_eq : m1 = m2 := Nat.eq_of_mul_eq_mul_left (Nat.pow_pos (by omega)) hprod_eq
        subst hm_eq
        rfl
      · rintro ⟨n, s⟩ hns
        simp only [Finset.mem_sigma, Finset.mem_filter, Finset.mem_Icc] at hns
        rcases hns with ⟨⟨hn1, hnT⟩, ⟨⟨hs2, hsT⟩, hsdT, hnsq⟩, ⟨m, rfl⟩⟩
        have hsd_pos : 0 < s ^ (2 ^ J) := Nat.pow_pos (by omega)
        have hm1 : 1 ≤ m := by
          by_contra h0
          have hm0 : m = 0 := by omega
          rw [hm0, mul_zero] at hn1
          omega
        have hm_div : m ≤ T / s ^ (2 ^ J) :=
          (Nat.le_div_iff_mul_le hsd_pos).mpr (by rw [mul_comm]; exact hnT)
        refine ⟨⟨s, m⟩, ?_, rfl⟩
        simp only [Finset.mem_sigma, Finset.mem_filter, Finset.mem_Icc]
        exact ⟨⟨⟨hs2, hsT⟩, hsdT, hnsq⟩, ⟨hm1, hm_div⟩⟩
      · rintro ⟨s, m⟩ hsm
        simp only [Finset.mem_sigma, Finset.mem_filter, Finset.mem_Icc] at hsm
        have hsd_pos : 0 < s ^ (2 ^ J) := Nat.pow_pos (by omega)
        rw [Nat.mul_div_cancel_left m hsd_pos]
  · intro u hu T
    let Q_mu := finiteQGeneral (fun n => (ArithmeticFunction.moebius n : ℝ)) T
    let Q_del := fun J => finiteQGeneral (fun n => (powerLiftIncrementDelta J n : ℝ)) T
    let I_J := Finset.Ico 1 (stabilizationDepthJ T)
    have h_pt :
        (fun X => finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) T X *
          finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) T X / X) =
        (fun X => (Q_mu X * Q_mu X / X -
            2 * (∑ J ∈ I_J, Q_mu X * Q_del J X / X)) +
          ∑ J1 ∈ I_J, ∑ J2 ∈ I_J, Q_del J1 X * Q_del J2 X / X) := by
      ext X
      rw [h_tele_Q T X]
      have h_sq :
          (Q_mu X - ∑ J ∈ I_J, Q_del J X) * (Q_mu X - ∑ J ∈ I_J, Q_del J X) =
            Q_mu X * Q_mu X - 2 * (Q_mu X * ∑ J ∈ I_J, Q_del J X) +
              (∑ J1 ∈ I_J, Q_del J1 X) * (∑ J2 ∈ I_J, Q_del J2 X) := by ring
      rw [h_sq, Finset.mul_sum, Finset.sum_mul_sum]
      simp_rw [add_div, sub_div, mul_div_assoc (2 : ℝ), Finset.sum_div]
    unfold actualWindowEnergyE windowEnergyNormSq windowPairing
    rw [h_pt]
    have h_int_mu_mu :
        IntervalIntegrable (fun X => Q_mu X * Q_mu X / X) volume u (RiemannScope.tau * u) :=
      intervalIntegrable_window_of_continuousOn_aux hu
        (continuousOn_finiteQGeneral_uIcc_aux hu (fun n => (ArithmeticFunction.moebius n : ℝ)) T)
        (continuousOn_finiteQGeneral_uIcc_aux hu (fun n => (ArithmeticFunction.moebius n : ℝ)) T)
    have h_int_mu_del : ∀ J : ℕ, IntervalIntegrable (fun X => Q_mu X * Q_del J X / X) volume u (RiemannScope.tau * u) :=
      fun J => intervalIntegrable_window_of_continuousOn_aux hu
        (continuousOn_finiteQGeneral_uIcc_aux hu (fun n => (ArithmeticFunction.moebius n : ℝ)) T)
        (continuousOn_finiteQGeneral_uIcc_aux hu (fun n => (powerLiftIncrementDelta J n : ℝ)) T)
    have h_int_del_del : ∀ J1 J2 : ℕ,
        IntervalIntegrable (fun X => Q_del J1 X * Q_del J2 X / X) volume u (RiemannScope.tau * u) :=
      fun J1 J2 => intervalIntegrable_window_of_continuousOn_aux hu
        (continuousOn_finiteQGeneral_uIcc_aux hu (fun n => (powerLiftIncrementDelta J1 n : ℝ)) T)
        (continuousOn_finiteQGeneral_uIcc_aux hu (fun n => (powerLiftIncrementDelta J2 n : ℝ)) T)
    have h_int_sum1 :
        IntervalIntegrable (fun X => ∑ J ∈ I_J, Q_mu X * Q_del J X / X) volume u (RiemannScope.tau * u) :=
      intervalIntegrable_finset_sum_fn_aux I_J (fun J _ => h_int_mu_del J)
    have h_int_sum2_inner : ∀ J1 : ℕ,
        IntervalIntegrable (fun X => ∑ J2 ∈ I_J, Q_del J1 X * Q_del J2 X / X)
          volume u (RiemannScope.tau * u) :=
      fun J1 => intervalIntegrable_finset_sum_fn_aux I_J (fun J2 _ => h_int_del_del J1 J2)
    have h_int_sum2 :
        IntervalIntegrable (fun X => ∑ J1 ∈ I_J, ∑ J2 ∈ I_J, Q_del J1 X * Q_del J2 X / X)
          volume u (RiemannScope.tau * u) :=
      intervalIntegrable_finset_sum_fn_aux I_J (fun J1 _ => h_int_sum2_inner J1)
    rw [intervalIntegral.integral_add (h_int_mu_mu.sub (h_int_sum1.const_mul 2)) h_int_sum2,
      intervalIntegral.integral_sub h_int_mu_mu (h_int_sum1.const_mul 2),
      intervalIntegral.integral_const_mul,
      intervalIntegral.integral_finset_sum (fun J _ => h_int_mu_del J),
      intervalIntegral.integral_finset_sum (fun J1 _ => h_int_sum2_inner J1)]
    congr 1
    apply Finset.sum_congr rfl
    intro J1 _
    exact intervalIntegral.integral_finset_sum (fun J2 _ => h_int_del_del J1 J2)
  · intro u _ T J1 J2 hJ1 hJ2
    obtain ⟨_, _, _, hJT_stab⟩ := hJT_props T
    have h_eq1 :
        ∀ X : ℝ,
          finiteQGeneral (fun n => (liouvillePowerLiftB J1 n : ℝ)) T X =
            finiteQGeneral (fun n => (ArithmeticFunction.moebius n : ℝ)) T X := by
      intro X
      unfold finiteQGeneral
      apply Finset.sum_congr rfl
      intro n hn
      dsimp only
      rw [hJT_stab J1 hJ1 n hn]
    have h_eq2 :
        ∀ X : ℝ,
          finiteQGeneral (fun n => (liouvillePowerLiftB J2 n : ℝ)) T X =
            finiteQGeneral (fun n => (ArithmeticFunction.moebius n : ℝ)) T X := by
      intro X
      unfold finiteQGeneral
      apply Finset.sum_congr rfl
      intro n hn
      dsimp only
      rw [hJT_stab J2 hJ2 n hn]
    refine ⟨h_eq1, ?_⟩
    have h_fun1 :
        finiteQGeneral (fun n => (liouvillePowerLiftB J1 n : ℝ)) T =
          finiteQGeneral (fun n => (ArithmeticFunction.moebius n : ℝ)) T := funext h_eq1
    have h_fun2 :
        finiteQGeneral (fun n => (liouvillePowerLiftB J2 n : ℝ)) T =
          finiteQGeneral (fun n => (ArithmeticFunction.moebius n : ℝ)) T := funext h_eq2
    rw [h_fun1, h_fun2]
    rfl

/-! ### Section 4: Primitive Coprime Pairs, Reciprocal Synthesis / Möbius Inversion, Dyadic Shells, and Separable Block Decoupling -/

/-- Ordered coprime positive-integer pairs up to `T`: `{(r, s) ∈ Icc 1 T ×ˢ Icc 1 T : gcd(r, s) = 1}`. -/
def coprimePairsUpTo (T : ℕ) : Finset (ℕ × ℕ) :=
  (Finset.Icc 1 T ×ˢ Finset.Icc 1 T).filter (fun rs => Nat.Coprime rs.1 rs.2)

/-- Primitive (`g = 1`) coprime correlation functional `Π_{a, T}(u) := ∑_{1 ≤ r, s ≤ T, gcd(r, s) = 1} a(r) a(s) K_u(r, s)`. -/
noncomputable def primitiveCoprimeSumPi (a : ℕ → ℝ) (T : ℕ) (u : ℝ) : ℝ :=
  ∑ rs ∈ coprimePairsUpTo T, a rs.1 * a rs.2 * windowKernelK u rs.1 rs.2

/-- Exact dyadic magnitude shell `B_T(j) := {1 ≤ n ≤ T : 2^j ≤ n < 2^{j + 1}}`. -/
def dyadicShellFinset (T j : ℕ) : Finset ℕ :=
  (Finset.Icc 1 T).filter (fun n => 2 ^ j ≤ n ∧ n < 2 ^ (j + 1))

/-- Primitive coprime dyadic block `B_T^{prim}(j_r, j_s) := {(r, s) ∈ B_T(j_r) ×ˢ B_T(j_s) : gcd(r, s) = 1}`. -/
def primitiveDyadicBlockPairs (T jr js : ℕ) : Finset (ℕ × ℕ) :=
  (dyadicShellFinset T jr ×ˢ dyadicShellFinset T js).filter (fun rs => Nat.Coprime rs.1 rs.2)

/-- Signed primitive dyadic block correlation `Π_{a; T, j_r, j_s}(u)`. -/
noncomputable def primitiveDyadicBlockSignedSum (a : ℕ → ℝ) (T jr js : ℕ) (u : ℝ) : ℝ :=
  ∑ rs ∈ primitiveDyadicBlockPairs T jr js, a rs.1 * a rs.2 * windowKernelK u rs.1 rs.2

/-- Unsigned primitive dyadic block correlation `Π_{|·|; T, j_r, j_s}(u) := ∑_{(r, s) ∈ B_T^{prim}(j_r, j_s)} K_u(r, s)`. -/
noncomputable def primitiveDyadicBlockUnsignedSum (T jr js : ℕ) (u : ℝ) : ℝ :=
  ∑ rs ∈ primitiveDyadicBlockPairs T jr js, windowKernelK u rs.1 rs.2

/-- Inherited quotient dyadic interval `I_d(T, j) := {1 ≤ q ≤ ⌊T / d⌋ : 2^j ≤ d * q < 2^{j + 1}}` (`d ≥ 1`). -/
def quotientDyadicShellFinset (T j d : ℕ) : Finset ℕ :=
  (Finset.Icc 1 (T / d)).filter (fun q => 2 ^ j ≤ d * q ∧ d * q < 2 ^ (j + 1))

/-- Partial Gaussian observable supported on the inherited quotient dyadic interval `I_d(T, j)`. -/
noncomputable def quotientDyadicShellQ (a : ℕ → ℝ) (T j d : ℕ) (X : ℝ) : ℝ :=
  ∑ q ∈ quotientDyadicShellFinset T j d, a q * gaussianTermPhi q X

/-- Coefficient (`m = n`, equivalently primitive pair `r = s = 1`) diagonal `D_coeff(a, T, u) := ∑_{1 ≤ m ≤ T} a(m)^2 K_u(m, m)`. -/
noncomputable def coeffDiagonalD (a : ℕ → ℝ) (T : ℕ) (u : ℝ) : ℝ :=
  ∑ m ∈ Finset.Icc 1 T, (a m) ^ 2 * windowKernelK u m m

private theorem liouvilleLambda_mul_pos_aux {m n : ℕ} (hm : 0 < m) (hn : 0 < n) :
    liouvilleLambda (m * n) = liouvilleLambda m * liouvilleLambda n := by
  have hm_ne : m ≠ 0 := ne_of_gt hm
  have hn_ne : n ≠ 0 := ne_of_gt hn
  have hmn_ne : m * n ≠ 0 := mul_ne_zero hm_ne hn_ne
  unfold liouvilleLambda liouvilleSignFromOmega natOmega
  rw [if_neg hmn_ne, if_neg hm_ne, if_neg hn_ne,
    ArithmeticFunction.cardFactors_mul hm_ne hn_ne, pow_add]

private theorem sum_divisors_moebius_real_aux (g : ℕ) :
    (∑ d ∈ g.divisors, (ArithmeticFunction.moebius d : ℝ)) = if g = 1 then 1 else 0 := by
  have h_mul_zeta :
      (ArithmeticFunction.moebius * (ArithmeticFunction.zeta : ArithmeticFunction ℤ)) g =
        (1 : ArithmeticFunction ℤ) g := by
    rw [ArithmeticFunction.moebius_mul_coe_zeta]
  rw [ArithmeticFunction.coe_mul_zeta_apply, ArithmeticFunction.one_apply] at h_mul_zeta
  have h_cast :
      (∑ d ∈ g.divisors, (ArithmeticFunction.moebius d : ℝ)) =
        ((∑ d ∈ g.divisors, ArithmeticFunction.moebius d : ℤ) : ℝ) := by
    push_cast; rfl
  rw [h_cast, h_mul_zeta]
  split_ifs <;> norm_num

/-- **Theorem 4 (`TASK-TC-059` §3 & §4B, Ordered Primitive-Pair Expansion, Reciprocal Synthesis / Möbius Inversion, Coefficient-Diagonal Comparison, Dyadic Shell Partition, and Separable Block Decoupling)**:
    *Formal scope (`CONCRETE_ANALYTIC_IN_LEAN` & `UNCONDITIONAL_FINITE_ARITHMETIC`)*:
    1. Common-factor Liouville sign cancellation (`g, r, s ≥ 1`):
       `liouvilleLambda (g * r) * liouvilleLambda (g * s) = liouvilleLambda (r * s) ∧ (liouvilleLambda g) ^ 2 = 1`;
    2. Exact ordered positive-integer primitive-pair expansion (`0 < u`, `T : ℕ`) for any completely multiplicative
       `a : ℕ → ℝ` with `∀ g ≥ 1, (a g) ^ 2 = 1` and specialized to `liouvilleLambda`:
       `actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) T u = ∑ rs ∈ coprimePairsUpTo T, (liouvilleLambda (rs.1 * rs.2) : ℝ) * ∑ g ∈ Finset.Icc 1 (T / max rs.1 rs.2), (1 / (g : ℝ)) * windowKernelK (u / (g : ℝ)) rs.1 rs.2`;
    3. Exact finite reciprocal synthesis and Möbius inversion (`0 < u`, `T : ℕ`) between `actualWindowEnergyE` and
       the `g = 1` primitive coprime correlation functional `primitiveCoprimeSumPi`:
       - `actualWindowEnergyE a T u = ∑ g ∈ Finset.Icc 1 T, (1 / (g : ℝ)) * primitiveCoprimeSumPi a (T / g) (u / (g : ℝ))`;
       - `primitiveCoprimeSumPi a T u = ∑ d ∈ Finset.Icc 1 T, ((ArithmeticFunction.moebius d : ℝ) / (d : ℝ)) * actualWindowEnergyE a (T / d) (u / (d : ℝ))`;
    4. Coefficient-diagonal (`m = n` ↔ primitive pair `r = s = 1`) comparison (`0 < u`, `T : ℕ`):
       - `0 ≤ coeffDiagonalD a T u`;
       - `(∀ m ≥ 1, (a m) ^ 2 = 1) → coeffDiagonalD a T u = ∑ g ∈ Finset.Icc 1 T, (1 / (g : ℝ)) * windowKernelK (u / (g : ℝ)) 1 1`;
       - `(∀ m ≥ 1, (a m) ^ 2 = 1) → ∑ d ∈ Finset.Icc 1 T, ((ArithmeticFunction.moebius d : ℝ) / (d : ℝ)) * coeffDiagonalD a (T / d) (u / (d : ℝ)) = if 1 ≤ T then windowKernelK u 1 1 else 0`;
    5. Exact dyadic magnitude-shell partition (`dyadicShellFinset T j`), unsigned block majorant, and exact separable
       window-pairing Möbius decoupling on each primitive dyadic block `(jr, js)` (`0 < u`, `T jr js : ℕ`):
       - Pairwise disjointness `j1 ≠ j2 → Disjoint (dyadicShellFinset T j1) (dyadicShellFinset T j2)` and exact union
         `(Finset.range (Nat.log 2 T + 1)).biUnion (dyadicShellFinset T) = Finset.Icc 1 T`;
       - `primitiveCoprimeSumPi a T u = ∑ jr ∈ Finset.range (Nat.log 2 T + 1), ∑ js ∈ Finset.range (Nat.log 2 T + 1), primitiveDyadicBlockSignedSum a T jr js u`;
       - `(∀ n ≥ 1, |a n| ≤ 1) → |primitiveDyadicBlockSignedSum a T jr js u| ≤ primitiveDyadicBlockUnsignedSum T jr js u`;
       - Under complete multiplicativity and `∀ d ≥ 1, (a d) ^ 2 = 1`,
         `primitiveDyadicBlockSignedSum a T jr js u = ∑ d ∈ Finset.Icc 1 T, ((ArithmeticFunction.moebius d : ℝ) / (d : ℝ)) * windowPairing (u / (d : ℝ)) (quotientDyadicShellQ a T jr d) (quotientDyadicShellQ a T js d)`. -/
theorem primitive_coprime_expansion_moebius_inversion_and_dyadic_block_tc059 :
    (∀ g r s : ℕ, 1 ≤ g → 1 ≤ r → 1 ≤ s →
      liouvilleLambda (g * r) * liouvilleLambda (g * s) = liouvilleLambda (r * s) ∧
        (liouvilleLambda g) ^ 2 = 1) ∧
    (∀ {u : ℝ}, 0 < u → ∀ T : ℕ,
      (∀ (a : ℕ → ℝ),
        (∀ d q : ℕ, 0 < d → 0 < q → a (d * q) = a d * a q) →
        (∀ g : ℕ, 1 ≤ g → (a g) ^ 2 = 1) →
        actualWindowEnergyE a T u =
          ∑ rs ∈ coprimePairsUpTo T,
            a rs.1 * a rs.2 *
              ∑ g ∈ Finset.Icc 1 (T / max rs.1 rs.2),
                (1 / (g : ℝ)) * windowKernelK (u / (g : ℝ)) rs.1 rs.2) ∧
      actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) T u =
        ∑ rs ∈ coprimePairsUpTo T,
          (liouvilleLambda (rs.1 * rs.2) : ℝ) *
            ∑ g ∈ Finset.Icc 1 (T / max rs.1 rs.2),
              (1 / (g : ℝ)) * windowKernelK (u / (g : ℝ)) rs.1 rs.2) ∧
    (∀ {u : ℝ}, 0 < u → ∀ (T : ℕ) (a : ℕ → ℝ),
      (∀ d q : ℕ, 0 < d → 0 < q → a (d * q) = a d * a q) →
      (∀ g : ℕ, 1 ≤ g → (a g) ^ 2 = 1) →
      actualWindowEnergyE a T u =
          (∑ g ∈ Finset.Icc 1 T,
            (1 / (g : ℝ)) * primitiveCoprimeSumPi a (T / g) (u / (g : ℝ))) ∧
        primitiveCoprimeSumPi a T u =
          ∑ d ∈ Finset.Icc 1 T,
            ((ArithmeticFunction.moebius d : ℝ) / (d : ℝ)) *
              actualWindowEnergyE a (T / d) (u / (d : ℝ))) ∧
    (∀ {u : ℝ}, 0 < u → ∀ (T : ℕ) (a : ℕ → ℝ),
      0 ≤ coeffDiagonalD a T u ∧
      ((∀ m : ℕ, 1 ≤ m → (a m) ^ 2 = 1) →
        coeffDiagonalD a T u =
            (∑ g ∈ Finset.Icc 1 T, (1 / (g : ℝ)) * windowKernelK (u / (g : ℝ)) 1 1) ∧
          (∑ d ∈ Finset.Icc 1 T,
              ((ArithmeticFunction.moebius d : ℝ) / (d : ℝ)) *
                coeffDiagonalD a (T / d) (u / (d : ℝ))) =
            if 1 ≤ T then windowKernelK u 1 1 else 0)) ∧
    ((∀ (T j1 j2 : ℕ), j1 ≠ j2 → Disjoint (dyadicShellFinset T j1) (dyadicShellFinset T j2)) ∧
      (∀ T : ℕ, (Finset.range (Nat.log 2 T + 1)).biUnion (dyadicShellFinset T) = Finset.Icc 1 T) ∧
      (∀ {u : ℝ}, 0 < u → ∀ (T : ℕ) (a : ℕ → ℝ),
        primitiveCoprimeSumPi a T u =
          ∑ jr ∈ Finset.range (Nat.log 2 T + 1),
            ∑ js ∈ Finset.range (Nat.log 2 T + 1),
              primitiveDyadicBlockSignedSum a T jr js u) ∧
      (∀ {u : ℝ}, 0 < u → ∀ (T jr js : ℕ) (a : ℕ → ℝ),
        (∀ n : ℕ, 1 ≤ n → |a n| ≤ 1) →
        |primitiveDyadicBlockSignedSum a T jr js u| ≤
          primitiveDyadicBlockUnsignedSum T jr js u) ∧
      (∀ {u : ℝ}, 0 < u → ∀ (T jr js : ℕ) (a : ℕ → ℝ),
        (∀ d q : ℕ, 0 < d → 0 < q → a (d * q) = a d * a q) →
        (∀ d : ℕ, 1 ≤ d → (a d) ^ 2 = 1) →
        primitiveDyadicBlockSignedSum a T jr js u =
          ∑ d ∈ Finset.Icc 1 T,
            ((ArithmeticFunction.moebius d : ℝ) / (d : ℝ)) *
              windowPairing (u / (d : ℝ))
                (quotientDyadicShellQ a T jr d) (quotientDyadicShellQ a T js d))) := by
  have h_lam_sq : ∀ g : ℕ, 1 ≤ g → (liouvilleLambda g) ^ 2 = 1 := by
    intro g hg
    have hg_ne : g ≠ 0 := by omega
    unfold liouvilleLambda liouvilleSignFromOmega
    rw [if_neg hg_ne, sq, ← pow_add]
    have h2 : natOmega g + natOmega g = 2 * natOmega g := by omega
    rw [h2, pow_mul]
    norm_num
  have h_prim_gen :
      ∀ {u : ℝ}, 0 < u → ∀ (T : ℕ) (a : ℕ → ℝ),
        (∀ d q : ℕ, 0 < d → 0 < q → a (d * q) = a d * a q) →
        (∀ g : ℕ, 1 ≤ g → (a g) ^ 2 = 1) →
        actualWindowEnergyE a T u =
          ∑ rs ∈ coprimePairsUpTo T,
            a rs.1 * a rs.2 *
              ∑ g ∈ Finset.Icc 1 (T / max rs.1 rs.2),
                (1 / (g : ℝ)) * windowKernelK (u / (g : ℝ)) rs.1 rs.2 := by
    intro u hu T a ha_mult ha_sq
    obtain ⟨_, _, _, hK_scale, h_bilin⟩ := window_integrability_and_kernel_scaling_tc059 hu
    unfold actualWindowEnergyE windowEnergyNormSq
    rw [h_bilin T a a, ← Finset.sum_product']
    have h_rhs_sigma :
        (∑ rs ∈ coprimePairsUpTo T,
            a rs.1 * a rs.2 *
              ∑ g ∈ Finset.Icc 1 (T / max rs.1 rs.2),
                (1 / (g : ℝ)) * windowKernelK (u / (g : ℝ)) rs.1 rs.2) =
          ∑ x ∈ (coprimePairsUpTo T).sigma (fun rs => Finset.Icc 1 (T / max rs.1 rs.2)),
            a x.1.1 * a x.1.2 * ((1 / (x.2 : ℝ)) * windowKernelK (u / (x.2 : ℝ)) x.1.1 x.1.2) := by
      simp_rw [Finset.mul_sum]
      rw [Finset.sum_sigma']
    rw [h_rhs_sigma]
    symm
    apply Finset.sum_bij (fun x _ => (x.2 * x.1.1, x.2 * x.1.2))
    · rintro ⟨⟨r, s⟩, g⟩ hx
      simp only [Finset.mem_sigma, coprimePairsUpTo, Finset.mem_filter, Finset.mem_product,
        Finset.mem_Icc] at hx ⊢
      rcases hx with ⟨⟨⟨⟨hr1, _⟩, ⟨hs1, _⟩⟩, _⟩, ⟨hg1, hg_le⟩⟩
      have hmax_pos : 0 < max r s := lt_of_lt_of_le (by omega : 0 < r) (le_max_left r s)
      have hg_max : g * max r s ≤ T := (Nat.le_div_iff_mul_le hmax_pos).mp hg_le
      have hgr_le : g * r ≤ T := le_trans (Nat.mul_le_mul_left g (le_max_left r s)) hg_max
      have hgs_le : g * s ≤ T := le_trans (Nat.mul_le_mul_left g (le_max_right r s)) hg_max
      exact ⟨⟨Nat.mul_pos hg1 hr1, hgr_le⟩, ⟨Nat.mul_pos hg1 hs1, hgs_le⟩⟩
    · rintro ⟨⟨r1, s1⟩, g1⟩ h1 ⟨⟨r2, s2⟩, g2⟩ h2 heq
      simp only [Finset.mem_sigma, coprimePairsUpTo, Finset.mem_filter, Finset.mem_product,
        Finset.mem_Icc] at h1 h2
      injection heq with heq_r heq_s
      have h_gcd1 : Nat.gcd (g1 * r1) (g1 * s1) = g1 := by
        rw [Nat.gcd_mul_left, h1.1.2, mul_one]
      have h_gcd2 : Nat.gcd (g2 * r2) (g2 * s2) = g2 := by
        rw [Nat.gcd_mul_left, h2.1.2, mul_one]
      have hg_eq : g1 = g2 := by rw [← h_gcd1, heq_r, heq_s, h_gcd2]
      subst hg_eq
      have hg1_pos : 0 < g1 := h1.2.1
      have hr_eq : r1 = r2 := Nat.eq_of_mul_eq_mul_left hg1_pos heq_r
      have hs_eq : s1 = s2 := Nat.eq_of_mul_eq_mul_left hg1_pos heq_s
      subst hr_eq; subst hs_eq; rfl
    · rintro ⟨m, n⟩ hmn
      simp only [Finset.mem_product, Finset.mem_Icc] at hmn
      rcases hmn with ⟨⟨hm1, hmT⟩, ⟨hn1, hnT⟩⟩
      let g := Nat.gcd m n
      have hg_pos : 0 < g := Nat.gcd_pos_of_pos_left n hm1
      let r := m / g
      let s := n / g
      have hgr : g * r = m := Nat.mul_div_cancel' (Nat.gcd_dvd_left m n)
      have hgs : g * s = n := Nat.mul_div_cancel' (Nat.gcd_dvd_right m n)
      have hr_pos : 1 ≤ r := Nat.div_pos (Nat.le_of_dvd hm1 (Nat.gcd_dvd_left m n)) hg_pos
      have hs_pos : 1 ≤ s := Nat.div_pos (Nat.le_of_dvd hn1 (Nat.gcd_dvd_right m n)) hg_pos
      have hr_le : r ≤ T := le_trans (Nat.div_le_self m g) hmT
      have hs_le : s ≤ T := le_trans (Nat.div_le_self n g) hnT
      have hcop : Nat.Coprime r s := Nat.coprime_div_gcd_div_gcd hg_pos
      have hg_max_le : g * max r s ≤ T := by
        rcases max_choice r s with hmax | hmax <;> rw [hmax]
        · rw [hgr]; exact hmT
        · rw [hgs]; exact hnT
      have hmax_pos : 0 < max r s := lt_of_lt_of_le hr_pos (le_max_left r s)
      have hg_le_div : g ≤ T / max r s := (Nat.le_div_iff_mul_le hmax_pos).mpr hg_max_le
      refine ⟨⟨(r, s), g⟩, ?_, Prod.ext hgr hgs⟩
      simp only [Finset.mem_sigma, coprimePairsUpTo, Finset.mem_filter, Finset.mem_product,
        Finset.mem_Icc]
      exact ⟨⟨⟨⟨hr_pos, hr_le⟩, ⟨hs_pos, hs_le⟩⟩, hcop⟩, ⟨hg_pos, hg_le_div⟩⟩
    · rintro ⟨⟨r, s⟩, g⟩ hx
      simp only [Finset.mem_sigma, coprimePairsUpTo, Finset.mem_filter, Finset.mem_product,
        Finset.mem_Icc] at hx
      rcases hx with ⟨⟨⟨⟨hr1, _⟩, ⟨hs1, _⟩⟩, _⟩, ⟨hg1, _⟩⟩
      rw [ha_mult g r hg1 hr1, ha_mult g s hg1 hs1, hK_scale hg1 r s]
      calc
        a r * a s * (1 / (g : ℝ) * windowKernelK (u / (g : ℝ)) r s)
          = 1 * (a r * a s) * (1 / (g : ℝ) * windowKernelK (u / (g : ℝ)) r s) := by ring
        _ = (a g) ^ 2 * (a r * a s) * (1 / (g : ℝ) * windowKernelK (u / (g : ℝ)) r s) := by
              rw [ha_sq g hg1]
        _ = a g * a r * (a g * a s) * (1 / (g : ℝ) * windowKernelK (u / (g : ℝ)) r s) := by ring
  have h_synth_gen :
      ∀ {u : ℝ}, 0 < u → ∀ (T : ℕ) (a : ℕ → ℝ),
        (∀ d q : ℕ, 0 < d → 0 < q → a (d * q) = a d * a q) →
        (∀ g : ℕ, 1 ≤ g → (a g) ^ 2 = 1) →
        actualWindowEnergyE a T u =
          ∑ g ∈ Finset.Icc 1 T,
            (1 / (g : ℝ)) * primitiveCoprimeSumPi a (T / g) (u / (g : ℝ)) := by
    intro u hu T a ha_mult ha_sq
    rw [h_prim_gen hu T a ha_mult ha_sq]
    have h_extend :
        (∑ rs ∈ coprimePairsUpTo T,
            a rs.1 * a rs.2 *
              ∑ g ∈ Finset.Icc 1 (T / max rs.1 rs.2),
                (1 / (g : ℝ)) * windowKernelK (u / (g : ℝ)) rs.1 rs.2) =
          ∑ rs ∈ coprimePairsUpTo T,
            ∑ g ∈ Finset.Icc 1 T,
              if g ≤ T / max rs.1 rs.2 then
                a rs.1 * a rs.2 * ((1 / (g : ℝ)) * windowKernelK (u / (g : ℝ)) rs.1 rs.2)
              else 0 := by
      apply Finset.sum_congr rfl
      intro rs hrs
      simp only [coprimePairsUpTo, Finset.mem_filter, Finset.mem_product, Finset.mem_Icc] at hrs
      rw [Finset.mul_sum, ← Finset.sum_filter]
      apply Finset.sum_congr
      · ext g
        simp only [Finset.mem_Icc, Finset.mem_filter]
        constructor
        · rintro ⟨hg1, hg_le⟩
          exact ⟨⟨hg1, le_trans hg_le (Nat.div_le_self T _)⟩, hg_le⟩
        · rintro ⟨⟨hg1, _⟩, hg_le⟩
          exact ⟨hg1, hg_le⟩
      · intros; rfl
    rw [h_extend, Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro g hg
    rw [Finset.mem_Icc] at hg
    unfold primitiveCoprimeSumPi
    rw [Finset.mul_sum, ← Finset.sum_filter]
    have h_set_eq :
        (coprimePairsUpTo T).filter (fun rs => g ≤ T / max rs.1 rs.2) =
          coprimePairsUpTo (T / g) := by
      ext ⟨r, s⟩
      simp only [coprimePairsUpTo, Finset.mem_filter, Finset.mem_product, Finset.mem_Icc]
      constructor
      · rintro ⟨⟨⟨⟨hr1, _⟩, ⟨hs1, _⟩⟩, hcop⟩, hg_le⟩
        have hmax_pos : 0 < max r s := lt_of_lt_of_le hr1 (le_max_left r s)
        have hprod_le : g * max r s ≤ T := (Nat.le_div_iff_mul_le hmax_pos).mp hg_le
        have hmax_le_div : max r s ≤ T / g :=
          (Nat.le_div_iff_mul_le hg.1).mpr (by rwa [mul_comm])
        exact ⟨⟨⟨hr1, le_trans (le_max_left r s) hmax_le_div⟩,
          ⟨hs1, le_trans (le_max_right r s) hmax_le_div⟩⟩, hcop⟩
      · rintro ⟨⟨⟨hr1, hr_div⟩, ⟨hs1, hs_div⟩⟩, hcop⟩
        have hmax_pos : 0 < max r s := lt_of_lt_of_le hr1 (le_max_left r s)
        have hmax_div : max r s ≤ T / g := max_le hr_div hs_div
        have hprod_le : max r s * g ≤ T := (Nat.le_div_iff_mul_le hg.1).mp hmax_div
        have hg_le : g ≤ T / max r s :=
          (Nat.le_div_iff_mul_le hmax_pos).mpr (by rwa [mul_comm])
        exact ⟨⟨⟨⟨hr1, le_trans hr_div (Nat.div_le_self T g)⟩,
          ⟨hs1, le_trans hs_div (Nat.div_le_self T g)⟩⟩, hcop⟩, hg_le⟩
    rw [h_set_eq]
    apply Finset.sum_congr rfl
    intro rs _
    ring
  have h_moebius_inv_scale :
      ∀ (F G : ℕ → ℝ → ℝ),
        (∀ {w : ℝ}, 0 < w → ∀ L : ℕ,
          F L w = ∑ k ∈ Finset.Icc 1 L, (1 / (k : ℝ)) * G (L / k) (w / (k : ℝ))) →
        ∀ {u : ℝ}, 0 < u → ∀ T : ℕ,
          (∑ d ∈ Finset.Icc 1 T,
              ((ArithmeticFunction.moebius d : ℝ) / (d : ℝ)) * F (T / d) (u / (d : ℝ))) =
            if 1 ≤ T then G T u else 0 := by
    intro F G hFG u hu T
    have h_sub :
        (∑ d ∈ Finset.Icc 1 T,
            ((ArithmeticFunction.moebius d : ℝ) / (d : ℝ)) * F (T / d) (u / (d : ℝ))) =
          ∑ x ∈ (Finset.Icc 1 T).sigma (fun d => Finset.Icc 1 (T / d)),
            (ArithmeticFunction.moebius x.1 : ℝ) *
              ((1 / ((x.1 * x.2 : ℕ) : ℝ)) *
                G (T / (x.1 * x.2)) (u / ((x.1 * x.2 : ℕ) : ℝ))) := by
      have h_inner_sub :
          ∀ d ∈ Finset.Icc 1 T,
            ((ArithmeticFunction.moebius d : ℝ) / (d : ℝ)) * F (T / d) (u / (d : ℝ)) =
              ∑ k ∈ Finset.Icc 1 (T / d),
                (ArithmeticFunction.moebius d : ℝ) *
                  ((1 / ((d * k : ℕ) : ℝ)) *
                    G (T / (d * k)) (u / ((d * k : ℕ) : ℝ))) := by
        intro d hd
        rw [Finset.mem_Icc] at hd
        have hd_pos : (0 : ℝ) < (d : ℝ) := Nat.cast_pos.mpr hd.1
        rw [hFG (div_pos hu hd_pos) (T / d), Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro k _
        rw [Nat.div_div_eq_div_mul, div_div]
        push_cast
        ring
      rw [Finset.sum_congr rfl h_inner_sub, Finset.sum_sigma']
    rw [h_sub]
    have h_bij :
        (∑ x ∈ (Finset.Icc 1 T).sigma (fun d => Finset.Icc 1 (T / d)),
            (ArithmeticFunction.moebius x.1 : ℝ) *
              ((1 / ((x.1 * x.2 : ℕ) : ℝ)) *
                G (T / (x.1 * x.2)) (u / ((x.1 * x.2 : ℕ) : ℝ)))) =
          ∑ y ∈ (Finset.Icc 1 T).sigma (fun g => g.divisors),
            (ArithmeticFunction.moebius y.2 : ℝ) *
              ((1 / (y.1 : ℝ)) * G (T / y.1) (u / (y.1 : ℝ))) := by
      apply Finset.sum_bij (fun x _ => ⟨x.1 * x.2, x.1⟩)
      · rintro ⟨d, k⟩ hx
        simp only [Finset.mem_sigma, Finset.mem_Icc, Nat.mem_divisors] at hx ⊢
        rcases hx with ⟨⟨hd1, _⟩, ⟨hk1, hk_div⟩⟩
        have hdk_le : d * k ≤ T := by
          rw [mul_comm]
          exact (Nat.le_div_iff_mul_le hd1).mp hk_div
        have hdk_pos : 0 < d * k := Nat.mul_pos hd1 hk1
        exact ⟨⟨hdk_pos, hdk_le⟩, ⟨⟨k, rfl⟩, ne_of_gt hdk_pos⟩⟩
      · rintro ⟨d1, k1⟩ h1 ⟨d2, k2⟩ h2 heq
        simp only [Finset.mem_sigma, Finset.mem_Icc] at h1 h2
        have h_fst : d1 * k1 = d2 * k2 := congrArg Sigma.fst heq
        have hd_eq : d1 = d2 := by
          have h_snd : (⟨d1 * k1, d1⟩ : Σ _ : ℕ, ℕ).2 = (⟨d2 * k2, d2⟩ : Σ _ : ℕ, ℕ).2 :=
            congrArg Sigma.snd heq
          exact h_snd
        subst hd_eq
        have hk_eq : k1 = k2 := Nat.eq_of_mul_eq_mul_left h1.1.1 h_fst
        subst hk_eq; rfl
      · rintro ⟨g, d⟩ hy
        simp only [Finset.mem_sigma, Finset.mem_Icc, Nat.mem_divisors] at hy
        rcases hy with ⟨⟨hg1, hgT⟩, ⟨hdvd, _⟩⟩
        have hd_pos : 1 ≤ d := Nat.pos_of_dvd_of_pos hdvd hg1
        have hd_le : d ≤ T := le_trans (Nat.le_of_dvd hg1 hdvd) hgT
        let k := g / d
        have hdk : d * k = g := Nat.mul_div_cancel' hdvd
        have hk_pos : 1 ≤ k := Nat.div_pos (Nat.le_of_dvd hg1 hdvd) hd_pos
        have hk_div : k ≤ T / d :=
          (Nat.le_div_iff_mul_le hd_pos).mpr (by rw [mul_comm, hdk]; exact hgT)
        refine ⟨⟨d, k⟩, ?_, by dsimp only; rw [hdk]⟩
        simp only [Finset.mem_sigma, Finset.mem_Icc]
        exact ⟨⟨hd_pos, hd_le⟩, ⟨hk_pos, hk_div⟩⟩
      · rintro ⟨d, k⟩ _; rfl
    rw [h_bij, Finset.sum_sigma]
    have h_collapse :
        ∀ g ∈ Finset.Icc 1 T,
          (∑ d ∈ g.divisors,
              (ArithmeticFunction.moebius d : ℝ) *
                ((1 / (g : ℝ)) * G (T / g) (u / (g : ℝ)))) =
            if g = 1 then G T u else 0 := by
      intro g _
      rw [← Finset.sum_mul, sum_divisors_moebius_real_aux g]
      by_cases hg1 : g = 1
      · subst hg1; simp
      · simp [hg1]
    rw [Finset.sum_congr rfl h_collapse]
    by_cases hT : 1 ≤ T
    · have h1_mem : (1 : ℕ) ∈ Finset.Icc 1 T := Finset.mem_Icc.mpr ⟨le_refl 1, hT⟩
      rw [Finset.sum_ite_eq' (Finset.Icc 1 T) 1 (fun _ => G T u), if_pos h1_mem, if_pos hT]
    · have hT0 : T = 0 := by omega
      subst hT0
      simp
  have h_shell_disj :
      ∀ (T j1 j2 : ℕ), j1 ≠ j2 → Disjoint (dyadicShellFinset T j1) (dyadicShellFinset T j2) := by
    intro T j1 j2 hne
    rw [Finset.disjoint_left]
    intro n hn1 hn2
    simp only [dyadicShellFinset, Finset.mem_filter, Finset.mem_Icc] at hn1 hn2
    rcases lt_trichotomy j1 j2 with hlt | rfl | hgt
    · have hle : 2 ^ (j1 + 1) ≤ 2 ^ j2 := Nat.pow_le_pow_right (by omega) (by omega)
      omega
    · exact hne rfl
    · have hle : 2 ^ (j2 + 1) ≤ 2 ^ j1 := Nat.pow_le_pow_right (by omega) (by omega)
      omega
  have h_shell_union :
      ∀ T : ℕ, (Finset.range (Nat.log 2 T + 1)).biUnion (dyadicShellFinset T) = Finset.Icc 1 T := by
    intro T
    ext n
    simp only [Finset.mem_biUnion, Finset.mem_range, dyadicShellFinset, Finset.mem_filter,
      Finset.mem_Icc]
    constructor
    · rintro ⟨_, _, ⟨hn1, hnT⟩, _⟩
      exact ⟨hn1, hnT⟩
    · rintro ⟨hn1, hnT⟩
      let j := Nat.log 2 n
      have hj_le : j ≤ Nat.log 2 T := Nat.log_mono_right hnT
      have h_lo : 2 ^ j ≤ n := Nat.pow_log_le_self 2 (by omega)
      have h_hi : n < 2 ^ (j + 1) := Nat.lt_pow_succ_log_self (by omega : 1 < 2) n
      exact ⟨j, by omega, ⟨hn1, hnT⟩, h_lo, h_hi⟩
  refine ⟨?_, ?_, ?_, ?_, ⟨h_shell_disj, h_shell_union, ?_, ?_, ?_⟩⟩
  · intro g r s hg hr hs
    refine ⟨?_, h_lam_sq g hg⟩
    rw [liouvilleLambda_mul_pos_aux hg hr, liouvilleLambda_mul_pos_aux hg hs,
      liouvilleLambda_mul_pos_aux hr hs]
    calc
      (liouvilleLambda g * liouvilleLambda r) * (liouvilleLambda g * liouvilleLambda s)
        = (liouvilleLambda g) ^ 2 * (liouvilleLambda r * liouvilleLambda s) := by ring
      _ = liouvilleLambda r * liouvilleLambda s := by rw [h_lam_sq g hg, one_mul]
  · intro u hu T
    refine ⟨fun a ha_mult ha_sq => h_prim_gen hu T a ha_mult ha_sq, ?_⟩
    have h_lam_mult_r :
        ∀ d q : ℕ, 0 < d → 0 < q →
          (liouvilleLambda (d * q) : ℝ) = (liouvilleLambda d : ℝ) * (liouvilleLambda q : ℝ) := by
      intro d q hd hq
      exact_mod_cast liouvilleLambda_mul_pos_aux hd hq
    have h_lam_sq_r : ∀ g : ℕ, 1 ≤ g → ((liouvilleLambda g : ℝ)) ^ 2 = 1 := by
      intro g hg
      exact_mod_cast h_lam_sq g hg
    rw [h_prim_gen hu T (fun n => (liouvilleLambda n : ℝ)) h_lam_mult_r h_lam_sq_r]
    apply Finset.sum_congr rfl
    intro rs hrs
    simp only [coprimePairsUpTo, Finset.mem_filter, Finset.mem_product, Finset.mem_Icc] at hrs
    rw [← h_lam_mult_r rs.1 rs.2 hrs.1.1.1 hrs.1.2.1]
  · intro u hu T a ha_mult ha_sq
    refine ⟨h_synth_gen hu T a ha_mult ha_sq, ?_⟩
    have h_inv := h_moebius_inv_scale
      (fun L w => actualWindowEnergyE a L w)
      (fun L w => primitiveCoprimeSumPi a L w)
      (fun hw L => h_synth_gen hw L a ha_mult ha_sq) hu T
    rw [h_inv]
    by_cases hT : 1 ≤ T
    · rw [if_pos hT]
    · have hT0 : T = 0 := by omega
      subst hT0
      simp [primitiveCoprimeSumPi, coprimePairsUpTo]
  · intro u hu T a
    obtain ⟨_, hK_props, _, _, _⟩ := window_integrability_and_kernel_scaling_tc059 hu
    have h_nn : 0 ≤ coeffDiagonalD a T u := by
      unfold coeffDiagonalD
      apply Finset.sum_nonneg
      intro m _
      exact mul_nonneg (sq_nonneg _) (hK_props m m).2
    refine ⟨h_nn, ?_⟩
    intro ha_sq
    have h_diag_eq :
        ∀ {w : ℝ}, 0 < w → ∀ L : ℕ,
          coeffDiagonalD a L w =
            ∑ g ∈ Finset.Icc 1 L, (1 / (g : ℝ)) * windowKernelK (w / (g : ℝ)) 1 1 := by
      intro w hw L
      obtain ⟨_, _, _, hK_sc_w, _⟩ := window_integrability_and_kernel_scaling_tc059 hw
      unfold coeffDiagonalD
      apply Finset.sum_congr rfl
      intro g hg
      rw [Finset.mem_Icc] at hg
      have hg1 : g * 1 = g := mul_one g
      rw [ha_sq g hg.1, one_mul, ← hg1, hK_sc_w hg.1 1 1, hg1]
    refine ⟨h_diag_eq hu T, ?_⟩
    exact h_moebius_inv_scale
      (fun L w => coeffDiagonalD a L w)
      (fun _ w => windowKernelK w 1 1)
      (fun hw L => h_diag_eq hw L) hu T
  · intro u _ T a
    let R := Finset.range (Nat.log 2 T + 1)
    have h_prod_union :
        (R ×ˢ R).biUnion (fun jj => dyadicShellFinset T jj.1 ×ˢ dyadicShellFinset T jj.2) =
          Finset.Icc 1 T ×ˢ Finset.Icc 1 T := by
      ext ⟨r, s⟩
      simp only [Finset.mem_biUnion, Finset.mem_product, ← h_shell_union T]
      constructor
      · rintro ⟨⟨jr, js⟩, ⟨hjr, hjs⟩, hr, hs⟩
        exact ⟨⟨jr, hjr, hr⟩, ⟨js, hjs, hs⟩⟩
      · rintro ⟨⟨jr, hjr, hr⟩, ⟨js, hjs, hs⟩⟩
        exact ⟨(jr, js), ⟨hjr, hjs⟩, hr, hs⟩
    have h_cop_union :
        (R ×ˢ R).biUnion (fun jj => primitiveDyadicBlockPairs T jj.1 jj.2) =
          coprimePairsUpTo T := by
      ext ⟨r, s⟩
      simp only [Finset.mem_biUnion, primitiveDyadicBlockPairs, coprimePairsUpTo,
        Finset.mem_filter, ← h_prod_union]
      constructor
      · rintro ⟨jj, hjj, hrs, hcop⟩
        exact ⟨⟨jj, hjj, hrs⟩, hcop⟩
      · rintro ⟨⟨jj, hjj, hrs⟩, hcop⟩
        exact ⟨jj, hjj, hrs, hcop⟩
    have h_cop_disj :
        ((R ×ˢ R : Finset (ℕ × ℕ)) : Set (ℕ × ℕ)).PairwiseDisjoint
          (fun jj => primitiveDyadicBlockPairs T jj.1 jj.2) := by
      intro ⟨j1, k1⟩ _ ⟨j2, k2⟩ _ hne
      change Disjoint (primitiveDyadicBlockPairs T j1 k1) (primitiveDyadicBlockPairs T j2 k2)
      rw [Finset.disjoint_left]
      rintro ⟨r, s⟩ h1 h2
      simp only [primitiveDyadicBlockPairs, Finset.mem_filter, Finset.mem_product] at h1 h2
      by_cases hj : j1 = j2
      · subst hj
        have hk : k1 ≠ k2 := fun hk_eq => hne (Prod.ext rfl hk_eq)
        exact Finset.disjoint_left.mp (h_shell_disj T k1 k2 hk) h1.1.2 h2.1.2
      · exact Finset.disjoint_left.mp (h_shell_disj T j1 j2 hj) h1.1.1 h2.1.1
    unfold primitiveCoprimeSumPi primitiveDyadicBlockSignedSum
    rw [← h_cop_union, Finset.sum_biUnion h_cop_disj, Finset.sum_product]
  · intro u hu T jr js a ha_abs
    obtain ⟨_, hK_props, _, _, _⟩ := window_integrability_and_kernel_scaling_tc059 hu
    unfold primitiveDyadicBlockSignedSum primitiveDyadicBlockUnsignedSum
    calc
      |∑ rs ∈ primitiveDyadicBlockPairs T jr js, a rs.1 * a rs.2 * windowKernelK u rs.1 rs.2|
        ≤ ∑ rs ∈ primitiveDyadicBlockPairs T jr js,
            |a rs.1 * a rs.2 * windowKernelK u rs.1 rs.2| :=
          Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ rs ∈ primitiveDyadicBlockPairs T jr js, windowKernelK u rs.1 rs.2 := by
          apply Finset.sum_le_sum
          rintro ⟨r, s⟩ hrs
          simp only [primitiveDyadicBlockPairs, dyadicShellFinset, Finset.mem_filter,
            Finset.mem_product, Finset.mem_Icc] at hrs
          have hK_nn : 0 ≤ windowKernelK u r s := (hK_props r s).2
          rw [abs_mul, abs_mul, abs_of_nonneg hK_nn]
          have h1 : |a r| * |a s| ≤ 1 * 1 :=
            mul_le_mul (ha_abs r hrs.1.1.1.1) (ha_abs s hrs.1.2.1.1) (abs_nonneg _) (by norm_num)
          nlinarith
  · intro u hu T jr js a ha_mult ha_sq
    obtain ⟨_, _, _, hK_scale, _⟩ := window_integrability_and_kernel_scaling_tc059 hu
    have h_pair_expand :
        ∀ d ∈ Finset.Icc 1 T,
          windowPairing (u / (d : ℝ))
              (quotientDyadicShellQ a T jr d) (quotientDyadicShellQ a T js d) =
            ∑ qr ∈ quotientDyadicShellFinset T jr d,
              ∑ qs ∈ quotientDyadicShellFinset T js d,
                a qr * a qs * windowKernelK (u / (d : ℝ)) qr qs := by
      intro d hd
      rw [Finset.mem_Icc] at hd
      have hd_pos : (0 : ℝ) < (d : ℝ) := Nat.cast_pos.mpr hd.1
      have hu_d : 0 < u / (d : ℝ) := div_pos hu hd_pos
      unfold windowPairing quotientDyadicShellQ
      have h_int_qq : ∀ qr qs : ℕ,
          IntervalIntegrable
            (fun X => (a qr * a qs) * (gaussianTermPhi qr X * gaussianTermPhi qs X / X))
            volume (u / (d : ℝ)) (RiemannScope.tau * (u / (d : ℝ))) :=
        fun qr qs =>
          (intervalIntegrable_window_of_continuousOn_aux hu_d
            (continuousOn_gaussianTermPhi_uIcc_aux hu_d qr)
            (continuousOn_gaussianTermPhi_uIcc_aux hu_d qs)).const_mul (a qr * a qs)
      have h_exp :
          (fun X =>
              (∑ qr ∈ quotientDyadicShellFinset T jr d, a qr * gaussianTermPhi qr X) *
                (∑ qs ∈ quotientDyadicShellFinset T js d, a qs * gaussianTermPhi qs X) / X) =
            (fun X =>
              ∑ qr ∈ quotientDyadicShellFinset T jr d,
                ∑ qs ∈ quotientDyadicShellFinset T js d,
                  (a qr * a qs) * (gaussianTermPhi qr X * gaussianTermPhi qs X / X)) := by
        ext X
        rw [Finset.sum_mul]
        simp_rw [Finset.mul_sum, Finset.sum_div]
        apply Finset.sum_congr rfl
        intro qr _
        apply Finset.sum_congr rfl
        intro qs _
        ring
      have h_inner_qq : ∀ qr : ℕ,
          IntervalIntegrable
            (fun X => ∑ qs ∈ quotientDyadicShellFinset T js d,
              (a qr * a qs) * (gaussianTermPhi qr X * gaussianTermPhi qs X / X))
            volume (u / (d : ℝ)) (RiemannScope.tau * (u / (d : ℝ))) :=
        fun qr =>
          intervalIntegrable_finset_sum_fn_aux (quotientDyadicShellFinset T js d)
            (fun qs _ => h_int_qq qr qs)
      rw [h_exp,
        intervalIntegral.integral_finset_sum (fun qr _ => h_inner_qq qr)]
      apply Finset.sum_congr rfl
      intro qr _
      rw [intervalIntegral.integral_finset_sum (fun qs _ => h_int_qq qr qs)]
      apply Finset.sum_congr rfl
      intro qs _
      rw [intervalIntegral.integral_const_mul]
      rfl
    have h_rhs_sigma :
        (∑ d ∈ Finset.Icc 1 T,
            ((ArithmeticFunction.moebius d : ℝ) / (d : ℝ)) *
              windowPairing (u / (d : ℝ))
                (quotientDyadicShellQ a T jr d) (quotientDyadicShellQ a T js d)) =
          ∑ x ∈ (Finset.Icc 1 T).sigma
              (fun d => quotientDyadicShellFinset T jr d ×ˢ quotientDyadicShellFinset T js d),
            (ArithmeticFunction.moebius x.1 : ℝ) *
              (a (x.1 * x.2.1) * a (x.1 * x.2.2) *
                windowKernelK u (x.1 * x.2.1) (x.1 * x.2.2)) := by
      have h_inner_d :
          ∀ d ∈ Finset.Icc 1 T,
            ((ArithmeticFunction.moebius d : ℝ) / (d : ℝ)) *
                windowPairing (u / (d : ℝ))
                  (quotientDyadicShellQ a T jr d) (quotientDyadicShellQ a T js d) =
              ∑ qq ∈ quotientDyadicShellFinset T jr d ×ˢ quotientDyadicShellFinset T js d,
                (ArithmeticFunction.moebius d : ℝ) *
                  (a (d * qq.1) * a (d * qq.2) *
                    windowKernelK u (d * qq.1) (d * qq.2)) := by
        intro d hd
        rw [h_pair_expand d hd]
        rw [Finset.mem_Icc] at hd
        rw [← Finset.sum_product', Finset.mul_sum]
        apply Finset.sum_congr rfl
        rintro ⟨qr, qs⟩ hqq
        dsimp only
        simp only [Finset.mem_product, quotientDyadicShellFinset, Finset.mem_filter,
          Finset.mem_Icc] at hqq
        rw [ha_mult d qr hd.1 hqq.1.1.1, ha_mult d qs hd.1 hqq.2.1.1, hK_scale hd.1 qr qs]
        have hd_ne : (d : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hd.1)
        calc
          ((ArithmeticFunction.moebius d : ℝ) / (d : ℝ)) *
              (a qr * a qs * windowKernelK (u / (d : ℝ)) qr qs)
            = (ArithmeticFunction.moebius d : ℝ) * 1 *
                (a qr * a qs * ((1 / (d : ℝ)) * windowKernelK (u / (d : ℝ)) qr qs)) := by
                  field_simp [hd_ne]
          _ = (ArithmeticFunction.moebius d : ℝ) *
                ((a d * a qr) * (a d * a qs) *
                  (1 / (d : ℝ) * windowKernelK (u / (d : ℝ)) qr qs)) := by
                rw [← ha_sq d hd.1]
                ring
      rw [Finset.sum_congr rfl h_inner_d, Finset.sum_sigma']
    rw [h_rhs_sigma]
    have h_bij_prod :
        (∑ x ∈ (Finset.Icc 1 T).sigma
              (fun d => quotientDyadicShellFinset T jr d ×ˢ quotientDyadicShellFinset T js d),
            (ArithmeticFunction.moebius x.1 : ℝ) *
              (a (x.1 * x.2.1) * a (x.1 * x.2.2) *
                windowKernelK u (x.1 * x.2.1) (x.1 * x.2.2))) =
          ∑ y ∈ (dyadicShellFinset T jr ×ˢ dyadicShellFinset T js).sigma
              (fun rs => (Nat.gcd rs.1 rs.2).divisors),
            (ArithmeticFunction.moebius y.2 : ℝ) *
              (a y.1.1 * a y.1.2 * windowKernelK u y.1.1 y.1.2) := by
      apply Finset.sum_bij (fun x _ => ⟨(x.1 * x.2.1, x.1 * x.2.2), x.1⟩)
      · rintro ⟨d, ⟨qr, qs⟩⟩ hx
        simp only [Finset.mem_sigma, Finset.mem_Icc, Finset.mem_product,
          quotientDyadicShellFinset, dyadicShellFinset, Finset.mem_filter,
          Nat.mem_divisors] at hx ⊢
        rcases hx with ⟨⟨hd1, _⟩, ⟨⟨hqr1, hqr_div⟩, hqr_lo, hqr_hi⟩,
          ⟨⟨hqs1, hqs_div⟩, hqs_lo, hqs_hi⟩⟩
        have hdqr_le : d * qr ≤ T := by
          rw [mul_comm]; exact (Nat.le_div_iff_mul_le hd1).mp hqr_div
        have hdqs_le : d * qs ≤ T := by
          rw [mul_comm]; exact (Nat.le_div_iff_mul_le hd1).mp hqs_div
        have h_gcd_pos : 0 < Nat.gcd (d * qr) (d * qs) :=
          Nat.gcd_pos_of_pos_left _ (Nat.mul_pos hd1 hqr1)
        exact ⟨⟨⟨⟨Nat.mul_pos hd1 hqr1, hdqr_le⟩, hqr_lo, hqr_hi⟩,
          ⟨⟨Nat.mul_pos hd1 hqs1, hdqs_le⟩, hqs_lo, hqs_hi⟩⟩,
          ⟨Nat.dvd_gcd ⟨qr, rfl⟩ ⟨qs, rfl⟩, ne_of_gt h_gcd_pos⟩⟩
      · rintro ⟨d1, ⟨qr1, qs1⟩⟩ h1 ⟨d2, ⟨qr2, qs2⟩⟩ h2 heq
        simp only [Finset.mem_sigma, Finset.mem_Icc] at h1 h2
        have hd_eq : d1 = d2 := by
          have h_snd :
              (⟨(d1 * qr1, d1 * qs1), d1⟩ : Σ _ : ℕ × ℕ, ℕ).2 =
                (⟨(d2 * qr2, d2 * qs2), d2⟩ : Σ _ : ℕ × ℕ, ℕ).2 :=
            congrArg Sigma.snd heq
          exact h_snd
        subst hd_eq
        have h_fst : (d1 * qr1, d1 * qs1) = (d1 * qr2, d1 * qs2) := congrArg Sigma.fst heq
        injection h_fst with h_r h_s
        have hqr_eq : qr1 = qr2 := Nat.eq_of_mul_eq_mul_left h1.1.1 h_r
        have hqs_eq : qs1 = qs2 := Nat.eq_of_mul_eq_mul_left h1.1.1 h_s
        subst hqr_eq; subst hqs_eq; rfl
      · rintro ⟨⟨r, s⟩, d⟩ hy
        simp only [Finset.mem_sigma, Finset.mem_product, dyadicShellFinset,
          Finset.mem_filter, Finset.mem_Icc, Nat.mem_divisors] at hy
        rcases hy with ⟨⟨⟨⟨hr1, hrT⟩, hr_lo, hr_hi⟩, ⟨⟨hs1, hsT⟩, hs_lo, hs_hi⟩⟩, ⟨hd_gcd, _⟩⟩
        have hd_r : d ∣ r := dvd_trans hd_gcd (Nat.gcd_dvd_left r s)
        have hd_s : d ∣ s := dvd_trans hd_gcd (Nat.gcd_dvd_right r s)
        have hd_pos : 1 ≤ d := Nat.pos_of_dvd_of_pos hd_r hr1
        have hd_le : d ≤ T := le_trans (Nat.le_of_dvd hr1 hd_r) hrT
        let qr := r / d
        let qs := s / d
        have hdqr : d * qr = r := Nat.mul_div_cancel' hd_r
        have hdqs : d * qs = s := Nat.mul_div_cancel' hd_s
        have hqr1 : 1 ≤ qr := Nat.div_pos (Nat.le_of_dvd hr1 hd_r) hd_pos
        have hqs1 : 1 ≤ qs := Nat.div_pos (Nat.le_of_dvd hs1 hd_s) hd_pos
        have hqr_div : qr ≤ T / d :=
          (Nat.le_div_iff_mul_le hd_pos).mpr (by rw [mul_comm, hdqr]; exact hrT)
        have hqs_div : qs ≤ T / d :=
          (Nat.le_div_iff_mul_le hd_pos).mpr (by rw [mul_comm, hdqs]; exact hsT)
        refine ⟨⟨d, (qr, qs)⟩, ?_, by dsimp only; rw [hdqr, hdqs]⟩
        simp only [Finset.mem_sigma, Finset.mem_Icc, Finset.mem_product,
          quotientDyadicShellFinset, Finset.mem_filter]
        exact ⟨⟨hd_pos, hd_le⟩,
          ⟨⟨hqr1, hqr_div⟩, by rwa [hdqr], by rwa [hdqr]⟩,
          ⟨⟨hqs1, hqs_div⟩, by rwa [hdqs], by rwa [hdqs]⟩⟩
      · rintro ⟨d, ⟨qr, qs⟩⟩ _; rfl
    rw [h_bij_prod, Finset.sum_sigma]
    unfold primitiveDyadicBlockSignedSum primitiveDyadicBlockPairs
    rw [Finset.sum_filter]
    symm
    apply Finset.sum_congr rfl
    rintro ⟨r, s⟩ _
    dsimp only
    rw [← Finset.sum_mul, sum_divisors_moebius_real_aux (Nat.gcd r s)]
    by_cases hcop : Nat.Coprime r s
    · have h1 : Nat.gcd r s = 1 := hcop
      rw [if_pos hcop, if_pos h1, one_mul]
    · have hne1 : Nat.gcd r s ≠ 1 := hcop
      rw [if_neg hcop, if_neg hne1, zero_mul]

/-! ### Section 5: Finite Parity Uniqueness, Auxiliary Turn Chart, Prime-Local Defect, Concrete Window `E = D̃ + S_comb`, and Conditional Logarithmic-Saving Closure Transfer -/

/-- Auxiliary turn-chart family `Z_a(z) := ζ(z / a)` (`TASK-TC-059` §5). -/
noncomputable def turnChartZ (a z : ℂ) : ℂ :=
  riemannZeta (z / a)

/-- Auxiliary real turn-chart exponent `K^* := 1 - log 2 / log τ` (`TASK-TC-059` §5; NOT proved algebraic). -/
noncomputable def turnChartProposedGradeKStar : ℝ :=
  1 - Real.log 2 / Real.log RiemannScope.tau

/-- Prime-local radial displacement defect `D_p(δ) := p^δ + p^{-δ} - 2` (`TASK-TC-059` §5). -/
noncomputable def primeLocalDefect (p : ℕ) (δ : ℝ) : ℝ :=
  (p : ℝ) ^ δ + (p : ℝ) ^ (-δ) - 2

/-- Normalized individual prime-power summand `F_{p^k, T}(X) := liouvillePrimePowerTerm T pk X / log X` (`X > 1`). -/
noncomputable def actualPrimePowerTermNormF (T : ℕ) (pk : ℕ × ℕ) (X : ℝ) : ℝ :=
  liouvillePrimePowerTerm T pk X / Real.log X

/-- Window-integrated normalized prime-power diagonal `D̃_T(Y) := ∑_{p^k ≤ T} ‖F_{p^k, T}‖_Y^2` (`Y ≥ 2`). -/
noncomputable def actualPrimePowerDiagDtilde (T : ℕ) (Y : ℝ) : ℝ :=
  ∑ pk ∈ primePowerPairsUpTo T, windowEnergyNormSq Y (actualPrimePowerTermNormF T pk)

/-- Window-integrated normalized prime-power off-diagonal `X̃_T(Y) := ∫_Y^{τ Y} x̃_{λ, pp}(X; T) dX / X`. -/
noncomputable def actualPrimePowerOffDiagXtilde (T : ℕ) (Y : ℝ) : ℝ :=
  ∫ X in Y..(RiemannScope.tau * Y), pointwisePrimePowerOffDiagNorm T X / X

/-- Window-integrated combined residual `S_{comb, T}(Y) := X̃_T(Y) + 2 ⟨P_T, R_T⟩_Y + ‖R_T‖_Y^2`. -/
noncomputable def actualCombinedResidualScomb (T : ℕ) (Y : ℝ) : ℝ :=
  actualPrimePowerOffDiagXtilde T Y +
    2 * windowPairing Y (normalizedPrimePowerTermP T) (normalizedFirstShiftTermR T) +
    windowEnergyNormSq Y (normalizedFirstShiftTermR T)

/-- Canonical `T(Y) = ⌈Y^{5/4}⌉` prime-power diagonal `D̃(Y)`. -/
noncomputable def canonicalPrimePowerDiagDtilde (Y : ℝ) : ℝ :=
  actualPrimePowerDiagDtilde (canonicalCutoffT Y) Y

/-- Canonical `T(Y) = ⌈Y^{5/4}⌉` combined residual `S_comb(Y)`. -/
noncomputable def canonicalCombinedResidualScomb (Y : ℝ) : ℝ :=
  actualCombinedResidualScomb (canonicalCutoffT Y) Y

private theorem uIcc_subset_Ioi_one_aux {Y : ℝ} (hY : 1 < Y) :
    ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), 1 < X ∧ 0 < X ∧ Real.log X ≠ 0 := by
  have htau : (1 : ℝ) < RiemannScope.tau := tau_gt_one_aux
  have hle : Y ≤ RiemannScope.tau * Y := by nlinarith
  intro X hX
  rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX
  have hX1 : 1 < X := lt_of_lt_of_le hY hX.1
  have hX0 : 0 < X := lt_trans zero_lt_one hX1
  exact ⟨hX1, hX0, ne_of_gt (Real.log_pos hX1)⟩

private theorem continuousOn_log_uIcc_gt_one_aux {Y : ℝ} (hY : 1 < Y) :
    ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) := by
  apply Real.continuousOn_log.mono
  intro X hX
  exact ne_of_gt (uIcc_subset_Ioi_one_aux hY X hX).2.1

private theorem continuousOn_finiteQShifted_uIcc_aux {Y : ℝ} (hY : 0 < Y) (a : ℕ → ℝ) (m T : ℕ) :
    ContinuousOn (finiteQShifted a m T) (Set.uIcc Y (RiemannScope.tau * Y)) := by
  unfold finiteQShifted
  apply continuousOn_finset_sum
  intro n hn
  rw [Finset.mem_Icc] at hn
  have hn_pos : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr hn.1
  have h_div_cont : ContinuousOn (fun X : ℝ => X / (n : ℝ)) (Set.uIcc Y (RiemannScope.tau * Y)) :=
    continuousOn_id.div_const (n : ℝ)
  have h_log_cont :
      ContinuousOn (fun X : ℝ => Real.log (X / (n : ℝ))) (Set.uIcc Y (RiemannScope.tau * Y)) := by
    apply Real.continuousOn_log.comp h_div_cont
    intro X hX
    exact ne_of_gt (div_pos (uIcc_subset_Ioi_of_pos_aux hY X hX) hn_pos)
  exact (continuousOn_const.mul (h_log_cont.pow m)).mul (continuousOn_gaussianTermPhi_uIcc_aux hY n)

private theorem continuousOn_liouvillePrimePowerTerm_uIcc_aux {Y : ℝ} (hY : 0 < Y) (T : ℕ) (pk : ℕ × ℕ) :
    ContinuousOn (liouvillePrimePowerTerm T pk) (Set.uIcc Y (RiemannScope.tau * Y)) := by
  unfold liouvillePrimePowerTerm
  have h_finQ_eq : ∀ L : ℕ, finiteQLambda L = finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) L := by
    intro L; ext w
    unfold finiteQLambda finiteQGeneral gaussianTermPhi
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro n _; ring
  rw [h_finQ_eq]
  have h_comp :
      ContinuousOn
        (fun X : ℝ =>
          finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) (T / pk.1 ^ pk.2)
            (X / ((pk.1 ^ pk.2 : ℕ) : ℝ)))
        (Set.uIcc Y (RiemannScope.tau * Y)) := by
    unfold finiteQGeneral
    apply continuousOn_finset_sum
    intro n _
    have h_phi_comp :
        ContinuousOn (fun X : ℝ => gaussianTermPhi n (X / ((pk.1 ^ pk.2 : ℕ) : ℝ)))
          (Set.uIcc Y (RiemannScope.tau * Y)) := by
      apply (continuousOn_gaussianTermPhi_Ici_aux n).comp (continuousOn_id.div_const _)
      intro X hX
      have hX_pos := uIcc_subset_Ioi_of_pos_aux hY X hX
      exact div_nonneg (le_of_lt hX_pos) (Nat.cast_nonneg _)
    exact continuousOn_const.mul h_phi_comp
  exact continuousOn_const.mul h_comp

private theorem polylog_le_rpow_of_exp_one_le_aux
    {Y κ η' : ℝ} (hY : Real.exp 1 ≤ Y) (hκ_pos : 0 < κ) (_ : κ ≤ 2) (hη' : 0 < η') :
    (Real.log Y) ^ (2 - κ) ≤ (Real.log Y) ^ 2 ∧
      (Real.log Y) ^ 2 ≤ (4 / ((Real.exp 1) ^ 2 * (η') ^ 2)) * Y ^ η' := by
  have he_pos : 0 < Real.exp 1 := Real.exp_pos 1
  have hY_pos : 0 < Y := lt_of_lt_of_le he_pos hY
  have hlog_ge1 : 1 ≤ Real.log Y := by
    have h := Real.log_le_log he_pos hY
    rwa [Real.log_exp] at h
  have h1 : (Real.log Y) ^ (2 - κ) ≤ (Real.log Y) ^ 2 := by
    have hpow := Real.rpow_le_rpow_of_exponent_le hlog_ge1 (by linarith : 2 - κ ≤ 2)
    rwa [Real.rpow_two] at hpow
  refine ⟨h1, ?_⟩
  have h_lin_exp : (η' / 2) * Real.log Y ≤ Real.exp ((η' / 2) * Real.log Y - 1) := by
    have h := Real.add_one_le_exp ((η' / 2) * Real.log Y - 1)
    linarith
  have h_exp_sub :
      Real.exp ((η' / 2) * Real.log Y - 1) =
        Real.exp ((η' / 2) * Real.log Y) / Real.exp 1 := by
    rw [sub_eq_add_neg, Real.exp_add, Real.exp_neg, ← div_eq_mul_inv]
  rw [h_exp_sub] at h_lin_exp
  have h_lhs_nn : 0 ≤ (η' / 2) * Real.log Y := by positivity
  have h_sq_le :
      ((η' / 2) * Real.log Y) ^ 2 ≤
        (Real.exp ((η' / 2) * Real.log Y) / Real.exp 1) ^ 2 :=
    pow_le_pow_left h_lhs_nn h_lin_exp 2
  have h_exp_sq :
      (Real.exp ((η' / 2) * Real.log Y)) ^ 2 = Y ^ η' := by
    rw [sq, ← Real.exp_add, Real.rpow_def_of_pos hY_pos]
    congr 1
    ring
  rw [div_pow, h_exp_sq] at h_sq_le
  have hη'_ne : η' ≠ 0 := ne_of_gt hη'
  have he_ne : Real.exp 1 ≠ 0 := ne_of_gt he_pos
  have h_mul_pos : 0 < 4 / (η' ^ 2) := by positivity
  have h_final := mul_le_mul_of_nonneg_left h_sq_le (le_of_lt h_mul_pos)
  calc
    (Real.log Y) ^ 2 = (4 / (η' ^ 2)) * (((η' / 2) * Real.log Y) ^ 2) := by
      field_simp [hη'_ne]; ring
    _ ≤ (4 / (η' ^ 2)) * (Y ^ η' / (Real.exp 1) ^ 2) := h_final
    _ = (4 / ((Real.exp 1) ^ 2 * (η') ^ 2)) * Y ^ η' := by
      field_simp [hη'_ne, he_ne]; ring

/-- **Theorem 5 (`TASK-TC-059` §§1, 3, 4, 5, Finite Parity Uniqueness, Turn-Chart Symmetry & Trivial Zeros, Prime-Local Defect Bridge, Concrete Window `E = D̃ + S_comb`, Conditional Logarithmic-Saving Closure Transfer, and Partial Block-Saving Aggregation)**:
    *Formal scope*:
    1. *Finite parity uniqueness (`UNCONDITIONAL_FINITE_ARITHMETIC`)*:
       On `1 ≤ n ≤ T`, the finite linear parity relations `a(1) = 1` and `a(p * m) + a(m) = 0` (`p` prime, `1 ≤ m`, `p * m ≤ T`)
       uniquely force `a(n) = λ(n)`;
    2. *Auxiliary turn-chart identities (`CONCRETE_ANALYTIC_IN_LEAN`)*:
       `Z_{τ/2}(τ q) = ζ(2 q)`, critical line `(q.re = 1 / 4 ↔ (2 * q).re = 1 / 2)`, reflection `2 * (1 / 2 - q) = 1 - 2 * q`,
       exact trivial zeros `Z_{τ/2}(τ * (-(m + 1))) = 0` (`m : ℕ`) via `RiemannScope.TrivialZero.trivialZero_exact`, and
       real scale identity `τ^{K^*} = τ / 2` (`K^* = 1 - log 2 / log τ` kept as an auxiliary real exponent without claiming algebraicity);
    3. *Prime-local defect & Euler-factor norm-square bridge (`CONCRETE_ANALYTIC_IN_LEAN`)*:
       For every prime `p`, `δ : ℝ`, and phase `θ : ℝ`,
       `D_p(δ) = (p^{δ/2} - p^{-δ/2})^2 ≥ 0`, `(D_p(δ) = 0 ↔ δ = 0)`, and
       `Complex.normSq ((p^δ : ℂ) * exp(I * θ) - 1) = p^δ * (D_p(δ) + 4 * sin^2(θ / 2)) ≥ p^δ * D_p(δ)`;
    4. *Concrete window-integrated `E = D̃ + S_comb` identity (`CONCRETE_ANALYTIC_IN_LEAN`)*:
       For every `Y > 1` (hence all `Y ≥ 2`) and all `T : ℕ`,
       `actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) T Y = actualPrimePowerDiagDtilde T Y + actualCombinedResidualScomb T Y`
       (and in particular `canonicalLiouvilleEnergyE Y = canonicalPrimePowerDiagDtilde Y + canonicalCombinedResidualScomb Y`);
    5. *Logarithmic-saving closure transfer (`CONDITIONAL_IMPLICATION`, specializing `Theorem 29` via finite-horizon `normalizedScaleSupremum` without assuming a globally finite supremum) and RH converse (`B_η = 0`)*:
       - Elementary polylog dominance `(log Y)^{2 - κ} ≤ (log Y)^2 ≤ (4 / (e^2 η'^2)) Y^{η'}` (`Y ≥ e`, `κ ∈ (0, 2]`, `0 < η'`);
       - Forward conditional transfer: from linear boundedness `0 ≤ E(Z) ≤ M_lin Z` (`Z ≥ 1`), the diagonal envelope estimate
         `D̃(Y) ≤ (C_diag / (log Y)^2) F(Y) + C_cut` (`Y ≥ Y_diag ≥ e`), and the §1 closure inequality
         `E(Y) ≤ A_η Y^η + B_η (log Y)^{2 - κ_η} D̃(Y)` (`Y ≥ Y_η ≥ e`, `0 < η < ε`, `κ_η ∈ (0, 2]`), with `η' := (η + ε) / 2` and
         explicit threshold `Y_* := max (max Y_diag Y_η) (exp ((2 B_η C_diag + 1)^{1 / κ_η}))`, the prospective feedback satisfies
         `B_η C_diag / (log Y)^{κ_η} ≤ 1 / 2` for all `Y ≥ Y_*` (`= 2 B_η ζ''(1 + ε) / (log Y)^{κ_η}` when `C_diag = 2 ζ''(1 + ε)`),
         every finite horizon `R_hor ≥ Y_*` satisfies `G_ε(R_hor) ≤ max (G_ε(Y_*)) (4 K')`, and `E(Y), F(Y) ≤ max (G_ε(Y_*)) (4 K') * Y^ε`
         for all `Y ≥ 1` (strictly a conditional transfer corollary, NOT an unconditional proof of the §1 arithmetic bound);
       - RH-strength subpower converse (`B_η = 0`): `(∀ Z ≥ 1, E(Z) ≤ A_η Z^η)` with `D̃(Y) ≥ 0` implies the §1 closure bound with `B_η = 0, κ_η = 1`;
    6. *Partial block-saving aggregation algebra (`UNCONDITIONAL_FINITE_ARITHMETIC`)*:
       If `|Π_g| ≤ B_loc (Y / g)^{1 - c}` (`c ∈ (0, 1)`, `Y > 0`, `1 ≤ g ≤ M`), then
       `∑_{1 ≤ g ≤ M} (1 / g) |Π_g| ≤ B_loc (∑_{1 ≤ g ≤ M} g^{-(2 - c)}) Y^{1 - c}`. -/
theorem parity_uniqueness_turn_chart_defect_and_log_saving_closure_tc059 :
    (∀ (T : ℕ) (a : ℕ → ℝ),
      a 1 = 1 →
      (∀ p m : ℕ, p.Prime → 1 ≤ m → p * m ≤ T → a (p * m) + a m = 0) →
      ∀ n ∈ Finset.Icc 1 T, a n = (liouvilleLambda n : ℝ)) ∧
    ((∀ q : ℂ,
        turnChartZ ((RiemannScope.tau : ℂ) / 2) ((RiemannScope.tau : ℂ) * q) = riemannZeta (2 * q) ∧
          (q.re = 1 / 4 ↔ (2 * q).re = 1 / 2) ∧
          2 * ((1 / 2 : ℂ) - q) = 1 - 2 * q) ∧
      (∀ m : ℕ,
        turnChartZ ((RiemannScope.tau : ℂ) / 2) ((RiemannScope.tau : ℂ) * (-((m : ℂ) + 1))) = 0) ∧
      RiemannScope.tau ^ turnChartProposedGradeKStar = RiemannScope.tau / 2) ∧
    (∀ {p : ℕ}, p.Prime → ∀ δ θ : ℝ,
      primeLocalDefect p δ = ((p : ℝ) ^ (δ / 2) - (p : ℝ) ^ (-δ / 2)) ^ 2 ∧
        0 ≤ primeLocalDefect p δ ∧
        (primeLocalDefect p δ = 0 ↔ δ = 0) ∧
        Complex.normSq ((((p : ℝ) ^ δ : ℝ) : ℂ) * Complex.exp (Complex.I * (θ : ℂ)) - 1) =
          (p : ℝ) ^ δ * (primeLocalDefect p δ + 4 * (Real.sin (θ / 2)) ^ 2) ∧
        (p : ℝ) ^ δ * primeLocalDefect p δ ≤
          Complex.normSq ((((p : ℝ) ^ δ : ℝ) : ℂ) * Complex.exp (Complex.I * (θ : ℂ)) - 1)) ∧
    (∀ {Y : ℝ}, 1 < Y → ∀ T : ℕ,
      actualPrimePowerDiagDtilde T Y =
          (∫ X in Y..(RiemannScope.tau * Y), pointwisePrimePowerDiagNorm T X / X) ∧
        actualCombinedResidualScomb T Y =
          (∫ X in Y..(RiemannScope.tau * Y), pointwiseCombinedResidualS T X / X) ∧
        actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) T Y =
          actualPrimePowerDiagDtilde T Y + actualCombinedResidualScomb T Y ∧
        canonicalLiouvilleEnergyE Y =
          canonicalPrimePowerDiagDtilde Y + canonicalCombinedResidualScomb Y) ∧
    ((∀ {Y κ η' : ℝ}, Real.exp 1 ≤ Y → 0 < κ → κ ≤ 2 → 0 < η' →
        (Real.log Y) ^ (2 - κ) ≤ (Real.log Y) ^ 2 ∧
          (Real.log Y) ^ 2 ≤ (4 / ((Real.exp 1) ^ 2 * (η') ^ 2)) * Y ^ η') ∧
      (∀ {E D_tilde : ℝ → ℝ} {M_lin C_diag C_cut Y_diag η ε A_η B_η κ_η Y_η : ℝ},
        (∀ Z : ℝ, 1 ≤ Z → 0 ≤ E Z) →
        0 ≤ M_lin →
        (∀ Z : ℝ, 1 ≤ Z → E Z ≤ M_lin * Z) →
        0 ≤ C_diag → 0 ≤ C_cut → Real.exp 1 ≤ Y_diag →
        (∀ Y : ℝ, Y_diag ≤ Y →
          D_tilde Y ≤ (C_diag / (Real.log Y) ^ 2) * monotoneScaleEnvelope E Y + C_cut) →
        0 < η → η < ε → 0 ≤ A_η → 0 ≤ B_η → 0 < κ_η → κ_η ≤ 2 → Real.exp 1 ≤ Y_η →
        (∀ Y : ℝ, Y_η ≤ Y →
          E Y ≤ A_η * Y ^ η + B_η * (Real.log Y) ^ (2 - κ_η) * D_tilde Y) →
        let η' := (η + ε) / 2
        let Y_star := max (max Y_diag Y_η) (Real.exp ((2 * B_η * C_diag + 1) ^ (1 / κ_η)))
        let A'_η' := A_η + B_η * C_cut * (4 / ((Real.exp 1) ^ 2 * (η') ^ 2))
        let K' := A'_η' * Y_star ^ (η' - ε)
        (∀ Y : ℝ, Y_star ≤ Y →
          B_η * C_diag / (Real.log Y) ^ κ_η ≤ 1 / 2 ∧
            E Y ≤ A'_η' * Y ^ η' + (1 / 2 : ℝ) * monotoneScaleEnvelope E Y) ∧
        (∀ R_hor : ℝ, Y_star ≤ R_hor →
          normalizedScaleSupremum E ε R_hor ≤
            max (normalizedScaleSupremum E ε Y_star) (K' + (3 / 4 : ℝ) * normalizedScaleSupremum E ε R_hor) ∧
          normalizedScaleSupremum E ε R_hor ≤
            max (normalizedScaleSupremum E ε Y_star) (4 * K')) ∧
        (∀ Y : ℝ, 1 ≤ Y →
          E Y ≤ max (normalizedScaleSupremum E ε Y_star) (4 * K') * Y ^ ε ∧
            monotoneScaleEnvelope E Y ≤
              max (normalizedScaleSupremum E ε Y_star) (4 * K') * Y ^ ε)) ∧
      (∀ (E D_tilde : ℝ → ℝ) {η A_η : ℝ},
        0 ≤ A_η →
        (∀ Y : ℝ, Real.exp 1 ≤ Y → 0 ≤ D_tilde Y) →
        (∀ Y : ℝ, 1 ≤ Y → E Y ≤ A_η * Y ^ η) →
        ∀ Y : ℝ, Real.exp 1 ≤ Y →
          E Y ≤ A_η * Y ^ η + (0 : ℝ) * (Real.log Y) ^ (2 - (1 : ℝ)) * D_tilde Y)) ∧
    (∀ (M : ℕ) (Pi_blk : ℕ → ℝ) {Y B_loc c : ℝ},
      0 < Y → 0 ≤ B_loc → 0 < c → c < 1 →
      (∀ g ∈ Finset.Icc 1 M, |Pi_blk g| ≤ B_loc * (Y / (g : ℝ)) ^ (1 - c)) →
      (∑ g ∈ Finset.Icc 1 M, (1 / (g : ℝ)) * |Pi_blk g|) ≤
        B_loc * (∑ g ∈ Finset.Icc 1 M, (g : ℝ) ^ (-(2 - c))) * Y ^ (1 - c)) := by
  refine ⟨?_, ?_, ?_, ?_, ⟨?_, ?_, ?_⟩, ?_⟩
  · intro T a ha1 ha_par n hn
    rw [Finset.mem_Icc] at hn
    rcases hn with ⟨hn1, hnT⟩
    induction' n using Nat.strong_induction_on with n ih
    by_cases hn_eq1 : n = 1
    · subst hn_eq1
      simp [ha1, liouvilleLambda, natOmega, liouvilleSignFromOmega]
    · have hn_ge2 : 2 ≤ n := by omega
      let p := n.minFac
      have hp : p.Prime := Nat.minFac_prime (by omega)
      have hp_dvd : p ∣ n := Nat.minFac_dvd n
      let m := n / p
      have hpm : p * m = n := Nat.mul_div_cancel' hp_dvd
      have hm_pos : 1 ≤ m := Nat.div_pos (Nat.le_of_dvd (by omega) hp_dvd) hp.pos
      have hm_lt : m < n := Nat.div_lt_self (by omega) hp.one_lt
      have hm_le_T : m ≤ T := le_trans (le_of_lt hm_lt) hnT
      have h_rel := ha_par p m hp hm_pos (by rwa [hpm])
      have h_ih := ih m hm_lt hm_pos hm_le_T
      have h_lam_p : (liouvilleLambda p : ℝ) = -1 := by
        have hop : natOmega p = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr hp
        simp [liouvilleLambda, hp.ne_zero, hop, liouvilleSignFromOmega]
      have h_lam_pm :
          (liouvilleLambda n : ℝ) = -(liouvilleLambda m : ℝ) := by
        rw [← hpm]
        have h_mul : (liouvilleLambda (p * m) : ℝ) =
            (liouvilleLambda p : ℝ) * (liouvilleLambda m : ℝ) := by
          exact_mod_cast liouvilleLambda_mul_pos_aux hp.pos hm_pos
        rw [h_mul, h_lam_p]
        ring
      rw [hpm] at h_rel
      linarith
  · refine ⟨?_, ?_, ?_⟩
    · intro q
      have htau_pos : 0 < RiemannScope.tau := lt_trans zero_lt_one tau_gt_one_aux
      have htau_ne : (RiemannScope.tau : ℂ) ≠ 0 := Complex.ofReal_ne_zero.mpr (ne_of_gt htau_pos)
      have h_div : ((RiemannScope.tau : ℂ) * q) / ((RiemannScope.tau : ℂ) / 2) = 2 * q := by
        field_simp [htau_ne]
        ring
      refine ⟨by unfold turnChartZ; rw [h_div], ?_, by ring⟩
      have h2re : (2 * q).re = 2 * q.re := by simp
      rw [h2re]
      constructor <;> intro h <;> linarith
    · intro m
      have htau_pos : 0 < RiemannScope.tau := lt_trans zero_lt_one tau_gt_one_aux
      have htau_ne : (RiemannScope.tau : ℂ) ≠ 0 := Complex.ofReal_ne_zero.mpr (ne_of_gt htau_pos)
      unfold turnChartZ
      have h_arg :
          ((RiemannScope.tau : ℂ) * (-((m : ℂ) + 1))) / ((RiemannScope.tau : ℂ) / 2) =
            -2 * ((m : ℂ) + 1) := by
        field_simp [htau_ne]
        ring
      rw [h_arg]
      exact RiemannScope.TrivialZero.trivialZero_exact m
    · have htau_gt1 : (1 : ℝ) < RiemannScope.tau := tau_gt_one_aux
      have htau_pos : 0 < RiemannScope.tau := lt_trans zero_lt_one htau_gt1
      have hlog_tau_ne : Real.log RiemannScope.tau ≠ 0 := ne_of_gt (Real.log_pos htau_gt1)
      unfold turnChartProposedGradeKStar
      rw [Real.rpow_def_of_pos htau_pos]
      have h_exp_arg :
          Real.log RiemannScope.tau * (1 - Real.log 2 / Real.log RiemannScope.tau) =
            Real.log RiemannScope.tau - Real.log 2 := by
        field_simp [hlog_tau_ne]
      rw [h_exp_arg, Real.exp_sub, Real.exp_log htau_pos, Real.exp_log (by norm_num : (0 : ℝ) < 2)]
  · intro p hp δ θ
    have hp_gt1 : (1 : ℝ) < (p : ℝ) := by exact_mod_cast hp.one_lt
    have hp_pos : (0 : ℝ) < (p : ℝ) := lt_trans zero_lt_one hp_gt1
    have hlogp_pos : 0 < Real.log (p : ℝ) := Real.log_pos hp_gt1
    have h_sq_id : primeLocalDefect p δ = ((p : ℝ) ^ (δ / 2) - (p : ℝ) ^ (-δ / 2)) ^ 2 := by
      unfold primeLocalDefect
      have h_pos_sq : ((p : ℝ) ^ (δ / 2)) ^ 2 = (p : ℝ) ^ δ := by
        rw [sq, ← Real.rpow_add hp_pos]
        congr 1; ring
      have h_neg_sq : ((p : ℝ) ^ (-δ / 2)) ^ 2 = (p : ℝ) ^ (-δ) := by
        rw [sq, ← Real.rpow_add hp_pos]
        congr 1; ring
      have h_prod_one : (p : ℝ) ^ (δ / 2) * (p : ℝ) ^ (-δ / 2) = 1 := by
        rw [← Real.rpow_add hp_pos]
        have hz : δ / 2 + -δ / 2 = 0 := by ring
        rw [hz, Real.rpow_zero]
      calc
        (p : ℝ) ^ δ + (p : ℝ) ^ (-δ) - 2
          = ((p : ℝ) ^ (δ / 2)) ^ 2 + ((p : ℝ) ^ (-δ / 2)) ^ 2 -
              2 * ((p : ℝ) ^ (δ / 2) * (p : ℝ) ^ (-δ / 2)) := by
                rw [h_pos_sq, h_neg_sq, h_prod_one]; ring
        _ = ((p : ℝ) ^ (δ / 2) - (p : ℝ) ^ (-δ / 2)) ^ 2 := by ring
    have h_nn : 0 ≤ primeLocalDefect p δ := by
      rw [h_sq_id]
      exact sq_nonneg _
    have h_zero_iff : primeLocalDefect p δ = 0 ↔ δ = 0 := by
      rw [h_sq_id, sq_eq_zero_iff, sub_eq_zero]
      constructor
      · intro heq
        rw [Real.rpow_def_of_pos hp_pos, Real.rpow_def_of_pos hp_pos] at heq
        have heq := Real.exp_injective heq
        have hlogp_ne : Real.log (p : ℝ) ≠ 0 := ne_of_gt hlogp_pos
        have h_eq2 : δ / 2 = -δ / 2 := mul_left_cancel₀ hlogp_ne heq
        linarith
      · rintro rfl
        simp
    have h_normSq :
        Complex.normSq ((((p : ℝ) ^ δ : ℝ) : ℂ) * Complex.exp (Complex.I * (θ : ℂ)) - 1) =
          (p : ℝ) ^ δ * (primeLocalDefect p δ + 4 * (Real.sin (θ / 2)) ^ 2) := by
      let r := (p : ℝ) ^ δ
      have hr_inv : r * (p : ℝ) ^ (-δ) = 1 := by
        dsimp [r]
        rw [← Real.rpow_add hp_pos, add_neg_self, Real.rpow_zero]
      have h_i_comm : Complex.I * (θ : ℂ) = (θ : ℂ) * Complex.I := mul_comm _ _
      rw [h_i_comm, Complex.exp_mul_I]
      have h_z_eq :
          ((r : ℂ) * (Complex.cos (θ : ℂ) + Complex.sin (θ : ℂ) * Complex.I) - 1) =
            (((r * Real.cos θ - 1 : ℝ) : ℂ) + ((r * Real.sin θ : ℝ) : ℂ) * Complex.I) := by
        rw [← Complex.ofReal_cos, ← Complex.ofReal_sin]
        push_cast
        ring
      rw [h_z_eq, Complex.normSq_add_mul_I]
      have h_trig1 : (Real.cos θ) ^ 2 + (Real.sin θ) ^ 2 = 1 := by
        rw [add_comm]
        exact Real.sin_sq_add_cos_sq θ
      have h_half : Real.cos θ = 1 - 2 * (Real.sin (θ / 2)) ^ 2 := by
        have h2 : θ = 2 * (θ / 2) := by ring
        conv_lhs => rw [h2, Real.cos_two_mul]
        have hs := Real.sin_sq_add_cos_sq (θ / 2)
        linarith
      unfold primeLocalDefect
      calc
        (r * Real.cos θ - 1) ^ 2 + (r * Real.sin θ) ^ 2
          = r ^ 2 * ((Real.cos θ) ^ 2 + (Real.sin θ) ^ 2) - 2 * r * Real.cos θ + 1 := by ring
        _ = r ^ 2 - 2 * r * (1 - 2 * (Real.sin (θ / 2)) ^ 2) + 1 := by rw [h_trig1, h_half]; ring
        _ = r * (r + (p : ℝ) ^ (-δ) - 2 + 4 * (Real.sin (θ / 2)) ^ 2) := by
              calc
                r ^ 2 - 2 * r * (1 - 2 * (Real.sin (θ / 2)) ^ 2) + 1
                  = r ^ 2 - 2 * r * (1 - 2 * (Real.sin (θ / 2)) ^ 2) + r * (p : ℝ) ^ (-δ) := by
                      rw [hr_inv]
                _ = r * (r + (p : ℝ) ^ (-δ) - 2 + 4 * (Real.sin (θ / 2)) ^ 2) := by ring
    have h_lb :
        (p : ℝ) ^ δ * primeLocalDefect p δ ≤
          Complex.normSq ((((p : ℝ) ^ δ : ℝ) : ℂ) * Complex.exp (Complex.I * (θ : ℂ)) - 1) := by
      rw [h_normSq]
      have hr_pos : 0 ≤ (p : ℝ) ^ δ := Real.rpow_nonneg (le_of_lt hp_pos) δ
      have h_nonneg : 0 ≤ (p : ℝ) ^ δ * (4 * (Real.sin (θ / 2)) ^ 2) :=
        mul_nonneg hr_pos (by positivity)
      linarith [h_nonneg]
    exact ⟨h_sq_id, h_nn, h_zero_iff, h_normSq, h_lb⟩
  · intro Y hY1 T
    have hY_pos : 0 < Y := lt_trans zero_lt_one hY1
    have h_log_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
      continuousOn_log_uIcc_gt_one_aux hY1
    have h_log_ne : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), Real.log X ≠ 0 :=
      fun X hX => (uIcc_subset_Ioi_one_aux hY1 X hX).2.2
    have h_log_sq_ne : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), (Real.log X) ^ 2 ≠ 0 :=
      fun X hX => pow_ne_zero 2 (h_log_ne X hX)
    have h_all :
        ∀ L : ℕ,
          (actualPrimePowerDiagDtilde L Y =
              ∫ X in Y..(RiemannScope.tau * Y), pointwisePrimePowerDiagNorm L X / X) ∧
            (actualCombinedResidualScomb L Y =
              ∫ X in Y..(RiemannScope.tau * Y), pointwiseCombinedResidualS L X / X) ∧
            (actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) L Y =
              actualPrimePowerDiagDtilde L Y + actualCombinedResidualScomb L Y) := by
      intro L
      have h_cont_P_L : ContinuousOn (normalizedPrimePowerTermP L) (Set.uIcc Y (RiemannScope.tau * Y)) := by
        unfold normalizedPrimePowerTermP
        refine (continuousOn_finset_sum _ (fun pk _ =>
          continuousOn_liouvillePrimePowerTerm_uIcc_aux hY_pos L pk)).div h_log_cont h_log_ne
      have h_cont_R_L : ContinuousOn (normalizedFirstShiftTermR L) (Set.uIcc Y (RiemannScope.tau * Y)) := by
        unfold normalizedFirstShiftTermR
        exact (continuousOn_finiteQShifted_uIcc_aux hY_pos _ 1 L).div h_log_cont h_log_ne
      have h_cont_X_L :
          ContinuousOn (pointwisePrimePowerOffDiagNorm L) (Set.uIcc Y (RiemannScope.tau * Y)) := by
        unfold pointwisePrimePowerOffDiagNorm
        refine (continuousOn_finset_sum _ (fun pk1 _ =>
          continuousOn_finset_sum _ (fun pk2 _ =>
            (continuousOn_liouvillePrimePowerTerm_uIcc_aux hY_pos L pk1).mul
              (continuousOn_liouvillePrimePowerTerm_uIcc_aux hY_pos L pk2)))).div
          (h_log_cont.pow 2) h_log_sq_ne
      have h_cont_D_L :
          ContinuousOn (pointwisePrimePowerDiagNorm L) (Set.uIcc Y (RiemannScope.tau * Y)) := by
        unfold pointwisePrimePowerDiagNorm
        have h_finQ_eq_k : ∀ M : ℕ, finiteQLambda M = finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) M := by
          intro M; ext w; unfold finiteQLambda finiteQGeneral gaussianTermPhi
          rw [Finset.mul_sum]; apply Finset.sum_congr rfl; intro n _; ring
        refine (continuousOn_finset_sum _ (fun pk _ => ?_)).div (h_log_cont.pow 2) h_log_sq_ne
        rw [h_finQ_eq_k]
        refine continuousOn_const.mul ((continuousOn_finset_sum _ (fun n _ => ?_)).pow 2)
        exact continuousOn_const.mul
          ((continuousOn_gaussianTermPhi_Ici_aux n).comp (continuousOn_id.div_const _)
            (fun X hX => div_nonneg (le_of_lt (uIcc_subset_Ioi_of_pos_aux hY_pos X hX))
              (Nat.cast_nonneg _)))
      have h_cont_S_L :
          ContinuousOn (pointwiseCombinedResidualS L) (Set.uIcc Y (RiemannScope.tau * Y)) := by
        unfold pointwiseCombinedResidualS
        exact (h_cont_X_L.add ((continuousOn_const.mul h_cont_P_L).mul h_cont_R_L)).add (h_cont_R_L.pow 2)
      have h_int_D_L :
          IntervalIntegrable (fun X => pointwisePrimePowerDiagNorm L X / X)
            volume Y (RiemannScope.tau * Y) := by
        have h1 : (fun X => pointwisePrimePowerDiagNorm L X / X) =
            (fun X => pointwisePrimePowerDiagNorm L X * 1 / X) := by ext X; ring
        rw [h1]
        exact intervalIntegrable_window_of_continuousOn_aux hY_pos h_cont_D_L continuousOn_const
      have h_int_S_L :
          IntervalIntegrable (fun X => pointwiseCombinedResidualS L X / X)
            volume Y (RiemannScope.tau * Y) := by
        have h1 : (fun X => pointwiseCombinedResidualS L X / X) =
            (fun X => pointwiseCombinedResidualS L X * 1 / X) := by ext X; ring
        rw [h1]
        exact intervalIntegrable_window_of_continuousOn_aux hY_pos h_cont_S_L continuousOn_const
      have h_D_L :
          actualPrimePowerDiagDtilde L Y =
            ∫ X in Y..(RiemannScope.tau * Y), pointwisePrimePowerDiagNorm L X / X := by
        unfold actualPrimePowerDiagDtilde windowEnergyNormSq windowPairing
        have h_cont_F_L : ∀ pk : ℕ × ℕ,
            ContinuousOn (actualPrimePowerTermNormF L pk) (Set.uIcc Y (RiemannScope.tau * Y)) :=
          fun pk => (continuousOn_liouvillePrimePowerTerm_uIcc_aux hY_pos L pk).div h_log_cont h_log_ne
        have h_int_pk_L : ∀ pk : ℕ × ℕ,
            IntervalIntegrable
              (fun X => actualPrimePowerTermNormF L pk X * actualPrimePowerTermNormF L pk X / X)
              volume Y (RiemannScope.tau * Y) :=
          fun pk => intervalIntegrable_window_of_continuousOn_aux hY_pos (h_cont_F_L pk) (h_cont_F_L pk)
        rw [← intervalIntegral.integral_finset_sum (fun pk _ => h_int_pk_L pk)]
        apply intervalIntegral.integral_congr
        intro X _
        dsimp only [actualPrimePowerTermNormF, pointwisePrimePowerDiagNorm, liouvillePrimePowerTerm]
        rw [← Finset.sum_div]
        congr 1
        have h_sum_term :
            (∑ pk ∈ primePowerPairsUpTo L,
                ((-1 : ℝ) ^ pk.2 * Real.log (pk.1 : ℝ) * (1 / Real.sqrt ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
                    finiteQLambda (L / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ)) / Real.log X) *
                  ((-1 : ℝ) ^ pk.2 * Real.log (pk.1 : ℝ) * (1 / Real.sqrt ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
                    finiteQLambda (L / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ)) / Real.log X)) =
              ∑ pk ∈ primePowerPairsUpTo L,
                ((Real.log (pk.1 : ℝ)) ^ 2 * (1 / ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
                  (finiteQLambda (L / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ))) ^ 2) /
                    (Real.log X) ^ 2 := by
          apply Finset.sum_congr rfl
          rintro ⟨p, k⟩ _
          have hsqrt_sq : (Real.sqrt ((p ^ k : ℕ) : ℝ)) ^ 2 = ((p ^ k : ℕ) : ℝ) :=
            Real.sq_sqrt (Nat.cast_nonneg _)
          have h_neg1_sq : ((-1 : ℝ) ^ k) ^ 2 = 1 := by
            rw [← pow_mul, mul_comm k 2, pow_mul]; norm_num
          calc
            ((-1 : ℝ) ^ k * Real.log (p : ℝ) * (1 / Real.sqrt ((p ^ k : ℕ) : ℝ)) *
                  finiteQLambda (L / p ^ k) (X / ((p ^ k : ℕ) : ℝ)) / Real.log X) *
                ((-1 : ℝ) ^ k * Real.log (p : ℝ) * (1 / Real.sqrt ((p ^ k : ℕ) : ℝ)) *
                  finiteQLambda (L / p ^ k) (X / ((p ^ k : ℕ) : ℝ)) / Real.log X)
              = (((-1 : ℝ) ^ k) ^ 2 * (Real.log (p : ℝ)) ^ 2 *
                  (1 / (Real.sqrt ((p ^ k : ℕ) : ℝ)) ^ 2) *
                  (finiteQLambda (L / p ^ k) (X / ((p ^ k : ℕ) : ℝ))) ^ 2) / (Real.log X) ^ 2 := by ring
            _ = (((Real.log (p : ℝ)) ^ 2 * (1 / ((p ^ k : ℕ) : ℝ)) *
                  (finiteQLambda (L / p ^ k) (X / ((p ^ k : ℕ) : ℝ))) ^ 2)) / (Real.log X) ^ 2 := by
                rw [h_neg1_sq, hsqrt_sq, one_mul]
        rw [h_sum_term, ← Finset.sum_div]
        congr 1
        apply Finset.sum_congr rfl
        intro pk _
        ring
      have h_S_L :
          actualCombinedResidualScomb L Y =
            ∫ X in Y..(RiemannScope.tau * Y), pointwiseCombinedResidualS L X / X := by
        unfold actualCombinedResidualScomb actualPrimePowerOffDiagXtilde windowEnergyNormSq windowPairing
        have h_int_X_L :
            IntervalIntegrable (fun X => pointwisePrimePowerOffDiagNorm L X / X)
              volume Y (RiemannScope.tau * Y) := by
          have h1 : (fun X => pointwisePrimePowerOffDiagNorm L X / X) =
              (fun X => pointwisePrimePowerOffDiagNorm L X * 1 / X) := by ext X; ring
          rw [h1]
          exact intervalIntegrable_window_of_continuousOn_aux hY_pos h_cont_X_L continuousOn_const
        have h_int_PR_L := intervalIntegrable_window_of_continuousOn_aux hY_pos h_cont_P_L h_cont_R_L
        have h_int_RR_L := intervalIntegrable_window_of_continuousOn_aux hY_pos h_cont_R_L h_cont_R_L
        rw [← intervalIntegral.integral_const_mul,
          ← intervalIntegral.integral_add h_int_X_L (h_int_PR_L.const_mul 2),
          ← intervalIntegral.integral_add (h_int_X_L.add (h_int_PR_L.const_mul 2)) h_int_RR_L]
        apply intervalIntegral.integral_congr
        intro X _
        dsimp only [pointwiseCombinedResidualS]
        ring
      refine ⟨h_D_L, h_S_L, ?_⟩
      rw [h_D_L, h_S_L, ← intervalIntegral.integral_add h_int_D_L h_int_S_L]
      unfold actualWindowEnergyE windowEnergyNormSq windowPairing
      have h_finQ_L : finiteQLambda L = finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) L := by
        ext w; unfold finiteQLambda finiteQGeneral gaussianTermPhi
        rw [Finset.mul_sum]; apply Finset.sum_congr rfl; intro n _; ring
      obtain ⟨h_pt_29, _⟩ :=
        combined_target_exact_quadratic_and_conditional_absorption_tc058
          (E := fun _ => 0) (M_lin := 0) (fun _ _ => le_refl 0) (le_refl 0) (fun _ _ => by ring_nf; exact le_refl 0)
      apply intervalIntegral.integral_congr
      intro X hX
      obtain ⟨_, hX_pos, hlogX_ne⟩ := uIcc_subset_Ioi_one_aux hY1 X hX
      have h_q2 := (h_pt_29 L 0 X hX_pos hlogX_ne).2.1
      rw [h_finQ_L] at h_q2
      calc
        finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) L X *
            finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) L X / X
          = (finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) L X) ^ 2 / X := by ring
        _ = (pointwisePrimePowerDiagNorm L X + pointwiseCombinedResidualS L X) / X := by rw [h_q2]
        _ = pointwisePrimePowerDiagNorm L X / X + pointwiseCombinedResidualS L X / X := add_div _ _ _
    exact ⟨(h_all T).1, (h_all T).2.1, (h_all T).2.2, (h_all (canonicalCutoffT Y)).2.2⟩
  · intro Y κ η' hY hκ_pos hκ_le2 hη'
    exact polylog_le_rpow_of_exp_one_le_aux hY hκ_pos hκ_le2 hη'
  · intro E D_tilde M_lin C_diag C_cut Y_diag η ε A_η B_η κ_η Y_η
      hE_nn hM_nn hE_lin hCd_nn hCc_nn hYdiag_ge_e hD_env
      hη_pos hηε hA_nn hB_nn hκ_pos hκ_le2 _ h_closure
    dsimp only
    let η' := (η + ε) / 2
    let Y_star := max (max Y_diag Y_η) (Real.exp ((2 * B_η * C_diag + 1) ^ (1 / κ_η)))
    let A'_η' := A_η + B_η * C_cut * (4 / ((Real.exp 1) ^ 2 * (η') ^ 2))
    let K' := A'_η' * Y_star ^ (η' - ε)
    have hη'_pos : 0 < η' := by dsimp [η']; linarith
    have hη_lt_η' : η < η' := by dsimp [η']; linarith
    have hη'_lt_ε : η' < ε := by dsimp [η']; linarith
    have he_ge1 : (1 : ℝ) ≤ Real.exp 1 := le_trans (by norm_num : (1 : ℝ) ≤ 1 + 1) (Real.add_one_le_exp 1)
    have hYstar_ge_e : Real.exp 1 ≤ Y_star :=
      le_trans hYdiag_ge_e (le_trans (le_max_left Y_diag Y_η) (le_max_left _ _))
    have hYstar_ge1 : 1 ≤ Y_star := le_trans he_ge1 hYstar_ge_e
    obtain ⟨⟨h_env_pt, _⟩, _, _, _⟩ :=
      abstract_polylog_scale_bootstrap_and_weighted_contraction_tc057 hE_nn hM_nn hE_lin
    have h_step_star :
        ∀ Y : ℝ, Y_star ≤ Y →
          B_η * C_diag / (Real.log Y) ^ κ_η ≤ 1 / 2 ∧
            E Y ≤ A'_η' * Y ^ η' + (1 / 2 : ℝ) * monotoneScaleEnvelope E Y := by
      intro Y hYYs
      have hY_ge_diag : Y_diag ≤ Y :=
        le_trans (le_trans (le_max_left Y_diag Y_η) (le_max_left _ _)) hYYs
      have hY_ge_η : Y_η ≤ Y :=
        le_trans (le_trans (le_max_right Y_diag Y_η) (le_max_left _ _)) hYYs
      have hY_ge_exp : Real.exp ((2 * B_η * C_diag + 1) ^ (1 / κ_η)) ≤ Y :=
        le_trans (le_max_right _ _) hYYs
      have hY_ge_e : Real.exp 1 ≤ Y := le_trans hYstar_ge_e hYYs
      have hY_ge1 : 1 ≤ Y := le_trans he_ge1 hY_ge_e
      have hlogY_ge1 : 1 ≤ Real.log Y := by
        have h := Real.log_le_log (Real.exp_pos 1) hY_ge_e
        rwa [Real.log_exp] at h
      have hlogY_pos : 0 < Real.log Y := lt_of_lt_of_le zero_lt_one hlogY_ge1
      have h_base_ge1 : 1 ≤ 2 * B_η * C_diag + 1 := by
        have h0 : 0 ≤ 2 * B_η * C_diag := by positivity
        linarith [h0]
      have h_base_pos : 0 < 2 * B_η * C_diag + 1 := lt_of_lt_of_le zero_lt_one h_base_ge1
      have h_log_ge_pow : (2 * B_η * C_diag + 1) ^ (1 / κ_η) ≤ Real.log Y := by
        have h := Real.log_le_log (Real.exp_pos _) hY_ge_exp
        rwa [Real.log_exp] at h
      have h_pow_log_ge : 2 * B_η * C_diag + 1 ≤ (Real.log Y) ^ κ_η := by
        have h1 := Real.rpow_le_rpow (by positivity) h_log_ge_pow (le_of_lt hκ_pos)
        rw [← Real.rpow_mul (le_of_lt h_base_pos), one_div_mul_cancel (ne_of_gt hκ_pos),
          Real.rpow_one] at h1
        exact h1
      have h_log_pow_pos : 0 < (Real.log Y) ^ κ_η := Real.rpow_pos_of_pos hlogY_pos κ_η
      have h_fb_half : B_η * C_diag / (Real.log Y) ^ κ_η ≤ 1 / 2 := by
        rw [div_le_iff h_log_pow_pos]
        linarith
      refine ⟨h_fb_half, ?_⟩
      have h_cl_Y := h_closure Y hY_ge_η
      have h_D_Y := hD_env Y hY_ge_diag
      have h_log_2mk_nn : 0 ≤ (Real.log Y) ^ (2 - κ_η) := Real.rpow_nonneg (le_of_lt hlogY_pos) _
      have h_mul_D :=
        mul_le_mul_of_nonneg_left h_D_Y (mul_nonneg hB_nn h_log_2mk_nn)
      have h_rpow_div :
          (Real.log Y) ^ (2 - κ_η) * (C_diag / (Real.log Y) ^ 2) =
            C_diag / (Real.log Y) ^ κ_η := by
        have h_two : (Real.log Y) ^ (2 : ℝ) = (Real.log Y) ^ 2 := Real.rpow_two (Real.log Y)
        rw [← h_two, mul_div_left_comm, ← Real.rpow_sub hlogY_pos]
        have hexp_sub : (2 - κ_η) - 2 = -κ_η := by ring
        rw [hexp_sub, Real.rpow_neg (le_of_lt hlogY_pos), div_eq_mul_inv]
      obtain ⟨h_pl1, h_pl2⟩ := polylog_le_rpow_of_exp_one_le_aux hY_ge_e hκ_pos hκ_le2 hη'_pos
      have h_pl_bound :
          (Real.log Y) ^ (2 - κ_η) ≤ (4 / ((Real.exp 1) ^ 2 * (η') ^ 2)) * Y ^ η' :=
        le_trans h_pl1 h_pl2
      have h_Y_mono : Y ^ η ≤ Y ^ η' := Real.rpow_le_rpow_of_exponent_le hY_ge1 (le_of_lt hη_lt_η')
      have hF_nn : 0 ≤ monotoneScaleEnvelope E Y := (h_env_pt Y hY_ge1).2.1
      have h_fb_F :
          (B_η * C_diag / (Real.log Y) ^ κ_η) * monotoneScaleEnvelope E Y ≤
            (1 / 2 : ℝ) * monotoneScaleEnvelope E Y :=
        mul_le_mul_of_nonneg_right h_fb_half hF_nn
      have h_A_mono : A_η * Y ^ η ≤ A_η * Y ^ η' :=
        mul_le_mul_of_nonneg_left h_Y_mono hA_nn
      have h_cut_mono :
          B_η * C_cut * (Real.log Y) ^ (2 - κ_η) ≤
            B_η * C_cut * ((4 / ((Real.exp 1) ^ 2 * (η') ^ 2)) * Y ^ η') :=
        mul_le_mul_of_nonneg_left h_pl_bound (mul_nonneg hB_nn hCc_nn)
      have h_expand_rhs :
          B_η * (Real.log Y) ^ (2 - κ_η) *
              ((C_diag / (Real.log Y) ^ 2) * monotoneScaleEnvelope E Y + C_cut) =
            (B_η * C_diag / (Real.log Y) ^ κ_η) * monotoneScaleEnvelope E Y +
              B_η * C_cut * (Real.log Y) ^ (2 - κ_η) := by
        calc
          B_η * (Real.log Y) ^ (2 - κ_η) *
              ((C_diag / (Real.log Y) ^ 2) * monotoneScaleEnvelope E Y + C_cut)
            = B_η * ((Real.log Y) ^ (2 - κ_η) * (C_diag / (Real.log Y) ^ 2)) *
                monotoneScaleEnvelope E Y +
              B_η * C_cut * (Real.log Y) ^ (2 - κ_η) := by ring
          _ = (B_η * C_diag / (Real.log Y) ^ κ_η) * monotoneScaleEnvelope E Y +
                B_η * C_cut * (Real.log Y) ^ (2 - κ_η) := by
              rw [h_rpow_div]; ring
      rw [h_expand_rhs] at h_mul_D
      dsimp [A'_η']
      linarith
    have hA'_nn : 0 ≤ A'_η' := by
      dsimp [A'_η']
      positivity
    obtain ⟨_, _, h_abs_29⟩ :=
      combined_target_exact_quadratic_and_conditional_absorption_tc058 hE_nn hM_nn hE_lin
    have h_spec :=
      h_abs_29 (fun _ => 0) E (fun _ => ∅) (fun _ _ => 0) (fun _ _ => 1)
        η' ε A'_η' (1 / 2) 0 (3 / 4) Y_star
        hη'_pos hη'_lt_ε hA'_nn (le_refl 0)
        (by norm_num) (by norm_num) (by norm_num) (by norm_num) hYstar_ge1
        (fun Y _ => by simp)
        (fun Y _ => ⟨fun _ hmem => False.elim (Finset.not_mem_empty _ hmem), by simp⟩)
        (fun Y hYYs => (h_step_star Y hYYs).2)
        (fun Y _ => by simp; norm_num)
    dsimp only at h_spec
    have hK_eq : A'_η' * Y_star ^ (η' - ε) + 0 * Y_star ^ (-ε) = K' := by
      dsimp [K']; ring
    have h_div_q : K' / (1 - (3 / 4 : ℝ)) = 4 * K' := by ring
    rw [hK_eq, h_div_q] at h_spec
    exact ⟨h_step_star, h_spec.1, h_spec.2⟩
  · intro E D_tilde η A_η _ _ hE_sub Y hY_ge_e
    have he_ge1 : (1 : ℝ) ≤ Real.exp 1 := le_trans (by norm_num : (1 : ℝ) ≤ 1 + 1) (Real.add_one_le_exp 1)
    have hY1 : 1 ≤ Y := le_trans he_ge1 hY_ge_e
    simpa using hE_sub Y hY1
  · intro M Pi_blk Y B_loc c hY_pos _ _ _ hPi_bound
    have hY_nn : 0 ≤ Y := le_of_lt hY_pos
    calc
      (∑ g ∈ Finset.Icc 1 M, (1 / (g : ℝ)) * |Pi_blk g|)
        ≤ ∑ g ∈ Finset.Icc 1 M, (1 / (g : ℝ)) * (B_loc * (Y / (g : ℝ)) ^ (1 - c)) := by
          apply Finset.sum_le_sum
          intro g hg
          rw [Finset.mem_Icc] at hg
          have hg_nn : 0 ≤ (1 / (g : ℝ)) := by positivity
          exact mul_le_mul_of_nonneg_left (hPi_bound g (Finset.mem_Icc.mpr hg)) hg_nn
      _ = B_loc * (∑ g ∈ Finset.Icc 1 M, (g : ℝ) ^ (-(2 - c))) * Y ^ (1 - c) := by
          rw [Finset.mul_sum, Finset.sum_mul]
          apply Finset.sum_congr rfl
          intro g hg
          rw [Finset.mem_Icc] at hg
          have hg_pos : (0 : ℝ) < (g : ℝ) := Nat.cast_pos.mpr hg.1
          have hg_nn : 0 ≤ (g : ℝ) := le_of_lt hg_pos
          have h_div_rpow :
              (Y / (g : ℝ)) ^ (1 - c) = Y ^ (1 - c) * (g : ℝ) ^ (-(1 - c)) := by
            rw [Real.div_rpow hY_nn hg_nn (1 - c), div_eq_mul_inv, ← Real.rpow_neg hg_nn]
          rw [h_div_rpow]
          have h_inv_g : (1 / (g : ℝ)) * (g : ℝ) ^ (-(1 - c)) = (g : ℝ) ^ (-(2 - c)) := by
            have hg1 : (1 / (g : ℝ)) = (g : ℝ) ^ (-1 : ℝ) := by
              rw [one_div, Real.rpow_neg_one]
            rw [hg1, ← Real.rpow_add hg_pos]
            congr 1; ring
          calc
            (1 / (g : ℝ)) * (B_loc * (Y ^ (1 - c) * (g : ℝ) ^ (-(1 - c))))
              = B_loc * ((1 / (g : ℝ)) * (g : ℝ) ^ (-(1 - c))) * Y ^ (1 - c) := by ring
            _ = B_loc * (g : ℝ) ^ (-(2 - c)) * Y ^ (1 - c) := by rw [h_inv_g]



end DyadicPowerLiftPrimitiveCorrelation

end RiemannScope
