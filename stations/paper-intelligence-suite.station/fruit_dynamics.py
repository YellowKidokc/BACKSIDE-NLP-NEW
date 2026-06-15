"""
fruit_dynamics.py — Canonical Fruits of the Spirit dynamical system.

Recovered 2026-04-07 from:
    O:\\Vault\\AI-Chats History\\2025-04-16_Divine Physics Equations_1393.md
    (Section: Spiritual_Math_Refactor_v0.2, line 458)

This module implements the actual mathematical framework for the Fruits of
the Spirit — NOT a lexicon, but a 9-dimensional state vector evolving under
faith-driven logistic dynamics, with a salvation phase transition gated by
the L2 norm of the fruit vector.

Equations
---------
Fruit ODE (per fruit i):
    d𝔽_i/dt = β_i · φ(t) · (1 − 𝔽_i)

Faith ODE (driver):
    dφ/dt = α·W̄(t) + β·Ē(t) − c·φ

Salvation phase transition (sigmoid on L2 norm):
    ζ = 1 / (1 + exp(−k_sig · (‖𝔽‖₂ − θ)))

Faith network amplification (multiplicative into χ):
    Φ_faith = γ · (1 + Σ F_i · exp(−d_i))^p

Canonical doc: O:\\_Theophysics_v4\\00_Canonical\\FRUITS_OF_SPIRIT_EQUATIONS.md
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Callable, Sequence

import numpy as np
from scipy.integrate import solve_ivp

# Force UTF-8 stdout on Windows so Greek letters in the smoke test print
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass


# ---------------------------------------------------------------------------
# 1. The 9 Galatians fruits, in canonical order
# ---------------------------------------------------------------------------

FRUIT_NAMES: tuple[str, ...] = (
    "love",
    "joy",
    "peace",
    "patience",
    "kindness",
    "goodness",
    "faithfulness",
    "gentleness",
    "self_control",
)

N_FRUITS = len(FRUIT_NAMES)  # == 9


# ---------------------------------------------------------------------------
# 2. Parameters (defaults are placeholders — calibration is an OPEN TASK)
# ---------------------------------------------------------------------------

@dataclass
class FruitParams:
    """Calibration constants for the fruit dynamical system.

    All defaults are reasonable placeholders; none of them are fitted to
    real data yet. See OPEN_IDEAS / Section 8 of the canonical doc.
    """

    # Per-fruit growth rates β_i (one per Galatians fruit)
    beta: np.ndarray = field(
        default_factory=lambda: np.full(N_FRUITS, 0.35)
    )

    # Faith ODE: dφ/dt = α·W̄ + β_e·Ē − c·φ
    alpha_word: float = 0.5      # Word intake coupling
    beta_experience: float = 0.4  # Experience intake coupling
    faith_decay: float = 0.1      # base decay constant c₀
    obedience_inertia: float = 0.0  # ι; effective c = c₀ / (1 + ι)

    # Salvation phase transition
    k_sig: float = 4.0    # sigmoid sharpness
    theta: float = 1.5    # phase transition threshold (on ‖𝔽‖₂, max 3)

    # Faith network gain Φ_faith
    gamma: float = 1.0
    p: float = 1.5  # non-linearity exponent (1 ≤ p ≤ 2)

    def __post_init__(self) -> None:
        self.beta = np.asarray(self.beta, dtype=float)
        if self.beta.shape != (N_FRUITS,):
            raise ValueError(
                f"beta must have shape ({N_FRUITS},), got {self.beta.shape}"
            )

    @property
    def effective_faith_decay(self) -> float:
        return self.faith_decay / (1.0 + self.obedience_inertia)


# ---------------------------------------------------------------------------
# 3. Core equations
# ---------------------------------------------------------------------------

def fruit_rhs(
    F: np.ndarray,
    phi: float,
    params: FruitParams,
) -> np.ndarray:
    """Right-hand side of d𝔽/dt = β · φ · (1 − 𝔽).

    Parameters
    ----------
    F : array of shape (9,)
        Current fruit vector, components in [0, 1].
    phi : float
        Current faith store, in [0, 1].
    params : FruitParams

    Returns
    -------
    array of shape (9,) — d𝔽/dt
    """
    F = np.clip(np.asarray(F, dtype=float), 0.0, 1.0)
    return params.beta * phi * (1.0 - F)


def faith_rhs(
    phi: float,
    word_intake: float,
    experience_intake: float,
    params: FruitParams,
) -> float:
    """dφ/dt = α·W̄ + β_e·Ē − c·φ."""
    return (
        params.alpha_word * word_intake
        + params.beta_experience * experience_intake
        - params.effective_faith_decay * phi
    )


def salvation_state(F: np.ndarray, params: FruitParams) -> float:
    """Salvation phase transition ζ = sigmoid(k_sig · (‖𝔽‖₂ − θ)).

    Note: this is the L2 norm version (v0.2 refactor), not the naive sum.
    The L2 norm forces breadth across all 9 fruits — you cannot compensate
    for zero self-control with extra joy.
    """
    F = np.asarray(F, dtype=float)
    norm = float(np.linalg.norm(F, ord=2))
    z = params.k_sig * (norm - params.theta)
    return 1.0 / (1.0 + np.exp(-z))


def utility_of_salvation(zeta: float) -> float:
    """U(ζ) = ζ·(1 − ζ). Peaks at ζ = 0.5 (the phase transition point)."""
    return zeta * (1.0 - zeta)


def faith_network_gain(
    F_network: Sequence[float],
    distances: Sequence[float],
    params: FruitParams,
) -> float:
    """Φ_faith = γ · (1 + Σ F_i · exp(−d_i))^p.

    Parameters
    ----------
    F_network : faith intensities of network nodes (NOT the fruit vector)
    distances : spiritual distances d_i = −ln(L_i · V_i · I_i)
    """
    F_arr = np.asarray(F_network, dtype=float)
    d_arr = np.asarray(distances, dtype=float)
    if F_arr.shape != d_arr.shape:
        raise ValueError("F_network and distances must have same shape")
    inner = 1.0 + float(np.sum(F_arr * np.exp(-d_arr)))
    return params.gamma * (inner ** params.p)


def spiritual_distance(love: float, values: float, interaction: float) -> float:
    """d_i = −ln(L_i · V_i · I_i), clipped to avoid log(0)."""
    product = max(love * values * interaction, 1e-9)
    return float(-np.log(product))


def normalize_observable(z_score: float) -> float:
    """Logistic squash of a z-scored composite into [0, 1].

    Source eq:  F_i = 1 + 9 / (1 + exp(−z))   (in [1, 10])
    Here we return the [0, 1] form for fruit vector use.
    """
    return 1.0 / (1.0 + np.exp(-z_score))


# ---------------------------------------------------------------------------
# 4. Coupled ODE integrator (faith + fruit vector)
# ---------------------------------------------------------------------------

@dataclass
class FruitTrajectory:
    t: np.ndarray              # shape (T,)
    phi: np.ndarray            # shape (T,)
    F: np.ndarray              # shape (T, 9)
    zeta: np.ndarray           # shape (T,)
    fruit_norm: np.ndarray     # shape (T,)


def integrate_fruit_dynamics(
    *,
    t_span: tuple[float, float],
    F0: np.ndarray | None = None,
    phi0: float = 0.05,
    word_intake: Callable[[float], float] = lambda t: 0.6,
    experience_intake: Callable[[float], float] = lambda t: 0.4,
    params: FruitParams | None = None,
    n_eval: int = 200,
) -> FruitTrajectory:
    """Integrate the coupled (φ, 𝔽) system over t_span.

    word_intake / experience_intake are functions of time so you can drive
    the system with a Word/Experience signal extracted from a paper or a
    biographical timeline.
    """
    params = params or FruitParams()
    F0 = np.zeros(N_FRUITS) if F0 is None else np.asarray(F0, dtype=float)
    if F0.shape != (N_FRUITS,):
        raise ValueError(f"F0 must have shape ({N_FRUITS},)")

    y0 = np.concatenate(([phi0], F0))

    def rhs(t: float, y: np.ndarray) -> np.ndarray:
        phi = y[0]
        F = y[1:]
        dphi = faith_rhs(phi, word_intake(t), experience_intake(t), params)
        dF = fruit_rhs(F, phi, params)
        return np.concatenate(([dphi], dF))

    t_eval = np.linspace(t_span[0], t_span[1], n_eval)
    sol = solve_ivp(
        rhs,
        t_span,
        y0,
        t_eval=t_eval,
        method="RK45",
        rtol=1e-6,
        atol=1e-9,
    )
    if not sol.success:
        raise RuntimeError(f"ODE integration failed: {sol.message}")

    phi_t = sol.y[0]
    F_t = sol.y[1:].T  # shape (T, 9)
    zeta_t = np.array([salvation_state(F, params) for F in F_t])
    norm_t = np.linalg.norm(F_t, ord=2, axis=1)

    return FruitTrajectory(
        t=sol.t,
        phi=phi_t,
        F=F_t,
        zeta=zeta_t,
        fruit_norm=norm_t,
    )


# ---------------------------------------------------------------------------
# 5. Smoke test
# ---------------------------------------------------------------------------

def _smoke_test() -> None:
    print("=" * 60)
    print("FRUIT DYNAMICS SMOKE TEST")
    print("=" * 60)

    params = FruitParams()
    print(f"\n9 fruits: {FRUIT_NAMES}")
    print(f"β vector: {params.beta}")
    print(f"Effective faith decay: {params.effective_faith_decay:.3f}")

    # Static checks
    F_zero = np.zeros(N_FRUITS)
    F_full = np.ones(N_FRUITS)
    F_partial = np.array([0.5] * N_FRUITS)
    print("\n--- Salvation state ---")
    print(f"  ζ(F=0)        = {salvation_state(F_zero, params):.4f}")
    print(f"  ζ(F=0.5·𝟙)    = {salvation_state(F_partial, params):.4f}")
    print(f"  ζ(F=𝟙)        = {salvation_state(F_full, params):.4f}")
    print(f"  ‖𝟙‖₂          = {np.linalg.norm(F_full):.4f}")

    # Network term
    print("\n--- Faith network ---")
    network_F = [0.8, 0.6, 0.9, 0.4]
    distances = [
        spiritual_distance(0.9, 0.8, 0.7),
        spiritual_distance(0.6, 0.5, 0.6),
        spiritual_distance(0.95, 0.9, 0.95),
        spiritual_distance(0.3, 0.4, 0.2),
    ]
    print(f"  d_i           = {[f'{d:.2f}' for d in distances]}")
    print(f"  Φ_faith       = {faith_network_gain(network_F, distances, params):.4f}")

    # Time integration
    print("\n--- Coupled ODE integration over t ∈ [0, 50] ---")
    traj = integrate_fruit_dynamics(
        t_span=(0.0, 50.0),
        word_intake=lambda t: 0.7,
        experience_intake=lambda t: 0.5,
        params=params,
        n_eval=200,
    )
    print(f"  φ(0)  = {traj.phi[0]:.4f}   φ(50) = {traj.phi[-1]:.4f}")
    print(f"  ‖𝔽‖₂(0) = {traj.fruit_norm[0]:.4f}")
    print(f"  ‖𝔽‖₂(50) = {traj.fruit_norm[-1]:.4f}")
    print(f"  ζ(0)  = {traj.zeta[0]:.4f}   ζ(50) = {traj.zeta[-1]:.4f}")
    print("\n  Final fruit vector:")
    for name, val in zip(FRUIT_NAMES, traj.F[-1]):
        print(f"    {name:<14} = {val:.4f}")

    # Find approximate phase transition crossing
    crossings = np.where(np.diff(np.sign(traj.zeta - 0.5)))[0]
    if len(crossings) > 0:
        t_cross = traj.t[crossings[0]]
        print(f"\n  ζ crosses 0.5 (phase transition) at t ≈ {t_cross:.2f}")
    else:
        print("\n  ζ never crosses 0.5 in this run.")

    print("\nAll equations operational. Don't lose this again.")
    print("=" * 60)


if __name__ == "__main__":
    _smoke_test()
