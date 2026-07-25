"""Tools to analyse a DOE and the response collected with it."""

from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


DEFAULT_MODEL_EFFECTS = ("intercept", "main", "2-interactions", "quadratic")


def get_X(A, effects=DEFAULT_MODEL_EFFECTS, return_names=False):
    """Build the model matrix for a design and requested effects.

    If ``return_names`` is true, also return the polynomial term names.
    """

    nfactors = A.shape[1]
    arrays_to_stack = []
    names = []

    if "intercept" in effects:
        names.append("(1)")
        arrays_to_stack.append(np.ones(len(A)).reshape(-1, 1))
    if "main" in effects:
        for i in range(nfactors):
            names.append(f"X{i+1}")
        arrays_to_stack.append(A)
    else:
        raise Exception("Main effects should be present!")
    if "2-interactions" in effects:
        for i, j in combinations(range(nfactors), 2):
            names.append(f"X{i+1}*X{j+1}")
            arrays_to_stack.append((A[:, i] * A[:, j]).reshape(-1, 1))
    if "3-interactions" in effects:
        for i, j, k in combinations(range(nfactors), 3):
            names.append(f"X{i+1}*X{j+1}*X{k+1}")
            arrays_to_stack.append((A[:, i] * A[:, j] * A[:, k]).reshape(-1, 1))
    if "quadratic" in effects:
        for i in range(A.shape[1]):
            names.append(f"X{i+1}^2")
            arrays_to_stack.append((A[:, i] * A[:, i]).reshape(-1, 1))

    X = np.hstack(arrays_to_stack)

    if return_names:
        return X, names
    else:
        return X


def get_efficiency(A, effects=("intercept", "main")):
    """https://www.jmp.com/support/help/Evaluate_Design_Window.shtml#168318
    p = n_params
    n = n_trials

    NOTE: G-Efficiency and I-Efficiency require a grid or Monte Carlo evaluation
          of the variance (see get_variance) in the whole design space
          (typically -1 to 1 in every factor dimension).
    """
    X = np.asarray(get_X(A, effects=effects), dtype=float)
    n_trials, n_params = X.shape

    # Work with the singular values of X rather than det(X.T @ X) and its
    # inverse.  This avoids spurious negative determinants from round-off and
    # makes the non-estimable case explicit.
    singular_values = np.linalg.svd(X, compute_uv=False)
    if singular_values.size < n_params:
        rank = singular_values.size
    elif singular_values.size == 0:
        rank = 0
    else:
        tolerance = (
            singular_values[0]
            * max(X.shape)
            * np.finfo(singular_values.dtype).eps
        )
        rank = np.count_nonzero(singular_values > tolerance)

    if rank < n_params:
        D_eff = 0.0
        A_eff = 0.0
    else:
        # det(X.T @ X) = product(s_i**2).  Accumulating in log space is
        # stable even when the determinant itself would under/overflow.
        D_eff = (
            100.0
            * np.exp(2.0 * np.mean(np.log(singular_values)))
            / n_trials
        )
        A_eff = (
            100.0
            * n_params
            / (n_trials * np.sum(singular_values**-2))
        )

    return {
        "Number of Trials": n_trials,
        "Number of Parameters": n_params,
        "D-Efficiency (%)": D_eff,
        "A-Efficiency (%)": A_eff,
    }


def get_variance(x, A, effects=("intercept", "main")):
    """https://www.jmp.com/support/help/Evaluate_Design_Window.shtml#168318
    x is a numpy.array vertical vector
    """
    n_factors, n_samples = x.shape

    x_copy = x.copy()

    if "intercept" in effects:
        x = np.vstack([np.ones([1, n_samples]), x])
    if "main" not in effects:
        raise Exception("Main effects should be present!")
    if "2-interactions" in effects:
        for i, j in combinations(range(n_factors), 2):
            xixj = x_copy[i, :] * x_copy[j, :]
            x = np.vstack([x, xixj])
    if "3-interactions" in effects:
        for i, j, k in combinations(range(n_factors), 3):
            xixjxk = x_copy[i, :] * x_copy[j, :] * x_copy[k, :]
            x = np.vstack([x, xixjxk])
    if "quadratic" in effects:
        x = np.vstack([x, x_copy**2])

    X = get_X(A, effects=effects)
    XTX = np.dot(X.T, X)
    if np.linalg.matrix_rank(X) < X.shape[1]:
        raise np.linalg.LinAlgError(
            "Prediction variance is undefined because the requested model "
            "matrix is rank deficient."
        )
    information_inverse = np.linalg.inv(XTX)
    return np.einsum("ij,jk,ki->i", x.T, information_inverse, x)


def _safe_column_correlation(X):
    """Return column correlations without warnings for constant columns.

    Correlations involving a constant column are mathematically undefined and
    are represented by ``np.nan``.  Nonconstant columns use the usual Pearson
    product-moment correlation.
    """

    X = np.asarray(X, dtype=float)
    if X.ndim != 2:
        raise ValueError("X must be a two-dimensional array.")
    if X.shape[0] < 2:
        raise ValueError("At least two runs are required for correlations.")

    centered = X - np.mean(X, axis=0)
    norms = np.linalg.norm(centered, axis=0)
    column_scale = np.maximum(1.0, np.max(np.abs(X), axis=0))
    tolerance = (
        np.finfo(X.dtype).eps * np.sqrt(X.shape[0]) * column_scale
    )
    variable = norms > tolerance
    valid_pairs = np.outer(variable, variable)

    correlations = np.full((X.shape[1], X.shape[1]), np.nan)
    denominator = np.outer(norms, norms)
    np.divide(
        centered.T @ centered,
        denominator,
        out=correlations,
        where=valid_pairs,
    )
    correlations[valid_pairs] = np.clip(
        correlations[valid_pairs], -1.0, 1.0
    )
    return correlations


def get_map_of_correlations(
    A,
    effects=(
        "intercept",
        "main",
        "2-interactions",
        "3-interactions",
        "quadratic",
    ),
    absolute=True,
    plot=True,
    annot=True,
    figsize=(11, 9),
):
    """Get the map of correlations.
    Compare with: https://rdrr.io/cran/daewr/man/colormap.html

    Inputs:

        A (numpy.array)
            DOE array.

        effects (list)
            List of effects, choose among:
                - "intercept"
                - "main"
                - "2-interactions"
                - "3-interactions"
                - "quadratic"

        absolute (bool)
            Return absolute values (JMP defaults).

        plot (bool)
            If True plot the graphical map of correlations as heatmap.

        annot (bool)
            Write the numerical value in the heatmap's cell.

        figsize (tuple of length 2)
            Figure size.


    Outputs:

            map_of_correlations (numpy.array)
    """

    X, names = get_X(A, effects, return_names=True)
    if "intercept" in effects:
        # The intercept is constant, so its correlation is undefined.
        X = X[:, 1:]
        names = names[1:]

    moc = _safe_column_correlation(X)

    if absolute:
        moc = abs(moc)
        vmin = 0
    else:
        vmin = -1  # Colors won't looking good anyway

    if plot:
        # Show the lower-left triangle, including its diagonal.
        mask = np.invert(np.tril(np.ones_like(moc, dtype=bool)))
        f, ax = plt.subplots(figsize=figsize)
        sns.heatmap(
            data=moc,
            cmap="RdYlGn_r",
            annot=annot,
            mask=mask,
            vmin=vmin,
            vmax=1,
            xticklabels=names,
            yticklabels=names,
            square=True,
            linewidths=0.5,
        )
        plt.show()

    return moc
