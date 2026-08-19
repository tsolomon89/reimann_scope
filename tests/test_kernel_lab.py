"""
tests/test_kernel_lab.py — Tests for Kernel Lab, Inverse Scale Lock, and Non-Holomorphic Deformations

Trust test 7 from SPEC.md §12 and Vector D from MATH_CONTRACT.md §13.
"""

import pytest
import mpmath
import math_core
import transforms


def test_vector_d_inverse_kernel_lock():
    """
    Vector D: A=2, B=1/2, C=D=0.
    Expected: AB = 1 and Z_{2,0,1/2,0}(s) == zeta(s).
    """
    t = transforms.KernelTransform(A=2.0, B=0.5, C=0.0, D=0.0, inverse_scale_lock=True)
    assert abs(t.A * t.B - 1.0) < 1e-12
    assert "EXACT KERNEL PAIRING PRESERVED" in t.classification
    
    test_points = [
        complex(0.5, 14.134725),
        complex(0.75, 25.0),
        complex(2.0, 3.0),
        complex(-0.5, 12.0)
    ]
    for s in test_points:
        z_trans = t.evaluate_function(s, dps=35)
        z_orig = math_core.zeta_eval(s, dps=35)
        assert abs(z_trans - z_orig) < 1e-12


def test_centered_kernel_lock():
    """Centered kernel mode with AB=1 gives zeta(1/2 + z) == zeta(s)."""
    t = transforms.CenteredKernelTransform(A=3.5, inverse_scale_lock=True)
    assert abs(t.A * t.B - 1.0) < 1e-12
    
    s = complex(0.5, 14.134725)
    val = t.evaluate_function(s, dps=35)
    val_orig = math_core.zeta_eval(s, dps=35)
    assert abs(val - val_orig) < 1e-12


def test_anisotropic_non_holomorphic_label():
    """Verify non-holomorphic deformation is properly flagged when A_delta != A_gamma."""
    t_non_holo = transforms.AnisotropicDeformation(A_delta=1.5, A_gamma=1.0)
    assert not t_non_holo.is_holomorphic
    assert "NON-HOLOMORPHIC DEFORMATION" in t_non_holo.classification
    
    t_holo = transforms.AnisotropicDeformation(A_delta=2.0, A_gamma=2.0)
    assert t_holo.is_holomorphic
    assert "NON-HOLOMORPHIC DEFORMATION" not in t_holo.classification
