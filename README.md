# Definitive Screening design

## References

- Jones, Bradley, and Christopher J. Nachtsheim. “A Class of Three-Level Designs for Definitive Screening in the Presence of Second-Order Effects.” Journal of Quality Technology 43, no. 1 (January 2011): 1–15. https://doi.org/10.1080/00224065.2011.11917841.

- Jones, Bradley, and Christopher J. Nachtsheim. "Definitive screening designs with added two-level categorical factors." Journal of Quality Technology 45.2 (2013): 121-129. https://doi.org/10.1080/00224065.2013.11917921

## Installation
```
pip install definitive_screening_design
```

## Examples
### Continuous-variables only (retrieving tables from the 2011 paper)
```
import definitive_screening_design
definitive_screening_design.create(4)
```
|    |   X01 |   X02 |   X03 |   X04 |
|---:|------:|------:|------:|------:|
|  0 |     0 |     0 |     0 |     0 |
|  1 |     0 |     1 |    -1 |    -1 |
|  2 |     0 |    -1 |     1 |     1 |
|  3 |    -1 |     0 |    -1 |     1 |
|  4 |     1 |     0 |     1 |    -1 |
|  5 |    -1 |    -1 |     0 |    -1 |
|  6 |     1 |     1 |     0 |     1 |
|  7 |    -1 |     1 |     1 |     0 |
|  8 |     1 |    -1 |    -1 |     0 |

or, specifying the variables' names 

```
definitive_screening_design.create(['Factor1', 'Factor-2', 'Factor-3', 'Factor-4'])
```
|    |   Factor1 |   Factor-2 |   Factor-3 |   Factor-4 |
|---:|----------:|-----------:|-----------:|-----------:|
|  0 |         0 |          0 |          0 |          0 |
|  1 |         0 |          1 |         -1 |         -1 |
|  2 |         0 |         -1 |          1 |          1 |
|  3 |        -1 |          0 |         -1 |          1 |
|  4 |         1 |          0 |          1 |         -1 |
|  5 |        -1 |         -1 |          0 |         -1 |
|  6 |         1 |          1 |          0 |          1 |
|  7 |        -1 |          1 |          1 |          0 |
|  8 |         1 |         -1 |         -1 |          0 |

### Both continuous and 2-levels categoricals variables (2013 paper)
```
import definitive_screening_design
definitive_screening_design.generate(n_cont_factors=3, n_cat_factors=2)
```
|    |   X01 |   X02 |   X03 |   C01 |   C02 |
|---:|------:|------:|------:|------:|------:|
|  0 |     0 |     1 |     1 |     2 |     2 |
|  1 |    -0 |    -1 |    -1 |     1 |     1 |
|  2 |     1 |     0 |    -1 |     2 |     2 |
|  3 |    -1 |    -0 |     1 |     1 |     1 |
|  4 |     1 |    -1 |     0 |     1 |     2 |
|  5 |    -1 |     1 |    -0 |     2 |     1 |
|  6 |     1 |     1 |    -1 |     2 |     1 |
|  7 |    -1 |    -1 |     1 |     1 |     2 |
|  8 |     1 |     1 |     1 |     1 |     2 |
|  9 |    -1 |    -1 |    -1 |     2 |     1 |
| 10 |     1 |    -1 |     1 |     2 |     1 |
| 11 |    -1 |     1 |    -1 |     1 |     2 |
| 12 |     0 |     0 |     0 |     1 |     1 |
| 13 |     0 |     0 |     0 |     2 |     2 |
