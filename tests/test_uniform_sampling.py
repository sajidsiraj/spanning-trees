"""The random-walk sampler's *marginal distribution over spanning trees*
must be uniform (this is the property Section 5 of the paper leans on for
using PWI/RAI estimated from samples). Checked via chi-square goodness of
fit against full enumeration on a small graph.
"""
import numpy as np
import networkx as nx
from scipy.stats import chisquare

from pairwise_graphs import pcmatrix


def _tree_id(tree: nx.Graph) -> frozenset:
    # edge tuples aren't canonically ordered (e.g. (3, 1) vs (1, 3) for the
    # same undirected edge), so sort each pair before hashing the tree
    return frozenset(tuple(sorted(e)) for e in tree.edges())


def test_random_spanning_tree_is_uniform():
    n = 4  # 4**2 = 16 spanning trees: enough classes for a real chi-square test
    A = np.ones((n, n))
    G = pcmatrix.to_graph(A)

    population = [_tree_id(t) for t in nx.SpanningTreeIterator(G)]
    assert len(population) == n ** (n - 2)

    rng = np.random.default_rng(12345)
    n_samples = 4000
    counts = {tid: 0 for tid in population}
    for _ in range(n_samples):
        seed = int(rng.integers(0, 2**31 - 1))
        tree = nx.random_spanning_tree(G, weight=None, seed=seed)
        counts[_tree_id(tree)] += 1

    observed = np.array(list(counts.values()))
    expected = np.full(len(population), n_samples / len(population))
    _, p_value = chisquare(observed, expected)
    assert p_value > 0.01, f"sampling looks non-uniform (p={p_value})"
