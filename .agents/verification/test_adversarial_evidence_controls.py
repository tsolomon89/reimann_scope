"""test_adversarial_evidence_controls.py — Adversarial Evidence Controls & Defect Regression Suite.

Validates the 12 critical failure modes identified during the TC continuation audit:
 1. Reject fake positivity backed only by an arbitrary threshold (< 50.0).
 2. Reject K=0 trivial-zero tail bound ignoring test profile support / decay.
 3. Reject candidate acceptance when total relative error exceeds target or numerical uncertainty is overwhelming.
 4. Reject column error derived from scalar norm differences or identical refinement grids.
 5. Reject empty research campaigns, missing required regimes, or NaN / Inf values.
 6. Reject mixed or increasing error trends labeled as monotonic convergence.
 7. Reject failed mesh stability promoted to exact rank or universal analytic obstruction.
 8. Reject cosmetic boundary phrases and unreviewed claims claiming audit pass (must stay AWAITING_INDEPENDENT_REVIEW).
 9. Reject missing evidence fields silently normalized to EXACT or external proof (must stay UNKNOWN and fail).
10. Reject scalar finite algebraic Lean lemma promoted to universal infinite analytic theorem.
11. Reject author self-review, self-certification, or review lacking adversarial challenges.
12. Reject mission completion when active research obligations remain unresolved in queue.
"""

import os
import sys
import math
import json
import tempfile
import pytest
import numpy as np

# Set up paths for skill and core imports
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILL_DIR = os.path.abspath(os.path.join(REPO_ROOT, ".agents", "skills", "zeta-proof-audit", "scripts"))
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import tc.approximation as app
import tc.weil_forms as wf
from audit_claim_spec import audit_claim_specification, verify_independent_review


class TestAdversarialEvidenceControls:
    """Production test suite enforcing evidence requirements across 12 adversarial failure modes."""

    def test_01_reject_fake_positivity_backed_only_by_arbitrary_threshold(self):
        """Mode 1: Reject fake positivity claimed solely from prime_cross_weight < 50.0.

        Requires genuine Archimedean dominance B_arch > B_prime and scopes conclusion
        strictly to EMPIRICAL_TWO_STATION_VECTOR_SIGN without claiming universal positivity.
        """
        res = app.audit_same_grade_resonance_K_neg3(h=0.05, window=(8.0, 20.0))
        assert res['status'] == 'SAME_GRADE_RESONANCE_AUDITED'

        # Check genuine quadratic form calculations
        rf = res['resonance_analysis']
        assert 'B_arch_form_lower_bound' in rf
        assert 'B_prime_form_evaluated' in rf
        assert 'net_weil_form_margin' in rf
        assert rf['B_arch_form_lower_bound'] > rf['B_prime_form_evaluated']
        assert rf['net_weil_form_margin'] > 0.0

        # Conclusion must be strictly scoped to two-station vector, never universal
        conc = res['positivity_conclusion']
        assert conc['evidence_scope'] == 'EMPIRICAL_TWO_STATION_VECTOR_SIGN'
        assert conc['archimedean_diagonal_dominates'] is True
        assert "positive definiteness of the full subspace" not in conc['reason'].lower()
        assert "constant-50 comparison has been removed" in conc['reason']

    def test_02_reject_k0_tail_bound_ignoring_test_profile(self):
        """Mode 2: Reject K=0 trivial-zero tail bound that ignores test profile support / decay.

        For K=0, a_0 = 1, so Q_b(-2k) -> b_0 != 0. Trivial zero remainder convergence requires
        test profile support [A, B] with A > 1 so Phi(-2k) decays geometrically.
        """
        # Baseline audit with valid profile supported on [1.5, 4.0] (A > 1)
        res_valid = app.audit_arithmetic_spectral_exact_formula(
            grades=[0, -1, -2, -3],
            test_profile={'support': (1.5, 4.0), 'amplitude_norm': 1.0}
        )
        triv = res_valid['trivial_zeros_remainder']
        assert triv['is_exponentially_convergent'] is True
        assert triv['tail_bound_k_gt_5'] > 0.0
        assert triv['reproduced_K0_geometric_failure']['Q_b_decays_alone_without_profile'] is False

        # Adversarial audit with profile touching or crossing x <= 1 (A = 0.8) must be rejected
        with pytest.raises(ValueError, match="Test profile support infimum A must be strictly greater than 1.0"):
            app.audit_arithmetic_spectral_exact_formula(
                grades=[0, -1, -2, -3],
                test_profile={'support': (0.8, 3.0), 'amplitude_norm': 1.0}
            )

        # Nontrivial zero tail control must be marked open, not falsely certified
        assert res_valid['spectral_research_conclusions']['nontrivial_zero_tail_status'] == 'UNRESOLVED_REQUIRES_STIELTJES_BOUND'

    def test_03_reject_candidate_error_exceeding_target_or_high_uncertainty(self):
        """Mode 3: Reject candidate acceptance when total error >= target or uncertainty >= 0.20.

        Verifies that:
        1. Unachievable targets terminate with GRADE_BUDGET_EXHAUSTED and target_satisfied=False.
        2. Production calculation rejects fine error zero with medium-grid error 100 (uncertainty set to 1.0, not zero).
        3. Production calculation rejects NaN absolute error (uncertainty set to 1.0, not accepted).
        """
        # Target epsilon 0.001 cannot be satisfied within K >= -1 budget
        res = app.execute_adaptive_diagonal_search(
            target_fractions=[0.001], max_negative_grade=-1, n_points=41
        )
        step = res['steps'][0]
        assert step['target_satisfied'] is False
        assert step['budget_status'] == 'GRADE_BUDGET_EXHAUSTED'
        assert step['accepted_grade_K'] is None

        # Verify all rejected grade attempts record clear discrepancy reasons
        grade_rejections = [rej for rej in res['rejected_attempts'] if 'E_total_relative' in rej]
        assert len(grade_rejections) > 0
        for rej in grade_rejections:
            assert rej['E_total_relative'] >= 0.001 or rej.get('rel_uncertainty', 0.0) >= 0.20

        # Adversarial Check A: Fine error zero with medium-grid error 100
        def mock_zero_fine_100_med(K, h, window, n_points):
            if n_points >= 41:
                return {'station_count': 5, 'active_station_count': 5, 'errors': {'E_arith_H1': 0.0, 'E_arith_relative': 0.0, 'E_smooth_H1': 0.001, 'E_smooth_relative': 0.001, 'E_total_H1': 0.0, 'E_total_relative': 0.0}}
            else:
                return {'station_count': 5, 'active_station_count': 5, 'errors': {'E_arith_H1': 100.0, 'E_arith_relative': 100.0, 'E_smooth_H1': 0.001, 'E_smooth_relative': 0.001, 'E_total_H1': 100.0, 'E_total_relative': 100.0}}

        orig_compute = app.compute_arithmetic_vs_smoothing_error
        app.compute_arithmetic_vs_smoothing_error = mock_zero_fine_100_med
        try:
            res_adv_a = app.execute_adaptive_diagonal_search(target_fractions=[0.05], max_negative_grade=0, n_points=41)
            step_a = res_adv_a['steps'][0]
            assert step_a['target_satisfied'] is False, "Fine error zero with medium 100 must be rejected"
            assert step_a['accepted_grade_K'] is None
            assert len(res_adv_a['rejected_attempts']) > 0
            assert any(r.get('rel_uncertainty', 0.0) >= 0.20 for r in res_adv_a['rejected_attempts'])
            assert any("invalid/non-positive/NaN errors" in r.get('reason', '') for r in res_adv_a['rejected_attempts'])
        finally:
            app.compute_arithmetic_vs_smoothing_error = orig_compute

        # Adversarial Check B: Absolute error NaN with finite relative error
        def mock_nan_absolute(K, h, window, n_points):
            return {'station_count': 5, 'active_station_count': 5, 'errors': {'E_arith_H1': 0.01, 'E_arith_relative': 0.01, 'E_smooth_H1': 0.001, 'E_smooth_relative': 0.001, 'E_total_H1': float('nan'), 'E_total_relative': 0.01}}

        app.compute_arithmetic_vs_smoothing_error = mock_nan_absolute
        try:
            res_adv_b = app.execute_adaptive_diagonal_search(target_fractions=[0.05], max_negative_grade=0, n_points=41)
            step_b = res_adv_b['steps'][0]
            assert step_b['target_satisfied'] is False, "NaN absolute error must be rejected"
            assert step_b['accepted_grade_K'] is None
            assert len(res_adv_b['rejected_attempts']) > 0
            assert any(r.get('rel_uncertainty', 0.0) >= 0.20 for r in res_adv_b['rejected_attempts'])
            assert any("invalid/non-positive/NaN errors" in r.get('reason', '') for r in res_adv_b['rejected_attempts'])
        finally:
            app.compute_arithmetic_vs_smoothing_error = orig_compute

    def test_04_reject_column_error_from_scalar_norm_difference_or_identical_grids(self):
        """Mode 4: Reject column uncertainty estimated by scalar norm differences |norm(f) - norm(g)|.

        Requires genuine common-grid H^1 function difference, strictly distinct refinement meshes,
        and tracking of Gram entry differences and SVD subspace projection stability.
        """
        res = app.investigate_actual_tc_grade_cancellation(
            grades=[-1, -2], anchor_grade=0, h=0.05, n_points=401
        )
        ms = res['mesh_stability']
        # Distinct mesh resolutions
        assert ms['coarse_grid_points'] < ms['medium_grid_points'] < ms['grid_points']

        # Column uncertainties must use genuine H^1 function differences
        col_unc = res['independent_target_fit']['column_uncertainty_estimates']
        assert 0 in col_unc
        assert -1 in col_unc
        assert -2 in col_unc
        for K, unc in col_unc.items():
            assert unc > 0.0 and math.isfinite(unc)

        # Gram entry and subspace projection stability must be explicitly computed
        assert 'gram_entry_differences' in ms
        assert 'subspace_projection_stability' in ms
        assert ms['gram_entry_differences']['relative_frobenius_difference'] >= 0.0
        assert ms['subspace_projection_stability']['subspace_dimension'] == 2
        assert 'function_subspace_distance_H1' in ms['subspace_projection_stability']
        assert ms['subspace_projection_stability']['function_subspace_distance_H1'] >= 0.0
        assert 'directions_stable_under_refinement' in ms

    def test_05_reject_empty_campaign_missing_regimes_or_nan_inf(self):
        """Mode 5: Reject empty campaigns, missing regime checks, or NaN/Inf values.

        Directly submits defective and empty evidence through the production pipeline
        run_tc_negative_grade_approximation_campaign and asserts invariants fail.
        """
        # 1. Check data/tc_arithmetic_residual_research.json
        residual_path = os.path.join(REPO_ROOT, "data", "tc_arithmetic_residual_research.json")
        assert os.path.exists(residual_path), f"Missing artifact at {residual_path}"
        with open(residual_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data['status'] == 'TC_GRADE_CANCELLATION_RESEARCH_CAMPAIGN_COMPLETED'
        required_keys = [
            'cancellation_anchor_0_h_005',
            'cancellation_anchor_0_h_002',
            'cancellation_moving_anchor_neg1',
            'same_grade_resonance_K_neg3',
            'arithmetic_spectral_explicit_formula',
            'adaptive_diagonal_search',
            'executive_synthesis'
        ]
        for key in required_keys:
            assert key in data, f"Missing required campaign section: {key}"

        # 2. Check data/tc_negative_grade_approximation_campaign.json
        camp_path = os.path.join(REPO_ROOT, "data", "tc_negative_grade_approximation_campaign.json")
        assert os.path.exists(camp_path), f"Missing artifact at {camp_path}"
        with open(camp_path, "r", encoding="utf-8") as f:
            camp = json.load(f)

        assert camp['status'] == 'TC_NEGATIVE_GRADE_CAMPAIGN_COMPLETED'
        assert len(camp['regime_1_single_grade_convergence']) > 0
        assert len(camp['regime_2_fixed_grade_bandwidth_scaling']) > 0
        assert 'regime_3_joint_diagonal_schedule' in camp

        # Recursively check no NaN or Inf in numeric fields
        def check_no_nan_inf(obj, path=""):
            if isinstance(obj, float):
                assert not math.isnan(obj), f"NaN encountered at {path}"
                assert not math.isinf(obj), f"Inf encountered at {path}"
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    check_no_nan_inf(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for idx, v in enumerate(obj):
                    check_no_nan_inf(v, f"{path}[{idx}]")

        check_no_nan_inf(data)
        check_no_nan_inf(camp)

        # 3. Direct adversarial submission: Submit empty required campaign sections through production pipeline
        camp_empty = app.run_tc_negative_grade_approximation_campaign(
            output_path="",
            override_regime_1_results=[],
            override_regime_2_results=[],
            override_regime_3_results=[],
            override_exp_continuum={},
            override_exp_independent={}
        )
        assert camp_empty['status'] == 'TC_NEGATIVE_GRADE_CAMPAIGN_INVARIANTS_FAILED'
        assert camp_empty['invariants_verified'] is False
        assert len(camp_empty['audit_invariant_failures']) >= 5
        assert any("Regime 1: Required single-grade convergence results are empty" in f for f in camp_empty['audit_invariant_failures'])
        assert any("Regime 2: Required fixed-grade bandwidth scaling results are empty" in f for f in camp_empty['audit_invariant_failures'])

        # 4. Direct adversarial submission: Submit NaN value in regime 1 through production pipeline
        bad_regime_1 = [{
            'K': 0, 'h': 0.10, 'station_count': 10, 'active_station_count': 10,
            'provenance_hash': 'test', 'E_arith_H1': float('nan'), 'E_arith_rel': 0.1,
            'E_smooth_H1': 0.1, 'E_smooth_rel': 0.1, 'E_total_H1': 0.2, 'E_total_rel': 0.2
        }]
        camp_nan = app.run_tc_negative_grade_approximation_campaign(
            output_path="",
            override_regime_1_results=bad_regime_1,
            override_regime_2_results=[],
            override_regime_3_results=[],
            override_exp_continuum={},
            override_exp_independent={}
        )
        assert camp_nan['status'] == 'TC_NEGATIVE_GRADE_CAMPAIGN_INVARIANTS_FAILED'
        assert any("Invalid, non-finite, or negative arithmetic error" in f for f in camp_nan['audit_invariant_failures'])

    def test_06_reject_mixed_or_increasing_trend_labeled_monotonic(self):
        """Mode 6: Reject mixed or increasing error trends falsely labeled as monotonic convergence."""
        camp_path = os.path.join(REPO_ROOT, "data", "tc_negative_grade_approximation_campaign.json")
        with open(camp_path, "r", encoding="utf-8") as f:
            camp = json.load(f)

        r3 = camp['regime_3_joint_diagonal_schedule']
        errors = [p['E_total_rel'] for p in r3['schedule_pairs']]
        is_strictly_decreasing = all(errors[i] < errors[i-1] for i in range(1, len(errors)))

        # Since errors increase dramatically (bump Sobolev scaling), it must NOT be labeled monotonic
        assert is_strictly_decreasing is False
        assert r3['is_monotonically_decreasing'] is False
        assert r3['empirical_schedule_verdict'] == 'EMPIRICAL_DIVERGENCE_ON_TESTED_SCHEDULE'

    def test_07_reject_failed_stability_promoted_to_exact_rank_or_universal_obstruction(self):
        """Mode 7: Reject underresolved / unstable mesh promoted to certified rank or analytic obstruction."""
        res = app.investigate_actual_tc_grade_cancellation(
            grades=[-1, -2], anchor_grade=0, h=0.01, n_points=35
        )
        assert res['mesh_stability']['directions_stable_under_refinement'] is False
        desc = res['research_findings']['surviving_directions_description']
        assert "UNRESOLVED / FAILED" in desc
        assert "cannot be certified as stable" in desc

    def test_08_reject_claim_with_fake_boundary_phrase_or_missing_review(self):
        """Mode 8: Reject cosmetic boundary phrases and unreviewed claims claiming audit pass."""
        clm_path = os.path.join(REPO_ROOT, ".agents", "claims", "CLM-CT-022.json")
        with open(clm_path, "r", encoding="utf-8") as f:
            base_claim = json.load(f)

        # Case A: Fake boundary phrase in falsification_attempts fails Gate 5
        fake_boundary_claim = dict(base_claim)
        fake_boundary_claim['claim_id'] = "CLM-TEST-ADVERSARIAL-08"
        fake_boundary_claim['falsification_attempts'] = ["Claim holds without boundary check"]
        res_a = audit_claim_specification(fake_boundary_claim, repo_root=REPO_ROOT)
        assert res_a['status'] == 'FAIL'
        assert any("Gate 5 [Dominance & Boundary] VIOLATION" in v for v in res_a['violations'])

        # Case B: Genuine boundary analysis but missing independent review artifact -> stays AWAITING_INDEPENDENT_REVIEW
        unreviewed_claim = dict(base_claim)
        unreviewed_claim['claim_id'] = "CLM-TEST-ADVERSARIAL-08B"
        res_b = audit_claim_specification(unreviewed_claim, repo_root=REPO_ROOT)
        assert res_b['status'] == 'PASS'
        assert res_b['mathematical_review_status'] == 'AWAITING_INDEPENDENT_REVIEW'

    def test_09_reject_missing_evidence_normalized_to_exact_or_external_proof(self):
        """Mode 9: Missing evidence class must NOT be defaulted to EXACT or EXTERNAL_ANALYTIC_PROOF.

        Must default to UNKNOWN and fail Gate 10 / schema validation.
        """
        claim_missing_evidence = {
            "claim_id": "CLM-TEST-ADVERSARIAL-09",
            "mathematical_statement": "Identity f(x) = g(x)",
            "quantifiers": "\\forall x",
            "hypotheses": ["None"],
            "claimed_scope": "ALL_X",
            "normalization": "Standard",
            "falsification_tests": ["test_f_eq_g"],
            "verification_command": "pytest",
            "artifact_hashes": ["sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"],
            "git_commit": "82643cafd605492233c6c1e992b78c2c30d45f13",
            "dependencies": ["Hardy 1914"],
            "author": "Test Author",
            "status": "PROPOSED",
            "schema_version": "1.0",
            "tolerances": {"epsilon": 1e-12},
            "boundary_cases_analyzed": "Boundary behavior verified via asymptotic expansions as x -> +/- infty.",
            "external_references": ["Hardy 1914, Sur les zeros de la fonction zeta de Riemann"]
        }
        res = audit_claim_specification(claim_missing_evidence, repo_root=REPO_ROOT)
        assert res['status'] == 'FAIL'
        assert any("UNKNOWN" in v or "evidence" in v.lower() for v in res['violations'])

    def test_10_reject_scalar_algebraic_lemma_promoted_to_infinite_analytic_theorem(self):
        """Mode 10: Reject finite scalar algebraic Lean lemma promoted to universal analytic theorem."""
        claim_overreach = {
            "claim_id": "CLM-TEST-ADVERSARIAL-10",
            "mathematical_statement": "The Riemann zeta function zeta(s) has no nontrivial zeros off the critical line Re(s) = 1/2.",
            "quantifiers": "\\forall s \\in \\mathbb{C}, (\\zeta(s) = 0 \\land 0 < \\text{Re}(s) < 1) \\implies \\text{Re}(s) = 1/2",
            "hypotheses": ["Analytic continuation of Riemann zeta function"],
            "claimed_scope": "UNIVERSAL_RIEMANN_HYPOTHESIS",
            "normalization": "Standard completed xi function",
            "evidence_class": "PROVED_CONDITIONAL",
            "boundary_cases_analyzed": "Full critical strip boundaries analyzed via Phragmen-Lindelof principle.",
            "falsification_tests": ["test_known_zeros"],
            "verification_command": "lake build",
            "artifact_hashes": ["sha256:abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcd"],
            "git_commit": "82643cafd605492233c6c1e992b78c2c30d45f13",
            "dependencies": ["Riemann 1859"],
            "author": "Overreach Generator",
            "status": "PROPOSED",
            "schema_version": "1.0",
            "tolerances": {"epsilon": 0.0},
            "external_references": ["Riemann 1859, Ueber die Anzahl der Primzahlen unter einer gegebenen Groesse"],
            "formal_spec": {
                "system": "Lean 4",
                "formal_statement": "theorem rh_algebraic_scalar_identity (m n : Int) (h : m = n) : m * 2 * Real.pi = n * 2 * Real.pi"
            }
        }
        res = audit_claim_specification(claim_overreach, repo_root=REPO_ROOT)
        # Cannot be certified as passing mathematical audit
        assert res['mathematical_review_status'] != 'INDEPENDENT_MATHEMATICAL_AUDIT_PASSED'

    def test_11_reject_author_self_review_and_stale_reviews(self):
        """Mode 11: Reject review artifacts created by the claim author, explicitly rejected reviews, or stale/wrong hashes."""
        spec = {
            "claim_id": "CLM-TEST-REVIEW-AUDIT",
            "author": "Alice Researcher",
            "git_commit": "82643cafd605492233c6c1e992b78c2c30d45f13"
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            claims_dir = os.path.join(temp_dir, ".agents", "claims")
            reviews_dir = os.path.join(claims_dir, "reviews")
            os.makedirs(reviews_dir, exist_ok=True)
            claim_file = os.path.join(claims_dir, "CLM-TEST-REVIEW-AUDIT.json")
            with open(claim_file, "w", encoding="utf-8") as f:
                json.dump(spec, f)

            review_file = os.path.join(reviews_dir, "CLM-TEST-REVIEW-AUDIT-derivation-review.md")

            # Case A: Explicitly rejected review (user reproduction: "Derivation: Incorrect. Objections: Fatal circularity. Resolution: REJECTED.")
            with open(review_file, "w", encoding="utf-8") as f:
                f.write("Derivation: Incorrect. Objections: Fatal circularity. Resolution: REJECTED. Date: yesterday.\n")
            passed, reason, _ = verify_independent_review("CLM-TEST-REVIEW-AUDIT", spec, repo_root=temp_dir)
            assert passed is False, "Explicitly rejected review must not pass audit"
            assert "negative verdict" in reason.lower() or "fatal objection" in reason.lower()

            # Case B: Author self-review (author reviewing their own work without explicit self-review keyword)
            with open(review_file, "w", encoding="utf-8") as f:
                f.write(
                    "# Independent Derivation Review for CLM-TEST-REVIEW-AUDIT\n"
                    "Reviewer: Alice Researcher\n"
                    "Derivation: Rigorous proof verified.\n"
                    "Objections: Adversarial checks attempted; no contradictions found.\n"
                    "Resolution: PASSED.\n"
                    "Commit: 82643cafd605492233c6c1e992b78c2c30d45f13\n"
                )
            passed, reason, _ = verify_independent_review("CLM-TEST-REVIEW-AUDIT", spec, repo_root=temp_dir)
            assert passed is False, "Author reviewing own work must be rejected"
            assert "Self-review" in reason

            # Case C: Stale commit SHA
            with open(review_file, "w", encoding="utf-8") as f:
                f.write(
                    "# Independent Derivation Review for CLM-TEST-REVIEW-AUDIT\n"
                    "Reviewer: Bob Redteam\n"
                    "Derivation: Rigorous mathematical deduction verified.\n"
                    "Objections: Adversarial checks attempted; no contradictions found.\n"
                    "Resolution: PASSED.\n"
                    "Commit: deadbeef1234567890abcdef1234567890abcdef\n"
                )
            passed, reason, _ = verify_independent_review("CLM-TEST-REVIEW-AUDIT", spec, repo_root=temp_dir)
            assert passed is False, "Stale commit must be rejected"
            assert "Stale review" in reason

            # Case D: Wrong claim hash
            with open(review_file, "w", encoding="utf-8") as f:
                f.write(
                    "# Independent Derivation Review for CLM-TEST-REVIEW-AUDIT\n"
                    "Reviewer: Bob Redteam\n"
                    "Derivation: Rigorous mathematical deduction verified.\n"
                    "Objections: Adversarial checks attempted; no contradictions found.\n"
                    "Resolution: PASSED.\n"
                    "Commit: 82643cafd605492233c6c1e992b78c2c30d45f13\n"
                    "Claim Hash: sha256:0000000000000000000000000000000000000000000000000000000000000000\n"
                )
            passed, reason, _ = verify_independent_review("CLM-TEST-REVIEW-AUDIT", spec, repo_root=temp_dir)
            assert passed is False, "Wrong claim hash must be rejected"
            assert "Wrong claim hash" in reason

            # Case E: Missing objections / adversarial challenge section
            with open(review_file, "w", encoding="utf-8") as f:
                f.write(
                    "# Independent Derivation Review for CLM-TEST-REVIEW-AUDIT\n"
                    "Reviewer: Bob Redteam\n"
                    "Derivation: Rigorous mathematical deduction verified.\n"
                    "Resolution: PASSED.\n"
                    "Commit: 82643cafd605492233c6c1e992b78c2c30d45f13\n"
                )
            passed, reason, _ = verify_independent_review("CLM-TEST-REVIEW-AUDIT", spec, repo_root=temp_dir)
            assert passed is False
            assert "objections" in reason.lower() or "adversarial" in reason.lower()

            # Case F: Valid independent review passes cleanly
            with open(review_file, "w", encoding="utf-8") as f:
                f.write(
                    "# Independent Derivation Review for CLM-TEST-REVIEW-AUDIT\n"
                    "Reviewer: Bob Redteam\n"
                    "Derivation: Rigorous mathematical deduction verified step by step.\n"
                    "Objections: Adversarial stress test on zero-crossings performed; resolved without circularity.\n"
                    "Resolution: PASSED and confirmed.\n"
                    "Commit: 82643cafd605492233c6c1e992b78c2c30d45f13\n"
                )
            passed, reason, _ = verify_independent_review("CLM-TEST-REVIEW-AUDIT", spec, repo_root=temp_dir)
            assert passed is True, f"Valid independent review failed: {reason}"

    def test_12_reject_completion_without_accepted_milestone(self):
        """Mode 12: Enforce that active open research obligations in queue prevent claiming completion.

        Directly invokes the production completion gate app.verify_research_milestone_completion()
        rather than testing a local helper.
        """
        # 1. Directly invoke production completion gate on repository state
        # With active open research obligations, live repository blocks milestone completion.
        can_complete, msg, details = app.verify_research_milestone_completion(repo_root=REPO_ROOT)
        assert can_complete is False, "Active research obligations (TASK-TC-004) must block milestone completion"
        assert "active task" in msg.lower() or "TASK-TC-004" in msg

        # 2. Test isolated temporary queue configurations through production gate
        with tempfile.TemporaryDirectory() as td:
            q_file = os.path.join(td, "queue.json")
            s_file = os.path.join(td, "state.json")
            real_art = os.path.join(td, "real_artifact.json")
            with open(real_art, "w", encoding="utf-8") as rf:
                rf.write('{"status": "OK"}')

            # Case A: Active task in progress
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump({"active_task_id": "TASK-UNRESOLVED", "tasks": [{"task_id": "TASK-UNRESOLVED", "status": "IN_PROGRESS"}]}, f)
            with open(s_file, "w", encoding="utf-8") as f:
                json.dump({"active_tracks": {}}, f)

            can_comp_a, msg_a, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file)
            assert can_comp_a is False
            assert "active task" in msg_a

            # Case B: Unresolved tasks in queue
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump({"active_task_id": None, "tasks": [{"task_id": "TASK-QUEUED", "status": "QUEUED"}]}, f)
            can_comp_b, msg_b, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file)
            assert can_comp_b is False
            assert "unresolved" in msg_b

            # Case C: Active research track in state
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump({"active_task_id": None, "tasks": [{"task_id": "TASK-RESOLVED", "status": "ACCEPTED", "evidence": [real_art], "review_status": "ACCEPTED"}]}, f)
            with open(s_file, "w", encoding="utf-8") as f:
                json.dump({"active_tracks": {"track_1": {"status": "ACTIVE"}}}, f)
            can_comp_c, msg_c, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file, repo_root=td)
            assert can_comp_c is False
            assert "unresolved research track(s) remain" in msg_c

            # Case D: Fully resolved queue and completed tracks
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump({
                    "active_task_id": None,
                    "tasks": [{
                        "task_id": "TASK-RESOLVED",
                        "status": "ACCEPTED",
                        "evidence": [real_art],
                        "review_status": "ACCEPTED"
                    }]
                }, f)
            with open(s_file, "w", encoding="utf-8") as f:
                json.dump({"active_tracks": {"track_1": {"status": "RESOLVED"}}}, f)
            can_comp_d, msg_d, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file, repo_root=td)
            assert can_comp_d is True
            assert "All persistent research obligations and tracks resolved" in msg_d

    def test_13_reject_unscaled_raw_T_differences_and_enforce_authentic_F_scaling(self):
        """Invariant 1: Enforce that zero-sum combinations act on authentic normalized family F_K = a_K T_K (a_K = tau^K),
        not raw unscaled T_K differences.

        Verifies:
        1. Raw differences T_K - T_{-1} without a_K scaling yield huge Archimedean eigenvalues ~ O(10^11 - 10^13).
        2. Contracted zero-sum family G_K = F_K - F_{-1} = tau^K T_K - tau^{-1} T_{-1} yields authentic O(10^7 - 10^9) eigenvalues.
        3. A zero-sum coefficient vector b (sum b_K = 0) corresponds to c_K = a_K * b_K; raw sum c_K is not zero.
        """
        tau = 2.0 * math.pi
        grades = [-1, -2, -3, -4]
        window = (8.0, 20.0)
        h = 0.05

        arch_eval = wf.ArchimedeanKernelEvaluator(h, N_t=1000, z_max=16.0)
        stations_by_grade = {}
        for K in grades:
            st_k = wf.sieve_prime_powers_in_window(window, K, tau=tau)
            items = []
            for n_val, x_float, lam_float in st_k:
                w_val = math.exp(1.0 - 1.0 / (1.0 - (2.0 * (x_float - 8.0) / 12.0 - 1.0)**2)) if 8.0 < x_float < 20.0 else 0.0
                d_val = lam_float * w_val
                if d_val > 0:
                    items.append({'u': math.log(x_float), 'd': d_val})
            stations_by_grade[K] = items

        C_list, S_list = [], []
        for K in grades:
            t_vals = np.array([s['u'] for s in stations_by_grade[K]])
            d_vals = np.array([s['d'] for s in stations_by_grade[K]])
            angles = np.outer(arch_eval.nodes_t, t_vals)
            C_list.append(np.cos(angles) @ d_vals)
            S_list.append(np.sin(angles) @ d_vals)

        W_arch_raw = np.zeros((4, 4))
        for i in range(4):
            for j in range(4):
                W_arch_raw[i, j] = np.sum(arch_eval.base * (C_list[i] * C_list[j] + S_list[i] * S_list[j]))

        P = np.array([
            [-1.0, -1.0, -1.0],
            [ 1.0,  0.0,  0.0],
            [ 0.0,  1.0,  0.0],
            [ 0.0,  0.0,  1.0]
        ])

        # Raw unscaled T differences: P.T @ W_arch_raw @ P
        W_raw_diff = P.T @ W_arch_raw @ P
        eigs_raw = np.linalg.eigvalsh(W_raw_diff)
        assert eigs_raw[0] > 1e11, "Raw unscaled T differences must be O(10^11)"
        assert np.isclose(eigs_raw[0], 2.86129074066e11, rtol=1e-4)

        # Authentic F differences: P.T @ D @ W_arch_raw @ D @ P with D = diag(tau^K)
        D = np.diag([tau**K for K in grades])
        W_auth_diff = P.T @ D @ W_arch_raw @ D @ P
        eigs_auth = np.linalg.eigvalsh(W_auth_diff)
        assert eigs_auth[0] < 1e8, "Authentic F differences must be scaled by tau^K ~ O(10^7)"
        assert np.isclose(eigs_auth[0], 1.31911601924e7, rtol=1e-4)

    def test_14_fourier_cutoff_tail_and_exact_position_space_enclosure(self):
        """Invariant 2: Enforce that Fourier truncation cutoff z_max=16 omits ~28.7% of the bump norm,
        and that exact position-space quadrature encloses the complete bump without Fourier truncation error.
        """
        h = 0.05
        exact_psi_norm_sq = 175879906.7832035

        arch_eval = wf.ArchimedeanKernelEvaluator(h, N_t=1000, z_max=16.0)
        t_nodes = arch_eval.nodes_t
        weights = arch_eval.weights_t
        fourier_vals = np.array([wf.kappa_hat_fast(t * h) for t in t_nodes])
        psi_hat_sq = ((t_nodes**2 + 0.25) * fourier_vals)**2
        truncated_norm_sq = (1.0 / math.pi) * np.sum(weights * psi_hat_sq)

        omitted_ratio = (exact_psi_norm_sq - truncated_norm_sq) / exact_psi_norm_sq
        assert 0.25 < omitted_ratio < 0.32, f"Fourier truncation at z_max=16 must omit ~28.7% of norm, got {omitted_ratio:.4f}"

        c_h_0 = wf._compute_C_h_position_quad(0.0, h)
        assert np.isclose(c_h_0, exact_psi_norm_sq, rtol=1e-4)

    def test_15_resonant_prime_matrix_completion_under_log2_separation(self):
        """Invariant 3: Enforce that prime-power matrix computation detects same-grade resonances
        within support and never falsely returns zero for W_prime.
        """
        res = wf.compute_canonical_reflected_weil_matrix(
            grades=[0],
            window=(1.0, 5.0),
            h=0.05
        )
        W_prime = res["W_prime"]
        W_arch = res["W_arch"]
        W_net = res["W"]

        assert W_prime[0][0] > 1e7, f"W_prime must be non-zero from log(2) resonance, got {W_prime[0][0]}"
        assert np.isclose(W_prime[0][0], 42528293.17, rtol=1e-3)
        assert np.isclose(W_net[0][0], W_arch[0][0] - W_prime[0][0], rtol=1e-6)
        assert W_net[0][0] > 0, "Archimedean background must dominate the log(2) prime resonance"

    def test_16_subspace_distance_rejects_orthogonal_spans_with_identical_grams(self):
        """Invariant 4: Enforce genuine principal angle Grassmannian distance.
        Must reject orthogonal subspaces even if both possess identical Gram matrices (e.g. G_A = G_B = I).
        """
        x = np.linspace(-1, 1, 1001)
        du = x[1] - x[0]
        f1 = np.sin(np.pi * x)
        f2 = np.cos(np.pi * x)
        f1_p = np.pi * np.cos(np.pi * x)
        f2_p = -np.pi * np.sin(np.pi * x)
        basis_A = np.array([f1, f2])
        basis_A_p = np.array([f1_p, f2_p])

        # Orthogonal spans
        f3 = np.sin(2 * np.pi * x)
        f4 = np.cos(2 * np.pi * x)
        f3_p = 2 * np.pi * np.cos(2 * np.pi * x)
        f4_p = -2 * np.pi * np.sin(2 * np.pi * x)
        basis_C = np.array([f3, f4])
        basis_C_p = np.array([f3_p, f4_p])

        res_orth = app.compute_function_subspace_principal_angles(basis_A, basis_A_p, basis_C, basis_C_p, du)
        assert res_orth['distance'] > 0.95
        assert res_orth['stable'] is False, "Orthogonal subspaces must be marked unstable"

        # Rotated identical spans
        theta = np.pi / 4
        basis_B = np.array([np.cos(theta)*f1 + np.sin(theta)*f2, -np.sin(theta)*f1 + np.cos(theta)*f2])
        basis_B_p = np.array([np.cos(theta)*f1_p + np.sin(theta)*f2_p, -np.sin(theta)*f1_p + np.cos(theta)*f2_p])
        res_rot = app.compute_function_subspace_principal_angles(basis_A, basis_A_p, basis_B, basis_B_p, du)
        assert res_rot['distance'] < 1e-4
        assert res_rot['stable'] is True, "Identical spans under change of basis must be marked stable"

        # Rank loss
        basis_D = np.array([f1, 2 * f1])
        basis_D_p = np.array([f1_p, 2 * f1_p])
        res_rank = app.compute_function_subspace_principal_angles(basis_A, basis_A_p, basis_D, basis_D_p, du)
        assert res_rank['distance'] == 1.0
        assert res_rank['stable'] is False

    def test_17_reject_invalid_or_nan_error_post_mesh_refinement(self):
        """Invariant 5: Enforce that mesh refinement re-evaluates validity.
        If refined grid generates negative, -inf, or NaN error, candidate must be rejected and uncertainty set to 1.0.
        """
        def mock_error_corrupts_on_refinement(K, h, window, n_points):
            if n_points < 41:
                # Medium grid on initial check: uncertainty = |0.002 - 0.001| / 0.001 = 1.0 >= 0.20
                return {'station_count': 5, 'active_station_count': 5, 'errors': {'E_arith_H1': 0.002, 'E_arith_relative': 0.002, 'E_smooth_H1': 0.001, 'E_smooth_relative': 0.001, 'E_total_H1': 0.002, 'E_total_relative': 0.002}}
            elif n_points == 41:
                # Fine grid on initial check
                return {'station_count': 5, 'active_station_count': 5, 'errors': {'E_arith_H1': 0.001, 'E_arith_relative': 0.001, 'E_smooth_H1': 0.001, 'E_smooth_relative': 0.001, 'E_total_H1': 0.001, 'E_total_relative': 0.001}}
            else:
                # Refined grid produces negative or non-finite error
                return {'station_count': 5, 'active_station_count': 5, 'errors': {'E_arith_H1': -0.5, 'E_arith_relative': -0.5, 'E_smooth_H1': 0.001, 'E_smooth_relative': 0.001, 'E_total_H1': -0.5, 'E_total_relative': -0.5}}

        orig = app.compute_arithmetic_vs_smoothing_error
        app.compute_arithmetic_vs_smoothing_error = mock_error_corrupts_on_refinement
        try:
            res = app.execute_adaptive_diagonal_search(target_fractions=[0.01], max_negative_grade=0, n_points=41)
            step = res['steps'][0]
            assert step['target_satisfied'] is False, "Candidate corrupted on refinement must be rejected"
            assert step['accepted_grade_K'] is None
            assert len(res['rejected_attempts']) > 0
            assert any(r.get('rel_uncertainty') == 1.0 for r in res['rejected_attempts'])
            assert any("invalid/non-positive/NaN errors" in r.get('reason', '') for r in res['rejected_attempts'])
        finally:
            app.compute_arithmetic_vs_smoothing_error = orig

    def test_18_campaign_preserves_regime3_invariant_failures(self):
        """Invariant 6: Campaign failure preservation.
        Enforces that Regime 3 invariants fail if contraction or smoothing error bounds are not verified.
        """
        bad_regime_3 = [{
            'target_fraction': 0.1,
            'achieved_error': 0.5,
            'target_satisfied': False,
            'contraction_satisfied': False,
            'smoothing_error_bound_satisfied': True
        }]
        camp_res = app.run_tc_negative_grade_approximation_campaign(
            output_path="",
            override_regime_1_results=[{'K': 0, 'h': 0.1, 'station_count': 5, 'active_station_count': 5, 'provenance_hash': 'h', 'E_arith_H1': 0.1, 'E_arith_rel': 0.1, 'E_smooth_H1': 0.1, 'E_smooth_rel': 0.1, 'E_total_H1': 0.2, 'E_total_rel': 0.2}],
            override_regime_2_results=[{'K': 0, 'h': 0.1, 'station_count': 5, 'active_station_count': 5, 'provenance_hash': 'h', 'E_arith_H1': 0.1, 'E_arith_rel': 0.1, 'E_smooth_H1': 0.1, 'E_smooth_rel': 0.1, 'E_total_H1': 0.2, 'E_total_rel': 0.2}],
            override_regime_3_results=bad_regime_3,
            override_exp_continuum={'status': 'ok'},
            override_exp_independent={'status': 'ok'}
        )
        assert camp_res['status'] == 'TC_NEGATIVE_GRADE_CAMPAIGN_INVARIANTS_FAILED'
        assert camp_res['invariants_verified'] is False
        assert any("contraction" in f.lower() for f in camp_res['audit_invariant_failures'])

    def test_19_review_verifier_rejects_pending_status_and_not_approved(self):
        """Invariant 7: Review verifier hardening.
        Rejects non-substantive sections, negative verdicts, missing reviewer, and invalid revision binding.
        """
        spec = {
            "claim_id": "CLM-TEST-REVIEW-INVARIANTS",
            "author": "Alice",
            "git_commit": "82643cafd605492233c6c1e992b78c2c30d45f13"
        }
        with tempfile.TemporaryDirectory() as td:
            r_dir = os.path.join(td, ".agents", "claims", "reviews")
            os.makedirs(r_dir, exist_ok=True)
            r_file = os.path.join(r_dir, "CLM-TEST-REVIEW-INVARIANTS-derivation-review.md")

            # 1. PENDING verdict
            with open(r_file, "w", encoding="utf-8") as f:
                f.write(
                    "Reviewer: Redteam Auditor\n"
                    "Derivation: Rigorous.\n"
                    "Objections: Investigating.\n"
                    "Status: PENDING\n"
                    "Commit: 82643cafd605492233c6c1e992b78c2c30d45f13\n"
                )
            ok, msg, _ = verify_independent_review("CLM-TEST-REVIEW-INVARIANTS", spec, repo_root=td)
            assert ok is False
            assert "negative verdict" in msg.lower() or "explicit positive approval" in msg.lower()

            # 2. NOT APPROVED verdict
            with open(r_file, "w", encoding="utf-8") as f:
                f.write(
                    "Reviewer: Redteam Auditor\n"
                    "Derivation: Rigorous.\n"
                    "Objections: Adversarial checks failed.\n"
                    "Verdict: NOT APPROVED\n"
                    "Commit: 82643cafd605492233c6c1e992b78c2c30d45f13\n"
                )
            ok2, msg2, _ = verify_independent_review("CLM-TEST-REVIEW-INVARIANTS", spec, repo_root=td)
            assert ok2 is False
            assert "negative verdict" in msg2.lower()

            # 3. Non-substantive derivation ("pending")
            with open(r_file, "w", encoding="utf-8") as f:
                f.write(
                    "Reviewer: Redteam Auditor\n"
                    "Derivation: Pending.\n"
                    "Objections: Not evaluated.\n"
                    "Verdict: PASSED\n"
                    "Commit: 82643cafd605492233c6c1e992b78c2c30d45f13\n"
                )
            ok3, msg3, _ = verify_independent_review("CLM-TEST-REVIEW-INVARIANTS", spec, repo_root=td)
            assert ok3 is False
            assert "negative verdict" in msg3.lower() or "fatal objection" in msg3.lower() or "non-substantive" in msg3.lower()

            # 4. Missing reviewer
            with open(r_file, "w", encoding="utf-8") as f:
                f.write(
                    "Derivation: Rigorous proof verified step by step.\n"
                    "Objections: Adversarial checks completed.\n"
                    "Verdict: PASSED\n"
                    "Commit: 82643cafd605492233c6c1e992b78c2c30d45f13\n"
                )
            ok4, msg4, _ = verify_independent_review("CLM-TEST-REVIEW-INVARIANTS", spec, repo_root=td)
            assert ok4 is False
            assert "reviewer identity" in msg4.lower()

    def test_20_completion_gate_rejects_empty_tasks_and_unresolved_statuses(self):
        """Invariant 8: Affirmative completion gate hardening.
        Rejects empty task lists, non-terminal task statuses (AWAITING_INDEPENDENT_REVIEW, FAILED),
        unrecorded supersessions, and empty/active tracks.
        """
        with tempfile.TemporaryDirectory() as td:
            q_file = os.path.join(td, "queue.json")
            s_file = os.path.join(td, "state.json")

            # Case 1: Empty tasks list
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump({"active_task_id": None, "tasks": []}, f)
            with open(s_file, "w", encoding="utf-8") as f:
                json.dump({"active_tracks": {"tr1": {"status": "RESOLVED"}}}, f)
            ok1, msg1, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file)
            assert ok1 is False
            assert "no recorded tasks" in msg1

            # Case 2: Task with status AWAITING_INDEPENDENT_REVIEW
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump({"active_task_id": None, "tasks": [{"task_id": "T1", "status": "AWAITING_INDEPENDENT_REVIEW"}]}, f)
            ok2, msg2, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file)
            assert ok2 is False
            assert "unresolved or non-terminal" in msg2 and "T1" in msg2

            # Case 3: Task with status FAILED
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump({"active_task_id": None, "tasks": [{"task_id": "T2", "status": "FAILED"}]}, f)
            ok3, msg3, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file)
            assert ok3 is False
            assert "unresolved or non-terminal" in msg3 and "T2" in msg3

            # Case 4: Superseded task without replacement
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump({"active_task_id": None, "tasks": [{"task_id": "T3", "status": "SUPERSEDED"}]}, f)
            ok4, msg4, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file)
            assert ok4 is False
            assert "lacks recorded replacement" in msg4

            # Case 5: Empty tracks in state.json
            real_art = os.path.join(td, "real_artifact.json")
            with open(real_art, "w", encoding="utf-8") as rf:
                rf.write('{"status": "OK"}')
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump({"active_task_id": None, "tasks": [{"task_id": "T4", "status": "COMPLETED", "evidence": [real_art], "review_status": "ACCEPTED"}]}, f)
            with open(s_file, "w", encoding="utf-8") as f:
                json.dump({"active_tracks": {}}, f)
            ok5, msg5, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file, repo_root=td)
            assert ok5 is False
            assert "no recorded research tracks" in msg5

    def test_21_mellin_tail_bound_repaired_weight_and_uniform_strip_control(self):
        r"""Invariant 9: Repaired Mellin tail bound weight and uniform critical strip control.
        For repository convention \widetilde\Phi(s) = \int_A^B \Phi(x) x^{s-1} dx,
        two integrations by parts give (1 / s(s+1)) \int_A^B \Phi''(x) x^{s+1} dx.
        Numerator requires weight x^{\beta+1}. Old code used x^{1-\beta}, underestimating by 4.8x - 15x.
        Repaired code strictly encloses direct transform at t=50 and incorporates full Trudgian (2014) envelope.
        """
        bound_res = app.derive_stieltjes_nontrivial_zero_tail_bound(window=(8.0, 20.0), k_deriv=2)
        assert bound_res['status'] == 'EXPLICIT_STIELTJES_TAIL_BOUND_CERTIFIED'

        # Check pointwise evaluations at t=50
        pts = bound_res['mellin_point_evaluations_t50']
        # beta = 0.5
        eval_05 = pts['beta_0.5']
        assert eval_05['computed_direct_mellin'] == pytest.approx(0.0104008751, rel=1e-3)
        assert eval_05['repaired_upper_bound'] > eval_05['computed_direct_mellin']
        assert eval_05['enclosure_holds'] is True
        # Ratio of repaired bound to direct transform must be > 1.0 (strict upper bound)
        assert eval_05['repaired_upper_bound'] / eval_05['computed_direct_mellin'] > 2.0

        # beta = 0.7
        eval_07 = pts['beta_0.7']
        assert eval_07['computed_direct_mellin'] == pytest.approx(0.0189061684, rel=1e-3)
        assert eval_07['repaired_upper_bound'] > eval_07['computed_direct_mellin']
        assert eval_07['enclosure_holds'] is True
        assert eval_07['repaired_upper_bound'] / eval_07['computed_direct_mellin'] > 2.0

        # Contrast with flawed old weight bound (underestimated by factors of 4.86 and 14.95)
        assert eval_05['flawed_weight_bound'] < eval_05['computed_direct_mellin']
        assert eval_07['flawed_weight_bound'] < eval_07['computed_direct_mellin']

        # Check full published Trudgian term 0.278 log log T is recorded
        assert bound_res['riemann_von_mangoldt_constants']['c2'] == 0.278

        # Check higher derivative order k=3 produces super-polynomial decay
        bound_k3 = app.derive_stieltjes_nontrivial_zero_tail_bound(window=(8.0, 20.0), k_deriv=3)
        assert 'x^(beta + 3 - 1)' in bound_k3['profile_sobolev_norms']['weight_formula'] or bound_k3['profile_sobolev_norms']['weight_formula'] == 'x^(beta + 2)'
        # At T=1000, tail bound for k=3 drops significantly below 0.001
        tail_1000_k3 = [c for c in bound_k3['cutoff_evaluations'] if c['T_cutoff'] == 1000.0][0]
        assert tail_1000_k3['tail_bound_critical_zeros'] < 0.001

    def test_22_complete_form_prime_evaluation_captures_all_supported_same_grade_pairs(self):
        r"""Invariant 10: Complete same-grade and cross-grade prime pairings.
        For test bump psi_h, prime coupling condition is |\Delta t \mp \log q| < 2h.
        At window [8, 20], h=0.05, grade K=-1:
        There are 17 supported same-grade pairs, none exactly multiplicative (n_b != q * n_a).
        The sweep must not assign zero to this diagonal prime contribution.
        """
        window = (8.0, 20.0)
        h = 0.05
        tau = 2.0 * math.pi
        K = -1

        st = wf.sieve_prime_powers_in_window(window, K, tau=tau)
        items = []
        for n_val, x_float, lam_float in st:
            w_val = math.exp(1.0 - 1.0 / (1.0 - (2.0 * (x_float - 8.0) / 12.0 - 1.0)**2)) if 8.0 < x_float < 20.0 else 0.0
            d_val = lam_float * w_val
            if d_val > 0:
                items.append({'u': math.log(x_float), 'd': d_val, 'n': n_val})

        q_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
        two_h = 2.0 * h
        detected_pairs = []
        for i, a in enumerate(items):
            for j, b in enumerate(items):
                if a['n'] < b['n']:
                    diff = b['u'] - a['u']
                    for q in q_primes:
                        log_q = math.log(q)
                        if abs(diff - log_q) < two_h:
                            detected_pairs.append((a['n'], b['n'], q))

        # Exactly 17 pairs exist in this canonical configuration
        assert len(detected_pairs) == 17
        # None of them are exact integer multiples n_b = q * n_a
        assert not any(b_n == q * a_n for a_n, b_n, q in detected_pairs)

        # In the sweep, evaluate K=-1 diagonal prime contribution
        sweep_res = wf.evaluate_tc_canonical_weil_spectrum_sweep(
            windows=[(8.0, 20.0)],
            bandwidths=[0.05],
            grades=[-1],
            anchor_grade=-1,
            q_max=20
        )
        run_data = sweep_res['runs'][0]
        # The diagonal prime entry is non-zero and negative in position space (~ -1.848e8)
        diag_prime = run_data['contracted_weil_matrix_W_G']['prime_form_matrix'][0][0]
        assert diag_prime < -1.0e8, f"Expected large negative prime diagonal contribution, got {diag_prime}"
        assert abs(diag_prime - (-184787530.24)) < 1.0e5

    def test_23_production_cancellation_rejects_orthogonal_subspaces_with_identical_grams(self):
        """Invariant 11: Production Grassmannian principal-angle stability decision.
        For two orthogonal subspaces with identical singular values / internal Grams:
        Separate Gram comparison yields distance = 0, stable = True (FALSE).
        Grassmannian principal angles yield distance = 1.0, stable = False (TRUE).
        Production directions_stable MUST incorporate Grassmannian principal angles.
        """
        # Create two 2D subspaces on common grid that are mutually orthogonal
        grid = np.linspace(0, 1, 101)
        du = float(grid[1] - grid[0])

        # Subspace A: span of {sin(2 pi x), sin(4 pi x)}
        u1 = np.sin(2.0 * math.pi * grid)
        u1_p = 2.0 * math.pi * np.cos(2.0 * math.pi * grid)
        u2 = np.sin(4.0 * math.pi * grid)
        u2_p = 4.0 * math.pi * np.cos(4.0 * math.pi * grid)
        basis_A = np.array([u1, u2])
        basis_p_A = np.array([u1_p, u2_p])

        # Subspace B: span of {sin(6 pi x), sin(8 pi x)} (orthogonal in H^1 on [0, 1])
        v1 = np.sin(6.0 * math.pi * grid)
        v1_p = 6.0 * math.pi * np.cos(6.0 * math.pi * grid)
        v2 = np.sin(8.0 * math.pi * grid)
        v2_p = 8.0 * math.pi * np.cos(8.0 * math.pi * grid)
        basis_B = np.array([v1, v2])
        basis_p_B = np.array([v1_p, v2_p])

        subspace_res = app.compute_function_subspace_principal_angles(
            basis_A, basis_p_A, basis_B, basis_p_B, du
        )
        assert subspace_res['distance'] == pytest.approx(1.0, abs=1e-3)
        assert subspace_res['stable'] is False

        # Now test investigate_actual_tc_grade_cancellation with production mesh refinement
        res = app.investigate_actual_tc_grade_cancellation(grades=[-1, -2], n_points=301)
        proj_stab = res['mesh_stability']['subspace_projection_stability']
        # Distance must be properly reported from function subspace principal angles
        assert 'function_subspace_distance_H1' in proj_stab
        assert 'min_principal_cosine' in proj_stab
        # Refinement stability must be False when distance exceeds 0.10
        if proj_stab['function_subspace_distance_H1'] >= 0.10:
            assert res['mesh_stability']['directions_stable_under_refinement'] is False

    def test_24_review_verifier_rejects_refusal_verdict_and_nonexistent_commit(self):
        """Invariant 12: Review verifier hardening.
        1. Reject explicit refusal verdict: 'Verdict: DO NOT ACCEPT. The prior version was approved.'
        2. Reject nonexistent git commit SHA, even if it matches the spec string.
        3. Accept valid approval with existing commit SHA.
        """
        spec = {
            "claim_id": "CLM-TEST-REFUSAL-AUDIT",
            "author": "Alice",
            "git_commit": "82643cafd605492233c6c1e992b78c2c30d45f13"
        }
        with tempfile.TemporaryDirectory() as td:
            r_dir = os.path.join(td, ".agents", "claims", "reviews")
            os.makedirs(r_dir, exist_ok=True)
            r_file = os.path.join(r_dir, "CLM-TEST-REFUSAL-AUDIT-derivation-review.md")

            # Case 1: DO NOT ACCEPT verdict followed by 'approved' prose
            with open(r_file, "w", encoding="utf-8") as f:
                f.write(
                    "# Independent Derivation Review for CLM-TEST-REFUSAL-AUDIT\n"
                    "Reviewer: Independent Auditor\n"
                    "Derivation: Rigorous mathematical deduction evaluated.\n"
                    "Objections: Adversarial checks attempted.\n"
                    "Verdict: DO NOT ACCEPT. The prior version was approved.\n"
                    "Commit: 82643cafd605492233c6c1e992b78c2c30d45f13\n"
                )
            ok1, msg1, _ = verify_independent_review("CLM-TEST-REFUSAL-AUDIT", spec, repo_root=td)
            assert ok1 is False, "Explicit refusal verdict 'DO NOT ACCEPT' must be rejected"
            assert "negative verdict" in msg1.lower() or "refusal" in msg1.lower()

            # Case 2: Matching but nonexistent commit SHA
            spec_nonexistent = {
                "claim_id": "CLM-TEST-REFUSAL-AUDIT",
                "author": "Alice",
                "git_commit": "deadbeef1234567890abcdef1234567890abcdef"
            }
            with open(r_file, "w", encoding="utf-8") as f:
                f.write(
                    "# Independent Derivation Review for CLM-TEST-REFUSAL-AUDIT\n"
                    "Reviewer: Independent Auditor\n"
                    "Derivation: Rigorous mathematical deduction evaluated.\n"
                    "Objections: Adversarial checks attempted.\n"
                    "Verdict: PASSED. Verified completely.\n"
                    "Commit: deadbeef1234567890abcdef1234567890abcdef\n"
                )
            ok2, msg2, _ = verify_independent_review("CLM-TEST-REFUSAL-AUDIT", spec_nonexistent, repo_root=td)
            assert ok2 is False, "Matching nonexistent commit SHA must be rejected by git verification"
            assert "nonexistent commit" in msg2.lower()

            # Case 3: Valid approval with real git commit SHA
            with open(r_file, "w", encoding="utf-8") as f:
                f.write(
                    "# Independent Derivation Review for CLM-TEST-REFUSAL-AUDIT\n"
                    "Reviewer: Independent Auditor\n"
                    "Derivation: Rigorous mathematical deduction evaluated.\n"
                    "Objections: Adversarial checks attempted.\n"
                    "Verdict: PASSED. Verified completely.\n"
                    "Commit: 82643cafd605492233c6c1e992b78c2c30d45f13\n"
                )
            ok3, msg3, _ = verify_independent_review("CLM-TEST-REFUSAL-AUDIT", spec, repo_root=td)
            assert ok3 is True, f"Valid review with existing commit must pass, got: {msg3}"

    def test_25_completion_gate_enforces_evidence_paths_and_rejects_refusals(self):
        """Invariant 13: Milestone completion gate enforces evidence and non-rejected review status.
        Rejects:
        1. Task marked RESOLVED with no declared evidence.
        2. Task marked RESOLVED with missing evidence file.
        3. Task marked RESOLVED with review_status: REJECTED.
        4. Accepts only when all terminal tasks have existing evidence files and non-rejected reviews.
        """
        with tempfile.TemporaryDirectory() as td:
            q_file = os.path.join(td, "queue.json")
            s_file = os.path.join(td, "state.json")
            real_evidence_file = os.path.join(td, "real_artifact.json")
            with open(real_evidence_file, "w", encoding="utf-8") as ef:
                ef.write('{"status": "OK"}')

            with open(s_file, "w", encoding="utf-8") as f:
                json.dump({"active_tracks": {"tr1": {"status": "RESOLVED"}}}, f)

            # Case 1: Task RESOLVED with no evidence
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump({
                    "active_task_id": None,
                    "tasks": [{"task_id": "T1", "status": "RESOLVED"}]
                }, f)
            ok1, msg1, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file, repo_root=td)
            assert ok1 is False, "Task with no evidence must block completion"
            assert "no declared evidence" in msg1

            # Case 2: Task RESOLVED with missing evidence file
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump({
                    "active_task_id": None,
                    "tasks": [{
                        "task_id": "T2",
                        "status": "RESOLVED",
                        "evidence": ["nonexistent_artifact.json"]
                    }]
                }, f)
            ok2, msg2, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file, repo_root=td)
            assert ok2 is False, "Task with missing evidence file must block completion"
            assert "missing evidence file" in msg2

            # Case 3: Task RESOLVED but review_status is REJECTED
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump({
                    "active_task_id": None,
                    "tasks": [{
                        "task_id": "T3",
                        "status": "RESOLVED",
                        "review_status": "REJECTED",
                        "evidence": [real_evidence_file]
                    }]
                }, f)
            ok3, msg3, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file, repo_root=td)
            assert ok3 is False, "Task with review_status REJECTED must block completion"
            assert "rejected/unapproved review status" in msg3

            # Case 4: Fully valid task with existing evidence and accepted review status
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump({
                    "active_task_id": None,
                    "tasks": [{
                        "task_id": "T4",
                        "status": "RESOLVED",
                        "review_status": "ACCEPTED",
                        "evidence": [real_evidence_file]
                    }]
                }, f)
            ok4, msg4, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file, repo_root=td)
            assert ok4 is True, f"Valid task with real evidence must allow completion, got: {msg4}"


