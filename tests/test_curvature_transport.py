"""
tests/test_curvature_transport.py — Verification suite for Curvature-Transport Unification,
Theta–Mellin Scaling, Grade Invariant Transport, and Countermodel Falsification.
"""

import pytest
import mpmath
import math_core


class TestRadialGeometryAndLattice:
    """Tests for circle circumference, radius, curvature, and Fourier lattice spacing."""

    @pytest.mark.parametrize("K", [-3, -1, 0, 1, 2, 5])
    def test_exact_radial_geometry_shift_laws(self, K):
        res = math_core.exact_radial_geometry(K=K, dps=50)
        assert res["status"] == "RADIAL_GEOMETRY_VERIFIED"
        assert res["is_symbolic_exact"] is True
        assert float(res["reciprocal_error"]) < 1e-45
        assert float(res["shift_r_error"]) < 1e-45
        assert float(res["shift_C_error"]) < 1e-45
        assert float(res["shift_kappa_error"]) < 1e-45
        assert float(res["unit_C1_error"]) < 1e-45

    def test_unit_circumference_at_K1(self):
        res = math_core.exact_radial_geometry(K=1, dps=50)
        tau = 2 * mpmath.pi
        expected_r1 = 1 / tau
        expected_C1 = mpmath.mpf(1)
        expected_kappa1 = tau

        assert abs(mpmath.mpf(res["r_K"]) - expected_r1) < 1e-45
        assert abs(mpmath.mpf(res["C_K"]) - expected_C1) < 1e-45
        assert abs(mpmath.mpf(res["kappa_K"]) - expected_kappa1) < 1e-45

    @pytest.mark.parametrize("K", [-2, -1, 0, 1, 3, 4])
    def test_fourier_lattice_spacing(self, K):
        res = math_core.fourier_lattice_spacing(K=K, dps=50)
        assert res["status"] == "FOURIER_LATTICE_SPACING_VERIFIED"
        assert res["is_symbolic_exact"] is True
        assert float(res["error"]) < 1e-45

    @pytest.mark.parametrize("b", [1.5, 2.0, 3.14159, 10.0])
    @pytest.mark.parametrize("K", [-2, 0, 3])
    def test_generic_scale_geometry_control(self, b, K):
        res = math_core.generic_scale_geometry(b=b, K=K, dps=50)
        assert res["status"] == "GENERIC_SCALE_GEOMETRY_VERIFIED"
        assert float(res["reciprocal_error"]) < 1e-45
        assert float(res["fourier_spacing_error"]) < 1e-45


class TestZeroAndRadialUnitTransport:
    """Tests for zero transport, radial-unit recovery, and grade-character modulus."""

    @pytest.mark.parametrize("delta", ["0.0", "0.001", "-0.05", "0.25"])
    @pytest.mark.parametrize("K", [-5, -1, 0, 2, 7])
    def test_transported_radial_defect(self, delta, K):
        res = math_core.transported_radial_defect(delta=delta, K=K, dps=50)
        assert res["status"] == "TRANSPORTED_RADIAL_DEFECT_VERIFIED"
        assert float(res["error_delta"]) < 1e-45
        assert float(res["error_sq"]) < 1e-45

    @pytest.mark.parametrize("delta,gamma,K", [
        ("0.0", "14.134725", "1.0"),
        ("0.002", "21.022040", "3.0"),
        ("-0.01", "30.424876", "-2.0"),
        ("0.1", "50.0", "0.5"),
    ])
    def test_grade_character_modulus_and_reciprocal(self, delta, gamma, K):
        res = math_core.grade_character_modulus(delta=delta, gamma=gamma, K=K, dps=50)
        assert res["status"] == "GRADE_CHARACTER_MODULUS_VERIFIED"
        assert float(res["abs_error"]) < 1e-45
        assert float(res["sharp_abs_error"]) < 1e-45
        assert float(res["reciprocal_error"]) < 1e-45


class TestReflectionPairCurvature:
    """Tests for reflection-pair defect formulas, nonnegativity, and native grade curvature."""

    @pytest.mark.parametrize("delta,K", [
        ("0.0", "2.0"),
        ("0.0001", "1.0"),
        ("0.01", "-3.0"),
        ("0.05", "0.5"),
        ("-0.02", "4.0"),
    ])
    def test_reflection_pair_defect_B_formulas(self, delta, K):
        res = math_core.reflection_pair_defect_B(delta=delta, K=K, dps=50)
        assert res["status"] == "REFLECTION_PAIR_DEFECT_VERIFIED"
        assert res["is_symbolic_exact"] is True
        assert res["is_nonnegative"] is True
        assert float(res["error_cosh"]) < 1e-45
        assert float(res["error_sinh"]) < 1e-45

    def test_reflection_pair_zero_rigidity(self):
        # On-line zero: delta = 0 => B == 0 for all K
        for K in [-5, -1, 1, 4]:
            res0 = math_core.reflection_pair_defect_B(delta="0.0", K=K, dps=50)
            assert abs(mpmath.mpf(res0["val_exp"])) < 1e-45

        # Off-line zero: delta != 0 => B > 0 for K != 0
        for K in [-3, -1, 1, 5]:
            res_pos = math_core.reflection_pair_defect_B(delta="0.001", K=K, dps=50)
            assert mpmath.mpf(res_pos["val_exp"]) > 0

    @pytest.mark.parametrize("delta", ["0.0", "0.0005", "0.01", "-0.025", "0.1"])
    def test_curvature_transport_invariant(self, delta):
        with mpmath.workdps(50):
            res = math_core.curvature_transport_invariant(delta=delta, h_step="1e-5", dps=50)
            assert res["status"] == "CURVATURE_TRANSPORT_INVARIANT_VERIFIED"
            assert float(res["derivative_error"]) < 1e-8
            assert float(res["curvature_error"]) < 1e-8

            # Exact algebraic value matches delta^2
            d_val = mpmath.mpf(delta)
            assert abs(mpmath.mpf(res["exact_curvature_invariant"]) - (d_val**2)) < 1e-45


class TestThetaMellinAndFalsificationControls:
    """Tests for theta-Mellin scaling, scalar multiplication obstruction, and countermodels."""

    @pytest.mark.parametrize("a", [0.5, 1.0, 2.0, 6.283185307179586])
    @pytest.mark.parametrize("s", [
        mpmath.mpc("2.0", "0.0"),
        mpmath.mpc("2.5", "3.0"),
        mpmath.mpc("3.0", "-1.5"),
    ])
    def test_theta_mellin_scaling(self, a, s):
        res = math_core.verify_theta_mellin_scaling(a=a, s=s, n_terms=150, dps=50)
        assert res["status"] == "THETA_MELLIN_SCALING_VERIFIED"
        assert float(res["error"]) < 1e-35

    @pytest.mark.parametrize("K", [-2, 0, 1, 3])
    @pytest.mark.parametrize("delta,gamma", [
        ("0.0", "14.134725"),
        ("0.01", "21.022040"),
    ])
    def test_scalar_zero_multiplication_obstruction(self, K, delta, gamma):
        res = math_core.verify_scalar_zero_multiplication_obstruction(K=K, delta=delta, gamma=gamma, dps=50)
        assert res["status"] == "SCALAR_ZERO_OBSTRUCTION_CONFIRMED"
        assert res["is_identically_zero"] is True

    @pytest.mark.parametrize("delta,gamma", [
        ("0.005", "14.134725"),
        ("0.02", "21.022040"),
        ("-0.01", "25.010857"),
    ])
    def test_countermodel_symmetries_and_curvature(self, delta, gamma):
        res = math_core.verify_countermodel_symmetries(delta=delta, gamma=gamma, dps=50)
        assert res["status"] == "COUNTERMODEL_SYMMETRIES_VERIFIED"
        assert float(res["even_symmetry_error"]) < 1e-45
        assert float(res["schwarz_symmetry_error"]) < 1e-45
        assert float(res["max_root_residual"]) < 1e-45
        assert mpmath.mpf(res["grade_curvature"]) > 0
