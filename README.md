# GenomicInfoSci-CancerRiskAnalysis

**Course**: Introduction to Genomic Information Science & Technology  
**Project**: Age-Dependent Mutation Accumulation Model for Cancer Risk Analysis

A computational analysis project examining how age and tissue-specific stem-cell dynamics shape cancer incidence patterns, building on the work of Tomasetti & Vogelstein (Science 2015).

## Project Overview

This project focuses on modeling how age and tissue-specific stem-cell dynamics shape cancer incidence patterns. The core idea is that each stem cell division carries a small probability of acquiring a driver mutation, that DNA repair can partially correct these lesions, and that a malignant clone emerges only after a critical number of driver hits has been reached.

### Research Questions

- How well can an age-only empirical model explain observed cancer incidence across the lifespan?
- To what extent can a mechanistic somatic-mutation model reproduce the empirical age–incidence curve from SEER/USCS data?
- How do changes in mutation rate, repair efficiency, and clonal threshold alter the age–risk relationship?

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

## Data

This project uses publicly available USCS (U.S. Cancer Statistics) ASCII incidence tables from 1999-2022. The data files should be placed in `data/USCS-1999-2022-ASCII/`.

### Data Source

The USCS data can be downloaded from the official CDC website:

**Download Link**: [CDC U.S. Cancer Statistics Data Tables](https://www.cdc.gov/united-states-cancer-statistics/dataviz/data-tables.html)

### Download Instructions

1. Visit the [CDC Data Tables page](https://www.cdc.gov/united-states-cancer-statistics/dataviz/data-tables.html)
2. Select the **1999-2022** data set (or your preferred time range)
3. Download the delimited ASCII files
4. Extract the files and place them in the `data/USCS-1999-2022-ASCII/` directory

### Key Data Files

The following files are used in this analysis:
- `BYAGE.TXT`: Age-specific incidence for all cancer sites combined
- `BRAINBYSITE.TXT`: Brain and nervous system tumor incidence

### Data Usage Disclaimer

By using these data, you agree to comply with the following requirements:
- These data are provided for statistical reporting and analysis purposes only
- CDC's Policy on Releasing and Sharing Data prohibits linking these data with other data sets for the purpose of identifying an individual
- All material in the reports are in the public domain and may be reproduced or copied without permission (citation requested)

For more information, please refer to the [CDC U.S. Cancer Statistics website](https://www.cdc.gov/united-states-cancer-statistics/index.html).

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

## Model Description

The baseline probabilistic model uses the expression:

$$P = 1 - (1 - p^N)^M$$

where:
- $p$ is the per-division driver-mutation probability
- $N$ is the effective number of divisions per stem-cell clone
- $M$ is the number of relevant stem-cell clones

The model is extended with:
- Stochastic mutation rate: $p \sim \text{LogNormal}(\mu, \sigma)$
- Repair efficiency parameter: $r \in [0,1]$ such that $p_{\text{eff}} = p (1 - r)$
- Clonal threshold: $C$ driver hits required for malignancy

## Results

The analysis examines:
1. Pediatric brain tumor incidence patterns (age 0-19)
2. Age-specific cancer incidence across the full lifespan
3. Comparison of empirical data with probabilistic mutation-accumulation models

## Contributing

This is a research project. For questions or suggestions, please open an issue.

## License

[Specify your license here]

## Citation

If you use this code in your research, please cite:

```
[Your citation information]
```

## References

- Tomasetti, C., & Vogelstein, B. (2015). Variation in cancer risk among tissues can be explained by the number of stem cell divisions. Science, 347(6217), 78-81.

