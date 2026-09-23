# spanning-trees
[M10] Spanning Trees Analysis

## pairwise-graphs (Python)

The active codebase. The original Java implementation (`code/`, `data/`)
is kept for reference only and is no longer maintained.

```
src/pairwise_graphs/
  pcmatrix.py     PC matrix <-> graph construction (handles incomplete matrices)
  spanning.py     full enumeration and uniform random sampling of spanning trees;
                   EAST/GMAST (arithmetic/geometric mean of the spanning-tree population)
  baselines.py    REV, RGM (comparison methods for workstream C)
  consistency.py  CR, CM, intransitive (Kendall) triad count, congruence, dissonance,
                   ported from the vendored ConsistencyAnalyzer/TournamentAnalyzer/
                   IndirectAnalyzer Java classes, including their exact RI table
```

## Data

`data/telecom-A.csv` through `data/telecom-goal.csv` and `data/telecom-gaseia/`
are the pairwise comparison matrices for the telecom backbone case study used
in the manuscript. The underlying judgements were collected and published by
Gasiea, Emsley and Mikhailov (2023), "Rural telecommunications infrastructure
selection using the analytic network process," Journal of Telecommunications
and Information Technology. We use them here, with citation, to reproduce
and validate our own analysis on a real published dataset, not as our own
collected data.

Setup:

```
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pytest
```

The test suite reproduces the manuscript's own published didactic
school-example numbers (PWI, RAI, RGM scores, CR) via full enumeration, as
the strongest available validation. See `tests/test_school_example.py`
and `tests/test_consistency.py`. It also checks GMAST against RGM on real
(not just trivially consistent) matrices, confirming Lundy2017's proven
equivalence numerically. See `tests/test_rgm_equivalence.py`.
