"""Independently verify all stored mathematical certificates in data/certificates/.

Supports:
- Default / --check: Strictly read-only verification of all certificate files and verification_report.json.
- --write-report: Recomputes verification and updates verification_report.json.

Returns exit code 0 if all certificates pass, or non-zero with diagnostic error messages.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from typing import Dict, Any, List, Tuple

# Ensure repository root is on Python path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import certification

CERT_DIR = os.path.join(REPO_ROOT, "data", "certificates")


def verify_all(write_report: bool = False, canonical_current: bool = True) -> Tuple[bool, int, List[str]]:
    """Verify all stored certificates.

    If write_report is True, generates/updates data/certificates/verification_report.json.
    Otherwise, runs in strictly read-only mode and validates the existing report.
    """
    zeros_files = sorted(glob.glob(os.path.join(CERT_DIR, "zeros", "*.json")))
    trivial_files = sorted(glob.glob(os.path.join(CERT_DIR, "trivial_zeros", "*.json")))
    blocks_files = sorted(glob.glob(os.path.join(CERT_DIR, "blocks", "*.json")))
    worldlines_files = sorted(glob.glob(os.path.join(CERT_DIR, "worldlines", "*.json")))

    cert_files = zeros_files + trivial_files + blocks_files + worldlines_files

    if not cert_files:
        return False, 0, ["No certificates found in data/certificates/"]

    all_anomalies: List[str] = []
    total_verified = 0

    # Pre-load all certificate dictionaries into memory for fast dependency resolution
    cert_store: Dict[str, Dict[str, Any]] = {}
    parsed_certs: List[Tuple[str, Dict[str, Any]]] = []

    for c_path in cert_files:
        try:
            with open(c_path, "r", encoding="utf-8") as f:
                c_dict = json.load(f)
            c_hash = c_dict.get("certificate_hash")
            if c_hash:
                cert_store[c_hash] = c_dict
            if c_dict.get("certificate_type") == "zero_isolation_and_simplicity":
                z_idx = c_dict.get("nontrivial_index") or c_dict.get("zero_index")
                if z_idx is not None:
                    cert_store[f"zero_{z_idx:05d}"] = c_dict
            elif c_dict.get("certificate_type") == "trivial_zero_certificate":
                m_idx = c_dict.get("trivial_index")
                if m_idx is not None:
                    cert_store[f"trivial_zero_{m_idx:05d}"] = c_dict
            parsed_certs.append((c_path, c_dict))
        except Exception as e:
            all_anomalies.append(f"[{os.path.basename(c_path)}] JSON parse failure: {e}")

    for c_path, cert_data in parsed_certs:
        try:
            ok, errs = certification.verify_certificate(cert_data, cert_store=cert_store, check_provenance=True, canonical_current=canonical_current)
            if not ok:
                all_anomalies.extend([f"[{os.path.basename(c_path)}] {e}" for e in errs])
            else:
                total_verified += 1
        except Exception as e:
            all_anomalies.append(f"[{os.path.basename(c_path)}] Exception during verification: {e}")

    if write_report:
        # Generate and save verification report artifact
        certification.generate_verification_report(cert_dir=CERT_DIR, check_provenance=True)
    else:
        # Read-only mode: validate existing report without modifying it
        rep_ok, rep_data, rep_errs = certification.load_verification_report(cert_dir=CERT_DIR, check_provenance=True, canonical_current=canonical_current)
        if not rep_ok:
            all_anomalies.extend([f"[verification_report.json] {e}" for e in rep_errs])

    return (len(all_anomalies) == 0), total_verified, all_anomalies


def verify_all_certificates() -> Tuple[int, int, List[str]]:
    ok, count, anomalies = verify_all(write_report=False)
    failed = len(anomalies)
    return count, failed, anomalies


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify mathematical certificates")
    parser.add_argument("--write-report", "-w", action="store_true", help="Generate and write verification_report.json")
    parser.add_argument("--check", "-c", action="store_true", help="Strictly read-only verification check (default)")
    args = parser.parse_args()

    write_mode = bool(args.write_report)
    mode_desc = "Writing verification report" if write_mode else "Read-only verification check"
    print(f"=== Verifying Mathematical Certificates ({mode_desc}) ===")
    ok, count, anomalies = verify_all(write_report=write_mode)
    if ok:
        print(f"[SUCCESS] All {count} certificates mathematically verified.")
        sys.exit(0)
    else:
        print(f"[FAILURE] {len(anomalies)} verification anomalies found:")
        for a in anomalies:
            print(f"  - {a}")
        sys.exit(1)


if __name__ == "__main__":
    main()
