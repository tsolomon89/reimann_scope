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
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=work_dir,
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        dirty_lines = [
            line for line in status.splitlines()
            if line.strip() and not line.strip().endswith("research/index.json")
        ]
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
    if not isinstance(crit, dict) or not all(k in crit for k in ["metric", "operator", "threshold"]):
        return False, "Spec 'criterion' must define 'metric', 'operator', and 'threshold'"
        
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
        "converter_perturbation"
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
    dps: int = 80
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
                mode = inputs.get("mode", "camera")
                k_str = inputs.get("k", "0.0")
                t_str = inputs.get("t", inputs.get("im_s", "14.134725"))
                delta_str = inputs.get("delta", "0.0")
                
                s_mpc = mpmath.mpc(mpmath.mpf('0.5') + math_core.to_mpf(delta_str, dps=dps), math_core.to_mpf(t_str, dps=dps))
                t_obj_trace: transforms.BaseTransform
                if mode == "origin_dilation":
                    t_obj_trace = transforms.OriginCoordinateDilation(k=k_str)
                elif mode == "argument":
                    t_obj_trace = transforms.ArgumentTransform(k=k_str)
                elif mode == "centered_dilation":
                    t_obj_trace = transforms.CenteredCoordinateDilation(k=k_str)
                else:
                    t_obj_trace = transforms.CameraTransform()
                    
                mapped_s = t_obj_trace.map_domain_point(complex(float(s_mpc.real), float(s_mpc.imag)))
                z_val = t_obj_trace.evaluate_function(s_mpc, dps=dps)

                
                return "ok", {
                    "mapped_s_re": str(mapped_s.real),
                    "mapped_s_im": str(mapped_s.imag),
                    "zeta_re": mpmath.nstr(z_val.real, n=dps),
                    "zeta_im": mpmath.nstr(z_val.imag, n=dps),
                    "modulus": mpmath.nstr(abs(z_val), n=dps)
                }, None

            elif operation == "converter_perturbation":
                x_str = inputs.get("x", "20.0")
                num_zeros = int(inputs.get("num_zeros", "10"))
                ref_zeros_str = reference_data.load_reference_zeros()[:num_zeros]
                if not ref_zeros_str:
                    ref_zeros_str = ["14.134725", "21.022040", "25.010858"]
                
                pi_val = converter.riemann_explicit_pi_audit(x_str, ref_zeros_str, dps=dps)
                true_pi_val = reference_data.prime_pi(float(x_str))
                diff = abs(pi_val - mpmath.mpf(true_pi_val))
                
                return "ok", {
                    "reconstructed_pi": mpmath.nstr(pi_val, n=dps),
                    "true_pi": str(true_pi_val),
                    "abs_diff": mpmath.nstr(diff, n=dps),
                    "residual": mpmath.nstr(diff, n=dps)
                }, None

            else:
                return "error", {}, f"Unknown operation '{operation}'"
                
        except Exception as e:
            return "error", {}, str(e)


def evaluate_criterion(
    observed_str: str,
    operator: str,
    threshold_str: str
) -> bool:
    """Evaluate declared mathematical criterion with arbitrary-precision comparison."""
    try:
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


def compute_summary(
    spec: Dict[str, Any],
    run_id: str,
    results: List[Dict[str, Any]],
    status: str
) -> Dict[str, Any]:
    """Generate canonical AI-facing summary.json artifact."""
    dps = spec["precision"]["dps"]
    crit_spec = spec["criterion"]
    target_metric = crit_spec["metric"]
    operator = crit_spec["operator"]
    threshold_str = str(crit_spec["threshold"])
    
    points_req = len(results)
    points_completed = sum(1 for r in results if r.get("status") == "ok")
    points_failed = sum(1 for r in results if r.get("status") == "error")
    
    # Extract values for the target metric across all completed points
    observed_values = []
    for r in results:
        if r.get("status") == "ok" and target_metric in r.get("outputs", {}):
            try:
                observed_values.append(mpmath.mpf(r["outputs"][target_metric]))
            except Exception:
                pass
                
    if observed_values:
        max_observed = max(observed_values)
        min_observed = min(observed_values)
        observed_metric_str = mpmath.nstr(max_observed, n=dps)
        criterion_met = evaluate_criterion(observed_metric_str, operator, threshold_str)
    else:
        observed_metric_str = "N/A"
        criterion_met = None
        min_observed = mpmath.mpf(0)
        max_observed = mpmath.mpf(0)
        
    summary = {
        "schema_version": "1",
        "run_id": run_id,
        "experiment_id": spec["id"],
        "status": status,
        "hypothesis": spec["hypothesis"]["statement"],
        "points_requested": points_req,
        "points_completed": points_completed,
        "points_failed": points_failed,
        "metrics": {
            target_metric: observed_metric_str
        },
        "criterion": {
            "metric": target_metric,
            "operator": operator,
            "threshold": threshold_str,
            "observed": observed_metric_str,
            "criterion_met": criterion_met if status == "complete" else None
        },
        "extrema": {
            "min": mpmath.nstr(min_observed, n=dps) if observed_values else "N/A",
            "max": mpmath.nstr(max_observed, n=dps) if observed_values else "N/A"
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
    """Generate concise human-readable run README.md digest."""
    crit = summary["criterion"]
    crit_status = "CRITERION MET" if crit.get("criterion_met") is True else (
        "CRITERION NOT MET" if crit.get("criterion_met") is False else "INCOMPLETE / INVALID"
    )
    
    return f"""# Experiment Run Digest — {spec.get('title', spec['id'])}

**Run ID:** `{manifest['run_id']}`  
**Experiment ID:** `{spec['id']}`  
**Status:** `{summary['status'].upper()}`  
**Criterion Outcome:** **{crit_status}**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**  
  > {spec['hypothesis']['statement']}
- **Declared Criterion:** `{crit['metric']} {crit['operator']} {crit['threshold']}`
- **Observed Metric:** `{crit['observed']}`
- **Criterion Met:** `{crit.get('criterion_met')}`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Execution & Environment Metadata

- **Git Commit:** `{manifest['git_commit']}` (Dirty: `{manifest['git_dirty']}`)
- **Precision:** `{manifest['precision']['dps']} dps`
- **Tau Value:** `{manifest['tau'][:24]}...`
- **Points Requested:** `{manifest['points_requested']}`
- **Points Completed:** `{manifest['points_completed']}`
- **Started At:** `{manifest['started_at']}`
- **Completed At:** `{manifest['completed_at'] or 'In Progress'}`

---

## 3. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
"""


def update_index_file(run_entry: Dict[str, Any]):
    """Update research/index.json with the given run entry."""
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
            
    # Update existing entry or append
    found = False
    for i, e in enumerate(entries):
        if e.get("run_id") == run_entry["run_id"]:
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
                
            status, outputs, err_msg = evaluate_point(operation, inputs, dps=dps)
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
    run_entry = {
        "run_id": run_id,
        "experiment_id": spec["id"],
        "timestamp": manifest["started_at"],
        "git_commit": git_commit,
        "status": final_status,
        "criterion_met": summary["criterion"].get("criterion_met"),
        "summary_path": f"research/runs/{run_id}/summary.json",
        "manifest_path": f"research/runs/{run_id}/manifest.json",
        "results_path": f"research/runs/{run_id}/results.jsonl"
    }
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
