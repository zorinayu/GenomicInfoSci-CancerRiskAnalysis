"""
Tests for utility functions.
"""

import pytest
import numpy as np
from src.utils import age_group_to_start, age_group_to_mid


def test_age_group_to_start():
    """Test age group to start conversion."""
    assert age_group_to_start("1-4") == 1.0
    assert age_group_to_start("70-74") == 70.0
    assert age_group_to_start("85+") == 85.0
    assert np.isnan(age_group_to_start("All Ages"))
    assert np.isnan(age_group_to_start("invalid"))


def test_age_group_to_mid():
    """Test age group to midpoint conversion."""
    assert age_group_to_mid("1-4") == 2.5
    assert age_group_to_mid("70-74") == 72.0
    assert age_group_to_mid("85+") == 87.5
    assert np.isnan(age_group_to_mid("All Ages"))
    assert np.isnan(age_group_to_mid("invalid"))

