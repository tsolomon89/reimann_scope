"""
research/handlers/dilation.py — Centered Dilation Zero Map Handler
"""

from __future__ import annotations
from typing import Dict, Any, Tuple, Optional, List
import mpmath

import transforms
from research.handlers.base import ExperimentHandler, HandlerDependencies


class CenteredDilationZeroMapHandler(ExperimentHandler):
    @property
    def experiment_id(self) -> str:
        return "centered-dilation-zero-map"

    @property
    def declared_dependencies(self) -> HandlerDependencies:
        return HandlerDependencies(
            common_modules=["research_runner.py", "research/handlers/base.py"],
            handler_modules=["research/handlers/dilation.py"],
            math_modules=["transforms.py", "math_core.py"],
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
