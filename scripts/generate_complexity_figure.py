"""Regenerates the wall-clock-vs-(m,n) sweep and figure for the manuscript's
computational complexity subsection (workstream D): synthetic reciprocal
PCMs with controlled inconsistency (pcmatrix.random_reciprocal_matrix),
varying m (criteria) and n (alternatives) in {3..8}, timing 20,000
random-walk iterations per (m,n) cell -- the same iteration count used
throughout the paper (Section 4's sample-size formula). Also runs a
lighter stability check (10 replications) at the largest cell, m=n=8, to
confirm estimate variance does not grow with problem size.

Usage: python scripts/generate_complexity_figure.py [output_dir]
Requires matplotlib (see the `figures` extra in pyproject.toml). Takes
around 15-20 minutes; most of the cost is the m=n=8 corner.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from pairwise_graphs import spanning, pcmatrix, consistency

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
OUT.mkdir(parents=True, exist_ok=True)

SIZES = list(range(3, 9))  # m, n in {3, ..., 8}
N_ITERS = 20000
NOISE_SIGMA = 0.35
SEED = 4242


def run_one_cell(m, n, rng, crit=None, alts=None):
    """Time N_ITERS iterations on a random (m, n) problem instance, or on
    a caller-supplied fixed instance (crit, alts) -- pass those when
    measuring estimate stability across repeated runs of the SAME problem,
    since a fresh random instance each time would measure instance-to-
    instance variation, not sampling variation.
    """
    if crit is None:
        crit = pcmatrix.random_reciprocal_matrix(m, NOISE_SIGMA, rng)
    if alts is None:
        alts = [pcmatrix.random_reciprocal_matrix(n, NOISE_SIGMA, rng) for _ in range(m)]
    scores = np.empty((N_ITERS, n))
    t0 = time.time()
    for k in range(N_ITERS):
        w = spanning.aldous_broder_priority_vector(crit, rng)
        u = np.array([spanning.aldous_broder_priority_vector(A, rng) for A in alts])
        scores[k] = w @ u
    elapsed = time.time() - t0
    pwi_01 = float(np.mean(scores[:, 0] > scores[:, 1])) if n >= 2 else None
    return {
        "wall_clock_s": elapsed,
        "criteria_cr": float(consistency.cr(crit)),
        "pwi_0_gt_1": pwi_01,
    }


def main():
    rng = np.random.default_rng(SEED)
    grid = {}
    for m in SIZES:
        for n in SIZES:
            result = run_one_cell(m, n, rng)
            grid[f"{m},{n}"] = result
            print(f"m={m} n={n}: {result['wall_clock_s']:.1f}s, "
                  f"criteria CR={result['criteria_cr']:.3f}, "
                  f"PWI(0>1)={result['pwi_0_gt_1']:.3f}", flush=True)

    # stability check: 10 repeated runs on ONE FIXED instance at the largest
    # cell (a fresh random instance per replication would measure instance-
    # to-instance variation, not sampling variation -- see run_one_cell).
    m = n = SIZES[-1]
    fixed_crit = pcmatrix.random_reciprocal_matrix(m, NOISE_SIGMA, rng)
    fixed_alts = [pcmatrix.random_reciprocal_matrix(n, NOISE_SIGMA, rng) for _ in range(m)]
    stability_pwis = []
    for rep in range(10):
        result = run_one_cell(m, n, rng, crit=fixed_crit, alts=fixed_alts)
        stability_pwis.append(result["pwi_0_gt_1"])
        print(f"stability rep {rep}: PWI(0>1)={result['pwi_0_gt_1']:.4f}", flush=True)
    stability = {
        "m": m, "n": n,
        "criteria_cr": float(consistency.cr(fixed_crit)),
        "pwis": stability_pwis,
        "empirical_sd": float(np.std(stability_pwis, ddof=1)),
        "mean": float(np.mean(stability_pwis)),
    }
    p_hat = stability["mean"]
    stability["theoretical_sd"] = float(np.sqrt(p_hat * (1 - p_hat) / N_ITERS))

    (OUT / "complexity-summary.json").write_text(json.dumps({
        "grid": grid, "stability": stability, "n_iters": N_ITERS, "noise_sigma": NOISE_SIGMA,
    }, indent=2))

    # heatmap of wall-clock time
    heat = np.array([[grid[f"{m},{n}"]["wall_clock_s"] for n in SIZES] for m in SIZES])
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    im = ax.imshow(heat, origin="lower", cmap="viridis")
    ax.set_xticks(range(len(SIZES)), SIZES)
    ax.set_yticks(range(len(SIZES)), SIZES)
    ax.set_xlabel("$n$ (alternatives)")
    ax.set_ylabel("$m$ (criteria)")
    for i in range(len(SIZES)):
        for j in range(len(SIZES)):
            ax.text(j, i, f"{heat[i, j]:.0f}", ha="center", va="center",
                     color="white" if heat[i, j] < heat.max() * 0.6 else "black", fontsize=7)
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Wall-clock, 20,000 iterations (s)")
    ax.set_title("Sampling cost vs. problem size\n(synthetic reciprocal PCMs, moderate inconsistency)", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "complexity-sweep.pdf")


if __name__ == "__main__":
    main()
