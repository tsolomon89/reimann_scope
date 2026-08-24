"""
research/handlers/kernel_lock.py — Inverse Kernel Lock Identity Handler
"""

from __future__ import annotations
from typing import Dict, Any, Tuple, Optional, List
import mpmath

import math_core
import transforms
from research.handlers.base import ExperimentHandler, HandlerDependencies


class InverseKernelLockHandler(ExperimentHandler):
    @property
    def experiment_id(self) -> str:
        return "inverse-kernel-lock-identity"

    @property
    def declared_dependencies(self) -> HandlerDependencies:
        return HandlerDependencies(
            common_modules=["research_runner.py", "research/handlers/base.py"],
            handler_modules=["research/handlers/kernel_lock.py"],
            math_modules=["math_core.py", "transforms.py"],
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
