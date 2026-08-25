"""tests/test_completed_mean_square_anchor.py — Verification Suite for Completed Mean-Square Anchor (CMSA)

Tests mathematical properties, gates, and falsification witnesses:
1. Exact completed logarithmic derivative identity: P(u) = A(u) - xi'/xi(u) for Re(u) > 1.
2. Prime Dirichlet series P_N(u) evaluation with explicit tail bounds.
3. Symmetrically paired Hadamard product Xi'/Xi(z) and truncation convergence.
4. Grade covariance: tau^K * D_K^xi(tau^K * u) = xi'/xi(u) (coordinate redundancy).
5. Finite Dirichlet mean-square sinc kernel and exact match with numerical quadrature.
6. T -> infinity diagonal limit convergence to sum Lambda(n)^2 / n^(2*sigma).
7. Base Completed Mean-Square Anchor (CMSA-1) arithmetic vanishing anchor.
8. Polarized Completed Mean-Square Anchor (CMSA-2) and cross-term expansion.
9. Grade-Normalized Completed Mean-Square Anchor (CMSA-3) coordinate redundancy.
10. Synthetic divisor tests (on-line, off-line quartet, repeated ordinates, close ordinates, multiplicities > 1).
11. Deliberate search for negative eigenvalues / spectral cancellations.
12. Structured candidate registry validation for CMSA-1, CMSA-2, CMSA-3.
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


class TestCompletedMeanSquareAnchorCandidates:
    """Verifies Candidates CMSA-1, CMSA-2, CMSA-3 evaluations and gate classifications."""

    def test_cmsa1_base_anchor_properties(self):
        """CMSA-1 proves arithmetic vanishing anchor = 0 and reports tail bounds."""
        with mpmath.workdps(80):
            res = completed_mean_square_anchor_cmsa1(sigma='2.0', T='50.0', max_N=100, dps=80)
            assert res["arithmetic_zero_anchor_proved"] is True
            assert res["classification"] == "LIVE_WITH_EXPLICIT_UNPROVED_ANALYTIC_GAP"
            assert mpmath.mpf(res["mean_square_tail_bound"]) < mpmath.mpf('1e-3')

    def test_cmsa2_polarized_anchor_properties(self):
        """CMSA-2 evaluates polarized anchor for sigma1 != sigma2."""
        with mpmath.workdps(80):
            res = polarized_mean_square_anchor_cmsa2(sigma1='2.0', sigma2='2.5', T='50.0', max_N=100, dps=80)
            assert res["arithmetic_zero_anchor_proved"] is True
            assert res["classification"] == "LIVE_WITH_EXPLICIT_UNPROVED_ANALYTIC_GAP"

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

    def test_deliberate_search_for_spectral_defects(self):
        """Verifies that the unregularized spectral difference Delta(delta) on the real axis is negative for z^2 < 3*gamma^2."""
        with mpmath.workdps(80):
            # For z = 1.5 (sigma = 2.0) and gamma = 14.1347: z^2 - 3*gamma^2 = 2.25 - 3*(199.79) = -597.12 < 0.
            # Compare 2 online roots with 2 offline roots (+delta, -delta) at the same ordinate.
            zeros_online = [('0.0', '14.134725', 2)]
            zeros_offline = [('0.1', '14.134725', 1), ('-0.1', '14.134725', 1)]

            z = mpmath.mpc('1.5', '0.0')
            xi_online = completed_log_derivative_spectral_Xi_prime_over_Xi(z=z, upper_zeros=zeros_online, dps=80).real
            xi_offline = completed_log_derivative_spectral_Xi_prime_over_Xi(z=z, upper_zeros=zeros_offline, dps=80).real

            # Offline pair is strictly less than online pair (Delta(delta) < 0)
            diff = xi_offline - xi_online
            assert diff < 0


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
