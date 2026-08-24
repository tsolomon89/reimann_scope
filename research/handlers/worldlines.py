"""
research/handlers/worldlines.py — Transcendental, Synthetic, and Trivial Worldline Handlers
"""

from __future__ import annotations
from typing import Dict, Any, Tuple, Optional, List
import os
import json
import mpmath

import math_core
import transcendental
import reference_data
import certification
from research.handlers.base import ExperimentHandler, HandlerDependencies
from research.handlers.cross_height import _lookup_zero_certificate


def _lookup_worldline_certificate(
    zero_family: str,
    index: int,
    grade: int,
    delta: str = "0.0",
    check_provenance: bool = True,
    canonical_current: bool = False
) -> Tuple[Optional[str], bool, Optional[Dict[str, Any]], List[str]]:
    """Look up and strictly verify a worldline certificate from data/certificates/worldlines/."""
    code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    delta_str = delta.strip()
    d_float = float(delta_str)
    delta_tag = f"delta_{d_float:+.2f}".replace(".", "p").replace("+", "pos").replace("-", "neg")
    if zero_family == "trivial":
        wl_filename = f"worldline_trivial_m{index:05d}_K{grade:+d}.json".replace("+", "p").replace("-", "m")
    else:
        wl_filename = f"worldline_z{index:05d}_K{grade:+d}_{delta_tag}.json".replace("+", "p").replace("-", "m")

    cert_path = os.path.join(code_root, "data", "certificates", "worldlines", wl_filename)
    if not os.path.exists(cert_path):
        return None, False, None, [f"Worldline certificate '{wl_filename}' does not exist"]

    try:
        with open(cert_path, "r", encoding="utf-8") as f:
            wlc = json.load(f)
    except Exception as e:
        return None, False, None, [f"Failed to read worldline certificate JSON: {e}"]

    ok, errs = certification.verify_certificate(wlc, check_provenance=check_provenance, canonical_current=canonical_current)
    if not ok:
        return wlc.get("certificate_hash"), False, wlc, errs

    return wlc.get("certificate_hash"), True, wlc, []


class TranscendentalWorldlinesHandler(ExperimentHandler):
    @property
    def experiment_id(self) -> str:
        return "transcendental-worldlines-001"

    @property
    def declared_dependencies(self) -> HandlerDependencies:
        return HandlerDependencies(
            common_modules=["research_runner.py", "research/handlers/base.py"],
            handler_modules=["research/handlers/worldlines.py"],
            math_modules=["transcendental.py", "math_core.py", "reference_data.py"],
            data_files=["data/zeros_reference.json"],
            consumed_certificates=["data/certificates/zeros/*.json", "data/certificates/worldlines/*.json"],
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
        delta_str = inputs.get("delta", "0.0")
        k_str = inputs.get("k", inputs.get("K", "0"))
        grade_type = inputs.get("grade_type", "auto")
        zero_fam = inputs.get("zero_family", "nontrivial")

        if "nontrivial_index" in inputs:
            z_1based = int(inputs["nontrivial_index"])
        else:
            z_1based = zero_idx + 1 if zero_idx >= 0 else 1

        ref_zeros_str = reference_data.load_reference_zeros()
        gamma_str = inputs.get("gamma", ref_zeros_str[z_1based - 1] if 0 < z_1based <= len(ref_zeros_str) else "14.13472514173469379045725198356247027078425711569924317568556746")

        cert_hash, cert_ok, zc, errs = _lookup_zero_certificate(
            z_1based,
            zero_family=zero_fam,
            expected_ordinate=gamma_str
        )
        if not cert_ok:
            return "error", {}, f"Zero #{z_1based} certificate verification failed: {errs}"

        grade_int = int(k_str) if k_str.lstrip("-+").isdigit() else 0
        wl_hash, wl_ok, wlc, wl_errs = _lookup_worldline_certificate(
            zero_family=zero_fam,
            index=z_1based,
            grade=grade_int,
            delta=delta_str
        )

        rho_clean = mpmath.mpc('0.5', gamma_str)
        d_val = math_core.to_mpf(delta_str, dps=dps + 15)

        g_obj = transcendental.parse_grade(k_str, grade_type=grade_type)
        scale_A = g_obj.numeric_scale(dps=dps + 15)

        s_world = transcendental.zero_worldline_point(rho_clean, g_obj, delta=delta_str, dps=dps + 15)
        sigma_c = transcendental.critical_surface_sigma(g_obj, dps=dps + 15)
        radial_leaf = transcendental.normalized_radial_leaf(s_world, g_obj, dps=dps + 15)

        leaf_inv_err = abs(radial_leaf - d_val)
        z_world = transcendental.evaluate_extended_zeta(s_world, grade=g_obj, dps=dps + 15)
        zeta_res = abs(z_world)
        max_res = max(zeta_res, leaf_inv_err)

        src_status = "certified" if cert_ok else ("verification_failed" if cert_hash else "not_available")
        wl_status = "certified" if wl_ok else ("verification_failed" if wl_hash else "not_available")
        wl_certified = bool(wl_ok and cert_ok and wl_hash and wl_hash != "N/A")

        return "ok", {
            "k": k_str,
            "grade_type": g_obj.semantic_type,
            "symbolic_scale": g_obj.symbolic_expression(),
            "scale_A": mpmath.nstr(scale_A, n=dps),
            "zero_family": zero_fam,
            "nontrivial_index": str(z_1based),
            "zero_index": str(zero_idx),
            "gamma": gamma_str,
            "delta": delta_str,
            "source_zero_certificate_status": src_status,
            "source_zero_cert_hash": cert_hash or "N/A",
            "worldline_certificate_status": wl_status,
            "worldline_cert_hash": wl_hash or "N/A",
            "worldline_certified": "true" if wl_certified else "false",
            "certificate_verified": "true" if wl_certified else "false",
            "worldline_s_re": mpmath.nstr(s_world.real, n=dps),
            "worldline_s_im": mpmath.nstr(s_world.imag, n=dps),
            "sigma_c": mpmath.nstr(sigma_c, n=dps),
            "radial_leaf": mpmath.nstr(radial_leaf, n=dps),
            "zeta_residual": mpmath.nstr(zeta_res, n=dps),
            "radial_residual": mpmath.nstr(leaf_inv_err, n=dps),
            "max_residual": mpmath.nstr(max_res, n=dps),
            "residual": mpmath.nstr(max_res, n=dps)
        }, None


class SyntheticRadialLeavesHandler(ExperimentHandler):
    @property
    def experiment_id(self) -> str:
        return "synthetic-radial-leaves-001"

    @property
    def declared_dependencies(self) -> HandlerDependencies:
        return HandlerDependencies(
            common_modules=["research_runner.py", "research/handlers/base.py"],
            handler_modules=["research/handlers/worldlines.py"],
            math_modules=["transcendental.py", "math_core.py", "reference_data.py"],
            data_files=["data/zeros_reference.json"],
            consumed_certificates=["data/certificates/zeros/*.json", "data/certificates/worldlines/*.json"],
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
        delta_str = inputs.get("delta", "0.01")
        k_str = inputs.get("k", inputs.get("K", "0"))
        grade_type = inputs.get("grade_type", "auto")
        zero_fam = inputs.get("zero_family", "nontrivial")

        if "nontrivial_index" in inputs:
            z_1based = int(inputs["nontrivial_index"])
        else:
            z_1based = zero_idx + 1 if zero_idx >= 0 else 1

        ref_zeros_str = reference_data.load_reference_zeros()
        gamma_str = inputs.get("gamma", ref_zeros_str[z_1based - 1] if 0 < z_1based <= len(ref_zeros_str) else "14.13472514173469379045725198356247027078425711569924317568556746")

        cert_hash, cert_ok, zc, errs = _lookup_zero_certificate(
            z_1based,
            zero_family=zero_fam,
            expected_ordinate=gamma_str
        )
        if not cert_ok:
            return "error", {}, f"Zero #{z_1based} certificate verification failed: {errs}"

        grade_int = int(k_str) if k_str.lstrip("-+").isdigit() else 0
        wl_hash, wl_ok, wlc, wl_errs = _lookup_worldline_certificate(
            zero_family=zero_fam,
            index=z_1based,
            grade=grade_int,
            delta=delta_str
        )

        rho_base = mpmath.mpc(mpmath.mpf('0.5'), gamma_str)
        d_val = math_core.to_mpf(delta_str, dps=dps + 15)

        g_obj = transcendental.parse_grade(k_str, grade_type=grade_type)
        scale_A = g_obj.numeric_scale(dps=dps + 15)

        s_world = transcendental.zero_worldline_point(rho_base, g_obj, delta=delta_str, dps=dps + 15)
        sigma_c = transcendental.critical_surface_sigma(g_obj, dps=dps + 15)
        radial_leaf = transcendental.normalized_radial_leaf(s_world, g_obj, dps=dps + 15)

        radial_residual = abs(radial_leaf - d_val)
        signed_defect = s_world.real - sigma_c
        expected_signed_defect = scale_A * d_val
        signed_defect_error = abs(signed_defect - expected_signed_defect)

        abs_defect = abs(signed_defect)
        expected_abs_defect = scale_A * abs(d_val)
        defect_scaling_error = abs(abs_defect - expected_abs_defect)

        max_res = max(radial_residual, defect_scaling_error)

        src_status = "certified" if cert_ok else ("verification_failed" if cert_hash else "not_available")
        wl_status = "certified" if wl_ok else ("verification_failed" if wl_hash else "not_available")
        wl_certified = bool(wl_ok and cert_ok and wl_hash and wl_hash != "N/A")

        return "ok", {
            "k": k_str,
            "grade_type": g_obj.semantic_type,
            "symbolic_scale": g_obj.symbolic_expression(),
            "scale_A": mpmath.nstr(scale_A, n=dps),
            "zero_family": zero_fam,
            "nontrivial_index": str(z_1based),
            "zero_index": str(zero_idx),
            "gamma": gamma_str,
            "delta": delta_str,
            "source_zero_certificate_status": src_status,
            "source_zero_cert_hash": cert_hash or "N/A",
            "worldline_certificate_status": wl_status,
            "worldline_cert_hash": wl_hash or "N/A",
            "worldline_certified": "true" if wl_certified else "false",
            "certificate_verified": "true" if wl_certified else "false",
            "worldline_s_re": mpmath.nstr(s_world.real, n=dps),
            "worldline_s_im": mpmath.nstr(s_world.imag, n=dps),
            "sigma_c": mpmath.nstr(sigma_c, n=dps),
            "radial_leaf": mpmath.nstr(radial_leaf, n=dps),
            "signed_defect": mpmath.nstr(signed_defect, n=dps),
            "expected_signed_defect": mpmath.nstr(expected_signed_defect, n=dps),
            "signed_defect_error": mpmath.nstr(signed_defect_error, n=dps),
            "abs_defect": mpmath.nstr(abs_defect, n=dps),
            "expected_abs_defect": mpmath.nstr(expected_abs_defect, n=dps),
            "defect_scaling_error": mpmath.nstr(defect_scaling_error, n=dps),
            "radial_residual": mpmath.nstr(radial_residual, n=dps),
            "max_residual": mpmath.nstr(max_res, n=dps),
            "residual": mpmath.nstr(max_res, n=dps)
        }, None


class TrivialWorldlinesHandler(ExperimentHandler):
    @property
    def experiment_id(self) -> str:
        return "trivial-worldlines-001"

    @property
    def declared_dependencies(self) -> HandlerDependencies:
        return HandlerDependencies(
            common_modules=["research_runner.py", "research/handlers/base.py"],
            handler_modules=["research/handlers/worldlines.py"],
            math_modules=["transcendental.py", "math_core.py"],
            data_files=[],
            consumed_certificates=["data/certificates/trivial_zeros/*.json", "data/certificates/worldlines/*.json"],
            material_packages=["mpmath", "flint"]
        )

    def evaluate_point(
        self,
        inputs: Dict[str, str],
        dps: int = 80,
        param_space: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Dict[str, str], Optional[str]]:
        m_idx = int(inputs.get("trivial_index", inputs.get("m", inputs.get("zero_index", "1"))))
        if m_idx < 1:
            m_idx = int(inputs.get("zero_index", 0)) + 1
        k_str = inputs.get("k", inputs.get("K", "0"))
        grade_type = inputs.get("grade_type", "auto")

        cert_hash, cert_ok, zc, errs = _lookup_zero_certificate(
            m_idx,
            zero_family="trivial"
        )
        if not cert_ok:
            return "error", {}, f"Trivial zero #{m_idx} certificate verification failed: {errs}"

        grade_int = int(k_str) if k_str.lstrip("-+").isdigit() else 0
        s_exact = -2 * m_idx

        wl_hash, wl_ok, wlc, wl_errs = _lookup_worldline_certificate(
            zero_family="trivial",
            index=m_idx,
            grade=grade_int,
            delta="0.0"
        )

        g_obj = transcendental.parse_grade(k_str, grade_type=grade_type)
        scale_A = g_obj.numeric_scale(dps=dps + 15)

        s_world = mpmath.mpc(s_exact, 0) * scale_A
        sigma_c = transcendental.critical_surface_sigma(g_obj, dps=dps + 15)
        radial_leaf = (s_world.real / scale_A) - mpmath.mpf("0.5")
        expected_R = mpmath.mpf(s_exact) - mpmath.mpf("0.5")

        leaf_inv_err = abs(radial_leaf - expected_R)
        z_world = transcendental.evaluate_extended_zeta(s_world, grade=g_obj, dps=dps + 15)
        zeta_res = abs(z_world)
        max_res = max(zeta_res, leaf_inv_err)

        src_status = "certified" if cert_ok else ("verification_failed" if cert_hash else "not_available")
        wl_status = "certified" if wl_ok else ("verification_failed" if wl_hash else "not_available")
        wl_certified = bool(wl_ok and cert_ok and wl_hash and wl_hash != "N/A")

        return "ok", {
            "k": k_str,
            "grade_type": g_obj.semantic_type,
            "symbolic_scale": g_obj.symbolic_expression(),
            "scale_A": mpmath.nstr(scale_A, n=dps),
            "zero_family": "trivial",
            "trivial_index": str(m_idx),
            "exact_s": str(s_exact),
            "source_zero_certificate_status": src_status,
            "source_zero_cert_hash": cert_hash or "N/A",
            "worldline_certificate_status": wl_status,
            "worldline_cert_hash": wl_hash or "N/A",
            "worldline_certified": "true" if wl_certified else "false",
            "certificate_verified": "true" if wl_certified else "false",
            "worldline_s_re": mpmath.nstr(s_world.real, n=dps),
            "worldline_s_im": mpmath.nstr(s_world.imag, n=dps),
            "sigma_c": mpmath.nstr(sigma_c, n=dps),
            "radial_leaf": mpmath.nstr(radial_leaf, n=dps),
            "expected_radial_leaf": mpmath.nstr(expected_R, n=dps),
            "zeta_residual": mpmath.nstr(zeta_res, n=dps),
            "radial_residual": mpmath.nstr(leaf_inv_err, n=dps),
            "max_residual": mpmath.nstr(max_res, n=dps),
            "residual": mpmath.nstr(max_res, n=dps)
        }, None
