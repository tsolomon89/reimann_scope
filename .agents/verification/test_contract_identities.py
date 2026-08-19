"""
Exact Symbolic and Contract Verification Tests (MATH_CONTRACT.md sections 1-13)
Tests Vectors A-F, Inverse Scale Lock, Coordinate Dilations, and Centrifuge relations.
"""

import sympy as sp
import pytest

def test_coordinate_split():
    s = sp.Symbol('s', complex=True)
    delta = sp.Symbol('delta', real=True)
    t = sp.Symbol('t', real=True)
    s_val = sp.Rational(1, 2) + delta + sp.I * t
    z = s_val - sp.Rational(1, 2)
    assert z == delta + sp.I * t
    assert sp.re(s_val) - sp.Rational(1, 2) == delta

def test_vector_a_identity():
    """Vector A: K=0 Identity"""
    tau = 2 * sp.pi
    K = 0
    scale = tau**K
    assert scale == 1

def test_vector_b_origin_dilation():
    """Vector B: K=1 Origin Coordinate Dilation"""
    tau = 2 * sp.pi
    K = 1
    s = sp.Symbol('s', complex=True)
    rho = sp.Symbol('rho', complex=True)
    t = sp.Symbol('t', real=True)
    
    # s' = tau^K * s
    s_prime = tau**K * s
    # Image critical line Re(s') = tau^K / 2 = pi
    crit_s = sp.Rational(1, 2) + sp.I * t
    image_crit_s = s_prime.subs(s, crit_s)
    assert sp.re(image_crit_s) == sp.pi
    # Zero map: rho' = tau * rho
    assert s_prime.subs(s, rho) == 2 * sp.pi * rho

def test_vector_c_centered_dilation():
    """Vector C: K=1 Centered Coordinate Dilation"""
    tau = 2 * sp.pi
    K = 1
    s = sp.Symbol('s', complex=True)
    rho = sp.Symbol('rho', complex=True)
    t = sp.Symbol('t', real=True)
    
    # s' = 1/2 + tau^K * (s - 1/2)
    s_prime = sp.Rational(1, 2) + tau**K * (s - sp.Rational(1, 2))
    # Image critical line remains Re(s') = 1/2
    crit_s = sp.Rational(1, 2) + sp.I * t
    image_crit_s = s_prime.subs(s, crit_s)
    assert sp.re(image_crit_s) == sp.Rational(1, 2)
    # Zero map: rho' = 1/2 + tau * (rho - 1/2)
    assert s_prime.subs(s, rho) == sp.Rational(1, 2) + 2 * sp.pi * (rho - sp.Rational(1, 2))

def test_vector_d_inverse_kernel_lock():
    """Vector D: Inverse Kernel Lock AB = 1, C=D=0"""
    s = sp.Symbol('s', complex=True)
    A = sp.Symbol('A', positive=True)
    B = 1 / A
    n = sp.Symbol('n', positive=True, integer=True)
    
    # Exponent pairing (B*s)*(A*log(n)) == s*log(n)
    pairing = (B * s) * (A * sp.log(n))
    assert sp.simplify(pairing - s * sp.log(n)) == 0

def test_kernel_zero_mapping():
    """General Kernel Zero Map: A*(B*s + D) = rho ==> s = (rho/A - D) / B"""
    s, A, B, C, D, rho = sp.symbols('s A B C D rho', complex=True)
    sol = sp.solve(sp.Eq(A * (B * s + D), rho), s)[0]
    expected = (rho / A - D) / B
    assert sp.simplify(sol - expected) == 0

def test_vector_e_radial_centrifuge():
    """Vector E: delta = 1e-4, K = 100 ==> log|q_rho^K| = 0.01 * log(tau)"""
    tau = 2 * sp.pi
    delta = sp.Rational(1, 10000)
    K = 100
    log_mod_q = K * delta * sp.log(tau)
    assert log_mod_q == sp.Rational(1, 100) * sp.log(2 * sp.pi)

def test_vector_f_online_centrifuge():
    """Vector F: delta = 0 ==> |q_rho^K| = 1, log|q_rho^K| = 0"""
    tau = 2 * sp.pi
    K = sp.Symbol('K', real=True)
    delta = 0
    log_mod_q = K * delta * sp.log(tau)
    assert log_mod_q == 0

def test_centrifuge_derivative_slope():
    """Centrifuge derivative: d/dK [ log |q_rho^K| ] = delta * log(tau)"""
    tau = 2 * sp.pi
    K = sp.Symbol('K', real=True)
    delta = sp.Symbol('delta', real=True)
    log_mod_q = K * delta * sp.log(tau)
    d_log_mod_dK = sp.diff(log_mod_q, K)
    assert d_log_mod_dK == delta * sp.log(2 * sp.pi)
