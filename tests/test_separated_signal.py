"""tests/test_separated_signal.py — High-Precision Verification Suite for Separated Sesquilinear Signal Sprint

Tests mathematical properties, gates, and falsification witnesses:
1. Exact finite algebraic curvature identity: sum_{a,b} (delta_a + delta_b)^2 = 2*N*sum(delta_a^2) under sum delta_a = 0.
2. Synthetic spectrum curvature detector: M_K''(0) == 0 iff all delta_a == 0.
3. Candidate SS-1 Cauchy-Riemann holomorphic rigidity failure witness.
4. Candidate SS-2 double-sum off-diagonal cross-term dominance witness.
5. Candidate SS-3 Cramér exponential translation divergence witness.
6. Candidate SS-4 transcendental non-resonance and coordinate pullback redundancy witness.
7. Candidate SS-5 non-holomorphic firewall and identity theorem obstruction witness.
8. Arithmetic firewall integrity for SS candidates.
9. Structured Candidate Registry validation for SS-1 through SS-5.
"""

import mpmath
import pytest
import sympy as sp
from math_core import (
    separated_spectral_signal,
    spectral_mean_square_m,
    spectral_curvature_m_double_prime,
    arithmetic_signal_ss1,
    spectral_signal_ss1,
    arithmetic_signal_ss2,
    spectral_signal_ss2,
    arithmetic_signal_ss3,
    spectral_signal_ss3,
    arithmetic_signal_ss4,
    spectral_signal_ss4,
    arithmetic_signal_ss5,
    spectral_signal_ss5,
    verify_cauchy_riemann_holomorphic_obstruction_ss1,
    verify_algebraic_curvature_identity,
    verify_cramer_divergence_witness_ss3,
    verify_transcendental_nonresonance_ss4,
    arithmetic_firewall_check,
    get_candidate_registry,
    to_mpf,
    to_mpc,
    get_tau,
)


class TestAlgebraicCurvatureIdentities:
    """Verifies the exact finite algebraic curvature identity for symmetric radial multisets."""

    def test_two_term_symmetric_pair_identity(self):
        """For delta_1 + delta_2 = 0, sum_{a,b=1}^2 (delta_a + delta_b)^2 = 4 * (delta_1^2 + delta_2^2) = 8 * delta_1^2."""
        with mpmath.workdps(80):
            d1 = mpmath.mpf('0.15')
            d2 = -d1
            deltas = [d1, d2]
            res = verify_algebraic_curvature_identity(deltas)
            assert res["is_exact"] is True
            assert res["zero_sum_reduction"] is True
            expected = 2 * 2 * (d1**2 + d2**2)
            assert mpmath.almosteq(mpmath.mpf(res["sum_pairs"]), expected, abs_eps=mpmath.mpf('1e-75'))

    def test_four_term_symmetric_quartet_identity(self):
        """For multiplicity n=2 upper fibre {d, d, -d, -d} (N=4), double sum equals 2 * 4 * (4*delta^2) = 32 * delta^2."""
        with mpmath.workdps(80):
            d = mpmath.mpf('0.075')
            deltas = [d, d, -d, -d]
            res = verify_algebraic_curvature_identity(deltas)
            assert res["is_exact"] is True
            assert res["zero_sum_reduction"] is True
            expected = 32 * (d**2)
            assert mpmath.almosteq(mpmath.mpf(res["sum_pairs"]), expected, abs_eps=mpmath.mpf('1e-75'))

    def test_general_multi_element_zero_sum_identity(self):
        """Tests 6-element asymmetric zero-sum configuration."""
        with mpmath.workdps(80):
            deltas = [
                mpmath.mpf('0.10'),
                mpmath.mpf('-0.04'),
                mpmath.mpf('-0.06'),
                mpmath.mpf('0.05'),
                mpmath.mpf('-0.08'),
                mpmath.mpf('0.03')
            ]
            res = verify_algebraic_curvature_identity(deltas)
            assert res["is_exact"] is True
            assert res["zero_sum_reduction"] is True

    def test_general_non_zero_sum_identity(self):
        """Tests general non-zero-sum multiset: sum_{a,b} (d_a+d_b)^2 = 2N*sum(d_a^2) + 2*(sum d_a)^2."""
        with mpmath.workdps(80):
            deltas = [
                mpmath.mpf('0.12'),
                mpmath.mpf('0.05'),
                mpmath.mpf('-0.03'),
                mpmath.mpf('0.07')
            ]
            res = verify_algebraic_curvature_identity(deltas)
            assert res["is_exact"] is True
            assert res["zero_sum_reduction"] is False


class TestSpectralDetectorAndCurvature:
    """Verifies synthetic spectral signal evaluation, mean-square energy, and curvature."""

    def test_online_spectrum_curvature_nullity(self):
        """An all-online spectrum yields identically zero radial curvature M_K''(0) == 0."""
        with mpmath.workdps(80):
            online_zeros = [
                ('0.0', '14.134725141734693790'),
                ('0.0', '21.022039638771554992'),
                ('0.0', '25.010857580145688763'),
            ]
            for K in [-2, 0, 1, 3]:
                curv = spectral_curvature_m_double_prime(online_zeros, K=K, dps=80)
                assert curv == mpmath.mpf('0.0')

    def test_single_offline_quartet_curvature_positivity(self):
        """A single off-line quartet produces strictly positive curvature M_K''(0) > 0."""
        with mpmath.workdps(80):
            # Upper-half-plane fibre at gamma = 14.1347 with zeros (+delta, -delta), N_gamma = 2
            quartet = [
                ('0.1', '14.134725141734693790', 1),
                ('-0.1', '14.134725141734693790', 1),
            ]
            curv = spectral_curvature_m_double_prime(quartet, K=0, dps=80)
            assert curv > 0

            # Verify against analytical formula: 2 * |a(gamma)|^2 * N * (delta_1^2 + delta_2^2) = 2 * |a|^2 * 2 * (2*delta^2) = 8*|a|^2*delta^2
            gamma = mpmath.mpf('14.134725141734693790')
            delta = mpmath.mpf('0.1')
            a_val = mpmath.exp(-mpmath.mpf('0.01') * gamma**2)
            expected = 2 * (a_val**2) * 2 * (2 * delta**2)
            assert mpmath.almosteq(curv, expected, abs_eps=mpmath.mpf('1e-75'))

            # Test normalized fibre curvature: C_gamma = curv / (2 * N_gamma * a_val^2) = delta^2 + (-delta)^2 = 2*delta^2
            from math_core import normalized_fibre_curvature
            c_gamma = normalized_fibre_curvature(curv / (a_val**2), N_gamma=2)
            expected_norm = 2 * delta**2
            assert mpmath.almosteq(c_gamma, expected_norm, abs_eps=mpmath.mpf('1e-75'))

    def test_mixed_online_and_offline_zeros_at_single_height(self):
        """Mixed on-line and off-line zeros at a single ordinate produce positive curvature solely from off-line roots."""
        with mpmath.workdps(80):
            zeros = [
                ('0.0', '14.134725141734693790', 1),  # on-line zero
                ('0.08', '14.134725141734693790', 1), # off-line +delta
                ('-0.08', '14.134725141734693790', 1),# off-line -delta
            ]
            curv = spectral_curvature_m_double_prime(zeros, K=0, dps=80)
            assert curv > 0

            gamma = mpmath.mpf('14.134725141734693790')
            a_val = mpmath.exp(-mpmath.mpf('0.01') * gamma**2)
            N = 3
            sum_sq = mpmath.mpf('0.0')**2 + mpmath.mpf('0.08')**2 + mpmath.mpf('-0.08')**2
            expected = 2 * (a_val**2) * N * sum_sq
            assert mpmath.almosteq(curv, expected, abs_eps=mpmath.mpf('1e-75'))

    def test_extreme_regimes_curvature(self):
        """Tests high ordinate gamma=10^6 and small displacement delta=10^-10."""
        with mpmath.workdps(120):
            gamma = mpmath.mpf('1000000.0')
            delta = mpmath.mpf('1e-10')
            zeros = [(delta, gamma, 1), (-delta, gamma, 1)]
            # Custom kernel avoiding underflow at gamma=10^6
            custom_kernel = lambda g: mpmath.mpf(1) / (1 + g**2)
            curv = spectral_curvature_m_double_prime(zeros, K=0, a_kernel=custom_kernel, dps=120)
            assert curv > 0

    def test_detailed_spectral_curvature_breakdown(self):
        """Detailed curvature breakdown reports quadratic, centering, and reflection symmetry status."""
        with mpmath.workdps(80):
            # Symmetric fibre: centering component is 0
            sym_zeros = [('0.1', '14.134725', 1), ('-0.1', '14.134725', 1)]
            res_sym = spectral_curvature_m_double_prime(sym_zeros, K=0, detailed=True, dps=80)
            assert res_sym["reflection_symmetric"] is True
            assert mpmath.mpf(res_sym["centering_component"]) < mpmath.mpf('1e-50')
            assert mpmath.almosteq(res_sym["quadratic_component"], res_sym["total_curvature"], abs_eps=mpmath.mpf('1e-75'))

            # Asymmetric fibre: centering component is positive and contributes to total curvature
            asym_zeros = [('0.1', '14.134725', 1), ('0.05', '14.134725', 1)]
            res_asym = spectral_curvature_m_double_prime(asym_zeros, K=0, detailed=True, dps=80)
            assert res_asym["reflection_symmetric"] is False
            assert mpmath.mpf(res_asym["centering_component"]) > 0
            expected_total = mpmath.mpf(res_asym["quadratic_component"]) + mpmath.mpf(res_asym["centering_component"])
            assert mpmath.almosteq(res_asym["total_curvature"], expected_total, abs_eps=mpmath.mpf('1e-50'))


class TestCandidateFalsificationWitnesses:
    """Verifies exact symbolic and numerical failure witnesses for Candidates SS-1 through SS-5."""

    def test_candidate_ss1_cauchy_riemann_holomorphic_rigidity(self):
        """Candidate SS-1 fails at Gate 2 because decoupled e^{x*delta + i*t*gamma} violates Cauchy-Riemann unless x=t."""
        res = verify_cauchy_riemann_holomorphic_obstruction_ss1()
        assert res["holomorphic_rigidity_proved"] is True
        assert res["cr1_forces_x_eq_t"] is True

    def test_candidate_ss2_double_sum_cross_terms(self):
        """Candidate SS-2 derives an unrestricted double sum over all zero pairs without involution-pair isolation."""
        with mpmath.workdps(80):
            online_zeros = [
                ('0.0', '14.134725141734693790', 1),
                ('0.0', '21.022039638771554992', 1),
            ]
            s1 = mpmath.mpc('0.6', '10.0')
            s2 = mpmath.mpc('0.6', '10.0')
            spec_ss2 = spectral_signal_ss2(online_zeros, K=0, s1=s1, s2=s2, dps=80)
            # The bilinear product yields an unconstrained double sum that is non-zero even on the critical line
            assert abs(spec_ss2) > 0

    def test_candidate_ss3_cramer_divergence_witness(self):
        """Candidate SS-3 fails at Gate 2 because translation-average integral diverges exponentially with T."""
        res = verify_cramer_divergence_witness_ss3(gamma='14.134725', T_vals=(1, 5, 10, 20), dps=80)
        assert res["exponential_growth_confirmed"] is True
        # For T=20, integral is > 10^240
        assert mpmath.mpf(res["integrals"]["T_20"]) > mpmath.mpf('1e240')

    def test_candidate_ss4_transcendental_nonresonance_witness(self):
        """Candidate SS-4 search verifies minimum frequency gap in finite search box (numerical evidence only)."""
        from math_core import search_bounded_transcendental_cross_grade_frequencies_ss4
        res = search_bounded_transcendental_cross_grade_frequencies_ss4(K=1, max_n=100, max_m=100)
        assert res["has_exact_resonance"] is False
        assert res["min_frequency_gap"] > 0
        assert res["epistemic_status"] == "NUMERICAL_SEARCH_EVIDENCE_ONLY_NOT_PROOF"

    def test_candidate_ss5_non_holomorphic_firewall(self):
        """Candidate SS-5 direct one-point holomorphic realization is excluded by the identity theorem on the critical line."""
        with mpmath.workdps(80):
            online_zeros = [('0.0', '14.134725141734693790', 1)]
            spec_ss5_online = spectral_signal_ss5(online_zeros, K=0, dps=80)
            assert spec_ss5_online == 0

            offline_quartet = [('0.1', '14.134725141734693790', 1)]
            spec_ss5_offline = spectral_signal_ss5(offline_quartet, K=0, dps=80)
            assert spec_ss5_offline > 0


class TestArithmeticFirewallsAndRegistry:
    """Verifies arithmetic independence firewalls and structured registry."""

    def test_arithmetic_firewall_rejection(self):
        """Arithmetic evaluators reject zero lists, projected ordinates, and spectral keys."""
        # Clean arithmetic call succeeds
        res = arithmetic_signal_ss1(K=0, x=0, t=0, N_max=10)
        assert abs(res) > 0

        # Spectral data injection triggers firewall exception
        with pytest.raises(ValueError, match="Firewall Violation"):
            arithmetic_firewall_check({"zero_list": [14.1347]})

        with pytest.raises(ValueError, match="Firewall Violation"):
            arithmetic_firewall_check({"zeros": [14.1347], "L_Q": 1.0})

    def test_candidate_registry_ss_entries(self):
        """Validates all SS candidates SS-1 through SS-5 in the registry."""
        registry = get_candidate_registry()
        expected_ss_ids = [f"CANDIDATE_SS{i}" for i in range(1, 6)]
        for cid in expected_ss_ids:
            assert cid in registry
            entry = registry[cid]
            assert "id" in entry
            assert "name" in entry
            assert "target" in entry
            assert "classification" in entry
            assert "earliest_failure" in entry
            assert entry["arithmetic_independence"] is True
            assert entry["pair_isolation"] is False

