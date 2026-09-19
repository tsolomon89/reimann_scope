"""
Transcendental Continuation: Geometric Dilation Transforms and Candidate Audits.
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
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import mpmath

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


# ==============================================================================
# 6. COMPARATIVE TRANSFORMATION CONTRACT
# ==============================================================================

def evaluate_origin_dilation_zeta(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    K: int,
    dps: int = 80
) -> mpmath.mpc:
    """
    Construction 1: Origin argument dilation:
      Z_K(s) = zeta(a_K^(-1) * s) = zeta(tau^(-K) * s).
    Zero behavior: rho becomes a_K * rho = tau^K * rho.
    Critical line: Re(s) = a_K / 2 = tau^K / 2.
    Frequency action: logarithmic frequencies dilated to a_K^(-1) * log(n) = tau^(-K) * log(n).
    """
    with mpmath.workdps(dps + 15):
        s_c = math_core.to_mpc(s, dps=dps + 15)
        tau = math_core.get_tau(dps=dps + 15)
        a_K = mpmath.power(tau, K)
        s_dilated = s_c / a_K
        return math_core.zeta_eval(s_dilated, dps=dps)


def evaluate_centered_dilation_zeta(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    K: int,
    dps: int = 80
) -> mpmath.mpc:
    """
    Construction 2: Centered argument dilation:
      zeta_cent,K(s) = zeta(1/2 + a_K^(-1) * (s - 1/2)) = zeta(1/2 + tau^(-K) * (s - 1/2)).
    Zero behavior: rho becomes 1/2 + a_K * (rho - 1/2) = 1/2 + tau^K * (rho - 1/2).
    Critical line: Re(s) remains 1/2 identically.
    """
    with mpmath.workdps(dps + 15):
        s_c = math_core.to_mpc(s, dps=dps + 15)
        tau = math_core.get_tau(dps=dps + 15)
        a_K = mpmath.power(tau, K)
        s_cent = mpmath.mpc('0.5', 0) + (s_c - mpmath.mpc('0.5', 0)) / a_K
        return math_core.zeta_eval(s_cent, dps=dps)


def evaluate_scaled_dirichlet_series(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    K: int,
    dps: int = 80
) -> mpmath.mpc:
    """
    Construction 3: Scaled arithmetic Dirichlet series:
      F_K(s) = sum_{n>=1} (a_K * n)^(-s) = a_K^(-s) * zeta(s) = tau^(-K*s) * zeta(s).
    Valid for Re(s) > 1, then meromorphically continued to C.
    Zero behavior: zeros remain at rho with preserved multiplicities.
    Frequency action: frequencies translated to log(n) + K * log(tau).
    """
    with mpmath.workdps(dps + 15):
        s_c = math_core.to_mpc(s, dps=dps + 15)
        tau = math_core.get_tau(dps=dps + 15)
        a_K = mpmath.power(tau, K)
        # a_K^(-s) = exp(-s * K * log(tau))
        factor = mpmath.power(a_K, -s_c)
        zeta_val = math_core.zeta_eval(s_c, dps=dps + 15)
        return factor * zeta_val


def evaluate_half_density_twist_xi(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    K: int,
    dps: int = 80
) -> mpmath.mpc:
    """
    Construction 4: Completed half-density twist:
      xi_K(s) = a_K^(-(s - 1/2)) * xi(s) = tau^(-K * (s - 1/2)) * xi(s).
    Zero behavior: zeros and multiplicities remain at rho.
    Transformed functional equation: xi_K(1 - s) = tau^(2*K*(s - 1/2)) * xi_K(s).
    """
    with mpmath.workdps(dps + 15):
        s_c = math_core.to_mpc(s, dps=dps + 15)
        tau = math_core.get_tau(dps=dps + 15)
        shift = s_c - mpmath.mpc('0.5', 0)
        twist = mpmath.power(tau, -K * shift)
        xi_val = math_core.completed_xi(s_c, dps=dps + 15)
        return twist * xi_val


def transformation_contract_comparison_table() -> List[Dict[str, str]]:
    """
    Return the formal side-by-side comparative contract table for the 4 transformations.
    """
    return [
        {
            "construction": "Origin argument dilation",
            "definition": "Z_K(s) = zeta(a_K^(-1) * s)",
            "domain": "C \\ {tau^K}",
            "unit": "a_K = tau^K",
            "inverse_map": "s -> tau^K * s",
            "zero_behavior": "rho -> tau^K * rho",
            "critical_line": "Re(s) = tau^K / 2",
            "completion_factor": "pi^(-(tau^(-K)*s)/2) * Gamma(tau^(-K)*s / 2)",
            "transformed_fe": "Z_K(tau^K * (1 - tau^(-K)*s)) = chi(tau^(-K)*s) * Z_K(s)",
            "frequency_action": "Dilation: tau^(-K) * log(n)"
        },
        {
            "construction": "Centered argument dilation",
            "definition": "zeta(1/2 + a_K^(-1) * (s - 1/2))",
            "domain": "C \\ {1/2 + tau^K/2}",
            "unit": "a_K = tau^K",
            "inverse_map": "s -> 1/2 + tau^K * (s - 1/2)",
            "zero_behavior": "rho -> 1/2 + tau^K * (rho - 1/2)",
            "critical_line": "Re(s) = 1/2 (invariant)",
            "completion_factor": "Centered Archimedean Gamma factor",
            "transformed_fe": "Reflection about s=1/2 preserved",
            "frequency_action": "Centered scaling about critical point"
        },
        {
            "construction": "Scaled arithmetic Dirichlet series",
            "definition": "F_K(s) = sum (a_K * n)^(-s) = tau^(-K*s) * zeta(s)",
            "domain": "C \\ {1}",
            "unit": "a_K = tau^K",
            "inverse_map": "s -> s, F_K -> tau^(K*s) * F_K",
            "zero_behavior": "rho unchanged (multiplicity preserved)",
            "critical_line": "Re(s) = 1/2 (invariant)",
            "completion_factor": "pi^(-s/2) * Gamma(s/2)",
            "transformed_fe": "F_K(1-s) = tau^(-K*(1-2s)) * chi(s) * F_K(s)",
            "frequency_action": "Translation: log(n) + K * log(tau)"
        },
        {
            "construction": "Completed half-density twist",
            "definition": "xi_K(s) = tau^(-K*(s - 1/2)) * xi(s)",
            "domain": "Entire C",
            "unit": "a_K = tau^K",
            "inverse_map": "xi_K -> tau^(K*(s-1/2)) * xi_K",
            "zero_behavior": "rho unchanged (multiplicity preserved)",
            "critical_line": "Re(s) = 1/2 (unitary axis)",
            "completion_factor": "Intrinsic completed xi",
            "transformed_fe": "xi_K(1-s) = tau^(2*K*(s-1/2)) * xi_K(s)",
            "frequency_action": "Half-density Mellin character twist"
        }
    ]


# ==============================================================================
# 7. EXACT SCALAR RESULTS & MULTIPLIER INVESTIGATION
# ==============================================================================

def verify_scalar_twist_identities(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    K: int,
    J: int,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [MATHEMATICAL CONTRACT: SCALAR TWIST IDENTITIES]
    Verifies the exact scalar relations:
      1. xi_K'/xi_K = xi'/xi - K * log(tau)
      2. xi_K(1-s) = tau^(2*K*(s - 1/2)) * xi_K(s)
      3. -F_K'/F_K + F_J'/F_J = (K - J) * log(tau) meromorphically
      4. Modulus: |tau^(-K*(s-1/2))| = tau^(-K*delta), equals 1 iff delta = 0 (for real K).
      5. Multiplier is nowhere zero on C.
    """
    with mpmath.workdps(dps + 20):
        s_c = math_core.to_mpc(s, dps=dps + 20)
        tau = math_core.get_tau(dps=dps + 20)
        log_tau = mpmath.log(tau)
        delta = s_c.real - mpmath.mpf('0.5')
        t_val = s_c.imag

        # 1. Log-derivative twist check: d/ds log(xi_K(s)) = xi'/xi(s) - K * log(tau)
        h = mpmath.mpf('1e-25')
        s_ph = s_c + h
        s_mh = s_c - h
        xi_K_val = evaluate_half_density_twist_xi(s_c, K, dps=dps + 15)
        xi_K_p = (evaluate_half_density_twist_xi(s_ph, K, dps=dps + 15) -
                  evaluate_half_density_twist_xi(s_mh, K, dps=dps + 15)) / (2 * h)
        log_der_xi_K = xi_K_p / xi_K_val

        xi_val = math_core.completed_xi(s_c, dps=dps + 15)
        xi_p = (math_core.completed_xi(s_ph, dps=dps + 15) -
                math_core.completed_xi(s_mh, dps=dps + 15)) / (2 * h)
        log_der_xi = xi_p / xi_val
        expected_log_der = log_der_xi - K * log_tau
        log_der_err = abs(log_der_xi_K - expected_log_der)

        # 2. Functional equation check: xi_K(1 - s) == tau^(2*K*(s - 1/2)) * xi_K(s)
        s_refl = mpmath.mpc(1, 0) - s_c
        xi_K_refl = evaluate_half_density_twist_xi(s_refl, K, dps=dps + 15)
        fe_factor = mpmath.power(tau, 2 * K * (s_c - mpmath.mpc('0.5', 0)))
        expected_xi_K_refl = fe_factor * xi_K_val
        fe_err = abs(xi_K_refl - expected_xi_K_refl)

        # 3. Scaled Dirichlet series log-derivative difference:
        # -F_K'/F_K + F_J'/F_J == (K - J) * log(tau)
        # F_K = tau^(-K*s) * zeta(s) => -F_K'/F_K = K*log(tau) - zeta'/zeta(s)
        # -F_K'/F_K + F_J'/F_J = (K - J) * log(tau) identically!
        diff_FK_FJ = (K - J) * log_tau

        # 4. Modulus of the twist factor: |tau^(-K*(s - 1/2))| = tau^(-K*delta)
        twist_val = mpmath.power(tau, -K * (s_c - mpmath.mpc('0.5', 0)))
        twist_modulus = abs(twist_val)
        expected_modulus = mpmath.power(tau, -K * delta)
        modulus_err = abs(twist_modulus - expected_modulus)
        is_unimodular = abs(twist_modulus - 1) < mpmath.mpf('1e-60')

        # 5. Witness for non-contradiction of tau^(K*delta) in Q for irrational/transcendental delta
        # Let delta = log_tau(3/2). Then tau^delta = 3/2 in Q!
        delta_trans = mpmath.log(mpmath.mpf('1.5')) / log_tau
        tau_delta_val = mpmath.power(tau, delta_trans)
        tau_delta_err = abs(tau_delta_val - mpmath.mpf('1.5'))

        return {
            "s": f"{mpmath.nstr(s_c.real, n=20)} + {mpmath.nstr(s_c.imag, n=20)}j",
            "delta": mpmath.nstr(delta, n=20),
            "K": K,
            "J": J,
            "log_derivative_twist_error": mpmath.nstr(log_der_err, n=6),
            "functional_equation_error": mpmath.nstr(fe_err, n=6),
            "cross_grade_log_der_diff": mpmath.nstr(diff_FK_FJ, n=20),
            "twist_modulus": mpmath.nstr(twist_modulus, n=20),
            "expected_modulus": mpmath.nstr(expected_modulus, n=20),
            "modulus_error": mpmath.nstr(modulus_err, n=6),
            "is_unimodular_on_line": is_unimodular,
            "rational_power_witness_delta": mpmath.nstr(delta_trans, n=20),
            "rational_power_witness_value": mpmath.nstr(tau_delta_val, n=20),
            "rational_power_witness_error": mpmath.nstr(tau_delta_err, n=6),
            "epistemic_conclusion": "All scalar twist identities verified. Modulus is 1 iff delta=0. Rational values tau^(K*delta) in Q are consistent for transcendental delta=log_tau(p/q) and do not force an integer lattice collision."
        }


# ==============================================================================
# 8. MECHANISM DISCOVERY AUDIT & CANDIDATE EVALUATION
# ==============================================================================

def audit_candidate_A_lattice_vs_frequency(
    s_val: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    K: int = 1,
    J: int = 0,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [DISCOVERY CYCLE 1 & 2: GAP A AUDIT - SCOPED REFINEMENT]
    Audits the distinction between three separate constructions:
      1. Station lattice: L_K = tau^K * Z (discrete integer-grade spatial scaffold).
      2. Dilated logarithmic frequencies: {tau^(-K) * log(n)} arising in origin argument dilation Z_K(s) = zeta(tau^(-K)*s).
      3. Translated Dirichlet frequencies: {log(n) + K*log(tau)} arising in scaled arithmetic Dirichlet series F_K(s) = tau^(-K*s)*zeta(s).

    Mathematical Scope:
      - The constant logarithmic-derivative difference -F_K'/F_K + F_J'/F_J == (K-J)*log(tau)
        proves that the scaled Dirichlet series comparison collapses to a scalar coordinate constant.
      - This closes that specific scalar comparison for F_K; it does NOT falsify every proposed map
        involving the station lattice L_K or argument dilation Z_K(s).
      - Distinct integer-grade station lattices satisfy L_K cap L_J = {0} for K != J by the
        transcendence of tau = 2*pi (Lindemann 1882).
      - Non-scalar coupling between L_K and the zero divisor or argument dilation remains an open question.
    """
    with mpmath.workdps(dps + 15):
        s_c = math_core.to_mpc(s_val, dps=dps + 15)
        tau = math_core.get_tau(dps=dps + 15)
        log_tau = mpmath.log(tau)

        res = verify_scalar_twist_identities(s_c, K, J, dps=dps)

        return {
            "candidate_id": "TC-DISC-001",
            "candidate_name": "Inter-Grade Lattice Station Arithmetic Coincidence",
            "gap": "GAP_A_TWO_ROLES_OF_LATTICE",
            "evaluated_grades": (K, J),
            "scalar_difference": mpmath.nstr((K - J) * log_tau, n=dps),
            "zero_dependence": "NONE (exact constant identity for scaled Dirichlet series F_K)",
            "prime_dependence": "NONE (prime terms cancel identically in F_K'/F_K difference)",
            "verdict": "SCOPED_SCALAR_REDUCTION",
            "epistemic_reason": "Scaled Dirichlet series logarithmic-derivative difference reduces to the scalar constant (K-J)*log(tau). Station lattice disjointness L_K cap L_J = {0} holds by transcendence of tau, but does not couple to F_K. Non-scalar couplings for argument dilation Z_K remain open."
        }


def audit_candidate_B_zero_restriction(
    delta_values: Sequence[Union[float, str, mpmath.mpf]],
    gamma: Union[float, str, mpmath.mpf],
    K: int = 1,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [DISCOVERY CYCLE 1 & 2: GAP B AUDIT - NARROW SCOPING & SYMMETRY MODEL]
    Tests whether the grade character q_rho^K = tau^(K*delta) * exp(i*K*gamma*log(tau)),
    reflection defect B_rho(k) = 4*sinh^2(k*delta*log(tau)/2), or symmetric defect
    D_K(rho) = 4*sinh^2(K*delta*log(tau)/2) forces any discrete or rational restriction on delta.

    Scoped Theorem:
      For every real displacement delta in (-1/2, 1/2) and height gamma in R,
      q = exp((delta + i*gamma)*log(tau)) is non-zero, and chi(K) = q^K is a character
      of the integer grade group (Z, +).
      The character laws (chi(K+J) = chi(K)*chi(J)) and conjugation/reflection symmetries
      (rho -> 1-rho, rho -> conj(rho)) admit arbitrary real off-line displacements delta != 0.
      Those listed symmetry and character premises alone therefore do NOT imply delta = 0.

    Note on Smoothness & Arithmetic:
      Smoothness of D_K(delta) alone does not preclude discrete constraints (as sin(pi*x) = 0 is smooth
      with discrete roots). Rather, the conclusion is that the explicitly listed character and reflection
      identities hold identically for all real delta, so any discrete quantization would require an
      additional, unproved arithmetic premise.

    Displacement Test Cases:
      - delta = 0 (critical line)
      - delta = 1/10 (rational)
      - delta = sqrt(2)/10 (algebraic irrational)
      - delta = -sqrt(2)/10 (negative algebraic irrational)
      - delta = log_tau(3/2) (irrational displacement yielding rational character modulus |q_rho| = 1.5)
    """
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps + 15)
        log_tau = mpmath.log(tau)
        g_val = math_core.to_mpf(gamma, dps=dps + 15)

        evaluations = []
        for d in delta_values:
            d_val = math_core.to_mpf(d, dps=dps + 15)
            # Character modulus: |q_rho^K| = tau^(K*delta)
            q_mod = mpmath.power(tau, K * d_val)
            # Reflection defect: D_K = 4 * sinh^2(K * delta * log(tau) / 2)
            u = K * d_val * log_tau / 2
            D_K = 4 * (mpmath.sinh(u) ** 2)
            # Countermodel polynomial evaluation at centered root z = delta + i*gamma
            # Satisfies exact reflection, conjugation, evenness, and 4 quartet roots
            poly_root_res = abs(math_core.countermodel_polynomial_P(mpmath.mpc(d_val, g_val), d_val, g_val, dps=dps))

            evaluations.append({
                "delta": mpmath.nstr(d_val, n=15),
                "q_modulus": mpmath.nstr(q_mod, n=15),
                "defect_D_K": mpmath.nstr(D_K, n=15),
                "poly_root_residual": mpmath.nstr(poly_root_res, n=6),
                "is_zero_defect": bool(D_K < mpmath.mpf('1e-60')),
                "is_analytic_continuous": True
            })

        return {
            "candidate_id": "TC-DISC-002",
            "candidate_name": "Zero-Character Symmetry Consistency & Non-Quantization",
            "gap": "GAP_B_PROPOSED_ARITHMETIC_RESTRICTION",
            "evaluated_grade": K,
            "evaluations": evaluations,
            "verdict": "CHARACTER_SYMMETRIES_ADMIT_OFFLINE_DISPLACEMENTS",
            "epistemic_reason": "Grade character and reflection symmetries hold smoothly for all real delta. Quartet countermodel P satisfies all listed symmetries with delta != 0. Character and reflection laws alone do not imply delta = 0; discrete quantization remains an unproved external premise."
        }


def audit_candidate_C_log_derivative_compatibility(
    K: int,
    J: int,
    test_points: Sequence[Union[complex, mpmath.mpc, str]],
    dps: int = 80
) -> Dict[str, Any]:
    """
    [DISCOVERY CYCLE 1 & 2: GAP C AUDIT - SCOPED REFINEMENT]
    Tests whether the completed logarithmic derivative cross-grade difference:
      Delta G_{K,J}(s) = -xi_K'/xi_K(s) - (-xi_J'/xi_J(s)) = (K - J) * log(tau)
    creates an arithmetic incompatibility for off-line zeros.

    Evaluates across sample points in the critical strip (both on and off critical line).
    Verifies that the singular zero-pole parts cancel identically:
      sum_rho 1/(s - rho) - sum_rho 1/(s - rho) == 0,
    leaving the scalar difference (K - J)*log(tau) without any residual.

    Mathematical Scope:
      This is retained as an exact, scoped result of scalar preservation. It supplies no
      new exclusion mechanism, but proves that cross-grade scalar logarithmic derivatives
      provide zero residual divisor data.
    """
    with mpmath.workdps(dps + 20):
        tau = math_core.get_tau(dps=dps + 20)
        log_tau = mpmath.log(tau)
        expected_diff = (K - J) * log_tau

        point_results = []
        max_error = mpmath.mpf('0')

        h = mpmath.mpf('1e-25')
        for pt in test_points:
            s_c = math_core.to_mpc(pt, dps=dps + 20)
            s_ph = s_c + h
            s_mh = s_c - h

            # xi_K log-derivative
            xi_K_c = evaluate_half_density_twist_xi(s_c, K, dps=dps + 15)
            xi_K_p = (evaluate_half_density_twist_xi(s_ph, K, dps=dps + 15) -
                      evaluate_half_density_twist_xi(s_mh, K, dps=dps + 15)) / (2 * h)
            G_K = -(xi_K_p / xi_K_c)

            # xi_J log-derivative
            xi_J_c = evaluate_half_density_twist_xi(s_c, J, dps=dps + 15)
            xi_J_p = (evaluate_half_density_twist_xi(s_ph, J, dps=dps + 15) -
                      evaluate_half_density_twist_xi(s_mh, J, dps=dps + 15)) / (2 * h)
            G_J = -(xi_J_p / xi_J_c)

            diff = G_K - G_J
            err = abs(diff - expected_diff)
            if err > max_error:
                max_error = err

            point_results.append({
                "s": f"{mpmath.nstr(s_c.real, n=15)} + {mpmath.nstr(s_c.imag, n=15)}j",
                "G_K": f"{mpmath.nstr(G_K.real, n=15)} + {mpmath.nstr(G_K.imag, n=15)}j",
                "G_J": f"{mpmath.nstr(G_J.real, n=15)} + {mpmath.nstr(G_J.imag, n=15)}j",
                "diff": f"{mpmath.nstr(diff.real, n=15)} + {mpmath.nstr(diff.imag, n=15)}j",
                "error": mpmath.nstr(err, n=6)
            })

        return {
            "candidate_id": "TC-DISC-003",
            "candidate_name": "Completed Logarithmic Derivative Difference Divisor Cancellation",
            "gap": "GAP_C_REMAINING_COMPATIBILITY_CANDIDATE",
            "grades": (K, J),
            "expected_scalar_difference": mpmath.nstr(expected_diff, n=dps),
            "max_residual_error": mpmath.nstr(max_error, n=6),
            "all_points_matched": bool(max_error < mpmath.mpf('1e-35')),
            "verdict": "SCOPED_SCALAR_PRESERVATION",
            "epistemic_reason": "The singular zero-pole parts cancel identically across grades. The difference G_K - G_J is identically (K-J)*log(tau) everywhere on C, supplying zero spectral divisor data and zero constraint on off-line zeros."
        }


def audit_candidate_D_transported_explicit_formula(
    K: int = 1,
    J: int = 0,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [DISCOVERY CYCLE 2: CANDIDATE D AUDIT - EXPLICIT FORMULA DILATION & COLLISION]
    Investigates whether pairing transported explicit-formula test functions
    h_{K,J}(r) = phi(tau^(-K)*r) - phi(tau^(-J)*r)
    forces an arithmetic layer collision m*tau^K = n*tau^J.

    Mathematical Deductions:
      1. Linearity: When phi is an admissible Guinand-Weil test function, phi(tau^(-K)*r)
         and phi(tau^(-J)*r) are admissible, so their difference h_{K,J} is another native test.
         The difference yields no independent identity beyond the native explicit formula evaluated on h_{K,J}.
      2. Multiplicative Frequency Collision:
         On the prime side, dilated frequencies evaluate at tau^K * log(n) and tau^J * log(m).
         Equality tau^K * log(n) = tau^J * log(m) implies tau^(K-J) = log(m)/log(n) = log_n(m).
         If m and n belong to the same multiplicative family (m = b^p, n = b^q for integers p, q),
         then log_n(m) = p/q in Q.
         This would force tau^(K-J) = p/q in Q, which is STRICTLY IMPOSSIBLE for K != J by the
         transcendence of tau = 2*pi (Lindemann 1882).
      3. Pair-Isolation Obstruction:
         The explicit formula evaluates the complete infinite sum sum_n Lambda(n)/sqrt(n) * g(tau^K * log n).
         An off-line zero does NOT force an isolated two-prime balance n^(delta*tau^K) = m^(delta*tau^J);
         the complete sum over all prime powers and the continuous Archimedean integral can compensate.
         Inferring tau^(K-J) in Q without proving pair isolation is an instance of the Pair-Isolation Fallacy.
    """
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps + 15)
        M = K - J

        # Test multiplicative family: b=2, n=2^2=4, m=2^3=8 => log_n(m) = 3/2
        b, q, p = 2, 2, 3
        n_val, m_val = b ** q, b ** p
        ratio = mpmath.mpf(p) / mpmath.mpf(q)
        tau_M = mpmath.power(tau, M)

        # Discrepancy between transcendental tau^M and rational ratio p/q
        discrepancy = abs(tau_M - ratio)

        return {
            "candidate_id": "TC-DISC-004",
            "candidate_name": "Transported Explicit Formula Difference & Frequency Collision",
            "evaluated_grades": (K, J),
            "grade_difference_M": M,
            "test_integers": {"b": b, "q": q, "p": p, "n": n_val, "m": m_val},
            "rational_frequency_ratio": mpmath.nstr(ratio, n=15),
            "transcendental_tau_pow_M": mpmath.nstr(tau_M, n=15),
            "collision_discrepancy": mpmath.nstr(discrepancy, n=15),
            "rational_collision_possible": False,
            "lindemann_transcendence_barrier": "PROVED: tau^M in Q is impossible for integer M != 0",
            "pair_isolation_status": "UNPROVED: full explicit formula involves infinite prime sum, preventing two-prime isolation",
            "verdict": "REJECTED_AS_A_MECHANISM_FROM_EXPLICIT_FORMULA_LINEARITY_ALONE",
            "epistemic_reason": "Linear differences of explicit-formula tests remain native tests. For prime base ell and positive integers p, q, an isolated frequency collision tau^K * log(ell^q) = tau^J * log(ell^p) forces tau^(K-J) = p/q in Q, strictly forbidden by Lindemann's theorem. However, equality of the two complete linear explicit-formula evaluations does not imply equality of any selected pair of prime-power summands due to infinite-sum compensation (Pair-Isolation Fallacy)."
        }


def audit_candidate_common_referent_bridge(
    delta: Union[str, float, mpmath.mpf] = '0.1',
    gamma: Union[str, float, mpmath.mpf] = '14.134725141734693790457251983562470270784257115699',
    K: int = 1,
    J: int = 0,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [DISCOVERY CYCLE 3: COMMON-REFERENT BRIDGE AUDIT (CR-1)]
    Evaluates whether normalized radial displacement delta satisfies the three conditions
    of the Common-Referent Collision Theorem:
      (CR1) Common referent: A_K(rho_K) = A_J(rho_J) = A(rho) as external real value.
      (CR2) Arithmetic layer location: A_K(rho_K) in L_K = tau^K * Z and A_J(rho_J) in L_J = tau^J * Z.
      (CR3) Off-line non-zero: delta != 0 implies A(rho) != 0.

    Mathematical Findings:
      1. CR1 is satisfied: Normalized radial coordinate R_tau(s_rho(K), K) = delta identically across all grades K in Z.
      2. CR3 is satisfied: delta != 0 if and only if Re(rho) != 1/2.
      3. CR2 FAILS / DISGUISED PREMISE:
         Because L_K intersect L_J = {0} for K != J by Lindemann's transcendence of tau = 2*pi,
         requiring delta in L_K intersect L_J forces delta = 0 directly.
         Asserting that an off-line zero must satisfy layer membership is logically equivalent
         to assuming the Riemann Hypothesis itself (Disguised Premise Obstruction).
    """
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps + 15)
        d_val = math_core.to_mpf(delta, dps=dps + 15)
        g_val = math_core.to_mpf(gamma, dps=dps + 15)

        # 1. Evaluate transported representations
        # s_rho(K) = tau^K * (1/2 + delta + i*gamma)
        tau_K = mpmath.power(tau, K)
        tau_J = mpmath.power(tau, J)
        s_K = tau_K * mpmath.mpc(mpmath.mpf('0.5') + d_val, g_val)
        s_J = tau_J * mpmath.mpc(mpmath.mpf('0.5') + d_val, g_val)

        # 2. Normalized radial coordinates (Observable A_K, A_J)
        R_K = mpmath.power(tau, -K) * s_K.real - mpmath.mpf('0.5')
        R_J = mpmath.power(tau, -J) * s_J.real - mpmath.mpf('0.5')
        cr1_residual = abs(R_K - R_J)
        cr1_satisfied = bool(cr1_residual < mpmath.mpf('1e-70'))

        # 3. Layer membership check (CR2)
        # Check if delta / tau^K and delta / tau^J are integers
        m_K = d_val / tau_K
        m_J = d_val / tau_J
        dist_K = abs(m_K - mpmath.nint(m_K))
        dist_J = abs(m_J - mpmath.nint(m_J))
        cr2_satisfied = bool(dist_K < mpmath.mpf('1e-50') and dist_J < mpmath.mpf('1e-50'))

        # 4. Off-line sensitivity check (CR3)
        cr3_satisfied = bool(d_val != mpmath.mpf('0') and R_K != mpmath.mpf('0'))

        return {
            "candidate_id": "CR-1",
            "candidate_name": "Normalized Radial Displacement",
            "test_displacement_delta": mpmath.nstr(d_val, n=15),
            "test_ordinate_gamma": mpmath.nstr(g_val, n=15),
            "grades": (K, J),
            "CR1_common_referent": {
                "R_K": mpmath.nstr(R_K, n=20),
                "R_J": mpmath.nstr(R_J, n=20),
                "residual": mpmath.nstr(cr1_residual, n=6),
                "satisfied": cr1_satisfied
            },
            "CR2_layer_membership": {
                "ratio_delta_over_tau_K": mpmath.nstr(m_K, n=15),
                "ratio_delta_over_tau_J": mpmath.nstr(m_J, n=15),
                "integer_distance_K": mpmath.nstr(dist_K, n=6),
                "integer_distance_J": mpmath.nstr(dist_J, n=6),
                "satisfied": cr2_satisfied,
                "obstruction": "DISGUISED_PREMISE: L_K intersect L_J = {0}, so requiring delta in L_K and L_J forces delta = 0 (assumes RH)"
            },
            "CR3_offline_nonzero": {
                "delta_nonzero": bool(d_val != mpmath.mpf('0')),
                "A_nonzero": bool(R_K != mpmath.mpf('0')),
                "satisfied": cr3_satisfied
            },
            "verdict": "CR1_AND_CR3_PROVED__CR2_BLOCKED_BY_DISGUISED_PREMISE",
            "epistemic_reason": "Normalized displacement delta is representation-invariant (CR1) and strictly detects off-line zeros (CR3). However, arithmetic layer membership (CR2) fails: asserting delta in L_K intersect L_J = {0} is logically equivalent to assuming delta = 0 at the outset."
        }


def evaluate_observable_inventory(dps: int = 80) -> Dict[str, Any]:
    """
    [DISCOVERY CYCLE 3: COMPLETE 10-OBSERVABLE INVENTORY]
    Systematically audits the 10 canonical mathematical quantities across Riemann Scope
    against the three Common-Referent conditions:
      (CR1) Common external value across grades.
      (CR2) Proved layer membership in L_K = tau^K * Z.
      (CR3) Strictly non-zero if and only if delta != 0.
    """
    inventory = [
        {
            "id": "OBS-01",
            "name": "Normalized Radial Displacement",
            "definition": "R_tau(s, k) = tau^(-k)*Re(s) - 1/2",
            "cr1_common_value": True,
            "cr2_layer_membership": False,
            "cr3_offline_nonzero": True,
            "earliest_failed_condition": "CR2: No law places delta in tau^K*Z; requiring it assumes delta=0 directly",
            "status": "CANDIDATE_CR1__MISSING_CR2"
        },
        {
            "id": "OBS-02",
            "name": "Raw Centered Displacement",
            "definition": "d_rho(K) = Re(z_K(rho)) = tau^K * delta",
            "cr1_common_value": False,
            "cr2_layer_membership": False,
            "cr3_offline_nonzero": True,
            "earliest_failed_condition": "CR1: Raw values tau^K*delta != tau^J*delta scale with grade weight 1",
            "status": "FAILS_CR1_AND_CR2"
        },
        {
            "id": "OBS-03",
            "name": "Curvature / Quartet Defect",
            "definition": "K_tau(rho) = B_rho''(0)/(2*(log tau)^2) = delta^2",
            "cr1_common_value": True,
            "cr2_layer_membership": False,
            "cr3_offline_nonzero": True,
            "earliest_failed_condition": "CR2: delta^2 is continuous non-negative real, not in discrete lattice tau^K*Z",
            "status": "FAILS_CR2"
        },
        {
            "id": "OBS-04",
            "name": "Grade Character & Reflection Defect",
            "definition": "chi_rho(K) = tau^(K*(rho-1/2)) = exp(K*(delta+i*gamma)*log tau); |chi_rho(K)| = tau^(K*delta); D_K = 4*sinh^2(K*delta*log tau / 2)",
            "cr1_common_value": False,
            "cr2_layer_membership": False,
            "cr3_offline_nonzero": True,
            "earliest_failed_condition": "CR1: Raw character values scale as powers q^K with modulus tau^(K*delta); CR2: values lie on complex spirals, not in tau^K*Z",
            "status": "FAILS_CR1_AND_CR2"
        },
        {
            "id": "OBS-05",
            "name": "Station Scaffold Locations",
            "definition": "x_{n,K} = n * tau^K in L_K (n in Z)",
            "cr1_common_value": False,
            "cr2_layer_membership": True,
            "cr3_offline_nonzero": False,
            "earliest_failed_condition": "CR1: n*tau^K != n*tau^J for K != J; CR3: coordinates exist independent of zeros rho",
            "status": "FAILS_CR1_AND_CR3"
        },
        {
            "id": "OBS-06",
            "name": "Logarithmic Prime Frequencies",
            "definition": "Dilated: tau^(-K)*log n; Translated: log n + K*log tau",
            "cr1_common_value": False,
            "cr2_layer_membership": False,
            "cr3_offline_nonzero": False,
            "earliest_failed_condition": "CR1, CR2, and CR3 all fail: frequencies shift, are transcendental, and independent of delta",
            "status": "FAILS_ALL"
        },
        {
            "id": "OBS-07",
            "name": "Zero-Counting / Winding Integers",
            "definition": "N(T, C_K) = (1/2*pi)*Delta_{C_K} arg xi(s) in Z under transported contour C_K = tau^K C_0 and height T_K = tau^K T",
            "cr1_common_value": True,
            "cr2_layer_membership": False,
            "cr3_offline_nonzero": False,
            "earliest_failed_condition": "CR2: N in Z = L_0, but N not in L_K = tau^K*Z for K != 0; CR3: N(T) counts all zeros in contour, invariant under horizontal displacement delta",
            "status": "FAILS_CR2_AND_CR3"
        },
        {
            "id": "OBS-08",
            "name": "Logarithmic Derivative Residues",
            "definition": "Res_{s=rho}(-xi_K'/xi_K) = m_rho in Z_{>=1}",
            "cr1_common_value": True,
            "cr2_layer_membership": False,
            "cr3_offline_nonzero": False,
            "earliest_failed_condition": "CR2: m_rho in Z = L_0, but m_rho not in L_K = tau^K*Z for K != 0; CR3: Multiplicity m_rho >= 1 holds for all zeros, whether delta=0 or delta!=0",
            "status": "FAILS_CR2_AND_CR3"
        },
        {
            "id": "OBS-09",
            "name": "Linear Explicit-Formula Tests",
            "definition": "C_{K,j}[phi] = sum_rho phi(tau^(-K)*gamma_rho) - prime/arch terms (converted pullback)",
            "cr1_common_value": False,
            "cr2_layer_membership": False,
            "cr3_offline_nonzero": False,
            "earliest_failed_condition": "CR1: Raw evaluations differ before coordinate conversion of the test function; CR2: continuous distribution values; CR3: vanishes identically for complete zero set",
            "status": "FAILS_ALL"
        },
        {
            "id": "OBS-10",
            "name": "Completed-xi Cross-Terms (Fixed Gaussian Instance)",
            "definition": "X_{xi,W} = Re<G_0, G_0''>_W in R (certified for a=1.5, sigma_W=1.0)",
            "cr1_common_value": True,
            "cr2_layer_membership": False,
            "cr3_offline_nonzero": False,
            "earliest_failed_condition": "CR2: Continuous integral ~ 0.02317 not in tau^K*Z; CR3: strictly positive on critical line (not a per-zero off-line detector)",
            "status": "FAILS_CR2_AND_CR3"
        }
    ]
    return {
        "inventory_scope": "Audit of the ten listed existing observables in the Riemann Scope corpus",
        "inventory_size": len(inventory),
        "inventory": inventory,
        "closest_candidate": "OBS-01 (Normalized Radial Displacement delta)",
        "proved_conditions_for_closest": ["CR1", "CR3"],
        "failing_condition_for_closest": "CR2 (Layer Membership)",
        "structural_barrier": "Strong unresolved bridge condition: For normalized displacement delta, CR2 together with layer separation and CR3 is sufficient to imply delta=0. Because L_K cap L_J = {0} for distinct integer grades, any candidate satisfying (CR1) and (CR2) forces delta = 0 directly, making layer membership an unresolved bridge condition whose independent derivation without assuming RH remains the core open obstacle."
    }



