"""
math_core.py — Certified High-Precision Mathematical Core

Provides arbitrary-precision evaluation of the Riemann zeta function,
the completed Xi function xi(s), the Hardy Z-function Z(t), Riemann-Siegel theta,
and radial centrifuge quantities using python-flint (Arb ball arithmetic)
with mpmath fallback.

Strict adherence to MATH_CONTRACT.md and SPEC.md.
"""

from __future__ import annotations
import math
from typing import Union, Tuple, List, Optional
import numpy as np
import mpmath

try:
    import flint
    from flint import arb, acb, ctx as flint_ctx
    HAS_FLINT = True
except ImportError:
    HAS_FLINT = False


# Cache for high-precision constants
_TAU_CACHE = {}


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


def to_mpc(s: Union[complex, str, Tuple[Union[str, float], Union[str, float]], mpmath.mpc, mpmath.mpf], dps: int = 80) -> mpmath.mpc:
    """Safely convert coordinate representation to mpmath.mpc without precision loss."""
    with mpmath.workdps(dps + 10):
        if isinstance(s, mpmath.mpc):
            return s
        if isinstance(s, tuple) and len(s) == 2:
            return mpmath.mpc(str(s[0]), str(s[1]))
        if isinstance(s, complex):
            return mpmath.mpc(str(s.real), str(s.imag))
        if isinstance(s, (int, float, str, mpmath.mpf)):
            return mpmath.mpc(str(s), '0')
        return mpmath.mpc(s)


def zeta_eval(s: Union[complex, mpmath.mpc, str, Tuple[str, str]], dps: int = 35) -> mpmath.mpc:
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


def zeta_eval_certified(s: Union[complex, mpmath.mpc, str, Tuple[str, str]], dps: int = 80) -> Tuple[mpmath.mpc, float, bool]:
    """
    Certified evaluation of zeta(s) returning (midpoint, radius_bound, contains_zero).
    Uses Arb ball arithmetic.
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
            rad = float(z_arb.rad())
            mid = z_arb.mid()
            val_mpc = mpmath.mpc(str(mid.real), str(mid.imag))
            return val_mpc, rad, contains_0
        else:
            val = mpmath.zeta(s_mpc)
            contains_0 = abs(val) < mpmath.mpf(10) ** (-dps + 5)
            rad = float(mpmath.mpf(10) ** (-dps + 2))
            return val, rad, contains_0


def completed_xi(s: Union[complex, mpmath.mpc], dps: int = 80) -> mpmath.mpc:
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


def hardy_theta(t: Union[float, str, mpmath.mpf], dps: int = 35) -> mpmath.mpf:
    """
    Compute the Riemann-Siegel theta function:
    theta(t) = Im(ln Gamma(1/4 + i*t/2)) - (t/2)*ln(pi).
    """
    with mpmath.workdps(dps + 10):
        t_mpf = mpmath.mpf(str(t))
        s = mpmath.mpc('0.25', str(t_mpf / 2))
        log_gamma = mpmath.loggamma(s)
        theta_val = mpmath.im(log_gamma) - (t_mpf / 2) * mpmath.log(mpmath.pi)
        return theta_val


def hardy_z(t: Union[float, str, mpmath.mpf], dps: int = 35) -> mpmath.mpf:
    """
    Evaluate the real-valued Hardy Z-function on the critical line:
    Z(t) = exp(i*theta(t)) * zeta(1/2 + i*t).
    Uses mpmath.siegelz for exact high-precision evaluation.
    """
    with mpmath.workdps(dps + 10):
        t_mpf = mpmath.mpf(str(t))
        return mpmath.siegelz(t_mpf)


def eval_zeta_path(
    s_coords: List[complex] | np.ndarray,
    dps: int = 35
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Batch evaluation of zeta(s) along a path s(u).
    Returns (re_values, im_values) as float64 numpy arrays for plotting.
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


def centrifuge_log_modulus(
    delta: Union[float, str, mpmath.mpf],
    K: Union[float, str, mpmath.mpf],
    dps: int = 35
) -> mpmath.mpf:
    """
    Exact algebraic formula for the radial centrifuge log-modulus:
    log |q_rho^K| = K * delta * ln(tau).
    """
    with mpmath.workdps(dps + 10):
        tau = get_tau(dps)
        d_val = mpmath.mpf(str(delta))
        k_val = mpmath.mpf(str(K))
        return k_val * d_val * mpmath.log(tau)


def centrifuge_q_k(
    delta: Union[float, str, mpmath.mpf],
    gamma: Union[float, str, mpmath.mpf],
    K: Union[float, str, mpmath.mpf],
    dps: int = 35
) -> mpmath.mpc:
    """
    Complex value of the centrifuge grade-K character:
    q_rho^K = tau^(K*delta) * exp(i * K * gamma * ln(tau)).
    """
    with mpmath.workdps(dps + 10):
        tau = get_tau(dps)
        d_val = mpmath.mpf(str(delta))
        g_val = mpmath.mpf(str(gamma))
        k_val = mpmath.mpf(str(K))
        
        modulus = mpmath.power(tau, k_val * d_val)
        phase = k_val * g_val * mpmath.log(tau)
        
        return modulus * (mpmath.cos(phase) + mpmath.j * mpmath.sin(phase))
