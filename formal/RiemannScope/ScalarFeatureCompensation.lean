/-
RiemannScope.ScalarFeatureCompensation
TASK-TC-065 (EPIC-TC-042 / SUBGATE-TC-043A):
Arithmetic Scalar-Feature Compensation, Paired-Station Synthesis, Uniform Cutoff-Fringe
Enclosures, Coupled Mode Expansions, and Bare-Liouville Shifted-Dilation Closure.

Formalizes in Lean 4 (complete machine-checked proofs using canonical circle constant
RiemannScope.tau throughout; complex coordinates written z = (x : ℂ) + (y : ℂ) * Complex.I
with real coordinates x, y and critical line x = 1 / 2; real analytic scale Y ≥ 2):
1. `damped_core_defect_and_closure_equivalence_tc065`
2. `paired_station_partition_divisor_synthesis_and_telescoping_tc065`
3. `arithmetic_synthesis_hilbert_budget_operator_norm_and_obstructions_tc065`
4. `coupled_mode_expansion_uniform_fringe_bounds_and_orthogonality_tc065`
5. `bare_liouville_shifted_dilation_closure_and_euler_limit_tc065`
-/

import RiemannScope.SquarefreeCoreCorrelation

open scoped ArithmeticFunction BigOperators
open MeasureTheory intervalIntegral

namespace RiemannScope

open RiemannScope.LiouvilleSquareDilation
open RiemannScope.DyadicPowerLiftPrimitiveCorrelation hiding canonicalPrimePowerDiagDtilde
open RiemannScope.SignedDilationArithmeticEnergy
open RiemannScope.MixedArithmeticCovariance
open RiemannScope.JointPrimeDilationSignedRemainder

/-! ### Core Definitions (`TASK-TC-065`) -/

/-- Complete Möbius-signed odd squarefree-core total scalar profile
    `U_Y(X) := divisibleCoreProfileSumS c_lam c_half T D0 1 X`. -/
noncomputable def coreTotalScalarProfileU (c_lam c_half : ℝ) (T D0 : ℕ) (X : ℝ) : ℝ :=
  divisibleCoreProfileSumS c_lam c_half T D0 1 X

/-- Complete Möbius-signed odd squarefree-core total prime-power feature vector
    `V_{Y, pk}(X) := divisibleCoreFeatureSumF T 1 pk X`. -/
noncomputable def coreTotalFeatureVectorV (T : ℕ) (pk : ℕ × ℕ) (X : ℝ) : ℝ :=
  divisibleCoreFeatureSumF T 1 pk X

/-- Odd squarefree-core scalar diagonal energy
    `J_A(Y) := ∑_{a ∈ C_odd(T)} ‖A_a‖_Y^2`. -/
noncomputable def coreScalarDiagJA (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ) : ℝ :=
  ∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (coreAdjustedProfileA c_lam c_half T D0 a)

/-- Odd squarefree-core feature diagonal energy
    `J_B(Y) := ∑_{a ∈ C_odd(T)} ∑_{pk} ‖B_{a, pk}‖_Y^2`. -/
noncomputable def coreFeatureDiagJB (T : ℕ) (Y : ℝ) : ℝ :=
  ∑ a ∈ oddSquarefreeCores T,
    ∑ pk ∈ primePowerPairsUpTo T,
      windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X)

/-- Distinct odd squarefree-core (`a ≠ c`) scalar Möbius-signed sum `S_core^{scal}(T, D0, Y)`. -/
noncomputable def coreDistinctScalarSumS (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ) : ℝ :=
  ∑ a ∈ oddSquarefreeCores T,
    ∑ c ∈ (oddSquarefreeCores T).erase a,
      (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
        windowPairing Y (coreAdjustedProfileA c_lam c_half T D0 a)
          (coreAdjustedProfileA c_lam c_half T D0 c)

/-- Damped squarefree-core scalar-feature defect
    `D_core(T, D0, Y) := S_core^{scal}(T, D0, Y) - 4 * ∑_{pk} ‖V_{pk}‖_Y^2`. -/
noncomputable def dampedCoreDefectD (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ) : ℝ :=
  coreDistinctScalarSumS c_lam c_half T D0 Y -
    4 * ∑ pk ∈ primePowerPairsUpTo T,
      windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV T pk X)

/-- Canonical-schedule (`T = canonicalCutoffT Y`, `D0 = ⌊log Y⌋`) damped core defect `D_core(Y)`. -/
noncomputable def canonicalDampedCoreDefectD (c_lam c_half : ℝ) (Y : ℝ) : ℝ :=
  dampedCoreDefectD c_lam c_half (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y

/-- Unweighted paired prime-power feature sum `P_{Ω_2}(X) := ∑_{pk} V_{pk}(X)`. -/
noncomputable def pairedPrimePowerSumP (T : ℕ) (X : ℝ) : ℝ :=
  ∑ pk ∈ primePowerPairsUpTo T, coreTotalFeatureVectorV T pk X

/-- Paired interior open-core oscillatory and second-shift observable `O_{Ω_2}(X)`. -/
noncomputable def pairedOpenCoreOscO (c_lam c_half : ℝ) (T D0 : ℕ) (X : ℝ) : ℝ :=
  (∑ n ∈ coveredInteriorStations 2 T,
    (openCoreSmoothCoeffS c_lam c_half T D0 n -
      (liouvilleLambda n : ℝ) * (Real.log (X / (n : ℝ))) ^ 2) *
      gaussianTermPhi n X) / (Real.log X) ^ 2

/-- Uncovered cutoff-fringe scalar observable
    `Φ_{fringe}(X) := ∑_{n ∈ Φ_2(T)} λ(n) ψ_n(X)`. -/
noncomputable def pairedCutoffFringeScalarPhi (c_lam c_half : ℝ) (T D0 : ℕ) (X : ℝ) : ℝ :=
  ∑ n ∈ uncoveredCutoffStripStations 2 T,
    (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X

/-- Full `[1, T]`-cutoff prime-power feature vector
    `G_{T, pk}(X) := ∑_{1 ≤ n ≤ T} λ(n) g_{n, pk}(X)`. -/
noncomputable def fullFeatureVectorG (T : ℕ) (pk : ℕ × ℕ) (X : ℝ) : ℝ :=
  ∑ n ∈ Finset.Icc 1 T, (liouvilleLambda n : ℝ) * stationPrimePowerFeatureG n pk X

/-- Uncovered cutoff-fringe prime-power feature vector
    `G_{Φ_2, pk}(X) := ∑_{n ∈ Φ_2(T)} λ(n) g_{n, pk}(X)`. -/
noncomputable def fringeFeatureVectorG (T : ℕ) (pk : ℕ × ℕ) (X : ℝ) : ℝ :=
  ∑ n ∈ uncoveredCutoffStripStations 2 T,
    (liouvilleLambda n : ℝ) * stationPrimePowerFeatureG n pk X

/-- Pointwise weighted prime-power synthesis operator
    `(L_w v)(X) := ∑_{pk ∈ primePowerPairsUpTo T} w(pk, X) * v(pk, X)`. -/
noncomputable def pointwiseSynthesisOp (T : ℕ) (w : ℕ × ℕ → ℝ → ℝ)
    (v : ℕ × ℕ → ℝ → ℝ) (X : ℝ) : ℝ :=
  ∑ pk ∈ primePowerPairsUpTo T, w pk X * v pk X

/-- Active prime-power channels dividing at least one paired interior station in `Ω_2(T)`. -/
def activePairedPrimePowers (T : ℕ) : Finset (ℕ × ℕ) :=
  (primePowerPairsUpTo T).filter (fun pk => ∃ n ∈ coveredInteriorStations 2 T, pk.1 ^ pk.2 ∣ n)

/-- Large-prime-power feature slice `V_{> M, pk}(X) := 1_{M < p^k} * V_{pk}(X)`. -/
noncomputable def splitFeatureHighV (T M : ℕ) (pk : ℕ × ℕ) (X : ℝ) : ℝ :=
  if M < pk.1 ^ pk.2 then coreTotalFeatureVectorV T pk X else 0

/-- Small-prime-power feature slice `V_{≤ M, pk}(X) := 1_{p^k ≤ M} * V_{pk}(X)`. -/
noncomputable def splitFeatureLowV (T M : ℕ) (pk : ℕ × ℕ) (X : ℝ) : ℝ :=
  if pk.1 ^ pk.2 ≤ M then coreTotalFeatureVectorV T pk X else 0

/-- Finite odd-prime Euler valuation-toggle multiplier
    `M_S(z) := ∏_{q ∈ S} (1 + q^(-z)) / (1 - q^(-z))`. -/
noncomputable def finiteEulerMultiplierM (S : Finset ℕ) (z : ℂ) : ℂ :=
  ∏ q ∈ S, (1 + (q : ℂ) ^ (-z)) / (1 - (q : ℂ) ^ (-z))

open scoped Classical

/-! ### Shared Continuity, Window Algebra, and Elementary Bounds -/

private theorem tau_gt_one_and_lt_eight_tc065_aux :
    (1 : ℝ) < RiemannScope.tau ∧ RiemannScope.tau < 8 := by
  have hC := (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2
  exact ⟨by linarith [hC.1], by linarith [hC.2.1]⟩

private theorem uIcc_tau_props_tc065_aux {Y : ℝ} (hY2 : 2 ≤ Y) :
    Y ≤ RiemannScope.tau * Y ∧
      ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
        2 ≤ X ∧ 0 < X ∧ 0 < Real.log X ∧ Real.log X ≠ 0 ∧ (Real.log X) ^ 2 ≠ 0 := by
  have htau := tau_gt_one_and_lt_eight_tc065_aux.1
  have hle : Y ≤ RiemannScope.tau * Y := by nlinarith
  refine ⟨hle, ?_⟩
  intro X hX
  rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX
  have hX2 : 2 ≤ X := le_trans hY2 hX.1
  have hX0 : 0 < X := by linarith
  have hlog : 0 < Real.log X := Real.log_pos (by linarith)
  exact ⟨hX2, hX0, hlog, ne_of_gt hlog, pow_ne_zero 2 (ne_of_gt hlog)⟩

private theorem uIcc_param_props_tc065_aux {Y w0 : ℝ} (hY2 : 2 ≤ Y) (hw0 : 1 < w0) :
    Y ≤ w0 * Y ∧
      ∀ X ∈ Set.uIcc Y (w0 * Y),
        2 ≤ X ∧ 0 < X ∧ 0 < Real.log X ∧ Real.log X ≠ 0 ∧ (Real.log X) ^ 2 ≠ 0 := by
  have hle : Y ≤ w0 * Y := by nlinarith
  refine ⟨hle, ?_⟩
  intro X hX
  rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX
  have hX2 : 2 ≤ X := le_trans hY2 hX.1
  have hX0 : 0 < X := by linarith
  have hlog : 0 < Real.log X := Real.log_pos (by linarith)
  exact ⟨hX2, hX0, hlog, ne_of_gt hlog, pow_ne_zero 2 (ne_of_gt hlog)⟩

private theorem continuousOn_core_objects_tc065_aux {Y w0 : ℝ} (hY2 : 2 ≤ Y) (hw0 : 1 < w0)
    (c_lam c_half : ℝ) (T D0 : ℕ) :
    (∀ n : ℕ, ContinuousOn (gaussianTermPhi n) (Set.uIcc Y (w0 * Y))) ∧
      (∀ n : ℕ, ContinuousOn (adjustedStationProfilePsi c_lam c_half T D0 n)
        (Set.uIcc Y (w0 * Y))) ∧
      (∀ (n : ℕ) (pk : ℕ × ℕ), ContinuousOn (stationPrimePowerFeatureG n pk)
        (Set.uIcc Y (w0 * Y))) ∧
      (∀ a : ℕ, ContinuousOn (coreAdjustedProfileA c_lam c_half T D0 a)
        (Set.uIcc Y (w0 * Y))) ∧
      (∀ (a : ℕ) (pk : ℕ × ℕ), ContinuousOn (coreFeatureVectorB a T pk)
        (Set.uIcc Y (w0 * Y))) ∧
      ContinuousOn (coreTotalScalarProfileU c_lam c_half T D0) (Set.uIcc Y (w0 * Y)) ∧
      (∀ pk : ℕ × ℕ, ContinuousOn (coreTotalFeatureVectorV T pk) (Set.uIcc Y (w0 * Y))) ∧
      ContinuousOn (pairedPrimePowerSumP T) (Set.uIcc Y (w0 * Y)) ∧
      ContinuousOn (pairedOpenCoreOscO c_lam c_half T D0) (Set.uIcc Y (w0 * Y)) ∧
      ContinuousOn (pairedCutoffFringeScalarPhi c_lam c_half T D0) (Set.uIcc Y (w0 * Y)) ∧
      (∀ pk : ℕ × ℕ, ContinuousOn (fullFeatureVectorG T pk) (Set.uIcc Y (w0 * Y))) ∧
      (∀ pk : ℕ × ℕ, ContinuousOn (fringeFeatureVectorG T pk) (Set.uIcc Y (w0 * Y))) := by
  obtain ⟨_, hprops⟩ := uIcc_param_props_tc065_aux hY2 hw0
  have hlog_c : ContinuousOn Real.log (Set.uIcc Y (w0 * Y)) :=
    ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1)
  have hphi : ∀ n : ℕ, ContinuousOn (gaussianTermPhi n) (Set.uIcc Y (w0 * Y)) := by
    intro n
    unfold gaussianTermPhi
    have hr : ContinuousOn (fun X : ℝ => X ^ (5 / 2 : ℝ)) (Set.uIcc Y (w0 * Y)) := by
      apply ContinuousOn.rpow_const continuousOn_id
      intro _ _; right; norm_num
    have he : Continuous (fun X : ℝ => (((n : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (n : ℝ) ^ 2))) := by
      continuity
    exact hr.mul he.continuousOn
  have hpsi : ∀ n : ℕ, ContinuousOn (adjustedStationProfilePsi c_lam c_half T D0 n)
      (Set.uIcc Y (w0 * Y)) := by
    intro n
    unfold adjustedStationProfilePsi
    exact (continuousOn_const.sub
      (continuousOn_const.div (hlog_c.pow 2) (fun X hX => (hprops X hX).2.2.2.2))).mul (hphi n)
  have hg : ∀ (n : ℕ) (pk : ℕ × ℕ), ContinuousOn (stationPrimePowerFeatureG n pk)
      (Set.uIcc Y (w0 * Y)) := by
    intro n pk
    unfold stationPrimePowerFeatureG
    by_cases hd : pk.1 ^ pk.2 ∣ n
    · simp only [hd, ↓reduceIte]
      exact (continuousOn_const.mul (hphi n)).div hlog_c (fun X hX => (hprops X hX).2.2.2.1)
    · simp only [hd, ↓reduceIte]
      exact continuousOn_const
  have hA : ∀ a : ℕ, ContinuousOn (coreAdjustedProfileA c_lam c_half T D0 a)
      (Set.uIcc Y (w0 * Y)) := by
    intro a
    unfold coreAdjustedProfileA oddChainAdjustedProfileUcal stationAdjustedDiffU
    exact continuousOn_finset_sum _ (fun b _ =>
      continuousOn_finset_sum _ (fun j _ => (hpsi _).sub (hpsi _)))
  have hB : ∀ (a : ℕ) (pk : ℕ × ℕ), ContinuousOn (coreFeatureVectorB a T pk)
      (Set.uIcc Y (w0 * Y)) := by
    intro a pk
    unfold coreFeatureVectorB oddChainFeatureVectorVcal stationFeatureDiffV
    exact continuousOn_finset_sum _ (fun b _ =>
      continuousOn_finset_sum _ (fun j _ => (hg _ pk).sub (hg _ pk)))
  have hU : ContinuousOn (coreTotalScalarProfileU c_lam c_half T D0) (Set.uIcc Y (w0 * Y)) := by
    unfold coreTotalScalarProfileU divisibleCoreProfileSumS
    exact continuousOn_finset_sum _ (fun a _ => continuousOn_const.mul (hA a))
  have hV : ∀ pk : ℕ × ℕ, ContinuousOn (coreTotalFeatureVectorV T pk) (Set.uIcc Y (w0 * Y)) := by
    intro pk
    unfold coreTotalFeatureVectorV divisibleCoreFeatureSumF
    exact continuousOn_finset_sum _ (fun a _ => continuousOn_const.mul (hB a pk))
  have hP : ContinuousOn (pairedPrimePowerSumP T) (Set.uIcc Y (w0 * Y)) := by
    unfold pairedPrimePowerSumP
    exact continuousOn_finset_sum _ (fun pk _ => hV pk)
  have hO : ContinuousOn (pairedOpenCoreOscO c_lam c_half T D0) (Set.uIcc Y (w0 * Y)) := by
    unfold pairedOpenCoreOscO
    refine (continuousOn_finset_sum _ ?_).div (hlog_c.pow 2) (fun X hX => (hprops X hX).2.2.2.2)
    intro n hn
    have hn1 : 1 ≤ n := by
      unfold coveredInteriorStations at hn
      simp only [Finset.mem_union, Finset.mem_image, primeInteriorTruncatedAnchors,
        primeEvenValuationAnchors, Finset.mem_filter, Finset.mem_Icc] at hn
      rcases hn with ⟨⟨⟨h1, _⟩, _⟩, _⟩ | ⟨m, ⟨⟨⟨h1, _⟩, _⟩, _⟩, rfl⟩
      · exact h1
      · omega
    have hn_ne : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
    have hlog_div : ContinuousOn (fun X => Real.log (X / (n : ℝ))) (Set.uIcc Y (w0 * Y)) :=
      ContinuousOn.log (continuousOn_id.div_const (n : ℝ))
        (fun X hX => div_ne_zero (ne_of_gt (hprops X hX).2.1) hn_ne)
    exact (continuousOn_const.sub (continuousOn_const.mul (hlog_div.pow 2))).mul (hphi n)
  have hPhi : ContinuousOn (pairedCutoffFringeScalarPhi c_lam c_half T D0) (Set.uIcc Y (w0 * Y)) := by
    unfold pairedCutoffFringeScalarPhi
    exact continuousOn_finset_sum _ (fun n _ => continuousOn_const.mul (hpsi n))
  have hGfull : ∀ pk : ℕ × ℕ, ContinuousOn (fullFeatureVectorG T pk) (Set.uIcc Y (w0 * Y)) := by
    intro pk
    unfold fullFeatureVectorG
    exact continuousOn_finset_sum _ (fun n _ => continuousOn_const.mul (hg n pk))
  have hGfr : ∀ pk : ℕ × ℕ, ContinuousOn (fringeFeatureVectorG T pk) (Set.uIcc Y (w0 * Y)) := by
    intro pk
    unfold fringeFeatureVectorG
    exact continuousOn_finset_sum _ (fun n _ => continuousOn_const.mul (hg n pk))
  exact ⟨hphi, hpsi, hg, hA, hB, hU, hV, hP, hO, hPhi, hGfull, hGfr⟩

private theorem windowEnergyNormSq_nonneg_tc065_aux {Y : ℝ} (hY0 : 0 < Y) (f : ℝ → ℝ) :
    0 ≤ windowEnergyNormSq Y f := by
  have htau := tau_gt_one_and_lt_eight_tc065_aux.1
  have hle : Y ≤ RiemannScope.tau * Y := by nlinarith
  unfold windowEnergyNormSq windowPairing
  apply intervalIntegral.integral_nonneg hle
  intro X hX
  exact div_nonneg (mul_self_nonneg _) (by linarith [hX.1])

private theorem windowPairing_finset_bilinear_tc065_aux {α β : Type*}
    {Y : ℝ} (hY0 : 0 < Y) (S : Finset α) (W : Finset β)
    (f : α → ℝ → ℝ) (g : β → ℝ → ℝ) (w1 : α → ℝ) (w2 : β → ℝ)
    (hf : ∀ i ∈ S, ContinuousOn (f i) (Set.uIcc Y (RiemannScope.tau * Y)))
    (hg : ∀ j ∈ W, ContinuousOn (g j) (Set.uIcc Y (RiemannScope.tau * Y))) :
    windowPairing Y (fun X => ∑ i ∈ S, w1 i * f i X) (fun X => ∑ j ∈ W, w2 j * g j X) =
      ∑ i ∈ S, ∑ j ∈ W, w1 i * w2 j * windowPairing Y (f i) (g j) := by
  have htau := tau_gt_one_and_lt_eight_tc065_aux.1
  have hle : Y ≤ RiemannScope.tau * Y := by nlinarith
  have hpos : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), 0 < X := by
    intro X hX; rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX; linarith
  have h_int : ∀ i ∈ S, ∀ j ∈ W,
      IntervalIntegrable (fun X => (w1 i * w2 j) * (f i X * g j X / X))
        volume Y (RiemannScope.tau * Y) := by
    intro i hi j hj
    exact (continuousOn_const.mul
      (((hf i hi).mul (hg j hj)).div continuousOn_id
        (fun X hX => ne_of_gt (hpos X hX)))).intervalIntegrable
  unfold windowPairing
  have h_pt :
      (fun X => (∑ i ∈ S, w1 i * f i X) * (∑ j ∈ W, w2 j * g j X) / X) =
        fun X => ∑ i ∈ S, ∑ j ∈ W, (w1 i * w2 j) * (f i X * g j X / X) := by
    ext X
    rw [Finset.sum_mul_sum, Finset.sum_div]
    apply Finset.sum_congr rfl
    intro i _
    rw [Finset.sum_div]
    apply Finset.sum_congr rfl
    intro j _; ring
  rw [h_pt, intervalIntegral.integral_finset_sum]
  · apply Finset.sum_congr rfl
    intro i hi
    rw [intervalIntegral.integral_finset_sum]
    · apply Finset.sum_congr rfl
      intro j _
      rw [intervalIntegral.integral_const_mul]
    · intro j hj
      exact h_int i hi j hj
  · intro i hi
    have h_sum2 :
        (fun X => ∑ j ∈ W, (w1 i * w2 j) * (f i X * g j X / X)) =
          ∑ j ∈ W, fun X => (w1 i * w2 j) * (f i X * g j X / X) := by
      ext X; simp [Finset.sum_apply]
    rw [h_sum2]
    exact IntervalIntegrable.sum W (fun j hj => h_int i hi j hj)

private theorem windowEnergyNormSq_add_eq_tc065_aux {Y : ℝ} (hY0 : 0 < Y)
    {f g : ℝ → ℝ}
    (hf : ContinuousOn f (Set.uIcc Y (RiemannScope.tau * Y)))
    (hg : ContinuousOn g (Set.uIcc Y (RiemannScope.tau * Y))) :
    windowEnergyNormSq Y (fun X => f X + g X) =
      windowEnergyNormSq Y f + 2 * windowPairing Y f g + windowEnergyNormSq Y g := by
  have htau := tau_gt_one_and_lt_eight_tc065_aux.1
  exact ((gaussian_window_majorant_and_local_frequency_split_tc060).2.1 hY0 htau hf hg).1

private theorem intervalIntegral_inv_param_tc065_aux {Y w0 : ℝ} (hY0 : 0 < Y) (hw0 : 1 < w0) :
    (∫ X in Y..(w0 * Y), (1 : ℝ) / X) = Real.log w0 := by
  have hle : Y ≤ w0 * Y := by nlinarith
  have hpos : ∀ X ∈ Set.uIcc Y (w0 * Y), 0 < X := by
    intro X hX
    rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX
    linarith
  have hderiv : ∀ X ∈ Set.uIcc Y (w0 * Y), HasDerivAt Real.log ((1 : ℝ) / X) X := by
    intro X hX
    rw [one_div]
    exact Real.hasDerivAt_log (ne_of_gt (hpos X hX))
  have hint : IntervalIntegrable (fun X => (1 : ℝ) / X) volume Y (w0 * Y) :=
    (continuousOn_const.div continuousOn_id (fun X hX => ne_of_gt (hpos X hX))).intervalIntegrable
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hint,
    Real.log_mul (ne_of_gt (by linarith)) (ne_of_gt hY0)]
  ring

private theorem liouvilleLambda_props_tc065_aux :
    (liouvilleLambda 1 : ℝ) = 1 ∧
      (∀ {n : ℕ}, 1 ≤ n → (liouvilleLambda n : ℝ) * (liouvilleLambda n : ℝ) = 1 ∧
        |(liouvilleLambda n : ℝ)| = 1) ∧
      (∀ {a b : ℕ}, 1 ≤ a → 1 ≤ b →
        (liouvilleLambda (a * b) : ℝ) = (liouvilleLambda a : ℝ) * (liouvilleLambda b : ℝ)) ∧
      (∀ {p : ℕ}, p.Prime → (liouvilleLambda p : ℝ) = -1) := by
  have h1 : (liouvilleLambda 1 : ℝ) = 1 := by
    simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
  have hsq : ∀ {n : ℕ}, 1 ≤ n →
      (liouvilleLambda n : ℝ) * (liouvilleLambda n : ℝ) = 1 ∧ |(liouvilleLambda n : ℝ)| = 1 := by
    intro n hn
    have hn_ne : n ≠ 0 := by omega
    have h_int : liouvilleLambda n * liouvilleLambda n = 1 := by
      simp only [liouvilleLambda, hn_ne, ↓reduceIte, liouvilleSignFromOmega]
      rw [← pow_add, show natOmega n + natOmega n = 2 * natOmega n by omega, pow_mul]
      norm_num
    have h_r : (liouvilleLambda n : ℝ) * (liouvilleLambda n : ℝ) = 1 := by exact_mod_cast h_int
    have habs_sq : |(liouvilleLambda n : ℝ)| ^ 2 = 1 := by rw [sq_abs, sq]; exact h_r
    exact ⟨h_r, by nlinarith [abs_nonneg (liouvilleLambda n : ℝ)]⟩
  have hmul : ∀ {a b : ℕ}, 1 ≤ a → 1 ≤ b →
      (liouvilleLambda (a * b) : ℝ) = (liouvilleLambda a : ℝ) * (liouvilleLambda b : ℝ) := by
    intro a b ha hb
    have ha_ne : a ≠ 0 := by omega
    have hb_ne : b ≠ 0 := by omega
    have hab_ne : a * b ≠ 0 := mul_ne_zero ha_ne hb_ne
    have h_int : liouvilleLambda (a * b) = liouvilleLambda a * liouvilleLambda b := by
      simp [liouvilleLambda, ha_ne, hb_ne, hab_ne, natOmega,
        ArithmeticFunction.cardFactors_mul ha_ne hb_ne, liouvilleSignFromOmega, pow_add]
    exact_mod_cast h_int
  have hpr : ∀ {p : ℕ}, p.Prime → (liouvilleLambda p : ℝ) = -1 := by
    intro p hp
    have hop : natOmega p = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr hp
    simp [liouvilleLambda, hp.ne_zero, hop, liouvilleSignFromOmega]
  exact ⟨h1, hsq, hmul, hpr⟩

/-! ### Section 1: Damped Core Defect Identities and Closure Equivalence (`TASK-TC-065` §2) -/

private theorem dampedCoreDefectD_identities_tc065_aux {Y : ℝ} (hY2 : 2 ≤ Y)
    (c_lam c_half : ℝ) (T D0 : ℕ) :
    dampedCoreDefectD c_lam c_half T D0 Y =
        windowEnergyNormSq Y (coreTotalScalarProfileU c_lam c_half T D0) -
          4 * (∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV T pk X)) -
          coreScalarDiagJA c_lam c_half T D0 Y ∧
      distinctSquarefreeCoreSumS c_lam c_half T D0 Y =
        dampedCoreDefectD c_lam c_half T D0 Y + 4 * coreFeatureDiagJB T Y ∧
      (0 ≤ coreScalarDiagJA c_lam c_half T D0 Y ∧ 0 ≤ coreFeatureDiagJB T Y) := by
  have hY0 : 0 < Y := by linarith
  have htau := tau_gt_one_and_lt_eight_tc065_aux.1
  obtain ⟨_, _, _, hA_c, hB_c, _, _, _, _, _, _, _⟩ :=
    continuousOn_core_objects_tc065_aux hY2 htau c_lam c_half T D0
  have h_filt1 : (oddSquarefreeCores T).filter (fun a => 1 ∣ a) = oddSquarefreeCores T := by
    ext a; simp
  have hU_eq :
      coreTotalScalarProfileU c_lam c_half T D0 =
        fun X => ∑ a ∈ oddSquarefreeCores T,
          (ArithmeticFunction.moebius a : ℝ) * coreAdjustedProfileA c_lam c_half T D0 a X := by
    ext X
    unfold coreTotalScalarProfileU divisibleCoreProfileSumS
    rw [h_filt1]
  have hV_eq :
      ∀ pk : ℕ × ℕ,
        coreTotalFeatureVectorV T pk =
          fun X => ∑ a ∈ oddSquarefreeCores T,
            (ArithmeticFunction.moebius a : ℝ) * coreFeatureVectorB a T pk X := by
    intro pk; ext X
    unfold coreTotalFeatureVectorV divisibleCoreFeatureSumF
    rw [h_filt1]
  have h_mu_sq : ∀ a ∈ oddSquarefreeCores T,
      (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius a : ℝ) = 1 := by
    intro a ha
    have ha_sf : Squarefree a := (Finset.mem_filter.mp ha).2.2.1
    have hsq := ((exact_odd_squarefree_core_bijection_and_complete_kernel_split_tc064).1.2 ha_sf
      (le_refl 1)).2
    rwa [sq] at hsq
  have hU_norm :
      windowEnergyNormSq Y (coreTotalScalarProfileU c_lam c_half T D0) =
        coreScalarDiagJA c_lam c_half T D0 Y + coreDistinctScalarSumS c_lam c_half T D0 Y := by
    unfold windowEnergyNormSq
    rw [hU_eq, windowPairing_finset_bilinear_tc065_aux hY0 (oddSquarefreeCores T)
      (oddSquarefreeCores T)
      (fun a => coreAdjustedProfileA c_lam c_half T D0 a)
      (fun c => coreAdjustedProfileA c_lam c_half T D0 c)
      (fun a => (ArithmeticFunction.moebius a : ℝ))
      (fun c => (ArithmeticFunction.moebius c : ℝ))
      (fun a _ => hA_c a) (fun c _ => hA_c c)]
    have h_split :
        ∀ a ∈ oddSquarefreeCores T,
          (∑ c ∈ oddSquarefreeCores T,
              (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                windowPairing Y (coreAdjustedProfileA c_lam c_half T D0 a)
                  (coreAdjustedProfileA c_lam c_half T D0 c)) =
            windowEnergyNormSq Y (coreAdjustedProfileA c_lam c_half T D0 a) +
              ∑ c ∈ (oddSquarefreeCores T).erase a,
                (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                  windowPairing Y (coreAdjustedProfileA c_lam c_half T D0 a)
                    (coreAdjustedProfileA c_lam c_half T D0 c) := by
      intro a ha
      rw [← Finset.add_sum_erase _ _ ha, h_mu_sq a ha, one_mul]
      rfl
    rw [Finset.sum_congr rfl h_split, Finset.sum_add_distrib]
    rfl
  have hV_norm_each :
      ∀ pk ∈ primePowerPairsUpTo T,
        windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV T pk X) =
          (∑ a ∈ oddSquarefreeCores T,
              windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X)) +
            ∑ a ∈ oddSquarefreeCores T, ∑ c ∈ (oddSquarefreeCores T).erase a,
              (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                windowPairing Y (fun X => coreFeatureVectorB a T pk X)
                  (fun X => coreFeatureVectorB c T pk X) := by
    intro pk _
    unfold windowEnergyNormSq
    change windowPairing Y (coreTotalFeatureVectorV T pk) (coreTotalFeatureVectorV T pk) = _
    rw [hV_eq pk, windowPairing_finset_bilinear_tc065_aux hY0 (oddSquarefreeCores T)
      (oddSquarefreeCores T)
      (fun a => coreFeatureVectorB a T pk) (fun c => coreFeatureVectorB c T pk)
      (fun a => (ArithmeticFunction.moebius a : ℝ))
      (fun c => (ArithmeticFunction.moebius c : ℝ))
      (fun a _ => hB_c a pk) (fun c _ => hB_c c pk)]
    have h_split :
        ∀ a ∈ oddSquarefreeCores T,
          (∑ c ∈ oddSquarefreeCores T,
              (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                windowPairing Y (coreFeatureVectorB a T pk) (coreFeatureVectorB c T pk)) =
            windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X) +
              ∑ c ∈ (oddSquarefreeCores T).erase a,
                (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                  windowPairing Y (fun X => coreFeatureVectorB a T pk X)
                    (fun X => coreFeatureVectorB c T pk X) := by
      intro a ha
      rw [← Finset.add_sum_erase _ _ ha, h_mu_sq a ha, one_mul]
      rfl
    rw [Finset.sum_congr rfl h_split, Finset.sum_add_distrib]
    rfl
  have hV_sum :
      (∑ pk ∈ primePowerPairsUpTo T,
          windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV T pk X)) =
        coreFeatureDiagJB T Y +
          ∑ a ∈ oddSquarefreeCores T, ∑ c ∈ (oddSquarefreeCores T).erase a,
            (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
              ∑ pk ∈ primePowerPairsUpTo T,
                windowPairing Y (fun X => coreFeatureVectorB a T pk X)
                  (fun X => coreFeatureVectorB c T pk X) := by
    rw [Finset.sum_congr rfl hV_norm_each, Finset.sum_add_distrib]
    congr 1
    · unfold coreFeatureDiagJB; exact Finset.sum_comm
    · trans (∑ a ∈ oddSquarefreeCores T, ∑ pk ∈ primePowerPairsUpTo T,
        ∑ c ∈ (oddSquarefreeCores T).erase a,
          (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
            windowPairing Y (fun X => coreFeatureVectorB a T pk X)
              (fun X => coreFeatureVectorB c T pk X))
      · exact Finset.sum_comm
      · apply Finset.sum_congr rfl
        intro a _
        rw [Finset.sum_comm]
        apply Finset.sum_congr rfl
        intro c _
        rw [Finset.mul_sum]
  have h_dist_eq :
      distinctSquarefreeCoreSumS c_lam c_half T D0 Y =
        coreDistinctScalarSumS c_lam c_half T D0 Y -
          4 * ∑ a ∈ oddSquarefreeCores T, ∑ c ∈ (oddSquarefreeCores T).erase a,
            (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
              ∑ pk ∈ primePowerPairsUpTo T,
                windowPairing Y (fun X => coreFeatureVectorB a T pk X)
                  (fun X => coreFeatureVectorB c T pk X) := by
    unfold distinctSquarefreeCoreSumS completeCorePairKernelMcal coreDistinctScalarSumS
    have h_rew :
        ∀ a ∈ oddSquarefreeCores T,
          (∑ c ∈ (oddSquarefreeCores T).erase a,
              (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                (windowPairing Y (coreAdjustedProfileA c_lam c_half T D0 a)
                    (coreAdjustedProfileA c_lam c_half T D0 c) -
                  4 * ∑ pk ∈ primePowerPairsUpTo T,
                    windowPairing Y (fun X => coreFeatureVectorB a T pk X)
                      (fun X => coreFeatureVectorB c T pk X))) =
            (∑ c ∈ (oddSquarefreeCores T).erase a,
                (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                  windowPairing Y (coreAdjustedProfileA c_lam c_half T D0 a)
                    (coreAdjustedProfileA c_lam c_half T D0 c)) -
              4 * ∑ c ∈ (oddSquarefreeCores T).erase a,
                (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                  ∑ pk ∈ primePowerPairsUpTo T,
                    windowPairing Y (fun X => coreFeatureVectorB a T pk X)
                      (fun X => coreFeatureVectorB c T pk X) := by
      intro a _
      rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro c _; ring
    rw [Finset.sum_congr rfl h_rew, Finset.sum_sub_distrib, ← Finset.mul_sum]
  have hJA_nn : 0 ≤ coreScalarDiagJA c_lam c_half T D0 Y :=
    Finset.sum_nonneg (fun a _ => windowEnergyNormSq_nonneg_tc065_aux hY0 _)
  have hJB_nn : 0 ≤ coreFeatureDiagJB T Y :=
    Finset.sum_nonneg (fun a _ => Finset.sum_nonneg (fun pk _ =>
      windowEnergyNormSq_nonneg_tc065_aux hY0 _))
  unfold dampedCoreDefectD
  refine ⟨by linarith [hU_norm], by linarith [h_dist_eq, hV_sum], hJA_nn, hJB_nn⟩

/-- **Theorem 1 (`TASK-TC-065` §2, Damped Squarefree-Core Defect Identities, Diagonal Nonnegativity, Uniform `O(1 + log Y)` Core-Diagonal Bound, and Two-Way `MixedCovarianceClosureHypothesis` Equivalence)**:
    1. *Exact damped-defect identities and diagonal nonnegativity (`2 ≤ Y`, `c_lam c_half : ℝ`, `T D0 : ℕ`)*:
       - `dampedCoreDefectD c_lam c_half T D0 Y = ‖U_Y‖_Y^2 - 4 * ∑_{pk} ‖V_{pk}‖_Y^2 - J_A`;
       - `distinctSquarefreeCoreSumS c_lam c_half T D0 Y = dampedCoreDefectD c_lam c_half T D0 Y + 4 * J_B`;
       - `0 ≤ coreScalarDiagJA c_lam c_half T D0 Y ∧ 0 ≤ coreFeatureDiagJB T Y`;
    2. *Canonical uniform core-diagonal bound and exact two-way closure equivalence*:
       For every `c_lam c_half : ℝ`, there exists `C_core ≥ 0` with
       `J_A(Y) + J_B(Y) ≤ C_core * (1 + Real.log Y)` for all real `Y ≥ 2`, and
       `MixedCovarianceClosureHypothesis (canonicalDampedCoreDefectD c_lam c_half) canonicalPrimePowerDiagDtilde ↔ MixedCovarianceClosureHypothesis (canonicalDistinctSquarefreeCoreSumS c_lam c_half) canonicalPrimePowerDiagDtilde`. -/
theorem damped_core_defect_and_closure_equivalence_tc065 :
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ (c_lam c_half : ℝ) (T D0 : ℕ),
      dampedCoreDefectD c_lam c_half T D0 Y =
          windowEnergyNormSq Y (coreTotalScalarProfileU c_lam c_half T D0) -
            4 * (∑ pk ∈ primePowerPairsUpTo T,
              windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV T pk X)) -
            coreScalarDiagJA c_lam c_half T D0 Y ∧
        distinctSquarefreeCoreSumS c_lam c_half T D0 Y =
          dampedCoreDefectD c_lam c_half T D0 Y + 4 * coreFeatureDiagJB T Y ∧
        (0 ≤ coreScalarDiagJA c_lam c_half T D0 Y ∧ 0 ≤ coreFeatureDiagJB T Y)) ∧
    (∀ (c_lam c_half : ℝ),
      ∃ C_core : ℝ, 0 ≤ C_core ∧
        (∀ {Y : ℝ}, 2 ≤ Y →
          coreScalarDiagJA c_lam c_half (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y +
              coreFeatureDiagJB (canonicalCutoffT Y) Y ≤
            C_core * (1 + Real.log Y)) ∧
        (MixedCovarianceClosureHypothesis (canonicalDampedCoreDefectD c_lam c_half)
            canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis (canonicalDistinctSquarefreeCoreSumS c_lam c_half)
            canonicalPrimePowerDiagDtilde)) := by
  refine ⟨fun {_} hY2 c_lam c_half T D0 =>
      dampedCoreDefectD_identities_tc065_aux hY2 c_lam c_half T D0, ?_⟩
  intro c_lam c_half
  obtain ⟨C_core, _, hC_nn, _, h_tc064_bd⟩ :=
    (uniform_same_core_hilbert_bound_and_closure_transfer_tc064).2.2.2.1.2 c_lam c_half
  have h_diag_sum :
      ∀ {Y : ℝ}, 2 ≤ Y →
        coreScalarDiagJA c_lam c_half (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y +
            coreFeatureDiagJB (canonicalCutoffT Y) Y ≤
          C_core * (1 + Real.log Y) := by
    intro Y hY2
    have h1 := (h_tc064_bd hY2).1
    rw [Finset.sum_add_distrib] at h1
    exact h1
  refine ⟨C_core, hC_nn, h_diag_sum, ?_⟩
  constructor
  · intro hD η hη
    obtain ⟨a_eta, b_eta, κ_eta, Y_eta, ha, hb, hκ_pos, hκ_le2, hYe, hD_bd⟩ := hD η hη
    obtain ⟨a_log, ha_log_nn, h_log_rpow⟩ :=
      (uniform_same_chain_hilbert_bound_and_closure_transfer_tc063).2.2.2.2.1
        (show 0 ≤ 4 * C_core by linarith) hη
    refine ⟨a_eta + a_log, b_eta, κ_eta, Y_eta,
      add_nonneg ha ha_log_nn, hb, hκ_pos, hκ_le2, hYe, ?_⟩
    intro Y hYYe
    have hY2 : 2 ≤ Y := le_trans hYe hYYe
    have hid := dampedCoreDefectD_identities_tc065_aux hY2 c_lam c_half
      (canonicalCutoffT Y) (Nat.floor (Real.log Y))
    have hJA_nn := hid.2.2.1
    have hJB_le : coreFeatureDiagJB (canonicalCutoffT Y) Y ≤ C_core * (1 + Real.log Y) := by
      linarith [h_diag_sum hY2, hJA_nn]
    have h_log_Y := h_log_rpow Y hY2
    have hD_Y := hD_bd Y hYYe
    unfold canonicalDistinctSquarefreeCoreSumS
    rw [hid.2.1]
    change dampedCoreDefectD c_lam c_half (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y +
        4 * coreFeatureDiagJB (canonicalCutoffT Y) Y ≤ _
    unfold canonicalDampedCoreDefectD at hD_Y
    linarith [show (a_eta + a_log) * Y ^ η = a_eta * Y ^ η + a_log * Y ^ η by ring]
  · intro hS η hη
    obtain ⟨a_eta, b_eta, κ_eta, Y_eta, ha, hb, hκ_pos, hκ_le2, hYe, hS_bd⟩ := hS η hη
    refine ⟨a_eta, b_eta, κ_eta, Y_eta, ha, hb, hκ_pos, hκ_le2, hYe, ?_⟩
    intro Y hYYe
    have hY2 : 2 ≤ Y := le_trans hYe hYYe
    have hid := dampedCoreDefectD_identities_tc065_aux hY2 c_lam c_half
      (canonicalCutoffT Y) (Nat.floor (Real.log Y))
    have hS_Y := hS_bd Y hYYe
    unfold canonicalDistinctSquarefreeCoreSumS at hS_Y
    unfold canonicalDampedCoreDefectD
    linarith [hid.2.1, hid.2.2.2, hS_Y]

/-! ### Section 2: Paired-Station Partition, Odd Prime-Power Vanishing, Divisor Synthesis, and Telescoping (`TASK-TC-065` §3) -/

private theorem coveredInteriorStations_partition_and_char_tc065_aux (T : ℕ) :
    (Disjoint (coveredInteriorStations 2 T) (uncoveredCutoffStripStations 2 T) ∧
        coveredInteriorStations 2 T ∪ uncoveredCutoffStripStations 2 T = Finset.Icc 1 T) ∧
      (∀ n ∈ Finset.Icc 1 T,
        n ∈ coveredInteriorStations 2 T ↔ (Odd (n.factorization 2) ∨ 2 * n ≤ T)) ∧
      (∀ n ∈ Finset.Icc 1 T,
        n ∈ uncoveredCutoffStripStations 2 T ↔ (Even (n.factorization 2) ∧ T < 2 * n)) ∧
      (∀ f : ℕ → ℝ,
        (∑ n ∈ coveredInteriorStations 2 T, f n) =
          ∑ m ∈ primeInteriorTruncatedAnchors 2 T, (f m + f (2 * m))) ∧
      ((∑ n ∈ coveredInteriorStations 2 T, (liouvilleLambda n : ℝ)) = 0 ∧
        (∑ n ∈ uncoveredCutoffStripStations 2 T, (liouvilleLambda n : ℝ)) =
          ∑ n ∈ Finset.Icc 1 T, (liouvilleLambda n : ℝ)) := by
  have h_sub : coveredInteriorStations 2 T ⊆ Finset.Icc 1 T := by
    intro n hn
    simp only [coveredInteriorStations, Finset.mem_union, Finset.mem_image,
      primeInteriorTruncatedAnchors, primeEvenValuationAnchors, Finset.mem_filter,
      Finset.mem_Icc] at hn ⊢
    rcases hn with ⟨⟨⟨hn1, _⟩, _⟩, h2nT⟩ | ⟨m, ⟨⟨⟨hm1, _⟩, _⟩, h2mT⟩, rfl⟩
    · exact ⟨hn1, by omega⟩
    · exact ⟨by omega, h2mT⟩
  have h_disj : Disjoint (coveredInteriorStations 2 T) (uncoveredCutoffStripStations 2 T) := by
    unfold uncoveredCutoffStripStations
    exact Finset.disjoint_sdiff
  have h_union : coveredInteriorStations 2 T ∪ uncoveredCutoffStripStations 2 T = Finset.Icc 1 T := by
    unfold uncoveredCutoffStripStations
    exact Finset.union_sdiff_of_subset h_sub
  have h_char_cov :
      ∀ n ∈ Finset.Icc 1 T,
        n ∈ coveredInteriorStations 2 T ↔ (Odd (n.factorization 2) ∨ 2 * n ≤ T) := by
    intro n hn
    obtain ⟨hn1, hnT⟩ := Finset.mem_Icc.mp hn
    constructor
    · intro hcov
      simp only [coveredInteriorStations, Finset.mem_union, Finset.mem_image,
        primeInteriorTruncatedAnchors, primeEvenValuationAnchors, Finset.mem_filter,
        Finset.mem_Icc] at hcov
      rcases hcov with ⟨⟨_, _⟩, h2nT⟩ | ⟨m, ⟨⟨⟨hm1, _⟩, hm_ev⟩, _⟩, rfl⟩
      · exact Or.inr h2nT
      · left
        have hm_ne : m ≠ 0 := by omega
        rw [Nat.factorization_mul (by decide) hm_ne, Finsupp.add_apply,
          Nat.Prime.factorization Nat.prime_two, Finsupp.single_eq_same]
        rcases hm_ev with ⟨k, hk⟩
        exact ⟨k, by omega⟩
    · rintro (h_odd | h2nT)
      · have h2_dvd : 2 ∣ n := by
          by_contra hnd
          rw [Nat.factorization_eq_zero_of_not_dvd hnd] at h_odd
          exact (Nat.odd_iff_not_even.mp h_odd) even_zero
        obtain ⟨m, rfl⟩ := h2_dvd
        have hm1 : 1 ≤ m := by omega
        have hm_ne : m ≠ 0 := by omega
        have hm_ev : Even (m.factorization 2) := by
          rw [Nat.factorization_mul (by decide) hm_ne, Finsupp.add_apply,
            Nat.Prime.factorization Nat.prime_two, Finsupp.single_eq_same] at h_odd
          rcases h_odd with ⟨k, hk⟩
          exact ⟨k, by omega⟩
        have hm_in : m ∈ primeInteriorTruncatedAnchors 2 T := by
          simp only [primeInteriorTruncatedAnchors, primeEvenValuationAnchors, Finset.mem_filter,
            Finset.mem_Icc]
          exact ⟨⟨⟨hm1, by omega⟩, hm_ev⟩, hnT⟩
        simp only [coveredInteriorStations, Finset.mem_union, Finset.mem_image]
        exact Or.inr ⟨m, hm_in, rfl⟩
      · rcases Nat.even_or_odd (n.factorization 2) with hn_ev | hn_odd
        · have hn_in : n ∈ primeInteriorTruncatedAnchors 2 T := by
            simp only [primeInteriorTruncatedAnchors, primeEvenValuationAnchors, Finset.mem_filter,
              Finset.mem_Icc]
            exact ⟨⟨⟨hn1, by omega⟩, hn_ev⟩, h2nT⟩
          simp only [coveredInteriorStations, Finset.mem_union]
          exact Or.inl hn_in
        · have h2_dvd : 2 ∣ n := by
            by_contra hnd
            rw [Nat.factorization_eq_zero_of_not_dvd hnd] at hn_odd
            exact (Nat.odd_iff_not_even.mp hn_odd) even_zero
          obtain ⟨m, rfl⟩ := h2_dvd
          have hm1 : 1 ≤ m := by omega
          have hm_ne : m ≠ 0 := by omega
          have hm_ev : Even (m.factorization 2) := by
            rw [Nat.factorization_mul (by decide) hm_ne, Finsupp.add_apply,
              Nat.Prime.factorization Nat.prime_two, Finsupp.single_eq_same] at hn_odd
            rcases hn_odd with ⟨k, hk⟩
            exact ⟨k, by omega⟩
          have hm_in : m ∈ primeInteriorTruncatedAnchors 2 T := by
            simp only [primeInteriorTruncatedAnchors, primeEvenValuationAnchors, Finset.mem_filter,
              Finset.mem_Icc]
            exact ⟨⟨⟨hm1, by omega⟩, hm_ev⟩, hnT⟩
          simp only [coveredInteriorStations, Finset.mem_union, Finset.mem_image]
          exact Or.inr ⟨m, hm_in, rfl⟩
  have h_char_uncov :
      ∀ n ∈ Finset.Icc 1 T,
        n ∈ uncoveredCutoffStripStations 2 T ↔ (Even (n.factorization 2) ∧ T < 2 * n) := by
    intro n hn
    unfold uncoveredCutoffStripStations
    rw [Finset.mem_sdiff, and_iff_right hn, h_char_cov n hn, not_or, Nat.odd_iff_not_even, not_not, not_le]
  have h_disj_anch := (uniform_same_chain_hilbert_bound_and_closure_transfer_tc063).1 T |>.1
  have h_sum_cov :
      ∀ f : ℕ → ℝ,
        (∑ n ∈ coveredInteriorStations 2 T, f n) =
          ∑ m ∈ primeInteriorTruncatedAnchors 2 T, (f m + f (2 * m)) := by
    intro f
    unfold coveredInteriorStations
    rw [Finset.sum_union h_disj_anch, Finset.sum_image, ← Finset.sum_add_distrib]
    intro m1 _ m2 _ h_eq; omega
  have h_lam_cov : (∑ n ∈ coveredInteriorStations 2 T, (liouvilleLambda n : ℝ)) = 0 := by
    rw [h_sum_cov]
    apply Finset.sum_eq_zero
    intro m hm
    have hm1 : 1 ≤ m :=
      (Finset.mem_Icc.mp (Finset.mem_filter.mp (Finset.mem_filter.mp hm).1).1).1
    rw [liouvilleLambda_props_tc065_aux.2.2.1 (by omega : 1 ≤ 2) hm1,
      liouvilleLambda_props_tc065_aux.2.2.2 Nat.prime_two]
    ring
  have h_lam_uncov :
      (∑ n ∈ uncoveredCutoffStripStations 2 T, (liouvilleLambda n : ℝ)) =
        ∑ n ∈ Finset.Icc 1 T, (liouvilleLambda n : ℝ) := by
    rw [← h_union, Finset.sum_union h_disj, h_lam_cov, zero_add]
  exact ⟨⟨h_disj, h_union⟩, h_char_cov, h_char_uncov, h_sum_cov, h_lam_cov, h_lam_uncov⟩

private theorem coreTotal_reindexed_over_covered_tc065_aux (T : ℕ) :
    (∀ (c_lam c_half : ℝ) (D0 : ℕ) (X : ℝ),
      coreTotalScalarProfileU c_lam c_half T D0 X =
        ∑ n ∈ coveredInteriorStations 2 T,
          (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) ∧
    (∀ (pk : ℕ × ℕ) (X : ℝ),
      coreTotalFeatureVectorV T pk X =
        ∑ n ∈ coveredInteriorStations 2 T,
          (liouvilleLambda n : ℝ) * stationPrimePowerFeatureG n pk X) := by
  have h_sum_odd_to_cores :
      ∀ φ : ℕ → ℝ,
        (∑ a ∈ oddSquarefreeCores T, ∑ b ∈ coreSquareMultipliers a T, φ (a * b ^ 2)) =
          ∑ u ∈ oddChainParts T, φ u := by
    intro φ
    obtain ⟨_, _, h_bi⟩ :=
      (exact_odd_squarefree_core_bijection_and_complete_kernel_split_tc064).2.1.2.1 T
    obtain ⟨h_inj_all, _⟩ :=
      (exact_odd_squarefree_core_bijection_and_complete_kernel_split_tc064).2.1.2.2
    rw [← h_bi, Finset.sum_biUnion]
    · apply Finset.sum_congr rfl
      intro a ha
      have ha_o : Odd a := (Finset.mem_filter.mp ha).2.1
      have ha_sf : Squarefree a := (Finset.mem_filter.mp ha).2.2.1
      rw [Finset.sum_image]
      intro b1 hb1 b2 hb2 h_eq
      have hb1_o : Odd b1 := (Finset.mem_filter.mp hb1).2.1
      have hb2_o : Odd b2 := (Finset.mem_filter.mp hb2).2.1
      exact ((h_inj_all (j1 := 0) (eps1 := 0) (j2 := 0) (eps2 := 0)
        ha_o ha_sf hb1_o (by decide) ha_o ha_sf hb2_o (by decide)).mp (by simpa using h_eq)).2.1
    · intro a1 ha1 a2 ha2 hne
      change Disjoint _ _
      rw [Finset.disjoint_left]
      intro u hu1 hu2
      simp only [Finset.mem_image] at hu1 hu2
      rcases hu1 with ⟨b1, hb1, rfl⟩
      rcases hu2 with ⟨b2, hb2, h_eq⟩
      have ha1_o : Odd a1 := (Finset.mem_filter.mp ha1).2.1
      have ha1_sf : Squarefree a1 := (Finset.mem_filter.mp ha1).2.2.1
      have hb1_o : Odd b1 := (Finset.mem_filter.mp hb1).2.1
      have ha2_o : Odd a2 := (Finset.mem_filter.mp ha2).2.1
      have ha2_sf : Squarefree a2 := (Finset.mem_filter.mp ha2).2.2.1
      have hb2_o : Odd b2 := (Finset.mem_filter.mp hb2).2.1
      exact hne ((h_inj_all (j1 := 0) (eps1 := 0) (j2 := 0) (eps2 := 0)
        ha2_o ha2_sf hb2_o (by decide) ha1_o ha1_sf hb1_o (by decide)).mp
          (by simpa using h_eq)).1.symm
  have h_sum_anch :
      ∀ ψ : ℕ → ℝ,
        (∑ u ∈ oddChainParts T, ∑ j ∈ dyadicChainExponents u T, ψ (4 ^ j * u)) =
          ∑ m ∈ primeInteriorTruncatedAnchors 2 T, ψ m := by
    intro ψ
    obtain ⟨h_uniq_m, _, _, h_anch_bi⟩ :=
      (exact_odd_part_bijection_and_dyadic_chain_offdiag_split_tc063).1
    obtain ⟨h_anch_mem, h_anch_eq⟩ := h_anch_bi T
    rw [← h_anch_eq, Finset.sum_biUnion]
    · apply Finset.sum_congr rfl
      intro u hu
      have hu1 : 1 ≤ u := (Finset.mem_Icc.mp (Finset.mem_filter.mp hu).1).1
      rw [Finset.sum_image]
      intro j1 _ j2 _ h_eq
      have h4_eq : 4 ^ j1 = 4 ^ j2 := Nat.eq_of_mul_eq_mul_right hu1 h_eq
      exact Nat.pow_right_injective (by decide : 2 ≤ 4) h4_eq
    · intro u1 hu1 u2 hu2 hne
      change Disjoint _ _
      rw [Finset.disjoint_left]
      intro m hm1 hm2
      simp only [Finset.mem_image] at hm1 hm2
      rcases hm1 with ⟨j1, hj1, rfl⟩
      rcases hm2 with ⟨j2, hj2, h_eq⟩
      have hm_in : 4 ^ j1 * u1 ∈ primeInteriorTruncatedAnchors 2 T := h_anch_mem u1 hu1 j1 hj1
      obtain ⟨_, _, h_u⟩ := h_uniq_m T (4 ^ j1 * u1) hm_in
      have hp1 := h_u (u1, j1) ⟨hu1, hj1, rfl⟩
      have hp2 := h_u (u2, j2) ⟨hu2, hj2, h_eq⟩
      exact hne (Prod.mk.inj (hp1.trans hp2.symm) |>.1)
  have h_gen :
      ∀ F : ℕ → ℝ,
        (∑ a ∈ (oddSquarefreeCores T).filter (fun a => 1 ∣ a),
            (ArithmeticFunction.moebius a : ℝ) *
              ∑ b ∈ coreSquareMultipliers a T,
                ∑ j ∈ dyadicChainExponents (a * b ^ 2) T,
                  (F (4 ^ j * (a * b ^ 2)) - F (2 * (4 ^ j * (a * b ^ 2))))) =
          ∑ n ∈ coveredInteriorStations 2 T, (liouvilleLambda n : ℝ) * F n := by
    intro F
    have hf1 : (oddSquarefreeCores T).filter (fun a => 1 ∣ a) = oddSquarefreeCores T := by
      ext a; simp
    rw [hf1]
    have h_step1 :
        (∑ a ∈ oddSquarefreeCores T,
            (ArithmeticFunction.moebius a : ℝ) *
              ∑ b ∈ coreSquareMultipliers a T,
                ∑ j ∈ dyadicChainExponents (a * b ^ 2) T,
                  (F (4 ^ j * (a * b ^ 2)) - F (2 * (4 ^ j * (a * b ^ 2))))) =
          ∑ a ∈ oddSquarefreeCores T, ∑ b ∈ coreSquareMultipliers a T,
            (liouvilleLambda (a * b ^ 2) : ℝ) *
              ∑ j ∈ dyadicChainExponents (a * b ^ 2) T,
                (F (4 ^ j * (a * b ^ 2)) - F (2 * (4 ^ j * (a * b ^ 2)))) := by
      apply Finset.sum_congr rfl
      intro a ha
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro b hb
      have ha_sf : Squarefree a := (Finset.mem_filter.mp ha).2.2.1
      have hb1 : 1 ≤ b := (Finset.mem_Icc.mp (Finset.mem_filter.mp hb).1).1
      have hlm := ((exact_odd_squarefree_core_bijection_and_complete_kernel_split_tc064).1.2
        ha_sf hb1).1
      rw [hlm]
    rw [h_step1,
      h_sum_odd_to_cores (fun u =>
        (liouvilleLambda u : ℝ) *
          ∑ j ∈ dyadicChainExponents u T, (F (4 ^ j * u) - F (2 * (4 ^ j * u))))]
    have h_step2 :
        (∑ u ∈ oddChainParts T,
            (liouvilleLambda u : ℝ) *
              ∑ j ∈ dyadicChainExponents u T, (F (4 ^ j * u) - F (2 * (4 ^ j * u)))) =
          ∑ u ∈ oddChainParts T, ∑ j ∈ dyadicChainExponents u T,
            (liouvilleLambda (4 ^ j * u) : ℝ) * (F (4 ^ j * u) - F (2 * (4 ^ j * u))) := by
      apply Finset.sum_congr rfl
      intro u hu
      have hu1 : 1 ≤ u := (Finset.mem_Icc.mp (Finset.mem_filter.mp hu).1).1
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro j _
      rw [(exact_odd_part_bijection_and_dyadic_chain_offdiag_split_tc063).2.2.1 u j hu1]
    rw [h_step2,
      h_sum_anch (fun m => (liouvilleLambda m : ℝ) * (F m - F (2 * m))),
      (coveredInteriorStations_partition_and_char_tc065_aux T).2.2.2.1]
    apply Finset.sum_congr rfl
    intro m hm
    have hm1 : 1 ≤ m :=
      (Finset.mem_Icc.mp (Finset.mem_filter.mp (Finset.mem_filter.mp hm).1).1).1
    rw [liouvilleLambda_props_tc065_aux.2.2.1 (by omega : 1 ≤ 2) hm1,
      liouvilleLambda_props_tc065_aux.2.2.2 Nat.prime_two]
    ring
  refine ⟨?_, ?_⟩
  · intro c_lam c_half D0 X
    exact h_gen (fun n => adjustedStationProfilePsi c_lam c_half T D0 n X)
  · intro pk X
    exact h_gen (fun n => stationPrimePowerFeatureG n pk X)

private theorem odd_prime_power_vanishing_above_half_tc065_aux
    {T p k : ℕ} (_hp : Nat.Prime p) (hp_odd : Odd p) (_hk : 1 ≤ k) (hT : T < 2 * p ^ k) (X : ℝ) :
    coreTotalFeatureVectorV T (p, k) X = 0 := by
  rw [(coreTotal_reindexed_over_covered_tc065_aux T).2]
  apply Finset.sum_eq_zero
  intro n hn
  have h_not_dvd : ¬ p ^ k ∣ n := by
    intro hd
    have hn_Icc : n ∈ Finset.Icc 1 T := by
      have h_un := (coveredInteriorStations_partition_and_char_tc065_aux T).1.2
      rw [← h_un]; exact Finset.mem_union_left _ hn
    obtain ⟨hn1, hnT⟩ := Finset.mem_Icc.mp hn_Icc
    obtain ⟨q, rfl⟩ := hd
    have hq1 : 1 ≤ q := by
      rcases Nat.eq_zero_or_pos q with rfl | hpos
      · simp at hn1
      · exact hpos
    have hq_eq1 : q = 1 := by
      by_contra hne
      have hq2 : 2 ≤ q := by omega
      have h_le : 2 * p ^ k ≤ p ^ k * q := by nlinarith
      omega
    subst hq_eq1
    rw [mul_one] at hn hn_Icc
    have h_char := ((coveredInteriorStations_partition_and_char_tc065_aux T).2.1 (p ^ k) hn_Icc).mp hn
    have h_pk_odd : Odd (p ^ k) := hp_odd.pow
    have h2_nd : ¬ 2 ∣ p ^ k := fun h2 =>
      (Nat.odd_iff_not_even.mp h_pk_odd) (even_iff_two_dvd.mpr h2)
    have hf0 : (p ^ k).factorization 2 = 0 := Nat.factorization_eq_zero_of_not_dvd h2_nd
    rcases h_char with h_odd | hle
    · rw [hf0] at h_odd
      exact (Nat.odd_iff_not_even.mp h_odd) even_zero
    · omega
  simp [stationPrimePowerFeatureG, h_not_dvd]

private theorem odd_prime_power_square_lift_parity_tc065_aux
    {p m r a b : ℕ} (hp : Nat.Prime p) (hp_odd : Odd p) (hm : 1 ≤ m)
    (ha_odd : Odd a) (ha_sf : Squarefree a) (hb_odd : Odd b) :
    (p ^ (2 * m) ∣ 2 ^ r * a * b ^ 2 ↔ p ^ m ∣ b) ∧
      (p ^ (2 * m - 1) ∣ 2 ^ r * a * b ^ 2 ↔
        (p ∣ a ∧ p ^ (m - 1) ∣ b) ∨ (¬ p ∣ a ∧ p ^ m ∣ b)) := by
  have ha_ne : a ≠ 0 := ne_of_gt ha_odd.pos
  have hb_ne : b ≠ 0 := ne_of_gt hb_odd.pos
  have h2r_ne : 2 ^ r ≠ 0 := pow_ne_zero r (by decide)
  have hprod_ne : 2 ^ r * a * b ^ 2 ≠ 0 :=
    mul_ne_zero (mul_ne_zero h2r_ne ha_ne) (pow_ne_zero 2 hb_ne)
  have hp_ne2 : p ≠ 2 := by
    intro h2; subst h2; exact (Nat.odd_iff_not_even.mp hp_odd) (by decide)
  have h2_nd_p : ¬ p ∣ 2 := by
    intro hd
    rcases Nat.prime_two.eq_one_or_self_of_dvd p hd with h1 | h2
    · exact hp.ne_one h1
    · exact hp_ne2 h2
  have h_fact_prod :
      (2 ^ r * a * b ^ 2).factorization p = a.factorization p + 2 * b.factorization p := by
    rw [Nat.factorization_mul (mul_ne_zero h2r_ne ha_ne) (pow_ne_zero 2 hb_ne),
      Nat.factorization_mul h2r_ne ha_ne, Finsupp.add_apply, Finsupp.add_apply,
      Nat.factorization_pow, Nat.factorization_pow, Finsupp.smul_apply, Finsupp.smul_apply,
      smul_eq_mul, smul_eq_mul, Nat.factorization_eq_zero_of_not_dvd h2_nd_p, mul_zero, zero_add]
  have ha_le1 : a.factorization p ≤ 1 := (Nat.squarefree_iff_factorization_le_one ha_ne).mp ha_sf p
  have ha_dvd_iff : p ∣ a ↔ a.factorization p = 1 := by
    rw [hp.dvd_iff_one_le_factorization ha_ne]; omega
  rw [hp.pow_dvd_iff_le_factorization hprod_ne, hp.pow_dvd_iff_le_factorization hprod_ne,
    hp.pow_dvd_iff_le_factorization hb_ne, hp.pow_dvd_iff_le_factorization hb_ne,
    h_fact_prod, ha_dvd_iff]
  constructor
  · omega
  · constructor
    · intro h
      by_cases h1 : a.factorization p = 1
      · left; exact ⟨h1, by omega⟩
      · right; exact ⟨h1, by omega⟩
    · rintro (⟨_h1, _h2⟩ | ⟨_h1, _h2⟩) <;> omega

private theorem gaussianTermPhi_dilation_tc065_aux {d q : ℕ} (hd : 1 ≤ d) (hq : 1 ≤ q)
    {X : ℝ} (hX0 : 0 < X) :
    gaussianTermPhi (d * q) X =
      (1 / Real.sqrt (d : ℝ)) * gaussianTermPhi q (X / (d : ℝ)) := by
  have hd_pos : (0 : ℝ) < (d : ℝ) := Nat.cast_pos.mpr hd
  have hq_pos : (0 : ℝ) < (q : ℝ) := Nat.cast_pos.mpr hq
  have hsq_pos : 0 < Real.sqrt (d : ℝ) := Real.sqrt_pos.mpr hd_pos
  unfold gaussianTermPhi
  rw [Nat.cast_mul, Real.div_rpow (le_of_lt hX0) (le_of_lt hd_pos)]
  have h_exp_eq : -((X / (d : ℝ)) ^ 2) / (q : ℝ) ^ 2 = -(X ^ 2) / ((d : ℝ) * (q : ℝ)) ^ 2 := by
    field_simp [ne_of_gt hd_pos, ne_of_gt hq_pos]; ring
  rw [h_exp_eq]
  have hd52 : (d : ℝ) ^ (5 / 2 : ℝ) * Real.sqrt (d : ℝ) = (d : ℝ) ^ 3 := by
    rw [Real.sqrt_eq_rpow, ← Real.rpow_add hd_pos]
    norm_num
    exact_mod_cast Real.rpow_natCast (d : ℝ) 3
  have hd52_ne : (d : ℝ) ^ (5 / 2 : ℝ) ≠ 0 := ne_of_gt (Real.rpow_pos_of_pos hd_pos _)
  have hd3_ne : (d : ℝ) ^ 3 ≠ 0 := pow_ne_zero 3 (ne_of_gt hd_pos)
  have hq3_ne : (q : ℝ) ^ 3 ≠ 0 := pow_ne_zero 3 (ne_of_gt hq_pos)
  have h_inv_eq :
      (((d : ℝ) * (q : ℝ)) ^ 3)⁻¹ =
        (1 / Real.sqrt (d : ℝ)) * (1 / (d : ℝ) ^ (5 / 2 : ℝ)) * ((q : ℝ) ^ 3)⁻¹ := by
    rw [mul_pow, mul_inv]
    field_simp [ne_of_gt hsq_pos, hd52_ne, hd3_ne, hq3_ne]
    linarith [hd52]
  rw [h_inv_eq]
  ring

private theorem sum_primePowerPairs_log_eq_log_tc065_aux {T n : ℕ} (hn : n ∈ Finset.Icc 1 T) :
    (∑ pk ∈ (primePowerPairsUpTo T).filter (fun pk => pk.1 ^ pk.2 ∣ n),
        Real.log (pk.1 : ℝ)) = Real.log (n : ℝ) := by
  obtain ⟨hn1, hnT⟩ := Finset.mem_Icc.mp hn
  have hn_ne : n ≠ 0 := by omega
  have h_sum_vm :
      (∑ d ∈ n.divisors, ArithmeticFunction.vonMangoldt d) = Real.log (n : ℝ) :=
    ArithmeticFunction.vonMangoldt_sum
  rw [← h_sum_vm]
  let S_pp := (primePowerPairsUpTo T).filter (fun pk => pk.1 ^ pk.2 ∣ n)
  let D_pp := n.divisors.filter (fun d => IsPrimePow d)
  have h_vm_filt :
      (∑ d ∈ n.divisors, ArithmeticFunction.vonMangoldt d) =
        ∑ d ∈ D_pp, ArithmeticFunction.vonMangoldt d := by
    symm
    apply Finset.sum_subset (Finset.filter_subset _ _)
    intro d hd hnot
    simp only [D_pp, Finset.mem_filter, not_and] at hnot
    have hnp : ¬ IsPrimePow d := hnot hd
    rw [ArithmeticFunction.vonMangoldt_apply, if_neg hnp]
  rw [h_vm_filt]
  apply Finset.sum_bij (fun pk _ => pk.1 ^ pk.2)
  · intro pk hpk
    simp only [S_pp, primePowerPairsUpTo, primesUpToFinset, Finset.mem_filter,
      Finset.mem_product, Finset.mem_Icc] at hpk
    rcases hpk with ⟨⟨⟨⟨⟨_, _⟩, hp⟩, ⟨hk1, _⟩⟩, _⟩, hdvd⟩
    simp only [D_pp, Finset.mem_filter, Nat.mem_divisors]
    exact ⟨⟨hdvd, hn_ne⟩, hp.isPrimePow.pow (by omega)⟩
  · intro pk1 hpk1 pk2 hpk2 h_eq
    simp only [S_pp, primePowerPairsUpTo, primesUpToFinset, Finset.mem_filter,
      Finset.mem_product, Finset.mem_Icc] at hpk1 hpk2
    have hp1 : pk1.1.Prime := hpk1.1.1.1.2
    have hk1 : 1 ≤ pk1.2 := hpk1.1.1.2.1
    have hp2 : pk2.1.Prime := hpk2.1.1.1.2
    have hk2 : 1 ≤ pk2.2 := hpk2.1.1.2.1
    have hp1_dvd : pk1.1 ∣ pk2.1 ^ pk2.2 := by
      rw [← h_eq]; exact dvd_pow_self pk1.1 (by omega)
    have hp_eq : pk1.1 = pk2.1 := by
      rcases hp2.eq_one_or_self_of_dvd pk1.1 (hp1.dvd_of_dvd_pow hp1_dvd) with h1 | h2
      · exact False.elim (hp1.ne_one h1)
      · exact h2
    have hk_eq : pk1.2 = pk2.2 := by
      rw [hp_eq] at h_eq
      exact Nat.pow_right_injective hp2.two_le h_eq
    exact Prod.ext hp_eq hk_eq
  · intro d hd
    simp only [D_pp, Finset.mem_filter, Nat.mem_divisors] at hd
    rcases hd with ⟨⟨hd_dvd, _⟩, hd_pp⟩
    rw [isPrimePow_nat_iff] at hd_pp
    rcases hd_pp with ⟨p, k, hp, hk_pos, rfl⟩
    have hd_le_n : p ^ k ≤ n := Nat.le_of_dvd hn1 hd_dvd
    have hp_le_T : p ≤ T := by
      have hp_le : p ≤ p ^ k := Nat.le_self_pow (by omega) p
      omega
    have hk_le_T : k ≤ T := by
      have h_le_two_pow : ∀ j : ℕ, j ≤ 2 ^ j := by
        intro j
        induction j with
        | zero => norm_num
        | succ m ihm =>
          rw [pow_succ]
          have h1 : 1 ≤ 2 ^ m := Nat.one_le_pow m 2 (by decide)
          omega
      have hk_le : k ≤ 2 ^ k := h_le_two_pow k
      have h2_le : 2 ^ k ≤ p ^ k := Nat.pow_le_pow_left hp.two_le k
      omega
    refine ⟨(p, k), ?_, rfl⟩
    simp only [S_pp, primePowerPairsUpTo, primesUpToFinset, Finset.mem_filter,
      Finset.mem_product, Finset.mem_Icc]
    exact ⟨⟨⟨⟨⟨hp.two_le, hp_le_T⟩, hp⟩, ⟨hk_pos, hk_le_T⟩⟩, by omega⟩, hd_dvd⟩
  · intro pk hpk
    simp only [S_pp, primePowerPairsUpTo, primesUpToFinset, Finset.mem_filter,
      Finset.mem_product, Finset.mem_Icc] at hpk
    have hp : pk.1.Prime := hpk.1.1.1.2
    have hk : 1 ≤ pk.2 := hpk.1.1.2.1
    rw [ArithmeticFunction.vonMangoldt_apply_pow (Nat.ne_of_gt hk),
      ArithmeticFunction.vonMangoldt_apply_prime hp]

private theorem fullFeatureVectorG_eq_liouvillePrimePowerTerm_div_log_tc065_aux
    {T : ℕ} {pk : ℕ × ℕ} (hpk : pk ∈ primePowerPairsUpTo T) {X : ℝ} (hX0 : 0 < X) :
    fullFeatureVectorG T pk X = liouvillePrimePowerTerm T pk X / Real.log X := by
  simp only [primePowerPairsUpTo, primesUpToFinset, Finset.mem_filter, Finset.mem_product,
    Finset.mem_Icc] at hpk
  rcases hpk with ⟨⟨⟨⟨_, _⟩, hp⟩, ⟨_hk1, _⟩⟩, _⟩
  let d := pk.1 ^ pk.2
  have hd1 : 1 ≤ d := Nat.one_le_pow pk.2 pk.1 hp.pos
  unfold fullFeatureVectorG stationPrimePowerFeatureG
  have h_filt :
      (∑ n ∈ Finset.Icc 1 T,
          (liouvilleLambda n : ℝ) *
            (if d ∣ n then Real.log (pk.1 : ℝ) * gaussianTermPhi n X / Real.log X else 0)) =
        ∑ n ∈ (Finset.Icc 1 T).filter (fun n => d ∣ n),
          (liouvilleLambda n : ℝ) * (Real.log (pk.1 : ℝ) * gaussianTermPhi n X / Real.log X) := by
    rw [Finset.sum_filter]
    apply Finset.sum_congr rfl
    intro n _; split_ifs <;> ring
  change (∑ n ∈ Finset.Icc 1 T,
      (liouvilleLambda n : ℝ) *
        (if d ∣ n then Real.log (pk.1 : ℝ) * gaussianTermPhi n X / Real.log X else 0)) = _
  rw [h_filt]
  have h_set :
      (Finset.Icc 1 T).filter (fun n => d ∣ n) = (Finset.Icc 1 (T / d)).image (fun q => d * q) := by
    ext n
    simp only [Finset.mem_filter, Finset.mem_Icc, Finset.mem_image]
    constructor
    · rintro ⟨⟨hn1, hnT⟩, ⟨q, rfl⟩⟩
      have hq1 : 1 ≤ q := by
        rcases Nat.eq_zero_or_pos q with rfl | hpos
        · simp at hn1
        · exact hpos
      have hq_le : q ≤ T / d := (Nat.le_div_iff_mul_le hd1).mpr (by rw [mul_comm]; exact hnT)
      exact ⟨q, ⟨hq1, hq_le⟩, rfl⟩
    · rintro ⟨q, ⟨hq1, hq_le⟩, rfl⟩
      have h_le : d * q ≤ T := by
        have hm := (Nat.le_div_iff_mul_le hd1).mp hq_le
        rwa [mul_comm] at hm
      exact ⟨⟨Nat.mul_pos hd1 hq1, h_le⟩, dvd_mul_right d q⟩
  rw [h_set, Finset.sum_image (fun q1 _ q2 _ heq => Nat.eq_of_mul_eq_mul_left hd1 heq)]
  have h_lam_d : (liouvilleLambda d : ℝ) = (-1 : ℝ) ^ pk.2 := by
    have hd_ne : d ≠ 0 := by omega
    have h_om_pow : ∀ j : ℕ, natOmega (pk.1 ^ j) = j := by
      intro j
      induction j with
      | zero => simp [natOmega]
      | succ m ihm =>
        rw [pow_succ]
        unfold natOmega at ihm ⊢
        rw [ArithmeticFunction.cardFactors_mul (pow_ne_zero m hp.ne_zero) hp.ne_zero,
          ihm, ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr hp]
    have hom : natOmega d = pk.2 := h_om_pow pk.2
    simp only [liouvilleLambda, hd_ne, ↓reduceIte, liouvilleSignFromOmega, hom]
    push_cast; rfl
  have h_each :
      ∀ q ∈ Finset.Icc 1 (T / d),
        (liouvilleLambda (d * q) : ℝ) *
            (Real.log (pk.1 : ℝ) * gaussianTermPhi (d * q) X / Real.log X) =
          ((-1 : ℝ) ^ pk.2 * Real.log (pk.1 : ℝ) * (1 / Real.sqrt (d : ℝ)) / Real.log X) *
            ((liouvilleLambda q : ℝ) * gaussianTermPhi q (X / (d : ℝ))) := by
    intro q hq
    have hq1 : 1 ≤ q := (Finset.mem_Icc.mp hq).1
    rw [liouvilleLambda_props_tc065_aux.2.2.1 hd1 hq1, h_lam_d,
      gaussianTermPhi_dilation_tc065_aux hd1 hq1 hX0]
    ring
  rw [Finset.sum_congr rfl h_each, ← Finset.mul_sum]
  have hQ_eq :
      finiteQLambda (T / d) (X / (d : ℝ)) =
        ∑ q ∈ Finset.Icc 1 (T / d), (liouvilleLambda q : ℝ) * gaussianTermPhi q (X / (d : ℝ)) := by
    unfold finiteQLambda gaussianTermPhi
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl; intro q _; ring
  unfold liouvillePrimePowerTerm
  dsimp [d] at hQ_eq ⊢
  rw [hQ_eq]
  ring

private theorem openCoreSmoothCoeffS_telescoping_tc065_aux {T : ℕ} (hT1 : 1 ≤ T)
    (D0 : ℕ) (c_lam c_half : ℝ) {n : ℕ} (hn : n ∈ Finset.Icc 1 T) :
    let D_eff := min D0 (T - 1)
    let R_osc := fun d => selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d
    openCoreSmoothCoeffS c_lam c_half T D0 n =
      (∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1),
          (liouvilleLambda (n / e) : ℝ) * (R_osc e - R_osc (e - 1))) +
        (if D_eff + 1 ≤ T - 1 ∧ (D_eff + 1) ∣ n then
          (liouvilleLambda (n / (D_eff + 1)) : ℝ) * R_osc (D_eff + 1)
        else 0) -
        (if n = T ∧ D_eff + 1 ≤ T - 1 then R_osc (T - 1) else 0) := by
  intro D_eff R_osc
  obtain ⟨hn1, hnT⟩ := Finset.mem_Icc.mp hn
  have hn_ne : n ≠ 0 := by omega
  unfold openCoreSmoothCoeffS
  change (∑ d ∈ (Finset.Icc (D_eff + 1) (T - 1)).filter (fun d => d ∣ n ∧ n / d ≤ T / d),
        R_osc d * (liouvilleLambda (n / d) : ℝ)) -
      (∑ d ∈ (Finset.Icc (D_eff + 1) (T - 1)).filter (fun d => (d + 1) ∣ n ∧ n / (d + 1) ≤ T / d),
        R_osc d * (liouvilleLambda (n / (d + 1)) : ℝ)) = _
  by_cases h_range : D_eff + 1 ≤ T - 1
  · have hS1_eq :
        (Finset.Icc (D_eff + 1) (T - 1)).filter (fun d => d ∣ n ∧ n / d ≤ T / d) =
          n.divisors.filter (fun e => D_eff + 1 ≤ e ∧ e ≤ T - 1) := by
      ext e
      simp only [Finset.mem_filter, Finset.mem_Icc, Nat.mem_divisors]
      constructor
      · rintro ⟨⟨h1, h2⟩, hd, _⟩; exact ⟨⟨hd, hn_ne⟩, h1, h2⟩
      · rintro ⟨⟨hd, _⟩, h1, h2⟩; exact ⟨⟨h1, h2⟩, hd, Nat.div_le_div_right hnT⟩
    have hS2_eq :
        ((Finset.Icc (D_eff + 1) (T - 1)).filter
            (fun d => (d + 1) ∣ n ∧ n / (d + 1) ≤ T / d)).image (fun d => d + 1) =
          n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T) := by
      ext e
      simp only [Finset.mem_image, Finset.mem_filter, Finset.mem_Icc, Nat.mem_divisors]
      constructor
      · rintro ⟨d, ⟨⟨h1, h2⟩, hd, _⟩, rfl⟩
        exact ⟨⟨hd, hn_ne⟩, by omega, by omega⟩
      · rintro ⟨⟨hd, _⟩, h1, h2⟩
        refine ⟨e - 1, ⟨⟨by omega, by omega⟩, ?_, ?_⟩, by omega⟩
        · rwa [show e - 1 + 1 = e by omega]
        · rw [show e - 1 + 1 = e by omega]
          exact le_trans (Nat.div_le_div_right hnT) (Nat.div_le_div_left (by omega) (by omega))
    have h_sum1 :
        (∑ d ∈ (Finset.Icc (D_eff + 1) (T - 1)).filter (fun d => d ∣ n ∧ n / d ≤ T / d),
            R_osc d * (liouvilleLambda (n / d) : ℝ)) =
          (∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1),
              (liouvilleLambda (n / e) : ℝ) * R_osc e) +
            (if (D_eff + 1) ∣ n then
              (liouvilleLambda (n / (D_eff + 1)) : ℝ) * R_osc (D_eff + 1)
            else 0) := by
      rw [hS1_eq]
      have h_mul_comm :
          (∑ e ∈ n.divisors.filter (fun e => D_eff + 1 ≤ e ∧ e ≤ T - 1),
              R_osc e * (liouvilleLambda (n / e) : ℝ)) =
            ∑ e ∈ n.divisors.filter (fun e => D_eff + 1 ≤ e ∧ e ≤ T - 1),
              (liouvilleLambda (n / e) : ℝ) * R_osc e :=
        Finset.sum_congr rfl (fun _ _ => mul_comm _ _)
      rw [h_mul_comm]
      by_cases hdv : (D_eff + 1) ∣ n
      · rw [if_pos hdv]
        have hmem : D_eff + 1 ∈ n.divisors.filter (fun e => D_eff + 1 ≤ e ∧ e ≤ T - 1) := by
          simp only [Finset.mem_filter, Nat.mem_divisors]
          exact ⟨⟨hdv, hn_ne⟩, le_refl _, h_range⟩
        have her :
            (n.divisors.filter (fun e => D_eff + 1 ≤ e ∧ e ≤ T - 1)).erase (D_eff + 1) =
              n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1) := by
          ext e
          simp only [Finset.mem_erase, Finset.mem_filter, Nat.mem_divisors]
          constructor
          · rintro ⟨hne, hd, h1, h2⟩; exact ⟨hd, by omega, h2⟩
          · rintro ⟨hd, h1, h2⟩; exact ⟨by omega, hd, by omega, h2⟩
        rw [← Finset.add_sum_erase _ _ hmem, her, add_comm]
      · rw [if_neg hdv, add_zero]
        apply Finset.sum_congr
        · ext e
          simp only [Finset.mem_filter, Nat.mem_divisors]
          constructor
          · rintro ⟨⟨hd, hne⟩, h1, h2⟩
            have hne1 : e ≠ D_eff + 1 := fun heq => hdv (heq ▸ hd)
            exact ⟨⟨hd, hne⟩, by omega, h2⟩
          · rintro ⟨hd, h1, h2⟩; exact ⟨hd, by omega, h2⟩
        · intro _ _; rfl
    have h_sum2 :
        (∑ d ∈ (Finset.Icc (D_eff + 1) (T - 1)).filter
            (fun d => (d + 1) ∣ n ∧ n / (d + 1) ≤ T / d),
            R_osc d * (liouvilleLambda (n / (d + 1)) : ℝ)) =
          (∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1),
              (liouvilleLambda (n / e) : ℝ) * R_osc (e - 1)) +
            (if n = T then R_osc (T - 1) else 0) := by
      have h_reidx :
          (∑ d ∈ (Finset.Icc (D_eff + 1) (T - 1)).filter
              (fun d => (d + 1) ∣ n ∧ n / (d + 1) ≤ T / d),
              R_osc d * (liouvilleLambda (n / (d + 1)) : ℝ)) =
            ∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T),
              (liouvilleLambda (n / e) : ℝ) * R_osc (e - 1) := by
        rw [← hS2_eq, Finset.sum_image (fun d1 _ d2 _ h => by omega)]
        apply Finset.sum_congr rfl
        intro d _
        rw [show d + 1 - 1 = d by omega, mul_comm]
      rw [h_reidx]
      by_cases hn_eq : n = T
      · subst hn_eq
        rw [if_pos rfl]
        have hmem : n ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ n) := by
          simp only [Finset.mem_filter, Nat.mem_divisors]
          exact ⟨⟨dvd_refl n, hn_ne⟩, by omega, le_refl n⟩
        have her :
            (n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ n)).erase n =
              n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ n - 1) := by
          ext e
          simp only [Finset.mem_erase, Finset.mem_filter, Nat.mem_divisors]
          constructor
          · rintro ⟨hne, hd, h1, h2⟩; exact ⟨hd, h1, by omega⟩
          · rintro ⟨hd, h1, h2⟩; exact ⟨by omega, hd, h1, by omega⟩
        rw [← Finset.add_sum_erase _ _ hmem, her, Nat.div_self hn1,
          liouvilleLambda_props_tc065_aux.1, one_mul, add_comm]
      · rw [if_neg hn_eq, add_zero]
        apply Finset.sum_congr
        · ext e
          simp only [Finset.mem_filter, Nat.mem_divisors]
          constructor
          · rintro ⟨⟨hd, hne⟩, h1, h2⟩
            have he_le_n : e ≤ n := Nat.le_of_dvd hn1 hd
            exact ⟨⟨hd, hne⟩, h1, by omega⟩
          · rintro ⟨hd, h1, h2⟩; exact ⟨hd, h1, by omega⟩
        · intro _ _; rfl
    rw [h_sum1, h_sum2]
    have h_if1 : (D_eff + 1 ≤ T - 1 ∧ (D_eff + 1) ∣ n) ↔ (D_eff + 1) ∣ n :=
      and_iff_right h_range
    have h_if2 : (n = T ∧ D_eff + 1 ≤ T - 1) ↔ n = T :=
      and_iff_left h_range
    simp only [h_if1, h_if2]
    have h_sub_sum :
        (∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1),
            (liouvilleLambda (n / e) : ℝ) * R_osc e) -
          (∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1),
            (liouvilleLambda (n / e) : ℝ) * R_osc (e - 1)) =
          ∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1),
            (liouvilleLambda (n / e) : ℝ) * (R_osc e - R_osc (e - 1)) := by
      rw [← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro e _; ring
    linarith [h_sub_sum]
  · have h_emp1 : (Finset.Icc (D_eff + 1) (T - 1)) = ∅ := Finset.Icc_eq_empty h_range
    have h_emp2 : n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1) = ∅ := by
      ext e; simp only [Finset.mem_filter, Finset.not_mem_empty, iff_false]; omega
    simp [h_emp1, h_emp2, h_range]

private theorem sum_divisors_abs_selbergLiouvilleWeight2_tc065_aux {n : ℕ} (hn1 : 1 ≤ n) :
    (∑ e ∈ n.divisors, |selbergLiouvilleWeight2 e|) = (Real.log (n : ℝ)) ^ 2 := by
  have hn_ne : n ≠ 0 := by omega
  have h_lv_eq : ∀ d : ℕ, 1 ≤ d →
      liouvilleVonMangoldt d = (liouvilleLambda d : ℝ) * ArithmeticFunction.vonMangoldt d := by
    intro d hd
    have h1 := (factorization_sign_agreement_and_selberg_w2_formulas_tc061).1.1 hd (le_refl 1)
    rw [liouvilleLambda_props_tc065_aux.1, mul_one, mul_one] at h1
    exact h1
  have h_abs_w2 : ∀ e : ℕ, 1 ≤ e →
      |selbergLiouvilleWeight2 e| =
        ArithmeticFunction.vonMangoldt e * Real.log (e : ℝ) +
          (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) e := by
    intro e he1
    have h_conv :
        (liouvilleVonMangoldt * liouvilleVonMangoldt) e =
          (liouvilleLambda e : ℝ) *
            (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) e := by
      rw [ArithmeticFunction.mul_apply, ArithmeticFunction.mul_apply, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro xy hxy
      rw [Nat.mem_divisorsAntidiagonal] at hxy
      have hx1 : 1 ≤ xy.1 := by
        rcases Nat.eq_zero_or_pos xy.1 with hz | hp
        · rw [hz, zero_mul] at hxy; omega
        · exact hp
      have hy1 : 1 ≤ xy.2 := by
        rcases Nat.eq_zero_or_pos xy.2 with hz | hp
        · rw [hz, mul_zero] at hxy; omega
        · exact hp
      rw [h_lv_eq xy.1 hx1, h_lv_eq xy.2 hy1, ← hxy.1,
        liouvilleLambda_props_tc065_aux.2.2.1 hx1 hy1]
      ring
    have h_w2 :
        selbergLiouvilleWeight2 e =
          (liouvilleLambda e : ℝ) *
            (ArithmeticFunction.vonMangoldt e * Real.log (e : ℝ) +
              (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) e) := by
      unfold selbergLiouvilleWeight2
      rw [h_lv_eq e he1, h_conv]
      ring
    have h_nn1 : 0 ≤ ArithmeticFunction.vonMangoldt e * Real.log (e : ℝ) :=
      mul_nonneg ArithmeticFunction.vonMangoldt_nonneg
        (Real.log_nonneg (by exact_mod_cast he1))
    have h_nn2 : 0 ≤ (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) e := by
      rw [ArithmeticFunction.mul_apply]
      exact Finset.sum_nonneg (fun _ _ =>
        mul_nonneg ArithmeticFunction.vonMangoldt_nonneg ArithmeticFunction.vonMangoldt_nonneg)
    rw [h_w2, abs_mul, (liouvilleLambda_props_tc065_aux.2.1 he1).2, one_mul,
      abs_of_nonneg (add_nonneg h_nn1 h_nn2)]
  have h_sum_abs :
      (∑ e ∈ n.divisors, |selbergLiouvilleWeight2 e|) =
        (∑ e ∈ n.divisors, ArithmeticFunction.vonMangoldt e * Real.log (e : ℝ)) +
          ∑ e ∈ n.divisors,
            (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) e := by
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro e he
    exact h_abs_w2 e (Nat.pos_of_dvd_of_pos (Nat.mem_divisors.mp he).1 hn1)
  rw [h_sum_abs]
  have h_conv_sum :
      (∑ e ∈ n.divisors,
          (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) e) =
        ∑ d ∈ n.divisors, ArithmeticFunction.vonMangoldt d * Real.log ((n / d : ℕ) : ℝ) := by
    have h_rewrite :
        (∑ e ∈ n.divisors,
            (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) e) =
          ∑ e ∈ n.divisors, ∑ d ∈ e.divisors,
            ArithmeticFunction.vonMangoldt d * ArithmeticFunction.vonMangoldt (e / d) := by
      apply Finset.sum_congr rfl
      intro e _
      rw [ArithmeticFunction.mul_apply]
      exact Nat.sum_divisorsAntidiagonal
        (fun a b => ArithmeticFunction.vonMangoldt a * ArithmeticFunction.vonMangoldt b)
    rw [h_rewrite]
    trans (∑ d ∈ n.divisors, ∑ r ∈ (n / d).divisors,
        ArithmeticFunction.vonMangoldt d * ArithmeticFunction.vonMangoldt r)
    · rw [Finset.sum_sigma', Finset.sum_sigma']
      apply Finset.sum_bij (fun ed _ => ⟨ed.2, ed.1 / ed.2⟩)
      · intro ed hed
        simp only [Finset.mem_sigma, Nat.mem_divisors] at hed ⊢
        rcases hed with ⟨⟨he_dvd, _⟩, ⟨hd_dvd, he_ne⟩⟩
        have hd_dvd_n : ed.2 ∣ n := dvd_trans hd_dvd he_dvd
        have hd_pos : 1 ≤ ed.2 := Nat.pos_of_dvd_of_pos hd_dvd (Nat.pos_of_ne_zero he_ne)
        have hq_dvd : ed.1 / ed.2 ∣ n / ed.2 := by
          obtain ⟨c, hc⟩ := he_dvd
          refine ⟨c, ?_⟩
          apply Nat.eq_of_mul_eq_mul_left hd_pos
          rw [Nat.mul_div_cancel' hd_dvd_n, ← mul_assoc, Nat.mul_div_cancel' hd_dvd, hc]
        have hnd_ne : n / ed.2 ≠ 0 :=
          ne_of_gt (Nat.div_pos (Nat.le_of_dvd hn1 hd_dvd_n) hd_pos)
        exact ⟨⟨hd_dvd_n, hn_ne⟩, ⟨hq_dvd, hnd_ne⟩⟩
      · intro a ha b hb heq
        simp only [Finset.mem_sigma, Nat.mem_divisors] at ha hb
        have h2 : a.2 = b.2 := congr_arg Sigma.fst heq
        have hq : a.1 / a.2 = b.1 / b.2 := by
          have := congr_arg Sigma.snd heq; simpa using this
        have h1 : a.1 = b.1 := by
          calc a.1 = a.2 * (a.1 / a.2) := (Nat.mul_div_cancel' ha.2.1).symm
            _ = b.2 * (b.1 / b.2) := by rw [hq, h2]
            _ = b.1 := Nat.mul_div_cancel' hb.2.1
        cases a; cases b; dsimp at h1 h2; subst h1; subst h2; rfl
      · intro dr hdr
        simp only [Finset.mem_sigma, Nat.mem_divisors] at hdr
        rcases hdr with ⟨⟨hd_dvd, _⟩, ⟨hr_dvd, _⟩⟩
        have hd_pos : 1 ≤ dr.1 := Nat.pos_of_dvd_of_pos hd_dvd hn1
        have hr_pos : 1 ≤ dr.2 := by
          have hnd_pos : 1 ≤ n / dr.1 := Nat.div_pos (Nat.le_of_dvd hn1 hd_dvd) hd_pos
          exact Nat.pos_of_dvd_of_pos hr_dvd hnd_pos
        have hdr_dvd : dr.1 * dr.2 ∣ n := by
          obtain ⟨k, hk⟩ := hr_dvd
          refine ⟨k, ?_⟩
          calc n = dr.1 * (n / dr.1) := (Nat.mul_div_cancel' hd_dvd).symm
            _ = dr.1 * (dr.2 * k) := by rw [hk]
            _ = dr.1 * dr.2 * k := by ring
        refine ⟨⟨dr.1 * dr.2, dr.1⟩, ?_, ?_⟩
        · simp only [Finset.mem_sigma, Nat.mem_divisors]
          exact ⟨⟨hdr_dvd, hn_ne⟩, ⟨dvd_mul_right dr.1 dr.2, mul_ne_zero (by omega) (by omega)⟩⟩
        · simp [Nat.mul_div_cancel_left dr.2 hd_pos]
      · intro _ _; rfl
    · apply Finset.sum_congr rfl
      intro d _
      rw [← Finset.mul_sum, ArithmeticFunction.vonMangoldt_sum]
  rw [h_conv_sum, ← Finset.sum_add_distrib]
  have h_comb :
      (∑ d ∈ n.divisors,
          (ArithmeticFunction.vonMangoldt d * Real.log (d : ℝ) +
            ArithmeticFunction.vonMangoldt d * Real.log ((n / d : ℕ) : ℝ))) =
        (∑ d ∈ n.divisors, ArithmeticFunction.vonMangoldt d) * Real.log (n : ℝ) := by
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro d hd
    have hd_dvd : d ∣ n := (Nat.mem_divisors.mp hd).1
    have hd_pos : 1 ≤ d := Nat.pos_of_dvd_of_pos hd_dvd hn1
    have hq_pos : 1 ≤ n / d := Nat.div_pos (Nat.le_of_dvd hn1 hd_dvd) hd_pos
    have h_log_add : Real.log (d : ℝ) + Real.log ((n / d : ℕ) : ℝ) = Real.log (n : ℝ) := by
      rw [← Real.log_mul (Nat.cast_ne_zero.mpr (by omega)) (Nat.cast_ne_zero.mpr (by omega)),
        ← Nat.cast_mul, Nat.mul_div_cancel' hd_dvd]
    rw [← mul_add, h_log_add]
  rw [h_comb, ArithmeticFunction.vonMangoldt_sum, sq]

private theorem paired_station_pt_alg_tc065_aux (lam s lX ln phi : ℝ)
    (hls : lam * lam = 1) (hlX : lX ≠ 0) :
    lam * ((1 - lam * (s - lam * ln ^ 2) / lX ^ 2) * phi) =
      2 * (lam * ln * phi) / lX - (s - lam * (lX - ln) ^ 2) * phi / lX ^ 2 := by
  have hlX2 : lX ^ 2 ≠ 0 := pow_ne_zero 2 hlX
  field_simp [hlX, hlX2]
  linear_combination (-(s * phi * lX ^ 3) + lam * ln ^ 2 * phi * lX ^ 3) * hls

/-- **Theorem 2 (`TASK-TC-065` §3, Paired-Station Partition, Odd Prime-Power Vanishing Above `T / 2`, Odd Square-Lift Parity Criterion, Complete-Observable Divisor Synthesis & Full-Cutoff Bridge, and Pointwise Telescoping with Exact `∑_{e ∣ n} |w_{2,λ}(e)| = (log n)^2`)**:
    1. *Exact paired-station partition & Liouville balance (`∀ T : ℕ`)*:
       - `coveredInteriorStations 2 T ⊔ uncoveredCutoffStripStations 2 T = Finset.Icc 1 T`;
       - `n ∈ coveredInteriorStations 2 T ↔ Odd (n.factorization 2) ∨ 2 * n ≤ T` and `n ∈ uncoveredCutoffStripStations 2 T ↔ Even (n.factorization 2) ∧ T < 2 * n` on `1 ≤ n ≤ T`;
       - `∑_{n ∈ Ω_2(T)} λ(n) = 0` and `∑_{n ∈ Φ_2(T)} λ(n) = ∑_{1 ≤ n ≤ T} λ(n)`;
    2. *Exact odd prime-power channel vanishing above `T / 2`*:
       `Nat.Prime p → Odd p → 1 ≤ k → T < 2 * p ^ k → coreTotalFeatureVectorV T (p, k) X = 0`;
    3. *Exact odd prime-power square-lift parity criterion* on `2 ^ r * a * b ^ 2`;
    4. *Complete-observable arithmetic divisor synthesis and full-cutoff bridge (`2 ≤ Y`, `1 ≤ T`, `X ∈ [Y, tau * Y]`)*:
       - `U_Y = ∑_{n ∈ Ω_2(T)} λ(n) ψ_n`;
       - `V_{pk} = ∑_{n ∈ Ω_2(T)} λ(n) g_{n, pk} = G_{T, pk} - G_{Φ_2, pk}` and `G_{T, pk}(X) = liouvillePrimePowerTerm T pk X / Real.log X`;
       - `P_{Ω_2}(X) = (∑_{n ∈ Ω_2(T)} λ(n) log(n) φ_n(X)) / Real.log X`;
       - `U_Y = 2 * P_{Ω_2} - O_{Ω_2}` and `U_Y = Q_T + A_T - S_spill - Φ_fringe`;
    5. *Exact pointwise telescoping of `openCoreSmoothCoeffS` on `1 ≤ n ≤ T` and exact `∑_{e ∣ n} |selbergLiouvilleWeight2 e| = (Real.log n)^2` (`1 ≤ n`)*. -/
theorem paired_station_partition_divisor_synthesis_and_telescoping_tc065 :
    (∀ T : ℕ,
      (Disjoint (coveredInteriorStations 2 T) (uncoveredCutoffStripStations 2 T) ∧
          coveredInteriorStations 2 T ∪ uncoveredCutoffStripStations 2 T = Finset.Icc 1 T) ∧
        (∀ n ∈ Finset.Icc 1 T,
          n ∈ coveredInteriorStations 2 T ↔ (Odd (n.factorization 2) ∨ 2 * n ≤ T)) ∧
        (∀ n ∈ Finset.Icc 1 T,
          n ∈ uncoveredCutoffStripStations 2 T ↔ (Even (n.factorization 2) ∧ T < 2 * n)) ∧
        ((∑ n ∈ coveredInteriorStations 2 T, (liouvilleLambda n : ℝ)) = 0 ∧
          (∑ n ∈ uncoveredCutoffStripStations 2 T, (liouvilleLambda n : ℝ)) =
            ∑ n ∈ Finset.Icc 1 T, (liouvilleLambda n : ℝ))) ∧
    (∀ {T p k : ℕ}, Nat.Prime p → Odd p → 1 ≤ k → T < 2 * p ^ k →
      ∀ X : ℝ, coreTotalFeatureVectorV T (p, k) X = 0) ∧
    (∀ {p m r a b : ℕ}, Nat.Prime p → Odd p → 1 ≤ m → Odd a → Squarefree a → Odd b →
      (p ^ (2 * m) ∣ 2 ^ r * a * b ^ 2 ↔ p ^ m ∣ b) ∧
        (p ^ (2 * m - 1) ∣ 2 ^ r * a * b ^ 2 ↔
          (p ∣ a ∧ p ^ (m - 1) ∣ b) ∨ (¬ p ∣ a ∧ p ^ m ∣ b))) ∧
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
      ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
        coreTotalScalarProfileU c_lam c_half T D0 X =
            (∑ n ∈ coveredInteriorStations 2 T,
              (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) ∧
          (∀ pk ∈ primePowerPairsUpTo T,
            coreTotalFeatureVectorV T pk X =
                (∑ n ∈ coveredInteriorStations 2 T,
                  (liouvilleLambda n : ℝ) * stationPrimePowerFeatureG n pk X) ∧
              coreTotalFeatureVectorV T pk X =
                fullFeatureVectorG T pk X - fringeFeatureVectorG T pk X ∧
              fullFeatureVectorG T pk X = liouvillePrimePowerTerm T pk X / Real.log X) ∧
          pairedPrimePowerSumP T X =
            (∑ n ∈ coveredInteriorStations 2 T,
              (liouvilleLambda n : ℝ) * Real.log (n : ℝ) * gaussianTermPhi n X) / Real.log X ∧
          coreTotalScalarProfileU c_lam c_half T D0 X =
            2 * pairedPrimePowerSumP T X - pairedOpenCoreOscO c_lam c_half T D0 X ∧
          coreTotalScalarProfileU c_lam c_half T D0 X =
            finiteQLambda T X + knownCompensatedD2Part c_lam c_half T D0 X -
              spilloverFringeS c_lam c_half T D0 X -
              pairedCutoffFringeScalarPhi c_lam c_half T D0 X) ∧
    ((∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ) {n : ℕ}, n ∈ Finset.Icc 1 T →
        let D_eff := min D0 (T - 1)
        let R_osc := fun d => selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d
        openCoreSmoothCoeffS c_lam c_half T D0 n =
          (∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1),
              (liouvilleLambda (n / e) : ℝ) * (R_osc e - R_osc (e - 1))) +
            (if D_eff + 1 ≤ T - 1 ∧ (D_eff + 1) ∣ n then
              (liouvilleLambda (n / (D_eff + 1)) : ℝ) * R_osc (D_eff + 1)
            else 0) -
            (if n = T ∧ D_eff + 1 ≤ T - 1 then R_osc (T - 1) else 0)) ∧
      (∀ {n : ℕ}, 1 ≤ n →
        (∑ e ∈ n.divisors, |selbergLiouvilleWeight2 e|) = (Real.log (n : ℝ)) ^ 2)) := by
  refine ⟨?_, fun hp hpo hk hT X => odd_prime_power_vanishing_above_half_tc065_aux hp hpo hk hT X,
    fun hp hpo hm hao hasf hbo => odd_prime_power_square_lift_parity_tc065_aux hp hpo hm hao hasf hbo,
    ?_,
    ⟨fun {_} hT1 D0 c_lam c_half {_} hn => openCoreSmoothCoeffS_telescoping_tc065_aux hT1 D0 c_lam c_half hn,
      fun {_} hn1 => sum_divisors_abs_selbergLiouvilleWeight2_tc065_aux hn1⟩⟩
  · intro T
    obtain ⟨h1, h2, h3, _, h5⟩ := coveredInteriorStations_partition_and_char_tc065_aux T
    exact ⟨h1, h2, h3, h5⟩
  · intro Y hY2 T hT1 D0 c_lam c_half X hX
    obtain ⟨_, hprops⟩ := uIcc_tau_props_tc065_aux hY2
    obtain ⟨_, hX0, _, hlog_ne, hlog2_ne⟩ := hprops X hX
    obtain ⟨h_disj, h_union⟩ := (coveredInteriorStations_partition_and_char_tc065_aux T).1
    have hU_cov := (coreTotal_reindexed_over_covered_tc065_aux T).1 c_lam c_half D0 X
    have hV_cov := (coreTotal_reindexed_over_covered_tc065_aux T).2
    have hV_all :
        ∀ pk ∈ primePowerPairsUpTo T,
          coreTotalFeatureVectorV T pk X =
              (∑ n ∈ coveredInteriorStations 2 T,
                (liouvilleLambda n : ℝ) * stationPrimePowerFeatureG n pk X) ∧
            coreTotalFeatureVectorV T pk X =
              fullFeatureVectorG T pk X - fringeFeatureVectorG T pk X ∧
            fullFeatureVectorG T pk X = liouvillePrimePowerTerm T pk X / Real.log X := by
      intro pk hpk
      have h1 := hV_cov pk X
      have h2 : fullFeatureVectorG T pk X =
          coreTotalFeatureVectorV T pk X + fringeFeatureVectorG T pk X := by
        unfold fullFeatureVectorG fringeFeatureVectorG
        rw [← h_union, Finset.sum_union h_disj, h1]
      exact ⟨h1, by linarith,
        fullFeatureVectorG_eq_liouvillePrimePowerTerm_div_log_tc065_aux hpk hX0⟩
    have hP_eq :
        pairedPrimePowerSumP T X =
          (∑ n ∈ coveredInteriorStations 2 T,
            (liouvilleLambda n : ℝ) * Real.log (n : ℝ) * gaussianTermPhi n X) / Real.log X := by
      unfold pairedPrimePowerSumP
      rw [Finset.sum_congr rfl (fun pk _ => hV_cov pk X), Finset.sum_comm, Finset.sum_div]
      apply Finset.sum_congr rfl
      intro n hn
      have hn_Icc : n ∈ Finset.Icc 1 T := by
        rw [← h_union]; exact Finset.mem_union_left _ hn
      unfold stationPrimePowerFeatureG
      have h_inner :
          (∑ pk ∈ primePowerPairsUpTo T,
              (liouvilleLambda n : ℝ) *
                (if pk.1 ^ pk.2 ∣ n then Real.log (pk.1 : ℝ) * gaussianTermPhi n X / Real.log X else 0)) =
            (∑ pk ∈ (primePowerPairsUpTo T).filter (fun pk => pk.1 ^ pk.2 ∣ n),
              Real.log (pk.1 : ℝ)) * ((liouvilleLambda n : ℝ) * gaussianTermPhi n X / Real.log X) := by
        rw [Finset.sum_mul, Finset.sum_filter]
        apply Finset.sum_congr rfl
        intro pk _; split_ifs <;> ring
      rw [h_inner, sum_primePowerPairs_log_eq_log_tc065_aux hn_Icc]
      ring
    have hU_eq_2PO :
        coreTotalScalarProfileU c_lam c_half T D0 X =
          2 * pairedPrimePowerSumP T X - pairedOpenCoreOscO c_lam c_half T D0 X := by
      rw [hU_cov, hP_eq]
      unfold pairedOpenCoreOscO adjustedStationProfilePsi signedAdjustedCoeffB
        openCoreAdjustedCoeffBeta truncatedLiouvilleCoeff
      have h_rhs :
          2 * ((∑ n ∈ coveredInteriorStations 2 T,
                (liouvilleLambda n : ℝ) * Real.log (n : ℝ) * gaussianTermPhi n X) / Real.log X) -
            (∑ n ∈ coveredInteriorStations 2 T,
                (openCoreSmoothCoeffS c_lam c_half T D0 n -
                  (liouvilleLambda n : ℝ) * (Real.log (X / (n : ℝ))) ^ 2) * gaussianTermPhi n X) /
              (Real.log X) ^ 2 =
            ∑ n ∈ coveredInteriorStations 2 T,
              (2 * ((liouvilleLambda n : ℝ) * Real.log (n : ℝ) * gaussianTermPhi n X) / Real.log X -
                (openCoreSmoothCoeffS c_lam c_half T D0 n -
                  (liouvilleLambda n : ℝ) * (Real.log (X / (n : ℝ))) ^ 2) * gaussianTermPhi n X /
                  (Real.log X) ^ 2) := by
        rw [Finset.sum_sub_distrib, ← Finset.sum_div, ← Finset.sum_div, ← Finset.mul_sum]
        ring
      rw [h_rhs]
      apply Finset.sum_congr rfl
      intro n hn
      have hn_Icc : n ∈ Finset.Icc 1 T := by
        rw [← h_union]; exact Finset.mem_union_left _ hn
      obtain ⟨hn1, hnT⟩ := Finset.mem_Icc.mp hn_Icc
      have hn_ne : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
      have hlam_sq := (liouvilleLambda_props_tc065_aux.2.1 hn1).1
      have hlog_div : Real.log (X / (n : ℝ)) = Real.log X - Real.log (n : ℝ) :=
        Real.log_div (ne_of_gt hX0) hn_ne
      simp only [hn1, hnT, and_self, ↓reduceIte, hlog_div]
      exact paired_station_pt_alg_tc065_aux (liouvilleLambda n : ℝ)
        (openCoreSmoothCoeffS c_lam c_half T D0 n)
        (Real.log X) (Real.log (n : ℝ)) (gaussianTermPhi n X) hlam_sq hlog_ne
    have hU_bridge :
        coreTotalScalarProfileU c_lam c_half T D0 X =
          finiteQLambda T X + knownCompensatedD2Part c_lam c_half T D0 X -
            spilloverFringeS c_lam c_half T D0 X -
            pairedCutoffFringeScalarPhi c_lam c_half T D0 X := by
      have h_mix := (mixed_covariance_identity_and_theta_energy_bound_tc061).2.1 hY2 hT1
        D0 c_lam c_half X hX
      have h_beta := ((complete_core_adjusted_expansion_and_compact_gram_tc061r).2.2.1
        hT1 D0 c_lam c_half hX0 hlog_ne).2.1
      have h_icc_split :
          Finset.Icc 1 (2 * T) = Finset.Icc 1 T ∪ Finset.Icc (T + 1) (2 * T) := by
        ext k; simp only [Finset.mem_Icc, Finset.mem_union]; omega
      have h_icc_disj : Disjoint (Finset.Icc 1 T) (Finset.Icc (T + 1) (2 * T)) := by
        rw [Finset.disjoint_left]
        intro k h1 h2; simp only [Finset.mem_Icc] at h1 h2; omega
      have h_trunc_spill :
          finiteQLambda T X + knownCompensatedD2Part c_lam c_half T D0 X =
            truncatedAdjustedCoreU c_lam c_half T D0 X + spilloverFringeS c_lam c_half T D0 X := by
        rw [← h_mix, h_beta]
        unfold truncatedAdjustedCoreU spilloverFringeS
        rw [h_icc_split, Finset.sum_union h_icc_disj]
        ring
      have h_trunc_eq_sum :
          truncatedAdjustedCoreU c_lam c_half T D0 X =
            ∑ n ∈ Finset.Icc 1 T,
              (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X := by
        have h_Q_phi :
            finiteQLambda T X =
              ∑ n ∈ Finset.Icc 1 T, (liouvilleLambda n : ℝ) * gaussianTermPhi n X := by
          unfold finiteQLambda gaussianTermPhi
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl; intro n _; ring
        unfold truncatedAdjustedCoreU adjustedStationProfilePsi signedAdjustedCoeffB
        rw [h_Q_phi, Finset.sum_div, ← Finset.sum_sub_distrib]
        apply Finset.sum_congr rfl
        intro n hn
        have hn1 : 1 ≤ n := (Finset.mem_Icc.mp hn).1
        have hlam_sq := (liouvilleLambda_props_tc065_aux.2.1 hn1).1
        field_simp [hlog2_ne]
        linear_combination (openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) * hlam_sq
      have h_trunc_part :
          truncatedAdjustedCoreU c_lam c_half T D0 X =
            coreTotalScalarProfileU c_lam c_half T D0 X +
              pairedCutoffFringeScalarPhi c_lam c_half T D0 X := by
        rw [h_trunc_eq_sum, ← h_union, Finset.sum_union h_disj, ← hU_cov]
        rfl
      linarith [h_trunc_spill, h_trunc_part]
    exact ⟨hU_cov, hV_all, hP_eq, hU_eq_2PO, hU_bridge⟩

/-! ### Section 3: Hilbert Residual Budget, Pointwise Synthesis Operator Norm, and Universal Obstructions (`TASK-TC-065` §4) -/

private theorem hilbert_budget_and_contraction_tc065_aux {Y : ℝ} (hY2 : 2 ≤ Y)
    (c_lam c_half : ℝ) (T D0 : ℕ) {LV : ℝ → ℝ}
    (hLV_c : ContinuousOn LV (Set.uIcc Y (RiemannScope.tau * Y))) :
    let R := fun X => coreTotalScalarProfileU c_lam c_half T D0 X - 2 * LV X
    dampedCoreDefectD c_lam c_half T D0 Y =
        4 * windowPairing Y LV R + windowEnergyNormSq Y R -
          coreScalarDiagJA c_lam c_half T D0 Y -
          4 * ((∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV T pk X)) -
            windowEnergyNormSq Y LV) ∧
      (∀ {r : ℝ}, 0 ≤ r → r < 1 →
        windowEnergyNormSq Y LV ≤
          r ^ 2 * (∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV T pk X)) →
        dampedCoreDefectD c_lam c_half T D0 Y ≤
          windowEnergyNormSq Y R / (1 - r ^ 2) - coreScalarDiagJA c_lam c_half T D0 Y) := by
  intro R
  have hY0 : 0 < Y := by linarith
  have htau := tau_gt_one_and_lt_eight_tc065_aux.1
  obtain ⟨_, _, _, _, _, hU_c, _, _, _, _, _, _⟩ :=
    continuousOn_core_objects_tc065_aux hY2 htau c_lam c_half T D0
  have hR_c : ContinuousOn R (Set.uIcc Y (RiemannScope.tau * Y)) :=
    hU_c.sub (continuousOn_const.mul hLV_c)
  have h2LV_c : ContinuousOn (fun X => 2 * LV X) (Set.uIcc Y (RiemannScope.tau * Y)) :=
    continuousOn_const.mul hLV_c
  have hU_eq : coreTotalScalarProfileU c_lam c_half T D0 = fun X => 2 * LV X + R X := by
    ext X; dsimp [R]; ring
  have h_norm_2LV : windowEnergyNormSq Y (fun X => 2 * LV X) = 4 * windowEnergyNormSq Y LV := by
    unfold windowEnergyNormSq windowPairing
    rw [← intervalIntegral.integral_const_mul]
    apply intervalIntegral.integral_congr; intro X _; ring
  have h_pair_2LV : windowPairing Y (fun X => 2 * LV X) R = 2 * windowPairing Y LV R := by
    unfold windowPairing
    rw [← intervalIntegral.integral_const_mul]
    apply intervalIntegral.integral_congr; intro X _; ring
  have hU_exp :
      windowEnergyNormSq Y (coreTotalScalarProfileU c_lam c_half T D0) =
        4 * windowEnergyNormSq Y LV + 4 * windowPairing Y LV R + windowEnergyNormSq Y R := by
    rw [hU_eq, windowEnergyNormSq_add_eq_tc065_aux hY0 h2LV_c hR_c, h_norm_2LV, h_pair_2LV]
    ring
  have h_budget :
      dampedCoreDefectD c_lam c_half T D0 Y =
        4 * windowPairing Y LV R + windowEnergyNormSq Y R -
          coreScalarDiagJA c_lam c_half T D0 Y -
          4 * ((∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV T pk X)) -
            windowEnergyNormSq Y LV) := by
    rw [(dampedCoreDefectD_identities_tc065_aux hY2 c_lam c_half T D0).1, hU_exp]
    ring
  refine ⟨h_budget, ?_⟩
  intro r hr0 hr1 h_contr
  let S_V := ∑ pk ∈ primePowerPairsUpTo T,
    windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV T pk X)
  have hSV_nn : 0 ≤ S_V :=
    Finset.sum_nonneg (fun pk _ => windowEnergyNormSq_nonneg_tc065_aux hY0 _)
  have hLV_nn : 0 ≤ windowEnergyNormSq Y LV := windowEnergyNormSq_nonneg_tc065_aux hY0 LV
  have h1mr2_pos : 0 < 1 - r ^ 2 := by nlinarith
  rcases eq_or_lt_of_le hr0 with rfl | hr_pos
  · have hLV_zero : windowEnergyNormSq Y LV = 0 := by linarith
    have h_cs : ∀ t : ℝ, 0 ≤ t ^ 2 * windowEnergyNormSq Y LV +
        2 * t * windowPairing Y LV R + windowEnergyNormSq Y R := by
      intro t
      have h_lin : windowEnergyNormSq Y (fun X => t * LV X + R X) =
          t ^ 2 * windowEnergyNormSq Y LV + 2 * t * windowPairing Y LV R +
            windowEnergyNormSq Y R := by
        rw [windowEnergyNormSq_add_eq_tc065_aux hY0 (continuousOn_const.mul hLV_c) hR_c]
        have h1 : windowEnergyNormSq Y (fun X => t * LV X) = t ^ 2 * windowEnergyNormSq Y LV := by
          unfold windowEnergyNormSq windowPairing
          rw [← intervalIntegral.integral_const_mul]
          apply intervalIntegral.integral_congr; intro X _; ring
        have h2 : windowPairing Y (fun X => t * LV X) R = t * windowPairing Y LV R := by
          unfold windowPairing
          rw [← intervalIntegral.integral_const_mul]
          apply intervalIntegral.integral_congr; intro X _; ring
        rw [h1, h2]; ring
      rw [← h_lin]
      exact windowEnergyNormSq_nonneg_tc065_aux hY0 _
    have h_pair_zero : windowPairing Y LV R = 0 := by
      by_contra hne
      have h1 := h_cs (-(windowEnergyNormSq Y R + 1) / (2 * windowPairing Y LV R))
      rw [hLV_zero, mul_zero, zero_add] at h1
      have h2 : 2 * (-(windowEnergyNormSq Y R + 1) / (2 * windowPairing Y LV R)) *
          windowPairing Y LV R = -(windowEnergyNormSq Y R + 1) := by
        field_simp [hne]; ring
      rw [h2] at h1
      linarith
    rw [h_budget, hLV_zero, h_pair_zero]
    change 4 * 0 + windowEnergyNormSq Y R - coreScalarDiagJA c_lam c_half T D0 Y -
        4 * (S_V - 0) ≤ windowEnergyNormSq Y R / (1 - 0 ^ 2) - coreScalarDiagJA c_lam c_half T D0 Y
    norm_num
    linarith
  · let α : ℝ := 2 * (1 - r ^ 2) / r
    have h_sq_nn : 0 ≤ windowEnergyNormSq Y (fun X => α * LV X + (-r) * R X) :=
      windowEnergyNormSq_nonneg_tc065_aux hY0 _
    have h_sq_exp :
        windowEnergyNormSq Y (fun X => α * LV X + (-r) * R X) =
          α ^ 2 * windowEnergyNormSq Y LV - 2 * α * r * windowPairing Y LV R +
            r ^ 2 * windowEnergyNormSq Y R := by
      rw [windowEnergyNormSq_add_eq_tc065_aux hY0 (continuousOn_const.mul hLV_c)
        (continuousOn_const.mul hR_c)]
      have h1 : windowEnergyNormSq Y (fun X => α * LV X) = α ^ 2 * windowEnergyNormSq Y LV := by
        unfold windowEnergyNormSq windowPairing
        rw [← intervalIntegral.integral_const_mul]
        apply intervalIntegral.integral_congr; intro X _; ring
      have h2 : windowEnergyNormSq Y (fun X => (-r) * R X) = r ^ 2 * windowEnergyNormSq Y R := by
        unfold windowEnergyNormSq windowPairing
        rw [← intervalIntegral.integral_const_mul]
        apply intervalIntegral.integral_congr; intro X _; ring
      have h3 : windowPairing Y (fun X => α * LV X) (fun X => (-r) * R X) =
          -(α * r) * windowPairing Y LV R := by
        unfold windowPairing
        rw [← intervalIntegral.integral_const_mul]
        apply intervalIntegral.integral_congr; intro X _; ring
      rw [h1, h2, h3]; ring
    have h_2ar : 2 * α * r = 4 * (1 - r ^ 2) := by
      dsimp [α]; field_simp [ne_of_gt hr_pos]; ring
    have h_a2 : α ^ 2 * windowEnergyNormSq Y LV ≤ 4 * (1 - r ^ 2) * (S_V - windowEnergyNormSq Y LV) := by
      have h_alg : α ^ 2 * r ^ 2 = 4 * (1 - r ^ 2) ^ 2 := by
        dsimp [α]; field_simp [ne_of_gt hr_pos]; ring
      have h_step : (1 - r ^ 2) * windowEnergyNormSq Y LV ≤ r ^ 2 * (S_V - windowEnergyNormSq Y LV) := by
        linarith [h_contr]
      have h_step2 := mul_le_mul_of_nonneg_left h_step (show 0 ≤ 4 * (1 - r ^ 2) by linarith)
      have h_r2_pos : 0 < r ^ 2 := sq_pos_of_pos hr_pos
      have h_mul : (α ^ 2 * windowEnergyNormSq Y LV) * r ^ 2 ≤
          (4 * (1 - r ^ 2) * (S_V - windowEnergyNormSq Y LV)) * r ^ 2 := by
        have h_l : (α ^ 2 * windowEnergyNormSq Y LV) * r ^ 2 =
            (α ^ 2 * r ^ 2) * windowEnergyNormSq Y LV := by ring
        rw [h_l, h_alg]
        linarith [h_step2]
      exact le_of_mul_le_mul_right h_mul h_r2_pos
    have h_cross_le :
        4 * (1 - r ^ 2) * windowPairing Y LV R -
            4 * (1 - r ^ 2) * (S_V - windowEnergyNormSq Y LV) ≤
          r ^ 2 * windowEnergyNormSq Y R := by
      rw [h_2ar] at h_sq_exp
      linarith [h_sq_nn, h_sq_exp, h_a2]
    have h_div :
        4 * windowPairing Y LV R + windowEnergyNormSq Y R -
            4 * (S_V - windowEnergyNormSq Y LV) ≤
          windowEnergyNormSq Y R / (1 - r ^ 2) :=
      (le_div_iff h1mr2_pos).mpr (by linarith [h_cross_le])
    rw [h_budget]
    change 4 * windowPairing Y LV R + windowEnergyNormSq Y R - coreScalarDiagJA c_lam c_half T D0 Y -
        4 * (S_V - windowEnergyNormSq Y LV) ≤ _
    linarith

private theorem pointwiseSynthesisOp_norm_and_sharpness_tc065_aux {Y : ℝ} (hY2 : 2 ≤ Y) (T : ℕ) :
    (∀ (w v : ℕ × ℕ → ℝ → ℝ) {M : ℝ}, 0 ≤ M →
      (∀ pk ∈ primePowerPairsUpTo T, ContinuousOn (w pk) (Set.uIcc Y (RiemannScope.tau * Y))) →
      (∀ pk ∈ primePowerPairsUpTo T, ContinuousOn (v pk) (Set.uIcc Y (RiemannScope.tau * Y))) →
      (∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
        (∑ pk ∈ primePowerPairsUpTo T, (w pk X) ^ 2) ≤ M ^ 2) →
      windowEnergyNormSq Y (pointwiseSynthesisOp T w v) ≤
        M ^ 2 * (∑ pk ∈ primePowerPairsUpTo T, windowEnergyNormSq Y (v pk))) ∧
    (∀ w0 : ℕ × ℕ → ℝ,
      windowEnergyNormSq Y
          (pointwiseSynthesisOp T (fun pk _ => w0 pk) (fun pk _ => w0 pk)) =
        (∑ pk ∈ primePowerPairsUpTo T, (w0 pk) ^ 2) *
          (∑ pk ∈ primePowerPairsUpTo T, windowEnergyNormSq Y (fun _ => w0 pk))) := by
  obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc065_aux hY2
  refine ⟨?_, ?_⟩
  · intro w v M _ hw_c hv_c hM
    have hL_c : ContinuousOn (pointwiseSynthesisOp T w v) (Set.uIcc Y (RiemannScope.tau * Y)) :=
      continuousOn_finset_sum _ (fun pk hpk => (hw_c pk hpk).mul (hv_c pk hpk))
    have h_int_L :
        IntervalIntegrable
          (fun X => pointwiseSynthesisOp T w v X * pointwiseSynthesisOp T w v X / X)
          volume Y (RiemannScope.tau * Y) :=
      ((hL_c.mul hL_c).div continuousOn_id
        (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
    have h_int_v :
        ∀ pk ∈ primePowerPairsUpTo T,
          IntervalIntegrable (fun X => v pk X * v pk X / X) volume Y (RiemannScope.tau * Y) := by
      intro pk hpk
      exact (((hv_c pk hpk).mul (hv_c pk hpk)).div continuousOn_id
        (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
    have h_rhs_eq :
        M ^ 2 * (∑ pk ∈ primePowerPairsUpTo T, windowEnergyNormSq Y (v pk)) =
          ∫ X in Y..(RiemannScope.tau * Y),
            M ^ 2 * (∑ pk ∈ primePowerPairsUpTo T, (v pk X) ^ 2) / X := by
      unfold windowEnergyNormSq windowPairing
      rw [← intervalIntegral.integral_finset_sum h_int_v, ← intervalIntegral.integral_const_mul]
      apply intervalIntegral.integral_congr
      intro X _
      dsimp only
      rw [Finset.mul_sum, Finset.mul_sum, Finset.sum_div]
      apply Finset.sum_congr rfl
      intro pk _; ring
    rw [h_rhs_eq]
    unfold windowEnergyNormSq windowPairing
    apply intervalIntegral.integral_mono_on hle h_int_L
    · exact ((continuousOn_const.mul
        (continuousOn_finset_sum _ (fun pk hpk => (hv_c pk hpk).pow 2))).div continuousOn_id
        (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
    · intro X hX
      have hX_u : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
      have hX0 : 0 < X := (hprops X hX_u).2.1
      have h_cs :
          (pointwiseSynthesisOp T w v X) ^ 2 ≤
            (∑ pk ∈ primePowerPairsUpTo T, (w pk X) ^ 2) *
              (∑ pk ∈ primePowerPairsUpTo T, (v pk X) ^ 2) :=
        Finset.sum_mul_sq_le_sq_mul_sq (primePowerPairsUpTo T) (fun pk => w pk X) (fun pk => v pk X)
      have h_sq_le :
          pointwiseSynthesisOp T w v X * pointwiseSynthesisOp T w v X ≤
            M ^ 2 * ∑ pk ∈ primePowerPairsUpTo T, (v pk X) ^ 2 := by
        rw [← sq]
        exact le_trans h_cs
          (mul_le_mul_of_nonneg_right (hM X hX_u) (Finset.sum_nonneg (fun _ _ => sq_nonneg _)))
      exact div_le_div_of_nonneg_right h_sq_le (le_of_lt hX0)
  · intro w0
    let S := ∑ pk ∈ primePowerPairsUpTo T, (w0 pk) ^ 2
    have hL_pt :
        ∀ X : ℝ, pointwiseSynthesisOp T (fun pk _ => w0 pk) (fun pk _ => w0 pk) X = S := by
      intro X
      unfold pointwiseSynthesisOp
      dsimp [S]
      apply Finset.sum_congr rfl; intro pk _; ring
    have h_lhs :
        windowEnergyNormSq Y (pointwiseSynthesisOp T (fun pk _ => w0 pk) (fun pk _ => w0 pk)) =
          S ^ 2 * (∫ X in Y..(RiemannScope.tau * Y), (1 : ℝ) / X) := by
      unfold windowEnergyNormSq windowPairing
      rw [← intervalIntegral.integral_const_mul]
      apply intervalIntegral.integral_congr
      intro X _; dsimp only; rw [hL_pt X]; ring
    have h_rhs_each :
        ∀ pk ∈ primePowerPairsUpTo T,
          windowEnergyNormSq Y (fun _ => w0 pk) =
            (w0 pk) ^ 2 * (∫ X in Y..(RiemannScope.tau * Y), (1 : ℝ) / X) := by
      intro pk _
      unfold windowEnergyNormSq windowPairing
      rw [← intervalIntegral.integral_const_mul]
      apply intervalIntegral.integral_congr; intro X _; ring
    rw [h_lhs, Finset.sum_congr rfl h_rhs_each, ← Finset.sum_mul]
    dsimp [S]; ring

/-- **Theorem 3 (`TASK-TC-065` §4, Supporting Hilbert Residual Budget & Contraction Bound, Pointwise Synthesis Operator Norm & Constant-Weight Sharpness, and Universal Pointwise Synthesis Obstructions)**:
    1. *Supporting Hilbert algebra*:
       Exact residual budget for `dampedCoreDefectD` against any continuous synthesis proxy `LV`,
       and strict-contraction upper bound `dampedCoreDefectD ≤ ‖R‖_Y^2 / (1 - r^2) - J_A` when
       `0 ≤ r < 1` and `‖LV‖_Y^2 ≤ r^2 * ∑_{pk} ‖V_{pk}‖_Y^2`;
    2. *Pointwise synthesis operator norm & constant-weight tightness (`2 ≤ Y`)*:
       `‖L_w v‖_Y^2 ≤ M^2 * ∑_{pk} ‖v_{pk}‖_Y^2` whenever `∑_{pk} w(pk, X)^2 ≤ M^2` on `[Y, tau * Y]`,
       attained with equality for every constant-in-`X` weight profile `w0` at `v(pk, X) = w0(pk)`;
    3. *Universal pointwise synthesis obstructions (`2 ≤ Y`, `1 ≤ T`)*:
       - Channel-weight dilution `(√|P_act(T)| - r)^2 ≤ ∑_{pk ∈ P_act(T)} (1 - w pk)^2`;
       - Pointwise oracle residual lower bound
         `∫_Y^{tau*Y} max(0, |U_Y(X)| - 2 r ‖V_Y(X)‖_{l^2})^2 dX / X ≤ ‖U_Y - 2 L_w V_Y‖_Y^2`;
       - Exact unweighted `S1` residual budget in terms of `pairedPrimePowerSumP` and `pairedOpenCoreOscO`. -/
theorem arithmetic_synthesis_hilbert_budget_operator_norm_and_obstructions_tc065 :
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ (c_lam c_half : ℝ) (T D0 : ℕ) {LV : ℝ → ℝ},
      ContinuousOn LV (Set.uIcc Y (RiemannScope.tau * Y)) →
      let R := fun X => coreTotalScalarProfileU c_lam c_half T D0 X - 2 * LV X
      dampedCoreDefectD c_lam c_half T D0 Y =
          4 * windowPairing Y LV R + windowEnergyNormSq Y R -
            coreScalarDiagJA c_lam c_half T D0 Y -
            4 * ((∑ pk ∈ primePowerPairsUpTo T,
              windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV T pk X)) -
              windowEnergyNormSq Y LV) ∧
        (∀ {r : ℝ}, 0 ≤ r → r < 1 →
          windowEnergyNormSq Y LV ≤
            r ^ 2 * (∑ pk ∈ primePowerPairsUpTo T,
              windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV T pk X)) →
          dampedCoreDefectD c_lam c_half T D0 Y ≤
            windowEnergyNormSq Y R / (1 - r ^ 2) - coreScalarDiagJA c_lam c_half T D0 Y)) ∧
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ (T : ℕ),
      (∀ (w v : ℕ × ℕ → ℝ → ℝ) {M : ℝ}, 0 ≤ M →
        (∀ pk ∈ primePowerPairsUpTo T, ContinuousOn (w pk) (Set.uIcc Y (RiemannScope.tau * Y))) →
        (∀ pk ∈ primePowerPairsUpTo T, ContinuousOn (v pk) (Set.uIcc Y (RiemannScope.tau * Y))) →
        (∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
          (∑ pk ∈ primePowerPairsUpTo T, (w pk X) ^ 2) ≤ M ^ 2) →
        windowEnergyNormSq Y (pointwiseSynthesisOp T w v) ≤
          M ^ 2 * (∑ pk ∈ primePowerPairsUpTo T, windowEnergyNormSq Y (v pk))) ∧
      (∀ w0 : ℕ × ℕ → ℝ,
        windowEnergyNormSq Y
            (pointwiseSynthesisOp T (fun pk _ => w0 pk) (fun pk _ => w0 pk)) =
          (∑ pk ∈ primePowerPairsUpTo T, (w0 pk) ^ 2) *
            (∑ pk ∈ primePowerPairsUpTo T, windowEnergyNormSq Y (fun _ => w0 pk)))) ∧
    ((∀ (T : ℕ) (w : ℕ × ℕ → ℝ) {r : ℝ}, 0 ≤ r →
        (∑ pk ∈ activePairedPrimePowers T, (w pk) ^ 2) ≤ r ^ 2 →
        r ≤ Real.sqrt ((activePairedPrimePowers T).card : ℝ) →
        (Real.sqrt ((activePairedPrimePowers T).card : ℝ) - r) ^ 2 ≤
          ∑ pk ∈ activePairedPrimePowers T, (1 - w pk) ^ 2) ∧
      (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        (∀ (w : ℕ × ℕ → ℝ → ℝ) {r : ℝ}, 0 ≤ r →
          (∀ pk ∈ primePowerPairsUpTo T, ContinuousOn (w pk) (Set.uIcc Y (RiemannScope.tau * Y))) →
          (∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
            (∑ pk ∈ primePowerPairsUpTo T, (w pk X) ^ 2) ≤ r ^ 2) →
          (∫ X in Y..(RiemannScope.tau * Y),
              (max 0 (|coreTotalScalarProfileU c_lam c_half T D0 X| -
                2 * r * Real.sqrt (∑ pk ∈ primePowerPairsUpTo T,
                  (coreTotalFeatureVectorV T pk X) ^ 2))) ^ 2 / X) ≤
            windowEnergyNormSq Y
              (fun X => coreTotalScalarProfileU c_lam c_half T D0 X -
                2 * pointwiseSynthesisOp T w (coreTotalFeatureVectorV T) X)) ∧
        dampedCoreDefectD c_lam c_half T D0 Y =
          4 * (windowEnergyNormSq Y (pairedPrimePowerSumP T) -
              ∑ pk ∈ primePowerPairsUpTo T,
                windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV T pk X)) +
            windowEnergyNormSq Y (pairedOpenCoreOscO c_lam c_half T D0) -
            4 * windowPairing Y (pairedPrimePowerSumP T) (pairedOpenCoreOscO c_lam c_half T D0) -
            coreScalarDiagJA c_lam c_half T D0 Y)) := by
  refine ⟨fun {_} hY2 c_lam c_half T D0 {_} hLV =>
      hilbert_budget_and_contraction_tc065_aux hY2 c_lam c_half T D0 hLV,
    fun {_} hY2 T => pointwiseSynthesisOp_norm_and_sharpness_tc065_aux hY2 T,
    ?_, ?_⟩
  · intro T w r hr0 h_w2 hr_le
    let A := activePairedPrimePowers T
    let N : ℝ := (A.card : ℝ)
    let x : ℝ := Real.sqrt (∑ pk ∈ A, (w pk) ^ 2)
    have h_sum_nn : 0 ≤ ∑ pk ∈ A, (w pk) ^ 2 := Finset.sum_nonneg (fun _ _ => sq_nonneg _)
    have hx_nn : 0 ≤ x := Real.sqrt_nonneg _
    have hx_le_r : x ≤ r := by
      have h1 := Real.sqrt_le_sqrt h_w2
      rwa [Real.sqrt_sq hr0] at h1
    have hx_sq : x ^ 2 = ∑ pk ∈ A, (w pk) ^ 2 := Real.sq_sqrt h_sum_nn
    have h_cs : (∑ pk ∈ A, w pk) ^ 2 ≤ N * x ^ 2 := by
      have h1 := Finset.sum_mul_sq_le_sq_mul_sq A (fun _ => (1 : ℝ)) w
      simp only [one_mul, one_pow, Finset.sum_const, nsmul_eq_mul, mul_one] at h1
      rwa [← hx_sq] at h1
    have h_sum_le : (∑ pk ∈ A, w pk) ≤ Real.sqrt N * x := by
      have h_nx : N * x ^ 2 = (Real.sqrt N * x) ^ 2 := by
        rw [mul_pow, Real.sq_sqrt (Nat.cast_nonneg _)]
      rw [h_nx] at h_cs
      have h_abs : |∑ pk ∈ A, w pk| ≤ Real.sqrt N * x := by
        rw [← Real.sqrt_sq_eq_abs]
        exact le_trans (Real.sqrt_le_sqrt h_cs)
          (le_of_eq (Real.sqrt_sq (mul_nonneg (Real.sqrt_nonneg _) hx_nn)))
      exact le_trans (le_abs_self _) h_abs
    have h_exp :
        (∑ pk ∈ A, (1 - w pk) ^ 2) = N - 2 * (∑ pk ∈ A, w pk) + x ^ 2 := by
      have h_pt : ∀ pk ∈ A, (1 - w pk) ^ 2 = 1 - 2 * w pk + (w pk) ^ 2 := fun _ _ => by ring
      rw [Finset.sum_congr rfl h_pt, Finset.sum_add_distrib, Finset.sum_sub_distrib,
        Finset.sum_const, nsmul_eq_mul, mul_one, ← Finset.mul_sum, ← hx_sq]
    have h_ge_x : (Real.sqrt N - x) ^ 2 ≤ ∑ pk ∈ A, (1 - w pk) ^ 2 := by
      rw [h_exp]
      have hN : (Real.sqrt N) ^ 2 = N := Real.sq_sqrt (Nat.cast_nonneg _)
      nlinarith
    have h_mono : (Real.sqrt N - r) ^ 2 ≤ (Real.sqrt N - x) ^ 2 :=
      pow_le_pow_left (by linarith) (by linarith) 2
    exact le_trans h_mono h_ge_x
  · intro Y hY2 T hT1 D0 c_lam c_half
    obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc065_aux hY2
    have htau := tau_gt_one_and_lt_eight_tc065_aux.1
    obtain ⟨_, _, _, _, _, hU_c, hV_c, hP_c, _, _, _, _⟩ :=
      continuousOn_core_objects_tc065_aux hY2 htau c_lam c_half T D0
    refine ⟨?_, ?_⟩
    · intro w r hr0 hw_c hr_bd
      have hL_c :
          ContinuousOn (pointwiseSynthesisOp T w (coreTotalFeatureVectorV T))
            (Set.uIcc Y (RiemannScope.tau * Y)) :=
        continuousOn_finset_sum _ (fun pk hpk => (hw_c pk hpk).mul (hV_c pk))
      have hV2_c :
          ContinuousOn
            (fun X => Real.sqrt (∑ pk ∈ primePowerPairsUpTo T, (coreTotalFeatureVectorV T pk X) ^ 2))
            (Set.uIcc Y (RiemannScope.tau * Y)) :=
        (continuousOn_finset_sum _ (fun pk _ => (hV_c pk).pow 2)).sqrt
      have h_max_c :
          ContinuousOn
            (fun X => max 0 (|coreTotalScalarProfileU c_lam c_half T D0 X| -
              2 * r * Real.sqrt (∑ pk ∈ primePowerPairsUpTo T,
                (coreTotalFeatureVectorV T pk X) ^ 2)))
            (Set.uIcc Y (RiemannScope.tau * Y)) :=
        ((continuous_const (y := (0 : ℝ))).max continuous_id).comp_continuousOn
          (hU_c.abs.sub (continuousOn_const.mul hV2_c))
      have h_lhs_c :
          ContinuousOn
            (fun X =>
              (max 0 (|coreTotalScalarProfileU c_lam c_half T D0 X| -
                2 * r * Real.sqrt (∑ pk ∈ primePowerPairsUpTo T,
                  (coreTotalFeatureVectorV T pk X) ^ 2))) ^ 2 / X)
            (Set.uIcc Y (RiemannScope.tau * Y)) :=
        (h_max_c.pow 2).div continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1)
      have h_rhs_c :
          ContinuousOn
            (fun X =>
              (coreTotalScalarProfileU c_lam c_half T D0 X -
                2 * pointwiseSynthesisOp T w (coreTotalFeatureVectorV T) X) *
              (coreTotalScalarProfileU c_lam c_half T D0 X -
                2 * pointwiseSynthesisOp T w (coreTotalFeatureVectorV T) X) / X)
            (Set.uIcc Y (RiemannScope.tau * Y)) :=
        (((hU_c.sub (continuousOn_const.mul hL_c)).mul
          (hU_c.sub (continuousOn_const.mul hL_c))).div
          continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1))
      unfold windowEnergyNormSq windowPairing
      apply intervalIntegral.integral_mono_on hle h_lhs_c.intervalIntegrable h_rhs_c.intervalIntegrable
      intro X hX
      have hX_u : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
      have hX0 : 0 < X := (hprops X hX_u).2.1
      have h_cs := Finset.sum_mul_sq_le_sq_mul_sq (primePowerPairsUpTo T)
        (fun pk => w pk X) (fun pk => coreTotalFeatureVectorV T pk X)
      have hV_sq_nn : 0 ≤ ∑ pk ∈ primePowerPairsUpTo T, (coreTotalFeatureVectorV T pk X) ^ 2 :=
        Finset.sum_nonneg (fun _ _ => sq_nonneg _)
      have hL_sq :
          (pointwiseSynthesisOp T w (coreTotalFeatureVectorV T) X) ^ 2 ≤
            (r * Real.sqrt (∑ pk ∈ primePowerPairsUpTo T,
              (coreTotalFeatureVectorV T pk X) ^ 2)) ^ 2 := by
        rw [mul_pow, Real.sq_sqrt hV_sq_nn]
        exact le_trans h_cs (mul_le_mul_of_nonneg_right (hr_bd X hX_u) hV_sq_nn)
      have hL_abs :
          |pointwiseSynthesisOp T w (coreTotalFeatureVectorV T) X| ≤
            r * Real.sqrt (∑ pk ∈ primePowerPairsUpTo T,
              (coreTotalFeatureVectorV T pk X) ^ 2) := by
        rw [← Real.sqrt_sq_eq_abs]
        exact le_trans (Real.sqrt_le_sqrt hL_sq)
          (le_of_eq (Real.sqrt_sq (mul_nonneg hr0 (Real.sqrt_nonneg _))))
      have h_tri :
          |coreTotalScalarProfileU c_lam c_half T D0 X| -
              2 * |pointwiseSynthesisOp T w (coreTotalFeatureVectorV T) X| ≤
            |coreTotalScalarProfileU c_lam c_half T D0 X -
              2 * pointwiseSynthesisOp T w (coreTotalFeatureVectorV T) X| := by
        have h1 := abs_sub_abs_le_abs_sub (coreTotalScalarProfileU c_lam c_half T D0 X)
          (2 * pointwiseSynthesisOp T w (coreTotalFeatureVectorV T) X)
        rw [abs_mul, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 2)] at h1
        exact h1
      have h_max_le :
          max 0 (|coreTotalScalarProfileU c_lam c_half T D0 X| -
            2 * r * Real.sqrt (∑ pk ∈ primePowerPairsUpTo T,
              (coreTotalFeatureVectorV T pk X) ^ 2)) ≤
            |coreTotalScalarProfileU c_lam c_half T D0 X -
              2 * pointwiseSynthesisOp T w (coreTotalFeatureVectorV T) X| := by
        apply max_le (abs_nonneg _)
        linarith
      have h_sq_le := pow_le_pow_left (le_max_left 0 _) h_max_le 2
      rw [sq_abs] at h_sq_le
      rw [← sq]
      exact div_le_div_of_nonneg_right h_sq_le (le_of_lt hX0)
    · have h_bud := (hilbert_budget_and_contraction_tc065_aux hY2 c_lam c_half T D0 hP_c).1
      have hR_eq_negO :
          ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
            coreTotalScalarProfileU c_lam c_half T D0 X - 2 * pairedPrimePowerSumP T X =
              -pairedOpenCoreOscO c_lam c_half T D0 X := by
        intro X hX
        have h_u := ((paired_station_partition_divisor_synthesis_and_telescoping_tc065).2.2.2.1
          hY2 hT1 D0 c_lam c_half X hX).2.2.2.1
        linarith
      have h_norm_R :
          windowEnergyNormSq Y
              (fun X => coreTotalScalarProfileU c_lam c_half T D0 X - 2 * pairedPrimePowerSumP T X) =
            windowEnergyNormSq Y (pairedOpenCoreOscO c_lam c_half T D0) := by
        unfold windowEnergyNormSq windowPairing
        apply intervalIntegral.integral_congr
        intro X hX
        dsimp only
        rw [hR_eq_negO X hX]; ring
      have h_pair_R :
          windowPairing Y (pairedPrimePowerSumP T)
              (fun X => coreTotalScalarProfileU c_lam c_half T D0 X - 2 * pairedPrimePowerSumP T X) =
            -windowPairing Y (pairedPrimePowerSumP T) (pairedOpenCoreOscO c_lam c_half T D0) := by
        unfold windowPairing
        rw [← intervalIntegral.integral_neg]
        apply intervalIntegral.integral_congr
        intro X hX
        dsimp only
        rw [hR_eq_negO X hX]; ring
      rw [h_bud, h_norm_R, h_pair_R]
      ring

/-! ### Section 4: Coupled Mode Expansion, Uniform Fringe Bounds, Orthogonality, and Small-Core Bounds (`TASK-TC-065` §5–§6) -/

private theorem sum_inv_rpow_three_halves_le_two_tc065_aux (T : ℕ) :
    (∑ m ∈ Finset.Icc 2 T, (1 : ℝ) / ((m : ℝ) * Real.sqrt (m : ℝ))) ≤ 2 := by
  have h_each :
      ∀ m ∈ Finset.Icc 2 T,
        (1 : ℝ) / ((m : ℝ) * Real.sqrt (m : ℝ)) ≤
          2 * (1 / Real.sqrt ((m - 1 : ℕ) : ℝ) - 1 / Real.sqrt (m : ℝ)) := by
    intro m hm
    have hm2 : 2 ≤ m := (Finset.mem_Icc.mp hm).1
    have hm1 : 1 ≤ m - 1 := by omega
    have hm_pos : (0 : ℝ) < (m : ℝ) := Nat.cast_pos.mpr (by omega)
    have hm1_pos : (0 : ℝ) < ((m - 1 : ℕ) : ℝ) := Nat.cast_pos.mpr hm1
    have ha_pos : 0 < Real.sqrt ((m - 1 : ℕ) : ℝ) := Real.sqrt_pos.mpr hm1_pos
    have hb_pos : 0 < Real.sqrt (m : ℝ) := Real.sqrt_pos.mpr hm_pos
    have hab : Real.sqrt ((m - 1 : ℕ) : ℝ) ≤ Real.sqrt (m : ℝ) :=
      Real.sqrt_le_sqrt (by exact_mod_cast (show m - 1 ≤ m by omega))
    have h_diff_sq :
        (Real.sqrt (m : ℝ) - Real.sqrt ((m - 1 : ℕ) : ℝ)) *
          (Real.sqrt (m : ℝ) + Real.sqrt ((m - 1 : ℕ) : ℝ)) = 1 := by
      have hm_cast : ((m - 1 : ℕ) : ℝ) = (m : ℝ) - 1 := by
        rw [Nat.cast_sub (by omega : 1 ≤ m), Nat.cast_one]
      have hsq1 : Real.sqrt (m : ℝ) ^ 2 = (m : ℝ) := Real.sq_sqrt (le_of_lt hm_pos)
      have hsq2 : Real.sqrt ((m - 1 : ℕ) : ℝ) ^ 2 = (m : ℝ) - 1 := by
        rw [Real.sq_sqrt (le_of_lt hm1_pos), hm_cast]
      nlinarith
    have h_eq :
        2 * (1 / Real.sqrt ((m - 1 : ℕ) : ℝ) - 1 / Real.sqrt (m : ℝ)) =
          2 / (Real.sqrt ((m - 1 : ℕ) : ℝ) * Real.sqrt (m : ℝ) *
            (Real.sqrt (m : ℝ) + Real.sqrt ((m - 1 : ℕ) : ℝ))) := by
      have h_alg : ∀ a b : ℝ, 0 < a → 0 < b → (b - a) * (b + a) = 1 →
          2 * (1 / a - 1 / b) = 2 / (a * b * (b + a)) := by
        intro a b ha hb hba
        have hab_pos : 0 < b + a := by linarith
        field_simp [ne_of_gt ha, ne_of_gt hb, ne_of_gt hab_pos]
        linear_combination (2 * a * b) * hba
      exact h_alg _ _ ha_pos hb_pos h_diff_sq
    rw [h_eq]
    have h_den_pos :
        0 < Real.sqrt ((m - 1 : ℕ) : ℝ) * Real.sqrt (m : ℝ) *
          (Real.sqrt (m : ℝ) + Real.sqrt ((m - 1 : ℕ) : ℝ)) := by positivity
    have h_den_le :
        Real.sqrt ((m - 1 : ℕ) : ℝ) * Real.sqrt (m : ℝ) *
            (Real.sqrt (m : ℝ) + Real.sqrt ((m - 1 : ℕ) : ℝ)) ≤
          2 * ((m : ℝ) * Real.sqrt (m : ℝ)) := by
      have hsq_b : Real.sqrt (m : ℝ) * Real.sqrt (m : ℝ) = (m : ℝ) :=
        Real.mul_self_sqrt (le_of_lt hm_pos)
      nlinarith [mul_le_mul_of_nonneg_right hab (le_of_lt hb_pos)]
    have h_two_eq :
        (1 : ℝ) / ((m : ℝ) * Real.sqrt (m : ℝ)) = 2 / (2 * ((m : ℝ) * Real.sqrt (m : ℝ))) := by
      field_simp [ne_of_gt hm_pos, ne_of_gt hb_pos]
    rw [h_two_eq]
    exact div_le_div_of_nonneg_left (by norm_num) h_den_pos h_den_le
  calc
    (∑ m ∈ Finset.Icc 2 T, (1 : ℝ) / ((m : ℝ) * Real.sqrt (m : ℝ)))
      ≤ ∑ m ∈ Finset.Icc 2 T,
          2 * (1 / Real.sqrt ((m - 1 : ℕ) : ℝ) - 1 / Real.sqrt (m : ℝ)) :=
        Finset.sum_le_sum h_each
    _ = 2 * ∑ m ∈ Finset.Icc 2 T,
          (1 / Real.sqrt ((m - 1 : ℕ) : ℝ) - 1 / Real.sqrt (m : ℝ)) := (Finset.mul_sum _ _ _).symm
    _ ≤ 2 * 1 := by
        apply mul_le_mul_of_nonneg_left _ (by norm_num)
        induction T with
        | zero => simp
        | succ n ih =>
          by_cases hn1 : n = 0
          · subst hn1; simp
          · have hn_ge1 : 1 ≤ n := by omega
            have h_tele :
                ∀ N : ℕ, 1 ≤ N →
                  (∑ m ∈ Finset.Icc 2 N,
                      (1 / Real.sqrt ((m - 1 : ℕ) : ℝ) - 1 / Real.sqrt (m : ℝ))) =
                    1 - 1 / Real.sqrt (N : ℝ) := by
              intro N hN1
              induction N with
              | zero => omega
              | succ k ihk =>
                by_cases hk0 : k = 0
                · subst hk0; simp
                · have hk1 : 1 ≤ k := by omega
                  have h_s : Finset.Icc 2 (k + 1) = insert (k + 1) (Finset.Icc 2 k) := by
                    ext m; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
                  rw [h_s, Finset.sum_insert (by simp), ihk hk1]
                  simp only [Nat.add_sub_cancel]; ring
            rw [h_tele (n + 1) (by omega)]
            have h_nn : 0 ≤ 1 / Real.sqrt ((n + 1 : ℕ) : ℝ) := by positivity
            linarith
    _ = 2 := mul_one 2

private theorem log_sq_div_sq_sum_le_32_tc065_aux (T : ℕ) :
    (∑ m ∈ Finset.Icc 2 T, (Real.log (m : ℝ)) ^ 2 / (m : ℝ) ^ 2) ≤ 32 := by
  have h_each :
      ∀ m ∈ Finset.Icc 2 T,
        (Real.log (m : ℝ)) ^ 2 / (m : ℝ) ^ 2 ≤ 16 * ((1 : ℝ) / ((m : ℝ) * Real.sqrt (m : ℝ))) := by
    intro m hm
    have hm2 : 2 ≤ m := (Finset.mem_Icc.mp hm).1
    have hm_pos : (0 : ℝ) < (m : ℝ) := Nat.cast_pos.mpr (by omega)
    have hm_ge1 : (1 : ℝ) ≤ (m : ℝ) := by exact_mod_cast (by omega : 1 ≤ m)
    have hlog_nn : 0 ≤ Real.log (m : ℝ) := Real.log_nonneg hm_ge1
    have h_r4_pos : 0 < (m : ℝ) ^ (1 / 4 : ℝ) := Real.rpow_pos_of_pos hm_pos _
    have h_log_le : Real.log (m : ℝ) ≤ 4 * (m : ℝ) ^ (1 / 4 : ℝ) := by
      have h1 := Real.log_le_sub_one_of_pos h_r4_pos
      rw [Real.log_rpow hm_pos] at h1
      linarith
    have h_sq_le : (Real.log (m : ℝ)) ^ 2 ≤ 16 * Real.sqrt (m : ℝ) := by
      have hp := pow_le_pow_left hlog_nn h_log_le 2
      have hr : ((m : ℝ) ^ (1 / 4 : ℝ)) ^ 2 = Real.sqrt (m : ℝ) := by
        rw [Real.sqrt_eq_rpow, ← Real.rpow_natCast, ← Real.rpow_mul (le_of_lt hm_pos)]
        norm_num
      calc
        (Real.log (m : ℝ)) ^ 2 ≤ (4 * (m : ℝ) ^ (1 / 4 : ℝ)) ^ 2 := hp
        _ = 16 * ((m : ℝ) ^ (1 / 4 : ℝ)) ^ 2 := by ring
        _ = 16 * Real.sqrt (m : ℝ) := by rw [hr]
    have h_div := div_le_div_of_nonneg_right h_sq_le (sq_nonneg (m : ℝ))
    have h_rhs :
        16 * Real.sqrt (m : ℝ) / (m : ℝ) ^ 2 = 16 * ((1 : ℝ) / ((m : ℝ) * Real.sqrt (m : ℝ))) := by
      have hsq : Real.sqrt (m : ℝ) * Real.sqrt (m : ℝ) = (m : ℝ) :=
        Real.mul_self_sqrt (le_of_lt hm_pos)
      have hb_ne : Real.sqrt (m : ℝ) ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hm_pos)
      field_simp [ne_of_gt hm_pos, hb_ne]
      calc 16 * Real.sqrt (m : ℝ) * ((m : ℝ) * Real.sqrt (m : ℝ))
          = 16 * (m : ℝ) * (Real.sqrt (m : ℝ) * Real.sqrt (m : ℝ)) := by ring
        _ = 16 * (m : ℝ) ^ 2 := by rw [hsq]; ring
    rwa [h_rhs] at h_div
  calc
    (∑ m ∈ Finset.Icc 2 T, (Real.log (m : ℝ)) ^ 2 / (m : ℝ) ^ 2)
      ≤ ∑ m ∈ Finset.Icc 2 T, 16 * ((1 : ℝ) / ((m : ℝ) * Real.sqrt (m : ℝ))) :=
        Finset.sum_le_sum h_each
    _ = 16 * ∑ m ∈ Finset.Icc 2 T, (1 : ℝ) / ((m : ℝ) * Real.sqrt (m : ℝ)) :=
        (Finset.mul_sum _ _ _).symm
    _ ≤ 16 * 2 := mul_le_mul_of_nonneg_left (sum_inv_rpow_three_halves_le_two_tc065_aux T) (by norm_num)
    _ = 32 := by norm_num

private theorem sum_primePower_log_sq_div_sq_le_32_tc065_aux (T : ℕ) :
    (∑ pk ∈ primePowerPairsUpTo T,
        (Real.log (pk.1 : ℝ)) ^ 2 / ((pk.1 ^ pk.2 : ℕ) : ℝ) ^ 2) ≤ 32 := by
  have h_le_pow :
      (∑ pk ∈ primePowerPairsUpTo T,
          (Real.log (pk.1 : ℝ)) ^ 2 / ((pk.1 ^ pk.2 : ℕ) : ℝ) ^ 2) ≤
        ∑ pk ∈ primePowerPairsUpTo T,
          (Real.log ((pk.1 ^ pk.2 : ℕ) : ℝ)) ^ 2 / ((pk.1 ^ pk.2 : ℕ) : ℝ) ^ 2 := by
    apply Finset.sum_le_sum
    intro pk hpk
    simp only [primePowerPairsUpTo, primesUpToFinset, Finset.mem_filter, Finset.mem_product,
      Finset.mem_Icc] at hpk
    have hp : pk.1.Prime := hpk.1.1.2
    have hk1 : 1 ≤ pk.2 := hpk.1.2.1
    have h_le : pk.1 ≤ pk.1 ^ pk.2 := Nat.le_self_pow (Nat.ne_of_gt hk1) pk.1
    have hlog_le : Real.log (pk.1 : ℝ) ≤ Real.log ((pk.1 ^ pk.2 : ℕ) : ℝ) :=
      Real.log_le_log (Nat.cast_pos.mpr hp.pos) (by exact_mod_cast h_le)
    have hlog_nn : 0 ≤ Real.log (pk.1 : ℝ) := Real.log_nonneg (by exact_mod_cast (by omega : 1 ≤ pk.1))
    exact div_le_div_of_nonneg_right (pow_le_pow_left hlog_nn hlog_le 2) (sq_nonneg _)
  have h_inj :
      ∀ pk1 ∈ primePowerPairsUpTo T, ∀ pk2 ∈ primePowerPairsUpTo T,
        pk1.1 ^ pk1.2 = pk2.1 ^ pk2.2 → pk1 = pk2 := by
    intro pk1 hpk1 pk2 hpk2 h_eq
    simp only [primePowerPairsUpTo, primesUpToFinset, Finset.mem_filter,
      Finset.mem_product, Finset.mem_Icc] at hpk1 hpk2
    have hp1 : pk1.1.Prime := hpk1.1.1.2
    have hk1 : 1 ≤ pk1.2 := hpk1.1.2.1
    have hp2 : pk2.1.Prime := hpk2.1.1.2
    have hk2 : 1 ≤ pk2.2 := hpk2.1.2.1
    have hd : pk1.1 ∣ pk2.1 ^ pk2.2 := by rw [← h_eq]; exact dvd_pow_self pk1.1 (by omega)
    have hp_eq : pk1.1 = pk2.1 := by
      rcases hp2.eq_one_or_self_of_dvd pk1.1 (hp1.dvd_of_dvd_pow hd) with h1 | h2
      · exact False.elim (hp1.ne_one h1)
      · exact h2
    have hk_eq : pk1.2 = pk2.2 := by
      rw [hp_eq] at h_eq
      exact Nat.pow_right_injective hp2.two_le h_eq
    exact Prod.ext hp_eq hk_eq
  have h_img_sub :
      (primePowerPairsUpTo T).image (fun pk : ℕ × ℕ => pk.1 ^ pk.2) ⊆ Finset.Icc 2 T := by
    intro m hm
    rcases Finset.mem_image.mp hm with ⟨pk, hpk, rfl⟩
    simp only [primePowerPairsUpTo, primesUpToFinset, Finset.mem_filter, Finset.mem_product,
      Finset.mem_Icc] at hpk
    have hp2 : 2 ≤ pk.1 := hpk.1.1.2.two_le
    have hk1 : 1 ≤ pk.2 := hpk.1.2.1
    exact Finset.mem_Icc.mpr ⟨le_trans hp2 (Nat.le_self_pow (Nat.ne_of_gt hk1) pk.1), hpk.2⟩
  let f_m : ℕ → ℝ := fun m => (Real.log (m : ℝ)) ^ 2 / (m : ℝ) ^ 2
  have h_sum_img :
      (∑ pk ∈ primePowerPairsUpTo T, f_m (pk.1 ^ pk.2)) =
        ∑ m ∈ (primePowerPairsUpTo T).image (fun pk : ℕ × ℕ => pk.1 ^ pk.2), f_m m := by
    symm
    exact Finset.sum_image (fun a ha b hb h => h_inj a ha b hb h)
  have h_sum_sub :
      (∑ m ∈ (primePowerPairsUpTo T).image (fun pk : ℕ × ℕ => pk.1 ^ pk.2), f_m m) ≤
        ∑ m ∈ Finset.Icc 2 T, f_m m :=
    Finset.sum_le_sum_of_subset_of_nonneg h_img_sub (fun _ _ _ => div_nonneg (sq_nonneg _) (sq_nonneg _))
  exact le_trans h_le_pow (h_sum_img ▸ le_trans h_sum_sub (log_sq_div_sq_sum_le_32_tc065_aux T))

private theorem fringe_feature_paramWindowNormSq_bound_tc065_aux {w0 Y : ℝ} (hw0 : 1 < w0)
    (hY2 : 2 ≤ Y) :
    let T := canonicalCutoffT Y
    (∑ pk ∈ primePowerPairsUpTo T, paramWindowNormSq Y w0 (fringeFeatureVectorG T pk)) ≤
      (8192 * w0 ^ 5 * Real.log w0) / (Real.log Y) ^ 2 +
        (324 * w0 ^ 5 * Real.log w0) / Y ^ (5 / 4 : ℝ) := by
  intro T
  have hY0 : 0 < Y := by linarith
  have hw0_pos : 0 < w0 := lt_trans zero_lt_one hw0
  have hlogY_pos : 0 < Real.log Y := Real.log_pos (by linarith)
  have hlogw0_pos : 0 < Real.log w0 := Real.log_pos hw0
  have hT_ge_rpow : Y ^ (5 / 4 : ℝ) ≤ (T : ℝ) := Nat.le_ceil _
  have hT1 : 1 ≤ T := by
    have hpos : (0 : ℝ) < Y ^ (5 / 4 : ℝ) := Real.rpow_pos_of_pos hY0 _
    exact Nat.one_le_iff_ne_zero.mpr (Nat.ceil_pos.mpr hpos).ne'
  have hT_pos_r : (0 : ℝ) < (T : ℝ) := Nat.cast_pos.mpr hT1
  have hY5_le_T4 : Y ^ 5 ≤ (T : ℝ) ^ 4 := by
    have h1 := pow_le_pow_left (Real.rpow_nonneg (le_of_lt hY0) _) hT_ge_rpow 4
    have h2 : (Y ^ (5 / 4 : ℝ)) ^ 4 = Y ^ 5 := by
      rw [← Real.rpow_natCast, ← Real.rpow_mul (le_of_lt hY0)]
      norm_num
      exact_mod_cast Real.rpow_natCast Y 5
    rwa [h2] at h1
  obtain ⟨hle, hprops⟩ := uIcc_param_props_tc065_aux hY2 hw0
  obtain ⟨_, _, _, _, _, _, _, _, _, _, _, hGfr_c⟩ :=
    continuousOn_core_objects_tc065_aux hY2 hw0 0 0 T 0
  have h_each_pk :
      ∀ pk ∈ primePowerPairsUpTo T,
        paramWindowNormSq Y w0 (fringeFeatureVectorG T pk) ≤
          (64 * w0 ^ 5 * Real.log w0 / (Real.log Y) ^ 2) *
            ((Real.log (pk.1 : ℝ)) ^ 2 / ((pk.1 ^ pk.2 : ℕ) : ℝ) ^ 2) := by
    intro pk hpk
    simp only [primePowerPairsUpTo, primesUpToFinset, Finset.mem_filter, Finset.mem_product,
      Finset.mem_Icc] at hpk
    rcases hpk with ⟨⟨⟨⟨_hp2, _⟩, hp⟩, ⟨_hk1, _⟩⟩, _hpkT⟩
    let m := pk.1 ^ pk.2
    have hm1 : 1 ≤ m := Nat.one_le_pow pk.2 pk.1 hp.pos
    have hm_pos_r : (0 : ℝ) < (m : ℝ) := Nat.cast_pos.mpr hm1
    have hlogp_nn : 0 ≤ Real.log (pk.1 : ℝ) := Real.log_nonneg (by exact_mod_cast (by omega : 1 ≤ pk.1))
    let F_pk := (uncoveredCutoffStripStations 2 T).filter (fun n => m ∣ n)
    have hF_card : (F_pk.card : ℝ) ≤ (T : ℝ) / (m : ℝ) := by
      have h_sub : F_pk ⊆ (Finset.Icc 1 (T / m)).image (fun q => m * q) := by
        intro n hn
        simp only [F_pk, Finset.mem_filter] at hn
        have hn_Icc : n ∈ Finset.Icc 1 T := by
          have hu := (coveredInteriorStations_partition_and_char_tc065_aux T).1.2
          rw [← hu]; exact Finset.mem_union_right _ hn.1
        obtain ⟨hn1, hnT⟩ := Finset.mem_Icc.mp hn_Icc
        obtain ⟨q, rfl⟩ := hn.2
        have hq1 : 1 ≤ q := by
          rcases Nat.eq_zero_or_pos q with rfl | hpos
          · simp at hn1
          · exact hpos
        have hq_le : q ≤ T / m := (Nat.le_div_iff_mul_le hm1).mpr (by rw [mul_comm]; exact hnT)
        exact Finset.mem_image.mpr ⟨q, Finset.mem_Icc.mpr ⟨hq1, hq_le⟩, rfl⟩
      have hc1 : F_pk.card ≤ T / m := by
        calc F_pk.card ≤ ((Finset.Icc 1 (T / m)).image (fun q => m * q)).card := Finset.card_le_card h_sub
          _ ≤ (Finset.Icc 1 (T / m)).card := Finset.card_image_le
          _ = T / m := by simp
      calc (F_pk.card : ℝ) ≤ ((T / m : ℕ) : ℝ) := by exact_mod_cast hc1
        _ ≤ (T : ℝ) / (m : ℝ) := Nat.cast_div_le
    have h_pt_sq :
        ∀ X ∈ Set.Icc Y (w0 * Y),
          (fringeFeatureVectorG T pk X) ^ 2 ≤
            (64 * w0 ^ 5 / (Real.log Y) ^ 2) * ((Real.log (pk.1 : ℝ)) ^ 2 / (m : ℝ) ^ 2) := by
      intro X hX
      have hX_u : X ∈ Set.uIcc Y (w0 * Y) := by rwa [Set.uIcc_of_le hle]
      have hX0 : 0 < X := (hprops X hX_u).2.1
      have hlogX_ge : Real.log Y ≤ Real.log X := Real.log_le_log hY0 hX.1
      have h_rew :
          fringeFeatureVectorG T pk X =
            ∑ n ∈ F_pk, (liouvilleLambda n : ℝ) *
              (Real.log (pk.1 : ℝ) * gaussianTermPhi n X / Real.log X) := by
        unfold fringeFeatureVectorG stationPrimePowerFeatureG
        dsimp [F_pk, m]
        rw [Finset.sum_filter]
        apply Finset.sum_congr rfl
        intro n _; split_ifs <;> ring
      have h_each_n :
          ∀ n ∈ F_pk,
            |(liouvilleLambda n : ℝ) *
                (Real.log (pk.1 : ℝ) * gaussianTermPhi n X / Real.log X)| ≤
              Real.log (pk.1 : ℝ) * (8 * (w0 * Y) ^ (5 / 2 : ℝ) / (T : ℝ) ^ 3) / Real.log Y := by
        intro n hn
        simp only [F_pk, Finset.mem_filter] at hn
        have hn_Icc : n ∈ Finset.Icc 1 T := by
          have hu := (coveredInteriorStations_partition_and_char_tc065_aux T).1.2
          rw [← hu]; exact Finset.mem_union_right _ hn.1
        have hn1 : 1 ≤ n := (Finset.mem_Icc.mp hn_Icc).1
        have hn_pos_r : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr hn1
        have hT_lt_2n : T < 2 * n :=
          ((coveredInteriorStations_partition_and_char_tc065_aux T).2.2.1 n hn_Icc).mp hn.1 |>.2
        have h_inv_n : (n : ℝ)⁻¹ ≤ 2 / (T : ℝ) := by
          have hT_le_2n : (T : ℝ) ≤ 2 * (n : ℝ) := by exact_mod_cast (le_of_lt hT_lt_2n)
          rw [inv_eq_one_div, div_le_div_iff hn_pos_r hT_pos_r]
          linarith
        have h_inv_n3 : ((n : ℝ) ^ 3)⁻¹ ≤ 8 / (T : ℝ) ^ 3 := by
          have hp3 := pow_le_pow_left (inv_nonneg.mpr (le_of_lt hn_pos_r)) h_inv_n 3
          rw [inv_pow] at hp3
          calc ((n : ℝ) ^ 3)⁻¹ ≤ (2 / (T : ℝ)) ^ 3 := hp3
            _ = 8 / (T : ℝ) ^ 3 := by ring
        have h_phi_nn : 0 ≤ gaussianTermPhi n X := by
          unfold gaussianTermPhi
          exact mul_nonneg (Real.rpow_nonneg (le_of_lt hX0) _)
            (mul_nonneg (inv_nonneg.mpr (pow_nonneg (le_of_lt hn_pos_r) 3))
              (le_of_lt (Real.exp_pos _)))
        have h_phi_le : gaussianTermPhi n X ≤ 8 * (w0 * Y) ^ (5 / 2 : ℝ) / (T : ℝ) ^ 3 := by
          unfold gaussianTermPhi
          have hexp : Real.exp (-(X ^ 2) / (n : ℝ) ^ 2) ≤ 1 := by
            rw [Real.exp_le_one_iff]
            exact div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg X)) (sq_nonneg _)
          have hX52 : X ^ (5 / 2 : ℝ) ≤ (w0 * Y) ^ (5 / 2 : ℝ) :=
            Real.rpow_le_rpow (le_of_lt hX0) hX.2 (by norm_num)
          calc
            X ^ (5 / 2 : ℝ) * (((n : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (n : ℝ) ^ 2))
              ≤ (w0 * Y) ^ (5 / 2 : ℝ) * ((8 / (T : ℝ) ^ 3) * 1) :=
                mul_le_mul hX52
                  (mul_le_mul h_inv_n3 hexp (le_of_lt (Real.exp_pos _)) (by positivity))
                  (by positivity) (by positivity)
            _ = 8 * (w0 * Y) ^ (5 / 2 : ℝ) / (T : ℝ) ^ 3 := by ring
        rw [abs_mul, (liouvilleLambda_props_tc065_aux.2.1 hn1).2, one_mul,
          abs_of_nonneg (div_nonneg (mul_nonneg hlogp_nn h_phi_nn) (by linarith))]
        exact div_le_div (mul_nonneg hlogp_nn (by positivity))
          (mul_le_mul_of_nonneg_left h_phi_le hlogp_nn) hlogY_pos hlogX_ge
      have h_abs :
          |fringeFeatureVectorG T pk X| ≤
            (8 * (w0 * Y) ^ (5 / 2 : ℝ) / ((T : ℝ) ^ 2 * Real.log Y)) *
              (Real.log (pk.1 : ℝ) / (m : ℝ)) := by
        rw [h_rew]
        calc
          |∑ n ∈ F_pk, (liouvilleLambda n : ℝ) *
              (Real.log (pk.1 : ℝ) * gaussianTermPhi n X / Real.log X)|
            ≤ ∑ n ∈ F_pk, |(liouvilleLambda n : ℝ) *
                (Real.log (pk.1 : ℝ) * gaussianTermPhi n X / Real.log X)| :=
              Finset.abs_sum_le_sum_abs _ _
          _ ≤ ∑ _n ∈ F_pk,
                Real.log (pk.1 : ℝ) * (8 * (w0 * Y) ^ (5 / 2 : ℝ) / (T : ℝ) ^ 3) / Real.log Y :=
              Finset.sum_le_sum h_each_n
          _ = (F_pk.card : ℝ) *
                (Real.log (pk.1 : ℝ) * (8 * (w0 * Y) ^ (5 / 2 : ℝ) / (T : ℝ) ^ 3) / Real.log Y) := by
              rw [Finset.sum_const, nsmul_eq_mul]
          _ ≤ ((T : ℝ) / (m : ℝ)) *
                (Real.log (pk.1 : ℝ) * (8 * (w0 * Y) ^ (5 / 2 : ℝ) / (T : ℝ) ^ 3) / Real.log Y) :=
              mul_le_mul_of_nonneg_right hF_card (by positivity)
          _ = (8 * (w0 * Y) ^ (5 / 2 : ℝ) / ((T : ℝ) ^ 2 * Real.log Y)) *
                (Real.log (pk.1 : ℝ) / (m : ℝ)) := by
              field_simp [ne_of_gt hT_pos_r, ne_of_gt hm_pos_r, ne_of_gt hlogY_pos]; ring
      have h_sq_abs := pow_le_pow_left (abs_nonneg _) h_abs 2
      rw [sq_abs] at h_sq_abs
      have hwY5 : ((w0 * Y) ^ (5 / 2 : ℝ)) ^ 2 = w0 ^ 5 * Y ^ 5 := by
        rw [← Real.rpow_natCast, ← Real.rpow_mul (by positivity)]
        norm_num
        rw [Real.mul_rpow (le_of_lt hw0_pos) (le_of_lt hY0)]
        have h1 : w0 ^ (5 : ℝ) = w0 ^ 5 := by exact_mod_cast Real.rpow_natCast w0 5
        have h2 : Y ^ (5 : ℝ) = Y ^ 5 := by exact_mod_cast Real.rpow_natCast Y 5
        rw [h1, h2]
      calc
        (fringeFeatureVectorG T pk X) ^ 2
          ≤ ((8 * (w0 * Y) ^ (5 / 2 : ℝ) / ((T : ℝ) ^ 2 * Real.log Y)) *
              (Real.log (pk.1 : ℝ) / (m : ℝ))) ^ 2 := h_sq_abs
        _ = (64 * w0 ^ 5 / (Real.log Y) ^ 2) * (Y ^ 5 / (T : ℝ) ^ 4) *
              ((Real.log (pk.1 : ℝ)) ^ 2 / (m : ℝ) ^ 2) := by
            rw [mul_pow, div_pow, mul_pow, hwY5]; ring
        _ ≤ (64 * w0 ^ 5 / (Real.log Y) ^ 2) * 1 *
              ((Real.log (pk.1 : ℝ)) ^ 2 / (m : ℝ) ^ 2) := by
            have h_rat : Y ^ 5 / (T : ℝ) ^ 4 ≤ 1 := (div_le_one (pow_pos hT_pos_r 4)).mpr hY5_le_T4
            exact mul_le_mul_of_nonneg_right
              (mul_le_mul_of_nonneg_left h_rat (by positivity)) (by positivity)
        _ = (64 * w0 ^ 5 / (Real.log Y) ^ 2) * ((Real.log (pk.1 : ℝ)) ^ 2 / (m : ℝ) ^ 2) := by ring
    let C_pk := (64 * w0 ^ 5 / (Real.log Y) ^ 2) * ((Real.log (pk.1 : ℝ)) ^ 2 / (m : ℝ) ^ 2)
    have h_int_lhs :
        IntervalIntegrable (fun X => fringeFeatureVectorG T pk X * fringeFeatureVectorG T pk X / X)
          volume Y (w0 * Y) :=
      (((hGfr_c pk).mul (hGfr_c pk)).div continuousOn_id
        (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
    have h_int_rhs :
        IntervalIntegrable (fun X => C_pk * ((1 : ℝ) / X)) volume Y (w0 * Y) :=
      (continuousOn_const.mul (continuousOn_const.div continuousOn_id
        (fun X hX => ne_of_gt (hprops X hX).2.1))).intervalIntegrable
    unfold paramWindowNormSq paramWindowPairing
    calc
      (∫ X in Y..(w0 * Y), fringeFeatureVectorG T pk X * fringeFeatureVectorG T pk X / X)
        ≤ ∫ X in Y..(w0 * Y), C_pk * ((1 : ℝ) / X) := by
          apply intervalIntegral.integral_mono_on hle h_int_lhs h_int_rhs
          intro X hX
          have hX0 : 0 < X := lt_of_lt_of_le hY0 hX.1
          have h1 := div_le_div_of_nonneg_right (h_pt_sq X hX) (le_of_lt hX0)
          rwa [sq, show C_pk / X = C_pk * ((1 : ℝ) / X) by ring] at h1
      _ = C_pk * ∫ X in Y..(w0 * Y), (1 : ℝ) / X := intervalIntegral.integral_const_mul _ _
      _ = C_pk * Real.log w0 := by rw [intervalIntegral_inv_param_tc065_aux hY0 hw0]
      _ = (64 * w0 ^ 5 * Real.log w0 / (Real.log Y) ^ 2) *
            ((Real.log (pk.1 : ℝ)) ^ 2 / ((pk.1 ^ pk.2 : ℕ) : ℝ) ^ 2) := by
          dsimp [C_pk, m]; ring
  have h_sum_pp :
      (∑ pk ∈ primePowerPairsUpTo T,
          (Real.log (pk.1 : ℝ)) ^ 2 / ((pk.1 ^ pk.2 : ℕ) : ℝ) ^ 2) ≤ 32 :=
    sum_primePower_log_sq_div_sq_le_32_tc065_aux T
  have h_extra_nn : 0 ≤ (324 * w0 ^ 5 * Real.log w0) / Y ^ (5 / 4 : ℝ) := by positivity
  calc
    (∑ pk ∈ primePowerPairsUpTo T, paramWindowNormSq Y w0 (fringeFeatureVectorG T pk))
      ≤ ∑ pk ∈ primePowerPairsUpTo T,
          (64 * w0 ^ 5 * Real.log w0 / (Real.log Y) ^ 2) *
            ((Real.log (pk.1 : ℝ)) ^ 2 / ((pk.1 ^ pk.2 : ℕ) : ℝ) ^ 2) :=
        Finset.sum_le_sum h_each_pk
    _ = (64 * w0 ^ 5 * Real.log w0 / (Real.log Y) ^ 2) *
          ∑ pk ∈ primePowerPairsUpTo T,
            (Real.log (pk.1 : ℝ)) ^ 2 / ((pk.1 ^ pk.2 : ℕ) : ℝ) ^ 2 :=
        (Finset.mul_sum _ _ _).symm
    _ ≤ (64 * w0 ^ 5 * Real.log w0 / (Real.log Y) ^ 2) * 32 :=
        mul_le_mul_of_nonneg_left h_sum_pp (by positivity)
    _ = (2048 * w0 ^ 5 * Real.log w0) / (Real.log Y) ^ 2 := by ring
    _ ≤ (8192 * w0 ^ 5 * Real.log w0) / (Real.log Y) ^ 2 := by
        apply div_le_div_of_nonneg_right _ (sq_nonneg _)
        have hpos : 0 ≤ w0 ^ 5 * Real.log w0 := by positivity
        linarith
    _ ≤ (8192 * w0 ^ 5 * Real.log w0) / (Real.log Y) ^ 2 +
          (324 * w0 ^ 5 * Real.log w0) / Y ^ (5 / 4 : ℝ) := by linarith

private theorem sum_inv_Icc_le_one_add_log_tc065_aux {T : ℕ} (hT1 : 1 ≤ T) :
    (∑ e ∈ Finset.Icc 1 T, (1 : ℝ) / (e : ℝ)) ≤ 1 + Real.log (T : ℝ) := by
  induction T with
  | zero => omega
  | succ n ih =>
    by_cases hn0 : n = 0
    · subst hn0; simp
    · have hn1 : 1 ≤ n := by omega
      have h_icc : Finset.Icc 1 (n + 1) = insert (n + 1) (Finset.Icc 1 n) := by
        ext k; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
      rw [h_icc, Finset.sum_insert (by simp)]
      have hn_pos : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr hn1
      have hn1_pos : (0 : ℝ) < ((n + 1 : ℕ) : ℝ) := Nat.cast_pos.mpr (by omega)
      have h_step : (1 : ℝ) / ((n + 1 : ℕ) : ℝ) ≤ Real.log ((n + 1 : ℕ) : ℝ) - Real.log (n : ℝ) := by
        have h1 := Real.log_le_sub_one_of_pos (div_pos hn_pos hn1_pos)
        rw [Real.log_div (ne_of_gt hn_pos) (ne_of_gt hn1_pos)] at h1
        have h_sub : (n : ℝ) / ((n + 1 : ℕ) : ℝ) - 1 = -(1 / ((n + 1 : ℕ) : ℝ)) := by
          push_cast; field_simp [ne_of_gt hn1_pos]
        rw [h_sub] at h1
        linarith
      linarith [ih hn1]

private theorem log_canonicalCutoffT_bounds_tc065_aux {Y : ℝ} (hY2 : 2 ≤ Y) :
    let T := canonicalCutoffT Y
    1 ≤ T ∧
      (1 / 2 : ℝ) < Real.log Y ∧
      Real.log (T : ℝ) ≤ (9 / 4 : ℝ) * Real.log Y ∧
      1 + Real.log (T : ℝ) ≤ 5 * Real.log Y := by
  intro T
  have hY0 : 0 < Y := by linarith
  have hT1 : 1 ≤ T := by
    have hpos : (0 : ℝ) < Y ^ (5 / 4 : ℝ) := Real.rpow_pos_of_pos hY0 _
    exact Nat.one_le_iff_ne_zero.mpr (Nat.ceil_pos.mpr hpos).ne'
  have h_log2 : (1 / 2 : ℝ) < Real.log 2 := by
    have h_inv8 : (7 / 8 : ℝ) ≤ Real.exp (-(1 / 8 : ℝ)) := by
      linarith [Real.add_one_le_exp (-(1 / 8 : ℝ))]
    have h_prod : Real.exp (1 / 8 : ℝ) * Real.exp (-(1 / 8 : ℝ)) = 1 := by
      rw [← Real.exp_add, add_neg_self, Real.exp_zero]
    have he8_le : Real.exp (1 / 8 : ℝ) ≤ 8 / 7 := by
      have hm := mul_le_mul_of_nonneg_left h_inv8 (le_of_lt (Real.exp_pos (1 / 8 : ℝ)))
      rw [h_prod] at hm; linarith
    have he_half_eq : (Real.exp (1 / 8 : ℝ)) ^ 4 = Real.exp (1 / 2 : ℝ) := by
      calc (Real.exp (1 / 8 : ℝ)) ^ 4
          = Real.exp (1 / 8 : ℝ) * Real.exp (1 / 8 : ℝ) *
              Real.exp (1 / 8 : ℝ) * Real.exp (1 / 8 : ℝ) := by ring
        _ = Real.exp (1 / 2 : ℝ) := by rw [← Real.exp_add, ← Real.exp_add, ← Real.exp_add]; congr 1; ring
    have hp4 : Real.exp (1 / 2 : ℝ) < 2 := by
      have h1 := pow_le_pow_left (le_of_lt (Real.exp_pos _)) he8_le 4
      rw [he_half_eq] at h1
      have hnum : (8 / 7 : ℝ) ^ 4 < 2 := by norm_num
      exact lt_of_le_of_lt h1 hnum
    have h2 := Real.log_lt_log (Real.exp_pos (1 / 2 : ℝ)) hp4
    rwa [Real.log_exp] at h2
  have h_logY : (1 / 2 : ℝ) < Real.log Y := lt_of_lt_of_le h_log2 (Real.log_le_log (by norm_num) hY2)
  have hT_le_rpow : (T : ℝ) ≤ Y ^ (9 / 4 : ℝ) := by
    have h1 : (T : ℝ) < Y ^ (5 / 4 : ℝ) + 1 := Nat.ceil_lt_add_one (Real.rpow_nonneg (le_of_lt hY0) _)
    have hY1_le : (1 : ℝ) ≤ Y ^ (5 / 4 : ℝ) := Real.one_le_rpow (by linarith) (by norm_num)
    have h3 : 2 * Y ^ (5 / 4 : ℝ) ≤ Y * Y ^ (5 / 4 : ℝ) :=
      mul_le_mul_of_nonneg_right hY2 (Real.rpow_nonneg (le_of_lt hY0) _)
    have h4 : Y * Y ^ (5 / 4 : ℝ) = Y ^ (9 / 4 : ℝ) := by
      have hadd : Y ^ ((1 : ℝ) + (5 / 4 : ℝ)) = Y ^ (1 : ℝ) * Y ^ (5 / 4 : ℝ) :=
        Real.rpow_add hY0 1 (5 / 4 : ℝ)
      rw [Real.rpow_one] at hadd
      rw [← hadd]; norm_num
    linarith
  have h_logT : Real.log (T : ℝ) ≤ (9 / 4 : ℝ) * Real.log Y := by
    have h1 := Real.log_le_log (Nat.cast_pos.mpr hT1) hT_le_rpow
    rwa [Real.log_rpow hY0] at h1
  refine ⟨hT1, h_logY, h_logT, ?_⟩
  linarith

private theorem abs_R_osc_le_tc065_aux (c_lam c_half : ℝ) {d : ℕ} (hd1 : 1 ≤ d) :
    |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| ≤
      (5 + |c_lam| + |c_half|) * (d : ℝ) * (1 + Real.log (d : ℝ)) ^ 2 := by
  have hd_pos : (0 : ℝ) < (d : ℝ) := Nat.cast_pos.mpr hd1
  have hd_ge1 : (1 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd1
  have hlogd_nn : 0 ≤ Real.log (d : ℝ) := Real.log_nonneg hd_ge1
  have h_w2 := (spillover_fringe_reindexing_and_mixed_covariance_reduction_tc062).2.1.2 hd1
  have h_sqd_le : Real.sqrt (d : ℝ) ≤ (d : ℝ) := by
    have hd_le_sq : (d : ℝ) ≤ (d : ℝ) ^ 2 := by
      rw [sq]; exact le_mul_of_one_le_left (le_of_lt hd_pos) hd_ge1
    have h1 := Real.sqrt_le_sqrt hd_le_sq
    rwa [Real.sqrt_sq (le_of_lt hd_pos)] at h1
  have h_M2 : |squarePoleDriftM c_half d| ≤ (4 + |c_half|) * (d : ℝ) * (1 + Real.log (d : ℝ)) := by
    unfold squarePoleDriftM
    rw [if_neg (by omega)]
    calc
      |4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ) + c_half * Real.sqrt (d : ℝ)|
        ≤ |4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ)| + |c_half * Real.sqrt (d : ℝ)| :=
          abs_add _ _
      _ = 4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ) + |c_half| * Real.sqrt (d : ℝ) := by
          rw [abs_mul, abs_mul, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 4),
            abs_of_nonneg (Real.sqrt_nonneg _), abs_of_nonneg hlogd_nn,
            abs_mul, abs_of_nonneg (Real.sqrt_nonneg _)]
      _ ≤ 4 * (d : ℝ) * Real.log (d : ℝ) + |c_half| * (d : ℝ) := by gcongr
      _ ≤ (4 + |c_half|) * (d : ℝ) * (1 + Real.log (d : ℝ)) := by
          have h2 : 0 ≤ |c_half| * (d : ℝ) * Real.log (d : ℝ) := by positivity
          linarith
  have h_step1 :
      |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| ≤
        |selbergCumulativeW2 d| + |c_lam| * (d : ℝ) + |squarePoleDriftM c_half d| := by
    unfold selbergCenteredRemainderInt
    calc
      |selbergCumulativeW2 d - c_lam * (d : ℝ) - squarePoleDriftM c_half d|
        ≤ |selbergCumulativeW2 d - c_lam * (d : ℝ)| + |squarePoleDriftM c_half d| := abs_sub _ _
      _ ≤ (|selbergCumulativeW2 d| + |c_lam * (d : ℝ)|) + |squarePoleDriftM c_half d| :=
          add_le_add_right (abs_sub _ _) _
      _ = |selbergCumulativeW2 d| + |c_lam| * (d : ℝ) + |squarePoleDriftM c_half d| := by
          rw [abs_mul, abs_of_nonneg (le_of_lt hd_pos)]
  have h_log2_le : (Real.log (d : ℝ)) ^ 2 ≤ (1 + Real.log (d : ℝ)) ^ 2 := by nlinarith
  have h_1log_le : 1 + Real.log (d : ℝ) ≤ (1 + Real.log (d : ℝ)) ^ 2 := by nlinarith
  have h_1_le : 1 ≤ (1 + Real.log (d : ℝ)) ^ 2 := by nlinarith
  have hw_le : (d : ℝ) * (Real.log (d : ℝ)) ^ 2 ≤ (d : ℝ) * (1 + Real.log (d : ℝ)) ^ 2 :=
    mul_le_mul_of_nonneg_left h_log2_le (le_of_lt hd_pos)
  have hc_le : |c_lam| * (d : ℝ) ≤ |c_lam| * (d : ℝ) * (1 + Real.log (d : ℝ)) ^ 2 :=
    le_mul_of_one_le_right (by positivity) h_1_le
  have hm_le : (4 + |c_half|) * (d : ℝ) * (1 + Real.log (d : ℝ)) ≤
      (4 + |c_half|) * (d : ℝ) * (1 + Real.log (d : ℝ)) ^ 2 :=
    mul_le_mul_of_nonneg_left h_1log_le (by positivity)
  linarith [h_step1, h_w2, h_M2, hw_le, hc_le, hm_le]

private theorem scalar_fringe_uniform_bound_tc065_aux (c_lam c_half : ℝ) :
    ∃ C_fr : ℝ, 0 ≤ C_fr ∧
      ∀ {Y : ℝ}, 2 ≤ Y →
        windowEnergyNormSq Y
            (pairedCutoffFringeScalarPhi c_lam c_half (canonicalCutoffT Y) (Nat.floor (Real.log Y))) ≤
          C_fr := by
  let C_R : ℝ := 5 + |c_lam| + |c_half|
  have hCR_nn : 0 ≤ C_R := by dsimp [C_R]; positivity
  let B_coeff : ℝ := 1 + 6 + 6 + 10 * |c_lam| + 30 * (8 + |c_half|) + 50 * C_R
  let B_fr : ℝ := 8 * RiemannScope.tau ^ (5 / 2 : ℝ) * B_coeff
  have htau := tau_gt_one_and_lt_eight_tc065_aux.1
  have htau_pos : 0 < RiemannScope.tau := lt_trans zero_lt_one htau
  refine ⟨B_fr ^ 2 * Real.log RiemannScope.tau,
    mul_nonneg (sq_nonneg _) (Real.log_nonneg (le_of_lt htau)), ?_⟩
  intro Y hY2
  let T := canonicalCutoffT Y
  let D0 := Nat.floor (Real.log Y)
  let D_eff := min D0 (T - 1)
  let R_osc : ℕ → ℝ := fun d => selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d
  have hY0 : 0 < Y := by linarith
  obtain ⟨hT1, hlogY_gt_half, hlogT_le, h1logT_le⟩ := log_canonicalCutoffT_bounds_tc065_aux hY2
  have hT_pos_r : (0 : ℝ) < (T : ℝ) := Nat.cast_pos.mpr hT1
  have hlogY_pos : 0 < Real.log Y := by linarith
  have hT_ge_rpow : Y ^ (5 / 4 : ℝ) ≤ (T : ℝ) := Nat.le_ceil _
  have hY52_le_T2 : Y ^ (5 / 2 : ℝ) ≤ (T : ℝ) ^ 2 := by
    have h1 := pow_le_pow_left (Real.rpow_nonneg (le_of_lt hY0) _) hT_ge_rpow 2
    have h2 : (Y ^ (5 / 4 : ℝ)) ^ 2 = Y ^ (5 / 2 : ℝ) := by
      rw [← Real.rpow_natCast, ← Real.rpow_mul (le_of_lt hY0)]; norm_num
    rwa [h2] at h1
  have h_R_osc_bd : ∀ {d : ℕ}, 1 ≤ d → |R_osc d| ≤ C_R * (d : ℝ) * (1 + Real.log (d : ℝ)) ^ 2 :=
    fun hd1 => abs_R_osc_le_tc065_aux c_lam c_half hd1
  have h_logT_rat : (Real.log (T : ℝ) / Real.log Y) ^ 2 ≤ 6 := by
    have h_nn : 0 ≤ Real.log (T : ℝ) / Real.log Y :=
      div_nonneg (Real.log_nonneg (by exact_mod_cast hT1)) (le_of_lt hlogY_pos)
    have h_le : Real.log (T : ℝ) / Real.log Y ≤ 9 / 4 := (div_le_iff hlogY_pos).mpr hlogT_le
    calc (Real.log (T : ℝ) / Real.log Y) ^ 2 ≤ (9 / 4 : ℝ) ^ 2 := pow_le_pow_left h_nn h_le 2
      _ ≤ 6 := by norm_num
  have h_1logT_rat : ((1 + Real.log (T : ℝ)) / Real.log Y) ^ 2 ≤ 25 := by
    have h_nn : 0 ≤ (1 + Real.log (T : ℝ)) / Real.log Y :=
      div_nonneg (add_nonneg zero_le_one (Real.log_nonneg (by exact_mod_cast hT1))) (le_of_lt hlogY_pos)
    have h_le : (1 + Real.log (T : ℝ)) / Real.log Y ≤ 5 := (div_le_iff hlogY_pos).mpr h1logT_le
    calc ((1 + Real.log (T : ℝ)) / Real.log Y) ^ 2 ≤ 5 ^ 2 := pow_le_pow_left h_nn h_le 2
      _ = 25 := by norm_num
  have h_1logT_over_logY2 : (1 + Real.log (T : ℝ)) / (Real.log Y) ^ 2 ≤ 10 := by
    have h1 : (1 + Real.log (T : ℝ)) / Real.log Y ≤ 5 := (div_le_iff hlogY_pos).mpr h1logT_le
    have h2 : 1 / Real.log Y ≤ 2 := by
      rw [div_le_iff hlogY_pos]; linarith
    have h_eq : (1 + Real.log (T : ℝ)) / (Real.log Y) ^ 2 =
        ((1 + Real.log (T : ℝ)) / Real.log Y) * (1 / Real.log Y) := by ring
    rw [h_eq]
    calc ((1 + Real.log (T : ℝ)) / Real.log Y) * (1 / Real.log Y) ≤ 5 * 2 :=
          mul_le_mul h1 h2 (by positivity) (by norm_num)
      _ = 10 := by norm_num
  have h_mult_card :
      ∀ {e : ℕ}, 1 ≤ e →
        (((Finset.Icc 1 T).filter (fun n => e ∣ n)).card : ℝ) ≤ (T : ℝ) / (e : ℝ) := by
    intro e he1
    have h_sub : (Finset.Icc 1 T).filter (fun n => e ∣ n) ⊆
        (Finset.Icc 1 (T / e)).image (fun q => e * q) := by
      intro n hn
      simp only [Finset.mem_filter, Finset.mem_Icc] at hn
      obtain ⟨⟨hn1, hnT⟩, ⟨q, rfl⟩⟩ := hn
      have hq1 : 1 ≤ q := by
        rcases Nat.eq_zero_or_pos q with rfl | hp
        · simp at hn1
        · exact hp
      have hq_le : q ≤ T / e := (Nat.le_div_iff_mul_le he1).mpr (by rw [mul_comm]; exact hnT)
      exact Finset.mem_image.mpr ⟨q, Finset.mem_Icc.mpr ⟨hq1, hq_le⟩, rfl⟩
    have hc : ((Finset.Icc 1 T).filter (fun n => e ∣ n)).card ≤ T / e := by
      calc _ ≤ ((Finset.Icc 1 (T / e)).image (fun q => e * q)).card := Finset.card_le_card h_sub
        _ ≤ (Finset.Icc 1 (T / e)).card := Finset.card_image_le
        _ = T / e := by simp
    exact le_trans (by exact_mod_cast hc) Nat.cast_div_le
  have h_swap_div :
      ∀ f : ℕ → ℝ, (∀ e, 0 ≤ f e) →
        (∑ n ∈ Finset.Icc 1 T, ∑ e ∈ n.divisors, f e) ≤
          ∑ e ∈ Finset.Icc 1 T, ((T : ℝ) / (e : ℝ)) * f e := by
    intro f hf_nn
    have h_eq :
        (∑ n ∈ Finset.Icc 1 T, ∑ e ∈ n.divisors, f e) =
          ∑ e ∈ Finset.Icc 1 T, (((Finset.Icc 1 T).filter (fun n => e ∣ n)).card : ℝ) * f e := by
      have h_lhs :
          (∑ n ∈ Finset.Icc 1 T, ∑ e ∈ n.divisors, f e) =
            ∑ n ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T, if e ∣ n then f e else 0 := by
        apply Finset.sum_congr rfl
        intro n hn
        have hn1 : 1 ≤ n := (Finset.mem_Icc.mp hn).1
        have hnT : n ≤ T := (Finset.mem_Icc.mp hn).2
        rw [← Finset.sum_filter]
        apply Finset.sum_congr
        · ext e
          simp only [Nat.mem_divisors, Finset.mem_filter, Finset.mem_Icc]
          constructor
          · rintro ⟨hd, _⟩
            exact ⟨⟨Nat.pos_of_dvd_of_pos hd hn1, le_trans (Nat.le_of_dvd hn1 hd) hnT⟩, hd⟩
          · rintro ⟨_, hd⟩
            exact ⟨hd, by omega⟩
        · intro _ _; rfl
      rw [h_lhs, Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro e _
      rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul]
    rw [h_eq]
    apply Finset.sum_le_sum
    intro e he
    exact mul_le_mul_of_nonneg_right (h_mult_card (Finset.mem_Icc.mp he).1) (hf_nn e)
  -- Bound ∑_{n=1}^T |openCoreSmoothCoeffS c_lam c_half T D0 n| / (log Y)^2:
  have h_sum_s :
      (∑ n ∈ Finset.Icc 1 T, |openCoreSmoothCoeffS c_lam c_half T D0 n|) / (Real.log Y) ^ 2 ≤
        (6 + 10 * |c_lam| + 30 * (8 + |c_half|) + 50 * C_R) * (T : ℝ) := by
    have h_step_bd :
        ∀ e : ℕ, 2 ≤ e →
          |R_osc e - R_osc (e - 1)| ≤
            |selbergLiouvilleWeight2 e| + |c_lam| +
              |squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)| := by
      intro e he2
      have h_w2_diff : selbergCumulativeW2 e - selbergCumulativeW2 (e - 1) = selbergLiouvilleWeight2 e := by
        unfold selbergCumulativeW2
        have h_icc : Finset.Icc 2 e = insert e (Finset.Icc 2 (e - 1)) := by
          ext k; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
        rw [h_icc, Finset.sum_insert (by simp only [Finset.mem_Icc]; omega)]
        ring
      have h_diff_eq :
          R_osc e - R_osc (e - 1) =
            selbergLiouvilleWeight2 e - c_lam -
              (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) := by
        dsimp [R_osc]
        unfold selbergCenteredRemainderInt
        have h_cast : ((e - 1 : ℕ) : ℝ) = (e : ℝ) - 1 := by
          rw [Nat.cast_sub (by omega : 1 ≤ e), Nat.cast_one]
        rw [h_cast]
        linarith [h_w2_diff]
      rw [h_diff_eq]
      calc
        |selbergLiouvilleWeight2 e - c_lam -
            (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1))|
          ≤ |selbergLiouvilleWeight2 e - c_lam| +
              |squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)| := abs_sub _ _
        _ ≤ (|selbergLiouvilleWeight2 e| + |c_lam|) +
              |squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)| :=
            add_le_add_right (abs_sub _ _) _
    have h_each_n_s :
        ∀ n ∈ Finset.Icc 1 T,
          |openCoreSmoothCoeffS c_lam c_half T D0 n| ≤
            (∑ e ∈ n.divisors, |selbergLiouvilleWeight2 e|) +
              (∑ _e ∈ n.divisors, |c_lam|) +
              (∑ e ∈ n.divisors, |squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)|) +
              (if D_eff + 1 ≤ T - 1 ∧ (D_eff + 1) ∣ n then |R_osc (D_eff + 1)| else 0) +
              (if n = T ∧ D_eff + 1 ≤ T - 1 then |R_osc (T - 1)| else 0) := by
      intro n hn
      have htel := openCoreSmoothCoeffS_telescoping_tc065_aux hT1 D0 c_lam c_half hn
      dsimp only at htel
      change |openCoreSmoothCoeffS c_lam c_half T D0 n| ≤ _
      rw [htel]
      have h_t1 :
          |∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1),
              (liouvilleLambda (n / e) : ℝ) * (R_osc e - R_osc (e - 1))| ≤
            (∑ e ∈ n.divisors, |selbergLiouvilleWeight2 e|) +
              (∑ _e ∈ n.divisors, |c_lam|) +
              (∑ e ∈ n.divisors, |squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)|) := by
        calc
          |∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1),
              (liouvilleLambda (n / e) : ℝ) * (R_osc e - R_osc (e - 1))|
            ≤ ∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1),
                |(liouvilleLambda (n / e) : ℝ) * (R_osc e - R_osc (e - 1))| :=
              Finset.abs_sum_le_sum_abs _ _
          _ ≤ ∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1),
                (|selbergLiouvilleWeight2 e| + |c_lam| +
                  |squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)|) := by
              apply Finset.sum_le_sum
              intro e he
              simp only [Finset.mem_filter, Nat.mem_divisors] at he
              have hn1 : 1 ≤ n := (Finset.mem_Icc.mp hn).1
              have hq1 : 1 ≤ n / e := Nat.div_pos (Nat.le_of_dvd hn1 he.1.1) (by omega)
              rw [abs_mul, (liouvilleLambda_props_tc065_aux.2.1 hq1).2, one_mul]
              exact h_step_bd e (by omega)
          _ ≤ ∑ e ∈ n.divisors,
                (|selbergLiouvilleWeight2 e| + |c_lam| +
                  |squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)|) :=
              Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _) (fun _ _ _ => by positivity)
          _ = _ := by rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
      have h_t2 :
          |if D_eff + 1 ≤ T - 1 ∧ (D_eff + 1) ∣ n then
              (liouvilleLambda (n / (D_eff + 1)) : ℝ) * R_osc (D_eff + 1)
            else 0| ≤
            if D_eff + 1 ≤ T - 1 ∧ (D_eff + 1) ∣ n then |R_osc (D_eff + 1)| else 0 := by
        split_ifs with h
        · have hn1 : 1 ≤ n := (Finset.mem_Icc.mp hn).1
          have hq1 : 1 ≤ n / (D_eff + 1) := Nat.div_pos (Nat.le_of_dvd hn1 h.2) (by omega)
          rw [abs_mul, (liouvilleLambda_props_tc065_aux.2.1 hq1).2, one_mul]
        · simp
      have h_t3 :
          |if n = T ∧ D_eff + 1 ≤ T - 1 then R_osc (T - 1) else 0| ≤
            if n = T ∧ D_eff + 1 ≤ T - 1 then |R_osc (T - 1)| else 0 := by
        split_ifs <;> simp
      have h_ab := abs_add
        (∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1),
          (liouvilleLambda (n / e) : ℝ) * (R_osc e - R_osc (e - 1)))
        (if D_eff + 1 ≤ T - 1 ∧ (D_eff + 1) ∣ n then
          (liouvilleLambda (n / (D_eff + 1)) : ℝ) * R_osc (D_eff + 1)
        else 0)
      calc
        |(∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1),
              (liouvilleLambda (n / e) : ℝ) * (R_osc e - R_osc (e - 1))) +
            (if D_eff + 1 ≤ T - 1 ∧ (D_eff + 1) ∣ n then
              (liouvilleLambda (n / (D_eff + 1)) : ℝ) * R_osc (D_eff + 1)
            else 0) -
            (if n = T ∧ D_eff + 1 ≤ T - 1 then R_osc (T - 1) else 0)|
          ≤ |(∑ e ∈ n.divisors.filter (fun e => D_eff + 2 ≤ e ∧ e ≤ T - 1),
                (liouvilleLambda (n / e) : ℝ) * (R_osc e - R_osc (e - 1))) +
              (if D_eff + 1 ≤ T - 1 ∧ (D_eff + 1) ∣ n then
                (liouvilleLambda (n / (D_eff + 1)) : ℝ) * R_osc (D_eff + 1)
              else 0)| +
              |if n = T ∧ D_eff + 1 ≤ T - 1 then R_osc (T - 1) else 0| := abs_sub _ _
        _ ≤ _ := by linarith [h_ab, h_t1, h_t2, h_t3]
    have h_p1 :
        (∑ n ∈ Finset.Icc 1 T, ∑ e ∈ n.divisors, |selbergLiouvilleWeight2 e|) ≤
          (T : ℝ) * (Real.log (T : ℝ)) ^ 2 := by
      calc
        _ = ∑ n ∈ Finset.Icc 1 T, (Real.log (n : ℝ)) ^ 2 :=
            Finset.sum_congr rfl (fun n hn =>
              sum_divisors_abs_selbergLiouvilleWeight2_tc065_aux (Finset.mem_Icc.mp hn).1)
        _ ≤ ∑ _n ∈ Finset.Icc 1 T, (Real.log (T : ℝ)) ^ 2 := by
            apply Finset.sum_le_sum
            intro n hn
            obtain ⟨hn1, hnT⟩ := Finset.mem_Icc.mp hn
            exact pow_le_pow_left (Real.log_nonneg (by exact_mod_cast hn1))
              (Real.log_le_log (Nat.cast_pos.mpr hn1) (by exact_mod_cast hnT)) 2
        _ = (T : ℝ) * (Real.log (T : ℝ)) ^ 2 := by simp
    have h_p2 :
        (∑ n ∈ Finset.Icc 1 T, ∑ _e ∈ n.divisors, |c_lam|) ≤
          |c_lam| * (T : ℝ) * (1 + Real.log (T : ℝ)) := by
      calc
        _ ≤ ∑ e ∈ Finset.Icc 1 T, ((T : ℝ) / (e : ℝ)) * |c_lam| :=
            h_swap_div (fun _ => |c_lam|) (fun _ => abs_nonneg _)
        _ = |c_lam| * (T : ℝ) * ∑ e ∈ Finset.Icc 1 T, (1 : ℝ) / (e : ℝ) := by
            rw [Finset.mul_sum]; apply Finset.sum_congr rfl; intro e _; ring
        _ ≤ |c_lam| * (T : ℝ) * (1 + Real.log (T : ℝ)) :=
            mul_le_mul_of_nonneg_left (sum_inv_Icc_le_one_add_log_tc065_aux hT1) (by positivity)
    have h_p3 :
        (∑ n ∈ Finset.Icc 1 T,
            ∑ e ∈ n.divisors, |squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)|) ≤
          3 * (8 + |c_half|) * (T : ℝ) * (1 + Real.log (T : ℝ)) := by
      have h_sum_e32 : (∑ e ∈ Finset.Icc 1 T, (1 : ℝ) / ((e : ℝ) * Real.sqrt (e : ℝ))) ≤ 3 := by
        have h_sp : Finset.Icc 1 T = insert 1 (Finset.Icc 2 T) := by
          ext k; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
        rw [h_sp, Finset.sum_insert (by simp)]
        simp only [Nat.cast_one, Real.sqrt_one, mul_one, div_one]
        linarith [sum_inv_rpow_three_halves_le_two_tc065_aux T]
      calc
        _ ≤ ∑ e ∈ Finset.Icc 1 T,
              ((T : ℝ) / (e : ℝ)) * |squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)| :=
            h_swap_div _ (fun _ => abs_nonneg _)
        _ ≤ ∑ e ∈ Finset.Icc 1 T,
              ((8 + |c_half|) * (T : ℝ) * (1 + Real.log (T : ℝ))) *
                ((1 : ℝ) / ((e : ℝ) * Real.sqrt (e : ℝ))) := by
            apply Finset.sum_le_sum
            intro e he
            obtain ⟨he1, heT⟩ := Finset.mem_Icc.mp he
            have hdM := (two_sided_interior_diag_bound_and_offdiag_equivalence_tc062r).2.2.2.1.1
              c_half he1
            have hlog_le : 1 + Real.log (e : ℝ) ≤ 1 + Real.log (T : ℝ) :=
              add_le_add_left (Real.log_le_log (Nat.cast_pos.mpr he1) (by exact_mod_cast heT)) 1
            have h1 := mul_le_mul_of_nonneg_left
              (le_trans hdM (div_le_div_of_nonneg_right
                (mul_le_mul_of_nonneg_left hlog_le (by positivity)) (Real.sqrt_nonneg _)))
              (div_nonneg (le_of_lt hT_pos_r) (Nat.cast_nonneg e))
            calc _ ≤ _ := h1
              _ = _ := by ring
        _ = ((8 + |c_half|) * (T : ℝ) * (1 + Real.log (T : ℝ))) *
              ∑ e ∈ Finset.Icc 1 T, (1 : ℝ) / ((e : ℝ) * Real.sqrt (e : ℝ)) :=
            (Finset.mul_sum _ _ _).symm
        _ ≤ ((8 + |c_half|) * (T : ℝ) * (1 + Real.log (T : ℝ))) * 3 :=
            mul_le_mul_of_nonneg_left h_sum_e32
              (mul_nonneg (mul_nonneg (by positivity) (le_of_lt hT_pos_r))
                (add_nonneg zero_le_one (Real.log_nonneg (by exact_mod_cast hT1))))
        _ = 3 * (8 + |c_half|) * (T : ℝ) * (1 + Real.log (T : ℝ)) := by ring
    have h_p4 :
        (∑ n ∈ Finset.Icc 1 T,
            if D_eff + 1 ≤ T - 1 ∧ (D_eff + 1) ∣ n then |R_osc (D_eff + 1)| else 0) ≤
          C_R * (T : ℝ) * (1 + Real.log (T : ℝ)) ^ 2 := by
      by_cases hr : D_eff + 1 ≤ T - 1
      · have h_rew :
            (∑ n ∈ Finset.Icc 1 T,
                if D_eff + 1 ≤ T - 1 ∧ (D_eff + 1) ∣ n then |R_osc (D_eff + 1)| else 0) =
              (((Finset.Icc 1 T).filter (fun n => (D_eff + 1) ∣ n)).card : ℝ) *
                |R_osc (D_eff + 1)| := by
          rw [← Finset.sum_filter]
          have h_f :
              (Finset.Icc 1 T).filter (fun n => D_eff + 1 ≤ T - 1 ∧ (D_eff + 1) ∣ n) =
                (Finset.Icc 1 T).filter (fun n => (D_eff + 1) ∣ n) := by
            ext n; simp [hr]
          rw [h_f, Finset.sum_const, nsmul_eq_mul]
        rw [h_rew]
        have hd1 : 1 ≤ D_eff + 1 := by omega
        have hdT : D_eff + 1 ≤ T := by omega
        have hd_pos : (0 : ℝ) < ((D_eff + 1 : ℕ) : ℝ) := Nat.cast_pos.mpr hd1
        have h_log_le : (1 + Real.log ((D_eff + 1 : ℕ) : ℝ)) ^ 2 ≤ (1 + Real.log (T : ℝ)) ^ 2 :=
          pow_le_pow_left
            (add_nonneg zero_le_one (Real.log_nonneg (by exact_mod_cast hd1)))
            (add_le_add_left (Real.log_le_log hd_pos (by exact_mod_cast hdT)) 1) 2
        calc
          _ ≤ ((T : ℝ) / ((D_eff + 1 : ℕ) : ℝ)) *
                (C_R * ((D_eff + 1 : ℕ) : ℝ) * (1 + Real.log ((D_eff + 1 : ℕ) : ℝ)) ^ 2) :=
              mul_le_mul (h_mult_card hd1) (h_R_osc_bd hd1) (abs_nonneg _) (by positivity)
          _ = C_R * (T : ℝ) * (1 + Real.log ((D_eff + 1 : ℕ) : ℝ)) ^ 2 := by
              field_simp [ne_of_gt hd_pos]; ring
          _ ≤ C_R * (T : ℝ) * (1 + Real.log (T : ℝ)) ^ 2 :=
              mul_le_mul_of_nonneg_left h_log_le (by positivity)
      · have h0 :
            (∑ n ∈ Finset.Icc 1 T,
                if D_eff + 1 ≤ T - 1 ∧ (D_eff + 1) ∣ n then |R_osc (D_eff + 1)| else 0) = 0 := by
          apply Finset.sum_eq_zero; intro n _; rw [if_neg (fun h => hr h.1)]
        rw [h0]; positivity
    have h_p5 :
        (∑ n ∈ Finset.Icc 1 T,
            if n = T ∧ D_eff + 1 ≤ T - 1 then |R_osc (T - 1)| else 0) ≤
          C_R * (T : ℝ) * (1 + Real.log (T : ℝ)) ^ 2 := by
      by_cases hr : D_eff + 1 ≤ T - 1
      · have hTm1_ge1 : 1 ≤ T - 1 := by omega
        have hTm1_le : T - 1 ≤ T := Nat.sub_le T 1
        have h_eq :
            (∑ n ∈ Finset.Icc 1 T,
                if n = T ∧ D_eff + 1 ≤ T - 1 then |R_osc (T - 1)| else 0) =
              |R_osc (T - 1)| := by
          have hT_in : T ∈ Finset.Icc 1 T := Finset.mem_Icc.mpr ⟨hT1, le_refl T⟩
          rw [← Finset.add_sum_erase _ _ hT_in, if_pos ⟨rfl, hr⟩,
            Finset.sum_eq_zero (fun n hn => by
              rw [if_neg (fun h => (Finset.mem_erase.mp hn).1 h.1)]), add_zero]
        rw [h_eq]
        have h_log_le : (1 + Real.log ((T - 1 : ℕ) : ℝ)) ^ 2 ≤ (1 + Real.log (T : ℝ)) ^ 2 :=
          pow_le_pow_left
            (add_nonneg zero_le_one (Real.log_nonneg (by exact_mod_cast hTm1_ge1)))
            (add_le_add_left (Real.log_le_log (Nat.cast_pos.mpr hTm1_ge1) (by exact_mod_cast hTm1_le)) 1) 2
        calc
          |R_osc (T - 1)| ≤ C_R * ((T - 1 : ℕ) : ℝ) * (1 + Real.log ((T - 1 : ℕ) : ℝ)) ^ 2 :=
            h_R_osc_bd hTm1_ge1
          _ ≤ C_R * (T : ℝ) * (1 + Real.log (T : ℝ)) ^ 2 :=
            mul_le_mul (mul_le_mul_of_nonneg_left (by exact_mod_cast hTm1_le) hCR_nn)
              h_log_le (sq_nonneg _) (by positivity)
      · have h0 :
            (∑ n ∈ Finset.Icc 1 T,
                if n = T ∧ D_eff + 1 ≤ T - 1 then |R_osc (T - 1)| else 0) = 0 := by
          apply Finset.sum_eq_zero; intro n _; rw [if_neg (fun h => hr h.2)]
        rw [h0]; positivity
    have h_tot_s :
        (∑ n ∈ Finset.Icc 1 T, |openCoreSmoothCoeffS c_lam c_half T D0 n|) ≤
          (T : ℝ) * (Real.log (T : ℝ)) ^ 2 +
            (|c_lam| + 3 * (8 + |c_half|)) * (T : ℝ) * (1 + Real.log (T : ℝ)) +
            2 * C_R * (T : ℝ) * (1 + Real.log (T : ℝ)) ^ 2 := by
      have h1 := Finset.sum_le_sum h_each_n_s
      simp_rw [Finset.sum_add_distrib] at h1
      linarith [h1, h_p1, h_p2, h_p3, h_p4, h_p5]
    have h_div := div_le_div_of_nonneg_right h_tot_s (sq_nonneg (Real.log Y))
    have h_rhs_le :
        ((T : ℝ) * (Real.log (T : ℝ)) ^ 2 +
            (|c_lam| + 3 * (8 + |c_half|)) * (T : ℝ) * (1 + Real.log (T : ℝ)) +
            2 * C_R * (T : ℝ) * (1 + Real.log (T : ℝ)) ^ 2) / (Real.log Y) ^ 2 ≤
          (6 + 10 * |c_lam| + 30 * (8 + |c_half|) + 50 * C_R) * (T : ℝ) := by
      have h_alg :
          ((T : ℝ) * (Real.log (T : ℝ)) ^ 2 +
              (|c_lam| + 3 * (8 + |c_half|)) * (T : ℝ) * (1 + Real.log (T : ℝ)) +
              2 * C_R * (T : ℝ) * (1 + Real.log (T : ℝ)) ^ 2) / (Real.log Y) ^ 2 =
            (Real.log (T : ℝ) / Real.log Y) ^ 2 * (T : ℝ) +
              (|c_lam| + 3 * (8 + |c_half|)) * ((1 + Real.log (T : ℝ)) / (Real.log Y) ^ 2) * (T : ℝ) +
              2 * C_R * ((1 + Real.log (T : ℝ)) / Real.log Y) ^ 2 * (T : ℝ) := by
        field_simp [ne_of_gt hlogY_pos]; ring
      rw [h_alg]
      have hc1 : (Real.log (T : ℝ) / Real.log Y) ^ 2 * (T : ℝ) ≤ 6 * (T : ℝ) :=
        mul_le_mul_of_nonneg_right h_logT_rat (le_of_lt hT_pos_r)
      have hc2 :
          (|c_lam| + 3 * (8 + |c_half|)) * ((1 + Real.log (T : ℝ)) / (Real.log Y) ^ 2) * (T : ℝ) ≤
            (|c_lam| + 3 * (8 + |c_half|)) * 10 * (T : ℝ) :=
        mul_le_mul_of_nonneg_right
          (mul_le_mul_of_nonneg_left h_1logT_over_logY2 (by positivity)) (le_of_lt hT_pos_r)
      have hc3 :
          2 * C_R * ((1 + Real.log (T : ℝ)) / Real.log Y) ^ 2 * (T : ℝ) ≤
            2 * C_R * 25 * (T : ℝ) :=
        mul_le_mul_of_nonneg_right
          (mul_le_mul_of_nonneg_left h_1logT_rat (by positivity)) (le_of_lt hT_pos_r)
      linarith
    exact le_trans h_div h_rhs_le
  -- Pointwise bound |pairedCutoffFringeScalarPhi ... X| ≤ B_fr on [Y, tau * Y]:
  obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc065_aux hY2
  obtain ⟨_, _, _, _, _, _, _, _, _, hPhi_c, _, _⟩ :=
    continuousOn_core_objects_tc065_aux hY2 htau c_lam c_half T D0
  have h_pt_fr :
      ∀ X ∈ Set.Icc Y (RiemannScope.tau * Y),
        |pairedCutoffFringeScalarPhi c_lam c_half T D0 X| ≤ B_fr := by
    intro X hX
    have hX_u : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
    have hX0 : 0 < X := (hprops X hX_u).2.1
    have hlogX_ge : Real.log Y ≤ Real.log X := Real.log_le_log hY0 hX.1
    have h_each_n :
        ∀ n ∈ uncoveredCutoffStripStations 2 T,
          |(liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X| ≤
            (1 + (Real.log (T : ℝ) / Real.log Y) ^ 2 +
              |openCoreSmoothCoeffS c_lam c_half T D0 n| / (Real.log Y) ^ 2) *
              (8 * RiemannScope.tau ^ (5 / 2 : ℝ) / (T : ℝ)) := by
      intro n hn
      have hn_Icc : n ∈ Finset.Icc 1 T := by
        have hu := (coveredInteriorStations_partition_and_char_tc065_aux T).1.2
        rw [← hu]; exact Finset.mem_union_right _ hn
      obtain ⟨hn1, hnT⟩ := Finset.mem_Icc.mp hn_Icc
      have hn_pos_r : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr hn1
      have hT_lt_2n : T < 2 * n :=
        ((coveredInteriorStations_partition_and_char_tc065_aux T).2.2.1 n hn_Icc).mp hn |>.2
      have h_inv_n3 : ((n : ℝ) ^ 3)⁻¹ ≤ 8 / (T : ℝ) ^ 3 := by
        have h_inv_n : (n : ℝ)⁻¹ ≤ 2 / (T : ℝ) := by
          have hT_le_2n : (T : ℝ) ≤ 2 * (n : ℝ) := by exact_mod_cast (le_of_lt hT_lt_2n)
          rw [inv_eq_one_div, div_le_div_iff hn_pos_r hT_pos_r]; linarith
        have hp3 := pow_le_pow_left (inv_nonneg.mpr (le_of_lt hn_pos_r)) h_inv_n 3
        rw [inv_pow] at hp3
        calc ((n : ℝ) ^ 3)⁻¹ ≤ (2 / (T : ℝ)) ^ 3 := hp3
          _ = 8 / (T : ℝ) ^ 3 := by ring
      have h_phi_nn : 0 ≤ gaussianTermPhi n X := by
        unfold gaussianTermPhi
        exact mul_nonneg (Real.rpow_nonneg (le_of_lt hX0) _)
          (mul_nonneg (inv_nonneg.mpr (pow_nonneg (le_of_lt hn_pos_r) 3))
            (le_of_lt (Real.exp_pos _)))
      have h_phi_le : gaussianTermPhi n X ≤ 8 * RiemannScope.tau ^ (5 / 2 : ℝ) / (T : ℝ) := by
        unfold gaussianTermPhi
        have hexp : Real.exp (-(X ^ 2) / (n : ℝ) ^ 2) ≤ 1 := by
          rw [Real.exp_le_one_iff]
          exact div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg X)) (sq_nonneg _)
        have hX52 : X ^ (5 / 2 : ℝ) ≤ RiemannScope.tau ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ) := by
          rw [← Real.mul_rpow (le_of_lt htau_pos) (le_of_lt hY0)]
          exact Real.rpow_le_rpow (le_of_lt hX0) hX.2 (by norm_num)
        calc
          X ^ (5 / 2 : ℝ) * (((n : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (n : ℝ) ^ 2))
            ≤ (RiemannScope.tau ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ)) * ((8 / (T : ℝ) ^ 3) * 1) :=
              mul_le_mul hX52
                (mul_le_mul h_inv_n3 hexp (le_of_lt (Real.exp_pos _)) (by positivity))
                (by positivity) (by positivity)
          _ ≤ (RiemannScope.tau ^ (5 / 2 : ℝ) * (T : ℝ) ^ 2) * ((8 / (T : ℝ) ^ 3) * 1) := by
              gcongr
          _ = 8 * RiemannScope.tau ^ (5 / 2 : ℝ) / (T : ℝ) := by
              field_simp [ne_of_gt hT_pos_r]; ring
      have h_coeff_bd :
          |1 - signedAdjustedCoeffB c_lam c_half T D0 n / (Real.log X) ^ 2| ≤
            1 + (Real.log (T : ℝ) / Real.log Y) ^ 2 +
              |openCoreSmoothCoeffS c_lam c_half T D0 n| / (Real.log Y) ^ 2 := by
        unfold signedAdjustedCoeffB openCoreAdjustedCoeffBeta truncatedLiouvilleCoeff
        simp only [hn1, hnT, and_self, ↓reduceIte]
        have h_logX2_ge : (Real.log Y) ^ 2 ≤ (Real.log X) ^ 2 :=
          pow_le_pow_left (le_of_lt hlogY_pos) hlogX_ge 2
        have h_logn_le : (Real.log (n : ℝ)) ^ 2 ≤ (Real.log (T : ℝ)) ^ 2 :=
          pow_le_pow_left (Real.log_nonneg (by exact_mod_cast hn1))
            (Real.log_le_log hn_pos_r (by exact_mod_cast hnT)) 2
        have h_b_abs :
            |(liouvilleLambda n : ℝ) *
                (openCoreSmoothCoeffS c_lam c_half T D0 n -
                  (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2)| ≤
              |openCoreSmoothCoeffS c_lam c_half T D0 n| + (Real.log (T : ℝ)) ^ 2 := by
          rw [abs_mul, (liouvilleLambda_props_tc065_aux.2.1 hn1).2, one_mul]
          calc
            |openCoreSmoothCoeffS c_lam c_half T D0 n -
                (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2|
              ≤ |openCoreSmoothCoeffS c_lam c_half T D0 n| +
                  |(liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2| := abs_sub _ _
            _ = |openCoreSmoothCoeffS c_lam c_half T D0 n| + (Real.log (n : ℝ)) ^ 2 := by
                rw [abs_mul, (liouvilleLambda_props_tc065_aux.2.1 hn1).2, one_mul,
                  abs_of_nonneg (sq_nonneg (Real.log (n : ℝ)))]
            _ ≤ |openCoreSmoothCoeffS c_lam c_half T D0 n| + (Real.log (T : ℝ)) ^ 2 := by linarith
        calc
          |1 - (liouvilleLambda n : ℝ) *
                (openCoreSmoothCoeffS c_lam c_half T D0 n -
                  (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2) / (Real.log X) ^ 2|
            ≤ 1 + |(liouvilleLambda n : ℝ) *
                (openCoreSmoothCoeffS c_lam c_half T D0 n -
                  (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2) / (Real.log X) ^ 2| := by
              simpa [abs_one] using abs_sub (1 : ℝ) _
          _ = 1 + |(liouvilleLambda n : ℝ) *
                (openCoreSmoothCoeffS c_lam c_half T D0 n -
                  (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2)| / (Real.log X) ^ 2 := by
              rw [abs_div, abs_of_nonneg (sq_nonneg (Real.log X))]
          _ ≤ 1 + (|openCoreSmoothCoeffS c_lam c_half T D0 n| + (Real.log (T : ℝ)) ^ 2) /
                (Real.log Y) ^ 2 := by
              have hd := div_le_div (by positivity) h_b_abs (sq_pos_of_pos hlogY_pos) h_logX2_ge
              linarith
          _ = 1 + (Real.log (T : ℝ) / Real.log Y) ^ 2 +
                |openCoreSmoothCoeffS c_lam c_half T D0 n| / (Real.log Y) ^ 2 := by
              rw [add_div, div_pow]; ring
      unfold adjustedStationProfilePsi
      rw [abs_mul, (liouvilleLambda_props_tc065_aux.2.1 hn1).2, one_mul, abs_mul,
        abs_of_nonneg h_phi_nn]
      exact mul_le_mul h_coeff_bd h_phi_le h_phi_nn (by positivity)
    unfold pairedCutoffFringeScalarPhi
    have h_sub_icc : uncoveredCutoffStripStations 2 T ⊆ Finset.Icc 1 T := by
      unfold uncoveredCutoffStripStations; exact Finset.sdiff_subset _ _
    calc
      |∑ n ∈ uncoveredCutoffStripStations 2 T,
          (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X|
        ≤ ∑ n ∈ uncoveredCutoffStripStations 2 T,
            |(liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X| :=
          Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ n ∈ uncoveredCutoffStripStations 2 T,
            (1 + (Real.log (T : ℝ) / Real.log Y) ^ 2 +
              |openCoreSmoothCoeffS c_lam c_half T D0 n| / (Real.log Y) ^ 2) *
              (8 * RiemannScope.tau ^ (5 / 2 : ℝ) / (T : ℝ)) :=
          Finset.sum_le_sum h_each_n
      _ ≤ ∑ n ∈ Finset.Icc 1 T,
            (1 + (Real.log (T : ℝ) / Real.log Y) ^ 2 +
              |openCoreSmoothCoeffS c_lam c_half T D0 n| / (Real.log Y) ^ 2) *
              (8 * RiemannScope.tau ^ (5 / 2 : ℝ) / (T : ℝ)) :=
          Finset.sum_le_sum_of_subset_of_nonneg h_sub_icc (fun _ _ _ => by positivity)
      _ = ((T : ℝ) * (1 + (Real.log (T : ℝ) / Real.log Y) ^ 2) +
            (∑ n ∈ Finset.Icc 1 T, |openCoreSmoothCoeffS c_lam c_half T D0 n|) / (Real.log Y) ^ 2) *
            (8 * RiemannScope.tau ^ (5 / 2 : ℝ) / (T : ℝ)) := by
          rw [← Finset.sum_mul, Finset.sum_add_distrib, Finset.sum_const, nsmul_eq_mul,
            Nat.card_Icc, show T + 1 - 1 = T by omega, ← Finset.sum_div]
      _ ≤ (B_coeff * (T : ℝ)) * (8 * RiemannScope.tau ^ (5 / 2 : ℝ) / (T : ℝ)) := by
          apply mul_le_mul_of_nonneg_right _ (by positivity)
          have h1 : (T : ℝ) * (1 + (Real.log (T : ℝ) / Real.log Y) ^ 2) ≤ (1 + 6) * (T : ℝ) := by
            rw [mul_comm]
            exact mul_le_mul_of_nonneg_right (by linarith [h_logT_rat]) (le_of_lt hT_pos_r)
          dsimp [B_coeff]
          linarith [h1, h_sum_s]
      _ = B_fr := by
          dsimp [B_fr]; field_simp [ne_of_gt hT_pos_r]; ring
  have h_int_lhs :
      IntervalIntegrable
        (fun X => pairedCutoffFringeScalarPhi c_lam c_half T D0 X *
          pairedCutoffFringeScalarPhi c_lam c_half T D0 X / X)
        volume Y (RiemannScope.tau * Y) :=
    ((hPhi_c.mul hPhi_c).div continuousOn_id
      (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
  have h_int_rhs :
      IntervalIntegrable (fun X => B_fr ^ 2 * ((1 : ℝ) / X)) volume Y (RiemannScope.tau * Y) :=
    (continuousOn_const.mul (continuousOn_const.div continuousOn_id
      (fun X hX => ne_of_gt (hprops X hX).2.1))).intervalIntegrable
  unfold windowEnergyNormSq windowPairing
  calc
    (∫ X in Y..(RiemannScope.tau * Y),
        pairedCutoffFringeScalarPhi c_lam c_half T D0 X *
          pairedCutoffFringeScalarPhi c_lam c_half T D0 X / X)
      ≤ ∫ X in Y..(RiemannScope.tau * Y), B_fr ^ 2 * ((1 : ℝ) / X) := by
        apply intervalIntegral.integral_mono_on hle h_int_lhs h_int_rhs
        intro X hX
        have hX0 : 0 < X := lt_of_lt_of_le hY0 hX.1
        have hsq := pow_le_pow_left (abs_nonneg _) (h_pt_fr X hX) 2
        rw [sq_abs, sq] at hsq
        have hd := div_le_div_of_nonneg_right hsq (le_of_lt hX0)
        rwa [show B_fr ^ 2 / X = B_fr ^ 2 * ((1 : ℝ) / X) by ring] at hd
    _ = B_fr ^ 2 * ∫ X in Y..(RiemannScope.tau * Y), (1 : ℝ) / X :=
        intervalIntegral.integral_const_mul _ _
    _ = B_fr ^ 2 * Real.log RiemannScope.tau := by
        rw [intervalIntegral_inv_param_tc065_aux hY0 htau]

private theorem fullFeatureVectorG_norm_sum_eq_Dtilde_tc065_aux {Y : ℝ} (hY2 : 2 ≤ Y)
    {T : ℕ} (_hT1 : 1 ≤ T) :
    (∑ pk ∈ primePowerPairsUpTo T, windowEnergyNormSq Y (fullFeatureVectorG T pk)) =
      inheritedPrimePowerDiagDtilde T Y := by
  have htau := tau_gt_one_and_lt_eight_tc065_aux.1
  obtain ⟨_hle, hprops⟩ := uIcc_tau_props_tc065_aux hY2
  obtain ⟨_, _, _, _, _, _, _, _, _, _, hGfull_c, _⟩ :=
    continuousOn_core_objects_tc065_aux hY2 htau 0 0 T 0
  have h_int :
      ∀ pk ∈ primePowerPairsUpTo T,
        IntervalIntegrable (fun X => fullFeatureVectorG T pk X * fullFeatureVectorG T pk X / X)
          volume Y (RiemannScope.tau * Y) :=
    fun pk _ => (((hGfull_c pk).mul (hGfull_c pk)).div continuousOn_id
      (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
  unfold windowEnergyNormSq windowPairing inheritedPrimePowerDiagDtilde
  rw [← intervalIntegral.integral_finset_sum h_int]
  apply intervalIntegral.integral_congr
  intro X hX
  dsimp only
  obtain ⟨_, hX0, _, _hlog_ne, _⟩ := hprops X hX
  unfold pointwisePrimePowerDiagNorm
  rw [Finset.sum_div, Finset.sum_div]
  apply Finset.sum_congr rfl
  intro pk hpk
  rw [fullFeatureVectorG_eq_liouvillePrimePowerTerm_div_log_tc065_aux hpk hX0]
  unfold liouvillePrimePowerTerm
  simp only [primePowerPairsUpTo, primesUpToFinset, Finset.mem_filter, Finset.mem_product,
    Finset.mem_Icc] at hpk
  have hp : pk.1.Prime := hpk.1.1.2
  have hd_pos : (0 : ℝ) < ((pk.1 ^ pk.2 : ℕ) : ℝ) :=
    Nat.cast_pos.mpr (Nat.one_le_pow pk.2 pk.1 hp.pos)
  have h_sgn_sq : ((-1 : ℝ) ^ pk.2) ^ 2 = 1 := by
    rw [← pow_mul, mul_comm, pow_mul, show (-1 : ℝ) ^ 2 = 1 by norm_num, one_pow]
  have h_sq_sqrt : (Real.sqrt ((pk.1 ^ pk.2 : ℕ) : ℝ)) ^ 2 = ((pk.1 ^ pk.2 : ℕ) : ℝ) :=
    Real.sq_sqrt (le_of_lt hd_pos)
  have h_alg :
      ((-1 : ℝ) ^ pk.2 * Real.log (pk.1 : ℝ) * (1 / Real.sqrt ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
          finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ)) / Real.log X) *
        ((-1 : ℝ) ^ pk.2 * Real.log (pk.1 : ℝ) * (1 / Real.sqrt ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
          finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ)) / Real.log X) =
        ((Real.log (pk.1 : ℝ)) ^ 2 / ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
          (finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ))) ^ 2 /
            (Real.log X) ^ 2 := by
    have h1 :
        ((-1 : ℝ) ^ pk.2 * Real.log (pk.1 : ℝ) * (1 / Real.sqrt ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
            finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ)) / Real.log X) *
          ((-1 : ℝ) ^ pk.2 * Real.log (pk.1 : ℝ) * (1 / Real.sqrt ((pk.1 ^ pk.2 : ℕ) : ℝ)) *
            finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ)) / Real.log X) =
          (((-1 : ℝ) ^ pk.2) ^ 2 * (Real.log (pk.1 : ℝ)) ^ 2 *
            (1 / (Real.sqrt ((pk.1 ^ pk.2 : ℕ) : ℝ)) ^ 2) *
            (finiteQLambda (T / pk.1 ^ pk.2) (X / ((pk.1 ^ pk.2 : ℕ) : ℝ))) ^ 2) /
            (Real.log X) ^ 2 := by ring
    rw [h1, h_sgn_sq, h_sq_sqrt]
    ring
  rw [h_alg]

private theorem direct_sum_reverse_triangle_tc065_aux {Y : ℝ} (hY0 : 0 < Y)
    {ι : Type*} (S : Finset ι) (A B : ι → ℝ → ℝ)
    (hA : ∀ i ∈ S, ContinuousOn (A i) (Set.uIcc Y (RiemannScope.tau * Y)))
    (hB : ∀ i ∈ S, ContinuousOn (B i) (Set.uIcc Y (RiemannScope.tau * Y))) :
    |Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (fun X => A i X - B i X)) -
        Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (A i))| ≤
      Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (B i)) := by
  have h_tri :
      ∀ (F G : ι → ℝ → ℝ),
        (∀ i ∈ S, ContinuousOn (F i) (Set.uIcc Y (RiemannScope.tau * Y))) →
        (∀ i ∈ S, ContinuousOn (G i) (Set.uIcc Y (RiemannScope.tau * Y))) →
        Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (fun X => F i X + G i X)) ≤
          Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (F i)) +
            Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (G i)) := by
    intro F G hF hG
    have hF_nn : 0 ≤ ∑ i ∈ S, windowEnergyNormSq Y (F i) :=
      Finset.sum_nonneg (fun i _ => windowEnergyNormSq_nonneg_tc065_aux hY0 _)
    have hG_nn : 0 ≤ ∑ i ∈ S, windowEnergyNormSq Y (G i) :=
      Finset.sum_nonneg (fun i _ => windowEnergyNormSq_nonneg_tc065_aux hY0 _)
    have h_cs_each :
        ∀ i ∈ S,
          windowPairing Y (F i) (G i) ≤
            Real.sqrt (windowEnergyNormSq Y (F i)) * Real.sqrt (windowEnergyNormSq Y (G i)) := by
      intro i hi
      have htau := tau_gt_one_and_lt_eight_tc065_aux.1
      have h_le := ((gaussian_window_majorant_and_local_frequency_split_tc060).2.1
        hY0 htau (hF i hi) (hG i hi)).2
      have h_eq := ((gaussian_window_majorant_and_local_frequency_split_tc060).2.1
        hY0 htau (hF i hi) (hG i hi)).1
      change windowEnergyNormSq Y (fun X => F i X + G i X) =
        windowEnergyNormSq Y (F i) + 2 * windowPairing Y (F i) (G i) +
          windowEnergyNormSq Y (G i) at h_eq
      change windowEnergyNormSq Y (fun X => F i X + G i X) ≤
        (Real.sqrt (windowEnergyNormSq Y (F i)) + Real.sqrt (windowEnergyNormSq Y (G i))) ^ 2 at h_le
      have h1 : (Real.sqrt (windowEnergyNormSq Y (F i)) + Real.sqrt (windowEnergyNormSq Y (G i))) ^ 2 =
          windowEnergyNormSq Y (F i) +
            2 * (Real.sqrt (windowEnergyNormSq Y (F i)) * Real.sqrt (windowEnergyNormSq Y (G i))) +
            windowEnergyNormSq Y (G i) := by
        have hsf : (Real.sqrt (windowEnergyNormSq Y (F i))) ^ 2 = windowEnergyNormSq Y (F i) :=
          Real.sq_sqrt (windowEnergyNormSq_nonneg_tc065_aux hY0 _)
        have hsg : (Real.sqrt (windowEnergyNormSq Y (G i))) ^ 2 = windowEnergyNormSq Y (G i) :=
          Real.sq_sqrt (windowEnergyNormSq_nonneg_tc065_aux hY0 _)
        nlinarith
      linarith
    have h_cs_sum :
        (∑ i ∈ S, windowPairing Y (F i) (G i)) ≤
          Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (F i)) *
            Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (G i)) := by
      have h1 := Finset.sum_le_sum h_cs_each
      have h2 := Finset.sum_mul_sq_le_sq_mul_sq S
        (fun i => Real.sqrt (windowEnergyNormSq Y (F i)))
        (fun i => Real.sqrt (windowEnergyNormSq Y (G i)))
      have h3 :
          (∑ i ∈ S, (Real.sqrt (windowEnergyNormSq Y (F i))) ^ 2) =
            ∑ i ∈ S, windowEnergyNormSq Y (F i) :=
        Finset.sum_congr rfl (fun i _ => Real.sq_sqrt (windowEnergyNormSq_nonneg_tc065_aux hY0 _))
      have h4 :
          (∑ i ∈ S, (Real.sqrt (windowEnergyNormSq Y (G i))) ^ 2) =
            ∑ i ∈ S, windowEnergyNormSq Y (G i) :=
        Finset.sum_congr rfl (fun i _ => Real.sq_sqrt (windowEnergyNormSq_nonneg_tc065_aux hY0 _))
      rw [h3, h4] at h2
      have h5 :
          (∑ i ∈ S, Real.sqrt (windowEnergyNormSq Y (F i)) * Real.sqrt (windowEnergyNormSq Y (G i))) ≤
            Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (F i)) *
              Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (G i)) := by
        have h_nn_l : 0 ≤ ∑ i ∈ S, Real.sqrt (windowEnergyNormSq Y (F i)) *
            Real.sqrt (windowEnergyNormSq Y (G i)) :=
          Finset.sum_nonneg (fun _ _ => mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _))
        have h_sq := Real.sqrt_le_sqrt h2
        rw [Real.sqrt_sq h_nn_l, Real.sqrt_mul hF_nn] at h_sq
        exact h_sq
      exact le_trans h1 h5
    have h_sq :
        (∑ i ∈ S, windowEnergyNormSq Y (fun X => F i X + G i X)) ≤
          (Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (F i)) +
            Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (G i))) ^ 2 := by
      have h_exp :
          (∑ i ∈ S, windowEnergyNormSq Y (fun X => F i X + G i X)) =
            (∑ i ∈ S, windowEnergyNormSq Y (F i)) +
              2 * (∑ i ∈ S, windowPairing Y (F i) (G i)) +
              (∑ i ∈ S, windowEnergyNormSq Y (G i)) := by
        rw [Finset.sum_congr rfl (fun i hi => windowEnergyNormSq_add_eq_tc065_aux hY0 (hF i hi) (hG i hi)),
          Finset.sum_add_distrib, Finset.sum_add_distrib, ← Finset.mul_sum]
      rw [h_exp]
      have hsf := Real.sq_sqrt hF_nn
      have hsg := Real.sq_sqrt hG_nn
      nlinarith [h_cs_sum]
    have h_rt := Real.sqrt_le_sqrt h_sq
    rwa [Real.sqrt_sq (add_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _))] at h_rt
  have h_negB : ∀ i ∈ S, windowEnergyNormSq Y (fun X => -B i X) = windowEnergyNormSq Y (B i) := by
    intro i _
    unfold windowEnergyNormSq windowPairing
    apply intervalIntegral.integral_congr; intro X _; ring
  have h1 :
      Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (fun X => A i X - B i X)) ≤
        Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (A i)) +
          Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (B i)) := by
    have h_rew :
        (∑ i ∈ S, windowEnergyNormSq Y (fun X => A i X - B i X)) =
          ∑ i ∈ S, windowEnergyNormSq Y (fun X => A i X + (-B i X)) :=
      Finset.sum_congr rfl (fun i _ => by simp [sub_eq_add_neg])
    rw [h_rew, ← Finset.sum_congr rfl h_negB]
    exact h_tri A (fun i X => -B i X) hA (fun i hi => (hB i hi).neg)
  have h2 :
      Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (A i)) ≤
        Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (fun X => A i X - B i X)) +
          Real.sqrt (∑ i ∈ S, windowEnergyNormSq Y (B i)) := by
    have h_rew :
        (∑ i ∈ S, windowEnergyNormSq Y (A i)) =
          ∑ i ∈ S, windowEnergyNormSq Y (fun X => (A i X - B i X) + B i X) := by
      apply Finset.sum_congr rfl; intro i _; simp
    rw [h_rew]
    exact h_tri (fun i X => A i X - B i X) B (fun i hi => (hA i hi).sub (hB i hi)) hB
  rw [abs_le]
  constructor <;> linarith

/-- **Theorem 4 (`TASK-TC-065` §5–§6, Coupled Mode Expansion, Unconditional General-Base & Canonical Cutoff-Fringe Bounds, Exact `E2` Feature Orthogonality & Large-Prime Station Disjointness, and Unconditional Small-Core Norm Bounds)**:
    1. *Exact coupled mode expansion identity (`2 ≤ Y`)*:
       For continuous `U_main + U_rem = U_Y` and `V_main + V_rem = V_Y` on `[Y, tau * Y]`,
       `dampedCoreDefectD = (‖U_main‖^2 - 4 ∑ ‖V_main‖^2) + (2 ⟨U_main, U_rem⟩ - 8 ∑ ⟨V_main, V_rem⟩) + (‖U_rem‖^2 - 4 ∑ ‖V_rem‖^2 - J_A)`;
    2. *Unconditional general-base (`w0 > 1`) & canonical (`w0 = tau`) fringe feature norm bounds (zero external premises)*:
       `∑_{pk} paramWindowNormSq Y w0 (fringeFeatureVectorG (canonicalCutoffT Y) pk) ≤ (8192 * w0^5 * log w0) / (log Y)^2 + (324 * w0^5 * log w0) / Y^(5/4)`
       for all real `w0 > 1`, `Y ≥ 2`, yielding the exact canonical norm coincidence
       `|√(∑_{pk} ‖V_{pk}‖_Y^2) - √(D_tilde(Y))| ≤ √((8192 * tau^5 * log tau)/(log Y)^2 + (324 * tau^5 * log tau)/Y^(5/4))`;
    3. *Unconditional scalar fringe norm bound (zero external premises)*:
       `∀ c_lam c_half : ℝ, ∃ C_fr ≥ 0, ∀ Y ≥ 2, ‖pairedCutoffFringeScalarPhi ...‖_Y^2 ≤ C_fr`;
    4. *Exact `E2` feature orthogonality (`⟨V_{> M, pk}, V_{≤ M, pk}⟩_Y = 0` and Pythagorean norm split) and station disjointness for distinct primes above `Nat.sqrt T`*;
    5. *Unconditional small-core norm bound*:
       `∀ c_lam c_half : ℝ, ∃ C_core ≥ 0, ∀ Y ≥ 2, ∀ M : ℕ`, both the truncated-core scalar norm squared and feature norm squared over `{a ∈ C_odd(T(Y)) : a ≤ M}` are bounded by `M * C_core * (1 + Real.log Y)`. -/
theorem coupled_mode_expansion_uniform_fringe_bounds_and_orthogonality_tc065 :
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ (c_lam c_half : ℝ) (T D0 : ℕ)
        (U_main U_rem : ℝ → ℝ) (V_main V_rem : ℕ × ℕ → ℝ → ℝ),
      ContinuousOn U_main (Set.uIcc Y (RiemannScope.tau * Y)) →
      ContinuousOn U_rem (Set.uIcc Y (RiemannScope.tau * Y)) →
      (∀ pk ∈ primePowerPairsUpTo T, ContinuousOn (V_main pk) (Set.uIcc Y (RiemannScope.tau * Y))) →
      (∀ pk ∈ primePowerPairsUpTo T, ContinuousOn (V_rem pk) (Set.uIcc Y (RiemannScope.tau * Y))) →
      (∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
        coreTotalScalarProfileU c_lam c_half T D0 X = U_main X + U_rem X) →
      (∀ pk ∈ primePowerPairsUpTo T, ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
        coreTotalFeatureVectorV T pk X = V_main pk X + V_rem pk X) →
      dampedCoreDefectD c_lam c_half T D0 Y =
        (windowEnergyNormSq Y U_main -
            4 * ∑ pk ∈ primePowerPairsUpTo T, windowEnergyNormSq Y (V_main pk)) +
          (2 * windowPairing Y U_main U_rem -
            8 * ∑ pk ∈ primePowerPairsUpTo T, windowPairing Y (V_main pk) (V_rem pk)) +
          (windowEnergyNormSq Y U_rem -
            4 * ∑ pk ∈ primePowerPairsUpTo T, windowEnergyNormSq Y (V_rem pk) -
            coreScalarDiagJA c_lam c_half T D0 Y)) ∧
    ((∀ {w0 Y : ℝ}, 1 < w0 → 2 ≤ Y →
        let T := canonicalCutoffT Y
        (∑ pk ∈ primePowerPairsUpTo T, paramWindowNormSq Y w0 (fringeFeatureVectorG T pk)) ≤
          (8192 * w0 ^ 5 * Real.log w0) / (Real.log Y) ^ 2 +
            (324 * w0 ^ 5 * Real.log w0) / Y ^ (5 / 4 : ℝ)) ∧
      (∀ {Y : ℝ}, 2 ≤ Y →
        |Real.sqrt (∑ pk ∈ primePowerPairsUpTo (canonicalCutoffT Y),
            windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV (canonicalCutoffT Y) pk X)) -
          Real.sqrt (canonicalPrimePowerDiagDtilde Y)| ≤
          Real.sqrt ((8192 * RiemannScope.tau ^ 5 * Real.log RiemannScope.tau) / (Real.log Y) ^ 2 +
            (324 * RiemannScope.tau ^ 5 * Real.log RiemannScope.tau) / Y ^ (5 / 4 : ℝ)))) ∧
    (∀ c_lam c_half : ℝ,
      ∃ C_fr : ℝ, 0 ≤ C_fr ∧
        ∀ {Y : ℝ}, 2 ≤ Y →
          windowEnergyNormSq Y
              (pairedCutoffFringeScalarPhi c_lam c_half
                (canonicalCutoffT Y) (Nat.floor (Real.log Y))) ≤
            C_fr) ∧
    ((∀ {Y : ℝ}, 2 ≤ Y → ∀ (T M : ℕ),
        (∀ pk ∈ primePowerPairsUpTo T,
          windowPairing Y (splitFeatureHighV T M pk) (splitFeatureLowV T M pk) = 0) ∧
        (∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (coreTotalFeatureVectorV T pk)) =
          (∑ pk ∈ primePowerPairsUpTo T, windowEnergyNormSq Y (splitFeatureHighV T M pk)) +
            (∑ pk ∈ primePowerPairsUpTo T, windowEnergyNormSq Y (splitFeatureLowV T M pk))) ∧
      (∀ {T p1 p2 n : ℕ}, Nat.Prime p1 → Nat.Prime p2 → p1 ≠ p2 →
        Nat.sqrt T < p1 → Nat.sqrt T < p2 → p1 ∣ n → p2 ∣ n → n ∈ Finset.Icc 1 T → False)) ∧
    (∀ c_lam c_half : ℝ,
      ∃ C_core : ℝ, 0 ≤ C_core ∧
        ∀ {Y : ℝ}, 2 ≤ Y → ∀ (M : ℕ),
          let T := canonicalCutoffT Y
          let D0 := Nat.floor (Real.log Y)
          let C_sm := (oddSquarefreeCores T).filter (fun a => a ≤ M)
          windowEnergyNormSq Y
              (fun X => ∑ a ∈ C_sm,
                (ArithmeticFunction.moebius a : ℝ) * coreAdjustedProfileA c_lam c_half T D0 a X) ≤
            (M : ℝ) * C_core * (1 + Real.log Y) ∧
          (∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y
              (fun X => ∑ a ∈ C_sm,
                (ArithmeticFunction.moebius a : ℝ) * coreFeatureVectorB a T pk X)) ≤
            (M : ℝ) * C_core * (1 + Real.log Y)) := by
  refine ⟨?_, ⟨fun hw0 hY2 => fringe_feature_paramWindowNormSq_bound_tc065_aux hw0 hY2, ?_⟩,
    fun c_lam c_half => scalar_fringe_uniform_bound_tc065_aux c_lam c_half,
    ⟨?_, ?_⟩, ?_⟩
  · -- Part 1: Coupled mode expansion
    intro Y hY2 c_lam c_half T D0 U_main U_rem V_main V_rem hUm_c hUr_c hVm_c hVr_c hU_sum hV_sum
    have hY0 : 0 < Y := by linarith
    have hU_norm :
        windowEnergyNormSq Y (coreTotalScalarProfileU c_lam c_half T D0) =
          windowEnergyNormSq Y U_main + 2 * windowPairing Y U_main U_rem +
            windowEnergyNormSq Y U_rem := by
      rw [← windowEnergyNormSq_add_eq_tc065_aux hY0 hUm_c hUr_c]
      unfold windowEnergyNormSq windowPairing
      apply intervalIntegral.integral_congr
      intro X hX; dsimp only; rw [hU_sum X hX]
    have hV_norm :
        ∀ pk ∈ primePowerPairsUpTo T,
          windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV T pk X) =
            windowEnergyNormSq Y (V_main pk) + 2 * windowPairing Y (V_main pk) (V_rem pk) +
              windowEnergyNormSq Y (V_rem pk) := by
      intro pk hpk
      rw [← windowEnergyNormSq_add_eq_tc065_aux hY0 (hVm_c pk hpk) (hVr_c pk hpk)]
      unfold windowEnergyNormSq windowPairing
      apply intervalIntegral.integral_congr
      intro X hX; dsimp only; rw [hV_sum pk hpk X hX]
    rw [(dampedCoreDefectD_identities_tc065_aux hY2 c_lam c_half T D0).1, hU_norm,
      Finset.sum_congr rfl hV_norm, Finset.sum_add_distrib, Finset.sum_add_distrib,
      ← Finset.mul_sum]
    ring
  · -- Part 2b: Canonical norm coincidence
    intro Y hY2
    have hY0 : 0 < Y := by linarith
    have htau := tau_gt_one_and_lt_eight_tc065_aux.1
    let T := canonicalCutoffT Y
    have hT1 : 1 ≤ T := (log_canonicalCutoffT_bounds_tc065_aux hY2).1
    obtain ⟨_, _, _, _, _, _, _, _, _, _, hGfull_c, hGfr_c⟩ :=
      continuousOn_core_objects_tc065_aux hY2 htau 0 0 T 0
    have hV_eq_diff :
        (∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => coreTotalFeatureVectorV T pk X)) =
          ∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => fullFeatureVectorG T pk X - fringeFeatureVectorG T pk X) := by
      apply Finset.sum_congr rfl
      intro pk hpk
      unfold windowEnergyNormSq windowPairing
      apply intervalIntegral.integral_congr
      intro X hX
      dsimp only
      have hv := (((paired_station_partition_divisor_synthesis_and_telescoping_tc065).2.2.2.1
        hY2 hT1 0 0 0 X hX).2.1 pk hpk).2.1
      rw [hv]
    have hD_eq :
        canonicalPrimePowerDiagDtilde Y =
          ∑ pk ∈ primePowerPairsUpTo T, windowEnergyNormSq Y (fullFeatureVectorG T pk) := by
      unfold canonicalPrimePowerDiagDtilde
      exact (fullFeatureVectorG_norm_sum_eq_Dtilde_tc065_aux hY2 hT1).symm
    have h_tri := direct_sum_reverse_triangle_tc065_aux hY0 (primePowerPairsUpTo T)
      (fullFeatureVectorG T) (fringeFeatureVectorG T) (fun pk _ => hGfull_c pk) (fun pk _ => hGfr_c pk)
    rw [← hV_eq_diff, ← hD_eq] at h_tri
    have h_bd := fringe_feature_paramWindowNormSq_bound_tc065_aux htau hY2
    exact le_trans h_tri (Real.sqrt_le_sqrt h_bd)
  · -- Part 4a: Exact E2 feature orthogonality
    intro Y _hY2 T M
    refine ⟨?_, ?_⟩
    · intro pk _
      unfold windowPairing splitFeatureHighV splitFeatureLowV
      have h0 :
          (fun X => (if M < pk.1 ^ pk.2 then coreTotalFeatureVectorV T pk X else 0) *
            (if pk.1 ^ pk.2 ≤ M then coreTotalFeatureVectorV T pk X else 0) / X) =
            fun _ => 0 := by
        ext X
        by_cases h : M < pk.1 ^ pk.2
        · have hnot : ¬ pk.1 ^ pk.2 ≤ M := not_le.mpr h
          simp [h, hnot]
        · have hle : pk.1 ^ pk.2 ≤ M := not_lt.mp h
          simp [h, hle]
      rw [h0, intervalIntegral.integral_zero]
    · rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro pk _
      unfold splitFeatureHighV splitFeatureLowV
      by_cases h : M < pk.1 ^ pk.2
      · have hnot : ¬ pk.1 ^ pk.2 ≤ M := not_le.mpr h
        simp only [h, hnot, ↓reduceIte]
        have hz : windowEnergyNormSq Y (fun _ => 0) = 0 := by
          unfold windowEnergyNormSq windowPairing; simp
        rw [hz, add_zero]
      · have hle : pk.1 ^ pk.2 ≤ M := not_lt.mp h
        simp only [h, hle, ↓reduceIte]
        have hz : windowEnergyNormSq Y (fun _ => 0) = 0 := by
          unfold windowEnergyNormSq windowPairing; simp
        rw [hz, zero_add]
  · -- Part 4b: Station disjointness above Nat.sqrt T
    intro T p1 p2 n hp1 hp2 hne hgt1 hgt2 hd1 hd2 hn
    obtain ⟨hn1, hnT⟩ := Finset.mem_Icc.mp hn
    have hcop : Nat.Coprime p1 p2 := (Nat.coprime_primes hp1 hp2).mpr hne
    have hmul_dvd : p1 * p2 ∣ n := hcop.mul_dvd_of_dvd_of_dvd hd1 hd2
    have hmul_le : p1 * p2 ≤ T := le_trans (Nat.le_of_dvd hn1 hmul_dvd) hnT
    have hsq_lt : T < (Nat.sqrt T + 1) * (Nat.sqrt T + 1) := Nat.lt_succ_sqrt T
    have h_le1 : Nat.sqrt T + 1 ≤ p1 := hgt1
    have h_le2 : Nat.sqrt T + 1 ≤ p2 := hgt2
    have h_le_prod : (Nat.sqrt T + 1) * (Nat.sqrt T + 1) ≤ p1 * p2 :=
      Nat.mul_le_mul h_le1 h_le2
    omega
  · -- Part 5: Unconditional small-core norm bound
    intro c_lam c_half
    obtain ⟨C_core, hC_nn, h_diag_bd, _⟩ :=
      (damped_core_defect_and_closure_equivalence_tc065).2 c_lam c_half
    refine ⟨C_core, hC_nn, ?_⟩
    intro Y hY2 M T D0 C_sm
    have hY0 : 0 < Y := by linarith
    have htau := tau_gt_one_and_lt_eight_tc065_aux.1
    obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc065_aux hY2
    obtain ⟨_, _, _, hA_c, hB_c, _, _, _, _, _, _, _⟩ :=
      continuousOn_core_objects_tc065_aux hY2 htau c_lam c_half T D0
    have h_card_le : (C_sm.card : ℝ) ≤ (M : ℝ) := by
      have h_sub : C_sm ⊆ Finset.Icc 1 M := by
        intro a ha
        simp only [C_sm, oddSquarefreeCores, Finset.mem_filter, Finset.mem_Icc] at ha ⊢
        exact ⟨ha.1.1.1, ha.2⟩
      have hc : C_sm.card ≤ M := by
        calc C_sm.card ≤ (Finset.Icc 1 M).card := Finset.card_le_card h_sub
          _ = M := by simp
      exact_mod_cast hc
    have h_cs_window :
        ∀ (f : ℕ → ℝ → ℝ),
          (∀ a ∈ C_sm, ContinuousOn (f a) (Set.uIcc Y (RiemannScope.tau * Y))) →
          windowEnergyNormSq Y
              (fun X => ∑ a ∈ C_sm, (ArithmeticFunction.moebius a : ℝ) * f a X) ≤
            (M : ℝ) * ∑ a ∈ C_sm, windowEnergyNormSq Y (f a) := by
      intro f hf_c
      have hsum_c :
          ContinuousOn (fun X => ∑ a ∈ C_sm, (ArithmeticFunction.moebius a : ℝ) * f a X)
            (Set.uIcc Y (RiemannScope.tau * Y)) :=
        continuousOn_finset_sum _ (fun a ha => continuousOn_const.mul (hf_c a ha))
      have h_int_f :
          ∀ a ∈ C_sm,
            IntervalIntegrable (fun X => f a X * f a X / X) volume Y (RiemannScope.tau * Y) :=
        fun a ha => (((hf_c a ha).mul (hf_c a ha)).div continuousOn_id
          (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
      have h_int_rhs :
          IntervalIntegrable (fun X => (C_sm.card : ℝ) * (∑ a ∈ C_sm, (f a X) ^ 2) / X)
            volume Y (RiemannScope.tau * Y) :=
        ((continuousOn_const.mul
          (continuousOn_finset_sum _ (fun a ha => (hf_c a ha).pow 2))).div continuousOn_id
          (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
      have h_rhs_eq :
          (C_sm.card : ℝ) * ∑ a ∈ C_sm, windowEnergyNormSq Y (f a) =
            ∫ X in Y..(RiemannScope.tau * Y),
              (C_sm.card : ℝ) * (∑ a ∈ C_sm, (f a X) ^ 2) / X := by
        unfold windowEnergyNormSq windowPairing
        rw [← intervalIntegral.integral_finset_sum h_int_f, ← intervalIntegral.integral_const_mul]
        apply intervalIntegral.integral_congr
        intro X _
        dsimp only
        rw [Finset.mul_sum, Finset.mul_sum, Finset.sum_div]
        apply Finset.sum_congr rfl; intro a _; ring
      have h_le_card :
          windowEnergyNormSq Y
              (fun X => ∑ a ∈ C_sm, (ArithmeticFunction.moebius a : ℝ) * f a X) ≤
            (C_sm.card : ℝ) * ∑ a ∈ C_sm, windowEnergyNormSq Y (f a) := by
        rw [h_rhs_eq]
        unfold windowEnergyNormSq windowPairing
        apply intervalIntegral.integral_mono_on hle
          (((hsum_c.mul hsum_c).div continuousOn_id
            (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable)
          h_int_rhs
        intro X hX
        change ((∑ a ∈ C_sm, (ArithmeticFunction.moebius a : ℝ) * f a X) *
            (∑ a ∈ C_sm, (ArithmeticFunction.moebius a : ℝ) * f a X)) / X ≤
          (C_sm.card : ℝ) * (∑ a ∈ C_sm, (f a X) ^ 2) / X
        have hX0 : 0 < X := lt_of_lt_of_le hY0 hX.1
        have h_cs := Finset.sum_mul_sq_le_sq_mul_sq C_sm
          (fun a => (ArithmeticFunction.moebius a : ℝ)) (fun a => f a X)
        have h_mu_card :
            (∑ a ∈ C_sm, (ArithmeticFunction.moebius a : ℝ) ^ 2) = (C_sm.card : ℝ) := by
          have h_each : ∀ a ∈ C_sm, (ArithmeticFunction.moebius a : ℝ) ^ 2 = 1 := by
            intro a ha
            have ha_sf : Squarefree a :=
              (Finset.mem_filter.mp (Finset.mem_filter.mp ha).1).2.2.1
            exact ((exact_odd_squarefree_core_bijection_and_complete_kernel_split_tc064).1.2
              ha_sf (le_refl 1)).2
          rw [Finset.sum_congr rfl h_each, Finset.sum_const, nsmul_eq_mul, mul_one]
        rw [h_mu_card] at h_cs
        rw [← sq]
        exact div_le_div_of_nonneg_right h_cs (le_of_lt hX0)
      exact le_trans h_le_card
        (mul_le_mul_of_nonneg_right h_card_le
          (Finset.sum_nonneg (fun a _ => windowEnergyNormSq_nonneg_tc065_aux hY0 _)))
    have h_diag_nn := (dampedCoreDefectD_identities_tc065_aux hY2 c_lam c_half T D0).2.2
    have h_sub_cores : C_sm ⊆ oddSquarefreeCores T := Finset.filter_subset _ _
    have h_bd_Y := h_diag_bd hY2
    refine ⟨?_, ?_⟩
    · calc
        windowEnergyNormSq Y
            (fun X => ∑ a ∈ C_sm,
              (ArithmeticFunction.moebius a : ℝ) * coreAdjustedProfileA c_lam c_half T D0 a X)
          ≤ (M : ℝ) * ∑ a ∈ C_sm, windowEnergyNormSq Y (coreAdjustedProfileA c_lam c_half T D0 a) :=
            h_cs_window (fun a => coreAdjustedProfileA c_lam c_half T D0 a) (fun a _ => hA_c a)
        _ ≤ (M : ℝ) * coreScalarDiagJA c_lam c_half T D0 Y :=
            mul_le_mul_of_nonneg_left
              (Finset.sum_le_sum_of_subset_of_nonneg h_sub_cores
                (fun _ _ _ => windowEnergyNormSq_nonneg_tc065_aux hY0 _)) (Nat.cast_nonneg M)
        _ ≤ (M : ℝ) * (C_core * (1 + Real.log Y)) :=
            mul_le_mul_of_nonneg_left (by linarith [h_bd_Y, h_diag_nn.2]) (Nat.cast_nonneg M)
        _ = (M : ℝ) * C_core * (1 + Real.log Y) := by ring
    · calc
        (∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y
              (fun X => ∑ a ∈ C_sm,
                (ArithmeticFunction.moebius a : ℝ) * coreFeatureVectorB a T pk X))
          ≤ ∑ pk ∈ primePowerPairsUpTo T,
              (M : ℝ) * ∑ a ∈ C_sm, windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X) :=
            Finset.sum_le_sum (fun pk _ =>
              h_cs_window (fun a => coreFeatureVectorB a T pk) (fun a _ => hB_c a pk))
        _ = (M : ℝ) * ∑ a ∈ C_sm, ∑ pk ∈ primePowerPairsUpTo T,
              windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X) := by
            rw [← Finset.mul_sum, Finset.sum_comm]
        _ ≤ (M : ℝ) * coreFeatureDiagJB T Y :=
            mul_le_mul_of_nonneg_left
              (Finset.sum_le_sum_of_subset_of_nonneg h_sub_cores
                (fun _ _ _ => Finset.sum_nonneg (fun _ _ => windowEnergyNormSq_nonneg_tc065_aux hY0 _)))
              (Nat.cast_nonneg M)
        _ ≤ (M : ℝ) * (C_core * (1 + Real.log Y)) :=
            mul_le_mul_of_nonneg_left (by linarith [h_bd_Y, h_diag_nn.1]) (Nat.cast_nonneg M)
        _ = (M : ℝ) * C_core * (1 + Real.log Y) := by ring

/-! ### Section 5: Bare-Liouville Shifted-Dilation Closure Without `PREM-07` and Section 9 Euler Multiplier Limit (`TASK-TC-065` §7, §9) -/

/-- **Theorem 5 (`TASK-TC-065` §7 & §9, Direct Bare-Liouville Shifted-Dilation Closure Transfer Without `PREM-07`, Converse Implication, and Nonzero Finite Euler Multiplier Limit vs. Zero Modified Liouville Quotient Limit at `z = 1`)**:
    1. *Direct conditional Route D closure transfer for `E_λ - 4 * D_tilde` using ONLY `PREM-04..06`* (no `knownCompensatedD2Part` / `PREM-07` hypothesis):
       Under `0 ≤ M_lin`, `canonicalLiouvilleEnergyE Z ≤ M_lin * Z` (`1 ≤ Z`),
       `MixedCovarianceClosureHypothesis (fun Y => canonicalLiouvilleEnergyE Y - 4 * canonicalPrimePowerDiagDtilde Y) canonicalPrimePowerDiagDtilde`,
       and `PREM-05` + `PREM-06`, we obtain
       `∀ ε > 0, ∃ C_tot ≥ 0, ∀ Z ≥ 1, canonicalLiouvilleEnergyE Z ≤ C_tot * Z ^ ε`;
    2. *Converse implication*:
       Subpower window energy `∀ ε > 0, ∃ C_tot ≥ 0, ∀ Z ≥ 1, canonicalLiouvilleEnergyE Z ≤ C_tot * Z ^ ε`
       implies `MixedCovarianceClosureHypothesis (fun Y => canonicalLiouvilleEnergyE Y - 4 * canonicalPrimePowerDiagDtilde Y) canonicalPrimePowerDiagDtilde`;
    3. *Section 9 clarification at `z = (1 : ℂ) + (0 : ℂ) * Complex.I = 1`*:
       For every finite set `S : Finset ℕ` of odd primes (`∀ q ∈ S, Nat.Prime q ∧ Odd q`),
       - `∏_{q ∈ S} ((q + 1) / (q - 1)) ≠ 0`;
       - `finiteEulerMultiplierM S w → ∏_{q ∈ S} ((q + 1) / (q - 1))` as `w → 1`;
       - `(riemannZeta (2 * w) / riemannZeta w) * finiteEulerMultiplierM S w → 0` along `nhdsWithin 1 {1}ᶜ`. -/
theorem bare_liouville_shifted_dilation_closure_and_euler_limit_tc065 :
    (∀ {M_lin : ℝ},
      0 ≤ M_lin →
      (∀ Z : ℝ, 1 ≤ Z → canonicalLiouvilleEnergyE Z ≤ M_lin * Z) →
      MixedCovarianceClosureHypothesis
        (fun Y => canonicalLiouvilleEnergyE Y - 4 * canonicalPrimePowerDiagDtilde Y)
        canonicalPrimePowerDiagDtilde →
      (∀ ε : ℝ, 0 < ε →
        ∃ zeta2_eps C_cut Y_diag : ℝ,
          0 ≤ zeta2_eps ∧ 0 ≤ C_cut ∧ Real.exp 1 ≤ Y_diag ∧
            (∀ Y : ℝ, 1 ≤ Y →
              (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
                (Real.log (pk.1 : ℝ)) ^ 2 / (primePowerScale pk) ^ (1 + ε)) ≤ zeta2_eps) ∧
            (∀ Y : ℝ, Y_diag ≤ Y →
              canonicalPrimePowerDiagDtilde Y ≤
                (2 / (Real.log Y) ^ 2) *
                  (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
                    primePowerDiagWeight pk *
                      monotoneScaleEnvelope canonicalLiouvilleEnergyE (Y / primePowerScale pk)) +
                  C_cut)) →
      ∀ ε : ℝ, 0 < ε →
        ∃ C_tot : ℝ, 0 ≤ C_tot ∧ ∀ Z : ℝ, 1 ≤ Z → canonicalLiouvilleEnergyE Z ≤ C_tot * Z ^ ε) ∧
    ((∀ ε : ℝ, 0 < ε →
        ∃ C_tot : ℝ, 0 ≤ C_tot ∧ ∀ Z : ℝ, 1 ≤ Z → canonicalLiouvilleEnergyE Z ≤ C_tot * Z ^ ε) →
      MixedCovarianceClosureHypothesis
        (fun Y => canonicalLiouvilleEnergyE Y - 4 * canonicalPrimePowerDiagDtilde Y)
        canonicalPrimePowerDiagDtilde) ∧
    (∀ (S : Finset ℕ), (∀ q ∈ S, Nat.Prime q ∧ Odd q) →
      (∏ q ∈ S, ((q : ℂ) + 1) / ((q : ℂ) - 1)) ≠ 0 ∧
        Filter.Tendsto (finiteEulerMultiplierM S) (nhds (1 : ℂ))
          (nhds (∏ q ∈ S, ((q : ℂ) + 1) / ((q : ℂ) - 1))) ∧
        Filter.Tendsto
          (fun w : ℂ => (riemannZeta (2 * w) / riemannZeta w) * finiteEulerMultiplierM S w)
          (nhdsWithin (1 : ℂ) {(1 : ℂ)}ᶜ) (nhds (0 : ℂ))) := by
  have hE_nn : ∀ Z : ℝ, 1 ≤ Z → 0 ≤ canonicalLiouvilleEnergyE Z := by
    intro Z hZ1
    unfold canonicalLiouvilleEnergyE actualWindowEnergyE
    exact windowEnergyNormSq_nonneg_tc065_aux (by linarith) _
  have hD_nn : ∀ {Y : ℝ}, 2 ≤ Y → 0 ≤ canonicalPrimePowerDiagDtilde Y :=
    fun hY2 => (signed_remainder_equivalence_and_sufficient_core_relaxation_tc061r).1.2.1 hY2
  have h2_le_exp1 : (2 : ℝ) ≤ Real.exp 1 := by linarith [Real.add_one_le_exp (1 : ℝ)]
  refine ⟨?_, ?_, ?_⟩
  · -- Part 1: Direct Route D closure transfer without PREM-07
    intro M_lin hM_nn hM_lin hJ_cl h_prem
    let J_half : ℝ → ℝ := fun Y =>
      (1 / 2 : ℝ) * (canonicalLiouvilleEnergyE Y - 4 * canonicalPrimePowerDiagDtilde Y)
    have hJ_half_cl : MixedCovarianceClosureHypothesis J_half canonicalPrimePowerDiagDtilde := by
      intro η hη
      obtain ⟨a_eta, b_eta, κ_eta, Y_eta, ha, hb, hκ_pos, hκ_le2, hYe, hbd⟩ := hJ_cl η hη
      refine ⟨a_eta / 2, b_eta / 2, κ_eta, Y_eta, by linarith, by linarith, hκ_pos, hκ_le2, hYe, ?_⟩
      intro Y hYYe
      have h1 := hbd Y hYYe
      dsimp only at h1
      dsimp [J_half]
      linarith
    exact (mixed_covariance_hypothesis_route_d_closure_transfer_tc061).2.2.1
      (E := canonicalLiouvilleEnergyE) (D_tilde := canonicalPrimePowerDiagDtilde)
      (J := J_half) (A_sq := fun _ => 0)
      hE_nn hM_nn hM_lin hJ_half_cl
      (by
        intro ε hε
        obtain ⟨zeta2_eps, C_cut, Y_diag, hz_nn, hC_nn, hYd_ge, h_zeta, h_diag⟩ := h_prem ε hε
        refine ⟨zeta2_eps, C_cut, Y_diag, 0, 0, 1,
          hz_nn, hC_nn, hYd_ge, le_refl 0, le_refl 0, zero_lt_one, h_zeta, h_diag, ?_, ?_⟩
        · intro R Y _ _; simp
        · intro Y hYYd
          have hY2 : 2 ≤ Y := le_trans h2_le_exp1 (le_trans hYd_ge hYYd)
          dsimp [J_half]
          linarith [hD_nn hY2])
  · -- Part 2: Converse implication
    intro h_sub η hη
    obtain ⟨C_tot, hC_nn, hE_bd⟩ := h_sub η hη
    refine ⟨C_tot, 0, 1, 2, hC_nn, le_refl 0, zero_lt_one, by norm_num, le_refl 2, ?_⟩
    intro Y hY2
    dsimp only
    have h1 := hE_bd Y (by linarith)
    have h2 := hD_nn hY2
    linarith
  · -- Part 3: Section 9 finite Euler multiplier limit vs modified Liouville quotient limit at z = 1
    intro S hS
    have h_factor_ne : ∀ q ∈ S, (((q : ℂ) + 1) / ((q : ℂ) - 1)) ≠ 0 := by
      intro q hq
      have hq_pr : Nat.Prime q := (hS q hq).1
      have hq_ge2 : 2 ≤ q := hq_pr.two_le
      have hnum_ne : ((q : ℂ) + 1) ≠ 0 := by
        have h : ((q + 1 : ℕ) : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
        simpa [Nat.cast_add] using h
      have hden_ne : ((q : ℂ) - 1) ≠ 0 := by
        have h : ((q - 1 : ℕ) : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
        rwa [Nat.cast_sub (by omega : 1 ≤ q), Nat.cast_one] at h
      exact div_ne_zero hnum_ne hden_ne
    have h_prod_ne : (∏ q ∈ S, ((q : ℂ) + 1) / ((q : ℂ) - 1)) ≠ 0 :=
      Finset.prod_ne_zero_iff.mpr h_factor_ne
    have h_factor_tendsto :
        ∀ q ∈ S,
          Filter.Tendsto (fun w : ℂ => (1 + (q : ℂ) ^ (-w)) / (1 - (q : ℂ) ^ (-w)))
            (nhds (1 : ℂ)) (nhds (((q : ℂ) + 1) / ((q : ℂ) - 1))) := by
      intro q hq
      obtain ⟨hq_pr, hq_odd⟩ := hS q hq
      have h_diff_on :
          DifferentiableOn ℂ (fun w : ℂ => (1 + (q : ℂ) ^ (-w)) / (1 - (q : ℂ) ^ (-w)))
            {w : ℂ | 0 < w.re} :=
        ((finite_euler_factor_dirichlet_multiplier_and_dilation_equivalence_tc064).2.1
          hq_pr hq_odd).2.1.2.1
      have h_open : IsOpen {w : ℂ | 0 < w.re} := isOpen_lt continuous_const Complex.continuous_re
      have h1_mem : (1 : ℂ) ∈ {w : ℂ | 0 < w.re} := by simp
      have h_cont_at :
          ContinuousAt (fun w : ℂ => (1 + (q : ℂ) ^ (-w)) / (1 - (q : ℂ) ^ (-w))) (1 : ℂ) :=
        (h_diff_on.differentiableAt (h_open.mem_nhds h1_mem)).continuousAt
      have h_val_at_1 :
          (1 + (q : ℂ) ^ (-(1 : ℂ))) / (1 - (q : ℂ) ^ (-(1 : ℂ))) =
            ((q : ℂ) + 1) / ((q : ℂ) - 1) := by
        have hq_ne : (q : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr hq_pr.ne_zero
        have hqm1_ne : (q : ℂ) - 1 ≠ 0 := by
          have h : ((q - 1 : ℕ) : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr (by have := hq_pr.two_le; omega)
          rwa [Nat.cast_sub (by have := hq_pr.two_le; omega : 1 ≤ q), Nat.cast_one] at h
        rw [Complex.cpow_neg_one]
        field_simp [hq_ne, hqm1_ne]
      simpa [h_val_at_1] using h_cont_at.tendsto
    have h_M_tendsto :
        Filter.Tendsto (finiteEulerMultiplierM S) (nhds (1 : ℂ))
          (nhds (∏ q ∈ S, ((q : ℂ) + 1) / ((q : ℂ) - 1))) := by
      unfold finiteEulerMultiplierM
      exact tendsto_finset_prod S h_factor_tendsto
    have h_zeta_tendsto :
        Filter.Tendsto (fun w : ℂ => riemannZeta (2 * w) / riemannZeta w)
          (nhdsWithin (1 : ℂ) {(1 : ℂ)}ᶜ) (nhds (0 : ℂ)) :=
      (finite_euler_factor_dirichlet_multiplier_and_dilation_equivalence_tc064).1
    have h_prod_tendsto :
        Filter.Tendsto
          (fun w : ℂ => (riemannZeta (2 * w) / riemannZeta w) * finiteEulerMultiplierM S w)
          (nhdsWithin (1 : ℂ) {(1 : ℂ)}ᶜ) (nhds (0 : ℂ)) := by
      have h_mul := h_zeta_tendsto.mul (h_M_tendsto.mono_left nhdsWithin_le_nhds)
      simpa using h_mul
    exact ⟨h_prod_ne, h_M_tendsto, h_prod_tendsto⟩

end RiemannScope
