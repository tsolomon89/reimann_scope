"""
research/handlers/grade_constraints.py — Grade Constraints Handler
"""

from __future__ import annotations
from typing import Dict, Any, Tuple, Optional, List
import mpmath

import math_core
from research.handlers.base import ExperimentHandler, HandlerDependencies


class GradeConstraintsHandler(ExperimentHandler):
    @property
    def experiment_id(self) -> str:
        return "grade-constraints-001"

    @property
    def declared_dependencies(self) -> HandlerDependencies:
        return HandlerDependencies(
            common_modules=["research_runner.py", "research/handlers/base.py"],
            handler_modules=["research/handlers/grade_constraints.py"],
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
