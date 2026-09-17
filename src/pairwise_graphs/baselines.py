"""Classic point-estimate priority-elicitation methods, kept here as
baselines to compare the spanning-tree distribution against (workstream C).

Both require a complete PC matrix: unlike the spanning-tree sampling in
:mod:`pairwise_graphs.spanning`, there is no meaningful way to run REV or
RGM on a matrix with a genuinely missing (not just reciprocal-fillable)
judgement.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import gmean

from . import pcmatrix


def _require_complete(A: np.ndarray, method: str) -> np.ndarray:
    B = pcmatrix.build(A)
    if np.isnan(B).any():
        missing = list(zip(*np.where(np.isnan(B))))
        raise ValueError(f"{method} requires a complete PC matrix; missing entries: {missing}")
    return B


def rev(A: np.ndarray) -> np.ndarray:
    """Right Eigenvector method (Saaty): the principal eigenvector of the
    PC matrix, normalised to sum to 1.
    """
    B = _require_complete(A, "REV")
    eigvals, eigvecs = np.linalg.eig(B)
    idx = int(np.argmax(eigvals.real))
    v = np.abs(eigvecs[:, idx].real)
    return v / v.sum()


def rgm(A: np.ndarray) -> np.ndarray:
    """Row Geometric Mean method: the geometric mean of each row,
    normalised to sum to 1.
    """
    B = _require_complete(A, "RGM")
    v = gmean(B, axis=1)
    return v / v.sum()
