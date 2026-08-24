"""
research/handlers/centrifuge.py — Centrifuge Slope & Symmetric Defect Handlers
"""

from __future__ import annotations
from typing import Dict, Any, Tuple, Optional, List
import mpmath

import math_core
from research.handlers.base import ExperimentHandler, HandlerDependencies


class CentrifugeSlopeHandler(ExperimentHandler):
    @property
    def experiment_id(self) -> str:
        return "centrifuge-slope-verification"

    @property
    def declared_dependencies(self) -> HandlerDependencies:
        return HandlerDependencies(
            common_modules=["research_runner.py", "research/handlers/base.py"],
            handler_modules=["research/handlers/centrifuge.py"],
            math_modules=["math_core.py"],
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


class SymmetricCentrifugeDefectHandler(ExperimentHandler):
    @property
    def experiment_id(self) -> str:
        return "symmetric-centrifuge-defect-001"

    @property
    def declared_dependencies(self) -> HandlerDependencies:
        return HandlerDependencies(
            common_modules=["research_runner.py", "research/handlers/base.py"],
            handler_modules=["research/handlers/centrifuge.py"],
            math_modules=["math_core.py"],
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
