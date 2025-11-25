# GenomicInfoSci-CancerRiskAnalysis

**Course**: Introduction to Genomic Information Science & Technology (ECBM E4060)  
**Instructor**: Dr. Tai-Hsien Ou Yang  
**Student**: Yanxuan Yu (UNI: yy3523, yy3523@columbia.edu)  
**Project**: Comparative Modeling of Somatic Mutation Accumulation for Age-Dependent Cancer Risk

A computational analysis project examining how age and tissue-specific stem-cell dynamics shape cancer incidence patterns, building on the work of Tomasetti & Vogelstein (Science 2015).

## Goal and Scientific Background

Cancer risk increases with the accumulation of somatic mutations. Building on the September 29 lecture, the baseline model expresses the probability of malignancy as:

$$P = 1 - (1 - p^N)^M$$

To reflect biological heterogeneity, the project adopts a comparative design that includes: (i) a probabilistic framework with mutation-rate variation ($p \sim \text{LogNormal}$), DNA repair efficiency ($r$), and a clonal threshold ($C$); and (ii) at least one alternative baseline (deterministic rate/hazard or empirical regression). In line with Tomasetti & Vogelstein (Science 2015), tissue-specific lifetime stem cell divisions (LSCD) will be incorporated as a replicative-risk covariate to explain cross-tissue variation. Recent studies further motivate these extensions by documenting driver-mutation accumulation in normal tissues and tissue/individual variability in cancer risk (Lawson et al., 2025; Imaoka, 2025).

### Research Questions

- How well can an age-only empirical model explain observed cancer incidence across the lifespan?
- To what extent can a mechanistic somatic-mutation model reproduce the empirical age–incidence curve from SEER/USCS data?
- How do changes in mutation rate, repair efficiency, and clonal threshold alter the age–risk relationship?
- After accounting for LSCD, does the probabilistic framework with $p$, $r$, and $C$ provide superior calibration compared with LSCD-based and deterministic baselines?

## Project Structure

```
FinalProject/
├── src/                    # Source code modules
│   ├── __init__.py
│   ├── data_loader.py      # Data loading utilities
│   ├── utils.py            # Utility functions
│   ├── visualization.py    # Plotting functions
│   └── models.py           # Probabilistic models
├── notebooks/              # Jupyter notebooks
│   └── final_project_analysis.ipynb
├── data/                   # Data files
│   └── USCS-1999-2022-ASCII/
├── tests/                  # Unit tests
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/zorinayu/GenomicInfoSci-CancerRiskAnalysis.git
cd GenomicInfoSci-CancerRiskAnalysis
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the USCS data (see [Data](#data) section below) and place the files in `data/USCS-1999-2022-ASCII/`.

## Datasets & Validation

This project uses multiple publicly available datasets for model development and validation:

### Primary Data Sources

#### 1. USCS (U.S. Cancer Statistics) - Current Analysis

Publicly available USCS ASCII incidence tables from 1999-2022, used for population-level age-incidence curves.

**Download Link**: [CDC U.S. Cancer Statistics Data Tables](https://www.cdc.gov/united-states-cancer-statistics/dataviz/data-tables.html)

**Download Instructions**:
1. Visit the [CDC Data Tables page](https://www.cdc.gov/united-states-cancer-statistics/dataviz/data-tables.html)
2. Select the **1999-2022** data set (or your preferred time range)
3. Download the delimited ASCII files
4. Extract the files and place them in the `data/USCS-1999-2022-ASCII/` directory

**Key Files**:
- `BYAGE.TXT`: Age-specific incidence for all cancer sites combined
- `BRAINBYSITE.TXT`: Brain and nervous system tumor incidence

**Data Usage Disclaimer**: By using these data, you agree to comply with CDC requirements:
- These data are provided for statistical reporting and analysis purposes only
- CDC's Policy on Releasing and Sharing Data prohibits linking these data with other data sets for the purpose of identifying an individual
- All material in the reports are in the public domain and may be reproduced or copied without permission (citation requested)

#### 2. SEER (Surveillance, Epidemiology, and End Results) - Planned

SEER incidence data for population curves and cross-tissue validation.

**Source**: [SEER Research Data and SEER*Stat](https://seer.cancer.gov/data/)

**Planned Use**: Primary dataset for estimating empirical age–incidence curves for different tissues and external validation across SEER tissues.

#### 3. TCGA (The Cancer Genome Atlas) - Planned

TCGA data for tumor mutation burden and driver panels.

**Source**: [TCGA Program via GDC](https://www.cancer.gov/tcga)

**Planned Use**: Analysis of mutation burden and driver mutation patterns.

#### 4. 1000 Genomes Project - Planned

1000 Genomes data for germline background analysis.

**Source**: [1000 Genomes Project](https://www.internationalgenome.org/)

**Planned Use**: Germline variant analysis and background mutation rate estimation.

### Computational Considerations

SEER, TCGA, and 1000 Genomes datasets can be sizable. If local compute/storage limits are reached, the plan uses:
- Stratified downsampling (by age bin × tissue)
- Sparse year grids
- Staged per-tissue processing

Any adjustments will follow the methodology and be documented during implementation.

## Usage

### Running the Analysis Notebook

Open and run the Jupyter notebook:
```bash
jupyter notebook notebooks/final_project_analysis.ipynb
```

### Using the Modules

You can also import and use the modules directly:

```python
from src.data_loader import load_uscs_data, prepare_all_sites_age_data
from src.models import MutationAccumulationModel, prepare_age_incidence_data
from src.visualization import plot_age_incidence_model

# Load data
brain_by_site, by_age = load_uscs_data()
all_sites_age_inc = prepare_all_sites_age_data(by_age)

# Prepare age-incidence data
ages, rates = prepare_age_incidence_data(all_sites_age_inc, target_year=2020)

# Create and fit model
model = MutationAccumulationModel(p=2e-9, M=500000, divisions_per_year=2.5)
predicted = model.predict_scaled(ages, scale_to_max=rates.max())

# Visualize
plot_age_incidence_model(ages, rates, ages, predicted, target_year=2020)
```

## Comparative Framework for Age-Dependent Cancer Risk

This project implements a comparative modeling framework with multiple models and multiple validation sets. The workflow follows:

**Inputs** → **Parallel Models (A/B/C)** → **Model Comparison & Calibration** → **Outputs**

### Models

#### (A) Probabilistic Mutation-Accumulation Model

The baseline probabilistic model uses the expression:

$$P = 1 - (1 - p^N)^M$$

where:
- $p$ is the per-division driver-mutation probability
- $N$ is the effective number of divisions per stem-cell clone
- $M$ is the number of relevant stem-cell clones

The model is extended with:
- **Stochastic mutation rate**: $p \sim \text{LogNormal}(\mu, \sigma)$ to capture biological heterogeneity
- **Repair efficiency parameter**: $r \in [0,1]$ such that the effective mutation probability is $p_{\text{eff}} = p (1 - r)$
- **Clonal threshold**: $C$ driver hits required for malignancy

#### (B) Replicative-Risk Baseline (LSCD Model)

A replicative-risk baseline relating log-incidence to log-LSCD, following Tomasetti & Vogelstein (Science 2015). The slope is estimated via log-linear regression with tissue fixed effects to explain cross-tissue variation in cancer risk. This model incorporates tissue-specific lifetime stem cell divisions (LSCD) as a replicative-risk covariate.

#### (C) Deterministic Hazard Model / Empirical Regression

Deterministic hazard model and/or empirical Cox regression as alternative baselines that do not explicitly encode mutation biology. These models provide flexible empirical frameworks for comparison with the mechanistic models.

### Simulation and Evaluation

- **Simulation**: Monte Carlo simulation ($10^6$ cells, 0-80 years) to generate age-incidence curves and examine Poisson limits for small $p$
- **Evaluation Metrics**:
  - **Calibration**: Brier score at 10-year intervals
  - **Discrimination**: Time-dependent AUC
  - **Fit**: Negative log-likelihood (NLL) / Akaike Information Criterion (AIC)
- **Validation**: External validation across SEER tissues
- **Ablation Studies**: Remove $r$, fix $C$, or replace LogNormal $p$ with Gamma to quantify component contributions

### Expected Outcomes

**Hypothesis**: After accounting for LSCD, the probabilistic framework with $p$, $r$, and $C$ will provide superior calibration and interpretable residual structure compared with LSCD-based and deterministic baselines.

**Outputs**:
- Age–repair efficiency surface: Visualization of how cancer risk varies with age and repair efficiency
- Cross-tissue residual plots vs LSCD: Analysis of residual variation after accounting for lifetime stem cell divisions
- Sensitivity analyses: Examination of model behavior over different values of $r$ and $C$
- Model comparison metrics: Calibration (Brier score), discrimination (AUC), and fit (NLL/AIC) comparisons across models A, B, and C
- Data-driven hypotheses: Connections between mutation burden, repair performance, and incidence trends


## Contributing

This is a research project. For questions or suggestions, please open an issue.

## License

[Specify your license here]

## Citation

If you use this code in your research, please cite:

```bibtex
@misc{genomicinfosci_cancerrisk_2025,
  title={Comparative Modeling of Somatic Mutation Accumulation for Age-Dependent Cancer Risk},
  author={Yu, Yanxuan},
  year={2025},
  institution={Columbia University, Department of Biomedical Engineering},
  course={ECBM E4060 - Introduction to Genomic Information Science and Technology},
  url={https://github.com/zorinayu/GenomicInfoSci-CancerRiskAnalysis}
}
```

Please also cite the key references listed above, particularly Tomasetti & Vogelstein (2015) and the data sources used.

## References

### Key Publications

1. **Tomasetti, C., & Vogelstein, B.** (2015). Variation in cancer risk among tissues can be explained by the number of stem cell divisions. *Science*, 347(6217), 78-81. https://www.science.org/doi/10.1126/science.1260825

2. **Lawson, A.R.J., et al.** (2025). Somatic mutation and selection at population scale. *Nature*. https://www.nature.com/articles/s41586-025-09584-w

3. **Imaoka, T.** (2025). Trans-Scale Insights into Variability in Radiation Cancer Risk Across Tissues, Individuals, and Species. *Biology*, 14(8), 1025. https://doi.org/10.3390/biology14081025

### Data Portals

- **SEER Research Data and SEER*Stat**: https://seer.cancer.gov/data/
- **TCGA Program (GDC)**: https://www.cancer.gov/tcga
- **1000 Genomes Project**: https://www.internationalgenome.org/
- **CDC U.S. Cancer Statistics**: https://www.cdc.gov/united-states-cancer-statistics/index.html

