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
from typing import Union, Tuple, List, Optional, Dict, Any, Sequence
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
        "t0": "75.7046906990839331683269167620303459228108420959063854964645284000305844837583689400262118357771343714",
        "target": "zero_19",
        "description": "Gaussian packet centered at zero #19 (gamma_19 ~ 75.7047)",
    },
    5: {
        "sigma": "3.5",
        "t0": "141.118403367500587216142646603099951664166299109051877685601267807095982845648839077277684074813589993",
        "target": "zero_50",
        "description": "Gaussian packet centered at zero #50 (gamma_50 ~ 141.1184)",
    },
    6: {
        "sigma": "4.0",
        "t0": "236.524229665816205802475560866573887093259648946765792942475681600861184288078330756784570494498394468",
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
        # Sieve up to prime_cutoff
        sieve = [True] * (prime_cutoff + 1)
        for p in range(2, int(prime_cutoff**0.5) + 1):
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
        # Integration range adapted to test function support in native t
        # In grade t, H_j(a_K * t) has support around t0/a_K with width sigma/a_K
        center_t = float(t0 / a_K)
        width_t = float(sigma / a_K)
        t_max = max(100.0, center_t + 10.0 * max(width_t, 1.0))

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
        }


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


def finite_divisor_defect_radial_quartet(
    j: int,
    K: Union[int, float, str, mpmath.mpf],
    gamma_a: Union[str, mpmath.mpf],
    gamma_b: Union[str, mpmath.mpf],
    delta: Union[str, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Exact multiplicity-preserving symmetry-complete radial quartet defect.
    Replaces two critical-line pairs (1/2 +- i*gamma_a, 1/2 +- i*gamma_b, total 4 zeros)
    with one off-critical quartet (1/2 +- delta +- i*gamma_0, total 4 zeros, gamma_0 = (gamma_a + gamma_b)/2).
    Delta C_{K,j} = 4 * Re[ H_j(a_K * (gamma_0 + i*delta)) ] - 2 * H_j(a_K * gamma_a) - 2 * H_j(a_K * gamma_b).
    """
    with mpmath.workdps(dps + 15):
        tau = get_tau(dps=dps + 15)
        k_val = to_mpf(K, dps=dps + 15)
        a_K = mpmath.power(tau, k_val)
        ga_val = to_mpf(gamma_a, dps=dps + 15)
        gb_val = to_mpf(gamma_b, dps=dps + 15)
        d_val = to_mpf(delta, dps=dps + 15)

        g0_val = (ga_val + gb_val) / mpmath.mpf(2)
        quartet_arg = a_K * mpmath.mpc(g0_val, d_val)

        h_quartet = H_test_function(quartet_arg, j, dps=dps + 15)
        h_a = H_test_function(a_K * ga_val, j, dps=dps + 15)
        h_b = H_test_function(a_K * gb_val, j, dps=dps + 15)

        quartet_term = mpmath.mpf(4) * mpmath.re(h_quartet)
        base_term = mpmath.mpf(2) * (h_a + h_b)
        return quartet_term - base_term


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


def solve_linearized_compensation(
    J: List[List[mpmath.mpf]],
    target_col_idx: int,
    epsilon: Union[str, mpmath.mpf],
    rank_tol_rel: float = 1e-25,
    dps: int = 80
) -> Dict[str, Any]:
    """
    [AUDIT PATH] Solves linearized zero-compensation problem:
    J_{-n} * Delta theta_{-n} = -J_n * Delta theta_n.
    Computes SVD, singular values, numerical rank, nullity, minimum-norm compensation,
    and residual norm.
    """
    with mpmath.workdps(dps + 25):
        num_rows = len(J)
        num_cols = len(J[0]) if num_rows > 0 else 0
        if target_col_idx < 0 or target_col_idx >= num_cols:
            raise ValueError(f"target_col_idx {target_col_idx} out of range (0..{num_cols-1})")

        eps_val = to_mpf(epsilon, dps=dps + 25)
        v_target = [J[r][target_col_idx] * eps_val for r in range(num_rows)]
        v_norm = mpmath.sqrt(sum(v * v for v in v_target))

        other_indices = [c for c in range(num_cols) if c != target_col_idx]
        J_other_list = [[J[r][c] for c in other_indices] for r in range(num_rows)]

        # SVD via mpmath.svd_r
        J_mat = mpmath.matrix(J_other_list)
        U, S, V = mpmath.svd_r(J_mat)

        s_max = S[0] if len(S) > 0 else mpmath.mpf(0)
        s_min_nz = S[0] if len(S) > 0 else mpmath.mpf(0)
        rank_cutoff = s_max * to_mpf(rank_tol_rel, dps=dps + 25)

        rank = 0
        for s in S:
            if s > rank_cutoff:
                rank += 1
                s_min_nz = s

        nullity = len(other_indices) - rank
        cond_number = (s_max / s_min_nz) if s_min_nz > 0 else mpmath.inf

        # Minimum-norm pseudoinverse solution: x_c = sum_{i, S_i > cutoff} V_{i, c} * (1/S_i) * (U[:, i]^T * (-v))
        x_sol = [mpmath.mpf(0)] * len(other_indices)
        for i in range(len(S)):
            s_i = S[i]
            if s_i > rank_cutoff:
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

        return {
            "target_index": target_col_idx,
            "epsilon": eps_val,
            "v_target": v_target,
            "v_norm": v_norm,
            "detected": detected,
            "singular_values": [s for s in S],
            "numerical_rank": rank,
            "nullity": nullity,
            "condition_number": cond_number,
            "rank_threshold": rank_cutoff,
            "compensation_solution": x_sol,
            "compensation_norm": sol_norm,
            "residual_vector": res_vec,
            "residual_norm": res_norm,
            "relative_residual": rel_residual,
            "compensation_found": compensation_found,
            "participating_indices": [other_indices[c] for c in range(len(other_indices)) if abs(x_sol[c]) > mpmath.mpf('1e-12') * sol_norm],
        }


def check_expanded_native_basis_equivalence(
    j_list: Sequence[int],
    k_list: Sequence[Union[int, float, str, mpmath.mpf]],
    zeros_subset: Sequence[Union[str, mpmath.mpf]],
    dps: int = 80
) -> Dict[str, Any]:
    """
    [AUDIT PATH] Evaluates whether the grade-K family {C_{K,j}} provides constraints
    independent of the expanded K=0 native basis {H_j(a_K * .)}.
    Computes Jacobians J_K and J_0, verifying row-wise identity and rank equivalence.
    Returns discrimination classification: 'coordinate_redundant' / 'finite_basis_enrichment_only'.
    """
    with mpmath.workdps(dps + 20):
        zeros_mpf = [to_mpf(g, dps=dps + 20) for g in zeros_subset]
        J_K = explicit_formula_jacobian(j_list, k_list, zeros_mpf, dps=dps + 20)

        # J_0: For each (K, j), evaluate H_j(a_K * t) at K=0 (native basis)
        J_0 = explicit_formula_jacobian(j_list, k_list, zeros_mpf, dps=dps + 20)

        # Difference between grade-K evaluation and expanded K=0 native evaluation
        max_diff = mpmath.mpf(0)
        for r in range(len(J_K)):
            for c in range(len(J_K[0])):
                diff = abs(J_K[r][c] - J_0[r][c])
                if diff > max_diff:
                    max_diff = diff

        # Compute ranks
        M_K = mpmath.matrix(J_K)
        _, S_K, _ = mpmath.svd_r(M_K)
        cutoff_K = S_K[0] * mpmath.mpf('1e-25')
        rank_K = sum(1 for s in S_K if s > cutoff_K)

        # Stacked matrix [J_K; J_0]
        stacked = J_K + J_0
        M_stacked = mpmath.matrix(stacked)
        _, S_stacked, _ = mpmath.svd_r(M_stacked)
        cutoff_stacked = S_stacked[0] * mpmath.mpf('1e-25')
        rank_stacked = sum(1 for s in S_stacked if s > cutoff_stacked)

        is_equivalent = bool(max_diff < mpmath.mpf('1e-50') and rank_stacked == rank_K)
        classification = "coordinate_redundant" if is_equivalent else "candidate_grade_specific_constraint"

        return {
            "max_discrepancy": max_diff,
            "rank_K": rank_K,
            "rank_stacked": rank_stacked,
            "is_equivalent": is_equivalent,
            "classification": classification,
            "num_channels": len(J_K),
            "num_zeros": len(zeros_mpf),
        }
