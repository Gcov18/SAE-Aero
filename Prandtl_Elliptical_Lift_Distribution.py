import numpy as np
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(filename='lift_distribution.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define parameters in imperial units
span = 15  # Total wingspan in feet
lift_coefficient = 1.165  # Lift coefficient (CL)
rho = 0.0023769  # Air density in slugs/ft³
velocity = 32.0  # Flight velocity in ft/s
root_chord = 3  # Root chord length in feet
tip_chord = 1  # Tip chord length in feet

logging.info(f"Parameters: span={span}, lift_coefficient={lift_coefficient}, rho={rho}, velocity={velocity}, root_chord={root_chord}, tip_chord={tip_chord}")

# Calculate the elliptical lift distribution with taper ratio
def elliptical_lift_distribution(span, lift_coefficient, rho, velocity, root_chord, tip_chord):
    b = span / 2  # Semi-span
    taper_ratio = tip_chord / root_chord
    y = np.linspace(-b, b, 100)  # Spanwise position from -b to b
    chord_length = root_chord * (1 - (1 - taper_ratio) * np.abs(y) / b)  # Linear taper
    lift_distribution = (4 * lift_coefficient * rho * velocity**2 * chord_length) / (np.pi * span) * np.sqrt(1 - (y / b)**2)
    logging.info("Calculated elliptical lift distribution")
    return y, lift_distribution, chord_length

# Function to find lift at a specific spanwise position
def lift_at_position(y_position, span, lift_coefficient, rho, velocity, root_chord, tip_chord):
    b = span / 2  # Semi-span
    taper_ratio = tip_chord / root_chord
    chord_length = root_chord * (1 - (1 - taper_ratio) * np.abs(y_position) / b)  # Linear taper
    lift = (4 * lift_coefficient * rho * velocity**2 * chord_length) / (np.pi * span) * np.sqrt(1 - (y_position / b)**2)
    lift_in = lift / 12  # Convert from lb/ft to lb/in
    return lift_in, chord_length  # Return lift in lb/in

# Get the lift distribution
y, lift_distribution, chord_lengths = elliptical_lift_distribution(span, lift_coefficient, rho, velocity, root_chord, tip_chord)

# Convert lift distribution from lb/ft to lb/in
lift_distribution_in_lbs = lift_distribution / 12

# Plot the lift distribution
plt.figure(figsize=(10, 6))
plt.plot(y, lift_distribution_in_lbs, label='Elliptical Lift Distribution')
plt.xlabel('Spanwise Position (ft)')
plt.ylabel('Lift per Unit Span (lb/in)')
plt.title('Elliptical Lift Distribution along the Wing Span')
plt.legend()
plt.grid(True)
plt.show()
logging.info("Plotted the lift distribution")

# Example: Find lift per unit span and load at specific positions
positions = [7.5, 7, 6.5, 6, 5.5, 5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5, 0]  # Example positions in feet
lifts_and_chords = [lift_at_position(pos, span, lift_coefficient, rho, velocity, root_chord, tip_chord) for pos in positions]

for pos, (lift, chord) in zip(positions, lifts_and_chords):
    load = lift * chord  # Calculate the load at each position
    logging.info(f"Lift per unit span at {pos} ft: {lift:.2f} lb/in, Chord length: {chord:.2f} ft, Load: {load:.2f} lb")