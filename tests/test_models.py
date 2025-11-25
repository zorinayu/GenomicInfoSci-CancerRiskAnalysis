"""
Tests for mutation accumulation models.
"""

import pytest
import numpy as np
from src.models import MutationAccumulationModel


def test_mutation_accumulation_model():
    """Test mutation accumulation model initialization and prediction."""
    model = MutationAccumulationModel(p=1e-9, M=1000, divisions_per_year=2.0)
    
    # Test parameters
    params = model.get_parameters()
    assert params["p"] == 1e-9
    assert params["M"] == 1000
    assert params["divisions_per_year"] == 2.0
    
    # Test prediction
    ages = np.array([20, 40, 60, 80])
    predictions = model.predict(ages)
    
    # Predictions should be non-negative and increasing with age
    assert np.all(predictions >= 0)
    assert np.all(predictions <= 1)
    assert predictions[-1] > predictions[0]  # Risk should increase with age
    
    # Test scaled prediction
    scaled = model.predict_scaled(ages, scale_to_max=100)
    assert np.max(scaled) == 100
    assert np.all(scaled >= 0)

