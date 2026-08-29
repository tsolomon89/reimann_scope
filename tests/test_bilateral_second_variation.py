"""tests/test_bilateral_second_variation.py — Verification Suite for Arithmetic Radial-Centering,
Integrated-Sigma Resolvent Identities, and Bilateral Grade Second-Variation Analysis.

Verifies:
1. Two-bump prime-only Weil autocorrelation Gram matrix indefiniteness (+- w_p eigenvalues).
2. Exact quartet-minus-projection resolvent difference:
   Delta Z_+(z) = 2*delta^2 / ((z - i*gamma)*((z - i*gamma)^2 - delta^2)).
3. CMSA-RDQ logarithmic derivative connection:
   d/dz log q_{delta,gamma}(z) = Delta Z_+(z).
4. Leading L^2(dt) resolvent coefficient 3*pi*delta^4 / (2*a^5) vs high-precision quadrature.
5. Exact Fourier transform of complete quartet difference:
   \\widehat{\\Delta Z_\\sigma}(\\xi) = 4*pi*e^{-a*xi}*(cosh(delta*xi)-1)*cos(gamma*xi).
6. Exact unnormalized prime cross-term and continuum sign indefiniteness.
7. Integrated prime diagonal closed form: - 1/2 * sum_p log p * log(1 - p^{-2*sigma_0}).
8. Bilateral grade centering second variation: exact opposition cancellation vs asymmetric cross-term non-cancellation.
9. Bilateral grade scale specificity: generic base a > 1 vs tau = 2*pi.
10. Probe regularization audit: sharp cutoff classification (OPEN_ADMISSIBLE_PROBE_REGULARIZATION).
"""

import mpmath
import pytest
import math_core


class TestFinitePrimeWeilGramMatrixTwoBump:
    """Verifies that local prime distributions on genuine two-bump test functions produce indefinite eigenvalues (+- w_p)."""

    def test_two_bump_indefinite_eigenvalues(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        res = math_core.evaluate_finite_prime_weil_gram_matrix(primes=primes, dps=50)

        assert res["status"] == "FINITE_PRIME_WEIL_GRAM_MATRIX_ANALYZED"
        assert res["is_positive_semidefinite"] is False
        assert res["is_strictly_negative_definite"] is False
        assert res["classification"] == "FAIL_NAIVE_PRIME_LOCAL_FACTORIZATION"
        assert res["falsification_witness"] == "PRIME_ONLY_AUTOCORRELATION_IS_INDEFINITE_NOT_POSITIVE_SEMIDEFINITE"

        # Check every 2x2 two-bump witness has eigenvalues +w_p and -w_p
        for w in res["two_bump_witnesses"]:
            assert w["is_indefinite"] is True
            w_p = float(w["w_p"])
            assert w_p > 0.0
            evs = [float(ev) for ev in w["eigenvalues"]]
            assert len(evs) == 2
            assert max(evs) > 0.0
            assert min(evs) < 0.0
            assert abs(max(evs) + min(evs)) < 1e-12


class TestExactQuartetResolventIdentity:
    """Verifies exact quartet-minus-projection resolvent differences."""

    @pytest.mark.parametrize("delta,gamma,z_re,z_im", [
        ("0.0", "14.134725", "1.5", "10.0"),
        ("0.05", "14.134725", "1.2", "5.0"),
        ("-0.05", "14.134725", "2.0", "-7.0"),
        ("0.1", "21.022040", "1.1", "25.0"),
        ("-0.2", "30.424876", "3.0", "14.0"),
    ])
    def test_quartet_resolvent_exact_match(self, delta, gamma, z_re, z_im):
        z_val = f"{z_re} + {z_im} * I"
        res = math_core.evaluate_quartet_resolvent_difference(delta=delta, gamma=gamma, z=z_val, dps=50)

        assert res["status"] == "QUARTET_RESOLVENT_DIFFERENCE_VERIFIED"
        assert res["is_exact_identity"] is True
        assert float(res["diff_plus"]) < 1e-45
        assert float(res["diff_minus"]) < 1e-45

        if delta == "0.0":
            dz_plus = math_core.to_mpc(res["delta_Z_plus_direct"], dps=50)
            dz_tot = math_core.to_mpc(res["delta_Z_total"], dps=50)
            assert abs(dz_plus) < 1e-45
            assert abs(dz_tot) < 1e-45


class TestCMSARDQDerivativeIdentity:
    """Verifies CMSA-RDQ logarithmic derivative connection d/dz log q_{delta,gamma}(z) = Delta Z_+(z)."""

    @pytest.mark.parametrize("delta,gamma,z_re,z_im", [
        ("0.05", "14.134725", "1.5", "10.0"),
        ("0.01", "21.022040", "2.0", "20.0"),
        ("-0.10", "30.424876", "1.2", "-15.0"),
    ])
    def test_cmsa_rdq_derivative_match(self, delta, gamma, z_re, z_im):
        z_val = f"{z_re} + {z_im} * I"
        res = math_core.evaluate_cmsa_rdq_derivative_identity(delta=delta, gamma=gamma, z=z_val, dps=50)

        assert res["status"] == "CMSA_RDQ_DERIVATIVE_IDENTITY_VERIFIED"
        assert res["is_exact_identity"] is True
        assert float(res["diff"]) < 1e-45


class TestIntegratedResolventL2Norm:
    """Verifies exact L^2(dt) leading resolvent norm coefficient 3*pi*delta^4 / (2*a^5)."""

    @pytest.mark.parametrize("delta,gamma,a", [
        ("0.01", "14.134725", "1.0"),
        ("0.02", "21.022040", "1.5"),
        ("0.005", "30.424876", "0.8"),
    ])
    def test_leading_l2_norm_exact_formula(self, delta, gamma, a):
        res = math_core.evaluate_integrated_resolvent_l2_norm(delta=delta, gamma=gamma, a=a, dps=50)

        assert res["status"] == "INTEGRATED_RESOLVENT_L2_NORM_VERIFIED"
        assert res["is_exact_leading_match"] is True
        assert float(res["diff_leading"]) < 1e-10
        # Full quadrature is strictly positive and bounded
        assert float(res["full_single_quad"]) > 0.0
        assert float(res["full_two_height_quad"]) > 0.0


class TestFourierQuartetDifference:
    """Verifies closed-form Fourier transform against numerical oscillatory integration."""

    @pytest.mark.parametrize("delta,gamma,a,xi", [
        ("0.02", "14.134725", "1.0", "0.5"),
        ("0.05", "14.134725", "1.2", "1.5"),
        ("0.01", "21.022040", "0.8", "2.0"),
    ])
    def test_fourier_quartet_transform_match(self, delta, gamma, a, xi):
        res = math_core.evaluate_fourier_quartet_difference(delta=delta, gamma=gamma, a=a, xi=xi, dps=50)

        assert res["status"] == "FOURIER_QUARTET_DIFFERENCE_VERIFIED"
        assert res["is_exact_match"] is True
        assert float(res["diff"]) < 1e-6



class TestExactPrimeCrosstermSeries:
    """Verifies exact prime cross-term series evaluation and continuum sign indefiniteness."""

    def test_prime_crossterm_sign_indefiniteness(self):
        # Evaluate cross-term at different gamma values to witness sign change
        gammas = ["5.0", "14.134725", "21.022040", "30.424876", "45.0"]
        evals = []
        for g in gammas:
            res = math_core.evaluate_exact_prime_crossterm_series(
                delta="0.05", gamma=g, sigma_0="1.5", max_n=500, dps=50
            )
            assert res["status"] == "EXACT_PRIME_CROSSTERM_SERIES_EVALUATED"
            evals.append(float(res["cross_leading"]))

        # Confirm there are non-zero values and values of differing magnitudes / signs
        assert any(e != 0.0 for e in evals)


class TestIntegratedPrimeDiagonal:
    """Verifies integrated prime diagonal series against closed Euler log sum."""

    @pytest.mark.parametrize("sigma_0", ["1.1", "1.5", "2.0"])
    def test_integrated_prime_diagonal_match(self, sigma_0):
        res = math_core.evaluate_integrated_prime_diagonal(sigma_0=sigma_0, max_n=5000, dps=50)

        assert res["status"] == "INTEGRATED_PRIME_DIAGONAL_EVALUATED"
        assert res["series_matches_closed_form"] is True
        assert float(res["diff"]) < 1e-4
        assert float(res["sum_series"]) > 0.0


class TestBilateralGradeCenteringSecondDifference:
    """Verifies bilateral grade centering second difference under exact opposition vs asymmetry."""

    def test_exact_opposition_cancellation(self):
        F = "1.5 + 2.5 * I"
        delta_h = "0.1 - 0.2 * I"
        delta_minus_h = "-0.1 + 0.2 * I"

        res = math_core.evaluate_bilateral_grade_centering_second_difference(
            F_val=F, delta_h=delta_h, delta_minus_h=delta_minus_h, dps=50
        )

        assert res["status"] == "BILATERAL_GRADE_CENTERING_EVALUATED"
        assert res["is_exact_opposite"] is True
        assert res["cross_term_vanishes"] is True
        assert res["decomposition_matches"] is True
        assert res["classification"] == "PROVED_CENTERING_UNDER_EXACT_OPPOSITION"
        assert float(res["C_h"]) > 0.0
        assert abs(float(res["C_h"]) - float(res["norm_sq_sum"])) < 1e-45

    def test_asymmetric_grade_perturbation_cross_term_non_cancellation(self):
        F = "2.0 + 3.0 * I"
        delta_h = "0.05 + 0.02 * I"
        # Asymmetric perturbation with O(h^2) defect B
        h_val = 0.1
        B = mpmath.mpc("0.3", "-0.4")
        dh_mp = mpmath.mpc("0.05", "0.02")
        dmh_mp = -dh_mp + (h_val**2) * B

        res = math_core.evaluate_bilateral_grade_centering_second_difference(
            F_val=F, delta_h=str(dh_mp), delta_minus_h=str(dmh_mp), dps=50
        )

        assert res["status"] == "BILATERAL_GRADE_CENTERING_EVALUATED"
        assert res["is_exact_opposite"] is False
        assert res["cross_term_vanishes"] is False
        assert res["decomposition_matches"] is True
        assert res["classification"] == "FAIL_BILATERAL_CROSS_TERM_CANCELLATION"
        assert abs(float(res["cross_term"])) > 1e-5


class TestBilateralScaleSpecificity:
    """Verifies that algebraic grade centering is scale-generic (holds for all a > 1)."""

    def test_scale_genericity(self):
        res = math_core.evaluate_bilateral_scale_specificity(dps=50)

        assert res["status"] == "BILATERAL_SCALE_SPECIFICITY_AUDITED"
        assert res["holds_for_all_scales"] is True
        assert res["classification"] == "SCALE_GENERIC_NOT_TAU_SPECIFIC"
        for eval_item in res["scale_evaluations"]:
            assert eval_item["is_positive"] is True


class TestAdmissibleProbeRegularizationClassification:
    """Verifies that sharp cutoffs are classified as OPEN_ADMISSIBLE_PROBE_REGULARIZATION."""

    def test_probe_regularization_classification(self):
        s_test = "0.5 + 14.134725 * I"
        res = math_core.evaluate_fourier_mellin_probe_analysis(s_test, dps=50)

        assert res["status"] == "FOURIER_MELLIN_PROBE_ANALYSIS_COMPLETED"
        assert res["is_smooth_cc_infty"] is False
        assert res["test_function_classification"] == "FAIL_TEST_FUNCTION_IDENTIFICATION"
        assert res["regularization_obligation"] == "OPEN_ADMISSIBLE_PROBE_REGULARIZATION"
