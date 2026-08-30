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

    def test_cross_check_claim_register_succeeds(self):
        """Test that cross_check_claim_register verifies the repository claim register."""
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        from audit_claim_spec import cross_check_claim_register
        ok, errors, passed = cross_check_claim_register(repo_root)
        assert ok is True, f"Claim register cross-check failed: {errors}"
        assert len(passed) >= 2


