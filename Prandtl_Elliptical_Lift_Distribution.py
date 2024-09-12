import numpy as np
import matplotlib.pyplot as plt

# Define parameters in imperial units
span = 32.8  # Total wingspan in feet (10 meters converted to feet)
lift_coefficient = 1.0  # Lift coefficient (CL)
rho = 0.0023769  # Air density in slugs/ft³ (1.225 kg/m³ converted to slugs/ft³)
velocity = 164.0  # Flight velocity in ft/s (50 m/s converted to ft/s)
chord_length = 3.28  # Chord length in feet (1 meter converted to feet)

# Calculate the elliptical lift distribution
def elliptical_lift_distribution(span, lift_coefficient, rho, velocity, chord_length):
    b = span / 2  # Semi-span
    y = np.linspace(-b, b, 100)  # Spanwise position from -b to b
    lift_distribution = (4 * lift_coefficient * rho * velocity**2 * chord_length) / (np.pi * span) * np.sqrt(1 - (y / b)**2)
    return y, lift_distribution

# Get the lift distribution
y, lift_distribution = elliptical_lift_distribution(span, lift_coefficient, rho, velocity, chord_length)

# Plot the lift distribution
plt.figure(figsize=(10, 6))
plt.plot(y, lift_distribution, label='Elliptical Lift Distribution')
plt.xlabel('Spanwise Position (ft)')
plt.ylabel('Lift per Unit Span (lb/ft)')
plt.title('Elliptical Lift Distribution along the Wing Span')
plt.legend()
plt.grid(True)
plt.show()