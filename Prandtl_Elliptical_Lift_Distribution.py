import os
import numpy as np
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(filename='lift_distribution.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define parameters in imperial units (inches)
span = 15 * 12  # Total wingspan in inches
lift_coefficient = 1.165  # Lift coefficient (CL)
rho = 0.0023769  # Air density in slugs/ft³
velocity = 38.0  # Flight velocity in feet per second
root_chord = 3 * 12  # Root chord length in inches
tip_chord = 1 * 12  # Tip chord length in inches

logging.info(f"Parameters: span={span} in, lift_coefficient={lift_coefficient}, rho={rho}, velocity={velocity} ft/s, root_chord={root_chord} in, tip_chord={tip_chord} in")

# Create a folder for the plots if it doesn't exist
output_folder = 'Wing_Loading'
os.makedirs(output_folder, exist_ok=True)

# Function to find lift at a specific spanwise position
def lift_at_position(y_position, span, lift_coefficient, rho, velocity, root_chord, tip_chord):
    b = span / 2  # Semi-span
    taper_ratio = tip_chord / root_chord
    chord_length = root_chord * (1 - (1 - taper_ratio) * y_position / b)  # Linear taper
    lift = (4 * lift_coefficient * rho * velocity**2 * chord_length) / (np.pi * span) * np.sqrt(1 - (y_position / b)**2)
    return lift, chord_length  # Return lift in lb/in

# Example: Find lift per unit span and load at specific positions
positions = [0.25 * 12, 0.75 * 12, 1.25 * 12, 1.75 * 12, 2.25 * 12, 2.75 * 12, 3.25 * 12, 3.75 * 12, 4.25 * 12, 4.75 * 12, 5.25 * 12, 5.75 * 12, 6.25 * 12, 6.75 * 12, 7.25 * 12, 7.5 * 12]  # Example positions in inches
lifts_and_chords = [lift_at_position(pos, span, lift_coefficient, rho, velocity, root_chord, tip_chord) for pos in positions]

# Add zero lift at the wingtip
lifts_and_chords[-1] = (0, tip_chord)

# Calculate the load at each position
loads = np.zeros(len(positions))
for i in range(len(positions) - 1):
    delta_pos = positions[i + 1] - positions[i]
    loads[i] = lifts_and_chords[i][0] * delta_pos
# For the last position, use the difference with the previous position
loads[-1] = lifts_and_chords[-1][0] * (positions[-1] - positions[-2])

# Calculate the shear force at each position
shear_forces = np.zeros(len(positions))
for i in range(len(positions) - 1, -1, -1):
    if i == len(positions) - 1:
        shear_forces[i] = 0  # Shear force at the wing tip is zero
    else:
        shear_forces[i] = shear_forces[i + 1] + loads[i]

# Calculate the bending moment at each position
bending_moments = np.zeros(len(positions))
for i in range(len(positions) - 1, -1, -1):
    if i == len(positions) - 1:
        bending_moments[i] = 0  # Bending moment at the wing tip is zero
    else:
        delta_pos = positions[i + 1] - positions[i]
        bending_moments[i] = bending_moments[i + 1] + shear_forces[i] * delta_pos

# Combine lift, chord, load, shear force, and bending moment into a single list
lifts_chords_loads_shear_moment = [(lift, chord, load, shear_force, bending_moment) for (lift, chord), load, shear_force, bending_moment in zip(lifts_and_chords, loads, shear_forces, bending_moments)]

# Plot the lift distribution
plt.figure(num=1, figsize=(10, 6))
plt.plot(positions, [lift for lift, _, _, _, _ in lifts_chords_loads_shear_moment], '-o', label='Elliptical Lift Distribution')
plt.xlabel('Spanwise Position (in)')
plt.ylabel('Lift per Unit Span (lb/in)')
plt.title('Elliptical Lift Distribution at Specific Positions')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(output_folder, 'lift_distribution.png'))
plt.show()
logging.info("Plotted and saved the lift distribution")

# Plot the load distribution
plt.figure(num=2, figsize=(10, 6))
plt.plot(positions, loads, '-o', label='Load Distribution', color='b')
plt.xlabel('Spanwise Position (in)')
plt.ylabel('Load (lb)')
plt.title('Load Distribution at Specific Positions')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(output_folder, 'load_distribution.png'))
plt.show()
logging.info("Plotted and saved the load distribution")

# Plot the shear force distribution
plt.figure(num=3, figsize=(10, 6))
plt.plot(positions, shear_forces, '-o', label='Shear Force Distribution', color='r')
plt.xlabel('Spanwise Position (in)')
plt.ylabel('Shear Force (lb)')
plt.title('Shear Force Distribution at Specific Positions')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(output_folder, 'shear_force_distribution.png'))
plt.show()
logging.info("Plotted and saved the shear force distribution")

# Plot the bending moment distribution
plt.figure(num=4, figsize=(10, 6))
plt.plot(positions, bending_moments, '-o', label='Bending Moment Distribution', color='g')
plt.xlabel('Spanwise Position (in)')
plt.ylabel('Bending Moment (lb-in)')
plt.title('Bending Moment Distribution at Specific Positions')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(output_folder, 'bending_moment_distribution.png'))
plt.show()
logging.info("Plotted and saved the bending moment distribution")

# Log the lift, chord length, load, shear force, and bending moment for each position
for pos, (lift, chord, load, shear_force, bending_moment) in zip(positions, lifts_chords_loads_shear_moment):
    logging.info(f"Lift per unit span at {pos:.2f} in: {lift:.2f} lb/in, Chord length: {chord:.2f} in, Load: {load:.2f} lb, Shear force: {shear_force:.2f} lb, Bending moment: {bending_moment:.2f} lb-in")