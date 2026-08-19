"""
tests/test_centrifuge.py — Tests for Radial Centrifuge Identity, Slope, and Vectors E, F

Trust tests 10, 11 from SPEC.md §12 and Vectors E, F from MATH_CONTRACT.md §13.
"""

import pytest
import mpmath
import math_core


def test_centrifuge_modulus_identity():
    """
    Trust Test 10: |q_rho^K| == tau^(K * delta).
    """
    delta = '0.005'
    gamma = '14.134725'
    K = '10.0'
    dps = 50
    
    with mpmath.workdps(dps):
        q_k = math_core.centrifuge_q_k(delta, gamma, K, dps=dps)
        modulus = abs(q_k)
        tau = math_core.get_tau(dps)
        expected_modulus = mpmath.power(tau, mpmath.mpf(K) * mpmath.mpf(delta))
        assert abs(modulus - expected_modulus) < mpmath.mpf('1e-40')


def test_vector_e_radial_centrifuge():
    """
    Vector E: delta = 10^-4, K = 100.
    Expected: log |q_rho^K| == 0.01 * log(tau).
    """
    dps = 50
    with mpmath.workdps(dps):
        log_mod = math_core.centrifuge_log_modulus('0.0001', '100.0', dps=dps)
        tau = math_core.get_tau(dps)
        expected = mpmath.mpf('0.01') * mpmath.log(tau)
        assert abs(log_mod - expected) < mpmath.mpf('1e-40')


def test_vector_f_online_centrifuge():
    """
    Vector F: delta = 0 and arbitrary K => |q_rho^K| == 1.
    """
    dps = 50
    with mpmath.workdps(dps):
        for K_val in ['-100.0', '-1.0', '0.0', '1.0', '50.0', '1000.0']:
            q_k = math_core.centrifuge_q_k('0.0', '14.134725', K_val, dps=dps)
            assert abs(abs(q_k) - 1.0) < mpmath.mpf('1e-40')
            log_mod = math_core.centrifuge_log_modulus('0.0', K_val, dps=dps)
            assert abs(log_mod) < mpmath.mpf('1e-40')


def test_centrifuge_slope():
    """
    Trust Test 11: d/dK log |q_rho^K| == delta * ln(tau).
    """
    delta = '0.002'
    dps = 50
    with mpmath.workdps(dps):
        tau = math_core.get_tau(dps)
        expected_slope = mpmath.mpf(delta) * mpmath.log(tau)
        
        # Finite difference numerical derivative
        K1 = mpmath.mpf('5.0')
        h = mpmath.mpf('1e-15')
        v1 = math_core.centrifuge_log_modulus(delta, str(K1 + h), dps=dps)
        v0 = math_core.centrifuge_log_modulus(delta, str(K1 - h), dps=dps)
        num_slope = (v1 - v0) / (2 * h)
        assert abs(num_slope - expected_slope) < mpmath.mpf('1e-25')
