"""
reference_data.py — External Reference Validation and Prime Truth Sieve

Loads vendored reference zeros and prime truth data for post-discovery validation.
Strictly adheres to DATA_PROVENANCE.md:
- Reference data NEVER seeds the discovery algorithm.
- Reference ordinates are maintained as exact decimal strings and arbitrary-precision mpmath.mpf values.
- Authoritative zero matching and residual checks are performed without float downcast.
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


def hash_normalized_bytes(filepath: str) -> str:
    """Compute SHA-256 of file bytes after normalizing CRLF line endings to LF.
    
    This provides cross-platform invariance between Windows and Linux checkouts.
    """
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "rb") as f:
        data = f.read()
    normalized = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(normalized).hexdigest()


def verify_provenance() -> bool:
    """Verify that stored reference files match their SHA-256 hashes in provenance.json.
    
    Hash scheme: Canonical LF-normalized bytes (SHA-256).
    """
    prov = load_provenance()
    if not prov:
        return False
    
    zeros_file = os.path.join(DATA_DIR, "zeros_reference.json")
    if os.path.exists(zeros_file):
        h = hash_normalized_bytes(zeros_file)
        expected_h = prov.get("zeta_zeros", {}).get("sha256") or prov.get("zeta_zeros_baseline", {}).get("sha256")
        if h != expected_h:
            return False
            
    first_100_file = os.path.join(DATA_DIR, "zeros_first_100_reference.json")
    if os.path.exists(first_100_file):
        h = hash_normalized_bytes(first_100_file)
        if h != prov.get("zeros_first_100_reference", {}).get("sha256"):
            return False

    canonical_file = os.path.join(DATA_DIR, "canonical_blocks.json")
    if os.path.exists(canonical_file):
        h = hash_normalized_bytes(canonical_file)
        if h != prov.get("canonical_blocks", {}).get("sha256"):
            return False

    primes_file = os.path.join(DATA_DIR, "primes.json")
    if os.path.exists(primes_file):
        h = hash_normalized_bytes(primes_file)
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


def load_first_100_reference_zeros() -> List[str]:
    """Load authoritative first 100 Odlyzko reference zeros as exact decimal strings."""
    first_100_file = os.path.join(DATA_DIR, "zeros_first_100_reference.json")
    if not os.path.exists(first_100_file):
        return []
    with open(first_100_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("ordinates", [])


def get_trivial_zero(m: int) -> complex:
    """Return trivial zero s = -2m as a complex number."""
    if m < 1:
        raise ValueError(f"Trivial zero index m must be >= 1, got {m}")
    return complex(-2 * m, 0.0)


def get_trivial_zero_exact(m: int) -> int:
    """Return exact integer location s = -2m for trivial zero m."""
    if m < 1:
        raise ValueError(f"Trivial zero index m must be >= 1, got {m}")
    return -2 * m


def get_first_100_trivial_zeros() -> List[int]:
    """Return exact negative even integer locations for m=1..100."""
    return [-2 * m for m in range(1, 101)]


def evaluate_trivial_zero_exact(s_val: Union[int, float, mpmath.mpf, str]) -> Dict[str, Any]:
    """Audit mathematical properties of exact integer point under Riemann zeta.

    Strictly requires an exact integer input s = -2m. Rejects non-integral floats,
    decimal strings, or non-integral mpf values.
    """
    if isinstance(s_val, int):
        s_int = s_val
    elif isinstance(s_val, float):
        if not s_val.is_integer():
            raise ValueError(f"evaluate_trivial_zero_exact requires an exact integer, got non-integral float {s_val}")
        s_int = int(s_val)
    elif isinstance(s_val, mpmath.mpf):
        if s_val != int(s_val):
            raise ValueError(f"evaluate_trivial_zero_exact requires an exact integer, got non-integral mpf {s_val}")
        s_int = int(s_val)
    elif isinstance(s_val, str):
        try:
            s_int = int(s_val)
        except ValueError:
            raise ValueError(f"evaluate_trivial_zero_exact requires an exact integer, got non-integral string '{s_val}'")
    else:
        raise TypeError(f"Unsupported type for evaluate_trivial_zero_exact: {type(s_val)}")

    is_neg_even = (s_int < 0) and (s_int % 2 == 0)
    is_simple = is_neg_even
    is_isolated = is_neg_even
    if s_int == 0:
        zeta_val = "-0.5"
    elif is_neg_even:
        zeta_val = "0.0"
    else:
        zeta_val = str(mpmath.zeta(s_int))
    return {
        "s": s_int,
        "is_trivial_zero": is_neg_even,
        "is_simple": is_simple,
        "is_isolated": is_isolated,
        "zeta_value": zeta_val
    }


def match_candidate_against_reference_interval(
    candidate_ordinate: Union[float, mpmath.mpf, str],
    ref_str: str,
    precision_digits: Optional[int] = None
) -> Tuple[bool, mpmath.mpf, Tuple[mpmath.mpf, mpmath.mpf]]:
    """
    Match a discovered or certified ordinate against an external reference decimal rounding interval:
        [d - 0.5 * 10^(-p), d + 0.5 * 10^(-p)]

    Treats sourced decimal with p digits after the decimal point as a rounding interval.
    Returns (is_contained, absolute_difference, (lower_bound, upper_bound)).
    """
    d_ref = mpmath.mpf(ref_str)
    if precision_digits is None:
        if "." in ref_str:
            precision_digits = len(ref_str.split(".")[1])
        else:
            precision_digits = 0

    half_ulp = mpmath.mpf('0.5') * (mpmath.mpf(10) ** (-precision_digits))
    lower_b = d_ref - half_ulp
    upper_b = d_ref + half_ulp

    cand = mpmath.mpf(candidate_ordinate)
    diff = abs(cand - d_ref)
    is_contained = bool(lower_b <= cand <= upper_b)

    return is_contained, diff, (lower_b, upper_b)




def load_canonical_blocks() -> Dict[str, Dict[str, Any]]:
    """Load canonical spectrum blocks from data/canonical_blocks.json."""
    blocks_file = os.path.join(DATA_DIR, "canonical_blocks.json")
    if os.path.exists(blocks_file):
        with open(blocks_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("blocks", {})
    return {}


def load_primes() -> List[int]:
    """Load deterministically sieved primes."""
    primes_file = os.path.join(DATA_DIR, "primes.json")
    if not os.path.exists(primes_file):
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
    t_min: Union[float, str, mpmath.mpf],
    t_max: Union[float, str, mpmath.mpf],
    tolerance: Union[float, str, mpmath.mpf] = "1e-5",
    dps: int = 35
) -> Dict[str, Any]:
    """
    Compare independently discovered zero ordinates against the vendored reference list.
    Calculates matched count, max difference, RMS error, unmatched roots, and residuals.
    Operates at arbitrary precision without float downcast.
    """
    with mpmath.workdps(dps + 20):
        t_min_mpf = math_core.to_mpf(t_min, dps=dps + 20)
        t_max_mpf = math_core.to_mpf(t_max, dps=dps + 20)
        tol_mpf = math_core.to_mpf(tolerance, dps=dps + 20)

        ref_zeros_str = load_reference_zeros()
        ref_ordinates_in_range: List[Tuple[str, mpmath.mpf]] = []
        for s in ref_zeros_str:
            s_mpf = math_core.to_mpf(s, dps=dps + 20)
            if t_min_mpf <= s_mpf <= t_max_mpf:
                ref_ordinates_in_range.append((s, s_mpf))

        disc_ordinates_in_range: List[Tuple[str, mpmath.mpf]] = []
        for g in discovered_ordinates:
            g_str = str(g)
            g_mpf = math_core.to_mpf(g, dps=dps + 20)
            if t_min_mpf <= g_mpf <= t_max_mpf:
                disc_ordinates_in_range.append((g_str, g_mpf))

        disc_ordinates_in_range.sort(key=lambda item: item[1])

        matched_pairs: List[Tuple[str, str, mpmath.mpf]] = []
        unmatched_disc: List[str] = []
        unmatched_ref = list(ref_ordinates_in_range)

        for d_str, d_mpf in disc_ordinates_in_range:
            closest_ref_item = None
            closest_dist = mpmath.mpf('inf')
            for r_item in unmatched_ref:
                dist = abs(d_mpf - r_item[1])
                if dist < closest_dist:
                    closest_dist = dist
                    closest_ref_item = r_item
            if closest_dist <= tol_mpf and closest_ref_item is not None:
                matched_pairs.append((d_str, closest_ref_item[0], closest_dist))
                unmatched_ref.remove(closest_ref_item)
            else:
                unmatched_disc.append(d_str)

        diffs = [p[2] for p in matched_pairs]
        max_diff = max(diffs) if diffs else mpmath.mpf('0.0')
        if diffs:
            mean_sq = sum(d ** 2 for d in diffs) / len(diffs)
            rms_diff = mpmath.sqrt(mean_sq)
        else:
            rms_diff = mpmath.mpf('0.0')

        # Calculate zeta residuals for discovered zeros at declared dps
        residuals: List[mpmath.mpf] = []
        for d_str, d_mpf in disc_ordinates_in_range:
            s_mpc = mpmath.mpc(mpmath.mpf('0.5'), d_mpf)
            z_val = math_core.zeta_eval(s_mpc, dps=dps)
            residuals.append(abs(z_val))

        max_res = max(residuals) if residuals else mpmath.mpf('0.0')
        mean_res = (sum(residuals) / len(residuals)) if residuals else mpmath.mpf('0.0')

        passed = (
            len(unmatched_disc) == 0 and
            len(unmatched_ref) == 0 and
            len(matched_pairs) > 0 and
            max_diff <= tol_mpf
        )

        return {
            "status": "PASS" if passed else "FAIL",
            "passed": passed,
            "t_min": float(t_min_mpf),
            "t_max": float(t_max_mpf),
            "t_min_str": mpmath.nstr(t_min_mpf, n=20),
            "t_max_str": mpmath.nstr(t_max_mpf, n=20),
            "discovered_count": len(disc_ordinates_in_range),
            "reference_in_range_count": len(ref_ordinates_in_range),
            "reference_count": len(ref_ordinates_in_range),
            "matched_count": len(matched_pairs),
            "unmatched_discovered": unmatched_disc,
            "unmatched_reference": [r[0] for r in unmatched_ref],
            "max_diff": float(max_diff),
            "max_difference": float(max_diff),
            "max_diff_str": mpmath.nstr(max_diff, n=15),
            "rms_diff": float(rms_diff),
            "rms_difference": float(rms_diff),
            "rms_diff_str": mpmath.nstr(rms_diff, n=15),
            "residuals": [float(r) for r in residuals],
            "max_residual": float(max_res),
            "max_residual_str": mpmath.nstr(max_res, n=15),
            "max_zeta_residual": float(max_res),
            "mean_zeta_residual": float(mean_res),
        }


# ==============================================================================
# BLOCK DATA ARCHITECTURE (DATA_PROVENANCE.md)
# ==============================================================================

# Load blocks from disk or use canonical fallback
_LOADED_BLOCKS = load_canonical_blocks()

CANONICAL_BLOCKS: Dict[str, Dict[str, Any]] = _LOADED_BLOCKS if _LOADED_BLOCKS else {
    "low_validation": {
        "name": "Low Validation Block (n=1..10)",
        "role": "validation",
        "provenance": "mpmath.zetazero low spectrum root refinement",
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
        "provenance": "mpmath.zetazero numerically refined simple zeros",
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
        "provenance": "mpmath.zetazero numerically refined zeros at 80 dps",
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
        "provenance": "mpmath.zetazero numerically refined zeros at 80 dps",
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


def audit_simple_zero_residual(
    gamma: Union[str, float, mpmath.mpf],
    dps: int = 80,
    tolerance: mpmath.mpf = mpmath.mpf('1e-20')
) -> Tuple[bool, mpmath.mpf, mpmath.mpc]:
    """
    Audit-mode numerical diagnostic: check that rho = 1/2 + i*gamma exhibits empirical evidence consistent with a simple zero:
    1. Check |zeta(1/2 + i*gamma)| < tolerance
    2. Check |zeta'(1/2 + i*gamma)| > 1e-15 (non-vanishing numerical derivative)
    
    CRITICAL DISTINCTION: Numerical residual agreement is empirical evidence, NEVER mathematical proof or certification.
    Authoritative certification requires certified Arb/ACB ball enclosures (certification.certify_zero / verify_certificate).
    Returns (evidence_consistent_with_simple_zero, zeta_residual, zeta_prime_val).
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


def verify_simple_zero(
    gamma: Union[str, float, mpmath.mpf],
    dps: int = 80,
    tolerance: mpmath.mpf = mpmath.mpf('1e-20')
) -> Tuple[bool, mpmath.mpf, mpmath.mpc]:
    """Deprecated alias for audit_simple_zero_residual.
    
    Use certification.certify_zero and certification.verify_certificate for authoritative mathematical certification.
    """
    return audit_simple_zero_residual(gamma=gamma, dps=dps, tolerance=tolerance)
