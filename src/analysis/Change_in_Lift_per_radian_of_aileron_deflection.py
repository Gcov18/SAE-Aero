# Aileron_Sizing.py

def calculate_cl_delta(wing_span, wing_area, aileron_effectiveness=0.9):
    """
    Calculate the change in lift coefficient per radian of aileron deflection.

    Parameters:
    wing_span (float): The span of the wing in feet.
    wing_area (float): The area of the wing in square feet.
    aileron_effectiveness (float): The effectiveness of the aileron (default is 0.9).

    Returns:
    float: The change in lift coefficient per radian of aileron deflection.
    """
    # Calculate the aspect ratio (AR)
    aspect_ratio = wing_span**2 / wing_area

    # Calculate Cl_delta using the empirical formula
    cl_delta = (2 * 3.14159 * aileron_effectiveness) / aspect_ratio

    return cl_delta

# Example usage
wing_span = 15  # feet
wing_area = 30  # square feet
aileron_effectiveness = 0.9  # typical value

cl_delta = calculate_cl_delta(wing_span, wing_area, aileron_effectiveness)
print(f"The change in lift coefficient per radian of aileron deflection is {cl_delta:.2f}.")