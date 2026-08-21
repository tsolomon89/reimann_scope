# Mathematical Dependency and Invariant Map

```mermaid
graph TD
    A[Native Zeta Function ζ(s)] --> B[Transcendental Continuation Z_tau(s, k)]
    B --> C[Zero Worldlines s_ρ(k) = τ^k ρ]
    C --> D[Radial Leaves R_tau = δ]
    D --> E[Bilateral Defect D_K = 4 sinh^2(K δ ln τ / 2)]
    A --> F[Explicit Formula Converter J_N(x), π_N(x)]
    F --> G[Coupled Scale Covariance C_J(x^(1/A), Aρ) = C_J(x, ρ)]
    A --> H[Derivative-Normalized Path P_n(u)]
    H --> I[Cross-Height Taylor Coefficients c_2,n, c_3,n]
    E --> J[Proof Firewall: Local/Finite Empirical Results != Proof]
    G --> J
    I --> J
    J --> K[Formal Lean 4 Verification Targets]
```
