"""
research/handlers/base.py — Authoritative Experiment Handler Base Contract

Defines the abstract interface for all mathematical experiment handlers.
Every experiment in research/experiments/ is bound to exactly one handler.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Optional, Set
import os
import hashlib


@dataclass
class HandlerDependencies:
    """Explicitly declared file and package dependencies for an experiment handler."""
    common_modules: List[str] = field(default_factory=lambda: ["research_runner.py", "research/handlers/base.py"])
    handler_modules: List[str] = field(default_factory=list)
    math_modules: List[str] = field(default_factory=list)
    data_files: List[str] = field(default_factory=list)
    consumed_certificates: List[str] = field(default_factory=list)
    material_packages: List[str] = field(default_factory=lambda: ["mpmath", "flint"])

    @property
    def all_source_files(self) -> List[str]:
        """Return all distinct source code files this handler depends on."""
        seen = set()
        out = []
        for f in self.common_modules + self.handler_modules + self.math_modules:
            norm = f.replace("\\", "/")
            if norm not in seen:
                seen.add(norm)
                out.append(norm)
        return sorted(out)

    @property
    def all_data_files(self) -> List[str]:
        """Return all distinct input data files this handler depends on."""
        seen = set()
        out = []
        for f in self.data_files:
            norm = f.replace("\\", "/")
            if norm not in seen:
                seen.add(norm)
                out.append(norm)
        return sorted(out)


class ExperimentHandler(ABC):
    """Abstract contract for an experiment evaluation, validation, and summary handler."""

    @property
    @abstractmethod
    def experiment_id(self) -> str:
        """The authoritative experiment identifier (matches YAML spec id)."""
        pass

    @property
    @abstractmethod
    def declared_dependencies(self) -> HandlerDependencies:
        """Explicitly declared file and library dependencies for this handler."""
        pass

    def validate_spec(self, spec: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate experiment-specific specification fields beyond standard schema."""
        errors: List[str] = []
        if spec.get("id") != self.experiment_id and spec.get("experiment_id") != self.experiment_id:
            errors.append(f"Spec ID mismatch: expected '{self.experiment_id}', got '{spec.get('id')}'")
        return len(errors) == 0, errors

    @abstractmethod
    def evaluate_point(
        self,
        inputs: Dict[str, str],
        dps: int = 80,
        param_space: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Dict[str, str], Optional[str]]:
        """Evaluate a single parameter space point.

        Returns (status, outputs_dict, error_message).
        All values in outputs_dict must serialize as exact decimal strings or boolean strings.
        """
        pass

    def compute_summary(
        self,
        results: List[Dict[str, Any]],
        spec: Dict[str, Any],
        manifest: Dict[str, Any],
        status: str = "complete"
    ) -> Dict[str, Any]:
        """Compute experiment-specific summary metrics and classifications from raw results.

        Default implementation returns empty dict. Handlers override with experiment-specific summary tables.
        """
        return {}

    def generate_diagnostics(
        self,
        results: List[Dict[str, Any]],
        spec: Dict[str, Any],
        run_dir: str
    ) -> Optional[Dict[str, Any]]:
        """Generate optional structured diagnostics (e.g. diagnostics.json).

        Returns diagnostic dict if generated, or None if not applicable.
        """
        return None
