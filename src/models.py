"""
Probabilistic mutation-accumulation models for cancer risk analysis.
"""

import numpy as np
import pandas as pd
from .utils import age_group_to_mid


class MutationAccumulationModel:
    """
    Probabilistic mutation-accumulation model for age-dependent cancer risk.
    
    The model uses the expression:
        P = 1 - (1 - p_cell)^M
    
    where p_cell is the probability that a single clone has >=1 driver hit:
        p_cell(a) = 1 - (1 - p)^N
    
    and N is the effective number of divisions per clone at age a:
        N = a * divisions_per_year
    """
    
    def __init__(self, p=2e-9, M=500000, divisions_per_year=2.5):
        """
        Initialize the mutation-accumulation model.
        
        Parameters
        ----------
        p : float
            Per-division driver-mutation probability.
        M : int
            Number of relevant stem-cell clones.
        divisions_per_year : float
            Effective stem-cell divisions per year.
        """
        self.p = p
        self.M = M
        self.divisions_per_year = divisions_per_year
    
    def predict(self, ages):
        """
        Predict cancer risk for given ages.
        
        Parameters
        ----------
        ages : array-like
            Ages in years.
        
        Returns
        -------
        array
            Predicted probabilities of malignancy.
        """
        ages = np.asarray(ages)
        N = ages * self.divisions_per_year
        p_cell = 1 - (1 - self.p) ** N
        P_tissue = 1 - (1 - p_cell) ** self.M
        return P_tissue
    
    def predict_scaled(self, ages, scale_to_max=None):
        """
        Predict cancer risk scaled to match empirical incidence scale.
        
        Parameters
        ----------
        ages : array-like
            Ages in years.
        scale_to_max : float, optional
            Maximum value to scale to. If None, returns unscaled predictions.
        
        Returns
        -------
        array
            Scaled predicted probabilities.
        """
        P_tissue = self.predict(ages)
        if scale_to_max is not None:
            P_scaled = P_tissue / P_tissue.max() * scale_to_max
            return P_scaled
        return P_tissue
    
    def get_parameters(self):
        """Return model parameters as a dictionary."""
        return {
            "p": self.p,
            "M": self.M,
            "divisions_per_year": self.divisions_per_year
        }


def prepare_age_incidence_data(all_sites_age_inc, target_year=2020):
    """
    Prepare age-incidence data for a specific year.
    
    Parameters
    ----------
    all_sites_age_inc : DataFrame
        Age-specific incidence data.
    target_year : int
        Target year to extract.
    
    Returns
    -------
    tuple
        (ages, rates) arrays of age midpoints and incidence rates.
    """
    age_model_df = all_sites_age_inc.copy()
    age_model_df["AGE_MID"] = age_model_df["AGE"].apply(age_group_to_mid)
    age_model_df = age_model_df[age_model_df["AGE_MID"].notna()].copy()
    
    age_year_df = age_model_df[
        pd.to_numeric(age_model_df["YEAR"], errors="coerce") == target_year
    ].copy()
    age_year_df = age_year_df.sort_values("AGE_MID")
    
    ages = age_year_df["AGE_MID"].values
    rates = age_year_df["RATE"].values
    
    return ages, rates

