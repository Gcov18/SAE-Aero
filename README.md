# SAE Aero Design Analysis Toolkit

A comprehensive toolkit for aerodynamic analysis and design calculations for SAE Aero Design Competition aircraft.

## Project Overview

This project contains various modules and tools for aircraft design analysis, including:
- Atmospheric property calculations
- Aerodynamic force calculations
- Wing loading analysis
- Aileron sizing and effectiveness
- Center of pressure calculations
- Prandtl elliptical lift distribution analysis

## Directory Structure

```
SAE_Aero/
├── src/                          # Source code modules
│   ├── calculators/             # Atmospheric and fluid property calculators
│   │   ├── Density_Calculator.py
│   │   ├── Dynamic_viscosity_Calculator.py
│   │   └── Reynolds_Number_Calculator.py
│   ├── analysis/                # Aerodynamic analysis modules
│   │   ├── Lift_Calculator.py
│   │   ├── Wing_Loading.py
│   │   ├── Aileron_Sizing.py
│   │   ├── Center_of_Pressure.py
│   │   ├── Prandtl_Elliptical_Lift_Distribution.py
│   │   ├── Change_in_Lift_per_radian_of_aileron_deflection.py
│   │   └── Moment_arms.py
│   └── gui/                     # Graphical user interface
│       └── Aero.py
├── output/                      # Generated plots and analysis results
│   ├── Wing_Loading/           # Wing loading analysis plots
│   └── Wing_Torsion/          # Wing torsion analysis plots
├── logs/                       # Log files from various analyses
├── archive/                    # Legacy code and test files
└── README.md                  # This file
```

## Modules Description

### Calculators (`src/calculators/`)

#### `Density_Calculator.py`
Calculates air density at various altitudes and atmospheric conditions using the standard atmosphere model.

**Features:**
- Standard atmosphere temperature calculation
- Barometric pressure calculation
- Air density calculation with humidity correction
- Supports imperial and metric units

**Key Functions:**
- `calculate_temperature(altitude)` - Temperature at given altitude
- `calculate_pressure(altitude)` - Pressure using barometric formula
- `calculate_air_density(altitude, humidity, barometric_pressure)` - Air density calculation

#### `Dynamic_viscosity_Calculator.py`
Calculates dynamic viscosity of air using Sutherland's law for temperature-dependent viscosity.

**Features:**
- Temperature-dependent viscosity calculation
- Sutherland's law implementation
- Logging capability for analysis tracking

#### `Reynolds_Number_Calculator.py`
Calculates Reynolds numbers for wing sections and aerodynamic analysis.

**Features:**
- Reynolds number calculation for wings
- Chord length calculation at spanwise positions
- Support for tapered wing geometries
- Multiple Reynolds number calculations along wingspan

**Key Functions:**
- `calculate_reynolds_number(density, velocity, chord_length, dynamic_viscosity)`
- `chord_length_at_position(root_chord, tip_chord, span, y_position)`

### Analysis Modules (`src/analysis/`)

#### `Lift_Calculator.py`
Comprehensive lift calculation module with airfoil data integration.

**Features:**
- Lift calculation using dynamic pressure and coefficients
- Built-in airfoil coefficient data
- Angle of attack analysis
- Lift coefficient interpolation
- Plotting capabilities for lift vs. angle of attack

**Key Functions:**
- `calculate_dynamic_pressure(velocity, density)`
- `interpolate_cl(alpha)` - Lift coefficient interpolation
- `calculate_lift(alpha)` - Total lift calculation

#### `Wing_Loading.py`
Wing loading analysis for aircraft weight distribution.

**Features:**
- Total aircraft wing loading calculation
- Inner and outer wing section analysis
- Imperial units (lbs/ft² and lbs/in²)
- Comprehensive loading distribution

**Key Functions:**
- `calculate_wing_loading(total_weight_lbs, inner_wing_weight_lbs, outer_wing_weight_lbs, inner_wing_area_ft2, outer_wing_area_ft2)`

#### `Aileron_Sizing.py`
Aileron design and sizing calculations using Gudmundsson's methods.

**Features:**
- Aileron size calculation based on desired roll rate
- Wing taper ratio consideration
- Aileron effectiveness modeling
- Rolling moment coefficient calculation

**Key Functions:**
- `calculate_aileron_size_gudmundsson(wing_span, wing_area, desired_roll_rate, airspeed, cl_delta, aileron_effectiveness, taper_ratio)`

#### `Center_of_Pressure.py`
Center of pressure calculation for airfoil sections.

**Features:**
- Aerodynamic center calculation (typically 25% chord)
- Center of pressure determination
- Moment coefficient integration
- Force and moment analysis

**Key Functions:**
- `calculate_aerodynamic_forces()` - Lift and moment calculation
- `calculate_center_of_pressure()` - Center of pressure location

#### `Prandtl_Elliptical_Lift_Distribution.py`
Advanced wing loading analysis using Prandtl's elliptical lift distribution theory.

**Features:**
- Elliptical lift distribution modeling
- Wing loading calculations with safety factors
- Bending moment and shear force analysis
- Torsional loading calculations
- Comprehensive plotting and visualization
- Design load factor integration

**Key Functions:**
- `lift_at_position(y_position)` - Lift calculation at spanwise position
- `calculate_distributions(positions)` - Complete load distribution analysis
- `plot_all()` - Generate all analysis plots

#### `Change_in_Lift_per_radian_of_aileron_deflection.py`
Aileron effectiveness calculation based on wing geometry.

**Features:**
- Lift coefficient change per radian calculation
- Aspect ratio consideration
- Aileron effectiveness modeling

#### `Moment_arms.py`
Wing moment arm calculations for structural analysis.

**Features:**
- Chord length calculation at any spanwise position
- Linear taper modeling
- Moment arm determination for various wing configurations

### GUI Application (`src/gui/`)

#### `Aero.py`
PyQt5-based graphical user interface for the aerodynamic analysis toolkit.

**Features:**
- User-friendly interface for input parameters
- Integration with calculator modules
- Real-time calculations
- Input validation and error handling
- Logging integration

**Capabilities:**
- Altitude and atmospheric condition input
- Humidity and pressure adjustments
- Direct integration with density and viscosity calculators
- Reynolds number analysis interface

## Quick Start

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd SAE_Aero

# Install requirements
pip install -r requirements.txt

# Optional: Install in development mode
pip install -e .
```

### Usage

#### GUI Application
```bash
python main.py --gui
```

#### Command Line Demo
```bash
python main.py --demo
```

#### Specific Analysis
```bash
python main.py --analysis wing    # Wing loading analysis
python main.py --analysis lift    # Lift analysis
python main.py --analysis aileron # Aileron sizing
```

#### Project Management
```bash
python manage.py status    # Show project status
python manage.py clean     # Clean build artifacts
python manage.py setup     # Setup development environment
python manage.py test      # Run tests
python manage.py format    # Format code with black
python manage.py lint      # Lint code with flake8
```

## Usage Examples
```python
from src.calculators.Density_Calculator import calculate_air_density

# Calculate air density at 1000ft altitude, 60% humidity, standard pressure
density = calculate_air_density(304.8, 60.0, 101325)  # altitude in meters
print(f"Air density: {density:.4f} kg/m³")
```

### Wing Loading Analysis
```python
from src.analysis.Wing_Loading import calculate_wing_loading

results = calculate_wing_loading(
    total_weight_lbs=40,
    inner_wing_weight_lbs=5.25,
    outer_wing_weight_lbs=3.25,
    inner_wing_area_ft2=8.0,
    outer_wing_area_ft2=6.0
)
print(f"Total wing loading: {results['total_wing_loading_lbs_per_ft2']:.2f} lbs/ft²")
```

### Lift Distribution Analysis
```python
from src.analysis.Prandtl_Elliptical_Lift_Distribution import EllipticalLiftDistribution

# Initialize analysis
analysis = EllipticalLiftDistribution(
    span=180,  # inches
    lift_coefficient=0.8,
    rho=0.00238,  # slug/ft³
    velocity=88,  # ft/s
    root_chord=36,  # inches
    tip_chord=18   # inches
)

# Generate analysis plots
analysis.plot_all()
```

## Requirements

- Python 3.x
- NumPy
- Matplotlib
- PyQt5 (for GUI application)
- AeroSandBox (for advanced aerodynamic analysis)
- Logging (standard library)

## Installation

1. Clone or download the project
2. Install required dependencies:
```bash
pip install numpy matplotlib pyqt5 aerosandbox
```
3. Run the GUI application:
```bash
python src/gui/Aero.py
```

## Design Parameters

The toolkit is configured for typical SAE Aero Design Competition aircraft with the following baseline parameters:

- **Wing Span**: 15 feet (180 inches)
- **Wing Area**: 30 square feet
- **Design Speed**: 60 mph (88 ft/s)
- **Operating Altitude**: Sea level to 5000 feet
- **Design Load Factor**: 3.52g (adjustable)
- **Taper Ratio**: Variable (typically 0.5-1.0)

## Output Files

The analysis modules generate various output files in the `output/` directory:

### Wing Loading Analysis
- `lift_distribution.png` - Lift distribution along wingspan
- `load_distribution.png` - Load distribution analysis
- `bending_moment_distribution.png` - Bending moment diagram
- `shear_force_distribution.png` - Shear force distribution
- `torsional_load_distribution.png` - Torsional loading analysis

### Logs
All modules generate detailed log files for debugging and analysis verification:
- Calculation parameters
- Intermediate results
- Error conditions
- Performance metrics

## Configuration

The modules support various configuration options:

- **Units**: Imperial and metric units supported
- **Safety Factors**: Adjustable design load factors
- **Atmospheric Conditions**: Variable altitude, humidity, and pressure
- **Wing Geometry**: Configurable span, chord, taper ratio
- **Airfoil Data**: Integrated coefficient data with interpolation

## Contributing

When adding new modules or features:

1. Follow the existing directory structure
2. Include comprehensive docstrings
3. Add logging for analysis tracking
4. Include unit tests where applicable
5. Update this README with new functionality

## Version History

- **v0.54**: Current GUI application version
- **v0.05**: Initial lift calculator implementation
- Various module updates and improvements

## Archive

The `archive/` directory contains:
- Legacy test files (`bob.py`, `Test.py`)
- Experimental analysis (`Wing_Testing.py`)
- Alternative implementations
- MATLAB scripts (`Prandtl_Elliptical_Lift_Distribution_Matlab.m`)
- Version update utilities (`update_Aero.py`)

## Notes

- All calculations use standard atmospheric conditions unless specified
- Wing loading calculations include safety factor considerations
- The toolkit is designed for educational and competition use
- Validation against known results is recommended for critical applications
