import unittest
import warnings

import numpy as np

from definitive_screening_design.analysis import (
    get_efficiency,
    get_map_of_correlations,
    get_variance,
)


class TestAnalysis(unittest.TestCase):
    def test_correlations_leave_constant_terms_undefined_without_warning(self):
        design = np.array(
            [
                [-1.0, -1.0],
                [-1.0, 1.0],
                [1.0, -1.0],
                [1.0, 1.0],
            ]
        )

        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            correlations = get_map_of_correlations(
                design,
                effects=("intercept", "main", "quadratic"),
                plot=False,
            )

        np.testing.assert_allclose(correlations[:2, :2], np.eye(2))
        self.assertTrue(np.isnan(correlations[2:, :]).all())
        self.assertTrue(np.isnan(correlations[:, 2:]).all())

    def test_efficiency_is_zero_for_rank_deficient_model_without_warning(self):
        design = np.array([[-1.0], [1.0]])

        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            efficiency = get_efficiency(
                design, effects=("intercept", "main", "quadratic")
            )

        self.assertEqual(efficiency["D-Efficiency (%)"], 0.0)
        self.assertEqual(efficiency["A-Efficiency (%)"], 0.0)

    def test_efficiency_matches_direct_full_rank_calculation(self):
        design = np.array([[-1.0], [0.0], [1.0]])
        X = np.column_stack(
            (np.ones(3), design[:, 0], design[:, 0] ** 2)
        )
        information = X.T @ X
        n_trials, n_params = X.shape
        expected_d = (
            100.0
            * np.linalg.det(information) ** (1.0 / n_params)
            / n_trials
        )
        expected_a = (
            100.0
            * n_params
            / (n_trials * np.trace(np.linalg.inv(information)))
        )

        efficiency = get_efficiency(
            design, effects=("intercept", "main", "quadratic")
        )

        np.testing.assert_allclose(
            efficiency["D-Efficiency (%)"], expected_d
        )
        np.testing.assert_allclose(
            efficiency["A-Efficiency (%)"], expected_a
        )

    def test_prediction_variance_returns_diagonal_for_each_point(self):
        design = np.array([[-1.0], [0.0], [1.0]])
        points = np.array([[-1.0, 0.0, 1.0]])
        X = np.column_stack((np.ones(3), design[:, 0]))
        Xp = np.column_stack((np.ones(3), points[0]))
        expected = np.diag(Xp @ np.linalg.inv(X.T @ X) @ Xp.T)

        actual = get_variance(
            points, design, effects=("intercept", "main")
        )

        np.testing.assert_allclose(actual, expected)

    def test_prediction_variance_rejects_nonestimable_model(self):
        design = np.array([[-1.0], [1.0]])
        points = np.array([[0.0]])

        with self.assertRaisesRegex(
            np.linalg.LinAlgError, "rank deficient"
        ):
            get_variance(
                points,
                design,
                effects=("intercept", "main", "quadratic"),
            )


if __name__ == "__main__":
    unittest.main()
