def calculate_wing_loading(total_weight_lbs, inner_wing_weight_lbs, outer_wing_weight_lbs, inner_wing_area_ft2, outer_wing_area_ft2):
    """
    Calculate the wing loading of an aircraft using imperial units.

    Parameters:
    total_weight_lbs (float): Total weight of the aircraft in pounds (lbs).
    inner_wing_weight_lbs (float): Weight of the inner wing section in pounds (lbs).
    outer_wing_weight_lbs (float): Weight of the outer wing section in pounds (lbs).
    inner_wing_area_ft2 (float): Inner wing area in square feet (ft²).
    outer_wing_area_ft2 (float): Outer wing area in square feet (ft²).

    Returns:
    dict: Wing loading in lbs/in² and lbs/ft² for inner wing, outer wing, and total wing.
    """
    if inner_wing_area_ft2 <= 0 or outer_wing_area_ft2 <= 0:
        raise ValueError("Wing areas must be greater than zero.")
    
    # Convert wing areas from square feet to square inches
    inner_wing_area_in2 = inner_wing_area_ft2 * 144
    outer_wing_area_in2 = outer_wing_area_ft2 * 144
    total_wing_area_in2 = inner_wing_area_in2 + outer_wing_area_in2
    
    # Calculate wing loading in lbs/in²
    inner_wing_loading_lbs_per_in2 = inner_wing_weight_lbs / inner_wing_area_in2
    outer_wing_loading_lbs_per_in2 = outer_wing_weight_lbs / outer_wing_area_in2
    total_wing_loading_lbs_per_in2 = total_weight_lbs / total_wing_area_in2
    
    # Calculate wing loading in lbs/ft²
    inner_wing_loading_lbs_per_ft2 = inner_wing_weight_lbs / inner_wing_area_ft2
    outer_wing_loading_lbs_per_ft2 = outer_wing_weight_lbs / outer_wing_area_ft2
    total_wing_loading_lbs_per_ft2 = total_weight_lbs / (inner_wing_area_ft2 + outer_wing_area_ft2)
    
    return {
        "inner_wing_loading_lbs_per_in2": inner_wing_loading_lbs_per_in2,
        "outer_wing_loading_lbs_per_in2": outer_wing_loading_lbs_per_in2,
        "total_wing_loading_lbs_per_in2": total_wing_loading_lbs_per_in2,
        "inner_wing_loading_lbs_per_ft2": inner_wing_loading_lbs_per_ft2,
        "outer_wing_loading_lbs_per_ft2": outer_wing_loading_lbs_per_ft2,
        "total_wing_loading_lbs_per_ft2": total_wing_loading_lbs_per_ft2
    }

if __name__ == "__main__":
    # Define the total weight of the aircraft (in pounds)
    total_weight_lbs = 40  

    # Define the weight of the inner wing section (in pounds)
    inner_wing_weight_lbs = 5.25  

    # Define the weight of the outer wing section (in pounds)
    outer_wing_weight_lbs = 3.25  

    # Define the inner wing area (in square feet)
    inner_wing_area_ft2 = 7.8333  

    # Define the outer wing area (in square feet)
    outer_wing_area_ft2 = 7.1667  

    
    wing_loading = calculate_wing_loading(total_weight_lbs, inner_wing_weight_lbs, outer_wing_weight_lbs, inner_wing_area_ft2, outer_wing_area_ft2)
    print(f"Inner Wing Loading: {wing_loading['inner_wing_loading_lbs_per_in2']:.6f} lbs/in², {wing_loading['inner_wing_loading_lbs_per_ft2']:.6f} lbs/ft²")
    print(f"Outer Wing Loading: {wing_loading['outer_wing_loading_lbs_per_in2']:.6f} lbs/in², {wing_loading['outer_wing_loading_lbs_per_ft2']:.6f} lbs/ft²")
    print(f"Total Wing Loading: {wing_loading['total_wing_loading_lbs_per_in2']:.6f} lbs/in², {wing_loading['total_wing_loading_lbs_per_ft2']:.6f} lbs/ft²")
