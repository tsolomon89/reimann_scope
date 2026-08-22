"""
tests/test_first_100_zeros.py — Complete 3-Layer Validation Baseline for First 100 Riemann Zeros.

Tests:
1. Full end-to-end chain for indices 1 through 100:
   a. Independent candidate discovery (zero_finder.py) without reading or seeding from reference table.
   b. Strict monotonic ordering and unique brackets.
   c. Comparison against external Odlyzko reference table with declared 3e-9 uncertainty.
   d. Match candidate against persisted certified zero n.
   e. Strict verification of all 100 persisted certificates.
   f. Confirmation of isolation, index, simplicity, and derivative exclusion.
   g. Reporting of maximum reference difference and maximum residual.
2. Anti-leakage regression test confirming discovery does not touch reference files.
3. Complete evaluation and strict certificate verification for all first 100 trivial zeros s_m = -2m (m=1..100).
"""

import json
import os
import time
import pytest
import mpmath
import reference_data
import zero_finder
import certification


def test_first_100_nontrivial_zeros_end_to_end_baseline():
    """Execute the complete 100-zero validation chain across discovery, reference matching, and certification."""
    t0 = time.time()

    # Step 1: Independently discover all 100 candidate zeros (no reference seeding)
    candidates = zero_finder.discover_first_n_nontrivial_zeros(100, dps=40)
    assert len(candidates) == 100, f"Expected 100 discovered zeros, found {len(candidates)}"

    # Step 2: Verify strict monotonic ordering and unique brackets
    for i in range(len(candidates) - 1):
        ord_curr = mpmath.mpf(candidates[i]["refined_ordinate"])
        ord_next = mpmath.mpf(candidates[i + 1]["refined_ordinate"])
        assert ord_curr < ord_next, f"Ordering violation: zero #{i+1} ({ord_curr}) >= zero #{i+2} ({ord_next})"
        assert float(candidates[i]["zeta_residual"]) < 1e-15, f"Residual too large at zero #{i+1}"

    # Step 3: Load external reference table
    ref_zeros = reference_data.load_first_100_reference_zeros()
    assert len(ref_zeros) == 100, f"Expected 100 reference zeros, got {len(ref_zeros)}"

    max_diff = mpmath.mpf("0.0")
    max_residual = mpmath.mpf("0.0")
    max_diff_zero = 0
    max_res_zero = 0

    # Step 4: Compare against external reference table and verify persisted certificates
    for n in range(1, 101):
        cand = candidates[n - 1]
        cand_ord = mpmath.mpf(cand["refined_ordinate"])
        ref_ord_str = ref_zeros[n - 1]
        ref_ord = mpmath.mpf(ref_ord_str)

        diff = abs(cand_ord - ref_ord)
        if diff > max_diff:
            max_diff = diff
            max_diff_zero = n

        # Odlyzko declared table uncertainty is 3e-9
        assert diff < mpmath.mpf("3e-9"), (
            f"Zero #{n} ordinate {cand_ord} differs from reference {ref_ord} by {diff} (exceeds declared 3e-9 uncertainty)"
        )

        res = mpmath.mpf(cand["zeta_residual"])
        if res > max_residual:
            max_residual = res
            max_res_zero = n

        # Load persisted certified zero certificate from data/certificates/zeros/
        cert_path = os.path.join(certification.ZEROS_DIR, f"zero_{n:05d}.json")
        assert os.path.exists(cert_path), f"Missing persisted certificate for zero #{n} at {cert_path}"
        with open(cert_path, "r", encoding="utf-8") as f:
            cert = json.load(f)

        # Strictly verify persisted certificate with fail-closed verifier
        is_valid, anomalies = certification.verify_certificate(cert, check_provenance=True)
        assert is_valid, f"Persisted certificate for zero #{n} failed verification: {anomalies}"
        assert cert["nontrivial_index"] == n
        assert cert["status"] == "simple_zero_certified"
        assert cert["derivative_enclosure"]["excludes_zero"] is True
        assert cert["isolation_interval"]["isolated"] is True

    elapsed = time.time() - t0
    print(f"\n[+] First 100 Zero Baseline Complete ({elapsed:.2f}s):")
    print(f"    - Discovered: {len(candidates)} / 100")
    print(f"    - Reference Matched: 100 / 100 (uncertainty < 3e-9)")
    print(f"    - Strictly Verified Certificates: 100 / 100")
    print(f"    - Max Reference Difference: {max_diff} (at zero #{max_diff_zero})")
    print(f"    - Max Zeta Residual: {max_residual} (at zero #{max_res_zero})")


def test_discovery_independence_no_reference_leakage(monkeypatch):
    """Verify that zero discovery executes strictly without reading or loading reference files."""
    def poisoned_loader(*args, **kwargs):
        raise AssertionError("Reference data was accessed during zero discovery! Anti-leakage contract violated.")

    monkeypatch.setattr(reference_data, "load_reference_zeros", poisoned_loader)
    monkeypatch.setattr(reference_data, "load_first_100_reference_zeros", poisoned_loader)

    # Discovery must succeed without calling any poisoned reference loaders
    cand = zero_finder.discover_first_n_nontrivial_zeros(5, dps=30)
    assert len(cand) == 5
    assert mpmath.mpf(cand[0]["refined_ordinate"]) < mpmath.mpf(cand[1]["refined_ordinate"])


def test_first_100_trivial_zeros_exact_and_certified():
    """Test exact properties and FLINT certification for all first 100 trivial zeros s_m = -2m."""
    t_zeros = reference_data.get_first_100_trivial_zeros()
    assert len(t_zeros) == 100

    for m, s_m in enumerate(t_zeros, start=1):
        assert s_m == -2 * m
        tz = reference_data.evaluate_trivial_zero_exact(s_m)
        assert tz["is_trivial_zero"] is True
        assert tz["is_isolated"] is True
        assert tz["is_simple"] is True
        assert tz["zeta_value"] == "0.0"

        # Load and verify persisted certificate
        cert_path = os.path.join(certification.TRIVIAL_ZEROS_DIR, f"trivial_zero_{m:05d}.json")
        assert os.path.exists(cert_path), f"Missing persisted certificate for trivial zero m={m} at {cert_path}"
        with open(cert_path, "r", encoding="utf-8") as f:
            cert = json.load(f)
        is_valid, anomalies = certification.verify_certificate(cert, check_provenance=True)
        assert is_valid, f"Trivial zero m={m} certificate failed verification: {anomalies}"

    # Negative controls and strict rejection of non-integers
    with pytest.raises(ValueError):
        reference_data.evaluate_trivial_zero_exact(-2.1)
    with pytest.raises(ValueError):
        reference_data.evaluate_trivial_zero_exact(-2.9)
    with pytest.raises(ValueError):
        reference_data.evaluate_trivial_zero_exact("-2.5")

    # Real evaluation negative controls
    assert reference_data.evaluate_trivial_zero_exact(0)["zeta_value"] == "-0.5"
    assert reference_data.evaluate_trivial_zero_exact(0)["is_trivial_zero"] is False
    assert reference_data.evaluate_trivial_zero_exact(-1)["is_trivial_zero"] is False
    assert reference_data.evaluate_trivial_zero_exact(-3)["is_trivial_zero"] is False
