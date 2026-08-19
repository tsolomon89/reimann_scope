"""
cache.py — High-Performance In-Memory Cache for Sub-200ms Interactivity

Caches:
- Complex zeta traces for given transform parameters and sampling bounds
- Discovered zero lists
- Baseline explicit-formula prime reconstruction curves

Conforms to SPEC.md §8 (Responsiveness tiers: Preview < 200ms, Audit certified).
"""

from __future__ import annotations
import functools
import hashlib
from typing import Dict, Any, Tuple, Optional, List
import numpy as np
import transforms
import converter
import reference_data

# Global memory caches
_TRACE_CACHE: Dict[str, Tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
_ZERO_CACHE: Dict[str, List[float]] = {}
_CONVERTER_CACHE: Optional[converter.PrimeReconstructionCache] = None


def make_trace_key(
    mode_name: str,
    k: float,
    t0: float,
    dt: float,
    delta: float,
    A: float,
    B: float,
    C: float,
    D: float,
    A_delta: float,
    A_gamma: float,
    n_samples: int,
    dps: int
) -> str:
    """Generate deterministic hash key for trace evaluations."""
    raw = f"{mode_name}:{k:.6f}:{t0:.6f}:{dt:.6f}:{delta:.6f}:{A:.6f}:{B:.6f}:{C:.6f}:{D:.6f}:{A_delta:.6f}:{A_gamma:.6f}:{n_samples}:{dps}"
    return hashlib.md5(raw.encode()).hexdigest()


def get_cached_trace(
    transform_obj: transforms.BaseTransform,
    t0: float,
    dt: float,
    delta: float,
    n_samples: int = 300,
    dps: int = 35
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Retrieve or compute the trace (u_grid, s_coords, (re_w, im_w)).
    """
    # Extract params
    k = getattr(transform_obj, 'k', 0.0)
    A = getattr(transform_obj, 'A', 1.0)
    B = getattr(transform_obj, 'B', 1.0)
    C = getattr(transform_obj, 'C', 0.0)
    D = getattr(transform_obj, 'D', 0.0)
    A_delta = getattr(transform_obj, 'A_delta', 1.0)
    A_gamma = getattr(transform_obj, 'A_gamma', 1.0)

    key = make_trace_key(
        transform_obj.name, k, t0, dt, delta, A, B, C, D, A_delta, A_gamma, n_samples, dps
    )

    if key in _TRACE_CACHE:
        return _TRACE_CACHE[key]

    # Compute sampling path s(u)
    # u in [0, 1]
    u_vals = np.linspace(0.0, 1.0, n_samples)
    t_vals = t0 + u_vals * dt
    s_coords = np.array([complex(0.5 + delta, t) for t in t_vals], dtype=np.complex128)
    
    # Map domain coords if required by transform
    mapped_s = transform_obj.map_domain_array(s_coords)
    
    # Evaluate
    re_w, im_w = transform_obj.evaluate_array(mapped_s, dps=dps)
    
    result = (u_vals, mapped_s, re_w, im_w)
    # Keep cache bounded to 128 entries
    if len(_TRACE_CACHE) > 128:
        _TRACE_CACHE.pop(next(iter(_TRACE_CACHE)))
    _TRACE_CACHE[key] = result
    return result


def get_converter_cache(max_x: float = 60.0, n_points: int = 400) -> converter.PrimeReconstructionCache:
    """
    Retrieve or initialize the global PrimeReconstructionCache.
    Precomputes baseline curves from vendored reference zeros.
    """
    global _CONVERTER_CACHE
    if _CONVERTER_CACHE is not None and _CONVERTER_CACHE.x_grid[-1] == max_x and len(_CONVERTER_CACHE.x_grid) == n_points:
        return _CONVERTER_CACHE

    x_grid = np.linspace(2.0, max_x, n_points)
    ref_zeros = reference_data.load_reference_zeros()
    # Take first 30 zeros for baseline prime reconstruction
    baseline_zeros = [complex(0.5, float(s)) for s in ref_zeros[:30]]
    if not baseline_zeros:
        # Fallback if reference file not yet written
        baseline_zeros = [complex(0.5, 14.134725), complex(0.5, 21.022040), complex(0.5, 25.010858)]
        
    _CONVERTER_CACHE = converter.PrimeReconstructionCache(x_grid, baseline_zeros)
    return _CONVERTER_CACHE
