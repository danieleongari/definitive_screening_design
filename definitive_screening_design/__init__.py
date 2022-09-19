"""All the functions you need are in this init module."""

from tkinter import N
import pandas as pd
import numpy as np
from pathlib import Path

from .generalized_dsd import compute_dsd

THIS_DIR = Path(__file__).resolve().parents[0]
TABS_DIR = THIS_DIR / ".." / "tabs"

def create(factors) -> pd.DataFrame:
    """Retrieve the DSD design (Jones 2011).
    Factors is a list of factors names or an integer (number of factors).

    TODO: provide the -1, 0, +1 values.
    """

    if isinstance(factors, int):
        nfactors = factors
        factors = [ f"X{i:02d}" for i in range(1, factors+1) ] # e.g., X01, X02, X03, ...
    elif isinstance(factors, list):
        nfactors = len(factors)
    else:
        raise Exception("Input factors is nor an integer nor a list.")

    if nfactors < 4 or nfactors > 30:
        raise Exception(f"Asking for {nfactors} factors, but DOE only available from 4 to 30 factors.")

    fname = f"JN{nfactors}F{1+2*nfactors}R.xlsb"

    df = pd.read_excel(TABS_DIR / fname, engine='pyxlsb')
    df.columns = factors

    # Move the last row (conventionally having the center) on top
    # You may like having the center as "zeroth" row, at the start!
    # df = df.apply(np.roll, shift=1)

    return df

def generate(n_cont_factors, n_cat_factors, method='dsd', min_trials=True) -> pd.DataFrame:
    """Generate DSD with 2-levels categoricals design from calculation (Jones 2013).
    
    INPUTS

        n_cont_factors (int)
            Number of continuous factors.

        n_cat_factors (int)
            Number of 2-levels categorical factors.

        method (str)
            Design choice: 'dsd' for de-alias all two-factor interactions with
            categorical factors or 'orth' to make orthogonal main-effects plan.

        min_trials (bool)
            If True, augment the experiments with 2, 3, 4 and 5 numerical factors
            to at least 13 trials.

    OUTPUTS

        dsd_df (pandas.DataFrame)
            Table with DSD trials. Order is not randomized.

    """
    assert n_cont_factors>1, "DSD must have at least 2 numerical factors"

    fake_factors = 0 # Fake continuous factor used to augment the number of trials
    if min_trials and n_cont_factors<6:
        fake_factors = 6-n_cont_factors

    dsd_array = compute_dsd(n_cont_factors+fake_factors, n_cat_factors, method)

    # Delete columns of fake factor
    for i in range(fake_factors):
        dsd_array = np.delete(dsd_array, n_cont_factors, 1)

    column_labels = [ f"X{i:02d}" for i in range(1, n_cont_factors+1) ] + [ f"C{i:02d}" for i in range(1, n_cat_factors+1) ]
    index_labels = [ x+1 for x in range(dsd_array.shape[0])]

    dsd_df = pd.DataFrame(dsd_array, columns=column_labels, index=index_labels)

    return dsd_df




    



