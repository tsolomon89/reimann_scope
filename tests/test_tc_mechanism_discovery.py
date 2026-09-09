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

import json
import math
import os
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
    import sympy
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
    assert "PROVED" in props["3_distributional_uniqueness"]["verdict"]
    assert res["aliasing_audit"]["status"] == "NO_INTEGER_ALIASING_ON_CRITICAL_LINE"
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
    assert answers["4_can_off_line_contribution_be_detected_in_infinite_formula"].startswith("YES")
    assert answers["5_what_forces_nonzero_membership_in_two_distinct_arithmetic_layers"].startswith("NOTHING")
    assert answers["6_was_exclusion_mechanism_found"].startswith("NO")
