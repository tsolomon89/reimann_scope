"""
transforms.py — Explicit Transformation Objects and Active Mathematics Card

Implements distinct, typed transform classes conforming to:
- RIEMANN_MICROSCOPE_SPEC.md §3, §4, §10
- MATH_CONTRACT.md §2 - §10
- DECISIONS.md
- EXPERIMENT_PROTOCOL.md

Every transform object provides:
- Mode Name & Parameter State
- Exact Domain Map
- Exact Function Evaluated
- Original Critical Line & Image Critical Line
- Predicted Zero Map (Preview float & Authoritative Arbitrary-Precision MPC)
- Exact Classification
- Callable evaluation for single points & numpy vector batches
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any, Optional, Union
import numpy as np
import mpmath
import math_core
import transcendental


class BaseTransform(ABC):
    """Abstract base class for all coordinate and arithmetic transformations."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def classification(self) -> str:
        pass

    @property
    @abstractmethod
    def domain_map_str(self) -> str:
        pass

    @property
    @abstractmethod
    def function_str(self) -> str:
        pass

    @property
    @abstractmethod
    def original_critical_line_str(self) -> str:
        return "Re(s) = 1/2"

    @property
    @abstractmethod
    def image_critical_line_str(self) -> str:
        pass

    @property
    @abstractmethod
    def zero_map_str(self) -> str:
        pass

    @abstractmethod
    def map_domain_point(self, s: complex) -> complex:
        """[Preview] Map input coordinate s to transformed domain coordinate s'."""
        pass

    @abstractmethod
    def evaluate_function(self, s: Union[complex, mpmath.mpc, str], dps: int = 35) -> mpmath.mpc:
        """[Authoritative] Evaluate the transformed function f(s) at precision dps."""
        pass

    @abstractmethod
    def map_zero(self, rho: complex) -> complex:
        """[Preview] Predict the mapped location of a baseline zero rho as float complex."""
        pass

    @abstractmethod
    def map_zero_mpc(self, rho: Union[complex, mpmath.mpc, str, Tuple[Any, Any]], dps: int = 80) -> mpmath.mpc:
        """[Audit/Authoritative] Predict mapped location of baseline zero rho at arbitrary precision."""
        pass

    def map_domain_array(self, s_arr: np.ndarray) -> np.ndarray:
        """Vectorized domain coordinate mapping (preview)."""
        return np.array([self.map_domain_point(s) for s in s_arr], dtype=np.complex128)

    def evaluate_array(self, s_arr: np.ndarray, dps: int = 35) -> Tuple[np.ndarray, np.ndarray]:
        """Vectorized evaluation along path, returns (Re f(s), Im f(s)) float arrays (preview)."""
        re_vals = np.empty(len(s_arr), dtype=np.float64)
        im_vals = np.empty(len(s_arr), dtype=np.float64)
        for i, s in enumerate(s_arr):
            val = self.evaluate_function(s, dps=dps)
            re_vals[i] = float(val.real)
            im_vals[i] = float(val.imag)
        return re_vals, im_vals

    def get_card_dict(self) -> Dict[str, str]:
        """Return key-value dictionary for Active Mathematics Card."""
        d = {
            "mode": self.name,
            "classification": self.classification,
            "domain_map": self.domain_map_str,
            "function": self.function_str,
            "original_critical_line": self.original_critical_line_str,
            "image_critical_line": self.image_critical_line_str,
            "zero_map": self.zero_map_str,
        }
        if hasattr(self, "converter_identity_str") and getattr(self, "converter_identity_str"):
            d["coupled_converter_identity"] = getattr(self, "converter_identity_str")
        return d

    def get_card_markdown(self) -> str:
        """Format the active mathematics card as clean GitHub Markdown."""
        d = self.get_card_dict()
        md = (
            f"**MODE: {d['mode']}**\n\n"
            f"- **Domain map:** `{d['domain_map']}`\n"
            f"- **Function plotted:** `{d['function']}`\n"
            f"- **Original critical line:** `{d['original_critical_line']}`\n"
            f"- **Image critical line:** `{d['image_critical_line']}`\n"
            f"- **Predicted zero map:** `{d['zero_map']}`\n"
        )
        if "coupled_converter_identity" in d:
            md += f"- **Coupled converter identity:** `{d['coupled_converter_identity']}`\n"
        md += f"\n**CLASS:** {d['classification']}"
        return md



class CameraTransform(BaseTransform):
    """Mode 1: Camera zoom and pan only. No mathematical alteration."""
    
    def __init__(self):
        pass

    @property
    def name(self) -> str:
        return "CAMERA ONLY"

    @property
    def classification(self) -> str:
        return "Rendering only. No mathematical change."

    @property
    def domain_map_str(self) -> str:
        return "T_camera(s) = s"

    @property
    def function_str(self) -> str:
        return "f(s) = ζ(s)"

    @property
    def original_critical_line_str(self) -> str:
        return "Re(s) = 1/2"

    @property
    def image_critical_line_str(self) -> str:
        return "Re(s) = 1/2"

    @property
    def zero_map_str(self) -> str:
        return "ρ' = ρ"

    def map_domain_point(self, s: complex) -> complex:
        return s

    def evaluate_function(self, s: Union[complex, mpmath.mpc, str], dps: int = 35) -> mpmath.mpc:
        return math_core.zeta_eval(s, dps=dps)

    def map_zero(self, rho: complex) -> complex:
        return rho

    def map_zero_mpc(self, rho: Union[complex, mpmath.mpc, str, Tuple[Any, Any]], dps: int = 80) -> mpmath.mpc:
        return math_core.to_mpc(rho, dps=dps)


class HeightMicroscopeTransform(BaseTransform):
    """
    Mode 2: Height microscope / macroscope.
    s_K(u) = 1/2 + delta + i(t0 + tau^K * u).
    Changes the sampled height range only.
    """
    def __init__(
        self,
        k: Union[str, float, int, mpmath.mpf] = 0.0,
        t0: Union[str, float, int, mpmath.mpf] = 14.0,
        delta: Union[str, float, int, mpmath.mpf] = 0.0
    ):
        self.k_str = str(k)
        self.t0_str = str(t0)
        self.delta_str = str(delta)
        self.k = float(k)
        self.t0 = float(t0)
        self.delta = float(delta)

    @property
    def name(self) -> str:
        return f"HEIGHT MICROSCOPE (k={self.k:.4f})"

    @property
    def classification(self) -> str:
        return "Height microscope/macroscope. Changes sampled ordinate range only."

    @property
    def domain_map_str(self) -> str:
        return f"s_K(u) = 1/2 + {self.delta:.4g} + i({self.t0:.4g} + τ^{self.k:.4g} * u)"

    @property
    def function_str(self) -> str:
        return "f(u) = ζ(s_K(u))"

    @property
    def original_critical_line_str(self) -> str:
        return "Re(s) = 1/2"

    @property
    def image_critical_line_str(self) -> str:
        if abs(self.delta) < 1e-12:
            return "Re(s) = 1/2"
        return f"Re(s) = 1/2 + {self.delta:.4g}"

    @property
    def zero_map_str(self) -> str:
        return "ρ' = ρ (zeros on critical line unchanged)"

    def map_domain_point(self, s: complex) -> complex:
        return s

    def evaluate_function(self, s: Union[complex, mpmath.mpc, str], dps: int = 35) -> mpmath.mpc:
        return math_core.zeta_eval(s, dps=dps)

    def map_zero(self, rho: complex) -> complex:
        return rho

    def map_zero_mpc(self, rho: Union[complex, mpmath.mpc, str, Tuple[Any, Any]], dps: int = 80) -> mpmath.mpc:
        return math_core.to_mpc(rho, dps=dps)


class OriginCoordinateDilation(BaseTransform):
    """
    Mode 3: Origin coordinate dilation.
    s' = tau^K * s
    f_K(s') = zeta(s' / tau^K)
    image critical line: Re(s') = tau^K / 2
    zero map: rho' = tau^K * rho
    """
    def __init__(self, k: Union[str, float, int, mpmath.mpf] = 0.0):
        self.k_str = str(k)
        self.k = float(k)
        self.tau = float(math_core.get_tau(50))
        self.scale = self.tau ** self.k

    @property
    def name(self) -> str:
        return f"ORIGIN COORDINATE DILATION (k={self.k:.4f})"

    @property
    def classification(self) -> str:
        return "Exact coordinate re-expression of ζ. Not a claim that ζ(τ^k s) = ζ(s)."

    @property
    def domain_map_str(self) -> str:
        return f"s' = τ^{self.k:.4g} s"

    @property
    def function_str(self) -> str:
        return f"f_k(s') = ζ(s' / τ^{self.k:.4g})"

    @property
    def original_critical_line_str(self) -> str:
        return "Re(s) = 1/2"

    @property
    def image_critical_line_str(self) -> str:
        return f"Re(s') = τ^{self.k:.4g} / 2 = {self.scale / 2.0:.6g}"

    @property
    def zero_map_str(self) -> str:
        return f"ρ' = τ^{self.k:.4g} ρ"

    @property
    def converter_identity_str(self) -> str:
        return f"A = τ^{self.k:.4g}, ρ' = Aρ, x' = x^(1/A) ⇒ ρ' log x' = ρ log x ⇒ C_J(x^(1/A), Aρ) = C_J(x, ρ)"


    def map_domain_point(self, s: complex) -> complex:
        return s * self.scale

    def evaluate_function(self, s_prime: Union[complex, mpmath.mpc, str], dps: int = 35) -> mpmath.mpc:
        with mpmath.workdps(dps + 10):
            tau_val = math_core.get_tau(dps + 10)
            k_val = math_core.to_mpf(self.k_str, dps=dps + 10)
            scale_val = mpmath.power(tau_val, k_val)
            s_orig = math_core.to_mpc(s_prime, dps=dps + 10) / scale_val
            return math_core.zeta_eval(s_orig, dps=dps)

    def map_zero(self, rho: complex) -> complex:
        return rho * self.scale

    def map_zero_mpc(self, rho: Union[complex, mpmath.mpc, str, Tuple[Any, Any]], dps: int = 80) -> mpmath.mpc:
        with mpmath.workdps(dps + 10):
            tau_val = math_core.get_tau(dps + 10)
            k_val = math_core.to_mpf(self.k_str, dps=dps + 10)
            scale_val = mpmath.power(tau_val, k_val)
            rho_mpc = math_core.to_mpc(rho, dps=dps + 10)
            return scale_val * rho_mpc


class CenteredCoordinateDilation(BaseTransform):
    """
    Mode 4: Centered coordinate dilation.
    s' = 1/2 + tau^K * (s - 1/2)
    f_K(s') = zeta(1/2 + (s' - 1/2) / tau^K)
    image critical line: Re(s') = 1/2 (geometrically fixed)
    zero map: rho' = 1/2 + tau^K * (rho - 1/2)
    """
    def __init__(self, k: Union[str, float, int, mpmath.mpf] = 0.0):
        self.k_str = str(k)
        self.k = float(k)
        self.tau = float(math_core.get_tau(50))
        self.scale = self.tau ** self.k

    @property
    def name(self) -> str:
        return f"CENTERED COORDINATE DILATION (k={self.k:.4f})"

    @property
    def classification(self) -> str:
        return "Exact centered coordinate dilation. Critical line Re(s')=1/2 fixed geometrically."

    @property
    def domain_map_str(self) -> str:
        return f"s' = 1/2 + τ^{self.k:.4g}(s - 1/2)"

    @property
    def function_str(self) -> str:
        return f"f_k(s') = ζ(1/2 + (s' - 1/2) / τ^{self.k:.4g})"

    @property
    def original_critical_line_str(self) -> str:
        return "Re(s) = 1/2"

    @property
    def image_critical_line_str(self) -> str:
        return "Re(s') = 1/2"

    @property
    def zero_map_str(self) -> str:
        return f"ρ' = 1/2 + τ^{self.k:.4g}(ρ - 1/2)"

    def map_domain_point(self, s: complex) -> complex:
        return 0.5 + self.scale * (s - 0.5)

    def evaluate_function(self, s_prime: Union[complex, mpmath.mpc, str], dps: int = 35) -> mpmath.mpc:
        with mpmath.workdps(dps + 10):
            tau_val = math_core.get_tau(dps + 10)
            k_val = math_core.to_mpf(self.k_str, dps=dps + 10)
            scale_val = mpmath.power(tau_val, k_val)
            s_mpc = math_core.to_mpc(s_prime, dps=dps + 10)
            s_orig = mpmath.mpf('0.5') + (s_mpc - mpmath.mpf('0.5')) / scale_val
            return math_core.zeta_eval(s_orig, dps=dps)

    def map_zero(self, rho: complex) -> complex:
        return 0.5 + self.scale * (rho - 0.5)

    def map_zero_mpc(self, rho: Union[complex, mpmath.mpc, str, Tuple[Any, Any]], dps: int = 80) -> mpmath.mpc:
        with mpmath.workdps(dps + 10):
            tau_val = math_core.get_tau(dps + 10)
            k_val = math_core.to_mpf(self.k_str, dps=dps + 10)
            scale_val = mpmath.power(tau_val, k_val)
            rho_mpc = math_core.to_mpc(rho, dps=dps + 10)
            return mpmath.mpf('0.5') + scale_val * (rho_mpc - mpmath.mpf('0.5'))


class ArgumentTransform(BaseTransform):
    """
    Mode 5: Zeta argument transform.
    f_K(s) = zeta(tau^K * s)
    critical-zero line: Re(s) = 1 / (2 * tau^K)
    zero map: s = rho / tau^K
    """
    def __init__(self, k: Union[str, float, int, mpmath.mpf] = 0.0):
        self.k_str = str(k)
        self.k = float(k)
        self.tau = float(math_core.get_tau(50))
        self.scale = self.tau ** self.k

    @property
    def name(self) -> str:
        return f"ARGUMENT TRANSFORM (k={self.k:.4f})"

    @property
    def classification(self) -> str:
        return "Analytic argument scaling. Changes the evaluated function; not a coordinate re-expression."

    @property
    def domain_map_str(self) -> str:
        return f"s ↦ τ^{self.k:.4g} s"

    @property
    def function_str(self) -> str:
        return f"f_k(s) = ζ(τ^{self.k:.4g} s)"

    @property
    def original_critical_line_str(self) -> str:
        return "Re(s) = 1/2"

    @property
    def image_critical_line_str(self) -> str:
        return f"Re(s) = 1 / (2 * τ^{self.k:.4g}) = {1.0 / (2.0 * self.scale):.6g}"

    @property
    def zero_map_str(self) -> str:
        return f"s_ρ = ρ / τ^{self.k:.4g}"

    def map_domain_point(self, s: complex) -> complex:
        return s

    def evaluate_function(self, s: Union[complex, mpmath.mpc, str], dps: int = 35) -> mpmath.mpc:
        with mpmath.workdps(dps + 10):
            tau_val = math_core.get_tau(dps + 10)
            k_val = math_core.to_mpf(self.k_str, dps=dps + 10)
            scale_val = mpmath.power(tau_val, k_val)
            s_arg = math_core.to_mpc(s, dps=dps + 10) * scale_val
            return math_core.zeta_eval(s_arg, dps=dps)

    def map_zero(self, rho: complex) -> complex:
        return rho / self.scale

    def map_zero_mpc(self, rho: Union[complex, mpmath.mpc, str, Tuple[Any, Any]], dps: int = 80) -> mpmath.mpc:
        with mpmath.workdps(dps + 10):
            tau_val = math_core.get_tau(dps + 10)
            k_val = math_core.to_mpf(self.k_str, dps=dps + 10)
            scale_val = mpmath.power(tau_val, k_val)
            rho_mpc = math_core.to_mpc(rho, dps=dps + 10)
            return rho_mpc / scale_val


class KernelTransform(BaseTransform):
    """
    Mode 6: Kernel Lab Transform.
    log n ↦ A log n + C
    s ↦ B s + D
    Canonical formula: Z_{A,C,B,D}(s) = exp(-C(Bs+D)) * zeta(A(Bs+D)).
    When Inverse Scale Lock is ON: AB = 1 (B = 1/A).
    """
    def __init__(
        self,
        A: Union[str, float, int, mpmath.mpf] = 1.0,
        B: Union[str, float, int, mpmath.mpf] = 1.0,
        C: Union[str, float, int, mpmath.mpf] = 0.0,
        D: Union[str, float, int, mpmath.mpf] = 0.0,
        inverse_scale_lock: bool = False
    ):
        self.A_str = str(A)
        self.A = float(A)
        self.inverse_scale_lock = inverse_scale_lock
        if inverse_scale_lock:
            self.B_str = str(1.0 / self.A) if self.A != 0 else "1.0"
            self.B = 1.0 / self.A if self.A != 0 else 1.0
        else:
            self.B_str = str(B)
            self.B = float(B)
        self.C_str = str(C)
        self.C = float(C)
        self.D_str = str(D)
        self.D = float(D)

    @property
    def name(self) -> str:
        lock_status = " [LOCKED AB=1]" if self.inverse_scale_lock else ""
        return f"KERNEL LAB (A={self.A:.4g}, B={self.B:.4g}{lock_status})"

    @property
    def classification(self) -> str:
        if abs(self.A * self.B - 1.0) < 1e-12 and abs(self.C) < 1e-12 and abs(self.D) < 1e-12:
            return "EXACT KERNEL PAIRING PRESERVED (AB=1, C=D=0: Z(s) = ζ(s))"
        return "Dirichlet kernel deformation (analytically continued in critical strip)."

    @property
    def domain_map_str(self) -> str:
        return f"log n ↦ {self.A:.4g} log n + {self.C:.4g}, s ↦ {self.B:.4g} s + {self.D:.4g}"

    @property
    def function_str(self) -> str:
        return f"Z_{{A,C,B,D}}(s) = exp(-{self.C:.4g}({self.B:.4g}s + {self.D:.4g})) * ζ({self.A:.4g}({self.B:.4g}s + {self.D:.4g}))"

    @property
    def original_critical_line_str(self) -> str:
        return "Re(s) = 1/2"

    @property
    def image_critical_line_str(self) -> str:
        # A(B s + D) = 1/2 + i*t => Re(s) = (1/(2A) - Re(D)) / B
        if abs(self.A * self.B) > 1e-12:
            crit_re = (0.5 / self.A - self.D) / self.B
            return f"Re(s) = (1/(2A) - D)/B = {crit_re:.6g}"
        return "Undefined (singular scale)"

    @property
    def zero_map_str(self) -> str:
        return "s_ρ = (ρ/A - D) / B"

    def map_domain_point(self, s: complex) -> complex:
        return s

    def evaluate_function(self, s: Union[complex, mpmath.mpc, str], dps: int = 35) -> mpmath.mpc:
        with mpmath.workdps(dps + 10):
            a_val = math_core.to_mpf(self.A_str, dps=dps + 10)
            if self.inverse_scale_lock and a_val != 0:
                b_val = mpmath.mpf(1) / a_val
            else:
                b_val = math_core.to_mpf(self.B_str, dps=dps + 10)
            c_val = math_core.to_mpf(self.C_str, dps=dps + 10)
            d_val = math_core.to_mpf(self.D_str, dps=dps + 10)
            s_mpc = math_core.to_mpc(s, dps=dps + 10)
            
            inner = b_val * s_mpc + d_val
            zeta_arg = a_val * inner
            prefactor = mpmath.exp(-c_val * inner)
            zeta_val = math_core.zeta_eval(zeta_arg, dps=dps)
            return prefactor * zeta_val

    def map_zero(self, rho: complex) -> complex:
        if abs(self.A * self.B) < 1e-12:
            return complex(float('nan'), float('nan'))
        return (rho / self.A - self.D) / self.B

    def map_zero_mpc(self, rho: Union[complex, mpmath.mpc, str, Tuple[Any, Any]], dps: int = 80) -> mpmath.mpc:
        with mpmath.workdps(dps + 10):
            a_val = math_core.to_mpf(self.A_str, dps=dps + 10)
            if self.inverse_scale_lock and a_val != 0:
                b_val = mpmath.mpf(1) / a_val
            else:
                b_val = math_core.to_mpf(self.B_str, dps=dps + 10)
            d_val = math_core.to_mpf(self.D_str, dps=dps + 10)
            rho_mpc = math_core.to_mpc(rho, dps=dps + 10)
            return (rho_mpc / a_val - d_val) / b_val


class CenteredKernelTransform(BaseTransform):
    """
    Centered kernel mode:
    Z^{ctr}_{A,B}(z) = zeta(1/2 + AB * z) where z = s - 1/2.
    When AB = 1: Z^{ctr}_{A,1/A}(z) = zeta(1/2 + z) = zeta(s).
    """
    def __init__(
        self,
        A: Union[str, float, int, mpmath.mpf] = 1.0,
        B: Union[str, float, int, mpmath.mpf] = 1.0,
        inverse_scale_lock: bool = True
    ):
        self.A_str = str(A)
        self.A = float(A)
        self.inverse_scale_lock = inverse_scale_lock
        if inverse_scale_lock:
            self.B_str = str(1.0 / self.A) if self.A != 0 else "1.0"
            self.B = 1.0 / self.A if self.A != 0 else 1.0
        else:
            self.B_str = str(B)
            self.B = float(B)

    @property
    def name(self) -> str:
        return f"CENTERED KERNEL MODE (A={self.A:.4g}, B={self.B:.4g})"

    @property
    def classification(self) -> str:
        if abs(self.A * self.B - 1.0) < 1e-12:
            return "EXACT KERNEL PAIRING PRESERVED: ζ argument unchanged (AB=1)."
        return "Centered kernel deformation."

    @property
    def domain_map_str(self) -> str:
        return f"z = s - 1/2 ↦ {self.A * self.B:.4g} z"

    @property
    def function_str(self) -> str:
        return f"Z^{{ctr}}_{{A,B}}(z) = ζ(1/2 + {self.A * self.B:.4g}(s - 1/2))"

    @property
    def original_critical_line_str(self) -> str:
        return "Re(s) = 1/2"

    @property
    def image_critical_line_str(self) -> str:
        return "Re(s) = 1/2"

    @property
    def zero_map_str(self) -> str:
        return f"s_ρ = 1/2 + (ρ - 1/2) / {self.A * self.B:.4g}"

    def map_domain_point(self, s: complex) -> complex:
        return s

    def evaluate_function(self, s: Union[complex, mpmath.mpc, str], dps: int = 35) -> mpmath.mpc:
        with mpmath.workdps(dps + 10):
            a_val = math_core.to_mpf(self.A_str, dps=dps + 10)
            if self.inverse_scale_lock:
                ab_val = mpmath.mpf('1.0')
            else:
                b_val = math_core.to_mpf(self.B_str, dps=dps + 10)
                ab_val = a_val * b_val
            s_mpc = math_core.to_mpc(s, dps=dps + 10)
            z = s_mpc - mpmath.mpf('0.5')
            zeta_arg = mpmath.mpf('0.5') + ab_val * z
            return math_core.zeta_eval(zeta_arg, dps=dps)

    def map_zero(self, rho: complex) -> complex:
        ab = self.A * self.B
        if abs(ab) < 1e-12:
            return complex(float('nan'), float('nan'))
        return 0.5 + (rho - 0.5) / ab

    def map_zero_mpc(self, rho: Union[complex, mpmath.mpc, str, Tuple[Any, Any]], dps: int = 80) -> mpmath.mpc:
        with mpmath.workdps(dps + 10):
            a_val = math_core.to_mpf(self.A_str, dps=dps + 10)
            if self.inverse_scale_lock:
                ab_val = mpmath.mpf('1.0')
            else:
                b_val = math_core.to_mpf(self.B_str, dps=dps + 10)
                ab_val = a_val * b_val
            rho_mpc = math_core.to_mpc(rho, dps=dps + 10)
            return mpmath.mpf('0.5') + (rho_mpc - mpmath.mpf('0.5')) / ab_val


class AnisotropicDeformation(BaseTransform):
    """
    Anisotropic centered deformation:
    z = delta + i*gamma ↦ A_delta * delta + i * A_gamma * gamma.
    If A_delta != A_gamma, labeled NON-HOLOMORPHIC DEFORMATION.
    """
    def __init__(
        self,
        A_delta: Union[str, float, int, mpmath.mpf] = 1.0,
        A_gamma: Union[str, float, int, mpmath.mpf] = 1.0
    ):
        self.A_delta_str = str(A_delta)
        self.A_gamma_str = str(A_gamma)
        self.A_delta = float(A_delta)
        self.A_gamma = float(A_gamma)

    @property
    def is_holomorphic(self) -> bool:
        return abs(self.A_delta - self.A_gamma) < 1e-12

    @property
    def name(self) -> str:
        return f"ANISOTROPIC DEFORMATION (A_δ={self.A_delta:.4g}, A_γ={self.A_gamma:.4g})"

    @property
    def classification(self) -> str:
        if not self.is_holomorphic:
            return "NON-HOLOMORPHIC DEFORMATION (A_δ ≠ A_γ breaks Cauchy-Riemann equations)"
        return f"Isotropic centered dilation (A={self.A_delta:.4g})"

    @property
    def domain_map_str(self) -> str:
        return f"δ + iγ ↦ {self.A_delta:.4g}δ + i{self.A_gamma:.4g}γ"

    @property
    def function_str(self) -> str:
        return f"f(s) = ζ(1/2 + {self.A_delta:.4g}(Re s - 1/2) + i{self.A_gamma:.4g} Im s)"

    @property
    def original_critical_line_str(self) -> str:
        return "Re(s) = 1/2"

    @property
    def image_critical_line_str(self) -> str:
        return "Re(s) = 1/2 (since δ=0 ↦ 0)"

    @property
    def zero_map_str(self) -> str:
        return f"s_ρ = 1/2 + (Re ρ - 1/2)/{self.A_delta:.4g} + i(Im ρ)/{self.A_gamma:.4g}"

    def map_domain_point(self, s: complex) -> complex:
        return s

    def evaluate_function(self, s: Union[complex, mpmath.mpc, str], dps: int = 35) -> mpmath.mpc:
        with mpmath.workdps(dps + 10):
            a_del = math_core.to_mpf(self.A_delta_str, dps=dps + 10)
            a_gam = math_core.to_mpf(self.A_gamma_str, dps=dps + 10)
            s_mpc = math_core.to_mpc(s, dps=dps + 10)
            delta = s_mpc.real - mpmath.mpf('0.5')
            gamma = s_mpc.imag
            arg = mpmath.mpc(mpmath.mpf('0.5') + a_del * delta, a_gam * gamma)
            return math_core.zeta_eval(arg, dps=dps)

    def map_zero(self, rho: complex) -> complex:
        delta = rho.real - 0.5
        gamma = rho.imag
        if abs(self.A_delta) < 1e-12 or abs(self.A_gamma) < 1e-12:
            return complex(float('nan'), float('nan'))
        return 0.5 + (delta / self.A_delta) + 1j * (gamma / self.A_gamma)

    def map_zero_mpc(self, rho: Union[complex, mpmath.mpc, str, Tuple[Any, Any]], dps: int = 80) -> mpmath.mpc:
        with mpmath.workdps(dps + 10):
            a_del = math_core.to_mpf(self.A_delta_str, dps=dps + 10)
            a_gam = math_core.to_mpf(self.A_gamma_str, dps=dps + 10)
            rho_mpc = math_core.to_mpc(rho, dps=dps + 10)
            delta = rho_mpc.real - mpmath.mpf('0.5')
            gamma = rho_mpc.imag
            return mpmath.mpc(mpmath.mpf('0.5') + delta / a_del, gamma / a_gam)


class TranscendentalContinuationTransform(BaseTransform):
    """
    Transcendental Continuation Transform:
    Represents the extended domain function Z_tau(s, k) = zeta(tau^(-k) * s).
    Supports explicit BaseGrade instances (IntegerTauGrade, RationalTauGrade, ContinuousGrade, GenericScale).
    At k = 0 (native analytic slice): identically Z_tau(s, 0) = zeta(s).
    """
    def __init__(
        self,
        grade: Union[transcendental.BaseGrade, str, int, float] = 0,
        grade_type: str = "auto"
    ):
        if isinstance(grade, transcendental.BaseGrade):
            self.grade = grade
        else:
            self.grade = transcendental.parse_grade(grade, grade_type=grade_type)

    @property
    def name(self) -> str:
        if self.grade.semantic_type == "integer_tau" and getattr(self.grade, "K", None) == 0:
            return "TRANSCENDENTAL CONTINUATION (k = 0, Native Analytic Slice)"
        return f"TRANSCENDENTAL CONTINUATION ({self.grade.display_label()})"

    @property
    def classification(self) -> str:
        if self.grade.semantic_type == "integer_tau" and getattr(self.grade, "K", None) == 0:
            return "NATIVE ANALYTIC SLICE: Z_tau(s, 0) = zeta(s)"
        return f"EXTENDED DOMAIN SLICE ({self.grade.semantic_type}): Z_tau(s, k) = zeta(tau^(-k) * s)"

    @property
    def domain_map_str(self) -> str:
        return f"s ↦ tau^(-k) s = s / {self.grade.symbolic_expression()}"

    @property
    def function_str(self) -> str:
        return f"Z_tau(s, k) = ζ(tau^(-k) s)"

    @property
    def original_critical_line_str(self) -> str:
        return "Re(s) = 1/2"

    @property
    def image_critical_line_str(self) -> str:
        scale_val = float(self.grade.numeric_scale(dps=15))
        return f"Re(s) = tau^k / 2 = {scale_val / 2.0:.6g}"

    @property
    def zero_map_str(self) -> str:
        return f"s_ρ(k) = tau^k ρ = {self.grade.symbolic_expression()} * ρ"

    @property
    def radial_leaf_str(self) -> str:
        return "R_tau(s, k) = tau^(-k) Re(s) - 1/2 = δ"

    def map_domain_point(self, s: complex) -> complex:
        scale_val = float(self.grade.numeric_scale(dps=15))
        return s / scale_val if scale_val != 0 else s

    def evaluate_function(self, s: Union[complex, mpmath.mpc, str], dps: int = 35) -> mpmath.mpc:
        return transcendental.evaluate_extended_zeta(s, grade=self.grade, dps=dps)

    def map_zero(self, rho: complex) -> complex:
        scale_val = float(self.grade.numeric_scale(dps=15))
        return scale_val * rho

    def map_zero_mpc(self, rho: Union[complex, mpmath.mpc, str, Tuple[Any, Any]], dps: int = 80) -> mpmath.mpc:
        return transcendental.zero_worldline_point(rho, grade=self.grade, delta="0.0", dps=dps)

    def get_card_dict(self) -> Dict[str, str]:
        d = super().get_card_dict()
        d["grade_type"] = self.grade.semantic_type
        d["symbolic_scale"] = self.grade.symbolic_expression()
        d["numeric_scale"] = mpmath.nstr(self.grade.numeric_scale(dps=30), n=15)
        d["radial_coordinate"] = self.radial_leaf_str
        d["epistemic_class"] = "canonical_continuation_slice"
        return d
