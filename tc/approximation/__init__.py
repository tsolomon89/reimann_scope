"""
Transcendental Continuation: Arithmetic Stations, Continuum Profiles, and Approximation Campaigns.

Modular package structure:
- .stations: Prime sieving, canonical window weights, bump functions, manifest validation
- .continuum: Continuum limit profiles, mollified profiles, actual TC grade basis, experiments
- .campaigns: Trend classification, negative grade campaigns, adaptive search, principal angles
- .bounds: Tail bounds (Stieltjes, quadratic spectral), resonance audits, milestone verification
"""
from __future__ import annotations

import cmath
import fractions
import functools
import glob
import hashlib
import json
import math
import os
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union, TYPE_CHECKING

import mpmath

if TYPE_CHECKING:
    import numpy as np
    import flint
    from flint import acb, arb, ctx
    FLINT_AVAILABLE = True
    NUMPY_AVAILABLE = True
else:
    try:
        import flint
        from flint import acb, arb, ctx
        FLINT_AVAILABLE = True
    except ImportError:
        flint = None
        acb = None
        arb = None
        ctx = None
        FLINT_AVAILABLE = False

    try:
        import numpy as np
        NUMPY_AVAILABLE = True
    except ImportError:
        np = None
        NUMPY_AVAILABLE = False

import math_core

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from tc.weil_forms import (
    verify_canonical_reflected_weil_sign_certificate,
    ArchimedeanKernelEvaluator,
    kappa_hat_fast,
    Z_CANONICAL_KERNEL,
    NORM_KAPPA_SQ,
    NORM_KAPPA_FIRST_DERIVATIVE_SQ,
    NORM_KAPPA_SECOND_DERIVATIVE_SQ,
    NORM_KAPPA_THIRD_DERIVATIVE_SQ,
    sieve_prime_powers_in_window,
)

# 1. Stations & geometry
from .stations import (
    audit_coefficient_rescaling_homogeneity,
    compute_support_components,
    audit_canonical_support_geometry_and_resonance,
    poincare_support_lower_bound,
    analyze_negative_grade_station_growth,
    sieve_primes_up_to,
    canonical_window_weight,
    canonical_window_weight_deriv,
    generate_actual_tc_stations,
    validate_tc_station_manifest,
    phi_smooth_standard,
    phi_pp_standard,
    psi_bump_canonical,
    psi_bump_deriv_canonical,
)

# 2. Continuum profiles & experiments
from .continuum import (
    evaluate_v_w_profile,
    evaluate_continuum_limit_profile_F_infty_0,
    evaluate_continuum_mollified_profile_F_infty_h,
    evaluate_continuum_mollified_profile_F_infty_h_direct_psi,
    evaluate_actual_tc_grade_basis,
    compute_arithmetic_vs_smoothing_error,
    evaluate_smooth_independent_target,
    construct_actual_tc_approximation_experiment,
    analyze_fourier_zero_compact_support_obstruction,
    investigate_varying_configurations_and_shared_grades,
    construct_admissible_target_and_approximation_experiment,
    audit_weil_continuity_and_connes_consani_bridge,
    audit_tc_epic_support_geometry_synthesis,
)

# 3. Campaigns & searches
from .campaigns import (
    classify_finite_series_trend,
    _is_finite_vanishing_integral,
    run_tc_negative_grade_approximation_campaign,
    search_adaptive_diagonal_schedule,
    _validate_candidate_error_record,
    execute_adaptive_diagonal_search,
    compute_function_subspace_principal_angles,
    investigate_actual_tc_grade_cancellation,
)

# 4. Tail bounds & milestones
from .bounds import (
    audit_same_grade_resonance_K_neg3,
    audit_arithmetic_spectral_exact_formula,
    run_tc_grade_cancellation_research_campaign,
    derive_explicit_stieltjes_nontrivial_zero_tail_bound,
    derive_stieltjes_nontrivial_zero_tail_bound,
    derive_quadratic_spectral_tail_bound,
    verify_research_milestone_completion,
)

__all__ = [
    "Any",
    "ArchimedeanKernelEvaluator",
    "Dict",
    "FLINT_AVAILABLE",
    "List",
    "NORM_KAPPA_FIRST_DERIVATIVE_SQ",
    "NORM_KAPPA_SECOND_DERIVATIVE_SQ",
    "NORM_KAPPA_SQ",
    "NORM_KAPPA_THIRD_DERIVATIVE_SQ",
    "NUMPY_AVAILABLE",
    "Optional",
    "REPO_ROOT",
    "Sequence",
    "TYPE_CHECKING",
    "Tuple",
    "Union",
    "Z_CANONICAL_KERNEL",
    "_is_finite_vanishing_integral",
    "_validate_candidate_error_record",
    "acb",
    "analyze_fourier_zero_compact_support_obstruction",
    "analyze_negative_grade_station_growth",
    "arb",
    "audit_arithmetic_spectral_exact_formula",
    "audit_canonical_support_geometry_and_resonance",
    "audit_coefficient_rescaling_homogeneity",
    "audit_same_grade_resonance_K_neg3",
    "audit_tc_epic_support_geometry_synthesis",
    "audit_weil_continuity_and_connes_consani_bridge",
    "canonical_window_weight",
    "canonical_window_weight_deriv",
    "classify_finite_series_trend",
    "cmath",
    "compute_arithmetic_vs_smoothing_error",
    "compute_function_subspace_principal_angles",
    "compute_support_components",
    "construct_actual_tc_approximation_experiment",
    "construct_admissible_target_and_approximation_experiment",
    "ctx",
    "dataclass",
    "derive_explicit_stieltjes_nontrivial_zero_tail_bound",
    "derive_quadratic_spectral_tail_bound",
    "derive_stieltjes_nontrivial_zero_tail_bound",
    "evaluate_actual_tc_grade_basis",
    "evaluate_continuum_limit_profile_F_infty_0",
    "evaluate_continuum_mollified_profile_F_infty_h",
    "evaluate_continuum_mollified_profile_F_infty_h_direct_psi",
    "evaluate_smooth_independent_target",
    "evaluate_v_w_profile",
    "execute_adaptive_diagonal_search",
    "flint",
    "fractions",
    "functools",
    "generate_actual_tc_stations",
    "glob",
    "hashlib",
    "investigate_actual_tc_grade_cancellation",
    "investigate_varying_configurations_and_shared_grades",
    "json",
    "kappa_hat_fast",
    "math",
    "math_core",
    "mpmath",
    "np",
    "os",
    "phi_pp_standard",
    "phi_smooth_standard",
    "poincare_support_lower_bound",
    "psi_bump_canonical",
    "psi_bump_deriv_canonical",
    "re",
    "run_tc_grade_cancellation_research_campaign",
    "run_tc_negative_grade_approximation_campaign",
    "search_adaptive_diagonal_schedule",
    "sieve_prime_powers_in_window",
    "sieve_primes_up_to",
    "sys",
    "validate_tc_station_manifest",
    "verify_canonical_reflected_weil_sign_certificate",
    "verify_research_milestone_completion",
]
