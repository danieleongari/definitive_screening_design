"""All the functions you need are in this init module."""

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

def generate(n_cont_factors, n_cat_factors, method='dsd'):
    """Generate DSD with 2-levels categoricals design from calculation (Jones 2013)."""
    return pd.DataFrame(
        compute_dsd(n_cont_factors,n_cat_factors,method),
        columns=[ f"X{i:02d}" for i in range(1, n_cont_factors+1) ] + [ f"C{i:02d}" for i in range(1, n_cat_factors+1) ]
    )




    



