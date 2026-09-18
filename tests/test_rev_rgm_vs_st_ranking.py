"""Regression test for the manuscript's "Comparison with point-estimate
methods" subsection (workstream H): REV/RGM ranks vs the spanning trees
approach's expected and most-probable rank, both examples.
"""
import csv
import itertools
from pathlib import Path

import numpy as np
import pytest

from pairwise_graphs import spanning, baselines

CRITERIA_ORDER = ["g1", "g2", "g3", "g4", "g5", "g6"]
TELECOM_DATA = Path(__file__).resolve().parent.parent / "data" / "telecom-gaseia" / "TelecomExample-random.csv"


def _expected_and_mode_rank(scores):
    ranks = np.argsort(np.argsort(-scores, axis=1), axis=1) + 1
    n = scores.shape[1]
    expected = ranks.mean(axis=0)
    mode = [int(np.argmax([np.mean(ranks[:, i] == r) for r in range(1, n + 1)]) + 1) for i in range(n)]
    return expected, mode


def test_school_rev_and_rgm_agree_and_match_published(school_criteria_matrices, school_criteria_weight_matrix):
    rev_w = baselines.rev(school_criteria_weight_matrix)
    rgm_w = baselines.rgm(school_criteria_weight_matrix)
    rev_u = np.array([baselines.rev(school_criteria_matrices[g]) for g in CRITERIA_ORDER])
    rgm_u = np.array([baselines.rgm(school_criteria_matrices[g]) for g in CRITERIA_ORDER])
    rev_overall = rev_w @ rev_u
    rgm_overall = rgm_w @ rgm_u

    # Published RGM overall scores: u(A)=0.37, u(B)=0.38, u(C)=0.25
    np.testing.assert_allclose(rgm_overall, [0.37, 0.38, 0.25], atol=0.01)
    # REV and RGM agree on the ranking (both put B first, A second, C third)
    assert np.argsort(-rev_overall).tolist() == [1, 0, 2]
    assert np.argsort(-rgm_overall).tolist() == [1, 0, 2]


def test_school_st_expected_and_mode_rank_ties_a_and_b(school_criteria_matrices, school_criteria_weight_matrix):
    per_criterion = [np.array(list(spanning.enumerate_priority_vectors(school_criteria_matrices[g])))
                      for g in CRITERIA_ORDER]
    weights = np.array(list(spanning.enumerate_priority_vectors(school_criteria_weight_matrix)))
    combo_index = np.array(list(itertools.product(range(3), repeat=6)))
    alt_matrix = np.empty((combo_index.shape[0], 6, 3))
    for j in range(6):
        alt_matrix[:, j, :] = per_criterion[j][combo_index[:, j]]
    scores = np.einsum("wj,cjk->wck", weights, alt_matrix).reshape(-1, 3)

    expected, mode = _expected_and_mode_rank(scores)
    # A's expected rank is (marginally) better than B's -- reversed from REV/RGM's B > A
    assert expected[0] < expected[1] < expected[2]
    np.testing.assert_allclose(expected, [1.58, 1.62, 2.80], atol=0.02)
    assert mode == [1, 1, 3]


def test_telecom_st_expected_and_mode_rank_ties_microwave_and_satellite():
    if not TELECOM_DATA.exists():
        pytest.skip(f"real telecom data not present locally: {TELECOM_DATA}")
    with open(TELECOM_DATA) as f:
        rows = [[float(row["w1"]), float(row["w2"]), float(row["w3"]), float(row["w4"])]
                for row in csv.DictReader(f)]
    scores = np.array(rows)  # Fibre, Powerline, Microwave, Satellite

    expected, mode = _expected_and_mode_rank(scores)
    # Microwave's expected rank is (marginally) better than Satellite's, matching
    # PWI(Microwave>Satellite)=0.51 -- opposite of REV/RGM's confident Satellite > Microwave
    assert expected[2] < expected[3]
    np.testing.assert_allclose(expected, [3.14, 3.50, 1.67, 1.70], atol=0.05)
    assert mode == [3, 4, 1, 1]
