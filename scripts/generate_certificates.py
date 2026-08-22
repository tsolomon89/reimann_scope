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

CANONICAL_BLOCKS = {
    "low_validation": list(range(1, 11)),
    "medium_research": list(range(100, 105)),
    "high_research": list(range(1000, 1003)),
    "very_high_sparse": list(range(10000, 10003)),
}

GRADES_TO_CERTIFY = [-2, -1, 0, 1, 2]
DELTAS_TO_CERTIFY = ["0.0", "-0.10", "-0.01", "+0.01", "+0.10"]


def generate_all(git_commit: Optional[str] = None) -> Tuple[int, int, int]:
    os.makedirs(ZEROS_DIR, exist_ok=True)
    os.makedirs(BLOCKS_DIR, exist_ok=True)
    os.makedirs(WORLDLINES_DIR, exist_ok=True)

    print("=== Generating Canonical Mathematical Certificates ===")
    
    # 1. Blocks and constituent zeros
    all_zero_certs: Dict[int, Dict[str, Any]] = {}
    block_count = 0
    
    for block_id, indices in CANONICAL_BLOCKS.items():
        print(f"[*] Certifying block '{block_id}' (n={indices[0]}..{indices[-1]})...")
        block_cert, zero_certs = certification.certify_block(block_id, indices, dps=80, git_commit=git_commit)
        
        # Save each zero certificate first
        for zc in zero_certs:
            idx = zc["zero_index"]
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
    print(f"[+] Certified {zero_count} individual zeros across {len(CANONICAL_BLOCKS)} blocks.")
    
    # 2. Bilateral worldlines for reference zero 1 (and sample higher zeros)
    worldline_count = 0
    test_zero_indices = [1, 100, 1000, 10000]
    
    for z_idx in test_zero_indices:
        zc = all_zero_certs[z_idx]
        for K in GRADES_TO_CERTIFY:
            for delta_val in DELTAS_TO_CERTIFY:
                wl_cert = certification.certify_worldline(zc, grade=K, delta=delta_val, dps=80, git_commit=git_commit)
                d_float = float(delta_val)
                delta_tag = f"delta_{d_float:+.2f}".replace(".", "p").replace("+", "pos").replace("-", "neg")
                wl_filename = f"worldline_z{z_idx:05d}_K{K:+d}_{delta_tag}.json".replace("+", "p").replace("-", "m")
                wl_path = os.path.join(WORLDLINES_DIR, wl_filename)
                with open(wl_path, "w", encoding="utf-8") as f:
                    json.dump(wl_cert, f, indent=2)
                worldline_count += 1
                
    print(f"[+] Certified {worldline_count} bilateral worldlines & radial leaves.")
    print("=== Certificate Generation Complete ===")
    return zero_count, block_count, worldline_count


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate canonical mathematical certificates")
    parser.add_argument("--commit", type=str, default=None, help="Explicit producing commit SHA")
    args = parser.parse_args()
    generate_all(git_commit=args.commit)


if __name__ == "__main__":
    main()
