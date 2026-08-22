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
    assert any("not contained in stored enclosure" in m for m in msgs)


def test_adversarial_02_wrong_zero_index_with_valid_fields():
    """Adversarial 2: Zero index set to 2 while keeping ordinate of zero 1 with recomputed self-hash."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    cert = certification.certify_zero(1, dps=50)
    tampered = dict(cert)
    tampered["zero_index"] = 2
    if "nontrivial_index" in tampered:
        tampered["nontrivial_index"] = 2
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("Replayed zero #2" in m for m in msgs)


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
    assert any("not contained in stored enclosure" in m for m in msgs)


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
    assert any("does not contain recomputed worldline point" in m for m in msgs)



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


def test_adversarial_15_oversized_zero_enclosure_ball():
    """Adversarial 15: Oversized enclosure radius exceeding isolation width / 2 rejected."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    tampered = dict(z)
    tampered["enclosure"] = dict(z["enclosure"])
    tampered["enclosure"]["imag_rad"] = "5.0"  # Radius 5.0 exceeds isolation half-width
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("exceeds half-width" in m for m in msgs)


def test_adversarial_16_negative_or_malformed_radius():
    """Adversarial 16: Negative or malformed radius string rejected."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    tampered = dict(z)
    tampered["enclosure"] = dict(z["enclosure"])
    tampered["enclosure"]["imag_rad"] = "-0.001"
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("negative" in m.lower() for m in msgs)


def test_adversarial_missing_dependency_fingerprint():
    """Adversarial: Certificate with missing or empty dependency fingerprint rejected."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    tampered = dict(z)
    del tampered["dependency_fingerprint"]
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("dependency_fingerprint" in m for m in msgs)


def test_adversarial_forged_incompatible_dependency_version():
    """Adversarial: Certificate with incompatible/unsupported library or missing version rejected."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    tampered = dict(z)
    tampered["dependency_fingerprint"] = dict(z["dependency_fingerprint"])
    tampered["dependency_fingerprint"]["python_flint"] = "N/A"
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("python_flint" in m for m in msgs)


def test_adversarial_empty_source_hash_map():
    """Adversarial: Certificate with empty source_code_hashes rejected."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    tampered = dict(z)
    tampered["source_code_hashes"] = {}
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("source_code_hashes" in m for m in msgs)


def test_adversarial_omitted_required_source_hash():
    """Adversarial: Certificate omitting a required source module hash rejected."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    tampered = dict(z)
    tampered["source_code_hashes"] = dict(z["source_code_hashes"])
    del tampered["source_code_hashes"]["transforms.py"]
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("transforms.py" in m for m in msgs)


def test_adversarial_empty_input_hash_map():
    """Adversarial: Certificate with empty input_data_hashes rejected."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    tampered = dict(z)
    tampered["input_data_hashes"] = {}
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("input_data_hashes" in m for m in msgs)


def test_adversarial_omitted_required_data_hash():
    """Adversarial: Certificate omitting a required input data hash rejected."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    tampered = dict(z)
    tampered["input_data_hashes"] = dict(z["input_data_hashes"])
    del tampered["input_data_hashes"]["canonical_blocks.json"]
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("canonical_blocks.json" in m for m in msgs)


def test_adversarial_fake_or_malformed_producing_commit():
    """Adversarial: Certificate with fake or malformed producing git commit rejected."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    for bad_commit in ["FAKE", "FORGED", "UNKNOWN", "abc"]:
        tampered = dict(z)
        tampered["producing_git_commit"] = bad_commit
        tampered["certificate_hash"] = certification._sha256_canonical(tampered)
        ok, msgs = certification.verify_certificate(tampered)
        assert not ok
        assert any("producing_git_commit" in m for m in msgs)


def test_adversarial_overlap_without_containment():
    """Adversarial: Stored ball that merely overlaps but does not contain the authoritative replay enclosure is rejected."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    tampered = dict(z)
    tampered["enclosure"] = dict(z["enclosure"])
    # Shift midpoint by 1e-10 and set radius to 2e-10 so it overlaps the true zero (~14.1347) but does not contain the 80-dps root
    true_im = float(tampered["enclosure"]["imag_mid"])
    tampered["enclosure"]["imag_mid"] = str(true_im + 1e-10)
    tampered["enclosure"]["imag_rad"] = "1e-12"
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered)
    assert not ok
    assert any("is not contained in stored enclosure" in m for m in msgs)


def test_adversarial_contradictory_block_status():
    """Adversarial: Block claiming complete_block_certified but all_zeros_simple is False."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    blk, z_certs = certification.certify_block("test_blk", [1, 2, 3], dps=50)
    tampered = dict(blk)
    tampered["all_zeros_simple"] = False
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    cert_store = {zc["certificate_hash"]: zc for zc in z_certs}
    ok, msgs = certification.verify_certificate(tampered, cert_store=cert_store)
    assert not ok
    assert any("Contradictory block status" in m for m in msgs)


def test_adversarial_missing_isolation_count_evidence():
    """Adversarial: Block certificate missing endpoint bounds for Turing zero counting."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    blk, z_certs = certification.certify_block("test_blk", [1, 2, 3], dps=50)
    tampered = dict(blk)
    tampered["endpoint_bounds"] = {}
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    cert_store = {zc["certificate_hash"]: zc for zc in z_certs}
    ok, msgs = certification.verify_certificate(tampered, cert_store=cert_store)
    assert not ok
    assert any("Missing endpoint bounds" in m for m in msgs)


def test_trivial_zero_certification_and_verification():
    """Test certification and verification of trivial zeros s_m = -2m."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    for m in [1, 2, 10, 50, 100]:
        cert = certification.certify_trivial_zero(m, dps=50)
        assert cert["certificate_type"] == "trivial_zero_certificate"
        assert cert["zero_family"] == "trivial"
        assert cert["trivial_index"] == m
        assert cert["exact_location"] == -2 * m
        assert cert["status"] in ("simple_zero_certified", "isolated_zero_certified")
        assert cert["derivative_enclosure"]["excludes_zero"] is True

        ok, msgs = certification.verify_certificate(cert, check_provenance=False)
        assert ok, f"Trivial zero m={m} failed verification: {msgs}"


def test_trivial_zero_worldline_certification():
    """Test worldline certification of trivial zeros."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    tzc = certification.certify_trivial_zero(1, dps=50)
    cert_store = {tzc["certificate_hash"]: tzc}

    for K in [-2, 0, 2]:
        wl = certification.certify_worldline(tzc, grade=K, delta="0.0", dps=50)
        assert wl["certificate_type"] == "worldline_certificate"
        assert wl["claim_type"] == "trivial_zero_worldline"
        assert wl["zero_family"] == "trivial"
        assert wl["trivial_index"] == 1

        ok, msgs = certification.verify_certificate(wl, cert_store=cert_store, check_provenance=False)
        assert ok, f"Trivial zero worldline K={K} failed verification: {msgs}"


def test_adversarial_forged_dependency_fingerprint():
    """Adversarial: Certificate with forged dependency fingerprint (e.g. flint 0.0 or platform forged) rejected."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)

    # Bad flint version
    t1 = dict(z)
    t1["dependency_fingerprint"] = dict(z["dependency_fingerprint"])
    t1["dependency_fingerprint"]["python_flint"] = "0.0"
    t1["certificate_hash"] = certification._sha256_canonical(t1)
    ok1, msgs1 = certification.verify_certificate(t1)
    assert not ok1
    assert any("python_flint" in m for m in msgs1)

    # Forged platform
    t2 = dict(z)
    t2["dependency_fingerprint"] = dict(z["dependency_fingerprint"])
    t2["dependency_fingerprint"]["platform"] = "forged"
    t2["certificate_hash"] = certification._sha256_canonical(t2)
    ok2, msgs2 = certification.verify_certificate(t2)
    assert not ok2
    assert any("platform" in m for m in msgs2)


def test_adversarial_40char_nonexistent_git_commit():
    """Adversarial: Certificate with 40-character hex commit that does not exist in git repo rejected."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    for fake_sha in ["0000000000000000000000000000000000000000", "ffffffffffffffffffffffffffffffffffffffff"]:
        tampered = dict(z)
        tampered["producing_git_commit"] = fake_sha
        tampered["certificate_hash"] = certification._sha256_canonical(tampered)
        ok, msgs = certification.verify_certificate(tampered)
        assert not ok
        assert any("producing_git_commit" in m for m in msgs)


def test_adversarial_trivial_nontrivial_family_confusion():
    """Adversarial: Worldline certificate declaring trivial family resolving nontrivial certificate rejected."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z_nontrivial = certification.certify_zero(1, dps=50)
    z_trivial = certification.certify_trivial_zero(1, dps=50)

    # Trivial worldline pointing to nontrivial hash
    wl = certification.certify_worldline(z_trivial, grade=1, delta="0.0", dps=50)
    tampered = dict(wl)
    tampered["source_zero_hash"] = z_nontrivial["certificate_hash"]
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)

    cert_store = {
        z_nontrivial["certificate_hash"]: z_nontrivial,
        z_trivial["certificate_hash"]: z_trivial
    }
    ok, msgs = certification.verify_certificate(tampered, cert_store=cert_store, check_provenance=False)
    assert not ok
    assert any("Source zero family mismatch" in m or "could not be resolved" in m for m in msgs)


def test_adversarial_historical_commit_blob_mismatch():
    """Adversarial: An older existing commit whose historical source blobs differ must be rejected."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")
    z = certification.certify_zero(1, dps=50)
    tampered = dict(z)
    # 9f47fbf is an older commit where certification.py had a different hash
    tampered["producing_git_commit"] = "9f47fbf0146784ef8d18ffd5774474d421b646bf"
    tampered["certificate_hash"] = certification._sha256_canonical(tampered)
    ok, msgs = certification.verify_certificate(tampered, check_provenance=True)
    assert not ok
    assert any("blob hash" in m or "does not match" in m for m in msgs)


def test_verification_report_missing_or_extra_file_fails(tmp_path):
    """Adversarial: Verification report fails if a certificate is missing or an extra untracked certificate exists."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")

    # Create temporary cert tree with 2 certs
    cert_dir = tmp_path / "certificates"
    (cert_dir / "zeros").mkdir(parents=True)
    (cert_dir / "trivial_zeros").mkdir(parents=True)
    (cert_dir / "blocks").mkdir(parents=True)
    (cert_dir / "worldlines").mkdir(parents=True)

    z1 = certification.certify_zero(1, dps=50)
    z2 = certification.certify_zero(2, dps=50)
    with open(cert_dir / "zeros" / "zero_00001.json", "w", encoding="utf-8") as f:
        json.dump(z1, f, indent=2)
    with open(cert_dir / "zeros" / "zero_00002.json", "w", encoding="utf-8") as f:
        json.dump(z2, f, indent=2)

    rep = certification.generate_verification_report(cert_dir=str(cert_dir), check_provenance=False)
    assert rep["status"] == "verified"
    assert rep["total_inventory"] == 2

    # Verify report loads cleanly
    ok, _, anomalies = certification.load_verification_report(cert_dir=str(cert_dir))
    assert ok, f"Expected clean report load: {anomalies}"

    # Remove 1 file -> must fail
    os.remove(cert_dir / "zeros" / "zero_00002.json")
    ok_missing, _, anomalies_missing = certification.load_verification_report(cert_dir=str(cert_dir))
    assert not ok_missing
    assert any("does not match report total_inventory" in a or "missing on disk" in a for a in anomalies_missing)

    # Restore and add extra file -> must fail
    with open(cert_dir / "zeros" / "zero_00002.json", "w", encoding="utf-8") as f:
        json.dump(z2, f, indent=2)
    z3 = certification.certify_zero(3, dps=50)
    with open(cert_dir / "zeros" / "zero_00003.json", "w", encoding="utf-8") as f:
        json.dump(z3, f, indent=2)

    ok_extra, _, anomalies_extra = certification.load_verification_report(cert_dir=str(cert_dir))
    assert not ok_extra
    assert any("does not match report total_inventory" in a or "missing from report" in a for a in anomalies_extra)


def test_verification_report_tampered_bytes_fails(tmp_path):
    """Adversarial: Verification report fails if a certificate file's bytes are tampered."""
    if not certification.FLINT_AVAILABLE:
        pytest.skip("FLINT/python-flint not available")

    cert_dir = tmp_path / "certificates"
    (cert_dir / "zeros").mkdir(parents=True)
    (cert_dir / "trivial_zeros").mkdir(parents=True)
    (cert_dir / "blocks").mkdir(parents=True)
    (cert_dir / "worldlines").mkdir(parents=True)

    z1 = certification.certify_zero(1, dps=50)
    fpath = cert_dir / "zeros" / "zero_00001.json"
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(z1, f, indent=2)

    rep = certification.generate_verification_report(cert_dir=str(cert_dir), check_provenance=False)
    assert rep["status"] == "verified"

    # Tamper with file
    with open(fpath, "a", encoding="utf-8") as f:
        f.write(" ")

    ok, _, anomalies = certification.load_verification_report(cert_dir=str(cert_dir))
    assert not ok
    assert any("File SHA-256 mismatch" in a or "Inventory root hash mismatch" in a for a in anomalies)
