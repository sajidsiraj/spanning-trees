"""Pairwise comparison (PC) matrices, represented as weighted graphs.

Convention: for a PC matrix ``A`` of size ``n x n``, ``A[i, j]`` is the
decision maker's judgement of how many times alternative/criterion ``i`` is
preferred over ``j`` (so ``A[i, j] == 1 / A[j, i]`` when both are given).
A missing judgement is represented as ``numpy.nan`` -- the matrix need not
be complete. The diagonal is not used and can be left as ``nan`` or ``1``.
"""
from __future__ import annotations

import numpy as np
import networkx as nx


def build(A: np.ndarray) -> np.ndarray:
    """Fill in reciprocal entries: if ``A[i, j]`` is given but ``A[j, i]``
    is not, set ``A[j, i] = 1 / A[i, j]``. Returns a new array; does not
    mutate the input.
    """
    n = A.shape[0]
    B = np.array(A, dtype=float, copy=True)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if np.isnan(B[i, j]) and not np.isnan(B[j, i]):
                B[i, j] = 1.0 / B[j, i]
    return B


def ratio(A: np.ndarray, i: int, j: int) -> float:
    """The judgement of ``i`` relative to ``j``, using whichever of
    ``A[i, j]`` / ``A[j, i]`` was actually given.
    """
    if not np.isnan(A[i, j]):
        return float(A[i, j])
    if not np.isnan(A[j, i]):
        return 1.0 / float(A[j, i])
    raise KeyError(f"no judgement given for ({i}, {j})")


def to_graph(A: np.ndarray) -> nx.Graph:
    """Convert a PC matrix into an undirected weighted graph: one node per
    alternative/criterion, one edge per judgement actually given. A missing
    judgement is simply not an edge -- incompleteness needs no special
    handling beyond this.

    The edge weight stored is ``A[i, j]`` for the canonical direction
    ``i < j`` (so ``weight > 1`` means ``i`` is preferred over ``j``);
    :func:`ratio` recovers the judgement in either direction.
    """
    n = A.shape[0]
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if not np.isnan(A[i, j]) or not np.isnan(A[j, i]):
                G.add_edge(i, j, weight=ratio(A, i, j))
    return G


def is_connected(A: np.ndarray) -> bool:
    """Whether enough judgements were given to compare every alternative
    to every other, directly or transitively. A disconnected graph means
    genuine incomparability, not just missing data (see the paper's
    incomplete-data discussion, Section 3.2).
    """
    return nx.is_connected(to_graph(A))
