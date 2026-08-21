"""
tests/test_transcendental.py

Unit tests for transcendental.py:
- Grade taxonomy & properties (IntegerTauGrade, RationalTauGrade, ContinuousGrade, GenericScale)
- Invariant scale inversion: scale(inverse) * scale(self) == 1
- Native analytic slice: Z_tau(s, 0) == zeta(s)
- Extended completed xi evaluation: X_tau(s, 0) == xi(s)
- Grade parsing and serialization
"""

import fractions
import mpmath
import pytest

import math_core
import transcendental


def test_integer_tau_grade():
    with mpmath.workdps(80):
        tau = math_core.get_tau(dps=80)
        
        g0 = transcendental.IntegerTauGrade(K=0)
        assert g0.semantic_type == "integer_tau"
        assert g0.symbolic_expression() == "tau^0"
        assert abs(g0.numeric_scale(dps=80) - 1) < 1e-75
        
        g1 = transcendental.IntegerTauGrade(K=1)
        assert g1.symbolic_expression() == "tau"
        assert abs(g1.numeric_scale(dps=80) - tau) < 1e-75
        
        g2 = transcendental.IntegerTauGrade(K=2)
        assert g2.symbolic_expression() == "tau^2"
        assert abs(g2.numeric_scale(dps=80) - tau**2) < 1e-75
        
        g_neg = transcendental.IntegerTauGrade(K=-3)
        assert g_neg.symbolic_expression() == "tau^(-3)"
        assert abs(g_neg.numeric_scale(dps=80) - (1 / tau**3)) < 1e-75
        
        inv_g = g_neg.inverse_grade()
        assert inv_g.K == 3
        assert abs(g_neg.numeric_scale(dps=80) * inv_g.numeric_scale(dps=80) - 1) < 1e-75


def test_rational_tau_grade():
    with mpmath.workdps(80):
        tau = math_core.get_tau(dps=80)
        
        g_half = transcendental.RationalTauGrade(fractions.Fraction(1, 2))
        assert g_half.semantic_type == "rational_tau"
        assert g_half.symbolic_expression() == "tau^(1/2)"
        assert abs(g_half.numeric_scale(dps=80) - mpmath.sqrt(tau)) < 1e-75
        
        g_neg_3_4 = transcendental.RationalTauGrade.from_str("-3/4")
        assert g_neg_3_4.symbolic_expression() == "tau^(-3/4)"
        assert abs(g_neg_3_4.numeric_scale(dps=80) - mpmath.power(tau, mpmath.mpf('-0.75'))) < 1e-75
        
        inv_g = g_neg_3_4.inverse_grade()
        assert inv_g.fraction == fractions.Fraction(3, 4)
        assert abs(g_neg_3_4.numeric_scale(dps=80) * inv_g.numeric_scale(dps=80) - 1) < 1e-75


def test_continuous_grade():
    with mpmath.workdps(80):
        tau = math_core.get_tau(dps=80)
        
        gc = transcendental.ContinuousGrade.from_value("1.25")
        assert gc.semantic_type == "continuous_tau"
        assert gc.symbolic_expression() == "tau^(1.25)"
        assert abs(gc.numeric_scale(dps=80) - mpmath.power(tau, mpmath.mpf('1.25'))) < 1e-75
        
        inv_gc = gc.inverse_grade()
        assert abs(gc.numeric_scale(dps=80) * inv_gc.numeric_scale(dps=80) - 1) < 1e-70


def test_generic_scale():
    with mpmath.workdps(80):
        gs = transcendental.GenericScale(A_str="3.14159265", base_str="10")
        assert gs.semantic_type == "generic_scale"
        assert abs(gs.numeric_scale(dps=80) - mpmath.mpf("3.14159265")) < 1e-75
        
        inv_gs = gs.inverse_grade()
        assert abs(gs.numeric_scale(dps=80) * inv_gs.numeric_scale(dps=80) - 1) < 1e-70


def test_grade_parser():
    g_int = transcendental.parse_grade("3")
    assert isinstance(g_int, transcendental.IntegerTauGrade) and g_int.K == 3
    
    g_rat = transcendental.parse_grade("3/5")
    assert isinstance(g_rat, transcendental.RationalTauGrade) and g_rat.fraction == fractions.Fraction(3, 5)
    
    g_cont = transcendental.parse_grade("2.71828")
    assert isinstance(g_cont, transcendental.ContinuousGrade)


def test_native_slice_identity():
    """Verify Z_tau(s, 0) == zeta(s) to authoritative 80 dps precision."""
    with mpmath.workdps(80):
        test_points = [
            mpmath.mpc('0.5', '14.13472514173469379045725198356247027078425711569924317568556746'),
            mpmath.mpc('2.0', '3.5'),
            mpmath.mpc('0.75', '45.0'),
            mpmath.mpc('-1.5', '12.0')
        ]
        for s in test_points:
            z_ext = transcendental.evaluate_extended_zeta(s, grade=0, dps=80)
            z_std = math_core.zeta_eval(s, dps=80)
            assert abs(z_ext - z_std) < 1e-75
            
            xi_ext = transcendental.evaluate_extended_xi(s, grade=0, dps=80)
            xi_std = math_core.xi_eval(s, dps=80)
            assert abs(xi_ext - xi_std) < 1e-75
