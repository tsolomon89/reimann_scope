"""
tests/test_certification.py — Rigorous mathematical certificate & verifier test suite.
"""

import os
import json
import pytest
import certification
import math_core
from scripts.verify_certificates import verify_all_certificates


def test_certify_and_verify_single_zero():
    """Verify zero certification on the first Riemann zero."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
        
    cert = certification.certify_zero(1, dps=50)
    assert cert["certificate_type"] == "zero_isolation_and_simplicity"
    assert cert["zero_index"] == 1
    assert cert["status"] == "simple_zero_certified"
    assert cert["derivative_enclosure"]["excludes_zero"] is True
    
    is_valid, msg = certification.verify_certificate(cert)
    assert is_valid, f"Certificate verification failed: {msg}"


def test_certify_and_verify_block():
    """Verify block certification on low validation block."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
        
    zero_indices = list(range(1, 11))
    cert, zero_certs = certification.certify_block("low_validation", zero_indices, dps=50)
    assert cert["certificate_type"] == "complete_block_certificate"
    assert cert["zero_count"] == 10
    assert len(zero_certs) == 10
    
    is_valid, msg = certification.verify_certificate(cert)
    assert is_valid, f"Block certificate verification failed: {msg}"


def test_certify_and_verify_worldline():
    """Verify worldline certification for actual zero (delta=0) and synthetic leaf (delta=0.05)."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
        
    z_cert = certification.certify_zero(1, dps=50)
    
    # Actual zero worldline
    wl_actual = certification.certify_worldline(z_cert, grade=1, delta=0.0, dps=50)
    assert wl_actual["certificate_type"] == "worldline_certificate"
    assert wl_actual["claim_type"] == "actual_zero_worldline"
    is_valid, msg = certification.verify_certificate(wl_actual)
    assert is_valid, f"Actual worldline verification failed: {msg}"
    
    # Synthetic leaf
    wl_synth = certification.certify_worldline(z_cert, grade=2, delta=0.05, dps=50)
    assert wl_synth["certificate_type"] == "worldline_certificate"
    assert wl_synth["claim_type"] == "synthetic_radial_leaf"
    is_valid, msg = certification.verify_certificate(wl_synth)
    assert is_valid, f"Synthetic worldline verification failed: {msg}"


def test_tampered_certificate_fails_closed():
    """Verify that tampering with any certificate data causes verification failure."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
        
    cert = certification.certify_zero(1, dps=50)
    
    # Tamper with midpoint ordinate
    cert_tampered = dict(cert)
    cert_tampered["enclosure"] = dict(cert["enclosure"])
    cert_tampered["enclosure"]["imag_mid"] = "14.99999999"
    
    is_valid, msg = certification.verify_certificate(cert_tampered)
    assert not is_valid
    assert any("Hash mismatch" in m for m in msg)


def test_all_persisted_certificates_pass_verification():
    """Run full verification across all certificates in data/certificates/."""
    passed, failed, errors = verify_all_certificates()
    assert failed == 0, f"Some certificates failed verification: {errors}"
    assert passed >= 125, f"Expected at least 125 certified artifacts, found {passed}"


def test_isolation_interval_excludes_adjacent_zeros():
    """Verify that isolation interval rigorously isolates the indexed zero and excludes adjacent zeros."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
        
    cert2 = certification.certify_zero(2, dps=50)
    lower_bound = certification._parse_arb_str_to_float(cert2["isolation_interval"]["lower_bound"])
    upper_bound = certification._parse_arb_str_to_float(cert2["isolation_interval"]["upper_bound"])
    z2_im = certification._parse_arb_str_to_float(cert2["enclosure"]["imag_mid"])
    
    cert1 = certification.certify_zero(1, dps=50)
    z1_im = certification._parse_arb_str_to_float(cert1["enclosure"]["imag_mid"])
    
    cert3 = certification.certify_zero(3, dps=50)
    z3_im = certification._parse_arb_str_to_float(cert3["enclosure"]["imag_mid"])
    
    # Check strict isolation ordering: z1 < lower_iso < z2 < upper_iso < z3
    assert z1_im < lower_bound < z2_im < upper_bound < z3_im, (
        f"Isolation bounds failed: {z1_im} < {lower_bound} < {z2_im} < {upper_bound} < {z3_im}"
    )


def test_simplicity_enclosure_excludes_zero_and_rejects_zero_in_derivative():
    """Verify that 0 ∉ ζ'(B_n) is required for simplicity certification and fails closed otherwise."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
        
    cert = certification.certify_zero(1, dps=50)
    assert cert["derivative_enclosure"]["excludes_zero"] is True
    assert certification._parse_arb_str_to_float(cert["derivative_enclosure"]["abs_lower"]) > 0.0
    
    # Tamper derivative enclosure to enclose zero
    cert_tampered = dict(cert)
    cert_tampered["derivative_enclosure"] = dict(cert["derivative_enclosure"])
    cert_tampered["derivative_enclosure"]["excludes_zero"] = False
    cert_tampered["derivative_enclosure"]["abs_lower"] = "0.0"
    cert_tampered["certificate_hash"] = certification._sha256_canonical(cert_tampered)
    
    is_valid, msg = certification.verify_certificate(cert_tampered)
    assert not is_valid
    assert any("derivative enclosure does not exclude zero" in m for m in msg)



def test_block_certification_rejects_gaps_and_hash_discrepancies():
    """Verify that block certification enforces strict consecutiveness and complete count."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
        
    # Non-consecutive indices must raise ValueError
    with pytest.raises(ValueError, match="Block indices must be consecutive"):
        certification.certify_block("broken_block", [1, 2, 4], dps=50)
        
    # Discrepancy in constituent hashes must fail verification
    cert, _ = certification.certify_block("low_validation", list(range(1, 11)), dps=50)
    cert_tampered = dict(cert)
    cert_tampered["constituent_zero_hashes"] = cert["constituent_zero_hashes"][:5]  # Only 5 hashes instead of 10
    cert_tampered["certificate_hash"] = certification._sha256_canonical(cert_tampered)
    
    is_valid, msg = certification.verify_certificate(cert_tampered)
    assert not is_valid
    assert any("does not match declared zero_count" in m for m in msg)


def test_authoritative_certification_path_prohibits_float_downcasts():
    """Verify that all ball midpoints and radii in certificates are stored as exact strings, not Python floats."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
        
    cert = certification.certify_zero(1, dps=50)
    enc = cert["enclosure"]
    assert isinstance(enc["real_mid"], str)
    assert isinstance(enc["real_rad"], str)
    assert isinstance(enc["imag_mid"], str)
    assert isinstance(enc["imag_rad"], str)
    
    iso = cert["isolation_interval"]
    assert isinstance(iso["lower_bound"], str)
    assert isinstance(iso["upper_bound"], str)
    
    deriv = cert["derivative_enclosure"]
    assert isinstance(deriv["real_mid"], str)
    assert isinstance(deriv["real_rad"], str)
    assert isinstance(deriv["imag_mid"], str)
    assert isinstance(deriv["imag_rad"], str)
    assert isinstance(deriv["abs_lower"], str)

