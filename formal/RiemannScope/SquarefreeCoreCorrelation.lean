/-
RiemannScope.SquarefreeCoreCorrelation
TASK-TC-064 (EPIC-TC-042 / SUBGATE-TC-043A):
Squarefree-Core Correlations and the Arithmetic Regularity Constraint.

Formalizes in Lean 4 (complete machine-checked proofs using canonical circle constant
RiemannScope.tau throughout; complex arguments written z = (x : ℂ) + (y : ℂ) * Complex.I
with real coordinates x, y and critical line x = 1 / 2):
1. `exact_odd_squarefree_core_bijection_and_complete_kernel_split_tc064`
2. `divisor_core_star_involution_and_support_bijection_tc064`
3. `uniform_same_core_hilbert_bound_and_closure_transfer_tc064`
4. `squarefree_core_gcd_prime_sector_and_prime_toggle_identities_tc064`
5. `finite_euler_factor_dirichlet_multiplier_and_dilation_equivalence_tc064`
-/

import RiemannScope.DyadicChainCorrelationRegularity

open scoped ArithmeticFunction BigOperators
open MeasureTheory intervalIntegral

namespace RiemannScope

open RiemannScope.LiouvilleSquareDilation
open RiemannScope.DyadicPowerLiftPrimitiveCorrelation hiding canonicalPrimePowerDiagDtilde
open RiemannScope.SignedDilationArithmeticEnergy
open RiemannScope.MixedArithmeticCovariance
open RiemannScope.JointPrimeDilationSignedRemainder

/-! ### Core Definitions (`TASK-TC-064`) -/

/-- Complete dyadic-chain grouped prime-power feature vector
    `Vcal_{u, pk}(X) := ∑_{j ∈ J_u(T)} V_{4^j u, pk}(X)`. -/
noncomputable def oddChainFeatureVectorVcal (u T : ℕ) (pk : ℕ × ℕ) (X : ℝ) : ℝ :=
  ∑ j ∈ dyadicChainExponents u T, stationFeatureDiffV (4 ^ j * u) pk X

/-- Odd squarefree core index set `C_odd(T) := {a ∈ [1, T] : Odd a ∧ Squarefree a ∧ 2 * a ≤ T}`. -/
def oddSquarefreeCores (T : ℕ) : Finset ℕ :=
  (Finset.Icc 1 T).filter (fun a => Odd a ∧ Squarefree a ∧ 2 * a ≤ T)

/-- Odd square-multiplier set `B_a(T) := {b ∈ [1, T] : Odd b ∧ 2 * a * b^2 ≤ T}` for core `a`. -/
def coreSquareMultipliers (a T : ℕ) : Finset ℕ :=
  (Finset.Icc 1 T).filter (fun b => Odd b ∧ 2 * a * b ^ 2 ≤ T)

/-- Squarefree-core grouped adjusted profile
    `Acal_a(X) := ∑_{b ∈ B_a(T)} Ucal_{a * b^2}(X)`. -/
noncomputable def coreAdjustedProfileA (c_lam c_half : ℝ) (T D0 a : ℕ) (X : ℝ) : ℝ :=
  ∑ b ∈ coreSquareMultipliers a T, oddChainAdjustedProfileUcal c_lam c_half T D0 (a * b ^ 2) X

/-- Squarefree-core grouped prime-power feature vector
    `Bcal_{a, pk}(X) := ∑_{b ∈ B_a(T)} Vcal_{a * b^2, pk}(X)`. -/
noncomputable def coreFeatureVectorB (a T : ℕ) (pk : ℕ × ℕ) (X : ℝ) : ℝ :=
  ∑ b ∈ coreSquareMultipliers a T, oddChainFeatureVectorVcal (a * b ^ 2) T pk X

/-- Complete squarefree-core pair interaction kernel `Mcal_Y(a, c)`. -/
noncomputable def completeCorePairKernelMcal (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ)
    (a c : ℕ) : ℝ :=
  windowPairing Y (coreAdjustedProfileA c_lam c_half T D0 a)
      (coreAdjustedProfileA c_lam c_half T D0 c) -
    4 * ∑ pk ∈ primePowerPairsUpTo T,
      windowPairing Y (fun X => coreFeatureVectorB a T pk X)
        (fun X => coreFeatureVectorB c T pk X)

/-- Distinct-squarefree-core (`a ≠ c`) Möbius-signed correlation sum `S_core(T, D0, Y)`. -/
noncomputable def distinctSquarefreeCoreSumS (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ) : ℝ :=
  ∑ a ∈ oddSquarefreeCores T,
    ∑ c ∈ (oddSquarefreeCores T).erase a,
      (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
        completeCorePairKernelMcal c_lam c_half T D0 Y a c

/-- Canonical-schedule (`T = canonicalCutoffT Y`, `D0 = ⌊log Y⌋`) distinct-squarefree-core sum. -/
noncomputable def canonicalDistinctSquarefreeCoreSumS (c_lam c_half : ℝ) (Y : ℝ) : ℝ :=
  distinctSquarefreeCoreSumS c_lam c_half (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y

/-- Same-core distinct-square-multiplier (`b ≠ d`) remainder `R_square(T, D0, Y)`. -/
noncomputable def sameCoreSquareRemainderR (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ) : ℝ :=
  (∑ a ∈ oddSquarefreeCores T, completeCorePairKernelMcal c_lam c_half T D0 Y a a) -
    (∑ u ∈ oddChainParts T,
      (windowEnergyNormSq Y (oddChainAdjustedProfileUcal c_lam c_half T D0 u) -
        4 * ∑ pk ∈ primePowerPairsUpTo T,
          windowEnergyNormSq Y (fun X => oddChainFeatureVectorVcal u T pk X)))

/-- Canonical-schedule (`T = canonicalCutoffT Y`, `D0 = ⌊log Y⌋`) same-core square remainder. -/
noncomputable def canonicalSameCoreSquareRemainderR (c_lam c_half : ℝ) (Y : ℝ) : ℝ :=
  sameCoreSquareRemainderR c_lam c_half (canonicalCutoffT Y) (Nat.floor (Real.log Y)) Y

/-- Squarefree symmetric-difference multiplication `a ⋆ c := a * c / gcd(a, c)^2`. -/
def squarefreeCoreStar (a c : ℕ) : ℕ :=
  a * c / (Nat.gcd a c) ^ 2

/-- Odd squarefree common-factor `gcd` index set `{g ∈ C_odd(T) : 6 * g ≤ T}`. -/
def oddSquarefreeCommonFactorSet (T : ℕ) : Finset ℕ :=
  (oddSquarefreeCores T).filter (fun g => 6 * g ≤ T)

/-- Primitive coprime squarefree-core pair set at odd squarefree common factor `g`. -/
def primitiveSquarefreeCorePairs (T g : ℕ) : Finset (ℕ × ℕ) :=
  (oddSquarefreeCores (T / g) ×ˢ oddSquarefreeCores (T / g)).filter
    (fun rt => rt.1 ≠ rt.2 ∧ Nat.Coprime rt.1 rt.2 ∧ Nat.Coprime g (rt.1 * rt.2))

/-- Primitive squarefree-core correlation sector `Π_core(T, D0, Y; g)` at common factor `g`. -/
noncomputable def primitiveSquarefreeCoreSectorPi (c_lam c_half : ℝ) (T D0 : ℕ) (Y : ℝ)
    (g : ℕ) : ℝ :=
  ∑ rt ∈ primitiveSquarefreeCorePairs T g,
    (ArithmeticFunction.moebius rt.1 : ℝ) * (ArithmeticFunction.moebius rt.2 : ℝ) *
      completeCorePairKernelMcal c_lam c_half T D0 Y (g * rt.1) (g * rt.2)

/-- Divisible-core Möbius-signed grouped profile sum `Scal_d(X) := ∑_{d ∣ a} μ(a) Acal_a(X)`. -/
noncomputable def divisibleCoreProfileSumS (c_lam c_half : ℝ) (T D0 d : ℕ) (X : ℝ) : ℝ :=
  ∑ a ∈ (oddSquarefreeCores T).filter (fun a => d ∣ a),
    (ArithmeticFunction.moebius a : ℝ) * coreAdjustedProfileA c_lam c_half T D0 a X

/-- Divisible-core Möbius-signed grouped feature sum `Fcal_{d, pk}(X) := ∑_{d ∣ a} μ(a) Bcal_{a, pk}(X)`. -/
noncomputable def divisibleCoreFeatureSumF (T d : ℕ) (pk : ℕ × ℕ) (X : ℝ) : ℝ :=
  ∑ a ∈ (oddSquarefreeCores T).filter (fun a => d ∣ a),
    (ArithmeticFunction.moebius a : ℝ) * coreFeatureVectorB a T pk X

/-- Prime-toggle interior-paired squarefree cores `{a ∈ C_odd(T) : a ⋆ p ∈ C_odd(T)}`. -/
def primeTogglePairedCores (p T : ℕ) : Finset ℕ :=
  (oddSquarefreeCores T).filter (fun a => squarefreeCoreStar a p ∈ oddSquarefreeCores T)

/-- Prime-toggle cutoff-boundary squarefree cores `{a ∈ C_odd(T) : a ⋆ p ∉ C_odd(T)}`. -/
def primeToggleBoundaryCores (p T : ℕ) : Finset ℕ :=
  (oddSquarefreeCores T).filter (fun a => squarefreeCoreStar a p ∉ oddSquarefreeCores T)

/-- Single-prime valuation-toggled Liouville sequence `a_q(n) := λ(n) * (-1)^{v_q(n)}`. -/
def primeValuationToggleSeq (q n : ℕ) : ℤ :=
  liouvilleLambda n * (-1 : ℤ) ^ (n.factorization q)

/-- Infinite sequence Gaussian observable `Q_a(X) := ∑'_{n ≥ 1} a(n) φ_n(X)`. -/
noncomputable def infiniteSeqGaussianObservableQ (a : ℕ → ℝ) (X : ℝ) : ℝ :=
  ∑' n : ℕ, if n = 0 then 0 else a n * gaussianTermPhi n X

/-- Finite `T`-truncated sequence Gaussian observable `Q_{a, T}(X) := ∑_{1 ≤ n ≤ T} a(n) φ_n(X)`. -/
noncomputable def truncatedSeqGaussianObservableQ (a : ℕ → ℝ) (T : ℕ) (X : ℝ) : ℝ :=
  ∑ n ∈ Finset.Icc 1 T, a n * gaussianTermPhi n X

open scoped Classical

/-! ### Section 1: Odd Squarefree-Core Bijection & Complete-Kernel Split (`TASK-TC-064` §2) -/

private theorem odd_of_odd_mul_tc064_aux {a b : ℕ} (h : Odd (a * b)) : Odd a ∧ Odd b := by
  constructor
  · rcases Nat.even_or_odd a with ha_ev | ha_odd
    · obtain ⟨k, rfl⟩ := even_iff_two_dvd.mp ha_ev
      exact False.elim ((Nat.odd_iff_not_even.mp h) (even_iff_two_dvd.mpr ⟨k * b, by ring⟩))
    · exact ha_odd
  · rcases Nat.even_or_odd b with hb_ev | hb_odd
    · obtain ⟨k, rfl⟩ := even_iff_two_dvd.mp hb_ev
      exact False.elim ((Nat.odd_iff_not_even.mp h) (even_iff_two_dvd.mpr ⟨a * k, by ring⟩))
    · exact hb_odd

private theorem odd_of_odd_sq_tc064_aux {b : ℕ} (h : Odd (b ^ 2)) : Odd b :=
  (odd_of_odd_mul_tc064_aux (by rwa [← sq])).1

private theorem squarefree_pos_and_coprime_of_mul_tc064_aux :
    (∀ {a : ℕ}, Squarefree a → 1 ≤ a) ∧
      (∀ {x y : ℕ}, Squarefree (x * y) → Squarefree x ∧ Squarefree y ∧ Nat.Coprime x y) := by
  refine ⟨?_, ?_⟩
  · intro a ha
    exact Nat.one_le_iff_ne_zero.mpr ha.ne_zero
  · intro x y hxy
    refine ⟨hxy.squarefree_of_dvd (dvd_mul_right x y),
      hxy.squarefree_of_dvd (dvd_mul_left y x), ?_⟩
    rw [Nat.Coprime]
    let d := Nat.gcd x y
    have hd_sq_dvd : d * d ∣ x * y := mul_dvd_mul (Nat.gcd_dvd_left x y) (Nat.gcd_dvd_right x y)
    exact Nat.isUnit_iff.mp (hxy d hd_sq_dvd)

private theorem unique_odd_squarefree_mul_sq_tc064_aux {u : ℕ} (hu : Odd u) :
    ∃! ab : ℕ × ℕ, Odd ab.1 ∧ Squarefree ab.1 ∧ Odd ab.2 ∧ ab.1 * ab.2 ^ 2 = u := by
  obtain ⟨a, b, _, _, hba, ha_sf⟩ := Nat.sq_mul_squarefree_of_pos hu.pos
  have hab : a * b ^ 2 = u := by linarith [hba]
  have hab_odd : Odd a ∧ Odd (b ^ 2) := odd_of_odd_mul_tc064_aux (by rwa [hab])
  have ha_odd : Odd a := hab_odd.1
  have hb_odd : Odd b := odd_of_odd_sq_tc064_aux hab_odd.2
  refine ⟨(a, b), ⟨ha_odd, ha_sf, hb_odd, hab⟩, ?_⟩
  rintro ⟨a', b'⟩ ⟨ha'_odd, ha'_sf, hb'_odd, hab'⟩
  dsimp only at ha'_odd ha'_sf hb'_odd hab'
  have ha_ne : a ≠ 0 := ne_of_gt ha_odd.pos
  have hb_ne : b ≠ 0 := ne_of_gt hb_odd.pos
  have ha'_ne : a' ≠ 0 := ne_of_gt ha'_odd.pos
  have hb'_ne : b' ≠ 0 := ne_of_gt hb'_odd.pos
  have h_eq : a' * b' ^ 2 = a * b ^ 2 := hab'.trans hab.symm
  have h_fact : ∀ p : ℕ, a'.factorization p = a.factorization p ∧
      b'.factorization p = b.factorization p := by
    intro p
    have hfp := congr_arg (fun n => n.factorization p) h_eq
    dsimp only at hfp
    rw [Nat.factorization_mul ha'_ne (pow_ne_zero 2 hb'_ne),
      Nat.factorization_mul ha_ne (pow_ne_zero 2 hb_ne),
      Finsupp.add_apply, Finsupp.add_apply,
      Nat.factorization_pow, Nat.factorization_pow,
      Finsupp.smul_apply, Finsupp.smul_apply, smul_eq_mul, smul_eq_mul] at hfp
    have h1 := (Nat.squarefree_iff_factorization_le_one ha'_ne).mp ha'_sf p
    have h2 := (Nat.squarefree_iff_factorization_le_one ha_ne).mp ha_sf p
    omega
  have ha_eq : a' = a := Nat.eq_of_factorization_eq ha'_ne ha_ne (fun p => (h_fact p).1)
  have hb_eq : b' = b := Nat.eq_of_factorization_eq hb'_ne hb_ne (fun p => (h_fact p).2)
  rw [ha_eq, hb_eq]

private theorem liouvilleLambda_squarefree_mul_sq_eq_moebius_tc064_aux
    {a b : ℕ} (ha_sf : Squarefree a) (hb1 : 1 ≤ b) :
    liouvilleLambda (a * b ^ 2) = ArithmeticFunction.moebius a ∧
      (ArithmeticFunction.moebius a : ℝ) ^ 2 = 1 := by
  have ha1 : 1 ≤ a := squarefree_pos_and_coprime_of_mul_tc064_aux.1 ha_sf
  have ha_ne : a ≠ 0 := by omega
  have hb_ne : b ≠ 0 := by omega
  have hb2_ne : b ^ 2 ≠ 0 := pow_ne_zero 2 hb_ne
  have hab_ne : a * b ^ 2 ≠ 0 := mul_ne_zero ha_ne hb2_ne
  have h_om_mul : natOmega (a * b ^ 2) = natOmega a + 2 * natOmega b := by
    rw [sq, natOmega, ArithmeticFunction.cardFactors_mul ha_ne (mul_ne_zero hb_ne hb_ne),
      ArithmeticFunction.cardFactors_mul hb_ne hb_ne]
    change ArithmeticFunction.cardFactors a +
      (ArithmeticFunction.cardFactors b + ArithmeticFunction.cardFactors b) =
      natOmega a + 2 * natOmega b
    unfold natOmega
    omega
  have h_lam_eq : liouvilleLambda (a * b ^ 2) = (-1 : ℤ) ^ (natOmega a) := by
    simp only [liouvilleLambda, hab_ne, ↓reduceIte, h_om_mul, liouvilleSignFromOmega]
    rw [pow_add, pow_mul]
    norm_num
  have h_mu_eq : ArithmeticFunction.moebius a = (-1 : ℤ) ^ (natOmega a) := by
    rw [ArithmeticFunction.moebius_apply_of_squarefree ha_sf]
    rfl
  refine ⟨h_lam_eq.trans h_mu_eq.symm, ?_⟩
  have h_mu_sq_int : ArithmeticFunction.moebius a ^ 2 = 1 := by
    rw [h_mu_eq, ← pow_mul, mul_comm (natOmega a) 2, pow_mul]
    norm_num
  exact_mod_cast h_mu_sq_int

private theorem oddSquarefreeCores_bijection_and_edges_tc064_aux (T : ℕ) :
    (oddSquarefreeCores T = ∅ ↔ T < 2) ∧
      (∀ a ∈ oddSquarefreeCores T, 1 ∈ coreSquareMultipliers a T) ∧
      (∀ a ∈ oddSquarefreeCores T, (coreSquareMultipliers a T).card = 1 ↔ T < 18 * a) ∧
      (∀ a ∈ oddSquarefreeCores T, ∀ b ∈ coreSquareMultipliers a T,
        a * b ^ 2 ∈ oddChainParts T) ∧
      (∀ u ∈ oddChainParts T,
        ∃! ab : ℕ × ℕ,
          ab.1 ∈ oddSquarefreeCores T ∧ ab.2 ∈ coreSquareMultipliers ab.1 T ∧
            ab.1 * ab.2 ^ 2 = u) ∧
      ((oddSquarefreeCores T).biUnion
        (fun a => (coreSquareMultipliers a T).image (fun b => a * b ^ 2)) = oddChainParts T) := by
  have h_emp : oddSquarefreeCores T = ∅ ↔ T < 2 := by
    constructor
    · intro he
      by_contra hge2
      have h1 : 1 ∈ oddSquarefreeCores T := by
        simp only [oddSquarefreeCores, Finset.mem_filter, Finset.mem_Icc]
        exact ⟨⟨le_refl 1, by omega⟩, odd_one, squarefree_one, by omega⟩
      rw [he] at h1
      exact Finset.not_mem_empty 1 h1
    · intro hlt2
      rw [Finset.eq_empty_iff_forall_not_mem]
      intro a ha
      simp only [oddSquarefreeCores, Finset.mem_filter, Finset.mem_Icc] at ha
      omega
  have h_one_in : ∀ a ∈ oddSquarefreeCores T, 1 ∈ coreSquareMultipliers a T := by
    intro a ha
    simp only [oddSquarefreeCores, coreSquareMultipliers, Finset.mem_filter, Finset.mem_Icc] at ha ⊢
    rcases ha with ⟨⟨ha1, _⟩, _, _, h2a⟩
    exact ⟨⟨le_refl 1, by omega⟩, odd_one, by simpa using h2a⟩
  have h_card1 : ∀ a ∈ oddSquarefreeCores T, (coreSquareMultipliers a T).card = 1 ↔ T < 18 * a := by
    intro a ha
    have h1_mem := h_one_in a ha
    simp only [oddSquarefreeCores, Finset.mem_filter, Finset.mem_Icc] at ha
    rcases ha with ⟨⟨ha1, _⟩, _, _, _⟩
    constructor
    · intro hc1
      by_contra hge18
      have h3_mem : 3 ∈ coreSquareMultipliers a T := by
        simp only [coreSquareMultipliers, Finset.mem_filter, Finset.mem_Icc]
        exact ⟨⟨by decide, by omega⟩, by decide, by omega⟩
      have hgt1 : 1 < (coreSquareMultipliers a T).card :=
        Finset.one_lt_card.mpr ⟨1, h1_mem, 3, h3_mem, by decide⟩
      omega
    · intro hlt18
      have h_eq1 : coreSquareMultipliers a T = {1} := by
        ext b
        rw [Finset.mem_singleton]
        constructor
        · intro hb
          simp only [coreSquareMultipliers, Finset.mem_filter, Finset.mem_Icc] at hb
          rcases hb with ⟨⟨hb1, _⟩, ⟨m, rfl⟩, h2ab2⟩
          by_contra hne1
          have hm1 : 1 ≤ m := by omega
          have hb2_ge9 : 9 ≤ (2 * m + 1) ^ 2 := by nlinarith
          have h18_le : 18 * a ≤ 2 * a * (2 * m + 1) ^ 2 := by nlinarith
          omega
        · rintro rfl
          exact h1_mem
      rw [h_eq1, Finset.card_singleton]
  have h_fwd : ∀ a ∈ oddSquarefreeCores T, ∀ b ∈ coreSquareMultipliers a T,
      a * b ^ 2 ∈ oddChainParts T := by
    intro a ha b hb
    simp only [oddSquarefreeCores, coreSquareMultipliers, oddChainParts,
      Finset.mem_filter, Finset.mem_Icc] at ha hb ⊢
    rcases ha with ⟨⟨ha1, _⟩, ha_odd, _, _⟩
    rcases hb with ⟨⟨hb1, _⟩, hb_odd, h2ab2⟩
    have hab2_ge1 : 1 ≤ a * b ^ 2 := Nat.mul_pos ha1 (pow_pos (by omega : 0 < b) 2)
    have h2_le : 2 * (a * b ^ 2) ≤ T := by linarith [show 2 * (a * b ^ 2) = 2 * a * b ^ 2 by ring]
    exact ⟨⟨hab2_ge1, by omega⟩, ha_odd.mul (hb_odd.pow), h2_le⟩
  have h_uniq : ∀ u ∈ oddChainParts T,
      ∃! ab : ℕ × ℕ,
        ab.1 ∈ oddSquarefreeCores T ∧ ab.2 ∈ coreSquareMultipliers ab.1 T ∧
          ab.1 * ab.2 ^ 2 = u := by
    intro u hu
    simp only [oddChainParts, Finset.mem_filter, Finset.mem_Icc] at hu
    rcases hu with ⟨⟨_, huT⟩, hu_odd, h2uT⟩
    obtain ⟨⟨a, b⟩, ⟨ha_odd, ha_sf, hb_odd, hab_eq⟩, h_ab_uniq⟩ :=
      unique_odd_squarefree_mul_sq_tc064_aux hu_odd
    dsimp only at ha_odd ha_sf hb_odd hab_eq
    have ha1 : 1 ≤ a := ha_odd.pos
    have hb1 : 1 ≤ b := hb_odd.pos
    have h2ab2 : 2 * a * b ^ 2 ≤ T := by
      calc
        2 * a * b ^ 2 = 2 * (a * b ^ 2) := by ring
        _ = 2 * u := by rw [hab_eq]
        _ ≤ T := h2uT
    have h2a_le : 2 * a ≤ T := by
      have hb2_ge1 : 1 ≤ b ^ 2 := pow_pos hb_odd.pos 2
      have hle : 2 * a * 1 ≤ 2 * a * b ^ 2 := Nat.mul_le_mul_left (2 * a) hb2_ge1
      omega
    have hb_le_T : b ≤ T := by
      have hb_le_b2 : b ≤ b ^ 2 := by nlinarith
      have hb2_le_u : b ^ 2 ≤ a * b ^ 2 := Nat.le_mul_of_pos_left (b ^ 2) ha1
      omega
    have ha_in : a ∈ oddSquarefreeCores T := by
      simp only [oddSquarefreeCores, Finset.mem_filter, Finset.mem_Icc]
      exact ⟨⟨ha1, by omega⟩, ha_odd, ha_sf, h2a_le⟩
    have hb_in : b ∈ coreSquareMultipliers a T := by
      simp only [coreSquareMultipliers, Finset.mem_filter, Finset.mem_Icc]
      exact ⟨⟨hb1, hb_le_T⟩, hb_odd, h2ab2⟩
    refine ⟨(a, b), ⟨ha_in, hb_in, hab_eq⟩, ?_⟩
    rintro ⟨a', b'⟩ ⟨ha'_in, hb'_in, hab'_eq⟩
    simp only [oddSquarefreeCores, coreSquareMultipliers, Finset.mem_filter] at ha'_in hb'_in
    exact h_ab_uniq (a', b') ⟨ha'_in.2.1, ha'_in.2.2.1, hb'_in.2.1, hab'_eq⟩
  refine ⟨h_emp, h_one_in, h_card1, h_fwd, h_uniq, ?_⟩
  ext u
  simp only [Finset.mem_biUnion, Finset.mem_image]
  constructor
  · rintro ⟨a, ha, b, hb, rfl⟩
    exact h_fwd a ha b hb
  · intro hu
    obtain ⟨⟨a, b⟩, ⟨ha, hb, rfl⟩, _⟩ := h_uniq u hu
    exact ⟨a, ha, b, hb, rfl⟩

private theorem two_pow_mul_odd_factorization_two_tc064_aux (r : ℕ) {u : ℕ} (hu : Odd u) :
    (2 ^ r * u).factorization 2 = r := by
  have hu_ne : u ≠ 0 := ne_of_gt hu.pos
  have h2_not_dvd : ¬ 2 ∣ u := fun h2 =>
    (Nat.odd_iff_not_even.mp hu) (even_iff_two_dvd.mpr h2)
  rw [Nat.factorization_mul (pow_ne_zero r (by decide)) hu_ne, Finsupp.add_apply,
    Nat.factorization_eq_zero_of_not_dvd h2_not_dvd, add_zero,
    Nat.Prime.factorization_pow Nat.prime_two, Finsupp.single_eq_same]

private theorem paired_station_injective_and_mem_tc064_aux :
    (∀ {a1 b1 j1 eps1 a2 b2 j2 eps2 : ℕ},
      Odd a1 → Squarefree a1 → Odd b1 → eps1 < 2 →
      Odd a2 → Squarefree a2 → Odd b2 → eps2 < 2 →
        (2 ^ (2 * j1 + eps1) * a1 * b1 ^ 2 = 2 ^ (2 * j2 + eps2) * a2 * b2 ^ 2 ↔
          a1 = a2 ∧ b1 = b2 ∧ j1 = j2 ∧ eps1 = eps2)) ∧
      (∀ (T : ℕ), ∀ a ∈ oddSquarefreeCores T, ∀ b ∈ coreSquareMultipliers a T,
        ∀ j ∈ dyadicChainExponents (a * b ^ 2) T, ∀ {eps : ℕ}, eps < 2 →
          2 ^ (2 * j + eps) * a * b ^ 2 ∈
            (Finset.Icc 1 T).filter (fun k => ∃ r b' : ℕ, Odd b' ∧ k = 2 ^ r * a * b' ^ 2)) := by
  refine ⟨?_, ?_⟩
  · intro a1 b1 j1 eps1 a2 b2 j2 eps2 ha1_o ha1_sf hb1_o heps1 ha2_o ha2_sf hb2_o heps2
    constructor
    · intro h_eq
      have hu1_o : Odd (a1 * b1 ^ 2) := ha1_o.mul (hb1_o.pow)
      have hu2_o : Odd (a2 * b2 ^ 2) := ha2_o.mul (hb2_o.pow)
      have h_mul_eq : 2 ^ (2 * j1 + eps1) * (a1 * b1 ^ 2) = 2 ^ (2 * j2 + eps2) * (a2 * b2 ^ 2) := by
        linarith [show 2 ^ (2 * j1 + eps1) * (a1 * b1 ^ 2) = 2 ^ (2 * j1 + eps1) * a1 * b1 ^ 2 by ring,
          show 2 ^ (2 * j2 + eps2) * (a2 * b2 ^ 2) = 2 ^ (2 * j2 + eps2) * a2 * b2 ^ 2 by ring]
      have hf1 := two_pow_mul_odd_factorization_two_tc064_aux (2 * j1 + eps1) hu1_o
      have hf2 := two_pow_mul_odd_factorization_two_tc064_aux (2 * j2 + eps2) hu2_o
      have h_exp : 2 * j1 + eps1 = 2 * j2 + eps2 := by rw [← hf1, h_mul_eq, hf2]
      have hj_eq : j1 = j2 := by omega
      have heps_eq : eps1 = eps2 := by omega
      subst hj_eq; subst heps_eq
      have h2_pos : 0 < 2 ^ (2 * j1 + eps1) := pow_pos (by decide) _
      have hu_eq : a1 * b1 ^ 2 = a2 * b2 ^ 2 := Nat.eq_of_mul_eq_mul_left h2_pos h_mul_eq
      obtain ⟨_, _, h_uniq⟩ := unique_odd_squarefree_mul_sq_tc064_aux hu1_o
      have h1 := h_uniq (a1, b1) ⟨ha1_o, ha1_sf, hb1_o, rfl⟩
      have h2 := h_uniq (a2, b2) ⟨ha2_o, ha2_sf, hb2_o, hu_eq.symm⟩
      have hp_eq : (a1, b1) = (a2, b2) := h1.trans h2.symm
      exact ⟨Prod.mk.inj hp_eq |>.1, Prod.mk.inj hp_eq |>.2, rfl, rfl⟩
    · rintro ⟨rfl, rfl, rfl, rfl⟩
      rfl
  · intro T a ha b hb j hj eps heps
    have hu_in := (oddSquarefreeCores_bijection_and_edges_tc064_aux T).2.2.2.1 a ha b hb
    have hu1 : 1 ≤ a * b ^ 2 := (Finset.mem_Icc.mp (Finset.mem_filter.mp hu_in).1).1
    have hj_le : 2 * 4 ^ j * (a * b ^ 2) ≤ T :=
      ((exact_odd_part_bijection_and_dyadic_chain_offdiag_split_tc063).1.2.1
        (a * b ^ 2) j T hu1).mp hj
    have hb_o : Odd b := (Finset.mem_filter.mp hb).2.1
    have h_pow_pos : 1 ≤ 2 ^ (2 * j + eps) := Nat.one_le_pow _ 2 (by decide)
    have hk_ge1 : 1 ≤ 2 ^ (2 * j + eps) * a * b ^ 2 := by
      have h1 : 1 ≤ 2 ^ (2 * j + eps) * (a * b ^ 2) := Nat.mul_pos h_pow_pos hu1
      linarith [show 2 ^ (2 * j + eps) * (a * b ^ 2) = 2 ^ (2 * j + eps) * a * b ^ 2 by ring]
    have h_pow_le : 2 ^ (2 * j + eps) ≤ 2 * 4 ^ j := by
      have h4 : (4 : ℕ) ^ j = 2 ^ (2 * j) := by
        rw [show (4 : ℕ) = 2 ^ 2 by norm_num, ← pow_mul]
      rw [h4, pow_add]
      have he2 : 2 ^ eps ≤ 2 := by
        rcases eps with _ | _ | eps'
        · norm_num
        · norm_num
        · omega
      calc
        2 ^ (2 * j) * 2 ^ eps ≤ 2 ^ (2 * j) * 2 := Nat.mul_le_mul_left _ he2
        _ = 2 * 2 ^ (2 * j) := by ring
    have hk_le_T : 2 ^ (2 * j + eps) * a * b ^ 2 ≤ T := by
      calc
        2 ^ (2 * j + eps) * a * b ^ 2 = 2 ^ (2 * j + eps) * (a * b ^ 2) := by ring
        _ ≤ (2 * 4 ^ j) * (a * b ^ 2) := Nat.mul_le_mul_right _ h_pow_le
        _ ≤ T := hj_le
    simp only [Finset.mem_filter, Finset.mem_Icc]
    exact ⟨⟨hk_ge1, hk_le_T⟩, ⟨2 * j + eps, b, hb_o, rfl⟩⟩

private theorem uIcc_tau_log_props_tc064_aux {Y : ℝ} (hY2 : 2 ≤ Y) :
    Y ≤ RiemannScope.tau * Y ∧
      ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y),
        0 < X ∧ 0 < Real.log X ∧ Real.log X ≠ 0 ∧ (Real.log X) ^ 2 ≠ 0 := by
  have hCg := (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2.1
  have hle : Y ≤ RiemannScope.tau * Y := by nlinarith [hCg]
  refine ⟨hle, ?_⟩
  intro X hX
  rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX
  have hX0 : 0 < X := by linarith
  have hlog : 0 < Real.log X := Real.log_pos (by linarith)
  exact ⟨hX0, hlog, ne_of_gt hlog, pow_ne_zero 2 (ne_of_gt hlog)⟩

private theorem continuousOn_station_and_chain_profiles_tc064_aux {Y : ℝ} (hY2 : 2 ≤ Y)
    (c_lam c_half : ℝ) (T D0 : ℕ) :
    (∀ n : ℕ, ContinuousOn (gaussianTermPhi n) (Set.uIcc Y (RiemannScope.tau * Y))) ∧
      (∀ n : ℕ, ContinuousOn (adjustedStationProfilePsi c_lam c_half T D0 n)
        (Set.uIcc Y (RiemannScope.tau * Y))) ∧
      (∀ (n : ℕ) (pk : ℕ × ℕ), ContinuousOn (stationPrimePowerFeatureG n pk)
        (Set.uIcc Y (RiemannScope.tau * Y))) ∧
      (∀ m : ℕ, ContinuousOn (stationAdjustedDiffU c_lam c_half T D0 m)
        (Set.uIcc Y (RiemannScope.tau * Y))) ∧
      (∀ (m : ℕ) (pk : ℕ × ℕ), ContinuousOn (stationFeatureDiffV m pk)
        (Set.uIcc Y (RiemannScope.tau * Y))) ∧
      (∀ u : ℕ, ContinuousOn (oddChainAdjustedProfileUcal c_lam c_half T D0 u)
        (Set.uIcc Y (RiemannScope.tau * Y))) ∧
      (∀ (u : ℕ) (pk : ℕ × ℕ), ContinuousOn (oddChainFeatureVectorVcal u T pk)
        (Set.uIcc Y (RiemannScope.tau * Y))) ∧
      (∀ a : ℕ, ContinuousOn (coreAdjustedProfileA c_lam c_half T D0 a)
        (Set.uIcc Y (RiemannScope.tau * Y))) ∧
      (∀ (a : ℕ) (pk : ℕ × ℕ), ContinuousOn (coreFeatureVectorB a T pk)
        (Set.uIcc Y (RiemannScope.tau * Y))) := by
  obtain ⟨_, hprops⟩ := uIcc_tau_log_props_tc064_aux hY2
  have hlog_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
    ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hprops X hX).1)
  have hphi : ∀ n : ℕ, ContinuousOn (gaussianTermPhi n) (Set.uIcc Y (RiemannScope.tau * Y)) := by
    intro n
    unfold gaussianTermPhi
    have hr : ContinuousOn (fun X : ℝ => X ^ (5 / 2 : ℝ)) (Set.uIcc Y (RiemannScope.tau * Y)) := by
      apply ContinuousOn.rpow_const continuousOn_id
      intro _ _; right; norm_num
    have he : Continuous (fun X : ℝ => (((n : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (n : ℝ) ^ 2))) := by
      continuity
    exact hr.mul he.continuousOn
  have hpsi : ∀ n : ℕ, ContinuousOn (adjustedStationProfilePsi c_lam c_half T D0 n)
      (Set.uIcc Y (RiemannScope.tau * Y)) := by
    intro n
    unfold adjustedStationProfilePsi
    exact (continuousOn_const.sub
      (continuousOn_const.div (hlog_cont.pow 2) (fun X hX => (hprops X hX).2.2.2))).mul (hphi n)
  have hfeat : ∀ (n : ℕ) (pk : ℕ × ℕ), ContinuousOn (stationPrimePowerFeatureG n pk)
      (Set.uIcc Y (RiemannScope.tau * Y)) := by
    intro n pk
    unfold stationPrimePowerFeatureG
    by_cases hd : pk.1 ^ pk.2 ∣ n
    · simp only [hd, ↓reduceIte]
      exact (continuousOn_const.mul (hphi n)).div hlog_cont (fun X hX => (hprops X hX).2.2.1)
    · simp only [hd, ↓reduceIte]
      exact continuousOn_const
  have hU : ∀ m : ℕ, ContinuousOn (stationAdjustedDiffU c_lam c_half T D0 m)
      (Set.uIcc Y (RiemannScope.tau * Y)) :=
    fun m => (hpsi m).sub (hpsi (2 * m))
  have hV : ∀ (m : ℕ) (pk : ℕ × ℕ), ContinuousOn (stationFeatureDiffV m pk)
      (Set.uIcc Y (RiemannScope.tau * Y)) :=
    fun m pk => (hfeat m pk).sub (hfeat (2 * m) pk)
  have hUcal : ∀ u : ℕ, ContinuousOn (oddChainAdjustedProfileUcal c_lam c_half T D0 u)
      (Set.uIcc Y (RiemannScope.tau * Y)) :=
    fun u => continuousOn_finset_sum _ (fun j _ => hU (4 ^ j * u))
  have hVcal : ∀ (u : ℕ) (pk : ℕ × ℕ), ContinuousOn (oddChainFeatureVectorVcal u T pk)
      (Set.uIcc Y (RiemannScope.tau * Y)) :=
    fun u pk => continuousOn_finset_sum _ (fun j _ => hV (4 ^ j * u) pk)
  have hA : ∀ a : ℕ, ContinuousOn (coreAdjustedProfileA c_lam c_half T D0 a)
      (Set.uIcc Y (RiemannScope.tau * Y)) :=
    fun a => continuousOn_finset_sum _ (fun b _ => hUcal (a * b ^ 2))
  have hB : ∀ (a : ℕ) (pk : ℕ × ℕ), ContinuousOn (coreFeatureVectorB a T pk)
      (Set.uIcc Y (RiemannScope.tau * Y)) :=
    fun a pk => continuousOn_finset_sum _ (fun b _ => hVcal (a * b ^ 2) pk)
  exact ⟨hphi, hpsi, hfeat, hU, hV, hUcal, hVcal, hA, hB⟩

private theorem windowPairing_finset_bilinear_tc064_aux {α β : Type*}
    {Y : ℝ} (hY0 : 0 < Y) (S : Finset α) (W : Finset β)
    (f : α → ℝ → ℝ) (g : β → ℝ → ℝ) (w1 : α → ℝ) (w2 : β → ℝ)
    (hf : ∀ i ∈ S, ContinuousOn (f i) (Set.uIcc Y (RiemannScope.tau * Y)))
    (hg : ∀ j ∈ W, ContinuousOn (g j) (Set.uIcc Y (RiemannScope.tau * Y))) :
    windowPairing Y (fun X => ∑ i ∈ S, w1 i * f i X) (fun X => ∑ j ∈ W, w2 j * g j X) =
      ∑ i ∈ S, ∑ j ∈ W, w1 i * w2 j * windowPairing Y (f i) (g j) := by
  have hCg := (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2.1
  have hle : Y ≤ RiemannScope.tau * Y := by nlinarith [hCg]
  have hpos : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), 0 < X := by
    intro X hX; rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX; linarith
  have h_int : ∀ (i : α), i ∈ S → ∀ (j : β), j ∈ W →
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

private theorem complete_kernel_split_tc064_aux {Y : ℝ} (hY2 : 2 ≤ Y)
    (c_lam c_half : ℝ) (T D0 : ℕ) :
    (∀ u ∈ oddChainParts T, ∀ v ∈ (oddChainParts T).erase u,
      oddChainGroupedKernel c_lam c_half T D0 Y u v =
        windowPairing Y (oddChainAdjustedProfileUcal c_lam c_half T D0 u)
            (oddChainAdjustedProfileUcal c_lam c_half T D0 v) -
          4 * ∑ pk ∈ primePowerPairsUpTo T,
            windowPairing Y (fun X => oddChainFeatureVectorVcal u T pk X)
              (fun X => oddChainFeatureVectorVcal v T pk X)) ∧
      differentOddChainSumS c_lam c_half T D0 Y =
        sameCoreSquareRemainderR c_lam c_half T D0 Y +
          distinctSquarefreeCoreSumS c_lam c_half T D0 Y := by
  have hY0 : 0 < Y := by linarith
  obtain ⟨_, _, _, hU_c, hV_c, hUcal_c, hVcal_c, _, _⟩ :=
    continuousOn_station_and_chain_profiles_tc064_aux hY2 c_lam c_half T D0
  have h_tc063_anch := (exact_odd_part_bijection_and_dyadic_chain_offdiag_split_tc063).1.2.2.2 T
  have h_tc063_off := (uniform_same_chain_hilbert_bound_and_closure_transfer_tc063).2.1.2 hY2
    c_lam c_half T D0
  have h_chain_off :
      ∀ u ∈ oddChainParts T, ∀ v ∈ (oddChainParts T).erase u,
        oddChainGroupedKernel c_lam c_half T D0 Y u v =
          windowPairing Y (oddChainAdjustedProfileUcal c_lam c_half T D0 u)
              (oddChainAdjustedProfileUcal c_lam c_half T D0 v) -
            4 * ∑ pk ∈ primePowerPairsUpTo T,
              windowPairing Y (fun X => oddChainFeatureVectorVcal u T pk X)
                (fun X => oddChainFeatureVectorVcal v T pk X) := by
    intro u hu v hv
    have hv_ne_u : v ≠ u := (Finset.mem_erase.mp hv).1
    have hv_in : v ∈ oddChainParts T := Finset.mem_of_mem_erase hv
    have hu_odd : Odd u := (Finset.mem_filter.mp hu).2.1
    have hv_odd : Odd v := (Finset.mem_filter.mp hv_in).2.1
    unfold oddChainGroupedKernel
    have h_each_jk :
        ∀ j ∈ dyadicChainExponents u T, ∀ k ∈ dyadicChainExponents v T,
          anchorFourTermDiffHcal c_lam c_half T D0 Y (4 ^ j * u) (4 ^ k * v) =
            windowPairing Y (stationAdjustedDiffU c_lam c_half T D0 (4 ^ j * u))
                (stationAdjustedDiffU c_lam c_half T D0 (4 ^ k * v)) -
              4 * ∑ pk ∈ primePowerPairsUpTo T,
                windowPairing Y (fun X => stationFeatureDiffV (4 ^ j * u) pk X)
                  (fun X => stationFeatureDiffV (4 ^ k * v) pk X) := by
      intro j hj k hk
      have hmj : 4 ^ j * u ∈ primeInteriorTruncatedAnchors 2 T := h_tc063_anch.1 u hu j hj
      have hmk : 4 ^ k * v ∈ primeInteriorTruncatedAnchors 2 T := h_tc063_anch.1 v hv_in k hk
      have hne : 4 ^ k * v ≠ 4 ^ j * u := by
        intro h_eq
        have hf1 := two_pow_mul_odd_factorization_two_tc064_aux (2 * k) hv_odd
        have hf2 := two_pow_mul_odd_factorization_two_tc064_aux (2 * j) hu_odd
        have h4k : (4 : ℕ) ^ k = 2 ^ (2 * k) := by
          rw [show (4 : ℕ) = 2 ^ 2 by norm_num, ← pow_mul]
        have h4j : (4 : ℕ) ^ j = 2 ^ (2 * j) := by
          rw [show (4 : ℕ) = 2 ^ 2 by norm_num, ← pow_mul]
        rw [← h4k] at hf1
        rw [← h4j] at hf2
        have h2kj : 2 * k = 2 * j := by rw [← hf1, h_eq, hf2]
        have hkj : k = j := by omega
        subst hkj
        exact hv_ne_u (Nat.eq_of_mul_eq_mul_left (pow_pos (by decide) k) h_eq)
      exact h_tc063_off (4 ^ j * u) hmj (4 ^ k * v) (Finset.mem_erase.mpr ⟨hne, hmk⟩)
    have h_congr1 :
        (∑ j ∈ dyadicChainExponents u T, ∑ k ∈ dyadicChainExponents v T,
            anchorFourTermDiffHcal c_lam c_half T D0 Y (4 ^ j * u) (4 ^ k * v)) =
          (∑ j ∈ dyadicChainExponents u T, ∑ k ∈ dyadicChainExponents v T,
              windowPairing Y (stationAdjustedDiffU c_lam c_half T D0 (4 ^ j * u))
                (stationAdjustedDiffU c_lam c_half T D0 (4 ^ k * v))) -
            4 * ∑ pk ∈ primePowerPairsUpTo T,
              ∑ j ∈ dyadicChainExponents u T, ∑ k ∈ dyadicChainExponents v T,
                windowPairing Y (fun X => stationFeatureDiffV (4 ^ j * u) pk X)
                  (fun X => stationFeatureDiffV (4 ^ k * v) pk X) := by
      have h1 :
          (∑ j ∈ dyadicChainExponents u T, ∑ k ∈ dyadicChainExponents v T,
              anchorFourTermDiffHcal c_lam c_half T D0 Y (4 ^ j * u) (4 ^ k * v)) =
            (∑ j ∈ dyadicChainExponents u T, ∑ k ∈ dyadicChainExponents v T,
                windowPairing Y (stationAdjustedDiffU c_lam c_half T D0 (4 ^ j * u))
                  (stationAdjustedDiffU c_lam c_half T D0 (4 ^ k * v))) -
              4 * (∑ j ∈ dyadicChainExponents u T, ∑ k ∈ dyadicChainExponents v T,
                ∑ pk ∈ primePowerPairsUpTo T,
                  windowPairing Y (fun X => stationFeatureDiffV (4 ^ j * u) pk X)
                    (fun X => stationFeatureDiffV (4 ^ k * v) pk X)) := by
        calc
          _ = ∑ j ∈ dyadicChainExponents u T, ∑ k ∈ dyadicChainExponents v T,
                (windowPairing Y (stationAdjustedDiffU c_lam c_half T D0 (4 ^ j * u))
                    (stationAdjustedDiffU c_lam c_half T D0 (4 ^ k * v)) -
                  4 * ∑ pk ∈ primePowerPairsUpTo T,
                    windowPairing Y (fun X => stationFeatureDiffV (4 ^ j * u) pk X)
                      (fun X => stationFeatureDiffV (4 ^ k * v) pk X)) :=
              Finset.sum_congr rfl (fun j hj => Finset.sum_congr rfl (fun k hk => h_each_jk j hj k hk))
          _ = _ := by
              simp_rw [Finset.sum_sub_distrib, ← Finset.mul_sum]
      rw [h1]
      congr 2
      trans (∑ j ∈ dyadicChainExponents u T, ∑ pk ∈ primePowerPairsUpTo T,
        ∑ k ∈ dyadicChainExponents v T,
          windowPairing Y (fun X => stationFeatureDiffV (4 ^ j * u) pk X)
            (fun X => stationFeatureDiffV (4 ^ k * v) pk X))
      · exact Finset.sum_congr rfl (fun _ _ => Finset.sum_comm)
      · exact Finset.sum_comm
    rw [h_congr1]
    have hU_bilin :=
      windowPairing_finset_bilinear_tc064_aux hY0 (dyadicChainExponents u T)
        (dyadicChainExponents v T)
        (fun j => stationAdjustedDiffU c_lam c_half T D0 (4 ^ j * u))
        (fun k => stationAdjustedDiffU c_lam c_half T D0 (4 ^ k * v))
        (fun _ => 1) (fun _ => 1)
        (fun j _ => hU_c (4 ^ j * u)) (fun k _ => hU_c (4 ^ k * v))
    simp only [one_mul] at hU_bilin
    unfold oddChainAdjustedProfileUcal oddChainFeatureVectorVcal
    rw [← hU_bilin]
    congr 2
    apply Finset.sum_congr rfl
    intro pk _
    have hV_bilin :=
      windowPairing_finset_bilinear_tc064_aux hY0 (dyadicChainExponents u T)
        (dyadicChainExponents v T)
        (fun j => stationFeatureDiffV (4 ^ j * u) pk)
        (fun k => stationFeatureDiffV (4 ^ k * v) pk)
        (fun _ => 1) (fun _ => 1)
        (fun j _ => hV_c (4 ^ j * u) pk) (fun k _ => hV_c (4 ^ k * v) pk)
    simp only [one_mul] at hV_bilin
    exact hV_bilin.symm
  refine ⟨h_chain_off, ?_⟩
  let G_ch : ℕ → ℕ → ℝ := fun u v =>
    windowPairing Y (oddChainAdjustedProfileUcal c_lam c_half T D0 u)
        (oddChainAdjustedProfileUcal c_lam c_half T D0 v) -
      4 * ∑ pk ∈ primePowerPairsUpTo T,
        windowPairing Y (fun X => oddChainFeatureVectorVcal u T pk X)
          (fun X => oddChainFeatureVectorVcal v T pk X)
  have h_Mcal_eq :
      ∀ a c : ℕ,
        completeCorePairKernelMcal c_lam c_half T D0 Y a c =
          ∑ b ∈ coreSquareMultipliers a T, ∑ d ∈ coreSquareMultipliers c T,
            G_ch (a * b ^ 2) (c * d ^ 2) := by
    intro a c
    unfold completeCorePairKernelMcal coreAdjustedProfileA coreFeatureVectorB
    have hA_bilin :=
      windowPairing_finset_bilinear_tc064_aux hY0 (coreSquareMultipliers a T)
        (coreSquareMultipliers c T)
        (fun b => oddChainAdjustedProfileUcal c_lam c_half T D0 (a * b ^ 2))
        (fun d => oddChainAdjustedProfileUcal c_lam c_half T D0 (c * d ^ 2))
        (fun _ => 1) (fun _ => 1)
        (fun b _ => hUcal_c (a * b ^ 2)) (fun d _ => hUcal_c (c * d ^ 2))
    simp only [one_mul] at hA_bilin
    have hB_each :
        ∀ pk ∈ primePowerPairsUpTo T,
          windowPairing Y
              (fun X => ∑ b ∈ coreSquareMultipliers a T, oddChainFeatureVectorVcal (a * b ^ 2) T pk X)
              (fun X => ∑ d ∈ coreSquareMultipliers c T, oddChainFeatureVectorVcal (c * d ^ 2) T pk X) =
            ∑ b ∈ coreSquareMultipliers a T, ∑ d ∈ coreSquareMultipliers c T,
              windowPairing Y (oddChainFeatureVectorVcal (a * b ^ 2) T pk)
                (oddChainFeatureVectorVcal (c * d ^ 2) T pk) := by
      intro pk _
      have hb :=
        windowPairing_finset_bilinear_tc064_aux hY0 (coreSquareMultipliers a T)
          (coreSquareMultipliers c T)
          (fun b => oddChainFeatureVectorVcal (a * b ^ 2) T pk)
          (fun d => oddChainFeatureVectorVcal (c * d ^ 2) T pk)
          (fun _ => 1) (fun _ => 1)
          (fun b _ => hVcal_c (a * b ^ 2) pk) (fun d _ => hVcal_c (c * d ^ 2) pk)
      simpa only [one_mul] using hb
    rw [hA_bilin, Finset.sum_congr rfl hB_each]
    have h_comm :
        (∑ pk ∈ primePowerPairsUpTo T,
            ∑ b ∈ coreSquareMultipliers a T, ∑ d ∈ coreSquareMultipliers c T,
              windowPairing Y (oddChainFeatureVectorVcal (a * b ^ 2) T pk)
                (oddChainFeatureVectorVcal (c * d ^ 2) T pk)) =
          ∑ b ∈ coreSquareMultipliers a T, ∑ d ∈ coreSquareMultipliers c T,
            ∑ pk ∈ primePowerPairsUpTo T,
              windowPairing Y (oddChainFeatureVectorVcal (a * b ^ 2) T pk)
                (oddChainFeatureVectorVcal (c * d ^ 2) T pk) := by
      trans (∑ b ∈ coreSquareMultipliers a T, ∑ pk ∈ primePowerPairsUpTo T,
        ∑ d ∈ coreSquareMultipliers c T,
          windowPairing Y (oddChainFeatureVectorVcal (a * b ^ 2) T pk)
            (oddChainFeatureVectorVcal (c * d ^ 2) T pk))
      · exact Finset.sum_comm
      · exact Finset.sum_congr rfl (fun _ _ => Finset.sum_comm)
    rw [h_comm]
    dsimp [G_ch]
    simp_rw [Finset.sum_sub_distrib, ← Finset.mul_sum]
  obtain ⟨_, _, _, _, _, h_bi⟩ := oddSquarefreeCores_bijection_and_edges_tc064_aux T
  have h_sum_odd :
      ∀ (φ : ℕ → ℝ),
        (∑ u ∈ oddChainParts T, φ u) =
          ∑ a ∈ oddSquarefreeCores T, ∑ b ∈ coreSquareMultipliers a T, φ (a * b ^ 2) := by
    intro φ
    rw [← h_bi, Finset.sum_biUnion]
    · apply Finset.sum_congr rfl
      intro a ha
      have ha_o : Odd a := (Finset.mem_filter.mp ha).2.1
      have ha_sf : Squarefree a := (Finset.mem_filter.mp ha).2.2.1
      rw [Finset.sum_image]
      intro b1 hb1 b2 hb2 h_eq
      have hb1_o : Odd b1 := (Finset.mem_filter.mp hb1).2.1
      have hb2_o : Odd b2 := (Finset.mem_filter.mp hb2).2.1
      exact (paired_station_injective_and_mem_tc064_aux.1
        (j1 := 0) (eps1 := 0) (j2 := 0) (eps2 := 0)
        ha_o ha_sf hb1_o (by decide) ha_o ha_sf hb2_o (by decide)).mp (by simpa using h_eq) |>.2.1
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
      exact hne ((paired_station_injective_and_mem_tc064_aux.1
        (j1 := 0) (eps1 := 0) (j2 := 0) (eps2 := 0)
        ha2_o ha2_sf hb2_o (by decide) ha1_o ha1_sf hb1_o (by decide)).mp
          (by simpa using h_eq)).1.symm
  have h_diff_G :
      differentOddChainSumS c_lam c_half T D0 Y =
        (∑ u ∈ oddChainParts T, ∑ v ∈ oddChainParts T,
            (liouvilleLambda u : ℝ) * (liouvilleLambda v : ℝ) * G_ch u v) -
          ∑ u ∈ oddChainParts T, G_ch u u := by
    unfold differentOddChainSumS
    have h_each_u :
        ∀ u ∈ oddChainParts T,
          (∑ v ∈ (oddChainParts T).erase u,
              (liouvilleLambda u : ℝ) * (liouvilleLambda v : ℝ) *
                oddChainGroupedKernel c_lam c_half T D0 Y u v) =
            (∑ v ∈ oddChainParts T,
                (liouvilleLambda u : ℝ) * (liouvilleLambda v : ℝ) * G_ch u v) -
              G_ch u u := by
      intro u hu
      have hu1 : 1 ≤ u := (Finset.mem_Icc.mp (Finset.mem_filter.mp hu).1).1
      have hu_ne : u ≠ 0 := by omega
      have h_lam_sq : (liouvilleLambda u : ℝ) * (liouvilleLambda u : ℝ) = 1 := by
        have hi : liouvilleLambda u * liouvilleLambda u = 1 := by
          simp only [liouvilleLambda, hu_ne, ↓reduceIte, liouvilleSignFromOmega]
          rw [← pow_add, show natOmega u + natOmega u = 2 * natOmega u by omega, pow_mul]
          norm_num
        exact_mod_cast hi
      have h_er :
          (∑ v ∈ (oddChainParts T).erase u,
              (liouvilleLambda u : ℝ) * (liouvilleLambda v : ℝ) *
                oddChainGroupedKernel c_lam c_half T D0 Y u v) =
            ∑ v ∈ (oddChainParts T).erase u,
              (liouvilleLambda u : ℝ) * (liouvilleLambda v : ℝ) * G_ch u v := by
        apply Finset.sum_congr rfl
        intro v hv
        rw [h_chain_off u hu v hv]
      rw [h_er, ← Finset.add_sum_erase (oddChainParts T)
        (fun v => (liouvilleLambda u : ℝ) * (liouvilleLambda v : ℝ) * G_ch u v) hu,
        h_lam_sq, one_mul]
      ring
    rw [Finset.sum_congr rfl h_each_u, Finset.sum_sub_distrib]
  have h_double_reidx :
      (∑ u ∈ oddChainParts T, ∑ v ∈ oddChainParts T,
          (liouvilleLambda u : ℝ) * (liouvilleLambda v : ℝ) * G_ch u v) =
        (∑ a ∈ oddSquarefreeCores T, completeCorePairKernelMcal c_lam c_half T D0 Y a a) +
          distinctSquarefreeCoreSumS c_lam c_half T D0 Y := by
    rw [h_sum_odd (fun u => ∑ v ∈ oddChainParts T,
      (liouvilleLambda u : ℝ) * (liouvilleLambda v : ℝ) * G_ch u v)]
    have h_in :
        ∀ a ∈ oddSquarefreeCores T,
          (∑ b ∈ coreSquareMultipliers a T, ∑ v ∈ oddChainParts T,
              (liouvilleLambda (a * b ^ 2) : ℝ) * (liouvilleLambda v : ℝ) *
                G_ch (a * b ^ 2) v) =
            ∑ c ∈ oddSquarefreeCores T,
              (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                completeCorePairKernelMcal c_lam c_half T D0 Y a c := by
      intro a ha
      have ha_sf : Squarefree a := (Finset.mem_filter.mp ha).2.2.1
      have h_each_b :
          ∀ b ∈ coreSquareMultipliers a T,
            (∑ v ∈ oddChainParts T,
                (liouvilleLambda (a * b ^ 2) : ℝ) * (liouvilleLambda v : ℝ) *
                  G_ch (a * b ^ 2) v) =
              ∑ c ∈ oddSquarefreeCores T, ∑ d ∈ coreSquareMultipliers c T,
                (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                  G_ch (a * b ^ 2) (c * d ^ 2) := by
        intro b hb
        have hb1 : 1 ≤ b := (Finset.mem_Icc.mp (Finset.mem_filter.mp hb).1).1
        have hlam_ab := (liouvilleLambda_squarefree_mul_sq_eq_moebius_tc064_aux ha_sf hb1).1
        rw [h_sum_odd]
        apply Finset.sum_congr rfl
        intro c hc
        have hc_sf : Squarefree c := (Finset.mem_filter.mp hc).2.2.1
        apply Finset.sum_congr rfl
        intro d hd
        have hd1 : 1 ≤ d := (Finset.mem_Icc.mp (Finset.mem_filter.mp hd).1).1
        have hlam_cd := (liouvilleLambda_squarefree_mul_sq_eq_moebius_tc064_aux hc_sf hd1).1
        rw [hlam_ab, hlam_cd]
      rw [Finset.sum_congr rfl h_each_b, Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro c _
      rw [h_Mcal_eq a c, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro b _
      rw [Finset.mul_sum]
    rw [Finset.sum_congr rfl h_in]
    have h_split_c :
        ∀ a ∈ oddSquarefreeCores T,
          (∑ c ∈ oddSquarefreeCores T,
              (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                completeCorePairKernelMcal c_lam c_half T D0 Y a c) =
            completeCorePairKernelMcal c_lam c_half T D0 Y a a +
              ∑ c ∈ (oddSquarefreeCores T).erase a,
                (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                  completeCorePairKernelMcal c_lam c_half T D0 Y a c := by
      intro a ha
      have ha_sf : Squarefree a := (Finset.mem_filter.mp ha).2.2.1
      have h_mu_sq := (liouvilleLambda_squarefree_mul_sq_eq_moebius_tc064_aux ha_sf (le_refl 1)).2
      rw [← Finset.add_sum_erase _ _ ha, ← sq, h_mu_sq, one_mul]
    rw [Finset.sum_congr rfl h_split_c, Finset.sum_add_distrib]
    rfl
  rw [h_diff_G, h_double_reidx]
  unfold sameCoreSquareRemainderR windowEnergyNormSq
  dsimp [G_ch]
  ring

/-- **Theorem 1 (`TASK-TC-064` §2, Unique Odd Squarefree-Core Representation, Edge Cases, Paired-Station Multiplicity-One Injectivity, and Complete-Kernel `R_square + S_core` Split)**:
    1. *Unique odd representation & Liouville-to-Möbius reduction*:
       - `∀ u : ℕ, Odd u → ∃! ab : ℕ × ℕ, Odd ab.1 ∧ Squarefree ab.1 ∧ Odd ab.2 ∧ ab.1 * ab.2 ^ 2 = u`;
       - `∀ {a b : ℕ}, Squarefree a → 1 ≤ b → liouvilleLambda (a * b ^ 2) = ArithmeticFunction.moebius a ∧ (ArithmeticFunction.moebius a : ℝ) ^ 2 = 1`;
    2. *Finite index-set & edge characterizations and multiplicity-one paired-station injectivity*:
       - `oddSquarefreeCores T = ∅ ↔ T < 2`, `∀ a ∈ oddSquarefreeCores T, 1 ∈ coreSquareMultipliers a T`, and `(coreSquareMultipliers a T).card = 1 ↔ T < 18 * a`;
       - Exact `(a, b) ↦ a * b ^ 2` bijection and `biUnion` onto `oddChainParts T`;
       - Global injectivity of `(a, b, j, eps) ↦ 2 ^ (2 * j + eps) * a * b ^ 2` (`eps < 2`) and landing inside `{k ∈ Icc 1 T : ∃ r b', Odd b' ∧ k = 2 ^ r * a * b' ^ 2}`;
    3. *Complete-kernel chain Gram identity & exact `R_square + S_core` split (`2 ≤ Y`)*:
       - On distinct `u ≠ v` in `oddChainParts T`, `oddChainGroupedKernel = <Ucal_u, Ucal_v>_Y - 4 * ∑_{pk} <Vcal_{u,pk}, Vcal_{v,pk}>_Y`;
       - `differentOddChainSumS c_lam c_half T D0 Y = sameCoreSquareRemainderR c_lam c_half T D0 Y + distinctSquarefreeCoreSumS c_lam c_half T D0 Y`,
         and canonically `canonicalDifferentOddChainSumS c_lam c_half Y = canonicalSameCoreSquareRemainderR c_lam c_half Y + canonicalDistinctSquarefreeCoreSumS c_lam c_half Y`. -/
theorem exact_odd_squarefree_core_bijection_and_complete_kernel_split_tc064 :
    ((∀ u : ℕ, Odd u →
        ∃! ab : ℕ × ℕ, Odd ab.1 ∧ Squarefree ab.1 ∧ Odd ab.2 ∧ ab.1 * ab.2 ^ 2 = u) ∧
      (∀ {a b : ℕ}, Squarefree a → 1 ≤ b →
        liouvilleLambda (a * b ^ 2) = ArithmeticFunction.moebius a ∧
          (ArithmeticFunction.moebius a : ℝ) ^ 2 = 1)) ∧
    ((∀ T : ℕ,
        (oddSquarefreeCores T = ∅ ↔ T < 2) ∧
          (∀ a ∈ oddSquarefreeCores T, 1 ∈ coreSquareMultipliers a T) ∧
          (∀ a ∈ oddSquarefreeCores T, (coreSquareMultipliers a T).card = 1 ↔ T < 18 * a)) ∧
      (∀ T : ℕ,
        (∀ a ∈ oddSquarefreeCores T, ∀ b ∈ coreSquareMultipliers a T,
          a * b ^ 2 ∈ oddChainParts T) ∧
          (∀ u ∈ oddChainParts T,
            ∃! ab : ℕ × ℕ,
              ab.1 ∈ oddSquarefreeCores T ∧ ab.2 ∈ coreSquareMultipliers ab.1 T ∧
                ab.1 * ab.2 ^ 2 = u) ∧
          (oddSquarefreeCores T).biUnion
            (fun a => (coreSquareMultipliers a T).image (fun b => a * b ^ 2)) =
              oddChainParts T) ∧
      (∀ {a1 b1 j1 eps1 a2 b2 j2 eps2 : ℕ},
        Odd a1 → Squarefree a1 → Odd b1 → eps1 < 2 →
        Odd a2 → Squarefree a2 → Odd b2 → eps2 < 2 →
          (2 ^ (2 * j1 + eps1) * a1 * b1 ^ 2 = 2 ^ (2 * j2 + eps2) * a2 * b2 ^ 2 ↔
            a1 = a2 ∧ b1 = b2 ∧ j1 = j2 ∧ eps1 = eps2)) ∧
      (∀ T : ℕ, ∀ a ∈ oddSquarefreeCores T, ∀ b ∈ coreSquareMultipliers a T,
        ∀ j ∈ dyadicChainExponents (a * b ^ 2) T, ∀ {eps : ℕ}, eps < 2 →
          2 ^ (2 * j + eps) * a * b ^ 2 ∈
            (Finset.Icc 1 T).filter (fun k => ∃ r b' : ℕ, Odd b' ∧ k = 2 ^ r * a * b' ^ 2))) ∧
    (∀ {Y : ℝ}, 2 ≤ Y →
      (∀ (c_lam c_half : ℝ) (T D0 : ℕ),
        ∀ u ∈ oddChainParts T, ∀ v ∈ (oddChainParts T).erase u,
          oddChainGroupedKernel c_lam c_half T D0 Y u v =
            windowPairing Y (oddChainAdjustedProfileUcal c_lam c_half T D0 u)
                (oddChainAdjustedProfileUcal c_lam c_half T D0 v) -
              4 * ∑ pk ∈ primePowerPairsUpTo T,
                windowPairing Y (fun X => oddChainFeatureVectorVcal u T pk X)
                  (fun X => oddChainFeatureVectorVcal v T pk X)) ∧
      (∀ (c_lam c_half : ℝ) (T D0 : ℕ),
        differentOddChainSumS c_lam c_half T D0 Y =
          sameCoreSquareRemainderR c_lam c_half T D0 Y +
            distinctSquarefreeCoreSumS c_lam c_half T D0 Y) ∧
      (∀ (c_lam c_half : ℝ),
        canonicalDifferentOddChainSumS c_lam c_half Y =
          canonicalSameCoreSquareRemainderR c_lam c_half Y +
            canonicalDistinctSquarefreeCoreSumS c_lam c_half Y)) := by
  refine ⟨⟨fun _ hu => unique_odd_squarefree_mul_sq_tc064_aux hu,
      fun ha hb => liouvilleLambda_squarefree_mul_sq_eq_moebius_tc064_aux ha hb⟩,
    ⟨fun T => ⟨(oddSquarefreeCores_bijection_and_edges_tc064_aux T).1,
        (oddSquarefreeCores_bijection_and_edges_tc064_aux T).2.1,
        (oddSquarefreeCores_bijection_and_edges_tc064_aux T).2.2.1⟩,
      fun T => (oddSquarefreeCores_bijection_and_edges_tc064_aux T).2.2.2,
      paired_station_injective_and_mem_tc064_aux.1,
      paired_station_injective_and_mem_tc064_aux.2⟩,
    ?_⟩
  intro Y hY2
  refine ⟨fun c_lam c_half T D0 => (complete_kernel_split_tc064_aux hY2 c_lam c_half T D0).1,
    fun c_lam c_half T D0 => (complete_kernel_split_tc064_aux hY2 c_lam c_half T D0).2,
    fun c_lam c_half => (complete_kernel_split_tc064_aux hY2 c_lam c_half
      (canonicalCutoffT Y) (Nat.floor (Real.log Y))).2⟩

/-! ### Section 2: Divisor-Core Star Involution & Support Bijection (`TASK-TC-064` §3.1) -/

private theorem squarefreeCoreStar_props_tc064_aux
    {a c : ℕ} (ha_o : Odd a) (ha_sf : Squarefree a) (hc_o : Odd c) (hc_sf : Squarefree c) :
    (Odd (squarefreeCoreStar a c) ∧ Squarefree (squarefreeCoreStar a c) ∧
        1 ≤ squarefreeCoreStar a c) ∧
      squarefreeCoreStar (squarefreeCoreStar a c) c = a ∧
      c * squarefreeCoreStar a c = a * (c / Nat.gcd a c) ^ 2 := by
  let g := Nat.gcd a c
  let a1 := a / g
  let c1 := c / g
  have hg_pos : 0 < g := Nat.gcd_pos_of_pos_left c ha_o.pos
  have hga1 : g * a1 = a := Nat.mul_div_cancel' (Nat.gcd_dvd_left a c)
  have hgc1 : g * c1 = c := Nat.mul_div_cancel' (Nat.gcd_dvd_right a c)
  have ha1c1_cop : Nat.Coprime a1 c1 := Nat.coprime_div_gcd_div_gcd hg_pos
  have ha_parts := squarefree_pos_and_coprime_of_mul_tc064_aux.2 (hga1.symm ▸ ha_sf)
  have hc_parts := squarefree_pos_and_coprime_of_mul_tc064_aux.2 (hgc1.symm ▸ hc_sf)
  have ha1_o : Odd a1 := (odd_of_odd_mul_tc064_aux (hga1.symm ▸ ha_o)).2
  have hc1_o : Odd c1 := (odd_of_odd_mul_tc064_aux (hgc1.symm ▸ hc_o)).2
  have h_star_eq : squarefreeCoreStar a c = a1 * c1 := by
    unfold squarefreeCoreStar
    change (a * c) / g ^ 2 = a1 * c1
    have h_prod : a * c = (a1 * c1) * g ^ 2 := by
      calc
        a * c = (g * a1) * (g * c1) := by rw [hga1, hgc1]
        _ = (a1 * c1) * g ^ 2 := by ring
    rw [h_prod, Nat.mul_div_cancel _ (pow_pos hg_pos 2)]
  have h_star_o : Odd (a1 * c1) := ha1_o.mul hc1_o
  have h_star_sf : Squarefree (a1 * c1) :=
    (Nat.squarefree_mul ha1c1_cop).mpr ⟨ha_parts.2.1, hc_parts.2.1⟩
  have h_inv : squarefreeCoreStar (a1 * c1) c = a := by
    unfold squarefreeCoreStar
    have h_gcd : Nat.gcd (a1 * c1) c = c1 := by
      rw [← hgc1, Nat.gcd_mul_right, ha_parts.2.2.symm.gcd_eq_one, one_mul]
    rw [h_gcd]
    have h_prod2 : (a1 * c1) * c = a * c1 ^ 2 := by
      calc
        (a1 * c1) * c = (a1 * c1) * (g * c1) := by rw [hgc1]
        _ = (g * a1) * c1 ^ 2 := by ring
        _ = a * c1 ^ 2 := by rw [hga1]
    rw [h_prod2, Nat.mul_div_cancel _ (pow_pos hc1_o.pos 2)]
  have h_id : c * (a1 * c1) = a * c1 ^ 2 := by
    calc
      c * (a1 * c1) = (g * c1) * (a1 * c1) := by rw [hgc1]
      _ = (g * a1) * c1 ^ 2 := by ring
      _ = a * c1 ^ 2 := by rw [hga1]
  rw [h_star_eq]
  exact ⟨⟨h_star_o, h_star_sf, h_star_o.pos⟩, h_inv, h_id⟩

private theorem dvd_of_sq_dvd_squarefree_mul_sq_tc064_aux
    {f m b : ℕ} (hm_sf : Squarefree m) (hb_ne : b ≠ 0) (hdvd : f ^ 2 ∣ m * b ^ 2) :
    f ∣ b := by
  have hm_ne : m ≠ 0 := hm_sf.ne_zero
  have hmb_ne : m * b ^ 2 ≠ 0 := mul_ne_zero hm_ne (pow_ne_zero 2 hb_ne)
  have hf2_ne : f ^ 2 ≠ 0 := fun h0 => hmb_ne (eq_zero_of_zero_dvd (h0 ▸ hdvd))
  have hf_ne : f ≠ 0 := fun h0 => hf2_ne (by simp [h0])
  rw [← Nat.factorization_le_iff_dvd hf_ne hb_ne]
  intro p
  have hfp := (Nat.factorization_le_iff_dvd hf2_ne hmb_ne).mpr hdvd p
  rw [Nat.factorization_pow, Nat.factorization_mul hm_ne (pow_ne_zero 2 hb_ne),
    Finsupp.add_apply, Nat.factorization_pow, Finsupp.smul_apply, Finsupp.smul_apply,
    smul_eq_mul, smul_eq_mul] at hfp
  have hm_le1 := (Nat.squarefree_iff_factorization_le_one hm_ne).mp hm_sf p
  omega

private theorem divisor_core_support_bijection_tc064_aux
    {e s c f a n : ℕ} (he : e = 2 ^ s * c * f ^ 2)
    (hc_o : Odd c) (hc_sf : Squarefree c) (hf_o : Odd f)
    (ha_o : Odd a) (ha_sf : Squarefree a) (hn1 : 1 ≤ n) :
    ((∃ r b : ℕ, Odd b ∧ n = 2 ^ r * a * b ^ 2) ∧ e ∣ n) ↔
      ∃! ql : ℕ × ℕ, Odd ql.2 ∧ 2 ^ ql.1 * e * squarefreeCoreStar a c * ql.2 ^ 2 = n := by
  obtain ⟨⟨hstar_o, hstar_sf, _⟩, _, h_c_star⟩ :=
    squarefreeCoreStar_props_tc064_aux ha_o ha_sf hc_o hc_sf
  have he_pos : 0 < e := by
    rw [he]
    exact Nat.mul_pos (Nat.mul_pos (pow_pos (by decide) s) hc_o.pos) (pow_pos hf_o.pos 2)
  have h_uniq_ql :
      ∀ {q1 l1 q2 l2 : ℕ}, Odd l1 → Odd l2 →
        2 ^ q1 * e * squarefreeCoreStar a c * l1 ^ 2 =
          2 ^ q2 * e * squarefreeCoreStar a c * l2 ^ 2 →
        q1 = q2 ∧ l1 = l2 := by
    intro q1 l1 q2 l2 hl1 hl2 h_eq
    let u1 := c * f ^ 2 * squarefreeCoreStar a c * l1 ^ 2
    let u2 := c * f ^ 2 * squarefreeCoreStar a c * l2 ^ 2
    have hu1_o : Odd u1 := ((hc_o.mul (hf_o.pow)).mul hstar_o).mul (hl1.pow)
    have hu2_o : Odd u2 := ((hc_o.mul (hf_o.pow)).mul hstar_o).mul (hl2.pow)
    have h_rewrite :
        2 ^ (q1 + s) * u1 = 2 ^ (q2 + s) * u2 := by
      dsimp [u1, u2]
      rw [he] at h_eq
      linarith [show 2 ^ (q1 + s) * (c * f ^ 2 * squarefreeCoreStar a c * l1 ^ 2) =
          2 ^ q1 * (2 ^ s * c * f ^ 2) * squarefreeCoreStar a c * l1 ^ 2 by rw [pow_add]; ring,
        show 2 ^ (q2 + s) * (c * f ^ 2 * squarefreeCoreStar a c * l2 ^ 2) =
          2 ^ q2 * (2 ^ s * c * f ^ 2) * squarefreeCoreStar a c * l2 ^ 2 by rw [pow_add]; ring]
    have hf1 := two_pow_mul_odd_factorization_two_tc064_aux (q1 + s) hu1_o
    have hf2 := two_pow_mul_odd_factorization_two_tc064_aux (q2 + s) hu2_o
    have hqs : q1 + s = q2 + s := by rw [← hf1, h_rewrite, hf2]
    have hq_eq : q1 = q2 := by omega
    subst hq_eq
    have h_pos_fac : 0 < 2 ^ q1 * e * squarefreeCoreStar a c :=
      Nat.mul_pos (Nat.mul_pos (pow_pos (by decide) q1) he_pos) hstar_o.pos
    have hl_sq_eq : l1 ^ 2 = l2 ^ 2 := Nat.eq_of_mul_eq_mul_left h_pos_fac h_eq
    have hl_eq : l1 = l2 := by
      have hs1 : Nat.sqrt (l1 ^ 2) = l1 := by rw [sq, Nat.sqrt_eq]
      have hs2 : Nat.sqrt (l2 ^ 2) = l2 := by rw [sq, Nat.sqrt_eq]
      rw [← hs1, ← hs2, hl_sq_eq]
    exact ⟨rfl, hl_eq⟩
  constructor
  · rintro ⟨⟨r, b, hb_o, hn_eq⟩, he_dvd⟩
    let g := Nat.gcd a c
    let a1 := a / g
    let c1 := c / g
    have hg_pos : 0 < g := Nat.gcd_pos_of_pos_left c ha_o.pos
    have hga1 : g * a1 = a := Nat.mul_div_cancel' (Nat.gcd_dvd_left a c)
    have hgc1 : g * c1 = c := Nat.mul_div_cancel' (Nat.gcd_dvd_right a c)
    have ha1c1_cop : Nat.Coprime a1 c1 := Nat.coprime_div_gcd_div_gcd hg_pos
    have hc1_sf : Squarefree c1 :=
      (squarefree_pos_and_coprime_of_mul_tc064_aux.2 (hgc1.symm ▸ hc_sf)).2.1
    have h_star_a1c1 : squarefreeCoreStar a c = a1 * c1 := by
      unfold squarefreeCoreStar
      have hp : a * c = (a1 * c1) * g ^ 2 := by
        calc a * c = (g * a1) * (g * c1) := by rw [hga1, hgc1]
          _ = (a1 * c1) * g ^ 2 := by ring
      rw [hp, Nat.mul_div_cancel _ (pow_pos hg_pos 2)]
    have hn_ne : n ≠ 0 := by omega
    have hv2_le : s ≤ r := by
      have hf_le := (Nat.factorization_le_iff_dvd (ne_of_gt he_pos) hn_ne).mpr he_dvd 2
      have h_e2 : e.factorization 2 = s := by
        rw [he, show 2 ^ s * c * f ^ 2 = 2 ^ s * (c * f ^ 2) by ring]
        exact two_pow_mul_odd_factorization_two_tc064_aux s (hc_o.mul (hf_o.pow))
      have h_n2 : n.factorization 2 = r := by
        rw [hn_eq, show 2 ^ r * a * b ^ 2 = 2 ^ r * (a * b ^ 2) by ring]
        exact two_pow_mul_odd_factorization_two_tc064_aux r (ha_o.mul (hb_o.pow))
      omega
    let q := r - s
    have hr_qs : r = q + s := by omega
    have h_odd_dvd : c * f ^ 2 ∣ a * b ^ 2 := by
      have h2_cop : Nat.Coprime (c * f ^ 2) (2 ^ r) := by
        apply Nat.Coprime.pow_right
        rw [Nat.Coprime, Nat.gcd_comm]
        apply Nat.Prime.coprime_iff_not_dvd Nat.prime_two |>.mpr
        exact fun h2 => (Nat.odd_iff_not_even.mp (hc_o.mul (hf_o.pow))) (even_iff_two_dvd.mpr h2)
      have hd1 : c * f ^ 2 ∣ 2 ^ r * (a * b ^ 2) := by
        have hd0 : c * f ^ 2 ∣ e := by rw [he]; exact ⟨2 ^ s, by ring⟩
        have hd_n := dvd_trans hd0 he_dvd
        rwa [hn_eq, show 2 ^ r * a * b ^ 2 = 2 ^ r * (a * b ^ 2) by ring] at hd_n
      exact h2_cop.dvd_of_dvd_mul_left hd1
    have hc1_f2_dvd : c1 * f ^ 2 ∣ a1 * b ^ 2 := by
      rw [← hgc1, ← hga1, mul_assoc g c1, mul_assoc g a1] at h_odd_dvd
      exact (Nat.mul_dvd_mul_iff_left hg_pos).mp h_odd_dvd
    have hc1_dvd_b2 : c1 ∣ b ^ 2 := by
      have hc1_dvd_ab2 : c1 ∣ a1 * b ^ 2 := dvd_trans (dvd_mul_right c1 (f ^ 2)) hc1_f2_dvd
      exact ha1c1_cop.symm.dvd_of_dvd_mul_left hc1_dvd_ab2
    have hc1_dvd_b : c1 ∣ b := by
      have hc1_sq_dvd : c1 ^ 2 ∣ c1 * b ^ 2 := by
        rw [sq]
        exact mul_dvd_mul_left c1 hc1_dvd_b2
      exact dvd_of_sq_dvd_squarefree_mul_sq_tc064_aux hc1_sf (ne_of_gt hb_o.pos) hc1_sq_dvd
    obtain ⟨b1, rfl⟩ := hc1_dvd_b
    have hb1_o : Odd b1 := (odd_of_odd_mul_tc064_aux hb_o).2
    have hc1_pos : 0 < c1 := (odd_of_odd_mul_tc064_aux hb_o).1.pos
    have hf2_dvd : f ^ 2 ∣ squarefreeCoreStar a c * b1 ^ 2 := by
      rw [h_star_a1c1]
      have h_mul : c1 * f ^ 2 ∣ c1 * (a1 * c1 * b1 ^ 2) := by
        convert hc1_f2_dvd using 1
        ring
      exact (Nat.mul_dvd_mul_iff_left hc1_pos).mp h_mul
    have hf_dvd_b1 : f ∣ b1 :=
      dvd_of_sq_dvd_squarefree_mul_sq_tc064_aux hstar_sf (ne_of_gt hb1_o.pos) hf2_dvd
    obtain ⟨l, rfl⟩ := hf_dvd_b1
    have hl_o : Odd l := (odd_of_odd_mul_tc064_aux hb1_o).2
    have h_ql_eq : 2 ^ q * e * squarefreeCoreStar a c * l ^ 2 = n := by
      rw [hn_eq, hr_qs, pow_add, he, h_star_a1c1, ← hga1, ← hgc1]
      ring
    refine ⟨(q, l), ⟨hl_o, h_ql_eq⟩, ?_⟩
    rintro ⟨q', l'⟩ ⟨hl'_o, h_ql'_eq⟩
    obtain ⟨hq_eq, hl_eq⟩ := h_uniq_ql hl'_o hl_o (h_ql'_eq.trans h_ql_eq.symm)
    exact Prod.ext hq_eq hl_eq
  · rintro ⟨⟨q, l⟩, ⟨hl_o, h_ql_eq⟩, _⟩
    dsimp only at hl_o h_ql_eq
    have he_dvd : e ∣ n := by
      rw [← h_ql_eq]
      exact ⟨2 ^ q * squarefreeCoreStar a c * l ^ 2, by ring⟩
    let c1 := c / Nat.gcd a c
    have hc1_o : Odd c1 := by
      have hgc1 : Nat.gcd a c * c1 = c := Nat.mul_div_cancel' (Nat.gcd_dvd_right a c)
      exact (odd_of_odd_mul_tc064_aux (hgc1.symm ▸ hc_o)).2
    let b := c1 * f * l
    have hb_o : Odd b := (hc1_o.mul hf_o).mul hl_o
    refine ⟨⟨q + s, b, hb_o, ?_⟩, he_dvd⟩
    rw [← h_ql_eq, he]
    dsimp [b, c1]
    calc
      2 ^ q * (2 ^ s * c * f ^ 2) * squarefreeCoreStar a c * l ^ 2
        = 2 ^ (q + s) * (c * squarefreeCoreStar a c) * f ^ 2 * l ^ 2 := by
            rw [pow_add]; ring
      _ = 2 ^ (q + s) * (a * (c / Nat.gcd a c) ^ 2) * f ^ 2 * l ^ 2 := by rw [h_c_star]
      _ = 2 ^ (q + s) * a * (c / Nat.gcd a c * f * l) ^ 2 := by ring

private theorem sum_inv_Icc_one_le_one_add_log_tc064_aux {T : ℕ} (hT1 : 1 ≤ T) :
    (∑ m ∈ Finset.Icc 1 T, (1 : ℝ) / (m : ℝ)) ≤ 1 + Real.log (T : ℝ) := by
  obtain ⟨k, rfl⟩ : ∃ k : ℕ, T = 1 + k := ⟨T - 1, by omega⟩
  induction k with
  | zero =>
    simp
  | succ k ih =>
    have h_ins : Finset.Icc 1 (1 + (k + 1)) = insert (1 + k + 1) (Finset.Icc 1 (1 + k)) := by
      ext m; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
    have h_not : 1 + k + 1 ∉ Finset.Icc 1 (1 + k) := by simp
    rw [h_ins, Finset.sum_insert h_not]
    have hk_ih := ih (by omega)
    let m : ℝ := ((1 + k + 1 : ℕ) : ℝ)
    have hm_ge2 : (2 : ℝ) ≤ m := by dsimp [m]; exact_mod_cast (by omega : 2 ≤ 1 + k + 1)
    have hm_pos : 0 < m := by linarith
    have hm1_pos : 0 < m - 1 := by linarith
    have h_exp := Real.add_one_le_exp (-(1 / m))
    have h_lhs : -(1 / m) + 1 = (m - 1) / m := by field_simp [ne_of_gt hm_pos]; ring
    rw [h_lhs] at h_exp
    have h_log := Real.log_le_log (div_pos hm1_pos hm_pos) h_exp
    rw [Real.log_exp, Real.log_div (ne_of_gt hm1_pos) (ne_of_gt hm_pos)] at h_log
    have h_m1_eq : m - 1 = ((1 + k : ℕ) : ℝ) := by dsimp [m]; push_cast; ring
    have h_m_eq : ((1 + (k + 1) : ℕ) : ℝ) = m := by dsimp [m]; push_cast; ring
    rw [h_m1_eq] at h_log
    rw [h_m_eq]
    change 1 / m + ∑ x ∈ Finset.Icc 1 (1 + k), 1 / (x : ℝ) ≤ 1 + Real.log m
    linarith

/-- **Theorem 2 (`TASK-TC-064` §3.1, Divisor-Core `⋆`-Involution, Unconditional Divisor-Core Support Bijection, and Active-Core Harmonic Bound)**:
    1. *Squarefree `⋆`-involution & squared-quotient identity*:
       For all odd squarefree `a, c : ℕ`:
       - `Odd (squarefreeCoreStar a c) ∧ Squarefree (squarefreeCoreStar a c) ∧ 1 ≤ squarefreeCoreStar a c`;
       - `squarefreeCoreStar (squarefreeCoreStar a c) c = a`;
       - `c * squarefreeCoreStar a c = a * (c / Nat.gcd a c) ^ 2`;
    2. *Exact divisor-core support bijection (with NO coprimality assumed between `c` and `f`)*:
       For `e = 2 ^ s * c * f ^ 2` (`Odd c`, `Squarefree c`, `Odd f`), odd squarefree `a`, and `n ∈ Finset.Icc 1 T`:
       `((∃ r b : ℕ, Odd b ∧ n = 2 ^ r * a * b ^ 2) ∧ e ∣ n) ↔ ∃! ql : ℕ × ℕ, Odd ql.2 ∧ 2 ^ ql.1 * e * squarefreeCoreStar a c * ql.2 ^ 2 = n`;
    3. *Active-core harmonic sum bound*:
       For `1 ≤ e ≤ T` (`e = 2 ^ s * c * f ^ 2`, `Odd c`, `Squarefree c`, `Odd f`):
       `∑ a ∈ (oddSquarefreeCores T).filter (fun a => e * squarefreeCoreStar a c ≤ T), 1 / (squarefreeCoreStar a c : ℝ) ≤ 1 + Real.log T ≤ 1 + 2 * Real.log T`. -/
theorem divisor_core_star_involution_and_support_bijection_tc064 :
    (∀ {a c : ℕ}, Odd a → Squarefree a → Odd c → Squarefree c →
      (Odd (squarefreeCoreStar a c) ∧ Squarefree (squarefreeCoreStar a c) ∧
          1 ≤ squarefreeCoreStar a c) ∧
        squarefreeCoreStar (squarefreeCoreStar a c) c = a ∧
        c * squarefreeCoreStar a c = a * (c / Nat.gcd a c) ^ 2) ∧
    (∀ {e s c f T a : ℕ},
      e = 2 ^ s * c * f ^ 2 → Odd c → Squarefree c → Odd f → Odd a → Squarefree a →
      ∀ n ∈ Finset.Icc 1 T,
        (((∃ r b : ℕ, Odd b ∧ n = 2 ^ r * a * b ^ 2) ∧ e ∣ n) ↔
          ∃! ql : ℕ × ℕ, Odd ql.2 ∧ 2 ^ ql.1 * e * squarefreeCoreStar a c * ql.2 ^ 2 = n)) ∧
    (∀ {e s c f T : ℕ},
      1 ≤ e → e ≤ T → e = 2 ^ s * c * f ^ 2 → Odd c → Squarefree c → Odd f →
        (∑ a ∈ (oddSquarefreeCores T).filter (fun a => e * squarefreeCoreStar a c ≤ T),
            (1 : ℝ) / (squarefreeCoreStar a c : ℝ)) ≤
          1 + Real.log (T : ℝ) ∧
          1 + Real.log (T : ℝ) ≤ 1 + 2 * Real.log (T : ℝ)) := by
  refine ⟨fun ha_o ha_sf hc_o hc_sf => squarefreeCoreStar_props_tc064_aux ha_o ha_sf hc_o hc_sf,
    fun he hc_o hc_sf hf_o ha_o ha_sf n hn =>
      divisor_core_support_bijection_tc064_aux he hc_o hc_sf hf_o ha_o ha_sf
        (Finset.mem_Icc.mp hn).1,
    ?_⟩
  intro e s c f T he1 heT _he hc_o hc_sf _hf_o
  have hT1 : 1 ≤ T := le_trans he1 heT
  let S_act := (oddSquarefreeCores T).filter (fun a => e * squarefreeCoreStar a c ≤ T)
  have h_inj : Set.InjOn (fun a => squarefreeCoreStar a c) ↑S_act := by
    intro a1 ha1 a2 ha2 h_eq
    dsimp only at h_eq
    have h1 := Finset.mem_filter.mp (Finset.mem_filter.mp ha1).1
    have h2 := Finset.mem_filter.mp (Finset.mem_filter.mp ha2).1
    have hinv1 := (squarefreeCoreStar_props_tc064_aux h1.2.1 h1.2.2.1 hc_o hc_sf).2.1
    have hinv2 := (squarefreeCoreStar_props_tc064_aux h2.2.1 h2.2.2.1 hc_o hc_sf).2.1
    rw [← hinv1, h_eq, hinv2]
  have h_sub : S_act.image (fun a => squarefreeCoreStar a c) ⊆ Finset.Icc 1 T := by
    intro m hm
    rw [Finset.mem_image] at hm
    rcases hm with ⟨a, ha, rfl⟩
    have ha_f := Finset.mem_filter.mp ha
    have ha_c := Finset.mem_filter.mp ha_f.1
    have h_st1 := (squarefreeCoreStar_props_tc064_aux ha_c.2.1 ha_c.2.2.1 hc_o hc_sf).1.2.2
    have h_le : squarefreeCoreStar a c ≤ e * squarefreeCoreStar a c :=
      Nat.le_mul_of_pos_left _ he1
    exact Finset.mem_Icc.mpr ⟨h_st1, le_trans h_le ha_f.2⟩
  have h_sum_le :
      (∑ a ∈ S_act, (1 : ℝ) / (squarefreeCoreStar a c : ℝ)) ≤ 1 + Real.log (T : ℝ) := by
    calc
      (∑ a ∈ S_act, (1 : ℝ) / (squarefreeCoreStar a c : ℝ))
        = ∑ m ∈ S_act.image (fun a => squarefreeCoreStar a c), (1 : ℝ) / (m : ℝ) :=
          (Finset.sum_image (f := fun m : ℕ => (1 : ℝ) / (m : ℝ)) h_inj).symm
      _ ≤ ∑ m ∈ Finset.Icc 1 T, (1 : ℝ) / (m : ℝ) :=
          Finset.sum_le_sum_of_subset_of_nonneg h_sub (fun _ _ _ => by positivity)
      _ ≤ 1 + Real.log (T : ℝ) := sum_inv_Icc_one_le_one_add_log_tc064_aux hT1
  have hlogT_nn : 0 ≤ Real.log (T : ℝ) := Real.log_nonneg (by exact_mod_cast hT1)
  exact ⟨h_sum_le, by linarith⟩

/-! ### Section 3: Uniform Same-Core Hilbert Bound and Closure Transfer (`TASK-TC-064` §3.2–§3.4) -/

private theorem integral_inv_window_eq_log_tc064_aux {w0 Y : ℝ} (hw0 : 1 < w0) (hY : 0 < Y) :
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
    Real.log_mul (ne_of_gt (by linarith)) (ne_of_gt hY)]
  ring

private theorem continuousOn_gaussianTermPhi_param_tc064_aux (Y w0 : ℝ) (n : ℕ) :
    ContinuousOn (gaussianTermPhi n) (Set.uIcc Y (w0 * Y)) := by
  unfold gaussianTermPhi
  have h_rpow : ContinuousOn (fun X : ℝ => X ^ (5 / 2 : ℝ)) (Set.uIcc Y (w0 * Y)) := by
    apply ContinuousOn.rpow_const continuousOn_id
    intro _ _; right; norm_num
  have h_exp : Continuous (fun X : ℝ => (((n : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (n : ℝ) ^ 2))) :=
    continuous_const.mul (Real.continuous_exp.comp ((continuous_pow 2).neg.div_const _))
  exact h_rpow.mul h_exp.continuousOn

private theorem paramWindowNormSq_gaussianTermPhi_sqrt_le_tc064_aux
    {w0 Y : ℝ} (hw0 : 1 < w0) (hY : 0 < Y) {n : ℕ} (_hn : 1 ≤ n) :
    Real.sqrt (paramWindowNormSq Y w0 (gaussianTermPhi n)) ≤
      w0 ^ (5 / 2 : ℝ) * Real.sqrt (Real.log w0) * Y ^ (5 / 2 : ℝ) / (n : ℝ) ^ 3 *
        Real.exp (-(Y ^ 2) / (n : ℝ) ^ 2) := by
  have hle : Y ≤ w0 * Y := by nlinarith
  have hw0_pos : 0 < w0 := by linarith
  have hlog_pos : 0 < Real.log w0 := Real.log_pos hw0
  let B : ℝ :=
    w0 ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ) / (n : ℝ) ^ 3 * Real.exp (-(Y ^ 2) / (n : ℝ) ^ 2)
  have hB_nn : 0 ≤ B := by dsimp [B]; positivity
  have hpos : ∀ X ∈ Set.uIcc Y (w0 * Y), 0 < X := by
    intro X hX; rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX; linarith
  have h_pt :
      ∀ X ∈ Set.Icc Y (w0 * Y),
        0 ≤ gaussianTermPhi n X ∧ gaussianTermPhi n X ≤ B := by
    intro X hX
    have hX_pos : 0 < X := lt_of_lt_of_le hY hX.1
    unfold gaussianTermPhi
    refine ⟨by positivity, ?_⟩
    have hrpow : X ^ (5 / 2 : ℝ) ≤ w0 ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ) := by
      calc
        X ^ (5 / 2 : ℝ) ≤ (w0 * Y) ^ (5 / 2 : ℝ) :=
          Real.rpow_le_rpow (le_of_lt hX_pos) hX.2 (by norm_num)
        _ = w0 ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ) :=
          Real.mul_rpow (le_of_lt hw0_pos) (le_of_lt hY)
    have hexp : Real.exp (-(X ^ 2) / (n : ℝ) ^ 2) ≤ Real.exp (-(Y ^ 2) / (n : ℝ) ^ 2) := by
      apply Real.exp_le_exp.mpr
      exact div_le_div_of_nonneg_right
        (neg_le_neg (pow_le_pow_left (le_of_lt hY) hX.1 2)) (sq_nonneg _)
    have h_inv_exp :
        ((n : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (n : ℝ) ^ 2) ≤
          ((n : ℝ) ^ 3)⁻¹ * Real.exp (-(Y ^ 2) / (n : ℝ) ^ 2) :=
      mul_le_mul_of_nonneg_left hexp (by positivity)
    calc
      X ^ (5 / 2 : ℝ) * (((n : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (n : ℝ) ^ 2))
        ≤ (w0 ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ)) *
            (((n : ℝ) ^ 3)⁻¹ * Real.exp (-(Y ^ 2) / (n : ℝ) ^ 2)) :=
          mul_le_mul hrpow h_inv_exp (by positivity) (by positivity)
      _ = B := by dsimp [B]; ring
  have hc_phi := continuousOn_gaussianTermPhi_param_tc064_aux Y w0 n
  have hi_lhs :
      IntervalIntegrable (fun X => gaussianTermPhi n X * gaussianTermPhi n X / X)
        volume Y (w0 * Y) := by
    apply ContinuousOn.intervalIntegrable
    exact (hc_phi.mul hc_phi).div continuousOn_id (fun X hX => ne_of_gt (hpos X hX))
  have hi_rhs :
      IntervalIntegrable (fun X => B ^ 2 * ((1 : ℝ) / X)) volume Y (w0 * Y) := by
    apply ContinuousOn.intervalIntegrable
    exact continuousOn_const.mul
      (continuousOn_const.div continuousOn_id (fun X hX => ne_of_gt (hpos X hX)))
  have h_int_le : paramWindowNormSq Y w0 (gaussianTermPhi n) ≤ (B * Real.sqrt (Real.log w0)) ^ 2 := by
    unfold paramWindowNormSq paramWindowPairing
    calc
      (∫ X in Y..(w0 * Y), gaussianTermPhi n X * gaussianTermPhi n X / X)
        ≤ ∫ X in Y..(w0 * Y), B ^ 2 * ((1 : ℝ) / X) := by
          apply intervalIntegral.integral_mono_on hle hi_lhs hi_rhs
          intro X hX
          have hX_pos : 0 < X := lt_of_lt_of_le hY hX.1
          obtain ⟨h_nn, h_ub⟩ := h_pt X hX
          have h_sq : gaussianTermPhi n X * gaussianTermPhi n X ≤ B ^ 2 := by
            rw [sq]; exact mul_le_mul h_ub h_ub h_nn hB_nn
          calc
            gaussianTermPhi n X * gaussianTermPhi n X / X
              ≤ B ^ 2 / X := div_le_div_of_nonneg_right h_sq (le_of_lt hX_pos)
            _ = B ^ 2 * ((1 : ℝ) / X) := by ring
      _ = B ^ 2 * (∫ X in Y..(w0 * Y), (1 : ℝ) / X) := intervalIntegral.integral_const_mul _ _
      _ = B ^ 2 * Real.log w0 := by rw [integral_inv_window_eq_log_tc064_aux hw0 hY]
      _ = (B * Real.sqrt (Real.log w0)) ^ 2 := by
          symm
          rw [mul_pow, Real.sq_sqrt (le_of_lt hlog_pos)]
  calc
    Real.sqrt (paramWindowNormSq Y w0 (gaussianTermPhi n))
      ≤ Real.sqrt ((B * Real.sqrt (Real.log w0)) ^ 2) := Real.sqrt_le_sqrt h_int_le
    _ = B * Real.sqrt (Real.log w0) := Real.sqrt_sq (mul_nonneg hB_nn (Real.sqrt_nonneg _))
    _ = w0 ^ (5 / 2 : ℝ) * Real.sqrt (Real.log w0) * Y ^ (5 / 2 : ℝ) / (n : ℝ) ^ 3 *
          Real.exp (-(Y ^ 2) / (n : ℝ) ^ 2) := by
        dsimp [B]; ring

private theorem sum_inv_pow_six_tail_le_tc064_aux {a : ℕ} (ha : 1 ≤ a) (L_lim : ℕ) :
    (∑ l ∈ Finset.Icc (a + 1) L_lim, (1 : ℝ) / (l : ℝ) ^ 6) ≤ 1 / (5 * (a : ℝ) ^ 5) := by
  have h_step :
      ∀ {x : ℝ}, 0 < x →
        (1 : ℝ) / (x + 1) ^ 6 ≤ (1 / 5 : ℝ) * (1 / x ^ 5 - 1 / (x + 1) ^ 5) := by
    intro x hx
    have hx1 : 0 < x + 1 := by linarith
    have h_diff :
        (1 / 5 : ℝ) * (1 / x ^ 5 - 1 / (x + 1) ^ 5) - (1 : ℝ) / (x + 1) ^ 6 =
          (15 * x ^ 4 + 20 * x ^ 3 + 15 * x ^ 2 + 6 * x + 1) / (5 * x ^ 5 * (x + 1) ^ 6) := by
      field_simp [ne_of_gt hx, ne_of_gt hx1]
      ring
    have h_nn : 0 ≤ (15 * x ^ 4 + 20 * x ^ 3 + 15 * x ^ 2 + 6 * x + 1) / (5 * x ^ 5 * (x + 1) ^ 6) := by
      positivity
    linarith
  have h_range :
      ∀ m : ℕ,
        (∑ j ∈ Finset.range m, (1 : ℝ) / ((a + 1 + j : ℕ) : ℝ) ^ 6) ≤
          (1 / 5 : ℝ) * (1 / (a : ℝ) ^ 5 - 1 / ((a + m : ℕ) : ℝ) ^ 5) := by
    intro m
    induction m with
    | zero =>
      simp
    | succ m ih =>
      rw [Finset.sum_range_succ]
      let x : ℝ := ((a + m : ℕ) : ℝ)
      have hx_pos : 0 < x := by dsimp [x]; exact_mod_cast (by omega : 0 < a + m)
      have hs := h_step hx_pos
      have h1 : ((a + 1 + m : ℕ) : ℝ) = x + 1 := by dsimp [x]; push_cast; ring
      have h2 : ((a + (m + 1) : ℕ) : ℝ) = x + 1 := by dsimp [x]; push_cast; ring
      rw [h1, h2]
      linarith
  by_cases hle : L_lim ≤ a
  · have hemp : Finset.Icc (a + 1) L_lim = ∅ := by
      ext l; simp only [Finset.mem_Icc, Finset.not_mem_empty, iff_false]; omega
    rw [hemp, Finset.sum_empty]
    positivity
  · let m := L_lim - a
    have h_im : Finset.Icc (a + 1) L_lim = (Finset.range m).image (fun j => a + 1 + j) := by
      ext l
      simp only [Finset.mem_Icc, Finset.mem_image, Finset.mem_range]
      constructor
      · intro hl
        exact ⟨l - (a + 1), by dsimp [m]; omega, by omega⟩
      · rintro ⟨j, hj, rfl⟩
        exact ⟨by omega, by dsimp [m] at hj; omega⟩
    have h_inj : Set.InjOn (fun j => a + 1 + j) ↑(Finset.range m) :=
      fun j1 _ j2 _ (h : a + 1 + j1 = a + 1 + j2) => by omega
    rw [h_im, Finset.sum_image h_inj]
    have hr := h_range m
    have h_neg_nn : 0 ≤ (1 / 5 : ℝ) * (1 / ((a + m : ℕ) : ℝ) ^ 5) := by positivity
    have h_rhs_eq : (1 / 5 : ℝ) * (1 / (a : ℝ) ^ 5) = 1 / (5 * (a : ℝ) ^ 5) := by ring
    linarith

private theorem quartic_gaussian_square_sum_le_tc064_aux {A : ℝ} (hA : 0 < A) (L_lim : ℕ) :
    (∑ l ∈ Finset.Icc 1 L_lim,
      A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4)) ≤ 16 / 5 := by
  let s : ℝ := Real.sqrt A
  have hs_pos : 0 < s := Real.sqrt_pos.mpr hA
  have hs_sq : s ^ 2 = A := Real.sq_sqrt (le_of_lt hA)
  have hA_52 : A ^ (5 / 2 : ℝ) = s ^ 5 := by
    rw [← hs_sq, ← Real.rpow_natCast s 2, ← Real.rpow_mul (le_of_lt hs_pos)]
    have he : ((2 : ℕ) : ℝ) * (5 / 2 : ℝ) = ((5 : ℕ) : ℝ) := by norm_num
    rw [he, Real.rpow_natCast]
  have hA2 : A ^ 2 = s ^ 4 := by rw [← hs_sq]; ring
  have hexp_le1 : ∀ l : ℕ, Real.exp (-(A ^ 2) / (l : ℝ) ^ 4) ≤ 1 := by
    intro l
    rw [Real.exp_le_one_iff]
    exact div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg A)) (pow_nonneg (Nat.cast_nonneg l) 4)
  have h_term_nn :
      ∀ l : ℕ, 0 ≤ A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4) :=
    fun _ => by positivity
  rcases le_or_gt A 1 with hA_le1 | hA_gt1
  · have hA52_le1 : A ^ (5 / 2 : ℝ) ≤ 1 :=
      Real.rpow_le_one (le_of_lt hA) hA_le1 (by norm_num)
    have h_each :
        ∀ l ∈ Finset.Icc 1 L_lim,
          A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4) ≤
            (1 : ℝ) / (l : ℝ) ^ 6 := by
      intro l _
      have hl6_nn : 0 ≤ (l : ℝ) ^ 6 := pow_nonneg (Nat.cast_nonneg l) 6
      calc
        A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4)
          ≤ A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * 1 :=
            mul_le_mul_of_nonneg_left (hexp_le1 l) (by positivity)
        _ = A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 := mul_one _
        _ ≤ 1 / (l : ℝ) ^ 6 := div_le_div_of_nonneg_right hA52_le1 hl6_nn
    have h_sub12 : Finset.Icc 1 L_lim ⊆ ({1} : Finset ℕ) ∪ Finset.Icc 2 L_lim := by
      intro l hl; simp only [Finset.mem_Icc, Finset.mem_union, Finset.mem_singleton] at hl ⊢; omega
    have h_d12 : Disjoint ({1} : Finset ℕ) (Finset.Icc 2 L_lim) := by
      rw [Finset.disjoint_left]; intro l h1 h2; simp at h1 h2; omega
    have h_tail := sum_inv_pow_six_tail_le_tc064_aux (le_refl 1) L_lim
    calc
      (∑ l ∈ Finset.Icc 1 L_lim,
          A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4))
        ≤ ∑ l ∈ Finset.Icc 1 L_lim, (1 : ℝ) / (l : ℝ) ^ 6 := Finset.sum_le_sum h_each
      _ ≤ ∑ l ∈ ({1} : Finset ℕ) ∪ Finset.Icc 2 L_lim, (1 : ℝ) / (l : ℝ) ^ 6 :=
          Finset.sum_le_sum_of_subset_of_nonneg h_sub12 (fun _ _ _ => by positivity)
      _ = 1 + ∑ l ∈ Finset.Icc (1 + 1) L_lim, (1 : ℝ) / (l : ℝ) ^ 6 := by
          rw [Finset.sum_union h_d12, Finset.sum_singleton]; norm_num
      _ ≤ 1 + 1 / (5 * ((1 : ℕ) : ℝ) ^ 5) := add_le_add_left h_tail 1
      _ ≤ 16 / 5 := by norm_num
  · let N_fl := Nat.floor s
    have hs1 : 1 ≤ Real.sqrt A := Real.one_le_sqrt.mpr (le_of_lt hA_gt1)
    have hN_ge1 : 1 ≤ N_fl := Nat.le_floor (by exact_mod_cast hs1)
    have hN_le_s : (N_fl : ℝ) ≤ s := Nat.floor_le (le_of_lt hs_pos)
    have hs_lt_N1 : s < ((N_fl + 1 : ℕ) : ℝ) := by
      simpa [Nat.cast_add, Nat.cast_one] using Nat.lt_floor_add_one s
    let S1 := Finset.Icc 1 N_fl
    let S2 : Finset ℕ := {N_fl + 1}
    let S3 := Finset.Icc (N_fl + 2) L_lim
    have h_sub : Finset.Icc 1 L_lim ⊆ (S1 ∪ S2) ∪ S3 := by
      intro l hl
      simp only [S1, S2, S3, Finset.mem_Icc, Finset.mem_union, Finset.mem_singleton] at hl ⊢
      omega
    have hd12 : Disjoint S1 S2 := by
      rw [Finset.disjoint_left]; intro l h1 h2; simp [S1, S2] at h1 h2; omega
    have hd123 : Disjoint (S1 ∪ S2) S3 := by
      rw [Finset.disjoint_left]; intro l h12 h3; simp [S1, S2, S3] at h12 h3; omega
    have h_bd1 :
        (∑ l ∈ S1, A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4)) ≤ 2 := by
      have h_each1 :
          ∀ l ∈ S1,
            A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4) ≤
              2 * (N_fl : ℝ) ^ 2 / s ^ 3 := by
        intro l hl
        have hl_bds := Finset.mem_Icc.mp hl
        have hl_pos : (0 : ℝ) < (l : ℝ) := Nat.cast_pos.mpr hl_bds.1
        have hl_le_N : (l : ℝ) ≤ (N_fl : ℝ) := by exact_mod_cast hl_bds.2
        let u : ℝ := s ^ 4 / (l : ℝ) ^ 4
        have hu_pos : 0 < u := by dsimp [u]; positivity
        have hq := Real.quadratic_le_exp_of_nonneg (le_of_lt hu_pos)
        have hu2_le : (u ^ 2 / 2) ≤ Real.exp u := by linarith
        have h_prod : Real.exp u * Real.exp (-u) = 1 := by
          rw [← Real.exp_add, add_neg_self, Real.exp_zero]
        have hm := mul_le_mul_of_nonneg_right hu2_le (le_of_lt (Real.exp_pos (-u)))
        rw [h_prod] at hm
        have hexp_u : Real.exp (-u) ≤ 2 / u ^ 2 := by
          rw [le_div_iff (pow_pos hu_pos 2)]
          linarith
        have h_neg_eq : -(A ^ 2) / (l : ℝ) ^ 4 = -u := by
          dsimp [u]; rw [hA2]; ring
        have hl2_le : (l : ℝ) ^ 2 ≤ (N_fl : ℝ) ^ 2 :=
          pow_le_pow_left (le_of_lt hl_pos) hl_le_N 2
        calc
          A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4)
            = s ^ 5 / (l : ℝ) ^ 6 * Real.exp (-u) := by rw [hA_52, h_neg_eq]
          _ ≤ s ^ 5 / (l : ℝ) ^ 6 * (2 / u ^ 2) :=
              mul_le_mul_of_nonneg_left hexp_u (by positivity)
          _ = 2 * (l : ℝ) ^ 2 / s ^ 3 := by
              dsimp [u]
              field_simp [ne_of_gt hl_pos, ne_of_gt hs_pos]
              ring
          _ ≤ 2 * (N_fl : ℝ) ^ 2 / s ^ 3 := by
              exact div_le_div_of_nonneg_right
                (mul_le_mul_of_nonneg_left hl2_le (by norm_num)) (by positivity)
      have hc1 : (S1.card : ℝ) ≤ (N_fl : ℝ) := by
        have hc : S1.card ≤ N_fl := by simp [S1, Nat.card_Icc]
        exact_mod_cast hc
      have hN3_le : (N_fl : ℝ) ^ 3 ≤ s ^ 3 :=
        pow_le_pow_left (Nat.cast_nonneg N_fl) hN_le_s 3
      calc
        (∑ l ∈ S1, A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4))
          ≤ ∑ _l ∈ S1, (2 * (N_fl : ℝ) ^ 2 / s ^ 3) := Finset.sum_le_sum h_each1
        _ = (S1.card : ℝ) * (2 * (N_fl : ℝ) ^ 2 / s ^ 3) := by simp
        _ ≤ (N_fl : ℝ) * (2 * (N_fl : ℝ) ^ 2 / s ^ 3) :=
            mul_le_mul_of_nonneg_right hc1 (by positivity)
        _ = 2 * ((N_fl : ℝ) ^ 3 / s ^ 3) := by ring
        _ ≤ 2 * 1 := mul_le_mul_of_nonneg_left ((div_le_one (pow_pos hs_pos 3)).mpr hN3_le) (by norm_num)
        _ = 2 := mul_one 2
    have h_bd2 :
        (∑ l ∈ S2, A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4)) ≤ 1 := by
      dsimp [S2]
      rw [Finset.sum_singleton, hA_52]
      have hN1_ge1 : (1 : ℝ) ≤ ((N_fl + 1 : ℕ) : ℝ) := by exact_mod_cast (by omega : 1 ≤ N_fl + 1)
      have hs5_le : s ^ 5 ≤ ((N_fl + 1 : ℕ) : ℝ) ^ 5 :=
        pow_le_pow_left (le_of_lt hs_pos) (le_of_lt hs_lt_N1) 5
      have h5_le_6 : ((N_fl + 1 : ℕ) : ℝ) ^ 5 ≤ ((N_fl + 1 : ℕ) : ℝ) ^ 6 := by
        calc
          ((N_fl + 1 : ℕ) : ℝ) ^ 5 = ((N_fl + 1 : ℕ) : ℝ) ^ 5 * 1 := (mul_one _).symm
          _ ≤ ((N_fl + 1 : ℕ) : ℝ) ^ 5 * ((N_fl + 1 : ℕ) : ℝ) :=
              mul_le_mul_of_nonneg_left hN1_ge1 (by positivity)
          _ = ((N_fl + 1 : ℕ) : ℝ) ^ 6 := by ring
      calc
        s ^ 5 / ((N_fl + 1 : ℕ) : ℝ) ^ 6 * Real.exp (-(A ^ 2) / ((N_fl + 1 : ℕ) : ℝ) ^ 4)
          ≤ s ^ 5 / ((N_fl + 1 : ℕ) : ℝ) ^ 6 * 1 :=
            mul_le_mul_of_nonneg_left (hexp_le1 (N_fl + 1)) (by positivity)
        _ = s ^ 5 / ((N_fl + 1 : ℕ) : ℝ) ^ 6 := mul_one _
        _ ≤ 1 := (div_le_one (by positivity)).mpr (le_trans hs5_le h5_le_6)
    have h_bd3 :
        (∑ l ∈ S3, A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4)) ≤ 1 / 5 := by
      have h_each3 :
          ∀ l ∈ S3,
            A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4) ≤
              s ^ 5 * ((1 : ℝ) / (l : ℝ) ^ 6) := by
        intro l _
        rw [hA_52]
        calc
          s ^ 5 / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4)
            ≤ s ^ 5 / (l : ℝ) ^ 6 * 1 :=
              mul_le_mul_of_nonneg_left (hexp_le1 l) (by positivity)
          _ = s ^ 5 * ((1 : ℝ) / (l : ℝ) ^ 6) := by ring
      have h_tail := sum_inv_pow_six_tail_le_tc064_aux (by omega : 1 ≤ N_fl + 1) L_lim
      have hs5_le : s ^ 5 ≤ ((N_fl + 1 : ℕ) : ℝ) ^ 5 :=
        pow_le_pow_left (le_of_lt hs_pos) (le_of_lt hs_lt_N1) 5
      have hN1_pos : (0 : ℝ) < ((N_fl + 1 : ℕ) : ℝ) := by positivity
      calc
        (∑ l ∈ S3, A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4))
          ≤ ∑ l ∈ S3, s ^ 5 * ((1 : ℝ) / (l : ℝ) ^ 6) := Finset.sum_le_sum h_each3
        _ = s ^ 5 * (∑ l ∈ Finset.Icc ((N_fl + 1) + 1) L_lim, (1 : ℝ) / (l : ℝ) ^ 6) :=
            (Finset.mul_sum _ _ _).symm
        _ ≤ s ^ 5 * (1 / (5 * ((N_fl + 1 : ℕ) : ℝ) ^ 5)) :=
            mul_le_mul_of_nonneg_left h_tail (by positivity)
        _ ≤ ((N_fl + 1 : ℕ) : ℝ) ^ 5 * (1 / (5 * ((N_fl + 1 : ℕ) : ℝ) ^ 5)) :=
            mul_le_mul_of_nonneg_right hs5_le (by positivity)
        _ = 1 / 5 := by field_simp [ne_of_gt hN1_pos]; ring
    calc
      (∑ l ∈ Finset.Icc 1 L_lim,
          A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4))
        ≤ ∑ l ∈ (S1 ∪ S2) ∪ S3,
            A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4) :=
          Finset.sum_le_sum_of_subset_of_nonneg h_sub (fun l _ _ => h_term_nn l)
      _ = (∑ l ∈ S1, A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4)) +
            (∑ l ∈ S2, A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4)) +
            (∑ l ∈ S3, A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4)) := by
          rw [Finset.sum_union hd123, Finset.sum_union hd12]
      _ ≤ 2 + 1 + 1 / 5 := add_le_add (add_le_add h_bd1 h_bd2) h_bd3
      _ = 16 / 5 := by norm_num

private theorem square_support_gaussian_norm_sum_tc064_aux
    {w0 Y : ℝ} (hw0 : 1 < w0) (hY : 0 < Y) {M : ℕ} (hM : 1 ≤ M) (R L_lim : ℕ) :
    (∑ r ∈ Finset.range (R + 1),
      ∑ l ∈ Finset.Icc 1 L_lim,
        Real.sqrt (paramWindowNormSq Y w0 (gaussianTermPhi (2 ^ r * M * l ^ 2)))) ≤
      ((16 / 5 : ℝ) * (2 + Real.sqrt 2) * w0 ^ (5 / 2 : ℝ) * Real.sqrt (Real.log w0)) /
        Real.sqrt (M : ℝ) := by
  have hlog_pos : 0 < Real.log w0 := Real.log_pos hw0
  let W_fac : ℝ := w0 ^ (5 / 2 : ℝ) * Real.sqrt (Real.log w0)
  have hM_pos : (0 : ℝ) < (M : ℝ) := Nat.cast_pos.mpr hM
  have h_each_r :
      ∀ r ∈ Finset.range (R + 1),
        (∑ l ∈ Finset.Icc 1 L_lim,
          Real.sqrt (paramWindowNormSq Y w0 (gaussianTermPhi (2 ^ r * M * l ^ 2)))) ≤
          ((16 / 5 : ℝ) * W_fac / Real.sqrt (M : ℝ)) * (1 / Real.sqrt 2) ^ r := by
    intro r _
    let Mr : ℕ := 2 ^ r * M
    have hMr1 : 1 ≤ Mr := Nat.mul_pos (pow_pos (by decide) r) hM
    have hMr_pos : (0 : ℝ) < (Mr : ℝ) := Nat.cast_pos.mpr hMr1
    let A : ℝ := Y / (Mr : ℝ)
    have hA_pos : 0 < A := div_pos hY hMr_pos
    have hMr_3 : (Mr : ℝ) ^ 3 = (Mr : ℝ) ^ (5 / 2 : ℝ) * Real.sqrt (Mr : ℝ) := by
      rw [Real.sqrt_eq_rpow, ← Real.rpow_add hMr_pos]
      have he : (5 / 2 : ℝ) + (1 / 2 : ℝ) = ((3 : ℕ) : ℝ) := by norm_num
      rw [he, Real.rpow_natCast]
    have hA_52 : A ^ (5 / 2 : ℝ) = Y ^ (5 / 2 : ℝ) / (Mr : ℝ) ^ (5 / 2 : ℝ) :=
      Real.div_rpow (le_of_lt hY) (le_of_lt hMr_pos) (5 / 2 : ℝ)
    have h_each_l :
        ∀ l ∈ Finset.Icc 1 L_lim,
          Real.sqrt (paramWindowNormSq Y w0 (gaussianTermPhi (Mr * l ^ 2))) ≤
            (W_fac / Real.sqrt (Mr : ℝ)) *
              (A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4)) := by
      intro l hl
      have hl1 : 1 ≤ l := (Finset.mem_Icc.mp hl).1
      have hl_pos : (0 : ℝ) < (l : ℝ) := Nat.cast_pos.mpr hl1
      have hn1 : 1 ≤ Mr * l ^ 2 := Nat.mul_pos hMr1 (Nat.one_le_pow 2 l hl1)
      have hb := paramWindowNormSq_gaussianTermPhi_sqrt_le_tc064_aux hw0 hY hn1
      have h_pow3 : ((Mr * l ^ 2 : ℕ) : ℝ) ^ 3 = (Mr : ℝ) ^ 3 * (l : ℝ) ^ 6 := by
        push_cast; ring
      have h_exp_eq :
          -(Y ^ 2) / ((Mr * l ^ 2 : ℕ) : ℝ) ^ 2 = -(A ^ 2) / (l : ℝ) ^ 4 := by
        dsimp [A]
        push_cast
        field_simp [ne_of_gt hMr_pos, ne_of_gt hl_pos]
        ring
      have hMr52_pos : 0 < (Mr : ℝ) ^ (5 / 2 : ℝ) := Real.rpow_pos_of_pos hMr_pos _
      have hsMr_pos : 0 < Real.sqrt (Mr : ℝ) := Real.sqrt_pos.mpr hMr_pos
      calc
        Real.sqrt (paramWindowNormSq Y w0 (gaussianTermPhi (Mr * l ^ 2)))
          ≤ W_fac * Y ^ (5 / 2 : ℝ) / ((Mr * l ^ 2 : ℕ) : ℝ) ^ 3 *
              Real.exp (-(Y ^ 2) / ((Mr * l ^ 2 : ℕ) : ℝ) ^ 2) := hb
        _ = W_fac * Y ^ (5 / 2 : ℝ) / ((Mr : ℝ) ^ (5 / 2 : ℝ) * Real.sqrt (Mr : ℝ) * (l : ℝ) ^ 6) *
              Real.exp (-(A ^ 2) / (l : ℝ) ^ 4) := by
            rw [h_pow3, hMr_3, h_exp_eq]
        _ = (W_fac / Real.sqrt (Mr : ℝ)) *
              (A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4)) := by
            rw [hA_52]
            field_simp [ne_of_gt hMr52_pos, ne_of_gt hsMr_pos, ne_of_gt hl_pos]
            ring
    have h_sqrt_2pow : ∀ k : ℕ, Real.sqrt ((2 : ℝ) ^ k) = (Real.sqrt 2) ^ k := by
      intro k
      induction k with
      | zero => simp
      | succ k ih => rw [pow_succ, Real.sqrt_mul (by positivity), ih, pow_succ]
    have h_sqrt_Mr :
        Real.sqrt (Mr : ℝ) = (Real.sqrt 2) ^ r * Real.sqrt (M : ℝ) := by
      dsimp [Mr]
      push_cast
      rw [Real.sqrt_mul (by positivity), h_sqrt_2pow r]
    have h_inv_Mr :
        1 / Real.sqrt (Mr : ℝ) = (1 / Real.sqrt 2) ^ r / Real.sqrt (M : ℝ) := by
      rw [h_sqrt_Mr, one_div_pow]
      field_simp [ne_of_gt (Real.sqrt_pos.mpr hM_pos),
        ne_of_gt (pow_pos (Real.sqrt_pos.mpr (by norm_num : (0 : ℝ) < 2)) r)]
    calc
      (∑ l ∈ Finset.Icc 1 L_lim,
          Real.sqrt (paramWindowNormSq Y w0 (gaussianTermPhi (Mr * l ^ 2))))
        ≤ ∑ l ∈ Finset.Icc 1 L_lim,
            (W_fac / Real.sqrt (Mr : ℝ)) *
              (A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4)) :=
          Finset.sum_le_sum h_each_l
      _ = (W_fac / Real.sqrt (Mr : ℝ)) *
            (∑ l ∈ Finset.Icc 1 L_lim,
              A ^ (5 / 2 : ℝ) / (l : ℝ) ^ 6 * Real.exp (-(A ^ 2) / (l : ℝ) ^ 4)) :=
          (Finset.mul_sum _ _ _).symm
      _ ≤ (W_fac / Real.sqrt (Mr : ℝ)) * (16 / 5 : ℝ) :=
          mul_le_mul_of_nonneg_left (quartic_gaussian_square_sum_le_tc064_aux hA_pos L_lim)
            (by positivity)
      _ = ((16 / 5 : ℝ) * W_fac / Real.sqrt (M : ℝ)) * (1 / Real.sqrt 2) ^ r := by
          rw [div_eq_mul_one_div W_fac, h_inv_Mr]
          ring
  have h_geom :
      ∀ m : ℕ,
        (∑ r ∈ Finset.range m, (1 / Real.sqrt 2) ^ r) =
          (2 + Real.sqrt 2) * (1 - (1 / Real.sqrt 2) ^ m) := by
    intro m
    induction m with
    | zero =>
      simp
    | succ m ih =>
      rw [Finset.sum_range_succ, ih]
      have hs2_pos : 0 < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
      have hs2_sq : Real.sqrt 2 * Real.sqrt 2 = 2 := Real.mul_self_sqrt (by norm_num)
      have h_one : (2 + Real.sqrt 2) * (1 - 1 / Real.sqrt 2) = 1 := by
        apply mul_right_cancel₀ (ne_of_gt hs2_pos)
        calc
          (2 + Real.sqrt 2) * (1 - 1 / Real.sqrt 2) * Real.sqrt 2
            = (2 + Real.sqrt 2) * (Real.sqrt 2 - (1 / Real.sqrt 2) * Real.sqrt 2) := by ring
          _ = (2 + Real.sqrt 2) * (Real.sqrt 2 - 1) := by
              rw [one_div_mul_cancel (ne_of_gt hs2_pos)]
          _ = 2 * Real.sqrt 2 - 2 + Real.sqrt 2 * Real.sqrt 2 - Real.sqrt 2 := by ring
          _ = Real.sqrt 2 := by rw [hs2_sq]; ring
          _ = 1 * Real.sqrt 2 := (one_mul _).symm
      calc
        (2 + Real.sqrt 2) * (1 - (1 / Real.sqrt 2) ^ m) + (1 / Real.sqrt 2) ^ m
          = (2 + Real.sqrt 2) * (1 - (1 / Real.sqrt 2) ^ m) +
              (2 + Real.sqrt 2) * (1 - 1 / Real.sqrt 2) * (1 / Real.sqrt 2) ^ m := by
              rw [h_one, one_mul]
        _ = (2 + Real.sqrt 2) * (1 - (1 / Real.sqrt 2) ^ (m + 1)) := by
            rw [pow_succ]; ring
  have h_geom_le : (∑ r ∈ Finset.range (R + 1), (1 / Real.sqrt 2) ^ r) ≤ 2 + Real.sqrt 2 := by
    rw [h_geom (R + 1)]
    have hq_nn : 0 ≤ (1 / Real.sqrt 2) ^ (R + 1) := by positivity
    nlinarith [Real.sqrt_nonneg 2]
  calc
    (∑ r ∈ Finset.range (R + 1),
        ∑ l ∈ Finset.Icc 1 L_lim,
          Real.sqrt (paramWindowNormSq Y w0 (gaussianTermPhi (2 ^ r * M * l ^ 2))))
      ≤ ∑ r ∈ Finset.range (R + 1),
          ((16 / 5 : ℝ) * W_fac / Real.sqrt (M : ℝ)) * (1 / Real.sqrt 2) ^ r :=
        Finset.sum_le_sum h_each_r
    _ = ((16 / 5 : ℝ) * W_fac / Real.sqrt (M : ℝ)) *
          (∑ r ∈ Finset.range (R + 1), (1 / Real.sqrt 2) ^ r) :=
        (Finset.mul_sum _ _ _).symm
    _ ≤ ((16 / 5 : ℝ) * W_fac / Real.sqrt (M : ℝ)) * (2 + Real.sqrt 2) :=
        mul_le_mul_of_nonneg_left h_geom_le (by positivity)
    _ = ((16 / 5 : ℝ) * (2 + Real.sqrt 2) * w0 ^ (5 / 2 : ℝ) * Real.sqrt (Real.log w0)) /
          Real.sqrt (M : ℝ) := by
        dsimp [W_fac]; ring

private theorem stationPrimePowerFeatureG_norm_le_tc064_aux
    {Y : ℝ} (hY2 : 2 ≤ Y) {T n : ℕ} (hn : n ∈ Finset.Icc 1 T) :
    Real.sqrt
        (∑ pk ∈ primePowerPairsUpTo T,
          windowEnergyNormSq Y (fun X => stationPrimePowerFeatureG n pk X)) ≤
      (Real.log (T : ℝ) / Real.log Y) *
        Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi n)) := by
  obtain ⟨hn1, hnT⟩ := Finset.mem_Icc.mp hn
  obtain ⟨hle, hprops⟩ := uIcc_tau_log_props_tc064_aux hY2
  have hlogY_pos : 0 < Real.log Y := Real.log_pos (by linarith)
  have h_eq :
      (∑ pk ∈ primePowerPairsUpTo T,
          windowEnergyNormSq Y (fun X => stationPrimePowerFeatureG n pk X)) =
        commonPrimePowerLogSq n n * logWeightedWindowKernel 2 Y n n :=
    (uniform_same_chain_hilbert_bound_and_closure_transfer_tc063).2.1.1 hY2 hn1 hnT hn1 hnT
  have h_off_nn : 0 ≤ offDiagPrimePowerWeight n n :=
    ((finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.1.2.2.2 n hn1).1
  have h_c_le : commonPrimePowerLogSq n n ≤ (Real.log (T : ℝ)) ^ 2 := by
    have h1 : commonPrimePowerLogSq n n ≤ (Real.log (n : ℝ)) ^ 2 := by
      unfold offDiagPrimePowerWeight at h_off_nn
      linarith [show Real.log (n : ℝ) * Real.log (n : ℝ) = (Real.log (n : ℝ)) ^ 2 by ring]
    have hlog_n_nn : 0 ≤ Real.log (n : ℝ) := Real.log_nonneg (by exact_mod_cast hn1)
    have hlog_le : Real.log (n : ℝ) ≤ Real.log (T : ℝ) :=
      Real.log_le_log (Nat.cast_pos.mpr hn1) (by exact_mod_cast hnT)
    exact le_trans h1 (pow_le_pow_left hlog_n_nn hlog_le 2)
  have hc_phi := (continuousOn_station_and_chain_profiles_tc064_aux hY2 0 0 T 0).1 n
  have hlog_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
    ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hprops X hX).1)
  have hi_G :
      IntervalIntegrable
        (fun X => (gaussianTermPhi n X * gaussianTermPhi n X / (Real.log X) ^ 2) / X)
        volume Y (RiemannScope.tau * Y) := by
    apply ContinuousOn.intervalIntegrable
    exact ((hc_phi.mul hc_phi).div (hlog_cont.pow 2)
      (fun X hX => (hprops X hX).2.2.2)).div continuousOn_id
      (fun X hX => ne_of_gt (hprops X hX).1)
  have hi_phi :
      IntervalIntegrable
        (fun X => (1 / (Real.log Y) ^ 2) * (gaussianTermPhi n X * gaussianTermPhi n X / X))
        volume Y (RiemannScope.tau * Y) := by
    apply ContinuousOn.intervalIntegrable
    exact continuousOn_const.mul
      ((hc_phi.mul hc_phi).div continuousOn_id (fun X hX => ne_of_gt (hprops X hX).1))
  have h_G_nn : 0 ≤ logWeightedWindowKernel 2 Y n n := by
    unfold logWeightedWindowKernel
    apply intervalIntegral.integral_nonneg hle
    intro X hX
    exact div_nonneg (div_nonneg (mul_self_nonneg _) (sq_nonneg _))
      (by rw [Set.mem_Icc] at hX; linarith)
  have h_G_le :
      logWeightedWindowKernel 2 Y n n ≤
        (1 / (Real.log Y) ^ 2) * windowEnergyNormSq Y (gaussianTermPhi n) := by
    unfold logWeightedWindowKernel windowEnergyNormSq windowPairing
    rw [← intervalIntegral.integral_const_mul]
    apply intervalIntegral.integral_mono_on hle hi_G hi_phi
    intro X hX
    have hX_pos : 0 < X := by linarith [hX.1]
    have hlog_le : (Real.log Y) ^ 2 ≤ (Real.log X) ^ 2 :=
      pow_le_pow_left (le_of_lt hlogY_pos) (Real.log_le_log (by linarith) hX.1) 2
    have h_div :
        gaussianTermPhi n X * gaussianTermPhi n X / (Real.log X) ^ 2 ≤
          gaussianTermPhi n X * gaussianTermPhi n X / (Real.log Y) ^ 2 :=
      div_le_div_of_nonneg_left (mul_self_nonneg _) (sq_pos_of_pos hlogY_pos) hlog_le
    calc
      (gaussianTermPhi n X * gaussianTermPhi n X / (Real.log X) ^ 2) / X
        ≤ (gaussianTermPhi n X * gaussianTermPhi n X / (Real.log Y) ^ 2) / X :=
          div_le_div_of_nonneg_right h_div (le_of_lt hX_pos)
      _ = (1 / (Real.log Y) ^ 2) * (gaussianTermPhi n X * gaussianTermPhi n X / X) := by ring
  have h_phi_nn : 0 ≤ windowEnergyNormSq Y (gaussianTermPhi n) := by
    unfold windowEnergyNormSq windowPairing
    apply intervalIntegral.integral_nonneg hle
    intro X hX; exact div_nonneg (mul_self_nonneg _) (by linarith [hX.1])
  have h_prod_le :
      commonPrimePowerLogSq n n * logWeightedWindowKernel 2 Y n n ≤
        ((Real.log (T : ℝ) / Real.log Y) *
          Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi n))) ^ 2 := by
    calc
      commonPrimePowerLogSq n n * logWeightedWindowKernel 2 Y n n
        ≤ (Real.log (T : ℝ)) ^ 2 *
            ((1 / (Real.log Y) ^ 2) * windowEnergyNormSq Y (gaussianTermPhi n)) :=
          mul_le_mul h_c_le h_G_le h_G_nn (sq_nonneg _)
      _ = (Real.log (T : ℝ) / Real.log Y) ^ 2 *
            (Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi n))) ^ 2 := by
          rw [Real.sq_sqrt h_phi_nn]; ring
      _ = ((Real.log (T : ℝ) / Real.log Y) *
            Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi n))) ^ 2 := (mul_pow _ _ 2).symm
  have h_rhs_nn :
      0 ≤ (Real.log (T : ℝ) / Real.log Y) *
        Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi n)) :=
    mul_nonneg (div_nonneg (Real.log_nonneg (by exact_mod_cast (le_trans hn1 hnT)))
      (le_of_lt hlogY_pos)) (Real.sqrt_nonneg _)
  rw [h_eq]
  calc
    Real.sqrt (commonPrimePowerLogSq n n * logWeightedWindowKernel 2 Y n n)
      ≤ Real.sqrt (((Real.log (T : ℝ) / Real.log Y) *
          Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi n))) ^ 2) :=
        Real.sqrt_le_sqrt h_prod_le
    _ = (Real.log (T : ℝ) / Real.log Y) *
          Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi n)) := Real.sqrt_sq h_rhs_nn

private theorem sum_subset_image_le_sum_tc064_aux {α β : Type*} [DecidableEq α] [DecidableEq β]
    (P : Finset α) (U : Finset β) (φ : α → β) (f : β → ℝ)
    (hf_nn : ∀ y, 0 ≤ f y) (h_cov : ∀ y ∈ U, ∃ x ∈ P, φ x = y) :
    (∑ y ∈ U, f y) ≤ ∑ x ∈ P, f (φ x) := by
  induction P using Finset.induction_on generalizing U with
  | empty =>
    have hU : U = ∅ := by
      ext y; simp only [Finset.not_mem_empty, iff_false]
      intro hy; obtain ⟨x, hx, _⟩ := h_cov y hy; exact Finset.not_mem_empty x hx
    rw [hU, Finset.sum_empty, Finset.sum_empty]
  | @insert x0 P' hx0 ih =>
    rw [Finset.sum_insert hx0]
    have h_cov' : ∀ y ∈ U.erase (φ x0), ∃ x ∈ P', φ x = y := by
      intro y hy
      obtain ⟨hy_ne, hy_U⟩ := Finset.mem_erase.mp hy
      obtain ⟨x, hx_ins, hφx⟩ := h_cov y hy_U
      rcases Finset.mem_insert.mp hx_ins with rfl | hx_P'
      · exact False.elim (hy_ne hφx.symm)
      · exact ⟨x, hx_P', hφx⟩
    have ih_er := ih (U.erase (φ x0)) h_cov'
    by_cases h_mem : φ x0 ∈ U
    · rw [← Finset.add_sum_erase _ _ h_mem]
      exact add_le_add_left ih_er _
    · rw [Finset.erase_eq_of_not_mem h_mem] at ih_er
      linarith [hf_nn (φ x0)]

private theorem finset_cauchy_schwarz_nonneg_tc064_aux {α : Type*}
    (S : Finset α) (x y : α → ℝ) (hx : ∀ a ∈ S, 0 ≤ x a) (hy : ∀ a ∈ S, 0 ≤ y a) :
    (∑ a ∈ S, x a * y a) ≤
      Real.sqrt (∑ a ∈ S, (x a) ^ 2) * Real.sqrt (∑ a ∈ S, (y a) ^ 2) := by
  have h_lag :
      0 ≤ ∑ a ∈ S, ∑ c ∈ S, (x a * y c - x c * y a) ^ 2 :=
    Finset.sum_nonneg (fun _ _ => Finset.sum_nonneg (fun _ _ => sq_nonneg _))
  have h_exp :
      (∑ a ∈ S, ∑ c ∈ S, (x a * y c - x c * y a) ^ 2) =
        2 * ((∑ a ∈ S, (x a) ^ 2) * (∑ c ∈ S, (y c) ^ 2) - (∑ a ∈ S, x a * y a) ^ 2) := by
    have h_in :
        ∀ a ∈ S,
          (∑ c ∈ S, (x a * y c - x c * y a) ^ 2) =
            (x a) ^ 2 * (∑ c ∈ S, (y c) ^ 2) -
              2 * (x a * y a) * (∑ c ∈ S, x c * y c) +
              (y a) ^ 2 * (∑ c ∈ S, (x c) ^ 2) := by
      intro a _
      have h1 :
          ∀ c ∈ S,
            (x a * y c - x c * y a) ^ 2 =
              (x a) ^ 2 * (y c) ^ 2 - 2 * (x a * y a) * (x c * y c) + (y a) ^ 2 * (x c) ^ 2 :=
        fun _ _ => by ring
      rw [Finset.sum_congr rfl h1, Finset.sum_add_distrib, Finset.sum_sub_distrib,
        ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.mul_sum]
    rw [Finset.sum_congr rfl h_in, Finset.sum_add_distrib, Finset.sum_sub_distrib,
      ← Finset.sum_mul, ← Finset.sum_mul, ← Finset.sum_mul, ← Finset.mul_sum]
    ring
  have h_sq : (∑ a ∈ S, x a * y a) ^ 2 ≤ (∑ a ∈ S, (x a) ^ 2) * (∑ a ∈ S, (y a) ^ 2) := by
    linarith
  have h_sx_nn : 0 ≤ ∑ a ∈ S, (x a) ^ 2 := Finset.sum_nonneg (fun _ _ => sq_nonneg _)
  have h_lhs_nn : 0 ≤ ∑ a ∈ S, x a * y a :=
    Finset.sum_nonneg (fun a ha => mul_nonneg (hx a ha) (hy a ha))
  rw [← Real.sqrt_mul h_sx_nn]
  calc
    (∑ a ∈ S, x a * y a)
      = Real.sqrt ((∑ a ∈ S, x a * y a) ^ 2) := (Real.sqrt_sq h_lhs_nn).symm
    _ ≤ Real.sqrt ((∑ a ∈ S, (x a) ^ 2) * (∑ a ∈ S, (y a) ^ 2)) := Real.sqrt_le_sqrt h_sq

private theorem direct_sum_window_minkowski_sq_tc064_aux {α ι : Type*} [DecidableEq ι]
    {Y : ℝ} (hY0 : 0 < Y) (S : Finset α) (I : Finset ι) (F : ι → α → ℝ → ℝ)
    (hF_cont : ∀ i ∈ I, ∀ a ∈ S, ContinuousOn (F i a) (Set.uIcc Y (RiemannScope.tau * Y))) :
    Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (fun X => ∑ i ∈ I, F i a X)) ≤
        ∑ i ∈ I, Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (F i a)) ∧
      (∑ a ∈ S, windowEnergyNormSq Y (fun X => ∑ i ∈ I, F i a X)) ≤
        (∑ i ∈ I, Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (F i a))) ^ 2 := by
  have hCg := (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2.1
  have hle : Y ≤ RiemannScope.tau * Y := by nlinarith [hCg]
  have hpos : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), 0 < X := by
    intro X hX; rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX; linarith
  have h_norm_nn : ∀ g : ℝ → ℝ, 0 ≤ windowEnergyNormSq Y g := by
    intro g
    unfold windowEnergyNormSq windowPairing
    apply intervalIntegral.integral_nonneg hle
    intro X hX; exact div_nonneg (mul_self_nonneg _) (by linarith [hX.1])
  have h_add2 :
      ∀ (U V : α → ℝ → ℝ),
        (∀ a ∈ S, ContinuousOn (U a) (Set.uIcc Y (RiemannScope.tau * Y))) →
        (∀ a ∈ S, ContinuousOn (V a) (Set.uIcc Y (RiemannScope.tau * Y))) →
          Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (fun X => U a X + V a X)) ≤
            Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (U a)) +
              Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (V a)) := by
    intro U V hU hV
    have h_each_a :
        ∀ a ∈ S,
          windowEnergyNormSq Y (fun X => U a X + V a X) ≤
            windowEnergyNormSq Y (U a) +
              2 * (Real.sqrt (windowEnergyNormSq Y (U a)) *
                Real.sqrt (windowEnergyNormSq Y (V a))) +
              windowEnergyNormSq Y (V a) := by
      intro a ha
      have hi_uu : IntervalIntegrable (fun X => U a X * U a X / X) volume Y (RiemannScope.tau * Y) := by
        apply ContinuousOn.intervalIntegrable
        exact ((hU a ha).mul (hU a ha)).div continuousOn_id (fun X hX => ne_of_gt (hpos X hX))
      have hi_uv : IntervalIntegrable (fun X => U a X * V a X / X) volume Y (RiemannScope.tau * Y) := by
        apply ContinuousOn.intervalIntegrable
        exact ((hU a ha).mul (hV a ha)).div continuousOn_id (fun X hX => ne_of_gt (hpos X hX))
      have hi_vv : IntervalIntegrable (fun X => V a X * V a X / X) volume Y (RiemannScope.tau * Y) := by
        apply ContinuousOn.intervalIntegrable
        exact ((hV a ha).mul (hV a ha)).div continuousOn_id (fun X hX => ne_of_gt (hpos X hX))
      have h_expand :
          windowEnergyNormSq Y (fun X => U a X + V a X) =
            windowEnergyNormSq Y (U a) + 2 * windowPairing Y (U a) (V a) +
              windowEnergyNormSq Y (V a) := by
        unfold windowEnergyNormSq windowPairing
        have h_pt :
            (fun X => (U a X + V a X) * (U a X + V a X) / X) =
              fun X => (U a X * U a X / X + 2 * (U a X * V a X / X)) + V a X * V a X / X := by
          ext X; ring
        rw [h_pt, intervalIntegral.integral_add (hi_uu.add (hi_uv.const_mul 2)) hi_vv,
          intervalIntegral.integral_add hi_uu (hi_uv.const_mul 2),
          intervalIntegral.integral_const_mul]
      have h_cs :=
        (((smooth_increment_window_norm_and_small_scale_tail_tc059r).2.1 hY0).1 (hU a ha) (hV a ha)).1
      have h_le_abs := le_abs_self (windowPairing Y (U a) (V a))
      linarith
    have h_sum_le := Finset.sum_le_sum h_each_a
    rw [Finset.sum_add_distrib, Finset.sum_add_distrib, ← Finset.mul_sum] at h_sum_le
    let x : α → ℝ := fun a => Real.sqrt (windowEnergyNormSq Y (U a))
    let y : α → ℝ := fun a => Real.sqrt (windowEnergyNormSq Y (V a))
    have h_cs_S :=
      finset_cauchy_schwarz_nonneg_tc064_aux S x y
        (fun _ _ => Real.sqrt_nonneg _) (fun _ _ => Real.sqrt_nonneg _)
    have hx2 : (∑ a ∈ S, (x a) ^ 2) = ∑ a ∈ S, windowEnergyNormSq Y (U a) :=
      Finset.sum_congr rfl (fun a _ => Real.sq_sqrt (h_norm_nn (U a)))
    have hy2 : (∑ a ∈ S, (y a) ^ 2) = ∑ a ∈ S, windowEnergyNormSq Y (V a) :=
      Finset.sum_congr rfl (fun a _ => Real.sq_sqrt (h_norm_nn (V a)))
    rw [hx2, hy2] at h_cs_S
    have h_sq_bd :
        (∑ a ∈ S, windowEnergyNormSq Y (fun X => U a X + V a X)) ≤
          (Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (U a)) +
            Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (V a))) ^ 2 := by
      have h_su :
          (Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (U a))) ^ 2 =
            ∑ a ∈ S, windowEnergyNormSq Y (U a) :=
        Real.sq_sqrt (Finset.sum_nonneg (fun a _ => h_norm_nn (U a)))
      have h_sv :
          (Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (V a))) ^ 2 =
            ∑ a ∈ S, windowEnergyNormSq Y (V a) :=
        Real.sq_sqrt (Finset.sum_nonneg (fun a _ => h_norm_nn (V a)))
      change (∑ a ∈ S, windowEnergyNormSq Y (fun X => U a X + V a X)) ≤ _
      dsimp [x, y] at h_cs_S
      linarith [h_sum_le, h_cs_S,
        show (Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (U a)) +
            Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (V a))) ^ 2 =
          (Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (U a))) ^ 2 +
            2 * (Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (U a)) *
              Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (V a))) +
            (Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (V a))) ^ 2 by ring]
    calc
      Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (fun X => U a X + V a X))
        ≤ Real.sqrt ((Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (U a)) +
            Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (V a))) ^ 2) := Real.sqrt_le_sqrt h_sq_bd
      _ = Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (U a)) +
            Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (V a)) :=
          Real.sqrt_sq (add_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _))
  have h_sqrt_mink :
      Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (fun X => ∑ i ∈ I, F i a X)) ≤
        ∑ i ∈ I, Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (F i a)) := by
    induction I using Finset.induction_on with
    | empty =>
      simp [windowEnergyNormSq, windowPairing]
    | @insert i0 I' hi0 ih =>
      have h_cont_i0 : ∀ a ∈ S, ContinuousOn (F i0 a) (Set.uIcc Y (RiemannScope.tau * Y)) :=
        fun a ha => hF_cont i0 (Finset.mem_insert_self i0 I') a ha
      have h_cont_I' :
          ∀ a ∈ S, ContinuousOn (fun X => ∑ i ∈ I', F i a X) (Set.uIcc Y (RiemannScope.tau * Y)) :=
        fun a ha => continuousOn_finset_sum I'
          (fun i hi => hF_cont i (Finset.mem_insert_of_mem hi) a ha)
      have h_ins_fn :
          (fun a => windowEnergyNormSq Y (fun X => ∑ i ∈ insert i0 I', F i a X)) =
            fun a => windowEnergyNormSq Y (fun X => F i0 a X + ∑ i ∈ I', F i a X) := by
        ext a; simp only [Finset.sum_insert hi0]
      rw [Finset.sum_congr rfl (fun a _ => congr_fun h_ins_fn a), Finset.sum_insert hi0]
      exact le_trans (h_add2 (F i0) (fun a X => ∑ i ∈ I', F i a X) h_cont_i0 h_cont_I')
        (add_le_add_left (ih (fun i hi => hF_cont i (Finset.mem_insert_of_mem hi))) _)
  refine ⟨h_sqrt_mink, ?_⟩
  have h_lhs_nn : 0 ≤ ∑ a ∈ S, windowEnergyNormSq Y (fun X => ∑ i ∈ I, F i a X) :=
    Finset.sum_nonneg (fun a _ => h_norm_nn _)
  have hp := pow_le_pow_left (Real.sqrt_nonneg _) h_sqrt_mink 2
  rwa [Real.sq_sqrt h_lhs_nn] at hp

private theorem weighted_gaussian_sum_window_norm_le_tc064_aux
    {Y : ℝ} (hY0 : 0 < Y) (U : Finset ℕ) (w : ℕ → ℝ) {B : ℝ} (_hB_nn : 0 ≤ B)
    (hw_le : ∀ k ∈ U, |w k| ≤ B) :
    windowEnergyNormSq Y (fun X => ∑ k ∈ U, w k * gaussianTermPhi k X) ≤
      B ^ 2 * (∑ k ∈ U, Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi k))) ^ 2 := by
  have hCg := (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2.1
  have hle : Y ≤ RiemannScope.tau * Y := by nlinarith [hCg]
  have hpos : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), 0 < X := by
    intro X hX; rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX; linarith
  have hc_phi : ∀ k : ℕ, ContinuousOn (gaussianTermPhi k) (Set.uIcc Y (RiemannScope.tau * Y)) :=
    continuousOn_gaussianTermPhi_param_tc064_aux Y RiemannScope.tau
  let H : ℝ → ℝ := fun X => ∑ k ∈ U, w k * gaussianTermPhi k X
  let G : ℝ → ℝ := fun X => ∑ k ∈ U, gaussianTermPhi k X
  have hc_H : ContinuousOn H (Set.uIcc Y (RiemannScope.tau * Y)) :=
    continuousOn_finset_sum U (fun k _ => continuousOn_const.mul (hc_phi k))
  have hc_G : ContinuousOn G (Set.uIcc Y (RiemannScope.tau * Y)) :=
    continuousOn_finset_sum U (fun k _ => hc_phi k)
  have hi_H : IntervalIntegrable (fun X => H X * H X / X) volume Y (RiemannScope.tau * Y) := by
    apply ContinuousOn.intervalIntegrable
    exact (hc_H.mul hc_H).div continuousOn_id (fun X hX => ne_of_gt (hpos X hX))
  have hi_G : IntervalIntegrable (fun X => B ^ 2 * (G X * G X / X)) volume Y (RiemannScope.tau * Y) := by
    apply ContinuousOn.intervalIntegrable
    exact continuousOn_const.mul
      ((hc_G.mul hc_G).div continuousOn_id (fun X hX => ne_of_gt (hpos X hX)))
  have h_HG : windowEnergyNormSq Y H ≤ B ^ 2 * windowEnergyNormSq Y G := by
    unfold windowEnergyNormSq windowPairing
    rw [← intervalIntegral.integral_const_mul]
    apply intervalIntegral.integral_mono_on hle hi_H hi_G
    intro X hX
    have hX_pos : 0 < X := lt_of_lt_of_le hY0 hX.1
    have hphi_nn : ∀ k : ℕ, 0 ≤ gaussianTermPhi k X := by
      intro k; unfold gaussianTermPhi; positivity
    have habs : |H X| ≤ B * G X := by
      dsimp [H, G]
      rw [Finset.mul_sum]
      calc
        |∑ k ∈ U, w k * gaussianTermPhi k X|
          ≤ ∑ k ∈ U, |w k * gaussianTermPhi k X| := Finset.abs_sum_le_sum_abs _ _
        _ ≤ ∑ k ∈ U, B * gaussianTermPhi k X := by
            apply Finset.sum_le_sum
            intro k hk
            rw [abs_mul, abs_of_nonneg (hphi_nn k)]
            exact mul_le_mul_of_nonneg_right (hw_le k hk) (hphi_nn k)
    have hsq : H X * H X ≤ B ^ 2 * (G X * G X) := by
      have hp := pow_le_pow_left (abs_nonneg _) habs 2
      rw [sq_abs] at hp
      linarith [hp, show (B * G X) ^ 2 = B ^ 2 * (G X * G X) by ring,
        show (H X) ^ 2 = H X * H X by ring]
    calc
      H X * H X / X ≤ (B ^ 2 * (G X * G X)) / X := div_le_div_of_nonneg_right hsq (le_of_lt hX_pos)
      _ = B ^ 2 * (G X * G X / X) := by ring
  have h_mink_G :=
    (direct_sum_window_minkowski_sq_tc064_aux hY0 ({0} : Finset ℕ) U
      (fun k _ X => gaussianTermPhi k X) (fun k _ _ _ => hc_phi k)).2
  simp only [Finset.sum_singleton] at h_mink_G
  exact le_trans h_HG (mul_le_mul_of_nonneg_left h_mink_G (sq_nonneg B))

private theorem log_sq_inv_windowEnergy_le_tc064_aux
    {Y : ℝ} (hY2 : 2 ≤ Y) {h : ℝ → ℝ}
    (hh_cont : ContinuousOn h (Set.uIcc Y (RiemannScope.tau * Y))) :
    windowEnergyNormSq Y (fun X => (1 / (Real.log X) ^ 2) * h X) ≤
      (1 / (Real.log Y) ^ 4) * windowEnergyNormSq Y h := by
  obtain ⟨hle, hprops⟩ := uIcc_tau_log_props_tc064_aux hY2
  have hlogY_pos : 0 < Real.log Y := Real.log_pos (by linarith)
  have hlog_cont : ContinuousOn Real.log (Set.uIcc Y (RiemannScope.tau * Y)) :=
    ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hprops X hX).1)
  have hc_lhs : ContinuousOn (fun X => (1 / (Real.log X) ^ 2) * h X)
      (Set.uIcc Y (RiemannScope.tau * Y)) :=
    (continuousOn_const.div (hlog_cont.pow 2) (fun X hX => (hprops X hX).2.2.2)).mul hh_cont
  have hi_lhs :
      IntervalIntegrable
        (fun X => ((1 / (Real.log X) ^ 2) * h X) * ((1 / (Real.log X) ^ 2) * h X) / X)
        volume Y (RiemannScope.tau * Y) := by
    apply ContinuousOn.intervalIntegrable
    exact (hc_lhs.mul hc_lhs).div continuousOn_id (fun X hX => ne_of_gt (hprops X hX).1)
  have hi_rhs :
      IntervalIntegrable
        (fun X => (1 / (Real.log Y) ^ 4) * (h X * h X / X))
        volume Y (RiemannScope.tau * Y) := by
    apply ContinuousOn.intervalIntegrable
    exact continuousOn_const.mul
      ((hh_cont.mul hh_cont).div continuousOn_id (fun X hX => ne_of_gt (hprops X hX).1))
  unfold windowEnergyNormSq windowPairing
  rw [← intervalIntegral.integral_const_mul]
  apply intervalIntegral.integral_mono_on hle hi_lhs hi_rhs
  intro X hX
  have hX_pos : 0 < X := by linarith [hX.1]
  have hlog_ge : Real.log Y ≤ Real.log X := Real.log_le_log (by linarith) hX.1
  have h4_le : (Real.log Y) ^ 4 ≤ (Real.log X) ^ 4 :=
    pow_le_pow_left (le_of_lt hlogY_pos) hlog_ge 4
  have h_inv4 : 1 / (Real.log X) ^ 4 ≤ 1 / (Real.log Y) ^ 4 :=
    one_div_le_one_div_of_le (pow_pos hlogY_pos 4) h4_le
  have h_num :
      ((1 / (Real.log X) ^ 2) * h X) * ((1 / (Real.log X) ^ 2) * h X) ≤
        (1 / (Real.log Y) ^ 4) * (h X * h X) := by
    calc
      ((1 / (Real.log X) ^ 2) * h X) * ((1 / (Real.log X) ^ 2) * h X)
        = (1 / (Real.log X) ^ 4) * (h X * h X) := by ring
      _ ≤ (1 / (Real.log Y) ^ 4) * (h X * h X) :=
          mul_le_mul_of_nonneg_right h_inv4 (mul_self_nonneg _)
  calc
    ((1 / (Real.log X) ^ 2) * h X) * ((1 / (Real.log X) ^ 2) * h X) / X
      ≤ ((1 / (Real.log Y) ^ 4) * (h X * h X)) / X :=
        div_le_div_of_nonneg_right h_num (le_of_lt hX_pos)
    _ = (1 / (Real.log Y) ^ 4) * (h X * h X / X) := by ring

private theorem paired_core_station_set_and_divisor_norm_tc064_aux :
    let C_tau : ℝ :=
      (16 / 5 : ℝ) * (2 + Real.sqrt 2) * RiemannScope.tau ^ (5 / 2 : ℝ) *
        Real.sqrt (Real.log RiemannScope.tau)
    let S_st : ℕ → ℕ → Finset ℕ := fun T a =>
      (coreSquareMultipliers a T).biUnion (fun b =>
        (dyadicChainExponents (a * b ^ 2) T).biUnion (fun j =>
          (Finset.range 2).image (fun eps => 2 ^ (2 * j + eps) * a * b ^ 2)))
    0 < C_tau ∧
      (∀ (T : ℕ), ∀ a ∈ oddSquarefreeCores T,
        S_st T a ⊆
            (Finset.Icc 1 T).filter (fun k => ∃ r b' : ℕ, Odd b' ∧ k = 2 ^ r * a * b' ^ 2) ∧
          (∀ k ∈ S_st T a, IsSquare k → a = 1) ∧
          (∀ w : ℕ → ℝ,
            (∑ b ∈ coreSquareMultipliers a T,
              ∑ j ∈ dyadicChainExponents (a * b ^ 2) T,
                (w (4 ^ j * (a * b ^ 2)) - w (2 * (4 ^ j * (a * b ^ 2))))) =
              ∑ k ∈ S_st T a, (-1 : ℝ) ^ (k.factorization 2) * w k)) ∧
      (∀ (T : ℕ), ∀ a1 ∈ oddSquarefreeCores T, ∀ a2 ∈ oddSquarefreeCores T,
        a1 ≠ a2 → Disjoint (S_st T a1) (S_st T a2)) ∧
      (∀ {Y : ℝ}, 0 < Y → ∀ (T : ℕ), ∀ a ∈ oddSquarefreeCores T,
        (∑ k ∈ S_st T a, Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi k))) ≤
          C_tau / Real.sqrt (a : ℝ)) ∧
      (∀ {Y : ℝ}, 0 < Y → ∀ {T e : ℕ}, 1 ≤ e → e ≤ T →
        ∀ (w : ℕ → ℝ), (∀ k : ℕ, |w k| ≤ 1) →
          Real.sqrt
              (∑ a ∈ oddSquarefreeCores T,
                windowEnergyNormSq Y
                  (fun X => ∑ k ∈ (S_st T a).filter (fun k => e ∣ k),
                    w k * gaussianTermPhi k X)) ≤
            C_tau * (1 / Real.sqrt (e : ℝ)) * Real.sqrt (1 + Real.log (T : ℝ))) := by
  intro C_tau S_st
  have hCg := (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2.1
  have htau_gt1 : (1 : ℝ) < RiemannScope.tau := by linarith
  have hCtau_pos : 0 < C_tau := by
    dsimp [C_tau]
    have hlog : 0 < Real.log RiemannScope.tau := Real.log_pos htau_gt1
    positivity
  obtain ⟨h_inj4, h_mem4⟩ := paired_station_injective_and_mem_tc064_aux
  have h_k_le_pow2 : ∀ r : ℕ, r < 2 ^ r := by
    intro r
    induction r with
    | zero => norm_num
    | succ r ih =>
      have hp : 1 ≤ 2 ^ r := Nat.one_le_pow r 2 (by decide)
      omega
  have h_partA :
      ∀ (T : ℕ), ∀ a ∈ oddSquarefreeCores T,
        S_st T a ⊆
            (Finset.Icc 1 T).filter (fun k => ∃ r b' : ℕ, Odd b' ∧ k = 2 ^ r * a * b' ^ 2) ∧
          (∀ k ∈ S_st T a, IsSquare k → a = 1) ∧
          (∀ w : ℕ → ℝ,
            (∑ b ∈ coreSquareMultipliers a T,
              ∑ j ∈ dyadicChainExponents (a * b ^ 2) T,
                (w (4 ^ j * (a * b ^ 2)) - w (2 * (4 ^ j * (a * b ^ 2))))) =
              ∑ k ∈ S_st T a, (-1 : ℝ) ^ (k.factorization 2) * w k) := by
    intro T a ha
    have ha_f := Finset.mem_filter.mp ha
    have ha1 : 1 ≤ a := (Finset.mem_Icc.mp ha_f.1).1
    have ha_o : Odd a := ha_f.2.1
    have ha_sf : Squarefree a := ha_f.2.2.1
    have h_sub :
        S_st T a ⊆
          (Finset.Icc 1 T).filter (fun k => ∃ r b' : ℕ, Odd b' ∧ k = 2 ^ r * a * b' ^ 2) := by
      intro k hk
      dsimp only [S_st] at hk
      simp only [Finset.mem_biUnion, Finset.mem_image, Finset.mem_range] at hk
      rcases hk with ⟨b, hb, j, hj, eps, heps, rfl⟩
      exact h_mem4 T a ha b hb j hj heps
    have h_sq_a1 : ∀ k ∈ S_st T a, IsSquare k → a = 1 := by
      intro k hk hsq
      have hk_m := Finset.mem_filter.mp (h_sub hk)
      obtain ⟨hk_Icc, ⟨r, b, hb_o, hk_eq⟩⟩ := hk_m
      obtain ⟨hk1, _⟩ := Finset.mem_Icc.mp hk_Icc
      subst hk_eq
      by_contra ha_ne1
      let p := Nat.minFac a
      have hp_pr : p.Prime := Nat.minFac_prime ha_ne1
      have hp_dvd_a : p ∣ a := Nat.minFac_dvd a
      have hp_ne2 : p ≠ 2 := by
        intro hp2
        rw [hp2] at hp_dvd_a
        exact (Nat.odd_iff_not_even.mp ha_o) (even_iff_two_dvd.mpr hp_dvd_a)
      have ha_ne0 : a ≠ 0 := by omega
      have hb_ne0 : b ≠ 0 := ne_of_gt hb_o.pos
      have hap_ge1 : 1 ≤ a.factorization p :=
        (hp_pr.pow_dvd_iff_le_factorization ha_ne0).mp (by simpa using hp_dvd_a)
      have hap_le1 : a.factorization p ≤ 1 :=
        (Nat.squarefree_iff_factorization_le_one ha_ne0).mp ha_sf p
      have h2_not_p : ¬ p ∣ 2 ^ r := fun hd => hp_ne2 (Nat.le_antisymm
        (Nat.le_of_dvd (by decide) (hp_pr.dvd_of_dvd_pow hd)) hp_pr.two_le)
      have hf_lhs : (2 ^ r * a * b ^ 2).factorization p = 1 + 2 * b.factorization p := by
        rw [Nat.factorization_mul (mul_ne_zero (pow_ne_zero r (by decide)) ha_ne0)
            (pow_ne_zero 2 hb_ne0),
          Nat.factorization_mul (pow_ne_zero r (by decide)) ha_ne0,
          Finsupp.add_apply, Finsupp.add_apply,
          Nat.factorization_eq_zero_of_not_dvd h2_not_p, Nat.factorization_pow,
          Finsupp.smul_apply, smul_eq_mul]
        omega
      obtain ⟨m, hm_eq⟩ := hsq
      have hm_ne0 : m ≠ 0 := by intro hm0; rw [hm0, mul_zero] at hm_eq; omega
      have hf_rhs : (2 ^ r * a * b ^ 2).factorization p = 2 * m.factorization p := by
        rw [hm_eq, Nat.factorization_mul hm_ne0 hm_ne0, Finsupp.add_apply]
        omega
      omega
    refine ⟨h_sub, h_sq_a1, ?_⟩
    intro w
    dsimp only [S_st]
    have h_disj_b :
        (coreSquareMultipliers a T : Set ℕ).PairwiseDisjoint
          (fun b => (dyadicChainExponents (a * b ^ 2) T).biUnion
            (fun j => (Finset.range 2).image (fun eps => 2 ^ (2 * j + eps) * a * b ^ 2))) := by
      intro b1 hb1 b2 hb2 hb_ne
      change Disjoint _ _
      rw [Finset.disjoint_left]
      intro k hk1 hk2
      simp only [Finset.mem_biUnion, Finset.mem_image, Finset.mem_range] at hk1 hk2
      rcases hk1 with ⟨j1, _, e1, he1, rfl⟩
      rcases hk2 with ⟨j2, _, e2, he2, h_eq⟩
      have hb1_o : Odd b1 := (Finset.mem_filter.mp hb1).2.1
      have hb2_o : Odd b2 := (Finset.mem_filter.mp hb2).2.1
      exact hb_ne ((h_inj4 ha_o ha_sf hb1_o he1 ha_o ha_sf hb2_o he2).mp h_eq.symm).2.1
    rw [Finset.sum_biUnion h_disj_b]
    apply Finset.sum_congr rfl
    intro b hb
    have hb_o : Odd b := (Finset.mem_filter.mp hb).2.1
    have hu_o : Odd (a * b ^ 2) := ha_o.mul hb_o.pow
    have h_disj_j :
        (dyadicChainExponents (a * b ^ 2) T : Set ℕ).PairwiseDisjoint
          (fun j => (Finset.range 2).image (fun eps => 2 ^ (2 * j + eps) * a * b ^ 2)) := by
      intro j1 _ j2 _ hj_ne
      change Disjoint _ _
      rw [Finset.disjoint_left]
      intro k hk1 hk2
      simp only [Finset.mem_image, Finset.mem_range] at hk1 hk2
      rcases hk1 with ⟨e1, he1, rfl⟩
      rcases hk2 with ⟨e2, he2, h_eq⟩
      exact hj_ne ((h_inj4 ha_o ha_sf hb_o he1 ha_o ha_sf hb_o he2).mp h_eq.symm).2.2.1
    rw [Finset.sum_biUnion h_disj_j]
    apply Finset.sum_congr rfl
    intro j _
    have h_inj_e : Set.InjOn (fun eps => 2 ^ (2 * j + eps) * a * b ^ 2) ↑(Finset.range 2) := by
      intro e1 he1 e2 he2 h_eq
      exact ((h_inj4 ha_o ha_sf hb_o (Finset.mem_range.mp he1)
        ha_o ha_sf hb_o (Finset.mem_range.mp he2)).mp h_eq).2.2.2
    rw [Finset.sum_image h_inj_e, Finset.sum_range_succ, Finset.sum_range_one]
    dsimp only
    have h4 : (4 : ℕ) ^ j = 2 ^ (2 * j) := by
      rw [show (4 : ℕ) = 2 ^ 2 by norm_num, ← pow_mul]
    have hk0 : 2 ^ (2 * j + 0) * a * b ^ 2 = 2 ^ (2 * j) * (a * b ^ 2) := by ring
    have hk1 : 2 ^ (2 * j + 1) * a * b ^ 2 = 2 ^ (2 * j + 1) * (a * b ^ 2) := by ring
    have hf0 : (2 ^ (2 * j + 0) * a * b ^ 2).factorization 2 = 2 * j := by
      rw [hk0, two_pow_mul_odd_factorization_two_tc064_aux (2 * j) hu_o]
    have hf1 : (2 ^ (2 * j + 1) * a * b ^ 2).factorization 2 = 2 * j + 1 := by
      rw [hk1, two_pow_mul_odd_factorization_two_tc064_aux (2 * j + 1) hu_o]
    have hm0 : 2 ^ (2 * j + 0) * a * b ^ 2 = 4 ^ j * (a * b ^ 2) := by rw [h4]; ring
    have hm1 : 2 ^ (2 * j + 1) * a * b ^ 2 = 2 * (4 ^ j * (a * b ^ 2)) := by
      rw [h4, pow_add, pow_one]; ring
    rw [hf0, hf1, hm0, hm1, pow_mul, show (-1 : ℝ) ^ 2 = 1 by norm_num, one_pow,
      pow_add, pow_mul, show (-1 : ℝ) ^ 2 = 1 by norm_num, one_pow, pow_one]
    ring
  have h_disj_a :
      ∀ (T : ℕ), ∀ a1 ∈ oddSquarefreeCores T, ∀ a2 ∈ oddSquarefreeCores T,
        a1 ≠ a2 → Disjoint (S_st T a1) (S_st T a2) := by
    intro T a1 ha1 a2 ha2 h_ne
    rw [Finset.disjoint_left]
    intro k hk1 hk2
    dsimp only [S_st] at hk1 hk2
    simp only [Finset.mem_biUnion, Finset.mem_image, Finset.mem_range] at hk1 hk2
    rcases hk1 with ⟨b1, hb1, j1, _, e1, he1, rfl⟩
    rcases hk2 with ⟨b2, hb2, j2, _, e2, he2, h_eq⟩
    have f1 := Finset.mem_filter.mp ha1
    have f2 := Finset.mem_filter.mp ha2
    exact h_ne ((h_inj4 f1.2.1 f1.2.2.1 (Finset.mem_filter.mp hb1).2.1 he1
      f2.2.1 f2.2.2.1 (Finset.mem_filter.mp hb2).2.1 he2).mp h_eq.symm).1
  have h_bare_a :
      ∀ {Y : ℝ}, 0 < Y → ∀ (T : ℕ), ∀ a ∈ oddSquarefreeCores T,
        (∑ k ∈ S_st T a, Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi k))) ≤
          C_tau / Real.sqrt (a : ℝ) := by
    intro Y hY0 T a ha
    have ha1 : 1 ≤ a := (Finset.mem_Icc.mp (Finset.mem_filter.mp ha).1).1
    have h_sub := (h_partA T a ha).1
    let P := Finset.range (T + 1) ×ˢ Finset.Icc 1 T
    have h_cov :
        ∀ k ∈ S_st T a, ∃ rl ∈ P, 2 ^ rl.1 * a * rl.2 ^ 2 = k := by
      intro k hk
      have hk_f := Finset.mem_filter.mp (h_sub hk)
      obtain ⟨hk_Icc, ⟨r, b, hb_o, hk_eq⟩⟩ := hk_f
      obtain ⟨hk1, hkT⟩ := Finset.mem_Icc.mp hk_Icc
      subst hk_eq
      have hb1 : 1 ≤ b := hb_o.pos
      have hr_le_T : r < T + 1 := by
        have h2r : 2 ^ r ≤ 2 ^ r * a * b ^ 2 := by
          calc
            2 ^ r = 2 ^ r * 1 * 1 := by ring
            _ ≤ 2 ^ r * a * 1 := Nat.mul_le_mul_right 1 (Nat.mul_le_mul_left _ ha1)
            _ ≤ 2 ^ r * a * b ^ 2 := Nat.mul_le_mul_left _ (pow_pos hb_o.pos 2)
        have hr_lt := h_k_le_pow2 r
        omega
      have hb_le_T : b ≤ T := by
        have hb2 : b ≤ b ^ 2 := by rw [sq]; exact Nat.le_mul_of_pos_left b hb1
        have hb_k : b ^ 2 ≤ 2 ^ r * a * b ^ 2 :=
          Nat.le_mul_of_pos_left _ (Nat.mul_pos (pow_pos (by decide) r) ha1)
        omega
      exact ⟨(r, b), Finset.mem_product.mpr ⟨Finset.mem_range.mpr hr_le_T,
        Finset.mem_Icc.mpr ⟨hb1, hb_le_T⟩⟩, rfl⟩
    calc
      (∑ k ∈ S_st T a, Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi k)))
        ≤ ∑ rl ∈ P, Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi (2 ^ rl.1 * a * rl.2 ^ 2))) :=
          sum_subset_image_le_sum_tc064_aux P (S_st T a) (fun rl => 2 ^ rl.1 * a * rl.2 ^ 2)
            (fun k => Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi k)))
            (fun _ => Real.sqrt_nonneg _) h_cov
      _ = ∑ r ∈ Finset.range (T + 1), ∑ l ∈ Finset.Icc 1 T,
            Real.sqrt (paramWindowNormSq Y RiemannScope.tau
              (gaussianTermPhi (2 ^ r * a * l ^ 2))) := by
          dsimp [P]; rw [Finset.sum_product]; rfl
      _ ≤ C_tau / Real.sqrt (a : ℝ) :=
          square_support_gaussian_norm_sum_tc064_aux htau_gt1 hY0 ha1 T T
  refine ⟨hCtau_pos, h_partA, h_disj_a, h_bare_a, ?_⟩
  intro Y hY0 T e he1 heT w hw_abs
  have hT1 : 1 ≤ T := le_trans he1 heT
  let s := e.factorization 2
  let m_odd := e / 2 ^ s
  have he_ne0 : e ≠ 0 := by omega
  have h2s_dvd : 2 ^ s ∣ e :=
    (Nat.prime_two.pow_dvd_iff_le_factorization he_ne0).mpr (le_refl s)
  have he_2sm : 2 ^ s * m_odd = e := Nat.mul_div_cancel' h2s_dvd
  have hm_odd : Odd m_odd := by
    rw [Nat.odd_iff_not_even, even_iff_two_dvd]
    intro h2m
    have hs1 : 2 ^ (s + 1) ∣ e := by
      rw [← he_2sm, pow_succ]
      exact Nat.mul_dvd_mul_left (2 ^ s) h2m
    have hle : s + 1 ≤ s :=
      (Nat.prime_two.pow_dvd_iff_le_factorization he_ne0).mp hs1
    omega
  obtain ⟨⟨c, f⟩, ⟨hc_o, hc_sf, hf_o, hcf_eq⟩, _⟩ :=
    unique_odd_squarefree_mul_sq_tc064_aux hm_odd
  have he_rep : e = 2 ^ s * c * f ^ 2 := by
    calc
      e = 2 ^ s * m_odd := he_2sm.symm
      _ = 2 ^ s * (c * f ^ 2) := by rw [← hcf_eq]
      _ = 2 ^ s * c * f ^ 2 := by ring
  let S_act := (oddSquarefreeCores T).filter (fun a => e * squarefreeCoreStar a c ≤ T)
  have h_each_a :
      ∀ a ∈ oddSquarefreeCores T,
        windowEnergyNormSq Y
            (fun X => ∑ k ∈ (S_st T a).filter (fun k => e ∣ k), w k * gaussianTermPhi k X) ≤
          if e * squarefreeCoreStar a c ≤ T then
            (C_tau ^ 2 / (e : ℝ)) * ((1 : ℝ) / (squarefreeCoreStar a c : ℝ))
          else 0 := by
    intro a ha
    have ha_f := Finset.mem_filter.mp ha
    have ha_o : Odd a := ha_f.2.1
    have ha_sf : Squarefree a := ha_f.2.2.1
    have h_st_pos : 1 ≤ squarefreeCoreStar a c :=
      (squarefreeCoreStar_props_tc064_aux ha_o ha_sf hc_o hc_sf).1.2.2
    have h_sub_a := (h_partA T a ha).1
    by_cases h_act : e * squarefreeCoreStar a c ≤ T
    · rw [if_pos h_act]
      let M := e * squarefreeCoreStar a c
      have hM1 : 1 ≤ M := Nat.mul_pos he1 h_st_pos
      let P := Finset.range (T + 1) ×ˢ Finset.Icc 1 T
      have h_cov :
          ∀ k ∈ (S_st T a).filter (fun k => e ∣ k),
            ∃ ql ∈ P, 2 ^ ql.1 * M * ql.2 ^ 2 = k := by
        intro k hk
        obtain ⟨hk_S, he_dvd⟩ := Finset.mem_filter.mp hk
        obtain ⟨hk_Icc, h_ex_rb⟩ := Finset.mem_filter.mp (h_sub_a hk_S)
        obtain ⟨hk1, hkT⟩ := Finset.mem_Icc.mp hk_Icc
        obtain ⟨⟨q, l⟩, ⟨hl_o, hql_eq⟩, _⟩ :=
          (divisor_core_support_bijection_tc064_aux he_rep hc_o hc_sf hf_o ha_o ha_sf hk1).mp
            ⟨h_ex_rb, he_dvd⟩
        have hl1 : 1 ≤ l := hl_o.pos
        have hM_eq : 2 ^ q * M * l ^ 2 = k := by
          dsimp [M]
          linarith [show 2 ^ q * (e * squarefreeCoreStar a c) * l ^ 2 =
            2 ^ q * e * squarefreeCoreStar a c * l ^ 2 by ring, hql_eq]
        have hq_lt : q < T + 1 := by
          have h2q : 2 ^ q ≤ k := by
            rw [← hM_eq]
            calc
              2 ^ q = 2 ^ q * 1 * 1 := by ring
              _ ≤ 2 ^ q * M * 1 := Nat.mul_le_mul_right 1 (Nat.mul_le_mul_left _ hM1)
              _ ≤ 2 ^ q * M * l ^ 2 := Nat.mul_le_mul_left _ (pow_pos hl_o.pos 2)
          have hq_2q := h_k_le_pow2 q
          omega
        have hl_le : l ≤ T := by
          have hl2 : l ≤ l ^ 2 := by rw [sq]; exact Nat.le_mul_of_pos_left l hl1
          have hlk : l ^ 2 ≤ k := by
            rw [← hM_eq]
            exact Nat.le_mul_of_pos_left _ (Nat.mul_pos (pow_pos (by decide) q) hM1)
          omega
        exact ⟨(q, l), Finset.mem_product.mpr ⟨Finset.mem_range.mpr hq_lt,
          Finset.mem_Icc.mpr ⟨hl1, hl_le⟩⟩, hM_eq⟩
      have h_w_bd :=
        weighted_gaussian_sum_window_norm_le_tc064_aux hY0 ((S_st T a).filter (fun k => e ∣ k)) w
          (by norm_num : (0 : ℝ) ≤ 1) (fun k _ => hw_abs k)
      have h_sum_phi :
          (∑ k ∈ (S_st T a).filter (fun k => e ∣ k),
              Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi k))) ≤
            C_tau / Real.sqrt (M : ℝ) := by
        calc
          (∑ k ∈ (S_st T a).filter (fun k => e ∣ k),
              Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi k)))
            ≤ ∑ ql ∈ P, Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi (2 ^ ql.1 * M * ql.2 ^ 2))) :=
              sum_subset_image_le_sum_tc064_aux P ((S_st T a).filter (fun k => e ∣ k))
                (fun ql => 2 ^ ql.1 * M * ql.2 ^ 2)
                (fun k => Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi k)))
                (fun _ => Real.sqrt_nonneg _) h_cov
          _ = ∑ q ∈ Finset.range (T + 1), ∑ l ∈ Finset.Icc 1 T,
                Real.sqrt (paramWindowNormSq Y RiemannScope.tau
                  (gaussianTermPhi (2 ^ q * M * l ^ 2))) := by
              dsimp [P]; rw [Finset.sum_product]; rfl
          _ ≤ C_tau / Real.sqrt (M : ℝ) :=
              square_support_gaussian_norm_sum_tc064_aux htau_gt1 hY0 hM1 T T
      have h_sq := pow_le_pow_left
        (Finset.sum_nonneg (fun _ _ => Real.sqrt_nonneg _)) h_sum_phi 2
      have hM_pos : (0 : ℝ) < (M : ℝ) := Nat.cast_pos.mpr hM1
      have he_pos : (0 : ℝ) < (e : ℝ) := Nat.cast_pos.mpr he1
      have hst_pos_r : (0 : ℝ) < (squarefreeCoreStar a c : ℝ) := Nat.cast_pos.mpr h_st_pos
      calc
        windowEnergyNormSq Y
            (fun X => ∑ k ∈ (S_st T a).filter (fun k => e ∣ k), w k * gaussianTermPhi k X)
          ≤ 1 ^ 2 * (C_tau / Real.sqrt (M : ℝ)) ^ 2 := by linarith
        _ = C_tau ^ 2 / (M : ℝ) := by
            rw [one_pow, one_mul, div_pow, Real.sq_sqrt (le_of_lt hM_pos)]
        _ = (C_tau ^ 2 / (e : ℝ)) * ((1 : ℝ) / (squarefreeCoreStar a c : ℝ)) := by
            dsimp [M]; push_cast
            field_simp [ne_of_gt he_pos, ne_of_gt hst_pos_r]
    · rw [if_neg h_act]
      have hemp : (S_st T a).filter (fun k => e ∣ k) = ∅ := by
        ext k
        simp only [Finset.mem_filter, Finset.not_mem_empty, iff_false]
        rintro ⟨hk_S, he_dvd⟩
        obtain ⟨hk_Icc, h_ex_rb⟩ := Finset.mem_filter.mp (h_sub_a hk_S)
        obtain ⟨hk1, hkT⟩ := Finset.mem_Icc.mp hk_Icc
        obtain ⟨⟨q, l⟩, ⟨hl_o, hql_eq⟩, _⟩ :=
          (divisor_core_support_bijection_tc064_aux he_rep hc_o hc_sf hf_o ha_o ha_sf hk1).mp
            ⟨h_ex_rb, he_dvd⟩
        dsimp only at hl_o hql_eq
        apply h_act
        have h1 : e * squarefreeCoreStar a c ≤ 2 ^ q * e * squarefreeCoreStar a c * l ^ 2 := by
          calc
            e * squarefreeCoreStar a c = 1 * (e * squarefreeCoreStar a c) * 1 := by ring
            _ ≤ 2 ^ q * (e * squarefreeCoreStar a c) * 1 :=
                Nat.mul_le_mul_right 1
                  (Nat.mul_le_mul_right _ (Nat.one_le_pow q 2 (by decide)))
            _ ≤ 2 ^ q * (e * squarefreeCoreStar a c) * l ^ 2 :=
                Nat.mul_le_mul_left _ (pow_pos hl_o.pos 2)
            _ = 2 ^ q * e * squarefreeCoreStar a c * l ^ 2 := by ring
        omega
      rw [hemp]
      simp [windowEnergyNormSq, windowPairing]
  have h_harm :=
    (divisor_core_star_involution_and_support_bijection_tc064).2.2 he1 heT he_rep hc_o hc_sf hf_o
  have he_pos_r : (0 : ℝ) < (e : ℝ) := Nat.cast_pos.mpr he1
  have hlogT_nn : 0 ≤ 1 + Real.log (T : ℝ) :=
    add_nonneg zero_le_one (Real.log_nonneg (by exact_mod_cast hT1))
  have h_sum_le :
      (∑ a ∈ oddSquarefreeCores T,
          windowEnergyNormSq Y
            (fun X => ∑ k ∈ (S_st T a).filter (fun k => e ∣ k), w k * gaussianTermPhi k X)) ≤
        (C_tau * (1 / Real.sqrt (e : ℝ)) * Real.sqrt (1 + Real.log (T : ℝ))) ^ 2 := by
    calc
      (∑ a ∈ oddSquarefreeCores T,
          windowEnergyNormSq Y
            (fun X => ∑ k ∈ (S_st T a).filter (fun k => e ∣ k), w k * gaussianTermPhi k X))
        ≤ ∑ a ∈ oddSquarefreeCores T,
            (if e * squarefreeCoreStar a c ≤ T then
              (C_tau ^ 2 / (e : ℝ)) * ((1 : ℝ) / (squarefreeCoreStar a c : ℝ))
            else 0) := Finset.sum_le_sum h_each_a
      _ = (C_tau ^ 2 / (e : ℝ)) *
            (∑ a ∈ S_act, (1 : ℝ) / (squarefreeCoreStar a c : ℝ)) := by
          dsimp [S_act]; rw [← Finset.sum_filter, ← Finset.mul_sum]
      _ ≤ (C_tau ^ 2 / (e : ℝ)) * (1 + Real.log (T : ℝ)) :=
          mul_le_mul_of_nonneg_left h_harm.1 (by positivity)
      _ = (C_tau * (1 / Real.sqrt (e : ℝ)) * Real.sqrt (1 + Real.log (T : ℝ))) ^ 2 := by
          symm
          rw [mul_pow, mul_pow, one_div_pow, Real.sq_sqrt (le_of_lt he_pos_r),
            Real.sq_sqrt hlogT_nn]
          ring
  calc
    Real.sqrt
        (∑ a ∈ oddSquarefreeCores T,
          windowEnergyNormSq Y
            (fun X => ∑ k ∈ (S_st T a).filter (fun k => e ∣ k), w k * gaussianTermPhi k X))
      ≤ Real.sqrt ((C_tau * (1 / Real.sqrt (e : ℝ)) * Real.sqrt (1 + Real.log (T : ℝ))) ^ 2) :=
        Real.sqrt_le_sqrt h_sum_le
    _ = C_tau * (1 / Real.sqrt (e : ℝ)) * Real.sqrt (1 + Real.log (T : ℝ)) :=
        Real.sqrt_sq (by positivity)

private theorem openCoreAdjustedCoeffBeta_interior_eq_and_elem_osc_tc064_aux :
    (∀ (c_lam c_half : ℝ) {d : ℕ}, 1 ≤ d →
      |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| ≤
        (4 + |c_lam| + |c_half|) * (d : ℝ) * (1 + Real.log (d : ℝ)) ^ 2) ∧
      (∀ {T : ℕ}, 2 ≤ T → ∀ (D0 : ℕ) (c_lam c_half : ℝ), ∀ k ∈ Finset.Icc 1 T,
        openCoreAdjustedCoeffBeta c_lam c_half T D0 k =
          -(c_lam * (if IsSquare k then 1 else 0)) -
            (if k = T then selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T else 0) -
            (∑ e ∈ (Finset.Icc 1 T).filter (fun e => e ∣ k),
              (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                (liouvilleLambda (k / e) : ℝ)) -
            ((∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => d ∣ k),
                (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                  (liouvilleLambda (k / d) : ℝ)) -
              (∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => (d + 1) ∣ k),
                (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                  (liouvilleLambda (k / (d + 1)) : ℝ)))) := by
  refine ⟨?_, ?_⟩
  · intro c_lam c_half d hd1
    have hd_ne : d ≠ 0 := by omega
    have hd_pos_r : (0 : ℝ) < (d : ℝ) := Nat.cast_pos.mpr hd1
    have hd1_r : (1 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd1
    have hlogd_nn : 0 ≤ Real.log (d : ℝ) := Real.log_nonneg hd1_r
    have hsqrt_le : Real.sqrt (d : ℝ) ≤ (d : ℝ) := by
      have hsq : (Real.sqrt (d : ℝ)) ^ 2 ≤ (d : ℝ) ^ 2 := by
        rw [Real.sq_sqrt (le_of_lt hd_pos_r)]; nlinarith
      nlinarith [Real.sqrt_nonneg (d : ℝ)]
    have hW2 := (spillover_fringe_reindexing_and_mixed_covariance_reduction_tc062).2.1.2 hd1
    unfold selbergCenteredRemainderInt squarePoleDriftM
    rw [if_neg hd_ne]
    have h2 : |c_lam * (d : ℝ)| = |c_lam| * (d : ℝ) := by rw [abs_mul, abs_of_pos hd_pos_r]
    have h3 : |4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ)| ≤ (d : ℝ) * (4 * Real.log (d : ℝ)) := by
      rw [abs_of_nonneg (by positivity)]; nlinarith
    have h4 : |c_half * Real.sqrt (d : ℝ)| ≤ (d : ℝ) * |c_half| := by
      rw [abs_mul, abs_of_nonneg (Real.sqrt_nonneg _)]; nlinarith [abs_nonneg c_half]
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
    have h_poly :
        (Real.log (d : ℝ)) ^ 2 + 4 * Real.log (d : ℝ) + |c_lam| + |c_half| ≤
          (4 + |c_lam| + |c_half|) * (1 + Real.log (d : ℝ)) ^ 2 := by
      have h_rem_nn :
          0 ≤ 4 + 3 * (Real.log (d : ℝ)) ^ 2 + 4 * Real.log (d : ℝ) +
            (|c_lam| + |c_half|) * (2 * Real.log (d : ℝ) + (Real.log (d : ℝ)) ^ 2) := by
        nlinarith [sq_nonneg (Real.log (d : ℝ)), hlogd_nn, abs_nonneg c_lam, abs_nonneg c_half]
      linarith [show (4 + |c_lam| + |c_half|) * (1 + Real.log (d : ℝ)) ^ 2 -
          ((Real.log (d : ℝ)) ^ 2 + 4 * Real.log (d : ℝ) + |c_lam| + |c_half|) =
        4 + 3 * (Real.log (d : ℝ)) ^ 2 + 4 * Real.log (d : ℝ) +
          (|c_lam| + |c_half|) * (2 * Real.log (d : ℝ) + (Real.log (d : ℝ)) ^ 2) by ring]
    calc
      |selbergCumulativeW2 d - c_lam * (d : ℝ) -
          (4 * Real.sqrt (d : ℝ) * Real.log (d : ℝ) + c_half * Real.sqrt (d : ℝ))|
        ≤ (d : ℝ) * ((Real.log (d : ℝ)) ^ 2 + 4 * Real.log (d : ℝ) + |c_lam| + |c_half|) := by
            linarith [h_tri, hW2, h2, h3, h4]
      _ ≤ (d : ℝ) * ((4 + |c_lam| + |c_half|) * (1 + Real.log (d : ℝ)) ^ 2) :=
          mul_le_mul_of_nonneg_left h_poly (le_of_lt hd_pos_r)
      _ = (4 + |c_lam| + |c_half|) * (d : ℝ) * (1 + Real.log (d : ℝ)) ^ 2 := by ring
  · intro T hT2 D0 c_lam c_half k hk
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
        rw [← Finset.sum_sub_distrib]; apply Finset.sum_congr rfl; intro d _; ring
      have h_sub2 :
          (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
              (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                (liouvilleLambda (k / (d + 1)) : ℝ)) =
            (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
                selbergCenteredRemainderInt c_lam d * (liouvilleLambda (k / (d + 1)) : ℝ)) -
              (∑ d ∈ (Finset.Icc 1 (T - 1)).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d),
                squarePoleDriftM c_half d * (liouvilleLambda (k / (d + 1)) : ℝ)) := by
        rw [← Finset.sum_sub_distrib]; apply Finset.sum_congr rfl; intro d _; ring
      linarith [h1, h2, h_sub1, h_sub2]
    have h_div_Icc : k.divisors = (Finset.Icc 1 T).filter (fun e => e ∣ k) := by
      ext e
      simp only [Nat.mem_divisors, Finset.mem_filter, Finset.mem_Icc]
      constructor
      · rintro ⟨hd, _⟩
        exact ⟨⟨Nat.pos_of_dvd_of_pos hd hk_bds.1, le_trans (Nat.le_of_dvd hk_bds.1 hd) hk_bds.2⟩, hd⟩
      · rintro ⟨_, hd⟩
        exact ⟨hd, hk_ne⟩
    have h_drift_eq :
        driftOp =
          (∑ e ∈ (Finset.Icc 1 T).filter (fun e => e ∣ k),
              (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                (liouvilleLambda (k / e) : ℝ)) -
            (if k = T then squarePoleDriftM c_half T else 0) := by
      rw [← h_div_Icc]
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
          · rintro ⟨⟨_, hd_hi⟩, ⟨hd_dvd, _⟩⟩; exact ⟨by omega, ⟨hd_dvd, hk_ne⟩⟩
          · rintro ⟨hd_ne_T, ⟨hd_dvd, _⟩⟩
            exact ⟨⟨Nat.pos_of_dvd_of_pos hd_dvd hk_bds.1, by
              have hle := Nat.le_of_dvd hk_bds.1 hd_dvd; omega⟩,
              ⟨hd_dvd, Nat.div_le_div_right hk_bds.2⟩⟩
        rw [hf_eq]
        by_cases hkT : k = T
        · rw [hkT]
          have hT_div : T ∈ T.divisors := Nat.mem_divisors.mpr ⟨dvd_refl T, by omega⟩
          have hl1 : (liouvilleLambda (T / T) : ℝ) = 1 := by
            rw [Nat.div_self (by omega)]
            simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
          rw [if_pos rfl, ← Finset.add_sum_erase _ _ hT_div, hl1, mul_one]; ring
        · have hT_not : T ∉ k.divisors := by
            intro hm; have hle := Nat.le_of_dvd hk_bds.1 (Nat.mem_divisors.mp hm).1; omega
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
        · intro _ _ _ _ h; omega
        · intro e he
          simp only [Finset.mem_erase, Nat.mem_divisors] at he
          rcases he with ⟨he_ne1, ⟨he_dvd, _⟩⟩
          have he_pos : 0 < e := Nat.pos_of_dvd_of_pos he_dvd hk_bds.1
          have he_le_T : e ≤ T := le_trans (Nat.le_of_dvd hk_bds.1 he_dvd) hk_bds.2
          let d := e - 1
          have hd1 : d + 1 = e := by omega
          have h_div_le : k / e ≤ T / d :=
            le_trans (Nat.div_le_div_right hk_bds.2)
              (Nat.div_le_div_left (by omega : d ≤ e) (by omega : 0 < d))
          refine ⟨d, ?_, hd1⟩
          simp only [Finset.mem_filter, Finset.mem_Icc]
          exact ⟨⟨by omega, by omega⟩, ⟨by rwa [hd1], by rwa [hd1]⟩⟩
        · intro _ _; simp
      dsimp [driftOp]
      rw [h_s1, h_s2, sub_right_comm, ← Finset.sum_sub_distrib]
      congr 1; apply Finset.sum_congr rfl; intro _ _; ring
    have h_f_d :
        (Finset.Icc 1 D_min).filter (fun d => d ∣ k ∧ k / d ≤ T / d) =
          (Finset.Icc 1 D_min).filter (fun d => d ∣ k) := by
      ext d; simp only [Finset.mem_filter]
      exact ⟨fun h => ⟨h.1, h.2.1⟩, fun h => ⟨h.1, h.2, Nat.div_le_div_right hk_bds.2⟩⟩
    have h_f_d1 :
        (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k ∧ k / (d + 1) ≤ T / d) =
          (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k) := by
      ext d; simp only [Finset.mem_filter, Finset.mem_Icc]
      refine ⟨fun h => ⟨h.1, h.2.1⟩, fun h => ⟨h.1, h.2, ?_⟩⟩
      exact le_trans (Nat.div_le_div_right hk_bds.2)
        (Nat.div_le_div_left (Nat.le_succ d) h.1.1)
    rw [h_beta_split, h_alpha_adj, h_drift_eq]
    dsimp [smallOp, D_min]
    rw [h_f_d, h_f_d1]
    split_ifs <;> ring

private theorem canonical_log_and_cutoff_bounds_tc064_aux {Y : ℝ} (hY2 : 2 ≤ Y) :
    3 ≤ canonicalCutoffT Y ∧
      (5 / 8 : ℝ) < Real.log Y ∧
      Real.log (canonicalCutoffT Y : ℝ) ≤ (9 / 4 : ℝ) * Real.log Y ∧
      Y ^ (5 / 2 : ℝ) ≤ (canonicalCutoffT Y : ℝ) ^ 2 ∧
      (1 + Real.log (canonicalCutoffT Y : ℝ)) / Real.log Y ≤ 4 ∧
      1 + Real.log (canonicalCutoffT Y : ℝ) ≤ (9 / 4 : ℝ) * (1 + Real.log Y) := by
  let T := canonicalCutoffT Y
  have hY_pos : 0 < Y := by linarith
  have h2_lt_rpow : (2 : ℝ) < Y ^ (5 / 4 : ℝ) := by
    have h2_lt : (2 : ℝ) ^ (1 : ℝ) < (2 : ℝ) ^ (5 / 4 : ℝ) :=
      Real.rpow_lt_rpow_of_exponent_lt (by norm_num) (by norm_num)
    rw [Real.rpow_one] at h2_lt
    exact lt_of_lt_of_le h2_lt (Real.rpow_le_rpow (by norm_num) hY2 (by norm_num))
  have hle_T : Y ^ (5 / 4 : ℝ) ≤ (T : ℝ) := Nat.le_ceil _
  have hT_gt2_r : (2 : ℝ) < (T : ℝ) := lt_of_lt_of_le h2_lt_rpow hle_T
  have hT_ge3 : 3 ≤ T := by
    have hlt : 2 < T := by exact_mod_cast hT_gt2_r
    omega
  have hlog2_gt : (5 / 8 : ℝ) < Real.log 2 := by
    have h1 : (27 / 32 : ℝ) ≤ Real.exp (-5 / 32 : ℝ) := by
      linarith [Real.add_one_le_exp (-5 / 32 : ℝ)]
    have hp4 : (27 / 32 : ℝ) ^ 4 ≤ Real.exp (-5 / 8 : ℝ) := by
      have hp := pow_le_pow_left (by norm_num) h1 4
      have hexp4 : (Real.exp (-5 / 32 : ℝ)) ^ 4 = Real.exp (-5 / 8 : ℝ) := by
        rw [← Real.exp_nat_mul]; congr 1; norm_num
      rwa [hexp4] at hp
    have h_half : (1 / 2 : ℝ) < Real.exp (-5 / 8 : ℝ) :=
      lt_of_lt_of_le (by norm_num) hp4
    have h_prod : Real.exp (-5 / 8 : ℝ) * Real.exp (5 / 8 : ℝ) = 1 := by
      rw [← Real.exp_add]; norm_num
    have h_lt2 : Real.exp (5 / 8 : ℝ) < 2 := by
      nlinarith [h_half, h_prod, Real.exp_pos (5 / 8 : ℝ)]
    have hl := Real.log_lt_log (Real.exp_pos _) h_lt2
    rwa [Real.log_exp] at hl
  have hlogY_gt : (5 / 8 : ℝ) < Real.log Y :=
    lt_of_lt_of_le hlog2_gt (Real.log_le_log (by norm_num) hY2)
  have hlogY_pos : 0 < Real.log Y := by linarith
  have hT_lt : (T : ℝ) < Y ^ (5 / 4 : ℝ) + 1 := Nat.ceil_lt_add_one (by positivity)
  have hT_le_Y94 : (T : ℝ) ≤ Y ^ (9 / 4 : ℝ) := by
    have h2 : (T : ℝ) ≤ 2 * Y ^ (5 / 4 : ℝ) := by linarith
    have hY_eq : Y * Y ^ (5 / 4 : ℝ) = Y ^ (9 / 4 : ℝ) := by
      calc
        Y * Y ^ (5 / 4 : ℝ) = Y ^ (1 : ℝ) * Y ^ (5 / 4 : ℝ) := by rw [Real.rpow_one]
        _ = Y ^ (9 / 4 : ℝ) := by rw [← Real.rpow_add hY_pos]; norm_num
    exact le_trans h2 (by rw [← hY_eq]; exact mul_le_mul_of_nonneg_right hY2 (by positivity))
  have hlogT_le : Real.log (T : ℝ) ≤ (9 / 4 : ℝ) * Real.log Y := by
    have hl := Real.log_le_log (by positivity) hT_le_Y94
    rwa [Real.log_rpow hY_pos] at hl
  have h52 : Y ^ (5 / 2 : ℝ) ≤ (T : ℝ) ^ 2 := by
    have he : (Y ^ (5 / 4 : ℝ)) ^ 2 = Y ^ (5 / 2 : ℝ) := by
      rw [← Real.rpow_natCast _ 2, ← Real.rpow_mul (le_of_lt hY_pos)]; norm_num
    rw [← he]; exact pow_le_pow_left (by positivity) hle_T 2
  have h_rat4 : (1 + Real.log (T : ℝ)) / Real.log Y ≤ 4 := by
    rw [div_le_iff hlogY_pos]
    linarith [hlogT_le, hlogY_gt]
  exact ⟨hT_ge3, hlogY_gt, hlogT_le, h52, h_rat4, by linarith⟩

private theorem small_divisor_jump_core_bounds_tc064_aux (c_lam c_half : ℝ) :
    let C_tau : ℝ :=
      (16 / 5 : ℝ) * (2 + Real.sqrt 2) * RiemannScope.tau ^ (5 / 2 : ℝ) *
        Real.sqrt (Real.log RiemannScope.tau)
    let S_st : ℕ → ℕ → Finset ℕ := fun T a =>
      (coreSquareMultipliers a T).biUnion (fun b =>
        (dyadicChainExponents (a * b ^ 2) T).biUnion (fun j =>
          (Finset.range 2).image (fun eps => 2 ^ (2 * j + eps) * a * b ^ 2)))
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ {W_sm : ℝ}, 0 ≤ W_sm →
      let T := canonicalCutoffT Y
      let D0 := Nat.floor (Real.log Y)
      (∀ d ∈ Finset.Icc 1 (min D0 (T - 1)),
        |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| / Real.sqrt (d : ℝ) ≤
          W_sm) →
      Real.sqrt
          (∑ a ∈ oddSquarefreeCores T,
            windowEnergyNormSq Y
              (fun X =>
                (1 / (Real.log X) ^ 2) *
                  (∑ k ∈ S_st T a,
                    (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                      ((∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => d ∣ k),
                          (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                            (liouvilleLambda (k / d) : ℝ)) -
                        (∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => (d + 1) ∣ k),
                          (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                            (liouvilleLambda (k / (d + 1)) : ℝ))) *
                      gaussianTermPhi k X))) ≤
        2 * C_tau * (((min D0 (T - 1) : ℕ) : ℝ) * W_sm / (Real.log Y) ^ 2) *
          Real.sqrt (1 + Real.log (T : ℝ))) ∧
      (∀ {C_osc : ℝ}, 0 ≤ C_osc →
        (∀ d : ℕ, 1 ≤ d →
          |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| ≤ C_osc * (d : ℝ)) →
        ∀ {Y : ℝ}, 2 ≤ Y →
          let T := canonicalCutoffT Y
          let D0 := Nat.floor (Real.log Y)
          Real.sqrt
              (∑ a ∈ oddSquarefreeCores T,
                windowEnergyNormSq Y
                  (fun X =>
                    (1 / (Real.log X) ^ 2) *
                      (∑ k ∈ S_st T a,
                        (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                          ((∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => d ∣ k),
                              (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                                (liouvilleLambda (k / d) : ℝ)) -
                            (∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => (d + 1) ∣ k),
                              (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                                (liouvilleLambda (k / (d + 1)) : ℝ))) *
                          gaussianTermPhi k X))) ≤
            4 * C_osc * C_tau) := by
  intro C_tau S_st
  obtain ⟨hCtau_pos, _, _, _, h_st_div⟩ :=
    paired_core_station_set_and_divisor_norm_tc064_aux
  have h_lam_abs : ∀ m : ℕ, |(liouvilleLambda m : ℝ)| ≤ 1 := by
    intro m
    by_cases hm : m = 0
    · subst hm; simp [liouvilleLambda]
    · simp [liouvilleLambda, hm, liouvilleSignFromOmega]
  have h_sgn_abs :
      ∀ (k q : ℕ), |(-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
          (liouvilleLambda q : ℝ)| ≤ 1 := by
    intro k q
    rw [abs_mul, abs_mul, abs_pow, abs_neg, abs_one, one_pow, one_mul]
    calc
      |(liouvilleLambda k : ℝ)| * |(liouvilleLambda q : ℝ)|
        ≤ 1 * 1 := mul_le_mul (h_lam_abs k) (h_lam_abs q) (abs_nonneg _) zero_le_one
      _ = 1 := one_mul 1
  -- Reusable bound for small-divisor operator (both d | k and (d + 1) | k) given any R_osc bound:
  have h_small_op_bound :
      ∀ {Y : ℝ} (hY2 : 2 ≤ Y) {W_sm : ℝ} (hW_nn : 0 ≤ W_sm),
        let T := canonicalCutoffT Y
        let D0 := Nat.floor (Real.log Y)
        (∀ d ∈ Finset.Icc 1 (min D0 (T - 1)),
          |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| / Real.sqrt (d : ℝ) ≤
            W_sm) →
        Real.sqrt
            (∑ a ∈ oddSquarefreeCores T,
              windowEnergyNormSq Y
                (fun X =>
                  (1 / (Real.log X) ^ 2) *
                    (∑ k ∈ S_st T a,
                      (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                        ((∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => d ∣ k),
                            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                              (liouvilleLambda (k / d) : ℝ)) -
                          (∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => (d + 1) ∣ k),
                            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                              (liouvilleLambda (k / (d + 1)) : ℝ))) *
                        gaussianTermPhi k X))) ≤
          2 * C_tau * (((min D0 (T - 1) : ℕ) : ℝ) * W_sm / (Real.log Y) ^ 2) *
            Real.sqrt (1 + Real.log (T : ℝ)) := by
    intro Y hY2 W_sm hW_nn T D0 hW_d
    have hY0 : 0 < Y := by linarith
    obtain ⟨hT_ge3, _, _, _, _, _⟩ := canonical_log_and_cutoff_bounds_tc064_aux hY2
    let D_min := min D0 (T - 1)
    let G1 : ℕ → ℕ → ℝ → ℝ := fun d a X =>
      (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
        (∑ k ∈ (S_st T a).filter (fun k => d ∣ k),
          ((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
            (liouvilleLambda (k / d) : ℝ)) * gaussianTermPhi k X)
    let G2 : ℕ → ℕ → ℝ → ℝ := fun d a X =>
      -(selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
        (∑ k ∈ (S_st T a).filter (fun k => (d + 1) ∣ k),
          ((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
            (liouvilleLambda (k / (d + 1)) : ℝ)) * gaussianTermPhi k X)
    have hc_phi : ∀ k : ℕ, ContinuousOn (gaussianTermPhi k) (Set.uIcc Y (RiemannScope.tau * Y)) :=
      continuousOn_gaussianTermPhi_param_tc064_aux Y RiemannScope.tau
    have hc_G12 :
        ∀ d ∈ Finset.Icc 1 D_min, ∀ a ∈ oddSquarefreeCores T,
          ContinuousOn (fun X => G1 d a X + G2 d a X) (Set.uIcc Y (RiemannScope.tau * Y)) := by
      intro d _ a _
      exact (continuousOn_const.mul
        (continuousOn_finset_sum _ (fun k _ => continuousOn_const.mul (hc_phi k)))).add
        (continuousOn_const.mul
          (continuousOn_finset_sum _ (fun k _ => continuousOn_const.mul (hc_phi k))))
    have h_reidx_a :
        ∀ a ∈ oddSquarefreeCores T, ∀ X : ℝ,
          (∑ k ∈ S_st T a,
              (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                ((∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k),
                    (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                      (liouvilleLambda (k / d) : ℝ)) -
                  (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k),
                    (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                      (liouvilleLambda (k / (d + 1)) : ℝ))) *
                gaussianTermPhi k X) =
            ∑ d ∈ Finset.Icc 1 D_min, (G1 d a X + G2 d a X) := by
      intro a _ X
      have h_sub_k :
          ∀ k ∈ S_st T a,
            (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                ((∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k),
                    (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                      (liouvilleLambda (k / d) : ℝ)) -
                  (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k),
                    (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                      (liouvilleLambda (k / (d + 1)) : ℝ))) *
                gaussianTermPhi k X =
              (∑ d ∈ Finset.Icc 1 D_min,
                  if d ∣ k then
                    (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                      (((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                        (liouvilleLambda (k / d) : ℝ)) * gaussianTermPhi k X)
                  else 0) +
                (∑ d ∈ Finset.Icc 1 D_min,
                  if (d + 1) ∣ k then
                    -(selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                      (((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                        (liouvilleLambda (k / (d + 1)) : ℝ)) * gaussianTermPhi k X)
                  else 0) := by
        intro k _
        rw [← Finset.sum_filter, ← Finset.sum_filter]
        have hs1 :
            (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k),
                  (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                    (liouvilleLambda (k / d) : ℝ)) * gaussianTermPhi k X =
              ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k),
                (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                  (((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                    (liouvilleLambda (k / d) : ℝ)) * gaussianTermPhi k X) := by
          rw [Finset.mul_sum, Finset.sum_mul]
          apply Finset.sum_congr rfl; intro _ _; ring
        have hs2 :
            -((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k),
                  (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                    (liouvilleLambda (k / (d + 1)) : ℝ)) * gaussianTermPhi k X) =
              ∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k),
                -(selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                  (((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                    (liouvilleLambda (k / (d + 1)) : ℝ)) * gaussianTermPhi k X) := by
          rw [Finset.mul_sum, Finset.sum_mul, ← Finset.sum_neg_distrib]
          apply Finset.sum_congr rfl; intro _ _; ring
        linarith [hs1, hs2]
      rw [Finset.sum_congr rfl h_sub_k, Finset.sum_add_distrib]
      conv_lhs => enter [1]; rw [Finset.sum_comm]
      conv_lhs => enter [2]; rw [Finset.sum_comm]
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro d _
      dsimp [G1, G2]
      rw [← Finset.sum_filter, ← Finset.sum_filter, Finset.mul_sum, Finset.mul_sum]
    have h_log_pull :
        (∑ a ∈ oddSquarefreeCores T,
            windowEnergyNormSq Y
              (fun X =>
                (1 / (Real.log X) ^ 2) *
                  (∑ d ∈ Finset.Icc 1 D_min, (G1 d a X + G2 d a X)))) ≤
          (1 / (Real.log Y) ^ 4) *
            (∑ a ∈ oddSquarefreeCores T,
              windowEnergyNormSq Y (fun X => ∑ d ∈ Finset.Icc 1 D_min, (G1 d a X + G2 d a X))) := by
      rw [Finset.mul_sum]
      apply Finset.sum_le_sum
      intro a ha
      exact log_sq_inv_windowEnergy_le_tc064_aux hY2
        (continuousOn_finset_sum _ (fun d hd => hc_G12 d hd a ha))
    have h_mink_d :=
      (direct_sum_window_minkowski_sq_tc064_aux hY0 (oddSquarefreeCores T) (Finset.Icc 1 D_min)
        (fun d a X => G1 d a X + G2 d a X) hc_G12).1
    have h_each_d :
        ∀ d ∈ Finset.Icc 1 D_min,
          Real.sqrt (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (fun X => G1 d a X + G2 d a X)) ≤
            2 * C_tau * W_sm * Real.sqrt (1 + Real.log (T : ℝ)) := by
      intro d hd
      obtain ⟨hd1, hd_hi⟩ := Finset.mem_Icc.mp hd
      have hd_le_T : d ≤ T := by dsimp [D_min] at hd_hi; omega
      have hd1_le_T : d + 1 ≤ T := by dsimp [D_min] at hd_hi; omega
      let R_d := selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d
      have hc1 : ∀ a ∈ oddSquarefreeCores T, ContinuousOn (G1 d a) (Set.uIcc Y (RiemannScope.tau * Y)) :=
        fun _ _ => continuousOn_const.mul
          (continuousOn_finset_sum _ (fun k _ => continuousOn_const.mul (hc_phi k)))
      have hc2 : ∀ a ∈ oddSquarefreeCores T, ContinuousOn (G2 d a) (Set.uIcc Y (RiemannScope.tau * Y)) :=
        fun _ _ => continuousOn_const.mul
          (continuousOn_finset_sum _ (fun k _ => continuousOn_const.mul (hc_phi k)))
      have h_2sum :=
        (direct_sum_window_minkowski_sq_tc064_aux hY0 (oddSquarefreeCores T) (Finset.range 2)
          (fun i a => if i = 0 then G1 d a else G2 d a)
          (fun i _ a ha => by
            by_cases h0 : i = 0
            · simp only [h0, ↓reduceIte]; exact hc1 a ha
            · simp only [h0, ↓reduceIte]; exact hc2 a ha)).1
      simp only [Finset.sum_range_succ, Finset.sum_range_one, Finset.sum_range_zero,
        ↓reduceIte, Nat.one_ne_zero, zero_add] at h_2sum
      have h_scale_norm :
          ∀ (c : ℝ) (f : ℝ → ℝ), windowEnergyNormSq Y (fun X => c * f X) = c ^ 2 * windowEnergyNormSq Y f := by
        intro c f
        unfold windowEnergyNormSq windowPairing
        rw [← intervalIntegral.integral_const_mul]
        apply intervalIntegral.integral_congr; intro X _; ring
      have hb_G1 :
          Real.sqrt (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (G1 d a)) ≤
            |R_d| * (C_tau * (1 / Real.sqrt (d : ℝ)) * Real.sqrt (1 + Real.log (T : ℝ))) := by
        have h_eq :
            (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (G1 d a)) =
              R_d ^ 2 * ∑ a ∈ oddSquarefreeCores T,
                windowEnergyNormSq Y (fun X => ∑ k ∈ (S_st T a).filter (fun k => d ∣ k),
                  ((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                    (liouvilleLambda (k / d) : ℝ)) * gaussianTermPhi k X) := by
          rw [Finset.mul_sum]; apply Finset.sum_congr rfl; intro a _; exact h_scale_norm R_d _
        rw [h_eq, Real.sqrt_mul (sq_nonneg R_d), Real.sqrt_sq_eq_abs]
        exact mul_le_mul_of_nonneg_left
          (h_st_div hY0 hd1 hd_le_T _ (fun k => h_sgn_abs k (k / d))) (abs_nonneg R_d)
      have hb_G2 :
          Real.sqrt (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (G2 d a)) ≤
            |R_d| * (C_tau * (1 / Real.sqrt (d : ℝ)) * Real.sqrt (1 + Real.log (T : ℝ))) := by
        have h_eq :
            (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (G2 d a)) =
              R_d ^ 2 * ∑ a ∈ oddSquarefreeCores T,
                windowEnergyNormSq Y (fun X => ∑ k ∈ (S_st T a).filter (fun k => (d + 1) ∣ k),
                  ((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                    (liouvilleLambda (k / (d + 1)) : ℝ)) * gaussianTermPhi k X) := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro a _
          have hs := h_scale_norm (-R_d)
            (fun X => ∑ k ∈ (S_st T a).filter (fun k => (d + 1) ∣ k),
              ((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                (liouvilleLambda (k / (d + 1)) : ℝ)) * gaussianTermPhi k X)
          have hneg_sq : (-R_d) ^ 2 = R_d ^ 2 := by ring
          rw [hneg_sq] at hs
          exact hs
        rw [h_eq, Real.sqrt_mul (sq_nonneg R_d), Real.sqrt_sq_eq_abs]
        have hd_pos_r : (0 : ℝ) < (d : ℝ) := Nat.cast_pos.mpr hd1
        have h_inv_d1 : 1 / Real.sqrt ((d + 1 : ℕ) : ℝ) ≤ 1 / Real.sqrt (d : ℝ) :=
          one_div_le_one_div_of_le (Real.sqrt_pos.mpr hd_pos_r)
            (Real.sqrt_le_sqrt (by exact_mod_cast Nat.le_succ d))
        have h_div_d1 :=
          h_st_div hY0 (by omega : 1 ≤ d + 1) hd1_le_T _ (fun k => h_sgn_abs k (k / (d + 1)))
        have h_le_d :
            C_tau * (1 / Real.sqrt ((d + 1 : ℕ) : ℝ)) * Real.sqrt (1 + Real.log (T : ℝ)) ≤
              C_tau * (1 / Real.sqrt (d : ℝ)) * Real.sqrt (1 + Real.log (T : ℝ)) :=
          mul_le_mul_of_nonneg_right
            (mul_le_mul_of_nonneg_left h_inv_d1 (le_of_lt hCtau_pos)) (Real.sqrt_nonneg _)
        exact mul_le_mul_of_nonneg_left (le_trans h_div_d1 h_le_d) (abs_nonneg R_d)
      have h_wd := hW_d d hd
      have h_prod_w :
          |R_d| * (1 / Real.sqrt (d : ℝ)) ≤ W_sm := by
        simpa [R_d, div_eq_mul_inv] using h_wd
      have h_comb :
          2 * (|R_d| * (C_tau * (1 / Real.sqrt (d : ℝ)) * Real.sqrt (1 + Real.log (T : ℝ)))) ≤
            2 * C_tau * W_sm * Real.sqrt (1 + Real.log (T : ℝ)) := by
        have hm := mul_le_mul_of_nonneg_right
          (mul_le_mul_of_nonneg_left h_prod_w (by positivity : 0 ≤ 2 * C_tau))
          (Real.sqrt_nonneg (1 + Real.log (T : ℝ)))
        linarith [hm, show 2 * (|R_d| * (C_tau * (1 / Real.sqrt (d : ℝ)) *
            Real.sqrt (1 + Real.log (T : ℝ)))) =
          (2 * C_tau) * (|R_d| * (1 / Real.sqrt (d : ℝ))) * Real.sqrt (1 + Real.log (T : ℝ)) by ring]
      exact le_trans h_2sum (le_trans (add_le_add hb_G1 hb_G2) (by rw [← two_mul]; exact h_comb))
    have h_congr_a :
        (∑ a ∈ oddSquarefreeCores T,
            windowEnergyNormSq Y
              (fun X =>
                (1 / (Real.log X) ^ 2) *
                  (∑ k ∈ S_st T a,
                    (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                      ((∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k),
                          (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                            (liouvilleLambda (k / d) : ℝ)) -
                        (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k),
                          (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                            (liouvilleLambda (k / (d + 1)) : ℝ))) *
                      gaussianTermPhi k X))) =
          ∑ a ∈ oddSquarefreeCores T,
            windowEnergyNormSq Y
              (fun X => (1 / (Real.log X) ^ 2) * (∑ d ∈ Finset.Icc 1 D_min, (G1 d a X + G2 d a X))) := by
      apply Finset.sum_congr rfl
      intro a ha
      congr 1; ext X; rw [h_reidx_a a ha X]
    rw [h_congr_a]
    have hc_card : ((Finset.Icc 1 D_min).card : ℝ) ≤ (D_min : ℝ) := by
      have hc : (Finset.Icc 1 D_min).card ≤ D_min := by simp [Nat.card_Icc]
      exact_mod_cast hc
    calc
      Real.sqrt
          (∑ a ∈ oddSquarefreeCores T,
            windowEnergyNormSq Y
              (fun X => (1 / (Real.log X) ^ 2) * (∑ d ∈ Finset.Icc 1 D_min, (G1 d a X + G2 d a X))))
        ≤ Real.sqrt
            ((1 / (Real.log Y) ^ 4) *
              (∑ a ∈ oddSquarefreeCores T,
                windowEnergyNormSq Y (fun X => ∑ d ∈ Finset.Icc 1 D_min, (G1 d a X + G2 d a X)))) :=
          Real.sqrt_le_sqrt h_log_pull
      _ = (1 / (Real.log Y) ^ 2) *
            Real.sqrt
              (∑ a ∈ oddSquarefreeCores T,
                windowEnergyNormSq Y (fun X => ∑ d ∈ Finset.Icc 1 D_min, (G1 d a X + G2 d a X))) := by
          rw [Real.sqrt_mul (by positivity), one_div, Real.sqrt_inv,
            show (Real.log Y) ^ 4 = ((Real.log Y) ^ 2) ^ 2 by ring,
            Real.sqrt_sq (by positivity), one_div]
      _ ≤ (1 / (Real.log Y) ^ 2) *
            (∑ d ∈ Finset.Icc 1 D_min,
              Real.sqrt (∑ a ∈ oddSquarefreeCores T,
                windowEnergyNormSq Y (fun X => G1 d a X + G2 d a X))) :=
          mul_le_mul_of_nonneg_left h_mink_d (by positivity)
      _ ≤ (1 / (Real.log Y) ^ 2) *
            (∑ _d ∈ Finset.Icc 1 D_min, (2 * C_tau * W_sm * Real.sqrt (1 + Real.log (T : ℝ)))) :=
          mul_le_mul_of_nonneg_left (Finset.sum_le_sum h_each_d) (by positivity)
      _ = (1 / (Real.log Y) ^ 2) *
            (((Finset.Icc 1 D_min).card : ℝ) *
              (2 * C_tau * W_sm * Real.sqrt (1 + Real.log (T : ℝ)))) := by simp
      _ ≤ (1 / (Real.log Y) ^ 2) *
            ((D_min : ℝ) * (2 * C_tau * W_sm * Real.sqrt (1 + Real.log (T : ℝ)))) :=
          mul_le_mul_of_nonneg_left
            (mul_le_mul_of_nonneg_right hc_card (by positivity)) (by positivity)
      _ = 2 * C_tau * ((D_min : ℝ) * W_sm / (Real.log Y) ^ 2) *
            Real.sqrt (1 + Real.log (T : ℝ)) := by ring
  -- Part 1: Bonus O(1) bound on small-divisor jump under linear |R_osc(d)| <= C_osc * d
  have h_bonus_small :
      ∀ {C_osc : ℝ}, 0 ≤ C_osc →
        (∀ d : ℕ, 1 ≤ d →
          |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| ≤ C_osc * (d : ℝ)) →
        ∀ {Y : ℝ}, 2 ≤ Y →
          let T := canonicalCutoffT Y
          let D0 := Nat.floor (Real.log Y)
          Real.sqrt
              (∑ a ∈ oddSquarefreeCores T,
                windowEnergyNormSq Y
                  (fun X =>
                    (1 / (Real.log X) ^ 2) *
                      (∑ k ∈ S_st T a,
                        (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                          ((∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => d ∣ k),
                              (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                                (liouvilleLambda (k / d) : ℝ)) -
                            (∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => (d + 1) ∣ k),
                              (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                                (liouvilleLambda (k / (d + 1)) : ℝ))) *
                          gaussianTermPhi k X))) ≤
            4 * C_osc * C_tau := by
    intro C_osc hCosc_nn h_osc Y hY2 T D0
    obtain ⟨_, hlogY_gt, hlogT_le, _, _, _⟩ := canonical_log_and_cutoff_bounds_tc064_aux hY2
    have hlogY_pos : 0 < Real.log Y := by linarith
    let D_min := min D0 (T - 1)
    by_cases hDm0 : D_min = 0
    · have h0 := h_small_op_bound hY2 (le_refl (0 : ℝ)) (by
        intro d hd
        change d ∈ Finset.Icc 1 D_min at hd
        rw [hDm0] at hd
        simp at hd)
      have h0_rhs :
          2 * C_tau * (((min D0 (T - 1) : ℕ) : ℝ) * 0 / (Real.log Y) ^ 2) *
              Real.sqrt (1 + Real.log (T : ℝ)) = 0 := by ring
      rw [h0_rhs] at h0
      exact le_trans h0 (by positivity)
    · have hDm1 : 1 ≤ D_min := by omega
      have hDm_le_L : (D_min : ℝ) ≤ Real.log Y :=
        le_trans (by exact_mod_cast min_le_left D0 (T - 1)) (Nat.floor_le (le_of_lt hlogY_pos))
      have hL_ge1 : 1 ≤ Real.log Y :=
        le_trans (show (1 : ℝ) ≤ (D_min : ℝ) by exact_mod_cast hDm1) hDm_le_L
      have h_w :
          ∀ d ∈ Finset.Icc 1 D_min,
            |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| / Real.sqrt (d : ℝ) ≤
              C_osc * Real.sqrt (Real.log Y) := by
        intro d hd
        obtain ⟨hd1, hd_hi⟩ := Finset.mem_Icc.mp hd
        have hd_le_L : (d : ℝ) ≤ Real.log Y := le_trans (by exact_mod_cast hd_hi) hDm_le_L
        have hsd : (d : ℝ) / Real.sqrt (d : ℝ) = Real.sqrt (d : ℝ) := Real.div_sqrt
        calc
          |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| / Real.sqrt (d : ℝ)
            ≤ (C_osc * (d : ℝ)) / Real.sqrt (d : ℝ) :=
              div_le_div_of_nonneg_right (h_osc d hd1) (Real.sqrt_nonneg _)
          _ = C_osc * ((d : ℝ) / Real.sqrt (d : ℝ)) := by ring
          _ = C_osc * Real.sqrt (d : ℝ) := by rw [hsd]
          _ ≤ C_osc * Real.sqrt (Real.log Y) :=
              mul_le_mul_of_nonneg_left (Real.sqrt_le_sqrt hd_le_L) hCosc_nn
      have hb := h_small_op_bound hY2 (mul_nonneg hCosc_nn (Real.sqrt_nonneg _)) h_w
      have h_sqrt_T : Real.sqrt (1 + Real.log (T : ℝ)) ≤ 2 * Real.sqrt (Real.log Y) := by
        have h1 : 1 + Real.log (T : ℝ) ≤ (2 * Real.sqrt (Real.log Y)) ^ 2 := by
          rw [mul_pow, Real.sq_sqrt (le_of_lt hlogY_pos)]
          linarith [hlogT_le, hL_ge1]
        calc
          Real.sqrt (1 + Real.log (T : ℝ))
            ≤ Real.sqrt ((2 * Real.sqrt (Real.log Y)) ^ 2) := Real.sqrt_le_sqrt h1
          _ = 2 * Real.sqrt (Real.log Y) := Real.sqrt_sq (by positivity)
      have h_dm_prod :
          ((min D0 (T - 1) : ℕ) : ℝ) * (C_osc * Real.sqrt (Real.log Y)) / (Real.log Y) ^ 2 *
              Real.sqrt (1 + Real.log (T : ℝ)) ≤
            2 * C_osc := by
        have h1 :
            ((min D0 (T - 1) : ℕ) : ℝ) * (C_osc * Real.sqrt (Real.log Y)) ≤
              Real.log Y * (C_osc * Real.sqrt (Real.log Y)) :=
          mul_le_mul_of_nonneg_right hDm_le_L (by positivity)
        have h2 :
            ((min D0 (T - 1) : ℕ) : ℝ) * (C_osc * Real.sqrt (Real.log Y)) / (Real.log Y) ^ 2 ≤
              Real.log Y * (C_osc * Real.sqrt (Real.log Y)) / (Real.log Y) ^ 2 :=
          div_le_div_of_nonneg_right h1 (by positivity)
        have h3 := mul_le_mul h2 h_sqrt_T (Real.sqrt_nonneg _) (by positivity)
        have h_id :
            (Real.log Y * (C_osc * Real.sqrt (Real.log Y)) / (Real.log Y) ^ 2) *
                (2 * Real.sqrt (Real.log Y)) = 2 * C_osc := by
          have hsL : Real.sqrt (Real.log Y) * Real.sqrt (Real.log Y) = Real.log Y :=
            Real.mul_self_sqrt (le_of_lt hlogY_pos)
          field_simp [ne_of_gt hlogY_pos]
          calc
            Real.log Y * (C_osc * Real.sqrt (Real.log Y)) * (2 * Real.sqrt (Real.log Y))
              = 2 * C_osc * Real.log Y * (Real.sqrt (Real.log Y) * Real.sqrt (Real.log Y)) := by ring
            _ = 2 * C_osc * (Real.log Y) ^ 2 := by rw [hsL]; ring
        linarith
      have hm := mul_le_mul_of_nonneg_left h_dm_prod (by positivity : 0 ≤ 2 * C_tau)
      linarith [hb, hm, show 2 * C_tau * (2 * C_osc) = 4 * C_osc * C_tau by ring]
  exact ⟨h_small_op_bound, h_bonus_small⟩

private theorem uncond_small_divisor_jump_core_bound_tc064_aux (c_lam c_half : ℝ) :
    let C_tau : ℝ :=
      (16 / 5 : ℝ) * (2 + Real.sqrt 2) * RiemannScope.tau ^ (5 / 2 : ℝ) *
        Real.sqrt (Real.log RiemannScope.tau)
    let C_sm : ℝ := 4 + |c_lam| + |c_half|
    let S_st : ℕ → ℕ → Finset ℕ := fun T a =>
      (coreSquareMultipliers a T).biUnion (fun b =>
        (dyadicChainExponents (a * b ^ 2) T).biUnion (fun j =>
          (Finset.range 2).image (fun eps => 2 ^ (2 * j + eps) * a * b ^ 2)))
    ∀ {Y : ℝ}, 2 ≤ Y →
      let T := canonicalCutoffT Y
      let D0 := Nat.floor (Real.log Y)
      Real.sqrt
          (∑ a ∈ oddSquarefreeCores T,
            windowEnergyNormSq Y
              (fun X =>
                (1 / (Real.log X) ^ 2) *
                  (∑ k ∈ S_st T a,
                    (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                      ((∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => d ∣ k),
                          (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                            (liouvilleLambda (k / d) : ℝ)) -
                        (∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => (d + 1) ∣ k),
                          (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                            (liouvilleLambda (k / (d + 1)) : ℝ))) *
                      gaussianTermPhi k X))) ≤
        48 * C_tau * C_sm * Real.sqrt (1 + Real.log Y) := by
  intro C_tau C_sm S_st Y hY2 T D0
  obtain ⟨hCtau_pos, _, _, _, _⟩ := paired_core_station_set_and_divisor_norm_tc064_aux
  obtain ⟨h_elem_osc, _⟩ := openCoreAdjustedCoeffBeta_interior_eq_and_elem_osc_tc064_aux
  obtain ⟨h_small_op_bound, _⟩ := small_divisor_jump_core_bounds_tc064_aux c_lam c_half
  obtain ⟨_, hlogY_gt, _, _, _, h1logT_le⟩ := canonical_log_and_cutoff_bounds_tc064_aux hY2
  have hlogY_pos : 0 < Real.log Y := by linarith
  have hCtau_nn : 0 ≤ C_tau := le_of_lt hCtau_pos
  have hCsm_nn : 0 ≤ C_sm := by dsimp [C_sm]; positivity
  have hsqrt_1logT_le :
      Real.sqrt (1 + Real.log (T : ℝ)) ≤ (3 / 2 : ℝ) * Real.sqrt (1 + Real.log Y) := by
    calc
      Real.sqrt (1 + Real.log (T : ℝ))
        ≤ Real.sqrt ((9 / 4 : ℝ) * (1 + Real.log Y)) := Real.sqrt_le_sqrt h1logT_le
      _ = (3 / 2 : ℝ) * Real.sqrt (1 + Real.log Y) := by
          rw [Real.sqrt_mul (by norm_num), show (9 / 4 : ℝ) = (3 / 2 : ℝ) ^ 2 by norm_num,
            Real.sqrt_sq (by norm_num)]
  let D_min := min D0 (T - 1)
  by_cases hDm0 : D_min = 0
  · have h0 := h_small_op_bound hY2 (le_refl (0 : ℝ)) (by
      intro d hd
      change d ∈ Finset.Icc 1 D_min at hd
      rw [hDm0] at hd
      simp at hd)
    have h0_rhs :
        2 * C_tau * (((min D0 (T - 1) : ℕ) : ℝ) * 0 / (Real.log Y) ^ 2) *
            Real.sqrt (1 + Real.log (T : ℝ)) = 0 := by ring
    rw [h0_rhs] at h0
    exact le_trans h0
      (mul_nonneg (mul_nonneg (mul_nonneg (by norm_num) hCtau_nn) hCsm_nn) (Real.sqrt_nonneg _))
  · have hDm1 : 1 ≤ D_min := by omega
    have hDm_le_L : (D_min : ℝ) ≤ Real.log Y :=
      le_trans (by exact_mod_cast min_le_left D0 (T - 1)) (Nat.floor_le (le_of_lt hlogY_pos))
    have hL_ge1 : 1 ≤ Real.log Y :=
      le_trans (show (1 : ℝ) ≤ (D_min : ℝ) by exact_mod_cast hDm1) hDm_le_L
    let s4 : ℝ := Real.sqrt (Real.sqrt (Real.log Y))
    have hs4_ge1 : 1 ≤ s4 := Real.one_le_sqrt.mpr (Real.one_le_sqrt.mpr hL_ge1)
    have hs4_pos : 0 < s4 := lt_of_lt_of_le zero_lt_one hs4_ge1
    have hs4_sq : s4 ^ 2 = Real.sqrt (Real.log Y) := Real.sq_sqrt (Real.sqrt_nonneg _)
    have hs4_4 : s4 ^ 4 = Real.log Y := by
      calc
        s4 ^ 4 = (s4 ^ 2) ^ 2 := by ring
        _ = Real.log Y := by rw [hs4_sq, Real.sq_sqrt (le_of_lt hlogY_pos)]
    have h_log_s4 : Real.log s4 ≤ s4 - 1 := by
      have hexp := Real.add_one_le_exp (s4 - 1)
      rw [sub_add_cancel] at hexp
      have hl := Real.log_le_log hs4_pos hexp
      rwa [Real.log_exp] at hl
    have h_1logL_le : 1 + Real.log (Real.log Y) ≤ 4 * s4 := by
      rw [← hs4_4, Real.log_pow]
      push_cast
      linarith
    have h_sq_16 : (1 + Real.log (Real.log Y)) ^ 2 ≤ 16 * Real.sqrt (Real.log Y) := by
      have h_nn : 0 ≤ 1 + Real.log (Real.log Y) :=
        add_nonneg zero_le_one (Real.log_nonneg hL_ge1)
      calc
        (1 + Real.log (Real.log Y)) ^ 2 ≤ (4 * s4) ^ 2 := pow_le_pow_left h_nn h_1logL_le 2
        _ = 16 * s4 ^ 2 := by ring
        _ = 16 * Real.sqrt (Real.log Y) := by rw [hs4_sq]
    have h_w_elem :
        ∀ d ∈ Finset.Icc 1 D_min,
          |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| / Real.sqrt (d : ℝ) ≤
            16 * C_sm * Real.log Y := by
      intro d hd
      obtain ⟨hd1, hd_hi⟩ := Finset.mem_Icc.mp hd
      have hd_pos : (0 : ℝ) < (d : ℝ) := Nat.cast_pos.mpr hd1
      have hd_le_L : (d : ℝ) ≤ Real.log Y := le_trans (by exact_mod_cast hd_hi) hDm_le_L
      have h1_log_d : 1 + Real.log (d : ℝ) ≤ 1 + Real.log (Real.log Y) :=
        add_le_add_left (Real.log_le_log hd_pos hd_le_L) 1
      have h_sq_d : (1 + Real.log (d : ℝ)) ^ 2 ≤ 16 * Real.sqrt (Real.log Y) :=
        le_trans (pow_le_pow_left
          (add_nonneg zero_le_one (Real.log_nonneg (by exact_mod_cast hd1))) h1_log_d 2) h_sq_16
      have hel := h_elem_osc c_lam c_half hd1
      have hsd : (d : ℝ) / Real.sqrt (d : ℝ) = Real.sqrt (d : ℝ) := Real.div_sqrt
      calc
        |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| / Real.sqrt (d : ℝ)
          ≤ (C_sm * (d : ℝ) * (1 + Real.log (d : ℝ)) ^ 2) / Real.sqrt (d : ℝ) :=
            div_le_div_of_nonneg_right hel (Real.sqrt_nonneg _)
        _ = C_sm * ((d : ℝ) / Real.sqrt (d : ℝ)) * (1 + Real.log (d : ℝ)) ^ 2 := by ring
        _ = C_sm * Real.sqrt (d : ℝ) * (1 + Real.log (d : ℝ)) ^ 2 := by rw [hsd]
        _ ≤ C_sm * Real.sqrt (Real.log Y) * (16 * Real.sqrt (Real.log Y)) := by
            have hm1 := mul_le_mul_of_nonneg_left (Real.sqrt_le_sqrt hd_le_L) hCsm_nn
            exact mul_le_mul hm1 h_sq_d (sq_nonneg _) (mul_nonneg hCsm_nn (Real.sqrt_nonneg _))
        _ = 16 * C_sm * Real.log Y := by
            have hsL : Real.sqrt (Real.log Y) * Real.sqrt (Real.log Y) = Real.log Y :=
              Real.mul_self_sqrt (le_of_lt hlogY_pos)
            calc
              C_sm * Real.sqrt (Real.log Y) * (16 * Real.sqrt (Real.log Y))
                = 16 * C_sm * (Real.sqrt (Real.log Y) * Real.sqrt (Real.log Y)) := by ring
              _ = 16 * C_sm * Real.log Y := by rw [hsL]
    have hb := h_small_op_bound hY2
      (mul_nonneg (mul_nonneg (by norm_num) hCsm_nn) (le_of_lt hlogY_pos)) h_w_elem
    have h_dm_ratio :
        (D_min : ℝ) * (16 * C_sm * Real.log Y) / (Real.log Y) ^ 2 ≤ 16 * C_sm := by
      have h1 :
          (D_min : ℝ) * (16 * C_sm * Real.log Y) ≤ Real.log Y * (16 * C_sm * Real.log Y) :=
        mul_le_mul_of_nonneg_right hDm_le_L
          (mul_nonneg (mul_nonneg (by norm_num) hCsm_nn) (le_of_lt hlogY_pos))
      calc
        (D_min : ℝ) * (16 * C_sm * Real.log Y) / (Real.log Y) ^ 2
          ≤ Real.log Y * (16 * C_sm * Real.log Y) / (Real.log Y) ^ 2 :=
            div_le_div_of_nonneg_right h1 (sq_nonneg _)
        _ = 16 * C_sm := by field_simp [ne_of_gt hlogY_pos]; ring
    have hm := mul_le_mul h_dm_ratio hsqrt_1logT_le (Real.sqrt_nonneg _)
      (mul_nonneg (by norm_num : (0 : ℝ) ≤ 16) hCsm_nn)
    have hm2 := mul_le_mul_of_nonneg_left hm (mul_nonneg (by norm_num : (0 : ℝ) ≤ 2) hCtau_nn)
    have hb' :
        Real.sqrt
            (∑ a ∈ oddSquarefreeCores T,
              windowEnergyNormSq Y
                (fun X =>
                  (1 / (Real.log X) ^ 2) *
                    (∑ k ∈ S_st T a,
                      (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                        ((∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => d ∣ k),
                            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                              (liouvilleLambda (k / d) : ℝ)) -
                          (∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => (d + 1) ∣ k),
                            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                              (liouvilleLambda (k / (d + 1)) : ℝ))) *
                        gaussianTermPhi k X))) ≤
          (2 * C_tau) * ((D_min : ℝ) * (16 * C_sm * Real.log Y) / (Real.log Y) ^ 2 *
            Real.sqrt (1 + Real.log (T : ℝ))) := by
      have hb0 : _ ≤ 2 * C_tau * ((D_min : ℝ) * (16 * C_sm * Real.log Y) / (Real.log Y) ^ 2) *
          Real.sqrt (1 + Real.log (T : ℝ)) := hb
      rwa [mul_assoc (2 * C_tau)] at hb0
    have h_alg_48 :
        (2 * C_tau) * (16 * C_sm * ((3 / 2 : ℝ) * Real.sqrt (1 + Real.log Y))) =
          48 * C_tau * C_sm * Real.sqrt (1 + Real.log Y) := by ring
    rw [h_alg_48] at hm2
    exact le_trans hb' hm2

private theorem odd_chain_diagonal_sum_bound_tc064_aux (c_lam c_half : ℝ) :
    ∃ C_uv : ℝ, 0 ≤ C_uv ∧
      ∀ {Y : ℝ}, 2 ≤ Y →
        |∑ u ∈ oddChainParts (canonicalCutoffT Y),
            (windowEnergyNormSq Y
                (oddChainAdjustedProfileUcal c_lam c_half
                  (canonicalCutoffT Y) (Nat.floor (Real.log Y)) u) -
              4 * ∑ pk ∈ primePowerPairsUpTo (canonicalCutoffT Y),
                windowEnergyNormSq Y
                  (fun X => oddChainFeatureVectorVcal u (canonicalCutoffT Y) pk X))| ≤
          C_uv * (1 + Real.log Y) := by
  have hCg_pos := (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2.1
  obtain ⟨C_psi, hCpsi_nn, h_tc063_psi⟩ :=
    (uniform_same_chain_hilbert_bound_and_closure_transfer_tc063).2.2.2.1.2.2 c_lam c_half
  let C_g : ℝ := 186 * (RiemannScope.tau - 1)
  refine ⟨4 * C_psi + 16 * C_g,
    add_nonneg (mul_nonneg (by norm_num) hCpsi_nn)
      (mul_nonneg (by norm_num) (le_of_lt hCg_pos)), ?_⟩
  intro Y hY2
  have hY0 : 0 < Y := by linarith
  obtain ⟨_, hlogY_gt, _, _, _, _⟩ := canonical_log_and_cutoff_bounds_tc064_aux hY2
  obtain ⟨hle_win, _⟩ := uIcc_tau_log_props_tc064_aux hY2
  have hlogY_pos : 0 < Real.log Y := by linarith
  let T := canonicalCutoffT Y
  let D0 := Nat.floor (Real.log Y)
  have h_norm_nn : ∀ g : ℝ → ℝ, 0 ≤ windowEnergyNormSq Y g := by
    intro g
    unfold windowEnergyNormSq windowPairing
    apply intervalIntegral.integral_nonneg hle_win
    intro X hX; exact div_nonneg (mul_self_nonneg _) (by linarith [hX.1])
  let L := maxDyadicChainLength T
  obtain ⟨_, hL_sub1⟩ :=
    (uniform_same_chain_hilbert_bound_and_closure_transfer_tc063).2.2.2.1.2.1 hY2
  have hL_le2 : (L : ℝ) ≤ 2 * (1 + Real.log Y) := by
    dsimp [L, T] at hL_sub1 ⊢; linarith [hlogY_pos]
  have h_card_mink :
      ∀ (J : Finset ℕ) (g : ℕ → ℝ → ℝ),
        (∀ j ∈ J, ContinuousOn (g j) (Set.uIcc Y (RiemannScope.tau * Y))) →
        windowEnergyNormSq Y (fun X => ∑ j ∈ J, g j X) ≤
          (J.card : ℝ) * ∑ j ∈ J, windowEnergyNormSq Y (g j) := by
    intro J g hg_c
    have hm := (direct_sum_window_minkowski_sq_tc064_aux hY0 ({0} : Finset ℕ) J
      (fun j _ X => g j X) (fun j hj _ _ => hg_c j hj)).2
    simp only [Finset.sum_singleton] at hm
    have h_cs := finset_cauchy_schwarz_nonneg_tc064_aux J
      (fun _ => (1 : ℝ)) (fun j => Real.sqrt (windowEnergyNormSq Y (g j)))
      (fun _ _ => zero_le_one) (fun _ _ => Real.sqrt_nonneg _)
    have h_sq_cs := pow_le_pow_left
      (Finset.sum_nonneg (fun _ _ => mul_nonneg zero_le_one (Real.sqrt_nonneg _))) h_cs 2
    rw [mul_pow, Real.sq_sqrt (Finset.sum_nonneg (fun _ _ => sq_nonneg _)),
      Real.sq_sqrt (Finset.sum_nonneg (fun _ _ => sq_nonneg _))] at h_sq_cs
    simp only [one_mul, one_pow, Finset.sum_const, nsmul_eq_mul, mul_one] at h_sq_cs
    have h_sq_id :
        (∑ j ∈ J, (Real.sqrt (windowEnergyNormSq Y (g j))) ^ 2) =
          ∑ j ∈ J, windowEnergyNormSq Y (g j) :=
      Finset.sum_congr rfl (fun j _ => Real.sq_sqrt (h_norm_nn (g j)))
    rw [h_sq_id] at h_sq_cs
    exact le_trans hm h_sq_cs
  have h_bi_anchor :
      ∀ (W : ℕ → ℝ),
        (∑ u ∈ oddChainParts T, ∑ j ∈ dyadicChainExponents u T, W (4 ^ j * u)) =
          ∑ m ∈ primeInteriorTruncatedAnchors 2 T, W m := by
    intro W
    have h_uniq_m := (exact_odd_part_bijection_and_dyadic_chain_offdiag_split_tc063).1.1 T
    have h_bi_eq := ((exact_odd_part_bijection_and_dyadic_chain_offdiag_split_tc063).1.2.2.2 T).2
    rw [← h_bi_eq]
    have h_disj_u :
        (oddChainParts T : Set ℕ).PairwiseDisjoint
          (fun u => (dyadicChainExponents u T).image (fun j => 4 ^ j * u)) := by
      intro u1 hu1 u2 hu2 hu_ne
      change Disjoint _ _
      rw [Finset.disjoint_left]
      intro m hm1 hm2
      rcases Finset.mem_image.mp hm1 with ⟨j1, hj1, rfl⟩
      rcases Finset.mem_image.mp hm2 with ⟨j2, hj2, h_eq⟩
      have hm_in : 4 ^ j1 * u1 ∈ primeInteriorTruncatedAnchors 2 T := by
        rw [← h_bi_eq]; exact Finset.mem_biUnion.mpr ⟨u1, hu1, Finset.mem_image.mpr ⟨j1, hj1, rfl⟩⟩
      obtain ⟨_, _, h_u⟩ := h_uniq_m (4 ^ j1 * u1) hm_in
      have e1 := h_u (u1, j1) ⟨hu1, hj1, rfl⟩
      have e2 := h_u (u2, j2) ⟨hu2, hj2, h_eq⟩
      exact hu_ne (Prod.mk.inj (e1.trans e2.symm)).1
    rw [Finset.sum_biUnion h_disj_u]
    apply Finset.sum_congr rfl
    intro u hu
    have h_inj_j : Set.InjOn (fun j => 4 ^ j * u) ↑(dyadicChainExponents u T) := by
      intro j1 hj1 j2 hj2 h_eq
      have hm_in : 4 ^ j1 * u ∈ primeInteriorTruncatedAnchors 2 T := by
        rw [← h_bi_eq]; exact Finset.mem_biUnion.mpr ⟨u, hu, Finset.mem_image.mpr ⟨j1, hj1, rfl⟩⟩
      obtain ⟨_, _, h_u⟩ := h_uniq_m (4 ^ j1 * u) hm_in
      have e1 := h_u (u, j1) ⟨hu, hj1, rfl⟩
      have e2 := h_u (u, j2) ⟨hu, hj2, h_eq.symm⟩
      exact (Prod.mk.inj (e1.trans e2.symm)).2
    exact (Finset.sum_image h_inj_j).symm
  obtain ⟨_, h_U_sum_le, _, _⟩ := h_tc063_psi hY2
  obtain ⟨h_V_sum1, h_V_sum2⟩ :=
    (uniform_same_chain_hilbert_bound_and_closure_transfer_tc063).2.2.1.2 hY2 T
  have h_V_sum_le :
      (∑ m ∈ primeInteriorTruncatedAnchors 2 T,
        ∑ pk ∈ primePowerPairsUpTo T,
          windowEnergyNormSq Y (fun X => stationFeatureDiffV m pk X)) ≤ 2 * C_g :=
    le_trans h_V_sum1 h_V_sum2
  have h_cont_all := continuousOn_station_and_chain_profiles_tc064_aux hY2 c_lam c_half T D0
  have h_each_u :
      ∀ u ∈ oddChainParts T,
        |windowEnergyNormSq Y (oddChainAdjustedProfileUcal c_lam c_half T D0 u) -
            4 * ∑ pk ∈ primePowerPairsUpTo T,
              windowEnergyNormSq Y (fun X => oddChainFeatureVectorVcal u T pk X)| ≤
          (L : ℝ) *
            (∑ j ∈ dyadicChainExponents u T,
              (windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 (4 ^ j * u)) +
                4 * ∑ pk ∈ primePowerPairsUpTo T,
                  windowEnergyNormSq Y (fun X => stationFeatureDiffV (4 ^ j * u) pk X))) := by
    intro u hu
    have hJ_le_L : ((dyadicChainExponents u T).card : ℝ) ≤ (L : ℝ) := by
      exact_mod_cast Finset.le_sup (f := fun u => (dyadicChainExponents u T).card) hu
    have hU_u :
        windowEnergyNormSq Y (oddChainAdjustedProfileUcal c_lam c_half T D0 u) ≤
          (L : ℝ) * ∑ j ∈ dyadicChainExponents u T,
            windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 (4 ^ j * u)) := by
      unfold oddChainAdjustedProfileUcal
      exact le_trans
        (h_card_mink (dyadicChainExponents u T)
          (fun j => stationAdjustedDiffU c_lam c_half T D0 (4 ^ j * u))
          (fun j _ => h_cont_all.2.2.2.1 _))
        (mul_le_mul_of_nonneg_right hJ_le_L
          (Finset.sum_nonneg (fun _ _ => h_norm_nn _)))
    have hV_u :
        (∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => oddChainFeatureVectorVcal u T pk X)) ≤
          (L : ℝ) * ∑ j ∈ dyadicChainExponents u T,
            ∑ pk ∈ primePowerPairsUpTo T,
              windowEnergyNormSq Y (fun X => stationFeatureDiffV (4 ^ j * u) pk X) := by
      have h_each_pk :
          ∀ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => oddChainFeatureVectorVcal u T pk X) ≤
              (L : ℝ) * ∑ j ∈ dyadicChainExponents u T,
                windowEnergyNormSq Y (fun X => stationFeatureDiffV (4 ^ j * u) pk X) := by
        intro pk _
        unfold oddChainFeatureVectorVcal
        exact le_trans
          (h_card_mink (dyadicChainExponents u T)
            (fun j X => stationFeatureDiffV (4 ^ j * u) pk X)
            (fun j _ => h_cont_all.2.2.2.2.1 _ pk))
          (mul_le_mul_of_nonneg_right hJ_le_L
            (Finset.sum_nonneg (fun _ _ => h_norm_nn _)))
      calc
        _ ≤ ∑ pk ∈ primePowerPairsUpTo T,
              (L : ℝ) * ∑ j ∈ dyadicChainExponents u T,
                windowEnergyNormSq Y (fun X => stationFeatureDiffV (4 ^ j * u) pk X) :=
            Finset.sum_le_sum h_each_pk
        _ = (L : ℝ) * ∑ j ∈ dyadicChainExponents u T,
              ∑ pk ∈ primePowerPairsUpTo T,
                windowEnergyNormSq Y (fun X => stationFeatureDiffV (4 ^ j * u) pk X) := by
            rw [← Finset.mul_sum, Finset.sum_comm]
    have ht := abs_sub
      (windowEnergyNormSq Y (oddChainAdjustedProfileUcal c_lam c_half T D0 u))
      (4 * ∑ pk ∈ primePowerPairsUpTo T,
        windowEnergyNormSq Y (fun X => oddChainFeatureVectorVcal u T pk X))
    rw [abs_of_nonneg (h_norm_nn _),
      abs_of_nonneg (mul_nonneg (by norm_num) (Finset.sum_nonneg (fun _ _ => h_norm_nn _)))] at ht
    have h_rhs_split :
        (L : ℝ) *
            (∑ j ∈ dyadicChainExponents u T,
              (windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 (4 ^ j * u)) +
                4 * ∑ pk ∈ primePowerPairsUpTo T,
                  windowEnergyNormSq Y (fun X => stationFeatureDiffV (4 ^ j * u) pk X))) =
          (L : ℝ) * (∑ j ∈ dyadicChainExponents u T,
              windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 (4 ^ j * u))) +
            4 * ((L : ℝ) * ∑ j ∈ dyadicChainExponents u T,
              ∑ pk ∈ primePowerPairsUpTo T,
                windowEnergyNormSq Y (fun X => stationFeatureDiffV (4 ^ j * u) pk X)) := by
      rw [Finset.sum_add_distrib, ← Finset.mul_sum]; ring
    linarith
  calc
    |∑ u ∈ oddChainParts T,
        (windowEnergyNormSq Y (oddChainAdjustedProfileUcal c_lam c_half T D0 u) -
          4 * ∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => oddChainFeatureVectorVcal u T pk X))|
      ≤ ∑ u ∈ oddChainParts T,
          |windowEnergyNormSq Y (oddChainAdjustedProfileUcal c_lam c_half T D0 u) -
            4 * ∑ pk ∈ primePowerPairsUpTo T,
              windowEnergyNormSq Y (fun X => oddChainFeatureVectorVcal u T pk X)| :=
        Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ u ∈ oddChainParts T,
          (L : ℝ) *
            (∑ j ∈ dyadicChainExponents u T,
              (windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 (4 ^ j * u)) +
                4 * ∑ pk ∈ primePowerPairsUpTo T,
                  windowEnergyNormSq Y (fun X => stationFeatureDiffV (4 ^ j * u) pk X))) :=
        Finset.sum_le_sum h_each_u
    _ = (L : ℝ) *
          (∑ m ∈ primeInteriorTruncatedAnchors 2 T,
            (windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 m) +
              4 * ∑ pk ∈ primePowerPairsUpTo T,
                windowEnergyNormSq Y (fun X => stationFeatureDiffV m pk X))) := by
        rw [← Finset.mul_sum,
          h_bi_anchor (fun m => windowEnergyNormSq Y (stationAdjustedDiffU c_lam c_half T D0 m) +
            4 * ∑ pk ∈ primePowerPairsUpTo T,
              windowEnergyNormSq Y (fun X => stationFeatureDiffV m pk X))]
    _ ≤ (L : ℝ) * (2 * C_psi + 4 * (2 * C_g)) := by
        rw [Finset.sum_add_distrib, ← Finset.mul_sum]
        exact mul_le_mul_of_nonneg_left
          (add_le_add h_U_sum_le (mul_le_mul_of_nonneg_left h_V_sum_le (by norm_num)))
          (Nat.cast_nonneg L)
    _ ≤ (2 * (1 + Real.log Y)) * (2 * C_psi + 8 * C_g) := by
        rw [show 2 * C_psi + 4 * (2 * C_g) = 2 * C_psi + 8 * C_g by ring]
        exact mul_le_mul_of_nonneg_right hL_le2
          (add_nonneg (mul_nonneg (by norm_num : (0 : ℝ) ≤ 2) hCpsi_nn)
            (mul_nonneg (by norm_num : (0 : ℝ) ≤ 8) (le_of_lt hCg_pos)))
    _ = (4 * C_psi + 16 * C_g) * (1 + Real.log Y) := by ring

private theorem same_core_hilbert_and_remainder_bounds_tc064_aux (c_lam c_half : ℝ) :
    let C_tau : ℝ :=
      (16 / 5 : ℝ) * (2 + Real.sqrt 2) * RiemannScope.tau ^ (5 / 2 : ℝ) *
        Real.sqrt (Real.log RiemannScope.tau)
    let S_st : ℕ → ℕ → Finset ℕ := fun T a =>
      (coreSquareMultipliers a T).biUnion (fun b =>
        (dyadicChainExponents (a * b ^ 2) T).biUnion (fun j =>
          (Finset.range 2).image (fun eps => 2 ^ (2 * j + eps) * a * b ^ 2)))
    (∀ {C_osc : ℝ}, 0 ≤ C_osc →
      (∀ d : ℕ, 1 ≤ d →
        |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| ≤ C_osc * (d : ℝ)) →
      ∀ {Y : ℝ}, 2 ≤ Y →
        let T := canonicalCutoffT Y
        let D0 := Nat.floor (Real.log Y)
        Real.sqrt
            (∑ a ∈ oddSquarefreeCores T,
              windowEnergyNormSq Y
                (fun X =>
                  (1 / (Real.log X) ^ 2) *
                    (∑ k ∈ S_st T a,
                      (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                        ((∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => d ∣ k),
                            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                              (liouvilleLambda (k / d) : ℝ)) -
                          (∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => (d + 1) ∣ k),
                            (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                              (liouvilleLambda (k / (d + 1)) : ℝ))) *
                        gaussianTermPhi k X))) ≤
          4 * C_osc * C_tau) ∧
      (∃ C_core C_square : ℝ, 0 ≤ C_core ∧ 0 ≤ C_square ∧
        ∀ {Y : ℝ}, 2 ≤ Y →
          (∑ a ∈ oddSquarefreeCores (canonicalCutoffT Y),
            (windowEnergyNormSq Y
                (coreAdjustedProfileA c_lam c_half
                  (canonicalCutoffT Y) (Nat.floor (Real.log Y)) a) +
              ∑ pk ∈ primePowerPairsUpTo (canonicalCutoffT Y),
                windowEnergyNormSq Y
                  (fun X => coreFeatureVectorB a (canonicalCutoffT Y) pk X))) ≤
            C_core * (1 + Real.log Y) ∧
          |canonicalSameCoreSquareRemainderR c_lam c_half Y| ≤ C_square * (1 + Real.log Y)) := by
  intro C_tau S_st
  obtain ⟨hCtau_pos, h_st_A, h_st_disj, h_st_bare, h_st_div⟩ :=
    paired_core_station_set_and_divisor_norm_tc064_aux
  obtain ⟨h_elem_osc, h_beta_eq⟩ := openCoreAdjustedCoeffBeta_interior_eq_and_elem_osc_tc064_aux
  obtain ⟨_, h_bonus_small⟩ := small_divisor_jump_core_bounds_tc064_aux c_lam c_half
  obtain ⟨C_uv, hCuv_nn, h_uv_bd⟩ := odd_chain_diagonal_sum_bound_tc064_aux c_lam c_half
  have hCg_pos := (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2.1
  have htau_gt1 : (1 : ℝ) < RiemannScope.tau := by linarith
  have h_lam_abs : ∀ m : ℕ, |(liouvilleLambda m : ℝ)| ≤ 1 := by
    intro m
    by_cases hm : m = 0
    · subst hm; simp [liouvilleLambda]
    · simp [liouvilleLambda, hm, liouvilleSignFromOmega]
  have h_sgn_abs :
      ∀ (k q : ℕ), |(-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
          (liouvilleLambda q : ℝ)| ≤ 1 := by
    intro k q
    rw [abs_mul, abs_mul, abs_pow, abs_neg, abs_one, one_pow, one_mul]
    calc
      |(liouvilleLambda k : ℝ)| * |(liouvilleLambda q : ℝ)|
        ≤ 1 * 1 := mul_le_mul (h_lam_abs k) (h_lam_abs q) (abs_nonneg _) zero_le_one
      _ = 1 := one_mul 1
  let C_sm : ℝ := 4 + |c_lam| + |c_half|
  let B_end : ℝ :=
    16 * C_sm * RiemannScope.tau ^ (5 / 2 : ℝ) * Real.sqrt (Real.log RiemannScope.tau)
  let B_tot : ℝ :=
    (3 / 2 : ℝ) * C_tau + 4 * |c_lam| * C_tau + B_end +
      24 * (8 + |c_half|) * C_tau + 48 * C_tau * C_sm
  let C_feat : ℝ := (729 / 64 : ℝ) * C_tau ^ 2
  let C_core : ℝ := B_tot ^ 2 + C_feat
  let C_square : ℝ := 4 * C_core + C_uv
  have hCtau_nn : 0 ≤ C_tau := le_of_lt hCtau_pos
  have hCsm_nn : 0 ≤ C_sm := by dsimp [C_sm]; positivity
  have h8ch_nn : 0 ≤ 8 + |c_half| := add_nonneg (by norm_num) (abs_nonneg _)
  have htau_52_nn : 0 ≤ RiemannScope.tau ^ (5 / 2 : ℝ) * Real.sqrt (Real.log RiemannScope.tau) := by
    have hlog_tau : 0 < Real.log RiemannScope.tau := Real.log_pos htau_gt1
    positivity
  have hBend_nn : 0 ≤ B_end := by
    dsimp [B_end]
    rw [mul_assoc (16 * C_sm)]
    exact mul_nonneg (mul_nonneg (by norm_num) hCsm_nn) htau_52_nn
  have hCcore_nn : 0 ≤ C_core := by dsimp [C_core, C_feat]; positivity
  have hCsq_nn : 0 ≤ C_square := by dsimp [C_square]; positivity
  refine ⟨h_bonus_small, C_core, C_square, hCcore_nn, hCsq_nn, ?_⟩
  intro Y hY2
  have hY0 : 0 < Y := by linarith
  obtain ⟨hT_ge3, hlogY_gt, hlogT_le, hY52_le, h_rat4, h1logT_le⟩ :=
    canonical_log_and_cutoff_bounds_tc064_aux hY2
  obtain ⟨hle_win, hprops_win⟩ := uIcc_tau_log_props_tc064_aux hY2
  have hlogY_pos : 0 < Real.log Y := by linarith
  have h1_le_1logY : 1 ≤ Real.sqrt (1 + Real.log Y) :=
    Real.one_le_sqrt.mpr (by linarith)
  let T := canonicalCutoffT Y
  let D0 := Nat.floor (Real.log Y)
  let D_min := min D0 (T - 1)
  have hT1 : 1 ≤ T := by omega
  have hT2 : 2 ≤ T := by omega
  have hsqrt_1logT_le :
      Real.sqrt (1 + Real.log (T : ℝ)) ≤ (3 / 2 : ℝ) * Real.sqrt (1 + Real.log Y) := by
    calc
      Real.sqrt (1 + Real.log (T : ℝ))
        ≤ Real.sqrt ((9 / 4 : ℝ) * (1 + Real.log Y)) := Real.sqrt_le_sqrt h1logT_le
      _ = (3 / 2 : ℝ) * Real.sqrt (1 + Real.log Y) := by
          rw [Real.sqrt_mul (by norm_num), show (9 / 4 : ℝ) = (3 / 2 : ℝ) ^ 2 by norm_num,
            Real.sqrt_sq (by norm_num)]
  -- Feature vector sum bound:
  have h_feat_bd :
      (∑ a ∈ oddSquarefreeCores T,
          ∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X)) ≤
        C_feat * (1 + Real.log Y) := by
    have h_each_a_feat :
        ∀ a ∈ oddSquarefreeCores T,
          (∑ pk ∈ primePowerPairsUpTo T,
              windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X)) ≤
            ((9 / 4 : ℝ) ^ 2 * C_tau ^ 2) * ((1 : ℝ) / (a : ℝ)) := by
      intro a ha
      have ha1 : 1 ≤ a := (Finset.mem_Icc.mp (Finset.mem_filter.mp ha).1).1
      have ha_pos_r : (0 : ℝ) < (a : ℝ) := Nat.cast_pos.mpr ha1
      obtain ⟨h_sub_a, _, h_reidx_w⟩ := h_st_A T a ha
      have h_B_eq :
          ∀ pk : ℕ × ℕ,
            windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X) =
              windowEnergyNormSq Y
                (fun X => ∑ k ∈ S_st T a,
                  (-1 : ℝ) ^ (k.factorization 2) * stationPrimePowerFeatureG k pk X) := by
        intro pk
        congr 1; ext X
        unfold coreFeatureVectorB oddChainFeatureVectorVcal stationFeatureDiffV
        exact h_reidx_w (fun k => stationPrimePowerFeatureG k pk X)
      rw [Finset.sum_congr rfl (fun pk _ => h_B_eq pk)]
      have hc_G :
          ∀ k ∈ S_st T a, ∀ pk ∈ primePowerPairsUpTo T,
            ContinuousOn (fun X => (-1 : ℝ) ^ (k.factorization 2) * stationPrimePowerFeatureG k pk X)
              (Set.uIcc Y (RiemannScope.tau * Y)) :=
        fun k _ pk _ => continuousOn_const.mul
          ((continuousOn_station_and_chain_profiles_tc064_aux hY2 0 0 T 0).2.2.1 k pk)
      have h_mink_pk :=
        (direct_sum_window_minkowski_sq_tc064_aux hY0 (primePowerPairsUpTo T) (S_st T a)
          (fun k pk X => (-1 : ℝ) ^ (k.factorization 2) * stationPrimePowerFeatureG k pk X)
          hc_G).2
      have h_sgn_sq :
          ∀ (k : ℕ) (pk : ℕ × ℕ),
            windowEnergyNormSq Y
                (fun X => (-1 : ℝ) ^ (k.factorization 2) * stationPrimePowerFeatureG k pk X) =
              windowEnergyNormSq Y (fun X => stationPrimePowerFeatureG k pk X) := by
        intro k pk
        unfold windowEnergyNormSq windowPairing
        apply intervalIntegral.integral_congr
        intro X _
        have hs : ((-1 : ℝ) ^ (k.factorization 2)) ^ 2 = 1 := by
          rw [← pow_mul, show k.factorization 2 * 2 = 2 * k.factorization 2 by ring,
            pow_mul, show (-1 : ℝ) ^ 2 = 1 by norm_num, one_pow]
        calc
          ((-1 : ℝ) ^ (k.factorization 2) * stationPrimePowerFeatureG k pk X) *
              ((-1 : ℝ) ^ (k.factorization 2) * stationPrimePowerFeatureG k pk X) / X
            = ((-1 : ℝ) ^ (k.factorization 2)) ^ 2 *
                (stationPrimePowerFeatureG k pk X * stationPrimePowerFeatureG k pk X) / X := by ring
          _ = stationPrimePowerFeatureG k pk X * stationPrimePowerFeatureG k pk X / X := by
              rw [hs, one_mul]
      have h_each_k :
          ∀ k ∈ S_st T a,
            Real.sqrt
                (∑ pk ∈ primePowerPairsUpTo T,
                  windowEnergyNormSq Y
                    (fun X => (-1 : ℝ) ^ (k.factorization 2) * stationPrimePowerFeatureG k pk X)) ≤
              (9 / 4 : ℝ) * Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi k)) := by
        intro k hk
        rw [Finset.sum_congr rfl (fun pk _ => h_sgn_sq k pk)]
        have hk_Icc : k ∈ Finset.Icc 1 T := (Finset.mem_filter.mp (h_sub_a hk)).1
        have h_gn := stationPrimePowerFeatureG_norm_le_tc064_aux hY2 hk_Icc
        have h_rat : Real.log (T : ℝ) / Real.log Y ≤ 9 / 4 :=
          (div_le_iff hlogY_pos).mpr hlogT_le
        exact le_trans h_gn (mul_le_mul_of_nonneg_right h_rat (Real.sqrt_nonneg _))
      have h_sum_k :
          (∑ k ∈ S_st T a,
              Real.sqrt
                (∑ pk ∈ primePowerPairsUpTo T,
                  windowEnergyNormSq Y
                    (fun X => (-1 : ℝ) ^ (k.factorization 2) * stationPrimePowerFeatureG k pk X))) ≤
            (9 / 4 : ℝ) * (C_tau / Real.sqrt (a : ℝ)) := by
        calc
          _ ≤ ∑ k ∈ S_st T a, (9 / 4 : ℝ) * Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi k)) :=
              Finset.sum_le_sum h_each_k
          _ = (9 / 4 : ℝ) * ∑ k ∈ S_st T a, Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi k)) :=
              (Finset.mul_sum _ _ _).symm
          _ ≤ (9 / 4 : ℝ) * (C_tau / Real.sqrt (a : ℝ)) :=
              mul_le_mul_of_nonneg_left (h_st_bare hY0 T a ha) (by norm_num)
      have h_sq_k := pow_le_pow_left
        (Finset.sum_nonneg (fun _ _ => Real.sqrt_nonneg _)) h_sum_k 2
      calc
        _ ≤ ((9 / 4 : ℝ) * (C_tau / Real.sqrt (a : ℝ))) ^ 2 := le_trans h_mink_pk h_sq_k
        _ = ((9 / 4 : ℝ) ^ 2 * C_tau ^ 2) * ((1 : ℝ) / (a : ℝ)) := by
            rw [mul_pow, div_pow C_tau, Real.sq_sqrt (le_of_lt ha_pos_r)]; ring
    have h_sub_cores : oddSquarefreeCores T ⊆ Finset.Icc 1 T := Finset.filter_subset _ _
    calc
      (∑ a ∈ oddSquarefreeCores T,
          ∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X))
        ≤ ∑ a ∈ oddSquarefreeCores T, ((9 / 4 : ℝ) ^ 2 * C_tau ^ 2) * ((1 : ℝ) / (a : ℝ)) :=
          Finset.sum_le_sum h_each_a_feat
      _ = ((9 / 4 : ℝ) ^ 2 * C_tau ^ 2) * ∑ a ∈ oddSquarefreeCores T, (1 : ℝ) / (a : ℝ) :=
          (Finset.mul_sum _ _ _).symm
      _ ≤ ((9 / 4 : ℝ) ^ 2 * C_tau ^ 2) * ∑ a ∈ Finset.Icc 1 T, (1 : ℝ) / (a : ℝ) :=
          mul_le_mul_of_nonneg_left
            (Finset.sum_le_sum_of_subset_of_nonneg h_sub_cores (fun _ _ _ => by positivity))
            (by positivity)
      _ ≤ ((9 / 4 : ℝ) ^ 2 * C_tau ^ 2) * (1 + Real.log (T : ℝ)) :=
          mul_le_mul_of_nonneg_left (sum_inv_Icc_one_le_one_add_log_tc064_aux hT1) (by positivity)
      _ ≤ ((9 / 4 : ℝ) ^ 2 * C_tau ^ 2) * ((9 / 4 : ℝ) * (1 + Real.log Y)) :=
          mul_le_mul_of_nonneg_left h1logT_le (by positivity)
      _ = C_feat * (1 + Real.log Y) := by dsimp [C_feat]; ring
  -- 5-piece decomposition of coreAdjustedProfileA:
  let F_p : Fin 5 → ℕ → ℝ → ℝ := fun i a X =>
    match i.val with
    | 0 => ∑ k ∈ S_st T a, (-1 : ℝ) ^ (k.factorization 2) * gaussianTermPhi k X
    | 1 => (1 / (Real.log X) ^ 2) *
        (c_lam * ∑ k ∈ S_st T a,
          (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
            (if IsSquare k then 1 else 0) * gaussianTermPhi k X)
    | 2 => (1 / (Real.log X) ^ 2) *
        ((selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T) *
          ∑ k ∈ (S_st T a).filter (fun k => k = T),
            (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) * gaussianTermPhi k X)
    | 3 => (1 / (Real.log X) ^ 2) *
        (∑ e ∈ Finset.Icc 1 T,
          (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
            (∑ k ∈ (S_st T a).filter (fun k => e ∣ k),
              (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                (liouvilleLambda (k / e) : ℝ) * gaussianTermPhi k X))
    | _ => (1 / (Real.log X) ^ 2) *
        (∑ k ∈ S_st T a,
          (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
            ((∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k),
                (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                  (liouvilleLambda (k / d) : ℝ)) -
              (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k),
                (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                  (liouvilleLambda (k / (d + 1)) : ℝ))) *
            gaussianTermPhi k X)
  have hc_phi : ∀ k : ℕ, ContinuousOn (gaussianTermPhi k) (Set.uIcc Y (RiemannScope.tau * Y)) :=
    continuousOn_gaussianTermPhi_param_tc064_aux Y RiemannScope.tau
  have hlog_inv2_cont :
      ContinuousOn (fun X => 1 / (Real.log X) ^ 2) (Set.uIcc Y (RiemannScope.tau * Y)) :=
    continuousOn_const.div
      ((ContinuousOn.log continuousOn_id (fun X hX => ne_of_gt (hprops_win X hX).1)).pow 2)
      (fun X hX => (hprops_win X hX).2.2.2)
  have hc_Fp :
      ∀ i ∈ (Finset.univ : Finset (Fin 5)), ∀ a ∈ oddSquarefreeCores T,
        ContinuousOn (F_p i a) (Set.uIcc Y (RiemannScope.tau * Y)) := by
    intro i _ a _
    fin_cases i
    · dsimp [F_p]; exact continuousOn_finset_sum _ (fun k _ => continuousOn_const.mul (hc_phi k))
    · dsimp [F_p]
      exact hlog_inv2_cont.mul (continuousOn_const.mul
        (continuousOn_finset_sum _ (fun k _ => continuousOn_const.mul (hc_phi k))))
    · dsimp [F_p]
      exact hlog_inv2_cont.mul (continuousOn_const.mul
        (continuousOn_finset_sum _ (fun k _ => continuousOn_const.mul (hc_phi k))))
    · dsimp [F_p]
      exact hlog_inv2_cont.mul (continuousOn_finset_sum _ (fun e _ => continuousOn_const.mul
        (continuousOn_finset_sum _ (fun k _ => continuousOn_const.mul (hc_phi k)))))
    · dsimp [F_p]
      exact hlog_inv2_cont.mul
        (continuousOn_finset_sum _ (fun k _ => continuousOn_const.mul (hc_phi k)))
  have h_A_eq_sum5 :
      ∀ a ∈ oddSquarefreeCores T,
        windowEnergyNormSq Y (coreAdjustedProfileA c_lam c_half T D0 a) =
          windowEnergyNormSq Y (fun X => ∑ i : Fin 5, F_p i a X) := by
    intro a ha
    obtain ⟨h_sub_a, _, h_reidx_w⟩ := h_st_A T a ha
    unfold windowEnergyNormSq windowPairing
    apply intervalIntegral.integral_congr
    intro X _hX
    have hA_X :
        coreAdjustedProfileA c_lam c_half T D0 a X =
          ∑ k ∈ S_st T a, (-1 : ℝ) ^ (k.factorization 2) *
            adjustedStationProfilePsi c_lam c_half T D0 k X := by
      unfold coreAdjustedProfileA oddChainAdjustedProfileUcal stationAdjustedDiffU
      exact h_reidx_w (fun k => adjustedStationProfilePsi c_lam c_half T D0 k X)
    have h_psi_k :
        ∀ k ∈ S_st T a,
          (-1 : ℝ) ^ (k.factorization 2) * adjustedStationProfilePsi c_lam c_half T D0 k X =
            (-1 : ℝ) ^ (k.factorization 2) * gaussianTermPhi k X +
              (1 / (Real.log X) ^ 2) *
                (c_lam * ((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                  (if IsSquare k then 1 else 0) * gaussianTermPhi k X)) +
              (1 / (Real.log X) ^ 2) *
                ((selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T) *
                  (if k = T then
                    (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) * gaussianTermPhi k X
                  else 0)) +
              (1 / (Real.log X) ^ 2) *
                (∑ e ∈ Finset.Icc 1 T,
                  if e ∣ k then
                    (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                      ((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                        (liouvilleLambda (k / e) : ℝ) * gaussianTermPhi k X)
                  else 0) +
              (1 / (Real.log X) ^ 2) *
                ((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                  ((∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => d ∣ k),
                      (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                        (liouvilleLambda (k / d) : ℝ)) -
                    (∑ d ∈ (Finset.Icc 1 D_min).filter (fun d => (d + 1) ∣ k),
                      (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                        (liouvilleLambda (k / (d + 1)) : ℝ))) *
                  gaussianTermPhi k X) := by
      intro k hk
      have hk_Icc : k ∈ Finset.Icc 1 T := (Finset.mem_filter.mp (h_sub_a hk)).1
      unfold adjustedStationProfilePsi signedAdjustedCoeffB
      rw [h_beta_eq hT2 D0 c_lam c_half k hk_Icc]
      have he_dist :
          (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
              (∑ e ∈ (Finset.Icc 1 T).filter (fun e => e ∣ k),
                (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                  (liouvilleLambda (k / e) : ℝ)) * gaussianTermPhi k X =
            ∑ e ∈ (Finset.Icc 1 T).filter (fun e => e ∣ k),
              (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                ((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                  (liouvilleLambda (k / e) : ℝ) * gaussianTermPhi k X) := by
        rw [Finset.mul_sum, Finset.sum_mul]
        apply Finset.sum_congr rfl; intro _ _; ring
      have hT_ite :
          (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
              (if k = T then selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T else 0) *
              gaussianTermPhi k X =
            (selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T) *
              (if k = T then
                (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) * gaussianTermPhi k X
              else 0) := by
        split_ifs <;> ring
      rw [← Finset.sum_filter, ← he_dist, ← hT_ite]
      dsimp only [D_min]
      ring
    have h_sum_5 : coreAdjustedProfileA c_lam c_half T D0 a X = ∑ i : Fin 5, F_p i a X := by
      rw [hA_X, Finset.sum_congr rfl h_psi_k, Finset.sum_add_distrib, Finset.sum_add_distrib,
        Finset.sum_add_distrib, Finset.sum_add_distrib]
      rw [Fin.sum_univ_five]
      dsimp [F_p]
      rw [← Finset.mul_sum, ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.mul_sum,
        ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.sum_filter, Finset.sum_comm]
      have h_e_comm :
          (∑ e ∈ Finset.Icc 1 T, ∑ k ∈ S_st T a,
              if e ∣ k then
                (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                  ((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                    (liouvilleLambda (k / e) : ℝ) * gaussianTermPhi k X)
              else 0) =
            ∑ e ∈ Finset.Icc 1 T,
              (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
                (∑ k ∈ (S_st T a).filter (fun k => e ∣ k),
                  (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                    (liouvilleLambda (k / e) : ℝ) * gaussianTermPhi k X) := by
        apply Finset.sum_congr rfl
        intro e _; rw [← Finset.sum_filter, ← Finset.mul_sum]
      rw [h_e_comm]
    dsimp only
    rw [h_sum_5]
  -- Bound each of the 5 direct-sum norms:
  -- Piece 0 (bare phi_k):
  have h_N0 :
      Real.sqrt (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (F_p 0 a)) ≤
        (3 / 2 : ℝ) * C_tau * Real.sqrt (1 + Real.log Y) := by
    have h_each :
        ∀ a ∈ oddSquarefreeCores T,
          windowEnergyNormSq Y (F_p 0 a) ≤ C_tau ^ 2 * ((1 : ℝ) / (a : ℝ)) := by
      intro a ha
      have ha_pos : (0 : ℝ) < (a : ℝ) := Nat.cast_pos.mpr (Finset.mem_Icc.mp (Finset.mem_filter.mp ha).1).1
      have hw := weighted_gaussian_sum_window_norm_le_tc064_aux hY0 (S_st T a)
        (fun k => (-1 : ℝ) ^ (k.factorization 2)) zero_le_one
        (fun k _ => by rw [abs_pow, abs_neg, abs_one, one_pow])
      have hb := pow_le_pow_left
        (Finset.sum_nonneg (fun _ _ => Real.sqrt_nonneg _)) (h_st_bare hY0 T a ha) 2
      dsimp [F_p]
      calc
        windowEnergyNormSq Y (fun X => ∑ k ∈ S_st T a, (-1 : ℝ) ^ (k.factorization 2) * gaussianTermPhi k X)
          ≤ 1 ^ 2 * (C_tau / Real.sqrt (a : ℝ)) ^ 2 := le_trans hw (by linarith)
        _ = C_tau ^ 2 * ((1 : ℝ) / (a : ℝ)) := by
            rw [one_pow, one_mul, div_pow, Real.sq_sqrt (le_of_lt ha_pos)]; ring
    have h_sum :
        (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (F_p 0 a)) ≤
          ((3 / 2 : ℝ) * C_tau * Real.sqrt (1 + Real.log Y)) ^ 2 := by
      calc
        _ ≤ ∑ a ∈ oddSquarefreeCores T, C_tau ^ 2 * ((1 : ℝ) / (a : ℝ)) := Finset.sum_le_sum h_each
        _ = C_tau ^ 2 * ∑ a ∈ oddSquarefreeCores T, (1 : ℝ) / (a : ℝ) := (Finset.mul_sum _ _ _).symm
        _ ≤ C_tau ^ 2 * ∑ a ∈ Finset.Icc 1 T, (1 : ℝ) / (a : ℝ) :=
            mul_le_mul_of_nonneg_left
              (Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
                (fun _ _ _ => by positivity)) (sq_nonneg _)
        _ ≤ C_tau ^ 2 * (1 + Real.log (T : ℝ)) :=
            mul_le_mul_of_nonneg_left (sum_inv_Icc_one_le_one_add_log_tc064_aux hT1) (sq_nonneg _)
        _ ≤ C_tau ^ 2 * ((9 / 4 : ℝ) * (1 + Real.log Y)) :=
            mul_le_mul_of_nonneg_left h1logT_le (sq_nonneg _)
        _ = ((3 / 2 : ℝ) * C_tau * Real.sqrt (1 + Real.log Y)) ^ 2 := by
            symm
            rw [mul_pow, mul_pow, Real.sq_sqrt (by linarith)]; ring
    calc
      Real.sqrt (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (F_p 0 a))
        ≤ Real.sqrt (((3 / 2 : ℝ) * C_tau * Real.sqrt (1 + Real.log Y)) ^ 2) :=
          Real.sqrt_le_sqrt h_sum
      _ = (3 / 2 : ℝ) * C_tau * Real.sqrt (1 + Real.log Y) := Real.sqrt_sq (by positivity)
  -- Piece 1 (square cancellation, supported only on a = 1):
  have h_N1 :
      Real.sqrt (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (F_p 1 a)) ≤
        4 * |c_lam| * C_tau * Real.sqrt (1 + Real.log Y) := by
    have h1_in : 1 ∈ oddSquarefreeCores T := by
      simp only [oddSquarefreeCores, Finset.mem_filter, Finset.mem_Icc]
      exact ⟨⟨le_refl 1, by omega⟩, odd_one, squarefree_one, by omega⟩
    have h_zero_ne1 :
        ∀ a ∈ (oddSquarefreeCores T).erase 1, windowEnergyNormSq Y (F_p 1 a) = 0 := by
      intro a ha
      obtain ⟨ha_ne1, ha_in⟩ := Finset.mem_erase.mp ha
      have h_sq1 := (h_st_A T a ha_in).2.1
      have hF_z : ∀ X : ℝ, F_p 1 a X = 0 := by
        intro X
        dsimp [F_p]
        have hs0 :
            (∑ k ∈ S_st T a,
                (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                  (if IsSquare k then 1 else 0) * gaussianTermPhi k X) = 0 := by
          apply Finset.sum_eq_zero
          intro k hk
          have hnsq : ¬ IsSquare k := fun hsq => ha_ne1 (h_sq1 k hk hsq)
          rw [if_neg hnsq]; ring
        rw [hs0]; ring
      unfold windowEnergyNormSq windowPairing
      simp [hF_z]
    rw [← Finset.add_sum_erase _ _ h1_in, Finset.sum_eq_zero h_zero_ne1, add_zero]
    have h_a1 :
        windowEnergyNormSq Y (F_p 1 1) ≤ (4 * |c_lam| * C_tau) ^ 2 := by
      let g_a1 : ℝ → ℝ := fun X =>
        c_lam * ∑ k ∈ S_st T 1,
          (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
            (if IsSquare k then 1 else 0) * gaussianTermPhi k X
      have h_lp := log_sq_inv_windowEnergy_le_tc064_aux (h := g_a1) hY2
        (continuousOn_const.mul
          (continuousOn_finset_sum _ (fun k _ => continuousOn_const.mul (hc_phi k))))
      have h_mul_c : windowEnergyNormSq Y g_a1 ≤ c_lam ^ 2 * C_tau ^ 2 := by
        have hs :
            windowEnergyNormSq Y g_a1 =
              c_lam ^ 2 * windowEnergyNormSq Y
                (fun X => ∑ k ∈ S_st T 1,
                  ((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                    (if IsSquare k then 1 else 0)) * gaussianTermPhi k X) := by
          unfold windowEnergyNormSq windowPairing
          rw [← intervalIntegral.integral_const_mul]
          apply intervalIntegral.integral_congr; intro X _; dsimp [g_a1]; ring
        rw [hs]
        have hw := weighted_gaussian_sum_window_norm_le_tc064_aux hY0 (S_st T 1)
          (fun k => (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
            (if IsSquare k then 1 else 0)) zero_le_one
          (fun k _ => by
            dsimp only
            split_ifs
            · rw [mul_one, ← mul_one (liouvilleLambda k : ℝ)]
              have hs := h_sgn_abs k 1
              have hl1 : (liouvilleLambda 1 : ℝ) = 1 := by
                simp [liouvilleLambda, natOmega, liouvilleSignFromOmega]
              rwa [hl1, mul_assoc] at hs
            · simp)
        have hb := h_st_bare hY0 T 1 h1_in
        rw [Nat.cast_one, Real.sqrt_one, div_one] at hb
        have hb2 := pow_le_pow_left
          (Finset.sum_nonneg (fun _ _ => Real.sqrt_nonneg _)) hb 2
        have hw_le :
            windowEnergyNormSq Y
                (fun X => ∑ k ∈ S_st T 1,
                  ((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                    (if IsSquare k then 1 else 0)) * gaussianTermPhi k X) ≤
              C_tau ^ 2 := by
          rw [one_pow, one_mul] at hw
          exact le_trans hw hb2
        exact mul_le_mul_of_nonneg_left hw_le (sq_nonneg c_lam)
      have h_inv_log4 : 1 / (Real.log Y) ^ 4 ≤ 16 := by
        have h_gt_half : (1 / 2 : ℝ) ^ 4 ≤ (Real.log Y) ^ 4 :=
          pow_le_pow_left (by norm_num) (by linarith : (1 / 2 : ℝ) ≤ Real.log Y) 4
        have h16 : (1 : ℝ) / (1 / 2 : ℝ) ^ 4 = 16 := by norm_num
        rw [← h16]
        exact one_div_le_one_div_of_le (by norm_num) h_gt_half
      change windowEnergyNormSq Y (fun X => (1 / (Real.log X) ^ 2) * g_a1 X) ≤
        (4 * |c_lam| * C_tau) ^ 2
      calc
        windowEnergyNormSq Y (fun X => (1 / (Real.log X) ^ 2) * g_a1 X)
          ≤ (1 / (Real.log Y) ^ 4) * (c_lam ^ 2 * C_tau ^ 2) :=
            le_trans h_lp (mul_le_mul_of_nonneg_left h_mul_c
              (div_nonneg zero_le_one (pow_nonneg (le_of_lt hlogY_pos) 4)))
        _ ≤ 16 * (c_lam ^ 2 * C_tau ^ 2) :=
            mul_le_mul_of_nonneg_right h_inv_log4 (mul_nonneg (sq_nonneg _) (sq_nonneg _))
        _ = (4 * |c_lam| * C_tau) ^ 2 := by
            have hc_sq : |c_lam| ^ 2 = c_lam ^ 2 := sq_abs c_lam
            calc
              16 * (c_lam ^ 2 * C_tau ^ 2) = 16 * |c_lam| ^ 2 * C_tau ^ 2 := by rw [hc_sq]; ring
              _ = (4 * |c_lam| * C_tau) ^ 2 := by ring
    calc
      Real.sqrt (windowEnergyNormSq Y (F_p 1 1))
        ≤ Real.sqrt ((4 * |c_lam| * C_tau) ^ 2) := Real.sqrt_le_sqrt h_a1
      _ = 4 * |c_lam| * C_tau := Real.sqrt_sq (by positivity)
      _ ≤ 4 * |c_lam| * C_tau * Real.sqrt (1 + Real.log Y) :=
          le_mul_of_one_le_right (by positivity) h1_le_1logY
  -- Piece 2 (endpoint k = T, active in at most one core a):
  have h_N2 :
      Real.sqrt (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (F_p 2 a)) ≤
        B_end * Real.sqrt (1 + Real.log Y) := by
    let R_T := selbergCenteredRemainderInt c_lam T - squarePoleDriftM c_half T
    have h_card_T : ((oddSquarefreeCores T).filter (fun a => T ∈ S_st T a)).card ≤ 1 := by
      rw [Finset.card_le_one]
      intro a1 ha1 a2 ha2
      simp only [Finset.mem_filter] at ha1 ha2
      by_contra h_ne
      exact Finset.disjoint_left.mp (h_st_disj T a1 ha1.1 a2 ha2.1 h_ne) ha1.2 ha2.2
    have h_each_T :
        ∀ a ∈ oddSquarefreeCores T,
          windowEnergyNormSq Y (F_p 2 a) ≤
            if T ∈ S_st T a then B_end ^ 2 else 0 := by
      intro a _
      by_cases hT_in : T ∈ S_st T a
      · rw [if_pos hT_in]
        have hf_eq : (S_st T a).filter (fun k => k = T) = {T} := by
          ext k; simp only [Finset.mem_filter, Finset.mem_singleton]
          exact ⟨fun h => h.2, fun h => ⟨h.symm ▸ hT_in, h⟩⟩
        obtain ⟨c_T, hcT_def, hcT_sq⟩ :
            ∃ c_T : ℝ,
              c_T = R_T * ((-1 : ℝ) ^ (T.factorization 2) * (liouvilleLambda T : ℝ)) ∧
                c_T ^ 2 ≤ R_T ^ 2 := by
          refine ⟨R_T * ((-1 : ℝ) ^ (T.factorization 2) * (liouvilleLambda T : ℝ)), rfl, ?_⟩
          have hs1 : ((-1 : ℝ) ^ (T.factorization 2)) ^ 2 = 1 := by
            rw [← pow_mul, mul_comm, pow_mul, show (-1 : ℝ) ^ 2 = 1 by norm_num, one_pow]
          have hl_sq : (liouvilleLambda T : ℝ) ^ 2 ≤ 1 := by
            have hp := pow_le_pow_left (abs_nonneg _) (h_lam_abs T) 2
            rwa [sq_abs, one_pow] at hp
          calc
            (R_T * ((-1 : ℝ) ^ (T.factorization 2) * (liouvilleLambda T : ℝ))) ^ 2
              = R_T ^ 2 * (((-1 : ℝ) ^ (T.factorization 2)) ^ 2 *
                  (liouvilleLambda T : ℝ) ^ 2) := by ring
            _ = R_T ^ 2 * (liouvilleLambda T : ℝ) ^ 2 := by rw [hs1, one_mul]
            _ ≤ R_T ^ 2 * 1 := mul_le_mul_of_nonneg_left hl_sq (sq_nonneg R_T)
            _ = R_T ^ 2 := mul_one _
        let g_T : ℝ → ℝ := fun X => c_T * gaussianTermPhi T X
        have hF2_fn : F_p 2 a = fun X => (1 / (Real.log X) ^ 2) * g_T X := by
          funext X
          change (1 / (Real.log X) ^ 2) *
              (R_T * ∑ k ∈ (S_st T a).filter (fun k => k = T),
                (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) * gaussianTermPhi k X) =
            (1 / (Real.log X) ^ 2) * (c_T * gaussianTermPhi T X)
          rw [hf_eq, Finset.sum_singleton, hcT_def]
          ring
        rw [hF2_fn]
        have h_lp := log_sq_inv_windowEnergy_le_tc064_aux (h := g_T) hY2
          (continuousOn_const.mul (hc_phi T))
        have h_sc :
            windowEnergyNormSq Y g_T ≤
              R_T ^ 2 * windowEnergyNormSq Y (gaussianTermPhi T) := by
          have hc_eq :
              windowEnergyNormSq Y g_T = c_T ^ 2 * windowEnergyNormSq Y (gaussianTermPhi T) := by
            unfold windowEnergyNormSq windowPairing
            rw [← intervalIntegral.integral_const_mul]
            apply intervalIntegral.integral_congr; intro X _; dsimp only [g_T]; ring
          have h_nn : 0 ≤ windowEnergyNormSq Y (gaussianTermPhi T) := by
            unfold windowEnergyNormSq windowPairing
            apply intervalIntegral.integral_nonneg hle_win
            intro X hX; exact div_nonneg (mul_self_nonneg _) (by linarith [hX.1])
          rw [hc_eq]
          exact mul_le_mul_of_nonneg_right hcT_sq h_nn
        have h_phi_T := paramWindowNormSq_gaussianTermPhi_sqrt_le_tc064_aux htau_gt1 hY0 hT1
        have hexp_T : Real.exp (-(Y ^ 2) / (T : ℝ) ^ 2) ≤ 1 := by
          rw [Real.exp_le_one_iff]
          exact div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg Y)) (sq_nonneg _)
        have hT_pos_r : (0 : ℝ) < (T : ℝ) := Nat.cast_pos.mpr hT1
        have h_sqrt_phi_T :
            Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi T)) ≤
              RiemannScope.tau ^ (5 / 2 : ℝ) * Real.sqrt (Real.log RiemannScope.tau) / (T : ℝ) := by
          have h_num_nn :
              0 ≤ RiemannScope.tau ^ (5 / 2 : ℝ) * Real.sqrt (Real.log RiemannScope.tau) *
                Y ^ (5 / 2 : ℝ) / (T : ℝ) ^ 3 :=
            div_nonneg (mul_nonneg htau_52_nn (Real.rpow_nonneg (le_of_lt hY0) _))
              (pow_nonneg (le_of_lt hT_pos_r) 3)
          calc
            Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi T))
              ≤ RiemannScope.tau ^ (5 / 2 : ℝ) * Real.sqrt (Real.log RiemannScope.tau) *
                  Y ^ (5 / 2 : ℝ) / (T : ℝ) ^ 3 * 1 :=
                le_trans h_phi_T (mul_le_mul_of_nonneg_left hexp_T h_num_nn)
            _ ≤ RiemannScope.tau ^ (5 / 2 : ℝ) * Real.sqrt (Real.log RiemannScope.tau) *
                  (T : ℝ) ^ 2 / (T : ℝ) ^ 3 := by
                rw [mul_one]
                exact div_le_div_of_nonneg_right
                  (mul_le_mul_of_nonneg_left hY52_le htau_52_nn)
                  (pow_nonneg (le_of_lt hT_pos_r) 3)
            _ = RiemannScope.tau ^ (5 / 2 : ℝ) * Real.sqrt (Real.log RiemannScope.tau) / (T : ℝ) := by
                field_simp [ne_of_gt hT_pos_r]; ring
        have hR_T := h_elem_osc c_lam c_half hT1
        have h_prod_T :
            (1 / (Real.log Y) ^ 2) * |R_T| *
                Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi T)) ≤
              B_end := by
          have h_rhs_R_nn : 0 ≤ C_sm * (T : ℝ) * (1 + Real.log (T : ℝ)) ^ 2 :=
            mul_nonneg (mul_nonneg hCsm_nn (le_of_lt hT_pos_r)) (sq_nonneg _)
          have h1 := mul_le_mul hR_T h_sqrt_phi_T (Real.sqrt_nonneg _) h_rhs_R_nn
          have h2 := mul_le_mul_of_nonneg_left h1
            (div_nonneg zero_le_one (sq_nonneg (Real.log Y)))
          have h_rat_sq : ((1 + Real.log (T : ℝ)) / Real.log Y) ^ 2 ≤ 16 := by
            have h_nn : 0 ≤ (1 + Real.log (T : ℝ)) / Real.log Y :=
              div_nonneg (add_nonneg zero_le_one (Real.log_nonneg (by exact_mod_cast hT1)))
                (le_of_lt hlogY_pos)
            calc
              ((1 + Real.log (T : ℝ)) / Real.log Y) ^ 2 ≤ 4 ^ 2 := pow_le_pow_left h_nn h_rat4 2
              _ = 16 := by norm_num
          have h_alg :
              (1 / (Real.log Y) ^ 2) *
                  ((C_sm * (T : ℝ) * (1 + Real.log (T : ℝ)) ^ 2) *
                    (RiemannScope.tau ^ (5 / 2 : ℝ) *
                      Real.sqrt (Real.log RiemannScope.tau) / (T : ℝ))) =
                ((1 + Real.log (T : ℝ)) / Real.log Y) ^ 2 *
                  (C_sm * (RiemannScope.tau ^ (5 / 2 : ℝ) *
                    Real.sqrt (Real.log RiemannScope.tau))) := by
            field_simp [ne_of_gt hT_pos_r, ne_of_gt hlogY_pos]; ring
          dsimp only [R_T] at h2 ⊢
          rw [← mul_assoc, h_alg] at h2
          have h3 := mul_le_mul_of_nonneg_right h_rat_sq (mul_nonneg hCsm_nn htau_52_nn)
          have h_be :
              16 * (C_sm * (RiemannScope.tau ^ (5 / 2 : ℝ) *
                  Real.sqrt (Real.log RiemannScope.tau))) = B_end := by
            dsimp [B_end]; ring
          rw [h_be] at h3
          exact le_trans h2 h3
        have h_sq_prod := pow_le_pow_left
          (mul_nonneg (mul_nonneg (div_nonneg zero_le_one (sq_nonneg _)) (abs_nonneg _))
            (Real.sqrt_nonneg _)) h_prod_T 2
        have h_phi_nn : 0 ≤ windowEnergyNormSq Y (gaussianTermPhi T) := by
          unfold windowEnergyNormSq windowPairing
          apply intervalIntegral.integral_nonneg hle_win
          intro X hX; exact div_nonneg (mul_self_nonneg _) (by linarith [hX.1])
        calc
          windowEnergyNormSq Y (fun X => (1 / (Real.log X) ^ 2) * g_T X)
            ≤ (1 / (Real.log Y) ^ 4) * (R_T ^ 2 * windowEnergyNormSq Y (gaussianTermPhi T)) :=
              le_trans h_lp (mul_le_mul_of_nonneg_left h_sc
                (div_nonneg zero_le_one (pow_nonneg (le_of_lt hlogY_pos) 4)))
          _ = ((1 / (Real.log Y) ^ 2) * |R_T| *
                Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi T))) ^ 2 := by
              have hR_sq : |R_T| ^ 2 = R_T ^ 2 := sq_abs R_T
              have hphi_sq : (Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi T))) ^ 2 =
                  windowEnergyNormSq Y (gaussianTermPhi T) := Real.sq_sqrt h_phi_nn
              calc
                (1 / (Real.log Y) ^ 4) * (R_T ^ 2 * windowEnergyNormSq Y (gaussianTermPhi T))
                  = (1 / (Real.log Y) ^ 4) * (|R_T| ^ 2 *
                      (Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi T))) ^ 2) := by
                      rw [hR_sq, hphi_sq]
                _ = ((1 / (Real.log Y) ^ 2) * |R_T| *
                      Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi T))) ^ 2 := by ring
          _ ≤ B_end ^ 2 := h_sq_prod
      · rw [if_neg hT_in]
        have hf_emp : (S_st T a).filter (fun k => k = T) = ∅ := by
          ext k; simp only [Finset.mem_filter, Finset.not_mem_empty, iff_false]
          rintro ⟨hk, rfl⟩; exact hT_in hk
        dsimp [F_p]; rw [hf_emp]
        simp [windowEnergyNormSq, windowPairing]
    have h_sum_T :
        (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (F_p 2 a)) ≤ B_end ^ 2 := by
      calc
        _ ≤ ∑ a ∈ oddSquarefreeCores T, (if T ∈ S_st T a then B_end ^ 2 else 0) :=
            Finset.sum_le_sum h_each_T
        _ = (((oddSquarefreeCores T).filter (fun a => T ∈ S_st T a)).card : ℝ) * B_end ^ 2 := by
            rw [← Finset.sum_filter]; simp
        _ ≤ 1 * B_end ^ 2 := mul_le_mul_of_nonneg_right (by exact_mod_cast h_card_T) (sq_nonneg _)
        _ = B_end ^ 2 := one_mul _
    calc
      Real.sqrt (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (F_p 2 a))
        ≤ Real.sqrt (B_end ^ 2) := Real.sqrt_le_sqrt h_sum_T
      _ = B_end := Real.sqrt_sq hBend_nn
      _ ≤ B_end * Real.sqrt (1 + Real.log Y) :=
          le_mul_of_one_le_right hBend_nn h1_le_1logY
  -- Piece 3 (full divisor drift 1 <= e <= T):
  have h_N3 :
      Real.sqrt (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (F_p 3 a)) ≤
        24 * (8 + |c_half|) * C_tau * Real.sqrt (1 + Real.log Y) := by
    let H_e : ℕ → ℕ → ℝ → ℝ := fun e a X =>
      (squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)) *
        (∑ k ∈ (S_st T a).filter (fun k => e ∣ k),
          ((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
            (liouvilleLambda (k / e) : ℝ)) * gaussianTermPhi k X)
    have hc_He :
        ∀ e ∈ Finset.Icc 1 T, ∀ a ∈ oddSquarefreeCores T,
          ContinuousOn (H_e e a) (Set.uIcc Y (RiemannScope.tau * Y)) :=
      fun _ _ _ _ => continuousOn_const.mul
        (continuousOn_finset_sum _ (fun k _ => continuousOn_const.mul (hc_phi k)))
    have h_lp :
        (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (F_p 3 a)) ≤
          (1 / (Real.log Y) ^ 4) *
            (∑ a ∈ oddSquarefreeCores T,
              windowEnergyNormSq Y (fun X => ∑ e ∈ Finset.Icc 1 T, H_e e a X)) := by
      rw [Finset.mul_sum]
      apply Finset.sum_le_sum
      intro a ha
      dsimp [F_p, H_e]
      exact log_sq_inv_windowEnergy_le_tc064_aux hY2
        (continuousOn_finset_sum _ (fun e he => hc_He e he a ha))
    have h_mink_e :=
      (direct_sum_window_minkowski_sq_tc064_aux hY0 (oddSquarefreeCores T) (Finset.Icc 1 T)
        H_e hc_He).1
    have h_each_e :
        ∀ e ∈ Finset.Icc 1 T,
          Real.sqrt (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (H_e e a)) ≤
            ((8 + |c_half|) * C_tau * (1 + Real.log (T : ℝ)) *
              Real.sqrt (1 + Real.log (T : ℝ))) * ((1 : ℝ) / (e : ℝ)) := by
      intro e he
      obtain ⟨he1, heT⟩ := Finset.mem_Icc.mp he
      have he_pos_r : (0 : ℝ) < (e : ℝ) := Nat.cast_pos.mpr he1
      let dM := squarePoleDriftM c_half e - squarePoleDriftM c_half (e - 1)
      have h_sc :
          (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (H_e e a)) =
            dM ^ 2 * ∑ a ∈ oddSquarefreeCores T,
              windowEnergyNormSq Y (fun X => ∑ k ∈ (S_st T a).filter (fun k => e ∣ k),
                ((-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                  (liouvilleLambda (k / e) : ℝ)) * gaussianTermPhi k X) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro a _
        unfold windowEnergyNormSq windowPairing
        rw [← intervalIntegral.integral_const_mul]
        apply intervalIntegral.integral_congr; intro X _; dsimp [H_e, dM]; ring
      rw [h_sc, Real.sqrt_mul (sq_nonneg dM), Real.sqrt_sq_eq_abs]
      have hdM_le :=
        (two_sided_interior_diag_bound_and_offdiag_equivalence_tc062r).2.2.2.1.1 c_half he1
      have hlog_e_le : 1 + Real.log (e : ℝ) ≤ 1 + Real.log (T : ℝ) :=
        add_le_add_left (Real.log_le_log he_pos_r (by exact_mod_cast heT)) 1
      have h1logT_nn : 0 ≤ 1 + Real.log (T : ℝ) :=
        add_nonneg zero_le_one (Real.log_nonneg (by exact_mod_cast hT1))
      have hdM_le2 : |dM| ≤ (8 + |c_half|) * (1 + Real.log (T : ℝ)) / Real.sqrt (e : ℝ) :=
        le_trans hdM_le (div_le_div_of_nonneg_right
          (mul_le_mul_of_nonneg_left hlog_e_le h8ch_nn) (Real.sqrt_nonneg _))
      have h_div_e := h_st_div hY0 he1 heT _ (fun k => h_sgn_abs k (k / e))
      have hm := mul_le_mul hdM_le2 h_div_e (Real.sqrt_nonneg _)
        (div_nonneg (mul_nonneg h8ch_nn h1logT_nn) (Real.sqrt_nonneg _))
      calc
        |dM| * Real.sqrt _
          ≤ ((8 + |c_half|) * (1 + Real.log (T : ℝ)) / Real.sqrt (e : ℝ)) *
              (C_tau * (1 / Real.sqrt (e : ℝ)) * Real.sqrt (1 + Real.log (T : ℝ))) := hm
        _ = ((8 + |c_half|) * C_tau * (1 + Real.log (T : ℝ)) *
              Real.sqrt (1 + Real.log (T : ℝ))) * ((1 : ℝ) / (e : ℝ)) := by
            field_simp [ne_of_gt (Real.sqrt_pos.mpr he_pos_r), ne_of_gt he_pos_r]
            ring
    have h_sum_e :
        (∑ e ∈ Finset.Icc 1 T,
            Real.sqrt (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (H_e e a))) ≤
          (8 + |c_half|) * C_tau * (1 + Real.log (T : ℝ)) ^ 2 *
            Real.sqrt (1 + Real.log (T : ℝ)) := by
      calc
        _ ≤ ∑ e ∈ Finset.Icc 1 T,
              ((8 + |c_half|) * C_tau * (1 + Real.log (T : ℝ)) *
                Real.sqrt (1 + Real.log (T : ℝ))) * ((1 : ℝ) / (e : ℝ)) :=
            Finset.sum_le_sum h_each_e
        _ = ((8 + |c_half|) * C_tau * (1 + Real.log (T : ℝ)) *
              Real.sqrt (1 + Real.log (T : ℝ))) * ∑ e ∈ Finset.Icc 1 T, (1 : ℝ) / (e : ℝ) :=
            (Finset.mul_sum _ _ _).symm
        _ ≤ ((8 + |c_half|) * C_tau * (1 + Real.log (T : ℝ)) *
              Real.sqrt (1 + Real.log (T : ℝ))) * (1 + Real.log (T : ℝ)) :=
            mul_le_mul_of_nonneg_left (sum_inv_Icc_one_le_one_add_log_tc064_aux hT1)
              (mul_nonneg (mul_nonneg (mul_nonneg h8ch_nn hCtau_nn)
                (add_nonneg zero_le_one (Real.log_nonneg (by exact_mod_cast hT1))))
                (Real.sqrt_nonneg _))
        _ = (8 + |c_half|) * C_tau * (1 + Real.log (T : ℝ)) ^ 2 *
              Real.sqrt (1 + Real.log (T : ℝ)) := by ring
    have h_rat_sq : ((1 + Real.log (T : ℝ)) / Real.log Y) ^ 2 ≤ 16 := by
      have h_nn : 0 ≤ (1 + Real.log (T : ℝ)) / Real.log Y :=
        div_nonneg (add_nonneg zero_le_one (Real.log_nonneg (by exact_mod_cast hT1)))
          (le_of_lt hlogY_pos)
      calc
        ((1 + Real.log (T : ℝ)) / Real.log Y) ^ 2 ≤ 4 ^ 2 := pow_le_pow_left h_nn h_rat4 2
        _ = 16 := by norm_num
    calc
      Real.sqrt (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (F_p 3 a))
        ≤ Real.sqrt
            ((1 / (Real.log Y) ^ 4) *
              (∑ a ∈ oddSquarefreeCores T,
                windowEnergyNormSq Y (fun X => ∑ e ∈ Finset.Icc 1 T, H_e e a X))) :=
          Real.sqrt_le_sqrt h_lp
      _ = (1 / (Real.log Y) ^ 2) *
            Real.sqrt
              (∑ a ∈ oddSquarefreeCores T,
                windowEnergyNormSq Y (fun X => ∑ e ∈ Finset.Icc 1 T, H_e e a X)) := by
          rw [Real.sqrt_mul (div_nonneg zero_le_one (pow_nonneg (le_of_lt hlogY_pos) 4)),
            one_div, Real.sqrt_inv,
            show (Real.log Y) ^ 4 = ((Real.log Y) ^ 2) ^ 2 by ring,
            Real.sqrt_sq (sq_nonneg _), one_div]
      _ ≤ (1 / (Real.log Y) ^ 2) *
            ((8 + |c_half|) * C_tau * (1 + Real.log (T : ℝ)) ^ 2 *
              Real.sqrt (1 + Real.log (T : ℝ))) :=
          mul_le_mul_of_nonneg_left (le_trans h_mink_e h_sum_e)
            (div_nonneg zero_le_one (sq_nonneg _))
      _ = ((8 + |c_half|) * C_tau) *
            (((1 + Real.log (T : ℝ)) / Real.log Y) ^ 2 * Real.sqrt (1 + Real.log (T : ℝ))) := by
          field_simp [ne_of_gt hlogY_pos]; ring
      _ ≤ ((8 + |c_half|) * C_tau) * (16 * ((3 / 2 : ℝ) * Real.sqrt (1 + Real.log Y))) :=
          mul_le_mul_of_nonneg_left
            (mul_le_mul h_rat_sq hsqrt_1logT_le (Real.sqrt_nonneg _) (by norm_num))
            (mul_nonneg h8ch_nn hCtau_nn)
      _ = 24 * (8 + |c_half|) * C_tau * Real.sqrt (1 + Real.log Y) := by ring
  -- Piece 4 (unconditional small-divisor jump 1 <= d <= min D0 (T - 1)):
  have h_N4 :
      Real.sqrt (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (F_p 4 a)) ≤
        48 * C_tau * C_sm * Real.sqrt (1 + Real.log Y) :=
    uncond_small_divisor_jump_core_bound_tc064_aux c_lam c_half hY2
  -- Assemble 5-piece direct-sum Minkowski bound on coreAdjustedProfileA:
  have h_mink_5 :=
    (direct_sum_window_minkowski_sq_tc064_aux hY0 (oddSquarefreeCores T)
      (Finset.univ : Finset (Fin 5)) F_p hc_Fp).2
  have h_sum_N5 :
      (∑ i : Fin 5, Real.sqrt (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (F_p i a))) ≤
        B_tot * Real.sqrt (1 + Real.log Y) := by
    rw [Fin.sum_univ_five]
    dsimp only [B_tot]
    rw [add_mul, add_mul, add_mul, add_mul]
    exact add_le_add (add_le_add (add_le_add (add_le_add h_N0 h_N1) h_N2) h_N3) h_N4
  have h_A_bd :
      (∑ a ∈ oddSquarefreeCores T, windowEnergyNormSq Y (coreAdjustedProfileA c_lam c_half T D0 a)) ≤
        B_tot ^ 2 * (1 + Real.log Y) := by
    rw [Finset.sum_congr rfl h_A_eq_sum5]
    have h_sq := pow_le_pow_left
      (Finset.sum_nonneg (fun _ _ => Real.sqrt_nonneg _)) h_sum_N5 2
    calc
      _ ≤ (B_tot * Real.sqrt (1 + Real.log Y)) ^ 2 := le_trans h_mink_5 h_sq
      _ = B_tot ^ 2 * (1 + Real.log Y) := by
          have hs : (Real.sqrt (1 + Real.log Y)) ^ 2 = 1 + Real.log Y :=
            Real.sq_sqrt (add_nonneg zero_le_one (le_of_lt hlogY_pos))
          calc
            (B_tot * Real.sqrt (1 + Real.log Y)) ^ 2
              = B_tot ^ 2 * (Real.sqrt (1 + Real.log Y)) ^ 2 := by ring
            _ = B_tot ^ 2 * (1 + Real.log Y) := by rw [hs]
  have h_core_tot :
      (∑ a ∈ oddSquarefreeCores T,
          (windowEnergyNormSq Y (coreAdjustedProfileA c_lam c_half T D0 a) +
            ∑ pk ∈ primePowerPairsUpTo T,
              windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X))) ≤
        C_core * (1 + Real.log Y) := by
    rw [Finset.sum_add_distrib]
    dsimp only [C_core]
    rw [add_mul]
    exact add_le_add h_A_bd h_feat_bd
  clear F_p hc_Fp h_A_eq_sum5 h_N0 h_N1 h_N2 h_N3 h_N4 h_mink_5 h_sum_N5 h_A_bd
  refine ⟨h_core_tot, ?_⟩
  -- Bound canonicalSameCoreSquareRemainderR:
  unfold canonicalSameCoreSquareRemainderR sameCoreSquareRemainderR
  change |(∑ a ∈ oddSquarefreeCores T, completeCorePairKernelMcal c_lam c_half T D0 Y a a) -
      (∑ u ∈ oddChainParts T,
        (windowEnergyNormSq Y (oddChainAdjustedProfileUcal c_lam c_half T D0 u) -
          4 * ∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => oddChainFeatureVectorVcal u T pk X)))| ≤
    C_square * (1 + Real.log Y)
  have h_norm_nn : ∀ g : ℝ → ℝ, 0 ≤ windowEnergyNormSq Y g := by
    intro g
    unfold windowEnergyNormSq windowPairing
    apply intervalIntegral.integral_nonneg hle_win
    intro X hX; exact div_nonneg (mul_self_nonneg _) (lt_of_lt_of_le hY0 hX.1).le
  have h_Mcal_aa :
      |∑ a ∈ oddSquarefreeCores T, completeCorePairKernelMcal c_lam c_half T D0 Y a a| ≤
        4 * C_core * (1 + Real.log Y) := by
    have h_each :
        ∀ a ∈ oddSquarefreeCores T,
          |completeCorePairKernelMcal c_lam c_half T D0 Y a a| ≤
            4 * (windowEnergyNormSq Y (coreAdjustedProfileA c_lam c_half T D0 a) +
              ∑ pk ∈ primePowerPairsUpTo T,
                windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X)) := by
      intro a _
      unfold completeCorePairKernelMcal
      change |windowEnergyNormSq Y (coreAdjustedProfileA c_lam c_half T D0 a) -
          4 * ∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X)| ≤ _
      have hA_nn := h_norm_nn (coreAdjustedProfileA c_lam c_half T D0 a)
      have hB_nn : 0 ≤ ∑ pk ∈ primePowerPairsUpTo T,
          windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X) :=
        Finset.sum_nonneg (fun _ _ => h_norm_nn _)
      have ht := abs_sub (windowEnergyNormSq Y (coreAdjustedProfileA c_lam c_half T D0 a))
        (4 * ∑ pk ∈ primePowerPairsUpTo T,
          windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X))
      rw [abs_of_nonneg hA_nn,
        abs_of_nonneg (mul_nonneg (by norm_num : (0 : ℝ) ≤ 4) hB_nn)] at ht
      have hA_le_4A :
          windowEnergyNormSq Y (coreAdjustedProfileA c_lam c_half T D0 a) ≤
            4 * windowEnergyNormSq Y (coreAdjustedProfileA c_lam c_half T D0 a) :=
        le_mul_of_one_le_left hA_nn (by norm_num)
      rw [mul_add]
      exact le_trans ht (add_le_add_right hA_le_4A _)
    calc
      |∑ a ∈ oddSquarefreeCores T, completeCorePairKernelMcal c_lam c_half T D0 Y a a|
        ≤ ∑ a ∈ oddSquarefreeCores T, |completeCorePairKernelMcal c_lam c_half T D0 Y a a| :=
          Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ a ∈ oddSquarefreeCores T,
            4 * (windowEnergyNormSq Y (coreAdjustedProfileA c_lam c_half T D0 a) +
              ∑ pk ∈ primePowerPairsUpTo T,
                windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X)) :=
          Finset.sum_le_sum h_each
      _ = 4 * ∑ a ∈ oddSquarefreeCores T,
            (windowEnergyNormSq Y (coreAdjustedProfileA c_lam c_half T D0 a) +
              ∑ pk ∈ primePowerPairsUpTo T,
                windowEnergyNormSq Y (fun X => coreFeatureVectorB a T pk X)) :=
          (Finset.mul_sum _ _ _).symm
      _ ≤ 4 * (C_core * (1 + Real.log Y)) := mul_le_mul_of_nonneg_left h_core_tot (by norm_num)
      _ = 4 * C_core * (1 + Real.log Y) := by ring
  have h_Ucal_Vcal := h_uv_bd hY2
  have h_tri_R := abs_sub
    (∑ a ∈ oddSquarefreeCores T, completeCorePairKernelMcal c_lam c_half T D0 Y a a)
    (∑ u ∈ oddChainParts T,
      (windowEnergyNormSq Y (oddChainAdjustedProfileUcal c_lam c_half T D0 u) -
        4 * ∑ pk ∈ primePowerPairsUpTo T,
          windowEnergyNormSq Y (fun X => oddChainFeatureVectorVcal u T pk X)))
  dsimp only [C_square]
  rw [add_mul]
  exact le_trans h_tri_R (add_le_add h_Mcal_aa h_Ucal_Vcal)

private theorem closure_hypothesis_iff_of_log_linear_diff_tc064_aux
    {F1 F2 D : ℝ → ℝ} {C : ℝ} (hC : 0 ≤ C)
    (h_diff : ∀ {Y : ℝ}, 2 ≤ Y → |F1 Y - F2 Y| ≤ C * (1 + Real.log Y)) :
    MixedCovarianceClosureHypothesis F1 D ↔ MixedCovarianceClosureHypothesis F2 D := by
  have h_one_way :
      ∀ {G1 G2 : ℝ → ℝ},
        (∀ {Y : ℝ}, 2 ≤ Y → G2 Y ≤ G1 Y + C * (1 + Real.log Y)) →
        MixedCovarianceClosureHypothesis G1 D → MixedCovarianceClosureHypothesis G2 D := by
    intro G1 G2 h_le hG1 η hη
    obtain ⟨a_eta, b_eta, κ_eta, Y_eta, ha, hb, hκ_pos, hκ_le2, hYe, hG1_bd⟩ := hG1 η hη
    obtain ⟨a_log, ha_log_nn, h_log_rpow⟩ :=
      (uniform_same_chain_hilbert_bound_and_closure_transfer_tc063).2.2.2.2.1 hC hη
    refine ⟨a_eta + a_log, b_eta, κ_eta, Y_eta,
      add_nonneg ha ha_log_nn, hb, hκ_pos, hκ_le2, hYe, ?_⟩
    intro Y hYYe
    have hY2 : 2 ≤ Y := le_trans hYe hYYe
    have h1 := h_le hY2
    have h2 := hG1_bd Y hYYe
    have h3 := h_log_rpow Y hY2
    linarith [show (a_eta + a_log) * Y ^ η = a_eta * Y ^ η + a_log * Y ^ η by ring]
  constructor
  · apply h_one_way
    intro Y hY2
    have habs := (abs_le.mp (h_diff hY2)).1
    linarith
  · apply h_one_way
    intro Y hY2
    have habs := (abs_le.mp (h_diff hY2)).2
    linarith

/-- **Theorem 3 (`TASK-TC-064` §3.2–§3.4, Square-Support Gaussian Norm Sum, Prime-Power Feature Norm Bound, Direct-Sum Hilbert Minkowski Inequality, Unconditional `O(1 + log Y)` Same-Core & `R_square` Bounds, and Two-Way `MixedCovarianceClosureHypothesis` Transfer)**:
    Let `C_tau := (16 / 5 : ℝ) * (2 + Real.sqrt 2) * RiemannScope.tau ^ (5 / 2 : ℝ) * Real.sqrt (Real.log RiemannScope.tau)`.
    1. *Square-support Gaussian norm sum*:
       For every `w0 > 1`, `Y > 0`, `M ≥ 1`, and `R, L_lim : ℕ`:
       `∑_{r=0}^R ∑_{l=1}^{L_lim} √(paramWindowNormSq Y w0 (gaussianTermPhi (2^r * M * l^2))) ≤ ((16/5)*(2+√2)*w0^(5/2)*√(log w0)) / √M`,
       and specialized to `w0 = RiemannScope.tau`:
       `∑_{r=0}^R ∑_{l=1}^{L_lim} √(windowEnergyNormSq Y (gaussianTermPhi (2^r * M * l^2))) ≤ C_tau / √M`;
    2. *Prime-power feature norm bound (`2 ≤ Y`, `n ∈ Icc 1 T`)*:
       `√(∑_{pk ∈ primePowerPairsUpTo T} ‖g_{n, pk}‖_Y^2) ≤ (log T / log Y) * √‖φ_n‖_Y^2`;
    3. *Direct-sum Hilbert Minkowski inequality (`0 < Y`)*:
       `∑_{a ∈ S} ‖∑_{i ∈ I} F i a‖_Y^2 ≤ (∑_{i ∈ I} √(∑_{a ∈ S} ‖F i a‖_Y^2))^2`;
    4. *Unconditional 5-piece same-core energy bound & `canonicalSameCoreSquareRemainderR` bound for all `2 ≤ Y`*
       (plus explicit `O(1)` small-divisor jump bound when `|R_osc(d)| ≤ C_osc * d`):
       `∑_{a ∈ oddSquarefreeCores (canonicalCutoffT Y)} (‖A_a‖_Y^2 + ∑_{pk} ‖B_{a,pk}‖_Y^2) ≤ C_core * (1 + log Y)` and
       `|canonicalSameCoreSquareRemainderR c_lam c_half Y| ≤ C_square * (1 + log Y)`;
    5. *Unconditional two-way `MixedCovarianceClosureHypothesis` equivalence onto `canonicalDistinctSquarefreeCoreSumS` and conditional Route D subpower transfer*. -/
theorem uniform_same_core_hilbert_bound_and_closure_transfer_tc064 :
    let C_tau : ℝ :=
      (16 / 5 : ℝ) * (2 + Real.sqrt 2) * RiemannScope.tau ^ (5 / 2 : ℝ) *
        Real.sqrt (Real.log RiemannScope.tau)
    ((∀ {w0 Y : ℝ}, 1 < w0 → 0 < Y → ∀ {M : ℕ}, 1 ≤ M → ∀ (R L_lim : ℕ),
        (∑ r ∈ Finset.range (R + 1),
          ∑ l ∈ Finset.Icc 1 L_lim,
            Real.sqrt (paramWindowNormSq Y w0 (gaussianTermPhi (2 ^ r * M * l ^ 2)))) ≤
          ((16 / 5 : ℝ) * (2 + Real.sqrt 2) * w0 ^ (5 / 2 : ℝ) * Real.sqrt (Real.log w0)) /
            Real.sqrt (M : ℝ)) ∧
      (∀ {Y : ℝ}, 0 < Y → ∀ {M : ℕ}, 1 ≤ M → ∀ (R L_lim : ℕ),
        (∑ r ∈ Finset.range (R + 1),
          ∑ l ∈ Finset.Icc 1 L_lim,
            Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi (2 ^ r * M * l ^ 2)))) ≤
          C_tau / Real.sqrt (M : ℝ))) ∧
    (∀ {Y : ℝ}, 2 ≤ Y → ∀ {T n : ℕ}, n ∈ Finset.Icc 1 T →
      Real.sqrt
          (∑ pk ∈ primePowerPairsUpTo T,
            windowEnergyNormSq Y (fun X => stationPrimePowerFeatureG n pk X)) ≤
        (Real.log (T : ℝ) / Real.log Y) *
          Real.sqrt (windowEnergyNormSq Y (gaussianTermPhi n))) ∧
    (∀ {Y : ℝ}, 0 < Y → ∀ (S : Finset ℕ) (I : Finset ℕ) (F : ℕ → ℕ → ℝ → ℝ),
      (∀ i ∈ I, ∀ a ∈ S, ContinuousOn (F i a) (Set.uIcc Y (RiemannScope.tau * Y))) →
      (∑ a ∈ S, windowEnergyNormSq Y (fun X => ∑ i ∈ I, F i a X)) ≤
        (∑ i ∈ I, Real.sqrt (∑ a ∈ S, windowEnergyNormSq Y (F i a))) ^ 2) ∧
    ((∀ (c_lam c_half : ℝ) {C_osc : ℝ}, 0 ≤ C_osc →
        (∀ d : ℕ, 1 ≤ d →
          |selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d| ≤ C_osc * (d : ℝ)) →
        ∀ {Y : ℝ}, 2 ≤ Y →
          let T := canonicalCutoffT Y
          let D0 := Nat.floor (Real.log Y)
          let S_st := fun a =>
            (coreSquareMultipliers a T).biUnion (fun b =>
              (dyadicChainExponents (a * b ^ 2) T).biUnion (fun j =>
                (Finset.range 2).image (fun eps => 2 ^ (2 * j + eps) * a * b ^ 2)))
          Real.sqrt
              (∑ a ∈ oddSquarefreeCores T,
                windowEnergyNormSq Y
                  (fun X =>
                    (1 / (Real.log X) ^ 2) *
                      (∑ k ∈ S_st a,
                        (-1 : ℝ) ^ (k.factorization 2) * (liouvilleLambda k : ℝ) *
                          ((∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => d ∣ k),
                              (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                                (liouvilleLambda (k / d) : ℝ)) -
                            (∑ d ∈ (Finset.Icc 1 (min D0 (T - 1))).filter (fun d => (d + 1) ∣ k),
                              (selbergCenteredRemainderInt c_lam d - squarePoleDriftM c_half d) *
                                (liouvilleLambda (k / (d + 1)) : ℝ))) *
                          gaussianTermPhi k X))) ≤
            4 * C_osc * C_tau) ∧
      (∀ (c_lam c_half : ℝ),
        ∃ C_core C_square : ℝ, 0 ≤ C_core ∧ 0 ≤ C_square ∧
          ∀ {Y : ℝ}, 2 ≤ Y →
            (∑ a ∈ oddSquarefreeCores (canonicalCutoffT Y),
              (windowEnergyNormSq Y
                  (coreAdjustedProfileA c_lam c_half
                    (canonicalCutoffT Y) (Nat.floor (Real.log Y)) a) +
                ∑ pk ∈ primePowerPairsUpTo (canonicalCutoffT Y),
                  windowEnergyNormSq Y
                    (fun X => coreFeatureVectorB a (canonicalCutoffT Y) pk X))) ≤
              C_core * (1 + Real.log Y) ∧
            |canonicalSameCoreSquareRemainderR c_lam c_half Y| ≤ C_square * (1 + Real.log Y))) ∧
    ((∀ (c_lam c_half : ℝ),
        (MixedCovarianceClosureHypothesis
            (canonicalDifferentOddChainSumS c_lam c_half) canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalDistinctSquarefreeCoreSumS c_lam c_half) canonicalPrimePowerDiagDtilde) ∧
        (MixedCovarianceClosureHypothesis
            (canonicalInteriorOffDiagSigma c_lam c_half 2) canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalDistinctSquarefreeCoreSumS c_lam c_half) canonicalPrimePowerDiagDtilde)) ∧
      ((MixedCovarianceClosureHypothesis
            (canonicalInteriorOffDiagSigma
              actualSelbergConstantCLam actualSquarePoleConstantCHalf 2)
            canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalDistinctSquarefreeCoreSumS
              actualSelbergConstantCLam actualSquarePoleConstantCHalf)
            canonicalPrimePowerDiagDtilde) ∧
        (MixedCovarianceClosureHypothesis
            (canonicalSignedMixedCovarianceJ
              actualSelbergConstantCLam actualSquarePoleConstantCHalf)
            canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalDistinctSquarefreeCoreSumS
              actualSelbergConstantCLam actualSquarePoleConstantCHalf)
            canonicalPrimePowerDiagDtilde)) ∧
      (∀ {M_lin : ℝ},
        0 ≤ M_lin →
        (∀ Z : ℝ, 1 ≤ Z → canonicalLiouvilleEnergyE Z ≤ M_lin * Z) →
        MixedCovarianceClosureHypothesis
          (canonicalDistinctSquarefreeCoreSumS
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
  intro C_tau
  have hCg := (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2.1
  have htau_gt1 : (1 : ℝ) < RiemannScope.tau := by linarith
  have h_iff_diff_core :
      ∀ (c_lam c_half : ℝ),
        MixedCovarianceClosureHypothesis
            (canonicalDifferentOddChainSumS c_lam c_half) canonicalPrimePowerDiagDtilde ↔
          MixedCovarianceClosureHypothesis
            (canonicalDistinctSquarefreeCoreSumS c_lam c_half) canonicalPrimePowerDiagDtilde := by
    intro c_lam c_half
    obtain ⟨_, C_square, _, hCsq_nn, h_bds⟩ :=
      (same_core_hilbert_and_remainder_bounds_tc064_aux c_lam c_half).2
    apply closure_hypothesis_iff_of_log_linear_diff_tc064_aux hCsq_nn
    intro Y hY2
    have h_split :=
      ((exact_odd_squarefree_core_bijection_and_complete_kernel_split_tc064).2.2 hY2).2.2
        c_lam c_half
    have h_diff_eq :
        canonicalDifferentOddChainSumS c_lam c_half Y -
            canonicalDistinctSquarefreeCoreSumS c_lam c_half Y =
          canonicalSameCoreSquareRemainderR c_lam c_half Y := by
      linarith [h_split]
    rw [h_diff_eq]
    exact (h_bds hY2).2
  have h_tc063_tr := (uniform_same_chain_hilbert_bound_and_closure_transfer_tc063).2.2.2.2
  refine ⟨⟨fun {_ _} hw0 hY0 {_} hM R L_lim =>
        square_support_gaussian_norm_sum_tc064_aux hw0 hY0 hM R L_lim,
      fun {_} hY0 {_} hM R L_lim =>
        square_support_gaussian_norm_sum_tc064_aux htau_gt1 hY0 hM R L_lim⟩,
    fun {_} hY2 {_ _} hn => stationPrimePowerFeatureG_norm_le_tc064_aux hY2 hn,
    fun {_} hY0 S I F hF => (direct_sum_window_minkowski_sq_tc064_aux hY0 S I F hF).2,
    ⟨fun c_lam c_half {_} hCo h_osc {_} hY2 =>
        (same_core_hilbert_and_remainder_bounds_tc064_aux c_lam c_half).1 hCo h_osc hY2,
      fun c_lam c_half => (same_core_hilbert_and_remainder_bounds_tc064_aux c_lam c_half).2⟩,
    ⟨fun c_lam c_half => ⟨h_iff_diff_core c_lam c_half,
        (h_tc063_tr.2.1 c_lam c_half).trans (h_iff_diff_core c_lam c_half)⟩,
      ⟨h_tc063_tr.2.2.1.1.trans
          (h_iff_diff_core actualSelbergConstantCLam actualSquarePoleConstantCHalf),
        h_tc063_tr.2.2.1.2.trans
          (h_iff_diff_core actualSelbergConstantCLam actualSquarePoleConstantCHalf)⟩,
      fun {_} hM_nn hM_lin h_core_cl h_route =>
        h_tc063_tr.2.2.2 hM_nn hM_lin
          ((h_iff_diff_core actualSelbergConstantCLam actualSquarePoleConstantCHalf).mpr h_core_cl)
          h_route⟩⟩

/-! ### Section 4: Squarefree-Core GCD Sectors, Prime Divisibility, and Prime Toggle (`TASK-TC-064` §4) -/

private theorem primitive_squarefree_core_pair_bijection_tc064_aux (T : ℕ) :
    (∀ g ∈ oddSquarefreeCommonFactorSet T,
      ∀ rt ∈ primitiveSquarefreeCorePairs T g,
        g * rt.1 ∈ oddSquarefreeCores T ∧ g * rt.2 ∈ oddSquarefreeCores T ∧
          g * rt.1 ≠ g * rt.2 ∧ Nat.gcd (g * rt.1) (g * rt.2) = g ∧
          (g * rt.1) / g = rt.1 ∧ (g * rt.2) / g = rt.2) ∧
    (∀ ac ∈ (oddSquarefreeCores T ×ˢ oddSquarefreeCores T).filter (fun ac => ac.1 ≠ ac.2),
      Nat.gcd ac.1 ac.2 ∈ oddSquarefreeCommonFactorSet T ∧
        (ac.1 / Nat.gcd ac.1 ac.2, ac.2 / Nat.gcd ac.1 ac.2) ∈
          primitiveSquarefreeCorePairs T (Nat.gcd ac.1 ac.2) ∧
        ∃! grt : ℕ × (ℕ × ℕ),
          grt.1 ∈ oddSquarefreeCommonFactorSet T ∧
            grt.2 ∈ primitiveSquarefreeCorePairs T grt.1 ∧
            grt.1 * grt.2.1 = ac.1 ∧ grt.1 * grt.2.2 = ac.2) ∧
    (∀ {g r t : ℕ}, Squarefree g → Nat.Coprime g (r * t) →
      ArithmeticFunction.moebius (g * r) * ArithmeticFunction.moebius (g * t) =
        ArithmeticFunction.moebius r * ArithmeticFunction.moebius t) ∧
    (∀ {g r : ℕ} (T : ℕ), 1 ≤ g → 1 ≤ r →
      coreSquareMultipliers (g * r) T = coreSquareMultipliers r (T / g)) := by
  have h_fwd :
      ∀ g ∈ oddSquarefreeCommonFactorSet T,
        ∀ rt ∈ primitiveSquarefreeCorePairs T g,
          g * rt.1 ∈ oddSquarefreeCores T ∧ g * rt.2 ∈ oddSquarefreeCores T ∧
            g * rt.1 ≠ g * rt.2 ∧ Nat.gcd (g * rt.1) (g * rt.2) = g ∧
            (g * rt.1) / g = rt.1 ∧ (g * rt.2) / g = rt.2 := by
    intro g hg ⟨r, t⟩ hrt
    simp only [oddSquarefreeCommonFactorSet, primitiveSquarefreeCorePairs, oddSquarefreeCores,
      Finset.mem_filter, Finset.mem_product, Finset.mem_Icc] at hg hrt ⊢
    rcases hg with ⟨⟨⟨hg1, _⟩, hg_o, hg_sf, _⟩, _⟩
    rcases hrt with ⟨⟨⟨⟨hr1, _⟩, hr_o, hr_sf, h2r_div⟩, ⟨⟨ht1, _⟩, ht_o, ht_sf, h2t_div⟩⟩,
      hrt_ne, hrt_cop, h_grt_cop⟩
    have hgr_cop : Nat.Coprime g r := h_grt_cop.coprime_dvd_right (dvd_mul_right r t)
    have hgt_cop : Nat.Coprime g t := h_grt_cop.coprime_dvd_right (dvd_mul_left t r)
    have h2gr : 2 * (g * r) ≤ T := by
      have hm := (Nat.le_div_iff_mul_le hg1).mp h2r_div
      linarith [show 2 * (g * r) = 2 * r * g by ring]
    have h2gt : 2 * (g * t) ≤ T := by
      have hm := (Nat.le_div_iff_mul_le hg1).mp h2t_div
      linarith [show 2 * (g * t) = 2 * t * g by ring]
    exact ⟨⟨⟨Nat.mul_pos hg1 hr1, by omega⟩, hg_o.mul hr_o,
        (Nat.squarefree_mul hgr_cop).mpr ⟨hg_sf, hr_sf⟩, h2gr⟩,
      ⟨⟨Nat.mul_pos hg1 ht1, by omega⟩, hg_o.mul ht_o,
        (Nat.squarefree_mul hgt_cop).mpr ⟨hg_sf, ht_sf⟩, h2gt⟩,
      fun heq => hrt_ne (Nat.eq_of_mul_eq_mul_left hg1 heq),
      by rw [Nat.gcd_mul_left, hrt_cop.gcd_eq_one, mul_one],
      Nat.mul_div_right r hg1,
      Nat.mul_div_right t hg1⟩
  have h_inv :
      ∀ ac ∈ (oddSquarefreeCores T ×ˢ oddSquarefreeCores T).filter (fun ac => ac.1 ≠ ac.2),
        Nat.gcd ac.1 ac.2 ∈ oddSquarefreeCommonFactorSet T ∧
          (ac.1 / Nat.gcd ac.1 ac.2, ac.2 / Nat.gcd ac.1 ac.2) ∈
            primitiveSquarefreeCorePairs T (Nat.gcd ac.1 ac.2) ∧
          ∃! grt : ℕ × (ℕ × ℕ),
            grt.1 ∈ oddSquarefreeCommonFactorSet T ∧
              grt.2 ∈ primitiveSquarefreeCorePairs T grt.1 ∧
              grt.1 * grt.2.1 = ac.1 ∧ grt.1 * grt.2.2 = ac.2 := by
    rintro ⟨a, c⟩ hac
    simp only [Finset.mem_filter, Finset.mem_product, oddSquarefreeCores, Finset.mem_Icc] at hac
    rcases hac with ⟨⟨⟨⟨ha1, _⟩, ha_o, ha_sf, h2aT⟩, ⟨⟨_, _⟩, hc_o, hc_sf, h2cT⟩⟩, hac_ne⟩
    let g := Nat.gcd a c
    let r := a / g
    let t := c / g
    have hg_pos : 0 < g := Nat.gcd_pos_of_pos_left c ha1
    have hgr : g * r = a := Nat.mul_div_cancel' (Nat.gcd_dvd_left a c)
    have hgt : g * t = c := Nat.mul_div_cancel' (Nat.gcd_dvd_right a c)
    have ha_p := squarefree_pos_and_coprime_of_mul_tc064_aux.2 (hgr.symm ▸ ha_sf)
    have hc_p := squarefree_pos_and_coprime_of_mul_tc064_aux.2 (hgt.symm ▸ hc_sf)
    have hg_o : Odd g := (odd_of_odd_mul_tc064_aux (hgr.symm ▸ ha_o)).1
    have hr_o : Odd r := (odd_of_odd_mul_tc064_aux (hgr.symm ▸ ha_o)).2
    have ht_o : Odd t := (odd_of_odd_mul_tc064_aux (hgt.symm ▸ hc_o)).2
    have hrt_ne : r ≠ t := fun heq => hac_ne (by rw [← hgr, ← hgt, heq])
    have hrt_cop : Nat.Coprime r t := Nat.coprime_div_gcd_div_gcd hg_pos
    have h_grt_cop : Nat.Coprime g (r * t) := ha_p.2.2.mul_right hc_p.2.2
    have h6g : 6 * g ≤ T := by
      have h_max3 : 3 ≤ r ∨ 3 ≤ t := by
        by_contra hnot
        push_neg at hnot
        obtain ⟨kr, hkr⟩ := hr_o
        obtain ⟨kt, hkt⟩ := ht_o
        omega
      rcases h_max3 with hr3 | ht3
      · have h1 : 2 * (g * 3) ≤ 2 * (g * r) := Nat.mul_le_mul_left 2 (Nat.mul_le_mul_left g hr3)
        rw [hgr] at h1; omega
      · have h1 : 2 * (g * 3) ≤ 2 * (g * t) := Nat.mul_le_mul_left 2 (Nat.mul_le_mul_left g ht3)
        rw [hgt] at h1; omega
    have hg_in : g ∈ oddSquarefreeCommonFactorSet T := by
      simp only [oddSquarefreeCommonFactorSet, oddSquarefreeCores, Finset.mem_filter, Finset.mem_Icc]
      exact ⟨⟨⟨hg_pos, by omega⟩, hg_o, ha_p.1, by omega⟩, h6g⟩
    have h2r_div : 2 * r ≤ T / g :=
      (Nat.le_div_iff_mul_le hg_pos).mpr (by linarith [show 2 * r * g = 2 * (g * r) by ring])
    have h2t_div : 2 * t ≤ T / g :=
      (Nat.le_div_iff_mul_le hg_pos).mpr (by linarith [show 2 * t * g = 2 * (g * t) by ring])
    have hrt_in : (r, t) ∈ primitiveSquarefreeCorePairs T g := by
      simp only [primitiveSquarefreeCorePairs, oddSquarefreeCores, Finset.mem_filter,
        Finset.mem_product, Finset.mem_Icc]
      exact ⟨⟨⟨⟨hr_o.pos, le_trans (Nat.le_mul_of_pos_left r (by decide)) h2r_div⟩,
          hr_o, ha_p.2.1, h2r_div⟩,
        ⟨⟨ht_o.pos, le_trans (Nat.le_mul_of_pos_left t (by decide)) h2t_div⟩,
          ht_o, hc_p.2.1, h2t_div⟩⟩,
        hrt_ne, hrt_cop, h_grt_cop⟩
    refine ⟨hg_in, hrt_in, ⟨(g, (r, t)), ⟨hg_in, hrt_in, hgr, hgt⟩, ?_⟩⟩
    rintro ⟨g', ⟨r', t'⟩⟩ ⟨hg'_in, hrt'_in, hgr', hgt'⟩
    dsimp only at hg'_in hrt'_in hgr' hgt'
    have hf' := h_fwd g' hg'_in (r', t') hrt'_in
    dsimp only at hf'
    have hg_eq : g' = g := by change g' = Nat.gcd a c; rw [← hgr', ← hgt', hf'.2.2.2.1]
    have hr_eq : r' = r := by change r' = a / g; rw [← hg_eq, ← hgr', hf'.2.2.2.2.1]
    have ht_eq : t' = t := by change t' = c / g; rw [← hg_eq, ← hgt', hf'.2.2.2.2.2]
    rw [hg_eq, hr_eq, ht_eq]
  have h_mu :
      ∀ {g r t : ℕ}, Squarefree g → Nat.Coprime g (r * t) →
        ArithmeticFunction.moebius (g * r) * ArithmeticFunction.moebius (g * t) =
          ArithmeticFunction.moebius r * ArithmeticFunction.moebius t := by
    intro g r t hg_sf h_cop
    have hgr : Nat.Coprime g r := h_cop.coprime_dvd_right (dvd_mul_right r t)
    have hgt : Nat.Coprime g t := h_cop.coprime_dvd_right (dvd_mul_left t r)
    rw [ArithmeticFunction.isMultiplicative_moebius.map_mul_of_coprime hgr,
      ArithmeticFunction.isMultiplicative_moebius.map_mul_of_coprime hgt]
    have h_sq_r := (liouvilleLambda_squarefree_mul_sq_eq_moebius_tc064_aux hg_sf (le_refl 1)).2
    have h_sq : ArithmeticFunction.moebius g * ArithmeticFunction.moebius g = 1 := by
      have hr : ((ArithmeticFunction.moebius g * ArithmeticFunction.moebius g : ℤ) : ℝ) = 1 := by
        push_cast; linarith [sq (ArithmeticFunction.moebius g : ℝ), h_sq_r]
      exact_mod_cast hr
    calc
      (ArithmeticFunction.moebius g * ArithmeticFunction.moebius r) *
          (ArithmeticFunction.moebius g * ArithmeticFunction.moebius t)
        = (ArithmeticFunction.moebius g * ArithmeticFunction.moebius g) *
            (ArithmeticFunction.moebius r * ArithmeticFunction.moebius t) := by ring
      _ = ArithmeticFunction.moebius r * ArithmeticFunction.moebius t := by rw [h_sq, one_mul]
  have h_mult_eq :
      ∀ {g r : ℕ} (T : ℕ), 1 ≤ g → 1 ≤ r →
        coreSquareMultipliers (g * r) T = coreSquareMultipliers r (T / g) := by
    intro g r T hg1 hr1
    ext b
    simp only [coreSquareMultipliers, Finset.mem_filter, Finset.mem_Icc]
    constructor
    · rintro ⟨⟨hb1, _⟩, hb_o, h2grb2⟩
      have h2rb2_div : 2 * r * b ^ 2 ≤ T / g :=
        (Nat.le_div_iff_mul_le hg1).mpr
          (by linarith [show 2 * r * b ^ 2 * g = 2 * (g * r) * b ^ 2 by ring])
      have hb_le_b2 : b ≤ b ^ 2 := by nlinarith
      have hb2_le : b ^ 2 ≤ 2 * r * b ^ 2 := by nlinarith
      exact ⟨⟨hb1, le_trans hb_le_b2 (le_trans hb2_le h2rb2_div)⟩, hb_o, h2rb2_div⟩
    · rintro ⟨⟨hb1, _⟩, hb_o, h2rb2_div⟩
      have h2grb2 : 2 * (g * r) * b ^ 2 ≤ T := by
        have hm := (Nat.le_div_iff_mul_le hg1).mp h2rb2_div
        linarith [show 2 * (g * r) * b ^ 2 = 2 * r * b ^ 2 * g by ring]
      have hb_le_b2 : b ≤ b ^ 2 := by nlinarith
      have hgr1 : 1 ≤ g * r := Nat.mul_pos hg1 hr1
      have hb2_le : b ^ 2 ≤ 2 * (g * r) * b ^ 2 := by nlinarith
      exact ⟨⟨hb1, le_trans hb_le_b2 (le_trans hb2_le h2grb2)⟩, hb_o, h2grb2⟩
  exact ⟨h_fwd, h_inv, h_mu, h_mult_eq⟩

private theorem divisibleCore_gram_identity_tc064_aux {Y : ℝ} (hY2 : 2 ≤ Y)
    (c_lam c_half : ℝ) (T D0 d : ℕ) :
    windowEnergyNormSq Y (divisibleCoreProfileSumS c_lam c_half T D0 d) -
        4 * ∑ pk ∈ primePowerPairsUpTo T,
          windowEnergyNormSq Y (fun X => divisibleCoreFeatureSumF T d pk X) =
      ∑ a ∈ (oddSquarefreeCores T).filter (fun a => d ∣ a),
        ∑ c ∈ (oddSquarefreeCores T).filter (fun c => d ∣ c),
          (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
            completeCorePairKernelMcal c_lam c_half T D0 Y a c := by
  have hY0 : 0 < Y := by linarith
  obtain ⟨_, _, _, _, _, _, _, hA_c, hB_c⟩ :=
    continuousOn_station_and_chain_profiles_tc064_aux hY2 c_lam c_half T D0
  let Cd := (oddSquarefreeCores T).filter (fun a => d ∣ a)
  unfold windowEnergyNormSq divisibleCoreProfileSumS divisibleCoreFeatureSumF
  have hA_bilin :=
    windowPairing_finset_bilinear_tc064_aux hY0 Cd Cd
      (coreAdjustedProfileA c_lam c_half T D0)
      (coreAdjustedProfileA c_lam c_half T D0)
      (fun a => (ArithmeticFunction.moebius a : ℝ))
      (fun c => (ArithmeticFunction.moebius c : ℝ))
      (fun a _ => hA_c a) (fun c _ => hA_c c)
  have hB_each :
      ∀ pk ∈ primePowerPairsUpTo T,
        windowPairing Y
            (fun X => ∑ a ∈ Cd, (ArithmeticFunction.moebius a : ℝ) * coreFeatureVectorB a T pk X)
            (fun X => ∑ c ∈ Cd, (ArithmeticFunction.moebius c : ℝ) * coreFeatureVectorB c T pk X) =
          ∑ a ∈ Cd, ∑ c ∈ Cd,
            (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
              windowPairing Y (coreFeatureVectorB a T pk) (coreFeatureVectorB c T pk) :=
    fun pk _ => windowPairing_finset_bilinear_tc064_aux hY0 Cd Cd
      (fun a => coreFeatureVectorB a T pk) (fun c => coreFeatureVectorB c T pk)
      (fun a => (ArithmeticFunction.moebius a : ℝ))
      (fun c => (ArithmeticFunction.moebius c : ℝ))
      (fun a _ => hB_c a pk) (fun c _ => hB_c c pk)
  rw [hA_bilin, Finset.sum_congr rfl hB_each]
  have h_comm :
      (∑ pk ∈ primePowerPairsUpTo T, ∑ a ∈ Cd, ∑ c ∈ Cd,
          (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
            windowPairing Y (coreFeatureVectorB a T pk) (coreFeatureVectorB c T pk)) =
        ∑ a ∈ Cd, ∑ c ∈ Cd,
          (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
            ∑ pk ∈ primePowerPairsUpTo T,
              windowPairing Y (coreFeatureVectorB a T pk) (coreFeatureVectorB c T pk) := by
    trans (∑ a ∈ Cd, ∑ pk ∈ primePowerPairsUpTo T, ∑ c ∈ Cd,
      (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
        windowPairing Y (coreFeatureVectorB a T pk) (coreFeatureVectorB c T pk))
    · exact Finset.sum_comm
    · apply Finset.sum_congr rfl
      intro a _
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro c _
      rw [Finset.mul_sum]
  rw [h_comm]
  unfold completeCorePairKernelMcal
  have h_each_ac :
      ∀ a ∈ Cd, ∀ c ∈ Cd,
        (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
            windowPairing Y (coreAdjustedProfileA c_lam c_half T D0 a)
              (coreAdjustedProfileA c_lam c_half T D0 c) -
          4 * ((ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
            ∑ pk ∈ primePowerPairsUpTo T,
              windowPairing Y (coreFeatureVectorB a T pk) (coreFeatureVectorB c T pk)) =
        (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
          (windowPairing Y (coreAdjustedProfileA c_lam c_half T D0 a)
              (coreAdjustedProfileA c_lam c_half T D0 c) -
            4 * ∑ pk ∈ primePowerPairsUpTo T,
              windowPairing Y (coreFeatureVectorB a T pk) (coreFeatureVectorB c T pk)) := by
    intro a _ c _; ring
  rw [Finset.mul_sum]
  have h_inner_mul :
      ∀ a ∈ Cd,
        4 * (∑ c ∈ Cd,
            (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
              ∑ pk ∈ primePowerPairsUpTo T,
                windowPairing Y (coreFeatureVectorB a T pk) (coreFeatureVectorB c T pk)) =
          ∑ c ∈ Cd,
            4 * ((ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
              ∑ pk ∈ primePowerPairsUpTo T,
                windowPairing Y (coreFeatureVectorB a T pk) (coreFeatureVectorB c T pk)) :=
    fun _ _ => Finset.mul_sum _ _ _
  rw [Finset.sum_congr rfl h_inner_mul, ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro a ha
  rw [← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl (h_each_ac a ha)

private theorem sector_moebius_and_log_gcd_identities_tc064_aux {Y : ℝ} (hY2 : 2 ≤ Y)
    (c_lam c_half : ℝ) (T D0 : ℕ) :
    (distinctSquarefreeCoreSumS c_lam c_half T D0 Y =
        ∑ g ∈ oddSquarefreeCommonFactorSet T,
          primitiveSquarefreeCoreSectorPi c_lam c_half T D0 Y g) ∧
      (∀ g ∈ oddSquarefreeCores T,
        primitiveSquarefreeCoreSectorPi c_lam c_half T D0 Y g +
            completeCorePairKernelMcal c_lam c_half T D0 Y g g =
          ∑ h ∈ (oddSquarefreeCores (T / g)).filter (Nat.Coprime g),
            (ArithmeticFunction.moebius h : ℝ) *
              (windowEnergyNormSq Y (divisibleCoreProfileSumS c_lam c_half T D0 (g * h)) -
                4 * ∑ pk ∈ primePowerPairsUpTo T,
                  windowEnergyNormSq Y (fun X => divisibleCoreFeatureSumF T (g * h) pk X))) ∧
      ((∑ g ∈ oddSquarefreeCommonFactorSet T,
          Real.log (g : ℝ) * primitiveSquarefreeCoreSectorPi c_lam c_half T D0 Y g) +
        (∑ a ∈ oddSquarefreeCores T,
          Real.log (a : ℝ) * completeCorePairKernelMcal c_lam c_half T D0 Y a a) =
        ∑ p ∈ (primesUpToFinset T).filter (fun p => 3 ≤ p),
          Real.log (p : ℝ) *
            (windowEnergyNormSq Y (divisibleCoreProfileSumS c_lam c_half T D0 p) -
              4 * ∑ pk ∈ primePowerPairsUpTo T,
                windowEnergyNormSq Y (fun X => divisibleCoreFeatureSumF T p pk X))) := by
  obtain ⟨h_fwd, h_inv, h_mu_cop, _⟩ := primitive_squarefree_core_pair_bijection_tc064_aux T
  let D_core := (oddSquarefreeCores T ×ˢ oddSquarefreeCores T).filter (fun ac => ac.1 ≠ ac.2)
  have h_distinct_prod :
      ∀ (w : ℕ → ℕ → ℝ),
        (∑ a ∈ oddSquarefreeCores T, ∑ c ∈ (oddSquarefreeCores T).erase a, w a c) =
          ∑ ac ∈ D_core, w ac.1 ac.2 := by
    intro w
    dsimp [D_core]
    rw [Finset.sum_filter, Finset.sum_product]
    apply Finset.sum_congr rfl
    intro a ha
    symm
    rw [← Finset.add_sum_erase _ _ ha, if_neg (not_not.mpr rfl), zero_add]
    apply Finset.sum_congr rfl
    intro c hc
    rw [if_pos (Finset.mem_erase.mp hc).1.symm]
  have h_sigma_bij :
      ∀ (w : ℕ → ℕ → ℝ),
        (∑ ac ∈ D_core, w ac.1 ac.2) =
          ∑ g ∈ oddSquarefreeCommonFactorSet T,
            ∑ rt ∈ primitiveSquarefreeCorePairs T g, w (g * rt.1) (g * rt.2) := by
    intro w
    rw [← Finset.sum_sigma (oddSquarefreeCommonFactorSet T) (primitiveSquarefreeCorePairs T)
      (fun grt => w (grt.1 * grt.2.1) (grt.1 * grt.2.2))]
    symm
    apply Finset.sum_bij (fun grt _ => (grt.1 * grt.2.1, grt.1 * grt.2.2))
    · rintro ⟨g, ⟨r, t⟩⟩ hmem
      rw [Finset.mem_sigma] at hmem
      obtain ⟨ha_in, hc_in, hac_ne, _, _, _⟩ := h_fwd g hmem.1 (r, t) hmem.2
      exact Finset.mem_filter.mpr ⟨Finset.mem_product.mpr ⟨ha_in, hc_in⟩, hac_ne⟩
    · rintro ⟨g1, ⟨r1, t1⟩⟩ h1 ⟨g2, ⟨r2, t2⟩⟩ h2 heq
      rw [Finset.mem_sigma] at h1 h2
      rw [Prod.mk.injEq] at heq
      have hf1 := h_fwd g1 h1.1 (r1, t1) h1.2
      have hf2 := h_fwd g2 h2.1 (r2, t2) h2.2
      dsimp only at h1 h2 heq hf1 hf2
      have hg_eq : g1 = g2 := by rw [← hf1.2.2.2.1, heq.1, heq.2, hf2.2.2.2.1]
      subst hg_eq
      have hr_eq : r1 = r2 := by rw [← hf1.2.2.2.2.1, heq.1, hf2.2.2.2.2.1]
      have ht_eq : t1 = t2 := by rw [← hf1.2.2.2.2.2, heq.2, hf2.2.2.2.2.2]
      subst hr_eq; subst ht_eq; rfl
    · rintro ⟨a, c⟩ hac
      obtain ⟨_, _, ⟨⟨g, ⟨r, t⟩⟩, ⟨hg', hrt', hgr', hgt'⟩, _⟩⟩ := h_inv (a, c) hac
      exact ⟨⟨g, (r, t)⟩, Finset.mem_sigma.mpr ⟨hg', hrt'⟩, Prod.ext hgr' hgt'⟩
    · intros; rfl
  have h_part1 :
      distinctSquarefreeCoreSumS c_lam c_half T D0 Y =
        ∑ g ∈ oddSquarefreeCommonFactorSet T,
          primitiveSquarefreeCoreSectorPi c_lam c_half T D0 Y g := by
    unfold distinctSquarefreeCoreSumS primitiveSquarefreeCoreSectorPi
    rw [h_distinct_prod, h_sigma_bij (fun a c =>
      (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
        completeCorePairKernelMcal c_lam c_half T D0 Y a c)]
    apply Finset.sum_congr rfl
    intro g hg
    have hg_sf : Squarefree g := (Finset.mem_filter.mp (Finset.mem_filter.mp hg).1).2.2.1
    apply Finset.sum_congr rfl
    intro rt hrt
    have h_cop : Nat.Coprime g (rt.1 * rt.2) := (Finset.mem_filter.mp hrt).2.2.2
    have h_mu_eq :
        (ArithmeticFunction.moebius (g * rt.1) : ℝ) *
            (ArithmeticFunction.moebius (g * rt.2) : ℝ) =
          (ArithmeticFunction.moebius rt.1 : ℝ) * (ArithmeticFunction.moebius rt.2 : ℝ) := by
      exact_mod_cast h_mu_cop hg_sf h_cop
    rw [h_mu_eq]
  have h_part2 :
      ∀ g ∈ oddSquarefreeCores T,
        primitiveSquarefreeCoreSectorPi c_lam c_half T D0 Y g +
            completeCorePairKernelMcal c_lam c_half T D0 Y g g =
          ∑ h ∈ (oddSquarefreeCores (T / g)).filter (Nat.Coprime g),
            (ArithmeticFunction.moebius h : ℝ) *
              (windowEnergyNormSq Y (divisibleCoreProfileSumS c_lam c_half T D0 (g * h)) -
                4 * ∑ pk ∈ primePowerPairsUpTo T,
                  windowEnergyNormSq Y (fun X => divisibleCoreFeatureSumF T (g * h) pk X)) := by
    intro g hg
    have hg_f := Finset.mem_filter.mp hg
    have hg1 : 1 ≤ g := (Finset.mem_Icc.mp hg_f.1).1
    have hg_o : Odd g := hg_f.2.1
    have hg_sf : Squarefree g := hg_f.2.2.1
    let Ug := (oddSquarefreeCores (T / g)).filter (Nat.Coprime g)
    have h1_in_Ug : 1 ∈ Ug := by
      simp only [Ug, oddSquarefreeCores, Finset.mem_filter, Finset.mem_Icc]
      have h2_div : 2 ≤ T / g := (Nat.le_div_iff_mul_le hg1).mpr (by linarith [hg_f.2.2.2])
      exact ⟨⟨⟨le_refl 1, by omega⟩, odd_one, squarefree_one, by omega⟩, Nat.coprime_one_right g⟩
    have h_div_bij :
        ∀ h ∈ Ug,
          (oddSquarefreeCores T).filter (fun a => g * h ∣ a) =
            (Ug.filter (fun r => h ∣ r)).image (fun r => g * r) := by
      intro h _
      ext a
      simp only [Finset.mem_filter, Finset.mem_image]
      constructor
      · rintro ⟨ha_c, hgh_dvd⟩
        have hg_dvd_a : g ∣ a := dvd_trans (dvd_mul_right g h) hgh_dvd
        let r := a / g
        have hgr : g * r = a := Nat.mul_div_cancel' hg_dvd_a
        have ha_cf := Finset.mem_filter.mp ha_c
        have ha_o : Odd a := ha_cf.2.1
        have ha_sf : Squarefree a := ha_cf.2.2.1
        have h2aT : 2 * a ≤ T := ha_cf.2.2.2
        have ha_p := squarefree_pos_and_coprime_of_mul_tc064_aux.2 (hgr.symm ▸ ha_sf)
        have hr_o : Odd r := (odd_of_odd_mul_tc064_aux (hgr.symm ▸ ha_o)).2
        have h2r_div : 2 * r ≤ T / g :=
          (Nat.le_div_iff_mul_le hg1).mpr (by linarith [show 2 * r * g = 2 * (g * r) by ring])
        have hh_dvd_r : h ∣ r := by
          rw [← hgr] at hgh_dvd
          exact (Nat.mul_dvd_mul_iff_left hg1).mp hgh_dvd
        refine ⟨r, ⟨?_, hh_dvd_r⟩, hgr⟩
        dsimp only [Ug]
        simp only [oddSquarefreeCores, Finset.mem_filter, Finset.mem_Icc]
        exact ⟨⟨⟨hr_o.pos, le_trans (Nat.le_mul_of_pos_left r (by decide)) h2r_div⟩,
          hr_o, ha_p.2.1, h2r_div⟩,
          ha_p.2.2⟩
      · rintro ⟨r, ⟨hr_Ug, hh_dvd_r⟩, rfl⟩
        simp only [Ug, oddSquarefreeCores, Finset.mem_filter, Finset.mem_Icc] at hr_Ug ⊢
        rcases hr_Ug with ⟨⟨⟨hr1, _⟩, hr_o, hr_sf, h2r_div⟩, hgr_cop⟩
        have h2gr : 2 * (g * r) ≤ T := by
          have hm := (Nat.le_div_iff_mul_le hg1).mp h2r_div
          linarith [show 2 * (g * r) = 2 * r * g by ring]
        exact ⟨⟨⟨Nat.mul_pos hg1 hr1, by omega⟩, hg_o.mul hr_o,
          (Nat.squarefree_mul hgr_cop).mpr ⟨hg_sf, hr_sf⟩, h2gr⟩,
          mul_dvd_mul_left g hh_dvd_r⟩
    have h_each_h :
        ∀ h ∈ Ug,
          (windowEnergyNormSq Y (divisibleCoreProfileSumS c_lam c_half T D0 (g * h)) -
              4 * ∑ pk ∈ primePowerPairsUpTo T,
                windowEnergyNormSq Y (fun X => divisibleCoreFeatureSumF T (g * h) pk X)) =
            ∑ r ∈ Ug, ∑ t ∈ Ug,
              if h ∣ r ∧ h ∣ t then
                (ArithmeticFunction.moebius r : ℝ) * (ArithmeticFunction.moebius t : ℝ) *
                  completeCorePairKernelMcal c_lam c_half T D0 Y (g * r) (g * t)
              else 0 := by
      intro h hh
      rw [divisibleCore_gram_identity_tc064_aux hY2 c_lam c_half T D0 (g * h), h_div_bij h hh]
      have h_inj_g : Set.InjOn (fun r => g * r) ↑(Ug.filter (fun r => h ∣ r)) :=
        fun _ _ _ _ heq => Nat.eq_of_mul_eq_mul_left hg1 heq
      rw [Finset.sum_image h_inj_g]
      have h_in_r :
          ∀ r ∈ Ug.filter (fun r => h ∣ r),
            (∑ c ∈ (Ug.filter (fun t => h ∣ t)).image (fun t => g * t),
                (ArithmeticFunction.moebius (g * r) : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                  completeCorePairKernelMcal c_lam c_half T D0 Y (g * r) c) =
              ∑ t ∈ Ug.filter (fun t => h ∣ t),
                (ArithmeticFunction.moebius r : ℝ) * (ArithmeticFunction.moebius t : ℝ) *
                  completeCorePairKernelMcal c_lam c_half T D0 Y (g * r) (g * t) := by
        intro r hr
        rw [Finset.sum_image h_inj_g]
        apply Finset.sum_congr rfl
        intro t ht
        have hr_cop : Nat.Coprime g r := (Finset.mem_filter.mp (Finset.mem_filter.mp hr).1).2
        have ht_cop : Nat.Coprime g t := (Finset.mem_filter.mp (Finset.mem_filter.mp ht).1).2
        have h_mu_eq :
            (ArithmeticFunction.moebius (g * r) : ℝ) * (ArithmeticFunction.moebius (g * t) : ℝ) =
              (ArithmeticFunction.moebius r : ℝ) * (ArithmeticFunction.moebius t : ℝ) := by
          exact_mod_cast h_mu_cop hg_sf (hr_cop.mul_right ht_cop)
        rw [h_mu_eq]
      rw [Finset.sum_congr rfl h_in_r, Finset.sum_filter (s := Ug)]
      apply Finset.sum_congr rfl
      intro r _
      rw [Finset.sum_filter (s := Ug)]
      by_cases hr_dvd : h ∣ r
      · rw [if_pos hr_dvd]
        apply Finset.sum_congr rfl
        intro t _
        by_cases ht_dvd : h ∣ t <;> simp [hr_dvd, ht_dvd]
      · rw [if_neg hr_dvd]
        symm
        apply Finset.sum_eq_zero
        intro t _; simp [hr_dvd]
    have h_rhs_exch :
        (∑ h ∈ Ug,
            (ArithmeticFunction.moebius h : ℝ) *
              (windowEnergyNormSq Y (divisibleCoreProfileSumS c_lam c_half T D0 (g * h)) -
                4 * ∑ pk ∈ primePowerPairsUpTo T,
                  windowEnergyNormSq Y (fun X => divisibleCoreFeatureSumF T (g * h) pk X))) =
          ∑ r ∈ Ug, ∑ t ∈ Ug,
            ((∑ h ∈ Ug.filter (fun h => h ∣ r ∧ h ∣ t), (ArithmeticFunction.moebius h : ℝ)) *
              ((ArithmeticFunction.moebius r : ℝ) * (ArithmeticFunction.moebius t : ℝ) *
                completeCorePairKernelMcal c_lam c_half T D0 Y (g * r) (g * t))) := by
      rw [Finset.sum_congr rfl (fun h hh => by rw [h_each_h h hh])]
      simp_rw [Finset.mul_sum]
      trans (∑ r ∈ Ug, ∑ h ∈ Ug, ∑ t ∈ Ug,
        (ArithmeticFunction.moebius h : ℝ) *
          (if h ∣ r ∧ h ∣ t then
            (ArithmeticFunction.moebius r : ℝ) * (ArithmeticFunction.moebius t : ℝ) *
              completeCorePairKernelMcal c_lam c_half T D0 Y (g * r) (g * t)
          else 0))
      · exact Finset.sum_comm
      apply Finset.sum_congr rfl
      intro r _
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro t _
      rw [Finset.sum_mul, Finset.sum_filter (s := Ug) (p := fun h => h ∣ r ∧ h ∣ t)]
      apply Finset.sum_congr rfl
      intro h _
      split_ifs <;> ring
    rw [h_rhs_exch]
    have h_moeb_sieve :
        ∀ r ∈ Ug, ∀ t ∈ Ug,
          (∑ h ∈ Ug.filter (fun h => h ∣ r ∧ h ∣ t), (ArithmeticFunction.moebius h : ℝ)) =
            if Nat.Coprime r t then 1 else 0 := by
      intro r hr t _
      have hr_Ug := Finset.mem_filter.mp hr
      have hr_cf := Finset.mem_filter.mp hr_Ug.1
      have hr1 : 1 ≤ r := (Finset.mem_Icc.mp hr_cf.1).1
      have hr_o : Odd r := hr_cf.2.1
      have hr_sf : Squarefree r := hr_cf.2.2.1
      have hgr_cop : Nat.Coprime g r := hr_Ug.2
      have hd_pos : 0 < Nat.gcd r t := Nat.gcd_pos_of_pos_left t hr1
      have h_set_eq : Ug.filter (fun h => h ∣ r ∧ h ∣ t) = (Nat.gcd r t).divisors := by
        ext h
        simp only [Finset.mem_filter, Nat.mem_divisors]
        constructor
        · rintro ⟨_, ⟨hhr, hht⟩⟩
          exact ⟨Nat.dvd_gcd hhr hht, ne_of_gt hd_pos⟩
        · rintro ⟨hh_gcd, _⟩
          have hhr : h ∣ r := dvd_trans hh_gcd (Nat.gcd_dvd_left r t)
          have hht : h ∣ t := dvd_trans hh_gcd (Nat.gcd_dvd_right r t)
          obtain ⟨q_r, hqr⟩ := hhr
          have hh_o : Odd h := (odd_of_odd_mul_tc064_aux (hqr ▸ hr_o)).1
          have hh_sf : Squarefree h := hr_sf.squarefree_of_dvd ⟨q_r, hqr⟩
          have hh_le_r : h ≤ r := Nat.le_of_dvd hr1 ⟨q_r, hqr⟩
          have hgh_cop : Nat.Coprime g h := hgr_cop.coprime_dvd_right ⟨q_r, hqr⟩
          refine ⟨?_, ⟨⟨q_r, hqr⟩, hht⟩⟩
          dsimp only [Ug]
          simp only [oddSquarefreeCores, Finset.mem_filter, Finset.mem_Icc]
          exact ⟨⟨⟨hh_o.pos, by omega⟩, hh_o, hh_sf, by omega⟩, hgh_cop⟩
      rw [h_set_eq]
      have h_cast :
          (∑ h ∈ (Nat.gcd r t).divisors, (ArithmeticFunction.moebius h : ℝ)) =
            ((∑ h ∈ (Nat.gcd r t).divisors, ArithmeticFunction.moebius h : ℤ) : ℝ) := by
        push_cast; rfl
      rw [h_cast]
      have h_conv_moeb :
          (∑ h ∈ (Nat.gcd r t).divisors, ArithmeticFunction.moebius h) =
            if Nat.gcd r t = 1 then 1 else 0 := by
        have hm :
            (ArithmeticFunction.moebius * (ArithmeticFunction.zeta : ArithmeticFunction ℤ))
              (Nat.gcd r t) =
              (1 : ArithmeticFunction ℤ) (Nat.gcd r t) := by
          rw [ArithmeticFunction.moebius_mul_coe_zeta]
        rw [ArithmeticFunction.coe_mul_zeta_apply, ArithmeticFunction.one_apply] at hm
        exact hm
      rw [h_conv_moeb]
      by_cases hcop : Nat.Coprime r t
      · rw [if_pos hcop, if_pos hcop.gcd_eq_one]; norm_num
      · have hne1 : Nat.gcd r t ≠ 1 := hcop
        rw [if_neg hcop, if_neg hne1]; norm_num
    have h_inner_eq :
        (∑ r ∈ Ug, ∑ t ∈ Ug,
            ((∑ h ∈ Ug.filter (fun h => h ∣ r ∧ h ∣ t), (ArithmeticFunction.moebius h : ℝ)) *
              ((ArithmeticFunction.moebius r : ℝ) * (ArithmeticFunction.moebius t : ℝ) *
                completeCorePairKernelMcal c_lam c_half T D0 Y (g * r) (g * t)))) =
          ∑ rt ∈ (Ug ×ˢ Ug).filter (fun rt => Nat.Coprime rt.1 rt.2),
            (ArithmeticFunction.moebius rt.1 : ℝ) * (ArithmeticFunction.moebius rt.2 : ℝ) *
              completeCorePairKernelMcal c_lam c_half T D0 Y (g * rt.1) (g * rt.2) := by
      rw [Finset.sum_filter (s := Ug ×ˢ Ug), Finset.sum_product]
      apply Finset.sum_congr rfl
      intro r hr
      apply Finset.sum_congr rfl
      intro t ht
      rw [h_moeb_sieve r hr t ht]
      split_ifs <;> ring
    rw [h_inner_eq]
    let C_cop := (Ug ×ˢ Ug).filter (fun rt => Nat.Coprime rt.1 rt.2)
    have h11_in : (1, 1) ∈ C_cop := by
      dsimp only [C_cop]
      simp only [Finset.mem_filter, Finset.mem_product]
      exact ⟨⟨h1_in_Ug, h1_in_Ug⟩, Nat.coprime_one_left 1⟩
    have h_erase_eq : C_cop.erase (1, 1) = primitiveSquarefreeCorePairs T g := by
      ext ⟨r, t⟩
      dsimp only [C_cop, Ug]
      simp only [primitiveSquarefreeCorePairs, Finset.mem_erase, Finset.mem_filter,
        Finset.mem_product]
      constructor
      · rintro ⟨hne11, ⟨⟨hr_c, hgr⟩, ⟨ht_c, hgt⟩⟩, hrt_cop⟩
        have hrt_ne : r ≠ t := by
          intro h_eq
          subst h_eq
          have hr1_eq : r = 1 := by simpa using hrt_cop.gcd_eq_one
          exact hne11 (Prod.ext hr1_eq hr1_eq)
        exact ⟨⟨hr_c, ht_c⟩, hrt_ne, hrt_cop, hgr.mul_right hgt⟩
      · rintro ⟨⟨hr_c, ht_c⟩, hrt_ne, hrt_cop, h_grt⟩
        have hne11 : (r, t) ≠ (1, 1) :=
          fun h => hrt_ne ((Prod.mk.inj h).1.trans (Prod.mk.inj h).2.symm)
        exact ⟨hne11, ⟨⟨hr_c, h_grt.coprime_dvd_right (dvd_mul_right r t)⟩,
          ⟨ht_c, h_grt.coprime_dvd_right (dvd_mul_left t r)⟩⟩, hrt_cop⟩
    rw [← Finset.add_sum_erase _ _ h11_in, h_erase_eq]
    unfold primitiveSquarefreeCoreSectorPi
    simp [ArithmeticFunction.moebius_apply_one]
    ring
  refine ⟨h_part1, h_part2, ?_⟩
  -- Part 3: Exact logarithmic GCD-weighted prime-divisibility identity
  let P_odd := (primesUpToFinset T).filter (fun p => 3 ≤ p)
  have h_lhs_full :
      (∑ g ∈ oddSquarefreeCommonFactorSet T,
          Real.log (g : ℝ) * primitiveSquarefreeCoreSectorPi c_lam c_half T D0 Y g) +
        (∑ a ∈ oddSquarefreeCores T,
          Real.log (a : ℝ) * completeCorePairKernelMcal c_lam c_half T D0 Y a a) =
        ∑ a ∈ oddSquarefreeCores T, ∑ c ∈ oddSquarefreeCores T,
          Real.log (Nat.gcd a c : ℝ) *
            ((ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
              completeCorePairKernelMcal c_lam c_half T D0 Y a c) := by
    have h_off :
        (∑ g ∈ oddSquarefreeCommonFactorSet T,
            Real.log (g : ℝ) * primitiveSquarefreeCoreSectorPi c_lam c_half T D0 Y g) =
          ∑ a ∈ oddSquarefreeCores T, ∑ c ∈ (oddSquarefreeCores T).erase a,
            Real.log (Nat.gcd a c : ℝ) *
              ((ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                completeCorePairKernelMcal c_lam c_half T D0 Y a c) := by
      rw [h_distinct_prod, h_sigma_bij (fun a c =>
        Real.log (Nat.gcd a c : ℝ) *
          ((ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
            completeCorePairKernelMcal c_lam c_half T D0 Y a c))]
      unfold primitiveSquarefreeCoreSectorPi
      apply Finset.sum_congr rfl
      intro g hg
      have hg_sf : Squarefree g := (Finset.mem_filter.mp (Finset.mem_filter.mp hg).1).2.2.1
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro rt hrt
      have hf_rt := h_fwd g hg rt hrt
      have h_cop : Nat.Coprime g (rt.1 * rt.2) := (Finset.mem_filter.mp hrt).2.2.2
      have h_mu_eq :
          (ArithmeticFunction.moebius (g * rt.1) : ℝ) *
              (ArithmeticFunction.moebius (g * rt.2) : ℝ) =
            (ArithmeticFunction.moebius rt.1 : ℝ) * (ArithmeticFunction.moebius rt.2 : ℝ) := by
        exact_mod_cast h_mu_cop hg_sf h_cop
      rw [hf_rt.2.2.2.1, h_mu_eq]
    rw [h_off, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro a ha
    have ha_sf : Squarefree a := (Finset.mem_filter.mp ha).2.2.1
    have h_mu_sq := (liouvilleLambda_squarefree_mul_sq_eq_moebius_tc064_aux ha_sf (le_refl 1)).2
    rw [← Finset.add_sum_erase (oddSquarefreeCores T)
      (fun c => Real.log (Nat.gcd a c : ℝ) *
        ((ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
          completeCorePairKernelMcal c_lam c_half T D0 Y a c)) ha,
      Nat.gcd_self, ← sq, h_mu_sq, one_mul, add_comm]
  rw [h_lhs_full]
  have h_log_gcd :
      ∀ a ∈ oddSquarefreeCores T, ∀ c ∈ oddSquarefreeCores T,
        Real.log (Nat.gcd a c : ℝ) =
          ∑ p ∈ P_odd, if p ∣ a ∧ p ∣ c then Real.log (p : ℝ) else 0 := by
    intro a ha c _
    have ha_f := Finset.mem_filter.mp ha
    have ha1 : 1 ≤ a := (Finset.mem_Icc.mp ha_f.1).1
    have haT : a ≤ T := (Finset.mem_Icc.mp ha_f.1).2
    have ha_o : Odd a := ha_f.2.1
    have ha_sf : Squarefree a := ha_f.2.2.1
    let d := Nat.gcd a c
    have hd_dvd_a : d ∣ a := Nat.gcd_dvd_left a c
    have hd_sf : Squarefree d := ha_sf.squarefree_of_dvd hd_dvd_a
    have hd_prod : (∏ p ∈ d.primeFactors, (p : ℝ)) = (d : ℝ) := by
      rw [← Nat.cast_prod, Nat.prod_primeFactors_of_squarefree hd_sf]
    have h_log_pf : Real.log (d : ℝ) = ∑ p ∈ d.primeFactors, Real.log (p : ℝ) := by
      rw [← hd_prod, Real.log_prod _ _ (fun p hp =>
        Nat.cast_ne_zero.mpr (Nat.prime_of_mem_primeFactors hp).ne_zero)]
    have h_pf_eq : d.primeFactors = P_odd.filter (fun p => p ∣ a ∧ p ∣ c) := by
      ext p
      dsimp only [P_odd]
      simp only [primesUpToFinset, Nat.mem_primeFactors, Finset.mem_filter,
        Finset.mem_Icc, Finset.mem_range]
      constructor
      · rintro ⟨hp_pr, hp_dvd_d, _⟩
        have hpa : p ∣ a := dvd_trans hp_dvd_d hd_dvd_a
        have hpc : p ∣ c := dvd_trans hp_dvd_d (Nat.gcd_dvd_right a c)
        have hp_le_T : p ≤ T := le_trans (Nat.le_of_dvd ha1 hpa) haT
        have hp_ne2 : p ≠ 2 := by
          intro h2; subst h2
          exact (Nat.odd_iff_not_even.mp ha_o) (even_iff_two_dvd.mpr hpa)
        have hp_ge2 : 2 ≤ p := hp_pr.two_le
        have hp_ge3 : 3 ≤ p := by omega
        refine ⟨⟨?_, hp_ge3⟩, ⟨hpa, hpc⟩⟩
        exact ⟨by omega, hp_pr⟩
      · rintro ⟨⟨⟨_, hp_pr⟩, _⟩, ⟨hpa, hpc⟩⟩
        exact ⟨hp_pr, Nat.dvd_gcd hpa hpc, ne_of_gt (Nat.gcd_pos_of_pos_left c ha1)⟩
    rw [h_log_pf, h_pf_eq, Finset.sum_filter (s := P_odd)]
  have h_exch :
      (∑ a ∈ oddSquarefreeCores T, ∑ c ∈ oddSquarefreeCores T,
          Real.log (Nat.gcd a c : ℝ) *
            ((ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
              completeCorePairKernelMcal c_lam c_half T D0 Y a c)) =
        ∑ p ∈ P_odd,
          Real.log (p : ℝ) *
            ∑ a ∈ (oddSquarefreeCores T).filter (fun a => p ∣ a),
              ∑ c ∈ (oddSquarefreeCores T).filter (fun c => p ∣ c),
                (ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                  completeCorePairKernelMcal c_lam c_half T D0 Y a c := by
    have h_rw :
        ∀ a ∈ oddSquarefreeCores T,
          (∑ c ∈ oddSquarefreeCores T,
              Real.log (Nat.gcd a c : ℝ) *
                ((ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                  completeCorePairKernelMcal c_lam c_half T D0 Y a c)) =
            ∑ p ∈ P_odd, ∑ c ∈ oddSquarefreeCores T,
              (if p ∣ a ∧ p ∣ c then Real.log (p : ℝ) else 0) *
                ((ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
                  completeCorePairKernelMcal c_lam c_half T D0 Y a c) := by
      intro a ha
      trans (∑ c ∈ oddSquarefreeCores T, ∑ p ∈ P_odd,
        (if p ∣ a ∧ p ∣ c then Real.log (p : ℝ) else 0) *
          ((ArithmeticFunction.moebius a : ℝ) * (ArithmeticFunction.moebius c : ℝ) *
            completeCorePairKernelMcal c_lam c_half T D0 Y a c))
      · apply Finset.sum_congr rfl
        intro c hc
        rw [h_log_gcd a ha c hc, Finset.sum_mul]
      · exact Finset.sum_comm
    rw [Finset.sum_congr rfl h_rw, Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro p _
    rw [Finset.mul_sum, Finset.sum_filter]
    apply Finset.sum_congr rfl
    intro a _
    by_cases hpa : p ∣ a
    · rw [if_pos hpa, Finset.mul_sum, Finset.sum_filter]
      apply Finset.sum_congr rfl
      intro c _
      by_cases hpc : p ∣ c <;> simp [hpa, hpc, mul_assoc]
    · rw [if_neg hpa]
      apply Finset.sum_eq_zero
      intro c _; simp [hpa]
  rw [h_exch]
  apply Finset.sum_congr rfl
  intro p _
  rw [divisibleCore_gram_identity_tc064_aux hY2 c_lam c_half T D0 p]

private theorem prime_toggle_identities_tc064_aux {p : ℕ} (hp : Nat.Prime p) (hp_o : Odd p) :
    (∀ {a : ℕ}, Odd a → Squarefree a →
      squarefreeCoreStar a p ≠ a ∧
        squarefreeCoreStar (squarefreeCoreStar a p) p = a ∧
        ArithmeticFunction.moebius (squarefreeCoreStar a p) = -ArithmeticFunction.moebius a) ∧
    (∀ T : ℕ,
      Disjoint (primeTogglePairedCores p T) (primeToggleBoundaryCores p T) ∧
        primeTogglePairedCores p T ∪ primeToggleBoundaryCores p T = oddSquarefreeCores T ∧
        primeToggleBoundaryCores p T =
          (oddSquarefreeCores T).filter (fun a => ¬ p ∣ a ∧ T < 2 * p * a)) ∧
    (∀ (T : ℕ) (w : ℕ → ℝ),
      (∑ a ∈ oddSquarefreeCores T, (ArithmeticFunction.moebius a : ℝ) * w a) =
        (1 / 2 : ℝ) *
            (∑ a ∈ primeTogglePairedCores p T,
              (ArithmeticFunction.moebius a : ℝ) * (w a - w (squarefreeCoreStar a p))) +
          ∑ a ∈ primeToggleBoundaryCores p T, (ArithmeticFunction.moebius a : ℝ) * w a) := by
  have hp_sf : Squarefree p := hp.squarefree
  have hp_ge3 : 3 ≤ p := by
    have hp2 : 2 ≤ p := hp.two_le
    have hp_ne2 : p ≠ 2 := fun h2 => (Nat.odd_iff_not_even.mp hp_o) (h2 ▸ even_two)
    omega
  have h_star_cases :
      ∀ {a : ℕ}, Odd a → Squarefree a →
        (p ∣ a → squarefreeCoreStar a p = a / p) ∧
          (¬ p ∣ a → squarefreeCoreStar a p = p * a) := by
    intro a _ _
    refine ⟨?_, ?_⟩
    · intro hpa
      obtain ⟨a0, rfl⟩ := hpa
      unfold squarefreeCoreStar
      have hgcd : Nat.gcd (p * a0) p = p := Nat.gcd_eq_right ⟨a0, rfl⟩
      rw [hgcd, show p * a0 * p = a0 * p ^ 2 by ring,
        Nat.mul_div_cancel _ (pow_pos hp.pos 2), Nat.mul_div_right a0 hp.pos]
    · intro hnpa
      have hcop : Nat.Coprime a p := (hp.coprime_iff_not_dvd.mpr hnpa).symm
      unfold squarefreeCoreStar
      rw [hcop.gcd_eq_one, one_pow, Nat.div_one, mul_comm]
  have h_part1 :
      ∀ {a : ℕ}, Odd a → Squarefree a →
        squarefreeCoreStar a p ≠ a ∧
          squarefreeCoreStar (squarefreeCoreStar a p) p = a ∧
          ArithmeticFunction.moebius (squarefreeCoreStar a p) = -ArithmeticFunction.moebius a := by
    intro a ha_o ha_sf
    have h_inv := (squarefreeCoreStar_props_tc064_aux ha_o ha_sf hp_o hp_sf).2.1
    by_cases hpa : p ∣ a
    · have h_eq := (h_star_cases ha_o ha_sf).1 hpa
      obtain ⟨a0, rfl⟩ := hpa
      have ha0_eq : p * a0 / p = a0 := Nat.mul_div_right a0 hp.pos
      rw [h_eq, ha0_eq]
      have ha0_pos : 0 < a0 := (odd_of_odd_mul_tc064_aux ha_o).2.pos
      have h_ne : a0 ≠ p * a0 := by nlinarith
      have h_cop : Nat.Coprime p a0 := (squarefree_pos_and_coprime_of_mul_tc064_aux.2 ha_sf).2.2
      have h_mu : ArithmeticFunction.moebius (p * a0) = -ArithmeticFunction.moebius a0 := by
        rw [ArithmeticFunction.isMultiplicative_moebius.map_mul_of_coprime h_cop,
          ArithmeticFunction.moebius_apply_prime hp]
        ring
      exact ⟨h_ne, by rwa [h_eq, ha0_eq] at h_inv, by omega⟩
    · have h_eq := (h_star_cases ha_o ha_sf).2 hpa
      rw [h_eq]
      have ha_pos : 0 < a := ha_o.pos
      have h_ne : p * a ≠ a := by nlinarith
      have h_cop : Nat.Coprime p a := hp.coprime_iff_not_dvd.mpr hpa
      have h_mu : ArithmeticFunction.moebius (p * a) = -ArithmeticFunction.moebius a := by
        rw [ArithmeticFunction.isMultiplicative_moebius.map_mul_of_coprime h_cop,
          ArithmeticFunction.moebius_apply_prime hp]
        ring
      exact ⟨h_ne, by rwa [h_eq] at h_inv, h_mu⟩
  have h_part2 :
      ∀ T : ℕ,
        Disjoint (primeTogglePairedCores p T) (primeToggleBoundaryCores p T) ∧
          primeTogglePairedCores p T ∪ primeToggleBoundaryCores p T = oddSquarefreeCores T ∧
          primeToggleBoundaryCores p T =
            (oddSquarefreeCores T).filter (fun a => ¬ p ∣ a ∧ T < 2 * p * a) := by
    intro T
    have h_disj : Disjoint (primeTogglePairedCores p T) (primeToggleBoundaryCores p T) := by
      unfold primeTogglePairedCores primeToggleBoundaryCores
      rw [Finset.disjoint_filter]
      intro _ _ h_in h_not; exact h_not h_in
    have h_union : primeTogglePairedCores p T ∪ primeToggleBoundaryCores p T = oddSquarefreeCores T := by
      unfold primeTogglePairedCores primeToggleBoundaryCores
      exact Finset.filter_union_filter_neg_eq _ (oddSquarefreeCores T)
    refine ⟨h_disj, h_union, ?_⟩
    ext a
    simp only [primeToggleBoundaryCores, Finset.mem_filter]
    constructor
    · rintro ⟨ha_c, h_not_in⟩
      have ha_f := Finset.mem_filter.mp ha_c
      have ha_o : Odd a := ha_f.2.1
      have ha_sf : Squarefree a := ha_f.2.2.1
      have h_st_props := (squarefreeCoreStar_props_tc064_aux ha_o ha_sf hp_o hp_sf).1
      have h_not_p : ¬ p ∣ a := by
        intro hpa
        apply h_not_in
        have h_eq := (h_star_cases ha_o ha_sf).1 hpa
        have hle_a : a / p ≤ a := Nat.div_le_self a p
        simp only [oddSquarefreeCores, Finset.mem_filter, Finset.mem_Icc]
        exact ⟨⟨h_st_props.2.2, by rw [h_eq]; omega⟩, h_st_props.1, h_st_props.2.1,
          by rw [h_eq]; omega⟩
      have h_eq := (h_star_cases ha_o ha_sf).2 h_not_p
      have h_gt : T < 2 * p * a := by
        by_contra h_le
        apply h_not_in
        have h2pa_le : 2 * (p * a) ≤ T := by
          linarith [show 2 * (p * a) = 2 * p * a by ring]
        simp only [oddSquarefreeCores, Finset.mem_filter, Finset.mem_Icc]
        exact ⟨⟨h_st_props.2.2, by rw [h_eq]; omega⟩, h_st_props.1, h_st_props.2.1,
          by rw [h_eq]; exact h2pa_le⟩
      exact ⟨ha_c, h_not_p, h_gt⟩
    · rintro ⟨ha_c, h_not_p, h_gt⟩
      have ha_f := Finset.mem_filter.mp ha_c
      have h_eq := (h_star_cases ha_f.2.1 ha_f.2.2.1).2 h_not_p
      refine ⟨ha_c, ?_⟩
      intro h_in
      have h2_le : 2 * squarefreeCoreStar a p ≤ T := (Finset.mem_filter.mp h_in).2.2.2
      rw [h_eq] at h2_le
      linarith [show 2 * (p * a) = 2 * p * a by ring]
  refine ⟨h_part1, h_part2, ?_⟩
  intro T w
  obtain ⟨h_disj, h_union, _⟩ := h_part2 T
  rw [← h_union, Finset.sum_union h_disj]
  congr 1
  have h_bij :
      (∑ a ∈ primeTogglePairedCores p T, (ArithmeticFunction.moebius a : ℝ) * w a) =
        ∑ a ∈ primeTogglePairedCores p T,
          -(ArithmeticFunction.moebius a : ℝ) * w (squarefreeCoreStar a p) := by
    symm
    apply Finset.sum_bij (fun a _ => squarefreeCoreStar a p)
    · intro a ha
      simp only [primeTogglePairedCores, Finset.mem_filter] at ha ⊢
      have ha_f := Finset.mem_filter.mp ha.1
      have h_inv := (h_part1 ha_f.2.1 ha_f.2.2.1).2.1
      exact ⟨ha.2, by rw [h_inv]; exact ha.1⟩
    · intro a1 ha1 a2 ha2 heq
      have h1 := Finset.mem_filter.mp (Finset.mem_filter.mp ha1).1
      have h2 := Finset.mem_filter.mp (Finset.mem_filter.mp ha2).1
      rw [← (h_part1 h1.2.1 h1.2.2.1).2.1, heq, (h_part1 h2.2.1 h2.2.2.1).2.1]
    · intro b hb
      simp only [primeTogglePairedCores, Finset.mem_filter] at hb
      have hb_f := Finset.mem_filter.mp hb.1
      have h_inv := (h_part1 hb_f.2.1 hb_f.2.2.1).2.1
      refine ⟨squarefreeCoreStar b p, ?_, h_inv⟩
      simp only [primeTogglePairedCores, Finset.mem_filter]
      exact ⟨hb.2, by rw [h_inv]; exact hb.1⟩
    · intro a ha
      have ha_f := Finset.mem_filter.mp (Finset.mem_filter.mp ha).1
      have h_mu := (h_part1 ha_f.2.1 ha_f.2.2.1).2.2
      have h_mu_r :
          (ArithmeticFunction.moebius (squarefreeCoreStar a p) : ℝ) =
            -(ArithmeticFunction.moebius a : ℝ) := by
        exact_mod_cast h_mu
      rw [h_mu_r]
  have h_sum_diff :
      (∑ a ∈ primeTogglePairedCores p T,
          (ArithmeticFunction.moebius a : ℝ) * (w a - w (squarefreeCoreStar a p))) =
        (∑ a ∈ primeTogglePairedCores p T, (ArithmeticFunction.moebius a : ℝ) * w a) +
          (∑ a ∈ primeTogglePairedCores p T,
            -(ArithmeticFunction.moebius a : ℝ) * w (squarefreeCoreStar a p)) := by
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro a _; ring
  rw [h_sum_diff, ← h_bij]
  ring

/-- **Theorem 4 (`TASK-TC-064` §4, Attempt 1 Squarefree-Core GCD Sectors, Möbius Sector Diagonalization, Log-GCD Prime-Divisibility Identity, and Attempt 2 Prime-Toggle Anti-Invariance & Grouped-Profile Identities)**:
    1. *Attempt 1 (Squarefree-core common-factor decomposition, Möbius sector diagonalization, & logarithmic GCD prime identity)*:
       - Unique odd-squarefree `gcd` primitive-pair bijection, `moebius (g * r) * moebius (g * t) = moebius r * moebius t`, `coreSquareMultipliers (g * r) T = coreSquareMultipliers r (T / g)`, and `distinctSquarefreeCoreSumS = ∑_{g ∈ oddSquarefreeCommonFactorSet T} primitiveSquarefreeCoreSectorPi ... g`;
       - For `2 ≤ Y` and `g ∈ oddSquarefreeCores T`:
         `primitiveSquarefreeCoreSectorPi ... g + completeCorePairKernelMcal ... g g = ∑_{h ∈ (oddSquarefreeCores (T / g)).filter (Nat.Coprime g)} μ(h) * (‖Scal_{g*h}‖_Y^2 - 4 * ∑_{pk} ‖Fcal_{g*h, pk}‖_Y^2)`;
       - For `2 ≤ Y`:
         `(∑_{g} log g * Π_core(g)) + (∑_{a} log a * Mcal_Y(a, a)) = ∑_{p ≤ T, 3 ≤ p prime} log p * (‖Scal_p‖_Y^2 - 4 * ∑_{pk} ‖Fcal_{p, pk}‖_Y^2)`;
    2. *Attempt 2 (Prime-toggle involution, sign anti-invariance, boundary characterization, & grouped-profile / feature identities)*:
       For every odd prime `p` (`Nat.Prime p ∧ Odd p`):
       - `squarefreeCoreStar a p ≠ a`, `squarefreeCoreStar (squarefreeCoreStar a p) p = a`, and `moebius (squarefreeCoreStar a p) = -moebius a` for all odd squarefree `a`;
       - Exact partition `oddSquarefreeCores T = primeTogglePairedCores p T ⊔ primeToggleBoundaryCores p T` with `primeToggleBoundaryCores p T = (oddSquarefreeCores T).filter (fun a => ¬ p ∣ a ∧ T < 2 * p * a)`;
       - Exact prime-toggle identities for `divisibleCoreProfileSumS c_lam c_half T D0 1 X` and `divisibleCoreFeatureSumF T 1 pk X`, plus convex/affine prime combinations for `∑ p ∈ S, w p = 1`. -/
theorem squarefree_core_gcd_prime_sector_and_prime_toggle_identities_tc064 :
    ((∀ T : ℕ,
        (∀ g ∈ oddSquarefreeCommonFactorSet T,
          ∀ rt ∈ primitiveSquarefreeCorePairs T g,
            g * rt.1 ∈ oddSquarefreeCores T ∧ g * rt.2 ∈ oddSquarefreeCores T ∧
              g * rt.1 ≠ g * rt.2 ∧ Nat.gcd (g * rt.1) (g * rt.2) = g ∧
              (g * rt.1) / g = rt.1 ∧ (g * rt.2) / g = rt.2) ∧
        (∀ ac ∈ (oddSquarefreeCores T ×ˢ oddSquarefreeCores T).filter (fun ac => ac.1 ≠ ac.2),
          Nat.gcd ac.1 ac.2 ∈ oddSquarefreeCommonFactorSet T ∧
            (ac.1 / Nat.gcd ac.1 ac.2, ac.2 / Nat.gcd ac.1 ac.2) ∈
              primitiveSquarefreeCorePairs T (Nat.gcd ac.1 ac.2) ∧
            ∃! grt : ℕ × (ℕ × ℕ),
              grt.1 ∈ oddSquarefreeCommonFactorSet T ∧
                grt.2 ∈ primitiveSquarefreeCorePairs T grt.1 ∧
                grt.1 * grt.2.1 = ac.1 ∧ grt.1 * grt.2.2 = ac.2)) ∧
      (∀ {g r t : ℕ}, Squarefree g → Nat.Coprime g (r * t) →
        ArithmeticFunction.moebius (g * r) * ArithmeticFunction.moebius (g * t) =
          ArithmeticFunction.moebius r * ArithmeticFunction.moebius t) ∧
      (∀ {g r : ℕ} (T : ℕ), 1 ≤ g → 1 ≤ r →
        coreSquareMultipliers (g * r) T = coreSquareMultipliers r (T / g)) ∧
      (∀ {Y : ℝ}, 2 ≤ Y → ∀ (c_lam c_half : ℝ) (T D0 : ℕ),
        distinctSquarefreeCoreSumS c_lam c_half T D0 Y =
          ∑ g ∈ oddSquarefreeCommonFactorSet T,
            primitiveSquarefreeCoreSectorPi c_lam c_half T D0 Y g) ∧
      (∀ {Y : ℝ}, 2 ≤ Y → ∀ (c_lam c_half : ℝ) (T D0 : ℕ),
        ∀ g ∈ oddSquarefreeCores T,
          primitiveSquarefreeCoreSectorPi c_lam c_half T D0 Y g +
              completeCorePairKernelMcal c_lam c_half T D0 Y g g =
            ∑ h ∈ (oddSquarefreeCores (T / g)).filter (Nat.Coprime g),
              (ArithmeticFunction.moebius h : ℝ) *
                (windowEnergyNormSq Y (divisibleCoreProfileSumS c_lam c_half T D0 (g * h)) -
                  4 * ∑ pk ∈ primePowerPairsUpTo T,
                    windowEnergyNormSq Y (fun X => divisibleCoreFeatureSumF T (g * h) pk X))) ∧
      (∀ {Y : ℝ}, 2 ≤ Y → ∀ (c_lam c_half : ℝ) (T D0 : ℕ),
        (∑ g ∈ oddSquarefreeCommonFactorSet T,
            Real.log (g : ℝ) * primitiveSquarefreeCoreSectorPi c_lam c_half T D0 Y g) +
          (∑ a ∈ oddSquarefreeCores T,
            Real.log (a : ℝ) * completeCorePairKernelMcal c_lam c_half T D0 Y a a) =
          ∑ p ∈ (primesUpToFinset T).filter (fun p => 3 ≤ p),
            Real.log (p : ℝ) *
              (windowEnergyNormSq Y (divisibleCoreProfileSumS c_lam c_half T D0 p) -
                4 * ∑ pk ∈ primePowerPairsUpTo T,
                  windowEnergyNormSq Y (fun X => divisibleCoreFeatureSumF T p pk X)))) ∧
    ((∀ {p : ℕ}, Nat.Prime p → Odd p →
        (∀ {a : ℕ}, Odd a → Squarefree a →
          squarefreeCoreStar a p ≠ a ∧
            squarefreeCoreStar (squarefreeCoreStar a p) p = a ∧
            ArithmeticFunction.moebius (squarefreeCoreStar a p) =
              -ArithmeticFunction.moebius a) ∧
        (∀ T : ℕ,
          Disjoint (primeTogglePairedCores p T) (primeToggleBoundaryCores p T) ∧
            primeTogglePairedCores p T ∪ primeToggleBoundaryCores p T = oddSquarefreeCores T ∧
            primeToggleBoundaryCores p T =
              (oddSquarefreeCores T).filter (fun a => ¬ p ∣ a ∧ T < 2 * p * a)) ∧
        (∀ (c_lam c_half : ℝ) (T D0 : ℕ) (X : ℝ),
          divisibleCoreProfileSumS c_lam c_half T D0 1 X =
            (1 / 2 : ℝ) *
                (∑ a ∈ primeTogglePairedCores p T,
                  (ArithmeticFunction.moebius a : ℝ) *
                    (coreAdjustedProfileA c_lam c_half T D0 a X -
                      coreAdjustedProfileA c_lam c_half T D0 (squarefreeCoreStar a p) X)) +
              ∑ a ∈ primeToggleBoundaryCores p T,
                (ArithmeticFunction.moebius a : ℝ) *
                  coreAdjustedProfileA c_lam c_half T D0 a X) ∧
        (∀ (T : ℕ) (pk : ℕ × ℕ) (X : ℝ),
          divisibleCoreFeatureSumF T 1 pk X =
            (1 / 2 : ℝ) *
                (∑ a ∈ primeTogglePairedCores p T,
                  (ArithmeticFunction.moebius a : ℝ) *
                    (coreFeatureVectorB a T pk X -
                      coreFeatureVectorB (squarefreeCoreStar a p) T pk X)) +
              ∑ a ∈ primeToggleBoundaryCores p T,
                (ArithmeticFunction.moebius a : ℝ) * coreFeatureVectorB a T pk X)) ∧
      (∀ (S : Finset ℕ) (w : ℕ → ℝ),
        (∀ p ∈ S, Nat.Prime p ∧ Odd p) →
        (∑ p ∈ S, w p) = 1 →
        ∀ (c_lam c_half : ℝ) (T D0 : ℕ) (X : ℝ),
          divisibleCoreProfileSumS c_lam c_half T D0 1 X =
            ∑ p ∈ S, w p *
              ((1 / 2 : ℝ) *
                  (∑ a ∈ primeTogglePairedCores p T,
                    (ArithmeticFunction.moebius a : ℝ) *
                      (coreAdjustedProfileA c_lam c_half T D0 a X -
                        coreAdjustedProfileA c_lam c_half T D0 (squarefreeCoreStar a p) X)) +
                ∑ a ∈ primeToggleBoundaryCores p T,
                  (ArithmeticFunction.moebius a : ℝ) *
                    coreAdjustedProfileA c_lam c_half T D0 a X))) := by
  have h_filt_one : ∀ T : ℕ, (oddSquarefreeCores T).filter (fun a => 1 ∣ a) = oddSquarefreeCores T := by
    intro T; ext a; simp
  refine ⟨⟨fun T => ⟨(primitive_squarefree_core_pair_bijection_tc064_aux T).1,
        (primitive_squarefree_core_pair_bijection_tc064_aux T).2.1⟩,
      fun hg_sf h_cop => (primitive_squarefree_core_pair_bijection_tc064_aux 0).2.2.1 hg_sf h_cop,
      fun T hg1 hr1 => (primitive_squarefree_core_pair_bijection_tc064_aux 0).2.2.2 T hg1 hr1,
      fun {_} hY2 c_lam c_half T D0 =>
        (sector_moebius_and_log_gcd_identities_tc064_aux hY2 c_lam c_half T D0).1,
      fun {_} hY2 c_lam c_half T D0 =>
        (sector_moebius_and_log_gcd_identities_tc064_aux hY2 c_lam c_half T D0).2.1,
      fun {_} hY2 c_lam c_half T D0 =>
        (sector_moebius_and_log_gcd_identities_tc064_aux hY2 c_lam c_half T D0).2.2⟩,
    ⟨?_, ?_⟩⟩
  · intro p hp hp_o
    obtain ⟨hp1, hp2, hp3⟩ := prime_toggle_identities_tc064_aux hp hp_o
    refine ⟨hp1, hp2, ?_, ?_⟩
    · intro c_lam c_half T D0 X
      unfold divisibleCoreProfileSumS
      rw [h_filt_one T]
      exact hp3 T (fun a => coreAdjustedProfileA c_lam c_half T D0 a X)
    · intro T pk X
      unfold divisibleCoreFeatureSumF
      rw [h_filt_one T]
      exact hp3 T (fun a => coreFeatureVectorB a T pk X)
  · intro S w hS hw c_lam c_half T D0 X
    have h_each_p :
        ∀ p ∈ S,
          w p * ((1 / 2 : ℝ) *
              (∑ a ∈ primeTogglePairedCores p T,
                (ArithmeticFunction.moebius a : ℝ) *
                  (coreAdjustedProfileA c_lam c_half T D0 a X -
                    coreAdjustedProfileA c_lam c_half T D0 (squarefreeCoreStar a p) X)) +
            ∑ a ∈ primeToggleBoundaryCores p T,
              (ArithmeticFunction.moebius a : ℝ) *
                coreAdjustedProfileA c_lam c_half T D0 a X) =
            w p * divisibleCoreProfileSumS c_lam c_half T D0 1 X := by
      intro p hpS
      obtain ⟨hp_pr, hp_o⟩ := hS p hpS
      unfold divisibleCoreProfileSumS
      rw [h_filt_one T,
        (prime_toggle_identities_tc064_aux hp_pr hp_o).2.2 T
          (fun a => coreAdjustedProfileA c_lam c_half T D0 a X)]
    rw [Finset.sum_congr rfl h_each_p, ← Finset.sum_mul, hw, one_mul]

/-! ### Section 5: Finite Euler-Factor Dirichlet Multiplier & Dilation Equivalence (`TASK-TC-064` §5) -/

private theorem toggle_pair_coeff_identities_tc064_aux {q : ℕ} (hq : Nat.Prime q)
    {a : ℕ → ℝ} (ha_neg : ∀ m : ℕ, 1 ≤ m → a (q * m) = -a m) :
    let b : ℕ → ℝ := fun n => a n * (-1 : ℝ) ^ (n.factorization q)
    (∀ (k : ℕ) {m : ℕ}, 1 ≤ m →
      a (q ^ k * m) = (-1 : ℝ) ^ k * a m ∧ b (q ^ k * m) = b m) ∧
    (∀ {n : ℕ}, 1 ≤ n →
      (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n) = Finset.Icc 1 (n.factorization q) ∧
        b n = a n + 2 * ∑ k ∈ (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n), a (n / q ^ k) ∧
        a n = b n + 2 * ∑ k ∈ (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n),
          (-1 : ℝ) ^ k * b (n / q ^ k)) := by
  intro b
  have h_pow_k :
      ∀ (k : ℕ) {m : ℕ}, 1 ≤ m →
        a (q ^ k * m) = (-1 : ℝ) ^ k * a m ∧ b (q ^ k * m) = b m := by
    intro k
    induction k with
    | zero =>
      intro m _
      simp [b]
    | succ k ih =>
      intro m hm
      have hqm1 : 1 ≤ q ^ k * m := Nat.mul_pos (pow_pos hq.pos k) hm
      obtain ⟨ih_a0, _⟩ := ih hm
      have ha_step : a (q ^ (k + 1) * m) = (-1 : ℝ) ^ (k + 1) * a m := by
        calc
          a (q ^ (k + 1) * m) = a (q * (q ^ k * m)) := by rw [pow_succ', mul_assoc]
          _ = -a (q ^ k * m) := ha_neg _ hqm1
          _ = -((-1 : ℝ) ^ k * a m) := by rw [ih_a0]
          _ = (-1 : ℝ) ^ (k + 1) * a m := by rw [pow_succ]; ring
      have hm_ne : m ≠ 0 := by omega
      have hfq : (q ^ (k + 1) * m).factorization q = (k + 1) + m.factorization q := by
        rw [Nat.factorization_mul (pow_ne_zero (k + 1) hq.ne_zero) hm_ne,
          Finsupp.add_apply, Nat.Prime.factorization_pow hq, Finsupp.single_eq_same]
      have hb_step : b (q ^ (k + 1) * m) = b m := by
        dsimp [b]
        rw [ha_step, hfq, pow_add (-1 : ℝ) (k + 1) (m.factorization q)]
        have hs : (-1 : ℝ) ^ (k + 1) * (-1 : ℝ) ^ (k + 1) = 1 := by
          rw [← pow_add, show (k + 1) + (k + 1) = 2 * (k + 1) by omega,
            pow_mul, show (-1 : ℝ) ^ 2 = 1 by norm_num, one_pow]
        calc
          ((-1 : ℝ) ^ (k + 1) * a m) * ((-1 : ℝ) ^ (k + 1) * (-1 : ℝ) ^ (m.factorization q))
            = ((-1 : ℝ) ^ (k + 1) * (-1 : ℝ) ^ (k + 1)) * (a m * (-1 : ℝ) ^ (m.factorization q)) := by
                ring
          _ = a m * (-1 : ℝ) ^ (m.factorization q) := by rw [hs, one_mul]
      exact ⟨ha_step, hb_step⟩
  have h_alt_sum :
      ∀ v : ℕ,
        1 + 2 * (∑ k ∈ Finset.Icc 1 v, (-1 : ℝ) ^ k) = (-1 : ℝ) ^ v ∧
          (-1 : ℝ) ^ v + 2 * (∑ k ∈ Finset.Icc 1 v, (-1 : ℝ) ^ (v - k)) = 1 := by
    intro v
    have h1 : 1 + 2 * (∑ k ∈ Finset.Icc 1 v, (-1 : ℝ) ^ k) = (-1 : ℝ) ^ v := by
      induction v with
      | zero => simp
      | succ v ih =>
        have h_ins : Finset.Icc 1 (v + 1) = insert (v + 1) (Finset.Icc 1 v) := by
          ext k; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
        have h_not : v + 1 ∉ Finset.Icc 1 v := by simp
        rw [h_ins, Finset.sum_insert h_not, pow_succ]
        linarith [ih]
    refine ⟨h1, ?_⟩
    have h_mul := congr_arg (fun x => (-1 : ℝ) ^ v * x) h1
    dsimp only at h_mul
    have h_rv : (-1 : ℝ) ^ v * (-1 : ℝ) ^ v = 1 := by
      rw [← pow_add, show v + v = 2 * v by omega, pow_mul, show (-1 : ℝ) ^ 2 = 1 by norm_num, one_pow]
    have h_each_k :
        ∀ k ∈ Finset.Icc 1 v, (-1 : ℝ) ^ v * (-1 : ℝ) ^ k = (-1 : ℝ) ^ (v - k) := by
      intro k hk
      have hkv : k ≤ v := (Finset.mem_Icc.mp hk).2
      have hv_eq : v = (v - k) + k := (Nat.sub_add_cancel hkv).symm
      calc
        (-1 : ℝ) ^ v * (-1 : ℝ) ^ k
          = (-1 : ℝ) ^ ((v - k) + k) * (-1 : ℝ) ^ k := by rw [← hv_eq]
        _ = (-1 : ℝ) ^ (v - k) * ((-1 : ℝ) ^ k * (-1 : ℝ) ^ k) := by rw [pow_add, mul_assoc]
        _ = (-1 : ℝ) ^ (v - k) := by
            rw [← pow_add, show k + k = 2 * k by omega, pow_mul,
              show (-1 : ℝ) ^ 2 = 1 by norm_num, one_pow, mul_one]
    have h_lhs_eq :
        (-1 : ℝ) ^ v * (1 + 2 * ∑ k ∈ Finset.Icc 1 v, (-1 : ℝ) ^ k) =
          (-1 : ℝ) ^ v + 2 * ∑ k ∈ Finset.Icc 1 v, (-1 : ℝ) ^ (v - k) := by
      rw [mul_add, mul_one, ← mul_assoc, mul_comm ((-1 : ℝ) ^ v) 2, mul_assoc,
        Finset.mul_sum, Finset.sum_congr rfl h_each_k]
    rw [h_lhs_eq, h_rv] at h_mul
    exact h_mul
  have h_k_le_2k : ∀ k : ℕ, k ≤ 2 ^ k := by
    intro k
    induction k with
    | zero => norm_num
    | succ k ih => have hp : 1 ≤ 2 ^ k := Nat.one_le_pow k 2 (by decide); omega
  refine ⟨h_pow_k, ?_⟩
  intro n hn1
  have hn_ne : n ≠ 0 := by omega
  let v := n.factorization q
  have h_filt : (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n) = Finset.Icc 1 v := by
    ext k
    simp only [Finset.mem_filter, Finset.mem_Icc]
    constructor
    · rintro ⟨⟨hk1, _⟩, hdvd⟩
      exact ⟨hk1, (hq.pow_dvd_iff_le_factorization hn_ne).mp hdvd⟩
    · rintro ⟨hk1, hkv⟩
      have hdvd : q ^ k ∣ n := (hq.pow_dvd_iff_le_factorization hn_ne).mpr hkv
      have hqk_le : q ^ k ≤ n := Nat.le_of_dvd hn1 hdvd
      have hk_le : k ≤ q ^ k := le_trans (h_k_le_2k k) (Nat.pow_le_pow_left hq.two_le k)
      exact ⟨⟨hk1, le_trans hk_le hqk_le⟩, hdvd⟩
  have hqv_dvd : q ^ v ∣ n := (hq.pow_dvd_iff_le_factorization hn_ne).mpr (le_refl v)
  let r := n / q ^ v
  have hn_eq : q ^ v * r = n := Nat.mul_div_cancel' hqv_dvd
  have hr1 : 1 ≤ r := Nat.pos_of_ne_zero (fun hr0 => by rw [hr0, mul_zero] at hn_eq; omega)
  have hr_not_q : ¬ q ∣ r := by
    intro hqr
    have h1 : q ^ (v + 1) ∣ n := by
      rw [← hn_eq, pow_succ]
      exact Nat.mul_dvd_mul_left (q ^ v) hqr
    have hle : v + 1 ≤ v := (hq.pow_dvd_iff_le_factorization hn_ne).mp h1
    omega
  have hbr_eq : b r = a r := by
    dsimp [b]
    rw [Nat.factorization_eq_zero_of_not_dvd hr_not_q, pow_zero, mul_one]
  have han_eq : a n = (-1 : ℝ) ^ v * a r := by
    rw [← hn_eq, (h_pow_k v hr1).1]
  have hbn_eq : b n = a r := by
    rw [← hn_eq, (h_pow_k v hr1).2, hbr_eq]
  have h_quot_k :
      ∀ k ∈ Finset.Icc 1 v,
        n / q ^ k = q ^ (v - k) * r := by
    intro k hk
    have hkv : k ≤ v := (Finset.mem_Icc.mp hk).2
    have h_prod : q ^ k * (q ^ (v - k) * r) = n := by
      rw [← mul_assoc, ← pow_add, Nat.add_sub_of_le hkv, hn_eq]
    rw [← h_prod, Nat.mul_div_right _ (pow_pos hq.pos k)]
  have h_sum_a :
      (∑ k ∈ Finset.Icc 1 v, a (n / q ^ k)) =
        (∑ k ∈ Finset.Icc 1 v, (-1 : ℝ) ^ (v - k)) * a r := by
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro k hk
    rw [h_quot_k k hk, (h_pow_k (v - k) hr1).1]
  have h_sum_b :
      (∑ k ∈ Finset.Icc 1 v, (-1 : ℝ) ^ k * b (n / q ^ k)) =
        (∑ k ∈ Finset.Icc 1 v, (-1 : ℝ) ^ k) * a r := by
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro k hk
    rw [h_quot_k k hk, (h_pow_k (v - k) hr1).2, hbr_eq]
  obtain ⟨halt1, halt2⟩ := h_alt_sum v
  rw [h_filt]
  refine ⟨rfl, ?_, ?_⟩
  · rw [hbn_eq, han_eq, h_sum_a]
    calc
      a r = 1 * a r := (one_mul _).symm
      _ = ((-1 : ℝ) ^ v + 2 * ∑ k ∈ Finset.Icc 1 v, (-1 : ℝ) ^ (v - k)) * a r := by rw [halt2]
      _ = (-1 : ℝ) ^ v * a r + 2 * ((∑ k ∈ Finset.Icc 1 v, (-1 : ℝ) ^ (v - k)) * a r) := by ring
  · rw [han_eq, hbn_eq, h_sum_b]
    calc
      (-1 : ℝ) ^ v * a r
        = (1 + 2 * ∑ k ∈ Finset.Icc 1 v, (-1 : ℝ) ^ k) * a r := by rw [← halt1]
      _ = a r + 2 * ((∑ k ∈ Finset.Icc 1 v, (-1 : ℝ) ^ k) * a r) := by ring

private theorem liouville_prime_mul_neg_tc064_aux {q m : ℕ} (hq : Nat.Prime q) (hm1 : 1 ≤ m) :
    (liouvilleLambda (q * m) : ℝ) = -(liouvilleLambda m : ℝ) := by
  have hm_ne : m ≠ 0 := by omega
  have hqm_ne : q * m ≠ 0 := mul_ne_zero hq.ne_zero hm_ne
  have hom : natOmega (q * m) = 1 + natOmega m := by
    simp [natOmega, ArithmeticFunction.cardFactors_mul hq.ne_zero hm_ne,
      ArithmeticFunction.cardFactors_eq_one_iff_prime.mpr hq]
  have h_int : liouvilleLambda (q * m) = -liouvilleLambda m := by
    simp [liouvilleLambda, hm_ne, hqm_ne, hom, liouvilleSignFromOmega, pow_add]
  exact_mod_cast h_int

private theorem zeta_two_div_zeta_tendsto_zero_at_one_tc064_aux :
    Filter.Tendsto (fun w : ℂ => riemannZeta (2 * w) / riemannZeta w)
      (nhdsWithin (1 : ℂ) {(1 : ℂ)}ᶜ) (nhds (0 : ℂ)) := by
  let N_fn : ℂ → ℂ := fun w => (w - 1) * riemannZeta (2 * w)
  let D_fn : ℂ → ℂ := fun w => (w - 1) * riemannZeta w
  have h2_ne1 : (2 : ℂ) * (1 : ℂ) ≠ 1 := by norm_num
  have h_diff_z2 : DifferentiableAt ℂ (fun w : ℂ => riemannZeta (2 * w)) 1 :=
    (differentiableAt_riemannZeta h2_ne1).comp 1 (differentiableAt_id.const_mul 2)
  have hN_cont : ContinuousAt N_fn 1 :=
    (continuousAt_id.sub continuousAt_const).mul h_diff_z2.continuousAt
  have hN_one : N_fn 1 = 0 := by dsimp [N_fn]; simp
  have hN_tend : Filter.Tendsto N_fn (nhdsWithin 1 {1}ᶜ) (nhds 0) := by
    rw [← hN_one]
    exact tendsto_nhdsWithin_of_tendsto_nhds hN_cont.tendsto
  have hD_tend : Filter.Tendsto D_fn (nhdsWithin 1 {1}ᶜ) (nhds 1) :=
    riemannZeta_residue_one
  have h_quot : Filter.Tendsto (fun w => N_fn w / D_fn w) (nhdsWithin 1 {1}ᶜ) (nhds (0 / 1)) :=
    hN_tend.div hD_tend one_ne_zero
  rw [zero_div] at h_quot
  refine h_quot.congr' ?_
  filter_upwards [self_mem_nhdsWithin] with w hw
  have hw_sub : w - 1 ≠ 0 := sub_ne_zero.mpr (Set.mem_compl_singleton_iff.mp hw)
  dsimp [N_fn, D_fn]
  exact mul_div_mul_left (riemannZeta (2 * w)) (riemannZeta w) hw_sub

private theorem euler_multiplier_and_lseries_ratio_tc064_aux {q : ℕ} (hq : Nat.Prime q) :
    let f_lam : ℕ → ℂ := fun n => if n = 0 then 0 else (liouvilleLambda n : ℂ)
    let f_q : ℕ → ℂ := fun n => if n = 0 then 0 else (primeValuationToggleSeq q n : ℂ)
    let M_q : ℂ → ℂ := fun w => (1 + (q : ℂ) ^ (-w)) / (1 - (q : ℂ) ^ (-w))
    let M_inv : ℂ → ℂ := fun w => (1 - (q : ℂ) ^ (-w)) / (1 + (q : ℂ) ^ (-w))
    ((∀ (x y : ℝ), 0 < x →
        let z : ℂ := (x : ℂ) + (y : ℂ) * Complex.I
        1 - (q : ℂ) ^ (-z) ≠ 0 ∧ 1 + (q : ℂ) ^ (-z) ≠ 0 ∧ M_q z * M_inv z = 1) ∧
      DifferentiableOn ℂ M_q {w : ℂ | 0 < w.re} ∧
      DifferentiableOn ℂ M_inv {w : ℂ | 0 < w.re} ∧
      (∀ w ∈ {w : ℂ | 0 < w.re}, M_q w ≠ 0 ∧ M_inv w ≠ 0 ∧ M_q w * M_inv w = 1)) ∧
    (∀ (x y : ℝ), 1 < x →
      let z : ℂ := (x : ℂ) + (y : ℂ) * Complex.I
      LSeries f_q z = LSeries f_lam z * M_q z) ∧
    (((∃ F_lam : ℂ → ℂ,
          DifferentiableOn ℂ F_lam {w : ℂ | (1 / 2 : ℝ) < w.re} ∧
            ∀ x y : ℝ, 1 < x →
              F_lam ((x : ℂ) + (y : ℂ) * Complex.I) =
                LSeries f_lam ((x : ℂ) + (y : ℂ) * Complex.I)) ↔
        (∃ F_q : ℂ → ℂ,
          DifferentiableOn ℂ F_q {w : ℂ | (1 / 2 : ℝ) < w.re} ∧
            ∀ x y : ℝ, 1 < x →
              F_q ((x : ℂ) + (y : ℂ) * Complex.I) =
                LSeries f_q ((x : ℂ) + (y : ℂ) * Complex.I))) ∧
      ((∃ F_q : ℂ → ℂ,
          DifferentiableOn ℂ F_q {w : ℂ | (1 / 2 : ℝ) < w.re} ∧
            ∀ x y : ℝ, 1 < x →
              F_q ((x : ℂ) + (y : ℂ) * Complex.I) =
                LSeries f_q ((x : ℂ) + (y : ℂ) * Complex.I)) →
        ∀ (x y : ℝ), 0 < x → x < 1 →
          riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) = 0 → x = 1 / 2)) := by
  intro f_lam f_q M_q M_inv
  have hq_pos_r : (0 : ℝ) < (q : ℝ) := Nat.cast_pos.mpr hq.pos
  have hq_gt1_r : (1 : ℝ) < (q : ℝ) := by exact_mod_cast hq.one_lt
  have hq_ne_c : (q : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr hq.ne_zero
  have h_abs_lt1 : ∀ {w : ℂ}, 0 < w.re → Complex.abs ((q : ℂ) ^ (-w)) < 1 := by
    intro w hw
    have hq_cast : (q : ℂ) = ((q : ℝ) : ℂ) := (Complex.ofReal_natCast q).symm
    rw [hq_cast, Complex.abs_cpow_eq_rpow_re_of_pos hq_pos_r (-w), Complex.neg_re]
    have h_lt := Real.rpow_lt_rpow_of_exponent_lt hq_gt1_r (neg_lt_zero.mpr hw)
    rwa [Real.rpow_zero] at h_lt
  have h_denom_ne :
      ∀ {w : ℂ}, 0 < w.re →
        1 - (q : ℂ) ^ (-w) ≠ 0 ∧ 1 + (q : ℂ) ^ (-w) ≠ 0 ∧ M_q w * M_inv w = 1 := by
    intro w hw
    have habs := h_abs_lt1 hw
    have h_sub_ne : 1 - (q : ℂ) ^ (-w) ≠ 0 := by
      intro h0
      have heq : (q : ℂ) ^ (-w) = 1 := (sub_eq_zero.mp h0).symm
      rw [heq, map_one] at habs
      exact lt_irrefl 1 habs
    have h_add_ne : 1 + (q : ℂ) ^ (-w) ≠ 0 := by
      intro h0
      have heq : (q : ℂ) ^ (-w) = -1 := eq_neg_of_add_eq_zero_right h0
      rw [heq, map_neg_eq_map, map_one] at habs
      exact lt_irrefl 1 habs
    refine ⟨h_sub_ne, h_add_ne, ?_⟩
    dsimp [M_q, M_inv]
    field_simp [h_sub_ne, h_add_ne]
  have h_diff_M :
      ∀ {w : ℂ}, 0 < w.re → DifferentiableAt ℂ M_q w ∧ DifferentiableAt ℂ M_inv w := by
    intro w hw
    obtain ⟨h_sub_ne, h_add_ne, _⟩ := h_denom_ne hw
    have hd_cpow : DifferentiableAt ℂ (fun u : ℂ => (q : ℂ) ^ (-u)) w :=
      DifferentiableAt.const_cpow differentiableAt_id.neg (Or.inl hq_ne_c)
    exact ⟨((differentiableAt_const 1).add hd_cpow).div
        ((differentiableAt_const 1).sub hd_cpow) h_sub_ne,
      ((differentiableAt_const 1).sub hd_cpow).div
        ((differentiableAt_const 1).add hd_cpow) h_add_ne⟩
  have h_part1 :
      (∀ (x y : ℝ), 0 < x →
          let z : ℂ := (x : ℂ) + (y : ℂ) * Complex.I
          1 - (q : ℂ) ^ (-z) ≠ 0 ∧ 1 + (q : ℂ) ^ (-z) ≠ 0 ∧ M_q z * M_inv z = 1) ∧
        DifferentiableOn ℂ M_q {w : ℂ | 0 < w.re} ∧
        DifferentiableOn ℂ M_inv {w : ℂ | 0 < w.re} ∧
        (∀ w ∈ {w : ℂ | 0 < w.re}, M_q w ≠ 0 ∧ M_inv w ≠ 0 ∧ M_q w * M_inv w = 1) := by
    refine ⟨?_, ?_, ?_, ?_⟩
    · intro x y hx
      have hz_re : 0 < ((x : ℂ) + (y : ℂ) * Complex.I).re := by
        simp [Complex.add_re, Complex.mul_re, hx]
      exact h_denom_ne hz_re
    · intro w hw; exact (h_diff_M hw).1.differentiableWithinAt
    · intro w hw; exact (h_diff_M hw).2.differentiableWithinAt
    · intro w hw
      obtain ⟨hs, ha, hm⟩ := h_denom_ne hw
      exact ⟨div_ne_zero ha hs, div_ne_zero hs ha, hm⟩
  have h_ratio_gt1 :
      ∀ (x y : ℝ), 1 < x →
        let z : ℂ := (x : ℂ) + (y : ℂ) * Complex.I
        LSeries f_q z = LSeries f_lam z * M_q z := by
    intro x y hx z
    have hz_re : 1 < z.re := by
      dsimp [z]; simp [Complex.add_re, Complex.mul_re]; exact hx
    have hz_pos : 0 < z.re := by linarith
    let c_q : ℕ → ℂ := fun m =>
      if m = 1 then 1 else if ∃ k : ℕ, 1 ≤ k ∧ m = q ^ k then 2 else 0
    have hf_bdd : ∀ n : ℕ, n ≠ 0 → Complex.abs (f_lam n) ≤ 1 := by
      intro n hn
      dsimp [f_lam]; rw [if_neg hn]
      simp only [liouvilleLambda, hn, ↓reduceIte, liouvilleSignFromOmega]
      push_cast; simp
    have hc_bdd : ∀ m : ℕ, m ≠ 0 → Complex.abs (c_q m) ≤ 2 := by
      intro m _
      dsimp [c_q]
      split_ifs <;> norm_num
    have hf_sum : LSeriesSummable f_lam z :=
      LSeriesSummable_of_bounded_of_one_lt_re hf_bdd hz_re
    have hc_sum : LSeriesSummable c_q z :=
      LSeriesSummable_of_bounded_of_one_lt_re hc_bdd hz_re
    have h_conv_eq : ∀ n : ℕ, n ≠ 0 → LSeries.convolution f_lam c_q n = f_q n := by
      intro n hn
      have hn1 : 1 ≤ n := Nat.pos_of_ne_zero hn
      rw [LSeries.convolution_def]
      dsimp only
      rw [Nat.sum_divisorsAntidiagonal' (fun d e => f_lam d * c_q e)]
      have h1_div : 1 ∈ n.divisors := Nat.one_mem_divisors.mpr hn
      rw [← Finset.add_sum_erase _ _ h1_div]
      have h_e1 : f_lam (n / 1) * c_q 1 = (liouvilleLambda n : ℂ) := by
        rw [Nat.div_one]; dsimp [f_lam, c_q]; rw [if_neg hn, if_pos rfl, mul_one]
      rw [h_e1]
      have h_er_eq :
          (∑ e ∈ n.divisors.erase 1, f_lam (n / e) * c_q e) =
            2 * ∑ k ∈ (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n),
              (liouvilleLambda (n / q ^ k) : ℂ) := by
        have h_ite :
            (∑ e ∈ n.divisors.erase 1, f_lam (n / e) * c_q e) =
              ∑ e ∈ (n.divisors.erase 1).filter (fun e => ∃ k : ℕ, 1 ≤ k ∧ e = q ^ k),
                2 * (liouvilleLambda (n / e) : ℂ) := by
          rw [Finset.sum_filter]
          apply Finset.sum_congr rfl
          intro e he
          obtain ⟨he_ne1, he_div⟩ := Finset.mem_erase.mp he
          have he_dvd : e ∣ n := (Nat.mem_divisors.mp he_div).1
          have hq_ne0 : n / e ≠ 0 := by
            intro h0
            have hp := Nat.mul_div_cancel' he_dvd
            rw [h0, mul_zero] at hp; exact hn hp.symm
          dsimp [f_lam, c_q]
          rw [if_neg hq_ne0, if_neg he_ne1]
          by_cases hex : ∃ k : ℕ, 1 ≤ k ∧ e = q ^ k
          · rw [if_pos hex, if_pos hex]; ring
          · rw [if_neg hex, if_neg hex, mul_zero]
        rw [h_ite, Finset.mul_sum]
        symm
        apply Finset.sum_bij (fun k _ => q ^ k)
        · intro k hk
          obtain ⟨hk_Icc, hk_dvd⟩ := Finset.mem_filter.mp hk
          have hk1 : 1 ≤ k := (Finset.mem_Icc.mp hk_Icc).1
          have hqk_gt1 : 1 < q ^ k :=
            lt_of_lt_of_le hq.one_lt (by simpa [pow_one] using Nat.pow_le_pow_right hq.pos hk1)
          simp only [Finset.mem_filter, Finset.mem_erase, Nat.mem_divisors]
          exact ⟨⟨ne_of_gt hqk_gt1, hk_dvd, hn⟩, ⟨k, hk1, rfl⟩⟩
        · intro k1 _ k2 _ h_eq
          exact Nat.pow_right_injective hq.two_le h_eq
        · intro e he
          obtain ⟨he_er, ⟨k, hk1, rfl⟩⟩ := Finset.mem_filter.mp he
          have hk_dvd : q ^ k ∣ n := (Nat.mem_divisors.mp (Finset.mem_of_mem_erase he_er)).1
          have hqk_le : q ^ k ≤ n := Nat.le_of_dvd hn1 hk_dvd
          have hk_le_2k : k ≤ 2 ^ k := by
            clear * -; induction k with
            | zero => norm_num
            | succ k ih => have hp : 1 ≤ 2 ^ k := Nat.one_le_pow k 2 (by decide); omega
          have hk_le_n : k ≤ n :=
            le_trans (le_trans hk_le_2k (Nat.pow_le_pow_left hq.two_le k)) hqk_le
          exact ⟨k, Finset.mem_filter.mpr ⟨Finset.mem_Icc.mpr ⟨hk1, hk_le_n⟩, hk_dvd⟩, rfl⟩
        · intros; rfl
      rw [h_er_eq]
      have h_id_r :=
        ((toggle_pair_coeff_identities_tc064_aux (a := fun m => (liouvilleLambda m : ℝ)) hq
          (fun _ hm => liouville_prime_mul_neg_tc064_aux hq hm)).2 hn1).2.1
      have h_eq_b :
          (primeValuationToggleSeq q n : ℝ) =
            (liouvilleLambda n : ℝ) +
              2 * ∑ k ∈ (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n),
                (liouvilleLambda (n / q ^ k) : ℝ) := by
        unfold primeValuationToggleSeq
        push_cast
        exact h_id_r
      have h_eq_c :
          ((primeValuationToggleSeq q n : ℝ) : ℂ) =
            (liouvilleLambda n : ℂ) +
              2 * ∑ k ∈ (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n),
                (liouvilleLambda (n / q ^ k) : ℂ) := by
        exact_mod_cast h_eq_b
      dsimp [f_q]
      rw [if_neg hn, ← h_eq_c]
      simp
    have h_term_eq : LSeries.term (LSeries.convolution f_lam c_q) z = LSeries.term f_q z := by
      ext n
      by_cases hn : n = 0
      · subst hn; simp [LSeries.term]
      · simp [LSeries.term, hn, h_conv_eq n hn]
    have h_L_conv : LSeries f_q z = LSeries f_lam z * LSeries c_q z := by
      rw [← LSeries_convolution' hf_sum hc_sum]
      unfold LSeries
      rw [h_term_eq]
    rw [h_L_conv]
    congr 1
    -- Evaluate LSeries c_q z = M_q z:
    let u : ℂ := (q : ℂ) ^ (-z)
    have hu_norm : ‖u‖ < 1 := h_abs_lt1 hz_pos
    let pow_map : ℕ → ℕ := fun k => q ^ k
    have h_pow_inj : Function.Injective pow_map := Nat.pow_right_injective hq.two_le
    have h_supp : Function.support (LSeries.term c_q z) ⊆ Set.range pow_map := by
      intro m hm_s
      rw [Function.mem_support] at hm_s
      by_contra hm_not
      apply hm_s
      by_cases hm0 : m = 0
      · subst hm0; simp [LSeries.term]
      · by_cases hm1 : m = 1
        · subst hm1; exact False.elim (hm_not ⟨0, rfl⟩)
        · have h_not_ex : ¬ ∃ k : ℕ, 1 ≤ k ∧ m = q ^ k := by
            rintro ⟨k, _, rfl⟩; exact hm_not ⟨k, rfl⟩
          simp [LSeries.term, c_q, hm0, hm1, h_not_ex]
    unfold LSeries
    rw [← h_pow_inj.tsum_eq h_supp]
    have h_cpow_inv : ∀ k : ℕ, (((q ^ k : ℕ) : ℂ) ^ z)⁻¹ = u ^ k := by
      intro k
      have hqk_pos_r : (0 : ℝ) < ((q ^ k : ℕ) : ℝ) := Nat.cast_pos.mpr (pow_pos hq.pos k)
      have hqk_ne_c : ((q ^ k : ℕ) : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr (pow_ne_zero k hq.ne_zero)
      have hlog_q : Complex.log (q : ℂ) = ((Real.log (q : ℝ) : ℝ) : ℂ) := by
        rw [← Complex.ofReal_natCast, ← Complex.ofReal_log (le_of_lt hq_pos_r)]
      have hlog_qk : Complex.log ((q ^ k : ℕ) : ℂ) = (k : ℂ) * Complex.log (q : ℂ) := by
        rw [← Complex.ofReal_natCast, ← Complex.ofReal_log (le_of_lt hqk_pos_r),
          Nat.cast_pow, Real.log_pow, Complex.ofReal_mul, Complex.ofReal_natCast, hlog_q]
      have h1 : ((q ^ k : ℕ) : ℂ) ^ z = Complex.exp ((k : ℂ) * (Complex.log (q : ℂ) * z)) := by
        rw [Complex.cpow_def_of_ne_zero hqk_ne_c, hlog_qk, mul_assoc]
      have h2 : u ^ k = Complex.exp (-(k : ℂ) * (Complex.log (q : ℂ) * z)) := by
        dsimp [u]
        rw [Complex.cpow_def_of_ne_zero hq_ne_c, ← Complex.exp_nat_mul]
        congr 1; ring
      have h_prod : ((q ^ k : ℕ) : ℂ) ^ z * u ^ k = 1 := by
        rw [h1, h2, ← Complex.exp_add]
        have h_add0 :
            (k : ℂ) * (Complex.log (q : ℂ) * z) + -(k : ℂ) * (Complex.log (q : ℂ) * z) = 0 := by
          ring
        rw [h_add0, Complex.exp_zero]
      exact inv_eq_of_mul_eq_one_right h_prod
    have h_t0 : LSeries.term c_q z (pow_map 0) = 1 := by
      dsimp [pow_map, LSeries.term, c_q]; simp
    have h_tk : ∀ k : ℕ, LSeries.term c_q z (pow_map (k + 1)) = 2 * u ^ (k + 1) := by
      intro k
      have h_ne0 : q ^ (k + 1) ≠ 0 := pow_ne_zero (k + 1) hq.ne_zero
      have h_gt1 : 1 < q ^ (k + 1) :=
        lt_of_lt_of_le hq.one_lt
          (by simpa [pow_one] using Nat.pow_le_pow_right hq.pos (show 1 ≤ k + 1 by omega))
      have h_ne1 : q ^ (k + 1) ≠ 1 := ne_of_gt h_gt1
      have h_ex : ∃ j : ℕ, 1 ≤ j ∧ q ^ (k + 1) = q ^ j := ⟨k + 1, by omega, rfl⟩
      dsimp [pow_map, LSeries.term, c_q]
      rw [if_neg h_ne0, if_neg h_ne1, if_pos h_ex, div_eq_mul_inv, h_cpow_inv (k + 1)]
    have h_u_sum : Summable (fun k : ℕ => u ^ k) := summable_geometric_of_norm_lt_one hu_norm
    have h_2u_sum : Summable (fun k : ℕ => 2 * u ^ k) := h_u_sum.mul_left 2
    have h_c_sum : Summable (fun k : ℕ => LSeries.term c_q z (pow_map k)) := by
      rw [← summable_nat_add_iff 1]
      exact (h_u_sum.mul_left (2 * u)).congr (fun k => by
        rw [h_tk k, pow_succ']; ring)
    have hs_c := sum_add_tsum_nat_add 1 h_c_sum
    have hs_2u := sum_add_tsum_nat_add 1 h_2u_sum
    simp only [Finset.sum_range_one, pow_zero, mul_one, h_t0] at hs_c hs_2u
    have h_tail_eq :
        (∑' i : ℕ, LSeries.term c_q z (pow_map (i + 1))) = ∑' i : ℕ, 2 * u ^ (i + 1) :=
      tsum_congr h_tk
    rw [h_tail_eq] at hs_c
    have h_tsum_2u : (∑' k : ℕ, 2 * u ^ k) = 2 * (1 - u)⁻¹ := by
      rw [tsum_mul_left, tsum_geometric_of_norm_lt_one hu_norm]
    have h_sub_u_ne : 1 - u ≠ 0 := (h_denom_ne hz_pos).1
    have h_alg_u : 1 + ((2 : ℂ) * (1 - u)⁻¹ - 2) = (1 + u) / (1 - u) := by
      field_simp [h_sub_u_ne]; ring
    dsimp [M_q]
    change ∑' k : ℕ, LSeries.term c_q z (pow_map k) = (1 + u) / (1 - u)
    rw [← hs_c, show (∑' i : ℕ, 2 * u ^ (i + 1)) = (∑' k : ℕ, 2 * u ^ k) - 2 by
      rw [← hs_2u]; ring, h_tsum_2u, h_alg_u]
  refine ⟨h_part1, h_ratio_gt1, ?_, ?_⟩
  · have h_sub_dom : {w : ℂ | (1 / 2 : ℝ) < w.re} ⊆ {w : ℂ | 0 < w.re} :=
      fun _ hw => lt_trans (by norm_num : (0 : ℝ) < 1 / 2) hw
    constructor
    · rintro ⟨F_lam, hF_diff, hF_gt1⟩
      refine ⟨fun w => F_lam w * M_q w,
        hF_diff.mul (h_part1.2.1.mono h_sub_dom), ?_⟩
      intro x y hx
      dsimp only
      rw [hF_gt1 x y hx, h_ratio_gt1 x y hx]
    · rintro ⟨F_q, hF_diff, hF_gt1⟩
      refine ⟨fun w => F_q w * M_inv w,
        hF_diff.mul (h_part1.2.2.1.mono h_sub_dom), ?_⟩
      intro x y hx
      let z : ℂ := (x : ℂ) + (y : ℂ) * Complex.I
      have hm1 := (h_part1.1 x y (by linarith)).2.2
      change F_q z * M_inv z = LSeries f_lam z
      rw [hF_gt1 x y hx, h_ratio_gt1 x y hx, mul_assoc, hm1, mul_one]
  · rintro ⟨F_q, hF_diff, hF_gt1⟩
    have h_sub_dom : {w : ℂ | (1 / 2 : ℝ) < w.re} ⊆ {w : ℂ | 0 < w.re} :=
      fun _ hw => lt_trans (by norm_num : (0 : ℝ) < 1 / 2) hw
    let F_lam : ℂ → ℂ := fun w => F_q w * M_inv w
    have hFlam_diff : DifferentiableOn ℂ F_lam {w : ℂ | (1 / 2 : ℝ) < w.re} :=
      hF_diff.mul (h_part1.2.2.1.mono h_sub_dom)
    have hFlam_gt1 :
        ∀ (x y : ℝ), 1 < x →
          F_lam ((x : ℂ) + (y : ℂ) * Complex.I) =
            riemannZeta (2 * ((x : ℂ) + (y : ℂ) * Complex.I)) /
              riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) := by
      intro x y hx
      let z : ℂ := (x : ℂ) + (y : ℂ) * Complex.I
      have hm1 := (h_part1.1 x y (by linarith)).2.2
      obtain ⟨hz_ne, _, hL_zeta⟩ :=
        (liouville_dirichlet_ratio_pole_contradiction_and_reflection_tc063).1 x y hx
      change F_q z * M_inv z = riemannZeta (2 * z) / riemannZeta z
      rw [hF_gt1 x y hx, h_ratio_gt1 x y hx, mul_assoc, hm1, mul_one, ← hL_zeta,
        mul_div_cancel_right₀ _ hz_ne]
    exact ((liouville_dirichlet_ratio_pole_contradiction_and_reflection_tc063).2.2.2.2
      F_lam hFlam_diff hFlam_gt1).2

private theorem gaussianTermPhi_dilation_and_infiniteQ_bounds_tc064_aux :
    (∀ {q : ℕ}, 1 ≤ q → ∀ {X : ℝ}, 0 < X → ∀ {k r : ℕ}, 1 ≤ r →
      gaussianTermPhi (q ^ k * r) X =
        (q : ℝ) ^ (-(k : ℝ) / 2) * gaussianTermPhi r (X / (q : ℝ) ^ k)) ∧
    (∀ {a : ℕ → ℝ}, (∀ n : ℕ, 1 ≤ n → |a n| ≤ 1) →
      (∀ {X : ℝ}, 0 < X →
        Summable (fun n : ℕ => if n = 0 then 0 else a n * gaussianTermPhi n X) ∧
          |infiniteSeqGaussianObservableQ a X| ≤ 2 * X ^ (5 / 2 : ℝ)) ∧
      (∀ {Y : ℝ}, 0 < Y →
        ContinuousOn (infiniteSeqGaussianObservableQ a) (Set.uIcc Y (RiemannScope.tau * Y))) ∧
      (∀ {Y : ℝ}, 1 ≤ Y →
        Real.sqrt
            (windowEnergyNormSq Y
              (fun X =>
                infiniteSeqGaussianObservableQ a X -
                  truncatedSeqGaussianObservableQ a (canonicalCutoffT Y) X)) ≤
          (1 / 2 : ℝ) * RiemannScope.tau ^ (5 / 2 : ℝ) *
            Real.sqrt (Real.log RiemannScope.tau))) := by
  -- Auxiliary 1 / n^3 telescoping tail and summability:
  have h_cube_tail :
      (∀ {M : ℕ}, 1 ≤ M → ∀ (m : ℕ),
        (∑ j ∈ Finset.range m, (1 : ℝ) / ((M + 1 + j : ℕ) : ℝ) ^ 3) ≤
          (1 / 2 : ℝ) * (1 / (M : ℝ) ^ 2 - 1 / ((M + m : ℕ) : ℝ) ^ 2)) ∧
      Summable (fun n : ℕ => if n = 0 then (0 : ℝ) else (1 : ℝ) / (n : ℝ) ^ 3) ∧
      (∑' n : ℕ, (if n = 0 then (0 : ℝ) else (1 : ℝ) / (n : ℝ) ^ 3)) ≤ 2 ∧
      (∀ {M : ℕ}, 1 ≤ M →
        Summable (fun j : ℕ => (1 : ℝ) / ((M + 1 + j : ℕ) : ℝ) ^ 3) ∧
          (∑' j : ℕ, (1 : ℝ) / ((M + 1 + j : ℕ) : ℝ) ^ 3) ≤ 1 / (2 * (M : ℝ) ^ 2)) := by
    have h_step :
        ∀ {x : ℝ}, 0 < x →
          (1 : ℝ) / (x + 1) ^ 3 ≤ (1 / 2 : ℝ) * (1 / x ^ 2 - 1 / (x + 1) ^ 2) := by
      intro x hx
      have hx1 : 0 < x + 1 := by linarith
      have hd :
          (1 / 2 : ℝ) * (1 / x ^ 2 - 1 / (x + 1) ^ 2) - (1 : ℝ) / (x + 1) ^ 3 =
            (3 * x + 1) / (2 * x ^ 2 * (x + 1) ^ 3) := by
        field_simp [ne_of_gt hx, ne_of_gt hx1]; ring
      have hnn : 0 ≤ (3 * x + 1) / (2 * x ^ 2 * (x + 1) ^ 3) := by positivity
      linarith
    have h_fin :
        ∀ {M : ℕ}, 1 ≤ M → ∀ (m : ℕ),
          (∑ j ∈ Finset.range m, (1 : ℝ) / ((M + 1 + j : ℕ) : ℝ) ^ 3) ≤
            (1 / 2 : ℝ) * (1 / (M : ℝ) ^ 2 - 1 / ((M + m : ℕ) : ℝ) ^ 2) := by
      intro M hM m
      induction m with
      | zero => simp
      | succ m ih =>
        rw [Finset.sum_range_succ]
        let x : ℝ := ((M + m : ℕ) : ℝ)
        have hx : 0 < x := by dsimp [x]; exact_mod_cast (by omega : 0 < M + m)
        have hs := h_step hx
        have c1 : ((M + 1 + m : ℕ) : ℝ) = x + 1 := by dsimp [x]; push_cast; ring
        have c2 : ((M + (m + 1) : ℕ) : ℝ) = x + 1 := by dsimp [x]; push_cast; ring
        rw [c1, c2]; linarith
    have h_M_sum :
        ∀ {M : ℕ}, 1 ≤ M →
          Summable (fun j : ℕ => (1 : ℝ) / ((M + 1 + j : ℕ) : ℝ) ^ 3) ∧
            (∑' j : ℕ, (1 : ℝ) / ((M + 1 + j : ℕ) : ℝ) ^ 3) ≤ 1 / (2 * (M : ℝ) ^ 2) := by
      intro M hM
      have h_ub :
          ∀ m : ℕ,
            (∑ j ∈ Finset.range m, (1 : ℝ) / ((M + 1 + j : ℕ) : ℝ) ^ 3) ≤
              1 / (2 * (M : ℝ) ^ 2) := by
        intro m
        have hf := h_fin hM m
        have h_nn : 0 ≤ (1 / 2 : ℝ) * (1 / ((M + m : ℕ) : ℝ) ^ 2) := by positivity
        have heq : (1 / 2 : ℝ) * (1 / (M : ℝ) ^ 2) = 1 / (2 * (M : ℝ) ^ 2) := by ring
        linarith
      have h_s : Summable (fun j : ℕ => (1 : ℝ) / ((M + 1 + j : ℕ) : ℝ) ^ 3) :=
        summable_of_sum_range_le (fun _ => by positivity) h_ub
      exact ⟨h_s, tsum_le_of_sum_range_le h_s h_ub⟩
    have h_all_ub :
        ∀ N : ℕ,
          (∑ n ∈ Finset.range N, (if n = 0 then (0 : ℝ) else (1 : ℝ) / (n : ℝ) ^ 3)) ≤ 2 := by
      intro N
      rcases N with _ | _ | m
      · simp
      · simp
      · rw [Finset.sum_range_succ' _ (m + 1), Finset.sum_range_succ' _ m]
        simp only [↓reduceIte, zero_add, Nat.succ_ne_zero, Nat.cast_one, one_pow, div_one]
        have h_eq :
            (∑ j ∈ Finset.range m, (1 : ℝ) / ((j + 1 + 1 : ℕ) : ℝ) ^ 3) =
              ∑ j ∈ Finset.range m, (1 : ℝ) / ((1 + 1 + j : ℕ) : ℝ) ^ 3 := by
          apply Finset.sum_congr rfl; intro j _; congr 2; exact_mod_cast (by omega : j + 1 + 1 = 1 + 1 + j)
        rw [h_eq]
        have hf := h_fin (le_refl 1) m
        have h_nn : 0 ≤ (1 / 2 : ℝ) * (1 / ((1 + m : ℕ) : ℝ) ^ 2) := by positivity
        have hf_id :
            (1 / 2 : ℝ) * (1 / ((1 : ℕ) : ℝ) ^ 2 - 1 / ((1 + m : ℕ) : ℝ) ^ 2) +
                (1 / 2 : ℝ) * (1 / ((1 + m : ℕ) : ℝ) ^ 2) = 1 / 2 := by
          push_cast; ring
        linarith [hf, h_nn, hf_id]
    have h_s_all : Summable (fun n : ℕ => if n = 0 then (0 : ℝ) else (1 : ℝ) / (n : ℝ) ^ 3) :=
      summable_of_sum_range_le (fun n => by split_ifs <;> positivity) h_all_ub
    exact ⟨h_fin, h_s_all, tsum_le_of_sum_range_le h_s_all h_all_ub, h_M_sum⟩
  refine ⟨?_, ?_⟩
  -- Part 1: Station dilation
  · intro q hq1 X hX0 k r hr1
    have hq_pos : (0 : ℝ) < (q : ℝ) := Nat.cast_pos.mpr hq1
    have hr_pos : (0 : ℝ) < (r : ℝ) := Nat.cast_pos.mpr hr1
    let c : ℝ := (q : ℝ) ^ k
    have hc_pos : 0 < c := pow_pos hq_pos k
    have hc_rpow : c = (q : ℝ) ^ (k : ℝ) := (Real.rpow_natCast (q : ℝ) k).symm
    have h_div_52 : (X / c) ^ (5 / 2 : ℝ) = X ^ (5 / 2 : ℝ) / c ^ (5 / 2 : ℝ) :=
      Real.div_rpow (le_of_lt hX0) (le_of_lt hc_pos) (5 / 2 : ℝ)
    have hc_52 : c ^ (5 / 2 : ℝ) = (q : ℝ) ^ ((5 / 2 : ℝ) * (k : ℝ)) := by
      rw [hc_rpow, ← Real.rpow_mul (le_of_lt hq_pos), mul_comm]
    have hq_prod :
        (q : ℝ) ^ (-(k : ℝ) / 2) / c ^ (5 / 2 : ℝ) = (c ^ 3)⁻¹ := by
      rw [hc_52, div_eq_mul_inv, ← Real.rpow_neg (le_of_lt hq_pos),
        ← Real.rpow_add hq_pos]
      have he : -(k : ℝ) / 2 + -((5 / 2 : ℝ) * (k : ℝ)) = -(((3 : ℕ) : ℝ) * (k : ℝ)) := by
        push_cast; ring
      rw [he, Real.rpow_neg (le_of_lt hq_pos), mul_comm ((3 : ℕ) : ℝ),
        Real.rpow_mul (le_of_lt hq_pos), ← hc_rpow, Real.rpow_natCast]
    have h_exp_eq :
        -((X / c) ^ 2) / (r : ℝ) ^ 2 = -(X ^ 2) / ((q ^ k * r : ℕ) : ℝ) ^ 2 := by
      dsimp [c]; push_cast
      field_simp [ne_of_gt hc_pos, ne_of_gt hr_pos]; ring
    unfold gaussianTermPhi
    have h_inv_qkr :
        (((q ^ k * r : ℕ) : ℝ) ^ 3)⁻¹ = (c ^ 3)⁻¹ * ((r : ℝ) ^ 3)⁻¹ := by
      dsimp [c]; push_cast; rw [mul_pow, mul_inv]
    rw [h_div_52, h_exp_eq, h_inv_qkr]
    calc
      X ^ (5 / 2 : ℝ) * ((c ^ 3)⁻¹ * ((r : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / ((q ^ k * r : ℕ) : ℝ) ^ 2))
        = ((c ^ 3)⁻¹) * X ^ (5 / 2 : ℝ) * (((r : ℝ) ^ 3)⁻¹ *
            Real.exp (-(X ^ 2) / ((q ^ k * r : ℕ) : ℝ) ^ 2)) := by ring
      _ = ((q : ℝ) ^ (-(k : ℝ) / 2) / c ^ (5 / 2 : ℝ)) * X ^ (5 / 2 : ℝ) *
            (((r : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / ((q ^ k * r : ℕ) : ℝ) ^ 2)) := by
          rw [← hq_prod]
      _ = (q : ℝ) ^ (-(k : ℝ) / 2) *
            (X ^ (5 / 2 : ℝ) / c ^ (5 / 2 : ℝ) *
              (((r : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / ((q ^ k * r : ℕ) : ℝ) ^ 2))) := by ring
  -- Part 2: Summability, small-X bound, continuity, and canonical tail window norm bound
  · intro a ha_abs
    obtain ⟨_, h_s3, h_t3_le2, h_M_tail⟩ := h_cube_tail
    have hCg := (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2.1
    have htau_gt1 : (1 : ℝ) < RiemannScope.tau := by linarith
    have h_phi_le :
        ∀ {X : ℝ}, 0 < X → ∀ {n : ℕ}, 1 ≤ n →
          0 ≤ gaussianTermPhi n X ∧ gaussianTermPhi n X ≤ X ^ (5 / 2 : ℝ) * ((1 : ℝ) / (n : ℝ) ^ 3) := by
      intro X hX0 n _
      unfold gaussianTermPhi
      refine ⟨by positivity, ?_⟩
      have hexp : Real.exp (-(X ^ 2) / (n : ℝ) ^ 2) ≤ 1 := by
        rw [Real.exp_le_one_iff]
        exact div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg X)) (sq_nonneg _)
      calc
        X ^ (5 / 2 : ℝ) * (((n : ℝ) ^ 3)⁻¹ * Real.exp (-(X ^ 2) / (n : ℝ) ^ 2))
          ≤ X ^ (5 / 2 : ℝ) * (((n : ℝ) ^ 3)⁻¹ * 1) :=
            mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left hexp (by positivity))
              (by positivity)
        _ = X ^ (5 / 2 : ℝ) * ((1 : ℝ) / (n : ℝ) ^ 3) := by ring
    have h_sum_and_small :
        ∀ {X : ℝ}, 0 < X →
          Summable (fun n : ℕ => if n = 0 then 0 else a n * gaussianTermPhi n X) ∧
            |infiniteSeqGaussianObservableQ a X| ≤ 2 * X ^ (5 / 2 : ℝ) := by
      intro X hX0
      let u_maj : ℕ → ℝ := fun n =>
        X ^ (5 / 2 : ℝ) * (if n = 0 then 0 else (1 : ℝ) / (n : ℝ) ^ 3)
      have hu_sum : Summable u_maj := h_s3.mul_left (X ^ (5 / 2 : ℝ))
      have h_norm_le :
          ∀ n : ℕ, ‖if n = 0 then (0 : ℝ) else a n * gaussianTermPhi n X‖ ≤ u_maj n := by
        intro n
        dsimp [u_maj]
        by_cases hn0 : n = 0
        · subst hn0; simp
        · rw [if_neg hn0, if_neg hn0, abs_mul]
          have hn1 : 1 ≤ n := Nat.pos_of_ne_zero hn0
          obtain ⟨h_nn, h_ub⟩ := h_phi_le hX0 hn1
          rw [abs_of_nonneg h_nn]
          calc
            |a n| * gaussianTermPhi n X
              ≤ 1 * (X ^ (5 / 2 : ℝ) * ((1 : ℝ) / (n : ℝ) ^ 3)) :=
                mul_le_mul (ha_abs n hn1) h_ub h_nn zero_le_one
            _ = X ^ (5 / 2 : ℝ) * ((1 : ℝ) / (n : ℝ) ^ 3) := one_mul _
      have hf_sum : Summable (fun n : ℕ => if n = 0 then 0 else a n * gaussianTermPhi n X) :=
        Summable.of_norm_bounded u_maj hu_sum h_norm_le
      have hf_norm_sum :
          Summable (fun n : ℕ => ‖if n = 0 then 0 else a n * gaussianTermPhi n X‖) :=
        hf_sum.norm
      refine ⟨hf_sum, ?_⟩
      unfold infiniteSeqGaussianObservableQ
      rw [← Real.norm_eq_abs]
      calc
        ‖∑' n : ℕ, if n = 0 then 0 else a n * gaussianTermPhi n X‖
          ≤ ∑' n : ℕ, ‖if n = 0 then 0 else a n * gaussianTermPhi n X‖ :=
            norm_tsum_le_tsum_norm hf_norm_sum
        _ ≤ ∑' n : ℕ, u_maj n := tsum_le_tsum h_norm_le hf_norm_sum hu_sum
        _ = X ^ (5 / 2 : ℝ) * ∑' n : ℕ, (if n = 0 then (0 : ℝ) else (1 : ℝ) / (n : ℝ) ^ 3) :=
            tsum_mul_left
        _ ≤ X ^ (5 / 2 : ℝ) * 2 := mul_le_mul_of_nonneg_left h_t3_le2 (by positivity)
        _ = 2 * X ^ (5 / 2 : ℝ) := by ring
    have h_cont_win :
        ∀ {Y : ℝ}, 0 < Y →
          ContinuousOn (infiniteSeqGaussianObservableQ a) (Set.uIcc Y (RiemannScope.tau * Y)) := by
      intro Y hY0
      have hle : Y ≤ RiemannScope.tau * Y := by nlinarith
      let u_win : ℕ → ℝ := fun n =>
        (RiemannScope.tau * Y) ^ (5 / 2 : ℝ) *
          (if n = 0 then 0 else (1 : ℝ) / (n : ℝ) ^ 3)
      have hu_sum : Summable u_win := h_s3.mul_left ((RiemannScope.tau * Y) ^ (5 / 2 : ℝ))
      unfold infiniteSeqGaussianObservableQ
      apply continuousOn_tsum
      · intro n
        by_cases hn0 : n = 0
        · subst hn0; simp; exact continuousOn_const
        · simp only [hn0, ↓reduceIte]
          exact continuousOn_const.mul
            (continuousOn_gaussianTermPhi_param_tc064_aux Y RiemannScope.tau n)
      · exact hu_sum
      · intro n X hX
        rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX
        have hX0 : 0 < X := lt_of_lt_of_le hY0 hX.1
        dsimp [u_win]
        by_cases hn0 : n = 0
        · subst hn0; simp
        · rw [if_neg hn0, if_neg hn0, abs_mul]
          have hn1 : 1 ≤ n := Nat.pos_of_ne_zero hn0
          obtain ⟨h_nn, h_ub⟩ := h_phi_le hX0 hn1
          rw [abs_of_nonneg h_nn]
          have hrpow : X ^ (5 / 2 : ℝ) ≤ (RiemannScope.tau * Y) ^ (5 / 2 : ℝ) :=
            Real.rpow_le_rpow (le_of_lt hX0) hX.2 (by norm_num)
          calc
            |a n| * gaussianTermPhi n X
              ≤ 1 * (X ^ (5 / 2 : ℝ) * ((1 : ℝ) / (n : ℝ) ^ 3)) :=
                mul_le_mul (ha_abs n hn1) h_ub h_nn zero_le_one
            _ ≤ (RiemannScope.tau * Y) ^ (5 / 2 : ℝ) * ((1 : ℝ) / (n : ℝ) ^ 3) := by
                rw [one_mul]
                exact mul_le_mul_of_nonneg_right hrpow (by positivity)
    refine ⟨h_sum_and_small, h_cont_win, ?_⟩
    intro Y hY1
    have hY0 : 0 < Y := by linarith
    have hle : Y ≤ RiemannScope.tau * Y := by nlinarith
    have hlog_tau : 0 < Real.log RiemannScope.tau := Real.log_pos htau_gt1
    let T := canonicalCutoffT Y
    have hY54_le : Y ^ (5 / 4 : ℝ) ≤ (T : ℝ) := Nat.le_ceil _
    have hT1 : 1 ≤ T := by
      have hp : 0 < Y ^ (5 / 4 : ℝ) := by positivity
      exact Nat.one_le_iff_ne_zero.mpr (Nat.ceil_pos.mpr hp).ne'
    have hT_pos_r : (0 : ℝ) < (T : ℝ) := Nat.cast_pos.mpr hT1
    have hY52_le : Y ^ (5 / 2 : ℝ) ≤ (T : ℝ) ^ 2 := by
      have he : (Y ^ (5 / 4 : ℝ)) ^ 2 = Y ^ (5 / 2 : ℝ) := by
        rw [← Real.rpow_natCast _ 2, ← Real.rpow_mul (le_of_lt hY0)]; norm_num
      rw [← he]; exact pow_le_pow_left (by positivity) hY54_le 2
    let B_tail : ℝ := (1 / 2 : ℝ) * RiemannScope.tau ^ (5 / 2 : ℝ)
    have hBt_nn : 0 ≤ B_tail := by dsimp [B_tail]; positivity
    have h_pt_tail :
        ∀ X ∈ Set.Icc Y (RiemannScope.tau * Y),
          |infiniteSeqGaussianObservableQ a X - truncatedSeqGaussianObservableQ a T X| ≤ B_tail := by
      intro X hX
      have hX0 : 0 < X := lt_of_lt_of_le hY0 hX.1
      have hf_sum := (h_sum_and_small hX0).1
      have hs := sum_add_tsum_nat_add (T + 1) hf_sum
      have h_trunc_eq :
          (∑ n ∈ Finset.range (T + 1), if n = 0 then 0 else a n * gaussianTermPhi n X) =
            truncatedSeqGaussianObservableQ a T X := by
        rw [Finset.sum_range_succ' _ T]
        simp only [↓reduceIte, zero_add, add_zero, Nat.succ_ne_zero]
        unfold truncatedSeqGaussianObservableQ
        have h_im : Finset.Icc 1 T = (Finset.range T).image (fun j => j + 1) := by
          ext n; simp only [Finset.mem_Icc, Finset.mem_image, Finset.mem_range]
          exact ⟨fun hn => ⟨n - 1, by omega, by omega⟩, by rintro ⟨j, hj, rfl⟩; omega⟩
        rw [h_im, Finset.sum_image (fun _ _ _ _ h => by omega)]
      have h_diff_tsum :
          infiniteSeqGaussianObservableQ a X - truncatedSeqGaussianObservableQ a T X =
            ∑' j : ℕ, a (T + 1 + j) * gaussianTermPhi (T + 1 + j) X := by
        unfold infiniteSeqGaussianObservableQ
        rw [← hs, h_trunc_eq, add_sub_cancel_left]
        apply tsum_congr
        intro j
        have h_ne0 : j + (T + 1) ≠ 0 := by omega
        rw [if_neg h_ne0, show j + (T + 1) = T + 1 + j by omega]
      rw [h_diff_tsum, ← Real.norm_eq_abs]
      obtain ⟨hM_s, hM_le⟩ := h_M_tail hT1
      let u_j : ℕ → ℝ := fun j =>
        (RiemannScope.tau ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ)) *
          ((1 : ℝ) / ((T + 1 + j : ℕ) : ℝ) ^ 3)
      have huj_sum : Summable u_j :=
        hM_s.mul_left (RiemannScope.tau ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ))
      have hj_norm :
          ∀ j : ℕ, ‖a (T + 1 + j) * gaussianTermPhi (T + 1 + j) X‖ ≤ u_j j := by
        intro j
        have hj1 : 1 ≤ T + 1 + j := by omega
        obtain ⟨h_nn, h_ub⟩ := h_phi_le hX0 hj1
        rw [Real.norm_eq_abs, abs_mul, abs_of_nonneg h_nn]
        have hrpow :
            X ^ (5 / 2 : ℝ) ≤ RiemannScope.tau ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ) := by
          calc
            X ^ (5 / 2 : ℝ) ≤ (RiemannScope.tau * Y) ^ (5 / 2 : ℝ) :=
              Real.rpow_le_rpow (le_of_lt hX0) hX.2 (by norm_num)
            _ = RiemannScope.tau ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ) :=
              Real.mul_rpow (by linarith) (le_of_lt hY0)
        dsimp [u_j]
        calc
          |a (T + 1 + j)| * gaussianTermPhi (T + 1 + j) X
            ≤ 1 * (X ^ (5 / 2 : ℝ) * ((1 : ℝ) / ((T + 1 + j : ℕ) : ℝ) ^ 3)) :=
              mul_le_mul (ha_abs _ hj1) h_ub h_nn zero_le_one
          _ ≤ (RiemannScope.tau ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ)) *
                ((1 : ℝ) / ((T + 1 + j : ℕ) : ℝ) ^ 3) := by
              rw [one_mul]
              exact mul_le_mul_of_nonneg_right hrpow (by positivity)
      have hf_j_sum : Summable (fun j : ℕ => ‖a (T + 1 + j) * gaussianTermPhi (T + 1 + j) X‖) :=
        (Summable.of_norm_bounded u_j huj_sum hj_norm).norm
      calc
        ‖∑' j : ℕ, a (T + 1 + j) * gaussianTermPhi (T + 1 + j) X‖
          ≤ ∑' j : ℕ, ‖a (T + 1 + j) * gaussianTermPhi (T + 1 + j) X‖ :=
            norm_tsum_le_tsum_norm hf_j_sum
        _ ≤ ∑' j : ℕ, u_j j := tsum_le_tsum hj_norm hf_j_sum huj_sum
        _ = (RiemannScope.tau ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ)) *
              ∑' j : ℕ, (1 : ℝ) / ((T + 1 + j : ℕ) : ℝ) ^ 3 := tsum_mul_left
        _ ≤ (RiemannScope.tau ^ (5 / 2 : ℝ) * Y ^ (5 / 2 : ℝ)) * (1 / (2 * (T : ℝ) ^ 2)) :=
            mul_le_mul_of_nonneg_left hM_le (by positivity)
        _ ≤ (RiemannScope.tau ^ (5 / 2 : ℝ) * (T : ℝ) ^ 2) * (1 / (2 * (T : ℝ) ^ 2)) :=
            mul_le_mul_of_nonneg_right
              (mul_le_mul_of_nonneg_left hY52_le (by positivity)) (by positivity)
        _ = B_tail := by dsimp [B_tail]; field_simp [ne_of_gt hT_pos_r]; ring
    let D_tail : ℝ → ℝ := fun X =>
      infiniteSeqGaussianObservableQ a X - truncatedSeqGaussianObservableQ a T X
    have hc_D : ContinuousOn D_tail (Set.uIcc Y (RiemannScope.tau * Y)) :=
      (h_cont_win hY0).sub
        (continuousOn_finset_sum _ (fun n _ => continuousOn_const.mul
          (continuousOn_gaussianTermPhi_param_tc064_aux Y RiemannScope.tau n)))
    have hpos_w : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), 0 < X := by
      intro X hX; rw [Set.uIcc_of_le hle, Set.mem_Icc] at hX; linarith
    have hi_D : IntervalIntegrable (fun X => D_tail X * D_tail X / X)
        volume Y (RiemannScope.tau * Y) := by
      apply ContinuousOn.intervalIntegrable
      exact (hc_D.mul hc_D).div continuousOn_id (fun X hX => ne_of_gt (hpos_w X hX))
    have hi_B : IntervalIntegrable (fun X => B_tail ^ 2 * ((1 : ℝ) / X))
        volume Y (RiemannScope.tau * Y) := by
      apply ContinuousOn.intervalIntegrable
      exact continuousOn_const.mul
        (continuousOn_const.div continuousOn_id (fun X hX => ne_of_gt (hpos_w X hX)))
    have h_int_le :
        windowEnergyNormSq Y D_tail ≤
          (B_tail * Real.sqrt (Real.log RiemannScope.tau)) ^ 2 := by
      unfold windowEnergyNormSq windowPairing
      calc
        (∫ X in Y..(RiemannScope.tau * Y), D_tail X * D_tail X / X)
          ≤ ∫ X in Y..(RiemannScope.tau * Y), B_tail ^ 2 * ((1 : ℝ) / X) := by
            apply intervalIntegral.integral_mono_on hle hi_D hi_B
            intro X hX
            have hX0 : 0 < X := lt_of_lt_of_le hY0 hX.1
            have habs := h_pt_tail X hX
            have hsq := pow_le_pow_left (abs_nonneg _) habs 2
            rw [sq_abs] at hsq
            have hsq2 : D_tail X * D_tail X ≤ B_tail ^ 2 := by
              change (D_tail X) ^ 2 ≤ B_tail ^ 2 at hsq
              linarith [hsq, show (D_tail X) ^ 2 = D_tail X * D_tail X by ring]
            calc
              D_tail X * D_tail X / X
                ≤ B_tail ^ 2 / X := div_le_div_of_nonneg_right hsq2 (le_of_lt hX0)
              _ = B_tail ^ 2 * ((1 : ℝ) / X) := by ring
        _ = B_tail ^ 2 * (∫ X in Y..(RiemannScope.tau * Y), (1 : ℝ) / X) :=
            intervalIntegral.integral_const_mul _ _
        _ = B_tail ^ 2 * Real.log RiemannScope.tau := by
            rw [integral_inv_window_eq_log_tc064_aux htau_gt1 hY0]
        _ = (B_tail * Real.sqrt (Real.log RiemannScope.tau)) ^ 2 := by
            symm; rw [mul_pow, Real.sq_sqrt (le_of_lt hlog_tau)]
    calc
      Real.sqrt (windowEnergyNormSq Y D_tail)
        ≤ Real.sqrt ((B_tail * Real.sqrt (Real.log RiemannScope.tau)) ^ 2) :=
          Real.sqrt_le_sqrt h_int_le
      _ = B_tail * Real.sqrt (Real.log RiemannScope.tau) :=
          Real.sqrt_sq (mul_nonneg hBt_nn (Real.sqrt_nonneg _))
      _ = (1 / 2 : ℝ) * RiemannScope.tau ^ (5 / 2 : ℝ) *
            Real.sqrt (Real.log RiemannScope.tau) := rfl

private theorem windowEnergyNormSq_comp_div_eq_tc064_aux
    {Y m : ℝ} (hm : 0 < m) (f : ℝ → ℝ) :
    windowEnergyNormSq Y (fun X => f (X / m)) = windowEnergyNormSq (Y / m) f := by
  unfold windowEnergyNormSq windowPairing
  let g : ℝ → ℝ := fun u => f u * f u / u
  have h_pt :
      (fun X : ℝ => f (X / m) * f (X / m) / X) = fun X : ℝ => (1 / m) * g (X / m) := by
    ext X; dsimp [g]; field_simp [ne_of_gt hm]
  rw [h_pt, intervalIntegral.integral_const_mul,
    intervalIntegral.integral_comp_div g (ne_of_gt hm), smul_eq_mul, ← mul_assoc,
    one_div_mul_cancel (ne_of_gt hm), one_mul, mul_div_assoc]

private theorem toggle_pair_series_and_subpower_iff_tc064_aux {q : ℕ} (hq : Nat.Prime q)
    {a : ℕ → ℝ} (ha_abs : ∀ n : ℕ, 1 ≤ n → |a n| ≤ 1)
    (ha_neg : ∀ m : ℕ, 1 ≤ m → a (q * m) = -a m) :
    let b : ℕ → ℝ := fun n => a n * (-1 : ℝ) ^ (n.factorization q)
    (∀ {X : ℝ}, 0 < X →
      infiniteSeqGaussianObservableQ b X =
          infiniteSeqGaussianObservableQ a X +
            2 * ∑' k : ℕ,
              (if k = 0 then 0 else
                (q : ℝ) ^ (-(k : ℝ) / 2) * infiniteSeqGaussianObservableQ a (X / (q : ℝ) ^ k)) ∧
        infiniteSeqGaussianObservableQ a X =
          infiniteSeqGaussianObservableQ b X +
            2 * ∑' k : ℕ,
              (if k = 0 then 0 else
                (-1 : ℝ) ^ k * (q : ℝ) ^ (-(k : ℝ) / 2) *
                  infiniteSeqGaussianObservableQ b (X / (q : ℝ) ^ k))) ∧
    (((∀ ε : ℝ, 0 < ε →
          ∃ C_eps : ℝ, 0 ≤ C_eps ∧
            ∀ Y : ℝ, 1 ≤ Y →
              windowEnergyNormSq Y (infiniteSeqGaussianObservableQ a) ≤ C_eps * Y ^ ε) ↔
        (∀ ε : ℝ, 0 < ε →
          ∃ C_eps : ℝ, 0 ≤ C_eps ∧
            ∀ Y : ℝ, 1 ≤ Y →
              windowEnergyNormSq Y (infiniteSeqGaussianObservableQ b) ≤ C_eps * Y ^ ε)) ∧
      ((∀ ε : ℝ, 0 < ε →
          ∃ C_eps : ℝ, 0 ≤ C_eps ∧
            ∀ Y : ℝ, 1 ≤ Y →
              windowEnergyNormSq Y
                  (truncatedSeqGaussianObservableQ a (canonicalCutoffT Y)) ≤
                C_eps * Y ^ ε) ↔
        (∀ ε : ℝ, 0 < ε →
          ∃ C_eps : ℝ, 0 ≤ C_eps ∧
            ∀ Y : ℝ, 1 ≤ Y →
              windowEnergyNormSq Y
                  (truncatedSeqGaussianObservableQ b (canonicalCutoffT Y)) ≤
                C_eps * Y ^ ε))) := by
  intro b
  obtain ⟨h_dil, h_inf_props⟩ := gaussianTermPhi_dilation_and_infiniteQ_bounds_tc064_aux
  obtain ⟨_, h_coeff_id⟩ := toggle_pair_coeff_identities_tc064_aux hq ha_neg
  have hb_abs : ∀ n : ℕ, 1 ≤ n → |b n| ≤ 1 := by
    intro n hn1
    dsimp [b]
    rw [abs_mul, abs_pow, abs_neg, abs_one, one_pow, mul_one]
    exact ha_abs n hn1
  have hq_pos_r : (0 : ℝ) < (q : ℝ) := Nat.cast_pos.mpr hq.pos
  have hq_gt1_r : (1 : ℝ) < (q : ℝ) := by exact_mod_cast hq.one_lt
  have h_k_le_qk : ∀ k : ℕ, k ≤ q ^ k := by
    intro k
    have h2 : k ≤ 2 ^ k := by
      induction k with
      | zero => norm_num
      | succ k ih => have hp : 1 ≤ 2 ^ k := Nat.one_le_pow k 2 (by decide); omega
    exact le_trans h2 (Nat.pow_le_pow_left hq.two_le k)
  -- General double-series Fubini + finite B_N exhaustion lemma:
  have h_double_series :
      ∀ {c d s : ℕ → ℝ},
        (∀ n : ℕ, 1 ≤ n → |c n| ≤ 1) →
        (∀ n : ℕ, 1 ≤ n → |d n| ≤ 1) →
        (∀ k : ℕ, |s k| ≤ 1) →
        (∀ n : ℕ, 1 ≤ n →
          d n = c n + 2 * ∑ k ∈ (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n),
            s k * c (n / q ^ k)) →
        ∀ {X : ℝ}, 0 < X →
          infiniteSeqGaussianObservableQ d X =
            infiniteSeqGaussianObservableQ c X +
              2 * ∑' k : ℕ,
                (if k = 0 then 0 else
                  s k * (q : ℝ) ^ (-(k : ℝ) / 2) *
                    infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k)) := by
    intro c d s hc_abs hd_abs hs_abs h_pt_cd X hX0
    let G : ℕ × ℕ → ℝ := fun km =>
      if km.1 = 0 ∨ km.2 = 0 then 0 else s km.1 * c km.2 * gaussianTermPhi (q ^ km.1 * km.2) X
    -- Product majorant for G:
    let u_k : ℕ → ℝ := fun k => (1 / (q : ℝ) ^ 3) ^ k
    let v_m : ℕ → ℝ := fun m =>
      X ^ (5 / 2 : ℝ) * (if m = 0 then 0 else (1 : ℝ) / (m : ℝ) ^ 3)
    have hq3_lt1 : ‖(1 / (q : ℝ) ^ 3 : ℝ)‖ < 1 := by
      rw [Real.norm_eq_abs, abs_of_pos (by positivity)]
      have hq3_gt1 : (1 : ℝ) < (q : ℝ) ^ 3 := by
        calc
          (1 : ℝ) = 1 ^ 3 := by norm_num
          _ < (q : ℝ) ^ 3 := pow_lt_pow_left hq_gt1_r zero_le_one (by decide)
      exact (div_lt_one (pow_pos hq_pos_r 3)).mpr hq3_gt1
    have huk_sum : Summable u_k := summable_geometric_of_norm_lt_one hq3_lt1
    have hvm_sum : Summable v_m := by
      have hs_m3 : Summable (fun m : ℕ => if m = 0 then (0 : ℝ) else (1 : ℝ) / (m : ℝ) ^ 3) := by
        apply summable_of_sum_range_le (c := (2 : ℝ)) (fun m => by split_ifs <;> positivity)
        intro N
        have h_step3 :
            ∀ m : ℕ,
              (∑ j ∈ Finset.range m, (1 : ℝ) / ((j + 2 : ℕ) : ℝ) ^ 3) ≤
                (1 / 2 : ℝ) * (1 - 1 / ((m + 1 : ℕ) : ℝ) ^ 2) := by
          intro m; induction m with
          | zero => simp
          | succ m ih =>
            rw [Finset.sum_range_succ]
            let x : ℝ := ((m + 1 : ℕ) : ℝ)
            have hx : 0 < x := by dsimp [x]; positivity
            have hx1 : 0 < x + 1 := by linarith
            have hd :
                (1 / 2 : ℝ) * (1 / x ^ 2 - 1 / (x + 1) ^ 2) - (1 : ℝ) / (x + 1) ^ 3 =
                  (3 * x + 1) / (2 * x ^ 2 * (x + 1) ^ 3) := by
              field_simp [ne_of_gt hx, ne_of_gt hx1]; ring
            have hnn : 0 ≤ (3 * x + 1) / (2 * x ^ 2 * (x + 1) ^ 3) := by positivity
            have c1 : ((m + 2 : ℕ) : ℝ) = x + 1 := by dsimp [x]; push_cast; ring
            rw [c1]
            change (∑ j ∈ Finset.range m, (1 : ℝ) / ((j + 2 : ℕ) : ℝ) ^ 3) + 1 / (x + 1) ^ 3 ≤
              (1 / 2 : ℝ) * (1 - 1 / (x + 1) ^ 2)
            have ih_x :
                (∑ j ∈ Finset.range m, (1 : ℝ) / ((j + 2 : ℕ) : ℝ) ^ 3) ≤
                  (1 / 2 : ℝ) * (1 - 1 / x ^ 2) := ih
            linarith [ih_x, hd, hnn]
        rcases N with _ | _ | m
        · simp
        · simp
        · rw [Finset.sum_range_succ' _ (m + 1), Finset.sum_range_succ' _ m]
          simp only [↓reduceIte, zero_add, add_zero, Nat.succ_ne_zero, Nat.cast_one, one_pow, div_one]
          have h_eq_j :
              (∑ j ∈ Finset.range m, (1 : ℝ) / ((j + 1 + 1 : ℕ) : ℝ) ^ 3) =
                ∑ j ∈ Finset.range m, (1 : ℝ) / ((j + 2 : ℕ) : ℝ) ^ 3 :=
            Finset.sum_congr rfl (fun _ _ => rfl)
          rw [h_eq_j]
          have hm := h_step3 m
          have h_nn : 0 ≤ (1 / 2 : ℝ) * (1 / ((m + 1 : ℕ) : ℝ) ^ 2) := by positivity
          linarith
      exact hs_m3.mul_left (X ^ (5 / 2 : ℝ))
    have huv_prod_sum : Summable (fun km : ℕ × ℕ => u_k km.1 * v_m km.2) :=
      Summable.mul_of_nonneg huk_sum hvm_sum
        (fun _ => by dsimp [u_k]; positivity)
        (fun m => by dsimp [v_m]; split_ifs <;> positivity)
    have hG_norm_le : ∀ km : ℕ × ℕ, ‖G km‖ ≤ u_k km.1 * v_m km.2 := by
      rintro ⟨k, m⟩
      dsimp [G, u_k, v_m]
      by_cases hkm : k = 0 ∨ m = 0
      · rw [if_pos hkm, abs_zero]
        exact mul_nonneg (by positivity) (by split_ifs <;> positivity)
      · push_neg at hkm
        obtain ⟨hk_ne, hm_ne⟩ := hkm
        rw [if_neg (not_or.mpr ⟨hk_ne, hm_ne⟩), if_neg hm_ne,
          abs_mul, abs_mul]
        have hm1 : 1 ≤ m := Nat.pos_of_ne_zero hm_ne
        have hqkm1 : 1 ≤ q ^ k * m := Nat.mul_pos (pow_pos hq.pos k) hm1
        unfold gaussianTermPhi
        have h_nn :
            0 ≤ X ^ (5 / 2 : ℝ) *
              ((((q ^ k * m : ℕ) : ℝ) ^ 3)⁻¹ *
                Real.exp (-(X ^ 2) / ((q ^ k * m : ℕ) : ℝ) ^ 2)) := by
          positivity
        rw [abs_of_nonneg h_nn]
        have hexp : Real.exp (-(X ^ 2) / ((q ^ k * m : ℕ) : ℝ) ^ 2) ≤ 1 := by
          rw [Real.exp_le_one_iff]
          exact div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg X)) (sq_nonneg _)
        have hsc : |s k| * |c m| ≤ 1 := by
          calc |s k| * |c m| ≤ 1 * 1 :=
              mul_le_mul (hs_abs k) (hc_abs m hm1) (abs_nonneg _) zero_le_one
            _ = 1 := one_mul 1
        have h_inv_eq :
            (((q ^ k * m : ℕ) : ℝ) ^ 3)⁻¹ =
              (1 / (q : ℝ) ^ 3) ^ k * ((1 : ℝ) / (m : ℝ) ^ 3) := by
          push_cast
          field_simp [ne_of_gt hq_pos_r, ne_of_gt (show (0 : ℝ) < m by exact_mod_cast hm1)]
          ring
        calc
          |s k| * |c m| *
              (X ^ (5 / 2 : ℝ) *
                ((((q ^ k * m : ℕ) : ℝ) ^ 3)⁻¹ *
                  Real.exp (-(X ^ 2) / ((q ^ k * m : ℕ) : ℝ) ^ 2)))
            ≤ 1 * (X ^ (5 / 2 : ℝ) * ((((q ^ k * m : ℕ) : ℝ) ^ 3)⁻¹ * 1)) :=
              mul_le_mul hsc
                (mul_le_mul_of_nonneg_left
                  (mul_le_mul_of_nonneg_left hexp (by positivity)) (by positivity))
                h_nn zero_le_one
          _ = (1 / (q : ℝ) ^ 3) ^ k * (X ^ (5 / 2 : ℝ) * ((1 : ℝ) / (m : ℝ) ^ 3)) := by
              rw [one_mul, mul_one, h_inv_eq]; ring
    have hG_sum : Summable G := Summable.of_norm_bounded _ huv_prod_sum hG_norm_le
    have hG_row_sum : ∀ k : ℕ, Summable (fun m : ℕ => G (k, m)) := by
      intro k
      exact Summable.of_norm_bounded (fun m => u_k k * v_m m)
        (hvm_sum.mul_left (u_k k)) (fun m => hG_norm_le (k, m))
    have h_tsum_iter :
        (∑' km : ℕ × ℕ, G km) =
          ∑' k : ℕ,
            (if k = 0 then 0 else
              s k * (q : ℝ) ^ (-(k : ℝ) / 2) *
                infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k)) := by
      rw [tsum_prod' hG_sum hG_row_sum]
      apply tsum_congr
      intro k
      by_cases hk0 : k = 0
      · subst hk0; simp [G]
      · rw [if_neg hk0]
        unfold infiniteSeqGaussianObservableQ
        rw [← tsum_mul_left]
        apply tsum_congr
        intro m
        dsimp [G]
        by_cases hm0 : m = 0
        · subst hm0; simp
        · rw [if_neg (not_or.mpr ⟨hk0, hm0⟩), if_neg hm0,
            h_dil hq.pos hX0 (Nat.pos_of_ne_zero hm0)]
          ring
    -- Exhaustion of ℕ × ℕ by B_N := {(k, m) ∈ range N × range N : k = 0 ∨ m = 0 ∨ q^k * m < N}
    let B_set : ℕ → Finset (ℕ × ℕ) := fun N =>
      (Finset.range N ×ˢ Finset.range N).filter
        (fun km => km.1 = 0 ∨ km.2 = 0 ∨ q ^ km.1 * km.2 < N)
    have hB_atTop : Filter.Tendsto B_set Filter.atTop Filter.atTop := by
      rw [Filter.tendsto_atTop]
      intro S_fin
      let N0 := S_fin.sup (fun km => max (max km.1 km.2) (q ^ km.1 * km.2)) + 1
      refine Filter.eventually_atTop.mpr ⟨N0, ?_⟩
      intro N hN km hkm
      have h_le : max (max km.1 km.2) (q ^ km.1 * km.2) ≤ S_fin.sup
          (fun p => max (max p.1 p.2) (q ^ p.1 * p.2)) :=
        Finset.le_sup (f := fun p : ℕ × ℕ => max (max p.1 p.2) (q ^ p.1 * p.2)) hkm
      have h_sup_lt : S_fin.sup (fun p => max (max p.1 p.2) (q ^ p.1 * p.2)) < N := by
        dsimp [N0] at hN; omega
      have h1 : km.1 < N := lt_of_le_of_lt (le_trans (le_max_left _ _) (le_max_left _ _))
        (lt_of_le_of_lt h_le h_sup_lt)
      have h2 : km.2 < N := lt_of_le_of_lt (le_trans (le_max_right _ _) (le_max_left _ _))
        (lt_of_le_of_lt h_le h_sup_lt)
      have h3 : q ^ km.1 * km.2 < N := lt_of_le_of_lt (le_max_right _ _)
        (lt_of_le_of_lt h_le h_sup_lt)
      simp only [B_set, Finset.mem_filter, Finset.mem_product, Finset.mem_range]
      exact ⟨⟨h1, h2⟩, Or.inr (Or.inr h3)⟩
    have hB_tendsto : Filter.Tendsto (fun N => ∑ km ∈ B_set N, G km) Filter.atTop
        (nhds (∑' km : ℕ × ℕ, G km)) :=
      hG_sum.hasSum.comp hB_atTop
    have hc_sum := ((h_inf_props hc_abs).1 hX0).1
    have hd_sum := ((h_inf_props hd_abs).1 hX0).1
    have hc_tend :
        Filter.Tendsto
          (fun N => ∑ n ∈ Finset.range N, if n = 0 then 0 else c n * gaussianTermPhi n X)
          Filter.atTop (nhds (infiniteSeqGaussianObservableQ c X)) :=
      hc_sum.hasSum.tendsto_sum_nat
    have hd_tend :
        Filter.Tendsto
          (fun N => ∑ n ∈ Finset.range N, if n = 0 then 0 else d n * gaussianTermPhi n X)
          Filter.atTop (nhds (infiniteSeqGaussianObservableQ d X)) :=
      hd_sum.hasSum.tendsto_sum_nat
    have h_fin_N :
        ∀ N : ℕ,
          (∑ n ∈ Finset.range N, if n = 0 then 0 else d n * gaussianTermPhi n X) =
            (∑ n ∈ Finset.range N, if n = 0 then 0 else c n * gaussianTermPhi n X) +
              2 * ∑ km ∈ B_set N, G km := by
      intro N
      have h_B_reidx :
          (∑ km ∈ B_set N, G km) =
            ∑ n ∈ Finset.range N,
              if n = 0 then 0 else
                (∑ k ∈ (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n),
                  s k * c (n / q ^ k)) * gaussianTermPhi n X := by
        have h_filt_B :
            (∑ km ∈ B_set N, G km) =
              ∑ km ∈ (B_set N).filter (fun km => km.1 ≠ 0 ∧ km.2 ≠ 0),
                s km.1 * c km.2 * gaussianTermPhi (q ^ km.1 * km.2) X := by
          symm
          rw [Finset.sum_filter]
          apply Finset.sum_congr rfl
          rintro ⟨k, m⟩ _
          dsimp [G]
          by_cases hkm : k = 0 ∨ m = 0
          · have hnot : ¬ (k ≠ 0 ∧ m ≠ 0) := by tauto
            rw [if_neg hnot, if_pos hkm]
          · have hand : k ≠ 0 ∧ m ≠ 0 := by tauto
            rw [if_pos hand, if_neg hkm]
        rw [h_filt_B]
        have h_rhs_sigma :
            (∑ n ∈ Finset.range N,
                if n = 0 then 0 else
                  (∑ k ∈ (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n),
                    s k * c (n / q ^ k)) * gaussianTermPhi n X) =
              ∑ nk ∈ ((Finset.range N).filter (fun n => n ≠ 0)).biUnion
                  (fun n => ((Finset.Icc 1 n).filter (fun k => q ^ k ∣ n)).image
                    (fun k => (n, k))),
                s nk.2 * c (nk.1 / q ^ nk.2) * gaussianTermPhi nk.1 X := by
          have h_ite_n :
              (∑ n ∈ Finset.range N,
                  if n = 0 then 0 else
                    (∑ k ∈ (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n),
                      s k * c (n / q ^ k)) * gaussianTermPhi n X) =
                ∑ n ∈ (Finset.range N).filter (fun n => n ≠ 0),
                  (∑ k ∈ (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n),
                    s k * c (n / q ^ k)) * gaussianTermPhi n X := by
            symm
            rw [Finset.sum_filter]
            apply Finset.sum_congr rfl
            intro n _
            by_cases hn0 : n = 0 <;> simp [hn0]
          rw [h_ite_n]
          have h_disj :
              (((Finset.range N).filter (fun n => n ≠ 0)) : Set ℕ).PairwiseDisjoint
                (fun n => ((Finset.Icc 1 n).filter (fun k => q ^ k ∣ n)).image
                  (fun k => (n, k))) := by
            intro n1 _ n2 _ hne
            change Disjoint _ _
            rw [Finset.disjoint_left]
            intro p hp1 hp2
            rcases Finset.mem_image.mp hp1 with ⟨_, _, rfl⟩
            rcases Finset.mem_image.mp hp2 with ⟨_, _, h_eq⟩
            exact hne (Prod.mk.inj h_eq).1.symm
          rw [Finset.sum_biUnion h_disj]
          apply Finset.sum_congr rfl
          intro n _
          rw [Finset.sum_image (fun _ _ _ _ h => (Prod.mk.inj h).2), Finset.sum_mul]
        rw [h_rhs_sigma]
        apply Finset.sum_bij (fun km _ => (q ^ km.1 * km.2, km.1))
        · rintro ⟨k, m⟩ hkm
          simp only [B_set, Finset.mem_filter, Finset.mem_product, Finset.mem_range] at hkm
          rcases hkm with ⟨⟨⟨_, _⟩, hk0 | hm0 | hprod_lt⟩, hk_ne, hm_ne⟩
          · exact False.elim (hk_ne hk0)
          · exact False.elim (hm_ne hm0)
          · have hk1 : 1 ≤ k := Nat.pos_of_ne_zero hk_ne
            have hm1 : 1 ≤ m := Nat.pos_of_ne_zero hm_ne
            have hn_ne : q ^ k * m ≠ 0 := ne_of_gt (Nat.mul_pos (pow_pos hq.pos k) hm1)
            have hk_le_prod : k ≤ q ^ k * m :=
              le_trans (h_k_le_qk k) (Nat.le_mul_of_pos_right _ hm1)
            simp only [Finset.mem_biUnion, Finset.mem_filter, Finset.mem_range,
              Finset.mem_image, Finset.mem_Icc]
            exact ⟨q ^ k * m, ⟨hprod_lt, hn_ne⟩, k,
              ⟨⟨hk1, hk_le_prod⟩, dvd_mul_right (q ^ k) m⟩, rfl⟩
        · rintro ⟨k1, m1⟩ h1 ⟨k2, m2⟩ _ h_eq
          have hk_eq : k1 = k2 := (Prod.mk.inj h_eq).2
          subst hk_eq
          have hm_eq : m1 = m2 :=
            Nat.eq_of_mul_eq_mul_left (pow_pos hq.pos k1) (Prod.mk.inj h_eq).1
          subst hm_eq; rfl
        · rintro ⟨n, k⟩ hnk
          simp only [Finset.mem_biUnion, Finset.mem_filter, Finset.mem_range,
            Finset.mem_image, Finset.mem_Icc] at hnk
          rcases hnk with ⟨n', ⟨hn'_lt, hn'_ne⟩, k', ⟨⟨hk'1, hk'n⟩, hk'_dvd⟩, h_pair⟩
          cases h_pair
          let m := n / q ^ k
          have h_prod : q ^ k * m = n := Nat.mul_div_cancel' hk'_dvd
          have hm_ne : m ≠ 0 := fun hm0 => by rw [hm0, mul_zero] at h_prod; exact hn'_ne h_prod.symm
          have hm_le_n : m ≤ n := Nat.div_le_self n (q ^ k)
          refine ⟨(k, m), ?_, by rw [h_prod]⟩
          simp only [B_set, Finset.mem_filter, Finset.mem_product, Finset.mem_range]
          exact ⟨⟨⟨lt_of_le_of_lt hk'n hn'_lt, lt_of_le_of_lt hm_le_n hn'_lt⟩,
            Or.inr (Or.inr (by rw [h_prod]; exact hn'_lt))⟩, by omega, hm_ne⟩
        · rintro ⟨k, m⟩ _
          dsimp only
          rw [Nat.mul_div_right m (pow_pos hq.pos k)]
      rw [h_B_reidx, Finset.mul_sum, ← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro n _
      by_cases hn0 : n = 0
      · subst hn0; simp
      · rw [if_neg hn0, if_neg hn0, if_neg hn0, h_pt_cd n (Nat.pos_of_ne_zero hn0)]
        ring
    have h_rhs_tend :
        Filter.Tendsto
          (fun N => (∑ n ∈ Finset.range N, if n = 0 then 0 else c n * gaussianTermPhi n X) +
            2 * ∑ km ∈ B_set N, G km)
          Filter.atTop
          (nhds (infiniteSeqGaussianObservableQ c X + 2 * ∑' km : ℕ × ℕ, G km)) :=
      hc_tend.add (hB_tendsto.const_mul 2)
    have h_fn_eq :
        (fun N => ∑ n ∈ Finset.range N, if n = 0 then 0 else d n * gaussianTermPhi n X) =
          fun N => (∑ n ∈ Finset.range N, if n = 0 then 0 else c n * gaussianTermPhi n X) +
            2 * ∑ km ∈ B_set N, G km := by
      ext N; exact h_fin_N N
    rw [h_fn_eq] at hd_tend
    rw [← h_tsum_iter]
    exact tendsto_nhds_unique hd_tend h_rhs_tend
  have h_series_both :
      ∀ {X : ℝ}, 0 < X →
        infiniteSeqGaussianObservableQ b X =
            infiniteSeqGaussianObservableQ a X +
              2 * ∑' k : ℕ,
                (if k = 0 then 0 else
                  (q : ℝ) ^ (-(k : ℝ) / 2) * infiniteSeqGaussianObservableQ a (X / (q : ℝ) ^ k)) ∧
          infiniteSeqGaussianObservableQ a X =
            infiniteSeqGaussianObservableQ b X +
              2 * ∑' k : ℕ,
                (if k = 0 then 0 else
                  (-1 : ℝ) ^ k * (q : ℝ) ^ (-(k : ℝ) / 2) *
                    infiniteSeqGaussianObservableQ b (X / (q : ℝ) ^ k)) := by
    intro X hX0
    refine ⟨?_, ?_⟩
    · have h1 := h_double_series ha_abs hb_abs (s := fun _ => 1) (fun _ => by norm_num)
        (fun n hn1 => by
          simpa [one_mul] using (h_coeff_id hn1).2.1) hX0
      simpa [one_mul] using h1
    · exact h_double_series hb_abs ha_abs (s := fun k => (-1 : ℝ) ^ k)
        (fun k => by rw [abs_pow, abs_neg, abs_one, one_pow])
        (fun n hn1 => (h_coeff_id hn1).2.2) hX0
  -- One-way subpower transfer for infiniteSeqGaussianObservableQ:
  have h_one_way_inf :
      ∀ {c d s : ℕ → ℝ},
        (∀ n : ℕ, 1 ≤ n → |c n| ≤ 1) →
        (∀ n : ℕ, 1 ≤ n → |d n| ≤ 1) →
        (∀ k : ℕ, |s k| ≤ 1) →
        (∀ {X : ℝ}, 0 < X →
          infiniteSeqGaussianObservableQ d X =
            infiniteSeqGaussianObservableQ c X +
              2 * ∑' k : ℕ,
                (if k = 0 then 0 else
                  s k * (q : ℝ) ^ (-(k : ℝ) / 2) *
                    infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k))) →
        (∀ ε : ℝ, 0 < ε →
          ∃ C_eps : ℝ, 0 ≤ C_eps ∧
            ∀ Y : ℝ, 1 ≤ Y →
              windowEnergyNormSq Y (infiniteSeqGaussianObservableQ c) ≤ C_eps * Y ^ ε) →
        (∀ ε : ℝ, 0 < ε →
          ∃ C_eps : ℝ, 0 ≤ C_eps ∧
            ∀ Y : ℝ, 1 ≤ Y →
              windowEnergyNormSq Y (infiniteSeqGaussianObservableQ d) ≤ C_eps * Y ^ ε) := by
    intro c d s hc_abs hd_abs hs_abs h_series h_c_sub ε hε
    obtain ⟨C_c, hCc_nn, hCc_bd⟩ := h_c_sub ε hε
    have hCg := (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2.1
    have htau_gt1 : (1 : ℝ) < RiemannScope.tau := by linarith
    have hlog_tau : 0 < Real.log RiemannScope.tau := Real.log_pos htau_gt1
    let B_c : ℝ := Real.sqrt C_c
    let B_tail : ℝ := 8 * RiemannScope.tau ^ (5 / 2 : ℝ) * Real.sqrt (Real.log RiemannScope.tau)
    have hBtail_nn : 0 ≤ B_tail := by dsimp [B_tail]; positivity
    let B_d : ℝ := B_c + 2 * (2 + Real.sqrt 2) * B_c + B_tail
    let C_d : ℝ := B_d ^ 2
    refine ⟨C_d, sq_nonneg _, ?_⟩
    intro Y hY1
    have hY0 : 0 < Y := by linarith
    have hle_w : Y ≤ RiemannScope.tau * Y :=
      le_mul_of_one_le_left (le_of_lt hY0) (le_of_lt htau_gt1)
    have hpos_w : ∀ X ∈ Set.uIcc Y (RiemannScope.tau * Y), 0 < X := by
      intro X hX; rw [Set.uIcc_of_le hle_w, Set.mem_Icc] at hX; linarith
    have hlogq_pos : 0 < Real.log (q : ℝ) := Real.log_pos hq_gt1_r
    let N_q := Nat.floor (Real.log Y / Real.log (q : ℝ))
    have h_sqrt_Cc :
        ∀ {Z : ℝ}, 1 ≤ Z →
          Real.sqrt (windowEnergyNormSq Z (infiniteSeqGaussianObservableQ c)) ≤
            B_c * Z ^ (ε / 2) := by
      intro Z hZ1
      have hZ0 : 0 < Z := by linarith
      have he : Z ^ ε = (Z ^ (ε / 2)) ^ 2 := by
        rw [← Real.rpow_natCast _ 2, ← Real.rpow_mul (le_of_lt hZ0)]
        congr 1; ring
      have h_bd := hCc_bd Z hZ1
      rw [he, ← Real.sq_sqrt hCc_nn, ← mul_pow] at h_bd
      calc
        Real.sqrt (windowEnergyNormSq Z (infiniteSeqGaussianObservableQ c))
          ≤ Real.sqrt ((Real.sqrt C_c * Z ^ (ε / 2)) ^ 2) := Real.sqrt_le_sqrt h_bd
        _ = B_c * Z ^ (ε / 2) := Real.sqrt_sq (by positivity)
    -- Summability of k-series for each X > 0:
    have hk_summable :
        ∀ {X : ℝ}, 0 < X →
          Summable (fun k : ℕ =>
            if k = 0 then (0 : ℝ) else
              s k * (q : ℝ) ^ (-(k : ℝ) / 2) *
                infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k)) := by
      intro X hX0
      let u_m : ℕ → ℝ := fun k => (2 * X ^ (5 / 2 : ℝ)) * (1 / (2 : ℝ)) ^ k
      have hum_s : Summable u_m :=
        (summable_geometric_of_norm_lt_one (by norm_num : ‖(1 / 2 : ℝ)‖ < 1)).mul_left _
      apply Summable.of_norm_bounded u_m hum_s
      intro k
      dsimp [u_m]
      by_cases hk0 : k = 0
      · subst hk0; simp; positivity
      · rw [if_neg hk0, abs_mul, abs_mul]
        have hqk_pos : 0 < (q : ℝ) ^ k := pow_pos hq_pos_r k
        have hsm := ((h_inf_props hc_abs).1 (div_pos hX0 hqk_pos)).2
        have h_rpow_le1 : (q : ℝ) ^ (-(k : ℝ) / 2) ≤ 1 :=
          Real.rpow_le_one_of_one_le_of_nonpos (le_of_lt hq_gt1_r)
            (by have : (0 : ℝ) ≤ k := Nat.cast_nonneg k; linarith)
        have h_div_52 :
            (X / (q : ℝ) ^ k) ^ (5 / 2 : ℝ) ≤ X ^ (5 / 2 : ℝ) * (1 / (2 : ℝ)) ^ k := by
          rw [Real.div_rpow (le_of_lt hX0) (le_of_lt hqk_pos)]
          have h2_le_q52 : (2 : ℝ) ^ k ≤ ((q : ℝ) ^ k) ^ (5 / 2 : ℝ) := by
            have hq2 : (2 : ℝ) ≤ (q : ℝ) := by exact_mod_cast hq.two_le
            have h1 : (2 : ℝ) ^ k ≤ (q : ℝ) ^ k := pow_le_pow_left (by norm_num) hq2 k
            have h2 : ((q : ℝ) ^ k) ^ (1 : ℝ) ≤ ((q : ℝ) ^ k) ^ (5 / 2 : ℝ) :=
              Real.rpow_le_rpow_of_exponent_le (one_le_pow_of_one_le (le_of_lt hq_gt1_r) k)
                (by norm_num)
            rw [Real.rpow_one] at h2
            exact le_trans h1 h2
          have h_inv :
              (((q : ℝ) ^ k) ^ (5 / 2 : ℝ))⁻¹ ≤ (1 / (2 : ℝ)) ^ k := by
            rw [one_div_pow, one_div]
            exact inv_le_inv_of_le (pow_pos (by norm_num) k) h2_le_q52
          calc
            X ^ (5 / 2 : ℝ) / ((q : ℝ) ^ k) ^ (5 / 2 : ℝ)
              = X ^ (5 / 2 : ℝ) * (((q : ℝ) ^ k) ^ (5 / 2 : ℝ))⁻¹ := div_eq_mul_inv _ _
            _ ≤ X ^ (5 / 2 : ℝ) * (1 / (2 : ℝ)) ^ k :=
                mul_le_mul_of_nonneg_left h_inv (by positivity)
        rw [abs_of_pos (Real.rpow_pos_of_pos hq_pos_r _)]
        calc
          |s k| * (q : ℝ) ^ (-(k : ℝ) / 2) * |infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k)|
            ≤ (1 * 1) * (2 * (X / (q : ℝ) ^ k) ^ (5 / 2 : ℝ)) :=
              mul_le_mul (mul_le_mul (hs_abs k) h_rpow_le1 (by positivity) zero_le_one)
                hsm (abs_nonneg _) (by norm_num)
          _ ≤ (2 * X ^ (5 / 2 : ℝ)) * (1 / (2 : ℝ)) ^ k := by
              linarith [h_div_52]
    -- Define the 3 window pieces on Set.uIcc Y (tau * Y):
    let P0 : ℝ → ℝ := infiniteSeqGaussianObservableQ c
    let P1 : ℝ → ℝ := fun X =>
      ∑ k ∈ Finset.Icc 1 N_q,
        2 * s k * (q : ℝ) ^ (-(k : ℝ) / 2) *
          infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k)
    let P2 : ℝ → ℝ := fun X =>
      infiniteSeqGaussianObservableQ d X - P0 X - P1 X
    have hc_c_dil :
        ∀ k : ℕ, ContinuousOn
          (fun X => infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k))
          (Set.uIcc Y (RiemannScope.tau * Y)) := by
      intro k
      have hqk_pos : 0 < (q : ℝ) ^ k := pow_pos hq_pos_r k
      have hc_sub := (h_inf_props hc_abs).2.1 (div_pos hY0 hqk_pos)
      have h_maps :
          Set.MapsTo (fun X : ℝ => X / (q : ℝ) ^ k)
            (Set.uIcc Y (RiemannScope.tau * Y))
            (Set.uIcc (Y / (q : ℝ) ^ k) (RiemannScope.tau * (Y / (q : ℝ) ^ k))) := by
        intro X hX
        have hle_k : Y / (q : ℝ) ^ k ≤ RiemannScope.tau * (Y / (q : ℝ) ^ k) :=
          le_mul_of_one_le_left (le_of_lt (div_pos hY0 hqk_pos)) (le_of_lt htau_gt1)
        rw [Set.uIcc_of_le hle_w, Set.mem_Icc] at hX
        rw [Set.uIcc_of_le hle_k, Set.mem_Icc]
        exact ⟨div_le_div_of_nonneg_right hX.1 (le_of_lt hqk_pos),
          by rw [← mul_div_assoc]; exact div_le_div_of_nonneg_right hX.2 (le_of_lt hqk_pos)⟩
      exact hc_sub.comp (continuousOn_id.div_const _) h_maps
    have hc_P0 : ContinuousOn P0 (Set.uIcc Y (RiemannScope.tau * Y)) :=
      (h_inf_props hc_abs).2.1 hY0
    have hc_P1 : ContinuousOn P1 (Set.uIcc Y (RiemannScope.tau * Y)) :=
      continuousOn_finset_sum _ (fun k _ => continuousOn_const.mul (hc_c_dil k))
    have hc_Qd : ContinuousOn (infiniteSeqGaussianObservableQ d)
        (Set.uIcc Y (RiemannScope.tau * Y)) := (h_inf_props hd_abs).2.1 hY0
    have hc_P2 : ContinuousOn P2 (Set.uIcc Y (RiemannScope.tau * Y)) :=
      (hc_Qd.sub hc_P0).sub hc_P1
    -- Bound norm of P1:
    have h_N_P1 :
        Real.sqrt (windowEnergyNormSq Y P1) ≤
          2 * (2 + Real.sqrt 2) * B_c * Y ^ (ε / 2) := by
      have h_mink_P1 :=
        (direct_sum_window_minkowski_sq_tc064_aux hY0 ({0} : Finset ℕ) (Finset.Icc 1 N_q)
          (fun k _ X => 2 * s k * (q : ℝ) ^ (-(k : ℝ) / 2) *
            infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k))
          (fun k _ _ _ => continuousOn_const.mul (hc_c_dil k))).1
      simp only [Finset.sum_singleton] at h_mink_P1
      have h_each_k :
          ∀ k ∈ Finset.Icc 1 N_q,
            Real.sqrt
                (windowEnergyNormSq Y
                  (fun X => 2 * s k * (q : ℝ) ^ (-(k : ℝ) / 2) *
                    infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k))) ≤
              (2 * B_c * Y ^ (ε / 2)) * (1 / Real.sqrt 2) ^ k := by
        intro k hk
        obtain ⟨_hk1, hkN⟩ := Finset.mem_Icc.mp hk
        have hqk_pos : 0 < (q : ℝ) ^ k := pow_pos hq_pos_r k
        have hZ1 : 1 ≤ Y / (q : ℝ) ^ k := by
          have hk_le_div : (k : ℝ) ≤ Real.log Y / Real.log (q : ℝ) :=
            le_trans (by exact_mod_cast hkN)
              (Nat.floor_le (div_nonneg (Real.log_nonneg hY1) (le_of_lt hlogq_pos)))
          have hk_log : (k : ℝ) * Real.log (q : ℝ) ≤ Real.log Y :=
            (le_div_iff hlogq_pos).mp hk_le_div
          have hqk_le_Y : (q : ℝ) ^ k ≤ Y := by
            have hexp := Real.exp_le_exp.mpr hk_log
            rw [Real.exp_log hY0, mul_comm (k : ℝ) (Real.log (q : ℝ)),
              ← Real.rpow_def_of_pos hq_pos_r, Real.rpow_natCast] at hexp
            exact hexp
          exact (one_le_div hqk_pos).mpr hqk_le_Y
        let sc : ℝ := 2 * s k * (q : ℝ) ^ (-(k : ℝ) / 2)
        have h_sc_norm :
            windowEnergyNormSq Y
                (fun X => sc * infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k)) =
              sc ^ 2 * windowEnergyNormSq (Y / (q : ℝ) ^ k) (infiniteSeqGaussianObservableQ c) := by
          rw [← windowEnergyNormSq_comp_div_eq_tc064_aux hqk_pos]
          unfold windowEnergyNormSq windowPairing
          rw [← intervalIntegral.integral_const_mul]
          apply intervalIntegral.integral_congr; intro X _; ring
        have h_qk_rpow : (q : ℝ) ^ (-(k : ℝ) / 2) ≤ (1 / Real.sqrt 2) ^ k := by
          have h_eq : (q : ℝ) ^ (-(k : ℝ) / 2) = (1 / Real.sqrt (q : ℝ)) ^ k := by
            rw [one_div_pow, Real.sqrt_eq_rpow, ← Real.rpow_natCast _ k,
              ← Real.rpow_mul (le_of_lt hq_pos_r), one_div, ← Real.rpow_neg (le_of_lt hq_pos_r)]
            congr 1; ring
          rw [h_eq]
          exact pow_le_pow_left (by positivity)
            (one_div_le_one_div_of_le (Real.sqrt_pos.mpr (by norm_num))
              (Real.sqrt_le_sqrt (by exact_mod_cast hq.two_le))) k
        have hsc_abs : |sc| ≤ 2 * (1 / Real.sqrt 2) ^ k := by
          dsimp [sc]
          rw [abs_mul, abs_mul, abs_of_pos (by norm_num : (0 : ℝ) < 2),
            abs_of_pos (Real.rpow_pos_of_pos hq_pos_r _)]
          calc
            2 * |s k| * (q : ℝ) ^ (-(k : ℝ) / 2)
              ≤ (2 * 1) * (1 / Real.sqrt 2) ^ k :=
                mul_le_mul (mul_le_mul_of_nonneg_left (hs_abs k) (by norm_num))
                  h_qk_rpow (by positivity) (by norm_num)
            _ = 2 * (1 / Real.sqrt 2) ^ k := by ring
        have hZ_le_Y : (Y / (q : ℝ) ^ k) ^ (ε / 2) ≤ Y ^ (ε / 2) :=
          Real.rpow_le_rpow (by positivity)
            (div_le_self (le_of_lt hY0) (one_le_pow_of_one_le (le_of_lt hq_gt1_r) k))
            (by linarith)
        change Real.sqrt (windowEnergyNormSq Y
          (fun X => sc * infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k))) ≤ _
        rw [h_sc_norm, Real.sqrt_mul (sq_nonneg sc), Real.sqrt_sq_eq_abs]
        calc
          |sc| * Real.sqrt (windowEnergyNormSq (Y / (q : ℝ) ^ k) (infiniteSeqGaussianObservableQ c))
            ≤ (2 * (1 / Real.sqrt 2) ^ k) * (B_c * (Y / (q : ℝ) ^ k) ^ (ε / 2)) :=
              mul_le_mul hsc_abs (h_sqrt_Cc hZ1) (Real.sqrt_nonneg _) (by positivity)
          _ ≤ (2 * (1 / Real.sqrt 2) ^ k) * (B_c * Y ^ (ε / 2)) :=
              mul_le_mul_of_nonneg_left
                (mul_le_mul_of_nonneg_left hZ_le_Y (Real.sqrt_nonneg _)) (by positivity)
          _ = (2 * B_c * Y ^ (ε / 2)) * (1 / Real.sqrt 2) ^ k := by ring
      have h_geom_s2 :
          (∑ k ∈ Finset.Icc 1 N_q, (1 / Real.sqrt 2) ^ k) ≤ 2 + Real.sqrt 2 := by
        have h_sub_r : Finset.Icc 1 N_q ⊆ Finset.range (N_q + 1) := by
          intro k hk; exact Finset.mem_range.mpr (by linarith [(Finset.mem_Icc.mp hk).2])
        have h_ind :
            ∀ m : ℕ, (∑ r ∈ Finset.range m, (1 / Real.sqrt 2) ^ r) ≤
              (2 + Real.sqrt 2) * (1 - (1 / Real.sqrt 2) ^ m) := by
          intro m; induction m with
          | zero => simp
          | succ m ih =>
            rw [Finset.sum_range_succ]
            have hs2_pos : 0 < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
            have hs2_sq : Real.sqrt 2 * Real.sqrt 2 = 2 := Real.mul_self_sqrt (by norm_num)
            have h_one : (2 + Real.sqrt 2) * (1 - 1 / Real.sqrt 2) = 1 := by
              apply mul_right_cancel₀ (ne_of_gt hs2_pos)
              calc (2 + Real.sqrt 2) * (1 - 1 / Real.sqrt 2) * Real.sqrt 2
                  = (2 + Real.sqrt 2) * (Real.sqrt 2 - (1 / Real.sqrt 2) * Real.sqrt 2) := by ring
                _ = (2 + Real.sqrt 2) * (Real.sqrt 2 - 1) := by
                    rw [one_div_mul_cancel (ne_of_gt hs2_pos)]
                _ = 2 * Real.sqrt 2 - 2 + Real.sqrt 2 * Real.sqrt 2 - Real.sqrt 2 := by ring
                _ = 1 * Real.sqrt 2 := by rw [hs2_sq]; ring
            have h_step :
                (2 + Real.sqrt 2) * (1 - (1 / Real.sqrt 2) ^ m) + (1 / Real.sqrt 2) ^ m =
                  (2 + Real.sqrt 2) * (1 - (1 / Real.sqrt 2) ^ (m + 1)) := by
              calc (2 + Real.sqrt 2) * (1 - (1 / Real.sqrt 2) ^ m) + (1 / Real.sqrt 2) ^ m
                  = (2 + Real.sqrt 2) * (1 - (1 / Real.sqrt 2) ^ m) +
                      (2 + Real.sqrt 2) * (1 - 1 / Real.sqrt 2) * (1 / Real.sqrt 2) ^ m := by
                    rw [h_one, one_mul]
                _ = (2 + Real.sqrt 2) * (1 - (1 / Real.sqrt 2) ^ (m + 1)) := by
                    rw [pow_succ]; ring
            linarith
        have hi := h_ind (N_q + 1)
        have hq_nn : 0 ≤ (1 / Real.sqrt 2) ^ (N_q + 1) := by positivity
        have h_ub_s2 :
            (2 + Real.sqrt 2) * (1 - (1 / Real.sqrt 2) ^ (N_q + 1)) ≤ 2 + Real.sqrt 2 := by
          have hm := mul_le_mul_of_nonneg_left (sub_le_self (1 : ℝ) hq_nn)
            (by positivity : 0 ≤ 2 + Real.sqrt 2)
          rwa [mul_one] at hm
        calc
          (∑ k ∈ Finset.Icc 1 N_q, (1 / Real.sqrt 2) ^ k)
            ≤ ∑ k ∈ Finset.range (N_q + 1), (1 / Real.sqrt 2) ^ k :=
              Finset.sum_le_sum_of_subset_of_nonneg h_sub_r (fun _ _ _ => by positivity)
          _ ≤ 2 + Real.sqrt 2 := le_trans hi h_ub_s2
      calc
        Real.sqrt (windowEnergyNormSq Y P1)
          ≤ ∑ k ∈ Finset.Icc 1 N_q,
              Real.sqrt
                (windowEnergyNormSq Y
                  (fun X => 2 * s k * (q : ℝ) ^ (-(k : ℝ) / 2) *
                    infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k))) := h_mink_P1
        _ ≤ ∑ k ∈ Finset.Icc 1 N_q, (2 * B_c * Y ^ (ε / 2)) * (1 / Real.sqrt 2) ^ k :=
            Finset.sum_le_sum h_each_k
        _ = (2 * B_c * Y ^ (ε / 2)) * ∑ k ∈ Finset.Icc 1 N_q, (1 / Real.sqrt 2) ^ k :=
            (Finset.mul_sum _ _ _).symm
        _ ≤ (2 * B_c * Y ^ (ε / 2)) * (2 + Real.sqrt 2) :=
            mul_le_mul_of_nonneg_left h_geom_s2 (by dsimp [B_c]; positivity)
        _ = 2 * (2 + Real.sqrt 2) * B_c * Y ^ (ε / 2) := by ring
    -- Bound norm of P2 (k >= N_q + 1 small-argument tail):
    have h_N_P2 :
        Real.sqrt (windowEnergyNormSq Y P2) ≤ B_tail * Y ^ (ε / 2) := by
      have hY_lt_qN1 : Y < (q : ℝ) ^ (N_q + 1) := by
        have hlt : Real.log Y / Real.log (q : ℝ) < ((N_q + 1 : ℕ) : ℝ) := by
          simpa [Nat.cast_add, Nat.cast_one] using
            Nat.lt_floor_add_one (Real.log Y / Real.log (q : ℝ))
        have hlog_lt : Real.log Y < ((N_q + 1 : ℕ) : ℝ) * Real.log (q : ℝ) :=
          (div_lt_iff hlogq_pos).mp hlt
        have hexp := Real.exp_lt_exp.mpr hlog_lt
        rw [Real.exp_log hY0, mul_comm ((N_q + 1 : ℕ) : ℝ) (Real.log (q : ℝ)),
          ← Real.rpow_def_of_pos hq_pos_r, Real.rpow_natCast] at hexp
        exact hexp
      have h_pt_P2 :
          ∀ X ∈ Set.Icc Y (RiemannScope.tau * Y),
            |P2 X| ≤ 8 * RiemannScope.tau ^ (5 / 2 : ℝ) := by
        intro X hX
        have hX0 : 0 < X := lt_of_lt_of_le hY0 hX.1
        have h_sX := h_series hX0
        have hk_sum := hk_summable hX0
        have hs_split := sum_add_tsum_nat_add (N_q + 1) hk_sum
        have h_head_eq :
            2 * (∑ k ∈ Finset.range (N_q + 1),
                if k = 0 then (0 : ℝ) else
                  s k * (q : ℝ) ^ (-(k : ℝ) / 2) *
                    infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k)) = P1 X := by
          rw [Finset.sum_range_succ' _ N_q]
          simp only [↓reduceIte, zero_add, add_zero, Nat.succ_ne_zero]
          have h_im : Finset.Icc 1 N_q = (Finset.range N_q).image (fun j => j + 1) := by
            ext k; simp only [Finset.mem_Icc, Finset.mem_image, Finset.mem_range]
            exact ⟨fun hk => ⟨k - 1, by omega, by omega⟩, by rintro ⟨j, hj, rfl⟩; omega⟩
          dsimp [P1]
          rw [h_im, Finset.sum_image (fun _ _ _ _ h => by omega), Finset.mul_sum]
          apply Finset.sum_congr rfl; intro _ _; ring
        have hP2_tsum :
            P2 X = 2 * ∑' j : ℕ,
              s (j + (N_q + 1)) * (q : ℝ) ^ (-((j + (N_q + 1) : ℕ) : ℝ) / 2) *
                infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ (j + (N_q + 1))) := by
          have h_tail :
              (∑' i : ℕ,
                  if i + (N_q + 1) = 0 then (0 : ℝ) else
                    s (i + (N_q + 1)) * (q : ℝ) ^ (-((i + (N_q + 1) : ℕ) : ℝ) / 2) *
                      infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ (i + (N_q + 1)))) =
                ∑' j : ℕ,
                  s (j + (N_q + 1)) * (q : ℝ) ^ (-((j + (N_q + 1) : ℕ) : ℝ) / 2) *
                    infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ (j + (N_q + 1))) :=
            tsum_congr (fun j => if_neg (by omega))
          dsimp [P2, P0]
          rw [h_sX, ← hs_split, mul_add, h_head_eq, h_tail]
          ring
        rw [hP2_tsum, abs_mul, abs_of_pos (by norm_num : (0 : ℝ) < 2), ← Real.norm_eq_abs]
        let u_g : ℕ → ℝ := fun j => (2 * RiemannScope.tau ^ (5 / 2 : ℝ)) * (1 / (2 : ℝ)) ^ j
        have hug_sum : Summable u_g :=
          (summable_geometric_of_norm_lt_one (by norm_num : ‖(1 / 2 : ℝ)‖ < 1)).mul_left _
        have hj_bd :
            ∀ j : ℕ,
              ‖s (j + (N_q + 1)) * (q : ℝ) ^ (-((j + (N_q + 1) : ℕ) : ℝ) / 2) *
                infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ (j + (N_q + 1)))‖ ≤ u_g j := by
          intro j
          let k := j + (N_q + 1)
          have hqk_pos : 0 < (q : ℝ) ^ k := pow_pos hq_pos_r k
          have hsm := ((h_inf_props hc_abs).1 (div_pos hX0 hqk_pos)).2
          have h_rpow_le1 : (q : ℝ) ^ (-(k : ℝ) / 2) ≤ 1 :=
            Real.rpow_le_one_of_one_le_of_nonpos (le_of_lt hq_gt1_r)
              (by have : (0 : ℝ) ≤ k := Nat.cast_nonneg k; linarith)
          have hX_div_le : X / (q : ℝ) ^ k ≤ RiemannScope.tau / (q : ℝ) ^ j := by
            have h1 : X / (q : ℝ) ^ (N_q + 1) ≤ RiemannScope.tau := by
              calc
                X / (q : ℝ) ^ (N_q + 1)
                  ≤ (RiemannScope.tau * Y) / (q : ℝ) ^ (N_q + 1) :=
                    div_le_div_of_nonneg_right hX.2 (by positivity)
                _ = RiemannScope.tau * (Y / (q : ℝ) ^ (N_q + 1)) := mul_div_assoc _ _ _
                _ ≤ RiemannScope.tau * 1 := mul_le_mul_of_nonneg_left
                    ((div_le_one (pow_pos hq_pos_r _)).mpr (le_of_lt hY_lt_qN1)) (by linarith)
                _ = RiemannScope.tau := mul_one _
            have h_pow_k : (q : ℝ) ^ k = (q : ℝ) ^ (N_q + 1) * (q : ℝ) ^ j := by
              dsimp [k]; rw [pow_add, mul_comm]
            rw [h_pow_k, ← div_div]
            exact div_le_div_of_nonneg_right h1 (by positivity)
          have h_tau_52 :
              (X / (q : ℝ) ^ k) ^ (5 / 2 : ℝ) ≤
                RiemannScope.tau ^ (5 / 2 : ℝ) * (1 / (2 : ℝ)) ^ j := by
            have hqj_pos : 0 < (q : ℝ) ^ j := pow_pos hq_pos_r j
            have h2_le_qj : (2 : ℝ) ^ j ≤ ((q : ℝ) ^ j) ^ (5 / 2 : ℝ) := by
              have hq2 : (2 : ℝ) ≤ (q : ℝ) := by exact_mod_cast hq.two_le
              have h1 : (2 : ℝ) ^ j ≤ (q : ℝ) ^ j := pow_le_pow_left (by norm_num) hq2 j
              have h2 : ((q : ℝ) ^ j) ^ (1 : ℝ) ≤ ((q : ℝ) ^ j) ^ (5 / 2 : ℝ) :=
                Real.rpow_le_rpow_of_exponent_le (one_le_pow_of_one_le (le_of_lt hq_gt1_r) j)
                  (by norm_num)
              rw [Real.rpow_one] at h2
              exact le_trans h1 h2
            calc
              (X / (q : ℝ) ^ k) ^ (5 / 2 : ℝ)
                ≤ (RiemannScope.tau / (q : ℝ) ^ j) ^ (5 / 2 : ℝ) :=
                  Real.rpow_le_rpow (by positivity) hX_div_le (by norm_num)
              _ = RiemannScope.tau ^ (5 / 2 : ℝ) * (((q : ℝ) ^ j) ^ (5 / 2 : ℝ))⁻¹ := by
                  rw [Real.div_rpow (by linarith) (le_of_lt hqj_pos), div_eq_mul_inv]
              _ ≤ RiemannScope.tau ^ (5 / 2 : ℝ) * (1 / (2 : ℝ)) ^ j := by
                  apply mul_le_mul_of_nonneg_left _ (by positivity)
                  rw [one_div_pow, one_div]
                  exact inv_le_inv_of_le (pow_pos (by norm_num) j) h2_le_qj
          change ‖s k * (q : ℝ) ^ (-(k : ℝ) / 2) *
            infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k)‖ ≤ u_g j
          rw [Real.norm_eq_abs, abs_mul, abs_mul, abs_of_pos (Real.rpow_pos_of_pos hq_pos_r _)]
          dsimp [u_g]
          calc
            |s k| * (q : ℝ) ^ (-(k : ℝ) / 2) *
                |infiniteSeqGaussianObservableQ c (X / (q : ℝ) ^ k)|
              ≤ (1 * 1) * (2 * (X / (q : ℝ) ^ k) ^ (5 / 2 : ℝ)) :=
                mul_le_mul (mul_le_mul (hs_abs k) h_rpow_le1 (by positivity) zero_le_one)
                  hsm (abs_nonneg _) (by norm_num)
            _ ≤ (2 * RiemannScope.tau ^ (5 / 2 : ℝ)) * (1 / (2 : ℝ)) ^ j := by
                linarith [h_tau_52]
        have hf_n_sum := (Summable.of_norm_bounded u_g hug_sum hj_bd).norm
        have h_geom_half : (∑' j : ℕ, (1 / (2 : ℝ)) ^ j) = 2 := by
          rw [tsum_geometric_of_norm_lt_one (by norm_num : ‖(1 / 2 : ℝ)‖ < 1)]
          norm_num
        have h_tsum_ug : (∑' j : ℕ, u_g j) = 4 * RiemannScope.tau ^ (5 / 2 : ℝ) := by
          dsimp [u_g]; rw [tsum_mul_left, h_geom_half]; ring
        have h_n_le := le_trans (norm_tsum_le_tsum_norm hf_n_sum)
          (tsum_le_tsum hj_bd hf_n_sum hug_sum)
        linarith [h_n_le, h_tsum_ug]
      have hi_P2 : IntervalIntegrable (fun X => P2 X * P2 X / X)
          volume Y (RiemannScope.tau * Y) := by
        apply ContinuousOn.intervalIntegrable
        exact (hc_P2.mul hc_P2).div continuousOn_id (fun X hX => ne_of_gt (hpos_w X hX))
      have hi_B8 :
          IntervalIntegrable
            (fun X => (8 * RiemannScope.tau ^ (5 / 2 : ℝ)) ^ 2 * ((1 : ℝ) / X))
            volume Y (RiemannScope.tau * Y) := by
        apply ContinuousOn.intervalIntegrable
        exact continuousOn_const.mul
          (continuousOn_const.div continuousOn_id (fun X hX => ne_of_gt (hpos_w X hX)))
      have h_int_P2 : windowEnergyNormSq Y P2 ≤ B_tail ^ 2 := by
        unfold windowEnergyNormSq windowPairing
        calc
          (∫ X in Y..(RiemannScope.tau * Y), P2 X * P2 X / X)
            ≤ ∫ X in Y..(RiemannScope.tau * Y),
                (8 * RiemannScope.tau ^ (5 / 2 : ℝ)) ^ 2 * ((1 : ℝ) / X) := by
              apply intervalIntegral.integral_mono_on hle_w hi_P2 hi_B8
              intro X hX
              have hX0 : 0 < X := lt_of_lt_of_le hY0 hX.1
              have hp := pow_le_pow_left (abs_nonneg _) (h_pt_P2 X hX) 2
              rw [sq_abs] at hp
              have hp2 : P2 X * P2 X ≤ (8 * RiemannScope.tau ^ (5 / 2 : ℝ)) ^ 2 := by
                rw [← sq (P2 X)]; exact hp
              calc
                P2 X * P2 X / X
                  ≤ (8 * RiemannScope.tau ^ (5 / 2 : ℝ)) ^ 2 / X :=
                    div_le_div_of_nonneg_right hp2 (le_of_lt hX0)
                _ = (8 * RiemannScope.tau ^ (5 / 2 : ℝ)) ^ 2 * ((1 : ℝ) / X) := by ring
          _ = (8 * RiemannScope.tau ^ (5 / 2 : ℝ)) ^ 2 *
                (∫ X in Y..(RiemannScope.tau * Y), (1 : ℝ) / X) :=
              intervalIntegral.integral_const_mul _ _
          _ = (8 * RiemannScope.tau ^ (5 / 2 : ℝ)) ^ 2 * Real.log RiemannScope.tau := by
              rw [integral_inv_window_eq_log_tc064_aux htau_gt1 hY0]
          _ = B_tail ^ 2 := by
              dsimp [B_tail]; symm; rw [mul_pow, Real.sq_sqrt (le_of_lt hlog_tau)]
      have h1_rpow : 1 ≤ Y ^ (ε / 2) := Real.one_le_rpow hY1 (by linarith)
      calc
        Real.sqrt (windowEnergyNormSq Y P2)
          ≤ Real.sqrt (B_tail ^ 2) := Real.sqrt_le_sqrt h_int_P2
        _ = B_tail := Real.sqrt_sq hBtail_nn
        _ ≤ B_tail * Y ^ (ε / 2) := le_mul_of_one_le_right hBtail_nn h1_rpow
    -- Combine P0 + P1 + P2 = Q_d via 3-term window Minkowski:
    let F3 : Fin 3 → ℕ → ℝ → ℝ := fun i _ X =>
      match i.val with
      | 0 => P0 X
      | 1 => P1 X
      | _ => P2 X
    have hc_F3 :
        ∀ i ∈ (Finset.univ : Finset (Fin 3)), ∀ _a ∈ ({0} : Finset ℕ),
          ContinuousOn (F3 i _a) (Set.uIcc Y (RiemannScope.tau * Y)) := by
      intro i _ _ _
      fin_cases i
      · exact hc_P0
      · exact hc_P1
      · exact hc_P2
    have h_mink3 :=
      (direct_sum_window_minkowski_sq_tc064_aux hY0 ({0} : Finset ℕ)
        (Finset.univ : Finset (Fin 3)) F3 hc_F3).2
    simp only [Finset.sum_singleton] at h_mink3
    have h_Qd_eq :
        windowEnergyNormSq Y (infiniteSeqGaussianObservableQ d) =
          windowEnergyNormSq Y (fun X => ∑ i : Fin 3, F3 i 0 X) := by
      congr 1; ext X
      rw [Fin.sum_univ_three]
      dsimp [F3, P2, P0, P1]; ring
    rw [h_Qd_eq]
    have h_sum3 :
        (∑ i : Fin 3, Real.sqrt (windowEnergyNormSq Y (F3 i 0))) ≤
          B_d * Y ^ (ε / 2) := by
      rw [Fin.sum_univ_three]
      dsimp [F3, B_d]
      have h0 := h_sqrt_Cc hY1
      linarith [h0, h_N_P1, h_N_P2]
    have h_sq3 := pow_le_pow_left
      (Finset.sum_nonneg (fun _ _ => Real.sqrt_nonneg _)) h_sum3 2
    have he : (Y ^ (ε / 2)) ^ 2 = Y ^ ε := by
      rw [← Real.rpow_natCast _ 2, ← Real.rpow_mul (le_of_lt hY0)]
      congr 1; ring
    calc
      windowEnergyNormSq Y (fun X => ∑ i : Fin 3, F3 i 0 X)
        ≤ (B_d * Y ^ (ε / 2)) ^ 2 := le_trans h_mink3 h_sq3
      _ = C_d * Y ^ ε := by dsimp [C_d]; rw [mul_pow, he]
  -- Equivalence between infiniteSeqGaussianObservableQ and canonical truncatedSeqGaussianObservableQ:
  have h_inf_iff_trunc :
      ∀ {c : ℕ → ℝ}, (∀ n : ℕ, 1 ≤ n → |c n| ≤ 1) →
        ((∀ ε : ℝ, 0 < ε →
            ∃ C_eps : ℝ, 0 ≤ C_eps ∧
              ∀ Y : ℝ, 1 ≤ Y →
                windowEnergyNormSq Y (infiniteSeqGaussianObservableQ c) ≤ C_eps * Y ^ ε) ↔
          (∀ ε : ℝ, 0 < ε →
            ∃ C_eps : ℝ, 0 ≤ C_eps ∧
              ∀ Y : ℝ, 1 ≤ Y →
                windowEnergyNormSq Y
                    (truncatedSeqGaussianObservableQ c (canonicalCutoffT Y)) ≤
                  C_eps * Y ^ ε)) := by
    intro c hc_abs
    let C_tr : ℝ :=
      (1 / 2 : ℝ) * RiemannScope.tau ^ (5 / 2 : ℝ) * Real.sqrt (Real.log RiemannScope.tau)
    have hCg := (finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061).2.2.1
    have htau_gt1 : (1 : ℝ) < RiemannScope.tau := by linarith
    have hCtr_nn : 0 ≤ C_tr := by
      dsimp [C_tr]; have := Real.log_pos htau_gt1; positivity
    constructor
    · intro h_inf ε hε
      obtain ⟨C_i, hCi_nn, hCi_bd⟩ := h_inf ε hε
      refine ⟨(Real.sqrt C_i + C_tr) ^ 2, sq_nonneg _, ?_⟩
      intro Y hY1
      have hY0 : 0 < Y := by linarith
      have hc_inf := (h_inf_props hc_abs).2.1 hY0
      have hc_tr : ContinuousOn (truncatedSeqGaussianObservableQ c (canonicalCutoffT Y))
          (Set.uIcc Y (RiemannScope.tau * Y)) :=
        continuousOn_finset_sum _ (fun n _ => continuousOn_const.mul
          (continuousOn_gaussianTermPhi_param_tc064_aux Y RiemannScope.tau n))
      have h_tri :=
        (((smooth_increment_window_norm_and_small_scale_tail_tc059r).2.1 hY0).1
          hc_inf (hc_inf.sub hc_tr)).2
      have h_sub_eq :
          (fun X => infiniteSeqGaussianObservableQ c X -
            (infiniteSeqGaussianObservableQ c X -
              truncatedSeqGaussianObservableQ c (canonicalCutoffT Y) X)) =
            truncatedSeqGaussianObservableQ c (canonicalCutoffT Y) := by
        ext X; ring
      rw [h_sub_eq] at h_tri
      have he : Y ^ ε = (Y ^ (ε / 2)) ^ 2 := by
        rw [← Real.rpow_natCast _ 2, ← Real.rpow_mul (le_of_lt hY0)]
        congr 1; ring
      have h_s1 :
          Real.sqrt (windowEnergyNormSq Y (infiniteSeqGaussianObservableQ c)) ≤
            Real.sqrt C_i * Y ^ (ε / 2) := by
        have hb := hCi_bd Y hY1
        rw [he, ← Real.sq_sqrt hCi_nn, ← mul_pow] at hb
        calc
          _ ≤ Real.sqrt ((Real.sqrt C_i * Y ^ (ε / 2)) ^ 2) := Real.sqrt_le_sqrt hb
          _ = Real.sqrt C_i * Y ^ (ε / 2) := Real.sqrt_sq (by positivity)
      have h_s2 :
          Real.sqrt
              (windowEnergyNormSq Y
                (fun X => infiniteSeqGaussianObservableQ c X -
                  truncatedSeqGaussianObservableQ c (canonicalCutoffT Y) X)) ≤
            C_tr * Y ^ (ε / 2) :=
        le_trans ((h_inf_props hc_abs).2.2 hY1)
          (le_mul_of_one_le_right hCtr_nn (Real.one_le_rpow hY1 (by linarith)))
      have h_tot :
          Real.sqrt
              (windowEnergyNormSq Y
                (truncatedSeqGaussianObservableQ c (canonicalCutoffT Y))) ≤
            (Real.sqrt C_i + C_tr) * Y ^ (ε / 2) := by
        linarith [h_tri, h_s1, h_s2]
      have h_nn_tr :
          0 ≤ windowEnergyNormSq Y
              (truncatedSeqGaussianObservableQ c (canonicalCutoffT Y)) := by
        have hle : Y ≤ RiemannScope.tau * Y :=
          le_mul_of_one_le_left (le_of_lt hY0) (le_of_lt htau_gt1)
        unfold windowEnergyNormSq windowPairing
        apply intervalIntegral.integral_nonneg hle
        intro X hX; exact div_nonneg (mul_self_nonneg _) (by linarith [hX.1])
      have hp := pow_le_pow_left (Real.sqrt_nonneg _) h_tot 2
      rw [Real.sq_sqrt h_nn_tr, mul_pow, ← he] at hp
      exact hp
    · intro h_tr ε hε
      obtain ⟨C_t, hCt_nn, hCt_bd⟩ := h_tr ε hε
      refine ⟨(Real.sqrt C_t + C_tr) ^ 2, sq_nonneg _, ?_⟩
      intro Y hY1
      have hY0 : 0 < Y := by linarith
      have hc_inf := (h_inf_props hc_abs).2.1 hY0
      have hc_tr : ContinuousOn (truncatedSeqGaussianObservableQ c (canonicalCutoffT Y))
          (Set.uIcc Y (RiemannScope.tau * Y)) :=
        continuousOn_finset_sum _ (fun n _ => continuousOn_const.mul
          (continuousOn_gaussianTermPhi_param_tc064_aux Y RiemannScope.tau n))
      have h_tri :=
        (((smooth_increment_window_norm_and_small_scale_tail_tc059r).2.1 hY0).1
          hc_tr (hc_tr.sub hc_inf)).2
      have h_sub_eq :
          (fun X => truncatedSeqGaussianObservableQ c (canonicalCutoffT Y) X -
            (truncatedSeqGaussianObservableQ c (canonicalCutoffT Y) X -
              infiniteSeqGaussianObservableQ c X)) =
            infiniteSeqGaussianObservableQ c := by
        ext X; ring
      rw [h_sub_eq] at h_tri
      have h_symm_norm :
          windowEnergyNormSq Y
              (fun X => truncatedSeqGaussianObservableQ c (canonicalCutoffT Y) X -
                infiniteSeqGaussianObservableQ c X) =
            windowEnergyNormSq Y
              (fun X => infiniteSeqGaussianObservableQ c X -
                truncatedSeqGaussianObservableQ c (canonicalCutoffT Y) X) := by
        unfold windowEnergyNormSq windowPairing
        apply intervalIntegral.integral_congr; intro X _; ring
      rw [h_symm_norm] at h_tri
      have he : Y ^ ε = (Y ^ (ε / 2)) ^ 2 := by
        rw [← Real.rpow_natCast _ 2, ← Real.rpow_mul (le_of_lt hY0)]
        congr 1; ring
      have h_s1 :
          Real.sqrt
              (windowEnergyNormSq Y
                (truncatedSeqGaussianObservableQ c (canonicalCutoffT Y))) ≤
            Real.sqrt C_t * Y ^ (ε / 2) := by
        have hb := hCt_bd Y hY1
        rw [he, ← Real.sq_sqrt hCt_nn, ← mul_pow] at hb
        calc
          _ ≤ Real.sqrt ((Real.sqrt C_t * Y ^ (ε / 2)) ^ 2) := Real.sqrt_le_sqrt hb
          _ = Real.sqrt C_t * Y ^ (ε / 2) := Real.sqrt_sq (by positivity)
      have h_s2 :
          Real.sqrt
              (windowEnergyNormSq Y
                (fun X => infiniteSeqGaussianObservableQ c X -
                  truncatedSeqGaussianObservableQ c (canonicalCutoffT Y) X)) ≤
            C_tr * Y ^ (ε / 2) :=
        le_trans ((h_inf_props hc_abs).2.2 hY1)
          (le_mul_of_one_le_right hCtr_nn (Real.one_le_rpow hY1 (by linarith)))
      have h_tot :
          Real.sqrt (windowEnergyNormSq Y (infiniteSeqGaussianObservableQ c)) ≤
            (Real.sqrt C_t + C_tr) * Y ^ (ε / 2) := by
        linarith [h_tri, h_s1, h_s2]
      have h_nn_inf :
          0 ≤ windowEnergyNormSq Y (infiniteSeqGaussianObservableQ c) := by
        have hle : Y ≤ RiemannScope.tau * Y :=
          le_mul_of_one_le_left (le_of_lt hY0) (le_of_lt htau_gt1)
        unfold windowEnergyNormSq windowPairing
        apply intervalIntegral.integral_nonneg hle
        intro X hX; exact div_nonneg (mul_self_nonneg _) (by linarith [hX.1])
      have hp := pow_le_pow_left (Real.sqrt_nonneg _) h_tot 2
      rw [Real.sq_sqrt h_nn_inf, mul_pow, ← he] at hp
      exact hp
  have h_inf_iff :
      (∀ ε : ℝ, 0 < ε →
          ∃ C_eps : ℝ, 0 ≤ C_eps ∧
            ∀ Y : ℝ, 1 ≤ Y →
              windowEnergyNormSq Y (infiniteSeqGaussianObservableQ a) ≤ C_eps * Y ^ ε) ↔
        (∀ ε : ℝ, 0 < ε →
          ∃ C_eps : ℝ, 0 ≤ C_eps ∧
            ∀ Y : ℝ, 1 ≤ Y →
              windowEnergyNormSq Y (infiniteSeqGaussianObservableQ b) ≤ C_eps * Y ^ ε) :=
    ⟨h_one_way_inf ha_abs hb_abs (s := fun _ => 1) (fun _ => by norm_num)
        (fun {_} hX0 => by simpa [one_mul] using (h_series_both hX0).1),
      h_one_way_inf hb_abs ha_abs (s := fun k => (-1 : ℝ) ^ k)
        (fun k => by rw [abs_pow, abs_neg, abs_one, one_pow])
        (fun {_} hX0 => (h_series_both hX0).2)⟩
  exact ⟨h_series_both, h_inf_iff,
    (h_inf_iff_trunc ha_abs).symm.trans (h_inf_iff.trans (h_inf_iff_trunc hb_abs))⟩

/-- **Theorem 5 (`TASK-TC-064` §5, Deliverable D — Finite Euler-Factor Valuation Toggle, Dirichlet Multiplier Holomorphy, `z → 1` Residue Cancellation, Bidirectional Infinite Gaussian Dilation Series, and Finite-Prime-Set Subpower Window Energy Equivalence)**:
    Writing `z = (x : ℂ) + (y : ℂ) * Complex.I` for real coordinates `x, y : ℝ`:
    1. *Exact `z → 1` ratio limit (`𝓝[≠] 1`)*:
       `Filter.Tendsto (fun w : ℂ => riemannZeta (2 * w) / riemannZeta w) (nhdsWithin 1 {1}ᶜ) (nhds 0)`;
    2. *Single odd-prime valuation toggle (`Nat.Prime q ∧ Odd q`)*:
       - Exact bidirectional pointwise coefficient identities on `n ≥ 1` between `primeValuationToggleSeq q` and `liouvilleLambda`;
       - Dirichlet ratio `LSeries f_q z = LSeries f_lam z * ((1 + q^(-z)) / (1 - q^(-z)))` on `1 < x`;
       - Multiplier holomorphy and nonvanishing of `(1 + q^(-w)) / (1 - q^(-w))` and its reciprocal on `{w : ℂ | 0 < w.re}` (and pointwise on `0 < x`), two-way pole-free continuation equivalence on `{w : ℂ | 1 / 2 < w.re}`, and critical-line zero localization `x = 1 / 2` on `0 < x < 1`;
       - Exact station dilation `gaussianTermPhi (q^k * r) X = q^(-k/2) * gaussianTermPhi r (X / q^k)`, summability, small-`X` bound `≤ 2 * X^(5/2)`, uniform canonical tail window norm bound `≤ (1/2) * tau^(5/2) * √(log tau)` (`1 ≤ Y`), bidirectional `infiniteSeqGaussianObservableQ` dilation series (`0 < X`), and two-way subpower window energy equivalence (both infinite and canonical truncated on `1 ≤ Y`);
    3. *Finite odd-prime set induction (`∀ q ∈ S, Nat.Prime q ∧ Odd q`)*:
       Two-way subpower window energy equivalence (both infinite and canonical truncated on `1 ≤ Y`) between `a_lam n := (liouvilleLambda n : ℝ)` and `a_S n := (liouvilleLambda n : ℝ) * (-1 : ℝ) ^ (∑ q ∈ S, n.factorization q)`. -/
theorem finite_euler_factor_dirichlet_multiplier_and_dilation_equivalence_tc064 :
    Filter.Tendsto (fun w : ℂ => riemannZeta (2 * w) / riemannZeta w)
        (nhdsWithin (1 : ℂ) {(1 : ℂ)}ᶜ) (nhds (0 : ℂ)) ∧
    (∀ {q : ℕ}, Nat.Prime q → Odd q →
      let a_lam : ℕ → ℝ := fun n => (liouvilleLambda n : ℝ)
      let a_q : ℕ → ℝ := fun n => (primeValuationToggleSeq q n : ℝ)
      let f_lam : ℕ → ℂ := fun n => if n = 0 then 0 else (liouvilleLambda n : ℂ)
      let f_q : ℕ → ℂ := fun n => if n = 0 then 0 else (primeValuationToggleSeq q n : ℂ)
      let M_q : ℂ → ℂ := fun w => (1 + (q : ℂ) ^ (-w)) / (1 - (q : ℂ) ^ (-w))
      let M_inv : ℂ → ℂ := fun w => (1 - (q : ℂ) ^ (-w)) / (1 + (q : ℂ) ^ (-w))
      (∀ {n : ℕ}, 1 ≤ n →
        (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n) = Finset.Icc 1 (n.factorization q) ∧
          (primeValuationToggleSeq q n : ℝ) =
            (liouvilleLambda n : ℝ) +
              2 * ∑ k ∈ (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n),
                (liouvilleLambda (n / q ^ k) : ℝ) ∧
          (liouvilleLambda n : ℝ) =
            (primeValuationToggleSeq q n : ℝ) +
              2 * ∑ k ∈ (Finset.Icc 1 n).filter (fun k => q ^ k ∣ n),
                (-1 : ℝ) ^ k * (primeValuationToggleSeq q (n / q ^ k) : ℝ)) ∧
      ((∀ (x y : ℝ), 0 < x →
          let z : ℂ := (x : ℂ) + (y : ℂ) * Complex.I
          1 - (q : ℂ) ^ (-z) ≠ 0 ∧ 1 + (q : ℂ) ^ (-z) ≠ 0 ∧ M_q z * M_inv z = 1) ∧
        DifferentiableOn ℂ M_q {w : ℂ | 0 < w.re} ∧
        DifferentiableOn ℂ M_inv {w : ℂ | 0 < w.re} ∧
        (∀ w ∈ {w : ℂ | 0 < w.re}, M_q w ≠ 0 ∧ M_inv w ≠ 0 ∧ M_q w * M_inv w = 1) ∧
        (∀ (x y : ℝ), 1 < x →
          let z : ℂ := (x : ℂ) + (y : ℂ) * Complex.I
          LSeries f_q z = LSeries f_lam z * M_q z) ∧
        ((∃ F_lam : ℂ → ℂ,
            DifferentiableOn ℂ F_lam {w : ℂ | (1 / 2 : ℝ) < w.re} ∧
              ∀ x y : ℝ, 1 < x →
                F_lam ((x : ℂ) + (y : ℂ) * Complex.I) =
                  LSeries f_lam ((x : ℂ) + (y : ℂ) * Complex.I)) ↔
          (∃ F_q : ℂ → ℂ,
            DifferentiableOn ℂ F_q {w : ℂ | (1 / 2 : ℝ) < w.re} ∧
              ∀ x y : ℝ, 1 < x →
                F_q ((x : ℂ) + (y : ℂ) * Complex.I) =
                  LSeries f_q ((x : ℂ) + (y : ℂ) * Complex.I))) ∧
        ((∃ F_q : ℂ → ℂ,
            DifferentiableOn ℂ F_q {w : ℂ | (1 / 2 : ℝ) < w.re} ∧
              ∀ x y : ℝ, 1 < x →
                F_q ((x : ℂ) + (y : ℂ) * Complex.I) =
                  LSeries f_q ((x : ℂ) + (y : ℂ) * Complex.I)) →
          ∀ (x y : ℝ), 0 < x → x < 1 →
            riemannZeta ((x : ℂ) + (y : ℂ) * Complex.I) = 0 → x = 1 / 2)) ∧
      ((∀ {X : ℝ}, 0 < X → ∀ {k r : ℕ}, 1 ≤ r →
          gaussianTermPhi (q ^ k * r) X =
            (q : ℝ) ^ (-(k : ℝ) / 2) * gaussianTermPhi r (X / (q : ℝ) ^ k)) ∧
        (∀ {a : ℕ → ℝ}, (∀ n : ℕ, 1 ≤ n → |a n| ≤ 1) →
          (∀ {X : ℝ}, 0 < X →
            Summable (fun n : ℕ => if n = 0 then 0 else a n * gaussianTermPhi n X) ∧
              |infiniteSeqGaussianObservableQ a X| ≤ 2 * X ^ (5 / 2 : ℝ)) ∧
          (∀ {Y : ℝ}, 1 ≤ Y →
            Real.sqrt
                (windowEnergyNormSq Y
                  (fun X =>
                    infiniteSeqGaussianObservableQ a X -
                      truncatedSeqGaussianObservableQ a (canonicalCutoffT Y) X)) ≤
              (1 / 2 : ℝ) * RiemannScope.tau ^ (5 / 2 : ℝ) *
                Real.sqrt (Real.log RiemannScope.tau))) ∧
        (∀ {X : ℝ}, 0 < X →
          infiniteSeqGaussianObservableQ a_q X =
              infiniteSeqGaussianObservableQ a_lam X +
                2 * ∑' k : ℕ,
                  (if k = 0 then 0 else
                    (q : ℝ) ^ (-(k : ℝ) / 2) *
                      infiniteSeqGaussianObservableQ a_lam (X / (q : ℝ) ^ k)) ∧
            infiniteSeqGaussianObservableQ a_lam X =
              infiniteSeqGaussianObservableQ a_q X +
                2 * ∑' k : ℕ,
                  (if k = 0 then 0 else
                    (-1 : ℝ) ^ k * (q : ℝ) ^ (-(k : ℝ) / 2) *
                      infiniteSeqGaussianObservableQ a_q (X / (q : ℝ) ^ k))) ∧
        (((∀ ε : ℝ, 0 < ε →
              ∃ C_eps : ℝ, 0 ≤ C_eps ∧
                ∀ Y : ℝ, 1 ≤ Y →
                  windowEnergyNormSq Y (infiniteSeqGaussianObservableQ a_lam) ≤ C_eps * Y ^ ε) ↔
            (∀ ε : ℝ, 0 < ε →
              ∃ C_eps : ℝ, 0 ≤ C_eps ∧
                ∀ Y : ℝ, 1 ≤ Y →
                  windowEnergyNormSq Y (infiniteSeqGaussianObservableQ a_q) ≤ C_eps * Y ^ ε)) ∧
          ((∀ ε : ℝ, 0 < ε →
              ∃ C_eps : ℝ, 0 ≤ C_eps ∧
                ∀ Y : ℝ, 1 ≤ Y →
                  windowEnergyNormSq Y
                      (truncatedSeqGaussianObservableQ a_lam (canonicalCutoffT Y)) ≤
                    C_eps * Y ^ ε) ↔
            (∀ ε : ℝ, 0 < ε →
              ∃ C_eps : ℝ, 0 ≤ C_eps ∧
                ∀ Y : ℝ, 1 ≤ Y →
                  windowEnergyNormSq Y
                      (truncatedSeqGaussianObservableQ a_q (canonicalCutoffT Y)) ≤
                    C_eps * Y ^ ε))))) ∧
    (∀ (S : Finset ℕ), (∀ q ∈ S, Nat.Prime q ∧ Odd q) →
      let a_lam : ℕ → ℝ := fun n => (liouvilleLambda n : ℝ)
      let a_S : ℕ → ℝ := fun n =>
        (liouvilleLambda n : ℝ) * (-1 : ℝ) ^ (∑ q ∈ S, n.factorization q)
      ((∀ ε : ℝ, 0 < ε →
          ∃ C_eps : ℝ, 0 ≤ C_eps ∧
            ∀ Y : ℝ, 1 ≤ Y →
              windowEnergyNormSq Y (infiniteSeqGaussianObservableQ a_lam) ≤ C_eps * Y ^ ε) ↔
        (∀ ε : ℝ, 0 < ε →
          ∃ C_eps : ℝ, 0 ≤ C_eps ∧
            ∀ Y : ℝ, 1 ≤ Y →
              windowEnergyNormSq Y (infiniteSeqGaussianObservableQ a_S) ≤ C_eps * Y ^ ε)) ∧
      ((∀ ε : ℝ, 0 < ε →
          ∃ C_eps : ℝ, 0 ≤ C_eps ∧
            ∀ Y : ℝ, 1 ≤ Y →
              windowEnergyNormSq Y
                  (truncatedSeqGaussianObservableQ a_lam (canonicalCutoffT Y)) ≤
                C_eps * Y ^ ε) ↔
        (∀ ε : ℝ, 0 < ε →
          ∃ C_eps : ℝ, 0 ≤ C_eps ∧
            ∀ Y : ℝ, 1 ≤ Y →
              windowEnergyNormSq Y
                  (truncatedSeqGaussianObservableQ a_S (canonicalCutoffT Y)) ≤
                C_eps * Y ^ ε))) := by
  have h_lam_abs : ∀ n : ℕ, 1 ≤ n → |(liouvilleLambda n : ℝ)| ≤ 1 := by
    intro n hn1
    have hn_ne : n ≠ 0 := by omega
    simp [liouvilleLambda, hn_ne, liouvilleSignFromOmega]
  refine ⟨zeta_two_div_zeta_tendsto_zero_at_one_tc064_aux, ?_, ?_⟩
  · intro q hq _hq_o a_lam a_q f_lam f_q M_q M_inv
    have ha_q_eq : a_q = fun n => a_lam n * (-1 : ℝ) ^ (n.factorization q) := by
      ext n; dsimp [a_q, a_lam]; unfold primeValuationToggleSeq; push_cast; rfl
    obtain ⟨_, h_coeff⟩ :=
      toggle_pair_coeff_identities_tc064_aux (a := a_lam) hq
        (fun _ hm => liouville_prime_mul_neg_tc064_aux hq hm)
    obtain ⟨h_M_props, h_L_ratio, h_cont_iff, h_loc⟩ :=
      euler_multiplier_and_lseries_ratio_tc064_aux hq
    obtain ⟨h_dil, h_inf_bds⟩ := gaussianTermPhi_dilation_and_infiniteQ_bounds_tc064_aux
    obtain ⟨h_series, h_iff_inf, h_iff_tr⟩ :=
      toggle_pair_series_and_subpower_iff_tc064_aux hq h_lam_abs
        (fun _ hm => liouville_prime_mul_neg_tc064_aux hq hm)
    refine ⟨?_, ⟨h_M_props.1, h_M_props.2.1, h_M_props.2.2.1, h_M_props.2.2.2,
        h_L_ratio, h_cont_iff, h_loc⟩,
      ⟨fun {_} hX0 {_ _} hr1 => h_dil hq.pos hX0 hr1,
        fun {_} ha => ⟨(h_inf_bds ha).1, (h_inf_bds ha).2.2⟩,
        fun {_} hX0 => by rw [ha_q_eq]; exact h_series hX0,
        by rw [ha_q_eq]; exact ⟨h_iff_inf, h_iff_tr⟩⟩⟩
    intro n hn1
    obtain ⟨hf_eq, hb1, hb2⟩ := h_coeff hn1
    have h_fn_eq :
        (fun m : ℕ => (liouvilleLambda m : ℝ) * (-1 : ℝ) ^ (m.factorization q)) = a_q :=
      ha_q_eq.symm
    change _ ∧ a_q n = a_lam n + 2 * ∑ k ∈ _, a_lam (n / q ^ k) ∧
      a_lam n = a_q n + 2 * ∑ k ∈ _, (-1 : ℝ) ^ k * a_q (n / q ^ k)
    rw [← h_fn_eq]
    exact ⟨hf_eq, hb1, hb2⟩
  · intro S hS
    induction S using Finset.induction_on with
    | empty =>
      dsimp only
      have ha_emp :
          (fun n : ℕ => (liouvilleLambda n : ℝ) *
              (-1 : ℝ) ^ (∑ q ∈ (∅ : Finset ℕ), n.factorization q)) =
            fun n => (liouvilleLambda n : ℝ) := by
        ext n; simp
      rw [ha_emp]
      exact ⟨Iff.rfl, Iff.rfl⟩
    | @insert q0 S' hq0_not ih =>
      have hq0_pr : Nat.Prime q0 := (hS q0 (Finset.mem_insert_self q0 S')).1
      have hS' : ∀ q ∈ S', Nat.Prime q ∧ Odd q :=
        fun q hq => hS q (Finset.mem_insert_of_mem hq)
      obtain ⟨ih_inf, ih_tr⟩ := ih hS'
      let a_S' : ℕ → ℝ := fun n =>
        (liouvilleLambda n : ℝ) * (-1 : ℝ) ^ (∑ q ∈ S', n.factorization q)
      have haS'_abs : ∀ n : ℕ, 1 ≤ n → |a_S' n| ≤ 1 := by
        intro n hn1
        dsimp [a_S']
        rw [abs_mul, abs_pow, abs_neg, abs_one, one_pow, mul_one]
        exact h_lam_abs n hn1
      have haS'_neg : ∀ m : ℕ, 1 ≤ m → a_S' (q0 * m) = -a_S' m := by
        intro m hm1
        have hm_ne : m ≠ 0 := by omega
        have h_sum_eq :
            (∑ q ∈ S', (q0 * m).factorization q) = ∑ q ∈ S', m.factorization q := by
          apply Finset.sum_congr rfl
          intro q hq_in
          have hq_ne_q0 : q ≠ q0 := fun heq => hq0_not (heq ▸ hq_in)
          have h_not_dvd : ¬ q ∣ q0 := by
            intro hd
            have hq_pr : Nat.Prime q := (hS' q hq_in).1
            rcases hq0_pr.eq_one_or_self_of_dvd q hd with rfl | rfl
            · exact hq_pr.ne_one rfl
            · exact hq_ne_q0 rfl
          rw [Nat.factorization_mul hq0_pr.ne_zero hm_ne, Finsupp.add_apply,
            Nat.factorization_eq_zero_of_not_dvd h_not_dvd, zero_add]
        dsimp [a_S']
        rw [liouville_prime_mul_neg_tc064_aux hq0_pr hm1, h_sum_eq]
        ring
      have ha_ins_eq :
          (fun n : ℕ => (liouvilleLambda n : ℝ) *
              (-1 : ℝ) ^ (∑ q ∈ insert q0 S', n.factorization q)) =
            fun n : ℕ => a_S' n * (-1 : ℝ) ^ (n.factorization q0) := by
        ext n
        dsimp [a_S']
        rw [Finset.sum_insert hq0_not, pow_add]
        ring
      obtain ⟨_, h_step_inf, h_step_tr⟩ :=
        toggle_pair_series_and_subpower_iff_tc064_aux hq0_pr haS'_abs haS'_neg
      dsimp only
      rw [ha_ins_eq]
      exact ⟨ih_inf.trans h_step_inf, ih_tr.trans h_step_tr⟩

end RiemannScope
