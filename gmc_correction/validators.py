"""
Input validation utilities for GMC Anisotropic Velocity Correction.
"""

from typing import Dict, Tuple, Any


def validate_arrival_time(arrival_time: Any) -> float:
    """
    Validate and convert arrival time to float.
    
    Parameters
    ----------
    arrival_time : Any
        Arrival time value to validate.
    
    Returns
    -------
    float
        Validated arrival time in seconds.
    
    Raises
    ------
    TypeError
        If arrival_time cannot be converted to float.
    ValueError
        If arrival_time is negative or NaN.
    """
    try:
        arrival_time = float(arrival_time)
    except (ValueError, TypeError):
        raise TypeError(f"arrival_time must be numeric, got {type(arrival_time).__name__}")
    
    if arrival_time < 0:
        raise ValueError(f"arrival_time must be non-negative, got {arrival_time}")
    
    if not isinstance(arrival_time, (int, float)) or (isinstance(arrival_time, float) and arrival_time != arrival_time):
        raise ValueError(f"arrival_time is NaN or invalid")
    
    return arrival_time


def validate_station_coords(coords: Any) -> Tuple[float, float, float]:
    """
    Validate and convert station coordinates to a tuple of floats.
    
    Parameters
    ----------
    coords : Any
        Station coordinates. Should be tuple/list of 3 numeric values (lat, lon, elev).
    
    Returns
    -------
    Tuple[float, float, float]
        Validated coordinates as (latitude, longitude, elevation).
    
    Raises
    ------
    TypeError
        If coords is not iterable or contains non-numeric values.
    ValueError
        If coords doesn't have exactly 3 elements or values are out of valid ranges.
    """
    try:
        coords_list = list(coords)
    except TypeError:
        raise TypeError(f"station_coords must be iterable (tuple, list, etc.), got {type(coords).__name__}")
    
    if len(coords_list) != 3:
        raise ValueError(f"station_coords must have exactly 3 elements (lat, lon, elev), got {len(coords_list)}")
    
    try:
        lat, lon, elev = float(coords_list[0]), float(coords_list[1]), float(coords_list[2])
    except (ValueError, TypeError):
        raise TypeError("station_coords elements must be numeric")
    
    if not (-90 <= lat <= 90):
        raise ValueError(f"Latitude must be between -90 and 90, got {lat}")
    
    if not (-180 <= lon <= 180):
        raise ValueError(f"Longitude must be between -180 and 180, got {lon}")
    
    # Elevation can technically be negative (below sea level) or very positive (high altitude)
    # Reasonable bounds: -11 km (Mariana Trench) to 9 km (Mt. Everest + buffer)
    if not (-15 <= elev <= 15):
        raise ValueError(f"Elevation appears unrealistic: {elev} km (expected -15 to 15 km)")
    
    return (lat, lon, elev)


def validate_slab_tensor_profile(profile: Any) -> Dict[str, float]:
    """
    Validate and convert slab tensor profile dictionary.
    
    Parameters
    ----------
    profile : Any
        Slab tensor profile dictionary. Must contain 'bulk_modulus' and 'density_ringwoodite'.
    
    Returns
    -------
    Dict[str, float]
        Validated tensor profile with normalized float values.
    
    Raises
    ------
    TypeError
        If profile is not a dictionary or contains non-numeric values.
    ValueError
        If required keys are missing or values are out of valid ranges.
    """
    if not isinstance(profile, dict):
        raise TypeError(f"slab_tensor_profile must be a dictionary, got {type(profile).__name__}")
    
    required_keys = {'bulk_modulus', 'density_ringwoodite'}
    missing_keys = required_keys - set(profile.keys())
    
    if missing_keys:
        raise ValueError(f"slab_tensor_profile missing required keys: {missing_keys}")
    
    try:
        bulk_modulus = float(profile['bulk_modulus'])
        density = float(profile['density_ringwoodite'])
    except (ValueError, TypeError):
        raise TypeError("slab_tensor_profile values must be numeric")
    
    # Reasonable bounds for bulk modulus in GPa (for crustal/mantle rocks: ~40-400 GPa)
    if not (1 <= bulk_modulus <= 500):
        raise ValueError(f"bulk_modulus out of reasonable range: {bulk_modulus} GPa (expected 1-500)")
    
    # Reasonable bounds for density in kg/m³ (ringwoodite: ~3900-4100 kg/m³)
    if not (1000 <= density <= 10000):
        raise ValueError(f"density_ringwoodite out of reasonable range: {density} kg/m³ (expected 1000-10000)")
    
    return {
        'bulk_modulus': bulk_modulus,
        'density_ringwoodite': density
    }