"""Full enumeration over a complete PC matrix must produce exactly
Cayley's k**(k-2) spanning trees -- a cheap, exact check that our PC
matrix -> graph wiring (not just networkx's enumerator) is correct.
"""
import numpy as np
import pytest

from pairwise_graphs import spanning


@pytest.mark.parametrize("n", [3, 4, 5, 6])
def test_full_enumeration_matches_cayley_formula(n):
    A = np.ones((n, n))  # a fully consistent, fully complete PC matrix
    count = sum(1 for _ in spanning.enumerate_priority_vectors(A))
    assert count == n ** (n - 2)
