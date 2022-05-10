#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

if __name__ == '__main__':
    setup(packages=find_packages(),
          long_description=LONG_DESCRIPTION,
          long_description_content_type='text/markdown',
          name="definitive_screening_design",
          author="Daniele Ongari",
          author_email="Daniele.Ongari@Solvay.com",
          description="Definitive Screening Design",
          url="https://github.com/danieleongari/definitive_screening_design",
          license="None",
          classifiers=["Programming Language :: Python"],
          version="0.1.1",
          install_requires=[
          "numpy",
          "pandas",
          "pyxlsb",
          ],
          extras_require={
              "testing": ["pytest==6.2.5", "pytest-cov==2.12.1"],
              "pre-commit": [
                  "pre-commit==2.15.0",
                  "yapf==0.31.0",
                  "prospector==1.5.1",
              ]
          })
