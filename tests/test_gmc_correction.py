"""
Unit tests for gmc_correction.gmc_correction module.
"""

import pytest
import numpy as np
from gmc_correction import calculate_corrected_depth
from gmc_correction.gmc_correction import (
    calculate_velocity_correction_factor,
    estimate_hypocenter_depth,
)


class TestCalculateCorrectedDepth:
    """Tests for the main calculate_corrected_depth function."""
    
    def test_basic_calculation(self):
        """Basic calculation should return expected distance."""
        profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        coords = (35.5, 141.2, 0.0)
        arrival_time = 10.0
        
        distance = calculate_corrected_depth(arrival_time, coords, profile)
        
        # Result should be positive and greater than isotropic calculation
        assert distance > 0
        assert distance > arrival_time * 8.1  # Standard isotropic velocity
        assert isinstance(distance, (float, np.floating))
    
    def test_zero_arrival_time(self):
        """Zero arrival time should return zero distance."""
        profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        coords = (35.5, 141.2, 0.0)
        
        distance = calculate_corrected_depth(0.0, coords, profile)
        assert distance == 0.0
    
    def test_larger_arrival_time_larger_distance(self):
        """Larger arrival times should result in larger distances."""
        profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        coords = (35.5, 141.2, 0.0)
        
        distance_1 = calculate_corrected_depth(5.0, coords, profile)
        distance_2 = calculate_corrected_depth(10.0, coords, profile)
        
        assert distance_2 > distance_1
        assert pytest.approx(distance_2 / distance_1, rel=1e-5) == 2.0
    
    def test_different_profiles_different_results(self):
        """Different tensor profiles should give different velocities."""
        coords = (35.5, 141.2, 0.0)
        arrival_time = 10.0
        
        profile_1 = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        profile_2 = {'bulk_modulus': 270.0, 'density_ringwoodite': 3980.0}
        
        distance_1 = calculate_corrected_depth(arrival_time, coords, profile_1)
        distance_2 = calculate_corrected_depth(arrival_time, coords, profile_2)
        
        assert distance_1 != distance_2
    
    def test_verbose_output(self, capsys):
        """Verbose mode should produce output."""
        profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        coords = (35.5, 141.2, 0.0)
        
        calculate_corrected_depth(10.0, coords, profile, verbose=True)
        
        captured = capsys.readouterr()
        assert "[INFO]" in captured.out or "[ALERT]" in captured.out
    
    def test_invalid_arrival_time(self):
        """Invalid arrival time should raise error."""
        profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        coords = (35.5, 141.2, 0.0)
        
        with pytest.raises(ValueError):
            calculate_corrected_depth(-1.0, coords, profile)
    
    def test_invalid_station_coords(self):
        """Invalid station coordinates should raise error."""
        profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        
        with pytest.raises(ValueError):
            calculate_corrected_depth(10.0, (95.0, 141.2, 0.0), profile)
    
    def test_invalid_profile(self):
        """Invalid tensor profile should raise error."""
        coords = (35.5, 141.2, 0.0)
        
        with pytest.raises(ValueError):
            calculate_corrected_depth(10.0, coords, {'bulk_modulus': 0.5, 'density_ringwoodite': 3950.0})


class TestCalculateVelocityCorrectionFactor:
    """Tests for velocity correction factor calculation."""
    
    def test_correction_factor_greater_than_one(self):
        """Correction factor should typically be > 1 (anisotropic > isotropic)."""
        profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        
        factor = calculate_velocity_correction_factor(profile)
        assert factor > 1.0
    
    def test_different_profiles_different_factors(self):
        """Different profiles should give different correction factors."""
        profile_1 = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        profile_2 = {'bulk_modulus': 270.0, 'density_ringwoodite': 3980.0}
        
        factor_1 = calculate_velocity_correction_factor(profile_1)
        factor_2 = calculate_velocity_correction_factor(profile_2)
        
        assert factor_1 != factor_2
    
    def test_custom_reference_velocity(self):
        """Custom reference velocity should affect the factor."""
        profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        
        factor_1 = calculate_velocity_correction_factor(profile, reference_velocity=8.1)
        factor_2 = calculate_velocity_correction_factor(profile, reference_velocity=7.0)
        
        assert factor_1 != factor_2
        assert factor_1 < factor_2  # Lower reference gives higher factor


class TestEstimateHypocenterDepth:
    """Tests for multi-station depth estimation."""
    
    def test_single_station_depth_estimation(self):
        """Single station should provide depth estimate."""
        arrival_times = {'STATION_001': 10.0}
        station_coords = {'STATION_001': (35.5, 141.2, 0.0)}
        profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        
        depth = estimate_hypocenter_depth(arrival_times, station_coords, profile)
        
        assert depth is not None
        assert depth > 0
    
    def test_multiple_stations_depth_estimation(self):
        """Multiple stations should average to provide depth estimate."""
        arrival_times = {
            'STATION_001': 10.0,
            'STATION_002': 10.5,
            'STATION_003': 9.8,
        }
        station_coords = {
            'STATION_001': (35.5, 141.2, 0.0),
            'STATION_002': (36.1, 140.8, 0.2),
            'STATION_003': (34.9, 141.5, 0.1),
        }
        profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        
        depth = estimate_hypocenter_depth(arrival_times, station_coords, profile)
        
        assert depth is not None
        assert depth > 0
    
    def test_empty_arrival_times(self):
        """Empty arrival times should return None."""
        arrival_times = {}
        station_coords = {}
        profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        
        depth = estimate_hypocenter_depth(arrival_times, station_coords, profile)
        assert depth is None
    
    def test_mismatched_station_data(self):
        """Mismatched number of stations should raise error."""
        arrival_times = {'STATION_001': 10.0, 'STATION_002': 10.5}
        station_coords = {'STATION_001': (35.5, 141.2, 0.0)}
        profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        
        with pytest.raises(ValueError, match="matching keys"):
            estimate_hypocenter_depth(arrival_times, station_coords, profile)
    
    def test_missing_station_in_coords(self):
        """Missing station in coordinates should raise KeyError."""
        arrival_times = {'STATION_001': 10.0, 'STATION_002': 10.5}
        station_coords = {'STATION_001': (35.5, 141.2, 0.0)}
        profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
        
        with pytest.raises(KeyError):
            estimate_hypocenter_depth(arrival_times, station_coords, profile)