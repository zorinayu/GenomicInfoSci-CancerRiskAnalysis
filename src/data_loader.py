"""
Data loading utilities for USCS cancer incidence data.
"""

from pathlib import Path
import pandas as pd


def load_uscs_data(data_dir=None):
    """
    Load USCS cancer incidence data from ASCII files.
    
    Parameters
    ----------
    data_dir : str or Path, optional
        Path to the USCS data directory. If None, uses default relative path.
    
    Returns
    -------
    tuple
        (brain_by_site, by_age) DataFrames containing BRAINBYSITE and BYAGE data.
    """
    if data_dir is None:
        # Default path relative to project root
        data_dir = Path(__file__).parent.parent / "data" / "USCS-1999-2022-ASCII"
    else:
        data_dir = Path(data_dir)
    
    brain_by_site_path = data_dir / "BRAINBYSITE.TXT"
    by_age_path = data_dir / "BYAGE.TXT"
    
    # Load pipe-delimited files, "~" denotes missing values
    brain_by_site = pd.read_csv(
        brain_by_site_path, 
        sep="|", 
        na_values="~",
        low_memory=False
    )
    by_age = pd.read_csv(
        by_age_path, 
        sep="|", 
        na_values="~",
        low_memory=False
    )
    
    return brain_by_site, by_age


def prepare_pediatric_brain_data(brain_by_site):
    """
    Prepare pediatric malignant brain tumor data (age 0-19).
    
    Parameters
    ----------
    brain_by_site : DataFrame
        Raw BRAINBYSITE data.
    
    Returns
    -------
    DataFrame
        Filtered and cleaned pediatric brain tumor data.
    """
    df = brain_by_site.copy()
    
    # Ensure numeric columns are correctly typed
    for col in ["AGE_ADJUSTED_RATE", "AGE_ADJUSTED_CI_LOWER", "AGE_ADJUSTED_CI_UPPER"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["COUNT", "POPULATION"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Focus on malignant brain tumors in children (0-19 years)
    pediatric_brain = df[
        (df["AGE"] == "0-19")
        & (df["BEHAVIOR"] == "Malignant")
    ].copy()
    
    # Drop rows where the age-adjusted rate is not reported
    pediatric_brain = pediatric_brain[pediatric_brain["AGE_ADJUSTED_RATE"].notna()].copy()
    
    # Add YEAR as numeric for year-wise plots
    pediatric_brain["YEAR_NUM"] = pd.to_numeric(pediatric_brain["YEAR"], errors="coerce")
    
    return pediatric_brain


def prepare_all_sites_age_data(by_age):
    """
    Prepare age-specific incidence data for all cancer sites combined.
    
    Parameters
    ----------
    by_age : DataFrame
        Raw BYAGE data.
    
    Returns
    -------
    DataFrame
        Filtered and cleaned age-specific incidence data.
    """
    from .utils import age_group_to_start
    
    df = by_age.copy()
    
    # Make sure numeric columns are correctly typed
    for col in ["CI_LOWER", "CI_UPPER", "COUNT", "POPULATION", "RATE"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Focus on incidence, all races, all cancer sites combined
    all_sites_age_inc = df[
        (df["EVENT_TYPE"] == "Incidence")
        & (df["RACE"] == "All Races")
        & (df["SITE"] == "All Cancer Sites Combined")
    ].copy()
    
    # Add age start for ordering
    all_sites_age_inc["AGE_START"] = all_sites_age_inc["AGE"].apply(age_group_to_start)
    
    # Remove "All Ages" and any age categories we cannot order
    all_sites_age_inc = all_sites_age_inc[
        all_sites_age_inc["AGE_START"].notna() 
        & (all_sites_age_inc["AGE"] != "All Ages")
    ]
    
    return all_sites_age_inc

