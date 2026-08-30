"""generate_legacy_manifest.py

Generates the hash-pinned legacy claim manifest directly from the immutable historical git baseline commit.
"""

import os
import sys
import json
import hashlib
import subprocess

BASELINE_COMMIT = "82643cafd605492233c6c1e992b78c2c30d45f13"

def generate_manifest(baseline_commit: str = BASELINE_COMMIT):
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    audited = {"CLM-CT-022", "CLM-CT-025"}
    exempt = {
        "CLM-EF-002", "CLM-EF-003", "CLM-ARB-009", "CLM-SS-004",
        "CLM-SS-006", "CLM-SS-007", "CLM-CMSA-026", "CLM-RH-001"
    }

    # Fetch claim register directly from git baseline commit
    cmd = ["git", "show", f"{baseline_commit}:.agents/corpus_map/claim_register.md"]
    try:
        res = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True, encoding="utf-8", check=True)
        register_text = res.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error reading baseline commit {baseline_commit}: {e.stderr}", file=sys.stderr)
        sys.exit(1)

    manifest = {
        "schema_version": "1.0.0",
        "baseline_commit": baseline_commit,
        "description": "Hash-pinned manifest of grandfathered legacy unaudited terminal claims in reimann_scope.",
        "claims": {}
    }

    for line in register_text.splitlines():
        line_str = line.strip()
        if not line_str.startswith("| `CLM-") and not line_str.startswith("|`CLM-"):
            continue
        parts = [p.strip() for p in line_str.split("|")]
        if parts and parts[0] == "":
            parts = parts[1:]
        if parts and parts[-1] == "":
            parts = parts[:-1]
        if len(parts) < 5:
            continue
        raw_cid = parts[0].strip("`")
        if raw_cid in audited or raw_cid in exempt:
            continue
        status = parts[-3].strip() if len(parts) >= 6 else parts[-2].strip()
        line_hash = hashlib.sha256(line_str.encode("utf-8")).hexdigest()
        manifest["claims"][raw_cid] = {
            "line_hash": line_hash,
            "status": status
        }

    out_path = os.path.join(repo_root, ".agents", "corpus_map", "legacy_claim_manifest.json")
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(manifest, out, indent=2)
    print(f"Wrote {len(manifest['claims'])} legacy claims from baseline {baseline_commit[:8]} to {out_path}")

if __name__ == "__main__":
    generate_manifest()
