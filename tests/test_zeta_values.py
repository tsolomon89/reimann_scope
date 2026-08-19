"""
tests/test_zeta_values.py — Tests for Zeta Values, Schwarz Reality, and Functional Equation

Trust tests 1, 2, 3 from SPEC.md §12.
"""

import pytest
import mpmath
import math_core


def test_generic_zeta_values():
    """Trust Test 1: Verify known special values of Riemann zeta to 50 dps."""
    with mpmath.workdps(50):
        # zeta(2) = pi^2 / 6
        z2 = math_core.zeta_eval(2, dps=50)
        expected_z2 = (mpmath.pi ** 2) / 6
        assert abs(z2 - expected_z2) < mpmath.mpf('1e-45')
        
        # zeta(4) = pi^4 / 90
        z4 = math_core.zeta_eval(4, dps=50)
        expected_z4 = (mpmath.pi ** 4) / 90
        assert abs(z4 - expected_z4) < mpmath.mpf('1e-45')
        
        # zeta(0) = -1/2
        z0 = math_core.zeta_eval(0, dps=50)
        assert abs(z0 - mpmath.mpf('-0.5')) < mpmath.mpf('1e-45')
        
        # zeta(-1) = -1/12
        zm1 = math_core.zeta_eval(-1, dps=50)
        assert abs(zm1 - (mpmath.mpf('-1') / 12)) < mpmath.mpf('1e-45')


def test_schwarz_reality():
    """Trust Test 2: Verify Schwarz reflection zeta(conj(s)) == conj(zeta(s)) to 80 dps."""
    dps = 80
    with mpmath.workdps(dps):
        test_points = [
            mpmath.mpc('0.75', '14.13472514173469379045725198356247027078425711569924317568556746'),
            mpmath.mpc('0.5', '21.0220396387715549926284795938969027773343405249027818047'),
            mpmath.mpc('-1.5', '3.14159265358979323846264338327950288419716939937510582097'),
            mpmath.mpc('2.5', '100.5')
        ]
        for s in test_points:
            z1 = math_core.zeta_eval(mpmath.conj(s), dps=dps)
            z2 = mpmath.conj(math_core.zeta_eval(s, dps=dps))
            assert abs(z1 - z2) < mpmath.mpf('1e-70')


def test_functional_equation():
    """Trust Test 3: Verify completed xi functional equation xi(s) == xi(1-s) to 80 dps."""
    dps = 80
    with mpmath.workdps(dps):
        test_points = [
            mpmath.mpc('0.75', '14.13472514173469379045725198356247027078425711569924317568556746'),
            mpmath.mpc('0.2', '35.467'),
            mpmath.mpc('-0.5', '18.2')
        ]
        for s in test_points:
            xi_s = math_core.completed_xi(s, dps=dps)
            xi_1ms = math_core.completed_xi(1 - s, dps=dps)
            assert abs(xi_s - xi_1ms) < mpmath.mpf('1e-70')
