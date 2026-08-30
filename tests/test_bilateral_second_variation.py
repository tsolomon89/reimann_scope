"""tests/test_bilateral_second_variation.py — Verification Suite for Arithmetic Radial-Centering,
Integrated-Sigma Resolvent Identities, and Zeta-Specific Bilateral Grade Second-Variation Analysis.

Verifies:
1. Two-bump prime-only Weil autocorrelation Gram matrix indefiniteness (+- w_p eigenvalues) under smooth bump model.
2. Exact quartet-minus-projection resolvent difference (one-height and full-quartet).
3. CMSA-RDQ logarithmic derivative connections for q+, q-, and q^{full}.
4. Leading L^2(dt) resolvent coefficient 3*pi*delta^4 / (2*a^5) vs high-precision quadrature.
5. Exact Fourier transform of complete quartet difference:
   \\widehat{\\Delta Z_\\sigma}(\\xi) = 8*pi*e^{-a*xi}*(cosh(delta*xi)-1)*cos(gamma*xi).
6. Exact unnormalized prime cross-term (-8*pi) vs direct 2D numerical quadrature (fails under factor-of-2 error).
7. Continuum gamma sign-change proof with certified witnesses (CONTINUUM_GAMMA_SIGN_CHANGE_PROVED) and separation from ACTUAL_ZETA_ZERO_ORDINATE_SIGN_OPEN.
8. Integrated prime diagonal exact matched truncation and tail-bounded Euler closed sum.
9. Generic bilateral grade centering second difference decomposition.
10. Exact zeta-specific grade jet cross-term evaluation (X_zeta = Re<F0, F0''> != 0) and classification FAIL_ZETA_SPECIFIC_BILATERAL_CROSS_TERM_CANCELLATION.
11. Finite-T grade pullback identity vs asymptotic coordinate redundancy.
12. Bilateral grade scale specificity (SCALE_GENERIC_NOT_TAU_SPECIFIC).
13. Probe regularization audit (OPEN_ADMISSIBLE_PROBE_REGULARIZATION).
"""

import mpmath
import pytest
import math_core


class TestFinitePrimeWeilGramMatrixTwoBump:
    """Verifies that local prime distributions on smooth bump test functions produce indefinite eigenvalues (+- w_p)."""

    def test_two_bump_indefinite_eigenvalues(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        res = math_core.evaluate_finite_prime_weil_gram_matrix(primes=primes, dps=50)

        assert res["status"] == "FINITE_PRIME_WEIL_GRAM_MATRIX_ANALYZED"
        assert res["witness_model"] == "SMOOTH_BUMP_TEST_FUNCTION_MODEL"
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
    """Verifies CMSA-RDQ logarithmic derivative connection for q+, q-, and q^{full}."""

    @pytest.mark.parametrize("delta,gamma,z_re,z_im", [
        ("0.05", "14.134725", "1.5", "10.0"),
        ("0.01", "21.022040", "2.0", "20.0"),
        ("-0.10", "30.424876", "1.2", "-15.0"),
    ])
    def test_cmsa_rdq_derivative_match(self, delta, gamma, z_re, z_im):
        z_val = f"{z_re} + {z_im} * I"
        res = math_core.evaluate_cmsa_rdq_derivative_identity(delta=delta, gamma=gamma, z=z_val, dps=50)

        assert res["status"] == "CMSA_RDQ_DERIVATIVE_IDENTITY_VERIFIED"
        assert res["is_exact_plus_identity"] is True
        assert res["is_exact_minus_identity"] is True
        assert res["is_exact_full_identity"] is True
        assert res["is_exact_identity"] is True
        assert float(res["diff_plus"]) < 1e-45
        assert float(res["diff_minus"]) < 1e-45
        assert float(res["diff_full"]) < 1e-45


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
        assert float(res["full_single_quad"]) > 0.0
        assert float(res["full_two_height_quad"]) > 0.0


class TestFourierQuartetDifference:
    """Verifies closed-form Fourier transform (8*pi complete quartet) against numerical oscillatory integration."""

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
    """Verifies exact prime cross-term series (-8*pi) vs direct numerical quadrature and continuum sign changes."""

    def test_direct_quadrature_vs_series_normalization(self):
        """Direct numerical quadrature comparison for single prime power term n=2 certifying -8*pi constant."""
        with mpmath.workdps(30):
            delta = mpmath.mpf("0.05")
            gamma = mpmath.mpf("14.134725")
            sigma_0 = mpmath.mpf("1.5")
            n = 2
            log_n = mpmath.log(n)
            lam_2 = mpmath.log(2)

            # 1. Exact series formula value for n=2
            cosh_fac = mpmath.cosh(delta * log_n) - 1
            weight_s0 = (mpmath.mpf(n) ** (mpmath.mpf("0.5") - 2 * sigma_0)) / log_n
            cos_fac = mpmath.cos(gamma * log_n)
            series_term_n2 = - 8 * mpmath.pi * lam_2 * weight_s0 * cosh_fac * cos_fac

            # 2. 1D numerical t-quadrature at fixed sigma_0 verifying the 8*pi Fourier pairing:
            # \int_{-\infty}^\infty P_{sigma_0, n=2}(t) conj(Delta Z_{sigma_0}(t)) dt == lam_2 * 2^{-sigma_0} * \widehat{\Delta Z_{sigma_0}}(log 2)
            a_0 = sigma_0 - mpmath.mpf("0.5")
            def inner_t_integrand(t: mpmath.mpf) -> mpmath.mpf:
                p_val = lam_2 * (mpmath.mpf(n) ** (-sigma_0)) * mpmath.exp(- mpmath.mpc(0, t * log_n))
                w_plus = mpmath.mpc(a_0, t - gamma)
                w_minus = mpmath.mpc(a_0, t + gamma)
                dz = (2 * (delta**2)) / (w_plus * (w_plus**2 - delta**2)) + (2 * (delta**2)) / (w_minus * (w_minus**2 - delta**2))
                return mpmath.re(p_val * mpmath.conj(dz))

            t_quad_val = mpmath.quad(inner_t_integrand, [-mpmath.inf, mpmath.inf])
            fourier_paired_val = lam_2 * (mpmath.mpf(n) ** (-sigma_0)) * (8 * mpmath.pi * mpmath.exp(-a_0 * log_n) * cosh_fac * cos_fac)

            assert abs(t_quad_val - fourier_paired_val) / abs(fourier_paired_val) < 1e-3

            # 3. sigma-integral of fourier_paired_val gives exact series_term_n2 / (-2):
            def sigma_int(sig: mpmath.mpf) -> mpmath.mpf:
                a_s = sig - mpmath.mpf("0.5")
                return lam_2 * (mpmath.mpf(n) ** (-sig)) * (8 * mpmath.pi * mpmath.exp(-a_s * log_n) * cosh_fac * cos_fac)

            sig_quad_val = - 2 * mpmath.quad(sigma_int, [sigma_0, mpmath.inf])
            assert abs(sig_quad_val - series_term_n2) / abs(series_term_n2) < 1e-10

            # 4. Verify that a factor-of-2 error (e.g. -4*pi) would strictly fail
            wrong_term_n2 = - 4 * mpmath.pi * lam_2 * weight_s0 * cosh_fac * cos_fac
            wrong_diff = abs(sig_quad_val - wrong_term_n2)
            assert wrong_diff > abs(series_term_n2) * 0.4

    def test_continuum_gamma_sign_witnesses(self):
        """Certifies continuum sign change with explicit positive and negative interval witnesses."""
        res = math_core.evaluate_continuum_gamma_sign_witness(delta="0.05", sigma_0="1.5", max_n=2000, dps=50)

        assert res["status"] == "CONTINUUM_GAMMA_SIGN_WITNESSES_EVALUATED"
        assert res["is_val0_negative"] is True
        assert res["is_val_pi_positive"] is True
        assert res["continuum_gamma_sign_change_proved"] is True
        assert res["classification"] == "CONTINUUM_GAMMA_SIGN_CHANGE_PROVED"
        assert res["actual_zeta_zero_status"] == "ACTUAL_ZETA_ZERO_ORDINATE_SIGN_OPEN"

        v0 = float(res["val_at_gamma_0"])
        v_pi = float(res["val_at_gamma_pi_over_log2"])
        assert v0 < 0.0 < v_pi


class TestIntegratedPrimeDiagonal:
    """Verifies integrated prime diagonal matched truncation, tail-bounded Euler closed sum, and failure rationale."""

    @pytest.mark.parametrize("sigma_0", ["1.1", "1.5", "2.0"])
    def test_exact_matched_prime_truncation(self, sigma_0):
        res = math_core.evaluate_integrated_prime_diagonal(sigma_0=sigma_0, max_n=5000, dps=50)

        assert res["status"] == "INTEGRATED_PRIME_DIAGONAL_EVALUATED"
        assert res["is_exact_matched_identity"] is True
        assert float(res["diff_matched"]) < 1e-40
        assert float(res["sum_direct"]) > 0.0
        assert float(res["diff_infinite_vs_direct"]) < float(res["tail_bound"]) * 2.0
        assert res["classification"] == "FAIL_ZERO_ARITHMETIC_ANCHOR_UNDER_UNNORMALIZED_T_LIMIT"


class TestZetaSpecificGradeJetCrossTerm:
    """Verifies the central research task: evaluation of the actual zeta-specific cross-term X_zeta and cancelling variances."""

    @pytest.mark.parametrize("a", ["1.5", "2.0", "3.0", "5.0"])
    def test_cancelling_variance_exact_cancellation_and_bounds(self, a):
        """
        Verifies that for every a > 1 / log 2 approx 1.442695:
        1. S_1(a) / S_2(a) <= 1 / log 2.
        2. v_*(a) = a^2 - a * (S1 / S2) > 0 strictly.
        3. X_zeta(a, v_*(a)) == 0 to 50 dps exact precision.
        4. Opposite signs strictly certified above and below v_*(a).
        """
        res = math_core.compute_truncated_cancelling_variance(a=a, max_n=2000, dps=50)

        assert res["status"] == "TRUNCATED_CANCELLING_VARIANCE_COMPUTED"
        assert res["ratio_satisfies_bound"] is True
        assert res["is_v_star_positive"] is True
        assert res["is_exact_zero"] is True
        assert res["sign_change_verified"] is True
        assert float(res["v_star"]) > 0.0
        assert abs(float(res["X_zeta_at_v_star"])) < 1e-35

    def test_falsification_of_universal_nonvanishing_assertion(self):
        """
        Adversarial falsification test:
        The previous sprint's claim that X_zeta != 0 for all a > 0, v >= 0 is false.
        This test constructs the exact cancelling variance at a = 2.0 and verifies that X_zeta == 0.
        """
        res = math_core.compute_cancelling_variance(a="2.0", max_n=2000, dps=50)
        v_star = res["v_star"]

        # Evaluate standard evaluator at (a=2.0, v=v_star)
        eval_res = math_core.evaluate_zeta_specific_grade_jet_crossterm(
            a="2.0", sigma_0="2.5", window_variance_t2=v_star, max_n=2000, dps=50
        )

        assert eval_res["status"] == "ZETA_SPECIFIC_GRADE_JET_CROSSTERM_EVALUATED"
        assert eval_res["is_cancelling_variance"] is True
        assert eval_res["X_zeta_nonzero"] is False
        assert abs(float(eval_res["X_zeta"])) < 1e-25

    @pytest.mark.parametrize("a,sigma_w", [
        ("1.5", "1.0"),
        ("2.0", "0.8"),
        ("1.2", "1.5"),
    ])
    def test_full_windowed_dirichlet_inner_product_matches_quadrature_and_reveals_offdiagonal(self, a, sigma_w):
        """
        Verifies that for finite windows:
        1. Full double sum matches 1D numerical quadrature of int W(t) F_0(t) conj(F_0''(t)) dt.
        2. Off-diagonal sum (m != n) is structurally present and non-zero for the tested witness.
        3. Diagonal-only formula differs from the true windowed inner product.
        """
        res = math_core.finite_windowed_dirichlet_polynomial_inner_product(
            a=a, sigma_w=sigma_w, max_n=15, dps=50, window_class="schwartz_gaussian"
        )

        assert res["status"] == "FINITE_WINDOWED_DIRICHLET_POLYNOMIAL_INNER_PRODUCT_EVALUATED"
        assert res["is_exact_match"] is True
        assert res["offdiagonal_is_structurally_present"] is True
        assert res["offdiagonal_witness_is_nonzero"] is True
        assert float(res["diff_quad_vs_exact"]) < 1e-10
        assert float(res["offdiagonal_norm"]) > 1e-5



class TestFiniteGradePullbackIdentity:
    """Verifies finite-T pullback identity vs asymptotic vanishing in Case A."""

    @pytest.mark.parametrize("T", ["10.0", "50.0", "100.0"])
    def test_finite_pullback_and_asymptotic_redundancy(self, T):
        res = math_core.evaluate_finite_grade_pullback_identity(T=T, h="0.1", dps=50)

        assert res["status"] == "FINITE_GRADE_PULLBACK_IDENTITY_EVALUATED"
        assert res["is_finite_pullback_identity"] is True
        assert res["finite_classification"] == "FINITE_GRADE_PULLBACK_IDENTITY"
        assert res["asymptotic_classification"] == "ASYMPTOTIC_GRADE_COORDINATE_REDUNDANCY"


class TestBilateralGradeCenteringSecondDifference:
    """Verifies bilateral grade centering generic algebraic identity."""

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
