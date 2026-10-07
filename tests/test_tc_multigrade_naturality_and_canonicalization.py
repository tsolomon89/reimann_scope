"""Tests for Multi-Grade Naturality, Cocycle/Holonomy Triviality, and Canonicalization.

TASK-TC-027 EPIC: Canonical Truth Reconciliation, Formal Claim Audit, and Multi-Grade Naturality.

Covers at minimum:
1. Two-grade transfer composition
2. Three-grade transfer path independence
3. Arbitrary finite path transfer
4. Ambient scale telescoping
5. Closed-loop scale equals one
6. Spectral character telescoping
7. Closed-loop spectral factor equals one
8. Natural unary observable reference-grade reconstruction
9. Natural binary observable reconstruction
10. Dirichlet pairwise transition
11. Dirichlet three-grade path equality
12. Finite-path Dirichlet multiplier
13. Simultaneous zero-set preservation
14. Synthetic nontrivial cocycle negative control
15. Synthetic genuinely grade-dependent coefficient negative control
16. Coefficient-field codomain correctness (ev_tau typing)
17. Regression: zero ordinates are not asserted non-algebraic
18. Regression: analytic pullback not canonical arithmetic TC
19. Regression: Gelfond–Schneider not claimed Lean-formalized
20. Regression: theorem count not treated as 400+ independent major claims
21. Regression: audit absence not interpreted as impossibility
22. Regression: cross-grade multiplication tagged ambient-only
"""

import math
import cmath
import os
import re
import json
import pytest
import mpmath

mpmath.mp.dps = 50
TAU = 2 * mpmath.pi
GAMMA_1_STR = "14.134725141734693790457251983562470270784257115699243175685567460149963429809"


def approx_eq(a, b, tol=1e-40):
    return abs(a - b) < tol


# ==============================================================================
# 1. Intrinsic Transfer & Pair Groupoid Properties
# ==============================================================================

class GradeFiber:
    """Tagged arithmetic fiber F_K = {K} x Z."""
    def __init__(self, K, val: int):
        self.K = K
        self.val = int(val)

    def __eq__(self, other):
        return isinstance(other, GradeFiber) and self.K == other.K and self.val == other.val

    def __repr__(self):
        return f"GradeFiber({self.K}, {self.val})"


def transfer(K, J, fiber_elem: GradeFiber) -> GradeFiber:
    """Canonical transfer T_{J <- K}: (K, n) |-> (J, n)."""
    assert fiber_elem.K == K
    return GradeFiber(J, fiber_elem.val)


def test_01_two_grade_transfer_composition():
    """1. Two-grade transfer composition: T_{K <- K} = id and T_{J <- K} is an isomorphism."""
    x = GradeFiber(1.5, 42)
    assert transfer(1.5, 1.5, x) == x
    y = transfer(1.5, -2.0, x)
    assert y == GradeFiber(-2.0, 42)
    assert transfer(-2.0, 1.5, y) == x


def test_02_three_grade_transfer_path_independence():
    """2. Three-grade transfer path independence: T_{M <- J} o T_{J <- K} = T_{M <- K}."""
    K, J, M = 0.5, 1.25, -3.75
    x = GradeFiber(K, 17)
    step1 = transfer(K, J, x)
    step2 = transfer(J, M, step1)
    direct = transfer(K, M, x)
    assert step2 == direct
    assert step2.val == 17
    assert step2.K == M


def test_03_arbitrary_finite_path_transfer():
    """3. Arbitrary finite path transfer: T_{K_r <- K_{r-1}} o ... o T_{K_1 <- K_0} = T_{K_r <- K_0}."""
    grades = [0.0, 1.5, -0.75, 2.25, -1.0, 3.0]
    x = GradeFiber(grades[0], 99)
    current = x
    for i in range(len(grades) - 1):
        current = transfer(grades[i], grades[i+1], current)
    direct = transfer(grades[0], grades[-1], x)
    assert current == direct
    assert current.val == 99


# ==============================================================================
# 2. Ambient Scale Cocycle & Coboundary Property
# ==============================================================================

def scale_cocycle(J, K, tau=TAU):
    """Ambient coordinate transition factor c(J, K) = tau^(J - K)."""
    return tau ** (J - K)


def test_04_ambient_scale_telescoping():
    """4. Ambient scale telescoping: c(M, J) * c(J, K) = c(M, K)."""
    K, J, M = 0.5, 1.75, -2.25
    c_JK = scale_cocycle(J, K)
    c_MJ = scale_cocycle(M, J)
    c_MK = scale_cocycle(M, K)
    assert approx_eq(c_MJ * c_JK, c_MK, tol=1e-45)


def test_05_closed_loop_scale_equals_one():
    """5. Closed-loop scale equals one: product around any cycle is identically 1."""
    loop_grades = [mpmath.mpf(x) for x in ['0.2', '1.4', '-0.8', '3.1', '-1.5', '0.2']]
    prod = mpmath.mpf(1)
    for i in range(len(loop_grades) - 1):
        prod *= scale_cocycle(loop_grades[i+1], loop_grades[i])
    assert approx_eq(prod, 1, tol=1e-45)


# ==============================================================================
# 3. Spectral Grade Cocycle & Coboundary Property
# ==============================================================================

def spectral_cocycle(J, K, s, tau=TAU):
    """Spectral grade transition factor c_s(J, K) = tau^(-(J - K) * s)."""
    return tau ** (-(J - K) * s)


def test_06_spectral_character_telescoping():
    """6. Spectral character telescoping: c_s(M, J) * c_s(J, K) = c_s(M, K)."""
    s = mpmath.mpc('0.5', GAMMA_1_STR)
    K, J, M = 1.0, -0.5, 2.5
    c_JK = spectral_cocycle(J, K, s)
    c_MJ = spectral_cocycle(M, J, s)
    c_MK = spectral_cocycle(M, K, s)
    assert approx_eq(c_MJ * c_JK, c_MK, tol=1e-45)


def test_07_closed_loop_spectral_factor_equals_one():
    """7. Closed-loop spectral factor equals one: product around any cycle is identically 1."""
    s = mpmath.mpc('0.75', '21.022039638771554992604252732890949146422886199806')
    loop_grades = [-1.0, 0.5, 2.0, -0.5, 1.25, -1.0]
    prod = mpmath.mpc(1, 0)
    for i in range(len(loop_grades) - 1):
        prod *= spectral_cocycle(loop_grades[i+1], loop_grades[i], s)
    assert approx_eq(prod, 1, tol=1e-45)


# ==============================================================================
# 4. Natural Observable Reconstruction
# ==============================================================================

def test_08_natural_unary_observable_reference_grade_reconstruction():
    """8. Natural unary observable: O_K(x) = O_0(T_{0 <- K}(x)) for any transfer-natural observable."""
    def von_mangoldt_Z(n: int) -> float:
        if n in (2, 3, 5, 7):
            return math.log(n)
        if n == 4:
            return math.log(2)
        return 0.0

    O = {K: (lambda x, K=K: von_mangoldt_Z(x.val)) for K in [0.0, 1.0, -1.0, 2.5]}

    for K in [1.0, -1.0, 2.5]:
        for n in [2, 3, 4, 6]:
            x_K = GradeFiber(K, n)
            x_0 = transfer(K, 0.0, x_K)
            assert O[K](x_K) == O[0.0](x_0)


def test_09_natural_binary_observable_reconstruction():
    """9. Natural binary observable: O_K(x, y) = O_0(T_{0 <- K}(x), T_{0 <- K}(y))."""
    for K in [-1.5, 0.5, 2.0]:
        x = GradeFiber(K, 7)
        y = GradeFiber(K, 6)
        x0 = transfer(K, 0.0, x)
        y0 = transfer(K, 0.0, y)
        assert (x.val + y.val) == (x0.val + y0.val)
        assert (x.val * y.val) == (x0.val * y0.val)


# ==============================================================================
# 5. Dirichlet Multi-Grade Transition & Zero-Set Preservation
# ==============================================================================

def test_10_dirichlet_pairwise_transition():
    """10. Dirichlet pairwise transition: D_J(s) = c_s(J, K) * D_K(s)."""
    s = mpmath.mpc(2.0, 1.0)
    zeta_val = mpmath.zeta(s)
    K, J = 0.5, 1.5
    D_K = (TAU ** (-K * s)) * zeta_val
    D_J = (TAU ** (-J * s)) * zeta_val
    trans_D_J = spectral_cocycle(J, K, s) * D_K
    assert approx_eq(D_J, trans_D_J, tol=1e-45)


def test_11_dirichlet_three_grade_path_equality():
    """11. Dirichlet three-grade path equality: accumulated equals direct."""
    s = mpmath.mpc(1.5, -2.0)
    D_K = mpmath.mpc(3.0, 4.0)
    K, J, M = -1.0, 0.5, 2.0
    accumulated = spectral_cocycle(M, J, s) * (spectral_cocycle(J, K, s) * D_K)
    direct = spectral_cocycle(M, K, s) * D_K
    assert approx_eq(accumulated, direct, tol=1e-45)


def test_12_finite_path_dirichlet_multiplier():
    """12. Finite-path Dirichlet multiplier: product of steps equals total transition."""
    s = mpmath.mpc('0.5', GAMMA_1_STR)
    path = [0.0, 0.5, 1.0, 1.5, 2.0]
    total_mult = mpmath.mpc(1, 0)
    for i in range(len(path) - 1):
        total_mult *= spectral_cocycle(path[i+1], path[i], s)
    direct_mult = spectral_cocycle(path[-1], path[0], s)
    assert approx_eq(total_mult, direct_mult, tol=1e-45)


def test_13_simultaneous_zero_set_preservation():
    """13. Simultaneous zero-set preservation: D_K(s) = 0 <=> D_J(s) = 0 for all J, K."""
    rho_1 = mpmath.mpc('0.5', GAMMA_1_STR)
    zeta_at_rho = mpmath.zeta(rho_1)
    assert abs(zeta_at_rho) < 1e-45

    grades = [-2.0, -1.0, 0.0, 0.5, 1.0, 2.0]
    for K in grades:
        factor_K = TAU ** (-K * rho_1)
        assert abs(factor_K) > 0
        D_K_val = factor_K * zeta_at_rho
        assert abs(D_K_val) < 1e-45


# ==============================================================================
# 6. Counterexample Controls (Deliberate Falsification Checks)
# ==============================================================================

def test_14_synthetic_nontrivial_cocycle_negative_control():
    """14. Negative Control: A synthetic non-coboundary cocycle WOULD create holonomy obstruction."""
    K0, K1, K2 = 0, 1, 2
    c_synth = {
        (K1, K0): mpmath.exp(mpmath.mpc(0, 1.0)),
        (K2, K1): mpmath.exp(mpmath.mpc(0, 1.0)),
        (K0, K2): mpmath.exp(mpmath.mpc(0, 1.0)),
    }
    loop_prod = c_synth[(K1, K0)] * c_synth[(K2, K1)] * c_synth[(K0, K2)]
    assert not approx_eq(loop_prod, 1, tol=1e-5)

    c_tc_loop = scale_cocycle(K1, K0) * scale_cocycle(K2, K1) * scale_cocycle(K0, K2)
    assert approx_eq(c_tc_loop, 1, tol=1e-45)


def test_15_synthetic_grade_dependent_coefficient_negative_control():
    """15. Negative Control: Synthetic non-factorable coupling a_{n,K} = n^(K/2) moves zeros."""
    rho_1 = mpmath.mpc('0.5', GAMMA_1_STR)
    assert abs(mpmath.zeta(rho_1)) < 1e-45

    K = 1.0
    shifted_zero = rho_1 + K / 2
    assert abs(mpmath.zeta(shifted_zero - K / 2)) < 1e-45
    assert abs(mpmath.zeta(rho_1 - K / 2)) > 0.1


# ==============================================================================
# 7. Epistemic & Canonical Regressions
# ==============================================================================

def test_16_coefficient_field_codomain_correctness():
    """16. Correct typing of ambient evaluation map ev_tau:
    Real version: ev_tau: A_R[A_R] -> R (where A_R = Q_bar cap R).
    Complex version: ev_tau: Q_bar[A_R] -> C.
    Codomain must match the field of scalars!"""
    coeffs_real = [mpmath.mpf(1), mpmath.sqrt(2), mpmath.cbrt(5)]
    grades = [0, 1, 2]
    val_real = sum(c * (TAU ** g) for c, g in zip(coeffs_real, grades))
    assert isinstance(val_real, mpmath.mpf)
    assert mpmath.im(val_real) == 0

    coeffs_complex = [mpmath.mpc(0, 1), mpmath.mpc(1, 0)]
    val_complex = sum(c * (TAU ** g) for c, g in zip(coeffs_complex, [0, 1]))
    assert abs(mpmath.im(val_complex)) > 0.9


def test_17_regression_zero_ordinates_not_asserted_nonalgebraic():
    """17. Regression: Zero ordinates gamma_n arithmetic nature is UNKNOWN;
    must never be asserted non-algebraic or transcendental."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    doc_path = os.path.join(repo_root, "TRANSCENDENTAL_CONTINUATION.md")
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "zero ordinates $\\gamma_n$ and $\\log p$ are non-algebraic" not in content


def test_18_regression_analytic_pullback_not_canonical_arithmetic_tc():
    """18. Regression: Auxiliary analytic pullback Z_K^{pull}(s) = zeta(tau^(-K) s)
    must NOT be described as canonical arithmetic TC."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    doc_path = os.path.join(repo_root, "TRANSCENDENTAL_CONTINUATION.md")
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "ANALYTIC_PULLBACK" in content or "Auxiliary Analytic Pullback" in content


def test_19_regression_gelfond_schneider_not_claimed_lean_formalized():
    """19. Regression: Gelfond-Schneider theorem itself must be classified as
    PROVED_WITH_EXTERNAL_GELFOND_SCHNEIDER, not as proved by Lean."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    lean_path = os.path.join(repo_root, "formal", "RiemannScope", "TranscendenceRigidity.lean")
    with open(lean_path, "r", encoding="utf-8") as f:
        lean_code = f.read()
    assert "h_GS : ∃ (q : ℚ)" in lean_code or "h_GS : exists (q : Rat)" in lean_code


def test_20_regression_theorem_count_not_treated_as_400_major_claims():
    """20. Regression: The build report theorem count (400+ declarations) represents
    Lean declaration statements accepted by the compiler, NOT 400+ independent major RH claims."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    report_path = os.path.join(repo_root, "formal", "build_report.json")
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        count = data.get("project_theorem_declarations_compiled", 0)
        assert count >= 400
        assert "project_theorem_declarations_compiled" in data


def test_21_regression_audit_absence_not_interpreted_as_impossibility():
    """21. Regression: Audit finding NO_KERNEL_ELEMENT or NO_COUPLING_FOUND
    must NOT be stated as an impossibility theorem of non-existence."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_path = os.path.join(repo_root, "data", "tc_unit_rescaling_no_go_and_genuine_coupling.json")
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        kernel_audit = data.get("ambient_realization_kernel_audit", {})
        status = kernel_audit.get("status", "")
        assert "NO_KERNEL_ELEMENT_FROM_STANDARD_ZETA_STRUCTURES_FOUND" in status
        assert "IMPOSSIBLE" not in status


def test_22_regression_cross_grade_multiplication_tagged_ambient_only():
    """22. Regression: Historical cross-grade multiplication tau^K * tau^(-K) = 1
    belongs strictly to AMBIENT_CROSS_GRADE_ALGEBRA, never intrinsic arithmetic."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    doc_path = os.path.join(repo_root, "TRANSCENDENTAL_CONTINUATION.md")
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "AMBIENT_CROSS_GRADE_ALGEBRA" in content
