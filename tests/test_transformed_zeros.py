"""
tests/test_transformed_zeros.py — Tests for Independent Discovery of Transformed Zeros

Tests:
- Independent discovery of zeros of transformed functions f_K(s) along their image critical line
- Verification that discovered zeros match algebraically predicted zero positions
- Zero-finding semantics without proof claims
"""

import pytest
import mpmath

import math_core
import transforms
import zero_finder
import reference_data


def test_independent_transformed_zero_discovery_origin_dilation():
    """
    Test that transformed zeros of f_K(s') = zeta(s'/tau^K) for K=0.5 are
    independently discovered along Re(s') = tau^0.5 / 2, and agree with predicted zeros.
    """
    dps = 35
    t_obj = transforms.OriginCoordinateDilation(k=0.5)
    
    # 1. Independently discover zeros along the image critical line
    discovered = zero_finder.discover_transformed_zeros(
        t_obj, t_min=30.0, t_max=60.0, dps=dps, max_residual=1e-7, scan_step=0.08
    )
    assert len(discovered) >= 2, f"Expected at least 2 discovered zeros, found {len(discovered)}"
    
    # 2. Check each discovered root has tiny residual under f_K
    for s_0 in discovered:
        res = abs(t_obj.evaluate_function(s_0, dps=dps))
        assert res < 1e-7, f"Residual at {s_0} was {res}"
        
    # 3. Compare with predicted mapped locations of known baseline zeros in range
    ref_zeros_str = reference_data.load_reference_zeros()[:10]
    comparison = zero_finder.compare_discovered_vs_predicted_zeros(
        t_obj, discovered, ref_zeros_str, tolerance=1e-4, dps=dps
    )
    assert comparison["matched_count"] > 0
    assert float(comparison["max_difference"]) < 1e-4


def test_independent_transformed_zero_discovery_centered_dilation():
    """
    Test independent discovery for centered coordinate dilation s' = 1/2 + tau^K(s-1/2) for K=0.25.
    Image critical line remains Re(s') = 1/2.
    """
    dps = 35
    t_obj = transforms.CenteredCoordinateDilation(k=0.25)
    
    discovered = zero_finder.discover_transformed_zeros(
        t_obj, t_min=20.0, t_max=45.0, dps=dps, max_residual=1e-7, scan_step=0.08
    )
    assert len(discovered) >= 2
    
    ref_zeros_str = reference_data.load_reference_zeros()[:10]
    comparison = zero_finder.compare_discovered_vs_predicted_zeros(
        t_obj, discovered, ref_zeros_str, tolerance=1e-4, dps=dps
    )
    assert comparison["matched_count"] > 0
    assert float(comparison["max_difference"]) < 1e-4
