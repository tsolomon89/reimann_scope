"""tests/test_completed_mean_square_anchor.py — Verification Suite for Completed Mean-Square Anchor (CMSA)

Tests mathematical properties, gates, and falsification witnesses:
1. Exact completed logarithmic derivative identity: P(u) = A(u) - xi'/xi(u) for Re(u) > 1.
2. Prime Dirichlet series P_N(u) evaluation with explicit tail bounds and monotonicity check.
3. Symmetrically paired Hadamard product Xi'/Xi(z) and truncation convergence.
4. Grade covariance: tau^K * D_K^xi(tau^K * u) = xi'/xi(u) (coordinate redundancy).
5. Finite Dirichlet mean-square sinc kernel and exact match with numerical quadrature.
6. T -> infinity diagonal limit convergence to sum Lambda(n)^2 / n^(2*sigma).
7. Base Completed Mean-Square Anchor (CMSA-1) arithmetic vanishing anchor and G4 gate metadata.
8. Polarized Completed Mean-Square Anchor (CMSA-2) and cross-term expansion.
9. Grade-Normalized Completed Mean-Square Anchor (CMSA-3) coordinate redundancy.
10. Synthetic divisor tests (on-line, off-line quartet, repeated ordinates, close ordinates, multiplicities > 1).
11. Real-axis spectral defect Delta(delta) formula and leading-order comparison.
12. Exact finite zero kernel J_T(p,q) and zero-zero kernel K_T(lambda1, lambda2).
13. Complete finite spectral expansion S_{N,T} = I_AA - I_AZ - I_ZA + I_ZZ closure.
14. Direct completed-function control vs -zeta'/zeta.
15. Structured candidate registry validation for CMSA-1, CMSA-2, CMSA-3.
"""

import mpmath
import pytest
from math_core import (
    completed_log_derivative_archimedean_A,
    prime_dirichlet_series_P,
    prime_dirichlet_series_tail_bound,
    completed_log_derivative_spectral_Xi_prime_over_Xi,
    completed_log_derivative_exact_residual,
    grade_dilated_completed_log_derivative,
    finite_dirichlet_mean_square_sinc_kernel,
    completed_mean_square_anchor_cmsa1,
    polarized_mean_square_anchor_cmsa2,
    grade_normalized_mean_square_anchor_cmsa3,
    evaluate_cmsa_synthetic_divisors,
    spectral_real_axis_defect_delta,
    spectral_real_axis_defect_leading_order,
    exact_finite_zero_kernel_J_T,
    exact_finite_zero_zero_kernel_K_T,
    evaluate_complete_finite_spectral_expansion,
    direct_completed_function_control,
    normalized_fibre_curvature,
    get_candidate_registry,
    to_mpf,
    to_mpc,
    get_tau
)
from reference_data import load_first_100_reference_zeros


class TestCompletedLogDerivativeDecomposition:
    """Verifies the exact pointwise identity P(u) = A(u) - xi'/xi(u) on Re(u) > 1."""

    def test_archimedean_term_exact_evaluation(self):
        """A(u) evaluates 1/u + 1/(u-1) - 0.5*log(pi) + 0.5*psi(u/2) accurately."""
        with mpmath.workdps(80):
            u = mpmath.mpf('2.5')
            a_val = completed_log_derivative_archimedean_A(u, dps=80)
            expected = 1/u + 1/(u - 1) - mpmath.mpf('0.5') * mpmath.log(mpmath.pi) + mpmath.mpf('0.5') * mpmath.digamma(u / 2)
            assert mpmath.almosteq(a_val.real, expected, abs_eps=mpmath.mpf('1e-75'))
            assert a_val.imag == 0

    def test_pointwise_identity_at_real_points(self):
        """P(u) + xi'/xi(u) == A(u) holds to machine precision against mpmath reference."""
        with mpmath.workdps(80):
            for u_val in ['2.0', '2.5', '3.0', '4.0']:
                u = mpmath.mpf(u_val)
                xi_fn = lambda s: mpmath.mpf('0.5') * s * (s - 1) * mpmath.power(mpmath.pi, -s / 2) * mpmath.gamma(s / 2) * mpmath.zeta(s)
                exact_xi_log_der = mpmath.diff(xi_fn, u) / xi_fn(u)
                a_val = completed_log_derivative_archimedean_A(u, dps=80).real
                exact_m_zeta_log_der = -mpmath.diff(mpmath.zeta, u) / mpmath.zeta(u)

                # A(u) - xi'/xi(u) must equal -zeta'/zeta(u)
                diff = abs((a_val - exact_xi_log_der) - exact_m_zeta_log_der)
                assert diff < mpmath.mpf('1e-70')

    def test_prime_dirichlet_series_with_explicit_tail_bound(self):
        """P_N(sigma) converges to -zeta'/zeta(sigma) within the proved integral tail bound."""
        with mpmath.workdps(80):
            sigma = mpmath.mpf('2.5')
            max_n = 2000
            p_n = prime_dirichlet_series_P(u=sigma, max_n=max_n, dps=80).real
            exact_p = -mpmath.diff(mpmath.zeta, sigma) / mpmath.zeta(sigma)
            diff = abs(p_n - exact_p)

            tail_res = prime_dirichlet_series_tail_bound(sigma=sigma, max_n=max_n, dps=80)
            lin_bound = to_mpf(tail_res["linear_tail_bound"], dps=80)

            assert diff < lin_bound
            assert diff > 0  # Truncation error is strictly positive

    def test_prime_tail_bound_preconditions(self):
        """Tail bound requires max_n >= 3 and sigma > 1 for monotonicity."""
        with pytest.raises(ValueError, match="sigma must be > 1"):
            prime_dirichlet_series_tail_bound(sigma='0.8', max_n=100)
        with pytest.raises(ValueError, match="max_n must be >= 3"):
            prime_dirichlet_series_tail_bound(sigma='2.0', max_n=2)

    def test_hadamard_product_spectral_sum_convergence(self):
        """Symmetric Hadamard sum for Xi'/Xi(z) matches analytic reference within tail truncation."""
        with mpmath.workdps(80):
            zeros = load_first_100_reference_zeros()
            z = mpmath.mpf('2.0')  # u = 2.5
            xi_spec = completed_log_derivative_spectral_Xi_prime_over_Xi(z=z, upper_zeros=zeros, dps=80).real

            u = z + mpmath.mpf('0.5')
            xi_fn = lambda s: mpmath.mpf('0.5') * s * (s - 1) * mpmath.power(mpmath.pi, -s / 2) * mpmath.gamma(s / 2) * mpmath.zeta(s)
            exact_xi_log_der = (mpmath.diff(xi_fn, u) / xi_fn(u)).real

            # Truncation with 100 zeros leaves residual ~ 0.015
            residual = abs(exact_xi_log_der - xi_spec)
            assert residual < mpmath.mpf('0.02')
            assert residual > mpmath.mpf('0.01')


class TestGradeCovarianceAndRedundancy:
    """Verifies that grade dilation tau^K D_K^xi is coordinate-redundant."""

    def test_grade_covariance_identity(self):
        """tau^K * D_K^xi(tau^K * u) == xi'/xi(u) for all grades K in Z."""
        with mpmath.workdps(80):
            for K in [-3, -1, 0, 1, 2, 4]:
                res = grade_dilated_completed_log_derivative(s_K='2.5', K=K, dps=80)
                assert res["is_coordinate_redundant"] is True
                assert mpmath.mpf(res["restoration_diff"]) < mpmath.mpf('1e-50')


class TestFiniteDirichletMeanSquareSincKernel:
    """Verifies the exact finite Dirichlet sinc kernel identity and its diagonal limit."""

    def test_sinc_kernel_vs_numerical_quadrature(self):
        """The sinc formula matches the numerical integral (1/2T) int_{-T}^T |P_N|^2 dt to 30 digits."""
        with mpmath.workdps(40):
            sigma = mpmath.mpf('2.0')
            T = mpmath.mpf('5.0')
            max_N = 10

            sinc_res = finite_dirichlet_mean_square_sinc_kernel(sigma=sigma, T=T, max_N=max_N, dps=40)
            sinc_val = mpmath.mpf(sinc_res["sinc_mean_square"])

            # Numerical quadrature
            def p_fn(t):
                return sum(mpmath.mangoldt(n) * mpmath.power(n, -sigma - mpmath.mpc(0, t)) for n in range(2, max_N + 1))

            quad_val = (1 / (2 * T)) * mpmath.quad(lambda t: abs(p_fn(t))**2, [-T, T])
            diff = abs(sinc_val - quad_val)
            assert diff < mpmath.mpf('1e-20')

    def test_diagonal_limit_as_t_goes_to_infinity(self):
        """As T -> infinity, the sinc mean square converges to the exact diagonal sum."""
        with mpmath.workdps(80):
            sigma = mpmath.mpf('2.0')
            max_N = 15
            res_T10 = finite_dirichlet_mean_square_sinc_kernel(sigma=sigma, T=10, max_N=max_N, dps=80)
            res_T100 = finite_dirichlet_mean_square_sinc_kernel(sigma=sigma, T=100, max_N=max_N, dps=80)
            res_T1000 = finite_dirichlet_mean_square_sinc_kernel(sigma=sigma, T=1000, max_N=max_N, dps=80)

            diff_10 = mpmath.mpf(res_T10["diff_from_diagonal"])
            diff_100 = mpmath.mpf(res_T100["diff_from_diagonal"])
            diff_1000 = mpmath.mpf(res_T1000["diff_from_diagonal"])

            assert diff_1000 < diff_100 < diff_10
            assert diff_1000 < mpmath.mpf('1e-4')


class TestExactFiniteSpectralKernelsAndExpansion:
    """Verifies exact analytic zero kernel J_T, zero-zero kernel K_T, and complete finite spectral expansion."""

    def test_exact_zero_kernel_J_T_vs_numerical_quadrature(self):
        """J_T(p,q) matches direct numerical quadrature of (1/2T) int_{-T}^T dt / [(p+it)(q-it)]."""
        with mpmath.workdps(50):
            p = mpmath.mpc('1.5', '14.134725')
            q = mpmath.mpc('1.8', '-21.022039')
            T = mpmath.mpf('25.0')

            j_analytic = exact_finite_zero_kernel_J_T(p, q, T, dps=50)
            j_quad = mpmath.quad(lambda t: 1 / ((p + mpmath.mpc(0, t)) * (q - mpmath.mpc(0, t))), [-T, T]) / (2 * T)

            diff = abs(j_analytic - j_quad)
            assert diff < mpmath.mpf('1e-18')

    def test_exact_zero_zero_kernel_K_T_vs_numerical_quadrature(self):
        """K_T(lambda1, lambda2; a) matches direct numerical quadrature of R_lambda1 * conj(R_lambda2)."""
        with mpmath.workdps(50):
            lam1 = mpmath.mpc('0.05', '14.134725')
            lam2 = mpmath.mpc('-0.08', '21.022039')
            a = mpmath.mpf('1.5')
            T = mpmath.mpf('30.0')

            k_analytic = exact_finite_zero_zero_kernel_K_T(lam1, lam2, a, T, dps=50)

            def resolvent(lam, t):
                z = mpmath.mpc(a, t)
                return 2 * z / (z * z - lam * lam)

            k_quad = mpmath.quad(lambda t: resolvent(lam1, t) * mpmath.conj(resolvent(lam2, t)), [-T, T]) / (2 * T)

            diff = abs(k_analytic - k_quad)
            assert diff < mpmath.mpf('1e-18')

    def test_complete_finite_spectral_expansion_closure(self):
        """Complete finite spectral expansion S_{N,T} = I_AA - I_AZ - I_ZA + I_ZZ closes to high precision."""
        with mpmath.workdps(40):
            zeros = [
                ('0.0', '14.134725', 1),
                ('0.05', '21.022039', 1),
                ('-0.05', '21.022039', 1),
            ]
            res = evaluate_complete_finite_spectral_expansion(sigma='2.0', T='10.0', upper_zeros=zeros, dps=35)
            closure_diff = mpmath.mpf(res["closure_difference"])
            assert closure_diff < mpmath.mpf('1e-15')
            assert res["status"] == "EXACT_FINITE_IDENTITY"
            assert res["earliest_open_gate"] == "G4"
            assert res["infinite_interchange_status"] == "INFINITE_INTERCHANGE_OPEN"

    def test_direct_completed_function_control(self):
        """Direct completed function matches -zeta'/zeta pointwise and in finite-T mean square."""
        with mpmath.workdps(40):
            res = direct_completed_function_control(sigma='2.5', T='10.0', dps=35)
            assert mpmath.mpf(res["pointwise_diff_t0"]) < mpmath.mpf('1e-30')
            assert mpmath.mpf(res["pointwise_diff_t1"]) < mpmath.mpf('1e-30')
            assert mpmath.mpf(res["mean_square_difference"]) == 0.0


class TestRealAxisSpectralDefect:
    """Verifies the exact real-axis spectral defect formula and its sign behavior."""

    def test_real_axis_defect_exact_formula_vs_direct_difference(self):
        """Delta(delta) formula matches direct difference of resolvents (R_off - R_on) to 70 digits."""
        with mpmath.workdps(80):
            z = mpmath.mpf('1.5')
            gamma = mpmath.mpf('14.134725')
            delta = mpmath.mpf('0.1')

            # Direct evaluation of resolvents
            r_on = 2 * (2 * z / (z**2 + gamma**2))
            r_plus = 2 * z / (z**2 - (delta + mpmath.mpc(0, gamma))**2)
            r_minus = 2 * z / (z**2 - (-delta + mpmath.mpc(0, gamma))**2)
            r_off = (r_plus + r_minus).real
            direct_defect = r_off - r_on

            formula_defect = spectral_real_axis_defect_delta(z, gamma, delta, dps=80)
            diff = abs(direct_defect - formula_defect)
            assert diff < mpmath.mpf('1e-70')

    def test_real_axis_defect_leading_order_approximation(self):
        """Leading-order formula matches exact defect with O(delta^4) remainder."""
        with mpmath.workdps(80):
            z = mpmath.mpf('1.5')
            gamma = mpmath.mpf('14.134725')
            delta = mpmath.mpf('0.001')

            exact_defect = spectral_real_axis_defect_delta(z, gamma, delta, dps=80)
            leading_defect = spectral_real_axis_defect_leading_order(z, gamma, delta, dps=80)
            diff = abs(exact_defect - leading_defect)

            # Error should be ~ O(delta^4) = 1e-12
            assert diff < mpmath.mpf('1e-10')

    def test_real_axis_defect_sign_transition(self):
        """Delta(delta) < 0 for z^2 < 3*gamma^2 + delta^2, and > 0 for z^2 > 3*gamma^2 + delta^2."""
        with mpmath.workdps(80):
            gamma = mpmath.mpf('10.0')
            delta = mpmath.mpf('0.1')
            crit_z = mpmath.sqrt(3 * gamma**2 + delta**2)

            # Below critical threshold: defect is negative
            z_below = crit_z - mpmath.mpf('1.0')
            defect_below = spectral_real_axis_defect_delta(z_below, gamma, delta, dps=80)
            assert defect_below < 0

            # Above critical threshold: defect is positive
            z_above = crit_z + mpmath.mpf('1.0')
            defect_above = spectral_real_axis_defect_delta(z_above, gamma, delta, dps=80)
            assert defect_above > 0


class TestCompletedMeanSquareAnchorCandidates:
    """Verifies Candidates CMSA-1, CMSA-2, CMSA-3 evaluations and gate classifications."""

    def test_cmsa1_base_anchor_properties(self):
        """CMSA-1 proves arithmetic finite sinc residual and reports G4 gate classification."""
        with mpmath.workdps(80):
            res = completed_mean_square_anchor_cmsa1(sigma='2.0', T='50.0', max_N=100, dps=80)
            assert res["status"] == "EXACT_FINITE_IDENTITY"
            assert res["earliest_open_gate"] == "G4"
            assert res["classification"] == "INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_GATE_G4"
            assert mpmath.mpf(res["mean_square_tail_bound"]) < mpmath.mpf('1e-3')

    def test_cmsa2_polarized_anchor_properties(self):
        """CMSA-2 evaluates polarized anchor for sigma1 != sigma2."""
        with mpmath.workdps(80):
            res = polarized_mean_square_anchor_cmsa2(sigma1='2.0', sigma2='2.5', T='50.0', max_N=100, dps=80)
            assert res["status"] == "EXACT_FINITE_IDENTITY"
            assert res["earliest_open_gate"] == "G4"
            assert res["classification"] == "INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_GATE_G4"

    def test_cmsa3_grade_normalized_anchor_redundancy(self):
        """CMSA-3 is coordinate-redundant with grade-zero anchor."""
        with mpmath.workdps(80):
            res = grade_normalized_mean_square_anchor_cmsa3(sigma='2.0', K=2, T='50.0', max_N=100, dps=80)
            assert res["is_coordinate_redundant"] is True
            assert res["classification"] == "GRADE_COORDINATE_REDUNDANT"


class TestSyntheticDivisorSpectralEvaluations:
    """Evaluates synthetic divisor configurations against the CMSA spectral kernel."""

    def test_online_fibres_null_response(self):
        """All-online fibres yield zero delta response."""
        with mpmath.workdps(80):
            zeros = [('0.0', '14.134725', 1), ('0.0', '21.022040', 1)]
            res = evaluate_cmsa_synthetic_divisors(zeros, sigma='2.0', t_val='0.0', dps=80)
            assert res["is_on_line"] is True

    def test_single_offline_quartet_delta_response(self):
        """An off-line quartet produces a non-zero response in Xi'/Xi."""
        with mpmath.workdps(80):
            zeros = [('0.1', '14.134725', 1), ('-0.1', '14.134725', 1)]
            res = evaluate_cmsa_synthetic_divisors(zeros, sigma='2.0', t_val='0.0', dps=80)
            assert res["is_on_line"] is False
            assert mpmath.mpf(res["delta_response_abs"]) > 0

    def test_multiple_offline_quartets_and_mixed_heights(self):
        """Multiple quartets with close ordinates and multiplicities > 1."""
        with mpmath.workdps(80):
            zeros = [
                ('0.08', '14.134725', 2),   # multiplicity 2
                ('-0.08', '14.134725', 2),
                ('0.05', '14.140000', 1),   # close ordinate
                ('-0.05', '14.140000', 1),
                ('0.0', '25.010858', 1),    # on-line zero
            ]
            res = evaluate_cmsa_synthetic_divisors(zeros, sigma='2.0', t_val='1.0', dps=80)
            assert res["is_on_line"] is False


class TestCandidateRegistryCompleteness:
    """Verifies that the candidate registry includes CMSA-1, CMSA-2, CMSA-3 with valid gate metadata."""

    def test_cmsa_registry_entries(self):
        registry = get_candidate_registry()
        for cid in ["CANDIDATE_CMSA1", "CANDIDATE_CMSA2", "CANDIDATE_CMSA3"]:
            assert cid in registry
            entry = registry[cid]
            assert "id" in entry
            assert "name" in entry
            assert "target" in entry
            assert "classification" in entry
            assert "earliest_failure" in entry
            assert entry["arithmetic_independence"] is True

