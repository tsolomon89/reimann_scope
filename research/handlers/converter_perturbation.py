"""
research/handlers/converter_perturbation.py — Isolated Radial Response Experiment Handler
"""

from __future__ import annotations
from typing import Dict, Any, Tuple, Optional, List
import mpmath

import math_core
import converter
import reference_data
from research.handlers.base import ExperimentHandler, HandlerDependencies


class IsolatedRadialResponseHandler(ExperimentHandler):
    @property
    def experiment_id(self) -> str:
        return "isolated-radial-response-002"

    @property
    def declared_dependencies(self) -> HandlerDependencies:
        return HandlerDependencies(
            common_modules=["research_runner.py", "research/handlers/base.py"],
            handler_modules=["research/handlers/converter_perturbation.py"],
            math_modules=["math_core.py", "converter.py", "reference_data.py"],
            data_files=["data/zeros_reference.json", "data/primes.json"],
            consumed_certificates=[],
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
                    import research_runner
                    declared_deltas_raw = research_runner.expand_parameter(param_space["delta"], dps=dps)
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
