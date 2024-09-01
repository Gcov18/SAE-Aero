# sizing Ailerons for a given aircraft in imperial units with a tapered straight wing planform

def calculate_aileron_dimensions(wing_span_ft, wing_area_sqft, desired_roll_rate_deg_per_sec, root_chord_ft, tip_chord_ft):
    # Constants
    aileron_effectiveness = 0.9  # Adjusted value for aileron effectiveness
    roll_damping = 0.07  # Adjusted value for roll damping coefficient

    # Calculate the mean aerodynamic chord (MAC) for a tapered wing
    taper_ratio = tip_chord_ft / root_chord_ft
    mac_ft = (2/3) * root_chord_ft * ((1 + taper_ratio + taper_ratio**2) / (1 + taper_ratio))

    # Calculate the aileron area required
    aileron_area_sqft = (desired_roll_rate_deg_per_sec * wing_area_sqft) / (aileron_effectiveness * roll_damping * wing_span_ft)

    # Assume aileron span is 20% of the wing span
    aileron_span_ft = 0.2 * wing_span_ft

    # Calculate aileron chord
    aileron_chord_ft = aileron_area_sqft / aileron_span_ft


    # Ensure aileron chord does not exceed 0.5 of the tip chord
    max_aileron_chord_ft = 0.5 * tip_chord_ft
    if aileron_chord_ft > max_aileron_chord_ft:
        aileron_chord_ft = max_aileron_chord_ft
        aileron_area_sqft = aileron_chord_ft * aileron_span_ft

    return aileron_span_ft, aileron_chord_ft, mac_ft, aileron_area_sqft

# Example usage
wing_span_ft = 15  # feet
wing_area_sqft = 30  # square feet
desired_roll_rate_deg_per_sec = 20.0  # degrees per second
root_chord_ft = 3  # feet
tip_chord_ft = 1  # feet

aileron_span_ft, aileron_chord_ft, mac_ft, aileron_area_sqft = calculate_aileron_dimensions(wing_span_ft, wing_area_sqft, desired_roll_rate_deg_per_sec, root_chord_ft, tip_chord_ft)

print(f"Aileron Span: {aileron_span_ft:.2f} feet")
print(f"Aileron Chord: {aileron_chord_ft:.2f} feet")
print(f"Mean Aerodynamic Chord (MAC): {mac_ft:.2f} feet")
print(f"Aileron Area: {aileron_area_sqft:.2f} square feet")