"""
tests/test_zero_worldlines.py

Unit tests for zero worldlines, critical surfaces, and radial leaf invariance:
- Worldline mapping: s_rho(k) = tau^k * rho
- Critical surface: sigma_c(k) = tau^k / 2
- Radial leaf invariance: R_tau(s_rho(k), k) == delta identically for all k
- Absolute radial defect: d_tau(s_rho(k), k) == tau^k * delta
"""

import mpmath
import pytest

import math_core
import transcendental


def test_zero_worldline_online():
    """Verify on-line zero worldline remains on the critical surface."""
    with mpmath.workdps(80):
        rho = mpmath.mpc('0.5', '14.13472514173469379045725198356247027078425711569924317568556746')
        
        for k in [-2, -1, 0, 1, 2, "0.5", "-1.5"]:
            g = transcendental.parse_grade(k)
            s_world = transcendental.zero_worldline_point(rho, g, delta="0.0", dps=80)
            sigma_c = transcendental.critical_surface_sigma(g, dps=80)
            
            # Real part must match critical surface exactly
            assert abs(s_world.real - sigma_c) < 1e-75
            
            # Normalized radial leaf must be 0
            r_leaf = transcendental.normalized_radial_leaf(s_world, g, dps=80)
            assert abs(r_leaf) < 1e-75
            
            # Absolute defect must be 0
            abs_defect = transcendental.absolute_radial_defect(s_world, g, dps=80)
            assert abs(abs_defect) < 1e-75
            
            # Extended zeta evaluates to zero on the worldline of a zero
            z_val = transcendental.evaluate_extended_zeta(s_world, grade=g, dps=80)
            assert abs(z_val) < 1e-35


def test_zero_worldline_offline_invariance():
    """Verify off-line zero worldline maintains constant normalized radial leaf delta."""
    with mpmath.workdps(80):
        rho = mpmath.mpc('0.5', '14.13472514173469379045725198356247027078425711569924317568556746')
        delta_test = mpmath.mpf('0.123456789')
        
        for k in [-3, -1, 0, 1, 3, "0.75", "-2.25"]:
            g = transcendental.parse_grade(k)
            s_world = transcendental.zero_worldline_point(rho, g, delta=delta_test, dps=80)
            
            # Normalized radial leaf must equal delta_test identically
            r_leaf = transcendental.normalized_radial_leaf(s_world, g, dps=80)
            assert abs(r_leaf - delta_test) < 1e-75
            
            # Absolute defect must equal tau^k * delta_test
            scale_A = g.numeric_scale(dps=80)
            abs_defect = transcendental.absolute_radial_defect(s_world, g, dps=80)
            assert abs(abs_defect - scale_A * delta_test) < 1e-75
