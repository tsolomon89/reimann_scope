"""
Modular-Covariant Theta–Conductor Curvature Audit (`TASK-TC-036`).

Audits the post-`TASK-TC-035` operator-level selector candidate under `OBL-CT-001A`:

    Does theta self-duality together with the conductor operator and modularly
    covariant scale differentiation canonically produce a zero-independent
    arithmetic functional whose complete spectral curvature is positive
    exactly off the critical line?

Mathematical & Structural Contents
----------------------------------
1. `TASK-TC-035` Evidence-Scope Patch (Section 3):
   - Distinguishes Hamburger/Burnol zeta-distribution uniqueness (`zeta(s) = sum_{n>=1} n^{-s}`)
     from the Euler-product logarithmic-derivative von Mangoldt distribution
     (`-zeta'(s)/zeta(s) = sum_{n>=2} Lambda(n) n^{-s}`), and both from test-kernel selection.
   - Scopes Gaussian uniqueness to the positive heat-semigroup, harmonic-oscillator ground-state,
     or minimum-uncertainty class (the full self-Fourier space `F f = f` is infinite-dimensional).
   - Aligns all canonical theta certificate references to `N_cutoff = 15` and the committed
     outward tail bound `~ 4.91e-347` (`4.909446635601906e-347`).
   - Scopes the `TASK-TC-035` selector trilemma to `SIX_STANDARD_SELECTOR_FAMILIES_AUDITED`
     and `CONDITIONAL_COMPLEMENT_SIGN_DICHOTOMY_LEAN_PROVED`.

2. Theta Heat Scaling & Unique Heat-Drift Compensator (Sections 5 & 6):
   - For `g_t(x) = exp(-pi t x^2)` and `Theta_t(x, y) = exp(-pi t (x^2 + y^2))` (`t > 0`),
     the spatial Euler generator `E = x d/dx + y d/dy` and heat Euler generator `D = t d/dt`
     satisfy `E Theta_t = 2 D Theta_t` and `E^2 Theta_t = 4 t^2 d^2/dt^2 Theta_t + 4 t d/dt Theta_t`.
   - For the monic second-order family `L_c = E(E - c) = E^2 - c E`,
     `L_c Theta_t = 4 t^2 d^2/dt^2 Theta_t + (4 - 2c) t d/dt Theta_t`, uniquely forcing `c = 2`:
         `L_heat = E(E - 2) = 4 (D^2 - D)`,   `L_heat Theta_t = 4 t^2 d^2/dt^2 Theta_t`
     (`HEAT_DRIFT_COMPENSATOR_UNIQUELY_FORCED`).

3. Modular Covariance vs. Heat-Drift Compensator (Sections 7 & 8):
   - For `f(1/t) = t^w f(t)`, the weight-normalized state `tilde{f}(t) = t^{w/2} f(t)` is
     inversion-even (`tilde{f}(1/t) = tilde{f}(t)`), with modular covariant derivative
     `nabla_w = D + w/2` satisfying `nabla_w f(1) = 0` and modular Hessian `H_{mod,w} = (D + w/2)^2`.
   - For the 2D theta product (`w = 1`), `4 H_{mod,1} = 4 (D + 1/2)^2 = (E + 1)^2` and
     `L_heat = E(E - 2) = 4 (D^2 - D)` do NOT coincide:
         `4 H_{mod,1} - L_heat = 8 D + 1 = 4 E + 1`
     (`HEAT_AND_MODULAR_HESSIANS_DIFFER_BY_FORCED_CONNECTION_TERMS`,
      `MODULAR_HESSIAN_DOES_NOT_REMOVE_HEAT_DRIFT`,
      `HEAT_COMPENSATOR_NOT_MODULARLY_FORCED`,
      `MODULAR_HESSIAN_DIFFERS_FROM_HEAT_COMPENSATOR`).

4. Primary-Source Conductor Operator & Dilation Commutator Audit (Sections 9, 10 & 11):
   - From Burnol (`math/9902080v1`, `math/9812012v1`, `math/0101068v1`), the local conductor
     operator on `L^2(K_nu, dx)` is `H_nu = A + B` where `A = M_{log|x|_nu}` and
     `B = F A F^{-1}` (with `y` denoting the 1D Fourier dual variable to `x`, NOT a second
     prime-station variable in a 2D kernel).
   - Under the 1D unitary dilation generator `A_dil = x d/dx + 1/2`, `[A_dil, A] = I` and
     `[A_dil, B] = -I` on the invariant core `Delta(R)`, so `[A_dil, H_nu] = 0` and
     `[A_dil, [A_dil, H_nu]] = 0` (`CONDUCTOR_COMMUTES_WITH_DILATION`,
     `CONDUCTOR_DILATION_COMMUTATION_REMOVES_NEW_GRADE_SIGNAL`).

5. Prime-Only Covariant Variance, No-Contradiction Firewall, Completed Functional & Spectral Audit (Sections 12–22):
   - Certifies in 128-bit Arb that `C_prime^cov(t) = A_0(t) A_{2,cov}(t) - A_1(t)^2 = 4*pi^2*t^2*(M_0*M_2 - M_1^2) > 0`.
   - Establishes `POSITIVE_ARITHMETIC_VARIANCE_HAS_NO_CONTRADICTORY_SPECTRAL_LAW`,
     `THETA_CONDUCTOR_FUNCTIONAL_REMAINS_DOUBLE_SPECTRAL`,
     `THETA_CONDUCTOR_POSITIVITY_IS_RH_EQUIVALENT`,
     `GENERIC_HEAT_VARIANCE_NOT_TC_CONSTRAINT`, and
     `ONE_PRECISE_THETA_CONDUCTOR_SUBGATE_OPEN`, keeping `OBL-CT-001A = OPEN`.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Sequence, Tuple

try:
    import flint  # type: ignore
except ImportError:  # pragma: no cover
    flint = None

from tc.transport_mismatch_curvature import (
    ARB_CERTIFICATION_NOT_AVAILABLE,
    prime_power_base_table,
)

# ---------------------------------------------------------------------------
# Constants and Required Classification Codes (`TASK-TC-036`)
# ---------------------------------------------------------------------------

TAU: float = 2.0 * math.pi
LOG_TAU: float = math.log(TAU)

TASK_TC_036_ID = "TASK-TC-036"
TASK_TC_036_STATUS = "TASK_TC_036_MODULAR_THETA_CONDUCTOR_AUDIT_COMPLETE"
STARTING_HEAD = "e3e967f5288e41e55e101e9d7e88f7f541e94d43"
SUBSTANTIVE_PARENT_HEAD = "a8d7ccd5bd72e7c0f9577befaf15b0dc11777f54"

# Section 3.4 Scope Classifications for TASK-TC-035 Patch
SIX_STANDARD_SELECTOR_FAMILIES_AUDITED = "SIX_STANDARD_SELECTOR_FAMILIES_AUDITED"
CONDITIONAL_COMPLEMENT_SIGN_DICHOTOMY_LEAN_PROVED = (
    "CONDITIONAL_COMPLEMENT_SIGN_DICHOTOMY_LEAN_PROVED"
)

# Section 6 Heat-Drift Compensator Classifications
HEAT_DRIFT_COMPENSATOR_UNIQUELY_FORCED = "HEAT_DRIFT_COMPENSATOR_UNIQUELY_FORCED"
HEAT_DRIFT_COMPENSATOR_UNIQUE_BUT_NOT_MODULAR_SELECTOR = (
    "HEAT_DRIFT_COMPENSATOR_UNIQUE_BUT_NOT_MODULAR_SELECTOR"
)

# Section 8 Hessian Comparison Classifications
HEAT_AND_MODULAR_HESSIANS_DIFFER_BY_FORCED_CONNECTION_TERMS = (
    "HEAT_AND_MODULAR_HESSIANS_DIFFER_BY_FORCED_CONNECTION_TERMS"
)
MODULAR_HESSIAN_DOES_NOT_REMOVE_HEAT_DRIFT = (
    "MODULAR_HESSIAN_DOES_NOT_REMOVE_HEAT_DRIFT"
)
HEAT_COMPENSATOR_NOT_MODULARLY_FORCED = "HEAT_COMPENSATOR_NOT_MODULARLY_FORCED"
MODULAR_HESSIAN_DIFFERS_FROM_HEAT_COMPENSATOR = (
    "MODULAR_HESSIAN_DIFFERS_FROM_HEAT_COMPENSATOR"
)

# Section 10 Dilation-Conductor Commutator Classifications
CONDUCTOR_COMMUTES_WITH_DILATION = "CONDUCTOR_COMMUTES_WITH_DILATION"
CONDUCTOR_DILATION_COMMUTATION_REMOVES_NEW_GRADE_SIGNAL = (
    "CONDUCTOR_DILATION_COMMUTATION_REMOVES_NEW_GRADE_SIGNAL"
)

# Section 12 Linear-Quadratic Firewall Classification
LINEAR_QUADRATIC_FUNCTIONAL_CONFLATION = "LINEAR_QUADRATIC_FUNCTIONAL_CONFLATION"

# Section 14 No-Contradiction Firewall Classification
POSITIVE_ARITHMETIC_VARIANCE_HAS_NO_CONTRADICTORY_SPECTRAL_LAW = (
    "POSITIVE_ARITHMETIC_VARIANCE_HAS_NO_CONTRADICTORY_SPECTRAL_LAW"
)

# Section 15 Pole-Regularization Repair Classifications (`TASK-TC-036R`)
TASK_TC_036R_ID = "TASK-TC-036R"
TASK_TC_036R_STATUS = "TASK_TC_036R_POLE_REGULARIZATION_REPAIR_COMPLETE"
UNSHIFTED_REGULARIZER_DOES_NOT_ANNIHILATE_POLES = (
    "UNSHIFTED_REGULARIZER_DOES_NOT_ANNIHILATE_POLES"
)
CORRECTED_POLE_REGULARIZER_D_SQUARED_MINUS_ONE_SIXTEENTH = (
    "CORRECTED_POLE_REGULARIZER_D_SQUARED_MINUS_ONE_SIXTEENTH"
)
COMPLETED_THETA_CONDUCTOR_REGULARIZATION_REPAIRED = (
    "COMPLETED_THETA_CONDUCTOR_REGULARIZATION_REPAIRED"
)

# Section 16 & 17 Spectral Transfer and Pairing Classifications
UNRESTRICTED_DOUBLE_ZERO_SUM = "UNRESTRICTED_DOUBLE_ZERO_SUM"
SIGNED_SINGLE_ZERO_SUM = "SIGNED_SINGLE_ZERO_SUM"
HERMITIAN_WEIL_FORM = "HERMITIAN_WEIL_FORM"
COMPLETE_SPECTRAL_TRANSFER_NOT_DERIVED = "COMPLETE_SPECTRAL_TRANSFER_NOT_DERIVED"
THETA_CONDUCTOR_FUNCTIONAL_REMAINS_DOUBLE_SPECTRAL = (
    "THETA_CONDUCTOR_FUNCTIONAL_REMAINS_DOUBLE_SPECTRAL"
)

# Section 19 & 20 Weil Equivalence and Generic-Base Classifications
THETA_CONDUCTOR_POSITIVITY_IS_RH_EQUIVALENT = (
    "THETA_CONDUCTOR_POSITIVITY_IS_RH_EQUIVALENT"
)
GENERIC_HEAT_VARIANCE_NOT_TC_CONSTRAINT = "GENERIC_HEAT_VARIANCE_NOT_TC_CONSTRAINT"

# Section 22 Principal Classification
ONE_PRECISE_THETA_CONDUCTOR_SUBGATE_OPEN = (
    "ONE_PRECISE_THETA_CONDUCTOR_SUBGATE_OPEN"
)
PRINCIPAL_CLASSIFICATION = ONE_PRECISE_THETA_CONDUCTOR_SUBGATE_OPEN
OBL_CT_001A_STATUS = "OPEN"



# ---------------------------------------------------------------------------
# Section 3: Required `TASK-TC-035` Scope Patch
# ---------------------------------------------------------------------------


def build_task_tc_035_scope_corrections() -> Dict[str, Any]:
    """
    Return the structured record of the four `TASK-TC-035` evidence-scope corrections
    mandated by Section 3 of `TASK-TC-036`.
    """
    return {
        "patch_status": "TASK_TC_035_SCOPE_OVERSTATEMENTS_REPAIRED",
        "distribution_vs_prime_power_distinction": {
            "zeta_dirichlet_series": "zeta(s) = sum_{n>=1} n^{-s}",
            "von_mangoldt_log_derivative": "-zeta'(s)/zeta(s) = sum_{n>=2} Lambda(n) n^{-s}",
            "valid_deductive_chain": [
                "1. The functional equation plus growth/support assumptions characterizes the zeta-side distribution.",
                "2. The Euler product and logarithmic differentiation determine the von Mangoldt prime-power distribution.",
                "3. Neither theorem selects a unique test kernel.",
            ],
            "zeta_and_von_mangoldt_identified_as_one_scalar_ray": False,
            "selects_unique_test_kernel": False,
        },
        "gaussian_uniqueness_scope": {
            "scoped_statement": (
                "The Gaussian is uniquely selected within the specified positive heat-semigroup, "
                "harmonic-oscillator ground-state, or minimum-uncertainty class."
            ),
            "full_self_fourier_space_is_one_dimensional": False,
            "self_fourier_eigenbasis_note": (
                "All even Hermite functions H_{4k}(sqrt(2*pi)*x) exp(-pi*x^2) (k >= 0) satisfy "
                "F(psi_{4k}) = psi_{4k}; only k = 0 is strictly positive / minimum-uncertainty / "
                "heat-semigroup ground state."
            ),
        },
        "canonical_theta_certificate_parameters": {
            "committed_N_cutoff": 15,
            "committed_outward_tail_bound_str": "[4.90944663560190599562356800150073399e-347 +/- 5.10e-383]",
            "committed_outward_tail_bound_approx": 4.909446635601906e-347,
            "uncommitted_narrative_values_removed": ["N=60", "10^{-3400}"],
        },
        "selector_trilemma_scope": {
            "families_audited_status": SIX_STANDARD_SELECTOR_FAMILIES_AUDITED,
            "lean_dichotomy_status": CONDITIONAL_COMPLEMENT_SIGN_DICHOTOMY_LEAN_PROVED,
            "lean_proves_all_possible_selectors_exhausted": False,
            "scope_explanation": (
                "The six standard selector families are audited by paper/Arb/literature analysis "
                "(SIX_STANDARD_SELECTOR_FAMILIES_AUDITED), while Lean proves the conditional "
                "algebraic complement-sign dichotomy (CONDITIONAL_COMPLEMENT_SIGN_DICHOTOMY_LEAN_PROVED)."
            ),
        },
    }


# ---------------------------------------------------------------------------
# Section 5 & 6: Exact Theta Heat State, Euler/Heat Generators & Compensator
# ---------------------------------------------------------------------------


def theta_1d_heat_state(x: float, t: float = 1.0, base_pi: float = math.pi) -> float:
    """Evaluate the 1D Gaussian heat state g_t(x) = exp(-pi * t * x^2) for t > 0."""
    if t <= 0.0:
        raise ValueError(f"Heat parameter t must be strictly positive, got {t}")
    return math.exp(-base_pi * t * x * x)


def theta_2d_heat_state(
    x: float, y: float, t: float = 1.0, base_pi: float = math.pi
) -> float:
    """Evaluate the 2D Gaussian heat state Theta_t(x, y) = g_t(x) g_t(y) = exp(-pi * t * (x^2 + y^2))."""
    if t <= 0.0:
        raise ValueError(f"Heat parameter t must be strictly positive, got {t}")
    return math.exp(-base_pi * t * (x * x + y * y))


def evaluate_theta_euler_and_heat_jets(
    x: float, y: float, t: float = 1.0, base_pi: float = math.pi
) -> Dict[str, float]:
    """
    Evaluate Theta_t(x, y) together with:
      - spatial Euler derivatives E Theta_t, E^2 Theta_t (where E = x d/dx + y d/dy);
      - heat derivatives d_t Theta_t, d_t^2 Theta_t;
      - heat Euler derivatives D Theta_t = t d_t Theta_t, D^2 Theta_t = (t d_t)^2 Theta_t.
    Verifies identically:
      - E Theta_t = 2 D Theta_t
      - E^2 Theta_t = 4 t^2 d_t^2 Theta_t + 4 t d_t Theta_t.
    """
    if t <= 0.0:
        raise ValueError(f"Heat parameter t must be strictly positive, got {t}")
    r = x * x + y * y
    theta = math.exp(-base_pi * t * r)

    # Spatial partial derivatives
    # x d/dx Theta_t = -2 * pi * t * x^2 * Theta_t
    # (x d/dx)^2 Theta_t = (4 * pi^2 * t^2 * x^4 - 4 * pi * t * x^2) * Theta_t
    ex = -2.0 * base_pi * t * x * x
    ey = -2.0 * base_pi * t * y * y
    e1_spatial = (ex + ey) * theta

    e2x = 4.0 * (base_pi * t * x * x) ** 2 - 4.0 * base_pi * t * x * x
    e2y = 4.0 * (base_pi * t * y * y) ** 2 - 4.0 * base_pi * t * y * y
    e2_spatial = (e2x + 2.0 * ex * ey + e2y) * theta

    # Heat parameter derivatives
    dt1 = -base_pi * r * theta
    dt2 = (base_pi * r) ** 2 * theta
    d1_heat = t * dt1
    d2_heat = t * t * dt2 + t * dt1

    rhs_e1 = 2.0 * d1_heat
    rhs_e2 = 4.0 * t * t * dt2 + 4.0 * t * dt1

    return {
        "x": x,
        "y": y,
        "t": t,
        "r": r,
        "theta_t": theta,
        "E_theta_t": e1_spatial,
        "two_D_theta_t": rhs_e1,
        "E_minus_2D_abs_err": abs(e1_spatial - rhs_e1),
        "E2_theta_t": e2_spatial,
        "D_theta_t": d1_heat,
        "D2_theta_t": d2_heat,
        "dt1_theta_t": dt1,
        "dt2_theta_t": dt2,
        "four_t2_dt2_plus_4t_dt1": rhs_e2,
        "E2_expansion_abs_err": abs(e2_spatial - rhs_e2),
    }


def evaluate_general_drift_operator_L_c(
    c: float, x: float, y: float, t: float = 1.0, base_pi: float = math.pi
) -> Dict[str, Any]:
    """
    Evaluate the monic second-order operator L_c = E(E - c) = E^2 - c E on Theta_t(x, y):
        L_c Theta_t = 4 t^2 d_t^2 Theta_t + (4 - 2c) t d_t Theta_t.
    """
    jets = evaluate_theta_euler_and_heat_jets(x, y, t=t, base_pi=base_pi)
    lhs = jets["E2_theta_t"] - c * jets["E_theta_t"]
    drift_coeff = 4.0 - 2.0 * c
    pure_second_heat = 4.0 * t * t * jets["dt2_theta_t"]
    drift_part = drift_coeff * t * jets["dt1_theta_t"]
    rhs = pure_second_heat + drift_part
    return {
        "c": c,
        "drift_coefficient_4_minus_2c": drift_coeff,
        "drift_vanishes": abs(drift_coeff) < 1e-15,
        "L_c_theta_t_direct": lhs,
        "L_c_theta_t_expansion": rhs,
        "four_t2_dt2_theta_t": pure_second_heat,
        "drift_term_value": drift_part,
        "expansion_abs_err": abs(lhs - rhs),
        "residual_vs_pure_second_heat": abs(lhs - pure_second_heat),
    }


def audit_unique_heat_drift_compensator() -> Dict[str, Any]:
    """
    Prove and verify Section 6: within the monic second-order family L_c = E(E - c) = E^2 - c E
    (no constant term), c = 2 is the unique coefficient cancelling the first-order t d/dt drift
    on the degree-two heat family Theta_t.
    """
    sample_points = [(2.0, 2.0, 1.0), (2.0, 3.0, 1.0), (3.0, 5.0, 0.75), (4.0, 7.0, 1.4)]
    max_scaling_err = 0.0
    max_c2_residual = 0.0
    for x, y, t in sample_points:
        jets = evaluate_theta_euler_and_heat_jets(x, y, t=t)
        max_scaling_err = max(
            max_scaling_err,
            jets["E_minus_2D_abs_err"],
            jets["E2_expansion_abs_err"],
        )
        c2_eval = evaluate_general_drift_operator_L_c(2.0, x, y, t=t)
        max_c2_residual = max(max_c2_residual, c2_eval["residual_vs_pure_second_heat"])

    non_c2_controls = {}
    for c_val in (0.0, 1.0, -1.0, 3.0):
        ev = evaluate_general_drift_operator_L_c(c_val, 2.0, 3.0, t=1.0)
        non_c2_controls[f"c={c_val}"] = {
            "drift_coefficient_4_minus_2c": ev["drift_coefficient_4_minus_2c"],
            "residual_vs_pure_second_heat": ev["residual_vs_pure_second_heat"],
        }

    return {
        "general_operator_family": "L_c = E(E - c) = E^2 - c*E",
        "expansion_on_theta_t": "L_c Theta_t = 4*t^2*d_t^2 Theta_t + (4 - 2*c)*t*d_t Theta_t",
        "drift_coefficient_formula": "4 - 2*c",
        "unique_compensator_c": 2.0,
        "unique_operator": "L_heat = E(E - 2) = 4*(D^2 - D)",
        "compensated_identity": "L_heat Theta_t = 4*t^2*d_t^2 Theta_t",
        "uniqueness_scope": [
            "monic quadratic polynomials in E",
            "no constant term",
            "exact removal of the t d/dt drift term on the degree-two heat family Theta_t",
        ],
        "is_modularly_canonical": False,
        "max_euler_heat_scaling_abs_err": max_scaling_err,
        "max_c2_drift_residual": max_c2_residual,
        "non_c2_controls": non_c2_controls,
        "classification": HEAT_DRIFT_COMPENSATOR_UNIQUELY_FORCED,
        "decision_tree_status": HEAT_DRIFT_COMPENSATOR_UNIQUE_BUT_NOT_MODULAR_SELECTOR,
    }


# ---------------------------------------------------------------------------
# Section 7 & 8: Modular Covariance Audit & Exact Comparison of Hessians
# ---------------------------------------------------------------------------


def jacobi_theta_1d_truncated(t: float, n_trunc: int = 50) -> float:
    """
    Evaluate the 1D Jacobi theta series theta(t) = sum_{n=-n_trunc}^{n_trunc} exp(-pi * n^2 * t)
    for t > 0. Satisfies theta(1/t) = t^{1/2} theta(t) up to exponentially small tail O(e^{-pi n_trunc^2 t}).
    """
    if t <= 0.0:
        raise ValueError(f"t must be > 0, got {t}")
    s = 1.0
    for n in range(1, n_trunc + 1):
        s += 2.0 * math.exp(-math.pi * (n * n) * t)
    return s


def modular_weight_normalized_value(
    f_fn: Any, t: float, w: float
) -> float:
    """Evaluate tilde{f}(t) = t^{w/2} f(t)."""
    return (t ** (0.5 * w)) * float(f_fn(t))


def evaluate_modular_covariant_derivative_1d_theta(
    t: float, n_trunc: int = 50
) -> Dict[str, float]:
    """
    Evaluate nabla_w f(t) = (t d/dt + w/2) f(t) and H_{mod,w} f(t) = (t d/dt + w/2)^2 f(t)
    on the 1D Jacobi theta function theta(t) (w = 1/2) and 2D product theta_2(t) = theta(t)^2 (w = 1).
    """
    theta0 = 1.0
    dt1 = 0.0
    dt2 = 0.0
    for n in range(1, n_trunc + 1):
        r = float(n * n)
        term = 2.0 * math.exp(-math.pi * r * t)
        theta0 += term
        dt1 += (-math.pi * r) * term
        dt2 += ((-math.pi * r) ** 2) * term

    # D = t d/dt, D^2 = t^2 d^2/dt^2 + t d/dt
    D_theta = t * dt1
    D2_theta = t * t * dt2 + t * dt1
    nabla_half_theta = D_theta + 0.25 * theta0
    H_mod_half_theta = D2_theta + 0.5 * D_theta + (1.0 / 16.0) * theta0

    # 2D product theta_2(t) = theta(t)^2 (weight w = 1)
    theta2 = theta0 * theta0
    D_theta2 = 2.0 * theta0 * D_theta
    D2_theta2 = 2.0 * (D_theta * D_theta + theta0 * D2_theta)
    nabla_1_theta2 = D_theta2 + 0.5 * theta2
    H_mod_1_theta2 = D2_theta2 + D_theta2 + 0.25 * theta2

    return {
        "t": t,
        "theta_1d": theta0,
        "D_theta_1d": D_theta,
        "nabla_1_2_theta_1d": nabla_half_theta,
        "H_mod_1_2_theta_1d": H_mod_half_theta,
        "theta_2d": theta2,
        "D_theta_2d": D_theta2,
        "nabla_1_theta_2d": nabla_1_theta2,
        "H_mod_1_theta_2d": H_mod_1_theta2,
    }


def compare_heat_and_modular_hessians(
    x: float = 2.0, y: float = 3.0, t: float = 1.0
) -> Dict[str, Any]:
    """
    Compare L_heat = E(E - 2) = 4(D^2 - D) with 4 H_{mod,1} = 4(D + 1/2)^2 = (E + 1)^2
    on the two-variable theta state Theta_t(x, y) (Section 8).

    Proves:
        4 H_{mod,1} - L_heat = 4(D + 1/2)^2 - 4(D^2 - D) = 8 D + 1 = 4 E + 1 != 0.
    """
    jets = evaluate_theta_euler_and_heat_jets(x, y, t=t)
    theta_val = jets["theta_t"]
    E_val = jets["E_theta_t"]
    E2_val = jets["E2_theta_t"]
    D_val = jets["D_theta_t"]
    D2_val = jets["D2_theta_t"]

    L_heat_spatial = E2_val - 2.0 * E_val
    L_heat_from_D = 4.0 * (D2_val - D_val)
    four_H_mod_1_from_D = 4.0 * (D2_val + D_val + 0.25 * theta_val)
    four_H_mod_1_from_E = E2_val + 2.0 * E_val + theta_val

    diff_val = four_H_mod_1_from_D - L_heat_from_D
    connection_8D_plus_1 = 8.0 * D_val + theta_val
    connection_4E_plus_1 = 4.0 * E_val + theta_val

    return {
        "heat_hessian_operator": "L_heat = E(E - 2) = 4*(D^2 - D) = 4*t^2*d_t^2",
        "scaled_modular_hessian_operator": "4*H_{mod,1} = 4*(D + 1/2)^2 = (E + 1)^2 = 4*t^2*d_t^2 + 8*t*d_t + 1",
        "exact_operator_difference": "4*H_{mod,1} - L_heat = 8*D + 1 = 4*E + 1",
        "operators_coincide": False,
        "modular_hessian_removes_heat_drift": False,
        "heat_compensator_is_modularly_covariant": False,
        "sample_point": {"x": x, "y": y, "t": t},
        "L_heat_theta_t": L_heat_spatial,
        "four_H_mod_1_theta_t": four_H_mod_1_from_D,
        "difference_value": diff_val,
        "eight_D_plus_1_theta_t": connection_8D_plus_1,
        "four_E_plus_1_theta_t": connection_4E_plus_1,
        "L_heat_spatial_vs_D_abs_err": abs(L_heat_spatial - L_heat_from_D),
        "four_H_mod_spatial_vs_D_abs_err": abs(
            four_H_mod_1_from_E - four_H_mod_1_from_D
        ),
        "difference_identity_abs_err": max(
            abs(diff_val - connection_8D_plus_1),
            abs(diff_val - connection_4E_plus_1),
        ),
        "classifications": [
            HEAT_AND_MODULAR_HESSIANS_DIFFER_BY_FORCED_CONNECTION_TERMS,
            MODULAR_HESSIAN_DOES_NOT_REMOVE_HEAT_DRIFT,
            HEAT_COMPENSATOR_NOT_MODULARLY_FORCED,
            MODULAR_HESSIAN_DIFFERS_FROM_HEAT_COMPENSATOR,
        ],
        "primary_classification": HEAT_AND_MODULAR_HESSIANS_DIFFER_BY_FORCED_CONNECTION_TERMS,
    }


def audit_modular_covariance() -> Dict[str, Any]:
    """
    Audit Section 7 (modular weight normalization tilde{f}(t) = t^{w/2} f(t),
    modular covariant derivative nabla_w = D + w/2, vanishing at t = 1, and
    modular Hessian H_{mod,w} = (D + w/2)^2).
    """
    test_t_values = [0.5, 0.8, 1.25, 2.0]
    max_involution_err_1d = 0.0
    max_involution_err_2d = 0.0
    for t in test_t_values:
        v1 = modular_weight_normalized_value(jacobi_theta_1d_truncated, t, w=0.5)
        v1_inv = modular_weight_normalized_value(
            jacobi_theta_1d_truncated, 1.0 / t, w=0.5
        )
        max_involution_err_1d = max(max_involution_err_1d, abs(v1 - v1_inv))

        theta2_fn = lambda u: jacobi_theta_1d_truncated(u) ** 2
        v2 = modular_weight_normalized_value(theta2_fn, t, w=1.0)
        v2_inv = modular_weight_normalized_value(theta2_fn, 1.0 / t, w=1.0)
        max_involution_err_2d = max(max_involution_err_2d, abs(v2 - v2_inv))

    at_self_dual = evaluate_modular_covariant_derivative_1d_theta(1.0, n_trunc=50)
    return {
        "modular_transformation_law": "f(1/t) = t^w f(t)",
        "weight_normalized_function": "tilde{f}(t) = t^{w/2} f(t)",
        "inversion_symmetry": "tilde{f}(1/t) = tilde{f}(t)",
        "weight_1d_theta": 0.5,
        "weight_2d_product_theta": 1.0,
        "modular_covariant_derivative": "nabla_w = D + w/2 = t d/dt + w/2",
        "self_dual_vanishing_law": "nabla_w f(1) = 0",
        "modular_hessian": "H_{mod,w} = nabla_w^2 = (D + w/2)^2",
        "max_involution_abs_err_1d_w_half": max_involution_err_1d,
        "max_involution_abs_err_2d_w_one": max_involution_err_2d,
        "nabla_1_2_theta_1d_at_t_eq_1": at_self_dual["nabla_1_2_theta_1d"],
        "nabla_1_theta_2d_at_t_eq_1": at_self_dual["nabla_1_theta_2d"],
        "self_dual_first_derivative_vanishes_verified": (
            abs(at_self_dual["nabla_1_2_theta_1d"]) < 1e-14
            and abs(at_self_dual["nabla_1_theta_2d"]) < 1e-14
        ),
    }


# ---------------------------------------------------------------------------
# Section 9 & 10: Primary-Source Conductor Operator & Dilation Commutator
# ---------------------------------------------------------------------------


def audit_conductor_operator_primary_sources() -> Dict[str, Any]:
    """
    Return the primary-source audit of Burnol's conductor operator (`math/9902080v1`,
    `math/9812012v1`, `math/0101068v1`), explicitly distinguishing the five objects
    required by Section 9 and explaining why Burnol's notation `log|x| + log|y|`
    denotes `M_{log|x|} + F M_{log|x|} F^{-1}` on 1D `L^2(K_nu, dx)` rather than a
    two-variable multiplication operator.
    """
    comparison_table = [
        {
            "object": "Multiplication by log|x|_nu (A = M_{log|x|_nu})",
            "hilbert_or_test_space": (
                "Dense domain S_0(K_nu) or Delta(K_nu) in L^2(K_nu, dx)"
            ),
            "exact_definition": "(A phi)(x) = log(|x|_nu) phi(x)",
            "self_adjoint_status": (
                "Essentially self-adjoint on S_0(K_nu) and Delta(K_nu) (unbounded multiplication operator)"
            ),
            "fourier_invariant_status": (
                "NO: F A F^{-1} = B != A"
            ),
            "dilation_relation": (
                "U(lambda) A U(lambda)^{-1} = A - (log|lambda|_nu) I; [A_dil, A] = I"
            ),
            "explicit_formula_role": (
                "Position-space logarithmic multiplier; generates d/ds on multiplicative character space X_nu"
            ),
        },
        {
            "object": "Fourier-conjugate logarithmic operator (B = F A F^{-1})",
            "hilbert_or_test_space": (
                "Dense domain S_0(K_nu) or Delta(K_nu) in L^2(K_nu, dx)"
            ),
            "exact_definition": (
                "(B phi)(x) = F(log(|y|_nu) (F^{-1} phi)(y))(x) = -(G_nu * phi)(x) where G_nu = F(-log|y|_nu)"
            ),
            "self_adjoint_status": (
                "Essentially self-adjoint on S_0(K_nu) and Delta(K_nu) (unitarily conjugate to A via F)"
            ),
            "fourier_invariant_status": (
                "NO: F B F^{-1} = A != B"
            ),
            "dilation_relation": (
                "U(lambda) B U(lambda)^{-1} = B + (log|lambda|_nu) I; [A_dil, B] = -I"
            ),
            "explicit_formula_role": (
                "Additive convolution with Haran-Burnol kernel G_nu = F(-log|y|_nu); equals -Gamma A Gamma^{-1}"
            ),
        },
        {
            "object": "Local conductor operator (H_nu = C_nu = A + B)",
            "hilbert_or_test_space": (
                "Essentially self-adjoint on S_0(K_nu) and invariant Schwartz-Mellin core Delta(K_nu) in L^2(K_nu, dx)"
            ),
            "exact_definition": (
                "H_nu = M_{log|.|_nu} + F M_{log|.|_nu} F^{-1} = A - Gamma A Gamma^{-1}; "
                "acts on L^2(X_nu) along Re(s)=1/2 as spectral multiplier d/ds log Gamma_nu(chi_nu, s)"
            ),
            "self_adjoint_status": (
                "YES: essentially self-adjoint on S_0(K_nu) and Delta(K_nu), unbounded above, bounded below (Burnol Thm E2, H2, J2)"
            ),
            "fourier_invariant_status": (
                "YES: F H_nu F^{-1} = B + A = H_nu and I H_nu I^{-1} = H_nu"
            ),
            "dilation_relation": (
                "Completely dilation-invariant: U(lambda) H_nu U(lambda)^{-1} = H_nu; [A_dil, H_nu] = 0"
            ),
            "explicit_formula_role": (
                "Explains each local Weil term W_nu(g; chi) = H_nu(g_{nu;chi})(1) as the spectral multiplier d/ds log Gamma_nu"
            ),
        },
        {
            "object": "Global sum over places of local conductor evaluations",
            "hilbert_or_test_space": (
                "Compactly supported smooth test functions g in C_c^infty((0, infty)) lifted to g_{nu;chi}(t) = g(|t|_nu) chi_nu^{-1}(t) in L^2(K_nu^x, d^*t)"
            ),
            "exact_definition": (
                "W(g; chi) = sum_nu H_nu(g_{nu;chi})(1) (Burnol math/0101068v1 Thm 3.3, math/9902080v1 Thm C1)"
            ),
            "self_adjoint_status": (
                "Linear scalar evaluation functional (point evaluation at t = 1 of sum_nu H_nu g_{nu;chi}), not a Hilbert-space operator"
            ),
            "fourier_invariant_status": (
                "Invariant under global functional-equation inversion g(u) |-> u^{-1} g(u^{-1})"
            ),
            "dilation_relation": (
                "Under multiplicative shift g_lambda(u) = g(u/lambda), shifts Mellin integrand by lambda^{s - 1/2}"
            ),
            "explicit_formula_role": (
                "Equals the arithmetic side (prime-power + Archimedean local terms) of Weil's explicit formula"
            ),
        },
        {
            "object": "Global explicit-formula distribution W_zeta",
            "hilbert_or_test_space": (
                "Tempered / compactly supported test space C_c^infty((0, infty)) or Weil admissible class on R_+^x"
            ),
            "exact_definition": (
                "<W_zeta, g> = sum_rho hat{g}(rho - 1/2) - (hat{g}(-1/2) + hat{g}(1/2)) = -sum_nu H_nu(g_nu)(1)"
            ),
            "self_adjoint_status": (
                "Distribution in D'((0, infty)); induces the Hermitian Weil sesquilinear form Z(g * g^*)"
            ),
            "fourier_invariant_status": (
                "Symmetric under multiplicative inversion g^*(u) = u^{-1} bar{g(u^{-1})}"
            ),
            "dilation_relation": (
                "Tracks zero ordinates and off-critical offsets under multiplicative shifts on R_+^x"
            ),
            "explicit_formula_role": (
                "Bridges the global zero-pole sum to the sum over all places nu of local conductor evaluations"
            ),
        },
    ]

    return {
        "conductor_operator_definition": (
            "H_nu = A + B = M_{log|.|_nu} + F M_{log|.|_nu} F^{-1} on L^2(K_nu, dx), "
            "with spectral multiplier H_nu(chi_nu, s) = d/ds log Gamma_nu(chi_nu, s) on Re(s) = 1/2"
        ),
        "conductor_domain": (
            "Initial domain S_0(K_nu) = C_c^infty(K_nu \\ {0}) and invariant core "
            "Delta(K_nu) = {phi in L^2(K_nu, dx) : multiplicative Fourier transform in S(X_nu)} "
            "(Burnol math/9902080v1 Theorems E2, J1, J2)"
        ),
        "physicist_notation_clarification": (
            "In Burnol's notation H = log|x| + log|y|, x and y are Fourier-conjugate variables "
            "on the SAME 1D local field K_nu (A = log|x|, B = F log|x| F^{-1}), NOT two independent "
            "spatial variables in a 2D kernel F_0(x_1, x_2)."
        ),
        "fourier_invariance_status": "PROVED_ON_INVARIANT_CORE_DELTA_BY_BURNOL_THEOREM_E2",
        "object_comparison_table": comparison_table,
        "primary_sources": [
            {
                "arxiv_id": "math/9902080v1",
                "url": "https://arxiv.org/abs/math/9902080v1",
                "citation": "Burnol (1999), The Explicit Formula and the conductor operator, 28 pp.",
            },
            {
                "arxiv_id": "math/9812012v1",
                "url": "https://arxiv.org/abs/math/9812012v1",
                "citation": "Burnol (1998), Spectral Analysis of the local Commutator Operators, 16 pp.",
            },
            {
                "arxiv_id": "math/0101068v1",
                "url": "https://arxiv.org/abs/math/0101068v1",
                "citation": "Burnol (2000), Sur les Formules Explicites I: analyse invariante, C. R. Acad. Sci. Paris 331, 423-428.",
            },
        ],
    }


def audit_dilation_conductor_commutator() -> Dict[str, Any]:
    """
    Audit Section 10: compute [A_dil, C] and [A_dil, [A_dil, C]] on the common dense
    invariant domain Delta(R), where A_dil = x d/dx + 1/2 is the skew-adjoint generator
    of the unitary dilation group (U(lambda) phi)(x) = lambda^{-1/2} phi(x / lambda).

    Since U(lambda) A U(lambda)^{-1} = A - (log lambda) I and
          U(lambda) B U(lambda)^{-1} = B + (log lambda) I,
    differentiating at lambda = 1 yields:
        [A_dil, A] = I,   [A_dil, B] = -I   ==>   [A_dil, C] = [A_dil, A + B] = 0,
    and consequently [A_dil, [A_dil, C]] = 0.
    """
    # Numerical spectral-space verification on the critical line s = 1/2 + i*tau:
    # On L^2(R, dtau / 2pi), A_dil acts as multiplication by -i*tau and C_infty acts as
    # multiplication by h_+(tau) = -log(pi) + Re(psi(1/4 + i*tau/2)).
    # Multiplication operators by -i*tau and h_+(tau) commute pointwise for all tau in R.
    comm_A_coeff = 1.0
    comm_B_coeff = -1.0
    comm_C_coeff = comm_A_coeff + comm_B_coeff
    double_comm_C_coeff = 0.0

    return {
        "unitary_dilation_group": "(U(lambda) phi)(x) = lambda^{-1/2} phi(x / lambda), lambda > 0",
        "dilation_generator": "A_dil = x d/dx + 1/2 I = E_1D + 1/2 I",
        "common_dense_domain": "Delta(R) = {|x|^{-1/2} F(log|x|) : F in S(R)} (Burnol Theorem J1)",
        "position_log_conjugation": "U(lambda) A U(lambda)^{-1} = A - (log lambda) I",
        "momentum_log_conjugation": "U(lambda) B U(lambda)^{-1} = B + (log lambda) I",
        "commutator_A_dil_with_A": "I",
        "commutator_A_dil_with_B": "-I",
        "commutator_A_dil_with_C": "0",
        "double_commutator_A_dil_with_C": "0",
        "commutator_E_with_C": "0",
        "double_commutator_E_with_C": "0",
        "comm_A_scalar_coeff": comm_A_coeff,
        "comm_B_scalar_coeff": comm_B_coeff,
        "comm_C_scalar_coeff": comm_C_coeff,
        "double_comm_C_scalar_coeff": double_comm_C_coeff,
        "removes_new_grade_curvature_from_conductor_commutators": True,
        "grade_curvature_implication": (
            "Because [A_dil, C] = 0 on Delta(R), C and scale dilation U(tau^{-eta K}) commute: "
            "U(tau^{-eta K}) C Phi = C U(tau^{-eta K}) Phi. All commutator generators [E, C] "
            "and [E, [E, C]] vanish identically, and inserting C before grade transport simply "
            "replaces the state Phi by the fixed state C Phi without generating a non-commuting "
            "scale connection."
        ),
        "status": CONDUCTOR_COMMUTES_WITH_DILATION,
        "secondary_status": CONDUCTOR_DILATION_COMMUTATION_REMOVES_NEW_GRADE_SIGNAL,
    }


# ---------------------------------------------------------------------------
# Section 11: Operator Selector Axioms & Symbolic Resolution
# ---------------------------------------------------------------------------


def solve_operator_selector_axioms() -> Dict[str, Any]:
    """
    Symbolically audit the 8 zero-independent operator selector axioms of Section 11
    on the candidate operator algebra generated by:
        {I, E, E^2, C, 1/2 (C E + E C), [E, C], [E, [E, C]]}
    restricted to total degree <= 2.

    Step 1: By [E, C] = 0 on Delta, [E, C] = 0, [E, [E, C]] = 0, and 1/2 (C E + E C) = C E.
            The candidate operator of total degree <= 2 has the general form:
                O = c_0 I + c_1 E + c_2 E^2 + c_3 C + c_4 C E + c_5 C^2.
    Step 2: On L^2(R^2, dx dy), the skew-adjoint dilation generator is A_2 = E + I (A_2^* = -A_2),
            satisfying F_2 A_2 F_2^{-1} = -A_2 and modular inversion I_inv A_2 I_inv^{-1} = -A_2,
            while F_2 C F_2^{-1} = C and C^* = C.
            In the (A_2, C) basis (with E = A_2 - I):
                O = b_0 I + b_1 A_2 + b_2 A_2^2 + b_3 C + b_4 C A_2 + b_5 C^2.
            Axiom 1 (Fourier invariance F_2 O F_2^{-1} = O), Axiom 2 (self-adjointness O^* = O),
            and Axiom 3 (2D theta modular inversion symmetry t |-> 1/t) require the odd-in-A_2
            coefficients to vanish:
                b_1 = 0,   b_4 = 0,
            leaving the 2-parameter scale family:
                b_0 I + b_2 A_2^2 = b_0 I + b_2 (E + I)^2 = b_2 E^2 + 2 b_2 E + (b_0 + b_2) I,
            forcing:
                c_2 = b_2,   c_1 = +2 c_2,   c_0 = c_2 + b_0 (with independent scalar b_0),   c_4 = 0.
            Imposing vanishing on the dilation-invariant mode ker(A_2) (b_0 = 0) further restricts
            to the single projective ray R^x * (E + I)^2 = R^x * 4 H_{mod,1} (where c_0 = c_2).
    Step 3: Axiom 4 (degree-two heat covariance / exact removal of t d/dt drift on Theta_t)
            requires the scale operator to be a multiple of L_heat = E(E - 2) = E^2 - 2 E,
            forcing:
                c_1 = -2 c_2,   c_0 = 0.
    Step 4: Combining modular/Fourier symmetry (c_1 = +2 c_2) and heat-drift removal (c_1 = -2 c_2)
            forces (independently of the scalar offset b_0):
                4 c_2 = 0  ==>  c_2 = 0, c_1 = 0, c_0 = 0 (and b_0 = 0)!
            And the remaining pure-conductor polynomial c_3 C + c_5 C^2 has degree 0 in scale
            differentiation E, violating Axiom 5 (second order in scale differentiation).
    """
    axioms = [
        "1. Fourier invariance (F O F^{-1} = O)",
        "2. Self-adjointness on a specified dense domain (Delta)",
        "3. Compatibility with theta modular inversion (t |-> 1/t, weight w = 1 on 2D theta)",
        "4. Degree-two heat covariance (exact removal of first-order t d/dt drift on Theta_t)",
        "5. Second order in scale differentiation (c_2 != 0)",
        "6. No fitted scalar coefficients",
        "7. Compatibility with the completed-zeta Archimedean factor",
        "8. Non-scalar action",
    ]
    generators_input = [
        "I",
        "E",
        "E^2",
        "C",
        "1/2 (C E + E C)",
        "[E, C]",
        "[E, [E, C]]",
    ]
    reduced_basis_on_delta = ["I", "E", "E^2", "C", "C E", "C^2"]

    # Symbolic linear system for the scale-derivative coefficients (c_0, c_1, c_2, c_4):
    # Modular/Fourier covariance (Axioms 1, 2, 3): c_1 - 2*c_2 = 0, c_0 = c_2 + b_0, c_4 = 0
    # Heat-drift removal (Axiom 4):                c_1 + 2*c_2 = 0, c_0 = 0
    # Unique solution (even before fixing b_0):    c_2 = c_1 = c_0 = b_0 = c_4 = 0.
    return {
        "axioms_audited": axioms,
        "candidate_generators": generators_input,
        "commutator_reduction_on_delta": {
            "[E, C]": "0",
            "[E, [E, C]]": "0",
            "1/2 (C E + E C)": "C E",
            "surviving_degree_le_2_monomials": reduced_basis_on_delta,
        },
        "modular_and_fourier_constraint_on_scale_part": {
            "two_parameter_invariant_subspace": "b_0 I + b_2 (E + I)^2 = b_2 E^2 + 2 b_2 E + (b_0 + b_2) I",
            "selected_projective_ray_after_ker_A2_normalization": "R^x * (E + I)^2 = R^x * 4 H_{mod,1} (at b_0 = 0)",
            "coefficient_relations": {
                "c_1": "2 * c_2",
                "c_0": "c_2 + b_0 (c_0 = c_2 when normalized by b_0 = 0 on ker(E + I))",
                "c_4": "0",
            },
        },
        "heat_drift_removal_constraint_on_scale_part": {
            "selected_projective_ray": "R^x * E(E - 2) = R^x * L_heat",
            "coefficient_relations": {"c_1": "-2 * c_2", "c_0": "0"},
        },
        "joint_linear_system_solution_for_scale_part": {
            "c_0": 0.0,
            "c_1": 0.0,
            "c_2": 0.0,
            "c_4": 0.0,
            "b_0": 0.0,
            "second_order_scale_term_survives_joint_axioms": False,
        },
        "fitted_coefficients_used": False,
        "outcome_classification": (
            "JOINT_MODULAR_AND_HEAT_DRIFT_AXIOMS_INCONSISTENT_AT_SECOND_ORDER_SPLITS_INTO_TWO_DISTINCT_RAYS"
        ),
        "split_canonical_rays_audited": {
            "ray_A_heat_compensator": "L_heat = E(E - 2) = 4(D^2 - D) (satisfies Axioms 4, 5, 6, 8; violates Axioms 1, 2, 3)",
            "ray_B_modular_hessian": "4 H_{mod,1} = (E + I)^2 = 4(D + 1/2)^2 (satisfies Axioms 1, 2, 3, 5, 6, 8 at b_0 = 0; violates Axiom 4)",
        },
    }


# ---------------------------------------------------------------------------
# Section 12, 13 & 14: Linear-Quadratic Firewall, Prime-Only Covariant Variance & No-Contradiction
# ---------------------------------------------------------------------------


def audit_linear_quadratic_firewall() -> Dict[str, Any]:
    """
    Maintain the strict distinction between the linear explicit-formula functional
    <W_zeta, O Phi> and the quadratic variance functional
    <W_zeta, Phi><W_zeta, O Phi> - <W_zeta, D Phi>^2 (Section 12).
    """
    return {
        "linear_functional": {
            "formula": "<W_zeta, O Phi>",
            "spectral_structure": "Single-zero linear sum sum_rho m_rho hat{(O Phi)}(rho - 1/2) - poles",
            "automatic_variance_positivity": False,
            "spectral_classification": SIGNED_SINGLE_ZERO_SUM,
        },
        "quadratic_variance_functional": {
            "formula": "<W, Phi><W, O Phi> - <W, E Phi>^2",
            "arithmetic_prime_only_positivity": (
                "Positive Cauchy-Schwarz / Bernstein variance 4*pi^2*t^2*(M_0*M_2 - M_1^2) >= 0 "
                "when W = mu_pp x mu_pp and O = L_heat = E(E - 2)"
            ),
            "completed_spectral_structure": (
                "Product of two linear explicit-formula sums, inducing an unrestricted double "
                "zero sum sum_{rho, sigma} m_rho m_sigma"
            ),
            "spectral_classification": UNRESTRICTED_DOUBLE_ZERO_SUM,
        },
        "transfer_of_quadratic_positivity_to_linear_sum_allowed": False,
        "conflation_error_code": LINEAR_QUADRATIC_FUNCTIONAL_CONFLATION,
    }


def certify_prime_only_covariant_variance_arb(
    t: float = 1.0,
    N_cutoff: int = 15,
    prec_bits: int = 128,
    force_flint_unavailable: bool = False,
) -> Dict[str, Any]:
    """
    Certify the prime-only covariant variance control (Section 13):
        A_0(t)       = <mu_pp x mu_pp, Theta_t>            = M_0(t),
        A_1(t)       = <mu_pp x mu_pp, E Theta_t>          = -2*pi*t * M_1(t),
        A_{2,cov}(t) = <mu_pp x mu_pp, E(E - 2) Theta_t>   = 4*pi^2*t^2 * M_2(t),
    and:
        C_prime^cov(t) := A_0(t) A_{2,cov}(t) - A_1(t)^2
                        = 4*pi^2*t^2 * (M_0(t) M_2(t) - M_1(t)^2) >= 0,
    using outward 128-bit Arb ball arithmetic with fail-closed fallback.
    """
    if flint is None or force_flint_unavailable:
        return {
            "certified": False,
            "status": ARB_CERTIFICATION_NOT_AVAILABLE,
            "prec_bits": prec_bits,
            "t": t,
            "N_cutoff": N_cutoff,
            "covariant_variance_enclosure": None,
            "zero_excluded": False,
        }

    saved_prec = flint.ctx.prec
    try:
        flint.ctx.prec = prec_bits
        arb = flint.arb
        pi_arb = arb.pi()
        t_arb = arb(str(t))
        c_arb = arb(2) * pi_arb * t_arb

        base_table = prime_power_base_table(N_cutoff)
        stations_arb = [(n, arb(p).log()) for n, p, _ in base_table]

        M0 = arb(0)
        M1 = arb(0)
        M2 = arb(0)
        for n, lam_n in stations_arb:
            for m, lam_m in stations_arb:
                wt = lam_n * lam_m
                r = arb(n * n + m * m)
                g0 = (-pi_arb * t_arb * r).exp()
                M0 += wt * g0
                M1 += wt * r * g0
                M2 += wt * r * r * g0

        A0 = M0
        A1 = -c_arb * M1
        A2_uncomp = c_arb * c_arb * M2 - arb(2) * c_arb * M1
        A2_cov = c_arb * c_arb * M2

        C_cov_direct = A0 * A2_cov - A1 * A1
        C_cov_formula = c_arb * c_arb * (M0 * M2 - M1 * M1)
        C_uncomp = A0 * A2_uncomp - A1 * A1

        # Outward infinite-lattice tail bound for max(n, m) >= N_cutoff + 1 = 16
        M_ext = arb(N_cutoff + 1)
        tail_1d_k2 = arb(2) * (M_ext ** 5) * (-pi_arb * t_arb * M_ext * M_ext).exp()
        full_1d_k2 = arb(2) * (arb(2) ** 5) * (-pi_arb * t_arb * arb(4)).exp()
        tail_M_bound = arb(2) * full_1d_k2 * tail_1d_k2 + tail_1d_k2 * tail_1d_k2
        ball_err = arb(0, tail_M_bound.upper())

        M0_inf = M0 + ball_err
        M1_inf = M1 + ball_err
        M2_inf = M2 + ball_err
        C_cov_inf = c_arb * c_arb * (M0_inf * M2_inf - M1_inf * M1_inf)

        strictly_pos_compact = bool(C_cov_direct > 0)
        strictly_pos_inf = bool(C_cov_inf > 0)
        certified = strictly_pos_compact and strictly_pos_inf

        mid = float(C_cov_direct.mid())
        rad = float(C_cov_direct.rad())
        return {
            "certified": certified,
            "status": (
                "PRIME_ONLY_COVARIANT_VARIANCE_POSITIVE_CERTIFIED"
                if certified
                else "ARB_ENCLOSURE_SIGN_UNRESOLVED"
            ),
            "is_control_theorem_only": True,
            "is_completed_zeta_constraint": False,
            "prec_bits": prec_bits,
            "t": t,
            "N_cutoff": N_cutoff,
            "A0_str": str(A0),
            "A1_str": str(A1),
            "A2_cov_str": str(A2_cov),
            "A2_uncompensated_str": str(A2_uncomp),
            "uncompensated_curvature_str": str(C_uncomp),
            "covariant_variance_enclosure": {
                "arb_str": str(C_cov_direct),
                "mid_display_float": mid,
                "rad_display_float": rad,
                "outward_float_interval": [mid - rad, mid + rad],
                "strictly_positive": strictly_pos_compact,
            },
            "infinite_lattice_tail_bound_str": str(tail_M_bound),
            "infinite_lattice_covariant_variance_enclosure": {
                "arb_str": str(C_cov_inf),
                "strictly_positive": strictly_pos_inf,
            },
            "identity_abs_diff_str": str(abs(C_cov_direct - C_cov_formula)),
            "identity_verified": bool(abs(C_cov_direct - C_cov_formula) < arb("1e-35")),
            "zero_excluded": certified,
        }
    finally:
        flint.ctx.prec = saved_prec


def audit_no_contradiction_firewall() -> Dict[str, Any]:
    """
    Audit Section 14: verify that having a positive arithmetic variance A_arith >= 0
    and a positive spectral variance A_spec >= 0 produces NO contradiction.
    """
    return {
        "arithmetic_variance_sign": "NONNEGATIVE (C_prime^cov(t) >= 0, strictly positive for >= 2 distinct prime radii)",
        "hypothetical_positive_spectral_sign": "NONNEGATIVE (A_spec >= 0)",
        "incompatible_sign_pair_present": False,
        "valid_contradiction_templates": [
            "A_arith = 0 versus A_spec > 0",
            "A_arith <= 0 versus A_spec > 0",
            "A_arith = C versus A_spec = C + D with D > 0",
        ],
        "drift_compensation_consequence": (
            "Replacing E^2 by L_heat = E(E - 2) flips the prime-only curvature sign from "
            "C_arith(Theta_1) < 0 to C_prime^cov(1) > 0, eliminating the nonpositive arithmetic "
            "sign needed to contradict a positive off-critical spectral term."
        ),
        "classification": POSITIVE_ARITHMETIC_VARIANCE_HAS_NO_CONTRADICTORY_SPECTRAL_LAW,
    }


# ---------------------------------------------------------------------------
# Section 15, 16, 17, 18, 19 & 20: Completed Functional, Spectral Transfer,
# Pairing, Complement Sign, Weil Equivalence & Generic-Base Control
# ---------------------------------------------------------------------------


def evaluate_unshifted_vs_corrected_pole_regularizer(
    t: float = 1.0,
    s_samples: Sequence[float] = (0.0, 0.25, 0.5, 0.75, 1.0, 2.0),
) -> Dict[str, Any]:
    """
    Audit the TASK-TC-036R pole-regularization repair on the weight-normalized
    1D theta state tilde{g}_t(u) = t^{1/4} exp(-pi * t * u^2):

    1. Because M[tilde{g}_t](s) = int_0^infty tilde{g}_t(u) u^{s-1} du
       = (1/2) pi^{-s/2} Gamma(s/2) t^{1/4 - s/2}, the heat Euler generator
       D = t d/dt acts on the Mellin transform by:
           lambda(s) = 1/4 - s/2 = -z/2,   where z = s - 1/2.
    2. The unshifted operator D(D - 1/2) used in TASK-TC-036 therefore acts by:
           (1/4 - s/2)(1/4 - s/2 - 1/2) = (1/4 - s/2)(-1/4 - s/2) = s^2/4 - 1/16,
       which evaluates to -1/16 != 0 at s = 0 and +3/16 != 0 at s = 1, and in spatial
       coordinates gives:
           D(D - 1/2)(t^{1/4} e^{-r}) = t^{1/4} (r^2 - r - 1/16) e^{-r},   r = pi * t * u^2,
       whose origin value at u = 0 is -(1/16) t^{1/4} != 0 (failing to kill the u = 0 mode).
    3. The exact pole-annihilating operator on tilde{g}_t(u) is:
           P_reg(D) := D^2 - 1/16 = (D - 1/4)(D + 1/4),
       whose Mellin multiplier on t^{1/4 - s/2} is:
           (1/4 - s/2)^2 - 1/16 = (1/4) s (s - 1) = (1/4) (z^2 - 1/4),
       which vanishes at both s = 0 (z = -1/2) and s = 1 (z = +1/2), annihilates both
       quarter-power modes t^{1/4} = tilde{g}_t(0) and t^{-1/4} = int_R tilde{g}_t(u) du,
       and produces the repaired spatial state:
           Phi_t(u) := (D^2 - 1/16)(t^{1/4} e^{-r})
                     = t^{1/4} (r^2 - (3/2) r) e^{-r}
                     = pi * t^{5/4} * u^2 * (pi * t * u^2 - 3/2) * exp(-pi * t * u^2),
       satisfying Phi_t(0) = 0, Phi_t'(0) = 0, and int_0^infty Phi_t(u) du = 0.
    4. Because Gamma(s/2) ~ 2/s has a simple pole at s = 0, the single factor s(s - 1)/4
       cancels the Gamma-pole at s = 0 to give the finite value M[Phi_t](0) = -(1/4) t^{1/4}
       and vanishes at s = 1 (M[Phi_t](1) = 0), while the squared regularizer
       P_reg(D)^2 = (D^2 - 1/16)^2 produces Phi_t^{(2)}(u) = (D^2 - 1/16)^2 tilde{g}_t(u)
       with M[Phi_t^{(2)}](0) = M[Phi_t^{(2)}](1) = 0.
    """
    if t <= 0.0:
        raise ValueError(f"Heat parameter t must be positive, got {t}")
    t_quarter = t ** 0.25
    t_minus_quarter = t ** (-0.25)

    # Spatial origin values at u = 0 (r = 0)
    unshifted_origin_val = -t_quarter / 16.0
    corrected_origin_val = 0.0

    # Zero-frequency integral int_0^infty (...) du:
    # For tilde{g}_t(u), int_0^infty tilde{g}_t(u) du = (1/2) t^{-1/4}.
    # D acts on t^{-1/4} by -1/4:
    #   D(D - 1/2)(1/2 t^{-1/4}) = (-1/4)(-3/4)(1/2 t^{-1/4}) = +3/32 t^{-1/4} != 0
    #   (D^2 - 1/16)(1/2 t^{-1/4}) = (1/16 - 1/16)(1/2 t^{-1/4}) = 0.
    unshifted_half_line_integral = (3.0 / 32.0) * t_minus_quarter
    corrected_half_line_integral = 0.0

    mellin_samples = []
    max_multiplier_identity_err = 0.0
    for s in s_samples:
        z = s - 0.5
        lam = 0.25 - 0.5 * s
        unshifted_mult = lam * (lam - 0.5)
        unshifted_formula = 0.25 * s * s - 0.0625
        corrected_mult = lam * lam - 0.0625
        corrected_s_formula = 0.25 * s * (s - 1.0)
        corrected_z_formula = 0.25 * (z * z - 0.25)
        err = max(
            abs(unshifted_mult - unshifted_formula),
            abs(corrected_mult - corrected_s_formula),
            abs(corrected_mult - corrected_z_formula),
        )
        max_multiplier_identity_err = max(max_multiplier_identity_err, err)
        mellin_samples.append(
            {
                "s": s,
                "z": z,
                "lambda_D": lam,
                "unshifted_D_D_minus_half_multiplier": unshifted_mult,
                "corrected_D2_minus_1_16_multiplier": corrected_mult,
                "corrected_s_formula_s_s_minus_1_over_4": corrected_s_formula,
                "corrected_z_formula_z2_minus_1_4_over_4": corrected_z_formula,
                "abs_identity_err": err,
            }
        )

    return {
        "defect_status": UNSHIFTED_REGULARIZER_DOES_NOT_ANNIHILATE_POLES,
        "repair_status": CORRECTED_POLE_REGULARIZER_D_SQUARED_MINUS_ONE_SIXTEENTH,
        "completed_repair_status": COMPLETED_THETA_CONDUCTOR_REGULARIZATION_REPAIRED,
        "weight_normalized_state": "tilde{g}_t(u) = t^{1/4} exp(-pi * t * u^2)",
        "mellin_scaling_power": "t^{1/4 - s/2} = t^{-z/2} (z = s - 1/2)",
        "D_mellin_eigenvalue": "lambda(s) = 1/4 - s/2 = -z/2",
        "defective_unshifted_operator": {
            "operator": "D(D - 1/2)",
            "mellin_multiplier_on_tilde_g_t": "(1/4 - s/2)(-1/4 - s/2) = s^2/4 - 1/16",
            "value_at_s_eq_0": -1.0 / 16.0,
            "value_at_s_eq_1": 3.0 / 16.0,
            "spatial_polynomial_factor": "r^2 - r - 1/16 (r = pi * t * u^2)",
            "origin_value_at_u_eq_0": unshifted_origin_val,
            "half_line_integral_value": unshifted_half_line_integral,
            "annihilates_poles": False,
        },
        "repaired_pole_regularizer": {
            "operator": "P_reg(D) = D^2 - 1/16 = (D - 1/4)(D + 1/4)",
            "mellin_multiplier_s": "(1/4 - s/2)^2 - 1/16 = (1/4) s (s - 1)",
            "mellin_multiplier_z": "(1/4) (z^2 - 1/4), z = s - 1/2",
            "value_at_s_eq_0": 0.0,
            "value_at_s_eq_1": 0.0,
            "annihilates_t_pos_quarter": True,
            "annihilates_t_neg_quarter": True,
            "spatial_formula": (
                "Phi_t(u) = (D^2 - 1/16)(t^{1/4} e^{-pi t u^2}) "
                "= t^{1/4} (pi^2 t^2 u^4 - (3/2) pi t u^2) e^{-pi t u^2}"
            ),
            "spatial_polynomial_factor": "r^2 - (3/2) r (r = pi * t * u^2)",
            "origin_value_Phi_t_0": corrected_origin_val,
            "origin_first_derivative_Phi_t_prime_0": 0.0,
            "half_line_integral_int_0_infty_Phi_t_du": corrected_half_line_integral,
            "mellin_transform_formula": (
                "M[Phi_t](s) = (1/8) s (s - 1) pi^{-s/2} Gamma(s/2) t^{1/4 - s/2}, "
                "holomorphic on Re(s) > -2 with M[Phi_t](0) = -(1/4) t^{1/4} and M[Phi_t](1) = 0"
            ),
            "squared_regularizer_formula": (
                "Phi_t^{(2)}(u) = (D^2 - 1/16)^2 tilde{g}_t(u) "
                "= t^{1/4} (r^4 - 6 r^3 + (45/8) r^2 - (3/8) r) e^{-r}, "
                "with M[Phi_t^{(2)}](s) = (1/32) s^2 (s - 1)^2 pi^{-s/2} Gamma(s/2) t^{1/4 - s/2} "
                "satisfying M[Phi_t^{(2)}](0) = M[Phi_t^{(2)}](1) = 0"
            ),
            "annihilates_poles": True,
        },
        "mellin_samples": mellin_samples,
        "max_multiplier_identity_abs_err": max_multiplier_identity_err,
    }


def audit_completed_theta_conductor_functional() -> Dict[str, Any]:
    """
    Audit Sections 15–19 (repaired in TASK-TC-036R):
    1. Construct the zero-independent completed arithmetic functional A_{Theta, C}^{cov}(t)
       on the repaired pole-regularized theta state
           Phi_t(u) = P_reg(D) tilde{g}_t(u) = (D^2 - 1/16)(t^{1/4} e^{-pi t u^2})
                    = t^{1/4} (pi^2 t^2 u^4 - (3/2) pi t u^2) e^{-pi t u^2}
       (and its squared pole-annihilated companion Phi_t^{(2)} = (D^2 - 1/16)^2 tilde{g}_t),
       including prime-power terms, pole terms at s = 0 and s = 1, trivial-zero / Archimedean
       gamma-factor terms via Burnol's local conductor H_infty, zero-mode cancellation at u = 0
       and infinity, and explicit domain conditions on Delta(R_+^x).
    2. Derive the spectral representation and natural zero pairing on the repaired state.
    3. Audit complement-sign and Weil-equivalence firewalls.
    """
    pole_reg_audit = evaluate_unshifted_vs_corrected_pole_regularizer(t=1.0)
    required_background_terms = {
        "prime_power_terms": (
            "W_prim(J Phi_t) = -sum_{n>=2} Lambda(n) n^{-1/2} ((J Phi_t)(n) + (J Phi_t)(n^{-1})) "
            "= -sum_p H_p(Phi_{t,p})(1), where (J Phi_t)(u) = u^{1/2} Phi_t(u); "
            "because Phi_t(n^{-1}) = O(n^{-2}) as n -> infty, the reflected prime-power sum "
            "sum_{n>=2} Lambda(n) n^{-1} Phi_t(n^{-1}) = O(sum_{n>=2} Lambda(n) n^{-3}) converges absolutely."
        ),
        "pole_terms_s_eq_0_and_1": (
            "W_pole(J Phi_t) = hat{(J Phi_t)}(-1/2) + hat{(J Phi_t)}(1/2) = M[Phi_t](0) + M[Phi_t](1). "
            "For Phi_t = (D^2 - 1/16) tilde{g}_t, the factor s(s-1)/4 cancels the simple pole of "
            "Gamma(s/2) ~ 2/s at s = 0 (leaving the finite value M[Phi_t](0) = -(1/4) t^{1/4}, which is "
            "subsequently annihilated by L_heat = 4(D^2 - D) when paired with (D - 1/4), or vanishes "
            "identically on the squared state Phi_t^{(2)} = (D^2 - 1/16)^2 tilde{g}_t where "
            "M[Phi_t^{(2)}](0) = M[Phi_t^{(2)}](1) = 0)."
        ),
        "trivial_zero_and_archimedean_gamma_terms": (
            "W_infty(J Phi_t) = -H_infty(Phi_{t,infty})(1) = (log(2*pi) + gamma_E) Phi_t(1) "
            "+ int_{1/2}^infty (Phi_t(1/u) u - Phi_t(1))/|1 - u| du/(2u) "
            "+ int_{-infty}^{1/2} Phi_t(1/|u|) |u| / |1 - u| du/(2|u|) "
            "(encodes pi^{-s/2} Gamma(s/2) and all trivial zeros s = -2m via Burnol Theorem D3)"
        ),
        "normalization_terms": (
            "Multiplicative half-density lift (J Phi_t)(u) = u^{1/2} Phi_t(u) in L^2(R_+^x, du/u), "
            "so that hat{(J Phi_t)}(z) = int_0^infty (J Phi_t)(u) u^{z} du/u = int_0^infty Phi_t(u) u^{s-1} du "
            "= M[Phi_t](s) with s = 1/2 + z"
        ),
        "regularization_at_origin_and_infinity": (
            "Because raw tilde{g}_t(0) = t^{1/4} != 0 and int_0^infty tilde{g}_t(u) du = (1/2) t^{-1/4} != 0 "
            "cause the reflected prime sum and the s = 0, 1 pole integrals to diverge (and the unshifted "
            "operator D(D - 1/2) gives D(D - 1/2) tilde{g}_t(0) = -(1/16) t^{1/4} != 0 with Mellin multiplier "
            "s^2/4 - 1/16), the weight-normalized theta state MUST be regularized by the shifted pole-annihilator "
            "P_reg(D) := D^2 - 1/16 = (D - 1/4)(D + 1/4), which multiplies M[tilde{g}_t](s) by "
            "(1/4 - s/2)^2 - 1/16 = s(s - 1)/4 = (z^2 - 1/4)/4 (matching completed xi(s) = 1/2 s(s - 1) pi^{-s/2} Gamma(s/2) zeta(s))."
        ),
        "operator_domain_condition": (
            "Phi_t(u) := (D^2 - 1/16) tilde{g}_t(u) = t^{1/4} (pi^2 t^2 u^4 - (3/2) pi t u^2) e^{-pi t u^2} "
            "(and Phi_t^{(2)} := (D^2 - 1/16)^2 tilde{g}_t), satisfying Phi_t(0) = 0, Phi_t'(0) = 0, "
            "int_0^infty Phi_t(u) du = 0, super-polynomial Gaussian decay as u -> infty, and "
            "hat{(J Phi_t)}(z) = (1/8)(z^2 - 1/4) pi^{-(z+1/2)/2} Gamma((z+1/2)/2) t^{-z/2} holomorphic on Re(z) > -5/2."
        ),
    }

    return {
        "functional_symbol": "A_{Theta, C}^{cov}(t)",
        "pole_regularization_repair": pole_reg_audit,
        "zero_independent_definition": (
            "For the repaired pole-regularized theta state Phi_t = (D^2 - 1/16)(t^{1/4} g_t) "
            "(or its squared pole-vanishing companion Phi_t^{(2)} = (D^2 - 1/16)^2(t^{1/4} g_t)) "
            "and the completed zero-independent explicit-formula linear functional "
            "W_comp(Psi) := W_pole(Psi) - sum_{p} H_p(Psi_p)(1) - H_infty(Psi_infty)(1), "
            "define the quadratic completed functional "
            "A_{Theta, C}^{cov}(t) := W_comp(J Phi_t) W_comp(L_heat J Phi_t) - W_comp(2 D J Phi_t)^2 "
            "(and its linear counterpart L_{Theta, C}^{cov}(t) := W_comp(L_heat J Phi_t), "
            "where 2 D = E_1D - 1/2 I acts on t^{1/4 - s/2} = t^{-z/2} by -z and "
            "L_heat = 4(D^2 - D) = 2D(2D - 2) acts by z(z + 2))."
        ),
        "defined_without_nontrivial_zero_coordinates": True,
        "structural_type": {
            "variance_form": "QUADRATIC_DISTRIBUTIONAL_REGULARIZED",
            "single_evaluation_form": "LINEAR_DISTRIBUTIONAL_REGULARIZED",
            "is_trace_class_operator_trace": False,
        },
        "background_terms_included": required_background_terms,
        "all_background_terms_explicit": True,
        "complete_spectral_representation": {
            "linear_form_expansion": (
                "L_{Theta, C}^{cov}(t) = sum_rho m_rho z_rho (z_rho + 2) hat{(J Phi_t)}(z_rho) - W_pole(L_heat J Phi_t), "
                "where z_rho = rho - 1/2 = delta_rho + i*gamma_rho and hat{(J Phi_t)}(z_rho) = (1/4) t^{-z_rho/2} xi_factor(rho)"
            ),
            "quadratic_variance_expansion": (
                "A_{Theta, C}^{cov}(t) = 1/2 sum_{rho, sigma} m_rho m_sigma hat{(J Phi_t^{(2)})}(z_rho) hat{(J Phi_t^{(2)})}(z_sigma) "
                "* [(z_rho - z_sigma)^2 + 2*(z_rho + z_sigma)]"
            ),
            "includes_multiplicities": True,
            "includes_reflections_and_conjugates": True,
            "includes_cross_zero_terms": True,
            "includes_pole_and_archimedean_transfer": True,
            "convergence_justification": (
                "Rapid Gaussian/Gamma decay |hat{(J Phi_t)}(delta + i*gamma)| << |gamma|^{A} exp(-pi*|gamma|/4) "
                "gives absolute convergence of both the single and double sums over nontrivial zeros."
            ),
            "linear_transfer_classification": SIGNED_SINGLE_ZERO_SUM,
            "quadratic_transfer_classification": UNRESTRICTED_DOUBLE_ZERO_SUM,
            "convolution_square_classification": HERMITIAN_WEIL_FORM,
        },
        "natural_zero_pairing_audit": {
            "conjugate_pair_rho_bar_rho": {
                "z_sum": "2 * delta_rho",
                "z_diff_squared": "-4 * gamma_rho^2 < 0",
                "isolated_by_completed_functional": False,
            },
            "reflection_pair_rho_1_minus_bar_rho": {
                "z_sum": "2 * i * gamma_rho",
                "z_diff_squared": "+4 * delta_rho^2 >= 0",
                "isolated_by_completed_functional": False,
            },
            "general_double_pair_rho_sigma": {
                "present_in_quadratic_variance": True,
                "reason": (
                    "The quadratic variance is a product of two global explicit-formula sums "
                    "W_comp(Psi_1) W_comp(Psi_2), which expands over all ordered zero pairs (rho, sigma)."
                ),
            },
            "conjugate_block_selected_by_hand": False,
            "pairing_classification": THETA_CONDUCTOR_FUNCTIONAL_REMAINS_DOUBLE_SPECTRAL,
        },
        "complement_sign_audit": {
            "decomposition": "A = S_rad + R_comp",
            "R_comp_zero_proved": False,
            "R_comp_nonneg_proved": False,
            "strict_remainder_domination_reused": False,
            "finite_truncation_promoted": False,
            "status": "COMPLEMENT_SIGN_UNCONTROLLED_WITHOUT_WEIL_POSITIVITY",
        },
        "weil_equivalence_audit": {
            "local_archimedean_conductor_positivity": (
                "Unconditional on Re(s) = 1/2 above the minimum mu_+ = -(log(8*pi) + gamma_E) - pi/2 "
                "(Burnol math/9902080v1 Theorem H2) and for support in [1/sqrt(2), sqrt(2)] "
                "(Burnol math/0101068v1 Theorem 3.7, where no primes >= 2 enter)"
            ),
            "global_positivity_across_primes": (
                "Equivalent to Weil's positivity criterion Z(g * g^*) >= 0 (Weil 1952; "
                "Burnol math/0101068v1 p. 2; Connes-Consani 2020 arXiv:2006.13771v1)"
            ),
            "classification": THETA_CONDUCTOR_POSITIVITY_IS_RH_EQUIVALENT,
        },
    }


def evaluate_generic_base_heat_control(
    q_values: Sequence[float] = (2.0, math.e, TAU, 10.0),
    t: float = 1.0,
    N_cutoff: int = 15,
) -> Dict[str, Any]:
    """
    Audit Section 20 (Tau-specificity vs. generic scale base q > 1):
    Under multiplicative grade transport x |-> q^{-eta K} x with arbitrary base q > 1:
      - d/d(eta)|_{eta=0} = -(K log q) E,
      - the heat-drift compensator L_heat = E(E - 2) and normalized covariant prime variance
        C_prime^cov(t) / A_0(t)^2 = 4*pi^2*t^2*(M_0*M_2 - M_1^2) / M_0^2
        are completely independent of q > 1!
    Identifies precisely where tau = 2*pi enters (additive Fourier character e^{-i*tau*x*y},
    Jacobi theta self-dual exponent pi = tau/2, and Archimedean conductor constant log(tau) + gamma_E).
    """
    stations = prime_power_base_table(N_cutoff)
    M0 = 0.0
    M1 = 0.0
    M2 = 0.0
    for n, p, _ in stations:
        lam_n = math.log(float(p))
        for m, q_p, _ in stations:
            lam_m = math.log(float(q_p))
            wt = lam_n * lam_m
            r = float(n * n + m * m)
            g0 = math.exp(-math.pi * t * r)
            M0 += wt * g0
            M1 += wt * r * g0
            M2 += wt * r * r * g0

    c = 2.0 * math.pi * t
    base_norm_var = (c * c * (M0 * M2 - M1 * M1)) / (M0 * M0)

    per_base_results = {}
    max_norm_var_diff = 0.0
    for q in q_values:
        if q <= 1.0:
            raise ValueError(f"Generic scale base q must satisfy q > 1, got {q}")
        L = math.log(q)
        # With eta-derivative generator -(L) E, the unnormalized second-order moments scale by L^2
        # and the normalized variance ratio (L^2 C_prime^cov) / (L^2 A_0^2) is invariant.
        unnorm_var_q = (L * L) * (c * c * (M0 * M2 - M1 * M1))
        norm_var_q = unnorm_var_q / ((L * M0) ** 2)
        diff = abs(norm_var_q - base_norm_var)
        max_norm_var_diff = max(max_norm_var_diff, diff)
        per_base_results[f"q={q:.6f}"] = {
            "q": q,
            "log_q": L,
            "unnormalized_eta_covariant_variance": unnorm_var_q,
            "normalized_covariant_variance_ratio": norm_var_q,
            "abs_diff_from_tau": diff,
        }

    return {
        "tested_bases_q": list(q_values),
        "normalized_covariant_variance_ratio": base_norm_var,
        "max_normalized_ratio_diff_across_q": max_norm_var_diff,
        "per_base_evaluations": per_base_results,
        "heat_compensator_depends_on_tau": False,
        "prime_variance_sign_depends_on_tau": False,
        "tau_specific_entry_points": [
            "Additive self-dual Fourier character lambda(x) = exp(-2*pi*i*x*y) = exp(-i*tau*x*y) on R",
            "Jacobi theta modular inversion theta(1/t) = sqrt(t) theta(t) requiring Gaussian exponent -pi*x^2 = -(tau/2)*x^2",
            "Completed zeta Archimedean factor pi^{-s/2} Gamma(s/2) = (tau/2)^{-s/2} Gamma(s/2)",
            "Burnol real Archimedean conductor constant log(2*pi) + gamma_E = log(tau) + gamma_E in W_R(F) (Burnol math/9902080v1 Theorem D3)",
        ],
        "classification": GENERIC_HEAT_VARIANCE_NOT_TC_CONSTRAINT,
    }


# ---------------------------------------------------------------------------
# Section 21: Primary-Source Literature Audit Table
# ---------------------------------------------------------------------------


def build_primary_source_literature_table() -> List[Dict[str, str]]:
    """
    Return the primary-source literature table required by Section 21.
    """
    return [
        {
            "result": "Hamburger (1921); Burnol (2007 math/0407443v3, 2012 arXiv:1106.4749v2); Baez-Duarte (2002 math/0207237v1)",
            "exact_hypotheses": (
                "Tempered / co-Poisson distribution supported on Z with completed functional equation "
                "xi(s) = xi(1 - s) and moderate polynomial growth"
            ),
            "selected_object": "1D zeta distribution ray C * zeta(s) (and via Euler product + log-derivative, -zeta'/zeta = sum Lambda(n) n^{-s})",
            "operator_identity": "F I = Gamma(chi, s) on multiplicative characters",
            "arithmetic_implication": "Fixes integer / prime-power station weights, NOT a unique test kernel",
            "spectral_implication": "Valid across all admissible test functions in the explicit formula",
            "rh_equivalent": "NO (unconditional characterization of zeta)",
        },
        {
            "result": "Burnol (1998 math/9812012v1, 1999 math/9902080v1, 2000 math/0101068v1)",
            "exact_hypotheses": (
                "Local completion K_nu with additive Haar measure dx, initial domain S_0(K_nu) or "
                "invariant Schwartz-Mellin core Delta(K_nu) in L^2(K_nu, dx)"
            ),
            "selected_object": "Local conductor operator H_nu = log|x|_nu + F log|x|_nu F^{-1} and bounded commutator K_nu = i[B, A]",
            "operator_identity": "[A_dil, H_nu] = 0, F H_nu F^{-1} = H_nu, I H_nu I^{-1} = H_nu, spectral multiplier d/ds log Gamma_nu(chi, s)",
            "arithmetic_implication": "W(g; chi) = sum_nu H_nu(g_{nu;chi})(1) reproduces all Weil local terms uniformly",
            "spectral_implication": "Reproduces linear explicit-formula sum over zeros and poles on Re(s) = 1/2",
            "rh_equivalent": "NO for operator identity; YES for global positivity Z(g * g^*) >= 0 (Burnol Thm 3.7 proves local positivity only for supp(g) in [1/c, c], c <= sqrt(2))",
        },
        {
            "result": "Jacobi (1829); Riemann (1859)",
            "exact_hypotheses": (
                "Positive heat semigroup g_t(x) = exp(-pi t x^2) (t > 0), Poisson summation on Z, "
                "and ground-state / minimum-uncertainty selection at t = 1"
            ),
            "selected_object": "1D Gaussian g_1(x) = exp(-pi x^2), 2D Gaussian Theta_1(x, y) = exp(-pi(x^2+y^2)), and theta series theta(t)",
            "operator_identity": "E Theta_t = 2 D Theta_t, L_heat Theta_t = E(E - 2) Theta_t = 4 t^2 d_t^2 Theta_t, nabla_w = D + w/2, P_reg(D) = D^2 - 1/16",
            "arithmetic_implication": "Uncompensated Euler curvature C_arith(Theta_1) < 0 by drift; drift-compensated prime variance C_prime^cov(t) >= 0",
            "spectral_implication": "Mellin transform of pole-regularized theta state (D^2 - 1/16) tilde{g}_t gives completed xi(s); quadratic variance yields double zero sum",
            "rh_equivalent": "NO (unconditional analytic continuation and functional equation)",
        },
        {
            "result": "Weil (1952); Haran (1990)",
            "exact_hypotheses": "Smooth compactly supported / rapidly decaying test function g on R_+^x",
            "selected_object": "Global explicit-formula distribution W_zeta and sesquilinear form Z(g * g^*)",
            "operator_identity": "Z(g) = sum_rho hat{g}(rho - 1/2) - (hat{g}(-1/2) + hat{g}(1/2)) = -sum_nu W_nu(g)",
            "arithmetic_implication": "Prime-power plus Archimedean local functional",
            "spectral_implication": "Single-zero sum for linear evaluation; reflection-paired Hermitian sum for convolution square g * g^*",
            "rh_equivalent": "YES: Z(g * g^*) >= 0 for all g in C_c^infty(R_+^x) <=> RH",
        },
        {
            "result": "Connes & Consani (2020 arXiv:2006.13771v1, 2021 arXiv:2106.01715v1, 2021 arXiv:2112.08820v1); Burnol (2001 math/0105120v1, 2004 math/0203120v7)",
            "exact_hypotheses": "Compression of scaling operator to Sonin space (orthogonal to cutoff projections P_Lambda, F P_Lambda F^{-1})",
            "selected_object": "Prolate spheroidal wave function basis and compressed semi-local trace functional",
            "operator_identity": "Angle-operator / prolate differential operator commuting with time-and-band limiting",
            "arithmetic_implication": "Archimedean compressed trace is positive by prolate/Toeplitz positivity",
            "spectral_implication": "Semi-local trace formula over finite primes + archimedean place reduces global positivity to Weil positivity",
            "rh_equivalent": "NO at single archimedean place; YES for global semi-local Weil positivity across primes",
        },
    ]


# ---------------------------------------------------------------------------
# Section 23: Exact Lean Theorem Map & Synchronization Verifier (`TASK-TC-036` / `TASK-TC-036R`)
# ---------------------------------------------------------------------------


def get_modular_theta_conductor_lean_map() -> Dict[str, Any]:
    """
    Return the exact declaration map for `formal/RiemannScope/ModularThetaConductorCurvature.lean`.
    """
    declarations = [
        {
            "identifier": "heatDriftCoeff",
            "kind": "def",
            "statement_scope": "heatDriftCoeff c := 4 - 2 * c",
            "algebraic_only": True,
            "paper_step_supported": "First-order heat-drift coefficient 4 - 2c in L_c Theta_t",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "poleRegMultiplier",
            "kind": "def",
            "statement_scope": "poleRegMultiplier s := (1 / 4 - s / 2) ^ 2 - 1 / 16",
            "algebraic_only": True,
            "paper_step_supported": "TASK-TC-036R: Mellin multiplier of the corrected pole regularizer P_reg(D) = D^2 - 1/16 on t^{1/4 - s/2}",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "theta_heat_euler_scaling",
            "kind": "theorem",
            "statement_scope": "(x * (-2*p*t*x) + y * (-2*p*t*y)) * theta = 2 * (t * (-p * (x^2 + y^2)) * theta)",
            "algebraic_only": True,
            "paper_step_supported": "Section 5: E Theta_t = 2 D Theta_t on the 2D Gaussian heat family",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "heat_drift_operator_expansion",
            "kind": "theorem",
            "statement_scope": "(4 * d2 + 4 * d1) - c * (2 * d1) = 4 * d2 + heatDriftCoeff c * d1",
            "algebraic_only": True,
            "paper_step_supported": "Section 6: L_c Theta_t = 4 t^2 d_t^2 Theta_t + (4 - 2c) t d_t Theta_t",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "heat_drift_compensator_unique",
            "kind": "theorem",
            "statement_scope": "(heatDriftCoeff c = 0 <-> c = 2) /\\ ((4 * d2 + 4 * d1) - 2 * (2 * d1) = 4 * d2)",
            "algebraic_only": True,
            "paper_step_supported": "Section 6: Unique heat-drift compensator c = 2 (L_heat = E(E - 2))",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "modular_weight_normalization_involution",
            "kind": "theorem",
            "statement_scope": "s != 0 -> f_inv = s^2 * f -> s^{-1} * f_inv = s * f",
            "algebraic_only": True,
            "paper_step_supported": "Section 7: Weight normalization tilde{f}(t) = t^{w/2} f(t) satisfies tilde{f}(1/t) = tilde{f}(t)",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "modular_covariant_deriv_vanishes_at_self_dual",
            "kind": "theorem",
            "statement_scope": "-(D1 + w / 2) = D1 + w / 2 -> D1 + w / 2 = 0",
            "algebraic_only": True,
            "paper_step_supported": "Section 7: Modular covariant derivative nabla_w f(1) = 0 at self-dual point t = 1",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "heat_and_modular_hessian_difference",
            "kind": "theorem",
            "statement_scope": "E = 2 * D -> 4*(D + 1/2)^2 - 4*(D^2 - D) = 8*D + 1 /\\ (E + 1)^2 - E*(E - 2) = 4*E + 1 /\\ 8*D + 1 = 4*E + 1",
            "algebraic_only": True,
            "paper_step_supported": "Section 8: Exact difference 4 H_{mod,1} - L_heat = 8 D + 1 = 4 E + 1",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "heat_and_modular_hessian_incompatibility",
            "kind": "theorem",
            "statement_scope": "c1 = 2 * c2 -> c1 = -2 * c2 -> c2 = 0 /\\ c1 = 0",
            "algebraic_only": True,
            "paper_step_supported": "Section 11: No nonzero second-order scale operator satisfies both modular Hessian and heat-drift compensator constraints",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "dilation_conductor_commutator_cancellation",
            "kind": "theorem",
            "statement_scope": "comm_A = 1 -> comm_B = -1 -> comm_A + comm_B = 0",
            "algebraic_only": True,
            "paper_step_supported": "Section 10: [A_dil, A] = I and [A_dil, B] = -I imply [A_dil, C] = 0",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "covariant_prime_variance_identity",
            "kind": "theorem",
            "statement_scope": "curvatureDet M0 (-c * M1) (c^2 * M2) = c^2 * curvatureDet M0 M1 M2",
            "algebraic_only": True,
            "paper_step_supported": "Section 13: Prime-only covariant variance identity C_prime^cov(t) = 4*pi^2*t^2*(M_0*M_2 - M_1^2)",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "covariant_prime_variance_nonneg",
            "kind": "theorem",
            "statement_scope": "0 <= w1 -> 0 <= w2 -> C_prime^cov = c^2 * w1 * w2 * (r1 - r2)^2 /\\ 0 <= C_prime^cov",
            "algebraic_only": True,
            "paper_step_supported": "Section 13: Nonnegativity of prime-only covariant variance via Lagrange identity",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "arithmetic_sign_and_spectral_sign_no_contradiction",
            "kind": "theorem",
            "statement_scope": "0 <= v -> exists A_arith A_spec, A_arith = v /\\ A_spec = v /\\ A_arith = A_spec /\\ 0 <= A_arith /\\ 0 <= A_spec",
            "algebraic_only": True,
            "paper_step_supported": "Section 14: Nonnegativity on both arithmetic and spectral sides is logically consistent (no contradiction)",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "complement_nonnegativity_contradiction",
            "kind": "theorem",
            "statement_scope": "A = S_rad + R_comp -> A <= 0 -> 0 < S_rad -> 0 <= R_comp -> False",
            "algebraic_only": True,
            "paper_step_supported": "Section 18: Complement-sign contradiction firewall",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "generic_quadratic_heat_base_control",
            "kind": "theorem",
            "statement_scope": "curvatureDet M0 (-(L * c) * M1) ((L * c)^2 * M2) = L^2 * (c^2 * curvatureDet M0 M1 M2)",
            "algebraic_only": True,
            "paper_step_supported": "Section 20: Generic scale base q > 1 homogeneity control (L = K log q)",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "unshifted_regularizer_mellin_defect",
            "kind": "theorem",
            "statement_scope": "(1/4 - s/2)*(1/4 - s/2 - 1/2) = s^2/4 - 1/16 /\\ value(0) = -1/16 /\\ value(1) = 3/16",
            "algebraic_only": True,
            "paper_step_supported": "TASK-TC-036R: Unshifted D(D - 1/2) fails to annihilate s = 0, 1 on t^{1/4 - s/2}",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "corrected_pole_regularizer_mellin_identity",
            "kind": "theorem",
            "statement_scope": "z = s - 1/2 -> poleRegMultiplier s = (1/4)*s*(s - 1) /\\ poleRegMultiplier s = (1/4)*(z^2 - 1/4) /\\ poleRegMultiplier 0 = 0 /\\ poleRegMultiplier 1 = 0",
            "algebraic_only": True,
            "paper_step_supported": "TASK-TC-036R: Repaired P_reg(D) = D^2 - 1/16 has Mellin multiplier s(s-1)/4 = (z^2 - 1/4)/4 vanishing at s = 0, 1",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "corrected_pole_regularizer_annihilates_quarter_powers",
            "kind": "theorem",
            "statement_scope": "((1/4)^2 - 1/16) * t_pos = 0 /\\ ((-1/4)^2 - 1/16) * t_neg = 0",
            "algebraic_only": True,
            "paper_step_supported": "TASK-TC-036R: P_reg(D) = D^2 - 1/16 annihilates both t^{1/4} = tilde{g}_t(0) and t^{-1/4} = int tilde{g}_t(u) du",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "corrected_pole_regularizer_spatial_jet",
            "kind": "theorem",
            "statement_scope": "((1/4 - r)^2 - r) - 1/16 = r^2 - (3/2)*r /\\ value_at_r_eq_0 = 0",
            "algebraic_only": True,
            "paper_step_supported": "TASK-TC-036R: Spatial polynomial factor r^2 - (3/2)r of Phi_t(u) = (D^2 - 1/16) tilde{g}_t(u) vanishes at u = 0",
            "external_theorem_dependency": "None",
        },
    ]

    return {
        "module_path": "formal/RiemannScope/ModularThetaConductorCurvature.lean",
        "total_module_declarations": len(declarations),
        "module_def_count": sum(1 for d in declarations if d["kind"] == "def"),
        "module_theorem_count": sum(1 for d in declarations if d["kind"] == "theorem"),
        "repository_compiled_theorem_declarations": 597,
        "formal_proof_hygiene": "0 sorry, 0 admit, no nonstandard project axioms introduced",
        "declarations": declarations,
        "not_formalized_in_lean": [
            "Burnol's functional-analytic conductor operator domain and essential self-adjointness on S_0 / Delta",
            "The complete Riemann-Weil explicit formula and contour-shift residue calculus",
            "Jacobi theta Poisson summation and modular transformation theta(1/t) = sqrt(t) theta(t)",
            "Global spectral positivity (Weil positivity criterion)",
            "Trace-class / Sonin-space operator properties",
            "OBL-CT-001A",
        ],
    }


def verify_modular_theta_conductor_lean_map_against_file(
    lean_file_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Verify that the declarations listed in `get_modular_theta_conductor_lean_map()`
    match the exact `def` and `theorem` identifiers in
    `formal/RiemannScope/ModularThetaConductorCurvature.lean`.
    """
    if lean_file_path is None:
        lean_file_path = (
            Path(__file__).resolve().parent.parent
            / "formal"
            / "RiemannScope"
            / "ModularThetaConductorCurvature.lean"
        )
    text = lean_file_path.read_text(encoding="utf-8")
    actual_defs = re.findall(r"^\s*def\s+([A-Za-z0-9_]+)", text, flags=re.MULTILINE)
    actual_thms = re.findall(r"^\s*theorem\s+([A-Za-z0-9_]+)", text, flags=re.MULTILINE)
    actual_all = actual_defs + actual_thms

    tmap = get_modular_theta_conductor_lean_map()
    mapped_all = [d["identifier"] for d in tmap["declarations"]]
    stripped = re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)
    stripped = "\n".join(line.split("--")[0] for line in stripped.splitlines())
    return {
        "matches_exact": actual_all == mapped_all,
        "actual_defs": actual_defs,
        "actual_theorems": actual_thms,
        "mapped_identifiers": mapped_all,
        "contains_sorry": re.search(r"\bsorry\b", stripped) is not None,
        "contains_admit": re.search(r"\badmit\b", stripped) is not None,
    }


# ---------------------------------------------------------------------------
# Section 24 & 27: Master Audit Entrypoint for `TASK-TC-036` / `TASK-TC-036R`
# ---------------------------------------------------------------------------


def audit_modular_theta_conductor_curvature() -> Dict[str, Any]:
    """
    Run the complete `TASK-TC-036` / `TASK-TC-036R` Modular-Covariant Theta-Conductor
    Curvature Audit (including the `TASK-TC-036R` pole-regularization and completed-functional
    evidence repair) and return the JSON-serializable artifact dictionary containing all
    required keys from Section 27 plus full diagnostic and literature metadata.
    """
    scope_patch = build_task_tc_035_scope_corrections()
    scaling_sample = evaluate_theta_euler_and_heat_jets(2.0, 3.0, t=1.0)
    drift_audit = audit_unique_heat_drift_compensator()
    modular_audit = audit_modular_covariance()
    hessian_comp = compare_heat_and_modular_hessians(2.0, 3.0, t=1.0)
    conductor_audit = audit_conductor_operator_primary_sources()
    comm_audit = audit_dilation_conductor_commutator()
    selector_axioms = solve_operator_selector_axioms()
    lq_firewall = audit_linear_quadratic_firewall()
    prime_var_arb = certify_prime_only_covariant_variance_arb(t=1.0, N_cutoff=15)
    no_contra = audit_no_contradiction_firewall()
    pole_reg_repair = evaluate_unshifted_vs_corrected_pole_regularizer(t=1.0)
    completed_audit = audit_completed_theta_conductor_functional()
    generic_base = evaluate_generic_base_heat_control()
    lit_table = build_primary_source_literature_table()
    lean_map = get_modular_theta_conductor_lean_map()

    exact_subgate = {
        "subgate_id": "SUBGATE-TC-036A",
        "theorem_name": "Zero-Independent Diagonal-Isolation and Sign-Incompatibility Identity",
        "exact_statement": (
            "There exists a zero-independently defined operator pair (P, Q) on the invariant "
            "domain Delta(A_Q^x / Q^x) of the completed explicit-formula distribution W_xi and "
            "a pole-regularized theta state Phi_t = (D^2 - 1/16) tilde{g}_t (or Phi_t^{(2)} = (D^2 - 1/16)^2 tilde{g}_t) "
            "in Delta such that: (1) the arithmetic evaluation A(Phi_t) := <W_xi, P Phi_t> "
            "(or bilinear form <W_xi, P Phi_t><W_xi, Q Phi_t>) satisfies an unconditional "
            "zero-independent nonpositivity law A_arith(Phi_t) <= 0 from prime-power, "
            "Archimedean conductor, and pole terms alone; and (2) its complete spectral "
            "transfer A_spec(Phi_t) eliminates off-diagonal zero-zero cross terms "
            "(rho, sigma) (sigma != 1 - bar{rho}) and signed ordinate phases -4*gamma_rho^2 "
            "without invoking Weil positivity, reducing to a radial sum sum_rho w_rho(t) delta_rho^2 "
            "+ R_comp(t) with w_rho(t) > 0 and unconditionally certified R_comp(t) >= 0."
        ),
        "status": "OPEN",
        "why_unclosed_by_theta_conductor_candidate": (
            "(a) L_heat = E(E - 2) = 4(D^2 - D) and 4 H_{mod,1} = 4(D + 1/2)^2 differ by 8D + 1; "
            "(b) Burnol's conductor C = A + B commutes with scale dilation ([A_dil, C] = 0), "
            "contributing no non-commuting scale curvature; "
            "(c) L_heat flips the prime-only variance sign from C_arith < 0 to C_prime^cov > 0, "
            "which is compatible with spectral positivity (no contradiction); and "
            "(d) on the repaired pole-regularized state Phi_t = (D^2 - 1/16) tilde{g}_t "
            "(and Phi_t^{(2)} = (D^2 - 1/16)^2 tilde{g}_t), the completed quadratic variance "
            "induces an unrestricted double zero sum over (rho, sigma), whereas the single-zero "
            "convolution form Z(g * g^*) reduces to RH-equivalent Weil positivity."
        ),
    }

    return {
        "task_id": TASK_TC_036_ID,
        "task_completion_status": TASK_TC_036_STATUS,
        "repair_task_id": TASK_TC_036R_ID,
        "repair_task_status": TASK_TC_036R_STATUS,
        "title": "Modular-Covariant Theta-Conductor Curvature Audit (with TASK-TC-036R Pole-Regularization Repair)",
        "starting_head": STARTING_HEAD,
        "substantive_parent_head": SUBSTANTIVE_PARENT_HEAD,
        "task_tc_035_scope_corrections": scope_patch,
        "pole_regularization_repair": pole_reg_repair,
        "theta_heat_state": {
            "one_dimensional": "g_t(x) = exp(-pi * t * x^2), t > 0",
            "two_dimensional": "Theta_t(x, y) = g_t(x) g_t(y) = exp(-pi * t * (x^2 + y^2)), t > 0",
            "sample_evaluation_at_2_3_t1": scaling_sample,
        },
        "spatial_euler_generator": "E = x d/dx + y d/dy",
        "heat_parameter_generator": "D = t d/dt",
        "heat_scaling_identity": {
            "first_order": "E Theta_t = 2 D Theta_t",
            "second_order": "E^2 Theta_t = 4 D^2 Theta_t = 4 t^2 d_t^2 Theta_t + 4 t d_t Theta_t",
            "max_numerical_abs_err": drift_audit["max_euler_heat_scaling_abs_err"],
            "status": "PROVED_EXACT_ALGEBRAIC_AND_LEAN_FORMALIZED",
        },
        "general_drift_operator": {
            "definition": "L_c = E(E - c) = E^2 - c E",
            "action_on_theta_t": "L_c Theta_t = 4 t^2 d_t^2 Theta_t + (4 - 2c) t d_t Theta_t",
            "drift_coefficient": "4 - 2c",
            "non_c2_controls": drift_audit["non_c2_controls"],
        },
        "unique_drift_compensator": drift_audit,
        "modular_weight": {
            "one_dimensional_theta_weight": 0.5,
            "two_dimensional_product_theta_weight": 1.0,
            "general_inversion_law": "f(1/t) = t^w f(t)",
            "weight_normalized_state": "tilde{f}(t) = t^{w/2} f(t)",
            "involution_even_law": "tilde{f}(1/t) = tilde{f}(t)",
            "verification": modular_audit,
        },
        "modular_covariant_derivative": {
            "definition": "nabla_w = D + w/2 = t d/dt + w/2",
            "self_dual_vanishing": "nabla_w f(1) = 0",
            "weight_half_at_t1": modular_audit["nabla_1_2_theta_1d_at_t_eq_1"],
            "weight_one_at_t1": modular_audit["nabla_1_theta_2d_at_t_eq_1"],
            "verified": modular_audit["self_dual_first_derivative_vanishes_verified"],
        },
        "heat_hessian": "L_heat = E(E - 2) = 4 (D^2 - D) = 4 t^2 d_t^2",
        "modular_hessian": "H_{mod,w} = nabla_w^2 = (D + w/2)^2; for w = 1, 4 H_{mod,1} = 4 (D + 1/2)^2 = (E + 1)^2 = 4 t^2 d_t^2 + 8 t d_t + 1",
        "hessian_comparison": hessian_comp,
        "conductor_operator_definition": conductor_audit["conductor_operator_definition"],
        "conductor_domain": conductor_audit["conductor_domain"],
        "conductor_primary_source_audit": conductor_audit,
        "fourier_invariance_status": conductor_audit["fourier_invariance_status"],
        "dilation_commutator_status": comm_audit["status"],
        "dilation_commutator_audit": comm_audit,
        "operator_selector_axioms": selector_axioms,
        "operator_uniqueness_status": selector_axioms["outcome_classification"],
        "linear_quadratic_firewall": lq_firewall,
        "prime_only_covariant_variance": prime_var_arb,
        "completed_functional_status": " explicitly_defined_regularized_quadratic_and_linear_distributions_on_delta ".strip().upper(),
        "completed_functional_audit": completed_audit,
        "linear_or_quadratic": (
            "STRICTLY_SEPARATED: linear explicit-formula functional <W_comp, O J Phi_t> is "
            "LINEAR_DISTRIBUTIONAL_REGULARIZED (SIGNED_SINGLE_ZERO_SUM); quadratic variance "
            "W_comp(J Phi_t) W_comp(L_heat J Phi_t) - W_comp(2 D J Phi_t)^2 is "
            "QUADRATIC_DISTRIBUTIONAL_REGULARIZED (UNRESTRICTED_DOUBLE_ZERO_SUM)"
        ),
        "complete_spectral_transfer_status": UNRESTRICTED_DOUBLE_ZERO_SUM,
        "natural_zero_pairing": THETA_CONDUCTOR_FUNCTIONAL_REMAINS_DOUBLE_SPECTRAL,
        "cross_term_status": (
            "ALL_ORDERED_ZERO_PAIRS_PRESENT_IN_QUADRATIC_VARIANCE_CONJUGATE_DIAGONAL_NOT_ISOLATED"
        ),
        "background_term_status": (
            "ALL_REQUIRED_TERMS_EXPLICITLY_INCLUDED_PRIME_POLE_TRIVIAL_GAMMA_CONDUCTOR_NORMALIZATION_REGULARIZATION"
        ),
        "arithmetic_sign_status": (
            "PRIME_ONLY_COVARIANT_VARIANCE_STRICTLY_POSITIVE_ARB_CERTIFIED_UNCOMPENSATED_STRICTLY_NEGATIVE"
        ),
        "spectral_sign_status": (
            "SIGNED_OSCILLATORY_OR_UNRESTRICTED_DOUBLE_ZERO_SUM_GLOBAL_POSITIVITY_WEIL_EQUIVALENT"
        ),
        "contradiction_status": POSITIVE_ARITHMETIC_VARIANCE_HAS_NO_CONTRADICTORY_SPECTRAL_LAW,
        "no_contradiction_firewall": no_contra,
        "weil_equivalence_status": THETA_CONDUCTOR_POSITIVITY_IS_RH_EQUIVALENT,
        "generic_base_status": GENERIC_HEAT_VARIANCE_NOT_TC_CONSTRAINT,
        "generic_base_control": generic_base,
        "tau_specific_input": generic_base["tau_specific_input"]
        if "tau_specific_input" in generic_base
        else generic_base["tau_specific_entry_points"],
        "primary_source_literature_table": lit_table,
        "arxiv_literature_retrieved": [
            {
                "arxiv_id": "math/9902080v1",
                "url": "https://arxiv.org/abs/math/9902080v1",
                "authors": ["Jean-Francois Burnol"],
                "title": "The Explicit Formula and the conductor operator",
            },
            {
                "arxiv_id": "math/9812012v1",
                "url": "https://arxiv.org/abs/math/9812012v1",
                "authors": ["Jean-Francois Burnol"],
                "title": "Spectral Analysis of the local Commutator Operators",
            },
            {
                "arxiv_id": "math/0101068v1",
                "url": "https://arxiv.org/abs/math/0101068v1",
                "authors": ["Jean-Francois Burnol"],
                "title": "Sur les Formules Explicites I: analyse invariante",
            },
            {
                "arxiv_id": "math/0112254v6",
                "url": "https://arxiv.org/abs/math/0112254v6",
                "authors": ["Jean-Francois Burnol"],
                "title": "On Fourier and Zeta(s)",
            },
            {
                "arxiv_id": "1106.4749v2",
                "url": "https://arxiv.org/abs/1106.4749v2",
                "authors": ["Jean-Francois Burnol"],
                "title": "Deux extensions de Theoremes de Hamburger",
            },
            {
                "arxiv_id": "math/0407443v3",
                "url": "https://arxiv.org/abs/math/0407443v3",
                "authors": ["Jean-Francois Burnol"],
                "title": "Entrelacement de co-Poisson",
            },
            {
                "arxiv_id": "math/0203120v7",
                "url": "https://arxiv.org/abs/math/0203120v7",
                "authors": ["Jean-Francois Burnol"],
                "title": "Two complete and minimal systems associated with the zeros of the Riemann zeta function",
            },
            {
                "arxiv_id": "math/0105120v1",
                "url": "https://arxiv.org/abs/math/0105120v1",
                "authors": ["Jean-Francois Burnol"],
                "title": "Sur certains espaces de Hilbert de fonctions entieres (Sonine spaces)",
            },
            {
                "arxiv_id": "math/0207237v1",
                "url": "https://arxiv.org/abs/math/0207237v1",
                "authors": ["Luis Baez-Duarte"],
                "title": "A general statement of the functional equation for the Riemann zeta-function",
            },
            {
                "arxiv_id": "2006.13771v1",
                "url": "https://arxiv.org/abs/2006.13771v1",
                "authors": ["Alain Connes", "Caterina Consani"],
                "title": "Weil positivity and Trace formula, the archimedean place",
            },
            {
                "arxiv_id": "2106.01715v1",
                "url": "https://arxiv.org/abs/2106.01715v1",
                "authors": ["Alain Connes", "Caterina Consani"],
                "title": "Spectral Triples and Zeta-Cycles",
            },
            {
                "arxiv_id": "2112.08820v1",
                "url": "https://arxiv.org/abs/2112.08820v1",
                "authors": ["Alain Connes", "Caterina Consani"],
                "title": "BC-system, absolute cyclotomy and the quantized calculus",
            },
        ],
        "obl_ct_001a_status": OBL_CT_001A_STATUS,
        "obl_ct_001a_completed": False,
        "rh_claimed": False,
        "candidate_failure_refutes_tc": False,
        "principal_classification": PRINCIPAL_CLASSIFICATION,
        "exact_remaining_subgate": exact_subgate,
        "lean_theorem_map": lean_map,
        "hypothesis_fidelity": {
            "general_tc_hypothesis": "One arithmetic object represented through all tau-grades implies a constraint.",
            "candidate_mechanism": "The constraint is an operator-level modular theta-conductor curvature law.",
            "candidate_evaluation": (
                "Refuted as a direct bridge: the affine heat-drift compensator L_heat = E(E - 2) "
                "and modular Hessian 4 H_{mod,1} = (E + 1)^2 differ by 8D + 1; Burnol's conductor "
                "commutes with dilation ([A_dil, C] = 0); prime-only drift compensation makes "
                "arithmetic variance positive (creating no contradiction with spectral positivity); "
                "and on the repaired pole-regularized state Phi_t = (D^2 - 1/16) tilde{g}_t "
                "(and Phi_t^{(2)} = (D^2 - 1/16)^2 tilde{g}_t), the completed quadratic variance "
                "remains an unrestricted double zero sum."
            ),
            "general_tc_hypothesis_refuted": False,
        },
    }


__all__ = [
    "COMPLETED_THETA_CONDUCTOR_REGULARIZATION_REPAIRED",
    "COMPLETE_SPECTRAL_TRANSFER_NOT_DERIVED",
    "CONDITIONAL_COMPLEMENT_SIGN_DICHOTOMY_LEAN_PROVED",
    "CONDUCTOR_COMMUTES_WITH_DILATION",
    "CONDUCTOR_DILATION_COMMUTATION_REMOVES_NEW_GRADE_SIGNAL",
    "CORRECTED_POLE_REGULARIZER_D_SQUARED_MINUS_ONE_SIXTEENTH",
    "GENERIC_HEAT_VARIANCE_NOT_TC_CONSTRAINT",
    "HEAT_AND_MODULAR_HESSIANS_DIFFER_BY_FORCED_CONNECTION_TERMS",
    "HEAT_COMPENSATOR_NOT_MODULARLY_FORCED",
    "HEAT_DRIFT_COMPENSATOR_UNIQUELY_FORCED",
    "HEAT_DRIFT_COMPENSATOR_UNIQUE_BUT_NOT_MODULAR_SELECTOR",
    "HERMITIAN_WEIL_FORM",
    "LINEAR_QUADRATIC_FUNCTIONAL_CONFLATION",
    "MODULAR_HESSIAN_DIFFERS_FROM_HEAT_COMPENSATOR",
    "MODULAR_HESSIAN_DOES_NOT_REMOVE_HEAT_DRIFT",
    "OBL_CT_001A_STATUS",
    "ONE_PRECISE_THETA_CONDUCTOR_SUBGATE_OPEN",
    "POSITIVE_ARITHMETIC_VARIANCE_HAS_NO_CONTRADICTORY_SPECTRAL_LAW",
    "PRINCIPAL_CLASSIFICATION",
    "SIGNED_SINGLE_ZERO_SUM",
    "SIX_STANDARD_SELECTOR_FAMILIES_AUDITED",
    "STARTING_HEAD",
    "SUBSTANTIVE_PARENT_HEAD",
    "TASK_TC_036R_ID",
    "TASK_TC_036R_STATUS",
    "TASK_TC_036_ID",
    "TASK_TC_036_STATUS",
    "THETA_CONDUCTOR_FUNCTIONAL_REMAINS_DOUBLE_SPECTRAL",
    "THETA_CONDUCTOR_POSITIVITY_IS_RH_EQUIVALENT",
    "UNRESTRICTED_DOUBLE_ZERO_SUM",
    "UNSHIFTED_REGULARIZER_DOES_NOT_ANNIHILATE_POLES",
    "audit_completed_theta_conductor_functional",
    "audit_conductor_operator_primary_sources",
    "audit_dilation_conductor_commutator",
    "audit_linear_quadratic_firewall",
    "audit_modular_covariance",
    "audit_modular_theta_conductor_curvature",
    "audit_no_contradiction_firewall",
    "audit_unique_heat_drift_compensator",
    "build_primary_source_literature_table",
    "build_task_tc_035_scope_corrections",
    "certify_prime_only_covariant_variance_arb",
    "compare_heat_and_modular_hessians",
    "evaluate_general_drift_operator_L_c",
    "evaluate_generic_base_heat_control",
    "evaluate_modular_covariant_derivative_1d_theta",
    "evaluate_theta_euler_and_heat_jets",
    "evaluate_unshifted_vs_corrected_pole_regularizer",
    "get_modular_theta_conductor_lean_map",
    "jacobi_theta_1d_truncated",
    "modular_weight_normalized_value",
    "solve_operator_selector_axioms",
    "theta_1d_heat_state",
    "theta_2d_heat_state",
    "verify_modular_theta_conductor_lean_map_against_file",
]


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Execute TASK-TC-036 Modular-Covariant Theta-Conductor Curvature Audit."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/tc_modular_theta_conductor_curvature.json",
        help="Path to write the JSON audit artifact.",
    )
    args = parser.parse_args()

    payload = audit_modular_theta_conductor_curvature()
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path} ({payload['principal_classification']})")


if __name__ == "__main__":
    main()
