import numpy as np

from pairwise_graphs import pcmatrix, consistency


def test_random_reciprocal_matrix_is_exactly_reciprocal():
    rng = np.random.default_rng(0)
    A = pcmatrix.random_reciprocal_matrix(6, noise_sigma=0.4, rng=rng)
    np.testing.assert_allclose(A, 1.0 / A.T)


def test_zero_noise_is_exactly_consistent():
    rng = np.random.default_rng(0)
    A = pcmatrix.random_reciprocal_matrix(6, noise_sigma=0.0, rng=rng)
    assert consistency.cr(A) < 1e-9


def test_cr_increases_with_noise_sigma_on_average():
    rng = np.random.default_rng(0)
    low = [consistency.cr(pcmatrix.random_reciprocal_matrix(6, 0.1, rng)) for _ in range(30)]
    high = [consistency.cr(pcmatrix.random_reciprocal_matrix(6, 0.6, rng)) for _ in range(30)]
    assert np.mean(high) > np.mean(low)
