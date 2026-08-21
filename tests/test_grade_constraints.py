"""
tests/test_grade_constraints.py — Unit tests for bilateral grade constraints and pairwise distances.
"""

import pytest
import mpmath
import math_core
import transcendental


def test_bilateral_defect_identity():
    """Verify |D_K| = 4 sinh^2(K * delta * ln(tau) / 2) at 80 dps."""
    with mpmath.workdps(80):
        tau = math_core.get_tau(dps=80)
        for K in [-3, -2, -1, 1, 2, 3]:
            for delta_val in [-0.05, -0.01, 0.0, 0.01, 0.05]:
                k_mpf = mpmath.mpf(K)
                d_mpf = mpmath.mpf(str(delta_val))
                phi = k_mpf * d_mpf * mpmath.log(tau)
                d_k = (mpmath.power(tau, k_mpf * d_mpf) - 1) * (1 - mpmath.power(tau, -k_mpf * d_mpf))
                expected = 4 * mpmath.power(mpmath.sinh(phi / 2), 2)
                assert abs(abs(d_k) - expected) < mpmath.mpf('1e-70')


def test_cross_height_pairwise_distance():
    """Verify that cross-height pairwise distance computation produces bounded L2 distance."""
    g1 = "14.1347251417346937904572519835624702707842571156992431756855674601"
    g2 = "236.524229665816205802475507955662978689529495212189123700918960988"
    u_grid = ["-0.5", "-0.25", "0.0", "0.25", "0.5"]
    res = transcendental.compute_cross_height_path_distance(g1, g2, u_points=u_grid, dps=50)
    
    assert res["num_u_points"] == len(u_grid)
    l2 = float(res["L_2_distance"])
    linf = float(res["L_infty_distance"])
    assert 0.0 < l2 < 2.0
    assert 0.0 < linf < 2.0


def test_cross_height_self_distance():
    """Verify that distance between a path and itself is zero."""
    g1 = "14.1347251417346937904572519835624702707842571156992431756855674601"
    u_grid = ["-0.5", "0.0", "0.5"]
    res = transcendental.compute_cross_height_path_distance(g1, g1, u_points=u_grid, dps=50)
    l2 = float(res["L_2_distance"])
    linf = float(res["L_infty_distance"])
    assert l2 < 1e-30
    assert linf < 1e-30
