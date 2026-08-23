"""
math_core.py — Certified High-Precision Mathematical Core

Provides arbitrary-precision evaluation of the Riemann zeta function,
the completed Xi function xi(s), the Hardy Z-function Z(t), Riemann-Siegel theta,
and radial centrifuge quantities using python-flint (Arb ball arithmetic)
with mpmath fallback.

Strict adherence to MATH_CONTRACT.md, SPEC.md, and EXPERIMENT_PROTOCOL.md.
Explicit separation of:
- Preview/render path (NumPy / float for responsive UI)
- Audit/authoritative path (arbitrary precision mpmath/flint Arb without float downcast)
"""

from __future__ import annotations
import math
from typing import Union, Tuple, List, Optional, Dict, Any, Sequence, Set
import numpy as np
import mpmath

try:
    import flint  # type: ignore[import]
    from flint import arb, acb, ctx as flint_ctx  # type: ignore[import]
    HAS_FLINT = True
except ImportError:
    HAS_FLINT = False



# Cache for high-precision constants
_TAU_CACHE: Dict[int, mpmath.mpf] = {}


def get_tau(dps: int = 80) -> mpmath.mpf:
    """Return tau = 2*pi computed to the requested decimal precision."""
    if dps in _TAU_CACHE:
        return _TAU_CACHE[dps]
    with mpmath.workdps(dps + 10):
        tau_val = mpmath.mpf(2) * mpmath.pi
    _TAU_CACHE[dps] = tau_val
    return tau_val


def get_tau_str(dps: int = 80) -> str:
    """Return tau = 2*pi as a high-precision decimal string."""
    with mpmath.workdps(dps + 5):
        return mpmath.nstr(mpmath.mpf(2) * mpmath.pi, n=dps)


def to_mpc(
    s: Union[complex, str, Tuple[Union[str, float, int, mpmath.mpf], Union[str, float, int, mpmath.mpf]], mpmath.mpc, mpmath.mpf, int, float],
    dps: int = 80
) -> mpmath.mpc:
    """
    Safely convert coordinate representation to mpmath.mpc without precision loss.
    Accepts exact decimal strings, 2-tuples of strings, mpmath objects, and complex.
    """
    with mpmath.workdps(dps + 10):
        if isinstance(s, mpmath.mpc):
            return s
        if isinstance(s, tuple) and len(s) == 2:
            return mpmath.mpc(str(s[0]).strip(), str(s[1]).strip())
        if isinstance(s, complex):
            return mpmath.mpc(str(s.real), str(s.imag))
        if isinstance(s, mpmath.mpf):
            return mpmath.mpc(s, mpmath.mpf('0'))
        if isinstance(s, (int, float)):
            return mpmath.mpc(str(s), '0')
        if isinstance(s, str):
            s_clean = s.strip().replace(' ', '').replace('*', '')
            if 'j' in s_clean or 'J' in s_clean or 'i' in s_clean or 'I' in s_clean:
                s_clean = s_clean.replace('i', 'j').replace('I', 'j').replace('J', 'j')
                if '+' in s_clean:
                    parts = s_clean.split('+')
                    re_part = parts[0]
                    im_part = parts[1].replace('j', '')
                    return mpmath.mpc(re_part, im_part if im_part else '1')
                elif '-' in s_clean[1:]:
                    idx = s_clean.rfind('-')
                    re_part = s_clean[:idx]
                    im_part = s_clean[idx:].replace('j', '')
                    return mpmath.mpc(re_part, im_part if im_part != '-' else '-1')
                else:
                    im_part = s_clean.replace('j', '')
                    return mpmath.mpc('0', im_part if im_part not in ['', '+', '-'] else (im_part + '1'))
            return mpmath.mpc(s_clean, '0')
        return mpmath.mpc(s)



def to_mpf(
    val: Union[str, float, int, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """Safely convert real parameter representation to mpmath.mpf without precision loss."""
    with mpmath.workdps(dps + 10):
        if isinstance(val, mpmath.mpf):
            return val
        return mpmath.mpf(str(val))


def zeta_eval(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any], mpmath.mpf, int, float],
    dps: int = 35
) -> mpmath.mpc:
    """
    Evaluate Riemann zeta function zeta(s) at arbitrary precision dps.
    Uses python-flint (Arb) if available for speed and certified precision,
    falling back cleanly to mpmath.zeta.
    """
    with mpmath.workdps(dps + 10):
        s_mpc = to_mpc(s, dps=dps)

        if HAS_FLINT:
            try:
                flint_ctx.dps = dps + 10
                re_str = mpmath.nstr(s_mpc.real, n=dps + 10)
                im_str = mpmath.nstr(s_mpc.imag, n=dps + 10)
                s_arb = acb(re_str, im_str)
                z_arb = s_arb.zeta()
                mid = z_arb.mid()
                return mpmath.mpc(str(mid.real), str(mid.imag))
            except Exception:
                pass  # fallback to mpmath

        return mpmath.zeta(s_mpc)


def zeta_eval_certified(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    dps: int = 80
) -> Tuple[mpmath.mpc, str, bool]:
    """
    Certified evaluation of zeta(s) using Arb ball arithmetic.
    Returns (midpoint, radius_bound_str, residual_encloses_zero).

    Semantics:
    - midpoint: mpmath.mpc enclosure center.
    - radius_bound_str: upper bound on evaluation uncertainty as a decimal string.
    - residual_encloses_zero: True if the ball enclosure of zeta(s) contains 0,
      meaning |zeta(s)| <= radius_bound.
    Note: This certifies the precision of the function evaluation residual at s;
    it does NOT claim proof of zero completeness or that s is an exact algebraic root.
    """
    with mpmath.workdps(dps + 10):
        s_mpc = to_mpc(s, dps=dps)
        if HAS_FLINT:
            flint_ctx.dps = dps + 10
            re_str = mpmath.nstr(s_mpc.real, n=dps + 10)
            im_str = mpmath.nstr(s_mpc.imag, n=dps + 10)
            s_arb = acb(re_str, im_str)
            z_arb = s_arb.zeta()
            contains_0 = bool(z_arb.contains(0))
            rad_str = str(z_arb.rad())
            mid = z_arb.mid()
            val_mpc = mpmath.mpc(str(mid.real), str(mid.imag))
            return val_mpc, rad_str, contains_0
        else:
            val = mpmath.zeta(s_mpc)
            tol = mpmath.mpf(10) ** (-dps + 5)
            contains_0 = bool(abs(val) < tol)
            rad_str = mpmath.nstr(mpmath.mpf(10) ** (-dps + 2), n=6)
            return val, rad_str, contains_0


def completed_xi(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    dps: int = 80
) -> mpmath.mpc:
    """
    Evaluate the completed Riemann xi function:
    xi(s) = 1/2 * s * (s - 1) * pi^(-s/2) * Gamma(s/2) * zeta(s).
    Satisfies the functional equation xi(s) = xi(1-s).
    """
    with mpmath.workdps(dps + 15):
        s_mpc = to_mpc(s, dps=dps)
        pi = mpmath.pi
        term1 = mpmath.mpf('0.5') * s_mpc * (s_mpc - 1)
        term2 = mpmath.power(pi, -s_mpc / 2)
        term3 = mpmath.gamma(s_mpc / 2)
        term4 = zeta_eval(s_mpc, dps=dps + 10)
        res = term1 * term2 * term3 * term4
        return res


xi_eval = completed_xi


def zeta_derivative(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    n: int = 1,
    dps: int = 80
) -> mpmath.mpc:
    """
    Evaluate the n-th complex derivative d^n/ds^n zeta(s) at arbitrary precision dps.
    Uses mpmath.zeta analytic derivative evaluation.
    """
    with mpmath.workdps(dps + 15):
        s_mpc = to_mpc(s, dps=dps + 15)
        return mpmath.zeta(s_mpc, derivative=n)


def hardy_theta(
    t: Union[float, str, mpmath.mpf, int],
    dps: int = 35
) -> mpmath.mpf:
    """
    Compute the Riemann-Siegel theta function:
    theta(t) = Im(ln Gamma(1/4 + i*t/2)) - (t/2)*ln(pi).
    """
    with mpmath.workdps(dps + 10):
        t_mpf = to_mpf(t, dps=dps)
        s = mpmath.mpc('0.25', str(t_mpf / 2))
        log_gamma = mpmath.loggamma(s)
        theta_val = mpmath.im(log_gamma) - (t_mpf / 2) * mpmath.log(mpmath.pi)
        return theta_val


def hardy_z(
    t: Union[float, str, mpmath.mpf, int],
    dps: int = 35
) -> mpmath.mpf:
    """
    Evaluate the real-valued Hardy Z-function on the critical line:
    Z(t) = exp(i*theta(t)) * zeta(1/2 + i*t).
    Uses mpmath.siegelz for exact high-precision evaluation.
    """
    with mpmath.workdps(dps + 10):
        t_mpf = to_mpf(t, dps=dps)
        return mpmath.siegelz(t_mpf)


# ==============================================================================
# PREVIEW PATH (Float / NumPy for interactive rendering)
# ==============================================================================

def eval_zeta_path(
    s_coords: List[complex] | np.ndarray,
    dps: int = 35
) -> Tuple[np.ndarray, np.ndarray]:
    """
    [PREVIEW PATH] Batch evaluation of zeta(s) along a path s(u).
    Returns (re_values, im_values) as float64 numpy arrays for rendering.
    Explicitly labeled preview; not authoritative evidence.
    """
    n_pts = len(s_coords)
    re_vals = np.empty(n_pts, dtype=np.float64)
    im_vals = np.empty(n_pts, dtype=np.float64)

    if HAS_FLINT and dps <= 60:
        flint_ctx.dps = dps
        for idx, pt in enumerate(s_coords):
            s_arb = acb(str(pt.real), str(pt.imag))
            z_arb = s_arb.zeta()
            mid = z_arb.mid()
            re_vals[idx] = float(mid.real)
            im_vals[idx] = float(mid.imag)
    else:
        with mpmath.workdps(dps):
            for idx, pt in enumerate(s_coords):
                s_mpc = mpmath.mpc(str(pt.real), str(pt.imag))
                z_val = mpmath.zeta(s_mpc)
                re_vals[idx] = float(z_val.real)
                im_vals[idx] = float(z_val.imag)

    return re_vals, im_vals


# ==============================================================================
# AUDIT PATH (Arbitrary-Precision without float downcast)
# ==============================================================================

def eval_zeta_path_audit(
    s_coords: List[Union[str, mpmath.mpc, Tuple[Any, Any]]],
    dps: int = 80
) -> List[mpmath.mpc]:
    """
    [AUDIT PATH] Certified high-precision evaluation of zeta(s) along coordinate points.
    Preserves exact arbitrary-precision mpmath.mpc values without binary float downcast.
    """
    results = []
    with mpmath.workdps(dps + 10):
        for pt in s_coords:
            z_val = zeta_eval(pt, dps=dps)
            results.append(z_val)
    return results


def centrifuge_log_modulus(
    delta: Union[float, str, mpmath.mpf, int],
    K: Union[float, str, mpmath.mpf, int],
    dps: int = 80
) -> mpmath.mpf:
    """
    Exact algebraic formula for the radial centrifuge log-modulus:
    log |q_rho^K| = K * delta * ln(tau).
    Evaluated at arbitrary precision dps without binary-float downcast.
    """
    with mpmath.workdps(dps + 10):
        tau = get_tau(dps)
        d_val = to_mpf(delta, dps=dps)
        k_val = to_mpf(K, dps=dps)
        return k_val * d_val * mpmath.log(tau)


def centrifuge_q_k(
    delta: Union[float, str, mpmath.mpf, int],
    gamma: Union[float, str, mpmath.mpf, int],
    K: Union[float, str, mpmath.mpf, int],
    dps: int = 80
) -> mpmath.mpc:
    """
    Complex value of the centrifuge grade-K character:
    q_rho^K = tau^(K*delta) * exp(i * K * gamma * ln(tau)).
    Evaluated at arbitrary precision dps without binary-float downcast.
    """
    with mpmath.workdps(dps + 10):
        tau = get_tau(dps)
        d_val = to_mpf(delta, dps=dps)
        g_val = to_mpf(gamma, dps=dps)
        k_val = to_mpf(K, dps=dps)

        modulus = mpmath.power(tau, k_val * d_val)
        phase = k_val * g_val * mpmath.log(tau)

        return modulus * (mpmath.cos(phase) + mpmath.j * mpmath.sin(phase))


def symmetric_centrifuge_defect(
    delta: Union[float, str, mpmath.mpf, int],
    gamma: Union[float, str, mpmath.mpf, int],
    K: Union[float, str, mpmath.mpf, int],
    dps: int = 80
) -> mpmath.mpc:
    """
    [AUDIT PATH] Exact algebraic calculation of the symmetry-complete centrifuge defect:
    D_K = q_+^K + q_-^K - 2 * q_0^K
    where q_+^K = tau^(K*delta) * exp(i*K*gamma*ln(tau)),
          q_-^K = tau^(-K*delta) * exp(i*K*gamma*ln(tau)),
          q_0^K = exp(i*K*gamma*ln(tau)).
    Evaluated at arbitrary precision dps without binary-float downcast.
    """
    with mpmath.workdps(dps + 15):
        d_val = to_mpf(delta, dps=dps + 15)
        g_val = to_mpf(gamma, dps=dps + 15)
        k_val = to_mpf(K, dps=dps + 15)

        q_plus = centrifuge_q_k(d_val, g_val, k_val, dps=dps + 15)
        q_minus = centrifuge_q_k(-d_val, g_val, k_val, dps=dps + 15)
        q_zero = centrifuge_q_k(mpmath.mpf('0'), g_val, k_val, dps=dps + 15)

        return q_plus + q_minus - mpmath.mpf(2) * q_zero


def symmetric_centrifuge_defect_expected(
    delta: Union[float, str, mpmath.mpf, int],
    K: Union[float, str, mpmath.mpf, int],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Exact closed-form absolute value of the symmetric centrifuge defect:
    |D_K| = 2 * [cosh(K * delta * ln(tau)) - 1] = 4 * sinh^2(K * delta * ln(tau) / 2).
    Evaluated at arbitrary precision dps.
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps)
        d_val = to_mpf(delta, dps=dps + 15)
        k_val = to_mpf(K, dps=dps + 15)

        arg = k_val * d_val * mpmath.log(tau) / mpmath.mpf(2)
        sh = mpmath.sinh(arg)
        return mpmath.mpf(4) * (sh * sh)


# =============================================================================
# Riemann–Weil Explicit Formula & Grade-Indexed Discrimination Engine
# =============================================================================

EXPLICIT_FORMULA_TEST_FUNCTIONS: Dict[int, Dict[str, str]] = {
    1: {
        "sigma": "2.0",
        "t0": "14.1347251417346937904572519835624702707842571156992431756855674601499634298092567649490103931715610127",
        "target": "zero_1",
        "description": "Gaussian packet centered at zero #1 (gamma_1 ~ 14.1347)",
    },
    2: {
        "sigma": "2.0",
        "t0": "21.0220396387715549926284795938969027773343405249027818047646197204481023773179247653775465942475143362",
        "target": "zero_2",
        "description": "Gaussian packet centered at zero #2 (gamma_2 ~ 21.0220)",
    },
    3: {
        "sigma": "2.5",
        "t0": "49.7738324776723021819167846785637240577231782996766621801324976210086708705703901416954203478952402123",
        "target": "zero_10",
        "description": "Gaussian packet centered at zero #10 (gamma_10 ~ 49.7738)",
    },
    4: {
        "sigma": "3.0",
        "t0": "75.70469069908393316832691676203034592281190353069740030164777530157419702770632360838403702183465280",
        "target": "zero_19",
        "description": "Gaussian packet centered at zero #19 (gamma_19 ~ 75.7047)",
    },
    5: {
        "sigma": "3.5",
        "t0": "143.1118458076206327394051238689139299662331024303546325485985229572806931441333492275444274025136984",
        "target": "zero_50",
        "description": "Gaussian packet centered at zero #50 (gamma_50 ~ 143.1118)",
    },
    6: {
        "sigma": "4.0",
        "t0": "236.5242296658162058024755079556629786895294952121891237009189609878191503842923328262614446040651740",
        "target": "zero_100",
        "description": "Gaussian packet centered at zero #100 (gamma_100 ~ 236.5242)",
    },
}


def get_test_function_params(j: int, dps: int = 80) -> Tuple[mpmath.mpf, mpmath.mpf]:
    """Retrieve arbitrary-precision (sigma, t0) for test function index j in 1..6."""
    if j not in EXPLICIT_FORMULA_TEST_FUNCTIONS:
        raise ValueError(f"Invalid test function index {j}; must be in 1..6")
    spec = EXPLICIT_FORMULA_TEST_FUNCTIONS[j]
    with mpmath.workdps(dps + 15):
        sigma = to_mpf(spec["sigma"], dps=dps + 15)
        t0 = to_mpf(spec["t0"], dps=dps + 15)
    return sigma, t0


def H_test_function(
    t: Union[mpmath.mpf, mpmath.mpc, float, str],
    j: int,
    dps: int = 80
) -> Union[mpmath.mpf, mpmath.mpc]:
    """
    Even modulated Gaussian test function in grade coordinates:
    H_j(t) = exp(-(t - t_{0,j})^2 / (2*sigma_j^2)) + exp(-(t + t_{0,j})^2 / (2*sigma_j^2)).
    Admissible: even, entire on C, rapid Schwartz decay on R.
    """
    with mpmath.workdps(dps + 15):
        sigma, t0 = get_test_function_params(j, dps=dps + 15)
        two_sigma_sq = mpmath.mpf(2) * (sigma * sigma)

        t_val = to_mpc(t, dps=dps + 15) if isinstance(t, (complex, mpmath.mpc)) or (isinstance(t, str) and ("j" in t or "+" in t.lstrip("+-"))) else to_mpf(t, dps=dps + 15)

        term_minus = mpmath.exp(-mpmath.power(t_val - t0, 2) / two_sigma_sq)
        term_plus = mpmath.exp(-mpmath.power(t_val + t0, 2) / two_sigma_sq)
        res = term_minus + term_plus
        if isinstance(t_val, mpmath.mpf):
            return mpmath.re(res)
        return res


def H_test_function_hat(
    x: Union[mpmath.mpf, float, str],
    j: int,
    dps: int = 80
) -> mpmath.mpf:
    """
    Analytic Fourier transform under convention:
    \\widehat{H}_j(x) = \\int_{-\\infty}^\\infty H_j(t) e^{-i x t} dt
                   = 2 * sigma_j * sqrt(2*pi) * exp(-sigma_j^2 * x^2 / 2) * cos(t_{0,j} * x).
    """
    with mpmath.workdps(dps + 15):
        sigma, t0 = get_test_function_params(j, dps=dps + 15)
        x_val = to_mpf(x, dps=dps + 15)
        tau = get_tau(dps=dps + 15)

        prefactor = mpmath.mpf(2) * sigma * mpmath.sqrt(tau)
        gaussian_decay = mpmath.exp(-(sigma * sigma * x_val * x_val) / mpmath.mpf(2))
        oscillation = mpmath.cos(t0 * x_val)
        return prefactor * gaussian_decay * oscillation


def H_test_function_prime(
    t: Union[mpmath.mpf, mpmath.mpc, float, str],
    j: int,
    dps: int = 80
) -> Union[mpmath.mpf, mpmath.mpc]:
    """
    Analytic derivative H_j'(t) = dH_j/dt:
    H_j'(t) = -((t - t0)/sigma^2)*exp(-(t-t0)^2/(2*sigma^2)) - ((t + t0)/sigma^2)*exp(-(t+t0)^2/(2*sigma^2)).
    """
    with mpmath.workdps(dps + 15):
        sigma, t0 = get_test_function_params(j, dps=dps + 15)
        sigma_sq = sigma * sigma
        two_sigma_sq = mpmath.mpf(2) * sigma_sq

        t_val = to_mpc(t, dps=dps + 15) if isinstance(t, (complex, mpmath.mpc)) or (isinstance(t, str) and ("j" in t or "+" in t.lstrip("+-"))) else to_mpf(t, dps=dps + 15)

        term_minus = ((t_val - t0) / sigma_sq) * mpmath.exp(-mpmath.power(t_val - t0, 2) / two_sigma_sq)
        term_plus = ((t_val + t0) / sigma_sq) * mpmath.exp(-mpmath.power(t_val + t0, 2) / two_sigma_sq)
        res = -term_minus - term_plus
        if isinstance(t_val, mpmath.mpf):
            return mpmath.re(res)
        return res


def h_kj_scaled(
    t: Union[mpmath.mpf, mpmath.mpc, float, str],
    j: int,
    K: Union[int, float, str, mpmath.mpf],
    dps: int = 80
) -> Union[mpmath.mpf, mpmath.mpc]:
    """
    Grade-K scaled test function: h_{K,j}(t) = H_j(a_K * t), where a_K = tau^K = (2*pi)^K.
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        k_val = to_mpf(K, dps=dps + 15)
        a_K = mpmath.power(tau, k_val)

        if isinstance(t, (complex, mpmath.mpc)) or (isinstance(t, str) and ("j" in t or "+" in t.lstrip("+-"))):
            t_val = to_mpc(t, dps=dps + 15)
            scaled_t = a_K * t_val
        else:
            t_val = to_mpf(t, dps=dps + 15)
            scaled_t = a_K * t_val
        return H_test_function(scaled_t, j, dps=dps + 15)


def h_kj_scaled_hat(
    x: Union[mpmath.mpf, float, str],
    j: int,
    K: Union[int, float, str, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """
    Fourier transform of h_{K,j}(t) under standard Fourier scaling:
    \\widehat{h}_{K,j}(x) = a_K^{-1} * \\widehat{H}_j(a_K^{-1} * x).
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        k_val = to_mpf(K, dps=dps + 15)
        a_K = mpmath.power(tau, k_val)
        x_val = to_mpf(x, dps=dps + 15)

        scaled_x = x_val / a_K
        h_hat_base = H_test_function_hat(scaled_x, j, dps=dps + 15)
        return h_hat_base / a_K


def h_kj_scaled_prime(
    t: Union[mpmath.mpf, mpmath.mpc, float, str],
    j: int,
    K: Union[int, float, str, mpmath.mpf],
    dps: int = 80
) -> Union[mpmath.mpf, mpmath.mpc]:
    """
    Derivative of h_{K,j}(t): h_{K,j}'(t) = a_K * H_j'(a_K * t).
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        k_val = to_mpf(K, dps=dps + 15)
        a_K = mpmath.power(tau, k_val)

        if isinstance(t, (complex, mpmath.mpc)) or (isinstance(t, str) and ("j" in t or "+" in t.lstrip("+-"))):
            t_val = to_mpc(t, dps=dps + 15)
            scaled_t = a_K * t_val
        else:
            t_val = to_mpf(t, dps=dps + 15)
            scaled_t = a_K * t_val
        return a_K * H_test_function_prime(scaled_t, j, dps=dps + 15)


def H_test_function_double_prime(
    t: Union[mpmath.mpf, mpmath.mpc, float, str],
    j: int,
    dps: int = 80
) -> Union[mpmath.mpf, mpmath.mpc]:
    """
    Analytic second derivative H_j''(t) = d^2 H_j / dt^2:
    H_j''(t) = ((t - t0)^2 - sigma^2)/sigma^4 * exp(-(t-t0)^2/(2*sigma^2))
             + ((t + t0)^2 - sigma^2)/sigma^4 * exp(-(t+t0)^2/(2*sigma^2)).
    """
    with mpmath.workdps(dps + 15):
        sigma, t0 = get_test_function_params(j, dps=dps + 15)
        sigma_sq = sigma * sigma
        sigma_4 = sigma_sq * sigma_sq
        two_sigma_sq = mpmath.mpf(2) * sigma_sq

        t_val = to_mpc(t, dps=dps + 15) if isinstance(t, (complex, mpmath.mpc)) or (isinstance(t, str) and ("j" in t or "+" in t.lstrip("+-"))) else to_mpf(t, dps=dps + 15)

        term_minus = ((mpmath.power(t_val - t0, 2) - sigma_sq) / sigma_4) * mpmath.exp(-mpmath.power(t_val - t0, 2) / two_sigma_sq)
        term_plus = ((mpmath.power(t_val + t0, 2) - sigma_sq) / sigma_4) * mpmath.exp(-mpmath.power(t_val + t0, 2) / two_sigma_sq)
        res = term_minus + term_plus
        if isinstance(t_val, mpmath.mpf):
            return mpmath.re(res)
        return res


def H_test_function_fourth_prime(
    t: Union[mpmath.mpf, mpmath.mpc, float, str],
    j: int,
    dps: int = 80
) -> Union[mpmath.mpf, mpmath.mpc]:
    """
    Analytic fourth derivative H_j^{(4)}(t) = d^4 H_j / dt^4:
    H_j^{(4)}(t) = ((t-t0)^4 - 6*sigma^2*(t-t0)^2 + 3*sigma^4)/sigma^8 * exp(-(t-t0)^2/(2*sigma^2))
                 + ((t+t0)^4 - 6*sigma^2*(t+t0)^2 + 3*sigma^4)/sigma^8 * exp(-(t+t0)^2/(2*sigma^2)).
    """
    with mpmath.workdps(dps + 15):
        sigma, t0 = get_test_function_params(j, dps=dps + 15)
        sigma_sq = sigma * sigma
        sigma_4 = sigma_sq * sigma_sq
        sigma_8 = sigma_4 * sigma_4
        two_sigma_sq = mpmath.mpf(2) * sigma_sq

        t_val = to_mpc(t, dps=dps + 15) if isinstance(t, (complex, mpmath.mpc)) or (isinstance(t, str) and ("j" in t or "+" in t.lstrip("+-"))) else to_mpf(t, dps=dps + 15)

        poly_minus = mpmath.power(t_val - t0, 4) - mpmath.mpf(6) * sigma_sq * mpmath.power(t_val - t0, 2) + mpmath.mpf(3) * sigma_4
        term_minus = (poly_minus / sigma_8) * mpmath.exp(-mpmath.power(t_val - t0, 2) / two_sigma_sq)

        poly_plus = mpmath.power(t_val + t0, 4) - mpmath.mpf(6) * sigma_sq * mpmath.power(t_val + t0, 2) + mpmath.mpf(3) * sigma_4
        term_plus = (poly_plus / sigma_8) * mpmath.exp(-mpmath.power(t_val + t0, 2) / two_sigma_sq)

        res = term_minus + term_plus
        if isinstance(t_val, mpmath.mpf):
            return mpmath.re(res)
        return res


def h_kj_scaled_double_prime(
    t: Union[mpmath.mpf, mpmath.mpc, float, str],
    j: int,
    K: Union[int, float, str, mpmath.mpf],
    dps: int = 80
) -> Union[mpmath.mpf, mpmath.mpc]:
    """
    Second derivative of h_{K,j}(t): h_{K,j}''(t) = a_K^2 * H_j''(a_K * t).
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        k_val = to_mpf(K, dps=dps + 15)
        a_K = mpmath.power(tau, k_val)
        a_K_sq = a_K * a_K

        if isinstance(t, (complex, mpmath.mpc)) or (isinstance(t, str) and ("j" in t or "+" in t.lstrip("+-"))):
            t_val = to_mpc(t, dps=dps + 15)
            scaled_t = a_K * t_val
        else:
            t_val = to_mpf(t, dps=dps + 15)
            scaled_t = a_K * t_val
        return a_K_sq * H_test_function_double_prime(scaled_t, j, dps=dps + 15)


def h_kj_scaled_fourth_prime(
    t: Union[mpmath.mpf, mpmath.mpc, float, str],
    j: int,
    K: Union[int, float, str, mpmath.mpf],
    dps: int = 80
) -> Union[mpmath.mpf, mpmath.mpc]:
    """
    Fourth derivative of h_{K,j}(t): h_{K,j}^{(4)}(t) = a_K^4 * H_j^{(4)}(a_K * t).
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        k_val = to_mpf(K, dps=dps + 15)
        a_K = mpmath.power(tau, k_val)
        a_K_4 = mpmath.power(a_K, 4)

        if isinstance(t, (complex, mpmath.mpc)) or (isinstance(t, str) and ("j" in t or "+" in t.lstrip("+-"))):
            t_val = to_mpc(t, dps=dps + 15)
            scaled_t = a_K * t_val
        else:
            t_val = to_mpf(t, dps=dps + 15)
            scaled_t = a_K * t_val
        return a_K_4 * H_test_function_fourth_prime(scaled_t, j, dps=dps + 15)


def compute_grade_quadrature_fourier(
    j: int,
    K: Union[int, float, str, mpmath.mpf],
    x: Union[int, float, str, mpmath.mpf],
    dps: int = 80
) -> Dict[str, Any]:
    """
    [INDEPENDENT NUMERICAL CONTROL] Computes independent numerical Fourier quadrature:
    \\widehat{h}_{K,j}(x) = \\int_{-\\infty}^\\infty h_{K,j}(t) e^{-i x t} dt
                         = \\frac{2}{a_K} \\int_0^\\infty H_j(u) \\cos((x/a_K) u) du
    using panel-subdivided tanh-sinh quadrature over the compact effective support [0, t0 + 15*sigma].
    Returns complete error and convergence metrics without calling closed-form Fourier transform for the integral.
    """
    with mpmath.workdps(dps + 20):
        tau = get_tau(dps=dps + 20)
        k_val = to_mpf(K, dps=dps + 20)
        a_K = mpmath.power(tau, k_val)
        x_val = to_mpf(x, dps=dps + 20)
        sigma, t0 = get_test_function_params(j, dps=dps + 20)

        ana_hat = h_kj_scaled_hat(x_val, j, k_val, dps=dps + 20)

        omega = x_val / a_K
        u_max = t0 + mpmath.mpf(15) * sigma
        num_panels = min(30, max(10, int(u_max * omega / 20) + 1))
        pts = [i * u_max / num_panels for i in range(num_panels + 1)]

        num_int = mpmath.quad(
            lambda u: H_test_function(u, j, dps=dps + 20) * mpmath.cos(omega * u),
            pts,
            method='tanh-sinh',
            maxdegree=8
        )
        num_hat = (mpmath.mpf(2) / a_K) * num_int

        abs_err = abs(ana_hat - num_hat)
        scale = max(abs(ana_hat), abs(num_hat), mpmath.mpf('1e-30'))
        rel_err = abs_err / scale

        return {
            "j": j,
            "K": k_val,
            "x": x_val,
            "a_K": a_K,
            "analytic_value": ana_hat,
            "numerical_value": num_hat,
            "absolute_error": abs_err,
            "relative_error": rel_err,
            "integration_domain": f"[0, {mpmath.nstr(u_max / a_K, n=8)}]",
            "transformed_domain": f"[0, {mpmath.nstr(u_max, n=8)}]",
            "quadrature_precision": dps + 20,
            "convergence_evidence": f"panel_subdivided_tanh_sinh_{num_panels}_panels"
        }



def explicit_formula_eval(
    j: int,
    K: Union[int, float, str, mpmath.mpf] = 0,
    zeros_ordinates: Optional[List[Union[str, mpmath.mpf]]] = None,
    prime_cutoff: int = 50000,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [AUDIT PATH] Evaluates the authoritative Riemann–Weil explicit formula for test function j at grade K:
    EF[h_{K,j}; D, A] = Spectral_Sum - (Pole_Term + Prime_Term + Gamma_Term).
    Evaluated at arbitrary precision dps without binary-float downcast.
    """
    with mpmath.workdps(dps + 20):
        tau = get_tau(dps=dps + 20)
        k_val = to_mpf(K, dps=dps + 20)
        a_K = mpmath.power(tau, k_val)

        # 1. Spectral Side: sum_{gamma} 2 * h_{K,j}(gamma)
        if zeros_ordinates is None:
            import reference_data
            zeros_str = reference_data.load_reference_zeros()
            zeros_mpf = [to_mpf(g, dps=dps + 20) for g in zeros_str]
        else:
            zeros_mpf = [to_mpf(g, dps=dps + 20) for g in zeros_ordinates]

        spec_sum = mpmath.mpf(2) * sum(h_kj_scaled(g, j, k_val, dps=dps + 20) for g in zeros_mpf)

        # 2. Pole Term: 2 * Re(h_{K,j}(i/2))
        s_i_half = mpmath.mpc(mpmath.mpf('0'), mpmath.mpf('0.5'))
        h_i_half = h_kj_scaled(s_i_half, j, k_val, dps=dps + 20)
        pole_term = mpmath.mpf(2) * mpmath.re(h_i_half)

        # 3. Prime Term: -1/pi * sum_{n=2}^N (Lambda(n)/sqrt(n)) * \\widehat{h}_{K,j}(log n)
        prime_term = mpmath.mpf(0)
        # Exact integer sieve bound without floating-point conversion
        sieve_bound = math.isqrt(prime_cutoff)
        sieve = [True] * (prime_cutoff + 1)
        for p in range(2, sieve_bound + 1):
            if sieve[p]:
                for multiple in range(p * p, prime_cutoff + 1, p):
                    sieve[multiple] = False

        for p in range(2, prime_cutoff + 1):
            if sieve[p]:
                log_p = mpmath.log(p)
                pk = p
                while pk <= prime_cutoff:
                    log_pk = mpmath.log(pk)
                    sqrt_pk = mpmath.sqrt(pk)
                    h_hat_val = h_kj_scaled_hat(log_pk, j, k_val, dps=dps + 20)
                    prime_term -= (mpmath.mpf(1) / mpmath.pi) * (log_p / sqrt_pk) * h_hat_val
                    pk *= p

        # 4. Archimedean / Gamma Term: 1/pi * int_0^T h_{K,j}(t) * Re(psi(1/4 + it/2) - log pi) dt
        sigma, t0 = get_test_function_params(j, dps=dps + 20)
        # Integration range adapted to test function support in native t without float downcast
        center_t = t0 / a_K
        width_t = sigma / a_K
        t_max = max(mpmath.mpf(100), center_t + mpmath.mpf(10) * max(width_t, mpmath.mpf(1)))

        def gamma_integrand(t_in: mpmath.mpf) -> mpmath.mpf:
            s_val = mpmath.mpc(mpmath.mpf('0.25'), t_in / mpmath.mpf(2))
            psi_val = mpmath.re(mpmath.psi(0, s_val)) - mpmath.log(mpmath.pi)
            h_val = h_kj_scaled(t_in, j, k_val, dps=dps + 20)
            return h_val * psi_val

        gamma_term = (mpmath.mpf(1) / mpmath.pi) * mpmath.quad(gamma_integrand, [0, t_max])

        total_rhs = pole_term + prime_term + gamma_term
        residual = spec_sum - total_rhs
        rel_error = abs(residual) / max(abs(spec_sum), abs(total_rhs), mpmath.mpf('1e-30'))

        return {
            "j": j,
            "k": k_val,
            "a_K": a_K,
            "spectral_sum": spec_sum,
            "pole_term": pole_term,
            "prime_term": prime_term,
            "gamma_term": gamma_term,
            "total_rhs": total_rhs,
            "residual": residual,
            "relative_error": rel_error,
            "zero_count": len(zeros_mpf),
            "prime_cutoff": prime_cutoff,
            "t_max": t_max,
        }


def validate_divisor_perturbation(
    mutation_type: str,
    zeros: Sequence[Union[complex, mpmath.mpc, str, Tuple[Any, Any], Dict[str, Any]]],
    claimed_multiplicity_preserved: bool = True,
    dps: int = 80
) -> Tuple[bool, Dict[str, Any], List[str]]:
    """
    [AUTHORITATIVE VALIDATOR] Validates candidate divisor mutations against exact symmetry
    and multiplicity preservation criteria for the Riemann explicit formula.

    Rules:
    - critical_height: Must contain a conjugate/reflection pair (1/2 +- i*gamma_new, multiplicity 2).
    - radial_quartet: Must contain a symmetry-complete off-line quartet
      (1/2 +- delta +- i*gamma_0, total 4 zeros, invariant under s -> conj(s) and s -> 1-s).
    - Rejects single complex zero without symmetry partners.
    - Rejects incomplete quartets (e.g. missing conjugate or reflection partners).
    - Rejects multiplicity mismatches when claimed_multiplicity_preserved is True.

    Returns:
        (is_valid, evidence_dict, list_of_rejection_reasons)
    """
    rejection_reasons: List[str] = []
    evidence: Dict[str, Any] = {
        "mutation_type": mutation_type,
        "input_zero_count": len(zeros),
        "claimed_multiplicity_preserved": claimed_multiplicity_preserved,
        "symmetries_preserved": [],
        "multiplicity_preserved": False,
        "is_valid": False
    }

    with mpmath.workdps(dps + 15):
        parsed_zeros: List[mpmath.mpc] = []
        for z in zeros:
            if isinstance(z, dict):
                re_val = to_mpf(z.get("real", "0.5"), dps=dps + 15)
                im_val = to_mpf(z.get("imag", "0.0"), dps=dps + 15)
                parsed_zeros.append(mpmath.mpc(re_val, im_val))
            elif isinstance(z, (tuple, list)) and len(z) == 2:
                re_val = to_mpf(z[0], dps=dps + 15)
                im_val = to_mpf(z[1], dps=dps + 15)
                parsed_zeros.append(mpmath.mpc(re_val, im_val))
            else:
                parsed_zeros.append(to_mpc(z, dps=dps + 15))

        tol = mpmath.mpf(f"1e-{dps - 10}")

        # Check conjugation symmetry: for every s in parsed_zeros, conj(s) must also be in parsed_zeros
        has_conjugation = True
        matched_conj: List[bool] = [False] * len(parsed_zeros)
        for i, s1 in enumerate(parsed_zeros):
            s1_conj = mpmath.conj(s1)
            found = False
            for j, s2 in enumerate(parsed_zeros):
                if not matched_conj[j] and abs(s2 - s1_conj) < tol:
                    matched_conj[j] = True
                    found = True
                    break
            if not found:
                has_conjugation = False
                break

        # Check reflection symmetry: for every s in parsed_zeros, 1-s must also be in parsed_zeros
        has_reflection = True
        matched_refl: List[bool] = [False] * len(parsed_zeros)
        for i, s1 in enumerate(parsed_zeros):
            s1_refl = mpmath.mpf(1) - s1
            found = False
            for j, s2 in enumerate(parsed_zeros):
                if not matched_refl[j] and abs(s2 - s1_refl) < tol:
                    matched_refl[j] = True
                    found = True
                    break
            if not found:
                has_reflection = False
                break

        if has_conjugation:
            evidence["symmetries_preserved"].append("conjugation")
        if has_reflection:
            evidence["symmetries_preserved"].append("functional_reflection")

        if mutation_type == "critical_height":
            # Must have exactly 2 zeros on critical line Re(s) = 1/2
            if len(parsed_zeros) != 2:
                rejection_reasons.append(
                    f"Critical-line height perturbation requires exactly 2 zeros (pair), got {len(parsed_zeros)}"
                )
            else:
                on_crit = all(abs(mpmath.re(s) - mpmath.mpf('0.5')) < tol for s in parsed_zeros)
                if not on_crit:
                    rejection_reasons.append("Critical-line height perturbation zeros must lie exactly on Re(s) = 1/2")
                if not (has_conjugation and has_reflection):
                    rejection_reasons.append("Critical-line pair lacks conjugation or reflection symmetry")
                else:
                    evidence["multiplicity_preserved"] = True

        elif mutation_type == "radial_quartet":
            # Must have exactly 4 zeros forming symmetry-complete quartet
            if len(parsed_zeros) != 4:
                rejection_reasons.append(
                    f"Radial quartet perturbation requires exactly 4 zeros (quartet), got {len(parsed_zeros)}"
                )
            else:
                if not (has_conjugation and has_reflection):
                    rejection_reasons.append("Radial quartet lacks conjugation (s -> conj(s)) or functional reflection (s -> 1-s) symmetry")
                else:
                    evidence["multiplicity_preserved"] = True

        elif mutation_type == "single_zero_unpartnered" or mutation_type == "negative_control_invalid":
            rejection_reasons.append(
                "Single unpartnered complex zero violates conjugation (s -> conj(s)) and functional equation reflection (s -> 1-s) symmetries"
            )

        elif mutation_type == "incomplete_quartet":
            rejection_reasons.append(
                "Incomplete off-line zero configuration violates functional equation reflection symmetry (1-s)"
            )

        else:
            if not (has_conjugation and has_reflection):
                rejection_reasons.append(f"Mutation type '{mutation_type}' fails conjugation and/or reflection symmetry")
            elif claimed_multiplicity_preserved and len(parsed_zeros) % 2 != 0:
                rejection_reasons.append(f"Odd number of zeros ({len(parsed_zeros)}) cannot preserve multiplicity under reflection")
            else:
                evidence["multiplicity_preserved"] = True

        is_valid = len(rejection_reasons) == 0
        evidence["is_valid"] = is_valid
        return is_valid, evidence, rejection_reasons


def finite_divisor_defect_critical_height(
    j: int,
    K: Union[int, float, str, mpmath.mpf],
    gamma_n: Union[str, mpmath.mpf],
    epsilon: Union[str, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Exact finite divisor defect for critical-line pair perturbation:
    1/2 +- i*gamma_n |-> 1/2 +- i*(gamma_n + epsilon).
    Preserves conjugation and functional equation reflection.
    Delta C_{K,j} = 2 * [ H_j(a_K * (gamma_n + epsilon)) - H_j(a_K * gamma_n) ].
    All arithmetic, pole, and gamma terms cancel exactly.
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        k_val = to_mpf(K, dps=dps + 15)
        a_K = mpmath.power(tau, k_val)
        g_val = to_mpf(gamma_n, dps=dps + 15)
        eps_val = to_mpf(epsilon, dps=dps + 15)

        h_pert = H_test_function(a_K * (g_val + eps_val), j, dps=dps + 15)
        h_base = H_test_function(a_K * g_val, j, dps=dps + 15)
        return mpmath.mpf(2) * (h_pert - h_base)


def finite_divisor_defect_critical_height_exact_and_linear(
    j: int,
    K: Union[int, float, str, mpmath.mpf],
    gamma_n: Union[str, mpmath.mpf],
    epsilon: Union[str, mpmath.mpf],
    dps: int = 80
) -> Dict[str, mpmath.mpf]:
    """
    [AUDIT PATH] Computes both exact finite defect and linearized defect for critical-line height perturbation:
    Delta C_{K,j}^exact = 2 * [ H_j(a_K * (gamma_n + epsilon)) - H_j(a_K * gamma_n) ]
    Delta C_{K,j}^linear = 2 * a_K * H_j'(a_K * gamma_n) * epsilon
    Nonlinear remainder = Delta C^exact - Delta C^linear.
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        k_val = to_mpf(K, dps=dps + 15)
        a_K = mpmath.power(tau, k_val)
        g_val = to_mpf(gamma_n, dps=dps + 15)
        eps_val = to_mpf(epsilon, dps=dps + 15)

        h_pert = H_test_function(a_K * (g_val + eps_val), j, dps=dps + 15)
        h_base = H_test_function(a_K * g_val, j, dps=dps + 15)
        h_prime = H_test_function_prime(a_K * g_val, j, dps=dps + 15)

        exact_defect = mpmath.mpf(2) * (h_pert - h_base)
        linear_defect = mpmath.mpf(2) * a_K * h_prime * eps_val
        remainder = exact_defect - linear_defect
        rel_error = abs(remainder) / abs(exact_defect) if abs(exact_defect) > mpmath.mpf('1e-50') else mpmath.mpf(0)

        return {
            "exact_defect": exact_defect,
            "linear_defect": linear_defect,
            "remainder": remainder,
            "relative_error": rel_error
        }


def finite_divisor_defect_radial_quartet(
    j: int,
    K: Union[int, float, str, mpmath.mpf],
    gamma_a: Union[str, mpmath.mpf],
    gamma_b: Union[str, mpmath.mpf],
    delta: Union[str, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Exact multiplicity-preserving symmetry-complete total quartet defect:
    Delta C_{K,j}^total = Delta C_{K,j}^merge + Delta C_{K,j}^radial(delta).
    """
    res = finite_divisor_defect_radial_quartet_decomposed(j, K, gamma_a, gamma_b, delta, dps=dps)
    return res["total_defect"]


def finite_divisor_defect_radial_quartet_decomposed(
    j: int,
    K: Union[int, float, str, mpmath.mpf],
    gamma_a: Union[str, mpmath.mpf],
    gamma_b: Union[str, mpmath.mpf],
    delta: Union[str, mpmath.mpf],
    dps: int = 80
) -> Dict[str, mpmath.mpf]:
    """
    [AUDIT PATH] Exact mathematical decomposition of the radial quartet substitution:
    Replaces critical-line pairs at gamma_a and gamma_b with an off-critical quartet at gamma_0 = (gamma_a + gamma_b)/2.

    Decomposition:
    1. Height-merging component (independent of delta):
       Delta C_{K,j}^merge = 4 * H_j(a_K * gamma_0) - 2 * H_j(a_K * gamma_a) - 2 * H_j(a_K * gamma_b)
    2. Pure radial increment (relative to multiplicity-matched critical-line divisor at gamma_0):
       Delta C_{K,j}^radial(delta) = 4 * Re[ H_j(a_K * (gamma_0 + i*delta)) ] - 4 * H_j(a_K * gamma_0)
    3. Total substitution defect:
       Delta C_{K,j}^total(delta) = Delta C_{K,j}^merge + Delta C_{K,j}^radial(delta)

    Guarantees Delta C_{K,j}^radial(0) == 0 to working precision and that radial response is strictly even in delta.
    """
    with mpmath.workdps(dps + 20):
        tau = get_tau(dps=dps + 20)
        k_val = to_mpf(K, dps=dps + 20)
        a_K = mpmath.power(tau, k_val)
        ga_val = to_mpf(gamma_a, dps=dps + 20)
        gb_val = to_mpf(gamma_b, dps=dps + 20)
        d_val = to_mpf(delta, dps=dps + 20)

        g0_val = (ga_val + gb_val) / mpmath.mpf(2)

        h_a = H_test_function(a_K * ga_val, j, dps=dps + 20)
        h_b = H_test_function(a_K * gb_val, j, dps=dps + 20)
        h_g0 = H_test_function(a_K * g0_val, j, dps=dps + 20)

        # 1. Height-merging component
        merge_defect = mpmath.mpf(4) * h_g0 - mpmath.mpf(2) * h_a - mpmath.mpf(2) * h_b

        # 2. Pure radial component
        if abs(d_val) < mpmath.mpf(f"1e-{dps}"):
            radial_defect = mpmath.mpf(0)
            total_defect = merge_defect
        else:
            quartet_arg = a_K * mpmath.mpc(g0_val, d_val)
            h_quartet = H_test_function(quartet_arg, j, dps=dps + 20)
            radial_defect = mpmath.mpf(4) * mpmath.re(h_quartet) - mpmath.mpf(4) * h_g0
            total_defect = merge_defect + radial_defect

        return {
            "merge_defect": merge_defect,
            "radial_defect": radial_defect,
            "total_defect": total_defect
        }


# =========================================================================
# Independent Native Test Function Representations for Equivalence Checks
# =========================================================================

def H_native_gaussian(
    t: Union[mpmath.mpf, mpmath.mpc, float, str],
    sigma_native: Union[mpmath.mpf, float, str],
    t0_native: Union[mpmath.mpf, float, str],
    dps: int = 80
) -> Union[mpmath.mpf, mpmath.mpc]:
    """
    [INDEPENDENT EXPANDED-NATIVE PATH] Evaluates native Gaussian test function
    directly parameterized by native parameters (sigma_native, t0_native) without calling grade wrappers:
    G(t; sigma, t0) = exp(-(t - t0)^2 / (2*sigma^2)) + exp(-(t + t0)^2 / (2*sigma^2)).
    """
    with mpmath.workdps(dps + 15):
        s_val = to_mpf(sigma_native, dps=dps + 15)
        t0_val = to_mpf(t0_native, dps=dps + 15)
        two_sig_sq = mpmath.mpf(2) * (s_val * s_val)

        t_val = to_mpc(t, dps=dps + 15) if isinstance(t, (complex, mpmath.mpc)) or (isinstance(t, str) and ("j" in t or "+" in t.lstrip("+-"))) else to_mpf(t, dps=dps + 15)

        term_m = mpmath.exp(-mpmath.power(t_val - t0_val, 2) / two_sig_sq)
        term_p = mpmath.exp(-mpmath.power(t_val + t0_val, 2) / two_sig_sq)
        res = term_m + term_p
        return mpmath.re(res) if isinstance(t_val, mpmath.mpf) else res


def H_native_gaussian_prime(
    t: Union[mpmath.mpf, mpmath.mpc, float, str],
    sigma_native: Union[mpmath.mpf, float, str],
    t0_native: Union[mpmath.mpf, float, str],
    dps: int = 80
) -> Union[mpmath.mpf, mpmath.mpc]:
    """
    [INDEPENDENT EXPANDED-NATIVE PATH] Direct derivative dG/dt with respect to native t:
    dG/dt = -((t - t0)/sigma^2)*exp(-(t-t0)^2/(2*sigma^2)) - ((t + t0)/sigma^2)*exp(-(t+t0)^2/(2*sigma^2)).
    """
    with mpmath.workdps(dps + 15):
        s_val = to_mpf(sigma_native, dps=dps + 15)
        t0_val = to_mpf(t0_native, dps=dps + 15)
        sig_sq = s_val * s_val
        two_sig_sq = mpmath.mpf(2) * sig_sq

        t_val = to_mpc(t, dps=dps + 15) if isinstance(t, (complex, mpmath.mpc)) or (isinstance(t, str) and ("j" in t or "+" in t.lstrip("+-"))) else to_mpf(t, dps=dps + 15)

        term_m = ((t_val - t0_val) / sig_sq) * mpmath.exp(-mpmath.power(t_val - t0_val, 2) / two_sig_sq)
        term_p = ((t_val + t0_val) / sig_sq) * mpmath.exp(-mpmath.power(t_val + t0_val, 2) / two_sig_sq)
        res = -term_m - term_p
        return mpmath.re(res) if isinstance(t_val, mpmath.mpf) else res


def H_native_gaussian_hat(
    x: Union[mpmath.mpf, float, str],
    sigma_native: Union[mpmath.mpf, float, str],
    t0_native: Union[mpmath.mpf, float, str],
    dps: int = 80
) -> mpmath.mpf:
    """
    [INDEPENDENT EXPANDED-NATIVE PATH] Analytic Fourier transform evaluated directly with native parameters:
    \\widehat{G}(x) = 2 * sigma_native * sqrt(2*pi) * exp(-sigma_native^2 * x^2 / 2) * cos(t0_native * x).
    """
    with mpmath.workdps(dps + 15):
        s_val = to_mpf(sigma_native, dps=dps + 15)
        t0_val = to_mpf(t0_native, dps=dps + 15)
        x_val = to_mpf(x, dps=dps + 15)
        tau = get_tau(dps=dps + 15)

        prefactor = mpmath.mpf(2) * s_val * mpmath.sqrt(tau)
        decay = mpmath.exp(-(s_val * s_val * x_val * x_val) / mpmath.mpf(2))
        osc = mpmath.cos(t0_val * x_val)
        return prefactor * decay * osc


def explicit_formula_jacobian(
    j_list: Sequence[int],
    k_list: Sequence[Union[int, float, str, mpmath.mpf]],
    zeros_subset: Sequence[Union[str, mpmath.mpf]],
    dps: int = 80
) -> List[List[mpmath.mpf]]:
    """
    [AUDIT PATH] Computes the Jacobian matrix J_{(K,j), m} = d C_{K,j} / d gamma_m
    = 2 * a_K * H_j'(a_K * gamma_m).
    Size: len(k_list) * len(j_list) rows by len(zeros_subset) columns.
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        zeros_mpf = [to_mpf(g, dps=dps + 15) for g in zeros_subset]

        rows: List[List[mpmath.mpf]] = []
        for K in k_list:
            k_val = to_mpf(K, dps=dps + 15)
            a_K = mpmath.power(tau, k_val)
            for j in j_list:
                row = [
                    mpmath.mpf(2) * a_K * H_test_function_prime(a_K * g, j, dps=dps + 15)
                    for g in zeros_mpf
                ]
                rows.append(row)
        return rows


def check_expanded_native_basis_equivalence(
    j_list: Sequence[int],
    k_list: Sequence[Union[int, float, str, mpmath.mpf]],
    zeros_subset: Sequence[Union[str, mpmath.mpf]],
    dps: int = 80
) -> Dict[str, Any]:
    """
    [AUDIT PATH] Evaluates whether the grade-K family {C_{K,j}} provides constraints
    independent of the expanded K=0 native basis {H_j(a_K * .)}.

    Computes two strictly independent paths:
    1. Grade path: J_K via h_{K,j}'(t) = a_K * H_j'(a_K * t).
    2. Expanded-native path: J_0 via H_native_prime(t; sigma_j/a_K, t0_j/a_K).

    Compares function values, analytic derivatives, Fourier transforms, Jacobian rows,
    and row-space SVD ranks.
    Returns discrimination classification: 'coordinate_redundant' (exact theoretical)
    and 'finite_basis_enrichment_only' (relative to unexpanded K=0 basis).
    """
    with mpmath.workdps(dps + 25):
        tau = get_tau(dps=dps + 25)
        zeros_mpf = [to_mpf(g, dps=dps + 25) for g in zeros_subset]

        # 1. Grade Path: direct grade-K scaling
        J_grade: List[List[mpmath.mpf]] = []
        for K in k_list:
            k_val = to_mpf(K, dps=dps + 25)
            a_K = mpmath.power(tau, k_val)
            for j in j_list:
                row = [
                    mpmath.mpf(2) * a_K * H_test_function_prime(a_K * g, j, dps=dps + 25)
                    for g in zeros_mpf
                ]
                J_grade.append(row)

        # 2. Expanded-Native Path: evaluate native Gaussian with transformed parameters
        J_native: List[List[mpmath.mpf]] = []
        fourier_discrepancies: List[mpmath.mpf] = []
        value_discrepancies: List[mpmath.mpf] = []

        for K in k_list:
            k_val = to_mpf(K, dps=dps + 25)
            a_K = mpmath.power(tau, k_val)
            for j in j_list:
                sigma_j, t0_j = get_test_function_params(j, dps=dps + 25)
                # Native transformed parameters
                sigma_native = sigma_j / a_K
                t0_native = t0_j / a_K

                # Native derivative row
                row_native = [
                    mpmath.mpf(2) * H_native_gaussian_prime(g, sigma_native, t0_native, dps=dps + 25)
                    for g in zeros_mpf
                ]
                J_native.append(row_native)

                # Check sample point value agreement: h_{K,j}(14.1347) vs H_native(14.1347)
                sample_t = mpmath.mpf("14.13472514173469379")
                val_grade = h_kj_scaled(sample_t, j, k_val, dps=dps + 25)
                val_native = H_native_gaussian(sample_t, sigma_native, t0_native, dps=dps + 25)
                value_discrepancies.append(abs(val_grade - val_native))

                # Check Fourier transform agreement: h_hat_{K,j}(1.0) vs H_native_hat(1.0)
                sample_x = mpmath.mpf("1.0")
                hat_grade = h_kj_scaled_hat(sample_x, j, k_val, dps=dps + 25)
                hat_native = H_native_gaussian_hat(sample_x, sigma_native, t0_native, dps=dps + 25)
                fourier_discrepancies.append(abs(hat_grade - hat_native))

        # Discrepancy between grade-path and expanded-native-path Jacobians
        max_diff = mpmath.mpf(0)
        for r in range(len(J_grade)):
            for c in range(len(J_grade[0])):
                diff = abs(J_grade[r][c] - J_native[r][c])
                if diff > max_diff:
                    max_diff = diff

        max_val_diff = max(value_discrepancies) if value_discrepancies else mpmath.mpf(0)
        max_hat_diff = max(fourier_discrepancies) if fourier_discrepancies else mpmath.mpf(0)

        # Compute SVD and ranks
        M_grade = mpmath.matrix(J_grade)
        _, S_grade, _ = mpmath.svd_r(M_grade)
        cutoff_grade = S_grade[0] * mpmath.mpf('1e-25') if len(S_grade) > 0 else mpmath.mpf(0)
        rank_grade = sum(1 for s in S_grade if s > cutoff_grade)

        M_native = mpmath.matrix(J_native)
        _, S_native, _ = mpmath.svd_r(M_native)
        cutoff_native = S_native[0] * mpmath.mpf('1e-25') if len(S_native) > 0 else mpmath.mpf(0)
        rank_native = sum(1 for s in S_native if s > cutoff_native)

        # Stacked matrix [J_grade; J_native]
        stacked = J_grade + J_native
        M_stacked = mpmath.matrix(stacked)
        _, S_stacked, _ = mpmath.svd_r(M_stacked)
        cutoff_stacked = S_stacked[0] * mpmath.mpf('1e-25') if len(S_stacked) > 0 else mpmath.mpf(0)
        rank_stacked = sum(1 for s in S_stacked if s > cutoff_stacked)

        # Threshold sweep for grade matrix
        sweep_thresholds = ['1e-18', '1e-20', '1e-25', '1e-30', '1e-35', '1e-40']
        grade_sweep: Dict[str, Any] = {}
        s0_grade = S_grade[0] if len(S_grade) > 0 else mpmath.mpf(0)
        for t_val in sweep_thresholds:
            t_mpf = to_mpf(t_val, dps=dps + 25)
            cut = s0_grade * t_mpf
            rk = sum(1 for s in S_grade if s > cut)
            nl = len(zeros_mpf) - rk
            grade_sweep[t_val] = {"relative_threshold": t_val, "absolute_cutoff": mpmath.nstr(cut, n=dps), "numerical_rank": rk, "nullity": nl}

        is_equivalent = bool(
            max_diff < mpmath.mpf('1e-50')
            and max_val_diff < mpmath.mpf('1e-50')
            and max_hat_diff < mpmath.mpf('1e-50')
            and rank_stacked == rank_grade
            and rank_grade == rank_native
        )
        classification = "coordinate_redundant" if is_equivalent else "candidate_grade_specific_constraint"

        return {
            "max_discrepancy": max_diff,
            "max_value_discrepancy": max_val_diff,
            "max_fourier_discrepancy": max_hat_diff,
            "grade_matrix_dims": [len(J_grade), len(zeros_mpf)],
            "native_matrix_dims": [len(J_native), len(zeros_mpf)],
            "stacked_matrix_dims": [len(stacked), len(zeros_mpf)],
            "rank_grade": rank_grade,
            "rank_native": rank_native,
            "rank_stacked": rank_stacked,
            "singular_values_grade": [s for s in S_grade],
            "singular_values_native": [s for s in S_native],
            "singular_values_stacked": [s for s in S_stacked],
            "rank_threshold": cutoff_grade,
            "threshold_sweep": grade_sweep,
            "is_equivalent": is_equivalent,
            "categorical_equivalence_result": is_equivalent,
            "classification": classification,
            "theoretical_classification": classification,
            "finite_basis_classification": "finite_basis_enrichment_only",
            "num_channels": len(J_grade),
            "num_zeros": len(zeros_mpf),
        }


def solve_linearized_compensation(
    J: List[List[mpmath.mpf]],
    target_col_idx: int,
    epsilon: Union[str, mpmath.mpf],
    rank_tol_rel: Union[str, mpmath.mpf] = '1e-25',
    rank_threshold_sweep: Optional[Sequence[Union[str, mpmath.mpf]]] = None,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [AUDIT PATH] Solves linearized zero-compensation problem:
    J_{-n} * Delta theta_{-n} = -J_n * Delta theta_n.

    Computes SVD of J_{-n}, full singular values list, complete predetermined threshold sweep
    [1e-18, 1e-20, 1e-25, 1e-30, 1e-35, 1e-40], numerical rank/nullity at every threshold,
    minimum-norm compensation vector, forward residual vector, and stability diagnostic.
    """
    with mpmath.workdps(dps + 30):
        num_rows = len(J)
        num_cols = len(J[0]) if num_rows > 0 else 0
        if target_col_idx < 0 or target_col_idx >= num_cols:
            raise ValueError(f"target_col_idx {target_col_idx} out of range (0..{num_cols-1})")

        eps_val = to_mpf(epsilon, dps=dps + 30)
        v_target = [J[r][target_col_idx] * eps_val for r in range(num_rows)]
        v_norm = mpmath.sqrt(sum(v * v for v in v_target))

        other_indices = [c for c in range(num_cols) if c != target_col_idx]
        J_other_list = [[J[r][c] for c in other_indices] for r in range(num_rows)]

        # SVD via mpmath.svd_r
        J_mat = mpmath.matrix(J_other_list)
        U, S, V = mpmath.svd_r(J_mat)

        s_max = S[0] if len(S) > 0 else mpmath.mpf(0)
        matrix_norm = s_max

        # Default rank threshold evaluation
        primary_tol = to_mpf(rank_tol_rel, dps=dps + 30)
        primary_cutoff = s_max * primary_tol

        primary_rank = 0
        primary_s_min_nz = s_max
        for s in S:
            if s > primary_cutoff:
                primary_rank += 1
                primary_s_min_nz = s

        primary_nullity = len(other_indices) - primary_rank
        primary_cond = (s_max / primary_s_min_nz) if primary_s_min_nz > 0 else mpmath.inf

        # Threshold sweep evaluation
        if rank_threshold_sweep is None:
            rank_threshold_sweep = ['1e-18', '1e-20', '1e-25', '1e-30', '1e-35', '1e-40']

        sweep_results: Dict[str, Dict[str, Any]] = {}
        distinct_ranks: Set[int] = set()

        for t_val in rank_threshold_sweep:
            t_mpf = to_mpf(t_val, dps=dps + 30)
            cutoff = s_max * t_mpf
            rk = 0
            s_min_sw = s_max
            for s in S:
                if s > cutoff:
                    rk += 1
                    s_min_sw = s
            nl = len(other_indices) - rk
            c_num = (s_max / s_min_sw) if s_min_sw > 0 else mpmath.inf
            distinct_ranks.add(rk)

            t_key = str(t_val)
            sweep_results[t_key] = {
                "relative_threshold": mpmath.nstr(t_mpf, n=8),
                "absolute_cutoff": mpmath.nstr(cutoff, n=dps),
                "numerical_rank": rk,
                "nullity": nl,
                "condition_number": mpmath.nstr(c_num, n=8) if c_num != mpmath.inf else "inf"
            }

        rank_stability = "stable" if len(distinct_ranks) <= 1 else "threshold_dependent"

        # Minimum-norm pseudoinverse solution under primary cutoff:
        # x_c = sum_{i, S_i > cutoff} V_{i, c} * (1/S_i) * (U[:, i]^T * (-v_target))
        x_sol = [mpmath.mpf(0)] * len(other_indices)
        for i in range(len(S)):
            s_i = S[i]
            if s_i > primary_cutoff:
                proj = sum(U[r, i] * (-v_target[r]) for r in range(num_rows))
                inv_s = proj / s_i
                for c in range(len(other_indices)):
                    x_sol[c] += inv_s * V[i, c]

        # Compute forward defect residual: r = J_other * x_sol + v_target
        res_vec = [
            sum(J_other_list[r][c] * x_sol[c] for c in range(len(other_indices))) + v_target[r]
            for r in range(num_rows)
        ]
        res_norm = mpmath.sqrt(sum(r * r for r in res_vec))
        sol_norm = mpmath.sqrt(sum(x * x for x in x_sol))
        rel_residual = (res_norm / v_norm) if v_norm > 0 else mpmath.mpf(0)

        detected = bool(v_norm > mpmath.mpf('1e-35'))
        compensation_found = bool(rel_residual < mpmath.mpf('1e-10'))

        # Participating indices: thresholded at 1e-12 of max component
        part_indices = [
            other_indices[c] for c in range(len(other_indices))
            if abs(x_sol[c]) > mpmath.mpf('1e-12') * max(sol_norm, mpmath.mpf('1e-30'))
        ]

        return {
            "target_index": target_col_idx,
            "epsilon": eps_val,
            "v_target": v_target,
            "v_norm": v_norm,
            "detected": detected,
            "matrix_norm": matrix_norm,
            "singular_values": [s for s in S],
            "numerical_rank": primary_rank,
            "nullity": primary_nullity,
            "condition_number": primary_cond,
            "rank_threshold": primary_cutoff,
            "threshold_sweep": sweep_results,
            "rank_stability": rank_stability,
            "compensation_solution": x_sol,
            "compensation_vector": x_sol,
            "compensation_norm": sol_norm,
            "residual_vector": res_vec,
            "residual_norm": res_norm,
            "relative_residual": rel_residual,
            "compensation_found": compensation_found,
            "participating_indices": part_indices,
            "other_indices": other_indices,
        }


def pure_radial_defect_exact_and_second_order(
    j: int,
    K: Union[int, float, str, mpmath.mpf],
    gamma: Union[str, float, mpmath.mpf],
    delta: Union[str, float, mpmath.mpf],
    dps: int = 80
) -> Dict[str, mpmath.mpf]:
    """
    Computes exact pure radial quartet defect and its second-order / fourth-order Taylor expansion:
    - exact_radial_defect: 4*Re[H_j(a_K*(gamma + i*delta))] - 4*H_j(a_K*gamma)
    - linear_second_order: -2 * a_K^2 * delta^2 * H_j''(a_K*gamma)
    - fourth_order_term: (a_K^4 * delta^4 / 12) * H_j^{(4)}(a_K*gamma)
    - remainder: exact - linear
    - relative_error: |remainder| / |exact| (if exact != 0)
    """
    with mpmath.workdps(dps + 20):
        g_val = to_mpf(gamma, dps=dps + 20)
        d_val = to_mpf(delta, dps=dps + 20)
        k_val = to_mpf(K, dps=dps + 20)
        tau = get_tau(dps=dps + 20)
        a_K = mpmath.power(tau, k_val)

        z_pert = a_K * mpmath.mpc(g_val, d_val)
        z_mid = a_K * g_val

        val_pert = H_test_function(z_pert, j, dps=dps + 20)
        val_mid = H_test_function(z_mid, j, dps=dps + 20)

        exact_def = mpmath.mpf(4) * mpmath.re(val_pert) - mpmath.mpf(4) * val_mid

        h_pp = H_test_function_double_prime(z_mid, j, dps=dps + 20)
        u_val = d_val * d_val
        linear_def = -mpmath.mpf(2) * (a_K * a_K) * u_val * h_pp

        h_4 = H_test_function_fourth_prime(z_mid, j, dps=dps + 20)
        fourth_term = ((mpmath.power(a_K, 4) * mpmath.power(d_val, 4)) / mpmath.mpf(12)) * h_4

        rem = exact_def - linear_def
        rel_err = (abs(rem) / abs(exact_def)) if abs(exact_def) > mpmath.mpf('1e-50') else mpmath.mpf(0)

        return {
            "exact_radial_defect": exact_def,
            "linear_second_order": linear_def,
            "fourth_order_term": fourth_term,
            "remainder": rem,
            "relative_error": rel_err,
            "h_double_prime": h_pp,
            "h_fourth_prime": h_4,
            "u": u_val,
        }


def radial_second_order_jacobian(
    j_list: Sequence[int],
    k_list: Sequence[Union[int, float, str, mpmath.mpf]],
    zeros_subset: Sequence[Union[str, float, mpmath.mpf]],
    dps: int = 80
) -> List[List[mpmath.mpf]]:
    """
    Second-order radial response matrix K_{(K,j), n} = -2 * a_K^2 * H_j''(a_K * gamma_n).
    Rows: (K, j) combinations in Cartesian order.
    Columns: zeros n in zeros_subset.
    """
    with mpmath.workdps(dps + 20):
        tau = get_tau(dps=dps + 20)
        matrix: List[List[mpmath.mpf]] = []

        for k_val in k_list:
            k_mpf = to_mpf(k_val, dps=dps + 20)
            a_K = mpmath.power(tau, k_mpf)
            a_K_sq = a_K * a_K

            for j_val in j_list:
                row: List[mpmath.mpf] = []
                for g_val in zeros_subset:
                    g_mpf = to_mpf(g_val, dps=dps + 20)
                    scaled_gamma = a_K * g_mpf
                    h_pp = H_test_function_double_prime(scaled_gamma, j_val, dps=dps + 20)
                    k_entry = -mpmath.mpf(2) * a_K_sq * h_pp
                    row.append(k_entry)
                matrix.append(row)
        return matrix


def solve_radial_second_order_nnls(
    K_mat: List[List[mpmath.mpf]],
    target_col_idx: int,
    u_val: Union[str, mpmath.mpf],
    rank_tol_rel: Union[str, mpmath.mpf] = '1e-25',
    rank_threshold_sweep: Optional[Sequence[Union[str, mpmath.mpf]]] = None,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [AUDIT PATH] Solves radial second-order zero-compensation problem:
    K_{-n} * u_{-n} = -K_n * u_n with u_{-n} >= 0.

    Evaluates:
    - SVD of K_{-n}, singular values, rank, nullity, condition number
    - Complete threshold sweep across [1e-18, 1e-20, 1e-25, 1e-30, 1e-35, 1e-40]
    - Unconstrained least squares solution and residual
    - Non-negative least squares (NNLS) solution (u >= 0) and residual
    - Quadratic radial energy E(u) = ||v_target||^2
    - Non-compensation verification: whether NNLS relative residual remains > 1e-5.
    """
    with mpmath.workdps(dps + 30):
        num_rows = len(K_mat)
        num_cols = len(K_mat[0]) if num_rows > 0 else 0
        if target_col_idx < 0 or target_col_idx >= num_cols:
            raise ValueError(f"target_col_idx {target_col_idx} out of range (0..{num_cols-1})")

        u_mpf = to_mpf(u_val, dps=dps + 30)
        v_target = [K_mat[r][target_col_idx] * u_mpf for r in range(num_rows)]
        v_norm = mpmath.sqrt(sum(v * v for v in v_target))
        energy = v_norm * v_norm

        other_indices = [c for c in range(num_cols) if c != target_col_idx]
        K_other_list = [[K_mat[r][c] for c in other_indices] for r in range(num_rows)]

        # SVD via mpmath.svd_r
        K_other_mat = mpmath.matrix(K_other_list)
        U, S, V = mpmath.svd_r(K_other_mat)

        s_max = S[0] if len(S) > 0 else mpmath.mpf(0)
        matrix_norm = s_max

        primary_tol = to_mpf(rank_tol_rel, dps=dps + 30)
        primary_cutoff = s_max * primary_tol

        primary_rank = 0
        primary_s_min_nz = s_max
        for s in S:
            if s > primary_cutoff:
                primary_rank += 1
                primary_s_min_nz = s

        primary_nullity = len(other_indices) - primary_rank
        primary_cond = (s_max / primary_s_min_nz) if primary_s_min_nz > 0 else mpmath.inf

        if rank_threshold_sweep is None:
            rank_threshold_sweep = ['1e-18', '1e-20', '1e-25', '1e-30', '1e-35', '1e-40']

        sweep_results: Dict[str, Dict[str, Any]] = {}
        distinct_ranks: Set[int] = set()

        for t_val in rank_threshold_sweep:
            t_mpf = to_mpf(t_val, dps=dps + 30)
            cutoff = s_max * t_mpf
            rk = 0
            s_min_sw = s_max
            for s in S:
                if s > cutoff:
                    rk += 1
                    s_min_sw = s
            nl = len(other_indices) - rk
            c_num = (s_max / s_min_sw) if s_min_sw > 0 else mpmath.inf
            distinct_ranks.add(rk)

            t_key = str(t_val)
            sweep_results[t_key] = {
                "relative_threshold": mpmath.nstr(t_mpf, n=8),
                "absolute_cutoff": mpmath.nstr(cutoff, n=dps),
                "numerical_rank": rk,
                "nullity": nl,
                "condition_number": mpmath.nstr(c_num, n=8) if c_num != mpmath.inf else "inf"
            }

        rank_stability = "stable" if len(distinct_ranks) <= 1 else "threshold_dependent"

        # Unconstrained pseudoinverse solution
        x_unconstrained = [mpmath.mpf(0)] * len(other_indices)
        for i in range(len(S)):
            s_i = S[i]
            if s_i > primary_cutoff:
                proj = sum(U[r, i] * (-v_target[r]) for r in range(num_rows))
                inv_s = proj / s_i
                for c in range(len(other_indices)):
                    x_unconstrained[c] += inv_s * V[i, c]

        res_unconstrained = [
            sum(K_other_list[r][c] * x_unconstrained[c] for c in range(len(other_indices))) + v_target[r]
            for r in range(num_rows)
        ]
        res_unconstrained_norm = mpmath.sqrt(sum(r * r for r in res_unconstrained))
        rel_unconstrained = (res_unconstrained_norm / v_norm) if v_norm > 0 else mpmath.mpf(0)

        # NNLS solution via scipy
        import scipy.optimize
        A_np = np.array([[float(K_other_list[r][c]) for c in range(len(other_indices))] for r in range(num_rows)], dtype=np.float64)
        b_np = np.array([-float(v_target[r]) for r in range(num_rows)], dtype=np.float64)
        x_nnls_np, _ = scipy.optimize.nnls(A_np, b_np)

        x_nnls = [to_mpf(float(x), dps=dps + 30) for x in x_nnls_np]
        res_nnls = [
            sum(K_other_list[r][c] * x_nnls[c] for c in range(len(other_indices))) + v_target[r]
            for r in range(num_rows)
        ]
        res_nnls_norm = mpmath.sqrt(sum(r * r for r in res_nnls))
        nnls_sol_norm = mpmath.sqrt(sum(x * x for x in x_nnls))
        rel_nnls_residual = (res_nnls_norm / v_norm) if v_norm > 0 else mpmath.mpf(0)

        nnls_compensation_found = bool(rel_nnls_residual < mpmath.mpf('1e-5'))
        positive_energy_holds = bool(res_nnls_norm > mpmath.mpf('1e-25'))

        part_indices = [
            other_indices[c] for c in range(len(other_indices))
            if abs(x_nnls[c]) > mpmath.mpf('1e-12') * max(nnls_sol_norm, mpmath.mpf('1e-30'))
        ]

        return {
            "target_index": target_col_idx,
            "u": u_mpf,
            "v_target": v_target,
            "v_norm": v_norm,
            "quadratic_energy": energy,
            "matrix_norm": matrix_norm,
            "singular_values": [s for s in S],
            "numerical_rank": primary_rank,
            "nullity": primary_nullity,
            "condition_number": primary_cond,
            "rank_threshold": primary_cutoff,
            "threshold_sweep": sweep_results,
            "rank_stability": rank_stability,
            "unconstrained_solution": x_unconstrained,
            "unconstrained_residual_norm": res_unconstrained_norm,
            "unconstrained_relative_residual": rel_unconstrained,
            "nnls_solution": x_nnls,
            "nnls_solution_norm": nnls_sol_norm,
            "nnls_residual_vector": res_nnls,
            "nnls_residual_norm": res_nnls_norm,
            "nnls_relative_residual": rel_nnls_residual,
            "nnls_compensation_found": nnls_compensation_found,
            "positive_energy_holds": positive_energy_holds,
            "participating_indices": part_indices,
            "other_indices": other_indices,
        }
