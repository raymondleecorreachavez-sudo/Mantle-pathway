"""
Unit tests for input validators in gmc_correction.validators module.
"""

import pytest
from gmc_correction.validators import (
    validate_arrival_time,
    validate_station_coords,
    validate_slab_tensor_profile,
)


class TestValidateArrivalTime:
    """Tests for arrival time validation."""
    
    def test_valid_arrival_time_float(self):
        """Valid positive float should pass."""
        result = validate_arrival_time(12.5)
        assert result == 12.5
        assert isinstance(result, float)
    
    def test_valid_arrival_time_int(self):
        """Valid positive integer should be converted to float."""
        result = validate_arrival_time(10)
        assert result == 10.0
        assert isinstance(result, float)
    
    def test_zero_arrival_time(self):
        """Zero arrival time should be valid."""
        result = validate_arrival_time(0.0)
        assert result == 0.0
    
    def test_negative_arrival_time_raises_error(self):
        """Negative arrival time should raise ValueError."""
        with pytest.raises(ValueError, match="must be non-negative"):
            validate_arrival_time(-1.5)
    
    def test_non_numeric_arrival_time_raises_error(self):
        """Non-numeric values should raise TypeError."""
        with pytest.raises(TypeError, match="must be numeric"):
            validate_arrival_time("12.5")
    
    def test_none_arrival_time_raises_error(self):
        """None should raise TypeError."""
        with pytest.raises(TypeError):
            validate_arrival_time(None)


class TestValidateStationCoords:
    """Tests for station coordinates validation."""
    
    def test_valid_coords_tuple(self):
        """Valid coordinate tuple should pass."""
        result = validate_station_coords((35.5, 141.2, 0.0))
        assert result == (35.5, 141.2, 0.0)
    
    def test_valid_coords_list(self):
        """Valid coordinate list should pass."""
        result = validate_station_coords([35.5, 141.2, 0.0])
        assert result == (35.5, 141.2, 0.0)
    
    def test_coords_with_integers(self):
        """Integer coordinates should be converted to floats."""
        result = validate_station_coords([35, 141, 0])
        assert result == (35.0, 141.0, 0.0)
    
    def test_coords_too_few_elements(self):
        """Coordinates with less than 3 elements should raise ValueError."""
        with pytest.raises(ValueError, match="exactly 3 elements"):
            validate_station_coords((35.5, 141.2))
    
    def test_coords_too_many_elements(self):
        """Coordinates with more than 3 elements should raise ValueError."""
        with pytest.raises(ValueError, match="exactly 3 elements"):
            validate_station_coords((35.5, 141.2, 0.0, 100.0))
    
    def test_invalid_latitude(self):
        """Latitude out of range should raise ValueError."""
        with pytest.raises(ValueError, match="Latitude"):
            validate_station_coords((95.0, 141.2, 0.0))
    
    def test_invalid_longitude(self):
        """Longitude out of range should raise ValueError."""
        with pytest.raises(ValueError, match="Longitude"):
            validate_station_coords((35.5, 190.0, 0.0))
    
    def test_non_iterable_coords(self):
        """Non-iterable coordinates should raise TypeError."""
        with pytest.raises(TypeError, match="must be iterable"):
            validate_station_coords(35.5)
    
    def test_non_numeric_coords(self):
        """Non-numeric coordinates should raise TypeError."""
        with pytest.raises(TypeError, match="must be numeric"):
            validate_station_coords((35.5, "141.2", 0.0))


class TestValidateSlabTensorProfile:
    """Tests for slab tensor profile validation."""
    
    def test_valid_profile(self):
        """Valid profile should pass."""
        profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        result = validate_slab_tensor_profile(profile)
        assert result['bulk_modulus'] == 260.0
        assert result['density_ringwoodite'] == 3950.0
    
    def test_profile_with_integer_values(self):
        """Integer values should be converted to floats."""
        profile = {'bulk_modulus': 260, 'density_ringwoodite': 3950}
        result = validate_slab_tensor_profile(profile)
        assert isinstance(result['bulk_modulus'], float)
        assert isinstance(result['density_ringwoodite'], float)
    
    def test_profile_missing_bulk_modulus(self):
        """Profile without bulk_modulus should raise ValueError."""
        with pytest.raises(ValueError, match="missing required keys"):
            validate_slab_tensor_profile({'density_ringwoodite': 3950.0})
    
    def test_profile_missing_density(self):
        """Profile without density_ringwoodite should raise ValueError."""
        with pytest.raises(ValueError, match="missing required keys"):
            validate_slab_tensor_profile({'bulk_modulus': 260.0})
    
    def test_profile_not_dict(self):
        """Non-dictionary profile should raise TypeError."""
        with pytest.raises(TypeError, match="must be a dictionary"):
            validate_slab_tensor_profile([(260.0, 3950.0)])
    
    def test_profile_bulk_modulus_too_low(self):
        """Bulk modulus below reasonable range should raise ValueError."""
        with pytest.raises(ValueError, match="bulk_modulus out of reasonable range"):
            validate_slab_tensor_profile({'bulk_modulus': 0.5, 'density_ringwoodite': 3950.0})
    
    def test_profile_bulk_modulus_too_high(self):
        """Bulk modulus above reasonable range should raise ValueError."""
        with pytest.raises(ValueError, match="bulk_modulus out of reasonable range"):
            validate_slab_tensor_profile({'bulk_modulus': 600.0, 'density_ringwoodite': 3950.0})
    
    def test_profile_density_too_low(self):
        """Density below reasonable range should raise ValueError."""
        with pytest.raises(ValueError, match="density_ringwoodite out of reasonable range"):
            validate_slab_tensor_profile({'bulk_modulus': 260.0, 'density_ringwoodite': 500.0})
    
    def test_profile_density_too_high(self):
        """Density above reasonable range should raise ValueError."""
        with pytest.raises(ValueError, match="density_ringwoodite out of reasonable range"):
            validate_slab_tensor_profile({'bulk_modulus': 260.0, 'density_ringwoodite': 15000.0})
    
    def test_profile_non_numeric_values(self):
        """Non-numeric values in profile should raise TypeError."""
        with pytest.raises(TypeError, match="values must be numeric"):
            validate_slab_tensor_profile({'bulk_modulus': "260.0", 'density_ringwoodite': 3950.0})