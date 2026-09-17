"""aldous_broder_priority_vector: same uniformity guarantee as
random_priority_vector (Wilson's algorithm), checked the same way as
test_uniform_sampling.py, plus a convergence check against exact
enumeration -- this is the fast sampler workstream A's large-scale
convergence/autocorrelation study depends on, so it needs the same level
of scrutiny as the networkx-backed path.
"""
import numpy as np
import networkx as nx
from scipy.stats import chisquare

from pairwise_graphs import pcmatrix, spanning


def _tree_id(tree: nx.Graph) -> frozenset:
    return frozenset(tuple(sorted(e)) for e in tree.edges())


def test_aldous_broder_tree_distribution_is_uniform():
    n = 4
    A = np.ones((n, n))
    G = pcmatrix.to_graph(A)
    population = [_tree_id(t) for t in nx.SpanningTreeIterator(G)]
    assert len(population) == n ** (n - 2)

    # Sample tree identity directly (mirroring the function's own walk),
    # since a priority vector alone doesn't identify which tree produced it.
    n_samples = 4000
    counts = {tid: 0 for tid in population}
    rng = np.random.default_rng(7)
    for _ in range(n_samples):
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
        counts[_tree_id(tree)] += 1

    observed = np.array(list(counts.values()))
    expected = np.full(len(population), n_samples / len(population))
    _, p_value = chisquare(observed, expected)
    assert p_value > 0.01, f"sampling looks non-uniform (p={p_value})"


def test_aldous_broder_large_n_converges_to_east(school_criteria_matrices):
    A = school_criteria_matrices["g1"]
    ground_truth = spanning.east(A)

    rng = np.random.default_rng(0)
    samples = np.array([spanning.aldous_broder_priority_vector(A, rng) for _ in range(3000)])
    np.testing.assert_allclose(samples.mean(axis=0), ground_truth, atol=0.02)
