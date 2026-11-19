/-
RiemannScope.DyadicChainCorrelationRegularity
TASK-TC-063 (EPIC-TC-042 / SUBGATE-TC-043A):
Dyadic-Chain Correlations and the Arithmetic Regularity Constraint.

Formalizes in Lean 4 (complete machine-checked proofs using canonical circle constant
RiemannScope.tau throughout; complex arguments written z = (x : ℂ) + (y : ℂ) * Complex.I
with real coordinates x, y and critical line x = 1 / 2):
1. `liouville_dirichlet_ratio_pole_contradiction_and_reflection_tc063`
2. `exact_odd_part_bijection_and_dyadic_chain_offdiag_split_tc063`
3. `uniform_same_chain_hilbert_bound_and_closure_transfer_tc063`
4. `odd_common_factor_primitive_regrouping_and_feature_decoupling_tc063`
5. `odd_square_projection_selberg_split_and_sign_extension_obstruction_tc063`
-/

import Mathlib.NumberTheory.LSeries.Dirichlet
import Mathlib.Analysis.SpecialFunctions.Gamma.Deligne
import Mathlib.Analysis.Complex.CauchyIntegral
import Mathlib.Analysis.Analytic.IsolatedZeros
import Mathlib.Analysis.Convex.Basic
import RiemannScope.JointPrimeDilationSignedRemainder

open scoped ArithmeticFunction BigOperators
open MeasureTheory intervalIntegral

namespace RiemannScope

open RiemannScope.LiouvilleSquareDilation
open RiemannScope.DyadicPowerLiftPrimitiveCorrelation hiding canonicalPrimePowerDiagDtilde
open RiemannScope.SignedDilationArithmeticEnergy
open RiemannScope.MixedArithmeticCovariance
open RiemannScope.JointPrimeDilationSignedRemainder

/-! ### Core Definitions (`TASK-TC-063`) -/

/-- Odd chain-root index set `O(T) := {u ∈ [1, T] : Odd u ∧ 2 * u ≤ T}`. -/
def oddChainParts (T : ℕ) : Finset ℕ :=
  (Finset.Icc 1 T).filter (fun u => Odd u ∧ 2 * u ≤ T)

/-- Dyadic `4^j`-chain exponent set `J_u(T) := {j < T + 1 : 2 * 4^j * u ≤ T}`. -/
def dyadicChainExponents (u T : ℕ) : Finset ℕ :=
  (Finset.range (T + 1)).filter (fun j => 2 * 4 ^ j * u ≤ T)

/-- Maximum dyadic `4^j`-chain length `L(T) := max_{u ∈ O(T)} |J_u(T)|`. -/
def maxDyadicChainLength (T : ℕ) : ℕ :=
  (oddChainParts T).sup (fun u => (dyadicChainExponents u T).card)

/-- Complete-kernel 4-term dyadic difference `Δ_{2,2} Hcal_Y(m, n)` on anchors `(m, n)`. -/
noncomputable def anchorFourTermDiffHcal (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ)
    (m n : ℕ) : ℝ :=
  completeSignedKernelHcal c_lam c_half T D0 Y m n -
    completeSignedKernelHcal c_lam c_half T D0 Y (2 * m) n -
    completeSignedKernelHcal c_lam c_half T D0 Y m (2 * n) +
    completeSignedKernelHcal c_lam c_half T D0 Y (2 * m) (2 * n)

/-- Grouped dyadic-chain interaction kernel `Hcal_chain(u, v)` summed over `J_u(T) × J_v(T)`. -/
noncomputable def oddChainGroupedKernel (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ)
    (u v : ℕ) : ℝ :=
  ∑ j ∈ dyadicChainExponents u T,
    ∑ k ∈ dyadicChainExponents v T,
      anchorFourTermDiffHcal c_lam c_half T D0 Y (4 ^ j * u) (4 ^ k * v)

/-- Same-odd-chain distinct-exponent off-diagonal sum `S_same(T, D0, Y)`. -/
noncomputable def sameOddChainSumS (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ) : ℝ :=
  ∑ u ∈ oddChainParts T,
    ∑ j ∈ dyadicChainExponents u T,
      ∑ k ∈ (dyadicChainExponents u T).erase j,
        anchorFourTermDiffHcal c_lam c_half T D0 Y (4 ^ j * u) (4 ^ k * u)

/-- Canonical-schedule (`T = canonicalCutoffT Y`, `D0 = ⌊log Y⌋`) same-odd-chain sum. -/
noncomputable def canonicalSameOddChainSumS (c_lam c_half : ℝ) (Y : ℝ) : ℝ :=
  sameOddChainSumS c_lam c_half (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y

/-- Different-odd-chain (`u ≠ v`) Liouville-signed correlation sum `S_diff(T, D0, Y)`. -/
noncomputable def differentOddChainSumS (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ) : ℝ :=
  ∑ u ∈ oddChainParts T,
    ∑ v ∈ (oddChainParts T).erase u,
      (liouvilleLambda u : ℝ) * (liouvilleLambda v : ℝ) *
        oddChainGroupedKernel c_lam c_half T D0 Y u v

/-- Canonical-schedule (`T = canonicalCutoffT Y`, `D0 = ⌊log Y⌋`) different-odd-chain sum. -/
noncomputable def canonicalDifferentOddChainSumS (c_lam c_half : ℝ) (Y : ℝ) : ℝ :=
  differentOddChainSumS c_lam c_half (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y

/-- Station-level prime-power divisibility feature `g_{n, (p, k)}(X)`. -/
noncomputable def stationPrimePowerFeatureG (n : ℕ) (pk : ℕ × ℕ) (X : ℝ) : ℝ :=
  if pk.1 ^ pk.2 ∣ n then Real.log (pk.1 : ℝ) * gaussianTermPhi n X / Real.log X else 0

/-- Dyadic-anchor adjusted station difference `U_m(X) := ψ_m(X) - ψ_{2m}(X)`. -/
noncomputable def stationAdjustedDiffU (c_lam c_half : ℝ) (T D0 m : ℕ) (X : ℝ) : ℝ :=
  adjustedStationProfilePsi c_lam c_half T D0 m X -
    adjustedStationProfilePsi c_lam c_half T D0 (2 * m) X

/-- Dyadic-anchor prime-power feature difference `V_{m, pk}(X) := g_{m, pk}(X) - g_{2m, pk}(X)`. -/
noncomputable def stationFeatureDiffV (m : ℕ) (pk : ℕ × ℕ) (X : ℝ) : ℝ :=
  stationPrimePowerFeatureG m pk X - stationPrimePowerFeatureG (2 * m) pk X

/-- Odd common-factor `gcd` index set `G_odd(T) := {g ∈ [1, T] : Odd g ∧ 6 * g ≤ T}`. -/
def oddCommonFactorGcdSet (T : ℕ) : Finset ℕ :=
  (Finset.Icc 1 T).filter (fun g => Odd g ∧ 6 * g ≤ T)

/-- Distinct coprime odd chain-root pairs in `O(⌊T / g⌋) × O(⌊T / g⌋)`. -/
def primitiveOddChainPairs (T g : ℕ) : Finset (ℕ × ℕ) :=
  (oddChainParts (T / g) ×ˢ oddChainParts (T / g)).filter
    (fun rt => rt.1 ≠ rt.2 ∧ Nat.Coprime rt.1 rt.2)

/-- Primitive coprime odd-chain correlation sector `Π_odd(T, D0, Y; g)` at odd `gcd` `g`. -/
noncomputable def primitiveOddChainSectorPi (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ)
    (g : ℕ) : ℝ :=
  ∑ rt ∈ primitiveOddChainPairs T g,
    (liouvilleLambda rt.1 : ℝ) * (liouvilleLambda rt.2 : ℝ) *
      oddChainGroupedKernel c_lam c_half T D0 Y (g * rt.1) (g * rt.2)

/-- Complete dyadic-chain grouped adjusted profile `Ucal_u(X) := ∑_{j ∈ J_u(T)} U_{4^j u}(X)`. -/
noncomputable def oddChainAdjustedProfileUcal (c_lam c_half : ℝ) (T D0 u : ℕ) (X : ℝ) : ℝ :=
  ∑ j ∈ dyadicChainExponents u T, stationAdjustedDiffU c_lam c_half T D0 (4 ^ j * u) X

/-- Odd-dilated grouped Liouville chain sum `Gcal_d(X)` over `u ∈ O(⌊T / d⌋)`. -/
noncomputable def dilatedOddChainSumGcal (c_lam c_half : ℝ) (T D0 d : ℕ) (X : ℝ) : ℝ :=
  ∑ u ∈ oddChainParts (T / d),
    (liouvilleLambda u : ℝ) * oddChainAdjustedProfileUcal c_lam c_half T D0 (d * u) X

/-! ### Section 1: Liouville Dirichlet Ratio, Pole Contradiction, and Strip Reflection (`TASK-TC-063` §2) -/

open scoped Classical

private theorem complex_re_im_coord_tc063_aux (x y : ℝ) :
    (((x : ℂ) + (y : ℂ) * Complex.I).re = x) ∧
      (((x : ℂ) + (y : ℂ) * Complex.I).im = y) ∧
      ((2 * ((x : ℂ) + (y : ℂ) * Complex.I)).re = 2 * x) := by
  simp [Complex.add_re, Complex.mul_re, Complex.add_im, Complex.mul_im]

private theorem liouville_lseries_mul_zeta_eq_zeta_two_tc063_aux {x y : ℝ} (hx : 1 < x) :
    let z : ℂ := (x : ℂ) + (y : ℂ) * Complex.I
    riemannZeta z ≠ 0 ∧
      riemannZeta (2 * z) ≠ 0 ∧
      LSeries (fun n => if n = 0 then 0 else (liouvilleLambda n : ℂ)) z * riemannZeta z =
        riemannZeta (2 * z) := by
  intro z
  have hz_re : 1 < z.re := by
    change 1 < ((x : ℂ) + (y : ℂ) * Complex.I).re
    rw [(complex_re_im_coord_tc063_aux x y).1]
    exact hx
  have h2z_re : 1 < (2 * z).re := by
    change 1 < (2 * ((x : ℂ) + (y : ℂ) * Complex.I)).re
    rw [(complex_re_im_coord_tc063_aux x y).2.2]
    linarith
  have hzeta_ne : riemannZeta z ≠ 0 := riemannZeta_ne_zero_of_one_lt_re hz_re
  have hzeta2_ne : riemannZeta (2 * z) ≠ 0 := riemannZeta_ne_zero_of_one_lt_re h2z_re
  refine ⟨hzeta_ne, hzeta2_ne, ?_⟩
  let f_lam : ℕ → ℂ := fun n => if n = 0 then 0 else (liouvilleLambda n : ℂ)
  have hf_bdd : ∀ n : ℕ, n ≠ 0 → Complex.abs (f_lam n) ≤ 1 := by
    intro n hn
    dsimp [f_lam]
    rw [if_neg hn]
    simp only [liouvilleLambda, hn, ↓reduceIte, liouvilleSignFromOmega]
    push_cast
    simp
  have hf_sum : LSeriesSummable f_lam z :=
    LSeriesSummable_of_bounded_of_one_lt_re hf_bdd hz_re
  have h1_sum : LSeriesSummable 1 z := LSeriesSummable_one_iff.mpr hz_re
  rw [← LSeries_one_eq_riemannZeta hz_re, ← LSeries_convolution' hf_sum h1_sum]
  let g_sq : ℕ → ℂ := fun n => if n = 0 then 0 else if IsSquare n then 1 else 0
  have h_conv_eq : ∀ n : ℕ, n ≠ 0 → LSeries.convolution f_lam 1 n = g_sq n := by
    intro n hn
    rw [LSeries.convolution_def]
    dsimp [f_lam, g_sq]
    rw [if_neg hn]
    have h_anti :
        (∑ p ∈ n.divisorsAntidiagonal,
            (if p.1 = 0 then (0 : ℂ) else (liouvilleLambda p.1 : ℂ)) * 1) =
          ∑ d ∈ n.divisors, (liouvilleLambda d : ℂ) := by
      rw [Nat.sum_divisorsAntidiagonal (fun a _b =>
        (if a = 0 then (0 : ℂ) else (liouvilleLambda a : ℂ)) * 1)]
      apply Finset.sum_congr rfl
      intro d hd
      have hd_ne : d ≠ 0 :=
        ne_of_gt (Nat.pos_of_dvd_of_pos (Nat.mem_divisors.mp hd).1 (Nat.pos_of_ne_zero hn))
      rw [if_neg hd_ne, mul_one]
    rw [h_anti]
    have h_ind :=
      (liouville_square_divisor_indicator_and_compensated_selberg_tc058 1 0).1
        n (Nat.pos_of_ne_zero hn)
    have h_cast :
        (∑ d ∈ n.divisors, (liouvilleLambda d : ℂ)) =
          ((∑ d ∈ n.divisors, liouvilleLambda d : ℤ) : ℂ) := by
      push_cast; rfl
    rw [h_cast, h_ind]
    split_ifs <;> simp
  have h_term_eq : LSeries.term (LSeries.convolution f_lam 1) z = LSeries.term g_sq z := by
    ext n
    by_cases hn : n = 0
    · subst hn; simp [LSeries.term]
    · simp [LSeries.term, hn, h_conv_eq n hn]
  unfold LSeries
  rw [h_term_eq]
  let sq_map : ℕ → ℕ := fun m => (m + 1) ^ 2
  have h_inj : Function.Injective sq_map := by
    intro m1 m2 h_eq
    dsimp [sq_map] at h_eq
    have hs1 : Nat.sqrt ((m1 + 1) ^ 2) = m1 + 1 := by rw [sq, Nat.sqrt_eq]
    have hs2 : Nat.sqrt ((m2 + 1) ^ 2) = m2 + 1 := by rw [sq, Nat.sqrt_eq]
    have h12 : m1 + 1 = m2 + 1 := by rw [← hs1, ← hs2, h_eq]
    omega
  have h_supp : Function.support (LSeries.term g_sq z) ⊆ Set.range sq_map := by
    intro n hn_supp
    rw [Function.mem_support] at hn_supp
    by_contra hn_not
    apply hn_supp
    by_cases hn0 : n = 0
    · subst hn0; simp [LSeries.term]
    · have h_not_sq : ¬ IsSquare n := by
        intro hsq
        obtain ⟨r, rfl⟩ := hsq
        have hr_ne : r ≠ 0 := fun hr0 => hn0 (by rw [hr0, mul_zero])
        apply hn_not
        refine ⟨r - 1, ?_⟩
        dsimp [sq_map]
        rw [Nat.sub_add_cancel (Nat.pos_of_ne_zero hr_ne), sq]
      simp [LSeries.term, g_sq, hn0, h_not_sq]
  rw [← h_inj.tsum_eq h_supp, zeta_eq_tsum_one_div_nat_add_one_cpow h2z_re]
  congr 1
  ext m
  have hm_sq_ne : (m + 1) ^ 2 ≠ 0 := pow_ne_zero 2 (Nat.succ_ne_zero m)
  have hm_is_sq : IsSquare ((m + 1) ^ 2) := ⟨m + 1, sq (m + 1)⟩
  have h_cpow : ((((m + 1) ^ 2 : ℕ) : ℂ)) ^ z = ((m : ℂ) + 1) ^ (2 * z) := by
    have h1 := (Complex.natCast_cpow_natCast_mul (m + 1) 2 z).symm
    simpa [Nat.cast_add, Nat.cast_one] using h1
  dsimp [sq_map, LSeries.term, g_sq]
  rw [if_neg hm_sq_ne, if_neg hm_sq_ne, if_pos hm_is_sq, h_cpow]

private theorem differentiableOn_continuation_eq_tc063_aux {F_hol : ℂ → ℂ}
    (hF_diff : DifferentiableOn ℂ F_hol {z : ℂ | 1 / 2 < z.re})
    (hF_gt1 : ∀ x y : ℝ, 1 < x →
      F_hol ((x : ℂ) + (y : ℂ) * Complex.I) =
        riemannZeta (2 * ((x : ℂ) + (y : ℂ) * Complex.I)) /
          riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I)) :
    ∀ x y : ℝ, 1 / 2 < x → ((x : ℂ) + (y : ℂ) * Complex.I) ≠ 1 →
      riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) *
        F_hol ((x : ℂ) + (y : ℂ) * Complex.I) =
          riemannZeta (2 * ((x : ℂ) + (y : ℂ) * Complex.I)) := by
  let L : ℂ → ℂ := fun w => riemannZeta w * F_hol w
  let R : ℂ → ℂ := fun w => riemannZeta (2 * w)
  have h_eq_gt1 : ∀ w : ℂ, 1 < w.re → L w = R w := by
    intro w hw
    have hw_rep : ((w.re : ℂ) + (w.im : ℂ) * Complex.I) = w := Complex.re_add_im w
    have hzeta_ne : riemannZeta w ≠ 0 := riemannZeta_ne_zero_of_one_lt_re hw
    have hF_w := hF_gt1 w.re w.im hw
    rw [hw_rep] at hF_w
    dsimp [L, R]
    rw [hF_w, mul_div_cancel₀ _ hzeta_ne]
  have hL_diff : ∀ w : ℂ, 1 / 2 < w.re → w ≠ 1 → DifferentiableAt ℂ L w := by
    intro w hw_re hw_ne1
    have hU_open : IsOpen {z : ℂ | 1 / 2 < z.re} :=
      isOpen_lt continuous_const Complex.continuous_re
    have hF_at : DifferentiableAt ℂ F_hol w :=
      (hF_diff w hw_re).differentiableAt (hU_open.mem_nhds hw_re)
    exact (differentiableAt_riemannZeta hw_ne1).mul hF_at
  have hR_diff : ∀ w : ℂ, 1 / 2 < w.re → DifferentiableAt ℂ R w := by
    intro w hw_re
    have h2w_ne1 : 2 * w ≠ 1 := by
      intro h_eq
      have hre := congr_arg Complex.re h_eq
      simp at hre
      linarith
    exact (differentiableAt_riemannZeta h2w_ne1).comp w (differentiableAt_id.const_mul 2)
  -- Upper half-plane right of 1/2:
  let V_pos : Set ℂ := {w : ℂ | 1 / 2 < w.re ∧ 0 < w.im}
  have hV_pos_open : IsOpen V_pos :=
    (isOpen_lt continuous_const Complex.continuous_re).inter
      (isOpen_lt continuous_const Complex.continuous_im)
  have hV_pos_pre : IsPreconnected V_pos :=
    ((convex_halfspace_re_gt (1 / 2)).inter (convex_halfspace_im_gt 0)).isPreconnected
  have hV_pos_ne1 : ∀ w ∈ V_pos, w ≠ 1 := by
    intro w hw h1
    have him : w.im = 0 := by rw [h1]; simp
    linarith [hw.2]
  have hL_diff_pos : DifferentiableOn ℂ L V_pos :=
    fun w hw => (hL_diff w hw.1 (hV_pos_ne1 w hw)).differentiableWithinAt
  have hR_diff_pos : DifferentiableOn ℂ R V_pos :=
    fun w hw => (hR_diff w hw.1).differentiableWithinAt
  have hL_an_pos : AnalyticOn ℂ L V_pos := hL_diff_pos.analyticOn hV_pos_open
  have hR_an_pos : AnalyticOn ℂ R V_pos := hR_diff_pos.analyticOn hV_pos_open
  let z_pos : ℂ := (2 : ℂ) + (1 : ℂ) * Complex.I
  have hz_pos_in : z_pos ∈ V_pos := by
    dsimp [V_pos, z_pos]
    simp
    norm_num
  have h_freq_pos : ∃ᶠ w in nhdsWithin z_pos {z_pos}ᶜ, L w = R w := by
    have h_ev_nhds : ∀ᶠ w in nhds z_pos, L w = R w := by
      have h_mem : {w : ℂ | 1 < w.re} ∈ nhds z_pos :=
        (isOpen_lt continuous_const Complex.continuous_re).mem_nhds (by dsimp [z_pos]; simp)
      exact Filter.eventually_of_mem h_mem h_eq_gt1
    haveI : (nhdsWithin z_pos {z_pos}ᶜ).NeBot := mem_closure_iff_nhdsWithin_neBot.mp (by
      rw [closure_compl, interior_singleton]
      exact Set.not_mem_empty z_pos)
    exact (eventually_nhdsWithin_of_eventually_nhds h_ev_nhds).frequently
  have h_eq_pos : Set.EqOn L R V_pos :=
    hL_an_pos.eqOn_of_preconnected_of_frequently_eq hR_an_pos hV_pos_pre hz_pos_in h_freq_pos
  -- Lower half-plane right of 1/2:
  let V_neg : Set ℂ := {w : ℂ | 1 / 2 < w.re ∧ w.im < 0}
  have hV_neg_open : IsOpen V_neg :=
    (isOpen_lt continuous_const Complex.continuous_re).inter
      (isOpen_lt Complex.continuous_im continuous_const)
  have hV_neg_pre : IsPreconnected V_neg :=
    ((convex_halfspace_re_gt (1 / 2)).inter (convex_halfspace_im_lt 0)).isPreconnected
  have hV_neg_ne1 : ∀ w ∈ V_neg, w ≠ 1 := by
    intro w hw h1
    have him : w.im = 0 := by rw [h1]; simp
    linarith [hw.2]
  have hL_diff_neg : DifferentiableOn ℂ L V_neg :=
    fun w hw => (hL_diff w hw.1 (hV_neg_ne1 w hw)).differentiableWithinAt
  have hR_diff_neg : DifferentiableOn ℂ R V_neg :=
    fun w hw => (hR_diff w hw.1).differentiableWithinAt
  have hL_an_neg : AnalyticOn ℂ L V_neg := hL_diff_neg.analyticOn hV_neg_open
  have hR_an_neg : AnalyticOn ℂ R V_neg := hR_diff_neg.analyticOn hV_neg_open
  let z_neg : ℂ := (2 : ℂ) + (-1 : ℂ) * Complex.I
  have hz_neg_in : z_neg ∈ V_neg := by
    dsimp [V_neg, z_neg]
    simp
    norm_num
  have h_freq_neg : ∃ᶠ w in nhdsWithin z_neg {z_neg}ᶜ, L w = R w := by
    have h_ev_nhds : ∀ᶠ w in nhds z_neg, L w = R w := by
      have h_mem : {w : ℂ | 1 < w.re} ∈ nhds z_neg :=
        (isOpen_lt continuous_const Complex.continuous_re).mem_nhds (by dsimp [z_neg]; simp)
      exact Filter.eventually_of_mem h_mem h_eq_gt1
    haveI : (nhdsWithin z_neg {z_neg}ᶜ).NeBot := mem_closure_iff_nhdsWithin_neBot.mp (by
      rw [closure_compl, interior_singleton]
      exact Set.not_mem_empty z_neg)
    exact (eventually_nhdsWithin_of_eventually_nhds h_ev_nhds).frequently
  have h_eq_neg : Set.EqOn L R V_neg :=
    hL_an_neg.eqOn_of_preconnected_of_frequently_eq hR_an_neg hV_neg_pre hz_neg_in h_freq_neg
  -- Combine y > 0, y < 0, and real axis y = 0 (by continuity from V_pos):
  intro x y hx hz_ne1
  let z : ℂ := (x : ℂ) + (y : ℂ) * Complex.I
  have hz_re : 1 / 2 < z.re := by
    change 1 / 2 < ((x : ℂ) + (y : ℂ) * Complex.I).re
    rw [(complex_re_im_coord_tc063_aux x y).1]
    exact hx
  have hz_im : z.im = y := (complex_re_im_coord_tc063_aux x y).2.1
  change L z = R z
  rcases lt_trichotomy y 0 with hy_neg | rfl | hy_pos
  · exact h_eq_neg ⟨hz_re, by linarith [hz_im]⟩
  · let seq : ℕ → ℂ := fun n => z + ((1 / ((n : ℝ) + 1) : ℝ) : ℂ) * Complex.I
    have hseq_in : ∀ n : ℕ, seq n ∈ V_pos := by
      intro n
      refine ⟨?_, ?_⟩
      · change 1 / 2 < (z + ((1 / ((n : ℝ) + 1) : ℝ) : ℂ) * Complex.I).re
        simp only [Complex.add_re, Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im,
          Complex.I_re, Complex.I_im, mul_zero, sub_zero, add_zero]
        linarith [hz_re]
      · change 0 < (z + ((1 / ((n : ℝ) + 1) : ℝ) : ℂ) * Complex.I).im
        have hn_pos : (0 : ℝ) < (n : ℝ) + 1 := by positivity
        simp only [Complex.add_im, Complex.mul_im, Complex.ofReal_re, Complex.ofReal_im,
          Complex.I_re, Complex.I_im, mul_one, add_zero, hz_im, zero_add]
        linarith [one_div_pos.mpr hn_pos]
    have hseq_tendsto : Filter.Tendsto seq Filter.atTop (nhds z) := by
      have h_inv : Filter.Tendsto (fun n : ℕ => (1 / ((n : ℝ) + 1) : ℝ)) Filter.atTop (nhds 0) :=
        tendsto_one_div_add_atTop_nhds_zero_nat
      have h_c : Filter.Tendsto (fun n : ℕ => ((1 / ((n : ℝ) + 1) : ℝ) : ℂ) * Complex.I)
          Filter.atTop (nhds (((0 : ℝ) : ℂ) * Complex.I)) :=
        (Complex.continuous_ofReal.continuousAt.tendsto.comp h_inv).mul_const Complex.I
      simpa [seq] using tendsto_const_nhds.add h_c
    have hL_tend : Filter.Tendsto (L ∘ seq) Filter.atTop (nhds (L z)) :=
      (hL_diff z hz_re hz_ne1).continuousAt.tendsto.comp hseq_tendsto
    have hR_tend : Filter.Tendsto (R ∘ seq) Filter.atTop (nhds (R z)) :=
      (hR_diff z hz_re).continuousAt.tendsto.comp hseq_tendsto
    have hLR_seq : L ∘ seq = R ∘ seq := by
      ext n; exact h_eq_pos (hseq_in n)
    rw [hLR_seq] at hL_tend
    exact tendsto_nhds_unique hL_tend hR_tend
  · exact h_eq_pos ⟨hz_re, by linarith [hz_im]⟩

/-- **Theorem 1 (`TASK-TC-063` §2, Liouville Dirichlet Ratio on `1 < x`, Trivial-Zero Double Vanishing, Strip Reflection on `0 < x < 1 / 2`, and Right-Half-Strip Pole Contradiction)**:
    Writing `z = (x : ℂ) + (y : ℂ) * Complex.I` for real coordinates `x, y : ℝ`:
    1. *Dirichlet ratio & Euler-product nonvanishing (`1 < x`)*:
       `riemannZeta z ≠ 0`, `riemannZeta (2 * z) ≠ 0`, and
       `LSeries (fun n => if n = 0 then 0 else (liouvilleLambda n : ℂ)) z * riemannZeta z = riemannZeta (2 * z)`;
    2. *Trivial-zero double vanishing (`n : ℕ`)*:
       `riemannZeta (-2 * ((n : ℂ) + 1)) = 0 ∧ riemannZeta (2 * (-2 * ((n : ℂ) + 1))) = 0`;
    3. *Functional-equation strip reflection (`0 < x < 1 / 2`) & right-half-strip pole contradiction (`1 / 2 < x`)*:
       - If `0 < x ∧ x < 1 / 2` and `riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) = 0`, then
         `1 / 2 < 1 - x ∧ 1 - x < 1` and
         `riemannZeta (((1 - x : ℝ) : ℂ) + ((-y : ℝ) : ℂ) * Complex.I) = 0`;
       - Any `F_hol : ℂ → ℂ` satisfying
         `∀ x y : ℝ, 1 / 2 < x → ((x : ℂ) + (y : ℂ) * Complex.I) ≠ 1 → riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) * F_hol ((x : ℂ) + (y : ℂ) * Complex.I) = riemannZeta (2 * ((x : ℂ) + (y : ℂ) * Complex.I))`
         (and in particular any `F_hol` with `DifferentiableOn ℂ F_hol {z : ℂ | 1 / 2 < z.re}`
         agreeing with `ζ(2z) / ζ(z)` on `1 < x`) forces both right-half-plane nonvanishing on
         `1 / 2 < x` (`z ≠ 1`) and critical-line localization `x = 1 / 2` for every strip zero on `0 < x < 1`. -/
theorem liouville_dirichlet_ratio_pole_contradiction_and_reflection_tc063 :
    (∀ (x y : ℝ), 1 < x →
      let z : ℂ := (x : ℂ) + (y : ℂ) * Complex.I
      riemannZeta z ≠ 0 ∧
        riemannZeta (2 * z) ≠ 0 ∧
        LSeries (fun n => if n = 0 then 0 else (liouvilleLambda n : ℂ)) z * riemannZeta z =
          riemannZeta (2 * z)) ∧
    (∀ n : ℕ,
      riemannZeta (-2 * ((n : ℂ) + 1)) = 0 ∧
        riemannZeta (2 * (-2 * ((n : ℂ) + 1))) = 0) ∧
    ((∀ (x y : ℝ), 0 < x → x < 1 / 2 →
        riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) = 0 →
          (1 / 2 < 1 - x ∧ 1 - x < 1) ∧
            riemannZeta (((1 - x : ℝ) : ℂ) + ((-y : ℝ) : ℂ) * Complex.I) = 0) ∧
      (∀ (F_hol : ℂ → ℂ),
        (∀ (x y : ℝ), 1 / 2 < x → ((x : ℂ) + (y : ℂ) * Complex.I) ≠ 1 →
          riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) *
            F_hol ((x : ℂ) + (y : ℂ) * Complex.I) =
              riemannZeta (2 * ((x : ℂ) + (y : ℂ) * Complex.I))) →
        (∀ (x y : ℝ), 1 / 2 < x → ((x : ℂ) + (y : ℂ) * Complex.I) ≠ 1 →
          riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) ≠ 0) ∧
        (∀ (x y : ℝ), 0 < x → x < 1 →
          riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) = 0 → x = 1 / 2)) ∧
      (∀ (F_hol : ℂ → ℂ),
        DifferentiableOn ℂ F_hol {z : ℂ | 1 / 2 < z.re} →
        (∀ (x y : ℝ), 1 < x →
          F_hol ((x : ℂ) + (y : ℂ) * Complex.I) =
            riemannZeta (2 * ((x : ℂ) + (y : ℂ) * Complex.I)) /
              riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I)) →
        (∀ (x y : ℝ), 1 / 2 < x → ((x : ℂ) + (y : ℂ) * Complex.I) ≠ 1 →
          riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) *
            F_hol ((x : ℂ) + (y : ℂ) * Complex.I) =
              riemannZeta (2 * ((x : ℂ) + (y : ℂ) * Complex.I))) ∧
        (∀ (x y : ℝ), 0 < x → x < 1 →
          riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) = 0 → x = 1 / 2))) := by
  have h_part1 :
      ∀ (x y : ℝ), 1 < x →
        let z : ℂ := (x : ℂ) + (y : ℂ) * Complex.I
        riemannZeta z ≠ 0 ∧
          riemannZeta (2 * z) ≠ 0 ∧
          LSeries (fun n => if n = 0 then 0 else (liouvilleLambda n : ℂ)) z * riemannZeta z =
            riemannZeta (2 * z) :=
    fun _ _ hx => liouville_lseries_mul_zeta_eq_zeta_two_tc063_aux hx
  have h_part2 :
      ∀ n : ℕ,
        riemannZeta (-2 * ((n : ℂ) + 1)) = 0 ∧
          riemannZeta (2 * (-2 * ((n : ℂ) + 1))) = 0 := by
    intro n
    refine ⟨riemannZeta_neg_two_mul_nat_add_one n, ?_⟩
    have h_double : 2 * (-2 * ((n : ℂ) + 1)) = -2 * (((2 * n + 1 : ℕ) : ℂ) + 1) := by
      push_cast; ring
    rw [h_double]
    exact riemannZeta_neg_two_mul_nat_add_one (2 * n + 1)
  have h_refl :
      ∀ (x y : ℝ), 0 < x → x < 1 / 2 →
        riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) = 0 →
          (1 / 2 < 1 - x ∧ 1 - x < 1) ∧
            riemannZeta (((1 - x : ℝ) : ℂ) + ((-y : ℝ) : ℂ) * Complex.I) = 0 := by
    intro x y hx0 hx_half h_zero
    let z : ℂ := (x : ℂ) + (y : ℂ) * Complex.I
    have hz_re : z.re = x := (complex_re_im_coord_tc063_aux x y).1
    have hz_ne0 : z ≠ 0 := by
      intro h0
      have hre : z.re = 0 := by rw [h0]; simp
      linarith
    have h_gamma_ne : z.Gammaℝ ≠ 0 :=
      Complex.Gammaℝ_ne_zero_of_re_pos (by linarith [hz_re])
    have h_def : riemannZeta z = completedRiemannZeta z / z.Gammaℝ :=
      riemannZeta_def_of_ne_zero hz_ne0
    have h_comp_zero : completedRiemannZeta z = 0 := by
      have hdiv0 : completedRiemannZeta z / z.Gammaℝ = 0 := h_def.symm.trans h_zero
      exact (div_eq_zero_iff.mp hdiv0).resolve_right h_gamma_ne
    have h_one_sub_eq : 1 - z = ((1 - x : ℝ) : ℂ) + ((-y : ℝ) : ℂ) * Complex.I := by
      dsimp [z]; push_cast; ring
    have h1z_ne0 : 1 - z ≠ 0 := by
      intro h0
      have hre : (1 - z).re = 0 := by rw [h0]; simp
      simp [hz_re] at hre
      linarith
    refine ⟨⟨by linarith, by linarith⟩, ?_⟩
    rw [← h_one_sub_eq, riemannZeta_def_of_ne_zero h1z_ne0, completedRiemannZeta_one_sub,
      h_comp_zero, zero_div]
  have h_pole_contra :
      ∀ (F_hol : ℂ → ℂ),
        (∀ (x y : ℝ), 1 / 2 < x → ((x : ℂ) + (y : ℂ) * Complex.I) ≠ 1 →
          riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) *
            F_hol ((x : ℂ) + (y : ℂ) * Complex.I) =
              riemannZeta (2 * ((x : ℂ) + (y : ℂ) * Complex.I))) →
        (∀ (x y : ℝ), 1 / 2 < x → ((x : ℂ) + (y : ℂ) * Complex.I) ≠ 1 →
          riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) ≠ 0) ∧
        (∀ (x y : ℝ), 0 < x → x < 1 →
          riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) = 0 → x = 1 / 2) := by
    intro F_hol hF_id
    have h_no_rhp :
        ∀ (x y : ℝ), 1 / 2 < x → ((x : ℂ) + (y : ℂ) * Complex.I) ≠ 1 →
          riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) ≠ 0 := by
      intro x y hx hz_ne1 hz_zero
      have h_id := hF_id x y hx hz_ne1
      rw [hz_zero, zero_mul] at h_id
      have h2z_re : 1 < (2 * ((x : ℂ) + (y : ℂ) * Complex.I)).re := by
        rw [(complex_re_im_coord_tc063_aux x y).2.2]; linarith
      exact riemannZeta_ne_zero_of_one_lt_re h2z_re h_id.symm
    refine ⟨h_no_rhp, ?_⟩
    intro x y hx0 hx1 hz_zero
    rcases lt_trichotomy x (1 / 2) with hx_lt | hx_eq | hx_gt
    · obtain ⟨⟨h1x_gt, h1x_lt1⟩, h1z_zero⟩ := h_refl x y hx0 hx_lt hz_zero
      have h1z_ne1 : (((1 - x : ℝ) : ℂ) + ((-y : ℝ) : ℂ) * Complex.I) ≠ 1 := by
        intro h1
        have hre := congr_arg Complex.re h1
        simp at hre
        linarith [h1x_lt1]
      exact False.elim (h_no_rhp (1 - x) (-y) h1x_gt h1z_ne1 h1z_zero)
    · exact hx_eq
    · have hz_ne1 : ((x : ℂ) + (y : ℂ) * Complex.I) ≠ 1 := by
        intro h1
        have hre := congr_arg Complex.re h1
        simp at hre
        linarith
      exact False.elim (h_no_rhp x y hx_gt hz_ne1 hz_zero)
  refine ⟨h_part1, h_part2, h_refl, h_pole_contra, ?_⟩
  intro F_hol hF_diff hF_gt1
  have h_id := differentiableOn_continuation_eq_tc063_aux hF_diff hF_gt1
  exact ⟨h_id, (h_pole_contra F_hol h_id).2⟩

/-! ### Section 2: Odd-Part Bijection & Dyadic-Chain Off-Diagonal Split (`TASK-TC-063` §3) -/

private theorem add_one_le_four_pow_tc063_aux (j : ℕ) : j + 1 ≤ 4 ^ j := by
  induction j with
  | zero => norm_num
  | succ j ih =>
    calc
      (j + 1) + 1 ≤ 4 * (j + 1) := by omega
      _ ≤ 4 * 4 ^ j := Nat.mul_le_mul_left 4 ih
      _ = 4 ^ (j + 1) := by ring

private theorem mem_dyadicChainExponents_iff_tc063_aux {u : ℕ} (hu : 1 ≤ u) (j T : ℕ) :
    j ∈ dyadicChainExponents u T ↔ 2 * 4 ^ j * u ≤ T := by
  simp only [dyadicChainExponents, Finset.mem_filter, Finset.mem_range]
  constructor
  · exact And.right
  · intro h_le
    refine ⟨?_, h_le⟩
    have hj4 := add_one_le_four_pow_tc063_aux j
    have h2 : 2 * (j + 1) * 1 ≤ 2 * 4 ^ j * u :=
      Nat.mul_le_mul (Nat.mul_le_mul_left 2 hj4) hu
    omega

private theorem two_pow_mul_odd_factorization_two_tc063_aux (v : ℕ) {u : ℕ} (hu : Odd u) :
    (2 ^ v * u).factorization 2 = v := by
  have hu_pos : 0 < u := hu.pos
  have hu_ne : u ≠ 0 := ne_of_gt hu_pos
  have h2_not_dvd : ¬ 2 ∣ u := fun h2 =>
    (Nat.odd_iff_not_even.mp hu) (even_iff_two_dvd.mpr h2)
  rw [Nat.factorization_mul (pow_ne_zero v (by decide)) hu_ne, Finsupp.add_apply,
    Nat.factorization_eq_zero_of_not_dvd h2_not_dvd, add_zero,
    Nat.Prime.factorization_pow Nat.prime_two, Finsupp.single_eq_same]

private theorem four_pow_mul_odd_factorization_two_tc063_aux (j : ℕ) {u : ℕ} (hu : Odd u) :
    (4 ^ j * u).factorization 2 = 2 * j := by
  have h4 : (4 : ℕ) ^ j = 2 ^ (2 * j) := by
    rw [show (4 : ℕ) = 2 ^ 2 by norm_num, ← pow_mul]
  rw [h4]
  exact two_pow_mul_odd_factorization_two_tc063_aux (2 * j) hu

private theorem exists_two_pow_mul_odd_tc063_aux :
    ∀ m : ℕ, 1 ≤ m → ∃ v u : ℕ, Odd u ∧ 2 ^ v * u = m := by
  intro m
  induction m using Nat.strongRecOn with
  | ind m ih =>
    intro hm1
    rcases Nat.even_or_odd m with hm_ev | hm_odd
    · obtain ⟨k, rfl⟩ := even_iff_two_dvd.mp hm_ev
      have hk1 : 1 ≤ k := by omega
      have hk_lt : k < 2 * k := by omega
      obtain ⟨v, u, hu_odd, h_eq⟩ := ih k hk_lt hk1
      exact ⟨v + 1, u, hu_odd, by rw [pow_succ', mul_assoc, h_eq]⟩
    · exact ⟨0, m, hm_odd, by simp⟩

private theorem four_pow_mul_odd_inj_tc063_aux {u1 u2 j1 j2 : ℕ}
    (hu1 : Odd u1) (hu2 : Odd u2) (h_eq : 4 ^ j1 * u1 = 4 ^ j2 * u2) :
    u1 = u2 ∧ j1 = j2 := by
  have hf1 := four_pow_mul_odd_factorization_two_tc063_aux j1 hu1
  have hf2 := four_pow_mul_odd_factorization_two_tc063_aux j2 hu2
  have h2j : 2 * j1 = 2 * j2 := by rw [← hf1, h_eq, hf2]
  have hj : j1 = j2 := by omega
  subst hj
  have h4_pos : 0 < 4 ^ j1 := pow_pos (by decide) j1
  exact ⟨Nat.eq_of_mul_eq_mul_left h4_pos h_eq, rfl⟩

private theorem odd_part_anchor_mem_and_unique_tc063_aux (T : ℕ) :
    (∀ u ∈ oddChainParts T, ∀ j ∈ dyadicChainExponents u T,
      4 ^ j * u ∈ primeInteriorTruncatedAnchors 2 T) ∧
    (∀ m ∈ primeInteriorTruncatedAnchors 2 T,
      ∃! uj : ℕ × ℕ,
        uj.1 ∈ oddChainParts T ∧ uj.2 ∈ dyadicChainExponents uj.1 T ∧ 4 ^ uj.2 * uj.1 = m) ∧
    ((oddChainParts T).biUnion
      (fun u => (dyadicChainExponents u T).image (fun j => 4 ^ j * u)) =
        primeInteriorTruncatedAnchors 2 T) := by
  have h_fwd :
      ∀ u ∈ oddChainParts T, ∀ j ∈ dyadicChainExponents u T,
        4 ^ j * u ∈ primeInteriorTruncatedAnchors 2 T := by
    intro u hu j hj
    simp only [oddChainParts, Finset.mem_filter, Finset.mem_Icc] at hu
    rcases hu with ⟨⟨hu1, _⟩, hu_odd, _⟩
    have hj_le : 2 * 4 ^ j * u ≤ T := (mem_dyadicChainExponents_iff_tc063_aux hu1 j T).mp hj
    have h4_pos : 1 ≤ 4 ^ j := Nat.one_le_pow j 4 (by decide)
    have hm1 : 1 ≤ 4 ^ j * u := Nat.mul_pos h4_pos hu1
    have h2m_le : 2 * (4 ^ j * u) ≤ T := by linarith [show 2 * (4 ^ j * u) = 2 * 4 ^ j * u by ring]
    have hm_ev : Even ((4 ^ j * u).factorization 2) := by
      rw [four_pow_mul_odd_factorization_two_tc063_aux j hu_odd]
      exact ⟨j, by ring⟩
    simp only [primeInteriorTruncatedAnchors, primeEvenValuationAnchors,
      Finset.mem_filter, Finset.mem_Icc]
    exact ⟨⟨⟨hm1, by omega⟩, hm_ev⟩, h2m_le⟩
  have h_uniq :
      ∀ m ∈ primeInteriorTruncatedAnchors 2 T,
        ∃! uj : ℕ × ℕ,
          uj.1 ∈ oddChainParts T ∧ uj.2 ∈ dyadicChainExponents uj.1 T ∧ 4 ^ uj.2 * uj.1 = m := by
    intro m hm
    simp only [primeInteriorTruncatedAnchors, primeEvenValuationAnchors,
      Finset.mem_filter, Finset.mem_Icc] at hm
    rcases hm with ⟨⟨⟨hm1, _⟩, hm_ev⟩, h2m_le⟩
    obtain ⟨v, u, hu_odd, hv_eq⟩ := exists_two_pow_mul_odd_tc063_aux m hm1
    have hv_fact : v = m.factorization 2 := by
      rw [← hv_eq, two_pow_mul_odd_factorization_two_tc063_aux v hu_odd]
    rw [← hv_fact] at hm_ev
    obtain ⟨j, hj_add⟩ := hm_ev
    have hv_2j : v = 2 * j := by omega
    have hm_4j : 4 ^ j * u = m := by
      have h4 : (4 : ℕ) ^ j = 2 ^ v := by
        rw [hv_2j, show (4 : ℕ) = 2 ^ 2 by norm_num, ← pow_mul]
      rwa [h4]
    have hu1 : 1 ≤ u := hu_odd.pos
    have h4_ge1 : 1 ≤ 4 ^ j := Nat.one_le_pow j 4 (by decide)
    have h2_4j_u : 2 * 4 ^ j * u ≤ T := by
      calc
        2 * 4 ^ j * u = 2 * (4 ^ j * u) := by ring
        _ = 2 * m := by rw [hm_4j]
        _ ≤ T := h2m_le
    have h2u_le : 2 * u ≤ T := by
      calc
        2 * u = 2 * (1 * u) := by ring
        _ ≤ 2 * (4 ^ j * u) := Nat.mul_le_mul_left 2 (Nat.mul_le_mul_right u h4_ge1)
        _ = 2 * m := by rw [hm_4j]
        _ ≤ T := h2m_le
    have hu_in : u ∈ oddChainParts T := by
      simp only [oddChainParts, Finset.mem_filter, Finset.mem_Icc]
      exact ⟨⟨hu1, by omega⟩, hu_odd, h2u_le⟩
    have hj_in : j ∈ dyadicChainExponents u T :=
      (mem_dyadicChainExponents_iff_tc063_aux hu1 j T).mpr h2_4j_u
    refine ⟨(u, j), ⟨hu_in, hj_in, hm_4j⟩, ?_⟩
    rintro ⟨u', j'⟩ ⟨hu'_in, _, hm_eq'⟩
    have hu'_odd : Odd u' := (Finset.mem_filter.mp hu'_in).2.1
    obtain ⟨rfl, rfl⟩ := four_pow_mul_odd_inj_tc063_aux hu'_odd hu_odd (hm_eq'.trans hm_4j.symm)
    rfl
  refine ⟨h_fwd, h_uniq, ?_⟩
  ext m
  simp only [Finset.mem_biUnion, Finset.mem_image]
  constructor
  · rintro ⟨u, hu, j, hj, rfl⟩
    exact h_fwd u hu j hj
  · intro hm
    obtain ⟨⟨u, j⟩, ⟨hu, hj, rfl⟩, _⟩ := h_uniq m hm
    exact ⟨u, hu, j, hj, rfl⟩

private theorem sum_anchors_eq_odd_chains_tc063_aux (T : ℕ) (f : ℕ → ℝ) :
    (∑ m ∈ primeInteriorTruncatedAnchors 2 T, f m) =
      ∑ u ∈ oddChainParts T, ∑ j ∈ dyadicChainExponents u T, f (4 ^ j * u) := by
  obtain ⟨_, _, h_bi⟩ := odd_part_anchor_mem_and_unique_tc063_aux T
  rw [← h_bi, Finset.sum_biUnion]
  · apply Finset.sum_congr rfl
    intro u hu
    have hu_odd : Odd u := (Finset.mem_filter.mp hu).2.1
    rw [Finset.sum_image]
    intro j1 _ j2 _ h_eq
    exact (four_pow_mul_odd_inj_tc063_aux hu_odd hu_odd h_eq).2
  · intro u1 hu1 u2 hu2 h_ne
    change Disjoint _ _
    rw [Finset.disjoint_left]
    intro x hx1 hx2
    simp only [Finset.mem_image] at hx1 hx2
    rcases hx1 with ⟨j1, _, rfl⟩
    rcases hx2 with ⟨j2, _, h_eq⟩
    have hu1_odd : Odd u1 := (Finset.mem_filter.mp hu1).2.1
    have hu2_odd : Odd u2 := (Finset.mem_filter.mp hu2).2.1
    exact h_ne (four_pow_mul_odd_inj_tc063_aux hu2_odd hu1_odd h_eq).1.symm

private theorem liouvilleLambda_four_pow_mul_tc063_aux {u : ℕ} (hu : 1 ≤ u) (j : ℕ) :
    liouvilleLambda (4 ^ j * u) = liouvilleLambda u := by
  induction j with
  | zero => simp
  | succ j ih =>
    have h4_pos : 1 ≤ 4 ^ j * u := Nat.mul_pos (Nat.one_le_pow j 4 (by decide)) hu
    have h2_pos : 1 ≤ 2 * (4 ^ j * u) := by omega
    have h_step : 4 ^ (j + 1) * u = 2 * (2 * (4 ^ j * u)) := by ring
    have h_mul2 : ∀ k : ℕ, 1 ≤ k → liouvilleLambda (2 * k) = -liouvilleLambda k := by
      intro k hk
      have hk_ne : k ≠ 0 := by omega
      have h2k_ne : 2 * k ≠ 0 := by omega
      have h_om : natOmega (2 * k) = 1 + natOmega k := by
        simp [natOmega, ArithmeticFunction.cardFactors_mul (by decide : 2 ≠ 0) hk_ne,
          ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr Nat.prime_two]
      simp [liouvilleLambda, hk_ne, h2k_ne, h_om, liouvilleSignFromOmega, pow_add]
    rw [h_step, h_mul2 _ h2_pos, h_mul2 _ h4_pos, neg_neg, ih]

/-- **Theorem 2 (`TASK-TC-063` §3, Odd-Part Unique Representation, Chain Edge Cases, Generic Ordered-Pair Reindexing, and Complete-Kernel `S_same + S_diff` Split)**:
    1. *Unique `m = 4^j * u` bijection onto `primeInteriorTruncatedAnchors 2 T` and chain edge cases*:
       - `∀ m ∈ primeInteriorTruncatedAnchors 2 T, ∃! uj : ℕ × ℕ, uj.1 ∈ oddChainParts T ∧ uj.2 ∈ dyadicChainExponents uj.1 T ∧ 4 ^ uj.2 * uj.1 = m`;
       - `∀ u j T : ℕ, 1 ≤ u → (j ∈ dyadicChainExponents u T ↔ 2 * 4 ^ j * u ≤ T)`;
       - `∀ T : ℕ, (oddChainParts T = ∅ ↔ T < 2)`, `∀ u ∈ oddChainParts T, 0 ∈ dyadicChainExponents u T`, and `∀ u ∈ oddChainParts T, ((dyadicChainExponents u T).card = 1 ↔ T < 8 * u)`;
       - `∀ u ∈ oddChainParts T, ∀ j ∈ dyadicChainExponents u T, 4 ^ j * u ∈ primeInteriorTruncatedAnchors 2 T` and `(oddChainParts T).biUnion (fun u => (dyadicChainExponents u T).image (fun j => 4 ^ j * u)) = primeInteriorTruncatedAnchors 2 T`;
    2. *Generic ordered-pair reindexing* for arbitrary `H : ℕ → ℕ → ℝ` and `a : ℕ → ℝ`;
    3. *`4^j` Liouville invariance (`liouvilleLambda (4^j * u) = liouvilleLambda u`) and exact decomposition*
       `interiorAnchorOffDiagSigma c_lam c_half 2 T D0 Y = sameOddChainSumS c_lam c_half T D0 Y + differentOddChainSumS c_lam c_half T D0 Y`,
       with canonical instantiation at `(actualSelbergConstantCLam, actualSquarePoleConstantCHalf)`. -/
theorem exact_odd_part_bijection_and_dyadic_chain_offdiag_split_tc063 :
    ((∀ (T : ℕ), ∀ m ∈ primeInteriorTruncatedAnchors 2 T,
        ∃! uj : ℕ × ℕ,
          uj.1 ∈ oddChainParts T ∧ uj.2 ∈ dyadicChainExponents uj.1 T ∧ 4 ^ uj.2 * uj.1 = m) ∧
      (∀ (u j T : ℕ), 1 ≤ u → (j ∈ dyadicChainExponents u T ↔ 2 * 4 ^ j * u ≤ T)) ∧
      (∀ (T : ℕ),
        (oddChainParts T = ∅ ↔ T < 2) ∧
          (∀ u ∈ oddChainParts T, 0 ∈ dyadicChainExponents u T) ∧
          (∀ u ∈ oddChainParts T, (dyadicChainExponents u T).card = 1 ↔ T < 8 * u)) ∧
      (∀ (T : ℕ),
        (∀ u ∈ oddChainParts T, ∀ j ∈ dyadicChainExponents u T,
          4 ^ j * u ∈ primeInteriorTruncatedAnchors 2 T) ∧
          (oddChainParts T).biUnion
            (fun u => (dyadicChainExponents u T).image (fun j => 4 ^ j * u)) =
              primeInteriorTruncatedAnchors 2 T)) ∧
    (∀ (T : ℕ) (a : ℕ → ℝ) (H : ℕ → ℕ → ℝ),
      (∑ m ∈ primeInteriorTruncatedAnchors 2 T,
        ∑ n ∈ (primeInteriorTruncatedAnchors 2 T).erase m,
          a m * a n * H m n) =
        (∑ u ∈ oddChainParts T,
          ∑ j ∈ dyadicChainExponents u T,
            ∑ k ∈ (dyadicChainExponents u T).erase j,
              a (4 ^ j * u) * a (4 ^ k * u) * H (4 ^ j * u) (4 ^ k * u)) +
        (∑ u ∈ oddChainParts T,
          ∑ v ∈ (oddChainParts T).erase u,
            ∑ j ∈ dyadicChainExponents u T,
              ∑ k ∈ dyadicChainExponents v T,
                a (4 ^ j * u) * a (4 ^ k * v) * H (4 ^ j * u) (4 ^ k * v))) ∧
    ((∀ (u j : ℕ), 1 ≤ u → liouvilleLambda (4 ^ j * u) = liouvilleLambda u) ∧
      (∀ (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ),
        interiorAnchorOffDiagSigma c_lam c_half 2 T D0 Y =
          sameOddChainSumS c_lam c_half T D0 Y +
            differentOddChainSumS c_lam c_half T D0 Y) ∧
      (∀ (Y : ℝ),
        canonicalInteriorOffDiagSigma
            actualSelbergConstantCLam actualSquarePoleConstantCHalf 2 Y =
          canonicalSameOddChainSumS
              actualSelbergConstantCLam actualSquarePoleConstantCHalf Y +
            canonicalDifferentOddChainSumS
              actualSelbergConstantCLam actualSquarePoleConstantCHalf Y)) := by
  have h_edges :
      ∀ (T : ℕ),
        (oddChainParts T = ∅ ↔ T < 2) ∧
          (∀ u ∈ oddChainParts T, 0 ∈ dyadicChainExponents u T) ∧
          (∀ u ∈ oddChainParts T, (dyadicChainExponents u T).card = 1 ↔ T < 8 * u) := by
    intro T
    refine ⟨?_, ?_, ?_⟩
    · constructor
      · intro h_emp
        by_contra h_ge2
        have h1_in : 1 ∈ oddChainParts T := by
          simp only [oddChainParts, Finset.mem_filter, Finset.mem_Icc]
          exact ⟨⟨le_refl 1, by omega⟩, odd_one, by omega⟩
        rw [h_emp] at h1_in
        exact Finset.not_mem_empty 1 h1_in
      · intro h_lt2
        rw [Finset.eq_empty_iff_forall_not_mem]
        intro u hu
        simp only [oddChainParts, Finset.mem_filter, Finset.mem_Icc] at hu
        omega
    · intro u hu
      simp only [oddChainParts, Finset.mem_filter, Finset.mem_Icc] at hu
      rw [mem_dyadicChainExponents_iff_tc063_aux hu.1.1 0 T]
      simpa using hu.2.2
    · intro u hu
      simp only [oddChainParts, Finset.mem_filter, Finset.mem_Icc] at hu
      rcases hu with ⟨⟨hu1, _⟩, _, h2u⟩
      have h0_in : 0 ∈ dyadicChainExponents u T := by
        rw [mem_dyadicChainExponents_iff_tc063_aux hu1 0 T]; simpa using h2u
      constructor
      · intro h_card1
        by_contra h_ge8
        have h1_in : 1 ∈ dyadicChainExponents u T := by
          rw [mem_dyadicChainExponents_iff_tc063_aux hu1 1 T]; omega
        have h_gt1 : 1 < (dyadicChainExponents u T).card :=
          Finset.one_lt_card.mpr ⟨0, h0_in, 1, h1_in, by decide⟩
        omega
      · intro h_lt8
        have h_eq0 : dyadicChainExponents u T = {0} := by
          ext j
          rw [Finset.mem_singleton, mem_dyadicChainExponents_iff_tc063_aux hu1 j T]
          constructor
          · intro hj
            by_contra hj_ne0
            have hj1 : 1 ≤ j := by omega
            have h4_ge : 4 ^ 1 ≤ 4 ^ j := Nat.pow_le_pow_right (by decide) hj1
            have h8_le : 8 * u ≤ 2 * 4 ^ j * u := by
              calc
                8 * u = 2 * 4 ^ 1 * u := by ring
                _ ≤ 2 * 4 ^ j * u := Nat.mul_le_mul_right u (Nat.mul_le_mul_left 2 h4_ge)
            omega
          · rintro rfl; simpa using h2u
        rw [h_eq0, Finset.card_singleton]
  have h_part1 :
      (∀ (T : ℕ), ∀ m ∈ primeInteriorTruncatedAnchors 2 T,
        ∃! uj : ℕ × ℕ,
          uj.1 ∈ oddChainParts T ∧ uj.2 ∈ dyadicChainExponents uj.1 T ∧ 4 ^ uj.2 * uj.1 = m) ∧
      (∀ (u j T : ℕ), 1 ≤ u → (j ∈ dyadicChainExponents u T ↔ 2 * 4 ^ j * u ≤ T)) ∧
      (∀ (T : ℕ),
        (oddChainParts T = ∅ ↔ T < 2) ∧
          (∀ u ∈ oddChainParts T, 0 ∈ dyadicChainExponents u T) ∧
          (∀ u ∈ oddChainParts T, (dyadicChainExponents u T).card = 1 ↔ T < 8 * u)) ∧
      (∀ (T : ℕ),
        (∀ u ∈ oddChainParts T, ∀ j ∈ dyadicChainExponents u T,
          4 ^ j * u ∈ primeInteriorTruncatedAnchors 2 T) ∧
          (oddChainParts T).biUnion
            (fun u => (dyadicChainExponents u T).image (fun j => 4 ^ j * u)) =
              primeInteriorTruncatedAnchors 2 T) := by
    refine ⟨fun T => (odd_part_anchor_mem_and_unique_tc063_aux T).2.1,
      fun u j T hu => mem_dyadicChainExponents_iff_tc063_aux hu j T,
      h_edges,
      fun T => ⟨(odd_part_anchor_mem_and_unique_tc063_aux T).1,
        (odd_part_anchor_mem_and_unique_tc063_aux T).2.2⟩⟩
  have h_part2 :
      ∀ (T : ℕ) (a : ℕ → ℝ) (H : ℕ → ℕ → ℝ),
        (∑ m ∈ primeInteriorTruncatedAnchors 2 T,
          ∑ n ∈ (primeInteriorTruncatedAnchors 2 T).erase m,
            a m * a n * H m n) =
          (∑ u ∈ oddChainParts T,
            ∑ j ∈ dyadicChainExponents u T,
              ∑ k ∈ (dyadicChainExponents u T).erase j,
                a (4 ^ j * u) * a (4 ^ k * u) * H (4 ^ j * u) (4 ^ k * u)) +
          (∑ u ∈ oddChainParts T,
            ∑ v ∈ (oddChainParts T).erase u,
              ∑ j ∈ dyadicChainExponents u T,
                ∑ k ∈ dyadicChainExponents v T,
                  a (4 ^ j * u) * a (4 ^ k * v) * H (4 ^ j * u) (4 ^ k * v)) := by
    intro T a H
    let I := primeInteriorTruncatedAnchors 2 T
    let g : ℕ → ℕ → ℝ := fun m n => a m * a n * H m n
    have h_er_ite :
        (∑ m ∈ I, ∑ n ∈ I.erase m, g m n) =
          ∑ m ∈ I, ∑ n ∈ I, (if n = m then 0 else g m n) := by
      apply Finset.sum_congr rfl
      intro m hm
      symm
      rw [← Finset.add_sum_erase _ _ hm, if_pos rfl, zero_add]
      apply Finset.sum_congr rfl
      intro n hn
      rw [if_neg (Finset.mem_erase.mp hn).1]
    rw [h_er_ite, sum_anchors_eq_odd_chains_tc063_aux T
      (fun m => ∑ n ∈ I, if n = m then 0 else g m n)]
    have h_in :
        ∀ u ∈ oddChainParts T,
          (∑ j ∈ dyadicChainExponents u T,
              ∑ n ∈ I, if n = 4 ^ j * u then 0 else g (4 ^ j * u) n) =
            (∑ j ∈ dyadicChainExponents u T,
              ∑ k ∈ (dyadicChainExponents u T).erase j, g (4 ^ j * u) (4 ^ k * u)) +
            (∑ v ∈ (oddChainParts T).erase u,
              ∑ j ∈ dyadicChainExponents u T,
                ∑ k ∈ dyadicChainExponents v T, g (4 ^ j * u) (4 ^ k * v)) := by
      intro u hu
      have hu_odd : Odd u := (Finset.mem_filter.mp hu).2.1
      have h1 :
          (∑ j ∈ dyadicChainExponents u T,
              ∑ n ∈ I, if n = 4 ^ j * u then 0 else g (4 ^ j * u) n) =
            ∑ v ∈ oddChainParts T,
              ∑ j ∈ dyadicChainExponents u T,
                ∑ k ∈ dyadicChainExponents v T,
                  if 4 ^ k * v = 4 ^ j * u then 0 else g (4 ^ j * u) (4 ^ k * v) := by
        have h_each_j :
            ∀ j ∈ dyadicChainExponents u T,
              (∑ n ∈ I, if n = 4 ^ j * u then 0 else g (4 ^ j * u) n) =
                ∑ v ∈ oddChainParts T,
                  ∑ k ∈ dyadicChainExponents v T,
                    if 4 ^ k * v = 4 ^ j * u then 0 else g (4 ^ j * u) (4 ^ k * v) :=
          fun j _ => sum_anchors_eq_odd_chains_tc063_aux T
            (fun n => if n = 4 ^ j * u then 0 else g (4 ^ j * u) n)
        rw [Finset.sum_congr rfl h_each_j, Finset.sum_comm]
      rw [h1, ← Finset.add_sum_erase _ _ hu]
      congr 1
      · apply Finset.sum_congr rfl
        intro j hj
        rw [← Finset.add_sum_erase _ _ hj, if_pos rfl, zero_add]
        apply Finset.sum_congr rfl
        intro k hk
        have hk_ne_j : k ≠ j := (Finset.mem_erase.mp hk).1
        have h_neq_val : 4 ^ k * u ≠ 4 ^ j * u := fun h_eq =>
          hk_ne_j (four_pow_mul_odd_inj_tc063_aux hu_odd hu_odd h_eq).2
        rw [if_neg h_neq_val]
      · apply Finset.sum_congr rfl
        intro v hv
        have hv_ne_u : v ≠ u := (Finset.mem_erase.mp hv).1
        have hv_odd : Odd v := (Finset.mem_filter.mp (Finset.mem_of_mem_erase hv)).2.1
        apply Finset.sum_congr rfl
        intro j _
        apply Finset.sum_congr rfl
        intro k _
        have h_neq_val : 4 ^ k * v ≠ 4 ^ j * u := fun h_eq =>
          hv_ne_u (four_pow_mul_odd_inj_tc063_aux hv_odd hu_odd h_eq).1
        rw [if_neg h_neq_val]
    rw [Finset.sum_congr rfl h_in, Finset.sum_add_distrib]
  have h_split :
      ∀ (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ),
        interiorAnchorOffDiagSigma c_lam c_half 2 T D0 Y =
          sameOddChainSumS c_lam c_half T D0 Y +
            differentOddChainSumS c_lam c_half T D0 Y := by
    intro c_lam c_half T D0 Y
    unfold interiorAnchorOffDiagSigma sameOddChainSumS differentOddChainSumS oddChainGroupedKernel
    have h_gen :=
      h_part2 T (fun m => (liouvilleLambda m : ℝ)) (anchorFourTermDiffHcal c_lam c_half T D0 Y)
    unfold anchorFourTermDiffHcal at h_gen ⊢
    rw [h_gen]
    congr 1
    · apply Finset.sum_congr rfl
      intro u hu
      have hu1 : 1 ≤ u := (Finset.mem_Icc.mp (Finset.mem_filter.mp hu).1).1
      have hu_ne : u ≠ 0 := by omega
      have h_sq_one : (liouvilleLambda u : ℝ) * (liouvilleLambda u : ℝ) = 1 := by
        have h_int : liouvilleLambda u * liouvilleLambda u = 1 := by
          simp only [liouvilleLambda, hu_ne, ↓reduceIte, liouvilleSignFromOmega]
          rw [← pow_add, show natOmega u + natOmega u = 2 * natOmega u by omega, pow_mul]
          norm_num
        exact_mod_cast h_int
      apply Finset.sum_congr rfl
      intro j _
      apply Finset.sum_congr rfl
      intro k _
      rw [liouvilleLambda_four_pow_mul_tc063_aux hu1 j,
        liouvilleLambda_four_pow_mul_tc063_aux hu1 k, h_sq_one, one_mul]
    · apply Finset.sum_congr rfl
      intro u hu
      have hu1 : 1 ≤ u := (Finset.mem_Icc.mp (Finset.mem_filter.mp hu).1).1
      apply Finset.sum_congr rfl
      intro v hv
      have hv1 : 1 ≤ v :=
        (Finset.mem_Icc.mp (Finset.mem_filter.mp (Finset.mem_of_mem_erase hv)).1).1
      simp_rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro j _
      apply Finset.sum_congr rfl
      intro k _
      rw [liouvilleLambda_four_pow_mul_tc063_aux hu1 j,
        liouvilleLambda_four_pow_mul_tc063_aux hv1 k]
  refine ⟨h_part1, h_part2, ⟨fun u j hu => liouvilleLambda_four_pow_mul_tc063_aux hu j, h_split, ?_⟩⟩
  intro Y
  exact h_split actualSelbergConstantCLam actualSquarePoleConstantCHalf
    (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y

/-! ### Section 3: Uniform Same-Chain Hilbert Bound & Closure Transfer (`TASK-TC-063` §4) -/

private theorem tau_gt_one_tc063_aux : (1 : ℝ) < RiemannScope.tau := by
  have h_bds :=
    (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2
  linarith [h_bds.1]

private theorem uIcc_window_props_tc063_aux {Y : ℝ} (hY2 : 2 ≤ Y) :
    Y ≤ RiemannScope.tau * Y ∧
      ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
        0 < X ∧ 0 < Real.log X ∧ Real.log X ≠ 0 ∧ (Real.log X) ^ 2 ≠ 0 := by
  have htau : (1 : ℝ) < RiemannScope.tau := tau_gt_one_tc063_aux
  have hle : Y ≤ RiemannScope.tau * Y := by nlinarith
  refine ⟨hle, ?_⟩
  intro X hX
  rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX
  have hX0 : 0 < X := by linarith
  have hlog : 0 < Real.log X := Real.log_pos (by linarith)
  exact ⟨hX0, hlog, ne_of_gt hlog, pow_ne_zero 2 (ne_of_gt hlog)⟩

private theorem continuousOn_gaussianTermPhi_tc063_aux (Y : ℝ) (n : ℕ) :
    ContinuousOn (gaussianTermPhi n) (Set.uIcc Y (RiemannScope.tau * Y)) := by
  unfold gaussianTermPhi
  have hr : ContinuousOn (fun X : ℝ => X ^ (5 / 2 : ℝ)) (Set.uIcc Y (RiemannScope.tau * Y)) := by
    apply ContinuousOn.rpow_const continuousOn_id
    intro _ _; right; norm_num
  have he : Continuous (fun X : ℝ => (((n : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (n : ℝ) ^ 2))) := by
    continuity
  exact hr.mul he.continuousOn

private theorem continuousOn_psi_and_featureG_tc063_aux {Y : ℝ} (hY2 : 2 ≤ Y)
    (c_lam c_half : ℝ) (T D0 n : ℕ) (pk : ℕ × ℕ) :
    ContinuousOn (adjustedStationProfilePsi c_lam c_half T D0 n)
        (Set.uIcc Y (RiemannScope.tau * Y)) ∧
      ContinuousOn (stationPrimePowerFeatureG n pk)
        (Set.uIcc Y (RiemannScope.tau * Y)) := by
  obtain ⟨_, hprops⟩ := uIcc_window_props_tc063_aux hY2
  have hlog_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
    ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hprops X hX).1)
  have hphi := continuousOn_gaussianTermPhi_tc063_aux Y n
  refine ⟨?_, ?_⟩
  · unfold adjustedStationProfilePsi
    exact (continuousOn_const.sub
      (continuousOn_const.div (hlog_cont.pow 2) (fun X hX => (hprops X hX).2.2.2))).mul hphi
  · unfold stationPrimePowerFeatureG
    by_cases hd : pk.1 ^ pk.2 ∣ n
    · simp only [hd, ↓reduceIte]
      exact (continuousOn_const.mul hphi).div hlog_cont (fun X hX => (hprops X hX).2.2.1)
    · simp only [hd, ↓reduceIte]
      exact continuousOn_const

private theorem windowPairing_bilinear_and_cauchy_tc063_aux {Y : ℝ} (hY2 : 2 ≤ Y) :
    (∀ {f0 f1 g0 g1 : ℝ → ℝ},
      ContinuousOn f0 (Set.uIcc Y (RiemannScope.tau * Y)) →
      ContinuousOn f1 (Set.uIcc Y (RiemannScope.tau * Y)) →
      ContinuousOn g0 (Set.uIcc Y (RiemannScope.tau * Y)) →
      ContinuousOn g1 (Set.uIcc Y (RiemannScope.tau * Y)) →
        windowPairing Y (fun X => f0 X - f1 X) (fun X => g0 X - g1 X) =
          windowPairing Y f0 g0 - windowPairing Y f1 g0 -
            windowPairing Y f0 g1 + windowPairing Y f1 g1) ∧
    (∀ {f g : ℝ → ℝ},
      ContinuousOn f (Set.uIcc Y (RiemannScope.tau * Y)) →
      ContinuousOn g (Set.uIcc Y (RiemannScope.tau * Y)) →
        0 ≤ windowEnergyNormSq Y f ∧
          2 * |windowPairing Y f g| ≤ windowEnergyNormSq Y f + windowEnergyNormSq Y g ∧
          windowEnergyNormSq Y (fun X => f X - g X) ≤
            2 * windowEnergyNormSq Y f + 2 * windowEnergyNormSq Y g) := by
  obtain ⟨hle, hprops⟩ := uIcc_window_props_tc063_aux hY2
  have h_int :
      ∀ {u v : ℝ → ℝ},
        ContinuousOn u (Set.uIcc Y (RiemannScope.tau * Y)) →
        ContinuousOn v (Set.uIcc Y (RiemannScope.tau * Y)) →
          IntervalIntegrable (fun X => u X * v X / X) volume Y (RiemannScope.tau * Y) := by
    intro u v hu hv
    exact ((hu.mul hv).div continuousOn_id
      (fun X hX => ne_of_gt (hprops X hX).1)).intervalIntegrable
  refine ⟨?_, ?_⟩
  · intro f0 f1 g0 g1 hf0 hf1 hg0 hg1
    have hi00 := h_int hf0 hg0
    have hi10 := h_int hf1 hg0
    have hi01 := h_int hf0 hg1
    have hi11 := h_int hf1 hg1
    unfold windowPairing
    have h_pt :
        (fun X => (f0 X - f1 X) * (g0 X - g1 X) / X) =
          fun X => ((f0 X * g0 X / X - f1 X * g0 X / X) - f0 X * g1 X / X) + f1 X * g1 X / X := by
      ext X; ring
    rw [h_pt, intervalIntegral.integral_add ((hi00.sub hi10).sub hi01) hi11,
      intervalIntegral.integral_sub (hi00.sub hi10) hi01,
      intervalIntegral.integral_sub hi00 hi10]
  · intro f g hf hg
    have hiff := h_int hf hf
    have higg := h_int hg hg
    have hifg := h_int hf hg
    have hisub := h_int (hf.sub hg) (hf.sub hg)
    have h_nn : 0 ≤ windowEnergyNormSq Y f := by
      unfold windowEnergyNormSq windowPairing
      apply intervalIntegral.integral_nonneg hle
      intro X hX
      exact div_nonneg (mul_self_nonneg _) (by rw [Set.mem_Icc] at hX; linarith)
    have h_pos_fg : 2 * windowPairing Y f g ≤ windowEnergyNormSq Y f + windowEnergyNormSq Y g := by
      unfold windowEnergyNormSq windowPairing
      rw [← intervalIntegral.integral_const_mul, ← intervalIntegral.integral_add hiff higg]
      apply intervalIntegral.integral_mono_on hle (hifg.const_mul 2) (hiff.add higg)
      intro X hX
      have hX_pos : 0 < X := by rw [Set.mem_Icc] at hX; linarith
      have hsq : 2 * (f X * g X) ≤ f X * f X + g X * g X := by
        linarith [sq_nonneg (f X - g X),
          show f X * f X + g X * g X - 2 * (f X * g X) = (f X - g X) ^ 2 by ring]
      calc
        2 * (f X * g X / X) = (2 * (f X * g X)) / X := by ring
        _ ≤ (f X * f X + g X * g X) / X := div_le_div_of_nonneg_right hsq (le_of_lt hX_pos)
        _ = f X * f X / X + g X * g X / X := add_div _ _ _
    have h_neg_fg : -2 * windowPairing Y f g ≤ windowEnergyNormSq Y f + windowEnergyNormSq Y g := by
      unfold windowEnergyNormSq windowPairing
      rw [← intervalIntegral.integral_const_mul, ← intervalIntegral.integral_add hiff higg]
      apply intervalIntegral.integral_mono_on hle (hifg.const_mul (-2)) (hiff.add higg)
      intro X hX
      have hX_pos : 0 < X := by rw [Set.mem_Icc] at hX; linarith
      have hsq : -2 * (f X * g X) ≤ f X * f X + g X * g X := by
        linarith [sq_nonneg (f X + g X),
          show f X * f X + g X * g X - (-2 * (f X * g X)) = (f X + g X) ^ 2 by ring]
      calc
        -2 * (f X * g X / X) = (-2 * (f X * g X)) / X := by ring
        _ ≤ (f X * f X + g X * g X) / X := div_le_div_of_nonneg_right hsq (le_of_lt hX_pos)
        _ = f X * f X / X + g X * g X / X := add_div _ _ _
    have h_abs_fg : 2 * |windowPairing Y f g| ≤ windowEnergyNormSq Y f + windowEnergyNormSq Y g := by
      rcases le_or_lt 0 (windowPairing Y f g) with hp | hp
      · rw [abs_of_nonneg hp]; exact h_pos_fg
      · rw [abs_of_neg hp]; linarith
    have h_diff_sq :
        windowEnergyNormSq Y (fun X => f X - g X) ≤
          2 * windowEnergyNormSq Y f + 2 * windowEnergyNormSq Y g := by
      unfold windowEnergyNormSq windowPairing
      rw [← intervalIntegral.integral_const_mul, ← intervalIntegral.integral_const_mul,
        ← intervalIntegral.integral_add (hiff.const_mul 2) (higg.const_mul 2)]
      apply intervalIntegral.integral_mono_on hle hisub ((hiff.const_mul 2).add (higg.const_mul 2))
      intro X hX
      have hX_pos : 0 < X := by rw [Set.mem_Icc] at hX; linarith
      have hsq : (f X - g X) * (f X - g X) ≤ 2 * (f X * f X) + 2 * (g X * g X) := by
        linarith [sq_nonneg (f X + g X),
          show 2 * (f X * f X) + 2 * (g X * g X) - (f X - g X) * (f X - g X) =
            (f X + g X) ^ 2 by ring]
      calc
        (f X - g X) * (f X - g X) / X
          ≤ (2 * (f X * f X) + 2 * (g X * g X)) / X :=
            div_le_div_of_nonneg_right hsq (le_of_lt hX_pos)
        _ = 2 * (f X * f X / X) + 2 * (g X * g X / X) := by ring
    exact ⟨h_nn, h_abs_fg, h_diff_sq⟩

private theorem primePowerPairsUpTo_gcd_filter_eq_tc063_aux {m n T : ℕ}
    (hm1 : 1 ≤ m) (hmT : m ≤ T) (hn1 : 1 ≤ n) (_hnT : n ≤ T) :
    (primePowerPairsUpTo T).filter (fun pk => pk.1 ^ pk.2 ∣ Nat.gcd m n) =
      (primePowerPairsUpTo (min m n)).filter (fun pk => pk.1 ^ pk.2 ∣ Nat.gcd m n) := by
  have h_min_le_T : min m n ≤ T := le_trans (min_le_left m n) hmT
  have h_gcd_pos : 0 < Nat.gcd m n := Nat.gcd_pos_of_pos_left n hm1
  have h_gcd_le_min : Nat.gcd m n ≤ min m n :=
    le_min (Nat.le_of_dvd hm1 (Nat.gcd_dvd_left m n))
      (Nat.le_of_dvd hn1 (Nat.gcd_dvd_right m n))
  have h_k_le_two_pow : ∀ k : ℕ, k ≤ 2 ^ k := by
    intro k
    induction k with
    | zero => norm_num
    | succ k ih =>
      have hpos : 1 ≤ 2 ^ k := Nat.one_le_pow k 2 (by decide)
      omega
  ext ⟨p, k⟩
  simp only [primePowerPairsUpTo, primesUpToFinset, Finset.mem_filter,
    Finset.mem_product, Finset.mem_Icc, Finset.mem_range]
  constructor
  · rintro ⟨⟨⟨⟨_, hp_prime⟩, ⟨hk1, _⟩⟩, _⟩, hdvd⟩
    have hpk_le_gcd : p ^ k ≤ Nat.gcd m n := Nat.le_of_dvd h_gcd_pos hdvd
    have hpk_le_min : p ^ k ≤ min m n := le_trans hpk_le_gcd h_gcd_le_min
    have hp_le_pk : p ≤ p ^ k := by
      calc
        p = p ^ 1 := (pow_one p).symm
        _ ≤ p ^ k := Nat.pow_le_pow_right hp_prime.pos hk1
    have hk_le_pk : k ≤ p ^ k :=
      le_trans (h_k_le_two_pow k) (Nat.pow_le_pow_left hp_prime.two_le k)
    exact ⟨⟨⟨⟨by omega, hp_prime⟩, ⟨hk1, le_trans hk_le_pk hpk_le_min⟩⟩, hpk_le_min⟩, hdvd⟩
  · rintro ⟨⟨⟨⟨hp_lt, hp_prime⟩, ⟨hk1, hk_le⟩⟩, hpk_le⟩, hdvd⟩
    exact ⟨⟨⟨⟨by omega, hp_prime⟩, ⟨hk1, le_trans hk_le h_min_le_T⟩⟩,
      le_trans hpk_le h_min_le_T⟩, hdvd⟩

private theorem featureG_sum_windowPairing_eq_tc063_aux {Y : ℝ} (_hY2 : 2 ≤ Y)
    {T m n : ℕ} (hm1 : 1 ≤ m) (hmT : m ≤ T) (hn1 : 1 ≤ n) (hnT : n ≤ T) :
    (∑ pk ∈ primePowerPairsUpTo T,
        windowPairing Y (fun X => stationPrimePowerFeatureG m pk X)
          (fun X => stationPrimePowerFeatureG n pk X)) =
      commonPrimePowerLogSq m n * logWeightedWindowKernel 2 Y m n := by
  have h_each :
      ∀ pk ∈ primePowerPairsUpTo T,
        windowPairing Y (fun X => stationPrimePowerFeatureG m pk X)
            (fun X => stationPrimePowerFeatureG n pk X) =
          if pk.1 ^ pk.2 ∣ Nat.gcd m n then
            (Real.log (pk.1 : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y m n
          else 0 := by
    intro pk _
    by_cases hdm : pk.1 ^ pk.2 ∣ m
    · by_cases hdn : pk.1 ^ pk.2 ∣ n
      · have hdg : pk.1 ^ pk.2 ∣ Nat.gcd m n := Nat.dvd_gcd hdm hdn
        rw [if_pos hdg]
        unfold windowPairing stationPrimePowerFeatureG logWeightedWindowKernel
        simp only [hdm, hdn, ↓reduceIte]
        rw [← intervalIntegral.integral_const_mul]
        apply intervalIntegral.integral_congr
        intro X _
        ring
      · have hdg : ¬ pk.1 ^ pk.2 ∣ Nat.gcd m n := fun h => hdn (dvd_trans h (Nat.gcd_dvd_right m n))
        rw [if_neg hdg]
        unfold windowPairing stationPrimePowerFeatureG
        simp [hdm, hdn]
    · have hdg : ¬ pk.1 ^ pk.2 ∣ Nat.gcd m n := fun h => hdm (dvd_trans h (Nat.gcd_dvd_left m n))
      rw [if_neg hdg]
      unfold windowPairing stationPrimePowerFeatureG
      simp [hdm]
  rw [Finset.sum_congr rfl h_each, ← Finset.sum_filter,
    primePowerPairsUpTo_gcd_filter_eq_tc063_aux hm1 hmT hn1 hnT, ← Finset.sum_mul]
  rfl

private theorem hcal_offdiag_eq_psi_sub_four_featureG_tc063_aux {Y : ℝ} (hY2 : 2 ≤ Y)
    (c_lam c_half : ℝ) {T D0 a b : ℕ}
    (ha1 : 1 ≤ a) (haT : a ≤ T) (hb1 : 1 ≤ b) (hbT : b ≤ T) (hab : a ≠ b) :
    completeSignedKernelHcal c_lam c_half T D0 Y a b =
      windowPairing Y (adjustedStationProfilePsi c_lam c_half T D0 a)
          (adjustedStationProfilePsi c_lam c_half T D0 b) -
        4 * ∑ pk ∈ primePowerPairsUpTo T,
          windowPairing Y (fun X => stationPrimePowerFeatureG a pk X)
            (fun X => stationPrimePowerFeatureG b pk X) := by
  rw [featureG_sum_windowPairing_eq_tc063_aux hY2 ha1 haT hb1 hbT]
  obtain ⟨_, hprops⟩ := uIcc_window_props_tc063_aux hY2
  have hlog_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
    ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hprops X hX).1)
  have h_int_nu :
      ∀ ν : ℕ,
        IntervalIntegrable
          (fun X => (gaussianTermPhi a X * gaussianTermPhi b X / (Real.log X) ^ ν) / X)
          volume Y (RiemannScope.tau * Y) := by
    intro ν
    exact ((((continuousOn_gaussianTermPhi_tc063_aux Y a).mul
      (continuousOn_gaussianTermPhi_tc063_aux Y b)).div
      (hlog_cont.pow ν) (fun X hX => pow_ne_zero ν (hprops X hX).2.2.1)).div
      continuousOn_id (fun X hX => ne_of_gt (hprops X hX).1)).intervalIntegrable
  have hi0 := h_int_nu 0
  have hi2 := h_int_nu 2
  have hi4 := h_int_nu 4
  let ba := signedAdjustedCoeffB c_lam c_half T D0 a
  let bb := signedAdjustedCoeffB c_lam c_half T D0 b
  have h_psi_pair :
      windowPairing Y (adjustedStationProfilePsi c_lam c_half T D0 a)
          (adjustedStationProfilePsi c_lam c_half T D0 b) =
        logWeightedWindowKernel 0 Y a b -
          (ba + bb) * logWeightedWindowKernel 2 Y a b +
          (ba * bb) * logWeightedWindowKernel 4 Y a b := by
    unfold windowPairing adjustedStationProfilePsi logWeightedWindowKernel
    have h_congr :
        ∫ X in Y..(RiemannScope.tau * Y),
            ((1 - ba / (Real.log X) ^ 2) * gaussianTermPhi a X) *
              ((1 - bb / (Real.log X) ^ 2) * gaussianTermPhi b X) / X =
          ∫ X in Y..(RiemannScope.tau * Y),
            ((gaussianTermPhi a X * gaussianTermPhi b X / (Real.log X) ^ 0) / X -
              (ba + bb) * ((gaussianTermPhi a X * gaussianTermPhi b X / (Real.log X) ^ 2) / X)) +
              (ba * bb) * ((gaussianTermPhi a X * gaussianTermPhi b X / (Real.log X) ^ 4) / X) := by
      apply intervalIntegral.integral_congr
      intro X hX
      have hX_ne : X ≠ 0 := ne_of_gt (hprops X hX).1
      have hlog_ne : Real.log X ≠ 0 := (hprops X hX).2.2.1
      simp only [pow_zero, div_one]
      field_simp [hlog_ne, hX_ne]
      ring
    change ∫ X in Y..(RiemannScope.tau * Y),
        ((1 - ba / (Real.log X) ^ 2) * gaussianTermPhi a X) *
          ((1 - bb / (Real.log X) ^ 2) * gaussianTermPhi b X) / X = _
    rw [h_congr, intervalIntegral.integral_add (hi0.sub (hi2.const_mul (ba + bb))) (hi4.const_mul (ba * bb)),
      intervalIntegral.integral_sub hi0 (hi2.const_mul (ba + bb)),
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul]
  rw [h_psi_pair]
  unfold completeSignedKernelHcal cutoffIndicatorT
  have h_in2T : (1 ≤ a ∧ a ≤ 2 * T) ∧ (1 ≤ b ∧ b ≤ 2 * T) := ⟨⟨ha1, by omega⟩, ⟨hb1, by omega⟩⟩
  rw [if_pos h_in2T, if_pos ⟨ha1, haT⟩, if_pos ⟨hb1, hbT⟩, if_neg hab]
  dsimp [ba, bb]
  ring

private theorem distinct_anchors_disjoint_shifts_tc063_aux (T : ℕ) :
    Disjoint (primeInteriorTruncatedAnchors 2 T)
        ((primeInteriorTruncatedAnchors 2 T).image (fun m => 2 * m)) ∧
      (∀ m ∈ primeInteriorTruncatedAnchors 2 T,
        ∀ n ∈ (primeInteriorTruncatedAnchors 2 T).erase m,
          m ≠ n ∧ m ≠ 2 * n ∧ 2 * m ≠ n ∧ 2 * m ≠ 2 * n ∧
            1 ≤ m ∧ 2 * m ≤ T ∧ 1 ≤ n ∧ 2 * n ≤ T) := by
  have h_disj :
      Disjoint (primeInteriorTruncatedAnchors 2 T)
        ((primeInteriorTruncatedAnchors 2 T).image (fun m => 2 * m)) := by
    rw [Finset.disjoint_left]
    intro k hk1 hk2
    simp only [primeInteriorTruncatedAnchors, primeEvenValuationAnchors,
      Finset.mem_filter, Finset.mem_Icc, Finset.mem_image] at hk1 hk2
    rcases hk1 with ⟨⟨⟨_, _⟩, hk_ev⟩, _⟩
    rcases hk2 with ⟨m, ⟨⟨⟨hm1, _⟩, hm_ev⟩, _⟩, rfl⟩
    have hm_ne : m ≠ 0 := by omega
    rw [Nat.factorization_mul (by decide : 2 ≠ 0) hm_ne, Finsupp.add_apply,
      Nat.Prime.factorization_self Nat.prime_two] at hk_ev
    obtain ⟨r1, hr1⟩ := hm_ev
    obtain ⟨r2, hr2⟩ := hk_ev
    omega
  refine ⟨h_disj, ?_⟩
  intro m hm n hn
  have hn_ne_m : n ≠ m := (Finset.mem_erase.mp hn).1
  have hn_in : n ∈ primeInteriorTruncatedAnchors 2 T := Finset.mem_of_mem_erase hn
  have hm_bds := hm
  have hn_bds := hn_in
  simp only [primeInteriorTruncatedAnchors, primeEvenValuationAnchors,
    Finset.mem_filter, Finset.mem_Icc] at hm_bds hn_bds
  have hm_not_2n : m ≠ 2 * n := by
    intro h_eq
    exact Finset.disjoint_left.mp h_disj hm (Finset.mem_image.mpr ⟨n, hn_in, h_eq.symm⟩)
  have h2m_not_n : 2 * m ≠ n := by
    intro h_eq
    exact Finset.disjoint_left.mp h_disj hn_in (Finset.mem_image.mpr ⟨m, hm, h_eq⟩)
  exact ⟨hn_ne_m.symm, hm_not_2n, h2m_not_n, by omega,
    hm_bds.1.1.1, hm_bds.2, hn_bds.1.1.1, hn_bds.2⟩

private theorem sum_anchor_pair_le_sum_Icc_tc063_aux (T : ℕ) {f : ℕ → ℝ}
    (hf_nn : ∀ n ∈ Finset.Icc 1 T, 0 ≤ f n) :
    (∑ m ∈ primeInteriorTruncatedAnchors 2 T, (f m + f (2 * m))) ≤
      ∑ n ∈ Finset.Icc 1 T, f n := by
  obtain ⟨h_disj, _⟩ := distinct_anchors_disjoint_shifts_tc063_aux T
  have h_sub : coveredInteriorStations 2 T ⊆ Finset.Icc 1 T := by
    intro k hk
    simp only [coveredInteriorStations, Finset.mem_union, Finset.mem_image,
      primeInteriorTruncatedAnchors, primeEvenValuationAnchors, Finset.mem_filter,
      Finset.mem_Icc] at hk ⊢
    rcases hk with ⟨⟨⟨hk1, _⟩, _⟩, h2k⟩ | ⟨m, ⟨⟨⟨hm1, _⟩, _⟩, h2m⟩, rfl⟩
    · exact ⟨hk1, by omega⟩
    · exact ⟨by omega, h2m⟩
  have h_cov_eq :
      (∑ n ∈ coveredInteriorStations 2 T, f n) =
        ∑ m ∈ primeInteriorTruncatedAnchors 2 T, (f m + f (2 * m)) := by
    unfold coveredInteriorStations
    rw [Finset.sum_union h_disj, Finset.sum_image (fun m1 _ m2 _ h => by omega),
      ← Finset.sum_add_distrib]
  rw [← h_cov_eq]
  exact Finset.sum_le_sum_of_subset_of_nonneg h_sub (fun n hn _ => hf_nn n hn)

private theorem finite_hilbert_erase_bound_tc063_aux (J : Finset ℕ) {L : ℕ}
    (hL1 : 1 ≤ L) (hJ_card : J.card ≤ L) (ip : ℕ → ℕ → ℝ) (nsq : ℕ → ℝ)
    (h_nsq_nn : ∀ j ∈ J, 0 ≤ nsq j)
    (h_cs : ∀ j ∈ J, ∀ k ∈ J.erase j, 2 * |ip j k| ≤ nsq j + nsq k) :
    |∑ j ∈ J, ∑ k ∈ J.erase j, ip j k| ≤ ((L : ℝ) - 1) * ∑ j ∈ J, nsq j := by
  have h_tri :
      |∑ j ∈ J, ∑ k ∈ J.erase j, ip j k| ≤
        ∑ j ∈ J, ∑ k ∈ J.erase j, |ip j k| := by
    calc
      |∑ j ∈ J, ∑ k ∈ J.erase j, ip j k|
        ≤ ∑ j ∈ J, |∑ k ∈ J.erase j, ip j k| := Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ j ∈ J, ∑ k ∈ J.erase j, |ip j k| :=
          Finset.sum_le_sum (fun _ _ => Finset.abs_sum_le_sum_abs _ _)
  have h_double :
      2 * (∑ j ∈ J, ∑ k ∈ J.erase j, |ip j k|) ≤
        ∑ j ∈ J, ∑ k ∈ J.erase j, (nsq j + nsq k) := by
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro j hj
    rw [Finset.mul_sum]
    exact Finset.sum_le_sum (fun k hk => h_cs j hj k hk)
  have h_symm_sum :
      (∑ j ∈ J, ∑ k ∈ J.erase j, (nsq j + nsq k)) =
        2 * ∑ j ∈ J, ((J.erase j).card : ℝ) * nsq j := by
    have h_s1 :
        (∑ j ∈ J, ∑ _k ∈ J.erase j, nsq j) =
          ∑ j ∈ J, ((J.erase j).card : ℝ) * nsq j := by
      apply Finset.sum_congr rfl
      intro j _; simp
    have h_s2 :
        (∑ j ∈ J, ∑ k ∈ J.erase j, nsq k) =
          ∑ k ∈ J, ((J.erase k).card : ℝ) * nsq k := by
      have h_ite1 :
          (∑ j ∈ J, ∑ k ∈ J.erase j, nsq k) =
            ∑ j ∈ J, ∑ k ∈ J, (if k = j then 0 else nsq k) := by
        apply Finset.sum_congr rfl
        intro j hj
        symm
        rw [← Finset.add_sum_erase _ _ hj, if_pos rfl, zero_add]
        apply Finset.sum_congr rfl
        intro k hk; rw [if_neg (Finset.mem_erase.mp hk).1]
      rw [h_ite1, Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro k hk
      rw [← Finset.add_sum_erase _ _ hk, if_pos rfl, zero_add]
      have h_er :
          (∑ j ∈ J.erase k, if k = j then 0 else nsq k) =
            ∑ _j ∈ J.erase k, nsq k := by
        apply Finset.sum_congr rfl
        intro j hj; rw [if_neg (Finset.mem_erase.mp hj).1.symm]
      rw [h_er]; simp
    have h_split_add :
        (∑ j ∈ J, ∑ k ∈ J.erase j, (nsq j + nsq k)) =
          (∑ j ∈ J, ∑ _k ∈ J.erase j, nsq j) + (∑ j ∈ J, ∑ k ∈ J.erase j, nsq k) := by
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro j _; exact Finset.sum_add_distrib
    rw [h_split_add, h_s1, h_s2]
    ring
  have h_card_le :
      (∑ j ∈ J, ((J.erase j).card : ℝ) * nsq j) ≤ ((L : ℝ) - 1) * ∑ j ∈ J, nsq j := by
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro j hj
    have hc : (J.erase j).card ≤ L - 1 := by
      rw [Finset.card_erase_of_mem hj]
      omega
    have hc_r : ((J.erase j).card : ℝ) ≤ (L : ℝ) - 1 := by
      calc
        ((J.erase j).card : ℝ) ≤ ((L - 1 : ℕ) : ℝ) := by exact_mod_cast hc
        _ = (L : ℝ) - 1 := by rw [Nat.cast_sub hL1, Nat.cast_one]
    exact mul_le_mul_of_nonneg_right hc_r (h_nsq_nn j hj)
  linarith

private theorem maxDyadicChainLength_canonical_bounds_tc063_aux {Y : ℝ} (hY2 : 2 ≤ Y) :
    1 ≤ maxDyadicChainLength (canonicalCutoffT Y) ∧
      ((maxDyadicChainLength (canonicalCutoffT Y) : ℝ) - 1) ≤ 1 + Real.log Y := by
  let T := canonicalCutoffT Y
  have hY_gt1 : (1 : ℝ) < Y := by linarith
  have h2_lt_rpow : (2 : ℝ) < Y ^ (5 / 4 : ℝ) := by
    have h2_lt : (2 : ℝ) ^ (1 : ℝ) < (2 : ℝ) ^ (5 / 4 : ℝ) :=
      Real.rpow_lt_rpow_of_exponent_lt (by norm_num) (by norm_num)
    rw [Real.rpow_one] at h2_lt
    exact lt_of_lt_of_le h2_lt (Real.rpow_le_rpow (by norm_num) hY2 (by norm_num))
  have h_le_ceil : Y ^ (5 / 4 : ℝ) ≤ (T : ℝ) := Nat.le_ceil _
  have hT_gt2_r : (2 : ℝ) < (T : ℝ) := lt_of_lt_of_le h2_lt_rpow h_le_ceil
  have hT_ge3 : 3 ≤ T := by
    have h2_lt_T : 2 < T := by exact_mod_cast hT_gt2_r
    omega
  have h1_in_odd : 1 ∈ oddChainParts T := by
    simp only [oddChainParts, Finset.mem_filter, Finset.mem_Icc]
    exact ⟨⟨le_refl 1, by omega⟩, odd_one, by omega⟩
  have h0_in_1 : 0 ∈ dyadicChainExponents 1 T := by
    rw [mem_dyadicChainExponents_iff_tc063_aux (le_refl 1) 0 T]
    omega
  have h_max_eq_1 : maxDyadicChainLength T = (dyadicChainExponents 1 T).card := by
    unfold maxDyadicChainLength
    apply le_antisymm
    · apply Finset.sup_le
      intro u hu
      have hu1 : 1 ≤ u := (Finset.mem_Icc.mp (Finset.mem_filter.mp hu).1).1
      apply Finset.card_le_card
      intro j hj
      rw [mem_dyadicChainExponents_iff_tc063_aux hu1 j T] at hj
      rw [mem_dyadicChainExponents_iff_tc063_aux (le_refl 1) j T]
      calc
        2 * 4 ^ j * 1 = 2 * 4 ^ j := by ring
        _ ≤ 2 * 4 ^ j * u := Nat.le_mul_of_pos_right _ hu1
        _ ≤ T := hj
    · exact Finset.le_sup (f := fun u => (dyadicChainExponents u T).card) h1_in_odd
  let L := maxDyadicChainLength T
  have hL_ge1 : 1 ≤ L := by
    change 1 ≤ maxDyadicChainLength T
    rw [h_max_eq_1]
    exact Finset.card_pos.mpr ⟨0, h0_in_1⟩
  refine ⟨hL_ge1, ?_⟩
  have hLm1_in : L - 1 ∈ dyadicChainExponents 1 T := by
    by_contra h_not
    have h_sub_range : dyadicChainExponents 1 T ⊆ Finset.range (L - 1) := by
      intro j hj
      rw [Finset.mem_range]
      by_contra h_ge
      have hj_ge : L - 1 ≤ j := by omega
      rw [mem_dyadicChainExponents_iff_tc063_aux (le_refl 1) j T] at hj
      have h4_le : 4 ^ (L - 1) ≤ 4 ^ j := Nat.pow_le_pow_right (by decide) hj_ge
      have hLm1_le : 2 * 4 ^ (L - 1) * 1 ≤ T := by linarith
      exact h_not ((mem_dyadicChainExponents_iff_tc063_aux (le_refl 1) (L - 1) T).mpr hLm1_le)
    have h_card_lt : (dyadicChainExponents 1 T).card ≤ L - 1 := by
      simpa using Finset.card_le_card h_sub_range
    rw [← h_max_eq_1] at h_card_lt
    change L ≤ L - 1 at h_card_lt
    omega
  have h2_4L_le_T : 2 * 4 ^ (L - 1) ≤ T := by
    have h := (mem_dyadicChainExponents_iff_tc063_aux (le_refl 1) (L - 1) T).mp hLm1_in
    omega
  have hT_lt : (T : ℝ) < Y ^ (5 / 4 : ℝ) + 1 :=
    Nat.ceil_lt_add_one (le_of_lt (lt_trans (by norm_num) h2_lt_rpow))
  have h4_lt : (4 : ℝ) ^ (L - 1) < Y ^ (5 / 4 : ℝ) := by
    have h_cast : (2 : ℝ) * (4 : ℝ) ^ (L - 1) ≤ (T : ℝ) := by exact_mod_cast h2_4L_le_T
    linarith
  have hlog4_gt : (5 / 4 : ℝ) < Real.log 4 := by
    have h_exp_neg : (27 / 32 : ℝ) ≤ Real.exp (-5 / 32 : ℝ) := by
      have h := Real.add_one_le_exp (-5 / 32 : ℝ)
      linarith
    have h_pow4 : (27 / 32 : ℝ) ^ 4 ≤ Real.exp (-5 / 8 : ℝ) := by
      have hp := pow_le_pow_left (by norm_num) h_exp_neg 4
      have hexp4 : (Real.exp (-5 / 32 : ℝ)) ^ 4 = Real.exp (-5 / 8 : ℝ) := by
        rw [← Real.exp_nat_mul]
        congr 1; norm_num
      rwa [hexp4] at hp
    have h_half_lt : (1 / 2 : ℝ) < Real.exp (-5 / 8 : ℝ) :=
      lt_of_lt_of_le (by norm_num : (1 / 2 : ℝ) < (27 / 32 : ℝ) ^ 4) h_pow4
    have h_exp_lt2 : Real.exp (5 / 8 : ℝ) < 2 := by
      have h_prod : Real.exp (-5 / 8 : ℝ) * Real.exp (5 / 8 : ℝ) = 1 := by
        rw [← Real.exp_add]; norm_num
      have hpos : 0 < Real.exp (5 / 8 : ℝ) := Real.exp_pos _
      nlinarith [h_half_lt, h_prod, hpos]
    have h_log2 : (5 / 8 : ℝ) < Real.log 2 := by
      have h := Real.log_lt_log (Real.exp_pos _) h_exp_lt2
      rwa [Real.log_exp] at h
    have h_log4_eq : Real.log (4 : ℝ) = 2 * Real.log 2 := by
      rw [show (4 : ℝ) = (2 : ℝ) ^ (2 : ℕ) by norm_num, Real.log_pow]
      ring
    linarith
  have h_log_pow : ((L : ℝ) - 1) * Real.log 4 < (5 / 4 : ℝ) * Real.log Y := by
    have h_lt := Real.log_lt_log (pow_pos (by norm_num) (L - 1)) h4_lt
    rw [Real.log_pow, Real.log_rpow (by linarith), Nat.cast_sub hL_ge1, Nat.cast_one] at h_lt
    exact h_lt
  have hlogY_pos : 0 < Real.log Y := Real.log_pos hY_gt1
  have h_rhs_lt : (5 / 4 : ℝ) * Real.log Y < Real.log 4 * Real.log Y :=
    mul_lt_mul_of_pos_right hlog4_gt hlogY_pos
  nlinarith

private theorem log_linear_le_rpow_tc063_aux {C : ℝ} (hC : 0 ≤ C) {eta : ℝ} (heta : 0 < eta) :
    ∃ a_eta : ℝ, 0 ≤ a_eta ∧ ∀ Y : ℝ, 2 ≤ Y → C * (1 + Real.log Y) ≤ a_eta * Y ^ eta := by
  let a_eta : ℝ := C * (1 + 2 / eta)
  have ha_nn : 0 ≤ a_eta := by dsimp [a_eta]; positivity
  refine ⟨a_eta, ha_nn, ?_⟩
  intro Y hY2
  have hY_pos : 0 < Y := by linarith
  have hY_ge1 : (1 : ℝ) ≤ Y := by linarith
  have h1_le : 1 ≤ Y ^ eta := Real.one_le_rpow hY_ge1 (le_of_lt heta)
  have h_half_le : Y ^ (eta / 2) ≤ Y ^ eta :=
    Real.rpow_le_rpow_of_exponent_le hY_ge1 (by linarith)
  have h_log_le : Real.log Y ≤ (2 / eta) * Y ^ eta := by
    have h_exp := Real.add_one_le_exp (Real.log Y * (eta / 2))
    rw [← Real.rpow_def_of_pos hY_pos (eta / 2)] at h_exp
    have h_u : Real.log Y * (eta / 2) ≤ Y ^ eta := by linarith
    have h_div := (le_div_iff (show 0 < eta / 2 by linarith)).mpr h_u
    calc
      Real.log Y ≤ Y ^ eta / (eta / 2) := h_div
      _ = (2 / eta) * Y ^ eta := by field_simp [ne_of_gt heta]; ring
  calc
    C * (1 + Real.log Y)
      ≤ C * (Y ^ eta + (2 / eta) * Y ^ eta) :=
        mul_le_mul_of_nonneg_left (add_le_add h1_le h_log_le) hC
    _ = a_eta * Y ^ eta := by dsimp [a_eta]; ring

/-- **Theorem 3 (`TASK-TC-063` §4, Shifted-Station Disjointness, Complete-Kernel `<U_m, U_n> - 4<V_m, V_n>` Off-Diagonal Formula, Uniform Norm-Sum Bounds, Finite Hilbert Bound on `canonicalSameOddChainSumS`, and Closure Equivalence onto `canonicalDifferentOddChainSumS`)**:
    Let `C_g := 186 * (RiemannScope.tau - 1)`.
    1. *Shifted-station disjointness on distinct dyadic anchors*:
       `Disjoint (primeInteriorTruncatedAnchors 2 T) ((primeInteriorTruncatedAnchors 2 T).image (fun m => 2 * m))`,
       and `m ≠ n ∧ m ≠ 2 * n ∧ 2 * m ≠ n ∧ 2 * m ≠ 2 * n` on distinct anchors in `primeInteriorTruncatedAnchors 2 T`;
    2. *Prime-power feature Gram identity & `<U_m, U_n> - 4<V_m, V_n>` complete-kernel formula (`2 ≤ Y`)*:
       `∑_{pk ∈ primePowerPairsUpTo T} <g_{m,pk}, g_{n,pk}>_Y = commonPrimePowerLogSq m n * logWeightedWindowKernel 2 Y m n`
       (`1 ≤ m, n ≤ T`), and on distinct anchors `m ≠ n` in `primeInteriorTruncatedAnchors 2 T`:
       `anchorFourTermDiffHcal c_lam c_half T D0 Y m n = <U_m, U_n>_Y - 4 * ∑_{pk} <V_{m,pk}, V_{n,pk}>_Y`;
    3. *Uniform norm-sum bounds (`2 ≤ Y`)*:
       `∑_{m ∈ I_2(T)} ‖U_m‖_Y^2 ≤ 2 * ∑_{n=1}^T ‖ψ_n‖_Y^2` and
       `∑_{m ∈ I_2(T)} ∑_{pk} ‖V_{m,pk}‖_Y^2 ≤ 2 * ∑_{n=1}^T (log n)^2 G_Y^{[2]}(n, n) ≤ 2 * C_g`;
    4. *Finite Hilbert inequality & unconditional `O(1 + log Y)` bound on `canonicalSameOddChainSumS` for all real `Y ≥ 2`*:
       `|canonicalSameOddChainSumS c_lam c_half Y| ≤ ((maxDyadicChainLength (canonicalCutoffT Y) : ℝ) - 1) * (2 * C_psi + 8 * C_g) ≤ (2 * C_psi + 8 * C_g) * (1 + Real.log Y)`;
    5. *`Y^η` absorption, two-way `MixedCovarianceClosureHypothesis` equivalence onto `canonicalDifferentOddChainSumS`, and conditional Route D transfer to `canonicalLiouvilleEnergyE Z ≤ C_tot * Z ^ ε`*. -/
theorem uniform_same_chain_hilbert_bound_and_closure_transfer_tc063 :
    let C_g : ℝ := 186 * (RiemannScope.tau - 1)
    (∀ (T : ℕ),
      Disjoint (primeInteriorTruncatedAnchors 2 T)
          ((primeInteriorTruncatedAnchors 2 T).image (fun m => 2 * m)) ∧
        (∀ m ∈ primeInteriorTruncatedAnchors 2 T,
          ∀ n ∈ (primeInteriorTruncatedAnchors 2 T).erase m,
            m ≠ n ∧ m ≠ 2 * n ∧ 2 * m ≠ n ∧ 2 * m ≠ 2 * n ∧
              1 ≤ m ∧ 2 * m ≤ T ∧ 1 ≤ n ∧ 2 * n ≤ T)) ∧
    ((∀ {Y : ℝ}, 2 ≤ Y → ∀ {T m n : ℕ}, 1 ≤ m → m ≤ T → 1 ≤ n → n ≤ T →
        (∑ pk ∈ primePowerPairsUpTo T,
          windowPairing Y (fun X => stationPrimePowerFeatureG m pk X)
            (fun X => stationPrimePowerFeatureG n pk X)) =
          commonPrimePowerLogSq m n * logWeightedWindowKernel 2 Y m n) ∧
      (∀ {Y : ℝ}, 2 ≤ Y → ∀ (c_lam c_half : ℝ) (T D0 : ℕ),
        ∀ m ∈ primeInteriorTruncatedAnchors 2 T,
          ∀ n ∈ (primeInteriorTruncatedAnchors 2 T).erase m,
            anchorFourTermDiffHcal c_lam c_half T D0 Y m n =
              windowPairing Y (stationAdjustedDiffU c_lam c_half T D0 m)
                  (stationAdjustedDiffU c_lam c_half T D0 n) -
                4 * ∑ pk ∈ primePowerPairsUpTo T,
                  windowPairing Y (fun X => stationFeatureDiffV m pk X)
                    (fun X => stationFeatureDiffV n pk X))) ∧
    ((∀ {Y : ℝ}, 2 ≤ Y → ∀ (c_lam c_half : ℝ) (T D0 : ℕ),
        (∑ m ∈ primeInteriorTruncatedAnchors 2 T,
          windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 m)) ≤
          2 * ∑ n ∈ Finset.Icc 1 T,
            windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 n)) ∧
      (∀ {Y : ℝ}, 2 ≤ Y → ∀ (T : ℕ),
        (∑ m ∈ primeInteriorTruncatedAnchors 2 T,
          ∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => stationFeatureDiffV m pk X)) ≤
          2 * ∑ n ∈ Finset.Icc 1 T,
            (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n ∧
        2 * (∑ n ∈ Finset.Icc 1 T,
            (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n) ≤
          2 * C_g)) ∧
    ((∀ (J : Finset ℕ) {L : ℕ}, 1 ≤ L → J.card ≤ L →
        ∀ (ip : ℕ → ℕ → ℝ) (nsq : ℕ → ℝ),
          (∀ j ∈ J, 0 ≤ nsq j) →
          (∀ j ∈ J, ∀ k ∈ J.erase j, 2 * |ip j k| ≤ nsq j + nsq k) →
            |∑ j ∈ J, ∑ k ∈ J.erase j, ip j k| ≤ ((L : ℝ) - 1) * ∑ j ∈ J, nsq j) ∧
      (∀ {Y : ℝ}, 2 ≤ Y →
        1 ≤ maxDyadicChainLength (canonicalCutoffT Y) ∧
          ((maxDyadicChainLength (canonicalCutoffT Y) : ℝ) - 1) ≤ 1 + Real.log Y) ∧
      (∀ (c_lam c_half : ℝ),
        ∃ C_psi : ℝ, 0 ≤ C_psi ∧
          ∀ {Y : ℝ}, 2 ≤ Y →
            (∑ n ∈ Finset.Icc 1 (canonicalCutoffT Y),
              windowEnergyNormSq Y
                (adjustedStationProfilePsi c_lam c_half
                  (canonicalCutoffT Y) (Nat.floor (Real.log Y)) n)) ≤ C_psi ∧
            (∑ m ∈ primeInteriorTruncatedAnchors 2 (canonicalCutoffT Y),
              windowEnergyNormSq Y
                (stationAdjustedDiffU c_lam c_half
                  (canonicalCutoffT Y) (Nat.floor (Real.log Y)) m)) ≤ 2 * C_psi ∧
            |canonicalSameOddChainSumS c_lam c_half Y| ≤
              ((maxDyadicChainLength (canonicalCutoffT Y) : ℝ) - 1) *
                (2 * C_psi + 8 * C_g) ∧
            ((maxDyadicChainLength (canonicalCutoffT Y) : ℝ) - 1) *
                (2 * C_psi + 8 * C_g) ≤
              (2 * C_psi + 8 * C_g) * (1 + Real.log Y))) ∧
    ((∀ {C : ℝ}, 0 ≤ C → ∀ {eta : ℝ}, 0 < eta →
        ∃ a_eta : ℝ, 0 ≤ a_eta ∧ ∀ Y : ℝ, 2 ≤ Y → C * (1 + Real.log Y) ≤ a_eta * Y ^ eta) ∧
      (∀ (c_lam c_half : ℝ),
        MixedCovarianceClosureHypothesis
            (canonicalInteriorOffDiagSigma c_lam c_half 2) canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalDifferentOddChainSumS c_lam c_half) canonicalPrimePowerDiagDtilde) ∧
      ((MixedCovarianceClosureHypothesis
            (canonicalInteriorOffDiagSigma
              actualSelbergConstantCLam actualSquarePoleConstantCHalf 2)
            canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalDifferentOddChainSumS
              actualSelbergConstantCLam actualSquarePoleConstantCHalf)
            canonicalPrimePowerDiagDtilde) ∧
        (MixedCovarianceClosureHypothesis
            (canonicalSignedMixedCovarianceJ
              actualSelbergConstantCLam actualSquarePoleConstantCHalf)
            canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalDifferentOddChainSumS
              actualSelbergConstantCLam actualSquarePoleConstantCHalf)
            canonicalPrimePowerDiagDtilde)) ∧
      (∀ {M_lin : ℝ},
        0 ≤ M_lin →
        (∀ Z : ℝ, 1 ≤ Z → canonicalLiouvilleEnergyE Z ≤ M_lin * Z) →
        MixedCovarianceClosureHypothesis
          (canonicalDifferentOddChainSumS
            actualSelbergConstantCLam actualSquarePoleConstantCHalf)
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
          ∃ C_tot : ℝ, 0 ≤ C_tot ∧ ∀ Z : ℝ, 1 ≤ Z → canonicalLiouvilleEnergyE Z ≤ C_tot * Z ^ ε)) := by
  intro C_g
  have hCg_pos : 0 < C_g :=
    (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2.1
  have h_part2b :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ (c_lam c_half : ℝ) (T D0 : ℕ),
        ∀ m ∈ primeInteriorTruncatedAnchors 2 T,
          ∀ n ∈ (primeInteriorTruncatedAnchors 2 T).erase m,
            anchorFourTermDiffHcal c_lam c_half T D0 Y m n =
              windowPairing Y (stationAdjustedDiffU c_lam c_half T D0 m)
                  (stationAdjustedDiffU c_lam c_half T D0 n) -
                4 * ∑ pk ∈ primePowerPairsUpTo T,
                  windowPairing Y (fun X => stationFeatureDiffV m pk X)
                    (fun X => stationFeatureDiffV n pk X) := by
    intro Y hY2 c_lam c_half T D0 m hm n hn
    obtain ⟨_, h_sep⟩ := distinct_anchors_disjoint_shifts_tc063_aux T
    obtain ⟨hmn, hm_2n, h2m_n, h2m_2n, hm1, h2mT, hn1, h2nT⟩ := h_sep m hm n hn
    have hmT : m ≤ T := by omega
    have hnT : n ≤ T := by omega
    have h2m1 : 1 ≤ 2 * m := by omega
    have h2n1 : 1 ≤ 2 * n := by omega
    obtain ⟨h_bilin, _⟩ := windowPairing_bilinear_and_cauchy_tc063_aux hY2
    unfold anchorFourTermDiffHcal stationAdjustedDiffU stationFeatureDiffV
    rw [hcal_offdiag_eq_psi_sub_four_featureG_tc063_aux hY2 c_lam c_half hm1 hmT hn1 hnT hmn,
      hcal_offdiag_eq_psi_sub_four_featureG_tc063_aux hY2 c_lam c_half h2m1 h2mT hn1 hnT h2m_n,
      hcal_offdiag_eq_psi_sub_four_featureG_tc063_aux hY2 c_lam c_half hm1 hmT h2n1 h2nT hm_2n,
      hcal_offdiag_eq_psi_sub_four_featureG_tc063_aux hY2 c_lam c_half h2m1 h2mT h2n1 h2nT h2m_2n,
      h_bilin
        (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 m (2, 1)).1
        (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 (2 * m) (2, 1)).1
        (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 n (2, 1)).1
        (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 (2 * n) (2, 1)).1]
    have h_pk_diff :
        (∑ pk ∈ primePowerPairsUpTo T,
            windowPairing Y
              (fun X => stationPrimePowerFeatureG m pk X - stationPrimePowerFeatureG (2 * m) pk X)
              (fun X => stationPrimePowerFeatureG n pk X - stationPrimePowerFeatureG (2 * n) pk X)) =
          (∑ pk ∈ primePowerPairsUpTo T,
              windowPairing Y (stationPrimePowerFeatureG m pk) (stationPrimePowerFeatureG n pk)) -
            (∑ pk ∈ primePowerPairsUpTo T,
              windowPairing Y (stationPrimePowerFeatureG (2 * m) pk) (stationPrimePowerFeatureG n pk)) -
            (∑ pk ∈ primePowerPairsUpTo T,
              windowPairing Y (stationPrimePowerFeatureG m pk) (stationPrimePowerFeatureG (2 * n) pk)) +
            (∑ pk ∈ primePowerPairsUpTo T,
              windowPairing Y (stationPrimePowerFeatureG (2 * m) pk)
                (stationPrimePowerFeatureG (2 * n) pk)) := by
      have h_each :
          ∀ pk ∈ primePowerPairsUpTo T,
            windowPairing Y
                (fun X => stationPrimePowerFeatureG m pk X - stationPrimePowerFeatureG (2 * m) pk X)
                (fun X => stationPrimePowerFeatureG n pk X - stationPrimePowerFeatureG (2 * n) pk X) =
              windowPairing Y (stationPrimePowerFeatureG m pk) (stationPrimePowerFeatureG n pk) -
                windowPairing Y (stationPrimePowerFeatureG (2 * m) pk) (stationPrimePowerFeatureG n pk) -
                windowPairing Y (stationPrimePowerFeatureG m pk) (stationPrimePowerFeatureG (2 * n) pk) +
                windowPairing Y (stationPrimePowerFeatureG (2 * m) pk)
                  (stationPrimePowerFeatureG (2 * n) pk) :=
        fun pk _ => h_bilin
          (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 m pk).2
          (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 (2 * m) pk).2
          (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 n pk).2
          (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 (2 * n) pk).2
      rw [Finset.sum_congr rfl h_each, Finset.sum_add_distrib, Finset.sum_sub_distrib,
        Finset.sum_sub_distrib]
    rw [h_pk_diff]
    ring
  have h_norm_U :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ (c_lam c_half : ℝ) (T D0 : ℕ),
        (∑ m ∈ primeInteriorTruncatedAnchors 2 T,
          windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 m)) ≤
          2 * ∑ n ∈ Finset.Icc 1 T,
            windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 n) := by
    intro Y hY2 c_lam c_half T D0
    obtain ⟨_, h_cs⟩ := windowPairing_bilinear_and_cauchy_tc063_aux hY2
    have h_each :
        ∀ m ∈ primeInteriorTruncatedAnchors 2 T,
          windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 m) ≤
            2 * (windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 m) +
              windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 (2 * m))) := by
      intro m _
      have h := (h_cs
        (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 m (2, 1)).1
        (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 (2 * m) (2, 1)).1).2.2
      unfold stationAdjustedDiffU
      linarith
    calc
      (∑ m ∈ primeInteriorTruncatedAnchors 2 T,
          windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 m))
        ≤ ∑ m ∈ primeInteriorTruncatedAnchors 2 T,
            2 * (windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 m) +
              windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 (2 * m))) :=
          Finset.sum_le_sum h_each
      _ = 2 * ∑ m ∈ primeInteriorTruncatedAnchors 2 T,
            (windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 m) +
              windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 (2 * m))) :=
          (Finset.mul_sum _ _ _).symm
      _ ≤ 2 * ∑ n ∈ Finset.Icc 1 T,
            windowEnergyNormSq Y (adjustedStationProfilePsi c_lam c_half T D0 n) := by
          apply mul_le_mul_of_nonneg_left _ (by norm_num)
          apply sum_anchor_pair_le_sum_Icc_tc063_aux T
          intro n _
          exact (h_cs
            (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 n (2, 1)).1
            (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 n (2, 1)).1).1
  have h_norm_V :
      ∀ {Y : ℝ}, 2 ≤ Y → ∀ (T : ℕ),
        (∑ m ∈ primeInteriorTruncatedAnchors 2 T,
          ∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => stationFeatureDiffV m pk X)) ≤
          2 * ∑ n ∈ Finset.Icc 1 T,
            (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n ∧
        2 * (∑ n ∈ Finset.Icc 1 T,
            (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n) ≤
          2 * C_g := by
    intro Y hY2 T
    obtain ⟨hle, _⟩ := uIcc_window_props_tc063_aux hY2
    obtain ⟨_, h_cs⟩ := windowPairing_bilinear_and_cauchy_tc063_aux hY2
    have h_self_tc061 :=
      (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2
    have h_log_bd :
        (∑ n ∈ Finset.Icc 1 T,
          (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n) ≤ C_g :=
      (h_self_tc061.2.2.2 hY2 T).2.2
    have h_n_le :
        ∀ {n : ℕ}, 1 ≤ n → n ≤ T →
          (∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => stationPrimePowerFeatureG n pk X)) ≤
            (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n := by
      intro n hn1 hnT
      unfold windowEnergyNormSq
      rw [featureG_sum_windowPairing_eq_tc063_aux hY2 hn1 hnT hn1 hnT]
      have h_off_nn : 0 ≤ offDiagPrimePowerWeight n n := (h_self_tc061.1.2.2.2 n hn1).1
      have h_c_le : commonPrimePowerLogSq n n ≤ (Real.log (n : ℝ)) ^ 2 := by
        unfold offDiagPrimePowerWeight at h_off_nn
        linarith [show Real.log (n : ℝ) * Real.log (n : ℝ) = (Real.log (n : ℝ)) ^ 2 by ring]
      have h_G_nn : 0 ≤ logWeightedWindowKernel 2 Y n n := by
        unfold logWeightedWindowKernel
        apply intervalIntegral.integral_nonneg hle
        intro X hX
        exact div_nonneg (div_nonneg (mul_self_nonneg _) (sq_nonneg _))
          (by rw [Set.mem_Icc] at hX; linarith)
      exact mul_le_mul_of_nonneg_right h_c_le h_G_nn
    have h_each_m :
        ∀ m ∈ primeInteriorTruncatedAnchors 2 T,
          (∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => stationFeatureDiffV m pk X)) ≤
            2 * ((Real.log (m : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y m m +
              (Real.log ((2 * m : ℕ) : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y (2 * m) (2 * m)) := by
      intro m hm
      have hm_bds := hm
      simp only [primeInteriorTruncatedAnchors, primeEvenValuationAnchors,
        Finset.mem_filter, Finset.mem_Icc] at hm_bds
      have hm1 : 1 ≤ m := hm_bds.1.1.1
      have h2mT : 2 * m ≤ T := hm_bds.2
      have hmT : m ≤ T := by omega
      have h2m1 : 1 ≤ 2 * m := by omega
      have h_pk :
          ∀ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => stationFeatureDiffV m pk X) ≤
              2 * windowEnergyNormSq Y (fun X => stationPrimePowerFeatureG m pk X) +
                2 * windowEnergyNormSq Y (fun X => stationPrimePowerFeatureG (2 * m) pk X) := by
        intro pk _
        exact (h_cs
          (continuousOn_psi_and_featureG_tc063_aux hY2 0 0 T 0 m pk).2
          (continuousOn_psi_and_featureG_tc063_aux hY2 0 0 T 0 (2 * m) pk).2).2.2
      calc
        (∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => stationFeatureDiffV m pk X))
          ≤ ∑ pk ∈ primePowerPairsUpTo T,
              (2 * windowEnergyNormSq Y (fun X => stationPrimePowerFeatureG m pk X) +
                2 * windowEnergyNormSq Y (fun X => stationPrimePowerFeatureG (2 * m) pk X)) :=
            Finset.sum_le_sum h_pk
        _ = 2 * (∑ pk ∈ primePowerPairsUpTo T,
              windowEnergyNormSq Y (fun X => stationPrimePowerFeatureG m pk X)) +
            2 * (∑ pk ∈ primePowerPairsUpTo T,
              windowEnergyNormSq Y (fun X => stationPrimePowerFeatureG (2 * m) pk X)) := by
            rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum]
        _ ≤ 2 * ((Real.log (m : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y m m +
              (Real.log ((2 * m : ℕ) : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y (2 * m) (2 * m)) := by
            linarith [h_n_le hm1 hmT, h_n_le h2m1 h2mT]
    refine ⟨?_, mul_le_mul_of_nonneg_left h_log_bd (by norm_num)⟩
    calc
      (∑ m ∈ primeInteriorTruncatedAnchors 2 T,
          ∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => stationFeatureDiffV m pk X))
        ≤ ∑ m ∈ primeInteriorTruncatedAnchors 2 T,
            2 * ((Real.log (m : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y m m +
              (Real.log ((2 * m : ℕ) : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y (2 * m) (2 * m)) :=
          Finset.sum_le_sum h_each_m
      _ = 2 * ∑ m ∈ primeInteriorTruncatedAnchors 2 T,
            ((Real.log (m : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y m m +
              (Real.log ((2 * m : ℕ) : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y (2 * m) (2 * m)) :=
          (Finset.mul_sum _ _ _).symm
      _ ≤ 2 * ∑ n ∈ Finset.Icc 1 T,
            (Real.log (n : ℝ)) ^ 2 * logWeightedWindowKernel 2 Y n n := by
          apply mul_le_mul_of_nonneg_left _ (by norm_num)
          apply sum_anchor_pair_le_sum_Icc_tc063_aux T
          intro n _
          have h_G_nn : 0 ≤ logWeightedWindowKernel 2 Y n n := by
            unfold logWeightedWindowKernel
            apply intervalIntegral.integral_nonneg hle
            intro X hX
            exact div_nonneg (div_nonneg (mul_self_nonneg _) (sq_nonneg _))
              (by rw [Set.mem_Icc] at hX; linarith)
          exact mul_nonneg (sq_nonneg _) h_G_nn
  have h_same_hilbert :
      ∀ (c_lam c_half : ℝ),
        ∃ C_psi : ℝ, 0 ≤ C_psi ∧
          ∀ {Y : ℝ}, 2 ≤ Y →
            (∑ n ∈ Finset.Icc 1 (canonicalCutoffT Y),
              windowEnergyNormSq Y
                (adjustedStationProfilePsi c_lam c_half
                  (canonicalCutoffT Y) (Nat.floor (Real.log Y)) n)) ≤ C_psi ∧
            (∑ m ∈ primeInteriorTruncatedAnchors 2 (canonicalCutoffT Y),
              windowEnergyNormSq Y
                (stationAdjustedDiffU c_lam c_half
                  (canonicalCutoffT Y) (Nat.floor (Real.log Y)) m)) ≤ 2 * C_psi ∧
            |canonicalSameOddChainSumS c_lam c_half Y| ≤
              ((maxDyadicChainLength (canonicalCutoffT Y) : ℝ) - 1) *
                (2 * C_psi + 8 * C_g) ∧
            ((maxDyadicChainLength (canonicalCutoffT Y) : ℝ) - 1) *
                (2 * C_psi + 8 * C_g) ≤
              (2 * C_psi + 8 * C_g) * (1 + Real.log Y) := by
    intro c_lam c_half
    obtain ⟨C_psi, _, hCpsi_nn, _, h_psi_bd, _⟩ :=
      (two_sided_interior_diag_bound_and_offdiag_equivalence_tc062r).2.2.2.1.2.2.2 c_lam c_half
    refine ⟨C_psi, hCpsi_nn, ?_⟩
    intro Y hY2
    let T := canonicalCutoffT Y
    let D0 := Nat.floor (Real.log Y)
    let L := maxDyadicChainLength T
    obtain ⟨hL1, hLm1_log⟩ := maxDyadicChainLength_canonical_bounds_tc063_aux hY2
    have h_psi_Y := h_psi_bd hY2
    have h_U_Y :
        (∑ m ∈ primeInteriorTruncatedAnchors 2 T,
          windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 m)) ≤ 2 * C_psi :=
      le_trans (h_norm_U hY2 c_lam c_half T D0) (mul_le_mul_of_nonneg_left h_psi_Y (by norm_num))
    obtain ⟨h_V_1, h_V_2⟩ := h_norm_V hY2 T
    have h_V_Y :
        (∑ m ∈ primeInteriorTruncatedAnchors 2 T,
          ∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => stationFeatureDiffV m pk X)) ≤ 2 * C_g :=
      le_trans h_V_1 h_V_2
    obtain ⟨_, h_cs⟩ := windowPairing_bilinear_and_cauchy_tc063_aux hY2
    let nsq_m : ℕ → ℝ := fun m =>
      windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 m) +
        4 * ∑ pk ∈ primePowerPairsUpTo T,
          windowEnergyNormSq Y (fun X => stationFeatureDiffV m pk X)
    have h_nsq_nn : ∀ m : ℕ, 0 ≤ nsq_m m := by
      intro m
      dsimp [nsq_m]
      have hU_nn := (h_cs
        ((continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 m (2, 1)).1.sub
          (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 (2 * m) (2, 1)).1)
        ((continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 m (2, 1)).1.sub
          (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 (2 * m) (2, 1)).1)).1
      have hV_nn :
          0 ≤ ∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => stationFeatureDiffV m pk X) := by
        apply Finset.sum_nonneg
        intro pk _
        exact (h_cs
          ((continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 m pk).2.sub
            (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 (2 * m) pk).2)
          ((continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 m pk).2.sub
            (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 (2 * m) pk).2)).1
      change 0 ≤ windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 m) at hU_nn
      linarith
    have h_each_chain :
        ∀ u ∈ oddChainParts T,
          |∑ j ∈ dyadicChainExponents u T,
              ∑ k ∈ (dyadicChainExponents u T).erase j,
                anchorFourTermDiffHcal c_lam c_half T D0 Y (4 ^ j * u) (4 ^ k * u)| ≤
            ((L : ℝ) - 1) * ∑ j ∈ dyadicChainExponents u T, nsq_m (4 ^ j * u) := by
      intro u hu
      have hu_odd : Odd u := (Finset.mem_filter.mp hu).2.1
      have h_card_u : (dyadicChainExponents u T).card ≤ L :=
        Finset.le_sup (f := fun v => (dyadicChainExponents v T).card) hu
      apply finite_hilbert_erase_bound_tc063_aux (dyadicChainExponents u T) hL1 h_card_u
      · intro j _; exact h_nsq_nn (4 ^ j * u)
      · intro j hj k hk
        have hk_in : k ∈ dyadicChainExponents u T := Finset.mem_of_mem_erase hk
        have hk_ne_j : k ≠ j := (Finset.mem_erase.mp hk).1
        have hmj_in : 4 ^ j * u ∈ primeInteriorTruncatedAnchors 2 T :=
          (odd_part_anchor_mem_and_unique_tc063_aux T).1 u hu j hj
        have hmk_in : 4 ^ k * u ∈ primeInteriorTruncatedAnchors 2 T :=
          (odd_part_anchor_mem_and_unique_tc063_aux T).1 u hu k hk_in
        have hmk_ne_mj : 4 ^ k * u ≠ 4 ^ j * u := fun h_eq =>
          hk_ne_j (four_pow_mul_odd_inj_tc063_aux hu_odd hu_odd h_eq).2
        have hmk_er : 4 ^ k * u ∈ (primeInteriorTruncatedAnchors 2 T).erase (4 ^ j * u) :=
          Finset.mem_erase.mpr ⟨hmk_ne_mj, hmk_in⟩
        rw [h_part2b hY2 c_lam c_half T D0 (4 ^ j * u) hmj_in (4 ^ k * u) hmk_er]
        let mj := 4 ^ j * u
        let mk := 4 ^ k * u
        have hU_cs := (h_cs
          ((continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 mj (2, 1)).1.sub
            (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 (2 * mj) (2, 1)).1)
          ((continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 mk (2, 1)).1.sub
            (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 (2 * mk) (2, 1)).1)).2.1
        change 2 * |windowPairing Y
            (stationAdjustedDiffU c_lam c_half T D0 mj)
            (stationAdjustedDiffU c_lam c_half T D0 mk)| ≤
          windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 mj) +
            windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 mk) at hU_cs
        have hV_cs :
            2 * |∑ pk ∈ primePowerPairsUpTo T,
                windowPairing Y (fun X => stationFeatureDiffV mj pk X)
                  (fun X => stationFeatureDiffV mk pk X)| ≤
              (∑ pk ∈ primePowerPairsUpTo T,
                  windowEnergyNormSq Y (fun X => stationFeatureDiffV mj pk X)) +
                (∑ pk ∈ primePowerPairsUpTo T,
                  windowEnergyNormSq Y (fun X => stationFeatureDiffV mk pk X)) := by
          calc
            2 * |∑ pk ∈ primePowerPairsUpTo T,
                windowPairing Y (fun X => stationFeatureDiffV mj pk X)
                  (fun X => stationFeatureDiffV mk pk X)|
              ≤ 2 * ∑ pk ∈ primePowerPairsUpTo T,
                  |windowPairing Y (fun X => stationFeatureDiffV mj pk X)
                    (fun X => stationFeatureDiffV mk pk X)| :=
                mul_le_mul_of_nonneg_left (Finset.abs_sum_le_sum_abs _ _) (by norm_num)
            _ = ∑ pk ∈ primePowerPairsUpTo T,
                  2 * |windowPairing Y (fun X => stationFeatureDiffV mj pk X)
                    (fun X => stationFeatureDiffV mk pk X)| := Finset.mul_sum _ _ _
            _ ≤ ∑ pk ∈ primePowerPairsUpTo T,
                  (windowEnergyNormSq Y (fun X => stationFeatureDiffV mj pk X) +
                    windowEnergyNormSq Y (fun X => stationFeatureDiffV mk pk X)) := by
                apply Finset.sum_le_sum
                intro pk _
                exact (h_cs
                  ((continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 mj pk).2.sub
                    (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 (2 * mj) pk).2)
                  ((continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 mk pk).2.sub
                    (continuousOn_psi_and_featureG_tc063_aux hY2 c_lam c_half T D0 (2 * mk) pk).2)).2.1
            _ = (∑ pk ∈ primePowerPairsUpTo T,
                  windowEnergyNormSq Y (fun X => stationFeatureDiffV mj pk X)) +
                (∑ pk ∈ primePowerPairsUpTo T,
                  windowEnergyNormSq Y (fun X => stationFeatureDiffV mk pk X)) :=
                Finset.sum_add_distrib
        have h_tri := abs_sub
          (windowPairing Y (stationAdjustedDiffU c_lam c_half T D0 mj)
            (stationAdjustedDiffU c_lam c_half T D0 mk))
          (4 * ∑ pk ∈ primePowerPairsUpTo T,
            windowPairing Y (fun X => stationFeatureDiffV mj pk X)
              (fun X => stationFeatureDiffV mk pk X))
        rw [abs_mul, show |(4 : ℝ)| = 4 by norm_num] at h_tri
        dsimp only [nsq_m, mj, mk] at hU_cs hV_cs h_tri ⊢
        linarith
    have h_Ssame_bd :
        |canonicalSameOddChainSumS c_lam c_half Y| ≤
          ((L : ℝ) - 1) * (2 * C_psi + 8 * C_g) := by
      unfold canonicalSameOddChainSumS sameOddChainSumS
      have h_Lm1_nn : 0 ≤ (L : ℝ) - 1 := by
        have h1 : (1 : ℝ) ≤ (L : ℝ) := by exact_mod_cast hL1
        linarith
      calc
        |∑ u ∈ oddChainParts T,
            ∑ j ∈ dyadicChainExponents u T,
              ∑ k ∈ (dyadicChainExponents u T).erase j,
                anchorFourTermDiffHcal c_lam c_half T D0 Y (4 ^ j * u) (4 ^ k * u)|
          ≤ ∑ u ∈ oddChainParts T,
              |∑ j ∈ dyadicChainExponents u T,
                ∑ k ∈ (dyadicChainExponents u T).erase j,
                  anchorFourTermDiffHcal c_lam c_half T D0 Y (4 ^ j * u) (4 ^ k * u)| :=
            Finset.abs_sum_le_sum_abs _ _
        _ ≤ ∑ u ∈ oddChainParts T,
              ((L : ℝ) - 1) * ∑ j ∈ dyadicChainExponents u T, nsq_m (4 ^ j * u) :=
            Finset.sum_le_sum h_each_chain
        _ = ((L : ℝ) - 1) *
              ∑ u ∈ oddChainParts T, ∑ j ∈ dyadicChainExponents u T, nsq_m (4 ^ j * u) :=
            (Finset.mul_sum _ _ _).symm
        _ = ((L : ℝ) - 1) * ∑ m ∈ primeInteriorTruncatedAnchors 2 T, nsq_m m := by
            rw [← sum_anchors_eq_odd_chains_tc063_aux T nsq_m]
        _ ≤ ((L : ℝ) - 1) * (2 * C_psi + 8 * C_g) := by
            apply mul_le_mul_of_nonneg_left _ h_Lm1_nn
            dsimp [nsq_m]
            rw [Finset.sum_add_distrib, ← Finset.mul_sum]
            linarith [h_U_Y, h_V_Y]
    have h_log_step :
        ((L : ℝ) - 1) * (2 * C_psi + 8 * C_g) ≤ (2 * C_psi + 8 * C_g) * (1 + Real.log Y) := by
      have h_const_nn : 0 ≤ 2 * C_psi + 8 * C_g := by positivity
      linarith [mul_le_mul_of_nonneg_right hLm1_log h_const_nn]
    exact ⟨h_psi_Y, h_U_Y, h_Ssame_bd, h_log_step⟩
  have h_closure_iff :
      ∀ (c_lam c_half : ℝ),
        MixedCovarianceClosureHypothesis
            (canonicalInteriorOffDiagSigma c_lam c_half 2) canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalDifferentOddChainSumS c_lam c_half) canonicalPrimePowerDiagDtilde := by
    intro c_lam c_half
    obtain ⟨C_psi, hCpsi_nn, h_bd⟩ := h_same_hilbert c_lam c_half
    let C_same : ℝ := 2 * C_psi + 8 * C_g
    have hCsame_nn : 0 ≤ C_same := by dsimp [C_same]; positivity
    have h_split :
        ∀ Y : ℝ,
          canonicalInteriorOffDiagSigma c_lam c_half 2 Y =
            canonicalSameOddChainSumS c_lam c_half Y +
              canonicalDifferentOddChainSumS c_lam c_half Y :=
      fun Y => (exact_odd_part_bijection_and_dyadic_chain_offdiag_split_tc063).2.2.2.1
        c_lam c_half (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y
    have h_abs_same :
        ∀ {Y : ℝ}, 2 ≤ Y → |canonicalSameOddChainSumS c_lam c_half Y| ≤ C_same * (1 + Real.log Y) :=
      fun hY2 => le_trans (h_bd hY2).2.2.1 (h_bd hY2).2.2.2
    have h_trans :
        ∀ {F1 F2 : ℝ → ℝ},
          (∀ {Y : ℝ}, 2 ≤ Y → F2 Y ≤ F1 Y + C_same * (1 + Real.log Y)) →
          MixedCovarianceClosureHypothesis F1 canonicalPrimePowerDiagDtilde →
          MixedCovarianceClosureHypothesis F2 canonicalPrimePowerDiagDtilde := by
      intro F1 F2 h_diff hF1 η hη
      obtain ⟨a_eta, b_eta, κ_eta, Y_eta, ha, hb, hκ_pos, hκ_le2, hYe, hF1_bd⟩ := hF1 η hη
      obtain ⟨a_same, ha_same, h_same_rpow⟩ := log_linear_le_rpow_tc063_aux hCsame_nn hη
      refine ⟨a_eta + a_same, b_eta, κ_eta, Y_eta,
        add_nonneg ha ha_same, hb, hκ_pos, hκ_le2, hYe, ?_⟩
      intro Y hYYe
      have hY2 : 2 ≤ Y := le_trans hYe hYYe
      have h1 := h_diff hY2
      have h2 := hF1_bd Y hYYe
      have h3 := h_same_rpow Y hY2
      linarith [show (a_eta + a_same) * Y ^ η = a_eta * Y ^ η + a_same * Y ^ η by ring]
    constructor
    · apply h_trans
      intro Y hY2
      have habs := (abs_le.mp (h_abs_same hY2)).1
      linarith [h_split Y]
    · apply h_trans
      intro Y hY2
      have habs := (abs_le.mp (h_abs_same hY2)).2
      linarith [h_split Y]
  have h_tc062r_2 :=
    (two_sided_interior_diag_bound_and_offdiag_equivalence_tc062r).2.2.2.2 Nat.prime_two
  have h_act_iff := h_closure_iff actualSelbergConstantCLam actualSquarePoleConstantCHalf
  refine ⟨distinct_anchors_disjoint_shifts_tc063_aux,
    ⟨fun {_} hY2 {_ _ _} hm1 hmT hn1 hnT =>
        featureG_sum_windowPairing_eq_tc063_aux hY2 hm1 hmT hn1 hnT,
      h_part2b⟩,
    ⟨h_norm_U, h_norm_V⟩,
    ⟨fun J {_} hL1 hJc ip nsq h_nn h_cs =>
        finite_hilbert_erase_bound_tc063_aux J hL1 hJc ip nsq h_nn h_cs,
      fun {_} hY2 => maxDyadicChainLength_canonical_bounds_tc063_aux hY2,
      h_same_hilbert⟩,
    ⟨fun {_} hC {_} heta => log_linear_le_rpow_tc063_aux hC heta,
      h_closure_iff,
      ⟨h_act_iff, h_tc062r_2.1.2.1.trans h_act_iff⟩,
      ?_⟩⟩
  intro M_lin hM_nn hE_lin h_diff_hyp h_route_d_inputs
  exact h_tc062r_2.2 hM_nn hE_lin (h_act_iff.mpr h_diff_hyp) h_route_d_inputs

/-! ### Section 4: Odd Common-Factor Regrouping & Feature Decoupling (`TASK-TC-063` §5) -/

private theorem odd_of_odd_mul_tc063_aux {a b : ℕ} (h : Odd (a * b)) : Odd a ∧ Odd b := by
  constructor
  · rcases Nat.even_or_odd a with ha_ev | ha_odd
    · obtain ⟨k, rfl⟩ := even_iff_two_dvd.mp ha_ev
      exact False.elim ((Nat.odd_iff_not_even.mp h) (even_iff_two_dvd.mpr ⟨k * b, by ring⟩))
    · exact ha_odd
  · rcases Nat.even_or_odd b with hb_ev | hb_odd
    · obtain ⟨k, rfl⟩ := even_iff_two_dvd.mp hb_ev
      exact False.elim ((Nat.odd_iff_not_even.mp h) (even_iff_two_dvd.mpr ⟨a * k, by ring⟩))
    · exact hb_odd

private theorem liouvilleLambda_common_factor_cancel_tc063_aux {g r t : ℕ}
    (hg : 1 ≤ g) (hr : 1 ≤ r) (ht : 1 ≤ t) :
    liouvilleLambda (g * r) * liouvilleLambda (g * t) = liouvilleLambda r * liouvilleLambda t := by
  have hg_ne : g ≠ 0 := by omega
  have hr_ne : r ≠ 0 := by omega
  have ht_ne : t ≠ 0 := by omega
  have h_mul : ∀ x y : ℕ, x ≠ 0 → y ≠ 0 → liouvilleLambda (x * y) = liouvilleLambda x * liouvilleLambda y := by
    intro x y hx hy
    have hxy : x * y ≠ 0 := mul_ne_zero hx hy
    simp [liouvilleLambda, hx, hy, hxy, natOmega,
      ArithmeticFunction.cardFactors_mul hx hy, liouvilleSignFromOmega, pow_add]
  have h_sq : liouvilleLambda g * liouvilleLambda g = 1 := by
    simp only [liouvilleLambda, hg_ne, ↓reduceIte, liouvilleSignFromOmega]
    rw [← pow_add, show natOmega g + natOmega g = 2 * natOmega g by omega, pow_mul]
    norm_num
  calc
    liouvilleLambda (g * r) * liouvilleLambda (g * t)
      = (liouvilleLambda g * liouvilleLambda g) * (liouvilleLambda r * liouvilleLambda t) := by
        rw [h_mul g r hg_ne hr_ne, h_mul g t hg_ne ht_ne]; ring
    _ = liouvilleLambda r * liouvilleLambda t := by rw [h_sq, one_mul]

private theorem odd_primitive_pair_bijection_tc063_aux (T : ℕ) :
    (∀ g ∈ oddCommonFactorGcdSet T,
      ∀ rt ∈ primitiveOddChainPairs T g,
        g * rt.1 ∈ oddChainParts T ∧ g * rt.2 ∈ oddChainParts T ∧
          g * rt.1 ≠ g * rt.2 ∧ Nat.gcd (g * rt.1) (g * rt.2) = g ∧
          (g * rt.1) / g = rt.1 ∧ (g * rt.2) / g = rt.2) ∧
    (∀ uv ∈ (oddChainParts T ×ˢ oddChainParts T).filter (fun uv => uv.1 ≠ uv.2),
      Nat.gcd uv.1 uv.2 ∈ oddCommonFactorGcdSet T ∧
        (uv.1 / Nat.gcd uv.1 uv.2, uv.2 / Nat.gcd uv.1 uv.2) ∈
          primitiveOddChainPairs T (Nat.gcd uv.1 uv.2) ∧
        ∃! grt : ℕ × (ℕ × ℕ),
          grt.1 ∈ oddCommonFactorGcdSet T ∧
            grt.2 ∈ primitiveOddChainPairs T grt.1 ∧
            grt.1 * grt.2.1 = uv.1 ∧ grt.1 * grt.2.2 = uv.2) := by
  have h_fwd :
      ∀ g ∈ oddCommonFactorGcdSet T,
        ∀ rt ∈ primitiveOddChainPairs T g,
          g * rt.1 ∈ oddChainParts T ∧ g * rt.2 ∈ oddChainParts T ∧
            g * rt.1 ≠ g * rt.2 ∧ Nat.gcd (g * rt.1) (g * rt.2) = g ∧
            (g * rt.1) / g = rt.1 ∧ (g * rt.2) / g = rt.2 := by
    intro g hg ⟨r, t⟩ hrt
    simp only [oddCommonFactorGcdSet, primitiveOddChainPairs, oddChainParts,
      Finset.mem_filter, Finset.mem_product, Finset.mem_Icc] at hg hrt ⊢
    rcases hg with ⟨⟨hg1, _⟩, hg_odd, _⟩
    rcases hrt with ⟨⟨⟨⟨hr1, _⟩, hr_odd, h2r_div⟩, ⟨⟨ht1, _⟩, ht_odd, h2t_div⟩⟩, hrt_ne, hrt_cop⟩
    have h2gr_le : 2 * (g * r) ≤ T := by
      have hm := (Nat.le_div_iff_mul_le hg1).mp h2r_div
      linarith [show 2 * (g * r) = 2 * r * g by ring]
    have h2gt_le : 2 * (g * t) ≤ T := by
      have hm := (Nat.le_div_iff_mul_le hg1).mp h2t_div
      linarith [show 2 * (g * t) = 2 * t * g by ring]
    have hgr1 : 1 ≤ g * r := Nat.mul_pos hg1 hr1
    have hgt1 : 1 ≤ g * t := Nat.mul_pos hg1 ht1
    refine ⟨⟨⟨hgr1, by omega⟩, hg_odd.mul hr_odd, h2gr_le⟩,
      ⟨⟨hgt1, by omega⟩, hg_odd.mul ht_odd, h2gt_le⟩,
      fun h_eq => hrt_ne (Nat.eq_of_mul_eq_mul_left hg1 h_eq),
      by rw [Nat.gcd_mul_left, hrt_cop.gcd_eq_one, mul_one],
      Nat.mul_div_right r hg1,
      Nat.mul_div_right t hg1⟩
  refine ⟨h_fwd, ?_⟩
  rintro ⟨u, v⟩ huv
  simp only [Finset.mem_filter, Finset.mem_product, oddChainParts, Finset.mem_Icc] at huv
  rcases huv with ⟨⟨⟨⟨hu1, _⟩, hu_odd, h2u_T⟩, ⟨⟨_, _⟩, hv_odd, h2v_T⟩⟩, huv_ne⟩
  let g := Nat.gcd u v
  let r := u / g
  let t := v / g
  have hg_pos : 0 < g := Nat.gcd_pos_of_pos_left v hu1
  have hgr : g * r = u := Nat.mul_div_cancel' (Nat.gcd_dvd_left u v)
  have hgt : g * t = v := Nat.mul_div_cancel' (Nat.gcd_dvd_right u v)
  have hgr_odd : Odd g ∧ Odd r := odd_of_odd_mul_tc063_aux (by rwa [hgr])
  have hgt_odd : Odd g ∧ Odd t := odd_of_odd_mul_tc063_aux (by rwa [hgt])
  have hg_odd : Odd g := hgr_odd.1
  have hr_odd : Odd r := hgr_odd.2
  have ht_odd : Odd t := hgt_odd.2
  have hr1 : 1 ≤ r := hr_odd.pos
  have ht1 : 1 ≤ t := ht_odd.pos
  have hrt_ne : r ≠ t := fun h_eq => huv_ne (by rw [← hgr, ← hgt, h_eq])
  have hrt_cop : Nat.Coprime r t := Nat.coprime_div_gcd_div_gcd hg_pos
  have h6g_le : 6 * g ≤ T := by
    have h_max3 : 3 ≤ r ∨ 3 ≤ t := by
      by_contra h_not
      push_neg at h_not
      obtain ⟨kr, hkr⟩ := hr_odd
      obtain ⟨kt, hkt⟩ := ht_odd
      omega
    rcases h_max3 with hr3 | ht3
    · have h1 : 2 * (g * 3) ≤ 2 * (g * r) :=
        Nat.mul_le_mul_left 2 (Nat.mul_le_mul_left g hr3)
      rw [hgr] at h1
      omega
    · have h1 : 2 * (g * 3) ≤ 2 * (g * t) :=
        Nat.mul_le_mul_left 2 (Nat.mul_le_mul_left g ht3)
      rw [hgt] at h1
      omega
  have hg_in : g ∈ oddCommonFactorGcdSet T := by
    simp only [oddCommonFactorGcdSet, Finset.mem_filter, Finset.mem_Icc]
    exact ⟨⟨hg_pos, by omega⟩, hg_odd, h6g_le⟩
  have h2r_div : 2 * r ≤ T / g :=
    (Nat.le_div_iff_mul_le hg_pos).mpr (by linarith [show 2 * r * g = 2 * (g * r) by ring])
  have h2t_div : 2 * t ≤ T / g :=
    (Nat.le_div_iff_mul_le hg_pos).mpr (by linarith [show 2 * t * g = 2 * (g * t) by ring])
  have hrt_in : (r, t) ∈ primitiveOddChainPairs T g := by
    simp only [primitiveOddChainPairs, oddChainParts, Finset.mem_filter,
      Finset.mem_product, Finset.mem_Icc]
    exact ⟨⟨⟨⟨hr1, by omega⟩, hr_odd, h2r_div⟩, ⟨⟨ht1, by omega⟩, ht_odd, h2t_div⟩⟩,
      hrt_ne, hrt_cop⟩
  refine ⟨hg_in, hrt_in, ⟨(g, (r, t)), ⟨hg_in, hrt_in, hgr, hgt⟩, ?_⟩⟩
  rintro ⟨g', ⟨r', t'⟩⟩ ⟨hg'_in, hrt'_in, hgr', hgt'⟩
  dsimp only at hg'_in hrt'_in hgr' hgt'
  have h_fwd' := h_fwd g' hg'_in (r', t') hrt'_in
  dsimp only at h_fwd'
  have hg'_eq : g' = g := by
    change g' = Nat.gcd u v
    rw [← hgr', ← hgt', h_fwd'.2.2.2.1]
  have hr'_eq : r' = r := by
    change r' = u / g
    rw [← hg'_eq, ← hgr', h_fwd'.2.2.2.2.1]
  have ht'_eq : t' = t := by
    change t' = v / g
    rw [← hg'_eq, ← hgt', h_fwd'.2.2.2.2.2]
  rw [hg'_eq, hr'_eq, ht'_eq]

private theorem gcd_and_commonPrimePowerLogSq_dyadic_odd_coprime_tc063_aux
    {g r t : ℕ} (a b : ℕ) (hg1 : 1 ≤ g) (hr1 : 1 ≤ r) (ht1 : 1 ≤ t)
    (_hg_odd : Odd g) (hr_odd : Odd r) (ht_odd : Odd t) (hrt_cop : Nat.Coprime r t) :
    Nat.gcd (2 ^ a * (g * r)) (2 ^ b * (g * t)) = 2 ^ (min a b) * g ∧
      commonPrimePowerLogSq (2 ^ a * (g * r)) (2 ^ b * (g * t)) =
        commonPrimePowerLogSq g g + ((min a b : ℕ) : ℝ) * (Real.log 2) ^ 2 := by
  have h_gcd_le :
      ∀ {x y u v : ℕ}, x ≤ y → Odd u → Nat.Coprime u v →
        Nat.gcd (2 ^ x * (g * u)) (2 ^ y * (g * v)) = 2 ^ x * g := by
    intro x y u v hxy hu_odd huv_cop
    have hy_split : 2 ^ y = 2 ^ x * 2 ^ (y - x) := by
      rw [← pow_add, Nat.add_sub_of_le hxy]
    have h1 : 2 ^ x * (g * u) = (2 ^ x * g) * u := by ring
    have h2 : 2 ^ y * (g * v) = (2 ^ x * g) * (2 ^ (y - x) * v) := by
      rw [hy_split]; ring
    rw [h1, h2, Nat.gcd_mul_left]
    have hu_cop2 : Nat.Coprime u 2 := by
      apply Nat.Coprime.symm
      rw [Nat.Prime.coprime_iff_not_dvd Nat.prime_two]
      exact fun h2 => (Nat.odd_iff_not_even.mp hu_odd) (even_iff_two_dvd.mpr h2)
    have hu_cop_rhs : Nat.Coprime u (2 ^ (y - x) * v) :=
      (hu_cop2.pow_right (y - x)).mul_right huv_cop
    rw [hu_cop_rhs.gcd_eq_one, mul_one]
  have h_gcd : Nat.gcd (2 ^ a * (g * r)) (2 ^ b * (g * t)) = 2 ^ (min a b) * g := by
    rcases le_total a b with hab | hba
    · rw [min_eq_left hab]
      exact h_gcd_le hab hr_odd hrt_cop
    · rw [min_eq_right hba, Nat.gcd_comm]
      exact h_gcd_le hba ht_odd hrt_cop.symm
  refine ⟨h_gcd, ?_⟩
  let M := 2 ^ a * (g * r)
  let N := 2 ^ b * (g * t)
  have hM1 : 1 ≤ M := Nat.mul_pos (Nat.one_le_pow a 2 (by decide)) (Nat.mul_pos hg1 hr1)
  have hN1 : 1 ≤ N := Nat.mul_pos (Nat.one_le_pow b 2 (by decide)) (Nat.mul_pos hg1 ht1)
  let d := Nat.gcd M N
  have hd1 : 1 ≤ d := Nat.gcd_pos_of_pos_left N hM1
  have hd_le_min : d ≤ min M N :=
    le_min (Nat.le_of_dvd hM1 (Nat.gcd_dvd_left M N))
      (Nat.le_of_dvd hN1 (Nat.gcd_dvd_right M N))
  have h_c_eq_d : commonPrimePowerLogSq M N = commonPrimePowerLogSq d d := by
    unfold commonPrimePowerLogSq
    have hf := primePowerPairsUpTo_gcd_filter_eq_tc063_aux hd1 hd_le_min hd1 hd_le_min
    rw [Nat.gcd_self, min_self] at hf
    have hd_def : Nat.gcd M N = d := rfl
    rw [hd_def, Nat.gcd_self, min_self, hf]
  have hd_val : d = 2 ^ (min a b) * g := h_gcd
  rw [h_c_eq_d, hd_val]
  have h_ind :
      ∀ c : ℕ,
        commonPrimePowerLogSq (2 ^ c * g) (2 ^ c * g) =
          commonPrimePowerLogSq g g + (c : ℝ) * (Real.log 2) ^ 2 := by
    intro c
    induction c with
    | zero => simp
    | succ c ih =>
      have hc_pos : 1 ≤ 2 ^ c * g := Nat.mul_pos (Nat.one_le_pow c 2 (by decide)) hg1
      have h_step :=
        (((two_sided_interior_diag_bound_and_offdiag_equivalence_tc062r).2.1 Nat.prime_two).1
          hc_pos).2
      have h_pow : 2 ^ (c + 1) * g = 2 * (2 ^ c * g) := by ring
      rw [h_pow, h_step, ih]
      push_cast
      ring
  exact h_ind (min a b)

/-- **Theorem 4 (`TASK-TC-063` §5, Odd Common-Factor Primitive-Pair Regrouping, Exact Chain-Length Preservation, and Prime-Power Feature Decoupling)**:
    1. *Unique odd-`gcd` primitive decomposition, exact chain-exponent set equality `J_{g*r}(T) = J_r(⌊T/g⌋)`, and Liouville common-factor sign cancellation*;
    2. *Exact complete-kernel primitive-sector decomposition*:
       `differentOddChainSumS c_lam c_half T D0 Y = ∑ g ∈ oddCommonFactorGcdSet T, primitiveOddChainSectorPi c_lam c_half T D0 Y g`;
    3. *Exact coprime odd prime-power feature decoupling*:
       For odd `g, r, t ≥ 1` with `Nat.Coprime r t` and `a, b : ℕ`:
       `Nat.gcd (2^a * (g * r)) (2^b * (g * t)) = 2^(min a b) * g` and
       `commonPrimePowerLogSq (2^a * (g * r)) (2^b * (g * t)) = commonPrimePowerLogSq g g + (min a b : ℝ) * (Real.log 2)^2`. -/
theorem odd_common_factor_primitive_regrouping_and_feature_decoupling_tc063 :
    ((∀ (T : ℕ),
        (∀ g ∈ oddCommonFactorGcdSet T,
          ∀ rt ∈ primitiveOddChainPairs T g,
            g * rt.1 ∈ oddChainParts T ∧ g * rt.2 ∈ oddChainParts T ∧
              g * rt.1 ≠ g * rt.2 ∧ Nat.gcd (g * rt.1) (g * rt.2) = g ∧
              (g * rt.1) / g = rt.1 ∧ (g * rt.2) / g = rt.2) ∧
        (∀ uv ∈ (oddChainParts T ×ˢ oddChainParts T).filter (fun uv => uv.1 ≠ uv.2),
          Nat.gcd uv.1 uv.2 ∈ oddCommonFactorGcdSet T ∧
            (uv.1 / Nat.gcd uv.1 uv.2, uv.2 / Nat.gcd uv.1 uv.2) ∈
              primitiveOddChainPairs T (Nat.gcd uv.1 uv.2) ∧
            ∃! grt : ℕ × (ℕ × ℕ),
              grt.1 ∈ oddCommonFactorGcdSet T ∧
                grt.2 ∈ primitiveOddChainPairs T grt.1 ∧
                grt.1 * grt.2.1 = uv.1 ∧ grt.1 * grt.2.2 = uv.2)) ∧
      (∀ (g r T : ℕ), 1 ≤ g → 1 ≤ r →
        dyadicChainExponents (g * r) T = dyadicChainExponents r (T / g)) ∧
      (∀ (g r t : ℕ), 1 ≤ g → 1 ≤ r → 1 ≤ t →
        liouvilleLambda (g * r) * liouvilleLambda (g * t) =
          liouvilleLambda r * liouvilleLambda t)) ∧
    (∀ (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ),
      differentOddChainSumS c_lam c_half T D0 Y =
        ∑ g ∈ oddCommonFactorGcdSet T, primitiveOddChainSectorPi c_lam c_half T D0 Y g) ∧
    (∀ {g r t : ℕ} (a b : ℕ),
      1 ≤ g → 1 ≤ r → 1 ≤ t → Odd g → Odd r → Odd t → Nat.Coprime r t →
        Nat.gcd (2 ^ a * (g * r)) (2 ^ b * (g * t)) = 2 ^ (min a b) * g ∧
          commonPrimePowerLogSq (2 ^ a * (g * r)) (2 ^ b * (g * t)) =
            commonPrimePowerLogSq g g + ((min a b : ℕ) : ℝ) * (Real.log 2) ^ 2) := by
  have h_chain_eq :
      ∀ (g r T : ℕ), 1 ≤ g → 1 ≤ r →
        dyadicChainExponents (g * r) T = dyadicChainExponents r (T / g) := by
    intro g r T hg hr
    have hgr : 1 ≤ g * r := Nat.mul_pos hg hr
    ext j
    rw [mem_dyadicChainExponents_iff_tc063_aux hgr j T,
      mem_dyadicChainExponents_iff_tc063_aux hr j (T / g),
      Nat.le_div_iff_mul_le hg,
      show 2 * 4 ^ j * (g * r) = 2 * 4 ^ j * r * g by ring]
  have h_regroup :
      ∀ (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ),
        differentOddChainSumS c_lam c_half T D0 Y =
          ∑ g ∈ oddCommonFactorGcdSet T, primitiveOddChainSectorPi c_lam c_half T D0 Y g := by
    intro c_lam c_half T D0 Y
    obtain ⟨h_fwd, h_inv⟩ := odd_primitive_pair_bijection_tc063_aux T
    let D_odd := (oddChainParts T ×ˢ oddChainParts T).filter (fun uv => uv.1 ≠ uv.2)
    have h_lhs :
        differentOddChainSumS c_lam c_half T D0 Y =
          ∑ uv ∈ D_odd,
            (liouvilleLambda uv.1 : ℝ) * (liouvilleLambda uv.2 : ℝ) *
              oddChainGroupedKernel c_lam c_half T D0 Y uv.1 uv.2 := by
      unfold differentOddChainSumS
      dsimp [D_odd]
      rw [Finset.sum_filter, Finset.sum_product]
      apply Finset.sum_congr rfl
      intro u hu
      symm
      rw [← Finset.add_sum_erase _ _ hu, if_neg (not_not.mpr rfl), zero_add]
      apply Finset.sum_congr rfl
      intro v hv
      rw [if_pos (Finset.mem_erase.mp hv).1.symm]
    rw [h_lhs]
    unfold primitiveOddChainSectorPi
    rw [← Finset.sum_sigma (oddCommonFactorGcdSet T) (primitiveOddChainPairs T)
      (fun grt =>
        (liouvilleLambda grt.2.1 : ℝ) * (liouvilleLambda grt.2.2 : ℝ) *
          oddChainGroupedKernel c_lam c_half T D0 Y (grt.1 * grt.2.1) (grt.1 * grt.2.2))]
    symm
    apply Finset.sum_bij (fun grt _ => (grt.1 * grt.2.1, grt.1 * grt.2.2))
    · rintro ⟨g, ⟨r, t⟩⟩ hmem
      rw [Finset.mem_sigma] at hmem
      obtain ⟨hu_in, hv_in, huv_ne, _, _, _⟩ := h_fwd g hmem.1 (r, t) hmem.2
      exact Finset.mem_filter.mpr ⟨Finset.mem_product.mpr ⟨hu_in, hv_in⟩, huv_ne⟩
    · rintro ⟨g1, ⟨r1, t1⟩⟩ h1 ⟨g2, ⟨r2, t2⟩⟩ h2 h_eq
      rw [Finset.mem_sigma] at h1 h2
      rw [Prod.mk.injEq] at h_eq
      have hf1 := h_fwd g1 h1.1 (r1, t1) h1.2
      have hf2 := h_fwd g2 h2.1 (r2, t2) h2.2
      dsimp only at h1 h2 h_eq hf1 hf2
      have hg_eq : g1 = g2 := by
        rw [← hf1.2.2.2.1, h_eq.1, h_eq.2, hf2.2.2.2.1]
      subst hg_eq
      have hr_eq : r1 = r2 := by rw [← hf1.2.2.2.2.1, h_eq.1, hf2.2.2.2.2.1]
      have ht_eq : t1 = t2 := by rw [← hf1.2.2.2.2.2, h_eq.2, hf2.2.2.2.2.2]
      subst hr_eq; subst ht_eq; rfl
    · rintro ⟨u, v⟩ huv
      obtain ⟨hg_in, hrt_in, _⟩ := h_inv (u, v) huv
      refine ⟨⟨Nat.gcd u v, (u / Nat.gcd u v, v / Nat.gcd u v)⟩,
        Finset.mem_sigma.mpr ⟨hg_in, hrt_in⟩, ?_⟩
      dsimp only
      rw [Nat.mul_div_cancel' (Nat.gcd_dvd_left u v),
        Nat.mul_div_cancel' (Nat.gcd_dvd_right u v)]
    · rintro ⟨g, ⟨r, t⟩⟩ hmem
      rw [Finset.mem_sigma] at hmem
      have hg1 : 1 ≤ g := (Finset.mem_Icc.mp (Finset.mem_filter.mp hmem.1).1).1
      have hr1 : 1 ≤ r :=
        (Finset.mem_Icc.mp (Finset.mem_filter.mp (Finset.mem_product.mp (Finset.mem_filter.mp hmem.2).1).1).1).1
      have ht1 : 1 ≤ t :=
        (Finset.mem_Icc.mp (Finset.mem_filter.mp (Finset.mem_product.mp (Finset.mem_filter.mp hmem.2).1).2).1).1
      have h_canc :
          (liouvilleLambda (g * r) : ℝ) * (liouvilleLambda (g * t) : ℝ) =
            (liouvilleLambda r : ℝ) * (liouvilleLambda t : ℝ) := by
        have h_int := liouvilleLambda_common_factor_cancel_tc063_aux hg1 hr1 ht1
        exact_mod_cast h_int
      dsimp only
      rw [h_canc]
  exact ⟨⟨odd_primitive_pair_bijection_tc063_aux,
      h_chain_eq,
      fun g r t hg hr ht => liouvilleLambda_common_factor_cancel_tc063_aux hg hr ht⟩,
    h_regroup,
    fun a b hg1 hr1 ht1 hgo hro hto hcop =>
      gcd_and_commonPrimePowerLogSq_dyadic_odd_coprime_tc063_aux a b hg1 hr1 ht1 hgo hro hto hcop⟩

/-! ### Section 5: Odd-Square Projection, Selberg Split, & Sign-Extension Obstruction (`TASK-TC-063` §6) -/

private theorem odd_divisor_liouville_quotient_sum_tc063_aux {n : ℕ}
    (_hn_odd : Odd n) (hn1 : 1 ≤ n) :
    (∑ d ∈ n.divisors, (liouvilleLambda (n / d) : ℝ)) = if IsSquare n then 1 else 0 := by
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
        Nat.div_pos (Nat.le_of_dvd hn1 hd1.1) (Nat.pos_of_dvd_of_pos hd1.1 hn1)
      rw [← h_eq] at h2
      exact Nat.eq_of_mul_eq_mul_right hq_pos (h1.trans h2.symm)
    · intro q hq
      rw [Nat.mem_divisors] at hq
      have hq_pos : 0 < q := Nat.pos_of_dvd_of_pos hq.1 hn1
      let d := n / q
      have hd_pos : 0 < d := Nat.div_pos (Nat.le_of_dvd hn1 hq.1) hq_pos
      have hqd : q * d = n := Nat.mul_div_cancel' hq.1
      refine ⟨d, Nat.mem_divisors.mpr ⟨Nat.div_dvd_of_dvd hq.1, hq.2⟩, ?_⟩
      change n / d = q
      rw [← hqd]
      exact Nat.mul_div_left q hd_pos
    · intros; rfl
  rw [h_bij]
  have h_ind := (liouville_square_divisor_indicator_and_compensated_selberg_tc058 1 0).1 n hn1
  have h_cast :
      (∑ q ∈ n.divisors, (liouvilleLambda q : ℝ)) =
        ((∑ q ∈ n.divisors, liouvilleLambda q : ℤ) : ℝ) := by
    push_cast; rfl
  rw [h_cast, h_ind]
  split_ifs <;> norm_num

private theorem odd_square_projection_and_moebius_recovery_tc063_aux
    (c_lam c_half : ℝ) (T D0 : ℕ) (X : ℝ) :
    (∑ d ∈ oddChainParts T, dilatedOddChainSumGcal c_lam c_half T D0 d X) =
        ∑ w ∈ (oddChainParts T).filter IsSquare,
          oddChainAdjustedProfileUcal c_lam c_half T D0 w X ∧
      (∑ e ∈ oddChainParts T,
        (ArithmeticFunction.moebius e : ℝ) *
          ∑ w ∈ (oddChainParts (T / e)).filter IsSquare,
            oddChainAdjustedProfileUcal c_lam c_half T D0 (e * w) X) =
        dilatedOddChainSumGcal c_lam c_half T D0 1 X := by
  let Ucal := oddChainAdjustedProfileUcal c_lam c_half T D0
  constructor
  · unfold dilatedOddChainSumGcal
    change (∑ d ∈ oddChainParts T, ∑ u ∈ oddChainParts (T / d),
        (liouvilleLambda u : ℝ) * Ucal (d * u) X) =
      ∑ w ∈ (oddChainParts T).filter IsSquare, Ucal w X
    rw [← Finset.sum_sigma (oddChainParts T) (fun d => oddChainParts (T / d))
      (fun du => (liouvilleLambda du.2 : ℝ) * Ucal (du.1 * du.2) X)]
    have h_reindex :
        (∑ du ∈ (oddChainParts T).sigma (fun d => oddChainParts (T / d)),
            (liouvilleLambda du.2 : ℝ) * Ucal (du.1 * du.2) X) =
          ∑ wd ∈ (oddChainParts T).sigma (fun w => w.divisors),
            (liouvilleLambda (wd.1 / wd.2) : ℝ) * Ucal wd.1 X := by
      apply Finset.sum_bij (fun du _ => ⟨du.1 * du.2, du.1⟩)
      · rintro ⟨d, u⟩ hmem
        simp only [Finset.mem_sigma, oddChainParts, Finset.mem_filter, Finset.mem_Icc,
          Nat.mem_divisors] at hmem ⊢
        rcases hmem with ⟨⟨⟨hd1, _⟩, hd_odd, _⟩, ⟨⟨hu1, _⟩, hu_odd, h2u_div⟩⟩
        have h2du_le : 2 * (d * u) ≤ T := by
          have hm := (Nat.le_div_iff_mul_le hd1).mp h2u_div
          linarith [show 2 * (d * u) = 2 * u * d by ring]
        have hdu1 : 1 ≤ d * u := Nat.mul_pos hd1 hu1
        exact ⟨⟨⟨hdu1, by omega⟩, hd_odd.mul hu_odd, h2du_le⟩, ⟨dvd_mul_right d u, by omega⟩⟩
      · rintro ⟨d1, u1⟩ h1 ⟨d2, u2⟩ _ h_eq
        simp only [Sigma.mk.inj_iff, heq_eq_eq] at h_eq
        rcases h_eq with ⟨h_prod, rfl⟩
        have hd1_pos : 0 < d1 :=
          (Finset.mem_Icc.mp (Finset.mem_filter.mp (Finset.mem_sigma.mp h1).1).1).1
        have hu_eq : u1 = u2 := Nat.eq_of_mul_eq_mul_left hd1_pos h_prod
        subst hu_eq; rfl
      · rintro ⟨w, d⟩ hmem
        simp only [Finset.mem_sigma, oddChainParts, Finset.mem_filter, Finset.mem_Icc,
          Nat.mem_divisors] at hmem
        rcases hmem with ⟨⟨⟨_, _⟩, hw_odd, h2w_T⟩, ⟨hd_dvd, _⟩⟩
        let u := w / d
        have hdu : d * u = w := Nat.mul_div_cancel' hd_dvd
        obtain ⟨hd_odd, hu_odd⟩ := odd_of_odd_mul_tc063_aux (by rwa [hdu])
        have hd1 : 1 ≤ d := hd_odd.pos
        have hu1 : 1 ≤ u := hu_odd.pos
        have h2d_le : 2 * d ≤ T := by
          have h1 : 2 * (d * 1) ≤ 2 * (d * u) :=
            Nat.mul_le_mul_left 2 (Nat.mul_le_mul_left d hu1)
          rw [mul_one, hdu] at h1
          omega
        have h2u_div : 2 * u ≤ T / d :=
          (Nat.le_div_iff_mul_le hd1).mpr (by linarith [show 2 * u * d = 2 * (d * u) by ring])
        refine ⟨⟨d, u⟩, ?_, ?_⟩
        · simp only [Finset.mem_sigma, oddChainParts, Finset.mem_filter, Finset.mem_Icc]
          exact ⟨⟨⟨hd1, by omega⟩, hd_odd, h2d_le⟩, ⟨⟨hu1, by omega⟩, hu_odd, h2u_div⟩⟩
        · simp [hdu]
      · rintro ⟨d, u⟩ hmem
        have hd1 : 0 < d :=
          (Finset.mem_Icc.mp (Finset.mem_filter.mp (Finset.mem_sigma.mp hmem).1).1).1
        dsimp only
        rw [Nat.mul_div_right u hd1]
    rw [h_reindex, Finset.sum_sigma, Finset.sum_filter]
    apply Finset.sum_congr rfl
    intro w hw
    have hw_bds := Finset.mem_filter.mp hw
    have hw1 : 1 ≤ w := (Finset.mem_Icc.mp hw_bds.1).1
    have hw_odd : Odd w := hw_bds.2.1
    dsimp only
    rw [← Finset.sum_mul, odd_divisor_liouville_quotient_sum_tc063_aux hw_odd hw1]
    split_ifs <;> ring
  · unfold dilatedOddChainSumGcal
    simp only [Nat.div_one, one_mul]
    change (∑ e ∈ oddChainParts T,
        (ArithmeticFunction.moebius e : ℝ) *
          ∑ w ∈ (oddChainParts (T / e)).filter IsSquare, Ucal (e * w) X) =
      ∑ n ∈ oddChainParts T, (liouvilleLambda n : ℝ) * Ucal n X
    simp_rw [Finset.mul_sum]
    rw [← Finset.sum_sigma (oddChainParts T)
      (fun e => (oddChainParts (T / e)).filter IsSquare)
      (fun ew => (ArithmeticFunction.moebius ew.1 : ℝ) * Ucal (ew.1 * ew.2) X)]
    have h_reindex_sq :
        (∑ ew ∈ (oddChainParts T).sigma (fun e => (oddChainParts (T / e)).filter IsSquare),
            (ArithmeticFunction.moebius ew.1 : ℝ) * Ucal (ew.1 * ew.2) X) =
          ∑ nr ∈ (oddChainParts T).sigma (fun n => squareDivisors n),
            (ArithmeticFunction.moebius (nr.1 / nr.2 ^ 2) : ℝ) * Ucal nr.1 X := by
      apply Finset.sum_bij (fun ew _ => ⟨ew.1 * ew.2, Nat.sqrt ew.2⟩)
      · rintro ⟨e, w⟩ hmem
        simp only [Finset.mem_sigma, oddChainParts, Finset.mem_filter, Finset.mem_Icc,
          squareDivisors, Nat.mem_divisors] at hmem ⊢
        rcases hmem with ⟨⟨⟨he1, _⟩, he_odd, _⟩, ⟨⟨⟨hw1, _⟩, hw_odd, h2w_div⟩, ⟨r, hr_eq⟩⟩⟩
        have hr_sq : (Nat.sqrt w) ^ 2 = w := by rw [hr_eq, Nat.sqrt_eq, sq]
        have h2ew_le : 2 * (e * w) ≤ T := by
          have hm := (Nat.le_div_iff_mul_le he1).mp h2w_div
          linarith [show 2 * (e * w) = 2 * w * e by ring]
        have hew1 : 1 ≤ e * w := Nat.mul_pos he1 hw1
        have hr_dvd_w : Nat.sqrt w ∣ w := ⟨Nat.sqrt w, by rw [← sq, hr_sq]⟩
        exact ⟨⟨⟨hew1, by omega⟩, he_odd.mul hw_odd, h2ew_le⟩,
          ⟨⟨dvd_trans hr_dvd_w (dvd_mul_left w e), by omega⟩, ⟨e, by rw [hr_sq, mul_comm]⟩⟩⟩
      · rintro ⟨e1, w1⟩ h1 ⟨e2, w2⟩ h2 h_eq
        simp only [Sigma.mk.inj_iff, heq_eq_eq] at h_eq
        rcases h_eq with ⟨h_prod, h_sqrt⟩
        obtain ⟨r1, hr1⟩ := (Finset.mem_filter.mp (Finset.mem_sigma.mp h1).2).2
        obtain ⟨r2, hr2⟩ := (Finset.mem_filter.mp (Finset.mem_sigma.mp h2).2).2
        dsimp only at hr1 hr2
        have hw1_sq : (Nat.sqrt w1) ^ 2 = w1 := by rw [hr1, Nat.sqrt_eq, sq]
        have hw2_sq : (Nat.sqrt w2) ^ 2 = w2 := by rw [hr2, Nat.sqrt_eq, sq]
        have hw_eq : w1 = w2 := by rw [← hw1_sq, h_sqrt, hw2_sq]
        subst hw_eq
        have hw1_pos : 0 < w1 :=
          (Finset.mem_Icc.mp (Finset.mem_filter.mp (Finset.mem_filter.mp (Finset.mem_sigma.mp h1).2).1).1).1
        have he_eq : e1 = e2 := Nat.eq_of_mul_eq_mul_right hw1_pos h_prod
        subst he_eq; rfl
      · rintro ⟨n, r⟩ hmem
        simp only [Finset.mem_sigma, oddChainParts, Finset.mem_filter, Finset.mem_Icc,
          squareDivisors, Nat.mem_divisors] at hmem
        rcases hmem with ⟨⟨⟨_, _⟩, hn_odd, h2n_T⟩, ⟨⟨_, _⟩, hr2_dvd⟩⟩
        let w := r ^ 2
        let e := n / w
        have hew : e * w = n := Nat.div_mul_cancel hr2_dvd
        obtain ⟨he_odd, hw_odd⟩ := odd_of_odd_mul_tc063_aux (by rwa [hew])
        have he1 : 1 ≤ e := he_odd.pos
        have hw1 : 1 ≤ w := hw_odd.pos
        have h2e_le : 2 * e ≤ T := by
          have h1 : 2 * (e * 1) ≤ 2 * (e * w) :=
            Nat.mul_le_mul_left 2 (Nat.mul_le_mul_left e hw1)
          rw [mul_one, hew] at h1
          omega
        have h2w_div : 2 * w ≤ T / e :=
          (Nat.le_div_iff_mul_le he1).mpr (by linarith [show 2 * w * e = 2 * (e * w) by ring])
        have hw_sq : IsSquare w := ⟨r, sq r⟩
        refine ⟨⟨e, w⟩, ?_, ?_⟩
        · simp only [Finset.mem_sigma, oddChainParts, Finset.mem_filter, Finset.mem_Icc]
          exact ⟨⟨⟨he1, by omega⟩, he_odd, h2e_le⟩,
            ⟨⟨⟨hw1, by omega⟩, hw_odd, h2w_div⟩, hw_sq⟩⟩
        · simp only [Sigma.mk.inj_iff, heq_eq_eq]
          exact ⟨hew, by dsimp [w]; rw [sq, Nat.sqrt_eq]⟩
      · rintro ⟨e, w⟩ hmem
        obtain ⟨r, hr_eq⟩ := (Finset.mem_filter.mp (Finset.mem_sigma.mp hmem).2).2
        dsimp only at hr_eq
        have hw_pos : 0 < w :=
          (Finset.mem_Icc.mp (Finset.mem_filter.mp (Finset.mem_filter.mp (Finset.mem_sigma.mp hmem).2).1).1).1
        have hr_sq : (Nat.sqrt w) ^ 2 = w := by rw [hr_eq, Nat.sqrt_eq, sq]
        dsimp only
        rw [hr_sq, Nat.mul_div_left e hw_pos]
    rw [h_reindex_sq, Finset.sum_sigma]
    apply Finset.sum_congr rfl
    intro n hn
    have hn1 : 1 ≤ n := (Finset.mem_Icc.mp (Finset.mem_filter.mp hn).1).1
    have hn_ne : n ≠ 0 := by omega
    dsimp only
    rw [← Finset.sum_mul]
    congr 1
    have h_inv :=
      (actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat
        Nat.prime_two 0 hn_ne).2.2.2.2.2.2.2.1
    unfold actualFlatMoebiusSquareDivisorSum at h_inv
    have h_cast :
        (∑ r ∈ squareDivisors n, (ArithmeticFunction.moebius (n / r ^ 2) : ℝ)) =
          ((∑ r ∈ squareDivisors n, ArithmeticFunction.moebius (n / r ^ 2) : ℤ) : ℝ) := by
      push_cast; rfl
    rw [h_cast, h_inv]

private theorem sign_extension_offdiag_lower_bound_tc063_aux
    {S A : Finset ℕ} (hAS : A ⊆ S) (H : ℕ → ℕ → ℝ) :
    ∃ eps : ℕ → ℝ,
      (∀ u ∈ S, eps u = 1 ∨ eps u = -1) ∧
        (∀ u ∈ A, eps u = 1) ∧
        (∑ u ∈ A, ∑ v ∈ A.erase u, H u v) ≤
          ∑ u ∈ S, ∑ v ∈ S.erase u, eps u * eps v * H u v := by
  have h_ind :
      ∀ (D : Finset ℕ), Disjoint A D →
        ∃ eps : ℕ → ℝ,
          (∀ u ∈ A ∪ D, eps u = 1 ∨ eps u = -1) ∧
            (∀ u ∈ A, eps u = 1) ∧
            (∑ u ∈ A, ∑ v ∈ A.erase u, H u v) ≤
              ∑ u ∈ A ∪ D, ∑ v ∈ (A ∪ D).erase u, eps u * eps v * H u v := by
    intro D
    induction D using Finset.induction_on with
    | empty =>
      intro _
      refine ⟨fun _ => 1, fun _ _ => Or.inl rfl, fun _ _ => rfl, ?_⟩
      simp
    | @insert w D' hw_not_D ih =>
      intro h_disj
      have hw_not_A : w ∉ A := fun hwA =>
        Finset.disjoint_left.mp h_disj hwA (Finset.mem_insert_self w D')
      have h_disj' : Disjoint A D' :=
        Finset.disjoint_of_subset_right (Finset.subset_insert w D') h_disj
      obtain ⟨eps0, heps0_pm, heps0_A, h_le0⟩ := ih h_disj'
      let B := A ∪ D'
      have hw_not_B : w ∉ B := by
        simp only [B, Finset.mem_union, not_or]
        exact ⟨hw_not_A, hw_not_D⟩
      let cross : ℝ := ∑ u ∈ B, eps0 u * (H w u + H u w)
      let sw : ℝ := if 0 ≤ cross then 1 else -1
      let eps : ℕ → ℝ := fun u => if u = w then sw else eps0 u
      have h_union_eq : A ∪ insert w D' = insert w B := Finset.union_insert w A D'
      rw [h_union_eq]
      refine ⟨eps, ?_, ?_, ?_⟩
      · intro u hu
        rw [Finset.mem_insert] at hu
        rcases hu with rfl | huB
        · dsimp [eps, sw]
          rw [if_pos rfl]
          split_ifs <;> [exact Or.inl rfl; exact Or.inr rfl]
        · have hu_ne : u ≠ w := fun h => hw_not_B (h ▸ huB)
          dsimp [eps]
          rw [if_neg hu_ne]
          exact heps0_pm u huB
      · intro u huA
        have hu_ne : u ≠ w := fun h => hw_not_A (h ▸ huA)
        dsimp [eps]
        rw [if_neg hu_ne]
        exact heps0_A u huA
      · have h_expand :
            (∑ u ∈ insert w B, ∑ v ∈ (insert w B).erase u, eps u * eps v * H u v) =
              (∑ u ∈ B, ∑ v ∈ B.erase u, eps0 u * eps0 v * H u v) + sw * cross := by
          rw [Finset.sum_insert hw_not_B, Finset.erase_insert hw_not_B]
          have h_first :
              (∑ v ∈ B, eps w * eps v * H w v) =
                sw * ∑ v ∈ B, eps0 v * H w v := by
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro v hvB
            have hv_ne : v ≠ w := fun h => hw_not_B (h ▸ hvB)
            dsimp [eps]
            rw [if_pos rfl, if_neg hv_ne]
            ring
          have h_rest :
              (∑ u ∈ B, ∑ v ∈ (insert w B).erase u, eps u * eps v * H u v) =
                (∑ u ∈ B, sw * (eps0 u * H u w)) +
                  ∑ u ∈ B, ∑ v ∈ B.erase u, eps0 u * eps0 v * H u v := by
            rw [← Finset.sum_add_distrib]
            apply Finset.sum_congr rfl
            intro u huB
            have hu_ne_w : u ≠ w := fun h => hw_not_B (h ▸ huB)
            have h_er_ins : (insert w B).erase u = insert w (B.erase u) := by
              ext x
              simp only [Finset.mem_erase, Finset.mem_insert]
              constructor
              · rintro ⟨hx_ne_u, rfl | hxB⟩
                · exact Or.inl rfl
                · exact Or.inr ⟨hx_ne_u, hxB⟩
              · rintro (rfl | ⟨hx_ne_u, hxB⟩)
                · exact ⟨hu_ne_w.symm, Or.inl rfl⟩
                · exact ⟨hx_ne_u, Or.inr hxB⟩
            have hw_not_Ber : w ∉ B.erase u := fun h => hw_not_B (Finset.mem_of_mem_erase h)
            rw [h_er_ins, Finset.sum_insert hw_not_Ber]
            congr 1
            · dsimp [eps]
              rw [if_neg hu_ne_w, if_pos rfl]
              ring
            · apply Finset.sum_congr rfl
              intro v hv
              have hv_ne_w : v ≠ w := fun h =>
                hw_not_B (h ▸ Finset.mem_of_mem_erase hv)
              dsimp [eps]
              rw [if_neg hu_ne_w, if_neg hv_ne_w]
          rw [h_first, h_rest, ← Finset.mul_sum]
          have h_cross_split :
              sw * (∑ v ∈ B, eps0 v * H w v) + sw * (∑ u ∈ B, eps0 u * H u w) = sw * cross := by
            dsimp [cross]
            rw [← mul_add, ← Finset.sum_add_distrib]
            congr 1
            apply Finset.sum_congr rfl
            intro u _; ring
          linarith
        have h_sw_nn : 0 ≤ sw * cross := by
          dsimp [sw]
          by_cases hc : 0 ≤ cross
          · rw [if_pos hc]; linarith
          · rw [if_neg hc]; linarith
        rw [h_expand]
        linarith
  obtain ⟨eps, h_pm, h_A, h_le⟩ := h_ind (S \ A) Finset.disjoint_sdiff
  rw [Finset.union_sdiff_of_subset hAS] at h_pm h_le
  exact ⟨eps, h_pm, h_A, h_le⟩

/-- **Theorem 5 (`TASK-TC-063` §6, Odd-Divisor Square Projection, Finite Odd-Möbius Recovery, Station-Level Selberg Decomposition, and Constructive Arbitrary-Sign Obstruction)**:
    1. *Odd-divisor square-indicator identity, square projection of `dilatedOddChainSumGcal`, and finite odd-Möbius recovery of `dilatedOddChainSumGcal ... 1`*;
    2. *Station-level Selberg decomposition of `adjustedStationProfilePsi` (`1 ≤ n ≤ T`, `0 < X`, `Real.log X ≠ 0`)*:
       `adjustedStationProfilePsi c_lam c_half T D0 n X = ((Real.log (X / n) / Real.log X)^2 + 2 * (Real.log n / Real.log X) - λ(n) * openCoreSmoothCoeffS c_lam c_half T D0 n / (Real.log X)^2) * gaussianTermPhi n X`;
    3. *Constructive `±1` sign-extension lower bound*:
       For any `A ⊆ S` and `H : ℕ → ℕ → ℝ`, there exists `eps : ℕ → {+1, -1}` on `S` extending `+1` on `A` such that
       `∑ u ∈ A, ∑ v ∈ A.erase u, H u v ≤ ∑ u ∈ S, ∑ v ∈ S.erase u, eps u * eps v * H u v`. -/
theorem odd_square_projection_selberg_split_and_sign_extension_obstruction_tc063 :
    ((∀ (n : ℕ), Odd n → 1 ≤ n →
        (∑ d ∈ n.divisors, (liouvilleLambda (n / d) : ℝ)) = if IsSquare n then 1 else 0) ∧
      (∀ (c_lam c_half : ℝ) (T D0 : ℕ) (X : ℝ),
        (∑ d ∈ oddChainParts T, dilatedOddChainSumGcal c_lam c_half T D0 d X) =
          ∑ w ∈ (oddChainParts T).filter IsSquare,
            oddChainAdjustedProfileUcal c_lam c_half T D0 w X) ∧
      (∀ (c_lam c_half : ℝ) (T D0 : ℕ) (X : ℝ),
        (∑ e ∈ oddChainParts T,
          (ArithmeticFunction.moebius e : ℝ) *
            ∑ w ∈ (oddChainParts (T / e)).filter IsSquare,
              oddChainAdjustedProfileUcal c_lam c_half T D0 (e * w) X) =
          dilatedOddChainSumGcal c_lam c_half T D0 1 X)) ∧
    (∀ (c_lam c_half : ℝ) (T D0 n : ℕ),
      1 ≤ n → n ≤ T → ∀ {X : ℝ}, 0 < X → Real.log X ≠ 0 →
        adjustedStationProfilePsi c_lam c_half T D0 n X =
          ((Real.log (X / (n : ℝ)) / Real.log X) ^ 2 +
              2 * (Real.log (n : ℝ) / Real.log X) -
              (liouvilleLambda n : ℝ) * openCoreSmoothCoeffS c_lam c_half T D0 n /
                (Real.log X) ^ 2) *
            gaussianTermPhi n X) ∧
    (∀ (S A : Finset ℕ), A ⊆ S → ∀ (H : ℕ → ℕ → ℝ),
      ∃ eps : ℕ → ℝ,
        (∀ u ∈ S, eps u = 1 ∨ eps u = -1) ∧
          (∀ u ∈ A, eps u = 1) ∧
          (∑ u ∈ A, ∑ v ∈ A.erase u, H u v) ≤
            ∑ u ∈ S, ∑ v ∈ S.erase u, eps u * eps v * H u v) := by
  refine ⟨⟨fun _ hn_odd hn1 => odd_divisor_liouville_quotient_sum_tc063_aux hn_odd hn1,
      fun c_lam c_half T D0 X =>
        (odd_square_projection_and_moebius_recovery_tc063_aux c_lam c_half T D0 X).1,
      fun c_lam c_half T D0 X =>
        (odd_square_projection_and_moebius_recovery_tc063_aux c_lam c_half T D0 X).2⟩,
    ?_,
    fun S A hAS H => sign_extension_offdiag_lower_bound_tc063_aux hAS H⟩
  intro c_lam c_half T D0 n hn1 hnT X hX hlogX
  have hn_ne : n ≠ 0 := by omega
  have hn_r_ne : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn_ne
  have hX_ne : X ≠ 0 := ne_of_gt hX
  have h_lam_sq : (liouvilleLambda n : ℝ) * (liouvilleLambda n : ℝ) = 1 := by
    have h_int : liouvilleLambda n * liouvilleLambda n = 1 := by
      simp only [liouvilleLambda, hn_ne, ↓reduceIte, liouvilleSignFromOmega]
      rw [← pow_add, show natOmega n + natOmega n = 2 * natOmega n by omega, pow_mul]
      norm_num
    exact_mod_cast h_int
  unfold adjustedStationProfilePsi signedAdjustedCoeffB openCoreAdjustedCoeffBeta
    truncatedLiouvilleCoeff
  rw [if_pos ⟨hn1, hnT⟩, Real.log_div hX_ne hn_r_ne]
  have h_coeff :
      1 - (liouvilleLambda n : ℝ) *
            (openCoreSmoothCoeffS c_lam c_half T D0 n -
              (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2) /
          (Real.log X) ^ 2 =
        ((Real.log X - Real.log (n : ℝ)) / Real.log X) ^ 2 +
          2 * (Real.log (n : ℝ) / Real.log X) -
          (liouvilleLambda n : ℝ) * openCoreSmoothCoeffS c_lam c_half T D0 n /
            (Real.log X) ^ 2 := by
    have h_prod :
        (liouvilleLambda n : ℝ) *
            (openCoreSmoothCoeffS c_lam c_half T D0 n -
              (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2) =
          (liouvilleLambda n : ℝ) * openCoreSmoothCoeffS c_lam c_half T D0 n -
            (Real.log (n : ℝ)) ^ 2 := by
      calc
        (liouvilleLambda n : ℝ) *
            (openCoreSmoothCoeffS c_lam c_half T D0 n -
              (liouvilleLambda n : ℝ) * (Real.log (n : ℝ)) ^ 2)
          = (liouvilleLambda n : ℝ) * openCoreSmoothCoeffS c_lam c_half T D0 n -
              ((liouvilleLambda n : ℝ) * (liouvilleLambda n : ℝ)) *
                (Real.log (n : ℝ)) ^ 2 := by ring
        _ = (liouvilleLambda n : ℝ) * openCoreSmoothCoeffS c_lam c_half T D0 n -
              (Real.log (n : ℝ)) ^ 2 := by rw [h_lam_sq, one_mul]
    rw [h_prod]
    field_simp [hlogX]
    ring
  rw [h_coeff]

end RiemannScope
