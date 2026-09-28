"""
Transcendental Continuation: Reflected Weil Forms, Archimedean Kernel, and Positivity.

Modular package structure:
- .kernel: Archimedean kernel, GL quadrature, bump Fourier transforms, prime power sieving
- .separation: Logarithmic separation, station-to-grade embeddings, quartet tests, candidate A
- .matrix: Canonical reflected Weil matrix evaluation, candidate B audits, asymptotic scaling
- .positivity: Connes-Consani criterion, surviving prime bounds, local positivity threshold
- .certificates: Sign certificates, error budgets, convolution tables, off-critical sensitivity
- .spectrum: Canonical Weil sweeps, enlarged grade Rayleigh, arithmetic baseline comparison, deflation
- .optimization: Upper objective solver, optimized suppression, observables, bridge investigations
"""
from __future__ import annotations

import bisect
import cmath
import fractions
import functools
import glob
import hashlib
import json
import math
import os
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

# Re-export two_variable functions for backward compatibility
from tc.two_variable import (
    _von_mangoldt_exact,
    _make_smooth_bump,
    audit_tc_cutoff_condition_counterexample,
    evaluate_two_variable_explicit_expansion,
    audit_selected_spectral_contribution,
    audit_two_variable_truncation_bound,
    evaluate_two_variable_finite_decomposition,
    audit_arithmetic_overlap_distinct_and_equal_grades,
    audit_smooth_kernel_indefiniteness_counterexample,
)

# 1. Kernel & quadrature
from .kernel import (
    Z_CANONICAL_KERNEL,
    _N_GL_KAPPA,
    _y_gl_raw,
    _w_gl_raw,
    _y_gl,
    _w_gl,
    _f_gl,
    _i,
    _yk,
    _KAPPA_GL_CACHE,
    _C_TAB_CACHE,
    kappa_hat_fast,
    archimedean_digamma_weight,
    NORM_KAPPA_THIRD_DERIVATIVE_SQ,
    NORM_KAPPA_SECOND_DERIVATIVE_SQ,
    NORM_KAPPA_FIRST_DERIVATIVE_SQ,
    NORM_KAPPA_SQ,
    sieve_prime_powers_in_window,
    _is_prime_power_exact,
    _compute_C_h_position_quad,
    _compute_C_tab_fast,
    ArchimedeanKernelEvaluator,
)

# 2. Separation & early audits
from .separation import (
    audit_station_to_grade_embedding_and_restricted_family,
    audit_reflected_weil_spectral_form,
    audit_compact_support_weil_quartet_test,
    audit_tc_comparison_map_candidate_A,
    audit_tc_logarithmic_separation_and_resonance_gap,
)

# 3. Canonical matrix & Candidate B
from .matrix import (
    compute_canonical_reflected_weil_matrix,
    audit_small_bandwidth_archimedean_asymptotic,
    audit_tc_candidate_B_reflected_weil_kernel,
    audit_tc_comparison_map_candidate_B,
)

# 4. Positivity & Weil bridges
from .positivity import (
    audit_weil_positivity_connes_consani_criterion,
    audit_weil_positivity_and_tc_bridge_comparison,
    audit_arithmetic_quadratic_form_mode_extraction,
    audit_finite_spectral_perturbation_rigidity,
    audit_arithmetic_compatibility_investigation,
    reproduce_cutoff_discrepancy,
    certify_archimedean_tail_psd,
    compute_surviving_prime_bound,
    compute_local_positivity_threshold,
    investigate_conditional_detection_implication,
    audit_weil_continuity_and_approximation_bridge,
)

# 5. Certificates & Error Budgets
from .certificates import (
    generate_canonical_reflected_weil_sign_certificate,
    verify_canonical_reflected_weil_sign_certificate,
    audit_tc_epic_two_variable_synthesis,
    certify_production_convolution_table,
    certify_baseline_canonical_weil_error_budget,
    validate_or_project_legal_b,
    certify_explicit_formula_off_critical_sensitivity,
)

# 6. Spectrum sweeps & Rayleigh spectrum
from .spectrum import (
    evaluate_tc_canonical_weil_spectrum_sweep,
    evaluate_tc_enlarged_grade_space_rayleigh_spectrum,
    evaluate_tc_arithmetic_spectral_baseline_comparison,
    compute_tc_quartet_matrix,
    audit_tc_critical_zero_deflation,
    evaluate_tc_asymptotic_scaling_sweep,
    audit_tc_h1_cutoff_sensitivity_and_enclosure,
)

# 7. Optimization, observables & bridge investigation
from .optimization import (
    validate_spectral_zero_coverage,
    solve_complete_upper_objective,
    evaluate_tc_optimized_suppression_comparison,
    compute_grouped_correlation_system,
    test_spectral_matrix_span_recovery,
    compute_critical_zero_observable,
    compute_reflected_quartet_observable,
    investigate_scalar_spectral_bridge_target_b,
    investigate_admissible_spectral_realization,
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
    "_C_TAB_CACHE",
    "_KAPPA_GL_CACHE",
    "_N_GL_KAPPA",
    "_compute_C_h_position_quad",
    "_compute_C_tab_fast",
    "_f_gl",
    "_i",
    "_is_prime_power_exact",
    "_make_smooth_bump",
    "_von_mangoldt_exact",
    "_w_gl",
    "_w_gl_raw",
    "_y_gl",
    "_y_gl_raw",
    "_yk",
    "acb",
    "arb",
    "archimedean_digamma_weight",
    "audit_arithmetic_compatibility_investigation",
    "audit_arithmetic_overlap_distinct_and_equal_grades",
    "audit_arithmetic_quadratic_form_mode_extraction",
    "audit_compact_support_weil_quartet_test",
    "audit_finite_spectral_perturbation_rigidity",
    "audit_reflected_weil_spectral_form",
    "audit_selected_spectral_contribution",
    "audit_small_bandwidth_archimedean_asymptotic",
    "audit_smooth_kernel_indefiniteness_counterexample",
    "audit_station_to_grade_embedding_and_restricted_family",
    "audit_tc_candidate_B_reflected_weil_kernel",
    "audit_tc_comparison_map_candidate_A",
    "audit_tc_comparison_map_candidate_B",
    "audit_tc_critical_zero_deflation",
    "audit_tc_cutoff_condition_counterexample",
    "audit_tc_epic_two_variable_synthesis",
    "audit_tc_h1_cutoff_sensitivity_and_enclosure",
    "audit_tc_logarithmic_separation_and_resonance_gap",
    "audit_two_variable_truncation_bound",
    "audit_weil_continuity_and_approximation_bridge",
    "audit_weil_positivity_and_tc_bridge_comparison",
    "audit_weil_positivity_connes_consani_criterion",
    "bisect",
    "certify_archimedean_tail_psd",
    "certify_baseline_canonical_weil_error_budget",
    "certify_explicit_formula_off_critical_sensitivity",
    "certify_production_convolution_table",
    "cmath",
    "compute_canonical_reflected_weil_matrix",
    "compute_critical_zero_observable",
    "compute_grouped_correlation_system",
    "compute_local_positivity_threshold",
    "compute_reflected_quartet_observable",
    "compute_surviving_prime_bound",
    "compute_tc_quartet_matrix",
    "ctx",
    "dataclass",
    "evaluate_tc_arithmetic_spectral_baseline_comparison",
    "evaluate_tc_asymptotic_scaling_sweep",
    "evaluate_tc_canonical_weil_spectrum_sweep",
    "evaluate_tc_enlarged_grade_space_rayleigh_spectrum",
    "evaluate_tc_optimized_suppression_comparison",
    "evaluate_two_variable_explicit_expansion",
    "evaluate_two_variable_finite_decomposition",
    "flint",
    "fractions",
    "functools",
    "generate_canonical_reflected_weil_sign_certificate",
    "glob",
    "hashlib",
    "investigate_admissible_spectral_realization",
    "investigate_conditional_detection_implication",
    "investigate_scalar_spectral_bridge_target_b",
    "json",
    "kappa_hat_fast",
    "math",
    "math_core",
    "mpmath",
    "np",
    "os",
    "reproduce_cutoff_discrepancy",
    "sieve_prime_powers_in_window",
    "solve_complete_upper_objective",
    "sys",
    "test_spectral_matrix_span_recovery",
    "validate_or_project_legal_b",
    "validate_spectral_zero_coverage",
    "verify_canonical_reflected_weil_sign_certificate",
]
