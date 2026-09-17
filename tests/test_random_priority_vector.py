"""random_priority_vector actually exercised end to end -- this is the gap
that let a real bug through: nx.random_spanning_tree doesn't copy edge
attributes onto the tree it returns (nx.SpanningTreeIterator does), so
every earlier test exercising only enumerate_priority_vectors passed while
random_priority_vector silently raised on first use.
"""
import numpy as np

from pairwise_graphs import spanning


def test_random_priority_vector_is_a_valid_probability_vector():
    A = np.array([[1, 1 / 3, 1 / 2], [3, 1, 3], [2, 1 / 3, 1]])
    v = spanning.random_priority_vector(A, seed=42)
    assert v.shape == (3,)
    assert np.all(v >= 0)
    assert abs(v.sum() - 1.0) < 1e-9


def test_random_priority_vector_large_n_converges_to_east(school_criteria_matrices):
    A = school_criteria_matrices["g1"]
    ground_truth = spanning.east(A)  # exact, via full enumeration (independently tested elsewhere)

    rng = np.random.default_rng(0)
    samples = np.array([
        spanning.random_priority_vector(A, seed=int(rng.integers(0, 2**31 - 1)))
        for _ in range(3000)
    ])
    empirical_mean = samples.mean(axis=0)
    np.testing.assert_allclose(empirical_mean, ground_truth, atol=0.02)
