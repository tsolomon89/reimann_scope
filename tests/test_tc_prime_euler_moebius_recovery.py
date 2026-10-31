"""Focused mathematical and 256-bit Arb tests for TASK-TC-046:
Prime-by-Prime Möbius Recovery and Arithmetic Cross-Grade Compatibility.

Covers:
1. Three-way agreement of lambda_y(n) = (mu_y * log)(n) across closed-form
   prime-factorization cases (omega_{<=y}(n) in {0, 1, >=2}), Dirichlet
   convolution, and prime-by-prime operator recursion, including explicit
   prime powers p^a (p <= y), r^b (r > y), mixed composites p^a n_{>y}, and
   multi-prime composites.
2. Exact agreement window lambda_y(n) = Lambda(n) for all 2 <= n < 2 q_{>y}
   (where q_{>y} = min{p prime : p > y}), non-negativity Delta_y(n) =
   lambda_y(n) - Lambda(n) >= 0 for all n >= 2, and first discrepancy
   Delta_y(2 q_{>y}) = log 2 > 0 at n = 2 q_{>y}.
3. Exact summatory factorial identity L_y(x) = sum_{d | P_y, d <= x} mu(d) log(floor(x/d)!)
   and L_y(x) = psi(x) for x < 2 q_{>y}.
4. Three-way agreement of W_y(X) across product recursion
   prod_{p<=y}(I - p^{-1/2} D_p) W_log(X), divisor sum
   sum_{m | P_y} mu(m) m^{-1/2} W_log(X/m), and coefficient series
   sum_{n>=2} lambda_y(n) n^{-1/2} h_0(n/X).
5. Two-sided boundary envelope |B_{log,boundary}(u)| <= min((30731/98304) u^{-5/2},
   (92193/131072) u^{5/2}) from the vanishing-moment Stieltjes decomposition.
6. Euler-sieved seed Gram norm ||Psi_y||_{L^2(d^*x)}^2 and low-frequency
   coherent arch spike |E_y(i t_y)|^2 at t_y = pi / log(y).
7. Quantitative comparison bound |W(X) - W_y(X)| <= C_{log,0} X^{5/2} / (2 M^2)
   for y >= M >= max(2, X), and coupled-cutoff bound
   |W(X) - W_{M(X)}(X)| <= (1/2) C_{log,0} = 0.2787147936 < 0.278715 at
   y = M(X) = ceil(max(2, X^{5/4})) across positive, negative, near-zero,
   and increasing rational grades K in A_R.
8. Lean 4 module verification for theorems 44 and 45 and full-tree 256-bit Arb
   round-trip verification for section_15.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

from flint import acb, arb, ctx as flint_ctx

from tc.canonical_theta_correlation_bound import (
    ARITHMETIC_CANCELLATION_CANONICAL_THETA_CORRELATION_STATUS,
    CANONICAL_THETA_CORRELATION_LEAN_DEFS,
    CANONICAL_THETA_CORRELATION_LEAN_THEOREMS,
    COMMON_REFERENT_PRIME_THETA_BRIDGE_STATUS,
    PRIME_EULER_MOEBIUS_RECOVERY_STATUS,
    SINGLE_OBSERVABLE_COMMON_REFERENT_AUDIT_STATUS,
    STARTING_HEAD_TC_046,
    STARTING_HEAD_TC_047,
    STARTING_HEAD_TC_048,
    STARTING_HEAD_TC_049,
    TASK_TC_046_ID,
    TASK_TC_047_ID,
    TASK_TC_048_ID,
    TASK_TC_049_ID,
    verify_all_serialized_arb_in_tree,
    verify_canonical_theta_correlation_lean_module,
)
from tc.common_referent_prime_theta_bridge import (
    alternating_factorial_prime_valuation_exact,
    cumulative_N_y_alternating_factorial_fraction,
    cumulative_N_y_from_local_factors_exact,
    evaluate_coupled_cutoff_jump_at_prime_threshold_arb,
    evaluate_grade_layer_observable_A_K_y_arb,
    evaluate_theta_zero_radial_defect_observable_arb,
    evaluate_w_y_from_grade_layer_jumps_arb,
    lcm_prefix_exact,
    local_prime_euler_factor_divisor_product_fraction,
    local_prime_euler_factor_m_y_exact,
    verify_symbolic_common_referent_identities,
    verify_symbolic_tc048_jump_and_single_observable_identities,
)
from tc.prime_euler_moebius_recovery import (
    certified_coupled_cutoff_M_X_arb,
    certify_dyadic_prime_block_and_subcritical_compensation_arb,
    certify_H0_local_monotonicity_and_global_decay_arb,
    certify_subproduct_counterexample_at_y210_arb,
    certify_w_log_large_scale_decay_and_resonant_band_reduction_arb,
    compute_coupled_cutoff_comparison_bound_arb,
    divisors_of_primorial,
    evaluate_H0_critical_line_arb,
    evaluate_b_log_boundary_term_arb,
    evaluate_chebyshev_psi_arb,
    evaluate_euler_dirichlet_poly_acb,
    evaluate_euler_sieved_seed_gram_norm_arb,
    evaluate_euler_spike_interval_gram_lower_bound_arb,
    evaluate_lambda_y_closed_form_arb,
    evaluate_lambda_y_convolution_arb,
    evaluate_lambda_y_recursion_arb,
    evaluate_prime_increment_J_p_arb,
    evaluate_summatory_L_y_direct_arb,
    evaluate_summatory_L_y_factorial_divisor_sum_arb,
    evaluate_w_log_divisor_aggregated_certified_arb,
    evaluate_w_prime_sum_certified_arb,
    evaluate_w_y_coefficient_certified_arb,
    evaluate_w_y_divisor_sum_certified_arb,
    evaluate_w_y_prime_recursion_certified_arb,
    next_prime_above,
    primes_up_to,
    verify_symbolic_finite_prime_identities,
    verify_symbolic_tc049_prime_increment_and_w_log_asymptotic_identities,
    von_mangoldt_arb,
)


def test_01_symbolic_finite_prime_euler_identities():
    """Verify exact symbolic identities for finite-prime Euler inversion and prime-power cases."""
    sym = verify_symbolic_finite_prime_identities()
    assert sym["commutation_verified"] is True
    assert sym["two_prime_expansion_verified"] is True
    assert sym["log_additivity_verified"] is True
    assert sym["small_prime_power_equals_log_p"] is True
    assert sym["large_prime_power_equals_b_log_r"] is True
    assert sym["mixed_composite_one_small_prime_equals_log_p"] is True
    assert sym["two_small_primes_vanishes"] is True
    assert sym["coupled_exponent_verified"] is True
    assert sym["coupled_exponent_difference_5_2_minus_2_times_5_4"] == 0


def test_02_lambda_y_three_way_agreement_and_prime_power_cases():
    """Verify closed-form, Dirichlet convolution, and prime-by-prime recursion for lambda_y(n)."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for y in (2, 3, 5, 7, 11):
            for n in range(2, 90):
                lam_cf = evaluate_lambda_y_closed_form_arb(n, y)
                lam_conv = evaluate_lambda_y_convolution_arb(n, y)
                lam_rec = evaluate_lambda_y_recursion_arb(n, y)
                assert bool((lam_cf - lam_conv).contains(0))
                assert bool(abs(lam_cf - lam_conv) < arb("1e-70"))
                assert bool((lam_cf - lam_rec).contains(0))
                assert bool(abs(lam_cf - lam_rec) < arb("1e-70"))

        # Explicit prime-power and composite cases at y = 5 (primes <= 5 are {2, 3, 5}, q_{>5} = 7):
        # 1. Prime power p^a with p <= y: lambda_5(2^3 = 8) = log 2 = Lambda(8), lambda_5(3^2 = 9) = log 3 = Lambda(9)
        for n_pp, p_base in ((4, 2), (8, 2), (16, 2), (9, 3), (27, 3), (25, 5)):
            val = evaluate_lambda_y_closed_form_arb(n_pp, 5)
            vm = von_mangoldt_arb(n_pp)
            assert bool((val - arb(p_base).log()).contains(0))
            assert bool((val - vm).contains(0))

        # 2. Prime power r^b with r > y: lambda_5(7) = log 7 = Lambda(7), but lambda_5(7^2 = 49) = 2 log 7 != Lambda(49) = log 7
        val_7 = evaluate_lambda_y_closed_form_arb(7, 5)
        assert bool((val_7 - arb(7).log()).contains(0))
        val_49 = evaluate_lambda_y_closed_form_arb(49, 5)
        assert bool((val_49 - arb(2) * arb(7).log()).contains(0))
        assert bool(((val_49 - von_mangoldt_arb(49)) - arb(7).log()).contains(0))

        # 3. Mixed composite p^a * n_{>y} with exactly one distinct prime p <= y:
        #    lambda_5(2 * 7 = 14) = log 2, lambda_5(2^2 * 7 = 28) = log 2, lambda_5(3 * 7 = 21) = log 3
        for n_mix, p_small in ((14, 2), (28, 2), (21, 3), (35, 5)):
            val_m = evaluate_lambda_y_closed_form_arb(n_mix, 5)
            assert bool((val_m - arb(p_small).log()).contains(0))
            assert bool(von_mangoldt_arb(n_mix) == 0)

        # 4. Multi-prime composite with >= 2 distinct primes <= y vanishes identically:
        for n_zero in (6, 10, 12, 15, 18, 20, 24, 30, 42, 60):
            val_z = evaluate_lambda_y_closed_form_arb(n_zero, 5)
            assert bool(val_z == 0)
    finally:
        flint_ctx.prec = saved_prec


def test_03_agreement_threshold_2_q_gt_y_and_summatory_factorial_identity():
    """Verify lambda_y(n) = Lambda(n) for 2 <= n < 2 q_{>y}, first discrepancy at 2 q_{>y}, and factorial identity for L_y(x)."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for y in (2, 3, 5, 7, 11, 13, 17, 19, 23):
            q_gt = next_prime_above(y)
            first_diff = None
            for n in range(2, 2 * q_gt + 15):
                diff = evaluate_lambda_y_closed_form_arb(n, y) - von_mangoldt_arb(n)
                # Non-negativity Delta_y(n) >= 0 for all n >= 2
                assert bool(diff.contains(0)) or bool(diff > arb(0))
                if first_diff is None and not (
                    bool(diff.contains(0)) and bool(abs(diff) < arb("1e-70"))
                ):
                    first_diff = n
            assert first_diff == 2 * q_gt
            diff_at_2q = evaluate_lambda_y_closed_form_arb(
                2 * q_gt, y
            ) - von_mangoldt_arb(2 * q_gt)
            assert bool((diff_at_2q - arb(2).log()).contains(0))
            assert bool(abs(diff_at_2q - arb(2).log()) < arb("1e-70"))

            # Verify L_y(x) = sum_{d | P_y, d <= x} mu(d) log(floor(x/d)!) and L_y(x) = psi(x) for x < 2 q_{>y}
            for x_test in (2 * q_gt - 1, 2 * q_gt, 2 * q_gt + 7):
                l_dir = evaluate_summatory_L_y_direct_arb(x_test, y)
                l_fac = evaluate_summatory_L_y_factorial_divisor_sum_arb(x_test, y)
                psi_x = evaluate_chebyshev_psi_arb(x_test)
                assert bool((l_dir - l_fac).contains(0))
                assert bool(abs(l_dir - l_fac) < arb("1e-70"))
                if x_test < 2 * q_gt:
                    assert bool((l_dir - psi_x).contains(0))
                    assert bool(abs(l_dir - psi_x) < arb("1e-70"))
                elif x_test == 2 * q_gt:
                    assert bool(((l_dir - psi_x) - arb(2).log()).contains(0))
    finally:
        flint_ctx.prec = saved_prec


def test_04_three_way_W_y_operator_divisor_coefficient_equivalence():
    """Verify product recursion, divisor sum, and coefficient series for W_y(X) agree in 256-bit Arb."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tau_a = arb(2) * arb.pi()
        for y in (2, 3, 5, 7):
            for X_a in (arb(1), tau_a ** (arb(1) / arb(2)), tau_a):
                rec_res = evaluate_w_y_prime_recursion_certified_arb(
                    X_a, y=y, k_max=1500, prec_bits=256
                )
                div_res = evaluate_w_y_divisor_sum_certified_arb(
                    X_a, y=y, k_max=1500, prec_bits=256
                )
                coeff_res = evaluate_w_y_coefficient_certified_arb(
                    X_a, y=y, n_max=1500, prec_bits=256
                )
                p_ball = rec_res["enclosure_arb"]
                d_ball = div_res["enclosure_arb"]
                c_ball = coeff_res["enclosure_arb"]
                assert bool((p_ball - d_ball).contains(0))
                assert bool(abs(arb(p_ball.mid()) - arb(d_ball.mid())) < arb("1e-70"))
                assert bool(p_ball.overlaps(c_ball))
                assert bool(d_ball.overlaps(c_ball))
    finally:
        flint_ctx.prec = saved_prec


def test_05_stieltjes_boundary_envelope_and_critical_line_spike():
    """Verify two-sided boundary envelope for B_{log,boundary}(u), Gram norm ||Psi_y||_{L^2}^2, and low-frequency spike."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        # 1. Two-sided boundary envelope |B_{log,boundary}(u)| <= min((30731/98304) u^{-5/2}, (92193/131072) u^{5/2})
        c_large = arb(30731) / arb(98304)
        c_small = arb(92193) / arb(131072)
        for u_val in (arb("0.1"), arb("0.25"), arb("0.5"), arb(1), arb(2), arb(4), arb(10)):
            b_u = evaluate_b_log_boundary_term_arb(u_val)
            b_hi = c_large * (u_val ** (-arb("2.5")))
            b_lo = c_small * (u_val ** arb("2.5"))
            env = b_hi if bool(b_hi <= b_lo) else b_lo
            assert bool(abs(b_u) <= env)

        # 2. Euler-sieved seed Gram norm ||Psi_y||_{L^2(d^*x)}^2 > 0
        for y in (2, 3, 5, 7, 11, 13):
            g_res = evaluate_euler_sieved_seed_gram_norm_arb(y, prec_bits=256)
            assert bool(g_res["gram_norm_sq_arb"] > arb("0.5"))
            assert bool(g_res["gram_norm_arb"] > arb("0.7"))

        # 3. Critical-line H_0(0) > 0, low-frequency coherent spike at t_y = pi / log(y),
        #    and controlled-width frequency interval Gram-norm lower bound on I_y = [7*pi / (8*log y), pi / log y]
        h0_0 = evaluate_H0_critical_line_arb(arb(0))
        assert bool(h0_0 > arb("2.82e-5")) and bool(h0_0 < arb("2.83e-5"))

        prev_spike = arb(0)
        for y in (11, 31, 97, 199, 499, 997):
            t_y = arb.pi() / arb(y).log()
            e_ty = evaluate_euler_dirichlet_poly_acb(acb(arb(0), t_y), y)
            e_sq = abs(e_ty) ** 2
            h0_ty = evaluate_H0_critical_line_arb(t_y)
            assert bool(h0_ty > h0_0)
            assert bool(e_sq > prev_spike)
            prev_spike = e_sq
        assert bool(prev_spike > arb(6000))

        prev_gram_lb = arb(0)
        for y in (97, 199, 499, 997, 1999, 4999, 9973):
            iv = evaluate_euler_spike_interval_gram_lower_bound_arb(y, prec_bits=256)
            assert iv["I_y_subset_of_analytic_unit_interval_0_1"] is True
            assert iv["E_y_sq_interval_monotonicity_by_phase_in_0_pi"] is True
            assert iv["H0_interval_monotonicity_certified_on_I_y"] is True
            assert iv["H0_interval_subdivision_exceeds_H0_0"] is True
            assert iv["endpoint_ordering_E_y_sq_minus_le_plus"] is True
            assert iv["endpoint_ordering_H0_0_le_minus_le_plus"] is True
            assert bool(iv["interval_width_arb"] > arb(0))
            assert bool(iv["e_sq_at_minus_arb"] <= iv["e_sq_at_plus_arb"])
            assert bool(iv["gram_sq_lb_H0_0_arb"] <= iv["gram_sq_lb_H0_subdiv_arb"])
            assert bool(
                iv["gram_sq_lb_H0_subdiv_arb"].lower()
                <= iv["gram_sq_lb_H0_minus_arb"].lower()
            )
            assert bool(iv["gram_sq_lb_H0_0_arb"] <= iv["gram_sq_lb_H0_minus_arb"])
            assert bool(iv["gram_sq_lb_H0_0_arb"] > prev_gram_lb)
            prev_gram_lb = iv["gram_sq_lb_H0_0_arb"]
        assert bool(prev_gram_lb > arb(153))

        # 4. Also verify finite-table rows with y < 24 (y in {2, 5, 11}) where I_y is not a subset of [0, 1]
        for y_small in (2, 5, 11):
            iv_s = evaluate_euler_spike_interval_gram_lower_bound_arb(y_small, prec_bits=256)
            assert iv_s["I_y_subset_of_analytic_unit_interval_0_1"] is False
            assert iv_s["E_y_sq_interval_monotonicity_by_phase_in_0_pi"] is True
            assert iv_s["H0_interval_monotonicity_certified_on_I_y"] is True
            assert iv_s["H0_interval_subdivision_exceeds_H0_0"] is True
            assert bool(iv_s["H0_dlog_dv_min_on_I_y_arb"] > arb(0))
            assert bool(iv_s["H0_subdiv_min_arb"] > iv_s["H0_at_0_arb"])

        # 5. Regression: Counterexample at y = 210 refuting the false subproduct inequality
        #    |E_y(i t_{y,-})|^2 >= prod_{y^{16/21} <= p <= y} (1 + p^{-1/2} + p^{-1})
        ce_210 = certify_subproduct_counterexample_at_y210_arb(210, prec_bits=256)
        assert ce_210["enclosures_disjoint_and_false_subproduct_exceeds_actual"] is True
        assert ce_210["omitted_lower_prime_product_strictly_less_than_one"] is True
        assert bool(
            ce_210["actual_E_y_abs_sq_at_t_y_minus_arb"]
            < ce_210["claimed_false_subproduct_arb"]
        )
        assert math.isclose(
            float(ce_210["actual_E_y_abs_sq_at_t_y_minus_arb"].mid()),
            3.360505748107592,
            rel_tol=1e-13,
        )
        assert math.isclose(
            float(ce_210["claimed_false_subproduct_arb"].mid()),
            18.253611894431243,
            rel_tol=1e-13,
        )
        assert math.isclose(
            float(ce_210["omitted_lower_prime_product_arb"].mid()),
            0.05585403137068536,
            rel_tol=1e-13,
        )

        # 6. Regression: Local monotonicity of H_0(it) on [0, 1] (and [0, t_{2,+}]),
        #    left-endpoint coefficient 4*cos(tau/16) = 2*sqrt(2+sqrt(2)), and global non-monotonicity
        h0_cert = certify_H0_local_monotonicity_and_global_decay_arb(prec_bits=256)
        assert h0_cert["left_endpoint_coeff_algebraic_identity_contains_zero"] is True
        assert h0_cert["left_endpoint_coeff_strictly_between_3_6955_and_4"] is True
        assert math.isclose(
            float(h0_cert["left_endpoint_coeff_4_cos_tau_over_16_arb"].mid()),
            3.695518130045147,
            rel_tol=1e-14,
        )
        assert h0_cert["dlog_dv_unit_interval_lb_strictly_positive"] is True
        assert h0_cert["dlog_dv_t_le_2_lb_strictly_positive"] is True
        assert h0_cert["y23_exceeds_unit_interval_and_y24_inside_unit_interval"] is True
        assert h0_cert["all_weierstrass_product_checks_intersect"] is True
        assert h0_cert["subdivision_64_on_0_to_t2plus_all_dlog_dv_positive"] is True
        assert bool(h0_cert["subdivision_64_min_dlog_dv_on_0_to_t2plus_arb"] > arb(0))
        assert h0_cert["global_monotonicity_falsified_H0_t5_lt_H0_t2plus"] is True
        assert h0_cert["high_frequency_decay_verified_H0_t20_lt_H0_0"] is True
    finally:
        flint_ctx.prec = saved_prec


def test_06_coupled_cutoff_comparison_bound_across_admissible_grades():
    """Verify |W(X) - W_{M(X)}(X)| <= C_{log,0} X^{5/2} / (2 M(X)^2) <= (1/2) C_{log,0} < 0.278715 across rational grades and X = 16 +/- 10^{-30} ceiling regression."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        # Near-integer ceiling regression without float rounding loss:
        x_below_16 = arb(16) - arb("1e-30")
        x_exact_16 = arb(16)
        x_above_16 = arb(16) + arb("1e-30")
        assert certified_coupled_cutoff_M_X_arb(x_below_16, prec_bits=256) == 32
        assert certified_coupled_cutoff_M_X_arb(x_exact_16, prec_bits=256) == 32
        assert certified_coupled_cutoff_M_X_arb(x_above_16, prec_bits=256) == 33

        # Reproduce why binary64 float rounding fails at X = 16 + 10^{-30}:
        u_above_16 = (x_above_16**5).root(4)
        assert bool(u_above_16 > arb(32))
        naive_float_cutoff = int(math.ceil(float(u_above_16.upper())))
        assert naive_float_cutoff == 32
        assert not bool(arb(naive_float_cutoff) >= u_above_16)

        cmp_above_16 = compute_coupled_cutoff_comparison_bound_arb(
            x_above_16, prec_bits=256
        )
        assert cmp_above_16["M_X"] == 33
        assert cmp_above_16["M_X_ge_X_pow_5_4"] is True
        assert cmp_above_16["M_X_sq_ge_X_pow_5_2"] is True
        assert cmp_above_16["satisfies_uniform_bound"] is True

        tau_a = arb(2) * arb.pi()
        for k_frac in (
            Fraction(0, 1),
            Fraction(1, 100),
            Fraction(-1, 100),
            Fraction(1, 4),
            Fraction(-1, 4),
            Fraction(1, 2),
            Fraction(-1, 2),
            Fraction(1, 1),
            Fraction(-1, 1),
        ):
            abs_k = abs(k_frac)
            k_arb = arb(abs_k.numerator) / arb(abs_k.denominator)
            X_a = tau_a**k_arb
            cmp_info = compute_coupled_cutoff_comparison_bound_arb(X_a, prec_bits=256)
            M_X = cmp_info["M_X"]
            bound_M = cmp_info["bound_at_M_X_arb"]
            half_c = cmp_info["half_c_log_0_arb"]
            assert cmp_info["satisfies_uniform_bound"] is True
            assert bool(bound_M <= half_c)
            assert bool(half_c < arb("0.278715"))

            w_act = evaluate_w_prime_sum_certified_arb(X_a, n_max=2000, prec_bits=256)[
                "enclosure_arb"
            ]
            w_y = evaluate_w_y_coefficient_certified_arb(
                X_a, y=M_X, n_max=2000, prec_bits=256
            )["enclosure_arb"]
            w_log = evaluate_w_log_divisor_aggregated_certified_arb(
                X_a, k_max=2000, prec_bits=256
            )["enclosure_arb"]
            diff = abs(w_act - w_y)
            assert bool(diff.lower() <= bound_M.upper())
            # Also verify W_y(X) = W_log(X) + sum_{m | P_y, m>=2} mu(m) m^{-1/2} W_log(X/m)
            w_y_div = evaluate_w_y_divisor_sum_certified_arb(
                X_a, y=M_X, k_max=2000, prec_bits=256
            )["enclosure_arb"]
            assert bool(w_y.overlaps(w_y_div))
            assert bool((w_y_div - w_log).overlaps(w_y - w_log))
    finally:
        flint_ctx.prec = saved_prec


def test_07_lean_module_and_artifact_section_15():
    """Verify Lean 4 module theorems 44 & 45 and section_15 of data/tc_canonical_theta_correlation_bound.json."""
    lean_audit = verify_canonical_theta_correlation_lean_module()
    assert lean_audit["exists"] is True
    assert lean_audit["contains_sorry"] is False
    assert lean_audit["contains_admit"] is False
    assert lean_audit["matches_exact"] is True
    assert len(CANONICAL_THETA_CORRELATION_LEAN_DEFS) == 32
    assert len(CANONICAL_THETA_CORRELATION_LEAN_THEOREMS) == 50
    assert "finitePrimeEulerRecursionStep" in CANONICAL_THETA_CORRELATION_LEAN_DEFS
    assert "finitePrimeCoeffCases" in CANONICAL_THETA_CORRELATION_LEAN_DEFS
    assert "finitePrimeMultiplicativeFactorCases" in CANONICAL_THETA_CORRELATION_LEAN_DEFS
    assert "gradeLayerRealizedObservable" in CANONICAL_THETA_CORRELATION_LEAN_DEFS
    assert (
        "finite_prime_euler_recursion_and_coefficient_cases"
        in CANONICAL_THETA_CORRELATION_LEAN_THEOREMS
    )
    assert (
        "coupled_prime_cutoff_comparison_and_boundedness_equivalence"
        in CANONICAL_THETA_CORRELATION_LEAN_THEOREMS
    )
    assert (
        "prime_euler_multiplicative_integrality_and_grade_layer_membership"
        in CANONICAL_THETA_CORRELATION_LEAN_THEOREMS
    )
    assert (
        "common_referent_integer_layer_bridge_and_station_ratio_identity"
        in CANONICAL_THETA_CORRELATION_LEAN_THEOREMS
    )

    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "tc_canonical_theta_correlation_bound.json"
    )
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert payload["prime_euler_moebius_recovery_task_id"] == TASK_TC_046_ID
    assert (
        payload["status_dimensions"]["prime_euler_moebius_recovery_status"]
        == PRIME_EULER_MOEBIUS_RECOVERY_STATUS
    )
    sec15 = payload[
        "section_15_prime_by_prime_moebius_recovery_and_euler_compatibility"
    ]
    assert sec15["task_id"] == TASK_TC_046_ID
    assert sec15["inspected_baseline"] == STARTING_HEAD_TC_046
    s2 = sec15["section_2_finite_prime_euler_inversion_and_coefficients"]
    win = s2["exact_agreement_window_with_von_mangoldt"]
    assert win["all_three_lambda_methods_agree_up_to_120"] is True
    assert win["all_delta_nonnegative_verified"] is True
    assert all(
        row["exact_agreement_for_all_2_le_n_lt_2_q_gt_y"]
        and row["discrepancy_at_2_q_gt_y_equals_log_2"]
        for row in win["threshold_verification_table"]
    )
    assert all(
        row["factorial_identity_encloses_zero"]
        and row["prime_step_recursion_encloses_zero"]
        and row["equals_psi_below_2_q_gt_y"]
        for row in s2["summatory_verification_checks"]
    )
    assert all(
        row["prod_minus_divisor_encloses_zero"]
        and row["coeff_minus_divisor_encloses_zero"]
        and row["coeff_minus_prod_encloses_zero"]
        for row in s2["three_way_W_y_representation_checks"]
    )
    s3 = sec15["section_3_quantitative_compatibility_and_obstruction_analysis"]
    mech_a = s3["mechanism_A_critical_line_mellin_fourier_and_gram_bound"]
    assert (
        "does NOT establish divergence of W_{M(X)}(X), failure of the concurrent-grade hypothesis"
        in mech_a["low_frequency_coherent_arch_obstruction"]
    )
    assert (
        "4*cos(tau/16)"
        in mech_a["low_frequency_coherent_arch_obstruction"]
    )
    ce_art = mech_a["subproduct_counterexample_y210"]
    assert ce_art["enclosures_disjoint_and_false_subproduct_exceeds_actual"] is True
    assert ce_art["omitted_lower_prime_product_strictly_less_than_one"] is True
    h0_art = mech_a["h0_local_monotonicity_and_decay_certificate"]
    assert h0_art["left_endpoint_coeff_algebraic_identity_contains_zero"] is True
    assert h0_art["dlog_dv_unit_interval_lb_strictly_positive"] is True
    assert h0_art["all_weierstrass_product_checks_intersect"] is True
    assert h0_art["subdivision_64_on_0_to_t2plus_all_dlog_dv_positive"] is True
    assert h0_art["global_monotonicity_falsified_H0_t5_lt_H0_t2plus"] is True
    assert h0_art["high_frequency_decay_verified_H0_t20_lt_H0_0"] is True
    spike_rows = mech_a["low_frequency_spike_table"]
    assert len(spike_rows) == 11
    assert all(
        row["E_y_sq_interval_monotonicity_by_phase_in_0_pi"] is True
        and row["H0_interval_monotonicity_certified_on_I_y"] is True
        and row["H0_interval_subdivision_exceeds_H0_0"] is True
        and row["endpoint_ordering_E_y_sq_minus_le_plus"] is True
        and row["endpoint_ordering_H0_0_le_minus_le_plus"] is True
        for row in spike_rows
    )
    assert (
        spike_rows[-1]["gram_norm_sq_lower_bound_expr_via_H0_0_certified"][
            "mid_float"
        ]
        > 153.0
    )

    s4 = sec15["section_4_coupled_cutoff_passage_and_grade_certification"]
    ceil_regs = {
        row["X_label"]: row for row in s4["certified_cutoff_ceiling_regression"]
    }
    assert ceil_regs["16 - 10^{-30}"]["certified_M_X"] == 32
    assert ceil_regs["16"]["certified_M_X"] == 32
    assert ceil_regs["16 + 10^{-30}"]["certified_M_X"] == 33
    assert ceil_regs["16 + 10^{-30}"]["naive_float_ceil_value"] == 32
    assert all(
        row["matches_expected_M_X"]
        and row["M_X_ge_X_pow_5_4_verified"]
        and row["M_X_sq_ge_X_pow_5_2_verified"]
        and row["satisfies_uniform_bound"]
        for row in s4["certified_cutoff_ceiling_regression"]
    )
    assert len(s4["certified_coupled_grade_table"]) == 13
    assert all(
        row["abs_W_minus_W_M_X_below_analytic_bound"]
        and row["abs_W_minus_W_M_X_below_half_C_log_0"]
        and row["abs_T_smooth_below_analytic_bound"]
        and row["smooth_plus_rough_partition_encloses_zero"]
        for row in s4["certified_coupled_grade_table"]
    )
    rem_obl = sec15["section_5_outcome_and_remaining_obligation"][
        "remaining_open_obligation"
    ]
    assert rem_obl["subgate_id"] == "SUBGATE-TC-043A"
    assert rem_obl["status"] == "OPEN"
    assert "|R_{mu, M(X)}(X)| <= M_trunc" in rem_obl["exact_surviving_lemma"]
    assert "|R_{mu, floor(X)}(X)| <=" not in rem_obl["exact_surviving_lemma"]
    assert "O(sqrt(X))" in rem_obl["exact_surviving_lemma"]

    rt15 = sec15["full_section_15_tree_roundtrip_verification"]
    assert rt15["all_enclose_original_256bit_arb_ball"] is True
    assert rt15["live_original_count_matches_enumerated_total"] is True
    assert (
        rt15["compared_against_live_original_arb_count"]
        == rt15["total_certified_arb_balls_checked"]
        == len(rt15["checked_paths"])
    )
    enum15 = verify_all_serialized_arb_in_tree(sec15, path_prefix="section_15")
    assert (
        rt15["compared_against_live_original_arb_count"]
        == enum15["total_certified_arb_balls_checked"]
    )


def test_08_task_tc047_common_referent_prime_theta_integer_layer_bridge():
    """Verify TASK-TC-047 common-referent observable N_y(x), A_{K,y}(x) = N_y(x)*tau^K in L_K^x,
    exact factorial-ratio integrality (denominator == 1), LCM agreement below 2 q_{>y},
    Mellin-Stieltjes station-ratio reconstruction of W_{M(X)}(X), and section_16 round-trip.
    """
    sym = verify_symbolic_common_referent_identities()
    assert sym["multiplicative_step_0_to_1_equals_p"] is True
    assert sym["multiplicative_step_1_to_2_equals_1"] is True
    assert sym["grade_layer_step_ratio_cancels_tau_K"] is True
    assert sym["cross_grade_station_ratio_identity_verified"] is True
    assert sym["ambient_coboundary_transfer_identity_verified"] is True

    # 1. Exact factorial-ratio integrality (denominator == 1), LCM agreement, and prime valuations:
    for y_cut in (2, 3, 5, 7, 11, 13):
        q_next = next_prime_above(y_cut)
        first_disc = 2 * q_next
        for n in range(1, first_disc + 6):
            m_int = local_prime_euler_factor_m_y_exact(n, y_cut)
            m_frac = local_prime_euler_factor_divisor_product_fraction(n, y_cut)
            assert m_int >= 1
            assert m_frac.denominator == 1
            assert m_frac.numerator == m_int

            N_prod = cumulative_N_y_from_local_factors_exact(n, y_cut)
            N_fact = cumulative_N_y_alternating_factorial_fraction(n, y_cut)
            assert N_fact.denominator == 1
            assert N_fact.numerator == N_prod
            if n < first_disc:
                assert N_prod == lcm_prefix_exact(n)
            elif n == first_disc:
                assert N_prod == 2 * lcm_prefix_exact(first_disc)

        for p_c in primes_up_to(first_disc):
            assert alternating_factorial_prime_valuation_exact(first_disc, y_cut, p_c) >= 0

    # 2. Grade-layer observable A_{K,y}(x) = N_y(x)*tau^K in L_K^x and Stieltjes station-ratio reconstruction:
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tau_a = arb(2) * arb.pi()
        for k_arb in (
            arb(0),
            arb(1) / arb(4),
            -arb(1) / arb(4),
            arb(2).sqrt() / arb(2),
            arb(1),
            -arb(1),
        ):
            abs_k = abs(k_arb)
            X_a = tau_a**abs_k
            M_k = certified_coupled_cutoff_M_X_arb(X_a, prec_bits=256)
            obs_k = evaluate_grade_layer_observable_A_K_y_arb(
                25, M_k, k_arb, prec_bits=256
            )
            obs_0 = evaluate_grade_layer_observable_A_K_y_arb(
                25, M_k, arb(0), prec_bits=256
            )
            assert obs_k["size_recovery_encloses_zero"] is True
            assert obs_k["log_N_y_equals_L_y_encloses_zero"] is True
            assert bool(
                (obs_k["A_K_y_arb"] - (tau_a**k_arb) * obs_0["A_K_y_arb"]).contains(0)
            )
            jump_res = evaluate_w_y_from_grade_layer_jumps_arb(
                X_a, M_k, abs_k, arb(0), n_cut=1200, prec_bits=256
            )
            assert jump_res["jump_vs_direct_encloses_zero"] is True
            assert jump_res["tau_K_cancellation_in_step_ratio_verified"] is True
    finally:
        flint_ctx.prec = saved_prec

    # 3. Artifact section_16 verification:
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "tc_canonical_theta_correlation_bound.json"
    )
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert payload["common_referent_prime_theta_bridge_task_id"] == TASK_TC_047_ID
    assert (
        payload["status_dimensions"]["common_referent_prime_theta_bridge_status"]
        == COMMON_REFERENT_PRIME_THETA_BRIDGE_STATUS
    )
    sec16 = payload["section_16_common_referent_prime_theta_integer_layer_bridge"]
    assert sec16["task_id"] == TASK_TC_047_ID
    assert sec16["inspected_baseline"] == STARTING_HEAD_TC_047
    s12 = sec16["section_1_2_factorial_ratio_integrality_and_lcm_audit"]
    assert s12["all_factorial_ratio_denominators_equal_one"] is True
    assert s12["all_local_factor_products_match_factorial_ratio"] is True
    assert s12["all_prime_valuations_nonnegative"] is True
    assert s12["all_lcm_agreement_windows_verified"] is True
    assert s12["all_first_discrepancy_ratios_equal_two"] is True
    assert s12["all_arb_logs_match_summatory_L_y"] is True
    s3 = sec16["section_3_grade_layer_membership_and_station_ratio_bridge"]
    assert s3["all_grade_size_recoveries_enclose_zero"] is True
    assert s3["all_grade_coboundary_transfers_enclose_zero"] is True
    assert s3["all_grade_jump_reconstructions_enclose_zero"] is True
    assert s3["all_nonzero_rational_grades_avoid_self_dual_peak"] is True
    assert len(s3["certified_grade_layer_bridge_table"]) == 15
    s4 = sec16["section_4_cr1_cr2_cr3_bridge_and_open_obligation"]
    assert s4["remaining_open_obligation"]["subgate_id"] == "SUBGATE-TC-043A"
    assert s4["remaining_open_obligation"]["status"] == "OPEN"
    rt16 = sec16["full_section_16_tree_roundtrip_verification"]
    assert rt16["all_enclose_original_256bit_arb_ball"] is True
    assert rt16["live_original_count_matches_enumerated_total"] is True
    enum16 = verify_all_serialized_arb_in_tree(sec16, path_prefix="section_16")
    assert (
        rt16["compared_against_live_original_arb_count"]
        == enum16["total_certified_arb_balls_checked"]
    )


def test_09_task_tc048_coupled_cutoff_jump_and_single_observable_audit():
    """Verify TASK-TC-048 coupled-cutoff piecewise continuity and right-hand jump formula
    F(X_0^+) - F(X_0) = -p^{-1/2} W_{p^-}(X_0 / p) at X_0 = (p - 1)^{4/5},
    Candidate 1 vs Candidate 2 single-observable collision contract audit,
    Covariance-Invariance-Discreteness Trilemma, and section_17 round-trip.
    """
    sym48 = verify_symbolic_tc048_jump_and_single_observable_identities()
    assert sym48["euler_prime_step_jump_identity_verified"] is True
    assert sym48["candidate_1_coboundary_ratio_verified"] is True
    assert sym48["candidate_1B_grade_invariant_modulation_still_leaves_tau_K_verified"] is True
    assert sym48["candidate_2A_pullback_grade_invariance_verified"] is True
    assert sym48["candidate_2A_radial_factor_square_identity_verified"] is True

    assert "coupledCutoffPrimeStepJump" in CANONICAL_THETA_CORRELATION_LEAN_DEFS
    assert "thetaZeroRadialDefectObservable" in CANONICAL_THETA_CORRELATION_LEAN_DEFS
    assert (
        "coupled_cutoff_prime_step_jump_and_dense_comparison_extension"
        in CANONICAL_THETA_CORRELATION_LEAN_THEOREMS
    )
    assert (
        "single_observable_common_referent_candidate_audit_and_trilemma"
        in CANONICAL_THETA_CORRELATION_LEAN_THEOREMS
    )

    # 1. Live 256-bit Arb verification of right-hand jumps at prime thresholds p in {3, 5, 7, 11, 13}
    #    (where 2/u_p in (2.6941, 8.6213) lies in the positive lobe of h_0, so W_{p^-}(u_p) > 0
    #    and F(X_0^+) - F(X_0) < 0) and continuity (jump == 0) at composite step m + 1 = 4:
    for p_val in (3, 5, 7, 11, 13):
        j_res = evaluate_coupled_cutoff_jump_at_prime_threshold_arb(
            p_val, k_max=2000, prec_bits=256
        )
        assert j_res["is_prime_threshold"] is True
        assert j_res["jump_identity_encloses_zero"] is True
        assert j_res["jump_certified_nonzero"] is True
        assert j_res["jump_certified_strictly_negative"] is True
        assert j_res["W_p_minus_at_u_p_certified_strictly_positive"] is True

    comp_res = evaluate_coupled_cutoff_jump_at_prime_threshold_arb(
        4, k_max=2000, prec_bits=256
    )
    assert comp_res["is_prime_threshold"] is False
    assert bool(comp_res["direct_jump_F_X0_plus_minus_F_X0_arb"].contains(0))

    # 2. Live 256-bit Arb verification of Candidate 2A across grades K = 0, J = 1, K = -1, K = sqrt(2)/2:
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        gamma_test = arb("14.1347251417346937904572519835625")
        # On critical line delta = 0: D_K^{(2A)} == 0 across all grades
        c2a_0_k0 = evaluate_theta_zero_radial_defect_observable_arb(
            arb(0), gamma_test, arb(0), prec_bits=256
        )
        c2a_0_j1 = evaluate_theta_zero_radial_defect_observable_arb(
            arb(0), gamma_test, arb(1), prec_bits=256
        )
        assert c2a_0_k0["abs_H0_at_z_sq_strictly_positive"] is True
        assert bool(c2a_0_k0["D_K_2A_arb"].contains(0))
        assert bool((c2a_0_k0["D_K_2A_arb"] - c2a_0_j1["D_K_2A_arb"]).contains(0))

        # Off critical line delta = 1/10 != 0: D_K^{(2A)} > 0 and D_K^{(2A)} == D_J^{(2A)}
        delta_off = arb(1) / arb(10)
        c2a_off_k0 = evaluate_theta_zero_radial_defect_observable_arb(
            delta_off, gamma_test, arb(0), prec_bits=256
        )
        c2a_off_j1 = evaluate_theta_zero_radial_defect_observable_arb(
            delta_off, gamma_test, arb(1), prec_bits=256
        )
        c2a_off_kn1 = evaluate_theta_zero_radial_defect_observable_arb(
            delta_off, gamma_test, -arb(1), prec_bits=256
        )
        c2a_off_ksqrt2 = evaluate_theta_zero_radial_defect_observable_arb(
            delta_off, gamma_test, arb(2).sqrt() / arb(2), prec_bits=256
        )
        assert c2a_off_k0["abs_H0_at_z_sq_strictly_positive"] is True
        assert bool(c2a_off_k0["D_K_2A_arb"].lower() > arb(0))
        assert bool((c2a_off_k0["D_K_2A_arb"] - c2a_off_j1["D_K_2A_arb"]).contains(0))
        assert bool((c2a_off_k0["D_K_2A_arb"] - c2a_off_kn1["D_K_2A_arb"]).contains(0))
        assert bool(
            (c2a_off_k0["D_K_2A_arb"] - c2a_off_ksqrt2["D_K_2A_arb"]).contains(0)
        )
    finally:
        flint_ctx.prec = saved_prec

    # 3. Artifact section_17 verification:
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "tc_canonical_theta_correlation_bound.json"
    )
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert payload["single_observable_common_referent_audit_task_id"] == TASK_TC_048_ID
    assert (
        payload["status_dimensions"]["single_observable_common_referent_audit_status"]
        == SINGLE_OBSERVABLE_COMMON_REFERENT_AUDIT_STATUS
    )
    sec17 = payload[
        "section_17_single_prime_theta_observable_and_coupled_cutoff_jump_audit"
    ]
    assert sec17["task_id"] == TASK_TC_048_ID
    assert sec17["inspected_baseline"] == STARTING_HEAD_TC_048

    s2_jump = sec17["section_2_coupled_cutoff_piecewise_continuity_and_jump_audit"]
    assert s2_jump["all_prime_jump_identities_enclose_zero"] is True
    assert s2_jump["all_prime_jumps_certified_nonzero"] is True
    assert s2_jump["all_small_prime_jumps_certified_strictly_negative"] is True
    assert len(s2_jump["certified_prime_threshold_jump_table"]) == 8
    tail_1901 = s2_jump["asymptotic_tail_prime_1901_jump_check"]
    assert tail_1901["in_strict_negative_h0_tail_alpha_ge_9"] is True
    assert tail_1901["W_p_minus_at_u_p_certified_strictly_negative"] is True
    assert tail_1901["jump_certified_nonzero"] is True
    assert tail_1901["jump_certified_strictly_positive"] is True
    assert (
        s2_jump["composite_threshold_continuity_check"][
            "jump_encloses_zero_at_composite_step"
        ]
        is True
    )
    assert (
        "NEVER invoke continuity of F(X)"
        in s2_jump["corrected_dense_grade_to_all_X_extension"]
    )

    s3_cand = sec17["section_3_single_observable_common_referent_candidate_audit"]
    sub_table = s3_cand["substantive_candidate_classification_table"]
    assert len(sub_table) == 3
    assert "N_y(x) * tau^K" in sub_table[0]["candidate"]
    assert len(sub_table[0]["established"]) == 2
    assert "Integer-layer membership (CR2" in sub_table[0]["established"][0]
    assert "Nonvanishing (one-way CR3 implication" in sub_table[0]["established"][1]
    assert "Raw cross-grade equality (CR1" in sub_table[0]["missing"][0]
    assert "D_K^{(2A)}" in sub_table[1]["candidate"]
    assert len(sub_table[1]["established"]) == 2
    assert "Raw cross-grade equality (CR1" in sub_table[1]["established"][0]
    assert "Off-critical nonvanishing (CR3" in sub_table[1]["established"][1]
    assert "Integer-layer membership (CR2" in sub_table[1]["missing"][0]
    assert "D_{K,y}^{(2B)}" in sub_table[2]["candidate"]
    assert len(sub_table[2]["established"]) == 1
    assert "Raw cross-grade equality (CR1" in sub_table[2]["established"][0]
    assert len(sub_table[2]["missing"]) == 2
    assert "General off-critical nonvanishing (CR3" in sub_table[2]["missing"][0]
    assert "Integer-layer membership (CR2" in sub_table[2]["missing"][1]

    c1_sub = s3_cand["candidate_1_grade_K_prime_euler_integer_layer_observable"]
    assert "ESTABLISHED" in c1_sub["subcase_1A_unmodulated_carrier_c_K_eq_1"]["CR3_status"]
    c1_bench = c1_sub["subcase_1A_unmodulated_carrier_c_K_eq_1"][
        "certified_benchmark_at_rho_1_K0_vs_J1"
    ]
    assert c1_bench["raw_CR1_difference_strictly_positive"] is True
    assert c1_bench["coboundary_encloses_zero"] is True
    assert c1_bench["raw_scale_CR1_difference_D_1_minus_D_0_strictly_positive"] is True
    c1b_sub = c1_sub["subcase_1B_zero_defect_modulated_carrier"]
    assert (
        c1b_sub["certified_grade_invariant_modulation_at_delta_1_10"][
            "grade_invariant_modulation_raw_CR1_difference_strictly_positive"
        ]
        is True
    )

    c2_audit = s3_cand[
        "candidate_2_canonical_theta_and_stieltjes_zero_defect_observables"
    ]
    assert "all_cand2a_strictly_below_one" not in c2_audit
    assert c2_audit["all_cand2a_cr1_enclose_zero"] is True
    assert c2_audit["all_cand2a_off_line_strictly_positive"] is True
    assert c2_audit["all_cand2a_on_line_enclose_zero"] is True
    z10_cert = c2_audit["subcase_2A_normalized_pullback_theta_zero_radial_defect"][
        "first_10_zeta_zeros_certification"
    ]
    assert z10_cert["all_first_10_zeros_abs_H0_sq_strictly_positive"] is True
    assert z10_cert["all_first_10_zeros_on_line_D_2A_enclose_zero"] is True
    assert z10_cert["all_first_10_zeros_off_line_D_2A_strictly_positive"] is True
    assert z10_cert["all_first_10_zeros_off_line_CR1_enclose_zero"] is True
    assert len(z10_cert["certified_first_10_zeros_table"]) == 10
    assert c2_audit["all_cand2b_cr1_enclose_zero"] is True
    assert (
        c2_audit["subcase_2B_prime_euler_stieltjes_shift_difference"][
            "cand2b_n_cut_800_delta_1_20_encloses_zero"
        ]
        is True
    )
    row_1_20 = c2_audit["certified_candidate_2_evaluation_table"][1]
    assert row_1_20["delta_label"] == "1/20"
    assert row_1_20["D_0_2B_n_cut_800_encloses_zero"] is True
    assert row_1_20["D_2B_sampled_point_strictly_nonzero_at_n_cut_2500"] is True
    assert (
        "What additional identity satisfied specifically by actual zeta zeros"
        in s3_cand["remaining_open_obligation"]["decisive_open_question"]
    )

    rem17 = s3_cand["remaining_open_obligation"]
    assert rem17["subgate_id"] == "SUBGATE-TC-043A"
    assert rem17["status"] == "OPEN"
    assert rem17["common_referent_bridge_complete"] is False

    rt17 = sec17["full_section_17_tree_roundtrip_verification"]
    assert rt17["all_enclose_original_256bit_arb_ball"] is True
    assert rt17["live_original_count_matches_enumerated_total"] is True
    enum17 = verify_all_serialized_arb_in_tree(sec17, path_prefix="section_17")
    assert (
        rt17["compared_against_live_original_arb_count"]
        == enum17["total_certified_arb_balls_checked"]
    )


def test_10_task_tc049_arithmetic_cancellation_and_resonant_band_reduction():
    """Verify TASK-TC-049 prime-increment telescoping J_p(X) = p^{-1/2} W_{p^-}(X/p),
    supercritical dyadic prime block obstruction (5X < p <= 10X), subcritical vs supercritical
    resummation cancellation, 4th-order Euler-Maclaurin O(X^{-5/2}) decay of W_log(X),
    two-sided localized resonant divisor band reduction (X^{5/6} < m <= M(X)), and section_18 round-trip.
    """
    sym49 = verify_symbolic_tc049_prime_increment_and_w_log_asymptotic_identities()
    assert sym49["kappa_factorization_verified"] is True
    assert sym49["kappa_at_10_exact_match"] is True
    assert sym49["dkappa_at_9_pos"] is True
    assert sym49["psi0_series_verified"] is True
    assert sym49["poly_coeffs_verified"] is True
    assert sym49["antideriv_L_verified"] is True
    assert sym49["subcritical_supercritical_coeff_cancellation_verified_n_2_to_400"] is True
    assert sym49["head_sum_bound_identity_verified"] is True
    assert sym49["all_verified"] is True

    assert "primeIncrementStep" in CANONICAL_THETA_CORRELATION_LEAN_DEFS
    assert "localizedResonantBandDecomp" in CANONICAL_THETA_CORRELATION_LEAN_DEFS
    assert (
        "prime_increment_telescoping_and_resonant_band_reduction"
        in CANONICAL_THETA_CORRELATION_LEAN_THEOREMS
    )

    # 1. Live 256-bit Arb verification of single-prime increments J_p(X) at X = 2 (p in {11, 13, 17, 19}):
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for p_val in (11, 13, 17, 19):
            jp = evaluate_prime_increment_J_p_arb(
                arb(2), p=p_val, n_max=800, prec_bits=256
            )
            assert jp["is_supercritical_2p_ge_9X"] is True
            assert jp["step_residual_encloses_zero"] is True
            assert jp["satisfies_n2_lower_bound"] is True
            assert bool(jp["J_p_direct_arb"] < arb(0))
            assert bool(jp["neg_J_p_arb"] >= jp["n2_lower_bound_arb"])
    finally:
        flint_ctx.prec = saved_prec

    # 2. Live 256-bit Arb verification of dyadic block and subcritical compensation:
    dyadic_cert = certify_dyadic_prime_block_and_subcritical_compensation_arb(
        prec_bits=256
    )
    assert dyadic_cert["c0_A5_certified"]["mid_float"] > 0.0219
    assert all(
        row["all_primes_satisfy_two_sided_inequality"]
        and row["block_satisfies_lower_and_upper_bounds"]
        for row in dyadic_cert["dyadic_block_table"]
    )
    assert all(
        row["telescoping_at_y_sub_encloses_zero"]
        and row["telescoping_at_M_X_encloses_zero"]
        and row["compensation_identity_encloses_zero"]
        and row["net_sum_bounded_by_half_C_log_0"]
        and row["linear_cutoff_D_5X_strictly_negative"]
        and row["linear_cutoff_T_5X_to_10X_strictly_positive"]
        and row["linear_cutoff_D_10X_strictly_negative"]
        and row["linear_cutoff_neg_D_5X_exceeds_T_5X_to_10X"]
        and row["linear_cutoff_compensation_encloses_zero"]
        for row in dyadic_cert["subcritical_compensation_table"]
    )

    # 3. Artifact section_18 verification:
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "tc_canonical_theta_correlation_bound.json"
    )
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert (
        payload["arithmetic_cancellation_canonical_theta_correlation_task_id"]
        == TASK_TC_049_ID
    )
    assert (
        payload["status_dimensions"][
            "arithmetic_cancellation_canonical_theta_correlation_status"
        ]
        == ARITHMETIC_CANCELLATION_CANONICAL_THETA_CORRELATION_STATUS
    )
    sec18 = payload[
        "section_18_arithmetic_cancellation_in_canonical_theta_correlation"
    ]
    assert sec18["task_id"] == TASK_TC_049_ID
    assert sec18["inspected_baseline"] == STARTING_HEAD_TC_049

    s2_18 = sec18[
        "section_2_supercritical_dyadic_block_obstruction_and_subcritical_compensation"
    ]["certified_audit_data"]
    assert len(s2_18["dyadic_block_table"]) == 6
    assert len(s2_18["subcritical_compensation_table"]) == 5

    s3_18 = sec18[
        "section_3_w_log_large_scale_decay_and_resonant_band_reduction"
    ]["certified_audit_data"]
    assert (
        s3_18["global_euler_maclaurin_constant_C_log_EM_certified"]["mid_float"]
        < 13.47
    )
    assert (
        s3_18["small_divisor_head_global_bound_5_6_C_log_EM_certified"]["mid_float"]
        < 11.224
    )
    assert (
        s3_18["resonant_band_comparison_bound_certified"]["mid_float"] < 11.503
    )
    assert all(
        row["satisfies_euler_maclaurin_bound"]
        for row in s3_18["w_log_asymptotic_table"]
    )
    assert all(
        row["head_satisfies_global_bound"]
        and row["tail_satisfies_half_C_log_0_bound"]
        and row["band_comparison_satisfies_global_bound"]
        and row["three_zone_decomposition_encloses_zero"]
        for row in s3_18["resonant_band_table"]
    )

    s4_18 = sec18["section_4_outcome_and_remaining_obligation"]
    assert s4_18["symbolic_identities_verification"]["all_verified"] is True
    assert s4_18["closes_subgate_tc043a"] is False
    rem18 = s4_18["remaining_open_obligation"]
    assert rem18["subgate_id"] == "SUBGATE-TC-043A"
    assert rem18["status"] == "OPEN"
    assert "X^{5/6} < m <= M(X)" in rem18["exact_surviving_lemma"]

    rt18 = sec18["full_section_18_tree_roundtrip_verification"]
    assert rt18["all_enclose_original_256bit_arb_ball"] is True
    assert rt18["live_original_count_matches_enumerated_total"] is True
    enum18 = verify_all_serialized_arb_in_tree(sec18, path_prefix="section_18")
    assert (
        rt18["compared_against_live_original_arb_count"]
        == enum18["total_certified_arb_balls_checked"]
    )


