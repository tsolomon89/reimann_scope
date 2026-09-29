"""Transcendental Continuation: Regularized Curvature-to-TC Transfer.

Implements the exact regularized curvature response for the weighted TC test:
1. Curvature kernel g_a(x) = (a^2 - x^2) / (a^2 + x^2)^2 for a > 0.
2. Fourier transform: \\hat{g}_a(u) = pi * |u| * exp(-a*|u|).
3. Distributional limit: g_a -> -Fp(1/x^2) as a -> 0 in the sense of Hadamard finite part.
4. Regularized test function:
       phi_{f_b}(t) = (1/pi) \\int_R f_b(u) (cos(u*t) - 1) / |u| du
   with removable singularity at u=0, phi(0)=0, and logarithmic growth as t -> inf.
5. Critical-line calibration:
       |u| * \\hat{phi}_{f_b}(u) = 2 f_b(u)  for u != 0.
   Exact pairing:
       K_{phi_{f_b}}(a, gamma) = \\int_R f_b(u) exp(-a*|u|) exp(i*u*gamma) du.
   On the critical line (a=0):
       K_{phi_{f_b}}(0, gamma) = Psi_b(i*gamma).
6. Reflected-pair correction:
       Psi_b(a + i*gamma) + Psi_b(-a + i*gamma) - 2 K_{phi_b}(a, gamma)
           = 2 \\int_R f_b(u) sinh(a*|u|) exp(i*u*gamma) du.
   Full quartet correction:
       Delta_{quartet}(a, gamma) = 8 m_0 \\int_0^R f_b(u) sinh(a*u) cos(u*gamma) du.
7. Distributional integration-by-parts bounds:
       |K_{f_b}(a, gamma)| <= (||f_b''||_1 + ||f_b'||_1 + (1/4)||f_b||_1 + |f_b(0)|) / gamma^2.
       |Delta_{pair}(a, gamma)| = O(a / gamma^2).
"""

import math
from typing import Callable, Dict, Any, List, Optional, Tuple
import numpy as np
import scipy.integrate


def curvature_kernel_g_a(x: float, a: float) -> float:
    """Second-derivative curvature response of a zero at distance a > 0.

    g_a(x) = (a^2 - x^2) / (a^2 + x^2)^2 = -d/dx [ x / (a^2 + x^2) ].
    """
    if a <= 0.0:
        raise ValueError(f"Curvature kernel requires a > 0; for a=0 use Hadamard finite-part distribution. Got a={a}")
    return (a**2 - x**2) / ((a**2 + x**2)**2)


def fourier_curvature_kernel(u: float, a: float) -> float:
    """Fourier transform of g_a(x) under convention \\hat{g}(u) = \\int g(x) exp(-iux) dx.

    \\hat{g}_a(u) = pi * |u| * exp(-a * |u|).
    """
    return math.pi * abs(u) * math.exp(-abs(a) * abs(u))


def hadamard_finite_part_pairing(
    phi_func: Callable[[float], float],
    gamma: float,
    t_max: float = 200.0,
    eps_rel: float = 1e-10
) -> float:
    """Evaluate the Hadamard finite-part pairing <-Fp(1/x^2), phi(. + gamma)>.

    For a C^2 test function with phi(0)=0 and logarithmic growth:
        <-Fp(1/x^2), phi(. + gamma)> = - \\int_0^\\infty [phi(gamma + x) + phi(gamma - x) - 2 phi(gamma)] / x^2 dx.
    """
    phi_gamma = phi_func(gamma)

    def integrand(x: float) -> float:
        if x == 0.0:
            return 0.0
        # Second-order finite difference numerator:
        num = phi_func(gamma + x) + phi_func(gamma - x) - 2.0 * phi_gamma
        return -num / (x**2)

    val, _ = scipy.integrate.quad(
        integrand,
        0.0,
        t_max,
        limit=1000,
        epsabs=1e-10,
        epsrel=eps_rel
    )
    return float(val)


def evaluate_regularized_test_function(
    f_b_func: Callable[[float], float],
    t: float,
    R_supp: float,
    eps_rel: float = 1e-11
) -> float:
    """Evaluate regularized test function phi_{f_b}(t).

    phi_{f_b}(t) = (1/pi) \\int_{-R}^R f_b(u) (cos(u*t) - 1) / |u| du
                 = (2/pi) \\int_0^R f_b(u) (cos(u*t) - 1) / u du.

    Removable singularity at u=0 since (cos(ut)-1)/u = -0.5*u*t^2 + O(u^3).
    Satisfies phi_{f_b}(0) = 0 and |phi_{f_b}(t)| = O(log |t|) as |t| -> inf.
    """
    if t == 0.0:
        return 0.0

    def integrand(u: float) -> float:
        if u == 0.0:
            return 0.0
        fb_val = f_b_func(u)
        if fb_val == 0.0:
            return 0.0
        return fb_val * (math.cos(u * t) - 1.0) / u

    val, _ = scipy.integrate.quad(
        integrand,
        0.0,
        R_supp,
        limit=500,
        epsabs=1e-12,
        epsrel=eps_rel
    )
    return float((2.0 / math.pi) * val)


def single_zero_curvature_response(
    f_b_func: Callable[[float], float],
    a: float,
    gamma: float,
    R_supp: float,
    eps_rel: float = 1e-12
) -> float:
    """Evaluate calibrated curvature response K_{phi_{f_b}}(a, gamma).

    K_{phi_{f_b}}(a, gamma) = \\int_{-R}^R f_b(u) exp(-a*|u|) exp(i*u*gamma) du
                            = 2 \\int_0^R f_b(u) exp(-a*u) cos(u*gamma) du.
    """
    a_abs = abs(a)

    def integrand(u: float) -> float:
        fb_val = f_b_func(u)
        if fb_val == 0.0:
            return 0.0
        return fb_val * math.exp(-a_abs * u) * math.cos(u * gamma)

    val, _ = scipy.integrate.quad(
        integrand,
        0.0,
        R_supp,
        limit=500,
        epsabs=1e-13,
        epsrel=eps_rel
    )
    return float(2.0 * val)


def spectral_test_observable(
    f_b_func: Callable[[float], float],
    z: complex,
    R_supp: float,
    eps_rel: float = 1e-12
) -> float:
    """Evaluate spectral observable Psi_b(z) = \\int_{-R}^R f_b(u) exp(z*u) du.

    For even real f_b:
        Psi_b(delta + i*gamma) = 2 \\int_0^R f_b(u) cosh(delta * u) cos(gamma * u) du.
    """
    delta = z.real
    gamma = z.imag

    def integrand(u: float) -> float:
        fb_val = f_b_func(u)
        if fb_val == 0.0:
            return 0.0
        return fb_val * math.cosh(delta * u) * math.cos(gamma * u)

    val, _ = scipy.integrate.quad(
        integrand,
        0.0,
        R_supp,
        limit=500,
        epsabs=1e-13,
        epsrel=eps_rel
    )
    return float(2.0 * val)


def reflected_pair_correction(
    f_b_func: Callable[[float], float],
    a: float,
    gamma: float,
    R_supp: float,
    eps_rel: float = 1e-12
) -> float:
    """Evaluate reflected-pair correction Delta_{pair}(a, gamma).

    Delta_{pair}(a, gamma) = Psi_b(a + i*gamma) + Psi_b(-a + i*gamma) - 2 K_{phi_b}(a, gamma)
                           = 2 \\int_{-R}^R f_b(u) sinh(a*|u|) exp(i*u*gamma) du
                           = 4 \\int_0^R f_b(u) sinh(a*u) cos(u*gamma) du.

    Identically zero for a = 0 (critical line).
    """
    if a == 0.0:
        return 0.0

    a_abs = abs(a)

    def integrand(u: float) -> float:
        fb_val = f_b_func(u)
        if fb_val == 0.0:
            return 0.0
        return fb_val * math.sinh(a_abs * u) * math.cos(u * gamma)

    val, _ = scipy.integrate.quad(
        integrand,
        0.0,
        R_supp,
        limit=500,
        epsabs=1e-13,
        epsrel=eps_rel
    )
    return float(4.0 * val)


def quartet_correction(
    f_b_func: Callable[[float], float],
    a: float,
    gamma: float,
    R_supp: float,
    multiplicity_m0: int = 1,
    eps_rel: float = 1e-12
) -> float:
    """Evaluate complete 4-zero quartet correction Delta_{quartet}(a, gamma).

    Q_{Psi_b}(a, gamma) - K_{quartet, phi_b}(a, gamma)
        = m_0 * [ Delta_{pair}(a, gamma) + Delta_{pair}(a, -gamma) ]
        = 8 m_0 \\int_0^R f_b(u) sinh(a*u) cos(u*gamma) du.
    """
    if a == 0.0:
        return 0.0

    pair_corr = reflected_pair_correction(f_b_func, a, gamma, R_supp, eps_rel=eps_rel)
    return float(2.0 * multiplicity_m0 * pair_corr)


def evaluate_distributional_jump_bound(
    f_b_0: float,
    l1_fb: float,
    l1_fb_prime: float,
    l1_fb_double_prime: float,
    a: float,
    gamma: float,
    R_supp: float
) -> Dict[str, float]:
    """Evaluate analytic bounds from distributional twice integration-by-parts.

    For 0 <= a <= 1/2 and gamma != 0:
    1. Single-zero curvature response bound:
           |K_{f_b}(a, gamma)| <= (||f_b''||_1 + ||f_b'||_1 + (1/4)||f_b||_1 + |f_b(0)|) / gamma^2.
    2. Reflected pair correction bound:
           |Delta_{pair}(a, gamma)| <= (4 a |f_b(0)| + 2 sinh(a R) ||f_b''||_1 + 4 a cosh(a R) ||f_b'||_1 + 2 a^2 sinh(a R) ||f_b||_1) / gamma^2.
    """
    if gamma == 0.0:
        raise ValueError("Distributional jump bound requires non-zero ordinate gamma.")

    gamma_sq = gamma ** 2
    a_abs = min(abs(a), 0.5)

    # Response numerator:
    num_resp = l1_fb_double_prime + l1_fb_prime + 0.25 * l1_fb + abs(f_b_0)
    bound_response = num_resp / gamma_sq

    # Correction numerator (has factor of a on every term):
    sinh_ar = math.sinh(a_abs * R_supp) if a_abs > 0 else 0.0
    cosh_ar = math.cosh(a_abs * R_supp) if a_abs > 0 else 1.0

    num_corr = (
        4.0 * a_abs * abs(f_b_0) +
        2.0 * sinh_ar * l1_fb_double_prime +
        4.0 * a_abs * cosh_ar * l1_fb_prime +
        2.0 * (a_abs ** 2) * sinh_ar * l1_fb
    )
    bound_correction = num_corr / gamma_sq

    return {
        'gamma': float(gamma),
        'a': float(a_abs),
        'R_supp': float(R_supp),
        'response_bound': float(bound_response),
        'correction_bound': float(bound_correction),
        'asymptotic_decay_power': -2.0,
        'linear_a_vanish_factor': float(num_corr / (a_abs if a_abs > 0 else 1.0))
    }


def evaluate_finite_symmetric_multiset_transfer(
    f_b_func: Callable[[float], float],
    zeros: List[Dict[str, Any]],
    R_supp: float
) -> Dict[str, Any]:
    """Verify exact transfer identity on a finite symmetric zero multiset.

    Evaluates:
      1. Spectral sum S_{Psi_b} = sum_{rho} m_rho Psi_b(rho - 1/2).
      2. Regularized curvature sum K_{phi_b} = sum_{rho} m_rho K_{phi_b}(rho).
      3. Predicted theoretical correction Delta_{total} = sum_{off-critical} m_rho Delta_{quartet}.
      4. Exact balance discrepancy |S - K - Delta|.
    """
    total_psi = 0.0
    total_k = 0.0
    total_delta_predicted = 0.0

    zero_details = []
    for z_spec in zeros:
        a = float(z_spec.get('a', 0.0))
        gamma = float(z_spec['gamma'])
        m = int(z_spec.get('multiplicity', 1))
        is_quartet = bool(z_spec.get('is_quartet', a > 0.0))

        if not is_quartet:
            # Critical line pair (+- gamma):
            psi_val = 2.0 * spectral_test_observable(f_b_func, complex(0.0, gamma), R_supp)
            k_val = 2.0 * single_zero_curvature_response(f_b_func, 0.0, gamma, R_supp)
            delta_val = 0.0
        else:
            # Full 4-zero quartet (+-a +- i*gamma):
            # Psi_b evaluated at 4 zeros:
            psi_single = spectral_test_observable(f_b_func, complex(a, gamma), R_supp)
            psi_val = 4.0 * psi_single
            # K_phi evaluated at 4 zeros: 2 upper + 2 lower:
            k_single = single_zero_curvature_response(f_b_func, a, gamma, R_supp)
            k_val = 4.0 * k_single
            # Theoretical quartet correction:
            delta_val = quartet_correction(f_b_func, a, gamma, R_supp, multiplicity_m0=1)

        term_psi = m * psi_val
        term_k = m * k_val
        term_delta = m * delta_val

        total_psi += term_psi
        total_k += term_k
        total_delta_predicted += term_delta

        zero_details.append({
            'a': a,
            'gamma': gamma,
            'multiplicity': m,
            'is_quartet': is_quartet,
            'psi_sum': float(term_psi),
            'k_curvature_sum': float(term_k),
            'pair_discrepancy': float(term_psi - term_k),
            'predicted_correction': float(term_delta),
            'residual': float(abs(term_psi - term_k - term_delta))
        })

    balance_discrepancy = abs(total_psi - total_k - total_delta_predicted)

    return {
        'total_zeros_count': len(zeros),
        'total_spectral_sum_S': float(total_psi),
        'total_curvature_sum_K': float(total_k),
        'total_predicted_correction_Delta': float(total_delta_predicted),
        'balance_discrepancy': float(balance_discrepancy),
        'is_transfer_exact_within_tol': bool(balance_discrepancy < 1e-12),
        'zero_details': zero_details
    }


def audit_regularized_curvature_transfer(
    output_path: Optional[str] = None
) -> Dict[str, Any]:
    """Execute complete mathematical audit and numerical reproduction of the curvature transfer."""
    import json
    h = 0.05
    R_supp = math.log(20.0 / 8.0) + 2.0 * h  # log(2.5) + 0.10 ~= 1.01629

    # Standard smooth bump kernel profile for testing:
    def canonical_fb(u: float) -> float:
        if abs(u) >= R_supp:
            return 0.0
        return (1.0 - (u / R_supp)**2)**4

    # Finite symmetric multiset test:
    # 5 critical line pairs and 1 off-critical quartet:
    test_zeros = [
        {'a': 0.0, 'gamma': 14.13472514, 'multiplicity': 1, 'is_quartet': False},
        {'a': 0.0, 'gamma': 21.02203964, 'multiplicity': 1, 'is_quartet': False},
        {'a': 0.0, 'gamma': 25.01085758, 'multiplicity': 1, 'is_quartet': False},
        {'a': 0.0, 'gamma': 30.42487613, 'multiplicity': 1, 'is_quartet': False},
        {'a': 0.0, 'gamma': 32.93506159, 'multiplicity': 1, 'is_quartet': False},
        {'a': 0.49, 'gamma': 50.0, 'multiplicity': 1, 'is_quartet': True}
    ]

    multiset_result = evaluate_finite_symmetric_multiset_transfer(canonical_fb, test_zeros, R_supp)

    # Estimate L1 norms of canonical_fb:
    u_dense = np.linspace(-R_supp, R_supp, 2001)
    fb_vals = np.array([canonical_fb(u) for u in u_dense])
    du = u_dense[1] - u_dense[0]
    fb_p = np.gradient(fb_vals, du)
    fb_pp = np.gradient(fb_p, du)

    l1_fb = float(np.sum(np.abs(fb_vals)) * du)
    l1_fb_prime = float(np.sum(np.abs(fb_p)) * du)
    l1_fb_double_prime = float(np.sum(np.abs(fb_pp)) * du)
    fb_0 = float(canonical_fb(0.0))

    jump_bounds = evaluate_distributional_jump_bound(
        f_b_0=fb_0,
        l1_fb=l1_fb,
        l1_fb_prime=l1_fb_prime,
        l1_fb_double_prime=l1_fb_double_prime,
        a=0.49,
        gamma=50.0,
        R_supp=R_supp
    )

    report = {
        'epistemic_status': 'EXACT_FINITE_IDENTITY_UNRESOLVED_INFINITE_EXTENSION',
        'parameters': {
            'bandwidth_h': float(h),
            'autocorrelation_support_radius_R_supp': float(R_supp),
            'formula_R_supp': 'log(20/8) + 2h = log(2.5) + 0.10 ~= 1.01629'
        },
        'transfer_theorems': {
            'single_zero_response': (
                "K_{phi_{f_b}}(a, gamma) = \\int_{-R}^R f_b(u) exp(-a*|u|) exp(i*u*gamma) du. "
                "For a=0: K_{phi_{f_b}}(0, gamma) = Psi_b(i*gamma) identically."
            ),
            'reflected_pair_correction': (
                "Psi_b(a + i*gamma) + Psi_b(-a + i*gamma) - 2 K_{phi_{f_b}}(a, gamma) = "
                "2 \\int_{-R}^R f_b(u) sinh(a*|u|) exp(i*u*gamma) du."
            ),
            'quartet_correction': (
                "Delta_{quartet}(a, gamma) = 8 m_0 \\int_0^R f_b(u) sinh(a*u) cos(u*gamma) du."
            ),
            'distributional_bound': (
                "|K_{f_b}(a, gamma)| <= (||f_b''||_1 + ||f_b'||_1 + (1/4)||f_b||_1 + |f_b(0)|) / gamma^2."
            )
        },
        'finite_symmetric_multiset_verification': multiset_result,
        'distributional_jump_bounds': jump_bounds,
        'reductio_implication_audit': {
            'what_H_supplies': (
                "Hypothesis H posits an off-critical zero rho_0 = 1/2 + delta_0 + i*gamma_0 (delta_0 != 0). "
                "This supplies a non-vanishing discrete quartet term and a non-vanishing local correction "
                "Delta_{quartet}(delta_0, gamma_0) = 8 m_0 \\int_0^R f_b(u) sinh(delta_0 u) cos(u gamma_0) du. "
                "By the distributional integration-by-parts bound, |Delta_{quartet}| <= O(delta_0 / gamma_0^2)."
            ),
            'what_remains_unproved': (
                "1. Hypothesis H does not bound the collective sum over critical zeros or exclude other off-critical zeros. "
                "2. The arithmetic energy A_{Psi, <= U} ~ 7.15e8 is balanced by the infinite sum over all zeros in the Guinand-Weil "
                "explicit formula, holding identically whether H is true or false. "
                "3. The local quartet correction O(1/gamma_0^2) is orders of magnitude smaller than 7.15e8 and cannot "
                "force the remainder |D| < 1/2 without an independent global arithmetic obstruction. "
                "4. An unregularized curvature integral diverges as (t-gamma_j)^{-2} at critical-line zeros; "
                "Hadamard finite-part regularization eliminates local divergence, but the infinite regularized curvature "
                "series sum_{gamma} K_{phi_b}(gamma) requires unconditional zero-counting summation control."
            ),
            'circularity_check': (
                "Asserting that |D| < 1/2 follows from H assumes that the spectral explicit formula sum fails to cancel "
                "the arithmetic energy by at least 7.14e8. But this asserts the contradiction that the reductio is intended "
                "to deduce, introducing circularity if asserted as a premise."
            ),
            'governing_next_question': (
                "Can an independent global arithmetic lower bound on |A_{Psi, <= U}(b) - S_{Psi, crit}(b)| be proved "
                "from the non-vanishing of rho_0 off the critical line, without assuming the reductio conclusion?"
            )
        }
    }

    if output_path:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
        except Exception:
            pass

    return report
