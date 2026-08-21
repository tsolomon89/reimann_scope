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
