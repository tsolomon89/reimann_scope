"""
tests/test_extended_xi.py — Unit tests for extended xi evaluation and functional equation covariance.
"""

import pytest
import mpmath
import math_core
import transcendental


def test_extended_xi_native_slice():
    """Verify X_tau(s, 0) == xi(s) at high precision."""
    with mpmath.workdps(80):
        s = mpmath.mpc('0.5', '14.1347251417346937904572519835624702707842571156992431756855674601')
        xi_native = math_core.completed_xi(s, dps=80)
        xi_ext = transcendental.evaluate_extended_xi(s, grade=0, dps=80)
        assert abs(xi_ext - xi_native) < mpmath.mpf('1e-70')
        assert abs(xi_ext) < mpmath.mpf('1e-50')


def test_extended_xi_functional_equation():
    """
    Verify extended functional equation:
    X_tau(s, k) = X_tau(tau^k - s, k).
    """
    with mpmath.workdps(80):
        tau = math_core.get_tau(dps=80)
        for K in [-2, -1, 0, 1, 2]:
            g_obj = transcendental.IntegerTauGrade(K=K)
            scale = g_obj.numeric_scale(dps=80)
            
            # Arbitrary test point s
            s = mpmath.mpc('1.75', '23.45')
            s_refl = scale - s  # tau^K - s
            
            xi_val1 = transcendental.evaluate_extended_xi(s, grade=g_obj, dps=80)
            xi_val2 = transcendental.evaluate_extended_xi(s_refl, grade=g_obj, dps=80)
            
            assert abs(xi_val1 - xi_val2) < mpmath.mpf('1e-65')
