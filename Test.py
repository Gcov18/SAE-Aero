import matplotlib.pyplot as plt

class Aileron:
    def __init__(self, root_chord_length_ft, tip_chord_length_ft, span_ft, hinge_line_position_ft, lift_coefficient, rho_slug_ft3, velocity_ft_s, deflection_angle):
        self.root_chord_length_ft = root_chord_length_ft
        self.tip_chord_length_ft = tip_chord_length_ft
        self.span_ft = span_ft
        self.hinge_line_position_ft = hinge_line_position_ft
        self.lift_coefficient = lift_coefficient
        self.rho_slug_ft3 = rho_slug_ft3
        self.velocity_ft_s = velocity_ft_s
        self.deflection_angle = deflection_angle

    def calculate_average_chord_length(self):
        average_chord_length_ft = (self.root_chord_length_ft + self.tip_chord_length_ft) / 2
        return average_chord_length_ft

    def calculate_lift_force(self):
        q = 0.5 * self.rho_slug_ft3 * self.velocity_ft_s**2
        average_chord_length_ft = self.calculate_average_chord_length()
        lift_per_unit_span = q * self.lift_coefficient * average_chord_length_ft
        total_lift_force = lift_per_unit_span * self.span_ft
        return total_lift_force

    def calculate_moment_arm(self):
        average_chord_length_ft = self.calculate_average_chord_length()
        center_of_pressure_ft = 0.25 * average_chord_length_ft
        moment_arm_ft = center_of_pressure_ft - self.hinge_line_position_ft
        return moment_arm_ft

    def calculate_torque(self):
        lift_force_lb = self.calculate_lift_force()
        moment_arm_ft = self.calculate_moment_arm()
        torque_ft_lb = lift_force_lb * moment_arm_ft
        torque_in_lb = torque_ft_lb * 12
        return torque_in_lb

    def draw_wing_with_aileron(self, wing_root_chord_ft, wing_tip_chord_ft, wing_span_ft):
        fig, ax = plt.subplots()
        
        # Define the coordinates of the wing (left half)
        wing_x_left = [0, wing_root_chord_ft, wing_tip_chord_ft + .50333333, .50333333]
        wing_y_left = [0, 0, wing_span_ft / 2, wing_span_ft / 2]
        
        # Define the coordinates of the aileron (left half)
        aileron_x_left = [
            2.15166667 + self.root_chord_length_ft,
            2.15166667,
            1.982,
            1.982 + self.tip_chord_length_ft
        ]
        aileron_y_left = [
            6.833333333333333-2.63533333,
            6.833333333333333-2.63533333,
            6.833333333333333,
            6.833333333333333
        ]
        
        # Hinge line (left half)
        hinge_line_x_left = [wing_root_chord_ft - self.hinge_line_position_ft, wing_root_chord_ft - self.hinge_line_position_ft]
        hinge_line_y_left = [wing_span_ft / 2 - self.span_ft, wing_span_ft / 2]

        # Leading edge line (left half)
        leading_edge_x_left = [0, .253333]
        leading_edge_y_left = [0, wing_span_ft / 2]

        # Plot the wing (left half)
        ax.plot(wing_x_left, wing_y_left, 'b', label='Wing (Left Half)')

        # Plot the aileron (left half)
        ax.plot(aileron_x_left, aileron_y_left, 'g', label='Aileron (Left Half)')
        ax.plot(hinge_line_x_left, hinge_line_y_left, 'r--', label='Hinge Line (Left Half)')

        # Plot the leading edge (left half)
        ax.plot(leading_edge_x_left, leading_edge_y_left, 'orange', label='Leading Edge (Left Half)')

        # Set labels and title
        ax.set_xlabel('Chord Length (ft)')
        ax.set_ylabel('Span (ft)')
        ax.set_title('Wing Planform with Aileron')

        # Move legend to the left side of the figure
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        # Set equal scaling
        ax.set_aspect('equal', adjustable='box')

        # Set axis limits to show only the left half-span
        ax.set_xlim(-.5, 3.5)
        ax.set_ylim(-.5, 8)

        # Show plot with interactive features
        plt.show()

# Example usage
if __name__ == "__main__":
    root_chord_length_ft = 0.5  # Root chord length in feet (2 meters)
    tip_chord_length_ft = 0.333  # Tip chord length in feet (1 meter)
    span_ft = 2.58333  # Span in feet (1.5 meters)
    hinge_line_position_ft = 0.1  # Hinge line position from the leading edge in feet (0.1 meters)
    lift_coefficient = 1.2  # Lift coefficient at full deflection
    rho_slug_ft3 = 0.002377  # Air density in slugs/ft^3 (1.225 kg/m^3)
    velocity_ft_s = 38  # Flight velocity in ft/s (50 m/s)
    deflection_angle = 20  # Deflection angle in degrees (not used in this simple model)

    aileron = Aileron(root_chord_length_ft, tip_chord_length_ft, span_ft, hinge_line_position_ft, lift_coefficient, rho_slug_ft3, velocity_ft_s, deflection_angle)

    # Calculate the torque
    torque = aileron.calculate_torque()
    print(f"Torque: {torque:.2f} in*lb")
    
    # Define wing geometry
    wing_root_chord_ft = 3.0  # Wing root chord length in feet
    wing_tip_chord_ft = 1.0  # Wing tip chord length in feet
    wing_span_ft = 14.33333333  # Wing full span in feet

    # Draw the wing with the aileron
    aileron.draw_wing_with_aileron(wing_root_chord_ft, wing_tip_chord_ft, wing_span_ft)