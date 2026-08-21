"""
tests/test_compression.py

Unit tests for target height compression/expansion:
- derive_compression_grade: computes k = log(target / source) / log(tau)
- verifies actual mapped height == target height
- verifies nearest integer K and integer scale ratio
"""

import mpmath
import pytest

import math_core
import transcendental


def test_derive_compression_grade():
    with mpmath.workdps(80):
        tau = math_core.get_tau(dps=80)
        
        # Test 1: exact integer grade power
        src = mpmath.mpf('14.13472514173469379045725198356247027078425711569924317568556746')
        tgt_exact = src * (tau**2)
        
        comp_info = transcendental.derive_compression_grade(src, tgt_exact, dps=80)
        assert abs(comp_info["continuous_k_val"] - 2) < 1e-75
        assert comp_info["nearest_integer_K"] == 2
        assert abs(mpmath.mpf(comp_info["actual_mapped_height"]) - tgt_exact) < 1e-75
        
        # Test 2: compression (negative k)
        tgt_small = src / tau
        comp_info_neg = transcendental.derive_compression_grade(src, tgt_small, dps=80)
        assert abs(comp_info_neg["continuous_k_val"] - (-1)) < 1e-75
        assert comp_info_neg["nearest_integer_K"] == -1
        
        # Test 3: arbitrary continuous target
        tgt_arb = mpmath.mpf('100.0')
        comp_arb = transcendental.derive_compression_grade(src, tgt_arb, dps=80)
        assert abs(mpmath.mpf(comp_arb["actual_mapped_height"]) - 100.0) < 1e-75
