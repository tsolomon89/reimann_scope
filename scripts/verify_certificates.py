"""Independently verify all stored mathematical certificates in data/certificates/.

Returns exit code 0 if all certificates pass, or non-zero with diagnostic error messages.
"""

from __future__ import annotations

import glob
import json
import os
import sys

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
    
    for c_path in cert_files:
        try:
            with open(c_path, "r", encoding="utf-8") as f:
                cert_data = json.load(f)
            ok, errs = certification.verify_certificate(cert_data)
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
