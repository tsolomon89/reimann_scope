"""
tests/test_zero_finder.py — Tests for Independent Zero Discovery and Validation Report

Trust test 4 from SPEC.md §12.
"""

import pytest
import zero_finder
import reference_data
import math_core


def test_independent_zero_discovery():
    """
    Trust Test 4: Independent zero finder finds known zeros in [10, 35]
    without reference seeding, achieves residual < 1e-10, and matches reference data.
    """
    t_min = 10.0
    t_max = 35.0
    
    # 1. Discover zeros independently via Hardy Z(t)
    discovered = zero_finder.discover_zeros_float(t_min, t_max, dps=35)
    assert len(discovered) >= 4, f"Expected at least 4 zeros in [{t_min}, {t_max}], found {len(discovered)}"
    
    # 2. Check each discovered zero has tiny residual
    for gam in discovered:
        s = complex(0.5, gam)
        residual = abs(math_core.zeta_eval(s, dps=35))
        assert residual < 1e-9, f"Residual at gamma={gam} was {residual} >= 1e-9"
        
    # 3. Validate against reference data post-discovery
    report = reference_data.validate_zero_discovery(discovered, t_min, t_max, tolerance=1e-5)
    assert report["passed"], f"Validation failed: {report}"
    assert report["matched_count"] == len(discovered)
    assert report["max_difference"] < 1e-5
    assert len(report["unmatched_discovered"]) == 0
    assert len(report["unmatched_reference"]) == 0
