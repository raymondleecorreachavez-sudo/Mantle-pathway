"""
GMC Anisotropic Velocity Correction Layer
Principal Researcher: Raymond Lee Correa Chavez
License: MIT Open Source

Description: Calculates true hypocenter depth by correcting for the 
'Velocity Illusion' in ultra-dense subducting slabs.
"""

__version__ = "0.1.0"
__author__ = "Raymond Lee Correa Chavez"
__license__ = "MIT"

from .gmc_correction import calculate_corrected_depth

__all__ = ["calculate_corrected_depth"]