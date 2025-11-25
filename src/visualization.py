"""
Visualization utilities for cancer incidence analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


# Set default style
sns.set(style="whitegrid", context="notebook")
plt.rcParams["figure.figsize"] = (6, 4)


def plot_pediatric_brain_distribution(pediatric_brain):
    """
    Plot distribution of pediatric malignant brain tumor incidence rates.
    
    Parameters
    ----------
    pediatric_brain : DataFrame
        Pediatric brain tumor data.
    """
    sns.histplot(pediatric_brain["AGE_ADJUSTED_RATE"].dropna(), bins=30)
    plt.xlabel("Age-adjusted incidence rate (per 100,000)")
    plt.title("Distribution of pediatric malignant brain tumor incidence rates (all years)")
    plt.tight_layout()
    plt.show()


def plot_pediatric_brain_by_year(pediatric_brain):
    """
    Plot year-wise distribution of pediatric brain tumor incidence rates.
    
    Parameters
    ----------
    pediatric_brain : DataFrame
        Pediatric brain tumor data with YEAR_NUM column.
    """
    plt.figure(figsize=(10, 4))
    order_years = sorted(pediatric_brain["YEAR_NUM"].dropna().unique())
    sns.boxplot(
        data=pediatric_brain[pediatric_brain["YEAR_NUM"].notna()],
        x="YEAR_NUM",
        y="AGE_ADJUSTED_RATE",
        order=order_years,
    )
    plt.xticks(rotation=90)
    plt.xlabel("Year")
    plt.ylabel("Age-adjusted incidence rate (per 100,000)")
    plt.title("Year-wise distribution of pediatric malignant brain tumor incidence rates")
    plt.tight_layout()
    plt.show()


def plot_pediatric_brain_trend(pediatric_brain):
    """
    Plot trend of mean pediatric brain tumor incidence by year.
    
    Parameters
    ----------
    pediatric_brain : DataFrame
        Pediatric brain tumor data with YEAR_NUM column.
    """
    annual_brain_rates = (
        pediatric_brain[pediatric_brain["YEAR_NUM"].notna()]
        .groupby("YEAR_NUM")["AGE_ADJUSTED_RATE"]
        .mean()
        .reset_index()
        .sort_values("YEAR_NUM")
    )
    
    plt.figure(figsize=(6, 4))
    plt.plot(annual_brain_rates["YEAR_NUM"], annual_brain_rates["AGE_ADJUSTED_RATE"], "-o")
    plt.xlabel("Year")
    plt.ylabel("Mean age-adjusted incidence rate (per 100,000)")
    plt.title("Trend of mean pediatric malignant brain tumor incidence by year")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_age_incidence_model(ages_emp, rates_emp, ages_model, rates_model, 
                             target_year=2020, model_label="Model"):
    """
    Plot empirical age-incidence curve vs model predictions.
    
    Parameters
    ----------
    ages_emp : array-like
        Empirical age values.
    rates_emp : array-like
        Empirical incidence rates.
    ages_model : array-like
        Model age values.
    rates_model : array-like
        Model predicted rates.
    target_year : int
        Year for the plot title.
    model_label : str
        Label for the model curve.
    """
    plt.figure(figsize=(8, 5))
    plt.scatter(ages_emp, rates_emp, alpha=0.6, s=30, label=f"Observed incidence {target_year}")
    plt.plot(ages_model, rates_model, color="darkorange", linewidth=2, label=model_label)
    plt.xlabel("Age (years)")
    plt.ylabel("Incidence / scaled probability")
    plt.title(f"Age–incidence curve vs {model_label} in {target_year}")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

