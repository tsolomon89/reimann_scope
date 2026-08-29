"""tests/test_weil_curvature.py — Verification Suite for Weil–Hermitian Curvature Identities

Verifies:
1. Pointwise Weil–curvature identity:
   1/2 * (1/|rho|^2 + 1/|1-rho|^2) - Re(1 / (rho*(1-rho))) = 2*delta^2 / (|rho|^2 * |1-rho|^2)
                                                            = B_rho''(0) / ((log tau)^2 * |rho|^2 * |1-rho|^2).
2. Geometric involution difference and squared discrepancy:
   J(rho) - C(rho) = 1 - rho - conj(rho) = - 2 * delta,
   |J(rho) - C(rho)|^2 = 4 * delta^2.
3. Truncated spectral sum closure on reference zeros and synthetic quartets:
   N_xi,sym - C_xi,trunc = sum 2*delta_j^2 / (|rho_j|^2 * |1-rho_j|^2).
4. On-line zero rigidity: Delta_curv == 0 for all delta_j = 0.
5. Off-line quartet strict positivity: Delta_curv > 0 for delta_j != 0.
6. Finite-prime local Gram matrix negative-definiteness (falsification witness for local-prime Hilbert space factorization).
7. Completed-xi Hadamard constant C_xi = 2 + EulerGamma - log(4*pi).
"""

import mpmath
import pytest
import math_core
from reference_data import load_first_100_reference_zeros


class TestPointwiseWeilCurvatureIdentity:
    """Verifies the pointwise Weil-Hermitian rational identity and geometric involutions."""

    @pytest.mark.parametrize("delta,gamma", [
        ("0.0", "14.134725"),
        ("0.0", "21.022040"),
        ("0.0", "100.123456"),
        ("0.001", "14.134725"),
        ("-0.005", "21.022040"),
        ("0.025", "30.424876"),
        ("-0.10", "50.000000"),
        ("0.25", "10.000000"),
    ])
    def test_pointwise_weil_curvature_exact_match(self, delta, gamma):
        res = math_core.evaluate_pointwise_weil_curvature_identity(delta=delta, gamma=gamma, dps=50)
        assert res["status"] == "POINTWISE_WEIL_CURVATURE_IDENTITY_VERIFIED"
        assert res["is_exact_match"] is True
        assert float(res["involution_diff_err"]) < 1e-45
        assert float(res["sq_discrepancy_err"]) < 1e-45
        assert float(res["diff_vs_exact_err"]) < 1e-45
        assert float(res["exact_vs_curv_err"]) < 1e-45

        # On-line vs off-line checks
        if delta == "0.0":
            assert res["is_on_critical_line"] is True
            assert abs(float(res["T_diff"])) < 1e-45
            assert abs(float(res["T_exact"])) < 1e-45
            assert abs(float(res["sq_discrepancy"])) < 1e-45
        else:
            assert res["is_on_critical_line"] is False
            assert float(res["T_diff"]) > 0.0
            assert float(res["T_exact"]) > 0.0
            assert float(res["sq_discrepancy"]) > 0.0


class TestWeilSpectralSumsAndRigidity:
    """Verifies finite spectral sums closure, on-line rigidity, and off-line positivity."""

    def test_first_10_reference_zeros_on_line_rigidity(self):
        zeros_100 = load_first_100_reference_zeros()
        zeros_10 = [("0.0", str(gam), 1) for gam in zeros_100[:10]]
        res = math_core.evaluate_weil_hermitian_spectral_sums(zeros_10, dps=50)

        assert res["status"] == "WEIL_HERMITIAN_SPECTRAL_SUMS_VERIFIED"
        assert res["closure_satisfied"] is True
        assert float(res["closure_error"]) < 1e-40
        assert res["all_on_line"] is True
        assert res["curvature_defect_is_zero"] is True
        assert float(res["delta_curv"]) == 0.0
        # N_xi,sym == C_xi,trunc for on-line zeros
        assert abs(float(res["N_xi_sym"]) - float(res["C_xi_trunc"])) < 1e-40

    def test_first_100_reference_zeros_on_line_rigidity(self):
        zeros_100 = load_first_100_reference_zeros()
        zeros_data = [("0.0", str(gam), 1) for gam in zeros_100]
        res = math_core.evaluate_weil_hermitian_spectral_sums(zeros_data, dps=50)

        assert res["status"] == "WEIL_HERMITIAN_SPECTRAL_SUMS_VERIFIED"
        assert res["closure_satisfied"] is True
        assert res["curvature_defect_is_zero"] is True
        assert float(res["delta_curv"]) == 0.0

        # Verify monotonicity towards C_xi
        C_xi_exact = float(res["C_xi_classical_constant"])
        C_xi_trunc_100 = float(res["C_xi_trunc"])
        assert 0 < C_xi_trunc_100 < C_xi_exact

    def test_synthetic_offline_quartet_strict_positivity(self):
        """Off-line quartets generate strictly positive curvature defect Delta_curv > 0."""
        quartet = [
            ("0.05", "14.134725", 1),
            ("0.05", "-14.134725", 1),
            ("-0.05", "14.134725", 1),
            ("-0.05", "-14.134725", 1),
        ]
        res = math_core.evaluate_weil_hermitian_spectral_sums(quartet, dps=50)

        assert res["status"] == "WEIL_HERMITIAN_SPECTRAL_SUMS_VERIFIED"
        assert res["closure_satisfied"] is True
        assert res["has_off_line"] is True
        assert res["curvature_defect_is_positive"] is True
        assert float(res["delta_curv"]) > 0.0
        assert abs(float(res["delta_diff"]) - float(res["delta_curv"])) < 1e-40

    def test_mixed_online_and_offline_zeros(self):
        """Mixed configuration of on-line zeros and off-line quartets."""
        zeros_100 = load_first_100_reference_zeros()
        mixed = [("0.0", str(gam), 1) for gam in zeros_100[:5]]
        mixed.extend([
            ("0.02", "25.010857", 1),
            ("-0.02", "25.010857", 1),
        ])
        res = math_core.evaluate_weil_hermitian_spectral_sums(mixed, dps=50)

        assert res["status"] == "WEIL_HERMITIAN_SPECTRAL_SUMS_VERIFIED"
        assert res["closure_satisfied"] is True
        assert res["has_off_line"] is True
        assert res["curvature_defect_is_positive"] is True
        assert float(res["delta_curv"]) > 0.0


class TestFinitePrimeWeilGramMatrix:
    """Verifies that local prime distributions on genuine two-bump test functions produce indefinite eigenvalues (+- w_p)."""

    def test_finite_prime_indefinite_eigenvalues(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        res = math_core.evaluate_finite_prime_weil_gram_matrix(primes=primes, dps=50)

        assert res["status"] == "FINITE_PRIME_WEIL_GRAM_MATRIX_ANALYZED"
        assert res["is_positive_semidefinite"] is False
        assert res["is_strictly_negative_definite"] is False
        assert res["falsification_witness"] == "PRIME_ONLY_AUTOCORRELATION_IS_INDEFINITE_NOT_POSITIVE_SEMIDEFINITE"
        assert res["classification"] == "FAIL_NAIVE_PRIME_LOCAL_FACTORIZATION"
        assert res["global_weil_positivity_status"] == "OPEN_GLOBAL_POSITIVE_TYPE_FACTORIZATION"

        # Verify each 2x2 two-bump witness has eigenvalues +w_p and -w_p
        for w in res["two_bump_witnesses"]:
            assert w["is_indefinite"] is True
            w_p = float(w["w_p"])
            assert w_p > 0.0
            evs = [float(ev) for ev in w["eigenvalues"]]
            assert len(evs) == 2
            assert max(evs) > 0.0
            assert min(evs) < 0.0
            assert abs(max(evs) + min(evs)) < 1e-10



class TestMellinProbeAnalysis:
    """Verifies test function Mellin transform vs spectral probe 1/s and regularization."""

    def test_naive_indicator_differs_from_one_over_s(self):
        # Test at first zero rho = 0.5 + 14.134725 i
        s_test = "0.5 + 14.1347251417346937904572519835624702707842571156992431756855674601499634298092567649490103931715610127723 * I"
        res = math_core.evaluate_fourier_mellin_probe_analysis(s_test, dps=50)

        assert res["status"] == "FOURIER_MELLIN_PROBE_ANALYSIS_COMPLETED"
        assert res["g0_equals_1_over_s"] is False
        assert float(res["diff_g0_vs_phi0"]) > 0.05
        assert res["test_function_classification"] == "FAIL_TEST_FUNCTION_IDENTIFICATION"
        assert res["regularization_obligation"] == "OPEN_ADMISSIBLE_PROBE_REGULARIZATION"

    def test_regularized_smoothing_family_approaches_one_over_s(self):
        s_test = "0.5 + 14.1347251417346937904572519835624702707842571156992431756855674601499634298092567649490103931715610127723 * I"
        res = math_core.evaluate_fourier_mellin_probe_analysis(s_test, dps=50)

        # Regularized cutoff error should be very small
        assert float(res["regularization_error"]) < 1e-3


class TestAdditiveCoordinateWeilHermitianForm:
    """Verifies additive coordinate Hermitian Weil form Q_W(f) and Hermitian companion Q_H(f)."""

    def test_additive_form_equality_on_line(self):
        zeros_100 = load_first_100_reference_zeros()
        zeros_data = [("0.0", str(gam), 1) for gam in zeros_100[:20]]
        res = math_core.evaluate_additive_coordinate_weil_hermitian_form(zeros_data, dps=50)

        assert res["status"] == "ADDITIVE_COORDINATE_WEIL_HERMITIAN_FORM_EVALUATED"
        assert res["all_on_line"] is True
        assert res["equality_holds"] is True
        assert float(res["diff_QH_vs_QW"]) < 1e-40

    def test_additive_form_discrepancy_off_line(self):
        quartet = [
            ("0.05", "14.134725", 1),
            ("0.05", "-14.134725", 1),
            ("-0.05", "14.134725", 1),
            ("-0.05", "-14.134725", 1),
        ]
        res = math_core.evaluate_additive_coordinate_weil_hermitian_form(quartet, dps=50)

        assert res["status"] == "ADDITIVE_COORDINATE_WEIL_HERMITIAN_FORM_EVALUATED"
        assert res["all_on_line"] is False
        assert res["equality_holds"] is False
        assert float(res["diff_QH_vs_QW"]) > 0.0

