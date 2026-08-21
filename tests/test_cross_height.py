"""
tests/test_cross_height.py

Unit tests for Cross-Height Path Coherence Engine:
- Mean zero spacing scale Delta_n = tau / log(gamma_n / tau)
- Exact properties of derivative normalized path P_n(u):
  P_n(0) == 0, P_n'(0) == 1
- Taylor shape coefficient extraction c_{2,n}, c_{3,n}
- Simple zero validation & non-vanishing derivative check
- Pairwise path distance computation
"""

import mpmath
import pytest

import math_core
import transcendental
import reference_data


def test_mean_zero_spacing():
    with mpmath.workdps(80):
        tau = math_core.get_tau(dps=80)
        gamma = mpmath.mpf('14.13472514173469379045725198356247027078425711569924317568556746')
        
        delta_n = transcendental.mean_zero_spacing_delta(gamma, dps=80)
        expected = tau / mpmath.log(gamma / tau)
        assert abs(delta_n - expected) < 1e-75
        assert delta_n > 0


def test_derivative_normalized_path_origin():
    """Verify P_n(0) == 0 and numerical derivative P_n'(0) == 1."""
    with mpmath.workdps(80):
        gamma = "14.13472514173469379045725198356247027078425711569924317568556746"
        
        # P_n(0)
        p0_info = transcendental.evaluate_derivative_normalized_path(gamma, u="0.0", dps=80)
        p0_val = p0_info["P_n_mpc"]
        assert abs(p0_val) < 1e-35
        
        # Estimate P_n'(0) via symmetric difference at eps = 1e-20
        eps = mpmath.mpf('1e-20')
        p_plus = transcendental.evaluate_derivative_normalized_path(gamma, u=eps, dps=80)["P_n_mpc"]
        p_minus = transcendental.evaluate_derivative_normalized_path(gamma, u=-eps, dps=80)["P_n_mpc"]
        
        deriv_est = (p_plus - p_minus) / (2 * eps)
        assert abs(deriv_est - 1) < 1e-15


def test_taylor_shape_coefficients():
    """Verify Taylor shape coefficients are well-defined and match quadratic approximation."""
    with mpmath.workdps(80):
        gamma = "14.13472514173469379045725198356247027078425711569924317568556746"
        coeffs = transcendental.extract_taylor_shape_coefficients(gamma, dps=80)
        
        c2 = coeffs["c2_mpc"]
        c3 = coeffs["c3_mpc"]
        assert mpmath.isfinite(c2)
        assert mpmath.isfinite(c3)
        
        # Compare P_n(u) with u + c2*u^2 for small u
        u_small = mpmath.mpf('1e-5')
        p_val = transcendental.evaluate_derivative_normalized_path(gamma, u=u_small, dps=80)["P_n_mpc"]
        p_taylor = u_small + c2 * (u_small**2) + c3 * (u_small**3)
        assert abs(p_val - p_taylor) < 1e-18


def test_simple_zero_verification():
    """Verify verify_simple_zero confirms simple zeros from canonical blocks."""
    for blk_name in reference_data.get_block_names():
        blk = reference_data.get_zero_block(blk_name)
        for ord_str in blk["ordinates"]:
            is_simple, res, zp = reference_data.verify_simple_zero(ord_str, dps=80)
            assert is_simple is True
            assert res < 1e-20
            assert abs(zp) > 1e-10


def test_cross_height_path_distance():
    """Verify path distance between two distinct zeros is well-defined and positive."""
    g1 = "14.13472514173469379045725198356247027078425711569924317568556746"
    g2 = "21.02203963877155499262847959389690277733434052408000778648358249"
    
    dist_info = transcendental.compute_cross_height_path_distance(g1, g2, dps=60)
    l_inf = mpmath.mpf(dist_info["L_infty_distance"])
    l_2 = mpmath.mpf(dist_info["L_2_distance"])
    
    assert l_inf > 0
    assert l_2 > 0
    assert l_2 <= l_inf + 1e-10
