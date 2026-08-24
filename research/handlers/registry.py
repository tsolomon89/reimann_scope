"""
research/handlers/registry.py — Authoritative Experiment Handler Registry

Maintains the deterministic mapping from experiment IDs to concrete ExperimentHandler instances.
Provides fail-closed resolution and interface validation for all 17 canonical experiments.
"""

from __future__ import annotations
from typing import Dict, Any, List, Tuple, Optional, Type
import os
import glob
import yaml

from research.handlers.base import ExperimentHandler


_HANDLERS: Dict[str, ExperimentHandler] = {}


def register_handler(handler: ExperimentHandler) -> None:
    """Register an experiment handler instance in the global registry."""
    exp_id = handler.experiment_id
    if not exp_id:
        raise ValueError("Handler must define a non-empty experiment_id")
    if exp_id in _HANDLERS:
        raise ValueError(f"Duplicate experiment handler registered for '{exp_id}'")
    _HANDLERS[exp_id] = handler


def get_handler(exp_id: str) -> ExperimentHandler:
    """Retrieve the registered handler for an experiment ID. Fails closed if unknown."""
    if exp_id not in _HANDLERS:
        # Trigger lazy load of all built-in handlers if registry is empty
        _ensure_handlers_loaded()
    if exp_id not in _HANDLERS:
        known = sorted(list(_HANDLERS.keys()))
        raise KeyError(f"No experiment handler registered for '{exp_id}'. Known handlers: {known}")
    return _HANDLERS[exp_id]


def list_registered_handlers() -> List[str]:
    """Return sorted list of all registered experiment IDs."""
    _ensure_handlers_loaded()
    return sorted(list(_HANDLERS.keys()))


def clear_registry() -> None:
    """Clear registered handlers (useful for testing)."""
    _HANDLERS.clear()


def _ensure_handlers_loaded() -> None:
    """Import and register all built-in concrete experiment handlers."""
    if _HANDLERS:
        return
    from research.handlers.dilation import CenteredDilationZeroMapHandler
    from research.handlers.centrifuge import CentrifugeSlopeHandler, SymmetricCentrifugeDefectHandler
    from research.handlers.covariance import (
        CoupledPerturbationCovarianceHandler,
        CoupledScaleCovarianceHandler,
    )
    from research.handlers.cross_height import (
        CrossHeightDistanceHandler,
        CrossHeightPathCoherenceHandler,
    )
    from research.handlers.explicit_formula import (
        ExplicitFormulaGradeCovarianceHandler,
        ExplicitFormulaNativeBaselineHandler,
        ExplicitFormulaPerturbationRankHandler,
        ExplicitFormulaRadialSecondVariationHandler,
    )
    from research.handlers.grade_constraints import GradeConstraintsHandler
    from research.handlers.kernel_lock import InverseKernelLockHandler
    from research.handlers.converter_perturbation import IsolatedRadialResponseHandler
    from research.handlers.worldlines import (
        SyntheticRadialLeavesHandler,
        TranscendentalWorldlinesHandler,
        TrivialWorldlinesHandler,
    )

    handlers = [
        CenteredDilationZeroMapHandler(),
        CentrifugeSlopeHandler(),
        SymmetricCentrifugeDefectHandler(),
        CoupledPerturbationCovarianceHandler(),
        CoupledScaleCovarianceHandler(),
        CrossHeightDistanceHandler(),
        CrossHeightPathCoherenceHandler(),
        ExplicitFormulaGradeCovarianceHandler(),
        ExplicitFormulaNativeBaselineHandler(),
        ExplicitFormulaPerturbationRankHandler(),
        ExplicitFormulaRadialSecondVariationHandler(),
        GradeConstraintsHandler(),
        InverseKernelLockHandler(),
        IsolatedRadialResponseHandler(),
        SyntheticRadialLeavesHandler(),
        TranscendentalWorldlinesHandler(),
        TrivialWorldlinesHandler(),
    ]
    for h in handlers:
        register_handler(h)
