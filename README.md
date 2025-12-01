# GenomicInfoSci-CancerRiskAnalysis

Comparative modeling of somatic mutation accumulation for age-dependent cancer risk.

## Project Overview

This project implements and compares multiple models for age-dependent cancer risk using **three complementary data layers**:

- **Population-level incidence (USCS)**: Age-specific cancer incidence curves (all sites and site-specific, e.g. colon and rectum).
- **Individual-level survival (lifelines)**: Survival datasets (shelf-life experiment and colon cancer survival) used to study lethality and hazard.
- **Tumor-level genomics (TCGA DR44)**: Project-level metadata from TCGA DR44 used to summarize mutation data coverage across tumor types.

On top of these data layers, the project develops three interconnected models:

- **Model A – Probabilistic Mutation-Accumulation Model**: A mechanistic model linking per-division driver mutation probability, stem-cell clone counts, clonal threshold, and repair efficiency to age–incidence curves. Includes analytic P(a) and grid-search calibration of key parameters using USCS all-sites and colon incidence.
- **Model B – Replicative-Risk / LSCD-Style Model**: A log-linear, cross-tissue model relating incidence to an LSCD-style covariate, combined with USCS age–incidence and TCGA DR44 coverage to explore how frequently each tissue develops cancer and how richly it is represented in genomics data.
- **Model C – Deterministic Hazard / Empirical Regression Models**: Hazard-based models (power-law, exponential, Weibull) fitted to USCS age–incidence, together with lifelines survival examples and colon incidence–survival cross-tables to study how age-dependent hazard and post-diagnosis lethality interact.

## Environment and Setup

Install dependencies (recommend using a fresh virtual environment):

```bash
pip install -r requirements.txt
```

## Running the Notebooks

The main analyses are in the Jupyter notebooks under the `notebooks/` directory:

- `model_a_probabilistic.ipynb`: Probabilistic mutation-accumulation model.
- `model_b_replicative_risk.ipynb`: LSCD-based replicative-risk baseline.
- `model_c_deterministic_hazard.ipynb`: Deterministic hazard / Cox-style models.
- `visualization_examples.ipynb`: Visualization and exploratory plots for the models and datasets.

You can start Jupyter and open these notebooks with:

```bash
jupyter notebook notebooks/model_b_replicative_risk.ipynb
```

or open any of the other notebooks listed above.

## Key References and External Resources

### Model B: Replicative-Risk Baseline (LSCD-based Model)

- **Tomasetti, C., & Vogelstein, B. (2015)**. Variation in cancer risk among tissues can be explained by the number of stem cell divisions. *Science*, 347(6217), 78–81.  
  - DOI: [10.1126/science.1260825](https://doi.org/10.1126/science.1260825)  
  - URL: [Science article page](https://www.science.org/doi/10.1126/science.1260825)

### Model C: Deterministic Hazard Model / Cox Regression

- **Cox, D. R. (1972)**. Regression Models and Life-Tables. *Journal of the Royal Statistical Society, Series B*, 34(2), 187–220.  
  - DOI: [10.1111/j.2517-6161.1972.tb00899.x](https://doi.org/10.1111/j.2517-6161.1972.tb00899.x)

- **lifelines Library**: Davidson-Pilon, C. (2019). lifelines: survival analysis in Python. *Journal of Open Source Software*, 4(40), 1317.
  - GitHub: [CamDavidsonPilon/lifelines](https://github.com/CamDavidsonPilon/lifelines)  
  - Documentation: [lifelines.readthedocs.io](https://lifelines.readthedocs.io/)

### Conceptual Figures from `lifelines-master/docs/images/`

This project uses the official `lifelines` documentation figures (in `lifelines-master/docs/images/`) as **conceptual references** for survival analysis, model selection, and calibration. In particular:

- **`lcd_parametric.png`**  
  This figure compares non-parametric estimates with several **parametric models** (Weibull, log-normal, log-logistic) fitted to left-censored lifetime data, along with QQ-plots.  
  The key conclusion in the original example is that the **log-normal distribution fits the data well**, while the **Weibull model fits poorly**, illustrating how QQ-plots and visual checks can guide **parametric model selection**. This motivates trying log-normal–type models, rather than relying only on Weibull, when modeling cancer-related lifetimes or mutation-accumulation processes.

- **`intro_survival_function.png`** and **`intro_hazards.png`**  
  These figures illustrate the definitions and typical shapes of the **survival function** \\(S(t) = P(T > t)\\), the **hazard function** \\(h(t)\\), and the **cumulative hazard** \\(H(t)\\).  
  The underlying relationships,
  \\[
  S(t) = \exp(-H(t)), \quad h(t) = -\frac{S'(t)}{S(t)},
  \\]
  are used in this project to interpret and compare the deterministic hazard model (Model C) with the probabilistic model (Model A).

- **`survival_weibull.png`**  
  Shows a fitted Weibull model and its cumulative hazard for survival data. This example highlights how **parametric hazard shapes** (e.g., increasing vs. decreasing hazard over age) can be read from the cumulative hazard curve, which we use as a qualitative reference when interpreting age–incidence patterns from our models.

- **`survival_calibration_probablilty.png`**  
  Demonstrates **survival probability calibration curves**, comparing predicted survival probabilities with observed event frequencies (following Austin et al., graphical calibration and Integrated Calibration Index ideas).  
  In this project, we adopt the same philosophy: **calibration plots** and related metrics are used to assess how well each model’s predicted cancer risk matches empirical age–incidence data.

### Lifelines-derived survival datasets in `data/lifelines/`

To ground the theoretical models in concrete, well-studied survival datasets, this project bundles selected CSV files from the `lifelines` project under `data/lifelines/`:

- **`shelflife.csv`** (from `lifelines-master/experiments/shelflife.csv`)  
  This dataset accompanies the *primary and secondary shelf life* experiment in `lifelines`. It distinguishes **primary shelf life** (time in store before purchase/opening) from **secondary shelf life** (time after opening until spoilage), and motivates a **two-regime hazard model**:
  \\[
  h_i(t) = 
  \begin{cases}
  h_1(t), & t \le \tau_i \\\\
  h_2(t - \tau_i), & t > \tau_i
  \end{cases}
  \\]
  or, when the same degradation continues after opening, an additive form
  \\[
  h_i(t) = 
  \begin{cases}
  h_1(t), & t \le \tau_i \\\\
  h_1(t) + h_2(t - \tau_i), & t > \tau_i \, ,
  \end{cases}
  \\]
  where \\(h_1\\) captures baseline degradation and \\(h_2\\) captures additional post-opening risk (for example, consumer-introduced contamination).  
  Conceptually, this mirrors **cancer risk as a combination of age-related baseline hazard and disease-specific lethality**: age plays the role of a long-term degradation process (analogous to primary shelf life), while tumor biology and treatment response contribute additional hazard once cancer has initiated (analogous to secondary shelf life).

- **`colon.csv`** (from `lifelines-master/examples/colon.csv`)  
  A classic colon cancer survival dataset with **time-to-event**, **event indicator (death/relapse)**, and **patient-level covariates** (including age). It provides a concrete example where **age** and **lethality (case-fatality / progression)** can be analyzed jointly using survival and hazard-based models. In this project, `colon.csv` serves as an external, tumor-level dataset that complements the population-level incidence curves (USCS) and allows qualitative checks that:
  - age-related patterns in colon cancer mortality are consistent with the age–incidence curves modeled in Models A–C, and  
  - hazard-based summaries (e.g., Weibull, log-normal fits, or Cox regression) exhibit shapes compatible with the multi-stage biological story encoded in the mutation-accumulation model.

These lifelines-derived datasets are not required to run the core USCS-based analyses, but they provide **rich, interpretable case studies** that help justify modeling cancer risk as a function of **age** (baseline hazard) and **lethality** (conditional event risk given cancer), in line with modern survival-analysis practice.

For additional references and links specific to this project, see `ref/REFERENCES.md`.
