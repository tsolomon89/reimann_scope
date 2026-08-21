"""
reference_data.py — External Reference Validation and Prime Truth Sieve

Loads vendored reference zeros and prime truth data for post-discovery validation.
Strictly adheres to DATA_PROVENANCE.md:
- Reference data NEVER seeds the discovery algorithm.
- Reference ordinates are maintained as exact decimal strings.
"""

from __future__ import annotations
import os
import json
import hashlib
import bisect
from typing import List, Dict, Any, Tuple, Optional, Union, Sequence
import numpy as np
import mpmath

import math_core

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load_provenance() -> Dict[str, Any]:
    """Load provenance metadata from data/provenance.json."""
    prov_file = os.path.join(DATA_DIR, "provenance.json")
    if not os.path.exists(prov_file):
        return {}
    with open(prov_file, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_provenance() -> bool:
    """Verify that stored reference files match their SHA-256 hashes in provenance.json."""
    prov = load_provenance()
    if not prov:
        return False
    
    zeros_file = os.path.join(DATA_DIR, "zeros_reference.json")
    if os.path.exists(zeros_file):
        with open(zeros_file, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        if h != prov.get("zeta_zeros", {}).get("sha256"):
            return False
            
    primes_file = os.path.join(DATA_DIR, "primes.json")
    if os.path.exists(primes_file):
        with open(primes_file, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        if h != prov.get("primes", {}).get("sha256"):
            return False
            
    return True


def load_reference_zeros() -> List[str]:
    """Load vendored reference zeros as exact decimal strings."""
    zeros_file = os.path.join(DATA_DIR, "zeros_reference.json")
    if not os.path.exists(zeros_file):
        return []
    with open(zeros_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("ordinates", [])


def load_primes() -> List[int]:
    """Load deterministically sieved primes."""
    primes_file = os.path.join(DATA_DIR, "primes.json")
    if not os.path.exists(primes_file):
        # Fallback local sieve
        return sieve_primes(2000)
    with open(primes_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("primes", [])


def sieve_primes(max_n: int = 2000) -> List[int]:
    """Deterministic local Sieve of Eratosthenes."""
    is_prime = [True] * (max_n + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(max_n**0.5) + 1):
        if is_prime[p]:
            for multiple in range(p * p, max_n + 1, p):
                is_prime[multiple] = False
    return [i for i, prime in enumerate(is_prime) if prime]


def prime_pi(x: float, primes_list: Optional[List[int]] = None) -> int:
    """Exact prime counting function pi(x) using binary search."""
    if x < 2:
        return 0
    if primes_list is None:
        primes_list = load_primes()
    idx = bisect.bisect_right(primes_list, int(x))
    return idx


def prime_pi_array(x_arr: np.ndarray) -> np.ndarray:
    """Vectorized exact prime counting function pi(x)."""
    primes_list = load_primes()
    return np.array([prime_pi(x, primes_list) for x in x_arr], dtype=np.int64)


def validate_zero_discovery(
    discovered_ordinates: Sequence[Union[float, str, mpmath.mpf]],
    t_min: float,
    t_max: float,
    tolerance: float = 1e-6,
    dps: int = 35
) -> Dict[str, Any]:
    """
    Compare independently discovered zero ordinates against the vendored reference list.
    Calculates matched count, max difference, RMS error, unmatched roots, and residuals.
    Strictly post-discovery validation at declared precision dps.
    """
    ref_zeros_str = load_reference_zeros()
    ref_ordinates_in_range = [
        float(s) for s in ref_zeros_str if t_min <= float(s) <= t_max
    ]
    
    disc_ordinates = sorted([float(g) for g in discovered_ordinates if t_min <= float(g) <= t_max])
    
    matched_pairs = []
    unmatched_disc = []
    unmatched_ref = list(ref_ordinates_in_range)
    
    for d in disc_ordinates:
        closest_ref = None
        closest_dist = float('inf')
        for r in unmatched_ref:
            dist = abs(d - r)
            if dist < closest_dist:
                closest_dist = dist
                closest_ref = r
        if closest_dist <= tolerance and closest_ref is not None:
            matched_pairs.append((d, closest_ref, closest_dist))
            unmatched_ref.remove(closest_ref)
        else:
            unmatched_disc.append(d)
            
    diffs = [p[2] for p in matched_pairs]
    max_diff = max(diffs) if diffs else 0.0
    rms_diff = float(np.sqrt(np.mean(np.array(diffs)**2))) if diffs else 0.0
    
    # Calculate zeta residuals for discovered zeros at declared dps
    residuals = []
    for d in disc_ordinates:
        s_mpc = math_core.to_mpc((mpmath.mpf('0.5'), mpmath.mpf(str(d))), dps=dps)
        z_val = math_core.zeta_eval(s_mpc, dps=dps)
        residuals.append(float(abs(z_val)))
        
    passed = (
        len(unmatched_disc) == 0 and
        len(unmatched_ref) == 0 and
        len(matched_pairs) > 0 and
        max_diff <= tolerance
    )
    
    return {
        "status": "PASS" if passed else "FAIL",
        "passed": passed,
        "t_min": t_min,
        "t_max": t_max,
        "discovered_count": len(disc_ordinates),
        "reference_in_range_count": len(ref_ordinates_in_range),
        "reference_count": len(ref_ordinates_in_range),
        "matched_count": len(matched_pairs),
        "unmatched_discovered": unmatched_disc,
        "unmatched_reference": unmatched_ref,
        "max_diff": max_diff,
        "max_difference": max_diff,
        "rms_diff": rms_diff,
        "rms_difference": rms_diff,
        "residuals": residuals,
        "max_residual": max(residuals) if residuals else 0.0,
        "max_zeta_residual": max(residuals) if residuals else 0.0,
        "mean_zeta_residual": float(np.mean(residuals)) if residuals else 0.0
    }


# ==============================================================================
# BLOCK DATA ARCHITECTURE (docs/REBUILD_PLAN.md §17)
# ==============================================================================

# Certified arbitrary-precision zero ordinates computed for canonical height blocks
CANONICAL_BLOCKS: Dict[str, Dict[str, Any]] = {
    "low_validation": {
        "name": "Low Validation Block (n=1..10)",
        "role": "validation",
        "provenance": "mpmath.zetazero low spectrum",
        "height_range": (14.0, 50.0),
        "ordinates": [
            "14.1347251417346937904572519835624702707842571156992431756855674601",
            "21.0220396387715549926284795938969027773343405249027817546295204036",
            "25.0108575801456887632137909925628218186595496725579966724965420067",
            "30.424876125859513210311897530584091320181560023715440180962146037",
            "32.9350615877391896906623689640749034888127156035170390092800034408",
            "37.5861781588256712572177634807053328214055973508307932183330011136",
            "40.9187190121474951873981269146332543957261659627772795361613036673",
            "43.3270732809149995194961221654068057826456683718368714468788936855",
            "48.0051508811671597279424727494275160416868440011444251177753125198",
            "49.7738324776723021819167846785637240577231782996766621007819557504"
        ]
    },
    "medium_research": {
        "name": "Medium Research Block (n=100..104)",
        "role": "research_input",
        "provenance": "mpmath.zetazero verified simple zeros",
        "height_range": (236.0, 243.0),
        "ordinates": [
            "236.524229665816205802475507955662978689529495212189123700918960988",
            "237.769820480925204003236625926387107794160619352116061306831441881",
            "239.55547757332762874026893203433449248170831832670616223135120843",
            "241.049157796216586412837921410335670549645682844722093845319867364",
            "242.823271934222600016826474458878549953940543767614932383169308258"
        ]
    },
    "high_research": {
        "name": "High Research Block (n=1000..1002, gamma~1419)",
        "role": "research_input",
        "provenance": "Arbitrary-precision certified root refinement",
        "height_range": (1419.0, 1422.0),
        "ordinates": [
            "1419.42248094599568646598903807991681923210060106416601630469081468",
            "1420.41652632375113603437525093291515974188139311280252287235808927",
            "1421.85056718704865391070680755098475060378464860608233005021146223"
        ]
    },
    "very_high_sparse": {
        "name": "Very High Sparse Block (n=10000..10002, gamma~9877)",
        "role": "research_input",
        "provenance": "Arbitrary-precision certified root refinement (mpmath.zetazero at 80 dps)",
        "height_range": (9877.0, 9880.0),
        "ordinates": [
            "9877.7826540055011427740990706901235776224680517811159960054482740589555119173035",
            "9878.6547723856922881889374071462807735979972354824356156846837136581877148413796",
            "9879.0367333965687307100358186647545453373894231374077987828703550766552039044751"
        ]
    }
}


def get_block_names() -> List[str]:
    """Return available zero block identifiers."""
    return list(CANONICAL_BLOCKS.keys())


def get_zero_block(block_name: str) -> Dict[str, Any]:
    """Retrieve block metadata and ordinates for declared block."""
    if block_name not in CANONICAL_BLOCKS:
        raise KeyError(f"Block '{block_name}' not found. Available: {get_block_names()}")
    return CANONICAL_BLOCKS[block_name]


def verify_simple_zero(
    gamma: Union[str, float, mpmath.mpf],
    dps: int = 80,
    tolerance: mpmath.mpf = mpmath.mpf('1e-20')
) -> Tuple[bool, mpmath.mpf, mpmath.mpc]:
    """
    Verify numerically that rho = 1/2 + i*gamma is a simple zero:
    1. Check |zeta(1/2 + i*gamma)| < tolerance
    2. Check |zeta'(1/2 + i*gamma)| > 1e-15 (non-vanishing derivative)
    Returns (is_simple, zeta_residual, zeta_prime_val).
    """
    with mpmath.workdps(dps + 20):
        g = math_core.to_mpf(gamma, dps=dps + 20)
        s_0 = mpmath.mpc(mpmath.mpf('0.5'), g)
        
        z_val = math_core.zeta_eval(s_0, dps=dps + 20)
        z_prime = math_core.zeta_derivative(s_0, n=1, dps=dps + 20)
        
        res = abs(z_val)
        deriv_abs = abs(z_prime)
        
        is_simple = (res <= tolerance) and (deriv_abs >= mpmath.mpf('1e-15'))
        return bool(is_simple), res, z_prime
