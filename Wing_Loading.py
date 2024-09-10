def calculate_wing_loading(total_weight_lbs, wing_area_ft2):
    """
    Calculate the wing loading of an aircraft using imperial units.

    Parameters:
    total_weight_lbs (float): Total weight of the aircraft in pounds (lbs).
    wing_area_ft2 (float): Wing area in square feet (ft²).

    Returns:
    float: Wing loading in lbs/in².
    """
    if wing_area_ft2 <= 0:
        raise ValueError("Wing area must be greater than zero.")
    
    # Convert wing area from square feet to square inches
    wing_area_in2 = wing_area_ft2 * 144
    
    # Calculate wing loading in lbs/in²
    wing_loading_lbs_per_in2 = total_weight_lbs / wing_area_in2
    
    return wing_loading_lbs_per_in2

# Example usage
if __name__ == "__main__":
    # Define the total weight of the aircraft (in pounds)
    total_weight_lbs = 38  # Example value, replace with actual weight

    # Define the wing area (in square feet)
    wing_area_ft2 = 30  # Example value, replace with actual wing area

    try:
        wing_loading = calculate_wing_loading(total_weight_lbs, wing_area_ft2)
        print(f"Wing Loading: {wing_loading:.6f} lbs/in²")
    except ValueError as e:
        print(e)