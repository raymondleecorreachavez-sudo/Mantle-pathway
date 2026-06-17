"""
Setup configuration for GMC Anisotropic Velocity Correction package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gmc-correction",
    version="0.1.0",
    author="Raymond Lee Correa Chavez",
    author_email="contact@gmc-research.example",
    description="GMC Anisotropic Velocity Correction Layer for seismic hypocenter depth calculation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raymondleecorreachavez-sudo/Mantle-pathway",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    keywords="seismology geophysics velocity anisotropy hypocenter",
    project_urls={
        "Bug Reports": "https://github.com/raymondleecorreachavez-sudo/Mantle-pathway/issues",
        "Source": "https://github.com/raymondleecorreachavez-sudo/Mantle-pathway",
    },
)