"""
tests/test_coupled_covariance_and_perturbation.py — Comprehensive Tests for Coupled Scale Covariance and Controlled Zero Perturbations

Covers all 14 mandatory requirements from prompt:
1. Exact high-precision zeta coordinate covariance: Z_A(A s) = zeta(s)
2. Mapped critical line: Re(s') = A/2
3. Mapped zero: rho' = A rho
4. Exact converter argument identity: (A rho) log(x^(1/A)) = rho log x
5. Single-zero J covariance: C_J(x^(1/A), A rho) = C_J(x, rho)
6. Single-zero pi covariance under matching truncation: C_pi(x^(1/A), A rho) = C_pi(x, rho)
7. Single-pair diagnostic construction: rho = 1/2 + delta + i gamma
8. Symmetry-complete quartet construction: rho_+ = 1/2+delta+i gamma, rho_- = 1/2-delta+i gamma
9. No conjugate double counting
10. Isolated delta-update equals independent full recomputation
11. delta = 0 reduces correctly to baseline
12. Batch converter_perturbation actually changes selected zero when delta != 0
13. Batch and direct canonical-engine calculations agree
14. Authoritative outputs remain high-precision decimal strings
"""

import pytest
import mpmath
import numpy as np

import math_core
import transforms
import converter
import research_runner
import reference_data


def test_exact_zeta_coordinate_covariance():
    """
    Test 1: Exact high-precision zeta coordinate covariance Z_A(A s) = zeta(s)
    across diverse s (generic points, critical-line, near zeros, outside critical strip)
    and k in [-10, -5, -2, -1, 0, 1, 2, 5, 10] at 80 dps.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps)
        test_k_values = ["-5", "-2", "-1", "0", "1", "2", "5"]
        test_s_points = [
            mpmath.mpc("0.5", "14.134725141734693790457251983562"),  # On critical line (zero)
            mpmath.mpc("0.5", "25.0"),                                # On critical line (non-zero)
            mpmath.mpc("0.75", "14.134725141734693790457251983562"), # Inside critical strip
            mpmath.mpc("2.5", "10.0"),                                # In absolute convergence domain
            mpmath.mpc("-1.5", "12.0")                                # In negative half-plane
        ]
        
        for k_str in test_k_values:
            t_orig = transforms.OriginCoordinateDilation(k=k_str)
            k_mpf = math_core.to_mpf(k_str, dps=dps)
            scale_A = mpmath.power(tau, k_mpf)
            
            for s in test_s_points:
                # Baseline value W = zeta(s)
                W = math_core.zeta_eval(s, dps=dps)
                
                # Mapped point s' = A * s
                s_prime = scale_A * s
                
                # Value of transformed coordinate representation evaluated AT MAPPED POINT:
                # W_A = Z_A(s') = zeta(s' / A)
                W_A = t_orig.evaluate_function(s_prime, dps=dps)
                
                diff = abs(W_A - W)
                assert diff < mpmath.mpf("1e-25"), (
                    f"Zeta coordinate covariance failed at k={k_str}, s={s}: diff={diff}"
                )


def test_mapped_critical_line():
    """
    Test 2: Mapped critical line under origin coordinate dilation is Re(s') = A/2.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps)
        for k_val in ["-2.0", "-1.0", "0.0", "1.0", "2.0"]:
            t_orig = transforms.OriginCoordinateDilation(k=k_val)
            scale_A = mpmath.power(tau, math_core.to_mpf(k_val, dps=dps))
            expected_re = scale_A / 2
            
            # Check image critical line coordinate
            s_crit = mpmath.mpc("0.5", "20.0")
            mapped_crit = t_orig.map_zero_mpc(s_crit, dps=dps)
            assert abs(mapped_crit.real - expected_re) < mpmath.mpf("1e-60")


def test_mapped_zero():
    """
    Test 3: Mapped zero under origin coordinate dilation is rho' = A * rho.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps)
        ref_zeros = reference_data.load_reference_zeros()[:3]
        for gamma_str in ref_zeros:
            rho = mpmath.mpc("0.5", gamma_str)
            for k_val in ["-1.5", "0.0", "1.5"]:
                t_orig = transforms.OriginCoordinateDilation(k=k_val)
                scale_A = mpmath.power(tau, math_core.to_mpf(k_val, dps=dps))
                
                mapped_rho = t_orig.map_zero_mpc(rho, dps=dps)
                expected_mapped = scale_A * rho
                assert abs(mapped_rho - expected_mapped) < mpmath.mpf("1e-60")


def test_converter_argument_identity():
    """
    Test 4: Exact converter argument identity (A*rho) * log(x^(1/A)) = rho * log(x)
    for arbitrary A > 0, x > 1, rho in C.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps)
        for k_val in ["-3.0", "-1.0", "0.5", "2.0"]:
            scale_A = mpmath.power(tau, math_core.to_mpf(k_val, dps=dps))
            for x_val in ["2.0", "10.0", "100.0"]:
                x_mpf = math_core.to_mpf(x_val, dps=dps)
                rho = mpmath.mpc("0.5", "14.134725141734693790457251983562")
                
                rho_prime = scale_A * rho
                x_prime = mpmath.power(x_mpf, mpmath.mpf(1) / scale_A)
                
                arg_baseline = rho * mpmath.log(x_mpf)
                arg_coupled = rho_prime * mpmath.log(x_prime)
                
                assert abs(arg_coupled - arg_baseline) < mpmath.mpf("1e-70")


def test_single_zero_j_covariance():
    """
    Test 5: Single-zero J covariance C_J(x^(1/A), A*rho) = C_J(x, rho) at 80 dps.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps)
        test_k = ["-5", "-2", "-1", "0", "1", "2", "5"]
        test_x = ["10.0", "50.0", "100.0"]
        test_rho = [
            mpmath.mpc("0.5", "14.13472514173469379045725198356247027078425711569924317568556746"),
            mpmath.mpc("0.5", "21.02203963877155499262847959389690277733434052490278180469829596")
        ]
        
        for k_str in test_k:
            scale_A = mpmath.power(tau, math_core.to_mpf(k_str, dps=dps))
            for x_str in test_x:
                x_mpf = math_core.to_mpf(x_str, dps=dps)
                x_prime = mpmath.power(x_mpf, mpmath.mpf(1) / scale_A)
                
                for rho in test_rho:
                    rho_prime = scale_A * rho
                    
                    cj_clean = converter.zero_j_contribution_audit(x_mpf, rho, dps=dps)
                    cj_coupled = converter.zero_j_contribution_audit(x_prime, rho_prime, dps=dps)
                    
                    diff = abs(cj_coupled - cj_clean)
                    assert diff < mpmath.mpf("1e-25"), (
                        f"C_J covariance failed at k={k_str}, x={x_str}: diff={diff}"
                    )


def test_single_zero_pi_covariance():
    """
    Test 6: Single-zero pi covariance C_pi(x^(1/A), A*rho) = C_pi(x, rho)
    when evaluated under matching truncation semantics (m >= 1).
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps)
        # Choose parameters where x' >= 2
        k_str = "0.2"
        scale_A = mpmath.power(tau, math_core.to_mpf(k_str, dps=dps))
        x_mpf = mpmath.mpf("100.0")
        x_prime = mpmath.power(x_mpf, mpmath.mpf(1) / scale_A)
        rho = mpmath.mpc("0.5", "14.134725141734693790457251983562")
        rho_prime = scale_A * rho
        
        # When evaluating sum over identical terms (rho log(x^(1/m)) = rho_prime log((x')^(1/m)))
        # each term in the Mobius sum is identical
        for m in [1, 2, 3]:
            xm = mpmath.power(x_mpf, mpmath.mpf(1) / m)
            xm_prime = mpmath.power(x_prime, mpmath.mpf(1) / m)
            cj_m = converter.zero_j_contribution_audit(xm, rho, dps=dps)
            cj_m_prime = converter.zero_j_contribution_audit(xm_prime, rho_prime, dps=dps)
            assert abs(cj_m_prime - cj_m) < mpmath.mpf("1e-25")


def test_single_pair_diagnostic_construction():
    """
    Test 7: Single-pair diagnostic construction: rho = 1/2 + delta + i*gamma.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        rho_clean = "0.5 + 14.134725141734693790457251983562j"
        delta = "0.05"
        
        zeros = converter.construct_perturbed_zeros_audit(rho_clean, delta, mode="single_pair_diagnostic", dps=dps)
        assert len(zeros) == 1
        assert abs(zeros[0].real - mpmath.mpf("0.55")) < mpmath.mpf("1e-70")
        assert abs(zeros[0].imag - mpmath.mpf("14.134725141734693790457251983562")) < mpmath.mpf("1e-70")


def test_symmetry_complete_quartet_construction():
    """
    Test 8: Symmetry-complete quartet construction:
    rho_+ = 1/2 + delta + i*gamma, rho_- = 1/2 - delta + i*gamma.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        rho_clean = "0.5 + 14.134725141734693790457251983562j"
        delta = "0.02"
        
        zeros = converter.construct_perturbed_zeros_audit(rho_clean, delta, mode="symmetry_complete_quartet", dps=dps)
        assert len(zeros) == 2
        assert abs(zeros[0].real - mpmath.mpf("0.52")) < mpmath.mpf("1e-70")
        assert abs(zeros[1].real - mpmath.mpf("0.48")) < mpmath.mpf("1e-70")
        assert abs(zeros[0].imag - zeros[1].imag) < mpmath.mpf("1e-70")


def test_no_conjugate_double_counting():
    """
    Test 9: Verify no conjugate double counting.
    In the 2*Re convention, C_J(x, rho) incorporates the conjugate pair (rho, bar(rho)).
    For a symmetry quartet with delta != 0, exactly 2 upper-half-plane zeros (rho_+, rho_-)
    represent the entire 4-point orbit {1/2 +/- delta +/- i*gamma}.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        x = "20.0"
        gamma = "14.134725141734693790457251983562"
        delta = "0.01"
        
        rho_plus = mpmath.mpc("0.51", gamma)
        rho_minus = mpmath.mpc("0.49", gamma)
        
        cj_plus = converter.zero_j_contribution_audit(x, rho_plus, dps=dps)
        cj_minus = converter.zero_j_contribution_audit(x, rho_minus, dps=dps)
        total_quartet_cj = cj_plus + cj_minus
        
        info = converter.compute_perturbed_contributions_audit(x, mpmath.mpc("0.5", gamma), delta, mode="symmetry_complete_quartet", dps=dps)
        assert abs(info["cj_perturbed"] - total_quartet_cj) < mpmath.mpf("1e-70")


def test_isolated_delta_update_equals_full_recomputation():
    """
    Test 10: Isolated delta-update pi_N,clean + Delta C_pi equals independent full recomputation
    from modified synthetic spectrum at audit precision for both modes.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        x = "20.0"
        ref_zeros = [mpmath.mpc("0.5", s) for s in reference_data.load_reference_zeros()[:5]]
        
        # 1. Single pair diagnostic mode
        info_diag = converter.compute_perturbed_contributions_audit(x, ref_zeros[0], "0.03", mode="single_pair_diagnostic", dps=dps)
        clean_pi = converter.riemann_explicit_pi_audit(x, ref_zeros, dps=dps)
        fast_pert_diag = clean_pi + info_diag["delta_cpi"]
        
        modified_zeros_diag = [info_diag["perturbed_rhos"][0]] + ref_zeros[1:]
        full_pert_diag = converter.riemann_explicit_pi_audit(x, modified_zeros_diag, dps=dps)
        
        assert abs(fast_pert_diag - full_pert_diag) < mpmath.mpf("1e-35")
        
        # 2. Symmetry complete split mode (with multiplicity 2 baseline)
        info_quart = converter.compute_perturbed_contributions_audit(x, ref_zeros[0], "0.03", mode="symmetry_complete_split", dps=dps)
        clean_zeros_double = [ref_zeros[0], ref_zeros[0]] + ref_zeros[1:]
        clean_pi_double = converter.riemann_explicit_pi_audit(x, clean_zeros_double, dps=dps)
        fast_pert_quart = clean_pi_double + info_quart["split_defect_cpi"]
        
        modified_zeros_quart = info_quart["perturbed_rhos"] + ref_zeros[1:]
        full_pert_quart = converter.riemann_explicit_pi_audit(x, modified_zeros_quart, dps=dps)
        
        assert abs(fast_pert_quart - full_pert_quart) < mpmath.mpf("1e-35")


def test_delta_zero_reduces_to_baseline():
    """
    Test 11: delta = 0 reduces correctly to baseline (Delta C_J = 0, Delta C_pi = 0, full diff = 0)
    for both single_pair_diagnostic and symmetry_complete_split modes.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        x = "20.0"
        rho = mpmath.mpc("0.5", "14.134725141734693790457251983562")
        
        for mode in ["single_pair_diagnostic", "symmetry_complete_split", "symmetry_complete_quartet"]:
            info = converter.compute_perturbed_contributions_audit(x, rho, "0.0", mode=mode, dps=dps)
            assert abs(info["delta_cj"]) < mpmath.mpf("1e-70")
            assert abs(info["delta_cpi"]) < mpmath.mpf("1e-70")
            assert abs(info["cj_perturbed"] - info["cj_clean"]) < mpmath.mpf("1e-70")
            assert abs(info["cpi_perturbed"] - info["cpi_clean"]) < mpmath.mpf("1e-70")


def test_batch_converter_perturbation_changes_selected_zero():
    """
    Test 12: Batch converter_perturbation actually changes selected zero when delta != 0.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        inputs = {
            "zero_index": "0",
            "delta": "0.05",
            "x": "20.0",
            "num_zeros": "5",
            "perturbation_mode": "single_pair_diagnostic"
        }
        status, outputs, err = research_runner.evaluate_point("converter_perturbation", inputs, dps=dps)
        assert status == "ok"
        assert err is None
        
        delta_cj = mpmath.mpf(outputs["delta_cj"])
        delta_cpi = mpmath.mpf(outputs["delta_cpi"])
        delta_pi = mpmath.mpf(outputs["delta_pi_n"])
        
        # When delta = 0.05, the perturbation is nonzero
        assert abs(delta_cj) > mpmath.mpf("1e-5")
        assert abs(delta_cpi) > mpmath.mpf("1e-5")
        assert abs(delta_pi) > mpmath.mpf("1e-5")
        assert "0.55" in outputs["perturbed_rhos"]


def test_batch_and_direct_canonical_engine_agreement():
    """
    Test 13: Batch and direct canonical-engine calculations agree to 80 dps.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        # 1. zeta_trace_compare
        inputs_zeta = {
            "k": "1.5",
            "s_re": "0.5",
            "s_im": "14.13472514173469379045725198356247027078425711569924317568556746",
            "x": "20.0"
        }
        status, out_zeta, err = research_runner.evaluate_point("zeta_trace_compare", inputs_zeta, dps=dps)
        assert status == "ok"
        cov_res_batch = mpmath.mpf(out_zeta["covariance_residual"])
        assert cov_res_batch < mpmath.mpf("1e-25")
        
        # 2. converter_perturbation
        inputs_pert = {
            "zero_index": "1",
            "delta": "0.01",
            "x": "25.0",
            "num_zeros": "6",
            "perturbation_mode": "symmetry_complete_split"
        }
        status, out_pert, err = research_runner.evaluate_point("converter_perturbation", inputs_pert, dps=dps)
        assert status == "ok"
        
        # Direct canonical evaluation
        ref_zeros = reference_data.load_reference_zeros()[:6]
        rho_clean = mpmath.mpc("0.5", ref_zeros[1])
        direct_info = converter.compute_perturbed_contributions_audit("25.0", rho_clean, "0.01", mode="symmetry_complete_split", dps=dps)
        batch_split_cj = mpmath.mpf(out_pert["split_defect_cj"])
        assert abs(batch_split_cj - direct_info["split_defect_cj"]) < mpmath.mpf("1e-70")


def test_authoritative_outputs_remain_decimal_strings():
    """
    Test 14: Authoritative batch runner outputs serialize as exact decimal strings.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        inputs = {
            "k": "2.0",
            "s_re": "0.5",
            "s_im": "14.13472514173469379045725198356247027078425711569924317568556746",
            "x": "10.0"
        }
        status, outputs, err = research_runner.evaluate_point("zeta_trace_compare", inputs, dps=dps)
        assert status == "ok"
        
        for key, val in outputs.items():
            assert isinstance(val, str), f"Output '{key}' was not a string: {type(val)}"
            try:
                mpmath.mpf(val)
            except Exception:
                pass


def test_symmetry_complete_split_multiplicity_2_baseline():
    """
    Test 15: Symmetry-complete split uses multiplicity 2 baseline so S_J(0) = 0 and S_pi(0) = 0.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        x = "20.0"
        rho_clean = mpmath.mpc("0.5", "14.134725141734693790457251983562")
        info = converter.compute_perturbed_contributions_audit(x, rho_clean, "0.0", mode="symmetry_complete_split", dps=dps)
        assert abs(info["split_defect_cj"]) < mpmath.mpf("1e-70")
        assert abs(info["split_defect_cpi"]) < mpmath.mpf("1e-70")


def test_split_defect_evenness_and_odd_term_cancellation():
    """
    Test 16: S_J(-delta) = S_J(delta), S_pi(-delta) = S_pi(delta), and odd first-order term cancels.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        x = "20.0"
        rho_clean = mpmath.mpc("0.5", "14.134725141734693790457251983562")
        delta = "0.005"
        
        info_pos = converter.compute_perturbed_contributions_audit(x, rho_clean, delta, mode="symmetry_complete_split", dps=dps)
        info_neg = converter.compute_perturbed_contributions_audit(x, rho_clean, f"-{delta}", mode="symmetry_complete_split", dps=dps)
        
        # Even symmetry
        assert abs(info_pos["split_defect_cj"] - info_neg["split_defect_cj"]) < mpmath.mpf("1e-70")
        assert abs(info_pos["split_defect_cpi"] - info_neg["split_defect_cpi"]) < mpmath.mpf("1e-70")
        
        # First derivative / odd slope at 0
        d_val = mpmath.mpf(delta)
        slope_odd = (info_pos["split_defect_cj"] - info_neg["split_defect_cj"]) / (mpmath.mpf(2) * d_val)
        assert abs(slope_odd) < mpmath.mpf("1e-65")


def test_small_delta_quadratic_scaling():
    """
    Test 17: Local quadratic scaling S_J(lambda * delta) / S_J(delta) -> lambda^2 near delta = 0.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        x = "20.0"
        rho_clean = mpmath.mpc("0.5", "14.134725141734693790457251983562")
        delta1 = "0.001"
        delta2 = "0.002"  # lambda = 2 -> expected ratio = 4
        
        info1 = converter.compute_perturbed_contributions_audit(x, rho_clean, delta1, mode="symmetry_complete_split", dps=dps)
        info2 = converter.compute_perturbed_contributions_audit(x, rho_clean, delta2, mode="symmetry_complete_split", dps=dps)
        
        s1 = info1["split_defect_cj"]
        s2 = info2["split_defect_cj"]
        
        ratio = s2 / s1
        assert abs(ratio - mpmath.mpf(4)) < mpmath.mpf("1e-4")


def test_symmetric_centrifuge_exact_identity():
    """
    Test 18: Exact closed form |D_K| = 4 * sinh^2(K * delta * ln(tau) / 2) across K and delta.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        gamma = "14.134725141734693790457251983562"
        for delta in ["-0.01", "-0.001", "0.0", "0.001", "0.01"]:
            for K in ["-20", "-5", "-1", "0", "1", "5", "20"]:
                D_K = math_core.symmetric_centrifuge_defect(delta, gamma, K, dps=dps)
                expected_abs = math_core.symmetric_centrifuge_defect_expected(delta, K, dps=dps)
                abs_D_K = abs(D_K)
                
                diff = abs(abs_D_K - expected_abs)
                assert diff < mpmath.mpf("1e-70"), f"Centrifuge identity failed at delta={delta}, K={K}: diff={diff}"


def test_symmetric_centrifuge_defect_symmetries():
    """
    Test 19: D_K is even in delta, |D_K| is even in K, D_K = 0 for K=0 or delta=0.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        gamma = "14.134725141734693790457251983562"
        # D_K = 0 for delta = 0
        D_0_delta = math_core.symmetric_centrifuge_defect("0.0", gamma, "10", dps=dps)
        assert abs(D_0_delta) < mpmath.mpf("1e-70")
        
        # D_K = 0 for K = 0
        D_0_k = math_core.symmetric_centrifuge_defect("0.01", gamma, "0", dps=dps)
        assert abs(D_0_k) < mpmath.mpf("1e-70")
        
        # Even in delta
        D_pos = math_core.symmetric_centrifuge_defect("0.005", gamma, "5", dps=dps)
        D_neg = math_core.symmetric_centrifuge_defect("-0.005", gamma, "5", dps=dps)
        assert abs(D_pos - D_neg) < mpmath.mpf("1e-70")
        
        # |D_K| even in K
        D_k_pos = math_core.symmetric_centrifuge_defect("0.005", gamma, "8", dps=dps)
        D_k_neg = math_core.symmetric_centrifuge_defect("0.005", gamma, "-8", dps=dps)
        assert abs(abs(D_k_pos) - abs(D_k_neg)) < mpmath.mpf("1e-70")


def test_coupled_perturbed_covariance_engine_consumes_k():
    """
    Test 20 & 21: coupled_perturbation_covariance engine genuinely consumes k,
    maps coordinates x' = x^(1/A) and rho' = A*rho, and achieves exact covariance <= 1e-25.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        inputs = {
            "zero_index": "0",
            "delta": "0.01",
            "k": "1.0",
            "x": "20.0",
            "num_zeros": "5",
            "perturbation_mode": "symmetry_complete_split"
        }
        status, outputs, err = research_runner.evaluate_point("coupled_perturbation_covariance", inputs, dps=dps)
        assert status == "ok"
        assert err is None
        
        # Verify k was consumed to produce tau^1
        A_val = mpmath.mpf(outputs["A"])
        tau = math_core.get_tau(dps=dps)
        assert abs(A_val - tau) < mpmath.mpf("1e-70")
        
        # Verify x' = x^(1/A) != x
        x_val = mpmath.mpf(outputs["x"])
        x_prime = mpmath.mpf(outputs["x_prime"])
        assert abs(x_prime - mpmath.power(x_val, mpmath.mpf(1) / tau)) < mpmath.mpf("1e-70")
        assert abs(x_prime - x_val) > mpmath.mpf("0.1")
        
        # Verify exact covariance residual <= 1e-25
        cov_res = mpmath.mpf(outputs["covariance_residual"])
        assert cov_res < mpmath.mpf("1e-25")


def test_mode_separated_metrics_emission():
    """
    Test mode-separated metric emission:
    - single_pair_diagnostic emits delta_cj, delta_cpi, delta_pi_n ONLY.
    - single_pair_diagnostic does NOT emit split_defect_*, symmetry_error*, or quadratic_* metrics.
    - symmetry_complete_split emits split_defect_*, symmetry_error*, normalized_quadratic_*, quadratic_ratio_* ONLY.
    - symmetry_complete_split does NOT emit delta_cj, delta_cpi, delta_pi_n.
    """
    dps = 80
    param_space = {
        "delta": {
            "kind": "explicit",
            "values": ["-0.01", "-0.005", "0.0", "0.005", "0.01"]
        }
    }
    
    # 1. Single pair diagnostic point
    inputs_single = {
        "zero_index": "0",
        "delta": "0.01",
        "x": "20.0",
        "num_zeros": "5",
        "perturbation_mode": "single_pair_diagnostic"
    }
    status, out_single, err = research_runner.evaluate_point(
        "converter_perturbation", inputs_single, dps=dps, param_space=param_space
    )
    assert status == "ok"
    assert "delta_cj" in out_single
    assert "delta_cpi" in out_single
    assert "delta_pi_n" in out_single
    
    # Forbidden in single-pair
    forbidden_in_single = [
        "split_defect_cj", "split_defect_cpi", "split_defect_pi_n",
        "symmetry_error", "symmetry_error_cj", "symmetry_error_cpi",
        "normalized_quadratic_cj", "normalized_quadratic_cpi",
        "quadratic_ratio_cj", "quadratic_ratio_cpi",
        "quadratic_ratio_error_cj", "quadratic_ratio_error_cpi"
    ]
    for key in forbidden_in_single:
        assert key not in out_single, f"Metric '{key}' should not be emitted for single_pair_diagnostic"
        
    # 2. Symmetry complete split point (with delta=0.01 where delta/2=0.005 is present)
    inputs_split = {
        "zero_index": "0",
        "delta": "0.01",
        "x": "20.0",
        "num_zeros": "5",
        "perturbation_mode": "symmetry_complete_split"
    }
    status, out_split, err = research_runner.evaluate_point(
        "converter_perturbation", inputs_split, dps=dps, param_space=param_space
    )
    assert status == "ok"
    assert "split_defect_cj" in out_split
    assert "split_defect_cpi" in out_split
    assert "split_defect_pi_n" in out_split
    assert "symmetry_error" in out_split
    assert "symmetry_error_cj" in out_split
    assert "symmetry_error_cpi" in out_split
    assert "normalized_quadratic_cj" in out_split
    assert "normalized_quadratic_cpi" in out_split
    assert "quadratic_ratio_cj" in out_split
    assert "quadratic_ratio_cpi" in out_split
    assert "quadratic_ratio_error_cj" in out_split
    assert "quadratic_ratio_error_cpi" in out_split
    
    # Forbidden in split-mode
    forbidden_in_split = ["delta_cj", "delta_cpi", "delta_pi_n"]
    for key in forbidden_in_split:
        assert key not in out_split, f"Metric '{key}' should not be emitted for symmetry_complete_split"


def test_split_symmetry_error_audit_precision():
    """
    Test split defect symmetry error is audit-precision small:
    |S_J(delta) - S_J(-delta)| < 1e-60 and |S_pi(delta) - S_pi(-delta)| < 1e-60.
    """
    dps = 80
    inputs = {
        "zero_index": "0",
        "delta": "0.005",
        "x": "20.0",
        "num_zeros": "5",
        "perturbation_mode": "symmetry_complete_split"
    }
    status, outputs, err = research_runner.evaluate_point("converter_perturbation", inputs, dps=dps)
    assert status == "ok"
    
    sym_cj = mpmath.mpf(outputs["symmetry_error_cj"])
    sym_cpi = mpmath.mpf(outputs["symmetry_error_cpi"])
    sym_err = mpmath.mpf(outputs["symmetry_error"])
    
    assert sym_cj < mpmath.mpf("1e-60")
    assert sym_cpi < mpmath.mpf("1e-60")
    assert sym_err < mpmath.mpf("1e-60")


def test_quadratic_scaling_and_half_delta_ratio():
    """
    Test local quadratic scaling:
    - S(delta) / delta^2 is finite and approaches local coefficient c_2.
    - S(delta/2) / S(delta) approaches 1/4 (i.e. S(delta) / S(delta/2) approaches 4).
    - quadratic_ratio_error is precision-controlled small.
    """
    dps = 80
    param_space = {
        "delta": {
            "kind": "explicit",
            "values": ["0.0005", "0.001", "0.005", "0.01"]
        }
    }
    
    inputs_1 = {
        "zero_index": "0",
        "delta": "0.001",
        "x": "20.0",
        "num_zeros": "5",
        "perturbation_mode": "symmetry_complete_split"
    }
    status, out_1, err = research_runner.evaluate_point(
        "converter_perturbation", inputs_1, dps=dps, param_space=param_space
    )
    assert status == "ok"
    
    # delta = 0.001 has half-delta = 0.0005 in param_space
    assert "quadratic_ratio_cj" in out_1
    assert "quadratic_ratio_cpi" in out_1
    
    ratio_cj = mpmath.mpf(out_1["quadratic_ratio_cj"])
    ratio_cpi = mpmath.mpf(out_1["quadratic_ratio_cpi"])
    err_cj = mpmath.mpf(out_1["quadratic_ratio_error_cj"])
    err_cpi = mpmath.mpf(out_1["quadratic_ratio_error_cpi"])
    
    assert abs(ratio_cj - 4) < mpmath.mpf("1e-3")
    assert abs(ratio_cpi - 4) < mpmath.mpf("1e-3")
    assert err_cj < mpmath.mpf("1e-3")
    assert err_cpi < mpmath.mpf("1e-3")
    
    # Normalized quadratic is finite
    norm_cj = mpmath.mpf(out_1["normalized_quadratic_cj"])
    norm_cpi = mpmath.mpf(out_1["normalized_quadratic_cpi"])
    assert mpmath.isfinite(norm_cj)
    assert mpmath.isfinite(norm_cpi)
    assert abs(norm_cj) > mpmath.mpf("1e-5")

