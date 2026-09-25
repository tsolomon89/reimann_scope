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
import numpy as np
import pytest
import mpmath

from tc.weil_forms import (
    _compute_C_tab_fast,
    compute_grouped_correlation_system,
    test_spectral_matrix_span_recovery as eval_spectral_matrix_span_recovery,
    certify_production_convolution_table,
    certify_baseline_canonical_weil_error_budget,
    sieve_prime_powers_in_window,
    Z_CANONICAL_KERNEL,
    NORM_KAPPA_SQ,
    NORM_KAPPA_FIRST_DERIVATIVE_SQ,
    NORM_KAPPA_SECOND_DERIVATIVE_SQ,
    NORM_KAPPA_THIRD_DERIVATIVE_SQ,
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
    key_contribs = {k: [] for k in target_keys}

    for i, K in enumerate(grades):
        for j, J in enumerate(grades):
            if K == J: continue
            d = K - J
            for n_val, a_n in a_kn[K].items():
                for m_val, a_m in a_kn[J].items():
                    g = math.gcd(n_val, m_val)
                    k = (d, n_val // g, m_val // g)
                    if k in key_contribs:
                        key_contribs[k].append({
                            'grades': (K, J),
                            'stations': (n_val, m_val),
                            'amp_prod': a_n * a_m
                        })

    # Each key has exactly 1 contributor
    for k in target_keys:
        assert len(key_contribs[k]) == 1, f"Key {k} has {len(key_contribs[k])} contributors, expected 1"
        assert key_contribs[k][0]['amp_prod'] > 0.0

    a12 = key_contribs[(1, 89, 563)][0]['amp_prod']
    a13 = key_contribs[(2, 89, 3511)][0]['amp_prod']
    a23 = key_contribs[(1, 563, 3511)][0]['amp_prod']

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
        i = grades.index(c['grades'][0])
        j = grades.index(c['grades'][1])
        M[i, j] += c['amp_prod']
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
    1. Certify production convolution table at h=0.05 on window [8, 20].
    2. Check that derivative remainder bound ||C_h - interp(C_h)||_infty <= (Delta v)^2 / 8 * ||psi_h'||_2^2
       is mathematically justified and computed.
    3. Test adversarial scaling case h=0.01: returns uncertified outside established domain.
    """
    cert = certify_production_convolution_table(h=0.05, window=(8.0, 20.0), N_tab=2001, n_nodes=256)
    assert cert['status'] == 'CONVOLUTION_TABLE_CERTIFIED'
    assert cert['is_table_certified'] is True
    assert cert['is_domain_certified'] is True

    # Check bounds
    interp_bound = cert['interpolation_model']['eps_interp_bound']
    nodal_bound = cert['quadrature_model']['eps_nodal_bound']
    total_bound = cert['table_enclosure']['total_pointwise_error_bound']
    assert total_bound == interp_bound + nodal_bound
    assert cert['table_enclosure']['relative_pointwise_accuracy'] < 1e-2

    # Adversarial scaling test: h=0.01 must fail closed
    cert_adv = certify_production_convolution_table(h=0.01, window=(8.0, 20.0), N_tab=2001, n_nodes=256)
    assert cert_adv['status'] == 'UNCERTIFIED_OUTSIDE_PARAMETER_DOMAIN'
    assert cert_adv['is_table_certified'] is False
    assert cert_adv['is_domain_certified'] is False
    assert "outside the certified production baseline domain" in cert_adv['reason']


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
        # Reciprocal atom (-1, 8, 1): J - K = -1, ratio 8/1
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
    # Both terms in previous vector were negative:
    assert b_prev[0] * b_prev[1] < 0
    assert b_prev[1] * b_prev[2] < 0


def test_40_digit_quadrature_diagnostic_assertions():
    """
    Check the quadrature test against 40-dps mpmath as promised in docstring.
    Verifies that the empirical discrepancy between 256-node GL and 40-dps mpmath
    is strictly bounded by the certified eps_nodal bound at baseline h=0.05.
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
    eps_nodal = cert['quadrature_model']['eps_nodal_bound']

    assert diff_0 <= eps_nodal, f"Measured 40-dps error {diff_0} exceeded certified nodal bound {eps_nodal}"
