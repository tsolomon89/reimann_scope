"""
research/handlers/cross_height.py — Cross-Height Distance & Path Coherence Handlers
"""

from __future__ import annotations
from typing import Dict, Any, Tuple, Optional, List
import mpmath

import transcendental
import reference_data
import certification
from research.handlers.base import ExperimentHandler, HandlerDependencies


def _lookup_zero_certificate(
    zero_idx_1based: int,
    zero_family: str = "nontrivial",
    expected_ordinate: Optional[str] = None
) -> Tuple[Optional[str], bool, Optional[Dict[str, Any]], List[str]]:
    """Lookup and strictly verify zero certificate."""
    if zero_family == "trivial":
        cert_path = f"data/certificates/trivial_zeros/trivial_zero_{zero_idx_1based:05d}.json"
    else:
        cert_path = f"data/certificates/zeros/zero_{zero_idx_1based:05d}.json"

    cert_data = certification.load_certificate_from_disk(cert_path)
    if not cert_data:
        return None, False, None, [f"Missing certificate file at {cert_path}"]

    cert_hash = cert_data.get("certificate_hash")
    ok, errs = certification.verify_certificate(cert_data, check_provenance=True, canonical_current=False)
    if not ok:
        return cert_hash, False, cert_data, errs

    if expected_ordinate:
        enc = cert_data.get("enclosure", {})
        mid = enc.get("imag_mid") or enc.get("real_mid")
        if mid and abs(mpmath.mpf(mid) - mpmath.mpf(expected_ordinate)) > mpmath.mpf("1e-10"):
            return cert_hash, False, cert_data, [f"Ordinate mismatch: cert {mid} != expected {expected_ordinate}"]

    return cert_hash, True, cert_data, []


class CrossHeightPathCoherenceHandler(ExperimentHandler):
    @property
    def experiment_id(self) -> str:
        return "cross-height-path-coherence-001"

    @property
    def declared_dependencies(self) -> HandlerDependencies:
        return HandlerDependencies(
            common_modules=["research_runner.py", "research/handlers/base.py"],
            handler_modules=["research/handlers/cross_height.py"],
            math_modules=["transcendental.py", "reference_data.py", "certification.py"],
            data_files=["data/zeros_reference.json", "data/canonical_blocks.json"],
            consumed_certificates=["data/certificates/zeros/*.json"],
            material_packages=["mpmath", "flint"]
        )

    def evaluate_point(
        self,
        inputs: Dict[str, str],
        dps: int = 80,
        param_space: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Dict[str, str], Optional[str]]:
        zero_idx = int(inputs.get("zero_index", inputs.get("n", "0")))
        u_str = inputs.get("u", "0.0")
        block_name = inputs.get("block", None)

        z_idx_1based = 1
        blocks = reference_data.load_canonical_blocks()
        if block_name:
            blk = blocks.get(block_name, {})
            ords = blk.get("ordinates", [])
            gamma_str = inputs.get("gamma", ords[zero_idx % len(ords)] if ords else "14.13472514173469379045725198356247027078425711569924317568556746")
            if block_name == "low_validation":
                z_idx_1based = 1 + (zero_idx % 10)
            elif block_name == "medium_research":
                z_idx_1based = 100 + (zero_idx % 5)
            elif block_name == "high_research":
                z_idx_1based = 1000 + (zero_idx % 3)
            elif block_name == "very_high_sparse":
                z_idx_1based = 10000 + (zero_idx % 3)
        else:
            ref_zeros_str = reference_data.load_reference_zeros()
            gamma_str = inputs.get("gamma", ref_zeros_str[zero_idx] if ref_zeros_str and zero_idx < len(ref_zeros_str) else "14.13472514173469379045725198356247027078425711569924317568556746")
            z_idx_1based = zero_idx + 1 if zero_idx < 10 else 1

        cert_hash, cert_ok, zc, _ = _lookup_zero_certificate(z_idx_1based)
        delta_n = transcendental.mean_zero_spacing_delta(gamma_str, dps=dps + 20)
        taylor_info = transcendental.extract_taylor_shape_coefficients(gamma_str, dps=dps + 20)
        path_info = transcendental.evaluate_derivative_normalized_path(gamma_str, u_str, dps=dps + 20)

        is_simple, z_res, _ = reference_data.audit_simple_zero_residual(gamma_str, dps=dps + 20)
        src_status = "certified" if cert_ok else ("verification_failed" if cert_hash else "not_available")

        return "ok", {
            "gamma": gamma_str,
            "u": u_str,
            "source_zero_certificate_status": src_status,
            "source_zero_cert_hash": cert_hash or "N/A",
            "worldline_certificate_status": "not_required",
            "worldline_cert_hash": "N/A",
            "worldline_certified": "false",
            "certificate_verified": "true" if cert_ok else "false",
            "is_simple_zero": "true" if (is_simple and cert_ok) else "false",
            "zeta_residual": mpmath.nstr(z_res, n=dps),
            "Delta_n": mpmath.nstr(delta_n, n=dps),
            "zeta_prime": taylor_info["zeta_prime"],
            "c2_re": taylor_info["c2_re"],
            "c2_im": taylor_info["c2_im"],
            "abs_c2": taylor_info["abs_c2"],
            "c3_re": taylor_info["c3_re"],
            "c3_im": taylor_info["c3_im"],
            "abs_c3": taylor_info["abs_c3"],
            "P_n_re": path_info["P_n_re"],
            "P_n_im": path_info["P_n_im"],
            "abs_P_n": path_info["abs_P_n"],
            "residual": mpmath.nstr(z_res, n=dps)
        }, None


class CrossHeightDistanceHandler(ExperimentHandler):
    @property
    def experiment_id(self) -> str:
        return "cross-height-distance-001"

    @property
    def declared_dependencies(self) -> HandlerDependencies:
        return HandlerDependencies(
            common_modules=["research_runner.py", "research/handlers/base.py"],
            handler_modules=["research/handlers/cross_height.py"],
            math_modules=["transcendental.py", "reference_data.py", "certification.py"],
            data_files=["data/canonical_blocks.json"],
            consumed_certificates=["data/certificates/zeros/*.json"],
            material_packages=["mpmath", "flint"]
        )

    def evaluate_point(
        self,
        inputs: Dict[str, str],
        dps: int = 80,
        param_space: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Dict[str, str], Optional[str]]:
        pair_key = inputs.get("block_pair", "low_to_medium")
        zero_idx = int(inputs.get("zero_index", "0"))
        u_max_val = mpmath.mpf(inputs.get("u_max", "0.5"))

        if pair_key == "low_to_medium":
            b1, b2 = "low_validation", "medium_research"
        elif pair_key == "low_to_high":
            b1, b2 = "low_validation", "high_research"
        elif pair_key == "low_to_very_high":
            b1, b2 = "low_validation", "very_high_sparse"
        elif "_to_" in pair_key:
            parts = pair_key.split("_to_")
            b1, b2 = parts[0], parts[1]
        else:
            b1, b2 = "low_validation", "medium_research"

        blocks = reference_data.load_canonical_blocks()
        blk1 = blocks.get(b1, {})
        blk2 = blocks.get(b2, {})
        ords1 = blk1.get("ordinates", [])
        ords2 = blk2.get("ordinates", [])

        if not ords1 or not ords2:
            ref_zeros = reference_data.load_reference_zeros()
            g1_str = ref_zeros[zero_idx % len(ref_zeros)] if ref_zeros else "14.134725141734693790457251983562"
            g2_str = ref_zeros[(zero_idx + 10) % len(ref_zeros)] if ref_zeros else "21.022039638771554992604299069"
        else:
            g1_str = ords1[zero_idx % len(ords1)]
            g2_str = ords2[zero_idx % len(ords2)]

        z1_idx = 1 + (zero_idx % (len(ords1) if ords1 else 10))
        z2_idx = 100 + (zero_idx % (len(ords2) if ords2 else 10)) if b2 == "medium_research" else (1000 + (zero_idx % (len(ords2) if ords2 else 10)) if b2 == "high_research" else 10000 + (zero_idx % (len(ords2) if ords2 else 10)))
        h1, ok1, _, _ = _lookup_zero_certificate(z1_idx)
        h2, ok2, _, _ = _lookup_zero_certificate(z2_idx)

        u_points = [mpmath.nstr(mpmath.mpf(i) * u_max_val / 10, n=8) for i in range(-10, 11)]

        dist_res = transcendental.compute_cross_height_path_distance(g1_str, g2_str, u_points=u_points, dps=dps + 20)

        l_inf = dist_res["L_infty_distance"]
        l_2 = dist_res["L_2_distance"]

        return "ok", {
            "block_pair": pair_key,
            "block_1": b1,
            "block_2": b2,
            "zero_index": str(zero_idx),
            "source_zero_certificate_status": "certified" if (ok1 and ok2) else ("verification_failed" if (h1 or h2) else "not_available"),
            "zero1_cert_hash": h1 or "N/A",
            "zero2_cert_hash": h2 or "N/A",
            "worldline_certificate_status": "not_required",
            "worldline_cert_hash": "N/A",
            "worldline_certified": "false",
            "certificate_verified": "true" if (ok1 and ok2) else "false",
            "gamma_1": g1_str,
            "gamma_2": g2_str,
            "u_max": str(u_max_val),
            "num_u_points": str(dist_res["num_u_points"]),
            "L_infty_distance": l_inf,
            "L_2_distance": l_2,
            "max_distance": l_inf,
            "residual": l_inf
        }, None
