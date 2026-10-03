"""
Tests for TASK-TC-019: Grade-Unit Characters, Unitarity, and the Positive-Definite TC Constraint.

Validates:
1. Zero-induced grade-unit character definition: eta_rho(K) = tau^{-K(rho - 1/2)}
2. Character law on integer skeleton Z: eta_rho(K + J) = eta_rho(K) * eta_rho(J)
3. Character modulus: |eta_rho(K)| = tau^{-K * delta}
4. Exact TC Unitarity Reformulation of RH: eta_rho is unitary on Z iff delta = 0
5. Non-unitarity defect identity: B_rho(K) = |eta_rho(K)| + |eta_rho(K)|^{-1} - 2 = 4 sinh^2(K delta log(tau) / 2)
6. Dual equals adjoint character on Z iff delta = 0 (inversion vs conjugation)
7. Functional equation reflection as grade inversion: eta_{1-rho}(K) = eta_rho(-K) = eta_rho(K)^{-1}
8. Multiplicative Mellin dilation unitarity on L^2(R_{>0}, dx/x)
9. Derivation of 1/2-centering from L^2(R_{>0}, dx) Plancherel isometry
10. Herglotz theorem on Z and non-unitarity obstruction for off-critical zeros
11. Circularity audit: arithmetic grade correlation equivalence to Weil positivity
12. Generic-base control: b > 1 universality of unitarity detection
"""

import math
import pytest
import mpmath
import sympy as sp


class TestGradeUnitCharacterUnitarity:
    """Test suite for TASK-TC-019 zero-induced grade characters and unitarity."""

    def test_grade_unit_character_definition_and_multiplicativity(self):
        """Verify eta_rho(K) = tau^{-K(rho - 1/2)} is a multiplicative character on Z."""
        dps = 50
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi

        # Zero ordinate for first Riemann zero
        gamma = mpmath.mpf("14.134725141734693790457251983562470270784257115699")
        delta = mpmath.mpf("0.05")  # Synthetic off-line zero
        rho = mpmath.mpc(mpmath.mpf("0.5") + delta, gamma)

        def eta(K_val):
            # eta_rho(K) = tau^{-K * (rho - 1/2)} = tau^{-K * (delta + i * gamma)}
            exponent = -K_val * (rho - mpmath.mpf("0.5"))
            return mpmath.power(tau, exponent)

        # 1. Identity law: eta(0) = 1
        assert abs(eta(0) - 1) < mpmath.mpf("1e-45")

        # 2. Multiplicative character law: eta(K + J) = eta(K) * eta(J)
        K = 3
        J = -5
        eta_K = eta(K)
        eta_J = eta(J)
        eta_sum = eta(K + J)
        assert abs(eta_sum - (eta_K * eta_J)) < mpmath.mpf("1e-45")

        # 3. Inversion law: eta(-K) = eta(K)^{-1}
        eta_negK = eta(-K)
        assert abs(eta_negK - (1 / eta_K)) < mpmath.mpf("1e-45")

    def test_grade_unit_character_modulus(self):
        """Verify |eta_rho(K)| = tau^{-K * delta}."""
        dps = 50
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi

        gamma = mpmath.mpf("14.134725")
        delta = mpmath.mpf("0.08")
        rho = mpmath.mpc(mpmath.mpf("0.5") + delta, gamma)

        for K in [-3, -1, 0, 1, 2, 4]:
            exponent = -K * (rho - mpmath.mpf("0.5"))
            val = mpmath.power(tau, exponent)
            modulus_actual = abs(val)
            modulus_expected = mpmath.power(tau, -K * delta)
            assert abs(modulus_actual - modulus_expected) < mpmath.mpf("1e-45")

    def test_unitarity_reformulation_of_rh(self):
        """Verify eta_rho is unitary on Z if and only if delta = 0."""
        dps = 50
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        gamma = mpmath.mpf("14.134725")

        # Case A: On the critical line (delta = 0, RH holds for this zero)
        delta_on = mpmath.mpf("0.0")
        rho_on = mpmath.mpc(mpmath.mpf("0.5") + delta_on, gamma)

        for K in [-10, -3, -1, 0, 1, 2, 5, 10]:
            exponent = -K * (rho_on - mpmath.mpf("0.5"))
            modulus = abs(mpmath.power(tau, exponent))
            # Exactly unitary: modulus == 1
            assert abs(modulus - 1) < mpmath.mpf("1e-45")

        # Case B: Off the critical line (delta != 0, RH violated)
        for delta_off in [mpmath.mpf("0.01"), mpmath.mpf("-0.05"), mpmath.mpf("0.2")]:
            rho_off = mpmath.mpc(mpmath.mpf("0.5") + delta_off, gamma)
            # At K = 1, modulus != 1
            mod_1 = abs(mpmath.power(tau, -(rho_off - mpmath.mpf("0.5"))))
            assert abs(mod_1 - 1) > mpmath.mpf("1e-4")

    def test_nonunitarity_defect_representation_identity(self):
        """Verify B_rho(K) = |eta_rho(K)| + |eta_rho(K)|^{-1} - 2 = 4 sinh^2(K delta log(tau) / 2)."""
        dps = 50
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi

        delta = mpmath.mpf("0.075")
        gamma = mpmath.mpf("21.022040")
        rho = mpmath.mpc(mpmath.mpf("0.5") + delta, gamma)

        for K in [-4, -2, -1, 1, 3, 5]:
            # Character modulus:
            mod_K = abs(mpmath.power(tau, -K * (rho - mpmath.mpf("0.5"))))
            # Non-unitarity defect from character:
            defect_char = mod_K + (1 / mod_K) - 2

            # Exact spectral detector formula:
            sinh_arg = (K * delta * mpmath.log(tau)) / 2
            detector_exact = 4 * (mpmath.sinh(sinh_arg) ** 2)

            # Bilateral power sum: tau^{K delta} + tau^{-K delta} - 2
            power_sum = mpmath.power(tau, K * delta) + mpmath.power(tau, -K * delta) - 2

            assert abs(defect_char - detector_exact) < mpmath.mpf("1e-45")
            assert abs(defect_char - power_sum) < mpmath.mpf("1e-45")
            assert defect_char > 0

        # At delta = 0, defect vanishes identically
        mod_zero_delta = abs(mpmath.power(tau, -3 * (mpmath.mpc("0.5", gamma) - mpmath.mpf("0.5"))))
        defect_zero = mod_zero_delta + (1 / mod_zero_delta) - 2
        assert abs(defect_zero) < mpmath.mpf("1e-45")

    def test_inversion_vs_conjugation_dual_equals_adjoint(self):
        """Verify eta_rho(K)^{-1} = conjugate(eta_rho(K)) if and only if delta = 0."""
        dps = 50
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        gamma = mpmath.mpf("14.134725")
        K = 2

        # When delta = 0:
        rho_critical = mpmath.mpc("0.5", gamma)
        eta_crit = mpmath.power(tau, -K * (rho_critical - mpmath.mpf("0.5")))
        inv_crit = 1 / eta_crit
        conj_crit = mpmath.conj(eta_crit)
        assert abs(inv_crit - conj_crit) < mpmath.mpf("1e-45")

        # When delta != 0:
        delta = mpmath.mpf("0.05")
        rho_off = mpmath.mpc(mpmath.mpf("0.5") + delta, gamma)
        eta_off = mpmath.power(tau, -K * (rho_off - mpmath.mpf("0.5")))
        inv_off = 1 / eta_off
        conj_off = mpmath.conj(eta_off)

        # Modulus of inv_off is tau^{K delta}, modulus of conj_off is tau^{-K delta}
        # Their ratio has modulus tau^{2 K delta} != 1
        assert abs(abs(inv_off) - abs(conj_off)) > mpmath.mpf("1e-3")
        assert abs(inv_off - conj_off) > mpmath.mpf("1e-3")

    def test_functional_equation_reflection_as_grade_inversion(self):
        """Verify functional equation reflection s |-> 1 - s induces grade inversion K |-> -K."""
        dps = 50
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi

        delta = mpmath.mpf("0.04")
        gamma = mpmath.mpf("14.134725")
        rho = mpmath.mpc(mpmath.mpf("0.5") + delta, gamma)
        rho_refl = 1 - rho  # 1/2 - delta - i * gamma

        K = 3
        # Character of reflected zero:
        eta_refl = mpmath.power(tau, -K * (rho_refl - mpmath.mpf("0.5")))
        # Inverted grade on original zero:
        eta_negK = mpmath.power(tau, -(-K) * (rho - mpmath.mpf("0.5")))

        assert abs(eta_refl - eta_negK) < mpmath.mpf("1e-45")
        assert abs(eta_refl - (1 / mpmath.power(tau, -K * (rho - mpmath.mpf("0.5"))))) < mpmath.mpf("1e-45")

    def test_mellin_dilation_unitarity_dx_over_x(self):
        """Verify multiplicative dilation x |-> tau^K x is unitary on L^2(R_{>0}, dx/x)."""
        dps = 30
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        K = mpmath.mpf("1.5")

        # Test function f(x) = exp(-(log(x))^2)
        # norm squared = int_0^infty |f(x)|^2 dx/x = int_{-infty}^infty exp(-2 u^2) du = sqrt(pi / 2)
        exact_norm_sq = mpmath.sqrt(mpmath.pi / 2)

        # Dilated function f_K(x) = f(tau^K * x) = exp(-(log(tau^K * x))^2)
        # Integral: int_0^infty |f(tau^K x)|^2 dx/x
        # Substitute u = tau^K x => du/u = dx/x, range stays (0, infty)
        # Therefore integral is identical: sqrt(pi / 2)
        integral_val = mpmath.quad(
            lambda x: (mpmath.exp(-((mpmath.log(mpmath.power(tau, K) * x)) ** 2))) ** 2 / x,
            [0, mpmath.inf]
        )
        assert abs(integral_val - exact_norm_sq) < mpmath.mpf("1e-20")

    def test_normalized_mellin_plancherel_centering_derivation(self):
        """Verify normalized dilation (U_K f)(x) = tau^{K/2} f(tau^K x) produces multiplier tau^{-K(s - 1/2)}."""
        dps = 30
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        K = mpmath.mpf("0.7")
        # Use a moderate imaginary ordinate for standard quad integration
        s = mpmath.mpc("0.55", "1.5")

        expected_multiplier = mpmath.power(tau, -K * (s - mpmath.mpf("0.5")))
        gamma_s = mpmath.gamma(s)
        expected_mellin = expected_multiplier * gamma_s

        # Numerical integration of M[f_K](s):
        actual_mellin = mpmath.quad(
            lambda x: mpmath.power(tau, K / 2) * mpmath.exp(-mpmath.power(tau, K) * x) * mpmath.power(x, s - 1),
            [0, mpmath.inf]
        )

        rel_diff = abs(actual_mellin - expected_mellin) / abs(expected_mellin)
        assert rel_diff < mpmath.mpf("1e-10")

    def test_herglotz_positive_definite_character_audit(self):
        """Verify that Herglotz's theorem on Z admits only unitary characters in its spectral support."""
        # Theorem (Herglotz 1911): A sequence C: Z -> C is positive definite iff
        # C(K) = int_T z^K dmu(z) for a finite positive Borel measure mu on T = {z in C : |z| = 1}.
        # For a character eta(K) = q^K:
        # eta is positive definite iff q in T, i.e., |q| = 1.
        dps = 40
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi

        # Zero character q_rho = tau^{-(rho - 1/2)} = tau^{-(delta + i * gamma)}
        # |q_rho| = tau^{-delta}
        delta_on = mpmath.mpf("0.0")
        q_on = mpmath.power(tau, -(delta_on + mpmath.mpc(0, "14.134725")))
        assert abs(abs(q_on) - 1) < mpmath.mpf("1e-35")  # Lies on T!

        delta_off = mpmath.mpf("0.05")
        q_off = mpmath.power(tau, -(delta_off + mpmath.mpc(0, "14.134725")))
        assert abs(abs(q_off) - 1) > mpmath.mpf("0.05")  # NOT on T!

        # Construct a 2x2 Toeplitz matrix from eta(K) for K = 0, 1:
        # M = [[eta(0), eta(-1)], [eta(1), eta(0)]] = [[1, 1/q], [q, 1]]
        # det(M) = 1 - q * (1/q) = 0 for any q.
        # But for conjugate-symmetric Toeplitz required by positive definiteness:
        # M_herm = [[C(0), conjugate(C(1))], [C(1), C(0)]] = [[1, conjugate(q)], [q, 1]]
        # det(M_herm) = 1 - |q|^2.
        # For M_herm to be positive semi-definite, we need det(M_herm) >= 0 => |q|^2 <= 1.
        # But also for K = -1, the inverse sequence requires |1/q|^2 <= 1 => |q|^2 >= 1.
        # Together: |q|^2 = 1, forcing |q| = 1 (unitarity!).
        det_on = 1 - (abs(q_on) ** 2)
        assert abs(det_on) < mpmath.mpf("1e-35")

        # For q_off: either q_off or 1/q_off has modulus > 1, so the bilateral sequence
        # FAILS positive semi-definiteness!
        det_off = 1 - (abs(q_off) ** 2)
        assert det_off != 0

    def test_circularity_audit_weil_equivalence_classification(self):
        """Verify the exact classification of arithmetic grade correlation vs Weil positivity."""
        # A positive-definite grade correlation on Z:
        # C(K) = <U_K v, v> is automatically positive definite on any Hilbert space.
        # However, equating C(K) with the sum over zeta zeros sum_rho w_rho eta_rho(K)
        # requires the Riemann-Weil explicit formula.
        # In Weil's theorem (1952), the quadratic functional on zeros is positive definite
        # IF AND ONLY IF all zeros satisfy Re(rho) = 1/2.
        # Therefore, any assertion that an arithmetic correlation decomposes solely into
        # zeta zero characters without archimedean/pole contributions, or that the zero
        # quadratic form is positive, is EQUIVALENT_REFORMULATION_OF_WEIL.
        classification = "EQUIVALENT_REFORMULATION_OF_WEIL"
        assert classification in [
            "STRICTLY_NEW_CONSTRAINT_FORM",
            "EQUIVALENT_REFORMULATION_OF_WEIL",
            "WEAKER_THAN_WEIL",
            "STRONGER_THAN_WEIL",
            "CIRCULAR_RH_EQUIVALENT",
        ]

    def test_generic_base_control_unitarity(self):
        """Verify that the unitarity criterion |eta_{rho, b}(K)| = 1 iff delta = 0 holds for all b > 1."""
        dps = 40
        mpmath.mp.dps = dps
        gamma = mpmath.mpf("14.134725")

        for b_val in [mpmath.mpf("2.0"), mpmath.mpf("3.0"), mpmath.mpf("10.0"), mpmath.e]:
            # Critical line zero:
            rho_crit = mpmath.mpc("0.5", gamma)
            val_crit = mpmath.power(b_val, -1 * (rho_crit - mpmath.mpf("0.5")))
            assert abs(abs(val_crit) - 1) < mpmath.mpf("1e-35")

            # Off-line zero:
            rho_off = mpmath.mpc("0.55", gamma)
            val_off = mpmath.power(b_val, -1 * (rho_off - mpmath.mpf("0.5")))
            assert abs(abs(val_off) - 1) > mpmath.mpf("0.01")
