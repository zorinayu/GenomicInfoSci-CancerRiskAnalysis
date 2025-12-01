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
    
    where p_cell is the probability that a single clone has >=C driver hits:
        p_cell(a) = sum_{k=C}^{N} C(N,k) * p^k * (1-p)^(N-k)
    
    For C=1 (single hit), this simplifies to:
        p_cell(a) = 1 - (1 - p)^N
    
    and N is the effective number of divisions per clone at age a:
        N = a * divisions_per_year
    
    For C>1 (multiple hits required), the model produces nonlinear growth.
    """
    
    def __init__(self, p=2e-9, M=500000, divisions_per_year=2.5, C=1, r=0.0):
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
        C : int, default=1
            Number of driver mutations required for malignancy (clonal threshold).
            C=1 means single hit model (linear-like growth).
            C>1 means multiple hits required (nonlinear growth).
        r : float, default=0.0
            DNA repair efficiency (0.0 = no repair, 1.0 = perfect repair).
            Effective mutation probability becomes p_eff = p * (1 - r).
        """
        self.p = p
        self.M = M
        self.divisions_per_year = divisions_per_year
        self.C = C
        self.r = r
    
    def _binomial_probability(self, n, k, p):
        """
        Calculate binomial probability P(X >= k) for n trials with success probability p.
        Uses Poisson approximation for large n and small p.
        """
        if k == 1:
            # Single hit case: use exact formula
            return 1 - (1 - p) ** n
        elif k > n:
            return 0.0
        else:
            # Multiple hits: use Poisson approximation for computational efficiency
            # When p is small and n is large, Binomial(n,p) ≈ Poisson(np)
            lambda_poisson = n * p
            if lambda_poisson < 1e-10:
                return 0.0
            
            # Calculate P(X >= k) using Poisson distribution
            # Try scipy first, fall back to manual calculation
            try:
                from scipy.stats import poisson
                return 1 - poisson.cdf(k - 1, lambda_poisson)
            except ImportError:
                # Manual Poisson CDF calculation using recurrence relation
                # P(X >= k) = 1 - sum_{i=0}^{k-1} exp(-lambda) * lambda^i / i!
                prob_sum = 0.0
                exp_neg_lambda = np.exp(-lambda_poisson)
                factorial = 1.0
                lambda_power = 1.0
                
                for i in range(k):
                    if i > 0:
                        factorial *= i
                        lambda_power *= lambda_poisson
                    prob_sum += exp_neg_lambda * lambda_power / factorial
                
                return 1 - prob_sum
    
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
        # Apply repair efficiency
        p_eff = self.p * (1 - self.r)
        
        # Calculate number of divisions
        N = ages * self.divisions_per_year
        
        # Calculate probability that a single clone has >=C driver hits
        if self.C == 1:
            # Single hit: use exact formula
            p_cell = 1 - (1 - p_eff) ** N
        else:
            # Multiple hits: use binomial/Poisson approximation
            p_cell = np.array([self._binomial_probability(int(n), self.C, p_eff) 
                              for n in N])
        
        # Calculate tissue-level probability
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
            max_val = P_tissue.max()
            if max_val > 0:
                P_scaled = P_tissue / max_val * scale_to_max
            else:
                # If all predictions are zero (shouldn't happen in practice), return zeros
                P_scaled = np.zeros_like(P_tissue)
            return P_scaled
        return P_tissue
    
    def get_parameters(self):
        """Return model parameters as a dictionary."""
        return {
            "p": self.p,
            "M": self.M,
            "divisions_per_year": self.divisions_per_year,
            "C": self.C,
            "r": self.r
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

