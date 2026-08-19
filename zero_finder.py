"""
zero_finder.py — Independent Critical-Line Zero Discovery

Discovers nontrivial zeros of the Riemann zeta function on the critical line
using real-valued Hardy Z-function Z(t) bracket scanning and certified root refinement.
Strictly adheres to DATA_PROVENANCE.md and SPEC.md §6:
- NEVER seeded from reference data.
- Refines roots to arbitrary precision (Preview: 35 dps, Audit: 80+ dps).
- Verifies residual |zeta(1/2 + i*gamma)| < epsilon before admitting root.
"""

from __future__ import annotations
import math
from typing import List, Tuple, Optional, Dict
import numpy as np
import mpmath
import math_core


def find_brackets(
    t_min: float,
    t_max: float,
    base_step: float = 0.08,
    dps: int = 25
) -> List[Tuple[float, float]]:
    """
    Scan the interval [t_min, t_max] to detect sign-change brackets [t_a, t_b] of Z(t).
    Uses density-adjusted step size to guard against closely spaced zeros.
    """
    brackets = []
    t = float(t_min)
    
    # Evaluate starting point
    z_prev = float(math_core.hardy_z(t, dps=dps))
    t_prev = t
    
    while t < t_max:
        # Near higher t, average zero spacing is 2*pi / ln(t / (2*pi))
        # Adjust step to guarantee at least 6-10 samples per expected zero
        if t > 10:
            avg_spacing = (2.0 * math.pi) / math.log(t / (2.0 * math.pi) + 1.1)
            step = min(base_step, max(0.015, avg_spacing / 10.0))
        else:
            step = base_step
            
        t_next = min(t + step, t_max)
        z_curr = float(math_core.hardy_z(t_next, dps=dps))
        
        # Check for sign change
        if z_prev * z_curr <= 0:
            brackets.append((t_prev, t_next))
        elif abs(z_curr) < 1e-4 and abs(z_prev) < 1e-4:
            # Possible near-tangent root, refine interval
            mid = 0.5 * (t_prev + t_next)
            z_mid = float(math_core.hardy_z(mid, dps=dps))
            if z_prev * z_mid <= 0:
                brackets.append((t_prev, mid))
            if z_mid * z_curr <= 0:
                brackets.append((mid, t_next))
                
        t_prev = t_next
        z_prev = z_curr
        t = t_next
        
    return brackets


def refine_zero(
    bracket: Tuple[float, float],
    dps: int = 35,
    max_residual: float = 1e-10
) -> Optional[mpmath.mpf]:
    """
    Refine a root bracket [t_a, t_b] using high-precision Brent/Illinois root finding.
    Verifies that |zeta(1/2 + i*gamma)| < max_residual.
    """
    t_a, t_b = bracket
    with mpmath.workdps(dps + 10):
        f = lambda t: math_core.hardy_z(t, dps=dps)
        try:
            # Find root with mpmath
            root = mpmath.findroot(f, (mpmath.mpf(str(t_a)), mpmath.mpf(str(t_b))), solver='anderson')
        except Exception:
            try:
                root = mpmath.findroot(f, (mpmath.mpf(str(t_a)), mpmath.mpf(str(t_b))), solver='bisect')
            except Exception:
                return None
                
        # Residual check on zeta(1/2 + i*root)
        s_root = mpmath.mpc('0.5', str(root))
        zeta_val = math_core.zeta_eval(s_root, dps=dps)
        if abs(zeta_val) <= mpmath.mpf(str(max_residual)):
            return root
        return None


def discover_zeros(
    t_min: float = 10.0,
    t_max: float = 55.0,
    dps: int = 35,
    max_residual: float = 1e-10
) -> List[mpmath.mpf]:
    """
    High-level zero discovery pipeline on [t_min, t_max].
    Discovers all zeros independently and returns sorted list of ordinates.
    """
    brackets = find_brackets(t_min, t_max, base_step=0.08, dps=min(dps, 30))
    zeros = []
    
    for bracket in brackets:
        root = refine_zero(bracket, dps=dps, max_residual=max_residual)
        if root is not None:
            # Deduplicate closely found roots
            if not any(abs(root - z) < 1e-5 for z in zeros):
                zeros.append(root)
                
    zeros.sort(key=lambda x: float(x))
    return zeros


def discover_zeros_float(
    t_min: float = 10.0,
    t_max: float = 55.0,
    dps: int = 35
) -> List[float]:
    """Convenience method returning float ordinates for plotting and UI."""
    return [float(z) for z in discover_zeros(t_min, t_max, dps=dps)]
