# Aileron_Sizing.py

def calculate_aileron_size_gudmundsson(wing_span, wing_area, desired_roll_rate, airspeed, cl_delta, aileron_effectiveness, taper_ratio=1.0):
    """
    Calculate the size of an aileron based on the wing's dimensions and desired roll rate using Gudmundsson's equation.

    Parameters:
    wing_span (float): The span of the wing in feet.
    wing_area (float): The area of the wing in square feet.
    desired_roll_rate (float): The desired roll rate in radians per second.
    airspeed (float): The airspeed in feet per second.
    cl_delta (float): The change in lift coefficient per radian of aileron deflection.
    aileron_effectiveness (float): The effectiveness of the aileron.
    taper_ratio (float): The taper ratio of the wing (tip chord / root chord).

    Returns:
    tuple: The required aileron area in square feet, aileron length in feet, and aileron chord in feet.
    """
    # Constants
    rho = 0.0023769  # Air density at sea level in slugs/ft^3

    # Adjust cl_delta for taper ratio
    cl_delta_adjusted = cl_delta * (1 + taper_ratio) / 2

    # Calculate the rolling moment coefficient
    rolling_moment_coefficient = (2 * desired_roll_rate * wing_span) / (airspeed * cl_delta_adjusted)

    # Calculate the required aileron area using Gudmundsson's equation
    aileron_area = (rolling_moment_coefficient * wing_area) / (2 * cl_delta_adjusted * aileron_effectiveness)

    # Ensure the aileron area is not larger than the wing area
    if aileron_area > wing_area:
        aileron_area = wing_area * 0.12  # Assume aileron area should be at most 10% of wing area

    # Aileron position and dimensions
    aileron_start_span = 0.7 * wing_span  # Aileron starts at 70% of the wing span
    aileron_end_span = 0.9 * wing_span  # Aileron ends at 90% of the wing span
    aileron_length = aileron_end_span - aileron_start_span  # Length of the aileron

    # Calculate the average chord of the wing at the aileron location
    root_chord = 3  # feet (example root chord)
    tip_chord = root_chord * taper_ratio
    average_chord = (root_chord + tip_chord) / 2

    # Aileron chord is typically a fraction of the wing chord at its location
    aileron_chord = 0.25 * average_chord  # Assume aileron chord is 25% of the average wing chord

    return aileron_area, aileron_length, aileron_chord

# Example usage
wing_span = 15  # feet (10 meters converted to feet)
wing_area = 30  # square feet (20 square meters converted to square feet)
desired_roll_rate = 0.274  # radians per second
airspeed = 30  # feet per second (50 meters per second converted to feet per second)
cl_delta = 2.78  # change in lift coefficient per radian of aileron deflection
aileron_effectiveness = 0.9  # aileron effectiveness
taper_ratio = 0.333  # example taper ratio

aileron_area, aileron_length, aileron_chord = calculate_aileron_size_gudmundsson(wing_span, wing_area, desired_roll_rate, airspeed, cl_delta, aileron_effectiveness, taper_ratio)
print(f"The aileron length is {aileron_length:.2f} feet.")
print(f"The aileron chord is {aileron_chord:.2f} feet.")
print(f"The required aileron area is {aileron_area:.2f} square feet.")