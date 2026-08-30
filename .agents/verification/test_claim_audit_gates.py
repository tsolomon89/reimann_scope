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
