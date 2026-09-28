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

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def sieve_prime_powers_in_window(
    window: Tuple[float, float],
    grade: int,
    tau: float = 2.0 * math.pi
) -> List[Tuple[int, float, float]]:
    """
    Dynamically enumerate all prime-power stations x_{K, n} = a_K * n in window [A, B],
    where a_K = tau^K and n >= 2 is a prime power (n = p^m, m >= 1).
    Returns list of (n, x_{K, n}, Lambda(n) = log p).

    Eliminates hardcoded prime cutoffs, ensuring complete prime-power coverage
    for any window (including windows extending to 100 with primes 53, 59, ..., 97).
    """
    a_K = tau ** grade
    low, high = window
    n_min = max(2, int(math.ceil(low / a_K)))
    n_max = int(math.floor(high / a_K))
    if n_max < n_min:
        return []

    is_prime = [True] * (n_max + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(math.isqrt(n_max)) + 1):
        if is_prime[p]:
            for mult in range(p * p, n_max + 1, p):
                is_prime[mult] = False
    primes = [p for p in range(2, n_max + 1) if is_prime[p]]

    stations = []
    for p in primes:
        log_p = math.log(p)
        pow_p = p
        while pow_p <= n_max:
            if pow_p >= n_min:
                x_val = a_K * float(pow_p)
                stations.append((pow_p, x_val, log_p))
            pow_p *= p

    stations.sort(key=lambda item: item[0])
    return stations


# ==============================================================================
# 9. ARCHIMEDEAN KERNEL AND REFLECTED WEIL SPECTRAL MATRIX (TC CANDIDATE B)
# ==============================================================================

Z_CANONICAL_KERNEL = 0.4439938161680794378  # int_{-1}^1 exp(-1 / (1 - u^2)) du

# Gauss-Legendre quadrature weights and nodes for Fourier transform of bump kernel
_N_GL_KAPPA = 64
if NUMPY_AVAILABLE and np is not None:
    _y_gl_raw, _w_gl_raw = np.polynomial.legendre.leggauss(_N_GL_KAPPA)
    _y_gl = 0.5 * (_y_gl_raw + 1.0)
    _w_gl = 0.5 * _w_gl_raw
    _f_gl = np.zeros(_N_GL_KAPPA)
    for _i in range(_N_GL_KAPPA):
        _yk = _y_gl[_i]
        if _yk < 1.0:
            _f_gl[_i] = math.exp(-1.0 / (1.0 - _yk**2)) / Z_CANONICAL_KERNEL * _w_gl[_i]
else:
    _y_gl_raw = None
    _w_gl_raw = None
    _y_gl = None
    _w_gl = None
    _f_gl = None


_KAPPA_GL_CACHE: Dict[int, Tuple[np.ndarray, np.ndarray]] = {}


def kappa_hat_fast(xi: float) -> float:
    """Evaluate Fourier transform of canonical bump kappa(u) at frequency xi."""
    abs_xi = abs(float(xi))
    if not NUMPY_AVAILABLE or np is None:
        return float(2.0 * mpmath.quad(
            lambda y: mpmath.exp(-1.0 / (1.0 - y**2)) / Z_CANONICAL_KERNEL * mpmath.cos(xi * y),
            [0, 1]
        ))
    if abs_xi <= 15.0 and _f_gl is not None and _y_gl is not None:
        return float(2.0 * np.sum(_f_gl * np.cos(xi * _y_gl)))
    # For higher frequencies, scale quadrature nodes proportionally with oscillation frequency
    n_nodes = max(64, min(1024, int(4 * abs_xi)))
    if n_nodes not in _KAPPA_GL_CACHE:
        y_nodes, w_nodes = np.polynomial.legendre.leggauss(n_nodes)
        y_nodes = 0.5 * (y_nodes + 1.0)
        w_nodes = 0.5 * w_nodes
        f_vals = np.exp(-1.0 / (1.0 - y_nodes**2)) / Z_CANONICAL_KERNEL * w_nodes
        _KAPPA_GL_CACHE[n_nodes] = (y_nodes, f_vals)
    y_nodes, f_vals = _KAPPA_GL_CACHE[n_nodes]
    return float(2.0 * np.sum(f_vals * np.cos(xi * y_nodes)))


def archimedean_digamma_weight(t: float) -> float:
    """
    Archimedean weight omega(t) = Re digamma(1/4 + i*t/2) - log(pi).
    Governs the spectral density of the Archimedean place in the explicit formula.
    """
    try:
        import scipy.special
        val = scipy.special.digamma(complex(0.25, 0.5 * t))
        return float(val.real - math.log(math.pi))
    except Exception:
        pass
    if FLINT_AVAILABLE and acb is not None and arb is not None:
        _acb, _arb = acb, arb
        s = _acb(_arb(0.25), _arb(0.5 * t))
        return float(s.digamma().real) - math.log(math.pi)
    return float(mpmath.re(mpmath.digamma(mpmath.mpc(0.25, 0.5 * t))) - mpmath.log(mpmath.pi))


NORM_KAPPA_THIRD_DERIVATIVE_SQ = 16247.684292415849
NORM_KAPPA_SECOND_DERIVATIVE_SQ = 54.959873423948665
NORM_KAPPA_FIRST_DERIVATIVE_SQ = 2.077745668366741
NORM_KAPPA_SQ = 0.675116813009698



def _is_prime_power_exact(n: int) -> Tuple[bool, int, int]:
    """Return (True, p, m) if n = p^m for prime p and integer m >= 1, else (False, 0, 0)."""
    if n < 2:
        return False, 0, 0
    d = 2
    while d * d <= n:
        if n % d == 0:
            p = d
            temp = n
            m = 0
            while temp % p == 0:
                temp //= p
                m += 1
            if temp == 1:
                return True, p, m
            return False, 0, 0
        d += 1 if d == 2 else 2
    return True, n, 1


def _compute_C_h_position_quad(v: float, h: float, n_nodes: int = 64) -> float:
    """Evaluate position-space convolution C_h(v) = (psi_h * psi_h)(v) via Gauss-Legendre quadrature.

    Support is strictly contained in [-2h, 2h]. At v = 0, matches exact Sobolev norm:
      ||psi_h||_2^2 = h^-5 ||kappa''||_2^2 + 0.5 h^-3 ||kappa'||_2^2 + 0.0625 h^-1 ||kappa||_2^2.
    """
    abs_v = abs(float(v))
    if abs_v >= 2.0 * h:
        return 0.0
    norm_psi_h_sq = (
        h**(-5) * NORM_KAPPA_SECOND_DERIVATIVE_SQ +
        0.5 * h**(-3) * NORM_KAPPA_FIRST_DERIVATIVE_SQ +
        0.0625 * h**(-1) * NORM_KAPPA_SQ
    )
    if abs_v < 1e-13:
        return norm_psi_h_sq

    xi = abs_v / h
    y_min = -1.0 + xi
    y_max = 1.0
    nodes, weights = np.polynomial.legendre.leggauss(n_nodes)
    y = 0.5 * (y_max - y_min) * nodes + 0.5 * (y_max + y_min)
    w = 0.5 * (y_max - y_min) * weights

    def _d2kappa(val):
        om = 1.0 - val * val
        k = math.exp(-1.0 / om) / Z_CANONICAL_KERNEL
        return (-2.0 / (om * om) - 8.0 * val * val / (om * om * om) + 4.0 * val * val / (om * om * om * om)) * k

    def _kappa(val):
        om = 1.0 - val * val
        return math.exp(-1.0 / om) / Z_CANONICAL_KERNEL

    psi1 = np.array([h**(-3) * _d2kappa(val) - 0.25 * h**(-1) * _kappa(val) for val in y])
    psi2 = np.array([h**(-3) * _d2kappa(val - xi) - 0.25 * h**(-1) * _kappa(val - xi) for val in y])
    return h * float(np.sum(w * psi1 * psi2))


_C_TAB_CACHE: Dict[Tuple[bytes, str, int], np.ndarray] = {}


def _compute_C_tab_fast(v_arr: np.ndarray, h: float, n_nodes: int = 256) -> np.ndarray:
    """Vectorized position-space convolution table generator C_h(v) for array of v points."""
    if len(v_arr) > 0:
        v_bytes = np.ascontiguousarray(v_arr, dtype=np.float64).tobytes()
        c_key = (v_bytes, float(h).hex(), int(n_nodes))
        if c_key in _C_TAB_CACHE:
            return _C_TAB_CACHE[c_key].copy()

    norm_psi_h_sq = (
        h**(-5) * NORM_KAPPA_SECOND_DERIVATIVE_SQ +
        0.5 * h**(-3) * NORM_KAPPA_FIRST_DERIVATIVE_SQ +
        0.0625 * h**(-1) * NORM_KAPPA_SQ
    )
    res = np.zeros_like(v_arr, dtype=float)
    nodes, weights = np.polynomial.legendre.leggauss(n_nodes)

    for idx, v in enumerate(v_arr):
        abs_v = abs(float(v))
        if abs_v >= 2.0 * h:
            continue
        if abs_v < 1e-13:
            res[idx] = norm_psi_h_sq
            continue
        xi = abs_v / h
        y_min = -1.0 + xi
        y_max = 1.0
        scale = 0.5 * (y_max - y_min)
        shift = 0.5 * (y_max + y_min)
        y = scale * nodes + shift
        w = scale * weights

        om1 = 1.0 - y * y
        k1 = np.exp(-1.0 / om1) / Z_CANONICAL_KERNEL
        d2k1 = (-2.0 / (om1 * om1) - 8.0 * (y * y) / (om1**3) + 4.0 * (y * y) / (om1**4)) * k1
        psi1 = h**(-3) * d2k1 - 0.25 * h**(-1) * k1

        y2 = y - xi
        om2 = 1.0 - y2 * y2
        k2 = np.exp(-1.0 / om2) / Z_CANONICAL_KERNEL
        d2k2 = (-2.0 / (om2 * om2) - 8.0 * (y2 * y2) / (om2**3) + 4.0 * (y2 * y2) / (om2**4)) * k2
        psi2 = h**(-3) * d2k2 - 0.25 * h**(-1) * k2

        res[idx] = h * float(np.sum(w * psi1 * psi2))

    if len(v_arr) > 0:
        _C_TAB_CACHE[c_key] = res.copy()
    return res.copy()


class ArchimedeanKernelEvaluator:
    """
    High-precision Gauss-Legendre evaluator for the Archimedean convolution kernel:
    k_arch(v; h) = (1 / pi) int_0^infty omega(t) |A_h(it)|^2 cos(t * v) dt.
    """
    def __init__(self, h: float, N_t: Optional[int] = None, z_max: float = 16.0, U: Optional[float] = None):
        if h <= 0:
            raise ValueError(f"Bandwidth h must be strictly positive, got {h}")
        self.h = float(h)
        self.z_max = float(z_max)
        if U is not None:
            self.t_max = float(U)
            self.U = float(U)
        else:
            self.t_max = self.z_max / self.h
            self.U = self.t_max
        if N_t is None:
            self.N_t = max(600, int(50 * self.z_max))
        else:
            self.N_t = int(N_t)
        if NUMPY_AVAILABLE and np is not None:
            nodes_t, weights_t = np.polynomial.legendre.leggauss(self.N_t)
            self.nodes_t = 0.5 * self.t_max * (nodes_t + 1.0)
            self.weights_t = 0.5 * self.t_max * weights_t
            k_vals = np.array([kappa_hat_fast(t * self.h) for t in self.nodes_t])
            Ah_sq = ((self.nodes_t**2 + 0.25) * k_vals)**2
            omega_vals = np.array([archimedean_digamma_weight(t) for t in self.nodes_t])
            self.base = (self.weights_t * omega_vals * Ah_sq) / math.pi
        else:
            self.nodes_t = None

    def evaluate(self, v: float) -> float:
        if NUMPY_AVAILABLE and np is not None and self.nodes_t is not None:
            cos_v = np.cos(self.nodes_t * v)
            return float(np.sum(self.base * cos_v))
        return float(mpmath.quad(
            lambda t: archimedean_digamma_weight(t) * ((t**2 + 0.25) * kappa_hat_fast(t * self.h))**2 * mpmath.cos(t * v),
            [0, self.t_max]
        ) / mpmath.pi)

    def evaluate_matrix(
        self,
        stations_by_grade: Dict[int, List[Dict[str, Any]]],
        grades: List[int]
    ) -> List[List[float]]:
        """Vectorized evaluation of Archimedean Gram matrix across grades.

        Uses trigonometric factorization cos(t(u_b - u_a)) = cos(t u_a) cos(t u_b) + sin(t u_a) sin(t u_b)
        to evaluate in O((N_stations + r) * N_t) rather than O(N_stations^2 * N_t).
        """
        r = len(grades)
        if not (NUMPY_AVAILABLE and np is not None and self.nodes_t is not None):
            W = [[0.0] * r for _ in range(r)]
            for i, Ki in enumerate(grades):
                for j, Kj in enumerate(grades):
                    if j < i:
                        W[i][j] = W[j][i]
                        continue
                    entry = 0.0
                    for s_a in stations_by_grade.get(Ki, []):
                        for s_b in stations_by_grade.get(Kj, []):
                            v = s_b['t'] - s_a['t']
                            entry += s_a['weight_d'] * s_b['weight_d'] * self.evaluate(v)
                    W[i][j] = entry
                    if i != j:
                        W[j][i] = entry
            return W

        C_list = []
        S_list = []
        for K in grades:
            sts = stations_by_grade.get(K, [])
            if not sts:
                C_list.append(np.zeros_like(self.nodes_t))
                S_list.append(np.zeros_like(self.nodes_t))
                continue
            t_vals = np.array([s['t'] for s in sts])
            d_vals = np.array([s['weight_d'] for s in sts])
            angles = np.outer(self.nodes_t, t_vals)
            C_list.append(np.cos(angles) @ d_vals)
            S_list.append(np.sin(angles) @ d_vals)

        W = [[0.0] * r for _ in range(r)]
        for i in range(r):
            for j in range(r):
                if j < i:
                    W[i][j] = W[j][i]
                else:
                    val = float(np.sum(self.base * (C_list[i] * C_list[j] + S_list[i] * S_list[j])))
                    W[i][j] = val
                    W[j][i] = val
        return W
