"""
research_runner.py — Reproducible Finite Hypothesis Sweep Runner

Conforms strictly to EXPERIMENT_PROTOCOL.md:
- Declarative YAML experiment spec validation.
- Deterministic parameter-space expansion (explicit, linear, log, Cartesian product).
- Strict reuse of canonical math engine (math_core, transforms, converter, zero_finder).
- Incremental JSONL streaming with resume and refusal of mismatched state.
- Authoritative high-precision values preserved as decimal strings.
- Machine-readable manifest.json, summary.json, results.jsonl, and human README.md.
- Continuous maintenance of research/index.json for AI-agent review.
"""

from __future__ import annotations
import os
import sys
import json
import yaml  # type: ignore[import]
import time

import hashlib
import itertools
import glob
import shutil
import subprocess
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple, Optional, Union, Set
import mpmath

import math_core
import transforms
import converter
import zero_finder
import reference_data
import transcendental
import certification

from research.handlers.registry import get_handler, list_registered_handlers, register_handler
from research.handlers.base import ExperimentHandler, HandlerDependencies


REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
RESEARCH_DIR = os.path.join(REPO_ROOT, "research")
EXPERIMENTS_DIR = os.path.join(RESEARCH_DIR, "experiments")
RUNS_DIR = os.path.join(RESEARCH_DIR, "runs")
INDEX_FILE = os.path.join(RESEARCH_DIR, "index.json")
CERT_DIR = os.path.join(REPO_ROOT, "data", "certificates")

OPERATION_CERTIFICATE_OBLIGATIONS: Dict[str, Dict[str, Any]] = {
    # 1. Transcendental Worldlines
    "transcendental_worldline": {
        "requires_consumed_certs": True,
        "requires_source_cert": True,
        "source_family": "nontrivial",
        "expected_source_status": "simple_zero_certified",
        "requires_worldline_cert": True,
        "expected_worldline_status": "worldline_certified",
        "requires_certified_flag": True,
        "is_synthetic": False
    },
    # 2. Trivial Zero Worldlines
    "trivial_worldlines": {
        "requires_consumed_certs": True,
        "requires_source_cert": True,
        "source_family": "trivial",
        "expected_source_status": "simple_zero_certified",
        "requires_worldline_cert": True,
        "expected_worldline_status": "worldline_certified",
        "requires_certified_flag": True,
        "is_synthetic": False
    },
    "trivial_worldline": {
        "requires_consumed_certs": True,
        "requires_source_cert": True,
        "source_family": "trivial",
        "expected_source_status": "simple_zero_certified",
        "requires_worldline_cert": True,
        "expected_worldline_status": "worldline_certified",
        "requires_certified_flag": True,
        "is_synthetic": False
    },
    "trivial_zero_worldlines": {
        "requires_consumed_certs": True,
        "requires_source_cert": True,
        "source_family": "trivial",
        "expected_source_status": "simple_zero_certified",
        "requires_worldline_cert": True,
        "expected_worldline_status": "worldline_certified",
        "requires_certified_flag": True,
        "is_synthetic": False
    },
    # 3. Synthetic Radial Leaves
    "synthetic_radial_leaf": {
        "requires_consumed_certs": True,
        "requires_source_cert": True,
        "source_family": "nontrivial",
        "expected_source_status": "simple_zero_certified",
        "requires_worldline_cert": True,
        "expected_worldline_status": "worldline_certified",
        "requires_certified_flag": True,
        "is_synthetic": True
    },
    "synthetic_radial_leaves": {
        "requires_consumed_certs": True,
        "requires_source_cert": True,
        "source_family": "nontrivial",
        "expected_source_status": "simple_zero_certified",
        "requires_worldline_cert": True,
        "expected_worldline_status": "worldline_certified",
        "requires_certified_flag": True,
        "is_synthetic": True
    },
    # 4. Cross-Height Coherence / Path Coherence
    "cross_height_coherence": {
        "requires_consumed_certs": True,
        "requires_source_cert": True,
        "source_family": "nontrivial",
        "expected_source_status": "simple_zero_certified",
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    "cross_height_path_coherence": {
        "requires_consumed_certs": True,
        "requires_source_cert": True,
        "source_family": "nontrivial",
        "expected_source_status": "simple_zero_certified",
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    # 5. Cross-Height Distance
    "cross_height_distance": {
        "requires_consumed_certs": True,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    # 6. Centered Dilation Zero Map / Transform Zero Map
    "transform_zero_map": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    "centered_dilation_zero_map": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    # 7. Centrifuge / Centrifuge Slope
    "centrifuge": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    "centrifuge_slope": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    # 8. Coupled Perturbation Covariance
    "coupled_perturbation_covariance": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    # 9. Coupled Scale Covariance / Zeta Trace Compare
    "zeta_trace_compare": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    "coupled_scale_covariance": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    # 10. Grade Constraints / Grade Constraint
    "grade_constraint": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    "grade_constraints": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    # 11. Inverse Kernel Lock / Kernel Identity
    "kernel_identity": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    "inverse_kernel_lock": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    # 12. Isolated Radial Response / Converter Perturbation
    "converter_perturbation": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    "isolated_radial_response": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    # 13. Symmetric Centrifuge / Symmetric Centrifuge Defect
    "symmetric_centrifuge": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    "symmetric_centrifuge_defect": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    # 14. Explicit Formula Native Baseline
    "explicit_formula_native_baseline": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    # 15. Explicit Formula Grade Covariance & Expanded-Basis Equivalence
    "explicit_formula_grade_covariance": {
        "requires_consumed_certs": False,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    },
    # 16. Explicit Formula Perturbation & Linearized Compensation
    "explicit_formula_perturbation_rank": {
        "requires_consumed_certs": True,
        "requires_source_cert": False,
        "requires_worldline_cert": False,
        "requires_certified_flag": False,
        "is_synthetic": False
    }
}


def hash_file_bytes(filepath: str) -> str:
    """Compute SHA-256 hash of a file after normalizing CRLF line endings to LF."""
    if not os.path.exists(filepath):
        return "N/A"
    with open(filepath, "rb") as f:
        data = f.read()
    normalized = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(normalized).hexdigest()


def hash_string(text: str) -> str:
    """Compute SHA-256 hash of a string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_git_info(cwd: Optional[str] = None) -> Tuple[str, bool]:
    """Retrieve current Git commit SHA and dirty state."""
    work_dir = cwd or os.path.dirname(os.path.abspath(__file__))
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=work_dir,
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
    except Exception:
        commit = "UNKNOWN"

    try:
        status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=work_dir,
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        dirty_lines = []
        for line in status.splitlines():
            line_str = line.strip()
            if not line_str:
                continue
            parts = line_str.split(None, 1)
            if len(parts) < 2:
                dirty_lines.append(line_str)
                continue
            path = parts[1].strip().strip('"').replace("\\", "/")
            if path in ("research/index.json", "formal/build_report.json") or path.startswith("research/runs/") or path.startswith("data/certificates/"):
                continue

            dirty_lines.append(line_str)
        is_dirty = len(dirty_lines) > 0
    except Exception:
        is_dirty = False

    return commit, is_dirty


def validate_spec(spec: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate experiment spec against EXPERIMENT_PROTOCOL.md §3 schema.
    Returns (is_valid, error_message).
    """
    required_top = ["schema_version", "id", "title", "hypothesis", "criterion", "engine", "parameters", "precision"]
    for field in required_top:
        if field not in spec:
            return False, f"Missing required spec field: '{field}'"

    if not isinstance(spec["hypothesis"], dict) or "statement" not in spec["hypothesis"]:
        return False, "Spec missing 'hypothesis.statement'"

    crit = spec["criterion"]
    if not isinstance(crit, dict) or "metric" not in crit:
        return False, "Spec 'criterion' must be a mapping defining at least 'metric'"

    aggregation = crit.get("aggregation", "max_abs")
    valid_aggs = ["max_abs", "max", "min", "all", "none"]
    if aggregation not in valid_aggs:
        return False, f"Invalid criterion aggregation '{aggregation}', must be one of {valid_aggs}"

    if aggregation != "none":
        if "operator" not in crit or "threshold" not in crit:
            return False, "Spec 'criterion' with active aggregation must define 'operator' and 'threshold'"
        valid_ops = ["<=", "<", ">=", ">", "==", "!="]
        if crit["operator"] not in valid_ops:
            return False, f"Invalid criterion operator '{crit['operator']}', must be one of {valid_ops}"

    engine = spec["engine"]
    if not isinstance(engine, dict) or "operation" not in engine:
        return False, "Spec missing 'engine.operation'"

    valid_engine_ops = [
        "centrifuge",
        "kernel_identity",
        "transform_zero_map",
        "zeta_trace_compare",
        "converter_perturbation",
        "symmetric_centrifuge",
        "coupled_perturbation_covariance",
        "coupled_scale_covariance",
        "transcendental_worldline",
        "trivial_zero_worldlines",
        "synthetic_radial_leaf",
        "cross_height_coherence",
        "cross_height_distance",
        "grade_constraint",
        "explicit_formula_native_baseline",
        "explicit_formula_grade_covariance",
        "explicit_formula_perturbation_rank",
        "explicit_formula_radial_second_variation"
    ]
    if engine["operation"] not in valid_engine_ops:
        return False, f"Unknown engine operation '{engine['operation']}'. Permitted: {valid_engine_ops}"

    params = spec["parameters"]
    if not isinstance(params, dict) or len(params) == 0:
        return False, "Spec 'parameters' must be a non-empty mapping of parameter names"

    for p_name, p_def in params.items():
        if not isinstance(p_def, dict) or "kind" not in p_def:
            return False, f"Parameter '{p_name}' missing 'kind'"
        kind = p_def["kind"]
        if kind == "explicit":
            if "values" not in p_def or not isinstance(p_def["values"], list) or len(p_def["values"]) == 0:
                return False, f"Explicit parameter '{p_name}' requires non-empty 'values' list"
        elif kind == "linear":
            for req in ["start", "stop", "step"]:
                if req not in p_def:
                    return False, f"Linear parameter '{p_name}' requires '{req}'"
        elif kind == "log":
            if "exponents" not in p_def or not isinstance(p_def["exponents"], list) or len(p_def["exponents"]) == 0:
                return False, f"Log parameter '{p_name}' requires non-empty 'exponents' list"
        elif kind == "integer_grade":
            for req in ["start", "stop"]:
                if req not in p_def:
                    return False, f"Integer grade parameter '{p_name}' requires '{req}'"
        elif kind == "rational_grade":
            if "values" not in p_def or not isinstance(p_def["values"], list) or len(p_def["values"]) == 0:
                return False, f"Rational grade parameter '{p_name}' requires non-empty 'values' list"
        else:
            return False, f"Unknown parameter kind '{kind}' for parameter '{p_name}'"

    prec = spec["precision"]
    if not isinstance(prec, dict) or "dps" not in prec or not isinstance(prec["dps"], int) or prec["dps"] <= 0:
        return False, "Spec 'precision.dps' must be a positive integer"

    return True, None


def expand_parameter(p_def: Dict[str, Any], dps: int = 80) -> List[str]:
    """
    Expand a single parameter definition into a deterministic list of decimal strings.
    Uses exact high-precision stepping without binary float downcast.
    """
    kind = p_def["kind"]
    with mpmath.workdps(dps + 15):
        if kind == "explicit":
            return [str(v).strip() for v in p_def["values"]]

        elif kind == "linear":
            start = mpmath.mpf(str(p_def["start"]).strip())
            stop = mpmath.mpf(str(p_def["stop"]).strip())
            step = mpmath.mpf(str(p_def["step"]).strip())

            if step <= 0 and start < stop:
                raise ValueError("Positive step required when start < stop")
            if step >= 0 and start > stop:
                raise ValueError("Negative step required when start > stop")

            values = []
            curr = start
            eps = abs(step) * mpmath.mpf("1e-12")
            if step > 0:
                while curr <= stop + eps:
                    values.append(mpmath.nstr(curr, n=dps, strip_zeros=False))
                    curr += step
            else:
                while curr >= stop - eps:
                    values.append(mpmath.nstr(curr, n=dps, strip_zeros=False))
                    curr += step
            return values

        elif kind == "log":
            base_str = str(p_def.get("base", "10")).strip()
            base = mpmath.mpf(base_str)
            values = []
            for exp_str in p_def["exponents"]:
                exp_val = mpmath.mpf(str(exp_str).strip())
                val = mpmath.power(base, exp_val)
                values.append(mpmath.nstr(val, n=dps, strip_zeros=False))
            return values

        elif kind == "integer_grade":
            start_k = int(p_def["start"])
            stop_k = int(p_def["stop"])
            step_k = int(p_def.get("step", 1))
            step_dir = 1 if step_k > 0 else -1
            return [str(k) for k in range(start_k, stop_k + step_dir, step_k)]

        elif kind == "rational_grade":
            return [str(v).strip() for v in p_def["values"]]

        else:
            raise ValueError(f"Unsupported parameter kind '{kind}'")


def generate_parameter_grid(
    parameters_def: Dict[str, Dict[str, Any]],
    dps: int = 80
) -> List[Dict[str, str]]:
    """
    Generate deterministic Cartesian product of all parameters in declared parameter order.
    Returns list of dictionaries mapping param_name -> decimal string value.
    """
    param_names = list(parameters_def.keys())
    param_values_list = [expand_parameter(parameters_def[name], dps=dps) for name in param_names]

    grid = []
    for combination in itertools.product(*param_values_list):
        point_dict = {name: val for name, val in zip(param_names, combination)}
        grid.append(point_dict)

    return grid


# ==============================================================================
# CANONICAL ENGINE DISPATCH (Strictly delegates to canonical math modules)
# ==============================================================================

def _lookup_zero_certificate(
    zero_index: int,
    zero_family: str = "nontrivial",
    expected_ordinate: Optional[Union[str, float, mpmath.mpf]] = None,
    check_provenance: bool = True,
    canonical_current: bool = False
) -> Tuple[Optional[str], bool, Optional[Dict[str, Any]], List[str]]:
    """Look up zero certificate by 1-based index and family, and verify all mathematical and provenance claims."""
    code_root = os.path.dirname(os.path.abspath(__file__))
    if zero_family == "nontrivial":
        cert_path = os.path.join(code_root, "data", "certificates", "zeros", f"zero_{zero_index:05d}.json")
    elif zero_family == "trivial":
        cert_path = os.path.join(code_root, "data", "certificates", "trivial_zeros", f"trivial_zero_{zero_index:05d}.json")
    else:
        return None, False, None, [f"Unknown zero_family: {zero_family}"]

    if not os.path.exists(cert_path):
        return None, False, None, [f"Certificate file '{cert_path}' does not exist"]

    try:
        with open(cert_path, "r", encoding="utf-8") as f:
            zc = json.load(f)
    except Exception as e:
        return None, False, None, [f"Failed to read certificate JSON: {e}"]

    cert_fam = zc.get("zero_family", "nontrivial" if zc.get("certificate_type") == "zero_isolation_and_simplicity" else "trivial")
    if cert_fam != zero_family:
        return zc.get("certificate_hash"), False, zc, [f"Zero family mismatch: requested {zero_family}, certificate has {cert_fam}"]

    c_idx = zc.get("nontrivial_index") if zero_family == "nontrivial" else zc.get("trivial_index")
    if c_idx is None:
        c_idx = zc.get("zero_index") if zero_family == "nontrivial" else zc.get("exact_location", 0) // -2
    if c_idx != zero_index:
        return zc.get("certificate_hash"), False, zc, [f"Zero index mismatch: requested {zero_index}, certificate has {c_idx}"]

    if zc.get("status") not in ("simple_zero_certified", "isolated_zero_certified"):
        return zc.get("certificate_hash"), False, zc, [f"Certificate status is not certified: {zc.get('status')}"]

    if expected_ordinate is not None and zero_family == "nontrivial":
        exp_ord = mpmath.mpf(expected_ordinate)
        enc = zc.get("enclosure", {})
        re_mid = enc.get("imag_mid")
        re_rad = enc.get("imag_rad", "1e-50")
        if re_mid:
            mid_val = mpmath.mpf(re_mid)
            rad_val = mpmath.mpf(re_rad)
            if abs(exp_ord - mid_val) > (rad_val + mpmath.mpf("1e-4")):
                return zc.get("certificate_hash"), False, zc, [f"Ordinate mismatch: expected {expected_ordinate}, certificate has {re_mid}"]

    ok, errs = certification.verify_certificate(zc, check_provenance=check_provenance, canonical_current=canonical_current)
    if not ok:
        return zc.get("certificate_hash"), False, zc, errs

    return zc.get("certificate_hash"), True, zc, []


def _lookup_worldline_certificate(
    zero_family: str,
    index: int,
    grade: int,
    delta: str = "0.0",
    check_provenance: bool = True,
    canonical_current: bool = False
) -> Tuple[Optional[str], bool, Optional[Dict[str, Any]], List[str]]:
    """Look up and strictly verify a worldline certificate from data/certificates/worldlines/."""
    code_root = os.path.dirname(os.path.abspath(__file__))
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



OPERATION_TO_EXPERIMENT_ID: Dict[str, str] = {
    "dilation_zero_map": "centered-dilation-zero-map",
    "transform_zero_map": "centered-dilation-zero-map",
    "centered_dilation_zero_map": "centered-dilation-zero-map",
    "centered-dilation-zero-map": "centered-dilation-zero-map",
    "centrifuge": "centrifuge-slope-verification",
    "centrifuge_slope": "centrifuge-slope-verification",
    "centrifuge-slope-verification": "centrifuge-slope-verification",
    "symmetric_centrifuge": "symmetric-centrifuge-defect-001",
    "symmetric_centrifuge_defect": "symmetric-centrifuge-defect-001",
    "symmetric-centrifuge-defect-001": "symmetric-centrifuge-defect-001",
    "coupled_perturbation_covariance": "coupled-perturbation-covariance-001",
    "coupled-perturbation-covariance-001": "coupled-perturbation-covariance-001",
    "zeta_trace_compare": "coupled-scale-covariance-001",
    "coupled_scale_covariance": "coupled-scale-covariance-001",
    "coupled-scale-covariance-001": "coupled-scale-covariance-001",
    "cross_height_distance": "cross-height-distance-001",
    "cross-height-distance-001": "cross-height-distance-001",
    "cross_height_coherence": "cross-height-path-coherence-001",
    "cross_height_path_coherence": "cross-height-path-coherence-001",
    "cross-height-path-coherence-001": "cross-height-path-coherence-001",
    "explicit_formula_native_baseline": "explicit-formula-native-baseline-001",
    "explicit-formula-native-baseline-001": "explicit-formula-native-baseline-001",
    "explicit_formula_grade_covariance": "explicit-formula-grade-covariance-001",
    "explicit-formula-grade-covariance-001": "explicit-formula-grade-covariance-001",
    "explicit_formula_perturbation_rank": "explicit-formula-perturbation-rank-001",
    "explicit-formula-perturbation-rank-001": "explicit-formula-perturbation-rank-001",
    "explicit_formula_radial_second_variation": "explicit-formula-radial-second-variation-001",
    "explicit-formula-radial-second-variation-001": "explicit-formula-radial-second-variation-001",
    "grade_constraint": "grade-constraints-001",
    "grade_constraints": "grade-constraints-001",
    "grade-constraints-001": "grade-constraints-001",
    "kernel_identity": "inverse-kernel-lock-identity",
    "inverse_kernel_lock": "inverse-kernel-lock-identity",
    "inverse-kernel-lock-identity": "inverse-kernel-lock-identity",
    "converter_perturbation": "isolated-radial-response-002",
    "isolated_radial_response": "isolated-radial-response-002",
    "isolated-radial-response-002": "isolated-radial-response-002",
    "synthetic_radial_leaf": "synthetic-radial-leaves-001",
    "synthetic_radial_leaves": "synthetic-radial-leaves-001",
    "synthetic-radial-leaves-001": "synthetic-radial-leaves-001",
    "transcendental_worldline": "transcendental-worldlines-001",
    "transcendental_worldlines": "transcendental-worldlines-001",
    "transcendental-worldlines-001": "transcendental-worldlines-001",
    "trivial_zero_worldlines": "trivial-worldlines-001",
    "trivial_worldlines": "trivial-worldlines-001",
    "trivial-worldlines-001": "trivial-worldlines-001",
}


def evaluate_point(
    operation: str,
    inputs: Dict[str, str],
    dps: int = 80,
    param_space: Optional[Dict[str, Any]] = None
) -> Tuple[str, Dict[str, str], Optional[str]]:
    """
    Evaluate a single parameter space point using the registered experiment handler or canonical math engine.
    Returns (status, outputs_dict, error_message).
    All outputs serialize as exact decimal strings.
    """
    exp_id = OPERATION_TO_EXPERIMENT_ID.get(operation, operation)
    try:
        handler = get_handler(exp_id)
        with mpmath.workdps(dps + 15):
            return handler.evaluate_point(inputs, dps=dps, param_space=param_space)
    except KeyError:
        pass
    except Exception as e:
        return "error", {}, str(e)

    with mpmath.workdps(dps + 15):
        try:
            if operation == "centrifuge":
                delta_str = inputs.get("delta", "0.0")
                gamma_str = inputs.get("gamma", "14.13472514173469379045725198356247027078425711569924317568556746")
                k_str = inputs.get("K", inputs.get("k", "0.0"))

                log_mod = math_core.centrifuge_log_modulus(delta_str, k_str, dps=dps)
                q_k = math_core.centrifuge_q_k(delta_str, gamma_str, k_str, dps=dps)
                abs_q_k = abs(q_k)

                tau = math_core.get_tau(dps=dps)
                d_mpf = math_core.to_mpf(delta_str, dps=dps)
                k_mpf = math_core.to_mpf(k_str, dps=dps)
                expected_log_mod = k_mpf * d_mpf * mpmath.log(tau)
                abs_slope_error = abs(log_mod - expected_log_mod)

                return "ok", {
                    "log_modulus": mpmath.nstr(log_mod, n=dps),
                    "abs_q_k": mpmath.nstr(abs_q_k, n=dps),
                    "expected_log_modulus": mpmath.nstr(expected_log_mod, n=dps),
                    "abs_slope_error": mpmath.nstr(abs_slope_error, n=dps),
                    "residual": mpmath.nstr(abs_slope_error, n=dps)
                }, None

            elif operation == "kernel_identity":
                A_str = inputs.get("A", "1.0")
                is_lock = inputs.get("inverse_scale_lock", "true").lower() in ["true", "1", "yes"]
                B_str = inputs.get("B", "1.0")
                C_str = inputs.get("C", "0.0")
                D_str = inputs.get("D", "0.0")

                s_re = inputs.get("s_re", inputs.get("re_s", "0.5"))
                s_im = inputs.get("s_im", inputs.get("im_s", "14.134725141734693790457251983562"))
                s_mpc = math_core.to_mpc((s_re, s_im), dps=dps)

                t_obj_kernel = transforms.KernelTransform(
                    A=A_str, B=B_str, C=C_str, D=D_str, inverse_scale_lock=is_lock
                )

                z_trans = t_obj_kernel.evaluate_function(s_mpc, dps=dps)
                z_canon = math_core.zeta_eval(s_mpc, dps=dps)
                abs_diff = abs(z_trans - z_canon)

                return "ok", {
                    "transformed_re": mpmath.nstr(z_trans.real, n=dps),
                    "transformed_im": mpmath.nstr(z_trans.imag, n=dps),
                    "canonical_re": mpmath.nstr(z_canon.real, n=dps),
                    "canonical_im": mpmath.nstr(z_canon.imag, n=dps),
                    "abs_diff": mpmath.nstr(abs_diff, n=dps),
                    "residual": mpmath.nstr(abs_diff, n=dps)
                }, None

            elif operation == "transform_zero_map":
                mode = inputs.get("mode", "centered_dilation")
                k_str = inputs.get("k", "1.0")
                gamma_str = inputs.get("gamma", "14.13472514173469379045725198356247027078425711569924317568556746")

                t_obj_map: transforms.BaseTransform
                if mode == "origin_dilation":
                    t_obj_map = transforms.OriginCoordinateDilation(k=k_str)
                elif mode == "argument":
                    t_obj_map = transforms.ArgumentTransform(k=k_str)
                else:
                    t_obj_map = transforms.CenteredCoordinateDilation(k=k_str)

                rho = mpmath.mpc('0.5', gamma_str)
                mapped_rho = t_obj_map.map_zero_mpc(rho, dps=dps)
                val_at_mapped = t_obj_map.evaluate_function(mapped_rho, dps=dps)

                residual = abs(val_at_mapped)

                return "ok", {
                    "mapped_rho_re": mpmath.nstr(mapped_rho.real, n=dps),
                    "mapped_rho_im": mpmath.nstr(mapped_rho.imag, n=dps),
                    "val_re": mpmath.nstr(val_at_mapped.real, n=dps),
                    "val_im": mpmath.nstr(val_at_mapped.imag, n=dps),
                    "residual": mpmath.nstr(residual, n=dps),
                    "max_residual": mpmath.nstr(residual, n=dps)
                }, None

            elif operation == "zeta_trace_compare":
                k_str = inputs.get("k", inputs.get("K", "0.0"))
                s_re_str = inputs.get("s_re", inputs.get("sigma", inputs.get("re_s", None)))
                if s_re_str is None:
                    if "delta" in inputs:
                        s_re_str = str(mpmath.mpf('0.5') + math_core.to_mpf(inputs["delta"], dps=dps + 10))
                    else:
                        s_re_str = "0.5"
                s_im_str = inputs.get("s_im", inputs.get("t", inputs.get("gamma", inputs.get("im_s", "14.13472514173469379045725198356247027078425711569924317568556746"))))

                s_mpc = mpmath.mpc(s_re_str, s_im_str)
                tau = math_core.get_tau(dps=dps + 10)
                k_mpf = math_core.to_mpf(k_str, dps=dps + 10)
                scale_A = mpmath.power(tau, k_mpf)

                mapped_s = scale_A * s_mpc
                W = math_core.zeta_eval(s_mpc, dps=dps + 10)

                t_orig = transforms.OriginCoordinateDilation(k=k_str)
                W_A = t_orig.evaluate_function(mapped_s, dps=dps + 10)

                E_zeta = abs(W_A - W)
                sigma_c = mpmath.mpf('0.5')
                sigma_c_prime = scale_A / 2

                outputs = {
                    "s_re": mpmath.nstr(s_mpc.real, n=dps),
                    "s_im": mpmath.nstr(s_mpc.imag, n=dps),
                    "k": k_str,
                    "scale_A": mpmath.nstr(scale_A, n=dps),
                    "mapped_s_re": mpmath.nstr(mapped_s.real, n=dps),
                    "mapped_s_im": mpmath.nstr(mapped_s.imag, n=dps),
                    "baseline_re": mpmath.nstr(W.real, n=dps),
                    "baseline_im": mpmath.nstr(W.imag, n=dps),
                    "transformed_re": mpmath.nstr(W_A.real, n=dps),
                    "transformed_im": mpmath.nstr(W_A.imag, n=dps),
                    "sigma_c": mpmath.nstr(sigma_c, n=dps),
                    "sigma_c_prime": mpmath.nstr(sigma_c_prime, n=dps),
                    "zeta_covariance_residual": mpmath.nstr(E_zeta, n=dps),
                    "covariance_residual": mpmath.nstr(E_zeta, n=dps),
                    "residual": mpmath.nstr(E_zeta, n=dps)
                }

                if "x" in inputs or "rho" in inputs or "gamma" in inputs or "rho_im" in inputs:
                    x_str = inputs.get("x", "10.0")
                    x_mpf = math_core.to_mpf(x_str, dps=dps + 10)
                    rho_re = inputs.get("rho_re", "0.5")
                    rho_im = inputs.get("rho_im", inputs.get("gamma", inputs.get("rho", "14.13472514173469379045725198356247027078425711569924317568556746")))
                    rho_mpc = math_core.to_mpc((rho_re, rho_im), dps=dps + 10)

                    mapped_rho = scale_A * rho_mpc
                    mapped_x = mpmath.power(x_mpf, mpmath.mpf(1) / scale_A)

                    cj_clean = converter.zero_j_contribution_audit(x_mpf, rho_mpc, dps=dps + 10)
                    cj_trans = converter.zero_j_contribution_audit(mapped_x, mapped_rho, dps=dps + 10)
                    e_cj = abs(cj_trans - cj_clean)

                    outputs["x"] = mpmath.nstr(x_mpf, n=dps)
                    outputs["mapped_x"] = mpmath.nstr(mapped_x, n=dps)
                    outputs["rho_re"] = mpmath.nstr(rho_mpc.real, n=dps)
                    outputs["rho_im"] = mpmath.nstr(rho_mpc.imag, n=dps)
                    outputs["mapped_rho_re"] = mpmath.nstr(mapped_rho.real, n=dps)
                    outputs["mapped_rho_im"] = mpmath.nstr(mapped_rho.imag, n=dps)
                    outputs["cj_clean"] = mpmath.nstr(cj_clean, n=dps)
                    outputs["cj_transformed"] = mpmath.nstr(cj_trans, n=dps)
                    outputs["cj_covariance_residual"] = mpmath.nstr(e_cj, n=dps)

                    if 2 <= mapped_x <= 100000 and 2 <= x_mpf <= 100000:
                        cpi_clean = converter.zero_pi_contribution_audit(x_mpf, rho_mpc, dps=dps + 10, max_m=50)
                        cpi_trans = converter.zero_pi_contribution_audit(mapped_x, mapped_rho, dps=dps + 10, max_m=50)
                        e_cpi = abs(cpi_trans - cpi_clean)
                        outputs["cpi_clean"] = mpmath.nstr(cpi_clean, n=dps)
                        outputs["cpi_transformed"] = mpmath.nstr(cpi_trans, n=dps)
                        outputs["cpi_covariance_residual"] = mpmath.nstr(e_cpi, n=dps)

                    max_cov_res = max(E_zeta, e_cj)
                    outputs["covariance_residual"] = mpmath.nstr(max_cov_res, n=dps)
                    outputs["residual"] = mpmath.nstr(max_cov_res, n=dps)

                return "ok", outputs, None

            elif operation == "converter_perturbation":
                zero_idx = int(inputs.get("zero_index", inputs.get("n", "0")))
                delta_str = inputs.get("delta", "0.0")
                x_str = inputs.get("x", "20.0")
                num_zeros = int(inputs.get("num_zeros", "10"))
                mode = inputs.get("perturbation_mode", inputs.get("mode", "single_pair_diagnostic"))

                ref_zeros_str = reference_data.load_reference_zeros()[:max(num_zeros, zero_idx + 1)]
                if not ref_zeros_str:
                    ref_zeros_str = ["14.13472514173469379045725198356247027078425711569924317568556746"]

                gamma_str = inputs.get("gamma", ref_zeros_str[zero_idx] if zero_idx < len(ref_zeros_str) else ref_zeros_str[0])
                rho_clean = mpmath.mpc('0.5', gamma_str)

                contrib_dict = converter.compute_perturbed_contributions_audit(
                    x_str, rho_clean, delta_str, mode=mode, dps=dps + 15
                )

                clean_zeros_mpc = [mpmath.mpc('0.5', g) for g in ref_zeros_str[:num_zeros]]
                pert_rhos = contrib_dict["perturbed_rhos"]

                if mode in ("symmetry_complete_split", "symmetry_complete_quartet"):
                    clean_for_recon = clean_zeros_mpc[:zero_idx] + [rho_clean, rho_clean] + clean_zeros_mpc[zero_idx + 1:]
                    modified_zeros_mpc = clean_zeros_mpc[:zero_idx] + pert_rhos + clean_zeros_mpc[zero_idx + 1:]
                else:
                    clean_for_recon = clean_zeros_mpc
                    modified_zeros_mpc = list(clean_zeros_mpc)
                    if 0 <= zero_idx < len(modified_zeros_mpc):
                        modified_zeros_mpc = clean_zeros_mpc[:zero_idx] + pert_rhos + clean_zeros_mpc[zero_idx + 1:]

                full_clean_pi = converter.riemann_explicit_pi_audit(x_str, clean_for_recon, dps=dps + 15)
                full_pert_pi = converter.riemann_explicit_pi_audit(x_str, modified_zeros_mpc, dps=dps + 15)
                full_diff = full_pert_pi - full_clean_pi

                x_mpf = math_core.to_mpf(x_str, dps=dps + 15)
                try:
                    true_pi_val = reference_data.prime_pi(float(x_mpf)) if x_mpf <= 100000 else "N/A"
                except Exception:
                    true_pi_val = "N/A"

                pert_rhos_str = "; ".join(f"{mpmath.nstr(r.real, n=dps)} + {mpmath.nstr(r.imag, n=dps)}j" for r in pert_rhos)
                d_mpf = math_core.to_mpf(delta_str, dps=dps + 15)

                outputs = {
                    "zero_index": str(zero_idx),
                    "gamma": mpmath.nstr(rho_clean.imag, n=dps),
                    "delta": delta_str,
                    "perturbation_mode": mode,
                    "clean_rho": f"{mpmath.nstr(rho_clean.real, n=dps)} + {mpmath.nstr(rho_clean.imag, n=dps)}j",
                    "perturbed_rhos": pert_rhos_str,
                    "x": mpmath.nstr(x_mpf, n=dps),
                    "clean_cj": mpmath.nstr(contrib_dict["cj_clean"], n=dps),
                    "perturbed_cj": mpmath.nstr(contrib_dict["cj_perturbed"], n=dps),
                    "clean_cpi": mpmath.nstr(contrib_dict["cpi_clean"], n=dps),
                    "perturbed_cpi": mpmath.nstr(contrib_dict["cpi_perturbed"], n=dps),
                    "full_clean_pi": mpmath.nstr(full_clean_pi, n=dps),
                    "full_perturbed_pi": mpmath.nstr(full_pert_pi, n=dps),
                    "full_reconstruction_diff": mpmath.nstr(full_diff, n=dps),
                    "true_pi": str(true_pi_val),
                    "residual": mpmath.nstr(abs(full_diff), n=dps)
                }

                if mode in ("symmetry_complete_split", "symmetry_complete_quartet"):
                    split_defect_cj = math_core.to_mpf(contrib_dict.get("split_defect_cj", contrib_dict.get("delta_cj", 0)), dps=dps + 15)
                    split_defect_cpi = math_core.to_mpf(contrib_dict.get("split_defect_cpi", contrib_dict.get("delta_cpi", 0)), dps=dps + 15)
                    split_defect_pi_n = full_diff

                    neg_contrib = converter.compute_perturbed_contributions_audit(
                        x_str, rho_clean, str(-d_mpf), mode=mode, dps=dps + 15
                    )
                    neg_s_cj = math_core.to_mpf(neg_contrib.get("split_defect_cj", neg_contrib.get("delta_cj", 0)), dps=dps + 15)
                    neg_s_cpi = math_core.to_mpf(neg_contrib.get("split_defect_cpi", neg_contrib.get("delta_cpi", 0)), dps=dps + 15)

                    sym_err_cj = abs(split_defect_cj - neg_s_cj)
                    sym_err_cpi = abs(split_defect_cpi - neg_s_cpi)
                    symmetry_error = max(sym_err_cj, sym_err_cpi)

                    outputs["split_defect_cj"] = mpmath.nstr(split_defect_cj, n=dps)
                    outputs["split_defect_cpi"] = mpmath.nstr(split_defect_cpi, n=dps)
                    outputs["split_defect_pi_n"] = mpmath.nstr(split_defect_pi_n, n=dps)
                    outputs["symmetry_error_cj"] = mpmath.nstr(sym_err_cj, n=dps)
                    outputs["symmetry_error_cpi"] = mpmath.nstr(sym_err_cpi, n=dps)
                    outputs["symmetry_error"] = mpmath.nstr(symmetry_error, n=dps)

                    if abs(d_mpf) > mpmath.mpf('1e-50'):
                        d_sq = d_mpf * d_mpf
                        norm_quad_cj = split_defect_cj / d_sq
                        norm_quad_cpi = split_defect_cpi / d_sq
                        outputs["normalized_quadratic_cj"] = mpmath.nstr(norm_quad_cj, n=dps)
                        outputs["normalized_quadratic_cpi"] = mpmath.nstr(norm_quad_cpi, n=dps)

                        declared_deltas_raw: Optional[List[Any]] = None
                        if param_space and "delta" in param_space:
                            declared_deltas_raw = expand_parameter(param_space["delta"], dps=dps)
                        elif "declared_deltas" in inputs:
                            val = inputs["declared_deltas"]
                            declared_deltas_raw = val if isinstance(val, list) else [val]

                        if declared_deltas_raw:
                            declared_deltas_mpf = [math_core.to_mpf(v, dps=dps + 15) for v in declared_deltas_raw]
                            half_d_mpf = d_mpf / 2
                            has_half_delta = any(abs(half_d_mpf - v) < mpmath.mpf('1e-25') for v in declared_deltas_mpf)
                            if has_half_delta:
                                half_contrib = converter.compute_perturbed_contributions_audit(
                                    x_str, rho_clean, str(half_d_mpf), mode=mode, dps=dps + 15
                                )
                                half_s_cj = math_core.to_mpf(half_contrib.get("split_defect_cj", half_contrib.get("delta_cj", 0)), dps=dps + 15)
                                half_s_cpi = math_core.to_mpf(half_contrib.get("split_defect_cpi", half_contrib.get("delta_cpi", 0)), dps=dps + 15)

                                if abs(half_s_cj) > mpmath.mpf('1e-50'):
                                    quad_ratio_cj = split_defect_cj / half_s_cj
                                    outputs["quadratic_ratio_cj"] = mpmath.nstr(quad_ratio_cj, n=dps)
                                    outputs["quadratic_ratio_error_cj"] = mpmath.nstr(abs(quad_ratio_cj - 4), n=dps)

                                if abs(half_s_cpi) > mpmath.mpf('1e-50'):
                                    quad_ratio_cpi = split_defect_cpi / half_s_cpi
                                    outputs["quadratic_ratio_cpi"] = mpmath.nstr(quad_ratio_cpi, n=dps)
                                    outputs["quadratic_ratio_error_cpi"] = mpmath.nstr(abs(quad_ratio_cpi - 4), n=dps)

                else:
                    delta_cj = math_core.to_mpf(contrib_dict.get("delta_cj", contrib_dict.get("split_defect_cj", 0)), dps=dps + 15)
                    delta_cpi = math_core.to_mpf(contrib_dict.get("delta_cpi", contrib_dict.get("split_defect_cpi", 0)), dps=dps + 15)
                    delta_pi_n = full_diff

                    outputs["delta_cj"] = mpmath.nstr(delta_cj, n=dps)
                    outputs["delta_cpi"] = mpmath.nstr(delta_cpi, n=dps)
                    outputs["delta_pi_n"] = mpmath.nstr(delta_pi_n, n=dps)

                return "ok", outputs, None

            elif operation == "symmetric_centrifuge":
                delta_str = inputs.get("delta", "0.0")
                gamma_str = inputs.get("gamma", "14.13472514173469379045725198356247027078425711569924317568556746")
                k_str = inputs.get("K", inputs.get("k", "0"))

                D_K = math_core.symmetric_centrifuge_defect(delta_str, gamma_str, k_str, dps=dps + 15)
                expected_abs_D_K = math_core.symmetric_centrifuge_defect_expected(delta_str, k_str, dps=dps + 15)
                abs_D_K = abs(D_K)
                identity_error = abs(abs_D_K - expected_abs_D_K)

                k_val = math_core.to_mpf(k_str, dps=dps + 15)
                d_val = math_core.to_mpf(delta_str, dps=dps + 15)
                tau = math_core.get_tau(dps=dps + 15)
                arg_scale = abs(k_val * d_val * mpmath.log(tau))

                if arg_scale > mpmath.mpf("1e-40"):
                    small_arg_ratio = abs_D_K / (k_val * d_val * mpmath.log(tau))**2
                    small_arg_ratio_str = mpmath.nstr(small_arg_ratio, n=dps)
                elif abs(d_val) < mpmath.mpf("1e-40") or abs(k_val) < mpmath.mpf("1e-40"):
                    small_arg_ratio_str = "1.0"
                else:
                    small_arg_ratio_str = "N/A"

                return "ok", {
                    "delta": delta_str,
                    "gamma": gamma_str,
                    "K": k_str,
                    "D_K_re": mpmath.nstr(D_K.real, n=dps),
                    "D_K_im": mpmath.nstr(D_K.imag, n=dps),
                    "abs_D_K": mpmath.nstr(abs_D_K, n=dps),
                    "expected_abs_D_K": mpmath.nstr(expected_abs_D_K, n=dps),
                    "identity_error": mpmath.nstr(identity_error, n=dps),
                    "small_arg_ratio": small_arg_ratio_str,
                    "residual": mpmath.nstr(identity_error, n=dps)
                }, None

            elif operation == "coupled_perturbation_covariance":
                zero_idx = int(inputs.get("zero_index", inputs.get("n", "0")))
                delta_str = inputs.get("delta", "0.0")
                k_str = inputs.get("k", inputs.get("K", "0"))
                x_str = inputs.get("x", "20.0")
                num_zeros = int(inputs.get("num_zeros", "10"))
                mode = inputs.get("perturbation_mode", inputs.get("mode", "single_pair_diagnostic"))

                ref_zeros_str = reference_data.load_reference_zeros()[:max(num_zeros, zero_idx + 1)]
                if not ref_zeros_str:
                    ref_zeros_str = ["14.13472514173469379045725198356247027078425711569924317568556746"]

                gamma_str = inputs.get("gamma", ref_zeros_str[zero_idx] if zero_idx < len(ref_zeros_str) else ref_zeros_str[0])

                k_val = math_core.to_mpf(k_str, dps=dps + 15)
                tau = math_core.get_tau(dps=dps + 15)
                A = mpmath.power(tau, k_val)
                x_mpf = math_core.to_mpf(x_str, dps=dps + 15)
                x_prime = mpmath.power(x_mpf, mpmath.mpf(1) / A)

                rho_clean = mpmath.mpc('0.5', gamma_str)
                rho_clean_prime = A * rho_clean
                d_val = math_core.to_mpf(delta_str, dps=dps + 15)

                clean_cj = converter.zero_j_contribution_audit(x_mpf, rho_clean, dps=dps + 15)
                clean_cj_prime = converter.zero_j_contribution_audit(x_prime, rho_clean_prime, dps=dps + 15)
                clean_cj_residual = abs(clean_cj_prime - clean_cj)

                if mode in ("symmetry_complete_split", "symmetry_complete_quartet"):
                    rho_plus = mpmath.mpc(mpmath.mpf('0.5') + d_val, rho_clean.imag)
                    rho_minus = mpmath.mpc(mpmath.mpf('0.5') - d_val, rho_clean.imag)
                    rho_plus_prime = A * rho_plus
                    rho_minus_prime = A * rho_minus

                    pert_cj = (
                        converter.zero_j_contribution_audit(x_mpf, rho_plus, dps=dps + 15) +
                        converter.zero_j_contribution_audit(x_mpf, rho_minus, dps=dps + 15)
                    )
                    pert_cj_prime = (
                        converter.zero_j_contribution_audit(x_prime, rho_plus_prime, dps=dps + 15) +
                        converter.zero_j_contribution_audit(x_prime, rho_minus_prime, dps=dps + 15)
                    )
                    pert_cj_residual = abs(pert_cj_prime - pert_cj)

                    split_defect = pert_cj - (mpmath.mpf(2) * clean_cj)
                    split_defect_prime = pert_cj_prime - (mpmath.mpf(2) * clean_cj_prime)
                    delta_cj_residual = abs(split_defect_prime - split_defect)
                else:
                    rho_pert = mpmath.mpc(mpmath.mpf('0.5') + d_val, rho_clean.imag)
                    rho_pert_prime = A * rho_pert
                    pert_cj = converter.zero_j_contribution_audit(x_mpf, rho_pert, dps=dps + 15)
                    pert_cj_prime = converter.zero_j_contribution_audit(x_prime, rho_pert_prime, dps=dps + 15)
                    pert_cj_residual = abs(pert_cj_prime - pert_cj)

                    delta_cj = pert_cj - clean_cj
                    delta_cj_prime = pert_cj_prime - clean_cj_prime
                    delta_cj_residual = abs(delta_cj_prime - delta_cj)

                cov_residual = max(clean_cj_residual, pert_cj_residual, delta_cj_residual)

                return "ok", {
                    "k": k_str,
                    "A": mpmath.nstr(A, n=dps),
                    "x": mpmath.nstr(x_mpf, n=dps),
                    "x_prime": mpmath.nstr(x_prime, n=dps),
                    "zero_index": str(zero_idx),
                    "gamma": mpmath.nstr(rho_clean.imag, n=dps),
                    "A_gamma": mpmath.nstr(A * rho_clean.imag, n=dps),
                    "delta": delta_str,
                    "A_delta": mpmath.nstr(A * d_val, n=dps),
                    "perturbation_mode": mode,
                    "clean_cj": mpmath.nstr(clean_cj, n=dps),
                    "clean_cj_prime": mpmath.nstr(clean_cj_prime, n=dps),
                    "clean_cj_residual": mpmath.nstr(clean_cj_residual, n=dps),
                    "pert_cj": mpmath.nstr(pert_cj, n=dps),
                    "pert_cj_prime": mpmath.nstr(pert_cj_prime, n=dps),
                    "pert_cj_residual": mpmath.nstr(pert_cj_residual, n=dps),
                    "delta_cj_residual": mpmath.nstr(delta_cj_residual, n=dps),
                    "covariance_residual": mpmath.nstr(cov_residual, n=dps),
                    "residual": mpmath.nstr(cov_residual, n=dps)
                }, None

            elif operation == "transcendental_worldline":
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

            elif operation == "synthetic_radial_leaf":
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

            elif operation == "trivial_zero_worldlines":
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

            elif operation == "cross_height_coherence":
                zero_idx = int(inputs.get("zero_index", inputs.get("n", "0")))
                u_str = inputs.get("u", "0.0")
                block_name = inputs.get("block", None)

                z_idx_1based = 1
                if block_name:
                    blk = reference_data.get_zero_block(block_name)
                    ords = blk.get("ordinates", [])
                    gamma_str = inputs.get("gamma", ords[zero_idx % len(ords)])
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

            elif operation == "cross_height_distance":
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

                blk1 = reference_data.get_zero_block(b1)
                blk2 = reference_data.get_zero_block(b2)
                ords1 = blk1.get("ordinates", [])
                ords2 = blk2.get("ordinates", [])

                g1_str = ords1[zero_idx % len(ords1)]
                g2_str = ords2[zero_idx % len(ords2)]

                z1_idx = 1 + (zero_idx % len(ords1))
                z2_idx = 100 + (zero_idx % len(ords2)) if b2 == "medium_research" else (1000 + (zero_idx % len(ords2)) if b2 == "high_research" else 10000 + (zero_idx % len(ords2)))
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

            elif operation == "grade_constraint":
                k_str = inputs.get("K", inputs.get("k", "1"))
                delta_str = inputs.get("delta", "0.0")

                tau = math_core.get_tau(dps=dps + 15)
                k_mpf = math_core.to_mpf(k_str, dps=dps + 15)
                d_mpf = math_core.to_mpf(delta_str, dps=dps + 15)

                phi = k_mpf * d_mpf * mpmath.log(tau)
                d_k = (mpmath.power(tau, k_mpf * d_mpf) - 1) * (1 - mpmath.power(tau, -k_mpf * d_mpf))
                abs_d_k = abs(d_k)
                expected_abs_d_k = 4 * mpmath.power(mpmath.sinh(phi / 2), 2)
                identity_error = abs(abs_d_k - expected_abs_d_k)

                return "ok", {
                    "K": k_str,
                    "delta": delta_str,
                    "abs_D_K": mpmath.nstr(abs_d_k, n=dps),
                    "expected_abs_D_K": mpmath.nstr(expected_abs_d_k, n=dps),
                    "identity_error": mpmath.nstr(identity_error, n=dps),
                    "residual": mpmath.nstr(identity_error, n=dps)
                }, None

            elif operation == "explicit_formula_native_baseline":
                j_idx = int(inputs.get("test_function_index", inputs.get("j", "1")))
                k_str = inputs.get("k", inputs.get("K", "0"))
                prime_cutoff = int(inputs.get("prime_cutoff", "50000"))

                # Reference zeros (200)
                ref_zeros = reference_data.load_reference_zeros()

                # Authoritative evaluation
                eval_res = math_core.explicit_formula_eval(
                    j=j_idx,
                    K=k_str,
                    zeros_ordinates=ref_zeros,
                    prime_cutoff=prime_cutoff,
                    dps=dps + 15
                )

                sigma, t0 = math_core.get_test_function_params(j_idx, dps=dps + 15)
                res_val = eval_res["residual"]
                rel_err = eval_res["relative_error"]

                # Truncation and convergence sensitivity diagnostics
                # 1. Spectral cutoff comparison (N=100 vs N=200, N=150 vs N=200)
                eval_n100 = math_core.explicit_formula_eval(j=j_idx, K=k_str, zeros_ordinates=ref_zeros[:100], prime_cutoff=prime_cutoff, dps=dps + 15)
                eval_n150 = math_core.explicit_formula_eval(j=j_idx, K=k_str, zeros_ordinates=ref_zeros[:150], prime_cutoff=prime_cutoff, dps=dps + 15)
                spectral_change_100_200 = abs(eval_res["residual"] - eval_n100["residual"])
                spectral_change_150_200 = abs(eval_res["residual"] - eval_n150["residual"])

                # 2. Prime cutoff comparison (10000 vs 50000)
                eval_p10k = math_core.explicit_formula_eval(j=j_idx, K=k_str, zeros_ordinates=ref_zeros, prime_cutoff=10000, dps=dps + 15)
                prime_cutoff_change = abs(eval_res["residual"] - eval_p10k["residual"])

                # 3. Precision comparison (70 vs 110 dps)
                eval_110 = math_core.explicit_formula_eval(j=j_idx, K=k_str, zeros_ordinates=ref_zeros, prime_cutoff=prime_cutoff, dps=110)
                prec_change = abs(eval_res["residual"] - eval_110["residual"])

                t_max_std = eval_res["t_max"]
                highest_zero_ord = ref_zeros[-1] if ref_zeros else "0"

                return "ok", {
                    "test_function_index": str(j_idx),
                    "j": str(j_idx),
                    "k": k_str,
                    "sigma": mpmath.nstr(sigma, n=dps),
                    "t0": mpmath.nstr(t0, n=dps),
                    "spectral_sum": mpmath.nstr(eval_res["spectral_sum"], n=dps),
                    "pole_term": mpmath.nstr(eval_res["pole_term"], n=dps),
                    "prime_term": mpmath.nstr(eval_res["prime_term"], n=dps),
                    "gamma_term": mpmath.nstr(eval_res["gamma_term"], n=dps),
                    "total_rhs": mpmath.nstr(eval_res["total_rhs"], n=dps),
                    "residual": mpmath.nstr(abs(res_val), n=dps),
                    "signed_residual": mpmath.nstr(res_val, n=dps),
                    "relative_error": mpmath.nstr(rel_err, n=dps),
                    "zero_count": str(len(ref_zeros)),
                    "highest_included_zero_index": str(len(ref_zeros)),
                    "highest_included_zero_ordinate": highest_zero_ord,

                    "certified_zero_count": "100",
                    "reference_approximation_zero_count": str(len(ref_zeros) - 100),
                    "prime_power_cutoff": str(prime_cutoff),
                    "integration_endpoint_t_max": mpmath.nstr(t_max_std, n=dps),
                    "spectral_cutoff_change_100_to_200": mpmath.nstr(spectral_change_100_200, n=dps),
                    "spectral_cutoff_change_150_to_200": mpmath.nstr(spectral_change_150_200, n=dps),
                    "prime_cutoff_change_10k_to_50k": mpmath.nstr(prime_cutoff_change, n=dps),
                    "precision_change_70_to_110": mpmath.nstr(prec_change, n=dps),
                    "epistemic_class": "observational_pattern",
                    "error_budget": "spectral_truncation_200_zeros_plus_prime_sieve_50000",
                }, None

            elif operation == "explicit_formula_grade_covariance":
                j_idx = int(inputs.get("test_function_index", inputs.get("j", "1")))
                k_str = inputs.get("k", inputs.get("K", "0"))

                tau = math_core.get_tau(dps=dps + 20)
                k_mpf = math_core.to_mpf(k_str, dps=dps + 20)
                a_K = mpmath.power(tau, k_mpf)

                # 1. Fourier scaling identity: h_hat_{K,j}(x) == a_K^{-1} * H_hat_j(a_K^{-1} * x)
                fourier_errs = []
                for x_test_str in ["0.5", "1.0", "2.5"]:
                    x_mpf = math_core.to_mpf(x_test_str, dps=dps + 20)
                    scaled_hat = math_core.h_kj_scaled_hat(x_mpf, j_idx, k_mpf, dps=dps + 20)
                    expected_hat = (mpmath.mpf(1) / a_K) * math_core.H_test_function_hat(x_mpf / a_K, j_idx, dps=dps + 20)
                    fourier_errs.append(abs(scaled_hat - expected_hat))
                max_fourier_err = max(fourier_errs)

                # 2. Coordinate pullback identity: h_{K,j}(t) == H_j(a_K * t)
                pullback_errs = []
                for t_test_str in ["0.0", "14.1347", "50.0"]:
                    t_mpf = math_core.to_mpf(t_test_str, dps=dps + 20)
                    h_val = math_core.h_kj_scaled(t_mpf, j_idx, k_mpf, dps=dps + 20)
                    h_direct = math_core.H_test_function(a_K * t_mpf, j_idx, dps=dps + 20)
                    pullback_errs.append(abs(h_val - h_direct))
                max_pullback_err = max(pullback_errs)

                # 3. Direct independent numerical quadrature vs scaled Fourier transform
                quad_errs = []
                for x_test_str in ["0.5", "1.0", "2.0"]:
                    x_mpf = math_core.to_mpf(x_test_str, dps=dps + 20)
                    q_res = math_core.compute_grade_quadrature_fourier(j_idx, k_mpf, x_mpf, dps=dps)
                    quad_errs.append(q_res["absolute_error"])
                max_quad_err = max(quad_errs)

                # 4. Expanded native basis equivalence test with independent paths
                ref_zeros = reference_data.load_reference_zeros()[:20]
                equiv_check = math_core.check_expanded_native_basis_equivalence(
                    j_list=[j_idx],
                    k_list=[k_mpf],
                    zeros_subset=ref_zeros,
                    dps=dps + 20
                )

                # 5. Compound exact-control consistency (rank equivalence across paths)
                rank_consistent = bool(equiv_check["rank_grade"] == equiv_check["rank_native"] == equiv_check["rank_stacked"])
                rank_penalty = mpmath.mpf(0) if rank_consistent else mpmath.mpf(1)

                total_cov_err = max(max_fourier_err, max_pullback_err, max_quad_err, equiv_check["max_discrepancy"], rank_penalty)

                return "ok", {
                    "test_function_index": str(j_idx),
                    "j": str(j_idx),
                    "k": k_str,
                    "a_K": mpmath.nstr(a_K, n=dps),
                    "fourier_scaling_error": mpmath.nstr(max_fourier_err, n=dps),
                    "pullback_identity_error": mpmath.nstr(max_pullback_err, n=dps),
                    "quadrature_fourier_error": mpmath.nstr(max_quad_err, n=dps),
                    "basis_equivalence_discrepancy": mpmath.nstr(equiv_check["max_discrepancy"], n=dps),
                    "rank_grade": str(equiv_check["rank_grade"]),
                    "rank_native": str(equiv_check["rank_native"]),
                    "rank_stacked": str(equiv_check["rank_stacked"]),
                    "categorical_equivalence_verified": "true" if (equiv_check["is_equivalent"] and rank_consistent) else "false",
                    "theoretical_classification": "coordinate_redundant",
                    "finite_basis_classification": "finite_basis_enrichment_only",
                    "discrimination_classification": "coordinate_redundant",
                    "residual": mpmath.nstr(total_cov_err, n=dps),
                }, None

            elif operation == "explicit_formula_perturbation_rank":
                mode = inputs.get("mode", inputs.get("perturbation_type", "critical_height"))
                case_str = inputs.get("case", inputs.get("zero_index", inputs.get("n", "1"))).strip()
                mag_str = inputs.get("magnitude", inputs.get("epsilon", inputs.get("delta", "0.001"))).strip()


                j_list = [1, 2, 3, 4, 5, 6]
                k_list = [-2, -1, 0, 1, 2]

                if mode == "critical_height":
                    # 1-based index n in {1, 10, 50}
                    n_idx = int(case_str)
                    c_hash, ok, zc, errs = _lookup_zero_certificate(n_idx, zero_family="nontrivial", check_provenance=True)
                    if not ok or zc is None or c_hash is None:
                        return "error", {}, f"Failed to load/verify certificate for zero {n_idx}: {errs}"

                    ord_str = zc["enclosure"]["imag_mid"]

                    # Validate divisor mutation
                    eps_mpf = math_core.to_mpf(mag_str, dps=dps + 20)
                    g_n = math_core.to_mpf(ord_str, dps=dps + 20)
                    is_valid, val_evidence, val_errs = math_core.validate_divisor_perturbation(
                        mutation_type="critical_height",
                        zeros=[
                            mpmath.mpc(mpmath.mpf('0.5'), g_n + eps_mpf),
                            mpmath.mpc(mpmath.mpf('0.5'), -(g_n + eps_mpf))
                        ],
                        claimed_multiplicity_preserved=True,
                        dps=dps + 20
                    )
                    if not is_valid:
                        return "error", {}, f"Divisor perturbation validation failed: {val_errs}"

                    # Compute exact and linear defects across all 30 channels
                    exact_defects = []
                    linear_defects = []
                    remainders = []
                    for k_val in k_list:
                        for j_val in j_list:
                            res_def = math_core.finite_divisor_defect_critical_height_exact_and_linear(
                                j=j_val,
                                K=k_val,
                                gamma_n=g_n,
                                epsilon=eps_mpf,
                                dps=dps + 20
                            )
                            exact_defects.append(res_def["exact_defect"])
                            linear_defects.append(res_def["linear_defect"])
                            remainders.append(res_def["remainder"])

                    exact_norm = mpmath.sqrt(sum(d * d for d in exact_defects))
                    linear_norm = mpmath.sqrt(sum(d * d for d in linear_defects))
                    rem_norm = mpmath.sqrt(sum(d * d for d in remainders))
                    rel_lin_err = (rem_norm / exact_norm) if exact_norm > mpmath.mpf('1e-50') else mpmath.mpf(0)

                    # Load first 100 certified zeros for Jacobian
                    first_100_ords = []
                    for idx_100 in range(1, 101):
                        ch_100, ok_100, zc_100, _ = _lookup_zero_certificate(idx_100, zero_family="nontrivial", check_provenance=False)
                        if zc_100 and "enclosure" in zc_100:
                            first_100_ords.append(zc_100["enclosure"]["imag_mid"])
                        else:
                            first_100_ords.append(reference_data.load_first_100_reference_zeros()[idx_100 - 1])

                    # Compute Jacobian
                    J = math_core.explicit_formula_jacobian(
                        j_list=j_list,
                        k_list=k_list,
                        zeros_subset=first_100_ords,
                        dps=dps + 20
                    )

                    # Solve linearized compensation (0-based column index is n_idx - 1)
                    target_col = n_idx - 1
                    comp_res = math_core.solve_linearized_compensation(
                        J=J,
                        target_col_idx=target_col,
                        epsilon=eps_mpf,
                        rank_tol_rel='1e-25',
                        dps=dps + 20
                    )

                    detected = bool(exact_norm > mpmath.mpf('1e-25'))

                    return "ok", {
                        "mode": "critical_height",
                        "perturbation_type": "critical_height",
                        "case": str(n_idx),
                        "zero_index": str(n_idx),
                        "target_gamma": ord_str,
                        "zero1_cert_hash": c_hash,
                        "epsilon": mag_str,
                        "magnitude": mag_str,

                        "validator_status": "valid",
                        "symmetries_preserved": "conjugation_and_functional_reflection",
                        "multiplicity_preserved": "true",
                        "defect_vector_norm": mpmath.nstr(exact_norm, n=dps),
                        "exact_defect_vector_norm": mpmath.nstr(exact_norm, n=dps),
                        "linear_defect_vector_norm": mpmath.nstr(linear_norm, n=dps),
                        "nonlinear_remainder_norm": mpmath.nstr(rem_norm, n=dps),
                        "relative_linearization_error": mpmath.nstr(rel_lin_err, n=dps),
                        "isolated_defect_detected": "true" if detected else "false",
                        "detection_threshold": "1e-25",
                        "detection_justification": "algebraic_cancellation_of_unperturbed_arithmetic_and_archimedean_terms",
                        "separating_test_limitation": f"detected_by_modulated_gaussian_family_separating_zero_{n_idx}",
                        "numerical_rank": str(comp_res["numerical_rank"]),
                        "nullity": str(comp_res["nullity"]),
                        "condition_number": mpmath.nstr(comp_res["condition_number"], n=8),
                        "rank_stability": comp_res["rank_stability"],
                        "threshold_sweep": json.dumps({k: v for k, v in comp_res["threshold_sweep"].items()}),
                        "compensation_solution_norm": mpmath.nstr(comp_res["compensation_norm"], n=dps),
                        "compensation_residual_norm": mpmath.nstr(comp_res["residual_norm"], n=dps),
                        "relative_compensation_residual": mpmath.nstr(comp_res["relative_residual"], n=dps),
                        "compensation_found": "true" if comp_res["compensation_found"] else "false",
                        "participating_indices_count": str(len(comp_res["participating_indices"])),
                        "theoretical_classification": "coordinate_redundant",
                        "finite_basis_classification": "finite_basis_enrichment_only",
                        "residual": mpmath.nstr(exact_norm, n=dps),
                    }, None

                elif mode == "radial_quartet":
                    # Predetermined pairs: 1 -> (1, 2), 10 -> (10, 11), 50 -> (50, 51)
                    case_val = int(case_str)
                    if case_val == 1:
                        idx_a, idx_b = 1, 2
                    elif case_val == 10:
                        idx_a, idx_b = 10, 11
                    elif case_val == 50:
                        idx_a, idx_b = 50, 51
                    else:
                        idx_a, idx_b = case_val, case_val + 1

                    c_hash_a, ok_a, zc_a, errs_a = _lookup_zero_certificate(idx_a, zero_family="nontrivial", check_provenance=True)
                    if not ok_a or zc_a is None or c_hash_a is None:
                        return "error", {}, f"Failed to load certificate for zero {idx_a}: {errs_a}"

                    c_hash_b, ok_b, zc_b, errs_b = _lookup_zero_certificate(idx_b, zero_family="nontrivial", check_provenance=True)
                    if not ok_b or zc_b is None or c_hash_b is None:
                        return "error", {}, f"Failed to load certificate for zero {idx_b}: {errs_b}"

                    ga_str = zc_a["enclosure"]["imag_mid"]
                    gb_str = zc_b["enclosure"]["imag_mid"]
                    d_val = math_core.to_mpf(mag_str, dps=dps + 20)

                    ga_mpf = math_core.to_mpf(ga_str, dps=dps + 20)
                    gb_mpf = math_core.to_mpf(gb_str, dps=dps + 20)
                    g0_mpf = (ga_mpf + gb_mpf) / mpmath.mpf(2)

                    # Validate quartet mutation
                    is_valid, val_evidence, val_errs = math_core.validate_divisor_perturbation(
                        mutation_type="radial_quartet",
                        zeros=[
                            mpmath.mpc(mpmath.mpf('0.5') + d_val, g0_mpf),
                            mpmath.mpc(mpmath.mpf('0.5') + d_val, -g0_mpf),
                            mpmath.mpc(mpmath.mpf('0.5') - d_val, g0_mpf),
                            mpmath.mpc(mpmath.mpf('0.5') - d_val, -g0_mpf),
                        ],
                        claimed_multiplicity_preserved=True,
                        dps=dps + 20
                    )
                    if not is_valid:
                        return "error", {}, f"Radial quartet validation failed: {val_errs}"

                    merge_defects = []
                    radial_defects = []
                    total_defects = []

                    for k_val in k_list:
                        for j_val in j_list:
                            res_q = math_core.finite_divisor_defect_radial_quartet_decomposed(
                                j=j_val,
                                K=k_val,
                                gamma_a=ga_mpf,
                                gamma_b=gb_mpf,
                                delta=d_val,
                                dps=dps + 20
                            )
                            merge_defects.append(res_q["merge_defect"])
                            radial_defects.append(res_q["radial_defect"])
                            total_defects.append(res_q["total_defect"])

                    merge_norm = mpmath.sqrt(sum(d * d for d in merge_defects))
                    radial_norm = mpmath.sqrt(sum(d * d for d in radial_defects))
                    total_norm = mpmath.sqrt(sum(d * d for d in total_defects))

                    detected = bool(radial_norm > mpmath.mpf('1e-25')) if abs(d_val) > mpmath.mpf('1e-20') else True

                    return "ok", {
                        "mode": "radial_quartet",
                        "perturbation_type": "radial_quartet",
                        "case": str(case_val),
                        "zero_index_a": str(idx_a),
                        "zero_index_b": str(idx_b),
                        "gamma_a": ga_str,
                        "gamma_b": gb_str,
                        "gamma_0": mpmath.nstr(g0_mpf, n=dps),
                        "zero1_cert_hash": c_hash_a,
                        "zero2_cert_hash": c_hash_b,
                        "delta": mag_str,

                        "magnitude": mag_str,
                        "validator_status": "valid",
                        "symmetries_preserved": "conjugation_and_functional_reflection",
                        "multiplicity_preserved": "true",
                        "pure_radial_defect_norm": mpmath.nstr(radial_norm, n=dps),
                        "height_merging_norm": mpmath.nstr(merge_norm, n=dps),
                        "total_quartet_norm": mpmath.nstr(total_norm, n=dps),
                        "defect_vector_norm": mpmath.nstr(radial_norm, n=dps),
                        "isolated_defect_detected": "true" if detected else "false",
                        "detection_threshold": "1e-25",
                        "detection_justification": "algebraic_cancellation_of_unperturbed_arithmetic_and_archimedean_terms",
                        "separating_test_limitation": f"detected_by_modulated_gaussian_family_separating_pair_({idx_a},{idx_b})",
                        "theoretical_classification": "coordinate_redundant",
                        "finite_basis_classification": "finite_basis_enrichment_only",
                        "residual": mpmath.nstr(radial_norm, n=dps),
                    }, None


                else:
                    return "error", {}, f"Unsupported perturbation mode: '{mode}'"

            elif operation == "explicit_formula_radial_second_variation":
                mode = inputs.get("mode", "pure_radial_variation")
                z_idx_str = inputs.get("zero_index", inputs.get("case", "1")).strip()
                delta_str = inputs.get("delta", inputs.get("magnitude", "0.001")).strip()

                z_idx = int(z_idx_str)
                c_hash, ok, zc, errs = _lookup_zero_certificate(z_idx, zero_family="nontrivial", check_provenance=True)
                if not ok or zc is None or c_hash is None:
                    return "error", {}, f"Failed to load certificate for zero {z_idx}: {errs}"

                gamma_str = zc["enclosure"]["imag_mid"]
                gamma_mpf = math_core.to_mpf(gamma_str, dps=dps + 20)
                delta_mpf = math_core.to_mpf(delta_str, dps=dps + 20)
                u_mpf = delta_mpf * delta_mpf

                # Symmetries & validation
                is_valid, val_evidence, val_errs = math_core.validate_divisor_perturbation(
                    mutation_type="radial_quartet",
                    zeros=[
                        mpmath.mpc(mpmath.mpf('0.5') + delta_mpf, gamma_mpf),
                        mpmath.mpc(mpmath.mpf('0.5') + delta_mpf, -gamma_mpf),
                        mpmath.mpc(mpmath.mpf('0.5') - delta_mpf, gamma_mpf),
                        mpmath.mpc(mpmath.mpf('0.5') - delta_mpf, -gamma_mpf),
                    ],
                    claimed_multiplicity_preserved=True,
                    dps=dps + 20
                )
                if not is_valid:
                    return "error", {}, f"Radial perturbation validation failed: {val_errs}"

                j_list = [1, 2, 3, 4, 5, 6]
                k_list = [-2, -1, 0, 1, 2]

                # 1. Exact vs second-order vs fourth-order across all 30 channels
                exact_radial_defects = []
                linear_second_order = []
                fourth_order_terms = []
                remainders = []
                half_delta_exact_defects = []

                for k_val in k_list:
                    for j_val in j_list:
                        pt_res = math_core.pure_radial_defect_exact_and_second_order(
                            j=j_val,
                            K=k_val,
                            gamma=gamma_mpf,
                            delta=delta_mpf,
                            dps=dps + 20
                        )
                        exact_radial_defects.append(pt_res["exact_radial_defect"])
                        linear_second_order.append(pt_res["linear_second_order"])
                        fourth_order_terms.append(pt_res["fourth_order_term"])
                        remainders.append(pt_res["remainder"])

                        # Half-delta evaluation for quadratic ratio test
                        pt_half = math_core.pure_radial_defect_exact_and_second_order(
                            j=j_val,
                            K=k_val,
                            gamma=gamma_mpf,
                            delta=delta_mpf / mpmath.mpf(2),
                            dps=dps + 20
                        )
                        half_delta_exact_defects.append(pt_half["exact_radial_defect"])

                exact_norm = mpmath.sqrt(sum(d * d for d in exact_radial_defects))
                linear_norm = mpmath.sqrt(sum(d * d for d in linear_second_order))
                fourth_norm = mpmath.sqrt(sum(d * d for d in fourth_order_terms))
                rem_norm = mpmath.sqrt(sum(d * d for d in remainders))
                half_exact_norm = mpmath.sqrt(sum(d * d for d in half_delta_exact_defects))

                quadratic_ratio = (exact_norm / half_exact_norm) if half_exact_norm > mpmath.mpf('1e-50') else mpmath.mpf(4)
                rel_second_order_error = (rem_norm / exact_norm) if exact_norm > mpmath.mpf('1e-50') else mpmath.mpf(0)
                quadratic_energy = linear_norm * linear_norm

                # 2. First 100 certified zeros for radial Jacobian
                first_100_ords = []
                for idx_100 in range(1, 101):
                    ch_100, ok_100, zc_100, _ = _lookup_zero_certificate(idx_100, zero_family="nontrivial", check_provenance=False)
                    if zc_100 and "enclosure" in zc_100:
                        first_100_ords.append(zc_100["enclosure"]["imag_mid"])
                    else:
                        first_100_ords.append(reference_data.load_first_100_reference_zeros()[idx_100 - 1])

                K_mat = math_core.radial_second_order_jacobian(
                    j_list=j_list,
                    k_list=k_list,
                    zeros_subset=first_100_ords,
                    dps=dps + 20
                )

                target_col = z_idx - 1
                nnls_res = math_core.solve_radial_second_order_nnls(
                    K_mat=K_mat,
                    target_col_idx=target_col,
                    u_val=u_mpf,
                    rank_tol_rel='1e-25',
                    dps=dps + 20
                )

                detected = bool(exact_norm > mpmath.mpf('1e-25'))

                return "ok", {
                    "mode": mode,
                    "zero_index": str(z_idx),
                    "target_gamma": gamma_str,
                    "zero_cert_hash": c_hash,
                    "delta": delta_str,
                    "u": mpmath.nstr(u_mpf, n=dps),
                    "exact_radial_defect_norm": mpmath.nstr(exact_norm, n=dps),
                    "linear_second_order_norm": mpmath.nstr(linear_norm, n=dps),
                    "fourth_order_term_norm": mpmath.nstr(fourth_norm, n=dps),
                    "second_order_remainder_norm": mpmath.nstr(rem_norm, n=dps),
                    "relative_second_order_error": mpmath.nstr(rel_second_order_error, n=dps),
                    "quadratic_ratio": mpmath.nstr(quadratic_ratio, n=8),
                    "quadratic_energy": mpmath.nstr(quadratic_energy, n=dps),
                    "nnls_solution_norm": mpmath.nstr(nnls_res["nnls_solution_norm"], n=dps),
                    "nnls_residual_norm": mpmath.nstr(nnls_res["nnls_residual_norm"], n=dps),
                    "nnls_relative_residual": mpmath.nstr(nnls_res["nnls_relative_residual"], n=dps),
                    "nnls_compensation_found": "true" if nnls_res["nnls_compensation_found"] else "false",
                    "nnls_residual_nonzero_at_threshold": "true" if nnls_res["nnls_residual_nonzero_at_threshold"] else "false",
                    "finite_response_energy_positive": "true" if nnls_res["finite_response_energy_positive"] else "false",
                    "unconstrained_residual_norm": mpmath.nstr(nnls_res["unconstrained_residual_norm"], n=dps),
                    "numerical_rank": str(nnls_res["numerical_rank"]),
                    "nullity": str(nnls_res["nullity"]),
                    "condition_number": mpmath.nstr(nnls_res["condition_number"], n=8),
                    "rank_stability": nnls_res["rank_stability"],
                    "threshold_sweep": json.dumps({k: v for k, v in nnls_res["threshold_sweep"].items()}),
                    "anti_circularity_status": "screened_no_rh_or_weil_assumed",
                    "theoretical_classification": "coordinate_redundant",
                    "finite_basis_classification": "finite_basis_enrichment_only",
                    "residual": mpmath.nstr(exact_norm, n=dps),
                }, None

            else:
                return "error", {}, f"Unknown operation '{operation}'"

        except Exception as e:
            return "error", {}, str(e)


def evaluate_criterion(
    observed_str: str,
    operator: str,
    threshold_str: str,
    dps: int = 80
) -> bool:
    """Evaluate declared mathematical criterion with arbitrary-precision comparison."""
    try:
        with mpmath.workdps(dps + 15):
            obs = mpmath.mpf(observed_str.strip())
            thresh = mpmath.mpf(threshold_str.strip())

            if operator == "<=":
                return bool(obs <= thresh)
            elif operator == "<":
                return bool(obs < thresh)
            elif operator == ">=":
                return bool(obs >= thresh)
            elif operator == ">":
                return bool(obs > thresh)
            elif operator == "==":
                return bool(abs(obs - thresh) < mpmath.mpf('1e-50'))
            elif operator == "!=":
                return bool(abs(obs - thresh) >= mpmath.mpf('1e-50'))
            return False
    except Exception:
        return False


def compute_metric_stats(
    metric_name: str,
    results: List[Dict[str, Any]],
    dps: int,
    kind: str = "criterion_component",
    label: Optional[str] = None
) -> Dict[str, Any]:
    """
    Compute statistics, argmax, and up to 5 worst points for a single metric across results.
    All calculations, parsing, comparisons, and formatting are strictly executed within
    mpmath.workdps(dps + 15).
    Authoritative values are preserved as decimal strings.
    """
    with mpmath.workdps(dps + 15):
        valid_points = []
        for idx, r in enumerate(results):
            if r.get("status") == "ok" and metric_name in r.get("outputs", {}):
                try:
                    raw_val = r["outputs"][metric_name]
                    raw_str = str(raw_val).strip()
                    if raw_str.lower() in ("n/a", "none", "null", ""):
                        continue
                    mpf_val = mpmath.mpf(raw_str)
                    val_abs = abs(mpf_val)
                    point_id = r.get("point_id", idx)
                    val_str = mpmath.nstr(mpf_val, n=dps)
                    abs_val_str = mpmath.nstr(val_abs, n=dps)
                    valid_points.append({
                        "point_id": point_id,
                        "val": mpf_val,
                        "val_abs": val_abs,
                        "val_str": val_str,
                        "abs_val_str": abs_val_str,
                        "inputs": dict(r.get("inputs", {}))
                    })
                except Exception:
                    pass

        if not valid_points:
            return {
                "metric": metric_name,
                "label": label or metric_name,
                "kind": kind,
                "count": 0,
                "min": "N/A",
                "max": "N/A",
                "max_abs": "N/A",
                "argmax_abs": None,
                "worst_points": []
            }

        count = len(valid_points)
        min_pt = min(valid_points, key=lambda p: p["val"])
        max_pt = max(valid_points, key=lambda p: p["val"])
        argmax_abs_pt = max(valid_points, key=lambda p: p["val_abs"])

        sorted_by_worst = sorted(valid_points, key=lambda p: p["val_abs"], reverse=True)
        worst_5 = sorted_by_worst[:5]

        worst_points_records = [
            {
                "point_id": p["point_id"],
                "value": p["val_str"],
                "abs_value": p["abs_val_str"],
                "inputs": p["inputs"]
            }
            for p in worst_5
        ]

        return {
            "metric": metric_name,
            "label": label or metric_name,
            "kind": kind,
            "count": count,
            "min": min_pt["val_str"],
            "max": max_pt["val_str"],
            "max_abs": argmax_abs_pt["abs_val_str"],
            "argmax_abs": {
                "point_id": argmax_abs_pt["point_id"],
                "value": argmax_abs_pt["val_str"],
                "abs_value": argmax_abs_pt["abs_val_str"],
                "inputs": argmax_abs_pt["inputs"]
            },
            "worst_points": worst_points_records
        }


def compute_summary(
    spec: Dict[str, Any],
    run_id: str,
    results: List[Dict[str, Any]],
    status: str
) -> Dict[str, Any]:
    """Generate canonical AI-facing summary.json artifact with multi-metric reporting."""
    dps = spec["precision"]["dps"]
    crit_spec = spec["criterion"]
    target_metric = crit_spec["metric"]
    aggregation = crit_spec.get("aggregation", "max_abs")
    operator = crit_spec.get("operator", "<=")
    threshold_str = str(crit_spec.get("threshold", "0.0"))

    points_req = len(results)
    points_completed = sum(1 for r in results if r.get("status") == "ok")
    points_failed = sum(1 for r in results if r.get("status") == "error")

    with mpmath.workdps(dps + 15):
        metric_declarations = []
        seen_metric_names = set()

        metric_declarations.append({
            "metric": target_metric,
            "kind": "primary_criterion" if aggregation != "none" else "observational_metric",
            "label": f"Primary metric: {target_metric}"
        })
        seen_metric_names.add(target_metric)

        declared_reports = spec.get("report_metrics", [])
        if isinstance(declared_reports, list):
            for item in declared_reports:
                if isinstance(item, str):
                    m_name = item
                    m_kind = "criterion_component"
                    m_label = item
                elif isinstance(item, dict):
                    m_name = item.get("metric", "")
                    m_kind = item.get("kind", "criterion_component")
                    m_label = item.get("label", m_name)
                else:
                    continue

                if m_name and m_name not in seen_metric_names:
                    metric_declarations.append({
                        "metric": m_name,
                        "kind": m_kind,
                        "label": m_label
                    })
                    seen_metric_names.add(m_name)
                elif m_name and m_name == target_metric:
                    metric_declarations[0]["kind"] = m_kind
                    metric_declarations[0]["label"] = m_label

        report_metrics_dict = {}
        metrics_summary_dict = {}

        for decl in metric_declarations:
            m_name = decl["metric"]
            stats = compute_metric_stats(
                metric_name=m_name,
                results=results,
                dps=dps,
                kind=decl["kind"],
                label=decl.get("label")
            )
            report_metrics_dict[m_name] = stats
            metrics_summary_dict[m_name] = stats["max_abs"]

        target_stats = report_metrics_dict.get(target_metric)
        anomalies = []
        warnings = []

        if aggregation == "none":
            observed_metric_str = None
            criterion_met = None
            min_observed = target_stats["min"] if target_stats else "N/A"
            max_observed = target_stats["max"] if target_stats else "N/A"
        elif target_stats and target_stats["count"] > 0:
            if aggregation == "max_abs":
                observed_metric_str = target_stats["max_abs"]
                criterion_met = evaluate_criterion(observed_metric_str, operator, threshold_str, dps=dps)
            elif aggregation == "max":
                observed_metric_str = target_stats["max"]
                criterion_met = evaluate_criterion(observed_metric_str, operator, threshold_str, dps=dps)
            elif aggregation == "min":
                observed_metric_str = target_stats["min"]
                criterion_met = evaluate_criterion(observed_metric_str, operator, threshold_str, dps=dps)
            elif aggregation == "all":
                all_met = True
                for r in results:
                    if r.get("status") == "ok" and target_metric in r.get("outputs", {}):
                        raw_v = str(r["outputs"][target_metric]).strip()
                        if not evaluate_criterion(raw_v, operator, threshold_str, dps=dps):
                            all_met = False
                observed_metric_str = target_stats["max_abs"]
                criterion_met = all_met
            else:
                observed_metric_str = target_stats["max_abs"]
                criterion_met = evaluate_criterion(observed_metric_str, operator, threshold_str, dps=dps)

            min_observed = target_stats["min"]
            max_observed = target_stats["max"]
        else:
            observed_metric_str = "N/A"
            criterion_met = False
            status = "failed"
            min_observed = "N/A"
            max_observed = "N/A"
            anomalies.append(f"Criterion metric '{target_metric}' was never emitted by any point.")

        for decl in metric_declarations:
            m_name = decl["metric"]
            if report_metrics_dict.get(m_name, {}).get("count", 0) == 0:
                warnings.append(f"Declared report metric '{m_name}' was not emitted by any point.")

        criterion_dict = {
            "metric": target_metric,
            "aggregation": aggregation,
            "operator": operator if aggregation != "none" else "N/A",
            "threshold": threshold_str if aggregation != "none" else "N/A",
            "observed": observed_metric_str,
            "criterion_met": criterion_met if status == "complete" else None
        }

        summary = {
            "schema_version": "2",
            "run_id": run_id,
            "experiment_id": spec["id"],
            "status": status,
            "hypothesis": spec.get("hypothesis", {}).get("statement", "") if isinstance(spec.get("hypothesis"), dict) else str(spec.get("hypothesis", "")),
            "points_requested": points_req,
            "points_completed": points_completed,
            "points_failed": points_failed,
            "metrics": metrics_summary_dict,
            "report_metrics": report_metrics_dict,
            "criterion": criterion_dict,
            "extrema": {
                "min": min_observed,
                "max": max_observed
            },
            "anomalies": anomalies,
            "warnings": warnings
        }

        exp_id = spec.get("id", run_id)
        try:
            handler = get_handler(exp_id)
            with mpmath.workdps(dps + 15):
                handler_summary = handler.compute_summary(results, spec, summary, status=status)
            if isinstance(handler_summary, dict):
                summary.update(handler_summary)
        except KeyError:
            pass
        except Exception as e:
            summary.setdefault("warnings", []).append(f"Handler summary computation failed: {e}")

        if points_failed > 0:
            summary["warnings"].append(f"{points_failed} points encountered execution errors")

        return summary


def generate_run_readme(
    spec: Dict[str, Any],
    manifest: Dict[str, Any],
    summary: Dict[str, Any]
) -> str:
    """Generate concise human-readable run README.md digest with multi-metric reporting."""
    crit = summary["criterion"]
    crit_agg = crit.get("aggregation", "max_abs")
    crit_met = crit.get("criterion_met")

    if crit_agg == "none":
        crit_status = "OBSERVATIONAL / NO CRITERION DECLARED"
    elif crit_met is True:
        crit_status = "CRITERION MET"
    elif crit_met is False:
        crit_status = "CRITERION NOT MET"
    else:
        crit_status = "INCOMPLETE / INVALID"

    report_metrics = summary.get("report_metrics", {})
    table_rows = []
    for m_name, m_data in report_metrics.items():
        kind = m_data.get("kind", "criterion_component")
        count = m_data.get("count", 0)
        min_val = m_data.get("min", "N/A")
        max_val = m_data.get("max", "N/A")
        max_abs = m_data.get("max_abs", "N/A")
        table_rows.append(f"| `{m_name}` | `{kind}` | {count} | `{min_val}` | `{max_val}` | `{max_abs}` |")

    metrics_table = "\n".join(table_rows) if table_rows else "| None | - | 0 | - | - | - |"

    metric_details = []
    for m_name, m_data in report_metrics.items():
        kind = m_data.get("kind", "criterion_component")
        label = m_data.get("label", m_name)
        max_abs = m_data.get("max_abs", "N/A")
        argmax = m_data.get("argmax_abs")
        worst = m_data.get("worst_points", [])

        detail_lines = [
            f"### `{m_name}`",
            f"- **Classification:** `{kind}`",
            f"- **Description:** {label}",
            f"- **Max Absolute Value:** `{max_abs}`"
        ]
        if kind == "fixed_m_truncation_diagnostic":
            detail_lines.append("- **Note:** *Diagnostic metric only; not evaluated as part of exact covariance pass/fail criterion.*")
        elif kind == "observational_metric":
            detail_lines.append("- **Note:** *Observational response metric; no pass/fail criterion declared.*")

        if argmax and argmax.get("inputs"):
            inputs_str = ", ".join(f"{k}={v}" for k, v in argmax["inputs"].items())
            val_display = argmax.get("value")
            abs_display = argmax.get("abs_value")
            if val_display and abs_display and val_display != abs_display:
                detail_lines.append(f"- **Argmax Parameter Point (id={argmax.get('point_id')}):** `val={val_display} (|val|={abs_display})` | `{inputs_str}`")
            else:
                detail_lines.append(f"- **Argmax Parameter Point (id={argmax.get('point_id')}):** `val={val_display}` | `{inputs_str}`")

        if worst:
            detail_lines.append("- **Top Worst Parameter Points:**")
            for wp in worst[:5]:
                in_str = ", ".join(f"{k}={v}" for k, v in wp.get("inputs", {}).items())
                w_val = wp.get("value")
                w_abs = wp.get("abs_value")
                if w_val and w_abs and w_val != w_abs:
                    detail_lines.append(f"  - id={wp.get('point_id')} | `val={w_val} (|val|={w_abs})` | `{in_str}`")
                else:
                    detail_lines.append(f"  - id={wp.get('point_id')} | `val={w_val}` | `{in_str}`")

        metric_details.append("\n".join(detail_lines))

    details_block = "\n\n".join(metric_details) if metric_details else "No metric details available."

    crit_summary_line = (
        f"- **Primary Criterion ({crit_agg}):** `{crit['metric']} {crit['operator']} {crit['threshold']}`\n"
        f"- **Observed Metric:** `{crit['observed']}`\n"
        f"- **Criterion Met:** `{crit['criterion_met']}`"
        if crit_agg != "none" else
        "- **Primary Criterion:** `N/A (Observational)`\n"
        "- **Observed Metric:** `N/A`\n"
        "- **Criterion Met:** `null (Observational)`"
    )

    tau_val = manifest.get('tau', '')
    if isinstance(tau_val, dict):
        tau_display = f"{tau_val.get('numeric_decimal', '')[:24]}... ({tau_val.get('symbolic', '2*pi')})"
    elif isinstance(tau_val, str):
        tau_display = f"{tau_val[:24]}..."
    else:
        tau_display = str(tau_val)

    readme_lines = [
        f"# Experiment Run Digest — {spec.get('title', spec['id'])}\n",
        f"**Run ID:** `{manifest['run_id']}`",
        f"**Experiment ID:** `{spec['id']}`",
        f"**Status:** `{summary['status'].upper()}`",
        f"**Criterion Outcome:** **{crit_status}**\n",
        "---\n",
        "## 1. Mathematical Statement & Criterion\n",
        f"- **Hypothesis:**\n  > {summary['hypothesis'].strip()}\n",
        f"{crit_summary_line}\n",
        "*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*\n",
        "---\n",
        "## 2. Multi-Metric Summary\n",
        "| Metric | Classification | Count | Min | Max | Max Abs |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
        f"{metrics_table}\n",
        "---\n",
        "## 3. Metric Diagnostics & Worst Points\n",
        f"{details_block}\n",
        "---\n",
        "## 4. Execution & Environment Metadata\n",
        f"- **Git Commit:** `{manifest['git_commit']}` (Dirty: `{manifest['git_dirty']}`)",
        f"- **Precision:** `{manifest['precision']['dps']} dps`",
        f"- **Tau Value:** `{tau_display}`",
        f"- **Points Requested:** `{manifest['points_requested']}`",
        f"- **Points Completed:** `{manifest['points_completed']}`",
        f"- **Started At:** `{manifest['started_at']}`",
        f"- **Completed At:** `{manifest['completed_at']}`\n",
        "---\n",
        "## 5. Artifact Index\n",
        "- Manifest: [`manifest.json`](manifest.json)",
        "- Summary: [`summary.json`](summary.json)",
        "- Detailed Points: [`results.jsonl`](results.jsonl)",
    ]
    if manifest.get("artifacts", {}).get("diagnostics_json"):
        readme_lines.append("- Diagnostics: [`diagnostics.json`](diagnostics.json)")
    readme_lines.append("")
    return "\n".join(readme_lines)


def generate_perturbation_rank_diagnostics(spec: Dict[str, Any], results: List[Dict[str, Any]], dps: int = 80) -> Dict[str, Any]:
    """Build complete, reconstructible linearized compensation diagnostics."""
    j_list = [1, 2, 3, 4, 5, 6]
    k_list = [-2, -1, 0, 1, 2]
    channels = [{"channel_index": i, "K": k, "j": j} for i, (k, j) in enumerate([(k, j) for k in k_list for j in j_list])]

    first_100_zeros = []
    first_100_ords = []
    for idx_100 in range(1, 101):
        ch, ok, zc, _ = _lookup_zero_certificate(idx_100, zero_family="nontrivial", check_provenance=False)
        ord_val = zc["enclosure"]["imag_mid"] if (zc and "enclosure" in zc) else reference_data.load_first_100_reference_zeros()[idx_100 - 1]
        first_100_ords.append(ord_val)
        first_100_zeros.append({
            "zero_index": idx_100,
            "ordinate": ord_val,
            "certificate_hash": ch if ch else "N/A"
        })

    J = math_core.explicit_formula_jacobian(j_list=j_list, k_list=k_list, zeros_subset=first_100_ords, dps=dps + 20)

    cases_diag = {}
    for rec in results:
        outs = rec.get("outputs", {})
        mode = outs.get("mode")
        if mode == "critical_height":
            n_idx = int(outs.get("zero_index", 1))
            eps_str = outs.get("epsilon", "0.001")
            eps_mpf = math_core.to_mpf(eps_str, dps=dps + 20)
            target_col = n_idx - 1
            comp_res = math_core.solve_linearized_compensation(
                J=J,
                target_col_idx=target_col,
                epsilon=eps_mpf,
                rank_tol_rel='1e-25',
                dps=dps + 20
            )
            case_key = f"critical_height_zero_{n_idx}_eps_{eps_str}"
            cases_diag[case_key] = {
                "mode": "critical_height",
                "target_zero_index": n_idx,
                "epsilon": eps_str,
                "excluded_target_column": target_col,
                "matrix_dimensions": [len(J), len(comp_res["other_indices"])],
                "singular_values": [mpmath.nstr(s, n=dps) for s in comp_res["singular_values"]],
                "threshold_sweep": comp_res["threshold_sweep"],
                "primary_threshold": "1e-25",
                "numerical_rank": comp_res["numerical_rank"],
                "nullity": comp_res["nullity"],
                "condition_number": mpmath.nstr(comp_res["condition_number"], n=8),
                "target_defect_vector": [mpmath.nstr(v, n=dps) for v in comp_res["v_target"]],
                "compensation_vector": [mpmath.nstr(x, n=dps) for x in comp_res["compensation_vector"]],
                "zero_index_mapping": [i + 1 for i in comp_res["other_indices"]],
                "forward_residual_vector": [mpmath.nstr(r, n=dps) for r in comp_res["residual_vector"]],
                "target_norm": mpmath.nstr(comp_res["v_norm"], n=dps),
                "compensation_norm": mpmath.nstr(comp_res["compensation_norm"], n=dps),
                "residual_norm": mpmath.nstr(comp_res["residual_norm"], n=dps),
                "relative_residual": mpmath.nstr(comp_res["relative_residual"], n=dps),
                "participating_indices": [i + 1 for i in comp_res["participating_indices"]],
                "participation_rule": "abs(x_i) > 1e-12 * norm(x)",
                "compensation_found": comp_res["compensation_found"],
                "working_precision_dps": dps
            }

    return {
        "schema_version": "2",
        "experiment_id": "explicit-formula-perturbation-rank-001",
        "channel_ordering": channels,
        "zero_column_ordering": first_100_zeros,
        "cases": cases_diag,
        "working_precision_dps": dps
    }


def generate_grade_covariance_diagnostics(spec: Dict[str, Any], results: List[Dict[str, Any]], dps: int = 80) -> Dict[str, Any]:
    """Build complete 30-channel global grade covariance diagnostics."""
    j_list = [1, 2, 3, 4, 5, 6]
    k_list = [-2, -1, 0, 1, 2]
    channels = [{"channel_index": i, "K": k, "j": j} for i, (k, j) in enumerate([(k, j) for k in k_list for j in j_list])]
    zeros = reference_data.load_reference_zeros()[:100]
    global_equiv = math_core.check_expanded_native_basis_equivalence(j_list=j_list, k_list=k_list, zeros_subset=zeros, dps=dps + 20)

    return {
        "schema_version": "2",
        "experiment_id": "explicit-formula-grade-covariance-001",
        "channel_ordering": channels,
        "num_zeros": len(zeros),
        "grade_matrix_dims": global_equiv["grade_matrix_dims"],
        "native_matrix_dims": global_equiv["native_matrix_dims"],
        "stacked_matrix_dims": global_equiv["stacked_matrix_dims"],
        "rank_grade": global_equiv["rank_grade"],
        "rank_native": global_equiv["rank_native"],
        "rank_stacked": global_equiv["rank_stacked"],
        "singular_values_grade": [mpmath.nstr(s, n=dps) for s in global_equiv["singular_values_grade"]],
        "singular_values_native": [mpmath.nstr(s, n=dps) for s in global_equiv["singular_values_native"]],
        "singular_values_stacked": [mpmath.nstr(s, n=dps) for s in global_equiv["singular_values_stacked"]],
        "threshold_sweep": global_equiv["threshold_sweep"],
        "max_discrepancy": mpmath.nstr(global_equiv["max_discrepancy"], n=dps),
        "max_value_discrepancy": mpmath.nstr(global_equiv["max_value_discrepancy"], n=dps),
        "max_fourier_discrepancy": mpmath.nstr(global_equiv["max_fourier_discrepancy"], n=dps),
        "theoretical_classification": global_equiv["theoretical_classification"],
        "finite_basis_classification": global_equiv["finite_basis_classification"],
        "categorical_equivalence_result": global_equiv["categorical_equivalence_result"],
        "working_precision_dps": dps
    }


def generate_radial_second_variation_diagnostics(spec: Dict[str, Any], results: List[Dict[str, Any]], dps: int = 80) -> Dict[str, Any]:
    """Build complete second-order radial response and NNLS diagnostics."""
    j_list = [1, 2, 3, 4, 5, 6]
    k_list = [-2, -1, 0, 1, 2]
    channels = [{"channel_index": i, "K": k, "j": j} for i, (k, j) in enumerate([(k, j) for k in k_list for j in j_list])]

    first_100_zeros = []
    first_100_ords = []
    for idx_100 in range(1, 101):
        ch, ok, zc, _ = _lookup_zero_certificate(idx_100, zero_family="nontrivial", check_provenance=False)
        ord_val = zc["enclosure"]["imag_mid"] if (zc and "enclosure" in zc) else reference_data.load_first_100_reference_zeros()[idx_100 - 1]
        first_100_ords.append(ord_val)
        first_100_zeros.append({
            "zero_index": idx_100,
            "ordinate": ord_val,
            "certificate_hash": ch if ch else "N/A"
        })

    K_mat = math_core.radial_second_order_jacobian(j_list=j_list, k_list=k_list, zeros_subset=first_100_ords, dps=dps + 20)

    cases_diag = {}
    for rec in results:
        outs = rec.get("outputs", {})
        z_idx = int(outs.get("zero_index", 1))
        d_str = outs.get("delta", "0.001")
        d_mpf = math_core.to_mpf(d_str, dps=dps + 20)
        u_mpf = d_mpf * d_mpf
        target_col = z_idx - 1
        nnls_res = math_core.solve_radial_second_order_nnls(
            K_mat=K_mat,
            target_col_idx=target_col,
            u_val=u_mpf,
            rank_tol_rel='1e-25',
            dps=dps + 20
        )
        case_key = f"radial_second_variation_zero_{z_idx}_delta_{d_str}"
        cases_diag[case_key] = {
            "target_zero_index": z_idx,
            "delta": d_str,
            "u": mpmath.nstr(u_mpf, n=dps),
            "excluded_target_column": target_col,
            "matrix_dimensions": [len(K_mat), len(nnls_res["other_indices"])],
            "singular_values": [mpmath.nstr(s, n=dps) for s in nnls_res["singular_values"]],
            "threshold_sweep": nnls_res["threshold_sweep"],
            "primary_threshold": "1e-25",
            "numerical_rank": nnls_res["numerical_rank"],
            "nullity": nnls_res["nullity"],
            "condition_number": mpmath.nstr(nnls_res["condition_number"], n=8),
            "quadratic_energy": mpmath.nstr(nnls_res["quadratic_energy"], n=dps),
            "unconstrained_residual_norm": mpmath.nstr(nnls_res["unconstrained_residual_norm"], n=dps),
            "unconstrained_relative_residual": mpmath.nstr(nnls_res["unconstrained_relative_residual"], n=dps),
            "nnls_solution_norm": mpmath.nstr(nnls_res["nnls_solution_norm"], n=dps),
            "nnls_residual_norm": mpmath.nstr(nnls_res["nnls_residual_norm"], n=dps),
            "nnls_relative_residual": mpmath.nstr(nnls_res["nnls_relative_residual"], n=dps),
            "nnls_compensation_found": nnls_res["nnls_compensation_found"],
            "nnls_residual_nonzero_at_threshold": nnls_res["nnls_residual_nonzero_at_threshold"],
            "finite_response_energy_positive": nnls_res["finite_response_energy_positive"],
            "participating_indices": [i + 1 for i in nnls_res["participating_indices"]],
            "working_precision_dps": dps
        }

    return {
        "schema_version": "2",
        "experiment_id": "explicit-formula-radial-second-variation-001",
        "channel_ordering": channels,
        "zero_column_ordering": first_100_zeros,
        "cases": cases_diag,
        "working_precision_dps": dps
    }


def update_index_file(run_entry: Dict[str, Any]):
    """Update research/index.json with the given canonical run entry in Schema v2 format atomically."""
    os.makedirs(RESEARCH_DIR, exist_ok=True)
    index_data: Dict[str, Any] = {"schema_version": "2", "runs": []}
    if os.path.exists(INDEX_FILE):
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
                if isinstance(raw, dict) and "runs" in raw:
                    index_data = raw
                elif isinstance(raw, list):
                    index_data = {"schema_version": "2", "runs": raw}
        except Exception:
            index_data = {"schema_version": "2", "runs": []}

    runs = index_data.get("runs", [])
    found = False
    for i, e in enumerate(runs):
        if e.get("experiment_id") == run_entry.get("experiment_id") or e.get("run_id") == run_entry.get("run_id"):
            runs[i] = run_entry
            found = True
            break
    if not found:
        runs.append(run_entry)

    index_data["runs"] = runs
    index_data["total_runs"] = len(runs)
    index_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    tmp_index = os.path.join(RESEARCH_DIR, f".index.json.{os.getpid()}.tmp")
    try:
        with open(tmp_index, "w", encoding="utf-8") as f:
            json.dump(index_data, f, indent=2)
        os.replace(tmp_index, INDEX_FILE)
    finally:
        if os.path.exists(tmp_index):
            try:
                os.remove(tmp_index)
            except Exception:
                pass


# ==============================================================================
# MAIN EXPERIMENT RUNNER ENGINE
# ==============================================================================

def run_experiment(
    spec_path: str,
    resume_run_id: Optional[str] = None,
    canonical_current: bool = False
) -> str:


    """
    Execute or resume an experiment sweep declared in a YAML spec file.
    Creates and manages all run artifacts according to EXPERIMENT_PROTOCOL.md.
    """
    if not os.path.exists(spec_path):
        raise FileNotFoundError(f"Spec file not found: {spec_path}")

    with open(spec_path, "r", encoding="utf-8") as f:
        raw_yaml = f.read()
        spec = yaml.safe_load(raw_yaml)

    is_valid, err_msg = validate_spec(spec)
    if not is_valid:
        raise ValueError(f"Invalid experiment specification in '{spec_path}': {err_msg}")

    spec_sha = hash_string(raw_yaml)
    git_commit, git_dirty = get_git_info()
    dps = spec["precision"]["dps"]
    tau_str = math_core.get_tau_str(dps=dps)

    grid = generate_parameter_grid(spec["parameters"], dps=dps)
    total_points = len(grid)

    exp_id = spec["id"]
    stable_dir = os.path.join(RUNS_DIR, exp_id)
    run_id = exp_id

    work_dir = os.path.join(RUNS_DIR, f".tmp_{exp_id}_{os.getpid()}")
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir, ignore_errors=True)

    if resume_run_id:
        if not os.path.exists(stable_dir):
            raise FileNotFoundError(f"Cannot resume: Run directory '{stable_dir}' does not exist")

        manifest_path = os.path.join(stable_dir, "manifest.json")
        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Cannot resume: Missing '{manifest_path}'")

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        if manifest.get("experiment_spec_sha256") != spec_sha:
            raise ValueError(
                f"Refusing resume: Spec hash mismatch! (Recorded: {manifest.get('experiment_spec_sha256')}, Current: {spec_sha})"
            )
        shutil.copytree(stable_dir, work_dir)
    else:
        os.makedirs(work_dir, exist_ok=True)

        manifest = {
            "schema_version": "2",
            "run_id": exp_id,
            "experiment_id": exp_id,
            "title": spec.get("title", exp_id),
            "epistemic_class": spec.get("epistemic_class", "exact_control"),
            "object_relationship": spec.get("object_relationship", "unknown"),
            "classification": spec.get("classification", "canonical_experiment"),
            "started_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": None,
            "status": "running",
            "git_commit": git_commit,
            "producing_git_commit": git_commit,
            "git_dirty": git_dirty,
            "experiment_spec_sha256": spec_sha,
            "precision": {"dps": dps},
            "parameter_space": spec["parameters"],
            "points_requested": total_points,
            "points_completed": 0,
            "tau": {
                "symbolic": "2*pi",
                "numeric_decimal": tau_str,
                "precision_dps": dps,
                "library": "mpmath"
            },
            "runtime": {
                "python": sys.version,
                "platform": sys.platform,
                "packages": {
                    "mpmath": getattr(mpmath, "__version__", "N/A"),
                    "flint": getattr(math_core, "flint_ctx", None) is not None
                }
            },
            "dependency_fingerprint": certification._get_dependency_fingerprint(),
            "source_code_hashes": certification._get_source_code_hashes(git_commit),
            "input_data_hashes": certification._get_input_data_hashes(git_commit),
            "code_modules": [
                {"path": m, "sha256": certification._get_source_code_hashes(git_commit).get(m, "N/A")}
                for m in certification.REQUIRED_SOURCE_MODULES
            ],
            "data_provenance": [
                {"path": f"data/{d}", "sha256": certification._get_input_data_hashes(git_commit).get(d, "N/A")}
                for d in certification.REQUIRED_INPUT_DATA_FILES
            ],
            "consumed_certificates": []
        }

        with open(os.path.join(work_dir, "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

    results_path = os.path.join(work_dir, "results.jsonl")

    completed_point_ids = set()
    existing_results = []
    if os.path.exists(results_path):
        with open(results_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        record = json.loads(line)
                        completed_point_ids.add(record["point_id"])
                        existing_results.append(record)
                    except Exception:
                        pass

    operation = spec["engine"]["operation"]
    all_results = list(existing_results)

    with open(results_path, "a", encoding="utf-8") as results_file:
        for point_id, inputs in enumerate(grid):
            if point_id in completed_point_ids:
                continue

            status, outputs, err_msg = evaluate_point(
                operation, inputs, dps=dps, param_space=spec.get("parameters")
            )
            point_record = {
                "point_id": point_id,
                "inputs": inputs,
                "outputs": outputs,
                "status": status,
                "error": err_msg
            }
            results_file.write(json.dumps(point_record) + "\n")
            results_file.flush()
            all_results.append(point_record)

    completed_points = len(all_results)
    final_status = "complete" if completed_points == total_points else "incomplete"

    consumed_cert_hashes: Set[str] = set()
    for rec in all_results:
        outs = rec.get("outputs", {})
        if isinstance(outs, dict):
            for k in ["source_zero_cert_hash", "worldline_cert_hash", "cert_hash", "zero1_cert_hash", "zero2_cert_hash"]:
                val = outs.get(k)
                if val and val != "N/A":
                    consumed_cert_hashes.add(str(val))

    manifest["status"] = final_status
    manifest["points_completed"] = completed_points
    manifest["completed_at"] = datetime.now(timezone.utc).isoformat()
    manifest["consumed_certificates"] = sorted(list(consumed_cert_hashes))
    manifest["dependency_fingerprint"] = certification._get_dependency_fingerprint()
    cur_src_hashes = certification._get_source_code_hashes(git_commit)
    cur_data_hashes = certification._get_input_data_hashes(git_commit)
    manifest["source_code_hashes"] = cur_src_hashes
    manifest["input_data_hashes"] = cur_data_hashes
    manifest["code_modules"] = [
        {"path": m, "sha256": cur_src_hashes.get(m, "N/A")}
        for m in certification.REQUIRED_SOURCE_MODULES
    ]
    manifest["data_provenance"] = [
        {"path": f"data/{d}", "sha256": cur_data_hashes.get(d, "N/A")}
        for d in certification.REQUIRED_INPUT_DATA_FILES
    ]

    summary = compute_summary(spec, exp_id, all_results, status=final_status)
    with open(os.path.join(work_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    readme_content = generate_run_readme(spec, manifest, summary)
    with open(os.path.join(work_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    try:
        handler = get_handler(exp_id)
        handler.generate_diagnostics(all_results, spec, work_dir)
    except KeyError:
        pass
    except Exception as e:
        manifest.setdefault("warnings", []).append(f"Diagnostics generation failed: {e}")

    with open(os.path.join(work_dir, "results.jsonl"), "rb") as rf:
        results_sha = hashlib.sha256(rf.read().replace(b"\r\n", b"\n")).hexdigest()
    with open(os.path.join(work_dir, "summary.json"), "rb") as sf:
        summary_sha = hashlib.sha256(sf.read().replace(b"\r\n", b"\n")).hexdigest()
    with open(os.path.join(work_dir, "README.md"), "rb") as rmf:
        readme_sha = hashlib.sha256(rmf.read().replace(b"\r\n", b"\n")).hexdigest()

    manifest["artifacts"] = {
        "results_jsonl": {
            "path": "results.jsonl",
            "sha256": results_sha
        },
        "summary_json": {
            "path": "summary.json",
            "sha256": summary_sha
        },
        "readme_md": {
            "path": "README.md",
            "sha256": readme_sha
        }
    }
    diag_file = os.path.join(work_dir, "diagnostics.json")
    diag_sha = None
    if os.path.exists(diag_file):
        with open(diag_file, "rb") as df:
            diag_sha = hashlib.sha256(df.read().replace(b"\r\n", b"\n")).hexdigest()
        manifest["artifacts"]["diagnostics_json"] = {
            "path": "diagnostics.json",
            "sha256": diag_sha
        }

    manifest["execution_provenance"] = {
        "results_sha256": results_sha,
        "producing_git_commit": git_commit,
        "git_dirty": git_dirty,
        "started_at": manifest["started_at"],
        "completed_at": manifest["completed_at"],
        "source_code_hashes": cur_src_hashes,
        "input_data_hashes": cur_data_hashes,
        "dependency_fingerprint": manifest["dependency_fingerprint"],
        "code_modules": manifest["code_modules"],
        "data_provenance": manifest["data_provenance"],
    }
    manifest["summary_provenance"] = {
        "summary_sha256": summary_sha,
        "readme_sha256": readme_sha,
        "diagnostics_sha256": diag_sha,
        "summary_git_commit": git_commit,
        "summarized_at": manifest["completed_at"],
        "summarizer_source_hashes": {
            "research_runner.py": cur_src_hashes.get("research_runner.py", "N/A"),
        }
    }

    with open(os.path.join(work_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    val_ok, val_errs = validate_manifest(manifest, all_results, spec=spec, canonical_current=canonical_current)

    if not val_ok:
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir, ignore_errors=True)
        raise RuntimeError(f"Canonical run publication rejected for '{exp_id}': {'; '.join(val_errs)}")

    run_entry = project_canonical_index_entry(manifest, summary, exp_id)
    if "notes" in spec and "notes" not in run_entry:
        run_entry["notes"] = spec["notes"]

    pid = os.getpid()
    backup_dir = os.path.join(RUNS_DIR, f".bak_{exp_id}_{pid}")
    backup_index_path = os.path.join(RESEARCH_DIR, f".index.json.bak_{pid}")

    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir, ignore_errors=True)
    if os.path.exists(backup_index_path):
        os.remove(backup_index_path)

    if os.path.exists(INDEX_FILE):
        shutil.copy2(INDEX_FILE, backup_index_path)
    if os.path.exists(stable_dir):
        shutil.copytree(stable_dir, backup_dir)

    # Atomic publication into stable_dir
    try:
        if os.path.exists(stable_dir):
            shutil.rmtree(stable_dir, ignore_errors=True)
        shutil.move(work_dir, stable_dir)
        update_index_file(run_entry)
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir, ignore_errors=True)
        if os.path.exists(backup_index_path):
            os.remove(backup_index_path)
    except Exception as e:
        if os.path.exists(stable_dir):
            shutil.rmtree(stable_dir, ignore_errors=True)
        if os.path.exists(backup_dir):
            shutil.move(backup_dir, stable_dir)
        if os.path.exists(backup_index_path):
            shutil.copy2(backup_index_path, INDEX_FILE)
            os.remove(backup_index_path)
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir, ignore_errors=True)
        raise e

    return exp_id


def summarize_run(run_id: str) -> Dict[str, Any]:
    """Recompute and return summary for an existing run."""
    run_dir = os.path.join(RUNS_DIR, run_id)
    if not os.path.exists(run_dir):
        raise FileNotFoundError(f"Run directory '{run_dir}' not found")

    manifest_path = os.path.join(run_dir, "manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    exp_id = manifest["experiment_id"]
    candidates = [
        os.path.join(EXPERIMENTS_DIR, f"{exp_id}.yaml"),
        os.path.join(EXPERIMENTS_DIR, f"{exp_id.replace('-', '_')}.yaml"),
        os.path.join(EXPERIMENTS_DIR, f"{exp_id.replace('_', '-')}.yaml"),
    ]
    spec_path = None
    for cand in candidates:
        if os.path.exists(cand):
            spec_path = cand
            break

    if not spec_path:
        for fname in os.listdir(EXPERIMENTS_DIR):
            if fname.endswith(".yaml") or fname.endswith(".yml"):
                p = os.path.join(EXPERIMENTS_DIR, fname)
                with open(p, "r", encoding="utf-8") as sf:
                    try:
                        s_data = yaml.safe_load(sf)
                        if s_data and (s_data.get("experiment_id") == exp_id or s_data.get("id") == exp_id):
                            spec_path = p
                            break
                    except Exception:
                        pass

    if not spec_path or not os.path.exists(spec_path):
        raise FileNotFoundError(f"Experiment spec for '{exp_id}' not found")

    with open(spec_path, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    results_path = os.path.join(run_dir, "results.jsonl")
    results = []
    if not os.path.exists(results_path):
        raise FileNotFoundError(f"Results file '{results_path}' not found")

    with open(results_path, "rb") as rf:
        raw_results_bytes = rf.read()
    results_sha_before = hashlib.sha256(raw_results_bytes.replace(b"\r\n", b"\n")).hexdigest()

    for line in raw_results_bytes.decode("utf-8").splitlines():
        if line.strip():
            results.append(json.loads(line))

    status = "complete" if len(results) >= manifest.get("points_requested", 0) else "incomplete"
    summary = compute_summary(spec, run_id, results, status=status)

    with open(os.path.join(run_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    readme_content = generate_run_readme(spec, manifest, summary)
    with open(os.path.join(run_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    try:
        handler = get_handler(exp_id)
        handler.generate_diagnostics(results, spec, run_dir)
    except KeyError:
        pass
    except Exception as e:
        manifest.setdefault("warnings", []).append(f"Diagnostics generation failed: {e}")

    with open(results_path, "rb") as rf:
        results_sha_after = hashlib.sha256(rf.read().replace(b"\r\n", b"\n")).hexdigest()
    if results_sha_before != results_sha_after:
        raise RuntimeError(f"summarize_run corrupted results.jsonl: SHA mismatch ({results_sha_before} != {results_sha_after})")

    with open(os.path.join(run_dir, "summary.json"), "rb") as sf:
        summary_sha = hashlib.sha256(sf.read().replace(b"\r\n", b"\n")).hexdigest()
    with open(os.path.join(run_dir, "README.md"), "rb") as rmf:
        readme_sha = hashlib.sha256(rmf.read().replace(b"\r\n", b"\n")).hexdigest()

    manifest.setdefault("artifacts", {})
    manifest["artifacts"]["results_jsonl"] = {"path": "results.jsonl", "sha256": results_sha_after}
    manifest["artifacts"]["summary_json"] = {"path": "summary.json", "sha256": summary_sha}
    manifest["artifacts"]["readme_md"] = {"path": "README.md", "sha256": readme_sha}

    diag_file = os.path.join(run_dir, "diagnostics.json")
    diag_sha = None
    if os.path.exists(diag_file):
        with open(diag_file, "rb") as df:
            diag_sha = hashlib.sha256(df.read().replace(b"\r\n", b"\n")).hexdigest()
        manifest["artifacts"]["diagnostics_json"] = {"path": "diagnostics.json", "sha256": diag_sha}

    commit, _ = get_git_info()
    cur_src = certification._get_source_code_hashes(commit)
    manifest["summary_provenance"] = {
        "summary_sha256": summary_sha,
        "readme_sha256": readme_sha,
        "diagnostics_sha256": diag_sha,
        "summary_git_commit": commit,
        "summarized_at": datetime.now(timezone.utc).isoformat(),
        "summarizer_source_hashes": {
            "research_runner.py": cur_src.get("research_runner.py", "N/A"),
        }
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return summary


REQUIRED_MANIFEST_BASE_FIELDS = [
    "schema_version",
    "run_id",
    "experiment_id",
    "title",
    "epistemic_class",
    "classification",
    "status",
    "precision",
    "parameter_space",
    "points_requested",
    "points_completed",
    "artifacts",
]

REQUIRED_MANIFEST_PROVENANCE_FIELDS = [
    "git_commit",
    "producing_git_commit",
    "git_dirty",
    "dependency_fingerprint",
    "source_code_hashes",
    "input_data_hashes",
    "code_modules",
    "data_provenance",
    "experiment_spec_sha256",
]

REQUIRED_ARTIFACT_MAPPINGS = {
    "results_jsonl": "results.jsonl",
    "summary_json": "summary.json",
    "readme_md": "README.md",
}

OPTIONAL_ARTIFACT_MAPPINGS = {
    "diagnostics_json": "diagnostics.json",
}


def project_canonical_index_entry(manifest: Dict[str, Any], summary: Dict[str, Any], exp_id: str) -> Dict[str, Any]:
    """Derive the canonical index entry projection from authoritative manifest and summary."""
    crit = summary.get("criterion", {}) if isinstance(summary, dict) else {}
    crit_met = crit.get("criterion_met") if isinstance(crit, dict) else None

    entry: Dict[str, Any] = {
        "schema_version": "2",
        "run_id": exp_id,
        "experiment_id": exp_id,
        "title": manifest.get("title", exp_id),
        "epistemic_class": manifest.get("epistemic_class", "exact_control"),
        "object_relationship": manifest.get("object_relationship", "unknown"),
        "classification": manifest.get("classification", "canonical_experiment"),
        "timestamp": manifest.get("started_at", ""),
        "git_commit": manifest.get("git_commit", ""),
        "producing_git_commit": manifest.get("producing_git_commit", ""),
        "git_dirty": manifest.get("git_dirty", False),
        "status": manifest.get("status", "complete"),
        "criterion_met": crit_met,
        "summary_path": f"research/runs/{exp_id}/summary.json",
        "manifest_path": f"research/runs/{exp_id}/manifest.json",
        "results_path": f"research/runs/{exp_id}/results.jsonl",
    }
    if "notes" in manifest:
        entry["notes"] = manifest["notes"]
    return entry


def validate_manifest(
    manifest: Dict[str, Any],
    results: Optional[List[Dict[str, Any]]] = None,
    spec: Optional[Dict[str, Any]] = None,
    canonical_current: bool = True
) -> Tuple[bool, List[str]]:
    """Validate a run manifest, results, and proof obligations against canonical contracts.

    Fails closed if:
    - Any required base or provenance field is missing, None, empty, or placeholder.
    - git_dirty is not boolean False.
    - git_commit or producing_git_commit is invalid or they disagree.
    - code_modules or data_provenance list representation disagrees with map representation.
    - Source/data hashes do not match historical commit or current workspace in canonical-current mode.
    - Experiment spec hash does not match canonical spec on disk.
    - Declared consumed certificate is missing from disk or fails strict verification.
    - Declared consumed certificate is not used by any result point.
    - Required point certificate is missing from consumed_certificates.
    - An operation's required certificates/hashes are missing or replaced by N/A.
    - A point claiming worldline_certified=true contains N/A hash or non-certified status.
    - Point parameters (index, grade K, radial delta) mismatch referenced certificates.
    - Source zero and worldline certificates do not belong to the same zero root.
    - Synthetic certificates are passed off as actual zeros or vice-versa.
    - Exact control experiments fail mathematical criterion or produce execution errors.
    """
    errors: List[str] = []
    if not isinstance(manifest, dict):
        return False, ["Manifest must be a dictionary"]

    # 1. Base identity and classification fields
    for req_k in REQUIRED_MANIFEST_BASE_FIELDS:
        val = manifest.get(req_k)
        if val is None or val == "" or val == "N/A":
            errors.append(f"Manifest missing or invalid required key '{req_k}'")

    # 2. Provenance fields presence and non-emptiness
    for req_p in REQUIRED_MANIFEST_PROVENANCE_FIELDS:
        val = manifest.get(req_p)
        if val is None or val == "" or val == "N/A":
            errors.append(f"Manifest missing or invalid required provenance field '{req_p}'")

    # 2b. Artifacts map schema, path integrity, and hash formatting
    artifacts_map = manifest.get("artifacts")
    if not isinstance(artifacts_map, dict) or not artifacts_map:
        errors.append("Manifest missing or empty 'artifacts' map")
    else:
        req_art_keys = set(REQUIRED_ARTIFACT_MAPPINGS.keys())
        allowed_art_keys = req_art_keys | set(OPTIONAL_ARTIFACT_MAPPINGS.keys())
        act_art_keys = set(artifacts_map.keys())
        missing_art = req_art_keys - act_art_keys
        if missing_art:
            errors.append(f"Manifest artifacts map missing required entries: {sorted(list(missing_art))}")
        extra_art = act_art_keys - allowed_art_keys
        if extra_art:
            errors.append(f"Manifest artifacts map contains unauthorized entries: {sorted(list(extra_art))}")

        all_art_mappings = {**REQUIRED_ARTIFACT_MAPPINGS, **OPTIONAL_ARTIFACT_MAPPINGS}
        seen_paths: Set[str] = set()
        for art_key, exp_fname in all_art_mappings.items():
            if art_key not in artifacts_map:
                continue
            art_entry = artifacts_map[art_key]
            if not isinstance(art_entry, dict):
                errors.append(f"Manifest artifacts entry '{art_key}' must be a dictionary")
                continue

            decl_path = art_entry.get("path")
            if not isinstance(decl_path, str) or not decl_path:
                errors.append(f"Manifest artifacts entry '{art_key}' missing 'path'")
            else:
                if "\\" in decl_path or decl_path.startswith("/") or ".." in decl_path or ":" in decl_path:
                    errors.append(f"Manifest artifacts entry '{art_key}' path has invalid format, traversal, or backslash: '{decl_path}'")
                elif decl_path != exp_fname:
                    errors.append(f"Manifest artifacts entry '{art_key}' declared path '{decl_path}' != expected canonical path '{exp_fname}'")
                elif decl_path in seen_paths:
                    errors.append(f"Manifest artifacts entry '{art_key}' duplicate destination path: '{decl_path}'")
                else:
                    seen_paths.add(decl_path)

            decl_sha = art_entry.get("sha256")
            if not decl_sha or len(decl_sha) != 64 or not all(c in "0123456789abcdefABCDEF" for c in decl_sha) or decl_sha.lower() in ("0" * 64, "fake", "none"):
                errors.append(f"Manifest artifacts entry '{art_key}' missing or invalid 64-hex SHA-256: '{decl_sha}'")

    # 3. git_dirty must be strictly boolean False
    if manifest.get("git_dirty") is not False:
        errors.append(f"Manifest git_dirty must be boolean False, got {manifest.get('git_dirty')}")



    # 4. Commit and producing commit validation
    commit = str(manifest.get("git_commit", "")).strip()
    prod_commit = str(manifest.get("producing_git_commit", "")).strip()
    if not commit or len(commit) != 40 or not all(c in "0123456789abcdefABCDEF" for c in commit) or commit.lower() in ("0000000000000000000000000000000000000000", "unknown", "fake", "forged"):
        errors.append(f"Manifest git_commit is invalid: '{commit}'")
    if not prod_commit or len(prod_commit) != 40 or not all(c in "0123456789abcdefABCDEF" for c in prod_commit) or prod_commit.lower() in ("0000000000000000000000000000000000000000", "unknown", "fake", "forged"):
        errors.append(f"Manifest producing_git_commit is invalid: '{prod_commit}'")
    if commit and prod_commit and commit != prod_commit:
        errors.append(f"Manifest git_commit '{commit}' does not match producing_git_commit '{prod_commit}'")

    # 5. Dependency fingerprint validation
    dep_fp = manifest.get("dependency_fingerprint")
    if not isinstance(dep_fp, dict) or not dep_fp:
        errors.append("Manifest missing or empty dependency_fingerprint map")
    else:
        dep_ok, dep_errs = certification.validate_dependency_compatibility(dep_fp, check_current_runtime=True)
        if not dep_ok:
            errors.extend(dep_errs)

    # 6. Source code hashes and code_modules list validation
    src_hashes = manifest.get("source_code_hashes")
    if not isinstance(src_hashes, dict) or not src_hashes:
        errors.append("Manifest missing or empty source_code_hashes map")
    else:
        for mod in certification.REQUIRED_SOURCE_MODULES:
            mh = src_hashes.get(mod)
            if not mh or len(mh) != 64 or mh == "N/A" or not all(c in "0123456789abcdefABCDEF" for c in mh):
                errors.append(f"source_code_hashes missing or invalid for required module '{mod}'")

    code_mods = manifest.get("code_modules")
    if not isinstance(code_mods, list) or len(code_mods) != len(certification.REQUIRED_SOURCE_MODULES):
        errors.append(f"code_modules list must contain exactly {len(certification.REQUIRED_SOURCE_MODULES)} modules")
    elif isinstance(src_hashes, dict):
        seen_mods: Set[str] = set()
        for m_entry in code_mods:
            if not isinstance(m_entry, dict):
                errors.append("Malformed entry in code_modules list")
                continue
            p = m_entry.get("path")
            sh = m_entry.get("sha256")
            if not isinstance(p, str):
                errors.append("Malformed entry in code_modules list: missing string 'path'")
                continue
            if p in seen_mods:
                errors.append(f"Duplicate module '{p}' in code_modules")
            seen_mods.add(p)
            if p not in certification.REQUIRED_SOURCE_MODULES:
                errors.append(f"Unexpected module '{p}' in code_modules")
            elif sh != src_hashes.get(p):
                errors.append(f"code_modules sha256 mismatch for '{p}': list {sh} != map {src_hashes.get(p)}")

    # 7. Input data hashes and data_provenance list validation
    data_hashes = manifest.get("input_data_hashes")
    if not isinstance(data_hashes, dict) or not data_hashes:
        errors.append("Manifest missing or empty input_data_hashes map")
    else:
        for df in certification.REQUIRED_INPUT_DATA_FILES:
            dh = data_hashes.get(df)
            if not dh or len(dh) != 64 or dh == "N/A" or not all(c in "0123456789abcdefABCDEF" for c in dh):
                errors.append(f"input_data_hashes missing or invalid for required data file '{df}'")

    data_prov = manifest.get("data_provenance")
    if not isinstance(data_prov, list) or len(data_prov) != len(certification.REQUIRED_INPUT_DATA_FILES):
        errors.append(f"data_provenance list must contain exactly {len(certification.REQUIRED_INPUT_DATA_FILES)} data files")
    elif isinstance(data_hashes, dict):
        seen_data: Set[str] = set()
        for d_entry in data_prov:
            if not isinstance(d_entry, dict):
                errors.append("Malformed entry in data_provenance list")
                continue
            p = d_entry.get("path", "")
            sh = d_entry.get("sha256")
            if not isinstance(p, str):
                errors.append("Malformed entry in data_provenance list: missing string 'path'")
                continue
            if p in seen_data:
                errors.append(f"Duplicate data file '{p}' in data_provenance")
            seen_data.add(p)

            df_name = p.replace("data/", "", 1) if p.startswith("data/") else p
            if df_name not in certification.REQUIRED_INPUT_DATA_FILES:
                errors.append(f"Unexpected data file '{p}' in data_provenance")
            elif sh != data_hashes.get(df_name):
                errors.append(f"data_provenance sha256 mismatch for '{p}': list {sh} != map {data_hashes.get(df_name)}")

    # 8. Git commit historical blob verification
    if commit and isinstance(src_hashes, dict) and isinstance(data_hashes, dict):
        commit_ok, commit_err = certification._is_valid_git_commit(
            commit,
            source_code_hashes=src_hashes,
            input_data_hashes=data_hashes
        )
        if not commit_ok:
            errors.append(f"Invalid manifest git_commit provenance: {commit_err}")

    exp_id = manifest.get("experiment_id", "")
    try:
        handler = get_handler(exp_id)
        req_mods = handler.declared_dependencies.all_source_files
        req_data = handler.declared_dependencies.all_data_files
    except KeyError:
        req_mods = certification.REQUIRED_SOURCE_MODULES
        req_data = certification.REQUIRED_INPUT_DATA_FILES

    # 9. Current workspace source and data compatibility
    if canonical_current and isinstance(src_hashes, dict) and isinstance(data_hashes, dict):
        curr_src = certification._get_source_code_hashes(modules=req_mods)
        for mod in req_mods:
            curr_h = curr_src.get(mod, "N/A")
            if curr_h == "N/A":
                errors.append(f"Required current source module '{mod}' missing on disk")
            elif curr_h != src_hashes.get(mod):
                errors.append(f"Current source module '{mod}' hash mismatch: disk {curr_h}, manifest {src_hashes.get(mod)}")

        curr_data = certification._get_input_data_hashes(files=req_data)
        for df in req_data:
            df_name = df.replace("data/", "", 1) if df.startswith("data/") else df
            curr_dh = curr_data.get(df_name, "N/A")
            if curr_dh == "N/A":
                errors.append(f"Required current input data file '{df_name}' missing on disk")
            elif curr_dh != data_hashes.get(df_name):
                errors.append(f"Current input data file '{df_name}' hash mismatch: disk {curr_dh}, manifest {data_hashes.get(df_name)}")

    # 9b. Execution and Summary Provenance structure validation (when present)
    exec_prov = manifest.get("execution_provenance")
    if exec_prov is not None:
        if not isinstance(exec_prov, dict):
            errors.append("Manifest 'execution_provenance' must be a dictionary")
        elif not exec_prov.get("results_sha256") or len(exec_prov.get("results_sha256", "")) != 64:
            errors.append("Manifest 'execution_provenance' missing valid 64-hex 'results_sha256'")

    summ_prov = manifest.get("summary_provenance")
    if summ_prov is not None:
        if not isinstance(summ_prov, dict):
            errors.append("Manifest 'summary_provenance' must be a dictionary")
        elif not summ_prov.get("summary_sha256") or len(summ_prov.get("summary_sha256", "")) != 64:
            errors.append("Manifest 'summary_provenance' missing valid 64-hex 'summary_sha256'")
    if spec is None and exp_id:
        candidates = [
            os.path.join(EXPERIMENTS_DIR, f"{exp_id}.yaml"),
            os.path.join(EXPERIMENTS_DIR, f"{exp_id.replace('-', '_')}.yaml"),
            os.path.join(EXPERIMENTS_DIR, f"{exp_id.replace('_', '-')}.yaml"),
        ]
        for cand in candidates:
            if os.path.exists(cand):
                try:
                    with open(cand, "r", encoding="utf-8") as sf:
                        spec = yaml.safe_load(sf)
                    break
                except Exception:
                    pass

    # 10. Experiment spec SHA-256 validation
    spec_sha = manifest.get("experiment_spec_sha256")
    if not spec_sha or len(spec_sha) != 64 or spec_sha == "N/A" or not all(c in "0123456789abcdefABCDEF" for c in spec_sha):
        errors.append(f"Manifest missing or invalid experiment_spec_sha256: '{spec_sha}'")
    elif exp_id:
        spec_file = os.path.join(EXPERIMENTS_DIR, f"{exp_id}.yaml")
        if os.path.exists(spec_file):
            with open(spec_file, "rb") as sf:
                actual_spec_sha = hashlib.sha256(sf.read().replace(b"\r\n", b"\n")).hexdigest()
            if actual_spec_sha != spec_sha:
                errors.append(f"Manifest experiment_spec_sha256 '{spec_sha}' != disk spec hash '{actual_spec_sha}'")

    op_name = (
        manifest.get("operation")
        or (spec.get("engine", {}).get("operation") if isinstance(spec, dict) else None)
        or (spec.get("operation") if isinstance(spec, dict) else None)
        or manifest.get("engine", {}).get("operation")
    )
    op_obl = OPERATION_CERTIFICATE_OBLIGATIONS.get(op_name, {})

    consumed = set(manifest.get("consumed_certificates", []))
    if op_obl.get("requires_consumed_certs") and len(consumed) == 0:
        errors.append(f"Operation '{op_name}' requires consumed certificates but manifest consumed_certificates is empty")

    cert_root = os.path.join(REPO_ROOT, "data", "certificates")
    cert_map: Dict[str, Dict[str, Any]] = {}
    for c_hash in consumed:
        if not isinstance(c_hash, str) or len(c_hash) != 64:
            errors.append(f"Invalid consumed certificate hash format: '{c_hash}'")
            continue
        found_cert = None
        for subdir in ["zeros", "trivial_zeros", "blocks", "worldlines"]:
            cand_files = glob.glob(os.path.join(cert_root, subdir, "*.json"))
            for cf in cand_files:
                try:
                    with open(cf, "r", encoding="utf-8") as f:
                        c_data = json.load(f)
                    if c_data.get("certificate_hash") == c_hash:
                        found_cert = c_data
                        break
                except Exception:
                    pass
            if found_cert is not None:
                break

        if found_cert is None:
            errors.append(f"Consumed certificate hash '{c_hash}' not found in data/certificates/")
        else:
            cert_map[c_hash] = found_cert
            ok, c_errs = certification.verify_certificate(found_cert, check_provenance=True, canonical_current=canonical_current)
            if not ok:
                errors.append(f"Consumed certificate '{c_hash}' failed verification: {'; '.join(c_errs)}")

    if results is not None:
        pts_req = manifest.get("points_requested", 0)
        pts_comp = manifest.get("points_completed", len(results))
        if manifest.get("status") == "complete":
            if len(results) != pts_req or pts_comp != pts_req:
                errors.append(f"Run claims status='complete' but results count ({len(results)}) != requested ({pts_req})")

        used_in_points: Set[str] = set()
        for idx, rec in enumerate(results):
            if manifest.get("status") == "complete" and rec.get("status") != "ok":
                errors.append(f"Point {idx} (id={rec.get('point_id')}) has failed status '{rec.get('status')}'")

            outs = rec.get("outputs", {})
            rec_in = rec.get("inputs", {})
            if not isinstance(outs, dict):
                continue

            if manifest.get("status") == "complete" and "point_error" in outs:
                errors.append(f"Point {idx} contains point_error: {outs.get('point_error')}")

            for k in ["source_zero_cert_hash", "worldline_cert_hash", "cert_hash", "zero1_cert_hash", "zero2_cert_hash"]:
                h_val = outs.get(k)
                if h_val and h_val != "N/A":
                    h_str = str(h_val)
                    used_in_points.add(h_str)
                    if h_str not in consumed:
                        errors.append(f"Point {idx} uses certificate {h_str} which is missing from manifest consumed_certificates")

            if str(outs.get("worldline_certified")).lower() == "true":
                if not outs.get("worldline_cert_hash") or outs.get("worldline_cert_hash") == "N/A":
                    errors.append(f"Point {idx} claims worldline_certified=true but worldline_cert_hash is 'N/A'")

            if op_obl.get("requires_certified_flag"):
                c_flag = outs.get("worldline_certified")
                if c_flag is None or str(c_flag).lower() != "true":
                    errors.append(f"Point {idx} operation '{op_name}' requires worldline_certified=true, got '{c_flag}'")

            if op_obl.get("requires_source_cert"):
                sz_h = outs.get("source_zero_cert_hash")
                if not sz_h or sz_h == "N/A":
                    errors.append(f"Point {idx} operation '{op_name}' missing source_zero_cert_hash")
                elif sz_h in cert_map:
                    szc = cert_map[sz_h]
                    exp_family = op_obl.get("source_family", "nontrivial")
                    if szc.get("zero_family") != exp_family:
                        errors.append(f"Point {idx} source zero family ({szc.get('zero_family')}) != expected ({exp_family})")
                    exp_src_stat = op_obl.get("expected_source_status", "simple_zero_certified")
                    if szc.get("status") != exp_src_stat:
                        errors.append(f"Point {idx} source zero status ({szc.get('status')}) != expected ({exp_src_stat})")

            if op_obl.get("requires_worldline_cert"):
                wl_h = outs.get("worldline_cert_hash")
                if not wl_h or wl_h == "N/A":
                    errors.append(f"Point {idx} operation '{op_name}' missing worldline_cert_hash")
                elif wl_h in cert_map:
                    wlc = cert_map[wl_h]
                    exp_wl_stat = op_obl.get("expected_worldline_status", "worldline_certified")
                    if wlc.get("status") != exp_wl_stat:
                        errors.append(f"Point {idx} worldline status ({wlc.get('status')}) != expected ({exp_wl_stat})")

                    sz_h = outs.get("source_zero_cert_hash")
                    if sz_h and sz_h in cert_map:
                        szc = cert_map[sz_h]
                        wl_src_h = wlc.get("source_zero_hash")
                        if wl_src_h and wl_src_h != sz_h:
                            errors.append(f"Point {idx} worldline source_zero_hash ({wl_src_h}) != point source_zero_cert_hash ({sz_h})")

                        sz_idx = szc.get("nontrivial_index") or szc.get("trivial_index")
                        wl_idx = wlc.get("nontrivial_index") or wlc.get("trivial_index") or wlc.get("source_zero_index")
                        if sz_idx is not None and wl_idx is not None and sz_idx != wl_idx:
                            errors.append(f"Point {idx} zero index mismatch between source cert ({sz_idx}) and worldline cert ({wl_idx})")

                    k_in = rec_in.get("grade_k", rec_in.get("K", rec_in.get("k", 0)))
                    if int(wlc.get("grade_K", 0)) != int(k_in):
                        errors.append(f"Point {idx} grade mismatch: input {k_in} != worldline cert {wlc.get('grade_K')}")

                    if op_obl.get("source_family") != "trivial":
                        pt_d = rec_in.get("radial_delta", rec_in.get("delta", rec_in.get("delta_val", 0.0)))
                        if wlc.get("delta") is not None:
                            try:
                                if abs(float(pt_d) - float(wlc["delta"])) > 1e-4:
                                    errors.append(f"Point {idx} input delta={pt_d} does not match worldline cert delta={wlc['delta']}")
                            except Exception:
                                pass

                        if op_obl.get("is_synthetic") is True:
                            if abs(float(wlc.get("delta", 0.0))) < 1e-6:
                                errors.append(f"Point {idx} synthetic operation uses delta=0.0 actual zero cert")
                        elif op_obl.get("is_synthetic") is False:
                            if abs(float(wlc.get("delta", 0.0))) > 1e-6:
                                errors.append(f"Point {idx} actual zero operation uses synthetic delta={wlc.get('delta')} cert")
                    else:
                        m_idx = int(rec_in.get("trivial_index") or rec_in.get("m") or 1)
                        exp_delta = str(-2 * m_idx - 0.5)
                        if abs(float(wlc.get("delta", 0.0)) - float(exp_delta)) > 1e-4:
                            errors.append(f"Point {idx} trivial zero m={m_idx} worldline cert delta ({wlc.get('delta')}) != expected ({exp_delta})")

        unused_consumed = consumed - used_in_points
        if unused_consumed:
            errors.append(f"Declared consumed certificates unused by any point: {sorted(list(unused_consumed))}")

        if spec is not None:
            recomputed_summary = compute_summary(spec, exp_id, results, status=manifest.get("status", "complete"))
            if spec.get("epistemic_class") == "exact_control":
                if recomputed_summary["criterion"].get("criterion_met") is not True:
                    errors.append(f"Exact control experiment '{exp_id}' failed criterion check: observed={recomputed_summary['criterion'].get('observed')}")
            if manifest.get("status") == "complete" and recomputed_summary.get("points_failed", 0) > 0:
                errors.append(f"Run claims status='complete' but {recomputed_summary['points_failed']} points failed")

    return len(errors) == 0, errors


def validate_run_bundle(
    run_dir_or_exp_id: str,
    require_provenance: bool = True,
    canonical_current: bool = True
) -> Tuple[bool, List[str]]:
    """Validate a complete committed canonical run bundle including:
    - manifest.json (schema, provenance, hashes, certificates, and artifacts map)
    - results.jsonl (completeness, point status, proof obligations, byte SHA-256)
    - summary.json (recomputed full multi-metric match, byte SHA-256)
    - README.md (presence, inventory, byte SHA-256)
    - research/index.json (presence and strict sync of matching run entry)
    - research/experiments/<exp_id>.yaml (spec SHA-256 match)
    - Directory cleanliness (no temporary or extra files)
    """
    errors: List[str] = []
    run_dir = run_dir_or_exp_id if os.path.isdir(run_dir_or_exp_id) else os.path.join(RUNS_DIR, run_dir_or_exp_id)
    if not os.path.exists(run_dir):
        return False, [f"Run directory '{run_dir}' does not exist"]

    exp_id = os.path.basename(run_dir.rstrip("/\\"))

    # 1. Directory hygiene: reject unexpected or temporary files
    try:
        entries = sorted(os.listdir(run_dir))
        allowed_files = {"manifest.json", "results.jsonl", "summary.json", "README.md", "diagnostics.json"}
        extra_files = set(entries) - allowed_files
        if extra_files:
            errors.append(f"Run bundle '{exp_id}' contains unauthorized or temporary files: {sorted(list(extra_files))}")
    except Exception as e:
        errors.append(f"Failed inspecting run directory entries: {e}")

    manifest_path = os.path.join(run_dir, "manifest.json")
    results_path = os.path.join(run_dir, "results.jsonl")
    summary_path = os.path.join(run_dir, "summary.json")
    readme_path = os.path.join(run_dir, "README.md")

    if not os.path.exists(manifest_path):
        errors.append(f"Run bundle '{exp_id}' missing manifest.json")
        return False, errors

    try:
        with open(manifest_path, "r", encoding="utf-8") as mf:
            manifest = json.load(mf)
    except Exception as e:
        return False, [f"Run bundle '{exp_id}' failed reading manifest.json: {e}"]

    # 2. Artifact byte hashes validation against declared paths
    artifacts_map = manifest.get("artifacts")
    if not isinstance(artifacts_map, dict) or not artifacts_map:
        errors.append(f"Run bundle '{exp_id}' manifest missing 'artifacts' map")
    else:
        all_art_mappings = {**REQUIRED_ARTIFACT_MAPPINGS, **OPTIONAL_ARTIFACT_MAPPINGS}
        for art_key, exp_fname in REQUIRED_ARTIFACT_MAPPINGS.items():
            if art_key not in artifacts_map:
                errors.append(f"Manifest artifacts map missing required entry '{art_key}'")

        for art_key, exp_fname in all_art_mappings.items():
            if art_key not in artifacts_map:
                continue
            art_entry = artifacts_map.get(art_key)
            if not isinstance(art_entry, dict) or not art_entry.get("sha256"):
                errors.append(f"Manifest artifacts map missing entry or sha256 for '{art_key}'")
            else:
                decl_path = art_entry.get("path", exp_fname)
                decl_sha = art_entry.get("sha256")
                full_art_path = os.path.join(run_dir, decl_path)
                if not os.path.exists(full_art_path):
                    errors.append(f"Declared artifact file '{decl_path}' missing in run bundle '{exp_id}'")
                else:
                    with open(full_art_path, "rb") as af:
                        calc_sha = hashlib.sha256(af.read().replace(b"\r\n", b"\n")).hexdigest()
                    if decl_sha and calc_sha != decl_sha:
                        errors.append(f"Artifact byte SHA-256 mismatch for '{decl_path}': computed {calc_sha}, declared {decl_sha}")

    results = []
    if os.path.exists(results_path):
        try:
            with open(results_path, "r", encoding="utf-8") as rf:
                for line in rf:
                    if line.strip():
                        results.append(json.loads(line))
        except Exception as e:
            errors.append(f"Run bundle '{exp_id}' failed reading results.jsonl: {e}")
    else:
        errors.append(f"Run bundle '{exp_id}' missing results.jsonl")

    candidates = [
        os.path.join(EXPERIMENTS_DIR, f"{exp_id}.yaml"),
        os.path.join(EXPERIMENTS_DIR, f"{exp_id.replace('-', '_')}.yaml"),
        os.path.join(EXPERIMENTS_DIR, f"{exp_id.replace('_', '-')}.yaml"),
    ]
    spec_path = None
    for cand in candidates:
        if os.path.exists(cand):
            spec_path = cand
            break
    if not spec_path:
        for fname in os.listdir(EXPERIMENTS_DIR):
            if fname.endswith(".yaml") or fname.endswith(".yml"):
                p = os.path.join(EXPERIMENTS_DIR, fname)
                try:
                    with open(p, "r", encoding="utf-8") as sf:
                        s_data = yaml.safe_load(sf)
                    if s_data and (s_data.get("experiment_id") == exp_id or s_data.get("id") == exp_id):
                        spec_path = p
                        break
                except Exception:
                    pass

    spec = None
    if spec_path and os.path.exists(spec_path):
        try:
            with open(spec_path, "r", encoding="utf-8") as sf:
                spec = yaml.safe_load(sf)
            spec_sha = hash_file_bytes(spec_path)
            rep_spec_sha = manifest.get("experiment_spec_sha256")
            if rep_spec_sha and rep_spec_sha != spec_sha:
                errors.append(f"Manifest experiment_spec_sha256 '{rep_spec_sha}' does not match disk spec hash '{spec_sha}'")
        except Exception as e:
            errors.append(f"Failed reading spec '{spec_path}': {e}")
    else:
        errors.append(f"No experiment specification found for '{exp_id}'")

    # 3. Validate manifest schema, provenance, and results obligations
    ok_m, m_errs = validate_manifest(manifest, results, spec=spec, canonical_current=canonical_current)
    if not ok_m:
        errors.extend(m_errs)

    # 4. Summary recomputation and complete deterministic semantic field comparison
    committed_summary: Dict[str, Any] = {}
    if not os.path.exists(summary_path):
        errors.append(f"Run bundle '{exp_id}' missing summary.json")
    elif spec is not None:
        try:
            with open(summary_path, "r", encoding="utf-8") as sf:
                committed_summary = json.load(sf)
            recomputed = compute_summary(spec, exp_id, results, status=manifest.get("status", "complete"))

            for fld in [
                "schema_version",
                "status",
                "points_requested",
                "points_completed",
                "points_failed",
                "metrics",
                "report_metrics",
                "criterion",
                "extrema",
                "anomalies",
                "warnings"
            ]:
                comm_v = committed_summary.get(fld)
                recomp_v = recomputed.get(fld)
                if comm_v != recomp_v:
                    errors.append(f"Summary field '{fld}' mismatch: committed={comm_v}, recomputed={recomp_v}")

            if spec.get("epistemic_class") == "exact_control" and recomputed.get("criterion", {}).get("criterion_met") is not True:
                errors.append(f"Exact control experiment '{exp_id}' criterion not met: observed={recomputed.get('criterion', {}).get('observed')}")
        except Exception as e:
            errors.append(f"Failed validating summary.json: {e}")

    if not os.path.exists(readme_path):
        errors.append(f"Run bundle '{exp_id}' missing README.md")

    # 5. Index entry synchronization against complete canonical projection
    if not os.path.exists(INDEX_FILE):
        errors.append("research/index.json missing")
    else:
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as inf:
                idx_data = json.load(inf)
            runs = idx_data.get("runs", []) if isinstance(idx_data, dict) else (idx_data if isinstance(idx_data, list) else [])
            matching_entries = [r for r in runs if isinstance(r, dict) and (r.get("experiment_id") == exp_id or r.get("run_id") == exp_id)]
            if not matching_entries:
                errors.append(f"No entry for experiment '{exp_id}' in research/index.json")
            elif len(matching_entries) > 1:
                errors.append(f"Duplicate entries ({len(matching_entries)}) for experiment '{exp_id}' in research/index.json")
            else:
                found_entry = matching_entries[0]
                expected_entry = project_canonical_index_entry(manifest, committed_summary, exp_id)
                if spec is not None and "notes" in spec and "notes" not in expected_entry:
                    expected_entry["notes"] = spec["notes"]

                REQUIRED_INDEX_FIELDS = [
                    "schema_version",
                    "run_id",
                    "experiment_id",
                    "title",
                    "epistemic_class",
                    "object_relationship",
                    "classification",
                    "timestamp",
                    "git_commit",
                    "producing_git_commit",
                    "git_dirty",
                    "status",
                    "criterion_met",
                    "manifest_path",
                    "results_path",
                    "summary_path",
                ]
                for fld in REQUIRED_INDEX_FIELDS:
                    act_v = found_entry.get(fld)
                    exp_v = expected_entry.get(fld)
                    if act_v != exp_v:
                        errors.append(f"Index entry '{fld}' mismatch for '{exp_id}': index '{act_v}' != expected '{exp_v}'")

                for k, v in found_entry.items():
                    if isinstance(v, str) and v.lower() in ("placeholder", "unknown", "fake", "forged"):
                        errors.append(f"Index entry contains placeholder for '{k}': '{v}'")

        except Exception as e:
            errors.append(f"Failed validating index.json entry: {e}")

    return len(errors) == 0, errors


def list_runs() -> List[Dict[str, Any]]:
    """List all recorded runs in research/index.json."""
    if not os.path.exists(INDEX_FILE):
        return []
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict) and "runs" in data:
            return data["runs"]
        elif isinstance(data, list):
            return data
        return []


# ==============================================================================
# CLI INTERFACE
# ==============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python research_runner.py [run <spec.yaml> [--resume <run_id>] | summarize <run_id> | list | validate [run_id]]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "run":
        if len(sys.argv) < 3:
            print("Error: Spec file required: python research_runner.py run <spec.yaml> [--resume <run_id>]")
            sys.exit(1)
        spec_file = sys.argv[2]
        resume_id = None
        if len(sys.argv) >= 5 and sys.argv[3] == "--resume":
            resume_id = sys.argv[4]

        print(f"Executing experiment sweep: {spec_file}...")
        run_id = run_experiment(spec_file, resume_run_id=resume_id)
        print(f"Run completed successfully: {run_id}")

        sum_path = os.path.join(RUNS_DIR, run_id, "summary.json")
        if os.path.exists(sum_path):
            with open(sum_path, "r", encoding="utf-8") as sf:
                summary = json.load(sf)
                crit = summary["criterion"]
                print(f"Status: {summary['status']}")
                print(f"Points Completed: {summary['points_completed']}/{summary['points_requested']}")
                print(f"Criterion: {crit['metric']} {crit['operator']} {crit['threshold']}")
                print(f"Observed: {crit['observed']}")
                print(f"Criterion Met: {crit['criterion_met']}")

    elif cmd in ("run-all", "run_all", "batch"):
        specs = sorted(glob.glob(os.path.join(EXPERIMENTS_DIR, "*.yaml")))
        print(f"Executing {len(specs)} canonical experiment sweeps...")
        for sf in specs:
            name = os.path.basename(sf)
            print(f"\n--- Running {name} ---")
            r_id = run_experiment(sf)
            s_dict = summarize_run(r_id)
            c = s_dict.get("criterion", {})
            print(f"[{name}] {r_id}: status={s_dict.get('status')} criterion_met={c.get('criterion_met')} observed={c.get('observed')}")
        print("\nAll canonical experiment sweeps complete.")

    elif cmd == "validate":
        target = sys.argv[2] if len(sys.argv) >= 3 else None
        if target:
            ok, errs = validate_run_bundle(target)
            if ok:
                print(f"[PASS] Run bundle '{target}' validated successfully.")
            else:
                print(f"[FAIL] Run bundle '{target}' validation errors:\n- " + "\n- ".join(errs))
                sys.exit(1)
        else:
            all_ok = True
            for r_dir in sorted(glob.glob(os.path.join(RUNS_DIR, "*"))):
                if os.path.isdir(r_dir) and not os.path.basename(r_dir).startswith("."):
                    b_name = os.path.basename(r_dir)
                    ok, errs = validate_run_bundle(r_dir)
                    if ok:
                        print(f"[PASS] {b_name}")
                    else:
                        print(f"[FAIL] {b_name}:\n  - " + "\n  - ".join(errs))
                        all_ok = False
            if not all_ok:
                sys.exit(1)
            print("\nAll canonical run bundles validated successfully.")

    elif cmd == "summarize":
        if len(sys.argv) < 3:
            print("Error: Run ID required: python research_runner.py summarize <run_id>")
            sys.exit(1)
        run_id = sys.argv[2]
        summary = summarize_run(run_id)
        print(json.dumps(summary, indent=2))

    elif cmd == "list":
        runs = list_runs()
        print(f"Total recorded runs: {len(runs)}")
        for r in runs:
            print(f"- {r['run_id']} | Exp: {r['experiment_id']} | Status: {r['status']} | Met: {r.get('criterion_met')}")

    else:
        print(f"Unknown command '{cmd}'")
        sys.exit(1)


if __name__ == "__main__":
    main()
