/-
RiemannScope.AmbientKernel
TASK-TC-028 / TASK-TC-028R: Ambient Realization Kernel, Rational Support Rank, and Algebraic-Power Independence.

LEAN_PROVED Scope (Algebraic Skeleton / Low Arity):
1. Support translation invariance of ambient evaluation for 2-term and 3-term sums:
   a1*tau^K1 + a2*tau^K2 = 0 <==> a1*tau^(K1-K0) + a2*tau^(K2-K0) = 0
2. Rank-zero trivial coefficient cancellation for 2-term and 3-term sums:
   a1*tau^K0 + a2*tau^K0 = 0 <==> a1 + a2 = 0
3. Base-grade affine difference identity of real numbers:
   (K - K0') = (K - K0) - (K0' - K0)
4. Explicit kernel witness for algebraic generator (alpha ∈ S_tau):
   tau^alpha = A ==> 1 * tau^alpha + (-A) * tau^0 = 0
5. Rank-one 2-term linear impossibility under abstract algebraicity predicate:
   c1 * tau^alpha + c0 = 0 with c1 ≠ 0 and c0, c1 algebraic forces tau^alpha algebraic
6. Group-algebra structural multiplication law:
   tau^K * tau^J = tau^(K + J) is an algebra homomorphism law
7. Bivariate Laurent monomial clearing algebra identity:
   c * X^(m + Nx) * Y^(n + Ny) = (X^Nx * Y^Ny) * (c * X^m * Y^n)
8. Pairwise transcendence insufficiency abstract countermodel:
   v = u^2 ==> v - u^2 = 0

NOTE ON SCOPE BOUNDARIES:
- LEAN_PROVED: The algebraic skeleton and low-arity identities enumerated above.
- PROVED_PAPER_DERIVATION: Full group algebra Q_bar[Q*alpha] injectivity,
  equality of Q-spans and vector space dimensions, higher-rank multivariate
  algebraic-independence equivalence, and the two-case Schanuel conditional theorem.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import RiemannScope.Grade
import RiemannScope.GradedMonoid
import RiemannScope.TranscendenceRigidity
import RiemannScope.FaithfulGradedAlgebra
import RiemannScope.ExceptionalTransfer
import RiemannScope.FiberArithmetic

set_option linter.unusedVariables false

namespace RiemannScope

/-! ### 1. Support Translation Invariance of Ambient Evaluation -/

/-- Translation of a single power of tau by reference grade K_0:
    tau^K = tau^K_0 * tau^(K - K_0). -/
theorem tau_pow_translation (tau_val : ℝ) (htau : 0 < tau_val) (K K0 : ℝ) :
    tau_val ^ K = tau_val ^ K0 * tau_val ^ (K - K0) := by
  have h_add : K = K0 + (K - K0) := by ring
  nth_rw 1 [h_add]
  exact Real.rpow_add htau K0 (K - K0)

/-- Support translation identity for a 2-term linear combination:
    a1 * tau^K1 + a2 * tau^K2 = tau^K0 * (a1 * tau^(K1 - K0) + a2 * tau^(K2 - K0)). -/
theorem sum_tau_pow_translation_two (tau_val : ℝ) (htau : 0 < tau_val) (K1 K2 K0 a1 a2 : ℝ) :
    a1 * (tau_val ^ K1) + a2 * (tau_val ^ K2) =
    (tau_val ^ K0) * (a1 * (tau_val ^ (K1 - K0)) + a2 * (tau_val ^ (K2 - K0))) := by
  rw [tau_pow_translation tau_val htau K1 K0, tau_pow_translation tau_val htau K2 K0]
  ring

/-- Support translation identity for a 3-term linear combination:
    a1 * tau^K1 + a2 * tau^K2 + a3 * tau^K3 =
    tau^K0 * (a1 * tau^(K1 - K0) + a2 * tau^(K2 - K0) + a3 * tau^(K3 - K0)). -/
theorem sum_tau_pow_translation_three (tau_val : ℝ) (htau : 0 < tau_val)
    (K1 K2 K3 K0 a1 a2 a3 : ℝ) :
    a1 * (tau_val ^ K1) + a2 * (tau_val ^ K2) + a3 * (tau_val ^ K3) =
    (tau_val ^ K0) * (a1 * (tau_val ^ (K1 - K0)) + a2 * (tau_val ^ (K2 - K0)) + a3 * (tau_val ^ (K3 - K0))) := by
  rw [tau_pow_translation tau_val htau K1 K0,
      tau_pow_translation tau_val htau K2 K0,
      tau_pow_translation tau_val htau K3 K0]
  ring

/-- Support translation invariance of the ambient realization kernel (2-term):
    a1 * tau^K1 + a2 * tau^K2 = 0 <==> a1 * tau^(K1 - K0) + a2 * tau^(K2 - K0) = 0. -/
theorem sum_tau_pow_zero_iff_translated_zero_two (tau_val : ℝ) (htau : 0 < tau_val)
    (K1 K2 K0 a1 a2 : ℝ) :
    a1 * (tau_val ^ K1) + a2 * (tau_val ^ K2) = 0 ↔
    a1 * (tau_val ^ (K1 - K0)) + a2 * (tau_val ^ (K2 - K0)) = 0 := by
  have hK0_pos : 0 < tau_val ^ K0 := Real.rpow_pos_of_pos htau K0
  have hK0_ne : tau_val ^ K0 ≠ 0 := ne_of_gt hK0_pos
  rw [sum_tau_pow_translation_two tau_val htau K1 K2 K0 a1 a2]
  constructor
  · intro h
    cases mul_eq_zero.mp h with
    | inl h_zero => exact (hK0_ne h_zero).elim
    | inr h_zero => exact h_zero
  · intro h
    rw [h, mul_zero]

/-- Support translation invariance of the ambient realization kernel (3-term):
    The vanishing of an evaluation sum is invariant under affine grade translation. -/
theorem sum_tau_pow_zero_iff_translated_zero_three (tau_val : ℝ) (htau : 0 < tau_val)
    (K1 K2 K3 K0 a1 a2 a3 : ℝ) :
    a1 * (tau_val ^ K1) + a2 * (tau_val ^ K2) + a3 * (tau_val ^ K3) = 0 ↔
    a1 * (tau_val ^ (K1 - K0)) + a2 * (tau_val ^ (K2 - K0)) + a3 * (tau_val ^ (K3 - K0)) = 0 := by
  have hK0_pos : 0 < tau_val ^ K0 := Real.rpow_pos_of_pos htau K0
  have hK0_ne : tau_val ^ K0 ≠ 0 := ne_of_gt hK0_pos
  rw [sum_tau_pow_translation_three tau_val htau K1 K2 K3 K0 a1 a2 a3]
  constructor
  · intro h
    cases mul_eq_zero.mp h with
    | inl h_zero => exact (hK0_ne h_zero).elim
    | inr h_zero => exact h_zero
  · intro h
    rw [h, mul_zero]

/-! ### 2. Rank-Zero Case: Trivial Coefficient Cancellation -/

/-- Factoring identical grades in rank-zero evaluation (2-term):
    a1 * tau^K0 + a2 * tau^K0 = (a1 + a2) * tau^K0. -/
theorem rank_zero_evaluation_factor (tau_val : ℝ) (K0 a1 a2 : ℝ) :
    a1 * (tau_val ^ K0) + a2 * (tau_val ^ K0) = (a1 + a2) * (tau_val ^ K0) := by
  ring

/-- Exact rank-zero classification:
    When all grades coincide, evaluation vanishes iff the sum of coefficients vanishes.
    This is trivial coefficient cancellation, not a cross-grade kernel relation. -/
theorem rank_zero_kernel_iff (tau_val : ℝ) (htau : 0 < tau_val) (K0 a1 a2 : ℝ) :
    a1 * (tau_val ^ K0) + a2 * (tau_val ^ K0) = 0 ↔ a1 + a2 = 0 := by
  have hK0_pos : 0 < tau_val ^ K0 := Real.rpow_pos_of_pos htau K0
  have hK0_ne : tau_val ^ K0 ≠ 0 := ne_of_gt hK0_pos
  rw [rank_zero_evaluation_factor tau_val K0 a1 a2]
  constructor
  · intro h
    cases mul_eq_zero.mp h with
    | inl h_zero => exact h_zero
    | inr h_zero => exact (hK0_ne h_zero).elim
  · intro h
    rw [h, zero_mul]

/-- Rank-zero classification for 3-term sums with identical grades. -/
theorem rank_zero_kernel_three_iff (tau_val : ℝ) (htau : 0 < tau_val) (K0 a1 a2 a3 : ℝ) :
    a1 * (tau_val ^ K0) + a2 * (tau_val ^ K0) + a3 * (tau_val ^ K0) = 0 ↔ a1 + a2 + a3 = 0 := by
  have hK0_pos : 0 < tau_val ^ K0 := Real.rpow_pos_of_pos htau K0
  have hK0_ne : tau_val ^ K0 ≠ 0 := ne_of_gt hK0_pos
  have h_factor : a1 * (tau_val ^ K0) + a2 * (tau_val ^ K0) + a3 * (tau_val ^ K0) =
                  (a1 + a2 + a3) * (tau_val ^ K0) := by ring
  rw [h_factor]
  constructor
  · intro h
    cases mul_eq_zero.mp h with
    | inl h_zero => exact h_zero
    | inr h_zero => exact (hK0_ne h_zero).elim
  · intro h
    rw [h, zero_mul]

/-! ### 3. Rational Support Rank: Base-Grade Invariance -/

/-- Affine difference shift under base-grade change:
    (K - K0') = (K - K0) - (K0' - K0).
    Therefore every difference relative to K0' lies in the affine translation of differences relative to K0. -/
theorem base_change_linear_span (K K0 K0' : ℝ) :
    K - K0' = (K - K0) - (K0' - K0) := by
  ring

/-- Pairwise difference invariance:
    (K1 - K0') - (K2 - K0') = (K1 - K0) - (K2 - K0).
    Relative differences are strictly independent of the chosen reference grade. -/
theorem support_affine_difference_base_change (K1 K2 K0 K0' : ℝ) :
    (K1 - K0') - (K2 - K0') = (K1 - K0) - (K2 - K0) := by
  ring

/-! ### 4. Rank-One Case: Explicit Kernel Witness and Polynomial Reduction -/

/-- Explicit kernel witness for algebraic generator (alpha ∈ S_tau):
    If tau^alpha = A ∈ Q_bar, then the non-zero element [alpha] - A[0] evaluates to 0. -/
theorem s_tau_explicit_kernel_witness (tau_val : ℝ) (alpha : ℝ) (A : ℝ)
    (hA : tau_val ^ alpha = A) :
    1 * (tau_val ^ alpha) + (-A) * (tau_val ^ (0 : ℝ)) = 0 := by
  rw [Real.rpow_zero, hA]
  ring

/-- Scaled explicit kernel witness for alpha ∈ S_tau with non-zero scalar c. -/
theorem s_tau_explicit_kernel_witness_scaled (tau_val : ℝ) (alpha : ℝ) (A : ℝ)
    (hA : tau_val ^ alpha = A) (c : ℝ) :
    c * (tau_val ^ alpha) + (-c * A) * (tau_val ^ (0 : ℝ)) = 0 := by
  rw [Real.rpow_zero, hA]
  ring

/-- Rank-one injectivity under transcendental generator (alpha ∉ S_tau):
    If tau^alpha is not algebraic, then no non-trivial 2-term linear combination
    c1 * tau^alpha + c0 = 0 with algebraic coefficients (c1 ≠ 0) can vanish. -/
theorem rank_one_injective_of_transcendental_power (tau_val : ℝ) (htau : 0 < tau_val)
    (alpha : ℝ) (isAlg : ℝ → Prop)
    (h_not_alg : ¬ isAlg (tau_val ^ alpha))
    (c0 c1 : ℝ) (hc0_alg : isAlg c0) (hc1_alg : isAlg c1) (hc1_ne : c1 ≠ 0)
    (h_div : ∀ x y, isAlg x → isAlg y → y ≠ 0 → isAlg (x / y))
    (h_neg : ∀ x, isAlg x → isAlg (-x)) :
    c1 * (tau_val ^ alpha) + c0 = 0 → False := by
  intro h_eq
  have h_val : tau_val ^ alpha = -c0 / c1 := by
    have h_c1_tau : c1 * (tau_val ^ alpha) = -c0 := by linarith
    calc tau_val ^ alpha
      _ = (c1 * (tau_val ^ alpha)) / c1 := (mul_div_cancel_left₀ (tau_val ^ alpha) hc1_ne).symm
      _ = -c0 / c1 := by rw [h_c1_tau]
  have h_alg_val : isAlg (tau_val ^ alpha) := by
    rw [h_val]
    exact h_div (-c0) c1 (h_neg c0 hc0_alg) hc1_alg hc1_ne
  exact h_not_alg h_alg_val

/-! ### 5. Group-Algebra Structural Multiplication vs Ambient Kernel -/

/-- Group-algebra exponent addition law:
    tau^K * tau^J = tau^(K + J).
    This is an algebra homomorphism property of ev_tau, not a kernel collapse. -/
theorem group_algebra_mul_law (tau_val : ℝ) (htau : 0 < tau_val) (K J : ℝ) :
    (tau_val ^ K) * (tau_val ^ J) = tau_val ^ (K + J) :=
  (Real.rpow_add htau K J).symm

/-- Structural multiplication relation vanishes identically for all base values:
    tau^(K + J) - tau^K * tau^J = 0.
    In the group algebra, [K][J] = [K + J] is the product definition;
    evaluating this product introduces no additive kernel condition on a Q-basis. -/
theorem group_algebra_mul_relation_is_structural (tau_val : ℝ) (htau : 0 < tau_val) (K J : ℝ) :
    tau_val ^ (K + J) - (tau_val ^ K) * (tau_val ^ J) = 0 := by
  rw [group_algebra_mul_law tau_val htau K J]
  ring

/-! ### 6. Bivariate Laurent Monomial Clearing for Rank-Two Support -/

/-- Factoring a common bivariate monomial clears Laurent shifts:
    For positive X, Y, c * X^(m + Nx) * Y^(n + Ny) = (X^Nx * Y^Ny) * (c * X^m * Y^n). -/
theorem bivariate_monomial_clearing (X Y : ℝ) (hX : 0 < X) (hY : 0 < Y) (c : ℝ) (m n Nx Ny : ℝ) :
    c * (X ^ (m + Nx)) * (Y ^ (n + Ny)) = (X ^ Nx * Y ^ Ny) * (c * (X ^ m) * (Y ^ n)) := by
  rw [Real.rpow_add hX m Nx, Real.rpow_add hY n Ny]
  ring

/-! ### 7. Pairwise Transcendence Insufficiency Abstract Witness -/

/-- Pairwise transcendence does not imply algebraic independence:
    If v = u^2, both u and v can be transcendental, yet they satisfy the polynomial relation
    v - u^2 = 0 over Q. -/
theorem pairwise_transcendence_not_algebraic_independence_model (u v : ℝ) (h_rel : v = u ^ 2) :
    v - u ^ 2 = 0 := by
  rw [h_rel]
  ring

/-- Multiplicative inverse relation:
    If v * u = 1, both numbers can be transcendental, yet they satisfy u * v - 1 = 0 over Q. -/
theorem inverse_pair_algebraic_relation (u v : ℝ) (h_inv : v * u = 1) :
    u * v - 1 = 0 := by
  rw [mul_comm u v, h_inv]
  ring

end RiemannScope
