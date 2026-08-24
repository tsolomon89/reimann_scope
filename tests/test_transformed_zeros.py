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


@pytest.mark.slow_numerical
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


@pytest.mark.slow_numerical
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


@pytest.mark.parametrize("k_val", [-2, 0, 2])
def test_transcendental_continuation_bilateral_zeros(k_val):
    """
    Test TranscendentalContinuationTransform across bilateral grades k in {-2, 0, 2}:
    1. Image critical line position is exactly tau^k / 2
    2. Zero mapping rho' = tau^k * rho
    3. Transformed function evaluation Z_tau(tau^k * rho, k) = zeta(rho) = 0
    4. Normalized radial leaf invariance R_tau(tau^k * rho, k) = delta = 0
    """
    dps = 80
    with mpmath.workdps(dps + 10):
        t_obj = transforms.TranscendentalContinuationTransform(grade=k_val)
        
        # 1. Critical line position
        re_crit = zero_finder.get_image_critical_line_re(t_obj, dps=dps)
        expected_re = math_core.get_tau(dps=dps) ** k_val / 2
        assert abs(re_crit - expected_re) < mpmath.mpf('1e-50'), f"Failed for k={k_val}: {re_crit} vs {expected_re}"
        
        # 2. Zero mapping and function evaluation for first zero
        gamma_str = "14.1347251417346937904572519835624702707842571156992431756855674601"
        rho_native = mpmath.mpc(mpmath.mpf('0.5'), math_core.to_mpf(gamma_str, dps=dps))
        
        rho_mapped = t_obj.map_zero_mpc(rho_native, dps=dps)
        expected_mapped = (math_core.get_tau(dps=dps) ** k_val) * rho_native
        assert abs(rho_mapped - expected_mapped) < mpmath.mpf('1e-50')
        
        # Transformed function evaluates to 0
        z_res = t_obj.evaluate_function(rho_mapped, dps=dps)
        assert abs(z_res) < mpmath.mpf('1e-50'), f"Transformed zero residual {z_res} too large for k={k_val}"
        
        # 3. Normalized radial leaf coordinate R_tau(rho_mapped, k) == 0.0
        scale = math_core.get_tau(dps=dps) ** k_val
        r_tau = (rho_mapped.real / scale) - mpmath.mpf('0.5')
        assert abs(r_tau) < mpmath.mpf('1e-50'), f"Radial coordinate {r_tau} != 0 for k={k_val}"
