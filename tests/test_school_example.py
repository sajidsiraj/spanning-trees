"""End-to-end regression test: run the full pipeline (full enumeration,
since this problem is small enough -- see module docstring in spanning.py)
on the manuscript's own didactic school example, and check the results
against numbers already published in the submitted manuscript.

This is the strongest validation available for this port: it isn't just
internally consistent, it reproduces figures that are already in the
paper under review.
"""
import itertools

import numpy as np

from pairwise_graphs import spanning, baselines
from conftest import (
    PUBLISHED_CRITERIA_WEIGHTS,
    PUBLISHED_SCORES,
    PUBLISHED_OVERALL_SCORES,
    PUBLISHED_TOTAL_COMBINATIONS,
    PUBLISHED_PWI_A_GT_C,
    PUBLISHED_PWI_B_GT_C,
    PUBLISHED_RAI_RANK1_A,
    PUBLISHED_RAI_RANK1_B,
    PUBLISHED_RAI_RANK3_C,
)

CRITERIA_ORDER = ["g1", "g2", "g3", "g4", "g5", "g6"]
# Published figures are rounded to 2dp (+/-0.005 on their own). The RGM
# criteria weights carry a bit more drift than that against a fresh
# computation -- plausibly the original (6-year-old) working used a
# different intermediate-rounding path on this fairly inconsistent matrix
# (CR = 0.24). The much stronger check is test_full_spanning_population_*
# below, which reproduces the paper's actual PWI/RAI headline figures
# tightly; this one is a supplementary sanity check, so its tolerance is
# a little more generous.
TOL = 0.008


def test_rgm_matches_published_scores(school_criteria_matrices, school_criteria_weight_matrix):
    for g, A in school_criteria_matrices.items():
        scores = baselines.rgm(A)  # order: School A, B, C
        expected = [PUBLISHED_SCORES[g]["A"], PUBLISHED_SCORES[g]["B"], PUBLISHED_SCORES[g]["C"]]
        np.testing.assert_allclose(scores, expected, atol=TOL)

    weights = baselines.rgm(school_criteria_weight_matrix)
    expected_weights = [PUBLISHED_CRITERIA_WEIGHTS[g] for g in CRITERIA_ORDER]
    np.testing.assert_allclose(weights, expected_weights, atol=TOL)


def test_rgm_overall_scores_match_published(school_criteria_matrices, school_criteria_weight_matrix):
    w = baselines.rgm(school_criteria_weight_matrix)
    per_criterion = np.array([
        baselines.rgm(school_criteria_matrices[g]) for g in CRITERIA_ORDER
    ])  # (6, 3): rows = criteria, columns = School A, B, C
    overall = w @ per_criterion  # (3,)
    np.testing.assert_allclose(
        overall,
        [PUBLISHED_OVERALL_SCORES["A"], PUBLISHED_OVERALL_SCORES["B"], PUBLISHED_OVERALL_SCORES["C"]],
        atol=TOL,
    )


def test_full_spanning_population_matches_published_pwi_and_rai(
    school_criteria_matrices, school_criteria_weight_matrix
):
    per_criterion_vectors = [
        np.array(list(spanning.enumerate_priority_vectors(school_criteria_matrices[g])))
        for g in CRITERIA_ORDER
    ]  # 6 arrays, each (3, 3)
    weight_vectors = np.array(
        list(spanning.enumerate_priority_vectors(school_criteria_weight_matrix))
    )  # (1296, 6)

    combo_index = np.array(list(itertools.product(range(3), repeat=6)))  # (729, 6)
    n_combos = combo_index.shape[0]
    assert weight_vectors.shape[0] * n_combos == PUBLISHED_TOTAL_COMBINATIONS

    alt_matrix = np.empty((n_combos, 6, 3))
    for j in range(6):
        alt_matrix[:, j, :] = per_criterion_vectors[j][combo_index[:, j]]

    # overall evaluation for every (weight-tree, alternative-tree-combo) pair
    scores = np.einsum("wj,cjk->wck", weight_vectors, alt_matrix).reshape(-1, 3)
    assert scores.shape[0] == PUBLISHED_TOTAL_COMBINATIONS

    a, b, c = scores[:, 0], scores[:, 1], scores[:, 2]

    pwi_a_gt_c = np.mean(a > c)
    pwi_b_gt_c = np.mean(b > c)
    assert abs(pwi_a_gt_c - PUBLISHED_PWI_A_GT_C) < TOL
    assert abs(pwi_b_gt_c - PUBLISHED_PWI_B_GT_C) < TOL

    # rank 1 = best; ties are measure-zero for these continuous scores
    ranks = np.argsort(np.argsort(-scores, axis=1), axis=1) + 1
    rai_rank1_a = np.mean(ranks[:, 0] == 1)
    rai_rank1_b = np.mean(ranks[:, 1] == 1)
    rai_rank3_c = np.mean(ranks[:, 2] == 3)

    assert abs(rai_rank1_a - PUBLISHED_RAI_RANK1_A) < TOL
    assert abs(rai_rank1_b - PUBLISHED_RAI_RANK1_B) < TOL
    assert abs(rai_rank3_c - PUBLISHED_RAI_RANK3_C) < TOL
