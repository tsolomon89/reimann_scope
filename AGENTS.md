# Riemann Scope: AI Agent Operations & Mathematical Claim Protocol

This file serves as the canonical operating manual and entrypoint for AI coding agents operating in `reimann_scope`.

## 0. Mandatory Root Rule

> **An unresolved or failed mathematical check creates a research obligation. It does not authorize a success claim, a universal obstruction claim, or termination of the mission. Structural validation does not establish mathematical truth. Consequential conclusions must identify their exact evidence and scope and pass the applicable independent review. Missing evidence remains missing. Agents must continue deriving, computing, falsifying, or refining while meaningful authorized work and execution resources remain.**

---

## 1. Startup and Resumption Protocol

Whenever initiating or resuming a work session, the agent must execute these steps in order:
1. **Repository & Workspace Baseline Inspection**:
   - Inspect git HEAD, working tree status (`git status`), and ensure no uncommitted artifacts or conflicting state exist.
   - Preserve valid modularization work (including `tc/` and facade `transcendental.py`).
   - Do NOT create a competing lowercase `agents.md` on case-insensitive Windows filesystems; the canonical entrypoints are root `AGENTS.md` and `.agents/AGENTS.md`.
2. **Persistent Mission State Inspection**:
   - Check `.agents/research/state.json` and `.agents/research/queue.json` for current active obligations, open research questions, and previous runs.
   - Review relevant execution artifacts in `research/runs/` via `research/index.json`.
3. **Repository Verification Health**:
   - Run the fast operational tier:
     ```bash
     python scripts/workflow.py check-fast
     ```
   - Run the claim register and spec cross-check:
     ```bash
     python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --cross-check-register --repo-root .
     ```
4. **Autonomous Continuation**:
   - Select the highest-priority open obligation from `.agents/research/queue.json`.
   - Do not stop after documentation changes or passing tests. Proceed autonomously to derive, calculate, falsify, or refine.

---

## 2. Primary Research Objective & Mathematical Constraints

### Core Reductio Implication
The primary research obligation remains:
$$H \Longrightarrow \exists K \ne J, \; m, n \in \mathbb{Z} \setminus \{0\} : m \tau^K = n \tau^J, \qquad \tau = 2\pi,$$
where $H$ denotes the existence of an off-critical nontrivial Riemann zeta zero ($\operatorname{Re}(\rho) \ne 1/2$). The forbidden coincidence $m \tau^K = n \tau^J$ ($K \ne J$) is the intended contradictory conclusion of the reductio ad absurdum, never a reason to dismiss or abort the derivation.

### Auxiliary Weil Route & Constraints
- **Separation of Auxiliary Routes**: The auxiliary Weil route (positivity vs. conditional negative-witness detection) must concern the same precisely specified family and functional form.
- **Genuine Targets vs. Fits**: Generic smooth target fits do not establish detection. A poor fit does not refute the original implication.
- **Authentic Arithmetic Family**: Preserve actual prime-power stations, von Mangoldt weights $\Lambda(n) = \log p$ (for $n = p^k$), common scale parameter $h$ and window $w$ within any combination, and one coefficient per grade:
  $$F_{K,h,w} = a_K T_{K,h,w}, \qquad a_K = \tau^K, \qquad \sum_K c_K T_K = \sum_K b_K F_K, \quad c_K = a_K b_K.$$
- **Controls & Distinctions**: Any independent station coefficients or modified weights must be explicitly labeled as non-standard diagnostic controls. Keep existential diagonal convergence and its hypotheses strictly separate from practical schedules, effective rates, and finite experimental outcomes.

---

## 3. Evidence-Dependent Acceptance & Status Dimensions

Acceptance is strictly evidence-dependent. Execution status, structural validity, numerical resolution, mathematical conclusion, formalization coverage, independent-review status, and research progress must remain separated across distinct dimensions:

### Explicit Status Classes
- `PROPOSED`: Formulated hypothesis with precise mathematical specification; evaluation pending.
- `EMPIRICAL`: Floating-point or high-precision numerical observation on a discrete grid or finite sample. Does not establish universal bounds or exact non-vanishing.
- `NUMERICALLY_UNRESOLVED`: Numerical investigation yielded ambiguous, insufficient precision, or discretization-dominated results. Constitutes an active research obligation.
- `CERTIFIED_FINITE`: Certified interval enclosure (e.g. Arb ball arithmetic) over a declared finite compact domain or point witness with rigorous error budget.
- `PROVED_CONDITIONAL`: Deductively verified proof or formal Lean theorem under an explicitly declared, unresolved premise.
- `REFUTED_WITHIN_SCOPE`: Counterexample or falsification established for a specific candidate class or parameter region.
- `AWAITING_INDEPENDENT_REVIEW`: Derivation or computation complete, awaiting independent red-team or formal review artifact.
- `SPECIFICATION_SCHEMA_PASSED`: Machine-readable specification conforms structurally to the schema. Does NOT imply mathematical validity.
- `INDEPENDENT_MATHEMATICAL_AUDIT_PASSED`: Verified mathematical proof, formal Lean verification (0 sorry), adversarial falsification review, and independent derivation review.

### Consequential Claim Requirements
For every consequential accepted claim:
1. **Exact Statement**: Quantifiers, hypotheses, family, parameters, normalization, and claimed scope.
2. **Evidence Class**: Explicitly state whether the conclusion is finite, conditional, sampled, asymptotic, or universal.
3. **Executable Verification**: Command line, raw evidence location, artifact hash, and declared dependencies.
4. **Source & Environment Provenance**: Git commit, input digests, precision/tolerances, and reproduction environment.
5. **Independent Review**: Review artifact in `.agents/claims/reviews/<CLAIM_ID>-derivation-review.md` bound to the exact input digest, containing objections, attempted falsification, resolution, and remaining obligations.
6. **No Self-Certification**: An author/producer cannot approve their own claim; empty paragraphs, filename mentions, or self-asserted flags do not constitute independent review.

---

## 4. Grandfathered Legacy Manifest & Exceptional Baseline Migrations

- Legacy unmigrated claims are anchored to the immutable git baseline commit (`82643cafd605492233c6c1e992b78c2c30d45f13`) in `.agents/corpus_map/legacy_claim_manifest.json`.
- Any modification to a legacy claim or new claim proposal strictly requires a validated `.agents/claims/<CLAIM_ID>.json` specification passing all mandatory gates.
- Grandfathered status represents legacy unmigrated data, NEVER independent mathematical verification.
- Modifying `baseline_commit` or regenerating the legacy manifest is an **exceptional migration requiring explicit user authorization**. Agents must never advance the baseline commit autonomously.

---

## 5. Verification Workflow Commands

Always verify repository health using the standard command tiers:
- **Fast Tier**: `python scripts/workflow.py check-fast`
- **Claim Register Audit**: `python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --cross-check-register --repo-root .`
- **Artifact Validation**: `python scripts/workflow.py validate-artifacts --current`
- **Formal Verification**: `python scripts/build_formal.py` (or `lake build` in `formal/`)
- **Canonical Plan Audit**: `python scripts/workflow.py plan-canonical`

---

## 6. Complete-Form Spectral Enclosures & Numerical Control Rigor

1. **Decoupled Numerical Controls**:
   Physical integration cutoffs ($U$) and discretization resolutions ($N_t$) must be controlled as independent variables. When using $U = z_{\max} / h$, increasing bandwidth $h$ while holding $z_{\max}$ fixed truncates the physical frequency domain.
2. **Complete Enclosures for Negative Witnesses vs. Positive Margins**:
   For any truncated quadratic form decomposition $B(G, G) = B_{\le U}(G, G) + R_U(G, G)$:
   - If $R_U \succeq 0$, zero provides a rigorous lower bound for the tail, but claiming a negative witness strictly requires an analytic upper bound on the omitted tail: $B(G, G) \le B_{\le U}(G, G) + \text{TailUpperBound} < 0$. Truncation alone never authorizes a negative witness.
   - For positive margins, lower bounds on $B_{\le U}$ combined with $R_U \ge 0$ establish positivity, provided discretization and interpolation errors are bounded by an analytic theorem rather than observed mesh differences.
3. **Absolute Remainder Theorems over Heuristic Differences**:
   Differences between refined meshes ($\Delta N_t$) or empirical interpolation discrepancies do not bound distance from the exact continuous functional. Analytic remainder bounds or certified ball arithmetic are strictly required.
4. **Quadratic Functional Consistency**:
   All explicit formula tail estimates, arithmetic margins, and zero contributions must compute the identical quadratic functional and obey homogeneity $B(\lambda G, \lambda G) = |\lambda|^2 B(G, G)$. Linear explicit formula bounds cannot be transferred without explicit quadratic profile derivation.
5. **No Intermediate Spectral Gaps**:
   Spectral zero accounting must not omit intermediate intervals (e.g. $[100, 1000]$). Every zero up to the tail cutoff must be explicitly accounted for, with completeness bounds and conjugate pairs.

