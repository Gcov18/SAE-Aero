import numpy as np
import logging

def calculate_reynolds_number(density, velocity, chord_length, dynamic_viscosity):
    """
    Calculate the Reynolds number for a wing.

    Parameters:
    density (float): Density of the fluid (kg/m^3)
    velocity (float): Velocity of the fluid relative to the wing (m/s)
    chord_length (float): Chord length of the wing at a specific spanwise position (m)
    dynamic_viscosity (float): Dynamic viscosity of the fluid (Pa·s or N·s/m^2)

    Returns:
    float: Reynolds number
    """
    reynolds_number = (density * velocity * chord_length) / dynamic_viscosity
    return reynolds_number

def chord_length_at_position(root_chord, tip_chord, span, y_position):
    """
    Calculate the chord length at a specific spanwise position for a tapered wing.

    Parameters:
    root_chord (float): Root chord length (m)
    tip_chord (float): Tip chord length (m)
    span (float): Total wingspan (m)
    y_position (float): Spanwise position (m)

    Returns:
    float: Chord length at the given spanwise position (m)
    """
    return root_chord + (tip_chord - root_chord) * (y_position / (span / 2))

def main_reynolds(density, velocity, root_chord, tip_chord, span, dynamic_viscosity, num_positions=50):
    """
    Main function to calculate the average Reynolds number for a tapered wing given fluid properties and wing characteristics.

    Parameters:
    density (float): Density of the fluid (kg/m^3)
    velocity (float): Velocity of the fluid relative to the wing (m/s)
    root_chord (float): Root chord length (m)
    tip_chord (float): Tip chord length (m)
    span (float): Total wingspan (m)
    dynamic_viscosity (float): Dynamic viscosity of the fluid (Pa·s or N·s/m^2)
    num_positions (int): Number of spanwise positions to calculate the Reynolds number

    Returns:
    float: Average Reynolds number
    """
    logging.basicConfig(level=logging.INFO)
    
    y_positions = np.linspace(0, span / 2, num_positions)
    reynolds_numbers = np.array([calculate_reynolds_number(density, velocity, chord_length_at_position(root_chord, tip_chord, span, y), dynamic_viscosity) for y in y_positions])
    
    average_reynolds_number = np.mean(reynolds_numbers)
    logging.info(f"The average Reynolds number is: {average_reynolds_number:.2e}")
    return average_reynolds_number

# Example usage
if __name__ == "__main__":
    # Define the input parameters
    density = 1.225  # kg/m^3 (density of air at sea level)
    velocity = 11.54  # m/s (example velocity)
    root_chord = 0.9144  # m (example root chord length)
    tip_chord = 0.3048  # m (example tip chord length)
    span = 4.572  # m (example wingspan)
    dynamic_viscosity = 1.81e-5  # Pa·s (dynamic viscosity of air at sea level)

    # Calculate the average Reynolds number
    average_reynolds_number = main_reynolds(density, velocity, root_chord, tip_chord, span, dynamic_viscosity)
    print(f"Average Reynolds Number: {average_reynolds_number:.2e}")