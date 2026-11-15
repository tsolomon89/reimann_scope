/-
RiemannScope.MixedArithmeticCovariance
TASK-TC-061 (EPIC-TC-042 / SUBGATE-TC-043A):
Mixed Arithmetic Covariance J_T(Y), Exact Prime-Power Factorization Sign Agreement,
Selberg w_{2,lambda} Prime-Power and Biprime Formulas, Finite-Window Off-Diagonal Kernel
Expansion with Unconditional Composite Self-Collision Bound, and Sharp Route D Closure
Transfer under MixedCovarianceClosureHypothesis.

Formalizes in Lean 4 (complete machine-checked proofs with canonical circle constant
RiemannScope.tau throughout):
1. `mixed_covariance_identity_and_theta_energy_bound_tc061`:
   Normalized prime-power energy split into `inheritedPrimePowerDiagDtilde` and
   `inheritedPrimePowerOffDiagXtilde`, pointwise identity `2 * P_T - O_T = Q_T + A_T` on
   `[Y, RiemannScope.tau * Y]`, exact mixed window norm identity
   `4 * D_tilde + J_T = ‖2 * P_T - O_T‖_Y^2 = ‖Q_T + A_T‖_Y^2 >= 0` with complete
   `IntervalIntegrable` proofs, exact `θ`-parameterized window energy inequality (`0 < θ < 1`),
   `θ = 1 / 2` specialization (`8 * D_tilde + 2 * J_T + 2 * ‖A_T‖_Y^2`), and canonical-schedule
   instantiation at `T = canonicalCutoffT Y`, `D0 = ⌊log Y⌋` for all `Y >= 2`.
2. `factorization_sign_agreement_and_selberg_w2_formulas_tc061`:
   Exact factorization sign agreement `Λ_λ(m) λ(q) = λ(m q) Λ(m)` (`m, q >= 1`), prime-power
   specialization `Λ_λ(p^k) λ(q) = λ(p^k q) log p`, divisor aggregation
   `∑_{d ∣ n} Λ_λ(d) λ(n / d) = λ(n) log n`, exact prime-power formula
   `w_{2,λ}(p^k) = (-1)^k (2k - 1) (log p)^2`, and exact biprime-power formula
   `w_{2,λ}(p^a q^b) = 2 (-1)^{a+b} log p log q` (`p ≠ q`).
3. `finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061`:
   Exact finite-window expansions of `inheritedPrimePowerDiagDtilde` and
   `inheritedPrimePowerOffDiagXtilde` against `logWeightedWindowKernel 2 Y m n`, exact values
   and two-sided `[0, (log n)^2]` bounds for the composite self-collision weight
   `offDiagPrimePowerWeight n n`, and unconditional uniform `O(1)` bound across all `Y >= 2`
   and `T : ℕ` on `∑_{1 ≤ n ≤ T} offDiagPrimePowerWeight n n * logWeightedWindowKernel 2 Y n n`.
4. `mixed_covariance_hypothesis_route_d_closure_transfer_tc061`:
   Polylogarithmic absorption `(log Y)^{2 - κ_eta} ≤ (log Y)^2 ≤ (4 / η'^2) Y^{η'}` (`Y >= e`),
   direct sharper `(8, 2, 2)` Route D contraction transfer with explicit `R`-independent `Y_star`
   and simultaneous `(1/4 + 1/4 + 1/4 = 3/4)` feedback contractions, all-`ε` transfer under
   `MixedCovarianceClosureHypothesis`, and companion `2 * A_sq ≤ 4 * A_sq` bridge to
   `complete_reconstruction_drift_contraction_transfer_tc060` at `η' = (η + ε) / 2`.
-/

import RiemannScope.SignedDilationArithmeticEnergy

open scoped ArithmeticFunction BigOperators Classical
open MeasureTheory intervalIntegral

namespace RiemannScope
namespace MixedArithmeticCovariance

open RiemannScope.LiouvilleSquareDilation
open RiemannScope.DyadicPowerLiftPrimitiveCorrelation hiding canonicalPrimePowerDiagDtilde
open RiemannScope.SignedDilationArithmeticEnergy

/-! ### Section 1: Core Definitions (`TASK-TC-061`) -/

/-- Inherited-cutoff prime-power diagonal window energy
    `D̃_T(Y) := ∫_Y^{tau * Y} pointwisePrimePowerDiagNorm T X / X`. -/
noncomputable def inheritedPrimePowerDiagDtilde (T : ℕ) (Y : ℝ) : ℝ :=
  ∫ X in Y..(RiemannScope.tau * Y), pointwisePrimePowerDiagNorm T X / X

/-- Inherited-cutoff prime-power off-diagonal window energy
    `X̃_T(Y) := ∫_Y^{tau * Y} pointwisePrimePowerOffDiagNorm T X / X`. -/
noncomputable def inheritedPrimePowerOffDiagXtilde (T : ℕ) (Y : ℝ) : ℝ :=
  ∫ X in Y..(RiemannScope.tau * Y), pointwisePrimePowerOffDiagNorm T X / X

/-- Signed mixed arithmetic covariance functional
    `J_T(Y) := 4 * X̃_T(Y) + ‖O_{T,D0}‖_Y^2 - 4 * ⟨P_T, O_{T,D0}⟩_Y`. -/
noncomputable def signedMixedCovarianceJ (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ) : ℝ :=
  4 * inheritedPrimePowerOffDiagXtilde T Y +
    windowEnergyNormSq Y (openCoreOscShiftD2Part c_lam c_half T D0) -
    4 * windowPairing Y (normalizedPrimePowerTermP T) (openCoreOscShiftD2Part c_lam c_half T D0)

/-- Canonical-schedule (`T = canonicalCutoffT Y`, `D0 = ⌊log Y⌋`) signed mixed covariance `J(Y)`. -/
noncomputable def canonicalSignedMixedCovarianceJ (c_lam c_half : ℝ) (Y : ℝ) : ℝ :=
  signedMixedCovarianceJ c_lam c_half (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y

/-- Canonical-schedule (`T = canonicalCutoffT Y`) inherited prime-power diagonal `D̃(Y)`. -/
noncomputable def canonicalPrimePowerDiagDtilde (Y : ℝ) : ℝ :=
  inheritedPrimePowerDiagDtilde (canonicalCutoffT Y) Y

/-- Log-weighted Gaussian window kernel
    `∫_Y^{tau * Y} (gaussianTermPhi m X * gaussianTermPhi n X / (log X)^ν) / X`. -/
noncomputable def logWeightedWindowKernel (ν : ℕ) (Y : ℝ) (m n : ℕ) : ℝ :=
  ∫ X in Y..(RiemannScope.tau * Y),
    (gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ ν) / X

/-- Common prime-power divisor squared-logarithm weight
    `∑_{(p, k) : p^k ∣ gcd(m, n)} (log p)^2`. -/
noncomputable def commonPrimePowerLogSq (m n : ℕ) : ℝ :=
  ∑ pk ∈ (primePowerPairsUpTo (min m n)).filter (fun pk => (pk.1 ^ pk.2) ∣ Nat.gcd m n),
    (Real.log (pk.1 : ℝ)) ^ 2

/-- Off-diagonal prime-power pair weight `log m * log n - commonPrimePowerLogSq m n`. -/
noncomputable def offDiagPrimePowerWeight (m n : ℕ) : ℝ :=
  Real.log (m : ℝ) * Real.log (n : ℝ) - commonPrimePowerLogSq m n

/-- Open mixed-covariance closure hypothesis (`TASK-TC-061` interface to `SUBGATE-TC-043A`):
    for every `η > 0`, `J(Y)` is bounded for `Y ≥ Y_eta` by `a_eta * Y^η` plus a
    polylogarithmically damped multiple `b_eta * (log Y)^{2 - κ_eta} * D_tilde(Y)` (`0 < κ_eta ≤ 2`). -/
def MixedCovarianceClosureHypothesis (J D_tilde : ℝ → ℝ) : Prop :=
  ∀ η : ℝ, 0 < η →
    ∃ a_eta b_eta κ_eta Y_eta : ℝ,
      0 ≤ a_eta ∧
      0 ≤ b_eta ∧
      0 < κ_eta ∧
      κ_eta ≤ 2 ∧
      2 ≤ Y_eta ∧
      ∀ Y : ℝ, Y_eta ≤ Y →
        J Y ≤ a_eta * Y ^ η + b_eta * (Real.log Y) ^ (2 - κ_eta) * D_tilde Y

/-! ### Section 2: Auxiliary Analytic and Arithmetic Helpers -/

private theorem abs_sin_le_abs_tc061_aux (x : ℝ) : |Real.sin x| ≤ |x| := by
  have h_cos_bds : ∀ t : ℝ, -1 ≤ Real.cos t ∧ Real.cos t ≤ 1 := by
    intro t
    have hsq : (Real.cos t) ^ 2 ≤ 1 := by
      linarith [Real.sin_sq_add_cos_sq t, sq_nonneg (Real.sin t)]
    have habs : |Real.cos t| ≤ 1 := by
      rw [← Real.sqrt_sq_eq_abs]
      exact le_trans (Real.sqrt_le_sqrt hsq) (by norm_num)
    exact abs_le.mp habs
  have h_nonneg : ∀ y : ℝ, 0 ≤ y → |Real.sin y| ≤ y := by
    intro y hy
    let f₁ : ℝ → ℝ := fun t => t - Real.sin t
    have hf₁_cont : ContinuousOn f₁ (Set.Ici 0) :=
      continuousOn_id.sub Real.continuous_sin.continuousOn
    have hf₁_deriv : ∀ t : ℝ, HasDerivAt f₁ (1 - Real.cos t) t :=
      fun t => (hasDerivAt_id t).sub (Real.hasDerivAt_sin t)
    have hf₁_mono : MonotoneOn f₁ (Set.Ici 0) := by
      apply monotoneOn_of_deriv_nonneg (convex_Ici 0) hf₁_cont
      · intro t _; exact (hf₁_deriv t).differentiableAt.differentiableWithinAt
      · intro t _; rw [(hf₁_deriv t).deriv]; linarith [(h_cos_bds t).2]
    have h_ub : Real.sin y ≤ y := by
      have h := hf₁_mono Set.left_mem_Ici hy hy
      dsimp [f₁] at h
      rw [Real.sin_zero] at h
      linarith
    let f₂ : ℝ → ℝ := fun t => t + Real.sin t
    have hf₂_cont : ContinuousOn f₂ (Set.Ici 0) :=
      continuousOn_id.add Real.continuous_sin.continuousOn
    have hf₂_deriv : ∀ t : ℝ, HasDerivAt f₂ (1 + Real.cos t) t :=
      fun t => (hasDerivAt_id t).add (Real.hasDerivAt_sin t)
    have hf₂_mono : MonotoneOn f₂ (Set.Ici 0) := by
      apply monotoneOn_of_deriv_nonneg (convex_Ici 0) hf₂_cont
      · intro t _; exact (hf₂_deriv t).differentiableAt.differentiableWithinAt
      · intro t _; rw [(hf₂_deriv t).deriv]; linarith [(h_cos_bds t).1]
    have h_lb : -y ≤ Real.sin y := by
      have h := hf₂_mono Set.left_mem_Ici hy hy
      dsimp [f₂] at h
      rw [Real.sin_zero] at h
      linarith
    exact abs_le.mpr ⟨h_lb, h_ub⟩
  rcases le_or_lt 0 x with hx | hx
  · rw [abs_of_nonneg hx]; exact h_nonneg x hx
  · have h := h_nonneg (-x) (by linarith)
    rw [Real.sin_neg, abs_neg] at h
    rwa [abs_of_neg hx]

private theorem tau_gt_one_and_lt_eight_tc061_aux :
    (1 : ℝ) < RiemannScope.tau ∧ RiemannScope.tau < 8 := by
  have hpos : 0 < RiemannScope.tau := RiemannScope.tau_pos
  have hdiv : ∀ x : ℝ, 2 * x / 4 = x / 2 := fun x => by ring
  have hsin : Real.sin (RiemannScope.tau / 4) = 1 := by
    unfold RiemannScope.tau
    rw [hdiv]
    simp
  have habs : |Real.sin (RiemannScope.tau / 4)| ≤ |RiemannScope.tau / 4| :=
    abs_sin_le_abs_tc061_aux (RiemannScope.tau / 4)
  rw [hsin, abs_one, abs_of_pos (by linarith)] at habs
  have hgt1 : (1 : ℝ) < RiemannScope.tau := by linarith
  have hceil : Nat.ceil (RiemannScope.tau * (4096 : ℝ)) ≤ 32767 :=
    (full_core_quantified_obstructions_and_w2_support_tc060r).1.2.1.2.1
  have hle_ceil : RiemannScope.tau * (4096 : ℝ) ≤ (Nat.ceil (RiemannScope.tau * (4096 : ℝ)) : ℝ) :=
    Nat.le_ceil _
  have hceil_real : (Nat.ceil (RiemannScope.tau * (4096 : ℝ)) : ℝ) ≤ 32767 := by
    exact_mod_cast hceil
  exact ⟨hgt1, by linarith⟩

private theorem uIcc_tau_props_tc061_aux {Y : ℝ} (hY2 : 2 ≤ Y) :
    Y ≤ RiemannScope.tau * Y ∧
      ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
        2 ≤ X ∧ 0 < X ∧ 0 < Real.log X ∧ Real.log X ≠ 0 ∧ (Real.log X) ^ 2 ≠ 0 := by
  have htau : (1 : ℝ) < RiemannScope.tau := tau_gt_one_and_lt_eight_tc061_aux.1
  have hle : Y ≤ RiemannScope.tau * Y := by nlinarith
  refine ⟨hle, ?_⟩
  intro X hX
  rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX
  have hX2 : 2 ≤ X := le_trans hY2 hX.1
  have hX0 : 0 < X := by linarith
  have hlog : 0 < Real.log X := Real.log_pos (by linarith)
  exact ⟨hX2, hX0, hlog, ne_of_gt hlog, pow_ne_zero 2 (ne_of_gt hlog)⟩

private theorem continuousOn_gaussianTermPhi_scaled_tc061_aux (Y : ℝ)
    (q : ℕ) (m : ℝ) :
    ContinuousOn (fun X => gaussianTermPhi q (X / m)) (Set.uIcc Y (RiemannScope.tau * Y)) := by
  unfold gaussianTermPhi
  have hr : ContinuousOn (fun X : ℝ => (X / m) ^ (5 / 2 : ℝ))
      (Set.uIcc Y (RiemannScope.tau * Y)) := by
    apply ContinuousOn.rpow_const (continuousOn_id.div_const m)
    intro _ _; right; norm_num
  have he : Continuous (fun X : ℝ =>
      (((q : ℝ) ^ 3)⁻¹ * Real.exp (-((X / m) ^ 2) / (q : ℝ) ^ 2))) := by continuity
  exact hr.mul he.continuousOn

private theorem continuousOn_gaussianTermPhi_uIcc_tc061_aux {Y : ℝ} (_hY2 : 2 ≤ Y) (n : ℕ) :
    ContinuousOn (gaussianTermPhi n) (Set.uIcc Y (RiemannScope.tau * Y)) := by
  have h := continuousOn_gaussianTermPhi_scaled_tc061_aux Y n 1
  simpa [div_one] using h

private theorem continuousOn_finiteQLambda_scaled_tc061_aux {Y : ℝ} (_hY2 : 2 ≤ Y)
    (L : ℕ) (m : ℝ) :
    ContinuousOn (fun X => finiteQLambda L (X / m)) (Set.uIcc Y (RiemannScope.tau * Y)) := by
  have h_fn :
      (fun X => finiteQLambda L (X / m)) =
        fun X => ∑ q ∈ Finset.Icc 1 L, (liouvilleLambda q : ℝ) * gaussianTermPhi q (X / m) := by
    ext X
    dsimp [finiteQLambda, gaussianTermPhi]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro q _
    ring
  rw [h_fn]
  exact continuousOn_finset_sum _ (fun q _ =>
    continuousOn_const.mul (continuousOn_gaussianTermPhi_scaled_tc061_aux Y q m))

private theorem continuousOn_core_components_tc061_aux {Y : ℝ} (hY2 : 2 ≤ Y)
    (T D0 : ℕ) (c_lam c_half : ℝ) :
    ContinuousOn (finiteQLambda T) (Set.uIcc Y (RiemannScope.tau * Y)) ∧
      ContinuousOn (finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) T)
        (Set.uIcc Y (RiemannScope.tau * Y)) ∧
      ContinuousOn (normalizedPrimePowerTermP T) (Set.uIcc Y (RiemannScope.tau * Y)) ∧
      ContinuousOn (knownCompensatedD2Part c_lam c_half T D0)
        (Set.uIcc Y (RiemannScope.tau * Y)) ∧
      ContinuousOn (openCoreOscShiftD2Part c_lam c_half T D0)
        (Set.uIcc Y (RiemannScope.tau * Y)) := by
  obtain ⟨_, hprops⟩ := uIcc_tau_props_tc061_aux hY2
  have hpos : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), 0 < X := fun X hX => (hprops X hX).2.1
  have hlog_ne : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), Real.log X ≠ 0 :=
    fun X hX => (hprops X hX).2.2.2.1
  have hlog_sq_ne : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), (Real.log X) ^ 2 ≠ 0 :=
    fun X hX => (hprops X hX).2.2.2.2
  have hlog_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
    ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hpos X hX))
  have hQ_cont : ContinuousOn (finiteQLambda T) (Set.uIcc Y (RiemannScope.tau * Y)) := by
    have h := continuousOn_finiteQLambda_scaled_tc061_aux hY2 T 1
    simpa [div_one] using h
  have hQgen_cont :
      ContinuousOn (finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) T)
        (Set.uIcc Y (RiemannScope.tau * Y)) := by
    unfold finiteQGeneral
    exact continuousOn_finset_sum _ (fun n _ =>
      continuousOn_const.mul (continuousOn_gaussianTermPhi_uIcc_tc061_aux hY2 n))
  have hP_cont :
      ContinuousOn (normalizedPrimePowerTermP T) (Set.uIcc Y (RiemannScope.tau * Y)) := by
    unfold normalizedPrimePowerTermP liouvillePrimePowerTerm
    refine (continuousOn_finset_sum _ (fun pk _ => ?_)).div hlog_cont hlog_ne
    exact continuousOn_const.mul (continuousOn_finiteQLambda_scaled_tc061_aux hY2 _ _)
  have h_sm_cont :
      ∀ d : ℕ,
        ContinuousOn (scaledFiberSmoothStep T d) (Set.uIcc Y (RiemannScope.tau * Y)) := by
    intro d
    unfold scaledFiberSmoothStep
    exact (continuousOn_const.mul (continuousOn_finiteQLambda_scaled_tc061_aux hY2 _ _)).sub
      (continuousOn_const.mul (continuousOn_finiteQLambda_scaled_tc061_aux hY2 _ _))
  have hQsq_cont : ContinuousOn (finiteQSquare T) (Set.uIcc Y (RiemannScope.tau * Y)) := by
    unfold finiteQSquare
    exact continuousOn_finset_sum _
      (fun r _ => continuousOn_gaussianTermPhi_uIcc_tc061_aux hY2 (r ^ 2))
  have hRjump_cont :
      ContinuousOn (jumpRemainderSumRjump c_lam T) (Set.uIcc Y (RiemannScope.tau * Y)) := by
    unfold jumpRemainderSumRjump scaledFiberCutoffJump
    exact continuousOn_finset_sum _ (fun d _ =>
      continuousOn_const.mul (continuousOn_const.mul
        ((continuousOn_finiteQLambda_scaled_tc061_aux hY2 _ _).sub
          (continuousOn_finiteQLambda_scaled_tc061_aux hY2 _ _))))
  have hQsh2_cont :
      ContinuousOn (finiteQShifted (fun n => (liouvilleLambda n : ℝ)) 2 T)
        (Set.uIcc Y (RiemannScope.tau * Y)) := by
    unfold finiteQShifted
    refine continuousOn_finset_sum _ (fun n hn => ?_)
    rw [Finset.mem_Icc] at hn
    have hn_pos : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr hn.1
    have h_div_ne : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), X / (n : ℝ) ≠ 0 :=
      fun X hX => ne_of_gt (div_pos (hpos X hX) hn_pos)
    exact (continuousOn_const.mul
      ((ContinuousOn.log (continuousOn_id.div_const (n : ℝ)) h_div_ne).pow 2)).mul
      (continuousOn_gaussianTermPhi_uIcc_tc061_aux hY2 n)
  have hA_cont :
      ContinuousOn (knownCompensatedD2Part c_lam c_half T D0)
        (Set.uIcc Y (RiemannScope.tau * Y)) := by
    unfold knownCompensatedD2Part
    refine (((((continuousOn_const.mul hQsq_cont).add
        (continuousOn_const.mul (continuousOn_gaussianTermPhi_uIcc_tc061_aux hY2 T))).add
        hRjump_cont).add
        (continuousOn_finset_sum _ (fun d _ => continuousOn_const.mul (h_sm_cont d)))).add
        (continuousOn_finset_sum _ (fun d _ => continuousOn_const.mul (h_sm_cont d)))).div
      (hlog_cont.pow 2) hlog_sq_ne
  have hO_cont :
      ContinuousOn (openCoreOscShiftD2Part c_lam c_half T D0)
        (Set.uIcc Y (RiemannScope.tau * Y)) := by
    unfold openCoreOscShiftD2Part
    refine ((continuousOn_finset_sum _ (fun d _ => continuousOn_const.mul (h_sm_cont d))).sub
      hQsh2_cont).div (hlog_cont.pow 2) hlog_sq_ne
  exact ⟨hQ_cont, hQgen_cont, hP_cont, hA_cont, hO_cont⟩

private theorem intervalIntegrable_window_pair_tc061_aux {Y : ℝ} (hY2 : 2 ≤ Y) {f g : ℝ → ℝ}
    (hf : ContinuousOn f (Set.uIcc Y (RiemannScope.tau * Y)))
    (hg : ContinuousOn g (Set.uIcc Y (RiemannScope.tau * Y))) :
    IntervalIntegrable (fun X => f X * g X / X) volume Y (RiemannScope.tau * Y) := by
  obtain ⟨_, hprops⟩ := uIcc_tau_props_tc061_aux hY2
  exact ((hf.mul hg).div continuousOn_id
    (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable

private theorem canonicalCutoffT_ge_one_tc061_aux {Y : ℝ} (hY2 : 2 ≤ Y) :
    1 ≤ canonicalCutoffT Y := by
  unfold canonicalCutoffT
  have hY_pos : 0 < Y := by linarith
  exact Nat.ceil_pos.mpr (Real.rpow_pos_of_pos hY_pos (5 / 4 : ℝ))

/-! ### Section 3: Public Theorem 1 (`mixed_covariance_identity_and_theta_energy_bound_tc061`) -/

/-- **Theorem 1 (`TASK-TC-061`, Mixed Covariance Window Norm Identity, Exact `θ`-Parameterized Energy Bound, and Canonical-Schedule Instantiation)**:
    For all `Y ≥ 2`, `T ≥ 1`, `D0 : ℕ`, and `c_lam, c_half : ℝ`:
    1. `windowEnergyNormSq Y (normalizedPrimePowerTermP T) = inheritedPrimePowerDiagDtilde T Y + inheritedPrimePowerOffDiagXtilde T Y`;
    2. Pointwise on `X ∈ Set.uIcc Y (RiemannScope.tau * Y)`:
       `2 * normalizedPrimePowerTermP T X - openCoreOscShiftD2Part c_lam c_half T D0 X = finiteQLambda T X + knownCompensatedD2Part c_lam c_half T D0 X`;
    3. Exact mixed window norm identity (with complete `IntervalIntegrable` verification on `[Y, RiemannScope.tau * Y]`):
       `4 * inheritedPrimePowerDiagDtilde T Y + signedMixedCovarianceJ c_lam c_half T D0 Y = windowEnergyNormSq Y (fun X => 2 * normalizedPrimePowerTermP T X - openCoreOscShiftD2Part c_lam c_half T D0 X)`,
       `= windowEnergyNormSq Y (fun X => finiteQLambda T X + knownCompensatedD2Part c_lam c_half T D0 X)`,
       and `0 ≤ 4 * inheritedPrimePowerDiagDtilde T Y + signedMixedCovarianceJ c_lam c_half T D0 Y`;
    4. Exact `θ`-inequality (`0 < θ < 1`):
       `(1 - θ) * actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) T Y ≤ 4 * inheritedPrimePowerDiagDtilde T Y + signedMixedCovarianceJ c_lam c_half T D0 Y + (θ⁻¹ - 1) * windowEnergyNormSq Y (knownCompensatedD2Part c_lam c_half T D0)`;
    5. Specialization at `θ = 1 / 2`:
       `actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) T Y ≤ 8 * inheritedPrimePowerDiagDtilde T Y + 2 * signedMixedCovarianceJ c_lam c_half T D0 Y + 2 * windowEnergyNormSq Y (knownCompensatedD2Part c_lam c_half T D0)`;
    6. Canonical-schedule instantiation (`T = canonicalCutoffT Y ≥ 1`, `D0 = ⌊log Y⌋`) for all `Y ≥ 2`. -/
theorem mixed_covariance_identity_and_theta_energy_bound_tc061 :
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T →
      windowEnergyNormSq Y (normalizedPrimePowerTermP T) =
        inheritedPrimePowerDiagDtilde T Y + inheritedPrimePowerOffDiagXtilde T Y) ∧
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
      ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
        2 * normalizedPrimePowerTermP T X - openCoreOscShiftD2Part c_lam c_half T D0 X =
          finiteQLambda T X + knownCompensatedD2Part c_lam c_half T D0 X) ∧
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
      4 * inheritedPrimePowerDiagDtilde T Y + signedMixedCovarianceJ c_lam c_half T D0 Y =
          windowEnergyNormSq Y
            (fun X =>
              2 * normalizedPrimePowerTermP T X -
                openCoreOscShiftD2Part c_lam c_half T D0 X) ∧
        windowEnergyNormSq Y
            (fun X =>
              2 * normalizedPrimePowerTermP T X -
                openCoreOscShiftD2Part c_lam c_half T D0 X) =
          windowEnergyNormSq Y
            (fun X => finiteQLambda T X + knownCompensatedD2Part c_lam c_half T D0 X) ∧
        0 ≤ 4 * inheritedPrimePowerDiagDtilde T Y + signedMixedCovarianceJ c_lam c_half T D0 Y) ∧
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ) {θ : ℝ},
      0 < θ → θ < 1 →
      (1 - θ) * actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) T Y ≤
        4 * inheritedPrimePowerDiagDtilde T Y + signedMixedCovarianceJ c_lam c_half T D0 Y +
          (θ⁻¹ - 1) * windowEnergyNormSq Y (knownCompensatedD2Part c_lam c_half T D0)) ∧
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
      actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) T Y ≤
        8 * inheritedPrimePowerDiagDtilde T Y +
          2 * signedMixedCovarianceJ c_lam c_half T D0 Y +
          2 * windowEnergyNormSq Y (knownCompensatedD2Part c_lam c_half T D0)) ∧
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ (c_lam c_half : ℝ),
      4 * canonicalPrimePowerDiagDtilde Y + canonicalSignedMixedCovarianceJ c_lam c_half Y =
          windowEnergyNormSq Y
            (fun X =>
              finiteQLambda (canonicalCutoffT Y) X +
                knownCompensatedD2Part c_lam c_half (canonicalCutoffT Y)
                  (Nat.floor (Real.log Y)) X) ∧
        actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) (canonicalCutoffT Y) Y ≤
          8 * canonicalPrimePowerDiagDtilde Y +
            2 * canonicalSignedMixedCovarianceJ c_lam c_half Y +
            2 *
              windowEnergyNormSq Y
                (knownCompensatedD2Part c_lam c_half (canonicalCutoffT Y)
                  (Nat.floor (Real.log Y)))) := by
  have h1 :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T →
        windowEnergyNormSq Y (normalizedPrimePowerTermP T) =
          inheritedPrimePowerDiagDtilde T Y + inheritedPrimePowerOffDiagXtilde T Y := by
    intro Y hY2 T _hT
    exact (full_core_quantified_obstructions_and_w2_support_tc060r).1.2.2.1 hY2 T
  have h2 :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
          2 * normalizedPrimePowerTermP T X - openCoreOscShiftD2Part c_lam c_half T D0 X =
            finiteQLambda T X + knownCompensatedD2Part c_lam c_half T D0 X := by
    intro Y hY2 T hT D0 c_lam c_half X hX
    obtain ⟨_, hprops⟩ := uIcc_tau_props_tc061_aux hY2
    have hQ := (complete_reconstruction_drift_contraction_transfer_tc060).1 hT D0 c_lam c_half
      (hprops X hX).2.1 (hprops X hX).2.2.2.1
    linarith [hQ.2]
  have h3 :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        4 * inheritedPrimePowerDiagDtilde T Y + signedMixedCovarianceJ c_lam c_half T D0 Y =
            windowEnergyNormSq Y
              (fun X =>
                2 * normalizedPrimePowerTermP T X -
                  openCoreOscShiftD2Part c_lam c_half T D0 X) ∧
          windowEnergyNormSq Y
              (fun X =>
                2 * normalizedPrimePowerTermP T X -
                  openCoreOscShiftD2Part c_lam c_half T D0 X) =
            windowEnergyNormSq Y
              (fun X => finiteQLambda T X + knownCompensatedD2Part c_lam c_half T D0 X) ∧
          0 ≤ 4 * inheritedPrimePowerDiagDtilde T Y + signedMixedCovarianceJ c_lam c_half T D0 Y := by
    intro Y hY2 T hT D0 c_lam c_half
    obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc061_aux hY2
    obtain ⟨_, _, hP_cont, _, hO_cont⟩ :=
      continuousOn_core_components_tc061_aux hY2 T D0 c_lam c_half
    have h_int_PP := intervalIntegrable_window_pair_tc061_aux hY2 hP_cont hP_cont
    have h_int_OO := intervalIntegrable_window_pair_tc061_aux hY2 hO_cont hO_cont
    have h_int_PO := intervalIntegrable_window_pair_tc061_aux hY2 hP_cont hO_cont
    have hP_split := h1 hY2 hT
    have h_comb_lhs :
        4 * inheritedPrimePowerDiagDtilde T Y + signedMixedCovarianceJ c_lam c_half T D0 Y =
          4 * windowEnergyNormSq Y (normalizedPrimePowerTermP T) +
            windowEnergyNormSq Y (openCoreOscShiftD2Part c_lam c_half T D0) -
            4 * windowPairing Y (normalizedPrimePowerTermP T)
              (openCoreOscShiftD2Part c_lam c_half T D0) := by
      unfold signedMixedCovarianceJ
      linarith [hP_split]
    have h_id1 :
        4 * inheritedPrimePowerDiagDtilde T Y + signedMixedCovarianceJ c_lam c_half T D0 Y =
          windowEnergyNormSq Y
            (fun X =>
              2 * normalizedPrimePowerTermP T X -
                openCoreOscShiftD2Part c_lam c_half T D0 X) := by
      rw [h_comb_lhs]
      unfold windowEnergyNormSq windowPairing
      rw [← intervalIntegral.integral_const_mul, ← intervalIntegral.integral_const_mul,
        ← intervalIntegral.integral_add (h_int_PP.const_mul 4) h_int_OO,
        ← intervalIntegral.integral_sub ((h_int_PP.const_mul 4).add h_int_OO)
          (h_int_PO.const_mul 4)]
      apply intervalIntegral.integral_congr
      intro X _
      ring
    have h_id2 :
        windowEnergyNormSq Y
            (fun X =>
              2 * normalizedPrimePowerTermP T X -
                openCoreOscShiftD2Part c_lam c_half T D0 X) =
          windowEnergyNormSq Y
            (fun X => finiteQLambda T X + knownCompensatedD2Part c_lam c_half T D0 X) := by
      unfold windowEnergyNormSq windowPairing
      apply intervalIntegral.integral_congr
      intro X hX
      dsimp only
      rw [h2 hY2 hT D0 c_lam c_half X hX]
    have h_nn :
        0 ≤ windowEnergyNormSq Y
          (fun X =>
            2 * normalizedPrimePowerTermP T X -
              openCoreOscShiftD2Part c_lam c_half T D0 X) := by
      unfold windowEnergyNormSq windowPairing
      apply intervalIntegral.integral_nonneg hle
      intro X hX
      have hX_uIcc : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
      have hX_pos : 0 < X := (hprops X hX_uIcc).2.1
      exact div_nonneg (mul_self_nonneg _) (le_of_lt hX_pos)
    exact ⟨h_id1, h_id2, by linarith⟩
  have h4 :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ) {θ : ℝ},
        0 < θ → θ < 1 →
        (1 - θ) * actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) T Y ≤
          4 * inheritedPrimePowerDiagDtilde T Y + signedMixedCovarianceJ c_lam c_half T D0 Y +
            (θ⁻¹ - 1) * windowEnergyNormSq Y (knownCompensatedD2Part c_lam c_half T D0) := by
    intro Y hY2 T hT D0 c_lam c_half θ hθ_pos _hθ_lt1
    obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc061_aux hY2
    obtain ⟨hQ_cont, hQgen_cont, _, hA_cont, _⟩ :=
      continuousOn_core_components_tc061_aux hY2 T D0 c_lam c_half
    have hQA_cont := hQ_cont.add hA_cont
    have h_int_Qgen := intervalIntegrable_window_pair_tc061_aux hY2 hQgen_cont hQgen_cont
    have h_int_QA := intervalIntegrable_window_pair_tc061_aux hY2 hQA_cont hQA_cont
    have h_int_AA := intervalIntegrable_window_pair_tc061_aux hY2 hA_cont hA_cont
    obtain ⟨h_id1, h_id2, _⟩ := h3 hY2 hT D0 c_lam c_half
    rw [h_id1, h_id2]
    unfold actualWindowEnergyE windowEnergyNormSq windowPairing
    rw [← intervalIntegral.integral_const_mul, ← intervalIntegral.integral_const_mul,
      ← intervalIntegral.integral_add h_int_QA (h_int_AA.const_mul (θ⁻¹ - 1))]
    apply intervalIntegral.integral_mono_on hle (h_int_Qgen.const_mul (1 - θ))
      (h_int_QA.add (h_int_AA.const_mul (θ⁻¹ - 1)))
    intro X hX
    have hX_uIcc : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
    have hX_pos : 0 < X := (hprops X hX_uIcc).2.1
    have hQ_eq : finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) T X = finiteQLambda T X := by
      unfold finiteQGeneral finiteQLambda gaussianTermPhi
      rw [Finset.mul_sum]; apply Finset.sum_congr rfl; intro n _; ring
    let q := finiteQLambda T X
    let a := knownCompensatedD2Part c_lam c_half T D0 X
    have hθ_ne : θ ≠ 0 := ne_of_gt hθ_pos
    have h_alg :
        θ * (((q + a) * (q + a) + (θ⁻¹ - 1) * (a * a)) - (1 - θ) * (q * q)) =
          (θ * q + a) ^ 2 := by
      have h_inv : θ * θ⁻¹ = 1 := mul_inv_cancel hθ_ne
      calc
        θ * (((q + a) * (q + a) + (θ⁻¹ - 1) * (a * a)) - (1 - θ) * (q * q))
          = (θ * θ⁻¹) * a ^ 2 + (θ ^ 2 * q ^ 2 + 2 * θ * q * a - 0 * a ^ 2) := by ring
        _ = (θ * q + a) ^ 2 := by rw [h_inv]; ring
    have h_quad_diff_nn :
        0 ≤ ((q + a) * (q + a) + (θ⁻¹ - 1) * (a * a)) - (1 - θ) * (q * q) := by
      have h_mul_nn :
          0 ≤ θ * (((q + a) * (q + a) + (θ⁻¹ - 1) * (a * a)) - (1 - θ) * (q * q)) := by
        rw [h_alg]; exact sq_nonneg _
      exact nonneg_of_mul_nonneg_right h_mul_nn hθ_pos
    have h_quad : (1 - θ) * (q * q) ≤ (q + a) * (q + a) + (θ⁻¹ - 1) * (a * a) := by
      linarith
    calc
      (1 - θ) *
          (finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) T X *
            finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) T X / X)
        = ((1 - θ) * (q * q)) / X := by rw [hQ_eq]; dsimp [q]; ring
      _ ≤ ((q + a) * (q + a) + (θ⁻¹ - 1) * (a * a)) / X :=
          div_le_div_of_nonneg_right h_quad (le_of_lt hX_pos)
      _ = (q + a) * (q + a) / X + (θ⁻¹ - 1) * (a * a / X) := by ring
  have h5 :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) T Y ≤
          8 * inheritedPrimePowerDiagDtilde T Y +
            2 * signedMixedCovarianceJ c_lam c_half T D0 Y +
            2 * windowEnergyNormSq Y (knownCompensatedD2Part c_lam c_half T D0) := by
    intro Y hY2 T hT D0 c_lam c_half
    have h_half :=
      h4 hY2 hT D0 c_lam c_half (θ := (1 / 2 : ℝ)) (by norm_num) (by norm_num)
    norm_num at h_half
    linarith
  refine ⟨h1, h2, h3, h4, h5, ?_⟩
  intro Y hY2 c_lam c_half
  have hT_can : 1 ≤ canonicalCutoffT Y := canonicalCutoffT_ge_one_tc061_aux hY2
  obtain ⟨h_c1, h_c2, _⟩ := h3 hY2 hT_can (Nat.floor (Real.log Y)) c_lam c_half
  have h_c5 := h5 hY2 hT_can (Nat.floor (Real.log Y)) c_lam c_half
  unfold canonicalPrimePowerDiagDtilde canonicalSignedMixedCovarianceJ
  exact ⟨h_c1.trans h_c2, h_c5⟩

/-! ### Section 4: Public Theorem 2 (`factorization_sign_agreement_and_selberg_w2_formulas_tc061`) -/

private theorem liouvilleLambda_mul_pos_tc061_aux {a b : ℕ} (ha : 1 ≤ a) (hb : 1 ≤ b) :
    (liouvilleLambda (a * b) : ℝ) = (liouvilleLambda a : ℝ) * (liouvilleLambda b : ℝ) := by
  have ha_ne : a ≠ 0 := by omega
  have hb_ne : b ≠ 0 := by omega
  have hab_ne : a * b ≠ 0 := mul_ne_zero ha_ne hb_ne
  have h_int : liouvilleLambda (a * b) = liouvilleLambda a * liouvilleLambda b := by
    simp [liouvilleLambda, ha_ne, hb_ne, hab_ne, natOmega,
      ArithmeticFunction.cardFactors_mul ha_ne hb_ne, liouvilleSignFromOmega, pow_add]
  exact_mod_cast h_int

private theorem liouvilleLambda_prime_pow_real_tc061_aux {p : ℕ} (hp : p.Prime) :
    ∀ k : ℕ, (liouvilleLambda (p ^ k) : ℝ) = (-1 : ℝ) ^ k
  | 0 => by simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
  | k + 1 => by
      have hp_pos : 1 ≤ p := hp.pos
      have hpk_pos : 1 ≤ p ^ k := Nat.one_le_pow k p hp.pos
      rw [pow_succ', liouvilleLambda_mul_pos_tc061_aux hp_pos hpk_pos,
        liouvilleLambda_prime_pow_real_tc061_aux hp k]
      have hop : natOmega p = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr hp
      have hlp : (liouvilleLambda p : ℝ) = -1 := by
        simp [liouvilleLambda, hp.ne_zero, hop, liouvilleSignFromOmega]
      rw [hlp, pow_succ']

private theorem selbergLiouvilleWeight2_factored_tc061_aux {n : ℕ} (hn : 1 ≤ n) :
    selbergLiouvilleWeight2 n =
      (liouvilleLambda n : ℝ) *
        (ArithmeticFunction.vonMangoldt n * Real.log (n : ℝ) +
          (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) n) := by
  obtain ⟨_, _, _, _, ⟨h_lv_mul, _, _, _⟩⟩ :=
    liouville_square_divisor_indicator_and_compensated_selberg_tc058 0 0
  rw [selbergLiouvilleWeight2, h_lv_mul n]
  have h_conv :
      (liouvilleVonMangoldt * liouvilleVonMangoldt) n =
        (liouvilleLambda n : ℝ) *
          (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) n := by
    rw [ArithmeticFunction.mul_apply, ArithmeticFunction.mul_apply, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro x hx
    rw [Nat.mem_divisorsAntidiagonal] at hx
    rcases hx with ⟨h_prod, _⟩
    have hx1_pos : 1 ≤ x.1 := by
      by_contra h0
      have hz : x.1 = 0 := by omega
      rw [hz, zero_mul] at h_prod
      omega
    have hx2_pos : 1 ≤ x.2 := by
      by_contra h0
      have hz : x.2 = 0 := by omega
      rw [hz, mul_zero] at h_prod
      omega
    rw [h_lv_mul x.1, h_lv_mul x.2, ← h_prod,
      liouvilleLambda_mul_pos_tc061_aux hx1_pos hx2_pos]
    ring
  rw [h_conv]
  ring

private theorem vonMangoldt_prime_pow_tc061_aux {p k : ℕ} (hp : p.Prime) (hk : 1 ≤ k) :
    ArithmeticFunction.vonMangoldt (p ^ k) = Real.log (p : ℝ) := by
  rw [ArithmeticFunction.vonMangoldt_apply_pow (by omega),
    ArithmeticFunction.vonMangoldt_apply_prime hp]

private theorem not_isPrimePow_of_two_primes_tc061_aux {m p q : ℕ}
    (hp : p.Prime) (hq : q.Prime) (hne : p ≠ q) (hpm : p ∣ m) (hqm : q ∣ m) :
    ¬ IsPrimePow m := by
  intro hpp
  obtain ⟨r, k, hr_pr, _, rfl⟩ := hpp
  have hr_nat : r.Prime := Nat.prime_iff.mpr hr_pr
  have h1 : p = r := (Nat.dvd_prime hr_nat).mp (hp.dvd_of_dvd_pow hpm) |>.resolve_left hp.ne_one
  have h2 : q = r := (Nat.dvd_prime hr_nat).mp (hq.dvd_of_dvd_pow hqm) |>.resolve_left hq.ne_one
  exact hne (h1.trans h2.symm)

/-- **Theorem 2 (`TASK-TC-061`, Prime-Power Factorization Sign Agreement and Exact `selbergLiouvilleWeight2` Prime-Power & Biprime-Power Formulas)**:
    1. Exact factorization sign agreement:
       - `∀ {m q : ℕ}, 1 ≤ m → 1 ≤ q → liouvilleVonMangoldt m * (liouvilleLambda q : ℝ) = (liouvilleLambda (m * q) : ℝ) * ArithmeticFunction.vonMangoldt m`;
       - `∀ {p k q : ℕ}, p.Prime → 1 ≤ k → 1 ≤ q → liouvilleVonMangoldt (p ^ k) * (liouvilleLambda q : ℝ) = (liouvilleLambda (p ^ k * q) : ℝ) * Real.log (p : ℝ)`;
       - `∀ {n : ℕ}, 1 ≤ n → (∑ d ∈ n.divisors, liouvilleVonMangoldt d * (liouvilleLambda (n / d) : ℝ)) = (liouvilleLambda n : ℝ) * Real.log (n : ℝ)`;
    2. Exact prime-power formula:
       `∀ {p k : ℕ}, p.Prime → 1 ≤ k → selbergLiouvilleWeight2 (p ^ k) = (-1 : ℝ) ^ k * (2 * (k : ℝ) - 1) * (Real.log (p : ℝ)) ^ 2`;
    3. Exact biprime-power formula:
       `∀ {p q a b : ℕ}, p.Prime → q.Prime → p ≠ q → 1 ≤ a → 1 ≤ b → selbergLiouvilleWeight2 (p ^ a * q ^ b) = 2 * (-1 : ℝ) ^ (a + b) * Real.log (p : ℝ) * Real.log (q : ℝ)`;
    4. Exact vanishing on integers with at least three distinct prime factors:
       `∀ {n q₁ q₂ q₃ : ℕ}, q₁.Prime → q₂.Prime → q₃.Prime → q₁ ≠ q₂ → q₁ ≠ q₃ → q₂ ≠ q₃ → q₁ ∣ n → q₂ ∣ n → q₃ ∣ n → selbergLiouvilleWeight2 n = 0`. -/
theorem factorization_sign_agreement_and_selberg_w2_formulas_tc061 :
    ((∀ {m q : ℕ}, 1 ≤ m → 1 ≤ q →
        liouvilleVonMangoldt m * (liouvilleLambda q : ℝ) =
          (liouvilleLambda (m * q) : ℝ) * ArithmeticFunction.vonMangoldt m) ∧
      (∀ {p k q : ℕ}, p.Prime → 1 ≤ k → 1 ≤ q →
        liouvilleVonMangoldt (p ^ k) * (liouvilleLambda q : ℝ) =
          (liouvilleLambda (p ^ k * q) : ℝ) * Real.log (p : ℝ)) ∧
      (∀ {n : ℕ}, 1 ≤ n →
        (∑ d ∈ n.divisors, liouvilleVonMangoldt d * (liouvilleLambda (n / d) : ℝ)) =
          (liouvilleLambda n : ℝ) * Real.log (n : ℝ))) ∧
    (∀ {p k : ℕ}, p.Prime → 1 ≤ k →
      selbergLiouvilleWeight2 (p ^ k) =
        (-1 : ℝ) ^ k * (2 * (k : ℝ) - 1) * (Real.log (p : ℝ)) ^ 2) ∧
    (∀ {p q a b : ℕ}, p.Prime → q.Prime → p ≠ q → 1 ≤ a → 1 ≤ b →
      selbergLiouvilleWeight2 (p ^ a * q ^ b) =
        2 * (-1 : ℝ) ^ (a + b) * Real.log (p : ℝ) * Real.log (q : ℝ)) ∧
    (∀ {n q₁ q₂ q₃ : ℕ},
      q₁.Prime → q₂.Prime → q₃.Prime →
      q₁ ≠ q₂ → q₁ ≠ q₃ → q₂ ≠ q₃ →
      q₁ ∣ n → q₂ ∣ n → q₃ ∣ n →
      selbergLiouvilleWeight2 n = 0) := by
  obtain ⟨_, _, _, _, ⟨h_lv_mul, _, _, _⟩⟩ :=
    liouville_square_divisor_indicator_and_compensated_selberg_tc058 0 0
  have h_sign_gen :
      ∀ {m q : ℕ}, 1 ≤ m → 1 ≤ q →
        liouvilleVonMangoldt m * (liouvilleLambda q : ℝ) =
          (liouvilleLambda (m * q) : ℝ) * ArithmeticFunction.vonMangoldt m := by
    intro m q hm hq
    rw [h_lv_mul m, liouvilleLambda_mul_pos_tc061_aux hm hq]
    ring
  have h_sign_pp :
      ∀ {p k q : ℕ}, p.Prime → 1 ≤ k → 1 ≤ q →
        liouvilleVonMangoldt (p ^ k) * (liouvilleLambda q : ℝ) =
          (liouvilleLambda (p ^ k * q) : ℝ) * Real.log (p : ℝ) := by
    intro p k q hp hk hq
    rw [h_sign_gen (Nat.one_le_pow k p hp.pos) hq, vonMangoldt_prime_pow_tc061_aux hp hk]
  have h_sign_div :
      ∀ {n : ℕ}, 1 ≤ n →
        (∑ d ∈ n.divisors, liouvilleVonMangoldt d * (liouvilleLambda (n / d) : ℝ)) =
          (liouvilleLambda n : ℝ) * Real.log (n : ℝ) := by
    intro n hn
    have h_each :
        ∀ d ∈ n.divisors,
          liouvilleVonMangoldt d * (liouvilleLambda (n / d) : ℝ) =
            (liouvilleLambda n : ℝ) * ArithmeticFunction.vonMangoldt d := by
      intro d hd
      rw [Nat.mem_divisors] at hd
      have hd_pos : 1 ≤ d := Nat.pos_of_dvd_of_pos hd.1 hn
      have hq_pos : 1 ≤ n / d := Nat.div_pos (Nat.le_of_dvd hn hd.1) hd_pos
      rw [h_sign_gen hd_pos hq_pos, Nat.mul_div_cancel' hd.1]
    rw [Finset.sum_congr rfl h_each, ← Finset.mul_sum, ArithmeticFunction.vonMangoldt_sum]
  refine ⟨⟨h_sign_gen, h_sign_pp, h_sign_div⟩, ?_, ?_, ?_⟩
  · intro p k hp hk
    have hpk_pos : 1 ≤ p ^ k := Nat.one_le_pow k p hp.pos
    rw [selbergLiouvilleWeight2_factored_tc061_aux hpk_pos,
      liouvilleLambda_prime_pow_real_tc061_aux hp k,
      vonMangoldt_prime_pow_tc061_aux hp hk]
    have h_log_pk : Real.log ((p ^ k : ℕ) : ℝ) = (k : ℝ) * Real.log (p : ℝ) := by
      push_cast; exact Real.log_pow (p : ℝ) k
    have h_conv_pk :
        (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) (p ^ k) =
          ((k : ℝ) - 1) * (Real.log (p : ℝ)) ^ 2 := by
      rw [ArithmeticFunction.mul_apply,
        Nat.sum_divisorsAntidiagonal
          (fun i j => ArithmeticFunction.vonMangoldt i * ArithmeticFunction.vonMangoldt j),
        Nat.sum_divisors_prime_pow hp]
      have h_range_eq :
          (∑ j ∈ Finset.range (k + 1),
              ArithmeticFunction.vonMangoldt (p ^ j) *
                ArithmeticFunction.vonMangoldt (p ^ k / p ^ j)) =
            ∑ j ∈ Finset.Icc 1 (k - 1), (Real.log (p : ℝ)) ^ 2 := by
        have h_sub : Finset.Icc 1 (k - 1) ⊆ Finset.range (k + 1) := by
          intro j hj
          rw [Finset.mem_Icc] at hj
          rw [Finset.mem_range]
          omega
        rw [← Finset.sum_subset h_sub]
        · apply Finset.sum_congr rfl
          intro j hj
          rw [Finset.mem_Icc] at hj
          have hj_le : j ≤ k := by omega
          rw [Nat.pow_div hj_le hp.pos, vonMangoldt_prime_pow_tc061_aux hp hj.1,
            vonMangoldt_prime_pow_tc061_aux hp (by omega)]
          ring
        · intro j hj_r hj_not
          rw [Finset.mem_range] at hj_r
          rw [Finset.mem_Icc] at hj_not
          rcases eq_or_ne j 0 with rfl | hj_ne0
          · simp [ArithmeticFunction.vonMangoldt_apply_one]
          · have hjk : j = k := by omega
            subst hjk
            rw [Nat.div_self hpk_pos, ArithmeticFunction.vonMangoldt_apply_one, mul_zero]
      rw [h_range_eq, Finset.sum_const, Nat.card_Icc]
      have h_cnt : ((k - 1 + 1 - 1 : ℕ) : ℝ) = (k : ℝ) - 1 := by
        have h_nat : k - 1 + 1 - 1 = k - 1 := by omega
        rw [h_nat, Nat.cast_sub hk, Nat.cast_one]
      simp only [nsmul_eq_mul, h_cnt]
    rw [h_log_pk, h_conv_pk]
    ring
  · intro p q a b hp hq hne ha hb
    have hpa_pos : 1 ≤ p ^ a := Nat.one_le_pow a p hp.pos
    have hqb_pos : 1 ≤ q ^ b := Nat.one_le_pow b q hq.pos
    have hn_pos : 1 ≤ p ^ a * q ^ b := Nat.mul_pos hpa_pos hqb_pos
    rw [selbergLiouvilleWeight2_factored_tc061_aux hn_pos]
    have h_lam_ab : (liouvilleLambda (p ^ a * q ^ b) : ℝ) = (-1 : ℝ) ^ (a + b) := by
      rw [liouvilleLambda_mul_pos_tc061_aux hpa_pos hqb_pos,
        liouvilleLambda_prime_pow_real_tc061_aux hp a,
        liouvilleLambda_prime_pow_real_tc061_aux hq b, pow_add]
    have hp_dvd_pa : p ∣ p ^ a := dvd_pow_self p (by omega)
    have hq_dvd_qb : q ∣ q ^ b := dvd_pow_self q (by omega)
    have h_vm_zero : ArithmeticFunction.vonMangoldt (p ^ a * q ^ b) = 0 := by
      apply ArithmeticFunction.vonMangoldt_eq_zero_iff.mpr
      exact not_isPrimePow_of_two_primes_tc061_aux hp hq hne
        (dvd_mul_of_dvd_left hp_dvd_pa (q ^ b)) (dvd_mul_of_dvd_right hq_dvd_qb (p ^ a))
    have hcop_pq : Nat.Coprime p q :=
      (hp.coprime_iff_not_dvd).mpr (fun hdvd =>
        hne ((Nat.dvd_prime hq).mp hdvd |>.resolve_left hp.ne_one))
    have hpa_ne_qb : p ^ a ≠ q ^ b := by
      intro heq
      have hp_dvd_qb : p ∣ q ^ b := by rw [← heq]; exact hp_dvd_pa
      exact hne ((Nat.dvd_prime hq).mp (hp.dvd_of_dvd_pow hp_dvd_qb) |>.resolve_left hp.ne_one)
    have h_pair_sub :
        ({(p ^ a, q ^ b), (q ^ b, p ^ a)} : Finset (ℕ × ℕ)) ⊆
          (p ^ a * q ^ b).divisorsAntidiagonal := by
      intro x hx
      simp only [Finset.mem_insert, Finset.mem_singleton] at hx
      rw [Nat.mem_divisorsAntidiagonal]
      rcases hx with rfl | rfl
      · exact ⟨rfl, by omega⟩
      · exact ⟨mul_comm (q ^ b) (p ^ a), by omega⟩
    have h_conv_ab :
        (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) (p ^ a * q ^ b) =
          2 * Real.log (p : ℝ) * Real.log (q : ℝ) := by
      rw [ArithmeticFunction.mul_apply, ← Finset.sum_subset h_pair_sub]
      · have h_pair_ne : (p ^ a, q ^ b) ≠ (q ^ b, p ^ a) :=
          fun h => hpa_ne_qb (Prod.mk.inj h).1
        rw [Finset.sum_pair h_pair_ne,
          vonMangoldt_prime_pow_tc061_aux hp ha,
          vonMangoldt_prime_pow_tc061_aux hq hb]
        ring
      · intro x hx_anti hx_not
        rw [Nat.mem_divisorsAntidiagonal] at hx_anti
        simp only [Finset.mem_insert, Finset.mem_singleton, not_or] at hx_not
        rcases hx_anti with ⟨h_prod, _⟩
        by_cases h1 : IsPrimePow x.1
        · by_cases h2 : IsPrimePow x.2
          · exfalso
            obtain ⟨r1, k1, hr1_pr, hk1_pos, hx1_eq⟩ := h1
            obtain ⟨r2, k2, hr2_pr, _hk2_pos, hx2_eq⟩ := h2
            have hr1 : r1.Prime := Nat.prime_iff.mpr hr1_pr
            have hr2 : r2.Prime := Nat.prime_iff.mpr hr2_pr
            have hr1_dvd_prod : r1 ∣ p ^ a * q ^ b := by
              rw [← h_prod, ← hx1_eq]
              exact dvd_mul_of_dvd_left (dvd_pow_self r1 (by omega)) x.2
            rcases hr1.dvd_mul.mp hr1_dvd_prod with hr1_pa | hr1_qb
            · have hr1_eq_p : r1 = p :=
                (Nat.dvd_prime hp).mp (hr1.dvd_of_dvd_pow hr1_pa) |>.resolve_left hr1.ne_one
              have hx1_p : x.1 = p ^ k1 := by rw [← hx1_eq, hr1_eq_p]
              have hq_dvd_x2 : q ∣ x.2 := by
                have hq_prod : q ∣ p ^ k1 * x.2 := by
                  rw [← hx1_p, h_prod]
                  exact dvd_mul_of_dvd_right hq_dvd_qb (p ^ a)
                exact (hcop_pq.symm.pow_right k1).dvd_of_dvd_mul_left hq_prod
              have hq_dvd_r2k2 : q ∣ r2 ^ k2 := by rwa [hx2_eq]
              have hq_eq_r2 : q = r2 :=
                (Nat.dvd_prime hr2).mp (hq.dvd_of_dvd_pow hq_dvd_r2k2) |>.resolve_left hq.ne_one
              have hx2_q : x.2 = q ^ k2 := by rw [← hx2_eq, ← hq_eq_r2]
              have h_pa_dvd_x1 : p ^ a ∣ x.1 := by
                have h_dvd : p ^ a ∣ p ^ k1 * q ^ k2 := by
                  rw [← hx1_p, ← hx2_q, h_prod]; exact dvd_mul_right _ _
                rw [hx1_p]
                exact (hcop_pq.pow a k2).dvd_of_dvd_mul_right h_dvd
              have h_x1_dvd_pa : x.1 ∣ p ^ a := by
                have h_dvd : p ^ k1 ∣ p ^ a * q ^ b := by
                  rw [← h_prod, hx1_p]; exact dvd_mul_right _ _
                rw [hx1_p]
                exact (hcop_pq.pow k1 b).dvd_of_dvd_mul_right h_dvd
              have hx1_pa : x.1 = p ^ a := Nat.dvd_antisymm h_x1_dvd_pa h_pa_dvd_x1
              have hx2_qb : x.2 = q ^ b := by
                apply Nat.eq_of_mul_eq_mul_left hpa_pos
                calc
                  p ^ a * x.2 = x.1 * x.2 := by rw [hx1_pa]
                  _ = p ^ a * q ^ b := h_prod
              exact hx_not.1 (Prod.ext hx1_pa hx2_qb)
            · have hr1_eq_q : r1 = q :=
                (Nat.dvd_prime hq).mp (hr1.dvd_of_dvd_pow hr1_qb) |>.resolve_left hr1.ne_one
              have hx1_q : x.1 = q ^ k1 := by rw [← hx1_eq, hr1_eq_q]
              have hp_dvd_x2 : p ∣ x.2 := by
                have hp_prod : p ∣ q ^ k1 * x.2 := by
                  rw [← hx1_q, h_prod]
                  exact dvd_mul_of_dvd_left hp_dvd_pa (q ^ b)
                exact (hcop_pq.pow_right k1).dvd_of_dvd_mul_left hp_prod
              have hp_dvd_r2k2 : p ∣ r2 ^ k2 := by rwa [hx2_eq]
              have hp_eq_r2 : p = r2 :=
                (Nat.dvd_prime hr2).mp (hp.dvd_of_dvd_pow hp_dvd_r2k2) |>.resolve_left hp.ne_one
              have hx2_p : x.2 = p ^ k2 := by rw [← hx2_eq, ← hp_eq_r2]
              have h_qb_dvd_x1 : q ^ b ∣ x.1 := by
                have h_dvd : q ^ b ∣ q ^ k1 * p ^ k2 := by
                  rw [← hx1_q, ← hx2_p, h_prod]; exact dvd_mul_left _ _
                rw [hx1_q]
                exact (hcop_pq.symm.pow b k2).dvd_of_dvd_mul_right h_dvd
              have h_x1_dvd_qb : x.1 ∣ q ^ b := by
                have h_dvd : q ^ k1 ∣ p ^ a * q ^ b := by
                  rw [← h_prod, hx1_q]; exact dvd_mul_right _ _
                rw [hx1_q]
                exact (hcop_pq.symm.pow k1 a).dvd_of_dvd_mul_left h_dvd
              have hx1_qb : x.1 = q ^ b := Nat.dvd_antisymm h_x1_dvd_qb h_qb_dvd_x1
              have hx2_pa : x.2 = p ^ a := by
                apply Nat.eq_of_mul_eq_mul_left hqb_pos
                calc
                  q ^ b * x.2 = x.1 * x.2 := by rw [hx1_qb]
                  _ = p ^ a * q ^ b := h_prod
                  _ = q ^ b * p ^ a := mul_comm _ _
              exact hx_not.2 (Prod.ext hx1_qb hx2_pa)
          · rw [ArithmeticFunction.vonMangoldt_eq_zero_iff.mpr h2, mul_zero]
        · rw [ArithmeticFunction.vonMangoldt_eq_zero_iff.mpr h1, zero_mul]
    rw [h_lam_ab, h_vm_zero, zero_mul, zero_add, h_conv_ab]
    ring
  · exact full_core_quantified_obstructions_and_w2_support_tc060r.2.2.2.1.2.2.1

/-! ### Section 5: Public Theorem 3 (`finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061`) -/

private theorem mem_primePowerPairsUpTo_iff_tc061_aux {M : ℕ} {pk : ℕ × ℕ} :
    pk ∈ primePowerPairsUpTo M ↔ pk.1.Prime ∧ 1 ≤ pk.2 ∧ pk.1 ^ pk.2 ≤ M := by
  simp only [primePowerPairsUpTo, primesUpToFinset, Finset.mem_filter, Finset.mem_product,
    Finset.mem_Icc]
  constructor
  · rintro ⟨⟨⟨_, hp⟩, ⟨hk1, _⟩⟩, hle⟩
    exact ⟨hp, hk1, hle⟩
  · rintro ⟨hp, hk1, hle⟩
    have hp_le : pk.1 ≤ pk.1 ^ pk.2 := by
      simpa using Nat.pow_le_pow_right hp.pos hk1
    have hk_lt : pk.2 < pk.1 ^ pk.2 := Nat.lt_pow_self hp.one_lt pk.2
    exact ⟨⟨⟨⟨hp.two_le, le_trans hp_le hle⟩, hp⟩, ⟨hk1, by omega⟩⟩, hle⟩

private theorem scaled_finiteQLambda_reindexed_tc061_aux (T : ℕ) {pk : ℕ × ℕ}
    (hp : pk.1.Prime) {X : ℝ} (hX_pos : 0 < X) :
    (1 / Real.sqrt ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
        finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ)) =
      (liouvilleLambda (pk.1 ^ pk.2) : ℝ) *
        ∑ m ∈ (Finset.Icc 1 T).filter (fun m => pk.1 ^ pk.2 ∣ m),
          (liouvilleLambda m : ℝ) * gaussianTermPhi m X := by
  let d := pk.1 ^ pk.2
  have hd_pos : 1 ≤ d := Nat.one_le_pow pk.2 pk.1 hp.pos
  obtain ⟨_, _, h_dil, _, _⟩ := window_integrability_and_kernel_scaling_tc059 zero_lt_one
  have hQ_eq :
      finiteQLambda (T / d) (X / (d : ℝ)) =
        ∑ q ∈ Finset.Icc 1 (T / d), (liouvilleLambda q : ℝ) * gaussianTermPhi q (X / (d : ℝ)) := by
    dsimp [finiteQLambda, gaussianTermPhi]
    rw [Finset.mul_sum]; apply Finset.sum_congr rfl; intro q _; ring
  rw [show pk.1 ^ pk.2 = d from rfl, hQ_eq, Finset.mul_sum, Finset.mul_sum]
  apply Finset.sum_bij (fun q _ => d * q)
  · intro q hq
    rw [Finset.mem_Icc] at hq
    simp only [Finset.mem_filter, Finset.mem_Icc]
    have h_le : d * q ≤ T := by
      rw [mul_comm]
      exact (Nat.le_div_iff_mul_le hd_pos).mp hq.2
    exact ⟨⟨Nat.mul_pos hd_pos hq.1, h_le⟩, ⟨q, rfl⟩⟩
  · intro q1 _ q2 _ heq
    exact Nat.eq_of_mul_eq_mul_left hd_pos heq
  · intro m hm
    simp only [Finset.mem_filter, Finset.mem_Icc] at hm
    rcases hm with ⟨⟨hm1, hmT⟩, ⟨q, rfl⟩⟩
    have hq_pos : 1 ≤ q := by
      by_contra h0
      have hz : q = 0 := by omega
      rw [hz, mul_zero] at hm1
      omega
    have hq_le : q ≤ T / d := (Nat.le_div_iff_mul_le hd_pos).mpr (by rw [mul_comm]; exact hmT)
    exact ⟨q, Finset.mem_Icc.mpr ⟨hq_pos, hq_le⟩, rfl⟩
  · intro q hq
    rw [Finset.mem_Icc] at hq
    have h_lam_sq : (liouvilleLambda d : ℝ) * (liouvilleLambda d : ℝ) = 1 := by
      rw [show d = pk.1 ^ pk.2 from rfl, liouvilleLambda_prime_pow_real_tc061_aux hp pk.2,
        ← pow_add, show pk.2 + pk.2 = 2 * pk.2 by omega, pow_mul]
      norm_num
    rw [liouvilleLambda_mul_pos_tc061_aux hd_pos hq.1,
      h_dil hd_pos q (le_of_lt hX_pos)]
    calc
      1 / Real.sqrt (d : ℝ) * ((liouvilleLambda q : ℝ) * gaussianTermPhi q (X / (d : ℝ)))
        = 1 * ((liouvilleLambda q : ℝ) *
            ((1 / Real.sqrt (d : ℝ)) * gaussianTermPhi q (X / (d : ℝ)))) := by ring
      _ = ((liouvilleLambda d : ℝ) * (liouvilleLambda d : ℝ)) *
            ((liouvilleLambda q : ℝ) *
              ((1 / Real.sqrt (d : ℝ)) * gaussianTermPhi q (X / (d : ℝ)))) := by
          rw [h_lam_sq]
      _ = (liouvilleLambda d : ℝ) *
            ((liouvilleLambda d : ℝ) * (liouvilleLambda q : ℝ) *
              (1 / Real.sqrt (d : ℝ) * gaussianTermPhi q (X / (d : ℝ)))) := by ring

private theorem pointwisePrimePowerDiagNorm_kernel_expand_tc061_aux (T : ℕ) {X : ℝ}
    (hX_pos : 0 < X) :
    pointwisePrimePowerDiagNorm T X / X =
      ∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T,
        (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
          ((gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ 2) / X) := by
  have h_num :
      (∑ pk ∈ primePowerPairsUpTo T,
          ((Real.log (pk.1 : ℝ)) ^ 2 / ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
            (finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ))) ^ 2) =
        ∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T,
          (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
            (gaussianTermPhi m X * gaussianTermPhi n X) := by
    have h_each_pk :
        ∀ pk ∈ primePowerPairsUpTo T,
          ((Real.log (pk.1 : ℝ)) ^ 2 / ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
              (finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ))) ^ 2 =
            ∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T,
              if pk.1 ^ pk.2 ∣ m ∧ pk.1 ^ pk.2 ∣ n then
                (Real.log (pk.1 : ℝ)) ^ 2 *
                  ((liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                    (gaussianTermPhi m X * gaussianTermPhi n X))
              else 0 := by
      intro pk hpk
      obtain ⟨hp, _, _⟩ := mem_primePowerPairsUpTo_iff_tc061_aux.mp hpk
      have hd_nn : (0 : ℝ) ≤ ((pk.1 ^ pk.2 : ℕ) : ℝ) := Nat.cast_nonneg _
      have h_sqrt_sq : (Real.sqrt ((pk.1 ^ pk.2 : ℕ) : ℝ)) ^ 2 = ((pk.1 ^ pk.2 : ℕ) : ℝ) :=
        Real.sq_sqrt hd_nn
      have h_lam_sq :
          (liouvilleLambda (pk.1 ^ pk.2) : ℝ) ^ 2 = 1 := by
        rw [liouvilleLambda_prime_pow_real_tc061_aux hp pk.2, ← pow_mul, mul_comm]
        norm_num
      have h_reind := scaled_finiteQLambda_reindexed_tc061_aux T hp hX_pos
      have h_sq_reind :
          (1 / ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
              (finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ))) ^ 2 =
            ∑ m ∈ (Finset.Icc 1 T).filter (fun m => pk.1 ^ pk.2 ∣ m),
              ∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
                ((liouvilleLambda m : ℝ) * gaussianTermPhi m X) *
                  ((liouvilleLambda n : ℝ) * gaussianTermPhi n X) := by
        have h_lhs :
            (1 / ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
                (finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ))) ^ 2 =
              ((1 / Real.sqrt ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
                finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ))) ^ 2 := by
          rw [mul_pow, div_pow, one_pow, h_sqrt_sq]
        rw [h_lhs, h_reind, mul_pow, h_lam_sq, one_mul, sq, Finset.sum_mul_sum]
      have h_prod_eq :
          ((Real.log (pk.1 : ℝ)) ^ 2 / ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
              (finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ))) ^ 2 =
            (Real.log (pk.1 : ℝ)) ^ 2 *
              ((1 / ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
                (finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ))) ^ 2) := by ring
      rw [h_prod_eq, h_sq_reind, Finset.mul_sum]
      simp only [Finset.sum_filter]
      apply Finset.sum_congr rfl
      intro m _
      by_cases hm : pk.1 ^ pk.2 ∣ m
      · rw [if_pos hm, Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro n _
        by_cases hn : pk.1 ^ pk.2 ∣ n
        · rw [if_pos hn, if_pos ⟨hm, hn⟩]; ring
        · rw [if_neg hn, if_neg (fun h => hn h.2), mul_zero]
      · simp [hm]
    rw [Finset.sum_congr rfl h_each_pk, Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro m hm
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro n hn
    rw [Finset.mem_Icc] at hm hn
    have h_filt_eq :
        (primePowerPairsUpTo T).filter (fun pk => pk.1 ^ pk.2 ∣ m ∧ pk.1 ^ pk.2 ∣ n) =
          (primePowerPairsUpTo (min m n)).filter (fun pk => (pk.1 ^ pk.2) ∣ Nat.gcd m n) := by
      ext pk
      simp only [Finset.mem_filter, mem_primePowerPairsUpTo_iff_tc061_aux, Nat.dvd_gcd_iff]
      constructor
      · rintro ⟨⟨hp, hk1, _⟩, hdm, hdn⟩
        exact ⟨⟨hp, hk1, le_min (Nat.le_of_dvd hm.1 hdm) (Nat.le_of_dvd hn.1 hdn)⟩, hdm, hdn⟩
      · rintro ⟨⟨hp, hk1, hmin⟩, hdm, hdn⟩
        exact ⟨⟨hp, hk1, le_trans hmin (le_trans (min_le_left m n) hm.2)⟩, hdm, hdn⟩
    have h_inner :
        (∑ pk ∈ primePowerPairsUpTo T,
            if pk.1 ^ pk.2 ∣ m ∧ pk.1 ^ pk.2 ∣ n then
              (Real.log (pk.1 : ℝ)) ^ 2 *
                ((liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                  (gaussianTermPhi m X * gaussianTermPhi n X))
            else 0) =
          (∑ pk ∈ (primePowerPairsUpTo T).filter (fun pk => pk.1 ^ pk.2 ∣ m ∧ pk.1 ^ pk.2 ∣ n),
              (Real.log (pk.1 : ℝ)) ^ 2) *
            ((liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
              (gaussianTermPhi m X * gaussianTermPhi n X)) := by
      rw [← Finset.sum_filter, Finset.sum_mul]
    rw [h_inner, h_filt_eq]
    unfold commonPrimePowerLogSq
    ring
  unfold pointwisePrimePowerDiagNorm
  rw [h_num, Finset.sum_div, Finset.sum_div]
  apply Finset.sum_congr rfl
  intro m _
  rw [Finset.sum_div, Finset.sum_div]
  apply Finset.sum_congr rfl
  intro n _
  ring

private theorem half_le_log_two_tc061_aux : (1 / 2 : ℝ) ≤ Real.log (2 : ℝ) := by
  have h1 : (1 / 2 : ℝ) ≤ Real.exp (-1 / 2 : ℝ) := by
    linarith [Real.add_one_le_exp (-1 / 2 : ℝ)]
  have h_pos : 0 < Real.exp (1 / 2 : ℝ) := Real.exp_pos _
  have h_prod : Real.exp (1 / 2 : ℝ) * Real.exp (-1 / 2 : ℝ) = 1 := by
    rw [← Real.exp_add]; norm_num
  have h2 : Real.exp (1 / 2 : ℝ) ≤ 2 := by
    have hm := mul_le_mul_of_nonneg_left h1 (le_of_lt h_pos)
    rw [h_prod] at hm
    linarith
  have hlog := Real.log_le_log h_pos h2
  rwa [Real.log_exp] at hlog

private theorem sum_inv_sq_Icc_succ_le_inv_tc061_aux {M : ℕ} (hM : 1 ≤ M) (T : ℕ) :
    (∑ n ∈ Finset.Icc (M + 1) T, (1 / (n : ℝ) ^ 2)) ≤ 1 / (M : ℝ) := by
  by_cases hMT : M + 1 ≤ T
  · obtain ⟨L, rfl⟩ : ∃ L : ℕ, T = M + 1 + L := ⟨T - (M + 1), by omega⟩
    have h_term :
        ∀ n ∈ Finset.Icc (M + 1) (M + 1 + L),
          (1 / (n : ℝ) ^ 2) ≤ 1 / ((n - 1 : ℕ) : ℝ) - 1 / (n : ℝ) := by
      intro n hn
      rw [Finset.mem_Icc] at hn
      have hn2 : 2 ≤ n := by omega
      have hn_pos : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr (by omega)
      have hnm1_eq : ((n - 1 : ℕ) : ℝ) = (n : ℝ) - 1 := by
        rw [Nat.cast_sub (by omega : 1 ≤ n), Nat.cast_one]
      have hnm1_pos : (0 : ℝ) < (n : ℝ) - 1 := by
        have h2r : (2 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn2
        linarith
      rw [hnm1_eq]
      have h_diff :
          (1 / ((n : ℝ) - 1) - 1 / (n : ℝ)) - 1 / (n : ℝ) ^ 2 =
            1 / ((n : ℝ) ^ 2 * ((n : ℝ) - 1)) := by
        field_simp [ne_of_gt hn_pos, ne_of_gt hnm1_pos]
        ring
      have h_nn : 0 ≤ 1 / ((n : ℝ) ^ 2 * ((n : ℝ) - 1)) := by positivity
      linarith
    have h_sum_le := Finset.sum_le_sum h_term
    have h_tele :
        ∀ m : ℕ,
          (∑ n ∈ Finset.Icc (M + 1) (M + 1 + m), (1 / ((n - 1 : ℕ) : ℝ) - 1 / (n : ℝ))) =
            1 / (M : ℝ) - 1 / ((M + 1 + m : ℕ) : ℝ) := by
      intro m
      induction' m with m ih
      · simp
      · have h_ins :
            Finset.Icc (M + 1) (M + 1 + (m + 1)) =
              insert (M + 1 + m + 1) (Finset.Icc (M + 1) (M + 1 + m)) := by
          ext x; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
        have h_not : (M + 1 + m + 1) ∉ Finset.Icc (M + 1) (M + 1 + m) := by
          simp only [Finset.mem_Icc]; omega
        rw [h_ins, Finset.sum_insert h_not, ih]
        have h_sub1 : M + 1 + m + 1 - 1 = M + 1 + m := by omega
        have h_eq1 : M + 1 + (m + 1) = M + 1 + m + 1 := by omega
        rw [h_sub1, h_eq1]
        ring
    rw [h_tele L] at h_sum_le
    have h_tail_nn : 0 ≤ 1 / ((M + 1 + L : ℕ) : ℝ) := by positivity
    linarith
  · have h_empty : Finset.Icc (M + 1) T = ∅ := by
      ext x; simp only [Finset.mem_Icc, Finset.not_mem_empty, iff_false]; omega
    rw [h_empty, Finset.sum_empty]
    positivity

private theorem gaussianTermPhi_sq_formula_tc061_aux {n : ℕ} (hn : 1 ≤ n) {X : ℝ}
    (hX_pos : 0 < X) :
    (gaussianTermPhi n X) ^ 2 =
      (1 / (n : ℝ)) * (X / (n : ℝ)) ^ 5 * Real.exp (-2 * (X / (n : ℝ)) ^ 2) := by
  have hn_pos : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr hn
  have hX5 : (X ^ (5 / 2 : ℝ)) ^ 2 = X ^ 5 := by
    rw [← Real.rpow_natCast (X ^ (5 / 2 : ℝ)) 2, ← Real.rpow_mul (le_of_lt hX_pos)]
    have h5 : (5 / 2 : ℝ) * ((2 : ℕ) : ℝ) = ((5 : ℕ) : ℝ) := by norm_num
    rw [h5, Real.rpow_natCast]
  have hexp2 :
      (Real.exp (-(X ^ 2) / (n : ℝ) ^ 2)) ^ 2 = Real.exp (-2 * (X / (n : ℝ)) ^ 2) := by
    rw [← Real.exp_nat_mul]
    congr 1; push_cast; ring
  unfold gaussianTermPhi
  rw [mul_pow, mul_pow, hX5, hexp2]
  field_simp [ne_of_gt hn_pos]
  ring

private theorem log_nat_sq_split_tc061_aux {n : ℕ} (hn : 1 ≤ n) {X : ℝ} (hX_pos : 0 < X) :
    (Real.log (n : ℝ)) ^ 2 ≤ 2 * (Real.log X) ^ 2 + 2 * (Real.log (X / (n : ℝ))) ^ 2 := by
  have hn_pos : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr hn
  have h_div : Real.log (X / (n : ℝ)) = Real.log X - Real.log (n : ℝ) :=
    Real.log_div (ne_of_gt hX_pos) (ne_of_gt hn_pos)
  have h_eq : Real.log (n : ℝ) = Real.log X - Real.log (X / (n : ℝ)) := by linarith
  rw [h_eq]
  nlinarith [sq_nonneg (Real.log X + Real.log (X / (n : ℝ)))]

private theorem head_diag_gaussian_term_le_tc061_aux {n : ℕ} (hn1 : 1 ≤ n) {X : ℝ}
    (hX_pos : 0 < X) (hn_le_X : (n : ℝ) ≤ X) :
    (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2 ≤
      ((27 / 4 : ℝ) * (Real.log X) ^ 2 + 32) * (1 / X) := by
  have hn_pos : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr hn1
  let u : ℝ := X / (n : ℝ)
  have hu_ge1 : 1 ≤ u := (one_le_div hn_pos).mpr hn_le_X
  have hu_pos : 0 < u := lt_of_lt_of_le zero_lt_one hu_ge1
  have h_exp_zero : 2 * u ^ 2 + (-2 * u ^ 2) = 0 := by ring
  have h_exp3 : (8 / 27 : ℝ) * u ^ 6 ≤ Real.exp (2 * u ^ 2) := by
    have h_lin : 2 * u ^ 2 / 3 ≤ Real.exp (2 * u ^ 2 / 3) := by
      linarith [Real.add_one_le_exp (2 * u ^ 2 / 3)]
    have h_pow3 := pow_le_pow_left (by positivity) h_lin 3
    rw [← Real.exp_nat_mul] at h_pow3
    have h_arg3 : ((3 : ℕ) : ℝ) * (2 * u ^ 2 / 3) = 2 * u ^ 2 := by push_cast; ring
    rw [h_arg3] at h_pow3
    linarith
  have h_u5_bd : u ^ 5 * Real.exp (-2 * u ^ 2) ≤ (27 / 8 : ℝ) / u := by
    have hm := mul_le_mul_of_nonneg_right h_exp3 (le_of_lt (Real.exp_pos (-2 * u ^ 2)))
    rw [← Real.exp_add, h_exp_zero, Real.exp_zero] at hm
    rw [le_div_iff hu_pos]
    have h_u6 : u ^ 5 * Real.exp (-2 * u ^ 2) * u = u ^ 6 * Real.exp (-2 * u ^ 2) := by ring
    rw [h_u6]
    linarith
  have h_exp4 : (1 / 16 : ℝ) * u ^ 8 ≤ Real.exp (2 * u ^ 2) := by
    have h_lin : 2 * u ^ 2 / 4 ≤ Real.exp (2 * u ^ 2 / 4) := by
      linarith [Real.add_one_le_exp (2 * u ^ 2 / 4)]
    have h_pow4 := pow_le_pow_left (by positivity) h_lin 4
    rw [← Real.exp_nat_mul] at h_pow4
    have h_arg4 : ((4 : ℕ) : ℝ) * (2 * u ^ 2 / 4) = 2 * u ^ 2 := by push_cast; ring
    rw [h_arg4] at h_pow4
    linarith
  have h_u7_bd : u ^ 7 * Real.exp (-2 * u ^ 2) ≤ (16 : ℝ) / u := by
    have hm := mul_le_mul_of_nonneg_right h_exp4 (le_of_lt (Real.exp_pos (-2 * u ^ 2)))
    rw [← Real.exp_add, h_exp_zero, Real.exp_zero] at hm
    rw [le_div_iff hu_pos]
    have h_u8 : u ^ 7 * Real.exp (-2 * u ^ 2) * u = u ^ 8 * Real.exp (-2 * u ^ 2) := by ring
    rw [h_u8]
    linarith
  have h_logu_sq : (Real.log u) ^ 2 ≤ u ^ 2 := by
    have h := Real.add_one_le_exp (Real.log u)
    rw [Real.exp_log hu_pos] at h
    exact pow_le_pow_left (Real.log_nonneg hu_ge1) (by linarith) 2
  have h_inv_nu : (1 / (n : ℝ)) * (1 / u) = 1 / X := by
    dsimp [u]
    field_simp [ne_of_gt hn_pos, ne_of_gt hX_pos]
  have h_p1 :
      (1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2) ≤ (27 / 8 : ℝ) * (1 / X) := by
    have hm := mul_le_mul_of_nonneg_left h_u5_bd (by positivity : 0 ≤ 1 / (n : ℝ))
    calc
      (1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2)
        = (1 / (n : ℝ)) * (u ^ 5 * Real.exp (-2 * u ^ 2)) := by ring
      _ ≤ (1 / (n : ℝ)) * ((27 / 8 : ℝ) / u) := hm
      _ = (27 / 8 : ℝ) * ((1 / (n : ℝ)) * (1 / u)) := by ring
      _ = (27 / 8 : ℝ) * (1 / X) := by rw [h_inv_nu]
  have h_p2 :
      (1 / (n : ℝ)) * (Real.log u) ^ 2 * u ^ 5 * Real.exp (-2 * u ^ 2) ≤
        (16 : ℝ) * (1 / X) := by
    have hm1 :
        (1 / (n : ℝ)) * (Real.log u) ^ 2 * u ^ 5 * Real.exp (-2 * u ^ 2) ≤
          (1 / (n : ℝ)) * (u ^ 7 * Real.exp (-2 * u ^ 2)) := by
      have hm :=
        mul_le_mul_of_nonneg_right h_logu_sq
          (by positivity : 0 ≤ (1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2))
      linarith
    have hm2 := mul_le_mul_of_nonneg_left h_u7_bd (by positivity : 0 ≤ 1 / (n : ℝ))
    calc
      (1 / (n : ℝ)) * (Real.log u) ^ 2 * u ^ 5 * Real.exp (-2 * u ^ 2)
        ≤ (1 / (n : ℝ)) * (u ^ 7 * Real.exp (-2 * u ^ 2)) := hm1
      _ ≤ (1 / (n : ℝ)) * ((16 : ℝ) / u) := hm2
      _ = (16 : ℝ) * ((1 / (n : ℝ)) * (1 / u)) := by ring
      _ = (16 : ℝ) * (1 / X) := by rw [h_inv_nu]
  rw [gaussianTermPhi_sq_formula_tc061_aux hn1 hX_pos]
  have hm_top :=
    mul_le_mul_of_nonneg_right (log_nat_sq_split_tc061_aux hn1 hX_pos)
      (by positivity : 0 ≤ (1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2))
  have h_expand_top :
      (2 * (Real.log X) ^ 2 + 2 * (Real.log u) ^ 2) *
          ((1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2)) =
        2 * (Real.log X) ^ 2 * ((1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2)) +
          2 * ((1 / (n : ℝ)) * (Real.log u) ^ 2 * u ^ 5 * Real.exp (-2 * u ^ 2)) := by ring
  change (Real.log (n : ℝ)) ^ 2 * ((1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2)) ≤ _
  rw [h_expand_top] at hm_top
  have hm_p1 := mul_le_mul_of_nonneg_left h_p1 (by positivity : 0 ≤ 2 * (Real.log X) ^ 2)
  linarith

private theorem tail_diag_gaussian_term_le_tc061_aux {n : ℕ} (hn1 : 1 ≤ n) {X : ℝ}
    (hX_pos : 0 < X) (hX_lt_n : X < (n : ℝ)) :
    (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2 ≤
      (2 * (Real.log X) ^ 2 + 8) * X * (1 / (n : ℝ) ^ 2) := by
  have hn_pos : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr hn1
  let u : ℝ := X / (n : ℝ)
  have hu_pos : 0 < u := div_pos hX_pos hn_pos
  have hu_le1 : u ≤ 1 := le_of_lt ((div_lt_one hn_pos).mpr hX_lt_n)
  have hexp_le1 : Real.exp (-2 * u ^ 2) ≤ 1 := by
    rw [← Real.exp_zero]
    exact Real.exp_le_exp.mpr (by nlinarith)
  have hu2_le1 : u ^ 2 ≤ 1 := by nlinarith
  have hu3_le1 : u ^ 3 ≤ 1 := by nlinarith [hu2_le1]
  have hu4_le1 : u ^ 4 ≤ 1 := by nlinarith [hu2_le1]
  have hu5_le_u : u ^ 5 ≤ u := by nlinarith [hu4_le1]
  have h_nX_ge1 : 1 ≤ (n : ℝ) / X := (one_le_div hX_pos).mpr (le_of_lt hX_lt_n)
  let s : ℝ := Real.sqrt ((n : ℝ) / X)
  have hs_ge1 : 1 ≤ s := Real.one_le_sqrt.mpr h_nX_ge1
  have hs_pos : 0 < s := lt_of_lt_of_le zero_lt_one hs_ge1
  have hs_sq : s ^ 2 = (n : ℝ) / X := Real.sq_sqrt (by positivity)
  have h_logu_eq : Real.log u = -(2 * Real.log s) := by
    have h1 : Real.log (X / (n : ℝ)) = -Real.log ((n : ℝ) / X) := by
      rw [Real.log_div (ne_of_gt hX_pos) (ne_of_gt hn_pos),
        Real.log_div (ne_of_gt hn_pos) (ne_of_gt hX_pos)]
      ring
    have h2 : Real.log ((n : ℝ) / X) = 2 * Real.log s := by
      rw [← hs_sq, Real.log_pow]
      push_cast; rfl
    dsimp [u]
    rw [h1, h2]
  have h_logu_sq : (Real.log u) ^ 2 ≤ 4 / u := by
    have h_logs_le_s : Real.log s ≤ s := by
      have h := Real.add_one_le_exp (Real.log s)
      rw [Real.exp_log hs_pos] at h
      linarith
    have h_sq_s : (Real.log s) ^ 2 ≤ s ^ 2 :=
      pow_le_pow_left (Real.log_nonneg hs_ge1) h_logs_le_s 2
    have h_4u : 4 * ((n : ℝ) / X) = 4 / u := by
      dsimp [u]
      rw [div_div_eq_mul_div]
      ring
    calc
      (Real.log u) ^ 2 = 4 * (Real.log s) ^ 2 := by rw [h_logu_eq]; ring
      _ ≤ 4 * s ^ 2 := by linarith
      _ = 4 * ((n : ℝ) / X) := by rw [hs_sq]
      _ = 4 / u := h_4u
  have h_inv_nu : (1 / (n : ℝ)) * u = X * (1 / (n : ℝ) ^ 2) := by
    dsimp [u]
    rw [one_div, one_div, div_eq_mul_inv, ← inv_pow]
    ring
  have h_t1 :
      (1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2) ≤ X * (1 / (n : ℝ) ^ 2) := by
    have hm1 : u ^ 5 * Real.exp (-2 * u ^ 2) ≤ u := by
      calc
        u ^ 5 * Real.exp (-2 * u ^ 2) ≤ u ^ 5 * 1 :=
          mul_le_mul_of_nonneg_left hexp_le1 (by positivity)
        _ = u ^ 5 := mul_one _
        _ ≤ u := hu5_le_u
    have hm2 := mul_le_mul_of_nonneg_left hm1 (by positivity : 0 ≤ 1 / (n : ℝ))
    calc
      (1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2)
        = (1 / (n : ℝ)) * (u ^ 5 * Real.exp (-2 * u ^ 2)) := by ring
      _ ≤ (1 / (n : ℝ)) * u := hm2
      _ = X * (1 / (n : ℝ) ^ 2) := h_inv_nu
  have h_t2 :
      (1 / (n : ℝ)) * (Real.log u) ^ 2 * u ^ 5 * Real.exp (-2 * u ^ 2) ≤
        4 * X * (1 / (n : ℝ) ^ 2) := by
    have hm_log : (Real.log u) ^ 2 * u ^ 5 ≤ 4 * u := by
      have hm := mul_le_mul_of_nonneg_right h_logu_sq (by positivity : 0 ≤ u ^ 5)
      have h_cancel : (4 / u) * u ^ 5 = 4 * u ^ 4 := by
        calc
          (4 / u) * u ^ 5 = (4 * u ^ 4 * u) / u := by ring
          _ = 4 * u ^ 4 := mul_div_cancel_right₀ (4 * u ^ 4) (ne_of_gt hu_pos)
      rw [h_cancel] at hm
      have hu4_u : 4 * u ^ 4 ≤ 4 * u := by
        calc
          4 * u ^ 4 = (4 * u) * u ^ 3 := by ring
          _ ≤ (4 * u) * 1 := mul_le_mul_of_nonneg_left hu3_le1 (by positivity)
          _ = 4 * u := mul_one _
      exact le_trans hm hu4_u
    have hm_exp : (Real.log u) ^ 2 * u ^ 5 * Real.exp (-2 * u ^ 2) ≤ 4 * u := by
      calc
        (Real.log u) ^ 2 * u ^ 5 * Real.exp (-2 * u ^ 2)
          ≤ ((Real.log u) ^ 2 * u ^ 5) * 1 :=
            mul_le_mul_of_nonneg_left hexp_le1 (by positivity)
        _ = (Real.log u) ^ 2 * u ^ 5 := mul_one _
        _ ≤ 4 * u := hm_log
    have hm2 := mul_le_mul_of_nonneg_left hm_exp (by positivity : 0 ≤ 1 / (n : ℝ))
    calc
      (1 / (n : ℝ)) * (Real.log u) ^ 2 * u ^ 5 * Real.exp (-2 * u ^ 2)
        = (1 / (n : ℝ)) * ((Real.log u) ^ 2 * u ^ 5 * Real.exp (-2 * u ^ 2)) := by ring
      _ ≤ (1 / (n : ℝ)) * (4 * u) := hm2
      _ = 4 * ((1 / (n : ℝ)) * u) := by ring
      _ = 4 * X * (1 / (n : ℝ) ^ 2) := by rw [h_inv_nu]; ring
  rw [gaussianTermPhi_sq_formula_tc061_aux hn1 hX_pos]
  have hm_top :=
    mul_le_mul_of_nonneg_right (log_nat_sq_split_tc061_aux hn1 hX_pos)
      (by positivity : 0 ≤ (1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2))
  have h_expand_top :
      (2 * (Real.log X) ^ 2 + 2 * (Real.log u) ^ 2) *
          ((1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2)) =
        2 * (Real.log X) ^ 2 * ((1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2)) +
          2 * ((1 / (n : ℝ)) * (Real.log u) ^ 2 * u ^ 5 * Real.exp (-2 * u ^ 2)) := by ring
  change (Real.log (n : ℝ)) ^ 2 * ((1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2)) ≤ _
  rw [h_expand_top] at hm_top
  have hm_t1 := mul_le_mul_of_nonneg_left h_t1 (by positivity : 0 ≤ 2 * (Real.log X) ^ 2)
  calc
    (Real.log (n : ℝ)) ^ 2 * ((1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2))
      ≤ 2 * (Real.log X) ^ 2 * ((1 / (n : ℝ)) * u ^ 5 * Real.exp (-2 * u ^ 2)) +
          2 * ((1 / (n : ℝ)) * (Real.log u) ^ 2 * u ^ 5 * Real.exp (-2 * u ^ 2)) := hm_top
    _ ≤ 2 * (Real.log X) ^ 2 * (X * (1 / (n : ℝ) ^ 2)) +
          2 * (4 * X * (1 / (n : ℝ) ^ 2)) :=
        add_le_add hm_t1 (mul_le_mul_of_nonneg_left h_t2 (by norm_num))
    _ = (2 * (Real.log X) ^ 2 + 8) * X * (1 / (n : ℝ) ^ 2) := by ring

private theorem pointwise_diag_gaussian_log_sq_bound_tc061_aux (T : ℕ) {X : ℝ} (hX2 : 2 ≤ X) :
    ((∑ n ∈ Finset.Icc 1 T, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2) /
        (Real.log X) ^ 2) ≤
      (186 : ℝ) := by
  have hX_pos : 0 < X := by linarith
  have hlogX_ge_half : (1 / 2 : ℝ) ≤ Real.log X :=
    le_trans half_le_log_two_tc061_aux (Real.log_le_log (by norm_num) hX2)
  have hlogX_pos : 0 < Real.log X := by linarith
  have hlogX_sq_ge : (1 / 4 : ℝ) ≤ (Real.log X) ^ 2 := by
    have h := pow_le_pow_left (by norm_num : (0 : ℝ) ≤ 1 / 2) hlogX_ge_half 2
    norm_num at h
    exact h
  let M : ℕ := Nat.floor X
  have hM_ge2 : 2 ≤ M := Nat.le_floor (by exact_mod_cast hX2)
  have hM_pos : 1 ≤ M := by omega
  have hM_real_pos : (0 : ℝ) < (M : ℝ) := Nat.cast_pos.mpr hM_pos
  have hM_le_X : (M : ℝ) ≤ X := Nat.floor_le (le_of_lt hX_pos)
  have hX_lt_M1 : X < (M : ℝ) + 1 := Nat.lt_floor_add_one X
  have hXM_le_32 : X / (M : ℝ) ≤ 3 / 2 := by
    rw [div_le_iff hM_real_pos]
    have h2r : (2 : ℝ) ≤ (M : ℝ) := by exact_mod_cast hM_ge2
    linarith
  have h_sub_union : Finset.Icc 1 T ⊆ Finset.Icc 1 M ∪ Finset.Icc (M + 1) T := by
    intro n hn
    rw [Finset.mem_Icc] at hn
    simp only [Finset.mem_union, Finset.mem_Icc]
    omega
  have h_disj : Disjoint (Finset.Icc 1 M) (Finset.Icc (M + 1) T) := by
    rw [Finset.disjoint_left]; intro n h1 h2; simp only [Finset.mem_Icc] at h1 h2; omega
  have h_split_sum :
      (∑ n ∈ Finset.Icc 1 T, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2) ≤
        (∑ n ∈ Finset.Icc 1 M, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2) +
          (∑ n ∈ Finset.Icc (M + 1) T, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2) := by
    rw [← Finset.sum_union h_disj]
    exact Finset.sum_le_sum_of_subset_of_nonneg h_sub_union
      (fun _ _ _ => mul_nonneg (sq_nonneg _) (sq_nonneg _))
  have h_head_sum :
      (∑ n ∈ Finset.Icc 1 M, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2) ≤
        (27 / 4 : ℝ) * (Real.log X) ^ 2 + 32 := by
    have hs :
        (∑ n ∈ Finset.Icc 1 M, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2) ≤
          ∑ _n ∈ Finset.Icc 1 M, ((27 / 4 : ℝ) * (Real.log X) ^ 2 + 32) * (1 / X) := by
      apply Finset.sum_le_sum
      intro n hn
      rw [Finset.mem_Icc] at hn
      exact head_diag_gaussian_term_le_tc061_aux hn.1 hX_pos
        (le_trans (by exact_mod_cast hn.2) hM_le_X)
    rw [Finset.sum_const, Nat.card_Icc, show M + 1 - 1 = M by omega, nsmul_eq_mul] at hs
    have hMX_le1 : (M : ℝ) / X ≤ 1 := (div_le_one hX_pos).mpr hM_le_X
    calc
      (∑ n ∈ Finset.Icc 1 M, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2)
        ≤ (M : ℝ) * (((27 / 4 : ℝ) * (Real.log X) ^ 2 + 32) * (1 / X)) := hs
      _ = ((27 / 4 : ℝ) * (Real.log X) ^ 2 + 32) * ((M : ℝ) / X) := by ring
      _ ≤ ((27 / 4 : ℝ) * (Real.log X) ^ 2 + 32) * 1 :=
          mul_le_mul_of_nonneg_left hMX_le1 (by positivity)
      _ = (27 / 4 : ℝ) * (Real.log X) ^ 2 + 32 := mul_one _
  have h_tail_sum :
      (∑ n ∈ Finset.Icc (M + 1) T, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2) ≤
        3 * (Real.log X) ^ 2 + 12 := by
    have hs :
        (∑ n ∈ Finset.Icc (M + 1) T, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2) ≤
          ∑ n ∈ Finset.Icc (M + 1) T,
            ((2 * (Real.log X) ^ 2 + 8) * X) * (1 / (n : ℝ) ^ 2) := by
      apply Finset.sum_le_sum
      intro n hn
      rw [Finset.mem_Icc] at hn
      exact tail_diag_gaussian_term_le_tc061_aux (by omega) hX_pos
        (lt_of_lt_of_le hX_lt_M1 (by exact_mod_cast hn.1))
    rw [← Finset.mul_sum] at hs
    calc
      (∑ n ∈ Finset.Icc (M + 1) T, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2)
        ≤ ((2 * (Real.log X) ^ 2 + 8) * X) *
            (∑ n ∈ Finset.Icc (M + 1) T, (1 / (n : ℝ) ^ 2)) := hs
      _ ≤ ((2 * (Real.log X) ^ 2 + 8) * X) * (1 / (M : ℝ)) :=
          mul_le_mul_of_nonneg_left (sum_inv_sq_Icc_succ_le_inv_tc061_aux hM_pos T)
            (by positivity)
      _ = (2 * (Real.log X) ^ 2 + 8) * (X / (M : ℝ)) := by ring
      _ ≤ (2 * (Real.log X) ^ 2 + 8) * (3 / 2 : ℝ) :=
          mul_le_mul_of_nonneg_left hXM_le_32 (by positivity)
      _ = 3 * (Real.log X) ^ 2 + 12 := by ring
  have h_num_tot :
      (∑ n ∈ Finset.Icc 1 T, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2) ≤
        (39 / 4 : ℝ) * (Real.log X) ^ 2 + 44 := by
    linarith [h_split_sum, h_head_sum, h_tail_sum]
  rw [div_le_iff (sq_pos_of_pos hlogX_pos)]
  nlinarith [h_num_tot, hlogX_sq_ge]

/-- **Theorem 3 (`TASK-TC-061`, Finite-Window Off-Diagonal Kernel Expansion, Self-Collision Weight Characterization, and Unconditional `O(1)` Composite Self-Collision Bound)**:
    1. Exact finite-window kernel expansions (`2 ≤ Y`, `T : ℕ`):
       - `inheritedPrimePowerDiagDtilde T Y = ∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T, (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n * logWeightedWindowKernel 2 Y m n`;
       - `inheritedPrimePowerOffDiagXtilde T Y = ∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T, (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * offDiagPrimePowerWeight m n * logWeightedWindowKernel 2 Y m n`;
    2. Exact properties of `offDiagPrimePowerWeight n n`:
       - `offDiagPrimePowerWeight 1 1 = 0`;
       - `∀ {p : ℕ}, p.Prime → offDiagPrimePowerWeight p p = 0`;
       - `∀ {p q : ℕ}, p.Prime → q.Prime → p ≠ q → offDiagPrimePowerWeight (p * q) (p * q) = 2 * Real.log (p : ℝ) * Real.log (q : ℝ)`;
       - `∀ n : ℕ, 1 ≤ n → 0 ≤ offDiagPrimePowerWeight n n ∧ offDiagPrimePowerWeight n n ≤ (Real.log (n : ℝ)) ^ 2`;
    3. Unconditional uniform `O(1)` bound on the `m = n` composite self-collision sum (`C_self = 186 * (RiemannScope.tau - 1)`):
       `0 < C_self`, `C_self < 1302`, and for ALL `Y ≥ 2` and ALL `T : ℕ`:
       `0 ≤ ∑ n ∈ Finset.Icc 1 T, offDiagPrimePowerWeight n n * logWeightedWindowKernel 2 Y n n ≤ ∑ n ∈ Finset.Icc 1 T, (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n ≤ C_self`. -/
theorem finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061 :
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ (T : ℕ),
      inheritedPrimePowerDiagDtilde T Y =
          (∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T,
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
              logWeightedWindowKernel 2 Y m n) ∧
        inheritedPrimePowerOffDiagXtilde T Y =
          (∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T,
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * offDiagPrimePowerWeight m n *
              logWeightedWindowKernel 2 Y m n)) ∧
    (offDiagPrimePowerWeight 1 1 = 0 ∧
      (∀ {p : ℕ}, p.Prime → offDiagPrimePowerWeight p p = 0) ∧
      (∀ {p q : ℕ}, p.Prime → q.Prime → p ≠ q →
        offDiagPrimePowerWeight (p * q) (p * q) = 2 * Real.log (p : ℝ) * Real.log (q : ℝ)) ∧
      (∀ n : ℕ, 1 ≤ n →
        0 ≤ offDiagPrimePowerWeight n n ∧ offDiagPrimePowerWeight n n ≤ (Real.log (n : ℝ)) ^ 2)) ∧
    (let C_self : ℝ := 186 * (RiemannScope.tau - 1);
      0 < C_self ∧
        C_self < 1302 ∧
        ∀ {Y : ℝ}, 2 ≤ Y → ∀ (T : ℕ),
          0 ≤ ∑ n ∈ Finset.Icc 1 T,
              offDiagPrimePowerWeight n n * logWeightedWindowKernel 2 Y n n ∧
            (∑ n ∈ Finset.Icc 1 T,
                offDiagPrimePowerWeight n n * logWeightedWindowKernel 2 Y n n) ≤
              (∑ n ∈ Finset.Icc 1 T,
                (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n) ∧
            (∑ n ∈ Finset.Icc 1 T,
                (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n) ≤
              C_self) := by
  have h_ker_cont :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ m n : ℕ,
        ContinuousOn
          (fun X => (gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ 2) / X)
          (Set.uIcc Y (RiemannScope.tau * Y)) := by
    intro Y hY2 m n
    obtain ⟨_, hprops⟩ := uIcc_tau_props_tc061_aux hY2
    have hlog_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
      ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1)
    exact (((continuousOn_gaussianTermPhi_uIcc_tc061_aux hY2 m).mul
      (continuousOn_gaussianTermPhi_uIcc_tc061_aux hY2 n)).div
      (hlog_cont.pow 2) (fun X hX => (hprops X hX).2.2.2.2)).div
      continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1)
  have h_ker_int :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ m n : ℕ,
        IntervalIntegrable
          (fun X => (gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ 2) / X)
          volume Y (RiemannScope.tau * Y) :=
    fun hY2 m n => (h_ker_cont hY2 m n).intervalIntegrable
  have h_part1 :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ (T : ℕ),
        inheritedPrimePowerDiagDtilde T Y =
            (∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T,
              (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
                logWeightedWindowKernel 2 Y m n) ∧
          inheritedPrimePowerOffDiagXtilde T Y =
            (∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T,
              (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * offDiagPrimePowerWeight m n *
                logWeightedWindowKernel 2 Y m n) := by
    intro Y hY2 T
    obtain ⟨_, hprops⟩ := uIcc_tau_props_tc061_aux hY2
    have h_diag_eq :
        inheritedPrimePowerDiagDtilde T Y =
          ∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T,
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
              logWeightedWindowKernel 2 Y m n := by
      unfold inheritedPrimePowerDiagDtilde
      have h_congr :
          ∫ X in Y..(RiemannScope.tau * Y), pointwisePrimePowerDiagNorm T X / X =
            ∫ X in Y..(RiemannScope.tau * Y),
              ∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T,
                (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
                  ((gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ 2) / X) := by
        apply intervalIntegral.integral_congr
        intro X hX
        exact pointwisePrimePowerDiagNorm_kernel_expand_tc061_aux T (hprops X hX).2.1
      rw [h_congr, intervalIntegral.integral_finset_sum]
      · apply Finset.sum_congr rfl
        intro m _
        rw [intervalIntegral.integral_finset_sum]
        · apply Finset.sum_congr rfl
          intro n _
          rw [intervalIntegral.integral_const_mul]
          rfl
        · intro n _
          exact (h_ker_int hY2 m n).const_mul _
      · intro m _
        exact (continuousOn_finset_sum _ (fun n _ =>
          continuousOn_const.mul (h_ker_cont hY2 m n))).intervalIntegrable
    have h_P_norm :
        windowEnergyNormSq Y (normalizedPrimePowerTermP T) =
          ∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T,
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
              (Real.log (m : ℝ) * Real.log (n : ℝ)) *
              logWeightedWindowKernel 2 Y m n := by
      have hlam1 : (liouvilleLambda 1 : ℝ) = 1 := by
        simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
      have hlam_mult :
          ∀ d q : ℕ, 0 < d → 0 < q →
            (liouvilleLambda (d * q) : ℝ) = (liouvilleLambda d : ℝ) * (liouvilleLambda q : ℝ) :=
        fun _ _ hd hq => liouvilleLambda_mul_pos_tc061_aux hd hq
      unfold windowEnergyNormSq windowPairing
      have h_congr_P :
          ∫ X in Y..(RiemannScope.tau * Y),
              normalizedPrimePowerTermP T X * normalizedPrimePowerTermP T X / X =
            ∫ X in Y..(RiemannScope.tau * Y),
              ∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T,
                (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                  (Real.log (m : ℝ) * Real.log (n : ℝ)) *
                  ((gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ 2) / X) := by
        apply intervalIntegral.integral_congr
        intro X hX
        dsimp only
        have h_desc :=
          (logarithmic_prime_power_descent_and_kernel_shift_tc057
            (a := fun n => (liouvilleLambda n : ℝ)) hlam1 hlam_mult 0 0 T
            (hprops X hX).2.1).2.1.1
        unfold normalizedPrimePowerTermP
        rw [← h_desc]
        have h_sq :
            ((∑ n ∈ Finset.Icc 1 T,
                (liouvilleLambda n : ℝ) * Real.log (n : ℝ) * gaussianTermPhi n X) /
              Real.log X) *
            ((∑ n ∈ Finset.Icc 1 T,
                (liouvilleLambda n : ℝ) * Real.log (n : ℝ) * gaussianTermPhi n X) /
              Real.log X) / X =
              ((∑ m ∈ Finset.Icc 1 T,
                  (liouvilleLambda m : ℝ) * Real.log (m : ℝ) * gaussianTermPhi m X) *
                (∑ n ∈ Finset.Icc 1 T,
                  (liouvilleLambda n : ℝ) * Real.log (n : ℝ) * gaussianTermPhi n X) /
                (Real.log X) ^ 2) / X := by ring
        rw [h_sq, Finset.sum_mul_sum, Finset.sum_div, Finset.sum_div]
        apply Finset.sum_congr rfl
        intro m _
        rw [Finset.sum_div, Finset.sum_div]
        apply Finset.sum_congr rfl
        intro n _
        ring
      rw [h_congr_P, intervalIntegral.integral_finset_sum]
      · apply Finset.sum_congr rfl
        intro m _
        rw [intervalIntegral.integral_finset_sum]
        · apply Finset.sum_congr rfl
          intro n _
          rw [intervalIntegral.integral_const_mul]
          rfl
        · intro n _
          exact (h_ker_int hY2 m n).const_mul _
      · intro m _
        exact (continuousOn_finset_sum _ (fun n _ =>
          continuousOn_const.mul (h_ker_cont hY2 m n))).intervalIntegrable
    have h_split_P :=
      (full_core_quantified_obstructions_and_w2_support_tc060r).1.2.2.1 hY2 T
    have h_off_eq :
        inheritedPrimePowerOffDiagXtilde T Y =
          windowEnergyNormSq Y (normalizedPrimePowerTermP T) -
            inheritedPrimePowerDiagDtilde T Y := by
      unfold inheritedPrimePowerDiagDtilde inheritedPrimePowerOffDiagXtilde
      linarith [h_split_P]
    refine ⟨h_diag_eq, ?_⟩
    rw [h_off_eq, h_P_norm, h_diag_eq, ← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro m _
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro n _
    unfold offDiagPrimePowerWeight
    ring
  have h_common_self :
      ∀ n : ℕ,
        commonPrimePowerLogSq n n =
          ∑ pk ∈ (primePowerPairsUpTo n).filter (fun pk => pk.1 ^ pk.2 ∣ n),
            (Real.log (pk.1 : ℝ)) ^ 2 := by
    intro n
    unfold commonPrimePowerLogSq
    simp [Nat.gcd_self]
  have h_w11 : offDiagPrimePowerWeight 1 1 = 0 := by
    unfold offDiagPrimePowerWeight
    rw [h_common_self 1]
    have h_emp : (primePowerPairsUpTo 1).filter (fun pk => pk.1 ^ pk.2 ∣ 1) = ∅ := by decide
    rw [h_emp, Finset.sum_empty]
    simp
  have h_wpp : ∀ {p : ℕ}, p.Prime → offDiagPrimePowerWeight p p = 0 := by
    intro p hp
    unfold offDiagPrimePowerWeight
    rw [h_common_self p]
    have h_sing : (primePowerPairsUpTo p).filter (fun pk => pk.1 ^ pk.2 ∣ p) = {(p, 1)} := by
      ext ⟨r, k⟩
      simp only [Finset.mem_filter, mem_primePowerPairsUpTo_iff_tc061_aux, Finset.mem_singleton,
        Prod.mk.injEq]
      constructor
      · rintro ⟨⟨hr, hk1, _⟩, hdvd⟩
        have hr_dvd_p : r ∣ p := dvd_trans (dvd_pow_self r (by omega)) hdvd
        have hr_eq : r = p := (Nat.dvd_prime hp).mp hr_dvd_p |>.resolve_left hr.ne_one
        subst hr_eq
        have hk_eq1 : k = 1 := by
          by_contra hne1
          have h_gt : r < r ^ k := by
            calc
              r = r ^ 1 := (pow_one r).symm
              _ < r ^ k := Nat.pow_lt_pow_right hr.one_lt (by omega)
          omega
        exact ⟨rfl, hk_eq1⟩
      · rintro ⟨rfl, rfl⟩
        exact ⟨⟨hp, le_refl 1, by simp⟩, by simp⟩
    rw [h_sing, Finset.sum_singleton]
    ring
  have h_wpq :
      ∀ {p q : ℕ}, p.Prime → q.Prime → p ≠ q →
        offDiagPrimePowerWeight (p * q) (p * q) = 2 * Real.log (p : ℝ) * Real.log (q : ℝ) := by
    intro p q hp hq hne
    unfold offDiagPrimePowerWeight
    rw [h_common_self (p * q)]
    have hcop_pq : Nat.Coprime p q :=
      (hp.coprime_iff_not_dvd).mpr (fun hdvd =>
        hne ((Nat.dvd_prime hq).mp hdvd |>.resolve_left hp.ne_one))
    have h_pair :
        (primePowerPairsUpTo (p * q)).filter (fun pk => pk.1 ^ pk.2 ∣ p * q) =
          {(p, 1), (q, 1)} := by
      ext ⟨r, k⟩
      simp only [Finset.mem_filter, mem_primePowerPairsUpTo_iff_tc061_aux, Finset.mem_insert,
        Finset.mem_singleton, Prod.mk.injEq]
      constructor
      · rintro ⟨⟨hr, hk1, _⟩, hdvd⟩
        have hr_dvd_pq : r ∣ p * q := dvd_trans (dvd_pow_self r (by omega)) hdvd
        rcases hr.dvd_mul.mp hr_dvd_pq with hr_p | hr_q
        · left
          have hr_eq : r = p := (Nat.dvd_prime hp).mp hr_p |>.resolve_left hr.ne_one
          subst hr_eq
          have h_dvd_p : r ^ k ∣ r := (hcop_pq.pow_left k).dvd_of_dvd_mul_right hdvd
          have h_le : r ^ k ≤ r := Nat.le_of_dvd hr.pos h_dvd_p
          have hk_eq1 : k = 1 := by
            by_contra hne1
            have h_gt : r < r ^ k := by
              calc
                r = r ^ 1 := (pow_one r).symm
                _ < r ^ k := Nat.pow_lt_pow_right hr.one_lt (by omega)
            omega
          exact ⟨rfl, hk_eq1⟩
        · right
          have hr_eq : r = q := (Nat.dvd_prime hq).mp hr_q |>.resolve_left hr.ne_one
          subst hr_eq
          have h_dvd_q : r ^ k ∣ r :=
            (hcop_pq.symm.pow_left k).dvd_of_dvd_mul_left hdvd
          have h_le : r ^ k ≤ r := Nat.le_of_dvd hr.pos h_dvd_q
          have hk_eq1 : k = 1 := by
            by_contra hne1
            have h_gt : r < r ^ k := by
              calc
                r = r ^ 1 := (pow_one r).symm
                _ < r ^ k := Nat.pow_lt_pow_right hr.one_lt (by omega)
            omega
          exact ⟨rfl, hk_eq1⟩
      · rintro (⟨hrp, hk1⟩ | ⟨hrq, hk1⟩)
        · rw [hrp, hk1]
          exact ⟨⟨hp, le_refl 1, by rw [pow_one]; exact Nat.le_mul_of_pos_right p hq.pos⟩,
            by rw [pow_one]; exact dvd_mul_right p q⟩
        · rw [hrq, hk1]
          exact ⟨⟨hq, le_refl 1, by rw [pow_one]; exact Nat.le_mul_of_pos_left q hp.pos⟩,
            by rw [pow_one]; exact dvd_mul_left q p⟩
    have h_ne_pair : (p, 1) ≠ (q, 1) := fun h => hne (Prod.mk.inj h).1
    rw [h_pair, Finset.sum_pair h_ne_pair]
    have h_log_pq : Real.log ((p * q : ℕ) : ℝ) = Real.log (p : ℝ) + Real.log (q : ℝ) := by
      push_cast
      exact Real.log_mul (Nat.cast_ne_zero.mpr hp.ne_zero) (Nat.cast_ne_zero.mpr hq.ne_zero)
    rw [h_log_pq]
    ring
  have h_wnn_bds :
      ∀ n : ℕ, 1 ≤ n →
        0 ≤ offDiagPrimePowerWeight n n ∧ offDiagPrimePowerWeight n n ≤ (Real.log (n : ℝ)) ^ 2 := by
    intro n hn
    unfold offDiagPrimePowerWeight
    rw [h_common_self n]
    let S := (primePowerPairsUpTo n).filter (fun pk => pk.1 ^ pk.2 ∣ n)
    have h_comm_nn : 0 ≤ ∑ pk ∈ S, (Real.log (pk.1 : ℝ)) ^ 2 :=
      Finset.sum_nonneg (fun _ _ => sq_nonneg _)
    have h_inj : Set.InjOn (fun pk : ℕ × ℕ => pk.1 ^ pk.2) (S : Set (ℕ × ℕ)) := by
      rintro ⟨p1, k1⟩ h1 ⟨p2, k2⟩ h2 heq
      simp only [Finset.mem_coe, S, Finset.mem_filter,
        mem_primePowerPairsUpTo_iff_tc061_aux] at h1 h2
      dsimp at heq
      have hp1_dvd : p1 ∣ p2 ^ k2 := heq ▸ dvd_pow_self p1 (by omega)
      have hp_eq : p1 = p2 :=
        (Nat.dvd_prime h2.1.1).mp (h1.1.1.dvd_of_dvd_pow hp1_dvd) |>.resolve_left h1.1.1.ne_one
      subst hp_eq
      have hk_eq : k1 = k2 := Nat.pow_right_injective h1.1.1.two_le heq
      exact Prod.ext rfl hk_eq
    have h_img_sub : S.image (fun pk : ℕ × ℕ => pk.1 ^ pk.2) ⊆ n.divisors := by
      intro d hd
      rcases Finset.mem_image.mp hd with ⟨pk, hpk, rfl⟩
      simp only [S, Finset.mem_filter] at hpk
      exact Nat.mem_divisors.mpr ⟨hpk.2, by omega⟩
    have h_each_le :
        ∀ pk ∈ S,
          (Real.log (pk.1 : ℝ)) ^ 2 ≤
            ArithmeticFunction.vonMangoldt (pk.1 ^ pk.2) * Real.log (n : ℝ) := by
      intro pk hpk
      simp only [S, Finset.mem_filter, mem_primePowerPairsUpTo_iff_tc061_aux] at hpk
      rcases hpk with ⟨⟨hp, hk1, hle_n⟩, _⟩
      have hp_le_n : (pk.1 : ℝ) ≤ (n : ℝ) := by
        have hp_le_pk : pk.1 ≤ pk.1 ^ pk.2 := by simpa using Nat.pow_le_pow_right hp.pos hk1
        exact_mod_cast le_trans hp_le_pk hle_n
      have hlog_le : Real.log (pk.1 : ℝ) ≤ Real.log (n : ℝ) :=
        Real.log_le_log (Nat.cast_pos.mpr hp.pos) hp_le_n
      have hlog_nn : 0 ≤ Real.log (pk.1 : ℝ) :=
        Real.log_nonneg (by exact_mod_cast hp.pos)
      rw [vonMangoldt_prime_pow_tc061_aux hp hk1, sq]
      exact mul_le_mul_of_nonneg_left hlog_le hlog_nn
    have h_comm_ub : (∑ pk ∈ S, (Real.log (pk.1 : ℝ)) ^ 2) ≤ (Real.log (n : ℝ)) ^ 2 := by
      calc
        (∑ pk ∈ S, (Real.log (pk.1 : ℝ)) ^ 2)
          ≤ ∑ pk ∈ S, ArithmeticFunction.vonMangoldt (pk.1 ^ pk.2) * Real.log (n : ℝ) :=
            Finset.sum_le_sum h_each_le
        _ = (∑ pk ∈ S, ArithmeticFunction.vonMangoldt (pk.1 ^ pk.2)) * Real.log (n : ℝ) :=
            (Finset.sum_mul _ _ _).symm
        _ = (∑ d ∈ S.image (fun pk : ℕ × ℕ => pk.1 ^ pk.2), ArithmeticFunction.vonMangoldt d) *
              Real.log (n : ℝ) := by
            rw [Finset.sum_image h_inj]
        _ ≤ (∑ d ∈ n.divisors, ArithmeticFunction.vonMangoldt d) * Real.log (n : ℝ) := by
            apply mul_le_mul_of_nonneg_right
            · exact Finset.sum_le_sum_of_subset_of_nonneg h_img_sub
                (fun d _ _ => ArithmeticFunction.vonMangoldt_nonneg)
            · exact Real.log_nonneg (by exact_mod_cast hn)
        _ = (Real.log (n : ℝ)) ^ 2 := by
            rw [ArithmeticFunction.vonMangoldt_sum, sq]
    change 0 ≤ Real.log (n : ℝ) * Real.log (n : ℝ) - ∑ pk ∈ S, (Real.log (pk.1 : ℝ)) ^ 2 ∧
      Real.log (n : ℝ) * Real.log (n : ℝ) - ∑ pk ∈ S, (Real.log (pk.1 : ℝ)) ^ 2 ≤
        (Real.log (n : ℝ)) ^ 2
    exact ⟨by nlinarith [h_comm_ub], by nlinarith [h_comm_nn]⟩
  refine ⟨h_part1, ⟨h_w11, h_wpp, h_wpq, h_wnn_bds⟩, ?_⟩
  dsimp only
  obtain ⟨htau_gt1, htau_lt8⟩ := tau_gt_one_and_lt_eight_tc061_aux
  refine ⟨by linarith, by linarith, ?_⟩
  intro Y hY2 T
  obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc061_aux hY2
  have hY_pos : 0 < Y := by linarith
  have h_ker_nn : ∀ n : ℕ, 0 ≤ logWeightedWindowKernel 2 Y n n := by
    intro n
    unfold logWeightedWindowKernel
    apply intervalIntegral.integral_nonneg hle
    intro X hX
    have hX_uIcc : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
    have hX_pos : 0 < X := (hprops X hX_uIcc).2.1
    exact div_nonneg (div_nonneg (mul_self_nonneg _) (sq_nonneg _)) (le_of_lt hX_pos)
  have h_sum_nn :
      0 ≤ ∑ n ∈ Finset.Icc 1 T, offDiagPrimePowerWeight n n * logWeightedWindowKernel 2 Y n n := by
    apply Finset.sum_nonneg
    intro n hn
    rw [Finset.mem_Icc] at hn
    exact mul_nonneg (h_wnn_bds n hn.1).1 (h_ker_nn n)
  have h_sum_mono :
      (∑ n ∈ Finset.Icc 1 T, offDiagPrimePowerWeight n n * logWeightedWindowKernel 2 Y n n) ≤
        ∑ n ∈ Finset.Icc 1 T, (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n := by
    apply Finset.sum_le_sum
    intro n hn
    rw [Finset.mem_Icc] at hn
    exact mul_le_mul_of_nonneg_right (h_wnn_bds n hn.1).2 (h_ker_nn n)
  refine ⟨h_sum_nn, h_sum_mono, ?_⟩
  have h_swap_int :
      (∑ n ∈ Finset.Icc 1 T, (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n) =
        ∫ X in Y..(RiemannScope.tau * Y),
          ((∑ n ∈ Finset.Icc 1 T, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2) /
            (Real.log X) ^ 2) / X := by
    unfold logWeightedWindowKernel
    have h_each_int :
        ∀ n ∈ Finset.Icc 1 T,
          (Real.log (n : ℝ)) ^ 2 *
              (∫ X in Y..(RiemannScope.tau * Y),
                (gaussianTermPhi n X * gaussianTermPhi n X / (Real.log X) ^ 2) / X) =
            ∫ X in Y..(RiemannScope.tau * Y),
              (Real.log (n : ℝ)) ^ 2 *
                ((gaussianTermPhi n X * gaussianTermPhi n X / (Real.log X) ^ 2) / X) :=
      fun n _ => (intervalIntegral.integral_const_mul _ _).symm
    rw [Finset.sum_congr rfl h_each_int,
      ← intervalIntegral.integral_finset_sum
        (fun n _ => (h_ker_int hY2 n n).const_mul ((Real.log (n : ℝ)) ^ 2))]
    apply intervalIntegral.integral_congr
    intro X _
    dsimp only
    rw [Finset.sum_div, Finset.sum_div]
    apply Finset.sum_congr rfl
    intro n _
    ring
  rw [h_swap_int]
  have h_int_lhs :
      IntervalIntegrable
        (fun X =>
          ((∑ n ∈ Finset.Icc 1 T, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2) /
            (Real.log X) ^ 2) / X)
        volume Y (RiemannScope.tau * Y) := by
    have hlog_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
      ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1)
    exact (((continuousOn_finset_sum _ (fun n _ =>
      continuousOn_const.mul ((continuousOn_gaussianTermPhi_uIcc_tc061_aux hY2 n).pow 2))).div
      (hlog_cont.pow 2) (fun X hX => (hprops X hX).2.2.2.2)).div
      continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
  have h_mono_int :
      (∫ X in Y..(RiemannScope.tau * Y),
          ((∑ n ∈ Finset.Icc 1 T, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2) /
            (Real.log X) ^ 2) / X) ≤
        ∫ _X in Y..(RiemannScope.tau * Y), (186 : ℝ) / Y := by
    apply intervalIntegral.integral_mono_on hle h_int_lhs intervalIntegrable_const
    intro X hX
    have hX_uIcc : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
    obtain ⟨hX2, hX_pos, _⟩ := hprops X hX_uIcc
    rw [Set.mem_Icc] at hX
    have h_pt := pointwise_diag_gaussian_log_sq_bound_tc061_aux T hX2
    calc
      ((∑ n ∈ Finset.Icc 1 T, (Real.log (n : ℝ)) ^ 2 * (gaussianTermPhi n X) ^ 2) /
          (Real.log X) ^ 2) / X
        ≤ (186 : ℝ) / X := div_le_div_of_nonneg_right h_pt (le_of_lt hX_pos)
      _ ≤ (186 : ℝ) / Y := div_le_div_of_nonneg_left (by norm_num) hY_pos hX.1
  have h_const_eval :
      (∫ _X in Y..(RiemannScope.tau * Y), (186 : ℝ) / Y) = 186 * (RiemannScope.tau - 1) := by
    rw [intervalIntegral.integral_const, smul_eq_mul]
    calc
      (RiemannScope.tau * Y - Y) * (186 / Y)
        = (186 * (RiemannScope.tau - 1) * Y) / Y := by ring
      _ = 186 * (RiemannScope.tau - 1) := mul_div_cancel_right₀ _ (ne_of_gt hY_pos)
  linarith

/-! ### Section 6: Public Theorem 4 (`mixed_covariance_hypothesis_route_d_closure_transfer_tc061`) -/

private theorem rpow_neg_antitone_tc061_aux {Y_star Y α : ℝ} (hY_star : 1 ≤ Y_star)
    (hYY : Y_star ≤ Y) (hα : 0 ≤ α) :
    Y ^ (-α) ≤ Y_star ^ (-α) := by
  have hY_star_pos : 0 < Y_star := lt_of_lt_of_le zero_lt_one hY_star
  have hY_nn : 0 ≤ Y := le_of_lt (lt_of_lt_of_le hY_star_pos hYY)
  have h_pos_pow : 0 < Y_star ^ α := Real.rpow_pos_of_pos hY_star_pos α
  have h_le_pow : Y_star ^ α ≤ Y ^ α := Real.rpow_le_rpow (le_of_lt hY_star_pos) hYY hα
  rw [Real.rpow_neg hY_nn, Real.rpow_neg (le_of_lt hY_star_pos)]
  exact inv_le_inv_of_le h_pos_pow h_le_pow

private theorem polylog_absorption_tc061_aux {η' κ_eta Y : ℝ}
    (hη' : 0 < η') (hκ_pos : 0 < κ_eta) (_hκ_le2 : κ_eta ≤ 2) (hY_ge_e : Real.exp 1 ≤ Y) :
    (Real.log Y) ^ (2 - κ_eta) ≤ (Real.log Y) ^ 2 ∧
      (Real.log Y) ^ 2 ≤ (4 / η' ^ 2) * Y ^ η' := by
  have hY_pos : 0 < Y := lt_of_lt_of_le (Real.exp_pos 1) hY_ge_e
  have hlogY_ge1 : 1 ≤ Real.log Y := by
    have h := Real.log_le_log (Real.exp_pos 1) hY_ge_e
    rwa [Real.log_exp] at h
  have h_pow_le : (Real.log Y) ^ (2 - κ_eta) ≤ (Real.log Y) ^ 2 := by
    have h := Real.rpow_le_rpow_of_exponent_le hlogY_ge1 (by linarith : 2 - κ_eta ≤ (2 : ℝ))
    rwa [Real.rpow_two] at h
  have h_lin : (η' / 2) * Real.log Y ≤ Y ^ (η' / 2) := by
    have h1 : (η' / 2) * Real.log Y ≤ Real.exp ((η' / 2) * Real.log Y) := by
      linarith [Real.add_one_le_exp ((η' / 2) * Real.log Y)]
    have h_exp : Real.exp ((η' / 2) * Real.log Y) = Y ^ (η' / 2) := by
      rw [mul_comm, ← Real.rpow_def_of_pos hY_pos]
    rwa [h_exp] at h1
  have h_sq_half : ((η' / 2) * Real.log Y) ^ 2 ≤ Y ^ η' := by
    have h_nn : 0 ≤ (η' / 2) * Real.log Y := mul_nonneg (by linarith) (by linarith)
    have h_sq := pow_le_pow_left h_nn h_lin 2
    have h_rhs : (Y ^ (η' / 2)) ^ 2 = Y ^ η' := by
      rw [← Real.rpow_natCast (Y ^ (η' / 2)) 2, ← Real.rpow_mul (le_of_lt hY_pos)]
      congr 1; push_cast; ring
    rwa [h_rhs] at h_sq
  have h_log_sq : (Real.log Y) ^ 2 ≤ (4 / η' ^ 2) * Y ^ η' := by
    have hm := mul_le_mul_of_nonneg_left h_sq_half (by positivity : 0 ≤ 4 / η' ^ 2)
    have h_lhs : (4 / η' ^ 2) * ((η' / 2) * Real.log Y) ^ 2 = (Real.log Y) ^ 2 := by
      field_simp [ne_of_gt hη']; ring
    rwa [h_lhs] at hm
  exact ⟨h_pow_le, h_log_sq⟩

/-- **Theorem 4 (`TASK-TC-061`, Polylogarithmic Absorption, Direct Sharper `(8, 2, 2)` Route D Contraction Transfer, All-`ε` `MixedCovarianceClosureHypothesis` Transfer, and Companion `TC-060` Bridge)**:
    1. *Polylogarithm absorption*:
       For `0 < η'`, `0 < κ_eta ≤ 2`, and `Real.exp 1 ≤ Y`:
       `(Real.log Y) ^ (2 - κ_eta) ≤ (Real.log Y) ^ 2 ∧ (Real.log Y) ^ 2 ≤ (4 / η' ^ 2) * Y ^ η'`;
    2. *Direct sharper Route D transfer (`E Y ≤ 8 * D_tilde Y + 2 * J Y + 2 * A_sq Y`)*:
       Exhibits explicit `R`-independent `Y_star`, `F_const`, and `C_tot`, proves simultaneous
       `(1/4, 1/4, 1/4)` feedback bounds, proves the explicit intermediate normalized inequality
       retaining `8 * C_cut + 2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta)` and contracting to
       `F_const + (3 / 4) * normalizedScaleSupremum E ε R`, and closes `E Y ≤ C_tot * Y ^ ε` for all `Y ≥ 1`;
    3. *All-`ε` quantification under `MixedCovarianceClosureHypothesis J D_tilde` (`∀ ε > 0, ∃ C_tot ≥ 0, ∀ Y ≥ 1, E Y ≤ C_tot * Y ^ ε`) AND companion `A_sq ≥ 0` upgrade (`2 * A_sq ≤ 4 * A_sq`)* connecting `R_open = 2 * J` directly to `complete_reconstruction_drift_contraction_transfer_tc060` at intermediate exponent `η' = (η + ε) / 2`. -/
theorem mixed_covariance_hypothesis_route_d_closure_transfer_tc061 :
    (∀ {η' κ_eta Y : ℝ}, 0 < η' → 0 < κ_eta → κ_eta ≤ 2 → Real.exp 1 ≤ Y →
      (Real.log Y) ^ (2 - κ_eta) ≤ (Real.log Y) ^ 2 ∧
        (Real.log Y) ^ 2 ≤ (4 / η' ^ 2) * Y ^ η') ∧
    (∀ {E D_tilde J A_sq : ℝ → ℝ}
        {M_lin ε zeta2_eps C_cut Y_diag η η' a_eta b_eta κ_eta Y_eta a_known B_drift κ_d : ℝ},
      (∀ Z : ℝ, 1 ≤ Z → 0 ≤ E Z) →
      0 ≤ M_lin →
      (∀ Z : ℝ, 1 ≤ Z → E Z ≤ M_lin * Z) →
      0 < ε → 0 ≤ zeta2_eps → 0 ≤ C_cut → Real.exp 1 ≤ Y_diag →
      (∀ Y : ℝ, 1 ≤ Y →
        (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
          (Real.log (pk.1 : ℝ)) ^ 2 / (primePowerScale pk) ^ (1 + ε)) ≤ zeta2_eps) →
      (∀ Y : ℝ, Y_diag ≤ Y →
        D_tilde Y ≤
          (2 / (Real.log Y) ^ 2) *
            (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
              primePowerDiagWeight pk * monotoneScaleEnvelope E (Y / primePowerScale pk)) +
            C_cut) →
      0 < η → η < η' → η' < ε →
      0 ≤ a_eta → 0 ≤ b_eta → 0 < κ_eta → κ_eta ≤ 2 → 2 ≤ Y_eta →
      0 ≤ a_known → 0 ≤ B_drift → 0 < κ_d →
      (∀ R Y : ℝ, Y_diag ≤ Y → Y ≤ R →
        A_sq Y ≤
          a_known * Y ^ η +
            (B_drift / (Real.log Y) ^ κ_d) * normalizedScaleSupremum E ε R * Y ^ ε) →
      (∀ Y : ℝ, Y_eta ≤ Y →
        J Y ≤ a_eta * Y ^ η + b_eta * (Real.log Y) ^ (2 - κ_eta) * D_tilde Y) →
      (∀ Y : ℝ, max Y_diag Y_eta ≤ Y →
        E Y ≤ 8 * D_tilde Y + 2 * J Y + 2 * A_sq Y) →
      let Y_star :=
        max (max Y_diag Y_eta)
          (max (Real.exp (Real.sqrt (64 * zeta2_eps + 1)))
            (max (Real.exp ((8 * B_drift + 1) ^ (1 / κ_d)))
              (Real.exp ((16 * b_eta * zeta2_eps + 1) ^ (1 / κ_eta)))))
      let F_const :=
        2 * (a_eta + a_known) * Y_star ^ (η - ε) +
          8 * C_cut * Y_star ^ (-ε) +
          (8 * b_eta * C_cut / η' ^ 2) * Y_star ^ (η' - ε)
      let C_tot := max (normalizedScaleSupremum E ε Y_star) (4 * F_const)
      max (max Y_diag Y_eta) (Real.exp 1) ≤ Y_star ∧
        (∀ Y : ℝ, Y_star ≤ Y →
          16 * zeta2_eps / (Real.log Y) ^ 2 ≤ 1 / 4 ∧
            2 * (B_drift / (Real.log Y) ^ κ_d) ≤ 1 / 4 ∧
            4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta ≤ 1 / 4) ∧
        (∀ R Y : ℝ, Y_star ≤ Y → Y ≤ R →
          E Y / Y ^ ε ≤
              2 * (a_eta + a_known) * Y ^ (η - ε) +
                (8 * C_cut + 2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta)) / Y ^ ε +
                (16 * zeta2_eps / (Real.log Y) ^ 2 +
                  2 * (B_drift / (Real.log Y) ^ κ_d) +
                  4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta) *
                  normalizedScaleSupremum E ε R ∧
            2 * (a_eta + a_known) * Y ^ (η - ε) +
                (8 * C_cut + 2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta)) / Y ^ ε +
                (16 * zeta2_eps / (Real.log Y) ^ 2 +
                  2 * (B_drift / (Real.log Y) ^ κ_d) +
                  4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta) *
                  normalizedScaleSupremum E ε R ≤
              F_const + (3 / 4 : ℝ) * normalizedScaleSupremum E ε R ∧
            E Y / Y ^ ε ≤ F_const + (3 / 4 : ℝ) * normalizedScaleSupremum E ε R) ∧
        (0 ≤ F_const ∧
          0 ≤ C_tot ∧
          (∀ R : ℝ, Y_star ≤ R → normalizedScaleSupremum E ε R ≤ C_tot) ∧
          (∀ Y : ℝ, 1 ≤ Y → E Y ≤ C_tot * Y ^ ε))) ∧
    ((∀ {E D_tilde J A_sq : ℝ → ℝ} {M_lin : ℝ},
        (∀ Z : ℝ, 1 ≤ Z → 0 ≤ E Z) →
        0 ≤ M_lin →
        (∀ Z : ℝ, 1 ≤ Z → E Z ≤ M_lin * Z) →
        MixedCovarianceClosureHypothesis J D_tilde →
        (∀ ε : ℝ, 0 < ε →
          ∃ zeta2_eps C_cut Y_diag a_known B_drift κ_d : ℝ,
            0 ≤ zeta2_eps ∧ 0 ≤ C_cut ∧ Real.exp 1 ≤ Y_diag ∧
              0 ≤ a_known ∧ 0 ≤ B_drift ∧ 0 < κ_d ∧
              (∀ Y : ℝ, 1 ≤ Y →
                (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
                  (Real.log (pk.1 : ℝ)) ^ 2 / (primePowerScale pk) ^ (1 + ε)) ≤ zeta2_eps) ∧
              (∀ Y : ℝ, Y_diag ≤ Y →
                D_tilde Y ≤
                  (2 / (Real.log Y) ^ 2) *
                    (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
                      primePowerDiagWeight pk * monotoneScaleEnvelope E (Y / primePowerScale pk)) +
                    C_cut) ∧
              (∀ R Y : ℝ, Y_diag ≤ Y → Y ≤ R →
                A_sq Y ≤
                  a_known * Y ^ (ε / 4) +
                    (B_drift / (Real.log Y) ^ κ_d) * normalizedScaleSupremum E ε R * Y ^ ε) ∧
              (∀ Y : ℝ, Y_diag ≤ Y → E Y ≤ 8 * D_tilde Y + 2 * J Y + 2 * A_sq Y)) →
        ∀ ε : ℝ, 0 < ε → ∃ C_tot : ℝ, 0 ≤ C_tot ∧ ∀ Y : ℝ, 1 ≤ Y → E Y ≤ C_tot * Y ^ ε) ∧
      (∀ {D_tilde_val J_val A_sq_val : ℝ},
        0 ≤ A_sq_val →
          8 * D_tilde_val + 2 * J_val + 2 * A_sq_val ≤
            8 * D_tilde_val + 4 * A_sq_val + 2 * J_val) ∧
      (∀ {E D_tilde J A_sq : ℝ → ℝ}
          {M_lin ε zeta2_eps C_cut Y_diag η a_eta b_eta κ_eta Y_eta a_known B_drift κ_d : ℝ},
        (∀ Z : ℝ, 1 ≤ Z → 0 ≤ E Z) →
        0 ≤ M_lin →
        (∀ Z : ℝ, 1 ≤ Z → E Z ≤ M_lin * Z) →
        0 < ε → 0 ≤ zeta2_eps → 0 ≤ C_cut → Real.exp 1 ≤ Y_diag →
        (∀ Y : ℝ, 1 ≤ Y →
          (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
            (Real.log (pk.1 : ℝ)) ^ 2 / (primePowerScale pk) ^ (1 + ε)) ≤ zeta2_eps) →
        (∀ Y : ℝ, Y_diag ≤ Y →
          D_tilde Y ≤
            (2 / (Real.log Y) ^ 2) *
              (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
                primePowerDiagWeight pk * monotoneScaleEnvelope E (Y / primePowerScale pk)) +
              C_cut) →
        0 < η → η < ε →
        0 ≤ a_eta → 0 ≤ b_eta → 0 < κ_eta → κ_eta ≤ 2 → 2 ≤ Y_eta →
        0 ≤ a_known → 0 ≤ B_drift → 0 < κ_d →
        (∀ Y : ℝ, max Y_diag Y_eta ≤ Y → 0 ≤ A_sq Y) →
        (∀ R Y : ℝ, Y_diag ≤ Y → Y ≤ R →
          A_sq Y ≤
            a_known * Y ^ η +
              (B_drift / (Real.log Y) ^ κ_d) * normalizedScaleSupremum E ε R * Y ^ ε) →
        (∀ Y : ℝ, Y_eta ≤ Y →
          J Y ≤ a_eta * Y ^ η + b_eta * (Real.log Y) ^ (2 - κ_eta) * D_tilde Y) →
        (∀ Y : ℝ, max Y_diag Y_eta ≤ Y →
          E Y ≤ 8 * D_tilde Y + 2 * J Y + 2 * A_sq Y) →
        let η' := (η + ε) / 2
        0 < η' ∧ η < η' ∧ η' < ε ∧
          ∃ C_tot : ℝ, 0 ≤ C_tot ∧ ∀ Y : ℝ, 1 ≤ Y → E Y ≤ C_tot * Y ^ ε)) := by
  have h_part2 :
      ∀ {E D_tilde J A_sq : ℝ → ℝ}
          {M_lin ε zeta2_eps C_cut Y_diag η η' a_eta b_eta κ_eta Y_eta a_known B_drift κ_d : ℝ},
        (∀ Z : ℝ, 1 ≤ Z → 0 ≤ E Z) →
        0 ≤ M_lin →
        (∀ Z : ℝ, 1 ≤ Z → E Z ≤ M_lin * Z) →
        0 < ε → 0 ≤ zeta2_eps → 0 ≤ C_cut → Real.exp 1 ≤ Y_diag →
        (∀ Y : ℝ, 1 ≤ Y →
          (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
            (Real.log (pk.1 : ℝ)) ^ 2 / (primePowerScale pk) ^ (1 + ε)) ≤ zeta2_eps) →
        (∀ Y : ℝ, Y_diag ≤ Y →
          D_tilde Y ≤
            (2 / (Real.log Y) ^ 2) *
              (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
                primePowerDiagWeight pk * monotoneScaleEnvelope E (Y / primePowerScale pk)) +
              C_cut) →
        0 < η → η < η' → η' < ε →
        0 ≤ a_eta → 0 ≤ b_eta → 0 < κ_eta → κ_eta ≤ 2 → 2 ≤ Y_eta →
        0 ≤ a_known → 0 ≤ B_drift → 0 < κ_d →
        (∀ R Y : ℝ, Y_diag ≤ Y → Y ≤ R →
          A_sq Y ≤
            a_known * Y ^ η +
              (B_drift / (Real.log Y) ^ κ_d) * normalizedScaleSupremum E ε R * Y ^ ε) →
        (∀ Y : ℝ, Y_eta ≤ Y →
          J Y ≤ a_eta * Y ^ η + b_eta * (Real.log Y) ^ (2 - κ_eta) * D_tilde Y) →
        (∀ Y : ℝ, max Y_diag Y_eta ≤ Y →
          E Y ≤ 8 * D_tilde Y + 2 * J Y + 2 * A_sq Y) →
        let Y_star :=
          max (max Y_diag Y_eta)
            (max (Real.exp (Real.sqrt (64 * zeta2_eps + 1)))
              (max (Real.exp ((8 * B_drift + 1) ^ (1 / κ_d)))
                (Real.exp ((16 * b_eta * zeta2_eps + 1) ^ (1 / κ_eta)))))
        let F_const :=
          2 * (a_eta + a_known) * Y_star ^ (η - ε) +
            8 * C_cut * Y_star ^ (-ε) +
            (8 * b_eta * C_cut / η' ^ 2) * Y_star ^ (η' - ε)
        let C_tot := max (normalizedScaleSupremum E ε Y_star) (4 * F_const)
        max (max Y_diag Y_eta) (Real.exp 1) ≤ Y_star ∧
          (∀ Y : ℝ, Y_star ≤ Y →
            16 * zeta2_eps / (Real.log Y) ^ 2 ≤ 1 / 4 ∧
              2 * (B_drift / (Real.log Y) ^ κ_d) ≤ 1 / 4 ∧
              4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta ≤ 1 / 4) ∧
          (∀ R Y : ℝ, Y_star ≤ Y → Y ≤ R →
            E Y / Y ^ ε ≤
                2 * (a_eta + a_known) * Y ^ (η - ε) +
                  (8 * C_cut + 2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta)) / Y ^ ε +
                  (16 * zeta2_eps / (Real.log Y) ^ 2 +
                    2 * (B_drift / (Real.log Y) ^ κ_d) +
                    4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta) *
                    normalizedScaleSupremum E ε R ∧
              2 * (a_eta + a_known) * Y ^ (η - ε) +
                  (8 * C_cut + 2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta)) / Y ^ ε +
                  (16 * zeta2_eps / (Real.log Y) ^ 2 +
                    2 * (B_drift / (Real.log Y) ^ κ_d) +
                    4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta) *
                    normalizedScaleSupremum E ε R ≤
                F_const + (3 / 4 : ℝ) * normalizedScaleSupremum E ε R ∧
              E Y / Y ^ ε ≤ F_const + (3 / 4 : ℝ) * normalizedScaleSupremum E ε R) ∧
          (0 ≤ F_const ∧
            0 ≤ C_tot ∧
            (∀ R : ℝ, Y_star ≤ R → normalizedScaleSupremum E ε R ≤ C_tot) ∧
            (∀ Y : ℝ, 1 ≤ Y → E Y ≤ C_tot * Y ^ ε)) := by
    intro E D_tilde J A_sq M_lin ε zeta2_eps C_cut Y_diag η η' a_eta b_eta κ_eta Y_eta a_known
      B_drift κ_d hE_nn hM_nn hE_lin hε_pos hzeta_nn hCc_nn hYdiag_ge_e h_zeta_mass hD_route_d
      hη_pos hη_lt_η' hη'_lt_ε ha_eta_nn hb_eta_nn hκ_eta_pos hκ_eta_le2 _hY_eta_ge2
      ha_known_nn hB_drift_nn hκ_d_pos hA_sq hJ_bound hE_direct
    dsimp only
    let Y_star :=
      max (max Y_diag Y_eta)
        (max (Real.exp (Real.sqrt (64 * zeta2_eps + 1)))
          (max (Real.exp ((8 * B_drift + 1) ^ (1 / κ_d)))
            (Real.exp ((16 * b_eta * zeta2_eps + 1) ^ (1 / κ_eta)))))
    let F_const :=
      2 * (a_eta + a_known) * Y_star ^ (η - ε) +
        8 * C_cut * Y_star ^ (-ε) +
        (8 * b_eta * C_cut / η' ^ 2) * Y_star ^ (η' - ε)
    let C_tot := max (normalizedScaleSupremum E ε Y_star) (4 * F_const)
    have hη'_pos : 0 < η' := lt_trans hη_pos hη_lt_η'
    have he_ge1 : (1 : ℝ) ≤ Real.exp 1 :=
      le_trans (by norm_num : (1 : ℝ) ≤ 1 + 1) (Real.add_one_le_exp 1)
    have hYs_ge_max : max Y_diag Y_eta ≤ Y_star := le_max_left _ _
    have hYs_ge_diag : Y_diag ≤ Y_star := le_trans (le_max_left _ _) hYs_ge_max
    have hYs_ge_eta : Y_eta ≤ Y_star := le_trans (le_max_right _ _) hYs_ge_max
    have hYs_ge_e : Real.exp 1 ≤ Y_star := le_trans hYdiag_ge_e hYs_ge_diag
    have hYs_ge1 : 1 ≤ Y_star := le_trans he_ge1 hYs_ge_e
    have hYs_pos : 0 < Y_star := lt_of_lt_of_le zero_lt_one hYs_ge1
    have h_max_le : max (max Y_diag Y_eta) (Real.exp 1) ≤ Y_star :=
      max_le hYs_ge_max hYs_ge_e
    have h_fb :
        ∀ Y : ℝ, Y_star ≤ Y →
          16 * zeta2_eps / (Real.log Y) ^ 2 ≤ 1 / 4 ∧
            2 * (B_drift / (Real.log Y) ^ κ_d) ≤ 1 / 4 ∧
            4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta ≤ 1 / 4 := by
      intro Y hYYs
      have hY_ge_e : Real.exp 1 ≤ Y := le_trans hYs_ge_e hYYs
      have hlogY_ge1 : 1 ≤ Real.log Y := by
        have h := Real.log_le_log (Real.exp_pos 1) hY_ge_e
        rwa [Real.log_exp] at h
      have hlogY_pos : 0 < Real.log Y := lt_of_lt_of_le zero_lt_one hlogY_ge1
      have h_ge_z : Real.exp (Real.sqrt (64 * zeta2_eps + 1)) ≤ Y :=
        le_trans (le_trans (le_max_left _ _) (le_max_right _ _)) hYYs
      have h_ge_d : Real.exp ((8 * B_drift + 1) ^ (1 / κ_d)) ≤ Y :=
        le_trans (le_trans (le_max_left _ _) (le_trans (le_max_right _ _) (le_max_right _ _))) hYYs
      have h_ge_b : Real.exp ((16 * b_eta * zeta2_eps + 1) ^ (1 / κ_eta)) ≤ Y :=
        le_trans (le_trans (le_max_right _ _) (le_trans (le_max_right _ _) (le_max_right _ _))) hYYs
      have h_log_z : Real.sqrt (64 * zeta2_eps + 1) ≤ Real.log Y := by
        have h := Real.log_le_log (Real.exp_pos _) h_ge_z
        rwa [Real.log_exp] at h
      have h_sq_z : 64 * zeta2_eps + 1 ≤ (Real.log Y) ^ 2 := by
        have h1 := pow_le_pow_left (Real.sqrt_nonneg _) h_log_z 2
        rwa [Real.sq_sqrt (by positivity)] at h1
      have h_fb1 : 16 * zeta2_eps / (Real.log Y) ^ 2 ≤ 1 / 4 := by
        rw [div_le_iff (sq_pos_of_pos hlogY_pos)]
        linarith
      have h_base_d : 0 < 8 * B_drift + 1 := by positivity
      have h_log_d : (8 * B_drift + 1) ^ (1 / κ_d) ≤ Real.log Y := by
        have h := Real.log_le_log (Real.exp_pos _) h_ge_d
        rwa [Real.log_exp] at h
      have h_pow_d : 8 * B_drift + 1 ≤ (Real.log Y) ^ κ_d := by
        have h1 := Real.rpow_le_rpow (by positivity) h_log_d (le_of_lt hκ_d_pos)
        rwa [← Real.rpow_mul (le_of_lt h_base_d), one_div_mul_cancel (ne_of_gt hκ_d_pos),
          Real.rpow_one] at h1
      have h_fb2 : 2 * (B_drift / (Real.log Y) ^ κ_d) ≤ 1 / 4 := by
        rw [show 2 * (B_drift / (Real.log Y) ^ κ_d) = 2 * B_drift / (Real.log Y) ^ κ_d by ring,
          div_le_iff (Real.rpow_pos_of_pos hlogY_pos κ_d)]
        linarith
      have h_base_b : 0 < 16 * b_eta * zeta2_eps + 1 := by positivity
      have h_log_b : (16 * b_eta * zeta2_eps + 1) ^ (1 / κ_eta) ≤ Real.log Y := by
        have h := Real.log_le_log (Real.exp_pos _) h_ge_b
        rwa [Real.log_exp] at h
      have h_pow_b : 16 * b_eta * zeta2_eps + 1 ≤ (Real.log Y) ^ κ_eta := by
        have h1 := Real.rpow_le_rpow (by positivity) h_log_b (le_of_lt hκ_eta_pos)
        rwa [← Real.rpow_mul (le_of_lt h_base_b), one_div_mul_cancel (ne_of_gt hκ_eta_pos),
          Real.rpow_one] at h1
      have h_fb3 : 4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta ≤ 1 / 4 := by
        rw [div_le_iff (Real.rpow_pos_of_pos hlogY_pos κ_eta)]
        linarith
      exact ⟨h_fb1, h_fb2, h_fb3⟩
    obtain ⟨hG_props, ⟨_, _, hD_hor⟩, _, _⟩ :=
      repaired_weighted_diagonal_closure_and_actual_observable_tc059r
    obtain ⟨hYs_fin, hG_mono⟩ := hG_props hE_nn hM_nn hE_lin (le_of_lt hε_pos)
    have h_pt_chain :
        ∀ R Y : ℝ, Y_star ≤ Y → Y ≤ R →
          E Y / Y ^ ε ≤
              2 * (a_eta + a_known) * Y ^ (η - ε) +
                (8 * C_cut + 2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta)) / Y ^ ε +
                (16 * zeta2_eps / (Real.log Y) ^ 2 +
                  2 * (B_drift / (Real.log Y) ^ κ_d) +
                  4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta) *
                  normalizedScaleSupremum E ε R ∧
            2 * (a_eta + a_known) * Y ^ (η - ε) +
                (8 * C_cut + 2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta)) / Y ^ ε +
                (16 * zeta2_eps / (Real.log Y) ^ 2 +
                  2 * (B_drift / (Real.log Y) ^ κ_d) +
                  4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta) *
                  normalizedScaleSupremum E ε R ≤
              F_const + (3 / 4 : ℝ) * normalizedScaleSupremum E ε R ∧
            E Y / Y ^ ε ≤ F_const + (3 / 4 : ℝ) * normalizedScaleSupremum E ε R := by
      intro R Y hYYs hYR
      have hYYd : Y_diag ≤ Y := le_trans hYs_ge_diag hYYs
      have hYYe : Y_eta ≤ Y := le_trans hYs_ge_eta hYYs
      have hYYm : max Y_diag Y_eta ≤ Y := le_trans hYs_ge_max hYYs
      have hRYd : Y_diag ≤ R := le_trans hYYd hYR
      have hY_ge_e : Real.exp 1 ≤ Y := le_trans hYs_ge_e hYYs
      have hY1 : 1 ≤ Y := le_trans hYs_ge1 hYYs
      have hR1 : 1 ≤ R := le_trans hY1 hYR
      have hY_pos : 0 < Y := lt_of_lt_of_le zero_lt_one hY1
      have hY_pow_pos : 0 < Y ^ ε := Real.rpow_pos_of_pos hY_pos ε
      have hlogY_ge1 : 1 ≤ Real.log Y := by
        have h := Real.log_le_log (Real.exp_pos 1) hY_ge_e
        rwa [Real.log_exp] at h
      have hlogY_pos : 0 < Real.log Y := lt_of_lt_of_le zero_lt_one hlogY_ge1
      have hGR_nn : 0 ≤ normalizedScaleSupremum E ε R := (hYs_fin hR1).2.2.1
      have hD_norm :=
        hD_hor hE_nn hM_nn hE_lin hε_pos hzeta_nn hCc_nn hYdiag_ge_e h_zeta_mass hD_route_d
          R Y hRYd hYYd hYR
      have h_E_comb :
          E Y ≤
            (8 + 2 * b_eta * (Real.log Y) ^ (2 - κ_eta)) * D_tilde Y +
              2 * a_eta * Y ^ η + 2 * A_sq Y := by
        linarith [hE_direct Y hYYm, hJ_bound Y hYYe]
      have h_E_div0 :
          E Y / Y ^ ε ≤
            (8 + 2 * b_eta * (Real.log Y) ^ (2 - κ_eta)) * (D_tilde Y / Y ^ ε) +
              2 * a_eta * (Y ^ η / Y ^ ε) + 2 * (A_sq Y / Y ^ ε) := by
        have hd := div_le_div_of_nonneg_right h_E_comb (le_of_lt hY_pow_pos)
        calc
          E Y / Y ^ ε
            ≤ ((8 + 2 * b_eta * (Real.log Y) ^ (2 - κ_eta)) * D_tilde Y +
                2 * a_eta * Y ^ η + 2 * A_sq Y) / Y ^ ε := hd
          _ = (8 + 2 * b_eta * (Real.log Y) ^ (2 - κ_eta)) * (D_tilde Y / Y ^ ε) +
                2 * a_eta * (Y ^ η / Y ^ ε) + 2 * (A_sq Y / Y ^ ε) := by ring
      have h_log_cancel :
          (2 * b_eta * (Real.log Y) ^ (2 - κ_eta)) * (2 * zeta2_eps / (Real.log Y) ^ 2) =
            4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta := by
        have h_sub : (Real.log Y) ^ (2 - κ_eta) = (Real.log Y) ^ 2 / (Real.log Y) ^ κ_eta := by
          rw [Real.rpow_sub hlogY_pos, Real.rpow_two]
        rw [h_sub]
        field_simp [ne_of_gt (sq_pos_of_pos hlogY_pos),
          ne_of_gt (Real.rpow_pos_of_pos hlogY_pos κ_eta)]
        ring
      have h_fac_nn : 0 ≤ 8 + 2 * b_eta * (Real.log Y) ^ (2 - κ_eta) :=
        add_nonneg (by norm_num)
          (mul_nonneg (by positivity) (Real.rpow_nonneg (le_of_lt hlogY_pos) _))
      have h_D_term :
          (8 + 2 * b_eta * (Real.log Y) ^ (2 - κ_eta)) * (D_tilde Y / Y ^ ε) ≤
            (16 * zeta2_eps / (Real.log Y) ^ 2 +
                4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta) *
              normalizedScaleSupremum E ε R +
              (8 * C_cut + 2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta)) / Y ^ ε := by
        have hm := mul_le_mul_of_nonneg_left hD_norm h_fac_nn
        have h_rhs_eq :
            (8 + 2 * b_eta * (Real.log Y) ^ (2 - κ_eta)) *
                ((2 * zeta2_eps / (Real.log Y) ^ 2) * normalizedScaleSupremum E ε R +
                  C_cut / Y ^ ε) =
              (8 * (2 * zeta2_eps / (Real.log Y) ^ 2) +
                  (2 * b_eta * (Real.log Y) ^ (2 - κ_eta)) *
                    (2 * zeta2_eps / (Real.log Y) ^ 2)) *
                normalizedScaleSupremum E ε R +
                (8 * C_cut + 2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta)) / Y ^ ε := by ring
        rw [h_rhs_eq, h_log_cancel] at hm
        have h16 : 8 * (2 * zeta2_eps / (Real.log Y) ^ 2) = 16 * zeta2_eps / (Real.log Y) ^ 2 := by
          ring
        rw [h16] at hm
        exact hm
      have h_rpow_sub_η : Y ^ η / Y ^ ε = Y ^ (η - ε) := (Real.rpow_sub hY_pos η ε).symm
      have h_A_term :
          2 * (A_sq Y / Y ^ ε) ≤
            2 * a_known * Y ^ (η - ε) +
              (2 * (B_drift / (Real.log Y) ^ κ_d)) * normalizedScaleSupremum E ε R := by
        have hd := div_le_div_of_nonneg_right (hA_sq R Y hYYd hYR) (le_of_lt hY_pow_pos)
        have h_simp :
            (a_known * Y ^ η +
                (B_drift / (Real.log Y) ^ κ_d) * normalizedScaleSupremum E ε R * Y ^ ε) / Y ^ ε =
              a_known * Y ^ (η - ε) +
                (B_drift / (Real.log Y) ^ κ_d) * normalizedScaleSupremum E ε R := by
          rw [add_div, mul_div_assoc, h_rpow_sub_η,
            mul_div_cancel_right₀ _ (ne_of_gt hY_pow_pos)]
        rw [h_simp] at hd
        linarith
      have h_step1 :
          E Y / Y ^ ε ≤
            2 * (a_eta + a_known) * Y ^ (η - ε) +
              (8 * C_cut + 2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta)) / Y ^ ε +
              (16 * zeta2_eps / (Real.log Y) ^ 2 +
                2 * (B_drift / (Real.log Y) ^ κ_d) +
                4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta) *
                normalizedScaleSupremum E ε R := by
        rw [h_rpow_sub_η] at h_E_div0
        linarith [h_E_div0, h_D_term, h_A_term]
      obtain ⟨h_abs1, h_abs2⟩ :=
        polylog_absorption_tc061_aux hη'_pos hκ_eta_pos hκ_eta_le2 hY_ge_e
      have h_eta_dec : Y ^ (η - ε) ≤ Y_star ^ (η - ε) := by
        rw [show η - ε = -(ε - η) by ring]
        exact rpow_neg_antitone_tc061_aux hYs_ge1 hYYs (by linarith)
      have h_eta'_dec : Y ^ (η' - ε) ≤ Y_star ^ (η' - ε) := by
        rw [show η' - ε = -(ε - η') by ring]
        exact rpow_neg_antitone_tc061_aux hYs_ge1 hYYs (by linarith)
      have h_eps_dec : Y ^ (-ε) ≤ Y_star ^ (-ε) :=
        rpow_neg_antitone_tc061_aux hYs_ge1 hYYs (le_of_lt hε_pos)
      have h_cut_abs :
          (8 * C_cut + 2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta)) / Y ^ ε ≤
            8 * C_cut * Y_star ^ (-ε) +
              (8 * b_eta * C_cut / η' ^ 2) * Y_star ^ (η' - ε) := by
        have h_log_y : (Real.log Y) ^ (2 - κ_eta) ≤ (4 / η' ^ 2) * Y ^ η' :=
          le_trans h_abs1 h_abs2
        have hm :=
          mul_le_mul_of_nonneg_left h_log_y (by positivity : 0 ≤ 2 * b_eta * C_cut)
        have hd := div_le_div_of_nonneg_right
          (add_le_add_left hm (8 * C_cut)) (le_of_lt hY_pow_pos)
        have h_split_c :
            (8 * C_cut + 2 * b_eta * C_cut * ((4 / η' ^ 2) * Y ^ η')) / Y ^ ε =
              8 * C_cut * Y ^ (-ε) + (8 * b_eta * C_cut / η' ^ 2) * Y ^ (η' - ε) := by
          have hr1 : 8 * C_cut / Y ^ ε = 8 * C_cut * Y ^ (-ε) := by
            rw [div_eq_mul_inv, Real.rpow_neg (le_of_lt hY_pos)]
          have hr2 : Y ^ η' / Y ^ ε = Y ^ (η' - ε) := (Real.rpow_sub hY_pos η' ε).symm
          calc
            (8 * C_cut + 2 * b_eta * C_cut * ((4 / η' ^ 2) * Y ^ η')) / Y ^ ε
              = 8 * C_cut / Y ^ ε + (8 * b_eta * C_cut / η' ^ 2) * (Y ^ η' / Y ^ ε) := by ring
            _ = 8 * C_cut * Y ^ (-ε) + (8 * b_eta * C_cut / η' ^ 2) * Y ^ (η' - ε) := by
                rw [hr1, hr2]
        rw [h_split_c] at hd
        have hc1 := mul_le_mul_of_nonneg_left h_eps_dec (by positivity : 0 ≤ 8 * C_cut)
        have hc2 :=
          mul_le_mul_of_nonneg_left h_eta'_dec (by positivity : 0 ≤ 8 * b_eta * C_cut / η' ^ 2)
        linarith
      obtain ⟨h_fb1, h_fb2, h_fb3⟩ := h_fb Y hYYs
      have h_fb_sum :
          (16 * zeta2_eps / (Real.log Y) ^ 2 +
              2 * (B_drift / (Real.log Y) ^ κ_d) +
              4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta) *
            normalizedScaleSupremum E ε R ≤
            (3 / 4 : ℝ) * normalizedScaleSupremum E ε R :=
        mul_le_mul_of_nonneg_right (by linarith) hGR_nn
      have h_a_dec :=
        mul_le_mul_of_nonneg_left h_eta_dec (by positivity : 0 ≤ 2 * (a_eta + a_known))
      have h_step2 :
          2 * (a_eta + a_known) * Y ^ (η - ε) +
              (8 * C_cut + 2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta)) / Y ^ ε +
              (16 * zeta2_eps / (Real.log Y) ^ 2 +
                2 * (B_drift / (Real.log Y) ^ κ_d) +
                4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta) *
                normalizedScaleSupremum E ε R ≤
            F_const + (3 / 4 : ℝ) * normalizedScaleSupremum E ε R := by
        dsimp [F_const]
        linarith [h_a_dec, h_cut_abs, h_fb_sum]
      exact ⟨h_step1, h_step2, le_trans h_step1 h_step2⟩
    have hF_nn : 0 ≤ F_const := by
      dsimp [F_const]
      exact add_nonneg
        (add_nonneg
          (mul_nonneg (by positivity) (Real.rpow_nonneg (le_of_lt hYs_pos) _))
          (mul_nonneg (by positivity) (Real.rpow_nonneg (le_of_lt hYs_pos) _)))
        (mul_nonneg (by positivity) (Real.rpow_nonneg (le_of_lt hYs_pos) _))
    have hGYs_nn : 0 ≤ normalizedScaleSupremum E ε Y_star := (hYs_fin hYs_ge1).2.2.1
    have hCtot_nn : 0 ≤ C_tot := le_trans hGYs_nn (le_max_left _ _)
    have h_R_ge : ∀ R : ℝ, Y_star ≤ R → normalizedScaleSupremum E ε R ≤ C_tot := by
      intro R hRYs
      have hR1 : 1 ≤ R := le_trans hYs_ge1 hRYs
      have h_ne_R := (hYs_fin hR1).1
      have h_bdd_Ys := (hYs_fin hYs_ge1).2.1
      have h_sup_split :
          normalizedScaleSupremum E ε R ≤
            max (normalizedScaleSupremum E ε Y_star)
              (F_const + (3 / 4 : ℝ) * normalizedScaleSupremum E ε R) := by
        show sSup ((fun Z => E Z / Z ^ ε) '' Set.Icc 1 R) ≤ _
        apply csSup_le h_ne_R
        rintro _ ⟨Z, ⟨hZ1, hZR⟩, rfl⟩
        by_cases hZYs : Z ≤ Y_star
        · exact le_trans (le_csSup h_bdd_Ys ⟨Z, ⟨hZ1, hZYs⟩, rfl⟩) (le_max_left _ _)
        · push_neg at hZYs
          exact le_trans (h_pt_chain R Z (le_of_lt hZYs) hZR).2.2 (le_max_right _ _)
      rcases max_cases (normalizedScaleSupremum E ε Y_star)
          (F_const + (3 / 4 : ℝ) * normalizedScaleSupremum E ε R) with
        ⟨h_eq, _⟩ | ⟨h_eq, _⟩
      · rw [h_eq] at h_sup_split
        exact le_trans h_sup_split (le_max_left _ _)
      · rw [h_eq] at h_sup_split
        have h_4F : normalizedScaleSupremum E ε R ≤ 4 * F_const := by
          have h_quarter :
              (1 / 4 : ℝ) * normalizedScaleSupremum E ε R ≤ F_const := by
            calc
              (1 / 4 : ℝ) * normalizedScaleSupremum E ε R
                = normalizedScaleSupremum E ε R -
                    (3 / 4 : ℝ) * normalizedScaleSupremum E ε R := by ring
              _ ≤ (F_const + (3 / 4 : ℝ) * normalizedScaleSupremum E ε R) -
                    (3 / 4 : ℝ) * normalizedScaleSupremum E ε R :=
                  sub_le_sub_right h_sup_split _
              _ = F_const := by ring
          have hm := mul_le_mul_of_nonneg_left h_quarter (by norm_num : (0 : ℝ) ≤ 4)
          calc
            normalizedScaleSupremum E ε R
              = 4 * ((1 / 4 : ℝ) * normalizedScaleSupremum E ε R) := by ring
            _ ≤ 4 * F_const := hm
        exact le_trans h_4F (le_max_right _ _)
    refine ⟨h_max_le, h_fb, h_pt_chain, hF_nn, hCtot_nn, h_R_ge, ?_⟩
    intro Y hY1
    have hY_pos : 0 < Y := lt_of_lt_of_le zero_lt_one hY1
    have hY_pow_pos : 0 < Y ^ ε := Real.rpow_pos_of_pos hY_pos ε
    have h_bdd_Y := (hYs_fin hY1).2.1
    have h_div_le_GY : E Y / Y ^ ε ≤ normalizedScaleSupremum E ε Y :=
      le_csSup h_bdd_Y ⟨Y, ⟨hY1, le_refl Y⟩, rfl⟩
    have hGY_le_C : normalizedScaleSupremum E ε Y ≤ C_tot := by
      by_cases hYYs : Y ≤ Y_star
      · exact le_trans (hG_mono Y Y_star hY1 hYYs) (le_max_left _ _)
      · push_neg at hYYs
        exact h_R_ge Y (le_of_lt hYYs)
    exact (div_le_iff hY_pow_pos).mp (le_trans h_div_le_GY hGY_le_C)
  refine ⟨fun hη' hκ_pos hκ_le2 hY_ge_e =>
    polylog_absorption_tc061_aux hη' hκ_pos hκ_le2 hY_ge_e, h_part2, ?_⟩
  refine ⟨?_, ?_, ?_⟩
  · intro E D_tilde J A_sq M_lin hE_nn hM_nn hE_lin h_hyp h_all_eps ε hε_pos
    obtain ⟨zeta2_eps, C_cut, Y_diag, a_known, B_drift, κ_d,
      hzeta_nn, hCc_nn, hYdiag_ge_e, ha_known_nn, hB_drift_nn, hκ_d_pos,
      h_zeta_mass, hD_route_d, hA_sq, hE_yd⟩ := h_all_eps ε hε_pos
    obtain ⟨a_eta, b_eta, κ_eta, Y_eta,
      ha_eta_nn, hb_eta_nn, hκ_eta_pos, hκ_eta_le2, hY_eta_ge2, hJ_bound⟩ :=
      h_hyp (ε / 4) (by linarith)
    have hE_max : ∀ Y : ℝ, max Y_diag Y_eta ≤ Y → E Y ≤ 8 * D_tilde Y + 2 * J Y + 2 * A_sq Y :=
      fun Y hY => hE_yd Y (le_trans (le_max_left _ _) hY)
    have h_res :=
      h_part2 hE_nn hM_nn hE_lin hε_pos hzeta_nn hCc_nn hYdiag_ge_e h_zeta_mass hD_route_d
        (η := ε / 4) (η' := ε / 2) (by linarith) (by linarith) (by linarith)
        ha_eta_nn hb_eta_nn hκ_eta_pos hκ_eta_le2 hY_eta_ge2
        ha_known_nn hB_drift_nn hκ_d_pos hA_sq hJ_bound hE_max
    exact ⟨_, h_res.2.2.2.2.1, h_res.2.2.2.2.2.2⟩
  · intro D_tilde_val J_val A_sq_val hA_nn
    linarith
  · intro E D_tilde J A_sq M_lin ε zeta2_eps C_cut Y_diag η a_eta b_eta κ_eta Y_eta a_known
      B_drift κ_d hE_nn hM_nn hE_lin hε_pos hzeta_nn hCc_nn hYdiag_ge_e h_zeta_mass hD_route_d
      hη_pos hη_lt_ε ha_eta_nn hb_eta_nn hκ_eta_pos hκ_eta_le2 _hY_eta_ge2
      ha_known_nn hB_drift_nn hκ_d_pos hA_nn hA_sq hJ_bound hE_direct
    dsimp only
    let η' := (η + ε) / 2
    have hη'_pos : 0 < η' := by dsimp [η']; linarith
    have hη_lt_η' : η < η' := by dsimp [η']; linarith
    have hη'_lt_ε : η' < ε := by dsimp [η']; linarith
    refine ⟨hη'_pos, hη_lt_η', hη'_lt_ε, ?_⟩
    let Y_diag' :=
      max (max Y_diag Y_eta) (Real.exp ((16 * b_eta * zeta2_eps + 1) ^ (1 / κ_eta)))
    let A_open := 2 * a_eta + 8 * b_eta * C_cut / η' ^ 2
    have hYd'_ge_max : max Y_diag Y_eta ≤ Y_diag' := le_max_left _ _
    have hYd'_ge_diag : Y_diag ≤ Y_diag' := le_trans (le_max_left _ _) hYd'_ge_max
    have hYd'_ge_eta : Y_eta ≤ Y_diag' := le_trans (le_max_right _ _) hYd'_ge_max
    have hYd'_ge_e : Real.exp 1 ≤ Y_diag' := le_trans hYdiag_ge_e hYd'_ge_diag
    have he_ge1 : (1 : ℝ) ≤ Real.exp 1 :=
      le_trans (by norm_num : (1 : ℝ) ≤ 1 + 1) (Real.add_one_le_exp 1)
    have hD_route_d' :
        ∀ Y : ℝ, Y_diag' ≤ Y →
          D_tilde Y ≤
            (2 / (Real.log Y) ^ 2) *
              (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
                primePowerDiagWeight pk * monotoneScaleEnvelope E (Y / primePowerScale pk)) +
              C_cut :=
      fun Y hY => hD_route_d Y (le_trans hYd'_ge_diag hY)
    have hA_sq' :
        ∀ R Y : ℝ, Y_diag' ≤ Y → Y ≤ R →
          A_sq Y ≤
            a_known * Y ^ η' +
              (B_drift / (Real.log Y) ^ κ_d) * normalizedScaleSupremum E ε R * Y ^ ε := by
      intro R Y hYYd' hYR
      have hY1 : 1 ≤ Y := le_trans he_ge1 (le_trans hYd'_ge_e hYYd')
      have h_pow_mono : Y ^ η ≤ Y ^ η' :=
        Real.rpow_le_rpow_of_exponent_le hY1 (le_of_lt hη_lt_η')
      have hm := mul_le_mul_of_nonneg_left h_pow_mono ha_known_nn
      linarith [hA_sq R Y (le_trans hYd'_ge_diag hYYd') hYR]
    have hE_4 :
        ∀ Y : ℝ, Y_diag' ≤ Y → E Y ≤ 8 * D_tilde Y + 4 * A_sq Y + 2 * J Y := by
      intro Y hYYd'
      have hYm : max Y_diag Y_eta ≤ Y := le_trans hYd'_ge_max hYYd'
      linarith [hE_direct Y hYm, hA_nn Y hYm]
    have h_tc060 :=
      (complete_reconstruction_drift_contraction_transfer_tc060).2.2
        (R_open := fun Y => 2 * J Y) (Y_diag := Y_diag') (η := η') (A_open := A_open)
        hE_nn hM_nn hE_lin hε_pos hzeta_nn hCc_nn hYd'_ge_e h_zeta_mass hD_route_d'
        hη'_pos hη'_lt_ε ha_known_nn hB_drift_nn hκ_d_pos (by positivity) hA_sq' hE_4
    obtain ⟨hG_props, ⟨_, _, hD_hor⟩, _, _⟩ :=
      repaired_weighted_diagonal_closure_and_actual_observable_tc059r
    obtain ⟨hYs_fin, _⟩ := hG_props hE_nn hM_nn hE_lin (le_of_lt hε_pos)
    have hR_open_bd :
        ∀ R Y : ℝ,
          max Y_diag'
              (max (Real.exp (Real.sqrt (64 * zeta2_eps + 1)))
                (Real.exp ((16 * B_drift + 1) ^ (1 / κ_d)))) ≤ Y →
            Y ≤ R →
            2 * J Y ≤ A_open * Y ^ η' + (1 / 4 : ℝ) * normalizedScaleSupremum E ε R * Y ^ ε := by
      intro R Y hYYs hYR
      have hYYd' : Y_diag' ≤ Y := le_trans (le_max_left _ _) hYYs
      have hRYd' : Y_diag' ≤ R := le_trans hYYd' hYR
      have hY_ge_e : Real.exp 1 ≤ Y := le_trans hYd'_ge_e hYYd'
      have hY1 : 1 ≤ Y := le_trans he_ge1 hY_ge_e
      have hR1 : 1 ≤ R := le_trans hY1 hYR
      have hY_pos : 0 < Y := lt_of_lt_of_le zero_lt_one hY1
      have hY_pow_pos : 0 < Y ^ ε := Real.rpow_pos_of_pos hY_pos ε
      have hlogY_ge1 : 1 ≤ Real.log Y := by
        have h := Real.log_le_log (Real.exp_pos 1) hY_ge_e
        rwa [Real.log_exp] at h
      have hlogY_pos : 0 < Real.log Y := lt_of_lt_of_le zero_lt_one hlogY_ge1
      have hGR_nn : 0 ≤ normalizedScaleSupremum E ε R := (hYs_fin hR1).2.2.1
      have hD_norm :=
        hD_hor hE_nn hM_nn hE_lin hε_pos hzeta_nn hCc_nn hYd'_ge_e h_zeta_mass hD_route_d'
          R Y hRYd' hYYd' hYR
      have hD_raw :
          D_tilde Y ≤
            (2 * zeta2_eps / (Real.log Y) ^ 2) * normalizedScaleSupremum E ε R * Y ^ ε + C_cut := by
        have hm := (div_le_iff hY_pow_pos).mp hD_norm
        have h_cancel : C_cut / Y ^ ε * Y ^ ε = C_cut :=
          div_mul_cancel₀ C_cut (ne_of_gt hY_pow_pos)
        linarith
      have h_ge_b : Real.exp ((16 * b_eta * zeta2_eps + 1) ^ (1 / κ_eta)) ≤ Y :=
        le_trans (le_max_right _ _) hYYd'
      have h_base_b : 0 < 16 * b_eta * zeta2_eps + 1 := by positivity
      have h_log_b : (16 * b_eta * zeta2_eps + 1) ^ (1 / κ_eta) ≤ Real.log Y := by
        have h := Real.log_le_log (Real.exp_pos _) h_ge_b
        rwa [Real.log_exp] at h
      have h_pow_b : 16 * b_eta * zeta2_eps + 1 ≤ (Real.log Y) ^ κ_eta := by
        have h1 := Real.rpow_le_rpow (by positivity) h_log_b (le_of_lt hκ_eta_pos)
        rwa [← Real.rpow_mul (le_of_lt h_base_b), one_div_mul_cancel (ne_of_gt hκ_eta_pos),
          Real.rpow_one] at h1
      have h_fb3 : 4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta ≤ 1 / 4 := by
        rw [div_le_iff (Real.rpow_pos_of_pos hlogY_pos κ_eta)]
        linarith
      have h_log_cancel :
          (2 * b_eta * (Real.log Y) ^ (2 - κ_eta)) * (2 * zeta2_eps / (Real.log Y) ^ 2) =
            4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta := by
        have h_sub : (Real.log Y) ^ (2 - κ_eta) = (Real.log Y) ^ 2 / (Real.log Y) ^ κ_eta := by
          rw [Real.rpow_sub hlogY_pos, Real.rpow_two]
        rw [h_sub]
        field_simp [ne_of_gt (sq_pos_of_pos hlogY_pos),
          ne_of_gt (Real.rpow_pos_of_pos hlogY_pos κ_eta)]
        ring
      obtain ⟨h_abs1, h_abs2⟩ :=
        polylog_absorption_tc061_aux hη'_pos hκ_eta_pos hκ_eta_le2 hY_ge_e
      have h_pow_mono : Y ^ η ≤ Y ^ η' :=
        Real.rpow_le_rpow_of_exponent_le hY1 (le_of_lt hη_lt_η')
      have h_a_mono := mul_le_mul_of_nonneg_left h_pow_mono (by positivity : 0 ≤ 2 * a_eta)
      have h_cut_abs :
          2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta) ≤
            (8 * b_eta * C_cut / η' ^ 2) * Y ^ η' := by
        have hm :=
          mul_le_mul_of_nonneg_left (le_trans h_abs1 h_abs2) (by positivity : 0 ≤ 2 * b_eta * C_cut)
        calc
          2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta)
            ≤ 2 * b_eta * C_cut * ((4 / η' ^ 2) * Y ^ η') := hm
          _ = (8 * b_eta * C_cut / η' ^ 2) * Y ^ η' := by ring
      have h_bD :=
        mul_le_mul_of_nonneg_left hD_raw
          (by positivity : 0 ≤ 2 * b_eta * (Real.log Y) ^ (2 - κ_eta))
      have h_bD_exp :
          (2 * b_eta * (Real.log Y) ^ (2 - κ_eta)) *
              ((2 * zeta2_eps / (Real.log Y) ^ 2) * normalizedScaleSupremum E ε R * Y ^ ε +
                C_cut) =
            (4 * b_eta * zeta2_eps / (Real.log Y) ^ κ_eta) *
                (normalizedScaleSupremum E ε R * Y ^ ε) +
              2 * b_eta * C_cut * (Real.log Y) ^ (2 - κ_eta) := by
        rw [← h_log_cancel]; ring
      rw [h_bD_exp] at h_bD
      have h_fb_mul :=
        mul_le_mul_of_nonneg_right h_fb3
          (mul_nonneg hGR_nn (le_of_lt hY_pow_pos))
      have h2J := mul_le_mul_of_nonneg_left (hJ_bound Y (le_trans hYd'_ge_eta hYYd'))
        (by norm_num : (0 : ℝ) ≤ 2)
      dsimp [A_open]
      linarith
    have h_closed := h_tc060.2.2 hR_open_bd
    exact ⟨_, h_closed.2.1, h_closed.2.2.2⟩

end MixedArithmeticCovariance
end RiemannScope
