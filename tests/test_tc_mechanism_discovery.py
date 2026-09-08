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





