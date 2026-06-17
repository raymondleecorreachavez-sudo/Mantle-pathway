"""
Data structures and models for GMC Anisotropic Velocity Correction.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class SlabTensorProfile:
    """
    Represents a slab tensor stiffness profile for anisotropic velocity correction.
    
    Attributes
    ----------
    bulk_modulus : float
        Bulk modulus modified by acoustic phonon injection (GPa).
    density_ringwoodite : float
        Density of ringwoodite phase (kg/m³).
    name : str, optional
        Descriptive name for this profile (e.g., "Kuril-Kamchatka_Ring_of_Fire").
    reference : str, optional
        Citation or reference for this profile's data.
    """
    bulk_modulus: float
    density_ringwoodite: float
    name: Optional[str] = None
    reference: Optional[str] = None
    
    def to_dict(self) -> Dict[str, float]:
        """Convert profile to dictionary format."""
        return {
            'bulk_modulus': self.bulk_modulus,
            'density_ringwoodite': self.density_ringwoodite
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SlabTensorProfile':
        """Create profile from dictionary."""
        return cls(
            bulk_modulus=data['bulk_modulus'],
            density_ringwoodite=data['density_ringwoodite'],
            name=data.get('name'),
            reference=data.get('reference')
        )


@dataclass
class SeismicStation:
    """
    Represents a seismic monitoring station.
    
    Attributes
    ----------
    name : str
        Station identifier (e.g., "STATION_001").
    latitude : float
        Station latitude in degrees (-90 to 90).
    longitude : float
        Station longitude in degrees (-180 to 180).
    elevation : float
        Station elevation in kilometers.
    """
    name: str
    latitude: float
    longitude: float
    elevation: float
    
    def get_coords(self) -> tuple:
        """Return coordinates as (lat, lon, elev) tuple."""
        return (self.latitude, self.longitude, self.elevation)


@dataclass
class SeismicEvent:
    """
    Represents a seismic event with arrival time data at multiple stations.
    
    Attributes
    ----------
    event_id : str
        Unique event identifier.
    arrival_times : Dict[str, float]
        Station name to arrival time (seconds) mapping.
    slab_profile : SlabTensorProfile
        Tensor profile for velocity correction.
    magnitude : Optional[float]
        Event magnitude (Richter scale, if available).
    """
    event_id: str
    arrival_times: Dict[str, float]
    slab_profile: SlabTensorProfile
    magnitude: Optional[float] = None
    
    def get_profile_dict(self) -> Dict:
        """Get profile as dictionary."""
        return self.slab_profile.to_dict()


# Pre-defined regional slab tensor profiles
RING_OF_FIRE_PROFILE = SlabTensorProfile(
    bulk_modulus=260.0,
    density_ringwoodite=3950.0,
    name="Ring_of_Fire_Composite",
    reference="GMC Research 2024"
)

KURIL_KAMCHATKA_PROFILE = SlabTensorProfile(
    bulk_modulus=265.0,
    density_ringwoodite=3920.0,
    name="Kuril_Kamchatka_Trench",
    reference="GMC Research 2024"
)

MARIANA_PROFILE = SlabTensorProfile(
    bulk_modulus=270.0,
    density_ringwoodite=3980.0,
    name="Mariana_Trench",
    reference="GMC Research 2024"
)

TONGA_KERMADEC_PROFILE = SlabTensorProfile(
    bulk_modulus=255.0,
    density_ringwoodite=3910.0,
    name="Tonga_Kermadec_Trench",
    reference="GMC Research 2024"
)

# Mapping of subduction zone names to profiles
REGIONAL_PROFILES = {
    'ring_of_fire': RING_OF_FIRE_PROFILE,
    'kuril_kamchatka': KURIL_KAMCHATKA_PROFILE,
    'mariana': MARIANA_PROFILE,
    'tonga_kermadec': TONGA_KERMADEC_PROFILE,
}


def get_profile_by_region(region_name: str) -> SlabTensorProfile:
    """
    Get a pre-defined slab tensor profile by region name.
    
    Parameters
    ----------
    region_name : str
        Region name (case-insensitive). Options: 'ring_of_fire', 'kuril_kamchatka', 'mariana', 'tonga_kermadec'.
    
    Returns
    -------
    SlabTensorProfile
        The corresponding tensor profile.
    
    Raises
    ------
    KeyError
        If region_name is not found.
    """
    region_key = region_name.lower().strip()
    if region_key not in REGIONAL_PROFILES:
        available = ", ".join(REGIONAL_PROFILES.keys())
        raise KeyError(f"Region '{region_name}' not found. Available: {available}")
    
    return REGIONAL_PROFILES[region_key]