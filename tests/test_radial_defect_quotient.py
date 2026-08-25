"""tests/test_radial_defect_quotient.py — High-Precision Verification Suite for Radial-Defect Quotient Q(z), L_Q, and Fredholm Theory

Tests exact mathematical identities and audited properties:
1. Quartet multiplicity and q(x) positivity/boundedness: 0 < q_{delta, gamma}(x) <= 1 with equality iff x=0 (delta != 0).
2. On-line zeros (delta = 0) yield q(x) == 1 identically.
3. Exact minimum location x_* = sqrt(delta^2 + 3*gamma^2) and minimum value q_min = 4 / [ (1+r)^2 * (4+r) ].
4. Exact uniform log-bound: sup_x |log q(x)| = 2*log(1+r) + log(1+r/4) <= (9/4)*r.
5. Limiting invariant L_Q = lim_{x->infty} Q(x) = (1+r)^(-2) per quartet, with 0 < L_Q <= 1 and L_Q = 1 iff delta = 0.
6. Grade invariance: q(x), Q(z), L_Q, and R are invariant under uniform coordinate dilation (x, delta, gamma) -> (tau^K x, tau^K delta, tau^K gamma).
7. Exact H = log z projection-subtraction identity: 2*Re log(delta + i*gamma) - 2*Re log(i*gamma) = log(1 + delta^2/gamma^2) = d(delta, gamma).
8. Relative Fredholm determinant bookkeeping: det(I + R_fin) = L_Q_fin^(-1), log det(I + R_fin) = Tr log(I + R_fin).
9. Involution pairing kernel: kappa_1(z, z^#) = delta^2 / gamma^2 for z = delta + i*gamma and z^# = -conj(z).
10. Finite trace zero-equivalence: Tr(R_fin) == 0 iff all delta_i == 0.
"""

import mpmath
import pytest
from math_core import (
    radial_factor_q,
    radial_factor_q_min,
    radial_factor_q_min_x,
    radial_factor_log_bound,
    projection_subtracted_defect_d,
    involution_pairing_kernel_kappa1,
    finite_radial_operator_trace,
    finite_radial_fredholm_det,
    finite_radial_defect_quotient_limit,
    to_mpf,
    to_mpc,
    get_tau,
)


class TestRadialFactorProperties:
    """Verifies audited analytical properties of the real-axis quartet factor q_{delta, gamma}(x)."""

    def test_online_zero_factor_identity(self):
        """When delta = 0, q_{0, gamma}(x) == 1 identically for all x."""
        with mpmath.workdps(80):
            gamma = mpmath.mpf('14.134725141734693790457251983562470270784257115699243175685567460149963429809256765')
            for x_val in ['0', '1', '10', '100', '-50']:
                q_val = radial_factor_q(x_val, '0', gamma, dps=80)
                assert q_val == mpmath.mpf('1.0')

    def test_positivity_and_boundedness(self):
        """For delta != 0, 0 < q_{delta, gamma}(x) <= 1 with equality iff x = 0."""
        with mpmath.workdps(80):
            gamma = mpmath.mpf('14.134725141734693790457251983562470270784257115699243175685567460149963429809256765')
            delta = mpmath.mpf('0.1')

            # At x = 0, q = 1 exactly
            q_zero = radial_factor_q('0', delta, gamma, dps=80)
            assert mpmath.almosteq(q_zero, mpmath.mpf('1.0'), abs_eps=mpmath.mpf('1e-75'))

            # For various non-zero x, 0 < q < 1 strictly
            test_x = ['0.001', '1.0', '10.0', '25.0', '100.0', '1000.0', '-15.0']
            for x_str in test_x:
                q_val = radial_factor_q(x_str, delta, gamma, dps=80)
                assert q_val > 0
                assert q_val < 1

    def test_exact_minimum_location_and_value(self):
        """The unique minimum occurs at x_*^2 = delta^2 + 3*gamma^2, with value q_min = 4 / [ (1+r)^2 * (4+r) ]."""
        with mpmath.workdps(80):
            gamma = mpmath.mpf('21.0220396387715549926284795938969027773343405240800097280697728819448216345688564')
            delta = mpmath.mpf('0.05')

            x_star = radial_factor_q_min_x(delta, gamma, dps=80)
            q_min_formula = radial_factor_q_min(delta, gamma, dps=80)
            q_at_x_star = radial_factor_q(x_star, delta, gamma, dps=80)

            # Check value matches formula
            assert mpmath.almosteq(q_at_x_star, q_min_formula, abs_eps=mpmath.mpf('1e-75'))

            # Check that slightly perturbed x values give larger q (local minimum test)
            eps = mpmath.mpf('1e-4')
            q_left = radial_factor_q(x_star - eps, delta, gamma, dps=80)
            q_right = radial_factor_q(x_star + eps, delta, gamma, dps=80)
            assert q_left > q_at_x_star
            assert q_right > q_at_x_star

    def test_exact_uniform_log_bound(self):
        """sup_x |log q(x)| = 2*log(1+r) + log(1+r/4) <= (9/4)*r where r = delta^2 / gamma^2."""
        with mpmath.workdps(80):
            gamma = mpmath.mpf('14.134725141734693790457251983562470270784257115699243175685567460149963429809256765')
            delta = mpmath.mpf('0.2')

            r = (delta * delta) / (gamma * gamma)
            exact_sup_log = radial_factor_log_bound(delta, gamma, dps=80)
            linear_bound = (mpmath.mpf(9) / mpmath.mpf(4)) * r

            # Exact bound is <= (9/4)*r
            assert exact_sup_log <= linear_bound

            # Check that |log q(x)| <= exact_sup_log for many sampled points
            x_star = radial_factor_q_min_x(delta, gamma, dps=80)
            sample_points = ['0.01', '1.0', '5.0', str(x_star), '50.0', '200.0', '10000.0']
            for x_s in sample_points:
                q_val = radial_factor_q(x_s, delta, gamma, dps=80)
                abs_log_q = abs(mpmath.log(q_val))
                assert abs_log_q <= exact_sup_log + mpmath.mpf('1e-75')

    def test_asymptotic_limit(self):
        """lim_{x->infty} q_{delta, gamma}(x) = (gamma^2 / (gamma^2 + delta^2))^2 = (1 + r)^(-2)."""
        with mpmath.workdps(80):
            gamma = mpmath.mpf('14.134725141734693790457251983562470270784257115699243175685567460149963429809256765')
            delta = mpmath.mpf('0.15')
            r = (delta * delta) / (gamma * gamma)
            expected_limit = mpmath.mpf(1) / ((mpmath.mpf(1) + r) * (mpmath.mpf(1) + r))

            # Very large x
            x_large = mpmath.mpf('1e20')
            q_large = radial_factor_q(x_large, delta, gamma, dps=80)
            assert mpmath.almosteq(q_large, expected_limit, abs_eps=mpmath.mpf('1e-35'))

    def test_grade_invariance(self):
        """q_{delta, gamma}(x) is invariant under uniform coordinate dilation (x, delta, gamma) -> (tau^K x, tau^K delta, tau^K gamma)."""
        with mpmath.workdps(80):
            tau = get_tau(dps=80)
            gamma = mpmath.mpf('25.0108575801456887632137909925628218186595503025257913077395041042735787611029285')
            delta = mpmath.mpf('0.08')
            x = mpmath.mpf('35.5')

            q_native = radial_factor_q(x, delta, gamma, dps=80)

            for K in [-3, -2, -1, 1, 2, 3]:
                scale = tau ** K
                q_scaled = radial_factor_q(x * scale, delta * scale, gamma * scale, dps=80)
                assert mpmath.almosteq(q_native, q_scaled, abs_eps=mpmath.mpf('1e-75'))


    def test_exact_symbolic_factorization_one_minus_q(self):
        r"""Exact symbolic regression test verifying:
        1 - q_{\delta,\gamma}(x) \equiv \frac{\delta^2 x^2 [(\delta^2 + 2\gamma^2)x^2 + 2\gamma^2(\delta^2 + 3\gamma^2)]}{(\delta^2+\gamma^2)^2 (x^2+\gamma^2)^2}.
        """
        import sympy as sp
        x, d, g = sp.symbols('x delta gamma', real=True)
        q_expr = (g**4 * ((x**2 + g**2 - d**2)**2 + 4 * d**2 * g**2)) / ((g**2 + d**2)**2 * (x**2 + g**2)**2)
        one_minus_q_direct = 1 - q_expr
        one_minus_q_formula = (d**2 * x**2 * ((d**2 + 2 * g**2) * x**2 + 2 * g**2 * (d**2 + 3 * g**2))) / ((d**2 + g**2)**2 * (x**2 + g**2)**2)
        diff = sp.simplify(one_minus_q_direct - one_minus_q_formula)
        assert diff == 0


class TestExplicitFormulaProjectionIdentity:
    """Verifies the exact identity between H = log z projection-subtraction and L_Q defect."""

    def test_exact_log_projection_subtraction_identity(self):
        """2*Re log(delta + i*gamma) - 2*Re log(i*gamma) = log(1 + delta^2/gamma^2) = d(delta, gamma)."""
        with mpmath.workdps(80):
            gamma = mpmath.mpf('14.134725141734693790457251983562470270784257115699243175685567460149963429809256765')
            delta = mpmath.mpf('0.12')

            z_actual = mpmath.mpc(delta, gamma)
            z_projected = mpmath.mpc('0', gamma)

            response_actual = mpmath.mpf(2) * mpmath.re(mpmath.log(z_actual))
            response_projected = mpmath.mpf(2) * mpmath.re(mpmath.log(z_projected))
            diff_response = response_actual - response_projected

            d_val = projection_subtracted_defect_d(delta, gamma, dps=80)
            assert mpmath.almosteq(diff_response, d_val, abs_eps=mpmath.mpf('1e-75'))


class TestRelativeFredholmAndInvolutionKernel:
    """Verifies the relative Fredholm spectral operator, trace, determinant, and involution kernel kappa_1."""

    def test_involution_pairing_kernel_identity(self):
        """kappa_1(z, z^#) = delta^2 / gamma^2 identically for z = delta + i*gamma and z^# = -conj(z)."""
        with mpmath.workdps(80):
            test_cases = [
                ('0.0', '14.134725141734693790457251983562470270784257115699243175685567460149963429809256765'),
                ('0.01', '21.0220396387715549926284795938969027773343405240800097280697728819448216345688564'),
                ('0.25', '25.0108575801456887632137909925628218186595503025257913077395041042735787611029285'),
                ('-0.15', '30.4248761258595132103118975305840213005930600857105404054974154970420912180405298'),
            ]
            for d_str, g_str in test_cases:
                d_m = to_mpf(d_str, dps=80)
                g_m = to_mpf(g_str, dps=80)
                z = mpmath.mpc(d_m, g_m)
                z_sharp = mpmath.mpc(-d_m, g_m)  # -conj(z) = -delta + i*gamma

                k1_val = involution_pairing_kernel_kappa1(z, z_sharp, dps=80)
                expected_ratio = (d_m * d_m) / (g_m * g_m)

                assert mpmath.almosteq(k1_val.real, expected_ratio, abs_eps=mpmath.mpf('1e-75'))
                assert mpmath.almosteq(k1_val.imag, mpmath.mpf('0.0'), abs_eps=mpmath.mpf('1e-75'))

    def test_finite_trace_and_determinant_bookkeeping(self):
        """Tr(R) = sum (delta_i^2 / gamma_i^2), det(I + R_fin) = L_Q_fin^(-1), log det(I + R_fin) = Tr log(I + R_fin).
        
        Properly represents:
        - both upper-half-plane members (+delta + i*gamma) and (-delta + i*gamma) of each off-line quartet;
        - multiplicities n > 1;
        - mixed on-line and off-line zeros at the same height;
        - direct invocation and equality with finite_radial_defect_quotient_limit.
        """
        with mpmath.workdps(80):
            g1 = '14.134725141734693790457251983562470270784257115699243175685567460149963429809256765'
            g2 = '21.0220396387715549926284795938969027773343405240800097280697728819448216345688564'
            g3 = '25.0108575801456887632137909925628218186595503025257913077395041042735787611029285'

            d1 = '0.05'
            d2 = '0.10'

            # Define quartets:
            # - Quartet 1 at height g2 with displacement d1 (multiplicity 1)
            # - Quartet 2 at height g3 with displacement d2 (multiplicity 2)
            quartets = [
                (d1, g2),
                (d2, g3),
                (d2, g3),  # Multiplicity 2
            ]

            # In upper half-plane Lambda^+, each off-line quartet has two roots (+-delta + i*gamma).
            # We also include mixed on-line zeros at g1 (multiplicity 2) and g2 (multiplicity 1, coexisting with quartet 1).
            zeros_upper = [
                # On-line zeros at g1
                ('0.0', g1),
                ('0.0', g1),
                # Mixed on-line zero at g2
                ('0.0', g2),
                # Quartet 1 upper members at g2 (+- d1 + i*g2)
                (d1, g2),
                (f'-{d1}', g2),
                # Quartet 2 upper members at g3 (multiplicity 2 -> 2 pairs of +- d2 + i*g3)
                (d2, g3),
                (f'-{d2}', g3),
                (d2, g3),
                (f'-{d2}', g3),
            ]

            # Trace of R over Lambda^+
            trace_val = finite_radial_operator_trace(zeros_upper, dps=80)
            det_val = finite_radial_fredholm_det(zeros_upper, t=1, dps=80)
            lq_val = finite_radial_defect_quotient_limit(quartets, dps=80)

            # Verification of exact identities:
            # 1. det(I + R_fin) == L_Q_fin^(-1)
            assert mpmath.almosteq(det_val, mpmath.mpf(1) / lq_val, abs_eps=mpmath.mpf('1e-75'))

            # 2. log det(I + R_fin) == -log L_Q_fin
            assert mpmath.almosteq(mpmath.log(det_val), -mpmath.log(lq_val), abs_eps=mpmath.mpf('1e-75'))

            # 3. Explicit ratio sum
            r1 = (to_mpf(d1, dps=80) ** 2) / (to_mpf(g2, dps=80) ** 2)
            r2 = (to_mpf(d2, dps=80) ** 2) / (to_mpf(g3, dps=80) ** 2)
            expected_trace = 2 * r1 + 4 * r2  # 2 upper zeros for quartet 1, 4 for quartet 2
            assert mpmath.almosteq(trace_val, expected_trace, abs_eps=mpmath.mpf('1e-75'))

    def test_finite_trace_zero_equivalence(self):
        """Tr(R_fin) == 0 iff all delta_i == 0."""
        with mpmath.workdps(80):
            # All on-line zeros
            online_zeros = [
                ('0.0', '14.134725141734693790457251983562470270784257115699243175685567460149963429809256765'),
                ('0.0', '21.0220396387715549926284795938969027773343405240800097280697728819448216345688564'),
                ('0.0', '25.0108575801456887632137909925628218186595503025257913077395041042735787611029285'),
            ]
            trace_zero = finite_radial_operator_trace(online_zeros, dps=80)
            det_one = finite_radial_fredholm_det(online_zeros, t=1, dps=80)
            assert trace_zero == mpmath.mpf(0)
            assert det_one == mpmath.mpf(1)

            # With one off-line zero
            mixed_zeros = online_zeros + [('0.001', '30.4248761258595132103118975305840213005930600857105404054974154970420912180405298')]
            trace_nonzero = finite_radial_operator_trace(mixed_zeros, dps=80)
            det_gt_one = finite_radial_fredholm_det(mixed_zeros, t=1, dps=80)
            assert trace_nonzero > 0
            assert det_gt_one > 1
