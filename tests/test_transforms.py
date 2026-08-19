"""
tests/test_transforms.py — Tests for Explicit Transforms and Contract Vectors A, B, C

Trust tests 5, 6 from SPEC.md §12 and Vectors A, B, C from MATH_CONTRACT.md §13.
"""

import pytest
import mpmath
import math_core
import transforms
import reference_data


def test_vector_a_identity():
    """Vector A: K=0 Identity on all dilation transforms."""
    t_orig = transforms.OriginCoordinateDilation(k=0.0)
    t_ctr = transforms.CenteredCoordinateDilation(k=0.0)
    t_arg = transforms.ArgumentTransform(k=0.0)
    
    s = complex(0.5, 14.13472514173469379)
    assert t_orig.map_domain_point(s) == s
    assert t_ctr.map_domain_point(s) == s
    assert t_arg.map_domain_point(s) == s
    
    # Critical line values
    assert "Re(s) = 1/2" in t_orig.original_critical_line_str
    assert "Re(s') = 1/2" in t_ctr.image_critical_line_str


def test_vector_b_origin_dilation():
    """
    Vector B: K=1 Origin Coordinate Dilation.
    s' = tau * s
    Expected image critical line: Re(s') = tau/2 = pi.
    Expected zero map: rho' = tau * rho.
    """
    t = transforms.OriginCoordinateDilation(k=1.0)
    tau = float(math_core.get_tau(50))
    
    # Image critical line
    expected_image_re = tau / 2.0
    assert abs(t.scale / 2.0 - expected_image_re) < 1e-12
    assert "Re(s') = τ^1 / 2" in t.image_critical_line_str
    
    # Zero map
    ref_zeros = reference_data.load_reference_zeros()
    gam_1 = float(ref_zeros[0]) if ref_zeros else 14.13472514173469379
    rho = complex(0.5, gam_1)
    rho_prime = t.map_zero(rho)
    assert abs(rho_prime - tau * rho) < 1e-12
    
    # Function evaluation at transformed point matches zeta at original point
    val_transformed = t.evaluate_function(rho_prime, dps=35)
    val_orig = math_core.zeta_eval(rho, dps=35)
    assert abs(val_transformed - val_orig) < 1e-10


def test_vector_c_centered_dilation():
    """
    Vector C: K=1 Centered Coordinate Dilation.
    s' = 1/2 + tau * (s - 1/2)
    Expected image critical line: Re(s') = 1/2.
    Expected zero map: rho' = 1/2 + tau * (rho - 1/2).
    """
    t = transforms.CenteredCoordinateDilation(k=1.0)
    tau = float(math_core.get_tau(50))
    
    # Image critical line stays 1/2
    assert t.image_critical_line_str == "Re(s') = 1/2"
    
    # Zero map
    ref_zeros = reference_data.load_reference_zeros()
    gam_1 = float(ref_zeros[0]) if ref_zeros else 14.13472514173469379
    rho = complex(0.5, gam_1)
    rho_prime = t.map_zero(rho)
    expected_rho_prime = 0.5 + tau * (rho - 0.5)
    assert abs(rho_prime - expected_rho_prime) < 1e-12
    
    # Function evaluation matches
    val_transformed = t.evaluate_function(rho_prime, dps=35)
    val_orig = math_core.zeta_eval(rho, dps=35)
    assert abs(val_transformed - val_orig) < 1e-10


def test_argument_transform():
    """Test Argument Transform f_K(s) = zeta(tau^K * s)."""
    t = transforms.ArgumentTransform(k=1.0)
    tau = float(math_core.get_tau(50))
    
    # Zero map s_rho = rho / tau
    ref_zeros = reference_data.load_reference_zeros()
    gam_1 = float(ref_zeros[0]) if ref_zeros else 14.13472514173469379
    rho = complex(0.5, gam_1)
    s_rho = t.map_zero(rho)
    assert abs(s_rho - rho / tau) < 1e-12
    
    # Critical zero line Re(s) = 1 / (2 * tau)
    assert abs(s_rho.real - 1.0 / (2.0 * tau)) < 1e-12
    
    # Function evaluation at s_rho vanishes
    val_at_zero = t.evaluate_function(s_rho, dps=35)
    assert abs(val_at_zero) < 1e-9


def test_active_card_generation():
    """Verify Active Mathematics Card content is generated cleanly without errors."""
    for t_obj in [
        transforms.CameraTransform(),
        transforms.HeightMicroscopeTransform(k=0.5, t0=14.0, delta=0.01),
        transforms.OriginCoordinateDilation(k=1.25),
        transforms.CenteredCoordinateDilation(k=0.75),
        transforms.ArgumentTransform(k=-0.5),
        transforms.KernelTransform(A=2.0, B=0.5, inverse_scale_lock=True),
        transforms.CenteredKernelTransform(A=2.0, B=0.5),
        transforms.AnisotropicDeformation(A_delta=1.5, A_gamma=1.0)
    ]:
        card_md = t_obj.get_card_markdown()
        assert "MODE:" in card_md
        assert "Domain map:" in card_md
        assert "Function plotted:" in card_md
        assert "CLASS:" in card_md
