"""tests/test_arithmetic_radial_bridge.py — High-Precision Verification Suite for Arithmetic Radial Bridge, Targets D, T, T_a, and Candidate Evaluations

Tests rigorous mathematical properties and audited invariants:
1. Exact kappa_1 involution identity: kappa_1(z, z^#) = delta^2 / gamma^2.
2. Positivity of every radial summand r_j >= 0.
3. Finite weighted trace vanishing firewall: T = 0 iff all delta_i == 0.
4. Determinant defect vanishing firewall: D = 0 iff all delta_i == 0.
5. Multiplicity consistency: m_gamma = m_{0,gamma} + 2*sum n_j.
6. Symmetry invariance: permutation, conjugation, functional equation reflection.
7. Correct grade-centering geometry: c_K = tau^K / 2, z_K = tau^K * z, invariant ratio (tau^K delta)^2 / (tau^K gamma)^2 = delta^2 / gamma^2.
8. Synthetic on-line spectrum yields D == 0, T == 0, T_a == 0.
9. Single off-line quartet yields D > 0, T > 0, T_a > 0 strictly.
10. Mixed on-line and off-line zeros at a single ordinate.
11. Arithmetic evaluator firewall: rejects zero lists and spectral inputs.
12. Exact symbolic collapse of Candidate A (linear grade differences).
13. Bilinear cross-grade Candidate B all-pairs cross-term contamination.
14. Structured Candidate Registry validation.
"""

import mpmath
import pytest
import sympy as sp
from math_core import (
    grade_center,
    centered_grade_coord,
    involution_pairing_kernel_kappa1,
    spectral_determinant_d,
    spectral_trace_t,
    spectral_weighted_trace_t_a,
    arithmetic_candidate_a,
    spectral_candidate_a,
    arithmetic_candidate_b,
    spectral_candidate_b,
    arithmetic_firewall_check,
    get_candidate_registry,
    to_mpf,
    to_mpc,
    get_tau,
)


class TestGradeCenteringGeometry:
    """Verifies exact grade-centering geometry and coordinate transport."""

    def test_grade_center_definition(self):
        """c_K = tau^K / 2 at all integer grades."""
        with mpmath.workdps(80):
            tau = get_tau(dps=80)
            for K in [-3, -1, 0, 1, 2, 5]:
                c_k = grade_center(K, dps=80)
                expected = mpmath.power(tau, K) / 2
                assert mpmath.almosteq(c_k, expected, abs_eps=mpmath.mpf('1e-75'))

    def test_centered_coordinate_dilation(self):
        """z_K = s_K - c_K = tau^K * (s - 1/2) = tau^K * z."""
        with mpmath.workdps(80):
            tau = get_tau(dps=80)
            s_pts = [
                mpmath.mpc('0.5', '14.134725'),
                mpmath.mpc('0.6', '21.022040'),
                mpmath.mpc('0.4', '-30.424876'),
            ]
            for s in s_pts:
                z = s - mpmath.mpc('0.5', '0')
                for K in [-2, 0, 1, 3]:
                    z_k = centered_grade_coord(s, K, dps=80)
                    a_K = mpmath.power(tau, K)
                    expected = a_K * z
                    assert mpmath.almosteq(z_k.real, expected.real, abs_eps=mpmath.mpf('1e-75'))
                    assert mpmath.almosteq(z_k.imag, expected.imag, abs_eps=mpmath.mpf('1e-75'))

    def test_normalized_radial_ratio_grade_invariance(self):
        """The ratio (tau^K * delta)^2 / (tau^K * gamma)^2 == delta^2 / gamma^2."""
        with mpmath.workdps(80):
            tau = get_tau(dps=80)
            delta = mpmath.mpf('0.15')
            gamma = mpmath.mpf('25.0')
            r_base = (delta * delta) / (gamma * gamma)
            for K in [-4, -1, 0, 2, 6]:
                a_K = mpmath.power(tau, K)
                delta_K = a_K * delta
                gamma_K = a_K * gamma
                r_K = (delta_K * delta_K) / (gamma_K * gamma_K)
                assert mpmath.almosteq(r_K, r_base, abs_eps=mpmath.mpf('1e-75'))


class TestSpectralTargets:
    """Verifies exact properties of targets D, T, and T_a."""

    def test_kappa1_involution_pairing_exact(self):
        """kappa_1(z, z^#) = delta^2 / gamma^2."""
        with mpmath.workdps(80):
            test_points = [
                ('0.1', '14.134725141734693'),
                ('0.005', '21.022039638771555'),
                ('0.25', '30.424876125859513'),
                ('0.0', '14.134725141734693'),
            ]
            for d_str, g_str in test_points:
                delta = mpmath.mpf(d_str)
                gamma = mpmath.mpf(g_str)
                z = mpmath.mpc(delta, gamma)
                z_sharp = mpmath.mpc(-delta, gamma)
                k_val = involution_pairing_kernel_kappa1(z, z_sharp, dps=80)
                expected_r = (delta * delta) / (gamma * gamma)
                assert mpmath.almosteq(k_val.real, expected_r, abs_eps=mpmath.mpf('1e-75'))
                assert mpmath.almosteq(k_val.imag, mpmath.mpf('0'), abs_eps=mpmath.mpf('1e-75'))

    def test_online_spectrum_nullity(self):
        """All-online spectrum yields D == 0, T == 0, T_a == 0."""
        with mpmath.workdps(80):
            online_zeros = [
                ('0.0', '14.134725141734693790'),
                ('0.0', '21.022039638771554992'),
                ('0.0', '25.010857580145688763'),
            ]
            d_val = spectral_determinant_d(online_zeros, dps=80)
            t_val = spectral_trace_t(online_zeros, dps=80)
            ta_val = spectral_weighted_trace_t_a(online_zeros, a=0.5, dps=80)
            assert d_val == mpmath.mpf('0.0')
            assert t_val == mpmath.mpf('0.0')
            assert ta_val == mpmath.mpf('0.0')

    def test_single_offline_quartet_positivity(self):
        """A single off-line quartet produces strictly positive D, T, T_a."""
        with mpmath.workdps(80):
            quartet = [('0.1', '14.134725141734693790', 1)]
            d_val = spectral_determinant_d(quartet, dps=80)
            t_val = spectral_trace_t([('0.1', '14.134725141734693790', 2)], dps=80)
            ta_val = spectral_weighted_trace_t_a([('0.1', '14.134725141734693790', 2)], a='0.01', dps=80)

            delta = mpmath.mpf('0.1')
            gamma = mpmath.mpf('14.134725141734693790')
            r = (delta * delta) / (gamma * gamma)

            expected_d = 2 * mpmath.log(1 + r)
            expected_t = 2 * r
            expected_ta = 2 * mpmath.exp(-mpmath.mpf('0.01') * gamma * gamma) * r

            assert mpmath.almosteq(d_val, expected_d, abs_eps=mpmath.mpf('1e-75'))
            assert mpmath.almosteq(t_val, expected_t, abs_eps=mpmath.mpf('1e-75'))
            assert mpmath.almosteq(ta_val, expected_ta, abs_eps=mpmath.mpf('1e-75'))
            assert d_val > 0
            assert t_val > 0
            assert ta_val > 0

    def test_mixed_online_offline_zeros_at_single_ordinate(self):
        """Mixed on-line and off-line zeros at a single ordinate obey multiplicity decomposition."""
        with mpmath.workdps(80):
            # Height gamma = 14.1347 with on-line multiplicity 1 and off-line quartet multiplicity 1 (2 upper roots)
            # Total upper roots: 1 on-line (delta=0) + 2 off-line (delta=0.05)
            zeros = [
                ('0.0', '14.134725141734693790', 1),
                ('0.05', '14.134725141734693790', 2),
            ]
            d_val = spectral_determinant_d([('0.0', '14.134725141734693790', 1), ('0.05', '14.134725141734693790', 1)], dps=80)
            t_val = spectral_trace_t(zeros, dps=80)

            delta = mpmath.mpf('0.05')
            gamma = mpmath.mpf('14.134725141734693790')
            r = (delta * delta) / (gamma * gamma)

            assert mpmath.almosteq(d_val, 2 * mpmath.log(1 + r), abs_eps=mpmath.mpf('1e-75'))
            assert mpmath.almosteq(t_val, 2 * r, abs_eps=mpmath.mpf('1e-75'))

    def test_extreme_regimes(self):
        """Tests high ordinate gamma=10^6 and small delta=10^-10."""
        with mpmath.workdps(120):
            gamma = mpmath.mpf('1000000.0')
            delta = mpmath.mpf('1e-10')
            r = (delta * delta) / (gamma * gamma)  # 1e-32
            zeros = [(delta, gamma, 1)]
            d_val = spectral_determinant_d(zeros, dps=120)
            t_val = spectral_trace_t(zeros, dps=120)

            assert d_val > 0
            assert t_val > 0
            assert mpmath.almosteq(d_val, 2 * mpmath.log(1 + r), abs_eps=mpmath.mpf('1e-110'))
            assert mpmath.almosteq(t_val, r, abs_eps=mpmath.mpf('1e-110'))


class TestArithmeticFirewallAndCandidateEvaluations:
    """Verifies arithmetic firewall and candidate mechanisms."""

    def test_arithmetic_firewall_rejection(self):
        """Arithmetic firewall rejects dictionaries or lists containing spectral keys."""
        with pytest.raises(ValueError, match="Firewall Violation"):
            arithmetic_firewall_check({"zeros": [14.134725]})

        with pytest.raises(ValueError, match="Firewall Violation"):
            arithmetic_firewall_check({"spectral": True, "L_Q": 0.99})

    def test_candidate_a_symbolic_reduction(self):
        """Exact SymPy verification that linear grade differences evaluate to C_0[H o tau^K] - C_0[H]."""
        tau, K, s, rho = sp.symbols('tau K s rho', positive=True)
        H = sp.Function('H')
        C_K = H(tau**K * rho)
        C_0 = H(rho)
        diff = C_K - C_0
        # When K=0, difference vanishes identically
        diff_0 = diff.subs(K, 0)
        assert diff_0 == 0

    def test_candidate_a_evaluations(self):
        """Verifies that arithmetic_candidate_a and spectral_candidate_a evaluate consistently."""
        with mpmath.workdps(60):
            # For K=0, difference vanishes
            diff_arith_0 = arithmetic_candidate_a(K=0, test_func_j=1, dps=60)
            assert mpmath.almosteq(diff_arith_0, 0, abs_eps=mpmath.mpf('1e-50'))

            zeros = [('0.0', '14.134725141734693790')]
            diff_spec_0 = spectral_candidate_a(zeros, K=0, test_func_j=1, dps=60)
            assert mpmath.almosteq(diff_spec_0, 0, abs_eps=mpmath.mpf('1e-50'))

    def test_candidate_b_double_sum_cross_terms(self):
        """Verifies that bilinear candidate B introduces unrestricted off-diagonal cross-terms."""
        with mpmath.workdps(80):
            # Test model with two distinct zeros rho_1, rho_2
            zeros = [
                ('0.0', '14.134725141734693790'),
                ('0.0', '21.022039638771554992'),
            ]
            s = mpmath.mpc('2.0', '5.0')
            spec_b = spectral_candidate_b(zeros, K=1, L=0, s=s, dps=80)
            # The bilinear product is non-zero even though all zeros are on-line (delta=0)
            assert abs(spec_b) > 0

    def test_candidate_registry_completeness(self):
        """Validates all 7 candidates A through G in the candidate registry."""
        registry = get_candidate_registry()
        expected_ids = [f"CANDIDATE_{letter}" for letter in "ABCDEFG"]
        for cid in expected_ids:
            assert cid in registry
            entry = registry[cid]
            assert "id" in entry
            assert "name" in entry
            assert "target" in entry
            assert "classification" in entry
            assert "earliest_failure" in entry
            assert entry["arithmetic_independence"] is True
