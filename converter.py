"""
converter.py — Truncated Riemann Explicit Formula and Prime Reconstruction

Implements:
- Truncated prime power staircase J_N(x) using nontrivial zeros rho_n.
- Mobius inversion to reconstruct pi_N(x).
- Exact remainder integral via exponential integral E_1 series:
    int_x^infty du / [u(u^2 - 1) ln u] = sum_{k=1}^infty E_1(2k ln x)
- Fast cached single-zero perturbation updates Delta C(x) without full recomputation.
- Certified high-precision audit explicit formula evaluation (Arbitrary DPS).

Conforms to SPEC.md §5, §7, MATH_CONTRACT.md §12, and EXPERIMENT_PROTOCOL.md.

Branch Convention:
For complex zeros rho = beta + i*gamma and real x >= 2, we define
Li(x^rho) = Ei(rho * ln x), where ln x in R^+ is the principal real logarithm,
and Ei(w) uses the standard principal branch with branch cut along the negative
real axis (as computed by scipy.special.expi in preview and mpmath.ei in audit).
"""

from __future__ import annotations
import math
from typing import List, Tuple, Dict, Optional, Union, Any
import numpy as np
import scipy.special
import mpmath
import math_core

# Small lookup for Mobius function mu(m) for m = 1..50
_MOBIUS = [
    0, 1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0, -1, 1, 1, 0, -1, 0, -1, 0,
    1, 1, -1, 0, 0, 1, 0, 0, -1, -1, -1, 0, 1, 1, 0, 0, -1, 1, 1, 0, -1,
    -1, -1, 0, 0, 1, -1, 0, 0, 0
]


def mobius(m: int) -> int:
    """Return Mobius function mu(m)."""
    if 1 <= m < len(_MOBIUS):
        return _MOBIUS[m]
    factors = 0
    d = 2
    temp = m
    while d * d <= temp:
        if temp % d == 0:
            factors += 1
            temp //= d
            if temp % d == 0:
                return 0
        d += 1
    if temp > 1:
        factors += 1
    return -1 if (factors % 2 == 1) else 1


def riemann_remainder_integral_preview(x: float) -> float:
    """
    [PREVIEW PATH] Compute the tail integral:
    int_x^infty du / [u(u^2 - 1) ln u] = sum_{k=1}^infty E_1(2k ln x)
    using scipy.special.exp1 for fast float evaluation.
    """
    if x < 2.0:
        return 0.0
    ln_x = math.log(x)
    val = 0.0
    for k in range(1, 30):
        arg = 2.0 * k * ln_x
        term = float(scipy.special.exp1(arg))
        val += term
        if term < 1e-15:
            break
    return val


def riemann_remainder_integral(x: float) -> float:
    """Alias for riemann_remainder_integral_preview for backward compatibility."""
    return riemann_remainder_integral_preview(x)


def riemann_remainder_integral_audit(
    x: Union[str, float, int, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Certified high-precision evaluation of the remainder integral:
    int_x^infty du / [u(u^2 - 1) ln u] = sum_{k=1}^infty E_1(2k ln x)
    using mpmath.e1 at declared dps without float downcast.
    """
    with mpmath.workdps(dps + 15):
        x_mpf = math_core.to_mpf(x, dps=dps + 15)
        if x_mpf < 2:
            return mpmath.mpf('0')
        ln_x = mpmath.log(x_mpf)
        val = mpmath.mpf('0')
        threshold = mpmath.power(10, -(dps + 5))
        for k in range(1, 1000):
            arg = mpmath.mpf(2 * k) * ln_x
            term = mpmath.e1(arg)
            val += term
            if term < threshold:
                break
        return val


def riemann_explicit_j_audit(
    x: Union[str, float, int, mpmath.mpf],
    zeros: List[Union[complex, mpmath.mpc, str, float, Tuple[Any, Any]]],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Authoritative high-precision evaluation of J_N(x):
    J_N(x) = Li(x) - 2 * Re sum_{n=1}^N Li(x^{rho_n}) - ln 2 + int_x^infty du/[u(u^2-1)ln u]
    using branch convention Li(x^rho) = Ei(rho * ln x).
    """
    with mpmath.workdps(dps + 15):
        x_mpf = math_core.to_mpf(x, dps=dps + 15)
        if x_mpf < 2:
            return mpmath.mpf('0')
        ln_x = mpmath.log(x_mpf)
        
        # Li(x) = Ei(ln x) for x > 1
        li_x = mpmath.ei(ln_x)
        
        # Sum over zeros
        zero_sum = mpmath.mpf('0')
        for rho in zeros:
            if isinstance(rho, (int, float, mpmath.mpf)):
                rho_mpc = mpmath.mpc('0.5', str(rho))
            elif isinstance(rho, str) and not ('+' in rho or 'j' in rho.lower() or 'i' in rho.lower()):
                rho_mpc = mpmath.mpc('0.5', rho.strip())
            else:
                rho_mpc = math_core.to_mpc(rho, dps=dps + 15)
                
            # Li(x^rho) = Ei(rho * ln x)
            ei_val = mpmath.ei(rho_mpc * ln_x)
            zero_sum += 2 * mpmath.re(ei_val)
            
        rem = riemann_remainder_integral_audit(x_mpf, dps=dps + 15)
        j_val = li_x - zero_sum - mpmath.log(2) + rem
        return j_val



def riemann_explicit_pi_audit(
    x: Union[str, float, int, mpmath.mpf],
    zeros: List[Union[complex, mpmath.mpc, str, float, Tuple[Any, Any]]],
    dps: int = 80
) -> mpmath.mpf:
    """
    [AUDIT PATH] Authoritative high-precision evaluation of pi_N(x) via Mobius inversion:
    pi_N(x) = sum_{m >= 1, x^{1/m} >= 2} (mu(m) / m) * J_N(x^{1/m}).
    """
    with mpmath.workdps(dps + 15):
        x_mpf = math_core.to_mpf(x, dps=dps + 15)
        if x_mpf < 2:
            return mpmath.mpf('0')
        
        total_pi = mpmath.mpf('0')
        m = 1
        while True:
            xr = mpmath.power(x_mpf, mpmath.mpf(1) / m)
            if xr < 2:
                break
            mu_m = mobius(m)
            if mu_m != 0:
                j_m = riemann_explicit_j_audit(xr, zeros, dps=dps)
                total_pi += (mpmath.mpf(mu_m) / m) * j_m
            m += 1
        return total_pi


def compute_single_zero_contribution_vectorized(
    x_grid: np.ndarray,
    rho: complex
) -> np.ndarray:
    """
    Fast vectorized evaluation of single zero contribution C(x, rho) across x_grid.
    Uses scipy.special.expi for sub-millisecond preview calculation.
    """
    contrib = np.zeros_like(x_grid, dtype=np.float64)
    valid_mask = x_grid >= 2.0
    if not np.any(valid_mask):
        return contrib
        
    x_valid = x_grid[valid_mask]
    ln_x = np.log(x_valid)
    
    total_val = np.zeros_like(x_valid, dtype=np.float64)
    max_x = float(np.max(x_valid))
    
    m = 1
    while True:
        if max_x ** (1.0 / m) < 2.0:
            break
        mu_m = mobius(m)
        if mu_m != 0:
            sub_mask = (x_valid ** (1.0 / m)) >= 2.0
            if np.any(sub_mask):
                arg = rho * (ln_x[sub_mask] / m)
                ei_vals = scipy.special.expi(arg)
                term = (float(mu_m) / float(m)) * 2.0 * np.real(ei_vals)
                total_val[sub_mask] += term
        m += 1
        
    contrib[valid_mask] = total_val
    return contrib


def compute_single_zero_contribution(
    x_grid: np.ndarray,
    rho: complex | mpmath.mpc | float
) -> np.ndarray:
    """
    Compute total contribution of a single zero rho (and its conjugate pair)
    to reconstructed pi_N(x) across array x_grid (preview).
    """
    if isinstance(rho, (int, float)):
        rho_c = complex(0.5, float(rho))
    elif isinstance(rho, mpmath.mpc):
        rho_c = complex(float(rho.real), float(rho.imag))
    else:
        rho_c = complex(rho)
        
    return compute_single_zero_contribution_vectorized(x_grid, rho_c)


class PrimeReconstructionCache:
    """
    Manages baseline explicit formula evaluations and provides instantaneous
    perturbation updates when a single zero moves.
    """
    def __init__(self, x_grid: np.ndarray, baseline_zeros: List[complex]):
        self.x_grid = np.array(x_grid, dtype=np.float64)
        self.baseline_zeros = [complex(z) for z in baseline_zeros]
        self.n_zeros = len(baseline_zeros)
        
        # Precompute smooth base curve:
        # Base(x) = sum_m (mu(m)/m) * [ Li(x^(1/m)) - ln 2 + R(x^(1/m)) ]
        self.base_curve = np.zeros_like(self.x_grid, dtype=np.float64)
        valid_mask = self.x_grid >= 2.0
        x_valid = self.x_grid[valid_mask]
        
        if len(x_valid) > 0:
            ln_x = np.log(x_valid)
            base_val = np.zeros_like(x_valid, dtype=np.float64)
            max_x = float(np.max(x_valid))
            
            m = 1
            while True:
                if max_x ** (1.0 / m) < 2.0:
                    break
                mu_m = mobius(m)
                if mu_m != 0:
                    sub_mask = (x_valid ** (1.0 / m)) >= 2.0
                    if np.any(sub_mask):
                        xr = x_valid[sub_mask] ** (1.0 / m)
                        ln_xr = ln_x[sub_mask] / m
                        li_xr = scipy.special.expi(ln_xr)
                        rem = np.array([riemann_remainder_integral_preview(x_val) for x_val in xr])
                        j_base = li_xr - math.log(2.0) + rem
                        base_val[sub_mask] += (float(mu_m) / float(m)) * j_base
                m += 1
            self.base_curve[valid_mask] = base_val
            
        # Cache contribution of each baseline zero
        self.zero_contributions: List[np.ndarray] = []
        for rho in self.baseline_zeros:
            c = compute_single_zero_contribution_vectorized(self.x_grid, rho)
            self.zero_contributions.append(c)

    def reconstruct_pi_n(self, num_zeros: int) -> np.ndarray:
        """Reconstruct unperturbed pi_N(x) using the first num_zeros zeros."""
        n = min(num_zeros, self.n_zeros)
        res = self.base_curve.copy()
        for i in range(n):
            res -= self.zero_contributions[i]
        return res

    def reconstruct_pi_perturbed(
        self,
        num_zeros: int,
        perturbed_zero_idx: int,
        perturbed_rho: complex
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Reconstruct both clean pi_N(x) and perturbed pi_N_pert(x).
        Uses Delta C update for instantaneous response (<1ms).
        Returns (clean_pi, perturbed_pi).
        """
        clean_pi = self.reconstruct_pi_n(num_zeros)
        if perturbed_zero_idx < 0 or perturbed_zero_idx >= num_zeros:
            return clean_pi, clean_pi.copy()
            
        orig_contrib = self.zero_contributions[perturbed_zero_idx]
        new_contrib = compute_single_zero_contribution_vectorized(self.x_grid, complex(perturbed_rho))
        
        # Delta C = new - orig
        perturbed_pi = clean_pi - (new_contrib - orig_contrib)
        return clean_pi, perturbed_pi
