"""Tools to analyse the DOE and the the response collected with the DOE."""

import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import seaborn as sns


def get_X(A, effects=["intercept", "main", "2-interactions", "quadratic"], return_names=False):
    """Given the matrix A of the experiment design and the effects included in the model,
    return the matrix X to multiply with the coefficients of the model.
    If `return_names` is True, return also the name of the terms of the polynomium used as model.
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


def get_efficiency(A, effects=["intercept", "main"]):
    """https://www.jmp.com/support/help/Evaluate_Design_Window.shtml#168318
    p = n_params
    n = n_trials

    NOTE: G-Efficiency and I-Efficiency require a grid or Monte Carlo evaluation
          of the variance (see get_variance) in the whole desing space (i.e., typically
          for -1 to 1 in the number-of-factors dimensionality)
    """
    X = get_X(A, effects=effects)
    XTX = np.dot(X.T, X)
    n_trials, n_params = X.shape
    try:
        D_eff = 100 * np.linalg.det(XTX) ** (1 / n_params) / n_trials
    except Exception:
        D_eff = 0
    try:
        A_eff = 100 * n_params / (n_trials * np.trace(np.linalg.inv(XTX)))
    except Exception:
        A_eff = 0

    return {
        "Number of Trials": n_trials,
        "Number of Parameters": n_params,
        "D-Efficiency (%)": D_eff,
        "A-Efficiency (%)": A_eff,
    }


def get_variance(x, A, effects=["intercept", "main"]):
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
    var = x.T.dot(np.linalg.inv(XTX)).dot(x)
    var = var[-1, :]
    return var


def get_map_of_correlations(
    A,
    effects=["intercept", "main", "2-interactions", "3-interactions", "quadratic"],
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
    if "intercept" in effects:  # remove intercept from X for computing correlations
        X = X[:, 1:]
        names = names[1:]

    moc = np.corrcoef(X, rowvar=False)

    if absolute:
        moc = abs(moc)
        vmin = 0
    else:
        vmin = -1  # Colors won't looking good anyway

    if plot:
        mask = np.invert(np.tril(np.ones_like(moc, dtype=bool)))  # Show only bottom-left corner, including the diagonal
        # cmap = sns.diverging_palette(h_neg=130, h_pos=359, s=100, l=60, sep=1, n=None, center="light", as_cmap=True)
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
