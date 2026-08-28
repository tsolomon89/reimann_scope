"""
Tests for Background Dependence and Fixed Finite Perturbation Invisibility in CMSA Gate G4.

Verifies:
1. Exact pointwise background-dependence identity:
   Q(F, Delta) = |Delta|^2 + 2 Re(F conj(Delta)),
   Q(F, Delta) - Q(G, Delta) = 2 Re((F - G) conj(Delta)).
2. Counterexample proving Q(F, Delta) is not background-independent.
3. Fixed finite perturbation invisibility theorem:
   For any fixed finite linear combination of zero resolvents (single, conjugate pair,
   same-height functional-reflection pair, or quartet), the normalized infinite mean-square
   variation (1 / 2T) int_{-T}^T (|P_sigma - Delta|^2 - |P_sigma|^2) dt vanishes as T -> infinity.
"""

import pytest
import mpmath

from math_core import (
    verify_squared_norm_background_dependence,
    verify_fixed_finite_perturbation_invisibility,
    verify_additive_reference_subtraction_invariance,
    verify_cofinal_subcritical_norm_bound
)


class TestBackgroundDependenceAndInvarianceScope:
    """Rigorous Pointwise and Algebraic Background-Dependence Tests."""

    def test_background_dependence_exact_algebra(self):
        """Verifies Q(F, Delta) = |Delta|^2 + 2 Re(F conj(Delta)) and background difference identity."""
        res = verify_squared_norm_background_dependence(
            F_val='2.5 + 3.5j',
            G_val='-1.2 + 0.8j',
            delta_val='0.05 - 0.1j',
            dps=50
        )
        assert res["status"] == "BACKGROUND_DEPENDENCE_VERIFIED"
        assert res["is_symbolic_exact"] is True
        assert res["is_background_dependent"] is True
        assert mpmath.mpf(res["error_expansion_F"]) < mpmath.mpf('1e-40')
        assert mpmath.mpf(res["error_expansion_diff"]) < mpmath.mpf('1e-40')

    def test_background_dependence_counterexample(self):
        """Tests concrete counterexample F = 1, G = -1, Delta = 1 proving Q(1, 1) = 3 != -1 = Q(-1, 1)."""
        res = verify_squared_norm_background_dependence(
            F_val='1.0',
            G_val='-1.0',
            delta_val='1.0',
            dps=50
        )
        assert res["is_background_dependent"] is True
        assert mpmath.mpf(res["Q_F"]) == mpmath.mpf('3.0')
        assert mpmath.mpf(res["Q_G"]) == mpmath.mpf('-1.0')
        assert mpmath.mpf(res["Q_diff"]) == mpmath.mpf('4.0')

    def test_additive_reference_scope_vs_inner_background(self):
        """Verifies outer scalar reference subtraction is invariant, but inner background shift is non-invariant."""
        # Outer additive reference is invariant
        ref_res = verify_additive_reference_subtraction_invariance(
            s_delta='1.5',
            s_0='1.0',
            reference_r='100.0',
            dps=50
        )
        assert ref_res["is_invariant"] is True

        # Inner background shift is NOT invariant
        bg_res = verify_squared_norm_background_dependence(
            F_val='100.0',
            G_val='0.0',
            delta_val='1.0',
            dps=50
        )
        assert bg_res["is_background_dependent"] is True
        # Q(100, 1) = 101^2 - 100^2 = 201; Q(0, 1) = 1^2 - 0 = 1; difference = 200 != 0
        assert mpmath.mpf(bg_res["Q_diff"]) == mpmath.mpf('200.0')


class TestFixedFinitePerturbationInvisibility:
    """Tests that finite Dirichlet polynomial samples show decreasing normalized variation for fixed resolvents."""

    def test_single_resolvent_invisibility(self):
        """Single zero resolvent delta_1(t) = 1 / (a + i(t - gamma)) finite numerical evaluation."""
        resolvents = [(1.0, 1.0, 14.134725)]
        res = verify_fixed_finite_perturbation_invisibility(
            sigma='1.5',
            resolvents=resolvents,
            T_values=['30.0', '100.0', '300.0'],
            max_prime_n=30,
            dps=35
        )
        assert res["status"] == "FINITE_DIRICHLET_TRUNCATION_NUMERICAL_EVIDENCE"
        assert res["endpoint_magnitude_decreased"] is True
        assert res["prime_cutoff"] == 30
        assert "limit_caveat" in res
        assert "analytic_L2_norm_bound_squared" in res
        val_30 = abs(mpmath.mpf(res["results_by_T"][0]["normalized_integral"]))
        val_300 = abs(mpmath.mpf(res["results_by_T"][-1]["normalized_integral"]))
        assert val_300 < val_30

    def test_conjugate_pair_invisibility(self):
        """Conjugate pair {delta + i*gamma, delta - i*gamma} finite numerical evaluation."""
        resolvents = [
            (1.0, 0.95, 14.134725),
            (1.0, 0.95, -14.134725)
        ]
        res = verify_fixed_finite_perturbation_invisibility(
            sigma='1.5',
            resolvents=resolvents,
            T_values=['30.0', '100.0', '300.0'],
            max_prime_n=30,
            dps=35
        )
        assert res["status"] == "FINITE_DIRICHLET_TRUNCATION_NUMERICAL_EVIDENCE"
        assert res["endpoint_magnitude_decreased"] is True
        val_30 = abs(mpmath.mpf(res["results_by_T"][0]["normalized_integral"]))
        val_300 = abs(mpmath.mpf(res["results_by_T"][-1]["normalized_integral"]))
        assert val_300 < val_30

    def test_same_height_reflection_pair_invisibility(self):
        """Same-height reflection pair {delta + i*gamma, -delta + i*gamma} finite numerical evaluation."""
        resolvents = [
            (1.0, 0.95, 14.134725),
            (1.0, 1.05, 14.134725)
        ]
        res = verify_fixed_finite_perturbation_invisibility(
            sigma='1.5',
            resolvents=resolvents,
            T_values=['30.0', '100.0', '300.0'],
            max_prime_n=30,
            dps=35
        )
        assert res["status"] == "FINITE_DIRICHLET_TRUNCATION_NUMERICAL_EVIDENCE"
        assert res["endpoint_magnitude_decreased"] is True

    def test_quartet_invisibility(self):
        """Symmetric quartet {+/- delta +/- i*gamma} finite numerical evaluation."""
        resolvents = [
            (1.0, 0.95, 14.134725),
            (1.0, 0.95, -14.134725),
            (1.0, 1.05, 14.134725),
            (1.0, 1.05, -14.134725)
        ]
        res = verify_fixed_finite_perturbation_invisibility(
            sigma='1.5',
            resolvents=resolvents,
            T_values=['30.0', '100.0', '300.0'],
            max_prime_n=30,
            dps=35
        )
        assert res["status"] == "FINITE_DIRICHLET_TRUNCATION_NUMERICAL_EVIDENCE"
        assert res["endpoint_magnitude_decreased"] is True
        val_30 = abs(mpmath.mpf(res["results_by_T"][0]["normalized_integral"]))
        val_300 = abs(mpmath.mpf(res["results_by_T"][-1]["normalized_integral"]))
        assert val_300 < val_30

    def test_evaluator_input_validation(self):
        """Verifies strict input validation on domain, cutoffs, widths, and windows."""
        resolvents = [(1.0, 1.0, 14.134725)]
        # sigma <= 1
        with pytest.raises(ValueError, match="sigma must be strictly greater than 1"):
            verify_fixed_finite_perturbation_invisibility(sigma='1.0', resolvents=resolvents, T_values=['10.0'])
        with pytest.raises(ValueError, match="sigma must be strictly greater than 1"):
            verify_fixed_finite_perturbation_invisibility(sigma='0.5', resolvents=resolvents, T_values=['10.0'])

        # max_prime_n < 2
        with pytest.raises(ValueError, match="max_prime_n must be >= 2"):
            verify_fixed_finite_perturbation_invisibility(sigma='1.5', resolvents=resolvents, T_values=['10.0'], max_prime_n=1)

        # T <= 0
        with pytest.raises(ValueError, match="T values must be strictly positive"):
            verify_fixed_finite_perturbation_invisibility(sigma='1.5', resolvents=resolvents, T_values=['0.0'])
        with pytest.raises(ValueError, match="T values must be strictly positive"):
            verify_fixed_finite_perturbation_invisibility(sigma='1.5', resolvents=resolvents, T_values=['-10.0'])

        # a_j <= 0
        with pytest.raises(ValueError, match="resolvent width a_j must be strictly positive"):
            verify_fixed_finite_perturbation_invisibility(sigma='1.5', resolvents=[(1.0, 0.0, 14.134725)], T_values=['10.0'])
        with pytest.raises(ValueError, match="resolvent width a_j must be strictly positive"):
            verify_fixed_finite_perturbation_invisibility(sigma='1.5', resolvents=[(1.0, -0.5, 14.134725)], T_values=['10.0'])

    def test_empty_resolvents_handling(self):
        """Verifies clean output structure for empty resolvents list."""
        res = verify_fixed_finite_perturbation_invisibility(
            sigma='1.5',
            resolvents=[],
            T_values=['10.0', '50.0'],
            max_prime_n=20
        )
        assert res["status"] == "FINITE_DIRICHLET_TRUNCATION_NUMERICAL_EVIDENCE"
        assert res["n_resolvents"] == 0
        assert res["endpoint_magnitude_decreased"] is False
        assert res["analytic_L2_norm_bound_squared"] == "0.0"


class TestCofinalSubcriticalNormBound:
    """Tests for the Cofinal Subcritical-Norm Growth Bound |V_T| <= x_T^2/2 + sqrt(2M)*x_T."""

    def test_subcritical_norm_bound_evaluation(self):
        """Verifies calculation of abstract subcritical variation upper bound."""
        # M = 4.0 (sqrt(2M) = sqrt(8) approx 2.8284), delta_norm = 1.0, T = 100 -> x_T = 0.1
        # V_bound = 0.01 / 2 + sqrt(8) * 0.1 = 0.005 + 0.2828427 = 0.2878427
        res = verify_cofinal_subcritical_norm_bound(
            M_bound='4.0',
            delta_L2_norm='1.0',
            T_val='100.0',
            dps=35
        )
        assert res["status"] == "SUBCRITICAL_NORM_BOUND_EVALUATED"
        assert mpmath.almosteq(mpmath.mpf(res["x_T"]), mpmath.mpf('0.1'), abs_eps=1e-10)
        assert mpmath.almosteq(mpmath.mpf(res["direct_energy_bound"]), mpmath.mpf('0.005'), abs_eps=1e-10)
        assert mpmath.almosteq(mpmath.mpf(res["cross_term_bound"]), mpmath.sqrt(8) * mpmath.mpf('0.1'), abs_eps=1e-10)

    def test_subcritical_norm_bound_scaling_to_zero(self):
        """Verifies that as T increases with ||Delta|| = o(sqrt(T)), the bound vanishes."""
        # Fixed ||Delta|| = 5.0, M = 2.0
        bounds = []
        for T_val in [100.0, 1000.0, 10000.0, 100000.0]:
            res = verify_cofinal_subcritical_norm_bound(
                M_bound='2.0',
                delta_L2_norm='5.0',
                T_val=T_val,
                dps=35
            )
            bounds.append(mpmath.mpf(res["total_variation_bound"]))
        # Bounds must strictly decrease towards 0
        for i in range(len(bounds) - 1):
            assert bounds[i+1] < bounds[i]
        assert bounds[-1] < mpmath.mpf('0.1')

    def test_subcritical_norm_bound_validation(self):
        """Verifies validation on M_bound >= 0, delta_norm >= 0, T > 0."""
        with pytest.raises(ValueError, match="M_bound must be non-negative"):
            verify_cofinal_subcritical_norm_bound(M_bound='-1.0', delta_L2_norm='1.0', T_val='10.0')
        with pytest.raises(ValueError, match="delta_L2_norm must be non-negative"):
            verify_cofinal_subcritical_norm_bound(M_bound='1.0', delta_L2_norm='-1.0', T_val='10.0')
        with pytest.raises(ValueError, match="T_val must be strictly positive"):
            verify_cofinal_subcritical_norm_bound(M_bound='1.0', delta_L2_norm='1.0', T_val='0.0')
