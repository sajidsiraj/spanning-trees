"""Regenerates the ablation data and figure for the manuscript's
"Robustness to missing judgements" subsection (workstream E), on the
school example's criteria matrix and its effect on PWI(A>C).

Ablates two missingness patterns at matched degree: random (150 trials per
degree) and structured (isolating one criterion entirely, one edge at a
time). Takes several minutes -- most of the cost is the full-enumeration
PWI recomputation at low degrees, where the criteria matrix is still close
to complete and so has close to its maximum 1,296 spanning trees.

Usage: python scripts/generate_incomplete_data_figure.py [output_dir]
Requires matplotlib (see the `figures` extra in pyproject.toml).
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
from pairwise_graphs import spanning, pcmatrix

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
N_TRIALS = 150
SEED = 2026

PAIRS = [(i, j) for i in range(6) for j in range(i + 1, 6)]


def _alt_matrix():
    per_criterion = [np.array(list(spanning.enumerate_priority_vectors(M_G[g]))) for g in ORDER]
    combo_index = np.array(list(itertools.product(range(3), repeat=6)))
    alt_matrix = np.empty((combo_index.shape[0], 6, 3))
    for j in range(6):
        alt_matrix[:, j, :] = per_criterion[j][combo_index[:, j]]
    return alt_matrix


ALT_MATRIX = _alt_matrix()


def pwi_a_gt_c(A_crit: np.ndarray) -> float:
    weights = np.array(list(spanning.enumerate_priority_vectors(A_crit)))
    scores = np.einsum("wj,cjk->wck", weights, ALT_MATRIX).reshape(-1, 3)
    return float(np.mean(scores[:, 0] > scores[:, 2]))


def run_random_ablation(rng):
    results = {}
    for degree in range(13):
        n_trials = N_TRIALS if degree > 0 else 1
        connected, pwis = 0, []
        for _ in range(n_trials):
            A = M_CRITERIA.copy()
            if degree > 0:
                for k in rng.choice(len(PAIRS), size=degree, replace=False):
                    i, j = PAIRS[k]
                    A[i, j] = A[j, i] = np.nan
            if pcmatrix.is_connected(A):
                connected += 1
                pwis.append(pwi_a_gt_c(A))
        results[degree] = {
            "connectivity_rate": connected / n_trials,
            "pwi_mean": float(np.mean(pwis)) if pwis else None,
            "pwi_std": float(np.std(pwis)) if pwis else None,
            "n_connected": len(pwis),
        }
        print(f"random degree {degree}: connectivity={results[degree]['connectivity_rate']:.2f}, "
              f"pwi_mean={results[degree]['pwi_mean']}", flush=True)
    return results


def run_structured_ablation(node_to_isolate=5):
    results = {}
    A = M_CRITERIA.copy()
    results[0] = {"connected": True, "pwi": pwi_a_gt_c(A)}
    for d, i in enumerate(range(node_to_isolate), start=1):
        A[i, node_to_isolate] = A[node_to_isolate, i] = np.nan
        connected = pcmatrix.is_connected(A)
        results[d] = {"connected": connected, "pwi": pwi_a_gt_c(A) if connected else None}
        print(f"structured degree {d}: connected={connected}, pwi={results[d]['pwi']}", flush=True)
    return results


def make_figure(ground_truth, random_results, structured_results):
    degrees = sorted(random_results)
    r_mean = np.array([random_results[d]["pwi_mean"] for d in degrees], dtype=float)
    r_std = np.array([random_results[d]["pwi_std"] if random_results[d]["pwi_std"] is not None else np.nan
                       for d in degrees], dtype=float)
    r_conn = [random_results[d]["connectivity_rate"] * 100 for d in degrees]
    valid = ~np.isnan(r_mean)
    d_arr = np.array(degrees)

    s_degrees = sorted(structured_results)
    s_connected_degrees = [d for d in s_degrees if structured_results[d]["connected"]]
    last_connected = max(s_connected_degrees)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6), sharex=True, height_ratios=[2.2, 1])

    ax1.plot(d_arr[valid], r_mean[valid], "-o", color="#2b6cb0", ms=4,
              label=f"Random missingness (mean over {N_TRIALS} trials)")
    ax1.fill_between(d_arr[valid], r_mean[valid] - r_std[valid], r_mean[valid] + r_std[valid],
                       color="#2b6cb0", alpha=0.15, label="Random missingness ($\\pm 1$ SD)")
    ax1.plot(s_connected_degrees, [structured_results[d]["pwi"] for d in s_connected_degrees],
              "-s", color="#c53030", ms=5, label="Structured missingness (isolating one criterion)")
    ax1.axvline(last_connected + 1, color="#c53030", ls=":", lw=1.2)
    ax1.annotate("disconnects here\n(structured)", xy=(last_connected + 1, 0.83), color="#c53030",
                  fontsize=8, ha="center")
    ax1.axhline(ground_truth, color="black", ls="--", lw=0.8, label=f"Ground truth ({ground_truth:.4f})")
    ax1.set_ylabel("$PWI(A\\succ C)$")
    ax1.set_ylim(0.75, 1.02)
    ax1.legend(loc="lower left", fontsize=7.5)
    ax1.set_title("Effect of missing judgements on $PWI(A\\succ C)$\n(school example, criteria matrix)", fontsize=10)

    ax2.plot(degrees, r_conn, "-o", color="#2b6cb0", ms=4)
    ax2.axvline(last_connected + 1, color="#c53030", ls=":", lw=1.2)
    ax2.set_ylabel("Connectivity rate\n(random, \\%)")
    ax2.set_xlabel("Missingness degree (number of judgements removed out of 15)")
    ax2.set_ylim(-5, 105)

    fig.tight_layout()
    fig.savefig(OUT / "incomplete-data-ablation.pdf")


def main():
    ground_truth = pwi_a_gt_c(M_CRITERIA)
    rng = np.random.default_rng(SEED)
    random_results = run_random_ablation(rng)
    structured_results = run_structured_ablation()

    (OUT / "ablation-summary.json").write_text(json.dumps({
        "ground_truth": ground_truth,
        "random": random_results,
        "structured": structured_results,
    }, indent=2))

    make_figure(ground_truth, random_results, structured_results)


if __name__ == "__main__":
    main()
