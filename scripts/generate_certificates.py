"""Generate all canonical mathematical certificates for Riemann Scope.

Outputs certificates to:
  data/certificates/zeros/
  data/certificates/blocks/
  data/certificates/worldlines/
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional, Tuple, Dict, Any, List


# Ensure repository root is on Python path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import certification

CERT_DIR = os.path.join(REPO_ROOT, "data", "certificates")
ZEROS_DIR = os.path.join(CERT_DIR, "zeros")
BLOCKS_DIR = os.path.join(CERT_DIR, "blocks")
WORLDLINES_DIR = os.path.join(CERT_DIR, "worldlines")

TRIVIAL_ZEROS_DIR = os.path.join(CERT_DIR, "trivial_zeros")

CANONICAL_BLOCKS = {
    "low_validation": list(range(1, 101)),
    "medium_research": list(range(100, 105)),
    "high_research": list(range(1000, 1003)),
    "very_high_sparse": list(range(10000, 10003)),
}


GRADES_TO_CERTIFY = [-2, -1, 0, 1, 2]
DELTAS_TO_CERTIFY = ["0.0", "-0.10", "-0.01", "+0.01", "+0.10"]


def generate_all(git_commit: Optional[str] = None) -> Tuple[int, int, int, int]:
    env_ok, env_err = certification.validate_generation_environment(git_commit)
    if not env_ok:
        print(f"[ERROR] Certificate generation aborted: {env_err}")
        sys.exit(1)

    os.makedirs(ZEROS_DIR, exist_ok=True)
    os.makedirs(TRIVIAL_ZEROS_DIR, exist_ok=True)
    os.makedirs(BLOCKS_DIR, exist_ok=True)
    os.makedirs(WORLDLINES_DIR, exist_ok=True)

    print("=== Generating Canonical Mathematical Certificates ===")
    
    # 1. Blocks and constituent nontrivial zeros
    all_zero_certs: Dict[int, Dict[str, Any]] = {}
    block_count = 0
    
    for block_id, indices in CANONICAL_BLOCKS.items():
        print(f"[*] Certifying block '{block_id}' (n={indices[0]}..{indices[-1]})...")
        block_cert, zero_certs = certification.certify_block(
            block_id, indices, dps=80, git_commit=git_commit, existing_zero_certs=all_zero_certs
        )

        
        # Save each zero certificate first
        for zc in zero_certs:
            idx = zc["nontrivial_index"]
            all_zero_certs[idx] = zc
            z_path = os.path.join(ZEROS_DIR, f"zero_{idx:05d}.json")
            with open(z_path, "w", encoding="utf-8") as f:
                json.dump(zc, f, indent=2)
                
        # Save block certificate
        block_path = os.path.join(BLOCKS_DIR, f"{block_id}.json")
        with open(block_path, "w", encoding="utf-8") as f:
            json.dump(block_cert, f, indent=2)
        block_count += 1
            
    zero_count = len(all_zero_certs)
    print(f"[+] Certified {zero_count} individual nontrivial zeros across {len(CANONICAL_BLOCKS)} blocks.")
    
    # 2. Trivial zeros (m=1..100)
    print("[*] Certifying 100 trivial zeros (m=1..100, s_m = -2m)...")
    all_trivial_certs: Dict[int, Dict[str, Any]] = {}
    for m in range(1, 101):
        tz_cert = certification.certify_trivial_zero(m, dps=80, git_commit=git_commit)
        all_trivial_certs[m] = tz_cert
        tz_path = os.path.join(TRIVIAL_ZEROS_DIR, f"trivial_zero_{m:05d}.json")
        with open(tz_path, "w", encoding="utf-8") as f:
            json.dump(tz_cert, f, indent=2)
    trivial_count = len(all_trivial_certs)
    print(f"[+] Certified {trivial_count} individual trivial zeros.")
    
    # 3. Bilateral worldlines for sample nontrivial zeros
    worldline_count = 0
    # Zeros 1, 2, 3 get full bilateral grade sweep K in [-5..5] for all 5 deltas (covers transcendental-worldlines-001 & synthetic-radial-leaves-001)
    primary_zero_indices = [1, 2, 3]
    for z_idx in primary_zero_indices:
        zc = all_zero_certs[z_idx]
        for K in range(-5, 6):
            for delta_val in DELTAS_TO_CERTIFY:
                wl_cert = certification.certify_worldline(zc, grade=K, delta=delta_val, dps=80, git_commit=git_commit)
                d_float = float(delta_val)
                delta_tag = f"delta_{d_float:+.2f}".replace(".", "p").replace("+", "pos").replace("-", "neg")
                wl_filename = f"worldline_z{z_idx:05d}_K{K:+d}_{delta_tag}.json".replace("+", "p").replace("-", "m")
                wl_path = os.path.join(WORLDLINES_DIR, wl_filename)
                with open(wl_path, "w", encoding="utf-8") as f:
                    json.dump(wl_cert, f, indent=2)
                worldline_count += 1

    # Research block zeros 100, 1000, 10000 get K in [-2..2]
    research_zero_indices = [100, 1000, 10000]
    for z_idx in research_zero_indices:
        zc = all_zero_certs[z_idx]
        for K in range(-2, 3):
            for delta_val in DELTAS_TO_CERTIFY:
                wl_cert = certification.certify_worldline(zc, grade=K, delta=delta_val, dps=80, git_commit=git_commit)
                d_float = float(delta_val)
                delta_tag = f"delta_{d_float:+.2f}".replace(".", "p").replace("+", "pos").replace("-", "neg")
                wl_filename = f"worldline_z{z_idx:05d}_K{K:+d}_{delta_tag}.json".replace("+", "p").replace("-", "m")
                wl_path = os.path.join(WORLDLINES_DIR, wl_filename)
                with open(wl_path, "w", encoding="utf-8") as f:
                    json.dump(wl_cert, f, indent=2)
                worldline_count += 1

    # 4. Trivial zero worldlines for canonical trivial sweep (m=1..10, K in [-2..2]) + sample m=100
    for m_idx in range(1, 11):
        tzc = all_trivial_certs[m_idx]
        for K in range(-2, 3):
            wl_cert = certification.certify_worldline(tzc, grade=K, delta="0.0", dps=80, git_commit=git_commit)
            wl_filename = f"worldline_trivial_m{m_idx:05d}_K{K:+d}.json".replace("+", "p").replace("-", "m")
            wl_path = os.path.join(WORLDLINES_DIR, wl_filename)
            with open(wl_path, "w", encoding="utf-8") as f:
                json.dump(wl_cert, f, indent=2)
            worldline_count += 1

    # Extra sample m=100
    tzc_100 = all_trivial_certs[100]
    for K in [-2, 0, 2]:
        wl_cert = certification.certify_worldline(tzc_100, grade=K, delta="0.0", dps=80, git_commit=git_commit)
        wl_filename = f"worldline_trivial_m00100_K{K:+d}.json".replace("+", "p").replace("-", "m")
        wl_path = os.path.join(WORLDLINES_DIR, wl_filename)
        with open(wl_path, "w", encoding="utf-8") as f:
            json.dump(wl_cert, f, indent=2)
        worldline_count += 1

    print(f"[+] Certified {worldline_count} bilateral worldlines & radial leaves.")
    report_path = os.path.join(CERT_DIR, "verification_report.json")
    print(f"[*] Updating verification report at {report_path}...")
    rep_data = certification.generate_verification_report(cert_dir=CERT_DIR, git_commit=git_commit, check_provenance=True)
    if rep_data.get("status") != "verified":
        print(f"[WARN] Verification report status: {rep_data.get('status')}")
    else:
        print(f"[+] Verification report generated successfully ({rep_data.get('total_inventory', 0)} items).")
    print("=== Certificate Generation Complete ===")
    return zero_count, trivial_count, block_count, worldline_count



def main() -> None:
    parser = argparse.ArgumentParser(description="Generate canonical mathematical certificates")
    parser.add_argument("--commit", type=str, default=None, help="Explicit producing commit SHA")
    args = parser.parse_args()
    generate_all(git_commit=args.commit)


if __name__ == "__main__":
    main()
