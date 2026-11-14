/-
RiemannScope.SignedDilationArithmeticEnergy
TASK-TC-060: Signed Dilation Multipliers and Arithmetic Control of the Complete Reconstruction
toward SUBGATE-TC-043A.

Formalizes in Lean 4 (complete machine-checked proofs with canonical circle constant
RiemannScope.tau throughout):
1. `noncircular_reassembly_and_basis_stratification_tc060`:
   Exact finite reassembly of `smoothRemainderSumRsm`, `jumpRemainderSumRjump`, and
   `endpointRemainderTerm` (`T = 0, 1` safe), exact relation to `compensatedSelbergResidualD2` and
   `P_T - R_T = D_{2,T}`, and exact `gaussianTermPhi n` basis stratification on `1 ≤ n ≤ 2 * T`
   with closed formulas on `1 ≤ n ≤ T - 1`, at `n = T`, and at `n = 2 * T`.
2. `adjacent_dilation_multiplier_and_cutoff_blocks_tc060`:
   Exact `t^(-3/2)` integral benchmark, elementary sharp-order multiplier norm bound
   `min (1/√d + 1/√(d+1)) (√(1/4 + v^2) * 2 * (1/√d - 1/√(d+1)))`, resonant odd-harmonic
   attainment using `RiemannScope.tau`, level-set block partition `cutoffLevelBlock T L` with
   empty-block witness `cutoffLevelBlock 2 1 = ∅`, Fourier and real-space block groupings, and
   `Nat.sqrt T - 1` nonempty-block lower bound.
3. `signed_gram_kernel_and_log_weighted_quadratic_form_tc060`:
   Parameterized `[Y, b * Y]` window pairing (`b = RiemannScope.tau` recovering `windowPairing`
   and `windowKernelK`), 4-term signed Gram kernel `signedSmoothGramH`, PSD real-space quadratic
   form, `(log X)^(-2)` weighted Gram kernel `weightedSignedSmoothGramH`, and two-sided logarithmic
   window norm sandwich on `[Y, b * Y]` (`Y ≥ 2, b > 1`).
4. `gaussian_window_majorant_and_local_frequency_split_tc060`:
   Gaussian Schwartz window majorant on `[log Y, log (b * Y)]`, local-window frequency-split
   cross-term retention and Minkowski square bound, and Gauss-product Gamma-factor algebraic
   monotonicity for `m ≥ 3 / 4, u ≥ 0`.
5. `second_order_drift_abel_and_small_divisor_contraction_tc060`:
   Second-order drift/oscillatory split for `smoothRemainderSumRsm`, exact Abel summation-by-parts
   reassembly of smooth drift, elementary properties and difference bound for `squarePoleDriftM`,
   sub-unit scale separation at `Nat.floor Y`, and small-divisor weighted window-norm bound.
6. `complete_reconstruction_drift_contraction_transfer_tc060`:
   Lossless decomposition `compensatedSelbergResidualD2 = knownCompensatedD2Part + openCoreOscShiftD2Part`
   and `Q_T = 2 P_T - K_known - R_open`, complete `(8, 4, 4)` window energy inequality, and
   `R`-independent threshold `Y_star` finite-horizon feedback contraction (`1/4 + 1/4 + 1/4 = 3/4`)
   transferring conditional open-core control to `E(Y) ≤ C_tot * Y^ε`.
-/

import RiemannScope.DyadicPowerLiftPrimitiveCorrelation

open scoped ArithmeticFunction BigOperators Classical
open MeasureTheory intervalIntegral

namespace RiemannScope
namespace SignedDilationArithmeticEnergy

open RiemannScope.LiouvilleSquareDilation
open RiemannScope.DyadicPowerLiftPrimitiveCorrelation

/-! ### Section 1: Noncircular Reassembly and Exact Basis Stratification (`TASK-TC-060` §1) -/

/-- Smooth kernel-variation remainder sum
    `R_{2,T}^{sm}(X; c_lam) := ∑_{1 ≤ d ≤ T - 1} R_2^{int}(d; c_lam) Δ_d^{sm}(X; T)`. -/
noncomputable def smoothRemainderSumRsm (c_lam : ℝ) (T : ℕ) (X : ℝ) : ℝ :=
  ∑ d ∈ Finset.Icc 1 (T - 1), selbergCenteredRemainderInt c_lam d * scaledFiberSmoothStep T d X

/-- Discrete inner-cutoff jump remainder sum
    `R_{2,T}^{jump}(X; c_lam) := ∑_{1 ≤ d ≤ T - 1} R_2^{int}(d; c_lam) Δ_d^{jump}(X; T)`. -/
noncomputable def jumpRemainderSumRjump (c_lam : ℝ) (T : ℕ) (X : ℝ) : ℝ :=
  ∑ d ∈ Finset.Icc 1 (T - 1), selbergCenteredRemainderInt c_lam d * scaledFiberCutoffJump T d X

/-- Total-endpoint remainder term safe at `T = 0` (never evaluating `gaussianTermPhi 0` at `T = 0`):
    `0` if `T = 0`, and `R_2^{int}(T; c_lam) * φ_T(X)` for `T ≥ 1`. -/
noncomputable def endpointRemainderTerm (c_lam : ℝ) (T : ℕ) (X : ℝ) : ℝ :=
  if T = 0 then 0 else selbergCenteredRemainderInt c_lam T * gaussianTermPhi T X

/-- Exact `gaussianTermPhi n` basis coefficient `α_{T,n}(c_lam)` of `smoothRemainderSumRsm c_lam T X`
    on `1 ≤ n ≤ 2 * T`. -/
noncomputable def smoothBasisCoeffAlpha (c_lam : ℝ) (T n : ℕ) : ℝ :=
  (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ n ∧ n / d ≤ T / d),
      selbergCenteredRemainderInt c_lam d * (liouvilleLambda (n / d) : ℝ)) -
    (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ n ∧ n / (d + 1) ≤ T / d),
      selbergCenteredRemainderInt c_lam d * (liouvilleLambda (n / (d + 1)) : ℝ))

private theorem abs_sin_le_abs_tc060_aux (x : ℝ) : |Real.sin x| ≤ |x| := by
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
      · intro t _
        rw [(hf₁_deriv t).deriv]
        linarith [(h_cos_bds t).2]
    have hf₁_0 : f₁ 0 = 0 := by simp [f₁]
    have h_ub : Real.sin y ≤ y := by
      have h := hf₁_mono Set.left_mem_Ici hy hy
      rw [hf₁_0] at h
      dsimp [f₁] at h
      linarith
    let f₂ : ℝ → ℝ := fun t => t + Real.sin t
    have hf₂_cont : ContinuousOn f₂ (Set.Ici 0) :=
      continuousOn_id.add Real.continuous_sin.continuousOn
    have hf₂_deriv : ∀ t : ℝ, HasDerivAt f₂ (1 + Real.cos t) t :=
      fun t => (hasDerivAt_id t).add (Real.hasDerivAt_sin t)
    have hf₂_mono : MonotoneOn f₂ (Set.Ici 0) := by
      apply monotoneOn_of_deriv_nonneg (convex_Ici 0) hf₂_cont
      · intro t _; exact (hf₂_deriv t).differentiableAt.differentiableWithinAt
      · intro t _
        rw [(hf₂_deriv t).deriv]
        linarith [(h_cos_bds t).1]
    have hf₂_0 : f₂ 0 = 0 := by simp [f₂]
    have h_lb : -y ≤ Real.sin y := by
      have h := hf₂_mono Set.left_mem_Ici hy hy
      rw [hf₂_0] at h
      dsimp [f₂] at h
      linarith
    exact abs_le.mpr ⟨h_lb, h_ub⟩
  rcases le_or_lt 0 x with hx | hx
  · rw [abs_of_nonneg hx]
    exact h_nonneg x hx
  · have hnx : 0 ≤ -x := by linarith
    have h := h_nonneg (-x) hnx
    rw [Real.sin_neg, abs_neg] at h
    rwa [abs_of_neg hx]

private theorem tau_gt_one_tc060_aux : (1 : ℝ) < RiemannScope.tau := by
  have hpos : 0 < RiemannScope.tau := RiemannScope.tau_pos
  have hdiv : ∀ x : ℝ, 2 * x / 4 = x / 2 := fun x => by ring
  have hsin : Real.sin (RiemannScope.tau / 4) = 1 := by
    unfold RiemannScope.tau
    rw [hdiv]
    simp
  have habs : |Real.sin (RiemannScope.tau / 4)| ≤ |RiemannScope.tau / 4| :=
    abs_sin_le_abs_tc060_aux (RiemannScope.tau / 4)
  rw [hsin, abs_one, abs_of_pos (by linarith)] at habs
  linarith

private theorem liouvilleLambda_mul_tc060_aux {a b : ℕ} (ha : a ≠ 0) (hb : b ≠ 0) :
    liouvilleLambda (a * b) = liouvilleLambda a * liouvilleLambda b := by
  have hab : a * b ≠ 0 := mul_ne_zero ha hb
  simp [liouvilleLambda, ha, hb, hab, natOmega, ArithmeticFunction.cardFactors_mul ha hb,
    liouvilleSignFromOmega, pow_add]

private theorem gaussianTermPhi_mul_scale_tc060_aux {g : ℕ} (hg : 0 < g) (r : ℕ) {X : ℝ}
    (hX : 0 ≤ X) :
    gaussianTermPhi (g * r) X =
      (1 / Real.sqrt (g : ℝ)) * gaussianTermPhi r (X / (g : ℝ)) := by
  obtain ⟨_, _, h_dil, _, _⟩ := window_integrability_and_kernel_scaling_tc059 zero_lt_one
  exact h_dil hg r hX

private theorem sum_divisors_selbergWeight2_tc060_aux {n : ℕ} (hn : 0 < n) :
    (∑ d ∈ n.divisors, selbergLiouvilleWeight2 d * (liouvilleLambda (n / d) : ℝ)) =
      (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2 := by
  have hn_ne : n ≠ 0 := ne_of_gt hn
  obtain ⟨_, _, _, _, ⟨h_lv_mul, _, _, _⟩⟩ :=
    liouville_square_divisor_indicator_and_compensated_selberg_tc058 0 0
  have h_w2_factor :
      ∀ d : ℕ, 0 < d →
        selbergLiouvilleWeight2 d =
          (liouvilleLambda d : ℝ) *
            (ArithmeticFunction.vonMangoldt d * Real.log (d : ℝ) +
              (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) d) := by
    intro d _
    rw [selbergLiouvilleWeight2, h_lv_mul d]
    have h_conv :
        (liouvilleVonMangoldt * liouvilleVonMangoldt) d =
          (liouvilleLambda d : ℝ) *
            (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) d := by
      rw [ArithmeticFunction.mul_apply, ArithmeticFunction.mul_apply, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro x hx
      rw [Nat.mem_divisorsAntidiagonal] at hx
      rcases hx with ⟨h_prod, hd_ne⟩
      have hx1_ne : x.1 ≠ 0 := fun h0 => hd_ne (by rw [← h_prod, h0, zero_mul])
      have hx2_ne : x.2 ≠ 0 := fun h0 => hd_ne (by rw [← h_prod, h0, mul_zero])
      rw [h_lv_mul x.1, h_lv_mul x.2]
      have h_lam_prod :
          (liouvilleLambda d : ℝ) = (liouvilleLambda x.1 : ℝ) * (liouvilleLambda x.2 : ℝ) := by
        rw [← h_prod, liouvilleLambda_mul_tc060_aux hx1_ne hx2_ne]
        push_cast; rfl
      rw [h_lam_prod]
      ring
    rw [h_conv]
    ring
  have h_each :
      ∀ d ∈ n.divisors,
        selbergLiouvilleWeight2 d * (liouvilleLambda (n / d) : ℝ) =
          (liouvilleLambda n : ℝ) *
            (ArithmeticFunction.vonMangoldt d * Real.log (d : ℝ) +
              (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) d) := by
    intro d hd
    rw [Nat.mem_divisors] at hd
    have hd_pos : 0 < d := Nat.pos_of_dvd_of_pos hd.1 hn
    have hd_ne : d ≠ 0 := ne_of_gt hd_pos
    have hq_pos : 0 < n / d := Nat.div_pos (Nat.le_of_dvd hn hd.1) hd_pos
    have hq_ne : n / d ≠ 0 := ne_of_gt hq_pos
    have h_prod : d * (n / d) = n := Nat.mul_div_cancel' hd.1
    have h_lam_n :
        (liouvilleLambda n : ℝ) = (liouvilleLambda d : ℝ) * (liouvilleLambda (n / d) : ℝ) := by
      conv_lhs => rw [← h_prod]
      rw [liouvilleLambda_mul_tc060_aux hd_ne hq_ne]
      push_cast; rfl
    rw [h_w2_factor d hd_pos, h_lam_n]
    ring
  rw [Finset.sum_congr rfl h_each, ← Finset.mul_sum]
  congr 1
  rw [Finset.sum_add_distrib]
  have h_conv_sum :
      (∑ d ∈ n.divisors, (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) d) =
        (Real.log (n : ℝ)) ^ 2 -
          ∑ d ∈ n.divisors, ArithmeticFunction.vonMangoldt d * Real.log (d : ℝ) := by
    have h_assoc :
        (∑ d ∈ n.divisors, (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) d) =
          (ArithmeticFunction.vonMangoldt * ArithmeticFunction.log) n := by
      rw [← ArithmeticFunction.coe_mul_zeta_apply, mul_assoc,
        ArithmeticFunction.vonMangoldt_mul_zeta]
    rw [h_assoc, ArithmeticFunction.mul_apply,
      Nat.sum_divisorsAntidiagonal
        (fun i j => ArithmeticFunction.vonMangoldt i * ArithmeticFunction.log j)]
    have h_log_div :
        (∑ d ∈ n.divisors, ArithmeticFunction.vonMangoldt d * ArithmeticFunction.log (n / d)) =
          ∑ d ∈ n.divisors,
            (ArithmeticFunction.vonMangoldt d * Real.log (n : ℝ) -
              ArithmeticFunction.vonMangoldt d * Real.log (d : ℝ)) := by
      apply Finset.sum_congr rfl
      intro d hd
      rw [Nat.mem_divisors] at hd
      have hd_pos : 0 < d := Nat.pos_of_dvd_of_pos hd.1 hn
      have hd_real_ne : (d : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (ne_of_gt hd_pos)
      have hn_real_ne : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn_ne
      rw [ArithmeticFunction.log_apply, Nat.cast_div hd.1 hd_real_ne,
        Real.log_div hn_real_ne hd_real_ne]
      ring
    rw [h_log_div, Finset.sum_sub_distrib, ← Finset.sum_mul, ArithmeticFunction.vonMangoldt_sum]
    ring
  rw [h_conv_sum]
  ring

private theorem sum_divisors_lambda_div_eq_isSquare_tc060_aux {n : ℕ} (hn : 0 < n) :
    (∑ d ∈ n.divisors, (liouvilleLambda (n / d) : ℝ)) = if IsSquare n then 1 else 0 := by
  obtain ⟨h_sq_ind, _, _, _, _⟩ :=
    liouville_square_divisor_indicator_and_compensated_selberg_tc058 0 0
  have h_bij :
      (∑ d ∈ n.divisors, (liouvilleLambda (n / d) : ℝ)) =
        ∑ q ∈ n.divisors, (liouvilleLambda q : ℝ) := by
    apply Finset.sum_bij (fun d _ => n / d)
    · intro d hd
      rw [Nat.mem_divisors] at hd ⊢
      exact ⟨Nat.div_dvd_of_dvd hd.1, hd.2⟩
    · intro d1 hd1 d2 hd2 h_eq
      rw [Nat.mem_divisors] at hd1 hd2
      have h1 : d1 * (n / d1) = n := Nat.mul_div_cancel' hd1.1
      have h2 : d2 * (n / d2) = n := Nat.mul_div_cancel' hd2.1
      have hq_pos : 0 < n / d1 :=
        Nat.div_pos (Nat.le_of_dvd hn hd1.1) (Nat.pos_of_dvd_of_pos hd1.1 hn)
      rw [← h_eq] at h2
      exact Nat.eq_of_mul_eq_mul_right hq_pos (h1.trans h2.symm)
    · intro q hq
      rw [Nat.mem_divisors] at hq
      have hq_pos : 0 < q := Nat.pos_of_dvd_of_pos hq.1 hn
      let d := n / q
      have hd_pos : 0 < d := Nat.div_pos (Nat.le_of_dvd hn hq.1) hq_pos
      have hqd : q * d = n := Nat.mul_div_cancel' hq.1
      refine ⟨d, Nat.mem_divisors.mpr ⟨Nat.div_dvd_of_dvd hq.1, hq.2⟩, ?_⟩
      change n / d = q
      rw [← hqd]
      exact Nat.mul_div_left q hd_pos
    · intros; rfl
  rw [h_bij]
  have h_int := h_sq_ind n hn
  have h_cast :
      (∑ q ∈ n.divisors, (liouvilleLambda q : ℝ)) =
        ((∑ q ∈ n.divisors, liouvilleLambda q : ℤ) : ℝ) := by
    push_cast; rfl
  rw [h_cast, h_int]
  split_ifs <;> norm_num

private theorem selbergCenteredRemainderInt_props_tc060_aux (c_lam : ℝ) :
    selbergCenteredRemainderInt c_lam 0 = 0 ∧
      selbergCenteredRemainderInt c_lam 1 = -c_lam ∧
      ∀ d : ℕ, 1 ≤ d →
        selbergCenteredRemainderInt c_lam d - selbergCenteredRemainderInt c_lam (d - 1) =
          selbergLiouvilleWeight2 d - c_lam := by
  obtain ⟨_, _, _, _, ⟨_, hw2_1, _, _⟩⟩ :=
    liouville_square_divisor_indicator_and_compensated_selberg_tc058 0 c_lam
  have h0 : selbergCenteredRemainderInt c_lam 0 = 0 := by
    simp [selbergCenteredRemainderInt, selbergCumulativeW2]
  have h1 : selbergCenteredRemainderInt c_lam 1 = -c_lam := by
    simp [selbergCenteredRemainderInt, selbergCumulativeW2]
  refine ⟨h0, h1, ?_⟩
  intro d hd
  by_cases hd1 : d = 1
  · subst hd1
    simp [h0, h1, hw2_1]
  · have hd2 : 2 ≤ d := by omega
    have h_ins : Finset.Icc 2 d = insert d (Finset.Icc 2 (d - 1)) := by
      ext x; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
    have h_not : d ∉ Finset.Icc 2 (d - 1) := by simp; omega
    have hW2_diff :
        selbergCumulativeW2 d - selbergCumulativeW2 (d - 1) = selbergLiouvilleWeight2 d := by
      dsimp [selbergCumulativeW2]
      rw [h_ins, Finset.sum_insert h_not]
      ring
    have hcast : ((d - 1 : ℕ) : ℝ) = (d : ℝ) - 1 := by
      rw [Nat.cast_sub hd, Nat.cast_one]
    dsimp [selbergCenteredRemainderInt]
    rw [hcast]
    linarith [hW2_diff]

private theorem scaledLiouvilleFiberG_self_tc060_aux {T : ℕ} (hT : 1 ≤ T) {X : ℝ} (hX : 0 ≤ X) :
    scaledLiouvilleFiberG T T X = gaussianTermPhi T X := by
  have hT_pos : 0 < T := by omega
  have hdiv : T / T = 1 := Nat.div_self hT_pos
  have hIcc1 : Finset.Icc 1 1 = {1} := by decide
  have hlam1 : (liouvilleLambda 1 : ℝ) = 1 := by
    simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
  have hQ1 : finiteQLambda 1 (X / (T : ℝ)) = gaussianTermPhi 1 (X / (T : ℝ)) := by
    dsimp [finiteQLambda, gaussianTermPhi]
    rw [hIcc1, Finset.sum_singleton, hlam1]
    ring
  unfold scaledLiouvilleFiberG
  rw [hdiv, hQ1]
  have hsc := gaussianTermPhi_mul_scale_tc060_aux hT_pos 1 hX
  rw [mul_one] at hsc
  exact hsc.symm

/-- **Theorem 1 (`TASK-TC-060` §1, Noncircular Candidate Reassembly, Compensated `D_{2,T}` Identity, and Exact `φ_n` Basis Stratification)**:
    1. *Endpoint and increment laws for `R_2^{int}(d; c_lam)`*:
       `R_2^{int}(0) = 0`, `R_2^{int}(1) = -c_lam`, and `R_2^{int}(d) - R_2^{int}(d - 1) = w_{2,λ}(d) - c_lam` for all `d ≥ 1`;
    2. *Safe `T = 0, 1` boundary evaluations and `g_T(X; T) = φ_T(X)`*:
       `R^{sm}_{2,0} = R^{jump}_{2,0} = endpointRemainderTerm 0 = 0`,
       `R^{sm}_{2,1} = R^{jump}_{2,1} = 0`, `endpointRemainderTerm c_lam 1 X = -c_lam * φ_1(X)`,
       and `scaledLiouvilleFiberG T T X = gaussianTermPhi T X` for `T ≥ 1, X ≥ 0`;
    3. *Exact candidate reassembly (`T ≥ 1, X ≥ 0`)*:
       `smoothRemainderSumRsm c_lam T X + jumpRemainderSumRjump c_lam T X + R_2^{int}(T) * φ_T(X) = (∑_{1 ≤ n ≤ T} λ(n) (log n)^2 φ_n(X)) - c_lam * Q_{square,T}(X)`;
    4. *Exact relation to `compensatedSelbergResidualD2` (`T ≥ 1, X > 0, log X ≠ 0`)*:
       `D_{2,T}(X; c_lam) = (c_lam Q_{square,T}(X) + R^{sm}_{2,T} + R^{jump}_{2,T} + R_2^{int}(T) φ_T(X) - Q_T^{[2]}(X)) / (log X)^2`
       and `P_T(X) - R_T(X) = D_{2,T}(X; c_lam)`;
    5. *Exact `φ_n` basis stratification on `1 ≤ n ≤ 2 * T` (`T ≥ 2`)*:
       - `smoothRemainderSumRsm c_lam T X = ∑_{1 ≤ n ≤ 2 * T} smoothBasisCoeffAlpha c_lam T n * φ_n(X)` (`X ≥ 0`);
       - For `1 ≤ n ≤ T - 1`: `smoothBasisCoeffAlpha c_lam T n = λ(n) (log n)^2 - c_lam * 1_{IsSquare n}`;
       - At `n = T`: `smoothBasisCoeffAlpha c_lam T T = λ(T) (log T)^2 - c_lam * 1_{IsSquare T} - R_2^{int}(T; c_lam)`;
       - At `n = 2 * T`: `smoothBasisCoeffAlpha c_lam T (2 * T) = c_lam * λ(T)`. -/
theorem noncircular_reassembly_and_basis_stratification_tc060 (c_lam : ℝ) :
    (selbergCenteredRemainderInt c_lam 0 = 0 ∧
      selbergCenteredRemainderInt c_lam 1 = -c_lam ∧
      ∀ d : ℕ, 1 ≤ d →
        selbergCenteredRemainderInt c_lam d - selbergCenteredRemainderInt c_lam (d - 1) =
          selbergLiouvilleWeight2 d - c_lam) ∧
    ((∀ X : ℝ,
        smoothRemainderSumRsm c_lam 0 X = 0 ∧
          jumpRemainderSumRjump c_lam 0 X = 0 ∧
          endpointRemainderTerm c_lam 0 X = 0) ∧
      (∀ X : ℝ, 0 ≤ X →
        smoothRemainderSumRsm c_lam 1 X = 0 ∧
          jumpRemainderSumRjump c_lam 1 X = 0 ∧
          endpointRemainderTerm c_lam 1 X = -c_lam * gaussianTermPhi 1 X) ∧
      (∀ T : ℕ, 1 ≤ T → ∀ X : ℝ, 0 ≤ X →
        scaledLiouvilleFiberG T T X = gaussianTermPhi T X)) ∧
    (∀ T : ℕ, 1 ≤ T → ∀ X : ℝ, 0 ≤ X →
      smoothRemainderSumRsm c_lam T X + jumpRemainderSumRjump c_lam T X +
          selbergCenteredRemainderInt c_lam T * gaussianTermPhi T X =
        (∑ n ∈ Finset.Icc 1 T,
            (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2 * gaussianTermPhi n X) -
          c_lam * finiteQSquare T X) ∧
    (∀ T : ℕ, 1 ≤ T → ∀ X : ℝ, 0 < X → Real.log X ≠ 0 →
      compensatedSelbergResidualD2 c_lam T X =
          (c_lam * finiteQSquare T X + smoothRemainderSumRsm c_lam T X +
            jumpRemainderSumRjump c_lam T X +
            selbergCenteredRemainderInt c_lam T * gaussianTermPhi T X -
            finiteQShifted (fun n => (liouvilleLambda n : ℝ)) 2 T X) / (Real.log X) ^ 2 ∧
        normalizedPrimePowerTermP T X - normalizedFirstShiftTermR T X =
          compensatedSelbergResidualD2 c_lam T X) ∧
    (∀ T : ℕ, 2 ≤ T →
      (∀ X : ℝ, 0 ≤ X →
        smoothRemainderSumRsm c_lam T X =
          ∑ n ∈ Finset.Icc 1 (2 * T), smoothBasisCoeffAlpha c_lam T n * gaussianTermPhi n X) ∧
      (∀ n ∈ Finset.Icc 1 (T - 1),
        smoothBasisCoeffAlpha c_lam T n =
          (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2 -
            c_lam * (if IsSquare n then 1 else 0)) ∧
      smoothBasisCoeffAlpha c_lam T T =
        (liouvilleLambda T : ℝ) * (Real.log (T : ℝ)) ^ 2 -
          c_lam * (if IsSquare T then 1 else 0) - selbergCenteredRemainderInt c_lam T ∧
      smoothBasisCoeffAlpha c_lam T (2 * T) = c_lam * (liouvilleLambda T : ℝ)) := by
  have hR_props := selbergCenteredRemainderInt_props_tc060_aux c_lam
  have h_reassemble :
      ∀ T : ℕ, 1 ≤ T → ∀ X : ℝ, 0 ≤ X →
        smoothRemainderSumRsm c_lam T X + jumpRemainderSumRjump c_lam T X +
            selbergCenteredRemainderInt c_lam T * gaussianTermPhi T X =
          (∑ n ∈ Finset.Icc 1 T,
              (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2 * gaussianTermPhi n X) -
            c_lam * finiteQSquare T X := by
    intro T hT X hX
    obtain ⟨_, _, ⟨h_post_abel, _⟩, _⟩ :=
      compensated_selberg_summation_by_parts_and_shift_elimination_tc058 T c_lam
    have h_ab := h_post_abel hT X hX
    rw [scaledLiouvilleFiberG_self_tc060_aux hT hX] at h_ab
    have h_split_sum :
        (∑ d ∈ Finset.Icc 1 (T - 1),
            selbergCenteredRemainderInt c_lam d *
              (scaledFiberSmoothStep T d X + scaledFiberCutoffJump T d X)) =
          smoothRemainderSumRsm c_lam T X + jumpRemainderSumRjump c_lam T X := by
      unfold smoothRemainderSumRsm jumpRemainderSumRjump
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro d _; ring
    rw [h_split_sum] at h_ab
    have h_selb_eq :
        (∑ d ∈ Finset.Icc 2 T, selbergLiouvilleWeight2 d * scaledLiouvilleFiberG T d X) =
          ∑ n ∈ Finset.Icc 1 T,
            (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2 * gaussianTermPhi n X := by
      rcases eq_or_lt_of_le hX with rfl | hX_pos
      · have h_phi0 : ∀ k : ℕ, gaussianTermPhi k 0 = 0 := by
          intro k
          unfold gaussianTermPhi
          rw [Real.zero_rpow (by norm_num : (5 / 2 : ℝ) ≠ 0), zero_mul]
        have h_Q0 : ∀ L : ℕ, finiteQLambda L 0 = 0 := by
          intro L
          unfold finiteQLambda
          rw [Real.zero_rpow (by norm_num : (5 / 2 : ℝ) ≠ 0), zero_mul]
        have h_lhs0 :
            (∑ d ∈ Finset.Icc 2 T, selbergLiouvilleWeight2 d * scaledLiouvilleFiberG T d 0) = 0 := by
          apply Finset.sum_eq_zero
          intro d _
          unfold scaledLiouvilleFiberG
          rw [zero_div, h_Q0, mul_zero, mul_zero]
        have h_rhs0 :
            (∑ n ∈ Finset.Icc 1 T,
              (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2 * gaussianTermPhi n 0) = 0 := by
          apply Finset.sum_eq_zero
          intro n _
          rw [h_phi0, mul_zero]
        rw [h_lhs0, h_rhs0]
      · obtain ⟨_, _, _, _, ⟨_, _, h_selb_id, _⟩⟩ :=
          liouville_square_divisor_indicator_and_compensated_selberg_tc058 T c_lam
        have h_id := h_selb_id X hX_pos
        have h_log_comb :
            (Real.log X) ^ 2 * finiteQLambda T X -
                2 * Real.log X * finiteQShifted (fun n => (liouvilleLambda n : ℝ)) 1 T X +
                finiteQShifted (fun n => (liouvilleLambda n : ℝ)) 2 T X =
              ∑ n ∈ Finset.Icc 1 T,
                (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2 * gaussianTermPhi n X := by
          dsimp [finiteQLambda, finiteQShifted, gaussianTermPhi]
          rw [Finset.mul_sum, Finset.mul_sum, Finset.mul_sum,
            ← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
          apply Finset.sum_congr rfl
          intro n hn
          rw [Finset.mem_Icc] at hn
          have hn_pos : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr (by omega)
          rw [Real.log_div (ne_of_gt hX_pos) (ne_of_gt hn_pos)]
          ring
        linarith
    linarith
  refine ⟨hR_props, ⟨?_, ?_, fun T hT X hX => scaledLiouvilleFiberG_self_tc060_aux hT hX⟩,
    h_reassemble, ?_, ?_⟩
  · intro X
    simp [smoothRemainderSumRsm, jumpRemainderSumRjump, endpointRemainderTerm]
  · intro X _
    refine ⟨by simp [smoothRemainderSumRsm], by simp [jumpRemainderSumRjump], ?_⟩
    simp [endpointRemainderTerm, hR_props.2.1]
  · intro T hT X hX hlog_ne
    obtain ⟨_, _, _, _, ⟨_, _, _, h_comp_sum⟩⟩ :=
      liouville_square_divisor_indicator_and_compensated_selberg_tc058 T c_lam
    obtain ⟨_, _, ⟨h_post_abel, _⟩, h_shift_elim⟩ :=
      compensated_selberg_summation_by_parts_and_shift_elimination_tc058 T c_lam
    have h_ab := h_post_abel hT X (le_of_lt hX)
    rw [scaledLiouvilleFiberG_self_tc060_aux hT (le_of_lt hX)] at h_ab
    have h_split_sum :
        (∑ d ∈ Finset.Icc 1 (T - 1),
            selbergCenteredRemainderInt c_lam d *
              (scaledFiberSmoothStep T d X + scaledFiberCutoffJump T d X)) =
          smoothRemainderSumRsm c_lam T X + jumpRemainderSumRjump c_lam T X := by
      unfold smoothRemainderSumRsm jumpRemainderSumRjump
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro d _; ring
    rw [h_split_sum] at h_ab
    have hc := h_comp_sum X (le_of_lt hX)
    have h_num_eq :
        c_lam * finiteQSquare T X +
            (∑ d ∈ Finset.Icc 1 T,
              (selbergLiouvilleWeight2 d - c_lam) * scaledLiouvilleFiberG T d X) =
          c_lam * finiteQSquare T X + smoothRemainderSumRsm c_lam T X +
            jumpRemainderSumRjump c_lam T X +
            selbergCenteredRemainderInt c_lam T * gaussianTermPhi T X := by
      linarith
    refine ⟨?_, (h_shift_elim X hX hlog_ne).2.1⟩
    unfold compensatedSelbergResidualD2
    rw [h_num_eq]
  · intro T hT2
    refine ⟨?_, ?_, ?_, ?_⟩
    · intro X hX
      unfold smoothRemainderSumRsm scaledFiberSmoothStep smoothBasisCoeffAlpha
      have h_sub_sum :
          (∑ d ∈ Finset.Icc 1 (T - 1),
              selbergCenteredRemainderInt c_lam d *
                ((1 / Real.sqrt (d : ℝ)) * finiteQLambda (T / d) (X / (d : ℝ)) -
                  (1 / Real.sqrt ((d + 1 : ℕ) : ℝ)) *
                    finiteQLambda (T / d) (X / ((d + 1 : ℕ) : ℝ)))) =
            (∑ d ∈ Finset.Icc 1 (T - 1),
                selbergCenteredRemainderInt c_lam d *
                  ((1 / Real.sqrt (d : ℝ)) * finiteQLambda (T / d) (X / (d : ℝ)))) -
              (∑ d ∈ Finset.Icc 1 (T - 1),
                selbergCenteredRemainderInt c_lam d *
                  ((1 / Real.sqrt ((d + 1 : ℕ) : ℝ)) *
                    finiteQLambda (T / d) (X / ((d + 1 : ℕ) : ℝ)))) := by
        rw [← Finset.sum_sub_distrib]
        apply Finset.sum_congr rfl
        intro d _; ring
      have h_rhs_sub :
          (∑ n ∈ Finset.Icc 1 (2 * T),
              ((∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ n ∧ n / d ≤ T / d),
                  selbergCenteredRemainderInt c_lam d * (liouvilleLambda (n / d) : ℝ)) -
                (∑ d ∈ (Finset.Icc 1 (T - 1)).filter
                    (fun d => (d + 1) ∣ n ∧ n / (d + 1) ≤ T / d),
                  selbergCenteredRemainderInt c_lam d * (liouvilleLambda (n / (d + 1)) : ℝ))) *
                gaussianTermPhi n X) =
            (∑ n ∈ Finset.Icc 1 (2 * T),
                (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ n ∧ n / d ≤ T / d),
                  selbergCenteredRemainderInt c_lam d * (liouvilleLambda (n / d) : ℝ)) *
                  gaussianTermPhi n X) -
              (∑ n ∈ Finset.Icc 1 (2 * T),
                (∑ d ∈ (Finset.Icc 1 (T - 1)).filter
                    (fun d => (d + 1) ∣ n ∧ n / (d + 1) ≤ T / d),
                  selbergCenteredRemainderInt c_lam d * (liouvilleLambda (n / (d + 1)) : ℝ)) *
                  gaussianTermPhi n X) := by
        rw [← Finset.sum_sub_distrib]
        apply Finset.sum_congr rfl
        intro n _; ring
      rw [h_sub_sum, h_rhs_sub]
      congr 1
      · have h1 :
            (∑ d ∈ Finset.Icc 1 (T - 1),
                selbergCenteredRemainderInt c_lam d *
                  ((1 / Real.sqrt (d : ℝ)) * finiteQLambda (T / d) (X / (d : ℝ)))) =
              ∑ dq ∈ (Finset.Icc 1 (T - 1)).sigma (fun d => Finset.Icc 1 (T / d)),
                selbergCenteredRemainderInt c_lam dq.1 * (liouvilleLambda dq.2 : ℝ) *
                  gaussianTermPhi (dq.1 * dq.2) X := by
          rw [Finset.sum_sigma]
          apply Finset.sum_congr rfl
          intro d hd
          rw [Finset.mem_Icc] at hd
          have hd_pos : 0 < d := by omega
          have hQ_eq :
              finiteQLambda (T / d) (X / (d : ℝ)) =
                ∑ q ∈ Finset.Icc 1 (T / d),
                  (liouvilleLambda q : ℝ) * gaussianTermPhi q (X / (d : ℝ)) := by
            dsimp [finiteQLambda, gaussianTermPhi]
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro q _; ring
          rw [hQ_eq, Finset.mul_sum, Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro q _
          rw [gaussianTermPhi_mul_scale_tc060_aux hd_pos q hX]
          ring
        have h2 :
            (∑ n ∈ Finset.Icc 1 (2 * T),
                (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ n ∧ n / d ≤ T / d),
                  selbergCenteredRemainderInt c_lam d * (liouvilleLambda (n / d) : ℝ)) *
                  gaussianTermPhi n X) =
              ∑ nd ∈ (Finset.Icc 1 (2 * T)).sigma
                  (fun n => (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ n ∧ n / d ≤ T / d)),
                selbergCenteredRemainderInt c_lam nd.2 * (liouvilleLambda (nd.1 / nd.2) : ℝ) *
                  gaussianTermPhi nd.1 X := by
          rw [Finset.sum_sigma]
          apply Finset.sum_congr rfl
          intro n _; rw [Finset.sum_mul]
        rw [h1, h2]
        apply Finset.sum_bij (fun dq _ => ⟨dq.1 * dq.2, dq.1⟩)
        · rintro ⟨d, q⟩ hdq
          simp only [Finset.mem_sigma, Finset.mem_Icc, Finset.mem_filter] at hdq ⊢
          rcases hdq with ⟨⟨hd1, hdT1⟩, ⟨hq1, hq_div⟩⟩
          have hd_pos : 0 < d := by omega
          have hdq_le : d * q ≤ T := by
            rw [mul_comm]
            exact (Nat.le_div_iff_mul_le hd_pos).mp hq_div
          exact ⟨⟨Nat.mul_pos hd_pos (by omega), by omega⟩,
            ⟨⟨hd1, hdT1⟩, ⟨⟨q, rfl⟩, by rwa [Nat.mul_div_right q hd_pos]⟩⟩⟩
        · rintro ⟨d1, q1⟩ h1 ⟨d2, q2⟩ _ h_eq
          simp only [Sigma.mk.inj_iff] at h_eq
          rcases h_eq with ⟨h_mul, hd_eq⟩
          have hd_eq' : d1 = d2 := eq_of_heq hd_eq
          subst hd_eq'
          simp only [Finset.mem_sigma, Finset.mem_Icc] at h1
          have hq_eq : q1 = q2 := Nat.eq_of_mul_eq_mul_left (by omega) h_mul
          subst hq_eq; rfl
        · rintro ⟨n, d⟩ hnd
          simp only [Finset.mem_sigma, Finset.mem_Icc, Finset.mem_filter] at hnd
          rcases hnd with ⟨⟨hn1, _⟩, ⟨⟨hd1, hdT1⟩, ⟨hd_dvd, hnd_le⟩⟩⟩
          have hd_pos : 0 < d := by omega
          let q := n / d
          have hdq : d * q = n := Nat.mul_div_cancel' hd_dvd
          have hq_pos : 0 < q := Nat.div_pos (Nat.le_of_dvd (by omega) hd_dvd) hd_pos
          refine ⟨⟨d, q⟩, Finset.mem_sigma.mpr ⟨Finset.mem_Icc.mpr ⟨hd1, hdT1⟩,
            Finset.mem_Icc.mpr ⟨hq_pos, hnd_le⟩⟩, ?_⟩
          exact Sigma.ext hdq (heq_of_eq rfl)
        · rintro ⟨d, q⟩ hdq
          dsimp only at hdq ⊢
          simp only [Finset.mem_sigma, Finset.mem_Icc] at hdq
          rw [Nat.mul_div_right q (by omega)]
      · have h1 :
            (∑ d ∈ Finset.Icc 1 (T - 1),
                selbergCenteredRemainderInt c_lam d *
                  ((1 / Real.sqrt ((d + 1 : ℕ) : ℝ)) *
                    finiteQLambda (T / d) (X / ((d + 1 : ℕ) : ℝ)))) =
              ∑ dq ∈ (Finset.Icc 1 (T - 1)).sigma (fun d => Finset.Icc 1 (T / d)),
                selbergCenteredRemainderInt c_lam dq.1 * (liouvilleLambda dq.2 : ℝ) *
                  gaussianTermPhi ((dq.1 + 1) * dq.2) X := by
          rw [Finset.sum_sigma]
          apply Finset.sum_congr rfl
          intro d _
          have hd1_pos : 0 < d + 1 := by omega
          have hQ_eq :
              finiteQLambda (T / d) (X / ((d + 1 : ℕ) : ℝ)) =
                ∑ q ∈ Finset.Icc 1 (T / d),
                  (liouvilleLambda q : ℝ) * gaussianTermPhi q (X / ((d + 1 : ℕ) : ℝ)) := by
            dsimp [finiteQLambda, gaussianTermPhi]
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro q _; ring
          rw [hQ_eq, Finset.mul_sum, Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro q _
          rw [gaussianTermPhi_mul_scale_tc060_aux hd1_pos q hX]
          ring
        have h2 :
            (∑ n ∈ Finset.Icc 1 (2 * T),
                (∑ d ∈ (Finset.Icc 1 (T - 1)).filter
                    (fun d => (d + 1) ∣ n ∧ n / (d + 1) ≤ T / d),
                  selbergCenteredRemainderInt c_lam d * (liouvilleLambda (n / (d + 1)) : ℝ)) *
                  gaussianTermPhi n X) =
              ∑ nd ∈ (Finset.Icc 1 (2 * T)).sigma
                  (fun n => (Finset.Icc 1 (T - 1)).filter
                    (fun d => (d + 1) ∣ n ∧ n / (d + 1) ≤ T / d)),
                selbergCenteredRemainderInt c_lam nd.2 *
                  (liouvilleLambda (nd.1 / (nd.2 + 1)) : ℝ) * gaussianTermPhi nd.1 X := by
          rw [Finset.sum_sigma]
          apply Finset.sum_congr rfl
          intro n _; rw [Finset.sum_mul]
        rw [h1, h2]
        apply Finset.sum_bij (fun dq _ => ⟨(dq.1 + 1) * dq.2, dq.1⟩)
        · rintro ⟨d, q⟩ hdq
          simp only [Finset.mem_sigma, Finset.mem_Icc, Finset.mem_filter] at hdq ⊢
          rcases hdq with ⟨⟨hd1, hdT1⟩, ⟨hq1, hq_div⟩⟩
          have hd_pos : 0 < d := by omega
          have hd1_pos : 0 < d + 1 := by omega
          have hdq_le : d * q ≤ T := by
            rw [mul_comm]
            exact (Nat.le_div_iff_mul_le hd_pos).mp hq_div
          have hq_le_dq : q ≤ d * q := Nat.le_mul_of_pos_left q hd_pos
          have h_d1q_le : (d + 1) * q ≤ 2 * T := by
            have h_exp : (d + 1) * q = d * q + q := Nat.succ_mul d q
            omega
          exact ⟨⟨Nat.mul_pos hd1_pos (by omega), h_d1q_le⟩,
            ⟨⟨hd1, hdT1⟩, ⟨⟨q, rfl⟩, by rwa [Nat.mul_div_right q hd1_pos]⟩⟩⟩
        · rintro ⟨d1, q1⟩ _ ⟨d2, q2⟩ _ h_eq
          simp only [Sigma.mk.inj_iff] at h_eq
          rcases h_eq with ⟨h_mul, hd_eq⟩
          have hd_eq' : d1 = d2 := eq_of_heq hd_eq
          subst hd_eq'
          have hq_eq : q1 = q2 := Nat.eq_of_mul_eq_mul_left (by omega) h_mul
          subst hq_eq; rfl
        · rintro ⟨n, d⟩ hnd
          simp only [Finset.mem_sigma, Finset.mem_Icc, Finset.mem_filter] at hnd
          rcases hnd with ⟨⟨hn1, _⟩, ⟨⟨hd1, hdT1⟩, ⟨hd_dvd, hnd_le⟩⟩⟩
          have hd1_pos : 0 < d + 1 := by omega
          let q := n / (d + 1)
          have hdq : (d + 1) * q = n := Nat.mul_div_cancel' hd_dvd
          have hq_pos : 0 < q := Nat.div_pos (Nat.le_of_dvd (by omega) hd_dvd) hd1_pos
          refine ⟨⟨d, q⟩, Finset.mem_sigma.mpr ⟨Finset.mem_Icc.mpr ⟨hd1, hdT1⟩,
            Finset.mem_Icc.mpr ⟨hq_pos, hnd_le⟩⟩, ?_⟩
          exact Sigma.ext hdq (heq_of_eq rfl)
        · rintro ⟨d, q⟩ _
          rw [Nat.mul_div_right q (by omega)]
    · intro n hn
      rw [Finset.mem_Icc] at hn
      rcases hn with ⟨hn1, hnT1⟩
      have hn_pos : 0 < n := by omega
      have h_filt1 :
          (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ n ∧ n / d ≤ T / d) = n.divisors := by
        ext d
        simp only [Finset.mem_filter, Finset.mem_Icc, Nat.mem_divisors]
        constructor
        · rintro ⟨_, hd_dvd, _⟩
          exact ⟨hd_dvd, by omega⟩
        · rintro ⟨hd_dvd, _⟩
          have hd_pos : 0 < d := Nat.pos_of_dvd_of_pos hd_dvd hn_pos
          have hd_le_n : d ≤ n := Nat.le_of_dvd hn_pos hd_dvd
          have h_div_le : n / d ≤ T / d := by
            apply (Nat.le_div_iff_mul_le hd_pos).mpr
            rw [mul_comm, Nat.mul_div_cancel' hd_dvd]
            omega
          exact ⟨⟨hd_pos, by omega⟩, hd_dvd, h_div_le⟩
      have h_sum2 :
          (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ n ∧ n / (d + 1) ≤ T / d),
              selbergCenteredRemainderInt c_lam d * (liouvilleLambda (n / (d + 1)) : ℝ)) =
            ∑ m ∈ n.divisors,
              selbergCenteredRemainderInt c_lam (m - 1) * (liouvilleLambda (n / m) : ℝ) := by
        have h1_mem : 1 ∈ n.divisors := Nat.mem_divisors.mpr ⟨one_dvd n, by omega⟩
        rw [← Finset.add_sum_erase _ _ h1_mem]
        have h1_zero :
            selbergCenteredRemainderInt c_lam (1 - 1) * (liouvilleLambda (n / 1) : ℝ) = 0 := by
          simp [hR_props.1]
        rw [h1_zero, zero_add]
        apply Finset.sum_bij (fun d _ => d + 1)
        · intro d hd
          simp only [Finset.mem_filter, Finset.mem_Icc, Finset.mem_erase, Nat.mem_divisors] at hd ⊢
          exact ⟨by omega, hd.2.1, by omega⟩
        · intro d1 _ d2 _ h_eq; omega
        · intro m hm
          simp only [Finset.mem_erase, Nat.mem_divisors] at hm
          rcases hm with ⟨hm_ne1, hm_dvd, _⟩
          have hm_pos : 0 < m := Nat.pos_of_dvd_of_pos hm_dvd hn_pos
          have hm_ge2 : 2 ≤ m := by omega
          have hm_le_n : m ≤ n := Nat.le_of_dvd hn_pos hm_dvd
          let d := m - 1
          have hd1_eq : d + 1 = m := by omega
          have hd_pos : 0 < d := by omega
          have h_div_le : n / (d + 1) ≤ T / d := by
            rw [hd1_eq]
            apply (Nat.le_div_iff_mul_le hd_pos).mpr
            have hle_m : (n / m) * d ≤ (n / m) * m := Nat.mul_le_mul_left (n / m) (by omega)
            have hmul_m : (n / m) * m = n := by rw [mul_comm]; exact Nat.mul_div_cancel' hm_dvd
            omega
          refine ⟨d, ?_, hd1_eq⟩
          simp only [Finset.mem_filter, Finset.mem_Icc]
          exact ⟨⟨hd_pos, by omega⟩, hd1_eq.symm ▸ hm_dvd, h_div_le⟩
        · intro d _; simp
      unfold smoothBasisCoeffAlpha
      rw [h_filt1, h_sum2, ← Finset.sum_sub_distrib]
      have h_diff_congr :
          (∑ m ∈ n.divisors,
              (selbergCenteredRemainderInt c_lam m * (liouvilleLambda (n / m) : ℝ) -
                selbergCenteredRemainderInt c_lam (m - 1) * (liouvilleLambda (n / m) : ℝ))) =
            (∑ m ∈ n.divisors, selbergLiouvilleWeight2 m * (liouvilleLambda (n / m) : ℝ)) -
              c_lam * (∑ m ∈ n.divisors, (liouvilleLambda (n / m) : ℝ)) := by
        rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
        apply Finset.sum_congr rfl
        intro m hm
        rw [Nat.mem_divisors] at hm
        have hm_ge1 : 1 ≤ m := Nat.pos_of_dvd_of_pos hm.1 hn_pos
        have h_inc := hR_props.2.2 m hm_ge1
        calc
          selbergCenteredRemainderInt c_lam m * (liouvilleLambda (n / m) : ℝ) -
              selbergCenteredRemainderInt c_lam (m - 1) * (liouvilleLambda (n / m) : ℝ)
            = (selbergCenteredRemainderInt c_lam m - selbergCenteredRemainderInt c_lam (m - 1)) *
                (liouvilleLambda (n / m) : ℝ) := by ring
          _ = (selbergLiouvilleWeight2 m - c_lam) * (liouvilleLambda (n / m) : ℝ) := by rw [h_inc]
          _ = selbergLiouvilleWeight2 m * (liouvilleLambda (n / m) : ℝ) -
                c_lam * (liouvilleLambda (n / m) : ℝ) := by ring
      rw [h_diff_congr, sum_divisors_selbergWeight2_tc060_aux hn_pos,
        sum_divisors_lambda_div_eq_isSquare_tc060_aux hn_pos]
    · have hT_pos : 0 < T := by omega
      have h_filt1_T :
          (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ T ∧ T / d ≤ T / d) =
            T.divisors.erase T := by
        ext d
        simp only [Finset.mem_filter, Finset.mem_Icc, Finset.mem_erase, Nat.mem_divisors]
        constructor
        · rintro ⟨⟨_, hdT1⟩, hd_dvd, _⟩
          exact ⟨by omega, hd_dvd, by omega⟩
        · rintro ⟨hd_ne, hd_dvd, _⟩
          have hd_pos : 0 < d := Nat.pos_of_dvd_of_pos hd_dvd hT_pos
          have hd_le_T : d ≤ T := Nat.le_of_dvd hT_pos hd_dvd
          exact ⟨⟨hd_pos, by omega⟩, hd_dvd, le_refl _⟩
      have hT_mem_div : T ∈ T.divisors := Nat.mem_divisors.mpr ⟨dvd_refl T, by omega⟩
      have hlam1 : (liouvilleLambda 1 : ℝ) = 1 := by
        simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
      have h_sum1_T :
          (∑ d ∈ T.divisors.erase T,
              selbergCenteredRemainderInt c_lam d * (liouvilleLambda (T / d) : ℝ)) =
            (∑ d ∈ T.divisors,
              selbergCenteredRemainderInt c_lam d * (liouvilleLambda (T / d) : ℝ)) -
              selbergCenteredRemainderInt c_lam T := by
        have h_add := Finset.add_sum_erase T.divisors
          (fun d => selbergCenteredRemainderInt c_lam d * (liouvilleLambda (T / d) : ℝ)) hT_mem_div
        dsimp only at h_add
        rw [Nat.div_self hT_pos, hlam1, mul_one] at h_add
        linarith
      have h_sum2_T :
          (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ T ∧ T / (d + 1) ≤ T / d),
              selbergCenteredRemainderInt c_lam d * (liouvilleLambda (T / (d + 1)) : ℝ)) =
            ∑ m ∈ T.divisors,
              selbergCenteredRemainderInt c_lam (m - 1) * (liouvilleLambda (T / m) : ℝ) := by
        have h1_mem : 1 ∈ T.divisors := Nat.mem_divisors.mpr ⟨one_dvd T, by omega⟩
        rw [← Finset.add_sum_erase _ _ h1_mem]
        rw [show (1 - 1 : ℕ) = 0 by rfl, hR_props.1, zero_mul, zero_add]
        apply Finset.sum_bij (fun d _ => d + 1)
        · intro d hd
          simp only [Finset.mem_filter, Finset.mem_Icc, Finset.mem_erase, Nat.mem_divisors] at hd ⊢
          exact ⟨by omega, hd.2.1, by omega⟩
        · intro d1 _ d2 _ h_eq; omega
        · intro m hm
          simp only [Finset.mem_erase, Nat.mem_divisors] at hm
          rcases hm with ⟨hm_ne1, hm_dvd, _⟩
          have hm_pos : 0 < m := Nat.pos_of_dvd_of_pos hm_dvd hT_pos
          have hm_le_T : m ≤ T := Nat.le_of_dvd hT_pos hm_dvd
          let d := m - 1
          have hd1_eq : d + 1 = m := by omega
          have hd_pos : 0 < d := by omega
          refine ⟨d, ?_, hd1_eq⟩
          simp only [Finset.mem_filter, Finset.mem_Icc]
          exact ⟨⟨hd_pos, by omega⟩, hd1_eq.symm ▸ hm_dvd, Nat.div_le_div_left (by omega) hd_pos⟩
        · intro d _; simp
      unfold smoothBasisCoeffAlpha
      rw [h_filt1_T, h_sum1_T, h_sum2_T]
      have h_comb :
          (∑ d ∈ T.divisors,
              selbergCenteredRemainderInt c_lam d * (liouvilleLambda (T / d) : ℝ)) -
            (∑ m ∈ T.divisors,
              selbergCenteredRemainderInt c_lam (m - 1) * (liouvilleLambda (T / m) : ℝ)) =
            (∑ m ∈ T.divisors, selbergLiouvilleWeight2 m * (liouvilleLambda (T / m) : ℝ)) -
              c_lam * (∑ m ∈ T.divisors, (liouvilleLambda (T / m) : ℝ)) := by
        rw [← Finset.sum_sub_distrib, Finset.mul_sum, ← Finset.sum_sub_distrib]
        apply Finset.sum_congr rfl
        intro m hm
        rw [Nat.mem_divisors] at hm
        have hm_ge1 : 1 ≤ m := Nat.pos_of_dvd_of_pos hm.1 hT_pos
        have h_inc := hR_props.2.2 m hm_ge1
        calc
          selbergCenteredRemainderInt c_lam m * (liouvilleLambda (T / m) : ℝ) -
              selbergCenteredRemainderInt c_lam (m - 1) * (liouvilleLambda (T / m) : ℝ)
            = (selbergCenteredRemainderInt c_lam m - selbergCenteredRemainderInt c_lam (m - 1)) *
                (liouvilleLambda (T / m) : ℝ) := by ring
          _ = (selbergLiouvilleWeight2 m - c_lam) * (liouvilleLambda (T / m) : ℝ) := by rw [h_inc]
          _ = selbergLiouvilleWeight2 m * (liouvilleLambda (T / m) : ℝ) -
                c_lam * (liouvilleLambda (T / m) : ℝ) := by ring
      rw [sum_divisors_selbergWeight2_tc060_aux hT_pos,
        sum_divisors_lambda_div_eq_isSquare_tc060_aux hT_pos] at h_comb
      linarith
    · have h_filt1_empty :
          (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ 2 * T ∧ (2 * T) / d ≤ T / d) = ∅ := by
        ext d
        simp only [Finset.mem_filter, Finset.mem_Icc, Finset.not_mem_empty, iff_false]
        rintro ⟨⟨_, _⟩, hd_dvd, h_le⟩
        have h1 : d * ((2 * T) / d) = 2 * T := Nat.mul_div_cancel' hd_dvd
        have h2 : d * ((2 * T) / d) ≤ d * (T / d) := Nat.mul_le_mul_left d h_le
        have h3 : d * (T / d) ≤ T := Nat.mul_div_le T d
        omega
      have h_filt2_one :
          (Finset.Icc 1 (T - 1)).filter
            (fun d => (d + 1) ∣ 2 * T ∧ (2 * T) / (d + 1) ≤ T / d) = {1} := by
        ext d
        simp only [Finset.mem_filter, Finset.mem_Icc, Finset.mem_singleton]
        constructor
        · rintro ⟨⟨hd1, _⟩, hd_dvd, h_le⟩
          by_contra hd_ne1
          have hd2 : 2 ≤ d := by omega
          have hd_pos : 0 < d := by omega
          let q := (2 * T) / (d + 1)
          have h_mul : (d + 1) * q = 2 * T := Nat.mul_div_cancel' hd_dvd
          have hq_pos : 0 < q := by
            by_contra hq0
            have hq_z : q = 0 := Nat.eq_zero_of_not_pos hq0
            rw [hq_z, mul_zero] at h_mul
            omega
          have hdq_le : d * q ≤ T := by
            rw [mul_comm]
            exact (Nat.le_div_iff_mul_le hd_pos).mp h_le
          have h_lt : (d + 1) * q < 2 * (d * q) := by
            have h_exp : (d + 1) * q = d * q + q := Nat.succ_mul d q
            have hq_lt : q < d * q := by
              calc
                q = 1 * q := (one_mul q).symm
                _ < 2 * q := Nat.mul_lt_mul_of_pos_right (by decide) hq_pos
                _ ≤ d * q := Nat.mul_le_mul_right q hd2
            omega
          omega
        · rintro rfl
          refine ⟨⟨le_refl 1, by omega⟩, ⟨T, rfl⟩, ?_⟩
          rw [show 1 + 1 = 2 by rfl, Nat.mul_div_right T (by decide), Nat.div_one]
      unfold smoothBasisCoeffAlpha
      rw [h_filt1_empty, h_filt2_one, Finset.sum_empty, Finset.sum_singleton]
      rw [show 1 + 1 = 2 by rfl, Nat.mul_div_right T (by decide), hR_props.2.1]
      ring

/-! ### Section 2: Adjacent Dilation Multiplier and Level-Set Cutoff Blocks (`TASK-TC-060` §2) -/

/-- Exact Mellin-Fourier adjacent dilation multiplier
    `m_d(v) := d^(-1/2 - i v) - (d + 1)^(-1/2 - i v)`. -/
noncomputable def adjacentDilationMultiplier (d : ℕ) (v : ℝ) : ℂ :=
  ((1 / Real.sqrt (d : ℝ) : ℝ) : ℂ) *
      Complex.exp (-(Complex.I * (v : ℂ) * (Real.log (d : ℝ) : ℂ))) -
    ((1 / Real.sqrt ((d + 1 : ℕ) : ℝ) : ℝ) : ℂ) *
      Complex.exp (-(Complex.I * (v : ℂ) * (Real.log ((d + 1 : ℕ) : ℝ) : ℂ)))

/-- Odd-harmonic resonant frequency `v_{d,k} := (2 k + 1) * τ / (2 * log((d + 1) / d))`
    written strictly in terms of `RiemannScope.tau`. -/
noncomputable def resonantMultiplierFreq (d : ℕ) (k : ℤ) : ℝ :=
  ((2 * k + 1 : ℤ) : ℝ) * RiemannScope.tau /
    (2 * Real.log (((d + 1 : ℕ) : ℝ) / (d : ℝ)))

/-- Inner-cutoff level block `B_{T,L} := {1 ≤ d ≤ T - 1 : ⌊T / d⌋ = L}`. -/
def cutoffLevelBlock (T L : ℕ) : Finset ℕ :=
  (Finset.Icc 1 (T - 1)).filter (fun d => T / d = L)

/-- Block-grouped signed dilation multiplier
    `M_{T,L}(v; c_lam) := ∑_{d ∈ cutoffLevelBlock T L} R_2^{int}(d; c_lam) m_d(v)`. -/
noncomputable def blockSignedMultiplier (c_lam : ℝ) (T L : ℕ) (v : ℝ) : ℂ :=
  ∑ d ∈ cutoffLevelBlock T L,
    (selbergCenteredRemainderInt c_lam d : ℂ) * adjacentDilationMultiplier d v

/-- Finite Liouville Dirichlet polynomial `D_{λ,L}(1/2 + i v) := ∑_{1 ≤ n ≤ L} λ(n) n^(-1/2 - i v)`. -/
noncomputable def finiteLiouvilleDirichletPoly (L : ℕ) (v : ℝ) : ℂ :=
  ∑ n ∈ Finset.Icc 1 L,
    (liouvilleLambda n : ℂ) * ((1 / Real.sqrt (n : ℝ) : ℝ) : ℂ) *
      Complex.exp (-(Complex.I * (v : ℂ) * (Real.log (n : ℝ) : ℂ)))

private theorem sq_le_cosh_two_sub_two_tc060_aux {u : ℝ} (hu : 0 ≤ u) :
    u ^ 2 ≤ Real.exp u + Real.exp (-u) - 2 := by
  let g : ℝ → ℝ := fun x => Real.exp x - Real.exp (-x) - 2 * x
  have hg_deriv : ∀ x : ℝ, HasDerivAt g (Real.exp x + Real.exp (-x) - 2) x := by
    intro x
    have h1 : HasDerivAt Real.exp (Real.exp x) x := Real.hasDerivAt_exp x
    have h2 : HasDerivAt (fun y : ℝ => Real.exp (-y)) (-Real.exp (-x)) x := by
      simpa using (Real.hasDerivAt_exp (-x)).comp x (hasDerivAt_id x).neg
    have h3 : HasDerivAt (fun y : ℝ => 2 * y) 2 x := by
      simpa using (hasDerivAt_id x).const_mul (2 : ℝ)
    convert (h1.sub h2).sub h3 using 1
    ring
  have hg_deriv_nn : ∀ x : ℝ, 0 ≤ Real.exp x + Real.exp (-x) - 2 := by
    intro x
    have h_sq :
        Real.exp x + Real.exp (-x) - 2 =
          (Real.exp (x / 2) - Real.exp (-(x / 2))) ^ 2 := by
      have hp : Real.exp (x / 2) * Real.exp (x / 2) = Real.exp x := by
        rw [← Real.exp_add]; ring_nf
      have hn : Real.exp (-(x / 2)) * Real.exp (-(x / 2)) = Real.exp (-x) := by
        rw [← Real.exp_add]; ring_nf
      have hm : Real.exp (x / 2) * Real.exp (-(x / 2)) = 1 := by
        rw [← Real.exp_add, add_neg_self, Real.exp_zero]
      calc
        Real.exp x + Real.exp (-x) - 2
          = Real.exp (x / 2) * Real.exp (x / 2) +
              Real.exp (-(x / 2)) * Real.exp (-(x / 2)) -
              2 * (Real.exp (x / 2) * Real.exp (-(x / 2))) := by
              rw [hp, hn, hm]; ring
        _ = (Real.exp (x / 2) - Real.exp (-(x / 2))) ^ 2 := by ring
    rw [h_sq]
    exact sq_nonneg _
  have hg_cont : Continuous g := by continuity
  have hg_mono : MonotoneOn g (Set.Ici 0) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ici 0) hg_cont.continuousOn
    · intro x _; exact (hg_deriv x).differentiableAt.differentiableWithinAt
    · intro x _
      rw [(hg_deriv x).deriv]
      exact hg_deriv_nn x
  have hg_nn : ∀ x ∈ Set.Ici (0 : ℝ), 0 ≤ g x := by
    intro x hx
    have h0 : g 0 = 0 := by simp [g]
    rw [← h0]
    exact hg_mono (Set.left_mem_Ici) hx hx
  let f : ℝ → ℝ := fun x => Real.exp x + Real.exp (-x) - 2 - x ^ 2
  have hf_deriv : ∀ x : ℝ, HasDerivAt f (g x) x := by
    intro x
    have h1 : HasDerivAt Real.exp (Real.exp x) x := Real.hasDerivAt_exp x
    have h2 : HasDerivAt (fun y : ℝ => Real.exp (-y)) (-Real.exp (-x)) x := by
      simpa using (Real.hasDerivAt_exp (-x)).comp x (hasDerivAt_id x).neg
    have h3 : HasDerivAt (fun y : ℝ => y ^ 2) (2 * x) x := by
      simpa using hasDerivAt_pow 2 x
    convert ((h1.add h2).sub (hasDerivAt_const x (2 : ℝ))).sub h3 using 1
    dsimp [g]; ring
  have hf_cont : Continuous f := by continuity
  have hf_mono : MonotoneOn f (Set.Ici 0) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ici 0) hf_cont.continuousOn
    · intro x _; exact (hf_deriv x).differentiableAt.differentiableWithinAt
    · intro x hx
      rw [(hf_deriv x).deriv]
      exact hg_nn x (interior_subset hx)
  have hf0 : f 0 = 0 := by simp [f]; norm_num
  have hfu : 0 ≤ f u := by
    rw [← hf0]
    exact hf_mono (Set.left_mem_Ici) hu hu
  dsimp [f] at hfu
  linarith

/-- **Theorem 2 (`TASK-TC-060` §2, Exact `t^(-3/2)` Benchmark, Elementary Multiplier Bound, Resonant Attainment, and Level-Set Cutoff Blocks)**:
    1. *Exact `t^(-3/2)` integral benchmark (`d ≥ 1`)*:
       `∫_{d}^{d+1} t^(-3/2) dt = 2 * (1 / √d - 1 / √(d + 1)) < d^(-3/2)`;
    2. *Elementary global multiplier benchmark (`d ≥ 1, v : ℝ`)*:
       `‖m_d(v)‖ ≤ min (1 / √d + 1 / √(d + 1)) (√(1 / 4 + v^2) * (2 * (1 / √d - 1 / √(d + 1))))`;
    3. *Sharp unrestricted-frequency attainment (`d ≥ 1, k : ℤ`)*:
       `‖m_d(resonantMultiplierFreq d k)‖ = 1 / √d + 1 / √(d + 1)`;
    4. *Exact level-set block partition, `T = 2` empty-block witness, Fourier/real-space block grouping, singleton `d * (d + 1) ≤ T` blocks, and `Nat.sqrt T - 1` nonempty-block lower bound*. -/
theorem adjacent_dilation_multiplier_and_cutoff_blocks_tc060 :
    (∀ d : ℕ, 1 ≤ d →
      (∫ t in (d : ℝ)..((d + 1 : ℕ) : ℝ), t ^ (-(3 / 2 : ℝ))) =
          2 * (1 / Real.sqrt (d : ℝ) - 1 / Real.sqrt ((d + 1 : ℕ) : ℝ)) ∧
        2 * (1 / Real.sqrt (d : ℝ) - 1 / Real.sqrt ((d + 1 : ℕ) : ℝ)) <
          (d : ℝ) ^ (-(3 / 2 : ℝ))) ∧
    (∀ d : ℕ, 1 ≤ d → ∀ v : ℝ,
      ‖adjacentDilationMultiplier d v‖ ≤
        min (1 / Real.sqrt (d : ℝ) + 1 / Real.sqrt ((d + 1 : ℕ) : ℝ))
          (Real.sqrt (1 / 4 + v ^ 2) *
            (2 * (1 / Real.sqrt (d : ℝ) - 1 / Real.sqrt ((d + 1 : ℕ) : ℝ))))) ∧
    (∀ d : ℕ, 1 ≤ d → ∀ k : ℤ,
      ‖adjacentDilationMultiplier d (resonantMultiplierFreq d k)‖ =
        1 / Real.sqrt (d : ℝ) + 1 / Real.sqrt ((d + 1 : ℕ) : ℝ)) ∧
    ((∀ T L₁ L₂ : ℕ, L₁ ≠ L₂ → Disjoint (cutoffLevelBlock T L₁) (cutoffLevelBlock T L₂)) ∧
      (∀ T : ℕ, (Finset.Icc 1 T).biUnion (cutoffLevelBlock T) = Finset.Icc 1 (T - 1)) ∧
      (cutoffLevelBlock 2 1 = ∅ ∧ cutoffLevelBlock 2 2 = {1}) ∧
      (∀ (T : ℕ) (c_lam : ℝ) (v : ℝ) (qhat : ℕ → ℝ → ℂ),
        (∑ d ∈ Finset.Icc 1 (T - 1),
            (selbergCenteredRemainderInt c_lam d : ℂ) *
              adjacentDilationMultiplier d v * qhat (T / d) v) =
          ∑ L ∈ Finset.Icc 1 T, blockSignedMultiplier c_lam T L v * qhat L v) ∧
      (∀ (T : ℕ) (c_lam : ℝ) (X : ℝ),
        smoothRemainderSumRsm c_lam T X =
          ∑ L ∈ Finset.Icc 1 T,
            ∑ d ∈ cutoffLevelBlock T L,
              selbergCenteredRemainderInt c_lam d *
                ((1 / Real.sqrt (d : ℝ)) * finiteQLambda L (X / (d : ℝ)) -
                  (1 / Real.sqrt ((d + 1 : ℕ) : ℝ)) *
                    finiteQLambda L (X / ((d + 1 : ℕ) : ℝ)))) ∧
      (∀ T d : ℕ, 1 ≤ d → d < T → d * (d + 1) ≤ T →
        cutoffLevelBlock T (T / d) = {d}) ∧
      (∀ T : ℕ,
        Nat.sqrt T - 1 ≤
          ((Finset.Icc 1 T).filter (fun L => (cutoffLevelBlock T L).Nonempty)).card)) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro d hd
    have hd_pos : (0 : ℝ) < (d : ℝ) := Nat.cast_pos.mpr hd
    have hd1_pos : (0 : ℝ) < ((d + 1 : ℕ) : ℝ) := by positivity
    have hd_le_d1 : (d : ℝ) ≤ ((d + 1 : ℕ) : ℝ) := by exact_mod_cast (Nat.le_succ d)
    have h_uIcc_pos : ∀ t ∈ Set.uIcc (d : ℝ) ((d + 1 : ℕ) : ℝ), 0 < t := by
      intro t ht
      rw [Set.uIcc_of_le hd_le_d1, Set.mem_Icc] at ht
      linarith
    let F : ℝ → ℝ := fun t => -2 * t ^ (-(1 / 2 : ℝ))
    have h_deriv :
        ∀ t ∈ Set.uIcc (d : ℝ) ((d + 1 : ℕ) : ℝ), HasDerivAt F (t ^ (-(3 / 2 : ℝ))) t := by
      intro t ht
      have ht_ne : t ≠ 0 := ne_of_gt (h_uIcc_pos t ht)
      have h1 := (Real.hasDerivAt_rpow_const (p := -(1 / 2 : ℝ)) (Or.inl ht_ne)).const_mul (-2 : ℝ)
      have h_exp : (-(1 / 2 : ℝ)) - 1 = -(3 / 2 : ℝ) := by ring
      rw [h_exp] at h1
      convert h1 using 1
      ring
    have h_cont :
        ContinuousOn (fun t : ℝ => t ^ (-(3 / 2 : ℝ))) (Set.uIcc (d : ℝ) ((d + 1 : ℕ) : ℝ)) := by
      apply ContinuousOn.rpow_const continuousOn_id
      intro t ht
      exact Or.inl (ne_of_gt (h_uIcc_pos t ht))
    have h_int_eq :=
      intervalIntegral.integral_eq_sub_of_hasDerivAt h_deriv h_cont.intervalIntegrable
    have h_rpow_sqrt : ∀ x : ℝ, 0 < x → x ^ (-(1 / 2 : ℝ)) = 1 / Real.sqrt x := by
      intro x hx
      rw [Real.rpow_neg (le_of_lt hx), ← Real.sqrt_eq_rpow, one_div]
    have hF_eval :
        F ((d + 1 : ℕ) : ℝ) - F (d : ℝ) =
          2 * (1 / Real.sqrt (d : ℝ) - 1 / Real.sqrt ((d + 1 : ℕ) : ℝ)) := by
      dsimp [F]
      rw [h_rpow_sqrt _ hd1_pos, h_rpow_sqrt _ hd_pos]
      ring
    refine ⟨h_int_eq.trans hF_eval, ?_⟩
    have hd_ge1 : (1 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd
    have hd1_eq : ((d + 1 : ℕ) : ℝ) = (d : ℝ) + 1 := by push_cast; ring
    have h_rpow_32 : (d : ℝ) ^ (-(3 / 2 : ℝ)) = 1 / ((d : ℝ) * Real.sqrt (d : ℝ)) := by
      have h32 : (d : ℝ) ^ (3 / 2 : ℝ) = (d : ℝ) * Real.sqrt (d : ℝ) := by
        have h1 : (3 / 2 : ℝ) = 1 + (1 / 2 : ℝ) := by ring
        rw [h1, Real.rpow_add hd_pos, Real.rpow_one, Real.sqrt_eq_rpow]
      rw [Real.rpow_neg (le_of_lt hd_pos), h32, one_div]
    rw [h_rpow_32, hd1_eq]
    have hsqrt_d_pos : 0 < Real.sqrt (d : ℝ) := Real.sqrt_pos.mpr hd_pos
    have hsqrt_d1_pos : 0 < Real.sqrt ((d : ℝ) + 1) := Real.sqrt_pos.mpr (by linarith)
    have h_sq_lt :
        ((2 * (d : ℝ) - 1) * Real.sqrt ((d : ℝ) + 1)) ^ 2 <
          (2 * (d : ℝ) * Real.sqrt (d : ℝ)) ^ 2 := by
      rw [mul_pow, mul_pow, Real.sq_sqrt (by linarith), Real.sq_sqrt (le_of_lt hd_pos)]
      have h_diff_eq :
          (2 * (d : ℝ)) ^ 2 * (d : ℝ) - (2 * (d : ℝ) - 1) ^ 2 * ((d : ℝ) + 1) =
            3 * (d : ℝ) - 1 := by ring
      have h_pos_3d : 0 < 3 * (d : ℝ) - 1 := by linarith
      rw [← h_diff_eq] at h_pos_3d
      exact sub_pos.mp h_pos_3d
    have h_lhs_nn : 0 ≤ (2 * (d : ℝ) - 1) * Real.sqrt ((d : ℝ) + 1) :=
      mul_nonneg (by linarith) (le_of_lt hsqrt_d1_pos)
    have h_rhs_nn : 0 ≤ 2 * (d : ℝ) * Real.sqrt (d : ℝ) := by positivity
    have h_lt :
        (2 * (d : ℝ) - 1) * Real.sqrt ((d : ℝ) + 1) < 2 * (d : ℝ) * Real.sqrt (d : ℝ) := by
      calc
        (2 * (d : ℝ) - 1) * Real.sqrt ((d : ℝ) + 1)
          = Real.sqrt (((2 * (d : ℝ) - 1) * Real.sqrt ((d : ℝ) + 1)) ^ 2) :=
            (Real.sqrt_sq h_lhs_nn).symm
        _ < Real.sqrt ((2 * (d : ℝ) * Real.sqrt (d : ℝ)) ^ 2) :=
            Real.sqrt_lt_sqrt (sq_nonneg _) h_sq_lt
        _ = 2 * (d : ℝ) * Real.sqrt (d : ℝ) :=
            Real.sqrt_sq h_rhs_nn
    have h_denom_pos :
        0 < (d : ℝ) * Real.sqrt (d : ℝ) * Real.sqrt ((d : ℝ) + 1) := by positivity
    have h_diff_pos :
        0 < 1 / ((d : ℝ) * Real.sqrt (d : ℝ)) -
          2 * (1 / Real.sqrt (d : ℝ) - 1 / Real.sqrt ((d : ℝ) + 1)) := by
      have h_alg :
          1 / ((d : ℝ) * Real.sqrt (d : ℝ)) -
              2 * (1 / Real.sqrt (d : ℝ) - 1 / Real.sqrt ((d : ℝ) + 1)) =
            (2 * (d : ℝ) * Real.sqrt (d : ℝ) -
                (2 * (d : ℝ) - 1) * Real.sqrt ((d : ℝ) + 1)) /
              ((d : ℝ) * Real.sqrt (d : ℝ) * Real.sqrt ((d : ℝ) + 1)) := by
        field_simp [ne_of_gt hd_pos, ne_of_gt hsqrt_d_pos, ne_of_gt hsqrt_d1_pos]
        ring
      rw [h_alg]
      exact div_pos (by linarith) h_denom_pos
    linarith
  · intro d hd v
    let a : ℝ := 1 / Real.sqrt (d : ℝ)
    let b : ℝ := 1 / Real.sqrt ((d + 1 : ℕ) : ℝ)
    have hd_pos : (0 : ℝ) < (d : ℝ) := Nat.cast_pos.mpr hd
    have hd1_pos : (0 : ℝ) < ((d + 1 : ℕ) : ℝ) := by positivity
    have hd_lt_d1 : (d : ℝ) < ((d + 1 : ℕ) : ℝ) := by exact_mod_cast (Nat.lt_succ_self d)
    have ha_pos : 0 < a := by dsimp [a]; positivity
    have hb_pos : 0 < b := by dsimp [b]; positivity
    have hb_lt_a : b < a := by
      dsimp [a, b]
      exact one_div_lt_one_div_of_lt (Real.sqrt_pos.mpr hd_pos) (Real.sqrt_lt_sqrt (le_of_lt hd_pos) hd_lt_d1)
    have h_exp_norm :
        ∀ x : ℝ, ‖Complex.exp (-(Complex.I * (v : ℂ) * (x : ℂ)))‖ = 1 := by
      intro x
      have h_arg : -(Complex.I * (v : ℂ) * (x : ℂ)) = ((-(v * x) : ℝ) : ℂ) * Complex.I := by
        push_cast; ring
      rw [h_arg]
      exact Complex.norm_exp_ofReal_mul_I (-(v * x))
    apply le_min
    · unfold adjacentDilationMultiplier
      calc
        ‖((a : ℝ) : ℂ) * Complex.exp (-(Complex.I * (v : ℂ) * (Real.log (d : ℝ) : ℂ))) -
            ((b : ℝ) : ℂ) *
              Complex.exp (-(Complex.I * (v : ℂ) * (Real.log ((d + 1 : ℕ) : ℝ) : ℂ)))‖
          ≤ ‖((a : ℝ) : ℂ) * Complex.exp (-(Complex.I * (v : ℂ) * (Real.log (d : ℝ) : ℂ)))‖ +
              ‖((b : ℝ) : ℂ) *
                Complex.exp (-(Complex.I * (v : ℂ) * (Real.log ((d + 1 : ℕ) : ℝ) : ℂ)))‖ :=
            norm_sub_le _ _
        _ = a + b := by
            rw [norm_mul, norm_mul, Complex.norm_real, Complex.norm_real,
              Real.norm_of_nonneg (le_of_lt ha_pos), Real.norm_of_nonneg (le_of_lt hb_pos),
              h_exp_norm (Real.log (d : ℝ)), h_exp_norm (Real.log ((d + 1 : ℕ) : ℝ)),
              mul_one, mul_one]
    · let u : ℝ := (Real.log ((d + 1 : ℕ) : ℝ) - Real.log (d : ℝ)) / 2
      let θ : ℝ := 2 * v * u
      have hu_pos : 0 < u := by
        dsimp [u]
        linarith [Real.log_lt_log hd_pos hd_lt_d1]
      have h_factor :
          adjacentDilationMultiplier d v =
            Complex.exp (-(Complex.I * (v : ℂ) * (Real.log (d : ℝ) : ℂ))) *
              (((a : ℝ) : ℂ) - ((b : ℝ) : ℂ) * Complex.exp (((-θ : ℝ) : ℂ) * Complex.I)) := by
        have h_exp_split :
            Complex.exp (-(Complex.I * (v : ℂ) * (Real.log ((d + 1 : ℕ) : ℝ) : ℂ))) =
              Complex.exp (-(Complex.I * (v : ℂ) * (Real.log (d : ℝ) : ℂ))) *
                Complex.exp (((-θ : ℝ) : ℂ) * Complex.I) := by
          rw [← Complex.exp_add]
          congr 1
          dsimp [θ, u]
          push_cast
          ring
        unfold adjacentDilationMultiplier
        rw [h_exp_split]
        dsimp [a, b]
        ring
      have h_norm_eq :
          ‖adjacentDilationMultiplier d v‖ =
            ‖((a : ℝ) : ℂ) - ((b : ℝ) : ℂ) * Complex.exp (((-θ : ℝ) : ℂ) * Complex.I)‖ := by
        rw [h_factor, norm_mul, h_exp_norm (Real.log (d : ℝ)), one_mul]
      have h_norm_sq :
          ‖((a : ℝ) : ℂ) - ((b : ℝ) : ℂ) * Complex.exp (((-θ : ℝ) : ℂ) * Complex.I)‖ ^ 2 =
            (a - b) ^ 2 + 4 * a * b * (Real.sin (v * u)) ^ 2 := by
        rw [Complex.norm_eq_abs, Complex.sq_abs, Complex.exp_mul_I]
        have h_z :
            (((a : ℝ) : ℂ) -
                ((b : ℝ) : ℂ) *
                  (Complex.cos ((-θ : ℝ) : ℂ) + Complex.sin ((-θ : ℝ) : ℂ) * Complex.I)) =
              (((a - b * Real.cos (-θ) : ℝ) : ℂ) +
                ((-b * Real.sin (-θ) : ℝ) : ℂ) * Complex.I) := by
          rw [← Complex.ofReal_cos, ← Complex.ofReal_sin]
          push_cast; ring
        rw [h_z, Complex.normSq_add_mul_I, Real.cos_neg, Real.sin_neg]
        have h_trig : (Real.cos θ) ^ 2 + (Real.sin θ) ^ 2 = 1 := by
          rw [add_comm]; exact Real.sin_sq_add_cos_sq θ
        have h_half : Real.cos θ = 1 - 2 * (Real.sin (v * u)) ^ 2 := by
          have h2 : θ = 2 * (v * u) := by dsimp [θ]; ring
          rw [h2, Real.cos_two_mul]
          linarith [Real.sin_sq_add_cos_sq (v * u)]
        calc
          (a - b * Real.cos θ) ^ 2 + (-b * -Real.sin θ) ^ 2
            = a ^ 2 - 2 * a * b * Real.cos θ + b ^ 2 * ((Real.cos θ) ^ 2 + (Real.sin θ) ^ 2) := by
                ring
          _ = a ^ 2 - 2 * a * b * (1 - 2 * (Real.sin (v * u)) ^ 2) + b ^ 2 * 1 := by
                rw [h_trig, h_half]
          _ = (a - b) ^ 2 + 4 * a * b * (Real.sin (v * u)) ^ 2 := by ring
      have h_sin_sq : (Real.sin (v * u)) ^ 2 ≤ v ^ 2 * u ^ 2 := by
        have h_abs : |Real.sin (v * u)| ≤ |v * u| := abs_sin_le_abs_tc060_aux (v * u)
        have h_sq := pow_le_pow_left (abs_nonneg _) h_abs 2
        rwa [sq_abs, sq_abs, mul_pow] at h_sq
      have h_exp_u : Real.exp u = a / b := by
        have h_2u : 2 * u = Real.log (((d + 1 : ℕ) : ℝ) / (d : ℝ)) := by
          dsimp [u]
          rw [Real.log_div (ne_of_gt hd1_pos) (ne_of_gt hd_pos)]
          ring
        have h_ab_pos : 0 < a / b := div_pos ha_pos hb_pos
        have h_sq_eq : (Real.exp u) ^ 2 = (a / b) ^ 2 := by
          rw [sq, ← Real.exp_add, show u + u = 2 * u by ring, h_2u,
            Real.exp_log (div_pos hd1_pos hd_pos)]
          dsimp [a, b]
          have hab_simp :
              (1 / Real.sqrt (d : ℝ)) / (1 / Real.sqrt ((d + 1 : ℕ) : ℝ)) =
                Real.sqrt ((d + 1 : ℕ) : ℝ) / Real.sqrt (d : ℝ) := by
            field_simp [ne_of_gt (Real.sqrt_pos.mpr hd_pos),
              ne_of_gt (Real.sqrt_pos.mpr hd1_pos)]
          rw [hab_simp, div_pow, Real.sq_sqrt (le_of_lt hd1_pos),
            Real.sq_sqrt (le_of_lt hd_pos)]
        rw [← Real.sqrt_sq (le_of_lt (Real.exp_pos u)),
          ← Real.sqrt_sq (le_of_lt h_ab_pos), h_sq_eq]
      have h_exp_neg_u : Real.exp (-u) = b / a := by
        rw [Real.exp_neg, h_exp_u, inv_div]
      have h_ab_cosh : a * b * (Real.exp u + Real.exp (-u) - 2) = (a - b) ^ 2 := by
        rw [h_exp_u, h_exp_neg_u]
        field_simp [ne_of_gt ha_pos, ne_of_gt hb_pos]
        ring
      have h_u_sq : u ^ 2 ≤ Real.exp u + Real.exp (-u) - 2 :=
        sq_le_cosh_two_sub_two_tc060_aux (le_of_lt hu_pos)
      have h_ab_u_sq : a * b * u ^ 2 ≤ (a - b) ^ 2 := by
        rw [← h_ab_cosh]
        exact mul_le_mul_of_nonneg_left h_u_sq (mul_nonneg (le_of_lt ha_pos) (le_of_lt hb_pos))
      have h_tot_sq :
          ‖adjacentDilationMultiplier d v‖ ^ 2 ≤
            (Real.sqrt (1 / 4 + v ^ 2) * (2 * (a - b))) ^ 2 := by
        rw [h_norm_eq, h_norm_sq, mul_pow, Real.sq_sqrt (by positivity)]
        have h1 : 4 * a * b * (Real.sin (v * u)) ^ 2 ≤ 4 * v ^ 2 * (a * b * u ^ 2) := by
          have hab4 : 0 ≤ 4 * a * b := by positivity
          have hm := mul_le_mul_of_nonneg_left h_sin_sq hab4
          linarith
        have h2 : 4 * v ^ 2 * (a * b * u ^ 2) ≤ 4 * v ^ 2 * (a - b) ^ 2 :=
          mul_le_mul_of_nonneg_left h_ab_u_sq (by positivity)
        linarith
      have h_rhs_nn : 0 ≤ Real.sqrt (1 / 4 + v ^ 2) * (2 * (a - b)) :=
        mul_nonneg (Real.sqrt_nonneg _) (by linarith)
      calc
        ‖adjacentDilationMultiplier d v‖
          = Real.sqrt (‖adjacentDilationMultiplier d v‖ ^ 2) :=
              (Real.sqrt_sq (norm_nonneg _)).symm
        _ ≤ Real.sqrt ((Real.sqrt (1 / 4 + v ^ 2) * (2 * (a - b))) ^ 2) :=
              Real.sqrt_le_sqrt h_tot_sq
        _ = Real.sqrt (1 / 4 + v ^ 2) * (2 * (a - b)) := Real.sqrt_sq h_rhs_nn
  · intro d hd k
    let a : ℝ := 1 / Real.sqrt (d : ℝ)
    let b : ℝ := 1 / Real.sqrt ((d + 1 : ℕ) : ℝ)
    let v : ℝ := resonantMultiplierFreq d k
    have hd_pos : (0 : ℝ) < (d : ℝ) := Nat.cast_pos.mpr hd
    have hd1_pos : (0 : ℝ) < ((d + 1 : ℕ) : ℝ) := by positivity
    have hd_lt_d1 : (d : ℝ) < ((d + 1 : ℕ) : ℝ) := by exact_mod_cast (Nat.lt_succ_self d)
    have hlog_ratio_pos : 0 < Real.log (((d + 1 : ℕ) : ℝ) / (d : ℝ)) :=
      Real.log_pos ((one_lt_div hd_pos).mpr hd_lt_d1)
    have hlog_ratio_ne : Real.log (((d + 1 : ℕ) : ℝ) / (d : ℝ)) ≠ 0 := ne_of_gt hlog_ratio_pos
    have hlog_diff :
        Real.log ((d + 1 : ℕ) : ℝ) - Real.log (d : ℝ) =
          Real.log (((d + 1 : ℕ) : ℝ) / (d : ℝ)) :=
      (Real.log_div (ne_of_gt hd1_pos) (ne_of_gt hd_pos)).symm
    have h_v_diff :
        v * (Real.log ((d + 1 : ℕ) : ℝ) - Real.log (d : ℝ)) =
          ((2 * k + 1 : ℤ) : ℝ) * RiemannScope.tau / 2 := by
      dsimp [v, resonantMultiplierFreq]
      rw [hlog_diff, div_mul_eq_mul_div, mul_div_mul_right _ _ hlog_ratio_ne]
    have h_factor :
        adjacentDilationMultiplier d v =
          Complex.exp (-(Complex.I * (v : ℂ) * (Real.log (d : ℝ) : ℂ))) *
            (((a : ℝ) : ℂ) -
              ((b : ℝ) : ℂ) *
                Complex.exp
                  (-(Complex.I *
                    ((((2 * k + 1 : ℤ) : ℝ) * RiemannScope.tau / 2 : ℝ) : ℂ)))) := by
      have h_exp_split :
          Complex.exp (-(Complex.I * (v : ℂ) * (Real.log ((d + 1 : ℕ) : ℝ) : ℂ))) =
            Complex.exp (-(Complex.I * (v : ℂ) * (Real.log (d : ℝ) : ℂ))) *
              Complex.exp
                (-(Complex.I *
                  ((((2 * k + 1 : ℤ) : ℝ) * RiemannScope.tau / 2 : ℝ) : ℂ))) := by
        rw [← Complex.exp_add, ← h_v_diff]
        congr 1
        push_cast
        ring
      unfold adjacentDilationMultiplier
      rw [h_exp_split]
      dsimp [a, b, v]
      ring
    have h_odd_exp :
        Complex.exp
            (-(Complex.I * ((((2 * k + 1 : ℤ) : ℝ) * RiemannScope.tau / 2 : ℝ) : ℂ))) = -1 := by
      have h_half :
          Complex.exp (((RiemannScope.tau / 2 : ℝ) : ℂ) * Complex.I) = -1 := by
        have h_half_tau : ∀ x : ℝ, ((2 * x / 2 : ℝ) : ℂ) * Complex.I = (x : ℂ) * Complex.I := by
          intro x; push_cast; ring
        unfold RiemannScope.tau
        rw [h_half_tau]
        simp
      have h_full :
          Complex.exp ((RiemannScope.tau : ℂ) * Complex.I) = 1 := by
        have h_two :
            (RiemannScope.tau : ℂ) * Complex.I =
              ((RiemannScope.tau / 2 : ℝ) : ℂ) * Complex.I +
                ((RiemannScope.tau / 2 : ℝ) : ℂ) * Complex.I := by
          push_cast; ring
        rw [h_two, Complex.exp_add, h_half]
        norm_num
      let m : ℤ := -(k + 1)
      have h_arg_eq :
          -(Complex.I * ((((2 * k + 1 : ℤ) : ℝ) * RiemannScope.tau / 2 : ℝ) : ℂ)) =
            (m : ℂ) * ((RiemannScope.tau : ℂ) * Complex.I) +
              ((RiemannScope.tau / 2 : ℝ) : ℂ) * Complex.I := by
        dsimp [m]
        push_cast
        ring
      rw [h_arg_eq, Complex.exp_add, Complex.exp_int_mul, h_full, one_zpow, h_half, one_mul]
    have h_unit :
        ‖Complex.exp (-(Complex.I * (v : ℂ) * (Real.log (d : ℝ) : ℂ)))‖ = 1 := by
      have h_arg :
          -(Complex.I * (v : ℂ) * (Real.log (d : ℝ) : ℂ)) =
            ((-(v * Real.log (d : ℝ)) : ℝ) : ℂ) * Complex.I := by
        push_cast; ring
      rw [h_arg]
      exact Complex.norm_exp_ofReal_mul_I _
    have hab_nn : 0 ≤ a + b := by dsimp [a, b]; positivity
    rw [h_factor, h_odd_exp, norm_mul, h_unit, one_mul]
    have h_sum_c : ((a : ℝ) : ℂ) - ((b : ℝ) : ℂ) * (-1) = ((a + b : ℝ) : ℂ) := by
      push_cast; ring
    rw [h_sum_c, Complex.norm_real, Real.norm_of_nonneg hab_nn]
  · have h_disj :
        ∀ T L₁ L₂ : ℕ, L₁ ≠ L₂ → Disjoint (cutoffLevelBlock T L₁) (cutoffLevelBlock T L₂) := by
      intro T L₁ L₂ hne
      rw [Finset.disjoint_left]
      intro d hd1 hd2
      simp only [cutoffLevelBlock, Finset.mem_filter] at hd1 hd2
      exact hne (hd1.2.symm.trans hd2.2)
    have h_biUnion :
        ∀ T : ℕ, (Finset.Icc 1 T).biUnion (cutoffLevelBlock T) = Finset.Icc 1 (T - 1) := by
      intro T
      ext d
      simp only [Finset.mem_biUnion, cutoffLevelBlock, Finset.mem_filter, Finset.mem_Icc]
      constructor
      · rintro ⟨_, _, hd, _⟩; exact hd
      · rintro ⟨hd1, hdT1⟩
        have hd_pos : 0 < d := by omega
        have hT_ge : d ≤ T := by omega
        exact ⟨T / d, ⟨Nat.div_pos hT_ge hd_pos, Nat.div_le_self T d⟩, ⟨hd1, hdT1⟩, rfl⟩
    have h_single :
        ∀ T d : ℕ, 1 ≤ d → d < T → d * (d + 1) ≤ T → cutoffLevelBlock T (T / d) = {d} := by
      intro T d hd1 hd_lt hdd
      ext e
      simp only [cutoffLevelBlock, Finset.mem_filter, Finset.mem_Icc, Finset.mem_singleton]
      constructor
      · rintro ⟨⟨he1, _⟩, he_div⟩
        let L := T / d
        have hL_ge : d + 1 ≤ L :=
          (Nat.le_div_iff_mul_le hd1).mpr (by rw [mul_comm]; exact hdd)
        have hdL_le : d * L ≤ T := Nat.mul_div_le T d
        have hT_lt_d : T < d * L + d := by
          have h1 := Nat.div_add_mod T d
          have h2 : T % d < d := Nat.mod_lt T hd1
          dsimp [L]
          omega
        have heL_le : e * L ≤ T := by
          dsimp [L]; rw [← he_div]; exact Nat.mul_div_le T e
        have hT_lt_e : T < e * L + e := by
          have h1 := Nat.div_add_mod T e
          have h2 : T % e < e := Nat.mod_lt T he1
          dsimp [L]; rw [← he_div]; omega
        rcases lt_trichotomy e d with h_lt | rfl | h_gt
        · have he1_le_d : (e + 1) * L ≤ d * L := Nat.mul_le_mul_right L (by omega)
          have h_exp : (e + 1) * L = e * L + L := Nat.succ_mul e L
          omega
        · rfl
        · have hd1_le_e : (d + 1) * L ≤ e * L := Nat.mul_le_mul_right L (by omega)
          have h_exp : (d + 1) * L = d * L + L := Nat.succ_mul d L
          omega
      · rintro rfl
        exact ⟨⟨hd1, by omega⟩, rfl⟩
    refine ⟨h_disj, h_biUnion, ⟨by decide, by decide⟩, ?_, ?_, h_single, ?_⟩
    · intro T c_lam v qhat
      rw [← h_biUnion T,
        Finset.sum_biUnion (fun L₁ _ L₂ _ hne => h_disj T L₁ L₂ hne)]
      apply Finset.sum_congr rfl
      intro L _
      unfold blockSignedMultiplier
      rw [Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro d hd
      simp only [cutoffLevelBlock, Finset.mem_filter] at hd
      rw [hd.2]
    · intro T c_lam X
      unfold smoothRemainderSumRsm
      rw [← h_biUnion T,
        Finset.sum_biUnion (fun L₁ _ L₂ _ hne => h_disj T L₁ L₂ hne)]
      apply Finset.sum_congr rfl
      intro L _
      apply Finset.sum_congr rfl
      intro d hd
      simp only [cutoffLevelBlock, Finset.mem_filter] at hd
      unfold scaledFiberSmoothStep
      rw [hd.2]
    · intro T
      by_cases hs : Nat.sqrt T ≤ 1
      · omega
      · have h_sq_le : Nat.sqrt T * Nat.sqrt T ≤ T := Nat.sqrt_le T
        let S := Finset.Icc 1 (Nat.sqrt T - 1)
        have hS_card : S.card = Nat.sqrt T - 1 := by
          dsimp [S]; simp
        have h_sub :
            S.image (fun d => T / d) ⊆
              (Finset.Icc 1 T).filter (fun L => (cutoffLevelBlock T L).Nonempty) := by
          rw [Finset.image_subset_iff]
          intro d hd
          dsimp [S] at hd
          rw [Finset.mem_Icc] at hd
          have hd1_le_s : d + 1 ≤ Nat.sqrt T := by omega
          have hdd : d * (d + 1) ≤ T := by
            have h1 : d * (d + 1) ≤ Nat.sqrt T * Nat.sqrt T :=
              Nat.mul_le_mul (by omega) hd1_le_s
            omega
          have hd_lt_T : d < T := by
            have h2 : d * 2 ≤ d * (d + 1) := Nat.mul_le_mul_left d (by omega)
            omega
          simp only [Finset.mem_filter, Finset.mem_Icc]
          refine ⟨⟨Nat.div_pos (by omega) hd.1, Nat.div_le_self T d⟩, ?_⟩
          rw [h_single T d hd.1 hd_lt_T hdd]
          exact Finset.singleton_nonempty d
        have h_inj : Set.InjOn (fun d => T / d) (S : Set ℕ) := by
          intro d1 hd1 d2 hd2 h_eq
          dsimp only at h_eq
          simp only [Finset.mem_coe, S, Finset.mem_Icc] at hd1 hd2
          have hdd1 : d1 * (d1 + 1) ≤ T :=
            le_trans (Nat.mul_le_mul (by omega) (by omega)) h_sq_le
          have hdd2 : d2 * (d2 + 1) ≤ T :=
            le_trans (Nat.mul_le_mul (by omega) (by omega)) h_sq_le
          have hd1_lt : d1 < T := by
            have h2 : d1 * 2 ≤ d1 * (d1 + 1) := Nat.mul_le_mul_left d1 (by omega)
            omega
          have hd2_lt : d2 < T := by
            have h2 : d2 * 2 ≤ d2 * (d2 + 1) := Nat.mul_le_mul_left d2 (by omega)
            omega
          have hs1 := h_single T d1 hd1.1 hd1_lt hdd1
          have hs2 := h_single T d2 hd2.1 hd2_lt hdd2
          have h_sing_eq : ({d1} : Finset ℕ) = {d2} := by
            rw [← hs1, ← hs2, h_eq]
          exact Finset.singleton_injective h_sing_eq
        rw [← hS_card, ← Finset.card_image_of_injOn h_inj]
        exact Finset.card_le_card h_sub

/-! ### Section 3: Signed Gram Kernel and `(log X)^(-2)`-Weighted Quadratic Form (`TASK-TC-060` §3) -/

/-- Parameterized logarithmic window pairing `⟨f, g⟩_{Y,b} := ∫_Y^{b Y} f(X) g(X) dX / X`. -/
noncomputable def paramWindowPairing (Y b : ℝ) (f g : ℝ → ℝ) : ℝ :=
  ∫ X in Y..(b * Y), f X * g X / X

/-- Parameterized logarithmic window norm squared `‖f‖_{Y,b}^2 := ⟨f, f⟩_{Y,b}`. -/
noncomputable def paramWindowNormSq (Y b : ℝ) (f : ℝ → ℝ) : ℝ :=
  paramWindowPairing Y b f f

/-- Parameterized Gaussian window kernel `K_{Y,b}(m, n) := ⟨φ_m, φ_n⟩_{Y,b}`. -/
noncomputable def paramWindowKernelK (Y b : ℝ) (m n : ℕ) : ℝ :=
  paramWindowPairing Y b (gaussianTermPhi m) (gaussianTermPhi n)

/-- Signed smooth-increment Gram matrix entry `H_{Y,b,T}(d, e) := ⟨Δ_d^{sm}, Δ_e^{sm}⟩_{Y,b}`. -/
noncomputable def signedSmoothGramH (Y b : ℝ) (T d e : ℕ) : ℝ :=
  paramWindowPairing Y b (scaledFiberSmoothStep T d) (scaledFiberSmoothStep T e)

/-- `(log X)^(-2)`-weighted Gaussian window kernel
    `K_{Y,b}^{log}(m, n) := ∫_Y^{b Y} (φ_m(X) / (log X)^2) (φ_n(X) / (log X)^2) dX / X`. -/
noncomputable def weightedLogWindowKernelK (Y b : ℝ) (m n : ℕ) : ℝ :=
  ∫ X in Y..(b * Y),
    (gaussianTermPhi m X / (Real.log X) ^ 2) * (gaussianTermPhi n X / (Real.log X) ^ 2) / X

/-- `(log X)^(-2)`-weighted signed smooth-increment Gram entry
    `H_{Y,b,T}^{log}(d, e) := ∫_Y^{b Y} (Δ_d^{sm}(X) / (log X)^2) (Δ_e^{sm}(X) / (log X)^2) dX / X`. -/
noncomputable def weightedSignedSmoothGramH (Y b : ℝ) (T d e : ℕ) : ℝ :=
  ∫ X in Y..(b * Y),
    (scaledFiberSmoothStep T d X / (Real.log X) ^ 2) *
      (scaledFiberSmoothStep T e X / (Real.log X) ^ 2) / X

private theorem uIcc_param_pos_tc060_aux {Y b : ℝ} (hY : 0 < Y) (hb : 1 < b) :
    Y ≤ b * Y ∧ ∀ X ∈ Set.uIcc Y (b * Y), 0 < X := by
  have hle : Y ≤ b * Y := by nlinarith
  refine ⟨hle, ?_⟩
  intro X hX
  rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX
  linarith

private theorem continuousOn_gaussianTermPhi_Ici_tc060_aux (m : ℕ) :
    ContinuousOn (gaussianTermPhi m) (Set.Ici 0) := by
  unfold gaussianTermPhi
  have h_rpow : ContinuousOn (fun X : ℝ => X ^ (5 / 2 : ℝ)) (Set.Ici 0) := by
    apply ContinuousOn.rpow_const continuousOn_id
    intro _ _; right; norm_num
  have h_exp :
      Continuous (fun X : ℝ => (((m : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (m : ℝ) ^ 2))) := by
    continuity
  exact h_rpow.mul h_exp.continuousOn

private theorem continuousOn_gaussianTermPhi_param_tc060_aux {Y b : ℝ} (hY : 0 < Y) (hb : 1 < b)
    (m : ℕ) :
    ContinuousOn (gaussianTermPhi m) (Set.uIcc Y (b * Y)) := by
  apply (continuousOn_gaussianTermPhi_Ici_tc060_aux m).mono
  intro X hX
  exact le_of_lt ((uIcc_param_pos_tc060_aux hY hb).2 X hX)

private theorem continuousOn_scaledFiberSmoothStep_param_tc060_aux {Y b : ℝ} (hY : 0 < Y)
    (hb : 1 < b) (T d : ℕ) :
    ContinuousOn (scaledFiberSmoothStep T d) (Set.uIcc Y (b * Y)) := by
  have h_Q_cont : ∀ (L : ℕ) (m : ℝ), 0 ≤ m →
      ContinuousOn (fun X => finiteQLambda L (X / m)) (Set.uIcc Y (b * Y)) := by
    intro L m hm_nn
    have h_eq : ∀ W : ℝ, finiteQLambda L W =
        ∑ q ∈ Finset.Icc 1 L, (liouvilleLambda q : ℝ) * gaussianTermPhi q W := by
      intro W; dsimp [finiteQLambda, gaussianTermPhi]
      rw [Finset.mul_sum]; apply Finset.sum_congr rfl; intro q _; ring
    have h_fn : (fun X => finiteQLambda L (X / m)) =
        fun X => ∑ q ∈ Finset.Icc 1 L, (liouvilleLambda q : ℝ) * gaussianTermPhi q (X / m) := by
      ext X; exact h_eq (X / m)
    rw [h_fn]
    refine continuousOn_finset_sum _ (fun q _ => continuousOn_const.mul ?_)
    exact (continuousOn_gaussianTermPhi_Ici_tc060_aux q).comp (continuousOn_id.div_const m)
      (fun X hX => div_nonneg (le_of_lt ((uIcc_param_pos_tc060_aux hY hb).2 X hX)) hm_nn)
  unfold scaledFiberSmoothStep
  exact (continuousOn_const.mul (h_Q_cont (T / d) (d : ℝ) (Nat.cast_nonneg d))).sub
    (continuousOn_const.mul (h_Q_cont (T / d) ((d + 1 : ℕ) : ℝ) (Nat.cast_nonneg _)))

private theorem intervalIntegrable_param_tc060_aux {Y b : ℝ} (hY : 0 < Y) (hb : 1 < b)
    {f g : ℝ → ℝ}
    (hf : ContinuousOn f (Set.uIcc Y (b * Y)))
    (hg : ContinuousOn g (Set.uIcc Y (b * Y))) :
    IntervalIntegrable (fun X => f X * g X / X) volume Y (b * Y) := by
  apply ContinuousOn.intervalIntegrable
  apply ContinuousOn.div (hf.mul hg) continuousOn_id
  intro X hX
  exact ne_of_gt ((uIcc_param_pos_tc060_aux hY hb).2 X hX)

private theorem paramWindowNormSq_nonneg_tc060_aux {Y b : ℝ} (hY : 0 < Y) (hb : 1 < b)
    (f : ℝ → ℝ) :
    0 ≤ paramWindowNormSq Y b f := by
  obtain ⟨hle, hpos⟩ := uIcc_param_pos_tc060_aux hY hb
  unfold paramWindowNormSq paramWindowPairing
  apply intervalIntegral.integral_nonneg hle
  intro X hX
  have hX_pos : 0 < X := hpos X (by rwa [Set.uIcc_of_le hle])
  exact div_nonneg (mul_self_nonneg (f X)) (le_of_lt hX_pos)

private theorem scaledFiberSmoothStep_sum_phi_tc060_aux (T : ℕ) {d : ℕ} (hd : 1 ≤ d) {X : ℝ}
    (hX : 0 ≤ X) :
    scaledFiberSmoothStep T d X =
      ∑ q ∈ Finset.Icc 1 (T / d),
        (liouvilleLambda q : ℝ) *
          (gaussianTermPhi (d * q) X - gaussianTermPhi ((d + 1) * q) X) := by
  have hd_pos : 0 < d := by omega
  have hd1_pos : 0 < d + 1 := by omega
  have hQ : ∀ (L : ℕ) (W : ℝ), finiteQLambda L W =
      ∑ q ∈ Finset.Icc 1 L, (liouvilleLambda q : ℝ) * gaussianTermPhi q W := by
    intro L W; dsimp [finiteQLambda, gaussianTermPhi]
    rw [Finset.mul_sum]; apply Finset.sum_congr rfl; intro q _; ring
  unfold scaledFiberSmoothStep
  rw [hQ, hQ, Finset.mul_sum, Finset.mul_sum, ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro q _
  rw [gaussianTermPhi_mul_scale_tc060_aux hd_pos q hX,
    gaussianTermPhi_mul_scale_tc060_aux hd1_pos q hX]
  ring

private theorem paramWindowPairing_finset_sum_tc060_aux {α β : Type*} {Y b : ℝ}
    (hY : 0 < Y) (hb : 1 < b) (S₁ : Finset α) (S₂ : Finset β)
    (f : α → ℝ → ℝ) (g : β → ℝ → ℝ)
    (hf : ∀ i ∈ S₁, ContinuousOn (f i) (Set.uIcc Y (b * Y)))
    (hg : ∀ j ∈ S₂, ContinuousOn (g j) (Set.uIcc Y (b * Y))) :
    paramWindowPairing Y b (fun X => ∑ i ∈ S₁, f i X) (fun X => ∑ j ∈ S₂, g j X) =
      ∑ i ∈ S₁, ∑ j ∈ S₂, paramWindowPairing Y b (f i) (g j) := by
  unfold paramWindowPairing
  have h_pt :
      (fun X => (∑ i ∈ S₁, f i X) * (∑ j ∈ S₂, g j X) / X) =
        fun X => ∑ i ∈ S₁, ∑ j ∈ S₂, f i X * g j X / X := by
    ext X
    rw [Finset.sum_mul_sum, Finset.sum_div]
    apply Finset.sum_congr rfl
    intro i _
    rw [Finset.sum_div]
  rw [h_pt]
  have h_outer :
      ∀ i ∈ S₁,
        IntervalIntegrable (fun X => ∑ j ∈ S₂, f i X * g j X / X) volume Y (b * Y) := by
    intro i hi
    have h_fn :
        (fun X => ∑ j ∈ S₂, f i X * g j X / X) =
          ∑ j ∈ S₂, fun X => f i X * g j X / X := by
      ext X; simp [Finset.sum_apply]
    rw [h_fn]
    exact IntervalIntegrable.sum S₂ (fun j hj =>
      intervalIntegrable_param_tc060_aux hY hb (hf i hi) (hg j hj))
  rw [intervalIntegral.integral_finset_sum h_outer]
  apply Finset.sum_congr rfl
  intro i hi
  exact intervalIntegral.integral_finset_sum (fun j hj =>
    intervalIntegrable_param_tc060_aux hY hb (hf i hi) (hg j hj))

/-- **Theorem 3 (`TASK-TC-060` §3, Parameterized Signed Gram Kernel, PSD Real-Space Quadratic Form, and `(log X)^(-2)`-Weighted Window Sandwich)**:
    1. *Canonical `b = RiemannScope.tau` specialization*:
       `paramWindowPairing Y RiemannScope.tau f g = windowPairing Y f g` and
       `paramWindowKernelK Y RiemannScope.tau m n = windowKernelK Y m n`;
    2. *Exact 4-term signed Gram matrix formula (`Y > 0, b > 1, d ≥ 1, e ≥ 1`)*;
    3. *Complete real-space quadratic form and positive semidefiniteness (`Y > 0, b > 1`)*;
    4. *Weighted `(log X)^(-2)` Gram formula, quadratic form, and two-sided logarithmic window sandwich (`Y ≥ 2, b > 1`)*. -/
theorem signed_gram_kernel_and_log_weighted_quadratic_form_tc060 :
    ((∀ (Y : ℝ) (f g : ℝ → ℝ),
        paramWindowPairing Y RiemannScope.tau f g = windowPairing Y f g) ∧
      (∀ (Y : ℝ) (m n : ℕ),
        paramWindowKernelK Y RiemannScope.tau m n = windowKernelK Y m n)) ∧
    (∀ {Y b : ℝ}, 0 < Y → 1 < b → ∀ (T d e : ℕ), 1 ≤ d → 1 ≤ e →
      signedSmoothGramH Y b T d e =
        ∑ q ∈ Finset.Icc 1 (T / d), ∑ r ∈ Finset.Icc 1 (T / e),
          (liouvilleLambda q : ℝ) * (liouvilleLambda r : ℝ) *
            (paramWindowKernelK Y b (d * q) (e * r) -
              paramWindowKernelK Y b ((d + 1) * q) (e * r) -
              paramWindowKernelK Y b (d * q) ((e + 1) * r) +
              paramWindowKernelK Y b ((d + 1) * q) ((e + 1) * r))) ∧
    (∀ {Y b : ℝ}, 0 < Y → 1 < b → ∀ (T : ℕ) (c_lam : ℝ),
      paramWindowNormSq Y b (smoothRemainderSumRsm c_lam T) =
          (∑ d ∈ Finset.Icc 1 (T - 1), ∑ e ∈ Finset.Icc 1 (T - 1),
            selbergCenteredRemainderInt c_lam d * selbergCenteredRemainderInt c_lam e *
              signedSmoothGramH Y b T d e) ∧
        ∀ w : ℕ → ℝ,
          0 ≤ ∑ d ∈ Finset.Icc 1 (T - 1), ∑ e ∈ Finset.Icc 1 (T - 1),
            w d * w e * signedSmoothGramH Y b T d e) ∧
    (∀ {Y b : ℝ}, 2 ≤ Y → 1 < b →
      (∀ (T d e : ℕ), 1 ≤ d → 1 ≤ e →
        weightedSignedSmoothGramH Y b T d e =
          ∑ q ∈ Finset.Icc 1 (T / d), ∑ r ∈ Finset.Icc 1 (T / e),
            (liouvilleLambda q : ℝ) * (liouvilleLambda r : ℝ) *
              (weightedLogWindowKernelK Y b (d * q) (e * r) -
                weightedLogWindowKernelK Y b ((d + 1) * q) (e * r) -
                weightedLogWindowKernelK Y b (d * q) ((e + 1) * r) +
                weightedLogWindowKernelK Y b ((d + 1) * q) ((e + 1) * r))) ∧
      (∀ (T : ℕ) (c_lam : ℝ),
        paramWindowNormSq Y b (fun X => smoothRemainderSumRsm c_lam T X / (Real.log X) ^ 2) =
          ∑ d ∈ Finset.Icc 1 (T - 1), ∑ e ∈ Finset.Icc 1 (T - 1),
            selbergCenteredRemainderInt c_lam d * selbergCenteredRemainderInt c_lam e *
              weightedSignedSmoothGramH Y b T d e) ∧
      (∀ {f : ℝ → ℝ}, ContinuousOn f (Set.uIcc Y (b * Y)) →
        (1 / (Real.log (b * Y)) ^ 4) * paramWindowNormSq Y b f ≤
            paramWindowNormSq Y b (fun X => f X / (Real.log X) ^ 2) ∧
          paramWindowNormSq Y b (fun X => f X / (Real.log X) ^ 2) ≤
            (1 / (Real.log Y) ^ 4) * paramWindowNormSq Y b f)) := by
  refine ⟨⟨fun _ _ _ => rfl, fun _ _ _ => rfl⟩, ?_, ?_, ?_⟩
  · intro Y b hY hb T d e hd he
    obtain ⟨_, hpos⟩ := uIcc_param_pos_tc060_aux hY hb
    let fq : ℕ → ℝ → ℝ := fun q X =>
      (liouvilleLambda q : ℝ) * (gaussianTermPhi (d * q) X - gaussianTermPhi ((d + 1) * q) X)
    let gr : ℕ → ℝ → ℝ := fun r X =>
      (liouvilleLambda r : ℝ) * (gaussianTermPhi (e * r) X - gaussianTermPhi ((e + 1) * r) X)
    have hfq_cont : ∀ q ∈ Finset.Icc 1 (T / d), ContinuousOn (fq q) (Set.uIcc Y (b * Y)) := by
      intro q _
      exact continuousOn_const.mul
        ((continuousOn_gaussianTermPhi_param_tc060_aux hY hb (d * q)).sub
          (continuousOn_gaussianTermPhi_param_tc060_aux hY hb ((d + 1) * q)))
    have hgr_cont : ∀ r ∈ Finset.Icc 1 (T / e), ContinuousOn (gr r) (Set.uIcc Y (b * Y)) := by
      intro r _
      exact continuousOn_const.mul
        ((continuousOn_gaussianTermPhi_param_tc060_aux hY hb (e * r)).sub
          (continuousOn_gaussianTermPhi_param_tc060_aux hY hb ((e + 1) * r)))
    have h_congr :
        signedSmoothGramH Y b T d e =
          paramWindowPairing Y b
            (fun X => ∑ q ∈ Finset.Icc 1 (T / d), fq q X)
            (fun X => ∑ r ∈ Finset.Icc 1 (T / e), gr r X) := by
      unfold signedSmoothGramH paramWindowPairing
      apply intervalIntegral.integral_congr
      intro X hX
      have hX_nn : 0 ≤ X := le_of_lt (hpos X hX)
      dsimp only
      rw [scaledFiberSmoothStep_sum_phi_tc060_aux T hd hX_nn,
        scaledFiberSmoothStep_sum_phi_tc060_aux T he hX_nn]
    rw [h_congr, paramWindowPairing_finset_sum_tc060_aux hY hb _ _ fq gr hfq_cont hgr_cont]
    apply Finset.sum_congr rfl
    intro q _
    apply Finset.sum_congr rfl
    intro r _
    unfold paramWindowPairing paramWindowKernelK
    have hi1 := intervalIntegrable_param_tc060_aux hY hb
      (continuousOn_gaussianTermPhi_param_tc060_aux hY hb (d * q))
      (continuousOn_gaussianTermPhi_param_tc060_aux hY hb (e * r))
    have hi2 := intervalIntegrable_param_tc060_aux hY hb
      (continuousOn_gaussianTermPhi_param_tc060_aux hY hb ((d + 1) * q))
      (continuousOn_gaussianTermPhi_param_tc060_aux hY hb (e * r))
    have hi3 := intervalIntegrable_param_tc060_aux hY hb
      (continuousOn_gaussianTermPhi_param_tc060_aux hY hb (d * q))
      (continuousOn_gaussianTermPhi_param_tc060_aux hY hb ((e + 1) * r))
    have hi4 := intervalIntegrable_param_tc060_aux hY hb
      (continuousOn_gaussianTermPhi_param_tc060_aux hY hb ((d + 1) * q))
      (continuousOn_gaussianTermPhi_param_tc060_aux hY hb ((e + 1) * r))
    have h_pt :
        (fun X => fq q X * gr r X / X) =
          fun X =>
            ((liouvilleLambda q : ℝ) * (liouvilleLambda r : ℝ)) *
              (((gaussianTermPhi (d * q) X * gaussianTermPhi (e * r) X / X -
                  gaussianTermPhi ((d + 1) * q) X * gaussianTermPhi (e * r) X / X) -
                gaussianTermPhi (d * q) X * gaussianTermPhi ((e + 1) * r) X / X) +
                gaussianTermPhi ((d + 1) * q) X * gaussianTermPhi ((e + 1) * r) X / X) := by
      ext X; dsimp [fq, gr]; ring
    rw [h_pt, intervalIntegral.integral_const_mul,
      intervalIntegral.integral_add ((hi1.sub hi2).sub hi3) hi4,
      intervalIntegral.integral_sub (hi1.sub hi2) hi3,
      intervalIntegral.integral_sub hi1 hi2]
    rfl
  · intro Y b hY hb T c_lam
    have h_quad_gen :
        ∀ w : ℕ → ℝ,
          paramWindowNormSq Y b
              (fun X => ∑ d ∈ Finset.Icc 1 (T - 1), w d * scaledFiberSmoothStep T d X) =
            ∑ d ∈ Finset.Icc 1 (T - 1), ∑ e ∈ Finset.Icc 1 (T - 1),
              w d * w e * signedSmoothGramH Y b T d e := by
      intro w
      let fd : ℕ → ℝ → ℝ := fun d X => w d * scaledFiberSmoothStep T d X
      have hfd_cont :
          ∀ d ∈ Finset.Icc 1 (T - 1), ContinuousOn (fd d) (Set.uIcc Y (b * Y)) := by
        intro d _
        exact continuousOn_const.mul
          (continuousOn_scaledFiberSmoothStep_param_tc060_aux hY hb T d)
      unfold paramWindowNormSq
      rw [paramWindowPairing_finset_sum_tc060_aux hY hb _ _ fd fd hfd_cont hfd_cont]
      apply Finset.sum_congr rfl
      intro d _
      apply Finset.sum_congr rfl
      intro e _
      unfold paramWindowPairing signedSmoothGramH
      have h_pt :
          (fun X => fd d X * fd e X / X) =
            fun X => (w d * w e) * (scaledFiberSmoothStep T d X * scaledFiberSmoothStep T e X / X) := by
        ext X; dsimp [fd]; ring
      rw [h_pt, intervalIntegral.integral_const_mul]
      rfl
    refine ⟨h_quad_gen (selbergCenteredRemainderInt c_lam), ?_⟩
    intro w
    rw [← h_quad_gen w]
    exact paramWindowNormSq_nonneg_tc060_aux hY hb _
  · intro Y b hY2 hb
    have hY_pos : 0 < Y := by linarith
    obtain ⟨hle, hpos⟩ := uIcc_param_pos_tc060_aux hY_pos hb
    have h_log_pos_uIcc : ∀ X ∈ Set.uIcc Y (b * Y), 0 < Real.log X := by
      intro X hX
      rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX
      exact Real.log_pos (by linarith)
    have h_log_sq_ne : ∀ X ∈ Set.uIcc Y (b * Y), (Real.log X) ^ 2 ≠ 0 :=
      fun X hX => pow_ne_zero 2 (ne_of_gt (h_log_pos_uIcc X hX))
    have h_log_cont : ContinuousOn Real.log (Set.uIcc Y (b * Y)) := by
      apply ContinuousOn.log continuousOn_id
      intro X hX; exact ne_of_gt (hpos X hX)
    have h_log_sq_cont : ContinuousOn (fun X => (Real.log X) ^ 2) (Set.uIcc Y (b * Y)) :=
      h_log_cont.pow 2
    refine ⟨?_, ?_, ?_⟩
    · intro T d e hd he
      let fq : ℕ → ℝ → ℝ := fun q X =>
        (liouvilleLambda q : ℝ) *
          (gaussianTermPhi (d * q) X / (Real.log X) ^ 2 -
            gaussianTermPhi ((d + 1) * q) X / (Real.log X) ^ 2)
      let gr : ℕ → ℝ → ℝ := fun r X =>
        (liouvilleLambda r : ℝ) *
          (gaussianTermPhi (e * r) X / (Real.log X) ^ 2 -
            gaussianTermPhi ((e + 1) * r) X / (Real.log X) ^ 2)
      have h_phi_w_cont : ∀ m : ℕ,
          ContinuousOn (fun X => gaussianTermPhi m X / (Real.log X) ^ 2) (Set.uIcc Y (b * Y)) :=
        fun m => (continuousOn_gaussianTermPhi_param_tc060_aux hY_pos hb m).div
          h_log_sq_cont h_log_sq_ne
      have hfq_cont : ∀ q ∈ Finset.Icc 1 (T / d), ContinuousOn (fq q) (Set.uIcc Y (b * Y)) :=
        fun q _ => continuousOn_const.mul ((h_phi_w_cont (d * q)).sub (h_phi_w_cont ((d + 1) * q)))
      have hgr_cont : ∀ r ∈ Finset.Icc 1 (T / e), ContinuousOn (gr r) (Set.uIcc Y (b * Y)) :=
        fun r _ => continuousOn_const.mul ((h_phi_w_cont (e * r)).sub (h_phi_w_cont ((e + 1) * r)))
      have h_congr :
          weightedSignedSmoothGramH Y b T d e =
            paramWindowPairing Y b
              (fun X => ∑ q ∈ Finset.Icc 1 (T / d), fq q X)
              (fun X => ∑ r ∈ Finset.Icc 1 (T / e), gr r X) := by
        unfold weightedSignedSmoothGramH paramWindowPairing
        apply intervalIntegral.integral_congr
        intro X hX
        have hX_nn : 0 ≤ X := le_of_lt (hpos X hX)
        dsimp only [fq, gr]
        rw [scaledFiberSmoothStep_sum_phi_tc060_aux T hd hX_nn,
          scaledFiberSmoothStep_sum_phi_tc060_aux T he hX_nn, Finset.sum_div, Finset.sum_div]
        have hs1 :
            (∑ q ∈ Finset.Icc 1 (T / d),
                (liouvilleLambda q : ℝ) *
                  (gaussianTermPhi (d * q) X - gaussianTermPhi ((d + 1) * q) X) /
                  (Real.log X) ^ 2) =
              ∑ q ∈ Finset.Icc 1 (T / d),
                (liouvilleLambda q : ℝ) *
                  (gaussianTermPhi (d * q) X / (Real.log X) ^ 2 -
                    gaussianTermPhi ((d + 1) * q) X / (Real.log X) ^ 2) := by
          apply Finset.sum_congr rfl; intro q _; ring
        have hs2 :
            (∑ r ∈ Finset.Icc 1 (T / e),
                (liouvilleLambda r : ℝ) *
                  (gaussianTermPhi (e * r) X - gaussianTermPhi ((e + 1) * r) X) /
                  (Real.log X) ^ 2) =
              ∑ r ∈ Finset.Icc 1 (T / e),
                (liouvilleLambda r : ℝ) *
                  (gaussianTermPhi (e * r) X / (Real.log X) ^ 2 -
                    gaussianTermPhi ((e + 1) * r) X / (Real.log X) ^ 2) := by
          apply Finset.sum_congr rfl; intro r _; ring
        rw [hs1, hs2]
      rw [h_congr, paramWindowPairing_finset_sum_tc060_aux hY_pos hb _ _ fq gr hfq_cont hgr_cont]
      apply Finset.sum_congr rfl
      intro q _
      apply Finset.sum_congr rfl
      intro r _
      unfold paramWindowPairing weightedLogWindowKernelK
      have hi1 := intervalIntegrable_param_tc060_aux hY_pos hb
        (h_phi_w_cont (d * q)) (h_phi_w_cont (e * r))
      have hi2 := intervalIntegrable_param_tc060_aux hY_pos hb
        (h_phi_w_cont ((d + 1) * q)) (h_phi_w_cont (e * r))
      have hi3 := intervalIntegrable_param_tc060_aux hY_pos hb
        (h_phi_w_cont (d * q)) (h_phi_w_cont ((e + 1) * r))
      have hi4 := intervalIntegrable_param_tc060_aux hY_pos hb
        (h_phi_w_cont ((d + 1) * q)) (h_phi_w_cont ((e + 1) * r))
      have h_pt :
          (fun X => fq q X * gr r X / X) =
            fun X =>
              ((liouvilleLambda q : ℝ) * (liouvilleLambda r : ℝ)) *
                ((((gaussianTermPhi (d * q) X / (Real.log X) ^ 2) *
                      (gaussianTermPhi (e * r) X / (Real.log X) ^ 2) / X -
                    (gaussianTermPhi ((d + 1) * q) X / (Real.log X) ^ 2) *
                      (gaussianTermPhi (e * r) X / (Real.log X) ^ 2) / X) -
                  (gaussianTermPhi (d * q) X / (Real.log X) ^ 2) *
                    (gaussianTermPhi ((e + 1) * r) X / (Real.log X) ^ 2) / X) +
                  (gaussianTermPhi ((d + 1) * q) X / (Real.log X) ^ 2) *
                    (gaussianTermPhi ((e + 1) * r) X / (Real.log X) ^ 2) / X) := by
        ext X; dsimp [fq, gr]; ring
      rw [h_pt, intervalIntegral.integral_const_mul,
        intervalIntegral.integral_add ((hi1.sub hi2).sub hi3) hi4,
        intervalIntegral.integral_sub (hi1.sub hi2) hi3,
        intervalIntegral.integral_sub hi1 hi2]
    · intro T c_lam
      let fd : ℕ → ℝ → ℝ := fun d X =>
        selbergCenteredRemainderInt c_lam d * (scaledFiberSmoothStep T d X / (Real.log X) ^ 2)
      have hfd_cont :
          ∀ d ∈ Finset.Icc 1 (T - 1), ContinuousOn (fd d) (Set.uIcc Y (b * Y)) := by
        intro d _
        exact continuousOn_const.mul
          ((continuousOn_scaledFiberSmoothStep_param_tc060_aux hY_pos hb T d).div
            h_log_sq_cont h_log_sq_ne)
      have h_lhs_eq :
          paramWindowNormSq Y b (fun X => smoothRemainderSumRsm c_lam T X / (Real.log X) ^ 2) =
            paramWindowPairing Y b
              (fun X => ∑ d ∈ Finset.Icc 1 (T - 1), fd d X)
              (fun X => ∑ e ∈ Finset.Icc 1 (T - 1), fd e X) := by
        unfold paramWindowNormSq paramWindowPairing smoothRemainderSumRsm
        apply intervalIntegral.integral_congr
        intro X _
        dsimp only [fd]
        have hs :
            (∑ d ∈ Finset.Icc 1 (T - 1),
                selbergCenteredRemainderInt c_lam d * scaledFiberSmoothStep T d X) /
                (Real.log X) ^ 2 =
              ∑ d ∈ Finset.Icc 1 (T - 1),
                selbergCenteredRemainderInt c_lam d *
                  (scaledFiberSmoothStep T d X / (Real.log X) ^ 2) := by
          rw [Finset.sum_div]
          apply Finset.sum_congr rfl; intro d _; ring
        rw [hs]
      rw [h_lhs_eq, paramWindowPairing_finset_sum_tc060_aux hY_pos hb _ _ fd fd hfd_cont hfd_cont]
      apply Finset.sum_congr rfl
      intro d _
      apply Finset.sum_congr rfl
      intro e _
      unfold paramWindowPairing weightedSignedSmoothGramH
      have h_pt :
          (fun X => fd d X * fd e X / X) =
            fun X =>
              (selbergCenteredRemainderInt c_lam d * selbergCenteredRemainderInt c_lam e) *
                ((scaledFiberSmoothStep T d X / (Real.log X) ^ 2) *
                  (scaledFiberSmoothStep T e X / (Real.log X) ^ 2) / X) := by
        ext X; dsimp [fd]; ring
      rw [h_pt, intervalIntegral.integral_const_mul]
    · intro f hf
      have hf_w_cont : ContinuousOn (fun X => f X / (Real.log X) ^ 2) (Set.uIcc Y (b * Y)) :=
        hf.div h_log_sq_cont h_log_sq_ne
      have h_int_f := intervalIntegrable_param_tc060_aux hY_pos hb hf hf
      have h_int_fw := intervalIntegrable_param_tc060_aux hY_pos hb hf_w_cont hf_w_cont
      have hlogY_pos : 0 < Real.log Y := Real.log_pos (by linarith)
      unfold paramWindowNormSq paramWindowPairing
      refine ⟨?_, ?_⟩
      · rw [← intervalIntegral.integral_const_mul]
        apply intervalIntegral.integral_mono_on hle (h_int_f.const_mul _) h_int_fw
        intro X hX
        rw [Set.mem_Icc] at hX
        have hX_pos : 0 < X := lt_of_lt_of_le hY_pos hX.1
        have hlogX_pos : 0 < Real.log X := lt_of_lt_of_le hlogY_pos (Real.log_le_log hY_pos hX.1)
        have hlogX_le : Real.log X ≤ Real.log (b * Y) := Real.log_le_log hX_pos hX.2
        have hpow_le : (Real.log X) ^ 4 ≤ (Real.log (b * Y)) ^ 4 :=
          pow_le_pow_left (le_of_lt hlogX_pos) hlogX_le 4
        have h_inv_le : 1 / (Real.log (b * Y)) ^ 4 ≤ 1 / (Real.log X) ^ 4 :=
          one_div_le_one_div_of_le (pow_pos hlogX_pos 4) hpow_le
        have h_fx_nn : 0 ≤ f X * f X / X :=
          div_nonneg (mul_self_nonneg (f X)) (le_of_lt hX_pos)
        calc
          1 / (Real.log (b * Y)) ^ 4 * (f X * f X / X)
            ≤ 1 / (Real.log X) ^ 4 * (f X * f X / X) :=
              mul_le_mul_of_nonneg_right h_inv_le h_fx_nn
          _ = f X / (Real.log X) ^ 2 * (f X / (Real.log X) ^ 2) / X := by ring
      · rw [← intervalIntegral.integral_const_mul]
        apply intervalIntegral.integral_mono_on hle h_int_fw (h_int_f.const_mul _)
        intro X hX
        rw [Set.mem_Icc] at hX
        have hX_pos : 0 < X := lt_of_lt_of_le hY_pos hX.1
        have hlogY_le : Real.log Y ≤ Real.log X := Real.log_le_log hY_pos hX.1
        have hpow_le : (Real.log Y) ^ 4 ≤ (Real.log X) ^ 4 :=
          pow_le_pow_left (le_of_lt hlogY_pos) hlogY_le 4
        have h_inv_le : 1 / (Real.log X) ^ 4 ≤ 1 / (Real.log Y) ^ 4 :=
          one_div_le_one_div_of_le (pow_pos hlogY_pos 4) hpow_le
        have h_fx_nn : 0 ≤ f X * f X / X :=
          div_nonneg (mul_self_nonneg (f X)) (le_of_lt hX_pos)
        calc
          f X / (Real.log X) ^ 2 * (f X / (Real.log X) ^ 2) / X
            = 1 / (Real.log X) ^ 4 * (f X * f X / X) := by ring
          _ ≤ 1 / (Real.log Y) ^ 4 * (f X * f X / X) :=
              mul_le_mul_of_nonneg_right h_inv_le h_fx_nn

/-! ### Section 4: Gaussian Window Majorant, Local Frequency Split, and Gamma Monotonicity (`TASK-TC-060` §4) -/

/-- **Theorem 4 (`TASK-TC-060` §4, Gaussian Schwartz Window Majorant, Local Frequency-Split Cross-Term Retention, and Gauss-Product Gamma-Factor Monotonicity)**:
    1. *Gaussian Schwartz window majorant (`Y > 0, b > 1`)*:
       For `t0 := Real.log Y + Real.log b / 2` and `δ_b := Real.log b / 2`, `0 < δ_b`,
       `1 ≤ e * exp(-((t - t0)^2 / δ_b^2))` on `[log Y, log(b * Y)]`, and
       `paramWindowNormSq Y b f ≤ ∫ X in Y..(b * Y), e * exp(-((log X - t0)^2 / δ_b^2)) * (f X)^2 / X`;
    2. *Local-window frequency-split cross-term retention (`Y > 0, b > 1`)*:
       `paramWindowNormSq Y b (f_lo + f_hi) = paramWindowNormSq Y b f_lo + 2 * paramWindowPairing Y b f_lo f_hi + paramWindowNormSq Y b f_hi`
       and `≤ (√(paramWindowNormSq Y b f_lo) + √(paramWindowNormSq Y b f_hi))^2`;
    3. *Gauss-product Gamma-factor algebraic monotonicity (`3 / 4 ≤ m, 0 ≤ u`)*. -/
theorem gaussian_window_majorant_and_local_frequency_split_tc060 :
    (∀ {Y b : ℝ}, 0 < Y → 1 < b →
      let t0 := Real.log Y + Real.log b / 2
      let δ_b := Real.log b / 2
      0 < δ_b ∧
        (∀ t ∈ Set.Icc (Real.log Y) (Real.log (b * Y)),
          1 ≤ Real.exp 1 * Real.exp (-((t - t0) ^ 2 / δ_b ^ 2))) ∧
        (∀ {f : ℝ → ℝ}, ContinuousOn f (Set.uIcc Y (b * Y)) →
          paramWindowNormSq Y b f ≤
            ∫ X in Y..(b * Y),
              Real.exp 1 * Real.exp (-((Real.log X - t0) ^ 2 / δ_b ^ 2)) * (f X) ^ 2 / X)) ∧
    (∀ {Y b : ℝ}, 0 < Y → 1 < b →
      ∀ {f_lo f_hi : ℝ → ℝ},
        ContinuousOn f_lo (Set.uIcc Y (b * Y)) →
        ContinuousOn f_hi (Set.uIcc Y (b * Y)) →
        paramWindowNormSq Y b (fun X => f_lo X + f_hi X) =
            paramWindowNormSq Y b f_lo + 2 * paramWindowPairing Y b f_lo f_hi +
              paramWindowNormSq Y b f_hi ∧
          paramWindowNormSq Y b (fun X => f_lo X + f_hi X) ≤
            (Real.sqrt (paramWindowNormSq Y b f_lo) +
              Real.sqrt (paramWindowNormSq Y b f_hi)) ^ 2) ∧
    (∀ {m u : ℝ}, 3 / 4 ≤ m → 0 ≤ u →
      (((m - 1 / 2) ^ 2 + u) * ((m + 1 / 2) ^ 2 + u)) / (m ^ 2 + u) ^ 2 -
          (1 - 1 / (4 * m ^ 2)) ^ 2 =
        u * ((8 * m ^ 2 - 1) * u + 24 * m ^ 4 - 2 * m ^ 2) /
          (16 * m ^ 4 * (m ^ 2 + u) ^ 2) ∧
        (1 - 1 / (4 * m ^ 2)) ^ 2 ≤
          (((m - 1 / 2) ^ 2 + u) * ((m + 1 / 2) ^ 2 + u)) / (m ^ 2 + u) ^ 2) := by
  refine ⟨?_, ?_, ?_⟩
  · intro Y b hY hb
    dsimp only
    let t0 := Real.log Y + Real.log b / 2
    let δ_b := Real.log b / 2
    have hlogb_pos : 0 < Real.log b := Real.log_pos hb
    have hδ_pos : 0 < δ_b := by dsimp [δ_b]; linarith
    have hδ_sq_pos : 0 < δ_b ^ 2 := sq_pos_of_pos hδ_pos
    have hb_pos : 0 < b := lt_trans zero_lt_one hb
    have h_maj :
        ∀ t ∈ Set.Icc (Real.log Y) (Real.log (b * Y)),
          1 ≤ Real.exp 1 * Real.exp (-((t - t0) ^ 2 / δ_b ^ 2)) := by
      intro t ht
      rw [Set.mem_Icc, Real.log_mul (ne_of_gt hb_pos) (ne_of_gt hY)] at ht
      have h_abs : |t - t0| ≤ δ_b := by
        rw [abs_le]
        dsimp [t0, δ_b]
        constructor <;> linarith
      have h_sq_le : (t - t0) ^ 2 ≤ δ_b ^ 2 := by
        have h1 := pow_le_pow_left (abs_nonneg _) h_abs 2
        rwa [sq_abs] at h1
      have h_div_le : (t - t0) ^ 2 / δ_b ^ 2 ≤ 1 := (div_le_one hδ_sq_pos).mpr h_sq_le
      rw [← Real.exp_add, Real.one_le_exp_iff]
      linarith
    refine ⟨hδ_pos, h_maj, ?_⟩
    intro f hf
    obtain ⟨hle, hpos⟩ := uIcc_param_pos_tc060_aux hY hb
    have h_int_lhs := intervalIntegrable_param_tc060_aux hY hb hf hf
    have h_log_cont : ContinuousOn Real.log (Set.uIcc Y (b * Y)) :=
      ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hpos X hX))
    have h_gauss_cont :
        ContinuousOn (fun X => Real.exp 1 * Real.exp (-((Real.log X - t0) ^ 2 / δ_b ^ 2)))
          (Set.uIcc Y (b * Y)) := by
      have hg_in :
          ContinuousOn (fun X => -((Real.log X - t0) ^ 2 / δ_b ^ 2)) (Set.uIcc Y (b * Y)) :=
        (((h_log_cont.sub continuousOn_const).pow 2).div_const (δ_b ^ 2)).neg
      exact continuousOn_const.mul
        ((Real.continuous_exp.continuousOn).comp hg_in (fun _ _ => Set.mem_univ _))
    have h_int_rhs :
        IntervalIntegrable
          (fun X => Real.exp 1 * Real.exp (-((Real.log X - t0) ^ 2 / δ_b ^ 2)) * (f X) ^ 2 / X)
          volume Y (b * Y) := by
      have h_eq :
          (fun X => Real.exp 1 * Real.exp (-((Real.log X - t0) ^ 2 / δ_b ^ 2)) * (f X) ^ 2 / X) =
            fun X =>
              (Real.exp 1 * Real.exp (-((Real.log X - t0) ^ 2 / δ_b ^ 2)) * f X) * f X / X := by
        ext X; ring
      rw [h_eq]
      exact intervalIntegrable_param_tc060_aux hY hb (h_gauss_cont.mul hf) hf
    unfold paramWindowNormSq paramWindowPairing
    apply intervalIntegral.integral_mono_on hle h_int_lhs h_int_rhs
    intro X hX
    rw [Set.mem_Icc] at hX
    have hX_pos : 0 < X := lt_of_lt_of_le hY hX.1
    have h_t_mem : Real.log X ∈ Set.Icc (Real.log Y) (Real.log (b * Y)) :=
      ⟨Real.log_le_log hY hX.1, Real.log_le_log hX_pos hX.2⟩
    have h_g1 := h_maj (Real.log X) h_t_mem
    have h_fx_nn : 0 ≤ (f X) ^ 2 / X := div_nonneg (sq_nonneg _) (le_of_lt hX_pos)
    calc
      f X * f X / X = 1 * ((f X) ^ 2 / X) := by ring
      _ ≤ Real.exp 1 * Real.exp (-((Real.log X - t0) ^ 2 / δ_b ^ 2)) * ((f X) ^ 2 / X) :=
          mul_le_mul_of_nonneg_right h_g1 h_fx_nn
      _ = Real.exp 1 * Real.exp (-((Real.log X - t0) ^ 2 / δ_b ^ 2)) * (f X) ^ 2 / X := by ring
  · intro Y b hY hb f_lo f_hi hflo hfhi
    let A := paramWindowNormSq Y b f_lo
    let B := paramWindowNormSq Y b f_hi
    let P := paramWindowPairing Y b f_lo f_hi
    have hA_nn : 0 ≤ A := paramWindowNormSq_nonneg_tc060_aux hY hb f_lo
    have hB_nn : 0 ≤ B := paramWindowNormSq_nonneg_tc060_aux hY hb f_hi
    have h_int_ll := intervalIntegrable_param_tc060_aux hY hb hflo hflo
    have h_int_lh := intervalIntegrable_param_tc060_aux hY hb hflo hfhi
    have h_int_hh := intervalIntegrable_param_tc060_aux hY hb hfhi hfhi
    have h_lin :
        ∀ t : ℝ,
          paramWindowNormSq Y b (fun X => f_lo X + t * f_hi X) = A + 2 * t * P + t ^ 2 * B := by
      intro t
      unfold paramWindowNormSq paramWindowPairing
      have h_pt :
          (fun X => (f_lo X + t * f_hi X) * (f_lo X + t * f_hi X) / X) =
            fun X =>
              (f_lo X * f_lo X / X + (2 * t) * (f_lo X * f_hi X / X)) +
                (t ^ 2) * (f_hi X * f_hi X / X) := by
        ext X; ring
      rw [h_pt,
        intervalIntegral.integral_add (h_int_ll.add (h_int_lh.const_mul (2 * t)))
          (h_int_hh.const_mul (t ^ 2)),
        intervalIntegral.integral_add h_int_ll (h_int_lh.const_mul (2 * t)),
        intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul]
      dsimp [A, B, P, paramWindowNormSq, paramWindowPairing]
    have h_sum_eq :
        paramWindowNormSq Y b (fun X => f_lo X + f_hi X) = A + 2 * P + B := by
      have h1 := h_lin 1
      have h_fn : (fun X => f_lo X + (1 : ℝ) * f_hi X) = fun X => f_lo X + f_hi X := by
        ext X; ring
      rw [h_fn] at h1
      linarith
    have h_quad_nn : ∀ t : ℝ, 0 ≤ A + 2 * t * P + t ^ 2 * B := by
      intro t
      rw [← h_lin t]
      exact paramWindowNormSq_nonneg_tc060_aux hY hb _
    have h_P_sq : P ^ 2 ≤ A * B := by
      by_cases hB0 : B = 0
      · by_cases hP0 : P = 0
        · rw [hB0, hP0]; norm_num
        · exfalso
          have hq := h_quad_nn (-(A + 1) / (2 * P))
          rw [hB0, mul_zero, add_zero] at hq
          have h_simp : A + 2 * (-(A + 1) / (2 * P)) * P = -1 := by
            field_simp [hP0]; ring
          rw [h_simp] at hq
          linarith
      · have hB_pos : 0 < B := lt_of_le_of_ne hB_nn (Ne.symm hB0)
        have hq := h_quad_nn (-P / B)
        have h_mul := mul_le_mul_of_nonneg_right hq (le_of_lt hB_pos)
        have h_simp : (A + 2 * (-P / B) * P + (-P / B) ^ 2 * B) * B = A * B - P ^ 2 := by
          field_simp [hB0]; ring
        rw [zero_mul, h_simp] at h_mul
        linarith
    have hP_le : P ≤ Real.sqrt A * Real.sqrt B := by
      calc
        P ≤ |P| := le_abs_self P
        _ = Real.sqrt (P ^ 2) := (Real.sqrt_sq_eq_abs P).symm
        _ ≤ Real.sqrt (A * B) := Real.sqrt_le_sqrt h_P_sq
        _ = Real.sqrt A * Real.sqrt B := Real.sqrt_mul hA_nn B
    refine ⟨h_sum_eq, ?_⟩
    rw [h_sum_eq]
    calc
      A + 2 * P + B
        ≤ A + 2 * (Real.sqrt A * Real.sqrt B) + B := by linarith
      _ = (Real.sqrt A) ^ 2 + 2 * (Real.sqrt A * Real.sqrt B) + (Real.sqrt B) ^ 2 := by
          rw [Real.sq_sqrt hA_nn, Real.sq_sqrt hB_nn]
      _ = (Real.sqrt A + Real.sqrt B) ^ 2 := by ring
  · intro m u hm hu
    have hm_pos : 0 < m := by linarith
    have hm_ne : m ≠ 0 := ne_of_gt hm_pos
    have hm_sq_ge : (9 / 16 : ℝ) ≤ m ^ 2 := by nlinarith
    have h_m2_u_pos : 0 < m ^ 2 + u := by linarith
    have h_alg :
        (((m - 1 / 2) ^ 2 + u) * ((m + 1 / 2) ^ 2 + u)) / (m ^ 2 + u) ^ 2 -
            (1 - 1 / (4 * m ^ 2)) ^ 2 =
          u * ((8 * m ^ 2 - 1) * u + 24 * m ^ 4 - 2 * m ^ 2) /
            (16 * m ^ 4 * (m ^ 2 + u) ^ 2) := by
      field_simp [hm_ne, ne_of_gt h_m2_u_pos]
      ring
    have h_num_nn : 0 ≤ u * ((8 * m ^ 2 - 1) * u + 24 * m ^ 4 - 2 * m ^ 2) := by
      have h1 : 0 ≤ 8 * m ^ 2 - 1 := by linarith
      have h2 : 0 ≤ 24 * m ^ 4 - 2 * m ^ 2 := by nlinarith
      have h_assoc :
          (8 * m ^ 2 - 1) * u + 24 * m ^ 4 - 2 * m ^ 2 =
            (8 * m ^ 2 - 1) * u + (24 * m ^ 4 - 2 * m ^ 2) := by ring
      rw [h_assoc]
      exact mul_nonneg hu (add_nonneg (mul_nonneg h1 hu) h2)
    have h_den_pos : 0 < 16 * m ^ 4 * (m ^ 2 + u) ^ 2 := by positivity
    have h_frac_nn :
        0 ≤ u * ((8 * m ^ 2 - 1) * u + 24 * m ^ 4 - 2 * m ^ 2) /
          (16 * m ^ 4 * (m ^ 2 + u) ^ 2) :=
      div_nonneg h_num_nn (le_of_lt h_den_pos)
    exact ⟨h_alg, by linarith⟩

/-! ### Section 5: Second-Order Square-Pole Drift, Abel Reassembly, and Small-Divisor Contraction (`TASK-TC-060` §5) -/

/-- Explicit second-order `ζ(2s)` pole drift model
    `M_2(d; c_half) := 4 √d log d + c_half √d` (`M_2(0) := 0`). -/
noncomputable def squarePoleDriftM (c_half : ℝ) (d : ℕ) : ℝ :=
  if d = 0 then 0 else 4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ) + c_half * Real.sqrt (d : ℝ)

private theorem half_lt_log_two_and_one_lt_log_three_tc060_aux :
    (1 / 2 : ℝ) < Real.log 2 ∧ (1 : ℝ) < Real.log 3 := by
  have h_inv8 : (7 / 8 : ℝ) ≤ Real.exp (-(1 / 8 : ℝ)) := by
    have h := Real.add_one_le_exp (-(1 / 8 : ℝ))
    linarith
  have h_prod : Real.exp (1 / 8 : ℝ) * Real.exp (-(1 / 8 : ℝ)) = 1 := by
    rw [← Real.exp_add, add_neg_self, Real.exp_zero]
  have he8_le : Real.exp (1 / 8 : ℝ) ≤ 8 / 7 := by
    have hm := mul_le_mul_of_nonneg_left h_inv8 (le_of_lt (Real.exp_pos (1 / 8 : ℝ)))
    rw [h_prod] at hm
    linarith
  have he8_nn : 0 ≤ Real.exp (1 / 8 : ℝ) := le_of_lt (Real.exp_pos _)
  have he_half_eq : (Real.exp (1 / 8 : ℝ)) ^ 4 = Real.exp (1 / 2 : ℝ) := by
    have h4 :
        (Real.exp (1 / 8 : ℝ)) ^ 4 =
          Real.exp (1 / 8 : ℝ) * Real.exp (1 / 8 : ℝ) *
            Real.exp (1 / 8 : ℝ) * Real.exp (1 / 8 : ℝ) := by ring
    rw [h4, ← Real.exp_add, ← Real.exp_add, ← Real.exp_add]
    congr 1; ring
  have he_half_lt2 : Real.exp (1 / 2 : ℝ) < 2 := by
    have hp4 : (Real.exp (1 / 8 : ℝ)) ^ 4 ≤ (8 / 7 : ℝ) ^ 4 :=
      pow_le_pow_left he8_nn he8_le 4
    rw [he_half_eq] at hp4
    have hnum4 : ((8 / 7 : ℝ) ^ 4) < 2 := by norm_num
    exact lt_of_le_of_lt hp4 hnum4
  have he1_eq : (Real.exp (1 / 2 : ℝ)) ^ 2 = Real.exp 1 := by
    rw [sq, ← Real.exp_add]
    congr 1; ring
  have he_one_lt3 : Real.exp 1 < 3 := by
    have hp8 : (Real.exp (1 / 8 : ℝ)) ^ 8 ≤ (8 / 7 : ℝ) ^ 8 :=
      pow_le_pow_left he8_nn he8_le 8
    have h8_eq : (Real.exp (1 / 8 : ℝ)) ^ 8 = Real.exp 1 := by
      have h8 : (Real.exp (1 / 8 : ℝ)) ^ 8 = ((Real.exp (1 / 8 : ℝ)) ^ 4) ^ 2 := by ring
      rw [h8, he_half_eq, he1_eq]
    rw [h8_eq] at hp8
    have hnum8 : ((8 / 7 : ℝ) ^ 8) < 3 := by norm_num
    exact lt_of_le_of_lt hp8 hnum8
  have h1 : (1 / 2 : ℝ) < Real.log 2 := by
    have h := Real.log_lt_log (Real.exp_pos (1 / 2 : ℝ)) he_half_lt2
    rwa [Real.log_exp] at h
  have h2 : (1 : ℝ) < Real.log 3 := by
    have h := Real.log_lt_log (Real.exp_pos 1) he_one_lt3
    rwa [Real.log_exp] at h
  exact ⟨h1, h2⟩

private theorem windowNorm_finset_sum_le_tc060_aux {Y : ℝ} (hY : 0 < Y) (S : Finset ℕ)
    (g : ℕ → ℝ → ℝ)
    (hg : ∀ d ∈ S, ContinuousOn (g d) (Set.uIcc Y (RiemannScope.tau * Y))) :
    Real.sqrt (windowEnergyNormSq Y (fun X => ∑ d ∈ S, g d X)) ≤
      ∑ d ∈ S, Real.sqrt (windowEnergyNormSq Y (g d)) := by
  obtain ⟨_, h_cs_mink, _, _⟩ := smooth_increment_window_norm_and_small_scale_tail_tc059r
  induction' S using Finset.induction_on with a s ha_not ih
  · unfold windowEnergyNormSq windowPairing
    simp
  · have ha_cont : ContinuousOn (g a) (Set.uIcc Y (RiemannScope.tau * Y)) :=
      hg a (Finset.mem_insert_self a s)
    have hs_cont : ∀ d ∈ s, ContinuousOn (g d) (Set.uIcc Y (RiemannScope.tau * Y)) :=
      fun d hd => hg d (Finset.mem_insert_of_mem hd)
    let gs : ℝ → ℝ := fun X => ∑ d ∈ s, g d X
    have hgs_cont : ContinuousOn gs (Set.uIcc Y (RiemannScope.tau * Y)) :=
      continuousOn_finset_sum s hs_cont
    have h_ins_fn :
        (fun X => ∑ d ∈ insert a s, g d X) = fun X => g a X - (-gs X) := by
      ext X
      rw [Finset.sum_insert ha_not]
      dsimp [gs]
      ring
    have h_neg_norm : windowEnergyNormSq Y (fun X => -gs X) = windowEnergyNormSq Y gs := by
      unfold windowEnergyNormSq windowPairing
      congr 1; ext X; ring
    have h_mink := ((h_cs_mink hY).1 ha_cont hgs_cont.neg).2
    rw [h_ins_fn, Finset.sum_insert ha_not]
    rw [h_neg_norm] at h_mink
    exact le_trans h_mink (add_le_add_left (ih hs_cont) _)

/-- **Theorem 5 (`TASK-TC-060` §5, Second-Order Drift Split, Abel Summation Reassembly, `squarePoleDriftM` Difference Bound, Sub-Unit Scale Separation, and Small-Divisor Contraction)**:
    1. *General drift/oscillatory split of `smoothRemainderSumRsm`*;
    2. *Exact summation-by-parts reassembly of smooth drift (`T ≥ 1, M 0 = 0`)*;
    3. *Elementary properties and `12 * log(d + 1) / √d` increment bound for `squarePoleDriftM c_half` (`-2 ≤ c_half ≤ 0`), plus sub-unit separation at `Nat.floor Y` (`Y ≥ 2`)*;
    4. *Small-divisor `(log X)^(-2)`-weighted window norm bound (`Y ≥ 2`)*. -/
theorem second_order_drift_abel_and_small_divisor_contraction_tc060 :
    (∀ (T : ℕ) (c_lam : ℝ) (M : ℕ → ℝ) (X : ℝ),
      smoothRemainderSumRsm c_lam T X =
        (∑ d ∈ Finset.Icc 1 (T - 1), M d * scaledFiberSmoothStep T d X) +
          (∑ d ∈ Finset.Icc 1 (T - 1),
            (selbergCenteredRemainderInt c_lam d - M d) * scaledFiberSmoothStep T d X)) ∧
    (∀ {T : ℕ}, 1 ≤ T → ∀ (M : ℕ → ℝ), M 0 = 0 → ∀ X : ℝ,
      (∑ d ∈ Finset.Icc 1 (T - 1), M d * scaledFiberSmoothStep T d X) =
        (∑ d ∈ Finset.Icc 1 T, (M d - M (d - 1)) * scaledLiouvilleFiberG T d X) -
          M T * scaledLiouvilleFiberG T T X -
          (∑ d ∈ Finset.Icc 1 (T - 1), M d * scaledFiberCutoffJump T d X)) ∧
    (∀ {c_half : ℝ}, -2 ≤ c_half → c_half ≤ 0 →
      squarePoleDriftM c_half 0 = 0 ∧
        (∀ d : ℕ, 2 ≤ d → 0 < squarePoleDriftM c_half d) ∧
        (∀ d : ℕ, 1 ≤ d →
          |squarePoleDriftM c_half d - squarePoleDriftM c_half (d - 1)| ≤
            12 * Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt (d : ℝ)) ∧
        (∀ {Y : ℝ}, 2 ≤ Y → ∀ T : ℕ,
          Finset.Icc 1 T =
              Finset.Icc 1 (min T (Nat.floor Y)) ∪ Finset.Icc (Nat.floor Y + 1) T ∧
            Disjoint (Finset.Icc 1 (min T (Nat.floor Y))) (Finset.Icc (Nat.floor Y + 1) T) ∧
            (∀ d ∈ Finset.Icc 1 (min T (Nat.floor Y)), 1 ≤ Y / (d : ℝ)) ∧
            (∀ d ∈ Finset.Icc (Nat.floor Y + 1) T, Y / (d : ℝ) < 1))) ∧
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ (T D0 : ℕ) (w : ℕ → ℝ),
      Real.sqrt
          (windowEnergyNormSq Y
            (fun X => (∑ d ∈ Finset.Icc 1 D0, w d * scaledFiberSmoothStep T d X) /
              (Real.log X) ^ 2)) ≤
        (1 / (Real.log Y) ^ 2) *
          ∑ d ∈ Finset.Icc 1 D0,
            |w d| *
              ((1 / Real.sqrt (d : ℝ)) *
                  Real.sqrt
                    (actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ))
                      (T / d) (Y / (d : ℝ))) +
                (1 / Real.sqrt ((d + 1 : ℕ) : ℝ)) *
                  Real.sqrt
                    (actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ))
                      (T / d) (Y / ((d + 1 : ℕ) : ℝ))))) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro T c_lam M X
    unfold smoothRemainderSumRsm
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro d _; ring
  · intro T hT M hM0 X
    have h_abel :
        ∀ (g : ℕ → ℝ) (N : ℕ), 1 ≤ N →
          (∑ d ∈ Finset.Icc 1 N, (M d - M (d - 1)) * g d) =
            M N * g N + ∑ d ∈ Finset.Icc 1 (N - 1), M d * (g d - g (d + 1)) := by
      intro g N hN
      obtain ⟨m, rfl⟩ : ∃ m : ℕ, N = m + 1 := ⟨N - 1, by omega⟩
      induction' m with k ih
      · have h1 : Finset.Icc 1 1 = {1} := by decide
        simp [h1, hM0]
      · have hs1 : k + 1 + 1 - 1 = k + 1 := by omega
        have hs0 : k + 1 - 1 = k := by omega
        have h_ins_lhs : Finset.Icc 1 (k + 1 + 1) = insert (k + 2) (Finset.Icc 1 (k + 1)) := by
          ext d; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
        have h_not_lhs : (k + 2) ∉ Finset.Icc 1 (k + 1) := by simp
        have h_ins_rhs : Finset.Icc 1 (k + 1) = insert (k + 1) (Finset.Icc 1 k) := by
          ext d; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
        have h_not_rhs : (k + 1) ∉ Finset.Icc 1 k := by simp
        rw [h_ins_lhs, Finset.sum_insert h_not_lhs, ih (by omega), hs0, hs1,
          h_ins_rhs, Finset.sum_insert h_not_rhs]
        have hk2 : k + 1 + 1 = k + 2 := by omega
        rw [hk2]
        ring
    have h_step := h_abel (fun d => scaledLiouvilleFiberG T d X) T hT
    dsimp only at h_step
    have h_g_split :
        ∀ d : ℕ,
          scaledLiouvilleFiberG T d X - scaledLiouvilleFiberG T (d + 1) X =
            scaledFiberSmoothStep T d X + scaledFiberCutoffJump T d X := by
      intro d
      dsimp [scaledLiouvilleFiberG, scaledFiberSmoothStep, scaledFiberCutoffJump]
      ring
    have h_sum_split :
        (∑ d ∈ Finset.Icc 1 (T - 1),
            M d * (scaledLiouvilleFiberG T d X - scaledLiouvilleFiberG T (d + 1) X)) =
          (∑ d ∈ Finset.Icc 1 (T - 1), M d * scaledFiberSmoothStep T d X) +
            (∑ d ∈ Finset.Icc 1 (T - 1), M d * scaledFiberCutoffJump T d X) := by
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro d _
      rw [h_g_split d]
      ring
    linarith
  · intro c_half hc_lo hc_hi
    obtain ⟨h_log2, h_log3⟩ := half_lt_log_two_and_one_lt_log_three_tc060_aux
    have hc_abs : |c_half| ≤ 2 := abs_le.mpr ⟨hc_lo, by linarith⟩
    refine ⟨rfl, ?_, ?_, ?_⟩
    · intro d hd2
      have hd_ne : d ≠ 0 := by omega
      have hd_ge2 : (2 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd2
      have hlogd_ge : Real.log 2 ≤ Real.log (d : ℝ) :=
        Real.log_le_log (by norm_num) hd_ge2
      have h_coef_pos : 0 < 4 * Real.log (d : ℝ) + c_half := by linarith
      have h_sqrt_pos : 0 < Real.sqrt (d : ℝ) := Real.sqrt_pos.mpr (by linarith)
      unfold squarePoleDriftM
      rw [if_neg hd_ne]
      have h_eq :
          4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ) + c_half * Real.sqrt (d : ℝ) =
            (4 * Real.log (d : ℝ) + c_half) * Real.sqrt (d : ℝ) := by ring
      rw [h_eq]
      exact mul_pos h_coef_pos h_sqrt_pos
    · intro d hd1
      by_cases hd_eq1 : d = 1
      · subst hd_eq1
        have hM1 : squarePoleDriftM c_half 1 = c_half := by
          simp [squarePoleDriftM]
        have hM0 : squarePoleDriftM c_half 0 = 0 := rfl
        rw [show 1 - 1 = 0 by rfl, hM1, hM0, sub_zero]
        have h_rhs :
            12 * Real.log ((1 + 1 : ℕ) : ℝ) / Real.sqrt ((1 : ℕ) : ℝ) = 12 * Real.log 2 := by
          norm_num
        rw [h_rhs]
        linarith
      · have hd2 : 2 ≤ d := by omega
        have hd_ne : d ≠ 0 := by omega
        have hdm1_ne : d - 1 ≠ 0 := by omega
        let x : ℝ := (d : ℝ)
        let y : ℝ := ((d - 1 : ℕ) : ℝ)
        have hx_ge2 : 2 ≤ x := by dsimp [x]; exact_mod_cast hd2
        have hy_eq : y = x - 1 := by
          dsimp [x, y]; rw [Nat.cast_sub hd1, Nat.cast_one]
        have hx_pos : 0 < x := by linarith
        have hy_pos : 0 < y := by linarith
        have hsq_x_pos : 0 < Real.sqrt x := Real.sqrt_pos.mpr hx_pos
        have hsq_y_pos : 0 < Real.sqrt y := Real.sqrt_pos.mpr hy_pos
        have h_diff_expr :
            squarePoleDriftM c_half d - squarePoleDriftM c_half (d - 1) =
              4 * (Real.sqrt x - Real.sqrt y) * Real.log x +
                4 * Real.sqrt y * (Real.log x - Real.log y) +
                c_half * (Real.sqrt x - Real.sqrt y) := by
          unfold squarePoleDriftM
          rw [if_neg hd_ne, if_neg hdm1_ne]
          dsimp [x, y]
          ring
        have hsq_diff_nn : 0 ≤ Real.sqrt x - Real.sqrt y :=
          sub_nonneg.mpr (Real.sqrt_le_sqrt (by linarith))
        have hsq_diff_ub : Real.sqrt x - Real.sqrt y ≤ 1 / Real.sqrt x := by
          have h_conj :
              (Real.sqrt x - Real.sqrt y) * (Real.sqrt x + Real.sqrt y) = 1 := by
            calc
              (Real.sqrt x - Real.sqrt y) * (Real.sqrt x + Real.sqrt y)
                = (Real.sqrt x) ^ 2 - (Real.sqrt y) ^ 2 := by ring
              _ = x - y := by rw [Real.sq_sqrt (le_of_lt hx_pos), Real.sq_sqrt (le_of_lt hy_pos)]
              _ = 1 := by linarith
          have h_sum_ge : Real.sqrt x ≤ Real.sqrt x + Real.sqrt y := by linarith
          have h_div_eq : Real.sqrt x - Real.sqrt y = 1 / (Real.sqrt x + Real.sqrt y) := by
            field_simp [ne_of_gt (by linarith : 0 < Real.sqrt x + Real.sqrt y)]
            exact h_conj
          rw [h_div_eq]
          exact one_div_le_one_div_of_le hsq_x_pos h_sum_ge
        have hlogx_nn : 0 ≤ Real.log x := le_of_lt (Real.log_pos (by linarith))
        have hlog_diff_nn : 0 ≤ Real.log x - Real.log y :=
          sub_nonneg.mpr (Real.log_le_log hy_pos (by linarith))
        have hlog_diff_ub : Real.log x - Real.log y ≤ 1 / y := by
          rw [← Real.log_div (ne_of_gt hx_pos) (ne_of_gt hy_pos)]
          have h_div_eq : x / y = 1 / y + 1 := by
            have hx_eq : x = 1 + y := by linarith [hy_eq]
            rw [hx_eq, add_div, div_self (ne_of_gt hy_pos)]
          have h_exp : x / y ≤ Real.exp (1 / y) := by
            rw [h_div_eq]
            exact Real.add_one_le_exp (1 / y)
          have h_lg := Real.log_le_log (div_pos hx_pos hy_pos) h_exp
          rwa [Real.log_exp] at h_lg
        have h_inv_sqy : 1 / Real.sqrt y ≤ (3 / 2 : ℝ) / Real.sqrt x := by
          have h_x_le : x ≤ (9 / 4 : ℝ) * y := by linarith
          have h_sq_le : Real.sqrt x ≤ (3 / 2 : ℝ) * Real.sqrt y := by
            have h94 : (9 / 4 : ℝ) * y = ((3 / 2 : ℝ) * Real.sqrt y) ^ 2 := by
              rw [mul_pow, Real.sq_sqrt (le_of_lt hy_pos)]; ring
            rw [h94] at h_x_le
            exact le_trans (Real.sqrt_le_sqrt h_x_le) (le_of_eq (Real.sqrt_sq (by positivity)))
          rw [div_le_div_iff hsq_y_pos hsq_x_pos]
          linarith
        have h_log_d1_ge1 : 1 ≤ Real.log ((d + 1 : ℕ) : ℝ) := by
          have hd1_ge3 : (3 : ℝ) ≤ ((d + 1 : ℕ) : ℝ) := by exact_mod_cast (by omega : 3 ≤ d + 1)
          exact le_trans (le_of_lt h_log3) (Real.log_le_log (by norm_num) hd1_ge3)
        have h_logx_le_d1 : Real.log x ≤ Real.log ((d + 1 : ℕ) : ℝ) := by
          apply Real.log_le_log hx_pos
          dsimp [x]
          exact_mod_cast (Nat.le_succ d)
        have h_t1 :
            4 * (Real.sqrt x - Real.sqrt y) * Real.log x ≤
              4 * Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt x := by
          calc
            4 * (Real.sqrt x - Real.sqrt y) * Real.log x
              ≤ 4 * (1 / Real.sqrt x) * Real.log ((d + 1 : ℕ) : ℝ) := by
                have hm1 := mul_le_mul hsq_diff_ub h_logx_le_d1 hlogx_nn (by positivity)
                linarith
            _ = 4 * Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt x := by ring
        have h_t2 :
            4 * Real.sqrt y * (Real.log x - Real.log y) ≤
              6 * Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt x := by
          have h_sqy_div : Real.sqrt y * (1 / y) = 1 / Real.sqrt y := by
            have hy_sq : y = (Real.sqrt y) ^ 2 := (Real.sq_sqrt (le_of_lt hy_pos)).symm
            conv_lhs => rw [hy_sq]
            field_simp [ne_of_gt hsq_y_pos]
          calc
            4 * Real.sqrt y * (Real.log x - Real.log y)
              ≤ 4 * (Real.sqrt y * (1 / y)) := by
                have hm := mul_le_mul_of_nonneg_left hlog_diff_ub (le_of_lt hsq_y_pos)
                linarith
            _ = 4 * (1 / Real.sqrt y) := by rw [h_sqy_div]
            _ ≤ 4 * ((3 / 2 : ℝ) / Real.sqrt x) := by linarith [h_inv_sqy]
            _ = 6 * (1 / Real.sqrt x) := by ring
            _ ≤ 6 * (Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt x) := by
                have h_le : 1 / Real.sqrt x ≤ Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt x :=
                  div_le_div_of_nonneg_right h_log_d1_ge1 (le_of_lt hsq_x_pos)
                linarith
            _ = 6 * Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt x := by ring
        have h_t3 :
            |c_half * (Real.sqrt x - Real.sqrt y)| ≤
              2 * Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt x := by
          rw [abs_mul, abs_of_nonneg hsq_diff_nn]
          calc
            |c_half| * (Real.sqrt x - Real.sqrt y)
              ≤ 2 * (1 / Real.sqrt x) :=
                mul_le_mul hc_abs hsq_diff_ub hsq_diff_nn (by norm_num)
            _ ≤ 2 * (Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt x) := by
                have h_le : 1 / Real.sqrt x ≤ Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt x :=
                  div_le_div_of_nonneg_right h_log_d1_ge1 (le_of_lt hsq_x_pos)
                linarith
            _ = 2 * Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt x := by ring
        have h_tri :
            |squarePoleDriftM c_half d - squarePoleDriftM c_half (d - 1)| ≤
              |4 * (Real.sqrt x - Real.sqrt y) * Real.log x +
                  4 * Real.sqrt y * (Real.log x - Real.log y)| +
                |c_half * (Real.sqrt x - Real.sqrt y)| := by
          rw [h_diff_expr]
          exact abs_add _ _
        have h_pos12 :
            0 ≤ 4 * (Real.sqrt x - Real.sqrt y) * Real.log x +
              4 * Real.sqrt y * (Real.log x - Real.log y) :=
          add_nonneg (mul_nonneg (by linarith) hlogx_nn) (mul_nonneg (by positivity) hlog_diff_nn)
        rw [abs_of_nonneg h_pos12] at h_tri
        dsimp [x] at h_tri h_t1 h_t2 h_t3
        have h_sum_12 :
            4 * Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt (d : ℝ) +
                6 * Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt (d : ℝ) +
                2 * Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt (d : ℝ) =
              12 * Real.log ((d + 1 : ℕ) : ℝ) / Real.sqrt (d : ℝ) := by ring
        linarith
    · intro Y hY2 T
      have hY_nn : 0 ≤ Y := by linarith
      refine ⟨?_, ?_, ?_, ?_⟩
      · ext d
        simp only [Finset.mem_Icc, Finset.mem_union]
        omega
      · rw [Finset.disjoint_left]
        intro d h1 h2
        simp only [Finset.mem_Icc] at h1 h2
        omega
      · intro d hd
        rw [Finset.mem_Icc] at hd
        have hd_pos : (0 : ℝ) < (d : ℝ) := Nat.cast_pos.mpr hd.1
        have hd_le_fl : d ≤ Nat.floor Y := le_trans hd.2 (min_le_right T _)
        have hd_le_Y : (d : ℝ) ≤ Y := le_trans (by exact_mod_cast hd_le_fl) (Nat.floor_le hY_nn)
        exact (one_le_div hd_pos).mpr hd_le_Y
      · intro d hd
        rw [Finset.mem_Icc] at hd
        have hd_pos : (0 : ℝ) < (d : ℝ) := Nat.cast_pos.mpr (by omega)
        have hY_lt : Y < (Nat.floor Y : ℝ) + 1 := Nat.lt_floor_add_one Y
        have hfl_le_d : (Nat.floor Y : ℝ) + 1 ≤ (d : ℝ) := by exact_mod_cast hd.1
        exact (div_lt_one hd_pos).mpr (lt_of_lt_of_le hY_lt hfl_le_d)
  · intro Y hY2 T D0 w
    have hY_pos : 0 < Y := by linarith
    have htau : 1 < RiemannScope.tau := tau_gt_one_tc060_aux
    have hlogY_pos : 0 < Real.log Y := Real.log_pos (by linarith)
    let f : ℝ → ℝ := fun X => ∑ d ∈ Finset.Icc 1 D0, w d * scaledFiberSmoothStep T d X
    have hf_cont : ContinuousOn f (Set.uIcc Y (RiemannScope.tau * Y)) := by
      dsimp [f]
      refine continuousOn_finset_sum _ (fun d _ => continuousOn_const.mul ?_)
      exact continuousOn_scaledFiberSmoothStep_param_tc060_aux hY_pos htau T d
    obtain ⟨_, _, _, h_weighted⟩ := signed_gram_kernel_and_log_weighted_quadratic_form_tc060
    have h_sand := ((h_weighted hY2 htau).2.2 hf_cont).2
    have h_param_eq :
        ∀ g : ℝ → ℝ, paramWindowNormSq Y RiemannScope.tau g = windowEnergyNormSq Y g :=
      fun _ => rfl
    rw [h_param_eq, h_param_eq] at h_sand
    have h_sqrt_sand :
        Real.sqrt (windowEnergyNormSq Y (fun X => f X / (Real.log X) ^ 2)) ≤
          (1 / (Real.log Y) ^ 2) * Real.sqrt (windowEnergyNormSq Y f) := by
      calc
        Real.sqrt (windowEnergyNormSq Y (fun X => f X / (Real.log X) ^ 2))
          ≤ Real.sqrt ((1 / (Real.log Y) ^ 4) * windowEnergyNormSq Y f) :=
            Real.sqrt_le_sqrt h_sand
        _ = Real.sqrt ((1 / (Real.log Y) ^ 2) ^ 2) * Real.sqrt (windowEnergyNormSq Y f) := by
            rw [Real.sqrt_mul (by positivity)]
            congr 1; congr 1; ring
        _ = (1 / (Real.log Y) ^ 2) * Real.sqrt (windowEnergyNormSq Y f) := by
            rw [Real.sqrt_sq (by positivity)]
    have h_mink_sum :=
      windowNorm_finset_sum_le_tc060_aux hY_pos (Finset.Icc 1 D0)
        (fun d X => w d * scaledFiberSmoothStep T d X)
        (fun d _ => continuousOn_const.mul
          (continuousOn_scaledFiberSmoothStep_param_tc060_aux hY_pos htau T d))
    obtain ⟨_, _, h_sm_bound, _⟩ := smooth_increment_window_norm_and_small_scale_tail_tc059r
    have h_each :
        ∀ d ∈ Finset.Icc 1 D0,
          Real.sqrt (windowEnergyNormSq Y (fun X => w d * scaledFiberSmoothStep T d X)) ≤
            |w d| *
              ((1 / Real.sqrt (d : ℝ)) *
                  Real.sqrt
                    (actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ))
                      (T / d) (Y / (d : ℝ))) +
                (1 / Real.sqrt ((d + 1 : ℕ) : ℝ)) *
                  Real.sqrt
                    (actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ))
                      (T / d) (Y / ((d + 1 : ℕ) : ℝ)))) := by
      intro d hd
      rw [Finset.mem_Icc] at hd
      have h_scale_w :
          windowEnergyNormSq Y (fun X => w d * scaledFiberSmoothStep T d X) =
            (w d) ^ 2 * windowEnergyNormSq Y (scaledFiberSmoothStep T d) := by
        unfold windowEnergyNormSq windowPairing
        have h_pt :
            (fun X =>
                (w d * scaledFiberSmoothStep T d X) *
                  (w d * scaledFiberSmoothStep T d X) / X) =
              fun X =>
                (w d) ^ 2 *
                  (scaledFiberSmoothStep T d X * scaledFiberSmoothStep T d X / X) := by
          ext X; ring
        rw [h_pt, intervalIntegral.integral_const_mul]
      rw [h_scale_w, Real.sqrt_mul (sq_nonneg _), Real.sqrt_sq_eq_abs]
      exact mul_le_mul_of_nonneg_left (h_sm_bound hY_pos T d hd.1) (abs_nonneg _)
    have h_f_le :
        Real.sqrt (windowEnergyNormSq Y f) ≤
          ∑ d ∈ Finset.Icc 1 D0,
            |w d| *
              ((1 / Real.sqrt (d : ℝ)) *
                  Real.sqrt
                    (actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ))
                      (T / d) (Y / (d : ℝ))) +
                (1 / Real.sqrt ((d + 1 : ℕ) : ℝ)) *
                  Real.sqrt
                    (actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ))
                      (T / d) (Y / ((d + 1 : ℕ) : ℝ)))) :=
      le_trans h_mink_sum (Finset.sum_le_sum h_each)
    exact le_trans h_sqrt_sand (mul_le_mul_of_nonneg_left h_f_le (by positivity))

/-! ### Section 6: Complete Reconstruction Decomposition and `R`-Independent Contraction Transfer (`TASK-TC-060` §6) -/

/-- Known unconditionally controlled compensated `D_{2,T}` component combining `c_lam Q_{square,T}`,
    total endpoint `R_2^{int}(T) φ_T`, cutoff jumps `R_{2,T}^{jump}`, second-order drift `M_2`,
    and small-divisor `d ≤ min D0 (T - 1)` oscillatory smooth terms. -/
noncomputable def knownCompensatedD2Part (c_lam c_half : ℝ) (T D0 : ℕ) (X : ℝ) : ℝ :=
  (c_lam * finiteQSquare T X +
    selbergCenteredRemainderInt c_lam T * gaussianTermPhi T X +
    jumpRemainderSumRjump c_lam T X +
    (∑ d ∈ Finset.Icc 1 (T - 1), squarePoleDriftM c_half d * scaledFiberSmoothStep T d X) +
    (∑ d ∈ Finset.Icc 1 (min D0 (T - 1)),
      (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
        scaledFiberSmoothStep T d X)) / (Real.log X) ^ 2

/-- Remaining `OPEN` oscillatory core plus second logarithmic shift component
    `(∑_{min(D0, T - 1) < d ≤ T - 1} (R_2^{int}(d) - M_2(d)) Δ_d^{sm}(X) - Q_T^{[2]}(X)) / (log X)^2`. -/
noncomputable def openCoreOscShiftD2Part (c_lam c_half : ℝ) (T D0 : ℕ) (X : ℝ) : ℝ :=
  ((∑ d ∈ Finset.Icc (min D0 (T - 1) + 1) (T - 1),
      (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
        scaledFiberSmoothStep T d X) -
    finiteQShifted (fun n => (liouvilleLambda n : ℝ)) 2 T X) / (Real.log X) ^ 2

private theorem rpow_neg_antitone_tc060_aux {Y_star Y α : ℝ} (hY_star : 1 ≤ Y_star)
    (hYY : Y_star ≤ Y) (hα : 0 ≤ α) :
    Y ^ (-α) ≤ Y_star ^ (-α) := by
  have hY_star_pos : 0 < Y_star := lt_of_lt_of_le zero_lt_one hY_star
  have hY_nn : 0 ≤ Y := le_of_lt (lt_of_lt_of_le hY_star_pos hYY)
  have h_pos_pow : 0 < Y_star ^ α := Real.rpow_pos_of_pos hY_star_pos α
  have h_le_pow : Y_star ^ α ≤ Y ^ α := Real.rpow_le_rpow (le_of_lt hY_star_pos) hYY hα
  rw [Real.rpow_neg hY_nn, Real.rpow_neg (le_of_lt hY_star_pos)]
  exact inv_le_inv_of_le h_pos_pow h_le_pow

/-- **Theorem 6 (`TASK-TC-060` §6, Lossless Complete Reconstruction Split, `(8, 4, 4)` Window Energy Inequality, and `R`-Independent Finite-Horizon Contraction Transfer)**:
    1. *Exact lossless decomposition (`T ≥ 1, D0 : ℕ, X > 0, log X ≠ 0`)*:
       `compensatedSelbergResidualD2 c_lam T X = knownCompensatedD2Part c_lam c_half T D0 X + openCoreOscShiftD2Part c_lam c_half T D0 X`
       and `finiteQLambda T X = 2 * normalizedPrimePowerTermP T X - knownCompensatedD2Part c_lam c_half T D0 X - openCoreOscShiftD2Part c_lam c_half T D0 X`;
    2. *Complete `(8, 4, 4)` window quadratic energy inequality (`Y ≥ 2, T ≥ 1, D0 : ℕ`)*:
       `actualWindowEnergyE λ T Y ≤ 8 * ‖P_T‖_Y^2 + 4 * ‖knownCompensatedD2Part‖_Y^2 + 4 * ‖openCoreOscShiftD2Part‖_Y^2`;
    3. *Explicit `R`-independent threshold `Y_star` and `(1/4 + 1/4 + 1/4 = 3/4)` finite-horizon feedback contraction*:
       Exhibits `Y_star ≥ max Y_diag (Real.exp 1)` independent of `R` where both the diagonal feedback
       `8 * (2 * zeta2_eps / (log Y)^2) ≤ 1 / 4` and the known drift feedback `4 * (B_drift / (log Y)^κ_d) ≤ 1 / 4`
       hold simultaneously for all `Y ≥ Y_star`, and proves that open-core control with coefficient `1 / 4`
       contracts `normalizedScaleSupremum E ε R ≤ max (normalizedScaleSupremum E ε Y_star) (4 * K_const)`
       across all `R ≥ Y_star` (and all `R ≥ 1`), yielding `E Y ≤ C_tot * Y^ε` for all `Y ≥ 1`. -/
theorem complete_reconstruction_drift_contraction_transfer_tc060 :
    (∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ) {X : ℝ}, 0 < X → Real.log X ≠ 0 →
      compensatedSelbergResidualD2 c_lam T X =
          knownCompensatedD2Part c_lam c_half T D0 X +
            openCoreOscShiftD2Part c_lam c_half T D0 X ∧
        finiteQLambda T X =
          2 * normalizedPrimePowerTermP T X -
            knownCompensatedD2Part c_lam c_half T D0 X -
            openCoreOscShiftD2Part c_lam c_half T D0 X) ∧
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
      actualWindowEnergyE (fun n => (liouvilleLambda n : ℝ)) T Y ≤
        8 * windowEnergyNormSq Y (normalizedPrimePowerTermP T) +
          4 * windowEnergyNormSq Y (knownCompensatedD2Part c_lam c_half T D0) +
          4 * windowEnergyNormSq Y (openCoreOscShiftD2Part c_lam c_half T D0)) ∧
    (∀ {E D_tilde K_known R_open : ℝ → ℝ}
        {M_lin ε zeta2_eps C_cut Y_diag η A_k B_drift κ_d A_open : ℝ},
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
      0 < η → η < ε → 0 ≤ A_k → 0 ≤ B_drift → 0 < κ_d → 0 ≤ A_open →
      (∀ R Y : ℝ, Y_diag ≤ Y → Y ≤ R →
        K_known Y ≤
          A_k * Y ^ η +
            (B_drift / (Real.log Y) ^ κ_d) * normalizedScaleSupremum E ε R * Y ^ ε) →
      (∀ Y : ℝ, Y_diag ≤ Y → E Y ≤ 8 * D_tilde Y + 4 * K_known Y + R_open Y) →
      let Y_star :=
        max Y_diag
          (max (Real.exp (Real.sqrt (64 * zeta2_eps + 1)))
            (Real.exp ((16 * B_drift + 1) ^ (1 / κ_d))))
      let K_const := (4 * A_k + A_open) * Y_star ^ (η - ε) + 8 * C_cut * Y_star ^ (-ε)
      let C_tot := max (normalizedScaleSupremum E ε Y_star) (4 * K_const)
      max Y_diag (Real.exp 1) ≤ Y_star ∧
        (∀ Y : ℝ, Y_star ≤ Y →
          8 * (2 * zeta2_eps / (Real.log Y) ^ 2) ≤ 1 / 4 ∧
            4 * (B_drift / (Real.log Y) ^ κ_d) ≤ 1 / 4) ∧
        ((∀ R Y : ℝ, Y_star ≤ Y → Y ≤ R →
            R_open Y ≤
              A_open * Y ^ η + (1 / 4 : ℝ) * normalizedScaleSupremum E ε R * Y ^ ε) →
          0 ≤ K_const ∧
            0 ≤ C_tot ∧
            (∀ R : ℝ, Y_star ≤ R → normalizedScaleSupremum E ε R ≤ C_tot) ∧
            (∀ Y : ℝ, 1 ≤ Y → E Y ≤ C_tot * Y ^ ε))) := by
  have h_decomp_pt :
      ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ) {X : ℝ}, 0 < X → Real.log X ≠ 0 →
        compensatedSelbergResidualD2 c_lam T X =
            knownCompensatedD2Part c_lam c_half T D0 X +
              openCoreOscShiftD2Part c_lam c_half T D0 X ∧
          finiteQLambda T X =
            2 * normalizedPrimePowerTermP T X -
              knownCompensatedD2Part c_lam c_half T D0 X -
              openCoreOscShiftD2Part c_lam c_half T D0 X := by
    intro T hT D0 c_lam c_half X hX hlog_ne
    obtain ⟨_, _, _, hD2_id, _⟩ := noncircular_reassembly_and_basis_stratification_tc060 c_lam
    obtain ⟨h_drift_split, _, _, _⟩ := second_order_drift_abel_and_small_divisor_contraction_tc060
    obtain ⟨_, _, _, h_shift_elim⟩ :=
      compensated_selberg_summation_by_parts_and_shift_elimination_tc058 T c_lam
    have h_icc_union :
        Finset.Icc 1 (T - 1) =
          Finset.Icc 1 (min D0 (T - 1)) ∪ Finset.Icc (min D0 (T - 1) + 1) (T - 1) := by
      ext d; simp only [Finset.mem_Icc, Finset.mem_union]; omega
    have h_icc_disj :
        Disjoint (Finset.Icc 1 (min D0 (T - 1))) (Finset.Icc (min D0 (T - 1) + 1) (T - 1)) := by
      rw [Finset.disjoint_left]
      intro d h1 h2; simp only [Finset.mem_Icc] at h1 h2; omega
    have h_osc_union :
        (∑ d ∈ Finset.Icc 1 (T - 1),
            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
              scaledFiberSmoothStep T d X) =
          (∑ d ∈ Finset.Icc 1 (min D0 (T - 1)),
              (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                scaledFiberSmoothStep T d X) +
            (∑ d ∈ Finset.Icc (min D0 (T - 1) + 1) (T - 1),
              (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                scaledFiberSmoothStep T d X) := by
      conv_lhs => rw [h_icc_union]
      exact Finset.sum_union h_icc_disj
    have hRsm_eq := h_drift_split T c_lam (squarePoleDriftM c_half) X
    rw [h_osc_union] at hRsm_eq
    have hD2 := (hD2_id T hT X hX hlog_ne).1
    have h_split_D2 :
        compensatedSelbergResidualD2 c_lam T X =
          knownCompensatedD2Part c_lam c_half T D0 X +
            openCoreOscShiftD2Part c_lam c_half T D0 X := by
      rw [hD2, hRsm_eq]
      unfold knownCompensatedD2Part openCoreOscShiftD2Part
      ring
    have hQ := (h_shift_elim X hX hlog_ne).2.2
    refine ⟨h_split_D2, ?_⟩
    rw [hQ, h_split_D2]
    ring
  refine ⟨h_decomp_pt, ?_, ?_⟩
  · intro Y hY2 T hT D0 c_lam c_half
    have hY_pos : 0 < Y := by linarith
    have htau : 1 < RiemannScope.tau := tau_gt_one_tc060_aux
    obtain ⟨hle, hpos⟩ := uIcc_param_pos_tc060_aux hY_pos htau
    have h_log_pos : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), 0 < Real.log X := by
      intro X hX
      rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX
      exact Real.log_pos (by linarith)
    have h_log_ne : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), Real.log X ≠ 0 :=
      fun X hX => ne_of_gt (h_log_pos X hX)
    have h_log_sq_ne : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), (Real.log X) ^ 2 ≠ 0 :=
      fun X hX => pow_ne_zero 2 (h_log_ne X hX)
    have h_log_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
      ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hpos X hX))
    have h_Q_scaled_cont :
        ∀ (L : ℕ) (m : ℝ), 0 ≤ m →
          ContinuousOn (fun X => finiteQLambda L (X / m)) (Set.uIcc Y (RiemannScope.tau * Y)) := by
      intro L m hm_nn
      have h_fn :
          (fun X => finiteQLambda L (X / m)) =
            fun X => ∑ q ∈ Finset.Icc 1 L, (liouvilleLambda q : ℝ) * gaussianTermPhi q (X / m) := by
        ext X; dsimp [finiteQLambda, gaussianTermPhi]
        rw [Finset.mul_sum]; apply Finset.sum_congr rfl; intro q _; ring
      rw [h_fn]
      refine continuousOn_finset_sum _ (fun q _ => continuousOn_const.mul ?_)
      exact (continuousOn_gaussianTermPhi_Ici_tc060_aux q).comp (continuousOn_id.div_const m)
        (fun X hX => div_nonneg (le_of_lt (hpos X hX)) hm_nn)
    have hP_cont :
        ContinuousOn (normalizedPrimePowerTermP T) (Set.uIcc Y (RiemannScope.tau * Y)) := by
      unfold normalizedPrimePowerTermP liouvillePrimePowerTerm
      refine (continuousOn_finset_sum _ (fun pk _ => ?_)).div h_log_cont h_log_ne
      exact continuousOn_const.mul (h_Q_scaled_cont _ _ (Nat.cast_nonneg _))
    have hQsq_cont :
        ContinuousOn (finiteQSquare T) (Set.uIcc Y (RiemannScope.tau * Y)) := by
      unfold finiteQSquare
      exact continuousOn_finset_sum _
        (fun r _ => continuousOn_gaussianTermPhi_param_tc060_aux hY_pos htau (r ^ 2))
    have hRjump_cont :
        ContinuousOn (jumpRemainderSumRjump c_lam T) (Set.uIcc Y (RiemannScope.tau * Y)) := by
      unfold jumpRemainderSumRjump scaledFiberCutoffJump
      refine continuousOn_finset_sum _ (fun d _ => continuousOn_const.mul
        (continuousOn_const.mul ((h_Q_scaled_cont _ _ (Nat.cast_nonneg _)).sub
          (h_Q_scaled_cont _ _ (Nat.cast_nonneg _)))))
    have hQsh2_cont :
        ContinuousOn (finiteQShifted (fun n => (liouvilleLambda n : ℝ)) 2 T)
          (Set.uIcc Y (RiemannScope.tau * Y)) := by
      unfold finiteQShifted
      refine continuousOn_finset_sum _ (fun n hn => ?_)
      rw [Finset.mem_Icc] at hn
      have hn_pos : (0 : ℝ) < (n : ℝ) := Nat.cast_pos.mpr hn.1
      have h_div_pos : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), X / (n : ℝ) ≠ 0 :=
        fun X hX => ne_of_gt (div_pos (hpos X hX) hn_pos)
      exact (continuousOn_const.mul
        ((ContinuousOn.log (continuousOn_id.div_const (n : ℝ)) h_div_pos).pow 2)).mul
        (continuousOn_gaussianTermPhi_param_tc060_aux hY_pos htau n)
    have hK_cont :
        ContinuousOn (knownCompensatedD2Part c_lam c_half T D0)
          (Set.uIcc Y (RiemannScope.tau * Y)) := by
      unfold knownCompensatedD2Part
      refine (((((continuousOn_const.mul hQsq_cont).add
          (continuousOn_const.mul (continuousOn_gaussianTermPhi_param_tc060_aux hY_pos htau T))).add
          hRjump_cont).add
          (continuousOn_finset_sum _ (fun d _ => continuousOn_const.mul
            (continuousOn_scaledFiberSmoothStep_param_tc060_aux hY_pos htau T d)))).add
          (continuousOn_finset_sum _ (fun d _ => continuousOn_const.mul
            (continuousOn_scaledFiberSmoothStep_param_tc060_aux hY_pos htau T d)))).div
        (h_log_cont.pow 2) h_log_sq_ne
    have hO_cont :
        ContinuousOn (openCoreOscShiftD2Part c_lam c_half T D0)
          (Set.uIcc Y (RiemannScope.tau * Y)) := by
      unfold openCoreOscShiftD2Part
      refine ((continuousOn_finset_sum _ (fun d _ => continuousOn_const.mul
        (continuousOn_scaledFiberSmoothStep_param_tc060_aux hY_pos htau T d))).sub
        hQsh2_cont).div (h_log_cont.pow 2) h_log_sq_ne
    have hQgen_cont :
        ContinuousOn (finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) T)
          (Set.uIcc Y (RiemannScope.tau * Y)) := by
      unfold finiteQGeneral
      exact continuousOn_finset_sum _ (fun n _ => continuousOn_const.mul
        (continuousOn_gaussianTermPhi_param_tc060_aux hY_pos htau n))
    have h_int_Q := intervalIntegrable_param_tc060_aux hY_pos htau hQgen_cont hQgen_cont
    have h_int_P := intervalIntegrable_param_tc060_aux hY_pos htau hP_cont hP_cont
    have h_int_K := intervalIntegrable_param_tc060_aux hY_pos htau hK_cont hK_cont
    have h_int_O := intervalIntegrable_param_tc060_aux hY_pos htau hO_cont hO_cont
    unfold actualWindowEnergyE windowEnergyNormSq windowPairing
    rw [← intervalIntegral.integral_const_mul, ← intervalIntegral.integral_const_mul,
      ← intervalIntegral.integral_const_mul,
      ← intervalIntegral.integral_add (h_int_P.const_mul 8) (h_int_K.const_mul 4),
      ← intervalIntegral.integral_add ((h_int_P.const_mul 8).add (h_int_K.const_mul 4))
        (h_int_O.const_mul 4)]
    apply intervalIntegral.integral_mono_on hle h_int_Q
      (((h_int_P.const_mul 8).add (h_int_K.const_mul 4)).add (h_int_O.const_mul 4))
    intro X hX
    have hX_uIcc : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
    have hX_pos : 0 < X := hpos X hX_uIcc
    have hQ_eq_gen :
        finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) T X = finiteQLambda T X := by
      unfold finiteQGeneral finiteQLambda gaussianTermPhi
      rw [Finset.mul_sum]; apply Finset.sum_congr rfl; intro n _; ring
    have hQ_split := (h_decomp_pt hT D0 c_lam c_half hX_pos (h_log_ne X hX_uIcc)).2
    let p := normalizedPrimePowerTermP T X
    let k := knownCompensatedD2Part c_lam c_half T D0 X
    let o := openCoreOscShiftD2Part c_lam c_half T D0 X
    have h_quad : (2 * p - k - o) ^ 2 ≤ 8 * p ^ 2 + 4 * k ^ 2 + 4 * o ^ 2 := by
      nlinarith [sq_nonneg (2 * p + k + o), sq_nonneg (k - o)]
    calc
      finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) T X *
          finiteQGeneral (fun n => (liouvilleLambda n : ℝ)) T X / X
        = (2 * p - k - o) ^ 2 / X := by
            rw [hQ_eq_gen, hQ_split]; dsimp [p, k, o]; ring
      _ ≤ (8 * p ^ 2 + 4 * k ^ 2 + 4 * o ^ 2) / X :=
          div_le_div_of_nonneg_right h_quad (le_of_lt hX_pos)
      _ = 8 * (p * p / X) + 4 * (k * k / X) + 4 * (o * o / X) := by ring
  · intro E D_tilde K_known R_open M_lin ε zeta2_eps C_cut Y_diag η A_k B_drift κ_d A_open
      hE_nn hM_nn hE_lin hε_pos hzeta_nn hCc_nn hYdiag_ge_e h_zeta_mass hD_route_d
      _ hη_lt_ε hAk_nn hBdrift_nn hκd_pos hAopen_nn hK_known hE_decomp
    dsimp only
    let Y_star :=
      max Y_diag
        (max (Real.exp (Real.sqrt (64 * zeta2_eps + 1)))
          (Real.exp ((16 * B_drift + 1) ^ (1 / κ_d))))
    let K_const := (4 * A_k + A_open) * Y_star ^ (η - ε) + 8 * C_cut * Y_star ^ (-ε)
    let C_tot := max (normalizedScaleSupremum E ε Y_star) (4 * K_const)
    have he_ge1 : (1 : ℝ) ≤ Real.exp 1 :=
      le_trans (by norm_num : (1 : ℝ) ≤ 1 + 1) (Real.add_one_le_exp 1)
    have hYstar_ge_diag : Y_diag ≤ Y_star := le_max_left _ _
    have hYstar_ge_e : Real.exp 1 ≤ Y_star := le_trans hYdiag_ge_e hYstar_ge_diag
    have hYstar_ge1 : 1 ≤ Y_star := le_trans he_ge1 hYstar_ge_e
    have h_max_le_Ystar : max Y_diag (Real.exp 1) ≤ Y_star :=
      max_le hYstar_ge_diag hYstar_ge_e
    have h_small_fb :
        ∀ Y : ℝ, Y_star ≤ Y →
          8 * (2 * zeta2_eps / (Real.log Y) ^ 2) ≤ 1 / 4 ∧
            4 * (B_drift / (Real.log Y) ^ κ_d) ≤ 1 / 4 := by
      intro Y hYYs
      have hY_ge_e : Real.exp 1 ≤ Y := le_trans hYstar_ge_e hYYs
      have hlogY_ge1 : 1 ≤ Real.log Y := by
        have h := Real.log_le_log (Real.exp_pos 1) hY_ge_e
        rwa [Real.log_exp] at h
      have hlogY_pos : 0 < Real.log Y := lt_of_lt_of_le zero_lt_one hlogY_ge1
      have h_ge_z : Real.exp (Real.sqrt (64 * zeta2_eps + 1)) ≤ Y :=
        le_trans (le_trans (le_max_left _ _) (le_max_right _ _)) hYYs
      have h_ge_d : Real.exp ((16 * B_drift + 1) ^ (1 / κ_d)) ≤ Y :=
        le_trans (le_trans (le_max_right _ _) (le_max_right _ _)) hYYs
      have h_log_ge_sqrt : Real.sqrt (64 * zeta2_eps + 1) ≤ Real.log Y := by
        have h := Real.log_le_log (Real.exp_pos _) h_ge_z
        rwa [Real.log_exp] at h
      have h_log_sq_ge : 64 * zeta2_eps + 1 ≤ (Real.log Y) ^ 2 := by
        have h1 := pow_le_pow_left (Real.sqrt_nonneg _) h_log_ge_sqrt 2
        rwa [Real.sq_sqrt (by positivity)] at h1
      have h_fb1 : 8 * (2 * zeta2_eps / (Real.log Y) ^ 2) ≤ 1 / 4 := by
        have h_eq : 8 * (2 * zeta2_eps / (Real.log Y) ^ 2) = 16 * zeta2_eps / (Real.log Y) ^ 2 := by
          ring
        rw [h_eq, div_le_iff (sq_pos_of_pos hlogY_pos)]
        linarith
      have h_base_pos : 0 < 16 * B_drift + 1 := by positivity
      have h_log_ge_pow : (16 * B_drift + 1) ^ (1 / κ_d) ≤ Real.log Y := by
        have h := Real.log_le_log (Real.exp_pos _) h_ge_d
        rwa [Real.log_exp] at h
      have h_log_kd_ge : 16 * B_drift + 1 ≤ (Real.log Y) ^ κ_d := by
        have h1 := Real.rpow_le_rpow (by positivity) h_log_ge_pow (le_of_lt hκd_pos)
        rwa [← Real.rpow_mul (le_of_lt h_base_pos), one_div_mul_cancel (ne_of_gt hκd_pos),
          Real.rpow_one] at h1
      have h_fb2 : 4 * (B_drift / (Real.log Y) ^ κ_d) ≤ 1 / 4 := by
        have h_eq : 4 * (B_drift / (Real.log Y) ^ κ_d) = 4 * B_drift / (Real.log Y) ^ κ_d := by
          ring
        rw [h_eq, div_le_iff (Real.rpow_pos_of_pos hlogY_pos κ_d)]
        linarith
      exact ⟨h_fb1, h_fb2⟩
    refine ⟨h_max_le_Ystar, h_small_fb, ?_⟩
    intro hR_open
    obtain ⟨hG_props, ⟨_, _, hD_hor⟩, _, _⟩ :=
      repaired_weighted_diagonal_closure_and_actual_observable_tc059r
    have hYstar_pos : 0 < Y_star := lt_of_lt_of_le zero_lt_one hYstar_ge1
    have hKconst_nn : 0 ≤ K_const := by
      dsimp [K_const]
      exact add_nonneg
        (mul_nonneg (by positivity) (Real.rpow_nonneg (le_of_lt hYstar_pos) _))
        (mul_nonneg (by positivity) (Real.rpow_nonneg (le_of_lt hYstar_pos) _))
    obtain ⟨hYs_fin, hG_mono⟩ := hG_props hE_nn hM_nn hE_lin (le_of_lt hε_pos)
    have hGYs_nn : 0 ≤ normalizedScaleSupremum E ε Y_star := (hYs_fin hYstar_ge1).2.2.1
    have hCtot_nn : 0 ≤ C_tot := le_trans hGYs_nn (le_max_left _ _)
    have h_pt_contr :
        ∀ R Y : ℝ, Y_star ≤ Y → Y ≤ R →
          E Y / Y ^ ε ≤ K_const + (3 / 4 : ℝ) * normalizedScaleSupremum E ε R := by
      intro R Y hYYs hYR
      have hYYd : Y_diag ≤ Y := le_trans hYstar_ge_diag hYYs
      have hRYd : Y_diag ≤ R := le_trans hYYd hYR
      have hY1 : 1 ≤ Y := le_trans hYstar_ge1 hYYs
      have hR1 : 1 ≤ R := le_trans hY1 hYR
      have hY_pos : 0 < Y := lt_of_lt_of_le zero_lt_one hY1
      have hY_pow_pos : 0 < Y ^ ε := Real.rpow_pos_of_pos hY_pos ε
      have hGR_nn : 0 ≤ normalizedScaleSupremum E ε R := (hYs_fin hR1).2.2.1
      obtain ⟨h_fb1, h_fb2⟩ := h_small_fb Y hYYs
      have hD_norm :=
        hD_hor hE_nn hM_nn hE_lin hε_pos hzeta_nn hCc_nn hYdiag_ge_e h_zeta_mass hD_route_d
          R Y hRYd hYYd hYR
      have h8D :
          8 * (D_tilde Y / Y ^ ε) ≤
            (1 / 4 : ℝ) * normalizedScaleSupremum E ε R + 8 * C_cut * Y_star ^ (-ε) := by
        have h1 :
            8 * (D_tilde Y / Y ^ ε) ≤
              (8 * (2 * zeta2_eps / (Real.log Y) ^ 2)) * normalizedScaleSupremum E ε R +
                8 * C_cut * Y ^ (-ε) := by
          have hm := mul_le_mul_of_nonneg_left hD_norm (by norm_num : (0 : ℝ) ≤ 8)
          have h_neg : C_cut / Y ^ ε = C_cut * Y ^ (-ε) := by
            rw [div_eq_mul_inv, Real.rpow_neg (le_of_lt hY_pos)]
          rw [h_neg] at hm
          linarith
        have h2 :
            (8 * (2 * zeta2_eps / (Real.log Y) ^ 2)) * normalizedScaleSupremum E ε R ≤
              (1 / 4 : ℝ) * normalizedScaleSupremum E ε R :=
          mul_le_mul_of_nonneg_right h_fb1 hGR_nn
        have h3 : 8 * C_cut * Y ^ (-ε) ≤ 8 * C_cut * Y_star ^ (-ε) :=
          mul_le_mul_of_nonneg_left
            (rpow_neg_antitone_tc060_aux hYstar_ge1 hYYs (le_of_lt hε_pos))
            (by positivity)
        linarith
      have hK_Y := hK_known R Y hYYd hYR
      have h_rpow_sub : Y ^ η / Y ^ ε = Y ^ (η - ε) := (Real.rpow_sub hY_pos η ε).symm
      have h_eta_dec : Y ^ (η - ε) ≤ Y_star ^ (η - ε) := by
        rw [show η - ε = -(ε - η) by ring]
        exact rpow_neg_antitone_tc060_aux hYstar_ge1 hYYs (by linarith)
      have h4K :
          4 * (K_known Y / Y ^ ε) ≤
            4 * A_k * Y_star ^ (η - ε) + (1 / 4 : ℝ) * normalizedScaleSupremum E ε R := by
        have h_div := div_le_div_of_nonneg_right hK_Y (le_of_lt hY_pow_pos)
        have h_simp :
            (A_k * Y ^ η +
                (B_drift / (Real.log Y) ^ κ_d) * normalizedScaleSupremum E ε R * Y ^ ε) /
              Y ^ ε =
              A_k * Y ^ (η - ε) +
                (B_drift / (Real.log Y) ^ κ_d) * normalizedScaleSupremum E ε R := by
          rw [add_div, mul_div_assoc, h_rpow_sub,
            mul_div_cancel_right₀ _ (ne_of_gt hY_pow_pos)]
        rw [h_simp] at h_div
        have h_fb_G :
            (4 * (B_drift / (Real.log Y) ^ κ_d)) * normalizedScaleSupremum E ε R ≤
              (1 / 4 : ℝ) * normalizedScaleSupremum E ε R :=
          mul_le_mul_of_nonneg_right h_fb2 hGR_nn
        have h_A_le : 4 * A_k * Y ^ (η - ε) ≤ 4 * A_k * Y_star ^ (η - ε) :=
          mul_le_mul_of_nonneg_left h_eta_dec (by positivity)
        linarith
      have hRo_Y := hR_open R Y hYYs hYR
      have hRo :
          R_open Y / Y ^ ε ≤
            A_open * Y_star ^ (η - ε) + (1 / 4 : ℝ) * normalizedScaleSupremum E ε R := by
        have h_div := div_le_div_of_nonneg_right hRo_Y (le_of_lt hY_pow_pos)
        have h_simp :
            (A_open * Y ^ η + (1 / 4 : ℝ) * normalizedScaleSupremum E ε R * Y ^ ε) / Y ^ ε =
              A_open * Y ^ (η - ε) + (1 / 4 : ℝ) * normalizedScaleSupremum E ε R := by
          rw [add_div, mul_div_assoc, h_rpow_sub,
            mul_div_cancel_right₀ _ (ne_of_gt hY_pow_pos)]
        rw [h_simp] at h_div
        have h_Ao_le : A_open * Y ^ (η - ε) ≤ A_open * Y_star ^ (η - ε) :=
          mul_le_mul_of_nonneg_left h_eta_dec hAopen_nn
        linarith
      have hE_div :
          E Y / Y ^ ε ≤ 8 * (D_tilde Y / Y ^ ε) + 4 * (K_known Y / Y ^ ε) + R_open Y / Y ^ ε := by
        have hd := div_le_div_of_nonneg_right (hE_decomp Y hYYd) (le_of_lt hY_pow_pos)
        calc
          E Y / Y ^ ε ≤ (8 * D_tilde Y + 4 * K_known Y + R_open Y) / Y ^ ε := hd
          _ = 8 * (D_tilde Y / Y ^ ε) + 4 * (K_known Y / Y ^ ε) + R_open Y / Y ^ ε := by ring
      dsimp [K_const]
      linarith
    have h_R_ge : ∀ R : ℝ, Y_star ≤ R → normalizedScaleSupremum E ε R ≤ C_tot := by
      intro R hRYs
      have hR1 : 1 ≤ R := le_trans hYstar_ge1 hRYs
      have h_ne_R := (hYs_fin hR1).1
      have h_bdd_Ys := (hYs_fin hYstar_ge1).2.1
      have h_sup_split :
          normalizedScaleSupremum E ε R ≤
            max (normalizedScaleSupremum E ε Y_star)
              (K_const + (3 / 4 : ℝ) * normalizedScaleSupremum E ε R) := by
        unfold normalizedScaleSupremum
        apply csSup_le h_ne_R
        rintro _ ⟨Z, ⟨hZ1, hZR⟩, rfl⟩
        by_cases hZYs : Z ≤ Y_star
        · exact le_trans (le_csSup h_bdd_Ys ⟨Z, ⟨hZ1, hZYs⟩, rfl⟩) (le_max_left _ _)
        · push_neg at hZYs
          exact le_trans (h_pt_contr R Z (le_of_lt hZYs) hZR) (le_max_right _ _)
      rcases max_cases (normalizedScaleSupremum E ε Y_star)
          (K_const + (3 / 4 : ℝ) * normalizedScaleSupremum E ε R) with
        ⟨h_eq, _⟩ | ⟨h_eq, _⟩
      · rw [h_eq] at h_sup_split
        exact le_trans h_sup_split (le_max_left _ _)
      · rw [h_eq] at h_sup_split
        have h_4K : normalizedScaleSupremum E ε R ≤ 4 * K_const := by
          have h1 :
              normalizedScaleSupremum E ε R -
                  (3 / 4 : ℝ) * normalizedScaleSupremum E ε R ≤
                K_const :=
            sub_le_iff_le_add.mpr h_sup_split
          have h2 :
              normalizedScaleSupremum E ε R -
                  (3 / 4 : ℝ) * normalizedScaleSupremum E ε R =
                (1 / 4 : ℝ) * normalizedScaleSupremum E ε R := by ring
          rw [h2] at h1
          have h3 := mul_le_mul_of_nonneg_left h1 (by norm_num : (0 : ℝ) ≤ 4)
          calc
            normalizedScaleSupremum E ε R
              = 4 * ((1 / 4 : ℝ) * normalizedScaleSupremum E ε R) := by ring
            _ ≤ 4 * K_const := h3
        exact le_trans h_4K (le_max_right _ _)
    refine ⟨hKconst_nn, hCtot_nn, h_R_ge, ?_⟩
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

end SignedDilationArithmeticEnergy
end RiemannScope
