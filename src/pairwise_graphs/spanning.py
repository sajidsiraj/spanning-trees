"""Spanning-tree sampling: turning a PC matrix into a priority vector, or a
distribution over priority vectors.

Two ways to explore the population of coherent preference vectors:

- :func:`enumerate_priority_vectors` -- exact, via full enumeration of every
  spanning tree. Only tractable for small problems (see the paper's own
  discussion of why the telecom case study cannot use this).
- :func:`random_priority_vector` -- one sample, drawn uniformly at random
  over the spanning trees, via Wilson's algorithm (loop-erased random
  walk). This is the practical route for larger problems; it gives the same
  uniformity guarantee the paper's Aldous--Broder citation relies on, via a
  different (and generally more efficient) construction.
"""
from __future__ import annotations

from typing import Iterator, Optional

import numpy as np
import networkx as nx

from . import pcmatrix


def _edge_ratio(source_graph: nx.Graph, frm: int, to: int) -> float:
    """Judgement of ``to`` relative to ``frm``, looked up from the
    *original* PC graph -- never from the tree itself. Not every networkx
    spanning-tree function copies edge attributes onto the tree it returns
    (``SpanningTreeIterator`` does; ``random_spanning_tree`` does not), so
    the tree is used purely for its structure (which nodes connect to
    which), and every ratio is resolved against ``source_graph``.
    """
    w = source_graph[frm][to]["weight"]
    return w if to == min(frm, to) else 1.0 / w


def _normalize(w: np.ndarray) -> np.ndarray:
    w = np.abs(w)
    total = w.sum()
    return w / total if total > 0 else w


def extract_priority_vector(tree: nx.Graph, source_graph: nx.Graph, root: Optional[int] = None) -> np.ndarray:
    """Given a spanning tree (a subset of ``source_graph``'s edges
    connecting every node), propagate judgement ratios out from an
    arbitrary root to obtain one priority vector, normalised to sum to 1.
    """
    nodes = sorted(tree.nodes())
    if root is None:
        root = nodes[0]
    w = {root: 1.0}
    for frm, to in nx.dfs_edges(tree, source=root):
        w[to] = w[frm] * _edge_ratio(source_graph, frm, to)
    return _normalize(np.array([w[i] for i in nodes], dtype=float))


def enumerate_priority_vectors(A: np.ndarray) -> Iterator[np.ndarray]:
    """Yield the priority vector for every spanning tree of the PC matrix
    ``A`` in turn (i.e. exact, complete enumeration -- see module docstring
    for when this is and isn't tractable).
    """
    G = pcmatrix.to_graph(A)
    for tree in nx.SpanningTreeIterator(G):
        yield extract_priority_vector(tree, G)


def random_priority_vector(A: np.ndarray, seed=None) -> np.ndarray:
    """One priority vector, drawn from a spanning tree sampled uniformly at
    random (Wilson's algorithm via networkx). ``seed`` may be an int, a
    ``numpy.random.Generator``, or ``None``.
    """
    G = pcmatrix.to_graph(A)
    tree = nx.random_spanning_tree(G, weight=None, seed=seed)
    return extract_priority_vector(tree, G)


def aldous_broder_priority_vector(A: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """One priority vector, via a direct Aldous--Broder random walk: walk
    the graph uniformly at random until every node has been visited,
    keeping the edge used to first reach each node.

    This is the specific algorithm the paper cites (\\citep{Aldous1990,
    Broder1989}) -- unlike :func:`random_priority_vector` (Wilson's
    algorithm via networkx, used elsewhere in this package for its
    generality), this is a lean from-scratch implementation, because
    networkx's per-call overhead (~25ms even on a 6-node graph, dominated
    by its own bookkeeping rather than the walk itself) makes it
    impractical for the hundreds of thousands of draws a convergence/
    autocorrelation study needs. Both give the same uniformity guarantee;
    this one is used only where volume matters.
    """
    G = pcmatrix.to_graph(A)
    nodes = list(G.nodes())
    current = nodes[0]
    visited = {current}
    tree = nx.Graph()
    tree.add_nodes_from(nodes)
    while len(visited) < len(nodes):
        neighbours = list(G.neighbors(current))
        nxt = neighbours[rng.integers(len(neighbours))]
        if nxt not in visited:
            tree.add_edge(current, nxt)
            visited.add(nxt)
        current = nxt
    return extract_priority_vector(tree, G)


def east(A: np.ndarray) -> np.ndarray:
    """Arithmetic mean of every spanning tree's priority vector (Siraj2012).
    Full-enumeration only -- see module docstring.
    """
    vectors = np.array(list(enumerate_priority_vectors(A)))
    return vectors.mean(axis=0)  # already sums to 1: mean of unit-sum vectors


def gmast(A: np.ndarray) -> np.ndarray:
    """Geometric mean of every spanning tree's priority vector (Lundy2017),
    proven equivalent to RGM on the original matrix -- see
    ``tests/test_rgm_equivalence.py`` for a numeric check of that claim on
    real (inconsistent) data. Full-enumeration only -- see module docstring.
    """
    vectors = np.array(list(enumerate_priority_vectors(A)))
    log_mean = np.mean(np.log(vectors), axis=0)
    return _normalize(np.exp(log_mean))
