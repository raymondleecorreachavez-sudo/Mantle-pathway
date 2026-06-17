# GMC Anisotropic Velocity Correction Layer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

The **GMC Anisotropic Velocity Correction Layer** is a geophysics research package that calculates true hypocenter depth by correcting for the "Velocity Illusion" in ultra-dense subducting slabs. 

This package applies anisotropic tensor stiffness corrections to seismic arrival time data, accounting for the acoustic superhighway effect in deeply subducting lithospheric slabs. It prevents traditional algorithms from defaulting to artificial depth artifacts (e.g., 10 km or 33 km) by using physically-based velocity models.

### Key Features

- **Anisotropic Velocity Correction**: Accounts for non-uniform wave propagation in compressed mantle material
- **Tensor-Based Physics**: Uses bulk modulus and density profiles from ringwoodite phase transitions
- **Ring of Fire Support**: Pre-configured profiles for major subduction zones (Kuril-Kamchatka, Mariana, Tonga-Kermadec, etc.)
- **Robust Input Validation**: Comprehensive checks on coordinates, tensor profiles, and arrival times
- **Multi-Station Depth Estimation**: Aggregate hypocenter depth from multiple seismic stations
- **Well-Documented**: Extensive docstrings and examples

---

## Installation

### From Source

```bash
git clone https://github.com/raymondleecorreachavez-sudo/Mantle-pathway.git
cd Mantle-pathway
pip install -e .
```

### Requirements

- Python 3.8+
- NumPy >= 1.19.0

---

## Quick Start

### Basic Usage

```python
from gmc_correction import calculate_corrected_depth

# Define slab tensor profile (bulk modulus in GPa, density in kg/m³)
profile = {
    'bulk_modulus': 260.0,
    'density_ringwoodite': 3950.0
}

# Station coordinates (latitude, longitude, elevation in km)
station_coords = (35.5, 141.2, 0.0)

# Seismic wave arrival time (seconds)
arrival_time = 12.5

# Calculate corrected distance
true_distance = calculate_corrected_depth(arrival_time, station_coords, profile, verbose=True)
print(f"Corrected hypocenter distance: {true_distance:.2f} km")
```

### Using Pre-Defined Regional Profiles

```python
from gmc_correction.models import get_profile_by_region

# Get pre-configured profile for Ring of Fire
profile = get_profile_by_region('ring_of_fire')

# Use it in calculation
distance = calculate_corrected_depth(12.5, (35.5, 141.2, 0.0), profile.to_dict())
```

### Multi-Station Depth Estimation

```python
from gmc_correction import calculate_corrected_depth

arrival_times = {
    'STATION_001': 10.2,
    'STATION_002': 11.5,
    'STATION_003': 12.8,
}

station_coords = {
    'STATION_001': (35.5, 141.2, 0.0),
    'STATION_002': (36.1, 140.8, 0.2),
    'STATION_003': (34.9, 141.5, 0.1),
}

profile = {
    'bulk_modulus': 260.0,
    'density_ringwoodite': 3950.0
}

# Estimate hypocenter depth
from gmc_correction.gmc_correction import estimate_hypocenter_depth
depth = estimate_hypocenter_depth(arrival_times, station_coords, profile)
print(f"Estimated hypocenter depth: {depth:.2f} km")
```

---

## Physical Background

### The Velocity Illusion

In ultra-dense subducting slabs, seismic waves travel faster than in typical mantle material due to:

1. **Extreme Pressure**: Densifies the material, increasing acoustic velocity
2. **Phase Transitions**: Ringwoodite formation increases bulk modulus
3. **Preferred Orientation**: Anisotropic crystal alignment creates "acoustic superhighways"

Traditional isotropic velocity models (e.g., 8.1 km/s) underestimate wave propagation in these zones, leading to inaccurate hypocenter depth estimates.

### GMC Correction Formula

The anisotropic velocity is calculated as:

```
V_anisotropic = sqrt(K_modified / ρ_ringwoodite)
```

Where:
- **K_modified**: Bulk modulus corrected for acoustic phonon injection (GPa)
- **ρ_ringwoodite**: Density of the ringwoodite phase (kg/m³)

The corrected distance is then:

```
true_distance = arrival_time × V_anisotropic
```

---

## API Reference

### Core Function: `calculate_corrected_depth()`

```python
calculate_corrected_depth(
    arrival_time: float,
    station_coords: Tuple[float, float, float],
    slab_tensor_profile: Dict[str, float],
    verbose: bool = False
) -> float
```

**Parameters:**
- `arrival_time` (float): Seismic wave arrival time in seconds
- `station_coords` (Tuple): Station position as (latitude, longitude, elevation in km)
- `slab_tensor_profile` (Dict): Contains `bulk_modulus` (GPa) and `density_ringwoodite` (kg/m³)
- `verbose` (bool): Enable diagnostic output

**Returns:** Corrected true distance in kilometers

**Example:**
```python
profile = {'bulk_modulus': 260.0, 'density_ringwoodite': 3950.0}
distance = calculate_corrected_depth(12.5, (35.5, 141.2, 0.0), profile)
```

### Utility: `calculate_velocity_correction_factor()`

Returns the multiplicative correction factor (v_anisotropic / v_reference).

```python
from gmc_correction.gmc_correction import calculate_velocity_correction_factor

factor = calculate_velocity_correction_factor(profile)
print(f"Velocity is {factor:.2f}x the standard isotropic velocity")
```

### Data Models

```python
from gmc_correction.models import SlabTensorProfile, SeismicStation, SeismicEvent

# Create a profile
profile = SlabTensorProfile(
    bulk_modulus=260.0,
    density_ringwoodite=3950.0,
    name="Kuril_Kamchatka",
    reference="GMC 2024"
)

# Create a station
station = SeismicStation(
    name="STATION_001",
    latitude=35.5,
    longitude=141.2,
    elevation=0.0
)

# Create an event
event = SeismicEvent(
    event_id="EV_20240617_001",
    arrival_times={'STATION_001': 12.5, 'STATION_002': 13.1},
    slab_profile=profile,
    magnitude=7.2
)
```

### Regional Profiles

Pre-configured profiles are available:

```python
from gmc_correction.models import (
    RING_OF_FIRE_PROFILE,
    KURIL_KAMCHATKA_PROFILE,
    MARIANA_PROFILE,
    TONGA_KERMADEC_PROFILE,
    get_profile_by_region
)

# Direct access
profile = MARIANA_PROFILE

# Or by name (case-insensitive)
profile = get_profile_by_region('mariana')
```

---

## Input Validation

The package includes robust validators:

```python
from gmc_correction.validators import (
    validate_arrival_time,
    validate_station_coords,
    validate_slab_tensor_profile
)

# Validate individual inputs
time = validate_arrival_time(12.5)  # Must be non-negative float
coords = validate_station_coords((35.5, 141.2, 0.0))  # Valid lat/lon/elev
profile = validate_slab_tensor_profile({'bulk_modulus': 260, 'density_ringwoodite': 3950})
```

Validation errors raise `TypeError` or `ValueError` with descriptive messages.

---

## Testing

Run the test suite:

```bash
pytest tests/
```

Tests cover:
- Input validation (edge cases, out-of-range values)
- Core calculations (velocity correction, distance estimation)
- Regional profile loading
- Error handling and exceptions

---

## Configuration Examples

### Subduction Zone Profiles

**Ring of Fire (Composite)**
```python
profile = {
    'bulk_modulus': 260.0,
    'density_ringwoodite': 3950.0
}
```

**Mariana Trench (Deepest)**
```python
profile = {
    'bulk_modulus': 270.0,
    'density_ringwoodite': 3980.0
}
```

**Tonga-Kermadec (Steeply Dipping)**
```python
profile = {
    'bulk_modulus': 255.0,
    'density_ringwoodite': 3910.0
}
```

---

## References

- Karato, S., & Wu, P. (1993). Rheology of the upper mantle: A synthesis. *Science*, 260(5109), 771-778.
- Ringwood, A. E. (1975). Composition and petrology of the Earth's mantle. McGraw-Hill.
- Recent GMC Research Publications (2024) - Available upon request

---

## License

This project is licensed under the **MIT License** — see `LICENSE` file for details.

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes with clear messages
4. Push to your fork
5. Open a Pull Request

---

## Contact & Support

**Principal Researcher:** Raymond Lee Correa Chavez  
**Repository:** https://github.com/raymondleecorreachavez-sudo/Mantle-pathway

For questions or issues, please open a GitHub issue or contact the maintainer.

---

## Disclaimer

This is a research package. While the physics is sound, always validate results against observed data and consult with domain experts for critical applications in earthquake hazard assessment or seismic monitoring.