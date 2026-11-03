"""
TASK-TC-050: Construct the Faithful tau-Arithmetic Spectral Realization and Prove Adjoint Compatibility.

Investigates and formalizes the bridge from actual prime arithmetic and tau-normalized Fourier
duality (tau = 2*pi, concurrent real algebraic grades K in A_R := Qbar intersect R, positive and
negative) toward a faithful spectral realization excluding off-critical growth:

    Actual prime arithmetic + tau-normalized Fourier duality
      ===>  Faithful spectral realization / canonical Hilbert-Schmidt orbit decomposition
            with exact isolation of the resonant-band Moebius obligation.

Key Mathematical Results Implemented & Certified
------------------------------------------------
1. Joint Roles of tau = 2*pi, Distinct Prime Transformations, and Primary-Source Generator Identity:
   - Role I (Tate rational-diagonal character rigidity, Cassels-Frohlich Ch. XV):
     For fixed local p-adic additive characters psi_p(x_p) = exp(i * tau * {x_p}_p) with tau = 2*pi,
     the partial-fraction identity q = sum_p {q}_p + n(q) (n(q) in Z) on principal adeles q in Q subset A_Q
     gives prod_p psi_p(q) * psi_inf(q) = exp(i * (tau - c_inf) * q), uniquely forcing c_inf = tau = 2*pi
     so that psi_inf(x_inf) = exp(-i * tau * x_inf) is self-dual with unit covolume.
   - Role II (Opposite-grade Poisson lattice duality):
     Scaling Z -> tau^K Z scales the dual character lattice to tau^{-K} Z with invariant covolume product
     tau^K * tau^{-K} = 1.
   - Role III (Arithmetic vs. analytic prime transforms and semidirect intertwining):
     Distinguishes the arithmetic grade realization p * tau^K (multiplicative shift D_{p,K} f(x) =
     f(p^{-1} tau^{-K} x), log-translation log x -> log x - log p - K log tau) from the analytic
     prime-station power p^{tau^{-K}} in Z_tau(s, K) = zeta(tau^{-K} s) (power operator A_K f(x) =
     f(x^{tau^{-K}}), log-scaling u = log x -> tau^{-K} u), and proves the exact semidirect relation
         A_K D_J = D_{J * tau^{-K}} A_K
     together with Zeta-operator sampling Z(U_{-K} f)(1) = tau^{K/2} sum_{n>=1} f(n * tau^K).
   - Role IV (Exact identity with Connes-Consani-Moscovici arXiv:2511.22755 Lemma 7.1):
     Proves symbolically and in 256-bit Arb that our canonical pole-annihilated generator
         f_tau(x) = 2 * (tau^2 * x^4 - (3*tau/2) * x^2) * exp(-(tau/2) * x^2)
     equals 8 * h_CCM(x), where h_CCM(x) = (pi/2) * x^2 * (2*pi*x^2 - 3) * exp(-pi*x^2) =
     (sqrt(3)/2^{11/4}) h_4(x) - (3/2^{17/4}) h_0(x) is the Hermite combination of Riemann and
     Connes-Consani-Moscovici (2511.22755 Lemma 7.1), and x^{1/2} Z f_tau(x) = 8 k_CCM(x).

2. Adjoint Compatibility on the Grade Algebra, Hyperbolic Null-Cone Obstruction, and Multiplicity Socle:
   - On the commutative grade group algebra C[A_R] with V_K V_J = V_{K+J} and star-involution
     V_K^* = V_{-K} induced by the L^2(R_+^x, d^x x) operator adjoint U_K^* = U_{-K}:
       * Every spectral mode chi_rho(V_K) = tau^{K * (rho - 1/2)} (rho = 1/2 + delta + i*gamma)
         satisfies chi_rho(V_K V_J) = chi_rho(V_K) chi_rho(V_J) for ALL rho in C.
       * Star-compatibility chi_rho(V_K^*) = conj(chi_rho(V_K)) holds at any K != 0 if and only if
         tau^{-K * delta} = tau^{K * delta}, which (since tau = 2*pi > 1) holds iff delta = 0 (Re(rho) = 1/2).
       * Functional-equation symmetry rho <-> 1 - conj(rho) gives chi_{1-conj(rho)}(V_K) = conj(chi_rho(V_K^*)),
         forcing any V_K^* = V_{-K}-invariant Hermitian form on span{e_rho, e_{1-conj(rho)}} with delta != 0
         to have isotropic null diagonal G_{11} = G_{22} = 0 and indefinite hyperbolic signature (1, 1)
         with eigenvalues +/- |G_{12}|.
       * For a zero of arbitrary multiplicity m_rho = ord_xi(rho) >= 1, the generalized eigenspace
         E_rho = ker((^t D_- - rho)^{m_rho}) always contains a non-empty socle ker(^t D_- - rho) != {0}
         whose socle vector l_{rho,0} is a genuine eigenvector satisfying U_K l_{rho,0} = tau^{K(rho-1/2)} l_{rho,0}
         without assuming simplicity of zeros or diagonalizability of Jordan blocks.

3. Primary-Source Constructions Audit (Tate, Meyer, Connes-Consani, Connes-Consani-Moscovici):
   - Meyer (arXiv:math/0412277 Cor. 4.2 & Thm. 5.8):
     Verifies the nuclear Frechet quotient H_-^0 = H_- / Z H_cap, its exact spectrum {rho : xi(rho) = 0}
     with algebraic multiplicity ord_xi(rho), and proves why ambient L^2(1/2 + i R) completion fails
     to extend off-critical point evaluation h |-> hat{h}(rho) continuously whereas the convolution-trace
     pairing <[g], [h]>_W = -chi(rho_-)(g * h^*) preserves all zeros and satisfies
     (U_K g) * (U_K h)^* = g * h^* for all K in A_R.
   - Connes-Consani (arXiv:2006.13771 Appendix A, Thms. 1, 4.4, 6.11):
     Evaluates the exact Sine-Integral archimedean trace-remainder delta(rho) in 256-bit Arb on [1/2, 2],
     verifying delta(1) = Si(4*pi)/(2*pi) + 2 = 2.2374848349418275..., inversion symmetry delta(1/rho) = delta(rho),
     and derivative jump delta'(1^+) - delta'(1^-) = 2, and demonstrates how separated grades
     |K - L| > log(2)/log(tau) = 0.377146... move the relative scale tau^{|K-L|} outside (1/2, 2)
     to activate prime stations p >= 2.
   - Connes-Consani-Moscovici (arXiv:2511.22755 Thm. 1.1, Lemma 7.1, Section 8):
     Audits the finite-dimensional rank-one perturbed scaling operator D_{lambda, N}, regularized
     determinant det_reg(D_{lambda, N} - z) = -i lambda^{-i z} hat{xi}(z), and the two open steps
     in Section 8 (irrationally aligned multi-prime visual zeros and inductive step from N to N+1).

4. Canonical Hilbert-Schmidt Unitary Orbit Decomposition (Target 2):
   - Constructs on H_tau^pos := H_tau^B (+) L^2(R_{>0}, d^x y) (using the inherited TC-042F/TC-043 Attempt B
     one-sided shift-difference operator (A_tau^B f)(x, y) := ((I - S_x^{-1}) f)(y) = f(y) - f(y/x))
     the Hilbert-Schmidt operator B_0 := |Psi_0^pos><e_0| with Psi_0^pos = (A_tau^B psi_tau, 2 R_0 psi_tau)
     and left unitary orbit B_K := U_K B_0 (K in A_R), proving:
         P_tau(K) := <B_K, B_0>_{HS} = <A_tau^B T_K psi_tau, A_tau^B psi_tau>_{H_tau^B}
                                       + 4 <R_0 T_K psi_tau, R_0 psi_tau>_{L^2(d^x y)}
                  = W_arch(h_K) + (c_tau^B + 2) h_0(tau^{|K|}),
         |P_tau(K)| <= ||B_0||_{HS}^2 = P_tau(0) = 2.558258007415831... < 2.55826   for all K in A_R.
   - Establishes the exact decomposition across all K in A_R (positive and negative, rational and
     irrational algebraic) using the rigorously supported TC-049/TC-049R divisor cutoffs
     H(X) = floor(X^{5/6}) and M(X) = ceil(max(2, X^{5/4})):
         C_tau(K) = P_tau(K) + E_tau(K),
         E_tau(K) = E_{tau,controlled}(K) - R_{mu,band}(tau^{|K|}),
     where
         E_{tau,controlled}(K) = -(c_tau^B + 2) h_0(X_K) - W(X_K^{-1}) - W_log(X_K)
                                 - R_{mu,head}(X_K) - R_{mu,tail}(X_K)    (X_K = tau^{|K|} >= 1)
     retains all pole, transfer, small-scale prime, divisor-aggregated log-prime, head-divisor
     (2 <= m <= H(X_K) = floor(X_K^{5/6})), and super-scale tail-divisor (m > M(X_K) = ceil(max(2, X_K^{5/4})))
     contributions, and satisfies the unconditional uniform bound |E_{tau,controlled}(K)| <= B_ctrl < 17.987140
     for all K in A_R (with the first three terms decaying as O(X_K^{-5/2}) = O(tau^{-5|K|/2}) and the
     head and tail terms satisfying proved uniform O(1) bounds (5/6) C_{log,EM} and (1/2) C_{log,0}).
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
import sys
from typing import Any, Dict, List, Tuple

from flint import acb, acb_series, arb, ctx as flint_ctx
import sympy as sp

if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tc.canonical_theta_correlation_bound import (
    EPIC_TC_042_ID,
    REPO_ROOT,
    evaluate_archimedean_integral_certified_arb,
    evaluate_h0_acb,
    evaluate_h0_arb,
    evaluate_tilde_h0_arb,
    get_prime_powers_up_to,
    serialize_arb_certified,
    verify_all_serialized_arb_in_tree,
    verify_canonical_theta_correlation_lean_module,
)
from tc.prime_euler_moebius_recovery import (
    certified_coupled_cutoff_M_X_arb,
    certify_w_log_large_scale_decay_and_resonant_band_reduction_arb,
    moebius_mu_int,
    prime_factors_with_multiplicity,
    primes_up_to,
)

TASK_TC_050_ID = "TASK-TC-050"
TASK_TC_051_ID = "TASK-TC-051"
STARTING_HEAD_TC_050 = "e6472e03c008cc8d20be177f1d96bf904bd0a16b"
STARTING_HEAD_TC_051 = "d93ab512c2df75af2365a3963804c172baf0e867"
REVIEWED_BASELINE_TC_050 = "5da0eb79e1732ff871ee1c7fee729c62972aa406"
FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION_STATUS = (
    "ADJOINT_COMPATIBILITY_HYPERBOLIC_NULL_CONE_AND_CANONICAL_HILBERT_SCHMIDT_"
    "ORBIT_DECOMPOSITION_PROVED_RESONANT_BAND_EQUIVALENCE_ISOLATED_SUBGATE_OPEN"
)
DEFAULT_TC050_ARTIFACT_PATH = (
    REPO_ROOT / "data" / "tc_faithful_tau_arithmetic_spectral_realization.json"
)


# ---------------------------------------------------------------------------
# 1. Section 1: Joint Roles of tau = 2*pi, Distinct Prime Transformations,
#    Quotient Retention, and Connes-Consani-Moscovici Generator Identity
# ---------------------------------------------------------------------------


def p_adic_fractional_part_rational(q: Fraction, p: int) -> Fraction:
    """Return the exact p-adic principal fractional part {q}_p in Z[1/p] intersect [0, 1)
    such that q - {q}_p is p-integral (denominator coprime to p)."""
    num = q.numerator
    den = q.denominator
    p_pow = 1
    while den % p == 0:
        den //= p
        p_pow *= p
    if p_pow == 1:
        return Fraction(0, 1)
    inv_den = pow(den, -1, p_pow)
    a_mod = (num * inv_den) % p_pow
    return Fraction(a_mod, p_pow)


def verify_tau_joint_arithmetic_fourier_roles_and_transforms(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify the four coupled roles of tau = 2*pi, the semidirect intertwining between
    arithmetic shifts p * tau^K and analytic prime stations p^{tau^{-K}}, quotient data
    retention, and the exact identity f_tau(x) = 8 h_CCM(x) (arXiv:2511.22755 Lemma 7.1)."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        pi_arb = arb.pi()
        tau_arb = arb(2) * pi_arb

        # 1A. Tate rational-diagonal partial-fraction identity over Q subset A_Q:
        # For every q in Q, q - sum_p {q}_p in Z, so prod_p exp(i * tau * {q}_p) = exp(i * tau * q),
        # which cancels psi_inf(q) = exp(-i * c_inf * q) on Q iff c_inf = tau = 2*pi.
        sample_rationals = [
            Fraction(1, 6),
            Fraction(5, 12),
            Fraction(-7, 30),
            Fraction(19, 42),
            Fraction(113, 210),
        ]
        tate_diagonal_checks: List[Dict[str, Any]] = []
        all_tate_diagonal_pass = True
        for q in sample_rationals:
            den_factors = [p for p, _ in prime_factors_with_multiplicity(q.denominator)]
            local_parts = {p: p_adic_fractional_part_rational(q, p) for p in den_factors}
            sum_local = sum(local_parts.values(), Fraction(0, 1))
            diff_int = q - sum_local
            is_int = diff_int.denominator == 1
            # Verify all p-adic integrality conditions: for each p, q - {q}_p has denominator coprime to p
            p_integral_ok = all(
                ((q - part).denominator % p != 0) for p, part in local_parts.items()
            )
            # Adelic character product with c_inf = tau vs c_inf != tau
            phase_at_tau = acb(0, 1) * acb(tau_arb) * acb(arb(sum_local.numerator) / arb(sum_local.denominator) - arb(q.numerator) / arb(q.denominator))
            char_prod_at_tau = phase_at_tau.exp()
            encloses_one = bool(abs(char_prod_at_tau - acb(1)).contains(0))
            if not (is_int and p_integral_ok and encloses_one):
                all_tate_diagonal_pass = False
            tate_diagonal_checks.append(
                {
                    "q_rational": f"{q.numerator}/{q.denominator}",
                    "active_primes": den_factors,
                    "p_adic_fractional_parts": {
                        str(p): f"{pt.numerator}/{pt.denominator}"
                        for p, pt in local_parts.items()
                    },
                    "sum_local_parts": f"{sum_local.numerator}/{sum_local.denominator}",
                    "q_minus_sum_local_integer": int(diff_int),
                    "p_integrality_verified": p_integral_ok,
                    "adelic_character_product_encloses_1_at_c_inf_eq_tau": encloses_one,
                }
            )

        # 1B. Symbolic and 256-bit Arb distinction + semidirect intertwining between:
        #   - Arithmetic realization p * tau^K: log-translation u = log x |-> u - log p - K log tau
        #   - Analytic prime station p^{tau^{-K}}: log-scaling u = log x |-> tau^{-K} u
        u_sym, J_sym, K_sym, tau_sym = sp.symbols("u J K tau", positive=True)
        scale_sym = tau_sym ** (-K_sym)
        # Log-coordinate action of (A_K D_J f)(e^u) = f(e^{tau^{-K} u - J}) vs (D_{J * tau^{-K}} A_K f)(e^u):
        lhs_intertwining_sym = scale_sym * u_sym - J_sym
        rhs_intertwining_sym = scale_sym * (u_sym - J_sym * (tau_sym**K_sym))
        # Direct operator identity A_K D_J = D_{J * tau^{-K}} A_K in log coordinate:
        # Here D_J acts on the argument of f(e^w) by w |-> w - J, and A_K acts by w |-> tau^{-K} w:
        # (A_K (D_J f))(e^u) = (D_J f)(e^{tau^{-K} u}) = f(e^{tau^{-K} u - J}),
        # (D_{J * tau^K} (A_K f))(e^u) = (A_K f)(e^{u - J * tau^K}) = f(e^{tau^{-K}(u - J * tau^K)}) = f(e^{tau^{-K} u - J}).
        # And in the opposite direction:
        # (D_J (A_K f))(e^u) = (A_K f)(e^{u - J}) = f(e^{tau^{-K}(u - J)}) = f(e^{tau^{-K} u - J * tau^{-K}}) = (A_K D_{J * tau^{-K}} f)(e^u).
        intertwining_diff_1 = sp.simplify(
            (scale_sym * (u_sym - J_sym)) - (scale_sym * u_sym - J_sym * scale_sym)
        )
        intertwining_diff_2 = sp.simplify(lhs_intertwining_sym - rhs_intertwining_sym)
        commutator_log_arg = sp.simplify(
            (scale_sym * u_sym - J_sym) - (scale_sym * (u_sym - J_sym))
        )  # = -(1 - tau^{-K}) J != 0 for K != 0, J != 0

        # Numerical verification at p = 2, 3, 5 and K in {1, -1, 1/2, sqrt(2)}:
        station_comparison_rows: List[Dict[str, Any]] = []
        for p_val in (2, 3, 5):
            p_a = arb(p_val)
            for k_label, k_a in (
                ("1", arb(1)),
                ("-1", arb(-1)),
                ("1/2", arb(1) / arb(2)),
                ("sqrt(2)", arb(2).sqrt()),
            ):
                arith_station = p_a * (tau_arb**k_a)
                analytic_station = p_a ** (tau_arb ** (-k_a))
                diff_stations = arith_station - analytic_station
                strictly_distinct = bool(not diff_stations.contains(0))
                station_comparison_rows.append(
                    {
                        "prime_p": p_val,
                        "K_label": k_label,
                        "arithmetic_station_p_tau_K_certified": serialize_arb_certified(
                            arith_station
                        ),
                        "analytic_station_p_pow_tau_neg_K_certified": serialize_arb_certified(
                            analytic_station
                        ),
                        "difference_certified": serialize_arb_certified(diff_stations),
                        "certified_strictly_distinct": strictly_distinct,
                    }
                )

        # 1C. Exact symbolic and 256-bit Arb verification of the Connes-Consani-Moscovici
        # (arXiv:2511.22755 Lemma 7.1) generator identity:
        # Our canonical single-pole-annihilated generator (with r = (tau/2) x^2 = pi x^2):
        #   P(D) G_1(x) = (r^2 - (3/2) r) exp(-r) = (1/4) (tau^2 x^4 - 3 tau x^2) exp(-(tau/2) x^2) = h_CCM(x),
        #   f_tau(x)    = 8 P(D) G_1(x) = 2 (tau^2 x^4 - 3 tau x^2) exp(-(tau/2) x^2) = 8 h_CCM(x)   (tau = 2 * pi)
        # Connes-Consani-Moscovici Lemma 7.1:
        #   h_CCM(x) = (pi / 2) * x^2 * (2 * pi * x^2 - 3) * exp(-pi * x^2)
        #            = (sqrt(3) / 2^{11/4}) * h_4(x) - (3 / 2^{17/4}) * h_0(x),
        # where h_n(x) = (2^{1/4} / sqrt(2^n * n!)) * H_n(sqrt(2*pi)*x) * e^{-pi x^2}
        # with physicists' Hermite polynomials H_0(u) = 1, H_4(u) = 16 u^4 - 48 u^2 + 12.
        x_s, pi_s = sp.symbols("x pi", positive=True)
        tau_s = 2 * pi_s
        f_tau_sym = 2 * (tau_s**2 * x_s**4 - 3 * tau_s * x_s**2) * sp.exp(
            -tau_s * x_s**2 / 2
        )
        h_ccm_sym = (
            (pi_s / 2) * x_s**2 * (2 * pi_s * x_s**2 - 3) * sp.exp(-pi_s * x_s**2)
        )
        h0_hermite_sym = (sp.Integer(2) ** sp.Rational(1, 4)) * sp.exp(-pi_s * x_s**2)
        u_herm = sp.sqrt(2 * pi_s) * x_s
        H4_phys = 16 * u_herm**4 - 48 * u_herm**2 + 12
        h4_hermite_sym = (
            (sp.Integer(2) ** sp.Rational(1, 4))
            / sp.sqrt(sp.factorial(4) * (2**4))
            * H4_phys
            * sp.exp(-pi_s * x_s**2)
        )
        h_ccm_from_hermite_sym = (
            sp.sqrt(3) / (sp.Integer(2) ** sp.Rational(11, 4))
        ) * h4_hermite_sym - (
            sp.Integer(3) / (sp.Integer(2) ** sp.Rational(17, 4))
        ) * h0_hermite_sym
        diff_f_tau_8_h_ccm = sp.simplify(f_tau_sym - 8 * h_ccm_sym)
        diff_h_ccm_hermite = sp.simplify(h_ccm_sym - h_ccm_from_hermite_sym)

        # Also check the squared pole-regularized seed Phi_1^{(2)}(x) = P(D)^2 G_1(x):
        # In Hermite basis {h_0, h_2, h_4, h_6, h_8}, P(D)^2 = (D^2 - 1/16)^2 annihilates h_0
        # and maps r^4 - 7 r^3 + (41/4) r^2 - (9/4) r (r = pi x^2) onto span{h_0, h_2, h_4, h_6, h_8}.
        r_s = pi_s * x_s**2
        p2_seed_sym = (
            r_s**4 - 7 * r_s**3 + sp.Rational(41, 4) * r_s**2 - sp.Rational(9, 4) * r_s
        ) * sp.exp(-r_s)
        # Verify that f_tau(x) = 8 P(D) G_1(x) satisfies f_tau(0) = 0 and int_0^infty f_tau(x) dx = 0
        # (making its Mellin transform holomorphic at s = 0 and 0 at s = 1), while the squared
        # pole-regularized seed Phi_1^{(2)}(x) = P(D)^2 G_1(x) has vanishing Mellin transform at BOTH s = 0 and s = 1:
        f_tau_at_0 = f_tau_sym.subs(x_s, 0)
        mellin_f_tau_1 = sp.integrate(f_tau_sym, (x_s, 0, sp.oo))
        mellin_p2_0 = sp.integrate(p2_seed_sym / x_s, (x_s, 0, sp.oo))
        mellin_p2_1 = sp.integrate(p2_seed_sym, (x_s, 0, sp.oo))

        return {
            "tau_coupled_roles_classification": {
                "role_1_tate_adelic_character_normalization": {
                    "statement": (
                        "For local p-adic characters psi_p(x_p) = exp(i * tau * {x_p}_p) with tau = 2*pi, "
                        "the partial-fraction decomposition q = sum_p {q}_p + n(q) (n(q) in Z) on Q subset A_Q "
                        "uniquely forces the archimedean character psi_inf(x_inf) = exp(-i * tau * x_inf) "
                        "(c_inf = tau = 2*pi) so that prod_{v <= inf} psi_v(q) = 1 for all q in Q."
                    ),
                    "all_sample_rationals_verified": all_tate_diagonal_pass,
                    "sample_rational_verifications": tate_diagonal_checks,
                },
                "role_2_poisson_opposite_grade_lattice_duality": {
                    "statement": (
                        "Under f_hat(y) = int_R f(x) exp(-i * tau * x * y) dx, scaling the spatial lattice "
                        "Z -> tau^K Z scales the dual lattice to tau^{-K} Z with covolume product "
                        "tau^K * tau^{-K} = 1, supplying opposite-grade Poisson summation "
                        "sum_{n in Z} f(n * tau^K) = tau^{-K} sum_{m in Z} f_hat(m * tau^{-K})."
                    ),
                },
                "role_3_grade_base_and_algebraic_exponent_scope": {
                    "statement": (
                        "For K in A_R = Qbar intersect R, the grade action U_K f(x) = tau^{-K/2} f(tau^{-K} x) "
                        "places prime-power stations at n * tau^K (additive log-shifts log n + K log tau). "
                        "By Lindemann-Weierstrass + Gelfond-Schneider, tau = 2*pi is transcendental and hence "
                        "tau^q is transcendental for every nonzero rational q in Q \\ {0}; we do NOT assume "
                        "transcendence of tau^K for irrational algebraic K in A_R \\ Q (an open Schanuel-type "
                        "problem), whereas density of Q in A_R and R already suffices for the spectral/analytic "
                        "continuation steps."
                    ),
                },
                "role_4_canonical_theta_gaussian_exponent": {
                    "statement": (
                        "The self-dual Gaussian exp(-(tau/2) x^2) = exp(-pi x^2) has quadratic exponent "
                        "tau/2 = pi tied to the Fourier kernel exp(-i tau x y), so P(D) = D^2 - 1/16 "
                        "(D = t d/dt) simultaneously annihilates the s = 0 (origin) and s = 1 (integral) poles."
                    ),
                },
            },
            "arithmetic_vs_analytic_prime_transformations": {
                "arithmetic_grade_shift_p_tau_K": (
                    "D_{p,K} f(x) = f(p^{-1} tau^{-K} x), log-coordinate translation u |-> u - log p - K log tau"
                ),
                "analytic_prime_power_p_pow_tau_neg_K": (
                    "A_K f(x) = f(x^{tau^{-K}}), log-coordinate scaling u |-> tau^{-K} u in Z_tau(s, K) = zeta(tau^{-K} s)"
                ),
                "semidirect_intertwining_law": (
                    "D_J A_K = A_K D_{J * tau^{-K}}  and  A_K D_J = D_{J * tau^K} A_K  (in log-shift parameter J)"
                ),
                "zeta_operator_grade_sampling_identity": (
                    "Z(U_{-K} f)(1) = sum_{n>=1} (U_{-K} f)(n) = tau^{K/2} sum_{n>=1} f(n * tau^K) = tau^{K/2} (Z f)(tau^K)"
                ),
                "symbolic_intertwining_diff_1_zero": bool(intertwining_diff_1 == 0),
                "symbolic_intertwining_diff_2_zero": bool(intertwining_diff_2 == 0),
                "symbolic_noncommutativity_for_K_ne_0": str(commutator_log_arg),
                "certified_station_comparisons": station_comparison_rows,
            },
            "quotient_data_retention_classification": {
                "unquotiented_graded_monoid_M_Z": (
                    "Retains individual prime factors p, exponents k, and grade index K in (n, K) -> n * tau^K."
                ),
                "divisor_aggregated_profile_W_log": (
                    "Applies sum_{d|k} Lambda(d) = log k via harmonic aggregation sum_{m>=1} m^{-1/2} W(X/m), "
                    "cancelling all zeta-zero poles in |Re(z)| < 5/2 while retaining integer stations k >= 2; "
                    "exact Moebius inversion W(X) = sum_{m>=1} (mu(m)/sqrt(m)) W_log(X/m) recovers all prime-power "
                    "weights Lambda(n)."
                ),
                "meyer_cotangent_quotient_H_minus_0": (
                    "Quotients H_- by Z(H_+ intersect H_-), annihilating the trivial integer lattice sum "
                    "while retaining all nontrivial zeros rho of xi(s) with exact multiplicities ord_xi(rho) "
                    "and all local prime Weil distributions W_p in the character trace formula."
                ),
                "connes_consani_sonin_compression": (
                    "Compresses the theta map by the projection S onto Sonin's space (functions vanishing along "
                    " with their Fourier transform on (-2^{-1/2}, 2^{1/2})), retaining the archimedean + p=2 "
                    "semilocal trace on supp(g) subset [2^{-1/2}, 2^{1/2}] whileseparated grades |K - L| > "
                    "log(2)/log(tau) extend support across all primes p >= 2."
                ),
            },
            "connes_consani_moscovici_generator_identity": {
                "f_tau_definition": "f_tau(x) = 8 * P(D) G_1(x) = 2 * (tau^2 * x^4 - 3 * tau * x^2) * exp(-(tau/2) * x^2)",
                "h_CCM_definition_arXiv_2511_22755_Lemma_7_1": (
                    "h_CCM(x) = (pi/2) * x^2 * (2*pi*x^2 - 3) * exp(-pi*x^2) "
                    "= (sqrt(3) / 2^{11/4}) * h_4(x) - (3 / 2^{17/4}) * h_0(x)"
                ),
                "exact_ratio_identity": "f_tau(x) = 8 * h_CCM(x)  and  x^{1/2} * Z(f_tau)(x) = 8 * k_CCM(x)",
                "symbolic_f_tau_minus_8_h_CCM_zero": bool(diff_f_tau_8_h_ccm == 0),
                "symbolic_h_CCM_hermite_decomposition_verified": bool(
                    diff_h_ccm_hermite == 0
                ),
                "mellin_vanishing_at_s_0_and_1_verified": bool(
                    f_tau_at_0 == 0
                    and mellin_f_tau_1 == 0
                    and mellin_p2_0 == 0
                    and mellin_p2_1 == 0
                ),
            },
        }
    finally:
        flint_ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# 2. Section 2: Adjoint Compatibility on the Grade Algebra, Hyperbolic Pair
#    Null-Cone Obstruction, and Multiplicity Socle Eigenvectors
# ---------------------------------------------------------------------------


def verify_adjoint_compatibility_and_hyperbolic_pair_obstruction(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify star-involution compatibility chi_rho(V_K^*) = conj(chi_rho(V_K)) <-> Re(rho) = 1/2,
    the off-critical functional-equation hyperbolic pair signature (1, 1), and the Jordan socle
    eigenvector l_{rho,0} for arbitrary zero multiplicity m_rho >= 1."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        tau_arb = arb(2) * arb.pi()
        L_arb = tau_arb.log()

        # 2A. Symbolic verification of character multiplication vs star-compatibility:
        K_s, J_s, delta_s, gamma_s, L_s = sp.symbols(
            "K J delta gamma L", real=True
        )
        chi_K = sp.exp(K_s * L_s * (delta_s + sp.I * gamma_s))
        chi_J = sp.exp(J_s * L_s * (delta_s + sp.I * gamma_s))
        chi_K_plus_J = sp.exp((K_s + J_s) * L_s * (delta_s + sp.I * gamma_s))
        chi_neg_K = sp.exp(-K_s * L_s * (delta_s + sp.I * gamma_s))
        conj_chi_K = sp.conjugate(chi_K)
        chi_partner_K = sp.exp(
            K_s * L_s * (-delta_s + sp.I * gamma_s)
        )  # for 1 - conj(rho) = 1/2 - delta + i*gamma

        mult_law_ok = bool(sp.simplify(chi_K * chi_J - chi_K_plus_J) == 0)
        partner_exchange_ok = bool(
            sp.simplify(chi_partner_K - sp.conjugate(chi_neg_K)) == 0
        )
        star_ratio = sp.simplify(chi_neg_K / conj_chi_K)  # = exp(-2 * K * L * delta)
        star_ratio_expected = sp.exp(-2 * K_s * L_s * delta_s)
        star_ratio_ok = bool(sp.simplify(star_ratio - star_ratio_expected) == 0)

        # 2B. 256-bit Arb verification across critical-line (delta = 0) and off-critical
        # (delta in {1/10, 1/4, -1/5}) sample spectral modes and grades K in {1, -1, 1/2, sqrt(2)}:
        gamma_sample = arb("14.134725141734693790457251983562470270784257115699")
        mode_rows: List[Dict[str, Any]] = []
        for delta_label, delta_a in (
            ("0", arb(0)),
            ("1/10", arb(1) / arb(10)),
            ("1/4", arb(1) / arb(4)),
            ("-1/5", arb(-1) / arb(5)),
        ):
            for k_label, k_a in (
                ("1", arb(1)),
                ("-1", arb(-1)),
                ("1/2", arb(1) / arb(2)),
                ("sqrt(2)", arb(2).sqrt()),
            ):
                z_rho = acb(delta_a, gamma_sample)
                z_partner = acb(-delta_a, gamma_sample)
                chi_rho_VK = (acb(k_a * L_arb) * z_rho).exp()
                chi_rho_VK_star = (acb(-k_a * L_arb) * z_rho).exp()
                conj_chi_rho_VK = chi_rho_VK.conjugate()
                chi_partner_VK = (acb(k_a * L_arb) * z_partner).exp()

                star_defect = abs(chi_rho_VK_star - conj_chi_rho_VK)
                partner_match_defect = abs(
                    chi_partner_VK - chi_rho_VK_star.conjugate()
                )
                radial_factor_diag = (arb(2) * k_a * L_arb * delta_a).exp() - arb(1)
                mode_rows.append(
                    {
                        "delta_label": delta_label,
                        "K_label": k_label,
                        "abs_chi_rho_VK_certified": serialize_arb_certified(
                            abs(chi_rho_VK)
                        ),
                        "star_compatibility_defect_abs_certified": serialize_arb_certified(
                            star_defect
                        ),
                        "star_compatible_encloses_zero": bool(
                            star_defect.contains(0)
                        ),
                        "star_defect_strictly_positive_off_critical": bool(
                            star_defect.lower() > arb(0)
                        ),
                        "functional_equation_partner_exchange_encloses_zero": bool(
                            partner_match_defect.contains(0)
                        ),
                        "diagonal_pairing_factor_tau_2K_delta_minus_1_certified": serialize_arb_certified(
                            radial_factor_diag
                        ),
                    }
                )

        # 2C. Symbolic verification of Jordan block socle eigenvector l_{rho,0} for m_rho in {1, 2, 3}:
        lam_s, K_log_s = sp.symbols("lambda K_log")
        jordan_checks: List[Dict[str, Any]] = []
        for m_mult in (1, 2, 3):
            # Upper-triangular Jordan matrix J_m(lambda) = lambda I_m + N_m:
            # Under exp(K_log * J_m), the first basis vector e_0 = (1, 0, ..., 0)^T (the socle
            # l_{rho,0} in ker(^t D_- - rho)) satisfies exp(K_log * N_m) e_0 = e_0, so
            # U_K l_{rho,0} = lambda l_{rho,0} with ZERO nilpotent polynomial drift.
            N_mat = sp.Matrix(
                m_mult,
                m_mult,
                lambda i, j: 1 if j == i + 1 else 0,
            )
            exp_N = sp.eye(m_mult)
            for r_pow in range(1, m_mult):
                exp_N += (K_log_s**r_pow / sp.factorial(r_pow)) * (N_mat**r_pow)
            U_jordan = lam_s * exp_N
            e_socle = sp.Matrix(m_mult, 1, lambda i, _: 1 if i == 0 else 0)
            socle_image = U_jordan * e_socle
            socle_is_pure_eigenvector = bool(socle_image == lam_s * e_socle)
            # Contrast with top generalized vector e_{m-1}:
            e_top = sp.Matrix(m_mult, 1, lambda i, _: 1 if i == m_mult - 1 else 0)
            top_image = U_jordan * e_top
            jordan_checks.append(
                {
                    "multiplicity_m_rho": m_mult,
                    "socle_vector_is_pure_eigenvector": socle_is_pure_eigenvector,
                    "socle_image_components": [str(c) for c in socle_image],
                    "top_generalized_vector_image_components": [
                        str(c) for c in top_image
                    ],
                }
            )

        return {
            "star_algebra_definition": {
                "algebra": "C[A_R] generated by {V_K : K in A_R} with V_K V_J = V_{K+J}, V_0 = I, V_K^* = V_{-K}",
                "hilbert_realization": "(U_K f)(x) = tau^{-K/2} f(tau^{-K} x) on L^2(R_+^x, dx/x) satisfies U_K^* = U_{-K}",
                "distinction_from_coordinate_conjugation": (
                    "The star-involution V_K^* = V_{-K} is the Hilbert-space operator adjoint of unitary dilation "
                    "U_K on L^2(R_+^x, dx/x), NOT complex conjugation of the real coordinate n * tau^K (which is "
                    "already real and fixed by conjugation) and NOT unnormalized scaling f(tau^K x) (whose L^2 "
                    "adjoint is tau^{-K} f(tau^{-K} x))."
                ),
            },
            "character_compatibility_equivalence": {
                "multiplication_preserved_for_all_rho": mult_law_ok,
                "star_ratio_identity_verified": star_ratio_ok,
                "star_compatibility_criterion": (
                    "chi_rho(V_K^*) = conj(chi_rho(V_K))  <==>  tau^{-K * delta} = tau^{K * delta}  "
                    "<==>  delta = Re(rho) - 1/2 = 0  (for any K != 0, since tau = 2*pi > 1)."
                ),
                "functional_equation_partner_exchange_verified": partner_exchange_ok,
                "hyperbolic_null_cone_explanation": (
                    "Functional-equation symmetry rho <-> 1 - conj(rho) satisfies chi_{1-conj(rho)}(V_K) = "
                    "conj(chi_rho(V_K^*)). For delta != 0, any V_K^* = V_{-K}-invariant Hermitian form B(., .) "
                    "on span{e_rho, e_{1-conj(rho)}} satisfies B(e_rho, e_rho) = tau^{2 K delta} B(e_rho, e_rho) "
                    "and B(e_{1-conj(rho)}, e_{1-conj(rho)}) = tau^{-2 K delta} B(e_{1-conj(rho)}, e_{1-conj(rho)}), "
                    "forcing isotropic diagonal B_{11} = B_{22} = 0 and signature-(1, 1) hyperbolic quadratic form "
                    "2 Re(B_{12} conj(c_1) c_2) with eigenvalues +/- |B_{12}|."
                ),
                "certified_mode_evaluations": mode_rows,
            },
            "multiplicity_and_jordan_socle_audit": {
                "no_simplicity_assumption_required": True,
                "socle_theorem_statement": (
                    "By Meyer (arXiv:math/0412277 Cor. 4.2 & Thm. 5.8), each nontrivial zero rho of xi(s) with "
                    "multiplicity m_rho = ord_xi(rho) >= 1 contributes the finite-dimensional generalized eigenspace "
                    "E_rho = ker((^t D_- - rho)^{m_rho}) of dimension m_rho >= 1. Even if m_rho > 1 and ^t D_- has "
                    "a non-trivial nilpotent Jordan part N_rho on E_rho, the socle ker(^t D_- - rho) subset E_rho "
                    "has dimension >= 1, and any nonzero socle vector l_{rho,0} in ker(^t D_- - rho) \\ {0} is a "
                    "strict eigenvector satisfying U_K l_{rho,0} = tau^{K(rho - 1/2)} l_{rho,0}. Thus Target 1 "
                    "requires only a positive inner product on the socle (or a semisimple multiplicity-weighted "
                    "eigenspace) and never assumes simplicity of zeros."
                ),
                "scalar_correlation_vs_operator_jordan_scope_distinction": {
                    "scalar_correlation_boundedness_equivalence": (
                        "RH <==> sup_{K in A_R} |C_tau(K)| <= C_tau(0) <==> sup_{K in A_R} |C_tau(K)| < infty "
                        "holds unconditionally in zero multiplicity m_rho >= 1 in BOTH directions: "
                        "(i) Under RH (Re(rho) = 1/2), each distinct zero rho = 1/2 + i*gamma_rho of multiplicity "
                        "m_rho = ord_xi(rho) >= 1 satisfies Res_{s=rho}(xi'(s)/xi(s)) = m_rho and "
                        "Res_{s=rho}(-xi'(s)/xi(s)) = -m_rho, so in the explicit-formula contour shift "
                        "across s = rho (clockwise orientation), -Res_{s=rho}(-F_tau(s) F_tau(1-s) (xi'(s)/xi(s)) tau^{-K(s-1/2)}) "
                        "= +m_rho |F_tau(rho)|^2 tau^{-i K gamma_rho} (with no polynomial drift in K), "
                        "giving |C_tau(K)| <= sum_{rho distinct} m_rho |F_tau(rho)|^2 = C_tau(0) < infty; "
                        "(ii) Conversely, by the Fixed-Seed RH Equivalence Theorem (TASK-TC-037 / Theorem 12), "
                        "sup_{K in A_R} |C_tau(K)| < infty implies RH via Laplace-Carleman analytic continuation "
                        "without assuming zero simplicity."
                    ),
                    "socle_operator_unitary_realization_equivalence": (
                        "Realizing the socle eigenvectors l_{rho,0} in ker(^t D_- - rho) \\ {0} (or a semisimple "
                        "multiplicity-weighted eigenspace) in a positive-definite inner-product space with "
                        "V_K^* = V_{-K} is equivalent to Re(rho) = 1/2 for all zeros (RH alone, arbitrary m_rho >= 1)."
                    ),
                    "full_generalized_eigenspace_unitary_realization_equivalence": (
                        "On the algebraic direct sum of finite-dimensional generalized eigenspaces (+)_rho E_rho, "
                        "an abstract Hilbert-space unitary realization of {V_K}_{K in A_R} exists if and only if "
                        "RH + Simplicity (Re(rho) = 1/2 and m_rho = 1 for all zeros), because for m_rho >= 2 the "
                        "nilpotent Jordan chain V_K l_{rho,1} = tau^{K(rho-1/2)} (l_{rho,1} + (K log tau) l_{rho,0}) "
                        "has norm growing linearly in |K|. On Meyer's full topological cotangent quotient "
                        "H_-^0 = H_- / Z(H_+ cap H_-) (a nuclear Frechet space), any Hilbert-space unitary realization "
                        "that faithfully embeds the generalized eigenspaces E_rho implies RH + Simplicity "
                        "(a one-way necessary condition); conversely, an abstract diagonal Hilbert model on (+)_rho E_rho "
                        "does not by itself establish a topology-compatible positive Hilbert inner product on the "
                        "nuclear Frechet quotient H_-^0."
                    ),
                    "algebraic_direct_sum_vs_meyer_topological_quotient_unitary_realization_scope": (
                        "On the algebraic direct sum of finite-dimensional generalized eigenspaces (+)_rho E_rho, "
                        "an abstract Hilbert-space unitary realization of {V_K}_{K in A_R} exists if and only if "
                        "RH + Simplicity (Re(rho) = 1/2 and m_rho = 1 for all zeros). On Meyer's full topological "
                        "cotangent quotient H_-^0 = H_- / Z(H_+ cap H_-) (a nuclear Frechet space), any Hilbert-space "
                        "unitary realization that faithfully embeds E_rho implies RH + Simplicity (one-way necessary "
                        "condition), whereas an abstract diagonal model on (+)_rho E_rho does not by itself establish "
                        "a topology-compatible positive Hilbert inner product on H_-^0."
                    ),
                },
                "jordan_socle_verifications": jordan_checks,
            },
        }
    finally:
        flint_ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# 3. Section 3: Primary Literature Constructions Audit (Meyer, Connes-Consani,
#    Connes-Consani-Moscovici) and Separated-Grade Support Extension
# ---------------------------------------------------------------------------


def evaluate_connes_consani_sine_integral_arb(x_a: arb) -> arb:
    """Evaluate Sine Integral Si(x) = int_0^x (sin(t)/t) dt in 256-bit Arb via power series
    Si(x) = sum_{n>=0} (-1)^n x^{2n+1} / ((2n+1) * (2n+1)!) with alternating remainder."""
    s_acc = arb(0)
    x_sq = x_a * x_a
    term = x_a
    for n in range(0, 75):
        denom = arb(2 * n + 1)
        contrib = term / denom
        if n % 2 == 0:
            s_acc += contrib
        else:
            s_acc -= contrib
        # Next term factor: x^2 / ((2n+2)*(2n+3))
        term = term * x_sq / (arb(2 * n + 2) * arb(2 * n + 3))
    rem_bound = abs(term) / arb(151)
    return s_acc + arb(0, rem_bound.upper())


def evaluate_connes_consani_si_over_z_arb(z_a: arb) -> arb:
    """Evaluate entire function Si(z)/z = sum_{n>=0} (-1)^n z^{2n} / ((2n+1) * (2n+1)!)
    in 256-bit Arb with rigorous alternating-series remainder (equals 1 at z = 0)."""
    s_acc = arb(0)
    z_sq = z_a * z_a
    term = arb(1)
    for n in range(0, 75):
        denom = arb(2 * n + 1)
        contrib = term / denom
        if n % 2 == 0:
            s_acc += contrib
        else:
            s_acc -= contrib
        term = term * z_sq / (arb(2 * n + 2) * arb(2 * n + 3))
    rem_bound = abs(term) / arb(151)
    return s_acc + arb(0, rem_bound.upper())


def evaluate_connes_consani_delta_arb(rho_a: arb) -> arb:
    """Evaluate Connes-Consani's archimedean trace-remainder function delta(rho) on R_+^*
    from arXiv:2006.13771 Proposition 2.2 & eq. (2.18) (\\eqref{sch18}):
        For r = max(rho, 1/rho) >= 1:
            delta(rho) = 2 * r^{1/2} * ( Si(2*pi*(r + 1)) / (2*pi*(r + 1))
                                       + Si(2*pi*(r - 1)) / (2*pi*(r - 1)) ),
    where Si(z)/z = 1 at z = 0 (so delta(1) = Si(4*pi)/(2*pi) + 2 = 2.2374848349418275...)
    and delta(1/rho) = delta(rho) with derivative jump delta'(1^+) - delta'(1^-) = 1 - (-1) = 2.
    """
    pi_a = arb.pi()
    two_pi = arb(2) * pi_a
    r_ge_1 = rho_a if rho_a.lower() >= arb(1) else (arb(1) / rho_a)
    z_plus = two_pi * (r_ge_1 + arb(1))
    z_minus = two_pi * (r_ge_1 - arb(1))
    term_plus = evaluate_connes_consani_si_over_z_arb(z_plus)
    term_minus = evaluate_connes_consani_si_over_z_arb(z_minus)
    return arb(2) * r_ge_1.sqrt() * (term_plus + term_minus)


def verify_primary_literature_constructions_and_support_extension(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify the structural properties and numerical invariants of the primary constructions:
    - Meyer (arXiv:math/0412277): nuclear quotient H_-^0, ambient L^2 obstruction vs convolution-trace
      isometry (U_K g) * (U_K h)^* = g * h^*.
    - Connes-Consani (arXiv:2006.13771): Sine-Integral trace remainder delta(rho), inversion symmetry
      delta(1/rho) = delta(rho), derivative jump at rho = 1, and separated-grade support extension
      beyond [2^{-1/2}, 2^{1/2}] for |K - L| > log(2)/log(tau).
    - Connes-Consani-Moscovici (arXiv:2511.22755): Zeta Spectral Triples, regularized determinant,
      and the two open steps in Section 8."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        pi_arb = arb.pi()
        tau_arb = arb(2) * pi_arb
        L_arb = tau_arb.log()

        # 3A. Connes-Consani (arXiv:2006.13771 eq. 189 & Prop. 2.2) delta(rho) evaluation:
        delta_at_1 = evaluate_connes_consani_delta_arb(arb(1))
        cc_delta_rows: List[Dict[str, Any]] = []
        for rho_label, num, den in (
            ("1/2", 1, 2),
            ("2/3", 2, 3),
            ("3/4", 3, 4),
            ("1", 1, 1),
            ("4/3", 4, 3),
            ("3/2", 3, 2),
            ("2", 2, 1),
        ):
            r_a = arb(num) / arb(den)
            inv_r_a = arb(den) / arb(num)
            d_r = evaluate_connes_consani_delta_arb(r_a)
            d_inv = evaluate_connes_consani_delta_arb(inv_r_a)
            sym_diff = d_r - d_inv
            cc_delta_rows.append(
                {
                    "rho_label": rho_label,
                    "rho_float": float(r_a.mid()),
                    "delta_rho_certified": serialize_arb_certified(d_r),
                    "inversion_symmetry_diff_encloses_zero": bool(
                        sym_diff.contains(0)
                    ),
                }
            )

        # Separated-grade prime activation threshold:
        # Connes-Consani Theorem 1.1 restricts supp(g) subset [2^{-1/2}, 2^{1/2}] so supp(g * g^*) subset (1/2, 2).
        # Under grade shifts T_K, T_L, the relative scale is X_{K-L} = tau^{|K-L|}.
        # It exits (1/2, 2) as soon as tau^{|K-L|} >= 2, i.e., |K - L| >= log(2)/log(tau) = 0.3771461964...
        k_threshold_prime_2 = (arb(2).log()) / L_arb
        k_threshold_prime_3 = (arb(3).log()) / L_arb
        k_threshold_prime_5 = (arb(5).log()) / L_arb

        # 3B. Meyer (arXiv:math/0412277) ambient L^2 obstruction vs convolution-trace isometry:
        # On L^2(1/2 + i R), if we take normalized Gaussian packets hat{g}_n(1/2 + it) centered at t = 0
        # whose L^2 norm on Re(s) = 1/2 is 1 while analytic continuation to s = 1/2 + delta_0 (delta_0 != 0)
        # grows by exp(n * delta_0^2 / 2), point evaluation at an off-critical s_0 is unbounded in the
        # critical-line L^2 norm. By contrast, the multiplicative convolution (U_K g) * (U_K h)^* = g * h^*
        # is identically invariant under U_K for all K in A_R, so the Weil/Meyer trace functional
        # <[g], [h]>_W = -chi(rho_-)(g * h^*) = W_xi(g * h^*) is strictly U_K-invariant on H_-^0
        # while retaining every zero rho of xi(s) with multiplicity ord_xi(rho).
        conv_checks: List[Dict[str, Any]] = []
        for k_label, k_a in (
            ("1/2", arb(1) / arb(2)),
            ("1", arb(1)),
            ("-1", arb(-1)),
            ("sqrt(2)", arb(2).sqrt()),
        ):
            # Diagonal convolution invariance ((U_K psi_tau) * (U_K psi_tau)^*)(alpha) = h_0(alpha)
            # and shifted cross-grade convolution ((U_{K+J} psi_tau) * (U_J psi_tau)^*)(alpha) = h_0(tau^K alpha)
            for alpha_val in (1, 2, 5):
                al_a = arb(alpha_val)
                # Explicit change of variable y' = tau^{-K} y shows:
                # int_0^infty tau^{-K/2} psi_tau(tau^{-K} x / y) tau^{-K/2} psi_tau(tau^{-K} / y) dy/y
                # = int_0^infty psi_tau(x / y') psi_tau(1 / y') dy'/y' = h_0(x).
                h0_unshifted = evaluate_h0_arb(al_a)
                h0_shifted_diff = evaluate_h0_arb((tau_arb**k_a) * al_a)
                conv_checks.append(
                    {
                        "K_label": k_label,
                        "alpha": alpha_val,
                        "diagonal_convolution_h0_alpha_certified": serialize_arb_certified(
                            h0_unshifted
                        ),
                        "cross_grade_convolution_h0_tau_K_alpha_certified": serialize_arb_certified(
                            h0_shifted_diff
                        ),
                    }
                )

        return {
            "meyer_0412277_spectral_realization": {
                "quotient_space": "H_-^0 = H_- / Z(H_+ intersect H_-) (Meyer arXiv:math/0412277 Cor. 4.2)",
                "spectrum_and_multiplicities": (
                    "Spec(^t D_- | (H_-^0)') = {rho in C : xi(rho) = 0} with algebraic multiplicity "
                    "dim ker((^t D_- - rho)^N) = ord_xi(rho) >= 1."
                ),
                "trace_formula_theorem_5_8": (
                    "chi(rho)(f) = Tr(rho_-(f) | H_-^0) = sum_p W_p(f) + W_inf(f) = -W_xi(f) "
                    "for admissible test functions f (Meyer Theorem 5.8)."
                ),
                "ambient_L2_completion_obstruction": (
                    "Completing H_-^0 in the ambient critical-line Hilbert norm ||[h]||_{L^2(1/2+iR)} "
                    "(where ||[h]||^2 = (1/tau) int_{-infty}^infty |hat{h}(1/2+it)|^2 dt) makes U_K unitary, "
                    "but off-critical point evaluation [h] |-> hat{h}(1/2 + delta_0 + i*gamma_0) (delta_0 != 0) "
                    "is unbounded in ||.||_{L^2(1/2+iR)} and therefore does NOT extend to the ambient L^2 completion."
                ),
                "convolution_trace_pairing_preservation": (
                    "Equipping H_-^0 with the convolution-trace pairing <[g], [h]>_W := -chi(rho_-)(g * h^*) "
                    "= W_xi(g * h^*) preserves every nontrivial zero rho of xi(s) (with multiplicity ord_xi(rho)) "
                    "in the spectral expansion and makes U_K isometric because (U_K g) * (U_K h)^* = g * h^*."
                ),
                "certified_convolution_samples": conv_checks,
            },
            "connes_consani_2006_13771_compressed_scaling_trace": {
                "compressed_trace_identity_prop_2_2": (
                    "Tr(theta(g * g^*) P P_hat) = int_{1/2}^2 (g * g^*)(rho) delta(rho) d^* rho "
                    "for supp(g) subset [2^{-1/2}, 2^{1/2}] (arXiv:2006.13771 Prop. 2.2 & Appendix A)."
                ),
                "delta_at_1_formula": "delta(1) = Si(4*pi)/(2*pi) + 2 = 2.2374848349418275...",
                "delta_at_1_certified": serialize_arb_certified(delta_at_1),
                "delta_derivative_jump_at_1": "delta'(1^+) - delta'(1^-) = 2",
                "certified_delta_grid_on_half_to_two": cc_delta_rows,
                "separated_grade_support_extension": {
                    "threshold_K_for_prime_2_certified": serialize_arb_certified(
                        k_threshold_prime_2
                    ),
                    "threshold_K_for_prime_3_certified": serialize_arb_certified(
                        k_threshold_prime_3
                    ),
                    "threshold_K_for_prime_5_certified": serialize_arb_certified(
                        k_threshold_prime_5
                    ),
                    "explanation": (
                        "While a single compactly supported g in [2^{-1/2}, 2^{1/2}] has supp(g * g^*) subset (1/2, 2) "
                        "(reaching only the archimedean place and p = 2 at the boundary), separated grade shifts "
                        "h_{K-L} = (T_K psi_tau) * (T_L psi_tau)^* translate the center of mass to X_{K-L} = tau^{|K-L|}, "
                        "crossing p = 2 at |K - L| = log(2)/log(tau) = 0.377146..., p = 3 at 0.597864..., and "
                        "activating arbitrarily large primes p <= tau^{|K-L|} as |K - L| grows."
                    ),
                },
            },
            "connes_consani_moscovici_2511_22755_zeta_spectral_triples": {
                "operator_construction": (
                    "Compresses the scaling generator D_0 = -i x d/dx to the finite-dimensional wavelet/prolate "
                    "subspace QW_lambda(N) subset L^2([-lambda, lambda])_{ev} and applies the rank-one perturbation "
                    "k_CCM = E(h_CCM) = (1/8) x^{1/2} psi_tau to obtain D_{lambda, N} with regularized determinant "
                    "det_reg(D_{lambda, N} - z) = -i lambda^{-i z} hat{xi}_{lambda, N}(z) (Theorem 1.1 & Section 5)."
                ),
                "self_adjoint_vs_rank_one_perturbed_realization": (
                    "Before the rank-one perturbation, the compressed scaling operator is self-adjoint with real "
                    "spectrum (visual zeros on the real axis corresponding to Re(s) = 1/2). After the rank-one "
                    "perturbation enforcing exact vanishing at the first N zeros of xi, D_{lambda, N} is a "
                    "rank-one perturbation of a self-adjoint operator whose reality of spectrum is equivalent "
                    "to those zeros lying on the critical line."
                ),
                "section_8_two_missing_steps": [
                    (
                        "Step 1 (Irrational multi-prime alignment, arXiv:2511.22755 Section 8): Extend the "
                        "caricature model (where log p are commensurable rational multiples of a single period "
                        "so the Euler product collapses to a finite trigonometric polynomial with real zeros) to "
                        "the actual incommensurable logarithms {log p} of distinct primes."
                    ),
                    (
                        "Step 2 (Inductive N -> N + 1 zero-location step, arXiv:2511.22755 Section 8): Prove that "
                        "the high-accuracy real-axis visual zeros of the self-adjoint compression persist as "
                        "genuine critical-line zeros as the cutoff dimension N and scaling parameter lambda -> infty."
                    ),
                ],
            },
        }
    finally:
        flint_ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# 4. Section 4: Canonical Hilbert-Schmidt Unitary Orbit Decomposition
#    C_tau(K) = P_tau(K) + E_tau(K) (Target 2)
# ---------------------------------------------------------------------------


def certified_head_cutoff_H_X_arb(X: arb, prec_bits: int = 256) -> int:
    """Certify the integer head cutoff H(X) := floor(X^{5/6}) for X > 0 in Arb
    by verifying the exact integer sixth-power inequality H^6 <= X^5 < (H + 1)^6
    without deciding floors from float midpoints.

    Raises ValueError if X <= 0 or if X is an inexact interval straddling an
    integer sixth-power boundary k^6 (for X^5)."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        X_arb = arb(X)
        if (X_arb - arb(0)).lower() <= arb(0):
            raise ValueError(f"X must be certified strictly positive: {X_arb}")
        x5_arb = X_arb ** arb(5)
        # Integer binary search for H >= 0 with H^6 <= x5_arb.lower()
        lo = 0
        hi = 1
        while (x5_arb - arb(hi ** 6)).lower() >= arb(0):
            lo = hi
            hi *= 2
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if (x5_arb - arb(mid ** 6)).lower() >= arb(0):
                lo = mid
            else:
                hi = mid
        h_cand = lo
        lower_ok = (x5_arb - arb(h_cand ** 6)).lower() >= arb(0)
        upper_ok = (arb((h_cand + 1) ** 6) - x5_arb).lower() > arb(0)
        if lower_ok and upper_ok:
            return h_cand
        raise ValueError(
            f"Unable to certify unique integer floor(X^(5/6)) for X={X_arb} "
            f"(X^5={x5_arb} straddles {(h_cand + 1) ** 6})."
        )
    finally:
        flint_ctx.prec = saved_prec


def certify_clamped_exact_cutoff_M_X_arb(
    X: arb, prec_bits: int = 256
) -> Dict[str, Any]:
    """Certify the clamped integer super-scale cutoff M(X) := ceil(max(2, X^{5/4})) for X >= 1
    and distinguish the exact mathematical cutoff M(X) from the interval safe upper helper
    `certified_coupled_cutoff_M_X_arb(X)` (defined in `tc/prime_euler_moebius_recovery.py`).

    - Exact Clamped Characterization (for real X >= 1 and integer M):
          M = ceil(max(2, X^{5/4}))
            <==>  M >= 2  and  X^5 <= M^4  and  (M = 2  or  (M - 1)^4 < X^5).
      Note that the unclamped strict lower inequality (M - 1)^4 < X^5 fails at X = 1, M = 2
      because (2 - 1)^4 = 1 = 1^5.
    - Helper Scope (`certified_coupled_cutoff_M_X_arb(X)` in `tc/prime_euler_moebius_recovery.py`):
      Computes `M_safe(X_ball) = max(2, int(((X_ball^5)^{1/4}).upper().ceil()))` and verifies
      `X_ball^5 <= M_safe^4`. This returns a certified safe upper cutoff across the entire input
      ball `X_ball` (so `X^5 / M_safe^2 <= X^{-5/2} X^5 / M(X)^2 <= 1` holds on all of `X_ball`).
      Whenever `u_ball = (X_ball^5)^{1/4}` does not straddle an integer >= 2, `M_safe(X_ball)`
      additionally satisfies `(M_safe = 2 or (M_safe - 1)^4 < X_ball^5)` across the entire ball
      and therefore equals the exact mathematical ceiling `M(X)` on every point of `X_ball`.
      If `u_ball` straddles an integer boundary >= 2 (e.g., `X = 16 +/- 10^{-30}`, where
      `16^{5/4} = 32`), `M_safe = 33` exceeds the midpoint ceiling `M(16) = 32` by 1 and
      `exact_clamped_characterization_certified` is False.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        X_arb = arb(X)
        if (X_arb - arb(1)).lower() < arb(0):
            raise ValueError(f"X must satisfy X >= 1 for M(X) clamped characterization: {X_arb}")
        x5_arb = X_arb ** arb(5)
        u_arb = x5_arb.root(4)
        m_safe = certified_coupled_cutoff_M_X_arb(X_arb, prec_bits=prec_bits)
        ceil_lower = u_arb.lower().ceil()
        fmpz_lower = ceil_lower.unique_fmpz()
        if fmpz_lower is None:
            raise RuntimeError(
                f"Non-unique integer ceiling for lower endpoint of X^(5/4): {ceil_lower}"
            )
        m_lower_ceil = max(2, int(fmpz_lower))
        m_ge_2 = bool(m_safe >= 2)
        upper_ok = bool((arb(m_safe ** 4) - x5_arb).lower() >= arb(0))
        unclamped_lower_strict_ok = bool(
            (x5_arb - arb((m_safe - 1) ** 4)).lower() > arb(0)
        )
        clamped_lower_ok = bool((m_safe == 2) or unclamped_lower_strict_ok)
        exact_clamped_ok = bool(
            m_ge_2 and upper_ok and clamped_lower_ok and (m_lower_ceil == m_safe)
        )
        return {
            "M_safe_upper_int": m_safe,
            "M_lower_ceil_int": m_lower_ceil,
            "m_ge_2": m_ge_2,
            "X5_le_M4_certified": upper_ok,
            "clamped_lower_M_eq_2_or_M_minus_1_pow4_lt_X5_certified": clamped_lower_ok,
            "unclamped_M_minus_1_pow4_lt_X5_holds": unclamped_lower_strict_ok,
            "exact_clamped_characterization_certified": exact_clamped_ok,
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_h0_autocorrelation_cauchy_schwarz_and_sign_change_arb(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Certify in SymPy and 256-bit Arb the exact properties of the multiplicative
    autocorrelation profile h_0(X) := (psi_tau * psi_tau^*)(X) = <T_{log_tau X} psi_tau, psi_tau>_{L^2(dy/y)}:
      1. Single consistent value at X = 1 (W_1 = (1 + 1)^2 = 4):
             h_0(1) = P_sym(4) / (512 * 2^{17/2})
                    = 92193 / (512 * 2^{17/2})
                    = 92193 / (131072 * sqrt(2))
                    = 0.4973624838099012444846118490259731100371...
         where P_sym(W) = -648 W^3 + 58380 W^2 - 706860 W + 2027025
                        = 92193 - 270924 (W - 4) + 50604 (W - 4)^2 - 648 (W - 4)^3.
      2. Explicit sign-change witness on [1, infty):
         h_0(X) is NOT strictly positive or monotone decreasing on [1, infty); at X = 2
         (W_2 = 25/4 = 6.25), P_sym(25/4) = -177558.75 < 0 and
             h_0(2) = -0.21743062244679337... < 0.
      3. Valid unconditional global bound |h_0(X)| <= h_0(1) for all X > 0:
         Derived directly from the unitary dilation Cauchy-Schwarz inequality on L^2(R_{>0}, dy/y):
             |h_0(X)| = |<T_{log_tau X} psi_tau, psi_tau>_{L^2(dy/y)}|
                     <= ||T_{log_tau X} psi_tau||_{L^2(dy/y)} ||psi_tau||_{L^2(dy/y)}
                      = ||psi_tau||_{L^2(dy/y)}^2 = h_0(1),
         and independently from the symmetric Bernstein polynomial envelope (Lean Theorem 5)
             |h_0(X)| <= (92193 / 32768) (X + X^{-1})^{-5/2} <= (92193 / 32768) 2^{-5/2} = h_0(1).
         Consequently, |-(c_tau^B + 2) h_0(X_K)| = c_tau^A |h_0(X_K)| <= c_tau^A h_0(1) =: B_{h_0}.
      4. Leading large-X asymptotic (X -> infty):
         With W_X = (X + X^{-1})^2 ~ X^2, the numerator -648 W_X^3 + ... ~ -648 X^6 divided by
         512 (X + X^{-1})^{17/2} ~ 512 X^{17/2} gives
             h_0(X) ~ -(648 / 512) X^{6 - 17/2} = -(81 / 64) X^{-5/2} = O(X^{-5/2}).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        W_sym = sp.Symbol("W", real=True)
        P_sym_poly = (
            -648 * W_sym**3 + 58380 * W_sym**2 - 706860 * W_sym + 2027025
        )
        P_sym_taylor_at_4 = (
            92193
            - 270924 * (W_sym - 4)
            + 50604 * (W_sym - 4) ** 2
            - 648 * (W_sym - 4) ** 3
        )
        taylor_diff_zero = bool(
            sp.simplify(sp.expand(P_sym_poly - P_sym_taylor_at_4)) == 0
        )
        p_sym_at_4 = int(P_sym_poly.subs(W_sym, 4))
        p_sym_at_25_4 = sp.Rational(P_sym_poly.subs(W_sym, sp.Rational(25, 4)))

        h0_1_arb = evaluate_h0_arb(arb(1))
        h0_1_closed_arb = arb(92193) / (arb(131072) * arb(2).sqrt())
        h0_1_diff_encloses_zero = bool((h0_1_arb - h0_1_closed_arb).contains(0))

        h0_2_arb = evaluate_h0_arb(arb(2))
        h0_2_strictly_negative = bool(h0_2_arb.upper() < arb(0))
        h0_5_arb = evaluate_h0_arb(arb(5))
        h0_5_strictly_positive = bool(h0_5_arb.lower() > arb(0))
        h0_10_arb = evaluate_h0_arb(arb(10))
        h0_10_strictly_negative = bool(h0_10_arb.upper() < arb(0))

        # Verify |h_0(X)| <= (92193/32768) (X + X^{-1})^{-5/2} <= h_0(1) across test scales
        c0_bernstein = arb(92193) / arb(32768)
        leading_coeff_arb = -arb(81) / arb(64)
        sample_scales = [arb(1), arb(2), arb(5), arb(10), arb(100), arb(1000)]
        scale_checks: List[Dict[str, Any]] = []
        all_cs_and_bernstein_verified = True
        for x_s in sample_scales:
            h_val = evaluate_h0_arb(x_s)
            is_one = bool(x_s == arb(1))
            bern_env = (
                h0_1_arb
                if is_one
                else c0_bernstein * ((x_s + arb(1) / x_s) ** arb("-2.5"))
            )
            cs_cert = certify_abs_le_bound_arb(
                h_val, h0_1_arb, exact_self_equality=is_one
            )
            bern_cert = certify_abs_le_bound_arb(
                h_val, bern_env, exact_self_equality=is_one
            )
            scaled_x52 = (x_s ** arb("2.5")) * h_val
            if not (cs_cert["certified"] and bern_cert["certified"]):
                all_cs_and_bernstein_verified = False
            scale_checks.append(
                {
                    "X": str(float(x_s.mid())),
                    "h0_X_certified": serialize_arb_certified(h_val),
                    "X_pow_5_2_times_h0_X_certified": serialize_arb_certified(
                        scaled_x52
                    ),
                    "abs_h0_X_le_h0_1_certified": cs_cert["certified"],
                    "abs_h0_X_le_bernstein_envelope_certified": bern_cert[
                        "certified"
                    ],
                }
            )

        return {
            "h0_1_closed_form": "92193 / (512 * 2^{17/2}) = 92193 / (131072 * sqrt(2))",
            "P_sym_at_W_eq_4_exact_int": p_sym_at_4,
            "P_sym_taylor_at_W_eq_4": "92193 - 270924*(W - 4) + 50604*(W - 4)^2 - 648*(W - 4)^3",
            "P_sym_taylor_identity_verified": taylor_diff_zero,
            "h0_1_certified": serialize_arb_certified(h0_1_arb),
            "h0_1_closed_form_diff_encloses_zero": h0_1_diff_encloses_zero,
            "sign_change_witnesses_on_1_to_infty": {
                "h0_is_strictly_positive_on_1_to_infty": False,
                "h0_is_monotone_decreasing_on_1_to_infty": False,
                "P_sym_at_X_eq_2_W_eq_25_over_4_rational": f"{p_sym_at_25_4.p}/{p_sym_at_25_4.q}",
                "h0_2_certified": serialize_arb_certified(h0_2_arb),
                "h0_2_strictly_negative_verified": h0_2_strictly_negative,
                "h0_5_certified": serialize_arb_certified(h0_5_arb),
                "h0_5_strictly_positive_verified": h0_5_strictly_positive,
                "h0_10_certified": serialize_arb_certified(h0_10_arb),
                "h0_10_strictly_negative_verified": h0_10_strictly_negative,
            },
            "valid_global_bound_derivation": (
                "By the multiplicative autocorrelation identity h_0(tau^{|K|}) = <T_{|K|} psi_tau, psi_tau>_{L^2(dy/y)} "
                "and unitary dilation Cauchy-Schwarz on L^2(R_{>0}, dy/y), |h_0(X_K)| <= ||T_{|K|} psi_tau||_{L^2} ||psi_tau||_{L^2} "
                "= ||psi_tau||_{L^2}^2 = h_0(1) for all K in R (and independently by the symmetric Bernstein bound "
                "|h_0(X)| <= (92193/32768) (X + X^{-1})^{-5/2} <= h_0(1), Lean Theorem 5)."
            ),
            "leading_large_X_asymptotic": {
                "formula": "h_0(X) = -(81/64) X^{-5/2} (1 + O(X^{-2})) = O(X^{-5/2}) as X -> infty",
                "leading_coefficient_exact": "-648 / 512 = -81 / 64 = -1.265625",
                "leading_coefficient_certified": serialize_arb_certified(
                    leading_coeff_arb
                ),
                "global_bernstein_decay_constant": "92193 / 32768 = 2.813507080078125",
            },
            "all_cauchy_schwarz_and_bernstein_checks_verified": all_cs_and_bernstein_verified,
            "sample_scale_evaluations": scale_checks,
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_euler_resolvent_R0_spatial_and_mellin_identity_arb(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Certify in SymPy and 256-bit Arb the reconciled causal s = 0 Euler resolvent R_0
    and pole-integral J(kappa) definitions:
      1. Spatial and integration-by-parts definitions (with Euler derivative D = y d/dy):
             (R_0 f)(y) := int_0^y (t/y)^{1/2} (D f)(t) dt/t
                         = f(y) - (1/2) int_0^y (t/y)^{1/2} f(t) dt/t
                         = ((I - (1/2) K_0) f)(y),
         where (K_0 f)(y) := y^{-1/2} int_0^y f(t) t^{1/2} dt/t is the derivative-free causal operator.
      2. Mellin / Fourier multiplier on L^2(R_{>0}, dy/y) (hat{f}(it) = int_0^infty f(y) y^{-it} dy/y):
             hat{K_0 f}(it) = (1 / (1/2 + it)) hat{f}(it),
             hat{R_0 f}(it) = (1 - (1/2) / (1/2 + it)) hat{f}(it) = (it / (1/2 + it)) hat{f}(it),
             |hat{R_0 f}(it)|^2 = (t^2 / (t^2 + 1/4)) |hat{f}(it)|^2 = (1 - (1/4) / (t^2 + 1/4)) |hat{f}(it)|^2.
      3. Exact inner-product identity with exponential weight e^{-u/2} in J(kappa):
             J(kappa) := int_0^infty e^{-u/2} (h_0(e^{kappa+u}) + h_0(e^{kappa-u})) du
                       = <K_0 T_K psi_tau, K_0 psi_tau>_{L^2(dy/y)},
             4 <R_0 T_K psi_tau, R_0 psi_tau>_{L^2(dy/y)} = 4 h_0(e^kappa) - J(kappa).
         By contrast, omitting the Euler derivative D (replacing R_0 by K_0) gives
         4 ||K_0 psi_tau||_{L^2(dy/y)}^2 = 4 J(0) = 0.103839045137624105450954... != 4 h_0(1) - J(0) = 1.963490173955198951575709...
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        tol_spec = 2 ** (-90)
        pi_arb = arb.pi()
        c0_bernstein = arb(92193) / arb(32768)

        # Symbolic Mellin multiplier identity: 1 - (1/2)/(1/2 + i*t) == (i*t)/(1/2 + i*t)
        # and |(i*t)/(1/2 + i*t)|^2 == t^2 / (t^2 + 1/4) == 1 - (1/4)/(t^2 + 1/4)
        t_sym = sp.Symbol("t", real=True)
        mult_diff = sp.simplify(
            (1 - sp.Rational(1, 2) / (sp.Rational(1, 2) + sp.I * t_sym))
            - (sp.I * t_sym) / (sp.Rational(1, 2) + sp.I * t_sym)
        )
        mod_sq_diff = sp.simplify(
            (t_sym**2 / (t_sym**2 + sp.Rational(1, 4)))
            - (1 - sp.Rational(1, 4) / (t_sym**2 + sp.Rational(1, 4)))
        )
        symbolic_mellin_multiplier_verified = bool(
            mult_diff == 0 and mod_sq_diff == 0
        )

        # Spatial verification of (R_0 psi_tau)(y) = int_0^y (t/y)^{1/2} (D psi_tau)(t) dt/t
        # vs psi_tau(y) - (1/2) y^{-1/2} int_0^y t^{1/2} psi_tau(t) dt/t at y in {1/2, 1, 2}.
        # Since psi_tau(t) = t^{1/2} Phi_1^{(2)}(t) with Phi_1^{(2)}(t) = P_2(r) e^{-r}, r = pi t^2,
        # we have t^{1/2} psi_tau(t) dt/t = Phi_1^{(2)}(t) dt and
        # t^{1/2} (D psi_tau)(t) dt/t = ((1/2) Phi_1^{(2)}(t) + (D Phi_1^{(2)})(t)) dt,
        # both of which are entire functions of t on [0, y]:
        def _phi2_acb(t_c: acb) -> acb:
            r_c = acb(pi_arb) * t_c * t_c
            poly = (
                r_c**4
                - acb(7) * (r_c**3)
                + (acb(41) / acb(4)) * (r_c**2)
                - (acb(9) / acb(4)) * r_c
            )
            return poly * ((-r_c).exp())

        def _t_sqrt_D_psi_tau_over_t_acb(t_c: acb) -> acb:
            # t^{-1/2} (D psi_tau)(t) = (1/2) Phi_1^{(2)}(t) + 2 r d/dr(P_2(r) e^{-r}):
            r_c = acb(pi_arb) * t_c * t_c
            d_poly = (
                -r_c**4
                + acb(11) * (r_c**3)
                - (acb(125) / acb(4)) * (r_c**2)
                + (acb(91) / acb(4)) * r_c
                - (acb(9) / acb(4))
            ) * r_c
            return (acb(1) / acb(2)) * _phi2_acb(t_c) + acb(2) * d_poly * (
                (-r_c).exp()
            )

        spatial_ibp_checks: List[Dict[str, Any]] = []
        all_spatial_ibp_enclose_zero = True
        for y_val in [arb("0.5"), arb(1), arb(2)]:
            sqrt_y = y_val.sqrt()

            def _int_D_t(t_c: acb, analytic: bool = False) -> acb:
                return _t_sqrt_D_psi_tau_over_t_acb(t_c)

            def _int_psi_t(t_c: acb, analytic: bool = False) -> acb:
                return _phi2_acb(t_c)

            r0_from_D = (
                acb.integral(
                    _int_D_t,
                    acb(0),
                    acb(y_val.mid()),
                    rel_tol=tol_spec,
                    abs_tol=tol_spec,
                ).real
                / sqrt_y
            )
            k0_val = (
                acb.integral(
                    _int_psi_t,
                    acb(0),
                    acb(y_val.mid()),
                    rel_tol=tol_spec,
                    abs_tol=tol_spec,
                ).real
                / sqrt_y
            )
            psi_y = sqrt_y * _phi2_acb(acb(y_val)).real
            r0_from_ibp = psi_y - arb("0.5") * k0_val
            diff_r0 = r0_from_D - r0_from_ibp
            encloses_zero = bool(diff_r0.contains(0))
            if not encloses_zero:
                all_spatial_ibp_enclose_zero = False
            spatial_ibp_checks.append(
                {
                    "y": str(float(y_val.mid())),
                    "R0_psi_tau_from_Euler_derivative_D_certified": serialize_arb_certified(
                        r0_from_D
                    ),
                    "R0_psi_tau_from_IBP_f_minus_half_K0_f_certified": serialize_arb_certified(
                        r0_from_ibp
                    ),
                    "derivative_free_K0_psi_tau_certified": serialize_arb_certified(
                        k0_val
                    ),
                    "R0_D_minus_R0_IBP_diff_certified": serialize_arb_certified(
                        diff_r0
                    ),
                    "R0_D_minus_R0_IBP_encloses_zero": encloses_zero,
                }
            )

        # Evaluate J(0) = 2 int_0^infty e^{-u/2} h_0(e^u) du and compare
        # 4 ||R_0 psi_tau||^2 = 4 h_0(1) - J(0) against 4 ||K_0 psi_tau||^2 = 4 J(0):
        def _f_j0(u_c: acb, analytic: bool = False) -> acb:
            return (
                acb(2)
                * evaluate_h0_acb(u_c.exp(), analytic=analytic)
                * ((-u_c / acb(2)).exp())
            )

        u_top_J0 = 20
        j0_fin = arb(0)
        for m_step in range(0, 4 * u_top_J0):
            j0_fin += acb.integral(
                _f_j0,
                acb(m_step) / acb(4),
                acb(m_step + 1) / acb(4),
                rel_tol=tol_spec,
                abs_tol=tol_spec,
            ).real
        j0_tail = (
            (arb(2) / arb(3))
            * c0_bernstein
            * ((-arb(3) * arb(u_top_J0)).exp())
        )
        j0_arb = j0_fin + arb(0, j0_tail.upper())
        h0_1_arb = evaluate_h0_arb(arb(1))
        four_r0_norm_sq = arb(4) * h0_1_arb - j0_arb
        four_k0_norm_sq = arb(4) * j0_arb
        discrepancy_r0_vs_k0 = four_r0_norm_sq - four_k0_norm_sq

        return {
            "euler_resolvent_R0_spatial_formula": (
                "(R_0 f)(y) := int_0^y (t/y)^{1/2} (D f)(t) dt/t = f(y) - (1/2) int_0^y (t/y)^{1/2} f(t) dt/t,   D = y d/dy"
            ),
            "derivative_free_operator_K0_formula": (
                "(K_0 f)(y) := y^{-1/2} int_0^y f(t) t^{1/2} dt/t,   so R_0 = K_0 D = I - (1/2) K_0"
            ),
            "mellin_multiplier_of_R0": "hat{R_0 f}(it) = (it / (1/2 + it)) hat{f}(it),   |hat{R_0 f}(it)|^2 = (1 - (1/4)/(t^2 + 1/4)) |hat{f}(it)|^2",
            "pole_integral_J_kappa_definition": (
                "J(kappa) := int_0^infty e^{-u/2} (h_0(e^{kappa+u}) + h_0(e^{kappa-u})) du "
                "= int_1^infty x^{-1/2} (h_0(e^kappa x) + h_0(e^kappa x^{-1})) dx/x"
            ),
            "attempt_B_weight_vs_J_kappa_weight_distinction": (
                "In J(kappa), the exponential weight is e^{-u/2} du = x^{-1/2} dx/x (arising from the "
                "L^2(R_{>0}, dy/y) convolution of the s = 0 pole kernel k_0(y) = y^{-1/2} 1_{y>1}). "
                "By contrast, the weight (e^{-3u/2} / (2 sinh u)) du = (x^{-3/2} / (x - x^{-1})) dx/x "
                "belongs to the Attempt B conductor space H_tau^B difference-square integral "
                "P_tau^B(K) = int_0^infty (e^{-3u/2} / (2 sinh u)) (2 h_0(e^kappa) - h_0(e^{kappa+u}) - h_0(e^{kappa-u})) du."
            ),
            "symbolic_mellin_multiplier_verified": symbolic_mellin_multiplier_verified,
            "all_spatial_ibp_enclose_zero": all_spatial_ibp_enclose_zero,
            "spatial_ibp_sample_checks": spatial_ibp_checks,
            "J_0_certified": serialize_arb_certified(j0_arb),
            "four_norm_R0_psi_tau_sq_eq_4_h0_1_minus_J_0_certified": serialize_arb_certified(
                four_r0_norm_sq
            ),
            "four_norm_derivative_free_K0_psi_tau_sq_eq_4_J_0_certified": serialize_arb_certified(
                four_k0_norm_sq
            ),
            "discrepancy_four_R0_sq_minus_four_K0_sq_certified": serialize_arb_certified(
                discrepancy_r0_vs_k0
            ),
        }
    finally:
        flint_ctx.prec = saved_prec



def certify_abs_le_bound_arb(
    value_arb: arb,
    bound_arb: arb,
    *,
    exact_self_equality: bool = False,
) -> Dict[str, Any]:
    """Certify the inequality |value| <= bound in Arb using outward-rounded endpoints.

    - Standard mode (`exact_self_equality=False`):
      Requires `(bound_arb - abs(value_arb)).lower() >= arb(0)` (equivalently
      `abs(value_arb).upper() <= bound_arb.lower()`). Mere interval overlap
      (`abs(value_arb).lower() <= bound_arb.upper()`) is explicitly rejected.
    - Self-equality mode (`exact_self_equality=True`):
      Used only when `value_arb` and `bound_arb` are the identical positive quantity
      (e.g., |P_tau(0)| <= P_tau(0) at K = 0 where P_tau(0) > 0 is a single ball of
      nonzero radius so interval subtraction B - |B| would double the radius).
      Requires `value_arb.lower() > arb(0)` and `value_arb == bound_arb`.
    """
    abs_val = abs(value_arb)
    margin = bound_arb - abs_val
    outward_ok = bool(margin.lower() >= arb(0))
    weak_overlap = bool(abs_val.lower() <= bound_arb.upper())
    if exact_self_equality:
        pos_self_ok = bool(
            (abs_val.lower() > arb(0))
            and (bound_arb.lower() > arb(0))
            and (abs_val.mid() == bound_arb.mid())
            and (abs_val.rad() == bound_arb.rad())
        )
        return {
            "certified": pos_self_ok,
            "certification_mode": "EXACT_ALGEBRAIC_SELF_EQUALITY_POSITIVE_BALL",
            "outward_upper_le_lower": outward_ok,
            "weak_overlap_lower_le_upper": weak_overlap,
            "abs_value_upper_str": str(abs_val.upper()),
            "bound_lower_str": str(bound_arb.lower()),
            "margin_bound_minus_abs_certified": serialize_arb_certified(
                arb(0) if pos_self_ok else margin
            ),
        }
    return {
        "certified": outward_ok,
        "certification_mode": "OUTWARD_UPPER_LE_LOWER",
        "outward_upper_le_lower": outward_ok,
        "weak_overlap_lower_le_upper": weak_overlap,
        "abs_value_upper_str": str(abs_val.upper()),
        "bound_lower_str": str(bound_arb.lower()),
        "margin_bound_minus_abs_certified": serialize_arb_certified(margin),
    }


def _compute_live_B_log_global_bound_arb(prec_bits: int = 256) -> Dict[str, Any]:
    """Compute the TC-044 global bound B_log := 30731/98304 + M_{tilde{h},0}^{(-3/2)} + (1/2) M_{tilde{h},log}^{(-3/2)}
    for sup_{X >= 1} |W_log(X)| live in 256-bit Arb from the 7 certified positive roots of
    Q_0(u) = 648 u^7 - 93844 u^6 + 1345108 u^5 - 4462075 u^4 + 4306220 u^3 - 1202252 u^2 + 75896 u - 432
    (where u = alpha^2)."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        tol_spec = 2 ** (-90)
        u_poly_sym = sp.Symbol("u", real=True)
        q0_poly_sym = (
            648 * u_poly_sym**7
            - 93844 * u_poly_sym**6
            + 1345108 * u_poly_sym**5
            - 4462075 * u_poly_sym**4
            + 4306220 * u_poly_sym**3
            - 1202252 * u_poly_sym**2
            + 75896 * u_poly_sym
            - 432
        )
        q0_deriv_sym = sp.diff(q0_poly_sym, u_poly_sym)
        q0_coeffs_d = [
            int(c) for c in sp.Poly(q0_poly_sym, u_poly_sym).all_coeffs()
        ]
        q0_deriv_coeffs_d = [
            int(c) for c in sp.Poly(q0_deriv_sym, u_poly_sym).all_coeffs()
        ]
        q0_intervals = sp.Poly(q0_poly_sym, u_poly_sym).intervals(eps=1e-35)

        def _horner_arb(coeffs_seq: List[int], u_a: arb) -> arb:
            acc = arb(0)
            for c_i in coeffs_seq:
                acc = acc * u_a + arb(c_i)
            return acc

        alpha_roots_7: List[arb] = []
        for (a_rat, b_rat), _ in q0_intervals:
            u_mid = arb(
                (
                    (
                        arb(int(a_rat.p)) / arb(int(a_rat.q))
                        + arb(int(b_rat.p)) / arb(int(b_rat.q))
                    )
                    / arb(2)
                ).mid()
            )
            for _ in range(12):
                u_mid = arb(
                    (
                        u_mid
                        - _horner_arb(q0_coeffs_d, u_mid)
                        / _horner_arb(q0_deriv_coeffs_d, u_mid)
                    ).mid()
                )
            u_pt = arb(u_mid.mid())
            rad_u = arb("1e-55")
            u_ball = arb(u_pt.mid(), rad_u.upper())
            n_step = u_pt - _horner_arb(q0_coeffs_d, u_pt) / _horner_arb(
                q0_deriv_coeffs_d, u_ball
            )
            if not bool(abs(n_step - u_pt) < rad_u):
                raise RuntimeError("Newton root certification failed in TC-050R B_log")
            alpha_roots_7.append(u_ball.sqrt())

        g_extrema = [
            (r_b ** arb("-0.5")) * evaluate_h0_arb(r_b) for r_b in alpha_roots_7
        ]
        m_th0_tv_arb = arb(2) * sum((abs(gv) for gv in g_extrema), arb(0))

        def _h0_over_al32_acb(al: acb, analytic: bool = False) -> acb:
            u2 = al * al
            op = acb(1) + u2
            op2 = op * op
            op4 = op2 * op2
            op6 = op4 * op2
            num = (
                -acb(648) * op6
                + acb(58380) * u2 * op4
                - acb(706860) * u2 * u2 * op2
                + acb(2027025) * u2 * u2 * u2
            )
            return al * num / (acb(512) * (op**8) * op.sqrt(analytic=analytic))

        def _h0_inv_u12_acb(u_c: acb, analytic: bool = False) -> acb:
            u2 = u_c * u_c
            op = acb(1) + u2
            op2 = op * op
            op4 = op2 * op2
            op6 = op4 * op2
            num = (
                -acb(648) * op6
                + acb(58380) * u2 * op4
                - acb(706860) * u2 * u2 * op2
                + acb(2027025) * u2 * u2 * u2
            )
            return u2 * num / (acb(512) * (op**8) * op.sqrt(analytic=analytic))

        def _log_g_endpoint(a_ball: arb) -> arb:
            m_f = float(a_ball.mid())
            if m_f == 0.0 or m_f == 1.0:
                return arb(0)
            return a_ball.log() * (a_ball ** arb("-0.5")) * evaluate_h0_arb(a_ball)

        nodes_log_ibp = [arb(0)] + alpha_roots_7[:4] + [arb(1)] + alpha_roots_7[4:]
        m_th_log_ibp_arb = arb(0)
        for idx_s in range(len(nodes_log_ibp) - 1):
            a_b = nodes_log_ibp[idx_s]
            b_b = nodes_log_ibp[idx_s + 1]
            int_h0_seg = acb.integral(
                _h0_over_al32_acb,
                acb(a_b.mid()),
                acb(b_b.mid()),
                rel_tol=tol_spec,
                abs_tol=tol_spec,
            ).real
            end_err = (
                arb(2) * abs(_h0_over_al32_acb(acb(a_b))).real * arb(a_b.rad())
                + arb(2) * abs(_h0_over_al32_acb(acb(b_b))).real * arb(b_b.rad())
            )
            seg_signed = (
                -_log_g_endpoint(b_b)
                + _log_g_endpoint(a_b)
                + int_h0_seg
                + arb(0, end_err.upper())
            )
            m_th_log_ibp_arb += abs(seg_signed)

        u_top_r7 = arb(1) / alpha_roots_7[-1]
        tail_h0_int = acb.integral(
            _h0_inv_u12_acb,
            acb(0),
            acb(u_top_r7.mid()),
            rel_tol=tol_spec,
            abs_tol=tol_spec,
        ).real
        tail_end_err = (
            arb(2) * abs(_h0_inv_u12_acb(acb(u_top_r7))).real * arb(u_top_r7.rad())
        )
        tail_seg_signed = (
            _log_g_endpoint(alpha_roots_7[-1])
            + tail_h0_int
            + arb(0, tail_end_err.upper())
        )
        m_th_log_ibp_arb += abs(tail_seg_signed)

        tail_constant = arb(30731) / arb(98304)
        b_log_total = tail_constant + m_th0_tv_arb + arb("0.5") * m_th_log_ibp_arb
        return {
            "B_log_arb": b_log_total,
            "M_tilde_h_0_arb": m_th0_tv_arb,
            "M_tilde_h_log_arb": m_th_log_ibp_arb,
            "tail_constant_30731_98304_arb": tail_constant,
        }
    finally:
        flint_ctx.prec = saved_prec


_LIVE_CONTROLLED_BOUNDS_CACHE: Dict[int, Dict[str, Any]] = {}


def _compute_live_controlled_component_bounds_arb(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Compute all 5 component global bounds for E_{tau,controlled}(K) (X_K = tau^{|K|} >= 1)
    live in 256-bit Arb from their proved analytic formulas."""
    if prec_bits in _LIVE_CONTROLLED_BOUNDS_CACHE:
        return _LIVE_CONTROLLED_BOUNDS_CACHE[prec_bits]
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        pi_arb = arb.pi()
        tau_arb = arb(2) * pi_arb
        gamma_e_arb = arb.const_euler()
        c_tau_A_arb = (arb(4) * tau_arb).log() + gamma_e_arb + tau_arb / arb(4)
        h0_1_arb = evaluate_h0_arb(arb(1))
        c0_bernstein = arb(92193) / arb(32768)

        # 1. Pole + transfer archimedean term -(c_tau^B + 2) h_0(X_K) = -c_tau^A h_0(X_K):
        # Note: h_0(X) changes sign on [1, infty) (e.g., h_0(2) = -0.217430622... < 0), so
        # |h_0(X_K)| <= h_0(1) is NOT proved by monotonicity/positivity; instead it follows
        # unconditionally from the multiplicative autocorrelation identity
        # h_0(tau^{|K|}) = <T_{|K|} psi_tau, psi_tau>_{L^2(dy/y)} and unitary dilation Cauchy-Schwarz
        # |h_0(X_K)| <= ||T_{|K|} psi_tau||_{L^2(dy/y)} ||psi_tau||_{L^2(dy/y)} = ||psi_tau||_{L^2(dy/y)}^2 = h_0(1)
        # (and independently from the symmetric Bernstein envelope |h_0(X)| <= (92193/32768)(X + X^{-1})^{-5/2} <= h_0(1)),
        # giving B_{h_0} = c_tau^A h_0(1).
        # For large X_K -> infty, h_0(X_K) ~ -(81/64) X_K^{-5/2} and
        # |c_tau^A h_0(X_K)| <= c_tau^A * (92193/32768) * X_K^{-5/2} = O(X_K^{-5/2}).
        B_h0_arb = c_tau_A_arb * h0_1_arb
        C_h0_decay_arb = c_tau_A_arb * c0_bernstein

        # 2. Reflected small-scale prime sum W(X_K^{-1}) for X_K >= 1:
        # |W(X_K^{-1})| <= (92193/32768) * (sum_{n>=2} Lambda(n)/n^3) * X_K^{-5/2} <= B_refl.
        n_max_pp = 25000
        pp_all = get_prime_powers_up_to(n_max_pp)
        s_prime_cube = arb(0)
        for pk, p, _ in pp_all:
            pk_a = arb(pk)
            s_prime_cube += arb(p).log() / (pk_a ** arb(3))
        rs_tail = arb("1.558245") / (arb(n_max_pp) ** arb(2))
        # Enclose sum_{n>=2} Lambda(n)/n^3 in [s_prime_cube, s_prime_cube + rs_tail]:
        half_rs = rs_tail / arb(2)
        prime_cube_enclosure = s_prime_cube + arb(half_rs.mid(), abs(half_rs).upper())
        B_refl_arb = c0_bernstein * prime_cube_enclosure

        # 3. Divisor-aggregated log-prime profile W_log(X_K) for X_K >= 1:
        # Global bound on [1, infty) from TC-044 total variation + IBP, and large-scale
        # O(X_K^{-5/2}) decay constant C_{log,EM} from TC-049R Euler-Maclaurin theorem:
        b_log_res = _compute_live_B_log_global_bound_arb(prec_bits=prec_bits)
        B_log_arb = b_log_res["B_log_arb"]
        tc049r_cert = certify_w_log_large_scale_decay_and_resonant_band_reduction_arb(
            prec_bits=prec_bits
        )
        c_em_cert_dict = tc049r_cert[
            "global_euler_maclaurin_constant_C_log_EM_certified"
        ]
        C_log_EM_arb = arb(c_em_cert_dict["arb_ball_str"])
        zeta_prime_3_arb = acb_series([acb(3), acb(1)], 2).zeta()[1].real
        C_log_0_arb = c0_bernstein * (-zeta_prime_3_arb)

        # 4. Head Moebius sum R_{mu,head}(X_K) over 2 <= m <= H(X_K) = floor(X_K^{5/6}):
        # |R_{mu,head}(X_K)| <= C_{log,EM} X_K^{-5/2} sum_{2 <= m <= H(X_K)} m^2 <= (5/6) C_{log,EM}.
        B_head_arb = (arb(5) / arb(6)) * C_log_EM_arb

        # 5. Super-scale tail Moebius sum R_{mu,tail}(X_K) over m > M(X_K) = ceil(max(2, X_K^{5/4})):
        # |R_{mu,tail}(X_K)| <= C_{log,0} X_K^{5/2} / (2 M(X_K)^2) <= (1/2) C_{log,0}.
        B_tail_arb = (arb(1) / arb(2)) * C_log_0_arb

        # Total global bound B_ctrl and asymptotic limsup bound B_head + B_tail:
        B_ctrl_arb = B_h0_arb + B_refl_arb + B_log_arb + B_head_arb + B_tail_arb
        B_limsup_arb = B_head_arb + B_tail_arb

        res = {
            "B_h0_arb": B_h0_arb,
            "C_h0_decay_arb": C_h0_decay_arb,
            "B_refl_arb": B_refl_arb,
            "B_log_arb": B_log_arb,
            "C_log_EM_arb": C_log_EM_arb,
            "C_log_0_arb": C_log_0_arb,
            "B_head_arb": B_head_arb,
            "B_tail_arb": B_tail_arb,
            "B_ctrl_arb": B_ctrl_arb,
            "B_limsup_arb": B_limsup_arb,
        }
        _LIVE_CONTROLLED_BOUNDS_CACHE[prec_bits] = res
        return res
    finally:
        flint_ctx.prec = saved_prec


_LOG_SQRT_TABLE_CACHE: Dict[int, List[Tuple[int, arb, arb]]] = {}


def _get_log_sqrt_table_arb(max_k: int, prec_bits: int = 256) -> List[Tuple[int, arb, arb]]:
    """Return precomputed [(k, arb(k), log(k)/sqrt(k)) for k in 2..max_k] at `prec_bits`."""
    cached = _LOG_SQRT_TABLE_CACHE.get(prec_bits)
    if cached is not None and len(cached) >= max_k - 1:
        return cached[: max_k - 1]
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        start_k = 2 if cached is None else len(cached) + 2
        rows = [] if cached is None else list(cached)
        for k_i in range(start_k, max_k + 1):
            k_a = arb(k_i)
            rows.append((k_i, k_a, k_a.log() / k_a.sqrt()))
        _LOG_SQRT_TABLE_CACHE[prec_bits] = rows
        return rows[: max_k - 1]
    finally:
        flint_ctx.prec = saved_prec


def evaluate_W_log_em4_certified_arb(
    u: arb, min_N0: int = 240, prec_bits: int = 256
) -> arb:
    """Certify W_log(u) = sum_{k=2}^infty (log k / sqrt(k)) h_0(k / u) in 256-bit Arb for any u > 0
    via 4th-order Euler-Maclaurin on [N_0, infty) with N_0 = max(60 if u <= 0.5 else min_N0, ceil(24 u))
    (so alpha_{N_0} = N_0 / u >= 24 >= 20 for all u > 0), using the exact Euler-derivative identity
        g_u'(x) = x^{-3/2} (h_0(x / u) - (log x) tilde{h}_0(x / u))
    and the proved TC-049R 4th-order Euler-Maclaurin remainder bound
        |R_{EM,4}(N_0)| <= u^{-7/2} (14580 log N_0 + 16281) / (73728 alpha_{N_0}^6).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        u_a = arb(u)
        if (u_a - arb(0)).lower() <= arb(0):
            raise ValueError(f"u must be certified strictly positive: {u_a}")
        c0_bern = arb(92193) / arb(32768)
        ceil_24u = (arb(24) * u_a).upper().ceil().unique_fmpz()
        if ceil_24u is None:
            raise RuntimeError(f"Non-unique integer ceiling for 24*u: {u_a}")
        eff_min_N0 = 60 if float(u_a.upper()) <= 0.5 else min_N0
        N0 = max(eff_min_N0, int(ceil_24u))
        N0_a = arb(N0)
        al_N0 = N0_a / u_a
        if not bool((al_N0 - arb(20)).lower() >= arb(0)):
            raise RuntimeError(f"Euler-Maclaurin cutoff N0={N0} failed al_N0 >= 20 for u={u_a}")

        table = _get_log_sqrt_table_arb(N0, prec_bits=prec_bits)
        s_part = arb(0)
        for _, k_a, lsk in table:
            s_part += lsk * evaluate_h0_arb(k_a / u_a)

        h0_al = evaluate_h0_arb(al_N0)
        tilde_h0_al = evaluate_tilde_h0_arb(al_N0)
        g_N0 = (N0_a.log() / N0_a.sqrt()) * h0_al
        gp_N0 = (N0_a ** arb("-1.5")) * (h0_al - N0_a.log() * tilde_h0_al)

        tol_i = 2 ** (-90)
        u_c = acb(u_a)

        def _f_g(z_c: acb, analytic: bool = False, uc: acb = u_c) -> acb:
            return (
                (z_c ** acb("-0.5"))
                * z_c.log(analytic=analytic)
                * evaluate_h0_acb(z_c / uc, analytic=analytic)
            )

        N1 = 16 * N0
        N2 = 256 * N0
        N3 = 4096 * N0
        if float(u_a.upper()) <= 0.5:
            int_tail = (
                acb.integral(_f_g, acb(N0), acb(N1), rel_tol=tol_i, abs_tol=tol_i).real
                + acb.integral(_f_g, acb(N1), acb(N2), rel_tol=tol_i, abs_tol=tol_i).real
                + acb.integral(_f_g, acb(N2), acb(N3), rel_tol=tol_i, abs_tol=tol_i).real
            )
            N_end_a = arb(N3)
        else:
            N4 = 65536 * N0
            int_tail = (
                acb.integral(_f_g, acb(N0), acb(N1), rel_tol=tol_i, abs_tol=tol_i).real
                + acb.integral(_f_g, acb(N1), acb(N2), rel_tol=tol_i, abs_tol=tol_i).real
                + acb.integral(_f_g, acb(N2), acb(N3), rel_tol=tol_i, abs_tol=tol_i).real
                + acb.integral(_f_g, acb(N3), acb(N4), rel_tol=tol_i, abs_tol=tol_i).real
            )
            N_end_a = arb(N4)
        rem_int = (
            c0_bern
            * (u_a ** arb("2.5"))
            * (arb(2) * N_end_a.log() + arb(1))
            / (arb(4) * N_end_a * N_end_a)
        )
        rem_em = (
            (u_a ** arb("-3.5"))
            * (arb(14580) * N0_a.log() + arb(16281))
            / (arb(73728) * (al_N0 ** arb(6)))
        )
        return (
            s_part
            + int_tail
            - arb("0.5") * g_N0
            - gp_N0 / arb(12)
            + arb(0, (rem_int + rem_em).upper())
        )
    finally:
        flint_ctx.prec = saved_prec


def evaluate_tilde_W_log_certified_arb(
    u: arb, min_cut: int = 1600, prec_bits: int = 256
) -> arb:
    """Certify tilde{W}_log(u) = sum_{k=2}^infty (log k / sqrt(k)) tilde{h}_0(k / u)
      = (1/2) W_log(u) + u W_log'(u)
    in 256-bit Arb with the rigorous rational Bernstein envelope constant
    tilde{C}_0 = 10329937 / 655360 (from TC-040 / TC-044):
        |sum_{k > k_cut} (log k / sqrt(k)) tilde{h}_0(k / u)|
          <= (10329937 / 655360) u^{5/2} (2 log k_cut + 1) / (4 k_cut^2).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        u_a = arb(u)
        if (u_a - arb(0)).lower() <= arb(0):
            raise ValueError(f"u must be certified strictly positive: {u_a}")
        u_up = float(u_a.upper())
        k_cut = max(min_cut, int(math.ceil(250.0 * u_up)))
        table = _get_log_sqrt_table_arb(k_cut, prec_bits=prec_bits)
        s_fin = arb(0)
        for _, k_a, lsk in table:
            s_fin += lsk * evaluate_tilde_h0_arb(k_a / u_a)
        tilde_c0_bern = arb(10329937) / arb(655360)
        k_cut_a = arb(k_cut)
        tail_mag = (
            tilde_c0_bern
            * (u_a ** arb("2.5"))
            * (arb(2) * k_cut_a.log() + arb(1))
            / (arb(4) * k_cut_a * k_cut_a)
        )
        return s_fin + arb(0, tail_mag.upper())
    finally:
        flint_ctx.prec = saved_prec


def verify_canonical_hilbert_schmidt_orbit_decomposition(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Certify in 256-bit Arb the exact Hilbert-Schmidt unitary orbit decomposition:
        C_tau(K) = P_tau(K) + E_tau(K),
        P_tau(K) = <U_K B_0, B_0>_{HS} = W_arch(h_K) + (c_tau^B + 2) h_0(tau^{|K|}),
        |P_tau(K)| <= ||B_0||_{HS}^2 = P_tau(0) = 2.558258007415831... < 2.55826,
        E_tau(K) = E_{tau,controlled}(K) - R_{mu,band}(tau^{|K|}),
    using the rigorously supported TC-049/TC-049R cutoffs H(X) = floor(X^{5/6}) and
    M(X) = ceil(max(2, X^{5/4})) across positive and negative rational and irrational
    algebraic grades K in {0, 1/4, -1/4, 1/2, -1/2, 1, -1, sqrt(2), -sqrt(2), 3/2, -3/2, 2, -2}."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        pi_arb = arb.pi()
        tau_arb = arb(2) * pi_arb
        L_arb = tau_arb.log()
        gamma_e_arb = arb.const_euler()
        c_tau_A_arb = (arb(4) * tau_arb).log() + gamma_e_arb + tau_arb / arb(4)
        c_tau_B_arb = c_tau_A_arb - arb(2)
        h0_1_arb = evaluate_h0_arb(arb(1))
        c0_bernstein = arb(92193) / arb(32768)
        tol_spec = 2 ** (-90)

        n_max_pp = 25000
        pp_all = get_prime_powers_up_to(n_max_pp)

        live_bounds = _compute_live_controlled_component_bounds_arb(
            prec_bits=prec_bits
        )
        B_h0_arb = live_bounds["B_h0_arb"]
        C_h0_decay_arb = live_bounds["C_h0_decay_arb"]
        B_refl_arb = live_bounds["B_refl_arb"]
        B_log_arb = live_bounds["B_log_arb"]
        C_log_EM_arb = live_bounds["C_log_EM_arb"]
        C_log_0_arb = live_bounds["C_log_0_arb"]
        B_head_arb = live_bounds["B_head_arb"]
        B_tail_arb = live_bounds["B_tail_arb"]
        B_ctrl_arb = live_bounds["B_ctrl_arb"]
        B_limsup_arb = live_bounds["B_limsup_arb"]

        # Helper for J(kappa) = 4 ||f||^2 - 4 <R_0 T_K psi_tau, R_0 psi_tau>:
        def _eval_j_kap(kappa_a: arb) -> arb:
            kap_c = acb(kappa_a)
            u_top_J = max(20, int(math.ceil(float(abs(kappa_a).upper()))) + 16)

            def _f_j_loc(u: acb, analytic: bool, kc: acb = kap_c) -> acb:
                hp = evaluate_h0_acb((kc + u).exp(), analytic=analytic)
                hm = evaluate_h0_acb((kc - u).exp(), analytic=analytic)
                return (hp + hm) * ((-u / acb(2)).exp())

            j_fin = arb(0)
            for m_step in range(0, 4 * u_top_J):
                j_fin += acb.integral(
                    _f_j_loc,
                    acb(m_step) / acb(4),
                    acb(m_step + 1) / acb(4),
                    rel_tol=tol_spec,
                    abs_tol=tol_spec,
                ).real
            u_top_a = arb(u_top_J)
            j_tail = (
                (arb(2) / arb(3))
                * c0_bernstein
                * ((arb("2.5") * abs(kappa_a)).exp())
                * ((-arb(3) * u_top_a).exp())
            )
            return j_fin + arb(0, j_tail.upper())

        # Helper for certified W_log(u) for any u > 0 using 4th-order Euler-Maclaurin on [N0, infty):
        def _eval_W_log_arb(u_a: arb, min_cut: int = 240) -> arb:
            return evaluate_W_log_em4_certified_arb(
                u_a, min_N0=max(240, min(min_cut, 360)), prec_bits=prec_bits
            )

        # Fast certified helper for tiny u <= 0.4 in the super-scale tail m > M(X_K):
        small_tail_table = _get_log_sqrt_table_arb(240, prec_bits=prec_bits)

        def _eval_W_log_small_tail_arb(u_a: arb, k_cut: int = 160) -> arb:
            s_fin = arb(0)
            for _, k_a, lsk in small_tail_table[: k_cut - 1]:
                s_fin += lsk * evaluate_h0_arb(k_a / u_a)
            k_cut_a = arb(k_cut)
            tail_mag = (
                c0_bernstein
                * (u_a ** arb("2.5"))
                * (arb(2) * k_cut_a.log() + arb(1))
                / (arb(4) * k_cut_a * k_cut_a)
            )
            return s_fin + arb(0, tail_mag.upper())

        # Helper for certified W(u) for any u > 0 using N_max = 25000 + Rosser-Schoenfeld tail:
        def _eval_W_arb(u_a: arb) -> arb:
            s_fin = arb(0)
            for pk, p, _ in pp_all:
                pk_a = arb(pk)
                s_fin += (arb(p).log() / pk_a.sqrt()) * evaluate_h0_arb(pk_a / u_a)
            n_cut_a = arb(n_max_pp)
            tail_mag = (
                c0_bernstein
                * (u_a ** arb("2.5"))
                * (arb("1.558245") / (n_cut_a * n_cut_a))
            )
            return s_fin + arb(0, tail_mag.upper())

        # Evaluate at K = 0 to obtain the Hilbert-Schmidt norm squared ||B_0||_{HS}^2 = P_tau(0):
        w_arch_0 = evaluate_archimedean_integral_certified_arb(
            arb(0), prec_bits=prec_bits
        )["w_arch_total_arb"]
        j_0 = _eval_j_kap(arb(0))
        four_r0_norm_sq_0 = arb(4) * h0_1_arb - j_0
        b_transfer_0 = arb(2) * h0_1_arb - j_0
        p_tau_B_0 = w_arch_0 + c_tau_B_arb * h0_1_arb - b_transfer_0
        p_tau_0 = p_tau_B_0 + four_r0_norm_sq_0  # = w_arch_0 + c_tau_A_arb * h0_1_arb

        # Evaluate across positive and negative rational and irrational algebraic grades:
        sqrt2_arb = arb(2).sqrt()
        grade_samples: List[Tuple[str, str, arb]] = [
            ("0", "0", arb(0)),
            ("1/4", "1/4", arb(1) / arb(4)),
            ("-1/4", "1/4", arb(-1) / arb(4)),
            ("1/2", "1/2", arb(1) / arb(2)),
            ("-1/2", "1/2", arb(-1) / arb(2)),
            ("1", "1", arb(1)),
            ("-1", "1", arb(-1)),
            ("sqrt(2)", "sqrt(2)", sqrt2_arb),
            ("-sqrt(2)", "sqrt(2)", -sqrt2_arb),
            ("3/2", "3/2", arb(3) / arb(2)),
            ("-3/2", "3/2", arb(-3) / arb(2)),
            ("2", "2", arb(2)),
            ("-2", "2", arb(-2)),
        ]

        # Pre-cache by |K| while independently evaluating K = -1 to certify evenness W_arch(-1) = W_arch(1):
        abs_k_cache: Dict[str, Dict[str, Any]] = {}
        w_arch_neg_1 = evaluate_archimedean_integral_certified_arb(
            arb(-1), prec_bits=prec_bits
        )["w_arch_total_arb"]
        orbit_rows: List[Dict[str, Any]] = []
        all_orbit_identities_enclose_zero = True
        all_hs_cauchy_schwarz_verified = True
        all_independent_tail_bounds_verified = True
        all_component_bounds_verified = True
        all_sample_cutoffs_exact_clamped_certified = True

        for k_label, abs_key, k_a in grade_samples:
            abs_k = abs(k_a)
            kap_a = abs_k * L_arb
            X_k = arb(1) if k_label == "0" else kap_a.exp()
            inv_X_k = arb(1) if k_label == "0" else (-kap_a).exp()
            h0_X_k = h0_1_arb if k_label == "0" else evaluate_h0_arb(X_k)

            if abs_key not in abs_k_cache:
                w_arch_abs = (
                    w_arch_0
                    if abs_key == "0"
                    else evaluate_archimedean_integral_certified_arb(
                        abs_k, prec_bits=prec_bits
                    )["w_arch_total_arb"]
                )
                j_abs = j_0 if abs_key == "0" else _eval_j_kap(kap_a)
                w_XK_abs = _eval_W_arb(X_k)
                w_inv_XK_abs = w_XK_abs if abs_key == "0" else _eval_W_arb(inv_X_k)
                w_log_XK_abs = _eval_W_log_arb(X_k, min_cut=3200)

                # Certified TC-049/TC-049R cutoffs H(X_K) = floor(X_K^{5/6}) and M(X_K) = ceil(max(2, X_K^{5/4})):
                h_cut_int = certified_head_cutoff_H_X_arb(X_k, prec_bits=prec_bits)
                m_cut_int = certified_coupled_cutoff_M_X_arb(X_k, prec_bits=prec_bits)
                m_clamped_cert = certify_clamped_exact_cutoff_M_X_arb(
                    X_k, prec_bits=prec_bits
                )

                # Direct finite-sum evaluation of R_{mu,head}(X_K) over 2 <= m <= H(X_K) (0 if H(X_K) < 2):
                r_mu_head_abs = arb(0)
                for m_i in range(2, h_cut_int + 1):
                    mu_m = moebius_mu_int(m_i)
                    if mu_m == 0:
                        continue
                    m_a = arb(m_i)
                    r_mu_head_abs += (
                        arb(mu_m) / m_a.sqrt()
                    ) * _eval_W_log_arb(X_k / m_a, min_cut=1200)

                # Direct finite-sum evaluation of R_{mu,band}(X_K) over max(2, H(X_K)+1) <= m <= M(X_K):
                r_mu_band_abs = arb(0)
                band_start = max(2, h_cut_int + 1)
                for m_i in range(band_start, m_cut_int + 1):
                    mu_m = moebius_mu_int(m_i)
                    if mu_m == 0:
                        continue
                    m_a = arb(m_i)
                    r_mu_band_abs += (
                        arb(mu_m) / m_a.sqrt()
                    ) * _eval_W_log_arb(X_k / m_a, min_cut=1000)

                # Direct certified enclosure of R_{mu,tail}(X_K) over m > M(X_K):
                # Sum M(X_K) < m <= m_tail_cut directly + analytic remainder C_{log,0} X_K^{5/2} / (2 m_tail_cut^2):
                m_tail_cut = max(800, 25 * m_cut_int)
                r_mu_tail_partial = arb(0)
                for m_i in range(m_cut_int + 1, m_tail_cut + 1):
                    mu_m = moebius_mu_int(m_i)
                    if mu_m == 0:
                        continue
                    m_a = arb(m_i)
                    k_cut_tail = 180 if m_i < 4 * m_cut_int else 70
                    r_mu_tail_partial += (
                        arb(mu_m) / m_a.sqrt()
                    ) * _eval_W_log_small_tail_arb(X_k / m_a, k_cut=k_cut_tail)
                rem_after_tail_cut = (
                    C_log_0_arb
                    * (X_k ** arb("2.5"))
                    / (arb(2) * (arb(m_tail_cut) ** arb(2)))
                )
                r_mu_tail_direct_abs = r_mu_tail_partial + arb(
                    0, rem_after_tail_cut.upper()
                )

                abs_k_cache[abs_key] = {
                    "w_arch_abs": w_arch_abs,
                    "j_abs": j_abs,
                    "w_XK_abs": w_XK_abs,
                    "w_inv_XK_abs": w_inv_XK_abs,
                    "w_log_XK_abs": w_log_XK_abs,
                    "h_cut_int": h_cut_int,
                    "m_cut_int": m_cut_int,
                    "m_clamped_cert": m_clamped_cert,
                    "r_mu_head_abs": r_mu_head_abs,
                    "r_mu_band_abs": r_mu_band_abs,
                    "r_mu_tail_direct_abs": r_mu_tail_direct_abs,
                }

            cached = abs_k_cache[abs_key]
            w_arch_k = w_arch_neg_1 if k_label == "-1" else cached["w_arch_abs"]
            j_k = cached["j_abs"]
            w_XK = cached["w_XK_abs"]
            w_inv_XK = cached["w_inv_XK_abs"]
            w_log_XK = cached["w_log_XK_abs"]
            h_cut_XK = cached["h_cut_int"]
            m_cut_XK = cached["m_cut_int"]
            m_clamped_cert_XK = cached["m_clamped_cert"]
            r_mu_head_XK = cached["r_mu_head_abs"]
            r_mu_band_XK = cached["r_mu_band_abs"]
            r_mu_tail_direct_XK = cached["r_mu_tail_direct_abs"]
            if not m_clamped_cert_XK["exact_clamped_characterization_certified"]:
                all_sample_cutoffs_exact_clamped_certified = False

            w_prime_k = w_XK + w_inv_XK
            c_tau_k = w_arch_k - w_prime_k

            four_r0_inner_k = arb(4) * h0_X_k - j_k
            b_transfer_k = arb(2) * h0_X_k - j_k
            p_tau_B_k = w_arch_k + c_tau_B_arb * h0_X_k - b_transfer_k
            p_tau_k = p_tau_B_k + four_r0_inner_k  # = <U_K B_0, B_0>_{HS}

            # Outward-rounded Cauchy-Schwarz certification |P_tau(K)| <= P_tau(0) and |P_tau^B(K)| <= P_tau^B(0):
            is_k_zero = k_label == "0"
            hs_cs_cert = certify_abs_le_bound_arb(
                p_tau_k, p_tau_0, exact_self_equality=is_k_zero
            )
            hs_B_cs_cert = certify_abs_le_bound_arb(
                p_tau_B_k, p_tau_B_0, exact_self_equality=is_k_zero
            )
            hs_cs_ok = bool(hs_cs_cert["certified"])
            hs_B_cs_ok = bool(hs_B_cs_cert["certified"])
            if not (hs_cs_ok and hs_B_cs_ok):
                all_hs_cauchy_schwarz_verified = False

            # Independent comparison between direct finite sums R_{mu,head}(X_K) + R_{mu,band}(X_K)
            # and independently evaluated R_mu(X_K) = W(X_K) - W_log(X_K):
            r_mu_total_XK = w_XK - w_log_XK
            r_mu_tail_from_diff_XK = r_mu_total_XK - (r_mu_head_XK + r_mu_band_XK)

            # Proved TC-049/TC-049R tail bound at M(X_K) = ceil(max(2, X_K^{5/4})):
            # |R_{mu,tail}(X_K)| <= C_{log,0} X_K^{5/2} / (2 M(X_K)^2) <= (1/2) C_{log,0}:
            analytic_tail_bound_XK = (
                C_log_0_arb
                * (X_k ** arb("2.5"))
                / (arb(2) * (arb(m_cut_XK) ** arb(2)))
            )
            tail_bound_cert_from_diff = certify_abs_le_bound_arb(
                r_mu_tail_from_diff_XK, analytic_tail_bound_XK
            )
            tail_bound_cert_direct = certify_abs_le_bound_arb(
                r_mu_tail_direct_XK, analytic_tail_bound_XK
            )
            tail_diff_consistency = r_mu_tail_from_diff_XK - r_mu_tail_direct_XK
            tail_encloses_zero = bool(tail_diff_consistency.contains(0))
            if not (
                tail_bound_cert_from_diff["certified"]
                and tail_bound_cert_direct["certified"]
                and tail_encloses_zero
            ):
                all_independent_tail_bounds_verified = False

            # Pole + transfer archimedean term -(c_tau^B + 2) h_0(X_K) = -c_tau^A h_0(X_K):
            c_pole_transfer_h0_k = -c_tau_A_arb * h0_X_k

            # Total remainder E_tau(K) = C_tau(K) - P_tau(K):
            e_tau_k = c_tau_k - p_tau_k

            # Full 5-term controlled remainder E_{tau,controlled}(K):
            e_ctrl_k = (
                c_pole_transfer_h0_k
                - w_inv_XK
                - w_log_XK
                - r_mu_head_XK
                - r_mu_tail_direct_XK
            )
            e_ctrl_minus_tail_k = (
                c_pole_transfer_h0_k - w_inv_XK - w_log_XK - r_mu_head_XK
            )

            # Outward-rounded component bound checks at grade K:
            cert_h0_k = certify_abs_le_bound_arb(
                c_pole_transfer_h0_k, B_h0_arb, exact_self_equality=is_k_zero
            )
            cert_refl_k = certify_abs_le_bound_arb(w_inv_XK, B_refl_arb)
            cert_log_k = certify_abs_le_bound_arb(w_log_XK, B_log_arb)
            cert_head_k = certify_abs_le_bound_arb(r_mu_head_XK, B_head_arb)
            cert_tail_global_k = certify_abs_le_bound_arb(
                r_mu_tail_direct_XK, B_tail_arb
            )
            cert_e_ctrl_k = certify_abs_le_bound_arb(e_ctrl_k, B_ctrl_arb)
            if not (
                cert_h0_k["certified"]
                and cert_refl_k["certified"]
                and cert_log_k["certified"]
                and cert_head_k["certified"]
                and cert_tail_global_k["certified"]
                and cert_e_ctrl_k["certified"]
            ):
                all_component_bounds_verified = False

            # Algebraic consistency check C_tau(K) = P_tau(K) + E_{tau,controlled}(K) - R_{mu,band}(X_K):
            c_tau_reconstructed = p_tau_k + e_ctrl_k - r_mu_band_XK
            recon_diff = c_tau_k - c_tau_reconstructed
            encloses_zero = bool(recon_diff.contains(0))
            if not encloses_zero:
                all_orbit_identities_enclose_zero = False

            orbit_rows.append(
                {
                    "K_label": k_label,
                    "K_float": float(k_a.mid()),
                    "X_K_eq_tau_abs_K_certified": serialize_arb_certified(X_k),
                    "H_XK_eq_floor_XK_5_6": h_cut_XK,
                    "M_XK_eq_ceil_max_2_XK_5_4": m_cut_XK,
                    "M_XK_clamped_exact_characterization": m_clamped_cert_XK,
                    "head_sum_is_empty": bool(h_cut_XK < 2),
                    "C_tau_K_certified": serialize_arb_certified(c_tau_k),
                    "P_tau_K_HS_orbit_certified": serialize_arb_certified(p_tau_k),
                    "P_tau_B_K_conductor_inner_certified": serialize_arb_certified(
                        p_tau_B_k
                    ),
                    "four_R0_inner_K_certified": serialize_arb_certified(
                        four_r0_inner_k
                    ),
                    "abs_P_tau_K_le_P_tau_0": hs_cs_ok,
                    "abs_P_tau_K_le_P_tau_0_certification": hs_cs_cert,
                    "abs_P_tau_B_K_le_P_tau_B_0_certification": hs_B_cs_cert,
                    "E_tau_K_total_remainder_certified": serialize_arb_certified(
                        e_tau_k
                    ),
                    "E_tau_controlled_K_certified": serialize_arb_certified(e_ctrl_k),
                    "E_ctrl_K_minus_tail_certified": serialize_arb_certified(
                        e_ctrl_minus_tail_k
                    ),
                    "pole_plus_transfer_term_neg_c_tau_A_h0_certified": serialize_arb_certified(
                        c_pole_transfer_h0_k
                    ),
                    "small_scale_prime_W_inv_XK_certified": serialize_arb_certified(
                        w_inv_XK
                    ),
                    "divisor_aggregated_W_log_XK_certified": serialize_arb_certified(
                        w_log_XK
                    ),
                    "head_divisor_R_mu_head_XK_certified": serialize_arb_certified(
                        r_mu_head_XK
                    ),
                    "resonant_band_R_mu_band_XK_direct_sum_certified": serialize_arb_certified(
                        r_mu_band_XK
                    ),
                    "super_scale_tail_R_mu_tail_XK_direct_certified": serialize_arb_certified(
                        r_mu_tail_direct_XK
                    ),
                    "super_scale_tail_R_mu_tail_XK_from_W_minus_Wlog_minus_head_band_certified": serialize_arb_certified(
                        r_mu_tail_from_diff_XK
                    ),
                    "super_scale_tail_analytic_bound_C_log_0_XK_5_2_over_2_M_sq_certified": serialize_arb_certified(
                        analytic_tail_bound_XK
                    ),
                    "independent_tail_enclosure_verification": {
                        "verification_type": "INDEPENDENT_HEAD_BAND_VS_TOTAL_MOEBIUS_TAIL_ENCLOSURE_CHECK",
                        "tail_from_diff_le_analytic_bound": tail_bound_cert_from_diff,
                        "tail_direct_le_analytic_bound": tail_bound_cert_direct,
                        "tail_diff_minus_direct_encloses_zero": tail_encloses_zero,
                    },
                    "component_bound_certifications": {
                        "abs_pole_transfer_le_B_h0": cert_h0_k,
                        "abs_W_inv_XK_le_B_refl": cert_refl_k,
                        "abs_W_log_XK_le_B_log": cert_log_k,
                        "abs_R_mu_head_le_B_head": cert_head_k,
                        "abs_R_mu_tail_le_B_tail": cert_tail_global_k,
                        "abs_E_ctrl_le_B_ctrl": cert_e_ctrl_k,
                    },
                    "reconstruction_diff_C_tau_minus_P_plus_E_certified": serialize_arb_certified(
                        recon_diff
                    ),
                    "reconstruction_verification_type": "ALGEBRAIC_CONSISTENCY_CHECK",
                    "reconstruction_encloses_zero": encloses_zero,
                }
            )

        r0_audit = verify_euler_resolvent_R0_spatial_and_mellin_identity_arb(
            prec_bits=prec_bits
        )
        h0_audit = verify_h0_autocorrelation_cauchy_schwarz_and_sign_change_arb(
            prec_bits=prec_bits
        )
        clamped_boundary_audit = {
            "exact_X_eq_1_M_eq_2": certify_clamped_exact_cutoff_M_X_arb(
                arb(1), prec_bits=prec_bits
            ),
            "exact_X_eq_16_M_eq_32": certify_clamped_exact_cutoff_M_X_arb(
                arb(16), prec_bits=prec_bits
            ),
            "straddling_ball_X_eq_16_pm_1e_30_M_safe_eq_33": certify_clamped_exact_cutoff_M_X_arb(
                arb(16, arb("1e-30").upper()), prec_bits=prec_bits
            ),
        }

        observable_radius_summary: Dict[str, Any] = {
            "sample_grade_set": [r["K_label"] for r in orbit_rows],
            "sample_grade_count": len(orbit_rows),
            "per_observable_max_radius": {
                obs_key: max(
                    float(r[obs_key]["enclosure_arb"].rad())
                    for r in orbit_rows
                )
                for obs_key in (
                    "P_tau_K_HS_orbit_certified",
                    "pole_plus_transfer_term_neg_c_tau_A_h0_certified",
                    "small_scale_prime_W_inv_XK_certified",
                    "divisor_aggregated_W_log_XK_certified",
                    "head_divisor_R_mu_head_XK_certified",
                    "resonant_band_R_mu_band_XK_direct_sum_certified",
                    "super_scale_tail_R_mu_tail_XK_direct_certified",
                    "E_tau_controlled_K_certified",
                    "E_tau_K_total_remainder_certified",
                    "C_tau_K_certified",
                )
            },
            "precision_scope_note": (
                "Each observable's radius reflects its specific analytical truncation and quadrature budget "
                "(all ceilings below are rounded upward): W_log(X_K), R_{mu,head}(X_K), and R_{mu,band}(X_K) "
                "(evaluated by 4th-order Euler-Maclaurin on [N0, infty)) have radii <= 6.59e-11 (<= 6.59e-11, "
                "<= 5.64e-11, and <= 5.65e-11), P_tau(K) has radius <= 3.22e-22, -(c_tau^B+2)h_0(X_K) has radius "
                "<= 6.35e-75, and W(X_K^{-1}) has radius <= 7.02e-9, whereas R_{mu,tail}(X_K) and E_{tau,controlled}(K) "
                "include the direct super-scale tail remainder C_{log,0} X_K^{5/2} / (2 m_tail_cut^2) (radii <= 4.36e-7 "
                "at K=0 up to <= 5.43e-4 at |K|=2), and C_tau(K) and E_tau(K) include the prime-power Rosser-Schoenfeld "
                "tail on n > 16500 in W(X_K) (radii <= 1.41e-8 at K=0 up to <= 6.87e-5 at |K|=2)."
            ),
        }

        return {
            "positive_hilbert_space_and_unitary_orbit": {
                "hilbert_space_H_tau_pos": "H_tau^pos := H_tau^B (+) L^2(R_{>0}, dy/y)",
                "conductor_space_H_tau_B": (
                    "H_tau^B := L^2([1, infty) x R_{>0}, (x^{-3/2} / (x - x^{-1})) (dx/x) (dy/y))"
                ),
                "shift_difference_operator_A_tau_B": (
                    "(A_tau^B f)(x, y) := ((I - S_x^{-1}) f)(y) = f(y) - f(y/x)   (x >= 1, y > 0)"
                ),
                "two_sided_vs_one_sided_shift_reconciliation": (
                    "With (S_x f)(y) = f(xy) and (S_x^{-1} f)(y) = f(y/x), the inherited TC-042F/TC-043 "
                    "Attempt B one-sided shift-difference (A_tau^B f)(x, y) = f(y) - f(y/x) satisfies "
                    "int_0^infty ((A_tau^B T_K f)(x, y)) conj((A_tau^B f)(x, y)) dy/y = "
                    "2 h_0(e^kappa) - h_0(e^{kappa + u}) - h_0(e^{kappa - u}) (kappa = |K| log tau, u = log x). "
                    "By contrast, a two-sided difference f(xy) - f(y/x) would evaluate to "
                    "2 h_0(e^kappa) - h_0(e^{kappa + 2u}) - h_0(e^{kappa - 2u}) (doubling the log-shift u -> 2u) "
                    "unless x is replaced by x^{1/2} via the isometric change of variable y |-> x^{-1/2} y."
                ),
                "isometric_embedding_J_tau": (
                    "J_tau(f) := (A_tau^B f, 2 R_0 f) in H_tau^pos = H_tau^B (+) L^2(R_{>0}, dy/y), "
                    "where (R_0 f)(y) := int_0^y (t/y)^{1/2} (D f)(t) dt/t = f(y) - (1/2) int_0^y (t/y)^{1/2} f(t) dt/t "
                    "(with Euler derivative D = y d/dy) is the causal s = 0 pole-resolvent with Mellin multiplier "
                    "it / (1/2 + it) and 4 <R_0 T_K psi_tau, R_0 psi_tau>_{L^2(dy/y)} = 4 h_0(e^kappa) - J(kappa), "
                    "J(kappa) := int_0^infty e^{-u/2} (h_0(e^{kappa+u}) + h_0(e^{kappa-u})) du."
                ),
                "euler_resolvent_R0_and_pole_integral_J_kappa_audit": r0_audit,
                "unitary_representation_and_intertwining": (
                    "U_K (phi, psi) := (U_K^B phi, T_K psi) for all K in A_R, where (U_K^B phi)(x, y) = phi(x, tau^{-K} y) "
                    "and (T_K psi)(y) = psi(tau^{-K} y) are unitary dilations with U_K^* = U_{-K}, satisfying "
                    "the exact intertwining identity J_tau(T_K f) = U_K J_tau(f)."
                ),
                "hilbert_schmidt_seed_operator_B_0": (
                    "B_0 := |Psi_0^pos><e_0| in HS(H_tau^pos), where Psi_0^pos := J_tau(psi_tau) = (A_tau^B psi_tau, 2 R_0 psi_tau) "
                    "and e_0 in H_tau^pos is a fixed unit vector (||e_0|| = 1), with left unitary orbit B_K := U_K B_0 = |U_K Psi_0^pos><e_0|."
                ),
                "pole_integral_J_kappa_cancellation_identity": (
                    "<A_tau^B T_K psi_tau, A_tau^B psi_tau>_{H_tau^B} = W_arch(h_K) + c_tau^B h_0(X_K) - (2 h_0(X_K) - J(kappa)) "
                    "and 4 <R_0 T_K psi_tau, R_0 psi_tau>_{L^2(dy/y)} = 4 h_0(X_K) - J(kappa) "
                    "(where J(kappa) = int_0^infty e^{-u/2} (h_0(e^{kappa+u}) + h_0(e^{kappa-u})) du has exponential weight e^{-u/2}, "
                    "while P_tau^B(K) has weight e^{-3u/2}/(2 sinh u)), so J(kappa) cancels identically in their sum "
                    "P_tau(K) = W_arch(h_K) + (c_tau^B + 2) h_0(X_K)."
                ),
                "matrix_coefficient_identity": (
                    "P_tau(K) := <B_K, B_0>_{HS} = <U_K Psi_0^pos, Psi_0^pos>_{H_tau^pos} "
                    "= <A_tau^B T_K psi_tau, A_tau^B psi_tau>_{H_tau^B} + 4 <R_0 T_K psi_tau, R_0 psi_tau>_{L^2(dy/y)} "
                    "= W_arch(h_K) + (c_tau^B + 2) h_0(tau^{|K|}) = W_arch(h_K) + c_tau^A h_0(tau^{|K|})."
                ),
                "norm_B_0_HS_sq_eq_P_tau_0_certified": serialize_arb_certified(
                    p_tau_0
                ),
                "norm_A_tau_B_psi_tau_sq_certified": serialize_arb_certified(
                    p_tau_B_0
                ),
                "four_norm_R0_psi_tau_sq_certified": serialize_arb_certified(
                    four_r0_norm_sq_0
                ),
                "all_sample_grades_satisfy_HS_cauchy_schwarz": all_hs_cauchy_schwarz_verified,
            },
            "exact_decomposition_and_controlled_remainder_bounds": {
                "decomposition_formula": (
                    "C_tau(K) = P_tau(K) + E_tau(K),   "
                    "E_tau(K) = E_{tau,controlled}(K) - R_{mu,band}(tau^{|K|})"
                ),
                "cutoff_definitions_tc049r": {
                    "H_X_formula": "H(X) := floor(X^{5/6})",
                    "H_X_exact_characterization": "H^6 <= X^5 < (H + 1)^6   (for X > 0, integer H >= 0)",
                    "H_X_helper_location": "certified_head_cutoff_H_X_arb in tc/faithful_tau_arithmetic_spectral_realization.py",
                    "M_X_formula": "M(X) := ceil(max(2, X^{5/4}))",
                    "M_X_clamped_exact_characterization": (
                        "M >= 2  and  X^5 <= M^4  and  (M = 2  or  (M - 1)^4 < X^5)   (for X >= 1, integer M)"
                    ),
                    "M_X_helper_location_and_scope": (
                        "certified_coupled_cutoff_M_X_arb in tc/prime_euler_moebius_recovery.py computes "
                        "M_safe(X_ball) = max(2, int(((X_ball^5)^{1/4}).upper().ceil())) and certifies X_ball^5 <= M_safe^4 "
                        "(a certified safe upper cutoff across X_ball). certify_clamped_exact_cutoff_M_X_arb in "
                        "tc/faithful_tau_arithmetic_spectral_realization.py additionally verifies the clamped lower "
                        "condition (M = 2 or (M - 1)^4 < X_ball^5) so M_safe(X_ball) = M(X) is exact on X_ball whenever "
                        "(X_ball^5)^{1/4} does not straddle an integer >= 2."
                    ),
                    "all_sample_cutoffs_exact_clamped_certified": all_sample_cutoffs_exact_clamped_certified,
                    "clamped_cutoff_boundary_audit": clamped_boundary_audit,
                    "R_mu_head_formula": "R_{mu,head}(X) := sum_{2 <= m <= H(X)} (mu(m)/sqrt(m)) W_log(X/m)  (0 when H(X) < 2)",
                    "R_mu_band_formula": "R_{mu,band}(X) := sum_{H(X) < m <= M(X)} (mu(m)/sqrt(m)) W_log(X/m)",
                    "R_mu_tail_formula": "R_{mu,tail}(X) := sum_{m > M(X)} (mu(m)/sqrt(m)) W_log(X/m)",
                    "divisor_vs_prime_cutoff_distinction": (
                        "H(X) and M(X) are divisor cutoffs on the integer index m in the full Moebius sum "
                        "R_mu(X) = sum_{m>=2} (mu(m)/sqrt(m)) W_log(X/m). By contrast, y in the prime-sieved "
                        "approximant W_y(X) = sum_{m | P_y} (mu(m)/sqrt(m)) W_log(X/m) is a prime factor cutoff "
                        "(restricting to squarefree m with P^+(m) <= y, where max divisor is P_y = exp(vartheta(y))). "
                        "For y >= M(X), every squarefree m <= M(X) divides P_y, so the shared head+band terms "
                        "2 <= m <= M(X) cancel in W(X) - W_y(X)."
                    ),
                },
                "h0_autocorrelation_cauchy_schwarz_and_sign_change_audit": h0_audit,
                "controlled_remainder_formula": (
                    "E_{tau,controlled}(K) = -(c_tau^B + 2) h_0(X_K) - W(X_K^{-1}) - W_log(X_K) "
                    "- R_{mu,head}(X_K) - R_{mu,tail}(X_K),   X_K = tau^{|K|} >= 1"
                ),
                "unconditional_component_bounds_over_all_K_in_A_R": {
                    "abs_P_tau_K_bound_certified": serialize_arb_certified(
                        p_tau_0
                    ),
                    "abs_pole_plus_transfer_h0_bound_certified": serialize_arb_certified(
                        B_h0_arb
                    ),
                    "abs_W_inv_XK_bound_certified": serialize_arb_certified(
                        B_refl_arb
                    ),
                    "abs_W_log_XK_bound_certified": serialize_arb_certified(
                        B_log_arb
                    ),
                    "abs_R_mu_head_XK_bound_certified": serialize_arb_certified(
                        B_head_arb
                    ),
                    "abs_R_mu_tail_XK_bound_certified": serialize_arb_certified(
                        B_tail_arb
                    ),
                    "abs_E_tau_controlled_global_bound_certified": serialize_arb_certified(
                        B_ctrl_arb
                    ),
                    "abs_E_tau_controlled_limsup_bound_certified": serialize_arb_certified(
                        B_limsup_arb
                    ),
                },
                "component_bound_provenance_records": {
                    "component_1_pole_plus_transfer_h0": {
                        "expression": "-(c_tau^B + 2) h_0(X_K) = -c_tau^A h_0(X_K)",
                        "domain": "X_K = tau^{|K|} >= 1 (all K in A_R)",
                        "inequality_used": (
                            "Unitary dilation Cauchy-Schwarz on L^2(R_{>0}, dy/y): "
                            "|h_0(X_K)| = |<T_{|K|} psi_tau, psi_tau>_{L^2(dy/y)}| <= ||psi_tau||_{L^2(dy/y)}^2 = h_0(1) "
                            "= 92193 / (512 * 2^{17/2}) = 0.49736248380990124... (note: h_0 changes sign on [1, infty), "
                            "with h_0(2) = -0.217430622... < 0, so the bound uses Cauchy-Schwarz / Bernstein envelope "
                            "|h_0(X_K)| <= (92193/32768)(X_K + X_K^{-1})^{-5/2} <= h_0(1), NOT monotonicity), "
                            "giving global bound B_{h_0} = c_tau^A h_0(1) and large-X_K asymptotic "
                            "h_0(X_K) ~ -(81/64) X_K^{-5/2} = O(X_K^{-5/2}) with |h_0(X_K)| <= (92193/32768) X_K^{-5/2}."
                        ),
                        "provenance": (
                            "Multiplicative autocorrelation Cauchy-Schwarz on L^2(R_{>0}, dy/y) + TASK-TC-040 "
                            "symmetric Bernstein envelope (Lean Theorem 5) + TASK-TC-042F/043 (c_tau^A = c_tau^B + 2)."
                        ),
                        "rounding_direction": "Outward-rounded Arb ball enclosure (.upper() provides certified upper bound).",
                        "bound_certified": serialize_arb_certified(B_h0_arb),
                        "asymptotic_decay_constant_C_h0_certified": serialize_arb_certified(
                            C_h0_decay_arb
                        ),
                    },
                    "component_2_reflected_small_scale_prime_W_inv_XK": {
                        "expression": "-W(X_K^{-1})",
                        "domain": "X_K = tau^{|K|} >= 1 (u = X_K^{-1} in (0, 1])",
                        "inequality_used": (
                            "|W(X_K^{-1})| <= (92193/32768) (sum_{n=2}^infty Lambda(n)/n^3) X_K^{-5/2} <= B_refl "
                            "(computed via prime powers n <= 25000 plus Rosser-Schoenfeld tail 1.558245 / 25000^2)."
                        ),
                        "provenance": "TASK-TC-043 / TASK-TC-044 prime-power cubic tail majorant.",
                        "rounding_direction": "Outward-rounded Arb ball enclosure (.upper() provides certified upper bound).",
                        "bound_certified": serialize_arb_certified(B_refl_arb),
                    },
                    "component_3_divisor_aggregated_W_log_XK": {
                        "expression": "-W_log(X_K)",
                        "domain": "X_K = tau^{|K|} >= 1",
                        "inequality_used": (
                            "Global bound |W_log(X_K)| <= B_log := 30731/98304 + M_{tilde{h},0}^{(-3/2)} + (1/2) M_{tilde{h},log}^{(-3/2)} "
                            "for all X_K >= 1, and large-scale decay |W_log(X_K)| <= C_{log,EM} X_K^{-5/2} for X_K > 0."
                        ),
                        "provenance": "TASK-TC-044 (7-root total-variation global bound) and TASK-TC-049R (Euler-Maclaurin decay constant C_{log,EM}).",
                        "rounding_direction": "Outward-rounded Arb ball enclosure (.upper() provides certified upper bound).",
                        "bound_certified": serialize_arb_certified(B_log_arb),
                        "large_scale_decay_constant_C_log_EM_certified": serialize_arb_certified(
                            C_log_EM_arb
                        ),
                    },
                    "component_4_head_divisor_R_mu_head_XK": {
                        "expression": "-R_{mu,head}(X_K) = -sum_{2 <= m <= H(X_K)} (mu(m)/sqrt(m)) W_log(X_K/m), H(X_K) = floor(X_K^{5/6})",
                        "domain": "X_K = tau^{|K|} >= 1 (empty sum = 0 for 1 <= X_K < 2^{6/5})",
                        "inequality_used": (
                            "|R_{mu,head}(X_K)| <= C_{log,EM} X_K^{-5/2} sum_{2 <= m <= H(X_K)} m^2 "
                            "<= C_{log,EM} X_K^{-5/2} (5/6) H(X_K)^3 <= (5/6) C_{log,EM} =: B_head (proved uniform O(1) bound). "
                            "Note: extending the head to floor(X/2) cannot use |W_log(u)| <= C u^{-5/2} to claim decay because "
                            "X^{-5/2} sum_{2 <= m <= X/2} m^2 = O(X^{1/2}) grows like sqrt(X) (though failure of this unsigned "
                            "majorant does not prove the signed Moebius head sum is unbounded)."
                        ),
                        "provenance": "TASK-TC-049 / TASK-TC-049R (resonant-band head reduction theorem).",
                        "rounding_direction": "Outward-rounded Arb ball enclosure (.upper() provides certified upper bound).",
                        "bound_certified": serialize_arb_certified(B_head_arb),
                    },
                    "component_5_super_scale_tail_R_mu_tail_XK": {
                        "expression": "-R_{mu,tail}(X_K) = -sum_{m > M(X_K)} (mu(m)/sqrt(m)) W_log(X_K/m), M(X_K) = ceil(max(2, X_K^{5/4}))",
                        "domain": "X_K = tau^{|K|} >= 1",
                        "inequality_used": (
                            "|R_{mu,tail}(X_K)| <= C_{log,0} X_K^{5/2} sum_{m > M(X_K)} m^{-3} "
                            "<= C_{log,0} X_K^{5/2} / (2 M(X_K)^2) <= (1/2) C_{log,0} =: B_tail (proved uniform O(1) bound, "
                            "since M(X_K) >= X_K^{5/4} implies X_K^{5/2} / M(X_K)^2 <= 1)."
                        ),
                        "provenance": "TASK-TC-045 (origin bound C_{log,0}) and TASK-TC-049 / TASK-TC-049R (super-scale tail bound).",
                        "rounding_direction": "Outward-rounded Arb ball enclosure (.upper() provides certified upper bound).",
                        "bound_certified": serialize_arb_certified(B_tail_arb),
                        "small_argument_constant_C_log_0_certified": serialize_arb_certified(
                            C_log_0_arb
                        ),
                    },
                },
                "large_grade_asymptotic_behavior_of_E_tau_controlled": (
                    "As |K| -> infty (X_K = tau^{|K|} -> infty): the first three components decay rapidly as "
                    "|(c_tau^B + 2) h_0(X_K)| = O(X_K^{-5/2}) (with h_0(X_K) ~ -(81/64) X_K^{-5/2}), "
                    "|W(X_K^{-1})| = O(X_K^{-5/2}), and |W_log(X_K)| <= C_{log,EM} X_K^{-5/2} = O(X_K^{-5/2}), "
                    "while at the TC-049/TC-049R cutoffs H(X_K) = floor(X_K^{5/6}) and M(X_K) = ceil(max(2, X_K^{5/4})) "
                    "the head and tail satisfy the proved uniform O(1) bounds |R_{mu,head}(X_K)| <= (5/6) C_{log,EM} "
                    "and |R_{mu,tail}(X_K)| <= (1/2) C_{log,0}. Consequently, sup_{K in A_R} |E_{tau,controlled}(K)| <= B_ctrl < 17.987140 "
                    "and limsup_{|K|->infty} |E_{tau,controlled}(K)| <= (5/6) C_{log,EM} + (1/2) C_{log,0} < 11.502478 "
                    "(establishing o(1) decay of R_{mu,head} would require cancellation or a strictly smaller exponent < 5/6, "
                    "and o(1) decay of R_{mu,tail} requires a cutoff growing faster than X_K^{5/4})."
                ),
                "observable_radius_summary_across_13_sample_grades": observable_radius_summary,
                "all_orbit_reconstructions_enclose_zero": all_orbit_identities_enclose_zero,
                "all_independent_tail_bounds_verified": all_independent_tail_bounds_verified,
                "all_component_bounds_verified": all_component_bounds_verified,
                "certified_grade_orbit_table": orbit_rows,
            },
            "parallel_connes_consani_hilbert_schmidt_compressions": {
                "half_line_projection_orbit_B_0_Sigma": (
                    "B_0^Sigma := theta(tilde{psi}_tau)^* P P_hat in HS(L^2(R)_{ev}) gives "
                    "P_tau^Sigma(K) = <U_K B_0^Sigma, B_0^Sigma>_{HS} = Tr(theta(h_K) P P_hat) and "
                    "W_arch(h_K) = P_tau^Sigma(K) - D_tau(K), where D_tau(K) is the archimedean trace defect."
                ),
                "sonin_projection_orbit_B_0_Sonin": (
                    "B_0^Sonin := theta(tilde{psi}_tau)^* S in HS(L^2(R)_{ev}) (where S projects onto "
                    "Sonin's space) gives P_tau^Sonin(K) = <U_K B_0^Sonin, B_0^Sonin>_{HS} = Tr(theta(h_K) S) "
                    "and W_arch(h_K) = P_tau^Sonin(K) - E_{tau,prolate}(K)."
                ),
            },
        }
    finally:
        flint_ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# 5. Section 7 (TASK-TC-051): Exact Prime-Separation Identity, Canonical
#    Rescaled-Band Boundary Theorem, Summation by Parts, and Sign Discrimination
# ---------------------------------------------------------------------------


def _interval_integer_bounds(A: arb, B: arb) -> Tuple[int, int]:
    """Return integer endpoints (m_start, m_end) such that m in (A, B] iff m_start <= m <= m_end,
    where A >= 0 and B >= A are real interval endpoints."""
    a_floor = A.floor().unique_fmpz()
    b_floor = B.floor().unique_fmpz()
    if a_floor is None or b_floor is None:
        raise RuntimeError(
            f"Interval endpoint straddles an integer in (A, B] = ({A}, {B}]"
        )
    m_start = max(1, int(a_floor) + 1)
    m_end = int(b_floor)
    return m_start, m_end


def evaluate_R_interval_arb(
    X: arb, A: arb, B: arb, prec_bits: int = 256
) -> arb:
    """Evaluate R(X; A, B) := sum_{A < m <= B} (mu(m) / sqrt(m)) W_log(X / m) in 256-bit Arb."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        X_a = arb(X)
        m_start, m_end = _interval_integer_bounds(arb(A), arb(B))
        acc = arb(0)
        for m in range(m_start, m_end + 1):
            mu_m = moebius_mu_int(m)
            if mu_m == 0:
                continue
            m_a = arb(m)
            acc += (arb(mu_m) / m_a.sqrt()) * evaluate_W_log_em4_certified_arb(
                X_a / m_a, prec_bits=prec_bits
            )
        return acc
    finally:
        flint_ctx.prec = saved_prec


def evaluate_S_p_interval_arb(
    X: arb, A: arb, B: arb, p: int, prec_bits: int = 256
) -> arb:
    """Evaluate the p-coprime partial sum
        S_p(X; A, B) := sum_{A < m <= B, p nmid m} (mu(m) / sqrt(m)) W_log(X / m)
    in 256-bit Arb."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        X_a = arb(X)
        m_start, m_end = _interval_integer_bounds(arb(A), arb(B))
        acc = arb(0)
        for m in range(m_start, m_end + 1):
            if m % p == 0:
                continue
            mu_m = moebius_mu_int(m)
            if mu_m == 0:
                continue
            m_a = arb(m)
            acc += (arb(mu_m) / m_a.sqrt()) * evaluate_W_log_em4_certified_arb(
                X_a / m_a, prec_bits=prec_bits
            )
        return acc
    finally:
        flint_ctx.prec = saved_prec


def evaluate_S_prime_set_interval_arb(
    X: arb, A: arb, B: arb, primes: List[int], prec_bits: int = 256
) -> arb:
    """Evaluate the multi-prime coprime partial sum
        S_P(X; A, B) := sum_{A < m <= B, gcd(m, prod_{p in P} p) = 1} (mu(m) / sqrt(m)) W_log(X / m)
    in 256-bit Arb."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        X_a = arb(X)
        m_start, m_end = _interval_integer_bounds(arb(A), arb(B))
        acc = arb(0)
        for m in range(m_start, m_end + 1):
            if any(m % p == 0 for p in primes):
                continue
            mu_m = moebius_mu_int(m)
            if mu_m == 0:
                continue
            m_a = arb(m)
            acc += (arb(mu_m) / m_a.sqrt()) * evaluate_W_log_em4_certified_arb(
                X_a / m_a, prec_bits=prec_bits
            )
        return acc
    finally:
        flint_ctx.prec = saved_prec


def verify_prime_separation_identity_and_canonical_band_boundary_arb(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Certify in SymPy and 256-bit Arb:
      1. Exact Prime-Separation Identity (Requirement 3):
             R(X; A, B) = S_p(X; A, B) - p^{-1/2} S_p(X / p; A / p, B / p)
         for all X > 0, 0 <= A < B, and prime p, accounting explicitly for the squarefree
         support of mu: partitioning m in (A, B] into p nmid m and m = p d (d in (A/p, B/p]),
         terms with p | d (i.e., p^2 | m) have mu(p d) = 0, while terms with p nmid d have
         mu(p d) = -mu(d) and (p d)^{-1/2} = p^{-1/2} d^{-1/2}.
      2. Canonical Rescaled-Band Decomposition & Unconditional Uniform Boundary Bound:
         With S_{p,band}(Y) := S_p(Y; H(Y), M(Y)) for Y >= 1 and 0 for 0 < Y < 1,
             R_{mu,band}(X) = S_{p,band}(X) - p^{-1/2} S_{p,band}(X / p) - p^{-1/2} B_p(X),
         where the rescaled-cutoff boundary discrepancy
             B_p(X) := S_p(X / p; H(X) / p, M(X) / p) - S_{p,band}(X / p)
                     = Delta_{p,low}(X) + Delta_{p,high}(X)
         satisfies the unconditional uniform bound across ALL X >= 1 and ALL primes p:
             |B_p(X)| <= B_rescaled := B_log + (5/6) C_{log,EM} + (1/2) C_{log,0}
                      <= 14.85148509 < 14.851486,
         and for H(X) >= p (where d = 1 is outside (H(X)/p, H(X/p)]):
             |B_p(X)| <= B_head + B_tail = (5/6) C_{log,EM} + (1/2) C_{log,0}
                      <= 11.50247707 < 11.502478,
         while for 1 <= X < p (where X / p < 1 and S_{p,band}(X / p) = 0):
             |B_p(X)| = |S_p(X / p; H(X) / p, M(X) / p)|
                      <= zeta(3) C_{log,0} (X / p)^{5/2} <= zeta(3) C_{log,0} < 0.670063.
      3. Iterated Prime-Power Tower & Two-Way Coprime Band Equivalence:
             S_{p,band}(X) = sum_{j=0}^{floor(log_p X)} p^{-j/2} (R_{mu,band}(X / p^j) + p^{-1/2} B_p(X / p^j)),
         proving unconditionally that for any fixed prime p (e.g. p = 2, odd squarefree integers):
             sup_{X >= 1} |R_{mu,band}(X)| < infty  <==>  sup_{X >= 1} |S_{p,band}(X)| < infty.
      4. Multi-Prime Inclusion-Exclusion & Tautological Sieve Collapse Obstruction:
             R(X; A, B) = sum_{d | P_P} (mu(d) / sqrt(d)) S_P(X / d; A / d, B / d).
         When P = {p <= M(X)} sieves all primes up to M(X), the only integer coprime to P_P in
         [1, M(X)/d] is k = 1, so S_P(X/d; H(X)/d, M(X)/d) = 1_{H(X) < d <= M(X)} W_log(X/d)
         and the expansion collapses tautologically back to R_{mu,band}(X); meanwhile, taking
         absolute values across d | P_P multiplies by prod_{p in P} (1 + p^{-1/2}) -> infty.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        pi_arb = arb.pi()
        tau_arb = arb(2) * pi_arb

        live_bounds = _compute_live_controlled_component_bounds_arb(
            prec_bits=prec_bits
        )
        B_log_arb = live_bounds["B_log_arb"]
        C_log_EM_arb = live_bounds["C_log_EM_arb"]
        C_log_0_arb = live_bounds["C_log_0_arb"]
        B_head_arb = live_bounds["B_head_arb"]
        B_tail_arb = live_bounds["B_tail_arb"]
        B_rescaled_arb = B_log_arb + B_head_arb + B_tail_arb
        B_rescaled_large_X_arb = B_head_arb + B_tail_arb
        zeta3_arb = acb(3).zeta().real
        B_subunit_arb = zeta3_arb * C_log_0_arb

        # 1. Verify exact single-prime separation and canonical band boundary across scales and primes
        sample_scales: List[Tuple[str, arb]] = [
            ("1", arb(1)),
            ("2", arb(2)),
            ("4", arb(4)),
            ("tau", tau_arb),
            ("10", arb(10)),
            ("16", arb(16)),
            ("tau^2", tau_arb * tau_arb),
        ]
        test_primes = [2, 3, 5, 7]
        band_prime_rows: List[Dict[str, Any]] = []
        all_prime_sep_enclose_zero = True
        all_canonical_band_sep_enclose_zero = True
        all_boundary_bounds_certified = True
        all_p_squared_obstructions_detected = True
        both_upper_cutoff_orderings_certified = True

        for x_label, x_a in sample_scales:
            H_x = certified_head_cutoff_H_X_arb(x_a, prec_bits=prec_bits)
            M_x = certified_coupled_cutoff_M_X_arb(x_a, prec_bits=prec_bits)
            A_a = arb(H_x)
            B_a = arb(M_x)
            R_band = evaluate_R_interval_arb(x_a, A_a, B_a, prec_bits=prec_bits)

            for p in test_primes:
                p_a = arb(p)
                inv_sqrt_p = arb(1) / p_a.sqrt()
                x_over_p = x_a / p_a
                A_over_p = A_a / p_a
                B_over_p = B_a / p_a

                S_p_band_X = evaluate_S_p_interval_arb(
                    x_a, A_a, B_a, p, prec_bits=prec_bits
                )
                S_p_rescaled = evaluate_S_p_interval_arb(
                    x_over_p, A_over_p, B_over_p, p, prec_bits=prec_bits
                )
                sep_rhs = S_p_band_X - inv_sqrt_p * S_p_rescaled
                sep_diff = R_band - sep_rhs
                sep_ok = bool(sep_diff.contains(0))
                if not sep_ok:
                    all_prime_sep_enclose_zero = False

                # Check what happens if p^2 | m exclusion (p nmid d in second term) is omitted:
                R_unfiltered_rescaled = evaluate_R_interval_arb(
                    x_over_p, A_over_p, B_over_p, prec_bits=prec_bits
                )
                omitted_p_sq_rhs = S_p_band_X - inv_sqrt_p * R_unfiltered_rescaled
                omitted_p_sq_err = R_band - omitted_p_sq_rhs
                has_p_sq_in_band = any(
                    (m % (p * p) == 0) and (moebius_mu_int(m // p) != 0)
                    for m in range(H_x + 1, M_x + 1)
                )
                if has_p_sq_in_band and bool(omitted_p_sq_err.contains(0)):
                    all_p_squared_obstructions_detected = False

                # Canonical rescaled band at Y = X / p:
                x_ge_p = bool((x_over_p - arb(1)).lower() >= arb(0))
                if x_ge_p:
                    H_xp = certified_head_cutoff_H_X_arb(
                        x_over_p, prec_bits=prec_bits
                    )
                    M_xp = certified_coupled_cutoff_M_X_arb(
                        x_over_p, prec_bits=prec_bits
                    )
                    S_p_band_xp = evaluate_S_p_interval_arb(
                        x_over_p, arb(H_xp), arb(M_xp), p, prec_bits=prec_bits
                    )
                    # Explicit lower boundary sum over H(X)/p < d <= H(X/p), p nmid d:
                    delta_low = evaluate_S_p_interval_arb(
                        x_over_p, A_over_p, arb(H_xp), p, prec_bits=prec_bits
                    )
                    # Explicit upper boundary sum over M(X/p) < d <= M(X)/p minus M(X)/p < d <= M(X/p), p nmid d:
                    delta_high = evaluate_S_p_interval_arb(
                        x_over_p, arb(M_xp), B_over_p, p, prec_bits=prec_bits
                    ) - evaluate_S_p_interval_arb(
                        x_over_p, B_over_p, arb(M_xp), p, prec_bits=prec_bits
                    )
                    B_p_val = delta_low + delta_high
                    if M_x >= p * M_xp:
                        upper_ordering = "M(X)/p >= M(X/p)"
                    else:
                        upper_ordering = (
                            "M(X)/p < M(X/p) (single-endpoint regime N - 1 < M(X)/p < N)"
                        )
                    high_cert = certify_abs_le_bound_arb(delta_high, B_tail_arb)
                    if not high_cert["certified"]:
                        both_upper_cutoff_orderings_certified = False
                        all_boundary_bounds_certified = False
                else:
                    H_xp = 0
                    M_xp = 0
                    S_p_band_xp = arb(0)
                    delta_low = S_p_rescaled
                    delta_high = arb(0)
                    B_p_val = S_p_rescaled
                    upper_ordering = "X/p < 1 (sub-unit regime)"

                canon_rhs = (
                    S_p_band_X
                    - inv_sqrt_p * S_p_band_xp
                    - inv_sqrt_p * B_p_val
                )
                canon_diff = R_band - canon_rhs
                canon_ok = bool(canon_diff.contains(0))
                if not canon_ok:
                    all_canonical_band_sep_enclose_zero = False

                bdry_cert = certify_abs_le_bound_arb(B_p_val, B_rescaled_arb)
                if not bdry_cert["certified"]:
                    all_boundary_bounds_certified = False

                if H_x >= p and x_ge_p:
                    large_cert = certify_abs_le_bound_arb(
                        B_p_val, B_rescaled_large_X_arb
                    )
                    if not large_cert["certified"]:
                        all_boundary_bounds_certified = False
                if not x_ge_p:
                    sub_bound = B_subunit_arb * (x_over_p ** arb("2.5"))
                    sub_cert = certify_abs_le_bound_arb(B_p_val, sub_bound)
                    if not sub_cert["certified"]:
                        all_boundary_bounds_certified = False

                if p in (2, 3) and x_label in ("1", "2", "tau", "16", "tau^2"):
                    band_prime_rows.append(
                        {
                            "X_label": x_label,
                            "prime_p": p,
                            "H_X": H_x,
                            "M_X": M_x,
                            "X_over_p_ge_1": x_ge_p,
                            "H_X_over_p": H_xp,
                            "M_X_over_p": M_xp,
                            "upper_cutoff_ordering": upper_ordering,
                            "R_mu_band_X_certified": serialize_arb_certified(
                                R_band
                            ),
                            "S_p_band_X_certified": serialize_arb_certified(
                                S_p_band_X
                            ),
                            "S_p_rescaled_certified": serialize_arb_certified(
                                S_p_rescaled
                            ),
                            "S_p_band_X_over_p_certified": serialize_arb_certified(
                                S_p_band_xp
                            ),
                            "Delta_p_low_certified": serialize_arb_certified(
                                delta_low
                            ),
                            "Delta_p_high_certified": serialize_arb_certified(
                                delta_high
                            ),
                            "B_p_X_boundary_certified": serialize_arb_certified(
                                B_p_val
                            ),
                            "prime_sep_identity_encloses_zero": sep_ok,
                            "canonical_band_sep_encloses_zero": canon_ok,
                            "abs_B_p_le_B_rescaled_certified": bdry_cert[
                                "certified"
                            ],
                            "has_p_squared_multiple_in_band": has_p_sq_in_band,
                            "omitted_p_squared_error_nonzero_certified": (
                                not bool(omitted_p_sq_err.contains(0))
                                if has_p_sq_in_band
                                else False
                            ),
                        }
                    )

        # Explicit single-endpoint upper-cutoff ordering checks (N - 1 < M(X)/p < N := M(Y)):
        # (a) At X = 2, p = 2: Y = X/p = 1, M(2) = 3, M(2)/2 = 3/2 < 2 = M(1) = N, so (M(2)/2, M(1)] = (3/2, 2]
        #     contains only the single integer endpoint d = N = 2 (annihilated by 2 | d, with unfiltered
        #     magnitude 2^{-1/2} |W_log(1/2)| <= (1/2) C_{log,0} = B_tail).
        single_ep_d2_term = (arb(1) / arb(2).sqrt()) * abs(
            evaluate_W_log_em4_certified_arb(arb("0.5"), prec_bits=prec_bits)
        )
        single_ep_d2_cert = certify_abs_le_bound_arb(
            single_ep_d2_term, B_tail_arb
        )
        if not single_ep_d2_cert["certified"]:
            both_upper_cutoff_orderings_certified = False

        # (b) At X = 18/5 = 3.6, p = 2: Y = X/p = 9/5 = 1.8.
        #     Exact integer powers give 4^4 = 256 < (18/5)^5 = 1889568/3125 = 604.66176 <= 625 = 5^4 => M(18/5) = 5,
        #     2^6 = 64 <= (18/5)^5 < 729 = 3^6 => H(18/5) = 2, and
        #     2^4 = 16 < (9/5)^5 = 59049/3125 = 18.89568 <= 81 = 3^4 => N = M(9/5) = 3, H(9/5) = 1.
        #     Thus N - 1 = 2 < M(X)/p = 5/2 = 2.5 < 3 = N = M(Y), and the omitted interval (5/2, 3]
        #     contains only the single integer endpoint d = N = 3, which satisfies 2 nmid 3 and therefore
        #     survives the coprime filter:
        #         Delta_{2,high}(18/5) = -S_2(9/5; 5/2, 3) = -(mu(3)/sqrt(3)) W_log(3/5) = +(1/sqrt(3)) W_log(3/5) != 0,
        #     satisfying |Delta_{2,high}(18/5)| <= C_{log,0} Y^{5/2} / N^3 <= (1/2) C_{log,0} = B_tail.
        x_18_5 = arb(18) / arb(5)
        y_9_5 = arb(9) / arb(5)
        H_18_5 = certified_head_cutoff_H_X_arb(x_18_5, prec_bits=prec_bits)
        M_18_5 = certified_coupled_cutoff_M_X_arb(x_18_5, prec_bits=prec_bits)
        H_9_5 = certified_head_cutoff_H_X_arb(y_9_5, prec_bits=prec_bits)
        M_9_5 = certified_coupled_cutoff_M_X_arb(y_9_5, prec_bits=prec_bits)
        R_band_18_5 = evaluate_R_interval_arb(
            x_18_5, arb(H_18_5), arb(M_18_5), prec_bits=prec_bits
        )
        S2_band_18_5 = evaluate_S_p_interval_arb(
            x_18_5, arb(H_18_5), arb(M_18_5), 2, prec_bits=prec_bits
        )
        S2_band_9_5 = evaluate_S_p_interval_arb(
            y_9_5, arb(H_9_5), arb(M_9_5), 2, prec_bits=prec_bits
        )
        delta_low_18_5 = evaluate_S_p_interval_arb(
            y_9_5, arb(H_18_5) / arb(2), arb(H_9_5), 2, prec_bits=prec_bits
        )
        delta_high_18_5 = evaluate_S_p_interval_arb(
            y_9_5, arb(M_9_5), arb(M_18_5) / arb(2), 2, prec_bits=prec_bits
        ) - evaluate_S_p_interval_arb(
            y_9_5, arb(M_18_5) / arb(2), arb(M_9_5), 2, prec_bits=prec_bits
        )
        expected_delta_high_18_5 = (arb(1) / arb(3).sqrt()) * evaluate_W_log_em4_certified_arb(
            arb(3) / arb(5), prec_bits=prec_bits
        )
        delta_high_18_5_matches_d3 = bool(
            (delta_high_18_5 - expected_delta_high_18_5).contains(0)
        )
        delta_high_18_5_nonzero = not bool(delta_high_18_5.contains(0))
        sharp_n3_bound_18_5 = (
            C_log_0_arb * (y_9_5 ** arb("2.5")) / (arb(M_9_5) ** arb(3))
        )
        cert_18_5_sharp = certify_abs_le_bound_arb(
            delta_high_18_5, sharp_n3_bound_18_5
        )
        cert_18_5_tail = certify_abs_le_bound_arb(delta_high_18_5, B_tail_arb)
        B2_18_5 = delta_low_18_5 + delta_high_18_5
        canon_sep_18_5_ok = bool(
            (
                R_band_18_5
                - (
                    S2_band_18_5
                    - (arb(1) / arb(2).sqrt()) * S2_band_9_5
                    - (arb(1) / arb(2).sqrt()) * B2_18_5
                )
            ).contains(0)
        )
        cert_18_5_rescaled = certify_abs_le_bound_arb(B2_18_5, B_rescaled_arb)
        if not (
            H_18_5 == 2
            and M_18_5 == 5
            and H_9_5 == 1
            and M_9_5 == 3
            and delta_high_18_5_matches_d3
            and delta_high_18_5_nonzero
            and cert_18_5_sharp["certified"]
            and cert_18_5_tail["certified"]
            and canon_sep_18_5_ok
            and cert_18_5_rescaled["certified"]
        ):
            both_upper_cutoff_orderings_certified = False

        # 2. Verify iterated single-prime tower telescoping (both arbitrary-interval rescaled tower
        #    S_0 = sum_{j=0}^{L-1} q^j R_j + q^L S_L and canonical-band tower
        #    S_{p,band}(X) = sum_{j=0}^{L-1} q^j (R_{mu,band}(X/p^j) + q B_p(X/p^j)) + q^L S_{p,band}(X/p^L))
        #    at L = 1, L = 2, and terminal L for p = 2 and p = 3 at X = tau^2:
        tower_checks: List[Dict[str, Any]] = []
        all_tower_telescoping_enclose_zero = True
        x_tower = tau_arb * tau_arb
        for p in (2, 3):
            p_a = arb(p)
            q_a = arb(1) / p_a.sqrt()
            H_top = certified_head_cutoff_H_X_arb(x_tower, prec_bits=prec_bits)
            M_top = certified_coupled_cutoff_M_X_arb(x_tower, prec_bits=prec_bits)
            A_top = arb(H_top)
            B_top = arb(M_top)
            S_p_top = evaluate_S_p_interval_arb(
                x_tower, A_top, B_top, p, prec_bits=prec_bits
            )

            # (2a) Simultaneously rescaled arbitrary-interval tower:
            #      R_j := R(X/p^j; A/p^j, B/p^j), S_j := S_p(X/p^j; A/p^j, B/p^j),
            #      R_j = S_j - q S_{j+1}, S_0 = sum_{j=0}^{L-1} q^j R_j + q^L S_L.
            R_rescaled_list: List[arb] = []
            S_rescaled_list: List[arb] = []
            j_res = 0
            while True:
                p_pow = p_a ** arb(j_res)
                Sj = evaluate_S_p_interval_arb(
                    x_tower / p_pow,
                    A_top / p_pow,
                    B_top / p_pow,
                    p,
                    prec_bits=prec_bits,
                )
                Rj = evaluate_R_interval_arb(
                    x_tower / p_pow,
                    A_top / p_pow,
                    B_top / p_pow,
                    prec_bits=prec_bits,
                )
                S_rescaled_list.append(Sj)
                R_rescaled_list.append(Rj)
                if bool(((B_top / p_pow) - arb(1)).upper() < arb(0)):
                    break
                j_res += 1

            L_res_terminal = len(R_rescaled_list) - 1
            rescaled_L1_rhs = R_rescaled_list[0] + q_a * S_rescaled_list[1]
            rescaled_L2_rhs = (
                R_rescaled_list[0]
                + q_a * R_rescaled_list[1]
                + (q_a ** arb(2)) * S_rescaled_list[2]
            )
            rescaled_term_rhs = arb(0)
            for j_idx in range(L_res_terminal):
                rescaled_term_rhs += (q_a ** arb(j_idx)) * R_rescaled_list[j_idx]
            rescaled_L1_ok = bool((S_p_top - rescaled_L1_rhs).contains(0))
            rescaled_L2_ok = bool((S_p_top - rescaled_L2_rhs).contains(0))
            rescaled_term_ok = bool((S_p_top - rescaled_term_rhs).contains(0)) and bool(
                S_rescaled_list[L_res_terminal].contains(0)
            )

            # (2b) Canonical-band tower:
            #      S_{p,band}(X) = sum_{j=0}^{L-1} q^j (R_{mu,band}(X/p^j) + q B_p(X/p^j)) + q^L S_{p,band}(X/p^L),
            #      terminating at L = floor(log_p X) + 1 where X/p^L < 1 => S_{p,band}(X/p^L) = 0 by definition.
            telescoped_sum = arb(0)
            canon_step_terms: List[arb] = []
            canon_S_bands: List[arb] = [S_p_top]
            y_cur = x_tower
            j_step = 0
            while bool((y_cur - arb(1)).lower() >= arb(0)):
                H_y = certified_head_cutoff_H_X_arb(y_cur, prec_bits=prec_bits)
                M_y = certified_coupled_cutoff_M_X_arb(y_cur, prec_bits=prec_bits)
                R_y = evaluate_R_interval_arb(
                    y_cur, arb(H_y), arb(M_y), prec_bits=prec_bits
                )
                y_next = y_cur / p_a
                S_res_y = evaluate_S_p_interval_arb(
                    y_next, arb(H_y) / p_a, arb(M_y) / p_a, p, prec_bits=prec_bits
                )
                if bool((y_next - arb(1)).lower() >= arb(0)):
                    H_yn = certified_head_cutoff_H_X_arb(
                        y_next, prec_bits=prec_bits
                    )
                    M_yn = certified_coupled_cutoff_M_X_arb(
                        y_next, prec_bits=prec_bits
                    )
                    S_band_yn = evaluate_S_p_interval_arb(
                        y_next, arb(H_yn), arb(M_yn), p, prec_bits=prec_bits
                    )
                else:
                    S_band_yn = arb(0)
                B_y = S_res_y - S_band_yn
                step_term = R_y + q_a * B_y
                canon_step_terms.append(step_term)
                canon_S_bands.append(S_band_yn)
                telescoped_sum += (q_a ** arb(j_step)) * step_term
                y_cur = y_next
                j_step += 1

            canon_L1_rhs = canon_step_terms[0] + q_a * canon_S_bands[1]
            canon_L2_rhs = (
                canon_step_terms[0]
                + q_a * canon_step_terms[1]
                + (q_a ** arb(2)) * canon_S_bands[2]
            )
            canon_L1_ok = bool((S_p_top - canon_L1_rhs).contains(0))
            canon_L2_ok = bool((S_p_top - canon_L2_rhs).contains(0))
            tower_diff = S_p_top - telescoped_sum
            tower_ok = (
                bool(tower_diff.contains(0))
                and rescaled_L1_ok
                and rescaled_L2_ok
                and rescaled_term_ok
                and canon_L1_ok
                and canon_L2_ok
            )
            if not tower_ok:
                all_tower_telescoping_enclose_zero = False
            tower_checks.append(
                {
                    "X_label": "tau^2",
                    "prime_p": p,
                    "canonical_band_steps_J_p_plus_1": j_step,
                    "rescaled_interval_terminal_L": L_res_terminal,
                    "S_p_band_X_certified": serialize_arb_certified(S_p_top),
                    "telescoped_tower_sum_certified": serialize_arb_certified(
                        telescoped_sum
                    ),
                    "rescaled_interval_L1_encloses_zero": rescaled_L1_ok,
                    "rescaled_interval_L2_encloses_zero": rescaled_L2_ok,
                    "rescaled_interval_terminal_encloses_zero": rescaled_term_ok,
                    "canonical_band_L1_encloses_zero": canon_L1_ok,
                    "canonical_band_L2_encloses_zero": canon_L2_ok,
                    "tower_diff_encloses_zero": tower_ok,
                }
            )

        # 3. Verify multi-prime inclusion-exclusion, P = 2 orientation regression, and tautological sieve collapse:
        #   (a) Orientation regression at P = 2, X = 1, (A, B] = (1, 2]:
        #       R(1; 1, 2) = -2^{-1/2} W_log(1/2), S_2(1; 1, 2) = 0, S_2(1/2; 1/2, 1) = W_log(1/2).
        #       Rightly oriented formula: sum_{d | 2} (mu(d)/sqrt(d)) S_2(1/d; 1/d, 2/d) = -2^{-1/2} W_log(1/2) = R(1; 1, 2).
        #       Reversed formula: sum_{d | 2} (mu(d)/sqrt(d)) R(1/d; 1/d, 2/d) = -sqrt(2) W_log(1/2) != 0 = S_2(1; 1, 2).
        R_1_1_2 = evaluate_R_interval_arb(
            arb(1), arb(1), arb(2), prec_bits=prec_bits
        )
        S2_1_1_2 = evaluate_S_p_interval_arb(
            arb(1), arb(1), arb(2), 2, prec_bits=prec_bits
        )
        S2_half_half_1 = evaluate_S_p_interval_arb(
            arb("0.5"), arb("0.5"), arb(1), 2, prec_bits=prec_bits
        )
        R_half_half_1 = evaluate_R_interval_arb(
            arb("0.5"), arb("0.5"), arb(1), prec_bits=prec_bits
        )
        inv_sqrt2 = arb(1) / arb(2).sqrt()
        correct_mp_p2_rhs = S2_1_1_2 - inv_sqrt2 * S2_half_half_1
        reversed_mp_p2_rhs = R_1_1_2 - inv_sqrt2 * R_half_half_1
        p2_correct_orientation_encloses_zero = bool(
            (R_1_1_2 - correct_mp_p2_rhs).contains(0)
        )
        p2_reversed_formula_discrepancy = S2_1_1_2 - reversed_mp_p2_rhs
        p2_reversed_formula_detected_nonzero = not bool(
            p2_reversed_formula_discrepancy.contains(0)
        )

        #   (b) At X = 16, H(16) = 10, M(16) = 32:
        #       For P = {2, 3, 5}, R(16; 10, 32) = sum_{d | 30} (mu(d)/sqrt(d)) S_{2,3,5}(16/d; 10/d, 32/d).
        #   (c) For P = {p <= 32} (all 11 primes <= M(16)), every integer k in (10/d, 32/d] coprime to P_P
        #       has k = 1 (which lies in (10/d, 32/d] iff 10 < d <= 32), so
        #       S_P(16/d; 10/d, 32/d) = 1_{10 < d <= 32} W_log(16/d), collapsing tautologically back to R_{mu,band}(16)!
        X_mp = arb(16)
        A_mp = arb(10)
        B_mp = arb(32)
        R_16_band = evaluate_R_interval_arb(X_mp, A_mp, B_mp, prec_bits=prec_bits)
        primes_3 = [2, 3, 5]
        divs_30 = [
            (1, 1),
            (2, -1),
            (3, -1),
            (5, -1),
            (6, 1),
            (10, 1),
            (15, 1),
            (30, -1),
        ]
        mp_3_rhs = arb(0)
        for d_i, mu_d in divs_30:
            d_a = arb(d_i)
            mp_3_rhs += (
                arb(mu_d) / d_a.sqrt()
            ) * evaluate_S_prime_set_interval_arb(
                X_mp / d_a, A_mp / d_a, B_mp / d_a, primes_3, prec_bits=prec_bits
            )
        mp_3_diff = R_16_band - mp_3_rhs
        mp_3_encloses_zero = bool(mp_3_diff.contains(0))

        primes_to_32 = primes_up_to(32)
        tautological_collapse_all_match = True
        for d_i in range(1, 35):
            if moebius_mu_int(d_i) == 0:
                continue
            d_a = arb(d_i)
            s_full_sieve = evaluate_S_prime_set_interval_arb(
                X_mp / d_a,
                A_mp / d_a,
                B_mp / d_a,
                primes_to_32,
                prec_bits=prec_bits,
            )
            expected_single = (
                evaluate_W_log_em4_certified_arb(X_mp / d_a, prec_bits=prec_bits)
                if (10 < d_i <= 32)
                else arb(0)
            )
            if not bool((s_full_sieve - expected_single).contains(0)):
                tautological_collapse_all_match = False

        # Euler product norm blow-up prod_{p <= y} (1 + p^{-1/2}) across y in {5, 13, 31, 97, 997}:
        euler_factor_growth: List[Dict[str, Any]] = []
        for y_cut in (5, 13, 31, 97, 997):
            prod_val = arb(1)
            for p_i in primes_up_to(y_cut):
                prod_val *= arb(1) + arb(1) / arb(p_i).sqrt()
            euler_factor_growth.append(
                {
                    "y_prime_cutoff": y_cut,
                    "prime_count_pi_y": len(primes_up_to(y_cut)),
                    "prod_1_plus_p_neg_half_certified": serialize_arb_certified(
                        prod_val
                    ),
                }
            )

        return {
            "exact_prime_separation_identity": (
                "R(X; A, B) = S_p(X; A, B) - p^{-1/2} S_p(X / p; A / p, B / p)   "
                "(for all X > 0, 0 <= A < B, and prime p in P, using mu(p d) = 0 for p | d and mu(p d) = -mu(d) for p nmid d)"
            ),
            "rescaled_interval_inverse_tower_identity": (
                "For R_j := R(X/p^j; A/p^j, B/p^j) and S_j := S_p(X/p^j; A/p^j, B/p^j) with q = p^{-1/2}, "
                "R_j = S_j - q S_{j+1} and S_0 = sum_{j=0}^{L-1} q^j R_j + q^L S_L for every L >= 1, "
                "terminating when B/p^L < 1 so S_L = 0."
            ),
            "canonical_rescaled_band_identity": (
                "R_{mu,band}(X) = S_{p,band}(X) - p^{-1/2} S_{p,band}(X / p) - p^{-1/2} B_p(X),   "
                "where B_p(X) = Delta_{p,low}(X) + Delta_{p,high}(X) is the rescaled cutoff boundary sum, "
                "and S_{p,band}(X) = sum_{j=0}^{L-1} q^j (R_{mu,band}(X/p^j) + q B_p(X/p^j)) + q^L S_{p,band}(X/p^L) "
                "holds for 1 <= L <= floor(log_p X) + 1 and terminates at L = floor(log_p X) + 1 where X/p^L < 1 so S_{p,band}(X/p^L) = 0 by definition."
            ),
            "unconditional_rescaled_boundary_bounds": {
                "B_rescaled_global_all_X_ge_1_and_all_p_certified": serialize_arb_certified(
                    B_rescaled_arb
                ),
                "B_rescaled_global_rational_ceiling": "14851486 / 1000000 = 14.851486",
                "B_rescaled_large_X_when_H_X_ge_p_certified": serialize_arb_certified(
                    B_rescaled_large_X_arb
                ),
                "B_rescaled_large_X_rational_ceiling": "11502478 / 1000000 = 11.502478",
                "B_subunit_when_X_lt_p_coeff_zeta3_C_log_0_certified": serialize_arb_certified(
                    B_subunit_arb
                ),
                "both_upper_cutoff_orderings_certified": both_upper_cutoff_orderings_certified,
                "small_Y_single_endpoint_regime_X2_p2": {
                    "X": 2,
                    "p": 2,
                    "Y_equals_X_over_p": 1,
                    "M_X": 3,
                    "M_X_over_p_ratio": "3/2 = 1.5",
                    "M_Y": 2,
                    "interval_M_X_over_p_to_M_Y": "(3/2, 2] containing only integer d = M(1) = 2 (filtered out by 2 nmid d)",
                    "single_endpoint_unfiltered_term_2_neg_half_abs_W_log_half_certified": serialize_arb_certified(
                        single_ep_d2_term
                    ),
                    "single_endpoint_le_B_tail_certified": single_ep_d2_cert[
                        "certified"
                    ],
                },
                "single_endpoint_coprime_surviving_regime_X_18_5_p2": {
                    "X": "18/5 = 3.6",
                    "p": 2,
                    "Y_equals_X_over_p": "9/5 = 1.8",
                    "H_X": H_18_5,
                    "M_X": M_18_5,
                    "H_Y": H_9_5,
                    "M_Y": M_9_5,
                    "M_X_over_p_ratio": "5/2 = 2.5",
                    "single_endpoint_inequality": "N - 1 = 2 < M(X)/p = 5/2 < 3 = N := M(Y)",
                    "interval_M_X_over_p_to_M_Y": "(5/2, 3] containing only integer d = M(9/5) = 3, which survives the coprime filter 2 nmid d",
                    "delta_high_certified": serialize_arb_certified(delta_high_18_5),
                    "single_endpoint_term_plus_3_neg_half_W_log_3_5_certified": serialize_arb_certified(
                        expected_delta_high_18_5
                    ),
                    "delta_high_minus_single_endpoint_term_certified": serialize_arb_certified(
                        delta_high_18_5 - expected_delta_high_18_5
                    ),
                    "delta_high_matches_single_endpoint_encloses_zero": delta_high_18_5_matches_d3,
                    "delta_high_nonzero_certified": delta_high_18_5_nonzero,
                    "abs_delta_high_certified": serialize_arb_certified(
                        abs(delta_high_18_5)
                    ),
                    "analytic_single_endpoint_bound_C_log_0_Y_5_2_over_N3_certified": serialize_arb_certified(
                        sharp_n3_bound_18_5
                    ),
                    "abs_delta_high_le_analytic_bound_certified": cert_18_5_sharp[
                        "certified"
                    ],
                    "abs_delta_high_le_B_tail_certified": cert_18_5_tail["certified"],
                    "R_band_X_certified": serialize_arb_certified(R_band_18_5),
                    "S2_band_X_certified": serialize_arb_certified(S2_band_18_5),
                    "S2_band_Y_certified": serialize_arb_certified(S2_band_9_5),
                    "delta_low_certified": serialize_arb_certified(delta_low_18_5),
                    "B2_X_certified": serialize_arb_certified(B2_18_5),
                    "abs_B2_X_le_B_rescaled_certified": cert_18_5_rescaled["certified"],
                    "canonical_band_separation_diff_certified": serialize_arb_certified(
                        R_band_18_5
                        - (
                            S2_band_18_5
                            - (arb(1) / arb(2).sqrt()) * S2_band_9_5
                            - (arb(1) / arb(2).sqrt()) * B2_18_5
                        )
                    ),
                    "canonical_band_separation_encloses_zero": canon_sep_18_5_ok,
                },
            },
            "two_way_coprime_band_equivalence_theorem": (
                "For every fixed prime p in P (in particular p = 2, odd squarefree integers 2 nmid m), "
                "sup_{X >= 1} |R_{mu,band}(X)| < infty <==> sup_{X >= 1} |S_{p,band}(X)| < infty, "
                "with explicit two-way bounds |R_{mu,band}(X)| <= (1 + p^{-1/2}) sup_{Y>=1} |S_{p,band}(Y)| + p^{-1/2} B_rescaled "
                "and |S_{p,band}(X)| <= (1 - p^{-1/2})^{-1} (sup_{Y>=1} |R_{mu,band}(Y)| + p^{-1/2} B_rescaled)."
            ),
            "multi_prime_sieve_collapse_and_coset_obstruction": {
                "multi_prime_inclusion_exclusion_formula": (
                    "R(X; A, B) = sum_{d | P_P} (mu(d) / sqrt(d)) S_P(X / d; A / d, B / d)"
                ),
                "p2_x1_interval_1_2_orientation_regression": {
                    "R_1_1_2_certified": serialize_arb_certified(R_1_1_2),
                    "S2_1_1_2_certified": serialize_arb_certified(S2_1_1_2),
                    "S2_half_half_1_certified": serialize_arb_certified(
                        S2_half_half_1
                    ),
                    "correct_formula_rhs_certified": serialize_arb_certified(
                        correct_mp_p2_rhs
                    ),
                    "reversed_formula_rhs_certified": serialize_arb_certified(
                        reversed_mp_p2_rhs
                    ),
                    "correct_orientation_encloses_zero": p2_correct_orientation_encloses_zero,
                    "reversed_formula_detected_nonzero": p2_reversed_formula_detected_nonzero,
                },
                "three_prime_P_2_3_5_at_X_16_encloses_zero": mp_3_encloses_zero,
                "full_sieve_P_le_M_X_tautological_collapse_verified": tautological_collapse_all_match,
                "tautological_collapse_explanation": (
                    "When P = {p <= M(X)} sieves all primes up to M(X), the only positive integer k <= M(X)/d "
                    "coprime to P_P is k = 1, so S_P(X/d; H(X)/d, M(X)/d) = 1_{H(X) < d <= M(X)} W_log(X/d), "
                    "and the multi-prime expansion sum_{d | P_P} (mu(d)/sqrt(d)) S_P(...) collapses "
                    "tautologically back to sum_{H(X) < d <= M(X)} (mu(d)/sqrt(d)) W_log(X/d) = R_{mu,band}(X)."
                ),
                "multiplicative_coset_shift_note": (
                    "Whether log_tau p = log p / log(2*pi) lies in A_R is not assumed; if log_tau p notin A_R, "
                    "then prime dilation X_K |-> X_K / p = tau^{|K| - log_tau p} leaves the algebraic grade locus "
                    "tau^{A_R} for the multiplicative coset p^{-1} tau^{A_R}, whereas all rescaled boundary bounds "
                    "are proved on all of R_{>0} without assuming log_tau p in A_R."
                ),
                "euler_product_log_expansion": (
                    "sum_{p <= y} log(1 + p^{-1/2}) = sum_{p <= y} p^{-1/2} - (1/2) sum_{p <= y} p^{-1} + O(1)"
                ),
                "euler_product_factor_growth": euler_factor_growth,
            },
            "all_prime_separation_identities_enclose_zero": all_prime_sep_enclose_zero,
            "all_canonical_band_separations_enclose_zero": all_canonical_band_sep_enclose_zero,
            "all_boundary_bounds_certified": all_boundary_bounds_certified,
            "both_upper_cutoff_orderings_certified": both_upper_cutoff_orderings_certified,
            "all_p_squared_obstructions_detected": all_p_squared_obstructions_detected,
            "all_tower_telescoping_enclose_zero": all_tower_telescoping_enclose_zero,
            "sample_band_prime_table": band_prime_rows,
            "iterated_prime_tower_checks": tower_checks,
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_summation_by_parts_and_tilde_W_log_identity_arb(
    prec_bits: int = 256,
    max_quadrature_M: int = 32,
) -> Dict[str, Any]:
    """Certify in SymPy and 256-bit Arb (Requirement 4):
      1. Exact Derivative Identity for F_X(t) = t^{-1/2} W_log(X / t):
             (1/2) W_log(u) + u W_log'(u) = tilde{W}_log(u) := sum_{k=2}^infty (log k / sqrt(k)) tilde{h}_0(k / u),
             F_X'(t) = -t^{-3/2} [(1/2) W_log(X / t) + (X / t) W_log'(X / t)] = -t^{-3/2} tilde{W}_log(X / t),
         justified by uniform convergence of sum_{k>=2} (log k / sqrt(k)) (d/du) h_0(k / u) on compact
         subsets of (0, infty) via |(d/du) h_0(k / u)| <= ((1/2) C_0 + tilde{C}_0) u^{3/2} k^{-5/2}.
      2. Exact Summation by Parts with Right-Continuous Relative Mertens Function M_A(t) := sum_{A < m <= t} mu(m):
             R(X; A, B) = M_A(B) F_X(B) - int_A^B M_A(t) F_X'(t) dt
                        = M_A(B) F_X(B) + int_A^B M_A(t) t^{-3/2} tilde{W}_log(X / t) dt,
         verified by piecewise-constant step summation across all sample scales and by independent
         complex-analytic quadrature (`acb.integral`) of F_X'(t) = -t^{-3/2} tilde{W}_log(X / t) on each
         unit step interval [n, n+1] for scales with M(X) <= max_quadrature_M (recording `"NOT_RUN"` and
         `None` for quadrature fields when M(X) > max_quadrature_M).
      3. Unconditional Upper-Endpoint Bound at (A, B) = (H(X), M(X)):
         Using ONLY the trivial counting inequality |M_{H(X)}(M(X))| <= M(X) - H(X) <= M(X) (with zero
         unproved Mertens hypotheses) and |W_log(X / M(X))| <= C_{log,0} (X / M(X))^{5/2} with X^{5/2} / M(X)^2 <= 1:
             |M_{H(X)}(M(X)) F_X(M(X))| <= M(X) * M(X)^{-1/2} C_{log,0} (X / M(X))^{5/2}
                                        = C_{log,0} (X^{5/2} / M(X)^2) <= C_{log,0} < 0.557430   (for all X >= 1).
         Consequently, SUBGATE-TC-043A is unconditionally equivalent (within +/- C_{log,0}) to uniform
         boundedness of the smooth Mertens-weighted integral
             I_{M,band}(X) := -int_{H(X)}^{M(X)} M_{H(X)}(t) F_X'(t) dt
                            = int_{H(X)}^{M(X)} M_{H(X)}(t) t^{-3/2} tilde{W}_log(X / t) dt.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        pi_arb = arb.pi()
        tau_arb = arb(2) * pi_arb
        live_bounds = _compute_live_controlled_component_bounds_arb(
            prec_bits=prec_bits
        )
        C_log_0_arb = live_bounds["C_log_0_arb"]

        # 1. Symbolic verification of chain-rule derivative:
        # For f(t) = t^{-1/2} W(X / t), f'(t) = -t^{-3/2} ((1/2) W(X / t) + (X / t) W'(X / t)),
        # and for w_k(u) = h_0(k / u), (1/2) w_k(u) + u w_k'(u) = (1/2) h_0(alpha) - alpha h_0'(alpha) = tilde{h}_0(alpha).
        t_s, X_s, k_s, u_s = sp.symbols("t X k u", positive=True)
        W_fn = sp.Function("W")
        F_expr = t_s ** (-sp.Rational(1, 2)) * W_fn(X_s / t_s)
        dF_dt = sp.diff(F_expr, t_s)
        u_sub = X_s / t_s
        expected_dF = -(t_s ** (-sp.Rational(3, 2))) * (
            sp.Rational(1, 2) * W_fn(u_sub)
            + u_sub * sp.Subs(sp.diff(W_fn(u_s), u_s), u_s, u_sub)
        )
        chain_rule_symbolic_verified = bool(
            sp.simplify(dF_dt - expected_dF) == 0
        )

        h0_fn = sp.Function("h0")
        wk_expr = h0_fn(k_s / u_s)
        euler_wk = sp.Rational(1, 2) * wk_expr + u_s * sp.diff(wk_expr, u_s)
        al_sub = k_s / u_s
        expected_euler_wk = sp.Rational(1, 2) * h0_fn(al_sub) - al_sub * sp.Subs(
            sp.diff(h0_fn(t_s), t_s), t_s, al_sub
        )
        termwise_euler_symbolic_verified = bool(
            sp.simplify(euler_wk - expected_euler_wk) == 0
        )

        # 2. 256-bit Arb verification of (1/2) W_log(u) + u W_log'(u) = tilde{W}_log(u) via acb_series jet:
        jet_checks: List[Dict[str, Any]] = []
        all_jet_identities_enclose_zero = True
        k_cut_jet = 1600
        table_jet = _get_log_sqrt_table_arb(k_cut_jet, prec_bits=prec_bits)
        tilde_c0_bern = arb(10329937) / arb(655360)
        for u_label, u_a in (
            ("0.5", arb("0.5")),
            ("1.0", arb(1)),
            ("2.0", arb(2)),
            ("tau", tau_arb),
        ):
            # Evaluate W_log(u + eps) as a length-2 acb_series jet:
            u_jet = acb_series([acb(u_a), acb(1)], prec=prec_bits)
            s_jet = acb_series([acb(0), acb(0)], prec=prec_bits)
            for _, k_a, lsk in table_jet:
                al_jet = acb_series([acb(k_a), acb(0)], prec=prec_bits) / u_jet
                inv_al_jet = u_jet / acb_series([acb(k_a), acb(0)], prec=prec_bits)
                s_sum_jet = al_jet + inv_al_jet
                w_jet = s_sum_jet * s_sum_jet
                num_jet = (
                    acb(-648) * (w_jet ** 3)
                    + acb(58380) * (w_jet * w_jet)
                    - acb(706860) * w_jet
                    + acb(2027025)
                )
                den_jet = acb(512) * (s_sum_jet ** acb("8.5"))
                h0_jet = num_jet / den_jet
                s_jet = s_jet + acb(lsk) * h0_jet
            w_u_from_jet = s_jet[0].real
            dw_du_from_jet = s_jet[1].real
            k_cut_a = arb(k_cut_jet)
            tail_tilde = (
                tilde_c0_bern
                * (u_a ** arb("2.5"))
                * (arb(2) * k_cut_a.log() + arb(1))
                / (arb(4) * k_cut_a * k_cut_a)
            )
            lhs_comb = (
                arb("0.5") * w_u_from_jet
                + u_a * dw_du_from_jet
                + arb(0, tail_tilde.upper())
            )
            rhs_tilde = evaluate_tilde_W_log_certified_arb(
                u_a, min_cut=k_cut_jet, prec_bits=prec_bits
            )
            diff_jet = lhs_comb - rhs_tilde
            ok_jet = bool(diff_jet.contains(0))
            if not ok_jet:
                all_jet_identities_enclose_zero = False
            jet_checks.append(
                {
                    "u_label": u_label,
                    "half_W_log_plus_u_dW_log_certified": serialize_arb_certified(
                        lhs_comb
                    ),
                    "tilde_W_log_u_certified": serialize_arb_certified(rhs_tilde),
                    "difference_encloses_zero": ok_jet,
                }
            )

        # 3. Verify summation by parts R(X; H(X), M(X)) = M_{H(X)}(M(X)) F_X(M(X)) - int_{H(X)}^{M(X)} M_{H(X)}(t) F_X'(t) dt
        #    and unconditional endpoint bound |M_{H(X)}(M(X)) F_X(M(X))| <= C_{log,0} across sample scales:
        sbp_rows: List[Dict[str, Any]] = []
        all_sbp_ftc_enclose_zero = True
        all_performed_sbp_quadrature_enclose_zero = True
        quadrature_checks_performed_count = 0
        quadrature_checks_passed_count = 0
        quadrature_checks_not_run_count = 0
        all_endpoint_bounds_certified = True
        all_smooth_mertens_transfer_certified = True

        # Helper for complex analytic tilde{h}_0(z) to integrate F_X'(t) = -t^{-3/2} tilde{W}_log(X/t) via acb.integral:
        def _eval_tilde_h0_acb(z: acb, analytic: bool = False) -> acb:
            if analytic and (
                not z.real.is_finite()
                or not z.imag.is_finite()
                or bool(z.real <= arb(0))
            ):
                return acb(arb.nan(), arb.nan())
            s_z = z + acb(1) / z
            w_z = s_z * s_z
            d_z = z - acb(1) / z
            p_sym_z = (
                acb(-648) * (w_z ** 3)
                + acb(58380) * (w_z * w_z)
                - acb(706860) * w_z
                + acb(2027025)
            )
            h0_z = p_sym_z / (acb(512) * (s_z ** acb("8.5")))
            p_d1_z = (
                acb(3240) * (w_z ** 3)
                - acb(525420) * (w_z * w_z)
                + acb(9189180) * w_z
                - acb(34459425)
            )
            dh0_z = d_z * p_d1_z / (acb(1024) * (s_z ** acb("9.5")))
            return acb("0.5") * h0_z - dh0_z

        quad_table = _get_log_sqrt_table_arb(300, prec_bits=prec_bits)
        tol_q = 2 ** (-70)

        for x_label, x_a in (
            ("1", arb(1)),
            ("2", arb(2)),
            ("4", arb(4)),
            ("tau", tau_arb),
            ("10", arb(10)),
            ("16", arb(16)),
            ("tau^2", tau_arb * tau_arb),
        ):
            H_x = certified_head_cutoff_H_X_arb(x_a, prec_bits=prec_bits)
            M_x = certified_coupled_cutoff_M_X_arb(x_a, prec_bits=prec_bits)
            R_band = evaluate_R_interval_arb(
                x_a, arb(H_x), arb(M_x), prec_bits=prec_bits
            )

            # Evaluate F_X(n) = n^{-1/2} W_log(X / n) for integers H(X) <= n <= M(X):
            F_vals: Dict[int, arb] = {}
            for n_i in range(H_x, M_x + 1):
                n_a = arb(n_i)
                F_vals[n_i] = (arb(1) / n_a.sqrt()) * evaluate_W_log_em4_certified_arb(
                    x_a / n_a, prec_bits=prec_bits
                )

            # Relative Mertens values M_{H(X)}(n) = sum_{H(X) < m <= n} mu(m):
            M_rel: Dict[int, int] = {H_x: 0}
            running_mu = 0
            for n_i in range(H_x + 1, M_x + 1):
                running_mu += moebius_mu_int(n_i)
                M_rel[n_i] = running_mu

            endpoint_term = arb(M_rel[M_x]) * F_vals[M_x]
            # Integral I_{M,band}(X) = -int_{H(X)}^{M(X)} M_{H(X)}(t) F_X'(t) dt via step-interval FTC:
            I_mertens_ftc = arb(0)
            for n_i in range(H_x + 1, M_x - 1 + 1):
                if M_rel[n_i] != 0:
                    I_mertens_ftc -= arb(M_rel[n_i]) * (
                        F_vals[n_i + 1] - F_vals[n_i]
                    )

            sbp_recon_ftc = endpoint_term + I_mertens_ftc
            ftc_diff = R_band - sbp_recon_ftc
            ftc_ok = bool(ftc_diff.contains(0))
            if not ftc_ok:
                all_sbp_ftc_enclose_zero = False

            # Direct complex-analytic quadrature of int_n^{n+1} t^{-3/2} tilde{W}_log(X/t) dt on each unit interval
            # for scales with M(X) <= max_quadrature_M (verifying the derivative formula under the integral sign):
            if M_x <= max_quadrature_M:
                quadrature_checks_performed_count += 1
                I_mertens_quad = arb(0)
                k_cut_q = 300
                k_cut_qa = arb(k_cut_q)
                for n_i in range(H_x + 1, M_x):
                    m_step_val = M_rel[n_i]
                    if m_step_val == 0:
                        continue
                    n_a = arb(n_i)
                    np1_a = arb(n_i + 1)

                    def _f_step(
                        t_c: acb,
                        analytic: bool = False,
                        xc: acb = acb(x_a),
                    ) -> acb:
                        s_q = acb(0)
                        for _, k_a, lsk in quad_table:
                            s_q += acb(lsk) * _eval_tilde_h0_acb(
                                (acb(k_a) * t_c) / xc, analytic=analytic
                            )
                        return (t_c ** acb("-1.5")) * s_q

                    seg_int = acb.integral(
                        _f_step,
                        acb(n_a),
                        acb(np1_a),
                        rel_tol=tol_q,
                        abs_tol=tol_q,
                    ).real
                    # Tail bound on [n, n+1] for k > k_cut_q:
                    seg_tail = (
                        tilde_c0_bern
                        * (x_a ** arb("2.5"))
                        * (arb(2) * k_cut_qa.log() + arb(1))
                        / (arb(4) * k_cut_qa * k_cut_qa)
                        * ((n_a ** arb("-3")) - (np1_a ** arb("-3")))
                        / arb(3)
                    )
                    I_mertens_quad += arb(m_step_val) * (
                        seg_int + arb(0, seg_tail.upper())
                    )
                quad_recon = endpoint_term + I_mertens_quad
                quad_diff = R_band - quad_recon
                quad_ok = bool(quad_diff.contains(0))
                if quad_ok:
                    quadrature_checks_passed_count += 1
                else:
                    all_performed_sbp_quadrature_enclose_zero = False
                quad_status = "CERTIFIED_QUADRATURE"
                quad_cert_entry: Any = serialize_arb_certified(I_mertens_quad)
                quad_encloses_zero_entry: Any = quad_ok
            else:
                quadrature_checks_not_run_count += 1
                quad_status = "NOT_RUN"
                quad_cert_entry = None
                quad_encloses_zero_entry = None

            # Certify unconditional upper-endpoint bound |M_{H(X)}(M(X)) F_X(M(X))| <= C_{log,0} X^{5/2} / M(X)^2 <= C_{log,0}:
            sharp_ep_bound = (
                C_log_0_arb * (x_a ** arb("2.5")) / (arb(M_x) ** arb(2))
            )
            ep_sharp_cert = certify_abs_le_bound_arb(
                endpoint_term, sharp_ep_bound
            )
            ep_global_cert = certify_abs_le_bound_arb(
                endpoint_term, C_log_0_arb
            )
            transfer_cert = certify_abs_le_bound_arb(
                R_band - I_mertens_ftc, C_log_0_arb
            )
            if not (
                ep_sharp_cert["certified"]
                and ep_global_cert["certified"]
                and transfer_cert["certified"]
            ):
                all_endpoint_bounds_certified = False
                all_smooth_mertens_transfer_certified = False

            sbp_rows.append(
                {
                    "X_label": x_label,
                    "H_X": H_x,
                    "M_X": M_x,
                    "M_rel_at_M_X": M_rel[M_x],
                    "abs_M_rel_le_M_X": bool(abs(M_rel[M_x]) <= M_x),
                    "R_mu_band_X_certified": serialize_arb_certified(R_band),
                    "upper_endpoint_term_M_B_F_B_certified": serialize_arb_certified(
                        endpoint_term
                    ),
                    "smooth_mertens_integral_I_M_band_ftc_certified": serialize_arb_certified(
                        I_mertens_ftc
                    ),
                    "independent_quadrature_status": quad_status,
                    "smooth_mertens_integral_I_M_band_quadrature_certified": quad_cert_entry,
                    "sharp_endpoint_bound_C_log_0_X_5_2_over_M_sq_certified": serialize_arb_certified(
                        sharp_ep_bound
                    ),
                    "sbp_ftc_identity_encloses_zero": ftc_ok,
                    "sbp_quadrature_identity_encloses_zero": quad_encloses_zero_entry,
                    "abs_endpoint_le_sharp_bound_certified": ep_sharp_cert[
                        "certified"
                    ],
                    "abs_endpoint_le_C_log_0_certified": ep_global_cert[
                        "certified"
                    ],
                    "abs_R_band_minus_I_M_band_le_C_log_0_certified": transfer_cert[
                        "certified"
                    ],
                }
            )

        return {
            "derivative_identity_formula": (
                "(1/2) W_log(u) + u W_log'(u) = tilde{W}_log(u) = sum_{k=2}^infty (log k / sqrt(k)) tilde{h}_0(k / u),   "
                "F_X'(t) = -t^{-3/2} [(1/2) W_log(X/t) + (X/t) W_log'(X/t)] = -t^{-3/2} tilde{W}_log(X/t)"
            ),
            "termwise_differentiation_justification": (
                "For u in [u_min, u_max] subset (0, infty), |(d/du) h_0(k / u)| = (k / u^2) |h_0'(k / u)| "
                "<= ((1/2) C_0 + tilde{C}_0) u_{max}^{3/2} k^{-5/2}, so sum_{k=2}^infty (log k / sqrt(k)) |(d/du) h_0(k / u)| "
                "<= ((1/2) C_0 + tilde{C}_0) u_{max}^{3/2} sum_{k=2}^infty k^{-3} log k < infty converges uniformly on compact subsets."
            ),
            "summation_by_parts_formula": (
                "R(X; A, B) = M_A(B) F_X(B) - int_A^B M_A(t) F_X'(t) dt "
                "= M_A(B) F_X(B) + int_A^B M_A(t) t^{-3/2} tilde{W}_log(X / t) dt,   "
                "where M_A(t) := sum_{A < m <= t} mu(m) (M_A(A) = 0, right-continuous)"
            ),
            "unconditional_upper_endpoint_bound": {
                "theorem_statement": (
                    "|M_{H(X)}(M(X)) F_X(M(X))| <= M(X) * M(X)^{-1/2} C_{log,0} (X / M(X))^{5/2} "
                    "= C_{log,0} (X^{5/2} / M(X)^2) <= C_{log,0} < 0.557430   for all X >= 1 "
                    "(proved unconditionally using only |M_{H(X)}(M(X))| <= M(X) and M(X) >= X^{5/4})."
                ),
                "C_log_0_certified": serialize_arb_certified(C_log_0_arb),
                "C_log_0_rational_ceiling": "557430 / 1000000 = 0.557430",
            },
            "chain_rule_symbolic_verified": chain_rule_symbolic_verified,
            "termwise_euler_symbolic_verified": termwise_euler_symbolic_verified,
            "all_jet_identities_enclose_zero": all_jet_identities_enclose_zero,
            "all_sbp_ftc_enclose_zero": all_sbp_ftc_enclose_zero,
            "all_performed_sbp_quadrature_enclose_zero": all_performed_sbp_quadrature_enclose_zero,
            "all_sbp_quadrature_enclose_zero": all_performed_sbp_quadrature_enclose_zero,
            "independent_quadrature_max_M_cutoff": max_quadrature_M,
            "independent_quadrature_performed_count": quadrature_checks_performed_count,
            "independent_quadrature_passed_count": quadrature_checks_passed_count,
            "independent_quadrature_not_run_count": quadrature_checks_not_run_count,
            "all_endpoint_bounds_certified": all_endpoint_bounds_certified,
            "all_smooth_mertens_transfer_certified": all_smooth_mertens_transfer_certified,
            "jet_derivative_checks": jet_checks,
            "summation_by_parts_table": sbp_rows,
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_sign_sequence_cancellation_discrimination_arb(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Compare across scales X in {1, 2, 4, tau, 10, 16, 25, tau^2, 64} the resonant-band sum
        R_sigma(X) := sum_{H(X) < m <= M(X)} (sigma_m / sqrt(m)) W_log(X / m)
    for the four evaluated bounded arithmetic sequences sigma_m in [-1, 1]:
      1. Actual Moebius sequence sigma_m = mu(m) (signed squarefree sum R_{mu,band}(X));
      2. Constant sequence sigma_m = +1 (signed kernel-weighted all-integer sum R_{1,band}(X));
      3. Squarefree indicator sigma_m = |mu(m)| = mu(m)^2 (signed kernel-weighted squarefree sum R_{|mu|,band}(X));
      4. Worst-case adversarial sign sequence sigma_m^{wc}(X) = |mu(m)| sgn(W_log(X / m)),
         giving the triangle-inequality majorant sum_{H(X) < m <= M(X)} (|mu(m)| / sqrt(m)) |W_log(X / m)|.
    Distinguishes signed sums |sum_m a_m m^{-1/2} W_log(X/m)| from absolute-value sums
    sum_m |a_m m^{-1/2} W_log(X/m)|: at X = 64 ((H, M) = (32, 182)), R_{mu,band}(64) = 0.03059141547...,
    R_{1,band}(64) = -0.01583365880..., R_{|mu|,band}(64) = 0.01904894182..., and the triangle-inequality
    majorant reaches 0.29032671364... (ratio 9.49046356... over |R_{mu,band}(64)|). Note that finite-grid
    observations do not determine the asymptotic behavior of R_{1,band}(X) or R_{|mu|,band}(X), and O(X^{1/2})
    is an upper bound for the triangle-inequality majorant unless a matching lower bound is proved."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        tau_arb = arb(2) * arb.pi()
        scales: List[Tuple[str, arb]] = [
            ("1", arb(1)),
            ("2", arb(2)),
            ("4", arb(4)),
            ("tau", tau_arb),
            ("10", arb(10)),
            ("16", arb(16)),
            ("25", arb(25)),
            ("tau^2", tau_arb * tau_arb),
            ("64", arb(64)),
        ]
        rows: List[Dict[str, Any]] = []
        max_abs_mu_band = arb(0)
        for x_label, x_a in scales:
            H_x = certified_head_cutoff_H_X_arb(x_a, prec_bits=prec_bits)
            M_x = certified_coupled_cutoff_M_X_arb(x_a, prec_bits=prec_bits)
            r_mu = arb(0)
            r_const_one = arb(0)
            r_sqfree_abs = arb(0)
            r_worst_case = arb(0)
            for m in range(H_x + 1, M_x + 1):
                m_a = arb(m)
                inv_sqrt_m = arb(1) / m_a.sqrt()
                w_xm = evaluate_W_log_em4_certified_arb(
                    x_a / m_a, prec_bits=prec_bits
                )
                r_const_one += inv_sqrt_m * w_xm
                mu_m = moebius_mu_int(m)
                if mu_m != 0:
                    r_mu += arb(mu_m) * inv_sqrt_m * w_xm
                    r_sqfree_abs += inv_sqrt_m * w_xm
                    r_worst_case += inv_sqrt_m * abs(w_xm)
            if bool(abs(r_mu).upper() > max_abs_mu_band.upper()):
                max_abs_mu_band = abs(r_mu)
            ratio_wc_to_mu = r_worst_case / abs(r_mu)
            rows.append(
                {
                    "X_label": x_label,
                    "X_float": float(x_a.mid()),
                    "H_X": H_x,
                    "M_X": M_x,
                    "band_length_M_minus_H": M_x - H_x,
                    "R_mu_band_actual_certified": serialize_arb_certified(r_mu),
                    "R_const_one_band_certified": serialize_arb_certified(
                        r_const_one
                    ),
                    "R_squarefree_indicator_band_certified": serialize_arb_certified(
                        r_sqfree_abs
                    ),
                    "R_worst_case_abs_band_certified": serialize_arb_certified(
                        r_worst_case
                    ),
                    "worst_case_to_actual_abs_ratio_certified": serialize_arb_certified(
                        ratio_wc_to_mu
                    ),
                    "worst_case_divided_by_sqrt_X_certified": serialize_arb_certified(
                        r_worst_case / x_a.sqrt()
                    ),
                }
            )
        return {
            "discrimination_summary": (
                "Across the 9 tested grid points X in {1, 2, 4, tau, 10, 16, 25, tau^2, 64}, "
                "max |R_{mu,band}(X)| = |R_{mu,band}(64)| = 0.03059141547..., whereas at X = 64 "
                "((H, M) = (32, 182)) the signed sums are R_{1,band}(64) = -0.01583365880... and "
                "R_{|mu|,band}(64) = 0.01904894182..., and the triangle-inequality majorant "
                "sum_{32 < m <= 182} (|mu(m)| / sqrt(m)) |W_log(64/m)| = 0.29032671364... "
                "(ratio 9.49046356... over |R_{mu,band}(64)|). This distinguishes signed sums "
                "|sum_m a_m m^{-1/2} W_log(X/m)| from absolute-value sums sum_m |a_m m^{-1/2} W_log(X/m)|; "
                "finite-grid evaluations do not determine the asymptotic behavior of R_{1,band}(X) or "
                "R_{|mu|,band}(X), and O(X^{1/2}) is an upper bound for the triangle-inequality majorant "
                "unless a matching lower bound is proved."
            ),
            "max_abs_R_mu_band_on_tested_grid_certified": serialize_arb_certified(
                max_abs_mu_band
            ),
            "sign_discrimination_table": rows,
        }
    finally:
        flint_ctx.prec = saved_prec


def execute_task_tc051_prime_arithmetic_resonant_band_audit(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Execute the complete TASK-TC-051 / TASK-TC-051R audit of the prime-separation identity,
    rescaled canonical-band boundary bounds, summation by parts, and sign-sequence
    cancellation discrimination."""
    prime_sep_audit = (
        verify_prime_separation_identity_and_canonical_band_boundary_arb(
            prec_bits=prec_bits
        )
    )
    sbp_audit = verify_summation_by_parts_and_tilde_W_log_identity_arb(
        prec_bits=prec_bits
    )
    sign_disc_audit = verify_sign_sequence_cancellation_discrimination_arb(
        prec_bits=prec_bits
    )
    return {
        "task_id": TASK_TC_051_ID,
        "repair_task_id": "TASK-TC-051R",
        "starting_head": STARTING_HEAD_TC_051,
        "tc051_merged_main_baseline": "b6f22dfee0dd6177ee855189304e7930f9ba3e20",
        "tc051_implementation_commit": "333661eecd69738e8a67143e635b6db4f40170ce",
        "tc051_branch_tip": "7ac0546b1177970ff0d87824f61643da2405c4c0",
        "subgate_tc043a_status": "OPEN",
        "rh_proved": False,
        "closure_target_formula": (
            "exists B < infty forall X >= 1 : |sum_{H(X) < m <= M(X)} (mu(m)/sqrt(m)) W_log(X/m)| <= B, "
            "H(X) = floor(X^{5/6}), M(X) = ceil(max(2, X^{5/4}))"
        ),
        "tc_compatibility_framework": {
            "common_observable": (
                "Complete grade-correlation functional C_tau(K) = W_arch(h_K) - W_prime(h_K) "
                "and its localized resonant-band Moebius core R_{mu,band}(X_K) at X_K = tau^{|K|} (tau = 2*pi, K in A_R)."
            ),
            "arithmetic_and_fourier_actions": (
                "Prime dilation D_p: X |-> X/p and Moebius sieve operator I - p^{-1/2} D_p on the divisor sum "
                "vs. tau-normalized Mellin-Fourier duality and unitary grade translation U_K on H_tau^pos."
            ),
            "compatibility_identities_proved": [
                "R(X; A, B) = S_p(X; A, B) - p^{-1/2} S_p(X/p; A/p, B/p)   (exact single-prime separation)",
                "R_j = S_j - q S_{j+1}, S_0 = sum_{j=0}^{L-1} q^j R_j + q^L S_L   (simultaneously rescaled arbitrary-interval tower)",
                "R_{mu,band}(X) = S_{p,band}(X) - p^{-1/2} S_{p,band}(X/p) - p^{-1/2} B_p(X)   (canonical rescaled-band separation)",
                "S_{p,band}(X) = sum_{j=0}^{L-1} q^j (R_{mu,band}(X/p^j) + q B_p(X/p^j)) + q^L S_{p,band}(X/p^L)   (canonical-band inverse tower, 1 <= L <= floor(log_p X) + 1)",
                "R(X; A, B) = sum_{d | P} (mu(d)/sqrt(d)) S_P(X/d; A/d, B/d)   (multi-prime inclusion-exclusion)",
                "R(X; A, B) = M_A(B) F_X(B) + int_A^B M_A(t) t^{-3/2} tilde{W}_log(X/t) dt   (exact summation by parts)",
            ],
            "unconditional_estimates_proved": [
                "|B_p(X)| <= B_rescaled := B_log + (5/6) C_{log,EM} + (1/2) C_{log,0} < 14.851486   (all X >= 1, all primes p, across both M(X)/p >= M(X/p) and M(X)/p < M(X/p))",
                "|M_{H(X)}(M(X)) F_X(M(X))| <= C_{log,0} (X^{5/2} / M(X)^2) <= C_{log,0} < 0.557430   (all X >= 1)",
                "|R_{mu,band}(X) - I_{M,band}(X)| <= C_{log,0} < 0.557430   (all X >= 1)",
            ],
            "off_critical_zero_contradiction_point": (
                "Any off-critical zero rho_0 = 1/2 + delta_0 + i*gamma_0 with delta_0 > 0 (of any multiplicity m_{rho_0} >= 1, "
                "with no maximal-offset assumption required because zeros of xi(s) are isolated and H_0(rho_0 - 1/2) != 0) "
                "creates an isolated simple pole of the meromorphic continuation of R_+(lambda) = int_0^infty C_tau(u) e^{-lambda u} du "
                "at lambda = (delta_0 - i*gamma_0) log tau in Re(lambda) > 0, contradicting holomorphy of R_+(lambda) on Re(lambda) > 0 "
                "whenever sup_{K in A_R} |C_tau(K)| < infty."
            ),
            "first_remaining_unproved_implication": (
                "Uniform O(1) boundedness of the smooth Mertens-weighted integral "
                "I_{M,band}(X) = int_{H(X)}^{M(X)} M_{H(X)}(t) t^{-3/2} tilde{W}_log(X/t) dt "
                "(or equivalently sup_{X >= 1} |S_{2,band}(X)| < infty on odd squarefree integers 2 nmid m), "
                "which requires proving that the relative Mertens step function M_{H(X)}(t) = sum_{H(X) < m <= t} mu(m) "
                "exhibits O(t^{1/2}) cancellation against the smooth derivative kernel -F_X'(t) = t^{-3/2} tilde{W}_log(X/t) "
                "across the transition zone t ~ X."
            ),
        },
        "prime_separation_and_rescaled_band_audit": prime_sep_audit,
        "summation_by_parts_and_tilde_W_log_audit": sbp_audit,
        "sign_sequence_cancellation_discrimination_audit": sign_disc_audit,
    }


# ---------------------------------------------------------------------------
# 6. Master Execution Function for TASK-TC-050 / TASK-TC-051 / TASK-TC-051R
# ---------------------------------------------------------------------------


def execute_task_tc050_faithful_spectral_realization_audit(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Execute the complete TASK-TC-050 / TASK-TC-051R audit and return the certified report dictionary."""
    sec1_roles = verify_tau_joint_arithmetic_fourier_roles_and_transforms(
        prec_bits=prec_bits
    )
    sec2_adjoint = verify_adjoint_compatibility_and_hyperbolic_pair_obstruction(
        prec_bits=prec_bits
    )
    sec3_literature = (
        verify_primary_literature_constructions_and_support_extension(
            prec_bits=prec_bits
        )
    )
    sec4_orbit = verify_canonical_hilbert_schmidt_orbit_decomposition(
        prec_bits=prec_bits
    )
    sec7_tc051 = execute_task_tc051_prime_arithmetic_resonant_band_audit(
        prec_bits=prec_bits
    )
    lean_audit = verify_canonical_theta_correlation_lean_module()

    report: Dict[str, Any] = {
        "task_id": TASK_TC_050_ID,
        "continuation_task_id": TASK_TC_051_ID,
        "repair_task_id": "TASK-TC-051R",
        "preceding_repair_task_ids": ["TASK-TC-050R", "TASK-TC-050R2"],
        "parent_epic": EPIC_TC_042_ID,
        "starting_head": STARTING_HEAD_TC_050,
        "tc051_starting_head": STARTING_HEAD_TC_051,
        "tc051_merged_main_baseline": "b6f22dfee0dd6177ee855189304e7930f9ba3e20",
        "tc051_implementation_commit": "333661eecd69738e8a67143e635b6db4f40170ce",
        "tc051_branch_tip": "7ac0546b1177970ff0d87824f61643da2405c4c0",
        "reviewed_baseline": REVIEWED_BASELINE_TC_050,
        "tc050r_reviewed_baseline": "2f7871fff666091c4152ecc8657f2345aacdd4fa",
        "tc050r2_reviewed_head": "0e6ae36ce995ef3037652b3dfb67645325f990b1",
        "tc050r_implementation_commit": "f5521363ea94774938fd37152d67d743413327ae",
        "status": FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION_STATUS,
        "subgate_tc043a_status": "OPEN",
        "rh_proved": False,
        "section_1_tau_roles_and_prime_transformations": sec1_roles,
        "section_2_adjoint_compatibility_and_hyperbolic_null_cone": sec2_adjoint,
        "section_3_primary_literature_constructions_audit": sec3_literature,
        "section_4_canonical_hilbert_schmidt_orbit_decomposition": sec4_orbit,
        "section_5_lean_formalization_and_remaining_obligation": {
            "lean_module_verification": lean_audit,
            "new_lean_theorems_tc050": [
                "tau_grade_star_involution_and_hyperbolic_pair_obstruction",
                "tate_rational_diagonal_character_rigidity_and_convolution_isometry",
                "canonical_hilbert_schmidt_orbit_decomposition_and_resonant_band_equivalence",
            ],
            "new_lean_theorems_tc051": [
                "prime_separation_and_canonical_band_boundary_equivalence",
                "summation_by_parts_endpoint_bound_and_smooth_mertens_reduction",
                "iterated_prime_tower_telescoping_and_coprime_band_transfer",
            ],
            "committed_lean_theorems_exact_scope": {
                "theorem_51_tau_grade_star_involution_and_hyperbolic_pair_obstruction": {
                    "parameters": "(tau K J delta B11 B12 B22 c1 c2 : ℝ) (htau : 1 < tau) (hK : K ≠ 0) (hB12 : 0 < B12)",
                    "definitions_used": [
                        "gradeRadialCharacter (tau K delta : ℝ) := tau ^ (K * delta)",
                        "hyperbolicPairForm (B12 c1 c2 : ℝ) := 2 * B12 * c1 * c2",
                        "jordanTwoByTwoSocleStep (lam c0 c1 : ℝ) : ℝ × ℝ := (lam * c0 + c1, lam * c1)",
                    ],
                    "proved_conjuncts": [
                        "gradeRadialCharacter tau (K + J) delta = gradeRadialCharacter tau K delta * gradeRadialCharacter tau J delta ∧ gradeRadialCharacter tau (-K) delta = gradeRadialCharacter tau K (-delta)",
                        "gradeRadialCharacter tau (-K) delta = gradeRadialCharacter tau K delta ↔ delta = 0",
                        "delta ≠ 0 → (tau ^ (2 * K * delta) - 1) * B11 = 0 → (tau ^ (-(2 * K * delta)) - 1) * B22 = 0 → (B11 = 0 ∧ B22 = 0 ∧ B11 * c1 ^ 2 + 2 * B12 * c1 * c2 + B22 * c2 ^ 2 = hyperbolicPairForm B12 c1 c2 ∧ 0 < hyperbolicPairForm B12 1 1 ∧ hyperbolicPairForm B12 1 (-1) < 0)",
                        "jordanTwoByTwoSocleStep (gradeRadialCharacter tau K delta) 1 0 = (gradeRadialCharacter tau K delta, 0) ∧ jordanTwoByTwoSocleStep (gradeRadialCharacter tau K delta) 0 1 = (1, gradeRadialCharacter tau K delta) ∧ (jordanTwoByTwoSocleStep (gradeRadialCharacter tau K delta) 0 1).1 ≠ 0",
                    ],
                    "external_analytic_scope_note": (
                        "In (4), Lean proves the Jordan block basis-action identities showing the socle vector (1, 0) "
                        "has zero nilpotent drift while (0, 1) has nonzero socle drift component 1 != 0; the Hilbert-norm "
                        "growth deduction ||V_K l_{rho,1}||^2 = ||l_{rho,1} + (K log tau) l_{rho,0}||^2 for m_rho >= 2 "
                        "is an external analytic corollary of that nonzero nilpotent drift."
                    ),
                },
                "theorem_52_tate_rational_diagonal_character_rigidity_and_convolution_isometry": {
                    "parameters": "(tau c_inf q K u J C_gh C_dil : ℝ) (T_conv : ℝ → ℝ) (htau : 1 < tau)",
                    "definitions_used": [
                        "adelicPhaseDiscrepancy (tau c_inf q : ℝ) := (tau - c_inf) * q",
                        "logPrimeShiftAction (u J : ℝ) := u - J",
                        "logScaleAction (scale u : ℝ) := scale * u",
                    ],
                    "proved_conjuncts": [
                        "(adelicPhaseDiscrepancy tau c_inf 1 = 0 ↔ c_inf = tau) ∧ (c_inf = tau → adelicPhaseDiscrepancy tau c_inf q = 0)",
                        "(tau ^ K) * (tau ^ (-K)) = 1",
                        "logScaleAction (tau ^ (-K)) (logPrimeShiftAction u J) = logPrimeShiftAction (logScaleAction (tau ^ (-K)) u) (J * (tau ^ (-K))) ∧ logScaleAction (tau ^ (-K)) (logPrimeShiftAction u J) - logPrimeShiftAction (logScaleAction (tau ^ (-K)) u) J = (1 - tau ^ (-K)) * J",
                        "C_dil = C_gh → T_conv C_dil = T_conv C_gh",
                    ],
                    "external_analytic_scope_note": (
                        "Theorem 52 is parameterized over generic real tau > 1 (not specialized to 2 * Real.pi inside Lean); "
                        "the principal-adele partial-fraction congruence sum_p {q}_p = q (mod 1) and multiplicative Haar "
                        "convolution invariance (U_K g) * (U_K h)^* = g * h^* are external analytic inputs."
                    ),
                },
                "theorem_53_canonical_hilbert_schmidt_orbit_decomposition_and_resonant_band_equivalence": {
                    "parameters_and_hypotheses": (
                        "(W_arch W_prime P_K P_0 c_tau_B h0_XK J_K c_pole_transfer_h0 W_reflected W_log_X R_head R_band_X R_tail "
                        "B_h0 B_refl B_log C_log_EM C_log_0 B_head B_tail M_band M_C : ℝ) "
                        "(h_arch : W_arch = P_K - c_pole_transfer_h0) "
                        "(h_prime : W_prime = W_reflected + W_log_X + localizedResonantBandDecomp R_head R_band_X R_tail) "
                        "(h_PK : |P_K| ≤ P_0) (h_h0 : |c_pole_transfer_h0| ≤ B_h0) (h_refl : |W_reflected| ≤ B_refl) "
                        "(h_log : |W_log_X| ≤ B_log) (h_head : |R_head| ≤ B_head) (h_tail : |R_tail| ≤ B_tail)"
                    ),
                    "definitions_used": [
                        "controlledCorrelationRemainder (c_pole_transfer_h0 W_reflected W_log_X R_head R_tail : ℝ) := -c_pole_transfer_h0 - W_reflected - W_log_X - R_head - R_tail",
                        "canonicalCorrelationHSOrbitDecomp (P_K E_ctrl_K R_band_X : ℝ) := P_K + (E_ctrl_K - R_band_X)",
                    ],
                    "proved_conjuncts": [
                        "((W_arch + c_tau_B * h0_XK - (2 * h0_XK - J_K)) + (4 * h0_XK - J_K) = W_arch + (c_tau_B + 2) * h0_XK) ∧ (0 ≤ P_0 → |P_0| ≤ P_0) ∧ C_K = canonicalCorrelationHSOrbitDecomp P_K E_ctrl_K R_band_X ∧ C_K = P_K + E_K",
                        "|E_ctrl_K| ≤ B_ctrl ∧ |C_K - (P_K - R_band_X)| ≤ B_ctrl ∧ (B_head = (5/6) * C_log_EM → B_tail = (1/2) * C_log_0 → B_h0 < 2671923/1000000 → B_refl < 463730/1000000 → B_log < 3349009/1000000 → C_log_EM < 13468515/1000000 → C_log_0 < 557430/1000000 → B_ctrl < 17987140/1000000)",
                        "(|R_band_X| ≤ M_band → (|E_K| ≤ B_ctrl + M_band ∧ |C_K| ≤ P_0 + B_ctrl + M_band)) ∧ (|C_K| ≤ M_C → (|E_K| ≤ M_C + P_0 ∧ |R_band_X| ≤ M_C + P_0 + B_ctrl))",
                    ],
                    "external_analytic_scope_note": (
                        "Theorem 53 retains h_arch, h_prime, h_PK, and the five component inequalities as explicit hypotheses, "
                        "proves the algebraic J_K-cancellation identity alongside h_arch, and proves B_ctrl < 17987140/1000000 "
                        "conditionally from the rational upper-bound hypotheses. The integer-power cutoff predicates for "
                        "H(X) = floor(X^{5/6}) and M(X) = ceil(max(2, X^{5/4})) are certified in Python Arb helpers rather than inside Theorem 53."
                    ),
                },
                "theorem_54_prime_separation_and_canonical_band_boundary_equivalence": {
                    "parameters_and_hypotheses": (
                        "(R_X S_p_X S_p_rescaled S_p_band_xp B_p_low B_p_high q B_log C_log_EM C_log_0 B_head B_tail M_S M_R : ℝ) "
                        "(hq_nonneg : 0 ≤ q) (hq_le_one : q ≤ 1) "
                        "(h_sep : R_X = primeSeparationDecomp S_p_X q S_p_rescaled) "
                        "(h_rescaled : S_p_rescaled = S_p_band_xp + rescaledBandBoundarySum B_p_low B_p_high) "
                        "(h_low : |B_p_low| ≤ B_log + B_head) (h_high : |B_p_high| ≤ B_tail)"
                    ),
                    "definitions_used": [
                        "primeSeparationDecomp (S_p_X q S_p_rescaled : ℝ) := S_p_X - q * S_p_rescaled",
                        "rescaledBandBoundarySum (B_p_low B_p_high : ℝ) := B_p_low + B_p_high",
                    ],
                    "proved_conjuncts": [
                        "R_X = S_p_X - q * S_p_band_xp - q * (B_p_low + B_p_high)",
                        "|B_p_low + B_p_high| ≤ B_log + B_head + B_tail ∧ (B_head = (5/6) * C_log_EM → B_tail = (1/2) * C_log_0 → B_log < 3349009/1000000 → C_log_EM < 13468515/1000000 → C_log_0 < 557430/1000000 → B_log + B_head + B_tail < 14851487/1000000)",
                        "(|S_p_X| ≤ M_S ∧ |S_p_band_xp| ≤ M_S → |R_X| ≤ (1 + q) * M_S + q * (B_log + B_head + B_tail)) ∧ (|R_X| ≤ M_R ∧ |S_p_band_xp| ≤ M_S → |S_p_X| ≤ M_R + q * M_S + q * (B_log + B_head + B_tail))",
                    ],
                    "external_analytic_scope_note": (
                        "Theorem 54 proves the algebraic consequences of the single-prime separation and rescaled-band "
                        "boundary decomposition from explicit hypotheses h_sep, h_rescaled, h_low, h_high; the squarefree "
                        "divisibility partition m = p d (mu(p d) = 0 for p | d, mu(p d) = -mu(d) for p nmid d), the lower "
                        "cutoff comparison floor(H(X)/p) <= H(X/p), and the upper boundary bound |Delta_{p,high}(X)| <= B_tail across "
                        "both cutoff orderings (M(X)/p >= M(X/p) and the single-endpoint regime N - 1 < M(X)/p < N := M(X/p)) "
                        "are proved analytically outside Lean."
                    ),
                },
                "theorem_55_summation_by_parts_endpoint_bound_and_smooth_mertens_reduction": {
                    "parameters_and_hypotheses": (
                        "(R_X M_B F_B I_mertens M_cut X25 C_log_0 M_I M_R : ℝ) "
                        "(h_sbp : R_X = summationByPartsDecomp M_B F_B I_mertens) "
                        "(h_M_pos : 0 < M_cut) (h_X25_nonneg : 0 ≤ X25) (h_C_nonneg : 0 ≤ C_log_0) "
                        "(h_mertens_triv : |M_B| ≤ M_cut) (h_F_bound : |F_B| * (M_cut ^ 3) ≤ C_log_0 * X25) "
                        "(h_cutoff_dom : X25 ≤ M_cut ^ 2)"
                    ),
                    "definitions_used": [
                        "summationByPartsDecomp (M_B F_B I_mertens : ℝ) := M_B * F_B + I_mertens",
                    ],
                    "proved_conjuncts": [
                        "|M_B * F_B| * (M_cut ^ 2) ≤ C_log_0 * X25 ∧ |M_B * F_B| ≤ C_log_0",
                        "|R_X - I_mertens| ≤ C_log_0 ∧ (C_log_0 < 557430 / 1000000 → |R_X - I_mertens| < 557430 / 1000000)",
                        "(|I_mertens| ≤ M_I → |R_X| ≤ M_I + C_log_0) ∧ (|R_X| ≤ M_R → |I_mertens| ≤ M_R + C_log_0)",
                    ],
                    "external_analytic_scope_note": (
                        "Theorem 55 proves the unconditional upper-endpoint cancellation |M_B * F_B| <= C_{log,0} "
                        "and two-way reduction between R_X and I_mertens from the trivial counting bound |M_B| <= M_cut, "
                        "the small-argument envelope |F_B| * M_cut^3 <= C_{log,0} * X^{5/2}, and X^{5/2} <= M_cut^2; "
                        "the Stieltjes integration-by-parts step and termwise Euler derivative tilde{W}_log are proved analytically outside Lean."
                    ),
                },
                "theorem_56_iterated_prime_tower_telescoping_and_coprime_band_transfer": {
                    "parameters_and_hypotheses": (
                        "(S_0 S_1 S_2 R_0 R_1 B_0 B_1 q M_R B_rescaled : ℝ) "
                        "(hq_nonneg : 0 ≤ q) (hq_lt_one : q < 1) "
                        "(h_step0 : R_0 = S_0 - q * S_1 - q * B_0) "
                        "(h_step1 : R_1 = S_1 - q * S_2 - q * B_1) "
                        "(h_R0 : |R_0| ≤ M_R) (h_R1 : |R_1| ≤ M_R) "
                        "(h_B0 : |B_0| ≤ B_rescaled) (h_B1 : |B_1| ≤ B_rescaled)"
                    ),
                    "definitions_used": [
                        "twoStepPrimeTowerSum (R_0 R_1 B_0 B_1 q S_2 : ℝ) := (R_0 + q * B_0) + q * (R_1 + q * B_1) + (q ^ 2) * S_2",
                    ],
                    "proved_conjuncts": [
                        "S_0 = twoStepPrimeTowerSum R_0 R_1 B_0 B_1 q S_2",
                        "|S_0 - (q ^ 2) * S_2| ≤ (1 + q) * (M_R + q * B_rescaled)",
                        "S_2 = 0 → (1 - q) * |S_0| ≤ M_R + q * B_rescaled",
                    ],
                    "external_analytic_scope_note": (
                        "Theorem 56 proves the two-step prime-power tower telescoping identity and geometric "
                        "contraction bound (1 - q) |S_0| <= M_R + q B_rescaled when the sub-unit base term S_2 = 0; "
                        "induction over arbitrary finite depth J_p(X) = floor(log_p X) is proved analytically in §8.1."
                    ),
                },
            },
            "remaining_open_obligation": {
                "obligation_id": "SUBGATE-TC-043A",
                "status": "OPEN",
                "exact_statement": (
                    "Prove uniform boundedness sup_{X >= 1} |R_{mu,band}(X)| < infty of the localized "
                    "resonant-band Moebius sum R_{mu,band}(X) = sum_{H(X) < m <= M(X)} (mu(m)/sqrt(m)) W_log(X/m) "
                    "with H(X) = floor(X^{5/6}) and M(X) = ceil(max(2, X^{5/4})), or equivalently prove uniform "
                    "O(1) boundedness of the smooth Mertens-weighted integral "
                    "I_{M,band}(X) = int_{H(X)}^{M(X)} M_{H(X)}(t) t^{-3/2} tilde{W}_log(X/t) dt."
                ),
            },
        },
        "section_7_task_tc051_prime_separation_and_summation_by_parts": sec7_tc051,
    }

    roundtrip_check = verify_all_serialized_arb_in_tree(
        report, path_prefix="task_tc050"
    )
    report["section_6_certified_arb_roundtrip_verification"] = roundtrip_check
    return report


def write_tc050_faithful_spectral_realization_artifact(
    output_path: Path = DEFAULT_TC050_ARTIFACT_PATH,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Generate and write data/tc_faithful_tau_arithmetic_spectral_realization.json."""
    report = execute_task_tc050_faithful_spectral_realization_audit(
        prec_bits=prec_bits
    )

    def _clean(obj: Any) -> Any:
        if isinstance(obj, (arb, acb)):
            return str(obj)
        if isinstance(obj, dict):
            return {
                k: _clean(v) for k, v in obj.items() if k != "enclosure_arb"
            }
        if isinstance(obj, (list, tuple)):
            return [_clean(v) for v in obj]
        return obj

    cleaned = _clean(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(cleaned, indent=2, sort_keys=False) + "\n", encoding="utf-8"
    )
    return cleaned


if __name__ == "__main__":
    artifact = write_tc050_faithful_spectral_realization_artifact()
    print(
        f"Wrote {DEFAULT_TC050_ARTIFACT_PATH.relative_to(REPO_ROOT)} "
        f"({artifact['status']})"
    )
