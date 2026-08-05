import itertools
import unittest
import os
import sys

import numpy as np

import definitive_screening_design as dsd

PARENTDIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PARENTDIR)


class TestA(unittest.TestCase):
    def test_primes(self):
        self.assertEqual(
            list(map(dsd._generalized_dsd.isprime, [2371, 2927, 6949, 6948, 1249, 3739, 9311])),
            [True, True, True, False, True, True, True],
        )

    def test_example(self):
        self.assertEqual(dsd.design.generate(n_num=3, n_cat=2).shape, (14, 5))

    def test_10(self):
        self.assertEqual(dsd.design.generate(10).shape[0], 21)

    def test_continuous_designs_have_defining_properties(self):
        for k in range(4, 18):
            with self.subTest(k=k):
                design = dsd.design.generate(n_num=k, min_13=False, verbose=False).to_numpy(dtype=float)
                rows = {tuple(row) for row in design}
                self.assertTrue(all(tuple(-row) in rows for row in design))

                np.testing.assert_allclose(design.sum(axis=0), 0)
                gram = design.T @ design
                np.testing.assert_allclose(gram - np.diag(np.diag(gram)), 0)

                for i, j in itertools.combinations(range(k), 2):
                    interaction = design[:, i] * design[:, j]
                    np.testing.assert_allclose(design.T @ interaction, 0)


if __name__ == "__main__":
    unittest.main()
