#!/usr/bin/env python3
"""
SAE Aero Design Analysis Toolkit - Main Entry Point

This script demonstrates the usage of various modules in the SAE Aero toolkit
and provides a command-line interface for running analyses.

Usage:
    python main.py --gui                    # Launch GUI application
    python main.py --demo                   # Run demonstration analysis
    python main.py --analysis <type>       # Run specific analysis
"""

import sys
import argparse
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def run_gui():
    """Launch the GUI application."""
    try:
        from src.gui.Aero import Ui_MainWindow
        from PyQt5 import QtWidgets

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    except ImportError as e:
        print(f"Error importing GUI modules: {e}")
        print("Please ensure PyQt5 is installed: pip install PyQt5")


def run_demo():
    """Run a comprehensive demonstration of the toolkit capabilities."""
    print("SAE Aero Design Analysis Toolkit - Demonstration")
    print("=" * 50)

    # Import modules
    try:
        from src.calculators.Density_Calculator import calculate_air_density
        from src.calculators.Reynolds_Number_Calculator import calculate_reynolds_number
        from src.analysis.Wing_Loading import calculate_wing_loading
        from src.analysis.Prandtl_Elliptical_Lift_Distribution import EllipticalLiftDistribution
    except ImportError as e:
        print(f"Error importing modules: {e}")
        return

    # Demo parameters
    altitude_m = 304.8  # 1000 feet
    humidity = 60.0  # 60%
    pressure = 101325  # Pa
    velocity = 26.8  # m/s (60 mph)
    chord = 0.9144  # m (3 feet)

    print("\n1. Atmospheric Calculations")
    print("-" * 30)

    # Calculate air density
    try:
        density = calculate_air_density(altitude_m, humidity, pressure)
        print(f"Altitude: {altitude_m:.1f} m ({altitude_m*3.28084:.0f} ft)")
        print(f"Air density: {density:.4f} kg/m³")
    except Exception as e:
        print(f"Error calculating air density: {e}")

    # Calculate Reynolds number
    try:
        # Approximate dynamic viscosity at standard conditions
        dynamic_viscosity = 1.81e-5  # Pa·s
        re_number = calculate_reynolds_number(density, velocity, chord, dynamic_viscosity)
        print(f"Reynolds number: {re_number:,.0f}")
    except Exception as e:
        print(f"Error calculating Reynolds number: {e}")

    print("\n2. Wing Loading Analysis")
    print("-" * 30)

    # Wing loading calculation
    try:
        loading_results = calculate_wing_loading(
            total_weight_lbs=40,
            inner_wing_weight_lbs=5.25,
            outer_wing_weight_lbs=3.25,
            inner_wing_area_ft2=8.0,
            outer_wing_area_ft2=6.0,
        )

        print(f"Total wing loading: {loading_results['total_wing_loading_lbs_per_ft2']:.2f} lbs/ft²")
        print(f"Inner wing loading: {loading_results['inner_wing_loading_lbs_per_ft2']:.2f} lbs/ft²")
        print(f"Outer wing loading: {loading_results['outer_wing_loading_lbs_per_ft2']:.2f} lbs/ft²")
    except Exception as e:
        print(f"Error calculating wing loading: {e}")

    print("\n3. Prandtl Lift Distribution Analysis")
    print("-" * 30)

    try:
        # Create elliptical lift distribution analysis
        analysis = EllipticalLiftDistribution(
            span=180,  # inches
            lift_coefficient=0.8,
            rho=0.00238,  # slug/ft³
            velocity=88,  # ft/s
            root_chord=36,  # inches
            tip_chord=18,  # inches
            design_load=3.52,
        )

        print("Elliptical lift distribution analysis initialized")
        print("Generating analysis plots...")

        # Generate plots if output directory exists
        output_dir = Path(__file__).parent / "output"
        if output_dir.exists():
            analysis.plot_all()
            print("Analysis plots saved to output/Wing_Loading/")
        else:
            print("Output directory not found. Creating...")
            output_dir.mkdir(exist_ok=True)
            analysis.plot_all()
            print("Analysis plots saved to output/Wing_Loading/")

    except Exception as e:
        print(f"Error running lift distribution analysis: {e}")

    print("\nDemo completed successfully!")


def run_analysis(analysis_type):
    """Run specific analysis type."""
    print(f"Running {analysis_type} analysis...")

    if analysis_type == "lift":
        from src.analysis.Lift_Calculator import Lift

        print("Lift analysis functionality available")
    elif analysis_type == "aileron":
        from src.analysis.Aileron_Sizing import calculate_aileron_size_gudmundsson

        print("Aileron sizing functionality available")
    elif analysis_type == "wing":
        from src.analysis.Wing_Loading import calculate_wing_loading

        print("Wing loading functionality available")
    else:
        print(f"Unknown analysis type: {analysis_type}")
        print("Available types: lift, aileron, wing")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="SAE Aero Design Analysis Toolkit", formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--gui", action="store_true", help="Launch GUI application")
    parser.add_argument("--demo", action="store_true", help="Run demonstration analysis")
    parser.add_argument("--analysis", choices=["lift", "aileron", "wing"], help="Run specific analysis type")
    parser.add_argument("--version", action="version", version="SAE Aero Toolkit v1.0.0")

    args = parser.parse_args()

    if args.gui:
        run_gui()
    elif args.demo:
        run_demo()
    elif args.analysis:
        run_analysis(args.analysis)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
