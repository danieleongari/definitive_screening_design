"""All the functions you need are in this init module."""
import numpy as np
import pandas as pd

from .generalized_dsd import compute_dsd

def generate(n_num, n_cat, factors_dict=None, method='dsd', min_13=True, n_fake_factors=0, verbose=True) -> pd.DataFrame:
    """Generate DSD with 2-levels categoricals design from calculation (Jones 2013).
    
    INPUTS

        n_num (int)
            Number of continuous factors.

        n_cat (int)
            Number of 2-levels categorical factors.

        factors_dict (dict)
            Factors info to populate the DSD table, e.g., { 'Temperature': (30, 90), 'Solvent': ("A", "B"), ...}.
            Note that the algorithm will infer if it is a numerical or categorical factor from the data type:
            use string number, e.g., ("1", "2"), if you want to treat the levels as categoricals.
            IF PRESENT, THIS WILL OVERWRITE n_num AND n_cat.

        method (str)
            Design choice: 'dsd' for de-alias all two-factor interactions with
            categorical factors or 'orth' to make orthogonal main-effects plan.

        min_13 (bool)
            If True, augment the experiments having only 2, 3, 4 and 5 numerical factors
            to at least 13 trials.

        n_fake_factors (int)
            Include numerical fake factors to increase the number of trials and have a larger design.
            Suggested use: 
                n_fake_factors=2 -> adds 4 trials, 
                n_fake_factors=4 -> adds 8 trials, 
                n_fake_factors=6 -> adds 12 trials, 
                ...

        verbose (bool)
            If True print info.

    OUTPUTS

        dsd_df (pandas.DataFrame)
            Table with DSD trials. Order is not randomized.

    """

    num_nms, cat_nms = [], []
    if factors_dict is None:
        factors_dict = {}
        for i in range(1, n_num+1):
            factor_nm = f"X{i:02d}"
            factors_dict[factor_nm] = (-1, 1)
            num_nms.append(factor_nm)
        for i in range(1, n_cat+1):
            factor_nm = f"C{i:02d}"
            factors_dict[factor_nm] = ("A", "B")   
            cat_nms.append(factor_nm)     
        if verbose:
            print(f"Generating a Definitive Screening Design with {n_num} numerical and {n_cat} categorical factors.")   
    else:
        for factor_nm, factor_range in factors_dict.items():
            if len(factor_range)!=2:
                raise ValueError(f"Factor `{factor_nm}` has not two range values: {factor_range}")
            if isinstance(factor_range[0], bool) or isinstance(factor_range[0], str):
                cat_nms.append(factor_nm)
            else:
                num_nms.append(factor_nm)
        n_num = len(num_nms)
        n_cat = len(cat_nms)
        if verbose:
            print(f"Generating a Definitive Screening Design from factors dictionary: {n_num} numerical and {n_cat} categorical.")       


    if min_13 and (n_num+n_cat+n_fake_factors)<6:
        n_fake_factors = 6-(n_num+n_cat)

    dsd_array = compute_dsd(
        n_num+n_fake_factors, 
        n_cat, 
        method
    )

    dsd_df = pd.DataFrame()
    for i, factor_nm in enumerate(num_nms):
        dsd_df[factor_nm] = dsd_array[:, i]
        dsd_df[factor_nm] = dsd_df[factor_nm].replace({
            -1.0: factors_dict[factor_nm][0], 
             0.0: np.mean(factors_dict[factor_nm]),
            +1.0: factors_dict[factor_nm][1], 
        })
    # NOTE: fake factors are skipped
    for i, factor_nm in enumerate(cat_nms):
        dsd_df[factor_nm] = dsd_array[:, -len(cat_nms)+i]
        dsd_df[factor_nm] = dsd_df[factor_nm].replace({
            1: factors_dict[factor_nm][0], 
            2: factors_dict[factor_nm][1], 
        })  

    # Restore original order of columns
    dsd_df = dsd_df[list(factors_dict.keys())]

    # Set indexes to 1-to-N range (instead of 0-to-(N-1))
    dsd_df.index = range(1, len(dsd_df)+1)

    return dsd_df