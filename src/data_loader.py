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


def get_site_age_incidence(by_age, site_name, target_year=2020):
    """
    Prepare age-specific incidence data for a given cancer site.

    This function aggregates over sex (summing COUNT and POPULATION) to obtain
    an "all sexes" age–incidence curve, then filters to a single calendar year.

    Parameters
    ----------
    by_age : DataFrame
        Raw BYAGE data.
    site_name : str
        Site name as recorded in the USCS BYAGE table
        (e.g., "Colon and Rectum", "Lung and Bronchus").
    target_year : int, default=2020
        Calendar year to extract.

    Returns
    -------
    tuple
        (ages, rates, df_year) where:
        - ages: numpy array of age midpoints
        - rates: numpy array of incidence rates (per 100,000)
        - df_year: filtered DataFrame for the specified year and site
    """
    from .utils import age_group_to_mid

    df = by_age.copy()
    # Filter by event type, race, and site; keep all sexes, aggregate later
    df_site = df[
        (df["EVENT_TYPE"] == "Incidence")
        & (df["RACE"] == "All Races")
        & (df["SITE"] == site_name)
    ].copy()

    if df_site.empty:
        return None, None, df_site

    # Ensure numeric
    for col in ["COUNT", "POPULATION"]:
        if col in df_site.columns:
            df_site[col] = pd.to_numeric(df_site[col], errors="coerce")

    # Aggregate over sex: sum counts and population by AGE and YEAR
    agg = (
        df_site
        .groupby(["AGE", "YEAR"], as_index=False)
        .agg({"COUNT": "sum", "POPULATION": "sum"})
    )
    agg["RATE"] = agg["COUNT"] / agg["POPULATION"] * 100000.0
    agg["AGE_MID"] = agg["AGE"].apply(age_group_to_mid)
    agg = agg[agg["AGE_MID"].notna()].copy()

    df_year = agg[pd.to_numeric(agg["YEAR"], errors="coerce") == target_year].copy()
    df_year = df_year.sort_values("AGE_MID")

    ages = df_year["AGE_MID"].values
    rates = df_year["RATE"].values

    return ages, rates, df_year

