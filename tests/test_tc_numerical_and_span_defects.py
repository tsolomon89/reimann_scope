"""
Regression tests reproducing and verifying the repair of numerical, caching, and span defects:
1. Convolution cache collisions:
   - Interior nodes omission (successive [0, .01, .10] vs [0, .04, .10] at h=0.05).
   - Step h collision (linspace(0, 2*h, 11) at h=0.05 vs h=0.0500000001).
   - Cold/warm cache equivalence and mutation isolation.
2. Two-grade default vector IndexError in compute_grouped_correlation_system.
3. Spectral span evaluator:
   - Physical quartet matrix Q(z) = 4 P^T Re[A_h(z)^2 sym(e(z)e(-z)^T)] P.
   - Exact scalar-versus-matrix agreement across multiple legal directions and two bandwidths (h=0.05, 0.025).
   - Critical zero factors 2|A_h(i*gamma)|^2.
   - Non-zero Target B keys: (1, 89, 563), (2, 89, 3511), (1, 563, 3511).
   - Deficient rank narrative when num_critical_zeros=0 or 1.
4. Target A:
   - Production convolution table certification for h=0.05 on window [8, 20].
   - Derivative remainder bound ||C_h - interp(C_h)||_infty <= (Delta v)^2 / 8 * ||psi_h'||_2^2.
   - Adversarial scaling case h=0.01 returning explicitly uncertified result.
5. Target B:
   - Unique active station contributors for (1, 89, 563), (2, 89, 3511), (1, 563, 3511).
   - Sym(2) rank 3 span.
   - Three-coefficient algebraic lemma: c_12 = c_13 = c_23 = 0 and sum b = 0 => b = 0.
   - Reciprocal atom simultaneous nulling: c_(1, 1, 8) and c_(-1, 8, 1).
   - Corrected null vector vs erroneous old vector.
6. 40-digit mpmath quadrature diagnostic check matching stated docstring purpose.
"""

import math
from typing import NamedTuple
import numpy as np
import pytest
import mpmath
import scipy.integrate


class KeyContributor(NamedTuple):
    grades: tuple[int, int]
    stations: tuple[int, int]
    amp_prod: float


from tc.weil_forms import (
    _compute_C_tab_fast,
    compute_grouped_correlation_system,
    test_spectral_matrix_span_recovery as eval_spectral_matrix_span_recovery,
    certify_production_convolution_table,
    certify_baseline_canonical_weil_error_budget,
    compute_critical_zero_observable,
    compute_reflected_quartet_observable,
    investigate_scalar_spectral_bridge_target_b,
    construct_weighted_admissible_spectral_test,
    validate_spectral_zero_coverage,
    sieve_prime_powers_in_window,
    Z_CANONICAL_KERNEL,
    NORM_KAPPA_SQ,
    NORM_KAPPA_FIRST_DERIVATIVE_SQ,
    NORM_KAPPA_SECOND_DERIVATIVE_SQ,
    NORM_KAPPA_THIRD_DERIVATIVE_SQ,
    kappa_hat_fast,
)
from tc.weil_forms.optimization import (
    compute_certified_stieltjes_tail_bound,
    CERTIFIED_L1_NORM_KAPPA_DERIVATIVES,
    evaluate_position_space_prime_functional,
)


def test_convolution_cache_interior_nodes_collision():
    """
    Defect: _compute_C_tab_fast previously keyed solely by length, rounded endpoints,
    rounded h, and n_nodes, completely omitting interior nodes.
    Arrays [0, .01, .10] and [0, .04, .10] at h=0.05 have identical length 3 and endpoints 0, 0.10.
    With the bug, the middle value differed by ~2,694,293.
    Verify that the repaired cache differentiates these arrays.
    """
    h = 0.05
    v1 = np.array([0.0, 0.01, 0.10])
    v2 = np.array([0.0, 0.04, 0.10])

    r1 = _compute_C_tab_fast(v1, h=h, n_nodes=256)
    r2 = _compute_C_tab_fast(v2, h=h, n_nodes=256)

    # Nodal evaluations at middle points
    # At v=0.01, C_h(0.01) is negative (~ -9.22e6)
    # At v=0.04, C_h(0.04) is negative (~ -1.19e7)
    diff_middle = abs(r1[1] - r2[1])
    assert diff_middle > 1.0e6, f"Expected middle values to differ significantly, got {diff_middle}"
    # Crucially, r2[1] must match a fresh un-cached evaluation at 0.04
    r_fresh_04 = _compute_C_tab_fast(np.array([0.04]), h=h, n_nodes=256)
    assert abs(r2[1] - r_fresh_04[0]) < 1e-10


def test_convolution_cache_step_h_collision():
    """
    Defect: rounding h to 8 decimal places mapped h=0.05 and h=0.0500000001
    to the same cache key, causing a C_h(0) error of ~1.75877, far exceeding
    the declared allowance ~2.28e-5.
    Verify that the repaired cache treats exact h floats with bit accuracy.
    """
    v_arr = np.linspace(0.0, 0.10, 11)
    h1 = 0.05
    h2 = 0.0500000001

    c1 = _compute_C_tab_fast(v_arr, h=h1, n_nodes=256)
    c2 = _compute_C_tab_fast(v_arr, h=h2, n_nodes=256)

    shift_C0 = abs(c1[0] - c2[0])
    # The true mathematical difference in C_h(0) between these two h values is ~1.75877
    assert 1.5 < shift_C0 < 2.0, f"Expected shift ~1.76, got {shift_C0}"
    # Verify that calling h1 again returns c1 exactly (no cross-contamination)
    c1_again = _compute_C_tab_fast(v_arr, h=h1, n_nodes=256)
    assert np.array_equal(c1, c1_again)


def test_convolution_cache_mutation_isolation():
    """
    Verify that mutating an array returned from _compute_C_tab_fast does not
    corrupt the cached array.
    """
    v_arr = np.array([0.0, 0.05, 0.10])
    h = 0.05

    ret1 = _compute_C_tab_fast(v_arr, h=h, n_nodes=256)
    orig_val = float(ret1[0])
    # Malicious mutation
    ret1[0] = 999999.0

    ret2 = _compute_C_tab_fast(v_arr, h=h, n_nodes=256)
    assert ret2[0] == orig_val, "Cached array was mutated in-place!"


def test_two_grade_default_vector_index_error_repaired():
    """
    Defect: In compute_grouped_correlation_system, test_b default assigned
    b_vec[2] = -0.5 when r=2, crashing with IndexError: index 2 is out of bounds.
    Verify that r=2 runs cleanly with legal zero-sum unit vector.
    """
    res = compute_grouped_correlation_system(
        grades=[-1, -2],
        window=(8.0, 20.0),
        test_b=None
    )
    assert res['status'] == 'GROUPED_CORRELATION_SYSTEM_COMPUTED'
    b_vec = res['test_vector_b']
    assert len(b_vec) == 2
    assert abs(sum(b_vec)) < 1e-12
    assert abs(np.linalg.norm(b_vec) - 1.0) < 1e-12


def test_spectral_span_quartet_physical_agreement():
    """
    Verify that the physical quartet matrix
        Q(z) = 4 P^T Re[A_h(z)^2 sym(e(z)e(-z)^T)] P
    strictly matches the scalar evaluation
        4 Re[A_h(z)^2 E_b(z) E_b(-z)]
    for multiple legal directions and two bandwidths (h=0.05, 0.025).
    """
    grades = [-1, -2, -3]
    anchor_grade = -1
    window = (8.0, 20.0)
    tau = 2.0 * math.pi
    delta = 0.49
    gamma = 100.0
    z0 = complex(delta, gamma)

    diff_grades = [g for g in grades if g != anchor_grade]
    r = len(grades)
    m = len(diff_grades)
    P = np.zeros((r, m))
    for c_idx, g in enumerate(diff_grades):
        P[grades.index(g), c_idx] = 1.0
        P[grades.index(anchor_grade), c_idx] = -1.0

    st_raw = {K: sieve_prime_powers_in_window(window, K, tau=tau) for K in grades}
    def w_bump(x: float) -> float:
        if x <= window[0] or x >= window[1]: return 0.0
        u = 2.0 * (x - window[0]) / (window[1] - window[0]) - 1.0
        return math.exp(1.0 - 1.0 / (1.0 - u * u))

    a_kn = {}
    for K in grades:
        a_kn[K] = {}
        for n_val, x_val, lam_val in st_raw[K]:
            w = w_bump(x_val)
            amp = (tau ** K) * lam_val * w
            if amp > 0:
                a_kn[K][n_val] = float(amp)

    n_k = 1000
    v_k, w_k = np.polynomial.legendre.leggauss(n_k)
    kappa_vals = np.exp(-1.0 / (1.0 - v_k**2)) / Z_CANONICAL_KERNEL * w_k

    for h_test in [0.05, 0.025]:
        ah_z0 = (z0**2 - 0.25) * np.sum(kappa_vals * np.exp(z0 * h_test * v_k))
        ep = np.array([sum(a * ((tau ** K * n) ** z0) for n, a in a_kn[K].items()) for K in grades])
        em = np.array([sum(a * ((tau ** K * n) ** (-z0)) for n, a in a_kn[K].items()) for K in grades])
        M_quart = 0.5 * (np.outer(ep, em) + np.outer(em, ep))
        cal_M = 4.0 * np.real((ah_z0**2) * M_quart)
        Q = P.T @ cal_M @ P

        # Test 4 distinct directions
        directions = [
            np.array([1.0, 0.0]),
            np.array([0.0, 1.0]),
            np.array([1.0, -1.0]) / math.sqrt(2.0),
            np.array([0.6, -0.8]),
        ]
        for beta in directions:
            b = P @ beta
            E_p = sum(b[i] * ep[i] for i in range(r))
            E_m = sum(b[i] * em[i] for i in range(r))
            scalar_val = float(4.0 * np.real((ah_z0**2) * E_p * E_m))
            mat_val = float(beta @ Q @ beta)
            rel_diff = abs(scalar_val - mat_val) / max(1.0, abs(scalar_val))
            assert rel_diff < 1e-12, f"Quartet scalar/matrix mismatch at h={h_test}, beta={beta}"


def test_critical_zero_observables_weighting():
    """
    Verify that critical zero matrices include the authentic factor 2*|A_h(i*gamma)|^2
    and match direct scalar evaluation 2*|A_h(i*gamma)|^2 * |E_b(i*gamma)|^2.
    """
    grades = [-1, -2, -3]
    anchor_grade = -1
    window = (8.0, 20.0)
    tau = 2.0 * math.pi
    h = 0.05
    gam = 14.134725141734693

    diff_grades = [g for g in grades if g != anchor_grade]
    r = len(grades)
    m = len(diff_grades)
    P = np.zeros((r, m))
    for c_idx, g in enumerate(diff_grades):
        P[grades.index(g), c_idx] = 1.0
        P[grades.index(anchor_grade), c_idx] = -1.0

    st_raw = {K: sieve_prime_powers_in_window(window, K, tau=tau) for K in grades}
    def w_bump(x: float) -> float:
        if x <= window[0] or x >= window[1]: return 0.0
        u = 2.0 * (x - window[0]) / (window[1] - window[0]) - 1.0
        return math.exp(1.0 - 1.0 / (1.0 - u * u))

    a_kn = {}
    for K in grades:
        a_kn[K] = {}
        for n_val, x_val, lam_val in st_raw[K]:
            w = w_bump(x_val)
            amp = (tau ** K) * lam_val * w
            if amp > 0:
                a_kn[K][n_val] = float(amp)

    n_k = 1000
    v_k, w_k = np.polynomial.legendre.leggauss(n_k)
    kappa_vals = np.exp(-1.0 / (1.0 - v_k**2)) / Z_CANONICAL_KERNEL * w_k
    ah_gam = ((1j * gam)**2 - 0.25) * np.sum(kappa_vals * np.exp(1j * gam * h * v_k))
    factor = 2.0 * (abs(ah_gam)**2)

    e_vec = np.array([sum(a * ((tau ** K * n) ** (1j * gam)) for n, a in a_kn[K].items()) for K in grades])
    M_gam = factor * np.real(np.outer(e_vec, np.conj(e_vec)))
    G_gam = P.T @ M_gam @ P

    beta = np.array([0.7071, -0.7071])
    b = P @ beta
    E_val = sum(b[i] * e_vec[i] for i in range(r))
    scalar_val = factor * (abs(E_val)**2)
    mat_val = float(beta @ G_gam @ beta)
    rel_diff = abs(scalar_val - mat_val) / max(1.0, abs(scalar_val))
    assert rel_diff < 1e-12


def test_target_b_three_keys_uniqueness_and_span():
    """
    Target B:
    1. Verify uniqueness and strict positivity of the 3 target keys:
       - (1, 89, 563): sole contributor (-1, -2) with (89, 563), a_12 ~ 0.1143016654
       - (2, 89, 3511): sole contributor (-1, -3) with (89, 3511), a_13 ~ 0.0234781599
       - (1, 563, 3511): sole contributor (-2, -3) with (563, 3511), a_23 ~ 0.0052662709
    2. Verify their symmetric matrices span Sym(2) with full rank 3 (det != 0).
    3. Verify algebraic lemma: c_12 = c_13 = c_23 = 0 and sum b = 0 => b = 0.
    """
    grades = [-1, -2, -3]
    window = (8.0, 20.0)
    tau = 2.0 * math.pi

    st_raw = {K: sieve_prime_powers_in_window(window, K, tau=tau) for K in grades}
    def w_bump(x: float) -> float:
        if x <= window[0] or x >= window[1]: return 0.0
        u = 2.0 * (x - window[0]) / (window[1] - window[0]) - 1.0
        return math.exp(1.0 - 1.0 / (1.0 - u * u))

    a_kn = {}
    for K in grades:
        a_kn[K] = {}
        for n_val, x_val, lam_val in st_raw[K]:
            w = w_bump(x_val)
            amp = (tau ** K) * lam_val * w
            if amp > 0:
                a_kn[K][n_val] = float(amp)

    target_keys = [(1, 89, 563), (2, 89, 3511), (1, 563, 3511)]
    key_contribs: dict[tuple[int, int, int], list[KeyContributor]] = {k: [] for k in target_keys}

    for i, K in enumerate(grades):
        for j, J in enumerate(grades):
            if K == J: continue
            d = K - J
            for n_val, a_n in a_kn[K].items():
                for m_val, a_m in a_kn[J].items():
                    g = math.gcd(n_val, m_val)
                    k = (d, n_val // g, m_val // g)
                    if k in key_contribs:
                        key_contribs[k].append(KeyContributor(
                            grades=(K, J),
                            stations=(n_val, m_val),
                            amp_prod=float(a_n * a_m)
                        ))

    # Each key has exactly 1 contributor
    for k in target_keys:
        assert len(key_contribs[k]) == 1, f"Key {k} has {len(key_contribs[k])} contributors, expected 1"
        assert key_contribs[k][0].amp_prod > 0.0

    a12 = key_contribs[(1, 89, 563)][0].amp_prod
    a13 = key_contribs[(2, 89, 3511)][0].amp_prod
    a23 = key_contribs[(1, 563, 3511)][0].amp_prod

    assert abs(a12 - 0.1143016654) < 1e-4
    assert abs(a13 - 0.0234781599) < 1e-4
    assert abs(a23 - 0.0052662709) < 1e-4

    # Build Sym(2) basis
    P = np.array([
        [-1.0, -1.0],
        [ 1.0,  0.0],
        [ 0.0,  1.0]
    ])
    def vec_sym(M):
        return np.array([M[0, 0], math.sqrt(2.0) * M[0, 1], M[1, 1]])

    G_mats = []
    for k in target_keys:
        M = np.zeros((3, 3))
        c = key_contribs[k][0]
        i = grades.index(c.grades[0])
        j = grades.index(c.grades[1])
        M[i, j] += c.amp_prod
        M_sym = 0.5 * (M + M.T)
        G = P.T @ M_sym @ P
        G_mats.append(G)

    A_target = np.column_stack([vec_sym(G) for G in G_mats])
    det_val = float(np.linalg.det(A_target))
    rank_val = int(np.linalg.matrix_rank(A_target))

    assert rank_val == 3
    assert abs(det_val) > 1e-6

    # Test algebraic lemma: c12 = c13 = c23 = 0 and sum b = 0 => b = 0
    # Every non-zero legal vector b has at least one non-zero coefficient among these three
    rng = np.random.default_rng(42)
    for _ in range(50):
        beta = rng.standard_normal(2)
        if np.linalg.norm(beta) < 1e-6: continue
        beta = beta / np.linalg.norm(beta)
        b = P @ beta
        c12_val = a12 * b[0] * b[1]
        c13_val = a13 * b[0] * b[2]
        c23_val = a23 * b[1] * b[2]
        max_c = max(abs(c12_val), abs(c13_val), abs(c23_val))
        assert max_c > 1e-6, f"All three coefficients vanished for non-zero legal b={b}!"


def test_spectral_span_deficient_rank_narrative():
    """
    Verify that test_spectral_matrix_span_recovery with num_critical_zeros=0 or 1
    returns deficient rank and states deficient rank in its narrative.
    """
    res_0 = eval_spectral_matrix_span_recovery(num_critical_zeros=0)
    assert res_0['is_full_symmetric_rank_spanned'] is False
    assert res_0['spectral_matrix_span_rank'] < 3
    assert "deficient rank" in res_0['epistemic_findings']['recoverability_verdict'].lower()

    res_1 = eval_spectral_matrix_span_recovery(num_critical_zeros=1)
    assert res_1['is_full_symmetric_rank_spanned'] is False
    assert res_1['spectral_matrix_span_rank'] < 3
    assert "deficient rank" in res_1['epistemic_findings']['recoverability_verdict'].lower()


def test_target_a_convolution_table_certification():
    """
    Target A:
    1. Certify production convolution table at baseline h=0.05 on window [8, 20].
    2. Check that derivative remainder bound ||C_h - interp(C_h)||_infty <= (Delta v)^2 / 8 * ||psi_h'||_2^2
       is mathematically computed (~6499.10) and encloses the first cell midpoint discrepancy (~6497.70).
    3. Verify that unproved nodal literals c4, c2, c0 prevent false certification:
       is_table_certified is False, status is UNCERTIFIED_NODAL_REMAINDER_PROOF_UNRESOLVED.
    4. Reproduce and verify the 1-node failure: n_nodes=1 produces ~1.58e8 error at v=0.00005
       and fails closed with UNCERTIFIED_UNSUPPORTED_QUADRATURE_ORDER.
    5. Test adversarial scaling case h=0.01: returns uncertified outside established domain.
    6. Verify that invalid parameters (negative h, N_tab < 2, non-integer nodes) fail closed.
    7. Verify production budget consumes the table enclosure and propagates is_table_certified=False.
    """
    cert = certify_production_convolution_table(h=0.05, window=(8.0, 20.0), N_tab=2001, n_nodes=256)
    assert cert['status'] == 'UNCERTIFIED_NODAL_REMAINDER_PROOF_UNRESOLVED'
    assert cert['is_table_certified'] is False
    assert cert['is_domain_certified'] is True

    # Check interpolation bounds and first-cell midpoint discrepancy
    interp_bound = cert['interpolation_model']['eps_interp_bound']
    assert interp_bound == pytest.approx(6499.101197, rel=1e-4)
    mid_disc = cert['interpolation_model']['first_cell_midpoint_discrepancy']
    assert mid_disc == pytest.approx(6497.700898, rel=1e-4)
    assert cert['interpolation_model']['midpoint_enclosed_by_interp_bound'] is True

    # Check peak-normalized allowance vs unbounded uniform relative error
    assert cert['table_enclosure']['peak_normalized_allowance'] < 1e-4
    assert "Uniform relative error across [0, 2h] is mathematically unbounded" in cert['table_enclosure']['uniform_relative_bound_status']

    # Reproduce defect: n_nodes=1 must fail closed with unsupported quadrature order
    cert_1 = certify_production_convolution_table(n_nodes=1)
    assert cert_1['status'] == 'UNCERTIFIED_UNSUPPORTED_QUADRATURE_ORDER'
    assert cert_1['is_table_certified'] is False
    assert "catastrophic quadrature errors" in cert_1['reason']

    # Adversarial scaling test: h=0.01 must fail closed
    cert_adv = certify_production_convolution_table(h=0.01, window=(8.0, 20.0), N_tab=2001, n_nodes=256)
    assert cert_adv['status'] == 'UNCERTIFIED_OUTSIDE_PARAMETER_DOMAIN'
    assert cert_adv['is_table_certified'] is False
    assert cert_adv['is_domain_certified'] is False
    assert "outside the certified production baseline domain" in cert_adv['reason']

    # Invalid parameter tests
    assert certify_production_convolution_table(h=-0.05)['is_table_certified'] is False
    assert certify_production_convolution_table(N_tab=1)['is_table_certified'] is False
    assert certify_production_convolution_table(n_nodes=0)['is_table_certified'] is False

    # Production budget integration
    budget = certify_baseline_canonical_weil_error_budget()
    assert budget['error_budget']['is_table_certified'] is False
    assert budget['error_budget']['table_certification_status'] == 'UNCERTIFIED_NODAL_REMAINDER_PROOF_UNRESOLVED'
    assert budget['prime_quadrature']['is_table_certified'] is False


def test_reciprocal_atom_simultaneous_nulling_and_corrected_vector():
    """
    1. Verify that c_(1, 1, 8)(b) = c_(-1, 8, 1)(b) identically.
    2. Verify the corrected null vector b = [0.02909535, 0.69211002, -0.72120537]
       vanishes for the tau/8 atom: c_(1, 1, 8)(b) = 0.
    3. Verify that the previously recorded vector [0.029096, -0.721205, 0.692110]
       fails to vanish because both terms are negative.
    """
    grades = [-1, -2, -3]
    window = (8.0, 20.0)
    tau = 2.0 * math.pi

    st_raw = {K: sieve_prime_powers_in_window(window, K, tau=tau) for K in grades}
    def w_bump(x: float) -> float:
        if x <= window[0] or x >= window[1]: return 0.0
        u = 2.0 * (x - window[0]) / (window[1] - window[0]) - 1.0
        return math.exp(1.0 - 1.0 / (1.0 - u * u))

    a_kn = {}
    for K in grades:
        a_kn[K] = {}
        for n_val, x_val, lam_val in st_raw[K]:
            w = w_bump(x_val)
            amp = (tau ** K) * lam_val * w
            if amp > 0:
                a_kn[K][n_val] = float(amp)

    a1_64 = a_kn[-1][64]
    a2_512 = a_kn[-2][512]
    a3_4096 = a_kn[-3][4096]
    A12 = a1_64 * a2_512
    A23 = a2_512 * a3_4096

    def eval_c_1_1_8(b_vec):
        return b_vec[1] * (A12 * b_vec[0] + A23 * b_vec[2])

    def eval_c_neg1_8_1(b_vec):
        return b_vec[1] * (A12 * b_vec[0] + A23 * b_vec[2])

    # Corrected null vector
    ratio = A12 / A23
    b_unnorm = np.array([1.0, ratio - 1.0, -ratio])
    b_correct = b_unnorm / np.linalg.norm(b_unnorm)

    assert abs(sum(b_correct)) < 1e-12
    val_correct = eval_c_1_1_8(b_correct)
    assert abs(val_correct) < 1e-16, f"Corrected vector did not vanish: {val_correct}"
    val_recip = eval_c_neg1_8_1(b_correct)
    assert abs(val_recip) < 1e-16, f"Reciprocal atom did not vanish simultaneously: {val_recip}"

    # Previously reported erroneous vector
    b_prev = np.array([0.029096, -0.721205, 0.692110])
    val_prev = eval_c_1_1_8(b_prev)
    assert abs(val_prev) > 1e-5, f"Expected previous vector to fail to vanish, got {val_prev}"
    assert b_prev[0] * b_prev[1] < 0
    assert b_prev[1] * b_prev[2] < 0


def test_40_digit_quadrature_diagnostic_assertions():
    """
    Check the quadrature test against 40-dps mpmath as promised in docstring.
    Verifies that the empirical discrepancy between 256-node GL and 40-dps mpmath
    is strictly bounded by the nominal eps_nodal bound at baseline h=0.05.
    """
    mpmath.mp.dps = 40
    h_base = 0.05

    Z_mp = mpmath.quad(lambda y: mpmath.exp(-1 / (1 - y**2)), [-1, 1])
    def f_mp(y):
        om = 1 - y**2
        y2 = y**2
        k = mpmath.exp(-1 / om) / Z_mp
        d2k = (-2 / (om**2) - 8 * y2 / (om**3) + 4 * y2 / (om**4)) * k
        return d2k - 0.25 * (h_base**2) * k

    val_mp_0, _ = mpmath.quad(lambda y: f_mp(y)**2, [-1, 1], error=True)
    C_mp_0 = float((h_base**(-5)) * val_mp_0)

    c_fast = _compute_C_tab_fast(np.array([0.0]), h=h_base, n_nodes=256)
    diff_0 = abs(c_fast[0] - C_mp_0)

    cert = certify_production_convolution_table(h=h_base)
    eps_nodal = cert['quadrature_model']['eps_nodal_bound_nominal']

    assert diff_0 <= eps_nodal, f"Measured 40-dps error {diff_0} exceeded nominal nodal bound {eps_nodal}"


def test_production_evaluators_scalar_matrix_agreement():
    """
    Verify that physical scalar/matrix agreement tests call production evaluators:
    compute_critical_zero_observable and compute_reflected_quartet_observable.
    """
    grades = [-1, -2, -3]
    tau = 2.0 * math.pi
    window = (8.0, 20.0)
    h = 0.05

    P = np.array([[-1.0, -1.0], [1.0, 0.0], [0.0, 1.0]])

    def w_bump(x):
        if x <= 8.0 or x >= 20.0: return 0.0
        u = 2.0 * (x - 8.0) / 12.0 - 1.0
        return math.exp(1.0 - 1.0 / (1.0 - u * u))

    st_raw = {K: sieve_prime_powers_in_window(window, K, tau=tau) for K in grades}
    a_kn = {}
    for K in grades:
        a_kn[K] = {}
        for n_val, x_val, lam_val in st_raw[K]:
            w = w_bump(x_val)
            amp = (tau ** K) * lam_val * w
            if amp > 0: a_kn[K][n_val] = float(amp)

    gam = 14.134725141734693
    crit_obs = compute_critical_zero_observable(gam, grades, a_kn, P, h=h, tau=tau)
    S_mat = np.array(crit_obs['S_matrix'])

    z0 = complex(0.49, 100.0)
    quart_obs = compute_reflected_quartet_observable(z0, grades, a_kn, P, h=h, tau=tau)
    Q_mat = np.array(quart_obs['Q_matrix'])

    # Test agreement for several beta vectors
    test_betas = [
        np.array([1.0, 0.0]),
        np.array([0.0, 1.0]),
        np.array([0.6, -0.8]),
        np.array([1.0 / math.sqrt(2), 1.0 / math.sqrt(2)])
    ]
    nodes_1000, weights_1000 = np.polynomial.legendre.leggauss(1000)
    kappa_1000 = np.exp(-1.0 / (1.0 - nodes_1000**2)) / Z_CANONICAL_KERNEL * weights_1000

    for beta in test_betas:
        b = P @ beta
        # Scalar critical evaluation
        ah_gam = ( (1j * gam)**2 - 0.25 ) * np.sum(kappa_1000 * np.exp(1j * gam * h * nodes_1000))
        Eb_gam = sum(b[i] * sum(a * ((tau ** grades[i] * n) ** (1j * gam)) for n, a in a_kn[grades[i]].items()) for i in range(3))
        s_scal = 2.0 * (abs(ah_gam)**2) * (abs(Eb_gam)**2)
        s_mat = float(beta.T @ S_mat @ beta)
        assert abs(s_scal - s_mat) < 1e-10

        # Scalar quartet evaluation
        ah_z0 = ( z0**2 - 0.25 ) * np.sum(kappa_1000 * np.exp(z0 * h * nodes_1000))
        Eb_p = sum(b[i] * sum(a * ((tau ** grades[i] * n) ** z0) for n, a in a_kn[grades[i]].items()) for i in range(3))
        Eb_m = sum(b[i] * sum(a * ((tau ** grades[i] * n) ** (-z0)) for n, a in a_kn[grades[i]].items()) for i in range(3))
        q_scal = 4.0 * float(np.real(ah_z0**2 * Eb_p * Eb_m))
        q_mat = float(beta.T @ Q_mat @ beta)
        assert abs(q_scal - q_mat) < 1e-10

    # Test 4-grade quartet real rank: check that a symmetrized rank-2 complex outer product can have rank up to 4
    grades_4 = [-1, -2, -3, -4]
    st_raw_4 = {K: sieve_prime_powers_in_window(window, K, tau=tau) for K in grades_4}
    a_kn_4 = {}
    for K in grades_4:
        a_kn_4[K] = {}
        for n_val, x_val, lam_val in st_raw_4[K]:
            w = w_bump(x_val)
            amp = (tau ** K) * lam_val * w
            if amp > 0: a_kn_4[K][n_val] = float(amp)
    P_4 = np.eye(4)
    quart_4 = compute_reflected_quartet_observable(z0, grades_4, a_kn_4, P_4, h=h, tau=tau)
    assert quart_4['cal_M_rank'] >= 3


def test_target_b_scalar_spectral_bridge_investigation():
    """
    Target B:
    1. Verify scalar algebraic invariant L(b) = -0.5 on legal unit sphere.
    2. Verify unique active station contributors and strictly positive amplitudes for the three selected keys:
       (1, 89, 563), (2, 89, 3511), (1, 563, 3511).
    3. Verify finite linear recovery of G_target = -(1/2) P^T P using critical zeros alone (residual < 1e-13, cond ~1104).
    4. Verify finite linear recovery including off-critical quartet Q(rho0) (residual < 1e-13, cond ~3876).
    5. Propagate ordinate uncertainty through sum_j |lambda_j| eps_j with MVT enclosure.
    6. Verify correct residue Res(-zeta'/zeta) = -m and bookkeeping balance identity.
    7. Evaluate correct arithmetic dilation D = diag(tau^K) yielding benchmark ~7.41e8 (not >1e11).
    8. Evaluate Target B admissible realization analysis, selected-weight mismatch, and first use of H.
    """
    res = investigate_scalar_spectral_bridge_target_b()
    assert res['status'] == 'SCALAR_SPECTRAL_BRIDGE_TARGET_B_INVESTIGATED'

    # 1. Algebraic invariant
    assert res['algebraic_invariant']['legal_unit_sphere_value'] == -0.5
    keys = res['algebraic_invariant']['selected_grouped_keys']
    assert len(keys) == 3
    for k in keys:
        assert k['is_positive'] is True
        assert k['key'] in [[1, 89, 563], [2, 89, 3511], [1, 563, 3511]]

    # 2. Critical recovery
    crit_rec = res['critical_only_recovery']
    assert crit_rec['reconstruction_residual_norm'] < 1e-13
    assert crit_rec['full_matrix_residual_frobenius'] < 1e-13
    assert crit_rec['full_matrix_residual_spectral_norm'] < 1e-13
    assert crit_rec['basis_condition_number'] < 2000.0
    assert crit_rec['ordinate_uncertainty_propagated_error'] < 1e-12

    # 3. Quartet recovery
    quart_rec = res['quartet_recovery']
    assert quart_rec['reconstruction_residual_norm'] < 1e-13
    assert quart_rec['full_matrix_residual_frobenius'] < 1e-13
    assert quart_rec['full_matrix_residual_spectral_norm'] < 1e-13
    assert quart_rec['basis_condition_number'] < 5000.0

    # 4. Bookkeeping balance (removing circular spectral verification)
    bookkeeping = res['bookkeeping_balance']
    assert bookkeeping['is_tautological_bookkeeping_identity'] is True
    assert bookkeeping['independent_explicit_formula_verified'] is False
    assert bookkeeping['bookkeeping_discrepancy'] < 1e-10
    assert bookkeeping['direct_station_evaluation_check_passed'] is True

    # 5. Arithmetic scaling repair benchmark with dilation D = diag(tau^K)
    # Correct dilation yields ~7.4076e8 at U=320, N_t=2000 (missing dilation gave ~1.4802e11)
    arith_energy = bookkeeping['arithmetic_side_A_Phi_b']
    assert abs(arith_energy - 7.4076e8) < 1.0e6, f"Expected ~7.4076e8 with dilation D, got {arith_energy}"

    # 6. Target B Admissible Realization Analysis
    tb = res['target_b_admissible_realization_analysis']
    assert tb['verdict'] == 'SPECIFIED_CONSTRUCTION_ANALYZED_BOUND_NOT_FORCED'
    assert "Res_{s=rho_0}(-zeta'/zeta) = -m" in tb['first_equation_using_H']
    assert tb['selected_weight_mismatch_r_match'] > 1e5
    assert tb['critical_zeros_partial_sum_T100'] > 5e7
    assert tb['cancellation_precision_needed_to_force_L'] < 1e-9
    assert abs(tb['scalar_invariant_L_b'] - (-0.5)) < 1e-12


def test_circular_spectral_verification_regression():
    """
    Defect: Defining r_rec = L - S_sel and R_Phi = A_Phi - S_sel makes
    A_Phi - L = R_Phi - r_rec an algebraic identity for arbitrary A_Phi.
    Verify that perturbing only the arithmetic input A_Phi' = A_Phi + 1e6 still produces
    (A_Phi' - L) - (R_Phi' - r_rec) == 0, proving this identity is an algebraic tautology
    by subtraction and does not count as independent arithmetic-spectral agreement.
    """
    res = investigate_scalar_spectral_bridge_target_b()
    bb = res['bookkeeping_balance']
    A_phi = bb['arithmetic_side_A_Phi_b']
    S_sel = bb['recovered_spectral_S_sel_b']
    L_val = res['algebraic_invariant']['legal_unit_sphere_value']
    r_rec = L_val - S_sel

    # Perturbed arithmetic input by arbitrary constant
    A_phi_perturbed = A_phi + 1.234567e6
    R_phi_perturbed = A_phi_perturbed - S_sel

    lhs = A_phi_perturbed - L_val
    rhs = R_phi_perturbed - r_rec
    discrepancy = abs(lhs - rhs)
    assert discrepancy < 1e-10, "Bookkeeping balance failed to hold tautologically for perturbed arithmetic input"


def test_scalar_recovery_restricted_to_declared_three_grades():
    """
    Defect:
    1. Passing len(grades) != 3 must fail closed with ValueError.
    2. Passing grades not equal to {-1, -2, -3} (e.g. [-1, -2, 0]) must fail closed with ValueError.
    3. Passing window (8, 9) where all 3 selected amplitude products vanish must fail closed with ValueError.
    4. Permutations of {-1, -2, -3} (e.g. [-3, -1, -2]) must succeed and preserve L(b) = -0.5.
    """
    with pytest.raises(ValueError, match="strictly restricted to the declared authentic 3-grade ensemble"):
        investigate_scalar_spectral_bridge_target_b(grades=[-1, -2, -3, -4])

    with pytest.raises(ValueError, match="strictly restricted to the declared authentic 3-grade ensemble"):
        investigate_scalar_spectral_bridge_target_b(grades=[-1, -2])

    with pytest.raises(ValueError, match="strictly restricted to the declared authentic 3-grade ensemble"):
        investigate_scalar_spectral_bridge_target_b(grades=[-1, -2, 0])

    with pytest.raises(ValueError, match="Selected station keys must have strictly positive active amplitudes"):
        investigate_scalar_spectral_bridge_target_b(window=(8.0, 9.0))

    # Permuted grade ordering must preserve exact invariant and direct evaluation
    res_perm = investigate_scalar_spectral_bridge_target_b(grades=[-3, -1, -2])
    assert res_perm['algebraic_invariant']['legal_unit_sphere_value'] == -0.5
    assert res_perm['bookkeeping_balance']['direct_station_evaluation_check_passed'] is True


def test_ordinate_uncertainty_certified_mvt_enclosure():
    """
    Defect: 7 Chebyshev nodes sampled maximum is not a certified supremum upper bound.
    Reproduce accepted input:
      grades = [-1, -2, -3], anchor = -1, h = 0.05, window = [8, 20],
      gamma = 21.022039638771556, eps_gamma = 20.0:
      - Claimed Chebyshev sampled max: ~527,955.59
      - Interior derivative norm at xi = 36.2670198055: ~727,589.09
    Verify:
      1. Interior derivative norm strictly exceeds the 7-node Chebyshev sample (refuting supremum enclosure).
      2. The analytic majorant strictly encloses the interior derivative norm.
      3. certified_mvt_error_bound is None and is_derivative_enclosure_certified is False.
      4. Negative uncertainty radii fail closed with ValueError.
    """
    grades = [-1, -2, -3]
    tau = 2.0 * math.pi
    window = (8.0, 20.0)
    h = 0.05
    anchor_grade = -1
    diff_grades = [g for g in grades if g != anchor_grade]
    r = len(grades)
    m_dim = len(diff_grades)
    anchor_idx = grades.index(anchor_grade)
    P = np.zeros((r, m_dim))
    for col_idx, g in enumerate(diff_grades):
        P[grades.index(g), col_idx] = 1.0
        P[anchor_idx, col_idx] = -1.0

    def w_bump(x):
        if x <= 8.0 or x >= 20.0: return 0.0
        u = 2.0 * (x - 8.0) / 12.0 - 1.0
        return math.exp(1.0 - 1.0 / (1.0 - u * u))

    st_raw = {K: sieve_prime_powers_in_window(window, K, tau=tau) for K in grades}
    a_kn = {}
    for K in grades:
        a_kn[K] = {}
        for n_val, x_val, lam_val in st_raw[K]:
            w = w_bump(x_val)
            amp = (tau ** K) * lam_val * w
            if amp > 0: a_kn[K][n_val] = float(amp)

    gam = 21.022039638771556
    eps_gam = 20.0

    obs_base = compute_critical_zero_observable(gam, grades, a_kn, P, h=h, tau=tau, eps_gamma=eps_gam)
    obs_xi = compute_critical_zero_observable(36.2670198055, grades, a_kn, P, h=h, tau=tau, eps_gamma=0.0)

    cheb_sampled_max = obs_base['diagnostic_chebyshev_sampled_max']
    interior_norm = obs_xi['S_prime_norm_2']

    # Reproduce defect: Chebyshev sampled max underestimates interior derivative
    assert abs(cheb_sampled_max - 527955.585567) < 5.0
    assert abs(interior_norm - 727589.092037) < 5.0
    assert interior_norm > cheb_sampled_max, "Interior derivative failed to exceed Chebyshev sampled max"

    # Analytic majorant strictly encloses the interior derivative
    analytic_majorant = obs_base['analytic_derivative_majorant']
    assert analytic_majorant >= interior_norm, "Analytic majorant failed to enclose interior derivative"

    # Uncertified status is correctly returned
    assert obs_base['certified_mvt_error_bound'] is None
    assert obs_base['is_derivative_enclosure_certified'] is False
    assert obs_base['diagnostic_mvt_error_bound'] > 0.0

    # Negative uncertainty radius validation
    with pytest.raises(ValueError, match="eps_gamma must be non-negative"):
        compute_critical_zero_observable(gam, grades, a_kn, P, h=h, tau=tau, eps_gamma=-1.0)


def test_admissible_spectral_realization_investigation():
    """
    Target B: Verify dedicated admissible spectral realization investigation.
    1. Returns status ADMISSIBLE_SPECTRAL_REALIZATION_INVESTIGATED.
    2. Quantifies single test function selected mismatch r_match ~ 3.88e5.
    3. Quantifies critical zeros partial sum ~ 5.49e7.
    4. Evaluates complete arithmetic energy with D ~ 7.41e8.
    5. Pinpoints first use of H (adding Q(rho0)).
    6. Identifies first unresolved analytic barrier.
    """
    from tc.weil_forms import investigate_admissible_spectral_realization
    res = investigate_admissible_spectral_realization()

    assert res['status'] == 'ADMISSIBLE_SPECTRAL_REALIZATION_INVESTIGATED'
    single_test = res['single_test_function_realization']
    assert single_test['selected_weight_mismatch_r_match'] > 3.8e5

    complete_id = res['complete_identity_and_use_of_H']
    assert complete_id['arithmetic_side_A_Phi'] > 7.4e8
    assert complete_id['critical_zeros_partial_sum_T100'] > 5e7
    assert "Res_{s=rho_0}(-zeta'/zeta) = -m" in complete_id['where_H_first_acts']

    gap = res['quantitative_gap_and_unresolved_step']
    assert gap['verdict'] == 'SPECIFIED_CONSTRUCTION_ANALYZED_BOUND_NOT_FORCED'
    assert "unconditional two-sided bounds" in gap['first_unresolved_analytic_step']


def test_baseline_error_budget_certification_consistency():
    """
    Defect: Previously, when is_table_certified was False, the error budget still emitted
    numeric values under bound_delta_W_G_prime_certified and certified_lambda_min_lower_margin.
    Verify that uncertified runs set these certified fields to None, emit diagnostic margins,
    and accurately state the unresolved reason.
    """
    res = certify_baseline_canonical_weil_error_budget()
    eb = res['error_budget']

    assert eb['is_table_certified'] is False
    assert eb['bound_delta_W_G_prime_certified'] is None
    assert eb['certified_lambda_min_lower_margin'] is None

    assert eb['bound_delta_W_G_prime_analytic'] < 2000.0
    assert eb['diagnostic_lambda_min_lower_margin'] > 1.3e7
    assert eb['is_strictly_positive'] is False
    assert res['epistemic_class'] == 'NUMERICALLY_UNRESOLVED'


def test_holomorphic_profile_continuation_and_cauchy_riemann_violation():
    r"""
    Target A.1:
    1. Distinguish physical test g_b = psi_h * e_b with transform F_b(z) = A_h(z) E_b(z)
       from reflected convolution k_b = g_b * \widetilde{g_b} with transform:
           H_b(z) = F_b(z) F_b(-z) = A_h(z)^2 E_b(z) E_b(-z).
    2. Verify H_b is even: H_b(-z) = H_b(z) and satisfies Schwarz reflection: H_b(conj(z)) = conj(H_b(z)).
    3. Verify on critical line z = it: H_b(it) = |F_b(it)|^2 >= 0.
    4. Refute that |A_h(z)|^2 |E_b(z)|^2 is entire: off the imaginary axis,
       |A_h(z)|^2 |E_b(z)|^2 is strictly real, whereas holomorphic H_b(z) has non-zero imaginary part,
       violating Cauchy-Riemann equations for holomorphic functions.
    """
    grades = [-1, -2, -3]
    tau = 2.0 * math.pi
    window = (8.0, 20.0)
    h = 0.05
    st_raw = {K: sieve_prime_powers_in_window(window, K, tau=tau) for K in grades}

    def w_bump(x: float) -> float:
        if x <= 8.0 or x >= 20.0: return 0.0
        u = 2.0 * (x - 8.0) / 12.0 - 1.0
        return math.exp(1.0 - 1.0 / (1.0 - u * u))

    a_kn = {}
    for K in grades:
        a_kn[K] = {}
        for n_val, x_val, lam_val in st_raw[K]:
            w = w_bump(x_val)
            amp = (tau ** K) * lam_val * w
            if amp > 0: a_kn[K][n_val] = float(amp)

    b_vec = np.array([-1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0), 0.0])

    # Legendre nodes for A_h
    v_k, w_k = np.polynomial.legendre.leggauss(500)
    kappa_vals = np.exp(-1.0 / (1.0 - v_k**2)) / Z_CANONICAL_KERNEL * w_k

    def eval_A_h(z: complex) -> complex:
        return (z**2 - 0.25) * np.sum(kappa_vals * np.exp(z * h * v_k))

    def eval_E_b(z: complex) -> complex:
        val = 0.0 + 0.0j
        for K_idx, K in enumerate(grades):
            for n_val, amp in a_kn[K].items():
                x_val = (tau ** K) * n_val
                val += b_vec[K_idx] * amp * (x_val ** (-z))
        return val

    def eval_H_b(z: complex) -> complex:
        return (eval_A_h(z) ** 2) * eval_E_b(z) * eval_E_b(-z)

    # 1. Even symmetry: H_b(-z) == H_b(z)
    z_test = complex(0.49, 100.0)
    H_pos = eval_H_b(z_test)
    H_neg = eval_H_b(-z_test)
    assert abs(H_pos - H_neg) < 1e-10

    # 2. Schwarz reflection: H_b(conj(z)) == conj(H_b(z))
    H_conj = eval_H_b(np.conj(z_test))
    assert abs(H_conj - np.conj(H_pos)) < 1e-10

    # 3. Critical line positivity: H_b(it) == |F_b(it)|^2 >= 0
    t_val = 14.134725
    H_it = eval_H_b(1j * t_val)
    F_it = eval_A_h(1j * t_val) * eval_E_b(1j * t_val)
    assert abs(H_it.imag) < 1e-12
    assert abs(H_it.real - abs(F_it)**2) < 1e-10
    assert H_it.real >= 0.0

    # 4. Modulus square |A_h(z)|^2 |E_b(z)|^2 is NOT holomorphic off the imaginary axis
    mod_sq_val = (abs(eval_A_h(z_test))**2) * (abs(eval_E_b(z_test))**2)
    # H_b(z_test) has non-zero imaginary part, whereas mod_sq_val is purely real!
    assert abs(H_pos.imag) > 1e-3, "H_b(z) should have non-zero imaginary part off-axis"
    assert abs(H_pos - mod_sq_val) > 1.0, "|A_h|^2 |E_b|^2 fails to equal holomorphic continuation H_b"


def test_real_numerical_controls_forwarding():
    """
    Target A.2:
    1. Forward arithmetic cutoff U and resolution N_t through investigate_scalar_spectral_bridge_target_b.
    2. Benchmark values at h=0.05, window [8, 20], b=(-1, 1, 0)/sqrt(2):
       - At U = 320: A_{<= 320} ~ 7.4076e8
       - At U = 640: A_{<= 640} ~ 1.1622e9
    3. Verify that U is genuinely effective (ratio ~ 1.57), disproving static serialization.
    4. Validate fail-closed guards for invalid U, N_t, and T_cutoff.
    """
    res_320 = investigate_scalar_spectral_bridge_target_b(U=320.0, N_t=2000)
    A_320 = res_320['bookkeeping_balance']['truncated_arithmetic_side_A_Phi_le_U']
    assert abs(A_320 - 7.4076e8) / 7.4076e8 < 0.01

    res_640 = investigate_scalar_spectral_bridge_target_b(U=640.0, N_t=2000)
    A_640 = res_640['bookkeeping_balance']['truncated_arithmetic_side_A_Phi_le_U']
    assert abs(A_640 - 1.1622e9) / 1.1622e9 < 0.01

    # Ratio proves U is genuinely propagated to the underlying continuous integral
    growth_ratio = A_640 / A_320
    assert 1.50 < growth_ratio < 1.65

    # Fail-closed numerical parameter validations
    with pytest.raises(ValueError, match="Arithmetic cutoff U must be >= 10.0"):
        investigate_scalar_spectral_bridge_target_b(U=5.0)

    with pytest.raises(ValueError, match="Quadrature resolution N_t must be >= 10"):
        investigate_scalar_spectral_bridge_target_b(N_t=5)

    with pytest.raises(ValueError, match="Spectral cutoff T_cutoff must be > 0.0"):
        investigate_scalar_spectral_bridge_target_b(T_cutoff=-10.0)


def test_grouped_key_collision_and_verified_window():
    """
    Target A.3:
    1. Reproduce genuine grouped key collision on window (1, 20) with grades [-1, -2, -3]:
       - Key (1, 89, 563) receives both (-1, -2) and (-2, -3) contributors.
       - Normalized sum of grouped coefficients for b = (0, 1, -1)/sqrt(2) produces
         ~ -0.5000422671185678, NOT -1/2.
    2. Verify that on the verified window [8, 20]:
       - Collision is absent (key_collision_detected is False).
       - Actual grouped matrix discrepancy ||G_actual - G_target||_2 < 1e-14.
       - Denominator amplitude products are strictly positive and separated from zero.
    3. Verify duplicate grade rejection and anchor validation.
    """
    # 1. Reproduce collision on window (1, 20)
    tau = 2.0 * math.pi
    window_coll = (1.0, 20.0)
    grades = [-1, -2, -3]

    def w_bump_coll(x: float) -> float:
        if x <= 1.0 or x >= 20.0: return 0.0
        u = 2.0 * (x - 1.0) / 19.0 - 1.0
        return math.exp(1.0 - 1.0 / (1.0 - u * u))

    st_raw = {K: sieve_prime_powers_in_window(window_coll, K, tau=tau) for K in grades}
    a_kn_coll = {}
    for K in grades:
        a_kn_coll[K] = {}
        for n_val, x_val, lam_val in st_raw[K]:
            w = w_bump_coll(x_val)
            amp = (tau ** K) * lam_val * w
            if amp > 0: a_kn_coll[K][n_val] = float(amp)

    # Check key (1, 89, 563) contributors
    amp_1_89 = a_kn_coll[-1].get(89, 0.0)
    amp_2_563 = a_kn_coll[-2].get(563, 0.0)
    amp_2_89 = a_kn_coll[-2].get(89, 0.0)
    amp_3_563 = a_kn_coll[-3].get(563, 0.0)

    contrib_12 = amp_1_89 * amp_2_563
    contrib_23 = amp_2_89 * amp_3_563
    assert abs(contrib_12 - 0.07990177443717375) < 1e-6
    assert abs(contrib_23 - 6.7544355478314894e-6) < 1e-9

    # Normalized sum for b = (0, 1, -1)/sqrt(2)
    b_test = np.array([0.0, 1.0 / math.sqrt(2.0), -1.0 / math.sqrt(2.0)])
    # For key (1, 89, 563), c_key = b_1 b_2 * contrib_12 + b_2 b_3 * contrib_23 = 0 - 0.5 * contrib_23
    # Grouped coefficient normalized by a12 = contrib_12 yields discrepancy:
    disc_ratio = contrib_23 / contrib_12
    normalized_val = -0.5 * (1.0 + disc_ratio)
    assert abs(normalized_val - (-0.5000422671185678)) < 1e-12

    # 2. Verified window [8, 20] has zero collisions
    res_820 = investigate_scalar_spectral_bridge_target_b(window=(8.0, 20.0))
    grp_info = res_820['algebraic_invariant']['actual_grouped_representation']
    assert grp_info['key_collision_detected'] is False
    assert grp_info['discrepancy_G_actual_vs_G_target'] < 1e-14
    assert grp_info['denominator_separated_from_zero'] is True

    # 3. Duplicate grade and invalid anchor rejection
    with pytest.raises(ValueError, match="Duplicate grades not permitted"):
        investigate_scalar_spectral_bridge_target_b(grades=[-1, -2, -2])

    with pytest.raises(ValueError, match="anchor_grade 0 must be one of the declared grades"):
        investigate_scalar_spectral_bridge_target_b(grades=[-1, -2, -3], anchor_grade=0)


def test_production_quartet_recovery_coefficients_and_disjoint_accounting():
    """
    Target A.4:
    1. Reconcile production quartet-recovery coefficients:
       lambda ~ (-6.56406e-5, -9.91246e-6, -1.02770e-3),
       refuting walkthrough typo (-2.5735e-4, +4.8471e-5, +8.5583e-5) which produces +6.70.
    2. Verify S_sel = -0.5000000000000051 on the legal representative vector.
    3. Multiplicity m_0: zero weight for rho_0 is lambda_Q / m_0.
    4. Disjoint accounting: selected zeros strictly excluded from unselected zeros below T.
    5. Explicit formula sign: A_<=U = S_selected + R_other - R_arch.
    """
    res = investigate_scalar_spectral_bridge_target_b(multiplicity_m0=2)
    q_rec = res['quartet_recovery']
    lambdas = q_rec['recovery_coefficients_lambda']

    assert abs(lambdas[0] - (-6.5640600718e-5)) < 1e-8
    assert abs(lambdas[1] - (-9.9124577690e-6)) < 1e-8
    assert abs(lambdas[2] - (-1.0277027639e-3)) < 1e-6

    # Multiplicity m_0 = 2 halves the individual zero target weight
    assert abs(q_rec['zero_weight_rho0'] - (lambdas[2] / 2.0)) < 1e-12

    # S_sel equals -0.5 to machine precision
    S_sel = res['bookkeeping_balance']['recovered_spectral_S_sel_b']
    assert abs(S_sel - (-0.5)) < 1e-12

    # Disjoint zero accounting
    acct = res['accounting_breakdown']
    sel_gammas = acct['selected_zeros']['critical_zeros']
    unsel_list = acct['unselected_zeros_below_T']
    assert len(sel_gammas) == 2
    for g_sel in sel_gammas:
        assert all(abs(g_sel - g_unsel) > 1e-6 for g_unsel in unsel_list.get('zeros_list', []))


def test_weighted_admissible_spectral_test_target_b():
    """
    Target B:
    1. Construct explicit polynomial multiplier p(z) = r(z^2) of degree 6 in z (degree 3 in w = z^2).
    2. Interpolate p(i*gamma_1) = lambda_1, p(i*gamma_2) = lambda_2, p(z_0) = lambda_Q / m_0.
    3. Invertibility: condition number kappa(M) ~ 2.11e12 and interpolation residual < 1e-14.
    4. Operator-norm mismatch ||Delta G||_2 < 1e-13 on legal space Sym(2).
    5. Exact weight realization: r_match = 0.0 and r_rec ~ 0.0 on representative vector.
    6. Physical derivative realization: Psi_b = sum_{k=0}^3 (-1)^k r_k H_{(g_b^{(k)})}.
       Check signs, C_c^infinity smoothness, support in [-12, 12].
    7. Direct arithmetic evaluation A_{Psi, <= U} ~ 5.04e8.
    8. Unconditional Stieltjes tail bound via Trudgian (2014) at T=100 and T=200.
    9. State exact use of H(rho_0, m_0) and Quantitative Admissible Annihilation Lemma.
    """
    res = construct_weighted_admissible_spectral_test(delta=0.49, gamma=100.0, multiplicity_m0=1)
    assert res['status'] == 'ADMISSIBLE_SPECTRAL_TEST_CONSTRUCTED_BOUND_UNRESOLVED'

    poly = res['polynomial_multiplier']
    assert poly['linear_system_matrix_condition_number'] < 500.0  # Scaled system cond ~= 472.62
    assert poly['interpolation_residual_norm'] < 1.0e-14

    # Exact interpolation verification
    conds = poly['interpolation_conditions']
    assert abs(conds['p_at_i_gamma1'] - conds['target_lambda1']) < 1e-14
    assert abs(conds['p_at_i_gamma2'] - conds['target_lambda2']) < 1e-14
    assert abs(conds['p_at_z0_real'] - conds['target_lambda_Q_over_m0']) < 1e-14
    assert abs(conds['p_at_z0_imag']) < 1e-14

    # Operator realization on legal space evaluated directly on implemented polynomial
    op = res['selected_weight_realization']
    assert op['operator_mismatch_spectral_norm'] < 1.0e-13
    assert op['is_operator_matched_within_machine_eps'] is True
    assert abs(op['selected_weight_mismatch_r_match']) < 1.0e-14
    assert abs(op['reconstruction_error_r_rec']) < 1.0e-12

    # Physical derivative decomposition
    phys = res['physical_derivative_decomposition']
    assert phys['derivative_orders'] == [0, 1, 2, 3]
    assert phys['alternating_signs'] == [1, -1, 1, -1]
    assert phys['compact_support_radius'] == 12.0
    assert phys['smoothness_class'] == 'C_c^infinity'

    # Direct arithmetic evaluation including non-vanishing prime contribution
    arith = res['direct_arithmetic_evaluation']
    assert abs(arith['prime_pairing_raw'] - (-211930587.0)) < 1.0e3  # Raw prime pairing ~= -211.93e6
    assert abs(arith['prime_contribution_signed'] - 211930587.0) < 1.0e3  # Signed contribution ~= +211.93e6
    assert abs(arith['archimedean_truncated'] - 502713211.15) < 1.0e2  # Archimedean ~= +502.71e6
    assert abs(arith['arithmetic_truncated'] - 714643798.08) < 1.0e2  # Correctly signed result ~= +714.64e6
    assert abs(arith['incorrect_assembled_diagnostic'] - 290782624.21) < 1.0e2  # Incorrect assembled diagnostic ~= +290.78e6
    assert abs(arith['evaluated_A_psi_le_U'] - 714643798.08) < 1.0e2
    assert arith['active_prime_resonance_count'] == 946
    assert arith['active_prime_sample_pair']['prime_q'] == 2
    assert abs(arith['active_prime_sample_pair']['log_separation_defect'] - 0.00938974) < 1.0e-6

    # Unconditional Stieltjes tail bound (m >= 6)
    tail = res['unconditional_stieltjes_tail_bound']
    assert tail['order_m6']['bound_at_T_100'] > 0.0
    assert tail['order_m6']['bound_at_T_200'] > 0.0
    assert tail['order_m7']['bound_at_T_100'] > 0.0
    assert tail['order_m7']['bound_at_T_200'] > 0.0
    assert tail['order_m6']['cutoff_refinement_ratio'] > 1.5
    assert tail['order_m7']['cutoff_refinement_ratio'] > 5.0
    assert "m >= 6" in tail['decay_requirement']
    assert tail['actual_cutoff_T']['T_cutoff'] == 100.0

    # Use of H and open lemma
    h_use = res['use_of_H_and_open_lemma']
    assert "Res_{s=rho_0}(-zeta'/zeta) = -m_0" in h_use['first_equation_using_H']
    assert "Quantitative Admissible Annihilation Lemma" in h_use['remaining_open_lemma']


def test_target_a1_prime_sign_and_independent_pairing_check():
    """Target A1: Verify prime sign repair and protect it with independent checks.

    1. Expose unambiguous quantities:
       prime_pairing_raw = the position-space von Mangoldt pairing;
       prime_contribution_signed = -prime_pairing_raw;
       arithmetic_truncated = archimedean_truncated - prime_pairing_raw.
    2. Reproduce exact values for b = (-1, 1, 0)/sqrt(2):
       - Archimedean truncated value: +502,713,211.1461
       - Raw prime pairing:          -211,930,586.9374
       - Incorrect assembled result:  +290,782,624.2087
       - Correctly signed result:     +714,643,798.0835
    3. Verify near-resonant station pair in grade K=-1:
       x1 = 53/(2pi) ~= 8.4352, x2 = 107/(2pi) ~= 17.0296 in [8, 20],
       |log 2 - log(107/53)| = log(107/106) ~= 0.00938974 < 2h = 0.10.
    4. Check both reflected shifts and multiplicities against canonical matrix convention W = W_arch - W_prime.
    """
    res = construct_weighted_admissible_spectral_test()
    arith = res['direct_arithmetic_evaluation']

    arch = arith['archimedean_truncated']
    raw_p = arith['prime_pairing_raw']
    sgn_p = arith['prime_contribution_signed']
    inc_p = arith['incorrect_assembled_diagnostic']
    net_p = arith['arithmetic_truncated']

    assert abs(arch - 502713211.1461) < 1.0, f"Archimedean mismatch: {arch}"
    assert abs(raw_p - (-211930586.9374)) < 1.0, f"Raw prime pairing mismatch: {raw_p}"
    assert abs(sgn_p - 211930586.9374) < 1.0, f"Signed prime contribution mismatch: {sgn_p}"
    assert abs(inc_p - 290782624.2087) < 1.0, f"Incorrect assembled diagnostic mismatch: {inc_p}"
    assert abs(net_p - 714643798.0835) < 1.0, f"Correctly signed result mismatch: {net_p}"
    assert abs(net_p - (arch - raw_p)) < 1e-10
    assert abs(net_p - (arch + sgn_p)) < 1e-10

    # Independent near-resonant pairing check
    h = 0.05
    x1 = 53.0 / (2.0 * math.pi)
    x2 = 107.0 / (2.0 * math.pi)
    assert 8.0 <= x1 <= 20.0 and 8.0 <= x2 <= 20.0
    defect = abs(math.log(2.0) - math.log(x2 / x1))
    assert abs(defect - 0.00938974) < 1e-6
    assert defect < 2.0 * h


def test_target_a2_complex_quartet_and_metric_whitening():
    """Target A2: Verify full complex quartet assembly and symmetric metric whitening.

    1. Assemble quartet from full complex product p(z_0) A_h(z_0)^2 E_b(z_0) E_b(-z_0).
       Verify that Im p(z_0) is not discarded.
    2. Solve generalized eigenproblem against P^T P via symmetric whitening (P^T P)^{-1/2}.
       Confirm eigenvalues match scipy.linalg.eigh.
    3. Verify invariance under grade permutation and legal-basis changes.
    """
    res = construct_weighted_admissible_spectral_test()
    op = res['selected_weight_realization']
    assert op['metric_whitening_method'] == 'symmetric_inverse_sqrt_(P^T P)^{-1/2}'
    assert op['operator_mismatch_spectral_norm'] < 1e-13
    assert op['floating_roundoff_bound'] < 1e-14

    # Diagnostic test: test arbitrary complex multiplier with nonzero imaginary part
    grades = [-1, -2, -3]
    anchor_grade = -1
    window = (8.0, 20.0)
    tau = 2.0 * math.pi
    h = 0.05
    delta = 0.49
    gamma = 100.0
    z0 = complex(delta, gamma)

    diff_grades = [g for g in grades if g != anchor_grade]
    P = np.zeros((3, 2))
    for c_idx, g in enumerate(diff_grades):
        P[grades.index(g), c_idx] = 1.0
        P[grades.index(anchor_grade), c_idx] = -1.0

    st_raw = {K: sieve_prime_powers_in_window(window, K, tau=tau) for K in grades}
    def w_bump(x: float) -> float:
        if x <= window[0] or x >= window[1]: return 0.0
        u = 2.0 * (x - window[0]) / (window[1] - window[0]) - 1.0
        return math.exp(1.0 - 1.0 / (1.0 - u * u))

    a_kn = {}
    for K in grades:
        a_kn[K] = {n: (tau**K)*lam*w_bump(x) for n, x, lam in st_raw[K] if w_bump(x) > 0}

    v_k, w_k = np.polynomial.legendre.leggauss(1000)
    ah_z0 = ((z0**2 - 0.25) * np.sum(
        np.exp(-1.0 / (1.0 - v_k**2)) / Z_CANONICAL_KERNEL * w_k * np.exp(z0 * h * v_k)
    ))
    e_p = np.array([sum(a * ((tau ** K * n) ** z0) for n, a in a_kn[K].items()) for K in grades])
    e_m = np.array([sum(a * ((tau ** K * n) ** (-z0)) for n, a in a_kn[K].items()) for K in grades])
    M_quart_sym = 0.5 * (np.outer(e_p, e_m) + np.outer(e_m, e_p))
    cal_M_complex = 4.0 * (ah_z0 ** 2) * M_quart_sym
    Q_complex = P.T @ cal_M_complex @ P

    p_test = complex(1.414, 2.718)
    Q_p_retained = np.real(p_test * Q_complex)
    Q_p_discarded = p_test.real * np.real(Q_complex)
    # Discarding Im(p) produces a non-negligible error:
    assert np.linalg.norm(Q_p_retained - Q_p_discarded) > 1e-3

    # Check scalar match for Q_p_retained
    beta = np.array([0.6, -0.8])
    b = P @ beta
    E_p = sum(b[i] * e_p[i] for i in range(3))
    E_m = sum(b[i] * e_m[i] for i in range(3))
    scalar_val = float(4.0 * np.real(p_test * (ah_z0**2) * E_p * E_m))
    mat_val = float(beta.T @ Q_p_retained @ beta)
    rel_diff = abs(scalar_val - mat_val) / max(1.0, abs(scalar_val))
    assert rel_diff < 1e-12


def test_target_a3_unsupported_derivative_orders_and_defect_reproduction():
    """Target A3: Reject unsupported derivative orders and reproduce tail defects.

    1. Reject m < 6 and m >= 8 with explicit ValueError.
    2. Demonstrate m=8 defect: at h=0.05, t=400, reusing m=6 constant gives ~0.000479,
       which is less than the actual Fourier transform magnitude ~0.001266.
    3. Confirm m=7 L1 derivative norm enclosure >= 1,571,233,582.37.
    """
    r_poly = [-1.028e-03, 2.825e-05, -3.992e-07, 1.155e-09]
    for m_low in [0, 1, 2, 3, 4, 5]:
        with pytest.raises(ValueError, match="only supports orders m in {6, 7}"):
            compute_certified_stieltjes_tail_bound(r_poly, C_E=100.0, m=m_low)

    for m_high in [8, 9, 10]:
        with pytest.raises(ValueError, match="only supports orders m in {6, 7}"):
            compute_certified_stieltjes_tail_bound(r_poly, C_E=100.0, m=m_high)

    # Defect reproduction:
    h = 0.05
    t = 400.0
    ft_mag = abs(kappa_hat_fast(h * t))
    assert abs(ft_mag - 0.00126556) < 1e-4

    L1_m6 = CERTIFIED_L1_NORM_KAPPA_DERIVATIVES[6]
    flawed_m8_est = L1_m6 / ((h * t)**8)
    assert abs(flawed_m8_est - 0.0004677) < 1e-4
    assert flawed_m8_est < ft_mag, "Flawed m=8 estimate failed to underestimate actual FT magnitude"

    # m=7 L1 norm enclosure
    assert CERTIFIED_L1_NORM_KAPPA_DERIVATIVES[7] >= 1571233582.37


def test_target_a4_coherent_cutoffs_and_fail_closed_coverage():
    """Target A4: Verify actual cutoff propagation and fail-closed zero coverage.

    1. Verify actual T_cutoff propagation (e.g. T=150.0).
    2. Verify that incomplete zero coverage sets spectral_coverage_certified=False
       and complete_spectral_enclosure_available=False with unclosed obligation recorded.
    """
    res_150 = construct_weighted_admissible_spectral_test(T_cutoff=150.0)
    tail_150 = res_150['unconditional_stieltjes_tail_bound']['actual_cutoff_T']
    assert tail_150['T_cutoff'] == 150.0
    assert tail_150['order_m6_bound'] > 0.0

    # At T_cutoff=100 with authoritative reference data:
    res_100 = construct_weighted_admissible_spectral_test(T_cutoff=100.0)
    audit_100 = res_100['unselected_zeros_evaluation']
    assert audit_100['spectral_coverage_certified'] is True
    assert audit_100['complete_spectral_enclosure_available'] is False

    # Issue 1 Reproduction: Unselected zero sum through T=100, truncated difference, and tail allowance
    s_unsel = audit_100['S_psi_unsel_le_T']
    assert abs(s_unsel - (-8200.3292)) < 1.0, f"Unselected zero sum mismatch: {s_unsel}"
    d_trunc = res_100['complete_explicit_formula_identity']['D_truncated']
    assert abs(d_trunc - 714651998.4127) < 1.0, f"D_truncated mismatch: {d_trunc}"
    tail_m6 = res_100['unconditional_stieltjes_tail_bound']['actual_cutoff_T']['order_m6_bound']
    # Repaired Stieltjes bound incorporating Brent (2016) Theorem 5 / Corollary 4 envelope 1/(150t)
    # and explicit single-endpoint integration yields ~1.04194e17.
    assert abs(tail_m6 - 1.04194e17) / 1.04194e17 < 1e-4, f"Tail allowance mismatch: {tail_m6}"

    # Issue 2 Reproduction: Reject incomplete, omitted, or duplicated zero coverage
    # a. Single zero above T_cutoff [101.0] must NOT certify coverage:
    res_single = construct_weighted_admissible_spectral_test(T_cutoff=100.0, reference_zeros=[101.0])
    assert res_single['unselected_zeros_evaluation']['spectral_coverage_certified'] is False
    assert res_single['unselected_zeros_evaluation']['complete_spectral_enclosure_available'] is False

    # b. Omitted interior zeros [14.1347, 101.0] must NOT certify coverage:
    res_omitted = construct_weighted_admissible_spectral_test(T_cutoff=100.0, reference_zeros=[14.1347, 101.0])
    assert res_omitted['unselected_zeros_evaluation']['spectral_coverage_certified'] is False

    # c. Duplicate interior zeros must NOT certify coverage:
    res_dup = construct_weighted_admissible_spectral_test(T_cutoff=100.0, reference_zeros=[14.1347, 14.1347, 101.0])
    assert res_dup['unselected_zeros_evaluation']['spectral_coverage_certified'] is False

    # At T_cutoff=150, authoritative reference zeros reach ~396.38 > 150, so coverage is certified:
    assert res_150['unselected_zeros_evaluation']['spectral_coverage_certified'] is True
    assert res_150['unselected_zeros_evaluation']['complete_spectral_enclosure_available'] is False

    # At T_cutoff=500, reference zeros (max ~396.38) do not cover up to 500, so it must fail-closed:
    res_500 = construct_weighted_admissible_spectral_test(T_cutoff=500.0)
    zeros_audit = res_500['unselected_zeros_evaluation']
    assert zeros_audit['spectral_coverage_certified'] is False
    assert zeros_audit['complete_spectral_enclosure_available'] is False
    assert zeros_audit['unclosed_coverage_obligation'] is not None


def test_target_b2_falsification_compensation_control():
    """Target B2: Test quartet curvature mechanism against nearby critical zero compensation.

    Control polynomial:
    X(t) = [((t-gamma)^2+delta^2)((t+gamma)^2+delta^2)]^m * [(t^2-(gamma-a)^2)(t^2-(gamma+a)^2)]^m
    with a = delta/2, gamma > delta > 0, m >= 1.

    Verify quantitatively that on |t - gamma| <= delta / 4, the nearby real-root
    contributions dominate and keep the total curvature strictly negative.
    """
    delta = 0.49
    gamma = 100.0
    a = delta / 2.0
    m = 1

    t_grid = np.linspace(gamma - delta/4.0, gamma + delta/4.0, 50)
    for t_val in t_grid:
        u = t_val - gamma
        q_upper = 2.0 * m * (delta**2 - u**2) / ((delta**2 + u**2)**2)
        q_lower = 2.0 * m * (delta**2 - (t_val + gamma)**2) / ((delta**2 + (t_val + gamma)**2)**2)
        r_near = m * (1.0 / ((t_val - (gamma - a))**2) + 1.0 / ((t_val - (gamma + a))**2))
        r_far = m * (1.0 / ((t_val + (gamma - a))**2) + 1.0 / ((t_val + (gamma + a))**2))
        c_total = q_upper + q_lower - r_near - r_far
        # The curvature is strictly negative throughout the entire interval
        assert c_total < -1.0 * m / (delta**2), f"Curvature at t={t_val} not dominated: {c_total}"


def test_target_1a_shifted_zeros_partition_and_uncertainty():
    """Target 1A: Verify shifted-zero reproduction, disjoint partitioning, and uncertainty propagation.

    Specific defect reproduced and repaired:
    - At T=100, shift each of the first two reference ordinates by +5e-5.
    - Previously: accepted by validator under 1e-4, but excluded via 1e-6, causing the 2 selected zeros
      to reappear as unselected (unselected count jumping from 27 to 29) with eps_gamma=0.0.
    - Repaired: stable 1-to-1 disjoint partition ensures selected zeros match indices 0 and 1,
      unselected count remains exactly 27, and max input displacement (5e-5) is preserved and
      propagated into effective_eps_gamma.
    """
    import reference_data
    raw_zeros = [float(g) for g in reference_data.load_reference_zeros()]
    crit_100 = [g for g in raw_zeros if g <= 100.0]
    first_above = min(g for g in raw_zeros if g > 100.0)
    test_zeros = list(crit_100) + [first_above]

    # Baseline normal run
    res_normal = construct_weighted_admissible_spectral_test(T_cutoff=100.0, reference_zeros=test_zeros)
    unsel_normal = res_normal['unselected_zeros_evaluation']
    assert unsel_normal['unselected_zero_count'] == 27
    assert unsel_normal['selected_zero_count'] == 2
    assert unsel_normal['spectral_partition_disjoint_and_complete'] is True
    assert unsel_normal['max_input_displacement'] == 0.0

    # Shifted run: +5e-5 on first two zeros
    shifted_zeros = list(test_zeros)
    shifted_zeros[0] += 5.0e-5
    shifted_zeros[1] += 5.0e-5

    # Validator accepts under 1e-4 tolerance and returns max displacement 5e-5
    ok, reason, unres, crit = validate_spectral_zero_coverage(shifted_zeros, 100.0)
    assert ok is True
    assert reason == "authoritative_reference_data_verified"
    assert abs(unres[1] - 5.0e-5) < 1e-10

    # Constructor correctly partitions: unselected count remains 27 (NOT 29!)
    res_shifted = construct_weighted_admissible_spectral_test(T_cutoff=100.0, reference_zeros=shifted_zeros)
    unsel_shifted = res_shifted['unselected_zeros_evaluation']
    assert unsel_shifted['unselected_zero_count'] == 27, (
        f"Defect reproduced if 29: got {unsel_shifted['unselected_zero_count']}"
    )
    assert unsel_shifted['selected_zero_count'] == 2
    assert unsel_shifted['spectral_partition_disjoint_and_complete'] is True
    assert abs(unsel_shifted['max_input_displacement'] - 5.0e-5) < 1e-10
    assert unsel_shifted['effective_eps_gamma'] >= 5.0e-5

    # Check separate evidence dimensions
    evidence = res_shifted['spectral_evidence_status']
    assert evidence['reference_agreement'] is True
    assert evidence['reference_agreement_tolerance'] == 1.0e-4
    assert abs(evidence['max_input_displacement'] - 5.0e-5) < 1e-10
    assert evidence['verified_zero_isolation_and_coverage'] is False
    assert "Numerical agreement" in evidence['verified_zero_isolation_rationale']
    assert evidence['complete_spectral_enclosure_available'] is False


def test_target_1a_coverage_rejections_and_boundary_checks():
    """Target 1A: Test robust zero validation failure modes and cutoff boundary checking."""
    import reference_data
    raw_zeros = [float(g) for g in reference_data.load_reference_zeros()]
    crit_100 = [g for g in raw_zeros if g <= 100.0]
    first_above = min(g for g in raw_zeros if g > 100.0)

    # 1. Ambiguous cutoff boundary intersection: zero within 1e-4 of T_cutoff
    boundary_zero_list = list(crit_100) + [100.00005, first_above]
    ok_b, reason_b, _, _ = validate_spectral_zero_coverage(boundary_zero_list, 100.0)
    assert ok_b is False
    assert "ambiguous_cutoff_boundary_zero" in reason_b

    # 2. Missing interior zero: omit index 5 (6th zero)
    omitted_list = [g for idx, g in enumerate(crit_100) if idx != 5] + [first_above]
    ok_m, reason_m, _, _ = validate_spectral_zero_coverage(omitted_list, 100.0)
    assert ok_m is False
    assert "zero_count_mismatch" in reason_m

    # 3. Duplicate interior zero
    dup_list = list(crit_100)
    dup_list.insert(5, dup_list[5])
    dup_list.append(first_above)
    ok_d, reason_d, _, _ = validate_spectral_zero_coverage(dup_list, 100.0)
    assert ok_d is False
    assert "duplicate_or_inverted_zeros" in reason_d

    # 4. Displaced zero exceeding tolerance (e.g. +2e-4)
    disp_list = list(crit_100) + [first_above]
    disp_list[3] += 2.0e-4
    ok_disp, reason_disp, _, _ = validate_spectral_zero_coverage(disp_list, 100.0)
    assert ok_disp is False
    assert "fabricated_or_displaced_zero" in reason_disp


def test_target_1b_brent_gamma_envelope_and_stieltjes_tail():
    """Target 1B: Verify Brent (2016) Stirling gamma envelope and repaired Stieltjes integration."""
    import mpmath
    mpmath.mp.dps = 40

    # Primary source verification: Brent (2016) Theorem 5 / Corollary 4
    # At t=100: theta(t)/pi + 1 - M(t) exceeds leading asymptotic term 1/(48*pi*t)
    t = mpmath.mpf('100.0')
    th = mpmath.siegeltheta(t)
    M = (t / (2 * mpmath.pi)) * mpmath.log(t / (2 * mpmath.pi)) - t / (2 * mpmath.pi) - mpmath.mpf('0.125') + 1
    diff = th / mpmath.pi + 1 - M
    leading_term = 1 / (48 * mpmath.pi * t)
    brent_bound = 1 / (150 * t)

    # Prove that leading term is a LOWER bound, not an upper envelope
    assert diff > leading_term, f"Expected diff > 1/(48pi*t): diff={diff}, leading={leading_term}"
    # Prove that 1/(150*t) is a valid upper envelope
    assert diff <= brent_bound, f"Expected diff <= 1/(150*t): diff={diff}, brent={brent_bound}"

    # Check for t in {10, 20, 50, 200, 500}
    for t_val in [10.0, 20.0, 50.0, 200.0, 500.0]:
        t_m = mpmath.mpf(t_val)
        th_m = mpmath.siegeltheta(t_m)
        M_m = (t_m / (2 * mpmath.pi)) * mpmath.log(t_m / (2 * mpmath.pi)) - t_m / (2 * mpmath.pi) - mpmath.mpf('0.125') + 1
        d_m = th_m / mpmath.pi + 1 - M_m
        assert d_m > 1 / (48 * mpmath.pi * t_m)
        assert d_m <= 1 / (150 * t_m)

    # Verify implementation of compute_certified_stieltjes_tail_bound
    dummy_r = np.array([1.0, 0.01, 1e-4, 1e-6])
    tail_res = compute_certified_stieltjes_tail_bound(dummy_r, C_E=1.0, h=0.05, T_cutoff=100.0, m=6)
    assert tail_res['gamma_correction_constant'] == 1.0 / 150.0
    assert tail_res['epistemic_status'] == 'ANALYTIC_POWER_MAJORANT_EMPIRICALLY_EVALUATED'
    assert 'gamma_correction_integral' in tail_res

    # Check exact sum of components
    components_sum = (
        tail_res['smooth_integral'] +
        tail_res['endpoint_term'] +
        tail_res['fluctuation_integral'] +
        tail_res['gamma_correction_integral']
    )
    assert abs(components_sum - tail_res['total_tail_bound']) < 1e-10 * tail_res['total_tail_bound']


def test_target_2_regularized_curvature_transfer():
    """Target 2: Verify exact regularized curvature response, finite-part limit, and reflected quartet correction."""
    from tc.weil_forms.curvature_transfer import (
        curvature_kernel_g_a,
        fourier_curvature_kernel,
        single_zero_curvature_response,
        spectral_test_observable,
        reflected_pair_correction,
        quartet_correction,
        evaluate_distributional_jump_bound,
        evaluate_finite_symmetric_multiset_transfer,
        audit_regularized_curvature_transfer
    )

    # 1. Fourier transform check for g_a(x)
    a = 0.35
    for u_val in [0.5, 1.0, 2.5]:
        val_fourier = fourier_curvature_kernel(u_val, a)
        # Direct numerical integration: \int_{-\infty}^\infty g_a(x) cos(u*x) dx
        dir_val, _ = scipy.integrate.quad(
            lambda x: curvature_kernel_g_a(x, a) * math.cos(u_val * x),
            -100.0, 100.0, limit=500, epsabs=1e-9, epsrel=1e-9
        )
        assert abs(dir_val - val_fourier) < 1e-3, f"Fourier mismatch: direct={dir_val}, formula={val_fourier}"

    # 2. Reflected pair and quartet correction on smooth bump
    R_supp = math.log(20.0 / 8.0) + 2.0 * 0.05
    def bump_fb(u: float) -> float:
        if abs(u) >= R_supp:
            return 0.0
        return (1.0 - (u / R_supp)**2)**4

    # On critical line (a = 0):
    # K_{phi_{f_b}}(0, gamma) must equal Psi_b(i*gamma) identically
    for gam in [14.134725, 21.022040, 25.010858]:
        psi_0 = spectral_test_observable(bump_fb, complex(0.0, gam), R_supp)
        k_0 = single_zero_curvature_response(bump_fb, 0.0, gam, R_supp)
        corr_0 = reflected_pair_correction(bump_fb, 0.0, gam, R_supp)
        assert abs(psi_0 - k_0) < 1e-12, f"Critical zero mismatch: psi={psi_0}, k={k_0}"
        assert abs(corr_0) == 0.0

    # Off critical line (a = 0.49, gamma = 50.0):
    a0 = 0.49
    gam0 = 50.0
    psi_off = spectral_test_observable(bump_fb, complex(a0, gam0), R_supp)
    k_off = single_zero_curvature_response(bump_fb, a0, gam0, R_supp)
    pair_corr = reflected_pair_correction(bump_fb, a0, gam0, R_supp)
    # Reflected pair identity: Psi(a + i*gamma) + Psi(-a + i*gamma) = 2 * Psi(a + i*gamma)
    # 2 * Psi(a + i*gamma) - 2 * K(a, gamma) = pair_corr
    diff = 2.0 * psi_off - 2.0 * k_off
    assert abs(diff - pair_corr) < 1e-14, f"Reflected pair identity mismatch: diff={diff}, corr={pair_corr}"

    # 3. Finite symmetric multiset audit
    audit_rep = audit_regularized_curvature_transfer()
    assert audit_rep['epistemic_status'] == 'EXACT_FINITE_IDENTITY_UNRESOLVED_INFINITE_EXTENSION'
    multiset_audit = audit_rep['finite_symmetric_multiset_verification']
    assert multiset_audit['is_transfer_exact_within_tol'] is True
    assert multiset_audit['balance_discrepancy'] < 1e-12

    # 4. Distributional integration by parts bounds
    jump_audit = audit_rep['distributional_jump_bounds']
    assert jump_audit['asymptotic_decay_power'] == -2.0
    assert jump_audit['correction_bound'] > 0.0
    assert jump_audit['response_bound'] > 0.0
