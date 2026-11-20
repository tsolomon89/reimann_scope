/-
RiemannScope.JointPrimeDilationSignedRemainder
TASK-TC-062 / TASK-TC-062R (EPIC-TC-042 / SUBGATE-TC-043A):
Joint Prime-Dilation Signed-Remainder Kernel, Exact One-Prime and Disjoint Two-Prime
Anchor Reindexings, Certified Whole-Line Contraction Ratios and Submultiplicativity
Refutation, Spillover Fringe Reindexing and Truncated Mixed-Covariance Equivalence,
Stage A Interior Hilbert Split with Candidate A1 Refutation and Replacement Bound A1',
Interior Prime-Pair Closure Equivalence with Conditional Route D Transfer, and
Two-Sided Interior Anchor-Diagonal Bound with Off-Diagonal Closure Equivalence.

Formalizes in Lean 4 (complete machine-checked proofs with canonical circle constant
RiemannScope.tau throughout; complex coordinates written z = x + i y with x, y real
and critical line x = 1/2):
1. `reassembly_known_part_and_complete_signed_kernel_tc062`
2. `generic_and_liouville_one_prime_pair_decomposition_tc062`
3. `disjoint_two_prime_sixteen_term_and_diagonal_coincidence_tc062`
4. `whole_line_contraction_enclosures_and_submultiplicativity_refutation_tc062`
5. `spillover_fringe_reindexing_and_mixed_covariance_reduction_tc062`
6. `stage_a_interior_hilbert_split_and_candidate_a1_refutation_tc062`
7. `interior_prime_pair_closure_equivalence_and_route_d_transfer_tc062`
8. `two_sided_interior_diag_bound_and_offdiag_equivalence_tc062r`
-/

import Mathlib.NumberTheory.Harmonic.EulerMascheroni
import RiemannScope.MixedArithmeticCovariance

open scoped ArithmeticFunction BigOperators Classical
open MeasureTheory intervalIntegral

namespace RiemannScope
namespace JointPrimeDilationSignedRemainder

open RiemannScope.LiouvilleSquareDilation
open RiemannScope.DyadicPowerLiftPrimitiveCorrelation hiding canonicalPrimePowerDiagDtilde
open RiemannScope.SignedDilationArithmeticEnergy
open RiemannScope.MixedArithmeticCovariance

/-! ### Section 1: Actual Arithmetic Constants and Complete Signed Kernel (`TASK-TC-062` §3) -/

/-- Actual Selberg second-order Liouville constant
    `4 * Re(zeta'(2) / zeta(2)) - 2 * gamma`. -/
noncomputable def actualSelbergConstantCLam : ℝ :=
  4 * (deriv riemannZeta 2 / riemannZeta 2).re - 2 * Real.eulerMascheroniConstant

/-- Actual square-pole drift constant at the critical-line basepoint `x = 1/2, y = 0`
    (`z = x + i y = 1/2`): `4 * Re(zeta'(1/2) / zeta(1/2)) - 8 - 8 * gamma`. -/
noncomputable def actualSquarePoleConstantCHalf : ℝ :=
  4 * (deriv riemannZeta (1 / 2) / riemannZeta (1 / 2)).re - 8 -
    8 * Real.eulerMascheroniConstant

/-- Indicator of the primary integer cutoff `[1, T]` (`1` on `1 <= n <= T`, `0` otherwise). -/
def cutoffIndicatorT (T n : ℕ) : ℝ :=
  if 1 ≤ n ∧ n ≤ T then 1 else 0

/-- Liouville-signed adjusted basis coefficient
    `b_{T, D0}(n) := liouvilleLambda(n) * openCoreAdjustedCoeffBeta(n)`. -/
noncomputable def signedAdjustedCoeffB (c_lam c_half : ℝ) (T D0 n : ℕ) : ℝ :=
  (liouvilleLambda n : ℝ) * openCoreAdjustedCoeffBeta c_lam c_half T D0 n

/-- Complete symmetric signed-remainder kernel `completeSignedKernelHcal` supported on
    `[1, 2 * T] x [1, 2 * T]` assembling the `(0, 2, 4)` logarithmic window kernels,
    the `4 * Dtilde` prime-power diagonal subtraction, and the `4 * Xself` composite
    self-collision subtraction. -/
noncomputable def completeSignedKernelHcal (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ)
    (m n : ℕ) : ℝ :=
  if (1 ≤ m ∧ m ≤ 2 * T) ∧ (1 ≤ n ∧ n ≤ 2 * T) then
    cutoffIndicatorT T m * cutoffIndicatorT T n * logWeightedWindowKernel 0 Y m n -
      (cutoffIndicatorT T m * signedAdjustedCoeffB c_lam c_half T D0 n +
          signedAdjustedCoeffB c_lam c_half T D0 m * cutoffIndicatorT T n +
          4 * cutoffIndicatorT T m * cutoffIndicatorT T n * commonPrimePowerLogSq m n +
          (if m = n then
            4 * cutoffIndicatorT T m * ((Real.log (m : ℝ)) ^ 2 - commonPrimePowerLogSq m m)
          else 0)) *
        logWeightedWindowKernel 2 Y m n +
      signedAdjustedCoeffB c_lam c_half T D0 m * signedAdjustedCoeffB c_lam c_half T D0 n *
        logWeightedWindowKernel 4 Y m n
  else 0

private theorem tau_gt_one_and_lt_eight_tc062_aux :
    (1 : ℝ) < RiemannScope.tau ∧ RiemannScope.tau < 8 := by
  have hpos : 0 < RiemannScope.tau := RiemannScope.tau_pos
  have h_abs_sin : ∀ y : ℝ, 0 ≤ y → Real.sin y ≤ y := by
    intro y hy
    have h_cos_le1 : ∀ t : ℝ, Real.cos t ≤ 1 := fun t => Real.cos_le_one t
    let f : ℝ → ℝ := fun t => t - Real.sin t
    have hf_cont : ContinuousOn f (Set.Ici 0) :=
      continuousOn_id.sub Real.continuous_sin.continuousOn
    have hf_deriv : ∀ t : ℝ, HasDerivAt f (1 - Real.cos t) t :=
      fun t => (hasDerivAt_id t).sub (Real.hasDerivAt_sin t)
    have hf_mono : MonotoneOn f (Set.Ici 0) := by
      apply monotoneOn_of_deriv_nonneg (convex_Ici 0) hf_cont
      · intro t _; exact (hf_deriv t).differentiableAt.differentiableWithinAt
      · intro t _; rw [(hf_deriv t).deriv]; linarith [h_cos_le1 t]
    have h := hf_mono Set.left_mem_Ici hy hy
    dsimp [f] at h
    rw [Real.sin_zero] at h
    linarith
  have hdiv : ∀ x : ℝ, 2 * x / 4 = x / 2 := fun x => by ring
  have hsin : Real.sin (RiemannScope.tau / 4) = 1 := by
    unfold RiemannScope.tau
    rw [hdiv]
    simp
  have hle := h_abs_sin (RiemannScope.tau / 4) (by linarith)
  rw [hsin] at hle
  have hgt1 : (1 : ℝ) < RiemannScope.tau := by linarith
  have hceil : Nat.ceil (RiemannScope.tau * (4096 : ℝ)) ≤ 32767 :=
    (full_core_quantified_obstructions_and_w2_support_tc060r).1.2.1.2.1
  have hle_ceil : RiemannScope.tau * (4096 : ℝ) ≤ (Nat.ceil (RiemannScope.tau * (4096 : ℝ)) : ℝ) :=
    Nat.le_ceil _
  have hceil_real : (Nat.ceil (RiemannScope.tau * (4096 : ℝ)) : ℝ) ≤ 32767 := by
    exact_mod_cast hceil
  exact ⟨hgt1, by linarith⟩

private theorem uIcc_tau_props_tc062_aux {Y : ℝ} (hY2 : 2 ≤ Y) :
    Y ≤ RiemannScope.tau * Y ∧
      ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
        2 ≤ X ∧ 0 < X ∧ 0 < Real.log X ∧ Real.log X ≠ 0 ∧ (Real.log X) ^ 2 ≠ 0 := by
  have htau : (1 : ℝ) < RiemannScope.tau := tau_gt_one_and_lt_eight_tc062_aux.1
  have hle : Y ≤ RiemannScope.tau * Y := by nlinarith
  refine ⟨hle, ?_⟩
  intro X hX
  rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX
  have hX2 : 2 ≤ X := le_trans hY2 hX.1
  have hX0 : 0 < X := by linarith
  have hlog : 0 < Real.log X := Real.log_pos (by linarith)
  exact ⟨hX2, hX0, hlog, ne_of_gt hlog, pow_ne_zero 2 (ne_of_gt hlog)⟩

private theorem canonicalCutoffT_ge_one_tc062_aux {Y : ℝ} (hY1 : 1 ≤ Y) :
    1 ≤ canonicalCutoffT Y := by
  unfold canonicalCutoffT
  have hpos : 0 < Y ^ (5 / 4 : ℝ) := Real.rpow_pos_of_pos (by linarith) (5 / 4 : ℝ)
  exact Nat.one_le_iff_ne_zero.mpr (Nat.ceil_pos.mpr hpos).ne'

private theorem liouvilleLambda_sq_eq_one_tc062_aux {m : ℕ} (hm : 1 ≤ m) :
    (liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ) = 1 := by
  have hm_ne : m ≠ 0 := by omega
  have h_int : liouvilleLambda m * liouvilleLambda m = 1 := by
    simp only [liouvilleLambda, hm_ne, ↓reduceIte, liouvilleSignFromOmega]
    rw [← pow_add, show natOmega m + natOmega m = 2 * natOmega m by omega, pow_mul]
    norm_num
  exact_mod_cast h_int

private theorem liouvilleLambda_mul_pos_tc062_aux {a b : ℕ} (ha : 1 ≤ a) (hb : 1 ≤ b) :
    (liouvilleLambda (a * b) : ℝ) = (liouvilleLambda a : ℝ) * (liouvilleLambda b : ℝ) := by
  have ha_ne : a ≠ 0 := by omega
  have hb_ne : b ≠ 0 := by omega
  have hab_ne : a * b ≠ 0 := mul_ne_zero ha_ne hb_ne
  have h_int : liouvilleLambda (a * b) = liouvilleLambda a * liouvilleLambda b := by
    simp [liouvilleLambda, ha_ne, hb_ne, hab_ne, natOmega,
      ArithmeticFunction.cardFactors_mul ha_ne hb_ne, liouvilleSignFromOmega, pow_add]
  exact_mod_cast h_int

private theorem liouvilleLambda_prime_real_tc062_aux {p : ℕ} (hp : p.Prime) :
    (liouvilleLambda p : ℝ) = -1 := by
  have hop : natOmega p = 1 := ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr hp
  simp [liouvilleLambda, hp.ne_zero, hop, liouvilleSignFromOmega]

private theorem liouvilleLambda_prime_mul_real_tc062_aux {p m : ℕ} (hp : p.Prime) (hm : 1 ≤ m) :
    (liouvilleLambda (p * m) : ℝ) = -(liouvilleLambda m : ℝ) := by
  rw [liouvilleLambda_mul_pos_tc062_aux hp.pos hm, liouvilleLambda_prime_real_tc062_aux hp]
  ring

private theorem abs_liouvilleLambda_eq_one_tc062_aux {n : ℕ} (hn : 1 ≤ n) :
    |(liouvilleLambda n : ℝ)| = 1 := by
  have hsq := liouvilleLambda_sq_eq_one_tc062_aux hn
  have habs : |(liouvilleLambda n : ℝ)| ^ 2 = 1 := by rw [sq_abs, sq]; exact hsq
  nlinarith [abs_nonneg (liouvilleLambda n : ℝ)]

private theorem abs_liouvilleLambda_le_one_tc062_aux (n : ℕ) :
    |(liouvilleLambda n : ℝ)| ≤ 1 := by
  by_cases hn0 : n = 0
  · simp [hn0, liouvilleLambda]
  · exact le_of_eq (abs_liouvilleLambda_eq_one_tc062_aux (Nat.pos_of_ne_zero hn0))

private theorem logWeightedWindowKernel_symm_tc062_aux (ν : ℕ) (Y : ℝ) (m n : ℕ) :
    logWeightedWindowKernel ν Y m n = logWeightedWindowKernel ν Y n m := by
  unfold logWeightedWindowKernel
  congr 1
  ext X
  ring

private theorem commonPrimePowerLogSq_symm_tc062_aux (m n : ℕ) :
    commonPrimePowerLogSq m n = commonPrimePowerLogSq n m := by
  unfold commonPrimePowerLogSq
  rw [min_comm m n, Nat.gcd_comm m n]

/-- **Theorem 1 (`TASK-TC-062` §3, Pointwise Known-Part Reassembly, Complete Signed Kernel Symmetry & Support, and Complete Signed-Remainder Bilinear Identity)**:
    1. *Pointwise known-part reassembly (`1 ≤ T`, `0 < X`, `Real.log X ≠ 0`, and on `[Y, RiemannScope.tau * Y]` for `2 ≤ Y`)*:
       `knownCompensatedD2Part c_lam c_half T D0 X = -(∑ n ∈ Finset.Icc 1 (2 * T), openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) / (Real.log X) ^ 2`;
    2. *Kernel symmetry and `[1, 2 * T]^2` support*:
       `completeSignedKernelHcal c_lam c_half T D0 Y m n = completeSignedKernelHcal c_lam c_half T D0 Y n m`,
       and `¬((1 ≤ m ∧ m ≤ 2 * T) ∧ (1 ≤ n ∧ n ≤ 2 * T)) → completeSignedKernelHcal c_lam c_half T D0 Y m n = 0`;
    3. *Exact complete signed remainder bilinear assembly (`2 ≤ Y`, `1 ≤ T`) and canonical instantiation at `(actualSelbergConstantCLam, actualSquarePoleConstantCHalf)`*:
       `completeSignedRemainderF c_lam c_half T D0 Y = ∑ m ∈ Finset.Icc 1 (2 * T), ∑ n ∈ Finset.Icc 1 (2 * T), (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * completeSignedKernelHcal c_lam c_half T D0 Y m n`. -/
theorem reassembly_known_part_and_complete_signed_kernel_tc062 :
    ((∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ) {X : ℝ},
        0 < X → Real.log X ≠ 0 →
          knownCompensatedD2Part c_lam c_half T D0 X =
            -(∑ n ∈ Finset.Icc 1 (2 * T),
                openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) /
              (Real.log X) ^ 2) ∧
      (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
          knownCompensatedD2Part c_lam c_half T D0 X =
            -(∑ n ∈ Finset.Icc 1 (2 * T),
                openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) /
              (Real.log X) ^ 2)) ∧
    ((∀ (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ) (m n : ℕ),
        completeSignedKernelHcal c_lam c_half T D0 Y m n =
          completeSignedKernelHcal c_lam c_half T D0 Y n m) ∧
      (∀ (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ) (m n : ℕ),
        ¬((1 ≤ m ∧ m ≤ 2 * T) ∧ (1 ≤ n ∧ n ≤ 2 * T)) →
          completeSignedKernelHcal c_lam c_half T D0 Y m n = 0)) ∧
    ((∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        completeSignedRemainderF c_lam c_half T D0 Y =
          ∑ m ∈ Finset.Icc 1 (2 * T), ∑ n ∈ Finset.Icc 1 (2 * T),
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
              completeSignedKernelHcal c_lam c_half T D0 Y m n) ∧
      (∀ {Y : ℝ}, 2 ≤ Y →
        1 ≤ canonicalCutoffT Y ∧
          canonicalSignedRemainderF actualSelbergConstantCLam actualSquarePoleConstantCHalf Y =
            ∑ m ∈ Finset.Icc 1 (2 * canonicalCutoffT Y),
              ∑ n ∈ Finset.Icc 1 (2 * canonicalCutoffT Y),
                (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                  completeSignedKernelHcal
                    actualSelbergConstantCLam actualSquarePoleConstantCHalf
                    (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y m n)) := by
  have h_pt :
      ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ) {X : ℝ},
        0 < X → Real.log X ≠ 0 →
          knownCompensatedD2Part c_lam c_half T D0 X =
            -(∑ n ∈ Finset.Icc 1 (2 * T),
                openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) /
              (Real.log X) ^ 2 := by
    intro T hT D0 c_lam c_half X hX hlog
    have h_tc060 :=
      ((complete_reconstruction_drift_contraction_transfer_tc060).1 hT D0 c_lam c_half hX hlog).2
    have h_tc061r :=
      ((complete_core_adjusted_expansion_and_compact_gram_tc061r).2.2.1 hT D0 c_lam c_half hX hlog).2.1
    rw [neg_div]
    linarith
  have h_win :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
          knownCompensatedD2Part c_lam c_half T D0 X =
            -(∑ n ∈ Finset.Icc 1 (2 * T),
                openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) /
              (Real.log X) ^ 2 := by
    intro Y hY2 T hT D0 c_lam c_half X hX
    obtain ⟨_, hprops⟩ := uIcc_tau_props_tc062_aux hY2
    exact h_pt hT D0 c_lam c_half (hprops X hX).2.1 (hprops X hX).2.2.2.1
  have h_symm :
      ∀ (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ) (m n : ℕ),
        completeSignedKernelHcal c_lam c_half T D0 Y m n =
          completeSignedKernelHcal c_lam c_half T D0 Y n m := by
    intro c_lam c_half T D0 Y m n
    unfold completeSignedKernelHcal
    by_cases hm_in : (1 ≤ m ∧ m ≤ 2 * T) ∧ (1 ≤ n ∧ n ≤ 2 * T)
    · have hn_in : (1 ≤ n ∧ n ≤ 2 * T) ∧ (1 ≤ m ∧ m ≤ 2 * T) := ⟨hm_in.2, hm_in.1⟩
      rw [if_pos hm_in, if_pos hn_in,
        logWeightedWindowKernel_symm_tc062_aux 0 Y m n,
        logWeightedWindowKernel_symm_tc062_aux 2 Y m n,
        logWeightedWindowKernel_symm_tc062_aux 4 Y m n,
        commonPrimePowerLogSq_symm_tc062_aux m n]
      by_cases heq : m = n
      · subst heq
        ring
      · have hneq_symm : ¬ (n = m) := fun h => heq h.symm
        rw [if_neg heq, if_neg hneq_symm]
        ring
    · have hn_not : ¬ ((1 ≤ n ∧ n ≤ 2 * T) ∧ (1 ≤ m ∧ m ≤ 2 * T)) :=
        fun h => hm_in ⟨h.2, h.1⟩
      rw [if_neg hm_in, if_neg hn_not]
  have h_supp :
      ∀ (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ) (m n : ℕ),
        ¬((1 ≤ m ∧ m ≤ 2 * T) ∧ (1 ≤ n ∧ n ≤ 2 * T)) →
          completeSignedKernelHcal c_lam c_half T D0 Y m n = 0 := by
    intro c_lam c_half T D0 Y m n hnot
    unfold completeSignedKernelHcal
    exact if_neg hnot
  have h_F_eq :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        completeSignedRemainderF c_lam c_half T D0 Y =
          ∑ m ∈ Finset.Icc 1 (2 * T), ∑ n ∈ Finset.Icc 1 (2 * T),
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
              completeSignedKernelHcal c_lam c_half T D0 Y m n := by
    intro Y hY2 T hT D0 c_lam c_half
    have h_J_split :=
      (signed_remainder_equivalence_and_sufficient_core_relaxation_tc061r).1.2.2.1
        c_lam c_half T D0 Y
    have h_J_gram :=
      (complete_core_adjusted_expansion_and_compact_gram_tc061r).2.2.2.1
        hY2 hT D0 c_lam c_half
    have h_D_exp :=
      ((finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).1 hY2 T).1
    have h_sub_Icc : Finset.Icc 1 T ⊆ Finset.Icc 1 (2 * T) := by
      intro x hx
      rw [Finset.mem_Icc] at hx ⊢
      omega
    have h_D_2T :
        4 * inheritedPrimePowerDiagDtilde T Y =
          ∑ m ∈ Finset.Icc 1 (2 * T), ∑ n ∈ Finset.Icc 1 (2 * T),
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
              (4 * cutoffIndicatorT T m * cutoffIndicatorT T n * commonPrimePowerLogSq m n) *
              logWeightedWindowKernel 2 Y m n := by
      rw [h_D_exp, Finset.mul_sum]
      have h_step1 :
          (∑ m ∈ Finset.Icc 1 T,
              4 * ∑ n ∈ Finset.Icc 1 T,
                (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
                  logWeightedWindowKernel 2 Y m n) =
            ∑ m ∈ Finset.Icc 1 T,
              ∑ n ∈ Finset.Icc 1 (2 * T),
                (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                  (4 * cutoffIndicatorT T m * cutoffIndicatorT T n * commonPrimePowerLogSq m n) *
                  logWeightedWindowKernel 2 Y m n := by
        apply Finset.sum_congr rfl
        intro m hm
        have hm_ind : cutoffIndicatorT T m = 1 := by
          unfold cutoffIndicatorT; exact if_pos (Finset.mem_Icc.mp hm)
        rw [Finset.mul_sum]
        have h_inner_eq :
            (∑ n ∈ Finset.Icc 1 T,
                4 * ((liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                  commonPrimePowerLogSq m n * logWeightedWindowKernel 2 Y m n)) =
              ∑ n ∈ Finset.Icc 1 T,
                (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                  (4 * cutoffIndicatorT T m * cutoffIndicatorT T n * commonPrimePowerLogSq m n) *
                  logWeightedWindowKernel 2 Y m n := by
          apply Finset.sum_congr rfl
          intro n hn
          have hn_ind : cutoffIndicatorT T n = 1 := by
            unfold cutoffIndicatorT; exact if_pos (Finset.mem_Icc.mp hn)
          rw [hm_ind, hn_ind]
          ring
        rw [h_inner_eq]
        apply Finset.sum_subset h_sub_Icc
        intro n _ hn_not
        have hn_ind : cutoffIndicatorT T n = 0 := by
          unfold cutoffIndicatorT; rw [if_neg]; rwa [Finset.mem_Icc] at hn_not
        rw [hn_ind]; ring
      rw [h_step1]
      apply Finset.sum_subset h_sub_Icc
      intro m _ hm_not
      have hm_ind : cutoffIndicatorT T m = 0 := by
        unfold cutoffIndicatorT; rw [if_neg]; rwa [Finset.mem_Icc] at hm_not
      apply Finset.sum_eq_zero
      intro n _
      rw [hm_ind]; ring
    have h_Xself_2T :
        4 * inheritedPrimePowerSelfCollisionXself T Y =
          ∑ m ∈ Finset.Icc 1 (2 * T), ∑ n ∈ Finset.Icc 1 (2 * T),
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
              (if m = n then
                4 * cutoffIndicatorT T m * ((Real.log (m : ℝ)) ^ 2 - commonPrimePowerLogSq m m)
              else 0) *
              logWeightedWindowKernel 2 Y m n := by
      unfold inheritedPrimePowerSelfCollisionXself
      rw [Finset.mul_sum]
      have h_collapse :
          ∀ m ∈ Finset.Icc 1 (2 * T),
            (∑ n ∈ Finset.Icc 1 (2 * T),
                (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                  (if m = n then
                    4 * cutoffIndicatorT T m *
                      ((Real.log (m : ℝ)) ^ 2 - commonPrimePowerLogSq m m)
                  else 0) *
                  logWeightedWindowKernel 2 Y m n) =
              4 * cutoffIndicatorT T m * offDiagPrimePowerWeight m m *
                logWeightedWindowKernel 2 Y m m := by
        intro m hm
        have hm1 : 1 ≤ m := (Finset.mem_Icc.mp hm).1
        have h_lam_sq := liouvilleLambda_sq_eq_one_tc062_aux hm1
        rw [← Finset.add_sum_erase _ _ hm]
        have h_er :
            (∑ n ∈ (Finset.Icc 1 (2 * T)).erase m,
                (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                  (if m = n then
                    4 * cutoffIndicatorT T m *
                      ((Real.log (m : ℝ)) ^ 2 - commonPrimePowerLogSq m m)
                  else 0) *
                  logWeightedWindowKernel 2 Y m n) = 0 := by
          apply Finset.sum_eq_zero
          intro n hn
          have hne : m ≠ n := (Finset.mem_erase.mp hn).1.symm
          rw [if_neg hne]
          ring
        rw [h_er, add_zero, if_pos rfl, h_lam_sq]
        unfold offDiagPrimePowerWeight
        ring
      symm
      rw [Finset.sum_congr rfl h_collapse]
      symm
      have h_lhs_eq :
          (∑ m ∈ Finset.Icc 1 T,
              4 * (offDiagPrimePowerWeight m m * logWeightedWindowKernel 2 Y m m)) =
            ∑ m ∈ Finset.Icc 1 T,
              4 * cutoffIndicatorT T m * offDiagPrimePowerWeight m m *
                logWeightedWindowKernel 2 Y m m := by
        apply Finset.sum_congr rfl
        intro m hm
        have hm_ind : cutoffIndicatorT T m = 1 := by
          unfold cutoffIndicatorT; exact if_pos (Finset.mem_Icc.mp hm)
        rw [hm_ind]; ring
      rw [h_lhs_eq]
      apply Finset.sum_subset h_sub_Icc
      intro m _ hm_not
      have hm_ind : cutoffIndicatorT T m = 0 := by
        unfold cutoffIndicatorT; rw [if_neg]; rwa [Finset.mem_Icc] at hm_not
      rw [hm_ind]; ring
    have h_F_from_J :
        completeSignedRemainderF c_lam c_half T D0 Y =
          signedMixedCovarianceJ c_lam c_half T D0 Y -
            4 * inheritedPrimePowerSelfCollisionXself T Y := by
      linarith [h_J_split]
    rw [h_F_from_J, h_J_gram, h_D_2T, h_Xself_2T]
    rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro m hm
    rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro n hn
    have hm_bds := Finset.mem_Icc.mp hm
    have hn_bds := Finset.mem_Icc.mp hn
    have hm_sq := liouvilleLambda_sq_eq_one_tc062_aux hm_bds.1
    have hn_sq := liouvilleLambda_sq_eq_one_tc062_aux hn_bds.1
    have h_trunc_m :
        truncatedLiouvilleCoeff T m = (liouvilleLambda m : ℝ) * cutoffIndicatorT T m := by
      unfold truncatedLiouvilleCoeff cutoffIndicatorT
      split_ifs <;> ring
    have h_trunc_n :
        truncatedLiouvilleCoeff T n = (liouvilleLambda n : ℝ) * cutoffIndicatorT T n := by
      unfold truncatedLiouvilleCoeff cutoffIndicatorT
      split_ifs <;> ring
    have h_beta_m :
        openCoreAdjustedCoeffBeta c_lam c_half T D0 m =
          (liouvilleLambda m : ℝ) * signedAdjustedCoeffB c_lam c_half T D0 m := by
      unfold signedAdjustedCoeffB
      calc
        openCoreAdjustedCoeffBeta c_lam c_half T D0 m
          = 1 * openCoreAdjustedCoeffBeta c_lam c_half T D0 m := (one_mul _).symm
        _ = ((liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ)) *
              openCoreAdjustedCoeffBeta c_lam c_half T D0 m := by rw [hm_sq]
        _ = (liouvilleLambda m : ℝ) *
              ((liouvilleLambda m : ℝ) * openCoreAdjustedCoeffBeta c_lam c_half T D0 m) := by ring
    have h_beta_n :
        openCoreAdjustedCoeffBeta c_lam c_half T D0 n =
          (liouvilleLambda n : ℝ) * signedAdjustedCoeffB c_lam c_half T D0 n := by
      unfold signedAdjustedCoeffB
      calc
        openCoreAdjustedCoeffBeta c_lam c_half T D0 n
          = 1 * openCoreAdjustedCoeffBeta c_lam c_half T D0 n := (one_mul _).symm
        _ = ((liouvilleLambda n : ℝ) * (liouvilleLambda n : ℝ)) *
              openCoreAdjustedCoeffBeta c_lam c_half T D0 n := by rw [hn_sq]
        _ = (liouvilleLambda n : ℝ) *
              ((liouvilleLambda n : ℝ) * openCoreAdjustedCoeffBeta c_lam c_half T D0 n) := by ring
    have h_hcal_eq :
        completeSignedKernelHcal c_lam c_half T D0 Y m n =
          cutoffIndicatorT T m * cutoffIndicatorT T n * logWeightedWindowKernel 0 Y m n -
            (cutoffIndicatorT T m * signedAdjustedCoeffB c_lam c_half T D0 n +
                signedAdjustedCoeffB c_lam c_half T D0 m * cutoffIndicatorT T n +
                4 * cutoffIndicatorT T m * cutoffIndicatorT T n * commonPrimePowerLogSq m n +
                (if m = n then
                  4 * cutoffIndicatorT T m * ((Real.log (m : ℝ)) ^ 2 - commonPrimePowerLogSq m m)
                else 0)) *
              logWeightedWindowKernel 2 Y m n +
            signedAdjustedCoeffB c_lam c_half T D0 m * signedAdjustedCoeffB c_lam c_half T D0 n *
              logWeightedWindowKernel 4 Y m n := by
      unfold completeSignedKernelHcal
      exact if_pos ⟨hm_bds, hn_bds⟩
    rw [h_hcal_eq, h_trunc_m, h_trunc_n, h_beta_m, h_beta_n]
    by_cases hmn : m = n
    · rw [if_pos hmn]
      ring
    · rw [if_neg hmn]
      ring
  refine ⟨⟨h_pt, h_win⟩, ⟨h_symm, h_supp⟩, ⟨h_F_eq, ?_⟩⟩
  intro Y hY2
  have hT_can : 1 ≤ canonicalCutoffT Y := canonicalCutoffT_ge_one_tc062_aux (by linarith)
  refine ⟨hT_can, ?_⟩
  unfold canonicalSignedRemainderF
  exact h_F_eq hY2 hT_can (Nat.floor (Real.log Y))
    actualSelbergConstantCLam actualSquarePoleConstantCHalf

/-! ### Section 2: Exact One-Prime and Disjoint Two-Prime Anchor Reindexings (`TASK-TC-062` §4) -/

/-- Even `p`-adic valuation anchors in `[1, N]`:
    `{m ∈ [1, N] : Even (m.factorization p)}`. -/
def primeEvenValuationAnchors (p N : ℕ) : Finset ℕ :=
  (Finset.Icc 1 N).filter (fun m => Even (m.factorization p))

/-- Interior `p`-adic anchor pairs on `[1, N]^2` whose `p`-dilates both stay in `[1, N]`. -/
def primeInteriorAnchorPairs (p N : ℕ) : Finset (ℕ × ℕ) :=
  (primeEvenValuationAnchors p N ×ˢ primeEvenValuationAnchors p N).filter
    (fun mn => p * mn.1 ≤ N ∧ p * mn.2 ≤ N)

/-- Terminal boundary `p`-adic anchor pairs on `[1, N]^2` where at least one `p`-dilate exceeds `N`. -/
def primeTerminalAnchorPairs (p N : ℕ) : Finset (ℕ × ℕ) :=
  (primeEvenValuationAnchors p N ×ˢ primeEvenValuationAnchors p N).filter
    (fun mn => N < p * mn.1 ∨ N < p * mn.2)

/-- Real-valued finite-prime parity control weight `a_S(n) = (finitePrimeSetParity S n : ℝ)`. -/
def finitePrimeParityWeight (S : Finset ℕ) (n : ℕ) : ℝ :=
  (finitePrimeSetParity S n : ℝ)

/-- Joint even `(p, q)`-adic valuation anchors in `[1, N]`. -/
def twoPrimeEvenValuationAnchors (p q N : ℕ) : Finset ℕ :=
  (Finset.Icc 1 N).filter (fun m => Even (m.factorization p) ∧ Even (m.factorization q))

private theorem factorization_prime_mul_self_tc062_aux {p m : ℕ} (hp : p.Prime) (hm : 1 ≤ m) :
    (p * m).factorization p = 1 + m.factorization p := by
  have hm_ne : m ≠ 0 := by omega
  rw [Nat.factorization_mul hp.ne_zero hm_ne, Finsupp.add_apply, hp.factorization,
    Finsupp.single_eq_same]

private theorem factorization_prime_mul_of_ne_tc062_aux {p r m : ℕ} (hp : p.Prime)
    (hpr : p ≠ r) (hm : 1 ≤ m) :
    (p * m).factorization r = m.factorization r := by
  have hm_ne : m ≠ 0 := by omega
  rw [Nat.factorization_mul hp.ne_zero hm_ne, Finsupp.add_apply, hp.factorization,
    Finsupp.single_eq_of_ne hpr, zero_add]

private theorem factorization_prime_pow_mul_self_tc062_aux {p e m : ℕ} (hp : p.Prime)
    (hm : 1 ≤ m) :
    (p ^ e * m).factorization p = e + m.factorization p := by
  have hm_ne : m ≠ 0 := by omega
  have hpe_ne : p ^ e ≠ 0 := pow_ne_zero e hp.ne_zero
  rw [Nat.factorization_mul hpe_ne hm_ne, Finsupp.add_apply, Nat.factorization_pow,
    Finsupp.smul_apply, smul_eq_mul, hp.factorization, Finsupp.single_eq_same, mul_one]

private theorem factorization_prime_pow_mul_of_ne_tc062_aux {p r e m : ℕ} (hp : p.Prime)
    (hpr : p ≠ r) (hm : 1 ≤ m) :
    (p ^ e * m).factorization r = m.factorization r := by
  have hm_ne : m ≠ 0 := by omega
  have hpe_ne : p ^ e ≠ 0 := pow_ne_zero e hp.ne_zero
  rw [Nat.factorization_mul hpe_ne hm_ne, Finsupp.add_apply, Nat.factorization_pow,
    Finsupp.smul_apply, smul_eq_mul, hp.factorization, Finsupp.single_eq_of_ne hpr,
    mul_zero, zero_add]

private theorem sum_filter_Icc_eq_even_factorization_pair_tc062_aux
    {p : ℕ} (hp : p.Prime) (N : ℕ) (P : ℕ → Prop) [DecidablePred P]
    (hP_inv : ∀ m : ℕ, 1 ≤ m → (P (p * m) ↔ P m))
    (g : ℕ → ℝ) (hg_zero : ∀ k : ℕ, N < k → g k = 0) :
    (∑ k ∈ (Finset.Icc 1 N).filter P, g k) =
      ∑ m ∈ (Finset.Icc 1 N).filter (fun m => P m ∧ Even (m.factorization p)),
        (g m + g (p * m)) := by
  let S := (Finset.Icc 1 N).filter P
  let A_even := (Finset.Icc 1 N).filter (fun m => P m ∧ Even (m.factorization p))
  have h_split :=
    (Finset.sum_filter_add_sum_filter_not S (fun k => Even (k.factorization p)) g).symm
  have h_even_eq : S.filter (fun k => Even (k.factorization p)) = A_even := by
    dsimp [S, A_even]
    exact Finset.filter_filter _ _ _
  have h_odd_bij :
      (∑ k ∈ S.filter (fun k => ¬ Even (k.factorization p)), g k) =
        ∑ m ∈ A_even.filter (fun m => p * m ≤ N), g (p * m) := by
    symm
    apply Finset.sum_bij (fun m _ => p * m)
    · intro m hm
      simp only [A_even, S, Finset.mem_filter, Finset.mem_Icc] at hm ⊢
      rcases hm with ⟨⟨⟨hm1, _⟩, ⟨hPm, hm_even⟩⟩, hpmN⟩
      have hpm1 : 1 ≤ p * m := Nat.mul_pos hp.pos hm1
      have hPpm : P (p * m) := (hP_inv m hm1).mpr hPm
      have h_not_even : ¬ Even ((p * m).factorization p) := by
        rw [factorization_prime_mul_self_tc062_aux hp hm1]
        obtain ⟨r, hr⟩ := hm_even
        rw [hr]
        intro h_ev
        obtain ⟨s, hs⟩ := h_ev
        omega
      exact ⟨⟨⟨hpm1, hpmN⟩, hPpm⟩, h_not_even⟩
    · intro m1 _ m2 _ h_eq
      exact Nat.eq_of_mul_eq_mul_left hp.pos h_eq
    · intro k hk
      simp only [S, Finset.mem_filter, Finset.mem_Icc] at hk
      rcases hk with ⟨⟨⟨hk1, hkN⟩, hPk⟩, hk_not_even⟩
      have hp_dvd : p ∣ k := by
        by_contra hnot
        rw [Nat.factorization_eq_zero_of_not_dvd hnot] at hk_not_even
        exact hk_not_even even_zero
      obtain ⟨m, rfl⟩ := hp_dvd
      have hm1 : 1 ≤ m := by
        by_contra hm0
        have hz : m = 0 := by omega
        rw [hz, mul_zero] at hk1
        omega
      have hmN : m ≤ N := le_trans (Nat.le_mul_of_pos_left m hp.pos) hkN
      have hPm : P m := (hP_inv m hm1).mp hPk
      have hm_even : Even (m.factorization p) := by
        rw [factorization_prime_mul_self_tc062_aux hp hm1, add_comm, Nat.even_add_one] at hk_not_even
        exact not_not.mp hk_not_even
      refine ⟨m, ?_, rfl⟩
      simp only [A_even, Finset.mem_filter, Finset.mem_Icc]
      exact ⟨⟨⟨hm1, hmN⟩, ⟨hPm, hm_even⟩⟩, hkN⟩
    · intros; rfl
  have h_odd_ext :
      (∑ m ∈ A_even.filter (fun m => p * m ≤ N), g (p * m)) =
        ∑ m ∈ A_even, g (p * m) := by
    apply Finset.sum_subset (Finset.filter_subset _ _)
    intro m hm hm_not
    have hgt : N < p * m := by
      simp only [Finset.mem_filter] at hm_not
      push_neg at hm_not
      exact hm_not hm
    exact hg_zero (p * m) hgt
  change (∑ k ∈ S, g k) = ∑ m ∈ A_even, (g m + g (p * m))
  rw [h_split, h_even_eq, h_odd_bij, h_odd_ext, ← Finset.sum_add_distrib]

private theorem gcd_factorization_eq_min_tc062_aux {a b r : ℕ} (hr : r.Prime)
    (ha : 1 ≤ a) (hb : 1 ≤ b) :
    (Nat.gcd a b).factorization r = min (a.factorization r) (b.factorization r) := by
  have ha_ne : a ≠ 0 := by omega
  have hb_ne : b ≠ 0 := by omega
  have hgcd_pos : 0 < Nat.gcd a b := Nat.gcd_pos_of_pos_left b (by omega)
  have hgcd_ne : Nat.gcd a b ≠ 0 := ne_of_gt hgcd_pos
  have h_iff : ∀ k : ℕ,
      k ≤ (Nat.gcd a b).factorization r ↔ k ≤ min (a.factorization r) (b.factorization r) := by
    intro k
    rw [← hr.pow_dvd_iff_le_factorization hgcd_ne, Nat.dvd_gcd_iff,
      hr.pow_dvd_iff_le_factorization ha_ne, hr.pow_dvd_iff_le_factorization hb_ne, le_min_iff]
  exact le_antisymm ((h_iff _).mp (le_refl _)) ((h_iff _).mpr (le_refl _))

private theorem commonPrimePowerLogSq_eq_sum_min_factorization_tc062_aux
    {a b : ℕ} (ha : 1 ≤ a) (hb : 1 ≤ b) (U : Finset ℕ)
    (hU_prime : ∀ r ∈ U, r.Prime)
    (hU_sub : (Nat.gcd a b).primeFactors ⊆ U) :
    commonPrimePowerLogSq a b =
      ∑ r ∈ U, ((min (a.factorization r) (b.factorization r) : ℕ) : ℝ) *
        (Real.log (r : ℝ)) ^ 2 := by
  let g := Nat.gcd a b
  have hg_pos : 0 < g := Nat.gcd_pos_of_pos_left b (by omega)
  have hg_ne : g ≠ 0 := ne_of_gt hg_pos
  have hg_le_min : g ≤ min a b :=
    le_min (Nat.le_of_dvd (by omega) (Nat.gcd_dvd_left a b))
      (Nat.le_of_dvd (by omega) (Nat.gcd_dvd_right a b))
  have h_sigma :
      commonPrimePowerLogSq a b =
        ∑ pk ∈ g.primeFactors.sigma (fun r => Finset.Icc 1 (g.factorization r)),
          (Real.log (pk.1 : ℝ)) ^ 2 := by
    unfold commonPrimePowerLogSq
    symm
    apply Finset.sum_bij (fun pk _ => (pk.1, pk.2))
    · rintro ⟨r, k⟩ hrk
      simp only [Finset.mem_sigma, Finset.mem_Icc] at hrk
      rcases hrk with ⟨hr_mem, ⟨hk1, hk_le⟩⟩
      have hr_pr : r.Prime := Nat.prime_of_mem_primeFactors hr_mem
      have hrk_dvd : r ^ k ∣ g := (hr_pr.pow_dvd_iff_le_factorization hg_ne).mpr hk_le
      have hrk_le_g : r ^ k ≤ g := Nat.le_of_dvd hg_pos hrk_dvd
      have hrk_le_min : r ^ k ≤ min a b := le_trans hrk_le_g hg_le_min
      have hr_le_rk : r ≤ r ^ k := Nat.le_self_pow (by omega) r
      have hk_lt_rk : k < r ^ k := Nat.lt_pow_self hr_pr.one_lt k
      simp only [Finset.mem_filter, primePowerPairsUpTo, Finset.mem_product, primesUpToFinset,
        Finset.mem_Icc]
      exact ⟨⟨⟨⟨⟨hr_pr.two_le, le_trans hr_le_rk hrk_le_min⟩, hr_pr⟩,
        ⟨hk1, by omega⟩⟩, hrk_le_min⟩, hrk_dvd⟩
    · rintro ⟨r1, k1⟩ _ ⟨r2, k2⟩ _ h_eq
      cases h_eq; rfl
    · rintro ⟨r, k⟩ hrk
      simp only [Finset.mem_filter, primePowerPairsUpTo, Finset.mem_product, primesUpToFinset,
        Finset.mem_Icc] at hrk
      rcases hrk with ⟨⟨⟨⟨_, hr_pr⟩, ⟨hk1, _⟩⟩, _⟩, hrk_dvd⟩
      have hk_le : k ≤ g.factorization r :=
        (hr_pr.pow_dvd_iff_le_factorization hg_ne).mp hrk_dvd
      have hr_dvd_rk : r ∣ r ^ k := dvd_pow_self r (by omega)
      have hr_mem : r ∈ g.primeFactors :=
        Nat.mem_primeFactors.mpr ⟨hr_pr, dvd_trans hr_dvd_rk hrk_dvd, hg_ne⟩
      exact ⟨⟨r, k⟩, Finset.mem_sigma.mpr ⟨hr_mem, Finset.mem_Icc.mpr ⟨hk1, hk_le⟩⟩, rfl⟩
    · intros; rfl
  rw [h_sigma, Finset.sum_sigma]
  have h_pf :
      (∑ r ∈ g.primeFactors, ∑ _k ∈ Finset.Icc 1 (g.factorization r), (Real.log (r : ℝ)) ^ 2) =
        ∑ r ∈ g.primeFactors,
          ((min (a.factorization r) (b.factorization r) : ℕ) : ℝ) * (Real.log (r : ℝ)) ^ 2 := by
    apply Finset.sum_congr rfl
    intro r hr_mem
    have hr_pr : r.Prime := Nat.prime_of_mem_primeFactors hr_mem
    simp only [Finset.sum_const, Nat.card_Icc, Nat.add_sub_cancel_right, nsmul_eq_mul]
    rw [gcd_factorization_eq_min_tc062_aux hr_pr ha hb]
  rw [h_pf]
  apply Finset.sum_subset hU_sub
  intro r hrU hr_not
  have hr_pr : r.Prime := hU_prime r hrU
  have h_not_dvd : ¬ r ∣ g := fun hd => hr_not (Nat.mem_primeFactors.mpr ⟨hr_pr, hd, hg_ne⟩)
  have hf0 : g.factorization r = 0 := Nat.factorization_eq_zero_of_not_dvd h_not_dvd
  rw [← gcd_factorization_eq_min_tc062_aux hr_pr ha hb, hf0]
  simp

private theorem primeFactors_gcd_subset_insert_two_tc062_aux
    {p q m n : ℕ} (hp : p.Prime) (hq : q.Prime) (hm : 1 ≤ m) (_hn : 1 ≤ n)
    (e1 e2 f1 f2 : ℕ) :
    (Nat.gcd (p ^ e1 * q ^ e2 * m) (p ^ f1 * q ^ f2 * n)).primeFactors ⊆
      insert p (insert q (m.primeFactors ∪ n.primeFactors)) := by
  intro r hr
  rw [Nat.mem_primeFactors] at hr
  rcases hr with ⟨hr_pr, hr_dvd_gcd, _⟩
  have hr_dvd_lhs : r ∣ p ^ e1 * q ^ e2 * m := dvd_trans hr_dvd_gcd (Nat.gcd_dvd_left _ _)
  rcases hr_pr.dvd_mul.mp hr_dvd_lhs with hr_pq | hr_m
  · rcases hr_pr.dvd_mul.mp hr_pq with hr_pe | hr_qe
    · have hrp : r = p :=
        (Nat.dvd_prime hp).mp (hr_pr.dvd_of_dvd_pow hr_pe) |>.resolve_left hr_pr.ne_one
      simp [hrp]
    · have hrq : r = q :=
        (Nat.dvd_prime hq).mp (hr_pr.dvd_of_dvd_pow hr_qe) |>.resolve_left hr_pr.ne_one
      simp [hrq]
  · have hm_ne : m ≠ 0 := by omega
    have hr_in_m : r ∈ m.primeFactors := Nat.mem_primeFactors.mpr ⟨hr_pr, hr_m, hm_ne⟩
    simp [hr_in_m]

/-- **Theorem 2 (`TASK-TC-062` §4, Unique One-Prime Parity Factorization, Generic 4-Term Anchor Reindexing, Matched Parity Sign Law, Liouville Decomposition with Boundary Split, and Exact `commonPrimePowerLogSq` Second Difference)**:
    For every prime `p` (`hp : p.Prime`):
    1. *Unique `p`-adic parity factorization & diagonal disjointness*:
       Every `k ≥ 1` factors uniquely as `(if b then p else 1) * m` with `b : Bool`, `1 ≤ m`, and
       `Even (m.factorization p)`; and for even-valuation positive anchors `m, n`,
       `p * m ≠ n ∧ m ≠ p * n ∧ (p * m = p * n ↔ m = n)`;
    2. *Generic finite 4-term anchor reindexing*:
       Holds for ANY `a : ℕ → ℝ` and ANY `H : ℕ → ℕ → ℝ` vanishing outside `[1, N]^2`;
    3. *Matched parity control sign law*:
       `finitePrimeParityWeight S (p * m) = if p ∈ S then -finitePrimeParityWeight S m else finitePrimeParityWeight S m` (`1 ≤ m`);
    4. *Liouville specialization on `completeSignedRemainderF`, interior/boundary anchor split, canonical instantiation at `(actualSelbergConstantCLam, actualSquarePoleConstantCHalf)`, and exact `commonPrimePowerLogSq` second difference*. -/
theorem generic_and_liouville_one_prime_pair_decomposition_tc062
    {p : ℕ} (hp : p.Prime) :
    ((∀ {k : ℕ}, 1 ≤ k →
        ∃! pair : Bool × ℕ,
          Even (pair.2.factorization p) ∧ 1 ≤ pair.2 ∧
            k = (if pair.1 then p else 1) * pair.2) ∧
      (∀ {m n : ℕ}, 1 ≤ m → 1 ≤ n →
        Even (m.factorization p) → Even (n.factorization p) →
          p * m ≠ n ∧ m ≠ p * n ∧ (p * m = p * n ↔ m = n))) ∧
    (∀ (N : ℕ) (a : ℕ → ℝ) (H : ℕ → ℕ → ℝ),
      (∀ m n : ℕ, ¬((1 ≤ m ∧ m ≤ N) ∧ (1 ≤ n ∧ n ≤ N)) → H m n = 0) →
        (∑ m ∈ Finset.Icc 1 N, ∑ n ∈ Finset.Icc 1 N, a m * a n * H m n) =
          ∑ m ∈ primeEvenValuationAnchors p N, ∑ n ∈ primeEvenValuationAnchors p N,
            (a m * a n * H m n +
              a (p * m) * a n * H (p * m) n +
              a m * a (p * n) * H m (p * n) +
              a (p * m) * a (p * n) * H (p * m) (p * n))) ∧
    (∀ (S : Finset ℕ), (∀ q ∈ S, q.Prime) → ∀ {m : ℕ}, 1 ≤ m →
      finitePrimeParityWeight S (p * m) =
        if p ∈ S then -finitePrimeParityWeight S m else finitePrimeParityWeight S m) ∧
    ((∀ {m : ℕ}, 1 ≤ m → (liouvilleLambda (p * m) : ℝ) = -(liouvilleLambda m : ℝ)) ∧
      (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        let Hcal := completeSignedKernelHcal c_lam c_half T D0 Y
        completeSignedRemainderF c_lam c_half T D0 Y =
            (∑ m ∈ primeEvenValuationAnchors p (2 * T),
              ∑ n ∈ primeEvenValuationAnchors p (2 * T),
                (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                  (Hcal m n - Hcal (p * m) n - Hcal m (p * n) + Hcal (p * m) (p * n))) ∧
          completeSignedRemainderF c_lam c_half T D0 Y =
            (∑ mn ∈ primeInteriorAnchorPairs p (2 * T),
                (liouvilleLambda mn.1 : ℝ) * (liouvilleLambda mn.2 : ℝ) *
                  (Hcal mn.1 mn.2 - Hcal (p * mn.1) mn.2 -
                    Hcal mn.1 (p * mn.2) + Hcal (p * mn.1) (p * mn.2))) +
              (∑ mn ∈ primeTerminalAnchorPairs p (2 * T),
                (liouvilleLambda mn.1 : ℝ) * (liouvilleLambda mn.2 : ℝ) *
                  (Hcal mn.1 mn.2 - Hcal (p * mn.1) mn.2 - Hcal mn.1 (p * mn.2))) ∧
          (∀ mn ∈ primeTerminalAnchorPairs p (2 * T), Hcal (p * mn.1) (p * mn.2) = 0)) ∧
      (∀ {Y : ℝ}, 2 ≤ Y →
        let T := canonicalCutoffT Y
        let D0 := Nat.floor (Real.log Y)
        let Hcal :=
          completeSignedKernelHcal
            actualSelbergConstantCLam actualSquarePoleConstantCHalf T D0 Y
        canonicalSignedRemainderF actualSelbergConstantCLam actualSquarePoleConstantCHalf Y =
          ∑ m ∈ primeEvenValuationAnchors p (2 * T),
            ∑ n ∈ primeEvenValuationAnchors p (2 * T),
              (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                (Hcal m n - Hcal (p * m) n - Hcal m (p * n) + Hcal (p * m) (p * n))) ∧
      (∀ {m n : ℕ}, 1 ≤ m → 1 ≤ n →
        Even (m.factorization p) → Even (n.factorization p) →
          commonPrimePowerLogSq m n - commonPrimePowerLogSq (p * m) n -
              commonPrimePowerLogSq m (p * n) + commonPrimePowerLogSq (p * m) (p * n) =
            if m.factorization p = n.factorization p then (Real.log (p : ℝ)) ^ 2 else 0)) := by
  have h_part1a :
      ∀ {k : ℕ}, 1 ≤ k →
        ∃! pair : Bool × ℕ,
          Even (pair.2.factorization p) ∧ 1 ≤ pair.2 ∧
            k = (if pair.1 then p else 1) * pair.2 := by
    intro k hk1
    have h_uniq :
        ∀ (p1 p2 : Bool × ℕ),
          (Even (p1.2.factorization p) ∧ 1 ≤ p1.2 ∧ k = (if p1.1 then p else 1) * p1.2) →
          (Even (p2.2.factorization p) ∧ 1 ≤ p2.2 ∧ k = (if p2.1 then p else 1) * p2.2) →
          p1 = p2 := by
      rintro ⟨b1, m1⟩ ⟨b2, m2⟩ ⟨hev1, hm1, hk_eq1⟩ ⟨hev2, hm2, hk_eq2⟩
      have h_eq : (if b1 then p else 1) * m1 = (if b2 then p else 1) * m2 :=
        hk_eq1.symm.trans hk_eq2
      cases b1 <;> cases b2
      · simp only [Bool.false_eq_true, ↓reduceIte, one_mul] at h_eq
        subst h_eq; rfl
      · simp only [Bool.false_eq_true, ↓reduceIte, one_mul] at h_eq
        exfalso
        dsimp only at hev1 hm1 hev2 hm2
        have hf : m1.factorization p = (p * m2).factorization p :=
          congr_arg (fun x => x.factorization p) h_eq
        rw [factorization_prime_mul_self_tc062_aux hp hm2] at hf
        obtain ⟨r1, hr1⟩ := hev1
        obtain ⟨r2, hr2⟩ := hev2
        omega
      · simp only [Bool.false_eq_true, ↓reduceIte, one_mul] at h_eq
        exfalso
        dsimp only at hev1 hm1 hev2 hm2
        have hf : (p * m1).factorization p = m2.factorization p :=
          congr_arg (fun x => x.factorization p) h_eq
        rw [factorization_prime_mul_self_tc062_aux hp hm1] at hf
        obtain ⟨r1, hr1⟩ := hev1
        obtain ⟨r2, hr2⟩ := hev2
        omega
      · simp only [↓reduceIte] at h_eq
        have hm_eq : m1 = m2 := Nat.eq_of_mul_eq_mul_left hp.pos h_eq
        subst hm_eq; rfl
    by_cases hk_ev : Even (k.factorization p)
    · refine ⟨(false, k), ⟨hk_ev, hk1, by simp⟩, fun pair hp_pair =>
        h_uniq pair (false, k) hp_pair ⟨hk_ev, hk1, by simp⟩⟩
    · have hp_dvd : p ∣ k := by
        by_contra hnot
        rw [Nat.factorization_eq_zero_of_not_dvd hnot] at hk_ev
        exact hk_ev even_zero
      obtain ⟨m, rfl⟩ := hp_dvd
      have hm1 : 1 ≤ m := by
        by_contra hm0
        have hz : m = 0 := by omega
        rw [hz, mul_zero] at hk1; omega
      have hm_ev : Even (m.factorization p) := by
        rw [factorization_prime_mul_self_tc062_aux hp hm1, add_comm, Nat.even_add_one] at hk_ev
        exact not_not.mp hk_ev
      refine ⟨(true, m), ⟨hm_ev, hm1, by simp⟩, fun pair hp_pair =>
        h_uniq pair (true, m) hp_pair ⟨hm_ev, hm1, by simp⟩⟩
  have h_part1b :
      ∀ {m n : ℕ}, 1 ≤ m → 1 ≤ n →
        Even (m.factorization p) → Even (n.factorization p) →
          p * m ≠ n ∧ m ≠ p * n ∧ (p * m = p * n ↔ m = n) := by
    intro m n hm1 hn1 hme hne
    refine ⟨?_, ?_, ?_⟩
    · intro h_eq
      have hf : (p * m).factorization p = n.factorization p :=
        congr_arg (fun x => x.factorization p) h_eq
      rw [factorization_prime_mul_self_tc062_aux hp hm1] at hf
      obtain ⟨r1, hr1⟩ := hme
      obtain ⟨r2, hr2⟩ := hne
      omega
    · intro h_eq
      have hf : m.factorization p = (p * n).factorization p :=
        congr_arg (fun x => x.factorization p) h_eq
      rw [factorization_prime_mul_self_tc062_aux hp hn1] at hf
      obtain ⟨r1, hr1⟩ := hme
      obtain ⟨r2, hr2⟩ := hne
      omega
    · exact ⟨Nat.eq_of_mul_eq_mul_left hp.pos, fun h => h ▸ rfl⟩
  have h_part2 :
      ∀ (N : ℕ) (a : ℕ → ℝ) (H : ℕ → ℕ → ℝ),
        (∀ m n : ℕ, ¬((1 ≤ m ∧ m ≤ N) ∧ (1 ≤ n ∧ n ≤ N)) → H m n = 0) →
          (∑ m ∈ Finset.Icc 1 N, ∑ n ∈ Finset.Icc 1 N, a m * a n * H m n) =
            ∑ m ∈ primeEvenValuationAnchors p N, ∑ n ∈ primeEvenValuationAnchors p N,
              (a m * a n * H m n +
                a (p * m) * a n * H (p * m) n +
                a m * a (p * n) * H m (p * n) +
                a (p * m) * a (p * n) * H (p * m) (p * n)) := by
    intro N a H hH
    have h1d :
        ∀ (g : ℕ → ℝ), (∀ k : ℕ, N < k → g k = 0) →
          (∑ k ∈ Finset.Icc 1 N, g k) =
            ∑ m ∈ primeEvenValuationAnchors p N, (g m + g (p * m)) := by
      intro g hg
      have h_tr :=
        sum_filter_Icc_eq_even_factorization_pair_tc062_aux hp N (fun _ => True)
          (fun _ _ => Iff.rfl) g hg
      have h_f1 : (Finset.Icc 1 N).filter (fun _ => True) = Finset.Icc 1 N := by
        ext x; simp
      have h_f2 :
          (Finset.Icc 1 N).filter (fun m => True ∧ Even (m.factorization p)) =
            primeEvenValuationAnchors p N := by
        ext x; simp [primeEvenValuationAnchors]
      rwa [h_f1, h_f2] at h_tr
    have h_inner :
        ∀ k1 : ℕ,
          (∑ n ∈ Finset.Icc 1 N, a k1 * a n * H k1 n) =
            ∑ n ∈ primeEvenValuationAnchors p N,
              (a k1 * a n * H k1 n + a k1 * a (p * n) * H k1 (p * n)) := by
      intro k1
      apply h1d
      intro k2 hk2
      have h0 : H k1 k2 = 0 := hH k1 k2 (fun h => by omega)
      rw [h0, mul_zero]
    rw [Finset.sum_congr rfl (fun m _ => h_inner m)]
    rw [h1d (fun k1 =>
      ∑ n ∈ primeEvenValuationAnchors p N,
        (a k1 * a n * H k1 n + a k1 * a (p * n) * H k1 (p * n)))]
    · apply Finset.sum_congr rfl
      intro m _
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro n _
      ring
    · intro k1 hk1
      apply Finset.sum_eq_zero
      intro n _
      have h0a : H k1 n = 0 := hH k1 n (fun h => by omega)
      have h0b : H k1 (p * n) = 0 := hH k1 (p * n) (fun h => by omega)
      rw [h0a, h0b]; ring
  have h_part3 :
      ∀ (S : Finset ℕ), (∀ q ∈ S, q.Prime) → ∀ {m : ℕ}, 1 ≤ m →
        finitePrimeParityWeight S (p * m) =
          if p ∈ S then -finitePrimeParityWeight S m else finitePrimeParityWeight S m := by
    intro S _hS m hm1
    have hm_ne : m ≠ 0 := by omega
    have hpm_ne : p * m ≠ 0 := mul_ne_zero hp.ne_zero hm_ne
    unfold finitePrimeParityWeight finitePrimeSetParity
    rw [if_neg hpm_ne, if_neg hm_ne]
    have h_sum :
        (∑ q ∈ S, (p * m).factorization q) =
          (if p ∈ S then 1 else 0) + ∑ q ∈ S, m.factorization q := by
      have h_each :
          ∀ q ∈ S,
            (p * m).factorization q = (if q = p then 1 else 0) + m.factorization q := by
        intro q _
        by_cases hqp : q = p
        · subst hqp
          rw [if_pos rfl]
          exact factorization_prime_mul_self_tc062_aux hp hm1
        · rw [if_neg hqp]
          simpa using factorization_prime_mul_of_ne_tc062_aux hp (Ne.symm hqp) hm1
      rw [Finset.sum_congr rfl h_each, Finset.sum_add_distrib]
      congr 1
      by_cases hpS : p ∈ S
      · rw [if_pos hpS, ← Finset.add_sum_erase _ _ hpS, if_pos rfl]
        have h_er : (∑ q ∈ S.erase p, if q = p then 1 else 0) = 0 := by
          apply Finset.sum_eq_zero
          intro q hq
          rw [if_neg (Finset.mem_erase.mp hq).1]
        omega
      · rw [if_neg hpS]
        apply Finset.sum_eq_zero
        intro q hq
        have hne : q ≠ p := fun h => hpS (h ▸ hq)
        rw [if_neg hne]
    rw [h_sum, pow_add]
    by_cases hpS : p ∈ S
    · rw [if_pos hpS, if_pos hpS]
      push_cast
      ring
    · rw [if_neg hpS, if_neg hpS]
      push_cast
      ring
  have h_lam_flip : ∀ {m : ℕ}, 1 ≤ m → (liouvilleLambda (p * m) : ℝ) = -(liouvilleLambda m : ℝ) :=
    fun hm1 => liouvilleLambda_prime_mul_real_tc062_aux hp hm1
  have h_F_one_prime :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        let Hcal := completeSignedKernelHcal c_lam c_half T D0 Y
        completeSignedRemainderF c_lam c_half T D0 Y =
            (∑ m ∈ primeEvenValuationAnchors p (2 * T),
              ∑ n ∈ primeEvenValuationAnchors p (2 * T),
                (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                  (Hcal m n - Hcal (p * m) n - Hcal m (p * n) + Hcal (p * m) (p * n))) ∧
          completeSignedRemainderF c_lam c_half T D0 Y =
            (∑ mn ∈ primeInteriorAnchorPairs p (2 * T),
                (liouvilleLambda mn.1 : ℝ) * (liouvilleLambda mn.2 : ℝ) *
                  (Hcal mn.1 mn.2 - Hcal (p * mn.1) mn.2 -
                    Hcal mn.1 (p * mn.2) + Hcal (p * mn.1) (p * mn.2))) +
              (∑ mn ∈ primeTerminalAnchorPairs p (2 * T),
                (liouvilleLambda mn.1 : ℝ) * (liouvilleLambda mn.2 : ℝ) *
                  (Hcal mn.1 mn.2 - Hcal (p * mn.1) mn.2 - Hcal mn.1 (p * mn.2))) ∧
          (∀ mn ∈ primeTerminalAnchorPairs p (2 * T), Hcal (p * mn.1) (p * mn.2) = 0) := by
    intro Y hY2 T hT D0 c_lam c_half
    dsimp only
    let Hcal := completeSignedKernelHcal c_lam c_half T D0 Y
    obtain ⟨_, ⟨_, h_supp⟩, ⟨h_F_eq, _⟩⟩ := reassembly_known_part_and_complete_signed_kernel_tc062
    have h_reidx :=
      h_part2 (2 * T) (fun m => (liouvilleLambda m : ℝ)) Hcal
        (h_supp c_lam c_half T D0 Y)
    have h1 :
        completeSignedRemainderF c_lam c_half T D0 Y =
          ∑ m ∈ primeEvenValuationAnchors p (2 * T),
            ∑ n ∈ primeEvenValuationAnchors p (2 * T),
              (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                (Hcal m n - Hcal (p * m) n - Hcal m (p * n) + Hcal (p * m) (p * n)) := by
      rw [h_F_eq hY2 hT D0 c_lam c_half, h_reidx]
      apply Finset.sum_congr rfl
      intro m hm
      have hm1 : 1 ≤ m := (Finset.mem_Icc.mp (Finset.mem_filter.mp hm).1).1
      apply Finset.sum_congr rfl
      intro n hn
      have hn1 : 1 ≤ n := (Finset.mem_Icc.mp (Finset.mem_filter.mp hn).1).1
      dsimp only
      rw [h_lam_flip hm1, h_lam_flip hn1]
      ring
    have h_term_zero :
        ∀ mn ∈ primeTerminalAnchorPairs p (2 * T), Hcal (p * mn.1) (p * mn.2) = 0 := by
      intro mn hmn
      have h_or := (Finset.mem_filter.mp hmn).2
      exact h_supp c_lam c_half T D0 Y (p * mn.1) (p * mn.2) (fun h => by omega)
    have h2 :
        completeSignedRemainderF c_lam c_half T D0 Y =
          (∑ mn ∈ primeInteriorAnchorPairs p (2 * T),
              (liouvilleLambda mn.1 : ℝ) * (liouvilleLambda mn.2 : ℝ) *
                (Hcal mn.1 mn.2 - Hcal (p * mn.1) mn.2 -
                  Hcal mn.1 (p * mn.2) + Hcal (p * mn.1) (p * mn.2))) +
            (∑ mn ∈ primeTerminalAnchorPairs p (2 * T),
              (liouvilleLambda mn.1 : ℝ) * (liouvilleLambda mn.2 : ℝ) *
                (Hcal mn.1 mn.2 - Hcal (p * mn.1) mn.2 - Hcal mn.1 (p * mn.2))) := by
      rw [h1, ← Finset.sum_product']
      let P_prod := primeEvenValuationAnchors p (2 * T) ×ˢ primeEvenValuationAnchors p (2 * T)
      have h_part_prod :=
        (Finset.sum_filter_add_sum_filter_not P_prod
          (fun mn : ℕ × ℕ => p * mn.1 ≤ 2 * T ∧ p * mn.2 ≤ 2 * T)
          (fun mn =>
            (liouvilleLambda mn.1 : ℝ) * (liouvilleLambda mn.2 : ℝ) *
              (Hcal mn.1 mn.2 - Hcal (p * mn.1) mn.2 -
                Hcal mn.1 (p * mn.2) + Hcal (p * mn.1) (p * mn.2)))).symm
      have h_not_eq :
          P_prod.filter (fun mn : ℕ × ℕ => ¬ (p * mn.1 ≤ 2 * T ∧ p * mn.2 ≤ 2 * T)) =
            primeTerminalAnchorPairs p (2 * T) := by
        ext mn
        simp only [P_prod, primeTerminalAnchorPairs, Finset.mem_filter]
        by_cases hm_in : mn ∈ primeEvenValuationAnchors p (2 * T) ×ˢ primeEvenValuationAnchors p (2 * T)
        · simp only [hm_in, true_and]; omega
        · simp only [hm_in, false_and]
      change (∑ mn ∈ P_prod, _) = _
      rw [h_part_prod, h_not_eq]
      congr 1
      apply Finset.sum_congr rfl
      intro mn hmn
      rw [h_term_zero mn hmn]
      ring
    exact ⟨h1, h2, h_term_zero⟩
  have h_c_diff :
      ∀ {m n : ℕ}, 1 ≤ m → 1 ≤ n →
        Even (m.factorization p) → Even (n.factorization p) →
          commonPrimePowerLogSq m n - commonPrimePowerLogSq (p * m) n -
              commonPrimePowerLogSq m (p * n) + commonPrimePowerLogSq (p * m) (p * n) =
            if m.factorization p = n.factorization p then (Real.log (p : ℝ)) ^ 2 else 0 := by
    intro m n hm1 hn1 _hme _hne
    let U := insert p (insert p (m.primeFactors ∪ n.primeFactors))
    have hU_prime : ∀ r ∈ U, r.Prime := by
      intro r hr
      simp only [U, Finset.mem_insert, Finset.mem_union] at hr
      rcases hr with rfl | rfl | hrm | hrn
      · exact hp
      · exact hp
      · exact Nat.prime_of_mem_primeFactors hrm
      · exact Nat.prime_of_mem_primeFactors hrn
    have hpm1 : 1 ≤ p * m := Nat.mul_pos hp.pos hm1
    have hpn1 : 1 ≤ p * n := Nat.mul_pos hp.pos hn1
    have h00 :
        commonPrimePowerLogSq m n =
          ∑ r ∈ U, ((min (m.factorization r) (n.factorization r) : ℕ) : ℝ) *
            (Real.log (r : ℝ)) ^ 2 := by
      apply commonPrimePowerLogSq_eq_sum_min_factorization_tc062_aux hm1 hn1 U hU_prime
      simpa [U] using primeFactors_gcd_subset_insert_two_tc062_aux hp hp hm1 hn1 0 0 0 0
    have h10 :
        commonPrimePowerLogSq (p * m) n =
          ∑ r ∈ U, ((min ((p * m).factorization r) (n.factorization r) : ℕ) : ℝ) *
            (Real.log (r : ℝ)) ^ 2 := by
      apply commonPrimePowerLogSq_eq_sum_min_factorization_tc062_aux hpm1 hn1 U hU_prime
      simpa [U] using primeFactors_gcd_subset_insert_two_tc062_aux hp hp hm1 hn1 1 0 0 0
    have h01 :
        commonPrimePowerLogSq m (p * n) =
          ∑ r ∈ U, ((min (m.factorization r) ((p * n).factorization r) : ℕ) : ℝ) *
            (Real.log (r : ℝ)) ^ 2 := by
      apply commonPrimePowerLogSq_eq_sum_min_factorization_tc062_aux hm1 hpn1 U hU_prime
      simpa [U] using primeFactors_gcd_subset_insert_two_tc062_aux hp hp hm1 hn1 0 0 1 0
    have h11 :
        commonPrimePowerLogSq (p * m) (p * n) =
          ∑ r ∈ U, ((min ((p * m).factorization r) ((p * n).factorization r) : ℕ) : ℝ) *
            (Real.log (r : ℝ)) ^ 2 := by
      apply commonPrimePowerLogSq_eq_sum_min_factorization_tc062_aux hpm1 hpn1 U hU_prime
      simpa [U] using primeFactors_gcd_subset_insert_two_tc062_aux hp hp hm1 hn1 1 0 1 0
    rw [h00, h10, h01, h11, ← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib,
      ← Finset.sum_add_distrib]
    have hpU : p ∈ U := Finset.mem_insert_self p _
    rw [← Finset.add_sum_erase _ _ hpU]
    have h_er_zero :
        (∑ r ∈ U.erase p,
            (((min (m.factorization r) (n.factorization r) : ℕ) : ℝ) * (Real.log (r : ℝ)) ^ 2 -
              ((min ((p * m).factorization r) (n.factorization r) : ℕ) : ℝ) *
                (Real.log (r : ℝ)) ^ 2 -
              ((min (m.factorization r) ((p * n).factorization r) : ℕ) : ℝ) *
                (Real.log (r : ℝ)) ^ 2 +
              ((min ((p * m).factorization r) ((p * n).factorization r) : ℕ) : ℝ) *
                (Real.log (r : ℝ)) ^ 2)) = 0 := by
      apply Finset.sum_eq_zero
      intro r hr
      have hrp : p ≠ r := (Finset.mem_erase.mp hr).1.symm
      rw [factorization_prime_mul_of_ne_tc062_aux hp hrp hm1,
        factorization_prime_mul_of_ne_tc062_aux hp hrp hn1]
      ring
    rw [h_er_zero, add_zero,
      factorization_prime_mul_self_tc062_aux hp hm1,
      factorization_prime_mul_self_tc062_aux hp hn1]
    set u := m.factorization p
    set v := n.factorization p
    rcases lt_trichotomy u v with huv | huv | huv
    · have h_neq : u ≠ v := ne_of_lt huv
      have h1 : min u v = u := min_eq_left (by omega)
      have h2 : min (1 + u) v = 1 + u := min_eq_left (by omega)
      have h3 : min u (1 + v) = u := min_eq_left (by omega)
      have h4 : min (1 + u) (1 + v) = 1 + u := min_eq_left (by omega)
      rw [if_neg h_neq, h1, h2, h3, h4]
      push_cast; ring
    · rw [if_pos huv, huv]
      have h1 : min v v = v := min_self v
      have h2 : min (1 + v) v = v := min_eq_right (by omega)
      have h3 : min v (1 + v) = v := min_eq_left (by omega)
      have h4 : min (1 + v) (1 + v) = 1 + v := min_self (1 + v)
      rw [h1, h2, h3, h4]
      push_cast; ring
    · have h_neq : u ≠ v := ne_of_gt huv
      have h1 : min u v = v := min_eq_right (by omega)
      have h2 : min (1 + u) v = v := min_eq_right (by omega)
      have h3 : min u (1 + v) = 1 + v := min_eq_right (by omega)
      have h4 : min (1 + u) (1 + v) = 1 + v := min_eq_right (by omega)
      rw [if_neg h_neq, h1, h2, h3, h4]
      push_cast; ring
  refine ⟨⟨h_part1a, h_part1b⟩, h_part2, h_part3, ⟨h_lam_flip, h_F_one_prime, ?_, h_c_diff⟩⟩
  intro Y hY2
  have hT_can : 1 ≤ canonicalCutoffT Y := canonicalCutoffT_ge_one_tc062_aux (by linarith)
  exact (h_F_one_prime hY2 hT_can (Nat.floor (Real.log Y))
    actualSelbergConstantCLam actualSquarePoleConstantCHalf).1

/-- **Theorem 3 (`TASK-TC-062` §4, Disjoint Two-Prime Unique Parity Factorization, 16-Term Diagonal Coincidence Classification, Generic & Liouville 16-Term Reindexing, and Exact Two-Prime Fourth-Difference Annihilation of `commonPrimePowerLogSq`)**:
    For distinct primes `p ≠ q` (`hp : p.Prime`, `hq : q.Prime`, `hpq : p ≠ q`):
    1. *Unique `(p, q)` parity factorization & exact 16-term diagonal coincidence classification*:
       `p ^ e1 * q ^ e2 * m = p ^ f1 * q ^ f2 * n ↔ e1 = f1 ∧ e2 = f2 ∧ m = n`
       for `e1, e2, f1, f2 ∈ {0, 1}` and positive `(p, q)`-even-valuation anchors `m, n`;
    2. *Generic 16-term reindexing and Liouville 16-term identity for `completeSignedRemainderF`*
       (including canonical instantiation at `(actualSelbergConstantCLam, actualSquarePoleConstantCHalf)`);
    3. *Exact two-prime fourth-difference annihilation of `commonPrimePowerLogSq`*:
       `∑_{e1, e2, f1, f2 ∈ {0, 1}} (-1)^(e1 + e2 + f1 + f2) * commonPrimePowerLogSq (p^e1 * q^e2 * m) (p^f1 * q^f2 * n) = 0`. -/
theorem disjoint_two_prime_sixteen_term_and_diagonal_coincidence_tc062
    {p q : ℕ} (hp : p.Prime) (hq : q.Prime) (hpq : p ≠ q) :
    ((∀ {k : ℕ}, 1 ≤ k →
        ∃! tup : ℕ × ℕ × ℕ,
          tup.1 ∈ ({0, 1} : Finset ℕ) ∧
            tup.2.1 ∈ ({0, 1} : Finset ℕ) ∧
            Even (tup.2.2.factorization p) ∧
            Even (tup.2.2.factorization q) ∧
            1 ≤ tup.2.2 ∧
            k = p ^ tup.1 * q ^ tup.2.1 * tup.2.2) ∧
      (∀ {m n e1 e2 f1 f2 : ℕ},
        1 ≤ m → 1 ≤ n →
        Even (m.factorization p) → Even (m.factorization q) →
        Even (n.factorization p) → Even (n.factorization q) →
        e1 ∈ ({0, 1} : Finset ℕ) → e2 ∈ ({0, 1} : Finset ℕ) →
        f1 ∈ ({0, 1} : Finset ℕ) → f2 ∈ ({0, 1} : Finset ℕ) →
          (p ^ e1 * q ^ e2 * m = p ^ f1 * q ^ f2 * n ↔ e1 = f1 ∧ e2 = f2 ∧ m = n))) ∧
    ((∀ (N : ℕ) (a : ℕ → ℝ) (H : ℕ → ℕ → ℝ),
        (∀ m n : ℕ, ¬((1 ≤ m ∧ m ≤ N) ∧ (1 ≤ n ∧ n ≤ N)) → H m n = 0) →
          (∑ m ∈ Finset.Icc 1 N, ∑ n ∈ Finset.Icc 1 N, a m * a n * H m n) =
            ∑ m ∈ twoPrimeEvenValuationAnchors p q N,
              ∑ n ∈ twoPrimeEvenValuationAnchors p q N,
                ∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ e2 ∈ ({0, 1} : Finset ℕ),
                  ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
                    a (p ^ e1 * q ^ e2 * m) * a (p ^ f1 * q ^ f2 * n) *
                      H (p ^ e1 * q ^ e2 * m) (p ^ f1 * q ^ f2 * n)) ∧
      (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        let Hcal := completeSignedKernelHcal c_lam c_half T D0 Y
        completeSignedRemainderF c_lam c_half T D0 Y =
          ∑ m ∈ twoPrimeEvenValuationAnchors p q (2 * T),
            ∑ n ∈ twoPrimeEvenValuationAnchors p q (2 * T),
              (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                ∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ e2 ∈ ({0, 1} : Finset ℕ),
                  ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
                    (-1 : ℝ) ^ (e1 + e2 + f1 + f2) *
                      Hcal (p ^ e1 * q ^ e2 * m) (p ^ f1 * q ^ f2 * n)) ∧
      (∀ {Y : ℝ}, 2 ≤ Y →
        let T := canonicalCutoffT Y
        let D0 := Nat.floor (Real.log Y)
        let Hcal :=
          completeSignedKernelHcal
            actualSelbergConstantCLam actualSquarePoleConstantCHalf T D0 Y
        canonicalSignedRemainderF actualSelbergConstantCLam actualSquarePoleConstantCHalf Y =
          ∑ m ∈ twoPrimeEvenValuationAnchors p q (2 * T),
            ∑ n ∈ twoPrimeEvenValuationAnchors p q (2 * T),
              (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                ∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ e2 ∈ ({0, 1} : Finset ℕ),
                  ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
                    (-1 : ℝ) ^ (e1 + e2 + f1 + f2) *
                      Hcal (p ^ e1 * q ^ e2 * m) (p ^ f1 * q ^ f2 * n))) ∧
    ((∀ {m n : ℕ}, 1 ≤ m → 1 ≤ n →
        (∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ e2 ∈ ({0, 1} : Finset ℕ),
          ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
            (-1 : ℝ) ^ (e1 + e2 + f1 + f2) *
              commonPrimePowerLogSq (p ^ e1 * q ^ e2 * m) (p ^ f1 * q ^ f2 * n)) = 0) ∧
      (∀ (N : ℕ), ∀ m ∈ twoPrimeEvenValuationAnchors p q N,
        ∀ n ∈ twoPrimeEvenValuationAnchors p q N,
          (∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ e2 ∈ ({0, 1} : Finset ℕ),
            ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
              (-1 : ℝ) ^ (e1 + e2 + f1 + f2) *
                commonPrimePowerLogSq (p ^ e1 * q ^ e2 * m) (p ^ f1 * q ^ f2 * n)) = 0)) := by
  have h_coinc :
      ∀ {m n e1 e2 f1 f2 : ℕ},
        1 ≤ m → 1 ≤ n →
        Even (m.factorization p) → Even (m.factorization q) →
        Even (n.factorization p) → Even (n.factorization q) →
        e1 ∈ ({0, 1} : Finset ℕ) → e2 ∈ ({0, 1} : Finset ℕ) →
        f1 ∈ ({0, 1} : Finset ℕ) → f2 ∈ ({0, 1} : Finset ℕ) →
          (p ^ e1 * q ^ e2 * m = p ^ f1 * q ^ f2 * n ↔ e1 = f1 ∧ e2 = f2 ∧ m = n) := by
    intro m n e1 e2 f1 f2 hm1 hn1 hmp hmq hnp hnq he1 he2 hf1 hf2
    constructor
    · intro h_eq
      have hqm1 : 1 ≤ q ^ e2 * m := Nat.mul_pos (pow_pos hq.pos e2) hm1
      have hqn1 : 1 ≤ q ^ f2 * n := Nat.mul_pos (pow_pos hq.pos f2) hn1
      have hfp : (p ^ e1 * q ^ e2 * m).factorization p = (p ^ f1 * q ^ f2 * n).factorization p :=
        congr_arg (fun x => x.factorization p) h_eq
      rw [mul_assoc (p ^ e1), mul_assoc (p ^ f1),
        factorization_prime_pow_mul_self_tc062_aux (e := e1) hp hqm1,
        factorization_prime_pow_mul_self_tc062_aux (e := f1) hp hqn1,
        factorization_prime_pow_mul_of_ne_tc062_aux (e := e2) hq hpq.symm hm1,
        factorization_prime_pow_mul_of_ne_tc062_aux (e := f2) hq hpq.symm hn1] at hfp
      have h_eq_qm : q ^ e2 * (p ^ e1 * m) = p ^ e1 * q ^ e2 * m := by ring
      have h_eq_qn : q ^ f2 * (p ^ f1 * n) = p ^ f1 * q ^ f2 * n := by ring
      have hpm1 : 1 ≤ p ^ e1 * m := Nat.mul_pos (pow_pos hp.pos e1) hm1
      have hpn1 : 1 ≤ p ^ f1 * n := Nat.mul_pos (pow_pos hp.pos f1) hn1
      have hfq : (q ^ e2 * (p ^ e1 * m)).factorization q = (q ^ f2 * (p ^ f1 * n)).factorization q :=
        congr_arg (fun x => x.factorization q) (h_eq_qm.trans (h_eq.trans h_eq_qn.symm))
      rw [factorization_prime_pow_mul_self_tc062_aux (e := e2) hq hpm1,
        factorization_prime_pow_mul_self_tc062_aux (e := f2) hq hpn1,
        factorization_prime_pow_mul_of_ne_tc062_aux (e := e1) hp hpq hm1,
        factorization_prime_pow_mul_of_ne_tc062_aux (e := f1) hp hpq hn1] at hfq
      simp only [Finset.mem_insert, Finset.mem_singleton] at he1 he2 hf1 hf2
      obtain ⟨rp1, hrp1⟩ := hmp
      obtain ⟨rp2, hrp2⟩ := hnp
      obtain ⟨rq1, hrq1⟩ := hmq
      obtain ⟨rq2, hrq2⟩ := hnq
      have he1_eq : e1 = f1 := by
        rcases he1 with rfl | rfl <;> rcases hf1 with rfl | rfl <;> omega
      have he2_eq : e2 = f2 := by
        rcases he2 with rfl | rfl <;> rcases hf2 with rfl | rfl <;> omega
      subst he1_eq; subst he2_eq
      have h_pos : 0 < p ^ e1 * q ^ e2 := Nat.mul_pos (pow_pos hp.pos e1) (pow_pos hq.pos e2)
      exact ⟨rfl, rfl, Nat.eq_of_mul_eq_mul_left h_pos h_eq⟩
    · rintro ⟨rfl, rfl, rfl⟩
      rfl
  have h_uniq_pq :
      ∀ {k : ℕ}, 1 ≤ k →
        ∃! tup : ℕ × ℕ × ℕ,
          tup.1 ∈ ({0, 1} : Finset ℕ) ∧
            tup.2.1 ∈ ({0, 1} : Finset ℕ) ∧
            Even (tup.2.2.factorization p) ∧
            Even (tup.2.2.factorization q) ∧
            1 ≤ tup.2.2 ∧
            k = p ^ tup.1 * q ^ tup.2.1 * tup.2.2 := by
    intro k hk1
    obtain ⟨⟨b1, m1⟩, ⟨hm1_ev_p, hm1_ge1, hk_eq1⟩, _⟩ :=
      (generic_and_liouville_one_prime_pair_decomposition_tc062 hp).1.1 hk1
    obtain ⟨⟨b2, m⟩, ⟨hm_ev_q, hm_ge1, hm1_eq⟩, _⟩ :=
      (generic_and_liouville_one_prime_pair_decomposition_tc062 hq).1.1 hm1_ge1
    let e1 : ℕ := if b1 then 1 else 0
    let e2 : ℕ := if b2 then 1 else 0
    have he1_mem : e1 ∈ ({0, 1} : Finset ℕ) := by dsimp [e1]; split_ifs <;> simp
    have he2_mem : e2 ∈ ({0, 1} : Finset ℕ) := by dsimp [e2]; split_ifs <;> simp
    have h_pow1 : (if b1 then p else 1) = p ^ e1 := by dsimp [e1]; cases b1 <;> simp
    have h_pow2 : (if b2 then q else 1) = q ^ e2 := by dsimp [e2]; cases b2 <;> simp
    have hm_ev_p : Even (m.factorization p) := by
      have hf := hm1_eq
      rw [h_pow2] at hf
      subst hf
      rwa [factorization_prime_pow_mul_of_ne_tc062_aux hq hpq.symm hm_ge1] at hm1_ev_p
    have hk_tot : k = p ^ e1 * q ^ e2 * m := by
      rw [hk_eq1, hm1_eq, h_pow1, h_pow2, mul_assoc]
    refine ⟨(e1, e2, m), ⟨he1_mem, he2_mem, hm_ev_p, hm_ev_q, hm_ge1, hk_tot⟩, ?_⟩
    rintro ⟨f1, f2, n⟩ ⟨hf1_mem, hf2_mem, hn_ev_p, hn_ev_q, hn_ge1, hk_tot'⟩
    have h_eq := hk_tot'.symm.trans hk_tot
    obtain ⟨h1, h2, h3⟩ :=
      (h_coinc hn_ge1 hm_ge1 hn_ev_p hn_ev_q hm_ev_p hm_ev_q
        hf1_mem hf2_mem he1_mem he2_mem).mp h_eq
    subst h1; subst h2; subst h3
    rfl
  have h1d_pq :
      ∀ (N : ℕ) (g : ℕ → ℝ), (∀ k : ℕ, N < k → g k = 0) →
        (∑ k ∈ Finset.Icc 1 N, g k) =
          ∑ m ∈ twoPrimeEvenValuationAnchors p q N,
            ∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ e2 ∈ ({0, 1} : Finset ℕ),
              g (p ^ e1 * q ^ e2 * m) := by
    intro N g hg
    have h_step_p :=
      sum_filter_Icc_eq_even_factorization_pair_tc062_aux hp N (fun _ => True)
        (fun _ _ => Iff.rfl) g hg
    have h_f1 : (Finset.Icc 1 N).filter (fun _ => True) = Finset.Icc 1 N := by
      ext x; simp
    have h_f2 :
        (Finset.Icc 1 N).filter (fun m => True ∧ Even (m.factorization p)) =
          (Finset.Icc 1 N).filter (fun m => Even (m.factorization p)) := by
      ext x; simp
    rw [h_f1, h_f2] at h_step_p
    have hP_q_inv : ∀ m : ℕ, 1 ≤ m →
        (Even ((q * m).factorization p) ↔ Even (m.factorization p)) := by
      intro m hm1
      rw [factorization_prime_mul_of_ne_tc062_aux hq hpq.symm hm1]
    have hg'_zero : ∀ k : ℕ, N < k → g k + g (p * k) = 0 := by
      intro k hk
      have hk_pm : N < p * k := lt_of_lt_of_le hk (Nat.le_mul_of_pos_left k hp.pos)
      rw [hg k hk, hg (p * k) hk_pm, add_zero]
    have h_step_q :=
      sum_filter_Icc_eq_even_factorization_pair_tc062_aux hq N
        (fun m => Even (m.factorization p)) hP_q_inv
        (fun k => g k + g (p * k)) hg'_zero
    rw [h_step_p, h_step_q]
    have h_set_eq :
        (Finset.Icc 1 N).filter (fun m => Even (m.factorization p) ∧ Even (m.factorization q)) =
          twoPrimeEvenValuationAnchors p q N := rfl
    rw [h_set_eq]
    apply Finset.sum_congr rfl
    intro m _
    have h01 : ({0, 1} : Finset ℕ) = insert 0 {1} := rfl
    rw [h01, Finset.sum_insert (by decide), Finset.sum_singleton,
      Finset.sum_insert (by decide), Finset.sum_singleton,
      Finset.sum_insert (by decide), Finset.sum_singleton]
    simp only [pow_zero, pow_one, one_mul]
    have h_comm_pq : p * q * m = p * (q * m) := by ring
    rw [h_comm_pq]
    ring
  have h_reidx_16_clean :
      ∀ (N : ℕ) (a : ℕ → ℝ) (H : ℕ → ℕ → ℝ),
        (∀ m n : ℕ, ¬((1 ≤ m ∧ m ≤ N) ∧ (1 ≤ n ∧ n ≤ N)) → H m n = 0) →
          (∑ m ∈ Finset.Icc 1 N, ∑ n ∈ Finset.Icc 1 N, a m * a n * H m n) =
            ∑ m ∈ twoPrimeEvenValuationAnchors p q N,
              ∑ n ∈ twoPrimeEvenValuationAnchors p q N,
                ∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ e2 ∈ ({0, 1} : Finset ℕ),
                  ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
                    a (p ^ e1 * q ^ e2 * m) * a (p ^ f1 * q ^ f2 * n) *
                      H (p ^ e1 * q ^ e2 * m) (p ^ f1 * q ^ f2 * n) := by
    intro N a H hH
    have h_in :
        ∀ k1 : ℕ,
          (∑ n ∈ Finset.Icc 1 N, a k1 * a n * H k1 n) =
            ∑ n ∈ twoPrimeEvenValuationAnchors p q N,
              ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
                a k1 * a (p ^ f1 * q ^ f2 * n) * H k1 (p ^ f1 * q ^ f2 * n) := by
      intro k1
      apply h1d_pq N
      intro k2 hk2
      rw [hH k1 k2 (fun h => by omega), mul_zero]
    rw [Finset.sum_congr rfl (fun m _ => h_in m)]
    rw [h1d_pq N (fun k1 =>
      ∑ n ∈ twoPrimeEvenValuationAnchors p q N,
        ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
          a k1 * a (p ^ f1 * q ^ f2 * n) * H k1 (p ^ f1 * q ^ f2 * n))]
    · apply Finset.sum_congr rfl
      intro m _
      trans (∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ n ∈ twoPrimeEvenValuationAnchors p q N,
        ∑ e2 ∈ ({0, 1} : Finset ℕ), ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
          a (p ^ e1 * q ^ e2 * m) * a (p ^ f1 * q ^ f2 * n) *
            H (p ^ e1 * q ^ e2 * m) (p ^ f1 * q ^ f2 * n))
      · apply Finset.sum_congr rfl
        intro e1 _
        exact Finset.sum_comm
      · exact Finset.sum_comm
    · intro k1 hk1
      apply Finset.sum_eq_zero
      intro n _
      apply Finset.sum_eq_zero
      intro f1 _
      apply Finset.sum_eq_zero
      intro f2 _
      rw [hH k1 _ (fun h => by omega), mul_zero]
  have h_lam_pq :
      ∀ {m : ℕ}, 1 ≤ m → ∀ e1 e2 : ℕ,
        (liouvilleLambda (p ^ e1 * q ^ e2 * m) : ℝ) =
          (-1 : ℝ) ^ (e1 + e2) * (liouvilleLambda m : ℝ) := by
    intro m hm1 e1 e2
    have hpe1 : 1 ≤ p ^ e1 := Nat.one_le_pow e1 p hp.pos
    have hqe2 : 1 ≤ q ^ e2 := Nat.one_le_pow e2 q hq.pos
    have h_pow_lam :
        ∀ {r : ℕ}, r.Prime → ∀ e : ℕ, (liouvilleLambda (r ^ e) : ℝ) = (-1 : ℝ) ^ e := by
      intro r hr e
      induction' e with e ih
      · simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
      · rw [pow_succ', liouvilleLambda_mul_pos_tc062_aux hr.pos (Nat.one_le_pow e r hr.pos),
          liouvilleLambda_prime_real_tc062_aux hr, ih, pow_succ']
    rw [liouvilleLambda_mul_pos_tc062_aux (Nat.mul_pos hpe1 hqe2) hm1,
      liouvilleLambda_mul_pos_tc062_aux hpe1 hqe2,
      h_pow_lam hp e1, h_pow_lam hq e2, pow_add]
  have h_F_16 :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        let Hcal := completeSignedKernelHcal c_lam c_half T D0 Y
        completeSignedRemainderF c_lam c_half T D0 Y =
          ∑ m ∈ twoPrimeEvenValuationAnchors p q (2 * T),
            ∑ n ∈ twoPrimeEvenValuationAnchors p q (2 * T),
              (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
                ∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ e2 ∈ ({0, 1} : Finset ℕ),
                  ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
                    (-1 : ℝ) ^ (e1 + e2 + f1 + f2) *
                      Hcal (p ^ e1 * q ^ e2 * m) (p ^ f1 * q ^ f2 * n) := by
    intro Y hY2 T hT D0 c_lam c_half
    dsimp only
    let Hcal := completeSignedKernelHcal c_lam c_half T D0 Y
    obtain ⟨_, ⟨_, h_supp⟩, ⟨h_F_eq, _⟩⟩ := reassembly_known_part_and_complete_signed_kernel_tc062
    rw [h_F_eq hY2 hT D0 c_lam c_half,
      h_reidx_16_clean (2 * T) (fun m => (liouvilleLambda m : ℝ)) Hcal
        (h_supp c_lam c_half T D0 Y)]
    apply Finset.sum_congr rfl
    intro m hm
    have hm1 : 1 ≤ m := (Finset.mem_Icc.mp (Finset.mem_filter.mp hm).1).1
    apply Finset.sum_congr rfl
    intro n hn
    have hn1 : 1 ≤ n := (Finset.mem_Icc.mp (Finset.mem_filter.mp hn).1).1
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro e1 _
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro e2 _
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro f1 _
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro f2 _
    rw [h_lam_pq hm1 e1 e2, h_lam_pq hn1 f1 f2,
      show e1 + e2 + f1 + f2 = (e1 + e2) + (f1 + f2) by omega, pow_add]
    ring
  have h_annih :
      ∀ {m n : ℕ}, 1 ≤ m → 1 ≤ n →
        (∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ e2 ∈ ({0, 1} : Finset ℕ),
          ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
            (-1 : ℝ) ^ (e1 + e2 + f1 + f2) *
              commonPrimePowerLogSq (p ^ e1 * q ^ e2 * m) (p ^ f1 * q ^ f2 * n)) = 0 := by
    intro m n hm1 hn1
    let U := insert p (insert q (m.primeFactors ∪ n.primeFactors))
    have hU_prime : ∀ r ∈ U, r.Prime := by
      intro r hr
      simp only [U, Finset.mem_insert, Finset.mem_union] at hr
      rcases hr with rfl | rfl | hrm | hrn
      · exact hp
      · exact hq
      · exact Nat.prime_of_mem_primeFactors hrm
      · exact Nat.prime_of_mem_primeFactors hrn
    have h_each_c :
        ∀ e1 e2 f1 f2 : ℕ,
          commonPrimePowerLogSq (p ^ e1 * q ^ e2 * m) (p ^ f1 * q ^ f2 * n) =
            ∑ r ∈ U,
              ((min ((p ^ e1 * q ^ e2 * m).factorization r)
                  ((p ^ f1 * q ^ f2 * n).factorization r) : ℕ) : ℝ) *
                (Real.log (r : ℝ)) ^ 2 := by
      intro e1 e2 f1 f2
      have ha1 : 1 ≤ p ^ e1 * q ^ e2 * m :=
        Nat.mul_pos (Nat.mul_pos (pow_pos hp.pos e1) (pow_pos hq.pos e2)) hm1
      have hb1 : 1 ≤ p ^ f1 * q ^ f2 * n :=
        Nat.mul_pos (Nat.mul_pos (pow_pos hp.pos f1) (pow_pos hq.pos f2)) hn1
      exact commonPrimePowerLogSq_eq_sum_min_factorization_tc062_aux ha1 hb1 U hU_prime
        (primeFactors_gcd_subset_insert_two_tc062_aux hp hq hm1 hn1 e1 e2 f1 f2)
    have h01 : ({0, 1} : Finset ℕ) = insert 0 {1} := rfl
    have h_expand_16 :
        (∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ e2 ∈ ({0, 1} : Finset ℕ),
          ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
            (-1 : ℝ) ^ (e1 + e2 + f1 + f2) *
              commonPrimePowerLogSq (p ^ e1 * q ^ e2 * m) (p ^ f1 * q ^ f2 * n)) =
          ∑ r ∈ U,
            ∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ e2 ∈ ({0, 1} : Finset ℕ),
              ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
                (-1 : ℝ) ^ (e1 + e2 + f1 + f2) *
                  (((min ((p ^ e1 * q ^ e2 * m).factorization r)
                      ((p ^ f1 * q ^ f2 * n).factorization r) : ℕ) : ℝ) *
                    (Real.log (r : ℝ)) ^ 2) := by
      simp_rw [h_each_c, Finset.mul_sum]
      trans (∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ e2 ∈ ({0, 1} : Finset ℕ),
        ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ r ∈ U, ∑ f2 ∈ ({0, 1} : Finset ℕ),
          (-1 : ℝ) ^ (e1 + e2 + f1 + f2) *
            (((min ((p ^ e1 * q ^ e2 * m).factorization r)
                ((p ^ f1 * q ^ f2 * n).factorization r) : ℕ) : ℝ) *
              (Real.log (r : ℝ)) ^ 2))
      · apply Finset.sum_congr rfl; intro e1 _
        apply Finset.sum_congr rfl; intro e2 _
        apply Finset.sum_congr rfl; intro f1 _
        exact Finset.sum_comm
      trans (∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ e2 ∈ ({0, 1} : Finset ℕ),
        ∑ r ∈ U, ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
          (-1 : ℝ) ^ (e1 + e2 + f1 + f2) *
            (((min ((p ^ e1 * q ^ e2 * m).factorization r)
                ((p ^ f1 * q ^ f2 * n).factorization r) : ℕ) : ℝ) *
              (Real.log (r : ℝ)) ^ 2))
      · apply Finset.sum_congr rfl; intro e1 _
        apply Finset.sum_congr rfl; intro e2 _
        exact Finset.sum_comm
      trans (∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ r ∈ U, ∑ e2 ∈ ({0, 1} : Finset ℕ),
        ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
          (-1 : ℝ) ^ (e1 + e2 + f1 + f2) *
            (((min ((p ^ e1 * q ^ e2 * m).factorization r)
                ((p ^ f1 * q ^ f2 * n).factorization r) : ℕ) : ℝ) *
              (Real.log (r : ℝ)) ^ 2))
      · apply Finset.sum_congr rfl; intro e1 _
        exact Finset.sum_comm
      · exact Finset.sum_comm
    rw [h_expand_16]
    apply Finset.sum_eq_zero
    intro r _hrU
    by_cases hrp : r = p
    · rw [hrp]
      have h_indep :
          ∀ e1 e2 f1 f2 : ℕ,
            (p ^ e1 * q ^ e2 * m).factorization p = e1 + m.factorization p ∧
              (p ^ f1 * q ^ f2 * n).factorization p = f1 + n.factorization p := by
        intro e1 e2 f1 f2
        have hqm1 : 1 ≤ q ^ e2 * m := Nat.mul_pos (pow_pos hq.pos e2) hm1
        have hqn1 : 1 ≤ q ^ f2 * n := Nat.mul_pos (pow_pos hq.pos f2) hn1
        rw [mul_assoc (p ^ e1), mul_assoc (p ^ f1),
          factorization_prime_pow_mul_self_tc062_aux (e := e1) hp hqm1,
          factorization_prime_pow_mul_self_tc062_aux (e := f1) hp hqn1,
          factorization_prime_pow_mul_of_ne_tc062_aux (e := e2) hq hpq.symm hm1,
          factorization_prime_pow_mul_of_ne_tc062_aux (e := f2) hq hpq.symm hn1]
        exact ⟨rfl, rfl⟩
      apply Finset.sum_eq_zero
      intro e1 _
      rw [Finset.sum_comm]
      apply Finset.sum_eq_zero
      intro f1 _
      have h_pair :
          ∀ e2 f2 : ℕ,
            min ((p ^ e1 * q ^ e2 * m).factorization p)
                ((p ^ f1 * q ^ f2 * n).factorization p) =
              min (e1 + m.factorization p) (f1 + n.factorization p) := by
        intro e2 f2
        rw [(h_indep e1 e2 f1 f2).1, (h_indep e1 e2 f1 f2).2]
      simp_rw [h_pair]
      simp_rw [Finset.sum_insert (by decide : (0 : ℕ) ∉ ({1} : Finset ℕ)),
        Finset.sum_singleton]
      simp only [zero_add, add_zero]
      rw [show e1 + 1 + f1 = e1 + f1 + 1 by omega,
        show e1 + f1 + 1 + 1 = e1 + f1 + 2 by omega, pow_add, pow_add]
      norm_num
      ring
    · by_cases hrq : r = q
      · rw [hrq]
        have h_indep :
            ∀ e1 e2 f1 f2 : ℕ,
              (p ^ e1 * q ^ e2 * m).factorization q = e2 + m.factorization q ∧
                (p ^ f1 * q ^ f2 * n).factorization q = f2 + n.factorization q := by
          intro e1 e2 f1 f2
          have h_qm : p ^ e1 * q ^ e2 * m = q ^ e2 * (p ^ e1 * m) := by ring
          have h_qn : p ^ f1 * q ^ f2 * n = q ^ f2 * (p ^ f1 * n) := by ring
          have hpm1 : 1 ≤ p ^ e1 * m := Nat.mul_pos (pow_pos hp.pos e1) hm1
          have hpn1 : 1 ≤ p ^ f1 * n := Nat.mul_pos (pow_pos hp.pos f1) hn1
          rw [h_qm, h_qn,
            factorization_prime_pow_mul_self_tc062_aux (e := e2) hq hpm1,
            factorization_prime_pow_mul_self_tc062_aux (e := f2) hq hpn1,
            factorization_prime_pow_mul_of_ne_tc062_aux (e := e1) hp hpq hm1,
            factorization_prime_pow_mul_of_ne_tc062_aux (e := f1) hp hpq hn1]
          exact ⟨rfl, rfl⟩
        rw [Finset.sum_comm]
        apply Finset.sum_eq_zero
        intro e2 _
        have h_comm_inner :
            (∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ f1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
                (-1 : ℝ) ^ (e1 + e2 + f1 + f2) *
                  (((min ((p ^ e1 * q ^ e2 * m).factorization q)
                      ((p ^ f1 * q ^ f2 * n).factorization q) : ℕ) : ℝ) *
                    (Real.log (q : ℝ)) ^ 2)) =
              ∑ f2 ∈ ({0, 1} : Finset ℕ), ∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ f1 ∈ ({0, 1} : Finset ℕ),
                (-1 : ℝ) ^ (e1 + e2 + f1 + f2) *
                  (((min (e2 + m.factorization q) (f2 + n.factorization q) : ℕ) : ℝ) *
                    (Real.log (q : ℝ)) ^ 2) := by
          have h_pair :
              ∀ e1 f1 f2 : ℕ,
                min ((p ^ e1 * q ^ e2 * m).factorization q)
                    ((p ^ f1 * q ^ f2 * n).factorization q) =
                  min (e2 + m.factorization q) (f2 + n.factorization q) := by
            intro e1 f1 f2
            rw [(h_indep e1 e2 f1 f2).1, (h_indep e1 e2 f1 f2).2]
          simp_rw [h_pair]
          trans (∑ e1 ∈ ({0, 1} : Finset ℕ), ∑ f2 ∈ ({0, 1} : Finset ℕ),
            ∑ f1 ∈ ({0, 1} : Finset ℕ),
              (-1 : ℝ) ^ (e1 + e2 + f1 + f2) *
                (((min (e2 + m.factorization q) (f2 + n.factorization q) : ℕ) : ℝ) *
                  (Real.log (q : ℝ)) ^ 2))
          · apply Finset.sum_congr rfl; intro e1 _; exact Finset.sum_comm
          · exact Finset.sum_comm
        rw [h_comm_inner]
        apply Finset.sum_eq_zero
        intro f2 _
        simp_rw [Finset.sum_insert (by decide : (0 : ℕ) ∉ ({1} : Finset ℕ)),
          Finset.sum_singleton]
        simp only [zero_add, add_zero]
        rw [show e2 + 1 + f2 = e2 + f2 + 1 by omega,
          show 1 + e2 + f2 = e2 + f2 + 1 by omega,
          show 1 + e2 + 1 + f2 = e2 + f2 + 2 by omega, pow_add, pow_add]
        norm_num
        ring
      · have h_indep :
            ∀ e1 e2 f1 f2 : ℕ,
              (p ^ e1 * q ^ e2 * m).factorization r = m.factorization r ∧
                (p ^ f1 * q ^ f2 * n).factorization r = n.factorization r := by
          intro e1 e2 f1 f2
          have hqm1 : 1 ≤ q ^ e2 * m := Nat.mul_pos (pow_pos hq.pos e2) hm1
          have hqn1 : 1 ≤ q ^ f2 * n := Nat.mul_pos (pow_pos hq.pos f2) hn1
          rw [mul_assoc (p ^ e1), mul_assoc (p ^ f1),
            factorization_prime_pow_mul_of_ne_tc062_aux (e := e1) hp (Ne.symm hrp) hqm1,
            factorization_prime_pow_mul_of_ne_tc062_aux (e := f1) hp (Ne.symm hrp) hqn1,
            factorization_prime_pow_mul_of_ne_tc062_aux (e := e2) hq (Ne.symm hrq) hm1,
            factorization_prime_pow_mul_of_ne_tc062_aux (e := f2) hq (Ne.symm hrq) hn1]
          exact ⟨rfl, rfl⟩
        have h_const :
            ∀ e1 e2 f1 f2 : ℕ,
              min ((p ^ e1 * q ^ e2 * m).factorization r)
                  ((p ^ f1 * q ^ f2 * n).factorization r) =
                min (m.factorization r) (n.factorization r) := by
          intro e1 e2 f1 f2
          rw [(h_indep e1 e2 f1 f2).1, (h_indep e1 e2 f1 f2).2]
        simp_rw [h_const]
        apply Finset.sum_eq_zero; intro e1 _
        apply Finset.sum_eq_zero; intro e2 _
        apply Finset.sum_eq_zero; intro f1 _
        rw [h01, Finset.sum_insert (by decide), Finset.sum_singleton]
        rw [add_zero, pow_succ]
        ring
  refine ⟨⟨h_uniq_pq, h_coinc⟩, ⟨h_reidx_16_clean, h_F_16, ?_⟩, ⟨h_annih, ?_⟩⟩
  · intro Y hY2
    have hT_can : 1 ≤ canonicalCutoffT Y := canonicalCutoffT_ge_one_tc062_aux (by linarith)
    exact h_F_16 hY2 hT_can (Nat.floor (Real.log Y))
      actualSelbergConstantCLam actualSquarePoleConstantCHalf
  · intro N m hm n hn
    have hm1 : 1 ≤ m := (Finset.mem_Icc.mp (Finset.mem_filter.mp hm).1).1
    have hn1 : 1 ≤ n := (Finset.mem_Icc.mp (Finset.mem_filter.mp hn).1).1
    exact h_annih hm1 hn1

/-! ### Section 3: Whole-Line Contraction Ratios & Submultiplicativity Refutation (`TASK-TC-062` §5) -/

/-- Exact positive whole-line Gaussian Gram constant
    `wholeLineConstantCG := 3 * sqrt(RiemannScope.tau / 2) / 8`. -/
noncomputable def wholeLineConstantCG : ℝ :=
  3 * Real.sqrt (RiemannScope.tau / 2) / 8

/-- Whole-line scale-invariant Gaussian Gram matrix entry
    `wholeLineConstantCG * ((m * n)^2 / (m^2 + n^2)^(5/2))`. -/
noncomputable def wholeLineGaussianGram (m n : ℕ) : ℝ :=
  wholeLineConstantCG * (((m * n : ℝ) ^ 2) / (((m : ℝ) ^ 2 + (n : ℝ) ^ 2) ^ (5 / 2 : ℝ)))

/-- Finite prime product `∏_{p ∈ S} p`. -/
def primeProductP (S : Finset ℕ) : ℕ :=
  ∏ p ∈ S, p

/-- Whole-line signed profile norm squared over divisors of `primeProductP S`. -/
noncomputable def wholeLineSignedProfileNormSq (S : Finset ℕ) : ℝ :=
  ∑ d1 ∈ (primeProductP S).divisors,
    ∑ d2 ∈ (primeProductP S).divisors,
      (liouvilleLambda d1 : ℝ) * (liouvilleLambda d2 : ℝ) * wholeLineGaussianGram d1 d2

/-- Whole-line diagonal sum norm squared over divisors of `primeProductP S`. -/
noncomputable def wholeLineDiagSumNormSq (S : Finset ℕ) : ℝ :=
  ∑ d ∈ (primeProductP S).divisors, wholeLineGaussianGram d d

/-- Whole-line finite-prime contraction ratio `R(S)`. -/
noncomputable def wholeLineContractionRatioR (S : Finset ℕ) : ℝ :=
  wholeLineSignedProfileNormSq S / wholeLineDiagSumNormSq S

private theorem rpow_five_halves_eq_sq_mul_sqrt_tc062_aux {x : ℝ} (hx : 0 ≤ x) :
    x ^ (5 / 2 : ℝ) = x ^ 2 * Real.sqrt x := by
  rcases eq_or_lt_of_le hx with rfl | hx_pos
  · norm_num
  · rw [Real.sqrt_eq_rpow, ← Real.rpow_natCast x 2, ← Real.rpow_add hx_pos]
    norm_num

private theorem inv_sqrt_rational_enclosure_tc062_aux {k a b Q : ℝ}
    (hk : 0 < k) (ha : 0 ≤ a) (hb : 0 < b) (hQ : 0 < Q)
    (h_lo : k * a ^ 2 ≤ Q ^ 2) (h_hi : Q ^ 2 ≤ k * b ^ 2) :
    a / Q ≤ 1 / Real.sqrt k ∧ 1 / Real.sqrt k ≤ b / Q := by
  have hsk_pos : 0 < Real.sqrt k := Real.sqrt_pos.mpr hk
  have hsk_sq : (Real.sqrt k) ^ 2 = k := Real.sq_sqrt (le_of_lt hk)
  constructor
  · rw [div_le_div_iff hQ hsk_pos, one_mul]
    have hsq : (a * Real.sqrt k) ^ 2 ≤ Q ^ 2 := by
      calc
        (a * Real.sqrt k) ^ 2 = k * a ^ 2 := by rw [mul_pow, hsk_sq]; ring
        _ ≤ Q ^ 2 := h_lo
    nlinarith [sq_nonneg (Q - a * Real.sqrt k), mul_nonneg ha (le_of_lt hsk_pos)]
  · rw [div_le_div_iff hsk_pos hQ, one_mul]
    have hsq : Q ^ 2 ≤ (Real.sqrt k * b) ^ 2 := by
      calc
        Q ^ 2 ≤ k * b ^ 2 := h_hi
        _ = (Real.sqrt k * b) ^ 2 := by rw [mul_pow, hsk_sq]
    nlinarith [sq_nonneg (Real.sqrt k * b - Q), mul_pos hsk_pos hb]

private theorem wholeLineGaussianGram_eq_unit_tc062_aux {d1 d2 g r1 r2 : ℕ}
    (hg : 0 < g) (h1 : d1 = g * r1) (h2 : d2 = g * r2) :
    wholeLineGaussianGram d1 d2 =
      wholeLineConstantCG *
        (((r1 * r2 : ℝ) ^ 2 / ((g : ℝ) * (((r1 : ℝ) ^ 2 + (r2 : ℝ) ^ 2) ^ 2))) *
          (1 / Real.sqrt ((r1 : ℝ) ^ 2 + (r2 : ℝ) ^ 2))) := by
  subst h1; subst h2
  have hg_pos : (0 : ℝ) < (g : ℝ) := Nat.cast_pos.mpr hg
  have hg_ne : (g : ℝ) ≠ 0 := ne_of_gt hg_pos
  have h_sum_nn : 0 ≤ ((g * r1 : ℕ) : ℝ) ^ 2 + ((g * r2 : ℕ) : ℝ) ^ 2 := by positivity
  unfold wholeLineGaussianGram
  rw [rpow_five_halves_eq_sq_mul_sqrt_tc062_aux h_sum_nn]
  have h_sum_factor :
      ((g * r1 : ℕ) : ℝ) ^ 2 + ((g * r2 : ℕ) : ℝ) ^ 2 =
        (g : ℝ) ^ 2 * ((r1 : ℝ) ^ 2 + (r2 : ℝ) ^ 2) := by
    push_cast; ring
  have h_sqrt_factor :
      Real.sqrt (((g * r1 : ℕ) : ℝ) ^ 2 + ((g * r2 : ℕ) : ℝ) ^ 2) =
        (g : ℝ) * Real.sqrt ((r1 : ℝ) ^ 2 + (r2 : ℝ) ^ 2) := by
    rw [h_sum_factor, Real.sqrt_mul (sq_nonneg _), Real.sqrt_sq (le_of_lt hg_pos)]
  rw [h_sqrt_factor, h_sum_factor]
  push_cast
  by_cases hrs : (r1 : ℝ) ^ 2 + (r2 : ℝ) ^ 2 = 0
  · have hr1_0 : (r1 : ℝ) = 0 := by nlinarith [sq_nonneg (r1 : ℝ), sq_nonneg (r2 : ℝ)]
    simp [hr1_0]
  · have hsqrt_ne : Real.sqrt ((r1 : ℝ) ^ 2 + (r2 : ℝ) ^ 2) ≠ 0 :=
      ne_of_gt (Real.sqrt_pos.mpr (lt_of_le_of_ne (by positivity) (Ne.symm hrs)))
    field_simp [hg_ne, hrs, hsqrt_ne]
    ring

private theorem wholeLineGaussianGram_eval_tc062_aux {d1 d2 g r1 r2 : ℕ} {c k : ℝ}
    (hg : 0 < g) (h1 : d1 = g * r1) (h2 : d2 = g * r2)
    (hk : (r1 : ℝ) ^ 2 + (r2 : ℝ) ^ 2 = k)
    (hc : (r1 * r2 : ℝ) ^ 2 / ((g : ℝ) * k ^ 2) = c) :
    wholeLineGaussianGram d1 d2 = wholeLineConstantCG * (c * (1 / Real.sqrt k)) := by
  rw [wholeLineGaussianGram_eq_unit_tc062_aux hg h1 h2, hk, hc]

/-- **Theorem 4 (`TASK-TC-062` §5 / `TASK-TC-062R` §7C, Certified `10^(-12)` Enclosures of Whole-Line Contraction Ratios `R({2}), R({3}), R({2, 3}), R({2, 3, 5})`, Product `R({2}) * R({3})`, and Strict Submultiplicativity & Monotonicity Refutation)**:
    *Scope note (`TASK-TC-062R` §7C)*: `wholeLineGaussianGram`, `wholeLineSignedProfileNormSq`,
    `wholeLineDiagSumNormSq`, and `wholeLineContractionRatioR` are algebraic closed-form
    definitions in Lean (`CONCRETE_ANALYTIC_IN_LEAN`), while the improper half-line
    Gaussian/Gamma integral identification
    `integral_{0..infty} phi_m(X) phi_n(X) dX/X = wholeLineGaussianGram m n` via
    `(d/dX)(-((2*a*X^3 + 3*X)/(4*a^2)) * exp(-a*X^2)) = (X^4 - 3/(4*a^2)) * exp(-a*X^2)`
    at `a = m^(-2) + n^(-2)` is proved analytically outside Lean (`ANALYTIC_PROVED_OUTSIDE_LEAN`).
    1. Exact algebraic `5/2`-power square-times-square-root identity (`(m^2 + n^2)^(5/2) = (m^2 + n^2)^2 * sqrt(m^2 + n^2)`) and positivity `0 < wholeLineConstantCG`;
    2. Certified `10^(-12)` rational interval enclosures for `R({2})`, `R({3})`, `R({2, 3})`, `R({2, 3, 5})`, and `R({2}) * R({3})`;
    3. Strict ordering `R({2}) * R({3}) < R({2}) < R({2, 3}) < R({2, 3, 5})`, refuting both submultiplicativity `R(S ∪ T) ≤ R(S) R(T)` and prime-set monotonicity `R(S ∪ {q}) ≤ R(S)`. -/
theorem whole_line_contraction_enclosures_and_submultiplicativity_refutation_tc062 :
    (0 < wholeLineConstantCG ∧
      ∀ m n : ℕ,
        (((m : ℝ) ^ 2 + (n : ℝ) ^ 2) ^ (5 / 2 : ℝ)) =
          ((m : ℝ) ^ 2 + (n : ℝ) ^ 2) ^ 2 * Real.sqrt ((m : ℝ) ^ 2 + (n : ℝ) ^ 2)) ∧
    ((460304612664 / (10 : ℝ) ^ 12 ≤ wholeLineContractionRatioR {2} ∧
        wholeLineContractionRatioR {2} ≤ 460304612665 / (10 : ℝ) ^ 12) ∧
      (758504658430 / (10 : ℝ) ^ 12 ≤ wholeLineContractionRatioR {3} ∧
        wholeLineContractionRatioR {3} ≤ 758504658431 / (10 : ℝ) ^ 12) ∧
      (577474326597 / (10 : ℝ) ^ 12 ≤ wholeLineContractionRatioR {2, 3} ∧
        wholeLineContractionRatioR {2, 3} ≤ 577474326598 / (10 : ℝ) ^ 12) ∧
      (706402204851 / (10 : ℝ) ^ 12 ≤ wholeLineContractionRatioR {2, 3, 5} ∧
        wholeLineContractionRatioR {2, 3, 5} ≤ 706402204852 / (10 : ℝ) ^ 12) ∧
      (349143193002 / (10 : ℝ) ^ 12 ≤
          wholeLineContractionRatioR {2} * wholeLineContractionRatioR {3} ∧
        wholeLineContractionRatioR {2} * wholeLineContractionRatioR {3} ≤
          349143193003 / (10 : ℝ) ^ 12)) ∧
    (wholeLineContractionRatioR {2} * wholeLineContractionRatioR {3} <
        wholeLineContractionRatioR {2} ∧
      wholeLineContractionRatioR {2} < wholeLineContractionRatioR {2, 3} ∧
      wholeLineContractionRatioR {2, 3} < wholeLineContractionRatioR {2, 3, 5}) := by
  have hCG_pos : 0 < wholeLineConstantCG := by
    unfold wholeLineConstantCG
    exact div_pos
      (mul_pos (by norm_num) (Real.sqrt_pos.mpr (div_pos RiemannScope.tau_pos (by norm_num))))
      (by norm_num)
  have hCG_ne : wholeLineConstantCG ≠ 0 := ne_of_gt hCG_pos
  have h52 : ∀ m n : ℕ,
      (((m : ℝ) ^ 2 + (n : ℝ) ^ 2) ^ (5 / 2 : ℝ)) =
        ((m : ℝ) ^ 2 + (n : ℝ) ^ 2) ^ 2 * Real.sqrt ((m : ℝ) ^ 2 + (n : ℝ) ^ 2) :=
    fun m n => rpow_five_halves_eq_sq_mul_sqrt_tc062_aux (by positivity)
  let Q : ℝ := 10000000000000000
  have hQ_pos : 0 < Q := by dsimp [Q]; norm_num
  have hs2 := inv_sqrt_rational_enclosure_tc062_aux (k := 2)
    (a := 7071067811865475) (b := 7071067811865476) (Q := Q)
    (by norm_num) (by norm_num) (by norm_num) hQ_pos (by dsimp [Q]; norm_num) (by dsimp [Q]; norm_num)
  have hs5 := inv_sqrt_rational_enclosure_tc062_aux (k := 5)
    (a := 4472135954999579) (b := 4472135954999580) (Q := Q)
    (by norm_num) (by norm_num) (by norm_num) hQ_pos (by dsimp [Q]; norm_num) (by dsimp [Q]; norm_num)
  have hs10 := inv_sqrt_rational_enclosure_tc062_aux (k := 10)
    (a := 3162277660168379) (b := 3162277660168380) (Q := Q)
    (by norm_num) (by norm_num) (by norm_num) hQ_pos (by dsimp [Q]; norm_num) (by dsimp [Q]; norm_num)
  have hs13 := inv_sqrt_rational_enclosure_tc062_aux (k := 13)
    (a := 2773500981126145) (b := 2773500981126146) (Q := Q)
    (by norm_num) (by norm_num) (by norm_num) hQ_pos (by dsimp [Q]; norm_num) (by dsimp [Q]; norm_num)
  have hs26 := inv_sqrt_rational_enclosure_tc062_aux (k := 26)
    (a := 1961161351381840) (b := 1961161351381841) (Q := Q)
    (by norm_num) (by norm_num) (by norm_num) hQ_pos (by dsimp [Q]; norm_num) (by dsimp [Q]; norm_num)
  have hs29 := inv_sqrt_rational_enclosure_tc062_aux (k := 29)
    (a := 1856953381770518) (b := 1856953381770519) (Q := Q)
    (by norm_num) (by norm_num) (by norm_num) hQ_pos (by dsimp [Q]; norm_num) (by dsimp [Q]; norm_num)
  have hs34 := inv_sqrt_rational_enclosure_tc062_aux (k := 34)
    (a := 1714985851425088) (b := 1714985851425089) (Q := Q)
    (by norm_num) (by norm_num) (by norm_num) hQ_pos (by dsimp [Q]; norm_num) (by dsimp [Q]; norm_num)
  have hs37 := inv_sqrt_rational_enclosure_tc062_aux (k := 37)
    (a := 1643989873053572) (b := 1643989873053573) (Q := Q)
    (by norm_num) (by norm_num) (by norm_num) hQ_pos (by dsimp [Q]; norm_num) (by dsimp [Q]; norm_num)
  have hs61 := inv_sqrt_rational_enclosure_tc062_aux (k := 61)
    (a := 1280368799328959) (b := 1280368799328960) (Q := Q)
    (by norm_num) (by norm_num) (by norm_num) hQ_pos (by dsimp [Q]; norm_num) (by dsimp [Q]; norm_num)
  have hs101 := inv_sqrt_rational_enclosure_tc062_aux (k := 101)
    (a := 995037190209989) (b := 995037190209990) (Q := Q)
    (by norm_num) (by norm_num) (by norm_num) hQ_pos (by dsimp [Q]; norm_num) (by dsimp [Q]; norm_num)
  have hs109 := inv_sqrt_rational_enclosure_tc062_aux (k := 109)
    (a := 957826285221151) (b := 957826285221152) (Q := Q)
    (by norm_num) (by norm_num) (by norm_num) hQ_pos (by dsimp [Q]; norm_num) (by dsimp [Q]; norm_num)
  have hs226 := inv_sqrt_rational_enclosure_tc062_aux (k := 226)
    (a := 665190105237739) (b := 665190105237740) (Q := Q)
    (by norm_num) (by norm_num) (by norm_num) hQ_pos (by dsimp [Q]; norm_num) (by dsimp [Q]; norm_num)
  have hs229 := inv_sqrt_rational_enclosure_tc062_aux (k := 229)
    (a := 660818600455089) (b := 660818600455090) (Q := Q)
    (by norm_num) (by norm_num) (by norm_num) hQ_pos (by dsimp [Q]; norm_num) (by dsimp [Q]; norm_num)
  have hs901 := inv_sqrt_rational_enclosure_tc062_aux (k := 901)
    (a := 333148302326384) (b := 333148302326385) (Q := Q)
    (by norm_num) (by norm_num) (by norm_num) hQ_pos (by dsimp [Q]; norm_num) (by dsimp [Q]; norm_num)
  have hl1 : (liouvilleLambda 1 : ℝ) = 1 := by simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
  have hl2 : (liouvilleLambda 2 : ℝ) = -1 := liouvilleLambda_prime_real_tc062_aux Nat.prime_two
  have hl3 : (liouvilleLambda 3 : ℝ) = -1 := liouvilleLambda_prime_real_tc062_aux Nat.prime_three
  have hl5 : (liouvilleLambda 5 : ℝ) = -1 :=
    liouvilleLambda_prime_real_tc062_aux (by decide : Nat.Prime 5)
  have hl6 : (liouvilleLambda 6 : ℝ) = 1 := by
    rw [show (6 : ℕ) = 2 * 3 from rfl, liouvilleLambda_mul_pos_tc062_aux (by decide) (by decide),
      hl2, hl3]; ring
  have hl10 : (liouvilleLambda 10 : ℝ) = 1 := by
    rw [show (10 : ℕ) = 2 * 5 from rfl, liouvilleLambda_mul_pos_tc062_aux (by decide) (by decide),
      hl2, hl5]; ring
  have hl15 : (liouvilleLambda 15 : ℝ) = 1 := by
    rw [show (15 : ℕ) = 3 * 5 from rfl, liouvilleLambda_mul_pos_tc062_aux (by decide) (by decide),
      hl3, hl5]; ring
  have hl30 : (liouvilleLambda 30 : ℝ) = -1 := by
    rw [show (30 : ℕ) = 2 * 15 from rfl, liouvilleLambda_mul_pos_tc062_aux (by decide) (by decide),
      hl2, hl15]; ring
  have h_g_diag : ∀ d : ℕ, 0 < d →
      wholeLineGaussianGram d d =
        wholeLineConstantCG * ((1 / (4 * (d : ℝ))) * (1 / Real.sqrt 2)) := by
    intro d hd
    rw [wholeLineGaussianGram_eq_unit_tc062_aux hd (show d = d * 1 by omega)
      (show d = d * 1 by omega)]
    congr 1; push_cast; norm_num; ring
  have h_g_symm : ∀ d1 d2 : ℕ, wholeLineGaussianGram d1 d2 = wholeLineGaussianGram d2 d1 := by
    intro d1 d2; unfold wholeLineGaussianGram; ring_nf
  have hg12 := wholeLineGaussianGram_eval_tc062_aux (d1 := 1) (d2 := 2) (g := 1) (r1 := 1) (r2 := 2) (c := 4 / 25) (k := 5) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg13 := wholeLineGaussianGram_eval_tc062_aux (d1 := 1) (d2 := 3) (g := 1) (r1 := 1) (r2 := 3) (c := 9 / 100) (k := 10) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg15 := wholeLineGaussianGram_eval_tc062_aux (d1 := 1) (d2 := 5) (g := 1) (r1 := 1) (r2 := 5) (c := 25 / 676) (k := 26) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg16 := wholeLineGaussianGram_eval_tc062_aux (d1 := 1) (d2 := 6) (g := 1) (r1 := 1) (r2 := 6) (c := 36 / 1369) (k := 37) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg1_10 := wholeLineGaussianGram_eval_tc062_aux (d1 := 1) (d2 := 10) (g := 1) (r1 := 1) (r2 := 10) (c := 100 / 10201) (k := 101) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg1_15 := wholeLineGaussianGram_eval_tc062_aux (d1 := 1) (d2 := 15) (g := 1) (r1 := 1) (r2 := 15) (c := 225 / 51076) (k := 226) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg1_30 := wholeLineGaussianGram_eval_tc062_aux (d1 := 1) (d2 := 30) (g := 1) (r1 := 1) (r2 := 30) (c := 900 / 811801) (k := 901) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg23 := wholeLineGaussianGram_eval_tc062_aux (d1 := 2) (d2 := 3) (g := 1) (r1 := 2) (r2 := 3) (c := 36 / 169) (k := 13) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg25 := wholeLineGaussianGram_eval_tc062_aux (d1 := 2) (d2 := 5) (g := 1) (r1 := 2) (r2 := 5) (c := 100 / 841) (k := 29) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg2_15 := wholeLineGaussianGram_eval_tc062_aux (d1 := 2) (d2 := 15) (g := 1) (r1 := 2) (r2 := 15) (c := 900 / 52441) (k := 229) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg35 := wholeLineGaussianGram_eval_tc062_aux (d1 := 3) (d2 := 5) (g := 1) (r1 := 3) (r2 := 5) (c := 225 / 1156) (k := 34) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg3_10 := wholeLineGaussianGram_eval_tc062_aux (d1 := 3) (d2 := 10) (g := 1) (r1 := 3) (r2 := 10) (c := 900 / 11881) (k := 109) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg56 := wholeLineGaussianGram_eval_tc062_aux (d1 := 5) (d2 := 6) (g := 1) (r1 := 5) (r2 := 6) (c := 900 / 3721) (k := 61) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg2_6 := wholeLineGaussianGram_eval_tc062_aux (d1 := 2) (d2 := 6) (g := 2) (r1 := 1) (r2 := 3) (c := 9 / 200) (k := 10) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg2_10 := wholeLineGaussianGram_eval_tc062_aux (d1 := 2) (d2 := 10) (g := 2) (r1 := 1) (r2 := 5) (c := 25 / 1352) (k := 26) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg2_30 := wholeLineGaussianGram_eval_tc062_aux (d1 := 2) (d2 := 30) (g := 2) (r1 := 1) (r2 := 15) (c := 225 / 102152) (k := 226) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg3_6 := wholeLineGaussianGram_eval_tc062_aux (d1 := 3) (d2 := 6) (g := 3) (r1 := 1) (r2 := 2) (c := 4 / 75) (k := 5) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg3_15 := wholeLineGaussianGram_eval_tc062_aux (d1 := 3) (d2 := 15) (g := 3) (r1 := 1) (r2 := 5) (c := 25 / 2028) (k := 26) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg3_30 := wholeLineGaussianGram_eval_tc062_aux (d1 := 3) (d2 := 30) (g := 3) (r1 := 1) (r2 := 10) (c := 100 / 30603) (k := 101) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg5_10 := wholeLineGaussianGram_eval_tc062_aux (d1 := 5) (d2 := 10) (g := 5) (r1 := 1) (r2 := 2) (c := 4 / 125) (k := 5) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg5_15 := wholeLineGaussianGram_eval_tc062_aux (d1 := 5) (d2 := 15) (g := 5) (r1 := 1) (r2 := 3) (c := 9 / 500) (k := 10) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg5_30 := wholeLineGaussianGram_eval_tc062_aux (d1 := 5) (d2 := 30) (g := 5) (r1 := 1) (r2 := 6) (c := 36 / 6845) (k := 37) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg6_10 := wholeLineGaussianGram_eval_tc062_aux (d1 := 6) (d2 := 10) (g := 2) (r1 := 3) (r2 := 5) (c := 225 / 2312) (k := 34) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg6_15 := wholeLineGaussianGram_eval_tc062_aux (d1 := 6) (d2 := 15) (g := 3) (r1 := 2) (r2 := 5) (c := 100 / 2523) (k := 29) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg6_30 := wholeLineGaussianGram_eval_tc062_aux (d1 := 6) (d2 := 30) (g := 6) (r1 := 1) (r2 := 5) (c := 25 / 4056) (k := 26) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg10_15 := wholeLineGaussianGram_eval_tc062_aux (d1 := 10) (d2 := 15) (g := 5) (r1 := 2) (r2 := 3) (c := 36 / 845) (k := 13) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg10_30 := wholeLineGaussianGram_eval_tc062_aux (d1 := 10) (d2 := 30) (g := 10) (r1 := 1) (r2 := 3) (c := 9 / 1000) (k := 10) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  have hg15_30 := wholeLineGaussianGram_eval_tc062_aux (d1 := 15) (d2 := 30) (g := 15) (r1 := 1) (r2 := 2) (c := 4 / 375) (k := 5) (by decide) (by decide) (by decide) (by norm_num) (by norm_num)
  -- 1. Enclosure for R({2}) to 10^(-14)
  dsimp [Q] at hs2 hs5 hs10 hs13 hs26 hs29 hs34 hs37 hs61 hs101 hs109 hs226 hs229 hs901
  have hR2_14 :
      46030461266459 / (100000000000000 : ℝ) ≤ wholeLineContractionRatioR {2} ∧
        wholeLineContractionRatioR {2} ≤ 46030461266460 / (100000000000000 : ℝ) := by
    have hdiv2 : (primeProductP {2}).divisors = {1, 2} := by decide
    have hd1 := h_g_diag 1 (by decide)
    have hd2 := h_g_diag 2 (by decide)
    have h21 := h_g_symm 2 1
    have h_num_eq :
        wholeLineSignedProfileNormSq {2} =
          wholeLineConstantCG *
            ((3 / 8 : ℝ) * (1 / Real.sqrt 2) - (8 / 25 : ℝ) * (1 / Real.sqrt 5)) := by
      unfold wholeLineSignedProfileNormSq
      rw [hdiv2]
      simp only [Finset.sum_insert (by decide : (1 : ℕ) ∉ ({2} : Finset ℕ)), Finset.sum_singleton]
      rw [hl1, hl2, h21, hd1, hd2, hg12]
      ring
    have h_den_eq :
        wholeLineDiagSumNormSq {2} =
          wholeLineConstantCG * ((3 / 8 : ℝ) * (1 / Real.sqrt 2)) := by
      unfold wholeLineDiagSumNormSq
      rw [hdiv2]
      simp only [Finset.sum_insert (by decide : (1 : ℕ) ∉ ({2} : Finset ℕ)), Finset.sum_singleton]
      rw [hd1, hd2]
      ring
    unfold wholeLineContractionRatioR
    rw [h_num_eq, h_den_eq, mul_div_mul_left _ _ hCG_ne]
    have h_den_pos : 0 < (3 / 8 : ℝ) * (1 / Real.sqrt 2) := by positivity
    constructor
    · rw [div_le_div_iff (by norm_num) h_den_pos]
      linarith only [hs2.1, hs2.2, hs5.1, hs5.2]
    · rw [div_le_div_iff h_den_pos (by norm_num)]
      linarith only [hs2.1, hs2.2, hs5.1, hs5.2]
  -- 2. Enclosure for R({3}) to 10^(-14)
  have hR3_14 :
      75850465843002 / (100000000000000 : ℝ) ≤ wholeLineContractionRatioR {3} ∧
        wholeLineContractionRatioR {3} ≤ 75850465843003 / (100000000000000 : ℝ) := by
    have hdiv3 : (primeProductP {3}).divisors = {1, 3} := by decide
    have hd1 := h_g_diag 1 (by decide)
    have hd3 := h_g_diag 3 (by decide)
    have h31 := h_g_symm 3 1
    have h_num_eq :
        wholeLineSignedProfileNormSq {3} =
          wholeLineConstantCG *
            ((1 / 3 : ℝ) * (1 / Real.sqrt 2) - (9 / 50 : ℝ) * (1 / Real.sqrt 10)) := by
      unfold wholeLineSignedProfileNormSq
      rw [hdiv3]
      simp only [Finset.sum_insert (by decide : (1 : ℕ) ∉ ({3} : Finset ℕ)), Finset.sum_singleton]
      rw [hl1, hl3, h31, hd1, hd3, hg13]
      ring
    have h_den_eq :
        wholeLineDiagSumNormSq {3} =
          wholeLineConstantCG * ((1 / 3 : ℝ) * (1 / Real.sqrt 2)) := by
      unfold wholeLineDiagSumNormSq
      rw [hdiv3]
      simp only [Finset.sum_insert (by decide : (1 : ℕ) ∉ ({3} : Finset ℕ)), Finset.sum_singleton]
      rw [hd1, hd3]
      ring
    unfold wholeLineContractionRatioR
    rw [h_num_eq, h_den_eq, mul_div_mul_left _ _ hCG_ne]
    have h_den_pos : 0 < (1 / 3 : ℝ) * (1 / Real.sqrt 2) := by positivity
    constructor
    · rw [div_le_div_iff (by norm_num) h_den_pos]
      linarith only [hs2.1, hs2.2, hs10.1, hs10.2]
    · rw [div_le_div_iff h_den_pos (by norm_num)]
      linarith only [hs2.1, hs2.2, hs10.1, hs10.2]
  -- 3. Enclosure for R({2, 3}) to 10^(-12)
  have h10_12 : (10 : ℝ) ^ 12 = 1000000000000 := by norm_num
  have hR23 :
      577474326597 / (10 : ℝ) ^ 12 ≤ wholeLineContractionRatioR {2, 3} ∧
        wholeLineContractionRatioR {2, 3} ≤ 577474326598 / (10 : ℝ) ^ 12 := by
    have hdiv23 : (primeProductP {2, 3}).divisors = {1, 2, 3, 6} := by decide
    have hd1 := h_g_diag 1 (by decide)
    have hd2 := h_g_diag 2 (by decide)
    have hd3 := h_g_diag 3 (by decide)
    have hd6 := h_g_diag 6 (by decide)
    have h_num_eq :
        wholeLineSignedProfileNormSq {2, 3} =
          wholeLineConstantCG *
            ((1 / 2 : ℝ) * (1 / Real.sqrt 2) -
              (32 / 75 : ℝ) * (1 / Real.sqrt 5) -
              (27 / 100 : ℝ) * (1 / Real.sqrt 10) +
              (72 / 169 : ℝ) * (1 / Real.sqrt 13) +
              (72 / 1369 : ℝ) * (1 / Real.sqrt 37)) := by
      unfold wholeLineSignedProfileNormSq
      rw [hdiv23]
      simp only [Finset.sum_insert (by decide : (1 : ℕ) ∉ ({2, 3, 6} : Finset ℕ)),
        Finset.sum_insert (by decide : (2 : ℕ) ∉ ({3, 6} : Finset ℕ)),
        Finset.sum_insert (by decide : (3 : ℕ) ∉ ({6} : Finset ℕ)),
        Finset.sum_singleton]
      rw [hl1, hl2, hl3, hl6,
        h_g_symm 2 1, h_g_symm 3 1, h_g_symm 6 1,
        h_g_symm 3 2, h_g_symm 6 2, h_g_symm 6 3,
        hd1, hd2, hd3, hd6, hg12, hg13, hg16, hg23, hg2_6, hg3_6]
      ring
    have h_den_eq :
        wholeLineDiagSumNormSq {2, 3} =
          wholeLineConstantCG * ((1 / 2 : ℝ) * (1 / Real.sqrt 2)) := by
      unfold wholeLineDiagSumNormSq
      rw [hdiv23]
      simp only [Finset.sum_insert (by decide : (1 : ℕ) ∉ ({2, 3, 6} : Finset ℕ)),
        Finset.sum_insert (by decide : (2 : ℕ) ∉ ({3, 6} : Finset ℕ)),
        Finset.sum_insert (by decide : (3 : ℕ) ∉ ({6} : Finset ℕ)),
        Finset.sum_singleton]
      rw [hd1, hd2, hd3, hd6]
      ring
    unfold wholeLineContractionRatioR
    rw [h_num_eq, h_den_eq, mul_div_mul_left _ _ hCG_ne, h10_12]
    have h_den_pos : 0 < (1 / 2 : ℝ) * (1 / Real.sqrt 2) := by positivity
    constructor
    · rw [div_le_div_iff (by norm_num) h_den_pos]
      linarith only [hs2.1, hs2.2, hs5.1, hs5.2, hs10.1, hs10.2, hs13.1, hs13.2, hs37.1, hs37.2]
    · rw [div_le_div_iff h_den_pos (by norm_num)]
      linarith only [hs2.1, hs2.2, hs5.1, hs5.2, hs10.1, hs10.2, hs13.1, hs13.2, hs37.1, hs37.2]
  -- 4. Enclosure for R({2, 3, 5}) to 10^(-12)
  have hR235 :
      706402204851 / (10 : ℝ) ^ 12 ≤ wholeLineContractionRatioR {2, 3, 5} ∧
        wholeLineContractionRatioR {2, 3, 5} ≤ 706402204852 / (10 : ℝ) ^ 12 := by
    have hdiv235 : (primeProductP {2, 3, 5}).divisors = {1, 2, 3, 5, 6, 10, 15, 30} := by decide
    have hd1 := h_g_diag 1 (by decide)
    have hd2 := h_g_diag 2 (by decide)
    have hd3 := h_g_diag 3 (by decide)
    have hd5 := h_g_diag 5 (by decide)
    have hd6 := h_g_diag 6 (by decide)
    have hd10 := h_g_diag 10 (by decide)
    have hd15 := h_g_diag 15 (by decide)
    have hd30 := h_g_diag 30 (by decide)
    have h_den_eq :
        wholeLineDiagSumNormSq {2, 3, 5} =
          wholeLineConstantCG * ((3 / 5 : ℝ) * (1 / Real.sqrt 2)) := by
      unfold wholeLineDiagSumNormSq
      rw [hdiv235]
      simp only [
        Finset.sum_insert (by decide : (1 : ℕ) ∉ ({2, 3, 5, 6, 10, 15, 30} : Finset ℕ)),
        Finset.sum_insert (by decide : (2 : ℕ) ∉ ({3, 5, 6, 10, 15, 30} : Finset ℕ)),
        Finset.sum_insert (by decide : (3 : ℕ) ∉ ({5, 6, 10, 15, 30} : Finset ℕ)),
        Finset.sum_insert (by decide : (5 : ℕ) ∉ ({6, 10, 15, 30} : Finset ℕ)),
        Finset.sum_insert (by decide : (6 : ℕ) ∉ ({10, 15, 30} : Finset ℕ)),
        Finset.sum_insert (by decide : (10 : ℕ) ∉ ({15, 30} : Finset ℕ)),
        Finset.sum_insert (by decide : (15 : ℕ) ∉ ({30} : Finset ℕ)),
        Finset.sum_singleton]
      rw [hd1, hd2, hd3, hd5, hd6, hd10, hd15, hd30]
      ring
    have h_num_eq :
        wholeLineSignedProfileNormSq {2, 3, 5} =
          wholeLineConstantCG *
            ((3 / 5 : ℝ) * (1 / Real.sqrt 2) -
              (64 / 125 : ℝ) * (1 / Real.sqrt 5) -
              (81 / 250 : ℝ) * (1 / Real.sqrt 10) +
              (432 / 845 : ℝ) * (1 / Real.sqrt 13) -
              (25 / 169 : ℝ) * (1 / Real.sqrt 26) +
              (800 / 2523 : ℝ) * (1 / Real.sqrt 29) +
              (675 / 1156 : ℝ) * (1 / Real.sqrt 34) +
              (432 / 6845 : ℝ) * (1 / Real.sqrt 37) -
              (1800 / 3721 : ℝ) * (1 / Real.sqrt 61) +
              (800 / 30603 : ℝ) * (1 / Real.sqrt 101) -
              (1800 / 11881 : ℝ) * (1 / Real.sqrt 109) +
              (675 / 51076 : ℝ) * (1 / Real.sqrt 226) -
              (1800 / 52441 : ℝ) * (1 / Real.sqrt 229) -
              (1800 / 811801 : ℝ) * (1 / Real.sqrt 901)) := by
      unfold wholeLineSignedProfileNormSq
      rw [hdiv235]
      simp only [
        Finset.sum_insert (by decide : (1 : ℕ) ∉ ({2, 3, 5, 6, 10, 15, 30} : Finset ℕ)),
        Finset.sum_insert (by decide : (2 : ℕ) ∉ ({3, 5, 6, 10, 15, 30} : Finset ℕ)),
        Finset.sum_insert (by decide : (3 : ℕ) ∉ ({5, 6, 10, 15, 30} : Finset ℕ)),
        Finset.sum_insert (by decide : (5 : ℕ) ∉ ({6, 10, 15, 30} : Finset ℕ)),
        Finset.sum_insert (by decide : (6 : ℕ) ∉ ({10, 15, 30} : Finset ℕ)),
        Finset.sum_insert (by decide : (10 : ℕ) ∉ ({15, 30} : Finset ℕ)),
        Finset.sum_insert (by decide : (15 : ℕ) ∉ ({30} : Finset ℕ)),
        Finset.sum_singleton]
      rw [hl1, hl2, hl3, hl5, hl6, hl10, hl15, hl30,
        h_g_symm 2 1, h_g_symm 3 1, h_g_symm 5 1, h_g_symm 6 1,
        h_g_symm 10 1, h_g_symm 15 1, h_g_symm 30 1,
        h_g_symm 3 2, h_g_symm 5 2, h_g_symm 6 2,
        h_g_symm 10 2, h_g_symm 15 2, h_g_symm 30 2,
        h_g_symm 5 3, h_g_symm 6 3, h_g_symm 10 3, h_g_symm 15 3, h_g_symm 30 3,
        h_g_symm 6 5, h_g_symm 10 5, h_g_symm 15 5, h_g_symm 30 5,
        h_g_symm 10 6, h_g_symm 15 6, h_g_symm 30 6,
        h_g_symm 15 10, h_g_symm 30 10,
        h_g_symm 30 15,
        hd1, hd2, hd3, hd5, hd6, hd10, hd15, hd30,
        hg12, hg13, hg15, hg16, hg1_10, hg1_15, hg1_30,
        hg23, hg25, hg2_6, hg2_10, hg2_15, hg2_30,
        hg35, hg3_6, hg3_10, hg3_15, hg3_30,
        hg56, hg5_10, hg5_15, hg5_30,
        hg6_10, hg6_15, hg6_30,
        hg10_15, hg10_30,
        hg15_30]
      ring
    unfold wholeLineContractionRatioR
    rw [h_num_eq, h_den_eq, mul_div_mul_left _ _ hCG_ne, h10_12]
    have h_den_pos : 0 < (3 / 5 : ℝ) * (1 / Real.sqrt 2) := by positivity
    constructor
    · rw [div_le_div_iff (by norm_num) h_den_pos]
      linarith only [hs2.1, hs2.2, hs5.1, hs5.2, hs10.1, hs10.2, hs13.1, hs13.2,
        hs26.1, hs26.2, hs29.1, hs29.2, hs34.1, hs34.2, hs37.1, hs37.2,
        hs61.1, hs61.2, hs101.1, hs101.2, hs109.1, hs109.2, hs226.1, hs226.2,
        hs229.1, hs229.2, hs901.1, hs901.2]
    · rw [div_le_div_iff h_den_pos (by norm_num)]
      linarith only [hs2.1, hs2.2, hs5.1, hs5.2, hs10.1, hs10.2, hs13.1, hs13.2,
        hs26.1, hs26.2, hs29.1, hs29.2, hs34.1, hs34.2, hs37.1, hs37.2,
        hs61.1, hs61.2, hs101.1, hs101.2, hs109.1, hs109.2, hs226.1, hs226.2,
        hs229.1, hs229.2, hs901.1, hs901.2]
  have hR2 :
      460304612664 / (10 : ℝ) ^ 12 ≤ wholeLineContractionRatioR {2} ∧
        wholeLineContractionRatioR {2} ≤ 460304612665 / (10 : ℝ) ^ 12 := by
    rw [h10_12]
    exact ⟨by linarith only [hR2_14.1], by linarith only [hR2_14.2]⟩
  have hR3 :
      758504658430 / (10 : ℝ) ^ 12 ≤ wholeLineContractionRatioR {3} ∧
        wholeLineContractionRatioR {3} ≤ 758504658431 / (10 : ℝ) ^ 12 := by
    rw [h10_12]
    exact ⟨by linarith only [hR3_14.1], by linarith only [hR3_14.2]⟩
  have hR2R3 :
      349143193002 / (10 : ℝ) ^ 12 ≤
          wholeLineContractionRatioR {2} * wholeLineContractionRatioR {3} ∧
        wholeLineContractionRatioR {2} * wholeLineContractionRatioR {3} ≤
          349143193003 / (10 : ℝ) ^ 12 := by
    have hR2_nn : 0 ≤ wholeLineContractionRatioR {2} := by linarith only [hR2_14.1]
    have hR3_nn : 0 ≤ wholeLineContractionRatioR {3} := by linarith only [hR3_14.1]
    have h_lo_mul :
        (46030461266459 / (100000000000000 : ℝ)) * (75850465843002 / (100000000000000 : ℝ)) ≤
          wholeLineContractionRatioR {2} * wholeLineContractionRatioR {3} :=
      mul_le_mul hR2_14.1 hR3_14.1 (by norm_num) hR2_nn
    have h_hi_mul :
        wholeLineContractionRatioR {2} * wholeLineContractionRatioR {3} ≤
          (46030461266460 / (100000000000000 : ℝ)) * (75850465843003 / (100000000000000 : ℝ)) :=
      mul_le_mul hR2_14.2 hR3_14.2 hR3_nn (by norm_num)
    exact ⟨le_trans (by norm_num) h_lo_mul, le_trans h_hi_mul (by norm_num)⟩
  refine ⟨⟨hCG_pos, h52⟩, ⟨hR2, hR3, hR23, hR235, hR2R3⟩, ?_⟩
  rw [h10_12] at hR2 hR3 hR23 hR235 hR2R3
  exact ⟨by linarith only [hR2R3.2, hR2.1],
    by linarith only [hR2.2, hR23.1],
    by linarith only [hR23.2, hR235.1]⟩

/-! ### Section 4: Spillover Fringe Reindexing, Selberg Bounds, and Truncated Equivalence (`TASK-TC-062` §6) -/

/-- Single-station adjusted profile
    `ψ_{Y, n}(X) := (1 - signedAdjustedCoeffB(n) / (log X)^2) * gaussianTermPhi n X`. -/
noncomputable def adjustedStationProfilePsi (c_lam c_half : ℝ) (T D0 n : ℕ) (X : ℝ) : ℝ :=
  (1 - signedAdjustedCoeffB c_lam c_half T D0 n / (Real.log X) ^ 2) * gaussianTermPhi n X

/-- Primary `[1, T]`-truncated adjusted observable
    `U_{T, D0}(X) := finiteQLambda T X - (∑_{1 ≤ n ≤ T} β_n φ_n(X)) / (log X)^2`. -/
noncomputable def truncatedAdjustedCoreU (c_lam c_half : ℝ) (T D0 : ℕ) (X : ℝ) : ℝ :=
  finiteQLambda T X -
    (∑ n ∈ Finset.Icc 1 T, openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) /
      (Real.log X) ^ 2

/-- Spillover fringe observable supported on `T + 1 ≤ n ≤ 2 * T`:
    `S_{spill, T, D0}(X) := -(∑_{T + 1 ≤ n ≤ 2T} β_n φ_n(X)) / (log X)^2`. -/
noncomputable def spilloverFringeS (c_lam c_half : ℝ) (T D0 : ℕ) (X : ℝ) : ℝ :=
  -(∑ n ∈ Finset.Icc (T + 1) (2 * T),
      openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) /
    (Real.log X) ^ 2

/-- Primary `[1, T]^2`-truncated signed remainder functional. -/
noncomputable def truncatedSignedRemainderF (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ) : ℝ :=
  ∑ m ∈ Finset.Icc 1 T, ∑ n ∈ Finset.Icc 1 T,
    (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
      completeSignedKernelHcal c_lam c_half T D0 Y m n

/-- Canonical-schedule (`T = canonicalCutoffT Y`, `D0 = ⌊log Y⌋`) truncated signed remainder. -/
noncomputable def canonicalTruncatedSignedRemainderF (c_lam c_half : ℝ) (Y : ℝ) : ℝ :=
  truncatedSignedRemainderF c_lam c_half (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y

/-- Canonical-schedule spillover fringe observable. -/
noncomputable def canonicalSpilloverFringeS (c_lam c_half : ℝ) (Y : ℝ) (X : ℝ) : ℝ :=
  spilloverFringeS c_lam c_half (canonicalCutoffT Y) (Nat.floor (Real.log Y)) X

/-- Subset prime-power diagonal quadratic form `Dtilde_{S_sub}(Y)`. -/
noncomputable def subsetPrimePowerDiagDtilde (S_sub : Finset ℕ) (Y : ℝ) : ℝ :=
  ∑ m ∈ S_sub, ∑ n ∈ S_sub,
    (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
      logWeightedWindowKernel 2 Y m n

/-- Subset composite self-collision sum `Xself_{S_sub}(Y)`. -/
noncomputable def subsetPrimePowerSelfCollisionXself (S_sub : Finset ℕ) (Y : ℝ) : ℝ :=
  ∑ n ∈ S_sub, offDiagPrimePowerWeight n n * logWeightedWindowKernel 2 Y n n

private theorem continuousOn_gaussianTermPhi_uIcc_tc062_aux (Y : ℝ) (n : ℕ) :
    ContinuousOn (gaussianTermPhi n) (Set.uIcc Y (RiemannScope.tau * Y)) := by
  unfold gaussianTermPhi
  have hr : ContinuousOn (fun X : ℝ => X ^ (5 / 2 : ℝ))
      (Set.uIcc Y (RiemannScope.tau * Y)) := by
    apply ContinuousOn.rpow_const continuousOn_id
    intro _ _; right; norm_num
  have he : Continuous (fun X : ℝ =>
      (((n : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (n : ℝ) ^ 2))) := by continuity
  exact hr.mul he.continuousOn

private theorem continuousOn_logWeightedKernel_integrand_tc062_aux {Y : ℝ} (hY2 : 2 ≤ Y)
    (ν m n : ℕ) :
    ContinuousOn
      (fun X => (gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ ν) / X)
      (Set.uIcc Y (RiemannScope.tau * Y)) := by
  obtain ⟨_, hprops⟩ := uIcc_tau_props_tc062_aux hY2
  have hlog_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
    ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1)
  exact (((continuousOn_gaussianTermPhi_uIcc_tc062_aux Y m).mul
    (continuousOn_gaussianTermPhi_uIcc_tc062_aux Y n)).div
    (hlog_cont.pow ν) (fun X hX => pow_ne_zero ν (hprops X hX).2.2.2.1)).div
    continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1)

private theorem continuousOn_adjustedStationProfilePsi_tc062_aux {Y : ℝ} (hY2 : 2 ≤ Y)
    (c_lam c_half : ℝ) (T D0 n : ℕ) :
    ContinuousOn (adjustedStationProfilePsi c_lam c_half T D0 n)
      (Set.uIcc Y (RiemannScope.tau * Y)) := by
  obtain ⟨_, hprops⟩ := uIcc_tau_props_tc062_aux hY2
  have hlog_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
    ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1)
  unfold adjustedStationProfilePsi
  exact (continuousOn_const.sub
    (continuousOn_const.div (hlog_cont.pow 2) (fun X hX => (hprops X hX).2.2.2.2))).mul
    (continuousOn_gaussianTermPhi_uIcc_tc062_aux Y n)

private theorem subset_hcal_bilinear_eq_windowNorm_sub_tc062_aux
    {Y : ℝ} (hY2 : 2 ≤ Y) {T : ℕ} (_hT : 1 ≤ T) (D0 : ℕ) (c_lam c_half : ℝ)
    (S_sub : Finset ℕ) (hS_sub : S_sub ⊆ Finset.Icc 1 T) :
    (∑ m ∈ S_sub, ∑ n ∈ S_sub,
      (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
        completeSignedKernelHcal c_lam c_half T D0 Y m n) =
      windowEnergyNormSq Y
        (fun X =>
          ∑ n ∈ S_sub, (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) -
        4 * subsetPrimePowerDiagDtilde S_sub Y -
        4 * subsetPrimePowerSelfCollisionXself S_sub Y := by
  obtain ⟨_, hprops⟩ := uIcc_tau_props_tc062_aux hY2
  have h_psi_gram :
      windowEnergyNormSq Y
          (fun X =>
            ∑ n ∈ S_sub, (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) =
        ∑ m ∈ S_sub, ∑ n ∈ S_sub,
          (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
            (logWeightedWindowKernel 0 Y m n -
              (signedAdjustedCoeffB c_lam c_half T D0 n +
                  signedAdjustedCoeffB c_lam c_half T D0 m) *
                logWeightedWindowKernel 2 Y m n +
              signedAdjustedCoeffB c_lam c_half T D0 m *
                signedAdjustedCoeffB c_lam c_half T D0 n *
                logWeightedWindowKernel 4 Y m n) := by
    have h_pair_cont :
        ∀ m n : ℕ,
          ContinuousOn
            (fun X =>
              ((liouvilleLambda m : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 m X) *
                ((liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) / X)
            (Set.uIcc Y (RiemannScope.tau * Y)) := by
      intro m n
      refine (((continuousOn_const.mul
        (continuousOn_adjustedStationProfilePsi_tc062_aux hY2 c_lam c_half T D0 m)).mul
        (continuousOn_const.mul
          (continuousOn_adjustedStationProfilePsi_tc062_aux hY2 c_lam c_half T D0 n))).div
        continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1))
    unfold windowEnergyNormSq windowPairing
    have h_sq_sum :
        (fun X =>
          (∑ m ∈ S_sub, (liouvilleLambda m : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 m X) *
            (∑ n ∈ S_sub, (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) /
              X) =
          fun X => ∑ m ∈ S_sub, ∑ n ∈ S_sub,
            ((liouvilleLambda m : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 m X) *
              ((liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) / X := by
      ext X
      rw [Finset.sum_mul, Finset.sum_div]
      apply Finset.sum_congr rfl
      intro m _
      rw [Finset.mul_sum, Finset.sum_div]
    rw [h_sq_sum, intervalIntegral.integral_finset_sum]
    · apply Finset.sum_congr rfl
      intro m _
      rw [intervalIntegral.integral_finset_sum]
      · apply Finset.sum_congr rfl
        intro n _
        have hi0 : IntervalIntegrable _ volume Y (RiemannScope.tau * Y) :=
          (continuousOn_logWeightedKernel_integrand_tc062_aux hY2 0 m n).intervalIntegrable
        have hi2 : IntervalIntegrable _ volume Y (RiemannScope.tau * Y) :=
          (continuousOn_logWeightedKernel_integrand_tc062_aux hY2 2 m n).intervalIntegrable
        have hi4 : IntervalIntegrable _ volume Y (RiemannScope.tau * Y) :=
          (continuousOn_logWeightedKernel_integrand_tc062_aux hY2 4 m n).intervalIntegrable
        let c0 := (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ)
        let c2 := c0 * (signedAdjustedCoeffB c_lam c_half T D0 n +
            signedAdjustedCoeffB c_lam c_half T D0 m)
        let c4 := c0 * (signedAdjustedCoeffB c_lam c_half T D0 m *
            signedAdjustedCoeffB c_lam c_half T D0 n)
        have h_pt :
            ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
              ((liouvilleLambda m : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 m X) *
                  ((liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) / X =
                c0 * ((gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ 0) / X) -
                  c2 * ((gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ 2) / X) +
                  c4 * ((gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ 4) / X) := by
          intro X hX
          have hlog_ne : Real.log X ≠ 0 := (hprops X hX).2.2.2.1
          have hX_ne : X ≠ 0 := ne_of_gt (hprops X hX).2.1
          dsimp [c0, c2, c4, adjustedStationProfilePsi]
          simp only [pow_zero, div_one]
          field_simp [hlog_ne, hX_ne]
          ring
        rw [intervalIntegral.integral_congr h_pt,
          intervalIntegral.integral_add ((hi0.const_mul c0).sub (hi2.const_mul c2))
            (hi4.const_mul c4),
          intervalIntegral.integral_sub (hi0.const_mul c0) (hi2.const_mul c2),
          intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
          intervalIntegral.integral_const_mul]
        dsimp [c0, c2, c4, logWeightedWindowKernel]
        ring
      · intro n _; exact (h_pair_cont m n).intervalIntegrable
    · intro m _
      exact (continuousOn_finset_sum _ (fun n _ => h_pair_cont m n)).intervalIntegrable
  have h_Xself_Ssub :
      4 * subsetPrimePowerSelfCollisionXself S_sub Y =
        ∑ m ∈ S_sub, ∑ n ∈ S_sub,
          (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
            (if m = n then 4 * ((Real.log (m : ℝ)) ^ 2 - commonPrimePowerLogSq m m) else 0) *
            logWeightedWindowKernel 2 Y m n := by
    unfold subsetPrimePowerSelfCollisionXself
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro m hm
    have hm1 : 1 ≤ m := (Finset.mem_Icc.mp (hS_sub hm)).1
    have h_lam_sq := liouvilleLambda_sq_eq_one_tc062_aux hm1
    symm
    rw [← Finset.add_sum_erase _ _ hm]
    have h_er :
        (∑ n ∈ S_sub.erase m,
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
              (if m = n then 4 * ((Real.log (m : ℝ)) ^ 2 - commonPrimePowerLogSq m m) else 0) *
              logWeightedWindowKernel 2 Y m n) = 0 := by
      apply Finset.sum_eq_zero
      intro n hn
      rw [if_neg (Finset.mem_erase.mp hn).1.symm]
      ring
    rw [h_er, add_zero, if_pos rfl, h_lam_sq]
    unfold offDiagPrimePowerWeight
    ring
  have h_D_Ssub :
      4 * subsetPrimePowerDiagDtilde S_sub Y =
        ∑ m ∈ S_sub, ∑ n ∈ S_sub,
          (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
            (4 * commonPrimePowerLogSq m n) * logWeightedWindowKernel 2 Y m n := by
    unfold subsetPrimePowerDiagDtilde
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro m _
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro n _
    ring
  rw [h_psi_gram, h_D_Ssub, h_Xself_Ssub, ← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro m hm
  rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro n hn
  have hm_Icc := Finset.mem_Icc.mp (hS_sub hm)
  have hn_Icc := Finset.mem_Icc.mp (hS_sub hn)
  have hm_2T : 1 ≤ m ∧ m ≤ 2 * T := ⟨hm_Icc.1, by omega⟩
  have hn_2T : 1 ≤ n ∧ n ≤ 2 * T := ⟨hn_Icc.1, by omega⟩
  have hm_ind : cutoffIndicatorT T m = 1 := by unfold cutoffIndicatorT; exact if_pos hm_Icc
  have hn_ind : cutoffIndicatorT T n = 1 := by unfold cutoffIndicatorT; exact if_pos hn_Icc
  have h_hcal :
      completeSignedKernelHcal c_lam c_half T D0 Y m n =
        cutoffIndicatorT T m * cutoffIndicatorT T n * logWeightedWindowKernel 0 Y m n -
          (cutoffIndicatorT T m * signedAdjustedCoeffB c_lam c_half T D0 n +
              signedAdjustedCoeffB c_lam c_half T D0 m * cutoffIndicatorT T n +
              4 * cutoffIndicatorT T m * cutoffIndicatorT T n * commonPrimePowerLogSq m n +
              (if m = n then
                4 * cutoffIndicatorT T m * ((Real.log (m : ℝ)) ^ 2 - commonPrimePowerLogSq m m)
              else 0)) *
            logWeightedWindowKernel 2 Y m n +
          signedAdjustedCoeffB c_lam c_half T D0 m * signedAdjustedCoeffB c_lam c_half T D0 n *
            logWeightedWindowKernel 4 Y m n := by
    unfold completeSignedKernelHcal
    exact if_pos ⟨hm_2T, hn_2T⟩
  rw [h_hcal, hm_ind, hn_ind]
  by_cases hmn : m = n
  · simp only [hmn, ↓reduceIte]; ring
  · simp only [hmn, ↓reduceIte]; ring

private theorem subsetPrimePowerDiagDtilde_integral_eq_tc062_aux
    {Y : ℝ} (hY2 : 2 ≤ Y) (T : ℕ) (S_sub : Finset ℕ) (hS_sub : S_sub ⊆ Finset.Icc 1 T) :
    subsetPrimePowerDiagDtilde S_sub Y =
      ∫ X in Y..(RiemannScope.tau * Y),
        ((∑ pk ∈ primePowerPairsUpTo T,
            (Real.log (pk.1 : ℝ)) ^ 2 *
              (∑ n ∈ S_sub.filter (fun n => pk.1 ^ pk.2 ∣ n),
                (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) /
          (Real.log X) ^ 2) / X := by
  have h_c_eq :
      ∀ m ∈ S_sub, ∀ n ∈ S_sub,
        commonPrimePowerLogSq m n =
          ∑ pk ∈ primePowerPairsUpTo T,
            (if pk.1 ^ pk.2 ∣ m ∧ pk.1 ^ pk.2 ∣ n then (Real.log (pk.1 : ℝ)) ^ 2 else 0) := by
    intro m hm n hn
    have hm_Icc := Finset.mem_Icc.mp (hS_sub hm)
    have hn_Icc := Finset.mem_Icc.mp (hS_sub hn)
    have hmin_le : min m n ≤ T := le_trans (min_le_left m n) hm_Icc.2
    unfold commonPrimePowerLogSq
    rw [← Finset.sum_filter]
    apply Finset.sum_congr _ (fun _ _ => rfl)
    ext ⟨r, k⟩
    simp only [Finset.mem_filter, primePowerPairsUpTo, Finset.mem_product, primesUpToFinset,
      Finset.mem_Icc, Nat.dvd_gcd_iff]
    constructor
    · rintro ⟨⟨⟨⟨⟨hr2, hr_min⟩, hr_pr⟩, ⟨hk1, hk_min⟩⟩, hrk_min⟩, ⟨hdm, hdn⟩⟩
      exact ⟨⟨⟨⟨⟨hr2, le_trans hr_min hmin_le⟩, hr_pr⟩, ⟨hk1, le_trans hk_min hmin_le⟩⟩,
        le_trans hrk_min hmin_le⟩, ⟨hdm, hdn⟩⟩
    · rintro ⟨⟨⟨⟨⟨hr2, _⟩, hr_pr⟩, ⟨hk1, _⟩⟩, _⟩, ⟨hdm, hdn⟩⟩
      have hrk_m : r ^ k ≤ m := Nat.le_of_dvd hm_Icc.1 hdm
      have hrk_n : r ^ k ≤ n := Nat.le_of_dvd hn_Icc.1 hdn
      have hrk_min : r ^ k ≤ min m n := le_min hrk_m hrk_n
      have hr_rk : r ≤ r ^ k := Nat.le_self_pow (by omega) r
      have hk_rk : k ≤ r ^ k := le_of_lt (Nat.lt_pow_self hr_pr.one_lt k)
      exact ⟨⟨⟨⟨⟨hr2, le_trans hr_rk hrk_min⟩, hr_pr⟩, ⟨hk1, le_trans hk_rk hrk_min⟩⟩,
        hrk_min⟩, ⟨hdm, hdn⟩⟩
  unfold subsetPrimePowerDiagDtilde logWeightedWindowKernel
  have h_cont_mn :
      ∀ m n : ℕ,
        ContinuousOn
          (fun X =>
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
              ((gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ 2) / X))
          (Set.uIcc Y (RiemannScope.tau * Y)) :=
    fun m n => continuousOn_const.mul (continuousOn_logWeightedKernel_integrand_tc062_aux hY2 2 m n)
  have h_pull :
      (∑ m ∈ S_sub, ∑ n ∈ S_sub,
          (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
            ∫ X in Y..(RiemannScope.tau * Y),
              (gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ 2) / X) =
        ∫ X in Y..(RiemannScope.tau * Y),
          ∑ m ∈ S_sub, ∑ n ∈ S_sub,
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
              ((gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ 2) / X) := by
    symm
    rw [intervalIntegral.integral_finset_sum]
    · apply Finset.sum_congr rfl
      intro m _
      rw [intervalIntegral.integral_finset_sum]
      · apply Finset.sum_congr rfl
        intro n _
        exact intervalIntegral.integral_const_mul _ _
      · intro n _; exact (h_cont_mn m n).intervalIntegrable
    · intro m _
      exact (continuousOn_finset_sum _ (fun n _ => h_cont_mn m n)).intervalIntegrable
  rw [h_pull]
  apply intervalIntegral.integral_congr
  intro X _hX
  have h_pt_sum :
      (∑ m ∈ S_sub, ∑ n ∈ S_sub,
          (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
            ((gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ 2) / X)) =
        ((∑ m ∈ S_sub, ∑ n ∈ S_sub, ∑ pk ∈ primePowerPairsUpTo T,
            (if pk.1 ^ pk.2 ∣ m ∧ pk.1 ^ pk.2 ∣ n then (Real.log (pk.1 : ℝ)) ^ 2 else 0) *
              ((liouvilleLambda m : ℝ) * gaussianTermPhi m X) *
              ((liouvilleLambda n : ℝ) * gaussianTermPhi n X)) / (Real.log X) ^ 2) / X := by
    rw [Finset.sum_div, Finset.sum_div]
    apply Finset.sum_congr rfl
    intro m hm
    rw [Finset.sum_div, Finset.sum_div]
    apply Finset.sum_congr rfl
    intro n hn
    rw [h_c_eq m hm n hn, Finset.mul_sum, Finset.sum_mul, Finset.sum_div, Finset.sum_div]
    apply Finset.sum_congr rfl
    intro pk _
    ring
  dsimp only
  rw [h_pt_sum]
  congr 2
  trans (∑ m ∈ S_sub, ∑ pk ∈ primePowerPairsUpTo T, ∑ n ∈ S_sub,
    (if pk.1 ^ pk.2 ∣ m ∧ pk.1 ^ pk.2 ∣ n then (Real.log (pk.1 : ℝ)) ^ 2 else 0) *
      ((liouvilleLambda m : ℝ) * gaussianTermPhi m X) *
      ((liouvilleLambda n : ℝ) * gaussianTermPhi n X))
  · apply Finset.sum_congr rfl; intro m _; exact Finset.sum_comm
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro pk _
  have h_f1 :
      (∑ m ∈ S_sub.filter (fun m => pk.1 ^ pk.2 ∣ m),
          ((liouvilleLambda m : ℝ) * gaussianTermPhi m X) *
            ∑ n ∈ S_sub.filter (fun n => pk.1 ^ pk.2 ∣ n),
              (liouvilleLambda n : ℝ) * gaussianTermPhi n X) =
        ∑ m ∈ S_sub, ∑ n ∈ S_sub,
          (if pk.1 ^ pk.2 ∣ m then (liouvilleLambda m : ℝ) * gaussianTermPhi m X else 0) *
            (if pk.1 ^ pk.2 ∣ n then (liouvilleLambda n : ℝ) * gaussianTermPhi n X else 0) := by
    rw [Finset.sum_filter]
    apply Finset.sum_congr rfl
    intro m _
    rw [Finset.sum_filter]
    by_cases hm_d : pk.1 ^ pk.2 ∣ m <;> simp [hm_d, Finset.mul_sum]
  symm
  rw [sq (∑ n ∈ S_sub.filter (fun n => pk.1 ^ pk.2 ∣ n),
    (liouvilleLambda n : ℝ) * gaussianTermPhi n X)]
  calc
    (Real.log (pk.1 : ℝ)) ^ 2 *
        ((∑ n ∈ S_sub.filter (fun n => pk.1 ^ pk.2 ∣ n),
          (liouvilleLambda n : ℝ) * gaussianTermPhi n X) *
          (∑ n ∈ S_sub.filter (fun n => pk.1 ^ pk.2 ∣ n),
            (liouvilleLambda n : ℝ) * gaussianTermPhi n X))
      = (Real.log (pk.1 : ℝ)) ^ 2 *
          (∑ m ∈ S_sub, ∑ n ∈ S_sub,
            (if pk.1 ^ pk.2 ∣ m then (liouvilleLambda m : ℝ) * gaussianTermPhi m X else 0) *
              (if pk.1 ^ pk.2 ∣ n then (liouvilleLambda n : ℝ) * gaussianTermPhi n X else 0)) := by
          rw [Finset.sum_mul, h_f1]
    _ = ∑ m ∈ S_sub, ∑ n ∈ S_sub,
          (if pk.1 ^ pk.2 ∣ m ∧ pk.1 ^ pk.2 ∣ n then (Real.log (pk.1 : ℝ)) ^ 2 else 0) *
            ((liouvilleLambda m : ℝ) * gaussianTermPhi m X) *
            ((liouvilleLambda n : ℝ) * gaussianTermPhi n X) := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro m _
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro n _
          (by_cases hm_d : pk.1 ^ pk.2 ∣ m <;> by_cases hn_d : pk.1 ^ pk.2 ∣ n <;>
            simp [hm_d, hn_d]); ring

private theorem subsetPrimePowerDiagDtilde_nonneg_tc062_aux
    {Y : ℝ} (hY2 : 2 ≤ Y) {T : ℕ} (S_sub : Finset ℕ) (hS_sub : S_sub ⊆ Finset.Icc 1 T) :
    0 ≤ subsetPrimePowerDiagDtilde S_sub Y := by
  obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc062_aux hY2
  rw [subsetPrimePowerDiagDtilde_integral_eq_tc062_aux hY2 T S_sub hS_sub]
  apply intervalIntegral.integral_nonneg hle
  intro X hX
  have hX_in : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
  have hX_pos : 0 < X := (hprops X hX_in).2.1
  apply div_nonneg _ (le_of_lt hX_pos)
  apply div_nonneg _ (sq_nonneg _)
  apply Finset.sum_nonneg
  intro pk _
  exact mul_nonneg (sq_nonneg _) (sq_nonneg _)

private theorem sum_inv_Icc_two_le_log_tc062_aux (T : ℕ) (hT1 : 1 ≤ T) :
    (∑ q ∈ Finset.Icc 2 T, (1 / (q : ℝ))) ≤ Real.log (T : ℝ) := by
  obtain ⟨m, rfl⟩ : ∃ m : ℕ, T = m + 1 := ⟨T - 1, by omega⟩
  induction' m with m ih
  · simp
  · have hm1 : 1 ≤ m + 1 := by omega
    have h_ih := ih hm1
    have h_ins : Finset.Icc 2 (m + 1 + 1) = insert (m + 1 + 1) (Finset.Icc 2 (m + 1)) := by
      ext q; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
    have h_not : (m + 1 + 1) ∉ Finset.Icc 2 (m + 1) := by simp
    rw [h_ins, Finset.sum_insert h_not]
    let a : ℝ := ((m + 1 : ℕ) : ℝ)
    have ha_pos : 0 < a := by dsimp [a]; positivity
    have ha1_pos : 0 < a + 1 := by linarith
    have h_exp := Real.add_one_le_exp (-(1 / (a + 1)))
    have h_lhs_eq : -(1 / (a + 1)) + 1 = a / (a + 1) := by
      field_simp [ne_of_gt ha1_pos]
    rw [h_lhs_eq] at h_exp
    have h_log_le := Real.log_le_log (div_pos ha_pos ha1_pos) h_exp
    rw [Real.log_exp, Real.log_div (ne_of_gt ha_pos) (ne_of_gt ha1_pos)] at h_log_le
    have h_cast : ((m + 1 + 1 : ℕ) : ℝ) = a + 1 := by dsimp [a]; push_cast; ring
    rw [h_cast]
    linarith

private theorem canonicalCutoffT_bounds_tc062_aux {Y : ℝ} (hY2 : 2 ≤ Y) :
    2 ≤ canonicalCutoffT Y ∧
      Y ^ (5 / 4 : ℝ) ≤ (canonicalCutoffT Y : ℝ) ∧
      (canonicalCutoffT Y : ℝ) ≤ 2 * Y ^ (5 / 4 : ℝ) ∧
      Real.log (canonicalCutoffT Y : ℝ) ≤ (9 / 4 : ℝ) * Real.log Y ∧
      Y ^ (5 / 2 : ℝ) ≤ (canonicalCutoffT Y : ℝ) ^ 2 ∧
      Y ^ 5 ≤ (canonicalCutoffT Y : ℝ) ^ 4 ∧
      (1 / 2 : ℝ) < Real.log Y := by
  have hY_pos : 0 < Y := by linarith
  have hY1_lt : 1 < Y := by linarith
  have hrpow_gt1 : 1 < Y ^ (5 / 4 : ℝ) := Real.one_lt_rpow hY1_lt (by norm_num)
  have hle_T : Y ^ (5 / 4 : ℝ) ≤ (canonicalCutoffT Y : ℝ) := by
    unfold canonicalCutoffT; exact Nat.le_ceil _
  have hT_gt1_real : (1 : ℝ) < (canonicalCutoffT Y : ℝ) := lt_of_lt_of_le hrpow_gt1 hle_T
  have hT_gt1 : 1 < canonicalCutoffT Y := by exact_mod_cast hT_gt1_real
  have hT_ge2 : 2 ≤ canonicalCutoffT Y := by omega
  have hT_lt : (canonicalCutoffT Y : ℝ) < Y ^ (5 / 4 : ℝ) + 1 := by
    unfold canonicalCutoffT
    exact Nat.ceil_lt_add_one (by positivity)
  have hT_le_2 : (canonicalCutoffT Y : ℝ) ≤ 2 * Y ^ (5 / 4 : ℝ) := by linarith
  have h2_le_Y : 2 * Y ^ (5 / 4 : ℝ) ≤ Y ^ (9 / 4 : ℝ) := by
    have h_eq : Y * Y ^ (5 / 4 : ℝ) = Y ^ (9 / 4 : ℝ) := by
      calc
        Y * Y ^ (5 / 4 : ℝ) = Y ^ (1 : ℝ) * Y ^ (5 / 4 : ℝ) := by rw [Real.rpow_one]
        _ = Y ^ (9 / 4 : ℝ) := by rw [← Real.rpow_add hY_pos]; norm_num
    rw [← h_eq]
    exact mul_le_mul_of_nonneg_right hY2 (by positivity)
  have hlogT : Real.log (canonicalCutoffT Y : ℝ) ≤ (9 / 4 : ℝ) * Real.log Y := by
    have h1 := Real.log_le_log (by positivity) (le_trans hT_le_2 h2_le_Y)
    rwa [Real.log_rpow hY_pos] at h1
  have h52 : Y ^ (5 / 2 : ℝ) ≤ (canonicalCutoffT Y : ℝ) ^ 2 := by
    have h_eq : (Y ^ (5 / 4 : ℝ)) ^ 2 = Y ^ (5 / 2 : ℝ) := by
      rw [← Real.rpow_natCast _ 2, ← Real.rpow_mul (le_of_lt hY_pos)]
      norm_num
    rw [← h_eq]
    exact pow_le_pow_left (by positivity) hle_T 2
  have h5 : Y ^ 5 ≤ (canonicalCutoffT Y : ℝ) ^ 4 := by
    have h_eq : (Y ^ (5 / 4 : ℝ)) ^ 4 = Y ^ 5 := by
      rw [← Real.rpow_natCast _ 4, ← Real.rpow_mul (le_of_lt hY_pos)]
      have hexp : (5 / 4 : ℝ) * ((4 : ℕ) : ℝ) = ((5 : ℕ) : ℝ) := by norm_num
      rw [hexp, Real.rpow_natCast]
    rw [← h_eq]
    exact pow_le_pow_left (by positivity) hle_T 4
  have hlog2_gt : (1 / 2 : ℝ) < Real.log 2 := by
    have h_inv8 : (7 / 8 : ℝ) ≤ Real.exp (-(1 / 8 : ℝ)) := by
      linarith [Real.add_one_le_exp (-(1 / 8 : ℝ))]
    have h_prod : Real.exp (1 / 8 : ℝ) * Real.exp (-(1 / 8 : ℝ)) = 1 := by
      rw [← Real.exp_add, add_neg_self, Real.exp_zero]
    have he8_le : Real.exp (1 / 8 : ℝ) ≤ 8 / 7 := by
      have hm := mul_le_mul_of_nonneg_left h_inv8 (le_of_lt (Real.exp_pos (1 / 8 : ℝ)))
      rw [h_prod] at hm; linarith
    have hp4 : (Real.exp (1 / 8 : ℝ)) ^ 4 ≤ (8 / 7 : ℝ) ^ 4 :=
      pow_le_pow_left (le_of_lt (Real.exp_pos _)) he8_le 4
    have he_half : (Real.exp (1 / 8 : ℝ)) ^ 4 = Real.exp (1 / 2 : ℝ) := by
      rw [← Real.exp_nat_mul]; congr 1; norm_num
    rw [he_half] at hp4
    have hlt2 : Real.exp (1 / 2 : ℝ) < 2 := lt_of_le_of_lt hp4 (by norm_num)
    have hl := Real.log_lt_log (Real.exp_pos _) hlt2
    rwa [Real.log_exp] at hl
  have hlogY_gt : (1 / 2 : ℝ) < Real.log Y :=
    lt_of_lt_of_le hlog2_gt (Real.log_le_log (by norm_num) hY2)
  exact ⟨hT_ge2, hle_T, hT_le_2, hlogT, h52, h5, hlogY_gt⟩

private theorem gaussianTermPhi_le_of_ge_tc062_aux {Y : ℝ} (hY2 : 2 ≤ Y)
    {X : ℝ} (hX : X ∈ Set.uIcc Y (RiemannScope.tau * Y)) {k : ℕ} {B : ℝ}
    (hB_pos : 0 < B) (hBk : B ≤ (k : ℝ)) :
    0 ≤ gaussianTermPhi k X ∧
      gaussianTermPhi k X ≤ (RiemannScope.tau * Y) ^ (5 / 2 : ℝ) / B ^ 3 := by
  obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc062_aux hY2
  have hX_Icc : Y ≤ X ∧ X ≤ RiemannScope.tau * Y := by
    rwa [Set.uIcc_of_le hle, Set.mem_Icc] at hX
  have hX_pos : 0 < X := (hprops X hX).2.1
  have hk_pos : 0 < (k : ℝ) := lt_of_lt_of_le hB_pos hBk
  unfold gaussianTermPhi
  refine ⟨by positivity, ?_⟩
  have hrpow_le : X ^ (5 / 2 : ℝ) ≤ (RiemannScope.tau * Y) ^ (5 / 2 : ℝ) :=
    Real.rpow_le_rpow (le_of_lt hX_pos) hX_Icc.2 (by norm_num)
  have hexp_le1 : Real.exp (-(X ^ 2) / (k : ℝ) ^ 2) ≤ 1 := by
    rw [Real.exp_le_one_iff]
    exact div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg X)) (sq_nonneg _)
  have hB3_le : B ^ 3 ≤ (k : ℝ) ^ 3 := pow_le_pow_left (le_of_lt hB_pos) hBk 3
  have hinv_le : ((k : ℝ) ^ 3)⁻¹ ≤ (B ^ 3)⁻¹ := inv_le_inv_of_le (pow_pos hB_pos 3) hB3_le
  calc
    X ^ (5 / 2 : ℝ) * (((k : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (k : ℝ) ^ 2))
      ≤ X ^ (5 / 2 : ℝ) * (((k : ℝ) ^ 3)⁻¹ * 1) := by
          gcongr
    _ = X ^ (5 / 2 : ℝ) * ((k : ℝ) ^ 3)⁻¹ := by ring
    _ ≤ (RiemannScope.tau * Y) ^ (5 / 2 : ℝ) * (B ^ 3)⁻¹ :=
          mul_le_mul hrpow_le hinv_le
            (inv_nonneg.mpr (pow_nonneg (Nat.cast_nonneg k) 3))
            (Real.rpow_nonneg (mul_nonneg (le_of_lt RiemannScope.tau_pos) (by linarith)) _)
    _ = (RiemannScope.tau * Y) ^ (5 / 2 : ℝ) / B ^ 3 := (div_eq_mul_inv _ _).symm

private theorem selbergWeight2_and_cumulative_abs_le_tc062_aux :
    (∀ {n : ℕ}, 1 ≤ n → |selbergLiouvilleWeight2 n| ≤ (Real.log (n : ℝ)) ^ 2) ∧
      (∀ {d : ℕ}, 1 ≤ d → |selbergCumulativeW2 d| ≤ (d : ℝ) * (Real.log (d : ℝ)) ^ 2) := by
  have h_w2 : ∀ {n : ℕ}, 1 ≤ n → |selbergLiouvilleWeight2 n| ≤ (Real.log (n : ℝ)) ^ 2 := by
    intro n hn1
    have hn_pos : 0 < n := by omega
    have hn_ne : n ≠ 0 := by omega
    obtain ⟨_, _, _, _, ⟨h_lv_mul, _, _, _⟩⟩ :=
      liouville_square_divisor_indicator_and_compensated_selberg_tc058 0 0
    have h_fact :
        selbergLiouvilleWeight2 n =
          (liouvilleLambda n : ℝ) *
            (ArithmeticFunction.vonMangoldt n * Real.log (n : ℝ) +
              (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) n) := by
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
        have hx1 : 1 ≤ x.1 := by
          rcases Nat.eq_zero_or_pos x.1 with hz | hpos
          · rw [hz, zero_mul] at h_prod; omega
          · exact hpos
        have hx2 : 1 ≤ x.2 := by
          rcases Nat.eq_zero_or_pos x.2 with hz | hpos
          · rw [hz, mul_zero] at h_prod; omega
          · exact hpos
        rw [h_lv_mul x.1, h_lv_mul x.2, ← h_prod, liouvilleLambda_mul_pos_tc062_aux hx1 hx2]
        ring
      rw [h_conv]; ring
    let A : ℕ → ℝ := fun d =>
      ArithmeticFunction.vonMangoldt d * Real.log (d : ℝ) +
        (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) d
    have hA_nn : ∀ d ∈ n.divisors, 0 ≤ A d := by
      intro d hd
      have hd_pos : 0 < d := Nat.pos_of_dvd_of_pos (Nat.mem_divisors.mp hd).1 hn_pos
      have hd1 : (1 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd_pos
      have hlog_nn : 0 ≤ Real.log (d : ℝ) := Real.log_nonneg hd1
      have hvm_nn : 0 ≤ ArithmeticFunction.vonMangoldt d := ArithmeticFunction.vonMangoldt_nonneg
      have hconv_nn : 0 ≤ (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) d := by
        rw [ArithmeticFunction.mul_apply]
        exact Finset.sum_nonneg (fun _ _ =>
          mul_nonneg ArithmeticFunction.vonMangoldt_nonneg ArithmeticFunction.vonMangoldt_nonneg)
      exact add_nonneg (mul_nonneg hvm_nn hlog_nn) hconv_nn
    have h_sum_A : (∑ d ∈ n.divisors, A d) = (Real.log (n : ℝ)) ^ 2 := by
      change (∑ d ∈ n.divisors,
        (ArithmeticFunction.vonMangoldt d * Real.log (d : ℝ) +
          (ArithmeticFunction.vonMangoldt * ArithmeticFunction.vonMangoldt) d)) =
        (Real.log (n : ℝ)) ^ 2
      rw [Finset.sum_add_distrib]
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
        have hd_pos : 0 < d := Nat.pos_of_dvd_of_pos hd.1 hn_pos
        have hd_ne_r : (d : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (ne_of_gt hd_pos)
        have hn_ne_r : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn_ne
        rw [ArithmeticFunction.log_apply, Nat.cast_div hd.1 hd_ne_r,
          Real.log_div hn_ne_r hd_ne_r]
        ring
      rw [h_log_div, Finset.sum_sub_distrib, ← Finset.sum_mul,
        ArithmeticFunction.vonMangoldt_sum]
      ring
    have hn_mem : n ∈ n.divisors := Nat.mem_divisors.mpr ⟨dvd_refl n, hn_ne⟩
    have hAn_le : A n ≤ (Real.log (n : ℝ)) ^ 2 := by
      rw [← h_sum_A]
      exact Finset.single_le_sum hA_nn hn_mem
    have hlam_abs : |(liouvilleLambda n : ℝ)| = 1 := abs_liouvilleLambda_eq_one_tc062_aux hn1
    rw [h_fact, abs_mul, hlam_abs, one_mul, abs_of_nonneg (hA_nn n hn_mem)]
    exact hAn_le
  refine ⟨h_w2, ?_⟩
  intro d _hd1
  unfold selbergCumulativeW2
  calc
    |∑ k ∈ Finset.Icc 2 d, selbergLiouvilleWeight2 k|
      ≤ ∑ k ∈ Finset.Icc 2 d, |selbergLiouvilleWeight2 k| := Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ k ∈ Finset.Icc 2 d, (Real.log (d : ℝ)) ^ 2 := by
          apply Finset.sum_le_sum
          intro k hk
          rw [Finset.mem_Icc] at hk
          have hk1 : 1 ≤ k := by omega
          have hlog_le : Real.log (k : ℝ) ≤ Real.log (d : ℝ) :=
            Real.log_le_log (by positivity) (by exact_mod_cast hk.2)
          have hlog_nn : 0 ≤ Real.log (k : ℝ) := Real.log_nonneg (by exact_mod_cast hk1)
          exact le_trans (h_w2 hk1) (pow_le_pow_left hlog_nn hlog_le 2)
    _ = ((Finset.Icc 2 d).card : ℝ) * (Real.log (d : ℝ)) ^ 2 := by simp
    _ ≤ (d : ℝ) * (Real.log (d : ℝ)) ^ 2 := by
          have hcard : (Finset.Icc 2 d).card ≤ d := by simp [Nat.card_Icc]
          exact mul_le_mul_of_nonneg_right (by exact_mod_cast hcard) (sq_nonneg _)

private theorem centered_minus_drift_abs_le_tc062_aux (c_lam c_half : ℝ) {d T : ℕ}
    (hd1 : 1 ≤ d) (hdT : d ≤ T) :
    |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| ≤
      (d : ℝ) * ((Real.log (T : ℝ)) ^ 2 + 4 * Real.log (T : ℝ) + |c_lam| + |c_half|) := by
  have hd_ne : d ≠ 0 := by omega
  have hd_pos_r : (0 : ℝ) < (d : ℝ) := by exact_mod_cast (by omega : 0 < d)
  have hd1_r : (1 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd1
  have hlogd_nn : 0 ≤ Real.log (d : ℝ) := Real.log_nonneg hd1_r
  have hlogT_ge : Real.log (d : ℝ) ≤ Real.log (T : ℝ) :=
    Real.log_le_log hd_pos_r (by exact_mod_cast hdT)
  have hsqrt_le : Real.sqrt (d : ℝ) ≤ (d : ℝ) := by
    have hsq : (Real.sqrt (d : ℝ)) ^ 2 ≤ (d : ℝ) ^ 2 := by
      rw [Real.sq_sqrt (le_of_lt hd_pos_r)]
      nlinarith
    nlinarith [Real.sqrt_nonneg (d : ℝ)]
  have hW2 := selbergWeight2_and_cumulative_abs_le_tc062_aux.2 hd1
  have hlog_sq_le : (Real.log (d : ℝ)) ^ 2 ≤ (Real.log (T : ℝ)) ^ 2 :=
    pow_le_pow_left hlogd_nn hlogT_ge 2
  unfold selbergCenteredRemainderInt squarePoleDriftM
  rw [if_neg hd_ne]
  have h1 : |selbergCumulativeW2 d| ≤ (d : ℝ) * (Real.log (T : ℝ)) ^ 2 :=
    le_trans hW2 (mul_le_mul_of_nonneg_left hlog_sq_le (le_of_lt hd_pos_r))
  have h2 : |c_lam * (d : ℝ)| = |c_lam| * (d : ℝ) := by
    rw [abs_mul, abs_of_pos hd_pos_r]
  have h3 : |4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ)| ≤ (d : ℝ) * (4 * Real.log (T : ℝ)) := by
    rw [abs_of_nonneg (by positivity)]
    calc
      4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ)
        ≤ 4 * (d : ℝ) * Real.log (d : ℝ) := by nlinarith
      _ ≤ 4 * (d : ℝ) * Real.log (T : ℝ) := by nlinarith
      _ = (d : ℝ) * (4 * Real.log (T : ℝ)) := by ring
  have h4 : |c_half * Real.sqrt (d : ℝ)| ≤ (d : ℝ) * |c_half| := by
    rw [abs_mul, abs_of_nonneg (Real.sqrt_nonneg _)]
    nlinarith [abs_nonneg c_half]
  have h_tri :
      |selbergCumulativeW2 d - c_lam * (d : ℝ) -
          (4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ) + c_half * Real.sqrt (d : ℝ))| ≤
        |selbergCumulativeW2 d| + |c_lam * (d : ℝ)| +
          |4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ)| + |c_half * Real.sqrt (d : ℝ)| := by
    have t1 := abs_sub (selbergCumulativeW2 d - c_lam * (d : ℝ))
      (4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ) + c_half * Real.sqrt (d : ℝ))
    have t2 := abs_sub (selbergCumulativeW2 d) (c_lam * (d : ℝ))
    have t3 := abs_add (4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ)) (c_half * Real.sqrt (d : ℝ))
    linarith
  linarith

private theorem log_cube_le_rpow_tc062_aux {Y η : ℝ} (hY1 : 1 ≤ Y) (hη : 0 < η) :
    (Real.log Y) ^ 3 ≤ (27 / η ^ 3) * Y ^ η := by
  have hY_pos : 0 < Y := lt_of_lt_of_le zero_lt_one hY1
  have hlog_nn : 0 ≤ Real.log Y := Real.log_nonneg hY1
  let u := (η / 3) * Real.log Y
  have hu_le : u ≤ Real.exp u := by linarith [Real.add_one_le_exp u]
  have hexp_u : Real.exp u = Y ^ (η / 3) := by
    dsimp [u]
    rw [mul_comm, ← Real.rpow_def_of_pos hY_pos]
  rw [hexp_u] at hu_le
  have hlog_le : Real.log Y ≤ (3 / η) * Y ^ (η / 3) := by
    have hm := mul_le_mul_of_nonneg_left hu_le (show 0 ≤ 3 / η by positivity)
    have hc : (3 / η) * ((η / 3) * Real.log Y) = Real.log Y := by
      field_simp [ne_of_gt hη]; ring
    dsimp [u] at hm
    rwa [hc] at hm
  have hcube := pow_le_pow_left hlog_nn hlog_le 3
  have hrhs : ((3 / η) * Y ^ (η / 3)) ^ 3 = (27 / η ^ 3) * Y ^ η := by
    rw [mul_pow, ← Real.rpow_natCast (Y ^ (η / 3)) 3, ← Real.rpow_mul (le_of_lt hY_pos)]
    have hexp : (η / 3) * ((3 : ℕ) : ℝ) = η := by push_cast; ring
    rw [hexp]
    ring
  rwa [hrhs] at hcube

private theorem mixedCovarianceClosure_of_log_perturbation_tc062_aux
    {F1 F2 D : ℝ → ℝ} {C_err : ℝ} (hC_nn : 0 ≤ C_err)
    (hD_nn : ∀ Y : ℝ, 2 ≤ Y → 0 ≤ D Y)
    (h_pert : ∀ Y : ℝ, Real.exp 1 ≤ Y →
      F2 Y ≤ (1 + 1 / Real.log Y) * F1 Y + (12 / Real.log Y) * D Y +
        C_err * (Real.log Y) ^ 3) :
    MixedCovarianceClosureHypothesis F1 D → MixedCovarianceClosureHypothesis F2 D := by
  intro hF1 η hη
  obtain ⟨a_eta, b_eta, κ_eta, Y_eta, ha, hb, hκ_pos, hκ_le2, hYe, hF1_bd⟩ := hF1 η hη
  refine ⟨2 * a_eta + C_err * (27 / η ^ 3), 2 * b_eta + 12, κ_eta, max Y_eta (Real.exp 1),
    by positivity, by positivity, hκ_pos, hκ_le2, le_trans hYe (le_max_left _ _), ?_⟩
  intro Y hYm
  have hYYe : Y_eta ≤ Y := le_trans (le_max_left _ _) hYm
  have hY_ge_e : Real.exp 1 ≤ Y := le_trans (le_max_right _ _) hYm
  have hY2 : 2 ≤ Y := le_trans hYe hYYe
  have hY1 : 1 ≤ Y := by linarith
  have hD := hD_nn Y hY2
  have hlog_ge1 : 1 ≤ Real.log Y := by
    have h := Real.log_le_log (Real.exp_pos 1) hY_ge_e
    rwa [Real.log_exp] at h
  have hlog_pos : 0 < Real.log Y := lt_of_lt_of_le zero_lt_one hlog_ge1
  have h_inv_le1 : 1 / Real.log Y ≤ 1 := div_le_one_of_le hlog_ge1 (le_of_lt hlog_pos)
  have h_1add_pos : 0 ≤ 1 + 1 / Real.log Y := by positivity
  have h_1add_le2 : 1 + 1 / Real.log Y ≤ 2 := by linarith
  have hF1_Y := hF1_bd Y hYYe
  have h_rhs_nn : 0 ≤ a_eta * Y ^ η + b_eta * (Real.log Y) ^ (2 - κ_eta) * D Y :=
    add_nonneg (mul_nonneg ha (Real.rpow_nonneg (by linarith) _))
      (mul_nonneg (mul_nonneg hb (Real.rpow_nonneg (le_of_lt hlog_pos) _)) hD)
  have h_term1 :
      (1 + 1 / Real.log Y) * F1 Y ≤
        2 * (a_eta * Y ^ η + b_eta * (Real.log Y) ^ (2 - κ_eta) * D Y) :=
    le_trans (mul_le_mul_of_nonneg_left hF1_Y h_1add_pos)
      (mul_le_mul_of_nonneg_right h_1add_le2 h_rhs_nn)
  have h_logpow_ge1 : 1 ≤ (Real.log Y) ^ (2 - κ_eta) :=
    Real.one_le_rpow hlog_ge1 (by linarith)
  have h_term2 : (12 / Real.log Y) * D Y ≤ 12 * (Real.log Y) ^ (2 - κ_eta) * D Y := by
    have h12_inv : 12 / Real.log Y ≤ 12 := by
      rw [show (12 : ℝ) / Real.log Y = 12 * (1 / Real.log Y) by ring]
      linarith
    calc
      (12 / Real.log Y) * D Y ≤ 12 * D Y := mul_le_mul_of_nonneg_right h12_inv hD
      _ ≤ 12 * ((Real.log Y) ^ (2 - κ_eta) * D Y) :=
          mul_le_mul_of_nonneg_left (le_mul_of_one_le_left hD h_logpow_ge1) (by norm_num)
      _ = 12 * (Real.log Y) ^ (2 - κ_eta) * D Y := by ring
  have h_term3 : C_err * (Real.log Y) ^ 3 ≤ C_err * (27 / η ^ 3) * Y ^ η := by
    have hc := mul_le_mul_of_nonneg_left (log_cube_le_rpow_tc062_aux hY1 hη) hC_nn
    linarith
  have hp := h_pert Y hY_ge_e
  linarith

private theorem windowEnergyNormSq_young_add_tc062_aux
    {Y : ℝ} (hY2 : 2 ≤ Y) {f g : ℝ → ℝ}
    (hf : ContinuousOn f (Set.uIcc Y (RiemannScope.tau * Y)))
    (hg : ContinuousOn g (Set.uIcc Y (RiemannScope.tau * Y)))
    {δ : ℝ} (hδ : 0 < δ) :
    windowEnergyNormSq Y (fun X => f X + g X) ≤
        (1 + δ) * windowEnergyNormSq Y f + (1 + 1 / δ) * windowEnergyNormSq Y g ∧
      windowEnergyNormSq Y f ≤
        (1 + δ) * windowEnergyNormSq Y (fun X => f X + g X) +
          (1 + 1 / δ) * windowEnergyNormSq Y g := by
  obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc062_aux hY2
  have h_int : ∀ h : ℝ → ℝ, ContinuousOn h (Set.uIcc Y (RiemannScope.tau * Y)) →
      IntervalIntegrable (fun X => h X * h X / X) volume Y (RiemannScope.tau * Y) := by
    intro h hh
    exact ((hh.mul hh).div continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
  have hfg := hf.add hg
  have h_if := h_int f hf
  have h_ig := h_int g hg
  have h_ifg := h_int _ hfg
  have hδ_ne : δ ≠ 0 := ne_of_gt hδ
  have h_scalar : ∀ u v : ℝ, (u + v) * (u + v) ≤ (1 + δ) * (u * u) + (1 + 1 / δ) * (v * v) := by
    intro u v
    have h_diff :
        (1 + δ) * (u * u) + (1 + 1 / δ) * (v * v) - (u + v) * (u + v) =
          (δ * u - v) ^ 2 / δ := by
      field_simp [hδ_ne]; ring
    have h_nn : 0 ≤ (δ * u - v) ^ 2 / δ := div_nonneg (sq_nonneg _) (le_of_lt hδ)
    linarith
  unfold windowEnergyNormSq windowPairing
  constructor
  · rw [← intervalIntegral.integral_const_mul, ← intervalIntegral.integral_const_mul,
      ← intervalIntegral.integral_add (h_if.const_mul _) (h_ig.const_mul _)]
    apply intervalIntegral.integral_mono_on hle h_ifg
      ((h_if.const_mul _).add (h_ig.const_mul _))
    intro X hX
    have hX_in : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
    have hX_pos : 0 < X := (hprops X hX_in).2.1
    have hs := h_scalar (f X) (g X)
    calc
      (f X + g X) * (f X + g X) / X
        ≤ ((1 + δ) * (f X * f X) + (1 + 1 / δ) * (g X * g X)) / X :=
          div_le_div_of_nonneg_right hs (le_of_lt hX_pos)
      _ = (1 + δ) * (f X * f X / X) + (1 + 1 / δ) * (g X * g X / X) := by ring
  · rw [← intervalIntegral.integral_const_mul, ← intervalIntegral.integral_const_mul,
      ← intervalIntegral.integral_add (h_ifg.const_mul _) (h_ig.const_mul _)]
    apply intervalIntegral.integral_mono_on hle h_if
      ((h_ifg.const_mul _).add (h_ig.const_mul _))
    intro X hX
    have hX_in : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
    have hX_pos : 0 < X := (hprops X hX_in).2.1
    have hs := h_scalar (f X + g X) (-g X)
    have hf_eq : (f X + g X + -g X) = f X := by ring
    have hneg_sq : (-g X) * (-g X) = g X * g X := by ring
    rw [hf_eq, hneg_sq] at hs
    calc
      f X * f X / X
        ≤ ((1 + δ) * ((f X + g X) * (f X + g X)) + (1 + 1 / δ) * (g X * g X)) / X :=
          div_le_div_of_nonneg_right hs (le_of_lt hX_pos)
      _ = (1 + δ) * ((f X + g X) * (f X + g X) / X) + (1 + 1 / δ) * (g X * g X / X) := by ring

/-- **Theorem 5 (`TASK-TC-062` §6, Spillover Fringe Reindexing & Support, Unconditional Pointwise Selberg Bounds, `[1, T]^2` Truncated Signed-Remainder Norm Identity, Polynomial-Log Spillover Energy Bound, and Two-Way `MixedCovarianceClosureHypothesis` Equivalence)**:
    1. *Exact spillover support & `q`-reindexing (`1 ≤ T`, `T < n`)*:
       - `openCoreAdjustedCoeffBeta c_lam c_half T D0 n = -∑ q ∈ (Finset.Icc 2 (T / (min D0 (T - 1) + 1))).filter (fun q => (T / q + 1) * q = n), (selbergCenteredRemainderInt c_lam (T / q) - squarePoleDriftM c_half (T / q)) * (liouvilleLambda q : ℝ)`;
       - `openCoreAdjustedCoeffBeta c_lam c_half T D0 n ≠ 0 → n ≤ T + T / (min D0 (T - 1) + 1)`;
       - `T < 2 * (min D0 (T - 1) + 1) → openCoreAdjustedCoeffBeta c_lam c_half T D0 n = 0`;
       - Pointwise spillover sum identity for all `X : ℝ`;
    2. *Unconditional pointwise Selberg bounds*:
       `|selbergLiouvilleWeight2 n| ≤ (Real.log n)^2` (`n ≥ 1`) and `|selbergCumulativeW2 d| ≤ d * (Real.log d)^2` (`d ≥ 1`);
    3. *Truncated `[1, T]^2` window norm identity, canonical `O((log Y)^2)` spillover bound (`Y ≥ 2`), and exact two-way equivalence `H(F_full, Dtilde) ↔ H(F_trunc, Dtilde)`* (for all `(c_lam, c_half)` and at `(actualSelbergConstantCLam, actualSquarePoleConstantCHalf)`). -/
theorem spillover_fringe_reindexing_and_mixed_covariance_reduction_tc062 :
    (∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
      (∀ {n : ℕ}, T < n →
        openCoreAdjustedCoeffBeta c_lam c_half T D0 n =
            -(∑ q ∈ (Finset.Icc 2 (T / (min D0 (T - 1) + 1))).filter
                (fun q => (T / q + 1) * q = n),
              (selbergCenteredRemainderInt c_lam (T / q) - squarePoleDriftM c_half (T / q)) *
                (liouvilleLambda q : ℝ)) ∧
          (openCoreAdjustedCoeffBeta c_lam c_half T D0 n ≠ 0 →
            n ≤ T + T / (min D0 (T - 1) + 1)) ∧
          (T < 2 * (min D0 (T - 1) + 1) →
            openCoreAdjustedCoeffBeta c_lam c_half T D0 n = 0)) ∧
        (∀ X : ℝ,
          (∑ n ∈ Finset.Icc (T + 1) (2 * T),
              openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) =
            -(∑ q ∈ Finset.Icc 2 (T / (min D0 (T - 1) + 1)),
              (selbergCenteredRemainderInt c_lam (T / q) - squarePoleDriftM c_half (T / q)) *
                (liouvilleLambda q : ℝ) * gaussianTermPhi ((T / q + 1) * q) X))) ∧
    ((∀ {n : ℕ}, 1 ≤ n → |selbergLiouvilleWeight2 n| ≤ (Real.log (n : ℝ)) ^ 2) ∧
      (∀ {d : ℕ}, 1 ≤ d → |selbergCumulativeW2 d| ≤ (d : ℝ) * (Real.log (d : ℝ)) ^ 2)) ∧
    ((∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        4 * inheritedPrimePowerDiagDtilde T Y +
            4 * inheritedPrimePowerSelfCollisionXself T Y +
            truncatedSignedRemainderF c_lam c_half T D0 Y =
          windowEnergyNormSq Y (truncatedAdjustedCoreU c_lam c_half T D0) ∧
          4 * inheritedPrimePowerDiagDtilde T Y +
              4 * inheritedPrimePowerSelfCollisionXself T Y +
              completeSignedRemainderF c_lam c_half T D0 Y =
            windowEnergyNormSq Y
              (fun X =>
                truncatedAdjustedCoreU c_lam c_half T D0 X +
                  spilloverFringeS c_lam c_half T D0 X)) ∧
      (∀ (c_lam c_half : ℝ),
        ∃ C_sp : ℝ, 0 ≤ C_sp ∧
          ∀ {Y : ℝ}, 2 ≤ Y →
            windowEnergyNormSq Y (canonicalSpilloverFringeS c_lam c_half Y) ≤
              C_sp * (Real.log Y) ^ 2) ∧
      (∀ (c_lam c_half : ℝ),
        MixedCovarianceClosureHypothesis
            (canonicalSignedRemainderF c_lam c_half) canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalTruncatedSignedRemainderF c_lam c_half) canonicalPrimePowerDiagDtilde) ∧
      (MixedCovarianceClosureHypothesis
          (canonicalSignedRemainderF actualSelbergConstantCLam actualSquarePoleConstantCHalf)
          canonicalPrimePowerDiagDtilde ↔
        MixedCovarianceClosureHypothesis
          (canonicalTruncatedSignedRemainderF
            actualSelbergConstantCLam actualSquarePoleConstantCHalf)
          canonicalPrimePowerDiagDtilde)) := by
  have h_part1 :
      ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        (∀ {n : ℕ}, T < n →
          openCoreAdjustedCoeffBeta c_lam c_half T D0 n =
              -(∑ q ∈ (Finset.Icc 2 (T / (min D0 (T - 1) + 1))).filter
                  (fun q => (T / q + 1) * q = n),
                (selbergCenteredRemainderInt c_lam (T / q) - squarePoleDriftM c_half (T / q)) *
                  (liouvilleLambda q : ℝ)) ∧
            (openCoreAdjustedCoeffBeta c_lam c_half T D0 n ≠ 0 →
              n ≤ T + T / (min D0 (T - 1) + 1)) ∧
            (T < 2 * (min D0 (T - 1) + 1) →
              openCoreAdjustedCoeffBeta c_lam c_half T D0 n = 0)) ∧
          (∀ X : ℝ,
            (∑ n ∈ Finset.Icc (T + 1) (2 * T),
                openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) =
              -(∑ q ∈ Finset.Icc 2 (T / (min D0 (T - 1) + 1)),
                (selbergCenteredRemainderInt c_lam (T / q) - squarePoleDriftM c_half (T / q)) *
                  (liouvilleLambda q : ℝ) * gaussianTermPhi ((T / q + 1) * q) X)) := by
    intro T hT D0 c_lam c_half
    let D_min := min D0 (T - 1)
    have h_coeff :
        ∀ {n : ℕ}, T < n →
          openCoreAdjustedCoeffBeta c_lam c_half T D0 n =
            -(∑ q ∈ (Finset.Icc 2 (T / (D_min + 1))).filter
                (fun q => (T / q + 1) * q = n),
              (selbergCenteredRemainderInt c_lam (T / q) - squarePoleDriftM c_half (T / q)) *
                (liouvilleLambda q : ℝ)) := by
      intro n hn_gt
      have h_beta_eq_s :
          openCoreAdjustedCoeffBeta c_lam c_half T D0 n =
            openCoreSmoothCoeffS c_lam c_half T D0 n :=
        (complete_core_adjusted_expansion_and_compact_gram_tc061r).2.2.2.2.2.1 hn_gt c_lam c_half
      rw [h_beta_eq_s]
      unfold openCoreSmoothCoeffS
      have h_first_empty :
          (Finset.Icc (D_min + 1) (T - 1)).filter (fun d => d ∣ n ∧ n / d ≤ T / d) = ∅ := by
        ext d
        simp only [Finset.mem_filter, Finset.mem_Icc, Finset.not_mem_empty, iff_false]
        rintro ⟨⟨_, _⟩, ⟨hd_dvd, h_div_le⟩⟩
        have h1 : n = d * (n / d) := (Nat.mul_div_cancel' hd_dvd).symm
        have h2 : d * (n / d) ≤ d * (T / d) := Nat.mul_le_mul_left d h_div_le
        have h3 : d * (T / d) ≤ T := Nat.mul_div_le T d
        omega
      change (∑ d ∈ (Finset.Icc (D_min + 1) (T - 1)).filter (fun d => d ∣ n ∧ n / d ≤ T / d), _) -
          (∑ d ∈ (Finset.Icc (D_min + 1) (T - 1)).filter
            (fun d => (d + 1) ∣ n ∧ n / (d + 1) ≤ T / d), _) = _
      rw [h_first_empty, Finset.sum_empty, zero_sub]
      congr 1
      apply Finset.sum_bij (fun d _ => n / (d + 1))
      · intro d hd
        simp only [Finset.mem_filter, Finset.mem_Icc] at hd ⊢
        rcases hd with ⟨⟨hd_lo, hd_hi⟩, ⟨hd1_dvd, hq_le⟩⟩
        let q := n / (d + 1)
        have h_prod : (d + 1) * q = n := Nat.mul_div_cancel' hd1_dvd
        have hq_ge2 : 2 ≤ q := by
          by_contra hlt2
          have hq_le1 : q ≤ 1 := by omega
          have hn_le : n ≤ d + 1 := by
            rw [← h_prod]
            calc (d + 1) * q ≤ (d + 1) * 1 := Nat.mul_le_mul_left (d + 1) hq_le1
              _ = d + 1 := mul_one _
          omega
        have hd_pos : 0 < d := by omega
        have hq_pos : 0 < q := by omega
        have hdq_le_T : d * q ≤ T := by
          rw [mul_comm]
          exact (Nat.le_div_iff_mul_le hd_pos).mp hq_le
        have hd_le_Tq : d ≤ T / q := (Nat.le_div_iff_mul_le hq_pos).mpr hdq_le_T
        have hTq_le_d : T / q ≤ d := by
          by_contra hgt
          have hd1_le : d + 1 ≤ T / q := by omega
          have h_mul : (d + 1) * q ≤ T := (Nat.le_div_iff_mul_le hq_pos).mp hd1_le
          omega
        have hd_eq : T / q = d := le_antisymm hTq_le_d hd_le_Tq
        have hq_hi : q ≤ T / (D_min + 1) := by
          rw [Nat.le_div_iff_mul_le (by omega : 0 < D_min + 1)]
          calc q * (D_min + 1) = (D_min + 1) * q := mul_comm _ _
            _ ≤ d * q := Nat.mul_le_mul_right q hd_lo
            _ ≤ T := hdq_le_T
        exact ⟨⟨hq_ge2, hq_hi⟩, by dsimp [q] at hd_eq h_prod ⊢; rw [hd_eq, h_prod]⟩
      · intro d1 hd1 d2 hd2 h_eq
        simp only [Finset.mem_filter] at hd1 hd2
        have hp1 := Nat.mul_div_cancel' hd1.2.1
        have hp2 := Nat.mul_div_cancel' hd2.2.1
        rw [h_eq] at hp1
        have hq_pos : 0 < n / (d2 + 1) := by
          rcases Nat.eq_zero_or_pos (n / (d2 + 1)) with hz | hpos
          · rw [hz, mul_zero] at hp2; omega
          · exact hpos
        have hd12 : d1 + 1 = d2 + 1 := Nat.eq_of_mul_eq_mul_right hq_pos (hp1.trans hp2.symm)
        omega
      · intro q hq
        simp only [Finset.mem_filter, Finset.mem_Icc] at hq
        rcases hq with ⟨⟨hq2, hq_hi⟩, h_prod_q⟩
        let d := T / q
        have hq_pos : 0 < q := by omega
        have h_dm_q : (D_min + 1) * q ≤ T := by
          rw [mul_comm]
          exact (Nat.le_div_iff_mul_le (by omega : 0 < D_min + 1)).mp hq_hi
        have hd_lo : D_min + 1 ≤ d := (Nat.le_div_iff_mul_le hq_pos).mpr h_dm_q
        have hT_ge2 : 2 ≤ T := by
          calc 2 = 1 * 2 := by norm_num
            _ ≤ (D_min + 1) * q := Nat.mul_le_mul (by omega) hq2
            _ ≤ T := h_dm_q
        have hd_hi : d ≤ T - 1 := by
          have hd_le_half : T / q ≤ T / 2 := Nat.div_le_div_left hq2 (by decide)
          omega
        have hd1_dvd : (d + 1) ∣ n := ⟨q, h_prod_q.symm⟩
        have h_nq_eq : n / (d + 1) = q := by
          rw [← h_prod_q, Nat.mul_div_right q (by omega : 0 < d + 1)]
        have hq_le_Td : n / (d + 1) ≤ T / d := by
          rw [h_nq_eq, Nat.le_div_iff_mul_le (by omega : 0 < d), mul_comm]
          exact Nat.div_mul_le_self T q
        refine ⟨d, ?_, h_nq_eq⟩
        simp only [Finset.mem_filter, Finset.mem_Icc]
        exact ⟨⟨hd_lo, hd_hi⟩, ⟨hd1_dvd, hq_le_Td⟩⟩
      · intro d hd
        simp only [Finset.mem_filter, Finset.mem_Icc] at hd
        rcases hd with ⟨⟨hd_lo, _⟩, ⟨hd1_dvd, hq_le⟩⟩
        let q := n / (d + 1)
        have h_prod : (d + 1) * q = n := Nat.mul_div_cancel' hd1_dvd
        have hq_pos : 0 < q := by
          rcases Nat.eq_zero_or_pos q with hz | hpos
          · dsimp [q] at hz h_prod; rw [hz, mul_zero] at h_prod; omega
          · exact hpos
        have hd_pos : 0 < d := by omega
        have hdq_le_T : d * q ≤ T := by
          rw [mul_comm]
          exact (Nat.le_div_iff_mul_le hd_pos).mp hq_le
        have hd_le_Tq : d ≤ T / q := (Nat.le_div_iff_mul_le hq_pos).mpr hdq_le_T
        have hTq_le_d : T / q ≤ d := by
          by_contra hgt
          have hd1_le : d + 1 ≤ T / q := by omega
          have h_mul : (d + 1) * q ≤ T := (Nat.le_div_iff_mul_le hq_pos).mp hd1_le
          omega
        have hd_eq : d = T / q := le_antisymm hd_le_Tq hTq_le_d
        dsimp [q] at hd_eq
        rw [← hd_eq]
    refine ⟨?_, ?_⟩
    · intro n hn_gt
      have hc := h_coeff hn_gt
      refine ⟨hc, ?_, ?_⟩
      · intro h_nz
        rw [hc, neg_ne_zero] at h_nz
        obtain ⟨q, hq_mem, _⟩ := Finset.exists_ne_zero_of_sum_ne_zero h_nz
        simp only [Finset.mem_filter, Finset.mem_Icc] at hq_mem
        rcases hq_mem with ⟨⟨_, hq_hi⟩, rfl⟩
        have h_mul_le : (T / q) * q ≤ T := Nat.div_mul_le_self T q
        calc
          (T / q + 1) * q = (T / q) * q + q := by ring
          _ ≤ T + T / (D_min + 1) := add_le_add h_mul_le hq_hi
      · intro h_small
        rw [hc]
        have h_div_lt2 : T / (D_min + 1) < 2 := by
          by_contra hge2
          have h2 : 2 ≤ T / (D_min + 1) := by omega
          have h_mul : 2 * (D_min + 1) ≤ T :=
            (Nat.le_div_iff_mul_le (by omega : 0 < D_min + 1)).mp h2
          omega
        have h_empty : Finset.Icc 2 (T / (D_min + 1)) = ∅ := by
          ext q; simp only [Finset.mem_Icc, Finset.not_mem_empty, iff_false]; omega
        simp [h_empty]
    · intro X
      let Q_set := Finset.Icc 2 (T / (D_min + 1))
      have h_maps :
          ∀ q ∈ Q_set, (T / q + 1) * q ∈ Finset.Icc (T + 1) (2 * T) := by
        intro q hq
        rw [Finset.mem_Icc] at hq ⊢
        have hq_pos : 0 < q := by omega
        have h_gt : T < (T / q + 1) * q := by
          have h_mod : T % q < q := Nat.mod_lt T hq_pos
          have h_div_add : q * (T / q) + T % q = T := Nat.div_add_mod T q
          calc
            T = (T / q) * q + T % q := by rw [mul_comm, h_div_add]
            _ < (T / q) * q + q := by omega
            _ = (T / q + 1) * q := by ring
        have hq_le_T : q ≤ T := le_trans hq.2 (Nat.div_le_self T _)
        have h_le_2T : (T / q + 1) * q ≤ 2 * T := by
          calc
            (T / q + 1) * q = (T / q) * q + q := by ring
            _ ≤ T + T := add_le_add (Nat.div_mul_le_self T q) hq_le_T
            _ = 2 * T := by omega
        exact ⟨by omega, h_le_2T⟩
      have h_fib :=
        Finset.sum_fiberwise_of_maps_to h_maps
          (fun q =>
            -((selbergCenteredRemainderInt c_lam (T / q) - squarePoleDriftM c_half (T / q)) *
                (liouvilleLambda q : ℝ) * gaussianTermPhi ((T / q + 1) * q) X))
      rw [Finset.sum_neg_distrib] at h_fib
      rw [← h_fib]
      apply Finset.sum_congr rfl
      intro n hn
      have hn_gt : T < n := by rw [Finset.mem_Icc] at hn; omega
      rw [h_coeff hn_gt, neg_mul, Finset.sum_mul, ← Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro q hq
      have h_eq_n : (T / q + 1) * q = n := (Finset.mem_filter.mp hq).2
      rw [h_eq_n]
  have h_part3a :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        4 * inheritedPrimePowerDiagDtilde T Y +
            4 * inheritedPrimePowerSelfCollisionXself T Y +
            truncatedSignedRemainderF c_lam c_half T D0 Y =
          windowEnergyNormSq Y (truncatedAdjustedCoreU c_lam c_half T D0) ∧
          4 * inheritedPrimePowerDiagDtilde T Y +
              4 * inheritedPrimePowerSelfCollisionXself T Y +
              completeSignedRemainderF c_lam c_half T D0 Y =
            windowEnergyNormSq Y
              (fun X =>
                truncatedAdjustedCoreU c_lam c_half T D0 X +
                  spilloverFringeS c_lam c_half T D0 X) := by
    intro Y hY2 T hT D0 c_lam c_half
    obtain ⟨_, hprops⟩ := uIcc_tau_props_tc062_aux hY2
    have h_sub_id :=
      subset_hcal_bilinear_eq_windowNorm_sub_tc062_aux hY2 hT D0 c_lam c_half
        (Finset.Icc 1 T) (Finset.Subset.refl _)
    have hD_eq :
        subsetPrimePowerDiagDtilde (Finset.Icc 1 T) Y = inheritedPrimePowerDiagDtilde T Y :=
      (((finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).1 hY2 T).1).symm
    have hX_eq :
        subsetPrimePowerSelfCollisionXself (Finset.Icc 1 T) Y =
          inheritedPrimePowerSelfCollisionXself T Y := rfl
    have hU_congr :
        windowEnergyNormSq Y
            (fun X =>
              ∑ n ∈ Finset.Icc 1 T,
                (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) =
          windowEnergyNormSq Y (truncatedAdjustedCoreU c_lam c_half T D0) := by
      unfold windowEnergyNormSq windowPairing
      apply intervalIntegral.integral_congr
      intro X _hX
      have h_pt_U :
          (∑ n ∈ Finset.Icc 1 T,
              (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) =
            truncatedAdjustedCoreU c_lam c_half T D0 X := by
        unfold truncatedAdjustedCoreU finiteQLambda adjustedStationProfilePsi signedAdjustedCoeffB
        have hQ :
            X ^ (5 / 2 : ℝ) *
                ∑ n ∈ Finset.Icc 1 T,
                  (liouvilleLambda n : ℝ) * ((n : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (n : ℝ) ^ 2) =
              ∑ n ∈ Finset.Icc 1 T, (liouvilleLambda n : ℝ) * gaussianTermPhi n X := by
          unfold gaussianTermPhi
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl; intro n _; ring
        rw [hQ, Finset.sum_div, ← Finset.sum_sub_distrib]
        apply Finset.sum_congr rfl
        intro n hn
        have hn1 : 1 ≤ n := (Finset.mem_Icc.mp hn).1
        have hsq := liouvilleLambda_sq_eq_one_tc062_aux hn1
        calc
          (liouvilleLambda n : ℝ) *
              ((1 - (liouvilleLambda n : ℝ) * openCoreAdjustedCoeffBeta c_lam c_half T D0 n /
                  (Real.log X) ^ 2) *
                gaussianTermPhi n X)
            = (liouvilleLambda n : ℝ) * gaussianTermPhi n X -
                (((liouvilleLambda n : ℝ) * (liouvilleLambda n : ℝ)) *
                  openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) /
                  (Real.log X) ^ 2 := by ring
          _ = (liouvilleLambda n : ℝ) * gaussianTermPhi n X -
                openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X /
                  (Real.log X) ^ 2 := by rw [hsq, one_mul]
      dsimp only
      rw [h_pt_U]
    have h_id_trunc :
        4 * inheritedPrimePowerDiagDtilde T Y +
            4 * inheritedPrimePowerSelfCollisionXself T Y +
            truncatedSignedRemainderF c_lam c_half T D0 Y =
          windowEnergyNormSq Y (truncatedAdjustedCoreU c_lam c_half T D0) := by
      unfold truncatedSignedRemainderF at *
      rw [hD_eq, hX_eq, hU_congr] at h_sub_id
      linarith
    have h_J_split :=
      (signed_remainder_equivalence_and_sufficient_core_relaxation_tc061r).1.2.2.1
        c_lam c_half T D0 Y
    have h_4DJ :=
      ((mixed_covariance_identity_and_theta_energy_bound_tc061).2.2.1 hY2 hT D0 c_lam c_half).1
    have h_full_congr :
        windowEnergyNormSq Y
            (fun X =>
              2 * normalizedPrimePowerTermP T X - openCoreOscShiftD2Part c_lam c_half T D0 X) =
          windowEnergyNormSq Y
            (fun X =>
              truncatedAdjustedCoreU c_lam c_half T D0 X +
                spilloverFringeS c_lam c_half T D0 X) := by
      unfold windowEnergyNormSq windowPairing
      apply intervalIntegral.integral_congr
      intro X hX
      have hX_pos : 0 < X := (hprops X hX).2.1
      have hlog_ne : Real.log X ≠ 0 := (hprops X hX).2.2.2.1
      have h_br :=
        ((complete_core_adjusted_expansion_and_compact_gram_tc061r).2.2.1 hT D0 c_lam c_half
          hX_pos hlog_ne).2.1
      have h_icc_u : Finset.Icc 1 (2 * T) = Finset.Icc 1 T ∪ Finset.Icc (T + 1) (2 * T) := by
        ext k; simp only [Finset.mem_Icc, Finset.mem_union]; omega
      have h_icc_d : Disjoint (Finset.Icc 1 T) (Finset.Icc (T + 1) (2 * T)) := by
        rw [Finset.disjoint_left]; intro k h1 h2; simp only [Finset.mem_Icc] at h1 h2; omega
      have h_sum_sp :
          (∑ n ∈ Finset.Icc 1 (2 * T),
              openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) =
            (∑ n ∈ Finset.Icc 1 T,
                openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) +
              (∑ n ∈ Finset.Icc (T + 1) (2 * T),
                openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) := by
        conv_lhs => rw [h_icc_u]
        exact Finset.sum_union h_icc_d
      have h_pt_eq :
          2 * normalizedPrimePowerTermP T X - openCoreOscShiftD2Part c_lam c_half T D0 X =
            truncatedAdjustedCoreU c_lam c_half T D0 X +
              spilloverFringeS c_lam c_half T D0 X := by
        rw [h_br, h_sum_sp]
        unfold truncatedAdjustedCoreU spilloverFringeS
        ring
      dsimp only
      rw [h_pt_eq]
    exact ⟨h_id_trunc, by linarith [h_J_split, h_4DJ, h_full_congr]⟩
  have h_part3b :
      ∀ (c_lam c_half : ℝ),
        ∃ C_sp : ℝ, 0 ≤ C_sp ∧
          ∀ {Y : ℝ}, 2 ≤ Y →
            windowEnergyNormSq Y (canonicalSpilloverFringeS c_lam c_half Y) ≤
              C_sp * (Real.log Y) ^ 2 := by
    intro c_lam c_half
    let M_c : ℝ :=
      RiemannScope.tau ^ (5 / 2 : ℝ) * (9 / 4 : ℝ) *
        ((9 / 4 : ℝ) ^ 2 + 18 + 4 * (|c_lam| + |c_half|))
    let C_sp : ℝ := (RiemannScope.tau - 1) * M_c ^ 2
    have htau_bds := tau_gt_one_and_lt_eight_tc062_aux
    have htau_pos : 0 < RiemannScope.tau := by linarith [htau_bds.1]
    have hCsp_nn : 0 ≤ C_sp := mul_nonneg (by linarith [htau_bds.1]) (sq_nonneg M_c)
    refine ⟨C_sp, hCsp_nn, ?_⟩
    intro Y hY2
    obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc062_aux hY2
    obtain ⟨hT_ge2, _, _, hlogT_le, hY52_le, _, hlogY_gt_half⟩ :=
      canonicalCutoffT_bounds_tc062_aux hY2
    let T := canonicalCutoffT Y
    let D0 := Nat.floor (Real.log Y)
    have hT1 : 1 ≤ T := by omega
    have hT_pos_r : (0 : ℝ) < (T : ℝ) := by exact_mod_cast (by omega : 0 < T)
    have hlogY_pos : 0 < Real.log Y := by linarith
    have h1_le_2logY : 1 ≤ 2 * Real.log Y := by linarith
    have h1_le_4logY_sq : 1 ≤ 4 * (Real.log Y) ^ 2 := by
      have hsq := pow_le_pow_left (by norm_num) (le_of_lt hlogY_gt_half) 2
      linarith
    have h_pt_sp :
        ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
          |canonicalSpilloverFringeS c_lam c_half Y X| ≤ M_c * Real.log Y := by
      intro X hX
      have hX_Icc : Y ≤ X ∧ X ≤ RiemannScope.tau * Y := by
        rwa [Set.uIcc_of_le hle, Set.mem_Icc] at hX
      have hlogX_ge : Real.log Y ≤ Real.log X :=
        Real.log_le_log (by linarith) hX_Icc.1
      have hlogX_sq_ge : (Real.log Y) ^ 2 ≤ (Real.log X) ^ 2 :=
        pow_le_pow_left (le_of_lt hlogY_pos) hlogX_ge 2
      unfold canonicalSpilloverFringeS spilloverFringeS
      change |-(∑ n ∈ Finset.Icc (T + 1) (2 * T),
          openCoreAdjustedCoeffBeta c_lam c_half T D0 n * gaussianTermPhi n X) /
          (Real.log X) ^ 2| ≤ _
      have hlogX_sq_abs : |(Real.log X) ^ 2| = (Real.log X) ^ 2 :=
        abs_of_pos (sq_pos_of_pos (hprops X hX).2.2.1)
      rw [(h_part1 hT1 D0 c_lam c_half).2 X, neg_neg, abs_div, hlogX_sq_abs]
      let Q_set := Finset.Icc 2 (T / (min D0 (T - 1) + 1))
      have h_sub_Q : Q_set ⊆ Finset.Icc 2 T := by
        intro q hq
        rw [Finset.mem_Icc] at hq ⊢
        exact ⟨hq.1, le_trans hq.2 (Nat.div_le_self T _)⟩
      have h_sum_bd :
          |∑ q ∈ Q_set,
              (selbergCenteredRemainderInt c_lam (T / q) - squarePoleDriftM c_half (T / q)) *
                (liouvilleLambda q : ℝ) * gaussianTermPhi ((T / q + 1) * q) X| ≤
            M_c * (Real.log Y) ^ 3 := by
        let B_coeff : ℝ :=
          (Real.log (T : ℝ)) ^ 2 + 4 * Real.log (T : ℝ) + |c_lam| + |c_half|
        have hB_nn : 0 ≤ B_coeff :=
          add_nonneg
            (add_nonneg
              (add_nonneg (sq_nonneg _)
                (mul_nonneg (by norm_num) (Real.log_nonneg (by exact_mod_cast hT1))))
              (abs_nonneg _))
            (abs_nonneg _)
        have h_each_q :
            ∀ q ∈ Q_set,
              |(selbergCenteredRemainderInt c_lam (T / q) - squarePoleDriftM c_half (T / q)) *
                  (liouvilleLambda q : ℝ) * gaussianTermPhi ((T / q + 1) * q) X| ≤
                (1 / (q : ℝ)) *
                  (B_coeff * (RiemannScope.tau * Y) ^ (5 / 2 : ℝ) / (T : ℝ) ^ 2) := by
          intro q hq
          have hq_Icc := Finset.mem_Icc.mp (h_sub_Q hq)
          have hq_pos : 0 < q := by omega
          have hd_ge1 : 1 ≤ T / q := by
            have h_dm : (min D0 (T - 1) + 1) * q ≤ T := by
              rw [mul_comm]
              exact (Nat.le_div_iff_mul_le (by omega)).mp (Finset.mem_Icc.mp hq).2
            exact (Nat.le_div_iff_mul_le hq_pos).mpr
              (le_trans (Nat.mul_le_mul_right q (by omega : 1 ≤ min D0 (T - 1) + 1)) h_dm)
          have hd_le_T : T / q ≤ T := Nat.div_le_self T q
          have hd_real_le : ((T / q : ℕ) : ℝ) ≤ (T : ℝ) / (q : ℝ) := by
            have hm : ((T / q : ℕ) : ℝ) * (q : ℝ) ≤ (T : ℝ) := by
              exact_mod_cast Nat.div_mul_le_self T q
            exact (le_div_iff (by positivity)).mpr hm
          have hw_bd := centered_minus_drift_abs_le_tc062_aux c_lam c_half hd_ge1 hd_le_T
          have hnq_gt_T : T ≤ (T / q + 1) * q := by
            have h_mod : T % q < q := Nat.mod_lt T hq_pos
            have h_div_add : q * (T / q) + T % q = T := Nat.div_add_mod T q
            calc T = (T / q) * q + T % q := by rw [mul_comm, h_div_add]
              _ ≤ (T / q) * q + q := by omega
              _ = (T / q + 1) * q := by ring
          have hphi_bds :=
            gaussianTermPhi_le_of_ge_tc062_aux hY2 hX hT_pos_r (by exact_mod_cast hnq_gt_T)
          have hlam_abs : |(liouvilleLambda q : ℝ)| = 1 :=
            abs_liouvilleLambda_eq_one_tc062_aux (le_trans (by decide : 1 ≤ 2) hq_Icc.1)
          rw [abs_mul, abs_mul, hlam_abs, mul_one, abs_of_nonneg hphi_bds.1]
          have hw_le2 :
              |selbergCenteredRemainderInt c_lam (T / q) - squarePoleDriftM c_half (T / q)| ≤
                ((T : ℝ) / (q : ℝ)) * B_coeff :=
            le_trans hw_bd (mul_le_mul_of_nonneg_right hd_real_le hB_nn)
          calc
            |selbergCenteredRemainderInt c_lam (T / q) - squarePoleDriftM c_half (T / q)| *
                gaussianTermPhi ((T / q + 1) * q) X
              ≤ (((T : ℝ) / (q : ℝ)) * B_coeff) *
                  ((RiemannScope.tau * Y) ^ (5 / 2 : ℝ) / (T : ℝ) ^ 3) :=
                mul_le_mul hw_le2 hphi_bds.2 hphi_bds.1 (by positivity)
            _ = (1 / (q : ℝ)) *
                  (B_coeff * (RiemannScope.tau * Y) ^ (5 / 2 : ℝ) / (T : ℝ) ^ 2) := by
                field_simp [ne_of_gt hT_pos_r]; ring
        have h_harm : (∑ q ∈ Q_set, (1 / (q : ℝ))) ≤ (9 / 4 : ℝ) * Real.log Y :=
          le_trans
            (le_trans (Finset.sum_le_sum_of_subset_of_nonneg h_sub_Q (fun _ _ _ => by positivity))
              (sum_inv_Icc_two_le_log_tc062_aux T hT1))
            hlogT_le
        have h_tau_split :
            (RiemannScope.tau * Y) ^ (5 / 2 : ℝ) =
              RiemannScope.tau ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ) :=
          Real.mul_rpow (le_of_lt htau_pos) (by linarith)
        have h_ratio_le1 : Y ^ (5 / 2 : ℝ) / (T : ℝ) ^ 2 ≤ 1 :=
          (div_le_one (sq_pos_of_pos hT_pos_r)).mpr hY52_le
        have hB_logY :
            B_coeff ≤ ((9 / 4 : ℝ) ^ 2 + 18 + 4 * (|c_lam| + |c_half|)) * (Real.log Y) ^ 2 := by
          have hlT_nn : 0 ≤ Real.log (T : ℝ) := Real.log_nonneg (by exact_mod_cast hT1)
          have hlT_sq : (Real.log (T : ℝ)) ^ 2 ≤ (9 / 4 : ℝ) ^ 2 * (Real.log Y) ^ 2 := by
            have hp := pow_le_pow_left hlT_nn hlogT_le 2
            linarith [show ((9 / 4 : ℝ) * Real.log Y) ^ 2 =
              (9 / 4 : ℝ) ^ 2 * (Real.log Y) ^ 2 by ring]
          have hlT_lin : 4 * Real.log (T : ℝ) ≤ 18 * (Real.log Y) ^ 2 := by
            have h1 : 4 * Real.log (T : ℝ) ≤ 9 * Real.log Y := by linarith
            have h2 : 9 * Real.log Y ≤ 9 * (Real.log Y * (2 * Real.log Y)) :=
              mul_le_mul_of_nonneg_left
                (le_mul_of_one_le_right (le_of_lt hlogY_pos) h1_le_2logY) (by norm_num)
            linarith only [h1, h2, show 9 * (Real.log Y * (2 * Real.log Y)) = 18 * (Real.log Y) ^ 2 by ring]
          have h_c_abs : |c_lam| + |c_half| ≤ 4 * (|c_lam| + |c_half|) * (Real.log Y) ^ 2 := by
            have h1 := mul_le_mul_of_nonneg_left h1_le_4logY_sq
              (show 0 ≤ |c_lam| + |c_half| by positivity)
            linarith [show (|c_lam| + |c_half|) * (4 * (Real.log Y) ^ 2) =
              4 * (|c_lam| + |c_half|) * (Real.log Y) ^ 2 by ring]
          dsimp [B_coeff]
          linarith
        have h_factor_le :
            B_coeff * (RiemannScope.tau * Y) ^ (5 / 2 : ℝ) / (T : ℝ) ^ 2 ≤
              RiemannScope.tau ^ (5 / 2 : ℝ) *
                ((9 / 4 : ℝ) ^ 2 + 18 + 4 * (|c_lam| + |c_half|)) * (Real.log Y) ^ 2 := by
          rw [h_tau_split, show B_coeff * (RiemannScope.tau ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ)) /
              (T : ℝ) ^ 2 =
            RiemannScope.tau ^ (5 / 2 : ℝ) * B_coeff * (Y ^ (5 / 2 : ℝ) / (T : ℝ) ^ 2) by ring]
          have h1 :
              RiemannScope.tau ^ (5 / 2 : ℝ) * B_coeff * (Y ^ (5 / 2 : ℝ) / (T : ℝ) ^ 2) ≤
                RiemannScope.tau ^ (5 / 2 : ℝ) * B_coeff * 1 :=
            mul_le_mul_of_nonneg_left h_ratio_le1 (by positivity)
          have h2 :
              RiemannScope.tau ^ (5 / 2 : ℝ) * B_coeff ≤
                RiemannScope.tau ^ (5 / 2 : ℝ) *
                  (((9 / 4 : ℝ) ^ 2 + 18 + 4 * (|c_lam| + |c_half|)) * (Real.log Y) ^ 2) :=
            mul_le_mul_of_nonneg_left hB_logY (by positivity)
          linarith
        calc
          |∑ q ∈ Q_set,
              (selbergCenteredRemainderInt c_lam (T / q) - squarePoleDriftM c_half (T / q)) *
                (liouvilleLambda q : ℝ) * gaussianTermPhi ((T / q + 1) * q) X|
            ≤ ∑ q ∈ Q_set,
                |(selbergCenteredRemainderInt c_lam (T / q) - squarePoleDriftM c_half (T / q)) *
                  (liouvilleLambda q : ℝ) * gaussianTermPhi ((T / q + 1) * q) X| :=
              Finset.abs_sum_le_sum_abs _ _
          _ ≤ ∑ q ∈ Q_set,
                (1 / (q : ℝ)) *
                  (B_coeff * (RiemannScope.tau * Y) ^ (5 / 2 : ℝ) / (T : ℝ) ^ 2) :=
              Finset.sum_le_sum h_each_q
          _ = (∑ q ∈ Q_set, (1 / (q : ℝ))) *
                (B_coeff * (RiemannScope.tau * Y) ^ (5 / 2 : ℝ) / (T : ℝ) ^ 2) :=
              (Finset.sum_mul _ _ _).symm
          _ ≤ ((9 / 4 : ℝ) * Real.log Y) *
                (RiemannScope.tau ^ (5 / 2 : ℝ) *
                  ((9 / 4 : ℝ) ^ 2 + 18 + 4 * (|c_lam| + |c_half|)) * (Real.log Y) ^ 2) :=
              mul_le_mul h_harm h_factor_le (by positivity) (by positivity)
          _ = M_c * (Real.log Y) ^ 3 := by dsimp [M_c]; ring
      rw [div_le_iff (sq_pos_of_pos (hprops X hX).2.2.1)]
      calc
        |∑ q ∈ Q_set,
            (selbergCenteredRemainderInt c_lam (T / q) - squarePoleDriftM c_half (T / q)) *
              (liouvilleLambda q : ℝ) * gaussianTermPhi ((T / q + 1) * q) X|
          ≤ M_c * (Real.log Y) ^ 3 := h_sum_bd
        _ = (M_c * Real.log Y) * (Real.log Y) ^ 2 := by ring
        _ ≤ (M_c * Real.log Y) * (Real.log X) ^ 2 :=
            mul_le_mul_of_nonneg_left hlogX_sq_ge (by positivity)
    have h_sp_cont :
        ContinuousOn (canonicalSpilloverFringeS c_lam c_half Y)
          (Set.uIcc Y (RiemannScope.tau * Y)) := by
      unfold canonicalSpilloverFringeS spilloverFringeS
      have hlog_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
        ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1)
      exact ((continuousOn_finset_sum _ (fun n _ =>
        continuousOn_const.mul (continuousOn_gaussianTermPhi_uIcc_tc062_aux Y n))).neg).div
        (hlog_cont.pow 2) (fun X hX => (hprops X hX).2.2.2.2)
    have h_sp_int :
        IntervalIntegrable
          (fun X =>
            canonicalSpilloverFringeS c_lam c_half Y X *
              canonicalSpilloverFringeS c_lam c_half Y X / X)
          volume Y (RiemannScope.tau * Y) :=
      ((h_sp_cont.mul h_sp_cont).div continuousOn_id
        (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
    have h_const_int :
        IntervalIntegrable (fun _ : ℝ => (M_c * Real.log Y) ^ 2 / Y)
          volume Y (RiemannScope.tau * Y) := intervalIntegrable_const
    unfold windowEnergyNormSq windowPairing
    have h_int_le :=
      intervalIntegral.integral_mono_on hle h_sp_int h_const_int (by
        intro X hX
        have hX_in : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
        have hX_Icc : Y ≤ X ∧ X ≤ RiemannScope.tau * Y := hX
        have hX_pos : 0 < X := by linarith
        have habs := h_pt_sp X hX_in
        have hsq :
            canonicalSpilloverFringeS c_lam c_half Y X *
                canonicalSpilloverFringeS c_lam c_half Y X ≤
              (M_c * Real.log Y) ^ 2 := by
          have h1 := pow_le_pow_left (abs_nonneg _) habs 2
          rwa [sq_abs, sq] at h1
        calc
          canonicalSpilloverFringeS c_lam c_half Y X *
              canonicalSpilloverFringeS c_lam c_half Y X / X
            ≤ (M_c * Real.log Y) ^ 2 / X :=
              div_le_div_of_nonneg_right hsq (le_of_lt hX_pos)
          _ ≤ (M_c * Real.log Y) ^ 2 / Y :=
              div_le_div_of_nonneg_left (sq_nonneg _) (by linarith) hX_Icc.1)
    rw [intervalIntegral.integral_const, smul_eq_mul] at h_int_le
    have h_rhs_eq :
        (RiemannScope.tau * Y - Y) * ((M_c * Real.log Y) ^ 2 / Y) =
          C_sp * (Real.log Y) ^ 2 := by
      dsimp [C_sp]
      field_simp [show Y ≠ 0 by linarith]
      ring
    linarith
  have h_part3c :
      ∀ (c_lam c_half : ℝ),
        MixedCovarianceClosureHypothesis
            (canonicalSignedRemainderF c_lam c_half) canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalTruncatedSignedRemainderF c_lam c_half) canonicalPrimePowerDiagDtilde := by
    intro c_lam c_half
    obtain ⟨C_sp, hCsp_nn, hCsp_bd⟩ := h_part3b c_lam c_half
    have h_self_bds :=
      (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2
    let C_self : ℝ := 186 * (RiemannScope.tau - 1)
    have hCself_nn : 0 ≤ C_self := le_of_lt h_self_bds.1
    have hD_nn : ∀ Y : ℝ, 2 ≤ Y → 0 ≤ canonicalPrimePowerDiagDtilde Y :=
      fun Y hY2 => (signed_remainder_equivalence_and_sufficient_core_relaxation_tc061r).1.2.1 hY2
    let C_err : ℝ := 4 * C_self + 2 * C_sp
    have hCerr_nn : 0 ≤ C_err := by dsimp [C_err]; positivity
    have h_both :
        ∀ Y : ℝ, Real.exp 1 ≤ Y →
          canonicalTruncatedSignedRemainderF c_lam c_half Y ≤
              (1 + 1 / Real.log Y) * canonicalSignedRemainderF c_lam c_half Y +
                (12 / Real.log Y) * canonicalPrimePowerDiagDtilde Y +
                C_err * (Real.log Y) ^ 3 ∧
            canonicalSignedRemainderF c_lam c_half Y ≤
              (1 + 1 / Real.log Y) * canonicalTruncatedSignedRemainderF c_lam c_half Y +
                (12 / Real.log Y) * canonicalPrimePowerDiagDtilde Y +
                C_err * (Real.log Y) ^ 3 := by
      intro Y hY_ge_e
      have he_ge2 : (2 : ℝ) ≤ Real.exp 1 := by
        linarith [Real.add_one_le_exp (1 : ℝ)]
      have hY2 : 2 ≤ Y := le_trans he_ge2 hY_ge_e
      have hT1 : 1 ≤ canonicalCutoffT Y := canonicalCutoffT_ge_one_tc062_aux (by linarith)
      have hlog_ge1 : 1 ≤ Real.log Y := by
        have h := Real.log_le_log (Real.exp_pos 1) hY_ge_e
        rwa [Real.log_exp] at h
      have hlog_pos : 0 < Real.log Y := lt_of_lt_of_le zero_lt_one hlog_ge1
      let δ : ℝ := 1 / Real.log Y
      have hδ_pos : 0 < δ := by dsimp [δ]; positivity
      have hδ_le1 : δ ≤ 1 := div_le_one_of_le hlog_ge1 (le_of_lt hlog_pos)
      have h1_div_δ : 1 / δ = Real.log Y := one_div_one_div (Real.log Y)
      obtain ⟨_, hprops⟩ := uIcc_tau_props_tc062_aux hY2
      let T := canonicalCutoffT Y
      let D0 := Nat.floor (Real.log Y)
      have hlog_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
        ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1)
      have hU_cont :
          ContinuousOn (truncatedAdjustedCoreU c_lam c_half T D0)
            (Set.uIcc Y (RiemannScope.tau * Y)) := by
        have hQ_eq :
            finiteQLambda T =
              fun X => ∑ n ∈ Finset.Icc 1 T, (liouvilleLambda n : ℝ) * gaussianTermPhi n X := by
          ext X
          unfold finiteQLambda gaussianTermPhi
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro n _; ring
        unfold truncatedAdjustedCoreU
        rw [hQ_eq]
        exact (continuousOn_finset_sum _ (fun n _ =>
          continuousOn_const.mul (continuousOn_gaussianTermPhi_uIcc_tc062_aux Y n))).sub
          ((continuousOn_finset_sum _ (fun n _ =>
            continuousOn_const.mul (continuousOn_gaussianTermPhi_uIcc_tc062_aux Y n))).div
            (hlog_cont.pow 2) (fun X hX => (hprops X hX).2.2.2.2))
      have hS_cont :
          ContinuousOn (spilloverFringeS c_lam c_half T D0)
            (Set.uIcc Y (RiemannScope.tau * Y)) := by
        unfold spilloverFringeS
        exact ((continuousOn_finset_sum _ (fun n _ =>
          continuousOn_const.mul (continuousOn_gaussianTermPhi_uIcc_tc062_aux Y n))).neg).div
          (hlog_cont.pow 2) (fun X hX => (hprops X hX).2.2.2.2)
      obtain ⟨hy_fwd, hy_rev⟩ := windowEnergyNormSq_young_add_tc062_aux hY2 hU_cont hS_cont hδ_pos
      obtain ⟨hid_trunc, hid_full⟩ := h_part3a hY2 hT1 D0 c_lam c_half
      rw [← hid_full, ← hid_trunc] at hy_fwd hy_rev
      have hXself_bds := h_self_bds.2.2 hY2 T
      have hXself_nn : 0 ≤ inheritedPrimePowerSelfCollisionXself T Y := hXself_bds.1
      have hXself_le : inheritedPrimePowerSelfCollisionXself T Y ≤ C_self :=
        le_trans hXself_bds.2.1 hXself_bds.2.2
      have hD_Y_nn : 0 ≤ canonicalPrimePowerDiagDtilde Y := hD_nn Y hY2
      have hSp_le : windowEnergyNormSq Y (spilloverFringeS c_lam c_half T D0) ≤
          C_sp * (Real.log Y) ^ 2 := hCsp_bd hY2
      have hSp_nn : 0 ≤ windowEnergyNormSq Y (spilloverFringeS c_lam c_half T D0) := by
        obtain ⟨hle_Y, _⟩ := uIcc_tau_props_tc062_aux hY2
        unfold windowEnergyNormSq windowPairing
        apply intervalIntegral.integral_nonneg hle_Y
        intro X hX
        exact div_nonneg (mul_self_nonneg _) (by rw [Set.mem_Icc] at hX; linarith)
      have h_sp_term :
          (1 + 1 / δ) * windowEnergyNormSq Y (spilloverFringeS c_lam c_half T D0) ≤
            2 * C_sp * (Real.log Y) ^ 3 := by
        rw [h1_div_δ]
        have h1_log : 1 + Real.log Y ≤ 2 * Real.log Y := by linarith
        calc
          (1 + Real.log Y) * windowEnergyNormSq Y (spilloverFringeS c_lam c_half T D0)
            ≤ (2 * Real.log Y) * (C_sp * (Real.log Y) ^ 2) :=
              mul_le_mul h1_log hSp_le hSp_nn (by positivity)
          _ = 2 * C_sp * (Real.log Y) ^ 3 := by ring
      have h_log3_ge1 : 1 ≤ (Real.log Y) ^ 3 := by
        simpa using pow_le_pow_left zero_le_one hlog_ge1 3
      have h_xself_term :
          4 * δ * inheritedPrimePowerSelfCollisionXself T Y ≤
            4 * C_self * (Real.log Y) ^ 3 := by
        calc
          4 * δ * inheritedPrimePowerSelfCollisionXself T Y
            ≤ 4 * 1 * C_self :=
              mul_le_mul (by linarith : 4 * δ ≤ 4 * 1) hXself_le hXself_nn (by norm_num)
          _ = 4 * C_self * 1 := by ring
          _ ≤ 4 * C_self * (Real.log Y) ^ 3 :=
              mul_le_mul_of_nonneg_left h_log3_ge1 (by positivity)
      have hD_term :
          4 * δ * inheritedPrimePowerDiagDtilde T Y ≤
            (12 / Real.log Y) * canonicalPrimePowerDiagDtilde Y := by
        change 4 * (1 / Real.log Y) * canonicalPrimePowerDiagDtilde Y ≤
          (12 / Real.log Y) * canonicalPrimePowerDiagDtilde Y
        have h4_12 : 4 * (1 / Real.log Y) ≤ 12 / Real.log Y := by
          rw [show 4 * (1 / Real.log Y) = 4 / Real.log Y by ring]
          exact div_le_div_of_nonneg_right (by norm_num) (le_of_lt hlog_pos)
        exact mul_le_mul_of_nonneg_right h4_12 hD_Y_nn
      unfold canonicalTruncatedSignedRemainderF canonicalSignedRemainderF
        canonicalPrimePowerDiagDtilde at *
      dsimp only [T, D0, δ, C_err] at hy_fwd hy_rev h_sp_term h_xself_term hD_term ⊢
      exact ⟨by linarith only [hy_rev, h_sp_term, h_xself_term, hD_term],
        by linarith only [hy_fwd, h_sp_term, h_xself_term, hD_term]⟩
    exact ⟨mixedCovarianceClosure_of_log_perturbation_tc062_aux hCerr_nn hD_nn
        (fun Y hY => (h_both Y hY).1),
      mixedCovarianceClosure_of_log_perturbation_tc062_aux hCerr_nn hD_nn
        (fun Y hY => (h_both Y hY).2)⟩
  exact ⟨h_part1, selbergWeight2_and_cumulative_abs_le_tc062_aux,
    ⟨h_part3a, h_part3b, h_part3c,
      h_part3c actualSelbergConstantCLam actualSquarePoleConstantCHalf⟩⟩

/-! ### Section 5: Stage A Interior Hilbert Split & Candidate Lemma A1 Refutation (`TASK-TC-062` §6 Stage A) -/

/-- Interior `p`-adic anchors whose `p`-dilate remains inside the primary cutoff `[1, T]`. -/
def primeInteriorTruncatedAnchors (p T : ℕ) : Finset ℕ :=
  (primeEvenValuationAnchors p (2 * T)).filter (fun m => p * m ≤ T)

/-- Union `Ω_p(T) := I_p(T) ∪ p * I_p(T)` of interior stations covered by complete `[1, T]` pairs. -/
def coveredInteriorStations (p T : ℕ) : Finset ℕ :=
  primeInteriorTruncatedAnchors p T ∪ (primeInteriorTruncatedAnchors p T).image (fun m => p * m)

/-- Uncovered cutoff-strip stations `[1, T] \ Ω_p(T)`. -/
def uncoveredCutoffStripStations (p T : ℕ) : Finset ℕ :=
  Finset.Icc 1 T \ coveredInteriorStations p T

/-- Interior `p`-paired signed remainder functional on `primeInteriorTruncatedAnchors p T`. -/
noncomputable def interiorPairedRemainderF (c_lam c_half : ℝ) (p T D0 : ℕ) (Y : ℝ) : ℝ :=
  ∑ m ∈ primeInteriorTruncatedAnchors p T,
    ∑ n ∈ primeInteriorTruncatedAnchors p T,
      (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
        (completeSignedKernelHcal c_lam c_half T D0 Y m n -
          completeSignedKernelHcal c_lam c_half T D0 Y (p * m) n -
          completeSignedKernelHcal c_lam c_half T D0 Y m (p * n) +
          completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * n))

/-- Canonical-schedule interior `p`-paired signed remainder functional. -/
noncomputable def canonicalInteriorPairedRemainderF (c_lam c_half : ℝ) (p : ℕ) (Y : ℝ) : ℝ :=
  interiorPairedRemainderF c_lam c_half p (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y

private theorem coveredInteriorStations_props_tc062_aux {p : ℕ} (hp : p.Prime) (T : ℕ) :
    coveredInteriorStations p T ⊆ Finset.Icc 1 T ∧
      Disjoint (primeInteriorTruncatedAnchors p T)
        ((primeInteriorTruncatedAnchors p T).image (fun m => p * m)) ∧
      (∀ k ∈ uncoveredCutoffStripStations p T,
        T / p < k ∧ k ≤ T ∧ Even (k.factorization p)) ∧
      (∀ (f : ℕ → ℝ),
        (∑ n ∈ coveredInteriorStations p T, f n) =
          ∑ m ∈ primeInteriorTruncatedAnchors p T, (f m + f (p * m))) := by
  have h_sub : coveredInteriorStations p T ⊆ Finset.Icc 1 T := by
    intro k hk
    simp only [coveredInteriorStations, Finset.mem_union, Finset.mem_image,
      primeInteriorTruncatedAnchors, primeEvenValuationAnchors, Finset.mem_filter,
      Finset.mem_Icc] at hk ⊢
    rcases hk with ⟨⟨⟨hk1, _⟩, _⟩, hpkT⟩ | ⟨m, ⟨⟨⟨hm1, _⟩, _⟩, hpmT⟩, rfl⟩
    · exact ⟨hk1, le_trans (Nat.le_mul_of_pos_left k hp.pos) hpkT⟩
    · exact ⟨Nat.mul_pos hp.pos hm1, hpmT⟩
  have h_disj :
      Disjoint (primeInteriorTruncatedAnchors p T)
        ((primeInteriorTruncatedAnchors p T).image (fun m => p * m)) := by
    rw [Finset.disjoint_left]
    intro k hk1 hk2
    simp only [primeInteriorTruncatedAnchors, primeEvenValuationAnchors, Finset.mem_filter,
      Finset.mem_Icc, Finset.mem_image] at hk1 hk2
    rcases hk1 with ⟨⟨⟨_, _⟩, hk_ev⟩, _⟩
    rcases hk2 with ⟨m, ⟨⟨⟨hm1, _⟩, hm_ev⟩, _⟩, rfl⟩
    rw [factorization_prime_mul_self_tc062_aux hp hm1] at hk_ev
    obtain ⟨r1, _⟩ := hm_ev
    obtain ⟨r2, _⟩ := hk_ev
    omega
  have h_uncov :
      ∀ k ∈ uncoveredCutoffStripStations p T,
        T / p < k ∧ k ≤ T ∧ Even (k.factorization p) := by
    intro k hk
    simp only [uncoveredCutoffStripStations, Finset.mem_sdiff, Finset.mem_Icc] at hk
    rcases hk with ⟨⟨hk1, hkT⟩, hk_not⟩
    have hk_ev : Even (k.factorization p) := by
      by_contra hk_odd
      have hp_dvd : p ∣ k := by
        by_contra hnd
        rw [Nat.factorization_eq_zero_of_not_dvd hnd] at hk_odd
        exact hk_odd even_zero
      obtain ⟨m, rfl⟩ := hp_dvd
      have hm1 : 1 ≤ m := by
        rcases Nat.eq_zero_or_pos m with hz | hpos
        · rw [hz, mul_zero] at hk1; omega
        · exact hpos
      have hm_ev : Even (m.factorization p) := by
        rw [factorization_prime_mul_self_tc062_aux hp hm1, add_comm, Nat.even_add_one] at hk_odd
        exact not_not.mp hk_odd
      have hm_le_T : m ≤ T := le_trans (Nat.le_mul_of_pos_left m hp.pos) hkT
      have hm_in : m ∈ primeInteriorTruncatedAnchors p T := by
        simp only [primeInteriorTruncatedAnchors, primeEvenValuationAnchors, Finset.mem_filter,
          Finset.mem_Icc]
        exact ⟨⟨⟨hm1, by omega⟩, hm_ev⟩, hkT⟩
      apply hk_not
      simp only [coveredInteriorStations, Finset.mem_union, Finset.mem_image]
      exact Or.inr ⟨m, hm_in, rfl⟩
    have hpk_gt : T < p * k := by
      by_contra hpk_le
      push_neg at hpk_le
      have hk_in : k ∈ primeInteriorTruncatedAnchors p T := by
        simp only [primeInteriorTruncatedAnchors, primeEvenValuationAnchors, Finset.mem_filter,
          Finset.mem_Icc]
        exact ⟨⟨⟨hk1, by omega⟩, hk_ev⟩, hpk_le⟩
      apply hk_not
      simp only [coveredInteriorStations, Finset.mem_union]
      exact Or.inl hk_in
    have h_div_lt : T / p < k := by
      by_contra hle
      push_neg at hle
      have hmul : k * p ≤ T := (Nat.le_div_iff_mul_le hp.pos).mp hle
      rw [mul_comm] at hmul
      omega
    exact ⟨h_div_lt, hkT, hk_ev⟩
  have h_sum :
      ∀ (f : ℕ → ℝ),
        (∑ n ∈ coveredInteriorStations p T, f n) =
          ∑ m ∈ primeInteriorTruncatedAnchors p T, (f m + f (p * m)) := by
    intro f
    unfold coveredInteriorStations
    rw [Finset.sum_union h_disj, Finset.sum_image, ← Finset.sum_add_distrib]
    intro m1 _ m2 _ h_eq
    exact Nat.eq_of_mul_eq_mul_left hp.pos h_eq
  exact ⟨h_sub, h_disj, h_uncov, h_sum⟩

private theorem interiorPairedRemainderF_eq_subset_hcal_tc062_aux
    {p : ℕ} (hp : p.Prime) (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ) :
    interiorPairedRemainderF c_lam c_half p T D0 Y =
      ∑ m ∈ coveredInteriorStations p T, ∑ n ∈ coveredInteriorStations p T,
        (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
          completeSignedKernelHcal c_lam c_half T D0 Y m n := by
  obtain ⟨_, _, _, h_sum⟩ := coveredInteriorStations_props_tc062_aux hp T
  symm
  rw [h_sum]
  unfold interiorPairedRemainderF
  apply Finset.sum_congr rfl
  intro m hm
  have hm1 : 1 ≤ m :=
    (Finset.mem_Icc.mp (Finset.mem_filter.mp (Finset.mem_filter.mp hm).1).1).1
  rw [h_sum, h_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro n hn
  have hn1 : 1 ≤ n :=
    (Finset.mem_Icc.mp (Finset.mem_filter.mp (Finset.mem_filter.mp hn).1).1).1
  rw [liouvilleLambda_prime_mul_real_tc062_aux hp hm1,
    liouvilleLambda_prime_mul_real_tc062_aux hp hn1]
  ring

/-- **Theorem 6 (`TASK-TC-062` §6 Stage A, Interior Hilbert Split, Refutation of Pointwise Anchor-Diagonal Candidate Lemma A1, and Proved Replacement Lemma A1')**:
    1. *Cutoff-strip characterization & exact interior Hilbert split (`hp : p.Prime`, `2 ≤ Y`, `1 ≤ T`)*:
       Every integer `k ∈ [1, T] \ coveredInteriorStations p T` satisfies `T / p < k ∧ k ≤ T` (and `Even (k.factorization p)`), and
       `interiorPairedRemainderF c_lam c_half p T D0 Y = windowEnergyNormSq Y (∑_{m ∈ I_p(T)} λ(m)(ψ_m - ψ_{p m})) - 4 * subsetPrimePowerDiagDtilde (coveredInteriorStations p T) Y - 4 * subsetPrimePowerSelfCollisionXself (coveredInteriorStations p T) Y`;
    2. *Refutation of Candidate Lemma A1 (`2`-adic anchor `m = 1`)*:
       For all `Y ≥ 8`, `T ≥ 2`, `D0 ≥ 2` (and on the canonical schedule for all `Y ≥ 8`),
       `signedAdjustedCoeffB c_lam c_half T D0 1 = 0`, `signedAdjustedCoeffB c_lam c_half T D0 2 = -(Real.log 2)^2`, `1 ∈ primeInteriorTruncatedAnchors 2 T`, and
       `0 < Hcal 1 1 - Hcal 2 1 - Hcal 1 2 + Hcal 2 2` (strictly positive, refuting non-positivity);
    3. *Proved Replacement Lemma A1'*:
       For every prime `p`, `2 ≤ Y`, `1 ≤ T`,
       `∑ m ∈ primeInteriorTruncatedAnchors p T, (Hcal m m - Hcal (p * m) m - Hcal m (p * m) + Hcal (p * m) (p * m)) ≤ 2 * ∑ n ∈ Finset.Icc 1 T, windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 n)`. -/
theorem stage_a_interior_hilbert_split_and_candidate_a1_refutation_tc062 :
    (∀ {p : ℕ}, p.Prime →
      (∀ (T : ℕ), ∀ k ∈ uncoveredCutoffStripStations p T,
        T / p < k ∧ k ≤ T ∧ Even (k.factorization p)) ∧
        (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
          interiorPairedRemainderF c_lam c_half p T D0 Y =
            windowEnergyNormSq Y
              (fun X =>
                ∑ m ∈ primeInteriorTruncatedAnchors p T,
                  (liouvilleLambda m : ℝ) *
                    (adjustedStationProfilePsi c_lam c_half T D0 m X -
                      adjustedStationProfilePsi c_lam c_half T D0 (p * m) X)) -
              4 * subsetPrimePowerDiagDtilde (coveredInteriorStations p T) Y -
              4 * subsetPrimePowerSelfCollisionXself (coveredInteriorStations p T) Y)) ∧
    ((∀ {T D0 : ℕ}, 2 ≤ T → 2 ≤ D0 → ∀ (c_lam c_half : ℝ),
        signedAdjustedCoeffB c_lam c_half T D0 1 = 0 ∧
          signedAdjustedCoeffB c_lam c_half T D0 2 = -(Real.log 2) ^ 2 ∧
          1 ∈ primeInteriorTruncatedAnchors 2 T) ∧
      (∀ {Y : ℝ}, 8 ≤ Y → ∀ {T D0 : ℕ}, 2 ≤ T → 2 ≤ D0 → ∀ (c_lam c_half : ℝ),
        let Hcal := completeSignedKernelHcal c_lam c_half T D0 Y
        0 < Hcal 1 1 - Hcal 2 1 - Hcal 1 2 + Hcal 2 2) ∧
      (∀ {Y : ℝ}, 8 ≤ Y → ∀ (c_lam c_half : ℝ),
        let T := canonicalCutoffT Y
        let D0 := Nat.floor (Real.log Y)
        let Hcal := completeSignedKernelHcal c_lam c_half T D0 Y
        2 ≤ T ∧ 2 ≤ D0 ∧ 1 ∈ primeInteriorTruncatedAnchors 2 T ∧
          0 < Hcal 1 1 - Hcal 2 1 - Hcal 1 2 + Hcal 2 2)) ∧
    (∀ {p : ℕ}, p.Prime → ∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T →
      ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        let Hcal := completeSignedKernelHcal c_lam c_half T D0 Y
        (∑ m ∈ primeInteriorTruncatedAnchors p T,
            (Hcal m m - Hcal (p * m) m - Hcal m (p * m) + Hcal (p * m) (p * m))) ≤
          2 * ∑ n ∈ Finset.Icc 1 T,
            windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 n)) := by
  have h_part1 :
      ∀ {p : ℕ}, p.Prime →
        (∀ (T : ℕ), ∀ k ∈ uncoveredCutoffStripStations p T,
          T / p < k ∧ k ≤ T ∧ Even (k.factorization p)) ∧
          (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ),
            interiorPairedRemainderF c_lam c_half p T D0 Y =
              windowEnergyNormSq Y
                (fun X =>
                  ∑ m ∈ primeInteriorTruncatedAnchors p T,
                    (liouvilleLambda m : ℝ) *
                      (adjustedStationProfilePsi c_lam c_half T D0 m X -
                        adjustedStationProfilePsi c_lam c_half T D0 (p * m) X)) -
                4 * subsetPrimePowerDiagDtilde (coveredInteriorStations p T) Y -
                4 * subsetPrimePowerSelfCollisionXself (coveredInteriorStations p T) Y) := by
    intro p hp
    refine ⟨fun T => (coveredInteriorStations_props_tc062_aux hp T).2.2.1, ?_⟩
    intro Y hY2 T hT D0 c_lam c_half
    obtain ⟨h_sub, _, _, h_sum⟩ := coveredInteriorStations_props_tc062_aux hp T
    rw [interiorPairedRemainderF_eq_subset_hcal_tc062_aux hp c_lam c_half T D0 Y,
      subset_hcal_bilinear_eq_windowNorm_sub_tc062_aux hY2 hT D0 c_lam c_half
        (coveredInteriorStations p T) h_sub]
    congr 2
    unfold windowEnergyNormSq windowPairing
    apply intervalIntegral.integral_congr
    intro X _
    have h_fn :
        (∑ n ∈ coveredInteriorStations p T,
            (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) =
          ∑ m ∈ primeInteriorTruncatedAnchors p T,
            (liouvilleLambda m : ℝ) *
              (adjustedStationProfilePsi c_lam c_half T D0 m X -
                adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) := by
      rw [h_sum]
      apply Finset.sum_congr rfl
      intro m hm
      have hm1 : 1 ≤ m :=
        (Finset.mem_Icc.mp (Finset.mem_filter.mp (Finset.mem_filter.mp hm).1).1).1
      rw [liouvilleLambda_prime_mul_real_tc062_aux hp hm1]
      ring
    dsimp only
    rw [h_fn]
  have h_b12 :
      ∀ {T D0 : ℕ}, 2 ≤ T → 2 ≤ D0 → ∀ (c_lam c_half : ℝ),
        signedAdjustedCoeffB c_lam c_half T D0 1 = 0 ∧
          signedAdjustedCoeffB c_lam c_half T D0 2 = -(Real.log 2) ^ 2 ∧
          1 ∈ primeInteriorTruncatedAnchors 2 T := by
    intro T D0 hT2 hD2 c_lam c_half
    have h_smooth_zero : ∀ n : ℕ, n = 1 ∨ n = 2 →
        openCoreSmoothCoeffS c_lam c_half T D0 n = 0 := by
      intro n hn
      unfold openCoreSmoothCoeffS
      have h_f1 :
          (Finset.Icc (min D0 (T - 1) + 1) (T - 1)).filter
              (fun d => d ∣ n ∧ n / d ≤ T / d) = ∅ := by
        ext d
        simp only [Finset.mem_filter, Finset.mem_Icc, Finset.not_mem_empty, iff_false]
        rintro ⟨⟨hd_lo, _⟩, ⟨hd_dvd, _⟩⟩
        have h_ge3 : 3 ≤ d := by omega
        have hd_le_n : d ≤ n := Nat.le_of_dvd (by rcases hn with rfl | rfl <;> omega) hd_dvd
        rcases hn with rfl | rfl <;> omega
      have h_f2 :
          (Finset.Icc (min D0 (T - 1) + 1) (T - 1)).filter
              (fun d => (d + 1) ∣ n ∧ n / (d + 1) ≤ T / d) = ∅ := by
        ext d
        simp only [Finset.mem_filter, Finset.mem_Icc, Finset.not_mem_empty, iff_false]
        rintro ⟨⟨hd_lo, _⟩, ⟨hd1_dvd, _⟩⟩
        have h_ge4 : 4 ≤ d + 1 := by omega
        have hd1_le_n : d + 1 ≤ n :=
          Nat.le_of_dvd (by rcases hn with rfl | rfl <;> omega) hd1_dvd
        rcases hn with rfl | rfl <;> omega
      change (∑ d ∈ (Finset.Icc (min D0 (T - 1) + 1) (T - 1)).filter
          (fun d => d ∣ n ∧ n / d ≤ T / d), _) -
        (∑ d ∈ (Finset.Icc (min D0 (T - 1) + 1) (T - 1)).filter
          (fun d => (d + 1) ∣ n ∧ n / (d + 1) ≤ T / d), _) = 0
      rw [h_f1, h_f2, Finset.sum_empty, Finset.sum_empty, sub_self]
    have hb1 : signedAdjustedCoeffB c_lam c_half T D0 1 = 0 := by
      unfold signedAdjustedCoeffB openCoreAdjustedCoeffBeta
      rw [h_smooth_zero 1 (Or.inl rfl)]
      simp [Real.log_one]
    have hb2 : signedAdjustedCoeffB c_lam c_half T D0 2 = -(Real.log 2) ^ 2 := by
      unfold signedAdjustedCoeffB openCoreAdjustedCoeffBeta truncatedLiouvilleCoeff
      rw [h_smooth_zero 2 (Or.inr rfl), if_pos ⟨by omega, hT2⟩,
        liouvilleLambda_prime_real_tc062_aux Nat.prime_two]
      push_cast; ring
    have h1_mem : 1 ∈ primeInteriorTruncatedAnchors 2 T := by
      simp only [primeInteriorTruncatedAnchors, primeEvenValuationAnchors, Finset.mem_filter,
        Finset.mem_Icc]
      exact ⟨⟨⟨le_refl 1, by omega⟩, by simp⟩, by omega⟩
    exact ⟨hb1, hb2, h1_mem⟩
  have h_a1_pos :
      ∀ {Y : ℝ}, 8 ≤ Y → ∀ {T D0 : ℕ}, 2 ≤ T → 2 ≤ D0 → ∀ (c_lam c_half : ℝ),
        let Hcal := completeSignedKernelHcal c_lam c_half T D0 Y
        0 < Hcal 1 1 - Hcal 2 1 - Hcal 1 2 + Hcal 2 2 := by
    intro Y hY8 T D0 hT2 hD2 c_lam c_half
    dsimp only
    have hY2 : 2 ≤ Y := by linarith
    have hT1 : 1 ≤ T := by omega
    obtain ⟨hb1, hb2, _⟩ := h_b12 hT2 hD2 c_lam c_half
    have h12_sub : ({1, 2} : Finset ℕ) ⊆ Finset.Icc 1 T := by
      intro x hx
      simp only [Finset.mem_insert, Finset.mem_singleton] at hx
      rw [Finset.mem_Icc]
      rcases hx with rfl | rfl <;> omega
    have h_sub_12 :=
      subset_hcal_bilinear_eq_windowNorm_sub_tc062_aux hY2 hT1 D0 c_lam c_half {1, 2} h12_sub
    have hl1 : (liouvilleLambda 1 : ℝ) = 1 := by simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
    have hl2 : (liouvilleLambda 2 : ℝ) = -1 := liouvilleLambda_prime_real_tc062_aux Nat.prime_two
    have h_lhs_12 :
        (∑ m ∈ ({1, 2} : Finset ℕ), ∑ n ∈ ({1, 2} : Finset ℕ),
            (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
              completeSignedKernelHcal c_lam c_half T D0 Y m n) =
          completeSignedKernelHcal c_lam c_half T D0 Y 1 1 -
            completeSignedKernelHcal c_lam c_half T D0 Y 2 1 -
            completeSignedKernelHcal c_lam c_half T D0 Y 1 2 +
            completeSignedKernelHcal c_lam c_half T D0 Y 2 2 := by
      simp only [Finset.sum_insert (by decide : (1 : ℕ) ∉ ({2} : Finset ℕ)), Finset.sum_singleton]
      rw [hl1, hl2]
      ring
    have hoff_bds := (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.1
    have h_xself_12 : subsetPrimePowerSelfCollisionXself {1, 2} Y = 0 := by
      unfold subsetPrimePowerSelfCollisionXself
      simp only [Finset.sum_insert (by decide : (1 : ℕ) ∉ ({2} : Finset ℕ)), Finset.sum_singleton]
      rw [hoff_bds.1, hoff_bds.2.1 Nat.prime_two]
      ring
    have hc11 : commonPrimePowerLogSq 1 1 = 0 := by
      have h0 := hoff_bds.1
      unfold offDiagPrimePowerWeight at h0
      simp [Real.log_one] at h0
      linarith
    have hc22 : commonPrimePowerLogSq 2 2 = (Real.log 2) ^ 2 := by
      have h0 := hoff_bds.2.1 Nat.prime_two
      unfold offDiagPrimePowerWeight at h0
      push_cast at h0
      linarith [sq (Real.log 2)]
    have hc12 : commonPrimePowerLogSq 1 2 = 0 := by
      unfold commonPrimePowerLogSq
      have hm1 : min 1 2 = 1 := by decide
      have hpp1 : primePowerPairsUpTo 1 = ∅ := by decide
      rw [hm1, hpp1]; simp
    have hc21 : commonPrimePowerLogSq 2 1 = 0 := by
      rw [commonPrimePowerLogSq_symm_tc062_aux, hc12]
    have h_dtilde_12 :
        subsetPrimePowerDiagDtilde {1, 2} Y =
          (Real.log 2) ^ 2 * logWeightedWindowKernel 2 Y 2 2 := by
      unfold subsetPrimePowerDiagDtilde
      simp only [Finset.sum_insert (by decide : (1 : ℕ) ∉ ({2} : Finset ℕ)), Finset.sum_singleton]
      rw [hl1, hl2, hc11, hc12, hc21, hc22]
      ring
    rw [h_lhs_12, h_xself_12, h_dtilde_12] at h_sub_12
    rw [h_sub_12]
    obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc062_aux hY2
    have htau_bds := tau_gt_one_and_lt_eight_tc062_aux
    have h_psi_cont :
        ContinuousOn
          (fun X =>
            ∑ n ∈ ({1, 2} : Finset ℕ),
              (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X)
          (Set.uIcc Y (RiemannScope.tau * Y)) :=
      continuousOn_finset_sum _ (fun n _ =>
        continuousOn_const.mul (continuousOn_adjustedStationProfilePsi_tc062_aux hY2 c_lam c_half T D0 n))
    have h_i1 :
        IntervalIntegrable
          (fun X =>
            (∑ n ∈ ({1, 2} : Finset ℕ),
                (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) *
              (∑ n ∈ ({1, 2} : Finset ℕ),
                (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) / X)
          volume Y (RiemannScope.tau * Y) :=
      ((h_psi_cont.mul h_psi_cont).div continuousOn_id
        (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
    have h_i2 : IntervalIntegrable _ volume Y (RiemannScope.tau * Y) :=
      ((continuousOn_logWeightedKernel_integrand_tc062_aux hY2 2 2 2).intervalIntegrable).const_mul
        (4 * (Real.log 2) ^ 2)
    have h_comb_int :
        windowEnergyNormSq Y
            (fun X =>
              ∑ n ∈ ({1, 2} : Finset ℕ),
                (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) -
            4 * ((Real.log 2) ^ 2 * logWeightedWindowKernel 2 Y 2 2) - 4 * 0 =
          ∫ X in Y..(RiemannScope.tau * Y),
            ((gaussianTermPhi 1 X -
                (1 + (Real.log 2) ^ 2 / (Real.log X) ^ 2) * gaussianTermPhi 2 X) ^ 2 -
              4 * ((Real.log 2) ^ 2 / (Real.log X) ^ 2) * (gaussianTermPhi 2 X) ^ 2) / X := by
      rw [show (4 : ℝ) * 0 = 0 by norm_num, sub_zero, ← mul_assoc]
      unfold windowEnergyNormSq windowPairing logWeightedWindowKernel
      rw [← intervalIntegral.integral_const_mul, ← intervalIntegral.integral_sub h_i1 h_i2]
      apply intervalIntegral.integral_congr
      intro X hX
      have hX_ne : X ≠ 0 := ne_of_gt (hprops X hX).2.1
      have hlog_ne : Real.log X ≠ 0 := (hprops X hX).2.2.2.1
      simp only [Finset.sum_insert (by decide : (1 : ℕ) ∉ ({2} : Finset ℕ)), Finset.sum_singleton]
      unfold adjustedStationProfilePsi
      rw [hl1, hl2, hb1, hb2]
      push_cast
      field_simp [hX_ne, hlog_ne]
      ring
    rw [h_comb_int]
    let m_phi2 : ℝ :=
      Y ^ (5 / 2 : ℝ) * (1 / 8 : ℝ) * Real.exp (-((RiemannScope.tau * Y) ^ 2) / 4)
    have hm_pos : 0 < m_phi2 := by
      dsimp [m_phi2]
      exact mul_pos
        (mul_pos (Real.rpow_pos_of_pos (by linarith only [hY8]) (5 / 2 : ℝ)) (by norm_num))
        (Real.exp_pos _)
    let c_pos : ℝ := (1 / 25 : ℝ) * m_phi2 ^ 2 / (RiemannScope.tau * Y)
    have hc_pos : 0 < c_pos := by
      dsimp [c_pos]
      exact div_pos (mul_pos (by norm_num) (sq_pos_of_pos hm_pos))
        (mul_pos (by linarith only [htau_bds.1]) (by linarith only [hY8]))
    have h_integrand_int := h_i1.sub h_i2
    have h_integrand_eq :
        (fun X =>
          ((gaussianTermPhi 1 X -
              (1 + (Real.log 2) ^ 2 / (Real.log X) ^ 2) * gaussianTermPhi 2 X) ^ 2 -
            4 * ((Real.log 2) ^ 2 / (Real.log X) ^ 2) * (gaussianTermPhi 2 X) ^ 2) / X) =
          fun X =>
            (∑ n ∈ ({1, 2} : Finset ℕ),
                (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) *
              (∑ n ∈ ({1, 2} : Finset ℕ),
                (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) / X -
            4 * (Real.log 2) ^ 2 *
              ((gaussianTermPhi 2 X * gaussianTermPhi 2 X / (Real.log X) ^ 2) / X) := by
      -- ContinuousOn directly is even cleaner!
      ext X
      by_cases hX0 : X = 0
      · subst hX0; simp [gaussianTermPhi]
      · by_cases hl0 : Real.log X = 0
        · simp only [Finset.sum_insert (by decide : (1 : ℕ) ∉ ({2} : Finset ℕ)),
            Finset.sum_singleton, adjustedStationProfilePsi, hl1, hl2, hb1, hb2, hl0]
          push_cast; simp; ring
        · simp only [Finset.sum_insert (by decide : (1 : ℕ) ∉ ({2} : Finset ℕ)),
            Finset.sum_singleton, adjustedStationProfilePsi, hl1, hl2, hb1, hb2]
          push_cast; field_simp [hX0, hl0]; ring
    have h_int_rhs :
        IntervalIntegrable
          (fun X =>
            ((gaussianTermPhi 1 X -
                (1 + (Real.log 2) ^ 2 / (Real.log X) ^ 2) * gaussianTermPhi 2 X) ^ 2 -
              4 * ((Real.log 2) ^ 2 / (Real.log X) ^ 2) * (gaussianTermPhi 2 X) ^ 2) / X)
          volume Y (RiemannScope.tau * Y) := by
      rw [h_integrand_eq]
      exact h_integrand_int
    have hc_pos_int : IntervalIntegrable (fun _ : ℝ => c_pos) volume Y (RiemannScope.tau * Y) :=
      intervalIntegrable_const
    have h_mono :=
      intervalIntegral.integral_mono_on hle hc_pos_int h_int_rhs (by
        intro X hX
        have hX_Icc : Y ≤ X ∧ X ≤ RiemannScope.tau * Y := hX
        have hX8 : 8 ≤ X := le_trans hY8 hX_Icc.1
        have hX_pos : 0 < X := by linarith only [hX8]
        have hlog2_pos : 0 < Real.log 2 := Real.log_pos (by norm_num)
        have hlog8 : 3 * Real.log 2 ≤ Real.log X := by
          have h8_eq : ((2 : ℝ) ^ (3 : ℕ)) = 8 := by norm_num
          have hl := Real.log_le_log (by norm_num) hX8
          rw [← h8_eq, Real.log_pow] at hl
          push_cast at hl
          linarith only [hl]
        have hlogX_pos : 0 < Real.log X := by linarith only [hlog2_pos, hlog8]
        let u := (Real.log 2) ^ 2 / (Real.log X) ^ 2
        have hu_le : u ≤ 1 / 9 := by
          dsimp [u]
          rw [div_le_div_iff (sq_pos_of_pos hlogX_pos) (by norm_num)]
          have hsq := pow_le_pow_left (by positivity : 0 ≤ 3 * Real.log 2) hlog8 2
          linarith only [hsq, show (3 * Real.log 2) ^ 2 = 9 * (Real.log 2) ^ 2 by ring]
        have h_1mu_sq : 64 / 81 ≤ (1 - u) ^ 2 := by
          have h1mu : 8 / 9 ≤ 1 - u := by linarith only [hu_le]
          have hsq := pow_le_pow_left (by norm_num) h1mu 2
          linarith only [hsq, show ((8 / 9 : ℝ) ^ 2) = 64 / 81 by norm_num]
        have h_phi_rel :
            gaussianTermPhi 1 X =
              8 * Real.exp (-(3 * X ^ 2 / 4)) * gaussianTermPhi 2 X := by
          unfold gaussianTermPhi
          push_cast
          have hexp_split :
              -(X ^ 2) / (1 : ℝ) ^ 2 = -(3 * X ^ 2 / 4) + (-(X ^ 2) / (2 : ℝ) ^ 2) := by ring
          rw [hexp_split, Real.exp_add]
          ring
        have hexp_le : Real.exp (-(3 * X ^ 2 / 4)) ≤ 1 / 49 := by
          have hsqX : (8 : ℝ) ^ 2 ≤ X ^ 2 := pow_le_pow_left (by norm_num) hX8 2
          have h48 : (48 : ℝ) ≤ 3 * X ^ 2 / 4 := by linarith only [hsqX]
          have h49 : (49 : ℝ) ≤ Real.exp (3 * X ^ 2 / 4) := by
            have h1 := Real.add_one_le_exp (3 * X ^ 2 / 4)
            linarith only [h48, h1]
          have hprod : Real.exp (3 * X ^ 2 / 4) * Real.exp (-(3 * X ^ 2 / 4)) = 1 := by
            rw [← Real.exp_add, add_neg_self, Real.exp_zero]
          have hm := mul_le_mul_of_nonneg_right h49 (le_of_lt (Real.exp_pos (-(3 * X ^ 2 / 4))))
          rw [hprod] at hm
          linarith only [hm]
        have hphi2_ge : m_phi2 ≤ gaussianTermPhi 2 X := by
          unfold gaussianTermPhi
          dsimp [m_phi2]
          push_cast
          have hrp : Y ^ (5 / 2 : ℝ) ≤ X ^ (5 / 2 : ℝ) :=
            Real.rpow_le_rpow (by linarith only [hY8]) hX_Icc.1 (by norm_num)
          have hexp_ge :
              Real.exp (-((RiemannScope.tau * Y) ^ 2) / 4) ≤ Real.exp (-(X ^ 2) / (2 : ℝ) ^ 2) := by
            apply Real.exp_le_exp.mpr
            have hsq_le : X ^ 2 ≤ (RiemannScope.tau * Y) ^ 2 :=
              pow_le_pow_left (le_of_lt hX_pos) hX_Icc.2 2
            rw [show ((2 : ℝ) ^ 2) = 4 by norm_num]
            linarith only [hsq_le]
          have h_inv8 : (((2 : ℝ) ^ 3)⁻¹) = (1 / 8 : ℝ) := by norm_num
          rw [h_inv8]
          calc
            Y ^ (5 / 2 : ℝ) * (1 / 8) * Real.exp (-((RiemannScope.tau * Y) ^ 2) / 4)
              ≤ X ^ (5 / 2 : ℝ) * (1 / 8) * Real.exp (-(X ^ 2) / (2 : ℝ) ^ 2) := by
                have h1 := mul_le_mul_of_nonneg_right hrp (by norm_num : (0 : ℝ) ≤ 1 / 8)
                exact mul_le_mul h1 hexp_ge (le_of_lt (Real.exp_pos _)) (by positivity)
            _ = X ^ (5 / 2 : ℝ) * ((1 / 8) * Real.exp (-(X ^ 2) / (2 : ℝ) ^ 2)) := by ring
        have hphi2_pos : 0 < gaussianTermPhi 2 X := lt_of_lt_of_le hm_pos hphi2_ge
        have hphi1_nn : 0 ≤ gaussianTermPhi 1 X := by unfold gaussianTermPhi; positivity
        have hphi1_le : gaussianTermPhi 1 X ≤ (8 / 49 : ℝ) * gaussianTermPhi 2 X := by
          rw [h_phi_rel]
          calc
            8 * Real.exp (-(3 * X ^ 2 / 4)) * gaussianTermPhi 2 X
              ≤ 8 * (1 / 49 : ℝ) * gaussianTermPhi 2 X :=
                mul_le_mul_of_nonneg_right
                  (mul_le_mul_of_nonneg_left hexp_le (by norm_num)) (le_of_lt hphi2_pos)
            _ = (8 / 49 : ℝ) * gaussianTermPhi 2 X := by ring
        have h_num_alg :
            (gaussianTermPhi 1 X - (1 + u) * gaussianTermPhi 2 X) ^ 2 -
                4 * u * (gaussianTermPhi 2 X) ^ 2 =
              (gaussianTermPhi 1 X) ^ 2 -
                2 * (1 + u) * gaussianTermPhi 1 X * gaussianTermPhi 2 X +
                (1 - u) ^ 2 * (gaussianTermPhi 2 X) ^ 2 := by ring
        have h_cross_le :
            2 * (1 + u) * gaussianTermPhi 1 X * gaussianTermPhi 2 X ≤
              (160 / 441 : ℝ) * (gaussianTermPhi 2 X) ^ 2 := by
          have h1u : 1 + u ≤ 10 / 9 := by linarith only [hu_le]
          have h1 :
              (1 + u) * gaussianTermPhi 1 X ≤ (10 / 9 : ℝ) * ((8 / 49 : ℝ) * gaussianTermPhi 2 X) :=
            mul_le_mul h1u hphi1_le hphi1_nn (by norm_num)
          have hm := mul_le_mul_of_nonneg_right h1 (le_of_lt hphi2_pos)
          linarith only [hm,
            show 2 * ((10 / 9 : ℝ) * ((8 / 49 : ℝ) * gaussianTermPhi 2 X) * gaussianTermPhi 2 X) =
              (160 / 441 : ℝ) * (gaussianTermPhi 2 X) ^ 2 by ring]
        have h_num_ge :
            (1 / 25 : ℝ) * m_phi2 ^ 2 ≤
              (gaussianTermPhi 1 X - (1 + u) * gaussianTermPhi 2 X) ^ 2 -
                4 * u * (gaussianTermPhi 2 X) ^ 2 := by
          have h_sq_m : m_phi2 ^ 2 ≤ (gaussianTermPhi 2 X) ^ 2 :=
            pow_le_pow_left (le_of_lt hm_pos) hphi2_ge 2
          have h1 := mul_le_mul_of_nonneg_right h_1mu_sq (sq_nonneg (gaussianTermPhi 2 X))
          linarith only [sq_nonneg (gaussianTermPhi 1 X), sq_nonneg m_phi2,
            h_num_alg, h_cross_le, h1, h_sq_m]
        dsimp [c_pos, u] at h_num_ge ⊢
        calc
          (1 / 25 : ℝ) * m_phi2 ^ 2 / (RiemannScope.tau * Y)
            ≤ (1 / 25 : ℝ) * m_phi2 ^ 2 / X :=
              div_le_div_of_nonneg_left (by positivity) hX_pos hX_Icc.2
          _ ≤ ((gaussianTermPhi 1 X -
                (1 + (Real.log 2) ^ 2 / (Real.log X) ^ 2) * gaussianTermPhi 2 X) ^ 2 -
              4 * ((Real.log 2) ^ 2 / (Real.log X) ^ 2) * (gaussianTermPhi 2 X) ^ 2) / X :=
              div_le_div_of_nonneg_right h_num_ge (le_of_lt hX_pos))
    rw [intervalIntegral.integral_const, smul_eq_mul] at h_mono
    have h_sub_pos : 0 < RiemannScope.tau * Y - Y := by
      have hm := mul_lt_mul_of_pos_right htau_bds.1 (by linarith : 0 < Y)
      linarith
    have h_pos_lhs : 0 < (RiemannScope.tau * Y - Y) * c_pos :=
      mul_pos h_sub_pos hc_pos
    linarith
  have h_can_a1 :
      ∀ {Y : ℝ}, 8 ≤ Y → ∀ (c_lam c_half : ℝ),
        let T := canonicalCutoffT Y
        let D0 := Nat.floor (Real.log Y)
        let Hcal := completeSignedKernelHcal c_lam c_half T D0 Y
        2 ≤ T ∧ 2 ≤ D0 ∧ 1 ∈ primeInteriorTruncatedAnchors 2 T ∧
          0 < Hcal 1 1 - Hcal 2 1 - Hcal 1 2 + Hcal 2 2 := by
    intro Y hY8 c_lam c_half
    dsimp only
    have hT2 : 2 ≤ canonicalCutoffT Y := (canonicalCutoffT_bounds_tc062_aux (by linarith)).1
    have hD2 : 2 ≤ Nat.floor (Real.log Y) := by
      have h_inv16 : (15 / 16 : ℝ) ≤ Real.exp (-(1 / 16 : ℝ)) := by
        linarith [Real.add_one_le_exp (-(1 / 16 : ℝ))]
      have h_prod16 : Real.exp (1 / 16 : ℝ) * Real.exp (-(1 / 16 : ℝ)) = 1 := by
        rw [← Real.exp_add, add_neg_self, Real.exp_zero]
      have he16_le : Real.exp (1 / 16 : ℝ) ≤ 16 / 15 := by
        have hm := mul_le_mul_of_nonneg_left h_inv16 (le_of_lt (Real.exp_pos (1 / 16 : ℝ)))
        rw [h_prod16] at hm; linarith
      have hp32 : (Real.exp (1 / 16 : ℝ)) ^ 32 ≤ (16 / 15 : ℝ) ^ 32 :=
        pow_le_pow_left (le_of_lt (Real.exp_pos _)) he16_le 32
      have he2 : (Real.exp (1 / 16 : ℝ)) ^ 32 = Real.exp 2 := by
        rw [← Real.exp_nat_mul]; congr 1; norm_num
      rw [he2] at hp32
      have he2_le_Y : Real.exp 2 ≤ Y := le_trans (le_trans hp32 (by norm_num)) hY8
      have h2_le_log : (2 : ℝ) ≤ Real.log Y := by
        have hl := Real.log_le_log (Real.exp_pos 2) he2_le_Y
        rwa [Real.log_exp] at hl
      exact Nat.le_floor h2_le_log
    exact ⟨hT2, hD2, (h_b12 hT2 hD2 c_lam c_half).2.2, h_a1_pos hY8 hT2 hD2 c_lam c_half⟩
  have h_part3 :
      ∀ {p : ℕ}, p.Prime → ∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T →
        ∀ (D0 : ℕ) (c_lam c_half : ℝ),
          let Hcal := completeSignedKernelHcal c_lam c_half T D0 Y
          (∑ m ∈ primeInteriorTruncatedAnchors p T,
              (Hcal m m - Hcal (p * m) m - Hcal m (p * m) + Hcal (p * m) (p * m))) ≤
            2 * ∑ n ∈ Finset.Icc 1 T,
              windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 n) := by
    intro p hp Y hY2 T hT D0 c_lam c_half
    dsimp only
    obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc062_aux hY2
    obtain ⟨h_cov_sub, _, _, h_cov_sum⟩ := coveredInteriorStations_props_tc062_aux hp T
    have h_each_m :
        ∀ m ∈ primeInteriorTruncatedAnchors p T,
          completeSignedKernelHcal c_lam c_half T D0 Y m m -
              completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
              completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
              completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m) ≤
            2 * (windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 m) +
              windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 (p * m))) := by
      intro m hm
      have hm_f := Finset.mem_filter.mp hm
      have hm_ev_f := Finset.mem_filter.mp hm_f.1
      have hm1 : 1 ≤ m := (Finset.mem_Icc.mp hm_ev_f.1).1
      have hm_ev : Even (m.factorization p) := hm_ev_f.2
      have hpmT : p * m ≤ T := hm_f.2
      have hpm_ne : m ≠ p * m :=
        ((generic_and_liouville_one_prime_pair_decomposition_tc062 hp).1.2 hm1 hm1 hm_ev hm_ev).2.1
      have h_pair_sub : ({m, p * m} : Finset ℕ) ⊆ Finset.Icc 1 T := by
        intro x hx
        simp only [Finset.mem_insert, Finset.mem_singleton] at hx
        rw [Finset.mem_Icc]
        rcases hx with hx_eq | hx_eq
        · rw [hx_eq]; exact ⟨hm1, le_trans (Nat.le_mul_of_pos_left m hp.pos) hpmT⟩
        · rw [hx_eq]; exact ⟨Nat.mul_pos hp.pos hm1, hpmT⟩
      have h_pair_id :=
        subset_hcal_bilinear_eq_windowNorm_sub_tc062_aux hY2 hT D0 c_lam c_half
          {m, p * m} h_pair_sub
      have h_not_mem : m ∉ ({p * m} : Finset ℕ) := Finset.not_mem_singleton.mpr hpm_ne
      have h_lam_sq := liouvilleLambda_sq_eq_one_tc062_aux hm1
      have h_lhs_pair :
          (∑ u ∈ ({m, p * m} : Finset ℕ), ∑ v ∈ ({m, p * m} : Finset ℕ),
              (liouvilleLambda u : ℝ) * (liouvilleLambda v : ℝ) *
                completeSignedKernelHcal c_lam c_half T D0 Y u v) =
            completeSignedKernelHcal c_lam c_half T D0 Y m m -
              completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
              completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
              completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m) := by
        simp only [Finset.sum_insert h_not_mem, Finset.sum_singleton]
        rw [liouvilleLambda_prime_mul_real_tc062_aux hp hm1]
        calc
          (liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ) *
                completeSignedKernelHcal c_lam c_half T D0 Y m m +
              (liouvilleLambda m : ℝ) * -(liouvilleLambda m : ℝ) *
                completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
              (-(liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ) *
                  completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m +
                -(liouvilleLambda m : ℝ) * -(liouvilleLambda m : ℝ) *
                  completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m))
            = ((liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ)) *
                (completeSignedKernelHcal c_lam c_half T D0 Y m m -
                  completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
                  completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
                  completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m)) := by ring
          _ = completeSignedKernelHcal c_lam c_half T D0 Y m m -
                completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
                completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
                completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m) := by
              rw [h_lam_sq, one_mul]
      have hD_nn := subsetPrimePowerDiagDtilde_nonneg_tc062_aux hY2 {m, p * m} h_pair_sub
      have hX_nn : 0 ≤ subsetPrimePowerSelfCollisionXself {m, p * m} Y := by
        unfold subsetPrimePowerSelfCollisionXself
        apply Finset.sum_nonneg
        intro k hk
        have hk1 : 1 ≤ k := (Finset.mem_Icc.mp (h_pair_sub hk)).1
        have hw_nn :=
          ((finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.1.2.2.2 k hk1).1
        have hk_nn : 0 ≤ logWeightedWindowKernel 2 Y k k := by
          unfold logWeightedWindowKernel
          apply intervalIntegral.integral_nonneg hle
          intro X hX
          exact div_nonneg (div_nonneg (mul_self_nonneg _) (sq_nonneg _))
            (by rw [Set.mem_Icc] at hX; linarith)
        exact mul_nonneg hw_nn hk_nn
      have h_norm_le :
          windowEnergyNormSq Y
              (fun X =>
                ∑ n ∈ ({m, p * m} : Finset ℕ),
                  (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) ≤
            2 * (windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 m) +
              windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 (p * m))) := by
        have h_c1 := continuousOn_adjustedStationProfilePsi_tc062_aux hY2 c_lam c_half T D0 m
        have h_c2 := continuousOn_adjustedStationProfilePsi_tc062_aux hY2 c_lam c_half T D0 (p * m)
        have h_cs :
            ContinuousOn
              (fun X =>
                ∑ n ∈ ({m, p * m} : Finset ℕ),
                  (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X)
              (Set.uIcc Y (RiemannScope.tau * Y)) :=
          continuousOn_finset_sum _ (fun n _ =>
            continuousOn_const.mul (continuousOn_adjustedStationProfilePsi_tc062_aux hY2 c_lam c_half T D0 n))
        have hi_s :
            IntervalIntegrable
              (fun X =>
                (∑ n ∈ ({m, p * m} : Finset ℕ),
                    (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) *
                  (∑ n ∈ ({m, p * m} : Finset ℕ),
                    (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) / X)
              volume Y (RiemannScope.tau * Y) :=
          ((h_cs.mul h_cs).div continuousOn_id
            (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
        have hi_1 :
            IntervalIntegrable
              (fun X =>
                adjustedStationProfilePsi c_lam c_half T D0 m X *
                  adjustedStationProfilePsi c_lam c_half T D0 m X / X)
              volume Y (RiemannScope.tau * Y) :=
          ((h_c1.mul h_c1).div continuousOn_id
            (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
        have hi_2 :
            IntervalIntegrable
              (fun X =>
                adjustedStationProfilePsi c_lam c_half T D0 (p * m) X *
                  adjustedStationProfilePsi c_lam c_half T D0 (p * m) X / X)
              volume Y (RiemannScope.tau * Y) :=
          ((h_c2.mul h_c2).div continuousOn_id
            (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
        unfold windowEnergyNormSq windowPairing
        dsimp only
        rw [← intervalIntegral.integral_add hi_1 hi_2, ← intervalIntegral.integral_const_mul]
        apply intervalIntegral.integral_mono_on hle hi_s ((hi_1.add hi_2).const_mul 2)
        intro X hX
        have hX_pos : 0 < X := by rw [Set.mem_Icc] at hX; linarith only [hY2, hX.1]
        simp only [Finset.sum_insert h_not_mem, Finset.sum_singleton]
        rw [liouvilleLambda_prime_mul_real_tc062_aux hp hm1]
        let a := adjustedStationProfilePsi c_lam c_half T D0 m X
        let b := adjustedStationProfilePsi c_lam c_half T D0 (p * m) X
        have h_sq_2 :
            ((liouvilleLambda m : ℝ) * a + -(liouvilleLambda m : ℝ) * b) *
                ((liouvilleLambda m : ℝ) * a + -(liouvilleLambda m : ℝ) * b) ≤
              2 * (a * a + b * b) := by
          have hl_eq :
              ((liouvilleLambda m : ℝ) * a + -(liouvilleLambda m : ℝ) * b) *
                  ((liouvilleLambda m : ℝ) * a + -(liouvilleLambda m : ℝ) * b) =
                ((liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ)) * ((a - b) ^ 2) := by ring
          rw [hl_eq, h_lam_sq, one_mul]
          linarith only [sq_nonneg (a + b),
            show 2 * (a * a + b * b) - (a - b) ^ 2 = (a + b) ^ 2 by ring]
        calc
          ((liouvilleLambda m : ℝ) * a + -(liouvilleLambda m : ℝ) * b) *
              ((liouvilleLambda m : ℝ) * a + -(liouvilleLambda m : ℝ) * b) / X
            ≤ (2 * (a * a + b * b)) / X := div_le_div_of_nonneg_right h_sq_2 (le_of_lt hX_pos)
          _ = 2 * (a * a / X + b * b / X) := by ring
      rw [h_lhs_pair] at h_pair_id
      linarith only [h_pair_id, h_norm_le, hD_nn, hX_nn]
    have h_sum_m := Finset.sum_le_sum h_each_m
    rw [← Finset.mul_sum,
      ← h_cov_sum (fun n => windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 n))]
      at h_sum_m
    have h_sub_sum :
        (∑ n ∈ coveredInteriorStations p T,
            windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 n)) ≤
          ∑ n ∈ Finset.Icc 1 T,
            windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 n) := by
      apply Finset.sum_le_sum_of_subset_of_nonneg h_cov_sub
      intro n _ _
      unfold windowEnergyNormSq windowPairing
      apply intervalIntegral.integral_nonneg hle
      intro X hX
      exact div_nonneg (mul_self_nonneg _) (by rw [Set.mem_Icc] at hX; linarith only [hY2, hX.1])
    linarith only [h_sum_m, h_sub_sum]
  exact ⟨h_part1, ⟨h_b12, h_a1_pos, h_can_a1⟩, h_part3⟩

/-! ### Section 6: Stage C Interior Closure Equivalence & Route D Transfer (`TASK-TC-062` §6 Stage C & §8) -/

private theorem squarePoleDriftM_step_abs_le_tc062_aux (c_half : ℝ) {d : ℕ} (hd1 : 1 ≤ d) :
    |squarePoleDriftM c_half d - squarePoleDriftM c_half (d - 1)| ≤
      4 * Real.log (d : ℝ) + 8 + |c_half| := by
  by_cases hd_eq1 : d = 1
  · subst hd_eq1
    unfold squarePoleDriftM
    simp [Real.log_one]
  · have hd2 : 2 ≤ d := by omega
    have hd_ne : d ≠ 0 := by omega
    have hdm1_ne : d - 1 ≠ 0 := by omega
    have hd_pos : (0 : ℝ) < (d : ℝ) := by positivity
    have hdm1_eq : ((d - 1 : ℕ) : ℝ) = (d : ℝ) - 1 := by
      rw [Nat.cast_sub hd1, Nat.cast_one]
    have hdm1_pos : (0 : ℝ) < (d : ℝ) - 1 := by
      have h2 : (2 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd2
      linarith
    have hdm1_ge1 : (1 : ℝ) ≤ (d : ℝ) - 1 := by
      have h2 : (2 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd2
      linarith
    have h_sqrt_diff_nn : 0 ≤ Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1) :=
      sub_nonneg.mpr (Real.sqrt_le_sqrt (by linarith))
    have h_sqrt_diff_le1 : Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1) ≤ 1 := by
      have h_prod :
          (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) *
            (Real.sqrt (d : ℝ) + Real.sqrt ((d : ℝ) - 1)) = 1 := by
        calc
          (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) *
              (Real.sqrt (d : ℝ) + Real.sqrt ((d : ℝ) - 1))
            = (Real.sqrt (d : ℝ)) ^ 2 - (Real.sqrt ((d : ℝ) - 1)) ^ 2 := by ring
          _ = (d : ℝ) - ((d : ℝ) - 1) := by
              rw [Real.sq_sqrt (le_of_lt hd_pos), Real.sq_sqrt (le_of_lt hdm1_pos)]
          _ = 1 := by ring
      have h_sum_ge1 : 1 ≤ Real.sqrt (d : ℝ) + Real.sqrt ((d : ℝ) - 1) := by
        have hs1 : (1 : ℝ) ≤ Real.sqrt ((d : ℝ) - 1) := by
          calc
            (1 : ℝ) = Real.sqrt 1 := Real.sqrt_one.symm
            _ ≤ Real.sqrt ((d : ℝ) - 1) := Real.sqrt_le_sqrt hdm1_ge1
        linarith [Real.sqrt_nonneg (d : ℝ)]
      have hm := mul_le_mul_of_nonneg_left h_sum_ge1 h_sqrt_diff_nn
      linarith [h_prod]
    have h_log_diff_le : Real.log (d : ℝ) - Real.log ((d : ℝ) - 1) ≤ 1 / ((d : ℝ) - 1) := by
      have h_exp := Real.add_one_le_exp (1 / ((d : ℝ) - 1))
      have h_lhs : 1 / ((d : ℝ) - 1) + 1 = (d : ℝ) / ((d : ℝ) - 1) := by
        field_simp [ne_of_gt hdm1_pos]
      rw [h_lhs] at h_exp
      have hl := Real.log_le_log (div_pos hd_pos hdm1_pos) h_exp
      rw [Real.log_exp, Real.log_div (ne_of_gt hd_pos) (ne_of_gt hdm1_pos)] at hl
      linarith
    have h_log_diff_nn : 0 ≤ Real.log (d : ℝ) - Real.log ((d : ℝ) - 1) :=
      sub_nonneg.mpr (Real.log_le_log hdm1_pos (by linarith))
    have h_sqrt_m1_le : Real.sqrt ((d : ℝ) - 1) ≤ (d : ℝ) - 1 :=
      Real.sqrt_le_iff.mpr ⟨le_of_lt hdm1_pos, by
        rw [sq]; exact le_mul_of_one_le_left (le_of_lt hdm1_pos) hdm1_ge1⟩
    have h_mid :
        4 * Real.sqrt ((d : ℝ) - 1) * (Real.log (d : ℝ) - Real.log ((d : ℝ) - 1)) ≤ 4 := by
      calc
        4 * Real.sqrt ((d : ℝ) - 1) * (Real.log (d : ℝ) - Real.log ((d : ℝ) - 1))
          ≤ 4 * ((d : ℝ) - 1) * (1 / ((d : ℝ) - 1)) := by
            have hm1 := mul_le_mul h_sqrt_m1_le h_log_diff_le h_log_diff_nn (le_of_lt hdm1_pos)
            linarith
        _ = 4 := by field_simp [ne_of_gt hdm1_pos]
    unfold squarePoleDriftM
    rw [if_neg hd_ne, if_neg hdm1_ne, hdm1_eq]
    have h_decomp :
        4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ) + c_half * Real.sqrt (d : ℝ) -
            (4 * Real.sqrt ((d : ℝ) - 1) * Real.log ((d : ℝ) - 1) +
              c_half * Real.sqrt ((d : ℝ) - 1)) =
          4 * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) * Real.log (d : ℝ) +
            4 * Real.sqrt ((d : ℝ) - 1) * (Real.log (d : ℝ) - Real.log ((d : ℝ) - 1)) +
            c_half * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) := by ring
    rw [h_decomp]
    have hlogd_nn : 0 ≤ Real.log (d : ℝ) := Real.log_nonneg (by linarith)
    have ht1 :
        |4 * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) * Real.log (d : ℝ)| ≤
          4 * Real.log (d : ℝ) := by
      rw [abs_of_nonneg (by positivity)]
      exact mul_le_mul_of_nonneg_right
        (by linarith : 4 * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) ≤ 4) hlogd_nn
    have ht2 :
        |4 * Real.sqrt ((d : ℝ) - 1) * (Real.log (d : ℝ) - Real.log ((d : ℝ) - 1))| ≤ 4 := by
      rw [abs_of_nonneg (by positivity)]
      exact h_mid
    have ht3 :
        |c_half * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1))| ≤ |c_half| := by
      rw [abs_mul, abs_of_nonneg h_sqrt_diff_nn]
      exact mul_le_of_le_one_right (abs_nonneg c_half) h_sqrt_diff_le1
    have h_tri1 := abs_add
      (4 * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) * Real.log (d : ℝ) +
        4 * Real.sqrt ((d : ℝ) - 1) * (Real.log (d : ℝ) - Real.log ((d : ℝ) - 1)))
      (c_half * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)))
    have h_tri2 := abs_add
      (4 * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) * Real.log (d : ℝ))
      (4 * Real.sqrt ((d : ℝ) - 1) * (Real.log (d : ℝ) - Real.log ((d : ℝ) - 1)))
    linarith

private theorem card_multiples_Icc_le_div_tc062_aux (T m : ℕ) (hm : 0 < m) :
    (((Finset.Icc 1 T).filter (fun k => m ∣ k)).card : ℝ) ≤ (T : ℝ) / (m : ℝ) := by
  have h_card_nat : ((Finset.Icc 1 T).filter (fun k => m ∣ k)).card ≤ T / m := by
    have h_inj :
        Set.InjOn (fun k => k / m) ↑((Finset.Icc 1 T).filter (fun k => m ∣ k)) := by
      intro k1 hk1 k2 hk2 h_eq
      simp only [Finset.mem_coe, Finset.mem_filter] at hk1 hk2
      dsimp only at h_eq
      have hp1 := Nat.mul_div_cancel' hk1.2
      have hp2 := Nat.mul_div_cancel' hk2.2
      rw [h_eq] at hp1
      exact hp1.symm.trans hp2
    have h_sub_im :
        ((Finset.Icc 1 T).filter (fun k => m ∣ k)).image (fun k => k / m) ⊆
          Finset.Icc 1 (T / m) := by
      intro y hy
      rcases Finset.mem_image.mp hy with ⟨k, hk, rfl⟩
      simp only [Finset.mem_filter, Finset.mem_Icc] at hk ⊢
      exact ⟨Nat.div_pos (Nat.le_of_dvd hk.1.1 hk.2) hm, Nat.div_le_div_right hk.1.2⟩
    rw [← Finset.card_image_of_injOn h_inj]
    simpa [Nat.card_Icc] using Finset.card_le_card h_sub_im
  have hm_r : (0 : ℝ) < (m : ℝ) := Nat.cast_pos.mpr hm
  have h_div_r : ((T / m : ℕ) : ℝ) ≤ (T : ℝ) / (m : ℝ) :=
    (le_div_iff hm_r).mpr (by exact_mod_cast Nat.div_mul_le_self T m)
  exact le_trans (by exact_mod_cast h_card_nat) h_div_r

private theorem sum_abs_openCoreAdjustedCoeffBeta_Icc_le_tc062_aux
    {T : ℕ} (hT2 : 2 ≤ T) (D0 : ℕ) (c_lam c_half : ℝ) :
    (∑ k ∈ Finset.Icc 1 T, |openCoreAdjustedCoeffBeta c_lam c_half T D0 k|) ≤
      (2 * (D0 : ℝ) + 4 * (1 + Real.log (T : ℝ))) *
        ((Real.log (T : ℝ)) ^ 2 + 4 * Real.log (T : ℝ) + 8 + |c_lam| + |c_half|) *
        (T : ℝ) := by
  let D_min := min D0 (T - 1)
  have hT1 : 1 ≤ T := by omega
  have hT_pos_r : (0 : ℝ) < (T : ℝ) := by exact_mod_cast (by omega : 0 < T)
  have hlogT_nn : 0 ≤ Real.log (T : ℝ) := Real.log_nonneg (by exact_mod_cast hT1)
  let B_big : ℝ := (Real.log (T : ℝ)) ^ 2 + 4 * Real.log (T : ℝ) + 8 + |c_lam| + |c_half|
  have hB_nn : 0 ≤ B_big := by dsimp [B_big]; positivity
  -- Exact decomposition of openCoreAdjustedCoeffBeta on 1 <= k <= T
  obtain ⟨_, h_alpha_lt, h_alpha_T, _⟩ :=
    (noncircular_reassembly_and_basis_stratification_tc060 c_lam).2.2.2.2 T hT2
  have h_alpha_adj :
      ∀ k ∈ Finset.Icc 1 T,
        smoothBasisCoeffAlpha c_lam T k -
            truncatedLiouvilleCoeff T k * (Real.log (k : ℝ)) ^ 2 =
          -(c_lam * (if IsSquare k then 1 else 0)) -
            (if k = T then selbergCenteredRemainderInt c_lam T else 0) := by
    intro k hk
    have hk_bds := Finset.mem_Icc.mp hk
    have h_tr : truncatedLiouvilleCoeff T k = (liouvilleLambda k : ℝ) :=
      if_pos hk_bds
    rw [h_tr]
    by_cases hkT : k = T
    · subst hkT
      rw [h_alpha_T, if_pos rfl]
      ring
    · have hk_lt : k ∈ Finset.Icc 1 (T - 1) := Finset.mem_Icc.mpr ⟨hk_bds.1, by omega⟩
      rw [h_alpha_lt k hk_lt, if_neg hkT]
      ring
  let driftOp : ℕ → ℝ := fun k =>
    (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
        squarePoleDriftM c_half d * (liouvilleLambda (k / d) : ℝ)) -
      (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
        squarePoleDriftM c_half d * (liouvilleLambda (k / (d + 1)) : ℝ))
  let smallOp : ℕ → ℝ := fun k =>
    (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
        (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
          (liouvilleLambda (k / d) : ℝ)) -
      (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
        (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
          (liouvilleLambda (k / (d + 1)) : ℝ))
  have h_beta_split :
      ∀ k ∈ Finset.Icc 1 T,
        openCoreAdjustedCoeffBeta c_lam c_half T D0 k =
          (smoothBasisCoeffAlpha c_lam T k -
              truncatedLiouvilleCoeff T k * (Real.log (k : ℝ)) ^ 2) -
            driftOp k - smallOp k := by
    intro k _
    have h_u : Finset.Icc 1 (T - 1) = Finset.Icc 1 D_min ∪ Finset.Icc (D_min + 1) (T - 1) := by
      ext d; simp only [D_min, Finset.mem_Icc, Finset.mem_union]; omega
    have h_d : Disjoint (Finset.Icc 1 D_min) (Finset.Icc (D_min + 1) (T - 1)) := by
      rw [Finset.disjoint_left]; intro d h1 h2; simp only [Finset.mem_Icc] at h1 h2; omega
    have h_lin :
        ∀ (P : ℕ → Prop) [DecidablePred P] (f : ℕ → ℝ),
          (∑ d ∈ (Finset.Icc 1 (T - 1)).filter P, f d) =
            (∑ d ∈ (Finset.Icc 1 D_min).filter P, f d) +
              (∑ d ∈ (Finset.Icc (D_min + 1) (T - 1)).filter P, f d) := by
      intro P _ f
      conv_lhs => rw [h_u, Finset.filter_union]
      exact Finset.sum_union (Finset.disjoint_filter_filter h_d)
    unfold openCoreAdjustedCoeffBeta openCoreSmoothCoeffS smoothBasisCoeffAlpha
    dsimp [driftOp, smallOp, D_min]
    have h1 := h_lin (fun d => d ∣ k ∧ k / d ≤ T / d)
      (fun d => (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
        (liouvilleLambda (k / d) : ℝ))
    have h2 := h_lin (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d)
      (fun d => (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
        (liouvilleLambda (k / (d + 1)) : ℝ))
    have h_sub1 :
        (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
              (liouvilleLambda (k / d) : ℝ)) =
          (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
              selbergCenteredRemainderInt c_lam d * (liouvilleLambda (k / d) : ℝ)) -
            (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
              squarePoleDriftM c_half d * (liouvilleLambda (k / d) : ℝ)) := by
      rw [← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl; intro d _; ring
    have h_sub2 :
        (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
              (liouvilleLambda (k / (d + 1)) : ℝ)) =
          (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
              selbergCenteredRemainderInt c_lam d * (liouvilleLambda (k / (d + 1)) : ℝ)) -
            (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
              squarePoleDriftM c_half d * (liouvilleLambda (k / (d + 1)) : ℝ)) := by
      rw [← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl; intro d _; ring
    linarith [h1, h2, h_sub1, h_sub2]
  have h_drift_eq :
      ∀ k ∈ Finset.Icc 1 T,
        driftOp k =
          (∑ e ∈ k.divisors,
              (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                (liouvilleLambda (k / e) : ℝ)) -
            (if k = T then squarePoleDriftM c_half T else 0) := by
    intro k hk
    have hk_bds := Finset.mem_Icc.mp hk
    have hk_ne : k ≠ 0 := by omega
    have h_s1 :
        (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
            squarePoleDriftM c_half d * (liouvilleLambda (k / d) : ℝ)) =
          (∑ e ∈ k.divisors,
              squarePoleDriftM c_half e * (liouvilleLambda (k / e) : ℝ)) -
            (if k = T then squarePoleDriftM c_half T else 0) := by
      have hf_eq :
          (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ k ∧ k / d ≤ T / d) =
            k.divisors.erase T := by
        ext d
        simp only [Finset.mem_filter, Finset.mem_Icc, Finset.mem_erase, Nat.mem_divisors]
        constructor
        · rintro ⟨⟨_, hd_hi⟩, ⟨hd_dvd, _⟩⟩
          exact ⟨by omega, ⟨hd_dvd, hk_ne⟩⟩
        · rintro ⟨hd_ne_T, ⟨hd_dvd, _⟩⟩
          have hd_pos : 0 < d := Nat.pos_of_dvd_of_pos hd_dvd hk_bds.1
          have hd_le_k : d ≤ k := Nat.le_of_dvd hk_bds.1 hd_dvd
          exact ⟨⟨hd_pos, by omega⟩, ⟨hd_dvd, Nat.div_le_div_right hk_bds.2⟩⟩
      rw [hf_eq]
      by_cases hkT : k = T
      · rw [hkT]
        have hT_div : T ∈ T.divisors := Nat.mem_divisors.mpr ⟨dvd_refl T, by omega⟩
        have hl1 : (liouvilleLambda (T / T) : ℝ) = 1 := by
          rw [Nat.div_self (by omega)]
          simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
        rw [if_pos rfl, ← Finset.add_sum_erase _ _ hT_div, hl1, mul_one]
        ring
      · have hT_not : T ∉ k.divisors := by
          intro hmem
          have hle := Nat.le_of_dvd hk_bds.1 (Nat.mem_divisors.mp hmem).1
          omega
        rw [if_neg hkT, Finset.erase_eq_of_not_mem hT_not, sub_zero]
    have h_s2 :
        (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
            squarePoleDriftM c_half d * (liouvilleLambda (k / (d + 1)) : ℝ)) =
          ∑ e ∈ k.divisors,
            squarePoleDriftM c_half (e - 1) * (liouvilleLambda (k / e) : ℝ) := by
      have h1_div : 1 ∈ k.divisors := Nat.one_mem_divisors.mpr hk_ne
      have hM0 : squarePoleDriftM c_half 0 = 0 := by simp [squarePoleDriftM]
      rw [← Finset.add_sum_erase _ _ h1_div, Nat.sub_self, hM0, zero_mul, zero_add]
      apply Finset.sum_bij (fun d _ => d + 1)
      · intro d hd
        simp only [Finset.mem_filter, Finset.mem_Icc, Finset.mem_erase, Nat.mem_divisors] at hd ⊢
        exact ⟨by omega, ⟨hd.2.1, hk_ne⟩⟩
      · intro d1 _ d2 _ h; omega
      · intro e he
        simp only [Finset.mem_erase, Nat.mem_divisors] at he
        rcases he with ⟨he_ne1, ⟨he_dvd, _⟩⟩
        have he_pos : 0 < e := Nat.pos_of_dvd_of_pos he_dvd hk_bds.1
        have he_ge2 : 2 ≤ e := by omega
        have he_le_T : e ≤ T := le_trans (Nat.le_of_dvd hk_bds.1 he_dvd) hk_bds.2
        let d := e - 1
        have hd1 : d + 1 = e := by omega
        have h_div_le : k / e ≤ T / d :=
          le_trans (Nat.div_le_div_right hk_bds.2)
            (Nat.div_le_div_left (by omega : d ≤ e) (by omega : 0 < d))
        refine ⟨d, ?_, hd1⟩
        simp only [Finset.mem_filter, Finset.mem_Icc]
        exact ⟨⟨by omega, by omega⟩, ⟨by rwa [hd1], by rwa [hd1]⟩⟩
      · intro d _; simp
    dsimp [driftOp]
    rw [h_s1, h_s2, sub_right_comm, ← Finset.sum_sub_distrib]
    congr 1
    apply Finset.sum_congr rfl
    intro e _
    ring
  have h_harm1 : (∑ e ∈ Finset.Icc 1 T, (1 / (e : ℝ))) ≤ 1 + Real.log (T : ℝ) := by
    have h_ins : Finset.Icc 1 T = insert 1 (Finset.Icc 2 T) := by
      ext e; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
    rw [h_ins, Finset.sum_insert (by simp)]
    have h1_eq : (1 : ℝ) / ((1 : ℕ) : ℝ) = 1 := by norm_num
    rw [h1_eq]
    linarith [sum_inv_Icc_two_le_log_tc062_aux T hT1]
  have h_sum_divisors_card :
      (∑ k ∈ Finset.Icc 1 T, (k.divisors.card : ℝ)) ≤ (T : ℝ) * (1 + Real.log (T : ℝ)) := by
    have h_eq_d :
        (∑ k ∈ Finset.Icc 1 T, (k.divisors.card : ℝ)) =
          ∑ e ∈ Finset.Icc 1 T, (((Finset.Icc 1 T).filter (fun k => e ∣ k)).card : ℝ) := by
      have h_k :
          ∀ k ∈ Finset.Icc 1 T,
            (k.divisors.card : ℝ) =
              ∑ e ∈ Finset.Icc 1 T, (if e ∣ k then (1 : ℝ) else 0) := by
        intro k hk
        have hk_bds := Finset.mem_Icc.mp hk
        have h_div_eq : k.divisors = (Finset.Icc 1 T).filter (fun e => e ∣ k) := by
          ext e
          simp only [Nat.mem_divisors, Finset.mem_filter, Finset.mem_Icc]
          constructor
          · rintro ⟨hd, _⟩
            exact ⟨⟨Nat.pos_of_dvd_of_pos hd hk_bds.1,
              le_trans (Nat.le_of_dvd hk_bds.1 hd) hk_bds.2⟩, hd⟩
          · rintro ⟨_, hd⟩
            exact ⟨hd, by omega⟩
        rw [h_div_eq, Finset.sum_boole]
      rw [Finset.sum_congr rfl h_k, Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro e _
      rw [Finset.sum_boole]
    rw [h_eq_d]
    calc
      (∑ e ∈ Finset.Icc 1 T, (((Finset.Icc 1 T).filter (fun k => e ∣ k)).card : ℝ))
        ≤ ∑ e ∈ Finset.Icc 1 T, (T : ℝ) * (1 / (e : ℝ)) := by
          apply Finset.sum_le_sum
          intro e he
          have he_pos : 0 < e := (Finset.mem_Icc.mp he).1
          simpa [div_eq_mul_inv] using card_multiples_Icc_le_div_tc062_aux T e he_pos
      _ = (T : ℝ) * ∑ e ∈ Finset.Icc 1 T, (1 / (e : ℝ)) := (Finset.mul_sum _ _ _).symm
      _ ≤ (T : ℝ) * (1 + Real.log (T : ℝ)) :=
          mul_le_mul_of_nonneg_left h_harm1 (le_of_lt hT_pos_r)
  have h_sum_alpha_drift :
      (∑ k ∈ Finset.Icc 1 T,
          |(smoothBasisCoeffAlpha c_lam T k -
              truncatedLiouvilleCoeff T k * (Real.log (k : ℝ)) ^ 2) - driftOp k|) ≤
        (4 * B_big) * (T : ℝ) * (1 + Real.log (T : ℝ)) := by
    have h_each :
        ∀ k ∈ Finset.Icc 1 T,
          |(smoothBasisCoeffAlpha c_lam T k -
              truncatedLiouvilleCoeff T k * (Real.log (k : ℝ)) ^ 2) - driftOp k| ≤
            |c_lam| +
              (if k = T then |selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T| else 0) +
              (k.divisors.card : ℝ) * B_big := by
      intro k hk
      have hk_bds := Finset.mem_Icc.mp hk
      rw [h_alpha_adj k hk, h_drift_eq k hk]
      have h_rearr :
          -(c_lam * (if IsSquare k then 1 else 0)) -
              (if k = T then selbergCenteredRemainderInt c_lam T else 0) -
              ((∑ e ∈ k.divisors,
                  (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                    (liouvilleLambda (k / e) : ℝ)) -
                (if k = T then squarePoleDriftM c_half T else 0)) =
            -(c_lam * (if IsSquare k then 1 else 0)) -
              (if k = T then selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T else 0) -
              (∑ e ∈ k.divisors,
                (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                  (liouvilleLambda (k / e) : ℝ)) := by
        split_ifs <;> ring
      rw [h_rearr]
      have ha1 : |-(c_lam * (if IsSquare k then 1 else 0))| ≤ |c_lam| := by
        rw [abs_neg]; split_ifs <;> simp [abs_nonneg]
      have ha2 :
          |if k = T then selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T else 0| =
            if k = T then |selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T| else 0 := by
        split_ifs <;> simp
      have ha3 :
          |∑ e ∈ k.divisors,
              (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                (liouvilleLambda (k / e) : ℝ)| ≤
            (k.divisors.card : ℝ) * B_big := by
        calc
          |∑ e ∈ k.divisors,
              (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                (liouvilleLambda (k / e) : ℝ)|
            ≤ ∑ e ∈ k.divisors,
                |(squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                  (liouvilleLambda (k / e) : ℝ)| := Finset.abs_sum_le_sum_abs _ _
          _ ≤ ∑ _e ∈ k.divisors, B_big := by
              apply Finset.sum_le_sum
              intro e he
              have he_dvd := (Nat.mem_divisors.mp he).1
              have he_pos : 1 ≤ e := Nat.pos_of_dvd_of_pos he_dvd hk_bds.1
              have he_le_T : e ≤ T := le_trans (Nat.le_of_dvd hk_bds.1 he_dvd) hk_bds.2
              have hq_pos : 1 ≤ k / e := Nat.div_pos (Nat.le_of_dvd hk_bds.1 he_dvd) he_pos
              have hlam_abs : |(liouvilleLambda (k / e) : ℝ)| = 1 :=
                abs_liouvilleLambda_eq_one_tc062_aux hq_pos
              rw [abs_mul, hlam_abs, mul_one]
              have hstep := squarePoleDriftM_step_abs_le_tc062_aux c_half he_pos
              have hlog_e : Real.log (e : ℝ) ≤ Real.log (T : ℝ) :=
                Real.log_le_log (by positivity) (by exact_mod_cast he_le_T)
              dsimp [B_big]
              linarith [sq_nonneg (Real.log (T : ℝ)), abs_nonneg c_lam]
          _ = (k.divisors.card : ℝ) * B_big := by simp
      have ht1 := abs_sub
        (-(c_lam * (if IsSquare k then 1 else 0)) -
          (if k = T then selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T else 0))
        (∑ e ∈ k.divisors,
          (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
            (liouvilleLambda (k / e) : ℝ))
      have ht2 := abs_sub
        (-(c_lam * (if IsSquare k then 1 else 0)))
        (if k = T then selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T else 0)
      linarith
    have h_sum_T_only :
        (∑ k ∈ Finset.Icc 1 T,
            (if k = T then |selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T| else 0)) =
          |selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T| := by
      have hT_in : T ∈ Finset.Icc 1 T := Finset.mem_Icc.mpr ⟨hT1, le_refl T⟩
      rw [← Finset.add_sum_erase _ _ hT_in, if_pos rfl]
      have her : (∑ k ∈ (Finset.Icc 1 T).erase T,
          if k = T then |selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T| else 0) = 0 := by
        apply Finset.sum_eq_zero; intro k hk; rw [if_neg (Finset.mem_erase.mp hk).1]
      rw [her, add_zero]
    have h_end_bd :
        |selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T| ≤ (T : ℝ) * B_big := by
      have h := centered_minus_drift_abs_le_tc062_aux c_lam c_half hT1 (le_refl T)
      dsimp [B_big]
      linarith [mul_nonneg (le_of_lt hT_pos_r) (by norm_num : (0 : ℝ) ≤ 8)]
    have h_clam_sum : (∑ _k ∈ Finset.Icc 1 T, |c_lam|) ≤ (T : ℝ) * B_big := by
      have hcard_eq : (∑ _k ∈ Finset.Icc 1 T, |c_lam|) = (T : ℝ) * |c_lam| := by
        simp [Nat.card_Icc]
      rw [hcard_eq]
      have h_le : |c_lam| ≤ B_big := by
        dsimp [B_big]
        linarith [sq_nonneg (Real.log (T : ℝ)), hlogT_nn, abs_nonneg c_half]
      exact mul_le_mul_of_nonneg_left h_le (le_of_lt hT_pos_r)
    have h_tot := Finset.sum_le_sum h_each
    rw [Finset.sum_add_distrib, Finset.sum_add_distrib, h_sum_T_only, ← Finset.sum_mul] at h_tot
    have h_div_B := mul_le_mul_of_nonneg_right h_sum_divisors_card hB_nn
    have h_tb_nn : 0 ≤ (T : ℝ) * B_big := mul_nonneg (le_of_lt hT_pos_r) hB_nn
    have h_tbl_nn : 0 ≤ (T : ℝ) * B_big * Real.log (T : ℝ) := mul_nonneg h_tb_nn hlogT_nn
    linarith [show (T : ℝ) * (1 + Real.log (T : ℝ)) * B_big =
      (T : ℝ) * B_big + (T : ℝ) * B_big * Real.log (T : ℝ) by ring,
      show (4 * B_big) * (T : ℝ) * (1 + Real.log (T : ℝ)) =
      4 * ((T : ℝ) * B_big) + 4 * ((T : ℝ) * B_big * Real.log (T : ℝ)) by ring]
  have h_sum_small :
      (∑ k ∈ Finset.Icc 1 T, |smallOp k|) ≤
        (2 * (D0 : ℝ) * B_big) * (T : ℝ) := by
    have h_each_sm :
        ∀ k ∈ Finset.Icc 1 T,
          |smallOp k| ≤
            (∑ d ∈ Finset.Icc 1 D_min,
              (if d ∣ k then (d : ℝ) * B_big else 0)) +
            (∑ d ∈ Finset.Icc 1 D_min,
              (if (d + 1) ∣ k then (d : ℝ) * B_big else 0)) := by
      intro k _
      dsimp [smallOp]
      have ht := abs_sub
        (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
          (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
            (liouvilleLambda (k / d) : ℝ))
        (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
          (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
            (liouvilleLambda (k / (d + 1)) : ℝ))
      have hb1 :
          |∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
              (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                (liouvilleLambda (k / d) : ℝ)| ≤
            ∑ d ∈ Finset.Icc 1 D_min, (if d ∣ k then (d : ℝ) * B_big else 0) := by
        calc
          |∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k ∧ k / d ≤ T / d), _|
            ≤ ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
                |(selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                  (liouvilleLambda (k / d) : ℝ)| := Finset.abs_sum_le_sum_abs _ _
          _ ≤ ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
                (d : ℝ) * B_big := by
              apply Finset.sum_le_sum
              intro d hd
              have hd_Icc := Finset.mem_Icc.mp (Finset.mem_filter.mp hd).1
              have hdT : d ≤ T := by dsimp [D_min] at hd_Icc; omega
              have hlam_le := abs_liouvilleLambda_le_one_tc062_aux (k / d)
              have hw := centered_minus_drift_abs_le_tc062_aux c_lam c_half hd_Icc.1 hdT
              rw [abs_mul]
              calc
                |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| *
                    |(liouvilleLambda (k / d) : ℝ)|
                  ≤ |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| * 1 :=
                    mul_le_mul_of_nonneg_left hlam_le (abs_nonneg _)
                _ ≤ (d : ℝ) * B_big := by
                    dsimp [B_big]; linarith [mul_nonneg (show (0 : ℝ) ≤ d by positivity) (by norm_num : (0 : ℝ) ≤ 8)]
          _ ≤ ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k), (d : ℝ) * B_big := by
              apply Finset.sum_le_sum_of_subset_of_nonneg
              · intro d hd; simp only [Finset.mem_filter] at hd ⊢; exact ⟨hd.1, hd.2.1⟩
              · intro d _ _; positivity
          _ = ∑ d ∈ Finset.Icc 1 D_min, (if d ∣ k then (d : ℝ) * B_big else 0) :=
              Finset.sum_filter _ _
      have hb2 :
          |∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
              (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                (liouvilleLambda (k / (d + 1)) : ℝ)| ≤
            ∑ d ∈ Finset.Icc 1 D_min, (if (d + 1) ∣ k then (d : ℝ) * B_big else 0) := by
        calc
          |∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d), _|
            ≤ ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
                |(selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                  (liouvilleLambda (k / (d + 1)) : ℝ)| := Finset.abs_sum_le_sum_abs _ _
          _ ≤ ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
                (d : ℝ) * B_big := by
              apply Finset.sum_le_sum
              intro d hd
              have hd_Icc := Finset.mem_Icc.mp (Finset.mem_filter.mp hd).1
              have hdT : d ≤ T := by dsimp [D_min] at hd_Icc; omega
              have hlam_le := abs_liouvilleLambda_le_one_tc062_aux (k / (d + 1))
              have hw := centered_minus_drift_abs_le_tc062_aux c_lam c_half hd_Icc.1 hdT
              rw [abs_mul]
              calc
                |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| *
                    |(liouvilleLambda (k / (d + 1)) : ℝ)|
                  ≤ |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| * 1 :=
                    mul_le_mul_of_nonneg_left hlam_le (abs_nonneg _)
                _ ≤ (d : ℝ) * B_big := by
                    dsimp [B_big]; linarith [mul_nonneg (show (0 : ℝ) ≤ d by positivity) (by norm_num : (0 : ℝ) ≤ 8)]
          _ ≤ ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k), (d : ℝ) * B_big := by
              apply Finset.sum_le_sum_of_subset_of_nonneg
              · intro d hd; simp only [Finset.mem_filter] at hd ⊢; exact ⟨hd.1, hd.2.1⟩
              · intro d _ _; positivity
          _ = ∑ d ∈ Finset.Icc 1 D_min, (if (d + 1) ∣ k then (d : ℝ) * B_big else 0) :=
              Finset.sum_filter _ _
      linarith
    have h_sum1 :
        (∑ k ∈ Finset.Icc 1 T, ∑ d ∈ Finset.Icc 1 D_min,
            (if d ∣ k then (d : ℝ) * B_big else 0)) ≤
          (D0 : ℝ) * B_big * (T : ℝ) := by
      rw [Finset.sum_comm]
      calc
        (∑ d ∈ Finset.Icc 1 D_min, ∑ k ∈ Finset.Icc 1 T,
            (if d ∣ k then (d : ℝ) * B_big else 0))
          ≤ ∑ _d ∈ Finset.Icc 1 D_min, B_big * (T : ℝ) := by
            apply Finset.sum_le_sum
            intro d hd
            have hd_pos : 0 < d := (Finset.mem_Icc.mp hd).1
            have hd_ne_r : (d : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (ne_of_gt hd_pos)
            rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul]
            have hc := card_multiples_Icc_le_div_tc062_aux T d hd_pos
            have hm := mul_le_mul_of_nonneg_right hc (show 0 ≤ (d : ℝ) * B_big by positivity)
            have h_cancel : ((T : ℝ) / (d : ℝ)) * ((d : ℝ) * B_big) = B_big * (T : ℝ) := by
              field_simp [hd_ne_r]; ring
            rwa [h_cancel] at hm
        _ = ((Finset.Icc 1 D_min).card : ℝ) * (B_big * (T : ℝ)) := by simp
        _ ≤ (D0 : ℝ) * B_big * (T : ℝ) := by
            have hc : (Finset.Icc 1 D_min).card ≤ D0 := by
              simp only [D_min, Nat.card_Icc]; omega
            calc
              ((Finset.Icc 1 D_min).card : ℝ) * (B_big * (T : ℝ))
                ≤ (D0 : ℝ) * (B_big * (T : ℝ)) :=
                  mul_le_mul_of_nonneg_right (by exact_mod_cast hc) (by positivity)
              _ = (D0 : ℝ) * B_big * (T : ℝ) := by ring
    have h_sum2 :
        (∑ k ∈ Finset.Icc 1 T, ∑ d ∈ Finset.Icc 1 D_min,
            (if (d + 1) ∣ k then (d : ℝ) * B_big else 0)) ≤
          (D0 : ℝ) * B_big * (T : ℝ) := by
      rw [Finset.sum_comm]
      calc
        (∑ d ∈ Finset.Icc 1 D_min, ∑ k ∈ Finset.Icc 1 T,
            (if (d + 1) ∣ k then (d : ℝ) * B_big else 0))
          ≤ ∑ _d ∈ Finset.Icc 1 D_min, B_big * (T : ℝ) := by
            apply Finset.sum_le_sum
            intro d hd
            have hd_pos : 0 < d := (Finset.mem_Icc.mp hd).1
            have hd_ne_r : (d : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (ne_of_gt hd_pos)
            have hc1 := card_multiples_Icc_le_div_tc062_aux T (d + 1) (by omega)
            have h_div_le : (T : ℝ) / ((d + 1 : ℕ) : ℝ) ≤ (T : ℝ) / (d : ℝ) :=
              div_le_div_of_nonneg_left (le_of_lt hT_pos_r) (by positivity) (by exact_mod_cast Nat.le_succ d)
            rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul]
            have hm := mul_le_mul_of_nonneg_right (le_trans hc1 h_div_le)
              (show 0 ≤ (d : ℝ) * B_big by positivity)
            have h_cancel : ((T : ℝ) / (d : ℝ)) * ((d : ℝ) * B_big) = B_big * (T : ℝ) := by
              field_simp [hd_ne_r]; ring
            rwa [h_cancel] at hm
        _ = ((Finset.Icc 1 D_min).card : ℝ) * (B_big * (T : ℝ)) := by simp
        _ ≤ (D0 : ℝ) * B_big * (T : ℝ) := by
            have hc : (Finset.Icc 1 D_min).card ≤ D0 := by
              simp only [D_min, Nat.card_Icc]; omega
            calc
              ((Finset.Icc 1 D_min).card : ℝ) * (B_big * (T : ℝ))
                ≤ (D0 : ℝ) * (B_big * (T : ℝ)) :=
                  mul_le_mul_of_nonneg_right (by exact_mod_cast hc) (by positivity)
              _ = (D0 : ℝ) * B_big * (T : ℝ) := by ring
    have h_tot := Finset.sum_le_sum h_each_sm
    rw [Finset.sum_add_distrib] at h_tot
    linarith
  have h_each_tot :
      ∀ k ∈ Finset.Icc 1 T,
        |openCoreAdjustedCoeffBeta c_lam c_half T D0 k| ≤
          |(smoothBasisCoeffAlpha c_lam T k -
              truncatedLiouvilleCoeff T k * (Real.log (k : ℝ)) ^ 2) - driftOp k| +
            |smallOp k| := by
    intro k hk
    rw [h_beta_split k hk]
    exact abs_sub _ _
  have h_final := Finset.sum_le_sum h_each_tot
  rw [Finset.sum_add_distrib] at h_final
  dsimp [B_big] at h_sum_alpha_drift h_sum_small
  linarith

private theorem subsetPrimePowerDiagDtilde_young_split_tc062_aux
    {Y : ℝ} (hY2 : 2 ≤ Y) (T : ℕ) (S_sub : Finset ℕ) (hS_sub : S_sub ⊆ Finset.Icc 1 T)
    {δ : ℝ} (hδ : 0 < δ) :
    inheritedPrimePowerDiagDtilde T Y - subsetPrimePowerDiagDtilde S_sub Y ≤
        δ * inheritedPrimePowerDiagDtilde T Y +
          (1 / δ) * subsetPrimePowerDiagDtilde (Finset.Icc 1 T \ S_sub) Y ∧
      subsetPrimePowerDiagDtilde S_sub Y - inheritedPrimePowerDiagDtilde T Y ≤
        δ * inheritedPrimePowerDiagDtilde T Y +
          (1 + 1 / δ) * subsetPrimePowerDiagDtilde (Finset.Icc 1 T \ S_sub) Y := by
  obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc062_aux hY2
  have hB_sub : Finset.Icc 1 T \ S_sub ⊆ Finset.Icc 1 T := Finset.sdiff_subset _ _
  have hD_T : inheritedPrimePowerDiagDtilde T Y = subsetPrimePowerDiagDtilde (Finset.Icc 1 T) Y :=
    ((finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).1 hY2 T).1
  rw [hD_T]
  have hi_S : ∀ S : Finset ℕ, S ⊆ Finset.Icc 1 T →
      IntervalIntegrable
        (fun X =>
          ((∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ S.filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) /
            (Real.log X) ^ 2) / X)
        volume Y (RiemannScope.tau * Y) := by
    intro S _
    have hlog_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
      ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1)
    apply ContinuousOn.intervalIntegrable
    refine ((continuousOn_finset_sum _ (fun pk _ => continuousOn_const.mul
      ((continuousOn_finset_sum _ (fun n _ => continuousOn_const.mul
        (continuousOn_gaussianTermPhi_uIcc_tc062_aux Y n))).pow 2))).div
      (hlog_cont.pow 2) (fun X hX => (hprops X hX).2.2.2.2)).div
      continuousOn_id (fun X hX => ne_of_gt (hprops X hX).2.1)
  have hi_all := hi_S (Finset.Icc 1 T) (Finset.Subset.refl _)
  have hi_Ssub := hi_S S_sub hS_sub
  have hi_B := hi_S (Finset.Icc 1 T \ S_sub) hB_sub
  rw [subsetPrimePowerDiagDtilde_integral_eq_tc062_aux hY2 T (Finset.Icc 1 T) (Finset.Subset.refl _),
    subsetPrimePowerDiagDtilde_integral_eq_tc062_aux hY2 T S_sub hS_sub,
    subsetPrimePowerDiagDtilde_integral_eq_tc062_aux hY2 T (Finset.Icc 1 T \ S_sub) hB_sub]
  have hδ_ne : δ ≠ 0 := ne_of_gt hδ
  have h_part_S :
      ∀ (pk : ℕ × ℕ) (X : ℝ),
        (∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
            (liouvilleLambda n : ℝ) * gaussianTermPhi n X) =
          (∑ n ∈ S_sub.filter (fun n => pk.1 ^ pk.2 ∣ n),
              (liouvilleLambda n : ℝ) * gaussianTermPhi n X) +
            (∑ n ∈ (Finset.Icc 1 T \ S_sub).filter (fun n => pk.1 ^ pk.2 ∣ n),
              (liouvilleLambda n : ℝ) * gaussianTermPhi n X) := by
    intro pk X
    have h_u : Finset.Icc 1 T = S_sub ∪ (Finset.Icc 1 T \ S_sub) :=
      (Finset.union_sdiff_of_subset hS_sub).symm
    have h_d : Disjoint S_sub (Finset.Icc 1 T \ S_sub) := Finset.disjoint_sdiff
    conv_lhs => rw [h_u, Finset.filter_union]
    exact Finset.sum_union (Finset.disjoint_filter_filter h_d)
  constructor
  · rw [← intervalIntegral.integral_sub hi_all hi_Ssub,
      ← intervalIntegral.integral_const_mul, ← intervalIntegral.integral_const_mul,
      ← intervalIntegral.integral_add (hi_all.const_mul _) (hi_B.const_mul _)]
    apply intervalIntegral.integral_mono_on hle (hi_all.sub hi_Ssub)
      ((hi_all.const_mul _).add (hi_B.const_mul _))
    intro X hX
    have hX_pos : 0 < X := by rw [Set.mem_Icc] at hX; linarith
    have hlog_sq_pos : 0 < (Real.log X) ^ 2 := by
      have hX_in : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
      exact sq_pos_of_pos (hprops X hX_in).2.2.1
    have h_sum_pk :
        (∑ pk ∈ primePowerPairsUpTo T,
            (Real.log (pk.1 : ℝ)) ^ 2 *
              (∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
                (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) -
          (∑ pk ∈ primePowerPairsUpTo T,
            (Real.log (pk.1 : ℝ)) ^ 2 *
              (∑ n ∈ S_sub.filter (fun n => pk.1 ^ pk.2 ∣ n),
                (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) ≤
          δ * (∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) +
            (1 / δ) * (∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ (Finset.Icc 1 T \ S_sub).filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) := by
      rw [← Finset.sum_sub_distrib, Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
      apply Finset.sum_le_sum
      intro pk _
      let a := ∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
        (liouvilleLambda n : ℝ) * gaussianTermPhi n X
      let b := ∑ n ∈ S_sub.filter (fun n => pk.1 ^ pk.2 ∣ n),
        (liouvilleLambda n : ℝ) * gaussianTermPhi n X
      let s := ∑ n ∈ (Finset.Icc 1 T \ S_sub).filter (fun n => pk.1 ^ pk.2 ∣ n),
        (liouvilleLambda n : ℝ) * gaussianTermPhi n X
      have habs : a = b + s := h_part_S pk X
      have hb_eq : b = a - s := by linarith
      have h_alg :
          δ * a ^ 2 + (1 / δ) * s ^ 2 - (a ^ 2 - (a - s) ^ 2) =
            (δ * a - s) ^ 2 / δ + s ^ 2 := by
        field_simp [hδ_ne]; ring
      have h_ineq : a ^ 2 - b ^ 2 ≤ δ * a ^ 2 + (1 / δ) * s ^ 2 := by
        rw [hb_eq]
        have hnn : 0 ≤ (δ * a - s) ^ 2 / δ + s ^ 2 :=
          add_nonneg (div_nonneg (sq_nonneg _) (le_of_lt hδ)) (sq_nonneg _)
        linarith
      calc
        (Real.log (pk.1 : ℝ)) ^ 2 * a ^ 2 - (Real.log (pk.1 : ℝ)) ^ 2 * b ^ 2
          = (Real.log (pk.1 : ℝ)) ^ 2 * (a ^ 2 - b ^ 2) := by ring
        _ ≤ (Real.log (pk.1 : ℝ)) ^ 2 * (δ * a ^ 2 + (1 / δ) * s ^ 2) :=
            mul_le_mul_of_nonneg_left h_ineq (sq_nonneg _)
        _ = δ * ((Real.log (pk.1 : ℝ)) ^ 2 * a ^ 2) +
              (1 / δ) * ((Real.log (pk.1 : ℝ)) ^ 2 * s ^ 2) := by ring
    have hd1 := div_le_div_of_nonneg_right h_sum_pk (le_of_lt hlog_sq_pos)
    have hd2 := div_le_div_of_nonneg_right hd1 (le_of_lt hX_pos)
    calc
      ((∑ pk ∈ primePowerPairsUpTo T,
            (Real.log (pk.1 : ℝ)) ^ 2 *
              (∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
                (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) /
          (Real.log X) ^ 2) / X -
        ((∑ pk ∈ primePowerPairsUpTo T,
            (Real.log (pk.1 : ℝ)) ^ 2 *
              (∑ n ∈ S_sub.filter (fun n => pk.1 ^ pk.2 ∣ n),
                (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) /
          (Real.log X) ^ 2) / X
        = (((∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) -
            (∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ S_sub.filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2)) /
            (Real.log X) ^ 2) / X := by ring
      _ ≤ ((δ * (∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) +
            (1 / δ) * (∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ (Finset.Icc 1 T \ S_sub).filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2)) /
            (Real.log X) ^ 2) / X := hd2
      _ = δ * (((∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) /
            (Real.log X) ^ 2) / X) +
          (1 / δ) * (((∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ (Finset.Icc 1 T \ S_sub).filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) /
            (Real.log X) ^ 2) / X) := by ring
  · rw [← intervalIntegral.integral_sub hi_Ssub hi_all,
      ← intervalIntegral.integral_const_mul, ← intervalIntegral.integral_const_mul,
      ← intervalIntegral.integral_add (hi_all.const_mul _) (hi_B.const_mul _)]
    apply intervalIntegral.integral_mono_on hle (hi_Ssub.sub hi_all)
      ((hi_all.const_mul _).add (hi_B.const_mul _))
    intro X hX
    have hX_pos : 0 < X := by rw [Set.mem_Icc] at hX; linarith
    have hlog_sq_pos : 0 < (Real.log X) ^ 2 := by
      have hX_in : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
      exact sq_pos_of_pos (hprops X hX_in).2.2.1
    have h_sum_pk :
        (∑ pk ∈ primePowerPairsUpTo T,
            (Real.log (pk.1 : ℝ)) ^ 2 *
              (∑ n ∈ S_sub.filter (fun n => pk.1 ^ pk.2 ∣ n),
                (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) -
          (∑ pk ∈ primePowerPairsUpTo T,
            (Real.log (pk.1 : ℝ)) ^ 2 *
              (∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
                (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) ≤
          δ * (∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) +
            (1 + 1 / δ) * (∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ (Finset.Icc 1 T \ S_sub).filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) := by
      rw [← Finset.sum_sub_distrib, Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
      apply Finset.sum_le_sum
      intro pk _
      let a := ∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
        (liouvilleLambda n : ℝ) * gaussianTermPhi n X
      let b := ∑ n ∈ S_sub.filter (fun n => pk.1 ^ pk.2 ∣ n),
        (liouvilleLambda n : ℝ) * gaussianTermPhi n X
      let s := ∑ n ∈ (Finset.Icc 1 T \ S_sub).filter (fun n => pk.1 ^ pk.2 ∣ n),
        (liouvilleLambda n : ℝ) * gaussianTermPhi n X
      have habs : a = b + s := h_part_S pk X
      have hb_eq : b = a - s := by linarith
      have h_alg :
          δ * a ^ 2 + (1 + 1 / δ) * s ^ 2 - ((a - s) ^ 2 - a ^ 2) =
            (δ * a + s) ^ 2 / δ := by
        field_simp [hδ_ne]; ring
      have h_ineq : b ^ 2 - a ^ 2 ≤ δ * a ^ 2 + (1 + 1 / δ) * s ^ 2 := by
        rw [hb_eq]
        have hnn : 0 ≤ (δ * a + s) ^ 2 / δ := div_nonneg (sq_nonneg _) (le_of_lt hδ)
        linarith
      calc
        (Real.log (pk.1 : ℝ)) ^ 2 * b ^ 2 - (Real.log (pk.1 : ℝ)) ^ 2 * a ^ 2
          = (Real.log (pk.1 : ℝ)) ^ 2 * (b ^ 2 - a ^ 2) := by ring
        _ ≤ (Real.log (pk.1 : ℝ)) ^ 2 * (δ * a ^ 2 + (1 + 1 / δ) * s ^ 2) :=
            mul_le_mul_of_nonneg_left h_ineq (sq_nonneg _)
        _ = δ * ((Real.log (pk.1 : ℝ)) ^ 2 * a ^ 2) +
              (1 + 1 / δ) * ((Real.log (pk.1 : ℝ)) ^ 2 * s ^ 2) := by ring
    have hd1 := div_le_div_of_nonneg_right h_sum_pk (le_of_lt hlog_sq_pos)
    have hd2 := div_le_div_of_nonneg_right hd1 (le_of_lt hX_pos)
    calc
      ((∑ pk ∈ primePowerPairsUpTo T,
            (Real.log (pk.1 : ℝ)) ^ 2 *
              (∑ n ∈ S_sub.filter (fun n => pk.1 ^ pk.2 ∣ n),
                (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) /
          (Real.log X) ^ 2) / X -
        ((∑ pk ∈ primePowerPairsUpTo T,
            (Real.log (pk.1 : ℝ)) ^ 2 *
              (∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
                (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) /
          (Real.log X) ^ 2) / X
        = (((∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ S_sub.filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) -
            (∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2)) /
            (Real.log X) ^ 2) / X := by ring
      _ ≤ ((δ * (∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) +
            (1 + 1 / δ) * (∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ (Finset.Icc 1 T \ S_sub).filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2)) /
            (Real.log X) ^ 2) / X := hd2
      _ = δ * (((∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ (Finset.Icc 1 T).filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) /
            (Real.log X) ^ 2) / X) +
          (1 + 1 / δ) * (((∑ pk ∈ primePowerPairsUpTo T,
              (Real.log (pk.1 : ℝ)) ^ 2 *
                (∑ n ∈ (Finset.Icc 1 T \ S_sub).filter (fun n => pk.1 ^ pk.2 ∣ n),
                  (liouvilleLambda n : ℝ) * gaussianTermPhi n X) ^ 2) /
            (Real.log X) ^ 2) / X) := by ring

private theorem uncovered_strip_phi_bound_tc062_aux
    {p : ℕ} (hp : p.Prime) {Y : ℝ} (hY2 : 2 ≤ Y) :
    ∀ k ∈ uncoveredCutoffStripStations p (canonicalCutoffT Y),
      ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
        0 ≤ gaussianTermPhi k X ∧
          gaussianTermPhi k X ≤
            RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 * Y ^ (5 / 2 : ℝ) /
              (canonicalCutoffT Y : ℝ) ^ 3 := by
  have htau_bds := tau_gt_one_and_lt_eight_tc062_aux
  have htau_pos : 0 < RiemannScope.tau := by linarith only [htau_bds.1]
  have hp_pos_r : (0 : ℝ) < (p : ℝ) := Nat.cast_pos.mpr hp.pos
  have hp_ne_r : (p : ℝ) ≠ 0 := ne_of_gt hp_pos_r
  let T := canonicalCutoffT Y
  have hT1 : 1 ≤ T := canonicalCutoffT_ge_one_tc062_aux (by linarith only [hY2])
  have hT_pos_r : (0 : ℝ) < (T : ℝ) := by exact_mod_cast (by omega : 0 < T)
  obtain ⟨_, _, h_uncov, _⟩ := coveredInteriorStations_props_tc062_aux hp T
  intro k hk X hX
  have h_gt : T / p < k := (h_uncov k hk).1
  have h_mul_gt : T ≤ p * k := by
    have h_mod : T % p < p := Nat.mod_lt T hp.pos
    have h_div_add : p * (T / p) + T % p = T := Nat.div_add_mod T p
    have hk_ge : T / p + 1 ≤ k := by omega
    calc
      T = p * (T / p) + T % p := h_div_add.symm
      _ ≤ p * (T / p) + p := by omega
      _ = p * (T / p + 1) := by ring
      _ ≤ p * k := Nat.mul_le_mul_left p hk_ge
  have hTp_le : (T : ℝ) / (p : ℝ) ≤ (k : ℝ) :=
    (div_le_iff hp_pos_r).mpr (by rw [mul_comm]; exact_mod_cast h_mul_gt)
  obtain ⟨hnn, hub⟩ :=
    gaussianTermPhi_le_of_ge_tc062_aux hY2 hX (div_pos hT_pos_r hp_pos_r) hTp_le
  refine ⟨hnn, ?_⟩
  rw [Real.mul_rpow (le_of_lt htau_pos) (by linarith only [hY2])] at hub
  calc
    gaussianTermPhi k X
      ≤ (RiemannScope.tau ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ)) / ((T : ℝ) / (p : ℝ)) ^ 3 := hub
    _ = RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 * Y ^ (5 / 2 : ℝ) / (T : ℝ) ^ 3 := by
        field_simp [ne_of_gt hT_pos_r, hp_ne_r]; ring

private theorem uncovered_strip_windowEnergy_bound_tc062_aux
    {p : ℕ} (hp : p.Prime) (c_lam c_half : ℝ) :
    ∃ C_strip : ℝ, 0 ≤ C_strip ∧
      ∀ {Y : ℝ}, 2 ≤ Y →
        let T := canonicalCutoffT Y
        let D0 := Nat.floor (Real.log Y)
        windowEnergyNormSq Y
            (fun X =>
              ∑ k ∈ uncoveredCutoffStripStations p T,
                (liouvilleLambda k : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 k X) ≤
          C_strip * (Real.log Y) ^ 2 := by
  have htau_bds := tau_gt_one_and_lt_eight_tc062_aux
  have htau_pos : 0 < RiemannScope.tau := by linarith only [htau_bds.1]
  let B0 : ℝ := (9 / 4 : ℝ) ^ 2 + 18 + 4 * (8 + |c_lam| + |c_half|)
  let M_strip : ℝ :=
    RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 * (2 + 19 * B0)
  let C_strip : ℝ := (RiemannScope.tau - 1) * M_strip ^ 2
  have hB0_nn : 0 ≤ B0 := by dsimp [B0]; positivity
  have hCs_nn : 0 ≤ C_strip := mul_nonneg (by linarith only [htau_bds.1]) (sq_nonneg M_strip)
  refine ⟨C_strip, hCs_nn, ?_⟩
  intro Y hY2
  dsimp only
  obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc062_aux hY2
  obtain ⟨hT_ge2, _, _, hlogT_le, hY52_le, _, hlogY_gt_half⟩ :=
    canonicalCutoffT_bounds_tc062_aux hY2
  let T := canonicalCutoffT Y
  let D0 := Nat.floor (Real.log Y)
  have hT1 : 1 ≤ T := by omega
  have hT_pos_r : (0 : ℝ) < (T : ℝ) := by exact_mod_cast (by omega : 0 < T)
  have hlogY_pos : 0 < Real.log Y := by linarith only [hlogY_gt_half]
  have h1_le_2logY : 1 ≤ 2 * Real.log Y := by linarith only [hlogY_gt_half]
  have h1_le_4logY_sq : 1 ≤ 4 * (Real.log Y) ^ 2 := by
    have hsq := pow_le_pow_left (by norm_num) (le_of_lt hlogY_gt_half) 2
    linarith only [hsq]
  let B_set := uncoveredCutoffStripStations p T
  have hB_sub : B_set ⊆ Finset.Icc 1 T := Finset.sdiff_subset _ _
  have hB_card : (B_set.card : ℝ) ≤ (T : ℝ) := by
    have hc : B_set.card ≤ T := by
      simpa [Nat.card_Icc] using Finset.card_le_card hB_sub
    exact_mod_cast hc
  have h_phi_strip := uncovered_strip_phi_bound_tc062_aux hp hY2
  have h_pt_strip :
      ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
        |∑ k ∈ B_set,
            (liouvilleLambda k : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 k X| ≤
          M_strip * Real.log Y := by
    intro X hX
    have hX_Icc : Y ≤ X ∧ X ≤ RiemannScope.tau * Y := by
      rwa [Set.uIcc_of_le hle, Set.mem_Icc] at hX
    have hlogX_ge : Real.log Y ≤ Real.log X :=
      Real.log_le_log (by linarith only [hY2]) hX_Icc.1
    have hlogX_sq_ge : (Real.log Y) ^ 2 ≤ (Real.log X) ^ 2 :=
      pow_le_pow_left (le_of_lt hlogY_pos) hlogX_ge 2
    have hlogX_sq_pos : 0 < (Real.log X) ^ 2 := sq_pos_of_pos (hprops X hX).2.2.1
    let P_bd : ℝ :=
      RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 * Y ^ (5 / 2 : ℝ) / (T : ℝ) ^ 3
    have hP_nn : 0 ≤ P_bd := by dsimp [P_bd]; positivity
    have h_each_k :
        ∀ k ∈ B_set,
          |(liouvilleLambda k : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 k X| ≤
            P_bd + (|openCoreAdjustedCoeffBeta c_lam c_half T D0 k| / (Real.log Y) ^ 2) * P_bd := by
      intro k hk
      have hk1 : 1 ≤ k := (Finset.mem_Icc.mp (hB_sub hk)).1
      have hlam_abs : |(liouvilleLambda k : ℝ)| = 1 :=
        abs_liouvilleLambda_eq_one_tc062_aux hk1
      have hb_abs :
          |signedAdjustedCoeffB c_lam c_half T D0 k| =
            |openCoreAdjustedCoeffBeta c_lam c_half T D0 k| := by
        unfold signedAdjustedCoeffB
        rw [abs_mul, hlam_abs, one_mul]
      obtain ⟨hphi_nn, hphi_ub⟩ := h_phi_strip k hk X hX
      unfold adjustedStationProfilePsi
      rw [abs_mul, abs_mul, hlam_abs, one_mul, abs_of_nonneg hphi_nn]
      have h1_sub :
          |1 - signedAdjustedCoeffB c_lam c_half T D0 k / (Real.log X) ^ 2| ≤
            1 + |openCoreAdjustedCoeffBeta c_lam c_half T D0 k| / (Real.log Y) ^ 2 := by
        have ht := abs_sub (1 : ℝ) (signedAdjustedCoeffB c_lam c_half T D0 k / (Real.log X) ^ 2)
        rw [abs_one, abs_div, hb_abs, abs_of_pos hlogX_sq_pos] at ht
        have hd :
            |openCoreAdjustedCoeffBeta c_lam c_half T D0 k| / (Real.log X) ^ 2 ≤
              |openCoreAdjustedCoeffBeta c_lam c_half T D0 k| / (Real.log Y) ^ 2 :=
          div_le_div_of_nonneg_left (abs_nonneg _) (sq_pos_of_pos hlogY_pos) hlogX_sq_ge
        linarith only [ht, hd]
      calc
        |1 - signedAdjustedCoeffB c_lam c_half T D0 k / (Real.log X) ^ 2| * gaussianTermPhi k X
          ≤ (1 + |openCoreAdjustedCoeffBeta c_lam c_half T D0 k| / (Real.log Y) ^ 2) * P_bd :=
            mul_le_mul h1_sub hphi_ub hphi_nn (by positivity)
        _ = P_bd + (|openCoreAdjustedCoeffBeta c_lam c_half T D0 k| / (Real.log Y) ^ 2) * P_bd := by ring
    have h_sum_beta_B :
        (∑ k ∈ B_set, |openCoreAdjustedCoeffBeta c_lam c_half T D0 k|) ≤
          19 * B0 * (T : ℝ) * (Real.log Y) ^ 3 := by
      have h_sub_le :
          (∑ k ∈ B_set, |openCoreAdjustedCoeffBeta c_lam c_half T D0 k|) ≤
            ∑ k ∈ Finset.Icc 1 T, |openCoreAdjustedCoeffBeta c_lam c_half T D0 k| :=
        Finset.sum_le_sum_of_subset_of_nonneg hB_sub (fun _ _ _ => abs_nonneg _)
      have h_tot_beta := sum_abs_openCoreAdjustedCoeffBeta_Icc_le_tc062_aux hT_ge2 D0 c_lam c_half
      have hD0_le : (D0 : ℝ) ≤ Real.log Y := Nat.floor_le (le_of_lt hlogY_pos)
      have h_19 : 2 * (D0 : ℝ) + 4 * (1 + Real.log (T : ℝ)) ≤ 19 * Real.log Y := by
        linarith only [hD0_le, h1_le_2logY, hlogT_le]
      have h_big_le :
          (Real.log (T : ℝ)) ^ 2 + 4 * Real.log (T : ℝ) + 8 + |c_lam| + |c_half| ≤
            B0 * (Real.log Y) ^ 2 := by
        have hlT_nn : 0 ≤ Real.log (T : ℝ) := Real.log_nonneg (by exact_mod_cast hT1)
        have hlT_sq : (Real.log (T : ℝ)) ^ 2 ≤ (9 / 4 : ℝ) ^ 2 * (Real.log Y) ^ 2 := by
          have hp_sq := pow_le_pow_left hlT_nn hlogT_le 2
          linarith only [hp_sq, show ((9 / 4 : ℝ) * Real.log Y) ^ 2 =
            (9 / 4 : ℝ) ^ 2 * (Real.log Y) ^ 2 by ring]
        have hlT_lin : 4 * Real.log (T : ℝ) ≤ 18 * (Real.log Y) ^ 2 := by
          have h1 : 4 * Real.log (T : ℝ) ≤ 9 * Real.log Y := by linarith only [hlogT_le]
          have h2 : 9 * Real.log Y ≤ 9 * (Real.log Y * (2 * Real.log Y)) :=
            mul_le_mul_of_nonneg_left
              (le_mul_of_one_le_right (le_of_lt hlogY_pos) h1_le_2logY) (by norm_num)
          linarith only [h1, h2, show 9 * (Real.log Y * (2 * Real.log Y)) = 18 * (Real.log Y) ^ 2 by ring]
        have h_c_abs :
            8 + |c_lam| + |c_half| ≤ 4 * (8 + |c_lam| + |c_half|) * (Real.log Y) ^ 2 := by
          have h1 := mul_le_mul_of_nonneg_left h1_le_4logY_sq
            (show 0 ≤ 8 + |c_lam| + |c_half| by positivity)
          linarith only [h1, show (8 + |c_lam| + |c_half|) * (4 * (Real.log Y) ^ 2) =
            4 * (8 + |c_lam| + |c_half|) * (Real.log Y) ^ 2 by ring]
        change (Real.log (T : ℝ)) ^ 2 + 4 * Real.log (T : ℝ) + 8 + |c_lam| + |c_half| ≤
          ((9 / 4 : ℝ) ^ 2 + 18 + 4 * (8 + |c_lam| + |c_half|)) * (Real.log Y) ^ 2
        linarith only [hlT_sq, hlT_lin, h_c_abs,
          show ((9 / 4 : ℝ) ^ 2 + 18 + 4 * (8 + |c_lam| + |c_half|)) * (Real.log Y) ^ 2 =
            (9 / 4 : ℝ) ^ 2 * (Real.log Y) ^ 2 + 18 * (Real.log Y) ^ 2 +
              4 * (8 + |c_lam| + |c_half|) * (Real.log Y) ^ 2 by ring]
      have h_prod1 :
          (2 * (D0 : ℝ) + 4 * (1 + Real.log (T : ℝ))) *
              ((Real.log (T : ℝ)) ^ 2 + 4 * Real.log (T : ℝ) + 8 + |c_lam| + |c_half|) ≤
            (19 * Real.log Y) * (B0 * (Real.log Y) ^ 2) :=
        mul_le_mul h_19 h_big_le (by positivity)
          (mul_nonneg (by norm_num) (le_of_lt hlogY_pos))
      have h_prod2 := mul_le_mul_of_nonneg_right h_prod1 (le_of_lt hT_pos_r)
      have _ := hB0_nn
      linarith only [h_sub_le, h_tot_beta, h_prod2,
        show (19 * Real.log Y) * (B0 * (Real.log Y) ^ 2) * (T : ℝ) =
          19 * B0 * (T : ℝ) * (Real.log Y) ^ 3 by ring,
        show (2 * (D0 : ℝ) + 4 * (1 + Real.log (T : ℝ))) *
            ((Real.log (T : ℝ)) ^ 2 + 4 * Real.log (T : ℝ) + 8 + |c_lam| + |c_half|) * (T : ℝ) =
          (T : ℝ) * (2 * (D0 : ℝ) + 4 * (1 + Real.log (T : ℝ))) *
            ((Real.log (T : ℝ)) ^ 2 + 4 * Real.log (T : ℝ) + 8 + |c_lam| + |c_half|) by ring]
    have h_TP_le :
        (T : ℝ) * P_bd ≤ RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 := by
      have h_ratio_le1 : Y ^ (5 / 2 : ℝ) / (T : ℝ) ^ 2 ≤ 1 :=
        (div_le_one (sq_pos_of_pos hT_pos_r)).mpr hY52_le
      have h_eq :
          (T : ℝ) * P_bd =
            (RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3) * (Y ^ (5 / 2 : ℝ) / (T : ℝ) ^ 2) := by
        change (T : ℝ) * (RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 * Y ^ (5 / 2 : ℝ) / (T : ℝ) ^ 3) = _
        field_simp [ne_of_gt hT_pos_r]; ring
      rw [h_eq]
      exact le_trans
        (mul_le_mul_of_nonneg_left h_ratio_le1 (by positivity))
        (by rw [mul_one])
    have h_card_P :
        (B_set.card : ℝ) * P_bd ≤
          RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 * (2 * Real.log Y) := by
      have h1 : (B_set.card : ℝ) * P_bd ≤ (T : ℝ) * P_bd :=
        mul_le_mul_of_nonneg_right hB_card hP_nn
      have h2 := le_trans h1 h_TP_le
      have hm := mul_le_mul_of_nonneg_left h1_le_2logY
        (show 0 ≤ RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 by positivity)
      linarith only [h2, hm,
        show (RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3) * 1 =
          RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 by ring]
    have h_beta_P :
        ((∑ k ∈ B_set, |openCoreAdjustedCoeffBeta c_lam c_half T D0 k|) / (Real.log Y) ^ 2) * P_bd ≤
          RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 * (19 * B0 * Real.log Y) := by
      have h_div :
          (∑ k ∈ B_set, |openCoreAdjustedCoeffBeta c_lam c_half T D0 k|) / (Real.log Y) ^ 2 ≤
            19 * B0 * (T : ℝ) * Real.log Y := by
        rw [div_le_iff (sq_pos_of_pos hlogY_pos)]
        calc
          (∑ k ∈ B_set, |openCoreAdjustedCoeffBeta c_lam c_half T D0 k|)
            ≤ 19 * B0 * (T : ℝ) * (Real.log Y) ^ 3 := h_sum_beta_B
          _ = (19 * B0 * (T : ℝ) * Real.log Y) * (Real.log Y) ^ 2 := by ring
      calc
        ((∑ k ∈ B_set, |openCoreAdjustedCoeffBeta c_lam c_half T D0 k|) / (Real.log Y) ^ 2) * P_bd
          ≤ (19 * B0 * (T : ℝ) * Real.log Y) * P_bd :=
            mul_le_mul_of_nonneg_right h_div hP_nn
        _ = (19 * B0 * Real.log Y) * ((T : ℝ) * P_bd) := by ring
        _ ≤ (19 * B0 * Real.log Y) * (RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3) :=
            mul_le_mul_of_nonneg_left h_TP_le (by positivity)
        _ = RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 * (19 * B0 * Real.log Y) := by ring
    calc
      |∑ k ∈ B_set, (liouvilleLambda k : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 k X|
        ≤ ∑ k ∈ B_set,
            |(liouvilleLambda k : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 k X| :=
          Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ k ∈ B_set,
            (P_bd + (|openCoreAdjustedCoeffBeta c_lam c_half T D0 k| / (Real.log Y) ^ 2) * P_bd) :=
          Finset.sum_le_sum h_each_k
      _ = (B_set.card : ℝ) * P_bd +
            ((∑ k ∈ B_set, |openCoreAdjustedCoeffBeta c_lam c_half T D0 k|) / (Real.log Y) ^ 2) * P_bd := by
          rw [Finset.sum_add_distrib, Finset.sum_const, nsmul_eq_mul, ← Finset.sum_mul,
            ← Finset.sum_div]
      _ ≤ RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 * (2 * Real.log Y) +
            RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 * (19 * B0 * Real.log Y) :=
          add_le_add h_card_P h_beta_P
      _ = M_strip * Real.log Y := by dsimp [M_strip]; ring
  have h_strip_cont :
      ContinuousOn
        (fun X =>
          ∑ k ∈ B_set,
            (liouvilleLambda k : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 k X)
        (Set.uIcc Y (RiemannScope.tau * Y)) :=
    continuousOn_finset_sum _ (fun k _ =>
      continuousOn_const.mul (continuousOn_adjustedStationProfilePsi_tc062_aux hY2 c_lam c_half T D0 k))
  have h_strip_int :
      IntervalIntegrable
        (fun X =>
          (∑ k ∈ B_set,
              (liouvilleLambda k : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 k X) *
            (∑ k ∈ B_set,
              (liouvilleLambda k : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 k X) / X)
        volume Y (RiemannScope.tau * Y) :=
    ((h_strip_cont.mul h_strip_cont).div continuousOn_id
      (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
  unfold windowEnergyNormSq windowPairing
  have hc_strip_int :
      IntervalIntegrable (fun _ : ℝ => (M_strip * Real.log Y) ^ 2 / Y)
        volume Y (RiemannScope.tau * Y) := intervalIntegrable_const
  have h_m :=
    intervalIntegral.integral_mono_on hle h_strip_int hc_strip_int (by
        intro X hX
        have hX_in : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
        have hX_pos : 0 < X := by rw [Set.mem_Icc] at hX; linarith only [hY2, hX.1]
        have habs := h_pt_strip X hX_in
        have hsq :
            (∑ k ∈ B_set,
                (liouvilleLambda k : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 k X) *
              (∑ k ∈ B_set,
                (liouvilleLambda k : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 k X) ≤
              (M_strip * Real.log Y) ^ 2 := by
          have h1 := pow_le_pow_left (abs_nonneg _) habs 2
          rwa [sq_abs, sq] at h1
        calc
          _ ≤ (M_strip * Real.log Y) ^ 2 / X :=
              div_le_div_of_nonneg_right hsq (le_of_lt hX_pos)
          _ ≤ (M_strip * Real.log Y) ^ 2 / Y :=
              div_le_div_of_nonneg_left (sq_nonneg _) (by linarith only [hY2]) hX.1)
  rw [intervalIntegral.integral_const, smul_eq_mul] at h_m
  have h_rhs :
      (RiemannScope.tau * Y - Y) * ((M_strip * Real.log Y) ^ 2 / Y) =
        C_strip * (Real.log Y) ^ 2 := by
    change (RiemannScope.tau * Y - Y) * ((M_strip * Real.log Y) ^ 2 / Y) =
      ((RiemannScope.tau - 1) * M_strip ^ 2) * (Real.log Y) ^ 2
    field_simp [show Y ≠ 0 by linarith only [hY2]]
    ring
  dsimp only
  linarith only [h_m, h_rhs]

private theorem uncovered_strip_diagDtilde_bound_tc062_aux
    {p : ℕ} (hp : p.Prime) :
    ∃ C_tail : ℝ, 0 ≤ C_tail ∧
      ∀ {Y : ℝ}, 2 ≤ Y →
        subsetPrimePowerDiagDtilde (uncoveredCutoffStripStations p (canonicalCutoffT Y)) Y ≤
          C_tail := by
  have htau_bds := tau_gt_one_and_lt_eight_tc062_aux
  have htau_pos : 0 < RiemannScope.tau := by linarith only [htau_bds.1]
  have hp_pos_r : (0 : ℝ) < (p : ℝ) := Nat.cast_pos.mpr hp.pos
  have h_tau1 : 0 ≤ RiemannScope.tau - 1 := by linarith only [htau_bds.1]
  let C_tail : ℝ :=
    (RiemannScope.tau - 1) * (9 / 4 : ℝ) ^ 2 * RiemannScope.tau ^ 5 * (p : ℝ) ^ 6
  have hCt_nn : 0 ≤ C_tail :=
    mul_nonneg
      (mul_nonneg
        (mul_nonneg h_tau1 (sq_nonneg _))
        (pow_nonneg (le_of_lt htau_pos) 5))
      (pow_nonneg (le_of_lt hp_pos_r) 6)
  refine ⟨C_tail, hCt_nn, ?_⟩
  intro Y hY2
  obtain ⟨hle, _⟩ := uIcc_tau_props_tc062_aux hY2
  obtain ⟨hT_ge2, _, _, hlogT_le, _, hY5_le, hlogY_gt_half⟩ :=
    canonicalCutoffT_bounds_tc062_aux hY2
  let T := canonicalCutoffT Y
  have hT1 : 1 ≤ T := by omega
  have hT_pos_r : (0 : ℝ) < (T : ℝ) := by exact_mod_cast (by omega : 0 < T)
  have hlogY_pos : 0 < Real.log Y := by linarith only [hlogY_gt_half]
  let B_set := uncoveredCutoffStripStations p T
  have hB_sub : B_set ⊆ Finset.Icc 1 T := Finset.sdiff_subset _ _
  have hB_card : (B_set.card : ℝ) ≤ (T : ℝ) := by
    have hc : B_set.card ≤ T := by
      simpa [Nat.card_Icc] using Finset.card_le_card hB_sub
    exact_mod_cast hc
  have h_phi_strip := uncovered_strip_phi_bound_tc062_aux hp hY2
  unfold subsetPrimePowerDiagDtilde
  have h_cmn_le :
      ∀ m ∈ B_set, ∀ n ∈ B_set,
        0 ≤ commonPrimePowerLogSq m n ∧
          commonPrimePowerLogSq m n ≤ (Real.log (T : ℝ)) ^ 2 := by
    intro m hm n _
    have hm_bds := Finset.mem_Icc.mp (hB_sub hm)
    have h_nn : 0 ≤ commonPrimePowerLogSq m n := by
      unfold commonPrimePowerLogSq
      exact Finset.sum_nonneg (fun _ _ => sq_nonneg _)
    have h_le_mm : commonPrimePowerLogSq m n ≤ commonPrimePowerLogSq m m := by
      unfold commonPrimePowerLogSq
      apply Finset.sum_le_sum_of_subset_of_nonneg
      · intro pk hpk
        simp only [Finset.mem_filter, primePowerPairsUpTo, Finset.mem_product,
          primesUpToFinset, Finset.mem_Icc, Nat.dvd_gcd_iff, Nat.gcd_self] at hpk ⊢
        rcases hpk with ⟨⟨⟨⟨⟨hr2, hr_mn⟩, hr_pr⟩, ⟨hk1, hk_mn⟩⟩, hrk_mn⟩, ⟨hdm, _⟩⟩
        have h_mn_le_m : min m n ≤ m := min_le_left m n
        rw [min_self]
        exact ⟨⟨⟨⟨⟨hr2, le_trans hr_mn h_mn_le_m⟩, hr_pr⟩,
          ⟨hk1, le_trans hk_mn h_mn_le_m⟩⟩, le_trans hrk_mn h_mn_le_m⟩, hdm⟩
      · intro _ _ _; exact sq_nonneg _
    have h_off_nn :=
      ((finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.1.2.2.2
        m hm_bds.1).1
    unfold offDiagPrimePowerWeight at h_off_nn
    have h_mm_le : commonPrimePowerLogSq m m ≤ (Real.log (m : ℝ)) ^ 2 := by
      linarith only [h_off_nn, sq (Real.log (m : ℝ))]
    have hlogm_nn : 0 ≤ Real.log (m : ℝ) := Real.log_nonneg (by exact_mod_cast hm_bds.1)
    have hlogm_le : Real.log (m : ℝ) ≤ Real.log (T : ℝ) :=
      Real.log_le_log (Nat.cast_pos.mpr hm_bds.1) (by exact_mod_cast hm_bds.2)
    exact ⟨h_nn, le_trans h_le_mm (le_trans h_mm_le (pow_le_pow_left hlogm_nn hlogm_le 2))⟩
  let G2_bd : ℝ :=
    (RiemannScope.tau - 1) *
      (RiemannScope.tau ^ 5 * (p : ℝ) ^ 6 * Y ^ 5 / (T : ℝ) ^ 6) / (Real.log Y) ^ 2
  have h_ker2_le :
      ∀ m ∈ B_set, ∀ n ∈ B_set,
        0 ≤ logWeightedWindowKernel 2 Y m n ∧ logWeightedWindowKernel 2 Y m n ≤ G2_bd := by
    intro m hm n hn
    have hi : IntervalIntegrable _ volume Y (RiemannScope.tau * Y) :=
      (continuousOn_logWeightedKernel_integrand_tc062_aux hY2 2 m n).intervalIntegrable
    unfold logWeightedWindowKernel
    have hnn :
        0 ≤ ∫ X in Y..(RiemannScope.tau * Y),
          (gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ 2) / X := by
      apply intervalIntegral.integral_nonneg hle
      intro X hX
      have hX_in : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
      obtain ⟨hm_nn, _⟩ := h_phi_strip m hm X hX_in
      obtain ⟨hn_nn, _⟩ := h_phi_strip n hn X hX_in
      exact div_nonneg (div_nonneg (mul_nonneg hm_nn hn_nn) (sq_nonneg _))
        (by rw [Set.mem_Icc] at hX; linarith only [hY2, hX.1])
    let M2 : ℝ :=
      (RiemannScope.tau ^ 5 * (p : ℝ) ^ 6 * Y ^ 5 / (T : ℝ) ^ 6) /
        ((Real.log Y) ^ 2 * Y)
    have hm2_int : IntervalIntegrable (fun _ : ℝ => M2) volume Y (RiemannScope.tau * Y) :=
      intervalIntegrable_const
    have hm_int :=
      intervalIntegral.integral_mono_on hle hi hm2_int (by
        intro X hX
        have hX_in : X ∈ Set.uIcc Y (RiemannScope.tau * Y) := by rwa [Set.uIcc_of_le hle]
        have hlogX_ge : Real.log Y ≤ Real.log X := Real.log_le_log (by linarith only [hY2]) hX.1
        have hlogX_sq_ge : (Real.log Y) ^ 2 ≤ (Real.log X) ^ 2 :=
          pow_le_pow_left (le_of_lt hlogY_pos) hlogX_ge 2
        obtain ⟨_, hm_ub⟩ := h_phi_strip m hm X hX_in
        obtain ⟨hn_nn, hn_ub⟩ := h_phi_strip n hn X hX_in
        have h_prod_phi :
            gaussianTermPhi m X * gaussianTermPhi n X ≤
              RiemannScope.tau ^ 5 * (p : ℝ) ^ 6 * Y ^ 5 / (T : ℝ) ^ 6 := by
          have hp1 := mul_le_mul hm_ub hn_ub hn_nn (by positivity)
          have htau5 : (RiemannScope.tau ^ (5 / 2 : ℝ)) ^ 2 = RiemannScope.tau ^ 5 := by
            rw [← Real.rpow_natCast _ 2, ← Real.rpow_mul (le_of_lt htau_pos)]
            have he : (5 / 2 : ℝ) * ((2 : ℕ) : ℝ) = ((5 : ℕ) : ℝ) := by norm_num
            rw [he, Real.rpow_natCast]
          have hY5 : (Y ^ (5 / 2 : ℝ)) ^ 2 = Y ^ 5 := by
            rw [← Real.rpow_natCast _ 2, ← Real.rpow_mul (by linarith only [hY2])]
            have he : (5 / 2 : ℝ) * ((2 : ℕ) : ℝ) = ((5 : ℕ) : ℝ) := by norm_num
            rw [he, Real.rpow_natCast]
          have hrhs :
              (RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 * Y ^ (5 / 2 : ℝ) / (T : ℝ) ^ 3) *
                (RiemannScope.tau ^ (5 / 2 : ℝ) * (p : ℝ) ^ 3 * Y ^ (5 / 2 : ℝ) / (T : ℝ) ^ 3) =
              RiemannScope.tau ^ 5 * (p : ℝ) ^ 6 * Y ^ 5 / (T : ℝ) ^ 6 := by
            calc
              _ = ((RiemannScope.tau ^ (5 / 2 : ℝ)) ^ 2 * (p : ℝ) ^ 6 *
                    (Y ^ (5 / 2 : ℝ)) ^ 2) / (T : ℝ) ^ 6 := by ring
              _ = RiemannScope.tau ^ 5 * (p : ℝ) ^ 6 * Y ^ 5 / (T : ℝ) ^ 6 := by
                  rw [htau5, hY5]
          rwa [hrhs] at hp1
        change (gaussianTermPhi m X * gaussianTermPhi n X / (Real.log X) ^ 2) / X ≤
          (RiemannScope.tau ^ 5 * (p : ℝ) ^ 6 * Y ^ 5 / (T : ℝ) ^ 6) / ((Real.log Y) ^ 2 * Y)
        rw [div_div]
        exact div_le_div (by positivity) h_prod_phi
          (mul_pos (sq_pos_of_pos hlogY_pos) (by linarith only [hY2]))
          (mul_le_mul hlogX_sq_ge hX.1 (by linarith only [hY2, hX.1]) (sq_nonneg _)))
    rw [intervalIntegral.integral_const, smul_eq_mul] at hm_int
    have h_eq_g2 : (RiemannScope.tau * Y - Y) * M2 = G2_bd := by
      change (RiemannScope.tau * Y - Y) *
          ((RiemannScope.tau ^ 5 * (p : ℝ) ^ 6 * Y ^ 5 / (T : ℝ) ^ 6) / ((Real.log Y) ^ 2 * Y)) =
        (RiemannScope.tau - 1) *
          (RiemannScope.tau ^ 5 * (p : ℝ) ^ 6 * Y ^ 5 / (T : ℝ) ^ 6) / (Real.log Y) ^ 2
      field_simp [show Y ≠ 0 by linarith only [hY2], ne_of_gt (sq_pos_of_pos hlogY_pos)]
      ring
    exact ⟨hnn, by linarith only [hm_int, h_eq_g2]⟩
  have h_each_mn :
      ∀ m ∈ B_set, ∀ n ∈ B_set,
        (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
            logWeightedWindowKernel 2 Y m n ≤
          (Real.log (T : ℝ)) ^ 2 * G2_bd := by
    intro m hm n hn
    have hm1 : 1 ≤ m := (Finset.mem_Icc.mp (hB_sub hm)).1
    have hn1 : 1 ≤ n := (Finset.mem_Icc.mp (hB_sub hn)).1
    have hlm : |(liouvilleLambda m : ℝ)| = 1 := abs_liouvilleLambda_eq_one_tc062_aux hm1
    have hln : |(liouvilleLambda n : ℝ)| = 1 := abs_liouvilleLambda_eq_one_tc062_aux hn1
    obtain ⟨hc_nn, hc_ub⟩ := h_cmn_le m hm n hn
    obtain ⟨hk_nn, hk_ub⟩ := h_ker2_le m hm n hn
    have habs_le :
        (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
            logWeightedWindowKernel 2 Y m n ≤
          commonPrimePowerLogSq m n * logWeightedWindowKernel 2 Y m n := by
      have h1 := le_abs_self
        ((liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
          logWeightedWindowKernel 2 Y m n)
      rw [abs_mul, abs_mul, abs_mul, hlm, hln, one_mul, one_mul,
        abs_of_nonneg hc_nn, abs_of_nonneg hk_nn] at h1
      exact h1
    exact le_trans habs_le (mul_le_mul hc_ub hk_ub hk_nn (sq_nonneg _))
  have h_double :
      (∑ m ∈ B_set, ∑ n ∈ B_set,
          (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
            logWeightedWindowKernel 2 Y m n) ≤
        (B_set.card : ℝ) ^ 2 * ((Real.log (T : ℝ)) ^ 2 * G2_bd) := by
    calc
      _ ≤ ∑ _m ∈ B_set, ∑ _n ∈ B_set, ((Real.log (T : ℝ)) ^ 2 * G2_bd) :=
          Finset.sum_le_sum (fun m hm => Finset.sum_le_sum (fun n hn => h_each_mn m hm n hn))
      _ = (B_set.card : ℝ) ^ 2 * ((Real.log (T : ℝ)) ^ 2 * G2_bd) := by
          simp [sq]; ring
  have h_card_sq : (B_set.card : ℝ) ^ 2 ≤ (T : ℝ) ^ 2 :=
    pow_le_pow_left (by positivity) hB_card 2
  have h_log_ratio : (Real.log (T : ℝ)) ^ 2 / (Real.log Y) ^ 2 ≤ (9 / 4 : ℝ) ^ 2 := by
    rw [div_le_iff (sq_pos_of_pos hlogY_pos)]
    have hlT_nn : 0 ≤ Real.log (T : ℝ) := Real.log_nonneg (by exact_mod_cast hT1)
    have hp_sq := pow_le_pow_left hlT_nn hlogT_le 2
    linarith only [hp_sq, show ((9 / 4 : ℝ) * Real.log Y) ^ 2 =
      (9 / 4 : ℝ) ^ 2 * (Real.log Y) ^ 2 by ring]
  have h_Y5_T4 : Y ^ 5 / (T : ℝ) ^ 4 ≤ 1 :=
    (div_le_one (pow_pos hT_pos_r 4)).mpr hY5_le
  have hY_nn : 0 ≤ Y := by linarith only [hY2]
  have h_G2_nn : 0 ≤ G2_bd := by
    have h_num : 0 ≤ RiemannScope.tau ^ 5 * (p : ℝ) ^ 6 * Y ^ 5 :=
      mul_nonneg (mul_nonneg (pow_nonneg (le_of_lt htau_pos) 5) (pow_nonneg (le_of_lt hp_pos_r) 6))
        (pow_nonneg hY_nn 5)
    have h_den1 : 0 ≤ (T : ℝ) ^ 6 := pow_nonneg (le_of_lt hT_pos_r) 6
    have h_den2 : 0 ≤ (Real.log Y) ^ 2 := sq_nonneg (Real.log Y)
    exact div_nonneg (mul_nonneg h_tau1 (div_nonneg h_num h_den1)) h_den2
  calc
    (∑ m ∈ B_set, ∑ n ∈ B_set,
        (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) * commonPrimePowerLogSq m n *
          logWeightedWindowKernel 2 Y m n)
      ≤ (T : ℝ) ^ 2 * ((Real.log (T : ℝ)) ^ 2 * G2_bd) :=
        le_trans h_double (mul_le_mul_of_nonneg_right h_card_sq (mul_nonneg (sq_nonneg _) h_G2_nn))
    _ = ((RiemannScope.tau - 1) * RiemannScope.tau ^ 5 * (p : ℝ) ^ 6) *
          ((Real.log (T : ℝ)) ^ 2 / (Real.log Y) ^ 2) * (Y ^ 5 / (T : ℝ) ^ 4) := by
        change (T : ℝ) ^ 2 *
            ((Real.log (T : ℝ)) ^ 2 *
              ((RiemannScope.tau - 1) *
                (RiemannScope.tau ^ 5 * (p : ℝ) ^ 6 * Y ^ 5 / (T : ℝ) ^ 6) / (Real.log Y) ^ 2)) = _
        field_simp [ne_of_gt hT_pos_r, ne_of_gt (sq_pos_of_pos hlogY_pos)]
        ring
    _ ≤ ((RiemannScope.tau - 1) * RiemannScope.tau ^ 5 * (p : ℝ) ^ 6) *
          (9 / 4 : ℝ) ^ 2 * 1 := by
        have h_pref_nn : 0 ≤ (RiemannScope.tau - 1) * RiemannScope.tau ^ 5 * (p : ℝ) ^ 6 :=
          mul_nonneg
            (mul_nonneg h_tau1 (pow_nonneg (le_of_lt htau_pos) 5))
            (pow_nonneg (le_of_lt hp_pos_r) 6)
        have hm1 := mul_le_mul_of_nonneg_left h_log_ratio h_pref_nn
        exact mul_le_mul hm1 h_Y5_T4
          (div_nonneg (pow_nonneg hY_nn 5) (pow_nonneg (le_of_lt hT_pos_r) 4))
          (mul_nonneg h_pref_nn (sq_nonneg _))
    _ = C_tail := by
        change _ = (RiemannScope.tau - 1) * (9 / 4 : ℝ) ^ 2 * RiemannScope.tau ^ 5 * (p : ℝ) ^ 6
        ring

private theorem trunc_iff_interior_closure_hypothesis_tc062_aux
    {p : ℕ} (hp : p.Prime) (c_lam c_half : ℝ) :
    MixedCovarianceClosureHypothesis
        (canonicalTruncatedSignedRemainderF c_lam c_half) canonicalPrimePowerDiagDtilde ↔
      MixedCovarianceClosureHypothesis
        (canonicalInteriorPairedRemainderF c_lam c_half p) canonicalPrimePowerDiagDtilde := by
  obtain ⟨C_strip, hCs_nn, h_strip_bd⟩ := uncovered_strip_windowEnergy_bound_tc062_aux hp c_lam c_half
  obtain ⟨C_tail, hCt_nn, h_tail_bd⟩ := uncovered_strip_diagDtilde_bound_tc062_aux hp
  have h_self_bds :=
    (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2
  let C_self : ℝ := 186 * (RiemannScope.tau - 1)
  have hCself_nn : 0 ≤ C_self := le_of_lt h_self_bds.1
  have hD_nn : ∀ Y : ℝ, 2 ≤ Y → 0 ≤ canonicalPrimePowerDiagDtilde Y :=
    fun Y hY2 => (signed_remainder_equivalence_and_sufficient_core_relaxation_tc061r).1.2.1 hY2
  let C_err : ℝ := 8 * C_self + 2 * C_strip + 16 * C_tail
  have hCerr_nn : 0 ≤ C_err :=
    add_nonneg
      (add_nonneg (mul_nonneg (by norm_num) hCself_nn) (mul_nonneg (by norm_num) hCs_nn))
      (mul_nonneg (by norm_num) hCt_nn)
  have h_both :
      ∀ Y : ℝ, Real.exp 1 ≤ Y →
        canonicalInteriorPairedRemainderF c_lam c_half p Y ≤
            (1 + 1 / Real.log Y) * canonicalTruncatedSignedRemainderF c_lam c_half Y +
              (12 / Real.log Y) * canonicalPrimePowerDiagDtilde Y +
              C_err * (Real.log Y) ^ 3 ∧
          canonicalTruncatedSignedRemainderF c_lam c_half Y ≤
            (1 + 1 / Real.log Y) * canonicalInteriorPairedRemainderF c_lam c_half p Y +
              (12 / Real.log Y) * canonicalPrimePowerDiagDtilde Y +
              C_err * (Real.log Y) ^ 3 := by
    intro Y hY_ge_e
    have he_ge2 : (2 : ℝ) ≤ Real.exp 1 := by linarith only [Real.add_one_le_exp (1 : ℝ)]
    have hY2 : 2 ≤ Y := le_trans he_ge2 hY_ge_e
    have hT1 : 1 ≤ canonicalCutoffT Y := canonicalCutoffT_ge_one_tc062_aux (by linarith only [hY2])
    have hlog_ge1 : 1 ≤ Real.log Y := by
      have h := Real.log_le_log (Real.exp_pos 1) hY_ge_e
      rwa [Real.log_exp] at h
    have hlog_pos : 0 < Real.log Y := lt_of_lt_of_le zero_lt_one hlog_ge1
    have h_log3_ge1 : 1 ≤ (Real.log Y) ^ 3 := by
      simpa using pow_le_pow_left zero_le_one hlog_ge1 3
    let δ : ℝ := 1 / Real.log Y
    have hδ_pos : 0 < δ := by dsimp [δ]; positivity
    have hδ_le1 : δ ≤ 1 := div_le_one_of_le hlog_ge1 (le_of_lt hlog_pos)
    have h1_div_δ : 1 / δ = Real.log Y := one_div_one_div (Real.log Y)
    let T := canonicalCutoffT Y
    let D0 := Nat.floor (Real.log Y)
    let S_sub := coveredInteriorStations p T
    let B_set := uncoveredCutoffStripStations p T
    have hS_sub : S_sub ⊆ Finset.Icc 1 T := (coveredInteriorStations_props_tc062_aux hp T).1
    let f_int : ℝ → ℝ := fun X =>
      ∑ n ∈ S_sub, (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X
    let f_strip : ℝ → ℝ := fun X =>
      ∑ k ∈ uncoveredCutoffStripStations p T,
        (liouvilleLambda k : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 k X
    have hf_int_cont : ContinuousOn f_int (Set.uIcc Y (RiemannScope.tau * Y)) :=
      continuousOn_finset_sum _ (fun n _ =>
        continuousOn_const.mul (continuousOn_adjustedStationProfilePsi_tc062_aux hY2 c_lam c_half T D0 n))
    have hf_strip_cont : ContinuousOn f_strip (Set.uIcc Y (RiemannScope.tau * Y)) :=
      continuousOn_finset_sum _ (fun n _ =>
        continuousOn_const.mul (continuousOn_adjustedStationProfilePsi_tc062_aux hY2 c_lam c_half T D0 n))
    obtain ⟨hy_sum_le, hy_int_le⟩ :=
      windowEnergyNormSq_young_add_tc062_aux hY2 hf_int_cont hf_strip_cont hδ_pos
    have h_sum_eq_all :
        windowEnergyNormSq Y (fun X => f_int X + f_strip X) =
          windowEnergyNormSq Y
            (fun X =>
              ∑ n ∈ Finset.Icc 1 T,
                (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) := by
      unfold windowEnergyNormSq windowPairing
      apply intervalIntegral.integral_congr
      intro X _
      have h_u : Finset.Icc 1 T = S_sub ∪ B_set := (Finset.union_sdiff_of_subset hS_sub).symm
      have h_d : Disjoint S_sub B_set := Finset.disjoint_sdiff
      have h_pt :
          (∑ n ∈ Finset.Icc 1 T,
              (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) =
            f_int X + f_strip X := by
        conv_lhs => rw [h_u]
        exact Finset.sum_union h_d
      dsimp only
      rw [h_pt]
    rw [h_sum_eq_all] at hy_sum_le hy_int_le
    have h_id_all :=
      subset_hcal_bilinear_eq_windowNorm_sub_tc062_aux hY2 hT1 D0 c_lam c_half
        (Finset.Icc 1 T) (Finset.Subset.refl _)
    have h_id_Ssub :=
      subset_hcal_bilinear_eq_windowNorm_sub_tc062_aux hY2 hT1 D0 c_lam c_half S_sub hS_sub
    rw [← interiorPairedRemainderF_eq_subset_hcal_tc062_aux hp c_lam c_half T D0 Y] at h_id_Ssub
    have hD_T_eq :
        subsetPrimePowerDiagDtilde (Finset.Icc 1 T) Y = inheritedPrimePowerDiagDtilde T Y :=
      (((finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).1 hY2 T).1).symm
    have hX_T_eq :
        subsetPrimePowerSelfCollisionXself (Finset.Icc 1 T) Y =
          inheritedPrimePowerSelfCollisionXself T Y := rfl
    change truncatedSignedRemainderF c_lam c_half T D0 Y = _ at h_id_all
    rw [hD_T_eq, hX_T_eq] at h_id_all
    have h_norm_all :
        windowEnergyNormSq Y
            (fun X =>
              ∑ n ∈ Finset.Icc 1 T,
                (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) =
          4 * inheritedPrimePowerDiagDtilde T Y +
            4 * inheritedPrimePowerSelfCollisionXself T Y +
            truncatedSignedRemainderF c_lam c_half T D0 Y := by linarith only [h_id_all]
    have h_norm_int :
        windowEnergyNormSq Y f_int =
          4 * subsetPrimePowerDiagDtilde S_sub Y +
            4 * subsetPrimePowerSelfCollisionXself S_sub Y +
            interiorPairedRemainderF c_lam c_half p T D0 Y := by
      change windowEnergyNormSq Y
          (fun X =>
            ∑ n ∈ S_sub, (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) = _
      linarith only [h_id_Ssub]
    rw [h_norm_all, h_norm_int] at hy_sum_le hy_int_le
    obtain ⟨hD_diff1, hD_diff2⟩ :=
      subsetPrimePowerDiagDtilde_young_split_tc062_aux hY2 T S_sub hS_sub hδ_pos
    have hB_eq : Finset.Icc 1 T \ S_sub = B_set := rfl
    rw [hB_eq] at hD_diff1 hD_diff2
    have h_strip_Y : windowEnergyNormSq Y f_strip ≤ C_strip * (Real.log Y) ^ 2 :=
      h_strip_bd hY2
    have h_tail_Y : subsetPrimePowerDiagDtilde B_set Y ≤ C_tail :=
      h_tail_bd hY2
    have h_tail_nn : 0 ≤ subsetPrimePowerDiagDtilde B_set Y :=
      subsetPrimePowerDiagDtilde_nonneg_tc062_aux hY2 B_set (Finset.sdiff_subset _ _)
    have h_strip_nn : 0 ≤ windowEnergyNormSq Y f_strip := by
      obtain ⟨hle_Y, _⟩ := uIcc_tau_props_tc062_aux hY2
      unfold windowEnergyNormSq windowPairing
      apply intervalIntegral.integral_nonneg hle_Y
      intro X hX
      exact div_nonneg (mul_self_nonneg _) (by rw [Set.mem_Icc] at hX; linarith only [hY2, hX.1])
    have hX_T_bds := h_self_bds.2.2 hY2 T
    have hX_T_nn : 0 ≤ inheritedPrimePowerSelfCollisionXself T Y := hX_T_bds.1
    have hX_T_le : inheritedPrimePowerSelfCollisionXself T Y ≤ C_self :=
      le_trans hX_T_bds.2.1 hX_T_bds.2.2
    have hX_Ssub_nn : 0 ≤ subsetPrimePowerSelfCollisionXself S_sub Y := by
      obtain ⟨hle_Y, _⟩ := uIcc_tau_props_tc062_aux hY2
      unfold subsetPrimePowerSelfCollisionXself
      apply Finset.sum_nonneg
      intro k hk
      have hk1 : 1 ≤ k := (Finset.mem_Icc.mp (hS_sub hk)).1
      have hw_nn :=
        ((finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.1.2.2.2
          k hk1).1
      have hk_nn : 0 ≤ logWeightedWindowKernel 2 Y k k := by
        unfold logWeightedWindowKernel
        apply intervalIntegral.integral_nonneg hle_Y
        intro X hX
        exact div_nonneg (div_nonneg (mul_self_nonneg _) (sq_nonneg _))
          (by rw [Set.mem_Icc] at hX; linarith only [hY2, hX.1])
      exact mul_nonneg hw_nn hk_nn
    have hX_Ssub_le : subsetPrimePowerSelfCollisionXself S_sub Y ≤ C_self := by
      refine le_trans ?_ hX_T_le
      unfold subsetPrimePowerSelfCollisionXself inheritedPrimePowerSelfCollisionXself
      obtain ⟨hle_Y, _⟩ := uIcc_tau_props_tc062_aux hY2
      apply Finset.sum_le_sum_of_subset_of_nonneg hS_sub
      intro k hk _
      have hk1 : 1 ≤ k := (Finset.mem_Icc.mp hk).1
      have hw_nn :=
        ((finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.1.2.2.2
          k hk1).1
      have hk_nn : 0 ≤ logWeightedWindowKernel 2 Y k k := by
        unfold logWeightedWindowKernel
        apply intervalIntegral.integral_nonneg hle_Y
        intro X hX
        exact div_nonneg (div_nonneg (mul_self_nonneg _) (sq_nonneg _))
          (by rw [Set.mem_Icc] at hX; linarith only [hY2, hX.1])
      exact mul_nonneg hw_nn hk_nn
    have hD_T_nn : 0 ≤ inheritedPrimePowerDiagDtilde T Y := hD_nn Y hY2
    have h_strip_term :
        (1 + 1 / δ) * windowEnergyNormSq Y f_strip ≤ 2 * C_strip * (Real.log Y) ^ 3 := by
      rw [h1_div_δ]
      have h1_log : 1 + Real.log Y ≤ 2 * Real.log Y := by linarith only [hlog_ge1]
      calc
        (1 + Real.log Y) * windowEnergyNormSq Y f_strip
          ≤ (2 * Real.log Y) * (C_strip * (Real.log Y) ^ 2) :=
            mul_le_mul h1_log h_strip_Y h_strip_nn
              (mul_nonneg (by norm_num) (le_of_lt hlog_pos))
        _ = 2 * C_strip * (Real.log Y) ^ 3 := by ring
    have h_tail_term :
        8 * (1 + 1 / δ) * subsetPrimePowerDiagDtilde B_set Y ≤
          16 * C_tail * (Real.log Y) ^ 3 := by
      rw [h1_div_δ]
      have h1_log : 8 * (1 + Real.log Y) ≤ 16 * Real.log Y := by linarith only [hlog_ge1]
      have hlog_le3 : Real.log Y ≤ (Real.log Y) ^ 3 := by
        have hsq : 1 ≤ (Real.log Y) ^ 2 := by
          simpa using pow_le_pow_left zero_le_one hlog_ge1 2
        calc
          Real.log Y = Real.log Y * 1 := (mul_one _).symm
          _ ≤ Real.log Y * (Real.log Y) ^ 2 :=
              mul_le_mul_of_nonneg_left hsq (le_of_lt hlog_pos)
          _ = (Real.log Y) ^ 3 := by ring
      calc
        8 * (1 + Real.log Y) * subsetPrimePowerDiagDtilde B_set Y
          ≤ (16 * Real.log Y) * C_tail :=
            mul_le_mul h1_log h_tail_Y h_tail_nn (by positivity)
        _ = 16 * C_tail * Real.log Y := by ring
        _ ≤ 16 * C_tail * (Real.log Y) ^ 3 :=
            mul_le_mul_of_nonneg_left hlog_le3 (by positivity)
    have h_d_fwd :
        4 * (1 + δ) * inheritedPrimePowerDiagDtilde T Y - 4 * subsetPrimePowerDiagDtilde S_sub Y ≤
          (12 / Real.log Y) * inheritedPrimePowerDiagDtilde T Y +
            8 * (1 + 1 / δ) * subsetPrimePowerDiagDtilde B_set Y := by
      have h1 :
          4 * (1 + δ) * inheritedPrimePowerDiagDtilde T Y - 4 * subsetPrimePowerDiagDtilde S_sub Y ≤
            8 * δ * inheritedPrimePowerDiagDtilde T Y +
              4 * (1 / δ) * subsetPrimePowerDiagDtilde B_set Y := by
        calc
          4 * (1 + δ) * inheritedPrimePowerDiagDtilde T Y - 4 * subsetPrimePowerDiagDtilde S_sub Y
            = 4 * (inheritedPrimePowerDiagDtilde T Y - subsetPrimePowerDiagDtilde S_sub Y) +
                4 * (δ * inheritedPrimePowerDiagDtilde T Y) := by ring
          _ ≤ 4 * (δ * inheritedPrimePowerDiagDtilde T Y +
                (1 / δ) * subsetPrimePowerDiagDtilde B_set Y) +
                4 * (δ * inheritedPrimePowerDiagDtilde T Y) :=
              add_le_add_right (mul_le_mul_of_nonneg_left hD_diff1 (by norm_num)) _
          _ = 8 * δ * inheritedPrimePowerDiagDtilde T Y +
                4 * (1 / δ) * subsetPrimePowerDiagDtilde B_set Y := by ring
      have h8_12 : 8 * δ ≤ 12 / Real.log Y := by
        change 8 * (1 / Real.log Y) ≤ 12 / Real.log Y
        rw [show 8 * (1 / Real.log Y) = 8 / Real.log Y by ring]
        exact div_le_div_of_nonneg_right (by norm_num) (le_of_lt hlog_pos)
      have h8_le := mul_le_mul_of_nonneg_right h8_12 hD_T_nn
      have h4_8 :
          4 * (1 / δ) * subsetPrimePowerDiagDtilde B_set Y ≤
            8 * (1 + 1 / δ) * subsetPrimePowerDiagDtilde B_set Y := by
        have h_nn_inv : 0 ≤ 1 / δ := by positivity
        exact mul_le_mul_of_nonneg_right (by linarith only [h_nn_inv]) h_tail_nn
      exact le_trans h1 (add_le_add h8_le h4_8)
    have h_d_rev :
        4 * (1 + δ) * subsetPrimePowerDiagDtilde S_sub Y - 4 * inheritedPrimePowerDiagDtilde T Y ≤
          (12 / Real.log Y) * inheritedPrimePowerDiagDtilde T Y +
            8 * (1 + 1 / δ) * subsetPrimePowerDiagDtilde B_set Y := by
      have h_coeff_D : 4 * ((1 + δ) * (1 + δ) - 1) ≤ 12 * δ := by
        have hsq_d : δ * δ ≤ δ * 1 := mul_le_mul_of_nonneg_left hδ_le1 (le_of_lt hδ_pos)
        linarith only [hsq_d, show 4 * ((1 + δ) * (1 + δ) - 1) = 8 * δ + 4 * (δ * δ) by ring]
      have h12_eq : 12 * δ = 12 / Real.log Y := by change 12 * (1 / Real.log Y) = _; ring
      have h_D_le :
          4 * ((1 + δ) * (1 + δ) - 1) * inheritedPrimePowerDiagDtilde T Y ≤
            (12 / Real.log Y) * inheritedPrimePowerDiagDtilde T Y := by
        rw [← h12_eq]
        exact mul_le_mul_of_nonneg_right h_coeff_D hD_T_nn
      have h_B_le :
          4 * (1 + δ) * (1 + 1 / δ) * subsetPrimePowerDiagDtilde B_set Y ≤
            8 * (1 + 1 / δ) * subsetPrimePowerDiagDtilde B_set Y := by
        have h_1d : 4 * (1 + δ) ≤ 8 := by linarith only [hδ_le1]
        exact mul_le_mul_of_nonneg_right
          (mul_le_mul_of_nonneg_right h_1d (by positivity)) h_tail_nn
      calc
        4 * (1 + δ) * subsetPrimePowerDiagDtilde S_sub Y - 4 * inheritedPrimePowerDiagDtilde T Y
          = 4 * (1 + δ) * (subsetPrimePowerDiagDtilde S_sub Y - inheritedPrimePowerDiagDtilde T Y) +
              4 * δ * inheritedPrimePowerDiagDtilde T Y := by ring
        _ ≤ 4 * (1 + δ) *
              (δ * inheritedPrimePowerDiagDtilde T Y +
                (1 + 1 / δ) * subsetPrimePowerDiagDtilde B_set Y) +
              4 * δ * inheritedPrimePowerDiagDtilde T Y :=
            add_le_add_right (mul_le_mul_of_nonneg_left hD_diff2 (by positivity)) _
        _ = 4 * ((1 + δ) * (1 + δ) - 1) * inheritedPrimePowerDiagDtilde T Y +
              4 * (1 + δ) * (1 + 1 / δ) * subsetPrimePowerDiagDtilde B_set Y := by ring
        _ ≤ (12 / Real.log Y) * inheritedPrimePowerDiagDtilde T Y +
              8 * (1 + 1 / δ) * subsetPrimePowerDiagDtilde B_set Y := add_le_add h_D_le h_B_le
    have h_1d8 : 4 * (1 + δ) ≤ 8 := by linarith only [hδ_le1]
    have h_x_fwd :
        4 * (1 + δ) * inheritedPrimePowerSelfCollisionXself T Y ≤
          8 * C_self * (Real.log Y) ^ 3 := by
      calc
        4 * (1 + δ) * inheritedPrimePowerSelfCollisionXself T Y
          ≤ 8 * C_self :=
            mul_le_mul h_1d8 hX_T_le hX_T_nn (by norm_num)
        _ = 8 * C_self * 1 := by ring
        _ ≤ 8 * C_self * (Real.log Y) ^ 3 :=
            mul_le_mul_of_nonneg_left h_log3_ge1 (mul_nonneg (by norm_num) hCself_nn)
    have h_x_rev :
        4 * (1 + δ) * subsetPrimePowerSelfCollisionXself S_sub Y ≤
          8 * C_self * (Real.log Y) ^ 3 := by
      calc
        4 * (1 + δ) * subsetPrimePowerSelfCollisionXself S_sub Y
          ≤ 8 * C_self :=
            mul_le_mul h_1d8 hX_Ssub_le hX_Ssub_nn (by norm_num)
        _ = 8 * C_self * 1 := by ring
        _ ≤ 8 * C_self * (Real.log Y) ^ 3 :=
            mul_le_mul_of_nonneg_left h_log3_ge1 (mul_nonneg (by norm_num) hCself_nn)
    have h_dist1 :
        (1 + δ) *
            (4 * inheritedPrimePowerDiagDtilde T Y +
              4 * inheritedPrimePowerSelfCollisionXself T Y +
              truncatedSignedRemainderF c_lam c_half T D0 Y) =
          4 * (1 + δ) * inheritedPrimePowerDiagDtilde T Y +
            4 * (1 + δ) * inheritedPrimePowerSelfCollisionXself T Y +
            (1 + δ) * truncatedSignedRemainderF c_lam c_half T D0 Y := by ring
    have h_dist2 :
        (1 + δ) *
            (4 * subsetPrimePowerDiagDtilde S_sub Y +
              4 * subsetPrimePowerSelfCollisionXself S_sub Y +
              interiorPairedRemainderF c_lam c_half p T D0 Y) =
          4 * (1 + δ) * subsetPrimePowerDiagDtilde S_sub Y +
            4 * (1 + δ) * subsetPrimePowerSelfCollisionXself S_sub Y +
            (1 + δ) * interiorPairedRemainderF c_lam c_half p T D0 Y := by ring
    have h_dist_err :
        (8 * C_self + 2 * C_strip + 16 * C_tail) * (Real.log Y) ^ 3 =
          8 * C_self * (Real.log Y) ^ 3 +
            2 * C_strip * (Real.log Y) ^ 3 +
            16 * C_tail * (Real.log Y) ^ 3 := by ring
    rw [h_dist1] at hy_int_le
    rw [h_dist2] at hy_sum_le
    change interiorPairedRemainderF c_lam c_half p T D0 Y ≤
        (1 + δ) * truncatedSignedRemainderF c_lam c_half T D0 Y +
          (12 / Real.log Y) * inheritedPrimePowerDiagDtilde T Y +
          (8 * C_self + 2 * C_strip + 16 * C_tail) * (Real.log Y) ^ 3 ∧
      truncatedSignedRemainderF c_lam c_half T D0 Y ≤
        (1 + δ) * interiorPairedRemainderF c_lam c_half p T D0 Y +
          (12 / Real.log Y) * inheritedPrimePowerDiagDtilde T Y +
          (8 * C_self + 2 * C_strip + 16 * C_tail) * (Real.log Y) ^ 3
    rw [h_dist_err]
    exact ⟨by linarith only [hy_int_le, hX_Ssub_nn, h_x_fwd, h_d_fwd, h_tail_term, h_strip_term],
      by linarith only [hy_sum_le, hX_T_nn, h_x_rev, h_d_rev, h_tail_term, h_strip_term]⟩
  exact ⟨mixedCovarianceClosure_of_log_perturbation_tc062_aux hCerr_nn hD_nn
      (fun Y hY => (h_both Y hY).1),
    mixedCovarianceClosure_of_log_perturbation_tc062_aux hCerr_nn hD_nn
      (fun Y hY => (h_both Y hY).2)⟩

/-- **Theorem 7 (`TASK-TC-062` §6 Stage C & §8, Cutoff-Strip Energy and Omitted `Dtilde` Tail Bounds, Full Chain of `MixedCovarianceClosureHypothesis` Equivalences onto `canonicalInteriorPairedRemainderF`, and Conditional Route D Closure Transfer)**:
    For every prime `p` (`hp : p.Prime`):
    1. *Elementary `O_p((log Y)^2)` cutoff-strip energy bound & `O_p(1)` omitted `Dtilde` tail bound on the canonical schedule (`Y ≥ 2`)*:
       Both `windowEnergyNormSq Y (∑_{k ∈ uncoveredCutoffStripStations p T} λ(k) ψ_{Y, k}) ≤ C_strip * (Real.log Y)^2`
       and `subsetPrimePowerDiagDtilde (uncoveredCutoffStripStations p T) Y ≤ C_tail` hold uniformly across all `Y ≥ 2`;
    2. *Full chain of two-way equivalences (`∀ c_lam c_half` and at `(actualSelbergConstantCLam, actualSquarePoleConstantCHalf)`)*:
       `MixedCovarianceClosureHypothesis (canonicalSignedMixedCovarianceJ c_lam c_half) canonicalPrimePowerDiagDtilde`
       `↔ MixedCovarianceClosureHypothesis (canonicalSignedRemainderF c_lam c_half) canonicalPrimePowerDiagDtilde`
       `↔ MixedCovarianceClosureHypothesis (canonicalTruncatedSignedRemainderF c_lam c_half) canonicalPrimePowerDiagDtilde`
       `↔ MixedCovarianceClosureHypothesis (canonicalInteriorPairedRemainderF c_lam c_half p) canonicalPrimePowerDiagDtilde`;
    3. *Conditional Route D closure transfer at `(actualSelbergConstantCLam, actualSquarePoleConstantCHalf)`*:
       Composes the interior `p`-pair equivalence with `mixed_covariance_hypothesis_route_d_closure_transfer_tc061`
       (automatically discharging nonnegativity and the `(8, 2, 2)` window energy bound on `canonicalLiouvilleEnergyE`)
       to deduce `∀ ε > 0, ∃ C_tot ≥ 0, ∀ Y ≥ 1, canonicalLiouvilleEnergyE Y ≤ C_tot * Y ^ ε`. -/
theorem interior_prime_pair_closure_equivalence_and_route_d_transfer_tc062
    {p : ℕ} (hp : p.Prime) :
    (∀ (c_lam c_half : ℝ),
      ∃ C_strip C_tail : ℝ, 0 ≤ C_strip ∧ 0 ≤ C_tail ∧
        ∀ {Y : ℝ}, 2 ≤ Y →
          let T := canonicalCutoffT Y
          let D0 := Nat.floor (Real.log Y)
          windowEnergyNormSq Y
              (fun X =>
                ∑ k ∈ uncoveredCutoffStripStations p T,
                  (liouvilleLambda k : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 k X) ≤
              C_strip * (Real.log Y) ^ 2 ∧
            subsetPrimePowerDiagDtilde (uncoveredCutoffStripStations p T) Y ≤ C_tail) ∧
    ((∀ (c_lam c_half : ℝ),
        (MixedCovarianceClosureHypothesis
            (canonicalSignedMixedCovarianceJ c_lam c_half) canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalInteriorPairedRemainderF c_lam c_half p) canonicalPrimePowerDiagDtilde) ∧
        (MixedCovarianceClosureHypothesis
            (canonicalSignedRemainderF c_lam c_half) canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalInteriorPairedRemainderF c_lam c_half p) canonicalPrimePowerDiagDtilde) ∧
        (MixedCovarianceClosureHypothesis
            (canonicalTruncatedSignedRemainderF c_lam c_half) canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalInteriorPairedRemainderF c_lam c_half p) canonicalPrimePowerDiagDtilde)) ∧
      (MixedCovarianceClosureHypothesis
          (canonicalSignedRemainderF actualSelbergConstantCLam actualSquarePoleConstantCHalf)
          canonicalPrimePowerDiagDtilde ↔
        MixedCovarianceClosureHypothesis
          (canonicalInteriorPairedRemainderF
            actualSelbergConstantCLam actualSquarePoleConstantCHalf p)
          canonicalPrimePowerDiagDtilde)) ∧
    (∀ {M_lin : ℝ},
      0 ≤ M_lin →
      (∀ Z : ℝ, 1 ≤ Z → canonicalLiouvilleEnergyE Z ≤ M_lin * Z) →
      MixedCovarianceClosureHypothesis
        (canonicalInteriorPairedRemainderF
          actualSelbergConstantCLam actualSquarePoleConstantCHalf p)
        canonicalPrimePowerDiagDtilde →
      (∀ ε : ℝ, 0 < ε →
        ∃ zeta2_eps C_cut Y_diag a_known B_drift κ_d : ℝ,
          0 ≤ zeta2_eps ∧ 0 ≤ C_cut ∧ Real.exp 1 ≤ Y_diag ∧
            0 ≤ a_known ∧ 0 ≤ B_drift ∧ 0 < κ_d ∧
            (∀ Y : ℝ, 1 ≤ Y →
              (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
                (Real.log (pk.1 : ℝ)) ^ 2 / (primePowerScale pk) ^ (1 + ε)) ≤ zeta2_eps) ∧
            (∀ Y : ℝ, Y_diag ≤ Y →
              canonicalPrimePowerDiagDtilde Y ≤
                (2 / (Real.log Y) ^ 2) *
                  (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
                    primePowerDiagWeight pk *
                      monotoneScaleEnvelope canonicalLiouvilleEnergyE (Y / primePowerScale pk)) +
                  C_cut) ∧
            (∀ R Y : ℝ, Y_diag ≤ Y → Y ≤ R →
              windowEnergyNormSq Y
                  (knownCompensatedD2Part
                    actualSelbergConstantCLam actualSquarePoleConstantCHalf
                    (canonicalCutoffT Y) (Nat.floor (Real.log Y))) ≤
                a_known * Y ^ (ε / 4) +
                  (B_drift / (Real.log Y) ^ κ_d) *
                    normalizedScaleSupremum canonicalLiouvilleEnergyE ε R * Y ^ ε)) →
      ∀ ε : ℝ, 0 < ε →
        ∃ C_tot : ℝ, 0 ≤ C_tot ∧ ∀ Y : ℝ, 1 ≤ Y → canonicalLiouvilleEnergyE Y ≤ C_tot * Y ^ ε) := by
  have h_part1 :
      ∀ (c_lam c_half : ℝ),
        ∃ C_strip C_tail : ℝ, 0 ≤ C_strip ∧ 0 ≤ C_tail ∧
          ∀ {Y : ℝ}, 2 ≤ Y →
            let T := canonicalCutoffT Y
            let D0 := Nat.floor (Real.log Y)
            windowEnergyNormSq Y
                (fun X =>
                  ∑ k ∈ uncoveredCutoffStripStations p T,
                    (liouvilleLambda k : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 k X) ≤
                C_strip * (Real.log Y) ^ 2 ∧
              subsetPrimePowerDiagDtilde (uncoveredCutoffStripStations p T) Y ≤ C_tail := by
    intro c_lam c_half
    obtain ⟨C_strip, hCs_nn, h_strip_bd⟩ :=
      uncovered_strip_windowEnergy_bound_tc062_aux hp c_lam c_half
    obtain ⟨C_tail, hCt_nn, h_tail_bd⟩ := uncovered_strip_diagDtilde_bound_tc062_aux hp
    exact ⟨C_strip, C_tail, hCs_nn, hCt_nn, fun hY2 => ⟨h_strip_bd hY2, h_tail_bd hY2⟩⟩
  have h_part2_all :
      ∀ (c_lam c_half : ℝ),
        (MixedCovarianceClosureHypothesis
            (canonicalSignedMixedCovarianceJ c_lam c_half) canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalInteriorPairedRemainderF c_lam c_half p) canonicalPrimePowerDiagDtilde) ∧
        (MixedCovarianceClosureHypothesis
            (canonicalSignedRemainderF c_lam c_half) canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalInteriorPairedRemainderF c_lam c_half p) canonicalPrimePowerDiagDtilde) ∧
        (MixedCovarianceClosureHypothesis
            (canonicalTruncatedSignedRemainderF c_lam c_half) canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalInteriorPairedRemainderF c_lam c_half p) canonicalPrimePowerDiagDtilde) := by
    intro c_lam c_half
    have h_JF :=
      (signed_remainder_equivalence_and_sufficient_core_relaxation_tc061r).2.1.2 c_lam c_half
    have h_FT :=
      (spillover_fringe_reindexing_and_mixed_covariance_reduction_tc062).2.2.2.2.1 c_lam c_half
    have h_TI := trunc_iff_interior_closure_hypothesis_tc062_aux hp c_lam c_half
    exact ⟨h_JF.trans (h_FT.trans h_TI), h_FT.trans h_TI, h_TI⟩
  refine ⟨h_part1,
    ⟨h_part2_all,
      (h_part2_all actualSelbergConstantCLam actualSquarePoleConstantCHalf).2.1⟩,
    ?_⟩
  intro M_lin hM_nn hE_lin h_int_hyp h_route_d_inputs
  have h_J_hyp :
      MixedCovarianceClosureHypothesis
        (canonicalSignedMixedCovarianceJ
          actualSelbergConstantCLam actualSquarePoleConstantCHalf)
        canonicalPrimePowerDiagDtilde :=
    ((h_part2_all actualSelbergConstantCLam actualSquarePoleConstantCHalf).1).mpr h_int_hyp
  have hE_nn : ∀ Z : ℝ, 1 ≤ Z → 0 ≤ canonicalLiouvilleEnergyE Z :=
    fun Z hZ1 =>
      (repaired_weighted_diagonal_closure_and_actual_observable_tc059r).2.2.2.1 Z
        (lt_of_lt_of_le zero_lt_one hZ1)
  have h_tc061_transfer :=
    (mixed_covariance_hypothesis_route_d_closure_transfer_tc061).2.2.1
      (E := canonicalLiouvilleEnergyE)
      (D_tilde := canonicalPrimePowerDiagDtilde)
      (J := canonicalSignedMixedCovarianceJ
        actualSelbergConstantCLam actualSquarePoleConstantCHalf)
      (A_sq := fun Y =>
        windowEnergyNormSq Y
          (knownCompensatedD2Part
            actualSelbergConstantCLam actualSquarePoleConstantCHalf
            (canonicalCutoffT Y) (Nat.floor (Real.log Y))))
      hE_nn hM_nn hE_lin h_J_hyp
  apply h_tc061_transfer
  intro ε hε
  obtain ⟨zeta2_eps, C_cut, Y_diag, a_known, B_drift, κ_d,
    hz, hCc, hYd, hak, hBd, hkd, h_z_mass, h_D_bd, h_A_bd⟩ := h_route_d_inputs ε hε
  refine ⟨zeta2_eps, C_cut, Y_diag, a_known, B_drift, κ_d,
    hz, hCc, hYd, hak, hBd, hkd, h_z_mass, h_D_bd, h_A_bd, ?_⟩
  intro Y hYYd
  have he_ge2 : (2 : ℝ) ≤ Real.exp 1 := by linarith [Real.add_one_le_exp (1 : ℝ)]
  have hY2 : 2 ≤ Y := le_trans he_ge2 (le_trans hYd hYYd)
  unfold canonicalLiouvilleEnergyE
  exact ((mixed_covariance_identity_and_theta_energy_bound_tc061).2.2.2.2.2 hY2
    actualSelbergConstantCLam actualSquarePoleConstantCHalf).2

/-! ### Section 7: Two-Sided Interior Anchor-Diagonal Bound & Off-Diagonal Equivalence (`TASK-TC-062R` §3, §7A, §7D) -/

/-- Aggregate interior `p`-adic anchor diagonal sum `Σ_{p, diag}^{int}(Y)` over
    `m ∈ primeInteriorTruncatedAnchors p T` (`TASK-TC-062R` §3 & §7A). -/
noncomputable def interiorAnchorDiagSigma (c_lam c_half : ℝ) (p T D0 : ℕ) (Y : ℝ) : ℝ :=
  ∑ m ∈ primeInteriorTruncatedAnchors p T,
    (completeSignedKernelHcal c_lam c_half T D0 Y m m -
      completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
      completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
      completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m))

/-- Distinct-anchor (`m ≠ n`) interior `p`-adic off-diagonal sum `Σ_{p, off}^{int}(Y)` over
    `primeInteriorTruncatedAnchors p T` (`TASK-TC-062R` §3 & §7D). -/
noncomputable def interiorAnchorOffDiagSigma (c_lam c_half : ℝ) (p T D0 : ℕ) (Y : ℝ) : ℝ :=
  ∑ m ∈ primeInteriorTruncatedAnchors p T,
    ∑ n ∈ (primeInteriorTruncatedAnchors p T).erase m,
      (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
        (completeSignedKernelHcal c_lam c_half T D0 Y m n -
          completeSignedKernelHcal c_lam c_half T D0 Y (p * m) n -
          completeSignedKernelHcal c_lam c_half T D0 Y m (p * n) +
          completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * n))

/-- Canonical-schedule (`T = canonicalCutoffT Y`, `D0 = ⌊log Y⌋`) interior anchor diagonal sum. -/
noncomputable def canonicalInteriorDiagSigma (c_lam c_half : ℝ) (p : ℕ) (Y : ℝ) : ℝ :=
  interiorAnchorDiagSigma c_lam c_half p (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y

/-- Canonical-schedule (`T = canonicalCutoffT Y`, `D0 = ⌊log Y⌋`) distinct-anchor interior
    off-diagonal sum (`TC062-OBL-INTERIOR-PRIME-PAIR-OFFDIAG` observable). -/
noncomputable def canonicalInteriorOffDiagSigma (c_lam c_half : ℝ) (p : ℕ) (Y : ℝ) : ℝ :=
  interiorAnchorOffDiagSigma c_lam c_half p (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y

private theorem interiorPairedRemainderF_diag_offdiag_split_tc062r_aux
    (c_lam c_half : ℝ) (p T D0 : ℕ) (Y : ℝ) :
    interiorPairedRemainderF c_lam c_half p T D0 Y =
        interiorAnchorDiagSigma c_lam c_half p T D0 Y +
          interiorAnchorOffDiagSigma c_lam c_half p T D0 Y ∧
      interiorAnchorOffDiagSigma c_lam c_half p T D0 Y =
        ∑ mn ∈ (primeInteriorTruncatedAnchors p T ×ˢ primeInteriorTruncatedAnchors p T).filter
            (fun mn => mn.1 ≠ mn.2),
          (liouvilleLambda mn.1 : ℝ) * (liouvilleLambda mn.2 : ℝ) *
            (completeSignedKernelHcal c_lam c_half T D0 Y mn.1 mn.2 -
              completeSignedKernelHcal c_lam c_half T D0 Y (p * mn.1) mn.2 -
              completeSignedKernelHcal c_lam c_half T D0 Y mn.1 (p * mn.2) +
              completeSignedKernelHcal c_lam c_half T D0 Y (p * mn.1) (p * mn.2)) := by
  let S := primeInteriorTruncatedAnchors p T
  let term : ℕ → ℕ → ℝ := fun m n =>
    (liouvilleLambda m : ℝ) * (liouvilleLambda n : ℝ) *
      (completeSignedKernelHcal c_lam c_half T D0 Y m n -
        completeSignedKernelHcal c_lam c_half T D0 Y (p * m) n -
        completeSignedKernelHcal c_lam c_half T D0 Y m (p * n) +
        completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * n))
  constructor
  · unfold interiorPairedRemainderF interiorAnchorDiagSigma interiorAnchorOffDiagSigma
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro m hm
    have hm1 : 1 ≤ m :=
      (Finset.mem_Icc.mp (Finset.mem_filter.mp (Finset.mem_filter.mp hm).1).1).1
    rw [← Finset.add_sum_erase _ _ hm, liouvilleLambda_sq_eq_one_tc062_aux hm1, one_mul]
  · unfold interiorAnchorOffDiagSigma
    change (∑ m ∈ S, ∑ n ∈ S.erase m, term m n) =
      ∑ mn ∈ (S ×ˢ S).filter (fun mn => mn.1 ≠ mn.2), term mn.1 mn.2
    rw [Finset.sum_filter, Finset.sum_product]
    apply Finset.sum_congr rfl
    intro m hm
    symm
    rw [← Finset.add_sum_erase _ _ hm, if_neg (not_not.mpr rfl), zero_add]
    apply Finset.sum_congr rfl
    intro n hn
    exact if_pos (Finset.mem_erase.mp hn).1.symm

private theorem commonPrimePowerLogSq_prime_mul_identities_tc062r_aux
    {p m : ℕ} (hp : p.Prime) (hm1 : 1 ≤ m) :
    commonPrimePowerLogSq m (p * m) = commonPrimePowerLogSq m m ∧
      commonPrimePowerLogSq (p * m) (p * m) =
        commonPrimePowerLogSq m m + (Real.log (p : ℝ)) ^ 2 := by
  have h_mp : commonPrimePowerLogSq m (p * m) = commonPrimePowerLogSq m m := by
    unfold commonPrimePowerLogSq
    have h_min : min m (p * m) = min m m := by
      rw [min_self, min_eq_left (Nat.le_mul_of_pos_left m hp.pos)]
    have h_gcd : Nat.gcd m (p * m) = Nat.gcd m m := by
      rw [Nat.gcd_self, Nat.gcd_eq_left (dvd_mul_left m p)]
    rw [h_min, h_gcd]
  refine ⟨h_mp, ?_⟩
  let U := insert p (insert p (m.primeFactors ∪ m.primeFactors))
  have hU_prime : ∀ r ∈ U, r.Prime := by
    intro r hr
    simp only [U, Finset.mem_insert, Finset.mem_union] at hr
    rcases hr with rfl | rfl | hrm | hrm
    · exact hp
    · exact hp
    · exact Nat.prime_of_mem_primeFactors hrm
    · exact Nat.prime_of_mem_primeFactors hrm
  have hpm1 : 1 ≤ p * m := Nat.mul_pos hp.pos hm1
  have h_mm :
      commonPrimePowerLogSq m m =
        ∑ r ∈ U, ((min (m.factorization r) (m.factorization r) : ℕ) : ℝ) *
          (Real.log (r : ℝ)) ^ 2 := by
    apply commonPrimePowerLogSq_eq_sum_min_factorization_tc062_aux hm1 hm1 U hU_prime
    simpa only [pow_zero, one_mul] using
      primeFactors_gcd_subset_insert_two_tc062_aux hp hp hm1 hm1 0 0 0 0
  have h_pmpm :
      commonPrimePowerLogSq (p * m) (p * m) =
        ∑ r ∈ U, ((min ((p * m).factorization r) ((p * m).factorization r) : ℕ) : ℝ) *
          (Real.log (r : ℝ)) ^ 2 := by
    apply commonPrimePowerLogSq_eq_sum_min_factorization_tc062_aux hpm1 hpm1 U hU_prime
    simpa only [pow_one, pow_zero, mul_one] using
      primeFactors_gcd_subset_insert_two_tc062_aux hp hp hm1 hm1 1 0 1 0
  have hpU : p ∈ U := Finset.mem_insert_self p _
  rw [h_pmpm, h_mm, ← Finset.add_sum_erase _ _ hpU,
    ← Finset.add_sum_erase U
      (fun r => ((min (m.factorization r) (m.factorization r) : ℕ) : ℝ) * (Real.log (r : ℝ)) ^ 2)
      hpU]
  have h_er_eq :
      (∑ r ∈ U.erase p,
          ((min ((p * m).factorization r) ((p * m).factorization r) : ℕ) : ℝ) *
            (Real.log (r : ℝ)) ^ 2) =
        ∑ r ∈ U.erase p,
          ((min (m.factorization r) (m.factorization r) : ℕ) : ℝ) *
            (Real.log (r : ℝ)) ^ 2 := by
    apply Finset.sum_congr rfl
    intro r hr
    have hrp : p ≠ r := (Finset.mem_erase.mp hr).1.symm
    rw [factorization_prime_mul_of_ne_tc062_aux hp hrp hm1]
  rw [h_er_eq, min_self, min_self, factorization_prime_mul_self_tc062_aux hp hm1]
  push_cast
  ring

private theorem anchor_diagonal_hcal_identities_tc062r_aux
    {p : ℕ} (hp : p.Prime) {Y : ℝ} (hY2 : 2 ≤ Y) {T m : ℕ}
    (hm1 : 1 ≤ m) (hpmT : p * m ≤ T) (D0 : ℕ) (c_lam c_half : ℝ) :
    (completeSignedKernelHcal c_lam c_half T D0 Y m m -
        completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
        completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
        completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m) =
      windowEnergyNormSq Y
          (fun X =>
            adjustedStationProfilePsi c_lam c_half T D0 m X -
              adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) -
        4 * (Real.log (m : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y m m -
        4 * (Real.log ((p * m : ℕ) : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y (p * m) (p * m) +
        8 * commonPrimePowerLogSq m m * logWeightedWindowKernel 2 Y m (p * m)) ∧
      (completeSignedKernelHcal c_lam c_half T D0 Y m m -
          completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
          completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
          completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m) =
        windowEnergyNormSq Y
            (fun X =>
              adjustedStationProfilePsi c_lam c_half T D0 m X -
                adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) -
          4 * (Real.log (p : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y (p * m) (p * m) -
          4 * offDiagPrimePowerWeight m m * logWeightedWindowKernel 2 Y m m -
          4 * offDiagPrimePowerWeight (p * m) (p * m) *
            logWeightedWindowKernel 2 Y (p * m) (p * m) -
          4 * commonPrimePowerLogSq m m *
            (logWeightedWindowKernel 2 Y m m -
              2 * logWeightedWindowKernel 2 Y m (p * m) +
              logWeightedWindowKernel 2 Y (p * m) (p * m))) := by
  have hp2 : 2 ≤ p := hp.two_le
  have hpm1 : 1 ≤ p * m := Nat.mul_pos hp.pos hm1
  have hT1 : 1 ≤ T := le_trans hpm1 hpmT
  have h2m_le : 2 * m ≤ p * m := Nat.mul_le_mul_right m hp2
  have hpm_ne : m ≠ p * m := by omega
  have h_not_mem : m ∉ ({p * m} : Finset ℕ) := Finset.not_mem_singleton.mpr hpm_ne
  have h_pair_sub : ({m, p * m} : Finset ℕ) ⊆ Finset.Icc 1 T := by
    intro x hx
    simp only [Finset.mem_insert, Finset.mem_singleton] at hx
    rw [Finset.mem_Icc]
    rcases hx with hx_eq | hx_eq
    · rw [hx_eq]; exact ⟨hm1, le_trans (Nat.le_mul_of_pos_left m hp.pos) hpmT⟩
    · rw [hx_eq]; exact ⟨hpm1, hpmT⟩
  have h_pair_id :=
    subset_hcal_bilinear_eq_windowNorm_sub_tc062_aux hY2 hT1 D0 c_lam c_half {m, p * m} h_pair_sub
  have h_lam_sq := liouvilleLambda_sq_eq_one_tc062_aux hm1
  have h_lam_pm := liouvilleLambda_prime_mul_real_tc062_aux hp hm1
  have h_lhs :
      (∑ u ∈ ({m, p * m} : Finset ℕ), ∑ v ∈ ({m, p * m} : Finset ℕ),
          (liouvilleLambda u : ℝ) * (liouvilleLambda v : ℝ) *
            completeSignedKernelHcal c_lam c_half T D0 Y u v) =
        completeSignedKernelHcal c_lam c_half T D0 Y m m -
          completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
          completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
          completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m) := by
    simp only [Finset.sum_insert h_not_mem, Finset.sum_singleton]
    rw [h_lam_pm]
    calc
      (liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ) *
            completeSignedKernelHcal c_lam c_half T D0 Y m m +
          (liouvilleLambda m : ℝ) * -(liouvilleLambda m : ℝ) *
            completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
          (-(liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ) *
              completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m +
            -(liouvilleLambda m : ℝ) * -(liouvilleLambda m : ℝ) *
              completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m))
        = ((liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ)) *
            (completeSignedKernelHcal c_lam c_half T D0 Y m m -
              completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
              completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
              completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m)) := by ring
      _ = completeSignedKernelHcal c_lam c_half T D0 Y m m -
            completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
            completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
            completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m) := by
          rw [h_lam_sq, one_mul]
  have h_norm_eq :
      windowEnergyNormSq Y
          (fun X =>
            ∑ n ∈ ({m, p * m} : Finset ℕ),
              (liouvilleLambda n : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 n X) =
        windowEnergyNormSq Y
          (fun X =>
            adjustedStationProfilePsi c_lam c_half T D0 m X -
              adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) := by
    unfold windowEnergyNormSq windowPairing
    apply intervalIntegral.integral_congr
    intro X _
    simp only [Finset.sum_insert h_not_mem, Finset.sum_singleton]
    rw [h_lam_pm]
    have h_sq_pt :
        ((liouvilleLambda m : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 m X +
            -(liouvilleLambda m : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) *
          ((liouvilleLambda m : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 m X +
            -(liouvilleLambda m : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) =
        (adjustedStationProfilePsi c_lam c_half T D0 m X -
            adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) *
          (adjustedStationProfilePsi c_lam c_half T D0 m X -
            adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) := by
      calc
        ((liouvilleLambda m : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 m X +
              -(liouvilleLambda m : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) *
            ((liouvilleLambda m : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 m X +
              -(liouvilleLambda m : ℝ) * adjustedStationProfilePsi c_lam c_half T D0 (p * m) X)
          = ((liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ)) *
              ((adjustedStationProfilePsi c_lam c_half T D0 m X -
                  adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) *
                (adjustedStationProfilePsi c_lam c_half T D0 m X -
                  adjustedStationProfilePsi c_lam c_half T D0 (p * m) X)) := by ring
        _ = (adjustedStationProfilePsi c_lam c_half T D0 m X -
                adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) *
              (adjustedStationProfilePsi c_lam c_half T D0 m X -
                adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) := by
            rw [h_lam_sq, one_mul]
    rw [h_sq_pt]
  obtain ⟨hc_mp, hc_pmpm⟩ := commonPrimePowerLogSq_prime_mul_identities_tc062r_aux hp hm1
  have hc_pm : commonPrimePowerLogSq (p * m) m = commonPrimePowerLogSq m m := by
    rw [commonPrimePowerLogSq_symm_tc062_aux, hc_mp]
  have hG_symm : logWeightedWindowKernel 2 Y (p * m) m = logWeightedWindowKernel 2 Y m (p * m) :=
    logWeightedWindowKernel_symm_tc062_aux 2 Y (p * m) m
  have h_dtilde :
      subsetPrimePowerDiagDtilde {m, p * m} Y =
        commonPrimePowerLogSq m m * logWeightedWindowKernel 2 Y m m -
          2 * commonPrimePowerLogSq m m * logWeightedWindowKernel 2 Y m (p * m) +
          (commonPrimePowerLogSq m m + (Real.log (p : ℝ)) ^ 2) *
            logWeightedWindowKernel 2 Y (p * m) (p * m) := by
    unfold subsetPrimePowerDiagDtilde
    simp only [Finset.sum_insert h_not_mem, Finset.sum_singleton]
    rw [h_lam_pm, hc_mp, hc_pm, hc_pmpm, hG_symm]
    calc
      (liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ) * commonPrimePowerLogSq m m *
            logWeightedWindowKernel 2 Y m m +
          (liouvilleLambda m : ℝ) * -(liouvilleLambda m : ℝ) * commonPrimePowerLogSq m m *
            logWeightedWindowKernel 2 Y m (p * m) +
          (-(liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ) * commonPrimePowerLogSq m m *
              logWeightedWindowKernel 2 Y m (p * m) +
            -(liouvilleLambda m : ℝ) * -(liouvilleLambda m : ℝ) *
              (commonPrimePowerLogSq m m + (Real.log (p : ℝ)) ^ 2) *
              logWeightedWindowKernel 2 Y (p * m) (p * m))
        = ((liouvilleLambda m : ℝ) * (liouvilleLambda m : ℝ)) *
            (commonPrimePowerLogSq m m * logWeightedWindowKernel 2 Y m m -
              2 * commonPrimePowerLogSq m m * logWeightedWindowKernel 2 Y m (p * m) +
              (commonPrimePowerLogSq m m + (Real.log (p : ℝ)) ^ 2) *
                logWeightedWindowKernel 2 Y (p * m) (p * m)) := by ring
      _ = commonPrimePowerLogSq m m * logWeightedWindowKernel 2 Y m m -
            2 * commonPrimePowerLogSq m m * logWeightedWindowKernel 2 Y m (p * m) +
            (commonPrimePowerLogSq m m + (Real.log (p : ℝ)) ^ 2) *
              logWeightedWindowKernel 2 Y (p * m) (p * m) := by rw [h_lam_sq, one_mul]
  have h_xself :
      subsetPrimePowerSelfCollisionXself {m, p * m} Y =
        offDiagPrimePowerWeight m m * logWeightedWindowKernel 2 Y m m +
          offDiagPrimePowerWeight (p * m) (p * m) * logWeightedWindowKernel 2 Y (p * m) (p * m) := by
    unfold subsetPrimePowerSelfCollisionXself
    simp only [Finset.sum_insert h_not_mem, Finset.sum_singleton]
  rw [h_lhs, h_norm_eq, h_dtilde, h_xself] at h_pair_id
  refine ⟨?_, ?_⟩
  · rw [h_pair_id]
    unfold offDiagPrimePowerWeight
    rw [hc_pmpm]
    ring
  · rw [h_pair_id]
    ring

private theorem interiorAnchorDiagSigma_lower_bound_tc062r_aux
    {p : ℕ} (hp : p.Prime) {Y : ℝ} (hY2 : 2 ≤ Y) {T : ℕ} (_hT : 1 ≤ T)
    (D0 : ℕ) (c_lam c_half : ℝ) :
    -744 * (RiemannScope.tau - 1) ≤
        -4 * (∑ n ∈ Finset.Icc 1 T,
          (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n) ∧
      -4 * (∑ n ∈ Finset.Icc 1 T,
          (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n) ≤
        interiorAnchorDiagSigma c_lam c_half p T D0 Y := by
  obtain ⟨hle, _⟩ := uIcc_tau_props_tc062_aux hY2
  have h_tc061 :=
    ((finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2.2.2 hY2 T).2.2
  have h_744 :
      -744 * (RiemannScope.tau - 1) ≤
        -4 * (∑ n ∈ Finset.Icc 1 T,
          (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n) := by
    linarith only [h_tc061]
  refine ⟨h_744, ?_⟩
  obtain ⟨h_cov_sub, _, _, h_cov_sum⟩ := coveredInteriorStations_props_tc062_aux hp T
  have h_ker_nn : ∀ a b : ℕ, 0 ≤ logWeightedWindowKernel 2 Y a b := by
    intro a b
    unfold logWeightedWindowKernel
    apply intervalIntegral.integral_nonneg hle
    intro X hX
    have hX_pos : 0 < X := by rw [Set.mem_Icc] at hX; linarith only [hY2, hX.1]
    have ha_nn : 0 ≤ gaussianTermPhi a X := by unfold gaussianTermPhi; positivity
    have hb_nn : 0 ≤ gaussianTermPhi b X := by unfold gaussianTermPhi; positivity
    exact div_nonneg (div_nonneg (mul_nonneg ha_nn hb_nn) (sq_nonneg _)) (le_of_lt hX_pos)
  have h_each_ge :
      ∀ m ∈ primeInteriorTruncatedAnchors p T,
        -4 * ((Real.log (m : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y m m +
            (Real.log ((p * m : ℕ) : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y (p * m) (p * m)) ≤
          completeSignedKernelHcal c_lam c_half T D0 Y m m -
            completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
            completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
            completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m) := by
    intro m hm
    have hm_f := Finset.mem_filter.mp hm
    have hm1 : 1 ≤ m := (Finset.mem_Icc.mp (Finset.mem_filter.mp hm_f.1).1).1
    have hpmT : p * m ≤ T := hm_f.2
    have h_id := (anchor_diagonal_hcal_identities_tc062r_aux hp hY2 hm1 hpmT D0 c_lam c_half).1
    rw [h_id]
    have h_wn_nn :
        0 ≤ windowEnergyNormSq Y
          (fun X =>
            adjustedStationProfilePsi c_lam c_half T D0 m X -
              adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) := by
      unfold windowEnergyNormSq windowPairing
      apply intervalIntegral.integral_nonneg hle
      intro X hX
      exact div_nonneg (mul_self_nonneg _) (by rw [Set.mem_Icc] at hX; linarith only [hY2, hX.1])
    have hc_nn : 0 ≤ commonPrimePowerLogSq m m := by
      unfold commonPrimePowerLogSq
      exact Finset.sum_nonneg (fun _ _ => sq_nonneg _)
    have h8_nn : 0 ≤ 8 * commonPrimePowerLogSq m m * logWeightedWindowKernel 2 Y m (p * m) :=
      mul_nonneg (mul_nonneg (by norm_num) hc_nn) (h_ker_nn m (p * m))
    linarith only [h_wn_nn, h8_nn]
  have h_sum_ge :
      (∑ m ∈ primeInteriorTruncatedAnchors p T,
          (-4 * ((Real.log (m : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y m m +
            (Real.log ((p * m : ℕ) : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y (p * m) (p * m)))) ≤
        interiorAnchorDiagSigma c_lam c_half p T D0 Y := by
    unfold interiorAnchorDiagSigma
    exact Finset.sum_le_sum h_each_ge
  rw [← Finset.mul_sum] at h_sum_ge
  have h_cov_eq :=
    h_cov_sum (fun n => (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n)
  rw [← h_cov_eq] at h_sum_ge
  have h_cov_le :
      (∑ n ∈ coveredInteriorStations p T,
          (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n) ≤
        ∑ n ∈ Finset.Icc 1 T,
          (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n :=
    Finset.sum_le_sum_of_subset_of_nonneg h_cov_sub
      (fun n _ _ => mul_nonneg (sq_nonneg _) (h_ker_nn n n))
  linarith only [h_sum_ge, h_cov_le]

private theorem squarePoleDriftM_sharp_step_abs_le_tc062r_aux
    (c_half : ℝ) {d : ℕ} (hd1 : 1 ≤ d) :
    |squarePoleDriftM c_half d - squarePoleDriftM c_half (d - 1)| ≤
      (8 + |c_half|) * (1 + Real.log (d : ℝ)) / Real.sqrt (d : ℝ) := by
  by_cases hd_eq1 : d = 1
  · subst hd_eq1
    unfold squarePoleDriftM
    simp [Real.log_one]
  · have hd2 : 2 ≤ d := by omega
    have hd_ne : d ≠ 0 := by omega
    have hdm1_ne : d - 1 ≠ 0 := by omega
    have hd_pos : (0 : ℝ) < (d : ℝ) := by positivity
    have hsqrt_pos : 0 < Real.sqrt (d : ℝ) := Real.sqrt_pos.mpr hd_pos
    have hdm1_eq : ((d - 1 : ℕ) : ℝ) = (d : ℝ) - 1 := by
      rw [Nat.cast_sub hd1, Nat.cast_one]
    have h2_le_d : (2 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd2
    have hdm1_pos : (0 : ℝ) < (d : ℝ) - 1 := by linarith
    have hsqrt_m1_pos : 0 < Real.sqrt ((d : ℝ) - 1) := Real.sqrt_pos.mpr hdm1_pos
    have h_sqrt_diff_nn : 0 ≤ Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1) :=
      sub_nonneg.mpr (Real.sqrt_le_sqrt (by linarith))
    have h_sqrt_diff_le :
        Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1) ≤ 1 / Real.sqrt (d : ℝ) := by
      have h_prod :
          (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) *
            (Real.sqrt (d : ℝ) + Real.sqrt ((d : ℝ) - 1)) = 1 := by
        calc
          (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) *
              (Real.sqrt (d : ℝ) + Real.sqrt ((d : ℝ) - 1))
            = (Real.sqrt (d : ℝ)) ^ 2 - (Real.sqrt ((d : ℝ) - 1)) ^ 2 := by ring
          _ = (d : ℝ) - ((d : ℝ) - 1) := by
              rw [Real.sq_sqrt (le_of_lt hd_pos), Real.sq_sqrt (le_of_lt hdm1_pos)]
          _ = 1 := by ring
      have h_sum_ge : Real.sqrt (d : ℝ) ≤ Real.sqrt (d : ℝ) + Real.sqrt ((d : ℝ) - 1) := by
        linarith [Real.sqrt_nonneg ((d : ℝ) - 1)]
      rw [le_div_iff hsqrt_pos]
      have hm := mul_le_mul_of_nonneg_left h_sum_ge h_sqrt_diff_nn
      linarith [h_prod]
    have h_log_diff_nn : 0 ≤ Real.log (d : ℝ) - Real.log ((d : ℝ) - 1) :=
      sub_nonneg.mpr (Real.log_le_log hdm1_pos (by linarith))
    have h_log_diff_le : Real.log (d : ℝ) - Real.log ((d : ℝ) - 1) ≤ 1 / ((d : ℝ) - 1) := by
      have h_exp := Real.add_one_le_exp (1 / ((d : ℝ) - 1))
      have h_lhs : 1 / ((d : ℝ) - 1) + 1 = (d : ℝ) / ((d : ℝ) - 1) := by
        field_simp [ne_of_gt hdm1_pos]
      rw [h_lhs] at h_exp
      have hl := Real.log_le_log (div_pos hd_pos hdm1_pos) h_exp
      rw [Real.log_exp, Real.log_div (ne_of_gt hd_pos) (ne_of_gt hdm1_pos)] at hl
      linarith
    have h_sqrt_d_le : Real.sqrt (d : ℝ) ≤ 2 * Real.sqrt ((d : ℝ) - 1) := by
      have h_sq_le : (Real.sqrt (d : ℝ)) ^ 2 ≤ (2 * Real.sqrt ((d : ℝ) - 1)) ^ 2 := by
        rw [Real.sq_sqrt (le_of_lt hd_pos), mul_pow, Real.sq_sqrt (le_of_lt hdm1_pos)]
        linarith
      have h_diff_sq :
          (2 * Real.sqrt ((d : ℝ) - 1)) ^ 2 - (Real.sqrt (d : ℝ)) ^ 2 =
            (2 * Real.sqrt ((d : ℝ) - 1) - Real.sqrt (d : ℝ)) *
              (2 * Real.sqrt ((d : ℝ) - 1) + Real.sqrt (d : ℝ)) := by ring
      have h_sum_pos : 0 < 2 * Real.sqrt ((d : ℝ) - 1) + Real.sqrt (d : ℝ) := by positivity
      by_contra h_gt
      push_neg at h_gt
      have h_neg : (2 * Real.sqrt ((d : ℝ) - 1)) ^ 2 - (Real.sqrt (d : ℝ)) ^ 2 < 0 := by
        rw [h_diff_sq]
        exact mul_neg_of_neg_of_pos (by linarith) h_sum_pos
      linarith
    have h_mid :
        4 * Real.sqrt ((d : ℝ) - 1) * (Real.log (d : ℝ) - Real.log ((d : ℝ) - 1)) ≤
          8 / Real.sqrt (d : ℝ) := by
      have h1 :
          4 * Real.sqrt ((d : ℝ) - 1) * (Real.log (d : ℝ) - Real.log ((d : ℝ) - 1)) ≤
            4 / Real.sqrt ((d : ℝ) - 1) := by
        have hsq : Real.sqrt ((d : ℝ) - 1) * Real.sqrt ((d : ℝ) - 1) = (d : ℝ) - 1 :=
          Real.mul_self_sqrt (le_of_lt hdm1_pos)
        have h_inv_s : Real.sqrt ((d : ℝ) - 1) * (Real.sqrt ((d : ℝ) - 1))⁻¹ = 1 :=
          mul_inv_cancel (ne_of_gt hsqrt_m1_pos)
        calc
          4 * Real.sqrt ((d : ℝ) - 1) * (Real.log (d : ℝ) - Real.log ((d : ℝ) - 1))
            ≤ 4 * Real.sqrt ((d : ℝ) - 1) * (1 / ((d : ℝ) - 1)) :=
              mul_le_mul_of_nonneg_left h_log_diff_le (by positivity)
          _ = 4 * Real.sqrt ((d : ℝ) - 1) *
                (1 / (Real.sqrt ((d : ℝ) - 1) * Real.sqrt ((d : ℝ) - 1))) := by rw [hsq]
          _ = (4 / Real.sqrt ((d : ℝ) - 1)) *
                (Real.sqrt ((d : ℝ) - 1) * (Real.sqrt ((d : ℝ) - 1))⁻¹) := by
              simp only [div_eq_mul_inv, mul_inv_rev, one_mul]
              ring
          _ = 4 / Real.sqrt ((d : ℝ) - 1) := by rw [h_inv_s, mul_one]
      have h2 : 4 / Real.sqrt ((d : ℝ) - 1) ≤ 8 / Real.sqrt (d : ℝ) := by
        rw [div_le_div_iff hsqrt_m1_pos hsqrt_pos]
        linarith
      exact le_trans h1 h2
    unfold squarePoleDriftM
    rw [if_neg hd_ne, if_neg hdm1_ne, hdm1_eq]
    have h_decomp :
        4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ) + c_half * Real.sqrt (d : ℝ) -
            (4 * Real.sqrt ((d : ℝ) - 1) * Real.log ((d : ℝ) - 1) +
              c_half * Real.sqrt ((d : ℝ) - 1)) =
          4 * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) * Real.log (d : ℝ) +
            4 * Real.sqrt ((d : ℝ) - 1) * (Real.log (d : ℝ) - Real.log ((d : ℝ) - 1)) +
            c_half * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) := by ring
    rw [h_decomp]
    have hlogd_nn : 0 ≤ Real.log (d : ℝ) := Real.log_nonneg (by linarith)
    have ht1 :
        |4 * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) * Real.log (d : ℝ)| ≤
          4 * Real.log (d : ℝ) / Real.sqrt (d : ℝ) := by
      rw [abs_of_nonneg (by positivity)]
      calc
        4 * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) * Real.log (d : ℝ)
          ≤ 4 * (1 / Real.sqrt (d : ℝ)) * Real.log (d : ℝ) :=
            mul_le_mul_of_nonneg_right
              (mul_le_mul_of_nonneg_left h_sqrt_diff_le (by norm_num)) hlogd_nn
        _ = 4 * Real.log (d : ℝ) / Real.sqrt (d : ℝ) := by ring
    have ht2 :
        |4 * Real.sqrt ((d : ℝ) - 1) * (Real.log (d : ℝ) - Real.log ((d : ℝ) - 1))| ≤
          8 / Real.sqrt (d : ℝ) := by
      rw [abs_of_nonneg (by positivity)]
      exact h_mid
    have ht3 :
        |c_half * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1))| ≤
          |c_half| / Real.sqrt (d : ℝ) := by
      rw [abs_mul, abs_of_nonneg h_sqrt_diff_nn]
      calc
        |c_half| * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1))
          ≤ |c_half| * (1 / Real.sqrt (d : ℝ)) :=
            mul_le_mul_of_nonneg_left h_sqrt_diff_le (abs_nonneg c_half)
        _ = |c_half| / Real.sqrt (d : ℝ) := by ring
    have h_tri1 := abs_add
      (4 * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) * Real.log (d : ℝ) +
        4 * Real.sqrt ((d : ℝ) - 1) * (Real.log (d : ℝ) - Real.log ((d : ℝ) - 1)))
      (c_half * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)))
    have h_tri2 := abs_add
      (4 * (Real.sqrt (d : ℝ) - Real.sqrt ((d : ℝ) - 1)) * Real.log (d : ℝ))
      (4 * Real.sqrt ((d : ℝ) - 1) * (Real.log (d : ℝ) - Real.log ((d : ℝ) - 1)))
    have h_sum_num :
        (4 * Real.log (d : ℝ) + 8 + |c_half|) / Real.sqrt (d : ℝ) ≤
          (8 + |c_half|) * (1 + Real.log (d : ℝ)) / Real.sqrt (d : ℝ) := by
      apply div_le_div_of_nonneg_right _ (le_of_lt hsqrt_pos)
      have h_extra_nn : 0 ≤ (4 + |c_half|) * Real.log (d : ℝ) :=
        mul_nonneg (by positivity) hlogd_nn
      linarith [h_extra_nn, show (8 + |c_half|) * (1 + Real.log (d : ℝ)) -
        (4 * Real.log (d : ℝ) + 8 + |c_half|) = (4 + |c_half|) * Real.log (d : ℝ) by ring]
    have h_comb :
        4 * Real.log (d : ℝ) / Real.sqrt (d : ℝ) +
            8 / Real.sqrt (d : ℝ) + |c_half| / Real.sqrt (d : ℝ) =
          (4 * Real.log (d : ℝ) + 8 + |c_half|) / Real.sqrt (d : ℝ) := by ring
    linarith

private theorem sum_inv_sq_Icc_succ_le_inv_tc062r_aux {a : ℕ} (ha : 1 ≤ a) (M : ℕ) :
    (∑ r ∈ Finset.Icc (a + 1) M, (1 / (r : ℝ) ^ 2)) ≤ 1 / (a : ℝ) := by
  by_cases h_lt : M < a
  · have h_emp : Finset.Icc (a + 1) M = ∅ := by
      ext r; simp only [Finset.mem_Icc, Finset.not_mem_empty, iff_false]; omega
    rw [h_emp, Finset.sum_empty]
    positivity
  · have ha_le : a ≤ M := by omega
    obtain ⟨k, rfl⟩ : ∃ k : ℕ, M = a + k := ⟨M - a, by omega⟩
    have h_tel :
        ∀ m : ℕ,
          (∑ r ∈ Finset.Icc (a + 1) (a + m), (1 / (r : ℝ) ^ 2)) ≤
            1 / (a : ℝ) - 1 / ((a + m : ℕ) : ℝ) := by
      intro m
      induction' m with m ih
      · simp
      · have h_ins :
            Finset.Icc (a + 1) (a + (m + 1)) =
              insert (a + m + 1) (Finset.Icc (a + 1) (a + m)) := by
          ext r; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
        have h_not : a + m + 1 ∉ Finset.Icc (a + 1) (a + m) := by simp
        rw [h_ins, Finset.sum_insert h_not]
        let x : ℝ := ((a + m : ℕ) : ℝ)
        have hx_pos : 0 < x := by dsimp [x]; exact_mod_cast (by omega : 0 < a + m)
        have hx1_pos : 0 < x + 1 := by linarith
        have h_cast : ((a + m + 1 : ℕ) : ℝ) = x + 1 := by dsimp [x]; push_cast; ring
        have h_cast2 : ((a + (m + 1) : ℕ) : ℝ) = x + 1 := by dsimp [x]; push_cast; ring
        rw [h_cast, h_cast2]
        have h_step : 1 / (x + 1) ^ 2 ≤ 1 / x - 1 / (x + 1) := by
          have h_diff : 1 / x - 1 / (x + 1) = 1 / (x * (x + 1)) := by
            field_simp [ne_of_gt hx_pos, ne_of_gt hx1_pos]
          rw [h_diff]
          exact one_div_le_one_div_of_le (mul_pos hx_pos hx1_pos) (by nlinarith)
        linarith
    have h_res := h_tel k
    have h_inv_nn : 0 ≤ 1 / ((a + k : ℕ) : ℝ) := by positivity
    linarith

private theorem gaussianTermPhi_windowEnergy_bounds_tc062r_aux
    {Y : ℝ} (hY2 : 2 ≤ Y) {k : ℕ} (hk1 : 1 ≤ k) :
    0 ≤ windowEnergyNormSq Y (gaussianTermPhi k) ∧
      windowEnergyNormSq Y (gaussianTermPhi k) ≤
        (27 / 8 : ℝ) * (RiemannScope.tau - 1) / Y ∧
      windowEnergyNormSq Y (gaussianTermPhi k) ≤
        (RiemannScope.tau - 1) * RiemannScope.tau ^ 4 * Y ^ 5 / (k : ℝ) ^ 6 := by
  obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc062_aux hY2
  have hY_pos : 0 < Y := by linarith only [hY2]
  have hk_pos : (0 : ℝ) < (k : ℝ) := Nat.cast_pos.mpr (by omega)
  have hk_ne : (k : ℝ) ≠ 0 := ne_of_gt hk_pos
  have h_cont := continuousOn_gaussianTermPhi_uIcc_tc062_aux Y k
  have h_int :
      IntervalIntegrable
        (fun X => gaussianTermPhi k X * gaussianTermPhi k X / X)
        volume Y (RiemannScope.tau * Y) :=
    ((h_cont.mul h_cont).div continuousOn_id
      (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
  have h_pt_eq :
      ∀ X : ℝ, 0 < X →
        gaussianTermPhi k X * gaussianTermPhi k X / X =
          X ^ 4 / (k : ℝ) ^ 6 * Real.exp (-(2 * X ^ 2 / (k : ℝ) ^ 2)) := by
    intro X hX_pos
    have hX_ne : X ≠ 0 := ne_of_gt hX_pos
    have hX5 : X ^ (5 / 2 : ℝ) * X ^ (5 / 2 : ℝ) = X ^ 5 := by
      rw [← sq, ← Real.rpow_natCast _ 2, ← Real.rpow_mul (le_of_lt hX_pos)]
      have he : (5 / 2 : ℝ) * ((2 : ℕ) : ℝ) = ((5 : ℕ) : ℝ) := by norm_num
      rw [he, Real.rpow_natCast]
    have hexp2 :
        Real.exp (-(X ^ 2) / (k : ℝ) ^ 2) * Real.exp (-(X ^ 2) / (k : ℝ) ^ 2) =
          Real.exp (-(2 * X ^ 2 / (k : ℝ) ^ 2)) := by
      rw [← Real.exp_add]
      congr 1
      ring
    unfold gaussianTermPhi
    calc
      (X ^ (5 / 2 : ℝ) * (((k : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (k : ℝ) ^ 2))) *
          (X ^ (5 / 2 : ℝ) * (((k : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (k : ℝ) ^ 2))) / X
        = (X ^ (5 / 2 : ℝ) * X ^ (5 / 2 : ℝ)) *
            ((((k : ℝ) ^ 3)⁻¹ * ((k : ℝ) ^ 3)⁻¹) *
              (Real.exp (-(X ^ 2) / (k : ℝ) ^ 2) * Real.exp (-(X ^ 2) / (k : ℝ) ^ 2))) / X := by
            ring
      _ = X ^ 5 * ((((k : ℝ) ^ 3)⁻¹ * ((k : ℝ) ^ 3)⁻¹) *
            Real.exp (-(2 * X ^ 2 / (k : ℝ) ^ 2))) / X := by rw [hX5, hexp2]
      _ = X ^ 4 / (k : ℝ) ^ 6 * Real.exp (-(2 * X ^ 2 / (k : ℝ) ^ 2)) := by
          field_simp [hX_ne, hk_ne]; ring
  unfold windowEnergyNormSq windowPairing
  have h_nn :
      0 ≤ ∫ X in Y..(RiemannScope.tau * Y),
        gaussianTermPhi k X * gaussianTermPhi k X / X := by
    apply intervalIntegral.integral_nonneg hle
    intro X hX
    exact div_nonneg (mul_self_nonneg _) (by rw [Set.mem_Icc] at hX; linarith only [hY2, hX.1])
  have h_bd1 :
      (∫ X in Y..(RiemannScope.tau * Y),
          gaussianTermPhi k X * gaussianTermPhi k X / X) ≤
        (27 / 8 : ℝ) * (RiemannScope.tau - 1) / Y := by
    have hc1 : IntervalIntegrable (fun _ : ℝ => (27 / 8 : ℝ) / Y ^ 2)
        volume Y (RiemannScope.tau * Y) := intervalIntegrable_const
    have hm1 :=
      intervalIntegral.integral_mono_on hle h_int hc1 (by
        intro X hX
        have hX_pos : 0 < X := by linarith only [hY_pos, hX.1]
        have hX_ne : X ≠ 0 := ne_of_gt hX_pos
        rw [h_pt_eq X hX_pos]
        let z : ℝ := 2 * X ^ 2 / (k : ℝ) ^ 2
        have hz_pos : 0 < z := by dsimp [z]; positivity
        have hz3 : z / 3 ≤ Real.exp (z / 3) := by linarith [Real.add_one_le_exp (z / 3)]
        have hz_cube : (z / 3) ^ 3 ≤ (Real.exp (z / 3)) ^ 3 :=
          pow_le_pow_left (by positivity) hz3 3
        have hexp_cube : (Real.exp (z / 3)) ^ 3 = Real.exp z := by
          rw [← Real.exp_nat_mul]; congr 1; ring
        rw [hexp_cube] at hz_cube
        have hexp_prod : Real.exp z * Real.exp (-z) = 1 := by
          rw [← Real.exp_add, add_neg_self, Real.exp_zero]
        have hm_exp := mul_le_mul_of_nonneg_right hz_cube (le_of_lt (Real.exp_pos (-z)))
        rw [hexp_prod] at hm_exp
        have hexp_neg_le : Real.exp (-z) ≤ 27 / z ^ 3 := by
          rw [le_div_iff (pow_pos hz_pos 3)]
          linarith [show (z / 3) ^ 3 * Real.exp (-z) = Real.exp (-z) * z ^ 3 / 27 by ring]
        calc
          X ^ 4 / (k : ℝ) ^ 6 * Real.exp (-z)
            ≤ X ^ 4 / (k : ℝ) ^ 6 * (27 / z ^ 3) :=
              mul_le_mul_of_nonneg_left hexp_neg_le (by positivity)
          _ = (27 / 8 : ℝ) / X ^ 2 := by
              dsimp [z]
              field_simp [hX_ne, hk_ne]
              ring
          _ ≤ (27 / 8 : ℝ) / Y ^ 2 :=
              div_le_div_of_nonneg_left (by norm_num) (sq_pos_of_pos hY_pos)
                (pow_le_pow_left (le_of_lt hY_pos) hX.1 2))
    rw [intervalIntegral.integral_const, smul_eq_mul] at hm1
    have h_eq1 :
        (RiemannScope.tau * Y - Y) * ((27 / 8 : ℝ) / Y ^ 2) =
          (27 / 8 : ℝ) * (RiemannScope.tau - 1) / Y := by
      field_simp [ne_of_gt hY_pos]; ring
    linarith only [hm1, h_eq1]
  have h_bd2 :
      (∫ X in Y..(RiemannScope.tau * Y),
          gaussianTermPhi k X * gaussianTermPhi k X / X) ≤
        (RiemannScope.tau - 1) * RiemannScope.tau ^ 4 * Y ^ 5 / (k : ℝ) ^ 6 := by
    have hc2 :
        IntervalIntegrable (fun _ : ℝ => (RiemannScope.tau * Y) ^ 4 / (k : ℝ) ^ 6)
          volume Y (RiemannScope.tau * Y) := intervalIntegrable_const
    have hm2 :=
      intervalIntegral.integral_mono_on hle h_int hc2 (by
        intro X hX
        have hX_pos : 0 < X := by linarith only [hY_pos, hX.1]
        rw [h_pt_eq X hX_pos]
        have hexp_le1 : Real.exp (-(2 * X ^ 2 / (k : ℝ) ^ 2)) ≤ 1 := by
          rw [Real.exp_le_one_iff]
          exact neg_nonpos.mpr (by positivity)
        have hX4_le : X ^ 4 ≤ (RiemannScope.tau * Y) ^ 4 :=
          pow_le_pow_left (le_of_lt hX_pos) hX.2 4
        calc
          X ^ 4 / (k : ℝ) ^ 6 * Real.exp (-(2 * X ^ 2 / (k : ℝ) ^ 2))
            ≤ X ^ 4 / (k : ℝ) ^ 6 * 1 :=
              mul_le_mul_of_nonneg_left hexp_le1 (by positivity)
          _ = X ^ 4 / (k : ℝ) ^ 6 := mul_one _
          _ ≤ (RiemannScope.tau * Y) ^ 4 / (k : ℝ) ^ 6 :=
              div_le_div_of_nonneg_right hX4_le (by positivity))
    rw [intervalIntegral.integral_const, smul_eq_mul] at hm2
    have h_eq2 :
        (RiemannScope.tau * Y - Y) * ((RiemannScope.tau * Y) ^ 4 / (k : ℝ) ^ 6) =
          (RiemannScope.tau - 1) * RiemannScope.tau ^ 4 * Y ^ 5 / (k : ℝ) ^ 6 := by
      field_simp [hk_ne]; ring
    linarith only [hm2, h_eq2]
  exact ⟨h_nn, h_bd1, h_bd2⟩

private theorem sum_multiples_gaussianTermPhi_windowEnergy_le_tc062r_aux :
    let C_phi : ℝ := (RiemannScope.tau - 1) * (27 / 8 + 2 * RiemannScope.tau ^ 4)
    0 < C_phi ∧
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ (T : ℕ) {L : ℕ}, 1 ≤ L →
        (∑ k ∈ (Finset.Icc 1 T).filter (fun k => L ∣ k),
          windowEnergyNormSq Y (gaussianTermPhi k)) ≤ C_phi / (L : ℝ) := by
  dsimp only
  have htau_bds := tau_gt_one_and_lt_eight_tc062_aux
  have htau_pos : 0 < RiemannScope.tau := by linarith only [htau_bds.1]
  have htau_m1_pos : 0 < RiemannScope.tau - 1 := by linarith only [htau_bds.1]
  let C_phi : ℝ := (RiemannScope.tau - 1) * (27 / 8 + 2 * RiemannScope.tau ^ 4)
  have hCphi_pos : 0 < C_phi := by dsimp [C_phi]; positivity
  refine ⟨hCphi_pos, ?_⟩
  intro Y hY2 T L hL1
  have hY_pos : 0 < Y := by linarith only [hY2]
  have hY_ne : Y ≠ 0 := ne_of_gt hY_pos
  have hL_pos_nat : 0 < L := by omega
  have hL_pos : (0 : ℝ) < (L : ℝ) := Nat.cast_pos.mpr hL_pos_nat
  have hL_ne : (L : ℝ) ≠ 0 := ne_of_gt hL_pos
  let M := T / L
  have h_reidx :
      (Finset.Icc 1 T).filter (fun k => L ∣ k) =
        (Finset.Icc 1 M).image (fun r => L * r) := by
    ext k
    simp only [M, Finset.mem_filter, Finset.mem_Icc, Finset.mem_image]
    constructor
    · rintro ⟨⟨hk1, hkT⟩, h_dvd⟩
      refine ⟨k / L, ⟨Nat.div_pos (Nat.le_of_dvd hk1 h_dvd) hL_pos_nat,
        Nat.div_le_div_right hkT⟩, Nat.mul_div_cancel' h_dvd⟩
    · rintro ⟨r, ⟨hr1, hrM⟩, rfl⟩
      have h_le : L * r ≤ T := by
        rw [mul_comm]
        exact le_trans (Nat.mul_le_mul_right L hrM) (Nat.div_mul_le_self T L)
      exact ⟨⟨Nat.mul_pos hL_pos_nat hr1, h_le⟩, dvd_mul_right L r⟩
  have h_inj : Set.InjOn (fun r => L * r) ↑(Finset.Icc 1 M) :=
    fun _ _ _ _ h_eq => Nat.eq_of_mul_eq_mul_left hL_pos_nat h_eq
  rw [h_reidx, Finset.sum_image h_inj]
  let m0 := Nat.floor (Y / (L : ℝ))
  have h_sub_u : Finset.Icc 1 M ⊆ Finset.Icc 1 m0 ∪ Finset.Icc (m0 + 1) M := by
    intro r hr
    rw [Finset.mem_Icc] at hr
    simp only [Finset.mem_union, Finset.mem_Icc]
    omega
  have h_disj : Disjoint (Finset.Icc 1 m0) (Finset.Icc (m0 + 1) M) := by
    rw [Finset.disjoint_left]; intro r h1 h2; simp only [Finset.mem_Icc] at h1 h2; omega
  have h_term_nn : ∀ r : ℕ, 0 ≤ windowEnergyNormSq Y (gaussianTermPhi (L * r)) := by
    intro r
    obtain ⟨hle, _⟩ := uIcc_tau_props_tc062_aux hY2
    unfold windowEnergyNormSq windowPairing
    apply intervalIntegral.integral_nonneg hle
    intro X hX
    exact div_nonneg (mul_self_nonneg _) (by rw [Set.mem_Icc] at hX; linarith only [hY2, hX.1])
  have h_split :
      (∑ r ∈ Finset.Icc 1 M, windowEnergyNormSq Y (gaussianTermPhi (L * r))) ≤
        (∑ r ∈ Finset.Icc 1 m0, windowEnergyNormSq Y (gaussianTermPhi (L * r))) +
          (∑ r ∈ Finset.Icc (m0 + 1) M, windowEnergyNormSq Y (gaussianTermPhi (L * r))) := by
    rw [← Finset.sum_union h_disj]
    exact Finset.sum_le_sum_of_subset_of_nonneg h_sub_u (fun r _ _ => h_term_nn r)
  have h_head :
      (∑ r ∈ Finset.Icc 1 m0, windowEnergyNormSq Y (gaussianTermPhi (L * r))) ≤
        (RiemannScope.tau - 1) * (27 / 8 : ℝ) / (L : ℝ) := by
    have h_each :
        ∀ r ∈ Finset.Icc 1 m0,
          windowEnergyNormSq Y (gaussianTermPhi (L * r)) ≤
            (27 / 8 : ℝ) * (RiemannScope.tau - 1) / Y := by
      intro r hr
      have hr1 : 1 ≤ r := (Finset.mem_Icc.mp hr).1
      exact (gaussianTermPhi_windowEnergy_bounds_tc062r_aux hY2 (Nat.mul_pos hL_pos_nat hr1)).2.1
    have h_m0_le : (m0 : ℝ) ≤ Y / (L : ℝ) := Nat.floor_le (by positivity)
    calc
      (∑ r ∈ Finset.Icc 1 m0, windowEnergyNormSq Y (gaussianTermPhi (L * r)))
        ≤ ∑ _r ∈ Finset.Icc 1 m0, ((27 / 8 : ℝ) * (RiemannScope.tau - 1) / Y) :=
          Finset.sum_le_sum h_each
      _ = ((Finset.Icc 1 m0).card : ℝ) * ((27 / 8 : ℝ) * (RiemannScope.tau - 1) / Y) := by simp
      _ ≤ (Y / (L : ℝ)) * ((27 / 8 : ℝ) * (RiemannScope.tau - 1) / Y) := by
          have hc : (Finset.Icc 1 m0).card ≤ m0 := by simp [Nat.card_Icc]
          exact mul_le_mul_of_nonneg_right
            (le_trans (by exact_mod_cast hc) h_m0_le) (by positivity)
      _ = (RiemannScope.tau - 1) * (27 / 8 : ℝ) / (L : ℝ) := by
          field_simp [hY_ne, hL_ne]; ring
  have h_tail :
      (∑ r ∈ Finset.Icc (m0 + 1) M, windowEnergyNormSq Y (gaussianTermPhi (L * r))) ≤
        (RiemannScope.tau - 1) * (2 * RiemannScope.tau ^ 4) / (L : ℝ) := by
    have h_each_tail :
        ∀ r ∈ Finset.Icc (m0 + 1) M,
          windowEnergyNormSq Y (gaussianTermPhi (L * r)) ≤
            ((RiemannScope.tau - 1) * RiemannScope.tau ^ 4 * Y ^ 5 / (L : ℝ) ^ 6) *
              (1 / (r : ℝ) ^ 6) := by
      intro r hr
      have hr1 : 1 ≤ r := by rw [Finset.mem_Icc] at hr; omega
      have hb :=
        (gaussianTermPhi_windowEnergy_bounds_tc062r_aux hY2 (Nat.mul_pos hL_pos_nat hr1)).2.2
      have h_pow6 : ((L * r : ℕ) : ℝ) ^ 6 = (L : ℝ) ^ 6 * (r : ℝ) ^ 6 := by push_cast; ring
      rw [h_pow6] at hb
      calc
        windowEnergyNormSq Y (gaussianTermPhi (L * r))
          ≤ (RiemannScope.tau - 1) * RiemannScope.tau ^ 4 * Y ^ 5 / ((L : ℝ) ^ 6 * (r : ℝ) ^ 6) := hb
        _ = ((RiemannScope.tau - 1) * RiemannScope.tau ^ 4 * Y ^ 5 / (L : ℝ) ^ 6) *
              (1 / (r : ℝ) ^ 6) := by ring
    have h_sum_r6 :
        (∑ r ∈ Finset.Icc (m0 + 1) M, windowEnergyNormSq Y (gaussianTermPhi (L * r))) ≤
          ((RiemannScope.tau - 1) * RiemannScope.tau ^ 4 * Y ^ 5 / (L : ℝ) ^ 6) *
            (∑ r ∈ Finset.Icc (m0 + 1) M, (1 / (r : ℝ) ^ 6)) := by
      rw [Finset.mul_sum]
      exact Finset.sum_le_sum h_each_tail
    by_cases hm0_zero : m0 = 0
    · have hYL_lt1 : Y / (L : ℝ) < 1 := by
        have hlt := Nat.lt_floor_add_one (Y / (L : ℝ))
        change Y / (L : ℝ) < (m0 : ℝ) + 1 at hlt
        rw [hm0_zero] at hlt
        simpa using hlt
      have hY_le_L : Y ≤ (L : ℝ) := by
        rw [div_lt_one hL_pos] at hYL_lt1
        exact le_of_lt hYL_lt1
      have hY5_L6 : Y ^ 5 / (L : ℝ) ^ 6 ≤ 1 / (L : ℝ) := by
        have hY5 : Y ^ 5 ≤ (L : ℝ) ^ 5 := pow_le_pow_left (le_of_lt hY_pos) hY_le_L 5
        calc
          Y ^ 5 / (L : ℝ) ^ 6 ≤ (L : ℝ) ^ 5 / (L : ℝ) ^ 6 :=
            div_le_div_of_nonneg_right hY5 (by positivity)
          _ = 1 / (L : ℝ) := by field_simp [hL_ne]; ring
      have h_r6_le2 : (∑ r ∈ Finset.Icc 1 M, (1 / (r : ℝ) ^ 6)) ≤ 2 := by
        have h_sub12 : Finset.Icc 1 M ⊆ ({1} : Finset ℕ) ∪ Finset.Icc 2 M := by
          intro r hr
          rw [Finset.mem_Icc] at hr
          simp only [Finset.mem_union, Finset.mem_singleton, Finset.mem_Icc]
          omega
        have h_d12 : Disjoint ({1} : Finset ℕ) (Finset.Icc 2 M) := by
          rw [Finset.disjoint_left]; intro r h1 h2; simp at h1 h2; omega
        have h1 :
            (∑ r ∈ Finset.Icc 1 M, (1 / (r : ℝ) ^ 6)) ≤
              1 + ∑ r ∈ Finset.Icc 2 M, (1 / (r : ℝ) ^ 6) := by
          calc
            (∑ r ∈ Finset.Icc 1 M, (1 / (r : ℝ) ^ 6))
              ≤ ∑ r ∈ ({1} : Finset ℕ) ∪ Finset.Icc 2 M, (1 / (r : ℝ) ^ 6) :=
                Finset.sum_le_sum_of_subset_of_nonneg h_sub12 (fun _ _ _ => by positivity)
            _ = 1 + ∑ r ∈ Finset.Icc 2 M, (1 / (r : ℝ) ^ 6) := by
                rw [Finset.sum_union h_d12, Finset.sum_singleton]; norm_num
        have h2 :
            (∑ r ∈ Finset.Icc 2 M, (1 / (r : ℝ) ^ 6)) ≤
              ∑ r ∈ Finset.Icc 2 M, (1 / (r : ℝ) ^ 2) := by
          apply Finset.sum_le_sum
          intro r hr
          have hr1 : (1 : ℝ) ≤ (r : ℝ) := by
            have hr_ge2 := (Finset.mem_Icc.mp hr).1
            exact_mod_cast (by omega : 1 ≤ r)
          have hp : (r : ℝ) ^ 2 ≤ (r : ℝ) ^ 6 := by
            have h4 : (1 : ℝ) ≤ (r : ℝ) ^ 4 := one_le_pow_of_one_le hr1 4
            calc
              (r : ℝ) ^ 2 = (r : ℝ) ^ 2 * 1 := (mul_one _).symm
              _ ≤ (r : ℝ) ^ 2 * (r : ℝ) ^ 4 := mul_le_mul_of_nonneg_left h4 (sq_nonneg _)
              _ = (r : ℝ) ^ 6 := by ring
          exact one_div_le_one_div_of_le (pow_pos (by linarith) 2) hp
        have h3 := sum_inv_sq_Icc_succ_le_inv_tc062r_aux (le_refl 1) M
        push_cast at h3
        linarith
      rw [hm0_zero, zero_add] at h_sum_r6 ⊢
      calc
        (∑ r ∈ Finset.Icc 1 M, windowEnergyNormSq Y (gaussianTermPhi (L * r)))
          ≤ ((RiemannScope.tau - 1) * RiemannScope.tau ^ 4 * (Y ^ 5 / (L : ℝ) ^ 6)) * 2 := by
            have hm := mul_le_mul_of_nonneg_left h_r6_le2
              (show 0 ≤ (RiemannScope.tau - 1) * RiemannScope.tau ^ 4 * Y ^ 5 / (L : ℝ) ^ 6 by positivity)
            linarith [h_sum_r6, hm,
              show ((RiemannScope.tau - 1) * RiemannScope.tau ^ 4 * Y ^ 5 / (L : ℝ) ^ 6) * 2 =
                ((RiemannScope.tau - 1) * RiemannScope.tau ^ 4 * (Y ^ 5 / (L : ℝ) ^ 6)) * 2 by ring]
        _ ≤ ((RiemannScope.tau - 1) * RiemannScope.tau ^ 4 * (1 / (L : ℝ))) * 2 :=
            mul_le_mul_of_nonneg_right
              (mul_le_mul_of_nonneg_left hY5_L6 (by positivity)) (by norm_num)
        _ = (RiemannScope.tau - 1) * (2 * RiemannScope.tau ^ 4) / (L : ℝ) := by ring
    · have hm0_ge1 : 1 ≤ m0 := by omega
      have hYL_lt : Y / (L : ℝ) < (m0 : ℝ) + 1 := Nat.lt_floor_add_one (Y / (L : ℝ))
      have hm0_ge_half : Y / (2 * (L : ℝ)) ≤ (m0 : ℝ) := by
        have h1_le_m0 : (1 : ℝ) ≤ (m0 : ℝ) := by exact_mod_cast hm0_ge1
        have h2m0 : Y / (L : ℝ) ≤ 2 * (m0 : ℝ) := by linarith
        have hm := div_le_div_of_nonneg_right h2m0 (by norm_num : (0 : ℝ) ≤ 2)
        calc
          Y / (2 * (L : ℝ)) = (Y / (L : ℝ)) / 2 := by ring
          _ ≤ (2 * (m0 : ℝ)) / 2 := hm
          _ = (m0 : ℝ) := by ring
      have h_inv_m0 : 1 / (m0 : ℝ) ≤ 2 * (L : ℝ) / Y := by
        have h_pos_div : 0 < Y / (2 * (L : ℝ)) := by positivity
        have h1 := one_div_le_one_div_of_le h_pos_div hm0_ge_half
        have h_simp : 1 / (Y / (2 * (L : ℝ))) = 2 * (L : ℝ) / Y := by
          field_simp [hY_ne, hL_ne]
        rwa [h_simp] at h1
      have h_r6_tail :
          (∑ r ∈ Finset.Icc (m0 + 1) M, (1 / (r : ℝ) ^ 6)) ≤
            2 * (L : ℝ) ^ 5 / Y ^ 5 := by
        have h_each_r :
            ∀ r ∈ Finset.Icc (m0 + 1) M,
              1 / (r : ℝ) ^ 6 ≤ ((L : ℝ) ^ 4 / Y ^ 4) * (1 / (r : ℝ) ^ 2) := by
          intro r hr
          have hr_ge : m0 + 1 ≤ r := (Finset.mem_Icc.mp hr).1
          have hr_r : (m0 : ℝ) + 1 ≤ (r : ℝ) := by exact_mod_cast hr_ge
          have hYL_le_r : Y / (L : ℝ) ≤ (r : ℝ) := le_of_lt (lt_of_lt_of_le hYL_lt hr_r)
          have h4 : (Y / (L : ℝ)) ^ 4 ≤ (r : ℝ) ^ 4 :=
            pow_le_pow_left (by positivity) hYL_le_r 4
          have h_inv4 : 1 / (r : ℝ) ^ 4 ≤ (L : ℝ) ^ 4 / Y ^ 4 := by
            have h1 := one_div_le_one_div_of_le (pow_pos (div_pos hY_pos hL_pos) 4) h4
            have h_eq : 1 / (Y / (L : ℝ)) ^ 4 = (L : ℝ) ^ 4 / Y ^ 4 := by
              field_simp [hY_ne, hL_ne]
            rwa [h_eq] at h1
          calc
            1 / (r : ℝ) ^ 6 = (1 / (r : ℝ) ^ 4) * (1 / (r : ℝ) ^ 2) := by ring
            _ ≤ ((L : ℝ) ^ 4 / Y ^ 4) * (1 / (r : ℝ) ^ 2) :=
                mul_le_mul_of_nonneg_right h_inv4 (by positivity)
        calc
          (∑ r ∈ Finset.Icc (m0 + 1) M, (1 / (r : ℝ) ^ 6))
            ≤ ∑ r ∈ Finset.Icc (m0 + 1) M, ((L : ℝ) ^ 4 / Y ^ 4) * (1 / (r : ℝ) ^ 2) :=
              Finset.sum_le_sum h_each_r
          _ = ((L : ℝ) ^ 4 / Y ^ 4) * ∑ r ∈ Finset.Icc (m0 + 1) M, (1 / (r : ℝ) ^ 2) :=
              (Finset.mul_sum _ _ _).symm
          _ ≤ ((L : ℝ) ^ 4 / Y ^ 4) * (1 / (m0 : ℝ)) :=
              mul_le_mul_of_nonneg_left (sum_inv_sq_Icc_succ_le_inv_tc062r_aux hm0_ge1 M)
                (by positivity)
          _ ≤ ((L : ℝ) ^ 4 / Y ^ 4) * (2 * (L : ℝ) / Y) :=
              mul_le_mul_of_nonneg_left h_inv_m0 (by positivity)
          _ = 2 * (L : ℝ) ^ 5 / Y ^ 5 := by ring
      calc
        (∑ r ∈ Finset.Icc (m0 + 1) M, windowEnergyNormSq Y (gaussianTermPhi (L * r)))
          ≤ ((RiemannScope.tau - 1) * RiemannScope.tau ^ 4 * Y ^ 5 / (L : ℝ) ^ 6) *
              (2 * (L : ℝ) ^ 5 / Y ^ 5) :=
            le_trans h_sum_r6
              (mul_le_mul_of_nonneg_left h_r6_tail (by positivity))
        _ = (RiemannScope.tau - 1) * (2 * RiemannScope.tau ^ 4) / (L : ℝ) := by
            field_simp [hY_ne, hL_ne]; ring
  have h_comb :
      (RiemannScope.tau - 1) * (27 / 8 : ℝ) / (L : ℝ) +
          (RiemannScope.tau - 1) * (2 * RiemannScope.tau ^ 4) / (L : ℝ) =
        ((RiemannScope.tau - 1) * (27 / 8 + 2 * RiemannScope.tau ^ 4)) / (L : ℝ) := by ring
  linarith only [h_split, h_head, h_tail, h_comb]

private theorem one_add_log_le_four_fourth_root_tc062r_aux {x : ℝ} (hx1 : 1 ≤ x) :
    1 + Real.log x ≤ 4 * Real.sqrt (Real.sqrt x) ∧
      (1 + Real.log x) ^ 4 ≤ 256 * x := by
  let u := Real.sqrt (Real.sqrt x)
  have hx_nn : 0 ≤ x := by linarith
  have hu2 : u ^ 2 = Real.sqrt x := by
    dsimp [u]
    exact Real.sq_sqrt (Real.sqrt_nonneg x)
  have hu4 : u ^ 4 = x := by
    calc
      u ^ 4 = (u ^ 2) ^ 2 := by ring
      _ = (Real.sqrt x) ^ 2 := by rw [hu2]
      _ = x := Real.sq_sqrt hx_nn
  have hu_ge1 : 1 ≤ u := by
    dsimp [u]
    calc
      (1 : ℝ) = Real.sqrt (Real.sqrt 1) := by norm_num
      _ ≤ Real.sqrt (Real.sqrt x) := Real.sqrt_le_sqrt (Real.sqrt_le_sqrt hx1)
  have hu_pos : 0 < u := lt_of_lt_of_le zero_lt_one hu_ge1
  have hlog_u : Real.log u ≤ u - 1 := by
    have he := Real.add_one_le_exp (Real.log u)
    rw [Real.exp_log hu_pos] at he
    linarith
  have hlog_x : Real.log x = 4 * Real.log u := by
    rw [← hu4, Real.log_pow]
    push_cast
    ring
  have h1 : 1 + Real.log x ≤ 4 * u := by linarith
  have h_nn : 0 ≤ 1 + Real.log x := by linarith [Real.log_nonneg hx1]
  have h4 := pow_le_pow_left h_nn h1 4
  have hrhs : (4 * u) ^ 4 = 256 * x := by
    calc
      (4 * u) ^ 4 = 256 * u ^ 4 := by ring
      _ = 256 * x := by rw [hu4]
  exact ⟨h1, by rwa [hrhs] at h4⟩

private theorem lcm_weighted_series_bound_tc062r_aux (T : ℕ) :
    (∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
      ((1 + Real.log (d : ℝ)) / Real.sqrt (d : ℝ)) *
        ((1 + Real.log (e : ℝ)) / Real.sqrt (e : ℝ)) /
        (Nat.lcm d e : ℝ)) ≤ 18785 := by
  let q : ℕ → ℝ := fun n => Real.sqrt (Real.sqrt (n : ℝ))
  have hq_props :
      ∀ n : ℕ, 1 ≤ n →
        1 ≤ q n ∧ (q n) ^ 2 = Real.sqrt (n : ℝ) ∧ (q n) ^ 4 = (n : ℝ) ∧
          (q n) ^ 6 = (n : ℝ) * Real.sqrt (n : ℝ) := by
    intro n hn1
    have h1 : 1 ≤ q n := by
      dsimp [q]
      calc
        (1 : ℝ) = Real.sqrt (Real.sqrt 1) := by norm_num
        _ ≤ Real.sqrt (Real.sqrt (n : ℝ)) :=
          Real.sqrt_le_sqrt (Real.sqrt_le_sqrt (by exact_mod_cast hn1))
    have h2 : (q n) ^ 2 = Real.sqrt (n : ℝ) := Real.sq_sqrt (Real.sqrt_nonneg _)
    have h4 : (q n) ^ 4 = (n : ℝ) := by
      calc
        (q n) ^ 4 = ((q n) ^ 2) ^ 2 := by ring
        _ = (Real.sqrt (n : ℝ)) ^ 2 := by rw [h2]
        _ = (n : ℝ) := Real.sq_sqrt (Nat.cast_nonneg n)
    have h6 : (q n) ^ 6 = (n : ℝ) * Real.sqrt (n : ℝ) := by
      calc
        (q n) ^ 6 = (q n) ^ 4 * (q n) ^ 2 := by ring
        _ = (n : ℝ) * Real.sqrt (n : ℝ) := by rw [h4, h2]
    exact ⟨h1, h2, h4, h6⟩
  have h_q5_step :
      ∀ n : ℕ, 2 ≤ n →
        1 / (q n) ^ 5 ≤ 4 * (1 / q (n - 1) - 1 / q n) := by
    intro n hn2
    let m := n - 1
    have hm1 : 1 ≤ m := by omega
    have hn_eq : n = m + 1 := by omega
    rw [hn_eq, show m + 1 - 1 = m by omega]
    obtain ⟨hv1, _, hv4, _⟩ := hq_props m hm1
    obtain ⟨hu1, _, hu4, _⟩ := hq_props (m + 1) (by omega)
    let u := q (m + 1)
    let v := q m
    have hv_pos : 0 < v := lt_of_lt_of_le zero_lt_one hv1
    have hu_pos : 0 < u := lt_of_lt_of_le zero_lt_one hu1
    have hv_le_u : v ≤ u :=
      Real.sqrt_le_sqrt (Real.sqrt_le_sqrt (by exact_mod_cast Nat.le_succ m))
    have h_diff4 : (u - v) * (u + v) * (u ^ 2 + v ^ 2) = 1 := by
      calc
        (u - v) * (u + v) * (u ^ 2 + v ^ 2) = u ^ 4 - v ^ 4 := by ring
        _ = ((m + 1 : ℕ) : ℝ) - (m : ℝ) := by rw [hu4, hv4]
        _ = 1 := by push_cast; ring
    have h_sum1 : u + v ≤ 2 * u := by linarith
    have h_sum2 : u ^ 2 + v ^ 2 ≤ 2 * u ^ 2 := by
      have hsq := pow_le_pow_left (le_of_lt hv_pos) hv_le_u 2
      linarith
    have h_prod_le : (u + v) * (u ^ 2 + v ^ 2) ≤ 4 * u ^ 3 := by
      calc
        (u + v) * (u ^ 2 + v ^ 2) ≤ (2 * u) * (2 * u ^ 2) :=
          mul_le_mul h_sum1 h_sum2 (by positivity) (by positivity)
        _ = 4 * u ^ 3 := by ring
    have h_uv_diff : 1 ≤ 4 * u ^ 3 * (u - v) := by
      have hm := mul_le_mul_of_nonneg_left h_prod_le (sub_nonneg.mpr hv_le_u)
      linarith [h_diff4, show (u - v) * (4 * u ^ 3) = 4 * u ^ 3 * (u - v) by ring]
    have h_uv_prod : v * u ≤ u ^ 2 := by
      calc
        v * u ≤ u * u := mul_le_mul_of_nonneg_right hv_le_u (le_of_lt hu_pos)
        _ = u ^ 2 := (sq u).symm
    have h_inv_diff : 1 / v - 1 / u = (u - v) / (v * u) := by
      field_simp [ne_of_gt hv_pos, ne_of_gt hu_pos]
    change 1 / u ^ 5 ≤ 4 * (1 / v - 1 / u)
    rw [h_inv_diff]
    have h_step1 : (u - v) / u ^ 2 ≤ (u - v) / (v * u) :=
      div_le_div_of_nonneg_left (sub_nonneg.mpr hv_le_u) (mul_pos hv_pos hu_pos) h_uv_prod
    have h_step2 : 1 / u ^ 5 ≤ 4 * ((u - v) / u ^ 2) := by
      rw [show 4 * ((u - v) / u ^ 2) = (4 * u ^ 3 * (u - v)) / u ^ 5 by
        field_simp [ne_of_gt hu_pos]; ring]
      exact div_le_div_of_nonneg_right h_uv_diff (by positivity)
    linarith
  have h_tel_q : ∀ M : ℕ, (∑ n ∈ Finset.Icc 2 M, (1 / q (n - 1) - 1 / q n)) ≤ 1 := by
    intro M
    by_cases hM0 : M = 0
    · subst hM0; simp
    · obtain ⟨k, rfl⟩ : ∃ k : ℕ, M = k + 1 := ⟨M - 1, by omega⟩
      have h_eq :
          ∀ m : ℕ,
            (∑ n ∈ Finset.Icc 2 (m + 1), (1 / q (n - 1) - 1 / q n)) =
              1 - 1 / q (m + 1) := by
        intro m
        induction' m with m ih
        · simp [q]
        · have h_ins :
              Finset.Icc 2 (m + 1 + 1) = insert (m + 2) (Finset.Icc 2 (m + 1)) := by
            ext r; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
          have h_not : m + 2 ∉ Finset.Icc 2 (m + 1) := by simp
          rw [h_ins, Finset.sum_insert h_not, ih]
          have h_sub : m + 2 - 1 = m + 1 := by omega
          have h_add : m + 1 + 1 = m + 2 := by omega
          rw [h_sub, h_add]
          ring
      rw [h_eq k]
      have h_inv_nn : 0 ≤ 1 / q (k + 1) := by dsimp [q]; positivity
      linarith
  have h_sum_a :
      (∑ a ∈ Finset.Icc 1 T, (1 + Real.log (a : ℝ)) / ((a : ℝ) * Real.sqrt (a : ℝ))) ≤ 17 := by
    have h_sub12 : Finset.Icc 1 T ⊆ ({1} : Finset ℕ) ∪ Finset.Icc 2 T := by
      intro a ha
      rw [Finset.mem_Icc] at ha
      simp only [Finset.mem_union, Finset.mem_singleton, Finset.mem_Icc]
      omega
    have h_d12 : Disjoint ({1} : Finset ℕ) (Finset.Icc 2 T) := by
      rw [Finset.disjoint_left]; intro a h1 h2; simp at h1 h2; omega
    have h_nn :
        ∀ a : ℕ, 0 ≤ (1 + Real.log (a : ℝ)) / ((a : ℝ) * Real.sqrt (a : ℝ)) := by
      intro a
      by_cases ha0 : a = 0
      · simp [ha0]
      · have ha1 : (1 : ℝ) ≤ (a : ℝ) := by exact_mod_cast Nat.pos_of_ne_zero ha0
        exact div_nonneg (by linarith [Real.log_nonneg ha1]) (by positivity)
    have h_u_le :
        (∑ a ∈ Finset.Icc 1 T, (1 + Real.log (a : ℝ)) / ((a : ℝ) * Real.sqrt (a : ℝ))) ≤
          1 + ∑ a ∈ Finset.Icc 2 T, (1 + Real.log (a : ℝ)) / ((a : ℝ) * Real.sqrt (a : ℝ)) := by
      calc
        _ ≤ ∑ a ∈ ({1} : Finset ℕ) ∪ Finset.Icc 2 T,
              (1 + Real.log (a : ℝ)) / ((a : ℝ) * Real.sqrt (a : ℝ)) :=
            Finset.sum_le_sum_of_subset_of_nonneg h_sub12 (fun a _ _ => h_nn a)
        _ = 1 + ∑ a ∈ Finset.Icc 2 T,
              (1 + Real.log (a : ℝ)) / ((a : ℝ) * Real.sqrt (a : ℝ)) := by
            rw [Finset.sum_union h_d12, Finset.sum_singleton]
            simp [Real.log_one]
    have h_each2 :
        ∀ a ∈ Finset.Icc 2 T,
          (1 + Real.log (a : ℝ)) / ((a : ℝ) * Real.sqrt (a : ℝ)) ≤
            16 * (1 / q (a - 1) - 1 / q a) := by
      intro a ha
      have ha2 : 2 ≤ a := (Finset.mem_Icc.mp ha).1
      have ha1 : 1 ≤ a := by omega
      obtain ⟨hq1, _, _, hq6⟩ := hq_props a ha1
      have hq_pos : 0 < q a := lt_of_lt_of_le zero_lt_one hq1
      have hlog_le := (one_add_log_le_four_fourth_root_tc062r_aux (x := (a : ℝ)) (by exact_mod_cast ha1)).1
      have h1 :
          (1 + Real.log (a : ℝ)) / ((a : ℝ) * Real.sqrt (a : ℝ)) ≤ 4 / (q a) ^ 5 := by
        rw [← hq6]
        calc
          (1 + Real.log (a : ℝ)) / (q a) ^ 6 ≤ (4 * q a) / (q a) ^ 6 :=
            div_le_div_of_nonneg_right hlog_le (by positivity)
          _ = 4 / (q a) ^ 5 := by field_simp [ne_of_gt hq_pos]; ring
      have h2 := h_q5_step a ha2
      linarith [h1, h2, show 4 / (q a) ^ 5 = 4 * (1 / (q a) ^ 5) by ring]
    have h_s2 :
        (∑ a ∈ Finset.Icc 2 T, (1 + Real.log (a : ℝ)) / ((a : ℝ) * Real.sqrt (a : ℝ))) ≤ 16 := by
      calc
        _ ≤ ∑ a ∈ Finset.Icc 2 T, 16 * (1 / q (a - 1) - 1 / q a) := Finset.sum_le_sum h_each2
        _ = 16 * ∑ a ∈ Finset.Icc 2 T, (1 / q (a - 1) - 1 / q a) := (Finset.mul_sum _ _ _).symm
        _ ≤ 16 * 1 := mul_le_mul_of_nonneg_left (h_tel_q T) (by norm_num)
        _ = 16 := mul_one _
    linarith
  have h_sum_g :
      (∑ g ∈ Finset.Icc 1 T, (1 + Real.log (g : ℝ)) ^ 2 / (g : ℝ) ^ 2) ≤ 65 := by
    have h_sub12 : Finset.Icc 1 T ⊆ ({1} : Finset ℕ) ∪ Finset.Icc 2 T := by
      intro g hg
      rw [Finset.mem_Icc] at hg
      simp only [Finset.mem_union, Finset.mem_singleton, Finset.mem_Icc]
      omega
    have h_d12 : Disjoint ({1} : Finset ℕ) (Finset.Icc 2 T) := by
      rw [Finset.disjoint_left]; intro g h1 h2; simp at h1 h2; omega
    have h_u_le :
        (∑ g ∈ Finset.Icc 1 T, (1 + Real.log (g : ℝ)) ^ 2 / (g : ℝ) ^ 2) ≤
          1 + ∑ g ∈ Finset.Icc 2 T, (1 + Real.log (g : ℝ)) ^ 2 / (g : ℝ) ^ 2 := by
      calc
        _ ≤ ∑ g ∈ ({1} : Finset ℕ) ∪ Finset.Icc 2 T, (1 + Real.log (g : ℝ)) ^ 2 / (g : ℝ) ^ 2 :=
            Finset.sum_le_sum_of_subset_of_nonneg h_sub12 (fun _ _ _ => by positivity)
        _ = 1 + ∑ g ∈ Finset.Icc 2 T, (1 + Real.log (g : ℝ)) ^ 2 / (g : ℝ) ^ 2 := by
            rw [Finset.sum_union h_d12, Finset.sum_singleton]
            simp [Real.log_one]
    have h_each2 :
        ∀ g ∈ Finset.Icc 2 T,
          (1 + Real.log (g : ℝ)) ^ 2 / (g : ℝ) ^ 2 ≤ 64 * (1 / q (g - 1) - 1 / q g) := by
      intro g hg
      have hg2 : 2 ≤ g := (Finset.mem_Icc.mp hg).1
      have hg1 : 1 ≤ g := by omega
      obtain ⟨hq1, _, hq4, _⟩ := hq_props g hg1
      have hq_pos : 0 < q g := lt_of_lt_of_le zero_lt_one hq1
      have hlog_le := (one_add_log_le_four_fourth_root_tc062r_aux (x := (g : ℝ)) (by exact_mod_cast hg1)).1
      have hlog_nn : 0 ≤ 1 + Real.log (g : ℝ) := by
        linarith [Real.log_nonneg (show (1 : ℝ) ≤ (g : ℝ) by exact_mod_cast hg1)]
      have hsq : (1 + Real.log (g : ℝ)) ^ 2 ≤ (4 * q g) ^ 2 := pow_le_pow_left hlog_nn hlog_le 2
      have hq5_le6 : (q g) ^ 5 ≤ (q g) ^ 6 := by
        have h5 : 0 ≤ (q g) ^ 5 := by positivity
        have heq : (q g) ^ 6 = (q g) ^ 5 * q g := by ring
        rw [heq]
        exact le_mul_of_one_le_right h5 hq1
      have h1 : (1 + Real.log (g : ℝ)) ^ 2 / (g : ℝ) ^ 2 ≤ 16 / (q g) ^ 5 := by
        calc
          (1 + Real.log (g : ℝ)) ^ 2 / (g : ℝ) ^ 2
            = (1 + Real.log (g : ℝ)) ^ 2 / ((q g) ^ 4) ^ 2 := by rw [hq4]
          _ ≤ (4 * q g) ^ 2 / ((q g) ^ 4) ^ 2 :=
              div_le_div_of_nonneg_right hsq (by positivity)
          _ = 16 / (q g) ^ 6 := by field_simp [ne_of_gt hq_pos]; ring
          _ ≤ 16 / (q g) ^ 5 :=
              div_le_div_of_nonneg_left (by norm_num) (pow_pos hq_pos 5) hq5_le6
      have h2 := h_q5_step g hg2
      linarith [h1, h2, show 16 / (q g) ^ 5 = 16 * (1 / (q g) ^ 5) by ring]
    have h_s2 : (∑ g ∈ Finset.Icc 2 T, (1 + Real.log (g : ℝ)) ^ 2 / (g : ℝ) ^ 2) ≤ 64 := by
      calc
        _ ≤ ∑ g ∈ Finset.Icc 2 T, 64 * (1 / q (g - 1) - 1 / q g) := Finset.sum_le_sum h_each2
        _ = 64 * ∑ g ∈ Finset.Icc 2 T, (1 / q (g - 1) - 1 / q g) := (Finset.mul_sum _ _ _).symm
        _ ≤ 64 * 1 := mul_le_mul_of_nonneg_left (h_tel_q T) (by norm_num)
        _ = 64 := mul_one _
    linarith
  let P2 := Finset.Icc 1 T ×ˢ Finset.Icc 1 T
  let P3 := (Finset.Icc 1 T ×ˢ Finset.Icc 1 T) ×ˢ Finset.Icc 1 T
  let phi : ℕ × ℕ → (ℕ × ℕ) × ℕ :=
    fun de => ((Nat.gcd de.1 de.2, de.1 / Nat.gcd de.1 de.2), de.2 / Nat.gcd de.1 de.2)
  let F3 : (ℕ × ℕ) × ℕ → ℝ := fun gab =>
    ((1 + Real.log (gab.1.1 : ℝ)) ^ 2 / (gab.1.1 : ℝ) ^ 2) *
      ((1 + Real.log (gab.1.2 : ℝ)) / ((gab.1.2 : ℝ) * Real.sqrt (gab.1.2 : ℝ))) *
      ((1 + Real.log (gab.2 : ℝ)) / ((gab.2 : ℝ) * Real.sqrt (gab.2 : ℝ)))
  have hF3_nn : ∀ gab ∈ P3, 0 ≤ F3 gab := by
    intro gab hgab
    simp only [P3, Finset.mem_product, Finset.mem_Icc] at hgab
    rcases hgab with ⟨⟨⟨_, _⟩, ⟨ha1, _⟩⟩, ⟨hb1, _⟩⟩
    have hla : 0 ≤ 1 + Real.log (gab.1.2 : ℝ) := by
      linarith [Real.log_nonneg (show (1 : ℝ) ≤ (gab.1.2 : ℝ) by exact_mod_cast ha1)]
    have hlb : 0 ≤ 1 + Real.log (gab.2 : ℝ) := by
      linarith [Real.log_nonneg (show (1 : ℝ) ≤ (gab.2 : ℝ) by exact_mod_cast hb1)]
    dsimp [F3]
    exact mul_nonneg
      (mul_nonneg (div_nonneg (sq_nonneg _) (sq_nonneg _)) (div_nonneg hla (by positivity)))
      (div_nonneg hlb (by positivity))
  have h_phi_sub : P2.image phi ⊆ P3 := by
    intro gab hgab
    rcases Finset.mem_image.mp hgab with ⟨⟨d, e⟩, hde, rfl⟩
    simp only [P2, P3, phi, Finset.mem_product, Finset.mem_Icc] at hde ⊢
    rcases hde with ⟨⟨hd1, hdT⟩, ⟨he1, heT⟩⟩
    have hg_pos : 0 < Nat.gcd d e := Nat.gcd_pos_of_pos_left e hd1
    have hg_dvd_d : Nat.gcd d e ∣ d := Nat.gcd_dvd_left d e
    have hg_dvd_e : Nat.gcd d e ∣ e := Nat.gcd_dvd_right d e
    have hg_le_d : Nat.gcd d e ≤ d := Nat.le_of_dvd hd1 hg_dvd_d
    have hg_le_e : Nat.gcd d e ≤ e := Nat.le_of_dvd he1 hg_dvd_e
    exact ⟨⟨⟨hg_pos, le_trans hg_le_d hdT⟩,
      ⟨Nat.div_pos hg_le_d hg_pos, le_trans (Nat.div_le_self d _) hdT⟩⟩,
      ⟨Nat.div_pos hg_le_e hg_pos, le_trans (Nat.div_le_self e _) heT⟩⟩
  have h_phi_inj : Set.InjOn phi ↑P2 := by
    rintro ⟨d1, e1⟩ h1 ⟨d2, e2⟩ h2 h_eq
    simp only [Finset.mem_coe, P2, Finset.mem_product, Finset.mem_Icc] at h1 h2
    simp only [phi, Prod.mk.injEq] at h_eq
    rcases h_eq with ⟨⟨hg_eq, ha_eq⟩, hb_eq⟩
    have hd1_eq : d1 = Nat.gcd d1 e1 * (d1 / Nat.gcd d1 e1) :=
      (Nat.mul_div_cancel' (Nat.gcd_dvd_left d1 e1)).symm
    have hd2_eq : d2 = Nat.gcd d2 e2 * (d2 / Nat.gcd d2 e2) :=
      (Nat.mul_div_cancel' (Nat.gcd_dvd_left d2 e2)).symm
    have he1_eq : e1 = Nat.gcd d1 e1 * (e1 / Nat.gcd d1 e1) :=
      (Nat.mul_div_cancel' (Nat.gcd_dvd_right d1 e1)).symm
    have he2_eq : e2 = Nat.gcd d2 e2 * (e2 / Nat.gcd d2 e2) :=
      (Nat.mul_div_cancel' (Nat.gcd_dvd_right d2 e2)).symm
    rw [ha_eq, hg_eq] at hd1_eq
    rw [hb_eq, hg_eq] at he1_eq
    exact Prod.ext (hd1_eq.trans hd2_eq.symm) (he1_eq.trans he2_eq.symm)
  have h_term_le :
      ∀ de ∈ P2,
        ((1 + Real.log (de.1 : ℝ)) / Real.sqrt (de.1 : ℝ)) *
          ((1 + Real.log (de.2 : ℝ)) / Real.sqrt (de.2 : ℝ)) /
          (Nat.lcm de.1 de.2 : ℝ) ≤ F3 (phi de) := by
    rintro ⟨d, e⟩ hde
    simp only [P2, Finset.mem_product, Finset.mem_Icc] at hde
    rcases hde with ⟨⟨hd1, _⟩, ⟨he1, _⟩⟩
    let g := Nat.gcd d e
    let a := d / g
    let b := e / g
    have hg_pos : 0 < g := Nat.gcd_pos_of_pos_left e hd1
    have hd_eq : g * a = d := Nat.mul_div_cancel' (Nat.gcd_dvd_left d e)
    have he_eq : g * b = e := Nat.mul_div_cancel' (Nat.gcd_dvd_right d e)
    have ha1 : 1 ≤ a := Nat.div_pos (Nat.le_of_dvd hd1 (Nat.gcd_dvd_left d e)) hg_pos
    have hb1 : 1 ≤ b := Nat.div_pos (Nat.le_of_dvd he1 (Nat.gcd_dvd_right d e)) hg_pos
    have hlcm_eq : Nat.lcm d e = g * a * b := by
      have hm : g * Nat.lcm d e = g * (g * a * b) := by
        calc
          g * Nat.lcm d e = d * e := Nat.gcd_mul_lcm d e
          _ = (g * a) * (g * b) := by rw [← hd_eq, ← he_eq]
          _ = g * (g * a * b) := by ring
      exact Nat.eq_of_mul_eq_mul_left hg_pos hm
    have hg_r : (1 : ℝ) ≤ (g : ℝ) := by exact_mod_cast hg_pos
    have ha_r : (1 : ℝ) ≤ (a : ℝ) := by exact_mod_cast ha1
    have hb_r : (1 : ℝ) ≤ (b : ℝ) := by exact_mod_cast hb1
    have hlg_nn : 0 ≤ Real.log (g : ℝ) := Real.log_nonneg hg_r
    have hla_nn : 0 ≤ Real.log (a : ℝ) := Real.log_nonneg ha_r
    have hlb_nn : 0 ≤ Real.log (b : ℝ) := Real.log_nonneg hb_r
    have h1_d : 1 + Real.log (d : ℝ) ≤ (1 + Real.log (g : ℝ)) * (1 + Real.log (a : ℝ)) := by
      rw [← hd_eq, Nat.cast_mul, Real.log_mul (by positivity) (by positivity)]
      linarith only [mul_nonneg hlg_nn hla_nn,
        show (1 + Real.log (g : ℝ)) * (1 + Real.log (a : ℝ)) -
            (1 + (Real.log (g : ℝ) + Real.log (a : ℝ))) =
          Real.log (g : ℝ) * Real.log (a : ℝ) by ring]
    have h1_e : 1 + Real.log (e : ℝ) ≤ (1 + Real.log (g : ℝ)) * (1 + Real.log (b : ℝ)) := by
      rw [← he_eq, Nat.cast_mul, Real.log_mul (by positivity) (by positivity)]
      linarith only [mul_nonneg hlg_nn hlb_nn,
        show (1 + Real.log (g : ℝ)) * (1 + Real.log (b : ℝ)) -
            (1 + (Real.log (g : ℝ) + Real.log (b : ℝ))) =
          Real.log (g : ℝ) * Real.log (b : ℝ) by ring]
    have hle_nn : 0 ≤ Real.log (e : ℝ) := Real.log_nonneg (by exact_mod_cast he1)
    have h_num :
        (1 + Real.log (d : ℝ)) * (1 + Real.log (e : ℝ)) ≤
          (1 + Real.log (g : ℝ)) ^ 2 * (1 + Real.log (a : ℝ)) * (1 + Real.log (b : ℝ)) := by
      have hm := mul_le_mul h1_d h1_e (by linarith [hle_nn]) (by positivity)
      linarith [hm, show ((1 + Real.log (g : ℝ)) * (1 + Real.log (a : ℝ))) *
          ((1 + Real.log (g : ℝ)) * (1 + Real.log (b : ℝ))) =
        (1 + Real.log (g : ℝ)) ^ 2 * (1 + Real.log (a : ℝ)) * (1 + Real.log (b : ℝ)) by ring]
    have h_den :
        Real.sqrt (d : ℝ) * Real.sqrt (e : ℝ) * (Nat.lcm d e : ℝ) =
          (g : ℝ) ^ 2 * ((a : ℝ) * Real.sqrt (a : ℝ)) * ((b : ℝ) * Real.sqrt (b : ℝ)) := by
      rw [hlcm_eq, ← hd_eq, ← he_eq]
      push_cast
      rw [Real.sqrt_mul (by positivity) (a : ℝ), Real.sqrt_mul (by positivity) (b : ℝ)]
      have hsg : Real.sqrt (g : ℝ) * Real.sqrt (g : ℝ) = (g : ℝ) :=
        Real.mul_self_sqrt (by positivity)
      calc
        Real.sqrt (g : ℝ) * Real.sqrt (a : ℝ) * (Real.sqrt (g : ℝ) * Real.sqrt (b : ℝ)) *
            ((g : ℝ) * (a : ℝ) * (b : ℝ))
          = (Real.sqrt (g : ℝ) * Real.sqrt (g : ℝ)) * (g : ℝ) *
              ((a : ℝ) * Real.sqrt (a : ℝ)) * ((b : ℝ) * Real.sqrt (b : ℝ)) := by ring
        _ = (g : ℝ) ^ 2 * ((a : ℝ) * Real.sqrt (a : ℝ)) * ((b : ℝ) * Real.sqrt (b : ℝ)) := by
            rw [hsg]; ring
    change ((1 + Real.log (d : ℝ)) / Real.sqrt (d : ℝ)) *
        ((1 + Real.log (e : ℝ)) / Real.sqrt (e : ℝ)) / (Nat.lcm d e : ℝ) ≤
      ((1 + Real.log (g : ℝ)) ^ 2 / (g : ℝ) ^ 2) *
        ((1 + Real.log (a : ℝ)) / ((a : ℝ) * Real.sqrt (a : ℝ))) *
        ((1 + Real.log (b : ℝ)) / ((b : ℝ) * Real.sqrt (b : ℝ)))
    have h_lhs_div :
        ((1 + Real.log (d : ℝ)) / Real.sqrt (d : ℝ)) *
            ((1 + Real.log (e : ℝ)) / Real.sqrt (e : ℝ)) / (Nat.lcm d e : ℝ) =
          ((1 + Real.log (d : ℝ)) * (1 + Real.log (e : ℝ))) /
            (Real.sqrt (d : ℝ) * Real.sqrt (e : ℝ) * (Nat.lcm d e : ℝ)) := by ring
    have h_rhs_div :
        ((1 + Real.log (g : ℝ)) ^ 2 / (g : ℝ) ^ 2) *
            ((1 + Real.log (a : ℝ)) / ((a : ℝ) * Real.sqrt (a : ℝ))) *
            ((1 + Real.log (b : ℝ)) / ((b : ℝ) * Real.sqrt (b : ℝ))) =
          ((1 + Real.log (g : ℝ)) ^ 2 * (1 + Real.log (a : ℝ)) * (1 + Real.log (b : ℝ))) /
            ((g : ℝ) ^ 2 * ((a : ℝ) * Real.sqrt (a : ℝ)) * ((b : ℝ) * Real.sqrt (b : ℝ))) := by
      ring
    rw [h_lhs_div, h_rhs_div, h_den]
    exact div_le_div_of_nonneg_right h_num (by positivity)
  have h_P3_fact :
      (∑ gab ∈ P3, F3 gab) =
        (∑ g ∈ Finset.Icc 1 T, (1 + Real.log (g : ℝ)) ^ 2 / (g : ℝ) ^ 2) *
          (∑ a ∈ Finset.Icc 1 T, (1 + Real.log (a : ℝ)) / ((a : ℝ) * Real.sqrt (a : ℝ))) ^ 2 := by
    dsimp [P3, F3]
    rw [Finset.sum_product, Finset.sum_product]
    dsimp only
    simp_rw [mul_assoc, ← Finset.mul_sum, ← Finset.sum_mul]
    ring
  have h_a_nn :
      0 ≤ ∑ a ∈ Finset.Icc 1 T, (1 + Real.log (a : ℝ)) / ((a : ℝ) * Real.sqrt (a : ℝ)) := by
    apply Finset.sum_nonneg
    intro a ha
    have ha1 : (1 : ℝ) ≤ (a : ℝ) := by exact_mod_cast (Finset.mem_Icc.mp ha).1
    exact div_nonneg (by linarith [Real.log_nonneg ha1]) (by positivity)
  calc
    (∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
        ((1 + Real.log (d : ℝ)) / Real.sqrt (d : ℝ)) *
          ((1 + Real.log (e : ℝ)) / Real.sqrt (e : ℝ)) /
          (Nat.lcm d e : ℝ))
      = ∑ de ∈ P2,
          ((1 + Real.log (de.1 : ℝ)) / Real.sqrt (de.1 : ℝ)) *
            ((1 + Real.log (de.2 : ℝ)) / Real.sqrt (de.2 : ℝ)) /
            (Nat.lcm de.1 de.2 : ℝ) := by
          dsimp [P2]; rw [Finset.sum_product]
    _ ≤ ∑ de ∈ P2, F3 (phi de) := Finset.sum_le_sum h_term_le
    _ = ∑ gab ∈ P2.image phi, F3 gab := (Finset.sum_image h_phi_inj).symm
    _ ≤ ∑ gab ∈ P3, F3 gab := Finset.sum_le_sum_of_subset_of_nonneg h_phi_sub (fun x hx _ => hF3_nn x hx)
    _ = (∑ g ∈ Finset.Icc 1 T, (1 + Real.log (g : ℝ)) ^ 2 / (g : ℝ) ^ 2) *
          (∑ a ∈ Finset.Icc 1 T, (1 + Real.log (a : ℝ)) / ((a : ℝ) * Real.sqrt (a : ℝ))) ^ 2 := h_P3_fact
    _ ≤ 65 * 17 ^ 2 := mul_le_mul h_sum_g (pow_le_pow_left h_a_nn h_sum_a 2) (sq_nonneg _) (by norm_num)
    _ = 18785 := by norm_num

private theorem sq_sum_le_card_mul_sum_sq_tc062r_aux (S : Finset ℕ) (f : ℕ → ℝ) :
    (∑ x ∈ S, f x) ^ 2 ≤ (S.card : ℝ) * ∑ x ∈ S, (f x) ^ 2 := by
  have h_nn : 0 ≤ ∑ x ∈ S, ∑ y ∈ S, (f x - f y) ^ 2 :=
    Finset.sum_nonneg (fun _ _ => Finset.sum_nonneg (fun _ _ => sq_nonneg _))
  have h_exp :
      (∑ x ∈ S, ∑ y ∈ S, (f x - f y) ^ 2) =
        2 * ((S.card : ℝ) * ∑ x ∈ S, (f x) ^ 2 - (∑ x ∈ S, f x) ^ 2) := by
    have h_inner :
        ∀ x ∈ S,
          (∑ y ∈ S, (f x - f y) ^ 2) =
            (S.card : ℝ) * (f x) ^ 2 - 2 * f x * (∑ y ∈ S, f y) + ∑ y ∈ S, (f y) ^ 2 := by
      intro x _
      have h1 : ∀ y ∈ S, (f x - f y) ^ 2 = (f x) ^ 2 - 2 * f x * f y + (f y) ^ 2 :=
        fun _ _ => by ring
      rw [Finset.sum_congr rfl h1, Finset.sum_add_distrib, Finset.sum_sub_distrib,
        Finset.sum_const, nsmul_eq_mul, ← Finset.mul_sum]
    rw [Finset.sum_congr rfl h_inner, Finset.sum_add_distrib, Finset.sum_sub_distrib,
      ← Finset.mul_sum, Finset.sum_const, nsmul_eq_mul]
    have h_mid :
        (∑ x ∈ S, 2 * f x * ∑ y ∈ S, f y) = 2 * (∑ x ∈ S, f x) ^ 2 := by
      have h2 : ∀ x ∈ S, 2 * f x * (∑ y ∈ S, f y) = f x * (2 * ∑ y ∈ S, f y) :=
        fun _ _ => by ring
      rw [Finset.sum_congr rfl h2, ← Finset.sum_mul]
      ring
    rw [h_mid]
    ring
  linarith

private theorem openCoreAdjustedCoeffBeta_four_piece_eq_tc062r_aux
    {T : ℕ} (hT2 : 2 ≤ T) (D0 : ℕ) (c_lam c_half : ℝ) {k : ℕ} (hk : k ∈ Finset.Icc 1 T) :
    openCoreAdjustedCoeffBeta c_lam c_half T D0 k =
      -(c_lam * (if IsSquare k then 1 else 0)) -
        (if k = T then selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T else 0) -
        (∑ e ∈ k.divisors,
          (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
            (liouvilleLambda (k / e) : ℝ)) -
        ((∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
              (liouvilleLambda (k / d) : ℝ)) -
          (∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter
              (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
              (liouvilleLambda (k / (d + 1)) : ℝ))) := by
  let D_min := min D0 (T - 1)
  obtain ⟨_, h_alpha_lt, h_alpha_T, _⟩ :=
    (noncircular_reassembly_and_basis_stratification_tc060 c_lam).2.2.2.2 T hT2
  have hk_bds := Finset.mem_Icc.mp hk
  have hk_ne : k ≠ 0 := by omega
  have h_alpha_adj :
      smoothBasisCoeffAlpha c_lam T k -
          truncatedLiouvilleCoeff T k * (Real.log (k : ℝ)) ^ 2 =
        -(c_lam * (if IsSquare k then 1 else 0)) -
          (if k = T then selbergCenteredRemainderInt c_lam T else 0) := by
    have h_tr : truncatedLiouvilleCoeff T k = (liouvilleLambda k : ℝ) := if_pos hk_bds
    rw [h_tr]
    by_cases hkT : k = T
    · subst hkT; rw [h_alpha_T, if_pos rfl]; ring
    · have hk_lt : k ∈ Finset.Icc 1 (T - 1) := Finset.mem_Icc.mpr ⟨hk_bds.1, by omega⟩
      rw [h_alpha_lt k hk_lt, if_neg hkT]; ring
  let driftOp : ℝ :=
    (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
        squarePoleDriftM c_half d * (liouvilleLambda (k / d) : ℝ)) -
      (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
        squarePoleDriftM c_half d * (liouvilleLambda (k / (d + 1)) : ℝ))
  let smallOp : ℝ :=
    (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
        (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
          (liouvilleLambda (k / d) : ℝ)) -
      (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
        (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
          (liouvilleLambda (k / (d + 1)) : ℝ))
  have h_beta_split :
      openCoreAdjustedCoeffBeta c_lam c_half T D0 k =
        (smoothBasisCoeffAlpha c_lam T k -
            truncatedLiouvilleCoeff T k * (Real.log (k : ℝ)) ^ 2) -
          driftOp - smallOp := by
    have h_u : Finset.Icc 1 (T - 1) = Finset.Icc 1 D_min ∪ Finset.Icc (D_min + 1) (T - 1) := by
      ext d; simp only [D_min, Finset.mem_Icc, Finset.mem_union]; omega
    have h_d : Disjoint (Finset.Icc 1 D_min) (Finset.Icc (D_min + 1) (T - 1)) := by
      rw [Finset.disjoint_left]; intro d h1 h2; simp only [Finset.mem_Icc] at h1 h2; omega
    have h_lin :
        ∀ (P : ℕ → Prop) [DecidablePred P] (f : ℕ → ℝ),
          (∑ d ∈ (Finset.Icc 1 (T - 1)).filter P, f d) =
            (∑ d ∈ (Finset.Icc 1 D_min).filter P, f d) +
              (∑ d ∈ (Finset.Icc (D_min + 1) (T - 1)).filter P, f d) := by
      intro P _ f
      conv_lhs => rw [h_u, Finset.filter_union]
      exact Finset.sum_union (Finset.disjoint_filter_filter h_d)
    unfold openCoreAdjustedCoeffBeta openCoreSmoothCoeffS smoothBasisCoeffAlpha
    dsimp [driftOp, smallOp, D_min]
    have h1 := h_lin (fun d => d ∣ k ∧ k / d ≤ T / d)
      (fun d => (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
        (liouvilleLambda (k / d) : ℝ))
    have h2 := h_lin (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d)
      (fun d => (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
        (liouvilleLambda (k / (d + 1)) : ℝ))
    have h_sub1 :
        (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
              (liouvilleLambda (k / d) : ℝ)) =
          (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
              selbergCenteredRemainderInt c_lam d * (liouvilleLambda (k / d) : ℝ)) -
            (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
              squarePoleDriftM c_half d * (liouvilleLambda (k / d) : ℝ)) := by
      rw [← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl; intro d _; ring
    have h_sub2 :
        (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
              (liouvilleLambda (k / (d + 1)) : ℝ)) =
          (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
              selbergCenteredRemainderInt c_lam d * (liouvilleLambda (k / (d + 1)) : ℝ)) -
            (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
              squarePoleDriftM c_half d * (liouvilleLambda (k / (d + 1)) : ℝ)) := by
      rw [← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl; intro d _; ring
    linarith [h1, h2, h_sub1, h_sub2]
  have h_drift_eq :
      driftOp =
        (∑ e ∈ k.divisors,
            (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
              (liouvilleLambda (k / e) : ℝ)) -
          (if k = T then squarePoleDriftM c_half T else 0) := by
    have h_s1 :
        (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
            squarePoleDriftM c_half d * (liouvilleLambda (k / d) : ℝ)) =
          (∑ e ∈ k.divisors,
              squarePoleDriftM c_half e * (liouvilleLambda (k / e) : ℝ)) -
            (if k = T then squarePoleDriftM c_half T else 0) := by
      have hf_eq :
          (Finset.Icc 1 (T - 1)).filter (fun d => d ∣ k ∧ k / d ≤ T / d) =
            k.divisors.erase T := by
        ext d
        simp only [Finset.mem_filter, Finset.mem_Icc, Finset.mem_erase, Nat.mem_divisors]
        constructor
        · rintro ⟨⟨_, hd_hi⟩, ⟨hd_dvd, _⟩⟩
          exact ⟨by omega, ⟨hd_dvd, hk_ne⟩⟩
        · rintro ⟨hd_ne_T, ⟨hd_dvd, _⟩⟩
          have hd_pos : 0 < d := Nat.pos_of_dvd_of_pos hd_dvd hk_bds.1
          have hd_le_k : d ≤ k := Nat.le_of_dvd hk_bds.1 hd_dvd
          exact ⟨⟨hd_pos, by omega⟩, ⟨hd_dvd, Nat.div_le_div_right hk_bds.2⟩⟩
      rw [hf_eq]
      by_cases hkT : k = T
      · rw [hkT]
        have hT_div : T ∈ T.divisors := Nat.mem_divisors.mpr ⟨dvd_refl T, by omega⟩
        have hl1 : (liouvilleLambda (T / T) : ℝ) = 1 := by
          rw [Nat.div_self (by omega)]
          simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
        rw [if_pos rfl, ← Finset.add_sum_erase _ _ hT_div, hl1, mul_one]
        ring
      · have hT_not : T ∉ k.divisors := by
          intro hmem
          have hle := Nat.le_of_dvd hk_bds.1 (Nat.mem_divisors.mp hmem).1
          omega
        rw [if_neg hkT, Finset.erase_eq_of_not_mem hT_not, sub_zero]
    have h_s2 :
        (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
            squarePoleDriftM c_half d * (liouvilleLambda (k / (d + 1)) : ℝ)) =
          ∑ e ∈ k.divisors,
            squarePoleDriftM c_half (e - 1) * (liouvilleLambda (k / e) : ℝ) := by
      have h1_div : 1 ∈ k.divisors := Nat.one_mem_divisors.mpr hk_ne
      have hM0 : squarePoleDriftM c_half 0 = 0 := by simp [squarePoleDriftM]
      rw [← Finset.add_sum_erase _ _ h1_div, Nat.sub_self, hM0, zero_mul, zero_add]
      apply Finset.sum_bij (fun d _ => d + 1)
      · intro d hd
        simp only [Finset.mem_filter, Finset.mem_Icc, Finset.mem_erase, Nat.mem_divisors] at hd ⊢
        exact ⟨by omega, ⟨hd.2.1, hk_ne⟩⟩
      · intro d1 _ d2 _ h; omega
      · intro e he
        simp only [Finset.mem_erase, Nat.mem_divisors] at he
        rcases he with ⟨he_ne1, ⟨he_dvd, _⟩⟩
        have he_pos : 0 < e := Nat.pos_of_dvd_of_pos he_dvd hk_bds.1
        have he_ge2 : 2 ≤ e := by omega
        have he_le_T : e ≤ T := le_trans (Nat.le_of_dvd hk_bds.1 he_dvd) hk_bds.2
        let d := e - 1
        have hd1 : d + 1 = e := by omega
        have h_div_le : k / e ≤ T / d :=
          le_trans (Nat.div_le_div_right hk_bds.2)
            (Nat.div_le_div_left (by omega : d ≤ e) (by omega : 0 < d))
        refine ⟨d, ?_, hd1⟩
        simp only [Finset.mem_filter, Finset.mem_Icc]
        exact ⟨⟨by omega, by omega⟩, ⟨by rwa [hd1], by rwa [hd1]⟩⟩
      · intro d _; simp
    dsimp [driftOp]
    rw [h_s1, h_s2, sub_right_comm, ← Finset.sum_sub_distrib]
    congr 1
    apply Finset.sum_congr rfl
    intro e _
    ring
  rw [h_beta_split, h_alpha_adj, h_drift_eq]
  dsimp [smallOp, D_min]
  split_ifs <;> ring

private theorem sq_mul_div_self_eq_tc062r_aux (a c : ℝ) (ha : a ≠ 0) :
    a ^ 2 * (c / a) = c * a := by
  field_simp [ha]
  ring

private theorem piece2_cancel_alg_tc062r_aux (L4 Tv B w Y5 : ℝ) (hT : Tv ≠ 0) (hL : L4 ≠ 0) :
    (1 / L4) * ((Tv ^ 2 * B ^ 2 * L4) * (w * Y5 / Tv ^ 6)) =
      (B ^ 2 * w) * (Y5 / Tv ^ 4) := by
  field_simp [hT, hL]
  ring

private theorem inv_mul_256_cancel_alg_tc062r_aux (L4 c s : ℝ) (hL : L4 ≠ 0) :
    (1 / L4) * (4 * c * s ^ 2 * (256 * L4)) = 1024 * c * s ^ 2 := by
  field_simp [hL]
  ring

private theorem driftStepDivisor_weighted_windowEnergy_le_tc062r_aux
    (c_half : ℝ) {C_phi Y : ℝ} (hCphi_pos : 0 < C_phi) (hY2 : 2 ≤ Y)
    (h_inv_log4_le16 : 1 / (Real.log Y) ^ 4 ≤ 16)
    (h_phi_mult :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ (T : ℕ) {L : ℕ}, 1 ≤ L →
        (∑ k ∈ (Finset.Icc 1 T).filter (fun k => L ∣ k),
          windowEnergyNormSq Y (gaussianTermPhi k)) ≤ C_phi / (L : ℝ))
    (T : ℕ) :
    (1 / (Real.log Y) ^ 4) *
        (∑ k ∈ Finset.Icc 1 T,
          (-(∑ e ∈ k.divisors,
              (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                (liouvilleLambda (k / e) : ℝ))) ^ 2 *
            windowEnergyNormSq Y (gaussianTermPhi k)) ≤
      16 * (8 + |c_half|) ^ 2 * C_phi * 18785 := by
  let p3 : ℕ → ℝ := fun k =>
    -(∑ e ∈ k.divisors,
        (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
          (liouvilleLambda (k / e) : ℝ))
  have h_phi_nn : ∀ k ∈ Finset.Icc 1 T, 0 ≤ windowEnergyNormSq Y (gaussianTermPhi k) :=
    fun k hk => (gaussianTermPhi_windowEnergy_bounds_tc062r_aux hY2 (Finset.mem_Icc.mp hk).1).1
  let w : ℕ → ℝ := fun e => (1 + Real.log (e : ℝ)) / Real.sqrt (e : ℝ)
  have hw_nn : ∀ e ∈ Finset.Icc 1 T, 0 ≤ w e := by
    intro e he
    have he1 : (1 : ℝ) ≤ (e : ℝ) := by exact_mod_cast (Finset.mem_Icc.mp he).1
    dsimp [w]
    exact div_nonneg (by linarith [Real.log_nonneg he1]) (by positivity)
  have h_p3_sq :
      ∀ k ∈ Finset.Icc 1 T,
        (p3 k) ^ 2 ≤
          (8 + |c_half|) ^ 2 *
            ∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
              (if d ∣ k ∧ e ∣ k then w d * w e else 0) := by
    intro k hk
    have hk_bds := Finset.mem_Icc.mp hk
    have h_div_eq : k.divisors = (Finset.Icc 1 T).filter (fun e => e ∣ k) := by
      ext e
      simp only [Nat.mem_divisors, Finset.mem_filter, Finset.mem_Icc]
      constructor
      · rintro ⟨hd, _⟩
        exact ⟨⟨Nat.pos_of_dvd_of_pos hd hk_bds.1,
          le_trans (Nat.le_of_dvd hk_bds.1 hd) hk_bds.2⟩, hd⟩
      · rintro ⟨_, hd⟩
        exact ⟨hd, by omega⟩
    have habs : |p3 k| ≤ (8 + |c_half|) * ∑ e ∈ k.divisors, w e := by
      dsimp [p3]
      rw [abs_neg]
      calc
        |∑ e ∈ k.divisors,
            (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
              (liouvilleLambda (k / e) : ℝ)|
          ≤ ∑ e ∈ k.divisors,
              |(squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                (liouvilleLambda (k / e) : ℝ)| := Finset.abs_sum_le_sum_abs _ _
        _ ≤ ∑ e ∈ k.divisors, (8 + |c_half|) * w e := by
            apply Finset.sum_le_sum
            intro e he
            have he_dvd := (Nat.mem_divisors.mp he).1
            have he1 : 1 ≤ e := Nat.pos_of_dvd_of_pos he_dvd hk_bds.1
            rw [abs_mul]
            have hlam := abs_liouvilleLambda_le_one_tc062_aux (k / e)
            have hst := squarePoleDriftM_sharp_step_abs_le_tc062r_aux c_half he1
            calc
              |squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)| *
                  |(liouvilleLambda (k / e) : ℝ)|
                ≤ |squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)| * 1 :=
                  mul_le_mul_of_nonneg_left hlam (abs_nonneg _)
              _ ≤ (8 + |c_half|) * (1 + Real.log (e : ℝ)) / Real.sqrt (e : ℝ) := by linarith
              _ = (8 + |c_half|) * w e := by dsimp [w]; ring
        _ = (8 + |c_half|) * ∑ e ∈ k.divisors, w e := (Finset.mul_sum _ _ _).symm
    have hsq1 := pow_le_pow_left (abs_nonneg _) habs 2
    rw [sq_abs, mul_pow, h_div_eq, sq (∑ e ∈ (Finset.Icc 1 T).filter (fun e => e ∣ k), w e),
      Finset.sum_mul_sum] at hsq1
    have h_ite_prod :
        (∑ d ∈ (Finset.Icc 1 T).filter (fun d => d ∣ k),
          ∑ e ∈ (Finset.Icc 1 T).filter (fun e => e ∣ k), w d * w e) =
          ∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
            (if d ∣ k ∧ e ∣ k then w d * w e else 0) := by
      rw [Finset.sum_filter]
      apply Finset.sum_congr rfl
      intro d _
      rw [Finset.sum_filter]
      by_cases hdk : d ∣ k <;> simp [hdk]
    rwa [h_ite_prod] at hsq1
  have h_exch :
      (∑ k ∈ Finset.Icc 1 T,
          (∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
            (if d ∣ k ∧ e ∣ k then w d * w e else 0)) *
            windowEnergyNormSq Y (gaussianTermPhi k)) ≤
        C_phi * 18785 := by
    have h_rw :
        (∑ k ∈ Finset.Icc 1 T,
            (∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
              (if d ∣ k ∧ e ∣ k then w d * w e else 0)) *
              windowEnergyNormSq Y (gaussianTermPhi k)) =
          ∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
            w d * w e *
              (∑ k ∈ (Finset.Icc 1 T).filter (fun k => Nat.lcm d e ∣ k),
                windowEnergyNormSq Y (gaussianTermPhi k)) := by
      simp_rw [Finset.sum_mul]
      trans (∑ d ∈ Finset.Icc 1 T, ∑ k ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
        (if d ∣ k ∧ e ∣ k then w d * w e else 0) *
          windowEnergyNormSq Y (gaussianTermPhi k))
      · exact Finset.sum_comm
      apply Finset.sum_congr rfl
      intro d _
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro e _
      rw [Finset.mul_sum, Finset.sum_filter]
      apply Finset.sum_congr rfl
      intro k _
      by_cases hde : d ∣ k ∧ e ∣ k
      · have hlcm : Nat.lcm d e ∣ k := Nat.lcm_dvd_iff.mpr hde
        rw [if_pos hde, if_pos hlcm, mul_assoc]
      · have hlcm : ¬ Nat.lcm d e ∣ k := fun h => hde (Nat.lcm_dvd_iff.mp h)
        rw [if_neg hde, if_neg hlcm, zero_mul]
    rw [h_rw]
    have h_de_le :
        ∀ d ∈ Finset.Icc 1 T, ∀ e ∈ Finset.Icc 1 T,
          w d * w e *
              (∑ k ∈ (Finset.Icc 1 T).filter (fun k => Nat.lcm d e ∣ k),
                windowEnergyNormSq Y (gaussianTermPhi k)) ≤
            C_phi * (w d * w e / (Nat.lcm d e : ℝ)) := by
      intro d hd e he
      have hd1 : 0 < d := (Finset.mem_Icc.mp hd).1
      have he1 : 0 < e := (Finset.mem_Icc.mp he).1
      have hlcm1 : 1 ≤ Nat.lcm d e := Nat.lcm_pos hd1 he1
      have hm := mul_le_mul_of_nonneg_left (h_phi_mult hY2 T hlcm1)
        (mul_nonneg (hw_nn d hd) (hw_nn e he))
      linarith [hm, show w d * w e * (C_phi / (Nat.lcm d e : ℝ)) =
        C_phi * (w d * w e / (Nat.lcm d e : ℝ)) by ring]
    calc
      (∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
          w d * w e *
            (∑ k ∈ (Finset.Icc 1 T).filter (fun k => Nat.lcm d e ∣ k),
              windowEnergyNormSq Y (gaussianTermPhi k)))
        ≤ ∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
            C_phi * (w d * w e / (Nat.lcm d e : ℝ)) :=
          Finset.sum_le_sum (fun d hd => Finset.sum_le_sum (fun e he => h_de_le d hd e he))
      _ = C_phi * ∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
            w d * w e / (Nat.lcm d e : ℝ) := by
          simp_rw [← Finset.mul_sum]
      _ ≤ C_phi * 18785 :=
          mul_le_mul_of_nonneg_left (lcm_weighted_series_bound_tc062r_aux T)
            (le_of_lt hCphi_pos)
  have hs3 :
      (∑ k ∈ Finset.Icc 1 T, (p3 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) ≤
        (8 + |c_half|) ^ 2 * (C_phi * 18785) := by
    calc
      _ ≤ ∑ k ∈ Finset.Icc 1 T,
            (8 + |c_half|) ^ 2 *
              ((∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
                (if d ∣ k ∧ e ∣ k then w d * w e else 0)) *
                windowEnergyNormSq Y (gaussianTermPhi k)) := by
          apply Finset.sum_le_sum
          intro k hk
          have hm := mul_le_mul_of_nonneg_right (h_p3_sq k hk) (h_phi_nn k hk)
          linarith [hm, show ((8 + |c_half|) ^ 2 *
              ∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
                (if d ∣ k ∧ e ∣ k then w d * w e else 0)) *
              windowEnergyNormSq Y (gaussianTermPhi k) =
            (8 + |c_half|) ^ 2 *
              ((∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
                (if d ∣ k ∧ e ∣ k then w d * w e else 0)) *
                windowEnergyNormSq Y (gaussianTermPhi k)) by ring]
      _ = (8 + |c_half|) ^ 2 *
            ∑ k ∈ Finset.Icc 1 T,
              (∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
                (if d ∣ k ∧ e ∣ k then w d * w e else 0)) *
                windowEnergyNormSq Y (gaussianTermPhi k) := (Finset.mul_sum _ _ _).symm
      _ ≤ (8 + |c_half|) ^ 2 * (C_phi * 18785) :=
          mul_le_mul_of_nonneg_left h_exch (sq_nonneg _)
  calc
    (1 / (Real.log Y) ^ 4) *
        (∑ k ∈ Finset.Icc 1 T, (p3 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k))
      ≤ 16 * ((8 + |c_half|) ^ 2 * (C_phi * 18785)) :=
        mul_le_mul h_inv_log4_le16 hs3
          (Finset.sum_nonneg (fun k hk => mul_nonneg (sq_nonneg _) (h_phi_nn k hk)))
          (by norm_num)
    _ = 16 * (8 + |c_half|) ^ 2 * C_phi * 18785 := by ring

private theorem smallOp_weighted_windowEnergy_le_tc062r_aux
    (c_lam c_half : ℝ) {C_phi Y : ℝ} (hCphi_pos : 0 < C_phi) (hY2 : 2 ≤ Y)
    (hlogY_pos : 0 < Real.log Y)
    (h_phi_mult :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ (T : ℕ) {L : ℕ}, 1 ≤ L →
        (∑ k ∈ (Finset.Icc 1 T).filter (fun k => L ∣ k),
          windowEnergyNormSq Y (gaussianTermPhi k)) ≤ C_phi / (L : ℝ))
    (T D0 : ℕ) (hD0_le_logY : (D0 : ℝ) ≤ Real.log Y) :
    (1 / (Real.log Y) ^ 4) *
        (∑ k ∈ Finset.Icc 1 T,
          (-((∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
                (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                  (liouvilleLambda (k / d) : ℝ)) -
              (∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter
                  (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
                (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                  (liouvilleLambda (k / (d + 1)) : ℝ)))) ^ 2 *
            windowEnergyNormSq Y (gaussianTermPhi k)) ≤
      1024 * C_phi * (4 + |c_lam| + |c_half|) ^ 2 := by
  let D_min := min D0 (T - 1)
  let C_sm : ℝ := 4 + |c_lam| + |c_half|
  let p4 : ℕ → ℝ := fun k =>
    -((∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
          (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
            (liouvilleLambda (k / d) : ℝ)) -
        (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
          (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
            (liouvilleLambda (k / (d + 1)) : ℝ)))
  have h_phi_nn : ∀ k ∈ Finset.Icc 1 T, 0 ≤ windowEnergyNormSq Y (gaussianTermPhi k) :=
    fun k hk => (gaussianTermPhi_windowEnergy_bounds_tc062r_aux hY2 (Finset.mem_Icc.mp hk).1).1
  by_cases hDm0 : D_min = 0
  · have hp4_zero :
        (∑ k ∈ Finset.Icc 1 T, (p4 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) = 0 := by
      apply Finset.sum_eq_zero
      intro k _
      dsimp [p4]
      rw [hDm0]
      simp
    change (1 / (Real.log Y) ^ 4) *
        (∑ k ∈ Finset.Icc 1 T, (p4 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) ≤
      1024 * C_phi * C_sm ^ 2
    rw [hp4_zero, mul_zero]
    dsimp [C_sm]
    positivity
  · have hDm1 : 1 ≤ D_min := by omega
    have hDm_le_D0 : D_min ≤ D0 := min_le_left _ _
    have hDm_le_logY : (D_min : ℝ) ≤ Real.log Y :=
      le_trans (by exact_mod_cast hDm_le_D0) hD0_le_logY
    have hlogY_ge1 : 1 ≤ Real.log Y :=
      le_trans (show (1 : ℝ) ≤ (D_min : ℝ) by exact_mod_cast hDm1) hDm_le_logY
    let L_sm : ℝ := C_sm * (1 + Real.log (D_min : ℝ)) ^ 2
    have hLsm_nn : 0 ≤ L_sm := by dsimp [L_sm, C_sm]; positivity
    have h_w_sm :
        ∀ d ∈ Finset.Icc 1 D_min,
          |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| ≤
            (d : ℝ) * L_sm := by
      intro d hd
      have hd_bds := Finset.mem_Icc.mp hd
      have hw := centered_minus_drift_abs_le_tc062_aux c_lam c_half hd_bds.1 (le_refl d)
      have hlog_d_nn : 0 ≤ Real.log (d : ℝ) := Real.log_nonneg (by exact_mod_cast hd_bds.1)
      have hlog_d_le : Real.log (d : ℝ) ≤ Real.log (D_min : ℝ) :=
        Real.log_le_log (Nat.cast_pos.mpr hd_bds.1) (by exact_mod_cast hd_bds.2)
      have h_q :
          (Real.log (d : ℝ)) ^ 2 + 4 * Real.log (d : ℝ) + |c_lam| + |c_half| ≤ L_sm := by
        dsimp [L_sm, C_sm]
        have hsq := pow_le_pow_left hlog_d_nn hlog_d_le 2
        have hlog_dm_nn : 0 ≤ Real.log (D_min : ℝ) := le_trans hlog_d_nn hlog_d_le
        have h2_nn : 0 ≤ 2 * Real.log (D_min : ℝ) + (Real.log (D_min : ℝ)) ^ 2 :=
          add_nonneg (mul_nonneg (by norm_num) hlog_dm_nn) (sq_nonneg _)
        have h_rem_nn :
            0 ≤ 4 + 3 * (Real.log (D_min : ℝ)) ^ 2 + 4 * Real.log (D_min : ℝ) +
              (|c_lam| + |c_half|) * (2 * Real.log (D_min : ℝ) + (Real.log (D_min : ℝ)) ^ 2) := by
          linarith [sq_nonneg (Real.log (D_min : ℝ)), hlog_dm_nn,
            mul_nonneg (add_nonneg (abs_nonneg c_lam) (abs_nonneg c_half)) h2_nn]
        linarith only [hlog_d_le, hsq, h_rem_nn,
          show (4 + |c_lam| + |c_half|) * (1 + Real.log (D_min : ℝ)) ^ 2 -
              ((Real.log (D_min : ℝ)) ^ 2 + 4 * Real.log (D_min : ℝ) + |c_lam| + |c_half|) =
            4 + 3 * (Real.log (D_min : ℝ)) ^ 2 + 4 * Real.log (D_min : ℝ) +
              (|c_lam| + |c_half|) * (2 * Real.log (D_min : ℝ) + (Real.log (D_min : ℝ)) ^ 2) by
            ring]
      exact le_trans hw (mul_le_mul_of_nonneg_left h_q (Nat.cast_nonneg d))
    have h_p4_sq :
        ∀ k ∈ Finset.Icc 1 T,
          (p4 k) ^ 2 ≤
            2 * (D_min : ℝ) * L_sm ^ 2 *
              ((∑ d ∈ Finset.Icc 1 D_min, if d ∣ k then (d : ℝ) ^ 2 else 0) +
                (∑ d ∈ Finset.Icc 1 D_min, if (d + 1) ∣ k then (d : ℝ) ^ 2 else 0)) := by
      intro k _
      let s1 :=
        ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
          (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
            (liouvilleLambda (k / d) : ℝ)
      let s2 :=
        ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
          (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
            (liouvilleLambda (k / (d + 1)) : ℝ)
      have hs1_abs :
          |s1| ≤ L_sm * ∑ d ∈ Finset.Icc 1 D_min, (if d ∣ k then (d : ℝ) else 0) := by
        calc
          |s1|
            ≤ ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
                |(selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                  (liouvilleLambda (k / d) : ℝ)| := Finset.abs_sum_le_sum_abs _ _
          _ ≤ ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
                (d : ℝ) * L_sm := by
              apply Finset.sum_le_sum
              intro d hd
              have hd_in := (Finset.mem_filter.mp hd).1
              rw [abs_mul]
              exact le_trans
                (mul_le_mul_of_nonneg_left (abs_liouvilleLambda_le_one_tc062_aux _) (abs_nonneg _))
                (by linarith [h_w_sm d hd_in])
          _ ≤ ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k), (d : ℝ) * L_sm := by
              apply Finset.sum_le_sum_of_subset_of_nonneg
              · intro d hd; simp only [Finset.mem_filter] at hd ⊢; exact ⟨hd.1, hd.2.1⟩
              · intro d _ _; exact mul_nonneg (Nat.cast_nonneg d) hLsm_nn
          _ = L_sm * ∑ d ∈ Finset.Icc 1 D_min, (if d ∣ k then (d : ℝ) else 0) := by
              rw [Finset.sum_filter, Finset.mul_sum]
              apply Finset.sum_congr rfl
              intro d _; split_ifs <;> ring
      have hs2_abs :
          |s2| ≤ L_sm * ∑ d ∈ Finset.Icc 1 D_min, (if (d + 1) ∣ k then (d : ℝ) else 0) := by
        calc
          |s2|
            ≤ ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
                |(selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                  (liouvilleLambda (k / (d + 1)) : ℝ)| := Finset.abs_sum_le_sum_abs _ _
          _ ≤ ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
                (d : ℝ) * L_sm := by
              apply Finset.sum_le_sum
              intro d hd
              have hd_in := (Finset.mem_filter.mp hd).1
              rw [abs_mul]
              exact le_trans
                (mul_le_mul_of_nonneg_left (abs_liouvilleLambda_le_one_tc062_aux _) (abs_nonneg _))
                (by linarith [h_w_sm d hd_in])
          _ ≤ ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k), (d : ℝ) * L_sm := by
              apply Finset.sum_le_sum_of_subset_of_nonneg
              · intro d hd; simp only [Finset.mem_filter] at hd ⊢; exact ⟨hd.1, hd.2.1⟩
              · intro d _ _; exact mul_nonneg (Nat.cast_nonneg d) hLsm_nn
          _ = L_sm * ∑ d ∈ Finset.Icc 1 D_min, (if (d + 1) ∣ k then (d : ℝ) else 0) := by
              rw [Finset.sum_filter, Finset.mul_sum]
              apply Finset.sum_congr rfl
              intro d _; split_ifs <;> ring
      have hc_card : ((Finset.Icc 1 D_min).card : ℝ) = (D_min : ℝ) := by
        simp [Nat.card_Icc, show D_min + 1 - 1 = D_min by omega]
      have hcs1 :=
        sq_sum_le_card_mul_sum_sq_tc062r_aux (Finset.Icc 1 D_min)
          (fun d => if d ∣ k then (d : ℝ) else 0)
      have hcs2 :=
        sq_sum_le_card_mul_sum_sq_tc062r_aux (Finset.Icc 1 D_min)
          (fun d => if (d + 1) ∣ k then (d : ℝ) else 0)
      rw [hc_card] at hcs1 hcs2
      have h_ite_sq1 :
          (∑ d ∈ Finset.Icc 1 D_min, (if d ∣ k then (d : ℝ) else 0) ^ 2) =
            ∑ d ∈ Finset.Icc 1 D_min, (if d ∣ k then (d : ℝ) ^ 2 else 0) := by
        apply Finset.sum_congr rfl; intro d _; split_ifs <;> simp
      have h_ite_sq2 :
          (∑ d ∈ Finset.Icc 1 D_min, (if (d + 1) ∣ k then (d : ℝ) else 0) ^ 2) =
            ∑ d ∈ Finset.Icc 1 D_min, (if (d + 1) ∣ k then (d : ℝ) ^ 2 else 0) := by
        apply Finset.sum_congr rfl; intro d _; split_ifs <;> simp
      rw [h_ite_sq1] at hcs1
      rw [h_ite_sq2] at hcs2
      have hs1_sq :
          s1 ^ 2 ≤
            (D_min : ℝ) * L_sm ^ 2 *
              ∑ d ∈ Finset.Icc 1 D_min, (if d ∣ k then (d : ℝ) ^ 2 else 0) := by
        have h1 := pow_le_pow_left (abs_nonneg _) hs1_abs 2
        rw [sq_abs, mul_pow] at h1
        have h2 := mul_le_mul_of_nonneg_left hcs1 (sq_nonneg L_sm)
        linarith [h1, h2, show L_sm ^ 2 * ((D_min : ℝ) *
          ∑ d ∈ Finset.Icc 1 D_min, (if d ∣ k then (d : ℝ) ^ 2 else 0)) =
          (D_min : ℝ) * L_sm ^ 2 *
            ∑ d ∈ Finset.Icc 1 D_min, (if d ∣ k then (d : ℝ) ^ 2 else 0) by ring]
      have hs2_sq :
          s2 ^ 2 ≤
            (D_min : ℝ) * L_sm ^ 2 *
              ∑ d ∈ Finset.Icc 1 D_min, (if (d + 1) ∣ k then (d : ℝ) ^ 2 else 0) := by
        have h1 := pow_le_pow_left (abs_nonneg _) hs2_abs 2
        rw [sq_abs, mul_pow] at h1
        have h2 := mul_le_mul_of_nonneg_left hcs2 (sq_nonneg L_sm)
        linarith [h1, h2, show L_sm ^ 2 * ((D_min : ℝ) *
          ∑ d ∈ Finset.Icc 1 D_min, (if (d + 1) ∣ k then (d : ℝ) ^ 2 else 0)) =
          (D_min : ℝ) * L_sm ^ 2 *
            ∑ d ∈ Finset.Icc 1 D_min, (if (d + 1) ∣ k then (d : ℝ) ^ 2 else 0) by ring]
      have hp4_eq : (p4 k) ^ 2 = (s1 - s2) ^ 2 := by dsimp [p4, s1, s2]; ring
      have h2_sub : (s1 - s2) ^ 2 ≤ 2 * s1 ^ 2 + 2 * s2 ^ 2 := by
        linarith only [sq_nonneg (s1 + s2),
          show 2 * s1 ^ 2 + 2 * s2 ^ 2 - (s1 - s2) ^ 2 = (s1 + s2) ^ 2 by ring]
      rw [hp4_eq]
      linarith
    have h_sum_d1 :
        (∑ k ∈ Finset.Icc 1 T,
            (∑ d ∈ Finset.Icc 1 D_min, if d ∣ k then (d : ℝ) ^ 2 else 0) *
              windowEnergyNormSq Y (gaussianTermPhi k)) ≤
          C_phi * (D_min : ℝ) ^ 2 := by
      simp_rw [Finset.sum_mul]
      rw [Finset.sum_comm]
      have h_each_d :
          ∀ d ∈ Finset.Icc 1 D_min,
            (∑ k ∈ Finset.Icc 1 T,
                (if d ∣ k then (d : ℝ) ^ 2 else 0) *
                  windowEnergyNormSq Y (gaussianTermPhi k)) ≤
              C_phi * (D_min : ℝ) := by
        intro d hd
        have hd_bds := Finset.mem_Icc.mp hd
        have hd_ne : (d : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
        have h_f :
            (∑ k ∈ Finset.Icc 1 T,
                (if d ∣ k then (d : ℝ) ^ 2 else 0) *
                  windowEnergyNormSq Y (gaussianTermPhi k)) =
              (d : ℝ) ^ 2 *
                ∑ k ∈ (Finset.Icc 1 T).filter (fun k => d ∣ k),
                  windowEnergyNormSq Y (gaussianTermPhi k) := by
          rw [Finset.mul_sum, Finset.sum_filter]
          apply Finset.sum_congr rfl; intro k _; split_ifs <;> simp
        rw [h_f]
        calc
          (d : ℝ) ^ 2 *
              ∑ k ∈ (Finset.Icc 1 T).filter (fun k => d ∣ k),
                windowEnergyNormSq Y (gaussianTermPhi k)
            ≤ (d : ℝ) ^ 2 * (C_phi / (d : ℝ)) :=
              mul_le_mul_of_nonneg_left (h_phi_mult hY2 T hd_bds.1) (sq_nonneg _)
          _ = C_phi * (d : ℝ) := sq_mul_div_self_eq_tc062r_aux (d : ℝ) C_phi hd_ne
          _ ≤ C_phi * (D_min : ℝ) :=
              mul_le_mul_of_nonneg_left (by exact_mod_cast hd_bds.2) (le_of_lt hCphi_pos)
      calc
        _ ≤ ∑ _d ∈ Finset.Icc 1 D_min, C_phi * (D_min : ℝ) := Finset.sum_le_sum h_each_d
        _ = C_phi * (D_min : ℝ) ^ 2 := by
            simp [Nat.card_Icc, show D_min + 1 - 1 = D_min by omega]; ring
    have h_sum_d2 :
        (∑ k ∈ Finset.Icc 1 T,
            (∑ d ∈ Finset.Icc 1 D_min, if (d + 1) ∣ k then (d : ℝ) ^ 2 else 0) *
              windowEnergyNormSq Y (gaussianTermPhi k)) ≤
          C_phi * (D_min : ℝ) ^ 2 := by
      simp_rw [Finset.sum_mul]
      rw [Finset.sum_comm]
      have h_each_d :
          ∀ d ∈ Finset.Icc 1 D_min,
            (∑ k ∈ Finset.Icc 1 T,
                (if (d + 1) ∣ k then (d : ℝ) ^ 2 else 0) *
                  windowEnergyNormSq Y (gaussianTermPhi k)) ≤
              C_phi * (D_min : ℝ) := by
        intro d hd
        have hd_bds := Finset.mem_Icc.mp hd
        have hd_pos : (0 : ℝ) < (d : ℝ) := Nat.cast_pos.mpr hd_bds.1
        have hd_ne : (d : ℝ) ≠ 0 := ne_of_gt hd_pos
        have h_f :
            (∑ k ∈ Finset.Icc 1 T,
                (if (d + 1) ∣ k then (d : ℝ) ^ 2 else 0) *
                  windowEnergyNormSq Y (gaussianTermPhi k)) =
              (d : ℝ) ^ 2 *
                ∑ k ∈ (Finset.Icc 1 T).filter (fun k => (d + 1) ∣ k),
                  windowEnergyNormSq Y (gaussianTermPhi k) := by
          rw [Finset.mul_sum, Finset.sum_filter]
          apply Finset.sum_congr rfl; intro k _; split_ifs <;> simp
        rw [h_f]
        have h_d1_le : C_phi / ((d + 1 : ℕ) : ℝ) ≤ C_phi / (d : ℝ) :=
          div_le_div_of_nonneg_left (le_of_lt hCphi_pos) hd_pos
            (by exact_mod_cast Nat.le_succ d)
        calc
          (d : ℝ) ^ 2 *
              ∑ k ∈ (Finset.Icc 1 T).filter (fun k => (d + 1) ∣ k),
                windowEnergyNormSq Y (gaussianTermPhi k)
            ≤ (d : ℝ) ^ 2 * (C_phi / (d : ℝ)) :=
              mul_le_mul_of_nonneg_left
                (le_trans (h_phi_mult hY2 T (by omega : 1 ≤ d + 1)) h_d1_le) (sq_nonneg _)
          _ = C_phi * (d : ℝ) := sq_mul_div_self_eq_tc062r_aux (d : ℝ) C_phi hd_ne
          _ ≤ C_phi * (D_min : ℝ) :=
              mul_le_mul_of_nonneg_left (by exact_mod_cast hd_bds.2) (le_of_lt hCphi_pos)
      calc
        _ ≤ ∑ _d ∈ Finset.Icc 1 D_min, C_phi * (D_min : ℝ) := Finset.sum_le_sum h_each_d
        _ = C_phi * (D_min : ℝ) ^ 2 := by
            simp [Nat.card_Icc, show D_min + 1 - 1 = D_min by omega]; ring
    have hs4 :
        (∑ k ∈ Finset.Icc 1 T, (p4 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) ≤
          4 * C_phi * C_sm ^ 2 * (D_min : ℝ) ^ 3 * (1 + Real.log (D_min : ℝ)) ^ 4 := by
      have h_step :
          (∑ k ∈ Finset.Icc 1 T, (p4 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) ≤
            2 * (D_min : ℝ) * L_sm ^ 2 * (2 * C_phi * (D_min : ℝ) ^ 2) := by
        calc
          _ ≤ ∑ k ∈ Finset.Icc 1 T,
                2 * (D_min : ℝ) * L_sm ^ 2 *
                  (((∑ d ∈ Finset.Icc 1 D_min, if d ∣ k then (d : ℝ) ^ 2 else 0) *
                      windowEnergyNormSq Y (gaussianTermPhi k)) +
                    ((∑ d ∈ Finset.Icc 1 D_min, if (d + 1) ∣ k then (d : ℝ) ^ 2 else 0) *
                      windowEnergyNormSq Y (gaussianTermPhi k))) := by
              apply Finset.sum_le_sum
              intro k hk
              have hm := mul_le_mul_of_nonneg_right (h_p4_sq k hk) (h_phi_nn k hk)
              linarith [hm, show (2 * (D_min : ℝ) * L_sm ^ 2 *
                  ((∑ d ∈ Finset.Icc 1 D_min, if d ∣ k then (d : ℝ) ^ 2 else 0) +
                    (∑ d ∈ Finset.Icc 1 D_min, if (d + 1) ∣ k then (d : ℝ) ^ 2 else 0))) *
                  windowEnergyNormSq Y (gaussianTermPhi k) =
                2 * (D_min : ℝ) * L_sm ^ 2 *
                  (((∑ d ∈ Finset.Icc 1 D_min, if d ∣ k then (d : ℝ) ^ 2 else 0) *
                      windowEnergyNormSq Y (gaussianTermPhi k)) +
                    ((∑ d ∈ Finset.Icc 1 D_min, if (d + 1) ∣ k then (d : ℝ) ^ 2 else 0) *
                      windowEnergyNormSq Y (gaussianTermPhi k))) by ring]
          _ = 2 * (D_min : ℝ) * L_sm ^ 2 *
                ((∑ k ∈ Finset.Icc 1 T,
                    (∑ d ∈ Finset.Icc 1 D_min, if d ∣ k then (d : ℝ) ^ 2 else 0) *
                      windowEnergyNormSq Y (gaussianTermPhi k)) +
                  (∑ k ∈ Finset.Icc 1 T,
                    (∑ d ∈ Finset.Icc 1 D_min, if (d + 1) ∣ k then (d : ℝ) ^ 2 else 0) *
                      windowEnergyNormSq Y (gaussianTermPhi k))) := by
              rw [← Finset.mul_sum, Finset.sum_add_distrib]
          _ ≤ 2 * (D_min : ℝ) * L_sm ^ 2 * (2 * C_phi * (D_min : ℝ) ^ 2) :=
              mul_le_mul_of_nonneg_left (by linarith [h_sum_d1, h_sum_d2]) (by positivity)
      calc
        _ ≤ 2 * (D_min : ℝ) * L_sm ^ 2 * (2 * C_phi * (D_min : ℝ) ^ 2) := h_step
        _ = 4 * C_phi * C_sm ^ 2 * (D_min : ℝ) ^ 3 * (1 + Real.log (D_min : ℝ)) ^ 4 := by
            dsimp [L_sm]; ring
    have h_logDm_le : Real.log (D_min : ℝ) ≤ Real.log (Real.log Y) :=
      Real.log_le_log (Nat.cast_pos.mpr hDm1) hDm_le_logY
    have h_logDm_nn : 0 ≤ 1 + Real.log (D_min : ℝ) := by
      linarith [Real.log_nonneg (show (1 : ℝ) ≤ (D_min : ℝ) by exact_mod_cast hDm1)]
    have h_256 := (one_add_log_le_four_fourth_root_tc062r_aux hlogY_ge1).2
    have h_pow4_log :
        (1 + Real.log (D_min : ℝ)) ^ 4 ≤ 256 * Real.log Y :=
      le_trans (pow_le_pow_left h_logDm_nn (by linarith) 4) h_256
    have h_Dm3 : (D_min : ℝ) ^ 3 ≤ (Real.log Y) ^ 3 :=
      pow_le_pow_left (Nat.cast_nonneg D_min) hDm_le_logY 3
    have h_prod_log4 :
        (D_min : ℝ) ^ 3 * (1 + Real.log (D_min : ℝ)) ^ 4 ≤ 256 * (Real.log Y) ^ 4 := by
      calc
        (D_min : ℝ) ^ 3 * (1 + Real.log (D_min : ℝ)) ^ 4
          ≤ (Real.log Y) ^ 3 * (256 * Real.log Y) :=
            mul_le_mul h_Dm3 h_pow4_log (by positivity) (by positivity)
        _ = 256 * (Real.log Y) ^ 4 := by ring
    change (1 / (Real.log Y) ^ 4) *
        (∑ k ∈ Finset.Icc 1 T, (p4 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) ≤
      1024 * C_phi * C_sm ^ 2
    calc
      (1 / (Real.log Y) ^ 4) *
          (∑ k ∈ Finset.Icc 1 T, (p4 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k))
        ≤ (1 / (Real.log Y) ^ 4) *
            (4 * C_phi * C_sm ^ 2 * ((D_min : ℝ) ^ 3 * (1 + Real.log (D_min : ℝ)) ^ 4)) := by
          have hm := mul_le_mul_of_nonneg_left hs4 (by positivity : 0 ≤ 1 / (Real.log Y) ^ 4)
          linarith [hm, show 4 * C_phi * C_sm ^ 2 * (D_min : ℝ) ^ 3 *
              (1 + Real.log (D_min : ℝ)) ^ 4 =
            4 * C_phi * C_sm ^ 2 * ((D_min : ℝ) ^ 3 * (1 + Real.log (D_min : ℝ)) ^ 4) by ring]
      _ ≤ (1 / (Real.log Y) ^ 4) * (4 * C_phi * C_sm ^ 2 * (256 * (Real.log Y) ^ 4)) :=
          mul_le_mul_of_nonneg_left
            (mul_le_mul_of_nonneg_left h_prod_log4 (by dsimp [C_sm]; positivity))
            (by positivity)
      _ = 1024 * C_phi * C_sm ^ 2 :=
          inv_mul_256_cancel_alg_tc062r_aux ((Real.log Y) ^ 4) C_phi C_sm
            (ne_of_gt (pow_pos hlogY_pos 4))

private theorem canonical_psi_sum_and_diag_abs_bound_tc062r_aux (c_lam c_half : ℝ) :
    ∃ C_psi C_diag : ℝ, 0 ≤ C_psi ∧ 0 ≤ C_diag ∧
      (∀ {Y : ℝ}, 2 ≤ Y →
        (∑ n ∈ Finset.Icc 1 (canonicalCutoffT Y),
          windowEnergyNormSq Y
            (adjustedStationProfilePsi c_lam c_half
              (canonicalCutoffT Y) (Nat.floor (Real.log Y)) n)) ≤ C_psi) ∧
      (∀ {p : ℕ}, p.Prime → ∀ {Y : ℝ}, 2 ≤ Y →
        |canonicalInteriorDiagSigma c_lam c_half p Y| ≤ C_diag) := by
  have htau_bds := tau_gt_one_and_lt_eight_tc062_aux
  have htau_pos : 0 < RiemannScope.tau := by linarith only [htau_bds.1]
  have htau_m1_nn : 0 ≤ RiemannScope.tau - 1 := by linarith only [htau_bds.1]
  let C_phi : ℝ := (RiemannScope.tau - 1) * (27 / 8 + 2 * RiemannScope.tau ^ 4)
  obtain ⟨hCphi_pos, h_phi_mult⟩ := sum_multiples_gaussianTermPhi_windowEnergy_le_tc062r_aux
  let B0 : ℝ := (9 / 4 : ℝ) ^ 2 + 18 + 4 * (|c_lam| + |c_half|)
  let C_sm : ℝ := 4 + |c_lam| + |c_half|
  let C_beta : ℝ :=
    16 * c_lam ^ 2 * C_phi +
      B0 ^ 2 * (RiemannScope.tau - 1) * RiemannScope.tau ^ 4 +
      16 * (8 + |c_half|) ^ 2 * C_phi * 18785 +
      1024 * C_phi * C_sm ^ 2
  let C_psi : ℝ := 2 * C_phi + 8 * C_beta
  let C_diag : ℝ := max (2 * C_psi) (744 * (RiemannScope.tau - 1))
  have hCpsi_nn : 0 ≤ C_psi := by dsimp [C_psi, C_beta, B0, C_sm]; positivity
  have hCdiag_nn : 0 ≤ C_diag := le_trans (mul_nonneg (by norm_num) hCpsi_nn) (le_max_left _ _)
  have h_psi_bd :
      ∀ {Y : ℝ}, 2 ≤ Y →
        (∑ n ∈ Finset.Icc 1 (canonicalCutoffT Y),
          windowEnergyNormSq Y
            (adjustedStationProfilePsi c_lam c_half
              (canonicalCutoffT Y) (Nat.floor (Real.log Y)) n)) ≤ C_psi := by
    intro Y hY2
    obtain ⟨hle, hprops⟩ := uIcc_tau_props_tc062_aux hY2
    obtain ⟨hT2, _, _, hlogT_le, _, hY5_le, hlogY_gt_half⟩ :=
      canonicalCutoffT_bounds_tc062_aux hY2
    let T := canonicalCutoffT Y
    let D0 := Nat.floor (Real.log Y)
    let D_min := min D0 (T - 1)
    have hT1 : 1 ≤ T := by omega
    have hT_pos_r : (0 : ℝ) < (T : ℝ) := by exact_mod_cast (by omega : 0 < T)
    have hlogY_pos : 0 < Real.log Y := by linarith only [hlogY_gt_half]
    have h1_le_2logY : 1 ≤ 2 * Real.log Y := by linarith only [hlogY_gt_half]
    have h1_le_4logY_sq : 1 ≤ 4 * (Real.log Y) ^ 2 := by
      have hsq := pow_le_pow_left (by norm_num) (le_of_lt hlogY_gt_half) 2
      linarith only [hsq]
    have h_inv_log4_le16 : 1 / (Real.log Y) ^ 4 ≤ 16 := by
      have hp4 := pow_le_pow_left (by norm_num) (le_of_lt hlogY_gt_half) 4
      rw [div_le_iff (pow_pos hlogY_pos 4)]
      linarith only [hp4]
    have h_phi_all :
        (∑ k ∈ Finset.Icc 1 T, windowEnergyNormSq Y (gaussianTermPhi k)) ≤ C_phi := by
      have hf1 : (Finset.Icc 1 T).filter (fun k => 1 ∣ k) = Finset.Icc 1 T := by
        ext k; simp
      have h1 := h_phi_mult hY2 T (le_refl 1)
      rw [hf1, Nat.cast_one, div_one] at h1
      exact h1
    have h_each_psi :
        ∀ k ∈ Finset.Icc 1 T,
          windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 k) ≤
            2 * windowEnergyNormSq Y (gaussianTermPhi k) +
              (2 / (Real.log Y) ^ 4) *
                ((openCoreAdjustedCoeffBeta c_lam c_half T D0 k) ^ 2 *
                  windowEnergyNormSq Y (gaussianTermPhi k)) := by
      intro k hk
      have hk1 : 1 ≤ k := (Finset.mem_Icc.mp hk).1
      have hlam_sq := liouvilleLambda_sq_eq_one_tc062_aux hk1
      have h_psi_c := continuousOn_adjustedStationProfilePsi_tc062_aux hY2 c_lam c_half T D0 k
      have h_phi_c := continuousOn_gaussianTermPhi_uIcc_tc062_aux Y k
      have hi_psi :
          IntervalIntegrable
            (fun X =>
              adjustedStationProfilePsi c_lam c_half T D0 k X *
                adjustedStationProfilePsi c_lam c_half T D0 k X / X)
            volume Y (RiemannScope.tau * Y) :=
        ((h_psi_c.mul h_psi_c).div continuousOn_id
          (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
      have hi_phi :
          IntervalIntegrable
            (fun X => gaussianTermPhi k X * gaussianTermPhi k X / X)
            volume Y (RiemannScope.tau * Y) :=
        ((h_phi_c.mul h_phi_c).div continuousOn_id
          (fun X hX => ne_of_gt (hprops X hX).2.1)).intervalIntegrable
      let c_k := 2 + (2 / (Real.log Y) ^ 4) * (openCoreAdjustedCoeffBeta c_lam c_half T D0 k) ^ 2
      have h_mono :=
        intervalIntegral.integral_mono_on hle hi_psi (hi_phi.const_mul c_k) (by
          intro X hX
          have hX_pos : 0 < X := by linarith only [hY2, hX.1]
          have hlogX_ge : Real.log Y ≤ Real.log X :=
            Real.log_le_log (by linarith only [hY2]) hX.1
          have hlogX4_ge : (Real.log Y) ^ 4 ≤ (Real.log X) ^ 4 :=
            pow_le_pow_left (le_of_lt hlogY_pos) hlogX_ge 4
          have hb_sq :
              (signedAdjustedCoeffB c_lam c_half T D0 k) ^ 2 =
                (openCoreAdjustedCoeffBeta c_lam c_half T D0 k) ^ 2 := by
            unfold signedAdjustedCoeffB
            calc
              ((liouvilleLambda k : ℝ) * openCoreAdjustedCoeffBeta c_lam c_half T D0 k) ^ 2
                = ((liouvilleLambda k : ℝ) * (liouvilleLambda k : ℝ)) *
                    (openCoreAdjustedCoeffBeta c_lam c_half T D0 k) ^ 2 := by ring
              _ = (openCoreAdjustedCoeffBeta c_lam c_half T D0 k) ^ 2 := by rw [hlam_sq, one_mul]
          have h_quad :
              (1 - signedAdjustedCoeffB c_lam c_half T D0 k / (Real.log X) ^ 2) ^ 2 ≤ c_k := by
            let v := signedAdjustedCoeffB c_lam c_half T D0 k / (Real.log X) ^ 2
            have h2v : (1 - v) ^ 2 ≤ 2 + 2 * v ^ 2 := by
              linarith only [sq_nonneg (1 + v), show 2 + 2 * v ^ 2 - (1 - v) ^ 2 = (1 + v) ^ 2 by ring]
            have hv2 :
                v ^ 2 ≤ (openCoreAdjustedCoeffBeta c_lam c_half T D0 k) ^ 2 / (Real.log Y) ^ 4 := by
              dsimp [v]
              rw [div_pow, hb_sq, show ((Real.log X) ^ 2) ^ 2 = (Real.log X) ^ 4 by ring]
              exact div_le_div_of_nonneg_left (sq_nonneg _) (pow_pos hlogY_pos 4) hlogX4_ge
            change (1 - v) ^ 2 ≤
              2 + (2 / (Real.log Y) ^ 4) * (openCoreAdjustedCoeffBeta c_lam c_half T D0 k) ^ 2
            linarith only [h2v, hv2,
              show (2 / (Real.log Y) ^ 4) * (openCoreAdjustedCoeffBeta c_lam c_half T D0 k) ^ 2 =
                2 * ((openCoreAdjustedCoeffBeta c_lam c_half T D0 k) ^ 2 / (Real.log Y) ^ 4) by ring]
          unfold adjustedStationProfilePsi
          have h_alg :
              ((1 - signedAdjustedCoeffB c_lam c_half T D0 k / (Real.log X) ^ 2) *
                  gaussianTermPhi k X) *
                ((1 - signedAdjustedCoeffB c_lam c_half T D0 k / (Real.log X) ^ 2) *
                  gaussianTermPhi k X) / X =
                (1 - signedAdjustedCoeffB c_lam c_half T D0 k / (Real.log X) ^ 2) ^ 2 *
                  (gaussianTermPhi k X * gaussianTermPhi k X / X) := by ring
          rw [h_alg]
          exact mul_le_mul_of_nonneg_right h_quad
            (div_nonneg (mul_self_nonneg _) (le_of_lt hX_pos)))
      rw [intervalIntegral.integral_const_mul] at h_mono
      unfold windowEnergyNormSq windowPairing
      dsimp [c_k] at h_mono
      linarith
    -- Bound each of the 4 pieces of beta_k^2 * ||phi_k||_Y^2 / (log Y)^4
    let p1 : ℕ → ℝ := fun k => -(c_lam * (if IsSquare k then 1 else 0))
    let p2 : ℕ → ℝ := fun k =>
      -(if k = T then selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T else 0)
    let p3 : ℕ → ℝ := fun k =>
      -(∑ e ∈ k.divisors,
          (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
            (liouvilleLambda (k / e) : ℝ))
    let p4 : ℕ → ℝ := fun k =>
      -((∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k ∧ k / d ≤ T / d),
            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
              (liouvilleLambda (k / d) : ℝ)) -
          (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
              (liouvilleLambda (k / (d + 1)) : ℝ)))
    have h_four_sq :
        ∀ k ∈ Finset.Icc 1 T,
          (openCoreAdjustedCoeffBeta c_lam c_half T D0 k) ^ 2 ≤
            4 * ((p1 k) ^ 2 + (p2 k) ^ 2 + (p3 k) ^ 2 + (p4 k) ^ 2) := by
      intro k hk
      have heq := openCoreAdjustedCoeffBeta_four_piece_eq_tc062r_aux hT2 D0 c_lam c_half hk
      have h_sum4 : openCoreAdjustedCoeffBeta c_lam c_half T D0 k = p1 k + p2 k + p3 k + p4 k := by
        rw [heq]; dsimp [p1, p2, p3, p4, D_min]; ring
      rw [h_sum4]
      linarith [sq_nonneg (p1 k - p2 k), sq_nonneg (p1 k - p3 k), sq_nonneg (p1 k - p4 k),
        sq_nonneg (p2 k - p3 k), sq_nonneg (p2 k - p4 k), sq_nonneg (p3 k - p4 k),
        show 4 * ((p1 k) ^ 2 + (p2 k) ^ 2 + (p3 k) ^ 2 + (p4 k) ^ 2) -
            (p1 k + p2 k + p3 k + p4 k) ^ 2 =
          (p1 k - p2 k) ^ 2 + (p1 k - p3 k) ^ 2 + (p1 k - p4 k) ^ 2 +
            (p2 k - p3 k) ^ 2 + (p2 k - p4 k) ^ 2 + (p3 k - p4 k) ^ 2 by ring]
    have h_phi_nn : ∀ k ∈ Finset.Icc 1 T, 0 ≤ windowEnergyNormSq Y (gaussianTermPhi k) :=
      fun k hk => (gaussianTermPhi_windowEnergy_bounds_tc062r_aux hY2 (Finset.mem_Icc.mp hk).1).1
    -- Piece 1 bound
    have h_bd_p1 :
        (1 / (Real.log Y) ^ 4) *
            (∑ k ∈ Finset.Icc 1 T, (p1 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) ≤
          16 * c_lam ^ 2 * C_phi := by
      have h_each1 :
          ∀ k ∈ Finset.Icc 1 T,
            (p1 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k) ≤
              c_lam ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k) := by
        intro k hk
        have hp1_le : (p1 k) ^ 2 ≤ c_lam ^ 2 := by
          dsimp [p1]; split_ifs <;> simp [sq_nonneg]
        exact mul_le_mul_of_nonneg_right hp1_le (h_phi_nn k hk)
      have hs1 :
          (∑ k ∈ Finset.Icc 1 T, (p1 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) ≤
            c_lam ^ 2 * C_phi := by
        calc
          _ ≤ ∑ k ∈ Finset.Icc 1 T, c_lam ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k) :=
              Finset.sum_le_sum h_each1
          _ = c_lam ^ 2 * ∑ k ∈ Finset.Icc 1 T, windowEnergyNormSq Y (gaussianTermPhi k) :=
              (Finset.mul_sum _ _ _).symm
          _ ≤ c_lam ^ 2 * C_phi := mul_le_mul_of_nonneg_left h_phi_all (sq_nonneg _)
      calc
        (1 / (Real.log Y) ^ 4) *
            (∑ k ∈ Finset.Icc 1 T, (p1 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k))
          ≤ 16 * (c_lam ^ 2 * C_phi) :=
            mul_le_mul h_inv_log4_le16 hs1
              (Finset.sum_nonneg (fun k hk => mul_nonneg (sq_nonneg _) (h_phi_nn k hk)))
              (by norm_num)
        _ = 16 * c_lam ^ 2 * C_phi := by ring
    -- Piece 2 bound
    have h_bd_p2 :
        (1 / (Real.log Y) ^ 4) *
            (∑ k ∈ Finset.Icc 1 T, (p2 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) ≤
          B0 ^ 2 * (RiemannScope.tau - 1) * RiemannScope.tau ^ 4 := by
      have hT_mem : T ∈ Finset.Icc 1 T := Finset.mem_Icc.mpr ⟨hT1, le_refl T⟩
      have h_only_T :
          (∑ k ∈ Finset.Icc 1 T, (p2 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) =
            (selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T) ^ 2 *
              windowEnergyNormSq Y (gaussianTermPhi T) := by
        rw [← Finset.add_sum_erase _ _ hT_mem]
        have h_er :
            (∑ k ∈ (Finset.Icc 1 T).erase T,
              (p2 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) = 0 := by
          apply Finset.sum_eq_zero
          intro k hk
          dsimp [p2]
          rw [if_neg (Finset.mem_erase.mp hk).1]
          ring
        rw [h_er, add_zero]
        dsimp [p2]
        rw [if_pos rfl]
        ring
      rw [h_only_T]
      have hw_T := centered_minus_drift_abs_le_tc062_aux c_lam c_half hT1 (le_refl T)
      have hlT_nn : 0 ≤ Real.log (T : ℝ) := Real.log_nonneg (by exact_mod_cast hT1)
      have hlT_sq : (Real.log (T : ℝ)) ^ 2 ≤ (9 / 4 : ℝ) ^ 2 * (Real.log Y) ^ 2 := by
        have hp_sq := pow_le_pow_left hlT_nn hlogT_le 2
        linarith only [hp_sq, show ((9 / 4 : ℝ) * Real.log Y) ^ 2 =
          (9 / 4 : ℝ) ^ 2 * (Real.log Y) ^ 2 by ring]
      have hlT_lin : 4 * Real.log (T : ℝ) ≤ 18 * (Real.log Y) ^ 2 := by
        have h1 : 4 * Real.log (T : ℝ) ≤ 9 * Real.log Y := by linarith only [hlogT_le]
        have h2 : 9 * Real.log Y ≤ 9 * (Real.log Y * (2 * Real.log Y)) :=
          mul_le_mul_of_nonneg_left
            (le_mul_of_one_le_right (le_of_lt hlogY_pos) h1_le_2logY) (by norm_num)
        linarith only [h1, h2, show 9 * (Real.log Y * (2 * Real.log Y)) = 18 * (Real.log Y) ^ 2 by ring]
      have h_c_abs : |c_lam| + |c_half| ≤ 4 * (|c_lam| + |c_half|) * (Real.log Y) ^ 2 := by
        have h1 := mul_le_mul_of_nonneg_left h1_le_4logY_sq
          (show 0 ≤ |c_lam| + |c_half| by positivity)
        linarith only [h1, show (|c_lam| + |c_half|) * (4 * (Real.log Y) ^ 2) =
          4 * (|c_lam| + |c_half|) * (Real.log Y) ^ 2 by ring]
      have h_B0_le :
          (Real.log (T : ℝ)) ^ 2 + 4 * Real.log (T : ℝ) + |c_lam| + |c_half| ≤
            B0 * (Real.log Y) ^ 2 := by
        dsimp [B0]
        linarith only [hlT_sq, hlT_lin, h_c_abs]
      have hw_T2 :
          |selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T| ≤
            (T : ℝ) * B0 * (Real.log Y) ^ 2 := by
        calc
          _ ≤ (T : ℝ) * ((Real.log (T : ℝ)) ^ 2 + 4 * Real.log (T : ℝ) + |c_lam| + |c_half|) := hw_T
          _ ≤ (T : ℝ) * (B0 * (Real.log Y) ^ 2) :=
              mul_le_mul_of_nonneg_left h_B0_le (le_of_lt hT_pos_r)
          _ = (T : ℝ) * B0 * (Real.log Y) ^ 2 := by ring
      have hw_sq :
          (selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T) ^ 2 ≤
            (T : ℝ) ^ 2 * B0 ^ 2 * (Real.log Y) ^ 4 := by
        have h1 := pow_le_pow_left (abs_nonneg _) hw_T2 2
        rw [sq_abs] at h1
        linarith only [h1, show ((T : ℝ) * B0 * (Real.log Y) ^ 2) ^ 2 =
          (T : ℝ) ^ 2 * B0 ^ 2 * (Real.log Y) ^ 4 by ring]
      have hphi_T := (gaussianTermPhi_windowEnergy_bounds_tc062r_aux hY2 hT1).2.2
      have hY5_T4 : Y ^ 5 / (T : ℝ) ^ 4 ≤ 1 := (div_le_one (pow_pos hT_pos_r 4)).mpr hY5_le
      calc
        (1 / (Real.log Y) ^ 4) *
            ((selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T) ^ 2 *
              windowEnergyNormSq Y (gaussianTermPhi T))
          ≤ (1 / (Real.log Y) ^ 4) *
              (((T : ℝ) ^ 2 * B0 ^ 2 * (Real.log Y) ^ 4) *
                ((RiemannScope.tau - 1) * RiemannScope.tau ^ 4 * Y ^ 5 / (T : ℝ) ^ 6)) :=
            mul_le_mul_of_nonneg_left
              (mul_le_mul hw_sq hphi_T (h_phi_nn T hT_mem) (by dsimp [B0]; positivity))
              (by positivity)
        _ = (B0 ^ 2 * (RiemannScope.tau - 1) * RiemannScope.tau ^ 4) * (Y ^ 5 / (T : ℝ) ^ 4) := by
            rw [piece2_cancel_alg_tc062r_aux ((Real.log Y) ^ 4) (T : ℝ) B0
              ((RiemannScope.tau - 1) * RiemannScope.tau ^ 4) (Y ^ 5)
              (ne_of_gt hT_pos_r) (ne_of_gt (pow_pos hlogY_pos 4))]
            ring
        _ ≤ (B0 ^ 2 * (RiemannScope.tau - 1) * RiemannScope.tau ^ 4) * 1 :=
            mul_le_mul_of_nonneg_left hY5_T4 (by dsimp [B0]; positivity)
        _ = B0 ^ 2 * (RiemannScope.tau - 1) * RiemannScope.tau ^ 4 := mul_one _
    -- Piece 3 bound
    have h_bd_p3 :
        (1 / (Real.log Y) ^ 4) *
            (∑ k ∈ Finset.Icc 1 T, (p3 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) ≤
          16 * (8 + |c_half|) ^ 2 * C_phi * 18785 :=
      driftStepDivisor_weighted_windowEnergy_le_tc062r_aux c_half hCphi_pos hY2
        h_inv_log4_le16 h_phi_mult T
    -- Piece 4 bound
    have hD0_le_logY : (D0 : ℝ) ≤ Real.log Y := Nat.floor_le (le_of_lt hlogY_pos)
    have h_bd_p4 :
        (1 / (Real.log Y) ^ 4) *
            (∑ k ∈ Finset.Icc 1 T, (p4 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) ≤
          1024 * C_phi * C_sm ^ 2 :=
      smallOp_weighted_windowEnergy_le_tc062r_aux c_lam c_half hCphi_pos hY2
        hlogY_pos h_phi_mult T D0 hD0_le_logY
    -- Combine all 4 pieces into C_psi
    have h_beta_tot :
        (1 / (Real.log Y) ^ 4) *
            (∑ k ∈ Finset.Icc 1 T,
              (openCoreAdjustedCoeffBeta c_lam c_half T D0 k) ^ 2 *
                windowEnergyNormSq Y (gaussianTermPhi k)) ≤
          4 * C_beta := by
      have h_sum_4 :
          (∑ k ∈ Finset.Icc 1 T,
              (openCoreAdjustedCoeffBeta c_lam c_half T D0 k) ^ 2 *
                windowEnergyNormSq Y (gaussianTermPhi k)) ≤
            4 * ((∑ k ∈ Finset.Icc 1 T, (p1 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) +
              (∑ k ∈ Finset.Icc 1 T, (p2 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) +
              (∑ k ∈ Finset.Icc 1 T, (p3 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) +
              (∑ k ∈ Finset.Icc 1 T, (p4 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k))) := by
        rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib, ← Finset.sum_add_distrib,
          Finset.mul_sum]
        apply Finset.sum_le_sum
        intro k hk
        have hm := mul_le_mul_of_nonneg_right (h_four_sq k hk) (h_phi_nn k hk)
        linarith [hm, show 4 * ((p1 k) ^ 2 + (p2 k) ^ 2 + (p3 k) ^ 2 + (p4 k) ^ 2) *
            windowEnergyNormSq Y (gaussianTermPhi k) =
          4 * ((p1 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k) +
            (p2 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k) +
            (p3 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k) +
            (p4 k) ^ 2 * windowEnergyNormSq Y (gaussianTermPhi k)) by ring]
      have hm := mul_le_mul_of_nonneg_left h_sum_4 (by positivity : 0 ≤ 1 / (Real.log Y) ^ 4)
      dsimp [C_beta]
      linarith [hm, h_bd_p1, h_bd_p2, h_bd_p3, h_bd_p4]
    have h_psi_sum := Finset.sum_le_sum h_each_psi
    rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum] at h_psi_sum
    have h_alg_2 :
        (2 / (Real.log Y) ^ 4) *
            (∑ i ∈ Finset.Icc 1 T,
              (openCoreAdjustedCoeffBeta c_lam c_half T D0 i) ^ 2 *
                windowEnergyNormSq Y (gaussianTermPhi i)) =
          2 * ((1 / (Real.log Y) ^ 4) *
            (∑ i ∈ Finset.Icc 1 T,
              (openCoreAdjustedCoeffBeta c_lam c_half T D0 i) ^ 2 *
                windowEnergyNormSq Y (gaussianTermPhi i))) := by ring
    rw [h_alg_2] at h_psi_sum
    calc
      (∑ n ∈ Finset.Icc 1 (canonicalCutoffT Y),
          windowEnergyNormSq Y
            (adjustedStationProfilePsi c_lam c_half
              (canonicalCutoffT Y) (Nat.floor (Real.log Y)) n))
        ≤ 2 * (∑ i ∈ Finset.Icc 1 T, windowEnergyNormSq Y (gaussianTermPhi i)) +
            2 * ((1 / (Real.log Y) ^ 4) *
              (∑ i ∈ Finset.Icc 1 T,
                (openCoreAdjustedCoeffBeta c_lam c_half T D0 i) ^ 2 *
                  windowEnergyNormSq Y (gaussianTermPhi i))) := h_psi_sum
      _ ≤ 2 * C_phi + 2 * (4 * C_beta) :=
          add_le_add
            (mul_le_mul_of_nonneg_left h_phi_all (by norm_num))
            (mul_le_mul_of_nonneg_left h_beta_tot (by norm_num))
      _ = C_psi := by dsimp [C_psi]; ring
  refine ⟨C_psi, C_diag, hCpsi_nn, hCdiag_nn, h_psi_bd, ?_⟩
  intro p hp Y hY2
  have hT1 : 1 ≤ canonicalCutoffT Y := canonicalCutoffT_ge_one_tc062_aux (by linarith only [hY2])
  have h_ub_sigma :
      canonicalInteriorDiagSigma c_lam c_half p Y ≤ 2 * C_psi := by
    have h_a1p :=
      (stage_a_interior_hilbert_split_and_candidate_a1_refutation_tc062).2.2 hp hY2 hT1
        (Nat.floor (Real.log Y)) c_lam c_half
    have h_psi := h_psi_bd hY2
    unfold canonicalInteriorDiagSigma interiorAnchorDiagSigma
    exact le_trans h_a1p (mul_le_mul_of_nonneg_left h_psi (by norm_num))
  have h_lb_sigma :
      -744 * (RiemannScope.tau - 1) ≤ canonicalInteriorDiagSigma c_lam c_half p Y := by
    obtain ⟨h1, h2⟩ :=
      interiorAnchorDiagSigma_lower_bound_tc062r_aux hp hY2 hT1
        (Nat.floor (Real.log Y)) c_lam c_half
    unfold canonicalInteriorDiagSigma
    exact le_trans h1 h2
  apply abs_le.mpr
  refine ⟨?_, le_trans h_ub_sigma (le_max_left _ _)⟩
  have h_max_r : 744 * (RiemannScope.tau - 1) ≤ C_diag := le_max_right _ _
  linarith only [h_lb_sigma, h_max_r]

private theorem mixedCovarianceClosure_of_bounded_diff_tc062r_aux
    {F1 F2 D : ℝ → ℝ} {C_bd : ℝ} (hC_nn : 0 ≤ C_bd)
    (h_diff : ∀ {Y : ℝ}, 2 ≤ Y → F2 Y ≤ F1 Y + C_bd) :
    MixedCovarianceClosureHypothesis F1 D → MixedCovarianceClosureHypothesis F2 D := by
  intro hF1 η hη
  obtain ⟨a_eta, b_eta, κ_eta, Y_eta, ha, hb, hκ_pos, hκ_le2, hYe, hF1_bd⟩ := hF1 η hη
  refine ⟨a_eta + C_bd, b_eta, κ_eta, Y_eta,
    add_nonneg ha hC_nn, hb, hκ_pos, hκ_le2, hYe, ?_⟩
  intro Y hYYe
  have hY2 : 2 ≤ Y := le_trans hYe hYYe
  have h1_rpow : 1 ≤ Y ^ η := Real.one_le_rpow (by linarith only [hY2]) (le_of_lt hη)
  have hC_rpow : C_bd ≤ C_bd * Y ^ η := by
    calc
      C_bd = C_bd * 1 := (mul_one _).symm
      _ ≤ C_bd * Y ^ η := mul_le_mul_of_nonneg_left h1_rpow hC_nn
  have h1 := h_diff hY2
  have h2 := hF1_bd Y hYYe
  linarith [show (a_eta + C_bd) * Y ^ η = a_eta * Y ^ η + C_bd * Y ^ η by ring]

private theorem interior_iff_offdiag_closure_hypothesis_tc062r_aux
    {p : ℕ} (hp : p.Prime) (c_lam c_half : ℝ) :
    MixedCovarianceClosureHypothesis
        (canonicalInteriorPairedRemainderF c_lam c_half p) canonicalPrimePowerDiagDtilde ↔
      MixedCovarianceClosureHypothesis
        (canonicalInteriorOffDiagSigma c_lam c_half p) canonicalPrimePowerDiagDtilde := by
  obtain ⟨_, C_diag, _, hCdiag_nn, _, h_diag_abs⟩ :=
    canonical_psi_sum_and_diag_abs_bound_tc062r_aux c_lam c_half
  have h_split :
      ∀ Y : ℝ,
        canonicalInteriorPairedRemainderF c_lam c_half p Y =
          canonicalInteriorDiagSigma c_lam c_half p Y +
            canonicalInteriorOffDiagSigma c_lam c_half p Y :=
    fun Y =>
      (interiorPairedRemainderF_diag_offdiag_split_tc062r_aux c_lam c_half p
        (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y).1
  constructor
  · apply mixedCovarianceClosure_of_bounded_diff_tc062r_aux hCdiag_nn
    intro Y hY2
    have habs := (abs_le.mp (h_diag_abs hp hY2)).1
    linarith [h_split Y]
  · apply mixedCovarianceClosure_of_bounded_diff_tc062r_aux hCdiag_nn
    intro Y hY2
    have habs := (abs_le.mp (h_diag_abs hp hY2)).2
    linarith [h_split Y]

/-- **Theorem 8 (`TASK-TC-062R` §3, §7A, §7D, Exact `Σ_diag + Σ_off` Interior Split, Repaired General-Anchor Diagonal Identities, Unconditional Two-Sided `O(1)` Bound on `canonicalInteriorDiagSigma`, Two-Way Closure Equivalence onto `canonicalInteriorOffDiagSigma`, and Conditional Route D Transfer)**:
    1. *Exact `F_{int,T} = Σ_diag + Σ_off` decomposition & off-diagonal product-filter form*:
       `interiorPairedRemainderF = interiorAnchorDiagSigma + interiorAnchorOffDiagSigma` for all
       parameters, with `interiorAnchorOffDiagSigma` equal to the sum over distinct pairs `m ≠ n` in
       `primeInteriorTruncatedAnchors p T ×ˢ primeInteriorTruncatedAnchors p T`;
    2. *Exact `commonPrimePowerLogSq` shift laws (`c(m, p*m) = c(m, m)`, `c(p*m, p*m) = c(m, m) + (log p)^2`) and both exact anchor-diagonal identities (`hp : p.Prime`, `2 ≤ Y`, `1 ≤ m`, `p * m ≤ T`)*:
       Both the combined `(log m)^2, (log(p*m))^2` identity and the repaired general-anchor `c_self`
       identity retaining `-4 * commonPrimePowerLogSq m m * (G^[2](m, m) - 2 * G^[2](m, p*m) + G^[2](p*m, p*m))`;
    3. *Uniform lower bound on `interiorAnchorDiagSigma` (`hp : p.Prime`, `2 ≤ Y`, `1 ≤ T`)*:
       `-744 * (RiemannScope.tau - 1) ≤ -4 * ∑_{n=1}^T (log n)^2 G^[2](n, n) ≤ interiorAnchorDiagSigma`;
    4. *Sharp `1/sqrt(d)` square-pole drift step bound, shifted `gaussianTermPhi` window-energy bound `≤ C_phi / L`, uniform `lcm` mean-square series bound `C_lcm`, and unconditional two-sided `O(1)` bound `|canonicalInteriorDiagSigma c_lam c_half p Y| ≤ C_diag`* (retaining all 4 components of `openCoreAdjustedCoeffBeta` on `1 ≤ k ≤ T` without any pointwise `(log n)^2` assumption);
    5. *Full chain of unconditional two-way `MixedCovarianceClosureHypothesis` equivalences onto `canonicalInteriorOffDiagSigma` (`TC062-OBL-INTERIOR-PRIME-PAIR-OFFDIAG`) and conditional Route D transfer to `canonicalLiouvilleEnergyE Y ≤ C_tot * Y ^ ε`*. -/
theorem two_sided_interior_diag_bound_and_offdiag_equivalence_tc062r :
    ((∀ (c_lam c_half : ℝ) (p T D0 : ℕ) (Y : ℝ),
        interiorPairedRemainderF c_lam c_half p T D0 Y =
            interiorAnchorDiagSigma c_lam c_half p T D0 Y +
              interiorAnchorOffDiagSigma c_lam c_half p T D0 Y ∧
          interiorAnchorOffDiagSigma c_lam c_half p T D0 Y =
            ∑ mn ∈ (primeInteriorTruncatedAnchors p T ×ˢ primeInteriorTruncatedAnchors p T).filter
                (fun mn => mn.1 ≠ mn.2),
              (liouvilleLambda mn.1 : ℝ) * (liouvilleLambda mn.2 : ℝ) *
                (completeSignedKernelHcal c_lam c_half T D0 Y mn.1 mn.2 -
                  completeSignedKernelHcal c_lam c_half T D0 Y (p * mn.1) mn.2 -
                  completeSignedKernelHcal c_lam c_half T D0 Y mn.1 (p * mn.2) +
                  completeSignedKernelHcal c_lam c_half T D0 Y (p * mn.1) (p * mn.2))) ∧
      (∀ (c_lam c_half : ℝ) (p : ℕ) (Y : ℝ),
        canonicalInteriorPairedRemainderF c_lam c_half p Y =
          canonicalInteriorDiagSigma c_lam c_half p Y +
            canonicalInteriorOffDiagSigma c_lam c_half p Y)) ∧
    (∀ {p : ℕ}, p.Prime →
      (∀ {m : ℕ}, 1 ≤ m →
        commonPrimePowerLogSq m (p * m) = commonPrimePowerLogSq m m ∧
          commonPrimePowerLogSq (p * m) (p * m) =
            commonPrimePowerLogSq m m + (Real.log (p : ℝ)) ^ 2) ∧
        (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T m : ℕ}, 1 ≤ m → p * m ≤ T →
          ∀ (D0 : ℕ) (c_lam c_half : ℝ),
            (completeSignedKernelHcal c_lam c_half T D0 Y m m -
                completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
                completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
                completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m) =
              windowEnergyNormSq Y
                  (fun X =>
                    adjustedStationProfilePsi c_lam c_half T D0 m X -
                      adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) -
                4 * (Real.log (m : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y m m -
                4 * (Real.log ((p * m : ℕ) : ℝ)) ^ 2 *
                  logWeightedWindowKernel 2 Y (p * m) (p * m) +
                8 * commonPrimePowerLogSq m m * logWeightedWindowKernel 2 Y m (p * m)) ∧
              (completeSignedKernelHcal c_lam c_half T D0 Y m m -
                  completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
                  completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
                  completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m) =
                windowEnergyNormSq Y
                    (fun X =>
                      adjustedStationProfilePsi c_lam c_half T D0 m X -
                        adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) -
                  4 * (Real.log (p : ℝ)) ^ 2 *
                    logWeightedWindowKernel 2 Y (p * m) (p * m) -
                  4 * offDiagPrimePowerWeight m m * logWeightedWindowKernel 2 Y m m -
                  4 * offDiagPrimePowerWeight (p * m) (p * m) *
                    logWeightedWindowKernel 2 Y (p * m) (p * m) -
                  4 * commonPrimePowerLogSq m m *
                    (logWeightedWindowKernel 2 Y m m -
                      2 * logWeightedWindowKernel 2 Y m (p * m) +
                      logWeightedWindowKernel 2 Y (p * m) (p * m))))) ∧
    (∀ {p : ℕ}, p.Prime → ∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T →
      ∀ (D0 : ℕ) (c_lam c_half : ℝ),
        -744 * (RiemannScope.tau - 1) ≤
            -4 * (∑ n ∈ Finset.Icc 1 T,
              (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n) ∧
          -4 * (∑ n ∈ Finset.Icc 1 T,
              (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n) ≤
            interiorAnchorDiagSigma c_lam c_half p T D0 Y) ∧
    ((∀ (c_half : ℝ) {d : ℕ}, 1 ≤ d →
        |squarePoleDriftM c_half d - squarePoleDriftM c_half (d - 1)| ≤
          (8 + |c_half|) * (1 + Real.log (d : ℝ)) / Real.sqrt (d : ℝ)) ∧
      (∃ C_phi : ℝ, 0 < C_phi ∧
        ∀ {Y : ℝ}, 2 ≤ Y → ∀ (T : ℕ) {L : ℕ}, 1 ≤ L →
          (∑ k ∈ (Finset.Icc 1 T).filter (fun k => L ∣ k),
            windowEnergyNormSq Y (gaussianTermPhi k)) ≤ C_phi / (L : ℝ)) ∧
      (∃ C_lcm : ℝ, 0 ≤ C_lcm ∧
        ∀ (T : ℕ),
          (∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
            ((1 + Real.log (d : ℝ)) / Real.sqrt (d : ℝ)) *
              ((1 + Real.log (e : ℝ)) / Real.sqrt (e : ℝ)) /
              (Nat.lcm d e : ℝ)) ≤ C_lcm) ∧
      (∀ (c_lam c_half : ℝ),
        ∃ C_psi C_diag : ℝ, 0 ≤ C_psi ∧ 0 ≤ C_diag ∧
          (∀ {Y : ℝ}, 2 ≤ Y →
            (∑ n ∈ Finset.Icc 1 (canonicalCutoffT Y),
              windowEnergyNormSq Y
                (adjustedStationProfilePsi c_lam c_half
                  (canonicalCutoffT Y) (Nat.floor (Real.log Y)) n)) ≤ C_psi) ∧
          (∀ {p : ℕ}, p.Prime → ∀ {Y : ℝ}, 2 ≤ Y →
            |canonicalInteriorDiagSigma c_lam c_half p Y| ≤ C_diag))) ∧
    (∀ {p : ℕ}, p.Prime →
      ((∀ (c_lam c_half : ℝ),
          (MixedCovarianceClosureHypothesis
              (canonicalInteriorPairedRemainderF c_lam c_half p)
              canonicalPrimePowerDiagDtilde ↔
            MixedCovarianceClosureHypothesis
              (canonicalInteriorOffDiagSigma c_lam c_half p)
              canonicalPrimePowerDiagDtilde) ∧
          (MixedCovarianceClosureHypothesis
              (canonicalTruncatedSignedRemainderF c_lam c_half)
              canonicalPrimePowerDiagDtilde ↔
            MixedCovarianceClosureHypothesis
              (canonicalInteriorOffDiagSigma c_lam c_half p)
              canonicalPrimePowerDiagDtilde) ∧
          (MixedCovarianceClosureHypothesis
              (canonicalSignedRemainderF c_lam c_half)
              canonicalPrimePowerDiagDtilde ↔
            MixedCovarianceClosureHypothesis
              (canonicalInteriorOffDiagSigma c_lam c_half p)
              canonicalPrimePowerDiagDtilde) ∧
          (MixedCovarianceClosureHypothesis
              (canonicalSignedMixedCovarianceJ c_lam c_half)
              canonicalPrimePowerDiagDtilde ↔
            MixedCovarianceClosureHypothesis
              (canonicalInteriorOffDiagSigma c_lam c_half p)
              canonicalPrimePowerDiagDtilde)) ∧
        ((MixedCovarianceClosureHypothesis
              (canonicalSignedMixedCovarianceJ
                actualSelbergConstantCLam actualSquarePoleConstantCHalf)
              canonicalPrimePowerDiagDtilde ↔
            MixedCovarianceClosureHypothesis
              (canonicalInteriorOffDiagSigma
                actualSelbergConstantCLam actualSquarePoleConstantCHalf p)
              canonicalPrimePowerDiagDtilde) ∧
          (MixedCovarianceClosureHypothesis
              (canonicalSignedRemainderF
                actualSelbergConstantCLam actualSquarePoleConstantCHalf)
              canonicalPrimePowerDiagDtilde ↔
            MixedCovarianceClosureHypothesis
              (canonicalInteriorOffDiagSigma
                actualSelbergConstantCLam actualSquarePoleConstantCHalf p)
              canonicalPrimePowerDiagDtilde) ∧
          (MixedCovarianceClosureHypothesis
              (canonicalInteriorPairedRemainderF
                actualSelbergConstantCLam actualSquarePoleConstantCHalf p)
              canonicalPrimePowerDiagDtilde ↔
            MixedCovarianceClosureHypothesis
              (canonicalInteriorOffDiagSigma
                actualSelbergConstantCLam actualSquarePoleConstantCHalf p)
              canonicalPrimePowerDiagDtilde))) ∧
      (∀ {M_lin : ℝ},
        0 ≤ M_lin →
        (∀ Z : ℝ, 1 ≤ Z → canonicalLiouvilleEnergyE Z ≤ M_lin * Z) →
        MixedCovarianceClosureHypothesis
          (canonicalInteriorOffDiagSigma
            actualSelbergConstantCLam actualSquarePoleConstantCHalf p)
          canonicalPrimePowerDiagDtilde →
        (∀ ε : ℝ, 0 < ε →
          ∃ zeta2_eps C_cut Y_diag a_known B_drift κ_d : ℝ,
            0 ≤ zeta2_eps ∧ 0 ≤ C_cut ∧ Real.exp 1 ≤ Y_diag ∧
              0 ≤ a_known ∧ 0 ≤ B_drift ∧ 0 < κ_d ∧
              (∀ Y : ℝ, 1 ≤ Y →
                (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
                  (Real.log (pk.1 : ℝ)) ^ 2 / (primePowerScale pk) ^ (1 + ε)) ≤ zeta2_eps) ∧
              (∀ Y : ℝ, Y_diag ≤ Y →
                canonicalPrimePowerDiagDtilde Y ≤
                  (2 / (Real.log Y) ^ 2) *
                    (∑ pk ∈ primePowerPairsUpTo (Nat.floor Y),
                      primePowerDiagWeight pk *
                        monotoneScaleEnvelope canonicalLiouvilleEnergyE (Y / primePowerScale pk)) +
                    C_cut) ∧
              (∀ R Y : ℝ, Y_diag ≤ Y → Y ≤ R →
                windowEnergyNormSq Y
                    (knownCompensatedD2Part
                      actualSelbergConstantCLam actualSquarePoleConstantCHalf
                      (canonicalCutoffT Y) (Nat.floor (Real.log Y))) ≤
                  a_known * Y ^ (ε / 4) +
                    (B_drift / (Real.log Y) ^ κ_d) *
                      normalizedScaleSupremum canonicalLiouvilleEnergyE ε R * Y ^ ε)) →
        ∀ ε : ℝ, 0 < ε →
          ∃ C_tot : ℝ, 0 ≤ C_tot ∧ ∀ Y : ℝ, 1 ≤ Y → canonicalLiouvilleEnergyE Y ≤ C_tot * Y ^ ε)) := by
  have h_part1 :
      (∀ (c_lam c_half : ℝ) (p T D0 : ℕ) (Y : ℝ),
        interiorPairedRemainderF c_lam c_half p T D0 Y =
            interiorAnchorDiagSigma c_lam c_half p T D0 Y +
              interiorAnchorOffDiagSigma c_lam c_half p T D0 Y ∧
          interiorAnchorOffDiagSigma c_lam c_half p T D0 Y =
            ∑ mn ∈ (primeInteriorTruncatedAnchors p T ×ˢ primeInteriorTruncatedAnchors p T).filter
                (fun mn => mn.1 ≠ mn.2),
              (liouvilleLambda mn.1 : ℝ) * (liouvilleLambda mn.2 : ℝ) *
                (completeSignedKernelHcal c_lam c_half T D0 Y mn.1 mn.2 -
                  completeSignedKernelHcal c_lam c_half T D0 Y (p * mn.1) mn.2 -
                  completeSignedKernelHcal c_lam c_half T D0 Y mn.1 (p * mn.2) +
                  completeSignedKernelHcal c_lam c_half T D0 Y (p * mn.1) (p * mn.2))) ∧
      (∀ (c_lam c_half : ℝ) (p : ℕ) (Y : ℝ),
        canonicalInteriorPairedRemainderF c_lam c_half p Y =
          canonicalInteriorDiagSigma c_lam c_half p Y +
            canonicalInteriorOffDiagSigma c_lam c_half p Y) := by
    refine ⟨interiorPairedRemainderF_diag_offdiag_split_tc062r_aux, ?_⟩
    intro c_lam c_half p Y
    exact (interiorPairedRemainderF_diag_offdiag_split_tc062r_aux c_lam c_half p
      (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y).1
  have h_part2 :
      ∀ {p : ℕ}, p.Prime →
        (∀ {m : ℕ}, 1 ≤ m →
          commonPrimePowerLogSq m (p * m) = commonPrimePowerLogSq m m ∧
            commonPrimePowerLogSq (p * m) (p * m) =
              commonPrimePowerLogSq m m + (Real.log (p : ℝ)) ^ 2) ∧
          (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T m : ℕ}, 1 ≤ m → p * m ≤ T →
            ∀ (D0 : ℕ) (c_lam c_half : ℝ),
              (completeSignedKernelHcal c_lam c_half T D0 Y m m -
                  completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
                  completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
                  completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m) =
                windowEnergyNormSq Y
                    (fun X =>
                      adjustedStationProfilePsi c_lam c_half T D0 m X -
                        adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) -
                  4 * (Real.log (m : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y m m -
                  4 * (Real.log ((p * m : ℕ) : ℝ)) ^ 2 *
                    logWeightedWindowKernel 2 Y (p * m) (p * m) +
                  8 * commonPrimePowerLogSq m m * logWeightedWindowKernel 2 Y m (p * m)) ∧
                (completeSignedKernelHcal c_lam c_half T D0 Y m m -
                    completeSignedKernelHcal c_lam c_half T D0 Y (p * m) m -
                    completeSignedKernelHcal c_lam c_half T D0 Y m (p * m) +
                    completeSignedKernelHcal c_lam c_half T D0 Y (p * m) (p * m) =
                  windowEnergyNormSq Y
                      (fun X =>
                        adjustedStationProfilePsi c_lam c_half T D0 m X -
                          adjustedStationProfilePsi c_lam c_half T D0 (p * m) X) -
                    4 * (Real.log (p : ℝ)) ^ 2 *
                      logWeightedWindowKernel 2 Y (p * m) (p * m) -
                    4 * offDiagPrimePowerWeight m m * logWeightedWindowKernel 2 Y m m -
                    4 * offDiagPrimePowerWeight (p * m) (p * m) *
                      logWeightedWindowKernel 2 Y (p * m) (p * m) -
                    4 * commonPrimePowerLogSq m m *
                      (logWeightedWindowKernel 2 Y m m -
                        2 * logWeightedWindowKernel 2 Y m (p * m) +
                        logWeightedWindowKernel 2 Y (p * m) (p * m)))) := by
    intro p hp
    refine ⟨?_, ?_⟩
    · intro m hm1
      exact commonPrimePowerLogSq_prime_mul_identities_tc062r_aux hp hm1
    · intro Y hY2 T m hm1 hpmT D0 c_lam c_half
      exact anchor_diagonal_hcal_identities_tc062r_aux hp hY2 hm1 hpmT D0 c_lam c_half
  have h_part3 :
      ∀ {p : ℕ}, p.Prime → ∀ {Y : ℝ}, 2 ≤ Y → ∀ {T : ℕ}, 1 ≤ T →
        ∀ (D0 : ℕ) (c_lam c_half : ℝ),
          -744 * (RiemannScope.tau - 1) ≤
              -4 * (∑ n ∈ Finset.Icc 1 T,
                (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n) ∧
            -4 * (∑ n ∈ Finset.Icc 1 T,
                (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n) ≤
              interiorAnchorDiagSigma c_lam c_half p T D0 Y := by
    intro p hp Y hY2 T hT D0 c_lam c_half
    exact interiorAnchorDiagSigma_lower_bound_tc062r_aux hp hY2 hT D0 c_lam c_half
  have h_part4 :
      (∀ (c_half : ℝ) {d : ℕ}, 1 ≤ d →
        |squarePoleDriftM c_half d - squarePoleDriftM c_half (d - 1)| ≤
          (8 + |c_half|) * (1 + Real.log (d : ℝ)) / Real.sqrt (d : ℝ)) ∧
      (∃ C_phi : ℝ, 0 < C_phi ∧
        ∀ {Y : ℝ}, 2 ≤ Y → ∀ (T : ℕ) {L : ℕ}, 1 ≤ L →
          (∑ k ∈ (Finset.Icc 1 T).filter (fun k => L ∣ k),
            windowEnergyNormSq Y (gaussianTermPhi k)) ≤ C_phi / (L : ℝ)) ∧
      (∃ C_lcm : ℝ, 0 ≤ C_lcm ∧
        ∀ (T : ℕ),
          (∑ d ∈ Finset.Icc 1 T, ∑ e ∈ Finset.Icc 1 T,
            ((1 + Real.log (d : ℝ)) / Real.sqrt (d : ℝ)) *
              ((1 + Real.log (e : ℝ)) / Real.sqrt (e : ℝ)) /
              (Nat.lcm d e : ℝ)) ≤ C_lcm) ∧
      (∀ (c_lam c_half : ℝ),
        ∃ C_psi C_diag : ℝ, 0 ≤ C_psi ∧ 0 ≤ C_diag ∧
          (∀ {Y : ℝ}, 2 ≤ Y →
            (∑ n ∈ Finset.Icc 1 (canonicalCutoffT Y),
              windowEnergyNormSq Y
                (adjustedStationProfilePsi c_lam c_half
                  (canonicalCutoffT Y) (Nat.floor (Real.log Y)) n)) ≤ C_psi) ∧
          (∀ {p : ℕ}, p.Prime → ∀ {Y : ℝ}, 2 ≤ Y →
            |canonicalInteriorDiagSigma c_lam c_half p Y| ≤ C_diag)) := by
    obtain ⟨hCphi_pos, h_phi_mult⟩ := sum_multiples_gaussianTermPhi_windowEnergy_le_tc062r_aux
    exact ⟨squarePoleDriftM_sharp_step_abs_le_tc062r_aux,
      ⟨_, hCphi_pos, h_phi_mult⟩,
      ⟨18785, by norm_num, lcm_weighted_series_bound_tc062r_aux⟩,
      canonical_psi_sum_and_diag_abs_bound_tc062r_aux⟩
  refine ⟨h_part1, h_part2, h_part3, h_part4, ?_⟩
  intro p hp
  have h_tc062 := interior_prime_pair_closure_equivalence_and_route_d_transfer_tc062 hp
  have h_eqv_all :
      ∀ (c_lam c_half : ℝ),
        (MixedCovarianceClosureHypothesis
            (canonicalInteriorPairedRemainderF c_lam c_half p)
            canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalInteriorOffDiagSigma c_lam c_half p)
            canonicalPrimePowerDiagDtilde) ∧
        (MixedCovarianceClosureHypothesis
            (canonicalTruncatedSignedRemainderF c_lam c_half)
            canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalInteriorOffDiagSigma c_lam c_half p)
            canonicalPrimePowerDiagDtilde) ∧
        (MixedCovarianceClosureHypothesis
            (canonicalSignedRemainderF c_lam c_half)
            canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalInteriorOffDiagSigma c_lam c_half p)
            canonicalPrimePowerDiagDtilde) ∧
        (MixedCovarianceClosureHypothesis
            (canonicalSignedMixedCovarianceJ c_lam c_half)
            canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalInteriorOffDiagSigma c_lam c_half p)
            canonicalPrimePowerDiagDtilde) := by
    intro c_lam c_half
    have h_IO := interior_iff_offdiag_closure_hypothesis_tc062r_aux hp c_lam c_half
    obtain ⟨h_JI, h_FI, h_TI⟩ := h_tc062.2.1.1 c_lam c_half
    exact ⟨h_IO, h_TI.trans h_IO, h_FI.trans h_IO, h_JI.trans h_IO⟩
  have h_act := h_eqv_all actualSelbergConstantCLam actualSquarePoleConstantCHalf
  refine ⟨⟨h_eqv_all, ⟨h_act.2.2.2, h_act.2.2.1, h_act.1⟩⟩, ?_⟩
  intro M_lin hM_nn hE_lin h_off_hyp h_route_d_inputs
  exact h_tc062.2.2 hM_nn hE_lin (h_act.1.mpr h_off_hyp) h_route_d_inputs

end JointPrimeDilationSignedRemainder
end RiemannScope
