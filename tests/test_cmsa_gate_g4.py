"""
Tests for Gate G4 Infinite-Regularization and Radial-Survival in Completed Mean-Square Anchor (CMSA).

Verifies:
1. G4a: Arithmetic Independence Firewall (zero-independent arithmetic evaluator).
2. G4b: Exact finite 4-term spectral expansion across Rectangular, Fejer, Abel, and Gaussian windows.
3. G4c & G4d: Asymptotic regimes, boundary layers, and cofinal schedule sweeps H = H(T).
4. G4e: Full regularized radial variation Delta S vs isolated Delta I_ZZ for on-line and off-line zeros.
5. Multi-precision consistency and symmetric zero permutation invariance.
"""

import pytest
import mpmath
from unittest.mock import patch

from math_core import (
    exact_finite_zero_kernel_J_T,
    exact_finite_zero_zero_kernel_K_T,
    exact_fejer_zero_kernel_J_T,
    exact_fejer_zero_zero_kernel_K_T,
    evaluate_g4_asymptotic_regimes,
    evaluate_g4_window_spectral_expansion,
    evaluate_g4_radial_variation_diagnostic,
    evaluate_g4_cofinal_schedule_sweep,
    evaluate_g4_radial_response_coefficient,
    certify_g4_radial_sign_witness,
    verify_g4_arithmetic_independence_firewall,
    finite_dirichlet_mean_square_sinc_kernel,
    completed_mean_square_anchor_cmsa1,
    spectral_real_axis_defect_delta
)


class TestGateG4ArithmeticFirewall:
    """Sub-Gate G4a: Arithmetic Path Zero-Divisor Independence."""

    def test_arithmetic_firewall_mock_verification(self):
        """Verifies that arithmetic anchor evaluation never invokes reference zero loaders."""
        res = verify_g4_arithmetic_independence_firewall()
        assert res["firewall_intact"] is True
        assert res["status"] == "ARITHMETIC_INDEPENDENCE_FIREWALL_VERIFIED"

    def test_arithmetic_anchor_zero_free_direct_mock(self):
        """Mocks reference_data functions and confirms completed_mean_square_anchor_cmsa1 runs without calling them."""
        with patch('reference_data.load_first_100_reference_zeros', side_effect=AssertionError("Zero loader invoked")):
            res = completed_mean_square_anchor_cmsa1(sigma='1.5', T='20.0', max_N=25, dps=35)
            assert res["status"] == "EXACT_FINITE_IDENTITY"
            assert res["earliest_open_gate"] == "G4"


class TestGateG4FiniteWindowExpansions:
    """Sub-Gate G4b: Exact Finite Expansions across Window Families."""

    def test_fejer_zero_kernel_analytic_vs_quadrature(self):
        """Tests exact analytic Fejer kernel J_T^Fejer against independent numerical quadrature."""
        with mpmath.workdps(60):
            p = mpmath.mpc('1.5', '14.134725')
            q = mpmath.mpc('1.5', '-14.134725')
            T_val = mpmath.mpf('30.0')

            j_analytic = exact_fejer_zero_kernel_J_T(p, q, T_val, dps=50)

            # Independent numerical quadrature
            f_integrand = lambda t: (1 - abs(t) / T_val) / ((p + mpmath.mpc(0, t)) * (q - mpmath.mpc(0, t)))
            j_quad = mpmath.quad(f_integrand, [-T_val, 0, T_val]) / T_val

            diff = abs(j_analytic - j_quad)
            assert diff < mpmath.mpf('1e-40')

    def test_fejer_zero_zero_kernel_analytic_vs_quadrature(self):
        """Tests exact paired Fejer kernel K_T^Fejer against numerical integration."""
        with mpmath.workdps(60):
            lam1 = mpmath.mpc('0.0', '14.134725')
            lam2 = mpmath.mpc('0.0', '21.022040')
            a = mpmath.mpf('1.5')
            T_val = mpmath.mpf('25.0')

            k_analytic = exact_fejer_zero_zero_kernel_K_T(lam1, lam2, a, T_val, mult1=1, mult2=1, dps=50)

            # Numerical evaluation via resolvents
            def r1(t):
                z = mpmath.mpc(a, t)
                return 2 * z / (z * z - lam1 * lam1)

            def r2(t):
                z = mpmath.mpc(a, t)
                return 2 * z / (z * z - lam2 * lam2)

            w_fn = lambda t: (1 - abs(t) / T_val) / T_val
            k_quad = mpmath.quad(lambda t: w_fn(t) * r1(t) * mpmath.conj(r2(t)), [-T_val, 0, T_val])

            diff = abs(k_analytic - k_quad)
            assert diff < mpmath.mpf('1e-40')

    @pytest.mark.slow_numerical
    @pytest.mark.parametrize("win_type", ["rectangular", "fejer", "abel", "gaussian"])
    def test_window_spectral_expansion_closure(self, win_type):
        """Verifies S_{N, T} = I_AA - I_AZ - I_ZA + I_ZZ across all 4 window types."""
        zeros = [(0.0, 14.134725, 1), (0.0, 21.022040, 1)]
        res = evaluate_g4_window_spectral_expansion(
            sigma='2.0', T='20.0', upper_zeros=zeros, window_type=win_type, dps=40
        )
        closure_diff = mpmath.mpf(res["closure_difference"])
        assert closure_diff < mpmath.mpf('1e-25')


class TestGateG4AsymptoticRegimesAndBoundaryLayers:
    """Sub-Gates G4c & G4d: Asymptotics, Boundary Layers, and Cofinal Limits."""

    def test_four_asymptotic_regimes(self):
        """Verifies the 4 asymptotic regimes of J_T(a - i*gamma, a + i*gamma)."""
        gamma = mpmath.mpf('50.0')
        a = mpmath.mpf('1.5')
        # T values representing: plateau (|gamma| << T), boundary layer (|gamma - T| = O(1)), outer tail (|gamma| >> T)
        T_vals = [500.0, 100.0, 50.0, 10.0]
        results = evaluate_g4_asymptotic_regimes(a=a, gamma=gamma, T_vals=T_vals, dps=35)

        # 1. Plateau regime (T=500, c=0.1)
        r_plateau = results[0]
        assert r_plateau["regime"] == "PLATEAU_INNER"
        diff_plateau = abs(mpmath.mpf(r_plateau["J_exact"]) - mpmath.mpf(r_plateau["asymp_plateau"]))
        assert diff_plateau / mpmath.mpf(r_plateau["asymp_plateau"]) < 0.02

        # 2. Boundary layer regime (T=50, c=1.0)
        r_boundary = results[2]
        assert r_boundary["regime"] == "BOUNDARY_LAYER"
        diff_boundary = abs(mpmath.mpf(r_boundary["J_exact"]) - mpmath.mpf(r_boundary["transition_formula"]))
        assert diff_boundary < mpmath.mpf('1e-15')

        # 3. Outer tail regime (T=10, c=5.0)
        r_tail = results[3]
        assert r_tail["regime"] == "OUTER_TAIL"
        diff_tail = abs(mpmath.mpf(r_tail["J_exact"]) - mpmath.mpf(r_tail["asymp_tail"]))
        assert diff_tail / mpmath.mpf(r_tail["asymp_tail"]) < 0.05

    def test_cofinal_schedule_sweep_scaling(self):
        """Tests cofinal schedule H(T) = c*T, confirming expansion of included zeros with interval."""
        zeros = [(0.0, 14.134725, 1), (0.0, 21.022040, 1), (0.0, 25.010858, 1), (0.0, 30.424876, 1)]
        schedule = lambda T: 1.5 * T
        T_vals = [10.0, 20.0, 30.0]
        results = evaluate_g4_cofinal_schedule_sweep(
            sigma='2.0', T_vals=T_vals, schedule_fn=schedule, available_zeros=zeros, dps=35
        )
        assert len(results) == 3
        # Included zero count grows as cutoff H(T) expands
        zero_counts = [r["included_zero_count"] for r in results]
        assert zero_counts == [1, 3, 4]
        # Unnormalized quantity T * S is positive and tracked
        for r in results:
            assert mpmath.mpf(r["T_times_S"]) > 0


class TestGateG4RadialVariationAndPositivity:
    """Sub-Gate G4e: Full Regularized Radial Variation Delta S."""

    def test_online_synthetic_zero_gives_exact_zero_variation(self):
        """An on-line synthetic zero pair gives Delta S = 0 identically."""
        res = evaluate_g4_radial_variation_diagnostic(
            sigma='2.0', gamma='14.134725', delta='0.0', T='30.0', window_type='rectangular', dps=40
        )
        delta_s = abs(mpmath.mpf(res["delta_S_full"]))
        assert delta_s < mpmath.mpf('1e-30')

    @pytest.mark.slow_numerical
    @pytest.mark.parametrize("win_type", ["rectangular", "fejer", "abel", "gaussian"])
    def test_offline_quartet_radial_variation_positive_above_resonance(self, win_type):
        """Replacing an on-line pair with an off-line quartet produces Delta S > 0 when T encompasses the resonance."""
        res = evaluate_g4_radial_variation_diagnostic(
            sigma='2.0', gamma='14.134725', delta='0.1', T='30.0', window_type=win_type, dps=40
        )
        delta_s = mpmath.mpf(res["delta_S_full"])
        assert delta_s > 0
        assert res["is_full_variation_positive"] is True

    @pytest.mark.slow_numerical
    def test_radial_variation_multi_precision_stability(self):
        """Verifies that Delta S is stable across dps=35, dps=50, and dps=80."""
        prec_vals = [35, 50, 80]
        delta_s_list = []
        for p in prec_vals:
            res = evaluate_g4_radial_variation_diagnostic(
                sigma='2.0', gamma='14.134725', delta='0.05', T='25.0', window_type='rectangular', dps=p
            )
            delta_s_list.append(mpmath.mpf(res["delta_S_full"]))

        assert abs(delta_s_list[0] - delta_s_list[1]) < mpmath.mpf('1e-30')
        assert abs(delta_s_list[1] - delta_s_list[2]) < mpmath.mpf('1e-45')

    @pytest.mark.slow_numerical
    def test_symmetric_permutation_invariance(self):
        """Verifies that reordering zero list does not change the spectral expansion."""
        zeros_a = [(0.0, 14.134725, 1), (0.0, 21.022040, 1), (0.0, 25.010858, 1)]
        zeros_b = [(0.0, 25.010858, 1), (0.0, 14.134725, 1), (0.0, 21.022040, 1)]

        res_a = evaluate_g4_window_spectral_expansion(sigma='1.8', T='20.0', upper_zeros=zeros_a, dps=40)
        res_b = evaluate_g4_window_spectral_expansion(sigma='1.8', T='20.0', upper_zeros=zeros_b, dps=40)

        diff = abs(mpmath.mpf(res_a["S_direct"]) - mpmath.mpf(res_b["S_direct"]))
        assert diff < mpmath.mpf('1e-35')


class TestGateG4RadialResponseCoefficientAndWitnesses:
    """Sub-Gate G4e Radial Sign Evidence and Certified Arb Ball Witness."""

    @pytest.mark.slow_numerical
    def test_c_w_second_order_coefficient_ratio(self):
        """Verifies Delta S / delta^2 -> C_W as delta -> 0 for Fejer window."""
        c_res = evaluate_g4_radial_response_coefficient(
            sigma=5.0, gamma=14.0, T=16.8, window_type="fejer", dps=40
        )
        c_val = mpmath.mpf(c_res["C_W"])
        assert c_val < 0  # Evidence against unconditional positivity on general parameters

        var_res = evaluate_g4_radial_variation_diagnostic(
            sigma=5.0, gamma=14.0, delta=0.005, T=16.8, window_type="fejer", dps=40
        )
        delta_s = mpmath.mpf(var_res["delta_S_full"])
        d_sq = mpmath.mpf(0.005) ** 2
        ratio = (delta_s / d_sq) / c_val
        assert abs(ratio - 1.0) < mpmath.mpf('1e-4')

    @pytest.mark.slow_numerical
    def test_rectangular_negative_witness_evidence(self):
        """Numerical evidence for Witness 1 (Rectangular): sigma=2, gamma=14, delta=0.1, T=2.8 -> Delta S < 0."""
        from math_core import evaluate_g4_radial_sign_evidence
        ev = evaluate_g4_radial_sign_evidence(
            sigma=2.0, gamma=14.0, delta=0.1, T=2.8, window_type="rectangular", dps=50
        )
        assert ev["has_negative_evidence"] is True
        assert ev["evidence_status"] == "NUMERICAL_EVIDENCE_NEGATIVE"
        assert mpmath.mpf(ev["estimate_upper_bound"]) < 0

    @pytest.mark.slow_numerical
    def test_fejer_negative_witness_evidence_above_resonance(self):
        """Numerical evidence for Witness 2 (Fejer): sigma=5, gamma=14, delta=0.49, T=16.8 (T > gamma) -> Delta S < 0."""
        from math_core import evaluate_g4_radial_sign_evidence
        ev = evaluate_g4_radial_sign_evidence(
            sigma=5.0, gamma=14.0, delta=0.49, T=16.8, window_type="fejer", dps=50
        )
        assert ev["has_negative_evidence"] is True
        assert ev["evidence_status"] == "NUMERICAL_EVIDENCE_NEGATIVE"
        assert mpmath.mpf(ev["estimate_upper_bound"]) < 0

    @pytest.mark.slow_numerical
    def test_fejer_witness_wit02_arb_ball_certification(self):
        """Rigorous certified outward-rounded Arb ball integration for Witness 2 (Fejer)."""
        from math_core import certify_g4_fejer_witness_arb
        cert = certify_g4_fejer_witness_arb(
            sigma="5.0", gamma="14.0", delta="0.49", T="16.8", n_subdivisions=50000, dps=60
        )
        assert cert["is_certified_negative"] is True
        assert cert["status"] == "CERTIFIED_NEGATIVE_ARB_BALL"
        # The upper bound of the enclosure ball must be strictly below 0
        from flint import arb
        upper_b = arb(cert["interval_upper"])
        assert upper_b < 0
        assert upper_b < arb("-0.00015")  # Enclosed strictly below -1.5e-4


    @pytest.mark.slow_numerical
    def test_abel_negative_witness_evidence(self):
        """Numerical evidence for Witness 3 (Abel): sigma=1.01, gamma=21, delta=0.49, T=1.05 -> Delta S < 0."""
        from math_core import evaluate_g4_radial_sign_evidence
        ev = evaluate_g4_radial_sign_evidence(
            sigma=1.01, gamma=21.0, delta=0.49, T=1.05, window_type="abel", dps=50
        )
        assert ev["has_negative_evidence"] is True
        assert ev["evidence_status"] == "NUMERICAL_EVIDENCE_NEGATIVE"
        assert mpmath.mpf(ev["estimate_upper_bound"]) < 0

    @pytest.mark.slow_numerical
    def test_gaussian_negative_witness_evidence(self):
        """Numerical evidence for Witness 4 (Gaussian): sigma=1.01, gamma=14, delta=0.49, T=1.4 -> Delta S < 0."""
        from math_core import evaluate_g4_radial_sign_evidence
        ev = evaluate_g4_radial_sign_evidence(
            sigma=1.01, gamma=14.0, delta=0.49, T=1.4, window_type="gaussian", dps=50
        )
        assert ev["has_negative_evidence"] is True
        assert ev["evidence_status"] == "NUMERICAL_EVIDENCE_NEGATIVE"
        assert mpmath.mpf(ev["estimate_upper_bound"]) < 0


class TestAdditiveReferenceInvarianceNoGo:
    """Rigorous No-Go Theorem for Additive Divisor-Independent Renormalizations."""

    def test_additive_reference_subtraction_invariance_exact(self):
        """For any scalar R, (S(Z_delta) - R) - (S(Z_0) - R) == S(Z_delta) - S(Z_0) identically."""
        from math_core import verify_additive_reference_subtraction_invariance
        res = verify_additive_reference_subtraction_invariance(
            s_delta='1.23456789',
            s_0='1.23456700',
            reference_r='98765.43210',
            dps=50
        )
        assert res["is_invariant"] is True
        assert res["is_symbolic_exact"] is True
        assert res["status"] == "ADDITIVE_REFERENCE_INVARIANCE_VERIFIED"
        assert mpmath.mpf(res["algebraic_discrepancy"]) < mpmath.mpf('1e-40')

    def test_additive_reference_cannot_repair_negative_witness(self):
        """Applying any additive reference R to Witness WIT-02 leaves Delta S < 0 invariant."""
        from math_core import verify_additive_reference_subtraction_invariance
        # Using Witness WIT-02 parameters
        res = verify_additive_reference_subtraction_invariance(
            s_delta='0.0010',
            s_0='0.00117183799',
            reference_r='100.5',
            dps=50
        )
        assert res["is_invariant"] is True
        raw = mpmath.mpf(res["raw_difference"])
        renorm = mpmath.mpf(res["renormalized_difference"])
        assert raw < 0
        assert renorm == raw < 0


