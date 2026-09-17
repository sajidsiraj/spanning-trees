"""Consistency and structure diagnostics for PC matrices: consistency
ratio/index (CR), a triad-based congruence measure (CM), intransitive
(Kendall) triad counting, and congruence/dissonance matrices.

Ported from the vendored ``ConsistencyAnalyzer``/``TournamentAnalyzer``/
``IndirectAnalyzer`` Java classes (``code/src/randomspanning/``), including
the exact Saaty random-index table those used -- kept faithful to that
reference rather than re-derived, since those are the numbers the
manuscript's own worked example (CR of M_g1..M_g6, M_criteria) was checked
against.
"""
from __future__ import annotations

import numpy as np

from . import pcmatrix

# Saaty random-index table, indexed by matrix size n (RI[0], RI[1] unused).
_RI = [0.00, 0.00, 1.00, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.51, 1.56, 1.59, 1.60]


def perron_eigenvalue(A: np.ndarray) -> float:
    """The dominant (largest real part) eigenvalue of the PC matrix."""
    B = pcmatrix.build(A)
    return float(np.max(np.linalg.eigvals(B).real))


def cr(A: np.ndarray) -> float:
    """Saaty's consistency ratio: CI / RI(n), where CI = |lambda_max - n| / (n - 1)."""
    B = pcmatrix.build(A)
    n = B.shape[0]
    lam = perron_eigenvalue(B)
    ci = abs(lam - n) / (n - 1)
    if 2 <= n < len(_RI):
        return ci / _RI[n]
    return ci


def cm(A: np.ndarray) -> float:
    """Triad-based congruence measure: the worst-case (maximum) disagreement,
    over every triple (i, j, k), between a direct judgement and what the
    other two legs of the triad imply about it.
    """
    B = pcmatrix.build(A)
    n = B.shape[0]
    worst = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            a = B[i, j]
            for k in range(n):
                if k in (i, j):
                    continue
                b, c = B[i, k], B[j, k]
                if a > 0 and b > 0 and c > 0:
                    cm_a = abs(a - b / c) / a
                    cm_b = abs(b - a * c) / b
                    cm_c = abs(c - b / a) / c
                    worst = max(worst, min(cm_a, cm_b, cm_c))
    return worst


def intransitive_triads(A: np.ndarray) -> set[tuple[int, int, int]]:
    """Every triad (i, j, k) where the direct judgement contradicts the two
    indirect ones (Kendall-style: i beats k, k beats j, but i does not beat
    j). One entry per triad, regardless of how many orderings trigger it.
    """
    B = pcmatrix.build(A)
    n = B.shape[0]
    loops: set[tuple[int, int, int]] = set()
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            a_ij = B[i, j]
            for k in range(n):
                if k in (i, j):
                    continue
                a_ik, a_kj = B[i, k], B[k, j]
                if a_ik > 0 and a_kj > 0 and a_ij > 0 and a_ik > 1 and a_kj > 1 and a_ij < 1:
                    loops.add(tuple(sorted((i, j, k))))
    return loops


def l(A: np.ndarray) -> int:
    """Count of intransitive (Kendall) triads -- see :func:`intransitive_triads`."""
    return len(intransitive_triads(A))


def congruence(A: np.ndarray) -> np.ndarray:
    """Per-judgement congruence matrix: how much a direct judgement A[i, j]
    disagrees, on a log scale, with the indirect judgements implied via
    every other node k.
    """
    return _triad_matrix(A, signed=False)


def dissonance(A: np.ndarray) -> np.ndarray:
    """Per-judgement dissonance matrix: the fraction of indirect judgements
    that disagree in *sign* (log-scale direction) with the direct one.
    """
    return _triad_matrix(A, signed=True)


def _triad_matrix(A: np.ndarray, signed: bool) -> np.ndarray:
    B = pcmatrix.build(A)
    n = B.shape[0]
    out = np.zeros((n, n))
    if n <= 2:
        return out
    for i in range(n):
        for j in range(n):
            if i == j or B[i, j] <= 0:
                continue
            b = np.log(B[i, j])
            total = 0.0
            for k in range(n):
                if k in (i, j):
                    continue
                a_ik, a_kj = B[i, k], B[k, j]
                if a_ik > 0 and a_kj > 0:
                    b2 = np.log(a_ik * a_kj)
                    if signed:
                        total += 1.0 if (b * b2) < 0 else 0.0
                    else:
                        total += abs(b - b2)
            out[i, j] = total / (n - 2)
    return out


def measure(P: np.ndarray) -> float:
    """Reduce a congruence/dissonance matrix to a single scalar: the mean
    of its off-diagonal entries.
    """
    n = P.shape[0]
    return (P.sum() - np.trace(P)) / (n * (n - 1))
