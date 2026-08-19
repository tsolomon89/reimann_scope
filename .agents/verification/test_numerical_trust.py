"""
Numerical Trust and High-Precision Verification Tests
Uses python-flint (Arb ball arithmetic) and mpmath to test zeta values, Schwarz reflection,
and the completed zeta functional equation at 80+ decimal digits.
"""

import pytest
import mpmath

try:
    import flint
    from flint import acb, arb
    HAS_FLINT = True
except ImportError:
    HAS_FLINT = False

def completed_xi(s, ctx):
    pi = ctx.pi
    term1 = ctx.mpf('0.5') * s * (s - 1)
    term2 = ctx.power(pi, -s / 2)
    term3 = ctx.gamma(s / 2)
    term4 = ctx.zeta(s)
    return term1 * term2 * term3 * term4

def test_schwarz_reflection_high_precision():
    """Verify Schwarz reflection: zeta(conj(s)) == conj(zeta(s)) to 80 dps"""
    mpmath.mp.dps = 80
    s = mpmath.mpc('0.75', '14.134725141734693790457251983562470270784257115699243175685567460149963429809')
    z1 = mpmath.zeta(mpmath.conj(s))
    z2 = mpmath.conj(mpmath.zeta(s))
    assert abs(z1 - z2) < mpmath.mpf('1e-75')

def test_functional_equation_high_precision():
    """Verify completed xi functional equation: xi(s) == xi(1-s) to 80 dps"""
    mpmath.mp.dps = 80
    s = mpmath.mpc('0.75', '14.134725141734693790457251983562470270784257115699243175685567460149963429809')
    xi_s = completed_xi(s, mpmath.mp)
    xi_1_minus_s = completed_xi(1 - s, mpmath.mp)
    assert abs(xi_s - xi_1_minus_s) < mpmath.mpf('1e-75')

def test_first_zero_residual():
    """Verify known first nontrivial zero gamma_1 residual to 80 dps"""
    mpmath.mp.dps = 80
    s_zero = mpmath.mpc('0.5', '14.134725141734693790457251983562470270784257115699243175685567460149963429809')
    z_val = mpmath.zeta(s_zero)
    assert abs(z_val) < mpmath.mpf('1e-75')

def test_flint_arb_certified_enclosure():
    """Verify python-flint Arb certified ball enclosure contains zero"""
    if not HAS_FLINT:
        pytest.skip("python-flint not installed")
    flint.ctx.dps = 80
    s = acb("0.5", "14.134725141734693790457251983562470270784257115699243175685567460149963429809256764949010393171561012779238324")
    z = s.zeta()
    assert z.contains(0)
