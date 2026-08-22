"""Independently verify all stored mathematical certificates in data/certificates/.

Returns exit code 0 if all certificates pass, or non-zero with diagnostic error messages.
"""

from __future__ import annotations

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


def verify_all() -> Tuple[bool, int, List[str]]:
    cert_pattern = os.path.join(CERT_DIR, "**", "*.json")
    cert_files = glob.glob(cert_pattern, recursive=True)
    
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
                z_idx = c_dict.get("zero_index")
                if z_idx is not None:
                    cert_store[f"zero_{z_idx:05d}"] = c_dict
            parsed_certs.append((c_path, c_dict))
        except Exception as e:
            all_anomalies.append(f"[{os.path.basename(c_path)}] JSON parse failure: {e}")

    for c_path, cert_data in parsed_certs:
        try:
            ok, errs = certification.verify_certificate(cert_data, cert_store=cert_store)
            if not ok:
                all_anomalies.extend([f"[{os.path.basename(c_path)}] {e}" for e in errs])
            else:
                total_verified += 1
        except Exception as e:
            all_anomalies.append(f"[{os.path.basename(c_path)}] Exception during verification: {e}")
            
    return (len(all_anomalies) == 0), total_verified, all_anomalies


def verify_all_certificates() -> Tuple[int, int, List[str]]:
    ok, count, anomalies = verify_all()
    failed = len(anomalies)
    return count, failed, anomalies


def main() -> None:
    print("=== Verifying Mathematical Certificates ===")
    ok, count, anomalies = verify_all()
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
