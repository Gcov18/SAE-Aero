class Aileron:
    def __init__(self, root_chord_length_ft, tip_chord_length_ft, span_ft, hinge_line_position_ft1, hinge_line_position_ft2, lift_coefficient, rho_slug_ft3, velocity_ft_s, deflection_angle):
        self.root_chord_length_ft = root_chord_length_ft
        self.tip_chord_length_ft = tip_chord_length_ft
        self.span_ft = span_ft
        self.hinge_line_position_ft1 = hinge_line_position_ft1
        self.hinge_line_position_ft2 = hinge_line_position_ft2
        self.lift_coefficient = lift_coefficient
        self.rho_slug_ft3 = rho_slug_ft3
        self.velocity_ft_s = velocity_ft_s
        self.deflection_angle = deflection_angle

    def calculate_average_chord_length(self):
        # Calculate the average chord length for a tapered aileron
        average_chord_length_ft = (self.root_chord_length_ft + self.tip_chord_length_ft) / 2
        return average_chord_length_ft

    def calculate_lift_force(self):
        # Calculate dynamic pressure (q = 0.5 * rho * V^2)
        q = 0.5 * self.rho_slug_ft3 * self.velocity_ft_s**2
        
        # Calculate average chord length
        average_chord_length_ft = self.calculate_average_chord_length()
        
        # Calculate lift force per unit span (L' = q * Cl * c)
        lift_per_unit_span = q * self.lift_coefficient * average_chord_length_ft
        
        # Total lift force (L = L' * b)
        total_lift_force = lift_per_unit_span * self.span_ft
        
        return total_lift_force

    def calculate_moment_arm(self):
        # Assume the center of pressure is at 25% of the average chord length from the leading edge
        average_chord_length_ft = self.calculate_average_chord_length()
        center_of_pressure_ft = 0.25 * average_chord_length_ft
        
        # Calculate the moment arm from each hinge line to the center of pressure
        moment_arm_ft1 = center_of_pressure_ft - self.hinge_line_position_ft1
        moment_arm_ft2 = center_of_pressure_ft - self.hinge_line_position_ft2
        
        # Average the moment arms
        average_moment_arm_ft = (moment_arm_ft1 + moment_arm_ft2) / 2
        
        return average_moment_arm_ft

    def calculate_torque(self):
        # Calculate the lift force
        lift_force_lb = self.calculate_lift_force()
        
        # Calculate the average moment arm
        average_moment_arm_ft = self.calculate_moment_arm()
        
        # Calculate the torque in ft*lb
        torque_ft_lb = lift_force_lb * average_moment_arm_ft
        
        # Convert torque to in*lb (1 ft*lb = 12 in*lb)
        torque_in_lb = torque_ft_lb * 12
        
        return torque_in_lb

# Example usage
if __name__ == "__main__":
    # Define aileron geometry and flight conditions
    root_chord_length_ft = .5  # Root chord length in feet (2 meters)
    tip_chord_length_ft = .333  # Tip chord length in feet (1 meter)
    span_ft = 2.58333  # Span in feet (1.5 meters)
    hinge_line_position_ft1 = 1.33333 # Hinge line position from the leading edge in feet (0.1 meters)
    hinge_line_position_ft2 = 0.816667  # Second hinge line position from the leading edge in feet (0.15 meters)
    lift_coefficient = 1.2  # Lift coefficient at full deflection
    rho_slug_ft3 = 0.002377  # Air density in slugs/ft^3 (1.225 kg/m^3)
    velocity_ft_s = 38  # Flight velocity in ft/s (50 m/s)
    deflection_angle = 20  # Deflection angle in degrees (not used in this simple model)

    # Create an instance of the class
    aileron = Aileron(root_chord_length_ft, tip_chord_length_ft, span_ft, hinge_line_position_ft1, hinge_line_position_ft2, lift_coefficient, rho_slug_ft3, velocity_ft_s, deflection_angle)

    # Calculate the torque
    torque = aileron.calculate_torque()
    print(f"Torque: {torque:.2f} in*lb")