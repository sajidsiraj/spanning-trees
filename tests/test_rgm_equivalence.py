"""For a fully (cardinally) consistent PC matrix, every spanning tree
represents the same underlying judgement, so the whole distribution should
collapse to a single point -- and that point should equal both REV and RGM.
This is the equivalence Lundy2017 established for the spanning-tree method;
it's a strong, closed-form check with no manuscript numbers needed.
"""
import numpy as np

from pairwise_graphs import spanning, baselines


def test_consistent_matrix_collapses_to_rev_and_rgm():
    w_true = np.array([1.0, 2.0, 4.0, 8.0, 0.5])
    A = w_true[:, None] / w_true[None, :]  # exactly consistent by construction

    vectors = list(spanning.enumerate_priority_vectors(A))
    assert len(vectors) == len(w_true) ** (len(w_true) - 2)

    first = vectors[0]
    for v in vectors[1:]:
        np.testing.assert_allclose(v, first, atol=1e-9)

    np.testing.assert_allclose(first, baselines.rev(A), atol=1e-9)
    np.testing.assert_allclose(first, baselines.rgm(A), atol=1e-9)
    np.testing.assert_allclose(first, w_true / w_true.sum(), atol=1e-9)


def test_gmast_matches_rgm_on_real_inconsistent_matrices(
    school_criteria_matrices, school_criteria_weight_matrix
):
    """The trivial case above (a fully consistent matrix) passes almost by
    definition -- every spanning tree gives the same vector regardless of
    the aggregation rule. The real claim (Lundy2017) is that GMAST, the
    *geometric* mean of the spanning-tree population, exactly equals RGM
    even when the matrix is genuinely inconsistent. Checked here against
    the manuscript's own school-example matrices, including M_criteria
    (CR = 0.24, the most inconsistent matrix in the whole example).
    """
    matrices = list(school_criteria_matrices.values()) + [school_criteria_weight_matrix]
    for A in matrices:
        np.testing.assert_allclose(spanning.gmast(A), baselines.rgm(A), atol=1e-9)
