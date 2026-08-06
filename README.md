# Definitive Screening Design (DSD)

> NOTE: [pyDOE](https://github.com/pydoe/pydoe), in its recent v1.4 release (Aug 2026),
> now implements this same design: I managed myself that implementation.
> You are encoureged to use pyDOE instead of this package, to benefit from its broader functionality and active maintenance. 
> Check out the [notebooks_pydoe](notebooks_pydoe/) folder for examples using pyDOE's DSD implementation.

This repository provides a lightweight Python implementation for constructing definitive
screening designs with numerical factors and optional two-level categorical factors. A DSD is
an economical experimental plan for identifying the few important effects among many candidate
factors while retaining information about curvature and selected second-order effects. The
package generates the coded run matrix; the accompanying notebooks show how to turn that matrix
into a randomized experimental run sheet, assess what a proposed model can estimate before
collecting responses, and analyze the responses afterward. DSDs are screening tools rather than
automatic model-selection procedures, so conclusions should be checked against subject-matter
knowledge and, when necessary, confirmed or refined with augmented experiments.

## Why the Definitive Screening Design?

### ELI5

Imagine having many knobs and not knowing which ones matter. A DSD tests carefully chosen combinations of low, middle, and high settings so you can find the important knobs - and notice when "more" is not simply better - with relatively few experiments. It is a first-pass map, not a universal recipe: it works best when most knobs are numeric, can be adjusted independently, and only a few effects are important.

### ELI Scientist/Engineer

A DSD is an economical early-stage experiment for screening several factors, especially continuous ones. The three levels expose curvature while the design keeps estimates of main effects clear of bias from two-factor interactions and quadratic effects; a classical DSD for `m` continuous factors needs only `2m + 1` runs. It can also accommodate a few two-level categorical factors. Use another design when the region is constrained, factors form a mixture, many factors are categorical, a split-plot structure is required, or higher-order effects are expected.

### ELI Statistician

DSDs combine foldover pairs with a center run to produce a second-order-friendly screening design. Linear main effects are mutually orthogonal and orthogonal to quadratic effects and two-factor interactions; all pure quadratics are estimable, and no two-factor interaction is completely confounded with another interaction or a quadratic, although such terms may be correlated. This alias structure supports joint screening for active first- and second-order terms under effect sparsity, but model selection degrades as the number of active terms approaches the run count; augmentation is advisable when many terms may be active or reliable second-order identification is the goal.

## Main References

- Bradley Jones and Christopher J. Nachtsheim. "A Class of Three-Level Designs for Definitive Screening in the Presence of Second-Order Effects" Journal of Quality Technology (2011) 43, 1–15. [10.1080/00224065.2011.11917841](https://doi.org/10.1080/00224065.2011.11917841)
- Lili Xiao, Dennis K. J. Lin, Fenghan Bai, "Constructing Definitive Screening Designs Using Conference Matrices" Journal of Quality Technology (2012) 44, 2-8. [10.1080/00224065.2012.11917877](https://doi.org/10.1080/00224065.2012.11917877)
- Bradley Jones and Christopher J. Nachtsheim. "Definitive screening designs with added two-level categorical factors" Journal of Quality Technology (2013) 45, 121-129. [10.1080/00224065.2013.11917921](https://doi.org/10.1080/00224065.2013.11917921)

## Further References about the practical use of this design
- Bradley Jones - ["Simulating Responses and Fitting Definitive Screening Designs"](https://community.jmp.com/t5/Discovery-Summit-2017/Simulating-Responses-and-Fitting-Definitive-Screening-Designs/ta-p/44056)
- Bradley Jones - ["Proper and Improper use of Definitive Screening Designs"](https://community.jmp.com/t5/JMP-Blog/Proper-and-improper-use-of-Definitive-Screening-Designs-DSDs/ba-p/30703?trMode=source)
- Douglas Montgomery - [Coursera lesson on "General Structure of a DSD with m Factors"](https://www.coursera.org/lecture/response-surfaces-mixtures-model-building/general-structure-of-a-definitive-screening-design-with-m-factors-N1Ebc)
- Paul Nelson - ["The Evolution of Definitive Screening Designs from Optimal (Custom) DoE"](https://www.prismtc.co.uk/resources/blogs-and-articles/article-the-evolution-of-definitive-screening-designs-from-optimal-custom-design-of-experiments)
- Errore, Jones, Nachtsheim (2016) - ["Using Definitive Screening Designs to Identify Active First- and Second-Order Factor Effects"](https://www.tandfonline.com/doi/full/10.1080/00224065.2017.11917993)
- Jones, Nachtesheim (2017) ["Effective Design-Based Model Selection for Definitive Screening Designs"](https://www.tandfonline.com/doi/full/10.1080/00401706.2016.1234979)
- Weese, Ramsey, Montgomery (2018) - ["Analysis of definitive screening designs: Screening vs prediction"](https://onlinelibrary.wiley.com/doi/10.1002/asmb.2297)
- Other applications of the DSD from [Google Scholar](https://scholar.google.com/scholar?hl=en&q=%22definitive+screening+design%22), [Semantic Scholar](https://www.semanticscholar.org/search?q=%22definitive%20screening%20design%22&sort=relevance), [Web Of Science](https://www.webofscience.com/wos/woscc/summary/c41701b1-fb7c-4c6f-8a6a-527c62a42a2e-ec09dc2d/relevance/1)

## Installation
```
pip install definitive_screening_design
```

## Example
Generate a Definitive Design screening with three numerical and two 2-levels categoricals factors,
using the protocol presented in the 2013 paper.
The result is a Pandas DataFrame.

```
import definitive_screening_design as dsd
dsd.generate(n_num=3, n_cat=2)
```
|    |   X01 |   X02 |   X03 |   C01 |   C02 |
|---:|------:|------:|------:|------:|------:|
|  1 |     0 |     1 |     1 |     2 |     2 |
|  2 |    -0 |    -1 |    -1 |     1 |     1 |
|  3 |     1 |     0 |    -1 |     2 |     2 |
|  4 |    -1 |    -0 |     1 |     1 |     1 |
|  5 |     1 |    -1 |     0 |     1 |     2 |
|  6 |    -1 |     1 |    -0 |     2 |     1 |
|  7 |     1 |     1 |    -1 |     2 |     1 |
|  8 |    -1 |    -1 |     1 |     1 |     2 |
|  9 |     1 |     1 |     1 |     1 |     2 |
| 10 |    -1 |    -1 |    -1 |     2 |     1 |
| 11 |     1 |    -1 |     1 |     2 |     1 |
| 12 |    -1 |     1 |    -1 |     1 |     2 |
| 13 |     0 |     0 |     0 |     1 |     1 |
| 14 |     0 |     0 |     0 |     2 |     2 |

See `notebooks/` for examples using this package and `notebooks_pydoe/` for paired
examples using pydoe's DSD implementation. Both sets explain how design rows translate into
experimental run sheets and distinguish design analysis from response-model selection.
