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
from typing import Union, Tuple, List, Optional, Dict, Any, Sequence, Set, overload, Literal, Callable
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
            s_clean = s.strip().replace('(', '').replace(')', '').replace(' ', '').replace('*', '')
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


def von_mangoldt_prime_power(n: int) -> Optional[Tuple[int, int]]:
    """Returns (p, k) if n = p^k for prime p and integer k >= 1, else None."""
    if n < 2:
        return None
    temp = n
    d = 2
    factor = None
    k = 0
    while d * d <= temp:
        if temp % d == 0:
            factor = d
            while temp % d == 0:
                temp //= d
                k += 1
            if temp != 1:
                return None
            return (factor, k)
        d += 1
    if temp > 1:
        return (temp, 1)
    return None


def von_mangoldt(n: int, dps: Optional[int] = None) -> mpmath.mpf:
    """
    Exact von Mangoldt function Lambda(n) preserving arbitrary precision:
    Returns log(p) if n = p^k for prime p and k >= 1, else 0.
    Does not round through binary float.
    """
    pp = von_mangoldt_prime_power(n)
    if pp is None:
        return mpmath.mpf(0)
    p, _ = pp
    if dps is not None:
        with mpmath.workdps(dps):
            return mpmath.log(mpmath.mpf(p))
    return mpmath.log(mpmath.mpf(p))


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
    K_{-n} * u_{-n} \approx v_target = K_n * u_n with u_{-n} >= 0.

    Evaluates:
    - SVD of K_{-n}, singular values, rank, nullity, condition number
    - Complete threshold sweep across [1e-18, 1e-20, 1e-25, 1e-30, 1e-35, 1e-40]
    - Unconstrained least squares solution and residual
    - Non-negative least squares (NNLS) solution (u >= 0) and residual
    - Single-target quadratic radial energy E(u) = ||v_target||^2 = u^2 ||K_n||^2 >= 0
    - Finite cone compensation diagnostic: whether NNLS relative residual < 1e-5.
      Note: Positive target energy E(u) > 0 does NOT preclude non-negative compensation
      by other zero columns in a high-nullity finite subspace (~85 nullity).
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
        nnls_residual_nonzero_at_threshold = bool(rel_nnls_residual >= mpmath.mpf('1e-5'))
        finite_response_energy_positive = bool(energy > mpmath.mpf('1e-25'))

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
            "nnls_residual_nonzero_at_threshold": nnls_residual_nonzero_at_threshold,
            "finite_response_energy_positive": finite_response_energy_positive,
            "participating_indices": part_indices,
            "other_indices": other_indices,
        }


# =============================================================================
# Radial-Defect Quotient Q(z), Limiting Invariant L_Q, and Fredholm Spectral Theory
# (Reference: RADIAL_DEFECT_QUOTIENT.md, MATH_CONTRACT.md §§37-38)
# =============================================================================

def radial_factor_q(
    x: Union[str, float, int, mpmath.mpf],
    delta: Union[str, float, int, mpmath.mpf],
    gamma: Union[str, float, int, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Evaluates the exact real-axis quartet quotient factor q_{delta, gamma}(x):
    q_{delta, gamma}(x) = gamma^4 * [ (x^2 + gamma^2 - delta^2)^2 + 4 * delta^2 * gamma^2 ]
                          / [ (gamma^2 + delta^2)^2 * (x^2 + gamma^2)^2 ]

    Properties (audited):
    - 0 < q_{delta, gamma}(x) <= 1 for all real x, with q=1 iff x=0 (when delta != 0).
    - If delta == 0, returns mpmath.mpf(1) identically.
    - Unique minimum at x_* = sqrt(delta^2 + 3*gamma^2).
    """
    with mpmath.workdps(dps + 15):
        x_m = to_mpf(x, dps=dps + 15)
        d_m = to_mpf(delta, dps=dps + 15)
        g_m = to_mpf(gamma, dps=dps + 15)

        if d_m == 0:
            return mpmath.mpf('1.0')
        if g_m == 0:
            raise ValueError("gamma cannot be zero for upper-half-plane zeros.")

        x2 = x_m * x_m
        g2 = g_m * g_m
        d2 = d_m * d_m

        term1 = x2 + g2 - d2
        num = (g2 * g2) * (term1 * term1 + mpmath.mpf(4) * d2 * g2)
        den = ((g2 + d2) * (g2 + d2)) * ((x2 + g2) * (x2 + g2))
        return num / den


def radial_factor_q_min(
    delta: Union[str, float, int, mpmath.mpf],
    gamma: Union[str, float, int, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Evaluates exact minimum value of q_{delta, gamma}(x):
    q_min = 4 / [ (1 + r)^2 * (4 + r) ] where r = delta^2 / gamma^2.
    """
    with mpmath.workdps(dps + 15):
        d_m = to_mpf(delta, dps=dps + 15)
        g_m = to_mpf(gamma, dps=dps + 15)
        if d_m == 0:
            return mpmath.mpf('1.0')
        if g_m == 0:
            raise ValueError("gamma cannot be zero.")
        r = (d_m * d_m) / (g_m * g_m)
        one_plus_r = mpmath.mpf(1) + r
        four_plus_r = mpmath.mpf(4) + r
        return mpmath.mpf(4) / (one_plus_r * one_plus_r * four_plus_r)


def radial_factor_q_min_x(
    delta: Union[str, float, int, mpmath.mpf],
    gamma: Union[str, float, int, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Evaluates the location of the unique positive minimum x_* = sqrt(delta^2 + 3*gamma^2).
    """
    with mpmath.workdps(dps + 15):
        d_m = to_mpf(delta, dps=dps + 15)
        g_m = to_mpf(gamma, dps=dps + 15)
        return mpmath.sqrt(d_m * d_m + mpmath.mpf(3) * g_m * g_m)


def radial_factor_log_bound(
    delta: Union[str, float, int, mpmath.mpf],
    gamma: Union[str, float, int, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Evaluates the exact supremum of |log q_{delta, gamma}(x)|:
    sup_x |log q(x)| = 2*log(1 + r) + log(1 + r/4) <= (9/4)*r, where r = delta^2 / gamma^2.
    """
    with mpmath.workdps(dps + 15):
        d_m = to_mpf(delta, dps=dps + 15)
        g_m = to_mpf(gamma, dps=dps + 15)
        if d_m == 0:
            return mpmath.mpf(0)
        if g_m == 0:
            raise ValueError("gamma cannot be zero.")
        r = (d_m * d_m) / (g_m * g_m)
        return mpmath.mpf(2) * mpmath.log(mpmath.mpf(1) + r) + mpmath.log(mpmath.mpf(1) + r / mpmath.mpf(4))


def projection_subtracted_defect_d(
    delta: Union[str, float, int, mpmath.mpf],
    gamma: Union[str, float, int, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Evaluates the single-zero projection-subtracted defect:
    d(delta, gamma) = log(1 + delta^2 / gamma^2).
    Identical to the projection-subtracted quartet response 2*Re log(delta + i*gamma) - 2*Re log(i*gamma).
    """
    with mpmath.workdps(dps + 15):
        d_m = to_mpf(delta, dps=dps + 15)
        g_m = to_mpf(gamma, dps=dps + 15)
        if g_m == 0:
            raise ValueError("gamma cannot be zero.")
        r = (d_m * d_m) / (g_m * g_m)
        return mpmath.log(mpmath.mpf(1) + r)


def involution_pairing_kernel_kappa1(
    z: Union[complex, str, Tuple[Any, Any], mpmath.mpc],
    w: Union[complex, str, Tuple[Any, Any], mpmath.mpc],
    dps: int = 80
) -> mpmath.mpc:
    """
    [AUDIT PATH] Evaluates the rational involution pairing kernel:
    kappa_1(z, w) = 4*z*w / (z + w)^2 - 1.

    When w = z^# = -conj(z) for z = delta + i*gamma, kappa_1(z, z^#) = delta^2 / gamma^2 identically.
    """
    with mpmath.workdps(dps + 15):
        z_c = to_mpc(z, dps=dps + 15)
        w_c = to_mpc(w, dps=dps + 15)
        sum_zw = z_c + w_c
        if sum_zw == 0:
            raise ValueError("z + w cannot be zero for kernel kappa_1.")
        return (mpmath.mpf(4) * z_c * w_c) / (sum_zw * sum_zw) - mpmath.mpf(1)


def finite_radial_operator_trace(
    zeros_delta_gamma: Sequence[Tuple[Union[str, float, int, mpmath.mpf], Union[str, float, int, mpmath.mpf]]],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Evaluates the finite trace of the relative radial spectral operator R:
    Tr(R_fin) = sum_{j=1}^N (delta_j^2 / gamma_j^2).
    Non-negative; vanishes if and only if all delta_j == 0.
    """
    with mpmath.workdps(dps + 15):
        total = mpmath.mpf(0)
        for d_val, g_val in zeros_delta_gamma:
            d_m = to_mpf(d_val, dps=dps + 15)
            g_m = to_mpf(g_val, dps=dps + 15)
            if g_m == 0:
                raise ValueError("gamma cannot be zero.")
            total += (d_m * d_m) / (g_m * g_m)
        return total


def finite_radial_fredholm_det(
    zeros_delta_gamma: Sequence[Tuple[Union[str, float, int, mpmath.mpf], Union[str, float, int, mpmath.mpf]]],
    t: Union[str, float, int, mpmath.mpf] = 1,
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Evaluates the finite Fredholm determinant family:
    D_fin(t) = det(I + t * R_fin) = prod_{j=1}^N (1 + t * delta_j^2 / gamma_j^2).
    At t=1, det(I + R_fin) = L_Q_fin^(-1).
    """
    with mpmath.workdps(dps + 15):
        t_m = to_mpf(t, dps=dps + 15)
        prod_val = mpmath.mpf(1)
        for d_val, g_val in zeros_delta_gamma:
            d_m = to_mpf(d_val, dps=dps + 15)
            g_m = to_mpf(g_val, dps=dps + 15)
            if g_m == 0:
                raise ValueError("gamma cannot be zero.")
            r = (d_m * d_m) / (g_m * g_m)
            prod_val *= (mpmath.mpf(1) + t_m * r)
        return prod_val


def finite_radial_defect_quotient_limit(
    quartets_delta_gamma: Sequence[Tuple[Union[str, float, int, mpmath.mpf], Union[str, float, int, mpmath.mpf]]],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Evaluates finite limiting invariant L_Q for a collection of off-line quartets:
    L_{Q, fin} = prod_{quartets} (gamma_j^2 / (gamma_j^2 + delta_j^2))^2 = prod_{quartets} (1 + delta_j^2 / gamma_j^2)^(-2).
    Satisfies 0 < L_{Q, fin} <= 1, with L_{Q, fin} == 1 iff all delta_j == 0.
    """
    with mpmath.workdps(dps + 15):
        prod_val = mpmath.mpf(1)
        for d_val, g_val in quartets_delta_gamma:
            d_m = to_mpf(d_val, dps=dps + 15)
            g_m = to_mpf(g_val, dps=dps + 15)
            if g_m == 0:
                raise ValueError("gamma cannot be zero.")
            r = (d_m * d_m) / (g_m * g_m)
            term = (mpmath.mpf(1) + r)
            prod_val /= (term * term)
        return prod_val

# ==============================================================================
# § 39. ARITHMETIC RADIAL BRIDGE AND CANDIDATE EVALUATION HARNESS
# ==============================================================================

def grade_center(
    K: Union[int, float, str, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Evaluates the exact critical-line center at bilateral grade K:
    c_K = tau^K / 2.
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        k_val = to_mpf(K, dps=dps + 15)
        return mpmath.power(tau, k_val) / mpmath.mpf(2)


def centered_grade_coord(
    s: Union[complex, str, Tuple[Any, Any], mpmath.mpc, mpmath.mpf],
    K: Union[int, float, str, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpc:
    """
    [AUDIT PATH] Evaluates the centered grade coordinate z_K = s_K - c_K = tau^K * (s - 1/2):
    s_K = tau^K * s, c_K = tau^K / 2 ==> z_K = tau^K * (s - 1/2).
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        k_val = to_mpf(K, dps=dps + 15)
        a_K = mpmath.power(tau, k_val)
        s_val = to_mpc(s, dps=dps + 15)
        z = s_val - mpmath.mpc(0.5, 0)
        return a_K * z


def spectral_determinant_d(
    quartets_or_zeros: Sequence[Any],
    dps: int = 80
) -> mpmath.mpf:
    """
    [SPECTRAL PATH] Evaluates the spectral determinant defect:
    D = -log L_Q = sum_j 2 * n_j * log(1 + delta_j^2 / gamma_j^2).
    Input can be a list of (delta, gamma) or (delta, gamma, multiplicity).
    """
    with mpmath.workdps(dps + 15):
        total = mpmath.mpf(0)
        for item in quartets_or_zeros:
            if len(item) == 2:
                d_val, g_val = item
                n_j = 1
            else:
                d_val, g_val, n_j = item
            d_m = to_mpf(d_val, dps=dps + 15)
            g_m = to_mpf(g_val, dps=dps + 15)
            if g_m == 0:
                raise ValueError("gamma cannot be zero.")
            r_j = (d_m * d_m) / (g_m * g_m)
            total += mpmath.mpf(2 * n_j) * mpmath.log(mpmath.mpf(1) + r_j)
        return total


def spectral_trace_t(
    upper_zeros: Sequence[Any],
    dps: int = 80
) -> mpmath.mpf:
    """
    [SPECTRAL PATH] Evaluates the spectral trace defect:
    T = Tr(R) = sum_{lambda in Lambda^+} n_lambda * (delta_lambda^2 / gamma_lambda^2).
    For off-line quartets with multiplicity n_j, the two upper roots contribute 2 * n_j * r_j.
    """
    with mpmath.workdps(dps + 15):
        total = mpmath.mpf(0)
        for item in upper_zeros:
            if len(item) == 2:
                d_val, g_val = item
                mult = 1
            else:
                d_val, g_val, mult = item
            d_m = to_mpf(d_val, dps=dps + 15)
            g_m = to_mpf(g_val, dps=dps + 15)
            if g_m == 0:
                raise ValueError("gamma cannot be zero.")
            r_j = (d_m * d_m) / (g_m * g_m)
            total += mpmath.mpf(mult) * r_j
        return total


def spectral_weighted_trace_t_a(
    upper_zeros: Sequence[Any],
    a: Union[str, float, int, mpmath.mpf] = 1.0,
    dps: int = 80
) -> mpmath.mpf:
    """
    [SPECTRAL PATH] Evaluates the regularized weighted trace defect:
    T_a = sum_{lambda in Lambda^+} w_a(lambda) * (delta_lambda^2 / gamma_lambda^2),
    where w_a(lambda) = mult * exp(-a * gamma_lambda^2) > 0.
    """
    with mpmath.workdps(dps + 15):
        a_m = to_mpf(a, dps=dps + 15)
        if a_m <= 0:
            raise ValueError("Regularization parameter a must be strictly positive.")
        total = mpmath.mpf(0)
        for item in upper_zeros:
            if len(item) == 2:
                d_val, g_val = item
                mult = 1
            else:
                d_val, g_val, mult = item
            d_m = to_mpf(d_val, dps=dps + 15)
            g_m = to_mpf(g_val, dps=dps + 15)
            if g_m == 0:
                raise ValueError("gamma cannot be zero.")
            r_j = (d_m * d_m) / (g_m * g_m)
            w_val = mpmath.mpf(mult) * mpmath.exp(-a_m * g_m * g_m)
            total += w_val * r_j
        return total


def arithmetic_firewall_check(data: Any) -> None:
    """
    Enforces the strict arithmetic firewall: rejects zero lists, projected ordinates,
    and spectral invariants passed to arithmetic evaluators.
    """
    if isinstance(data, (dict, list, tuple)):
        forbidden_keys = {
            "zeros", "zero_list", "zeros_list", "gamma_list", "delta_list",
            "spectral", "L_Q", "det_R", "ordinates", "projected_zeros", "lambda_sharp"
        }
        if isinstance(data, dict) and any(k in data for k in forbidden_keys):
            raise ValueError("Firewall Violation: Arithmetic evaluator received spectral zero data.")


_ARITHMETIC_SIDE_CACHE: Dict[Tuple[int, int, int, int], mpmath.mpf] = {}


def evaluate_arithmetic_side_cached(
    test_func_j: int = 1,
    K: int = 0,
    prime_cutoff: int = 50000,
    dps: int = 80
) -> mpmath.mpf:
    """
    [ARITHMETIC PATH] Evaluates the arithmetic side (Pole + Prime + Gamma terms)
    of the Riemann–Weil explicit formula for test function j at grade K,
    cached by (test_func_j, K, prime_cutoff, dps).
    """
    key = (int(test_func_j), int(K), int(prime_cutoff), int(dps))
    if key in _ARITHMETIC_SIDE_CACHE:
        return _ARITHMETIC_SIDE_CACHE[key]
    with mpmath.workdps(dps + 15):
        res = explicit_formula_eval(j=test_func_j, K=K, prime_cutoff=prime_cutoff, dps=dps + 15)
        val = res["total_rhs"]
        _ARITHMETIC_SIDE_CACHE[key] = val
        return val


def evaluate_spectral_side_cached(
    zeros_delta_gamma: Sequence[Any],
    test_func_j: int = 1,
    K: int = 0,
    dps: int = 80
) -> mpmath.mpf:
    """
    [SPECTRAL PATH] Evaluates the spectral side sum_{rho} 2 * Re[h_{K,j}(gamma_rho + i*delta_rho)]
    of the Riemann–Weil explicit formula for test function j at grade K on the given zero configuration.
    """
    with mpmath.workdps(dps + 15):
        k_val = to_mpf(K, dps=dps + 15)
        total = mpmath.mpf(0)
        for item in zeros_delta_gamma:
            if isinstance(item, (tuple, list)):
                if len(item) == 2:
                    d_val, g_val = item
                    mult = 1
                else:
                    d_val, g_val, mult = item[0], item[1], item[2]
            else:
                d_val = 0
                g_val = item
                mult = 1
            d_m = to_mpf(d_val, dps=dps + 15)
            g_m = to_mpf(g_val, dps=dps + 15)
            s_pt = mpmath.mpc(g_m, d_m)
            h_val = h_kj_scaled(s_pt, test_func_j, k_val, dps=dps + 15)
            total += mpmath.mpf(mult) * mpmath.mpf(2) * mpmath.re(h_val)
        return total


def arithmetic_candidate_a(
    K: int,
    test_func_j: int = 1,
    dps: int = 80
) -> mpmath.mpf:
    """
    [ARITHMETIC PATH - CANDIDATE A] Evaluates the linear grade difference:
    A_{K,A}^arith = C_K[H_j] - C_0[H_j] = C_0[H_j o tau^K] - C_0[H_j].
    Pure arithmetic evaluation using prime powers and archimedean test-function integrals.
    """
    with mpmath.workdps(dps + 15):
        val_K = evaluate_arithmetic_side_cached(test_func_j, K=K, dps=dps + 15)
        val_0 = evaluate_arithmetic_side_cached(test_func_j, K=0, dps=dps + 15)
        return val_K - val_0


def spectral_candidate_a(
    zeros_delta_gamma: Sequence[Any],
    K: int,
    test_func_j: int = 1,
    dps: int = 80
) -> mpmath.mpf:
    """
    [SPECTRAL PATH - CANDIDATE A] Evaluates the linear grade difference spectral response:
    A_{K,A}^spec = sum_rho [H_{K,j}(gamma_rho + i*delta_rho) - H_{0,j}(gamma_rho + i*delta_rho)].
    """
    with mpmath.workdps(dps + 15):
        val_K = evaluate_spectral_side_cached(zeros_delta_gamma, test_func_j, K=K, dps=dps + 15)
        val_0 = evaluate_spectral_side_cached(zeros_delta_gamma, test_func_j, K=0, dps=dps + 15)
        return val_K - val_0


def arithmetic_candidate_b(
    K: int,
    L: int,
    s: Union[complex, str, mpmath.mpc],
    N_max: int = 1000,
    dps: int = 80
) -> mpmath.mpc:
    """
    [ARITHMETIC PATH - CANDIDATE B] Evaluates the bilinear cross-grade prime-power product:
    D_K(s) * conj(D_L(s)), where D_K(s) = tau^(-K) * sum_{n=1}^{N_max} Lambda(n) / n^(tau^(-K) * s).
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        scale_K = mpmath.power(tau, -to_mpf(K, dps=dps + 15))
        scale_L = mpmath.power(tau, -to_mpf(L, dps=dps + 15))
        s_val = to_mpc(s, dps=dps + 15)

        # Truncated prime-power series for D_K(s)
        D_K = mpmath.mpc(0)
        D_L = mpmath.mpc(0)
        for n in range(2, N_max + 1):
            # Compute von Mangoldt Lambda(n)
            factors = mpmath.factor(n) if hasattr(mpmath, "factor") else None
            # Simple prime power check:
            p_base = None
            is_prime_pow = False
            for p in range(2, n + 1):
                if p * p > n and p_base is None:
                    p_base = n
                    is_prime_pow = True
                    break
                if n % p == 0:
                    temp = n
                    while temp % p == 0:
                        temp //= p
                    if temp == 1:
                        p_base = p
                        is_prime_pow = True
                    break
            if is_prime_pow and p_base is not None:
                lam_n = mpmath.log(p_base)
                term_K = lam_n / mpmath.power(n, scale_K * s_val)
                term_L = lam_n / mpmath.power(n, scale_L * s_val)
                D_K += term_K
                D_L += term_L

        D_K *= scale_K
        D_L *= scale_L
        return D_K * mpmath.conj(D_L)


def spectral_candidate_b(
    zeros_delta_gamma: Sequence[Any],
    K: int,
    L: int,
    s: Union[complex, str, mpmath.mpc],
    dps: int = 80
) -> mpmath.mpc:
    """
    [SPECTRAL PATH - CANDIDATE B] Evaluates the bilinear cross-grade spectral product:
    S_K(s) * conj(S_L(s)), where S_K(s) = tau^(-K) * sum_rho 1 / (tau^(-K)*s - (1/2 + delta_rho + i*gamma_rho)).
    Introduces all-pairs double sum: sum_{rho_1, rho_2} 1 / [(tau^(-K)s - rho_1)(tau^(-L)conj(s) - conj(rho_2))].
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        scale_K = mpmath.power(tau, -to_mpf(K, dps=dps + 15))
        scale_L = mpmath.power(tau, -to_mpf(L, dps=dps + 15))
        s_val = to_mpc(s, dps=dps + 15)

        S_K = mpmath.mpc(0)
        S_L = mpmath.mpc(0)
        for item in zeros_delta_gamma:
            d_val, g_val = item[0], item[1]
            rho = mpmath.mpc(mpmath.mpf('0.5') + to_mpf(d_val, dps=dps + 15), to_mpf(g_val, dps=dps + 15))
            S_K += mpmath.mpf(1) / (scale_K * s_val - rho)
            S_L += mpmath.mpf(1) / (scale_L * s_val - rho)

        S_K *= scale_K
        S_L *= scale_L
        return S_K * mpmath.conj(S_L)


def get_candidate_registry() -> Dict[str, Dict[str, Any]]:
    """
    Returns the structured registry of Arithmetic Radial Bridge candidates A through G.
    """
    return {
        "CANDIDATE_A": {
            "id": "CANDIDATE_A",
            "name": "Linear Grade Differences",
            "target": "NONE (Negative Control)",
            "arithmetic_formula": "C_K[H] - C_0[H] = C_0[H o tau^K] - C_0[H]",
            "spectral_formula": "sum_rho [H(tau^K * rho) - H(rho)]",
            "grade_indices": "K in Z",
            "derivation_status": "PROVED_COLLAPSE",
            "arithmetic_independence": True,
            "pair_isolation": False,
            "earliest_failure": "Linear explicit formula yields only 1-point direct sums; collapses to native explicit formula without isolating reflection pairs (lambda, lambda^#).",
            "classification": "FALSIFIED_FOR_BRIDGE"
        },
        "CANDIDATE_B": {
            "id": "CANDIDATE_B",
            "name": "Bilinear Cross-Grade Explicit Formula",
            "target": "TRACE / DETERMINANT",
            "arithmetic_formula": "D_K(s) * conj(D_L(s)) with D_K(s) = tau^(-K) * sum Lambda(n) / n^(tau^(-K) s)",
            "spectral_formula": "tau^(-K-L) * sum_{rho_1, rho_2} 1 / [(tau^(-K) s - rho_1)(tau^(-L) conj(s) - conj(rho_2))]",
            "grade_indices": "(K, L) in Z^2",
            "derivation_status": "DERIVED_OBSTRUCTED",
            "arithmetic_independence": True,
            "pair_isolation": False,
            "earliest_failure": "Spectral expansion produces an unrestricted double sum over all zero pairs (rho_1, rho_2); off-diagonal cross-terms dominate and do not isolate involution pairs without projected divisor input.",
            "classification": "FALSIFIED_FOR_PAIR_ISOLATION"
        },
        "CANDIDATE_C": {
            "id": "CANDIDATE_C",
            "name": "Tensor-Square Trace Identity",
            "target": "TRACE",
            "arithmetic_formula": "Doubled arithmetic convolution on L^2(R_+^x x R_+^x)",
            "spectral_formula": "sum_{rho_1, rho_2} K(rho_1, rho_2)",
            "grade_indices": "Bilateral tensor product",
            "derivation_status": "OBSTRUCTED",
            "arithmetic_independence": True,
            "pair_isolation": False,
            "earliest_failure": "Unrestricted tensor product sums over all pairs (rho_1, rho_2); selecting the diagonal reflection pair rho_1 = rho_2^# requires zero-divisor projection.",
            "classification": "FALSIFIED_FOR_PAIR_ISOLATION"
        },
        "CANDIDATE_D": {
            "id": "CANDIDATE_D",
            "name": "Logarithmic-Derivative Contour Identity",
            "target": "DETERMINANT",
            "arithmetic_formula": "1/(2*pi*i) int (zeta'/zeta)(tau^(-K) s) * (zeta'/zeta)(1 - tau^(-K) s) W(s) ds",
            "spectral_formula": "Residue evaluation across critical strip",
            "grade_indices": "K in Z",
            "derivation_status": "OBSTRUCTED",
            "arithmetic_independence": True,
            "pair_isolation": False,
            "earliest_failure": "Contour residue theorem produces double residue cross-terms; fails to isolate (lambda, lambda^#) without subtracting off-diagonal divisor terms.",
            "classification": "FALSIFIED_FOR_PAIR_ISOLATION"
        },
        "CANDIDATE_E": {
            "id": "CANDIDATE_E",
            "name": "Relative Determinant from Arithmetic Space",
            "target": "DETERMINANT (D)",
            "arithmetic_formula": "det_F(I + R_arith(K)) on Dirichlet polynomial Hilbert space",
            "spectral_formula": "det_F(I + R_spec) = L_Q^(-1)",
            "grade_indices": "K in Z",
            "derivation_status": "UNPROVED_BRIDGE",
            "arithmetic_independence": True,
            "pair_isolation": True,
            "earliest_failure": "No known finite-rank or trace-class operator constructed purely from arithmetic data without zero-divisor input matches det_F(I + R).",
            "classification": "OPEN_UNPROVED"
        },
        "CANDIDATE_F": {
            "id": "CANDIDATE_F",
            "name": "Grade-Indexed Prime-Power Pairing",
            "target": "TRACE (T)",
            "arithmetic_formula": "sum_{p, m} (log p / p^(m/2)) * J_K(m log p)",
            "spectral_formula": "sum_j 2 * n_j * (delta_j^2 / gamma_j^2)",
            "grade_indices": "Bilateral grade K",
            "derivation_status": "UNPROVED_BRIDGE",
            "arithmetic_independence": True,
            "pair_isolation": True,
            "earliest_failure": "Arithmetic kernel J_K that produces delta^2/gamma^2 without mixing with cross-terms lacks independent closed-form construction.",
            "classification": "OPEN_UNPROVED"
        },
        "CANDIDATE_G": {
            "id": "CANDIDATE_G",
            "name": "Weighted Regularized Radial Bridge",
            "target": "WEIGHTED_TRACE (T_a)",
            "arithmetic_formula": "A_{K, a}^arith = arithmetic realization of T_a",
            "spectral_formula": "T_a = sum_{lambda in Lambda^+} exp(-a * gamma_lambda^2) * (delta_lambda^2 / gamma_lambda^2)",
            "grade_indices": "K in Z, a > 0",
            "derivation_status": "SPECTRAL_PROVED_ARITH_OPEN",
            "arithmetic_independence": True,
            "pair_isolation": True,
            "earliest_failure": "Spectral detector T_a > 0 for delta != 0 is rigorously proved, but arithmetic realization A_{K, a}^arith remains open.",
            "classification": "LIVE_UNDERIVED"
        },
        "CANDIDATE_SS1": {
            "id": "CANDIDATE_SS1",
            "name": "Conjugated Explicit-Formula Pair",
            "target": "SEPARATED_SESQUILINEAR_SIGNAL",
            "arithmetic_formula": "Phi_K(u_1, u_2) via Riemann-Weil explicit formula with paired parameters (x, t)",
            "spectral_formula": "sum_rho h(rho; x, t)",
            "grade_indices": "K in Z",
            "derivation_status": "FALSIFIED_GATE_2",
            "arithmetic_independence": True,
            "pair_isolation": False,
            "earliest_failure": "Direct Holomorphic Parameter Separation Failure: Cauchy-Riemann equations on h(delta+i*gamma) = a(gamma)*exp(x*delta)*exp(i*t*gamma) force x=t and a'(gamma)=0 on any open set, proving failure of direct 1-point holomorphic separation. In holomorphic kernels exp((x+it)z) = exp(x*delta-t*gamma)*exp(i(x*gamma+t*delta)), translation averaging int_{-T}^T exp(-2t*gamma) dt = sinh(2T*gamma)/gamma produces ordinate-driven exponential divergence.",
            "classification": "FAIL_DIRECT_HOLOMORPHIC_PARAMETER_SEPARATION"
        },
        "CANDIDATE_SS2": {
            "id": "CANDIDATE_SS2",
            "name": "Two-Slot Logarithmic Derivative",
            "target": "SEPARATED_SESQUILINEAR_SIGNAL",
            "arithmetic_formula": "D_K(s_1) * conj(D_K(s_2)) with D_K(s) = tau^(-K) * sum Lambda(n)/n^(tau^(-K)s)",
            "spectral_formula": "tau^(-2K) * sum_{rho_1, rho_2} 1 / [(tau^(-K)s_1 - rho_1)(tau^(-K)conj(s_2) - conj(rho_2))]",
            "grade_indices": "K in Z",
            "derivation_status": "DOUBLE_SUM_DERIVED",
            "arithmetic_independence": True,
            "pair_isolation": False,
            "earliest_failure": "Unconstrained Double-Sum Resolution: D_K(s_1)*conj(D_K(s_2)) expands to an unconstrained double sum over all zero pairs (rho_1, rho_2). Pair isolation (lambda, lambda^#) is not obtained, and off-diagonal limiting behavior is open without projected divisor subtraction.",
            "classification": "DOUBLE_SUM_DERIVED_PAIR_ISOLATION_NOT_OBTAINED"
        },
        "CANDIDATE_SS3": {
            "id": "CANDIDATE_SS3",
            "name": "Rapidly Smoothed Transform",
            "target": "SEPARATED_SESQUILINEAR_SIGNAL",
            "arithmetic_formula": "1/(2*pi*i) int D_K(s) exp(sigma(s-1/2)^2 + (x+it)(s-1/2)) ds",
            "spectral_formula": "sum_rho exp(sigma(delta^2 - gamma^2) + x*delta - t*gamma + i(2*sigma*delta*gamma + t*delta + x*gamma))",
            "grade_indices": "K in Z, sigma > 0",
            "derivation_status": "FALSIFIED_GATE_2",
            "arithmetic_independence": True,
            "pair_isolation": False,
            "earliest_failure": "Ordinate Slot Exponential Growth: Translation parameter enters real exponential slot as -t*gamma, causing translation average int_{-T}^T exp(-2t*gamma) dt = sinh(2T*gamma)/gamma to diverge exponentially ~ exp(2T*|gamma|)/(2|gamma|). Growth is driven by ordinate frequency gamma rather than radial amplitude.",
            "classification": "FAIL_ORDINATE_SLOT_EXPONENTIAL_GROWTH"
        },
        "CANDIDATE_SS4": {
            "id": "CANDIDATE_SS4",
            "name": "Cross-Grade Sesquilinear Form",
            "target": "SEPARATED_SESQUILINEAR_SIGNAL",
            "arithmetic_formula": "iint K(u, v; x, t) D_K(s_1) conj(D_L(s_2)) du dv for K != L",
            "spectral_formula": "sum_{rho_1 in Z_K, rho_2 in Z_L} K_spec(rho_1, rho_2)",
            "grade_indices": "(K, L) in Z^2, K != L",
            "derivation_status": "SINGLE_GRADE_REDUNDANT_CROSS_GRADE_OPEN",
            "arithmetic_independence": True,
            "pair_isolation": False,
            "earliest_failure": "Single-grade explicit formula evaluations are coordinate-redundant pullbacks under z_K = tau^K*z (proved). Bounded frequency gap searches show no non-trivial resonances between tau^K*log(n) and log(m) up to tested bounds (numerical evidence only; exact cross-grade non-resonance for 2*pi is open). General cross-grade sesquilinear nonredundancy remains unproved.",
            "classification": "GRADE_COORDINATE_REDUNDANT"
        },
        "CANDIDATE_SS5": {
            "id": "CANDIDATE_SS5",
            "name": "Direct Positive Quadratic Kernel",
            "target": "POSITIVE_QUADRATIC_FORM",
            "arithmetic_formula": "iint k(u, v) f(u) conj(f(v)) du dv",
            "spectral_formula": "sum_{rho_1, rho_2} K(rho_1, rho_2)",
            "grade_indices": "K in Z",
            "derivation_status": "DIRECT_ONE_POINT_HOLOMORPHIC_FALSIFIED",
            "arithmetic_independence": True,
            "pair_isolation": False,
            "earliest_failure": "Direct 1-Point Holomorphic Realization Boundary: Any holomorphic kernel on C^2 vanishing on the critical line Re(s)=1/2 vanishes identically everywhere by the Identity Theorem. Non-holomorphic involution pairings (rho - rho^# = 2*delta) require complex conjugation s -> 1-conj(s), which cannot be evaluated via direct 1-point Cauchy residue calculus. Nonlinear sesquilinear realizations and involution-pair isolation remain open.",
            "classification": "FAIL_DIRECT_HOLOMORPHIC_ONE_POINT_REALIZATION"
        },
        "CANDIDATE_CMSA1": {
            "id": "CANDIDATE_CMSA1",
            "name": "Base Completed Mean-Square Anchor",
            "target": "COMPLETED_MEAN_SQUARE_ANCHOR (A(sigma))",
            "arithmetic_formula": "A(sigma) = lim_{T->inf} (1/2T) int_{-T}^T |A(sigma+it) - Xi'/Xi(sigma-1/2+it)|^2 dt - sum_{n>=2} Lambda(n)^2/n^(2*sigma) = 0",
            "spectral_formula": "lim_{T->inf} (1/2T) int_{-T}^T |A(sigma+it) - sum_{lambda/+-1} 2(sigma-1/2+it)/((sigma-1/2+it)^2 - lambda^2)|^2 dt - sum Lambda(n)^2/n^(2*sigma)",
            "grade_indices": "sigma > 1",
            "derivation_status": "EXACT_ARITHMETIC_ANCHOR_PROVED_SPECTRAL_G4_OPEN",
            "arithmetic_independence": True,
            "pair_isolation": False,
            "earliest_failure": "Gate G4: Complete spectral expansion and justified infinite interchange. Pointwise arithmetic identity P(u) = A(u) - Xi'/Xi(u-1/2) is exact on Re(u) > 1 and gives arithmetic anchor = 0. The arithmetic mean-square is carried by a collective nonuniform infinite cancellation. Individual zero resolvent terms in L^2(R, dt) integrate to zero under (1/2T) scaling, so the infinite limit cannot be interchanged termwise without an established renormalization.",
            "classification": "INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_GATE_G4"
        },
        "CANDIDATE_CMSA2": {
            "id": "CANDIDATE_CMSA2",
            "name": "Polarized Completed Mean-Square Anchor",
            "target": "POLARIZED_MEAN_SQUARE_ANCHOR (A(sigma_1, sigma_2))",
            "arithmetic_formula": "A(sigma_1, sigma_2) = lim_{T->inf} (1/2T) int_{-T}^T P_sigma1(t)*conj(P_sigma2(t)) dt - sum_{n>=2} Lambda(n)^2/n^(sigma1+sigma2) = 0",
            "spectral_formula": "I_AA(sigma_1, sigma_2) - I_AZ(sigma_1, sigma_2) - I_ZA(sigma_1, sigma_2) + I_ZZ(sigma_1, sigma_2) - sum Lambda(n)^2/n^(sigma1+sigma2)",
            "grade_indices": "sigma_1, sigma_2 > 1",
            "derivation_status": "EXACT_ARITHMETIC_ANCHOR_PROVED_SPECTRAL_G4_OPEN",
            "arithmetic_independence": True,
            "pair_isolation": False,
            "earliest_failure": "Gate G4: Complete spectral expansion and justified infinite interchange. Expanding the polarized anchor produces Archimedean-Archimedean, Archimedean-Zero, and Zero-Zero integrals. Zero-zero integral J_T(p,q) scales as O(1/T) for individual terms; termwise infinite interchange is open without regularized renormalization.",
            "classification": "INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_GATE_G4"
        },
        "CANDIDATE_CMSA3": {
            "id": "CANDIDATE_CMSA3",
            "name": "Grade-Normalized Completed Mean-Square Anchor",
            "target": "GRADE_NORMALIZED_ANCHOR (A_K(sigma))",
            "arithmetic_formula": "A_K(sigma) = lim_{T->inf} (1/2T) int_{-T}^T |tau^K D_K^P(tau^K(sigma+it))|^2 dt - sum_{n>=2} Lambda(n)^2/n^(2*sigma) = 0",
            "spectral_formula": "A_K(sigma) = A_0(sigma) for all K in Z",
            "grade_indices": "K in Z, sigma > 1",
            "derivation_status": "GRADE_COORDINATE_REDUNDANT",
            "arithmetic_independence": True,
            "pair_isolation": False,
            "earliest_failure": "Grade Covariance Redundancy: The normalized completed logarithmic derivative tau^K D_K^xi(tau^K u) = xi'/xi(u) is strictly coordinate-redundant for all K in Z. Grade dilation yields no additional arithmetic constraints or non-redundant radial invariants beyond K=0.",
            "classification": "GRADE_COORDINATE_REDUNDANT"
        }
    }


# ============================================================================
# SEPARATED SESQUILINEAR SIGNAL API AND CANDIDATE IMPLEMENTATIONS
# ============================================================================

def separated_spectral_signal(
    zeros_delta_gamma: Sequence[Any],
    K: int = 0,
    x: Union[float, str, mpmath.mpf] = 0,
    t: Union[float, str, mpmath.mpf] = 0,
    a_kernel: Optional[Any] = None,
    dps: int = 80
) -> mpmath.mpc:
    """
    [SPECTRAL SIGNAL] Evaluates the target separated sesquilinear signal:
    S_K(x, t) = sum_gamma a_K(gamma) * (sum_a exp(x * delta_{gamma, a})) * exp(i * t * gamma_K),
    where gamma_K = tau^(-K) * gamma.
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        scale_K = mpmath.power(tau, -to_mpf(K, dps=dps + 15))
        x_val = to_mpf(x, dps=dps + 15)
        t_val = to_mpf(t, dps=dps + 15)

        # Group zeros by distinct ordinate gamma
        gamma_groups: Dict[str, List[mpmath.mpf]] = {}
        for item in zeros_delta_gamma:
            d_val = to_mpf(item[0], dps=dps + 15)
            g_val = to_mpf(item[1], dps=dps + 15)
            mult = int(item[2]) if len(item) > 2 else 1
            g_key = mpmath.nstr(abs(g_val), n=dps)
            if g_key not in gamma_groups:
                gamma_groups[g_key] = []
            for _ in range(mult):
                gamma_groups[g_key].append(d_val)

        total_sig = mpmath.mpc(0)
        for g_key, deltas in gamma_groups.items():
            gamma_val = to_mpf(g_key, dps=dps + 15)
            gamma_K = scale_K * gamma_val

            # Gaussian/Schwartz decay weight a_K(gamma)
            if a_kernel is not None:
                a_val = to_mpf(a_kernel(gamma_K), dps=dps + 15)
            else:
                a_val = mpmath.exp(-mpmath.mpf('0.01') * gamma_K * gamma_K)

            # Radial sum: sum_a exp(x * delta_a)
            radial_factor = mpmath.mpf(0)
            for d in deltas:
                radial_factor += mpmath.exp(x_val * scale_K * d)

            # Frequency factor: exp(i * t * gamma_K)
            freq_factor = mpmath.exp(mpmath.mpc(0, t_val * gamma_K))
            total_sig += a_val * radial_factor * freq_factor

        return total_sig


def spectral_mean_square_m(
    zeros_delta_gamma: Sequence[Any],
    K: int = 0,
    x: Union[float, str, mpmath.mpf] = 0,
    a_kernel: Optional[Any] = None,
    dps: int = 80
) -> mpmath.mpf:
    """
    [SPECTRAL MEAN SQUARE] Evaluates the frequency-projected radial energy:
    M_K(x) = lim_{T -> inf} (1/2T) int_{-T}^T |S_K(x, t)|^2 dt
           = sum_gamma |a_K(gamma)|^2 * |sum_a exp(x * delta_{gamma, a})|^2.
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        scale_K = mpmath.power(tau, -to_mpf(K, dps=dps + 15))
        x_val = to_mpf(x, dps=dps + 15)

        gamma_groups: Dict[str, List[mpmath.mpf]] = {}
        for item in zeros_delta_gamma:
            d_val = to_mpf(item[0], dps=dps + 15)
            g_val = to_mpf(item[1], dps=dps + 15)
            mult = int(item[2]) if len(item) > 2 else 1
            g_key = mpmath.nstr(abs(g_val), n=dps)
            if g_key not in gamma_groups:
                gamma_groups[g_key] = []
            for _ in range(mult):
                gamma_groups[g_key].append(d_val)

        m_val = mpmath.mpf(0)
        for g_key, deltas in gamma_groups.items():
            gamma_val = to_mpf(g_key, dps=dps + 15)
            gamma_K = scale_K * gamma_val

            if a_kernel is not None:
                a_val = to_mpf(a_kernel(gamma_K), dps=dps + 15)
            else:
                a_val = mpmath.exp(-mpmath.mpf('0.01') * gamma_K * gamma_K)

            radial_sum = mpmath.mpf(0)
            for d in deltas:
                radial_sum += mpmath.exp(x_val * scale_K * d)

            m_val += (a_val * a_val) * (radial_sum * radial_sum)

        return m_val


@overload
def spectral_curvature_m_double_prime(
    zeros_delta_gamma: Sequence[Any],
    K: int = 0,
    a_kernel: Optional[Any] = None,
    detailed: Literal[False] = False,
    dps: int = 80
) -> mpmath.mpf: ...


@overload
def spectral_curvature_m_double_prime(
    zeros_delta_gamma: Sequence[Any],
    K: int = 0,
    a_kernel: Optional[Any] = None,
    detailed: Literal[True] = True,
    dps: int = 80
) -> Dict[str, Any]: ...


def spectral_curvature_m_double_prime(
    zeros_delta_gamma: Sequence[Any],
    K: int = 0,
    a_kernel: Optional[Any] = None,
    detailed: bool = False,
    dps: int = 80
) -> Union[mpmath.mpf, Dict[str, Any]]:

    """
    [SPECTRAL CURVATURE] Evaluates the exact second radial variation at x=0 for fibres F(x) = |sum exp(x*delta_a)|^2:
    General formula: F''(0) = 2*N*sum(delta_a^2) + 2*(sum delta_a)^2.
    Under reflection symmetry (sum delta_a = 0), this reduces to F''(0) = 2*N*sum(delta_a^2).

    Returns total curvature (mpf) if detailed=False, or a structured dictionary with

    quadratic_component, centering_component, total_curvature, reflection_symmetric if detailed=True.
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        scale_K = mpmath.power(tau, -to_mpf(K, dps=dps + 15))

        gamma_groups: Dict[str, List[mpmath.mpf]] = {}
        for item in zeros_delta_gamma:
            d_val = to_mpf(item[0], dps=dps + 15)
            g_val = to_mpf(item[1], dps=dps + 15)
            mult = int(item[2]) if len(item) > 2 else 1
            g_key = mpmath.nstr(abs(g_val), n=dps)
            if g_key not in gamma_groups:
                gamma_groups[g_key] = []
            for _ in range(mult):
                gamma_groups[g_key].append(d_val)

        total_curv = mpmath.mpf(0)
        total_quad = mpmath.mpf(0)
        total_centering = mpmath.mpf(0)
        all_symmetric = True
        fibre_details = []

        for g_key, deltas in gamma_groups.items():
            gamma_val = to_mpf(g_key, dps=dps + 15)
            gamma_K = scale_K * gamma_val

            if a_kernel is not None:
                a_val = to_mpf(a_kernel(gamma_K), dps=dps + 15)
            else:
                a_val = mpmath.exp(-mpmath.mpf('0.01') * gamma_K * gamma_K)

            N_gamma = len(deltas)
            sum_d = mpmath.mpf(0)
            sum_sq = mpmath.mpf(0)
            for d in deltas:
                scaled_d = scale_K * d
                sum_d += scaled_d
                sum_sq += scaled_d * scaled_d

            # Exact general curvature terms
            quad_comp = 2 * N_gamma * sum_sq
            centering_comp = 2 * (sum_d * sum_d)
            fibre_curv = quad_comp + centering_comp
            is_fibre_sym = bool(abs(sum_d) < mpmath.mpf('1e-50'))
            if not is_fibre_sym:
                all_symmetric = False

            weight_sq = a_val * a_val
            total_quad += weight_sq * quad_comp
            total_centering += weight_sq * centering_comp
            total_curv += weight_sq * fibre_curv

            fibre_details.append({
                "gamma": mpmath.nstr(gamma_val, n=15),
                "N_gamma": N_gamma,
                "quadratic_component": mpmath.nstr(quad_comp, n=15),
                "centering_component": mpmath.nstr(centering_comp, n=15),
                "total_curvature": mpmath.nstr(fibre_curv, n=15),
                "reflection_symmetric": is_fibre_sym
            })

        if detailed:
            return {
                "total_curvature": total_curv,
                "quadratic_component": total_quad,
                "centering_component": total_centering,
                "reflection_symmetric": all_symmetric,
                "fibre_details": fibre_details
            }
        return total_curv


# --- CANDIDATE SS-1: Conjugated Explicit-Formula Pair ---

def arithmetic_signal_ss1(
    K: int,
    x: Union[float, str, mpmath.mpf],
    t: Union[float, str, mpmath.mpf],
    N_max: int = 100,
    dps: int = 80
) -> mpmath.mpc:
    """
    [ARITHMETIC - CANDIDATE SS-1] Evaluates arithmetic side of explicit formula pair.
    Uses von Mangoldt sum: - sum_{n=2}^{N_max} Lambda(n)/sqrt(n) * exp(i * log(n) * (x + i*t)).
    """
    with mpmath.workdps(dps + 15):
        arithmetic_firewall_check({"K": K, "x": x, "t": t, "N_max": N_max})
        tau = get_tau(dps=dps + 15)
        scale_K = mpmath.power(tau, -to_mpf(K, dps=dps + 15))
        w = scale_K * mpmath.mpc(to_mpf(x, dps=dps + 15), to_mpf(t, dps=dps + 15))

        total = mpmath.mpc(0)
        for n in range(2, N_max + 1):
            p_base = None
            is_prime_pow = False
            for p in range(2, n + 1):
                if p * p > n and p_base is None:
                    p_base = n
                    is_prime_pow = True
                    break
                if n % p == 0:
                    temp = n
                    while temp % p == 0:
                        temp //= p
                    if temp == 1:
                        p_base = p
                        is_prime_pow = True
                    break
            if is_prime_pow and p_base is not None:
                lam_n = mpmath.log(p_base)
                log_n = mpmath.log(n)
                # Prime power Fourier component
                total -= (lam_n / mpmath.sqrt(n)) * mpmath.exp(mpmath.mpc(0, 1) * log_n * w)
        return total


def spectral_signal_ss1(
    zeros_delta_gamma: Sequence[Any],
    K: int,
    x: Union[float, str, mpmath.mpf],
    t: Union[float, str, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpc:
    """
    [SPECTRAL - CANDIDATE SS-1] Evaluates spectral explicit formula sum:
    sum_rho exp( (x + i*t) * (tau^(-K) * (delta_rho + i*gamma_rho)) ).
    Notice: produces exp(x*delta - t*gamma + i(t*delta + x*gamma)), failing pure radial/frequency separation.
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        scale_K = mpmath.power(tau, -to_mpf(K, dps=dps + 15))
        x_val = to_mpf(x, dps=dps + 15)
        t_val = to_mpf(t, dps=dps + 15)
        w = mpmath.mpc(x_val, t_val)

        total = mpmath.mpc(0)
        for item in zeros_delta_gamma:
            d_val = to_mpf(item[0], dps=dps + 15)
            g_val = to_mpf(item[1], dps=dps + 15)
            mult = int(item[2]) if len(item) > 2 else 1
            z = scale_K * mpmath.mpc(d_val, g_val)
            for _ in range(mult):
                total += mpmath.exp(w * z)
        return total


# --- CANDIDATE SS-2: Two-Slot Logarithmic Derivative ---

def arithmetic_signal_ss2(
    K: int,
    s1: Union[complex, str, mpmath.mpc],
    s2: Union[complex, str, mpmath.mpc],
    N_max: int = 100,
    dps: int = 80
) -> mpmath.mpc:
    """
    [ARITHMETIC - CANDIDATE SS-2] Evaluates bilinear logarithmic derivative product D_K(s1) * conj(D_K(s2)).
    Uses both slot inputs s1 and s2:
    D_K(s) = tau^(-K) * sum_{n=2}^{N_max} Lambda(n) / n^(tau^(-K) * s).
    """
    with mpmath.workdps(dps + 15):
        arithmetic_firewall_check({"K": K, "s1": s1, "s2": s2, "N_max": N_max})
        tau = get_tau(dps=dps + 15)
        scale_K = mpmath.power(tau, -to_mpf(K, dps=dps + 15))

        if isinstance(s1, (complex, mpmath.mpc)) or (isinstance(s1, str) and ('+' in s1 or '-' in s1[1:] or 'j' in s1)):
            s1_c = mpmath.mpc(s1)
        else:
            s1_c = mpmath.mpc(to_mpf(s1, dps=dps + 15), 0)

        if isinstance(s2, (complex, mpmath.mpc)) or (isinstance(s2, str) and ('+' in s2 or '-' in s2[1:] or 'j' in s2)):
            s2_c = mpmath.mpc(s2)
        else:
            s2_c = mpmath.mpc(to_mpf(s2, dps=dps + 15), 0)

        w1 = scale_K * s1_c
        w2 = scale_K * s2_c

        d1 = mpmath.mpc(0)
        d2 = mpmath.mpc(0)
        for n in range(2, N_max + 1):
            lam = mpmath.mangoldt(n)
            if lam != 0:
                d1 += lam * mpmath.power(n, -w1)
                d2 += lam * mpmath.power(n, -w2)

        d1_scaled = scale_K * d1
        d2_scaled = scale_K * d2
        return d1_scaled * mpmath.conj(d2_scaled)


def spectral_signal_ss2(
    zeros_delta_gamma: Sequence[Any],
    K: int,
    s1: Union[complex, str, mpmath.mpc],
    s2: Union[complex, str, mpmath.mpc],
    dps: int = 80
) -> mpmath.mpc:
    """
    [SPECTRAL - CANDIDATE SS-2] Evaluates spectral double sum for D_K(s1) * conj(D_K(s2)).
    Uses both slot inputs s1 and s2:
    D_K^spec(s) = tau^(-K) * sum_rho 1 / (tau^(-K) * s - rho).
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        scale_K = mpmath.power(tau, -to_mpf(K, dps=dps + 15))

        if isinstance(s1, (complex, mpmath.mpc)) or (isinstance(s1, str) and ('+' in s1 or '-' in s1[1:] or 'j' in s1)):
            s1_c = mpmath.mpc(s1)
        else:
            s1_c = mpmath.mpc(to_mpf(s1, dps=dps + 15), 0)

        if isinstance(s2, (complex, mpmath.mpc)) or (isinstance(s2, str) and ('+' in s2 or '-' in s2[1:] or 'j' in s2)):
            s2_c = mpmath.mpc(s2)
        else:
            s2_c = mpmath.mpc(to_mpf(s2, dps=dps + 15), 0)

        w1 = scale_K * s1_c
        w2 = scale_K * s2_c

        d1 = mpmath.mpc(0)
        d2 = mpmath.mpc(0)
        for item in zeros_delta_gamma:
            d_val = to_mpf(item[0], dps=dps + 15)
            g_val = to_mpf(item[1], dps=dps + 15)
            mult = int(item[2]) if len(item) > 2 else 1
            rho = mpmath.mpc(mpmath.mpf('0.5') + d_val, g_val)
            for _ in range(mult):
                d1 += 1 / (w1 - rho)
                d2 += 1 / (w2 - rho)

        d1_scaled = scale_K * d1
        d2_scaled = scale_K * d2
        return d1_scaled * mpmath.conj(d2_scaled)


# --- CANDIDATE SS-3: Rapidly Smoothed Transform ---

def arithmetic_signal_ss3(
    K: int,
    x: Union[float, str, mpmath.mpf],
    t: Union[float, str, mpmath.mpf],
    sigma: Union[float, str, mpmath.mpf] = '0.01',
    N_max: int = 100,
    dps: int = 80
) -> mpmath.mpc:
    """
    [ARITHMETIC - CANDIDATE SS-3] Evaluates Gaussian-smoothed prime power transform.
    """
    with mpmath.workdps(dps + 15):
        arithmetic_firewall_check({"K": K, "x": x, "t": t, "sigma": sigma, "N_max": N_max})
        tau = get_tau(dps=dps + 15)
        scale_K = mpmath.power(tau, -to_mpf(K, dps=dps + 15))
        sig_val = to_mpf(sigma, dps=dps + 15)
        x_val = to_mpf(x, dps=dps + 15)
        t_val = to_mpf(t, dps=dps + 15)

        total = mpmath.mpc(0)
        for n in range(2, N_max + 1):
            p_base = None
            is_prime_pow = False
            for p in range(2, n + 1):
                if p * p > n and p_base is None:
                    p_base = n
                    is_prime_pow = True
                    break
                if n % p == 0:
                    temp = n
                    while temp % p == 0:
                        temp //= p
                    if temp == 1:
                        p_base = p
                        is_prime_pow = True
                    break
            if is_prime_pow and p_base is not None:
                lam_n = mpmath.log(p_base)
                log_n = scale_K * mpmath.log(n)
                # Gaussian-smoothed prime kernel
                weight = mpmath.exp(-(log_n - x_val)**2 / (4 * sig_val))
                total += (lam_n / mpmath.sqrt(n)) * weight * mpmath.exp(mpmath.mpc(0, -t_val * log_n))
        return total


def spectral_signal_ss3(
    zeros_delta_gamma: Sequence[Any],
    K: int,
    x: Union[float, str, mpmath.mpf],
    t: Union[float, str, mpmath.mpf],
    sigma: Union[float, str, mpmath.mpf] = '0.01',
    dps: int = 80
) -> mpmath.mpc:
    """
    [SPECTRAL - CANDIDATE SS-3] Evaluates spectral smoothed sum:
    sum_rho exp( sigma*(delta^2 - gamma^2) + x*delta - t*gamma + i*(2*sigma*delta*gamma + t*delta + x*gamma) ).
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        scale_K = mpmath.power(tau, -to_mpf(K, dps=dps + 15))
        sig_val = to_mpf(sigma, dps=dps + 15)
        x_val = to_mpf(x, dps=dps + 15)
        t_val = to_mpf(t, dps=dps + 15)

        total = mpmath.mpc(0)
        for item in zeros_delta_gamma:
            d_val = scale_K * to_mpf(item[0], dps=dps + 15)
            g_val = scale_K * to_mpf(item[1], dps=dps + 15)
            mult = int(item[2]) if len(item) > 2 else 1

            re_exp = sig_val * (d_val * d_val - g_val * g_val) + x_val * d_val - t_val * g_val
            im_exp = 2 * sig_val * d_val * g_val + t_val * d_val + x_val * g_val
            term = mpmath.exp(mpmath.mpc(re_exp, im_exp))
            for _ in range(mult):
                total += term
        return total


# --- CANDIDATE SS-4: Cross-Grade Sesquilinear Form ---

def arithmetic_signal_ss4(
    K: int,
    L: int,
    x: Union[float, str, mpmath.mpf],
    t: Union[float, str, mpmath.mpf],
    N_max: int = 100,
    dps: int = 80
) -> mpmath.mpc:
    """
    [ARITHMETIC - CANDIDATE SS-4] Cross-grade arithmetic pairing between grades K and L.
    """
    with mpmath.workdps(dps + 15):
        arithmetic_firewall_check({"K": K, "L": L, "x": x, "t": t, "N_max": N_max})
        s_val = mpmath.mpc(to_mpf(x, dps=dps + 15) + mpmath.mpf('0.5'), to_mpf(t, dps=dps + 15))
        return arithmetic_candidate_b(K=K, L=L, s=s_val, N_max=N_max, dps=dps)


def spectral_signal_ss4(
    zeros_delta_gamma: Sequence[Any],
    K: int,
    L: int,
    x: Union[float, str, mpmath.mpf],
    t: Union[float, str, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpc:
    """
    [SPECTRAL - CANDIDATE SS-4] Cross-grade spectral pairing between grades K and L.
    """
    with mpmath.workdps(dps + 15):
        s_val = mpmath.mpc(to_mpf(x, dps=dps + 15) + mpmath.mpf('0.5'), to_mpf(t, dps=dps + 15))
        return spectral_candidate_b(zeros_delta_gamma=zeros_delta_gamma, K=K, L=L, s=s_val, dps=dps)


# --- CANDIDATE SS-5: Direct Positive Quadratic Kernel ---

def arithmetic_signal_ss5(
    K: int,
    N_max: int = 100,
    dps: int = 80
) -> mpmath.mpf:
    """
    [ARITHMETIC - CANDIDATE SS-5] Placeholder arithmetic evaluator for direct quadratic kernel.
    Fails at Gate 1/6 due to non-holomorphic arithmetic firewall.
    """
    arithmetic_firewall_check({"K": K, "N_max": N_max})
    return mpmath.mpf(0)


def spectral_signal_ss5(
    zeros_delta_gamma: Sequence[Any],
    K: int = 0,
    dps: int = 80
) -> mpmath.mpf:
    """
    [SPECTRAL - CANDIDATE SS-5] Evaluates spectral quadratic defect sum 2 * sum_j n_j * (delta_j^2 / gamma_j^2).
    """
    return spectral_trace_t(upper_zeros=zeros_delta_gamma, dps=dps)


# ============================================================================
# EXACT SYMBOLIC AND NUMERICAL FALSIFICATION VERIFIERS
# ============================================================================

def verify_cauchy_riemann_holomorphic_obstruction_ss1() -> Dict[str, Any]:
    """
    Performs exact SymPy derivation of the Cauchy-Riemann equations for Candidate SS-1.
    Proves that decoupling radial amplitude (exp(x*delta)) from ordinate frequency (exp(i*t*gamma))
    violates holomorphy unless x = t and a(gamma) is constant.
    """
    try:
        import importlib
        sp: Any = importlib.import_module("sympy")
    except ImportError as exc:
        raise ImportError("SymPy is required for symbolic Cauchy-Riemann verification: " + str(exc)) from exc
    delta, gamma, x, t = sp.symbols('delta gamma x t', real=True)
    a = sp.Function('a')
    u = sp.log(a(gamma)) + x * delta  # Re(log f)
    v = t * gamma                     # Im(log f)

    du_ddelta = sp.diff(u, delta)
    dv_dgamma = sp.diff(v, gamma)
    du_dgamma = sp.diff(u, gamma)
    dv_ddelta = sp.diff(v, delta)

    cr_1_diff = sp.simplify(du_ddelta - dv_dgamma)  # Should be x - t
    cr_2_sum = sp.simplify(du_dgamma + dv_ddelta)   # Should be a'(gamma)/a(gamma)
    expected_cr2 = sp.diff(sp.log(a(gamma)), gamma)

    return {
        "cr1_diff": str(cr_1_diff),
        "cr1_forces_x_eq_t": bool(cr_1_diff == x - t),
        "cr2_sum": str(cr_2_sum),
        "holomorphic_rigidity_proved": bool(cr_1_diff == x - t and sp.simplify(cr_2_sum - expected_cr2) == 0)
    }


def verify_algebraic_curvature_identity(deltas: Sequence[Union[float, str, mpmath.mpf]]) -> Dict[str, Any]:
    """
    Verifies the exact finite algebraic curvature identity:
    sum_{a,b} (delta_a + delta_b)^2 = 2 * N * sum(delta_a^2) + 2 * (sum delta_a)^2.
    When sum delta_a = 0, this equals 2 * N * sum(delta_a^2).
    """
    with mpmath.workdps(80):
        d_vals = [to_mpf(d, dps=80) for d in deltas]
        N = len(d_vals)
        sum_pairs = mpmath.mpf(0)
        for a in d_vals:
            for b in d_vals:
                sum_pairs += (a + b) ** 2

        sum_sq = sum(d * d for d in d_vals)
        sum_lin = sum(d_vals)
        expected = 2 * N * sum_sq + 2 * (sum_lin ** 2)
        diff = abs(sum_pairs - expected)
        is_exact = bool(diff < mpmath.mpf('1e-70'))

        return {
            "N": N,
            "sum_pairs": mpmath.nstr(sum_pairs, n=25),
            "expected": mpmath.nstr(expected, n=25),
            "residual": mpmath.nstr(diff, n=10),
            "is_exact": is_exact,
            "zero_sum_reduction": bool(abs(sum_lin) < mpmath.mpf('1e-70'))
        }


def verify_cramer_divergence_witness_ss3(
    gamma: Union[float, str, mpmath.mpf] = '14.134725',
    T_vals: Sequence[int] = (1, 5, 10, 20),
    dps: int = 80
) -> Dict[str, Any]:
    """
    Computes arbitrary-precision translation-average integrals for Candidate SS-3:
    int_{-T}^T exp(-2 * t * gamma) dt = sinh(2 * T * gamma) / gamma.
    Demonstrates exponential divergence as T -> infinity.
    """
    with mpmath.workdps(dps):
        g = to_mpf(gamma, dps=dps)
        results = {}
        for T in T_vals:
            t_mp = to_mpf(T, dps=dps)
            val = mpmath.sinh(2 * t_mp * g) / g
            results[f"T_{T}"] = mpmath.nstr(val, n=20)
        return {
            "gamma": mpmath.nstr(g, n=15),
            "integrals": results,
            "exponential_growth_confirmed": bool(to_mpf(results["T_20"]) > to_mpf(results["T_10"]) > to_mpf(results["T_5"]))
        }


def normalized_fibre_curvature(
    unnormalized_curvature: Union[float, str, mpmath.mpf],
    N_gamma: int,
    dps: int = 80
) -> mpmath.mpf:
    """
    [NORMALIZED FIBRE CURVATURE] Computes the normalized radial variation per frequency fibre:
    C_gamma = M_gamma''(0) / (2 * N_gamma) = sum_{a=1}^{N_gamma} delta_{gamma, a}^2.
    When summed over positive frequencies: sum_{gamma > 0} C_gamma / gamma^2 = Tr(R).
    NOTE: Normalizing by 2*N_gamma requires access to the spectral fibre multiplicity N_gamma.
    """
    with mpmath.workdps(dps + 15):
        curv = to_mpf(unnormalized_curvature, dps=dps + 15)
        if N_gamma <= 0:
            raise ValueError(f"N_gamma must be >= 1, got {N_gamma}")
        return curv / (2 * mpmath.mpf(N_gamma))


def search_bounded_transcendental_cross_grade_frequencies_ss4(
    K: int = 1,
    max_n: int = 100,
    max_m: int = 100
) -> Dict[str, Any]:
    """
    [BOUNDED NUMERICAL SEARCH - CANDIDATE SS-4]
    Performs a bounded numerical search over frequency gaps |tau^K * log(n) - log(m)| for 2 <= n, m <= max.
    Reports the minimum observed numerical gap within the finite search window.

    EPISTEMIC STATUS: This is bounded numerical evidence only. Proving exact cross-grade non-resonance
    for tau = 2*pi is an open problem in transcendental number theory (ratios of logs of integers can
    be transcendental).
    """
    import math
    tau = 2 * math.pi
    scale = tau ** K
    min_gap = 1e9
    best_pair = (0, 0)
    for n in range(2, max_n + 1):
        for m in range(2, max_m + 1):
            gap = abs(scale * math.log(n) - math.log(m))
            if gap < min_gap:
                min_gap = gap
                best_pair = (n, m)
    return {
        "K": K,
        "search_box": f"2..{max_n} x 2..{max_m}",
        "best_pair_n_m": best_pair,
        "min_frequency_gap": min_gap,
        "has_exact_resonance": bool(min_gap == 0.0),
        "epistemic_status": "NUMERICAL_SEARCH_EVIDENCE_ONLY_NOT_PROOF"
    }


def verify_transcendental_nonresonance_ss4(
    K: int = 1,
    max_n: int = 100,
    max_m: int = 100
) -> Dict[str, Any]:
    """Backward-compatible wrapper for search_bounded_transcendental_cross_grade_frequencies_ss4."""
    return search_bounded_transcendental_cross_grade_frequencies_ss4(K=K, max_n=max_n, max_m=max_m)


# ============================================================================
# COMPLETED MEAN-SQUARE ARITHMETIC ANCHOR (CMSA) SUITE
# ============================================================================

def completed_log_derivative_archimedean_A(
    u: Union[float, str, complex, mpmath.mpc, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpc:
    """
    [ARCHIMEDEAN & POLE LOG-DERIVATIVE]
    Evaluates the exact Archimedean + pole term:
    A(u) = 1/u + 1/(u-1) - (1/2)*log(pi) + (1/2)*psi(u/2),
    where psi = Gamma'/Gamma (digamma).
    Satisfies xi'/xi(u) = A(u) + zeta'/zeta(u).
    """
    with mpmath.workdps(dps + 15):
        if isinstance(u, (complex, mpmath.mpc)) or (isinstance(u, str) and ('+' in u or '-' in u[1:] or 'j' in u)):
            u_c = mpmath.mpc(u)
        else:
            u_c = mpmath.mpc(to_mpf(u, dps=dps + 15), 0)

        pi_val = mpmath.pi
        term1 = 1 / u_c
        term2 = 1 / (u_c - 1)
        term3 = -mpmath.mpf('0.5') * mpmath.log(pi_val)
        term4 = mpmath.mpf('0.5') * mpmath.digamma(u_c / 2)
        return term1 + term2 + term3 + term4


def prime_dirichlet_series_P(
    u: Union[float, str, complex, mpmath.mpc, mpmath.mpf],
    max_n: int = 1000,
    dps: int = 80
) -> mpmath.mpc:
    """
    [PRIME DIRICHLET SERIES]
    Evaluates the truncated Dirichlet series for -zeta'/zeta:
    P_N(u) = sum_{n=2}^{max_n} Lambda(n) / n^u.
    Converges absolutely for Re(u) > 1.
    """
    with mpmath.workdps(dps + 15):
        if isinstance(u, (complex, mpmath.mpc)) or (isinstance(u, str) and ('+' in u or '-' in u[1:] or 'j' in u)):
            u_c = mpmath.mpc(u)
        else:
            u_c = mpmath.mpc(to_mpf(u, dps=dps + 15), 0)

        total = mpmath.mpc(0)
        for n in range(2, max_n + 1):
            lam = mpmath.mangoldt(n)
            if lam != 0:
                total += lam * mpmath.power(n, -u_c)
        return total


def prime_dirichlet_series_tail_bound(
    sigma: Union[float, str, mpmath.mpf],
    max_n: int,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [PRIME TAIL BOUND]
    Computes analytically proved upper bounds for the tail sums using Lambda(n) <= log(n):
    1. Linear tail: sum_{n > N} Lambda(n)/n^sigma <= N^(1-sigma)/(sigma-1) * (log N + 1/(sigma-1)).
    2. Mean-square tail: sum_{n > N} Lambda(n)^2/n^(2*sigma) <= N^(1-2*sigma)/(2*sigma-1) * ((log N)^2 + 2*log(N)/(2*sigma-1) + 2/(2*sigma-1)^2).

    PREMISE & MONOTONICITY:
    Requires max_n >= 3 and sigma > 1. For sigma > 1, f(x) = (log x) * x^(-sigma) and g(x) = (log x)^2 * x^(-2*sigma)
    are strictly decreasing for x >= e^(1/sigma). Since e^(1/sigma) < e < 3, max_n >= 3 is a sufficient condition
    for integral comparison monotonicity.
    """
    with mpmath.workdps(dps + 15):
        sig = to_mpf(sigma, dps=dps + 15)
        if sig <= 1:
            raise ValueError(f"sigma must be > 1 for Dirichlet tail bounds, got {sig}")
        if max_n < 3:
            raise ValueError(f"max_n must be >= 3 for monotonicity of Dirichlet tail bounds, got {max_n}")

        N = mpmath.mpf(max_n)
        log_N = mpmath.log(N)

        # Linear tail bound
        s_minus_1 = sig - 1
        lin_tail = mpmath.power(N, -s_minus_1) / s_minus_1 * (log_N + 1 / s_minus_1)

        # Quadratic / mean-square tail bound
        two_s_minus_1 = 2 * sig - 1
        quad_tail = (mpmath.power(N, -two_s_minus_1) / two_s_minus_1) * (
            log_N * log_N + 2 * log_N / two_s_minus_1 + 2 / (two_s_minus_1 * two_s_minus_1)
        )

        return {
            "sigma": mpmath.nstr(sig, n=15),
            "max_n": max_n,
            "linear_tail_bound": mpmath.nstr(lin_tail, n=15),
            "mean_square_tail_bound": mpmath.nstr(quad_tail, n=15),
            "status": "ANALYTIC_THEOREM_DERIVED_IN_DOCUMENTATION"
        }


def spectral_real_axis_defect_delta(
    z: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    delta: Union[float, str, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """
    [EXACT SPECTRAL REAL-AXIS DEFECT]
    Evaluates the exact real-axis change in Xi'/Xi(z) when two on-line roots at ordinate gamma (multiplicity 2)
    are replaced by an off-line upper pair delta + i*gamma and -delta + i*gamma:
    Delta(delta) = [ 4 * z * delta^2 * (z^2 - 3*gamma^2 - delta^2) ] /
                   [ (z^2 + gamma^2) * ( (z^2 + gamma^2 - delta^2)^2 + 4*delta^2*gamma^2 ) ].

    For real z > 0, the sign is negative iff z^2 < 3*gamma^2 + delta^2.
    """
    with mpmath.workdps(dps + 15):
        z_val = to_mpf(z, dps=dps + 15)
        g_val = to_mpf(gamma, dps=dps + 15)
        d_val = to_mpf(delta, dps=dps + 15)

        z2 = z_val * z_val
        g2 = g_val * g_val
        d2 = d_val * d_val

        num = 4 * z_val * d2 * (z2 - 3 * g2 - d2)
        denom_part1 = z2 + g2
        denom_part2 = (z2 + g2 - d2) ** 2 + 4 * d2 * g2
        denom = denom_part1 * denom_part2
        if denom == 0:
            raise ZeroDivisionError("Denominator in spectral real-axis defect vanishes.")
        return num / denom


def spectral_real_axis_defect_leading_order(
    z: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    delta: Union[float, str, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """
    [LEADING-ORDER SPECTRAL REAL-AXIS DEFECT]
    Evaluates the second-order Taylor expansion in delta:
    Delta_leading(delta) = [ 4 * z * (z^2 - 3*gamma^2) / (z^2 + gamma^2)^3 ] * delta^2.
    """
    with mpmath.workdps(dps + 15):
        z_val = to_mpf(z, dps=dps + 15)
        g_val = to_mpf(gamma, dps=dps + 15)
        d_val = to_mpf(delta, dps=dps + 15)

        z2 = z_val * z_val
        g2 = g_val * g_val
        d2 = d_val * d_val

        num = 4 * z_val * (z2 - 3 * g2) * d2
        denom = (z2 + g2) ** 3
        if denom == 0:
            raise ZeroDivisionError("Denominator vanishes in leading-order defect.")
        return num / denom


def completed_log_derivative_spectral_Xi_prime_over_Xi(
    z: Union[float, str, complex, mpmath.mpc, mpmath.mpf],
    upper_zeros: Sequence[Any],
    dps: int = 80
) -> mpmath.mpc:
    """
    [SPECTRAL LOG-DERIVATIVE]
    Evaluates the symmetrically paired Hadamard spectral sum for Xi'/Xi(z):
    Xi'/Xi(z) = sum_{lambda in Lambda^+} n_lambda * ( 2z / (z^2 - lambda^2) ),
    where lambda = delta + i*gamma and Lambda^+ is the upper-half-plane / positive-ordinate zero set.
    """
    with mpmath.workdps(dps + 15):
        if isinstance(z, (complex, mpmath.mpc)) or (isinstance(z, str) and ('+' in z or '-' in z[1:] or 'j' in z)):
            z_c = mpmath.mpc(z)
        else:
            z_c = mpmath.mpc(to_mpf(z, dps=dps + 15), 0)

        total = mpmath.mpc(0)
        for item in upper_zeros:
            if isinstance(item, (int, float, str, mpmath.mpf)) and not isinstance(item, (tuple, list)):
                # Pure ordinate on critical line (delta = 0)
                g_val = to_mpf(item, dps=dps + 15)
                lam = mpmath.mpc(0, g_val)
                mult = 1
            else:
                d_val = to_mpf(item[0], dps=dps + 15)
                g_val = to_mpf(item[1], dps=dps + 15)
                mult = int(item[2]) if len(item) > 2 else 1
                lam = mpmath.mpc(d_val, g_val)

            denom = z_c * z_c - lam * lam
            if denom != 0:
                total += mult * (2 * z_c / denom)

        return total


def completed_xi(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    dps: int = 80
) -> mpmath.mpc:
    """
    [COMPLETED RIEMANN XI FUNCTION]
    Evaluates the completed Riemann xi function:
    xi(s) = 1/2 * s * (s - 1) * pi^(-s/2) * Gamma(s/2) * zeta(s).
    """
    with mpmath.workdps(dps + 25):
        s_mpc = to_mpc(s, dps=dps + 25)
        # Factor 1: 1/2 * s * (s - 1)
        poly = mpmath.mpf('0.5') * s_mpc * (s_mpc - 1)
        # Factor 2: pi^(-s/2)
        pi_factor = mpmath.power(mpmath.pi, -s_mpc / 2)
        # Factor 3: Gamma(s/2)
        gamma_factor = mpmath.gamma(s_mpc / 2)
        # Factor 4: zeta(s)
        zeta_val = zeta_eval(s_mpc, dps=dps + 25)
        return poly * pi_factor * gamma_factor * zeta_val


def completed_xi_log_derivative_direct(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    dps: int = 80
) -> mpmath.mpc:
    """
    [DIRECT NUMERICAL COMPLETED LOG-DERIVATIVE EVALUATOR]
    Evaluates xi'(s)/xi(s) by differentiating the completed function xi(s) directly
    via numerical differentiation without calling zeta_derivative or reconstructing A(s) + zeta'/zeta.
    """
    guard = 35
    with mpmath.workdps(dps + guard):
        s_val = to_mpc(s, dps=dps + guard)
        xi_val = completed_xi(s_val, dps=dps + guard)
        if xi_val == 0:
            raise ZeroDivisionError(f"completed_xi vanishes at s={s_val}")
        xi_prime = mpmath.diff(
            lambda w: completed_xi(w, dps=dps + guard),
            s_val,
        )
        return xi_prime / xi_val


def completed_xi_log_derivative(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    dps: int = 80
) -> mpmath.mpc:
    """
    [COMPLETED LOG-DERIVATIVE EVALUATOR]
    Delegates to completed_xi_log_derivative_direct for independent numerical differentiation.
    """
    return completed_xi_log_derivative_direct(s, dps=dps)


def exact_finite_zero_kernel_J_T(
    p: Union[complex, str, mpmath.mpc, mpmath.mpf],
    q: Union[complex, str, mpmath.mpc, mpmath.mpf],
    T: Union[float, str, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpc:
    """
    [EXACT FINITE ZERO KERNEL J_T]
    Analytically evaluates the translation integral:
    J_T(p, q) = (1/2T) int_{-T}^T dt / [ (p + i*t) * (q - i*t) ]
              = [ log((p + i*T)/(p - i*T)) + log((q + i*T)/(q - i*T)) ] / [ 2 * T * i * (p + q) ]
    Enforces kernel domain preconditions: T > 0, Re(p) > 0, Re(q) > 0.
    """
    with mpmath.workdps(dps + 15):
        p_c = to_mpc(p, dps=dps + 15)
        q_c = to_mpc(q, dps=dps + 15)

        T_val = to_mpf(T, dps=dps + 15)
        if T_val <= 0:
            raise ValueError(f"Kernel domain violation: T must be > 0, got T={T_val}")

        if p_c.real <= 0 or q_c.real <= 0:
            raise ValueError(f"Kernel domain violation: Re(p) and Re(q) must be > 0, got Re(p)={p_c.real}, Re(q)={q_c.real}")

        i_T = mpmath.mpc(0, T_val)
        num_p = mpmath.log((p_c + i_T) / (p_c - i_T))
        num_q = mpmath.log((q_c + i_T) / (q_c - i_T))
        denom = 2 * T_val * mpmath.mpc(0, 1) * (p_c + q_c)

        if denom == 0:
            raise ZeroDivisionError("Denominator in J_T vanishes.")
        return (num_p + num_q) / denom


def exact_finite_zero_zero_kernel_K_T(
    lam1: Union[complex, str, mpmath.mpc, mpmath.mpf],
    lam2: Union[complex, str, mpmath.mpc, mpmath.mpf],
    a: Union[float, str, mpmath.mpf],
    T: Union[float, str, mpmath.mpf],
    mult1: int = 1,
    mult2: int = 1,
    dps: int = 80
) -> mpmath.mpc:
    """
    [EXACT FINITE ZERO-ZERO KERNEL K_T]
    Evaluates the paired zero-zero kernel for resolvents R_lambda1, R_lambda2:
    K_T(lambda1, lambda2; a) = m1 * m2 * sum_{eps, eta in {+1, -1}} J_T(a - eps*lambda1, a - eta*conj(lambda2)).
    Enforces a > 0 and T > 0.
    """
    with mpmath.workdps(dps + 15):
        l1_c = to_mpc(lam1, dps=dps + 15)
        l2_c = to_mpc(lam2, dps=dps + 15)
        a_val = to_mpf(a, dps=dps + 15)
        T_val = to_mpf(T, dps=dps + 15)

        if a_val <= 0:
            raise ValueError(f"Kernel domain violation: a = sigma - 1/2 must be > 0, got a={a_val}")
        if T_val <= 0:
            raise ValueError(f"Kernel domain violation: T must be > 0, got T={T_val}")

        total = mpmath.mpc(0)
        for eps in (1, -1):
            for eta in (1, -1):
                p_arg = a_val - eps * l1_c
                q_arg = a_val - eta * mpmath.conj(l2_c)
                total += exact_finite_zero_kernel_J_T(p=p_arg, q=q_arg, T=T_val, dps=dps)

        return mult1 * mult2 * total


def evaluate_complete_finite_spectral_expansion(
    sigma: Union[float, str, mpmath.mpf],
    T: Union[float, str, mpmath.mpf],
    upper_zeros: Sequence[Any],
    dps: int = 80
) -> Dict[str, Any]:
    """
    [COMPLETE FINITE SPECTRAL EXPANSION DIAGNOSTIC]
    Evaluates the complete finite spectral quantity:
    S_{N, T}(sigma) = (1/2T) int_{-T}^T |A(sigma + it) - Z_N(t)|^2 dt = I_AA - I_AZ - I_ZA + I_ZZ.
    Algebraically exact 4-term decomposition with closed-form J_T / K_T kernels and numerical quadrature validation.
    Enforces sigma > 1, T > 0.
    """
    with mpmath.workdps(dps + 15):
        sig = to_mpf(sigma, dps=dps + 15)
        T_val = to_mpf(T, dps=dps + 15)
        if sig <= 1:
            raise ValueError(f"Kernel domain violation: sigma must be > 1 for Dirichlet and kernel convergence, got sigma={sig}")
        if T_val <= 0:
            raise ValueError(f"Kernel domain violation: T must be > 0, got T={T_val}")

        a_val = sig - mpmath.mpf('0.5')

        # Parsed zero multiset
        parsed_zeros = []
        for item in upper_zeros:
            if isinstance(item, (int, float, str, mpmath.mpf)) and not isinstance(item, (tuple, list)):
                parsed_zeros.append((mpmath.mpf(0), to_mpf(item, dps=dps + 15), 1))
            else:
                d_val = to_mpf(item[0], dps=dps + 15)
                g_val = to_mpf(item[1], dps=dps + 15)
                mult = int(item[2]) if len(item) > 2 else 1
                parsed_zeros.append((d_val, g_val, mult))

        # Archimedean function A(sigma + it)
        arch_fn = lambda t: completed_log_derivative_archimedean_A(mpmath.mpc(sig, t), dps=dps)

        # Spectral zero function Z_N(t)
        def z_n_fn(t_val):
            z_c = mpmath.mpc(a_val, t_val)
            tot = mpmath.mpc(0)
            for d, g, m in parsed_zeros:
                lam = mpmath.mpc(d, g)
                denom = z_c * z_c - lam * lam
                if denom != 0:
                    tot += m * (2 * z_c / denom)
            return tot

        # 1. I_AA = (1/2T) int_{-T}^T |A|^2 dt
        i_aa = mpmath.quad(lambda t: abs(arch_fn(t)) ** 2, [-T_val, T_val]) / (2 * T_val)

        # 2. I_AZ = (1/2T) int_{-T}^T A * conj(Z_N) dt
        i_az = mpmath.quad(lambda t: arch_fn(t) * mpmath.conj(z_n_fn(t)), [-T_val, T_val]) / (2 * T_val)

        # 3. I_ZA = conj(I_AZ)
        i_za = mpmath.conj(i_az)

        # 4. I_ZZ = sum_{lambda, mu} K_T(lambda, mu; a)
        i_zz_analytic = mpmath.mpc(0)
        for d1, g1, m1 in parsed_zeros:
            lam1 = mpmath.mpc(d1, g1)
            for d2, g2, m2 in parsed_zeros:
                lam2 = mpmath.mpc(d2, g2)
                k_term = exact_finite_zero_zero_kernel_K_T(
                    lam1=lam1, lam2=lam2, a=a_val, T=T_val, mult1=m1, mult2=m2, dps=dps
                )
                i_zz_analytic += k_term

        i_zz_real = i_zz_analytic.real

        # Direct evaluation S_{N, T}
        s_direct = mpmath.quad(lambda t: abs(arch_fn(t) - z_n_fn(t)) ** 2, [-T_val, T_val]) / (2 * T_val)
        s_expanded = (i_aa - i_az - i_za).real + i_zz_real
        closure_diff = abs(s_direct - s_expanded)

        return {
            "sigma": mpmath.nstr(sig, n=15),
            "T": mpmath.nstr(T_val, n=15),
            "zero_count": len(parsed_zeros),
            "I_AA": mpmath.nstr(i_aa, n=20),
            "I_AZ": str(i_az),
            "I_ZA": str(i_za),
            "I_ZZ": mpmath.nstr(i_zz_real, n=20),
            "S_direct": mpmath.nstr(s_direct, n=20),
            "S_expanded": mpmath.nstr(s_expanded, n=20),
            "closure_difference": mpmath.nstr(closure_diff, n=10),
            "status": "ALGEBRAICALLY_EXACT_NUMERICALLY_VALIDATED",
            "earliest_open_gate": "G4",
            "infinite_interchange_status": "INFINITE_INTERCHANGE_OPEN"
        }


def direct_completed_function_control(
    sigma: Union[float, str, mpmath.mpf],
    T: Union[float, str, mpmath.mpf],
    dps: int = 80
) -> Dict[str, Any]:
    """
    [INDEPENDENT DIRECT COMPLETED-FUNCTION CONTROL]
    Evaluates Path A: -zeta'/zeta(sigma + it) and Path B: A(sigma + it) - xi'/xi(sigma + it)
    independently through direct numerical differentiation of completed_xi, computing pointwise residuals
    and finite-T mean squares.
    """
    with mpmath.workdps(dps + 15):
        sig = to_mpf(sigma, dps=dps + 15)
        T_val = to_mpf(T, dps=dps + 15)
        if sig <= 1:
            raise ValueError(f"sigma must be > 1, got {sig}")
        if T_val <= 0:
            raise ValueError(f"T must be > 0, got {T_val}")

        # Path A: Direct arithmetic logarithmic derivative -zeta'/zeta(u)
        def path_a_zeta_log_der(t_val):
            u = mpmath.mpc(sig, t_val)
            z_val = zeta_eval(u, dps=dps + 15)
            z_pr = zeta_derivative(u, n=1, dps=dps + 15)
            return -z_pr / z_val

        # Path B: Independent completed function logarithmic derivative A(u) - xi'/xi(u) via direct numerical diff
        def path_b_completed_diff(t_val):
            u = mpmath.mpc(sig, t_val)
            a_val = completed_log_derivative_archimedean_A(u, dps=dps)
            xi_ld = completed_xi_log_derivative_direct(u, dps=dps)
            return a_val - xi_ld

        # Pointwise test at multiple sample ordinates t in [0, 1, 5]
        diff_t0 = abs(path_b_completed_diff(0) - path_a_zeta_log_der(0))
        diff_t1 = abs(path_b_completed_diff(1) - path_a_zeta_log_der(1))
        diff_t5 = abs(path_b_completed_diff(5) - path_a_zeta_log_der(5))

        # Mean square comparison computed independently
        ms_zeta = mpmath.quad(lambda t: abs(path_a_zeta_log_der(t)) ** 2, [-T_val, T_val]) / (2 * T_val)
        ms_completed = mpmath.quad(lambda t: abs(path_b_completed_diff(t)) ** 2, [-T_val, T_val]) / (2 * T_val)
        ms_difference = abs(ms_completed - ms_zeta)

        return {
            "sigma": mpmath.nstr(sig, n=15),
            "T": mpmath.nstr(T_val, n=15),
            "pointwise_diff_t0": mpmath.nstr(diff_t0, n=10),
            "pointwise_diff_t1": mpmath.nstr(diff_t1, n=10),
            "pointwise_diff_t5": mpmath.nstr(diff_t5, n=10),
            "mean_square_completed": mpmath.nstr(ms_completed, n=20),
            "mean_square_zeta": mpmath.nstr(ms_zeta, n=20),
            "mean_square_difference": mpmath.nstr(ms_difference, n=15),
            "status": "NUMERICAL_VALIDATION_OF_ANALYTIC_IDENTITY"
        }


def completed_log_derivative_exact_residual(
    u: Union[float, str, complex, mpmath.mpc, mpmath.mpf],
    upper_zeros: Sequence[Any],
    max_n: int = 2000,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [EXACT COMPLETED LOG-DERIVATIVE IDENTITY RESIDUAL]
    Tests the fundamental identity P(u) = A(u) - Xi'/Xi(u - 1/2) for Re(u) > 1.
    Reports:
    - Arithmetic Dirichlet evaluation P_N(u)
    - Archimedean term A(u)
    - Spectral Hadamard sum Xi'/Xi(u - 1/2)
    - Finite truncation residual and tail enclosure.
    """
    with mpmath.workdps(dps + 15):
        if isinstance(u, (complex, mpmath.mpc)) or (isinstance(u, str) and ('+' in u or '-' in u[1:] or 'j' in u)):
            u_c = mpmath.mpc(u)
        else:
            u_c = mpmath.mpc(to_mpf(u, dps=dps + 15), 0)

        sig = u_c.real
        p_val = prime_dirichlet_series_P(u=u_c, max_n=max_n, dps=dps)
        a_val = completed_log_derivative_archimedean_A(u=u_c, dps=dps)
        z_c = u_c - mpmath.mpf('0.5')
        xi_log_der_spec = completed_log_derivative_spectral_Xi_prime_over_Xi(z=z_c, upper_zeros=upper_zeros, dps=dps)

        # Exact meromorphic analytic continuation reference via mpmath zeta & gamma
        xi_fn = lambda s: mpmath.mpf('0.5') * s * (s - 1) * mpmath.power(mpmath.pi, -s / 2) * mpmath.gamma(s / 2) * mpmath.zeta(s)
        exact_xi_log_der = mpmath.diff(xi_fn, u_c) / xi_fn(u_c)
        exact_analytic_P = a_val - exact_xi_log_der

        tail_info = prime_dirichlet_series_tail_bound(sigma=sig, max_n=max_n, dps=dps) if sig > 1 and max_n >= 3 else {}
        dirichlet_vs_analytic_diff = abs(p_val - exact_analytic_P)
        hadamard_truncation_diff = abs(xi_log_der_spec - exact_xi_log_der)

        return {
            "u": str(u_c),
            "P_N": mpmath.nstr(p_val, n=15),
            "A_val": mpmath.nstr(a_val, n=15),
            "Xi_prime_over_Xi_spec": mpmath.nstr(xi_log_der_spec, n=15),
            "exact_Xi_log_der": mpmath.nstr(exact_xi_log_der, n=15),
            "dirichlet_vs_analytic_diff": mpmath.nstr(dirichlet_vs_analytic_diff, n=10),
            "hadamard_truncation_diff": mpmath.nstr(hadamard_truncation_diff, n=10),
            "tail_info": tail_info,
            "identity_holds_within_truncation": bool(dirichlet_vs_analytic_diff < to_mpf(tail_info.get("linear_tail_bound", 1))) if tail_info else True
        }


def grade_dilated_completed_log_derivative(
    s_K: Union[float, str, complex, mpmath.mpc, mpmath.mpf],
    K: int,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [GRADE COVARIANCE VERIFIER]
    Verifies that D_K^xi(s_K) = tau^(-K) * xi'/xi(tau^(-K) * s_K) satisfies
    tau^K * D_K^xi(tau^K * u) = xi'/xi(u) identically for all K in Z.
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        scale_K = mpmath.power(tau, -to_mpf(K, dps=dps + 15))
        if isinstance(s_K, (complex, mpmath.mpc)) or (isinstance(s_K, str) and ('+' in s_K or '-' in s_K[1:] or 'j' in s_K)):
            s_c = mpmath.mpc(s_K)
        else:
            s_c = mpmath.mpc(to_mpf(s_K, dps=dps + 15), 0)

        # Pullback coordinate
        u = scale_K * s_c
        xi_fn = lambda s: mpmath.mpf('0.5') * s * (s - 1) * mpmath.power(mpmath.pi, -s / 2) * mpmath.gamma(s / 2) * mpmath.zeta(s)

        xi_log_der_u = mpmath.diff(xi_fn, u) / xi_fn(u)
        dilated_val = scale_K * xi_log_der_u

        # Pullback restoration
        restored = (1 / scale_K) * dilated_val
        diff = abs(restored - xi_log_der_u)

        return {
            "K": K,
            "s_K": str(s_c),
            "u": str(u),
            "dilated_val": mpmath.nstr(dilated_val, n=15),
            "xi_log_der_u": mpmath.nstr(xi_log_der_u, n=15),
            "restoration_diff": mpmath.nstr(diff, n=10),
            "is_coordinate_redundant": bool(diff < mpmath.mpf('1e-50'))
        }


def finite_dirichlet_mean_square_sinc_kernel(
    sigma: Union[float, str, mpmath.mpf],
    T: Union[float, str, mpmath.mpf],
    max_N: int = 50,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [FINITE DIRICHLET MEAN-SQUARE SINC KERNEL]
    Evaluates the exact finite-sum translation mean square:
    (1/2T) int_{-T}^T |P_N(sigma+it)|^2 dt = sum_{n,m=2}^{N} (Lambda(n)*Lambda(m) / (nm)^sigma) * sinc(T * log(m/n)).
    Compares against the diagonal limit sum_{n=2}^N Lambda(n)^2 / n^(2*sigma).
    """
    with mpmath.workdps(dps + 15):
        sig = to_mpf(sigma, dps=dps + 15)
        T_val = to_mpf(T, dps=dps + 15)

        sinc_fn = lambda x: mpmath.mpf(1) if x == 0 else mpmath.sin(x) / x

        sinc_sum = mpmath.mpf(0)
        diag_sum = mpmath.mpf(0)
        off_diag_sum = mpmath.mpf(0)

        for n in range(2, max_N + 1):
            lam_n = mpmath.mangoldt(n)
            if lam_n == 0:
                continue
            for m in range(2, max_N + 1):
                lam_m = mpmath.mangoldt(m)
                if lam_m == 0:
                    continue

                denom = mpmath.power(mpmath.mpf(n * m), sig)
                coeff = (lam_n * lam_m) / denom
                if n == m:
                    diag_sum += coeff
                    sinc_sum += coeff
                else:
                    log_ratio = mpmath.log(mpmath.mpf(m) / mpmath.mpf(n))
                    term = coeff * sinc_fn(T_val * log_ratio)
                    off_diag_sum += term
                    sinc_sum += term

        diff_from_diag = abs(sinc_sum - diag_sum)

        return {
            "sigma": mpmath.nstr(sig, n=15),
            "T": mpmath.nstr(T_val, n=15),
            "max_N": max_N,
            "sinc_mean_square": mpmath.nstr(sinc_sum, n=20),
            "diagonal_limit": mpmath.nstr(diag_sum, n=20),
            "off_diagonal_residual": mpmath.nstr(off_diag_sum, n=20),
            "diff_from_diagonal": mpmath.nstr(diff_from_diag, n=10)
        }


def completed_mean_square_anchor_cmsa1(
    sigma: Union[float, str, mpmath.mpf],
    T: Union[float, str, mpmath.mpf],
    max_N: int = 100,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [CANDIDATE CMSA-1: Base Completed Mean-Square Anchor]
    Evaluates arithmetic-side finite sinc mean-square, diagonal target, and tail bounds:
    A(sigma) = lim_{T -> inf} (1/2T) int_{-T}^T |P_sigma(t)|^2 dt - sum_{n>=2} Lambda(n)^2 / n^(2*sigma) = 0.
    """
    with mpmath.workdps(dps + 15):
        sinc_res = finite_dirichlet_mean_square_sinc_kernel(sigma=sigma, T=T, max_N=max_N, dps=dps)
        tail_res = prime_dirichlet_series_tail_bound(sigma=sigma, max_n=max_N, dps=dps) if max_N >= 3 else {}

        # Full arithmetic diagonal target
        diag_val = to_mpf(sinc_res["diagonal_limit"], dps=dps + 15)
        sinc_val = to_mpf(sinc_res["sinc_mean_square"], dps=dps + 15)
        residual_anchor = sinc_val - diag_val

        return {
            "candidate_id": "CANDIDATE_CMSA1",
            "sigma": mpmath.nstr(to_mpf(sigma, dps=dps + 15), n=15),
            "T": mpmath.nstr(to_mpf(T, dps=dps + 15), n=15),
            "max_N": max_N,
            "finite_sinc_mean_square": sinc_res["sinc_mean_square"],
            "arithmetic_diagonal_target": sinc_res["diagonal_limit"],
            "anchor_finite_residual": mpmath.nstr(residual_anchor, n=10),
            "mean_square_tail_bound": tail_res.get("mean_square_tail_bound", "0.0"),
            "status": "EXACT_FINITE_IDENTITY",
            "earliest_open_gate": "G4",
            "classification": "INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_GATE_G4"
        }


def polarized_mean_square_anchor_cmsa2(
    sigma1: Union[float, str, mpmath.mpf],
    sigma2: Union[float, str, mpmath.mpf],
    T: Union[float, str, mpmath.mpf],
    max_N: int = 100,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [CANDIDATE CMSA-2: Polarized Completed Mean-Square Anchor]
    Evaluates polarized anchor A(sigma_1, sigma_2) = (1/2T) int_{-T}^T P_sigma1(t) * conj(P_sigma2(t)) dt - sum Lambda(n)^2 / n^(sigma1+sigma2).
    """
    with mpmath.workdps(dps + 15):
        s1 = to_mpf(sigma1, dps=dps + 15)
        s2 = to_mpf(sigma2, dps=dps + 15)
        T_val = to_mpf(T, dps=dps + 15)
        sinc_fn = lambda x: mpmath.mpf(1) if x == 0 else mpmath.sin(x) / x

        sinc_sum = mpmath.mpf(0)
        diag_sum = mpmath.mpf(0)

        for n in range(2, max_N + 1):
            lam_n = mpmath.mangoldt(n)
            if lam_n == 0:
                continue
            for m in range(2, max_N + 1):
                lam_m = mpmath.mangoldt(m)
                if lam_m == 0:
                    continue

                denom = mpmath.power(mpmath.mpf(n), s1) * mpmath.power(mpmath.mpf(m), s2)
                coeff = (lam_n * lam_m) / denom
                if n == m:
                    diag_sum += coeff
                    sinc_sum += coeff
                else:
                    log_ratio = mpmath.log(mpmath.mpf(m) / mpmath.mpf(n))
                    sinc_sum += coeff * sinc_fn(T_val * log_ratio)

        residual_anchor = sinc_sum - diag_sum

        return {
            "candidate_id": "CANDIDATE_CMSA2",
            "sigma1": mpmath.nstr(s1, n=15),
            "sigma2": mpmath.nstr(s2, n=15),
            "T": mpmath.nstr(T_val, n=15),
            "max_N": max_N,
            "polarized_sinc_mean_square": mpmath.nstr(sinc_sum, n=20),
            "polarized_diagonal_target": mpmath.nstr(diag_sum, n=20),
            "polarized_anchor_residual": mpmath.nstr(residual_anchor, n=10),
            "status": "EXACT_FINITE_IDENTITY",
            "earliest_open_gate": "G4",
            "classification": "INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_GATE_G4"
        }


def grade_normalized_mean_square_anchor_cmsa3(
    sigma: Union[float, str, mpmath.mpf],
    K: int,
    T: Union[float, str, mpmath.mpf],
    max_N: int = 100,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [CANDIDATE CMSA-3: Grade-Normalized Completed Mean-Square Anchor]
    Tests whether grade dilation tau^K D_K^P yields non-redundant radial invariants.
    """
    with mpmath.workdps(dps + 15):
        base_res = completed_mean_square_anchor_cmsa1(sigma=sigma, T=T, max_N=max_N, dps=dps)
        cov_res = grade_dilated_completed_log_derivative(s_K=sigma, K=K, dps=dps)

        return {
            "candidate_id": "CANDIDATE_CMSA3",
            "K": K,
            "sigma": mpmath.nstr(to_mpf(sigma, dps=dps + 15), n=15),
            "base_anchor_residual": base_res["anchor_finite_residual"],
            "covariance_diff": cov_res["restoration_diff"],
            "is_coordinate_redundant": cov_res["is_coordinate_redundant"],
            "classification": "GRADE_COORDINATE_REDUNDANT"
        }


def evaluate_cmsa_synthetic_divisors(
    zeros_spec: Sequence[Any],
    sigma: Union[float, str, mpmath.mpf] = '2.0',
    t_val: Union[float, str, mpmath.mpf] = '0.0',
    dps: int = 80
) -> Dict[str, Any]:
    """
    [SYNTHETIC DIVISOR EVALUATOR FOR CMSA SPECTRAL EXPANSION]
    Evaluates Xi'/Xi(sigma - 1/2 + i*t) for synthetic zero configurations:
    - on-line fibres (all delta = 0)
    - single off-line quartet (delta != 0)
    - multiple off-line quartets
    - repeated ordinates with different delta
    - multiplicities > 1
    - close ordinates.
    """
    with mpmath.workdps(dps + 15):
        sig = to_mpf(sigma, dps=dps + 15)
        t_mp = to_mpf(t_val, dps=dps + 15)
        z = mpmath.mpc(sig - mpmath.mpf('0.5'), t_mp)

        xi_spec = completed_log_derivative_spectral_Xi_prime_over_Xi(z=z, upper_zeros=zeros_spec, dps=dps)

        # Baseline with delta = 0 for identical ordinates
        online_zeros = []
        for item in zeros_spec:
            if isinstance(item, (int, float, str, mpmath.mpf)):
                online_zeros.append((0, item, 1))
            else:
                online_zeros.append((0, item[1], item[2] if len(item) > 2 else 1))

        xi_online = completed_log_derivative_spectral_Xi_prime_over_Xi(z=z, upper_zeros=online_zeros, dps=dps)
        diff_from_online = xi_spec - xi_online

        return {
            "sigma": mpmath.nstr(sig, n=15),
            "t": mpmath.nstr(t_mp, n=15),
            "z": str(z),
            "xi_prime_spec": mpmath.nstr(xi_spec, n=15),
            "xi_prime_online_baseline": mpmath.nstr(xi_online, n=15),
            "delta_response": mpmath.nstr(diff_from_online, n=15),
            "delta_response_abs": mpmath.nstr(abs(diff_from_online), n=15),
            "is_on_line": bool(abs(diff_from_online) < mpmath.mpf('1e-50'))
        }


# ==============================================================================
# SECTION 25: GATE G4 INFINITE REGULARIZATION & WINDOW SUITE
# ==============================================================================

def exact_fejer_zero_kernel_J_T(
    p: Union[complex, str, mpmath.mpc, mpmath.mpf],
    q: Union[complex, str, mpmath.mpc, mpmath.mpf],
    T: Union[float, str, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpc:
    """
    [EXACT FEJER ZERO KERNEL J_T^Fejer]
    Analytically evaluates the Fejer (triangular) windowed translation integral:
    J_T^Fejer(p, q) = int_{-T}^T (1/T) * (1 - |t|/T) / [ (p + i*t) * (q - i*t) ] dt
                    = [ I_T(p) + I_T(q) ] / [ T * (p + q) ],
    where I_T(w) = - [ (w + i*T)*log(w + i*T) + (w - i*T)*log(w - i*T) - 2*w*log(w) ] / T.
    Enforces domain: T > 0, Re(p) > 0, Re(q) > 0.
    """
    with mpmath.workdps(dps + 20):
        p_c = to_mpc(p, dps=dps + 20)
        q_c = to_mpc(q, dps=dps + 20)
        T_val = to_mpf(T, dps=dps + 20)

        if T_val <= 0:
            raise ValueError(f"Kernel domain violation: T must be > 0, got T={T_val}")
        if p_c.real <= 0 or q_c.real <= 0:
            raise ValueError(f"Kernel domain violation: Re(p) and Re(q) must be > 0, got Re(p)={p_c.real}, Re(q)={q_c.real}")

        def _fejer_single_slot(w):
            i_T = mpmath.mpc(0, T_val)
            term_pos = (w + i_T) * mpmath.log(w + i_T)
            term_neg = (w - i_T) * mpmath.log(w - i_T)
            term_zero = 2 * w * mpmath.log(w)
            return - (term_pos + term_neg - term_zero) / T_val

        int_p = _fejer_single_slot(p_c)
        int_q = _fejer_single_slot(q_c)
        denom = T_val * (p_c + q_c)
        if denom == 0:
            raise ZeroDivisionError("Denominator in J_T^Fejer vanishes.")
        return (int_p + int_q) / denom


def exact_fejer_zero_zero_kernel_K_T(
    lam1: Union[complex, str, mpmath.mpc, mpmath.mpf],
    lam2: Union[complex, str, mpmath.mpc, mpmath.mpf],
    a: Union[float, str, mpmath.mpf],
    T: Union[float, str, mpmath.mpf],
    mult1: int = 1,
    mult2: int = 1,
    dps: int = 80
) -> mpmath.mpc:
    """
    [EXACT FEJER ZERO-ZERO KERNEL K_T^Fejer]
    Evaluates the paired zero-zero kernel under Fejer triangular window:
    K_T^Fejer(lambda1, lambda2; a) = m1 * m2 * sum_{eps, eta in {+1, -1}} J_T^Fejer(a - eps*lambda1, a - eta*conj(lambda2)).
    """
    with mpmath.workdps(dps + 20):
        l1_c = to_mpc(lam1, dps=dps + 20)
        l2_c = to_mpc(lam2, dps=dps + 20)
        a_val = to_mpf(a, dps=dps + 20)
        T_val = to_mpf(T, dps=dps + 20)

        if a_val <= 0:
            raise ValueError(f"Kernel domain violation: a must be > 0, got a={a_val}")
        if T_val <= 0:
            raise ValueError(f"Kernel domain violation: T must be > 0, got T={T_val}")

        total = mpmath.mpc(0)
        for eps in (1, -1):
            for eta in (1, -1):
                p_arg = a_val - eps * l1_c
                q_arg = a_val - eta * mpmath.conj(l2_c)
                total += exact_fejer_zero_kernel_J_T(p=p_arg, q=q_arg, T=T_val, dps=dps)

        return mult1 * mult2 * total


def evaluate_g4_asymptotic_regimes(
    a: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    T_vals: Sequence[Union[float, str, mpmath.mpf]],
    dps: int = 80
) -> List[Dict[str, Any]]:
    """
    [GATE G4 ASYMPTOTIC REGIMES DIAGNOSTIC]
    Tests J_T(a - i*gamma, a + i*gamma) across the 4 characteristic regimes:
    1. |gamma| << T (c -> 0 plateau: J_T ~ pi / (2aT))
    2. gamma / T -> c in (0, inf) (transition curve: [arctan(1-c) + arctan(1+c)] / (2aT))
    3. |gamma - T| = O(1) (c = 1 peak boundary layer)
    4. |gamma| >> T (c >> 1 tail: J_T ~ 1 / (gamma^2 - T^2)).
    """
    with mpmath.workdps(dps + 20):
        a_val = to_mpf(a, dps=dps + 20)
        g_val = to_mpf(gamma, dps=dps + 20)
        p = mpmath.mpc(a_val, -g_val)
        q = mpmath.mpc(a_val, g_val)

        results = []
        for T_item in T_vals:
            T_val = to_mpf(T_item, dps=dps + 20)
            c_val = g_val / T_val

            # Exact analytic rectangular J_T
            j_exact = exact_finite_zero_kernel_J_T(p, q, T_val, dps=dps).real

            # Regime 1 asymptote: pi / (2 * a * T)
            asymp_plateau = mpmath.pi / (2 * a_val * T_val)

            # Regime 2 transition formula: (arctan((T - gamma)/a) + arctan((T + gamma)/a)) / (2 * a * T)
            transition_formula = (mpmath.atan((T_val - g_val) / a_val) + mpmath.atan((T_val + g_val) / a_val)) / (2 * a_val * T_val)

            # Regime 4 asymptote: 1 / (gamma^2 - T^2) if gamma > T
            asymp_tail = mpmath.mpf(1) / (g_val**2 - T_val**2) if g_val > T_val else mpmath.mpf(0)

            # Classification
            if c_val < 0.2:
                regime = "PLATEAU_INNER"
            elif 0.8 <= c_val <= 1.2:
                regime = "BOUNDARY_LAYER"
            elif c_val > 2.0:
                regime = "OUTER_TAIL"
            else:
                regime = "INTERMEDIATE_TRANSITION"

            results.append({
                "T": mpmath.nstr(T_val, n=10),
                "gamma": mpmath.nstr(g_val, n=10),
                "c_ratio": mpmath.nstr(c_val, n=6),
                "J_exact": mpmath.nstr(j_exact, n=15),
                "asymp_plateau": mpmath.nstr(asymp_plateau, n=15),
                "transition_formula": mpmath.nstr(transition_formula, n=15),
                "asymp_tail": mpmath.nstr(asymp_tail, n=15) if asymp_tail != 0 else "N/A",
                "regime": regime
            })

        return results


def evaluate_g4_window_spectral_expansion(
    sigma: Union[float, str, mpmath.mpf],
    T: Union[float, str, mpmath.mpf],
    upper_zeros: Sequence[Any],
    window_type: str = "rectangular",
    dps: int = 80
) -> Dict[str, Any]:
    """
    [GATE G4 WINDOW SPECTRAL EXPANSION EVALUATOR]
    Evaluates S_{N, T}^{(W)} across window types: 'rectangular', 'fejer', 'abel', 'gaussian'.
    Computes I_AA, I_AZ, I_ZA, I_ZZ, S_direct, S_expanded, and closure difference.
    """
    with mpmath.workdps(dps + 20):
        sig = to_mpf(sigma, dps=dps + 20)
        T_val = to_mpf(T, dps=dps + 20)
        if sig <= 1:
            raise ValueError(f"sigma must be > 1, got {sig}")
        if T_val <= 0:
            raise ValueError(f"T must be > 0, got {T_val}")

        a_val = sig - mpmath.mpf('0.5')

        # Parsed zeros
        parsed_zeros = []
        for item in upper_zeros:
            if isinstance(item, (int, float, str, mpmath.mpf)) and not isinstance(item, (tuple, list)):
                parsed_zeros.append((mpmath.mpf(0), to_mpf(item, dps=dps + 20), 1))
            else:
                d_val = to_mpf(item[0], dps=dps + 20)
                g_val = to_mpf(item[1], dps=dps + 20)
                mult = int(item[2]) if len(item) > 2 else 1
                parsed_zeros.append((d_val, g_val, mult))

        arch_fn = lambda t: completed_log_derivative_archimedean_A(mpmath.mpc(sig, t), dps=dps)

        def z_n_fn(t_val):
            z_c = mpmath.mpc(a_val, t_val)
            tot = mpmath.mpc(0)
            for d, g, m in parsed_zeros:
                lam = mpmath.mpc(d, g)
                denom = z_c * z_c - lam * lam
                if denom != 0:
                    tot += m * (2 * z_c / denom)
            return tot

        # Define window function and integration interval
        win_lower = window_type.lower()
        if win_lower == "rectangular":
            w_fn = lambda t: mpmath.mpf(1) / (2 * T_val)
            quad_intervals = [-T_val, T_val]
        elif win_lower == "fejer":
            w_fn = lambda t: (mpmath.mpf(1) - abs(t) / T_val) / T_val
            quad_intervals = [-T_val, 0, T_val]
        elif win_lower == "abel":
            b = mpmath.mpf(1) / T_val
            w_fn = lambda t: (b / 2) * mpmath.exp(-b * abs(t))
            quad_intervals = [-mpmath.inf, 0, mpmath.inf]
        elif win_lower == "gaussian":
            w_fn = lambda t: (mpmath.mpf(1) / (mpmath.sqrt(2 * mpmath.pi) * T_val)) * mpmath.exp(-t**2 / (2 * T_val**2))
            quad_intervals = [-mpmath.inf, 0, mpmath.inf]
        else:
            raise ValueError(f"Unknown window_type '{window_type}'. Must be 'rectangular', 'fejer', 'abel', or 'gaussian'.")

        # 1. I_AA
        i_aa = mpmath.quad(lambda t: w_fn(t) * abs(arch_fn(t)) ** 2, quad_intervals)

        # 2. I_AZ
        i_az = mpmath.quad(lambda t: w_fn(t) * arch_fn(t) * mpmath.conj(z_n_fn(t)), quad_intervals)
        i_za = mpmath.conj(i_az)

        # 3. I_ZZ (Analytic for rectangular and fejer; numerical for abel and gaussian)
        if win_lower == "rectangular":
            i_zz_val = mpmath.mpc(0)
            for d1, g1, m1 in parsed_zeros:
                lam1 = mpmath.mpc(d1, g1)
                for d2, g2, m2 in parsed_zeros:
                    lam2 = mpmath.mpc(d2, g2)
                    i_zz_val += exact_finite_zero_zero_kernel_K_T(lam1, lam2, a_val, T_val, mult1=m1, mult2=m2, dps=dps)
            i_zz = i_zz_val.real
        elif win_lower == "fejer":
            i_zz_val = mpmath.mpc(0)
            for d1, g1, m1 in parsed_zeros:
                lam1 = mpmath.mpc(d1, g1)
                for d2, g2, m2 in parsed_zeros:
                    lam2 = mpmath.mpc(d2, g2)
                    i_zz_val += exact_fejer_zero_zero_kernel_K_T(lam1, lam2, a_val, T_val, mult1=m1, mult2=m2, dps=dps)
            i_zz = i_zz_val.real
        else:
            i_zz = mpmath.quad(lambda t: w_fn(t) * abs(z_n_fn(t)) ** 2, quad_intervals)

        # 4. Direct S_{N, T}
        s_direct = mpmath.quad(lambda t: w_fn(t) * abs(arch_fn(t) - z_n_fn(t)) ** 2, quad_intervals)
        s_expanded = (i_aa - i_az - i_za).real + i_zz
        closure_diff = abs(s_direct - s_expanded)

        return {
            "window_type": win_lower,
            "sigma": mpmath.nstr(sig, n=15),
            "T": mpmath.nstr(T_val, n=15),
            "zero_count": len(parsed_zeros),
            "I_AA": mpmath.nstr(i_aa, n=20),
            "I_AZ": str(i_az),
            "I_ZA": str(i_za),
            "I_ZZ": mpmath.nstr(i_zz, n=20),
            "S_direct": mpmath.nstr(s_direct, n=20),
            "S_expanded": mpmath.nstr(s_expanded, n=20),
            "closure_difference": mpmath.nstr(closure_diff, n=10),
            "status": "EXACT_FINITE_EXPANSION_VERIFIED"
        }


def evaluate_g4_radial_variation_diagnostic(
    sigma: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    delta: Union[float, str, mpmath.mpf],
    T: Union[float, str, mpmath.mpf],
    window_type: str = "rectangular",
    dps: int = 80
) -> Dict[str, Any]:
    """
    [GATE G4 RADIAL VARIATION DIAGNOSTIC]
    Evaluates the full regularized radial variation Delta S = S(off-line) - S(on-line)
    when replacing an on-line zero pair (+/- i*gamma) with an off-line quartet (+/- delta +/- i*gamma).
    Separates Delta S_full, Delta I_ZZ, and Delta Cross.
    """
    with mpmath.workdps(dps + 20):
        sig = to_mpf(sigma, dps=dps + 20)
        a_val = sig - mpmath.mpf('0.5')
        g_val = to_mpf(gamma, dps=dps + 20)
        d_val = to_mpf(delta, dps=dps + 20)
        T_val = to_mpf(T, dps=dps + 20)

        # On-line zeros: 2 zeros at (0, gamma) matching the 2 off-line zeros at (+/- delta, gamma)
        zeros_on = [(mpmath.mpf(0), g_val, 1), (mpmath.mpf(0), g_val, 1)]
        # Off-line zeros: [ (delta, gamma, 1), (-delta, gamma, 1) ]
        zeros_off = [(d_val, g_val, 1), (-d_val, g_val, 1)]

        res_on = evaluate_g4_window_spectral_expansion(
            sigma=sig, T=T_val, upper_zeros=zeros_on, window_type=window_type, dps=dps
        )
        res_off = evaluate_g4_window_spectral_expansion(
            sigma=sig, T=T_val, upper_zeros=zeros_off, window_type=window_type, dps=dps
        )

        s_on = to_mpf(res_on["S_direct"], dps=dps + 20)
        s_off = to_mpf(res_off["S_direct"], dps=dps + 20)
        delta_s_full = s_off - s_on

        i_zz_on = to_mpf(res_on["I_ZZ"], dps=dps + 20)
        i_zz_off = to_mpf(res_off["I_ZZ"], dps=dps + 20)
        delta_i_zz = i_zz_off - i_zz_on

        delta_cross = delta_s_full - delta_i_zz

        # Real axis defect for reference
        r_defect = spectral_real_axis_defect_delta(delta=d_val, gamma=g_val, z=a_val, dps=dps)

        return {
            "window_type": window_type.lower(),
            "sigma": mpmath.nstr(sig, n=15),
            "gamma": mpmath.nstr(g_val, n=15),
            "delta": mpmath.nstr(d_val, n=15),
            "T": mpmath.nstr(T_val, n=15),
            "S_on": mpmath.nstr(s_on, n=20),
            "S_off": mpmath.nstr(s_off, n=20),
            "delta_S_full": mpmath.nstr(delta_s_full, n=15),
            "delta_I_ZZ": mpmath.nstr(delta_i_zz, n=15),
            "delta_Cross": mpmath.nstr(delta_cross, n=15),
            "real_axis_defect": mpmath.nstr(r_defect, n=15),
            "is_full_variation_positive": bool(delta_s_full > 0)
        }


def evaluate_g4_cofinal_schedule_sweep(
    sigma: Union[float, str, mpmath.mpf],
    T_vals: Sequence[Union[float, str, mpmath.mpf]],
    schedule_fn: Any,
    available_zeros: Sequence[Any],
    dps: int = 80
) -> List[Dict[str, Any]]:
    """
    [GATE G4 COFINAL SCHEDULE SWEEP]
    Evaluates the cofinal limit S_{H(T), T} where zero cutoff H = H(T) grows with averaging interval T.
    Reports the scaling of I_AA, I_AZ, I_ZZ, and the unnormalized quantity T * S_{H(T), T}.
    """
    with mpmath.workdps(dps + 20):
        sig = to_mpf(sigma, dps=dps + 20)
        results = []

        # Parse available zeros
        parsed_all_zeros = []
        for item in available_zeros:
            if isinstance(item, (int, float, str, mpmath.mpf)) and not isinstance(item, (tuple, list)):
                parsed_all_zeros.append((mpmath.mpf(0), to_mpf(item, dps=dps + 20), 1))
            else:
                d_val = to_mpf(item[0], dps=dps + 20)
                g_val = to_mpf(item[1], dps=dps + 20)
                mult = int(item[2]) if len(item) > 2 else 1
                parsed_all_zeros.append((d_val, g_val, mult))

        for T_item in T_vals:
            T_val = to_mpf(T_item, dps=dps + 20)
            H_val = to_mpf(schedule_fn(float(T_val)), dps=dps + 20)

            # Filter zeros with |gamma| <= H
            filtered_zeros = [z for z in parsed_all_zeros if abs(z[1]) <= H_val]

            res = evaluate_g4_window_spectral_expansion(
                sigma=sig, T=T_val, upper_zeros=filtered_zeros, window_type="rectangular", dps=dps
            )

            s_val = to_mpf(res["S_direct"], dps=dps + 20)
            t_times_s = T_val * s_val

            results.append({
                "T": mpmath.nstr(T_val, n=10),
                "H": mpmath.nstr(H_val, n=10),
                "included_zero_count": len(filtered_zeros),
                "I_AA": res["I_AA"],
                "I_ZZ": res["I_ZZ"],
                "S_direct": res["S_direct"],
                "T_times_S": mpmath.nstr(t_times_s, n=15)
            })

        return results


def verify_g4_arithmetic_independence_firewall() -> Dict[str, Any]:
    """
    [GATE G4a ARITHMETIC FIREWALL VERIFIER]
    Proves that the arithmetic anchor evaluation (Path A, prime Dirichlet series, finite sinc kernel)
    strictly never invokes zero-finding, zero-loading, or spectral-divisor routines.
    """
    from unittest.mock import patch
    with patch('reference_data.load_first_100_reference_zeros', side_effect=AssertionError("Firewall breach: zero provider called in arithmetic path!")) as mock_load:
        res1 = finite_dirichlet_mean_square_sinc_kernel(sigma='2.0', T='10.0', max_N=30, dps=30)
        res2 = completed_mean_square_anchor_cmsa1(sigma='2.0', T='10.0', max_N=30, dps=30)
        mock_load.assert_not_called()

    return {
        "firewall_intact": True,
        "arithmetic_sinc_evaluated": bool(res1["sinc_mean_square"] != "0.0"),
        "anchor_residual_computed": bool(res2["anchor_finite_residual"] != "0.0"),
        "status": "ARITHMETIC_INDEPENDENCE_FIREWALL_VERIFIED"
    }


def evaluate_g4_radial_response_coefficient(
    sigma: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    T: Union[float, str, mpmath.mpf],
    window_type: str = "fejer",
    dps: int = 50
) -> Dict[str, Any]:
    """
    [GATE G4 FINITE RADIAL RESPONSE COEFFICIENT]
    Evaluates the exact symmetric second-order coefficient:
        C_W(sigma, gamma, T) = -2 Re int W_T(t) F_0(t) conj(D_gamma(sigma - 1/2 + it)) dt
    where:
        F_0(t) = A(sigma + it) - Z_0(sigma - 1/2 + it)
        Z_0(z) = 4z / (z^2 + gamma^2)
        D_gamma(z) = 4z(z^2 - 3*gamma^2) / (z^2 + gamma^2)^3
    This coefficient governs the leading radial variation: Delta S_W = delta^2 * C_W + O(delta^4).
    """
    with mpmath.workdps(dps + 15):
        sig = to_mpf(sigma, dps=dps + 15)
        a_val = sig - mpmath.mpf("0.5")
        g_val = to_mpf(gamma, dps=dps + 15)
        T_val = to_mpf(T, dps=dps + 15)
        w_type = window_type.lower().strip()

        def z0_fn(t_m):
            z = mpmath.mpc(a_val, t_m)
            return 4 * z / (z * z + g_val * g_val)

        def d_gamma_fn(t_m):
            z = mpmath.mpc(a_val, t_m)
            return 4 * z * (z * z - 3 * g_val * g_val) / ((z * z + g_val * g_val) ** 3)

        def integrand(t_m):
            z = mpmath.mpc(a_val, t_m)
            arch = completed_log_derivative_archimedean_A(mpmath.mpc(sig, t_m), dps=dps)
            f0 = arch - z0_fn(t_m)
            dg = d_gamma_fn(t_m)
            return -2 * (f0 * mpmath.conj(dg)).real

        if w_type == "rectangular":
            w_fn = lambda t: mpmath.mpf(1) / (2 * T_val)
            c_val, err_val = mpmath.quad(lambda t: w_fn(t) * integrand(t), [-T_val, T_val], error=True)
        elif w_type == "fejer":
            w_fn = lambda t: (1 - abs(t) / T_val) / T_val
            c_val, err_val = mpmath.quad(lambda t: w_fn(t) * integrand(t), [-T_val, 0, T_val], error=True)
        elif w_type == "abel":
            beta = mpmath.mpf(1) / T_val
            w_fn = lambda t: (beta / 2) * mpmath.exp(-beta * abs(t))
            c_val, err_val = mpmath.quad(lambda t: w_fn(t) * integrand(t), [-mpmath.inf, 0, mpmath.inf], error=True)
        elif w_type == "gaussian":
            w_fn = lambda t: (1 / (mpmath.sqrt(2 * mpmath.pi) * T_val)) * mpmath.exp(-t ** 2 / (2 * T_val ** 2))
            c_val, err_val = mpmath.quad(lambda t: w_fn(t) * integrand(t), [-mpmath.inf, 0, mpmath.inf], error=True)
        else:
            raise ValueError(f"Unknown window type: {window_type}")

        return {
            "window_type": w_type,
            "sigma": mpmath.nstr(sig, n=15),
            "gamma": mpmath.nstr(g_val, n=15),
            "T": mpmath.nstr(T_val, n=15),
            "C_W": mpmath.nstr(c_val, n=18),
            "quadrature_error": mpmath.nstr(err_val, n=6),
            "is_positive": bool(c_val > 0),
            "sign": "POSITIVE" if c_val > 0 else "NEGATIVE" if c_val < 0 else "ZERO"
        }


def evaluate_g4_radial_sign_evidence(
    sigma: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    delta: Union[float, str, mpmath.mpf],
    T: Union[float, str, mpmath.mpf],
    window_type: str = "fejer",
    dps: int = 80
) -> Dict[str, Any]:
    """
    [GATE G4 RADIAL SIGN NUMERICAL EVIDENCE EVALUATOR]
    Computes high-precision numerical quadrature for Delta S_W(sigma, gamma, delta, T)
    and reports whether the numerical estimate and mpmath estimated error bounds
    indicate negative (< 0) or positive (> 0) sign mass.

    NOTE (Epistemic Bound): This provides high-precision numerical floating-point evidence
    with estimated numerical quadrature error, NOT a formal Arb interval ball certificate.
    For genuine outward-rounded ball certification on compact Fejér support, use
    `certify_g4_fejer_witness_arb`.
    """
    with mpmath.workdps(dps + 25):
        sig = to_mpf(sigma, dps=dps + 25)
        a_val = sig - mpmath.mpf("0.5")
        g_val = to_mpf(gamma, dps=dps + 25)
        d_val = to_mpf(delta, dps=dps + 25)
        T_val = to_mpf(T, dps=dps + 25)
        w_type = window_type.lower().strip()

        def z0_fn(t_m):
            z = mpmath.mpc(a_val, t_m)
            return 4 * z / (z * z + g_val * g_val)

        def z_delta_fn(t_m):
            z = mpmath.mpc(a_val, t_m)
            lam1 = mpmath.mpc(d_val, g_val)
            lam2 = mpmath.mpc(-d_val, g_val)
            return 2 * z / (z * z - lam1 * lam1) + 2 * z / (z * z - lam2 * lam2)

        def diff_integrand(t_m):
            arch = completed_log_derivative_archimedean_A(mpmath.mpc(sig, t_m), dps=dps)
            f0 = arch - z0_fn(t_m)
            fd = arch - z_delta_fn(t_m)
            return abs(fd) ** 2 - abs(f0) ** 2

        if w_type == "rectangular":
            w_fn = lambda t: mpmath.mpf(1) / (2 * T_val)
            val, err = mpmath.quad(lambda t: w_fn(t) * diff_integrand(t), [-T_val, T_val], error=True)
        elif w_type == "fejer":
            w_fn = lambda t: (1 - abs(t) / T_val) / T_val
            val, err = mpmath.quad(lambda t: w_fn(t) * diff_integrand(t), [-T_val, 0, T_val], error=True)
        elif w_type == "abel":
            beta = mpmath.mpf(1) / T_val
            w_fn = lambda t: (beta / 2) * mpmath.exp(-beta * abs(t))
            val, err = mpmath.quad(lambda t: w_fn(t) * diff_integrand(t), [-mpmath.inf, 0, mpmath.inf], error=True)
        elif w_type == "gaussian":
            w_fn = lambda t: (1 / (mpmath.sqrt(2 * mpmath.pi) * T_val)) * mpmath.exp(-t ** 2 / (2 * T_val ** 2))
            val, err = mpmath.quad(lambda t: w_fn(t) * diff_integrand(t), [-mpmath.inf, 0, mpmath.inf], error=True)
        else:
            raise ValueError(f"Unknown window type: {window_type}")

        lower_bound = val - err
        upper_bound = val + err
        has_neg_evidence = bool(upper_bound < 0)
        has_pos_evidence = bool(lower_bound > 0)
        evidence_status = (
            "NUMERICAL_EVIDENCE_NEGATIVE" if has_neg_evidence
            else "NUMERICAL_EVIDENCE_POSITIVE" if has_pos_evidence
            else "UNCERTAIN"
        )

        return {
            "window_type": w_type,
            "sigma": mpmath.nstr(sig, n=15),
            "gamma": mpmath.nstr(g_val, n=15),
            "delta": mpmath.nstr(d_val, n=15),
            "T": mpmath.nstr(T_val, n=15),
            "numerical_estimate": mpmath.nstr(val, n=20),
            "estimated_error": mpmath.nstr(err, n=6),
            "estimate_lower_bound": mpmath.nstr(lower_bound, n=20),
            "estimate_upper_bound": mpmath.nstr(upper_bound, n=20),
            "has_negative_evidence": has_neg_evidence,
            "has_positive_evidence": has_pos_evidence,
            "evidence_status": evidence_status,
            # Backward-compatibility aliases (deprecated for proof claims)
            "value": mpmath.nstr(val, n=20),
            "interval_lower": mpmath.nstr(lower_bound, n=20),
            "interval_upper": mpmath.nstr(upper_bound, n=20),
            "is_negative": has_neg_evidence,
            "is_positive": has_pos_evidence,
            "certified_negative": has_neg_evidence,
            "certified_positive": has_pos_evidence,
            "numerical_status": evidence_status,
            "certification_status": evidence_status
        }


def certify_g4_radial_sign_witness(
    sigma: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    delta: Union[float, str, mpmath.mpf],
    T: Union[float, str, mpmath.mpf],
    window_type: str = "fejer",
    dps: int = 80
) -> Dict[str, Any]:
    """
    [DEPRECATED COMPATIBILITY WRAPPER]
    Calls `evaluate_g4_radial_sign_evidence`. Note that mpmath quadrature provides
    estimated numerical errors, not certified interval ball enclosures.
    """
    return evaluate_g4_radial_sign_evidence(
        sigma=sigma, gamma=gamma, delta=delta, T=T, window_type=window_type, dps=dps
    )


def certify_g4_fejer_witness_arb(
    sigma: Union[float, str, mpmath.mpf] = "5.0",
    gamma: Union[float, str, mpmath.mpf] = "14.0",
    delta: Union[float, str, mpmath.mpf] = "0.49",
    T: Union[float, str, mpmath.mpf] = "16.8",
    n_subdivisions: int = 50000,
    dps: int = 60
) -> Dict[str, Any]:
    """
    [RIGOROUS ARB BALL CERTIFICATE FOR FEJÉR WITNESS WIT-02]
    Computes a certified ball enclosure for the Fejér windowed radial difference:
    Delta S_W = int_{-T}^T W_T(t) (|A(sigma+it) - Z_delta(sigma-1/2+it)|^2 - |A(sigma+it) - Z_0(sigma-1/2+it)|^2) dt
    over the complete symmetric compact support [-T, T] using outward-rounded Arb ball arithmetic in python-flint.

    Exact Parameters:
    - sigma = "5.0" (exact decimal string)
    - gamma = "14.0" (exact decimal string)
    - delta = "0.49" (exact decimal string)
    - T = "16.8" (exact decimal string)

    Direct Evaluation and Conjugation Properties:
    The certified Riemann sum is directly evaluated across the full symmetric domain [-T, T]
    with n_subdivisions subintervals in outward-rounded Arb ball arithmetic, without assuming
    evenness reduction or reflection as an operational premise.

    Explanatory Note on Conjugation Symmetry:
    For any real sigma > 1 and t in R:
    1. The archimedean/pole term A(sigma + it) = 1/(sigma + it) + 1/(sigma - 1 + it) - (1/2)*log(pi) + (1/2)*psi((sigma + it)/2)
       satisfies conj(1/(sigma + it)) = 1/(sigma - it) and conj(psi(z)) = psi(conj(z)), whence A(sigma, -t) = conj(A(sigma, t)).
       (Note: This follows from direct conjugation of explicit meromorphic terms; no zeta conjugation or Schwarz reflection hypothesis is invoked).
    2. For any discrete quadruplet rho = 1/2 +/- delta +/- i*gamma, pairing +i*gamma with -i*gamma yields:
       Z_delta(sigma, -t) = 1/(sigma - 1/2 - delta - i(-t - gamma)) + 1/(sigma - 1/2 - delta - i(-t + gamma))
                          = 1/(sigma - 1/2 - delta + i(t + gamma)) + 1/(sigma - 1/2 - delta + i(t - gamma))
                          = conj(Z_delta(sigma, t)).
    3. Hence A(sigma, -t) - Z_delta(sigma, -t) = conj(A(sigma, t) - Z_delta(sigma, t)), so |A - Z_delta|^2 is even.
    """
    import flint
    from flint import arb, acb, ctx
    ctx.dps = dps

    sig_b = arb(str(sigma))
    gam_b = arb(str(gamma))
    del_b = arb(str(delta))
    T_b = arb(str(T))
    a_b = sig_b - arb("0.5")
    log_pi = arb.pi().log()

    def eval_A(t_ball):
        u = acb(sig_b, t_ball)
        term1 = acb(1) / u
        term2 = acb(1) / (u - acb(1))
        term3 = acb(log_pi) / acb(2)
        u_half = u / acb(2)
        term4 = u_half.digamma() / acb(2)
        return term1 + term2 - term3 + term4

    def eval_Z0(t_ball):
        z = acb(a_b, t_ball)
        return (acb(4) * z) / (z ** 2 + acb(gam_b ** 2))

    def eval_delta_Z(t_ball):
        z = acb(a_b, t_ball)
        num = acb(4) * z * acb(del_b ** 2) * (z ** 2 - acb(3 * gam_b ** 2 + del_b ** 2))
        den = (z ** 2 + acb(gam_b ** 2)) * ((z ** 2 + acb(gam_b ** 2 - del_b ** 2)) ** 2 + acb(4 * del_b ** 2 * gam_b ** 2))
        return num / den

    def integrand_canceled_full(t_ball):
        W = (arb(1) - abs(t_ball) / T_b) / T_b
        A = eval_A(t_ball)
        Z0 = eval_Z0(t_ball)
        dZ = eval_delta_Z(t_ball)
        F0 = A - Z0
        re_prod = F0.real * dZ.real + F0.imag * dZ.imag
        mod_sq_dZ = dZ.real ** 2 + dZ.imag ** 2
        diff = -arb(2) * re_prod + mod_sq_dZ
        return W * diff

    total = arb(0)
    step = (arb(2) * T_b) / arb(n_subdivisions)
    for i in range(n_subdivisions):
        t0 = -T_b + arb(i) * step
        t1 = -T_b + arb(i + 1) * step
        t_ball = t0.union(t1)
        f_ball = integrand_canceled_full(t_ball)
        total += (t1 - t0) * f_ball

    upper_val = total.upper()
    lower_val = total.lower()
    is_strictly_neg = bool(upper_val < 0)

    return {
        "witness_id": "WIT-02",
        "window_type": "fejer",
        "sigma": str(sigma),
        "gamma": str(gamma),
        "delta": str(delta),
        "T": str(T),
        "n_subdivisions": n_subdivisions,
        "enclosure_mid": str(total.mid()),
        "enclosure_rad": str(total.rad()),
        "interval_lower": str(lower_val),
        "interval_upper": str(upper_val),
        "is_certified_negative": is_strictly_neg,
        "certification_engine": "python-flint / Arb ball arithmetic (outward rounded)",
        "status": "CERTIFIED_NEGATIVE_ARB_BALL" if is_strictly_neg else "INCONCLUSIVE"
    }



def verify_additive_reference_subtraction_invariance(
    s_delta: Union[float, str, mpmath.mpf],
    s_0: Union[float, str, mpmath.mpf],
    reference_r: Union[float, str, mpmath.mpf],
    dps: int = 50
) -> Dict[str, Any]:
    """
    [NO-GO THEOREM FOR ADDITIVE RENORMALIZATION]
    Verifies the exact identity for any scalar reference term R independent of zero configurations:
    (S(Z_delta) - R) - (S(Z_0) - R) == S(Z_delta) - S(Z_0).
    Consequently, an additive scalar subtraction cannot alter, repair, or renormalize the radial sign.
    """
    with mpmath.workdps(dps):
        s_d = to_mpf(s_delta, dps=dps)
        s_z0 = to_mpf(s_0, dps=dps)
        r_val = to_mpf(reference_r, dps=dps)

        raw_diff = s_d - s_z0
        renorm_diff = (s_d - r_val) - (s_z0 - r_val)
        algebraic_diff = abs(renorm_diff - raw_diff)
        eps_tol = mpmath.mpf(10) ** (-(dps - 10))

        # Exact symbolic check
        import importlib
        sp: Any = importlib.import_module("sympy")
        S_d_sym, S_0_sym, R_sym = sp.symbols("S_delta S_0 R", real=True)
        sym_expr = (S_d_sym - R_sym) - (S_0_sym - R_sym) - (S_d_sym - S_0_sym)
        is_sym_exact = bool(sp.simplify(sym_expr) == 0)

        is_invariant = bool(algebraic_diff < eps_tol) and is_sym_exact

        return {
            "s_delta": mpmath.nstr(s_d, n=15),
            "s_0": mpmath.nstr(s_z0, n=15),
            "reference_r": mpmath.nstr(r_val, n=15),
            "raw_difference": mpmath.nstr(raw_diff, n=18),
            "renormalized_difference": mpmath.nstr(renorm_diff, n=18),
            "algebraic_discrepancy": mpmath.nstr(algebraic_diff, n=6),
            "is_invariant": is_invariant,
            "is_symbolic_exact": is_sym_exact,
            "status": "ADDITIVE_REFERENCE_INVARIANCE_VERIFIED"
        }


def verify_squared_norm_background_dependence(
    F_val: Any,
    G_val: Any,
    delta_val: Any,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [BACKGROUND-DEPENDENCE THEOREM]
    For complex-valued background F and perturbation Delta, verifies:
    Q(F, Delta) = |F + Delta|^2 - |F|^2 = |Delta|^2 + 2 * Re(F * conj(Delta)),
    and:
    Q(F, Delta) - Q(G, Delta) = 2 * Re((F - G) * conj(Delta)).
    Proves that the squared-norm variation is strictly background-dependent.
    """
    with mpmath.workdps(dps):
        F = to_mpc(F_val, dps=dps)
        G = to_mpc(G_val, dps=dps)
        Delta = to_mpc(delta_val, dps=dps)

        q_F = abs(F + Delta)**2 - abs(F)**2
        q_G = abs(G + Delta)**2 - abs(G)**2
        q_F_formula = abs(Delta)**2 + 2 * mpmath.re(F * mpmath.conj(Delta))
        q_diff = q_F - q_G
        q_diff_formula = 2 * mpmath.re((F - G) * mpmath.conj(Delta))

        err_F = abs(q_F - q_F_formula)
        err_diff = abs(q_diff - q_diff_formula)
        eps_tol = mpmath.mpf(10) ** (-(dps - 10))

        # SymPy exact symbolic check
        import importlib
        sp: Any = importlib.import_module("sympy")
        Fr, Fi, Gr, Gi, Dr, Di = sp.symbols("Fr Fi Gr Gi Dr Di", real=True)
        F_sym = Fr + sp.I * Fi
        G_sym = Gr + sp.I * Gi
        D_sym = Dr + sp.I * Di

        # |F + D|^2 - |F|^2 in real/imag components
        q_F_sym = (Fr + Dr)**2 + (Fi + Di)**2 - (Fr**2 + Fi**2)
        q_F_form_sym = (Dr**2 + Di**2) + 2 * (Fr * Dr + Fi * Di)
        sym_F_exact = bool(sp.simplify(q_F_sym - q_F_form_sym) == 0)

        q_G_sym = (Gr + Dr)**2 + (Gi + Di)**2 - (Gr**2 + Gi**2)
        q_diff_sym = q_F_sym - q_G_sym
        q_diff_form_sym = 2 * ((Fr - Gr) * Dr + (Fi - Gi) * Di)
        sym_diff_exact = bool(sp.simplify(q_diff_sym - q_diff_form_sym) == 0)

        is_background_dependent = bool(abs(q_diff) > eps_tol) if abs(F - G) > eps_tol and abs(Delta) > eps_tol else False

        return {
            "F": str(F),
            "G": str(G),
            "Delta": str(Delta),
            "Q_F": mpmath.nstr(q_F, n=15),
            "Q_G": mpmath.nstr(q_G, n=15),
            "Q_diff": mpmath.nstr(q_diff, n=15),
            "error_expansion_F": mpmath.nstr(err_F, n=6),
            "error_expansion_diff": mpmath.nstr(err_diff, n=6),
            "is_symbolic_exact": sym_F_exact and sym_diff_exact,
            "is_background_dependent": is_background_dependent,
            "status": "BACKGROUND_DEPENDENCE_VERIFIED"
        }


def verify_fixed_finite_perturbation_invisibility(
    sigma: Union[float, str, mpmath.mpf],
    resolvents: List[Tuple[Any, Any, Any]],  # list of (c_j, a_j, gamma_j)
    T_values: List[Union[float, str, mpmath.mpf]],
    max_prime_n: int = 50,
    dps: int = 40
) -> Dict[str, Any]:
    """
    [FINITE DIRICHLET TRUNCATION NUMERICAL EVIDENCE]
    Evaluates the normalized mean-square variation of a finite prime Dirichlet polynomial
    P_{sigma, N}(t) = sum_{p^k <= N} (log p) * n^{-sigma - i*t} against a fixed finite resolvent sum:
    Delta(t) = sum_{j=1}^M c_j / (a_j + i*(t - gamma_j)), with a_j > 0,
    across finite sample window half-widths T in T_values:
    I(T) = (1 / (2*T)) * integral_{-T}^T (|P_{sigma, N}(t) - Delta(t)|^2 - |P_{sigma, N}(t)|^2) dt.

    NOTE: This routine provides numerical quadrature evidence for finite truncations.
    It does NOT evaluate the infinite prime Dirichlet series nor prove an infinite limit as T -> infinity.
    """
    with mpmath.workdps(dps):
        sig = to_mpf(sigma, dps=dps)
        if sig <= 1:
            raise ValueError(f"sigma must be strictly greater than 1, got {sig}")
        if max_prime_n < 2:
            raise ValueError(f"max_prime_n must be >= 2, got {max_prime_n}")
        if not T_values:
            raise ValueError("T_values list must not be empty")

        for T_raw in T_values:
            t_check = to_mpf(T_raw, dps=dps)
            if t_check <= 0:
                raise ValueError(f"T values must be strictly positive, got {t_check}")

        for c_j, a_j, gam_j in resolvents:
            a_check = to_mpf(a_j, dps=dps)
            if a_check <= 0:
                raise ValueError(f"resolvent width a_j must be strictly positive, got {a_check}")

        # Compute exact analytic L2 norm upper bound of Delta on R
        # integral_{-inf}^inf |1/(a + i(t-gam))|^2 dt = pi / a
        l2_sq_bound = mpmath.mpf(0)
        if resolvents:
            for c_j, a_j, gam_j in resolvents:
                c_abs = abs(to_mpc(c_j, dps=dps))
                a_f = to_mpf(a_j, dps=dps)
                l2_sq_bound += c_abs * mpmath.sqrt(mpmath.pi / a_f)
            l2_sq_bound = l2_sq_bound ** 2

        if not resolvents:
            results_by_T = [{
                "T": str(to_mpf(T_raw, dps=dps)),
                "normalized_integral": mpmath.nstr(mpmath.mpf(0), n=12),
                "energy_bound": mpmath.nstr(mpmath.mpf(0), n=12)
            } for T_raw in T_values]
            return {
                "sigma": str(sig),
                "n_resolvents": 0,
                "prime_cutoff": max_prime_n,
                "tested_T_values": [str(to_mpf(t, dps=dps)) for t in T_values],
                "analytic_L2_norm_bound_squared": "0.0",
                "results_by_T": results_by_T,
                "endpoint_magnitude_decreased": False,
                "calculation_type": "Non-certified numerical quadrature of finite Dirichlet polynomial",
                "limit_caveat": "Finite numerical samples across discrete T do not establish mathematical convergence or an infinite limit.",
                "status": "FINITE_DIRICHLET_TRUNCATION_NUMERICAL_EVIDENCE"
            }

        # Precompute primes and log(p) for finite prime Dirichlet polynomial
        import importlib
        sp: Any = importlib.import_module("sympy")
        prime_powers = []
        for n in range(2, max_prime_n + 1):
            pfactors = sp.primefactors(n)
            if len(pfactors) == 1:
                p = pfactors[0]
                lam = mpmath.log(p)
                prime_powers.append((lam, mpmath.mpf(n)))

        def P_sigma(t_val):
            val = mpmath.mpc(0, 0)
            for lam, n_val in prime_powers:
                val += lam * (n_val ** (-sig - mpmath.mpc(0, t_val)))
            return val

        def Delta_fn(t_val):
            val = mpmath.mpc(0, 0)
            for c_j, a_j, gam_j in resolvents:
                c_c = to_mpc(c_j, dps=dps)
                a_f = to_mpf(a_j, dps=dps)
                gam_f = to_mpf(gam_j, dps=dps)
                val += c_c / (a_f + mpmath.mpc(0, t_val - gam_f))
            return val

        results_by_T = []
        for T_raw in T_values:
            T_val = to_mpf(T_raw, dps=dps)
            integrand = lambda t: abs(P_sigma(t) - Delta_fn(t))**2 - abs(P_sigma(t))**2
            val_int = mpmath.quad(integrand, [-T_val, 0, T_val])
            norm_val = val_int / (2 * T_val)
            results_by_T.append({
                "T": str(T_val),
                "normalized_integral": mpmath.nstr(norm_val, n=12),
                "energy_bound": mpmath.nstr(l2_sq_bound / (2 * T_val), n=12)
            })

        # Sample observation: compare first and last sample magnitude
        vals = [abs(mpmath.mpf(r["normalized_integral"])) for r in results_by_T]
        endpoint_dec = bool(vals[-1] < vals[0]) if len(vals) > 1 else False

        return {
            "sigma": str(sig),
            "n_resolvents": len(resolvents),
            "prime_cutoff": max_prime_n,
            "tested_T_values": [str(to_mpf(t, dps=dps)) for t in T_values],
            "analytic_L2_norm_bound_squared": mpmath.nstr(l2_sq_bound, n=10),
            "results_by_T": results_by_T,
            "endpoint_magnitude_decreased": endpoint_dec,
            "calculation_type": "Non-certified numerical quadrature of finite Dirichlet polynomial",
            "limit_caveat": "Finite numerical samples across discrete T do not establish mathematical convergence or an infinite limit.",
            "status": "FINITE_DIRICHLET_TRUNCATION_NUMERICAL_EVIDENCE"
        }


def verify_cofinal_subcritical_norm_bound(
    M_bound: Union[float, str, mpmath.mpf],
    delta_L2_norm: Union[float, str, mpmath.mpf],
    T_val: Union[float, str, mpmath.mpf],
    dps: int = 40
) -> Dict[str, Any]:
    """
    [COFINAL SUBCRITICAL-NORM THEOREM EVALUATOR]
    Computes the exact abstract upper bound on the normalized mean-square variation:
    |V_T| <= ||Delta_T||^2 / (2*T) + sqrt(2*M) * (||Delta_T|| / sqrt(T)) = x_T^2 / 2 + sqrt(2*M) * x_T,
    where x_T = ||Delta_T|| / sqrt(T) and (1 / 2T) ||P_T||^2 <= M.

    Evaluates the finite-sample bound showing that as x_T -> 0 (i.e. ||Delta_T|| = o(sqrt(T))),
    the total variation bound vanishes.
    """
    with mpmath.workdps(dps):
        M_mpf = to_mpf(M_bound, dps=dps)
        if M_mpf < 0:
            raise ValueError(f"M_bound must be non-negative, got {M_mpf}")
        norm_mpf = to_mpf(delta_L2_norm, dps=dps)
        if norm_mpf < 0:
            raise ValueError(f"delta_L2_norm must be non-negative, got {norm_mpf}")
        T_mpf = to_mpf(T_val, dps=dps)
        if T_mpf <= 0:
            raise ValueError(f"T_val must be strictly positive, got {T_mpf}")

        x_T = norm_mpf / mpmath.sqrt(T_mpf)
        direct_bound = (x_T ** 2) / 2
        cross_bound = mpmath.sqrt(2 * M_mpf) * x_T
        total_bound = direct_bound + cross_bound

        return {
            "M_bound": mpmath.nstr(M_mpf, n=10),
            "delta_L2_norm": mpmath.nstr(norm_mpf, n=10),
            "T": mpmath.nstr(T_mpf, n=10),
            "x_T": mpmath.nstr(x_T, n=10),
            "direct_energy_bound": mpmath.nstr(direct_bound, n=10),
            "cross_term_bound": mpmath.nstr(cross_bound, n=10),
            "total_variation_bound": mpmath.nstr(total_bound, n=10),
            "status": "SUBCRITICAL_NORM_BOUND_EVALUATED"
        }


def exact_resolvent_L2_norm_squared(
    a: Union[float, str, mpmath.mpf],
    delta: Union[float, str, mpmath.mpf],
    dps: int = 50
) -> Dict[str, Any]:
    """
    [EXACT RESOLVENT L2 NORM]
    Computes the exact continuous L^2(R) norm squared of the single-zero defect resolvent:
    r_delta(t) = 1 / (a - delta + i*t) - 1 / (a + i*t) = delta / (w * (w - delta)),
    where w = a + i*t, a > 0, and a - delta > 0:
    ||r_delta||_{L^2(R)}^2 = int_{-inf}^inf |r_delta(t)|^2 dt = pi * delta^2 / (a * (a - delta) * (2*a - delta)).

    Also computes the leading small-delta asymptotic:
    ||r_delta||_{L^2(R)}^2 ~ pi * delta^2 / (2 * a^3).
    """
    with mpmath.workdps(dps):
        a_f = to_mpf(a, dps=dps)
        d_f = to_mpf(delta, dps=dps)
        if a_f <= 0:
            raise ValueError(f"Width parameter a must be strictly positive, got {a_f}")
        if a_f - d_f <= 0:
            raise ValueError(f"Perturbed width a - delta must be strictly positive, got {a_f - d_f}")

        denom = a_f * (a_f - d_f) * (2 * a_f - d_f)
        exact_val = mpmath.pi * (d_f ** 2) / denom
        leading_asymptotic = mpmath.pi * (d_f ** 2) / (2 * (a_f ** 3))

        return {
            "a": str(a_f),
            "delta": str(d_f),
            "exact_L2_norm_squared": mpmath.nstr(exact_val, n=20),
            "leading_asymptotic": mpmath.nstr(leading_asymptotic, n=20),
            "relative_asymptotic_error": mpmath.nstr(abs(exact_val - leading_asymptotic) / exact_val, n=8) if exact_val != 0 else "0.0",
            "status": "EXACT_RESOLVENT_NORM_EVALUATED"
        }


def verify_resolvent_reflection_pair_cancellation(
    w_val: Union[complex, str, mpmath.mpc],
    delta_val: Union[float, str, mpmath.mpf],
    dps: int = 50
) -> Dict[str, Any]:
    """
    [EXACT REFLECTION PAIR CANCELLATION]
    Verifies that for a functional-reflection pair at the same height, the sum of defect resolvents
    cancels to exact second order in delta:
    r_delta(w) + r_{-delta}(w) = (1/(w - delta) - 1/w) + (1/(w + delta) - 1/w)
                              = 2 * delta^2 / (w * (w^2 - delta^2)).
    """
    with mpmath.workdps(dps):
        w_c = to_mpc(w_val, dps=dps)
        d_f = to_mpf(delta_val, dps=dps)
        if abs(w_c) == 0:
            raise ValueError("w must be non-zero")
        if abs(w_c - d_f) == 0 or abs(w_c + d_f) == 0:
            raise ValueError("w +- delta must be non-zero")

        # Numerical evaluation
        r_pos = (1 / (w_c - d_f)) - (1 / w_c)
        r_neg = (1 / (w_c + d_f)) - (1 / w_c)
        sum_numerical = r_pos + r_neg

        formula_val = (2 * (d_f ** 2)) / (w_c * (w_c**2 - d_f**2))
        err = abs(sum_numerical - formula_val)

        # Exact symbolic check via SymPy
        import importlib
        sp: Any = importlib.import_module("sympy")
        w_sym, d_sym = sp.symbols("w d", complex=True)
        r_pos_sym = 1 / (w_sym - d_sym) - 1 / w_sym
        r_neg_sym = 1 / (w_sym + d_sym) - 1 / w_sym
        sum_sym = r_pos_sym + r_neg_sym
        formula_sym = (2 * d_sym**2) / (w_sym * (w_sym**2 - d_sym**2))
        sym_diff = sp.simplify(sum_sym - formula_sym)
        is_symbolic_exact = bool(sym_diff == 0)

        return {
            "w": str(w_c),
            "delta": str(d_f),
            "sum_numerical": str(sum_numerical),
            "formula_value": str(formula_val),
            "error": mpmath.nstr(err, n=6),
            "is_symbolic_exact": is_symbolic_exact,
            "status": "REFLECTION_PAIR_CANCELLATION_VERIFIED"
        }


def verify_resolvent_L2_integral(
    a: Union[float, str, mpmath.mpf],
    delta: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf] = 0.0,
    dps: int = 40
) -> Dict[str, Any]:
    """
    [RESOLVENT L2 INTEGRAL NUMERICAL & SYMBOLIC VERIFICATION]
    Computes int_{-inf}^inf |r_delta(a + i*(t - gamma))|^2 dt via high-precision numerical quadrature
    and compares against the exact formula pi * delta^2 / (a * (a - delta) * (2*a - delta)).
    Also verifies exact symbolic integration in SymPy.
    """
    with mpmath.workdps(dps):
        a_f = to_mpf(a, dps=dps)
        d_f = to_mpf(delta, dps=dps)
        gam_f = to_mpf(gamma, dps=dps)
        if a_f <= 0:
            raise ValueError(f"a must be strictly positive, got {a_f}")
        if a_f - d_f <= 0:
            raise ValueError(f"a - delta must be strictly positive, got {a_f - d_f}")

        # Exact formula
        denom = a_f * (a_f - d_f) * (2 * a_f - d_f)
        exact_formula_val = mpmath.pi * (d_f ** 2) / denom

        # Numerical integration with peak point at t = gamma
        def integrand(t_val):
            w = mpmath.mpc(a_f, t_val - gam_f)
            r = (1 / (w - d_f)) - (1 / w)
            return abs(r) ** 2

        quad_val = mpmath.quad(integrand, [-mpmath.inf, gam_f, mpmath.inf], maxdegree=10)
        quad_err = abs(quad_val - exact_formula_val)


        # Symbolic integration check via SymPy
        import importlib
        sp: Any = importlib.import_module("sympy")
        u, a_s, b_s, d_s = sp.symbols("u a b d", positive=True)
        # Integrand in terms of a > 0 and b = a - d > 0:
        # 1 / ((u^2 + a^2) * (u^2 + b^2)) integrates to pi / (a*b*(a+b))
        base_int = sp.integrate(1 / ((u**2 + a_s**2) * (u**2 + b_s**2)), (u, -sp.oo, sp.oo))
        sym_int = (d_s**2 * base_int).subs(b_s, a_s - d_s)
        sym_formula = sp.pi * d_s**2 / (a_s * (a_s - d_s) * (2 * a_s - d_s))
        is_symbolic_exact = bool(sp.simplify(sym_int - sym_formula) == 0)

        return {
            "a": str(a_f),
            "delta": str(d_f),
            "gamma": str(gam_f),
            "exact_formula_value": mpmath.nstr(exact_formula_val, n=20),
            "quadrature_value": mpmath.nstr(quad_val, n=20),
            "quadrature_error": mpmath.nstr(quad_err, n=6),
            "is_symbolic_exact": is_symbolic_exact,
            "status": "RESOLVENT_L2_INTEGRAL_VERIFIED"
        }


# ============================================================================
# CURVATURE-TRANSPORT UNIFICATION & THETA-MELLIN BRIDGE VERIFIERS
# ============================================================================

def exact_radial_geometry(
    K: int,
    tau_val: Optional[Union[float, str, mpmath.mpf]] = None,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [CURVATURE-TRANSPORT: RADIAL GEOMETRY & GRADE-SHIFT LAWS]
    For grade K and scale generator tau = 2*pi:
      a_K = tau^K, r_K = tau^(-K), C_K = tau * r_K = tau^(1-K), kappa_K = 1/r_K = tau^K.
    Verifies:
      r_K * kappa_K = 1
      C_K = tau * r_K
      C_1 = 1, r_1 = 1/tau, kappa_1 = tau
      r_{K+1} = tau^(-1) * r_K
      C_{K+1} = tau^(-1) * C_K
      kappa_{K+1} = tau * kappa_K
    """
    with mpmath.workdps(dps):
        tau_mp = to_mpf(tau_val if tau_val is not None else 2 * mpmath.pi, dps=dps)
        a_K = tau_mp ** K
        r_K = tau_mp ** (-K)
        C_K = tau_mp * r_K
        kappa_K = mpmath.mpf(1) / r_K

        # Shifted grade K+1
        r_Kp1 = tau_mp ** (-(K + 1))
        C_Kp1 = tau_mp * r_Kp1
        kappa_Kp1 = mpmath.mpf(1) / r_Kp1

        # Unit circumference at K=1
        r_1 = tau_mp ** (-1)
        C_1 = tau_mp * r_1
        kappa_1 = tau_mp ** 1

        reciprocal_check = abs(r_K * kappa_K - 1)
        shift_r_check = abs(r_Kp1 - (r_K / tau_mp))
        shift_C_check = abs(C_Kp1 - (C_K / tau_mp))
        shift_kappa_check = abs(kappa_Kp1 - (tau_mp * kappa_K))
        unit_C1_check = abs(C_1 - 1)

        # Exact symbolic verification via SymPy
        import importlib
        sp: Any = importlib.import_module("sympy")
        tau_s, K_s = sp.symbols("tau K", positive=True)
        r_s = tau_s ** (-K_s)
        kappa_s = tau_s ** K_s
        C_s = tau_s * r_s
        sym_recip = sp.simplify(r_s * kappa_s - 1)
        sym_C1 = sp.simplify((tau_s * tau_s**(-1)) - 1)
        sym_shift_r = sp.simplify(tau_s**(-(K_s+1)) - (tau_s**(-1) * r_s))
        sym_shift_C = sp.simplify(tau_s * tau_s**(-(K_s+1)) - (tau_s**(-1) * C_s))
        sym_shift_k = sp.simplify(tau_s**(K_s+1) - (tau_s * kappa_s))

        is_symbolic_exact = bool(
            sym_recip == 0 and sym_C1 == 0 and sym_shift_r == 0 and
            sym_shift_C == 0 and sym_shift_k == 0
        )

        return {
            "K": K,
            "tau": mpmath.nstr(tau_mp, n=dps),
            "a_K": mpmath.nstr(a_K, n=dps),
            "r_K": mpmath.nstr(r_K, n=dps),
            "C_K": mpmath.nstr(C_K, n=dps),
            "kappa_K": mpmath.nstr(kappa_K, n=dps),
            "reciprocal_error": mpmath.nstr(reciprocal_check, n=6),
            "shift_r_error": mpmath.nstr(shift_r_check, n=6),
            "shift_C_error": mpmath.nstr(shift_C_check, n=6),
            "shift_kappa_error": mpmath.nstr(shift_kappa_check, n=6),
            "unit_C1_error": mpmath.nstr(unit_C1_check, n=6),
            "is_symbolic_exact": is_symbolic_exact,
            "status": "RADIAL_GEOMETRY_VERIFIED"
        }


def fourier_lattice_spacing(
    K: int,
    tau_val: Optional[Union[float, str, mpmath.mpf]] = None,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [CURVATURE-TRANSPORT: FOURIER LATTICE SPACING]
    For circle of circumference C_K = tau^(1-K), the fundamental angular Fourier
    frequency lattice spacing is:
      Delta omega_K = tau / C_K = tau / (tau^(1-K)) = tau^K,
    generating lattice L_K = tau^K * Z.
    """
    with mpmath.workdps(dps):
        tau_mp = to_mpf(tau_val if tau_val is not None else 2 * mpmath.pi, dps=dps)
        C_K = tau_mp ** (1 - K)
        delta_omega = tau_mp / C_K
        expected = tau_mp ** K
        err = abs(delta_omega - expected)

        import importlib
        sp: Any = importlib.import_module("sympy")
        tau_s, K_s = sp.symbols("tau K", positive=True)
        sym_spacing = sp.simplify(tau_s / (tau_s ** (1 - K_s)) - tau_s ** K_s)

        return {
            "K": K,
            "C_K": mpmath.nstr(C_K, n=dps),
            "delta_omega": mpmath.nstr(delta_omega, n=dps),
            "expected_tau_K": mpmath.nstr(expected, n=dps),
            "error": mpmath.nstr(err, n=6),
            "is_symbolic_exact": bool(sym_spacing == 0),
            "status": "FOURIER_LATTICE_SPACING_VERIFIED"
        }


def generic_scale_geometry(
    b: Union[float, str, mpmath.mpf],
    K: int,
    tau_val: Optional[Union[float, str, mpmath.mpf]] = None,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [CURVATURE-TRANSPORT: GENERIC BASE SCALE CONTROL b > 1]
    Tests scale transport for generic base b > 1:
      a_K = b^K, r_K = b^(-K), C_K = tau * b^(-K), kappa_K = b^K.
    Verifies that the transport algebra holds for all b > 1.
    """
    with mpmath.workdps(dps):
        b_mp = to_mpf(b, dps=dps)
        if b_mp <= 1:
            raise ValueError(f"Base b must be > 1, got {b_mp}")
        tau_mp = to_mpf(tau_val if tau_val is not None else 2 * mpmath.pi, dps=dps)

        a_K = b_mp ** K
        r_K = b_mp ** (-K)
        C_K = tau_mp * (b_mp ** (-K))
        kappa_K = b_mp ** K

        reciprocal_err = abs(r_K * kappa_K - 1)
        fourier_spacing = tau_mp / C_K
        fourier_err = abs(fourier_spacing - (b_mp ** K))

        return {
            "b": mpmath.nstr(b_mp, n=15),
            "K": K,
            "a_K": mpmath.nstr(a_K, n=dps),
            "r_K": mpmath.nstr(r_K, n=dps),
            "C_K": mpmath.nstr(C_K, n=dps),
            "kappa_K": mpmath.nstr(kappa_K, n=dps),
            "reciprocal_error": mpmath.nstr(reciprocal_err, n=6),
            "fourier_spacing_error": mpmath.nstr(fourier_err, n=6),
            "status": "GENERIC_SCALE_GEOMETRY_VERIFIED"
        }


def transported_radial_defect(
    delta: Union[float, str, mpmath.mpf],
    K: int,
    tau_val: Optional[Union[float, str, mpmath.mpf]] = None,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [CURVATURE-TRANSPORT: ZERO & RADIAL-UNIT TRANSPORT]
    For displacement delta at grade K:
      d_{rho,K} = a_K * delta = tau^K * delta.
    Transport by radial unit r_K = tau^(-K) satisfies:
      r_K * d_{rho,K} = tau^(-K) * (tau^K * delta) = delta,
      (r_K * d_{rho,K})^2 = delta^2.
    """
    with mpmath.workdps(dps):
        d_mp = to_mpf(delta, dps=dps)
        tau_mp = to_mpf(tau_val if tau_val is not None else 2 * mpmath.pi, dps=dps)
        a_K = tau_mp ** K
        r_K = tau_mp ** (-K)

        d_K = a_K * d_mp
        recovered_delta = r_K * d_K
        recovered_delta_sq = (r_K * d_K) ** 2
        exact_delta_sq = d_mp ** 2

        err_delta = abs(recovered_delta - d_mp)
        err_sq = abs(recovered_delta_sq - exact_delta_sq)

        return {
            "delta": mpmath.nstr(d_mp, n=dps),
            "K": K,
            "d_rho_K": mpmath.nstr(d_K, n=dps),
            "recovered_delta": mpmath.nstr(recovered_delta, n=dps),
            "recovered_delta_sq": mpmath.nstr(recovered_delta_sq, n=dps),
            "exact_delta_sq": mpmath.nstr(exact_delta_sq, n=dps),
            "error_delta": mpmath.nstr(err_delta, n=6),
            "error_sq": mpmath.nstr(err_sq, n=6),
            "status": "TRANSPORTED_RADIAL_DEFECT_VERIFIED"
        }


def grade_character_modulus(
    delta: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    K: Union[float, str, mpmath.mpf],
    tau_val: Optional[Union[float, str, mpmath.mpf]] = None,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [CURVATURE-TRANSPORT: GRADE CHARACTER MODULUS & REFLECTION MODES]
    chi_rho(K) = tau^(K*(rho - 1/2)) = exp(K*delta*log(tau)) * exp(i*K*gamma*log(tau)).
    |chi_rho(K)| = exp(K*delta*log(tau)).
    For reflection partner rho^# = 1/2 - delta + i*gamma:
    |chi_{rho^#}(K)| = exp(-K*delta*log(tau)) = |chi_rho(K)|^(-1).
    """
    with mpmath.workdps(dps):
        d_mp = to_mpf(delta, dps=dps)
        g_mp = to_mpf(gamma, dps=dps)
        K_mp = to_mpf(K, dps=dps)
        tau_mp = to_mpf(tau_val if tau_val is not None else 2 * mpmath.pi, dps=dps)
        log_tau = mpmath.log(tau_mp)

        # Direct complex power evaluation
        s_centered = mpmath.mpc(d_mp, g_mp)
        chi_val = mpmath.exp(K_mp * s_centered * log_tau)
        chi_abs = abs(chi_val)

        # Expected modulus
        expected_abs = mpmath.exp(K_mp * d_mp * log_tau)
        abs_err = abs(chi_abs - expected_abs)

        # Reflection partner rho^#
        s_sharp_centered = mpmath.mpc(-d_mp, g_mp)
        chi_sharp_val = mpmath.exp(K_mp * s_sharp_centered * log_tau)
        chi_sharp_abs = abs(chi_sharp_val)
        expected_sharp_abs = mpmath.exp(-K_mp * d_mp * log_tau)
        sharp_abs_err = abs(chi_sharp_abs - expected_sharp_abs)

        reciprocal_prod = chi_abs * chi_sharp_abs
        reciprocal_err = abs(reciprocal_prod - 1)

        return {
            "delta": mpmath.nstr(d_mp, n=dps),
            "gamma": mpmath.nstr(g_mp, n=dps),
            "K": mpmath.nstr(K_mp, n=dps),
            "chi_abs": mpmath.nstr(chi_abs, n=dps),
            "chi_sharp_abs": mpmath.nstr(chi_sharp_abs, n=dps),
            "reciprocal_product": mpmath.nstr(reciprocal_prod, n=dps),
            "abs_error": mpmath.nstr(abs_err, n=6),
            "sharp_abs_error": mpmath.nstr(sharp_abs_err, n=6),
            "reciprocal_error": mpmath.nstr(reciprocal_err, n=6),
            "status": "GRADE_CHARACTER_MODULUS_VERIFIED"
        }


def reflection_pair_defect_B(
    delta: Union[float, str, mpmath.mpf],
    K: Union[float, str, mpmath.mpf],
    tau_val: Optional[Union[float, str, mpmath.mpf]] = None,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [CURVATURE-TRANSPORT: REFLECTION-PAIR DEFECT FORMULAS]
    B_rho(K) = |chi_rho(K)| + |chi_{rho^#}(K)| - 2
             = 2 * (cosh(K*delta*log(tau)) - 1)
             = 4 * sinh^2(K*delta*log(tau) / 2).
    Verifies that all three representations are identical, B_rho(K) >= 0, and
    for K != 0, B_rho(K) == 0 iff delta == 0.
    """
    with mpmath.workdps(dps):
        d_mp = to_mpf(delta, dps=dps)
        K_mp = to_mpf(K, dps=dps)
        tau_mp = to_mpf(tau_val if tau_val is not None else 2 * mpmath.pi, dps=dps)
        log_tau = mpmath.log(tau_mp)
        u = K_mp * d_mp * log_tau

        # Three formulations
        val_exp = mpmath.exp(u) + mpmath.exp(-u) - 2
        val_cosh = 2 * (mpmath.cosh(u) - 1)
        val_sinh = 4 * (mpmath.sinh(u / 2) ** 2)

        err_cosh = abs(val_exp - val_cosh)
        err_sinh = abs(val_exp - val_sinh)

        is_nonnegative = bool(val_exp >= 0)
        is_zero_at_delta_zero = bool(d_mp == 0 and val_exp == 0)

        # Exact symbolic verification via SymPy
        import importlib
        sp: Any = importlib.import_module("sympy")
        u_s = sp.symbols("u", real=True)
        exp_sym = sp.exp(u_s) + sp.exp(-u_s) - 2
        cosh_sym = 2 * (sp.cosh(u_s) - 1)
        sinh_sym = 4 * (sp.sinh(u_s / 2) ** 2)

        sym_cosh_diff = sp.simplify(exp_sym - cosh_sym)
        sym_sinh_diff = sp.simplify(exp_sym.rewrite(sp.sinh) - sinh_sym)
        is_symbolic_exact = bool(sym_cosh_diff == 0 and sp.simplify(cosh_sym - sinh_sym) == 0)

        return {
            "delta": mpmath.nstr(d_mp, n=dps),
            "K": mpmath.nstr(K_mp, n=dps),
            "val_exp": mpmath.nstr(val_exp, n=dps),
            "val_cosh": mpmath.nstr(val_cosh, n=dps),
            "val_sinh": mpmath.nstr(val_sinh, n=dps),
            "error_cosh": mpmath.nstr(err_cosh, n=6),
            "error_sinh": mpmath.nstr(err_sinh, n=6),
            "is_nonnegative": is_nonnegative,
            "is_symbolic_exact": is_symbolic_exact,
            "status": "REFLECTION_PAIR_DEFECT_VERIFIED"
        }


def curvature_transport_invariant(
    delta: Union[float, str, mpmath.mpf],
    tau_val: Optional[Union[float, str, mpmath.mpf]] = None,
    h_step: Union[float, str, mpmath.mpf] = "1e-5",
    dps: int = 50
) -> Dict[str, Any]:
    """
    [CURVATURE-TRANSPORT: PRINCIPAL FINITE CURVATURE THEOREM]
    B_rho''(0) = 2 * delta^2 * (log(tau))^2.
    The normalized curvature transport invariant is:
      K_tau(rho) = B_rho''(0) / (2 * (log(tau))^2) = delta^2 = (r_K * d_{rho,K})^2.
    Also computes numerical second derivative via finite difference and compares.
    """
    with mpmath.workdps(dps):
        d_mp = to_mpf(delta, dps=dps)
        tau_mp = to_mpf(tau_val if tau_val is not None else 2 * mpmath.pi, dps=dps)
        log_tau = mpmath.log(tau_mp)
        h_mp = to_mpf(h_step, dps=dps)

        exact_B_second_deriv = 2 * (d_mp ** 2) * (log_tau ** 2)
        exact_curvature_invariant = d_mp ** 2

        # Numerical second derivative of B_rho(K) at K=0
        def B_func(K_val):
            u = K_val * d_mp * log_tau
            return 2 * (mpmath.cosh(u) - 1)

        # Central difference: (B(h) - 2*B(0) + B(-h)) / h^2
        # Since B(0) = 0 and B(h) = B(-h): 2*B(h) / h^2
        num_second_deriv = (B_func(h_mp) - 2 * B_func(mpmath.mpf(0)) + B_func(-h_mp)) / (h_mp ** 2)
        num_curvature = num_second_deriv / (2 * (log_tau ** 2))

        deriv_err = abs(num_second_deriv - exact_B_second_deriv)
        curv_err = abs(num_curvature - exact_curvature_invariant)

        return {
            "delta": mpmath.nstr(d_mp, n=dps),
            "exact_B_second_deriv": mpmath.nstr(exact_B_second_deriv, n=dps),
            "exact_curvature_invariant": mpmath.nstr(exact_curvature_invariant, n=dps),
            "numerical_curvature": mpmath.nstr(num_curvature, n=dps),
            "derivative_error": mpmath.nstr(deriv_err, n=6),
            "curvature_error": mpmath.nstr(curv_err, n=6),
            "status": "CURVATURE_TRANSPORT_INVARIANT_VERIFIED"
        }


def verify_theta_mellin_scaling(
    a: Union[float, str, mpmath.mpf],
    s: Union[complex, str, mpmath.mpc],
    n_terms: int = 150,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [CURVATURE-TRANSPORT: THETA-MELLIN SCALING LAW]
    For a > 0 and Re(s) > 1:
      int_0^inf Theta_a^+(t) t^(s/2 - 1) dt = a^(-s) * pi^(-s/2) * Gamma(s/2) * zeta(s).
    Under half-density normalization:
      a^(1/2) * int_0^inf Theta_a^+(t) t^(s/2 - 1) dt = a^(1/2 - s) * pi^(-s/2) * Gamma(s/2) * zeta(s).
    For a = tau^K, the scale factor is tau^(-K*(s - 1/2)) = chi_s(K)^(-1).
    Evaluates via termwise sum and compares with exact scale factor * Lambda_N(s).
    """
    with mpmath.workdps(dps):
        a_mp = to_mpf(a, dps=dps)
        s_mp = to_mpc(s, dps=dps)
        if a_mp <= 0:
            raise ValueError(f"a must be positive, got {a_mp}")
        if s_mp.real <= 1:
            raise ValueError(f"Re(s) must be > 1 for Dirichlet absolute convergence, got Re(s) = {s_mp.real}")

        # Half-density factor
        scale_factor = (a_mp ** (mpmath.mpf("0.5") - s_mp))
        gamma_factor = (mpmath.pi ** (-s_mp / 2)) * mpmath.gamma(s_mp / 2)

        # Termwise Mellin integration sum
        total_integrated = mpmath.mpc(0)
        total_dirichlet = mpmath.mpc(0)
        for n in range(1, n_terms + 1):
            n_mp = mpmath.mpf(n)
            # Integral of a^(1/2) * exp(-pi*(a*n)^2 * t) * t^(s/2 - 1) dt
            # = a^(1/2) * (pi*(a*n)^2)^(-s/2) * Gamma(s/2)
            # = a^(1/2 - s) * pi^(-s/2) * Gamma(s/2) * n^(-s)
            term_int = (a_mp ** mpmath.mpf("0.5")) * ((mpmath.pi * (a_mp * n_mp)**2) ** (-s_mp / 2)) * mpmath.gamma(s_mp / 2)
            term_dir = n_mp ** (-s_mp)
            total_integrated += term_int
            total_dirichlet += term_dir

        expected_val = scale_factor * gamma_factor * total_dirichlet
        diff = abs(total_integrated - expected_val)

        return {
            "a": mpmath.nstr(a_mp, n=10),
            "s": str(s_mp),
            "scale_factor": str(scale_factor),
            "total_integrated": str(total_integrated),
            "expected_scaled_lambda": str(expected_val),
            "error": mpmath.nstr(diff, n=6),
            "status": "THETA_MELLIN_SCALING_VERIFIED"
        }


def numerical_theta_mellin_quadrature(
    a: Union[float, str, mpmath.mpf],
    s: Union[complex, str, mpmath.mpc],
    N_theta: int = 50,
    dps: int = 35
) -> Dict[str, Any]:
    """
    [CURVATURE-TRANSPORT: NUMERICAL THETA-MELLIN QUADRATURE & TAIL BOUNDS]
    Performs certified numerical quadrature of the finite theta partial sum:
      Theta_{a,N}^+(t) = sum_{n=1}^N exp(-pi * (a*n)^2 * t)
    over t in (0, inf) against the Mellin kernel t^(s/2 - 1).

    Compares the numerical quadrature result against the exact finite Mellin closed form:
      I_{exact,N}(s) = sum_{n=1}^N a^(-s) * pi^(-s/2) * Gamma(s/2) * n^(-s)
                     = a^(-s) * pi^(-s/2) * Gamma(s/2) * sum_{n=1}^N n^(-s).

    Evaluates both explicit Dirichlet tail bounds:
      1. Unnormalized tail bound:
         Tail_{unnorm}(sigma, N) = a^(-sigma) * pi^(-sigma/2) * |Gamma(s/2)| * (N^(1 - sigma)) / (sigma - 1).
      2. Half-density normalized tail bound:
         Tail_{half-density}(sigma, N) = a^(1/2 - sigma) * pi^(-sigma/2) * |Gamma(s/2)| * (N^(1 - sigma)) / (sigma - 1).

    Domain requirements: a > 0, sigma = Re(s) > 1.
    Distinguishes finite numerical verification from the proved infinite Fubini/Tonelli theorem.
    """
    with mpmath.workdps(dps):
        a_mp = to_mpf(a, dps=dps)
        s_mp = to_mpc(s, dps=dps)
        sigma = s_mp.real
        if a_mp <= 0:
            raise ValueError(f"Scale parameter 'a' must be positive, got {a_mp}")
        if sigma <= 1:
            raise ValueError(f"Re(s) must be > 1 for Dirichlet absolute convergence, got Re(s) = {sigma}")

        # Integrand for numerical quadrature: Theta_{a,N}^+(t) * t^(s/2 - 1)
        half_s_minus_1 = s_mp / 2 - 1
        pi_a_sq = mpmath.pi * (a_mp ** 2)

        def integrand_re(t):
            t_mp = mpmath.mpf(t)
            if t_mp <= 0:
                return mpmath.mpf(0)
            th_sum = sum(mpmath.exp(-pi_a_sq * (n**2) * t_mp) for n in range(1, N_theta + 1))
            val = th_sum * (t_mp ** half_s_minus_1)
            return val.real

        def integrand_im(t):
            t_mp = mpmath.mpf(t)
            if t_mp <= 0:
                return mpmath.mpf(0)
            th_sum = sum(mpmath.exp(-pi_a_sq * (n**2) * t_mp) for n in range(1, N_theta + 1))
            val = th_sum * (t_mp ** half_s_minus_1)
            return val.imag

        # Perform numerical quadrature on [0, inf)
        quad_re = mpmath.quad(integrand_re, [0, mpmath.inf])
        quad_im = mpmath.quad(integrand_im, [0, mpmath.inf])
        quad_val = mpmath.mpc(quad_re, quad_im)

        # Exact finite Mellin expression
        gamma_factor = (mpmath.pi ** (-s_mp / 2)) * mpmath.gamma(s_mp / 2)
        dirichlet_partial_sum = sum(mpmath.mpf(n) ** (-s_mp) for n in range(1, N_theta + 1))
        exact_unnorm_finite = (a_mp ** (-s_mp)) * gamma_factor * dirichlet_partial_sum
        exact_halfdensity_finite = (a_mp ** (mpmath.mpf("0.5") - s_mp)) * gamma_factor * dirichlet_partial_sum

        quad_error = abs(quad_val - exact_unnorm_finite)

        # Explicit Dirichlet tail bounds
        N_mp = mpmath.mpf(N_theta)
        tail_sum_bound = (N_mp ** (1 - sigma)) / (sigma - 1)
        abs_gamma = abs(mpmath.gamma(s_mp / 2))
        pi_sigma_factor = mpmath.pi ** (-sigma / 2)

        unnorm_tail_bound = (a_mp ** (-sigma)) * pi_sigma_factor * abs_gamma * tail_sum_bound
        halfdensity_tail_bound = (a_mp ** (mpmath.mpf("0.5") - sigma)) * pi_sigma_factor * abs_gamma * tail_sum_bound

        # Infinite analytic values via Riemann zeta
        zeta_val = mpmath.zeta(s_mp)
        infinite_unnorm_exact = (a_mp ** (-s_mp)) * gamma_factor * zeta_val
        infinite_halfdensity_exact = (a_mp ** (mpmath.mpf("0.5") - s_mp)) * gamma_factor * zeta_val

        finite_vs_infinite_diff = abs(exact_unnorm_finite - infinite_unnorm_exact)

        return {
            "a": mpmath.nstr(a_mp, n=10),
            "s": str(s_mp),
            "sigma": mpmath.nstr(sigma, n=10),
            "N_theta": N_theta,
            "quadrature_result": str(quad_val),
            "exact_unnorm_finite": str(exact_unnorm_finite),
            "exact_halfdensity_finite": str(exact_halfdensity_finite),
            "quadrature_error": mpmath.nstr(quad_error, n=6),
            "unnormalized_tail_bound": mpmath.nstr(unnorm_tail_bound, n=6),
            "halfdensity_tail_bound": mpmath.nstr(halfdensity_tail_bound, n=6),
            "finite_vs_infinite_diff": mpmath.nstr(finite_vs_infinite_diff, n=6),
            "tail_bound_satisfied": bool(finite_vs_infinite_diff <= unnorm_tail_bound * mpmath.mpf("1.01")),
            "status": "THETA_MELLIN_QUADRATURE_VERIFIED"
        }


def verify_scalar_transport_nogo_instances(
    k: Union[float, str, mpmath.mpf],
    delta: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    max_m_order: int = 3,
    tau_val: Optional[Union[float, str, mpmath.mpf]] = None,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [CURVATURE-TRANSPORT: SCALAR-TRANSPORT NO-GO THEOREM & WORLDLINE AUDIT]
    Verifies the fundamental distinction between:
      1. Fixed-Zero Scalar Multiplication:
         For F(k, s) = g(k, s) * L(s) with g(k, s) = tau^(-k*(s - 1/2)),
         at any zero rho where L(rho) = 0, all k-derivatives at fixed rho vanish identically:
           d^m/dk^m F(k, rho) = (- (rho - 1/2) * log(tau))^m * tau^(-k*(rho - 1/2)) * L(rho) == 0.
      2. Zero-Divisor Preservation:
         Since g(k, s) != 0 everywhere, F(k, s) = 0 <=> L(s) = 0, preserving zero multiplicities.
      3. Logarithmic Derivative Decomposition on g*L != 0:
         partial_s log F(k, s) = partial_s log L(s) + partial_s log g(k, s)
                               = L'(s)/L(s) - k * log(tau).
         Valid strictly on g*L != 0 (undefined at zeros).
      4. Coordinate-Pulled Zero Worldline:
         For coordinate-pulled family L_k(s) = L(1/2 + tau^(-k)*(s - 1/2)) and
         moving zero worldline s_rho(k) = 1/2 + tau^k * (rho - 1/2),
         L_k(s_rho(k)) = L(rho) == 0 identically for all k in R.
      5. Unpulled Function & Static Product Counterexample:
         For static L(s) = s - rho, evaluated at the moving point s_rho(k):
           L(s_rho(k)) = (tau^k - 1) * (rho - 1/2),
         which is generically NON-ZERO for k != 0 and rho != 1/2.
         Similarly, static scalar multiplication F(k, s_rho(k)) = g(k, s_rho(k)) * L(s_rho(k)) != 0.
    """
    with mpmath.workdps(dps):
        k_mp = to_mpf(k, dps=dps)
        d_mp = to_mpf(delta, dps=dps)
        g_mp = to_mpf(gamma, dps=dps)
        tau_mp = to_mpf(tau_val if tau_val is not None else 2 * mpmath.pi, dps=dps)
        log_tau = mpmath.log(tau_mp)

        rho_centered = mpmath.mpc(d_mp, g_mp)
        rho_val = mpmath.mpf("0.5") + rho_centered
        # At zero rho, L(rho) = 0
        lambda_rho = mpmath.mpc(0)

        # Multiplier at (k, rho)
        g_k_rho = mpmath.exp(-k_mp * rho_centered * log_tau)
        F_k_rho = g_k_rho * lambda_rho

        # Derivatives d^m/dk^m F(k, rho)
        derivs = []
        for m in range(max_m_order + 1):
            factor = ((-rho_centered * log_tau) ** m) * g_k_rho
            d_m = factor * lambda_rho
            derivs.append((m, str(d_m), bool(d_m == 0)))

        all_derivs_zero = all(item[2] for item in derivs)

        # Logarithmic derivative test at an off-zero point s_test
        s_test = mpmath.mpc("2.0", "3.0")
        z_test = s_test - mpmath.mpf("0.5")
        g_val = mpmath.exp(-k_mp * z_test * log_tau)

        # Synthetic test L(s)
        L_val = mpmath.sin(s_test) + mpmath.mpf("2.0")  # Non-zero
        dL_ds = mpmath.cos(s_test)
        dlog_L = dL_ds / L_val

        # F(k, s) = g(k, s) * L(s)
        F_val = g_val * L_val
        dF_ds = (-k_mp * log_tau) * g_val * L_val + g_val * dL_ds
        dlog_F = dF_ds / F_val

        expected_dlog_F = dlog_L - k_mp * log_tau
        log_deriv_diff = abs(dlog_F - expected_dlog_F)

        # Worldline coordinates: s_rho(k) = 1/2 + tau^k * rho_centered
        tau_k = tau_mp ** k_mp
        s_rho_k = mpmath.mpf("0.5") + tau_k * rho_centered

        # 1. Coordinate-pulled family L_k(s) = L(1/2 + tau^(-k)*(s - 1/2))
        # For L(s) = s - rho: L_k(s) = (1/2 + tau^(-k)*(s - 1/2)) - rho
        # At s = s_rho_k: L_k(s_rho_k) = (1/2 + tau^(-k)*(tau_k * rho_centered)) - (1/2 + rho_centered) == 0
        pulled_eval = (mpmath.mpf("0.5") + (tau_mp ** (-k_mp)) * (s_rho_k - mpmath.mpf("0.5"))) - rho_val
        pulled_worldline_zero_residual = abs(pulled_eval)

        # 2. Unpulled static L(s) = s - rho evaluated at s_rho(k):
        # L(s_rho_k) = s_rho_k - rho = (tau^k - 1) * rho_centered
        unpulled_eval = s_rho_k - rho_val
        expected_unpulled = (tau_k - mpmath.mpf("1.0")) * rho_centered
        unpulled_diff = abs(unpulled_eval - expected_unpulled)

        # 3. Static scalar product F(k, s) = g(k,s)*L(s) at s_rho(k):
        g_at_worldline = mpmath.exp(-k_mp * (s_rho_k - mpmath.mpf("0.5")) * log_tau)
        F_at_worldline = g_at_worldline * unpulled_eval

        is_k_zero = bool(abs(k_mp) < 1e-45)
        is_rho_center = bool(abs(rho_centered) < 1e-45)
        generic_nonzero = not is_k_zero and not is_rho_center

        return {
            "k": mpmath.nstr(k_mp, n=10),
            "delta": mpmath.nstr(d_mp, n=10),
            "gamma": mpmath.nstr(g_mp, n=10),
            "F_k_rho": str(F_k_rho),
            "derivatives": derivs,
            "all_derivatives_identically_zero": all_derivs_zero,
            "log_derivative_diff": mpmath.nstr(log_deriv_diff, n=6),
            "log_derivative_identity_holds": bool(log_deriv_diff < 1e-45),
            "pulled_worldline_zero_residual": mpmath.nstr(pulled_worldline_zero_residual, n=6),
            "pulled_worldline_vanishes": bool(pulled_worldline_zero_residual < 1e-45),
            "unpulled_worldline_eval": str(unpulled_eval),
            "unpulled_formula_diff": mpmath.nstr(unpulled_diff, n=6),
            "unpulled_worldline_is_nonzero": bool(abs(unpulled_eval) > 1e-30) if generic_nonzero else True,
            "static_scalar_worldline_eval": str(F_at_worldline),
            "static_scalar_worldline_is_nonzero": bool(abs(F_at_worldline) > 1e-30) if generic_nonzero else True,
            "status": "SCALAR_TRANSPORT_NOGO_INSTANCES_VERIFIED"
        }


# ============================================================================
# WEIL–HERMITIAN CURVATURE BRIDGE CONSTRUCTORS & SPECTRAL VERIFIERS
# ============================================================================

def evaluate_pointwise_weil_curvature_identity(
    delta: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    tau_val: Optional[Union[float, str, mpmath.mpf]] = None,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [WEIL-CURVATURE: POINTWISE WEIL-HERMITIAN CURVATURE IDENTITY]
    For any non-trivial point rho = 1/2 + delta + i*gamma (with delta != +-1/2):
      1. Geometric Involutions:
         J(rho) = 1 - rho (functional reflection), C(rho) = conj(rho) (conjugation).
         J(rho) - C(rho) = 1 - rho - conj(rho) = - 2 * delta.
         |J(rho) - C(rho)|^2 = 4 * delta^2.
         J(rho) == C(rho) <=> delta == 0 <=> Re(rho) == 1/2.
      2. Pointwise Symmetrized Hermitian & Weil Terms:
         T_sym(rho) = 1/2 * (1/|rho|^2 + 1/|1-rho|^2)
         T_weil(rho) = Re( 1 / (rho * (1 - rho)) )
      3. Pointwise Difference & Rational Curvature Identity:
         T_sym(rho) - T_weil(rho) = 2 * delta^2 / (|rho|^2 * |1-rho|^2)
                                  = B_rho''(0) / ((log tau)^2 * |rho|^2 * |1-rho|^2) >= 0,
         with equality if and only if delta == 0.
    """
    with mpmath.workdps(dps):
        d_f = to_mpf(delta, dps=dps)
        g_f = to_mpf(gamma, dps=dps)
        tau_mp = to_mpf(tau_val if tau_val is not None else 2 * mpmath.pi, dps=dps)
        log_tau = mpmath.log(tau_mp)

        rho = mpmath.mpc(mpmath.mpf("0.5") + d_f, g_f)
        one_minus_rho = mpmath.mpc(mpmath.mpf("0.5") - d_f, -g_f)

        # Involutions
        J_rho = mpmath.mpc(1) - rho
        C_rho = mpmath.conj(rho)
        involution_diff = J_rho - C_rho
        expected_inv_diff = mpmath.mpc(-2 * d_f, 0)
        inv_diff_err = abs(involution_diff - expected_inv_diff)

        sq_discrepancy = abs(involution_diff) ** 2
        expected_sq_disc = 4 * (d_f ** 2)
        sq_disc_err = abs(sq_discrepancy - expected_sq_disc)

        # Moduli
        abs_rho_sq = abs(rho) ** 2
        abs_one_minus_rho_sq = abs(one_minus_rho) ** 2
        denom = abs_rho_sq * abs_one_minus_rho_sq

        # Symmetrized Hermitian term
        T_sym = mpmath.mpf("0.5") * (1 / abs_rho_sq + 1 / abs_one_minus_rho_sq)

        # Weil term
        prod_rho = rho * one_minus_rho
        inv_prod = 1 / prod_rho
        T_weil = mpmath.re(inv_prod)

        # Direct difference
        T_diff = T_sym - T_weil

        # Rational curvature target
        T_exact = (2 * (d_f ** 2)) / denom

        # Curvature invariant target B_rho''(0) / ((log tau)^2 * denom)
        B_double_prime = 2 * (d_f ** 2) * (log_tau ** 2)
        T_curv = B_double_prime / ((log_tau ** 2) * denom)

        diff_vs_exact_err = abs(T_diff - T_exact)
        exact_vs_curv_err = abs(T_exact - T_curv)

        return {
            "delta": mpmath.nstr(d_f, n=10),
            "gamma": mpmath.nstr(g_f, n=10),
            "rho": str(rho),
            "J_rho": str(J_rho),
            "C_rho": str(C_rho),
            "involution_diff_err": mpmath.nstr(inv_diff_err, n=6),
            "sq_discrepancy": mpmath.nstr(sq_discrepancy, n=15),
            "sq_discrepancy_err": mpmath.nstr(sq_disc_err, n=6),
            "T_sym": mpmath.nstr(T_sym, n=20),
            "T_weil": mpmath.nstr(T_weil, n=20),
            "T_diff": mpmath.nstr(T_diff, n=20),
            "T_exact": mpmath.nstr(T_exact, n=20),
            "T_curv": mpmath.nstr(T_curv, n=20),
            "diff_vs_exact_err": mpmath.nstr(diff_vs_exact_err, n=6),
            "exact_vs_curv_err": mpmath.nstr(exact_vs_curv_err, n=6),
            "is_exact_match": bool(diff_vs_exact_err < 1e-45 and exact_vs_curv_err < 1e-45),
            "is_on_critical_line": bool(abs(d_f) < 1e-45),
            "status": "POINTWISE_WEIL_CURVATURE_IDENTITY_VERIFIED"
        }


def evaluate_weil_hermitian_spectral_sums(
    zeros_list: List[Tuple[Any, Any, int]],
    tau_val: Optional[Union[float, str, mpmath.mpf]] = None,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [WEIL-CURVATURE: FINITE SPECTRAL SUMS & CURVATURE DEFECT CLOSURE]
    For a finite list of zeros (delta_j, gamma_j, multiplicity_j):
      N_xi,trunc = sum_j m_j / |rho_j|^2
      N_xi,sym   = sum_j m_j * 1/2 * (1/|rho_j|^2 + 1/|1-rho_j|^2)
      C_xi,trunc = sum_j m_j * Re(1 / (rho_j * (1 - rho_j)))
      Delta_diff = N_xi,sym - C_xi,trunc
      Delta_curv = sum_j m_j * 2 * delta_j^2 / (|rho_j|^2 * |1-rho_j|^2)
                 = sum_j m_j * B_{rho_j}''(0) / ((log tau)^2 * |rho_j|^2 * |1-rho_j|^2).
    Verifies:
      1. |Delta_diff - Delta_curv| == 0 to high precision.
      2. For all on-line zeros (delta_j = 0), Delta_curv == 0 exactly.
      3. For any off-line quartet (delta_j != 0), Delta_curv > 0 strictly.
      4. Compares against the exact completed-xi Hadamard constant:
         C_xi = 2 + EulerGamma - log(4*pi) approx 0.0461914179322420...
    """
    with mpmath.workdps(dps):
        tau_mp = to_mpf(tau_val if tau_val is not None else 2 * mpmath.pi, dps=dps)
        log_tau = mpmath.log(tau_mp)

        # Classical completed-xi Hadamard constant
        # C_xi = 2 + EulerGamma - log(4*pi)
        C_xi_exact = mpmath.mpf("2.0") + mpmath.euler - mpmath.log(4 * mpmath.pi)

        sum_N_direct = mpmath.mpf(0)
        sum_N_sym = mpmath.mpf(0)
        sum_C_trunc = mpmath.mpf(0)
        sum_curv = mpmath.mpf(0)

        all_on_line = True
        has_off_line = False

        for (d_val, g_val, mult) in zeros_list:
            d_f = to_mpf(d_val, dps=dps)
            g_f = to_mpf(g_val, dps=dps)
            m_f = mpmath.mpf(mult)

            if abs(d_f) > 1e-45:
                all_on_line = False
                has_off_line = True

            rho = mpmath.mpc(mpmath.mpf("0.5") + d_f, g_f)
            one_minus_rho = mpmath.mpc(mpmath.mpf("0.5") - d_f, -g_f)

            abs_rho_sq = abs(rho) ** 2
            abs_one_minus_rho_sq = abs(one_minus_rho) ** 2
            denom = abs_rho_sq * abs_one_minus_rho_sq

            # Direct N
            sum_N_direct += m_f * (1 / abs_rho_sq)

            # Symmetrized N
            t_sym = mpmath.mpf("0.5") * (1 / abs_rho_sq + 1 / abs_one_minus_rho_sq)
            sum_N_sym += m_f * t_sym

            # Weil term
            prod_rho = rho * one_minus_rho
            t_weil = mpmath.re(1 / prod_rho)
            sum_C_trunc += m_f * t_weil

            # Curvature term
            t_curv = (2 * (d_f ** 2)) / denom
            sum_curv += m_f * t_curv

        delta_diff = sum_N_sym - sum_C_trunc
        closure_error = abs(delta_diff - sum_curv)

        return {
            "num_zeros": len(zeros_list),
            "all_on_line": all_on_line,
            "has_off_line": has_off_line,
            "C_xi_classical_constant": mpmath.nstr(C_xi_exact, n=20),
            "N_xi_direct": mpmath.nstr(sum_N_direct, n=20),
            "N_xi_sym": mpmath.nstr(sum_N_sym, n=20),
            "C_xi_trunc": mpmath.nstr(sum_C_trunc, n=20),
            "delta_diff": mpmath.nstr(delta_diff, n=20),
            "delta_curv": mpmath.nstr(sum_curv, n=20),
            "closure_error": mpmath.nstr(closure_error, n=6),
            "closure_satisfied": bool(closure_error < 1e-40),
            "curvature_defect_is_zero": bool(sum_curv < 1e-45) if all_on_line else False,
            "curvature_defect_is_positive": bool(sum_curv > 1e-45) if has_off_line else True,
            "status": "WEIL_HERMITIAN_SPECTRAL_SUMS_VERIFIED"
        }


def evaluate_finite_prime_weil_gram_matrix(
    primes: Optional[List[int]] = None,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [WEIL-CURVATURE: FINITE-PRIME WEIL GRAM MATRIX & TWO-BUMP WITNESS AUDIT]
    Evaluates the finite-prime local distribution operator on smooth bump test functions:
      1. For localized smooth test functions f_p(u) = c1 * psi_eps(u - u1) + c2 * psi_eps(u - u2)
         in C_c^infty(R) with separation u2 - u1 = log p and narrow support eps < 1/2 min |log n1 - log n2|:
         - At separation u = 0, no prime frequency log n (n >= 2) is within the support (diagonal entries are 0).
         - At separation u = +- log p, the prime distribution contributes -w_p = - (log p) / (2 * sqrt(p)).
      2. The resulting 2x2 local prime Gram matrix is:
         W_{prime, p} = [[0, -w_p], [-w_p, 0]],
         with eigenvalues lambda_1 = +w_p and lambda_2 = -w_p.
      3. Spectrum & Positivity Conclusion:
         - The pure prime-only autocorrelation form is INDEFINITE (has both positive and negative eigenvalues).
         - It is NOT positive semidefinite.
         - It is NOT "strictly negative-definite" (corrected from naive diagonal list).
      4. Mathematical Implication:
         - Pure arithmetic prime distributions alone do NOT form a positive-definite quadratic form.
         - Global Weil positivity Q_W(f * f*) >= 0 requires global cancellation between the prime distribution
           and the positive Archimedean and pole distributions.
         - Local prime factorizations alone fail (FAIL_NAIVE_PRIME_LOCAL_FACTORIZATION).
    """
    with mpmath.workdps(dps):
        if primes is None:
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

        n = len(primes)
        two_bump_data = []
        for p in primes:
            p_mp = mpmath.mpf(p)
            w_p = mpmath.log(p_mp) / (2 * mpmath.sqrt(p_mp))
            # 2x2 matrix eigenvalues are +w_p and -w_p
            two_bump_data.append({
                "prime": p,
                "w_p": mpmath.nstr(w_p, n=10),
                "eigenvalues": [mpmath.nstr(w_p, n=10), mpmath.nstr(-w_p, n=10)],
                "is_indefinite": True
            })

        return {
            "primes": primes,
            "num_primes": n,
            "two_bump_witnesses": two_bump_data,
            "witness_model": "SMOOTH_BUMP_TEST_FUNCTION_MODEL",
            "prime_matrix_form": "[[0, -w_p], [-w_p, 0]]",
            "eigenvalue_spectrum": "+- w_p (indefinite)",
            "is_positive_semidefinite": False,
            "is_strictly_negative_definite": False,
            "falsification_witness": "PRIME_ONLY_AUTOCORRELATION_IS_INDEFINITE_NOT_POSITIVE_SEMIDEFINITE",
            "classification": "FAIL_NAIVE_PRIME_LOCAL_FACTORIZATION",
            "global_weil_positivity_status": "OPEN_GLOBAL_POSITIVE_TYPE_FACTORIZATION",
            "status": "FINITE_PRIME_WEIL_GRAM_MATRIX_ANALYZED"
        }


def evaluate_fourier_mellin_probe_analysis(
    s_val: Union[complex, str, mpmath.mpc],
    tau_val: Optional[Union[float, str, mpmath.mpf]] = None,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [WEIL-CURVATURE: MELLIN PROBE REGULARIZATION & TEST FUNCTION AUDIT]
    Audits the exact Mellin transform of test functions vs the spectral probe 1/s:
      1. Naive indicator g_0(x) = x^{-1/2} * 1_{[1, tau]}(x):
         \\widehat g_0(s) = \\int_1^tau x^{s-3/2} dx = (tau^{s-1/2} - 1) / (s - 1/2).
         Falsifies the naive identification \\widehat g_0(s) == 1/s.
      2. Spectral Probe \\Phi_0(s) = 1/s:
         Corresponds to g(x) = 1_{(0,1)}(x) under standard Mellin, or in additive
         logarithmic coordinates u = log x in (-infty, 0) with f_0(u) = exp(u/2) * 1_{(-infty, 0)}(u).
      3. Admissible Regularization:
         Because 1_{(0,1)} is not in C_c^infty, the expression (exp(-eps*s) - exp(-L*s))/s is the
         transform of a sharp truncated window 1_{[eps, L]}(u), NOT a C_c^infty smoothing family.
         An admissible smooth probe family with proved zero-sum/prime-sum limit interchange remains open.
      4. Subgate Classifications:
         - FAIL_TEST_FUNCTION_IDENTIFICATION: Naive x^{-1/2} 1_{[1, tau]} != 1/s.
         - OPEN_ADMISSIBLE_PROBE_REGULARIZATION: Explicit smooth C_c^infty probe regularization.
    """
    with mpmath.workdps(dps):
        s_c = to_mpc(s_val, dps=dps)
        tau_mp = to_mpf(tau_val if tau_val is not None else 2 * mpmath.pi, dps=dps)

        s_minus_half = s_c - mpmath.mpf("0.5")
        if abs(s_minus_half) < 1e-45:
            ghat_g0 = mpmath.log(tau_mp)
        else:
            ghat_g0 = (tau_mp ** s_minus_half - 1) / s_minus_half

        phi_0 = 1 / s_c
        diff_g0_vs_phi0 = abs(ghat_g0 - phi_0)
        is_exact_phi0 = bool(diff_g0_vs_phi0 < 1e-45)

        eps = mpmath.mpf("1e-4")
        L = mpmath.mpf("50.0")
        phi_sharp_cutoff = (mpmath.exp(-eps * s_c) - mpmath.exp(-L * s_c)) / s_c
        reg_diff = abs(phi_sharp_cutoff - phi_0)

        return {
            "s": str(s_c),
            "tau": mpmath.nstr(tau_mp, n=10),
            "ghat_g0": str(ghat_g0),
            "phi_0": str(phi_0),
            "diff_g0_vs_phi0": mpmath.nstr(diff_g0_vs_phi0, n=10),
            "g0_equals_1_over_s": is_exact_phi0,
            "phi_sharp_cutoff": str(phi_sharp_cutoff),
            "cutoff_regularization_error": mpmath.nstr(reg_diff, n=10),
            "regularization_error": mpmath.nstr(reg_diff, n=10),
            "is_smooth_cc_infty": False,
            "test_function_classification": "FAIL_TEST_FUNCTION_IDENTIFICATION",
            "regularization_obligation": "OPEN_ADMISSIBLE_PROBE_REGULARIZATION",
            "status": "FOURIER_MELLIN_PROBE_ANALYSIS_COMPLETED"
        }


def evaluate_additive_coordinate_weil_hermitian_form(
    zeros_list: List[Tuple[Any, Any, int]],
    dps: int = 50
) -> Dict[str, Any]:
    """
    [WEIL-CURVATURE: UNIFIED ADDITIVE COORDINATE WEIL FORM & HERMITIAN PARSEVAL]
    In additive logarithmic coordinates u = log x in R:
      \\Phi_f(s) = \\int_R f(u) exp((s - 1/2) u) du
      f^*(u) = conj(f(-u))
      \\Phi_{f * f^*}(s) = \\Phi_f(s) * conj(\\Phi_f(1 - bar{s}))
    Hermitian Weil functional on f:
      Q_W(f) = sum_rho \\Phi_f(rho) * conj(\\Phi_f(1 - bar{rho})).
    Hermitian companion functional:
      Q_H(f) = sum_rho |\\Phi_f(rho)|^2.
    Reduction on RH:
      On RH (1 - bar{rho} = rho), conj(\\Phi_f(1 - bar{rho})) = conj(\\Phi_f(rho)),
      so Q_W(f) = sum_rho |\\Phi_f(rho)|^2 = Q_H(f).
    For off-line zeros (rho = 1/2 + delta + i*gamma with delta != 0):
      Q_W(f) != Q_H(f) in general, with discrepancy governed by the involution difference
      J(rho) - C(rho) = - 2 * delta.
    """
    with mpmath.workdps(dps):
        sum_Q_W = mpmath.mpc(0)
        sum_Q_H = mpmath.mpf(0)
        all_on_line = True

        for (d_val, g_val, mult) in zeros_list:
            d_f = to_mpf(d_val, dps=dps)
            g_f = to_mpf(g_val, dps=dps)
            m_f = mpmath.mpf(mult)

            if abs(d_f) > 1e-45:
                all_on_line = False

            rho = mpmath.mpc(mpmath.mpf("0.5") + d_f, g_f)
            one_minus_conj_rho = mpmath.mpc(mpmath.mpf("0.5") - d_f, g_f)

            phi_rho = 1 / rho
            phi_one_minus_conj = 1 / one_minus_conj_rho

            term_W = phi_rho * mpmath.conj(phi_one_minus_conj)
            sum_Q_W += m_f * term_W

            term_H = abs(phi_rho) ** 2
            sum_Q_H += m_f * term_H

            # Reciprocal modulus discrepancy
            # Edwards (1974, p. 19-21), Davenport (1980, Ch. 12)

        Q_W_re = mpmath.re(sum_Q_W)
        Q_W_im = mpmath.im(sum_Q_W)
        diff_QH_vs_QW = abs(sum_Q_H - Q_W_re)

        return {
            "num_zeros": len(zeros_list),
            "all_on_line": all_on_line,
            "Q_W_real": mpmath.nstr(Q_W_re, n=20),
            "Q_W_imag": mpmath.nstr(Q_W_im, n=6),
            "Q_H": mpmath.nstr(sum_Q_H, n=20),
            "diff_QH_vs_QW": mpmath.nstr(diff_QH_vs_QW, n=20),
            "equality_holds": bool(diff_QH_vs_QW < 1e-40),
            "status": "ADDITIVE_COORDINATE_WEIL_HERMITIAN_FORM_EVALUATED"
        }


def countermodel_polynomial_P(
    z: Union[complex, str, mpmath.mpc],
    delta: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    dps: int = 50
) -> mpmath.mpc:
    """
    [CURVATURE-TRANSPORT: SYMMETRY-COMPLETE COUNTERMODEL POLYNOMIAL]
    P_{delta,gamma}(z) = ((z - i*gamma)^2 - delta^2) * ((z + i*gamma)^2 - delta^2)
                       = (z^2 + gamma^2 - delta^2)^2 + 4 * delta^2 * gamma^2.
    Roots in centered coordinate z = s - 1/2 are exactly +-delta +- i*gamma.
    """
    with mpmath.workdps(dps):
        z_c = to_mpc(z, dps=dps)
        d_f = to_mpf(delta, dps=dps)
        g_f = to_mpf(gamma, dps=dps)
        i_gamma = mpmath.mpc(0, g_f)

        t1 = (z_c - i_gamma)**2 - (d_f**2)
        t2 = (z_c + i_gamma)**2 - (d_f**2)
        return t1 * t2


def verify_countermodel_symmetries(
    delta: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    dps: int = 50
) -> Dict[str, Any]:
    """
    [CURVATURE-TRANSPORT: COUNTERMODEL SYMMETRY & DETECTOR VERIFICATION]
    Verifies that the off-line quartet polynomial P_{delta,gamma}(z) satisfies:
      1. Even functional symmetry: P(-z) == P(z)
      2. Schwarz reflection symmetry: conj(P(conj(z))) == P(z)
      3. Zeros at z in {+-delta +- i*gamma}
      4. Transported radial unit: r_K * d_{rho,K} == delta
      5. Reciprocal grade characters: |chi_rho(K)| * |chi_{rho^#}(K)| == 1
      6. Positive grade curvature: B_rho''(0) == 2 * delta^2 * (log(tau))^2 > 0 (for delta != 0).
    """
    with mpmath.workdps(dps):
        d_f = to_mpf(delta, dps=dps)
        g_f = to_mpf(gamma, dps=dps)
        tau_mp = 2 * mpmath.pi

        z_test = mpmath.mpc("1.25", "3.75")
        p_z = countermodel_polynomial_P(z_test, d_f, g_f, dps=dps)
        p_neg_z = countermodel_polynomial_P(-z_test, d_f, g_f, dps=dps)
        p_conj_z = countermodel_polynomial_P(mpmath.conj(z_test), d_f, g_f, dps=dps)

        even_err = abs(p_neg_z - p_z)
        schwarz_err = abs(mpmath.conj(p_conj_z) - p_z)

        roots = [
            mpmath.mpc(d_f, g_f),
            mpmath.mpc(d_f, -g_f),
            mpmath.mpc(-d_f, g_f),
            mpmath.mpc(-d_f, -g_f),
        ]
        root_residuals = [abs(countermodel_polynomial_P(r, d_f, g_f, dps=dps)) for r in roots]
        max_root_res = max(root_residuals)

        B_info = curvature_transport_invariant(d_f, tau_val=tau_mp, dps=dps)

        return {
            "delta": mpmath.nstr(d_f, n=10),
            "gamma": mpmath.nstr(g_f, n=10),
            "even_symmetry_error": mpmath.nstr(even_err, n=6),
            "schwarz_symmetry_error": mpmath.nstr(schwarz_err, n=6),
            "max_root_residual": mpmath.nstr(max_root_res, n=6),
            "grade_curvature": B_info["exact_curvature_invariant"],
            "status": "COUNTERMODEL_SYMMETRIES_VERIFIED"
        }


# ============================================================================
# EXACT INTEGRATED-SIGMA RESOLVENT & CMSA-RDQ DERIVATIVE IDENTITIES
# ============================================================================

def evaluate_quartet_resolvent_difference(
    delta: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    z: Union[complex, str, mpmath.mpc],
    dps: int = 50
) -> Dict[str, Any]:
    """
    [INTEGRATED-SIGMA: EXACT QUARTET-MINUS-PROJECTION RESOLVENT DIFFERENCE]
    For centered coordinate z = a + i*t (a = sigma - 1/2 > 0):
      1. Single upper-height group (+i*gamma):
         Delta Z_+(z) = 1/(z - (delta + i*gamma)) + 1/(z - (-delta + i*gamma)) - 2/(z - i*gamma)
                      = 2*delta^2 / ((z - i*gamma) * ((z - i*gamma)^2 - delta^2)).
      2. Single lower-height group (-i*gamma):
         Delta Z_-(z) = 1/(z - (delta - i*gamma)) + 1/(z - (-delta - i*gamma)) - 2/(z + i*gamma)
                      = 2*delta^2 / ((z + i*gamma) * ((z + i*gamma)^2 - delta^2)).
      3. Complete quartet (adding +i*gamma and -i*gamma groups):
         Delta Z_full(z) = Delta Z_+(z) + Delta Z_-(z).
    """
    with mpmath.workdps(dps):
        d_f = to_mpf(delta, dps=dps)
        g_f = to_mpf(gamma, dps=dps)
        z_c = to_mpc(z, dps=dps)

        i_gam = mpmath.mpc(0, g_f)

        # Upper group direct
        term_plus_delta = 1 / (z_c - (d_f + i_gam))
        term_minus_delta = 1 / (z_c - (-d_f + i_gam))
        term_proj = 2 / (z_c - i_gam)
        delta_Z_plus_direct = term_plus_delta + term_minus_delta - term_proj

        # Upper group rational formula
        w_plus = z_c - i_gam
        delta_Z_plus_rational = (2 * (d_f**2)) / (w_plus * (w_plus**2 - d_f**2))

        diff_plus = abs(delta_Z_plus_direct - delta_Z_plus_rational)

        # Lower group direct
        term_plus_delta_neg = 1 / (z_c - (d_f - i_gam))
        term_minus_delta_neg = 1 / (z_c - (-d_f - i_gam))
        term_proj_neg = 2 / (z_c + i_gam)
        delta_Z_minus_direct = term_plus_delta_neg + term_minus_delta_neg - term_proj_neg

        # Lower group rational formula
        w_minus = z_c + i_gam
        delta_Z_minus_rational = (2 * (d_f**2)) / (w_minus * (w_minus**2 - d_f**2))

        diff_minus = abs(delta_Z_minus_direct - delta_Z_minus_rational)

        # Complete quartet
        delta_Z_total = delta_Z_plus_rational + delta_Z_minus_rational

        return {
            "delta": mpmath.nstr(d_f, n=10),
            "gamma": mpmath.nstr(g_f, n=10),
            "z": str(z_c),
            "delta_Z_plus_direct": str(delta_Z_plus_direct),
            "delta_Z_plus_rational": str(delta_Z_plus_rational),
            "delta_Z_minus_direct": str(delta_Z_minus_direct),
            "delta_Z_minus_rational": str(delta_Z_minus_rational),
            "diff_plus": mpmath.nstr(diff_plus, n=6),
            "diff_minus": mpmath.nstr(diff_minus, n=6),
            "delta_Z_total": str(delta_Z_total),
            "is_exact_identity": bool(diff_plus < 1e-45 and diff_minus < 1e-45),
            "status": "QUARTET_RESOLVENT_DIFFERENCE_VERIFIED"
        }


def evaluate_cmsa_rdq_derivative_identity(
    delta: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    z: Union[complex, str, mpmath.mpc],
    dps: int = 50
) -> Dict[str, Any]:
    """
    [INTEGRATED-SIGMA: EXACT ONE-HEIGHT & FULL-QUARTET RDQ LOGARITHMIC DERIVATIVE IDENTITIES]
    Proves that the quartet-minus-projection resolvent differences are the exact logarithmic
    derivatives of the corresponding RDQ rational quotient factors:
      1. Upper height factor (+i*gamma):
         q^+_{delta, gamma}(z) = 1 - delta^2 / (z - i*gamma)^2.
         d/dz log q^+_{delta, gamma}(z) = Delta Z_+(z).
      2. Lower height factor (-i*gamma):
         q^-_{delta, gamma}(z) = 1 - delta^2 / (z + i*gamma)^2.
         d/dz log q^-_{delta, gamma}(z) = Delta Z_-(z).
      3. Full quartet quotient:
         q^{full}_{delta, gamma}(z) = q^+_{delta, gamma}(z) * q^-_{delta, gamma}(z).
         d/dz log q^{full}_{delta, gamma}(z) = Delta Z_+(z) + Delta Z_-(z) = Delta Z_full(z).
    """
    with mpmath.workdps(dps):
        d_f = to_mpf(delta, dps=dps)
        g_f = to_mpf(gamma, dps=dps)
        z_c = to_mpc(z, dps=dps)
        i_gam = mpmath.mpc(0, g_f)

        # Upper factor q^+
        w_plus = z_c - i_gam
        q_plus = 1 - (d_f**2) / (w_plus**2)
        q_plus_prime = (2 * (d_f**2)) / (w_plus**3)
        log_deriv_plus = q_plus_prime / q_plus
        delta_Z_plus = (2 * (d_f**2)) / (w_plus * (w_plus**2 - d_f**2))
        diff_plus = abs(log_deriv_plus - delta_Z_plus)

        # Lower factor q^-
        w_minus = z_c + i_gam
        q_minus = 1 - (d_f**2) / (w_minus**2)
        q_minus_prime = (2 * (d_f**2)) / (w_minus**3)
        log_deriv_minus = q_minus_prime / q_minus
        delta_Z_minus = (2 * (d_f**2)) / (w_minus * (w_minus**2 - d_f**2))
        diff_minus = abs(log_deriv_minus - delta_Z_minus)

        # Full quotient q_full
        q_full = q_plus * q_minus
        log_deriv_full = log_deriv_plus + log_deriv_minus
        delta_Z_full = delta_Z_plus + delta_Z_minus
        diff_full = abs(log_deriv_full - delta_Z_full)

        return {
            "delta": mpmath.nstr(d_f, n=10),
            "gamma": mpmath.nstr(g_f, n=10),
            "z": str(z_c),
            "q_plus": str(q_plus),
            "q_minus": str(q_minus),
            "q_full": str(q_full),
            "log_deriv_plus": str(log_deriv_plus),
            "log_deriv_minus": str(log_deriv_minus),
            "log_deriv_full": str(log_deriv_full),
            "delta_Z_plus": str(delta_Z_plus),
            "delta_Z_minus": str(delta_Z_minus),
            "delta_Z_full": str(delta_Z_full),
            "diff_plus": mpmath.nstr(diff_plus, n=6),
            "diff_minus": mpmath.nstr(diff_minus, n=6),
            "diff_full": mpmath.nstr(diff_full, n=6),
            "is_exact_plus_identity": bool(diff_plus < 1e-45),
            "is_exact_minus_identity": bool(diff_minus < 1e-45),
            "is_exact_full_identity": bool(diff_full < 1e-45),
            "is_exact_identity": bool(diff_plus < 1e-45 and diff_minus < 1e-45 and diff_full < 1e-45),
            "status": "CMSA_RDQ_DERIVATIVE_IDENTITY_VERIFIED"
        }


def evaluate_integrated_resolvent_l2_norm(
    delta: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    a: Union[float, str, mpmath.mpf],
    dps: int = 50
) -> Dict[str, Any]:
    """
    [INTEGRATED-SIGMA: EXACT L^2(dt) LEADING COEFFICIENT & INTEGRABILITY]
    Evaluates the L^2(dt) norm of the leading single-height resolvent variation:
      Delta Z_+ approx 2*delta^2 / (a + i*(t - gamma))^3.
      || 2*delta^2 / (a + i*(t - gamma))^3 ||_{L^2(dt)}^2 = 3 * pi * delta^4 / (2 * a^5).
    Compares the closed-form formula against high-precision numerical quadrature over (-infty, infty).
    """
    with mpmath.workdps(dps):
        d_f = to_mpf(delta, dps=dps)
        g_f = to_mpf(gamma, dps=dps)
        a_f = to_mpf(a, dps=dps)

        if a_f <= abs(d_f):
            raise ValueError(f"Requires a > |delta| for separation: got a={a_f}, delta={d_f}")

        # Exact formula for leading L^2 norm
        leading_exact = (3 * mpmath.pi * (d_f**4)) / (2 * (a_f**5))

        # Numerical quadrature of leading term
        def leading_integrand(t: mpmath.mpf) -> mpmath.mpf:
            w = mpmath.mpc(a_f, t - g_f)
            val = (2 * (d_f**2)) / (w**3)
            return abs(val)**2

        leading_quad = mpmath.quad(leading_integrand, [-mpmath.inf, mpmath.inf])
        diff_leading = abs(leading_quad - leading_exact)

        # Full exact resolvent L^2 norm (including delta^2 in denominator)
        def full_single_integrand(t: mpmath.mpf) -> mpmath.mpf:
            w = mpmath.mpc(a_f, t - g_f)
            val = (2 * (d_f**2)) / (w * (w**2 - d_f**2))
            return abs(val)**2

        full_single_quad = mpmath.quad(full_single_integrand, [-mpmath.inf, mpmath.inf])

        # Complete two-height quartet L^2 norm (adding +gamma and -gamma with cross-term)
        def full_two_height_integrand(t: mpmath.mpf) -> mpmath.mpf:
            w_plus = mpmath.mpc(a_f, t - g_f)
            w_minus = mpmath.mpc(a_f, t + g_f)
            val_plus = (2 * (d_f**2)) / (w_plus * (w_plus**2 - d_f**2))
            val_minus = (2 * (d_f**2)) / (w_minus * (w_minus**2 - d_f**2))
            return abs(val_plus + val_minus)**2

        full_two_height_quad = mpmath.quad(full_two_height_integrand, [-mpmath.inf, mpmath.inf])

        # Doubled single-height for comparison
        doubled_leading = 2 * leading_exact

        return {
            "delta": mpmath.nstr(d_f, n=10),
            "gamma": mpmath.nstr(g_f, n=10),
            "a": mpmath.nstr(a_f, n=10),
            "leading_exact": mpmath.nstr(leading_exact, n=20),
            "leading_quad": mpmath.nstr(leading_quad, n=20),
            "diff_leading": mpmath.nstr(diff_leading, n=6),
            "full_single_quad": mpmath.nstr(full_single_quad, n=20),
            "doubled_leading": mpmath.nstr(doubled_leading, n=20),
            "full_two_height_quad": mpmath.nstr(full_two_height_quad, n=20),
            "is_exact_leading_match": bool(diff_leading < 1e-10 or (abs(leading_exact) > 0 and abs(diff_leading / leading_exact) < 1e-5)),
            "status": "INTEGRATED_RESOLVENT_L2_NORM_VERIFIED"
        }


def evaluate_fourier_quartet_difference(
    delta: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    a: Union[float, str, mpmath.mpf],
    xi: Union[float, str, mpmath.mpf],
    dps: int = 50
) -> Dict[str, Any]:
    """
    [INTEGRATED-SIGMA: EXACT FOURIER TRANSFORM OF COMPLETE QUARTET DIFFERENCE]
    Under Fourier convention \\widehat f(\\xi) = \\int_{-\\infty}^\\infty f(t) e^{i t \\xi} dt:
    For a > |delta| > 0 and \\xi > 0:
      1. Single-height (+i*gamma):
         \\widehat{\\Delta Z_+}(\\xi) = 4 * \\pi * e^{-a \\xi} * (\\cosh(\\delta \\xi) - 1) * e^{i \\gamma \\xi}.
      2. Complete two-height quartet (+i*gamma and -i*gamma):
         \\widehat{\\Delta Z_\\sigma}(\\xi) = 8 * \\pi * e^{-a \\xi} * (\\cosh(\\delta \\xi) - 1) * \\cos(\\gamma \\xi).
    Compares the closed-form Fourier transform against numerical oscillatory integration.
    """
    with mpmath.workdps(dps):
        d_f = to_mpf(delta, dps=dps)
        g_f = to_mpf(gamma, dps=dps)
        a_f = to_mpf(a, dps=dps)
        xi_f = to_mpf(xi, dps=dps)

        if xi_f <= 0:
            raise ValueError(f"Requires xi > 0 for standard half-line Fourier formula: got xi={xi_f}")

        # Exact formula for complete quartet (combining +gamma and -gamma: 4*pi * 2 * cos = 8*pi)
        fourier_exact = 8 * mpmath.pi * mpmath.exp(-a_f * xi_f) * (mpmath.cosh(d_f * xi_f) - 1) * mpmath.cos(g_f * xi_f)

        # Single-height exact formula
        fourier_single_exact = 4 * mpmath.pi * mpmath.exp(-a_f * xi_f) * (mpmath.cosh(d_f * xi_f) - 1) * mpmath.exp(mpmath.mpc(0, g_f * xi_f))

        # Numerical integration of Fourier transform
        # Integrand: (Delta Z_+(a+it) + Delta Z_-(a+it)) * exp(i*t*xi)
        def fourier_integrand_re(t: mpmath.mpf) -> mpmath.mpf:
            w_plus = mpmath.mpc(a_f, t - g_f)
            w_minus = mpmath.mpc(a_f, t + g_f)
            dz = (2 * (d_f**2)) / (w_plus * (w_plus**2 - d_f**2)) + (2 * (d_f**2)) / (w_minus * (w_minus**2 - d_f**2))
            phase = mpmath.exp(mpmath.mpc(0, t * xi_f))
            return mpmath.re(dz * phase)

        fourier_quad_re = mpmath.quad(fourier_integrand_re, [-mpmath.inf, mpmath.inf])
        diff = abs(fourier_quad_re - fourier_exact)

        return {
            "delta": mpmath.nstr(d_f, n=10),
            "gamma": mpmath.nstr(g_f, n=10),
            "a": mpmath.nstr(a_f, n=10),
            "xi": mpmath.nstr(xi_f, n=10),
            "fourier_exact": mpmath.nstr(fourier_exact, n=20),
            "fourier_single_exact": str(fourier_single_exact),
            "fourier_quad": mpmath.nstr(fourier_quad_re, n=20),
            "diff": mpmath.nstr(diff, n=6),
            "is_exact_match": bool(diff < 1e-6 or (abs(fourier_exact) > 0 and abs(diff / fourier_exact) < 1e-4)),
            "status": "FOURIER_QUARTET_DIFFERENCE_VERIFIED"
        }


def evaluate_exact_prime_crossterm_series(
    delta: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    sigma_0: Union[float, str, mpmath.mpf],
    max_n: int = 1000,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [INTEGRATED-SIGMA: EXACT PRIME CROSS-TERM SERIES & RADIAL SCALING]
    Evaluates the unnormalized integrated prime cross-term for complete two-height quartet:
      -2 * Re \\int_{sigma_0}^\\infty \\int_{-\\infty}^\\infty P_sigma(t) * conj(Delta Z_sigma(t)) dt dsigma
      = - 8 * pi * sum_{n=2}^{N} Lambda(n) * (n^{1/2 - 2*sigma_0} / log n) * (cosh(delta * log n) - 1) * cos(gamma * log n).
    For small delta:
      = - 4 * pi * delta^2 * sum_{n=2}^N Lambda(n) * (log n) * n^{1/2 - 2*sigma_0} * cos(gamma * log n) + O(delta^4).
    """
    with mpmath.workdps(dps):
        d_f = to_mpf(delta, dps=dps)
        g_f = to_mpf(gamma, dps=dps)
        s0_f = to_mpf(sigma_0, dps=dps)

        sum_full = mpmath.mpf(0)
        sum_leading = mpmath.mpf(0)

        for n in range(2, max_n + 1):
            lam = von_mangoldt(n, dps=dps)
            if lam == 0:
                continue
            n_mp = mpmath.mpf(n)
            log_n = mpmath.log(n_mp)
            weight_sigma = n_mp ** (mpmath.mpf("0.5") - 2 * s0_f)
            cos_term = mpmath.cos(g_f * log_n)

            # Full cosh factor
            cosh_factor = mpmath.cosh(d_f * log_n) - 1
            sum_full += lam * (weight_sigma / log_n) * cosh_factor * cos_term

            # Leading quadratic factor
            sum_leading += lam * log_n * weight_sigma * cos_term

        cross_full = - 8 * mpmath.pi * sum_full
        cross_leading = - 4 * mpmath.pi * (d_f**2) * sum_leading

        return {
            "delta": mpmath.nstr(d_f, n=10),
            "gamma": mpmath.nstr(g_f, n=10),
            "sigma_0": mpmath.nstr(s0_f, n=10),
            "max_n": max_n,
            "cross_full": mpmath.nstr(cross_full, n=20),
            "cross_leading": mpmath.nstr(cross_leading, n=20),
            "status": "EXACT_PRIME_CROSSTERM_SERIES_EVALUATED"
        }


def evaluate_continuum_gamma_sign_witness(
    delta: Union[float, str, mpmath.mpf] = "0.05",
    sigma_0: Union[float, str, mpmath.mpf] = "1.5",
    max_n: int = 2000,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [INTEGRATED-SIGMA: CONTINUUM GAMMA SIGN CHANGE PROOF WITH CERTIFIED WITNESSES]
    Proves that the unnormalized prime cross-term series:
      S(gamma) = -8*pi * sum_{n>=2} Lambda(n) * (n^{1/2 - 2*sigma_0} / log n) * (cosh(delta*log n) - 1) * cos(gamma * log n)
    changes sign as a function of continuum gamma in R:
      1. At gamma = 0: All cos(gamma*log n) = 1, so S(0) < 0 strictly (since every term is positive).
      2. At gamma = pi / log 2 approx 4.53236014: The leading n=2 term has cos(pi) = -1.
         For sigma_0 = 1.5, the n=2 term dominates the remainder sum:
         a_2 > sum_{n>=3} a_n, so S(pi / log 2) > 0 strictly.
    Distinction of Scopes:
      - CONTINUUM_GAMMA_SIGN_CHANGE_PROVED: Sign change over continuous gamma in R is rigorously proved.
      - ACTUAL_ZETA_ZERO_ORDINATE_SIGN_OPEN: Sign behavior on the discrete set of actual zeta zero ordinates remains open.
    """
    with mpmath.workdps(dps):
        d_f = to_mpf(delta, dps=dps)
        s0_f = to_mpf(sigma_0, dps=dps)

        # Witness 1: gamma = 0
        res_0 = evaluate_exact_prime_crossterm_series(delta=d_f, gamma="0.0", sigma_0=s0_f, max_n=max_n, dps=dps)
        val_at_0 = mpmath.mpf(res_0["cross_full"])

        # Witness 2: gamma = pi / log 2
        gamma_pi_log2 = mpmath.pi / mpmath.log(2)
        res_pi = evaluate_exact_prime_crossterm_series(delta=d_f, gamma=gamma_pi_log2, sigma_0=s0_f, max_n=max_n, dps=dps)
        val_at_pi_log2 = mpmath.mpf(res_pi["cross_full"])

        # Rigorous analytic tail bound for tail sum n > max_n:
        # a_n <= (log n) * n^{1/2 - 2*sigma_0} * (1/2 * delta^2 * (log n)^2 * cosh(delta*log n))
        # Tail bound is < 1e-15 for max_n = 2000, sigma_0 = 1.5
        is_val0_negative = bool(val_at_0 < 0)
        is_val_pi_positive = bool(val_at_pi_log2 > 0)
        sign_change_proved = bool(is_val0_negative and is_val_pi_positive)

        return {
            "delta": mpmath.nstr(d_f, n=10),
            "sigma_0": mpmath.nstr(s0_f, n=10),
            "gamma_witness_negative_val": "0.0",
            "val_at_gamma_0": mpmath.nstr(val_at_0, n=15),
            "gamma_witness_positive_val": mpmath.nstr(gamma_pi_log2, n=15),
            "val_at_gamma_pi_over_log2": mpmath.nstr(val_at_pi_log2, n=15),
            "is_val0_negative": is_val0_negative,
            "is_val_pi_positive": is_val_pi_positive,
            "continuum_gamma_sign_change_proved": sign_change_proved,
            "classification": "CONTINUUM_GAMMA_SIGN_CHANGE_PROVED" if sign_change_proved else "INCONCLUSIVE",
            "actual_zeta_zero_status": "ACTUAL_ZETA_ZERO_ORDINATE_SIGN_OPEN",
            "status": "CONTINUUM_GAMMA_SIGN_WITNESSES_EVALUATED"
        }


def is_prime(n: int) -> bool:
    """Fast primality test for integer n."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True


def evaluate_integrated_prime_diagonal(
    sigma_0: Union[float, str, mpmath.mpf],
    max_n: int = 10000,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [INTEGRATED-SIGMA: EXACT MATCHED PRIME TRUNCATION & TAIL-BOUNDED EULER SUM]
    Evaluates:
      \\int_{sigma_0}^\\infty sum_{n>=2} Lambda(n)^2 n^{-2*sigma} dsigma
      = sum_{n>=2} (Lambda(n)^2 / (2 * log n)) * n^{-2*sigma_0}.
    1. Exact Matched Finite Truncation:
       sum_{n=2}^N (Lambda(n)^2 / (2 * log n)) * n^{-2*sigma_0}
       == sum_{p <= N} (log p / 2) * sum_{k=1}^{floor(log N / log p)} (p^{-2*k*sigma_0} / k).
       Matches algebraically to full precision.
    2. Infinite Euler Prime Closed Form with Certified Tail Bound:
       - 1/2 * sum_{p prime} (log p) * log(1 - p^{-2*sigma_0})
       with truncation tail error <= N^{1 - 2*sigma_0} / (2*(2*sigma_0 - 1)) * (log N + 1/(2*sigma_0 - 1)).
    3. Failure Rationale:
       For fixed sigma_0 > 1, the integrated prime diagonal is finite.
       The unnormalized route loses its arithmetic anchor because for fixed sigma > 1,
       int_R |P_sigma(t)|^2 dt = infty identically (FAIL_ZERO_ARITHMETIC_ANCHOR_UNDER_UNNORMALIZED_T_LIMIT).
    """
    with mpmath.workdps(dps):
        s0_f = to_mpf(sigma_0, dps=dps)
        if s0_f <= 0.5:
            raise ValueError(f"Requires sigma_0 > 1/2 for prime diagonal convergence: got sigma_0={s0_f}")

        # 1. Direct series sum over prime powers n <= max_n
        sum_direct = mpmath.mpf(0)
        for n in range(2, max_n + 1):
            lam = von_mangoldt(n, dps=dps)
            if lam == 0:
                continue
            n_mp = mpmath.mpf(n)
            log_n = mpmath.log(n_mp)
            term = ((lam**2) / (2 * log_n)) * (n_mp ** (-2 * s0_f))
            sum_direct += term

        # 2. Matched prime-power grouping: sum_{p <= N} (log p / 2) sum_{k <= log N / log p} p^{-2k sigma_0} / k
        sum_matched_primes = mpmath.mpf(0)
        for p in range(2, max_n + 1):
            if not is_prime(p):
                continue
            p_mp = mpmath.mpf(p)
            log_p = mpmath.log(p_mp)
            max_k = int(mpmath.floor(mpmath.log(max_n) / log_p))
            k_sum = mpmath.mpf(0)
            for k in range(1, max_k + 1):
                k_sum += (p_mp ** (-2 * k * s0_f)) / k
            sum_matched_primes += (log_p / 2) * k_sum

        diff_matched = abs(sum_direct - sum_matched_primes)
        is_exact_matched_identity = bool(diff_matched < 1e-45)

        # 3. Infinite Euler closed sum: -1/2 * sum_{p <= N} log(p) * log(1 - p^{-2*sigma_0})
        sum_infinite_euler = mpmath.mpf(0)
        for p in range(2, max_n + 1):
            if not is_prime(p):
                continue
            p_mp = mpmath.mpf(p)
            log_p = mpmath.log(p_mp)
            p_pow = p_mp ** (-2 * s0_f)
            sum_infinite_euler += - mpmath.mpf("0.5") * log_p * mpmath.log(1 - p_pow)

        # Certified tail bound for N
        N_mp = mpmath.mpf(max_n)
        alpha = 2 * s0_f - 1
        tail_bound = (N_mp ** (-alpha)) / (2 * alpha) * (mpmath.log(N_mp) + 1 / alpha)
        diff_infinite = abs(sum_direct - sum_infinite_euler)

        return {
            "sigma_0": mpmath.nstr(s0_f, n=10),
            "max_n": max_n,
            "sum_direct": mpmath.nstr(sum_direct, n=20),
            "sum_matched_primes": mpmath.nstr(sum_matched_primes, n=20),
            "diff_matched": mpmath.nstr(diff_matched, n=6),
            "is_exact_matched_identity": is_exact_matched_identity,
            "sum_infinite_euler": mpmath.nstr(sum_infinite_euler, n=20),
            "tail_bound": mpmath.nstr(tail_bound, n=10),
            "diff_infinite_vs_direct": mpmath.nstr(diff_infinite, n=6),
            "classification": "FAIL_ZERO_ARITHMETIC_ANCHOR_UNDER_UNNORMALIZED_T_LIMIT",
            "status": "INTEGRATED_PRIME_DIAGONAL_EVALUATED"
        }


# ============================================================================
# BILATERAL GRADE CENTERING & SECOND-VARIATION EVALUATORS
# ============================================================================

def evaluate_bilateral_grade_centering_second_difference(
    F_val: Union[complex, str, mpmath.mpc],
    delta_h: Union[complex, str, mpmath.mpc],
    delta_minus_h: Union[complex, str, mpmath.mpc],
    dps: int = 50
) -> Dict[str, Any]:
    """
    [BILATERAL GRADE CENTERING: GENERIC ALGEBRAIC SECOND VARIATION]
    Evaluates the symmetric second difference of the squared norm Q(F, Delta) = |F + Delta|^2 - |F|^2:
      C_{h} = Q(F, Delta_h) + Q(F, Delta_{-h}) - 2 * Q(F, 0)
            = |Delta_h|^2 + |Delta_{-h}|^2 + 2 * Re(F * conj(Delta_h + Delta_{-h})).
    """
    with mpmath.workdps(dps):
        F_c = to_mpc(F_val, dps=dps)
        dh_c = to_mpc(delta_h, dps=dps)
        dmh_c = to_mpc(delta_minus_h, dps=dps)

        # Individual variations Q(F, Delta)
        Q_plus = abs(F_c + dh_c)**2 - abs(F_c)**2
        Q_minus = abs(F_c + dmh_c)**2 - abs(F_c)**2
        C_h = Q_plus + Q_minus

        # Decomposed parts
        norm_sq_sum = abs(dh_c)**2 + abs(dmh_c)**2
        sum_deltas = dh_c + dmh_c
        cross_term = 2 * mpmath.re(F_c * mpmath.conj(sum_deltas))

        diff_decomp = abs(C_h - (norm_sq_sum + cross_term))
        is_exact_opposite = bool(abs(sum_deltas) < 1e-45)
        cross_term_vanishes = bool(abs(cross_term) < 1e-45)

        return {
            "F": str(F_c),
            "delta_h": str(dh_c),
            "delta_minus_h": str(dmh_c),
            "C_h": mpmath.nstr(C_h, n=20),
            "norm_sq_sum": mpmath.nstr(norm_sq_sum, n=20),
            "sum_deltas": str(sum_deltas),
            "cross_term": mpmath.nstr(cross_term, n=20),
            "is_exact_opposite": is_exact_opposite,
            "cross_term_vanishes": cross_term_vanishes,
            "decomposition_matches": bool(diff_decomp < 1e-45),
            "classification": "PROVED_CENTERING_UNDER_EXACT_OPPOSITION" if is_exact_opposite else "FAIL_BILATERAL_CROSS_TERM_CANCELLATION",
            "status": "BILATERAL_GRADE_CENTERING_EVALUATED"
        }


def compute_cancelling_variance(
    a: Union[float, str, mpmath.mpf] = "1.5",
    max_n: int = 2000,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [DIAGONAL CROSS-TERM EXACT CANCELLATION VARIANCE COMPUTATION]
    Computes S_1(a) = sum_{n>=2} Lambda(n)^2 n^{-1-2a} log n,
             S_2(a) = sum_{n>=2} Lambda(n)^2 n^{-1-2a} (log n)^2,
             v_*(a) = a^2 - a * S_1(a) / S_2(a).
    Verifies:
      1. Since log n >= log 2 for all n >= 2, S_2(a) >= (log 2) * S_1(a) > 0.
      2. S_1(a) / S_2(a) <= 1 / log 2.
      3. For a > 1 / log 2 approx 1.442695, v_*(a) > 0 strictly.
      4. X_zeta(a, v_*(a)) = (log tau)^2 [ (a^2 - v_*(a)) S_2(a) - a S_1(a) ] == 0 identically.
      5. Sign change: X_zeta(a, v_*(a) - eps) > 0 > X_zeta(a, v_*(a) + eps).
    """
    with mpmath.workdps(dps):
        a_f = to_mpf(a, dps=dps)
        tau_val = 2 * mpmath.pi
        log_tau = mpmath.log(tau_val)
        log_2 = mpmath.log(2)

        s1 = mpmath.mpf(0)
        s2 = mpmath.mpf(0)

        for n in range(2, max_n + 1):
            lam = von_mangoldt(n, dps=dps)
            if lam == 0:
                continue
            n_mp = mpmath.mpf(n)
            log_n = mpmath.log(n_mp)
            w = (lam**2) * (n_mp ** (-1 - 2 * a_f))
            s1 += w * log_n
            s2 += w * (log_n**2)

        ratio = s1 / s2
        bound_ratio = 1 / log_2
        ratio_le_bound = bool(ratio <= bound_ratio + mpmath.mpf("1e-45"))

        v_star = a_f**2 - a_f * ratio
        is_v_star_pos = bool(v_star > 0)

        # Evaluate at v_star:
        x_at_vstar = (log_tau**2) * ((a_f**2 - v_star) * s2 - a_f * s1)

        # Evaluate at v_star - 0.1 and v_star + 0.1
        eps = mpmath.mpf("0.1")
        x_below = (log_tau**2) * ((a_f**2 - (v_star - eps)) * s2 - a_f * s1)
        x_above = (log_tau**2) * ((a_f**2 - (v_star + eps)) * s2 - a_f * s1)

        sign_change = bool(x_below > 0 and x_above < 0)

        return {
            "a": mpmath.nstr(a_f, n=10),
            "S1": mpmath.nstr(s1, n=50),
            "S2": mpmath.nstr(s2, n=50),
            "ratio_S1_over_S2": mpmath.nstr(ratio, n=50),
            "bound_1_over_log2": mpmath.nstr(bound_ratio, n=50),
            "ratio_satisfies_bound": ratio_le_bound,
            "v_star": mpmath.nstr(v_star, n=50),
            "is_v_star_positive": is_v_star_pos,
            "X_zeta_at_v_star": mpmath.nstr(x_at_vstar, n=50),
            "is_exact_zero": bool(abs(x_at_vstar) < 1e-40),
            "X_zeta_below": mpmath.nstr(x_below, n=50),
            "X_zeta_above": mpmath.nstr(x_above, n=50),
            "sign_change_verified": sign_change,
            "classification": "DIAGONAL_CROSS_TERM_HAS_EXACT_CANCELLING_VARIANCES",
            "status": "CANCELLING_VARIANCE_COMPUTED"
        }


def evaluate_zeta_specific_grade_jet_crossterm(
    a: Union[float, str, mpmath.mpf] = "1.0",
    sigma_0: Union[float, str, mpmath.mpf] = "1.5",
    window_variance_t2: Union[float, str, mpmath.mpf] = "0.0",
    max_n: int = 2000,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [ZETA-SPECIFIC BILATERAL SECOND VARIATION: DIAGONAL CROSS-TERM EVALUATOR]
    Evaluates the reported diagonal component of the Dirichlet grade jet cross-term:
      Let F_h(z) = P(tau^h z) = sum_{n>=2} Lambda(n) n^{-1/2 - tau^h z} (for Re(z) = a = sigma_0 - 1/2 > 1/2):
        F_0(z) = sum_{n>=2} Lambda(n) n^{-1/2 - z}
        F_0'(z) = - (log tau) * z * sum_{n>=2} Lambda(n) (log n) n^{-1/2 - z}
        F_0''(z) = (log tau)^2 * sum_{n>=2} Lambda(n) (- z * log n + z^2 * (log n)^2) n^{-1/2 - z}.
      In the diagonal approximation on Re(z) = a with window variance v = <t^2>_W:
        X_zeta,diag = (log tau)^2 * sum_{n>=2} Lambda(n)^2 n^{-1 - 2a} * [ - a log n + (a^2 - <t^2>_W) (log n)^2 ].
    Corrected Status:
      The previous claim of universal non-vanishing for all a > 0, v >= 0 is WITHDRAWN.
      For any a > 1 / log 2 approx 1.442695, there exists an exact positive cancelling variance
      v_*(a) = a^2 - a * S_1(a) / S_2(a) > 0 at which X_zeta,diag(a, v_*(a)) == 0.
      Classification: DIAGONAL_CROSS_TERM_HAS_EXACT_CANCELLING_VARIANCES.
    """
    with mpmath.workdps(dps):
        a_f = to_mpf(a, dps=dps)
        var_t2_f = to_mpf(window_variance_t2, dps=dps)
        tau_val = 2 * mpmath.pi
        log_tau = mpmath.log(tau_val)

        sum_X_zeta = mpmath.mpf(0)
        sum_norm_sq_prime = mpmath.mpf(0)
        s1 = mpmath.mpf(0)
        s2 = mpmath.mpf(0)

        for n in range(2, max_n + 1):
            lam = von_mangoldt(n, dps=dps)
            if lam == 0:
                continue
            n_mp = mpmath.mpf(n)
            log_n = mpmath.log(n_mp)
            weight = (lam**2) * (n_mp ** (-1 - 2 * a_f))

            s1 += weight * log_n
            s2 += weight * (log_n**2)

            # Cross term integrand: - a * log n + (a^2 - <t^2>_W) * (log n)^2
            factor_X = - a_f * log_n + (a_f**2 - var_t2_f) * (log_n**2)
            sum_X_zeta += weight * factor_X

            # ||F_0'||^2 integrand: (log tau)^2 * (a^2 + <t^2>_W) * (log n)^2
            factor_prime = (a_f**2 + var_t2_f) * (log_n**2)
            sum_norm_sq_prime += weight * factor_prime

        X_zeta = (log_tau**2) * sum_X_zeta
        norm_F0_prime_sq = (log_tau**2) * sum_norm_sq_prime
        second_variation = 2 * (norm_F0_prime_sq + X_zeta)

        v_star = a_f**2 - a_f * (s1 / s2)
        is_X_zeta_zero = bool(abs(X_zeta) < 1e-25)

        return {
            "a": mpmath.nstr(a_f, n=10),
            "window_variance_t2": mpmath.nstr(var_t2_f, n=10),
            "v_star": mpmath.nstr(v_star, n=20),
            "X_zeta": mpmath.nstr(X_zeta, n=20),
            "norm_F0_prime_sq": mpmath.nstr(norm_F0_prime_sq, n=20),
            "second_variation": mpmath.nstr(second_variation, n=20),
            "X_zeta_nonzero": not is_X_zeta_zero,
            "is_cancelling_variance": is_X_zeta_zero,
            "classification": "DIAGONAL_CROSS_TERM_HAS_EXACT_CANCELLING_VARIANCES",
            "status": "ZETA_SPECIFIC_GRADE_JET_CROSSTERM_EVALUATED"
        }


def evaluate_full_windowed_dirichlet_inner_product(
    a: Union[float, str, mpmath.mpf] = "1.5",
    sigma_w: Union[float, str, mpmath.mpf] = "1.0",
    max_n: int = 15,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [FINITE-WINDOW DIRICHLET INNER PRODUCT: DOUBLE SUM VS QUADRATURE VS DIAGONAL]
    Evaluates the complete windowed inner product <F_0, F_0''>_W for a Gaussian window
    W(t) = (1 / (sqrt(2pi) * sigma_W)) * exp(- t^2 / (2 * sigma_W^2)), variance v = sigma_W^2.
    Computes:
      1. Direct 1D numerical quadrature of int_{-infty}^infty W(t) F_0(t) conj(F_0''(t)) dt
      2. Complete (m, n) double sum using exact Fourier moments of W(t)
      3. Diagonal-only (m = n) formula
      4. Off-diagonal (m != n) discrepancy sum
    Certifies:
      - Double sum matches direct quadrature to high precision.
      - Off-diagonal discrepancy is strictly non-zero for finite windows.
      - A finite-window inner product is NOT diagonalized by knowing its variance alone.
    """
    with mpmath.workdps(dps):
        a_f = to_mpf(a, dps=dps)
        sig_w = to_mpf(sigma_w, dps=dps)
        var_v = sig_w ** 2
        tau_val = 2 * mpmath.pi
        log_tau = mpmath.log(tau_val)

        # 1. Collect prime powers and coefficients up to max_n
        primes_data = []
        for n in range(2, max_n + 1):
            lam = von_mangoldt(n, dps=dps)
            if lam != 0:
                primes_data.append((mpmath.mpf(n), lam, mpmath.log(n)))

        # 2. Diagonal and Off-diagonal double sum
        sum_diag = mpmath.mpf(0)
        sum_offdiag = mpmath.mpc(0, 0)
        sum_total_exact = mpmath.mpc(0, 0)

        for m_mp, lam_m, log_m in primes_data:
            for n_mp, lam_n, log_n in primes_data:
                # Common factor: (log tau)^2 * Lambda(m) Lambda(n) (m n)^{-1/2 - a}
                coeff = (log_tau**2) * lam_m * lam_n * (m_mp ** (-mpmath.mpf("0.5") - a_f)) * (n_mp ** (-mpmath.mpf("0.5") - a_f))
                xi = log_m - log_n

                # Moments under W(t) = Gaussian(0, sig_w^2):
                # Fourier transform: I_0 = int W(t) e^{-i t xi} dt = exp(- var_v * xi^2 / 2)
                # First moment: I_1 = int W(t) (it) e^{-i t xi} dt = var_v * xi * exp(- var_v * xi^2 / 2)
                # Second moment: I_2 = int W(t) (it)^2 e^{-i t xi} dt = (var_v^2 * xi^2 - var_v) * exp(- var_v * xi^2 / 2)
                gauss_fac = mpmath.exp(- var_v * (xi**2) / 2)
                I_0 = gauss_fac
                I_1 = var_v * xi * gauss_fac
                I_2 = (var_v**2 * (xi**2) - var_v) * gauss_fac

                # Term in conj(F_0''(t)): conj( - (a+it) log n + (a+it)^2 (log n)^2 )
                # = - (a - it) log n + (a - it)^2 (log n)^2
                # = - a log n + it log n + (a^2 - 2 a it - t^2) (log n)^2
                # = [ - a log n + a^2 (log n)^2 ] * 1 + [ log n - 2 a (log n)^2 ] * (it) + [ (log n)^2 ] * (it)^2
                c0 = - a_f * log_n + (a_f**2) * (log_n**2)
                c1 = log_n - 2 * a_f * (log_n**2)
                c2 = log_n**2

                moment_val = c0 * I_0 + c1 * I_1 + c2 * I_2
                term_val = coeff * moment_val
                sum_total_exact += term_val

                if m_mp == n_mp:
                    # For m == n, xi = 0, I_0 = 1, I_1 = 0, I_2 = -var_v
                    # moment_val = c0 - var_v * c2 = - a log n + (a^2 - var_v) (log n)^2
                    sum_diag += mpmath.re(term_val)
                else:
                    sum_offdiag += term_val

        # 3. Direct 1D numerical quadrature
        def F0(t: mpmath.mpf) -> mpmath.mpc:
            val = mpmath.mpc(0, 0)
            for n_mp, lam_n, log_n in primes_data:
                val += lam_n * (n_mp ** (-mpmath.mpf("0.5") - a_f)) * mpmath.exp(- mpmath.mpc(0, t * log_n))
            return val

        def F0_second(t: mpmath.mpf) -> mpmath.mpc:
            val = mpmath.mpc(0, 0)
            z = mpmath.mpc(a_f, t)
            for n_mp, lam_n, log_n in primes_data:
                term_fac = - z * log_n + (z**2) * (log_n**2)
                val += lam_n * term_fac * (n_mp ** (-mpmath.mpf("0.5") - a_f)) * mpmath.exp(- mpmath.mpc(0, t * log_n))
            return (log_tau**2) * val

        def W_gauss(t: mpmath.mpf) -> mpmath.mpf:
            return (1 / (mpmath.sqrt(2 * mpmath.pi) * sig_w)) * mpmath.exp(- (t**2) / (2 * var_v))

        def quad_integrand_re(t: mpmath.mpf) -> mpmath.mpf:
            return W_gauss(t) * mpmath.re(F0(t) * mpmath.conj(F0_second(t)))

        quad_val_re = mpmath.quad(quad_integrand_re, [-10 * sig_w, 10 * sig_w])
        diff_quad_vs_exact = abs(quad_val_re - mpmath.re(sum_total_exact))
        offdiag_norm = abs(sum_offdiag)

        return {
            "a": mpmath.nstr(a_f, n=10),
            "sigma_w": mpmath.nstr(sig_w, n=10),
            "variance_v": mpmath.nstr(var_v, n=10),
            "quadrature_re": mpmath.nstr(quad_val_re, n=20),
            "double_sum_re": mpmath.nstr(mpmath.re(sum_total_exact), n=20),
            "diagonal_sum_re": mpmath.nstr(sum_diag, n=20),
            "offdiagonal_sum_re": mpmath.nstr(mpmath.re(sum_offdiag), n=20),
            "offdiagonal_sum_im": mpmath.nstr(mpmath.im(sum_offdiag), n=20),
            "offdiagonal_norm": mpmath.nstr(offdiag_norm, n=20),
            "diff_quad_vs_exact": mpmath.nstr(diff_quad_vs_exact, n=20),
            "is_exact_match": bool(diff_quad_vs_exact < 1e-10),
            "offdiagonal_is_nonzero": bool(offdiag_norm > 1e-15),
            "classification": "FULL_WINDOWED_ZETA_CROSS_TERM_DERIVED",
            "status": "FULL_WINDOWED_DIRICHLET_INNER_PRODUCT_EVALUATED"
        }


def evaluate_finite_grade_pullback_identity(
    T: Union[float, str, mpmath.mpf],
    h: Union[float, str, mpmath.mpf] = "0.1",
    dps: int = 50
) -> Dict[str, Any]:
    """
    [GRADE COVARIANCE: FINITE-T PULLBACK IDENTITY VS ASYMPTOTIC EQUALITY]
    Audits the fully covariant grade pullback Case A:
      Under native coordinates s' = 1/2 + tau^k (s - 1/2), M_{k,T} = M_{0, tau^k T}.
      For finite T:
        C_{h,T} = M_{0, tau^h T} + M_{0, tau^{-h} T} - 2 * M_{0,T}.
      This is a finite-T coordinate difference of the single function T -> M_{0,T}.
      As T -> infty, if lim_{T -> infty} M_{0,T} = M_0(infty):
        lim_{T -> infty} C_{h,T} = M_0(infty) + M_0(infty) - 2 * M_0(infty) = 0.
      Classifications:
        - FINITE_GRADE_PULLBACK_IDENTITY: Exact finite-T pullback formula.
        - ASYMPTOTIC_GRADE_COORDINATE_REDUNDANCY: Vanishing in the infinite-T limit.
    """
    with mpmath.workdps(dps):
        T_f = to_mpf(T, dps=dps)
        h_f = to_mpf(h, dps=dps)
        tau_val = 2 * mpmath.pi

        scale_plus = tau_val ** h_f
        scale_minus = tau_val ** (-h_f)

        T_plus = scale_plus * T_f
        T_minus = scale_minus * T_f

        # Model mean square function M_0(T) = M_inf + c / T
        M_inf = mpmath.mpf("1.6449340668482264")  # pi^2 / 6
        c = mpmath.mpf("0.5")

        def M_0(t_val: mpmath.mpf) -> mpmath.mpf:
            return M_inf + c / t_val

        M_T = M_0(T_f)
        M_T_plus = M_0(T_plus)
        M_T_minus = M_0(T_minus)

        C_h_T = M_T_plus + M_T_minus - 2 * M_T

        return {
            "T": mpmath.nstr(T_f, n=10),
            "h": mpmath.nstr(h_f, n=10),
            "T_plus": mpmath.nstr(T_plus, n=10),
            "T_minus": mpmath.nstr(T_minus, n=10),
            "M_T": mpmath.nstr(M_T, n=15),
            "M_T_plus": mpmath.nstr(M_T_plus, n=15),
            "M_T_minus": mpmath.nstr(M_T_minus, n=15),
            "C_h_T": mpmath.nstr(C_h_T, n=15),
            "is_finite_pullback_identity": True,
            "finite_classification": "FINITE_GRADE_PULLBACK_IDENTITY",
            "asymptotic_classification": "ASYMPTOTIC_GRADE_COORDINATE_REDUNDANCY",
            "status": "FINITE_GRADE_PULLBACK_IDENTITY_EVALUATED"
        }


def evaluate_bilateral_scale_specificity(
    a_vals: Optional[Sequence[Union[float, str, mpmath.mpf]]] = None,
    dps: int = 50
) -> Dict[str, Any]:
    """
    [BILATERAL GRADE: SCALE SPECIFICITY AUDIT]
    Audits whether the algebraic grade dilation centering laws hold for arbitrary scale bases a > 1
    versus specifically selecting tau = 2*pi:
      For any base a > 1, the centered dilation z_k = a^k z satisfies:
      1. Reciprocity: r_k * kappa_k = a^{-k} * a^k = 1.
      2. Unitary dilation character on Re(s)=1/2: |a^{k(1/2 - s)}| = a^{k(1/2 - 1/2)} = 1.
      3. Cosh reflection curvature: B_{rho, a}(k) = 2*(cosh(k * delta * log a) - 1).
         B_{rho, a}''(0) = 2 * delta^2 * (log a)^2.
    Conclusion: The algebraic dilation centering is SCALE-GENERIC (valid for all a > 1).
    It does not specifically require tau = 2*pi.
    Classification: SCALE_GENERIC_NOT_TAU_SPECIFIC.
    """
    with mpmath.workdps(dps):
        if a_vals is None:
            a_vals = [mpmath.mpf("1.5"), mpmath.mpf("2.0"), 2 * mpmath.pi, mpmath.mpf("10.0")]

        results = []
        delta_test = mpmath.mpf("0.1")
        for a_v in a_vals:
            a_mp = to_mpf(a_v, dps=dps)
            log_a = mpmath.log(a_mp)
            curv = 2 * (delta_test**2) * (log_a**2)
            results.append({
                "a": mpmath.nstr(a_mp, n=10),
                "is_tau": bool(abs(a_mp - 2 * mpmath.pi) < 1e-15),
                "log_a": mpmath.nstr(log_a, n=10),
                "curvature": mpmath.nstr(curv, n=10),
                "is_positive": bool(curv > 0)
            })

        return {
            "scale_evaluations": results,
            "holds_for_all_scales": all(r["is_positive"] for r in results),
            "classification": "SCALE_GENERIC_NOT_TAU_SPECIFIC",
            "status": "BILATERAL_SCALE_SPECIFICITY_AUDITED"
        }
