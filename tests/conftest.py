"""Fixtures reproducing the manuscript's own didactic school example
(Saaty's school-selection problem, Section 3.3 / 5.1 of the paper), so the
pipeline can be regression-tested against numbers already published in the
submitted manuscript rather than only against internal consistency checks.

Matrices cross-checked against the original Java code's
``Example_SaatySchool`` (six years old, same author, same case study) --
they match exactly.
"""
import numpy as np
import pytest


@pytest.fixture
def school_criteria_matrices():
    """The six per-criterion alternative-evaluation matrices M_g1..M_g6
    (School A, B, C), as printed in the manuscript.
    """
    return {
        "g1": np.array([  # Learning
            [1, 1 / 3, 1 / 2],
            [3, 1, 3],
            [2, 1 / 3, 1],
        ]),
        "g2": np.array([  # Friends
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]),
        "g3": np.array([  # School life
            [1, 5, 1],
            [1 / 5, 1, 1 / 5],
            [1, 5, 1],
        ]),
        "g4": np.array([  # Vocational training
            [1, 9, 7],
            [1 / 9, 1, 1 / 5],
            [1 / 7, 5, 1],
        ]),
        "g5": np.array([  # Ease of installation-style criterion (5th)
            [1, 1 / 2, 1],
            [2, 1, 2],
            [1, 1 / 2, 1],
        ]),
        "g6": np.array([  # Sixth criterion
            [1, 6, 4],
            [1 / 6, 1, 1 / 3],
            [1 / 4, 3, 1],
        ]),
    }


@pytest.fixture
def school_criteria_weight_matrix():
    """M_criteria: the DM's pairwise comparison of the six criteria
    themselves, as printed in the manuscript.
    """
    return np.array([
        [1, 4, 3, 1, 3, 4],
        [1 / 4, 1, 7, 3, 1 / 5, 1],
        [1 / 3, 1 / 7, 1, 1 / 5, 1 / 5, 1 / 6],
        [1, 1 / 3, 5, 1, 1, 1 / 3],
        [1 / 3, 5, 5, 1, 1, 3],
        [1 / 4, 1, 6, 3, 1 / 3, 1],
    ])


# Numbers as published in the submitted manuscript (main.tex), used as the
# regression targets in test_school_example.py. Rounded to 2 significant
# figures there; the full-enumeration computation is exact, so a tight
# tolerance is appropriate.
PUBLISHED_CRITERIA_WEIGHTS = {  # RGM(M_criteria)
    "g1": 0.32, "g2": 0.14, "g3": 0.03, "g4": 0.13, "g5": 0.24, "g6": 0.14,
}
PUBLISHED_SCORES = {  # RGM(M_gj), Table "Scores for alternatives..."
    "g1": {"A": 0.16, "B": 0.59, "C": 0.25},
    "g2": {"A": 0.33, "B": 0.33, "C": 0.33},
    "g3": {"A": 0.45, "B": 0.09, "C": 0.46},
    "g4": {"A": 0.77, "B": 0.05, "C": 0.17},
    "g5": {"A": 0.25, "B": 0.50, "C": 0.25},
    "g6": {"A": 0.69, "B": 0.09, "C": 0.22},
}
PUBLISHED_OVERALL_SCORES = {"A": 0.37, "B": 0.38, "C": 0.25}
PUBLISHED_TOTAL_COMBINATIONS = 944784  # 6**4 * 3**6
PUBLISHED_PWI_A_GT_C = 0.91
PUBLISHED_PWI_B_GT_C = 0.89
PUBLISHED_RAI_RANK1_A = 0.51
PUBLISHED_RAI_RANK1_B = 0.49
PUBLISHED_RAI_RANK3_C = 0.80
