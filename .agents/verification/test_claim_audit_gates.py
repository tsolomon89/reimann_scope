"""test_claim_audit_gates.py — Verification Suite for the Mathematical Claim Audit Capability.

Tests that the 10 mandatory pre-acceptance gates in `zeta-proof-audit` correctly accept
rigorous claims and reject flawed claims, specifically including:
1. Universal non-vanishing claims without equality-case analysis (historical bilateral cross-term failure).
2. Prime-only Dirichlet series labeled as completed zeta functions without a completion bridge theorem.
3. Finite-window Dirichlet series inner products asserting diagonal form without off-diagonal analysis.
4. Sampling-only numerical evidence asserting universal (\\forall) status.
"""

import sys
import os
import json
import hashlib
import pytest

# Ensure skills script is importable
SKILL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skills", "zeta-proof-audit", "scripts"))
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

from audit_claim_spec import audit_claim_specification


class TestClaimAuditGates:
    """Tests for the 10-gate mathematical claim audit system."""

    def test_rigorous_algebraic_identity_passes_all_gates(self):
        valid_spec = {
            "claim_id": "CLM-TEST-001",
            "statement": "\\forall F, \\Delta \\in \\mathbb{C}, Q(F, \\Delta) + Q(F, -\\Delta) = 2|\\Delta|^2",
            "quantified_variables": ["\\forall F \\in \\mathbb{C}", "\\forall \\Delta \\in \\mathbb{C}"],
            "variable_domains": {"F": "\\mathbb{C}", "\\Delta": "\\mathbb{C}"},
            "hypotheses": ["None (unconditional algebraic identity in \\mathbb{C})"],
            "object_studied": "Pointwise complex quadratic defect functional Q(F, \\Delta) = |F + \\Delta|^2 - |F|^2",
            "fourier_normalization": "N/A (pointwise algebraic)",
            "multiplicity_convention": "N/A",
            "measure_and_window": "Pointwise evaluation (no integration)",
            "order_of_limits": "N/A (finite algebra)",
            "exact_conclusion": "Q(F, \\Delta) + Q(F, -\\Delta) = 2|\\Delta|^2",
            "logical_negation": "\\exists F, \\Delta \\in \\mathbb{C} \\text{ s.t. } Q(F, \\Delta) + Q(F, -\\Delta) \\ne 2|\\Delta|^2",
            "epistemic_role": "ALGEBRAIC_IDENTITY",
            "dependencies": ["Complex norm squared algebraic expansion"],
            "proof_artifact": "formal/RiemannScope/CurvatureTransport.lean (bilateral_squared_norm_centering_exact_opposite)",
            "falsification_attempts": [
                "SymPy exact symbolic expansion over generic complex coordinates",
                "Tested extreme complex values F=10^6+10^6i, Delta=10^-6i",
                "Equality-case analysis: 2|Delta|^2 = 0 iff Delta = 0",
                "Boundary limits Delta -> 0 and Delta -> infty audited"
            ],
            "computational_evidence": ["pytest tests/test_bilateral_second_variation.py"],
            "external_sources": [{"source": "Standard algebra in C", "theorem": "Binomial expansion"}],
            "remaining_analytic_dependencies": []
        }

        res = audit_claim_specification(valid_spec)
        assert res["status"] == "PASS"
        assert len(res["violations"]) == 0
        assert len(res["passed_gates"]) >= 8

    def test_historical_false_cross_term_claim_is_rejected(self):
        """
        The previous sprint's false assertion that X_zeta != 0 for all a > 0, v >= 0
        must be strictly rejected by Gate 4 and Gate 6.
        """
        flawed_historical_spec = {
            "claim_id": "CLM-CT-022-FLAWED",
            "statement": "\\forall a > 0, \\forall v \\ge 0, \\mathfrak X_\\zeta(a, v) \\ne 0",
            "quantified_variables": ["\\forall a > 0", "\\forall v \\ge 0"],
            "variable_domains": {"a": "(0, \\infty)", "v": "[0, \\infty)"},
            "hypotheses": ["P(z) = \\sum_{n\\ge 2} \\Lambda(n) n^{-1/2-z}"],
            "object_studied": "Completed-zeta grade family inner product \\Re\\langle F_0, F_0''\\rangle_W",
            "fourier_normalization": "Standard L^2 Fourier transform",
            "multiplicity_convention": "Von Mangoldt weights \\Lambda(n)",
            "measure_and_window": "Finite smooth window W with variance v = \\langle t^2 \\rangle_W",
            "order_of_limits": "Derivative before infinite Dirichlet summation",
            "exact_conclusion": "\\mathfrak X_\\zeta \\ne 0 \\text{ for all } a > 0, v \\ge 0",
            "logical_negation": "\\exists a > 0, v \\ge 0 \\text{ s.t. } \\mathfrak X_\\zeta(a, v) = 0",
            "epistemic_role": "LOAD_BEARING_ANALYTIC_THEOREM",
            "dependencies": ["von Mangoldt Dirichlet series"],
            "proof_artifact": "None (relies on sampled numerical test points a=1, v=0; a=1, v=5)",
            "falsification_attempts": [
                "None (only sampled confirming test points)"
            ],
            "computational_evidence": ["pytest tests/test_bilateral_second_variation.py at 4 parameter points"],
            "external_sources": [],
            "remaining_analytic_dependencies": ["Convergence of second derivative under windowed inner product"]
        }

        res = audit_claim_specification(flawed_historical_spec)
        assert res["status"] == "FAIL"
        # Must fail Gate 1 (prime-only called completed-zeta), Gate 2 (universal without proof artifact),
        # Gate 4 (non-vanishing without equality-case analysis), Gate 6 (finite window without off-diagonal),
        # Gate 9 (no falsification attempts), and Gate 10 (load bearing with open dependencies)
        assert any("Gate 1" in v for v in res["violations"])
        assert any("Gate 2" in v for v in res["violations"])
        assert any("Gate 4" in v for v in res["violations"])
        assert any("Gate 6" in v for v in res["violations"])
        assert any("Gate 9" in v for v in res["violations"])
        assert any("Gate 10" in v for v in res["violations"])

    def test_prime_only_labeled_as_completed_zeta_rejected(self):
        spec = {
            "claim_id": "CLM-TEST-OBJ",
            "statement": "The completed zeta function \\xi(s) satisfies \\sum_{n\\le N} \\Lambda(n) n^{-s} = 0",
            "quantified_variables": ["s \\in \\mathbb{C}"],
            "variable_domains": {"s": "\\mathbb{C}"},
            "hypotheses": ["Finite Dirichlet polynomial"],
            "object_studied": "Prime-only Dirichlet polynomial P(z)",
            "fourier_normalization": "N/A",
            "multiplicity_convention": "N/A",
            "measure_and_window": "N/A",
            "order_of_limits": "N/A",
            "exact_conclusion": "\\xi(s) vanishes",
            "logical_negation": "\\xi(s) does not vanish",
            "epistemic_role": "ALGEBRAIC_IDENTITY",
            "dependencies": [],
            "proof_artifact": "math_core.py",
            "falsification_attempts": ["equality analysis"],
            "computational_evidence": [],
            "external_sources": [],
            "remaining_analytic_dependencies": []
        }
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 1" in v for v in res["violations"])

    def test_finite_window_without_offdiagonal_rejected(self):
        spec = {
            "claim_id": "CLM-TEST-OFFDIAG",
            "statement": "\\langle F_0, F_0''\\rangle_W = \\sum_n c_n \\bar d_n",
            "quantified_variables": ["W \\in C_c^\\infty"],
            "variable_domains": {"W": "C_c^\\infty"},
            "hypotheses": ["Dirichlet polynomial"],
            "object_studied": "Finite-window inner product of Dirichlet polynomial",
            "fourier_normalization": "Standard",
            "multiplicity_convention": "Standard",
            "measure_and_window": "Finite smooth window W \\in C_c^\\infty(\\mathbb R)",
            "order_of_limits": "Finite sum",
            "exact_conclusion": "Off-diagonal terms are zero",
            "logical_negation": "Off-diagonal terms are non-zero",
            "epistemic_role": "ALGEBRAIC_IDENTITY",
            "dependencies": [],
            "proof_artifact": "None",
            "falsification_attempts": ["Tested equality"],
            "computational_evidence": [],
            "external_sources": [],
            "remaining_analytic_dependencies": []
        }
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 6" in v for v in res["violations"])

    def test_real_repository_claim_clm_ct_022_passes(self):
        """Test that the actual repository claim specification CLM-CT-022.json passes all 10 gates."""
        claim_path = os.path.join(os.path.dirname(__file__), "..", "claims", "CLM-CT-022.json")
        assert os.path.exists(claim_path), f"Claim file {claim_path} must exist"
        with open(claim_path, "r", encoding="utf-8") as f:
            import json
            spec = json.load(f)
        res = audit_claim_specification(spec)
        assert res["status"] == "PASS", f"CLM-CT-022 failed: {res['violations']}"
        assert len(res["passed_gates"]) == 10

    def test_real_repository_claim_clm_ct_025_passes(self):
        """Test that the actual repository claim specification CLM-CT-025.json passes all 10 gates."""
        claim_path = os.path.join(os.path.dirname(__file__), "..", "claims", "CLM-CT-025.json")
        assert os.path.exists(claim_path), f"Claim file {claim_path} must exist"
        with open(claim_path, "r", encoding="utf-8") as f:
            import json
            spec = json.load(f)
        res = audit_claim_specification(spec)
        assert res["status"] == "PASS", f"CLM-CT-025 failed: {res['violations']}"
        assert len(res["passed_gates"]) == 10

    def test_clm_ct_026_spec_passes_audit(self):
        """Test that CLM-CT-026 specification passes all 10 gates."""
        from audit_claim_spec import audit_claim_specification
        spec_path = os.path.join(os.path.dirname(__file__), "..", "claims", "CLM-CT-026.json")
        with open(spec_path, "r", encoding="utf-8") as f:
            import json
            spec = json.load(f)
        res = audit_claim_specification(spec)
        assert res["status"] == "PASS", f"CLM-CT-026 failed: {res['violations']}"
        assert len(res["passed_gates"]) == 10

    def test_clm_ct_027_spec_passes_audit(self):
        """Test that CLM-CT-027 specification passes all 10 gates."""
        from audit_claim_spec import audit_claim_specification
        spec_path = os.path.join(os.path.dirname(__file__), "..", "claims", "CLM-CT-027.json")
        with open(spec_path, "r", encoding="utf-8") as f:
            import json
            spec = json.load(f)
        res = audit_claim_specification(spec)
        assert res["status"] == "PASS", f"CLM-CT-027 failed: {res['violations']}"
        assert len(res["passed_gates"]) == 10

    def test_clm_ct_028_spec_passes_audit(self):
        """Test that CLM-CT-028 specification passes all 10 gates."""
        from audit_claim_spec import audit_claim_specification
        spec_path = os.path.join(os.path.dirname(__file__), "..", "claims", "CLM-CT-028.json")
        with open(spec_path, "r", encoding="utf-8") as f:
            import json
            spec = json.load(f)
        res = audit_claim_specification(spec)
        assert res["status"] == "PASS", f"CLM-CT-028 failed: {res['violations']}"
        assert len(res["passed_gates"]) == 10

    def test_clm_ct_029_spec_passes_audit(self):
        """Test that CLM-CT-029 specification passes all 10 gates."""
        from audit_claim_spec import audit_claim_specification
        spec_path = os.path.join(os.path.dirname(__file__), "..", "claims", "CLM-CT-029.json")
        with open(spec_path, "r", encoding="utf-8") as f:
            import json
            spec = json.load(f)
        res = audit_claim_specification(spec)
        assert res["status"] == "PASS", f"CLM-CT-029 failed: {res['violations']}"
        assert len(res["passed_gates"]) == 10

    def test_cross_check_claim_register_succeeds(self):
        """Test that cross_check_claim_register verifies the repository claim register with exact arithmetic."""
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        from audit_claim_spec import cross_check_claim_register
        ok, errors, passed, coverage = cross_check_claim_register(repo_root)
        assert ok is True, f"Claim register cross-check failed: {errors}"
        assert coverage["total_claims"] == 92
        assert coverage["terminal_claims"] == 84
        assert coverage["audited_terminal_claims"] == 6
        assert coverage["legacy_unaudited_terminal_claims"] == 78
        assert coverage["open_or_exempt_claims"] == 8
        assert coverage["missing_specifications"] == 0
        assert coverage["unrecognized_statuses"] == 0
        # Strict coverage arithmetic
        assert coverage["terminal_claims"] == coverage["audited_terminal_claims"] + coverage["legacy_unaudited_terminal_claims"] + coverage["missing_specifications"]
        assert coverage["total_claims"] == coverage["terminal_claims"] + coverage["open_or_exempt_claims"]

    def test_new_terminal_claim_without_json_fails(self, tmp_path):
        """Test that a new terminal claim without JSON specification fails cross-check."""
        from audit_claim_spec import cross_check_claim_register
        mock_agents = tmp_path / ".agents"
        (mock_agents / "corpus_map").mkdir(parents=True)
        (mock_agents / "claims").mkdir(parents=True)
        (mock_agents / "corpus_map" / "legacy_claim_manifest.json").write_text('{"claims": {}}', encoding="utf-8")
        (mock_agents / "corpus_map" / "claim_register.md").write_text(
            "# Register\n| `CLM-NEW-001` | Statement | Layer | PROVED / EXACT | doc | target |\n",
            encoding="utf-8"
        )
        ok, errors, passed, coverage = cross_check_claim_register(str(tmp_path))
        assert ok is False
        assert coverage["missing_specifications"] == 1
        assert any("MISSING_SPECIFICATION_VIOLATION" in e for e in errors)

    def test_modified_legacy_terminal_claim_without_json_fails(self, tmp_path):
        """Test that a modified legacy terminal claim without JSON fails cross-check due to hash mismatch."""
        from audit_claim_spec import cross_check_claim_register
        mock_agents = tmp_path / ".agents"
        (mock_agents / "corpus_map").mkdir(parents=True)
        (mock_agents / "claims").mkdir(parents=True)
        (mock_agents / "corpus_map" / "legacy_claim_manifest.json").write_text(
            '{"claims": {"CLM-LEG-001": {"line_hash": "deadbeef1234", "status": "PROVED / EXACT"}}}',
            encoding="utf-8"
        )
        (mock_agents / "corpus_map" / "claim_register.md").write_text(
            "# Register\n| `CLM-LEG-001` | Modified statement | Layer | PROVED / EXACT | doc | target |\n",
            encoding="utf-8"
        )
        ok, errors, passed, coverage = cross_check_claim_register(str(tmp_path))
        assert ok is False
        assert coverage["missing_specifications"] == 1
        assert any("MODIFIED_LEGACY_CLAIM_VIOLATION" in e for e in errors)

    def test_unchanged_manifest_listed_legacy_claim_passes_provisionally(self, tmp_path):
        """Test that an unchanged legacy claim matching manifest passes provisionally as LEGACY_UNAUDITED."""
        from audit_claim_spec import cross_check_claim_register
        mock_agents = tmp_path / ".agents"
        (mock_agents / "corpus_map").mkdir(parents=True)
        (mock_agents / "claims").mkdir(parents=True)
        line = "| `CLM-LEG-001` | Original statement | Layer | PROVED / EXACT | doc | target |"
        line_hash = hashlib.sha256(line.encode("utf-8")).hexdigest()
        (mock_agents / "corpus_map" / "legacy_claim_manifest.json").write_text(
            json.dumps({
                "schema_version": "1.0.0",
                "baseline_commit": "82643cafd605492233c6c1e992b78c2c30d45f13",
                "claims": {"CLM-LEG-001": {"line_hash": line_hash, "status": "PROVED / EXACT"}}
            }),
            encoding="utf-8"
        )
        (mock_agents / "corpus_map" / "claim_register.md").write_text(
            f"# Register\n{line}\n",
            encoding="utf-8"
        )
        ok, errors, passed, coverage = cross_check_claim_register(str(tmp_path), verify_git_baseline=False)
        assert ok is True
        assert coverage["legacy_unaudited_terminal_claims"] == 1
        assert coverage["audited_terminal_claims"] == 0
        assert any("LEGACY_UNAUDITED" in p for p in passed)

    def test_unrecognized_custom_status_fails_cross_check(self, tmp_path):
        """Test that an unrecognized status in claim register is strictly rejected as a bypass attempt."""
        from audit_claim_spec import cross_check_claim_register
        mock_agents_dir = tmp_path / ".agents"
        mock_corpus = mock_agents_dir / "corpus_map"
        mock_corpus.mkdir(parents=True)
        mock_claims = mock_agents_dir / "claims"
        mock_claims.mkdir(parents=True)
        (mock_corpus / "legacy_claim_manifest.json").write_text('{"claims": {}}', encoding="utf-8")

        mock_reg = mock_corpus / "claim_register.md"
        mock_reg.write_text(
            "# Register\n| `CLM-FAKE-001` | Fake claim | Layer | CUSTOM_BYPASS_STATUS | doc | target |\n",
            encoding="utf-8"
        )

        ok, errors, passed, coverage = cross_check_claim_register(str(tmp_path))
        assert ok is False
        assert coverage["unrecognized_statuses"] == 1
        assert any("UNRECOGNIZED_STATUS_VIOLATION" in e for e in errors)

    def test_inconsistent_witness_rejected_by_gate9(self):
        """Test that an inconsistent witness value in a claim specification is rejected by Gate 9."""
        claim_path = os.path.join(os.path.dirname(__file__), "..", "claims", "CLM-CT-025.json")
        with open(claim_path, "r", encoding="utf-8") as f:
            import json
            spec = json.load(f)
        spec["statement"] = spec["statement"].replace("-0.0515509", "-0.054321")
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 9" in v for v in res["violations"])

    def test_tampered_manifest_with_non_baseline_claim_fails(self, tmp_path):
        """Test that injecting a non-baseline claim into legacy manifest fails baseline verification."""
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        from audit_claim_spec import cross_check_claim_register
        mock_agents = tmp_path / ".agents"
        (mock_agents / "corpus_map").mkdir(parents=True)
        (mock_agents / "claims").mkdir(parents=True)
        # Point to real repo's git root for git validation, but tampered manifest
        manifest = {
            "schema_version": "1.0.0",
            "baseline_commit": "82643cafd605492233c6c1e992b78c2c30d45f13",
            "claims": {
                "CLM-INJECTED-FAKE": {
                    "line_hash": "deadbeef",
                    "status": "PROVED / EXACT"
                }
            }
        }
        (mock_agents / "corpus_map" / "legacy_claim_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (mock_agents / "corpus_map" / "claim_register.md").write_text(
            "# Register\n| `CLM-INJECTED-FAKE` | Fake | Layer | PROVED / EXACT | doc | target |\n",
            encoding="utf-8"
        )
        ok, errors, passed, coverage = cross_check_claim_register(str(tmp_path), verify_git_baseline=False)
        assert ok is False
        # When git baseline verification runs on real repo:
        ok_real, errors_real, passed_real, cov_real = cross_check_claim_register(repo_root, verify_git_baseline=True)
        assert ok_real is True
        assert cov_real["legacy_unaudited_terminal_claims"] == 78
        assert cov_real["audited_terminal_claims"] == 6


class TestAdversarialAuditGates:
    """Mandatory adversarial test suite verifying fail-closed audit rejection of all 15 failure modes."""

    def _base_valid_spec(self):
        return {
            "claim_id": "CLM-ADV-TEST",
            "statement": "Tested mathematical property for fixed instance a = 1.5.",
            "quantified_variables": ["a = 1.5"],
            "variable_domains": ["a in Real, a = 1.5"],
            "hypotheses": ["P(s) = sum Lambda(n) n^{-s}"],
            "object_studied": "Fixed instance Dirichlet series evaluation",
            "fourier_normalization": "Centered coordinates z = a + it",
            "multiplicity_convention": "Standard arithmetic weights",
            "measure_and_window": "Canonical Gaussian window W(t)",
            "order_of_limits": "Derivative before summation",
            "exact_conclusion": "Tested property holds for fixed instance",
            "logical_negation": "Tested property fails for fixed instance",
            "epistemic_role": "FINITE_ANALYTIC_COMPONENT",
            "evidence_scope": "CERTIFIED_POINT_WITNESS",
            "exact_or_truncated": "EXACT",
            "arithmetic_cutoff": "NONE",
            "spectral_cutoff": "NONE",
            "integration_domain": "R",
            "omitted_tail": "NONE",
            "tail_enclosure": "NONE",
            "dependencies": ["Standard analysis"],
            "proof_artifact": "math_core.py",
            "falsification_attempts": [
                "Tested boundary asymptotic limits",
                "Equality-case root analysis performed"
            ],
            "computational_evidence": ["Arb certified interval [0.0239, 0.0240] excluding zero"],
            "external_sources": [{"source": "Edwards (1974)", "theorem": "Chapter 1"}],
            "remaining_analytic_dependencies": []
        }

    def test_adv_1_fake_arb_certificate_with_floats_rejected(self):
        """1. Fake Arb certificate made from floats is rejected by Gate 8."""
        spec = self._base_valid_spec()
        spec["computational_evidence"] = ["fake_arb: float(midpoint)=0.0239, float(radius)=1e-12"]
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 8" in v for v in res["violations"])

    def test_adv_2_finite_prime_truncation_labelled_exact_completed_xi_rejected(self):
        """2. Finite prime truncation labelled exact completed xi without certified tail is rejected by Gate 1."""
        spec = self._base_valid_spec()
        spec["statement"] = "Exact completed xi logarithmic derivative cross term evaluates to 0.0239."
        spec["exact_or_truncated"] = "TRUNCATED"
        spec["arithmetic_cutoff"] = "N=500"
        spec["tail_enclosure"] = "NONE"
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 1" in v for v in res["violations"])

    def test_adv_3_integral_over_compact_without_realline_tail_rejected(self):
        """3. Integral over [-T, T] without a real-line tail enclosure is rejected by Gate 1."""
        spec = self._base_valid_spec()
        spec["statement"] = "Real-line integral int_{R} W(t) f(t) dt evaluates to strictly positive interval."
        spec["integration_domain"] = "[-10.0, 10.0]"
        spec["omitted_tail"] = "NONE"
        spec["tail_enclosure"] = "NONE"
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 1" in v for v in res["violations"])

    def test_adv_4_nine_grid_positivity_promoted_to_universal_rejected(self):
        """4. Positivity at 9 grid points promoted to universal 'for all parameters' is rejected by Gate 2."""
        spec = self._base_valid_spec()
        spec["statement"] = "For all a >= 1.0 and for all sigma_W in [0.5, 2.0], cross term is strictly positive throughout."
        spec["quantified_variables"] = ["forall a in [1.0, 2.0]", "forall sigma_W in [0.5, 2.0]"]
        spec["evidence_scope"] = "FINITE_GRID_NUMERICAL"
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 2" in v for v in res["violations"])

    def test_adv_5_point_witness_promoted_to_no_root_exists_rejected(self):
        """5. Point witness promoted to 'no root exists on interval' is rejected by Gate 2."""
        spec = self._base_valid_spec()
        spec["statement"] = "No root exists across the parameter domain [1.0, 2.0] and cross term is always nonzero."
        spec["evidence_scope"] = "CERTIFIED_POINT_WITNESS"
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 2" in v for v in res["violations"])

    def test_adv_6_finite_lean_identity_promoted_to_infinite_analytic_theorem_rejected(self):
        """6. Finite Lean identity promoted to infinite analytic double sum theorem is rejected by Gate 10."""
        spec = self._base_valid_spec()
        spec["statement"] = "The infinite double sum converges to the continuous 1D quadrature on R."
        spec["evidence_scope"] = "FORMAL_LEAN_PROOF"
        spec["proof_artifact"] = "formal/RiemannScope/CurvatureTransport.lean (finset_double_sum_diag_offdiag_decomp)"
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 10" in v for v in res["violations"])

    def test_adv_7_decomposition_residual_used_as_numerical_error_rejected(self):
        """7. Decomposition residual (|I_direct - I_sum|) used as numerical quadrature error is rejected by Gate 8."""
        spec = self._base_valid_spec()
        spec["computational_evidence"] = ["residual_as_error: radius = abs(I_direct - I_sum)"]
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 8" in v for v in res["violations"])

    def test_adv_8_hardcoded_all_branches_eliminated_rejected(self):
        """8. Hardcoded evaluator all_branches_eliminated = True is rejected by Gate 9."""
        spec = self._base_valid_spec()
        spec["statement"] = "Entire bilateral route closed across all candidate branches."
        spec["epistemic_role"] = "NO_GO_COMPONENT"
        spec["evidence_scope"] = "NO_GO_FOR_DEFINED_CLASS"
        spec["computational_evidence"] = ["evaluate_bilateral_branch_elimination_summary: all_branches_eliminated = True"]
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 9" in v for v in res["violations"])

    def test_adv_9_hardcoded_distinct_viable_paths_count_rejected(self):
        """9. Hardcoded distinct_viable_paths_count = 1 without structural isomorphism map is rejected by Gate 9."""
        spec = self._base_valid_spec()
        spec["statement"] = "All 5 spectral routes are mutually isomorphic proof paths."
        spec["computational_evidence"] = ["distinct_viable_paths_count = 1"]
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 9" in v for v in res["violations"])

    def test_adv_10_shared_zero_sets_promoted_to_functional_isomorphism_rejected(self):
        """10. Shared zero sets promoted to functional isomorphism without explicit bijection is rejected by Gate 9."""
        spec = self._base_valid_spec()
        spec["statement"] = "Functional isomorphism between RDQ and Curvature Transport based on zero sets."
        spec["computational_evidence"] = ["distinct_viable_paths_count = 1"]
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 9" in v for v in res["violations"])

    def test_adv_11_no_falsification_attempts_rejected(self):
        """11. Mere presence of boilerplate review without falsification attempts is rejected by Gate 9."""
        spec = self._base_valid_spec()
        spec["falsification_attempts"] = []
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 9" in v for v in res["violations"])

    def test_adv_12_no_go_without_defined_exhaustive_class_rejected(self):
        """12. No-go claim without a defined exhaustive candidate class is rejected by Gate 10."""
        spec = self._base_valid_spec()
        spec["statement"] = "No bilateral grade construction of any form can succeed."
        spec["exact_conclusion"] = "Bilateral route closed."
        spec["epistemic_role"] = "NO_GO_COMPONENT"
        spec["evidence_scope"] = "NO_GO_FOR_DEFINED_CLASS"
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 10" in v for v in res["violations"])

    def test_adv_13_omitted_positive_terms_in_tail_bound_rejected(self):
        """13. Omitted positive terms in asserted integral tail bound is rejected by Gate 7."""
        spec = self._base_valid_spec()
        spec["hypotheses"] = ["tail bound: int_N^infty log(x)^2 x^{-sigma} dx"]
        spec["falsification_attempts"] = ["Audit noted omitted positive integration-by-parts terms in tail bound"]
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 7" in v for v in res["violations"])

    def test_adv_14_finite_algebra_promoted_to_infinite_convergence_rejected(self):
        """14. Finite exact algebra claiming infinite convergence is rejected by Gate 2."""
        spec = self._base_valid_spec()
        spec["statement"] = "Infinite double series convergence theorem."
        spec["evidence_scope"] = "FINITE_EXACT_ALGEBRA"
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 2" in v for v in res["violations"])

    def test_adv_15_universal_nonvanishing_without_equality_case_rejected(self):
        """15. Universal nonvanishing claim without equality-case analysis is rejected by Gate 4."""
        spec = self._base_valid_spec()
        spec["statement"] = "For all a >= 1.0, cross term is always nonzero (\\ne 0)."
        spec["evidence_scope"] = "EXTERNAL_ANALYTIC_PROOF"
        spec["falsification_attempts"] = ["Evaluated boundary limit as a -> infty"]  # No equality/root analysis
        res = audit_claim_specification(spec)
        assert res["status"] == "FAIL"
        assert any("Gate 4" in v for v in res["violations"])

    def test_adv_16_reproduced_previous_crossterm_false_certification_rejected(self):
        """16. Exact reproduction of previous false-certification structure in evaluate_completed_xi_grade_jet_crossterm is rejected."""
        reproduced_false_spec = {
            "claim_id": "CLM-CT-027-OLD-FALSE",
            "statement": "Under canonical Gaussian window W in S(R), X_{xi, W} is strictly positive and non-zero across all tested (a, sigma_W) in [1.0, 2.0] x [0.5, 2.0] and certified strictly positive in Arb ball arithmetic throughout.",
            "quantified_variables": [
                {"name": "a", "domain": "a in Real, a >= 1.0"},
                {"name": "sigma_w", "domain": "sigma_w in Real, 0.5 <= sigma_w <= 2.0"}
            ],
            "variable_domains": ["a in Real, a >= 1.0", "sigma_w in Real, 0.5 <= sigma_w <= 2.0"],
            "hypotheses": [
                "G(s) = -xi'/xi(s) = A(s) + P(s)",
                "P(s) truncated at max_n=500 without omitted tail bound",
                "integration on [-10, 10] without omitted Gaussian tail"
            ],
            "object_studied": "Completed Riemann xi-function second grade variation real cross-term X_{xi, W}",
            "fourier_normalization": "Centered coordinates z = a + it",
            "multiplicity_convention": "Standard arithmetic weights",
            "measure_and_window": "Canonical Gaussian window",
            "order_of_limits": "1D numerical quadrature on R with Arb interval error bounds",
            "exact_conclusion": "X_{xi, W} > 0 on entire test grid; exact cancellation does not occur",
            "logical_negation": "X_{xi, W} = 0 identically for canonical Gaussian window",
            "epistemic_role": "FINITE_ANALYTIC_COMPONENT",
            "evidence_scope": "FINITE_GRID_NUMERICAL",  # 9-point grid promoted to universal interval non-vanishing
            "exact_or_truncated": "TRUNCATED",
            "arithmetic_cutoff": "N=500",
            "spectral_cutoff": "NONE",
            "integration_domain": "[-10.0, 10.0]",
            "omitted_tail": "NONE",
            "tail_enclosure": "NONE",
            "dependencies": ["Completion bridge theorem"],
            "proof_artifact": "formal/RiemannScope/CurvatureTransport.lean",
            "falsification_attempts": ["Evaluated 4-block decomposition agreement to 50 dps"],
            "computational_evidence": ["residual_as_error: diff_direct_vs_sum < 1e-50"],
            "external_sources": [{"source": "Edwards (1974)", "theorem": "Chapter 1"}],
            "remaining_analytic_dependencies": []
        }

        res = audit_claim_specification(reproduced_false_spec)
        assert res["status"] == "FAIL"
        # Must fail Gate 1 (truncated without tail enclosure), Gate 2 (grid promoted to universal), Gate 8 (residual as error)
        assert any("Gate 1" in v for v in res["violations"])
        assert any("Gate 2" in v for v in res["violations"])
        assert any("Gate 8" in v for v in res["violations"])
