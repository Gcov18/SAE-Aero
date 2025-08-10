"""
Setup script for SAE Aero Design Analysis Toolkit
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, "r") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
else:
    requirements = ["numpy>=1.21.0", "matplotlib>=3.5.0", "PyQt5>=5.15.0"]

setup(
    name="sae-aero-toolkit",
    version="1.0.0",
    author="SAE Aero Team",
    author_email="",
    description="Aerodynamic analysis toolkit for SAE Aero Design Competition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gcov18/SAE-Aero",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "flake8>=4.0.0",
        ],
        "advanced": [
            "aerosandbox>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sae-aero=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
