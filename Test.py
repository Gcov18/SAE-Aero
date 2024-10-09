import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(filename='Aileron_Loading_Log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Aileron:
    def __init__(self, root_chord_length_in, tip_chord_length_in, span_in, lift_coefficient, rho_slug_ft3, velocity_ft_s, deflection_angle):
        self.root_chord_length_in = root_chord_length_in
        self.tip_chord_length_in = tip_chord_length_in
        self.span_in = span_in
        self.lift_coefficient = lift_coefficient
        self.rho_slug_ft3 = rho_slug_ft3
        self.velocity_ft_s = velocity_ft_s
        self.deflection_angle = deflection_angle
        logging.info(f'Aileron initialized with root_chord_length_in={root_chord_length_in}, tip_chord_length_in={tip_chord_length_in}, span_in={span_in}, lift_coefficient={lift_coefficient}, rho_slug_ft3={rho_slug_ft3}, velocity_ft_s={velocity_ft_s}, deflection_angle={deflection_angle}')

    def calculate_average_chord_length(self):
        average_chord_length_in = (self.root_chord_length_in + self.tip_chord_length_in) / 2
        logging.info(f'Calculated average_chord_length_in={average_chord_length_in}')
        return average_chord_length_in

    def calculate_lift_force(self):
        q = 0.5 * self.rho_slug_ft3 * self.velocity_ft_s**2
        average_chord_length_in = self.calculate_average_chord_length()
        average_chord_length_ft = average_chord_length_in / 12  # Convert inches to feet
        
        # Adjust lift coefficient based on deflection angle
        adjusted_lift_coefficient = self.lift_coefficient * (1 + 0.1 * self.deflection_angle / 20)  # Example adjustment
        
        lift_per_unit_span = q * adjusted_lift_coefficient * average_chord_length_ft
        total_lift_force = lift_per_unit_span * (self.span_in / 12)  # Convert inches to feet
        logging.info(f'Calculated lift_force_lb={total_lift_force} with q={q}, average_chord_length_in={average_chord_length_in}, lift_per_unit_span={lift_per_unit_span}, adjusted_lift_coefficient={adjusted_lift_coefficient}')
        return total_lift_force

    def calculate_moment_arm(self, hinge_line_position_in):
        average_chord_length_in = self.calculate_average_chord_length()
        center_of_pressure_in = 0.25 * average_chord_length_in
        moment_arm_in = center_of_pressure_in - hinge_line_position_in
        logging.info(f'Calculated moment_arm_in={moment_arm_in} with center_of_pressure_in={center_of_pressure_in}')
        return moment_arm_in

    def calculate_torque(self, hinge_line_position_in):
        lift_force_lb = self.calculate_lift_force()
        moment_arm_in = self.calculate_moment_arm(hinge_line_position_in)
        torque_in_lb = lift_force_lb * moment_arm_in
        logging.info(f'Calculated torque_in_lb={torque_in_lb} with lift_force_lb={lift_force_lb}, moment_arm_in={moment_arm_in}')
        return torque_in_lb

    def draw_wing_with_aileron(self, wing_root_chord_in, wing_tip_chord_in, wing_span_in):
        logging.info(f'Drawing wing with aileron with wing_root_chord_in={wing_root_chord_in}, wing_tip_chord_in={wing_tip_chord_in}, wing_span_in={wing_span_in}')
        fig, ax = plt.subplots()
        
        # Define the coordinates of the wing (left half)
        wing_x_left = [0, wing_root_chord_in, wing_tip_chord_in + 6.04, 6.04]
        wing_y_left = [0, 0, wing_span_in / 2, wing_span_in / 2]
        
        # Define the coordinates of the aileron (left half)
        aileron_x_left = [
            19.18 + self.root_chord_length_in,
            19.18,
            15.22,
            15.22 + self.tip_chord_length_in
        ]
        aileron_y_left = [
            82 - 31.62,
            82 - 31.62,
            82,
            82
        ]
        
        # Hinge line (left half)
        hinge_line_x_left = [19.18, 15.22]
        hinge_line_y_left = [82 - 31.62, 82]

        # Leading edge line (left half)
        leading_edge_x_left = [0, 6.04]
        leading_edge_y_left = [0, wing_span_in / 2]

        # MAC line at 43 inches
        mac_x = [3, 27]
        mac_y = [43, 43]

        # Plot the wing (left half)
        ax.plot(wing_x_left, wing_y_left, 'b', label='Wing (Left Half)')

        # Plot the aileron (left half)
        ax.plot(aileron_x_left, aileron_y_left, 'g', label='Aileron (Left Half)')
        ax.plot(hinge_line_x_left, hinge_line_y_left, 'r--', label='Hinge Line (Left Half)')

        # Plot the leading edge (left half)
        ax.plot(leading_edge_x_left, leading_edge_y_left, 'orange', label='Leading Edge (Left Half)')

        # Shade the aileron area with grey
        ax.fill(aileron_x_left, aileron_y_left, 'grey', alpha=0.5, label='Aileron Area')

        # Plot the MAC line
        ax.plot(mac_x, mac_y, 'purple', label='MAC Line')

        # Set labels and title
        ax.set_xlabel('Chord Length (in)')
        ax.set_ylabel('Span (in)')
        ax.set_title('Wing Planform with Aileron')

        # Move legend to the left side of the figure
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        # Set equal scaling
        ax.set_aspect('equal', adjustable='box')

        # Set axis limits to show only the left half-span
        ax.set_xlim(-6, 42)
        ax.set_ylim(-6, 96)

        # Show plot with interactive features
        plt.show()

        # Return the hinge line position
        return hinge_line_x_left[0]  # Example: return the first hinge line position

# Example usage
if __name__ == "__main__":
    root_chord_length_in = 6  # Root chord length in inches (0.5 feet)
    tip_chord_length_in = 4  # Tip chord length in inches (0.333 feet)
    span_in = 31  # Span in inches (2.58333 feet)
    lift_coefficient = 1.2  # Lift coefficient at full deflection
    rho_slug_ft3 = 0.002377  # Air density in slugs/ft^3 (1.225 kg/m^3)
    velocity_ft_s = 38  # Flight velocity in ft/s (50 m/s)
    deflection_angle = 20  # Deflection angle in degrees

    aileron = Aileron(root_chord_length_in, tip_chord_length_in, span_in, lift_coefficient, rho_slug_ft3, velocity_ft_s, deflection_angle)

    # Draw the wing with the aileron and get the hinge line position
    wing_root_chord_in = 36  # Wing root chord length in inches (3 feet)
    wing_tip_chord_in = 12  # Wing tip chord length in inches (1 foot)
    wing_span_in = 172  # Wing full span in inches (14.33333333 feet)
    hinge_line_position_in = aileron.draw_wing_with_aileron(wing_root_chord_in, wing_tip_chord_in, wing_span_in)

    # Calculate the torque using the plotted hinge line position
    torque = aileron.calculate_torque(hinge_line_position_in)
    print(f"Torque: {torque:.2f} in*lb")