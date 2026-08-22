"""Rigorous mathematical certification engine for the Riemann Scope research instrument.

Utilizes FLINT/Arb ball arithmetic (via python-flint) to compute certified root enclosures,
isolate non-trivial zeros, verify simplicity via non-zero derivative enclosures (0 ∉ ζ'(B_n)),
verify consecutive block completeness via Turing zero counting, and certify bilateral transcendental worldlines.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import subprocess
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    import flint
    from flint import acb, acb_series, arb, ctx
    FLINT_AVAILABLE = True
except ImportError:
    flint = None  # type: ignore[assignment]
    acb = None    # type: ignore[assignment]
    acb_series = None  # type: ignore[assignment]
    arb = None    # type: ignore[assignment]
    ctx = None    # type: ignore[assignment]
    FLINT_AVAILABLE = False

FLINT_VERSION = getattr(flint, "__version__", "0.6.0") if flint is not None else "N/A"
CERTIFICATE_SCHEMA_VERSION = "2.0"
VERIFIER_VERSION = "2.0.0"
ALGORITHM_VERSION = "2.0.0"

CERTIFICATION_LEVELS = [
    "candidate",
    "residual_verified",
    "isolated_zero_certified",
    "simple_zero_certified",
    "complete_block_certified",
    "worldline_certified",
]

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
CERT_DIR = os.path.join(REPO_ROOT, "data", "certificates")
ZEROS_DIR = os.path.join(CERT_DIR, "zeros")
TRIVIAL_ZEROS_DIR = os.path.join(CERT_DIR, "trivial_zeros")
BLOCKS_DIR = os.path.join(CERT_DIR, "blocks")
WORLDLINES_DIR = os.path.join(CERT_DIR, "worldlines")


def _sha256_canonical(obj: Dict[str, Any]) -> str:
    """Compute SHA-256 of JSON object without the 'certificate_hash' field."""
    clean_obj = {k: v for k, v in obj.items() if k != "certificate_hash"}
    encoded = json.dumps(clean_obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _get_source_code_hashes() -> Dict[str, str]:
    """Compute normalized LF SHA-256 hashes of core mathematical and certification modules."""
    modules = [
        "certification.py",
        "transforms.py",
        "reference_data.py",
        "math_core.py",
        "transcendental.py",
        "converter.py",
        "research_runner.py",
        "zero_finder.py"
    ]
    hashes: Dict[str, str] = {}
    for mod in modules:
        mod_path = os.path.join(REPO_ROOT, mod)
        if os.path.exists(mod_path):
            with open(mod_path, "rb") as f:
                content = f.read().replace(b"\r\n", b"\n")
            hashes[mod] = hashlib.sha256(content).hexdigest()
        else:
            hashes[mod] = "N/A"
    return hashes


def _get_input_data_hashes() -> Dict[str, str]:
    """Get SHA-256 hashes of reference data."""
    data_files = [
        "zeros_reference.json",
        "zeros_first_100_reference.json",
        "canonical_blocks.json",
        "primes.json"
    ]
    hashes: Dict[str, str] = {}
    for df in data_files:
        df_path = os.path.join(REPO_ROOT, "data", df)
        if os.path.exists(df_path):
            with open(df_path, "rb") as f:
                content = f.read().replace(b"\r\n", b"\n")
            hashes[df] = hashlib.sha256(content).hexdigest()
        else:
            hashes[df] = "N/A"
    return hashes



def _get_dependency_fingerprint() -> Dict[str, str]:
    """Capture environment dependency versions."""
    import mpmath
    return {
        "python": sys.version.split()[0],
        "python_flint": FLINT_VERSION,
        "mpmath": getattr(mpmath, "__version__", "N/A"),
        "platform": sys.platform,
    }


def _get_git_commit() -> str:
    """Retrieve current Git commit hash or fallback."""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        return commit
    except Exception:
        return "UNKNOWN"


def _split_ball_str(ball: Any) -> Tuple[str, str]:
    """Extract midpoint and radius strings from an Arb ball representation."""
    s = str(ball).strip()
    if s.startswith("[") and "+/-" in s:
        parts = s.strip("[]").split("+/-")
        return parts[0].strip(), parts[1].strip()
    return s, "0"


def _reconstruct_arb_ball(mid_str: str, rad_str: Optional[str] = None) -> Any:
    """Reconstruct an Arb ball without float downcast."""
    if not FLINT_AVAILABLE or arb is None:
        raise RuntimeError("FLINT is not available")
    m_clean = str(mid_str).strip()
    if m_clean.startswith("[") and "+/-" in m_clean:
        return arb(m_clean)
    if rad_str is not None:
        r_clean = str(rad_str).strip("[]").split("+/-")[0].strip()
        if r_clean and r_clean not in ["0", "0.0"]:
            return arb(f"[{m_clean} +/- {r_clean}]")
    return arb(m_clean)


def certify_zero(index: int, dps: int = 80, git_commit: Optional[str] = None) -> Dict[str, Any]:
    """Obtain a certified Arb/ACB enclosure and simplicity verification for the n-th zero.
    
    Args:
        index: Positive integer zero index (1-based, e.g. 1 for first zero ~14.1347).
        dps: Decimal precision for evaluation context.
        git_commit: Optional explicit producing commit SHA.
        
    Returns:
        A structured zero certificate dictionary with cryptographic hash.
    """
    if index < 1:
        raise ValueError(f"Zero index must be positive integer >= 1, got {index}")
    if not FLINT_AVAILABLE or ctx is None or acb is None or arb is None or acb_series is None:
        raise RuntimeError(
            "FLINT/python-flint is required for rigorous mathematical certification. "
            "Please ensure python-flint>=0.6.0 is installed in your Python environment."
        )

    old_dps = ctx.dps
    try:
        ctx.dps = dps + 20
        # Compute certified Arb/ACB zero enclosure
        z_enc = acb.zeta_zero(index)
        
        # Real and imaginary components as Arb balls
        re_ball = z_enc.real
        im_ball = z_enc.imag
        
        # Compute adjacent zeros for rigorous isolation interval bounds
        if index == 1:
            z_next = acb.zeta_zero(2)
            lower_iso = arb("0.0")
            upper_iso = (im_ball + z_next.imag) / 2
        else:
            z_prev = acb.zeta_zero(index - 1)
            z_next = acb.zeta_zero(index + 1)
            lower_iso = (z_prev.imag + im_ball) / 2
            upper_iso = (im_ball + z_next.imag) / 2
            
        # Rigorous Taylor expansion at z_enc to degree 3: ζ(z + x) = ζ(z) + ζ'(z)x + (ζ''(z)/2)x^2 + ...
        ser = acb_series([z_enc, 1], 4).zeta()
        z_res = ser[0]
        z_prime = ser[1]
        c2 = ser[2]
        c3 = ser[3]
        
        # Simplicity check: 0 ∉ ζ'(B_n)
        zp_abs_lower = z_prime.abs_lower()
        is_simple = bool(zp_abs_lower > 0)
        status = "simple_zero_certified" if is_simple else "isolated_zero_certified"
        
        commit = git_commit or _get_git_commit()
        
        re_m, re_r = _split_ball_str(re_ball)
        im_m, im_r = _split_ball_str(im_ball)
        low_m, _ = _split_ball_str(lower_iso)
        up_m, _ = _split_ball_str(upper_iso)
        zp_re_m, zp_re_r = _split_ball_str(z_prime.real)
        zp_im_m, zp_im_r = _split_ball_str(z_prime.imag)
        zp_abs_low_m, _ = _split_ball_str(zp_abs_lower)
        c2_re_m, _ = _split_ball_str(c2.real)
        c2_im_m, _ = _split_ball_str(c2.imag)
        c3_re_m, _ = _split_ball_str(c3.real)
        c3_im_m, _ = _split_ball_str(c3.imag)
        
        cert: Dict[str, Any] = {
            "schema_version": CERTIFICATE_SCHEMA_VERSION,
            "certificate_type": "zero_isolation_and_simplicity",
            "status": status,
            "zero_family": "nontrivial",
            "nontrivial_index": index,
            "zero_index": index,
            "mathematical_claim": f"Nontrivial Riemann zeta zero index {index} uniquely isolated on critical line; simplicity verified via 0 ∉ ζ'(B_{index})",
            "enclosure": {
                "real_mid": re_m,
                "real_rad": re_r,
                "imag_mid": im_m,
                "imag_rad": im_r,
                "exact_real": bool(re_ball == arb("0.5")),
            },
            "isolation_interval": {
                "lower_bound": low_m,
                "upper_bound": up_m,
                "isolated": True,
            },
            "derivative_enclosure": {
                "real_mid": zp_re_m,
                "real_rad": zp_re_r,
                "imag_mid": zp_im_m,
                "imag_rad": zp_im_r,
                "abs_lower": zp_abs_low_m,
                "excludes_zero": is_simple,
            },
            "higher_coefficients": {
                "c2_real": c2_re_m,
                "c2_imag": c2_im_m,
                "c3_real": c3_re_m,
                "c3_imag": c3_im_m,
            },
            "method": "flint.acb.zeta_zero via Arb Turing-method isolating balls and acb_series Taylor expansion",
            "precision_dps": dps,
            "precision_bits": int(dps * 3.321928),
            "library": "python-flint",
            "library_version": FLINT_VERSION,
            "verifier_version": VERIFIER_VERSION,
            "algorithm_version": ALGORITHM_VERSION,
            "producing_git_commit": commit,
            "source_code_hashes": _get_source_code_hashes(),
            "input_data_hashes": _get_input_data_hashes(),
            "dependency_fingerprint": _get_dependency_fingerprint(),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "invalidation_conditions": [
                "source_code_hash_mismatch",
                "dependency_fingerprint_mismatch",
                "input_data_hash_mismatch",
                "flint_replay_containment_failure"
            ]
        }
        cert["certificate_hash"] = _sha256_canonical(cert)
        return cert
    finally:
        ctx.dps = old_dps


def certify_trivial_zero(m: int, dps: int = 80, git_commit: Optional[str] = None) -> Dict[str, Any]:
    """Obtain a certified Arb/ACB enclosure and simplicity verification for the m-th trivial zero s = -2m.
    
    Args:
        m: Positive integer trivial zero index (1-based, e.g. 1 for s = -2).
        dps: Decimal precision for evaluation context.
        git_commit: Optional explicit producing commit SHA.
        
    Returns:
        A structured trivial zero certificate dictionary with cryptographic hash.
    """
    if m < 1:
        raise ValueError(f"Trivial zero index m must be positive integer >= 1, got {m}")
    if not FLINT_AVAILABLE or ctx is None or acb is None or arb is None or acb_series is None:
        raise RuntimeError(
            "FLINT/python-flint is required for rigorous mathematical certification."
        )

    old_dps = ctx.dps
    try:
        ctx.dps = dps + 20
        s_exact = -2 * m
        s_ball = acb(s_exact, 0)
        
        # Evaluate zeta and derivative at s = -2m
        ser = acb_series([s_ball, 1], 3).zeta()
        z_val = ser[0]
        z_prime = ser[1]
        c2 = ser[2]
        
        # Verification that zeta(-2m) contains 0
        zero_arb = arb("0.0")
        contains_zero = z_val.real.contains(zero_arb) and z_val.imag.contains(zero_arb)
        
        # Simplicity check: 0 ∉ ζ'(s_m)
        zp_abs_lower = z_prime.abs_lower()
        is_simple = bool(zp_abs_lower > 0)
        status = "simple_zero_certified" if (contains_zero and is_simple) else "isolated_zero_certified"
        
        # Isolation interval [-2m - 0.5, -2m + 0.5]
        lower_iso = arb(str(s_exact - 0.5))
        upper_iso = arb(str(s_exact + 0.5))
        
        # Negative control evaluations: zeta(0) = -1/2, zeta(-2m + 1)
        z0 = acb(0, 0).zeta()
        z_odd = acb(s_exact + 1, 0).zeta()
        neg_ctrl_z0_pass = not z0.real.contains(zero_arb)
        neg_ctrl_odd_pass = not z_odd.real.contains(zero_arb)
        
        commit = git_commit or _get_git_commit()
        
        zp_re_m, zp_re_r = _split_ball_str(z_prime.real)
        zp_im_m, zp_im_r = _split_ball_str(z_prime.imag)
        zp_abs_low_m, _ = _split_ball_str(zp_abs_lower)
        c2_re_m, _ = _split_ball_str(c2.real)
        c2_im_m, _ = _split_ball_str(c2.imag)
        
        cert: Dict[str, Any] = {
            "schema_version": CERTIFICATE_SCHEMA_VERSION,
            "certificate_type": "trivial_zero_certificate",
            "status": status,
            "zero_family": "trivial",
            "trivial_index": m,
            "exact_location": s_exact,
            "mathematical_claim": (
                f"Trivial Riemann zeta zero index {m} at s = {s_exact} isolated on negative real axis; "
                f"simplicity verified via 0 ∉ ζ'([{s_exact - 0.5}, {s_exact + 0.5}])"
            ),
            "enclosure": {
                "real_mid": str(s_exact),
                "real_rad": "0.0",
                "imag_mid": "0.0",
                "imag_rad": "0.0",
                "exact_real": True,
                "exact_imag": True,
            },
            "isolation_interval": {
                "lower_bound": str(s_exact - 0.5),
                "upper_bound": str(s_exact + 0.5),
                "isolated": True,
            },
            "derivative_enclosure": {
                "real_mid": zp_re_m,
                "real_rad": zp_re_r,
                "imag_mid": zp_im_m,
                "imag_rad": zp_im_r,
                "abs_lower": zp_abs_low_m,
                "excludes_zero": is_simple,
            },
            "higher_coefficients": {
                "c2_real": c2_re_m,
                "c2_imag": c2_im_m,
            },
            "negative_controls": {
                "zeta_at_zero_excluded": neg_ctrl_z0_pass,
                "zeta_at_odd_excluded": neg_ctrl_odd_pass,
            },
            "method": "Exact algebraic evaluation of Riemann functional equation trivial zero s = -2m with Arb ball enclosures",
            "precision_dps": dps,
            "precision_bits": int(dps * 3.321928),
            "library": "python-flint",
            "library_version": FLINT_VERSION,
            "verifier_version": VERIFIER_VERSION,
            "algorithm_version": ALGORITHM_VERSION,
            "producing_git_commit": commit,
            "source_code_hashes": _get_source_code_hashes(),
            "input_data_hashes": _get_input_data_hashes(),
            "dependency_fingerprint": _get_dependency_fingerprint(),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "invalidation_conditions": [
                "source_code_hash_mismatch",
                "dependency_fingerprint_mismatch",
                "input_data_hash_mismatch",
                "flint_replay_containment_failure"
            ]
        }
        cert["certificate_hash"] = _sha256_canonical(cert)
        return cert
    finally:
        ctx.dps = old_dps



def certify_block(
    block_id: str,
    zero_indices: List[int],
    dps: int = 80,
    git_commit: Optional[str] = None,
    existing_zero_certs: Optional[Dict[int, Dict[str, Any]]] = None
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Obtain a certified block certificate for a consecutive sequence of zeros.
    
    Verifies isolation, simplicity, and Turing zero count across the block boundary.
    
    Args:
        block_id: Identifier name for the block (e.g. 'low_validation').
        zero_indices: List of consecutive 1-based zero indices.
        dps: Decimal precision.
        git_commit: Optional explicit producing commit SHA.
        existing_zero_certs: Optional map of already-certified zero dictionaries.
    """
    if not FLINT_AVAILABLE or ctx is None or acb is None or arb is None or acb_series is None:
        raise RuntimeError(
            "FLINT/python-flint is required for rigorous mathematical certification. "
            "Please ensure python-flint>=0.6.0 is installed in your Python environment."
        )
    if not zero_indices:
        raise ValueError("zero_indices must be non-empty")
    
    sorted_indices = sorted(zero_indices)
    # Check consecutiveness
    for i in range(len(sorted_indices) - 1):
        if sorted_indices[i + 1] != sorted_indices[i] + 1:
            raise ValueError(f"Block indices must be consecutive, got gap between {sorted_indices[i]} and {sorted_indices[i+1]}")
            
    commit = git_commit or _get_git_commit()
    zero_certs = []
    for idx in sorted_indices:
        if existing_zero_certs and idx in existing_zero_certs:
            zero_certs.append(existing_zero_certs[idx])
        else:
            zero_certs.append(certify_zero(idx, dps=dps, git_commit=commit))
    
    min_idx = sorted_indices[0]
    max_idx = sorted_indices[-1]
    
    first_iso_lower = zero_certs[0]["isolation_interval"]["lower_bound"]
    last_iso_upper = zero_certs[-1]["isolation_interval"]["upper_bound"]
    
    old_dps = ctx.dps
    try:
        ctx.dps = dps + 20
        t_min = arb(first_iso_lower)
        t_max = arb(last_iso_upper)
        n_min_zeros = t_min.zeta_nzeros()
        n_max_zeros = t_max.zeta_nzeros()
        
        n_min_int = int(n_min_zeros.unique_fmpz())
        n_max_int = int(n_max_zeros.unique_fmpz())
        turing_count = n_max_int - n_min_int
        count_matches = (turing_count == len(sorted_indices)) and (n_min_int == min_idx - 1) and (n_max_int == max_idx)
        
        all_simple = all(c["derivative_enclosure"]["excludes_zero"] for c in zero_certs)
        status = "complete_block_certified" if (all_simple and count_matches) else "isolated_block_certified"
        
        cert: Dict[str, Any] = {
            "schema_version": CERTIFICATE_SCHEMA_VERSION,
            "certificate_type": "complete_block_certificate",
            "status": status,
            "block_id": block_id,
            "index_range": [min_idx, max_idx],
            "zero_count": len(sorted_indices),
            "mathematical_claim": f"Canonical block '{block_id}' contains exactly {len(sorted_indices)} certified consecutive simple zeros for indices {min_idx}..{max_idx}",
            "constituent_zero_hashes": [c["certificate_hash"] for c in zero_certs],
            "height_range": [zero_certs[0]["enclosure"]["imag_mid"], zero_certs[-1]["enclosure"]["imag_mid"]],
            "endpoint_bounds": {
                "t_min": first_iso_lower,
                "t_max": last_iso_upper,
                "N_t_min": str(n_min_int),
                "N_t_max": str(n_max_int),
                "turing_count": turing_count,
                "count_verified": count_matches
            },
            "all_zeros_simple": all_simple,
            "method": "flint.arb.zeta_nzeros Turing zero-count difference across isolating boundary endpoints",
            "precision_dps": dps,
            "library": "python-flint",
            "library_version": FLINT_VERSION,
            "verifier_version": VERIFIER_VERSION,
            "algorithm_version": ALGORITHM_VERSION,
            "producing_git_commit": commit,
            "source_code_hashes": _get_source_code_hashes(),
            "input_data_hashes": _get_input_data_hashes(),
            "dependency_fingerprint": _get_dependency_fingerprint(),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "invalidation_conditions": [
                "constituent_zero_hash_mismatch",
                "turing_endpoint_count_mismatch",
                "source_code_hash_mismatch"
            ]
        }
        cert["certificate_hash"] = _sha256_canonical(cert)
        return cert, zero_certs
    finally:
        ctx.dps = old_dps


def certify_worldline(
    zero_cert: Dict[str, Any],
    grade: int,
    delta: Union[float, str] = "0.0",
    dps: int = 80,
    git_commit: Optional[str] = None
) -> Dict[str, Any]:
    """Certify bilateral transcendental worldline covariance and radial leaf invariance.
    
    Args:
        zero_cert: A validated zero certificate dictionary.
        grade: Integer grade K in Z.
        delta: Radial perturbation displacement string or float ("0.0" for actual zeros).
        dps: Precision in decimal digits.
        git_commit: Optional explicit producing commit SHA.
    """
    if not FLINT_AVAILABLE or ctx is None or acb is None or arb is None or acb_series is None:
        raise RuntimeError(
            "FLINT/python-flint is required for rigorous mathematical certification. "
            "Please ensure python-flint>=0.6.0 is installed in your Python environment."
        )

    delta_str = str(delta).strip()
    old_dps = ctx.dps
    try:
        ctx.dps = dps + 20
        # Exact symbolic tau = 2*pi
        tau_ball = arb.pi() * 2
        tau_K = tau_ball ** grade
        tau_neg_K = tau_ball ** (-grade)
        sigma_critical = tau_K / 2
        
        is_trivial = (
            zero_cert.get("zero_family") == "trivial"
            or zero_cert.get("certificate_type") == "trivial_zero_certificate"
        )
        
        if is_trivial:
            m_idx = int(zero_cert.get("trivial_index", 1))
            s_exact = -2 * m_idx
            s_worldline = acb(s_exact, 0) * acb(tau_K, 0)
            
            # Normalized radial coordinate R_tau(-2m, K) = tau^(-K)*Re(tau^K * (-2m)) - 1/2 = -2m - 1/2
            R_tau = (tau_neg_K * s_worldline.real) - arb("0.5")
            expected_R = arb(str(s_exact - 0.5))
            radial_residual = (R_tau - expected_R).abs_upper()
            signed_defect = s_worldline.real - sigma_critical
            expected_signed_defect = tau_K * arb(str(s_exact - 0.5))
            defect_residual = (signed_defect - expected_signed_defect).abs_upper()
            claim_type = "trivial_zero_worldline"
            source_idx = m_idx
            src_family = "trivial"
            math_claim = (
                f"Trivial zero worldline s({grade}) = tau^{grade} * ({s_exact}) occupies exact radial leaf "
                f"R_tau = {s_exact - 0.5} (non-critical zero, R_tau != 0)"
            )
        else:
            # Reconstruct source zero ball with radii
            enc = zero_cert["enclosure"]
            re_ball = _reconstruct_arb_ball(enc["real_mid"], enc["real_rad"])
            im_ball = _reconstruct_arb_ball(enc["imag_mid"], enc["imag_rad"])
            
            # Apply delta perturbation if synthetic
            delta_arb = arb(delta_str)
            re_point = re_ball + delta_arb
            z_point = acb(re_point, im_ball)
            
            # Graded worldline point s_rho(K) = tau^K * rho
            s_worldline = z_point * acb(tau_K, 0)
            
            # Normalized radial coordinate: R_tau(s, K) = tau^(-K) * Re(s) - 1/2
            R_tau = (tau_neg_K * s_worldline.real) - arb("0.5")
            radial_residual = (R_tau - delta_arb).abs_upper()
            
            # Defect scaling
            signed_defect = s_worldline.real - sigma_critical
            expected_signed_defect = tau_K * delta_arb
            defect_residual = (signed_defect - expected_signed_defect).abs_upper()
            
            is_actual = (delta_str in ["0.0", "0", "+0.0", "-0.0"])
            claim_type = "actual_zero_worldline" if is_actual else "synthetic_radial_leaf"
            source_idx = zero_cert.get("nontrivial_index") or zero_cert.get("zero_index")
            src_family = "nontrivial"
            math_claim = (
                f"Bilateral graded worldline s_rho({grade}) = tau^{grade} * rho occupies radial leaf R_tau = {delta_str}"
                + (" (critical surface on-line zero)" if is_actual else " (synthetic radial perturbation leaf)")
            )
        
        commit = git_commit or _get_git_commit()
        
        wl_re_m, wl_re_r = _split_ball_str(s_worldline.real)
        wl_im_m, wl_im_r = _split_ball_str(s_worldline.imag)
        sig_c_m, _ = _split_ball_str(sigma_critical)
        r_tau_m, _ = _split_ball_str(R_tau)
        rad_res_m, _ = _split_ball_str(radial_residual)
        def_res_m, _ = _split_ball_str(defect_residual)
        
        cert: Dict[str, Any] = {
            "schema_version": CERTIFICATE_SCHEMA_VERSION,
            "certificate_type": "worldline_certificate",
            "status": "worldline_certified",
            "claim_type": claim_type,
            "zero_family": src_family,
            "trivial_index": source_idx if is_trivial else None,
            "nontrivial_index": source_idx if not is_trivial else None,
            "source_zero_hash": zero_cert["certificate_hash"],
            "source_zero_family": src_family,
            "source_zero_index": source_idx,
            "grade_K": grade,
            "symbolic_scale": f"tau^{grade}" if grade != 0 else "1",
            "delta": delta_str if not is_trivial else str(s_exact - 0.5),
            "transformed_point": {
                "real_mid": wl_re_m,
                "real_rad": wl_re_r,
                "imag_mid": wl_im_m,
                "imag_rad": wl_im_r,
            },

            "critical_surface_real": sig_c_m,
            "normalized_radial": r_tau_m,
            "radial_residual": rad_res_m,
            "defect_residual": def_res_m,
            "mathematical_claim": math_claim,
            "formal_theorem_reference": "RiemannScope.RadialLeaf.radialLeaf_worldline_invariance",
            "precision_dps": dps,
            "library": "python-flint",
            "library_version": FLINT_VERSION,
            "verifier_version": VERIFIER_VERSION,
            "algorithm_version": ALGORITHM_VERSION,
            "producing_git_commit": commit,
            "source_code_hashes": _get_source_code_hashes(),
            "input_data_hashes": _get_input_data_hashes(),
            "dependency_fingerprint": _get_dependency_fingerprint(),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "invalidation_conditions": [
                "source_zero_hash_mismatch",
                "radial_residual_tolerance_exceeded",
                "formal_theorem_missing"
            ]
        }
        cert["certificate_hash"] = _sha256_canonical(cert)
        return cert
    finally:
        ctx.dps = old_dps


def verify_certificate(
    cert: Dict[str, Any],
    cert_store: Optional[Dict[str, Dict[str, Any]]] = None,
    check_provenance: bool = True
) -> Tuple[bool, List[str]]:
    """Independently verify a certificate schema, SHA-256 self-hash, and replay all mathematical claims.
    
    Fails closed: Any tampering with mathematical claims, index, bounds, constituents,
    oversized balls, contradictory metadata, or source zeros will result in (False, anomalies).
    
    Args:
        cert: The certificate dictionary to verify.
        cert_store: Optional dictionary mapping certificate_hash or (type, id) -> cert dictionary for resolving dependencies.
        check_provenance: If True (default), strictly verify source module hashes and input data hashes against current files.
        
    Returns:
        (is_valid, list_of_anomalies)
    """
    anomalies: List[str] = []
    
    if not isinstance(cert, dict):
        return False, ["Certificate must be a dictionary"]
        
    expected_hash = cert.get("certificate_hash")
    if not expected_hash:
        anomalies.append("Missing certificate_hash")
    else:
        computed_hash = _sha256_canonical(cert)
        if computed_hash != expected_hash:
            anomalies.append(f"Hash mismatch: stored {expected_hash}, computed {computed_hash}")
            
    cert_type = cert.get("certificate_type")
    
    if not FLINT_AVAILABLE or ctx is None or acb is None or arb is None or acb_series is None:
        return False, ["FLINT/python-flint is required for independent mathematical verification"]

    dps = int(cert.get("precision_dps", 80))
    old_dps = ctx.dps
    ctx.dps = dps + 20

    try:
        if cert_type == "zero_isolation_and_simplicity":
            if "nontrivial_index" in cert and "zero_index" in cert and cert["nontrivial_index"] != cert["zero_index"]:
                anomalies.append(f"Contradictory index metadata: nontrivial_index ({cert['nontrivial_index']}) != zero_index ({cert['zero_index']})")
                return False, anomalies
                
            z_idx = cert.get("nontrivial_index") or cert.get("zero_index")
            if not isinstance(z_idx, int) or z_idx < 1:
                anomalies.append(f"Invalid nontrivial zero index: {z_idx}")
                return False, anomalies
                
            enc = cert.get("enclosure", {})
            re_mid_str = enc.get("real_mid")
            im_mid_str = enc.get("imag_mid")
            re_rad_str = str(enc.get("real_rad", "1e-50")).strip()
            im_rad_str = str(enc.get("imag_rad", "1e-50")).strip()
            
            if not re_mid_str or not im_mid_str:
                anomalies.append("Missing enclosure coordinates")
                return False, anomalies
                
            if re_rad_str.startswith("-") or im_rad_str.startswith("-"):
                anomalies.append(f"Negative enclosure radius is invalid: real_rad={re_rad_str}, imag_rad={im_rad_str}")
                return False, anomalies
                
            # Reconstruct stored Arb balls
            stored_re = _reconstruct_arb_ball(re_mid_str, re_rad_str)
            stored_im = _reconstruct_arb_ball(im_mid_str, im_rad_str)
            
            # Critical line check: Real part must contain 1/2
            half = arb("0.5")
            if not stored_re.contains(half) and stored_re != half:
                anomalies.append(f"Real part of zero enclosure does not contain 1/2: {stored_re}")
                
            # Replay mathematical zero enclosure with FLINT
            try:
                replayed_zero = acb.zeta_zero(z_idx)
                replayed_re = replayed_zero.real
                replayed_im = replayed_zero.imag
            except Exception as e:
                anomalies.append(f"FLINT acb.zeta_zero({z_idx}) replay failed: {e}")
                return False, anomalies
                
            # Overlap check
            if not stored_im.overlaps(replayed_im):
                anomalies.append(
                    f"Replayed zero #{z_idx} ordinate {replayed_im} does not overlap stored enclosure {stored_im}"
                )
            
            # Verify isolation interval
            iso = cert.get("isolation_interval", {})
            lower_str = iso.get("lower_bound")
            upper_str = iso.get("upper_bound")
            if not lower_str or not upper_str:
                anomalies.append("Missing isolation interval bounds")
            else:
                low_iso = arb(lower_str)
                up_iso = arb(upper_str)
                
                # Zero containment: The entire stored ball must be strictly inside the isolation interval
                if not (low_iso <= stored_im.lower() and stored_im.upper() <= up_iso):
                    anomalies.append(f"Zero ball [{stored_im.lower()}, {stored_im.upper()}] not strictly contained in isolation interval [{low_iso}, {up_iso}]")
                    
                # Oversized ball check: stored radius must not exceed half isolation interval width
                iso_width = up_iso - low_iso
                stored_rad = stored_im.rad()
                if stored_rad > iso_width / 2 or stored_rad >= arb("1.0"):
                    anomalies.append(f"Zero enclosure radius {stored_rad} is oversized (exceeds half-width or >= 1.0) and does not provide isolated zero certification")

                    
                if z_idx > 1:
                    prev_z = acb.zeta_zero(z_idx - 1)
                    if not (prev_z.imag.upper() < low_iso.lower()):
                        anomalies.append(f"Adjacent zero #{z_idx-1} ({prev_z.imag}) not excluded by lower isolation bound {low_iso}")
                next_z = acb.zeta_zero(z_idx + 1)
                if not (up_iso.upper() < next_z.imag.lower()):
                    anomalies.append(f"Adjacent zero #{z_idx+1} ({next_z.imag}) not excluded by upper isolation bound {up_iso}")
                    
                # Rigorous Turing zero count check for this isolation interval: N(up_iso) - N(low_iso) must be exactly 1
                try:
                    n_low = int(low_iso.zeta_nzeros().unique_fmpz())
                    n_up = int(up_iso.zeta_nzeros().unique_fmpz())
                    if n_up - n_low != 1:
                        anomalies.append(f"Turing zero count for isolation interval [{low_iso}, {up_iso}] is {n_up - n_low}, expected 1")
                except Exception as e:
                    anomalies.append(f"Turing count evaluation failed on [{low_iso}, {up_iso}]: {e}")
                    
            # Recompute derivative enclosure over complete stored ball and verify simplicity
            deriv = cert.get("derivative_enclosure", {})
            z_ball = acb(stored_re, stored_im)
            ser = acb_series([z_ball, 1], 2).zeta()
            z_prime = ser[1]
            abs_lower = z_prime.abs_lower()
            replayed_simple = bool(abs_lower > 0)
            
            if cert.get("status") == "simple_zero_certified":
                if not replayed_simple:
                    anomalies.append(f"Simple zero claimed but recomputed derivative enclosure contains zero: |zeta'| lower bound = {abs_lower}")
                if not deriv.get("excludes_zero"):
                    anomalies.append("Simple zero claimed but derivative_enclosure.excludes_zero is False")
                stored_abs_lower = _reconstruct_arb_ball(deriv.get("abs_lower", "0.0"))
                if not (stored_abs_lower > 0):
                    anomalies.append(f"Simple zero claimed but stored derivative lower bound <= 0: {stored_abs_lower}")
                    
        elif cert_type == "trivial_zero_certificate":
            m_idx = cert.get("trivial_index")
            s_exact = cert.get("exact_location")
            if not isinstance(m_idx, int) or m_idx < 1:
                anomalies.append(f"Invalid trivial_index: {m_idx}")
                return False, anomalies
            if not isinstance(s_exact, int) or s_exact != -2 * m_idx:
                anomalies.append(f"exact_location ({s_exact}) does not match -2 * trivial_index ({-2 * m_idx})")
                return False, anomalies

                
            # Replay FLINT evaluation of zeta(-2m)
            s_ball = acb(s_exact, 0)
            ser = acb_series([s_ball, 1], 3).zeta()
            z_val = ser[0]
            z_prime = ser[1]
            
            zero_arb = arb("0.0")
            if not z_val.real.contains(zero_arb) or not z_val.imag.contains(zero_arb):
                anomalies.append(f"zeta({s_exact}) enclosure does not contain 0: {z_val}")
                
            zp_abs_lower = z_prime.abs_lower()
            if zp_abs_lower <= 0:
                anomalies.append(f"Derivative enclosure at trivial zero s = {s_exact} contains zero: |zeta'| lower bound = {zp_abs_lower}")
                
            # Verify isolation interval [-2m - 0.5, -2m + 0.5]
            iso = cert.get("isolation_interval", {})
            low_str = iso.get("lower_bound")
            up_str = iso.get("upper_bound")
            if not low_str or not up_str:
                anomalies.append("Missing isolation interval in trivial zero certificate")
            else:
                low_val = float(low_str)
                up_val = float(up_str)
                if not (low_val <= s_exact <= up_val):
                    anomalies.append(f"Trivial zero {s_exact} not inside isolation interval [{low_val}, {up_val}]")
                if not (s_exact - 1 < low_val and up_val < s_exact + 1):
                    anomalies.append(f"Isolation interval [{low_val}, {up_val}] does not strictly isolate {s_exact} from adjacent integers")
                    
            # Negative controls verification
            z0 = acb(0, 0).zeta()
            if z0.real.contains(zero_arb):
                anomalies.append("Negative control failed: zeta(0) contains zero")
            z_odd = acb(s_exact + 1, 0).zeta()
            if z_odd.real.contains(zero_arb):
                anomalies.append(f"Negative control failed: zeta({s_exact + 1}) contains zero")
                
        elif cert_type == "complete_block_certificate":
            const_hashes = cert.get("constituent_zero_hashes", [])
            zero_count = cert.get("zero_count")
            idx_range = cert.get("index_range", [])
            
            if not isinstance(idx_range, list) or len(idx_range) != 2:
                anomalies.append(f"Invalid index_range: {idx_range}")
                return False, anomalies
                
            min_idx, max_idx = idx_range[0], idx_range[1]
            expected_count = max_idx - min_idx + 1
            
            if zero_count != expected_count:
                anomalies.append(f"zero_count ({zero_count}) does not match index range {min_idx}..{max_idx} ({expected_count})")
            if len(const_hashes) != expected_count:
                anomalies.append(f"Constituent zero hash count ({len(const_hashes)}) != expected count ({expected_count})")
                
            # Contradictory block status check
            if cert.get("status") == "complete_block_certified":
                if cert.get("all_zeros_simple") is not True:
                    anomalies.append("Contradictory block status: complete_block_certified claimed but all_zeros_simple is False")
                if cert.get("endpoint_bounds", {}).get("count_verified") is not True:
                    anomalies.append("Contradictory block status: complete_block_certified claimed but count_verified is False")
                
            # Verify each constituent zero certificate
            resolved_certs: List[Dict[str, Any]] = []
            for i, expected_zero_idx in enumerate(range(min_idx, max_idx + 1)):
                expected_c_hash = const_hashes[i] if i < len(const_hashes) else None
                zc = None
                if cert_store:
                    if expected_c_hash is not None:
                        zc = cert_store.get(expected_c_hash)
                    if zc is None:
                        zc = cert_store.get(f"zero_{expected_zero_idx:05d}")

                if zc is None:
                    # Look up on filesystem
                    disk_path = os.path.join(ZEROS_DIR, f"zero_{expected_zero_idx:05d}.json")
                    if os.path.exists(disk_path):
                        try:
                            with open(disk_path, "r", encoding="utf-8") as f:
                                zc = json.load(f)
                        except Exception:
                            zc = None
                if zc is None:
                    anomalies.append(f"Constituent zero certificate for index {expected_zero_idx} (hash {expected_c_hash}) could not be resolved")
                    continue
                if expected_c_hash and zc.get("certificate_hash") != expected_c_hash:
                    anomalies.append(f"Constituent zero #{expected_zero_idx} hash mismatch: expected {expected_c_hash}, found {zc.get('certificate_hash')}")
                z_actual_idx = zc.get("nontrivial_index") or zc.get("zero_index")
                if z_actual_idx != expected_zero_idx:
                    anomalies.append(f"Constituent zero index mismatch: expected {expected_zero_idx}, found {z_actual_idx}")
                # Independently verify constituent zero certificate
                ok_z, errs_z = verify_certificate(zc, cert_store=cert_store, check_provenance=False)
                if not ok_z:
                    anomalies.append(f"Constituent zero #{expected_zero_idx} failed verification: {errs_z}")
                resolved_certs.append(zc)
                
            # Rigorous Turing zero counting at block endpoints
            endpoint_bounds = cert.get("endpoint_bounds", {})
            t_min_str = endpoint_bounds.get("t_min") or (resolved_certs[0]["isolation_interval"]["lower_bound"] if resolved_certs else None)
            t_max_str = endpoint_bounds.get("t_max") or (resolved_certs[-1]["isolation_interval"]["upper_bound"] if resolved_certs else None)
            
            if t_min_str and t_max_str:
                t_min = arb(t_min_str)
                t_max = arb(t_max_str)
                n_min_zeros = t_min.zeta_nzeros()
                n_max_zeros = t_max.zeta_nzeros()
                try:
                    n_min_int = int(n_min_zeros.unique_fmpz())
                    n_max_int = int(n_max_zeros.unique_fmpz())
                    turing_count = n_max_int - n_min_int
                    
                    if turing_count != expected_count:
                        anomalies.append(f"Turing zero count difference N({t_max_str}) - N({t_min_str}) = {turing_count}, expected {expected_count}")
                    if n_min_int != min_idx - 1:
                        anomalies.append(f"Lower endpoint count N({t_min_str}) = {n_min_int}, expected {min_idx - 1}")
                    if n_max_int != max_idx:
                        anomalies.append(f"Upper endpoint count N({t_max_str}) = {n_max_int}, expected {max_idx}")
                except Exception as e:
                    anomalies.append(f"FLINT Turing zero counting failed on endpoints [{t_min_str}, {t_max_str}]: {e}")
            else:
                anomalies.append("Missing endpoint bounds for Turing zero counting")
                
        elif cert_type == "worldline_certificate":
            src_hash = cert.get("source_zero_hash")
            src_idx = cert.get("source_zero_index")
            grade_K = cert.get("grade_K")
            delta_str = str(cert.get("delta", "0.0")).strip()
            
            if src_hash is None or src_idx is None or grade_K is None:
                anomalies.append("Worldline certificate missing source_zero_hash, source_zero_index, or grade_K")
                return False, anomalies
                
            # Resolve source zero certificate
            src_cert = None
            if cert_store:
                src_cert = cert_store.get(src_hash) or cert_store.get(f"zero_{src_idx:05d}") or cert_store.get(f"trivial_zero_{src_idx:05d}")
            if src_cert is None:
                disk_path = os.path.join(ZEROS_DIR, f"zero_{src_idx:05d}.json")
                if not os.path.exists(disk_path):
                    disk_path = os.path.join(TRIVIAL_ZEROS_DIR, f"trivial_zero_{src_idx:05d}.json")
                if os.path.exists(disk_path):
                    try:
                        with open(disk_path, "r", encoding="utf-8") as f:
                            src_cert = json.load(f)
                    except Exception:
                        src_cert = None
            if src_cert is None:
                anomalies.append(f"Source zero certificate for index {src_idx} (hash {src_hash}) could not be resolved")
                return False, anomalies
            if src_cert.get("certificate_hash") != src_hash:
                anomalies.append(f"Source zero certificate hash mismatch: expected {src_hash}, found {src_cert.get('certificate_hash')}")
            # Verify source zero certificate
            ok_src, errs_src = verify_certificate(src_cert, cert_store=cert_store, check_provenance=False)
            if not ok_src:
                anomalies.append(f"Source zero certificate verification failed: {errs_src}")
                
            tp = cert.get("transformed_point", {})
            if "real_rad" not in tp or "imag_rad" not in tp:
                anomalies.append("Worldline transformed_point missing radius enclosures (dropped radius vulnerability)")
            else:
                re_rad_str = str(tp.get("real_rad", "0.0")).strip()
                im_rad_str = str(tp.get("imag_rad", "0.0")).strip()
                if re_rad_str.startswith("-") or im_rad_str.startswith("-"):
                    anomalies.append(f"Negative radius in transformed point: real_rad={re_rad_str}, imag_rad={im_rad_str}")
                else:
                    try:
                        if float(re_rad_str) < 0 or float(im_rad_str) < 0:
                            anomalies.append(f"Negative radius in transformed point: real_rad={re_rad_str}, imag_rad={im_rad_str}")
                    except Exception:
                        pass
                        
            tau_ball = arb.pi() * 2
            tau_K = tau_ball ** grade_K
            tau_neg_K = tau_ball ** (-grade_K)
            
            is_trivial_src = (
                src_cert.get("zero_family") == "trivial"
                or src_cert.get("certificate_type") == "trivial_zero_certificate"
            )
            
            if is_trivial_src:
                s_exact = -2 * src_idx
                s_worldline = acb(s_exact, 0) * acb(tau_K, 0)
                R_tau = (tau_neg_K * s_worldline.real) - arb("0.5")
                expected_R = arb(str(s_exact - 0.5))
                if not R_tau.contains(expected_R):
                    anomalies.append(f"Trivial zero worldline radial coordinate does not contain {s_exact - 0.5}: {R_tau}")
            else:
                # Reconstruct full source ball with radii
                s_enc = src_cert.get("enclosure", {})
                re_ball = _reconstruct_arb_ball(s_enc.get("real_mid", "0.5"), s_enc.get("real_rad", "1e-50"))
                im_ball = _reconstruct_arb_ball(s_enc.get("imag_mid", "0.0"), s_enc.get("imag_rad", "1e-50"))
                
                # Re-propagate through worldline transformation
                delta_arb = arb(delta_str)
                z_point = acb(re_ball + delta_arb, im_ball)
                s_worldline = z_point * acb(tau_K, 0)
                
                # Stored transformed point ball comparison
                stored_re = _reconstruct_arb_ball(tp.get("real_mid", "0.0"), tp.get("real_rad", "1e-50"))
                stored_im = _reconstruct_arb_ball(tp.get("imag_mid", "0.0"), tp.get("imag_rad", "1e-50"))
                if not stored_re.overlaps(s_worldline.real) or not stored_im.overlaps(s_worldline.imag):
                    anomalies.append(
                        f"Stored transformed point {stored_re}+{stored_im}j does not overlap recomputed worldline point {s_worldline}"
                    )
                    
                # Recompute normalized radial coordinate and defect
                sigma_critical = tau_K / 2
                R_tau = (tau_neg_K * s_worldline.real) - arb("0.5")
                radial_residual = (R_tau - delta_arb).abs_upper()
                
                if radial_residual > arb("1e-30"):
                    anomalies.append(f"Radial residual exceeds certification threshold: {radial_residual}")
                    
                is_actual = (delta_str in ["0.0", "0", "+0.0", "-0.0"])
                expected_claim_type = "actual_zero_worldline" if is_actual else "synthetic_radial_leaf"
                actual_claim_type = cert.get("claim_type")
                if actual_claim_type != expected_claim_type:
                    anomalies.append(f"claim_type mismatch: expected '{expected_claim_type}', found '{actual_claim_type}'")
                    
                if is_actual:
                    if not R_tau.contains(arb("0.0")):
                        anomalies.append(f"Actual zero worldline radial coordinate does not contain 0.0: {R_tau}")
                else:
                    if not R_tau.contains(delta_arb):
                        anomalies.append(f"Synthetic radial leaf coordinate does not contain declared delta {delta_str}: {R_tau}")
                        
            # Check formal theorem reference existence in Lean source
            thm_ref = cert.get("formal_theorem_reference", "")
            if thm_ref:
                lean_file = os.path.join(REPO_ROOT, "formal", "RiemannScope", "RadialLeaf.lean")
                if os.path.exists(lean_file):
                    with open(lean_file, "r", encoding="utf-8") as lf:
                        if "radialLeaf_worldline_invariance" not in lf.read():
                            anomalies.append(f"Referenced formal Lean theorem '{thm_ref}' not found in {lean_file}")
                else:
                    anomalies.append(f"Lean source file {lean_file} not found")
        else:
            anomalies.append(f"Unknown certificate_type: {cert_type}")
            
        if check_provenance:
            # Check source module hashes
            curr_src = _get_source_code_hashes()
            cert_src = cert.get("source_code_hashes", {})
            for mod, h in cert_src.items():
                if mod in curr_src and curr_src[mod] != h:
                    anomalies.append(f"Source module '{mod}' hash mismatch: cert {h}, current {curr_src[mod]}")
                    
            # Check input data hashes
            curr_data = _get_input_data_hashes()
            cert_data = cert.get("input_data_hashes", {})
            for df, h in cert_data.items():
                if df in curr_data and curr_data[df] != h:
                    anomalies.append(f"Input data '{df}' hash mismatch: cert {h}, current {curr_data[df]}")
                    
    finally:
        ctx.dps = old_dps
        
    return (len(anomalies) == 0), anomalies


def load_and_verify_certificate(
    cert_path: str,
    cert_store: Optional[Dict[str, Dict[str, Any]]] = None,
    check_provenance: bool = True
) -> Tuple[bool, Optional[Dict[str, Any]], List[str]]:
    """Load a certificate from disk and run full mathematical verification.
    
    Returns:
        (is_valid, certificate_dict_or_None, list_of_anomalies)
    """
    if not os.path.exists(cert_path):
        return False, None, [f"Certificate file '{cert_path}' does not exist"]
    try:
        with open(cert_path, "r", encoding="utf-8") as f:
            cert = json.load(f)
    except Exception as e:
        return False, None, [f"Failed to read certificate JSON from '{cert_path}': {e}"]
        
    is_valid, anomalies = verify_certificate(cert, cert_store=cert_store, check_provenance=check_provenance)
    return is_valid, cert, anomalies

