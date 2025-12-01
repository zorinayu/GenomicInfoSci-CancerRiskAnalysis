# References

## Model B: Replicative-Risk Baseline (LSCD-based Model)

**Primary Reference:**
- Tomasetti, C., & Vogelstein, B. (2015). Variation in cancer risk among tissues can be explained by the number of stem cell divisions. *Science*, 347(6217), 78-81.
  - DOI: https://doi.org/10.1126/science.1260825
  - URL: https://www.science.org/doi/10.1126/science.1260825
  - Supplementary Materials: Available at the Science website

**Key Concepts:**
- LSCD (Lifetime Stem Cell Divisions): Tissue-specific lifetime number of stem cell divisions
- Log-linear relationship: log(incidence) = α + β · log(LSCD) + tissue effects
- Replicative risk hypothesis: Cancer risk correlates with number of cell divisions

## Model C: Deterministic Hazard Model / Cox Regression

**Primary References:**
- Cox, D. R. (1972). Regression Models and Life-Tables. *Journal of the Royal Statistical Society, Series B*, 34(2), 187-220.
  - DOI: https://doi.org/10.1111/j.2517-6161.1972.tb00899.x

**Implementation Library:**
- Davidson-Pilon, C. (2019). lifelines: survival analysis in Python. *Journal of Open Source Software*, 4(40), 1317.
  - GitHub: https://github.com/CamDavidsonPilon/lifelines
  - Documentation: https://lifelines.readthedocs.io/
  - PyPI: https://pypi.org/project/lifelines/

**Key Concepts:**
- Hazard function: h(t) = λ · t^k (power-law) or h(t) = λ · e^(βt) (exponential)
- Cumulative hazard: H(t) = ∫₀ᵗ h(s) ds
- Survival function: S(t) = exp(-H(t))
- Incidence: I(t) = 1 - S(t)

## Data Sources

**USCS (U.S. Cancer Statistics) Data:**
- U.S. Cancer Statistics Data Visualizations Tool: https://www.cdc.gov/cancer/dataviz
- Data Dictionary: Available in `data/USCS-1999-2022-ASCII/Data Dictionary USCS ASCII Nov_2024 submission.xlsx`


