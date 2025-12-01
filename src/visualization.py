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
    plt.figure(figsize=(10, 6))
    plt.scatter(ages_emp, rates_emp, alpha=0.6, s=50, color='steelblue', 
                label=f"Observed incidence {target_year}", zorder=2)
    plt.plot(ages_model, rates_model, color="darkorange", linewidth=2.5, 
             label=model_label, zorder=3)
    plt.xlabel("Age (years)", fontsize=12)
    plt.ylabel("Incidence rate (per 100,000)", fontsize=12)
    plt.title(f"Age–Incidence Curve: Observed vs {model_label} ({target_year})", fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_age_incidence_curve(ages, rates, target_year=2020, title_suffix=""):
    """
    Plot age-specific incidence curve.
    
    Parameters
    ----------
    ages : array-like
        Age values.
    rates : array-like
        Incidence rates.
    target_year : int
        Year for the plot title.
    title_suffix : str
        Additional text for the title.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(ages, rates, alpha=0.7, s=50, color='steelblue', label=f'Observed incidence ({target_year})')
    plt.plot(ages, rates, alpha=0.5, linewidth=1.5, color='steelblue')
    plt.xlabel('Age (years)', fontsize=12)
    plt.ylabel('Incidence rate (per 100,000)', fontsize=12)
    title = f'Age-Specific Cancer Incidence - All Sites Combined ({target_year})'
    if title_suffix:
        title += f" - {title_suffix}"
    plt.title(title, fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.show()


def plot_parameter_sensitivity(ages, rates_emp, model_class, param_name, param_values, 
                               other_params=None, scale_to_max=None):
    """
    Plot sensitivity analysis for a model parameter.
    
    Parameters
    ----------
    ages : array-like
        Age values.
    rates_emp : array-like
        Empirical incidence rates.
    model_class : class
        Model class to instantiate.
    param_name : str
        Name of parameter to vary ('p', 'M', or 'divisions_per_year').
    param_values : list
        List of parameter values to test.
    other_params : dict, optional
        Other model parameters to keep constant.
    scale_to_max : float, optional
        Maximum value to scale predictions to.
    """
    if other_params is None:
        other_params = {}
    
    if scale_to_max is None:
        scale_to_max = np.max(rates_emp)
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(param_values)))
    
    plt.figure(figsize=(10, 6))
    plt.scatter(ages, rates_emp, alpha=0.4, s=30, color='gray', 
                label='Observed data', zorder=1)
    
    for param_val, color in zip(param_values, colors):
        params = other_params.copy()
        params[param_name] = param_val
        model = model_class(**params)
        pred = model.predict_scaled(ages, scale_to_max=scale_to_max)
        label = f'{param_name} = {param_val:.2e}' if param_val < 1 else f'{param_name} = {param_val:,}'
        plt.plot(ages, pred, linewidth=2, label=label, color=color, zorder=2)
    
    plt.xlabel('Age (years)', fontsize=12)
    plt.ylabel('Incidence rate (per 100,000)', fontsize=12)
    plt.title(f'Sensitivity Analysis: Effect of {param_name.upper()}', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_multi_year_comparison(all_sites_age_inc, years=[2015, 2018, 2020, 2022]):
    """
    Plot age-incidence curves for multiple years.
    
    Parameters
    ----------
    all_sites_age_inc : DataFrame
        Age-specific incidence data.
    years : list
        List of years to plot.
    """
    from src.models import prepare_age_incidence_data
    
    plt.figure(figsize=(10, 6))
    colors = plt.cm.tab10(np.linspace(0, 1, len(years)))
    
    for year, color in zip(years, colors):
        try:
            ages, rates = prepare_age_incidence_data(all_sites_age_inc, target_year=year)
            plt.plot(ages, rates, linewidth=2, label=f'{year}', color=color, alpha=0.8)
        except Exception as e:
            print(f"Warning: Could not plot data for year {year}: {e}")
    
    plt.xlabel('Age (years)', fontsize=12)
    plt.ylabel('Incidence rate (per 100,000)', fontsize=12)
    plt.title('Age-Specific Cancer Incidence: Multi-Year Comparison', fontsize=14)
    plt.legend(fontsize=11, title='Year')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_residual_analysis(ages, rates_obs, rates_pred, model_label="Model"):
    """
    Plot comprehensive residual analysis with improved visualization.
    
    Parameters
    ----------
    ages : array-like
        Age values.
    rates_obs : array-like
        Observed incidence rates.
    rates_pred : array-like
        Predicted incidence rates.
    model_label : str
        Label for the model.
    """
    residuals = rates_obs - rates_pred
    
    # Create figure with two subplots
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    # Top panel: Model fit comparison
    axes[0].scatter(ages, rates_obs, alpha=0.6, s=50, color='steelblue', 
                    label='Observed data', zorder=2)
    axes[0].plot(ages, rates_pred, color='darkorange', linewidth=2.5, 
                 label=f'{model_label} prediction', zorder=3)
    axes[0].set_xlabel('Age (years)', fontsize=12)
    axes[0].set_ylabel('Incidence rate (per 100,000)', fontsize=12)
    axes[0].set_title(f'Model Fit: {model_label} vs Observed Data', fontsize=14)
    axes[0].legend(fontsize=11)
    axes[0].grid(True, alpha=0.3)
    
    # Bottom panel: Residual plot with enhanced visualization
    # Color code residuals: positive (underestimate) vs negative (overestimate)
    positive_mask = residuals >= 0
    negative_mask = residuals < 0
    
    axes[1].scatter(ages[positive_mask], residuals[positive_mask], 
                    alpha=0.7, s=60, color='purple', 
                    label='Model underestimates (predicted < observed)', zorder=2)
    axes[1].scatter(ages[negative_mask], residuals[negative_mask], 
                    alpha=0.7, s=60, color='red', 
                    label='Model overestimates (predicted > observed)', zorder=2)
    
    # Reference line at zero
    axes[1].axhline(y=0, color='black', linestyle='--', linewidth=2, 
                    label='Perfect fit (zero error)', zorder=1)
    
    # Add good fit zone (±10% of max rate as threshold)
    max_rate = np.max(rates_obs)
    threshold = 0.1 * max_rate
    axes[1].fill_between([ages.min(), ages.max()], -threshold, threshold, 
                         alpha=0.15, color='green', 
                         label=f'Good fit zone (±{threshold:.0f})', zorder=0)
    
    axes[1].set_xlabel('Age (years)', fontsize=12)
    axes[1].set_ylabel('Residuals (Observed - Predicted)', fontsize=12)
    axes[1].set_title('Residual Plot: Model Fit Quality Assessment', fontsize=14)
    axes[1].legend(fontsize=10, loc='upper right')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Calculate and return statistics
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    
    mse = mean_squared_error(rates_obs, rates_pred)
    r2 = r2_score(rates_obs, rates_pred)
    mae = mean_absolute_error(rates_obs, rates_pred)
    rmse = np.sqrt(mse)
    
    return {
        'mse': mse,
        'r2': r2,
        'mae': mae,
        'rmse': rmse,
        'residuals': residuals
    }

