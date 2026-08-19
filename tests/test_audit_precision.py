"""
tests/test_audit_precision.py — Tests for Precision Boundaries and Audit Explicit Formula Fidelity

Tests:
- Preservation of decimal strings without binary float downcast
- Remainder integral exactness: sum_{k=1}^infty E_1(2k ln x) vs numerical quadrature
- High-precision audit evaluation of Riemann explicit formula pi_N(x)
- Preview vs Audit separation
"""

import pytest
import mpmath
import numpy as np

import math_core
import converter
import transforms
import reference_data


def test_remainder_integral_series_vs_quadrature():
    """
    Verify that the exponential integral series sum_{k=1}^infty E_1(2k ln x)
    agrees exactly with numerical quadrature int_x^infty du / [u(u^2 - 1) ln u]
    to high precision (60+ digits).
    """
    dps = 60
    with mpmath.workdps(dps + 15):
        for x_val in ["2.0", "3.5", "10.0", "50.0"]:
            x_mpf = mpmath.mpf(x_val)
            
            # 1. Exact series sum
            series_val = converter.riemann_remainder_integral_audit(x_mpf, dps=dps)
            
            # 2. Direct numerical quadrature of int_x^infty du / [u(u^2-1) ln u]
            # Change of variables u = x + t / (1 - t) for t in [0, 1) or mpmath.quad
            integrand = lambda u: 1 / (u * (u**2 - 1) * mpmath.log(u))
            quad_val = mpmath.quad(integrand, [x_mpf, mpmath.inf])
            
            diff = abs(series_val - quad_val)
            assert diff < mpmath.mpf("1e-45"), f"Remainder mismatch at x={x_val}: {diff}"


def test_remainder_integral_preview_vs_audit():
    """Verify that preview float and audit mpmath remainder integrals agree to float precision."""
    for x in [2.0, 5.0, 15.0, 30.0]:
        prev_val = converter.riemann_remainder_integral_preview(x)
        aud_val = float(converter.riemann_remainder_integral_audit(str(x), dps=35))
        assert abs(prev_val - aud_val) < 1e-12


def test_decimal_string_preservation_in_transforms():
    """
    Verify that high-precision decimal strings passed to transform constructors
    are preserved without binary-float downcast in audit calculations.
    """
    dps = 80
    high_prec_k = "1.123456789012345678901234567890123456789012345678901234567890"
    t_orig = transforms.OriginCoordinateDilation(k=high_prec_k)
    
    assert t_orig.k_str == high_prec_k
    
    with mpmath.workdps(dps + 10):
        # Audit zero mapping uses exact k_str
        rho_str = "0.5 + 14.13472514173469379045725198356247027078425711569924317568556746j"
        rho_mpc = math_core.to_mpc(rho_str, dps=dps)
        
        mapped_rho = t_orig.map_zero_mpc(rho_mpc, dps=dps)
        
        tau = math_core.get_tau(dps=dps)
        expected_scale = mpmath.power(tau, mpmath.mpf(high_prec_k))
        expected_mapped = expected_scale * rho_mpc
        
        assert abs(mapped_rho - expected_mapped) < mpmath.mpf("1e-70")



def test_explicit_formula_pi_audit_vs_prime_truth():
    """
    Verify that high-precision audit explicit formula pi_N(x) reconstructs
    prime staircase approximating prime_pi(x) over [2, 30].
    """
    dps = 50
    ref_zeros_str = reference_data.load_reference_zeros()[:25]
    
    # At x = 20: true pi(20) = 8
    pi_audit_20 = converter.riemann_explicit_pi_audit("20.0", ref_zeros_str, dps=dps)
    true_pi_20 = reference_data.prime_pi(20.0)
    
    assert true_pi_20 == 8
    assert abs(pi_audit_20 - 8) < 1.5
