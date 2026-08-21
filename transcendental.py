"""
Transcendental Continuation Core Mathematical Module for Riemann Scope.

Implements the canonical mathematical framework defined in:
- docs/TRANSCENDENTAL_CONTINUATION.md
- docs/MATH_CONTRACT.md
- docs/CROSS_HEIGHT_COHERENCE.md
- docs/RESEARCH_HYPOTHESIS.md
"""

from __future__ import annotations

import fractions
import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import mpmath

import math_core


# ==============================================================================
# 1. GRADE TAXONOMY AND SCALE TYPES
# ==============================================================================

class BaseGrade:
    """Abstract base class for transcendental continuation scale grades."""
    
    @property
    def semantic_type(self) -> str:
        raise NotImplementedError
        
    def numeric_scale(self, dps: int = 80) -> mpmath.mpf:
        """Evaluate numeric scale factor A > 0 at specified precision."""
        raise NotImplementedError
        
    def symbolic_expression(self) -> str:
        """Return exact symbolic expression (e.g. 'tau^2', 'tau^(-3)', 'tau^(1/2)')."""
        raise NotImplementedError
        
    def display_label(self) -> str:
        """Human-readable label for UI and reports."""
        raise NotImplementedError
        
    def inverse_grade(self) -> BaseGrade:
        """Return the reciprocal grade satisfying scale(inverse) = 1 / scale(self)."""
        raise NotImplementedError


@dataclass(frozen=True)
class IntegerTauGrade(BaseGrade):
    """
    Canonical bilateral integer grade: K in Z.
    Scale A_K = tau^K.
    """
    K: int

    @property
    def semantic_type(self) -> str:
        return "integer_tau"

    def numeric_scale(self, dps: int = 80) -> mpmath.mpf:
        with mpmath.workdps(dps + 15):
            tau = math_core.get_tau(dps=dps + 15)
            return mpmath.power(tau, self.K)

    def symbolic_expression(self) -> str:
        if self.K == 0:
            return "tau^0"
        elif self.K == 1:
            return "tau"
        elif self.K > 1:
            return f"tau^{self.K}"
        else:
            return f"tau^({self.K})"

    def display_label(self) -> str:
        if self.K == 0:
            return "K = 0 (Native Slice, A = 1)"
        return f"Integer Grade K = {self.K} (A = {self.symbolic_expression()})"

    def inverse_grade(self) -> IntegerTauGrade:
        return IntegerTauGrade(K=-self.K)


@dataclass(frozen=True)
class RationalTauGrade(BaseGrade):
    """
    Rational root grade: q = n/d in Q.
    Scale A_q = tau^q.
    """
    fraction: fractions.Fraction

    @classmethod
    def from_str(cls, s: str) -> RationalTauGrade:
        return cls(fractions.Fraction(s.strip()))

    @property
    def semantic_type(self) -> str:
        return "rational_tau"

    def numeric_scale(self, dps: int = 80) -> mpmath.mpf:
        with mpmath.workdps(dps + 15):
            tau = math_core.get_tau(dps=dps + 15)
            q_mpf = mpmath.mpf(self.fraction.numerator) / mpmath.mpf(self.fraction.denominator)
            return mpmath.power(tau, q_mpf)

    def symbolic_expression(self) -> str:
        if self.fraction.denominator == 1:
            return f"tau^{self.fraction.numerator}"
        return f"tau^({self.fraction.numerator}/{self.fraction.denominator})"

    def display_label(self) -> str:
        return f"Rational Grade q = {self.fraction} (A = {self.symbolic_expression()})"

    def inverse_grade(self) -> RationalTauGrade:
        return RationalTauGrade(fraction=-self.fraction)


@dataclass(frozen=True)
class ContinuousGrade(BaseGrade):
    """
    Continuous real grade: k in R.
    Scale a(k) = tau^k.
    """
    k_str: str

    @classmethod
    def from_value(cls, val: Union[str, float, int, mpmath.mpf]) -> ContinuousGrade:
        return cls(k_str=str(val).strip())

    @property
    def semantic_type(self) -> str:
        return "continuous_tau"

    def numeric_scale(self, dps: int = 80) -> mpmath.mpf:
        with mpmath.workdps(dps + 15):
            tau = math_core.get_tau(dps=dps + 15)
            k_mpf = math_core.to_mpf(self.k_str, dps=dps + 15)
            return mpmath.power(tau, k_mpf)

    def symbolic_expression(self) -> str:
        return f"tau^({self.k_str})"

    def display_label(self) -> str:
        return f"Continuous Grade k = {self.k_str} (A = {self.symbolic_expression()})"

    def inverse_grade(self) -> ContinuousGrade:
        with mpmath.workdps(80):
            k_mpf = math_core.to_mpf(self.k_str, dps=80)
            neg_k = -k_mpf
            neg_k_str = mpmath.nstr(neg_k, n=15)
            return ContinuousGrade(k_str=neg_k_str)


@dataclass(frozen=True)
class GenericScale(BaseGrade):
    """
    Generic scale factor A > 0 with optional base b > 1 (e.g. b = e, 10, etc.).
    """
    A_str: str
    base_str: Optional[str] = None

    @property
    def semantic_type(self) -> str:
        return "generic_scale"

    def numeric_scale(self, dps: int = 80) -> mpmath.mpf:
        return math_core.to_mpf(self.A_str, dps=dps)

    def symbolic_expression(self) -> str:
        if self.base_str:
            return f"{self.base_str}^k"
        return f"A={self.A_str}"

    def display_label(self) -> str:
        if self.base_str:
            return f"Generic Base ({self.base_str}), Scale = {self.A_str}"
        return f"Generic Scale A = {self.A_str}"

    def inverse_grade(self) -> GenericScale:
        with mpmath.workdps(120):
            a_mpf = math_core.to_mpf(self.A_str, dps=120)
            inv_a = mpmath.mpf(1) / a_mpf
            return GenericScale(A_str=mpmath.nstr(inv_a, n=100), base_str=self.base_str)


def parse_grade(
    grade_input: Union[int, float, str, fractions.Fraction, BaseGrade],
    grade_type: str = "auto"
) -> BaseGrade:
    """
    Parse a grade input into an explicit BaseGrade instance.
    Supported types: 'integer', 'rational', 'continuous', 'generic', or 'auto'.
    """
    if isinstance(grade_input, BaseGrade):
        return grade_input

    s = str(grade_input).strip()
    
    if grade_type == "integer" or (grade_type == "auto" and (isinstance(grade_input, int) or (s.lstrip('-+').isdigit()))):
        return IntegerTauGrade(K=int(s))
        
    if grade_type == "rational" or (grade_type == "auto" and ('/' in s)):
        try:
            return RationalTauGrade.from_str(s)
        except Exception:
            pass
            
    if grade_type == "generic":
        return GenericScale(A_str=s)
        
    return ContinuousGrade.from_value(s)


# ==============================================================================
# 2. TRANSCENDENTAL EXTENDED DOMAIN FUNCTIONS
# ==============================================================================

def evaluate_extended_zeta(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    grade: Union[BaseGrade, str, int, float] = 0,
    dps: int = 80
) -> mpmath.mpc:
    """
    Evaluate the transcendental continuation function Z_tau(s, k) = zeta(tau^(-k) * s).
    At k = 0, identically Z_tau(s, 0) = zeta(s).
    """
    with mpmath.workdps(dps + 15):
        s_mpc = math_core.to_mpc(s, dps=dps + 15)
        g_obj = parse_grade(grade) if not isinstance(grade, BaseGrade) else grade
        scale_A = g_obj.numeric_scale(dps=dps + 15)
        
        # s_native = s / scale_A = tau^(-k) * s
        s_native = s_mpc / scale_A
        return math_core.zeta_eval(s_native, dps=dps)


def evaluate_extended_xi(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    grade: Union[BaseGrade, str, int, float] = 0,
    dps: int = 80
) -> mpmath.mpc:
    """
    Evaluate the completed xi function under transcendental continuation:
    X_tau(s, k) = xi(tau^(-k) * s).
    """
    with mpmath.workdps(dps + 15):
        s_mpc = math_core.to_mpc(s, dps=dps + 15)
        g_obj = parse_grade(grade) if not isinstance(grade, BaseGrade) else grade
        scale_A = g_obj.numeric_scale(dps=dps + 15)
        
        s_native = s_mpc / scale_A
        return math_core.completed_xi(s_native, dps=dps)


# ==============================================================================
# 3. ZERO WORLDLINES AND CRITICAL SURFACE
# ==============================================================================

def zero_worldline_point(
    rho_clean: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    grade: Union[BaseGrade, str, int, float],
    delta: Union[str, float, mpmath.mpf] = "0.0",
    dps: int = 80
) -> mpmath.mpc:
    """
    Compute point on the zero worldline s_rho(k) = tau^k * (1/2 + delta + i*gamma).
    For on-line zeros, delta = 0 and s_rho(k) = tau^k * (1/2 + i*gamma).
    """
    with mpmath.workdps(dps + 15):
        clean_mpc = math_core.to_mpc(rho_clean, dps=dps + 15)
        d_mpf = math_core.to_mpf(delta, dps=dps + 15)
        
        rho_pert = mpmath.mpc(clean_mpc.real + d_mpf, clean_mpc.imag)
        g_obj = parse_grade(grade) if not isinstance(grade, BaseGrade) else grade
        scale_A = g_obj.numeric_scale(dps=dps + 15)
        
        return scale_A * rho_pert


def critical_surface_sigma(
    grade: Union[BaseGrade, str, int, float],
    dps: int = 80
) -> mpmath.mpf:
    """
    Return critical line real coordinate at grade k: sigma_c(k) = tau^k / 2.
    """
    with mpmath.workdps(dps + 15):
        g_obj = parse_grade(grade) if not isinstance(grade, BaseGrade) else grade
        scale_A = g_obj.numeric_scale(dps=dps + 15)
        return scale_A / 2


def normalized_radial_leaf(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    grade: Union[BaseGrade, str, int, float],
    dps: int = 80
) -> mpmath.mpf:
    """
    Compute normalized radial leaf coordinate:
    R_tau(s, k) = tau^(-k) * Re(s) - 1/2.
    For any point on the worldline of rho = 1/2 + delta + i*gamma, R_tau = delta identically.
    """
    with mpmath.workdps(dps + 15):
        s_mpc = math_core.to_mpc(s, dps=dps + 15)
        g_obj = parse_grade(grade) if not isinstance(grade, BaseGrade) else grade
        scale_A = g_obj.numeric_scale(dps=dps + 15)
        
        return (s_mpc.real / scale_A) - mpmath.mpf('0.5')


def absolute_radial_defect(
    s: Union[complex, mpmath.mpc, str, Tuple[Any, Any]],
    grade: Union[BaseGrade, str, int, float],
    dps: int = 80
) -> mpmath.mpf:
    """
    Compute unscaled absolute radial displacement from the critical line at grade k:
    d_tau(s, k) = Re(s) - sigma_c(k) = Re(s) - tau^k / 2 = tau^k * delta.
    """
    with mpmath.workdps(dps + 15):
        s_mpc = math_core.to_mpc(s, dps=dps + 15)
        sigma_c = critical_surface_sigma(grade, dps=dps + 15)
        return s_mpc.real - sigma_c


def derive_compression_grade(
    source_height: Union[str, float, mpmath.mpf],
    target_height: Union[str, float, mpmath.mpf],
    dps: int = 80
) -> Dict[str, Any]:
    """
    Derive the continuous grade k and nearest integer K that maps source_height to target_height:
    target = tau^k * source  =>  k = log(target / source) / log(tau).
    """
    with mpmath.workdps(dps + 15):
        src = math_core.to_mpf(source_height, dps=dps + 15)
        tgt = math_core.to_mpf(target_height, dps=dps + 15)
        if src <= 0 or tgt <= 0:
            raise ValueError("Source and target heights must be strictly positive.")
            
        tau = math_core.get_tau(dps=dps + 15)
        k_mpf = mpmath.log(tgt / src) / mpmath.log(tau)
        k_float = float(k_mpf)
        nearest_K = round(k_float)
        
        actual_mapped_height = src * mpmath.power(tau, k_mpf)
        integer_mapped_height = src * mpmath.power(tau, nearest_K)
        
        return {
            "source_height": mpmath.nstr(src, n=dps),
            "target_height": mpmath.nstr(tgt, n=dps),
            "continuous_k": mpmath.nstr(k_mpf, n=dps),
            "continuous_k_val": k_mpf,
            "nearest_integer_K": nearest_K,
            "actual_mapped_height": mpmath.nstr(actual_mapped_height, n=dps),
            "integer_mapped_height": mpmath.nstr(integer_mapped_height, n=dps),
            "integer_scale_ratio": mpmath.nstr(mpmath.power(tau, nearest_K), n=dps)
        }


# ==============================================================================
# 4. CROSS-HEIGHT PATH COHERENCE ENGINE
# ==============================================================================

def mean_zero_spacing_delta(
    gamma: Union[str, float, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpf:
    """
    Compute baseline local mean-spacing scale for zero ordinate gamma:
    Delta_n = tau / log(gamma_n / tau).
    """
    with mpmath.workdps(dps + 15):
        g = math_core.to_mpf(gamma, dps=dps + 15)
        tau = math_core.get_tau(dps=dps + 15)
        if g <= tau:
            raise ValueError(f"Ordinate gamma ({g}) must exceed tau ({tau}) for positive mean spacing.")
        return tau / mpmath.log(g / tau)


def evaluate_zeta_derivative_at_zero(
    gamma: Union[str, float, mpmath.mpf],
    dps: int = 80
) -> mpmath.mpc:
    """
    Evaluate exact first derivative zeta'(1/2 + i*gamma) using high-precision differentiation.
    """
    with mpmath.workdps(dps + 25):
        s_0 = mpmath.mpc(mpmath.mpf('0.5'), math_core.to_mpf(gamma, dps=dps + 25))
        return math_core.zeta_derivative(s_0, n=1, dps=dps + 25)


def evaluate_derivative_normalized_path(
    gamma: Union[str, float, mpmath.mpf],
    u: Union[str, float, mpmath.mpf],
    dps: int = 80,
    zeta_prime: Optional[mpmath.mpc] = None
) -> Dict[str, Any]:
    """
    Evaluate derivative-normalized local trajectory:
    P_n(u) = zeta(1/2 + i*(gamma_n + Delta_n * u)) / [i * Delta_n * zeta'(rho_n)].
    Guaranteed properties: P_n(0) = 0, P_n'(0) = 1.
    """
    with mpmath.workdps(dps + 25):
        g = math_core.to_mpf(gamma, dps=dps + 25)
        u_val = math_core.to_mpf(u, dps=dps + 25)
        delta_n = mean_zero_spacing_delta(g, dps=dps + 25)
        
        # Sampling point s_n(u) = 1/2 + i*(gamma + Delta_n * u)
        t_sample = g + delta_n * u_val
        s_sample = mpmath.mpc(mpmath.mpf('0.5'), t_sample)
        
        zeta_val = math_core.zeta_eval(s_sample, dps=dps + 25)
        
        if zeta_prime is None:
            zeta_prime = evaluate_zeta_derivative_at_zero(g, dps=dps + 25)
            
        denom = mpmath.mpc('0', '1') * delta_n * zeta_prime
        if abs(denom) < mpmath.mpf('1e-50'):
            raise ValueError(f"Derivative at gamma={gamma} is nearly zero (|denom| < 1e-50); zero may not be simple.")
            
        p_n = zeta_val / denom
        
        return {
            "gamma": mpmath.nstr(g, n=dps),
            "u": mpmath.nstr(u_val, n=dps),
            "Delta_n": mpmath.nstr(delta_n, n=dps),
            "s_sample": f"{mpmath.nstr(s_sample.real, n=dps)} + {mpmath.nstr(s_sample.imag, n=dps)}j",
            "zeta_val": f"{mpmath.nstr(zeta_val.real, n=dps)} + {mpmath.nstr(zeta_val.imag, n=dps)}j",
            "zeta_prime": f"{mpmath.nstr(zeta_prime.real, n=dps)} + {mpmath.nstr(zeta_prime.imag, n=dps)}j",
            "P_n_re": mpmath.nstr(p_n.real, n=dps),
            "P_n_im": mpmath.nstr(p_n.imag, n=dps),
            "abs_P_n": mpmath.nstr(abs(p_n), n=dps),
            "P_n_mpc": p_n
        }


def extract_taylor_shape_coefficients(
    gamma: Union[str, float, mpmath.mpf],
    dps: int = 80
) -> Dict[str, Any]:
    """
    Extract exact local Taylor shape coefficients:
    P_n(u) = u + c_2,n * u^2 + c_3,n * u^3 + O(u^4)
    where:
      c_2,n = (i * Delta_n * zeta''(rho_n)) / (2 * zeta'(rho_n))
      c_3,n = ((i * Delta_n)^2 * zeta'''(rho_n)) / (6 * zeta'(rho_n))
    """
    with mpmath.workdps(dps + 25):
        g = math_core.to_mpf(gamma, dps=dps + 25)
        delta_n = mean_zero_spacing_delta(g, dps=dps + 25)
        s_0 = mpmath.mpc(mpmath.mpf('0.5'), g)
        
        z_1 = math_core.zeta_derivative(s_0, n=1, dps=dps + 25)
        z_2 = math_core.zeta_derivative(s_0, n=2, dps=dps + 25)
        z_3 = math_core.zeta_derivative(s_0, n=3, dps=dps + 25)
        
        i_delta = mpmath.mpc('0', '1') * delta_n
        c_2 = (i_delta * z_2) / (mpmath.mpf(2) * z_1)
        c_3 = (mpmath.power(i_delta, 2) * z_3) / (mpmath.mpf(6) * z_1)
        
        return {
            "gamma": mpmath.nstr(g, n=dps),
            "Delta_n": mpmath.nstr(delta_n, n=dps),
            "zeta_prime": f"{mpmath.nstr(z_1.real, n=dps)} + {mpmath.nstr(z_1.imag, n=dps)}j",
            "c2_re": mpmath.nstr(c_2.real, n=dps),
            "c2_im": mpmath.nstr(c_2.imag, n=dps),
            "abs_c2": mpmath.nstr(abs(c_2), n=dps),
            "c3_re": mpmath.nstr(c_3.real, n=dps),
            "c3_im": mpmath.nstr(c_3.imag, n=dps),
            "abs_c3": mpmath.nstr(abs(c_3), n=dps),
            "c2_mpc": c_2,
            "c3_mpc": c_3
        }


def compute_cross_height_path_distance(
    gamma_1: Union[str, float, mpmath.mpf],
    gamma_2: Union[str, float, mpmath.mpf],
    u_points: Optional[Sequence[Union[str, float, mpmath.mpf]]] = None,
    dps: int = 80
) -> Dict[str, Any]:
    """
    Compute distance metrics between derivative-normalized paths P_1(u) and P_2(u)
    across a discrete grid u in [-1, 1]:
      L_infty = max_u |P_1(u) - P_2(u)|
      L_2     = sqrt( (1/N) * sum_u |P_1(u) - P_2(u)|^2 )
    """
    with mpmath.workdps(dps + 20):
        if u_points is None:
            # Default 21-point symmetric grid on [-1, 1]
            u_points = [str(mpmath.nstr(mpmath.mpf(i) / 10, n=5)) for i in range(-10, 11)]
            
        g1 = math_core.to_mpf(gamma_1, dps=dps + 20)
        g2 = math_core.to_mpf(gamma_2, dps=dps + 20)
        
        zp_1 = evaluate_zeta_derivative_at_zero(g1, dps=dps + 20)
        zp_2 = evaluate_zeta_derivative_at_zero(g2, dps=dps + 20)
        
        diffs = []
        point_comparisons = []
        
        for u in u_points:
            p1_info = evaluate_derivative_normalized_path(g1, u, dps=dps + 15, zeta_prime=zp_1)
            p2_info = evaluate_derivative_normalized_path(g2, u, dps=dps + 15, zeta_prime=zp_2)
            
            p1_val = p1_info["P_n_mpc"]
            p2_val = p2_info["P_n_mpc"]
            diff_abs = abs(p1_val - p2_val)
            diffs.append(diff_abs)
            
            point_comparisons.append({
                "u": str(u),
                "P1_re": mpmath.nstr(p1_val.real, n=dps),
                "P1_im": mpmath.nstr(p1_val.imag, n=dps),
                "P2_re": mpmath.nstr(p2_val.real, n=dps),
                "P2_im": mpmath.nstr(p2_val.imag, n=dps),
                "diff_abs": mpmath.nstr(diff_abs, n=dps)
            })
            
        l_infty = max(diffs) if diffs else mpmath.mpf('0')
        l_2 = mpmath.sqrt(sum(d * d for d in diffs) / mpmath.mpf(len(diffs))) if diffs else mpmath.mpf('0')
        
        return {
            "gamma_1": mpmath.nstr(g1, n=dps),
            "gamma_2": mpmath.nstr(g2, n=dps),
            "num_u_points": len(u_points),
            "L_infty_distance": mpmath.nstr(l_infty, n=dps),
            "L_2_distance": mpmath.nstr(l_2, n=dps),
            "point_comparisons": point_comparisons
        }
