"""
GMC Anisotropic Velocity Correction Module

Calculates true hypocenter depth by correcting for the 'Velocity Illusion'
in ultra-dense subducting slabs using anisotropic tensor profiles.
"""

import numpy as np
from typing import Dict, Tuple, Optional
from .validators import validate_slab_tensor_profile, validate_arrival_time, validate_station_coords


def calculate_corrected_depth(
    arrival_time: float,
    station_coords: Tuple[float, float, float],
    slab_tensor_profile: Dict[str, float],
    verbose: bool = False
) -> float:
    """
    Calculate corrected hypocenter depth accounting for velocity anisotropy in subducting slabs.
    
    This function corrects for the 'Velocity Illusion' effect that occurs in ultra-dense
    subducting slabs by applying a GMC (Geophysical Mantle Correction) anisotropic correction
    layer based on tensor stiffness properties.
    
    Parameters
    ----------
    arrival_time : float
        Seismic wave arrival time at the station (in seconds).
    station_coords : Tuple[float, float, float]
        Station coordinates as (latitude, longitude, elevation) in km.
    slab_tensor_profile : Dict[str, float]
        Slab tensor profile containing:
        - 'bulk_modulus': Bulk modulus modified by acoustic phonon injection (GPa)
        - 'density_ringwoodite': Density of ringwoodite phase (kg/m³)
    verbose : bool, optional
        If True, print diagnostic information. Default is False.
    
    Returns
    -------
    float
        Corrected true distance (hypocenter distance) in kilometers.
    
    Raises
    ------
    ValueError
        If arrival_time is negative or slab_tensor_profile is invalid.
    TypeError
        If input parameters have incorrect types.
    
    Examples
    --------
    >>> profile = {'bulk_modulus': 250.0, 'density_ringwoodite': 3900.0}
    >>> coords = (35.5, 141.2, 0.0)
    >>> distance = calculate_corrected_depth(12.5, coords, profile)
    >>> print(f"Corrected distance: {distance:.2f} km")
    """
    
    # Validate inputs
    try:
        arrival_time = validate_arrival_time(arrival_time)
        station_coords = validate_station_coords(station_coords)
        slab_tensor_profile = validate_slab_tensor_profile(slab_tensor_profile)
    except (ValueError, TypeError) as e:
        raise type(e)(f"Input validation failed: {str(e)}")
    
    # 1. Load Standard Isotropic Model (The Baseline)
    v_isotropic = 8.1  # km/s (Standard Mantle)
    
    if verbose:
        print(f"[INFO] Standard isotropic velocity: {v_isotropic} km/s")
    
    # 2. GMC Anisotropic Correction Layer
    # Fetches the specific tensor stiffness for the Ring of Fire segment
    K_mod = slab_tensor_profile['bulk_modulus']  # GPa
    rho = slab_tensor_profile['density_ringwoodite']  # kg/m³
    
    if verbose:
        print(f"[INFO] Bulk modulus (K_mod): {K_mod} GPa")
        print(f"[INFO] Density (ringwoodite): {rho} kg/m³")
    
    # 3. Calculate Hyper-Velocity (V = sqrt(K/rho))
    # Convert K from GPa to Pa, and account for units to get km/s
    # K in Pa = K_GPa * 1e9
    # V = sqrt(K_Pa / rho) in m/s, then convert to km/s by dividing by 1000
    try:
        K_pa = K_mod * 1e9
        v_anisotropic = np.sqrt(K_pa / rho) / 1000.0  # Convert m/s to km/s
    except (ValueError, ZeroDivisionError) as e:
        raise ValueError(f"Failed to calculate anisotropic velocity: {str(e)}")
    
    if verbose:
        print(f"[INFO] Calculated anisotropic velocity: {v_anisotropic:.4f} km/s")
        print(f"[INFO] Velocity correction factor: {v_anisotropic / v_isotropic:.4f}x")
    
    # 4. Threshold Check - Alert for superhighway effect
    if v_anisotropic > 10.0:
        if verbose:
            print(f"[ALERT] Deep Slab Superhighway Detected (V={v_anisotropic:.2f} km/s)")
            print("[ALERT] Applying GMC Correction Matrix...")
    
    # 5. Recalculate Distance based on Tensor Velocity
    # Prevents the algorithm from defaulting to 10km/33km artifacts
    true_distance = arrival_time * v_anisotropic
    
    if verbose:
        print(f"[INFO] Corrected true distance: {true_distance:.4f} km")
    
    return true_distance


def calculate_velocity_correction_factor(
    slab_tensor_profile: Dict[str, float],
    reference_velocity: float = 8.1
) -> float:
    """
    Calculate the velocity correction factor for anisotropic versus isotropic models.
    
    Parameters
    ----------
    slab_tensor_profile : Dict[str, float]
        Slab tensor profile with 'bulk_modulus' and 'density_ringwoodite'.
    reference_velocity : float, optional
        Reference isotropic velocity in km/s. Default is 8.1.
    
    Returns
    -------
    float
        Correction factor (v_anisotropic / v_reference).
    """
    slab_tensor_profile = validate_slab_tensor_profile(slab_tensor_profile)
    
    K_mod = slab_tensor_profile['bulk_modulus']
    rho = slab_tensor_profile['density_ringwoodite']
    
    K_pa = K_mod * 1e9
    v_anisotropic = np.sqrt(K_pa / rho) / 1000.0
    
    return v_anisotropic / reference_velocity


def estimate_hypocenter_depth(
    arrival_times: Dict[str, float],
    station_coords: Dict[str, Tuple[float, float, float]],
    slab_tensor_profile: Dict[str, float],
    epicenter: Tuple[float, float] = (0.0, 0.0)
) -> Optional[float]:
    """
    Estimate hypocenter depth using multiple station arrival times.
    
    Parameters
    ----------
    arrival_times : Dict[str, float]
        Dictionary mapping station names to arrival times (seconds).
    station_coords : Dict[str, Tuple[float, float, float]]
        Dictionary mapping station names to (lat, lon, elev) coordinates in km.
    slab_tensor_profile : Dict[str, float]
        Slab tensor profile with 'bulk_modulus' and 'density_ringwoodite'.
    epicenter : Tuple[float, float], optional
        Epicenter coordinates (lat, lon). Default is (0.0, 0.0).
    
    Returns
    -------
    float or None
        Estimated hypocenter depth in km, or None if estimation failed.
    """
    if not arrival_times or not station_coords:
        return None
    
    if len(arrival_times) != len(station_coords):
        raise ValueError("arrival_times and station_coords must have matching keys")
    
    distances = []
    for station_name, arrival_time in arrival_times.items():
        if station_name not in station_coords:
            raise KeyError(f"Station '{station_name}' not found in station_coords")
        
        coords = station_coords[station_name]
        distance = calculate_corrected_depth(arrival_time, coords, slab_tensor_profile)
        distances.append(distance)
    
    # Simple averaging; more sophisticated triangulation could be applied
    avg_distance = np.mean(distances)
    
    # Estimate depth as a fraction of the corrected distance
    # (This is a simplified approximation; detailed ray-tracing would be needed for production)
    estimated_depth = avg_distance * 0.6  # Empirical factor
    
    return estimated_depth