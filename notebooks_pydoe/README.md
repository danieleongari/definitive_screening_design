# Pydoe notebook examples

These notebooks reproduce the examples in `../notebooks/` without importing the
`definitive_screening_design` package. DSD construction uses `pydoe`; response analysis uses
NumPy, SciPy, pandas, Matplotlib, seaborn, and scikit-learn as appropriate.

## Reading the paired notebooks

- A row is an experimental run, not an effect estimate.
- Pydoe codes continuous factors as `-1, 0, +1` and categorical factors as `-1, +1`.
- Preserve standard order for traceability and create a separately randomized execution order.
- Fake factors are construction devices that add runs and are dropped from the returned matrix.
- Response-model notebooks are exploratory; selected terms require hierarchy checks and
  confirmation or augmentation.

The paired DSD calls were audited after normalizing coding and run order. The notebook cases
produce the same row multisets and information matrices. A wider audit of 1,856 combinations
found 1,852 exact row-multiset matches; the remaining four six-factor cases differ only by a
column sign convention and run order.

Notebook 5 discusses Jones and Nachtsheim (2017), *Effective Design-Based Model Selection for
Definitive Screening Designs*, Technometrics 59(3), 319-329,
https://doi.org/10.1080/00401706.2016.1234979.
