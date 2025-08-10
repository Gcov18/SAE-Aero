import numpy as np

class WingMomentArms:
    def __init__(self, root_chord, tip_chord, span):
        self.root_chord = root_chord
        self.tip_chord = tip_chord
        self.span = span

    def chord_length_at_position(self, y_position):
        # Linear taper from root to tip
        return self.root_chord + (self.tip_chord - self.root_chord) * (y_position / (self.span / 2))

    def aerodynamic_center(self, y_position):
        # Aerodynamic center is typically at the quarter-chord point
        chord_length = self.chord_length_at_position(y_position)
        return 0.25 * chord_length

    def mid_chord_point(self, y_position):
        # Mid-chord point
        chord_length = self.chord_length_at_position(y_position)
        return 0.5 * chord_length

    def calculate_moment_arms(self, y_positions):
        lift_moment_arms = np.zeros(len(y_positions))
        drag_moment_arms = np.zeros(len(y_positions))

        for i, y in enumerate(y_positions):
            ac = self.aerodynamic_center(y)
            mid_chord = self.mid_chord_point(y)
            lift_moment_arms[i] = ac
            drag_moment_arms[i] = mid_chord  # Assuming drag acts at the mid-chord point

        return lift_moment_arms, drag_moment_arms

# Example usage
if __name__ == "__main__":
    # Define wing geometry in inches
    root_chord = 36  # Root chord length in inches
    tip_chord = 12  # Tip chord length in inches
    span = 180  # Total wingspan in inches

    # Create an instance of the class
    wing = WingMomentArms(root_chord, tip_chord, span)

    # Define spanwise positions in inches
    num_positions = 50
    y_positions = np.linspace(0, span / 2, num_positions)  # From root to tip

    # Calculate moment arms
    lift_moment_arms, drag_moment_arms = wing.calculate_moment_arms(y_positions)

    # Print results
    for y, lift_arm, drag_arm in zip(y_positions, lift_moment_arms, drag_moment_arms):
        print(f"Spanwise Position: {y:.2f} in, Lift Moment Arm: {lift_arm:.2f} in, Drag Moment Arm: {drag_arm:.2f} in")