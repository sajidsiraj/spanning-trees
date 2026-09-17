"""Regenerates the two figures and summary statistics for the manuscript's
"Independence and convergence of the random-walk estimator" subsection
(workstream A), on the school example's PWI(A>C).

Usage: python scripts/generate_convergence_figures.py [output_dir]
Requires matplotlib (not a runtime dependency of the package itself --
install separately, e.g. `pip install matplotlib`).
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from pairwise_graphs import spanning

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
OUT.mkdir(parents=True, exist_ok=True)

M_CRITERIA = np.array([
    [1, 4, 3, 1, 3, 4], [1 / 4, 1, 7, 3, 1 / 5, 1], [1 / 3, 1 / 7, 1, 1 / 5, 1 / 5, 1 / 6],
    [1, 1 / 3, 5, 1, 1, 1 / 3], [1 / 3, 5, 5, 1, 1, 3], [1 / 4, 1, 6, 3, 1 / 3, 1],
])
M_G = {
    "g1": np.array([[1, 1 / 3, 1 / 2], [3, 1, 3], [2, 1 / 3, 1]]),
    "g2": np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
    "g3": np.array([[1, 5, 1], [1 / 5, 1, 1 / 5], [1, 5, 1]]),
    "g4": np.array([[1, 9, 7], [1 / 9, 1, 1 / 5], [1 / 7, 5, 1]]),
    "g5": np.array([[1, 1 / 2, 1], [2, 1, 2], [1, 1 / 2, 1]]),
    "g6": np.array([[1, 6, 4], [1 / 6, 1, 1 / 3], [1 / 4, 3, 1]]),
}
ORDER = ["g1", "g2", "g3", "g4", "g5", "g6"]
N = 20000
N_EXPERIMENTS = 20
SEED = 12345


def exact_pwi_a_gt_c():
    per_criterion = [np.array(list(spanning.enumerate_priority_vectors(M_G[g]))) for g in ORDER]
    weights = np.array(list(spanning.enumerate_priority_vectors(M_CRITERIA)))
    combo_index = np.array(list(itertools.product(range(3), repeat=6)))
    alt_matrix = np.empty((combo_index.shape[0], 6, 3))
    for j in range(6):
        alt_matrix[:, j, :] = per_criterion[j][combo_index[:, j]]
    scores = np.einsum("wj,cjk->wck", weights, alt_matrix).reshape(-1, 3)
    return float(np.mean(scores[:, 0] > scores[:, 2]))


def draw_indicator_sequence(rng, n):
    ind = np.empty(n, dtype=bool)
    for k in range(n):
        w = spanning.aldous_broder_priority_vector(M_CRITERIA, rng)
        u = np.array([spanning.aldous_broder_priority_vector(M_G[g], rng) for g in ORDER])
        score = w @ u
        ind[k] = score[0] > score[2]
    return ind


def acf(x, max_lag):
    x = x - x.mean()
    denom = np.dot(x, x)
    return np.array([1.0] + [np.dot(x[:-lag], x[lag:]) / denom for lag in range(1, max_lag + 1)])


def main():
    ground_truth = exact_pwi_a_gt_c()
    rng_master = np.random.default_rng(SEED)

    pwi_per_experiment = []
    running_mean_exp1 = None
    indicator_exp1 = None
    for exp in range(N_EXPERIMENTS):
        rng = np.random.default_rng(rng_master.integers(0, 2**31 - 1))
        indicators = draw_indicator_sequence(rng, N)
        pwi_per_experiment.append(indicators.mean())
        if exp == 0:
            running_mean_exp1 = np.cumsum(indicators) / np.arange(1, N + 1)
            indicator_exp1 = indicators.astype(float)

    pwi_per_experiment = np.array(pwi_per_experiment)
    p_hat = pwi_per_experiment.mean()
    empirical_sd = pwi_per_experiment.std(ddof=1)
    theoretical_sd = np.sqrt(p_hat * (1 - p_hat) / N)

    acf_vals = acf(indicator_exp1, max_lag=30)
    lag1 = acf_vals[1]
    ess = N * (1 - lag1) / (1 + lag1)

    summary = {
        "N": N, "N_EXPERIMENTS": N_EXPERIMENTS,
        "exact_ground_truth_pwi_a_gt_c": ground_truth,
        "mean_pwi_ac": float(p_hat),
        "empirical_sd": float(empirical_sd),
        "theoretical_sd": float(theoretical_sd),
        "lag1_autocorr": float(lag1),
        "ess": float(ess),
    }
    (OUT / "convergence-summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

    fig, ax = plt.subplots(figsize=(6, 3.8))
    iters = np.arange(1, N + 1)
    ax.plot(iters, running_mean_exp1, lw=0.8, color="#2b6cb0", label="Running-mean $\\widehat{PWI}(A\\succ C)$")
    ax.axhline(ground_truth, color="#c53030", ls="--", lw=1.2, label=f"Exact population value ({ground_truth:.4f})")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Running-mean estimate of $PWI(A\\succ C)$")
    ax.set_xscale("log")
    ax.set_ylim(0.80, 1.00)
    ax.legend(loc="lower right", fontsize=8)
    ax.set_title("Convergence of the random-walk PWI estimate\n(school example, $A \\succ C$)", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "convergence-pwi.pdf")

    fig, ax = plt.subplots(figsize=(6, 3.2))
    lags = np.arange(0, 31)
    ci = 1.96 / np.sqrt(N)
    ax.stem(lags, acf_vals, basefmt=" ", linefmt="#2b6cb0", markerfmt="o")
    ax.axhline(ci, color="#c53030", ls="--", lw=1, label="95\\% CI under independence")
    ax.axhline(-ci, color="#c53030", ls="--", lw=1)
    ax.set_xlabel("Lag")
    ax.set_ylabel("Autocorrelation")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc="upper right", fontsize=8)
    ax.set_title("Autocorrelation of the PWI indicator sequence\n(school example, $A \\succ C$, $N=20{,}000$)", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "autocorrelation-pwi.pdf")


if __name__ == "__main__":
    main()
