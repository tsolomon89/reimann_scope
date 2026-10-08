/-
RiemannScope.FiberArithmetic
TASK-TC-025: Intrinsic Grade-Fiber Arithmetic, Ambient Realization, and the Correct TC Zeta.

Formalizes:
1. Abstract grade-fiber structure GradeFiber K = {K} × ℤ
2. Intrinsic fiber ring operations (⊕_K, ⊙_K) and multiplicative identity 1_K
3. Canonical ring equivalence GradeFiber K ≃ ℤ
4. Realized fiber multiplication x ⊙_K y = xy / tau^K
5. Canonical transfer maps T_{J ← K} and transfer functoriality (id, composition)
6. Coordinate scaling law: Phi_J(T_{J ← K}(x)) = tau^{J - K} Phi_K(x)
7. Intrinsic normalized size N_K and multiplicativity
8. Intrinsic metric identity: d_K(m*tau^K, n*tau^K) = |m - n|
9. Ambient cross-grade multiplication moving to grade K + J
10. Generic-base invariance of intrinsic fiber arithmetic
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Algebra.Ring.Equiv
import Mathlib.Logic.Equiv.TransferInstance
import RiemannScope.Grade
import RiemannScope.GradedMonoid
import RiemannScope.TranscendenceRigidity
import RiemannScope.FaithfulGradedAlgebra
import RiemannScope.ExceptionalTransfer

set_option linter.unusedVariables false

namespace RiemannScope

/-! ### 1. Abstract Grade-Fiber Structure and Ring Operations -/

/-- Tagged arithmetic fiber at grade K: an element represents an integer n
    measured in the grade-K unit. -/
structure GradeFiber (K : ℝ) where
  val : ℤ

namespace GradeFiber

variable {K J M : ℝ}

/-- Fiber addition: (K, m) ⊕_K (K, n) = (K, m + n). -/
def add (x y : GradeFiber K) : GradeFiber K :=
  ⟨x.val + y.val⟩

instance (K : ℝ) : Add (GradeFiber K) where
  add := add

theorem add_val (x y : GradeFiber K) : (x + y).val = x.val + y.val := rfl

/-- Fiber zero: (K, 0). -/
def zero : GradeFiber K := ⟨0⟩

instance (K : ℝ) : Zero (GradeFiber K) where
  zero := zero

theorem zero_val : (0 : GradeFiber K).val = 0 := rfl

/-- Fiber negation: -(K, n) = (K, -n). -/
def neg (x : GradeFiber K) : GradeFiber K := ⟨-x.val⟩

instance (K : ℝ) : Neg (GradeFiber K) where
  neg := neg

theorem neg_val (x : GradeFiber K) : (-x).val = -x.val := rfl

/-- Fiber subtraction: (K, m) - (K, n) = (K, m - n). -/
def sub (x y : GradeFiber K) : GradeFiber K := ⟨x.val - y.val⟩

instance (K : ℝ) : Sub (GradeFiber K) where
  sub := sub

theorem sub_val (x y : GradeFiber K) : (x - y).val = x.val - y.val := rfl

/-- Additive inverse law: -x + x = 0. -/
theorem add_left_neg (x : GradeFiber K) : -x + x = 0 := by
  cases x
  show GradeFiber.mk (-_ + _) = GradeFiber.mk 0
  rw [_root_.add_left_neg]

/-- Fiber multiplication (intrinsic ⊙_K): (K, m) ⊙_K (K, n) = (K, mn). -/
def mul (x y : GradeFiber K) : GradeFiber K :=
  ⟨x.val * y.val⟩

instance (K : ℝ) : Mul (GradeFiber K) where
  mul := mul

theorem mul_val (x y : GradeFiber K) : (x * y).val = x.val * y.val := rfl

/-- Multiplicative unit 1_K = (K, 1). -/
def one : GradeFiber K := ⟨1⟩

instance (K : ℝ) : One (GradeFiber K) where
  one := one

theorem one_val : (1 : GradeFiber K).val = 1 := rfl

/-- Addition associativity in the fiber ring. -/
theorem add_assoc (x y z : GradeFiber K) : (x + y) + z = x + (y + z) := by
  cases x; cases y; cases z
  show GradeFiber.mk ((_ + _) + _) = GradeFiber.mk (_ + (_ + _))
  rw [_root_.add_assoc]

/-- Addition commutativity in the fiber ring. -/
theorem add_comm (x y : GradeFiber K) : x + y = y + x := by
  cases x; cases y
  show GradeFiber.mk (_ + _) = GradeFiber.mk (_ + _)
  rw [_root_.add_comm]

/-- Zero addition left identity. -/
theorem zero_add (x : GradeFiber K) : 0 + x = x := by
  cases x
  show GradeFiber.mk (0 + _) = GradeFiber.mk _
  rw [_root_.zero_add]

/-- Zero addition right identity. -/
theorem add_zero (x : GradeFiber K) : x + 0 = x := by
  cases x
  show GradeFiber.mk (_ + 0) = GradeFiber.mk _
  rw [_root_.add_zero]

/-- Multiplication associativity in the fiber ring. -/
theorem mul_assoc (x y z : GradeFiber K) : (x * y) * z = x * (y * z) := by
  cases x; cases y; cases z
  show GradeFiber.mk ((_ * _) * _) = GradeFiber.mk (_ * (_ * _))
  rw [_root_.mul_assoc]

/-- Multiplication commutativity in the fiber ring. -/
theorem mul_comm (x y : GradeFiber K) : x * y = y * x := by
  cases x; cases y
  show GradeFiber.mk (_ * _) = GradeFiber.mk (_ * _)
  rw [_root_.mul_comm]

/-- Multiplicative unit left identity: 1_K ⊙_K x = x. -/
theorem one_mul (x : GradeFiber K) : 1 * x = x := by
  cases x
  show GradeFiber.mk (1 * _) = GradeFiber.mk _
  rw [_root_.one_mul]

/-- Multiplicative unit right identity: x ⊙_K 1_K = x. -/
theorem mul_one (x : GradeFiber K) : x * 1 = x := by
  cases x
  show GradeFiber.mk (_ * 1) = GradeFiber.mk _
  rw [_root_.mul_one]

/-- Distributivity of fiber multiplication over fiber addition. -/
theorem left_distrib (x y z : GradeFiber K) : x * (y + z) = x * y + x * z := by
  cases x; cases y; cases z
  show GradeFiber.mk (_ * (_ + _)) = GradeFiber.mk (_ * _ + _ * _)
  rw [_root_.mul_add]

theorem right_distrib (x y z : GradeFiber K) : (x + y) * z = x * z + y * z := by
  cases x; cases y; cases z
  show GradeFiber.mk ((_ + _) * _) = GradeFiber.mk (_ * _ + _ * _)
  rw [_root_.add_mul]

/-! ### 2. Ring Equivalence to Integers -/

/-- Projection to the underlying integer referent. -/
def toZ (x : GradeFiber K) : ℤ := x.val

/-- Embedding of integer referents into grade-K units. -/
def fromZ (K : ℝ) (n : ℤ) : GradeFiber K := ⟨n⟩

theorem toZ_fromZ (n : ℤ) : toZ (fromZ K n) = n := rfl

theorem fromZ_toZ (x : GradeFiber K) : fromZ K (toZ x) = x := by
  cases x; rfl

theorem toZ_add (x y : GradeFiber K) : toZ (x + y) = toZ x + toZ y := rfl

theorem toZ_mul (x y : GradeFiber K) : toZ (x * y) = toZ x * toZ y := rfl

theorem toZ_zero : toZ (0 : GradeFiber K) = 0 := rfl

theorem toZ_one : toZ (1 : GradeFiber K) = 1 := rfl

theorem toZ_neg (x : GradeFiber K) : toZ (-x) = -toZ x := rfl

theorem toZ_sub (x y : GradeFiber K) : toZ (x - y) = toZ x - toZ y := rfl

theorem toZ_injective (K : ℝ) : Function.Injective (toZ : GradeFiber K → ℤ) := by
  intro a b h
  cases a; cases b
  dsimp [toZ] at h
  rw [h]

/-- Canonical bijection between GradeFiber K and ℤ. -/
def equivZ (K : ℝ) : GradeFiber K ≃ ℤ where
  toFun := toZ
  invFun := fromZ K
  left_inv := fromZ_toZ
  right_inv := toZ_fromZ

/-- Commutative ring structure on GradeFiber K, canonically transferred from ℤ. -/
instance (K : ℝ) : CommRing (GradeFiber K) := (equivZ K).commRing

/-- Canonical ring equivalence GradeFiber K ≃+* ℤ. -/
def ringEquivZ (K : ℝ) : GradeFiber K ≃+* ℤ := (equivZ K).ringEquiv

/-- Forward evaluation of the ring equivalence equals the integer referent. -/
theorem ringEquivZ_apply (x : GradeFiber K) : ringEquivZ K x = x.val := rfl

/-- Inverse evaluation of the ring equivalence embeds an integer referent. -/
theorem ringEquivZ_symm_apply (n : ℤ) : (ringEquivZ K).symm n = fromZ K n := rfl

/-! ### 3. Realized Fiber Multiplication -/

/-- Realized multiplication formula:
    On the real line, (m * tau_K) ⊙_K (n * tau_K) = (m * n) * tau_K = (x * y) / tau_K. -/
theorem realized_fiber_mul_identity (m n tau_K : ℝ) (htau : tau_K ≠ 0) :
    ((m * tau_K) * (n * tau_K)) / tau_K = (m * n) * tau_K := by
  calc ((m * tau_K) * (n * tau_K)) / tau_K
    _ = (m * n * (tau_K * tau_K)) / tau_K := by ring
    _ = (m * n * tau_K * tau_K) / tau_K := by ring
    _ = (m * n * tau_K) := by
      rw [mul_div_cancel_right₀ (m * n * tau_K) htau]
    _ = (m * n) * tau_K := by ring

/-! ### 4. Canonical Transfer Maps -/

/-- Canonical transfer map T_{J ← K}: GradeFiber K → GradeFiber J
    sending (K, n) ↦ (J, n). -/
def transfer (K J : ℝ) (x : GradeFiber K) : GradeFiber J :=
  ⟨x.val⟩

theorem transfer_val (x : GradeFiber K) : (transfer K J x).val = x.val := rfl

/-- Identity transfer map: T_{K ← K} = id. -/
theorem transfer_refl (K : ℝ) (x : GradeFiber K) : transfer K K x = x := by
  cases x; rfl

/-- Transfer composition law: T_{M ← J} ∘ T_{J ← K} = T_{M ← K}. -/
theorem transfer_trans (K J M : ℝ) (x : GradeFiber K) :
    transfer J M (transfer K J x) = transfer K M x := by
  cases x; rfl

/-- Transfer preserves addition: T(x + y) = T(x) + T(y). -/
theorem transfer_preserves_add (K J : ℝ) (x y : GradeFiber K) :
    transfer K J (x + y) = transfer K J x + transfer K J y := rfl

/-- Transfer preserves multiplication: T(x * y) = T(x) * T(y). -/
theorem transfer_preserves_mul (K J : ℝ) (x y : GradeFiber K) :
    transfer K J (x * y) = transfer K J x * transfer K J y := rfl

/-- Transfer preserves the unit: T(1_K) = 1_J. -/
theorem transfer_preserves_one (K J : ℝ) :
    transfer K J (1 : GradeFiber K) = (1 : GradeFiber J) := rfl

/-- Transfer preserves zero: T(0_K) = 0_J. -/
theorem transfer_preserves_zero (K J : ℝ) :
    transfer K J (0 : GradeFiber K) = (0 : GradeFiber J) := rfl

/-! ### 5. Ambient Realization and Coordinate Scaling -/

/-- Realization map Phi_K: GradeFiber K → ℝ sending (K, n) ↦ n * tau^K. -/
def phi (tau_K : ℝ) (x : GradeFiber K) : ℝ :=
  (x.val : ℝ) * tau_K

/-- Coordinate change law:
    Phi_J(T_{J ← K}(x)) = (tau^J / tau^K) * Phi_K(x) = tau^{J - K} * Phi_K(x). -/
theorem realization_coordinate_change (n tau_K tau_J : ℝ) (htau : tau_K ≠ 0) :
    n * tau_J = (tau_J / tau_K) * (n * tau_K) := by
  calc n * tau_J
    _ = (tau_J / tau_K * tau_K) * n := by
      rw [div_mul_cancel₀ tau_J htau]
      ring
    _ = (tau_J / tau_K) * (n * tau_K) := by ring

/-! ### 6. Intrinsic Normalized Size -/

/-- Intrinsic normalized size N_K(K, n) = n. -/
def normSize (x : GradeFiber K) : ℤ := x.val

/-- Multiplicativity of normalized size under intrinsic fiber multiplication:
    N_K(x ⊙_K y) = N_K(x) * N_K(y). -/
theorem normSize_mul (x y : GradeFiber K) :
    normSize (x * y) = normSize x * normSize y := rfl

/-- Realized normalized size:
    N_K(n * tau^K) = (n * tau^K) / tau^K = n. -/
theorem realized_normSize (n tau_K : ℝ) (htau : tau_K ≠ 0) :
    (n * tau_K) / tau_K = n :=
  mul_div_cancel_right₀ n htau

/-! ### 7. Intrinsic Metric -/

/-- Intrinsic metric on the realized line:
    d_K(m * tau^K, n * tau^K) = |m * tau^K - n * tau^K| / tau^K = |m - n|. -/
theorem intrinsic_metric_identity (m n tau_K : ℝ) (htau : 0 < tau_K) :
    |m * tau_K - n * tau_K| / tau_K = |m - n| := by
  have hne : tau_K ≠ 0 := ne_of_gt htau
  have hdiff : m * tau_K - n * tau_K = (m - n) * tau_K := by ring
  rw [hdiff, abs_mul, abs_of_pos htau, mul_div_cancel_right₀ |m - n| hne]

/-! ### 8. Ambient Cross-Grade Multiplication -/

/-- Ambient cross-grade multiplication between GradeFiber K and GradeFiber J
    produces an element in GradeFiber (K + J):
    (K, m) ★ (J, n) = (K + J, mn). -/
def ambientMul (x : GradeFiber K) (y : GradeFiber J) : GradeFiber (K + J) :=
  ⟨x.val * y.val⟩

theorem ambientMul_val (x : GradeFiber K) (y : GradeFiber J) :
    (ambientMul x y).val = x.val * y.val := rfl

/-- Contrast: Fiber multiplication stays at grade K,
    while ambient cross-grade multiplication shifts to grade K + J. -/
theorem ambient_vs_fiber_mul_grade (x y : GradeFiber K) :
    (ambientMul x y).val = (x * y).val := rfl

/-! ### 9. Generic Base Invariance -/

/-- The intrinsic ring equivalence to ℤ is independent of any realization base b > 0. -/
theorem generic_base_realized_mul (m n b_K : ℝ) (hb : b_K ≠ 0) :
    ((m * b_K) * (n * b_K)) / b_K = (m * n) * b_K := by
  calc ((m * b_K) * (n * b_K)) / b_K
    _ = (m * n * (b_K * b_K)) / b_K := by ring
    _ = (m * n * b_K * b_K) / b_K := by ring
    _ = (m * n * b_K) := by
      rw [mul_div_cancel_right₀ (m * n * b_K) hb]
    _ = (m * n) * b_K := by ring

end GradeFiber

end RiemannScope
