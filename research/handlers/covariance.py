"""
research/handlers/covariance.py — Coupled Scale & Perturbation Covariance Handlers
"""

from __future__ import annotations
from typing import Dict, Any, Tuple, Optional, List
import mpmath

import math_core
import transforms
import converter
import reference_data
from research.handlers.base import ExperimentHandler, HandlerDependencies


class CoupledScaleCovarianceHandler(ExperimentHandler):
    @property
    def experiment_id(self) -> str:
        return "coupled-scale-covariance-001"

    @property
    def declared_dependencies(self) -> HandlerDependencies:
        return HandlerDependencies(
            common_modules=["research_runner.py", "research/handlers/base.py"],
            handler_modules=["research/handlers/covariance.py"],
            math_modules=["math_core.py", "transforms.py", "converter.py"],
            data_files=[],
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


class CoupledPerturbationCovarianceHandler(ExperimentHandler):
    @property
    def experiment_id(self) -> str:
        return "coupled-perturbation-covariance-001"

    @property
    def declared_dependencies(self) -> HandlerDependencies:
        return HandlerDependencies(
            common_modules=["research_runner.py", "research/handlers/base.py"],
            handler_modules=["research/handlers/covariance.py"],
            math_modules=["math_core.py", "converter.py", "reference_data.py"],
            data_files=["data/zeros_reference.json"],
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
