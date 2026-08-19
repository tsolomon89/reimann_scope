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
from typing import List, Dict, Any, Tuple
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
    if primes_list is None:
        primes_list = load_primes()
    if x < 2:
        return 0
    return bisect.bisect_right(primes_list, int(x))


def prime_pi_array(x_arr: np.ndarray) -> np.ndarray:
    """Vectorized exact prime counting function pi(x)."""
    primes_list = load_primes()
    return np.array([prime_pi(x, primes_list) for x in x_arr], dtype=np.int64)


def validate_zero_discovery(
    discovered_ordinates: List[float | mpmath.mpf],
    t_min: float,
    t_max: float,
    tolerance: float = 1e-6
) -> Dict[str, Any]:
    """
    Compare independently discovered zero ordinates against the vendored reference list.
    Calculates matched count, max difference, RMS error, unmatched roots, and residuals.
    Strictly post-discovery validation.
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
    
    # Calculate zeta residuals for discovered zeros
    residuals = []
    for d in disc_ordinates:
        z_val = math_core.zeta_eval(complex(0.5, d), dps=35)
        residuals.append(float(abs(z_val)))
        
    passed = (
        len(unmatched_disc) == 0 and
        len(unmatched_ref) == 0 and
        len(matched_pairs) > 0 and
        max_diff <= tolerance
    )
    
    return {
        "t_min": t_min,
        "t_max": t_max,
        "discovered_count": len(disc_ordinates),
        "reference_count": len(ref_ordinates_in_range),
        "matched_count": len(matched_pairs),
        "max_difference": max_diff,
        "rms_difference": rms_diff,
        "unmatched_discovered": unmatched_disc,
        "unmatched_reference": unmatched_ref,
        "residuals": residuals,
        "max_residual": max(residuals) if residuals else 0.0,
        "passed": passed
    }
