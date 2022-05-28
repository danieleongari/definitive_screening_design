# Definitive Screening design

## References

- Jones, Bradley, and Christopher J. Nachtsheim. “A Class of Three-Level Designs for Definitive Screening in the Presence of Second-Order Effects.” Journal of Quality Technology 43, no. 1 (January 2011): 1–15. https://doi.org/10.1080/00224065.2011.11917841.

## Installation
```
git clone ...
cd definitive_screening_design
pip install -e .
```

## Example

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

or 

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