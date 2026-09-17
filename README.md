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
  consistency.py  CR, CM, intransitive (Kendall) triad count, congruence, dissonance --
                   ported from the vendored ConsistencyAnalyzer/TournamentAnalyzer/
                   IndirectAnalyzer Java classes, including their exact RI table
```

Setup:

```
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pytest
```

The test suite reproduces the manuscript's own published didactic
school-example numbers (PWI, RAI, RGM scores, CR) via full enumeration, as
the strongest available validation -- see `tests/test_school_example.py`
and `tests/test_consistency.py`. It also checks GMAST against RGM on real
(not just trivially consistent) matrices, confirming Lundy2017's proven
equivalence numerically -- see `tests/test_rgm_equivalence.py`.
