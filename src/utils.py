"""
Utility functions for data processing and age group handling.
"""

import math
import pandas as pd
import numpy as np


def age_group_to_start(age_str):
    """
    Convert age group string (e.g., "1-4", "70-74", "85+") to starting age.
    
    Parameters
    ----------
    age_str : str
        Age group string.
    
    Returns
    -------
    float
        Starting age, or NaN if cannot be parsed.
    """
    if pd.isna(age_str):
        return math.nan
    if isinstance(age_str, str):
        age_str = age_str.strip()
        if age_str == "All Ages":
            return -1
        if age_str.endswith("+"):
            try:
                return float(age_str.rstrip("+"))
            except ValueError:
                return math.nan
        if "-" in age_str:
            try:
                return float(age_str.split("-")[0])
            except ValueError:
                return math.nan
    return math.nan


def age_group_to_mid(age_str):
    """
    Convert age group string to midpoint age.
    
    Parameters
    ----------
    age_str : str
        Age group string (e.g., "1-4", "70-74", "85+").
    
    Returns
    -------
    float
        Midpoint age, or NaN if cannot be parsed.
    """
    if pd.isna(age_str):
        return np.nan
    age_str = str(age_str).strip()
    if age_str == "All Ages":
        return np.nan
    if age_str.endswith("+"):
        try:
            start = float(age_str.rstrip("+"))
            return start + 2.5  # assume 5-year width for open-ended group
        except ValueError:
            return np.nan
    if "-" in age_str:
        try:
            lo, hi = age_str.split("-")
            return (float(lo) + float(hi)) / 2.0
        except ValueError:
            return np.nan
    return np.nan

