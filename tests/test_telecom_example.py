"""Regression test for the telecom case study's real random-walk samples
(``data/telecom-gaseia/TelecomExample-random.csv``, sourced from the
original PriEsT project), checked against the manuscript's own published
Table tab:preference-freq / tab:rank-order-freq, and against the sigma-mu
table added to the manuscript's new decision-support subsection
(workstream D).

This is a single ~3,555-iteration sample, not the paper's own 20x20,000
protocol, so the tolerance is wider than the school-example checks.
"""
import csv
from pathlib import Path

import numpy as np
import pytest

DATA = Path(__file__).resolve().parent.parent / "data" / "telecom-gaseia" / "TelecomExample-random.csv"
NAMES = ["Fibre", "Powerline", "Microwave", "Satellite"]

# Published in main.tex, Table tab:preference-freq
PUBLISHED_PWI = {
    ("Fibre", "Powerline"): 0.63,
    ("Microwave", "Fibre"): 0.87,
    ("Microwave", "Powerline"): 0.96,
    ("Microwave", "Satellite"): 0.51,
    ("Satellite", "Fibre"): 0.91,
    ("Satellite", "Powerline"): 0.91,
}
# Published in main.tex, Table tab:rank-order-freq
PUBLISHED_RAI_RANK1 = {"Fibre": 0.049, "Powerline": 0.025, "Microwave": 0.473, "Satellite": 0.453}
PUBLISHED_RAI_WORST = {"Fibre": 0.365, "Powerline": 0.622, "Microwave": 0.006, "Satellite": 0.007}
# Published in main.tex, Table tab:sigma-mu-telecom (workstream D)
PUBLISHED_SIGMA_MU = {
    "Fibre": (0.219, 0.042),
    "Powerline": (0.194, 0.047),
    "Microwave": (0.293, 0.037),
    "Satellite": (0.294, 0.041),
}
TOL = 0.02  # single ~3.5k-iteration sample vs. the paper's 20x20,000-iteration protocol


@pytest.fixture(scope="module")
def telecom_scores():
    if not DATA.exists():
        pytest.skip(f"real telecom data not present locally: {DATA}")
    with open(DATA) as f:
        rows = [[float(row["w1"]), float(row["w2"]), float(row["w3"]), float(row["w4"])] for row in csv.DictReader(f)]
    return np.array(rows)  # columns: Fibre, Powerline, Microwave, Satellite


def test_pwi_matches_published_table(telecom_scores):
    idx = {name: i for i, name in enumerate(NAMES)}
    for (a, b), published in PUBLISHED_PWI.items():
        pwi = np.mean(telecom_scores[:, idx[a]] > telecom_scores[:, idx[b]])
        assert abs(pwi - published) < TOL, f"{a} > {b}"


def test_rai_matches_published_table(telecom_scores):
    ranks = np.argsort(np.argsort(-telecom_scores, axis=1), axis=1) + 1  # 1 = best, 4 = worst
    for i, name in enumerate(NAMES):
        assert abs(np.mean(ranks[:, i] == 1) - PUBLISHED_RAI_RANK1[name]) < TOL, name
        assert abs(np.mean(ranks[:, i] == 4) - PUBLISHED_RAI_WORST[name]) < TOL, name


def test_sigma_mu_matches_published_table(telecom_scores):
    for i, name in enumerate(NAMES):
        mu, sigma = PUBLISHED_SIGMA_MU[name]
        assert abs(telecom_scores[:, i].mean() - mu) < TOL, name
        assert abs(telecom_scores[:, i].std() - sigma) < TOL, name


def test_microwave_beats_satellite_on_robustness_not_pwi(telecom_scores):
    # The manuscript's risk-attitude argument (workstream D): PWI ties
    # Microwave and Satellite, but Microwave has both the lower score
    # variance and the lower worst-rank probability of the two.
    idx = {name: i for i, name in enumerate(NAMES)}
    mw, sat = telecom_scores[:, idx["Microwave"]], telecom_scores[:, idx["Satellite"]]
    pwi = np.mean(mw > sat)
    assert abs(pwi - 0.5) < 0.02  # a tie
    assert mw.std() < sat.std()

    ranks = np.argsort(np.argsort(-telecom_scores, axis=1), axis=1) + 1
    worst_mw = np.mean(ranks[:, idx["Microwave"]] == 4)
    worst_sat = np.mean(ranks[:, idx["Satellite"]] == 4)
    assert worst_mw < worst_sat
