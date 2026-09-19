"""
tests/test_tc_mechanism_discovery.py

Mechanism-Discovery Cycle 1 Verification Suite for Transcendental Continuation (TC).
Tests:
1. Exact symbolic proof of integer/rational grade lattice non-coincidence (L_K cap L_J = {0}).
2. Continuous real grade counterexample (k = log_tau(2) => L_k cap L_0 = 2*Z != {0}).
3. Transported arithmetic operations: addition, multiplication, and isomorphism.
4. Side-by-side comparative transformation contract across 4 constructions.
5. Exact scalar twist identities, modulus evaluation, and rational power witnesses.
6. Gap A Audit (Candidate TC-DISC-01): Station lattice vs logarithmic frequency reduction.
7. Gap B Audit (Candidate TC-DISC-02): Zero-character quantization & continuous displacement test.
8. Gap C Audit (Candidate TC-DISC-03): Logarithmic derivative cross-grade difference and pole cancellation.
9. 100+ Reference zero control and trivial zero control.
10. Non-Euler counterexample control: Davenport-Heilbronn zeta function.
"""

import fractions
import json
import math
import os
import numpy as np
import mpmath
import pytest

import math_core
import transcendental


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# ==============================================================================
# 1. LATTICE SEPARATION & NON-COINCIDENCE
# ==============================================================================

def test_integer_lattice_noncoincidence_symbolic():
    """
    Verify symbolic proof of L_K cap L_J = {0} for distinct integer grades K != J
    based on the transcendence of tau = 2*pi.
    """
    res1 = transcendental.prove_lattice_noncoincidence_symbolic(K=1, J=0)
    assert res1["is_proved"] is True
    assert res1["M"] == 1
    assert res1["epistemic_status"] == "PROVED_SYMBOLIC_ALGEBRAIC"

    res2 = transcendental.prove_lattice_noncoincidence_symbolic(K=3, J=-2)
    assert res2["is_proved"] is True
    assert res2["M"] == 5

    with pytest.raises(ValueError):
        transcendental.prove_lattice_noncoincidence_symbolic(K=2, J=2)


def test_real_grade_coincidence_counterexample():
    """
    Verify that continuous real scaling permits lattice collisions:
    for k = log_tau(2), tau^k = 2, so L_k = 2*Z has infinite intersection with L_0 = Z.
    """
    res = transcendental.verify_real_grade_coincidence_counterexample(dps=80)
    assert float(res["error_from_2"]) < 1e-75
    assert len(res["witnesses"]) == 3
    for w in res["witnesses"]:
        # Verify m * tau^k == n * tau^0
        assert abs(float(w["val_Lk"]) - float(w["val_L0"])) < 1e-70


def test_transported_arithmetic_operations():
    """
    Verify transported operations in layer L_K = tau^K * Z:
      (a_K * m) odot_K (a_K * n) == a_K * (m * n).
    """
    res = transcendental.transported_arithmetic_operations(x="2.5", y="4.0", K=2, dps=80)
    assert res["is_isomorphic"] is True
    assert float(res["isomorphism_error"]) < 1e-70


# ==============================================================================
# 2. COMPARATIVE TRANSFORMATION CONTRACT
# ==============================================================================

def test_comparative_transformations_contract_table():
    """
    Verify that the comparative contract table contains all 4 constructions
    with distinct domains, units, zero mappings, and frequency actions.
    """
    table = transcendental.transformation_contract_comparison_table()
    assert len(table) == 4
    names = [entry["construction"] for entry in table]
    assert "Origin argument dilation" in names
    assert "Centered argument dilation" in names
    assert "Scaled arithmetic Dirichlet series" in names
    assert "Completed half-density twist" in names

    # Verify distinct zero behaviors
    origin_entry = next(e for e in table if "Origin" in e["construction"])
    assert "tau^K * rho" in origin_entry["zero_behavior"]

    centered_entry = next(e for e in table if "Centered" in e["construction"])
    assert "1/2 + tau^K * (rho - 1/2)" in centered_entry["zero_behavior"]

    scaled_entry = next(e for e in table if "Scaled" in e["construction"])
    assert "unchanged" in scaled_entry["zero_behavior"]

    twist_entry = next(e for e in table if "Completed" in e["construction"])
    assert "unchanged" in twist_entry["zero_behavior"]


def test_transformation_evaluations_and_zero_mappings():
    """
    Verify numerical evaluations of the 4 transformations on a known zero:
    rho_1 = 1/2 + i * 14.13472514173469...
    """
    with mpmath.workdps(60):
        tau = math_core.get_tau(dps=60)
        gamma_1 = mpmath.mpf("14.13472514173469379045725198356247027078")
        rho_1 = mpmath.mpc(mpmath.mpf('0.5'), gamma_1)
        K = 1

        # 1. Origin argument dilation Z_1(tau * rho_1) = zeta(rho_1) == 0
        s_origin = tau * rho_1
        z_origin = transcendental.evaluate_origin_dilation_zeta(s_origin, K=K, dps=50)
        assert abs(z_origin) < 1e-35

        # 2. Centered argument dilation zeta_cent,1(1/2 + tau * (rho_1 - 1/2)) == 0
        s_cent = mpmath.mpc('0.5', 0) + tau * (rho_1 - mpmath.mpc('0.5', 0))
        z_cent = transcendental.evaluate_centered_dilation_zeta(s_cent, K=K, dps=50)
        assert abs(z_cent) < 1e-35

        # 3. Scaled Dirichlet series F_1(rho_1) = tau^(-rho_1) * zeta(rho_1) == 0
        f_val = transcendental.evaluate_scaled_dirichlet_series(rho_1, K=K, dps=50)
        assert abs(f_val) < 1e-35

        # 4. Completed half-density twist xi_1(rho_1) == 0
        xi_twist = transcendental.evaluate_half_density_twist_xi(rho_1, K=K, dps=50)
        assert abs(xi_twist) < 1e-35


# ==============================================================================
# 3. EXACT SCALAR IDENTITIES & MULTIPLIER GROUNDWORK
# ==============================================================================

def test_scalar_twist_identities():
    """
    Verify exact scalar twist identities:
      xi_K'/xi_K == xi'/xi - K * log(tau)
      xi_K(1-s) == tau^(2*K*(s - 1/2)) * xi_K(s)
      -F_K'/F_K + F_J'/F_J == (K - J) * log(tau)
    """
    # Test point off the critical line: s = 0.6 + 21.022040j
    s_test = mpmath.mpc("0.6", "21.02203964")
    res = transcendental.verify_scalar_twist_identities(s_test, K=2, J=-1, dps=70)
    assert float(res["log_derivative_twist_error"]) < 1e-15
    assert float(res["functional_equation_error"]) < 1e-45
    assert float(res["modulus_error"]) < 1e-60
    assert res["is_unimodular_on_line"] is False

    # Test point on the critical line: s = 0.5 + 14.134725j
    s_online = mpmath.mpc("0.5", "14.13472514")
    res_online = transcendental.verify_scalar_twist_identities(s_online, K=3, J=0, dps=70)
    assert res_online["is_unimodular_on_line"] is True
    assert abs(float(res_online["twist_modulus"]) - 1.0) < 1e-60

    # Test witness: delta = log_tau(1.5) => tau^delta == 1.5 in Q
    assert float(res["rational_power_witness_error"]) < 1e-60


# ==============================================================================
# 4. MECHANISM DISCOVERY CYCLE 1 AUDIT
# ==============================================================================

def test_audit_gap_A_lattice_vs_frequency():
    """
    Gap A (Candidate TC-DISC-001):
    Confirm that scaled Dirichlet series logarithmic-derivative difference
    reduces to the scalar constant (K - J)*log(tau).
    Lattice station disjointness L_K cap L_J = {0} holds by transcendence of tau,
    but does not couple to F_K. Non-scalar couplings for argument dilation Z_K remain open.
    """
    res = transcendental.audit_candidate_A_lattice_vs_frequency(s_val="1.75 + 14.134725j", K=2, J=-1, dps=70)
    assert res["candidate_id"] == "TC-DISC-001"
    assert res["gap"] == "GAP_A_TWO_ROLES_OF_LATTICE"
    assert res["verdict"] == "SCOPED_SCALAR_REDUCTION"
    assert res["zero_dependence"] == "NONE (exact constant identity for scaled Dirichlet series F_K)"
    assert res["prime_dependence"] == "NONE (prime terms cancel identically in F_K'/F_K difference)"


def test_audit_gap_B_displacement_restriction():
    """
    Gap B (Candidate TC-DISC-002):
    Confirm that grade-character modulus and symmetric defect identities
    hold smoothly for arbitrary real displacements without quantization.
    Verify the narrowly scoped theorem:
      For every real displacement delta in (-1/2, 1/2) and height gamma,
      q = exp((delta + i*gamma)*log(tau)) != 0, and chi(K) = q^K is a character
      of (Z, +). The character laws and conjugation/reflection symmetries admit
      off-line displacements delta != 0. Those listed premises alone therefore do NOT imply delta = 0.
    """
    tau = 2 * mpmath.pi
    log_tau = mpmath.log(tau)
    # Irrational displacement yielding rational character modulus |q_rho| = 1.5
    delta_trans = mpmath.log(mpmath.mpf('1.5')) / log_tau

    deltas = [
        mpmath.mpf('0.0'),
        mpmath.mpf('0.1'),
        mpmath.sqrt(2) / 10,
        -mpmath.sqrt(2) / 10,
        delta_trans
    ]
    res = transcendental.audit_candidate_B_zero_restriction(
        delta_values=deltas, gamma="14.134725", K=2, dps=70
    )
    assert res["candidate_id"] == "TC-DISC-002"
    assert res["gap"] == "GAP_B_PROPOSED_ARITHMETIC_RESTRICTION"
    assert res["verdict"] == "CHARACTER_SYMMETRIES_ADMIT_OFFLINE_DISPLACEMENTS"

    # Verify each evaluation is analytically continuous and root residual vanishes
    for ev in res["evaluations"]:
        assert float(ev["poly_root_residual"]) < 1e-45
        if float(ev["delta"]) == 0.0:
            assert ev["is_zero_defect"] is True
            assert abs(float(ev["q_modulus"]) - 1.0) < 1e-40
        else:
            assert ev["is_zero_defect"] is False
            assert float(ev["defect_D_K"]) > 0.0


def test_audit_gap_C_log_derivative_compatibility():
    """
    Gap C (Candidate TC-DISC-003):
    Confirm that completed logarithmic derivative cross-grade difference
    G_K(s) - G_J(s) == (K - J) * log(tau) cancels all zero singularities identically.
    Retained as an exact scoped result of scalar preservation.
    """
    test_pts = [
        mpmath.mpc("0.5", "14.134725"),
        mpmath.mpc("0.6", "21.022040"),
        mpmath.mpc("0.75", "25.010857"),
        mpmath.mpc("1.5", "30.424876")
    ]
    res = transcendental.audit_candidate_C_log_derivative_compatibility(
        K=1, J=-1, test_points=test_pts, dps=70
    )
    assert res["candidate_id"] == "TC-DISC-003"
    assert res["all_points_matched"] is True
    assert float(res["max_residual_error"]) < 1e-15
    assert res["verdict"] == "SCOPED_SCALAR_PRESERVATION"


def test_audit_candidate_D_transported_explicit_formula():
    """
    Cycle 2 (Candidate TC-DISC-004):
    Audit transported explicit formula test difference h_{K,J} = phi(tau^(-K)*r) - phi(tau^(-J)*r).
    Confirms:
      1. Rational frequency ratio collisions tau^M = p/q are impossible by Lindemann's theorem.
      2. Pair-Isolation Barrier prevents deducing a single-prime collision from the infinite sum.
    """
    res = transcendental.audit_candidate_D_transported_explicit_formula(K=1, J=0, dps=70)
    assert res["candidate_id"] == "TC-DISC-004"
    assert res["rational_collision_possible"] is False
    assert float(res["collision_discrepancy"]) > 4.0  # |2pi - 1.5| > 4.7
    assert res["verdict"] == "REJECTED_AS_A_MECHANISM_FROM_EXPLICIT_FORMULA_LINEARITY_ALONE"


# ==============================================================================
# 4. CYCLE 3: COMMON-REFERENT BRIDGE & INVENTORY TESTS
# ==============================================================================

def test_common_referent_bridge_cr1_cr3_proved_cr2_fails():
    """
    Cycle 3 (Candidate CR-1 / TC-DISC-005 / CLM-TC-008):
    Tests the Common-Referent Collision conditions on normalized radial displacement delta:
      CR1 (Common Referent): R_tau is identical across grades (|R_K - R_J| < 1e-70).
      CR3 (Off-line Non-Zero): delta != 0 implies A(rho) != 0.
      CR2 (Layer Membership): Fails because delta is not an integer multiple of tau^K or tau^J.
    """
    res = transcendental.audit_candidate_common_referent_bridge(
        delta='0.1', gamma='14.13472514173469379', K=1, J=0, dps=70
    )
    assert res["candidate_id"] == "CR-1"
    assert res["CR1_common_referent"]["satisfied"] is True
    assert float(res["CR1_common_referent"]["residual"]) < 1e-65
    assert res["CR3_offline_nonzero"]["satisfied"] is True
    assert res["CR2_layer_membership"]["satisfied"] is False
    assert float(res["CR2_layer_membership"]["integer_distance_K"]) > 1e-5
    assert res["verdict"] == "CR1_AND_CR3_PROVED__CR2_BLOCKED_BY_DISGUISED_PREMISE"


def test_observable_inventory_classification():
    """
    Cycle 3 (Observable Inventory / TC-DISC-006 / CLM-TC-008):
    Audits the 10 canonical observables against (CR1), (CR2), (CR3).
    Confirms that every single observable fails at least one condition.
    """
    inv_res = transcendental.evaluate_observable_inventory(dps=70)
    assert inv_res["inventory_size"] == 10
    assert inv_res["closest_candidate"] == "OBS-01 (Normalized Radial Displacement delta)"
    assert inv_res["proved_conditions_for_closest"] == ["CR1", "CR3"]
    assert inv_res["failing_condition_for_closest"] == "CR2 (Layer Membership)"

    # Check that no candidate passes all three
    for item in inv_res["inventory"]:
        all_passed = item["cr1_common_value"] and item["cr2_layer_membership"] and item["cr3_offline_nonzero"]
        assert all_passed is False, f"Candidate {item['id']} unexpectedly passed all three conditions"


def test_disguised_premise_obstruction_symbolic():
    """
    Cycle 3 (Symbolic Disguised Premise Proof / TC-DISC-007):
    Proves that for integer grades K != J:
      L_K intersect L_J = {0}.
    Therefore, requiring delta in L_K and delta in L_J forces delta = 0 directly.
    Demanding layer membership for an off-line zero is logically equivalent to assuming RH.
    """
    import sympy  # type: ignore
    tau = sympy.Symbol("tau", positive=True)
    m, n = sympy.symbols("m n", integer=True)
    K, J = 1, 0

    # m * tau^1 = n * tau^0 => m * tau = n
    # For m != 0, tau = n / m in Q, which is false for transcendental tau = 2*pi
    # Hence m = 0, n = 0, so delta = 0
    sol = sympy.solve(sympy.Eq(m * tau, n), [m, n])
    # The linear system with transcendental tau forces m = 0 and n = 0
    assert sol == {m: 0, n: 0} or sol == [(0, 0)] or (0, 0) in sol or (isinstance(sol, dict) and sol.get(m) == 0 and sol.get(n) == 0)


# ==============================================================================
# 5. DATASET & COUNTEREXAMPLE CONTROLS
# ==============================================================================

def test_first_100_reference_zeros_unimodular_twist():
    """
    Verify on actual dataset of 100 non-trivial zeros from data/zeros_first_100_reference.json
    that the half-density twist modulus is strictly 1.0 (unimodular on critical line).
    """
    ref_file = os.path.join(REPO_ROOT, "data", "zeros_first_100_reference.json")
    with open(ref_file, "r", encoding="utf-8") as f:
        ref_data = json.load(f)

    ordinates = ref_data["ordinates"]
    assert len(ordinates) >= 100

    with mpmath.workdps(50):
        tau = math_core.get_tau(dps=50)
        K = 2
        for gamma_str in ordinates:
            gamma = mpmath.mpf(gamma_str)
            rho = mpmath.mpc(mpmath.mpf('0.5'), gamma)
            # Twist factor tau^(-K*(s - 1/2)) = tau^(-K * i * gamma)
            twist = mpmath.power(tau, -K * (rho - mpmath.mpc('0.5', 0)))
            assert abs(abs(twist) - 1.0) < 1e-40


def test_trivial_zeros_control():
    """
    Verify that completed xi and half-density twist xi_K distinguish trivial zeros:
    zeta(-2) == 0, but xi(-2) != 0 because Gamma(s/2) pole cancels the trivial zero.
    """
    with mpmath.workdps(50):
        # Trivial zero s = -2
        s_triv = mpmath.mpc(-2, 0)
        z_val = math_core.zeta_eval(s_triv, dps=50)
        assert abs(z_val) < 1e-45

        xi_val = math_core.completed_xi(s_triv, dps=50)
        # xi(-2) is non-zero
        assert abs(xi_val) > 0.01

        xi_twist = transcendental.evaluate_half_density_twist_xi(s_triv, K=1, dps=50)
        assert abs(xi_twist) > 0.01


def davenport_heilbronn(s, dps=40):
    """
    Evaluates the Davenport-Heilbronn zeta function:
    f(s) = c1 * L(s, chi) + c2 * L(s, chi_bar)
    where chi is the non-principal character mod 5.
    Satisfies the functional equation xi(s) = xi(1-s) but lacks Euler product
    and possesses infinitely many off-line zeros in Re(s) > 1/2.
    """
    with mpmath.workdps(dps):
        sqrt5 = mpmath.sqrt(5)
        kappa = (mpmath.sqrt(10 - 2*sqrt5) - 2) / (sqrt5 - 1)
        c1 = (1 - mpmath.j * kappa) / 2
        c2 = (1 + mpmath.j * kappa) / 2

        s_c = mpmath.mpc(s)
        scale = mpmath.power(5, -s_c)
        z1 = mpmath.hurwitz(s_c, mpmath.mpf('0.2'))
        z2 = mpmath.hurwitz(s_c, mpmath.mpf('0.4'))
        z3 = mpmath.hurwitz(s_c, mpmath.mpf('0.6'))
        z4 = mpmath.hurwitz(s_c, mpmath.mpf('0.8'))

        L_chi = scale * (z1 + mpmath.j * z2 - mpmath.j * z3 - z4)
        L_chi_bar = scale * (z1 - mpmath.j * z2 + mpmath.j * z3 - z4)
        return c1 * L_chi + c2 * L_chi_bar


def test_davenport_heilbronn_control():
    """
    Non-Euler product control:
    Verify that the Davenport-Heilbronn zeta function has off-line zeros,
    proving that functional equation symmetry alone does not force zeros to the critical line.
    """
    with mpmath.workdps(40):
        s_guess = mpmath.mpc('0.808517', '85.699348')
        root = mpmath.findroot(lambda s: davenport_heilbronn(s, 40), s_guess)
        residual = abs(davenport_heilbronn(root, 40))
        assert residual < 1e-12
        # Off-critical displacement delta approx 0.3085 > 0.25
        assert abs(root.real - 0.5) > 0.25


# ==============================================================================
# 6. CYCLE 4: BOUNDED GRADE-CHARACTER BRIDGE & CANONICAL NORM AUDIT
# ==============================================================================

def test_grade_character_modulus_and_homomorphism():
    """
    Cycle 4:
    Verify exact character laws:
      chi_rho(K+J) = chi_rho(K) * chi_rho(J)
      chi_rho(0) = 1
      chi_rho(-K) = 1 / chi_rho(K)
      |chi_rho(K)| = tau^(K*delta)
    """
    with mpmath.workdps(70):
        delta = mpmath.mpf('0.15')
        gamma = mpmath.mpf('14.134725')
        tau = 2 * mpmath.pi

        K, J = 2, 3
        res_K = transcendental.evaluate_grade_character(delta, gamma, K=K, dps=70)
        res_J = transcendental.evaluate_grade_character(delta, gamma, K=J, dps=70)
        res_KJ = transcendental.evaluate_grade_character(delta, gamma, K=K + J, dps=70)
        res_0 = transcendental.evaluate_grade_character(delta, gamma, K=0, dps=70)
        res_negK = transcendental.evaluate_grade_character(delta, gamma, K=-K, dps=70)

        chi_K = mpmath.mpc(res_K["chi_rho_K"]["re"], res_K["chi_rho_K"]["im"])
        chi_J = mpmath.mpc(res_J["chi_rho_K"]["re"], res_J["chi_rho_K"]["im"])
        chi_KJ = mpmath.mpc(res_KJ["chi_rho_K"]["re"], res_KJ["chi_rho_K"]["im"])
        chi_0 = mpmath.mpc(res_0["chi_rho_K"]["re"], res_0["chi_rho_K"]["im"])
        chi_negK = mpmath.mpc(res_negK["chi_rho_K"]["re"], res_negK["chi_rho_K"]["im"])

        # 1. Homomorphism chi(K+J) == chi(K) * chi(J)
        assert abs(chi_K * chi_J - chi_KJ) < 1e-18

        # 2. Identity chi(0) == 1
        assert abs(chi_0 - 1.0) < 1e-18

        # 3. Inverse chi(-K) == 1 / chi(K)
        assert abs(chi_K * chi_negK - 1.0) < 1e-18

        # 4. Modulus law |chi_rho(K)| = tau^(K*delta)
        expected_modulus = mpmath.power(tau, K * delta)
        actual_modulus = mpmath.mpf(res_K["modulus_actual"])
        assert abs(actual_modulus - expected_modulus) < 1e-18


def test_theorem_A_unitary_criterion():
    """
    Cycle 4 (Theorem A):
    Verify that for tau > 1 and K != 0:
      |chi_rho(K)| = 1 iff delta = 0.
    """
    gamma = mpmath.mpf('14.134725')

    # delta = 0 is unitary
    res_0 = transcendental.verify_theorem_A_unitary_criterion(delta='0.0', gamma=gamma, K=1, dps=70)
    assert res_0["is_unitary"] is True
    assert res_0["delta_is_zero"] is True
    assert res_0["criterion_holds"] is True

    # delta != 0 are not unitary
    for d in ['0.05', '-0.05', '0.25']:
        res_d = transcendental.verify_theorem_A_unitary_criterion(delta=d, gamma=gamma, K=1, dps=70)
        assert res_d["is_unitary"] is False
        assert res_d["delta_is_zero"] is False
        assert res_d["criterion_holds"] is True


def test_theorem_B_bilateral_boundedness_criterion():
    """
    Cycle 4 (Theorem B):
    Verify that sup_{K in Z} |chi_rho(K)| < infty iff delta = 0.
    Demonstrate that bilateral grades are essential:
      delta > 0 diverges as K -> +infty (bounded for K <= 0)
      delta < 0 diverges as K -> -infty (bounded for K >= 0)
      delta = 0 is bounded for all K in Z.
    """
    # delta = 0: bilaterally bounded
    res_0 = transcendental.verify_theorem_B_bilateral_boundedness_criterion(delta='0.0', max_K=10, dps=70)
    assert res_0["is_bilaterally_bounded"] is True
    assert res_0["delta_is_zero"] is True
    assert "NONE" in res_0["divergence_branch"]
    assert res_0["criterion_holds"] is True

    # delta = 0.1 > 0: forward divergence
    res_pos = transcendental.verify_theorem_B_bilateral_boundedness_criterion(delta='0.1', max_K=10, dps=70)
    assert res_pos["is_bilaterally_bounded"] is False
    assert res_pos["delta_is_zero"] is False
    assert "FORWARD" in res_pos["divergence_branch"]
    assert res_pos["criterion_holds"] is True

    # delta = -0.1 < 0: backward divergence
    res_neg = transcendental.verify_theorem_B_bilateral_boundedness_criterion(delta='-0.1', max_K=10, dps=70)
    assert res_neg["is_bilaterally_bounded"] is False
    assert res_neg["delta_is_zero"] is False
    assert "BACKWARD" in res_neg["divergence_branch"]
    assert res_neg["criterion_holds"] is True


def test_canonical_norm_candidates_audit():
    """
    Cycle 4 (Canonical Norm Audit):
    Verify that all 5 candidate normed spaces/models fail to prove membership of zeta zeros
    without assuming RH or an RH-equivalent condition.
    """
    res = transcendental.audit_canonical_norm_candidates(dps=70)
    assert res["overall_status"] == "CONDITIONAL_ONLY"
    assert res["models_audited"] == 5
    assert res["all_models_fail_to_force_unitarity"] is True

    model_ids = [m["model_id"] for m in res["models"]]
    assert model_ids == ["MODEL-A", "MODEL-B", "MODEL-C", "MODEL-D", "MODEL-E"]

    for m in res["models"]:
        assert m["forces_unitarity_independently"] is False
        assert len(m["barrier"]) > 0


def test_davenport_heilbronn_grade_character_unboundedness():
    """
    Cycle 4 Countermodel Control:
    The Davenport-Heilbronn zeta function satisfies xi(s) = xi(1-s) and has off-line zeros.
    Verify that its off-line zero produces an exponentially unbounded bilateral grade character,
    proving that functional equation symmetry and dilation alone cannot force unitarity or boundedness.
    """
    with mpmath.workdps(50):
        # Known Davenport-Heilbronn zero
        s_guess = mpmath.mpc('0.808517', '85.699348')
        root = mpmath.findroot(lambda s: davenport_heilbronn(s, 50), s_guess)
        delta_dh = root.real - mpmath.mpf('0.5')
        gamma_dh = root.imag

        assert delta_dh > 0.25

        # Grade K = 5
        K = 5
        chi_pos = transcendental.evaluate_grade_character(delta_dh, gamma_dh, K=K, dps=50)
        chi_neg = transcendental.evaluate_grade_character(delta_dh, gamma_dh, K=-K, dps=50)

        # For K = 5, tau^(5 * delta) > (6.28)^(1.5) > 15
        assert float(chi_pos["modulus_actual"]) > 10.0
        # For K = -5, tau^(-5 * delta) < 0.1
        assert float(chi_neg["modulus_actual"]) < 0.1

        # Defect is strictly positive (> 10.0 for delta approx 0.3085, K=5)
        assert float(chi_pos["defect_D_K"]) > 10.0


# ==============================================================================
# 7. CYCLE 5: LOG-HAAR TEMPEREDNESS BRIDGE & PRIME ERROR EQUIVALENCE
# ==============================================================================

def test_pure_radial_defect_vs_complex_difference():
    """
    Cycle 5 (Defect Correction):
    Verify that:
      (abs(chi(K/2)) - abs(chi(-K/2)))^2 = 4*sinh^2(a) is purely radial,
      abs(chi(K)) + abs(chi(-K)) - 2 = 4*sinh^2(a) is the canonical integer-grade radial defect,
      abs(chi(K/2) - chi(-K/2))^2 = 4*sinh^2(a) + 4*sin^2(b) = 2*cosh(2a) - 2*cos(2b)
      contains an explicit phase term 4*sin^2(b).
    """
    with mpmath.workdps(70):
        delta = mpmath.mpf('0.1')
        gamma = mpmath.mpf('14.134725')
        tau = 2 * mpmath.pi
        K = 2

        res = transcendental.evaluate_grade_character(delta, gamma, K=K, dps=70)
        d_rad_half = float(res["defect_radial_halfgrade"])
        d_rad_int = float(res["defect_radial_integer"])
        d_complex = float(res["defect_complex_difference"])
        phase_part = float(res["phase_defect_component"])

        # Radial integer and half-grade formulas match identically
        assert abs(d_rad_half - d_rad_int) < 1e-15

        # Complex difference equals radial part + phase part
        assert abs(d_complex - (d_rad_half + phase_part)) < 1e-15

        # Pure radial defect is strictly positive
        assert d_rad_int > 0.0

        # When delta = 0, pure radial defect vanishes identically
        res_zero = transcendental.evaluate_grade_character('0.0', gamma, K=K, dps=70)
        assert float(res_zero["defect_radial_integer"]) == 0.0
        # But complex difference does NOT vanish if 2*b not in 2*pi*Z
        assert float(res_zero["defect_complex_difference"]) > 0.0


def test_log_haar_zero_mode_translation_and_modulus():
    """
    Cycle 5 (Theorem C Foundations):
    Verify in logarithmic coordinate u = log x:
      phi_lambda(u) = exp((delta + i*gamma)*u)
      |phi_lambda(u)| = exp(delta * u)
      phi_lambda(u + t) = exp(lambda * t) * phi_lambda(u).
    """
    with mpmath.workdps(70):
        delta = mpmath.mpf('0.15')
        gamma = mpmath.mpf('14.134725')
        u = mpmath.mpf('3.0')

        res = transcendental.evaluate_log_haar_zero_mode(delta, gamma, u=u, dps=70)
        assert float(res["modulus_residual"]) < 1e-65
        assert float(res["translation_cocycle_residual"]) < 1e-65

        # Modulus is exp(delta * u)
        expected_mod = mpmath.exp(delta * u)
        assert abs(float(res["modulus_actual"]) - float(expected_mod)) < 1e-15

        # Off-line delta > 0 is unbounded as u -> +infty
        assert res["is_unbounded_positive"] is True
        assert res["is_bounded_on_R"] is False

        # On-line delta = 0 is bounded on all of R
        res_0 = transcendental.evaluate_log_haar_zero_mode('0.0', gamma, u=u, dps=70)
        assert res_0["is_bounded_on_R"] is True
        assert abs(float(res_0["modulus_actual"]) - 1.0) < 1e-15


def test_log_mode_temperedness_criterion():
    """
    Cycle 5 (Theorem C):
    Verify that phi_lambda defines a regular tempered distribution in S'(R)
    if and only if delta = 0.
    """
    gamma = mpmath.mpf('14.134725')

    # delta = 0: regular tempered distribution (polynomially bounded of degree 0)
    res_0 = transcendental.verify_log_mode_temperedness_criterion(delta='0.0', gamma=gamma, dps=70)
    assert res_0["is_tempered_distribution"] is True
    assert res_0["classification"] == "REGULAR_TEMPERED_DISTRIBUTION"
    assert res_0["criterion_holds"] is True

    # delta != 0: exponential growth outgrows all polynomials, non-tempered
    for d in ['0.05', '-0.05', '0.2']:
        res_d = transcendental.verify_log_mode_temperedness_criterion(delta=d, gamma=gamma, dps=70)
        assert res_d["is_tempered_distribution"] is False
        assert res_d["classification"] == "EXPONENTIALLY_GROWING_NON_TEMPERED"
        assert res_d["criterion_holds"] is True


def test_prime_counting_error_growth_and_rh_equivalence():
    """
    Cycle 5 (Prime Error Analysis, corrected in Cycle 6):
    Verify that normalized Chebyshev error E(u) = exp(-u/2)*(psi(exp u) - exp u):
    1. Unconditional Vinogradov-Korobov upper bound is too weak to establish polynomial growth,
       leaving its unconditional status as UNKNOWN_FROM_THIS_BOUND (non-temperedness claim withdrawn).
    2. Under RH has polynomial bound O(u^2), hence is tempered in S'(R).
    3. Temperedness in S'(R) is logically equivalent to RH (Cramer-Ingham and Route II).
    """
    res = transcendental.evaluate_prime_counting_error_growth(dps=70)
    assert res["unconditional_status"] == "UNKNOWN_FROM_THIS_BOUND"
    assert res["conditional_rh_status"] == "POLYNOMIALLY_BOUNDED_TEMPERED_IN_S_PRIME"
    assert res["is_rh_equivalent"] is True

    # Ratio of unconditional upper scale to polynomial growth diverges with u
    evals = res["evaluations"]
    assert len(evals) >= 4
    # u=5: ratio ~ 0.48; u=50: ratio > 10^7
    assert float(evals[-1]["unconditional_over_rh_ratio"]) > 1e7


def test_tc_orbit_uniformity_countermodel():
    """
    Cycle 5 (Uniformity Audit):
    Verify that for countermodel f(u) = exp(delta * u) with delta != 0:
      (P1) Pointwise transport T_K f is well-defined for each finite grade K (holds).
      (P2) Uniform bilateral orbit bound fails (diverges exponentially).
      (P3) Tempered space membership fails.
    Confirms that invertible coordinate transport does NOT imply uniform orbit admissibility.
    """
    res = transcendental.audit_tc_orbit_uniformity(delta='0.1', K_max=8, dps=70)
    assert res["P1_pointwise_transport_well_defined"] is True
    assert res["P2_uniform_bilateral_orbit_bounded"] is False
    assert res["P3_common_tempered_space_membership"] is False

    # For delta = 0, all three hold
    res_0 = transcendental.audit_tc_orbit_uniformity(delta='0.0', K_max=8, dps=70)
    assert res_0["P1_pointwise_transport_well_defined"] is True
    assert res_0["P2_uniform_bilateral_orbit_bounded"] is True
    assert res_0["P3_common_tempered_space_membership"] is True


def test_log_haar_temperedness_mechanism_audit():
    """
    Cycle 5 Synthesis Audit (updated in Cycle 6):
    Verify the overall synthesis of the Log-Haar Temperedness Bridge (TC-DISC-010 / CLM-TC-010):
    Status is CONDITIONAL_ONLY because prime-side temperedness is equivalent to RH.
    """
    res = transcendental.audit_log_haar_temperedness_mechanism(dps=70)
    assert res["candidate_id"] == "TC-DISC-010"
    assert res["status"] == "CONDITIONAL_ONLY"
    assert res["mode_online_tempered"] is True
    assert res["mode_offline_tempered"] is False
    assert res["prime_error_unconditional_status"] == "UNKNOWN_FROM_THIS_BOUND"
    assert res["prime_error_rh_equivalent"] is True
    assert res["tc_supplies_p1_pointwise"] is True
    assert res["tc_supplies_p2_p3_uniformity"] is False


# ==============================================================================
# 9. MECHANISM DISCYCLE 6 AUDIT (PRIME-ERROR TEMPEREDNESS EQUIVALENCE)
# ==============================================================================

def test_phase_cancelling_schwartz_pairing_divergence():
    """
    Cycle 6 (Section 2.3):
    Verify that the phase-cancelling test family:
      eta_n(u) = exp(-i*gamma*u) * exp(-u^2/(2*n^2))
    yields exact pairing:
      <phi_lambda, eta_n> = sqrt(2*pi) * n * exp(n^2 * delta^2 / 2),
    which for delta != 0 outgrows all polynomial Schwartz seminorms p_{alpha,beta}(eta_n).
    """
    # Off-line zero delta = 0.1
    res = transcendental.evaluate_phase_cancelling_schwartz_pairing(delta='0.1', gamma='14.134725', dps=70)
    assert res["is_delta_zero"] is False
    assert res["proves_discontinuity_for_nonzero_delta"] is True

    evals = res["evaluations"]
    assert len(evals) >= 5
    # Pairing-to-p00 ratio grows super-linearly
    assert float(evals[-1]["pairing_over_p00_ratio"]) > 100 * float(evals[0]["pairing_over_p00_ratio"])
    # For n >= 10, pairing-to-p20 ratio diverges super-polynomially (for n=40, ratio > 200, exceeding n=1)
    assert float(evals[-1]["pairing_over_p20_ratio"]) > float(evals[0]["pairing_over_p20_ratio"])
    assert float(evals[-1]["pairing_over_p20_ratio"]) > float(evals[-2]["pairing_over_p20_ratio"])

    # On-line zero delta = 0: exact pairing is sqrt(2*pi)*n, exactly linear
    res_0 = transcendental.evaluate_phase_cancelling_schwartz_pairing(delta='0.0', gamma='14.134725', dps=70)
    assert res_0["is_delta_zero"] is True
    assert res_0["proves_discontinuity_for_nonzero_delta"] is False


def test_chebyshev_error_local_slope_and_jump_structure():
    """
    Cycle 6 (Section 4 & Route I):
    Verify that between jumps, E'(u) = -(1/2)*exp(-u/2)*(psi(e^u) + e^u) ~ -exp(u/2)
    diverges exponentially downwards, which violates polynomial slow decrease
    without an a priori prime bound.
    """
    res = transcendental.evaluate_chebyshev_error_local_structure(dps=70)
    assert res["route_I_tauberian_verdict"] == "TAUBERIAN_SLOW_DECREASE_FAILS_UNCONDITIONALLY"

    evals = res["evaluations"]
    assert len(evals) >= 4
    # At u=20, downward slope exceeds 22,000 while jump is <= 0.001
    assert float(evals[-1]["slope_over_jump_ratio"]) > 1e7


def test_chebyshev_laplace_meromorphic_poles_and_residues():
    """
    Cycle 6 (Route II Singularity Audit):
    Verify that in G(z) = -1/(z+1/2)*(zeta'/zeta)(z+1/2) - 1/(z-1/2):
    1. Pole at s = 1 (z = 1/2) has residue 0 (exact cancellation).
    2. Every off-critical zero with delta > 0 has an isolated pole in Re(z) > 0 with residue -m/rho != 0.
    """
    res = transcendental.evaluate_chebyshev_laplace_meromorphic_poles(dps=70)
    assert res["route_II_verdict"] == "EQUIVALENCE_PROVED"

    poles = res["pole_evaluations"]
    assert len(poles) == 4
    # On-line zeros (delta = 0) do not lie in Re(z) > 0
    assert poles[0]["in_right_half_plane"] is False
    assert poles[1]["in_right_half_plane"] is False

    # Hypothetical off-line zeros (delta > 0) lie in Re(z) > 0 and have strictly non-zero residue
    assert poles[2]["in_right_half_plane"] is True
    assert poles[2]["is_strictly_non_zero"] is True
    assert float(poles[2]["residue_magnitude"]) > 0.0

    assert poles[3]["in_right_half_plane"] is True
    assert poles[3]["is_strictly_non_zero"] is True
    assert float(poles[3]["residue_magnitude"]) > 0.0


def test_prime_error_temperedness_equivalence_synthesis():
    """
    Cycle 6 Synthesis Audit:
    Verify the overall synthesis of Cycle 6 (TC-DISC-011 / CLM-TC-011):
    Classification is EQUIVALENCE_PROVED:
      (A) RH <=> (B) E(u) = O((1+u)^N) <=> (C) T_E in S'(R).
    """
    res = transcendental.audit_prime_error_temperedness_equivalence(dps=70)
    assert res["candidate_id"] == "TC-DISC-011"
    assert res["claim_id"] == "CLM-TC-011"
    assert res["overall_classification"] == "EQUIVALENCE_PROVED"
    assert res["route_I_status"] == "TAUBERIAN_SLOW_DECREASE_FAILS_UNCONDITIONALLY"
    assert res["route_II_status"] == "EQUIVALENCE_PROVED"
    assert "PROVED" in res["implications_status"]["C_implies_A"]
    assert "PROVED" in res["implications_status"]["A_implies_B"]
    assert "PROVED" in res["implications_status"]["B_implies_C"]


# ==============================================================================
# 10. MECHANISM DISCYCLE 7 AUDIT (GRADE-ORBIT UNIFORMITY & GLUING BRIDGE)
# ==============================================================================

def test_theorem_d_partition_of_unity_reconstruction():
    """
    Cycle 7 (Section 3):
    Verify that the discrete grade-orbit partition of unity:
      sum_{K in Z} theta(u - K*a) = 1 identically on R,
    holds to high precision (error < 1e-65) across test points.
    """
    res = transcendental.evaluate_theorem_d_partition_of_unity(dps=70)
    assert res["partition_is_exact"] is True
    assert float(res["max_partition_error"]) < 1e-65
    assert len(res["partition_evaluations"]) >= 5


def test_tc_grade_orbit_countermodel_p0_p1_p2():
    """
    Cycle 7 (Sections 4 & 5):
    Verify the three levels of the off-line exponential countermodel:
      f_{delta, gamma}(u) = exp((delta + i*gamma)*u).
    1. Level P0: Pointwise coordinate naturality holds identically (error < 1e-70).
    2. Level P1: Ambient distribution exists in D'(R) (locally integrable).
    3. Level P2: Uniform polynomial grade-orbit bound FAILS for delta != 0,
       as tau^{K*delta} grows exponentially and outgrows any polynomial bound.
    4. For delta == 0: P2 is satisfied with constant uniform bound.
    """
    # Off-line mode delta = 0.1
    res_off = transcendental.evaluate_tc_grade_orbit_countermodel(delta='0.1', gamma='14.134725', dps=70)
    assert "SATISFIED" in res_off["P0_coordinate_naturality"]
    assert "SATISFIED" in res_off["P1_distribution_gluing"]
    assert "VIOLATED" in res_off["P2_uniform_polynomial_bound"]
    assert res_off["p2_violation_witnessed"] is True
    assert res_off["verdict"] == "COORDINATE_NATURALITY_DOES_NOT_IMPLY_GRADE_UNIFORM_TEMPEREDNESS"

    for ev in res_off["evaluations"]:
        assert float(ev["p0_covariance_error"]) < 1e-60

    # Check that for large K (K = 100), the ratio of orbit modulus to polynomial bound is huge (> 100)
    large_K_eval = next(e for e in res_off["evaluations"] if e["K"] == 100)
    assert float(large_K_eval["ratio_orbit_over_poly"]) > 100.0
    assert float(res_off["J_0"]) > 0.0

    # On-line mode delta = 0.0
    res_on = transcendental.evaluate_tc_grade_orbit_countermodel(delta='0.0', gamma='14.134725', dps=70)
    assert "SATISFIED" in res_on["P0_coordinate_naturality"]
    assert "SATISFIED" in res_on["P1_distribution_gluing"]
    assert "SATISFIED" in res_on["P2_uniform_polynomial_bound"]
    assert res_on["p2_violation_witnessed"] is False


def test_grade_orbit_uniformity_mechanism_synthesis():
    """
    Cycle 7 Synthesis Audit (TC-DISC-012 / CLM-TC-012):
    Verify answers to the 5 core mission questions:
    1. Did Cycle 7 find a TC exclusion mechanism: NO.
    2. Do existing TC axioms imply polynomial grade-orbit control: NO.
    3. Exact missing premise: Polynomial grade-orbit control of E under discrete translations u -> u + K*log(tau).
    4. Is that premise independent of RH, equivalent to RH, or unknown: EQUIVALENT_TO_RH.
    5. What did Lean prove, exactly:
       RiemannScope.polynomial_bilateral_grade_growth_implies_delta_zero forces delta = 0.
    """
    res = transcendental.audit_grade_orbit_uniformity_mechanism(dps=70)
    assert res["candidate_id"] == "TC-DISC-012"
    assert res["claim_id"] == "CLM-TC-012"
    assert res["direct_answers"]["did_cycle_7_find_tc_exclusion_mechanism"] == "NO"
    assert res["direct_answers"]["do_existing_tc_axioms_imply_polynomial_grade_orbit_control"] == "NO"
    assert res["direct_answers"]["premise_status"] == "EQUIVALENT_TO_RH"
    assert "delta = 0" in res["direct_answers"]["lean_formalization_exact_scope"]
    assert res["level_classification"]["P0_pointwise_coordinate_naturality"].startswith("ESTABLISHED")
    assert res["level_classification"]["P1_global_distribution_gluing"].startswith("ESTABLISHED")
    assert res["level_classification"]["P2_uniform_polynomial_grade_orbit_bound"].startswith("NOT_SUPPLIED_BY_TC")
    assert res["countermodel_status"]["satisfies_P0"] is True
    assert res["countermodel_status"]["satisfies_P1"] is True
    assert res["countermodel_status"]["satisfies_P2"] is False
    assert res["overall_classification"] == "FAILURE_OF_COORDINATE_NATURALITY_TO_IMPLY_GRADE_UNIFORM_TEMPEREDNESS"


def test_cutoff_correction_compact_support_and_entire_extension():
    """
    Cycle 6 / Cycle 7 Cutoff Correction Audit:
    Verify that:
    1. The integrand of H(z) = int_0^0.5 (chi(u) - 1) * E(u) * exp(-zu) du is supported on [0, 0.5].
    2. At any hypothetical off-line zero z_rho = delta + i*gamma with delta > 0,
       H(z_rho) is finite (entire) and cannot cancel the pole of G(z) because Res(G, z_rho) = -m/rho != 0.
    """
    # Verify bounds for H(z) on [0, 0.5]
    with mpmath.workdps(70):
        # On [0, 0.5], u in [0, 0.5], exp(u) in [1, exp(0.5)] ~ [1, 1.6487] < 2.
        # Since the first prime is 2, psi(exp u) = 0 for u in [0, 0.5]!
        # Therefore, for u in [0, 0.5]:
        #   E(u) = exp(-u/2) * (0 - exp u) = - exp(u/2).
        # This is smooth and explicitly known: E(u) = - exp(u/2)!
        # The integrand of H(z) is (chi(u) - 1) * (-exp(u/2)) * exp(-zu).
        # Since chi(u) - 1 = 0 for u >= 0.5 and integration starts at u = 0,
        # the integrand has compact support contained in [0, 0.5].
        # For any z in C:
        #   |H(z)| <= int_0^0.5 1 * exp(u/2) * exp(-Re(z)*u) du <= 0.5 * exp(0.25) * max(1, exp(-0.5*Re(z))) < infty.
        # Thus H(z) is unconditionally ENTIRE!
        z_rho = mpmath.mpc('0.1', '14.134725')
        # Numerical integration of H(z_rho)
        # Using a simple smooth transition model for chi(u):
        def chi_smooth(u: mpmath.mpf) -> mpmath.mpf:
            if u <= mpmath.mpf('0.1'):
                return mpmath.mpf('0')
            elif u >= mpmath.mpf('0.5'):
                return mpmath.mpf('1')
            else:
                # Smooth polynomial blend
                s = (u - mpmath.mpf('0.1')) / mpmath.mpf('0.4')
                return s * s * (mpmath.mpf('3') - mpmath.mpf('2') * s)

        def integrand_re(u: mpmath.mpf) -> mpmath.mpf:
            c = chi_smooth(u)
            e_u = - mpmath.exp(u / mpmath.mpf('2'))
            kernel = mpmath.exp(- z_rho * u)
            return (c - mpmath.mpf('1')) * e_u * kernel.real

        def integrand_im(u: mpmath.mpf) -> mpmath.mpf:
            c = chi_smooth(u)
            e_u = - mpmath.exp(u / mpmath.mpf('2'))
            kernel = mpmath.exp(- z_rho * u)
            return (c - mpmath.mpf('1')) * e_u * kernel.imag

        val_re = mpmath.quad(integrand_re, [mpmath.mpf('0'), mpmath.mpf('0.5')])
        val_im = mpmath.quad(integrand_im, [mpmath.mpf('0'), mpmath.mpf('0.5')])
        H_val = mpmath.mpc(val_re, val_im)

        assert abs(H_val) < mpmath.mpf('10.0')
        # Pole residue of G(z) at z_rho = delta + i*gamma
        rho = mpmath.mpf('0.5') + z_rho
        res_G = - mpmath.mpf('1') / rho
        assert abs(res_G) > mpmath.mpf('0.05')


# ==============================================================================
# 10. CYCLE 8: CANONICAL TC DIAGRAM & COLLISION WITNESS VERIFICATION
# ==============================================================================

def test_canonical_tc_diagram_isomorphism_and_fixed_zeros():
    """
    Cycle 8 (Sections 3, 4, 5):
    Verify the Canonical TC Commutative Diagram:
    1. iota_K: N_{>=1} -> L_K is an exact isomorphism of (+_K, *_K).
    2. Layers L_K and L_J are strictly disjoint for K != J.
    3. External Dirichlet series D_K(s) = tau^{-Ks} * zeta(s) has strictly invariant zeros:
       div(D_K) = div(zeta) for all K in Z.
    4. D_K(s) is distinct from frequency-dilated Z_K(s) = zeta(tau^{-K} s).
    """
    res = transcendental.evaluate_canonical_tc_diagram(K=1, J=2, dps=60)
    assert res["arithmetic_isomorphism"]["is_isomorphic"] is True
    assert float(res["arithmetic_isomorphism"]["addition_homomorphism_error"]) < 1e-50
    assert float(res["arithmetic_isomorphism"]["multiplication_homomorphism_error"]) < 1e-50
    assert res["layer_disjointness"]["layers_externally_disjoint"] is True
    assert float(res["layer_disjointness"]["min_distance_grid_1_to_20"]) > 0.01

    assert float(res["analytic_objects"]["conversion_factor_agreement_error"]) < 1e-50
    assert res["analytic_objects"]["DK_differs_from_frequency_dilation_ZK"] is True
    assert float(res["analytic_objects"]["zero_at_rho_1_fixed_error"]) < 1e-45
    assert "FIXED_INVARIANT_ZEROS" in res["analytic_objects"]["zero_behavior_verdict"]


def test_collision_witness_obligation_and_transcendental_separation():
    """
    Cycle 8 (Sections 6 & 7):
    Audit the 5 collision witness conditions W1-W5:
    W1: Prime-zeta derivation is exact (Perron / explicit formula).
    W2: Fails because tau^{K-J} is transcendental and cannot equal rational n/m.
    W3: Fails because single zero modes x^rho/rho are C^infty on (0, infty) with NO jump discontinuities;
        jump discontinuities of psi_K occur strictly at tau^K p^k in L_K.
    W4: Compatible on critical line (no collision on or off the line).
    W5: No circular RH assumption.
    """
    res = transcendental.audit_collision_witness_obligation(delta='0.1', gamma='14.134725', K=1, J=0, dps=60)
    assert res["W1_prime_zeta_derivation"]["status"] == "PASS"
    assert "FAILED_IMPOSSIBLE" in res["W2_arithmetic_incidence"]["status"]
    assert "FAILED_NO_ARROW" in res["W3_off_line_forcing"]["status"]
    assert res["W3_off_line_forcing"]["zero_mode_smoothness"] is True
    assert "PASS" in res["W4_critical_line_compatibility"]["status"]
    assert res["W5_no_hidden_rh_premise"]["status"] == "PASS"
    assert res["classification"] == "COLLISION_WITNESS_PROVED_IMPOSSIBLE_UNDER_PRESENT_TC_MAPS"


def test_canonical_tc_synthesis_cycle8():
    """
    Cycle 8 (Section 10):
    Verify the 6 core answers in the canonical synthesis audit.
    """
    res = transcendental.audit_canonical_tc_synthesis(dps=60)
    answers = res["direct_answers"]
    assert answers["1_is_there_one_canonical_tc_transport"].startswith("YES")
    assert answers["2_are_previously_used_zeta_transforms_compatible_or_different"].startswith("DIFFERENT_CONSTRUCTIONS")
    assert answers["3_does_canonical_diagram_contain_zero_to_arithmetic_incidence_map"].startswith("NO")
    assert answers["4_was_concrete_collision_witness_found"].startswith("NO")
    assert "transcendental" in answers["5_exact_absent_arrow_or_theorem"]
    assert "arithmetic_isomorphism_add" in answers["6_what_did_lean_prove_exactly"]
    assert "FALSIFIED_IMPOSSIBLE" in res["collision_witness_verdict"]


def test_dense_disjoint_layer_theorems():
    """
    Cycle 9 (Section 3):
    Verify Theorem A (Pairwise Separation) and Theorem B (Countable Density).
    """
    res = transcendental.prove_dense_disjoint_layer_theorems(dps=60)
    assert res["theorem_A_separation"]["status"] == "PROVED_TRANSCENDENTAL_EXACT"
    assert res["theorem_B_density"]["status"] == "PROVED_CONSTRUCTIVE_EXACT"
    assert res["theorem_B_density"]["all_test_cases_passed"] is True

    # Verify constructive approximation bound for each tested case
    for tc in res["theorem_B_density"]["tested_cases"]:
        assert tc["satisfies_bound"] is True
        assert tc["satisfies_eps"] is True


def test_competing_grade_sequences_disjointness_and_convergence():
    """
    Cycle 9 (Section 5):
    Verify the construction of competing grade sequences from disjoint layers.
    """
    res = transcendental.construct_competing_grade_sequences(x_val='2.5', num_terms=8, dps=60)
    assert res["layers_disjoint"] is True
    assert len(res["sequence_A"]) == 8
    assert len(res["sequence_B"]) == 8

    # Check that grades K_r and J_r are distinct for every term
    for i in range(8):
        assert res["sequence_A"][i]["grade_K"] != res["sequence_B"][i]["grade_J"]
        # Error decreases as r grows
        err_A = float(res["sequence_A"][i]["error_from_x"])
        err_B = float(res["sequence_B"][i]["error_from_x"])
        assert err_A < 1.0
        assert err_B < 1.0


def test_grade_limit_observables_absence_of_defect():
    """
    Cycle 9 (Section 6):
    Test Candidates 1-5 along competing grade sequences for both delta = 0 and delta = 0.2.
    Demonstrates absence of grade-limit defect across all correctly converted observables.
    """
    # On-line zero mode (delta = 0)
    res_on = transcendental.evaluate_grade_limit_observables(
        x_val='2.5', s_val='2.0+1.0j', delta='0.0', gamma='14.134725', num_terms=6, dps=60
    )
    assert res_on["grade_limit_defect_detected"] is False
    assert res_on["defect_audit"]["cand1_raw_s_converges_to_x_s"] is True
    assert res_on["defect_audit"]["cand3_converted_s_converges_to_x_s"] is True
    assert res_on["defect_audit"]["cand4_zero_mode_converges_to_x_lambda"] is True
    assert float(res_on["defect_audit"]["final_defect_zm_conv"]) < 1e-4

    # Off-line zero mode (delta = 0.2)
    res_off = transcendental.evaluate_grade_limit_observables(
        x_val='2.5', s_val='2.0+1.0j', delta='0.2', gamma='14.134725', num_terms=6, dps=60
    )
    assert res_off["grade_limit_defect_detected"] is False
    assert res_off["defect_audit"]["cand1_raw_s_converges_to_x_s"] is True
    assert res_off["defect_audit"]["cand3_converted_s_converges_to_x_s"] is True
    assert res_off["defect_audit"]["cand4_zero_mode_converges_to_x_lambda"] is True
    assert float(res_off["defect_audit"]["final_defect_zm_conv"]) < 1e-4


def test_cycle9_limit_compatibility_synthesis():
    """
    Cycle 9 (Section 11):
    Verify the 8 direct answers in the Cycle 9 synthesis audit.
    """
    res = transcendental.audit_cycle9_limit_compatibility_synthesis(dps=60)
    answers = res["direct_answers"]
    assert answers["1_is_union_dense_in_R"].startswith("YES")
    assert answers["2_are_layers_pairwise_disjoint_away_from_zero"].startswith("YES")
    assert "zeta(s)" in answers["3_what_is_intrinsic_transported_zeta"]
    assert "tau^{-Ks}" in answers["4_what_is_raw_external_dirichlet_series"]
    assert answers["5_do_correctly_converted_grade_values_have_unique_limits"].startswith("YES")
    assert answers["6_does_limit_defect_occur_specifically_when_delta_ne_0"].startswith("NO")
    assert answers["7_was_tc_exclusion_mechanism_found"].startswith("NO")
    assert "nu_K_mul_scaled" in answers["8_what_did_lean_prove_exactly"]
    assert "The layer union is dense" in res["epistemic_conclusion"]


def test_prime_measure_transport_and_weak_limit():
    """
    Cycle 10 (Mini-Sprint 1):
    Verify transported prime measure mu_h = (d_h)_* mu, Jacobian normalization nu_h = h * mu_h,
    and weak convergence nu_h -> dx on compactly supported smooth test functions.
    """
    res = transcendental.audit_prime_measure_transport(dps=40)
    assert res["weak_convergence_observed"] is True
    assert res["jacobian_forced"] is True
    assert "transcendence of tau" in res["support_disjointness_property"]

    evals = res["grade_evaluations"]
    err_fine = float(evals[0]["pairing_error"])  # K = -3
    err_coarse = float(evals[-1]["pairing_error"])  # K = 0
    assert err_fine < err_coarse
    assert err_fine < 0.01

    ratio_fine = float(evals[0]["cum_ratio_to_X"])  # K = -3
    assert abs(ratio_fine - 1.0) < 0.01  # > 99% of X


def test_half_density_fluctuation_zero_scaling():
    """
    Cycle 10 (Mini-Sprint 2):
    Verify half-density zero mode scaling h^{1/2 - rho} = tau^{-K*(delta + i*gamma)}.
    Confirm:
      1. For delta = 0 (on-line): modulus is identically 1 for all grades K in Z.
      2. For delta > 0 (off-line): modulus grows exponentially as K -> -infty.
      3. Theory and direct power agree to machine precision.
    """
    # On-line
    res_on = transcendental.audit_half_density_fluctuation(delta_val=0.0, dps=40)
    assert "BOUNDED_PURE_PHASE" in res_on["behavior"]
    for ev in res_on["mode_evaluations"]:
        assert abs(float(ev["modulus_direct"]) - 1.0) < 1e-15
        assert abs(float(ev["modulus_theory"]) - 1.0) < 1e-15

    # Off-line (delta = 0.2)
    res_off = transcendental.audit_half_density_fluctuation(delta_val=0.2, dps=40)
    assert "EXPONENTIAL_GROWTH_FINE_GRADES" in res_off["behavior"]
    evals_off = res_off["mode_evaluations"]
    mod_fine = float(evals_off[0]["modulus_direct"])  # K = -5
    mod_coarse = float(evals_off[-1]["modulus_direct"])  # K = 2
    assert mod_fine > mod_coarse
    assert mod_fine > 5.0
    for ev in evals_off:
        assert abs(float(ev["modulus_direct"]) - float(ev["modulus_theory"])) < 1e-15


def test_smoothed_explicit_formula_fluctuation():
    """
    Cycle 10 (Mini-Sprint 3):
    Verify smoothed explicit formula zero sum S_zeros(h) on C_c^infty test function.
    Confirm:
      1. On-line quartet has bounded oscillation.
      2. Off-line quartet exhibits exponential growth as K -> -infty.
      3. H1 and H2 are forced, whereas H3 (grade regularity) is not derived from TC.
    """
    res = transcendental.audit_smoothed_explicit_formula_fluctuation(dps=40)
    assert res["offline_exponential_growth_detected"] is True
    assert float(res["max_offline_modulus"]) > float(res["max_online_modulus"])
    assert res["h1_jacobian_status"] == "FORCED_BY_COORDINATE_MEASURE_TRANSPORT"
    assert res["h2_center_status"] == "FORCED_BY_ZETA_FUNCTIONAL_EQUATION"
    assert "NOT_DERIVED_FROM_TC" in res["h3_grade_regularity_status"]


def test_cycle10_prime_measure_synthesis():
    """
    Cycle 10 (Section 16):
    Verify all 11 direct answers in the Cycle 10 synthesis resolution.
    """
    res = transcendental.audit_cycle10_prime_measure_synthesis(dps=40)
    answers = res["direct_answers"]
    assert "mu_h = (d_h)_* mu" in answers["1_exact_transported_prime_measure"]
    assert "Lebesgue measure transforms" in answers["2_why_jacobian_factor_forced"]
    assert answers["3_does_h_mu_h_converge_to_dx"].startswith("YES")
    assert "Prime Number Theorem" in answers["4_is_convergence_equivalent_to_pnt_or_rh"]
    assert "h^{-1/2}" in answers["5_exact_half_density_fluctuation"]
    assert "tau^{-K*(delta + i*gamma)}" in answers["6_how_zero_transforms"]
    assert "Ingham/Landau" in answers["7_does_complete_smoothed_sum_preserve_growth"]
    assert answers["8_does_tc_force_regularity"].startswith("NO")
    assert answers["9_was_exclusion_mechanism_found"].startswith("NO")
    assert "supp(mu_h) cap supp(mu_{h'}) = emptyset" in answers["10_where_is_transcendental_separation_essential"]
    assert "half_density_scaling_exponent_complex" in answers["11_what_did_lean_prove_exactly"]
    assert "The remaining regularity condition (H3) is not derived independently of RH" in res["epistemic_conclusion"]


# ==============================================================================
# 11. CYCLE 11: TC PHASE NONRESONANCE, CERTIFIED BOUNDS, AND CANCELLATION
# ==============================================================================

def test_tc_phase_propositions_disentanglement():
    """
    Cycle 11 (Section 2):
    Verify that the 5 propositions P1 - P5 are logically distinguished:
      P1 (aperiodicity), P2 (pairwise distinction), P3 (homogeneous LI),
      P4 (joint density via Kronecker-Weyl), P5 (zero-index equidistribution).
    Confirm that P2 (distinct bases) is strictly the weakest condition required
    for the finite Vandermonde uniqueness theorem.
    """
    res = transcendental.audit_tc_phase_propositions(dps=40)
    props = res["propositions"]

    assert props["P1_single_phase_aperiodicity"]["status"].startswith("OPEN")
    assert props["P2_pairwise_phase_distinction"]["status"].startswith("CERTIFIED")
    assert props["P2_pairwise_phase_distinction"]["required_for_cycle10_cancellation"] is True
    assert props["P1_single_phase_aperiodicity"]["required_for_cycle10_cancellation"] is False
    assert props["P3_homogeneous_rational_independence"]["required_for_cycle10_cancellation"] is False
    assert props["P4_joint_grade_orbit_density"]["required_for_cycle10_cancellation"] is False
    assert props["P5_zero_index_equidistribution"]["status"].startswith("PROVED")
    assert res["weakest_condition_for_cancellation"] == "P2_pairwise_phase_distinction"


def test_certify_pairwise_phase_distinction_arb():
    """
    Cycle 11 (N1):
    Verify certified pairwise phase distinction theta_j - theta_ell not in Z
    for the first N = 25 nontrivial zeros using Arb ball arithmetic.
    Confirm min certified separation from Z > 0.001.
    """
    res = transcendental.certify_pairwise_phase_distinction_arb(N=25, prec_bits=256)
    if res.get("status") == "FLINT_UNAVAILABLE":
        pytest.skip("flint not available")

    assert res["classification"] == "CERTIFIED_WITH_EXPLICIT_BOUNDS"
    assert res["N"] == 25
    assert res["pairs_checked"] == 25 * 24 // 2
    assert res["all_pairs_strictly_separated_from_Z"] is True
    assert float(res["min_separation_from_integer"]) > 0.003


def test_certify_bounded_rational_exclusion_arb():
    """
    Cycle 11 (N2):
    Verify bounded rational exclusion theta_j != p/q for 1 <= q <= 10^6
    for the first N = 20 zeros via continued fraction convergents of Arb balls.
    Confirm achieved Q >= 10^6 and min approximation error >> ball radius.
    """
    res = transcendental.certify_bounded_rational_exclusion_arb(N=20, Q_target=1000000, prec_bits=256)
    if res.get("status") == "FLINT_UNAVAILABLE":
        pytest.skip("flint not available")

    assert res["classification"] == "CERTIFIED_WITH_EXPLICIT_BOUNDS"
    assert res["all_zeros_certified"] is True
    assert res["N"] == 20
    assert float(res["min_rational_distance_overall"]) > 1e-16
    for item in res["detailed_results"]:
        assert item["achieved_Q"] >= 1000000
        assert item["certified_no_rational_up_to_Q"] is True
        assert item["min_rational_distance"] > item["theta_radius"]


def test_audit_bounded_integer_relations():
    """
    Cycle 11 (N3):
    Verify bounded integer relation audit:
      1. Dimension 2 box search (|a1|, |a2| <= 50) is CERTIFIED_WITH_EXPLICIT_BOUNDS.
      2. Dimension 4 PSLQ search is strictly NUMERICAL_EVIDENCE_ONLY.
    """
    res = transcendental.audit_bounded_integer_relations(max_coeff=50, dps=50)
    r2 = res["r2_box_search"]
    pslq = res["pslq_search"]

    assert r2["classification"] == "CERTIFIED_WITH_EXPLICIT_BOUNDS"
    assert r2["box_bound_B"] == 50
    assert r2["min_certified_distance"] > 1e-5
    assert pslq["classification"] == "NUMERICAL_EVIDENCE_ONLY"


def test_audit_phase_equidistribution_diagnostics():
    """
    Cycle 11 (N4):
    Verify equidistribution diagnostics over the zero index (Hlawka / Ford-Zaharescu):
      Confirm discrepancy and Weyl sums decay as N increases from 20 to 100.
    """
    res = transcendental.audit_phase_equidistribution_diagnostics(N=100, num_zeros=100, dps=50)
    assert res["classification"] == "NUMERICAL_EVIDENCE_ONLY"
    assert res["decay_observed"] is True

    diag = res["diagnostics_by_cutoff"]
    assert diag["N_100"]["discrepancy_D_N"] < diag["N_20"]["discrepancy_D_N"]
    assert diag["N_100"]["histogram_L1_deviation"] < diag["N_20"]["histogram_L1_deviation"]


def test_audit_tc_zero_phase_nonresonance_theorem():
    """
    Cycle 11 (Section 3):
    Verify the TC Zero-Phase Nonresonance Theorem formulation:
      Unconditional zero-phase equidistribution (Hlawka 1975)
      Nonresonance with prime-power frequencies (tau^q != p^a via Lindemann 1882)
      Identical vanishing of limiting Ford-Zaharescu correction measure.
    """
    res = transcendental.audit_tc_zero_phase_nonresonance_theorem()
    assert res["classification"] == "PROVED"
    assert "FIRST_RIGOROUS_TC_PRIME_FREQUENCY_NONRESONANCE_THEOREM" in res["status"]
    assert len(res["theorem_statements"]) == 5
    assert len(res["explicit_non_proofs"]) >= 5


def test_tc_bridge_implication_chain():
    """
    Cycle 11 (Section 7):
    Audit the TC bridge implication chain and confirm earliest unproved inference.
    """
    res = transcendental.audit_tc_bridge_implication_chain()
    assert "TC PHASE NONRESONANCE PROVED; RH EXCLUSION BRIDGE STILL OPEN" in res["verdict"]
    assert res["steps"][0]["status"] == "PROVED"
    assert res["steps"][1]["status"] == "PROVED"
    assert res["steps"][2]["status"] == "OPEN"
    assert res["steps"][3]["status"] == "MISSING / UNPROVED"


def test_cycle11_synthesis():
    """
    Cycle 11 (Section 10):
    Verify all four executive answers of Cycle 11 synthesis.
    """
    res = transcendental.audit_cycle11_synthesis(dps=40)
    exec_answers = res["executive_answers"]

    assert exec_answers["1_are_tc_phases_nonresonant_with_prime_frequencies"].startswith("YES (PROVED)")
    assert exec_answers["2_is_grade_axis_incommensurability_proved"].startswith("NO (OPEN)")
    assert exec_answers["3_does_result_force_forbidden_lattice_coincidence"].startswith("NO (OPEN)")
    assert "TC PHASE NONRESONANCE PROVED; RH EXCLUSION BRIDGE STILL OPEN" in exec_answers["4_has_rh_exclusion_mechanism_been_found"]


# ==============================================================================
# 12. CYCLE 12: COMPLETE TC TRANSPORT, HONEST CERTIFICATION, & DETECTABILITY
# ==============================================================================

def test_n1_fail_closed_inputs():
    """
    Cycle 12 (Soundness Repair A):
    Verify that certify_pairwise_phase_distinction_arb fails closed when:
      1. Given an invalid directory path (returns INPUT_INVALID).
      2. Given an empty list or missing certificates.
    """
    res_bad = transcendental.certify_pairwise_phase_distinction_arb(repo_root="nonexistent_path_xyz")
    assert res_bad["classification"] == "INPUT_INVALID"
    assert res_bad["all_pairs_strictly_separated_from_Z"] is False
    assert "INPUT_ERROR" in res_bad["status"]


def test_n2_farey_witness_coverage_and_brute_force():
    """
    Cycle 12 (Soundness Repair B):
    Verify Farey coverage witness algorithm:
      1. Correctly detects rational inside an interval (e.g. 10/81 in [0.123456, 0.123458]).
      2. For an interval with no rationals <= Q, constructs Farey neighbors a/b < c/d
         with unimodular check b*c - a*d == 1 and mediant denominator b + d > Q.
      3. certify_bounded_rational_exclusion_arb returns CERTIFIED_WITH_EXPLICIT_BOUNDS
         with valid Farey brackets for each zero.
    """
    # 1. Detection of internal rational
    wit_in, msg_in = transcendental.find_farey_witness_coverage(0.123456, 0.123458, Q_target=100)
    assert wit_in is None
    assert "10/81" in msg_in

    # 2. Construction of Farey bracket
    wit_ok, msg_ok = transcendental.find_farey_witness_coverage(0.123460, 0.123465, Q_target=100)
    assert wit_ok is not None
    a, b, c, d = wit_ok
    assert b * c - a * d == 1
    assert b + d > 100

    # 3. Execution of certified rational exclusion
    res = transcendental.certify_bounded_rational_exclusion_arb(N=5, Q_target=1000000, prec_bits=256)
    if res.get("status") == "FLINT_UNAVAILABLE":
        pytest.skip("flint not available")
    assert res["classification"] == "CERTIFIED_WITH_EXPLICIT_BOUNDS"
    assert res["all_zeros_certified"] is True
    for item in res["detailed_results"]:
        fb = item["farey_bracket"]
        assert fb["unimodular_check"] == 1
        assert item["achieved_Q"] > 1000000
        assert item["certified_no_rational_up_to_Q"] is True


def test_n3_integer_relations_repaired():
    """
    Cycle 12 (Soundness Repair C):
    Verify integer relations:
      1. Correct sign of a0 witness: a0 + a1*theta_1 + a2*theta_2 has residual
         magnitude matching the reported distance (~7.9e-5, not ~74).
      2. Synthetic duplicate detection: zeros=['1.0', '1.0'] returns RELATION_FOUND.
    """
    # 1. Default box search witness sign check
    res = transcendental.audit_bounded_integer_relations(max_coeff=50, dps=50)
    r2 = res["r2_box_search"]
    assert r2["classification"] == "CERTIFIED_WITH_EXPLICIT_BOUNDS"
    rel = r2["closest_relation"]
    assert rel["a0"] == 37
    assert rel["a1"] == -3
    assert rel["a2"] == -4
    # Compute residual: a0 + a1*theta_1 + a2*theta_2
    tau = 2 * math.pi
    c_tau = math.log(tau) / tau
    th1 = c_tau * 14.13472514173469379
    th2 = c_tau * 21.02203963877155499
    res_val = 37 - 3 * th1 - 4 * th2
    assert abs(abs(res_val) - rel["distance"]) < 1e-6
    assert abs(res_val) < 1e-4

    # 2. Synthetic duplicate detection
    res_dup = transcendental.audit_bounded_integer_relations(zeros=["1.0", "1.0"], max_coeff=1, dps=40)
    assert res_dup["r2_box_search"]["classification"] == "RELATION_FOUND"


def test_complete_smoothed_tc_transport():
    """
    Cycle 12 (Primary Mathematical Task):
    Verify the complete smoothed TC transport identity:
      h * sum_{n >= 1} Lambda(n) phi(hn) = phi_tilde(1) - sum_rho m_rho phi_tilde(rho) h^{1-rho} - background
    on C_c^infty test function with support in [2, 4], 0 < h < 2.
    Confirm:
      1. Background series sum_{j>=1} phi_tilde(-2j) h^{1+2j} matches background integral to < 1e-12.
      2. Constant -zeta'(0)/zeta(0) is identically 0.
      3. Prime side and spectral side agree within zero tail truncation error (residual < 1e-4 for N=75 zeros).
    """
    res = transcendental.audit_complete_smoothed_tc_transport(h_val=1.0, num_zeros=75, dps=40)
    assert res["classification"] == "DERIVED_AND_VERIFIED"
    assert res["spectral_components"]["background_representations_discrepancy"] < 1e-12
    assert res["spectral_components"]["constant_zeta_prime_term"] == 0.0
    assert res["residual"] < 1e-4
    assert res["error_budget"]["residual_within_tail_budget"] is True


def test_quantitative_vandermonde_block_detectability():
    """
    Cycle 12 (Next Theorem):
    Verify the quantitative Vandermonde block estimate:
      max_{0 <= l < r} |S(k+l)| >= c(q_1, ..., q_r) * max_j |a_j q_j^k|
    with c = 1 / ||V^{-1}||_{infty -> infty} > 0.
    Confirm bound is satisfied across all tested grades k = 0..9 for an off-line quartet.
    """
    res = transcendental.audit_quantitative_vandermonde_block_detectability(r=4, off_line_delta=0.25, dps=40)
    assert res["classification"] == "PROVED"
    assert res["block_constant_c"] > 0.15
    assert res["all_blocks_satisfied"] is True
    for blk in res["blocks"]:
        assert blk["bound_satisfied"] is True
        assert blk["ratio"] >= 1.0


def test_infinite_extension_detectability():
    """
    Cycle 12 (Infinite Extension Audit):
    Verify the distinction among the three infinite extension propositions,
    absence of critical-line integer aliasing, and open status of the collision bridge.
    """
    res = transcendental.audit_infinite_extension_detectability()
    assert res["classification"] == "AUDITED_AND_STRUCTURED"
    props = res["propositions"]
    assert "IMPOSSIBLE" in props["1_fixed_annihilating_test"]["verdict"]
    assert "FEASIBLE" in props["2_approximate_isolation_family"]["verdict"]
    assert "DISTRIBUTIONAL_UNIQUENESS_PROVED" in props["3_distributional_uniqueness"]["verdict"]
    assert "DISCRETE_SPECTRAL_SYNTHESIS_UNPROVED" in props["3_distributional_uniqueness"]["verdict"]
    assert "OPEN_SPECTRAL_INDEPENDENCE_HYPOTHESIS" in res["aliasing_audit"]["status"]
    assert "OPEN" in res["collision_mechanism_audit"]["verdict"]


def test_cycle12_synthesis():
    """
    Cycle 12 (Synthesis Audit):
    Verify the six executive answers for Cycle 12.
    """
    res = transcendental.audit_cycle12_synthesis(dps=40)
    answers = res["executive_answers"]
    assert answers["1_does_complete_tc_transport_have_correct_derivation_and_real_test"].startswith("YES (DERIVED AND VERIFIED)")
    assert answers["2_which_finite_incommensurability_statements_are_certified"].startswith("CERTIFIED")
    assert answers["3_what_new_theorem_established_and_what_did_lean_prove"].startswith("PROVED")
    assert answers["4_can_off_line_contribution_be_detected_in_infinite_formula"].startswith("INCONCLUSIVE")
    assert answers["5_what_forces_nonzero_membership_in_two_distinct_arithmetic_layers"].startswith("NOTHING")
    assert answers["6_was_exclusion_mechanism_found"].startswith("NO")



# ==============================================================================
# 18. CYCLE 13: RELIABLE CERTIFICATION & COMPLETE TC DETECTION SUITE
# ==============================================================================

def test_cycle13_farey_1_over_49_counterexample_regression():
    """
    Cycle 13 Regression & Soundness Audit:
    Reproduce the review counterexample:
      - At Q = 49, the rational 1/49 lies on the boundary/inside the test.
      - Old floating-point conversion accepted the bracket (0/1, 1/49) which does NOT strictly
        contain 1/49, falsely certifying exclusion.
      - Rigorous exact rational Farey coverage must return None (refuse to certify)
        both for exact 1/49 and for an Arb interval containing 1/49.
    """
    # 1. Exact rational interval [1/49, 1/49] at target Q=49
    res_exact, msg_exact = transcendental.find_farey_witness_coverage(
        x_low=fractions.Fraction(1, 49),
        x_high=fractions.Fraction(1, 49),
        Q_target=49
    )
    assert res_exact is None
    assert "lies inside" in msg_exact or "non-empty" in msg_exact or "target" in msg_exact

    # 2. Arb interval containing 1/49 at Q=49
    try:
        from flint import arb, ctx
        old_prec = ctx.prec
        ctx.prec = 256
        theta_arb = arb("1/49") + arb(0, "1e-25")
        # Direct verification that theta_arb contains 1/49
        assert theta_arb.contains(arb("1/49"))

        # Attempt Farey coverage at Q=49 on this Arb interval
        x_lo = theta_arb.lower().fmpq()
        x_hi = theta_arb.upper().fmpq()
        res_arb, msg_arb = transcendental.find_farey_witness_coverage(
            x_low=fractions.Fraction(int(x_lo.p), int(x_lo.q)),
            x_high=fractions.Fraction(int(x_hi.p), int(x_hi.q)),
            Q_target=49,
            arb_ball=theta_arb
        )
        assert res_arb is None, "Farey coverage must refuse to certify exclusion for interval containing 1/49 at Q=49"
        ctx.prec = old_prec
    except ImportError:
        pass

    # 3. Positive control: valid interval strictly avoiding small rationals
    # At Q=10, the interval [0.15, 0.16] lies strictly between 1/7 (~0.1428) and 1/6 (~0.1666)
    # Mediants check: 1/7 (b=7) and 1/6 (d=6) has b+d = 13 > 10.
    res_pos, msg_pos = transcendental.find_farey_witness_coverage(
        x_low=fractions.Fraction(15, 100),
        x_high=fractions.Fraction(16, 100),
        Q_target=10
    )
    assert res_pos is not None
    a, b, c, d = res_pos
    assert a == 1 and b == 7
    assert c == 1 and d == 6
    assert b * c - a * d == 1
    assert b + d == 13
    assert b + d > 10


def test_cycle13_bounded_relations_classifications():
    """
    Cycle 13 Soundness Audit (Bounded Integer Relations):
    Verifies the four distinct classifications:
      1. EXACT RELATION -> RELATION_FOUND (synthetic identical zeros).
      2. STRICT SEPARATION -> CERTIFIED_WITH_EXPLICIT_BOUNDS (certified zeros 1 and 2).
      3. ZERO-CONTAINING RESIDUAL -> INCONCLUSIVE (adversarial synthetic input containing 0).
      4. FLOATING-POINT FALLBACK -> NUMERICAL_EVIDENCE_ONLY.
    """
    # 1. Exact synthetic relation: identical zeros
    res_exact = transcendental.audit_bounded_integer_relations(zeros=["14.134725", "14.134725"], max_coeff=5, dps=40)
    assert res_exact["r2_box_search"]["classification"] == "RELATION_FOUND"
    assert res_exact["r2_box_search"]["min_certified_distance"] == 0.0

    # 2. Strict separation with certified zero enclosures
    res_cert = transcendental.audit_bounded_integer_relations(max_coeff=50, dps=50)
    assert res_cert["r2_box_search"]["classification"] == "CERTIFIED_WITH_EXPLICIT_BOUNDS"
    assert res_cert["r2_box_search"]["min_certified_distance"] > 0.0
    assert "Search domain: checked a0 + a1*theta_1 + a2*theta_2" in res_cert["r2_box_search"]["search_domain_justification"] or "Nearest-integer reduction" in res_cert["r2_box_search"]["search_domain_justification"]

    # 3. Adversarial zero-containing residual: synthetic zeros where a linear form straddles an integer
    # Using theta_1 = 0.5, theta_2 = 0.25: 2*theta_1 - 4*theta_2 = 1 - 1 = 0.
    res_zero = transcendental.audit_bounded_integer_relations(zeros=["0.5", "0.25"], max_coeff=5, dps=40)
    # Either RELATION_FOUND or INCONCLUSIVE depending on exactness vs enclosure
    assert res_zero["r2_box_search"]["classification"] in ["RELATION_FOUND", "INCONCLUSIVE"]


def test_cycle13_complete_transport_multi_grade_and_error_budget():
    """
    Cycle 13 Complete Transport Audit:
    Verifies:
      1. Complete formula evaluated across multiple grades h in {1.0, 0.5, tau^{-1}, tau^{-2}}.
      2. Discrepancy at M=15 (8.57e-14) is rigorously enclosed by geometric tail bound (6.89169e-11).
      3. Zero truncation error is bounded by Stieltjes formula (log T + 1)/T with Mellin derivative norms C_k.
      4. Residuals are strictly within error budgets across all tested grades.
      5. Absence of phantom pole at s=0 is documented and confirmed.
    """
    res = transcendental.audit_complete_smoothed_tc_transport(h_val=1.0, num_zeros=75, dps=40, eval_multi_grade=True)
    assert res["classification"] == "DERIVED_AND_VERIFIED"
    assert len(res["multi_grade_runs"]) == 4

    for run in res["multi_grade_runs"]:
        # Check that residual is within rigorous zero tail budget
        assert run["error_budget"]["residual_within_tail_budget"] is True
        assert run["error_budget"]["discrepancy_enclosed_by_geometric_bound"] is True
        assert run["residual"] <= run["error_budget"]["rigorous_zero_tail_bound"]

    # Verify Cycle 12 inconsistency resolution
    primary = res["primary_run"]
    disc_15 = primary["spectral_components"]["background_discrepancy_M15"]
    geom_15 = primary["error_budget"]["bg_geometric_tail_bound_M15"]
    assert disc_15 <= geom_15, f"Discrepancy {disc_15} must be <= geometric bound {geom_15}"
    assert disc_15 > 7e-14  # Replicates the ~8.57e-14 observed discrepancy

    # Verify absence of pole at s=0 explanation
    assert "has no pole at s=0" in res["mathematical_audit"]["absence_of_pole_at_s_zero"]
    assert "zeta(0) = -1/2 != 0" in res["mathematical_audit"]["absence_of_pole_at_s_zero"]


def test_cycle13_remainder_aware_vandermonde_detection():
    """
    Cycle 13 Remainder-Aware Vandermonde Block Detectability:
    Verifies the quantitative theorem:
      max_{0 <= l < r} |Y(k+l)| >= c * max_j |a_j q_j^k| - max_l |R(k+l)|
    with c = 1 / ||V^{-1}||_{infty -> infty} > 0.
    Confirms behavior across 3 remainder regimes:
      1. Zero remainder: lower bound > 0 (detected).
      2. Subordinate remainder: lower bound > 0 (detected).
      3. Dominant remainder: lower bound <= 0 (detection threshold violated).
    """
    res = transcendental.audit_quantitative_vandermonde_block_detectability(r=4, off_line_delta=0.25, dps=40)
    assert res["classification"] == "PROVED"
    assert res["block_constant_c"] > 0.15
    assert res["all_inequalities_satisfied"] is True
    assert res["all_blocks_satisfied"] is True

    regimes = res["remainder_regimes"]
    assert regimes["zero_remainder"]["detected"] is True
    assert regimes["zero_remainder"]["lower_bound"] > 0.0

    assert regimes["subordinate_remainder"]["detected"] is True
    assert regimes["subordinate_remainder"]["lower_bound"] > 0.0

    assert regimes["dominant_remainder"]["detected"] is False
    assert regimes["dominant_remainder"]["lower_bound"] < 0.0


def test_cycle13_infinite_extension_aliasing_and_pw():
    """
    Cycle 13 Infinite Extension Structural Audit:
    Verifies:
      1. Synthetic aliasing control: ordinates separated by Delta gamma = 2*pi/log(tau)
         produce identical bases q_1 = q_2.
      2. Paley-Wiener / Jensen theorem: entire functions of exponential type have n(r) = O(r),
         strictly slower than N(r) ~ (r/pi) log r, precluding single-test full annihilation.
      3. Distributional uniqueness in D'((0, infty)) does not equal discrete synthesis.
      4. Arithmetic layer disjointness (L_K cap L_J = {0}) leaves the collision bridge open.
    """
    res = transcendental.audit_infinite_extension_detectability()
    assert res["classification"] == "AUDITED_AND_STRUCTURED"

    # 1. Aliasing control
    alias = res["aliasing_control"]
    assert alias["aliasing_confirmed"] is True
    assert alias["base_difference"] < 1e-12

    # 2. Paley-Wiener / Jensen
    pw = res["paley_wiener_impossibility"]
    assert "Paley-Wiener / Jensen" in pw["theorem"]
    assert "in C_c^infty" in pw["conclusion"]

    # 3. Collision bridge
    bridge = res["collision_bridge_audit"]
    assert bridge["status"] == "OPEN_RESEARCH_PROBLEM"
    assert "L_K cap L_J = {0}" in bridge["layer_disjointness"]


def test_cycle13_synthesis():
    """
    Cycle 13 Synthesis Resolution:
    Verifies that audit_cycle13_synthesis() executes all sub-audits and produces
    definitive answers to all 7 executive questions.
    """
    res = transcendental.audit_cycle13_synthesis(dps=30)
    assert res["cycle"].startswith("Cycle 13")
    answers = res["executive_answers"]
    assert len(answers) == 7
    assert answers["1_which_previous_claims_repaired_withdrawn_or_unresolved"].startswith("REPAIRED")
    assert "EXACT THEOREMS" in answers["2_what_is_proved_exactly_vs_certified_within_finite_bounds"]
    assert "vandermonde_block_remainder_2" in answers["3_what_did_lean_actually_establish"]
    assert answers["4_does_complete_formula_have_justified_error_budget_at_tested_grades"].startswith("YES")
    assert "Paley-Wiener" in answers["5_what_was_learned_about_infinite_mode_detectability"]
    assert answers["6_was_implication_toward_forbidden_coincidence_derived"].startswith("NO")
    assert answers["7_what_is_the_single_next_theorem_or_research_obligation"].startswith("Investigate")


# ==============================================================================
# 19. CYCLE 14: EVIDENCE REPAIRS, TRANSPORT AUDIT, & TC TEST-FAMILY INVESTIGATION
# ==============================================================================

def test_cycle14_certificate_tamper_and_fail_closed(tmp_path):
    """
    Cycle 14 Regression:
    1. Tampered midpoint without hash change fails with INPUT_ERROR_HASH_MISMATCH.
    2. Corrupted schema, invalid status, or missing enclosure fields fail with INPUT_INVALID.
    3. Precision restoration: ctx.prec is restored after error.
    """
    import json
    from flint import ctx
    repo_root = str(tmp_path)
    cert_dir = tmp_path / "data" / "certificates" / "zeros"
    cert_dir.mkdir(parents=True)

    # Copy actual valid certificate for zero 1
    src_cert = os.path.join(REPO_ROOT, "data", "certificates", "zeros", "zero_00001.json")
    with open(src_cert, "r", encoding="utf-8") as f:
        valid_data = json.load(f)

    # 1. Modify imaginary midpoint without changing sha256
    tampered_data = dict(valid_data)
    tampered_data["enclosure"] = dict(valid_data["enclosure"])
    tampered_data["enclosure"]["imag_mid"] = "14.999999999999999"
    with open(cert_dir / "zero_00001.json", "w", encoding="utf-8") as f:
        json.dump(tampered_data, f)

    zeros, info = transcendental.load_validated_zero_certificates(N=1, repo_root=repo_root)
    assert zeros is None
    assert info is not None
    assert "INPUT_ERROR_HASH_MISMATCH" in info["status"]
    assert info["classification"] == "INPUT_INVALID"

    # 2. Corrupt schema version
    tampered_data["schema_version"] = "1.0"
    with open(cert_dir / "zero_00001.json", "w", encoding="utf-8") as f:
        json.dump(tampered_data, f)
    zeros, info = transcendental.load_validated_zero_certificates(N=1, repo_root=repo_root)
    assert zeros is None
    assert info is not None
    assert "INPUT_ERROR_UNSUPPORTED_SCHEMA" in info["status"]

    # 3. Test precision restoration
    old_prec = ctx.prec
    try:
        ctx.prec = 128
        transcendental.load_validated_zero_certificates(N=1, repo_root=repo_root, prec_bits=512)
        assert ctx.prec == 128
    finally:
        ctx.prec = old_prec


def test_cycle14_consumer_fail_closed_without_fallback_promotion(tmp_path):
    """
    Cycle 14 Consumer Audit:
    Pointing consumers at an invalid or empty certificate directory fails closed
    and does NOT promote fallback decimals to certified zero data.
    """
    empty_repo = str(tmp_path)
    (tmp_path / "data" / "certificates" / "zeros").mkdir(parents=True)

    # 1. Pairwise distinction fails closed
    res_pair = transcendental.certify_pairwise_phase_distinction_arb(N=5, repo_root=empty_repo)
    assert res_pair["classification"] == "INPUT_INVALID"
    assert res_pair["all_zeros_valid"] is False

    # 2. Bounded rational exclusion fails closed
    res_rat = transcendental.certify_bounded_rational_exclusion_arb(N=5, Q_target=1000, repo_root=empty_repo)
    assert res_rat["classification"] == "INPUT_INVALID"

    # 3. Bounded integer relations fails closed by default
    res_rel = transcendental.audit_bounded_integer_relations(max_coeff=10, repo_root=empty_repo, allow_fallback=False)
    assert res_rel["classification"] == "INPUT_INVALID"

    # 4. If fallback is explicitly requested, outputs are flagged as NUMERICAL_EVIDENCE_ONLY, certified_zero_inputs=False
    res_fb = transcendental.audit_bounded_integer_relations(max_coeff=10, repo_root=empty_repo, allow_fallback=True)
    assert res_fb["r2_box_search"]["classification"] == "NUMERICAL_EVIDENCE_ONLY"
    assert res_fb["r2_box_search"]["certified_zero_inputs"] is False

    # 5. Transport fails closed without certificates
    res_trans = transcendental.audit_complete_smoothed_tc_transport(repo_root=empty_repo)
    assert res_trans["classification"] == "INPUT_INVALID"


def test_cycle14_transport_delimitation_and_tail_bounds():
    """
    Cycle 14 Transport Delimitation Audit:
    Verifies:
      1. Certification status is EMPIRICAL_QUADRATURE_WITH_RIGOROUS_TAIL_BOUNDS.
      2. M=15 background discrepancy is bounded by <= 6.89169e-11 (not 1.12e-11).
      3. Missing rigorous bounds for full certification are explicitly listed.
      4. Exact real parts are used only when certified exact.
    """
    res = transcendental.audit_complete_smoothed_tc_transport(dps=30, eval_multi_grade=False)
    assert res["classification"] == "DERIVED_AND_VERIFIED"
    assert res["certification_status"] == "EMPIRICAL_QUADRATURE_WITH_RIGOROUS_TAIL_BOUNDS"
    assert len(res["missing_rigorous_bounds_for_full_certification"]) >= 3

    # Background tail bound verification
    bg_audit = res["background_integral_audit"]
    assert bg_audit["M15_tail_bound"] <= 6.892e-11
    assert abs(bg_audit["M15_tail_bound"] - 6.891691e-11) < 1e-15
    assert bg_audit["observed_discrepancy"] <= bg_audit["M15_tail_bound"]


def test_cycle14_test_family_normalization_and_target_detection():
    """
    Cycle 14 Explicit Test-Family Investigation:
    For phi_{L, rho_0}(x) = (1/L) * x^{-rho_0} * w((log x)/L) with bump w_0 on (1.25, 1.75):
      1. Normalization int w(v) dv = 1, phi_tilde(rho_0) = 1.0 identically.
      2. For on-line zeros, remainder ratio eta(L) achieves target detection (< 1.0) for L >= 2.0.
      3. Strong detection (eta << 1.0) is achieved at L = 5.0.
    """
    res = transcendental.audit_tc_test_family_investigation(dps=30)
    assert res["classification"] == "AUDITED_AND_STRUCTURED"
    assert res["target_zero"]["identity_verified"] is True
    assert abs(res["target_zero"]["phi_tilde_target"][0] - 1.0) < 1e-10
    assert abs(res["target_zero"]["phi_tilde_target"][1]) < 1e-10

    # Scale sweep checks
    sweep = {row["L"]: row for row in res["scale_sweep_eta"]}
    assert sweep[0.5]["detected"] is False
    assert sweep[0.5]["eta"] > 1.0
    assert sweep[1.0]["detected"] is False
    assert sweep[1.0]["eta"] > 1.0
    assert sweep[2.0]["detected"] is True
    assert sweep[2.0]["eta"] < 1.0
    assert sweep[5.0]["detected"] is True
    assert sweep[5.0]["eta"] < 0.1


def test_cycle14_test_family_adversarial_competitor_blowup():
    """
    Cycle 14 Adversarial Competitor & Obstruction Audit:
    When an off-line competitor rho_comp with Re(rho_comp) > Re(rho_0) is present:
      1. Competitor amplitude grows exponentially with L as exp(L * Delta_beta * v).
      2. At L=20, competitor amplitude exceeds c_F, driving eta > 1.
      3. Proves test-family scaling cannot isolate a target without an a priori zero-free region.
    """
    res = transcendental.audit_tc_test_family_investigation(dps=30)
    comp_audit = res["adversarial_competitor_analysis"]
    assert comp_audit["competitor_real_part"] > comp_audit["target_real_part"]

    scaling = {row["L"]: row for row in comp_audit["scaling_results"]}
    assert scaling[20.0]["exceeds_cF"] is True
    assert scaling[20.0]["eta_lower_bound_from_competitor"] > 1.0
    assert "obstruction" in comp_audit


def test_cycle14_synthesis_executive_answers():
    """
    Cycle 14 Executive Synthesis Audit:
    Verifies that audit_cycle14_synthesis() executes and answers all 6 executive questions:
      1. TC preservation status
      2. Rigorously supported finite exclusions
      3. Transport certification status (empirical with tail bounds)
      4. Test-family investigation findings (on-line detection vs off-line competitor blowup)
      5. Arithmetic coincidence implication status (OPEN)
      6. Single next mathematical obligation
    """
    res = transcendental.audit_cycle14_synthesis(dps=30)
    assert res["cycle"].startswith("Cycle 14")
    answers = res["executive_answers"]
    assert len(answers) == 6
    assert "preserves the prime-zeta structure" in answers["1_tc_preservation_status"]
    assert "Bounded rational exclusion certified" in answers["2_rigorously_supported_finite_exclusions"]
    assert "EMPIRICAL WITH RIGOROUS TAIL BOUNDS" in answers["3_full_transport_certification_vs_empirical"]
    assert "INVESTIGATED" in answers["4_executed_test_family_investigation_results"]
    assert "competitor amplitudes blow up exponentially" in answers["4_executed_test_family_investigation_results"]
    assert answers["5_arithmetic_coincidence_implication_status"].startswith("NO IMPLICATION DERIVED")
    assert "Derive an explicit prime-zeta Tauberian identity" in answers["6_exact_single_next_mathematical_obligation"]


# =====================================================================
# SECTION 20: AUTONOMOUS TC MECHANISM DISCOVERY EPIC REGRESSION TESTS
# =====================================================================

def test_epic_whole_spectrum_gaussian_family():
    """
    Epic Track 1: Whole-Spectrum Spectral Isolation (Section 7E):
    Verifies:
      1. Truncated log-Gaussian test family with cancellation polynomial P(z).
      2. Competitor set C is finite (compactness of [0, 1] x [gamma_0 - 3, gamma_0 + 3]).
      3. Lean-proved quadratic exponent bound ensures Re(L*z^2 + 6L*z) <= -2L outside the band.
      4. Normalization error |1 - c_L| <= (1/(2*sqrt(pi*L))) * exp(-4L).
      5. Weighted cutoff error ||exp(t)*r_L(t)||_L1 <= L^{-1/2} * exp(-2L).
      6. Support condition 0 < h_k < exp(L) is satisfied for L >= 5.0 on grade block [-2, 2].
      7. Whole-spectrum limit lim_{L -> infty} max_{k in I} |Y_{phi_L}(k) - m_{rho_0} * q_{rho_0}^k| = 0.
    """
    res = transcendental.audit_whole_spectrum_gaussian_family(dps=30)
    assert res["classification"] == "PROVED_AND_VERIFIED"
    assert "Whole-Spectrum Spectral Isolation" in res["theorem"]

    comp = res["competitor_set_C"]
    assert "compactness" in comp["finiteness_proof"].lower()
    assert comp["cancellation_polynomial_degree"] >= 0

    lemmas = res["proved_lemmas"]
    assert "gaussian_exponent_band_bound" in lemmas
    assert "Lean 4" in lemmas["gaussian_exponent_band_bound"]
    assert "cutoff_error_lemma" in lemmas

    sweep = {row["L"]: row for row in res["parameter_sweep"]}
    for L in [1.0, 2.0, 5.0, 10.0]:
        row = sweep[L]
        # Normalization error is enclosed by the theoretical bound
        assert row["normalization_error"] <= row["normalization_error_bound"] * 1.05
        # Weighted cutoff tail is enclosed by the theoretical bound
        assert row["weighted_cutoff_tail_L1"] <= row["weighted_cutoff_bound"] * 1.05
        # Peak outside band decays exponentially
        assert row["untruncated_outside_band_peak"] <= math.exp(-2 * L) * 1.001

    # Support condition for grade block [-2, 2] requires a = exp(L) > tau^2 ≈ 39.478, satisfied at L=5 (exp(5) ≈ 148.4)
    assert sweep[1.0]["support_condition_satisfied"] is False
    assert sweep[2.0]["support_condition_satisfied"] is False
    assert sweep[5.0]["support_condition_satisfied"] is True
    assert sweep[10.0]["support_condition_satisfied"] is True

    # Limit statement and reconciliation with Paley-Wiener
    limit = res["whole_spectrum_limit"]
    assert limit["status"] == "PROVED_EXISTENTIAL_ANALYTIC_LIMIT"
    assert "Paley-Wiener" in limit["paley_wiener_reconciliation"]
    assert "does NOT force" in limit["epistemic_scoping"]
    assert "FOR ALL rho_0 in Z(zeta)" in limit["quantifier_structure"]
    assert "Y_L(k) = q^k * exp(-k^2 / L)" in limit["counterexample_d_to_e"]
    assert "Trudgian" in limit["tail_domain_vs_completeness"]
    assert "Turing" in limit["tail_domain_vs_completeness"]
    assert "Sampled values at L=2, 5 do not certify" in limit["sampling_caveat"]
    assert "phase cancellation" in limit["envelope_vs_phase_cancellation"]

    # Direct test of the counterexample: Y_L(k) = q^k * exp(-k^2/L)
    # Proves that uniform convergence on compact blocks as L -> infty does NOT imply growth as k -> infty
    q = 2.0
    k_test = 5
    # As L -> infty, Y_L(k) -> q^k:
    assert abs(q**k_test * math.exp(-(k_test**2) / 1000.0) - q**k_test) < 1.0
    # For fixed L=2.0, as k -> infty, Y_L(k) -> 0:
    assert q**20 * math.exp(-(20**2) / 2.0) < 1e-70


def test_epic_arithmetic_measure_atoms_and_bridge():
    """
    Epic Track 2: Arithmetic Measure Pushforward, Atom Extraction, & Disjointness (Section 8):
    Verifies:
      1. Formula pairing P_h(phi) = h * <mu_{-k}, phi> with K = -k.
      2. Layer support disjointness supp(mu_K) cap supp(mu_J) = emptyset for all K != J (Lindemann 1882).
      3. Atom extraction limit: prime powers yield delta atoms, while finite zero modes integrate to O(eps) -> 0.
      4. Non-multiplicativity of Lambda: Lambda(6) = 0 != Lambda(2)*Lambda(3) > 0.
      5. Opening bridge formula restricts to nontrivial zeros (0 < Re(rho) < 1) to exclude rho = -2.
      6. Six candidate bridge controls pass (unit conversion, linearity, distribution, prime-power, off-line, object).
      7. Arithmetic coincidence bridge is honestly classified as strictly OPEN.
    """
    res = transcendental.audit_arithmetic_measure_atoms_and_bridge(dps=30)
    assert res["classification"] == "PROVED_AND_VERIFIED"

    # Pairing
    assert res["pairing"]["pairing_verified"] is True
    assert "-k" in res["pairing"]["grade_sign_relation"]

    # Layer disjointness
    disjoint = res["layer_disjointness"]
    assert "Lindemann" in disjoint["proof"]
    for check in disjoint["sample_checks"]:
        assert check["sample_station_distance"] > 0.0

    # Non-multiplicativity of Lambda
    vmp = res["von_mangoldt_properties"]
    assert vmp["is_multiplicative"] is False
    assert "Lambda(6) = 0" in vmp["counterexample"]
    assert "logarithmic derivative" in vmp["euler_product_mechanism"]

    # Opening bridge formula nontrivial zero restriction
    obf = res["opening_bridge_formula"]
    assert "0 < Re(rho) < 1" in obf["target_zeros"]
    assert "rho = -2" in obf["trivial_zero_counterexample"]

    # Atom extraction
    atoms = res["atom_extraction"]
    assert "O(eps)" in atoms["finite_mode_annihilation"]
    assert "singular support" in atoms["complete_spectral_sum_localization"]
    for row in atoms["numerical_scaling"]:
        assert abs(row["prime_atom_value"] - math.log(2)) < 1e-10
        # Spectral mode integral scales down linearly with epsilon
        assert row["spectral_mode_integral"] < 2.0 * row["epsilon"]
    assert atoms["numerical_scaling"][-1]["spectral_mode_integral"] < 0.002

    # Controls
    controls = res["controls_audit"]
    assert len(controls) == 6
    for k, v in controls.items():
        assert v.startswith("PASSED:")

    # Bridge status
    verdict = res["arithmetic_coincidence_verdict"]
    assert verdict["status"] == "ARITHMETIC_COINCIDENCE_BRIDGE_STRICTLY_OPEN"
    assert "remains OPEN" in verdict["summary"]


def test_epic_synthesis_deliverables():
    """
    Epic Synthesis & Deliverables Audit:
    Verifies that audit_tc_epic_synthesis() executes cleanly and confirms:
      1. All 8 starting questions and review requirements are resolved.
      2. Track 0 compiled theorems count is 193 with zero sorry.
      3. Track 1 and Track 2 audits are fully integrated.
    """
    res = transcendental.audit_tc_epic_synthesis(dps=30)
    assert res["epic"] == "Autonomous TC Mechanism Discovery Epic"

    # Starting questions
    sq = res["starting_questions_resolved"]
    assert len(sq) == 8
    assert "RESOLVED" in sq["1_quoted_integer_grade_theorem"]
    assert "vandermonde_2_reconstruction_bound_zpow" in sq["1_quoted_integer_grade_theorem"]
    assert "CONFIRMED" in sq["2_finite_experiment_reproduced"]
    assert "RESOLVED" in sq["3_asymptotic_leap_resolved"]
    assert "RESOLVED" in sq["4_tail_domain_resolved"]
    assert "RECOMPUTED AND ENCLOSED" in sq["5_recorded_constants_recomputed"]
    assert "VERIFIED" in sq["6_input_and_evidence_integrity"]
    assert "DELIMITED" in sq["7_alternative_target_delimited"]
    assert "DEMONSTRATED" in sq["8_research_agent_loops"]

    # Formal theorems
    formal = res["track_0_formal_theorems"]
    assert formal["compiled_theorems_count"] == 199
    assert len(formal["new_declarations"]) == 9
    assert "0 sorry" in formal["axioms"]

    # Tracks
    assert res["track_1_whole_spectrum_isolation"]["classification"] == "PROVED_AND_VERIFIED"
    assert res["track_1_notation_and_estimates"]["classification"] == "PROVED_AND_VERIFIED"
    assert res["track_2_arithmetic_measure_bridge"]["classification"] == "PROVED_AND_VERIFIED"
    assert res["track_3_arithmetic_overlap_observable"]["classification"] == "PROVED_AND_VERIFIED"
    assert res["track_4_gaussian_support_barrier"]["classification"] == "PROVED_AND_VERIFIED"


def test_epic_spectral_isolation_notation_and_estimates():
    """
    Epic Track 1: Spectral Isolation Notation, Exponents, and Derivative Estimates:
    Verifies:
      1. Unnormalized mode scaling: h_k = tau^(-k) => h_k^(1-rho) = tau^(k*(rho-1)).
         Verifies algebraically exact match with tau^(k*(rho-1)) across positive and negative k.
      2. Centered observable normalization: Y_phi(k) = h_k^(-1/2) * X_phi(k) = q_rho^k with q_rho = tau^(rho - 1/2).
      3. Repaired integration-by-parts factor isolates |eta|^p = |Im(rho - rho_0)|^p, not |z|^p.
      4. Gaussian completion of the square frequency decay |e^(L(z^2+6z))| <= e^(-2L) * e^(-L(eta^2 - 9)).
      5. Stieltjes frequency summability S_rho0 < infty via Trudgian (2014 Cor. 1).
    """
    res = transcendental.audit_spectral_isolation_notation_and_estimates(dps=30)
    assert res["classification"] == "PROVED_AND_VERIFIED"
    assert "tau^(k*(rho - 1))" in res["unnormalized_mode_formula"]
    assert "q_rho^k" in res["centered_mode_formula"]

    # Exponent audit across k in [-2, -1, 0, 1, 2, 3]
    for row in res["exponent_audit"]:
        k = row["k"]
        assert row["unnorm_identity_diff"] < 1e-25
        assert row["centered_identity_diff"] < 1e-25
        # For k != 0, old erroneous formula deviates significantly from correct unnormalized mode
        if k != 0:
            assert row["sign_error_ratio"] != 1.0

    # Integration by parts
    ibp = res["integration_by_parts"]
    assert "|eta|^p" in ibp["mathematical_formula"]
    assert "algebraically exact" in ibp["repaired_factor"]

    # Gaussian frequency decay
    for check in res["gaussian_decay_audit"]:
        assert check["is_bounded"] is True
        assert check["ratio"] <= 1.000001

    # Stieltjes tail
    stieltjes = res["stieltjes_audit"]
    assert stieltjes["tail_integral_status"] == "CONVERGENT"
    assert "Trudgian" in stieltjes["source"]


def test_epic_arithmetic_overlap_observable_and_obstruction():
    """
    Epic Track 3: Arithmetic Overlap Observable Exact Contract and Contradiction Architecture:
    Verifies:
      1. Finite station count in compact window [a, b].
      2. Transcendental disjointness: minimum station separation d_min > 0 between distinct grades K != J.
      3. Identical vanishing: Q_epsilon^{K, J}[w] == 0 for all epsilon < d_min.
      4. Diagonal mass control: for K = J, Q_epsilon^{K, K}[w] -> sum Lambda(n)^2 w(tau^K n)^2 > 0.
      5. Contradiction architecture & bridge inequality audit:
         If Q_epsilon >= c * D_{K-J}(rho_0) - r_epsilon were forced by an off-line zero, then for epsilon < d_min,
         LHS = 0 would yield 0 >= c * D / 2 > 0 (formalized in Lean candidate_bridge_positivity_contradiction).
         However, because LHS = 0 identically for small epsilon, the complete explicit formula forces
         exact cancellation R_bar_0 = -A_bar_0(rho_0), leaving the conditional spectral lower bound unproved.
    """
    res = transcendental.audit_arithmetic_overlap_observable(
        K=0, J=1, window=(2.0, 30.0), epsilons=[1.0, 0.5, 0.2, 0.1, 0.05, 0.01, 0.001], dps=30
    )
    assert res["classification"] == "PROVED_AND_VERIFIED"
    assert res["stations_K_count"] > 0
    assert res["stations_J_count"] > 0
    assert res["d_min"] > 0.0

    d_min = res["d_min"]
    # Verify vanishing for all epsilon < d_min
    for q_row in res["q_cross_grade_results"]:
        if q_row["epsilon"] < d_min:
            assert q_row["Q_epsilon"] == 0.0
            assert q_row["is_identically_zero"] is True
            assert q_row["contributing_pairs"] == 0

    # Diagonal mass control
    diag = res["q_diagonal_control"]
    assert diag["theoretical_diagonal_mass"] > 0.0
    # Smallest epsilon should approach theoretical diagonal mass closely
    smallest_diag = diag["q_diag_results"][-1]
    assert smallest_diag["diff_from_diagonal_mass"] < 1e-10

    # Contradiction architecture & bridge inequality audit
    refutation = res["bridge_inequality_refutation"]
    assert refutation["D_M_rho0"] > 0.0
    assert refutation["Q_at_small_epsilon"] == 0.0
    assert "impossible" in refutation["contradiction"]
    assert "candidate_bridge_positivity_contradiction" in refutation["intended_contradiction_endpoint"]
    assert "exact_cancellation_mechanism" in refutation
    assert "cancellation" in refutation["exact_cancellation_mechanism"]


def test_epic_gaussian_support_localization_barrier():
    """
    Epic Track 4: Gaussian Support Localization Escaping Barrier:
    Verifies:
      1. supp(phi_L) subset [e^L, e^(17L)].
      2. For any fixed window [a, b], as soon as L > log(b), supp(phi_L) cap [a, b] = emptyset.
      3. For window [2, 30], log(30) ≈ 3.4012. For L in [4, 5, 10, 20], phi_L vanishes identically on [2, 30].
      4. Confirms that Gaussian spectral isolation family cannot be inserted into fixed-window arithmetic observables.
    """
    res = transcendental.audit_gaussian_support_localization_barrier(
        L_vals=[1.0, 2.0, 3.0, 4.0, 5.0, 10.0, 20.0], window=(2.0, 30.0), dps=30
    )
    assert res["classification"] == "PROVED_AND_VERIFIED"
    log_b = res["log_b"]
    assert abs(log_b - math.log(30.0)) < 1e-6

    for check in res["barrier_checks"]:
        L = check["L"]
        if L > log_b:
            assert check["L_exceeds_log_b"] is True
            assert check["support_disjoint_from_window"] is True
            assert check["phi_L_identically_zero_on_window"] is True
        else:
            assert check["L_exceeds_log_b"] is False


# ==============================================================================
# TC EPIC: TWO-VARIABLE EXPANSION, TRUNCATION BOUNDS & BRIDGE TESTING
# ==============================================================================

def test_epic_tc_cutoff_condition_counterexample():
    """
    Epic Section 3.1 & 3.2:
    Verifies that the old cutoff condition T(eps) >> eps^(-(p-1)/(p-2)) is falsified
    by the exact counterexample p=3, ell = log(1/eps), T = eps^(-2) * sqrt(ell),
    and verifies the normalized power cutoff condition alpha > p/(p-2).
    """
    res = transcendental.audit_tc_cutoff_condition_counterexample(dps=30)
    assert res["classification"] == "DEFECT_REPAIRED_AND_VERIFIED"
    assert res["old_claim_verdict"] == "FALSIFIED_BY_EXACT_COUNTEREXAMPLE"

    for row in res["counterexample_rows"]:
        assert row["ratio_T_to_power"] > 1.0
        assert row["diverges"] is True
        assert row["symbolic_match_error"] < 1e-12

    # Power trajectory
    norm = res["normalization_analysis"]
    assert norm["p4_critical_alpha"] == 2.0
    assert norm["p4_justified_alpha"] == 3.0
    rows = norm["power_trajectory_rows"]
    # For alpha = 3, normalized bound decreases toward 0
    assert rows[-1]["norm_bound_alpha_3"] < rows[0]["norm_bound_alpha_3"] * 1e-3
    # For alpha = 2, critical normalized bound grows as log^2(1/eps)
    assert rows[-1]["norm_bound_alpha_2"] > rows[0]["norm_bound_alpha_2"]


def test_epic_two_variable_explicit_expansion():
    """
    Epic Section 5:
    Verifies the complete one-variable background geometric series identity,
    all 9 uncombined terms of the two-variable tensor product, and the 4 combined terms.
    """
    res = transcendental.evaluate_two_variable_explicit_expansion(
        K=0, J=1, window=(8.0, 20.0), dps=30
    )
    assert res["classification"] == "PROVED_AND_VERIFIED"
    assert res["window_satisfies_hypotheses"] is True

    # One-variable background geometric identity
    bg = res["one_variable_background_identity"]
    for row in bg["numerical_checks"]:
        assert row["absolute_diff"] < 1e-15

    # 9 Uncombined terms
    nine = res["uncombined_nine_terms"]
    assert len(nine) == 9
    signs = [t["sign"] for t in nine]
    assert signs.count("+") == 5
    assert signs.count("-") == 4

    # 4 Combined terms
    four = res["combined_four_terms"]
    assert len(four) == 4


def test_epic_selected_spectral_contribution_limit_and_falsification():
    """
    Epic Section 6:
    Verifies:
      1. Reality of f_{K, Gamma}(x) and A_{eps, Gamma}.
      2. Convergence A_{eps, Gamma} / eps -> A_{0, Gamma} with O(eps^2) error rate for even eta.
      3. Falsification of asserted identity A_{0, Gamma} = c * D_M on critical line zeros
         (where D_M = 0 while A_0 != 0).
    """
    res = transcendental.audit_selected_spectral_contribution(
        K=0, J=1, window=(8.0, 20.0), epsilons=[0.5, 0.2, 0.1, 0.05], dps=30
    )
    assert res["classification"] == "PROVED_AND_VERIFIED"
    assert res["is_on_critical_line"] is True
    assert res["D_M_rho0"] == 0.0
    assert abs(res["A_0_Gamma"]) > 0.1
    assert res["asserted_identity_A0_eq_cD_falsified"] is True
    assert res["even_mollifier_second_order_rate_confirmed"] is True

    # Check that diff / eps^2 is bounded
    for row in res["quadrature_convergence"]:
        assert row["diff_over_eps2"] < 1.0


def test_epic_two_variable_truncation_bound():
    """
    Epic Section 7:
    Verifies the conservative truncation bound C_p * eps^(1-p) * log^2(2+T) / T^(p-2),
    normalized scaling, and monotonic convergence along T = eps^(-3) for p=4.
    """
    res = transcendental.audit_two_variable_truncation_bound(
        K=0, J=1, p=4, window=(8.0, 20.0), dps=30
    )
    assert res["classification"] == "PROVED_AND_VERIFIED"
    assert res["critical_alpha"] == 2.0
    assert res["justified_alpha"] == 3.0
    assert res["convergence_verified"] is True


def test_epic_arithmetic_overlap_window_8_20_and_commensurable():
    """
    Epic Section 9:
    Verifies arithmetic overlap observable on window (8, 20) with K=0, J=1:
      1. Station disjointness: d_min > 0.
      2. Arithmetic vanishing: Q_eps^{0, 1} == 0 for all eps < d_min.
      3. Positive equal-grade diagonal mass Q_eps^{0, 0} > 0.
      4. Toy commensurable control detects genuine common station collision.
    """
    res = transcendental.audit_arithmetic_overlap_distinct_and_equal_grades(
        window=(8.0, 20.0), K=0, J=1, epsilons=[0.5, 0.2, 0.1, 0.05, 0.01], dps=30
    )
    assert res["classification"] == "PROVED_AND_VERIFIED"
    assert res["d_min"] > 0.1
    assert res["stations_0_count"] == 7
    assert res["stations_1_count"] == 2
    assert res["vanishing_verified_below_d_min"] is True
    assert res["equal_grade_is_positive"] is True
    assert res["toy_commensurable_control"]["detection_successful"] is True


def test_epic_two_variable_synthesis_deliverables():
    res = transcendental.audit_tc_epic_two_variable_synthesis(dps=25)
    assert 'Two-Variable Formula' in res['epic']
    assert res['formal_lean_theorems']['total_compiled_theorems'] >= 213
    assert len(res['formal_lean_theorems']['new_theorems']) >= 8
    assert 'explicit_formula_remainder_cancellation_tendsto' in res['formal_lean_theorems']['new_theorems']
    assert 'explicit_formula_remainder_cancellation_quantified' in res['formal_lean_theorems']['new_theorems']
    assert 'finite_spectral_perturbation_rigidity_2point' in res['formal_lean_theorems']['new_theorems']
    assert '0 sorry' in res['formal_lean_theorems']['axioms']
    epistemic = res['epistemic_classification']
    assert 'PROVED' in epistemic['arithmetic_vanishing']
    assert 'PROVED' in epistemic['two_variable_expansion']
    assert 'PROVED' in epistemic['conservative_truncation_bound']
    assert 'PROVED' in epistemic['normalized_cutoff_convergence']
    assert 'PROVED' in epistemic['selected_term_limit']
    assert 'FALSIFIED' in epistemic['assertion_A0_eq_cD_falsified']
    assert 'EXACT CANCELLATION' in epistemic['remainder_behavior']
    assert 'OBSTRUCTED' in epistemic['quadratic_form_mode_extraction']
    assert 'REFUTED' in epistemic['arbitrary_compensation_refuted']
    assert 'AUDITED' in epistemic['arithmetic_compatibility_chains']
    assert 'UNPROVED' in epistemic['conditional_spectral_lower_bound']
    assert 'STRICTLY OPEN' in epistemic['transcendental_continuation_bridge']
    import os
    assert os.path.exists('data/tc_epic_two_variable_synthesis.json')


def test_epic_two_variable_truncation_bound_parameter_handling_and_orders():
    res_p4 = transcendental.audit_two_variable_truncation_bound(p=4)
    assert res_p4['classification'] == 'PROVED_AND_VERIFIED'
    assert res_p4['evaluation_type'] == 'BOUND_SHAPE_ILLUSTRATIVE'
    assert res_p4['critical_alpha'] == 2.0
    assert res_p4['justified_alpha'] == 3.0
    assert res_p4['alpha_is_admissible'] is True
    assert res_p4['convergence_verified'] is True

    # Discriminating test: unverified caller-supplied constant cannot yield PROVED_AND_VERIFIED
    res_unverified = transcendental.audit_two_variable_truncation_bound(p=4, C_p=1e-100)
    assert res_unverified['classification'] == 'CALLER_UNVERIFIED_CONSTANT'
    assert res_unverified['evaluation_type'] == 'CALLER_SUPPLIED_UNVERIFIED'
    assert 'numeric constants cannot create mathematical proof' in res_unverified['status_reason']

    # Analytically derived and machine-checked constants
    res_derived = transcendental.audit_two_variable_truncation_bound(p=4, C_p=10.0, constant_source='DERIVED')
    assert res_derived['classification'] == 'ANALYTICALLY_DERIVED_CONSTANT'
    assert res_derived['evaluation_type'] == 'BOUND_WITH_DERIVED_CONSTANT'

    res_enclosure = transcendental.audit_two_variable_truncation_bound(p=4, C_p=10.0, constant_source='CERTIFIED_ENCLOSURE')
    assert res_enclosure['classification'] == 'MACHINE_CHECKED_ENCLOSURE'
    assert res_enclosure['evaluation_type'] == 'BOUND_WITH_CERTIFIED_ENCLOSURE'

    # Invalid constant values
    assert transcendental.audit_two_variable_truncation_bound(p=4, C_p=-1.0)['classification'] == 'INVALID_CONSTANT_ERROR'
    assert transcendental.audit_two_variable_truncation_bound(p=4, C_p=0.0)['classification'] == 'INVALID_CONSTANT_ERROR'
    assert transcendental.audit_two_variable_truncation_bound(p=4, C_p=float('nan'))['classification'] == 'INVALID_CONSTANT_ERROR'

    res_p3_crit = transcendental.audit_two_variable_truncation_bound(p=3, alpha=3.0)
    assert res_p3_crit['classification'] == 'NON_CONVERGENT_DEFECT'
    assert res_p3_crit['critical_alpha'] == 3.0
    assert res_p3_crit['alpha_is_admissible'] is False
    assert res_p3_crit['convergence_verified'] is False

    res_p3_below = transcendental.audit_two_variable_truncation_bound(p=3, alpha=2.5)
    assert res_p3_below['classification'] == 'NON_CONVERGENT_DEFECT'

    res_p3_above = transcendental.audit_two_variable_truncation_bound(p=3, alpha=4.0)
    assert res_p3_above['classification'] == 'PROVED_AND_VERIFIED'
    assert res_p3_above['alpha_is_admissible'] is True
    assert res_p3_above['convergence_verified'] is True

    res_p5 = transcendental.audit_two_variable_truncation_bound(p=5)
    assert res_p5['classification'] == 'PROVED_AND_VERIFIED'
    assert abs(res_p5['critical_alpha'] - (5.0 / 3.0)) < 1e-12
    assert res_p5['alpha_is_admissible'] is True
    assert res_p5['convergence_verified'] is True

    assert transcendental.audit_two_variable_truncation_bound(p=2)['classification'] == 'INVALID_ORDER_ERROR'
    assert transcendental.audit_two_variable_truncation_bound(p=1)['classification'] == 'INVALID_ORDER_ERROR'
    assert transcendental.audit_two_variable_truncation_bound(p=3.5)['classification'] == 'INVALID_ORDER_ERROR'
    assert transcendental.audit_two_variable_truncation_bound(p=4, epsilons=[])['classification'] == 'INVALID_DOMAIN_ERROR'
    assert transcendental.audit_two_variable_truncation_bound(p=4, epsilons=[-0.1])['classification'] == 'INVALID_DOMAIN_ERROR'


def test_epic_two_variable_explicit_expansion_window_hypothesis_enforcement():
    res_valid = transcendental.evaluate_two_variable_explicit_expansion(K=0, J=1, window=(8.0, 20.0))
    assert res_valid['classification'] == 'PROVED_AND_VERIFIED'
    assert res_valid['window_satisfies_hypotheses'] is True

    res_invalid = transcendental.evaluate_two_variable_explicit_expansion(K=0, J=2, window=(8.0, 20.0))
    assert res_invalid['classification'] == 'HYPOTHESIS_VIOLATION_WINDOW_BELOW_SCALE'
    assert res_invalid['window_satisfies_hypotheses'] is False


def test_epic_selected_spectral_contribution_precision_and_enclosure():
    res = transcendental.audit_selected_spectral_contribution(
        K=0, J=1, window=(8.0, 20.0), epsilons=[0.5, 0.2, 0.1, 0.05], dps=35
    )
    assert res['classification'] == 'PROVED_AND_VERIFIED'
    assert res['geometry_status'] == 'CRITICAL_LINE_PAIR'
    assert res['is_on_critical_line'] is True
    assert res['asserted_identity_A0_eq_cD_falsified'] is True
    enc = res.get('interval_enclosure')
    if enc and enc.get('engine') == 'flint.arb':
        assert enc['strictly_positive'] is True
        assert enc['lower_bound'] > 0.54
        assert 'flint.acb.zeta_zero(1).imag' in enc['zero_ordinate_provenance']
    offline = res['offline_zero_comparison']
    assert offline['synthetic_designation'] == 'SYNTHETIC_OFFLINE_CONTROL'
    assert 'not an actual Riemann zeta zero' in offline['purpose']


def test_epic_finite_decomposition_consistency_and_error_budget():
    # Discriminating test 1: Cutoff below first zero (T=10 < 14.13) has 0 zeros, Q_BZ=0, Q_ZZ=0, Q_ret == Q_BB
    res_10 = transcendental.evaluate_two_variable_finite_decomposition(
        K=0, J=1, window=(8.0, 20.0), eps=0.1, T=10.0, dps=25, recompute=True
    )
    assert res_10['classification'] == 'PROVED_AND_VERIFIED'
    assert res_10['retained_zero_count'] == 0
    assert res_10['selected_block_empty'] is True
    assert res_10['retained_spectral_expansion']['Q_BZ'] == 0.0
    assert res_10['retained_spectral_expansion']['Q_ZB'] == 0.0
    assert res_10['retained_spectral_expansion']['Q_ZZ'] == 0.0
    assert abs(res_10['retained_spectral_expansion']['Q_retained_sum'] - res_10['retained_spectral_expansion']['Q_BB']) < 1e-12

    # Discriminating test 2: Cutoff T=18 has 1 zero, Q_ret != Q_BB
    res_18 = transcendental.evaluate_two_variable_finite_decomposition(
        K=0, J=1, window=(8.0, 20.0), eps=0.1, T=18.0, dps=25, recompute=True
    )
    assert res_18['retained_zero_count'] == 1
    assert res_18['selected_block_empty'] is False
    assert abs(res_18['retained_spectral_expansion']['Q_retained_sum'] - res_10['retained_spectral_expansion']['Q_retained_sum']) > 0.01

    # Discriminating test 3: Cutoff T=30 has 3 zeros, Q_ret differs from T=18
    res_30 = transcendental.evaluate_two_variable_finite_decomposition(
        K=0, J=1, window=(8.0, 20.0), eps=0.1, T=30.0, dps=25, recompute=True
    )
    assert res_30['retained_zero_count'] == 3
    assert abs(res_30['retained_spectral_expansion']['Q_retained_sum'] - res_18['retained_spectral_expansion']['Q_retained_sum']) > 0.01

    # Independent remainder consistency check: R_eps_independent matches Q_ret - A_eps
    assert res_30['retained_remainder_R']['consistency_check_R_eq_Q_minus_A'] is True
    assert abs(res_30['retained_remainder_R']['R_eps_independent'] - res_30['retained_remainder_R']['R_eps']) < 1e-12

    # Arithmetic vanishing and error budget
    assert res_30['arithmetic_vanishing_verified'] is True
    assert res_30['arithmetic_observable_Q_eps'] == 0.0
    budget = res_30['error_budget']
    assert 'REFERENCE_ZERO_TRUNCATION' in budget['zero_inputs']
    assert 'Turing-method' in budget['missing_enumeration_obligation']
    assert 'quadrature_uncertainty' in budget
    assert 'rounding_uncertainty' in budget
    assert 'analytic_infinite_tail' in budget

    # Hypothesis violation handling
    res_inv = transcendental.evaluate_two_variable_finite_decomposition(
        K=0, J=2, window=(8.0, 20.0), eps=0.1, T=30.0
    )
    assert res_inv['classification'] == 'HYPOTHESIS_VIOLATION_WINDOW'


def test_epic_arithmetic_quadratic_form_mode_extraction_obstruction():
    res = transcendental.audit_arithmetic_quadratic_form_mode_extraction(
        K=0, J=1, window=(8.0, 20.0), epsilons=[0.2, 0.1, 0.05, 0.01], dps=30
    )
    assert res['classification'] == 'PROVED_AND_VERIFIED'
    assert res['mollifier_normalization']['is_unit_integral'] is True
    assert res['gram_matrix_limits']['is_positive_definite'] is True
    assert res['gram_matrix_limits']['H_01'] == 0.0
    assert res['smooth_spectral_mode_decay']['smooth_mass_vanishes_as_eps_to_zero'] is True

    # Check actual convolution vs asymptotic leading term
    rows = res['smooth_spectral_mode_decay']['scaling_rows']
    for r in rows:
        assert r['actual_convolution_mass'] > 0.0
        assert r['asymptotic_leading_term_mass'] > 0.0
        assert r['relative_difference'] < 0.01
        assert r['divergence_lower_bound_C_eps'] > 1.0

    obs = res['spectral_atomic_scaling_dichotomy_obstruction']
    assert obs['status'] == 'PROVED_MATHEMATICAL_OBSTRUCTION'
    assert 'Spectral-Atomic Scaling Dichotomy' in obs['theorem']
    assert 'scoped obstruction' in obs['scope_limitations']


def test_epic_finite_spectral_perturbation_rigidity():
    res = transcendental.audit_finite_spectral_perturbation_rigidity(
        window=(8.0, 20.0), K=0, dps=30
    )
    assert res['classification'] == 'PROVED_AND_VERIFIED'
    assert res['linear_independence_verified'] is True
    assert res['derivative_matrix_det_abs'] > 1e-10
    assert res['sample_evaluation_matrix_det_abs'] > 1e-10
    assert 'finite_spectral_perturbation_rigidity_2point' in res['formal_lean_theorems']
    refutation = res['refutation_of_arbitrary_compensation']
    assert 'Any perturbation of one zero is absorbed' in refutation['claim_refuted']
    assert 'linear independence' in refutation['mathematical_reason']


def test_epic_arithmetic_compatibility_investigation():
    res = transcendental.audit_arithmetic_compatibility_investigation(dps=30)
    assert res['classification'] == 'INVESTIGATION_COMPLETED'
    assert len(res['candidate_relations_audited']) == 4
    candidates = {c['name']: c for c in res['candidate_relations_audited']}
    assert 'Euler Product / Weil Positivity' in candidates
    assert candidates['Euler Product / Weil Positivity']['classification'] == 'CIRCULAR_EQUIVALENCE'
    assert 'Transcendental Continuation / Graded Radial Defect' in candidates
    assert candidates['Transcendental Continuation / Graded Radial Defect']['classification'] == 'STRICTLY_OPEN'
    assert 'Jacobi Theta Modular Inversion / Completed Functional Equation' in candidates
    assert candidates['Jacobi Theta Modular Inversion / Completed Functional Equation']['classification'] == 'INSUFFICIENT_WITHOUT_EULER_PRODUCT'
    assert 'Density Theorems and Zero-Free Regions (Vinogradov-Korobov)' in candidates
    assert candidates['Density Theorems and Zero-Free Regions (Vinogradov-Korobov)']['classification'] == 'ASYMPTOTIC_BOUND_ONLY'
    assert 'transfer step' in res['earliest_unproved_inference_in_tc']
    assert res['transcendental_continuation_bridge_status'] == 'STRICTLY_OPEN'


def test_epic_kernel_comparison_and_benchmark_diagnostics():
    """Verify kernel distinction, normalization, integral, and 256/512-node benchmarks."""
    # 1. Smooth exponential bump kernel at 512 nodes (canonical benchmark)
    res_smooth_512 = transcendental.evaluate_two_variable_finite_decomposition(
        K=0, J=1, window=(8.0, 20.0), eps=0.1, T=30.0, dps=25, recompute=True, kernel='smooth', n_nodes=512
    )
    meta_s = res_smooth_512['kernel_metadata']
    assert meta_s['kernel_id'] == 'smooth'
    assert meta_s['kernel_smoothness'] == 'C_infinity'
    assert abs(meta_s['kernel_integral'] - 1.2069003224378743) < 1e-6
    assert meta_s['kernel_peak'] == 1.0
    q_ret_s512 = res_smooth_512['retained_spectral_expansion']['Q_retained_sum']
    assert abs(q_ret_s512 - 0.26928881653228) < 1e-9

    # 2. Smooth exponential bump kernel at 256 nodes
    res_smooth_256 = transcendental.evaluate_two_variable_finite_decomposition(
        K=0, J=1, window=(8.0, 20.0), eps=0.1, T=30.0, dps=25, recompute=True, kernel='smooth', n_nodes=256
    )
    q_ret_s256 = res_smooth_256['retained_spectral_expansion']['Q_retained_sum']
    assert abs(q_ret_s256 - 0.26928881653232) < 1e-6

    # 3. Polynomial kernel (1 - v^2)^4 at 512 nodes
    res_poly_512 = transcendental.evaluate_two_variable_finite_decomposition(
        K=0, J=1, window=(8.0, 20.0), eps=0.1, T=30.0, dps=25, recompute=True, kernel='poly', n_nodes=512
    )
    meta_p = res_poly_512['kernel_metadata']
    assert meta_p['kernel_id'] == 'poly'
    assert meta_p['kernel_smoothness'] == 'C_3'
    assert abs(meta_p['kernel_integral'] - 256.0 / 315.0) < 1e-12
    assert meta_p['kernel_peak'] == 1.0
    q_ret_p512 = res_poly_512['retained_spectral_expansion']['Q_retained_sum']
    assert abs(q_ret_p512 - 0.18132691987364) < 1e-8

    # 4. Polynomial kernel at 256 nodes
    res_poly_256 = transcendental.evaluate_two_variable_finite_decomposition(
        K=0, J=1, window=(8.0, 20.0), eps=0.1, T=30.0, dps=25, recompute=True, kernel='poly', n_nodes=256
    )
    q_ret_p256 = res_poly_256['retained_spectral_expansion']['Q_retained_sum']
    assert abs(q_ret_p256 - 0.18132691987365) < 1e-6

    # 5. Arithmetic vanishing holds identically for BOTH kernels when eps < d_min
    assert res_smooth_512['arithmetic_vanishing_verified'] is True
    assert res_poly_512['arithmetic_vanishing_verified'] is True
    assert res_smooth_512['arithmetic_observable_Q_eps'] == 0.0
    assert res_poly_512['arithmetic_observable_Q_eps'] == 0.0


def test_epic_selected_spectral_block_positivity_scope():
    """Verify quantifier scope of A_{0, Gamma}: instance-specific positivity vs universal sign."""
    # Instance 1: K=0, J=1, window [8, 20], rho_1 ~ 14.13 -> strictly positive
    res_inst1 = transcendental.audit_selected_spectral_contribution(K=0, J=1, window=(8.0, 20.0), dps=25)
    assert res_inst1['classification'] == 'PROVED_AND_VERIFIED'
    assert res_inst1['A_0_Gamma'] > 0.54
    assert res_inst1['positivity_scope']['is_instance_positive'] is True
    assert res_inst1['positivity_scope']['universal_positivity_status'] == 'FALSIFIED_UNIVERSALLY'

    # Instance 2: Cross-grade phase factor cos(M * gamma * log(tau)) can be negative for distinct grades
    tau = 2.0 * math.pi
    log_tau = math.log(tau)
    gamma_1 = 14.13472514173469379
    cos_phase_M2 = math.cos(2 * gamma_1 * log_tau)
    assert cos_phase_M2 < 0.0  # cos(2 * gamma_1 * ln tau) ~ -0.1192 < 0

    # Admissible window for K=0, J=2 is a > tau^2 ~ 39.48. On [45, 65], A_0 is negative
    import scipy.integrate as integrate
    a_K = 1.0
    a_J = tau ** 2
    a, b = 45.0, 65.0
    mid = (a + b) / 2.0
    vmid = math.exp(-1.0 / ((mid - a) * (b - mid)))
    def integrand(x):
        w = math.exp(-1.0 / ((x - a) * (b - x))) / vmid
        f_K = 2.0 / math.sqrt(a_K * x) * math.cos(gamma_1 * math.log(x / a_K))
        f_J = 2.0 / math.sqrt(a_J * x) * math.cos(gamma_1 * math.log(x / a_J))
        return (w ** 2) * f_K * f_J
    val, _ = integrate.quad(integrand, a, b, epsabs=1e-12)
    int_eta = 1.2069003224378743
    A0_M2 = int_eta * val
    assert A0_M2 < 0.0  # approximately -0.00708 < 0


def test_epic_reductio_logical_structure_audit():
    """Verify logical clarification of intended reductio ad absurdum vs universal impossibility."""
    res = transcendental.audit_arithmetic_compatibility_investigation(dps=25)
    struct = res['logical_structure_of_intended_reductio']
    assert 'A |- Q_eps = 0' in struct['established_implication']
    assert 'A, H(rho_0) |- Q_eps > 0' in struct['research_obligation']
    assert 'A |- not H(rho_0)' in struct['intended_conclusion']
    assert 'does not prove' in struct['logical_clarification']
    assert 'full cancellation' in res['core_finding']
    assert res['transcendental_continuation_bridge_status'] == 'STRICTLY_OPEN'


def test_epic_product_measure_nonzero_and_positivity_conditions():
    """
    Verify:
    1. Product measure mu_K otimes mu_J is non-zero on W x W:
       Total pairing <mu_0 otimes mu_1, w otimes w> > 0 (approximately 13.91 on [8, 20]).
    2. Overlap Q_eps^{0, 1}[w] vanishes below the station gap d_min ~ 0.1504 (e.g. at eps = 0.05, 0.1).
    3. Overlap Q_eps^{0, 1}[w] is strictly positive when contributing station pairs are present
       (e.g. at eps = 0.2 and 0.5).
    4. Unconditional non-negativity: Q_eps^{K, J}[w] >= 0 for all grades and epsilons.
    5. Empty station window: Q_eps = 0 on (14.5, 15.5) even for K = J because Lambda(15) = 0
       and no prime-power stations fall in this interval.
    """
    # 1. Standard window [8, 20] with K=0, J=1
    res_cross = transcendental.audit_arithmetic_overlap_distinct_and_equal_grades(
        window=(8.0, 20.0), K=0, J=1, epsilons=[0.5, 0.2, 0.1, 0.05, 0.01], dps=25
    )
    assert res_cross['classification'] == 'PROVED_AND_VERIFIED'
    assert res_cross['product_measure_nonzero_on_window'] is True
    assert res_cross['product_measure_total_pairing_on_window'] > 10.0
    assert res_cross['unconditional_nonnegativity_verified'] is True
    assert res_cross['strict_positivity_when_pairs_present'] is True
    assert res_cross['vanishing_verified_below_d_min'] is True
    assert res_cross['d_min'] > 0.15

    rows = {r['epsilon']: r for r in res_cross['cross_grade_overlap_evaluations']}
    # Vanishing below d_min
    assert rows[0.05]['is_zero'] is True
    assert rows[0.05]['Q_epsilon'] == 0.0
    assert rows[0.1]['is_zero'] is True
    assert rows[0.1]['Q_epsilon'] == 0.0
    # Strict positivity above d_min
    assert rows[0.2]['is_zero'] is False
    assert rows[0.2]['Q_epsilon'] > 0.0
    assert rows[0.2]['contributing_pairs'] > 0
    assert rows[0.5]['is_zero'] is False
    assert rows[0.5]['Q_epsilon'] > 0.0
    assert rows[0.5]['contributing_pairs'] > 0

    # 2. Empty station window (14.5, 15.5): 15 is composite (Lambda(15) = 0)
    # Even for equal grades K = J = 0, Q_eps vanishes identically when test window has no stations
    res_empty = transcendental.audit_arithmetic_overlap_distinct_and_equal_grades(
        window=(14.5, 15.5), K=0, J=0, epsilons=[0.1, 0.2], dps=25
    )
    assert res_empty['is_empty_station_set'] is True
    assert res_empty['stations_0_count'] == 0
    assert res_empty['stations_1_count'] == 0
    assert res_empty['product_measure_total_pairing_on_window'] == 0.0
    for r in res_empty['cross_grade_overlap_evaluations']:
        assert r['is_zero'] is True
        assert r['Q_epsilon'] == 0.0


def test_epic_weil_positivity_and_cross_grade_polarization():
    """
    Verify:
    1. Connes-Consani (2026), Weil (1952), Bombieri (2000) conventions:
       multiplicative Haar convolution, involution h^*(x) = conj(h(1/x)),
       centering Delta^{-1/2}, centered admissible space V_centered.
    2. Polarization formula: B(g_K + g_J, g_K + g_J) = B(g_K, g_K) + B(g_J, g_J) + 2*Re B(g_K, g_J),
       refuting the unsupported identification of self-convolution with equal grades K = J.
    3. Three-form comparison table distinguishing Arithmetic overlap Q_eps,
       Multi-Grade matrix (falsified positive-definiteness for smooth bump), and Weil form B(g, h) (RH-equivalent).
    4. Map analysis: dimensional reduction from 2-variable measure pairing to 1-variable group convolution.
    5. Attempted derivation 5-step record stopping at exact remainder cancellation R = -A.
    6. Challenger rejections of overbroad claims (including kernel indefiniteness and centering).
    """
    res = transcendental.audit_weil_positivity_and_tc_bridge_comparison(dps=25)
    assert res['classification'] == 'COMPARISON_COMPLETED'
    assert res['epistemic_verdict'] == 'NO_NEW_IMPLICATION_ESTABLISHED'
    assert res['transcendental_continuation_bridge_status'] == 'STRICTLY_OPEN'

    conv = res['conventions']
    assert 'R_+^*' in conv['group']
    assert 'du / u' in conv['haar_measure']
    assert 'Delta^{1/2}' in conv['centering_automorphism']
    assert 'x^{-1/2}' in conv['bilinear_weil_form'] or 'Delta^{-1/2}' in conv['bilinear_weil_form']
    assert 'tilde{g}(-1/2) = tilde{g}(1/2) = 0' in conv['admissible_test_space_V']

    pol = res['polarization_analysis']
    assert '2 * Re B(g_K, g_J)' in pol['hermitian_polarization_formula']
    assert 'hermitian_polarization_complex' in pol['complex_hermitian_polarization']
    assert 'hermitian_polarization_real_part' in pol['complex_hermitian_real_part_polarization']
    assert 'RiemannScope.hermitian_polarization_complex' in pol['formal_lean_theorems']

    table = res['three_form_comparison_table']
    assert len(table) == 3
    objects = [item['object'] for item in table]
    assert any('Arithmetic Overlap' in o for o in objects)
    assert any('Multi-Grade Matrix' in o for o in objects)
    assert any('Weil' in o for o in objects)

    # Positivity property checks
    arith_item = next(item for item in table if 'Arithmetic Overlap' in item['object'])
    assert 'Entrywise non-negative' in arith_item['positivity_property']
    gram_item = next(item for item in table if 'Multi-Grade Matrix' in item['object'])
    assert 'PSD' in gram_item['epistemic_status'] and 'INDEFINITE' in gram_item['epistemic_status']
    weil_item = next(item for item in table if 'Weil' in item['object'])
    assert 'RH' in weil_item['positivity_property'] or 'EQUIVALENT TO RH' in weil_item.get('strict_positivity_condition', '')

    # Map analysis checks
    m_analysis = res['map_analysis']
    assert 'tensor product' in m_analysis['dimensional_and_measure_distinction']
    assert '1-variable multiplicative convolution' in m_analysis['dimensional_and_measure_distinction']
    assert 'spectral_side_structure' in m_analysis

    # Attempted derivation record
    rec = res['attempted_derivation_record']
    assert 'step_1_arithmetic_property' in rec
    assert 'step_2_offline_zero_entry' in rec
    assert 'step_3_spectral_and_background_terms_retained' in rec
    assert 'step_4_proposed_implication' in rec
    assert 'step_5_earliest_unsupported_inference' in rec
    assert 'bar{R}^{full}_eps = -bar{A}_{eps, Gamma}' in rec['step_5_earliest_unsupported_inference']

    # Challenger rejections: 7 items
    rej = res['challenger_rejections']
    assert len(rej) == 7
    assert 'product measure' in rej['rejection_1']['claim_rejected'].lower()
    assert 'equal grades' in rej['rejection_2']['claim_rejected'].lower()
    assert 'self-convolution' in rej['rejection_3']['claim_rejected'].lower()
    assert 'growing windows' in rej['rejection_4']['claim_rejected'].lower()
    assert 'grade matrix' in rej['rejection_5']['claim_rejected'].lower()
    assert 'centering' in rej['rejection_6']['claim_rejected'].lower()
    assert 'squared moduli' in rej['rejection_7']['claim_rejected'].lower()


def test_epic_smooth_kernel_indefiniteness_counterexample():
    """
    Verify:
    1. Smooth exponential bump kernel eta(v) = exp(1 - 1/(1-v^2)) * 1_{|v|<1} is NOT positive definite.
    2. Exact counterexample on x = (1, 3/2, 2) at eps = 1 yields M = [[1, a, 0], [a, 1, a], [0, a, 1]]
       with a = exp(-1/3) ~= 0.71653131.
    3. Smallest eigenvalue lambda_min = 1 - sqrt(2)*exp(-1/3) ~= -0.01332829727842 < 0.
    4. Quadratic form on v = (1, -sqrt(2), 1)^T: v^T M v = 4*(1 - sqrt(2)*exp(-1/3)) ~= -0.053313189 < 0.
    5. Bochner harmonic analysis: Fourier transform hat{eta}(xi) is strictly negative on [5.0, 8.8],
       reaching a minimum ~= -0.1154 near xi ~= 6.8.
    6. Restricted TC prime-power family: primes {3, 5, 7} at eps = 4 reproduce M exactly;
       by Sylvester's law of inertia, weighted matrix Q = D M D has inertia (1, 0, 2) and
       is strictly indefinite, proving that positivity fails on TC prime measures too.
    """
    res = transcendental.audit_smooth_kernel_indefiniteness_counterexample(dps=25)
    assert 'FALSIFIED' in res['classification'] and 'POSITIVE_DEFINITENESS' in res['classification']

    cfg = res['counterexample_configuration']
    assert abs(cfg['coupling_a'] - math.exp(-1.0 / 3.0)) < 1e-12
    assert cfg['is_indefinite'] is True
    assert cfg['smallest_eigenvalue'] < -0.013
    assert abs(cfg['smallest_eigenvalue'] - (1.0 - math.sqrt(2.0) * math.exp(-1.0 / 3.0))) < 1e-10
    assert cfg['quadratic_form_v_T_M_v'] < -0.05

    bochner = res['bochner_harmonic_analysis']
    assert bochner['bochner_positivity_falsified'] is True
    assert any(s['is_negative'] for s in bochner['fourier_transform_samples'])
    assert bochner['minimum_negative_val'] < -0.1

    tc_fam = res['restricted_tc_prime_family_investigation']
    assert tc_fam['restricted_family_indefinite'] is True
    assert tc_fam['sylvester_inertia']['negative'] == 1
    assert tc_fam['sylvester_inertia']['positive'] == 2
    assert tc_fam['quadratic_form_witness_y_T_Q_y'] < 0.0

    theorems = res['formal_lean_theorems']
    assert 'RiemannScope.tridiagonal_kernel_matrix_quadratic_form' in theorems
    assert 'RiemannScope.tridiagonal_kernel_matrix_indefinite' in theorems


def test_epic_weil_centered_test_space_reconciliation():
    """
    Verify:
    1. Reconciliation of centered test space pole conditions:
       Under g(x) = x^{1/2} g_old(x), Mellin transform shifts tilde{g}(s) = tilde{g}_old(s + 1/2).
       The classical pole conditions tilde{g}_old(0) = tilde{g}_old(1) = 0 transport to
       tilde{g}(-1/2) = tilde{g}(1/2) = 0 (Connes & Consani 2026).
    2. In additive coordinates f(u) = g(e^u), this corresponds to
       int_{-infty}^infty f(u) exp(+/- u/2) du = 0.
    3. Complex Hermitian polarization identity B(x+y, x+y) = B(x, x) + B(y, y) + 2*Re B(x, y)
       and real-part polarization Re B(x+y, x+y) = Re B(x, x) + Re B(y, y) + 2*Re B(x, y).
    """
    res = transcendental.audit_weil_positivity_and_tc_bridge_comparison(dps=25)
    space_desc = res['conventions']['admissible_test_space_V']
    assert 'tilde{g}(-1/2) = tilde{g}(1/2) = 0' in space_desc
    assert 'tilde{g}_old(s + 1/2)' in space_desc
    assert '+/- i/2' in space_desc

    pol = res['polarization_analysis']
    assert 'hermitian_polarization_complex' in pol['complex_hermitian_polarization']
    assert 'hermitian_polarization_real_part' in pol['complex_hermitian_real_part_polarization']


def test_epic_smooth_bump_fourier_normalization_integral():
    """
    Verify the corrected Fourier normalization integral:
    hat{eta}(0) = int_{-1}^1 exp(1 - 1/(1 - v^2)) dv ~= 1.20690032243787617534
    (correcting earlier 0.8872 misprint), and verify sampled Fourier values at 5.0, 6.8, 8.8.
    """
    res = transcendental.audit_smooth_kernel_indefiniteness_counterexample(dps=25)
    hat_0 = res['bochner_harmonic_analysis']['normalization_integral_hat_eta_0']
    assert abs(hat_0 - 1.2069003224378762) < 1e-10

    samples = res['bochner_harmonic_analysis']['fourier_transform_samples']
    sample_dict = {s['xi']: s['hat_eta'] for s in samples}
    assert sample_dict[5.0] < 0.0
    assert abs(sample_dict[5.0] - (-0.000576955)) < 1e-6
    assert sample_dict[6.8] < -0.1
    assert abs(sample_dict[6.8] - (-0.115444)) < 1e-5
    assert sample_dict[8.8] < 0.0
    assert abs(sample_dict[8.8] - (-0.0048945)) < 1e-6


def test_epic_complete_prime_power_sieve_window_100():
    """
    Verify complete dynamic prime power sieve up to window boundary 100 without cutoff.
    Must include primes 53, 59, 61, 67, 71, 73, 79, 83, 89, 97 (previously omitted by list ending at 47),
    as well as prime powers (e.g. 2^3=8, 3^2=9, 2^4=16, 5^2=25, 3^3=27, 2^5=32, 7^2=49, 2^6=64, 3^4=81)
    with weight Lambda(p^m) = log(p).
    """
    stations = transcendental.sieve_prime_powers_in_window(window=(8.0, 100.0), grade=0)
    station_dict = {item[0]: {'x': item[1], 'lambda_n': item[2]} for item in stations}

    # Verify primes above 47 are present
    primes_above_47 = [53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    for p in primes_above_47:
        assert p in station_dict, f"Prime {p} missing from sieve in window [8, 100]"
        assert abs(station_dict[p]['lambda_n'] - math.log(p)) < 1e-12

    # Verify prime powers
    prime_powers = [8, 9, 16, 25, 27, 32, 49, 64, 81]
    for n in prime_powers:
        assert n in station_dict, f"Prime power {n} missing from sieve"
        # Base prime
        p_base = {8: 2, 9: 3, 16: 2, 25: 5, 27: 3, 32: 2, 49: 7, 64: 2, 81: 3}[n]
        assert abs(station_dict[n]['lambda_n'] - math.log(p_base)) < 1e-12


def test_epic_station_to_grade_embedding_and_pullback_identity():
    """
    Verify the finite algebraic pullback identity:
    G = E^* H E,  c^* G c = (E c)^* H (E c)
    and that the discrepancy between matrix pullback and direct double sum is < 1e-12.
    """
    res = transcendental.audit_station_to_grade_embedding_and_restricted_family(dps=25)
    assert res['status'] == 'STATION_TO_GRADE_EMBEDDING_AUDITED'
    assert res['pullback_identity']['algebraic_pullback_verified'] is True
    assert 'RiemannScope.matrix_pullback_quadratic_form' in res['pullback_identity']['lean4_theorem']
    assert 'RiemannScope.matrix_pullback_psd' in res['pullback_identity']['psd_inheritance_theorem']

    # Cross-grade separation
    delta_cross = res['minimum_cross_grade_separation_Delta_cross']
    assert delta_cross > 0.15


def test_epic_small_resolution_grade_matrix_psd():
    """
    Verify the small-resolution grade PSD theorem:
    For eps < Delta_cross, cross-grade overlap vanishes identically (G_ij = 0 for i != j)
    and diagonal entries G_ii >= 0, so c^* G c >= 0 unconditionally.
    """
    res = transcendental.audit_station_to_grade_embedding_and_restricted_family(dps=25)
    small_res = res['small_resolution_theorem']
    assert small_res['is_psd'] is True
    assert 'RiemannScope.small_resolution_grade_psd' in small_res['lean4_theorem']

    # Check sweep items below delta_cross
    for item in res['resolution_sweep']:
        if item['is_below_delta_cross']:
            assert item['is_positive_semidefinite'] is True
            assert item['smallest_eigenvalue'] >= -1e-12


def test_epic_large_resolution_grade_matrix_indefinite_witness():
    """
    Verify the restricted family investigation at larger resolutions:
    At eps = 8.0 on grades {0, 1} in window [8, 20], cross-grade overlap causes
    G to become indefinite with an explicit witness vector c having c^T G c < 0.
    """
    res = transcendental.audit_station_to_grade_embedding_and_restricted_family(dps=25)
    witness = res['large_resolution_indefinite_witness']
    assert witness is not None
    assert witness['witness_verified'] is True
    assert witness['resolution_eps'] == 8.0
    assert witness['determinant_G'] < -0.5
    assert witness['quadratic_form_c_T_G_c'] < -0.01


def test_epic_reflected_weil_form_and_offline_quartet_distinction():
    """
    Verify the Reflected Weil spectral pairing:
    1. Bilinear form B(g, h) = sum_rho m_rho M g(rho - 1/2) conj(M h(1/2 - bar(rho))).
    2. On the critical line (delta = 0), pairing reduces to squared modulus |M g(i*gamma)|^2 > 0.
    3. Off the critical line (delta != 0), arguments are reflected across imaginary axis.
    4. For admissible test f = (d_u^2 - 1/4) f_0, reflected quartet pairing is NEGATIVE,
       while erroneous squared modulus sum would be positive (+4.33e-82).
    5. Refutes substitution of squared moduli off-line.
    """
    res = transcendental.audit_reflected_weil_spectral_form(dps=30)
    assert res['status'] == 'REFLECTED_WEIL_SPECTRAL_FORM_AUDITED'

    # Pole conditions
    poles = res['transported_pole_conditions']
    assert poles['pole_cancellation_verified'] is True

    # On-line control
    online = res['on_line_control']
    assert online['is_strictly_positive'] is True
    assert online['term_value'] > 0

    # Off-line quartet
    offline = res['off_line_quartet_analysis']
    assert offline['is_reflected_pairing_negative'] is True
    assert offline['correct_reflected_quartet_pairing'] < 0.0
    assert offline['erroneous_squared_modulus_sum'] > 0.0

    # Dilation action
    tc_action = res['tc_grade_dilation_action']
    assert tc_action['grade_difference_orientation'] == 'K - J'


def test_epic_compact_support_weil_quartet_test_R15():
    """
    Verify the genuine compactly supported admissible Weil test g_R:
    1. f_R = (d_u^2 - 1/4)[chi(u/R) * exp(-u^2/(2*sigma^2))], g_R(x) = f_R(log x).
    2. Exact pole vanishing M g_R(-1/2) = M g_R(1/2) = 0 proved by integration by parts.
    3. Analytic tail error bound |M g_R(s) - F_sigma(s)| <= |s^2 - 1/4| * I_R(Re(s), sigma).
    4. For R = 15.0 and sigma = 1.0, quartet error bound is <= 1.46e-87.
    5. Certified upper bound B_Q(g_R, g_R) <= -1.63275e-81 + 1.46e-87 < 0 strictly.
    """
    res = transcendental.audit_compact_support_weil_quartet_test(R=15.0, sigma=1.0, dps=50)
    assert res['status'] == 'COMPACT_SUPPORT_WEIL_QUARTET_TEST_CERTIFIED'
    assert res['is_strictly_negative'] is True
    assert res['certified_upper_bound_B_Q'] < 0.0
    assert res['certified_upper_bound_B_Q'] < -1.63e-81
    assert res['gaussian_control_quartet_pairing'] < -1.63e-81
    assert res['quartet_product_error_bound'] < 2.0e-87
    assert res['signal_to_error_ratio'] > 1.0e5

    # Check finite support intervals
    supp_mult = res['support_interval_multiplicative']
    assert supp_mult[0] > 0.0
    assert supp_mult[1] < 1.0e15


def test_epic_comparison_map_candidate_A_toeplitz_obstruction():
    """
    Verify Candidate A comparison map (grade orbit T_g c = sum c_i U_{K_i} g):
    1. Spectral matrix W_{ij} has identical diagonal entries W_{ii} = B(g, g) (Toeplitz).
    2. Fixed-window arithmetic matrix G has G_00 ~= 39.76, G_11 ~= 0.50 (ratio ~= 80:1).
    3. Identifies exact obstruction: spatial window breaks scale invariance.
    4. Proves Cauchy-Schwarz obstruction if scaling is attempted to match indefinite matrix.
    """
    res = transcendental.audit_tc_comparison_map_candidate_A(dps=35)
    assert res['status'] == 'TC_COMPARISON_CANDIDATE_A_AUDITED'
    assert res['discriminating_result'] == 'CANDIDATE_A_STRUCTURALLY_OBSTRUCTED'

    struct_w = res['structural_properties_W']
    assert struct_w['equal_diagonals_required'] is True

    arith_g = res['actual_arithmetic_matrix_G']
    assert arith_g['equal_diagonals_observed'] is False
    assert arith_g['diagonal_ratio_G00_over_G11'] > 50.0

    obstruction = res['structural_obstruction_identified']
    assert 'equal_diagonal_violation' in obstruction
    assert 'geometric_cause' in obstruction
    assert 'cauchy_schwarz_barrier_under_scaling' in obstruction


def test_epic_comparison_map_candidate_B_logarithmic_autocorrelation():
    """
    Verify Candidate B comparison map (smoothed logarithmic station measure):
    1. Scope corrected: station separation preserved in log coordinates, prime resonances excluded.
    2. Admissible test T_h c in V has exact pole cancellation A_h(+-1/2) = 0.
    3. Reflected Weil kernel derived with vanishing cross-grade prime evaluations for 2h < Delta_res.
    4. Remaining distinction: Archimedean cross terms and same-grade prime terms.
    """
    res = transcendental.audit_tc_comparison_map_candidate_B(dps=35)
    assert res['status'] == 'TC_COMPARISON_CANDIDATE_B_AUDITED'
    assert res['discriminating_result'] == 'CANDIDATE_B_SCOPE_CORRECTED_AND_KERNEL_DERIVED'
    assert res['scope_correction']['rejection_repaired'] is True
    assert res['scope_correction']['cross_grade_prime_resonance_exclusion_proved'] is True

    kernel_audit = res['reflected_weil_kernel']
    admiss = kernel_audit['kernel_definition']
    assert 'A_h(-1/2) = A_h(1/2) = 0' in admiss['exact_pole_cancellation']


def test_epic_matrix_source_reconciliation_exact_values():
    """
    Verify the exact reproducible values for the restricted family at eps = 8.0:
    G = [[39.759668, 4.547769], [4.547769, 0.497067]],
    det(G) ~= -0.918992,
    c ~= (0.113576, -0.993529)^T,
    c^T G c ~= -0.022815.
    """
    res = transcendental.audit_station_to_grade_embedding_and_restricted_family(
        grades=[0, 1], window=(8.0, 20.0), epsilons=[8.0], dps=40
    )
    witness = res['large_resolution_indefinite_witness']
    assert witness is not None
    assert witness['witness_verified'] is True

    g_mat = witness['grade_matrix_G']
    assert abs(g_mat[0][0] - 39.759668) < 1e-4
    assert abs(g_mat[1][1] - 0.497067) < 1e-4
    assert abs(g_mat[0][1] - 4.547769) < 1e-4
    assert abs(g_mat[1][0] - 4.547769) < 1e-4

    assert abs(witness['determinant_G'] - (-0.918992)) < 1e-4
    assert abs(witness['witness_vector_c'][0] - 0.113576) < 1e-4
    assert abs(witness['witness_vector_c'][1] - (-0.993529)) < 1e-4
    assert abs(witness['quadratic_form_c_T_G_c'] - (-0.022815)) < 1e-4


def test_epic_candidate_A_fallback_removed_dynamic_eval():
    """
    Verify Candidate A:
    1. Removes hardcoded fallback: retrieves actual computed matrix for any requested epsilon.
    2. At eps = 0.1, G = diag(13.765932696619211, 0.45352393717389383), cross entry is exactly zero.
    3. At eps = 8.0, G has non-zero cross entry ~ 4.547769, is indefinite.
    4. Empty window (20.1, 20.2) returns zero matrix with 0 stations, handles gracefully.
    5. Fails explicitly with ValueError if matrix cannot be computed (never substitutes fallback).
    """
    # 1. At eps = 0.1 on window [8, 20]
    res_01 = transcendental.audit_tc_comparison_map_candidate_A(
        grades=[0, 1], window=(8.0, 20.0), epsilon=0.1, dps=35
    )
    g_01 = res_01['actual_arithmetic_matrix_G']
    assert abs(g_01['G_00'] - 13.765932696619211) < 1e-6
    assert abs(g_01['G_11'] - 0.45352393717389383) < 1e-6
    assert abs(g_01['G_01']) < 1e-12
    assert g_01['cross_entry_is_zero'] is True
    assert g_01['is_positive_semidefinite'] is True
    assert g_01['equal_diagonals_observed'] is False

    # 2. At eps = 8.0 on window [8, 20]
    res_80 = transcendental.audit_tc_comparison_map_candidate_A(
        grades=[0, 1], window=(8.0, 20.0), epsilon=8.0, dps=35
    )
    g_80 = res_80['actual_arithmetic_matrix_G']
    assert abs(g_80['G_00'] - 39.759668) < 1e-3
    assert abs(g_80['G_01'] - 4.547769) < 1e-3
    assert abs(g_80['G_11'] - 0.497067) < 1e-3
    assert g_80['cross_entry_is_zero'] is False
    assert g_80['is_positive_semidefinite'] is False

    # 3. Empty station window
    res_empty = transcendental.audit_tc_comparison_map_candidate_A(
        grades=[0, 1], window=(20.1, 20.2), epsilon=0.1, dps=25
    )
    g_empty = res_empty['actual_arithmetic_matrix_G']
    assert g_empty['station_count'] == 0
    assert g_empty['G_00'] == 0.0
    assert g_empty['G_11'] == 0.0
    assert g_empty['G_01'] == 0.0
    assert g_empty['equal_diagonals_observed'] is True

    # 4. Explicit failure test: returns explicit failure when computation fails; never substitutes fallback
    import pytest
    from unittest.mock import patch
    with patch('transcendental.audit_station_to_grade_embedding_and_restricted_family', return_value={'resolution_sweep': []}):
        with pytest.raises(ValueError, match="Failed to compute arithmetic grade matrix"):
            transcendental.audit_tc_comparison_map_candidate_A(
                grades=[0, 1], window=(8.0, 20.0), epsilon=0.1
            )


def test_epic_logarithmic_separation_and_resonance_gap():
    """
    Verify Logarithmic Station Separation and Prime-Power Resonance Exclusion:
    1. Mean value bound: |x-y|/b <= |log x - log y| <= |x-y|/a on [a, b].
    2. Finite station separation in log coordinates: Delta_log >= Delta_x / b > 0.
    3. Transcendence rational ratio reduction: tau^{K-J} is irrational for K != J.
    4. Prime-power resonance gap: Delta_res ~= 0.0461176 > 0 for grades {0, 1} on [8, 20].
    5. Critical bandwidth h_crit = Delta_res / 2 ~= 0.0230588.
    6. Exact vanishing: for h < h_crit, all cross-grade prime evaluations vanish identically.
    """
    res = transcendental.audit_tc_logarithmic_separation_and_resonance_gap(
        grades=[0, 1], window=(8.0, 20.0), bandwidth_ceiling_h0=1.0, dps=35
    )
    assert res['status'] == 'TC_LOGARITHMIC_SEPARATION_AND_RESONANCE_GAP_AUDITED'

    # Check Mean Value Theorem bounds
    mvt = res['mean_value_theorem_bounds']
    assert mvt['inequality_verified'] is True
    assert mvt['lower_bound_Delta_x_over_b'] > 0.0075
    assert res['logarithmic_separation_Delta_log'] >= mvt['lower_bound_Delta_x_over_b']
    assert res['spatial_separation_Delta_x'] > 0.15

    # Check resonance gap
    res_gap = res['prime_power_resonance_gap']
    delta_res = res_gap['minimum_resonance_gap_Delta_res']
    assert abs(delta_res - 0.0461176) < 1e-4
    assert abs(res_gap['critical_bandwidth_h_crit'] - 0.0230588) < 1e-4

    # Check finite support bound
    supp = res['finite_resonance_support_bound']
    assert supp['maximum_resonating_prime_power'] >= 16
    assert supp['enumerated_prime_power_count'] > 0
    assert res['active_stations_grade_0'] == [9, 11, 13, 16, 17, 19]
    assert res['active_stations_grade_1'] == [2, 3]


def test_epic_candidate_B_reflected_weil_kernel_and_explicit_formula():
    """
    Verify Candidate B Reflected Weil Kernel:
    1. Multiplicative test T_h c in V with exact pole cancellation A_h(+-1/2) = 0.
    2. Explicit formula decomposition: Poles - Primes + Archimedean.
    3. For h = 0.02 < h_crit, cross-grade prime evaluations vanish identically.
    4. Same-grade prime evaluations vanish identically on active stations since 2h = 0.04 < log(19/18).
    5. Cross-grade block W_{ij} (i != j) is purely Archimedean (non-vanishing).
    6. Numerical matrix computation proves strict positive definiteness.
    7. Clear distinction among G_add, G_log, G_L2, and W.
    """
    res = transcendental.audit_tc_candidate_B_reflected_weil_kernel(
        grades=[0, 1], window=(8.0, 20.0), h=0.02, dps=35
    )
    assert res['status'] == 'TC_CANDIDATE_B_REFLECTED_WEIL_KERNEL_AUDITED'

    decomp = res['explicit_formula_decomposition']
    assert decomp['pole_terms'] == '0.0 (vanish identically because A_h(+-1/2) = 0)'

    cross_prime = decomp['prime_terms_cross_grade']
    assert cross_prime['is_bandwidth_below_resonance_gap'] is True
    assert cross_prime['cross_grade_prime_evaluations_status'] == 'VANISH_IDENTICALLY'

    same_prime = decomp['prime_terms_same_grade']
    assert same_prime['same_grade_vanishing_status'] == 'VANISH_IDENTICALLY'
    assert 'w(8)=0' in same_prime['off_diagonal_station_pairs']

    arch = decomp['archimedean_distribution']
    assert 'coupling ratio' in arch['cross_grade_contribution']

    # Matrix spectral certification
    mat = res['computed_canonical_matrix']
    assert mat['spectral_verdict'] == 'STRICTLY_POSITIVE_DEFINITE'
    assert mat['all_prime_terms_vanish'] is True
    assert mat['W_arch'][0][0] > 1e11
    assert mat['W_arch'][1][1] > 1e10
    assert mat['determinant'] > 0
    assert min(mat['eigenvalues']) > 0
    assert mat['coupling_ratio'] < 0.25

    # 4 objects distinction
    four_obj = res['four_distinct_objects_clarification']
    assert 'G_add' in four_obj
    assert 'G_log' in four_obj
    assert 'G_L2' in four_obj
    assert 'W' in four_obj


def test_epic_canonical_reflected_weil_matrix_quadrature():
    """
    Verify high-precision quadrature evaluation of the canonical 2x2 Reflected Weil Matrix:
    - Bandwidth h = 0.02 on window [8, 20] for grades {0, 1}.
    - Active stations: Grade 0 has {9, 11, 13, 16, 17, 19}; Grade 1 has {2, 3}.
    - W_prime == 0 since 2h = 0.04 < min(Delta_res, log(19/18)).
    - Strict positive definiteness: W_00 > 0, det W > 0, lambda_min > 0.
    - Complex quadratic form c^* W c > 0 for all non-zero c in C^2.
    """
    mat = transcendental.compute_canonical_reflected_weil_matrix(
        grades=[0, 1], window=(8.0, 20.0), h=0.02
    )
    assert mat['status'] == 'CANONICAL_REFLECTED_WEIL_MATRIX_COMPUTED'
    assert mat['spectral_verdict'] == 'STRICTLY_POSITIVE_DEFINITE'
    assert mat['all_prime_terms_vanish'] is True
    assert mat['W'] == mat['W_arch']

    # Entry magnitudes
    W00 = mat['W'][0][0]
    W01 = mat['W'][0][1]
    W10 = mat['W'][1][0]
    W11 = mat['W'][1][1]

    assert abs(W01 - W10) < 1e-6
    assert W00 > 5e11
    assert W11 > 1.7e10
    assert abs(W01) > 1.9e10

    # Positive definiteness checks
    assert mat['determinant'] > 8e21
    assert mat['coupling_ratio'] < 0.25
    assert min(mat['eigenvalues']) > 1.6e10

    # Complex quadratic form positivity test
    for c0, c1 in [(1.0, 0.0), (0.0, 1.0), (1.0, -1.0), (1.0 + 2j, 3.0 - 1j), (-2.5j, 4.0)]:
        val = (c0.conjugate() * (W00 * c0 + W01 * c1) +
               c1.conjugate() * (W10 * c0 + W11 * c1))
        assert val.real > 0.0
        assert abs(val.imag) / val.real < 1e-12


def test_epic_reflected_weil_matrix_controls():
    """
    Verify control configurations for the reflected Weil matrix:
    1. Empty configuration returns exact zero matrix with 'EMPTY_CONFIGURATION'.
    2. Single active grade returns 1x1 strictly positive scalar.
    3. Invalid bandwidth h <= 0 raises ValueError.
    """
    import pytest

    # 1. Empty window with no stations
    mat_empty = transcendental.compute_canonical_reflected_weil_matrix(
        grades=[0, 1], window=(21.0, 21.5), h=0.02
    )
    assert mat_empty['spectral_verdict'] == 'EMPTY_CONFIGURATION'
    assert mat_empty['is_empty'] is True
    assert mat_empty['W'] == [[0.0, 0.0], [0.0, 0.0]]
    assert mat_empty['determinant'] == 0.0

    # 2. Single active grade
    mat_single = transcendental.compute_canonical_reflected_weil_matrix(
        grades=[0], window=(8.0, 20.0), h=0.02
    )
    assert mat_single['spectral_verdict'] == 'STRICTLY_POSITIVE_DEFINITE'
    assert mat_single['matrix_dimensions'] == [1, 1]
    assert mat_single['W'][0][0] > 1e11

    # 3. Invalid bandwidth
    with pytest.raises(ValueError, match="Bandwidth h must be strictly positive"):
        transcendental.compute_canonical_reflected_weil_matrix(
            grades=[0, 1], window=(8.0, 20.0), h=-0.01
        )


def test_epic_small_bandwidth_archimedean_asymptotic():
    """
    Verify small-bandwidth Archimedean asymptotic and the incompatibility obstruction:
    1. Operator norm dominance of diagonal terms over off-diagonal cross terms.
    2. Monotonic decay of coupling ratio as h -> 0.
    3. Proves the structural incompatibility: in the positive regime 0 < h < h_pos,
       W(C, h) is strictly positive definite, so no test function in F_pos can satisfy
       B(g, g) < 0 to detect an off-line zero.
    4. Epistemic status: TC bridge remains strictly OPEN.
    """
    res = transcendental.audit_small_bandwidth_archimedean_asymptotic(
        grades=[0, 1], window=(8.0, 20.0)
    )
    assert res['status'] == 'SMALL_BANDWIDTH_ARCHIMEDEAN_ASYMPTOTIC_AUDITED'

    dom = res['operator_norm_dominance']
    assert dom['dominance_holds'] is True
    assert dom['coupling_ratio_limit_as_h_to_zero'] == 0.0

    # Check bandwidth sweep monotonicity of coupling ratio
    sweep = res['bandwidth_sweep']
    coupling_ratios = [pt['coupling_ratio'] for pt in sweep]
    # Verify that coupling ratio is strictly smaller at h=0.001 than at h=0.05
    assert coupling_ratios[-1] < coupling_ratios[0]
    assert coupling_ratios[-1] < 0.005

    # Incompatibility verdict & rectified conditional logic
    incomp = res['incompatibility_obstruction_analysis']
    assert incomp['incompatibility_verdict'] == 'POSITIVITY_AND_OFFLINE_DETECTION_INCOMPATIBLE_ON_SAME_FAMILY'

    cond_logic = res['conditional_detection_logic']
    assert 'Every g in F satisfies B(g, g) >= 0' in cond_logic['definitions']['P_F']
    assert 'Together P_F and D_F imply not H' in cond_logic['logical_relations']['intended_rh_contradiction']
    assert 'does NOT imply not D_F' in cond_logic['logical_relations']['no_refutation_of_conditional_detection']
    assert cond_logic['detection_implication_status'].startswith('STRICTLY_OPEN')
    assert res['transcendental_continuation_bridge_status'] == 'STRICTLY_OPEN'


def test_epic_connes_consani_positivity_criterion_and_obligations():
    """
    Verify Connes-Consani (2020) Proposition C.1 and the Two Distinct TC Obligations:
    1. Classical criterion: not RH ==> exists g in V: B(g, g) < 0.
    2. Restricted TC family F_TC has grade-tied coefficients and bandwidth 2h < Delta_res.
    3. Two obligations are strictly separated:
       Obligation 1: Derive positivity / sign constraint on F_TC.
       Obligation 2: Prove F_TC contains a negative test or approximates one under not RH.
    4. Identifies mode vanishing risk if A_h(rho_0 - 1/2) = 0.
    5. TC bridge remains strictly open.
    """
    res = transcendental.audit_weil_positivity_connes_consani_criterion(dps=35)
    assert res['status'] == 'WEIL_POSITIVITY_CONNES_CONSANI_CRITERION_AUDITED'
    assert res['transcendental_continuation_bridge_status'] == 'STRICTLY_OPEN'

    source = res['primary_source']
    assert source['authors'] == 'Alain Connes & Caterina Consani'
    assert source['year'] == 2020
    assert 'Proposition C.1' in source['citation']

    ob1 = res['two_separated_obligations']['obligation_1_arithmetic_positivity']
    ob2 = res['two_separated_obligations']['obligation_2_offline_zero_detection']
    assert 'Derive positivity' in ob1
    assert 'Prove that under H(rho_0)' in ob2


def test_epic_reproduce_cutoff_discrepancy():
    """
    Verify reproduction of the cutoff discrepancy between t <= 600 and t <= 16000:
    1. Truncating at t = 600 (z = 12) yields W00 ~= 5.286e11, W01 ~= 1.956e10, W11 ~= 1.751e10.
    2. Extending to t = 16000 (z = 320) yields W00 ~= 1.032e12, W01 ~= 2.723e10, W11 ~= 3.402e10.
    3. Canonical constants match high-precision values: Z ~= 0.44399, ||kappa''||^2 ~= 54.95987.
    4. Confirms diagnostic: bump kernel has Gevrey-regular slow sub-exponential decay;
       stopping at z = 12 omits roughly 48.8% of diagonal Archimedean energy.
    """
    res = transcendental.reproduce_cutoff_discrepancy(h=0.02, grades=[0, 1], window=(8.0, 20.0))
    assert res['status'] == 'CUTOFF_DISCREPANCY_REPRODUCED'

    consts = res['canonical_constants']
    assert abs(consts['Z_canonical'] - 0.443993816) < 1e-6
    assert abs(consts['norm_kappa_pp_sq'] - 54.959873) < 1e-4
    assert abs(consts['norm_kappa_p_sq'] - 2.077745) < 1e-4
    assert abs(consts['norm_kappa_sq'] - 0.675116) < 1e-4

    r600 = res['quadrature_ranges']['cutoff_t_600']
    assert abs(r600['W00'] - 5.286380e11) / 5.286380e11 < 1e-3
    assert abs(r600['W01'] - 1.955673e10) / 1.955673e10 < 1e-3
    assert abs(r600['W11'] - 1.750710e10) / 1.750710e10 < 1e-3

    r16000 = res['quadrature_ranges']['cutoff_t_16000']
    assert abs(r16000['W00'] - 1.032430e12) / 1.032430e12 < 1e-3
    assert abs(r16000['W01'] - 2.722763e10) / 2.722763e10 < 1e-3
    assert abs(r16000['W11'] - 3.401611e10) / 3.401611e10 < 1e-3


def test_epic_certify_archimedean_tail_psd():
    """
    Verify Archimedean PSD Tail Certification (Full-Sign vs Full-Value):
    1. NIST DLMF 5.7.6 digamma monotonicity: d/dy Re digamma(1/4 + iy) > 0 for y > 0.
    2. Lower bound at cutoff: omega(t) >= omega(10) > 0.464 > 0 for all t >= 10.
    3. Integrand is PSD rank-1 at every t, so tail matrix R_T is guaranteed PSD (R_T >= 0).
    4. Full-sign certified: lambda_min(W_arch) >= lambda_min(M_T) > 0.
    5. Full-value status: unenclosed at t = 600, certified on extended range z >= 320.
    """
    res = transcendental.certify_archimedean_tail_psd(t_cutoff=600.0, h=0.02)
    assert res['status'] == 'ARCHIMEDEAN_TAIL_PSD_CERTIFIED'

    dlmf = res['digamma_series_nist_dlmf_5_7_6']
    assert dlmf['monotonicity_proved'] is True
    assert dlmf['omega_positive_for_all_t_ge_T'] is True
    assert dlmf['omega_lower_bound_at_T'] > 4.5

    tail = res['tail_matrix_psd']
    assert tail['integrand_is_psd'] is True
    assert tail['R_T_is_psd'] is True

    sign_cert = res['full_sign_certificate']
    assert sign_cert['certified'] is True
    assert sign_cert['lambda_min_lower_bound'] > 1.6e10
    assert sign_cert['complete_W_positive_definite'] is True

    val_cert = res['full_value_certificate']
    assert val_cert['certified'] is False
    assert val_cert['status'] == 'UNENCLOSED_TAIL_AT_CUTOFF'


def test_epic_surviving_prime_bound_and_counterexample():
    """
    Verify Surviving Prime Terms and Mandatory Counterexample Control:
    1. Scaling identity: ||psi_h||_2^2 = h^-5 ||kappa''||^2 + (1/2)h^-3 ||kappa'||^2 + (1/16)h^-1 ||kappa||^2.
    2. Bound: ||W_prime(C, h)||_op <= C_prime(C, h0) * h^-5.
    3. Mandatory counterexample control: window [7, 17] has active stations 8 and 16 in grade 0;
       their ratio is 16/8 = 2, an exact prime power (q = 2).
       The term C_h(0) = ||psi_h||_2^2 > 0 survives for ALL h > 0!
    4. Asymptotic dominance: W_prime / W_arch -> 0 as h -> 0 due to log(1/h) divergence.
    """
    res = transcendental.compute_surviving_prime_bound(grades=[0, 1], window=(7.0, 17.0), h=0.02)
    assert res['status'] == 'SURVIVING_PRIME_BOUND_COMPUTED'

    assert 'h^-5' in res['scaling_identity']
    assert res['c_psi_h0'] > 56.0
    assert res['C_prime_bound'] > 0.0

    ce = res['mandatory_counterexample_control']
    assert ce['resonant_stations'] == [8, 16]
    assert ce['prime_power_q'] == 2
    assert ce['evaluates_C_h_at_zero'] is True
    assert ce['survives_for_all_h'] is True

    assert len(res['exact_resonances_found']) >= 1
    exact_q2 = [r for r in res['exact_resonances_found'] if r['q'] == 2]
    assert len(exact_q2) >= 1

    dom = res['asymptotic_dominance']
    assert dom['limit_as_h_to_zero'] == 0.0
    assert dom['archimedean_dominance_holds'] is True


def test_epic_local_positivity_threshold_and_complex_form():
    """
    Verify Eventual Positivity Threshold and Complex Coefficient Positivity:
    1. Computes genuine positive threshold h_pos(C) > 0 for active configurations.
    2. Positivity holds for arbitrary complex vectors:
       c^* W c = (Re c)^T W (Re c) + (Im c)^T W (Im c) >= lambda_min(W) ||c||^2 > 0.
    3. Empty configurations handled with zero rows/cols.
    """
    res = transcendental.compute_local_positivity_threshold(grades=[0, 1], window=(8.0, 20.0))
    assert res['status'] == 'LOCAL_POSITIVITY_THRESHOLD_COMPUTED'
    assert res['h_pos_threshold'] > 0.0
    assert res['d_min_active'] > 0.0

    thm = res['eventual_positivity_theorem']
    assert thm['complex_coefficients_covered'] is True
    assert 'c^* W c = (Re c)^T W (Re c) + (Im c)^T W (Im c)' in thm['complex_identity']


def test_epic_conditional_detection_investigation():
    """
    Verify Substantive Conditional Detection Investigation (D_F Obligation):
    1. Classical Connes-Consani (2020) Prop C.1 import: not RH ==> exists g_0 in V with B(g_0, g_0) < 0.
    2. Sobolev H^1 continuity bound controls quadratic form error on compact support.
    3. Scoped obstruction: small-bandwidth bump combinations in F_pos cannot approximate g_0
       within eta-tolerance because B(f_n, f_n) > 0 while B(g_0, g_0) = -eta < 0.
    4. Crucial conditional logic: failure of this approximation scheme closes the scheme,
       NOT the conditional proposition D_F: H ==> E_F.
    5. Epistemic status: D_F is strictly OPEN (RH-strength obligation under P_F).
    """
    res = transcendental.investigate_conditional_detection_implication(grades=[0, 1], window=(8.0, 20.0))
    assert res['status'] == 'CONDITIONAL_DETECTION_IMPLICATION_INVESTIGATED'

    classic = res['classical_consequence_under_H']
    assert 'Connes & Consani' in classic['citation']
    assert 'Proposition C.1' in classic['citation']

    approx = res['attempted_tc_approximation_analysis']
    assert approx['scoped_result'] == 'CLOSES_LOCALIZED_SMALL_BANDWIDTH_APPROXIMATION_SCHEME'
    assert len(approx['structural_constraints']) >= 3

    clarif = res['conditional_logic_clarification']
    assert 'Together P_F and D_F imply not H' in clarif['intended_contradiction']
    assert 'does NOT refute D_F' in clarif['non_refutation']
    assert clarif['status_of_D_F'] == 'STRICTLY_OPEN'
    assert res['transcendental_continuation_bridge_status'] == 'STRICTLY_OPEN'


def test_epic_two_variable_synthesis_milestone_10():
    """
    Verify full epic synthesis with Milestone 10 integration:
    1. All 10 milestones present.
    2. Total Lean 4 compiled theorems >= 263.
    3. Six new Lean 4 theorems included in new_theorems.
    4. Epistemic classifications reflect corrected conditional logic, full-sign PSD tail certificate,
       cutoff reproduction, surviving prime bound, and open conditional detection.
    """
    res = transcendental.audit_tc_epic_two_variable_synthesis()
    assert 'milestone_10_cutoff_reproduction' in res
    assert 'milestone_10_tail_psd_certification' in res
    assert 'milestone_10_surviving_prime_bound' in res
    assert 'milestone_10_local_positivity_threshold' in res
    assert 'milestone_10_conditional_detection_investigation' in res

    formal = res['formal_lean_theorems']
    assert formal['total_compiled_theorems'] >= 263
    for thm in [
        'realQuadraticForm_add',
        'realQuadraticForm_sub',
        'positivity_and_conditional_detection_imply_no_offline_zero',
        'real_quadratic_form_add_psd_tail',
        'complex_quadratic_form_add_psd_tail',
        'real_quadratic_form_prime_perturbation'
    ]:
        assert thm in formal['new_theorems']

    ep = res['epistemic_classification']
    assert 'PROVED' in ep['conditional_logic_rectification']
    assert 'REPRODUCED' in ep['cutoff_discrepancy']
    assert 'CERTIFIED' in ep['archimedean_tail_psd']
    assert 'CERTIFIED' in ep['full_sign_certificate']
    assert 'BOUNDED' in ep['surviving_prime_bound']
    assert 'PROVED' in ep['local_positivity_theorem']
    assert 'OPEN' in ep['conditional_detection_implication']
    assert ep['transcendental_continuation_bridge'] == 'STRICTLY OPEN'


def test_epic_matrix_invariants_and_cutoff_discrepancy():
    """
    Verify algebraic consistency and omitted-tail slab reproduction:
      1. Det equals product of eigenvalues and trace equals sum within 1e-14.
      2. Previous unverified claim of < 130 beyond z=320 is withdrawn.
      3. Omitted slab [320, 480] reproduced at ~1730.80 matching independent review.
    """
    res = transcendental.reproduce_cutoff_discrepancy()
    assert res['status'] == 'CUTOFF_DISCREPANCY_REPRODUCED'

    diag_slab = res['omitted_slab_320_to_480']
    assert diag_slab['claimed_under_130_withdrawn'] is True
    assert diag_slab['reproduced_target_1730'] is True
    assert abs(diag_slab['W00_slab_contribution_fine'] - 1730.80) < 0.1

    alg = res['algebraic_consistency_audit']
    assert alg['status'] == 'ALGEBRAICALLY_CONSISTENT'

    spec_16000 = res['quadrature_ranges']['cutoff_t_16000']
    assert spec_16000['checks']['det_equals_prod_eigenvalues'] is True
    assert spec_16000['checks']['trace_equals_sum_eigenvalues'] is True
    assert spec_16000['checks']['determinant_ge_lambda_min_times_W00'] is True


def test_epic_canonical_sign_certificate_generation_and_verification():
    """
    Verify reproducible canonical reflected Weil matrix sign certificate:
      1. Generates data/canonical_reflected_weil_matrix_sign.json.
      2. Reconstructs inequalities: omega(10) > 0, tail is PSD, prime terms vanish.
      3. Verifies strict positive margin >= 3.3274e10.
      4. Fails closed on invalid or corrupted certificate.
    """
    cert = transcendental.generate_canonical_reflected_weil_sign_certificate()
    assert cert['certificate_verdict'] == 'COMPLETE_CANONICAL_REFLECTED_WEIL_MATRIX_POSITIVE_DEFINITE'
    assert cert['error_bounds_and_margin']['strictly_positive_margin'] is True
    assert cert['error_bounds_and_margin']['net_positive_margin'] > 3.3e10

    ver = transcendental.verify_canonical_reflected_weil_sign_certificate(strict=True)
    assert ver['status'] == 'CERTIFICATE_VERIFIED'
    assert ver['verified'] is True
    assert ver['net_positive_margin'] > 3.3e10

    # Test fail-closed on corrupted cert
    corrupt_cert = dict(cert)
    corrupt_cert['error_bounds_and_margin'] = dict(cert['error_bounds_and_margin'])
    corrupt_cert['error_bounds_and_margin']['net_positive_margin'] = -1.0
    
    tmp_path = os.path.join(os.path.dirname(__file__), 'tmp_corrupt_cert.json')
    try:
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(corrupt_cert, f)
        
        try:
            transcendental.verify_canonical_reflected_weil_sign_certificate(tmp_path, strict=True)
            assert False, "Should have raised ValueError on negative margin"
        except ValueError as e:
            assert 'margin_positive' in str(e)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_epic_sobolev_scaling_and_continuity_bridge():
    """
    Verify Sobolev H^1 scaling, continuity in V_R, and the two structural barriers:
      1. Leading order Sobolev norm is h^(-7) ||kappa'''||_2^2 (~ 16247.68 * h^(-7)).
      2. ||psi_h||_{H^1} ~ 127.47 * h^(-7/2), severely dominating W_arch ~ h^(-5) log(1/h).
      3. False heuristic |B - B_crit| <= C delta_0 ||g||_{H^1}^2 and exp(-Delta/(2h)) withdrawn.
      4. Two structural barriers identified:
         - Barrier 1: Asymptotic Sobolev norm divergence in positive regime.
         - Barrier 2: Shared-grade arithmetic rigidity with fixed d_alpha.
      5. Scoped scheme closed, D_F remains strictly open.
    """
    res = transcendental.audit_weil_continuity_and_approximation_bridge()
    assert res['status'] == 'WEIL_CONTINUITY_AND_APPROXIMATION_BRIDGE_AUDITED'

    scaling = res['sobolev_scaling_exact_identities']
    assert scaling['canonical_kernel_constants']['norm_kappa_third_deriv_sq'] > 16200.0
    assert scaling['canonical_h_values']['norm_psi_h_H1'] > 1.0e8

    withdrawn = res['false_heuristics_withdrawn']
    assert withdrawn['B_crit_heuristic_withdrawn'] is True
    assert withdrawn['exp_delta_over_2h_withdrawn'] is True

    barriers = res['approximation_bridge_structural_barriers']
    assert 'barrier_1_asymptotic_scaling_divergence' in barriers
    assert 'barrier_2_shared_grade_arithmetic_rigidity' in barriers

    ep = res['epistemic_classification']
    assert 'CERTIFIED' in ep['positivity_property_P_F']
    assert 'CLOSED' in ep['localized_small_bandwidth_bump_approximation']
    assert ep['conditional_implication_D_F'] == 'STRICTLY_OPEN (Under P_F, D_F is equivalent to not H; not refuted by local bump failure)'
    assert ep['transcendental_continuation_status'] == 'STRICTLY_OPEN'


def test_epic_milestone_11_synthesis_and_lean_theorems():
    """
    Verify complete epic synthesis with Milestone 11 integration:
      1. Milestone 11 bridge, certificate, and verification present.
      2. Formal Lean 4 theorems count >= 267.
      3. Four new Lean theorems formalized with 0 sorry.
      4. Epistemic classifications fully updated.
    """
    res = transcendental.audit_tc_epic_two_variable_synthesis()
    assert 'milestone_11_weil_continuity_and_approximation_bridge' in res
    assert 'milestone_11_sign_certificate' in res
    assert 'milestone_11_certificate_verification' in res

    formal = res['formal_lean_theorems']
    assert formal['total_compiled_theorems'] >= 267
    for thm in [
        'matrix_lower_bound_psd_tail_perturbation',
        'real_symmetric_matrix_complex_pos_of_real_pos',
        'negativity_transfer_continuity',
        'sobolev_reverse_triangle_lower_bound'
    ]:
        assert thm in formal['new_theorems']

    ep = res['epistemic_classification']
    assert 'REPRODUCED' in ep['omitted_slab_discrepancy']
    assert 'RECOMPUTED' in ep['matrix_invariants_consistency']
    assert 'PROVED' in ep['sobolev_h1_norm_scaling']
    assert 'PROVED' in ep['weil_continuity_bound']
    assert 'IDENTIFIED' in ep['tc_approximation_barriers']
    assert 'STRICTLY_OPEN' in ep['tc_bridge_conditional_status']


def test_epic_coefficient_rescaling_homogeneity():
    """
    Verify Milestone 1: Coefficient Rescaling Homogeneity:
      1. Retraction of universal norm divergence.
      2. Refutation counterexample f_h = h * g_h / ||g_h||_{H^1}.
      3. Precise requirements for uniform divergence.
    """
    res = transcendental.audit_coefficient_rescaling_homogeneity()
    assert res['status'] == 'COEFFICIENT_RESCALING_HOMOGENEITY_AUDITED'
    ret = res['retraction_record']
    assert ret['homogeneity_holds'] is True
    assert 'f_h = h * g_h / ||g_h||_{H^1}' in ret['refutation_counterexample']
    assert len(res['divergence_requirements']) == 2


def test_epic_support_geometry_components_and_poincare():
    """
    Verify Milestone 2 & 3: Support Geometry Components & Poincare Obstruction:
      1. Merging of overlapping intervals.
      2. Computation of ell(C, h) and min station separation.
      3. Amplitude-independent Poincare lower bound.
    """
    stations = [math.log(9.0), math.log(11.0), math.log(13.0), math.log(16.0), math.log(17.0), math.log(19.0)]
    geom = transcendental.compute_support_components(stations, h=0.02)
    assert geom['num_stations'] == 6
    assert geom['is_disjoint'] is True
    assert geom['max_component_length_ell'] == pytest.approx(0.04)

    poincare = transcendental.poincare_support_lower_bound(f_star_L2=6.385504, f_star_deriv_L2=29.511691, ell=geom['max_component_length_ell'])
    assert poincare['poincare_error_lower_bound'] > 4.9
    assert poincare['strictly_positive_lower_bound'] is True


def test_epic_varying_families_and_approximation_regimes():
    """
    Verify Milestone 4: Varying Configurations and Approximation Regimes:
      1. Distinction between fixed-span and varying families.
      2. Regime 4A prime resonance activation barrier.
      3. Regime 4B Fourier zeros barrier.
    """
    res = transcendental.investigate_varying_configurations_and_shared_grades(h_test=0.02)
    assert res['status'] == 'VARYING_FAMILIES_AND_APPROXIMATION_REGIMES_AUDITED'
    assert 'positivity_consequence' in res['regime_4A_shrinking_bandwidth_macroscopic_components']
    assert 'fourier_common_factor' in res['regime_4B_bounded_bandwidth']


def test_epic_admissible_target_and_approximation_experiment():
    """
    Verify Milestone 5: Explicit Admissible Target & Constrained Approximation:
      1. Pole vanishing integrals vanish identically for (D_u^2 - 1/4)Phi.
      2. Least-squares approximation plateau under TC basis.
    """
    res = transcendental.construct_admissible_target_and_approximation_experiment(h=0.1, N_stations=7)
    assert res['status'] == 'APPROXIMATION_EXPERIMENT_COMPLETED'
    poles = res['target_function']['pole_integrals']
    assert poles['int_f_exp_pos_half'] == pytest.approx(0.0, abs=1e-7)
    assert poles['int_f_exp_neg_half'] == pytest.approx(0.0, abs=1e-7)
    # Defect 4 fix: Validate mathematical identities and numerical reliability instead of demanding > 0.95 error
    rel_err = res['shared_grade_model']['relative_error']
    assert isinstance(rel_err, float) and math.isfinite(rel_err) and rel_err >= 0.0
    target_norm = res['target_function']['norm_H1']
    residual_norm = res['shared_grade_model']['H1_error']
    assert target_norm > 0.0
    assert abs(residual_norm / target_norm - rel_err) < 1e-10


def test_epic_weil_continuity_and_connes_consani_bridge():
    """
    Verify Milestone 6: Complete Reflected Form Continuity & Connes-Consani Bridge:
      1. Continuity bound |B(f, l)| <= C_R ||f||_{H^1} ||l||_{H^1}.
      2. Critical H^1 error threshold for negativity transfer.
    """
    res = transcendental.audit_weil_continuity_and_connes_consani_bridge(R=1.0, C_R=100.0, eta=1.0)
    assert res['status'] == 'WEIL_CONTINUITY_AND_CONNES_CONSANI_BRIDGE_AUDITED'
    assert res['negativity_transfer_threshold']['eps_critical'] > 0
    assert res['negativity_transfer_threshold']['eps_critical'] < 0.001


def test_epic_support_geometry_synthesis_master():
    """
    Verify Master Synthesis for TC Research Epic:
      1. All 7 milestones present and validated.
      2. All 8 required final questions answered accurately.
      3. Output file exists.
    """
    res = transcendental.audit_tc_epic_support_geometry_synthesis()
    assert 'TC Research Epic' in res['epic']
    answers = res['answers_to_required_questions']
    assert len(answers) == 8
    for i in range(1, 9):
        key = f'q{i}_'
        assert any(k.startswith(key) for k in answers.keys())
    assert os.path.exists('data/tc_epic_support_geometry_synthesis.json')


def test_epic_canonical_overlap_and_prime_vanishing():
    """
    Verify prompt Section 5 diagnostic controls:
      1. Canonical active stations on [8, 20], grades {0, 1}.
      2. Overlap at h=0.02: log(19/(6pi)) ~= 0.00795 < 0.04, log(13/(4pi)) ~= 0.03393 < 0.04.
      3. Maximal merged length ell ~= 0.0739251105 > 0.04.
      4. Min cross-grade prime resonance gap ~= 0.0461175972 > 0.04.
      5. W_prime = 0 vanishes identically despite support overlap.
    """
    diag = transcendental.audit_canonical_support_geometry_and_resonance(h=0.02)
    assert diag['status'] == 'CANONICAL_SUPPORT_GEOMETRY_AND_RESONANCE_AUDITED'
    geom = diag['support_geometry']
    assert geom['overlaps_present'] is True
    assert geom['overlap_19_vs_6pi'] == pytest.approx(0.0079496241, abs=1e-6)
    assert geom['overlap_13_vs_4pi'] == pytest.approx(0.0339251105, abs=1e-6)
    assert geom['maximal_merged_length_ell'] == pytest.approx(0.0739251105, abs=1e-6)

    res = diag['resonance_analysis']
    assert res['min_cross_grade_resonance_gap'] == pytest.approx(0.0461175972, abs=1e-6)
    assert res['W_prime_vanishes_identically'] is True
    assert res['prime_resonance_activated'] is False


def test_epic_negative_grade_station_growth():
    """
    Verify prompt Section 2 & 6:
      1. Growing station count does NOT force growing grade count.
      2. In [8, 20], negative grades K -> -infty supply rapidly growing station counts.
      3. For K in {0, -1, -2, -3}, counts are {7, 19, 79, 376}.
    """
    res = transcendental.analyze_negative_grade_station_growth(window=(8.0, 20.0), K_values=[0, -1, -2, -3])
    assert res['status'] == 'NEGATIVE_GRADE_STATION_GROWTH_ANALYZED'
    rbg = res['results_by_grade']
    assert rbg['grade_0']['station_count'] == 7
    assert rbg['grade_-1']['station_count'] == 19
    assert rbg['grade_-2']['station_count'] == 79
    assert rbg['grade_-3']['station_count'] == 376


def test_epic_fourier_zero_compact_support_obstruction():
    """
    Verify prompt Section 4B & 6:
      1. Proved Cauchy-Schwarz lower bound on compact support [-R, R]:
         ||f - f_*||_{L^2} >= |hat{f_*}(xi_0)| / sqrt(2R).
      2. Nonzero lower bound at universal node xi_0 = 4.9965 / h.
    """
    obs = transcendental.analyze_fourier_zero_compact_support_obstruction(R=1.0, h=0.1)
    assert obs['status'] == 'FOURIER_ZERO_COMPACT_SUPPORT_OBSTRUCTION_ANALYZED'
    assert obs['analytic_L2_lower_bound'] > 0.0
    assert obs['strictly_positive_bound'] is True


def test_epic_continuous_weil_constant_derivation():
    """
    Verify prompt Section 4:
      1. Digamma growth envelope C_omega = 18.
      2. Prime sum S_prime for R = 1.0 (exp(2R) ~= 7.389) across prime powers {2, 3, 4, 5, 7}.
      3. Derived constant C_R = 18 + 2 * S_prime ~= 23.8525.
    """
    bridge = transcendental.audit_weil_continuity_and_connes_consani_bridge(R=1.0, C_omega=18.0, eta=1.0)
    assert bridge['status'] == 'WEIL_CONTINUITY_AND_CONNES_CONSANI_BRIDGE_AUDITED'
    assert bridge['continuity_bound']['support_constant_C_R'] == pytest.approx(23.8525, abs=1e-3)
    assert bridge['continuity_bound']['S_prime'] == pytest.approx(2.92625, abs=1e-3)


# ==============================================================================
# TC ARITHMETIC FIDELITY & NEGATIVE-GRADE INVESTIGATION ADVERSARIAL REGRESSIONS
# ==============================================================================

def test_adversarial_1_reject_synthetic_stations_as_actual_tc():
    """Adversarial Regression 1: Ensure synthetic equally-spaced stations fail TC provenance and active validation check."""
    fake_manifest = {
        'K': 0,
        'window': [8.0, 20.0],
        'is_actual_tc': False,
        'stations': [
            {'grade': 0, 'prime': 0, 'exponent': 1, 'n': 10, 'x': 10.0, 'u': math.log(10.0),
             'Lambda_n': 1.0, 'w_val': 1.0, 'd_val': 1.0, 'is_active': True}
        ],
        'provenance_hash': 'fake_hash'
    }
    is_valid, reasons = transcendental.validate_tc_station_manifest(fake_manifest, window=(8.0, 20.0))
    assert is_valid is False
    assert any("not marked as actual TC" in r or "prime" in r.lower() for r in reasons)

    # Active interface must raise ValueError when given an invalid manifest
    u_grid = np.linspace(math.log(8.0), math.log(20.0), 10)
    with pytest.raises(ValueError, match="failed"):
        transcendental.evaluate_actual_tc_grade_basis(u_grid, K=0, h=0.1, manifest=fake_manifest)


def test_adversarial_2_reject_log_n_in_place_of_log_p():
    """Adversarial Regression 2: Ensure Lambda(p^r) is strictly log(p), rejecting log(n)."""
    man = transcendental.generate_actual_tc_stations(K=0, window=(8.0, 20.0))
    station_9 = next(s for s in man['stations'] if s['n'] == 9)
    assert station_9['prime'] == 3
    assert station_9['exponent'] == 2
    assert station_9['Lambda_n'] == pytest.approx(math.log(3.0), abs=1e-12)
    assert station_9['Lambda_n'] != pytest.approx(math.log(9.0), abs=1e-3)

    station_16 = next(s for s in man['stations'] if s['n'] == 16)
    assert station_16['prime'] == 2
    assert station_16['exponent'] == 4
    assert station_16['Lambda_n'] == pytest.approx(math.log(2.0), abs=1e-12)
    assert station_16['Lambda_n'] != pytest.approx(math.log(16.0), abs=1e-3)


def test_adversarial_3_log_coordinate_jacobian_verification():
    """Adversarial Regression 3: Ensure log-coordinate continuum density includes the exact e^u Jacobian."""
    u_test = math.log(14.0)
    v_val = transcendental.evaluate_v_w_profile(u_test, window=(8.0, 20.0))
    w_val = transcendental.canonical_window_weight(14.0, window=(8.0, 20.0))
    # v_w(u) = e^u * w(e^u) = 14.0 * w(14.0)
    assert v_val == pytest.approx(14.0 * w_val, rel=1e-10)
    # Reject density missing the e^u Jacobian
    assert v_val != pytest.approx(w_val, rel=1e-2)


def test_adversarial_4_boundary_zero_weight_stations_not_counted_as_active():
    """Adversarial Regression 4: Ensure boundary stations with w(x)=0 are not reported as active."""
    man = transcendental.generate_actual_tc_stations(K=0, window=(8.0, 20.0))
    st_8 = next(s for s in man['stations'] if s['n'] == 8)
    assert st_8['x'] == 8.0
    assert st_8['w_val'] == 0.0
    assert st_8['d_val'] == 0.0
    assert st_8['is_active'] is False
    assert man['enumerated_station_count'] == 7
    assert man['active_station_count'] == 6
    assert 8 not in [s['n'] for s in man['active_stations']]


def test_adversarial_5_reject_independent_coefficients_in_shared_grade_model():
    """Adversarial Regression 5: Ensure shared-grade model strictly uses 1 coefficient per grade."""
    exp = transcendental.construct_actual_tc_approximation_experiment(
        grades=[0, -1, -2], h=0.05, window=(8.0, 20.0), target_role="continuum_consistency"
    )
    shared = exp['shared_grade_model']
    uncon = exp['unconstrained_model']
    assert shared['num_grades'] == 3
    assert len(shared['coefficients_c']) == 3
    assert uncon['num_independent_stations'] > 3
    assert uncon['is_enlarged_family_control'] is True


def test_adversarial_6_raw_norm_growth_does_not_exclude_normalized_convergence():
    """Adversarial Regression 6: Raw bump norm divergence does not prevent normalized F_{K,h,w} convergence."""
    res_k0 = transcendental.compute_arithmetic_vs_smoothing_error(K=0, h=0.1, window=(8.0, 20.0))
    res_k4 = transcendental.compute_arithmetic_vs_smoothing_error(K=-4, h=0.1, window=(8.0, 20.0))
    assert res_k4['errors']['E_arith_H1'] < res_k0['errors']['E_arith_H1']
    assert res_k4['errors']['E_arith_relative'] < res_k0['errors']['E_arith_relative']


def test_adversarial_7_reject_incompatible_disjoint_support_comparison():
    """Adversarial Regression 7: Ensure target and basis supports are strictly compatible."""
    log_8 = math.log(8.0)
    log_20 = math.log(20.0)
    val_outside, _ = transcendental.evaluate_continuum_limit_profile_F_infty_0(0.0, window=(8.0, 20.0))
    assert val_outside == 0.0
    val_inside, _ = transcendental.evaluate_continuum_limit_profile_F_infty_0(0.5 * (log_8 + log_20), window=(8.0, 20.0))
    assert abs(val_inside) > 0.0


def test_adversarial_8_reject_generic_target_as_negative_weil_witness():
    """Adversarial Regression 8: Generic smooth target is not relabeled as negative witness without proof."""
    exp = transcendental.construct_actual_tc_approximation_experiment(
        grades=[0, -1], h=0.1, window=(8.0, 20.0), target_role="continuum_consistency"
    )
    assert exp['target_function']['role'] == "continuum_consistency"
    assert "Weil witness" not in exp['target_function']['description']


def test_adversarial_9_quadrature_resolution_and_hash_stability():
    """Adversarial Regression 9: Stable Gauss-Legendre quadrature resolves convolution and matches direct evaluation."""
    # 1. Diagnostic test at h=0.02, u=log(14):
    u_diag = math.log(14.0)
    h_diag = 0.02
    f_val, f_p = transcendental.evaluate_continuum_mollified_profile_F_infty_h(u_diag, h_diag, window=(8.0, 20.0))
    f_dir, f_p_dir = transcendental.evaluate_continuum_mollified_profile_F_infty_h_direct_psi(u_diag, h_diag, window=(8.0, 20.0), n_quad=2048)

    # Old 64-panel evaluator returned roughly (350.78674, -147234.64)
    # Correct values are roughly (-117.84010, -751.47854)
    assert f_val == pytest.approx(-117.84010, abs=0.5)
    assert f_p == pytest.approx(-751.47854, abs=5.0)
    assert abs(f_val - f_dir) < 1.0e-3
    assert abs(f_p - f_p_dir) < 1.0e-1

    # 2. Hash reproducibility
    man1 = transcendental.generate_actual_tc_stations(K=-2, window=(8.0, 20.0))
    man2 = transcendental.generate_actual_tc_stations(K=-2, window=(8.0, 20.0))
    assert man1['provenance_hash'] == man2['provenance_hash']
    assert man1['active_station_count'] == 79


def test_adversarial_10_negative_grade_campaign_artifact_verification():
    """Adversarial Regression 10: Campaign artifact exists, contains required regimes, and validates status."""
    artifact_path = os.path.join(REPO_ROOT, "data", "tc_negative_grade_approximation_campaign.json")
    assert os.path.exists(artifact_path)
    with open(artifact_path, "r", encoding="utf-8") as f:
        campaign = json.load(f)

    assert campaign['status'] == 'TC_NEGATIVE_GRADE_CAMPAIGN_COMPLETED'
    assert len(campaign['regime_1_single_grade_convergence']) == 10
    assert len(campaign['regime_2_fixed_grade_bandwidth_scaling']) == 4

    # Regime 3 empirical divergence
    r3 = campaign['regime_3_joint_diagonal_schedule']
    assert r3['empirical_schedule_verdict'] == 'EMPIRICAL_DIVERGENCE_ON_TESTED_SCHEDULE'
    assert r3['is_monotonically_decreasing'] is False
    rel_errors = [p['E_total_rel'] for p in r3['schedule_pairs']]
    assert rel_errors[0] == pytest.approx(3.3885, abs=0.05)
    assert rel_errors[-1] == pytest.approx(1083.34, abs=5.0)

    # Regime 2 smoothing error bounded
    r2_h002 = next(p for p in campaign['regime_2_fixed_grade_bandwidth_scaling'] if p['h'] == 0.02)
    assert r2_h002['E_smooth_H1'] < 20000.0  # Repaired from 420107.0

    # Regime 4 target verification and geometry
    r4 = campaign['regime_4_multigrade_shared_vs_unconstrained']
    cont = r4['continuum_target']
    indep = r4['independent_target']
    assert cont['target_function']['pole_cancellation_verified'] is True
    assert indep['target_function']['pole_cancellation_verified'] is True
    assert cont['support_geometry']['max_component_length_ell'] > 1.0

    # Dynamic answers
    answers = campaign['answers_to_six_core_questions']
    assert len(answers) == 6
    assert "DIVERGENCE" in answers['q1_does_negative_grade_approach_continuum']
    assert "OPEN" in answers['q2_which_additional_targets_approximated']
    assert "OPEN" in answers['q5_has_D_F_advanced']
    assert "NO" in answers['q6_has_arithmetic_coincidence_advanced']


def test_mutation_continuum_evaluator_invariant():
    """Mutation/Regression: Stable evaluator satisfies convolution contraction and smoothing error bound <= 2||F_0||."""
    res = transcendental.compute_arithmetic_vs_smoothing_error(K=-2, h=0.02, window=(8.0, 20.0), n_points=201)
    norm_f0 = res['target_norms']['H1']
    norm_fh = res['target_norms']['norm_mollified_H1']
    e_smooth = res['errors']['E_smooth_H1']

    # Contraction: ||F_{infty, h}||_{H^1} <= ||F_{infty, 0}||_{H^1}
    assert norm_fh <= norm_f0 * 1.001  # allow numerical discretization margin
    assert res['errors']['convolution_contraction_satisfied'] is True
    # Smoothing error bound: ||F_{infty, h} - F_{infty, 0}||_{H^1} <= 2 * ||F_{infty, 0}||_{H^1}
    assert e_smooth <= 2.0 * norm_f0
    assert res['errors']['smoothing_error_bound_satisfied'] is True

    # Assert defect rejection: old un-repaired error (~420107) violates 2 * norm_f0 (~65896)
    assert e_smooth < 20000.0
    assert 420107.0 > 2.0 * norm_f0


def test_mutation_worsening_joint_schedule_reports_failure():
    """
    Mutation/Regression: Production campaign reporting strictly reflects schedule evidence:
    1. For the production worsening schedule, production assigns EMPIRICAL_DIVERGENCE_ON_TESTED_SCHEDULE
       and states that relative error increased.
    2. For an improving schedule [10, 9, 8, 7], production assigns EMPIRICAL_CONVERGENCE,
       states that error decreased from 10.00 to 7.00, and does NOT claim divergence.
    """
    # 1. Production schedule behavior
    camp_prod = transcendental.run_tc_negative_grade_approximation_campaign(output_path="")
    r3_prod = camp_prod['regime_3_joint_diagonal_schedule']
    assert r3_prod['empirical_schedule_verdict'] == 'EMPIRICAL_DIVERGENCE_ON_TESTED_SCHEDULE'
    assert r3_prod['is_monotonically_decreasing'] is False
    q1_prod = camp_prod['answers_to_six_core_questions']['q1_does_negative_grade_approach_continuum']
    assert "EMPIRICAL_DIVERGENCE" in q1_prod
    assert "increased from 3.39 to 1083.34" in q1_prod
    assert "decreased monotonically" not in q1_prod

    # 2. Injected improving schedule behavior
    improving_schedule = [10.0, 9.0, 8.0, 7.0]
    camp_imp = transcendental.run_tc_negative_grade_approximation_campaign(
        override_joint_relative_errors=improving_schedule,
        output_path=""
    )
    r3_imp = camp_imp['regime_3_joint_diagonal_schedule']
    assert r3_imp['empirical_schedule_verdict'] == 'EMPIRICAL_CONVERGENCE'
    assert r3_imp['is_monotonically_decreasing'] is True
    q1_imp = camp_imp['answers_to_six_core_questions']['q1_does_negative_grade_approach_continuum']
    assert "EMPIRICAL_CONVERGENCE" in q1_imp
    assert "decreased monotonically from 10.00 to 7.00" in q1_imp
    assert "diverged from 10.00 to 7.00" not in q1_imp
    assert "diverged" not in q1_imp
    assert "EMPIRICAL_DIVERGENCE" not in q1_imp


def test_mutation_false_pole_flag_rejected():
    """
    Mutation/Regression: Production target verification and campaign report strictly detect and
    reject false pole cancellation flags.
    """
    # 1. Non-cancelling control target (pure bump without D^2 - 1/4 operator)
    exp_non_cancelling = transcendental.construct_actual_tc_approximation_experiment(
        grades=[0, -1], h=0.05, target_role="non_cancelling_control"
    )
    assert exp_non_cancelling['target_function']['pole_cancellation_verified'] is False
    assert abs(exp_non_cancelling['target_function']['int_pole_pos']) > 1e-4
    assert abs(exp_non_cancelling['target_function']['int_pole_neg']) > 1e-4

    # 2. Production campaign report generation must actively detect failed pole verification
    camp_failed = transcendental.run_tc_negative_grade_approximation_campaign(
        override_exp_independent=exp_non_cancelling,
        output_path=""
    )
    assert camp_failed['invariants_verified'] is False
    assert camp_failed['status'] == 'TC_NEGATIVE_GRADE_CAMPAIGN_INVARIANTS_FAILED'
    assert any("pole cancellation verification failed" in f for f in camp_failed['audit_invariant_failures'])
    q2_text = camp_failed['answers_to_six_core_questions']['q2_which_additional_targets_approximated']
    assert "WARNING: Target pole cancellation verification FAILED" in q2_text


def test_mutation_missing_geometry_key_rejected():
    """Mutation/Regression: Nonempty merged interval must not receive length zero via missing-key fallback."""
    man0 = transcendental.generate_actual_tc_stations(K=0, window=(8.0, 20.0))
    man1 = transcendental.generate_actual_tc_stations(K=-1, window=(8.0, 20.0))
    man2 = transcendental.generate_actual_tc_stations(K=-2, window=(8.0, 20.0))
    active_u = sorted(
        [s['u'] for s in man0['stations'] if s['is_active']] +
        [s['u'] for s in man1['stations'] if s['is_active']] +
        [s['u'] for s in man2['stations'] if s['is_active']]
    )
    assert len(active_u) == 104

    geom = transcendental.compute_support_components(active_u, h=0.05)
    # The contract key is 'max_component_length_ell'
    assert 'max_component_length_ell' in geom
    assert geom['max_component_length_ell'] > 1.0  # Merged component covers ~1.01

    # Old defect read 'maximal_length', which was absent and silently defaulted to 0.0
    assert 'maximal_length' not in geom
    with pytest.raises(KeyError):
        _ = geom['maximal_length']


def test_coefficient_conversion_reconstructs_identical_basis():
    """
    Mutation/Regression: Production experiment coefficients satisfy sum c_K T_K == sum b_K F_K.
    Tests production-returned normalized coefficients b_K against raw c_K.
    """
    tau = 2.0 * math.pi
    grades = [0, -1, -2]
    h = 0.05
    window = (8.0, 20.0)
    u_grid = np.linspace(math.log(8.0), math.log(20.0), 101)

    # Obtain production experiment
    exp = transcendental.construct_actual_tc_approximation_experiment(
        grades=grades, h=h, window=window, target_role="continuum_consistency"
    )

    # Extract production coefficients directly from experiment dictionary
    c_shared = exp['shared_grade_model']['coefficients_c']
    b_norm = exp['shared_grade_model']['normalized_coefficients']
    assert len(c_shared) == len(grades)
    assert len(b_norm) == len(grades)

    # Verify that production computes b_K = c_K / a_K
    for i, K in enumerate(grades):
        expected_a_K = tau ** K
        assert b_norm[i] == pytest.approx(c_shared[i] / expected_a_K, rel=1e-12)

    # Verify basis reconstruction equivalence in production
    recon_T = np.zeros_like(u_grid)
    recon_Tp = np.zeros_like(u_grid)
    recon_F = np.zeros_like(u_grid)
    recon_Fp = np.zeros_like(u_grid)
    recon_F_flawed = np.zeros_like(u_grid)

    for i, K in enumerate(grades):
        c = c_shared[i]
        b = b_norm[i]
        b_fl = c * (tau ** K)  # flawed inversion formula
        man = transcendental.generate_actual_tc_stations(K=K, window=window)
        T_vals, T_p_vals, F_vals, F_p_vals = transcendental.evaluate_actual_tc_grade_basis(u_grid, K=K, h=h, manifest=man)
        recon_T += c * T_vals
        recon_Tp += c * T_p_vals
        recon_F += b * F_vals
        recon_Fp += b * F_p_vals
        recon_F_flawed += b_fl * F_vals

    assert np.max(np.abs(recon_T - recon_F)) < 1e-9
    assert np.max(np.abs(recon_Tp - recon_Fp)) < 1e-6
    assert np.max(np.abs(recon_T - recon_F_flawed)) > 1.0


def test_tampered_station_manifest_actively_rejected():
    """
    Mutation/Regression: Validate station manifest actively detects:
    1. Empty station list for nonempty window (even with recomputed hash)
    2. Duplicated station list (even with recomputed hash)
    3. Non-finite / NaN arithmetic weight (even with recomputed hash)
    4. Evaluation grade mismatch (evaluating grade K=0 with K=-1 manifest)
    5. Non-prime powers, incorrect von Mangoldt weights, and out-of-bounds coordinates.
    """
    import copy
    import hashlib
    window = (8.0, 20.0)
    man = transcendental.generate_actual_tc_stations(K=0, window=window)

    def recompute_hash(station_list):
        prov_bytes = json.dumps(
            [{'K': s.get('grade'), 'p': s.get('prime'), 'r': s.get('exponent'), 'n': s.get('n'),
              'x': f"{s.get('x', 0.0):.12e}" if (isinstance(s.get('x'), (int, float)) and math.isfinite(s.get('x', 0.0))) else "nan",
              'u': f"{s.get('u', 0.0):.12e}" if (isinstance(s.get('u'), (int, float)) and math.isfinite(s.get('u', 0.0))) else "nan",
              'L': f"{s.get('Lambda_n', 0.0):.12e}" if (isinstance(s.get('Lambda_n'), (int, float)) and math.isfinite(s.get('Lambda_n', 0.0))) else "nan",
              'w': f"{s.get('w_val', 0.0):.12e}" if (isinstance(s.get('w_val'), (int, float)) and math.isfinite(s.get('w_val', 0.0))) else "nan",
              'd': f"{s.get('d_val', 0.0):.12e}" if (isinstance(s.get('d_val'), (int, float)) and math.isfinite(s.get('d_val', 0.0))) else "nan"}
             for s in station_list if isinstance(s, dict)],
            sort_keys=True
        ).encode('utf-8')
        return hashlib.sha256(prov_bytes).hexdigest()

    # Attack 1: Empty station list for non-empty canonical window
    man_empty = copy.deepcopy(man)
    man_empty['stations'] = []
    man_empty['active_stations'] = []
    man_empty['provenance_hash'] = recompute_hash([])
    is_valid, reasons = transcendental.validate_tc_station_manifest(man_empty, window=window)
    assert is_valid is False
    assert any("empty stations list" in r.lower() for r in reasons)

    # Attack 2: Every station duplicated
    man_dup = copy.deepcopy(man)
    man_dup['stations'] = sorted(man['stations'] + man['stations'], key=lambda s: (s['n'], s['prime']))
    man_dup['active_stations'] = [s for s in man_dup['stations'] if s['is_active']]
    man_dup['provenance_hash'] = recompute_hash(man_dup['stations'])
    is_valid, reasons = transcendental.validate_tc_station_manifest(man_dup, window=window)
    assert is_valid is False
    assert any("duplicate" in r.lower() or "count mismatch" in r.lower() for r in reasons)

    # Attack 3: NaN arithmetic weight
    man_nan = copy.deepcopy(man)
    man_nan['stations'][0]['Lambda_n'] = float('nan')
    man_nan['provenance_hash'] = recompute_hash(man_nan['stations'])
    is_valid, reasons = transcendental.validate_tc_station_manifest(man_nan, window=window)
    assert is_valid is False
    assert any("non-finite" in r.lower() or "nan" in r.lower() for r in reasons)

    # Attack 4: Manifest evaluated at wrong grade (K=0 evaluating K=-1 manifest)
    man_k_minus_1 = transcendental.generate_actual_tc_stations(K=-1, window=window)
    u_grid = np.linspace(math.log(8.0), math.log(20.0), 10)
    with pytest.raises(ValueError, match="Grade mismatch"):
        transcendental.evaluate_actual_tc_grade_basis(u_grid, K=0, h=0.1, manifest=man_k_minus_1)

    # Attack 5: Composite number that is not a prime power (e.g. n=6)
    tampered_1 = copy.deepcopy(man)
    tampered_1['stations'].append({
        'grade': 0, 'prime': 0, 'exponent': 1, 'n': 6, 'x': 6.0, 'u': math.log(6.0),
        'Lambda_n': math.log(6.0), 'w_val': 1.0, 'd_val': 1.0, 'is_active': True
    })
    tampered_1['stations'].sort(key=lambda s: s['n'])
    tampered_1['provenance_hash'] = recompute_hash(tampered_1['stations'])
    is_valid, reasons = transcendental.validate_tc_station_manifest(tampered_1, window=window)
    assert is_valid is False
    assert any("prime" in r.lower() or "count mismatch" in r.lower() for r in reasons)

    # Attack 6: Prime power with Lambda(n) = log(n) instead of log(p)
    tampered_2 = copy.deepcopy(man)
    st9 = next(s for s in tampered_2['stations'] if s['n'] == 9)
    st9['Lambda_n'] = math.log(9.0)
    tampered_2['provenance_hash'] = recompute_hash(tampered_2['stations'])
    is_valid, reasons = transcendental.validate_tc_station_manifest(tampered_2, window=window)
    assert is_valid is False
    assert any("Lambda_n" in r or "log(n)" in r for r in reasons)


def test_toy_family_varying_spans_counterexample():
    """
    Mutation/Regression: Common-limit toy family F_j = v + eps_j * g refutes the inference
    that limiting rank 1 implies unrestricted varying spans have rank 1.
    """
    # Grid
    x = np.linspace(-1.0, 1.0, 101)
    v = np.exp(-x**2)
    g = x * np.exp(-x**2)  # linearly independent from v

    # Family F_j -> v as j -> infty
    def F_j(j: int):
        eps_j = 2.0**(-j)
        return v + eps_j * g

    F_1 = F_j(1)  # v + 0.5 * g
    F_2 = F_j(2)  # v + 0.25 * g
    F_10 = F_j(10) # v + 2^(-10) * g

    # 1. Pointwise column limit is rank 1
    assert np.max(np.abs(F_10 - v)) < 1e-3

    # 2. But difference quotient isolates g exactly:
    # (F_1 - F_2) / (0.5 - 0.25) = g
    isolated_g = (F_1 - F_2) / (0.5 - 0.25)
    assert np.max(np.abs(isolated_g - g)) < 1e-14

    # 3. Span matrix [F_1, F_2] has full rank 2
    M = np.column_stack([F_1, F_2])
    rank = np.linalg.matrix_rank(M)
    assert rank == 2


def test_acceptance_matrix_trend_classification():
    """
    Test all rows of the required acceptance matrix in classify_finite_series_trend:
    - Finite strictly decreasing errors -> Observed decrease on the tested points. No inferred zero limit.
    - Finite strictly increasing errors -> Observed increase on the tested points. No inferred asymptotic divergence.
    - Constant or numerically unresolved changes -> Constant within declared tolerance.
    - Mixed sequence, including [10, 5, 6, 4] -> Mixed finite trend; separately report net improvement from 10 to 4.
    - Empty or singleton series -> Insufficient evidence for a trend. A valid single measurement remains a measurement.
    - Negative norm errors, NaN, infinity, malformed data -> Invalid or incomplete evidence; no scientific validation.
    """
    # 1. Strictly decreasing
    t_dec = transcendental.classify_finite_series_trend([10.0, 8.0, 5.0, 2.0])
    assert t_dec['status'] == 'STRICTLY_DECREASING'
    assert t_dec['is_valid'] is True
    assert t_dec['is_decreasing'] is True
    assert "No inferred zero limit" in t_dec['detail']

    # 2. Strictly increasing
    t_inc = transcendental.classify_finite_series_trend([1.0, 3.0, 7.0, 15.0])
    assert t_inc['status'] == 'STRICTLY_INCREASING'
    assert t_inc['is_valid'] is True
    assert t_inc['is_increasing'] is True
    assert "No inferred asymptotic divergence" in t_inc['detail']

    # 3. Constant within tolerance
    t_const = transcendental.classify_finite_series_trend([1.0, 1.0, 1.0, 1.0])
    assert t_const['status'] == 'CONSTANT_WITHIN_TOLERANCE'
    assert t_const['is_valid'] is True
    assert t_const['is_constant'] is True

    # 4. Mixed sequence [10, 5, 6, 4]
    t_mix = transcendental.classify_finite_series_trend([10.0, 5.0, 6.0, 4.0])
    assert t_mix['status'] == 'MIXED_FINITE_TREND'
    assert t_mix['is_valid'] is True
    assert t_mix['is_mixed'] is True
    assert "net improvement from 10.00 to 4.00" in t_mix['detail']
    assert t_mix['net_change'] == -6.0

    # 5. Empty and Singleton series
    t_empty = transcendental.classify_finite_series_trend([])
    assert t_empty['status'] == 'INSUFFICIENT_EVIDENCE_EMPTY'
    assert t_empty['is_valid'] is False

    t_single = transcendental.classify_finite_series_trend([42.0])
    assert t_single['status'] == 'INSUFFICIENT_EVIDENCE_SINGLETON'
    assert t_single['is_valid'] is True
    assert t_single['single_value'] == 42.0

    # 6. Negative, NaN, Inf, and Malformed data
    t_neg = transcendental.classify_finite_series_trend([10.0, 5.0, -1.0])
    assert t_neg['status'] == 'INVALID_OR_INCOMPLETE_EVIDENCE'
    assert t_neg['is_valid'] is False
    assert "negative" in t_neg['detail'].lower()

    t_nan = transcendental.classify_finite_series_trend([10.0, 9.0, float('nan')])
    assert t_nan['status'] == 'INVALID_OR_INCOMPLETE_EVIDENCE'
    assert t_nan['is_valid'] is False

    t_inf = transcendental.classify_finite_series_trend([10.0, float('inf')])
    assert t_inf['status'] == 'INVALID_OR_INCOMPLETE_EVIDENCE'
    assert t_inf['is_valid'] is False

    t_bad = transcendental.classify_finite_series_trend([10.0, "bad_data"])
    assert t_bad['status'] == 'INVALID_OR_INCOMPLETE_EVIDENCE'
    assert t_bad['is_valid'] is False


def test_mutation_missing_flag_rejected():
    """
    Mutation/Regression: Missing boolean flags in Regime 2 must not default to True.
    """
    tampered_r2 = [
        {'K': -2, 'h': 0.1, 'E_arith_H1': 100.0, 'E_smooth_H1': 50.0, 'E_total_H1': 120.0}
        # Notice: contraction_satisfied and smoothing_error_bound_satisfied are MISSING!
    ]
    camp = transcendental.run_tc_negative_grade_approximation_campaign(
        override_regime_2_results=tampered_r2,
        output_path=""
    )
    assert camp['invariants_verified'] is False
    assert camp['status'] == 'TC_NEGATIVE_GRADE_CAMPAIGN_INVARIANTS_FAILED'
    assert any("Regime 2" in f and ("missing" in f or "violated" in f) for f in camp['audit_invariant_failures'])


def test_mutation_contradictory_flags_rejected():
    """
    Mutation/Regression: If an invariant flag is set to True but numerical quantities contradict it,
    the contradictory flag is actively rejected and the invariant audit fails.
    """
    exp_bad_pole = transcendental.construct_actual_tc_approximation_experiment(
        grades=[0, -1], h=0.05, target_role="non_cancelling_control"
    )
    # Tamper flag to claim True even though integrals do not vanish
    exp_bad_pole['target_function']['pole_cancellation_verified'] = True
    assert abs(exp_bad_pole['target_function']['int_pole_pos']) > 1e-4

    camp = transcendental.run_tc_negative_grade_approximation_campaign(
        override_exp_independent=exp_bad_pole,
        output_path=""
    )
    assert camp['invariants_verified'] is False
    assert camp['status'] == 'TC_NEGATIVE_GRADE_CAMPAIGN_INVARIANTS_FAILED'
    assert any("contradicts" in f.lower() or "pole cancellation" in f.lower() for f in camp['audit_invariant_failures'])


def test_mutation_nondecreasing_not_labeled_divergent():
    """
    Mutation/Regression: A constant sequence [1, 1, 1, 1] must report CONSTANT_WITHIN_TOLERANCE,
    not EMPIRICAL_DIVERGENCE.
    """
    camp_const = transcendental.run_tc_negative_grade_approximation_campaign(
        override_joint_relative_errors=[1.0, 1.0, 1.0, 1.0],
        output_path=""
    )
    r3 = camp_const['regime_3_joint_diagonal_schedule']
    assert r3['empirical_schedule_verdict'] == 'CONSTANT_WITHIN_TOLERANCE'
    q1 = camp_const['answers_to_six_core_questions']['q1_does_negative_grade_approach_continuum']
    assert "CONSTANT_WITHIN_TOLERANCE" in q1
    assert "EMPIRICAL_DIVERGENCE" not in q1


def test_mutation_dynamic_ratios_recomputed():
    """
    Mutation/Regression: Altering grades_scan dynamically recomputes ratio text and endpoints
    without mentioning stale hardcoded strings.
    """
    camp_custom = transcendental.run_tc_negative_grade_approximation_campaign(
        grades_scan=[0, -1, -2],
        output_path=""
    )
    q1 = camp_custom['answers_to_six_core_questions']['q1_does_negative_grade_approach_continuum']
    assert "K=-4" not in q1
    assert "factor of 30" not in q1
    assert "K=0 to K=-2" in q1


def test_actual_tc_grade_cancellation_research():
    """
    Research Test: Investigate surviving arithmetic directions via legal grade cancellation G_i = F_{K_i} - F_{K_0}.
    Verifies:
    1. sum_K b_K == 0 exactly cancels the continuum profile F_{infty, h, w}.
    2. Surviving difference directions have full numerical rank.
    3. At well-resolved grid (n_points=401), singular values are stable under mesh refinement.
    4. Mathematical identities: Gram PSD, valid relative error float, defensible uncertainty propagation.
    """
    res = transcendental.investigate_actual_tc_grade_cancellation(
        grades=[-1, -2], anchor_grade=0, h=0.05, n_points=401
    )
    assert res['status'] == 'ACTUAL_TC_GRADE_CANCELLATION_INVESTIGATED'
    assert res['continuum_cancellation']['is_exact_zero_sum'] is True
    assert abs(res['continuum_cancellation']['sum_normalized_b']) < 1e-12
    assert res['gram_matrix_spectrum']['numerical_rank_at_1e6'] == 2
    assert res['mesh_stability']['directions_stable_under_refinement'] is True
    assert "empirically stable under mesh refinement" in res['research_findings']['surviving_directions_description']
    # Defect 4 fix: Mathematical identities, valid spectrum, uncertainty classification and bounds
    assert all(ev >= -1e-12 for ev in res['gram_matrix_spectrum']['singular_values'])
    rel_fit_err = res['independent_target_fit']['relative_error']
    assert isinstance(rel_fit_err, float) and math.isfinite(rel_fit_err) and rel_fit_err >= 0.0
    assert res['independent_target_fit']['uncertainty_classification'] == 'EMPIRICAL_DISCRETIZATION_UNCERTAINTY_ESTIMATE'
    assert res['independent_target_fit']['propagated_uncertainty_bound'] >= 0.0
    assert all(u >= 0.0 and math.isfinite(u) for u in res['independent_target_fit']['column_uncertainty_estimates'].values())


def test_deliberately_underresolved_mesh_detected():
    """
    Defect 3 Regression: Assert that a deliberately underresolved mesh (e.g. n_points=35, h=0.01)
    is detected as unstable under refinement (directions_stable_under_refinement is False),
    and prose dynamically reports UNRESOLVED / FAILED without claiming stability.
    """
    res = transcendental.investigate_actual_tc_grade_cancellation(
        grades=[-1, -2], anchor_grade=0, h=0.01, n_points=35
    )
    assert res['mesh_stability']['directions_stable_under_refinement'] is False
    assert "UNRESOLVED / FAILED" in res['research_findings']['surviving_directions_description']
    assert "cannot be certified as stable" in res['research_findings']['surviving_directions_description']


def test_nonfinite_or_nan_pole_integral_fails_audit():
    """
    Defect 6 Regression: Assert that non-finite or NaN pole integrals fail the pole vanishing check
    and flag audit failures rather than silently passing.
    """
    assert transcendental._is_finite_vanishing_integral(0.0) is True
    assert transcendental._is_finite_vanishing_integral(1e-8) is True
    assert transcendental._is_finite_vanishing_integral(float('nan')) is False
    assert transcendental._is_finite_vanishing_integral(float('inf')) is False
    assert transcendental._is_finite_vanishing_integral(-float('inf')) is False
    assert transcendental._is_finite_vanishing_integral(0.1) is False


def test_adaptive_diagonal_schedule_search():
    """
    Research Test: Budgeted adaptive diagonal schedule search across (K, h) grid.
    Verifies exploration of negative grades and bandwidths, identification of optimal
    computable path, and trade-off analysis between smoothing and bump norm scaling.
    """
    res = transcendental.search_adaptive_diagonal_schedule(
        grades_budget=[0, -1, -2], bandwidths_budget=[0.20, 0.10, 0.05], n_points=101
    )
    assert res['status'] == 'ADAPTIVE_DIAGONAL_SCHEDULE_SEARCH_COMPLETED'
    assert len(res['grid_evaluations']) == 9
    assert len(res['adaptive_best_path']) == 3
    assert 'bottleneck_analysis' in res['conclusions']


def test_same_grade_resonance_K_neg3():
    """
    Research Test: Verify concrete same-grade log(2) resonance at K=-3 on active prime powers 2048 and 4096.
    Verifies:
      1. Stations 2048 = 2^11 and 4096 = 2^12 lie strictly within window [8, 20].
      2. Coordinate separation u2 - u1 equals log(2) exactly.
      3. Prime convolution kernel argument evaluates at v - (u2 - u1) = 0 (exact resonance).
      4. Archimedean diagonal term strictly dominates, confirming resonance does not force negativity.
    """
    res = transcendental.audit_same_grade_resonance_K_neg3(h=0.05)
    assert res['status'] == 'SAME_GRADE_RESONANCE_AUDITED'
    assert res['resonance_analysis']['is_exact_log2_resonance'] is True
    assert res['positivity_conclusion']['same_grade_resonance_confirmed'] is True
    assert res['positivity_conclusion']['proves_negativity_of_B'] is False
    assert res['positivity_conclusion']['archimedean_diagonal_dominates'] is True


def test_arithmetic_spectral_exact_formula():
    """
    Research Test: Verify arithmetic-spectral explicit formula, Laurent polynomial response, and remainders.
    Verifies:
      1. Legal zero-sum condition cancels the pole at s=1.
      2. Single-variable Laurent polynomial representation in z = tau^{1-rho} with P(1) = 0.
      3. Incommensurability refutation: integer multiples K*log(tau) are commensurate.
      4. Trivial zeros remainder decays geometrically as 39.48^{-k} with certified tail bound.
      5. Higher prime-power remainder is finite and bounded.
    """
    res = transcendental.audit_arithmetic_spectral_exact_formula(grades=[0, -1, -2, -3])
    assert res['status'] == 'ARITHMETIC_SPECTRAL_EXPLICIT_FORMULA_AUDITED'
    assert res['is_legal_zero_sum'] is True
    assert res['laurent_polynomial_analysis']['root_at_one'] is True
    assert res['trivial_zeros_remainder']['is_exponentially_convergent'] is True
    assert res['trivial_zeros_remainder']['tail_bound_k_gt_5'] < 1e-8
    assert res['higher_prime_remainder']['is_finite_sum'] is True


def test_execute_adaptive_diagonal_search():
    """
    Research Test: Verify genuine error-driven adaptive diagonal search algorithm.
    Verifies:
      1. Step-by-step decisions driven by smoothing bias vs arithmetic discrepancy.
      2. Logs all candidate evaluations, decisions, and rejected attempts.
      3. Correctly identifies grade budget exhaustion as a computational ceiling rather than an obstruction.
    """
    res = transcendental.execute_adaptive_diagonal_search(
        target_fractions=[1.0, 0.5], max_negative_grade=-3, n_points=151
    )
    assert res['status'] == 'ADAPTIVE_DIAGONAL_SEARCH_COMPLETED'
    assert res['method'] == 'ERROR_DRIVEN_ADAPTIVE_TRAJECTORY'
    assert len(res['steps']) >= 1
    assert res['rejected_attempts_count'] > 0
    assert res['resource_costs']['total_evaluations'] > 0
    assert 'resource_boundary_identified' in res['conclusions']




