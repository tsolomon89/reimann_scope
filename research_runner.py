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
import subprocess
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple, Optional, Union
import mpmath

import math_core
import transforms
import converter
import zero_finder
import reference_data


RESEARCH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "research")
EXPERIMENTS_DIR = os.path.join(RESEARCH_DIR, "experiments")
RUNS_DIR = os.path.join(RESEARCH_DIR, "runs")
INDEX_FILE = os.path.join(RESEARCH_DIR, "index.json")


def hash_file_bytes(filepath: str) -> str:
    """Compute SHA-256 hash of a file."""
    if not os.path.exists(filepath):
        return "N/A"
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


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
            # Match status: code followed by file path
            parts = line_str.split(None, 1)
            if len(parts) < 2:
                dirty_lines.append(line_str)
                continue
            path = parts[1].strip().strip('"').replace("\\", "/")
            # Ignore runner's own output artifacts
            if path == "research/index.json" or path.startswith("research/runs/"):
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
        "coupled_perturbation_covariance"
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
            # Guard against floating comparison issues with high-precision tolerance
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
        point_dict = {name: str(val) for name, val in zip(param_names, combination)}
        grid.append(point_dict)
        
    return grid


# ==============================================================================
# CANONICAL ENGINE DISPATCH (Strictly delegates to canonical math modules)
# ==============================================================================

def evaluate_point(
    operation: str,
    inputs: Dict[str, str],
    dps: int = 80,
    param_space: Optional[Dict[str, Any]] = None
) -> Tuple[str, Dict[str, str], Optional[str]]:
    """
    Evaluate a single parameter space point using the canonical math engine.
    Returns (status, outputs_dict, error_message).
    All outputs serialize as exact decimal strings.
    """
    with mpmath.workdps(dps + 15):
        try:
            if operation == "centrifuge":
                delta_str = inputs.get("delta", "0.0")
                gamma_str = inputs.get("gamma", "14.13472514173469379045725198356247027078425711569924317568556746")
                k_str = inputs.get("K", inputs.get("k", "0.0"))
                
                log_mod = math_core.centrifuge_log_modulus(delta_str, k_str, dps=dps)
                q_k = math_core.centrifuge_q_k(delta_str, gamma_str, k_str, dps=dps)
                abs_q_k = abs(q_k)
                
                # Theoretical line: K * delta * ln(tau)
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
                # Kernel Lab transformation
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
                # Mode-dependent zero map check
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
                    
                rho = mpmath.mpc('0.5', str(gamma_str))
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
                
                # Mapped coordinate: s' = A * s
                mapped_s = scale_A * s_mpc
                
                # Baseline value: W = zeta(s)
                W = math_core.zeta_eval(s_mpc, dps=dps + 10)
                
                # Transformed coordinate representation evaluated AT MAPPED POINT:
                # W_A = Z_A(s') = zeta(s' / A)
                t_orig = transforms.OriginCoordinateDilation(k=k_str)
                W_A = t_orig.evaluate_function(mapped_s, dps=dps + 10)
                
                # Covariance residual: E_zeta = |W_A - W|
                E_zeta = abs(W_A - W)
                
                sigma_c = mpmath.mpf('0.5')
                sigma_c_prime = scale_A / 2
                
                outputs = {
                    "s_re": mpmath.nstr(s_mpc.real, n=dps),
                    "s_im": mpmath.nstr(s_mpc.imag, n=dps),
                    "k": str(k_str),
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
                
                # Single-zero converter covariance check if x or rho/gamma are provided
                if "x" in inputs or "rho" in inputs or "gamma" in inputs or "rho_im" in inputs:
                    x_str = inputs.get("x", "10.0")
                    x_mpf = math_core.to_mpf(x_str, dps=dps + 10)
                    rho_re = inputs.get("rho_re", "0.5")
                    rho_im = inputs.get("rho_im", inputs.get("gamma", inputs.get("rho", "14.13472514173469379045725198356247027078425711569924317568556746")))
                    rho_mpc = math_core.to_mpc((rho_re, rho_im), dps=dps + 10)
                    
                    # Coupled transformation: rho' = A * rho, x' = x^(1/A)
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
                    
                    # Evaluate C_pi if mapped_x >= 2 and mapped_x <= 1e5 (prevent astronomical Mobius truncation counts)
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
                
                # Compute isolated single-zero / split contributions
                contrib_dict = converter.compute_perturbed_contributions_audit(
                    x_str, rho_clean, delta_str, mode=mode, dps=dps + 15
                )
                
                # Build clean baseline zeros list up to num_zeros
                clean_zeros_mpc = [mpmath.mpc('0.5', g) for g in ref_zeros_str[:num_zeros]]
                pert_rhos = contrib_dict["perturbed_rhos"]
                
                if mode in ("symmetry_complete_split", "symmetry_complete_quartet"):
                    # Baseline contains two coincident copies of rho_clean for split mode
                    clean_for_recon = clean_zeros_mpc[:zero_idx] + [rho_clean, rho_clean] + clean_zeros_mpc[zero_idx + 1:]
                    modified_zeros_mpc = clean_zeros_mpc[:zero_idx] + pert_rhos + clean_zeros_mpc[zero_idx + 1:]
                else:
                    clean_for_recon = clean_zeros_mpc
                    modified_zeros_mpc = list(clean_zeros_mpc)
                    if 0 <= zero_idx < len(modified_zeros_mpc):
                        modified_zeros_mpc = clean_zeros_mpc[:zero_idx] + pert_rhos + clean_zeros_mpc[zero_idx + 1:]
                
                # Compute full explicit formula reconstructions
                full_clean_pi = converter.riemann_explicit_pi_audit(x_str, clean_for_recon, dps=dps + 15)
                full_pert_pi = converter.riemann_explicit_pi_audit(x_str, modified_zeros_mpc, dps=dps + 15)
                full_diff = full_pert_pi - full_clean_pi
                
                # True prime pi(x)
                x_mpf = math_core.to_mpf(x_str, dps=dps + 15)
                try:
                    true_pi_val = reference_data.prime_pi(float(x_mpf)) if x_mpf <= 100000 else "N/A"
                except Exception:
                    true_pi_val = "N/A"
                    
                pert_rhos_str = "; ".join(f"{mpmath.nstr(r.real, n=dps)} + {mpmath.nstr(r.imag, n=dps)}j" for r in pert_rhos)
                d_mpf = math_core.to_mpf(delta_str, dps=dps + 15)

                outputs: Dict[str, str] = {
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
                    
                    # Evaluate symmetry error S(delta) - S(-delta)
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

                    # Quadratic scaling diagnostics
                    if abs(d_mpf) > mpmath.mpf('1e-50'):
                        d_sq = d_mpf * d_mpf
                        norm_quad_cj = split_defect_cj / d_sq
                        norm_quad_cpi = split_defect_cpi / d_sq
                        outputs["normalized_quadratic_cj"] = mpmath.nstr(norm_quad_cj, n=dps)
                        outputs["normalized_quadratic_cpi"] = mpmath.nstr(norm_quad_cpi, n=dps)

                        # Pairwise ratio where half-delta exists
                        declared_deltas_raw = None
                        if param_space and "delta" in param_space:
                            declared_deltas_raw = expand_parameter(param_space["delta"], dps=dps)
                        elif "declared_deltas" in inputs:
                            declared_deltas_raw = inputs["declared_deltas"]

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
                    # single_pair_diagnostic
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
                
                # Unperturbed clean converter wave covariance
                clean_cj = converter.zero_j_contribution_audit(x_mpf, rho_clean, dps=dps + 15)
                clean_cj_prime = converter.zero_j_contribution_audit(x_prime, rho_clean_prime, dps=dps + 15)
                clean_cj_residual = abs(clean_cj_prime - clean_cj)
                
                # Perturbed converter wave covariance
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
                    # single_pair_diagnostic
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
            obs = mpmath.mpf(str(observed_str).strip())
            thresh = mpmath.mpf(str(threshold_str).strip())
            
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
        
        # Sort points descending by absolute value for worst points
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
        # Collect all declared report metrics
        metric_declarations = []
        seen_metric_names = set()
        
        # Primary criterion metric is always tracked
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
                # Check every point
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
            criterion_met = None
            min_observed = "N/A"
            max_observed = "N/A"
            
        criterion_dict = {
            "metric": target_metric,
            "aggregation": aggregation,
            "operator": operator if aggregation != "none" else "N/A",
            "threshold": threshold_str if aggregation != "none" else "N/A",
            "observed": observed_metric_str,
            "criterion_met": criterion_met if status == "complete" else None
        }
        
        summary = {
            "schema_version": "1",
            "run_id": run_id,
            "experiment_id": spec["id"],
            "status": status,
            "hypothesis": spec["hypothesis"]["statement"],
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
            "anomalies": [],
            "warnings": []
        }
        
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

    return f"""# Experiment Run Digest — {spec.get('title', spec['id'])}

**Run ID:** `{manifest['run_id']}`  
**Experiment ID:** `{spec['id']}`  
**Status:** `{summary['status'].upper()}`  
**Criterion Outcome:** **{crit_status}**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**  
  > {summary['hypothesis'].strip()}

{crit_summary_line}

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
{metrics_table}

---

## 3. Metric Diagnostics & Worst Points

{details_block}

---

## 4. Execution & Environment Metadata

- **Git Commit:** `{manifest['git_commit']}` (Dirty: `{manifest['git_dirty']}`)
- **Precision:** `{manifest['precision']['dps']} dps`
- **Tau Value:** `{manifest['tau'][:24]}...`
- **Points Requested:** `{manifest['points_requested']}`
- **Points Completed:** `{manifest['points_completed']}`
- **Started At:** `{manifest['started_at']}`
- **Completed At:** `{manifest['completed_at']}`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
"""


def update_index_file(run_entry: Dict[str, Any]):
    """Update research/index.json with the given canonical run entry (one per experiment_id)."""
    os.makedirs(RESEARCH_DIR, exist_ok=True)
    entries = []
    if os.path.exists(INDEX_FILE):
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                entries = json.load(f)
                if not isinstance(entries, list):
                    entries = []
        except Exception:
            entries = []
            
    # Update existing entry by experiment_id or run_id, or append
    found = False
    for i, e in enumerate(entries):
        if e.get("experiment_id") == run_entry.get("experiment_id") or e.get("run_id") == run_entry.get("run_id"):
            entries[i] = run_entry
            found = True
            break
    if not found:
        entries.append(run_entry)
        
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


# ==============================================================================
# MAIN EXPERIMENT RUNNER ENGINE
# ==============================================================================

def run_experiment(
    spec_path: str,
    resume_run_id: Optional[str] = None
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
    
    # Expand parameter grid
    grid = generate_parameter_grid(spec["parameters"], dps=dps)
    total_points = len(grid)
    
    # Determine run identity
    if resume_run_id:
        run_id = resume_run_id
        run_dir = os.path.join(RUNS_DIR, run_id)
        if not os.path.exists(run_dir):
            raise FileNotFoundError(f"Cannot resume: Run directory '{run_dir}' does not exist")
            
        manifest_path = os.path.join(run_dir, "manifest.json")
        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Cannot resume: Missing '{manifest_path}'")
            
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            
        # Verify compatibility for resume
        if manifest.get("experiment_spec_sha256") != spec_sha:
            raise ValueError(
                f"Refusing resume: Spec hash mismatch! (Recorded: {manifest.get('experiment_spec_sha256')}, Current: {spec_sha})"
            )
    else:
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        short_hash = spec_sha[:8]
        run_id = f"{timestamp_str}_{spec['id']}_{short_hash}"
        run_dir = os.path.join(RUNS_DIR, run_id)
        os.makedirs(run_dir, exist_ok=True)
        
        # Source module hashes
        code_root = os.path.dirname(os.path.abspath(__file__))
        code_modules = {
            "math_core.py": hash_file_bytes(os.path.join(code_root, "math_core.py")),
            "transforms.py": hash_file_bytes(os.path.join(code_root, "transforms.py")),
            "converter.py": hash_file_bytes(os.path.join(code_root, "converter.py")),
            "zero_finder.py": hash_file_bytes(os.path.join(code_root, "zero_finder.py"))
        }
        
        manifest = {
            "schema_version": "1",
            "run_id": run_id,
            "experiment_id": spec["id"],
            "experiment_spec_sha256": spec_sha,
            "git_commit": git_commit,
            "git_dirty": git_dirty,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": None,
            "status": "running",
            "precision": {"dps": dps},
            "parameter_space": spec["parameters"],
            "points_requested": total_points,
            "points_completed": 0,
            "tau": tau_str,
            "runtime": {
                "python": sys.version,
                "platform": sys.platform,
                "packages": {
                    "mpmath": getattr(mpmath, "__version__", "N/A"),
                    "flint": getattr(math_core, "flint_ctx", None) is not None
                }
            },
            "data_provenance": reference_data.load_provenance(),
            "code_modules": code_modules
        }
        
        with open(os.path.join(run_dir, "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

    results_path = os.path.join(run_dir, "results.jsonl")
    
    # Read already completed point IDs if resuming
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

    # Open results.jsonl in append mode with immediate flushing
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
            
    # Mark completion
    completed_points = len(all_results)
    final_status = "complete" if completed_points == total_points else "incomplete"
    
    manifest["status"] = final_status
    manifest["points_completed"] = completed_points
    manifest["completed_at"] = datetime.now(timezone.utc).isoformat()
    
    with open(os.path.join(run_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    summary = compute_summary(spec, run_id, all_results, status=final_status)
    with open(os.path.join(run_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    readme_content = generate_run_readme(spec, manifest, summary)
    with open(os.path.join(run_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
        
    # Update index
    run_entry: Dict[str, Any] = {
        "run_id": run_id,
        "experiment_id": spec["id"],
        "classification": spec.get("classification", "canonical_experiment"),
        "timestamp": manifest["started_at"],
        "git_commit": git_commit,
        "status": final_status,
        "criterion_met": summary["criterion"].get("criterion_met"),
        "summary_path": f"research/runs/{run_id}/summary.json",
        "manifest_path": f"research/runs/{run_id}/manifest.json",
        "results_path": f"research/runs/{run_id}/results.jsonl"
    }
    if "notes" in spec:
        run_entry["notes"] = spec["notes"]
    update_index_file(run_entry)
    
    return run_id


def summarize_run(run_id: str) -> Dict[str, Any]:
    """Recompute and return summary for an existing run."""
    run_dir = os.path.join(RUNS_DIR, run_id)
    if not os.path.exists(run_dir):
        raise FileNotFoundError(f"Run directory '{run_dir}' not found")
        
    manifest_path = os.path.join(run_dir, "manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    # Find corresponding experiment spec
    exp_id = manifest["experiment_id"]
    spec_path = os.path.join(EXPERIMENTS_DIR, f"{exp_id}.yaml")
    if not os.path.exists(spec_path):
        # Scan experiments dir
        for fname in os.listdir(EXPERIMENTS_DIR):
            if fname.endswith(".yaml") or fname.endswith(".yml"):
                p = os.path.join(EXPERIMENTS_DIR, fname)
                with open(p, "r", encoding="utf-8") as sf:
                    try:
                        s_data = yaml.safe_load(sf)
                        if s_data.get("id") == exp_id:
                            spec_path = p
                            break
                    except Exception:
                        pass
                        
    if not os.path.exists(spec_path):
        raise FileNotFoundError(f"Spec for experiment '{exp_id}' not found in {EXPERIMENTS_DIR}")
        
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)
        
    results_path = os.path.join(run_dir, "results.jsonl")
    results = []
    if os.path.exists(results_path):
        with open(results_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    results.append(json.loads(line))
                    
    status = "complete" if len(results) >= manifest.get("points_requested", 0) else "incomplete"
    summary = compute_summary(spec, run_id, results, status=status)
    
    with open(os.path.join(run_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    return summary


def list_runs() -> List[Dict[str, Any]]:
    """List all recorded runs in research/index.json."""
    if not os.path.exists(INDEX_FILE):
        return []
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ==============================================================================
# CLI INTERFACE
# ==============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python research_runner.py [run <spec.yaml> [--resume <run_id>] | summarize <run_id> | list]")
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
        
        # Print summary digest
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
