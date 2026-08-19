"""
Counterexample and Falsification Regression Tests
Tests Davenport-Heilbronn off-line zeros, centrifuge off-line amplification,
and Dirichlet series failure in the critical strip.
"""

import pytest
import mpmath

def davenport_heilbronn(s, dps=40):
    mpmath.mp.dps = dps
    sqrt5 = mpmath.sqrt(5)
    kappa = (mpmath.sqrt(10 - 2*sqrt5) - 2) / (sqrt5 - 1)
    c1 = (1 - mpmath.j * kappa) / 2
    c2 = (1 + mpmath.j * kappa) / 2
    
    s_c = mpmath.mpc(s)
    scale = mpmath.power(5, -s_c)
    z1 = mpmath.hurwitz(s_c, mpmath.mpf('0.2'))
    z2 = mpmath.hurwitz(s_c, mpmath.mpf('0.4'))
    z3 = mpmath.hurwitz(s_c, mpmath.mpf('0.6'))
    z4 = mpmath.hurwitz(s_c, mpmath.mpf('0.8'))
    
    L_chi = scale * (z1 + mpmath.j * z2 - mpmath.j * z3 - z4)
    L_chi_bar = scale * (z1 - mpmath.j * z2 + mpmath.j * z3 - z4)
    return c1 * L_chi + c2 * L_chi_bar

def test_davenport_heilbronn_has_offline_zero():
    """Verify that the Davenport-Heilbronn zeta function has zeros off Re(s)=1/2"""
    mpmath.mp.dps = 40
    # Seed near known root sigma approx 0.808517, t approx 85.699348
    s_guess = mpmath.mpc('0.808517', '85.699348')
    root = mpmath.findroot(lambda s: davenport_heilbronn(s, 40), s_guess)
    residual = abs(davenport_heilbronn(root, 40))
    assert residual < 1e-15
    # Confirm it is strictly off the critical line Re(s) = 0.5
    assert abs(root.real - 0.5) > 0.25

def test_centrifuge_offline_zero_amplification():
    """Verify that off-line zero delta=1e-4 experiences strict amplification |q_rho^100| > 1"""
    mpmath.mp.dps = 50
    tau = 2 * mpmath.pi
    delta = mpmath.mpf('1e-4')
    K = mpmath.mpf('100')
    q_mod = mpmath.power(tau, K * delta)
    expected = mpmath.power(tau, mpmath.mpf('0.01'))
    assert abs(q_mod - expected) < 1e-40
    assert q_mod > 1.01

def test_dirichlet_series_divergence_in_strip():
    """Verify that partial Dirichlet series sum diverges/fails inside the critical strip"""
    mpmath.mp.dps = 50
    s_zero = mpmath.mpc('0.5', '14.13472514173469379045725198356247')
    partial_sum = sum(mpmath.power(n, -s_zero) for n in range(1, 501))
    error = abs(partial_sum) # True zeta(s_zero) == 0
    assert error > 0.1
