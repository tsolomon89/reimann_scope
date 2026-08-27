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
    verify_additive_reference_subtraction_invariance
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
    """Tests that fixed finite zero perturbations produce zero normalized infinite mean response."""

    def test_single_resolvent_invisibility(self):
        """Single zero resolvent delta_1(t) = 1 / (a + i(t - gamma)) has vanishing mean square variation."""
        # a = 1.0, gamma = 14.134725
        resolvents = [(1.0, 1.0, 14.134725)]
        res = verify_fixed_finite_perturbation_invisibility(
            sigma='1.5',
            resolvents=resolvents,
            T_values=['30.0', '100.0', '300.0'],
            max_prime_n=30,
            dps=35
        )
        assert res["status"] == "FIXED_FINITE_PERTURBATION_INVISIBILITY_VERIFIED"
        assert res["is_decaying_to_zero"] is True
        # Check that normalized integral at T=300 is significantly smaller than at T=30
        val_30 = abs(mpmath.mpf(res["results_by_T"][0]["normalized_integral"]))
        val_300 = abs(mpmath.mpf(res["results_by_T"][-1]["normalized_integral"]))
        assert val_300 < val_30

    def test_conjugate_pair_invisibility(self):
        """Conjugate pair {delta + i*gamma, delta - i*gamma} has vanishing mean square variation."""
        # gamma = 14.134725, delta = 0.05, sigma = 1.5 -> a = 1.5 - 0.5 - 0.05 = 0.95
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
        assert res["status"] == "FIXED_FINITE_PERTURBATION_INVISIBILITY_VERIFIED"
        assert res["is_decaying_to_zero"] is True
        val_30 = abs(mpmath.mpf(res["results_by_T"][0]["normalized_integral"]))
        val_300 = abs(mpmath.mpf(res["results_by_T"][-1]["normalized_integral"]))
        assert val_300 < val_30

    def test_same_height_reflection_pair_invisibility(self):
        """Same-height reflection pair {delta + i*gamma, -delta + i*gamma} has vanishing mean square variation."""
        # gamma = 14.134725, delta = 0.05 -> a_1 = 0.95, a_2 = 1.05
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
        assert res["status"] == "FIXED_FINITE_PERTURBATION_INVISIBILITY_VERIFIED"
        assert res["is_decaying_to_zero"] is True

    def test_quartet_invisibility(self):
        """Symmetric quartet {+/- delta +/- i*gamma} has vanishing mean square variation."""
        # gamma = 14.134725, delta = 0.05 -> a = 0.95 and a = 1.05 at +/- gamma
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
        assert res["status"] == "FIXED_FINITE_PERTURBATION_INVISIBILITY_VERIFIED"
        assert res["is_decaying_to_zero"] is True
        val_30 = abs(mpmath.mpf(res["results_by_T"][0]["normalized_integral"]))
        val_300 = abs(mpmath.mpf(res["results_by_T"][-1]["normalized_integral"]))
        assert val_300 < val_30
