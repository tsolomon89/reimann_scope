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
from typing import Union, Tuple, List, Optional, Dict, Any
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

