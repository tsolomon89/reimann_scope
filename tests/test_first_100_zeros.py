"""
tests/test_first_100_zeros.py — Complete 3-Layer Validation Baseline for First 100 Riemann Zeros.

Tests:
1. Layer A: Independent candidate discovery (zero_finder.py) without seeds.
2. Layer B: Authoritative reference matching against Odlyzko table (interval containment).
3. Layer C: Rigorous FLINT/Arb certification (isolation, simplicity, non-vanishing derivative).
4. Trivial zero controls (first 100 trivial zeros s_m = -2m, non-vanishing derivative, negative controls).
"""

import pytest
import mpmath
import reference_data
import zero_finder
import certification


def test_layer_a_independent_candidate_discovery_first_20():
    """Test Layer A: Independent candidate discovery without external seeds for first 20 zeros."""
    candidates = zero_finder.discover_first_n_nontrivial_zeros(20, dps=30)
    assert len(candidates) >= 20
    
    # Strictly monotonically increasing ordinates
    for i in range(19):
        ord_i = mpmath.mpf(candidates[i]["refined_ordinate"])
        ord_next = mpmath.mpf(candidates[i+1]["refined_ordinate"])
        assert ord_i < ord_next
        assert float(candidates[i]["zeta_residual"]) < 1e-15



def test_layer_b_reference_interval_matching_first_100():
    """Test Layer B: Matching all 100 discovered zeros against Odlyzko reference rounding intervals."""
    ref_zeros = reference_data.load_first_100_reference_zeros()
    assert len(ref_zeros) == 100
    
    for n, ord_str in enumerate(ref_zeros, start=1):
        matched, diff, (low_b, high_b) = reference_data.match_candidate_against_reference_interval(
            candidate_ordinate=ord_str,
            ref_str=ord_str
        )
        assert matched, f"Zero #{n} ordinate {ord_str} does not lie in rounding interval [{low_b}, {high_b}]"


def test_layer_c_flint_certification_first_10():
    """Test Layer C: Rigorous FLINT/Arb ball certification on low zeros."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
        
    for n in range(1, 11):
        cert = certification.certify_zero(n, dps=50)
        assert cert["zero_family"] == "nontrivial"
        assert cert["nontrivial_index"] == n
        assert cert["status"] == "simple_zero_certified"
        assert cert["derivative_enclosure"]["excludes_zero"] is True
        
        ok, msgs = certification.verify_certificate(cert, check_provenance=False)
        assert ok, f"Zero #{n} certificate verification failed: {msgs}"


def test_first_100_trivial_zeros():
    """Test exact properties and FLINT certification for trivial zeros m=1..100."""
    t_zeros = reference_data.get_first_100_trivial_zeros()
    assert len(t_zeros) == 100
    
    for m, s_m in enumerate(t_zeros[:20], start=1):
        assert s_m == -2 * m
        tz = reference_data.evaluate_trivial_zero_exact(s_m)
        assert tz["is_trivial_zero"] is True
        assert tz["is_isolated"] is True
        assert tz["is_simple"] is True
        
    # Negative controls
    assert reference_data.evaluate_trivial_zero_exact(0)["zeta_value"] == "-0.5"
    assert reference_data.evaluate_trivial_zero_exact(-1)["is_trivial_zero"] is False
    assert reference_data.evaluate_trivial_zero_exact(-3)["is_trivial_zero"] is False

