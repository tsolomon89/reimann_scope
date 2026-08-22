"""
tests/test_certification.py — Rigorous mathematical certificate & adversarial verifier test suite.
Tests legitimate mathematical certification, full artifact verification, and rejection of all 14 adversarial forged certificate variants.
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
    assert cert["status"] == "complete_block_certified"
    
    cert_store = {zc["certificate_hash"]: zc for zc in zero_certs}
    is_valid, msg = certification.verify_certificate(cert, cert_store=cert_store)
    assert is_valid, f"Block certificate verification failed: {msg}"


def test_certify_and_verify_worldline():
    """Verify worldline certification for actual zero (delta=0) and synthetic leaf (delta=0.05)."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
        
    z_cert = certification.certify_zero(1, dps=50)
    cert_store = {z_cert["certificate_hash"]: z_cert}
    
    # Actual zero worldline
    wl_actual = certification.certify_worldline(z_cert, grade=1, delta="0.0", dps=50)
    assert wl_actual["certificate_type"] == "worldline_certificate"
    assert wl_actual["claim_type"] == "actual_zero_worldline"
    is_valid, msg = certification.verify_certificate(wl_actual, cert_store=cert_store)
    assert is_valid, f"Actual worldline verification failed: {msg}"
    
    # Synthetic leaf
    wl_synth = certification.certify_worldline(z_cert, grade=2, delta="0.05", dps=50)
    assert wl_synth["certificate_type"] == "worldline_certificate"
    assert wl_synth["claim_type"] == "synthetic_radial_leaf"
    is_valid, msg = certification.verify_certificate(wl_synth, cert_store=cert_store)
    assert is_valid, f"Synthetic worldline verification failed: {msg}"


def test_all_persisted_certificates_pass_verification():
    """Run full verification across all certificates in data/certificates/."""
    passed, failed, errors = verify_all_certificates()
    assert failed == 0, f"Some certificates failed verification: {errors}"
    assert passed >= 125, f"Expected at least 125 certified artifacts, found {passed}"


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


# ==============================================================================
# ADVERSARIAL FORGED CERTIFICATE VERIFICATION SUITE (14 SCENARIOS)
# ==============================================================================

def test_adversarial_01_zero_ordinate_moved_to_999():
    """Adversarial 1: Zero ordinate moved to approximately 999 with recomputed self-hash."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    cert = certification.certify_zero(1, dps=50)
    tampered = dict(cert)
    tampered["enclosure"] = dict(cert["enclosure"])
    tampered["enclosure"]["imag_mid"] = "999.123456"
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("does not overlap stored enclosure" in m for m in msgs)


def test_adversarial_02_wrong_zero_index_with_valid_fields():
    """Adversarial 2: Zero index set to 2 while keeping ordinate of zero 1 with recomputed self-hash."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    cert = certification.certify_zero(1, dps=50)
    tampered = dict(cert)
    tampered["zero_index"] = 2
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("Replayed zero #2 ordinate" in m for m in msgs)


def test_adversarial_03_zero_enclosure_radius_removed_or_narrowed():
    """Adversarial 3: Zero enclosure radius set to 0/unrealistically narrowed so replay fails."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    cert = certification.certify_zero(1, dps=50)
    tampered = dict(cert)
    tampered["enclosure"] = dict(cert["enclosure"])
    tampered["enclosure"]["imag_mid"] = "14.13470000000000000000000000000000000000"
    tampered["enclosure"]["imag_rad"] = "1e-50"
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("does not overlap stored enclosure" in m for m in msgs)


def test_adversarial_04_claimed_simplicity_with_derivative_containing_zero():
    """Adversarial 4: Status simple_zero_certified but derivative lower bound zero / excludes_zero False."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    cert = certification.certify_zero(1, dps=50)
    tampered = dict(cert)
    tampered["derivative_enclosure"] = dict(cert["derivative_enclosure"])
    tampered["derivative_enclosure"]["excludes_zero"] = False
    tampered["derivative_enclosure"]["abs_lower"] = "0.0"
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("derivative" in m.lower() for m in msgs)



def test_adversarial_05_block_nonexistent_constituent_hashes():
    """Adversarial 5: Block containing nonexistent constituent hashes."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    blk, _ = certification.certify_block("test_block", [1, 2, 3], dps=50)
    tampered = dict(blk)
    tampered["constituent_zero_hashes"] = [
        "0000000000000000000000000000000000000000000000000000000000000001",
        "0000000000000000000000000000000000000000000000000000000000000002",
        "0000000000000000000000000000000000000000000000000000000000000003"
    ]
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered, cert_store={})
    assert not ok
    assert any("hash mismatch" in m.lower() or "could not be resolved" in m.lower() for m in msgs)


def test_adversarial_06_block_valid_hashes_wrong_index_range():
    """Adversarial 6: Block declared for indices 1..3 but constituent hashes for 4..6."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    blk_1_3, z_1_3 = certification.certify_block("blk1", [1, 2, 3], dps=50)
    _, z_4_6 = certification.certify_block("blk2", [4, 5, 6], dps=50)
    tampered = dict(blk_1_3)
    tampered["constituent_zero_hashes"] = [zc["certificate_hash"] for zc in z_4_6]
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    cert_store = {zc["certificate_hash"]: zc for zc in z_1_3 + z_4_6}
    ok, msgs = certification.verify_certificate(tampered, cert_store=cert_store)
    assert not ok
    assert any("hash mismatch" in m.lower() or "index mismatch" in m.lower() for m in msgs)


def test_adversarial_07_block_count_not_matching_endpoint_turing_count():
    """Adversarial 7: Block declares count 5 for index range [1, 5] but endpoints evaluate to different count."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    blk, z_certs = certification.certify_block("blk", list(range(1, 6)), dps=50)
    tampered = dict(blk)
    tampered["endpoint_bounds"] = dict(blk["endpoint_bounds"])
    # Change t_max to ordinate before zero 3 (~22.0) so Turing count is 2 instead of 5
    tampered["endpoint_bounds"]["t_max"] = "22.0"
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    cert_store = {zc["certificate_hash"]: zc for zc in z_certs}
    ok, msgs = certification.verify_certificate(tampered, cert_store=cert_store)
    assert not ok
    assert any("Turing zero count difference" in m or "Upper endpoint count" in m for m in msgs)


def test_adversarial_08_fake_block_endpoint_range():
    """Adversarial 8: Block endpoint range altered to invalid values."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    blk, z_certs = certification.certify_block("blk", list(range(1, 4)), dps=50)
    tampered = dict(blk)
    tampered["index_range"] = [1, 10]  # Declares 1..10 while only having 3 constituents
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    cert_store = {zc["certificate_hash"]: zc for zc in z_certs}
    ok, msgs = certification.verify_certificate(tampered, cert_store=cert_store)
    assert not ok
    assert any("does not match index range" in m for m in msgs)


def test_adversarial_09_worldline_nonexistent_source_hash():
    """Adversarial 9: Worldline referencing a nonexistent source zero hash."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    wl = certification.certify_worldline(z, grade=1, delta="0.0", dps=50)
    tampered = dict(wl)
    tampered["source_zero_hash"] = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered, cert_store={})
    assert not ok
    assert any("could not be resolved" in m or "hash mismatch" in m for m in msgs)


def test_adversarial_10_worldline_arbitrary_transformed_point():
    """Adversarial 10: Worldline with an arbitrary faked transformed point."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    wl = certification.certify_worldline(z, grade=1, delta="0.0", dps=50)
    tampered = dict(wl)
    tampered["transformed_point"] = {
        "real_mid": "123.456",
        "real_rad": "1e-50",
        "imag_mid": "789.012",
        "imag_rad": "1e-50"
    }
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    cert_store = {z["certificate_hash"]: z}
    ok, msgs = certification.verify_certificate(tampered, cert_store=cert_store)
    assert not ok
    assert any("does not overlap recomputed worldline point" in m for m in msgs)


def test_adversarial_11_worldline_dropped_source_radius():
    """Adversarial 11: Worldline certificate dropping radius fields."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    wl = certification.certify_worldline(z, grade=1, delta="0.0", dps=50)
    tampered = dict(wl)
    tampered["transformed_point"] = {
        "real_mid": wl["transformed_point"]["real_mid"],
        "imag_mid": wl["transformed_point"]["imag_mid"]
        # Dropped real_rad and imag_rad
    }
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    cert_store = {z["certificate_hash"]: z}
    ok, msgs = certification.verify_certificate(tampered, cert_store=cert_store)
    assert not ok
    assert any("missing radius enclosures" in m for m in msgs)


def test_adversarial_12_synthetic_worldline_mislabeled_as_actual_zero():
    """Adversarial 12: Synthetic leaf (delta=0.05) mislabeled as actual_zero_worldline."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    wl = certification.certify_worldline(z, grade=1, delta="0.05", dps=50)
    tampered = dict(wl)
    tampered["claim_type"] = "actual_zero_worldline"
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    cert_store = {z["certificate_hash"]: z}
    ok, msgs = certification.verify_certificate(tampered, cert_store=cert_store)
    assert not ok
    assert any("claim_type mismatch" in m for m in msgs)


def test_adversarial_13_stale_source_module_hash():
    """Adversarial 13: Certificate with stale source module hash under provenance checking."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    tampered = dict(z)
    tampered["source_code_hashes"] = dict(z["source_code_hashes"])
    tampered["source_code_hashes"]["certification.py"] = "0000000000000000000000000000000000000000000000000000000000000000"
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered, check_provenance=True)
    assert not ok
    assert any("Source module 'certification.py' hash mismatch" in m for m in msgs)


def test_adversarial_14_tampered_certificate_without_recomputing_hash():
    """Adversarial 14: Tampered certificate without recomputing self-hash fails immediately on hash check."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    tampered = dict(z)
    tampered["zero_index"] = 999
    # Do NOT recompute self-hash
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("Hash mismatch" in m for m in msgs)
