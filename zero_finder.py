"""
zero_finder.py — Independent Critical-Line and Transformed Zero Discovery

Discovers nontrivial zeros of the Riemann zeta function on the critical line
using real-valued Hardy Z-function Z(t) bracket scanning and certified root refinement,
as well as independent zero discovery for transformed functions along their image critical lines.

Strictly adheres to DATA_PROVENANCE.md, SPEC.md §6, and EXPERIMENT_PROTOCOL.md:
- NEVER seeded from reference data.
- Refines roots to arbitrary precision (Preview: 35 dps, Audit: 80+ dps).
- Verifies residual |zeta(1/2 + i*gamma)| < epsilon before admitting root.
- Uses precise terminology: discovered, refined, residual_verified, matched.
"""

from __future__ import annotations
import math
from typing import List, Tuple, Optional, Dict, Any, Union, Sequence

import mpmath
import math_core
import transforms


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
    t = t_min
    
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
    Verifies that residual |zeta(1/2 + i*gamma)| < max_residual.
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
    zeros: List[mpmath.mpf] = []
    
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


def generate_baseline_validation_report(
    t_min: float = 10.0,
    t_max: float = 60.0,
    dps: int = 35
) -> Dict[str, Any]:
    """Discover baseline zeros and validate against reference dataset."""
    import reference_data
    disc = discover_zeros(t_min, t_max, dps=dps)
    rep = reference_data.validate_zero_discovery(disc, t_min, t_max, dps=dps)
    rep["zeros_evaluated"] = rep.get("discovered_count", len(disc))
    return rep


# ==============================================================================
# TRANSFORMED ZERO DISCOVERY (Independent discovery of f(s) zeros)
# ==============================================================================

def get_image_critical_line_re(transform_obj: transforms.BaseTransform, dps: int = 80) -> Optional[mpmath.mpf]:
    """
    Determine the real coordinate Re(s') of the image critical line for a transform.
    For Transcendental Continuation Z_tau(s, k) across any bilateral grade k in R:
    Re(s_critical) = tau^k / 2.
    """
    with mpmath.workdps(dps + 10):
        if isinstance(transform_obj, transforms.TranscendentalContinuationTransform):
            scale_val = transform_obj.grade.numeric_scale(dps=dps)
            return scale_val / 2
        elif isinstance(transform_obj, (transforms.CameraTransform, transforms.CenteredCoordinateDilation, transforms.CenteredKernelTransform)):
            return mpmath.mpf('0.5')
        elif isinstance(transform_obj, transforms.HeightMicroscopeTransform):
            return mpmath.mpf('0.5') + math_core.to_mpf(transform_obj.delta_str, dps=dps)
        elif isinstance(transform_obj, transforms.OriginCoordinateDilation):
            tau = math_core.get_tau(dps)
            k_val = math_core.to_mpf(transform_obj.k_str, dps=dps)
            return mpmath.power(tau, k_val) / 2
        elif isinstance(transform_obj, transforms.ArgumentTransform):
            tau = math_core.get_tau(dps)
            k_val = math_core.to_mpf(transform_obj.k_str, dps=dps)
            return mpmath.mpf(1) / (2 * mpmath.power(tau, k_val))
        elif isinstance(transform_obj, transforms.KernelTransform):
            a_val = math_core.to_mpf(transform_obj.A_str, dps=dps)
            b_val = math_core.to_mpf(transform_obj.B_str, dps=dps)
            d_val = math_core.to_mpf(transform_obj.D_str, dps=dps)
            if abs(a_val * b_val) > 1e-12:
                return (mpmath.mpf('0.5') / a_val - d_val) / b_val
            return None
        elif isinstance(transform_obj, transforms.AnisotropicDeformation):
            return mpmath.mpf('0.5')
        return mpmath.mpf('0.5')


def discover_transformed_zeros(
    transform_obj: transforms.BaseTransform,
    t_min: float = 10.0,
    t_max: float = 55.0,
    dps: int = 35,
    max_residual: float = 1e-8,
    scan_step: float = 0.05
) -> List[mpmath.mpc]:
    """
    Independently discover zeros of the transformed function f(s) along its image
    critical line in the interval Im(s) in [t_min, t_max].

    Does NOT use mapped baseline zeros as seeds.
    Finds roots via local minima / sign tracking and refines them at declared dps.
    Returns list of discovered complex roots s_0 where |f(s_0)| < max_residual.
    """
    re_crit = get_image_critical_line_re(transform_obj, dps=dps)
    if re_crit is None:
        return []
        
    discovered_roots: List[mpmath.mpc] = []
    t = t_min

    
    with mpmath.workdps(dps + 10):
        # Scan along Re(s) = re_crit
        prev_s = mpmath.mpc(re_crit, t)
        prev_val = transform_obj.evaluate_function(prev_s, dps=dps)
        prev_mod = abs(prev_val)
        
        while t < t_max:
            t_next = min(t + scan_step, t_max)
            curr_s = mpmath.mpc(re_crit, t_next)
            curr_val = transform_obj.evaluate_function(curr_s, dps=dps)
            curr_mod = abs(curr_val)
            
            # Check for real part sign change or magnitude local minimum
            re_sign_change = (mpmath.re(prev_val) * mpmath.re(curr_val) <= 0)
            is_near_zero = (curr_mod < 0.2 and prev_mod < 0.2)
            
            if re_sign_change or is_near_zero:
                # Bracket candidate found; refine using mpmath findroot
                try:
                    def obj_func(im_val):
                        s_eval = mpmath.mpc(re_crit, im_val)
                        return mpmath.re(transform_obj.evaluate_function(s_eval, dps=dps))
                        
                    refined_im = mpmath.findroot(obj_func, (mpmath.mpf(str(t)), mpmath.mpf(str(t_next))), solver='anderson')
                    candidate_s = mpmath.mpc(re_crit, refined_im)
                    residual = abs(transform_obj.evaluate_function(candidate_s, dps=dps))
                    
                    if residual <= mpmath.mpf(str(max_residual)):
                        if not any(abs(candidate_s - r) < 1e-4 for r in discovered_roots):
                            discovered_roots.append(candidate_s)
                except Exception:
                    pass
                    
            t = t_next
            prev_val = curr_val
            prev_mod = curr_mod
            
    discovered_roots.sort(key=lambda s: float(s.imag))
    return discovered_roots


def compare_discovered_vs_predicted_zeros(
    transform_obj: transforms.BaseTransform,
    discovered_zeros: Sequence[Union[complex, mpmath.mpc]],
    baseline_zeros: Sequence[Union[float, str, mpmath.mpf, complex]],
    tolerance: float = 1e-5,
    dps: int = 80
) -> Dict[str, Any]:

    """
    Compare independently discovered transformed zeros against algebraically
    predicted mapped zeros rho' = transform_obj.map_zero_mpc(rho).
    """
    with mpmath.workdps(dps + 10):
        predicted_zeros = []
        for b in baseline_zeros:
            if isinstance(b, (float, str, mpmath.mpf)):
                rho_b = mpmath.mpc('0.5', str(b))
            else:
                rho_b = math_core.to_mpc(b, dps=dps)
            pred = transform_obj.map_zero_mpc(rho_b, dps=dps)
            predicted_zeros.append(pred)
            
        matched = []
        unmatched_disc = []
        unmatched_pred = list(predicted_zeros)
        
        for disc in discovered_zeros:
            closest_pred = None
            closest_dist = mpmath.mpf('inf')
            for p in unmatched_pred:
                dist = abs(disc - p)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_pred = p
            if closest_dist <= mpmath.mpf(str(tolerance)) and closest_pred is not None:
                matched.append((disc, closest_pred, closest_dist))
                unmatched_pred.remove(closest_pred)
            else:
                unmatched_disc.append(disc)
                
        diffs = [p[2] for p in matched]
        max_diff = max(diffs) if diffs else mpmath.mpf('0')
        rms_diff = mpmath.sqrt(sum(d*d for d in diffs) / len(diffs)) if diffs else mpmath.mpf('0')
        
        return {
            "discovered_count": len(discovered_zeros),
            "predicted_count": len(predicted_zeros),
            "matched_count": len(matched),
            "max_difference": str(max_diff),
            "rms_difference": str(rms_diff),
            "unmatched_discovered": [str(d) for d in unmatched_disc],
            "unmatched_predicted": [str(p) for p in unmatched_pred],
            "passed": len(unmatched_disc) == 0 and len(matched) > 0 and max_diff <= mpmath.mpf(str(tolerance))
        }
