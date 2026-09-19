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
        can_complete, msg, details = app.verify_research_milestone_completion(repo_root=REPO_ROOT)
        # Because TASK-TC-004 is active and Track 2 is active, milestone completion must be blocked!
        assert can_complete is False, "Production completion gate must reject completion when active research obligations remain"
        assert "Milestone completion blocked" in msg
        assert "TASK-TC-004" in msg or "active_task_id" in details or "active_tracks" in details

        # 2. Test isolated temporary queue configurations through production gate
        with tempfile.TemporaryDirectory() as td:
            q_file = os.path.join(td, "queue.json")
            s_file = os.path.join(td, "state.json")

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
            assert "unresolved in queue" in msg_b

            # Case C: Active research track in state
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump({"active_task_id": None, "tasks": [{"task_id": "TASK-RESOLVED", "status": "ACCEPTED"}]}, f)
            with open(s_file, "w", encoding="utf-8") as f:
                json.dump({"active_tracks": {"track_1": {"status": "ACTIVE"}}}, f)
            can_comp_c, msg_c, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file)
            assert can_comp_c is False
            assert "active research track(s) remain" in msg_c

            # Case D: Fully resolved queue and completed tracks
            with open(s_file, "w", encoding="utf-8") as f:
                json.dump({"active_tracks": {"track_1": {"status": "RESOLVED"}}}, f)
            can_comp_d, msg_d, _ = app.verify_research_milestone_completion(queue_path=q_file, state_path=s_file)
            assert can_comp_d is True
            assert "All persistent research obligations and tracks resolved" in msg_d
