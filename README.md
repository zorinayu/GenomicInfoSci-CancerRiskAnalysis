# GenomicInfoSci-CancerRiskAnalysis

Comparative modeling of somatic mutation accumulation and survival for **age‑dependent cancer risk**.

This is a **course-based project** for **ECBME4060_001_2025_3 - INTRO-GENOMIC INFO SCI & TECH Assignments**.

## Project Overview

This project implements the proposal of building a **unified, age-dependent cancer risk framework** on three data layers and three models:

- **Population-level incidence (USCS)** – age-specific cancer incidence curves for:
  - **All cancer sites combined**, and
  - Multiple **site-specific cancers** (colon and rectum, lung and bronchus, female breast, prostate, etc.).
- **Individual-level survival (lifelines)** – curated survival datasets (primary/secondary shelf life and colon cancer survival) that make **lethality and hazard shapes** explicit.
- **Tumor-level genomics (TCGA DR44)** – project-level metadata summarizing how many mutation-related data files exist per TCGA project, used as a **cross-scale bridge** from incidence patterns to genomic coverage.

On top of these data layers, the project develops three interconnected models that follow a single storyline:

- **Model A – Probabilistic Mutation-Accumulation Model**  
  A mechanistic model of somatic driver accumulation,
  \[
  P(a) = 1 - (1 - p_\text{cell}(a))^M ,
  \]
  where \(p_\text{cell}(a)\) depends on **per-division driver mutation probability** \(p\), **stem-cell divisions per year**, **clonal threshold** \(C\), and **DNA repair efficiency** \(r\).  
  The notebook:
  - Fits analytic \(P(a)\) to **USCS all-sites and colon age–incidence curves**.
  - Uses **grid search** to calibrate \((p, \text{divisions\_per\_year})\).
  - Validates the analytic approximation with a **Monte Carlo simulator**.
  - Performs an **ablation study** over \(C\) and \(r\).
  - Evaluates a **single calibrated parameter set across multiple cancer sites**, showing where a shared mutation-accumulation mechanism works well or breaks down.

- **Model B – Replicative-Risk / LSCD-Style Model**  
  A cross-tissue, log–log regression inspired by Tomasetti & Vogelstein (2015),
  linking mid-life incidence to a **Lifetime Stem Cell Division (LSCD)-style covariate**.  
  Using an explicit `LSCD_example.csv` table, the notebook:
  - Builds **cross-tissue log–log regressions** of incidence vs LSCD.
  - Extracts **mid-life incidence (50–69 years)** from USCS for several major sites.
  - Summarizes **USCS incidence vs TCGA DR44 project coverage**, and
  - Studies how **LSCD residuals correlate with TCGA coverage**, highlighting tissues that are over‑ or under‑represented in current genomics data.

- **Model C – Deterministic Hazard / Empirical Regression Models**  
  A family of **parametric hazard models** (power-law, exponential, Weibull) and survival tools that connect incidence to **post‑diagnosis lethality**.  
  The notebook:
  - Fits **multi-site Weibull hazard models** to USCS age–incidence for all sites and key tissues.
  - Implements **manual Kaplan–Meier survival curves** on the lifelines colon dataset.
  - Recreates **primary vs secondary shelf life** as a two-regime hazard example.
  - Builds a **colon-specific cross-table** combining USCS incidence and lifelines colon survival by age band, making explicit how age-dependent *risk of getting cancer* and *risk of dying after diagnosis* interact.

Throughout the project, **colon and rectal cancer** serve as a **reference example** that appears in all three models (USCS incidence, lifelines survival, TCGA‑COAD coverage), while **multi-site analyses** (all sites, lung, breast, prostate, etc.) demonstrate that the framework is not limited to a single disease.

## Environment and Setup

Install dependencies (recommend using a fresh virtual environment):

```bash
pip install -r requirements.txt
```

## Running the Notebooks

The main analyses are in `notebooks/` and are designed to be read as a **single narrative** rather than four unrelated scripts:

- **`visualization_examples.ipynb` – Data and narrative warm‑up**  
  - Introduces **USCS age–incidence curves** for all sites and selected tissues.  
  - Provides first visual links to **TCGA DR44 coverage**.

- **`model_a_probabilistic.ipynb` – Model A: probabilistic mutation accumulation**  
  - Calibrates the mechanistic model \(P(a)\) to **USCS all-sites and colon incidence**.  
  - Runs **grid search**, **Monte Carlo validation**, **C/r ablation**, and **multi-site evaluation with shared parameters**.

- **`model_b_replicative_risk.ipynb` – Model B: LSCD / replicative risk**  
  - Builds **cross-tissue log–log regressions** using `LSCD_example.csv`.  
  - Connects **USCS mid-life incidence** with **TCGA DR44 project coverage** and LSCD residuals.

- **`model_c_deterministic_hazard.ipynb` – Model C: deterministic hazard and survival**  
  - Compares **power-law, exponential, and Weibull hazard families** on USCS age–incidence.  
  - Uses **lifelines `shelflife.csv`** to illustrate primary vs secondary hazard regimes.  
  - Uses **lifelines `colon.csv`** to build Kaplan–Meier curves and a **colon incidence–survival cross-table**.

You can start Jupyter and open the notebooks with:

```bash
jupyter notebook notebooks/visualization_examples.ipynb
```

and then work through Models A–C in order.

## Alignment with the Proposal

This project implements the core ideas of the original proposal, with some deliberate simplifications:

- **Implemented as proposed**
  - Age-dependent incidence modeling for **all cancer sites** and **multiple individual sites** (USCS BYAGE).
  - Mechanistic **probabilistic mutation-accumulation framework** (Model A) with parameters \(p\), \(M\), \(C\), and \(r\), fitted to real data.
  - **Cross-tissue LSCD-style regressions** and **replicative-risk interpretation** (Model B).
  - **Deterministic hazard families** and **survival analysis tools** (Model C), including manual Kaplan–Meier curves and multi-site Weibull fits.
  - **Three-scale linkage**:
    - Population: USCS incidence curves.
    - Individual: lifelines survival datasets.
    - Tumor genomics: TCGA DR44 project‑level coverage summaries.

- **Simplifications and limitations (for future extensions)**
  - Model A currently uses **fixed \(p\)** per fit, rather than a full **LogNormal hierarchical prior for \(p\)** across tissues.  
  - Monte Carlo simulations are calibrated for **demonstrating agreement with the analytic formula**, not for exhaustive \(10^6\)-cell simulations over all parameter settings.  
  - LSCD values are stored in an **approximate `LSCD_example.csv`**, not the full table from the original Science supplement.  
  - Model C relies on **deterministic hazard and manual Kaplan–Meier**, rather than a full Cox PH implementation with Brier score and time‑dependent AUC.  
  - TCGA DR44 is used at the level of **project/file counts**; per-tumor mutation burdens are outlined conceptually but not computed from VCFs in this version.

These design choices keep the code **fully runnable within a course project setting**, while still delivering the main scientific message of the proposal:  
**cancer risk is an age-accumulating process whose incidence curves, survival shapes, and genomic representation can be linked coherently across population, individual, and tumor scales.**

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
