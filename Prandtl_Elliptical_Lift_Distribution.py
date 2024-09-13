import os
import numpy as np
import matplotlib.pyplot as plt
import logging

class EllipticalLiftDistribution:
    def __init__(self, span, lift_coefficient, rho, velocity, root_chord, tip_chord, output_folder='Wing_Loading', design_load=3.52):
        self.span = span
        self.lift_coefficient = lift_coefficient
        self.rho = rho
        self.velocity = velocity
        self.root_chord = root_chord
        self.tip_chord = tip_chord
        self.output_folder = output_folder
        self.design_load = design_load
        os.makedirs(self.output_folder, exist_ok=True)
        logging.info(f"Parameters: span={span} in, lift_coefficient={lift_coefficient}, rho={rho}, velocity={velocity} ft/s, root_chord={root_chord} in, tip_chord={tip_chord} in")

    # Calculate lift at a given spanwise position
    def lift_at_position(self, y_position):
        b = self.span / 2  # Semi-span
        taper_ratio = self.tip_chord / self.root_chord
        chord_length = self.root_chord * (1 - (1 - taper_ratio) * y_position / b)  # Linear taper
        lift = (4 * self.lift_coefficient * self.rho * self.velocity**2 * chord_length) / (np.pi * self.span) * np.sqrt(1 - (y_position / b)**2)
        return lift, chord_length  # Return lift in lb/in
    
    # Calculate loads, shear forces, and bending moments
    def calculate_distributions(self, positions):
        lifts_and_chords = [self.lift_at_position(pos) for pos in positions]
        lifts_and_chords[-1] = (0, self.tip_chord)  # Add zero lift at the wingtip

        loads = np.zeros(len(positions))
        for i in range(len(positions) - 1):
            delta_pos = positions[i + 1] - positions[i]
            loads[i] = lifts_and_chords[i][0] * delta_pos
            logging.debug(f"Position {positions[i]:.2f} in, Lift {lifts_and_chords[i][0]:.2f} lb/in, Delta Pos {delta_pos:.2f} in, Load {loads[i]:.2f} lb")
        loads[-1] = lifts_and_chords[-1][0] * (positions[-1] - positions[-2])
        logging.debug(f"Position {positions[-1]:.2f} in, Lift {lifts_and_chords[-1][0]:.2f} lb/in, Delta Pos {positions[-1] - positions[-2]:.2f} in, Load {loads[-1]:.2f} lb")

        shear_forces = np.zeros(len(positions))
        for i in range(len(positions) - 1, -1, -1):
            if i == len(positions) - 1:
                shear_forces[i] = 0  # Shear force at the wing tip is zero
            else:
                shear_forces[i] = shear_forces[i + 1] + loads[i]
            logging.debug(f"Position {positions[i]:.2f} in, Shear Force {shear_forces[i]:.2f} lb")

        bending_moments = np.zeros(len(positions))
        for i in range(len(positions) - 1, -1, -1):
            if i == len(positions) - 1:
                bending_moments[i] = 0  # Bending moment at the wing tip is zero
            else:
                delta_pos = positions[i + 1] - positions[i]
                bending_moments[i] = bending_moments[i + 1] + shear_forces[i] * delta_pos
            logging.debug(f"Position {positions[i]:.2f} in, Bending Moment {bending_moments[i]:.2f} lb-in")

        return lifts_and_chords, loads, shear_forces, bending_moments

    # Plot distributions
    def plot_distribution(self, positions, values, ylabel, title, filename, figure_num, color='b', fontweight='normal'):
        plt.figure(num=figure_num, figsize=(10, 6))
        plt.plot(positions, values, '-o', label=title, color=color)
        plt.xlabel('Spanwise Position (in)')
        plt.ylabel(ylabel)
        plt.title(f"{title}\nVelocity: {self.velocity} ft/s, Lift Coefficient: {self.lift_coefficient}, Air Density: {self.rho} slugs/ft³", fontweight=fontweight)
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.output_folder, filename))
        plt.show()
        logging.info(f"Plotted and saved the {title.lower()}")

    # Log results
    def log_results(self, positions, lifts_chords_loads_shear_moment):
        for pos, (lift, chord, load, shear_force, bending_moment) in zip(positions, lifts_chords_loads_shear_moment):
            logging.info(f"Lift per unit span at {pos:.2f} in: {lift:.2f} lb/in, Chord length: {chord:.2f} in, Load: {load:.2f} lb, Shear force: {shear_force:.2f} lb, Bending moment: {bending_moment:.2f} lb-in")

    # Size the spar
    def size_spar(self, bending_moments, yield_strength):
        max_bending_moment = max(bending_moments)
        required_section_modulus = max_bending_moment * self.design_load / yield_strength

        # Given specifications
        top_bottom_thickness = 0.25  # 1/4" spars at the top and bottom
        side_thickness = 0.125  # 1/8" thick pieces on the sides

        # Initial guess for height and width
        h = 2.5  # Initial guess for height in inches
        b = .5  # Initial guess for width in inches

        # Calculate the section modulus for a hollow rectangular cross-section
        def section_modulus(h, b, top_bottom_thickness, side_thickness):
            outer_area = b * h
            inner_height = h - 2 * top_bottom_thickness
            inner_width = b - 2 * side_thickness
            inner_area = inner_width * inner_height
            net_area = outer_area - inner_area
            return (b * h**2 - inner_width * inner_height**2) / 6

        # Adjust dimensions to meet the required section modulus
        while section_modulus(h, b, top_bottom_thickness, side_thickness) < required_section_modulus:
            h += 0.1  # Increment height
            b += 0.1  # Increment width

        # Calculate the section modulus of the sized spar
        final_section_modulus = section_modulus(h, b, top_bottom_thickness, side_thickness)

        # Determine the maximum bending moment the spar can handle
        max_bending_moment_handled = final_section_modulus * yield_strength / self.design_load

        logging.info(f"Max bending moment: {max_bending_moment:.2f} lb-in")
        logging.info(f"Required section modulus: {required_section_modulus:.2f} in^3")
        logging.info(f"Spar dimensions: height = {h:.2f} in, width = {b:.2f} in")
        logging.info(f"Max bending moment the spar can handle: {max_bending_moment_handled:.2f} lb-in")

        return h, b, max_bending_moment_handled

# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(filename='Wing_Loading_Log.log', level=logging.DEBUG, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Define parameters in imperial units (inches)
    span = 15 * 12  # Total wingspan in inches
    lift_coefficient = .946  # Lift coefficient (CL)
    rho = 0.0023769  # Air density in slugs/ft³
    velocity = 38.0  # Flight velocity in feet per second
    root_chord = 3 * 12  # Root chord length in inches
    tip_chord = 1 * 12  # Tip chord length in inches
    # design_load = 3.52  # Design load
    # Sf = 1.10  # Safety factor
    # G_load = 3.2  # Gust load

    # Create an instance of the class
    distribution = EllipticalLiftDistribution(span, lift_coefficient, rho, velocity, root_chord, tip_chord)

    # Example positions in inches
    positions = [0.166667 * 12, 0.5 * 12, 0.833333 * 12, 1.16667 * 12, 1.5 * 12, 1.83333 * 12, 2.16667 * 12, 2.5 * 12, 2.83333 * 12, 3.16667 * 12, 3.458333 * 12, 3.75 * 12, 4.08333 * 12, 4.41667 * 12, 4.75 * 12, 5.08333 * 12, 5.41667 * 12, 5.75 * 12, 6.08333 * 12, 6.41667 * 12, 6.75 * 12, 7.041667 * 12, 7.16667 * 12]

    # Calculate distributions
    lifts_and_chords, loads, shear_forces, bending_moments = distribution.calculate_distributions(positions)

    # Combine lift, chord, load, shear force, and bending moment into a single list
    lifts_chords_loads_shear_moment = [(lift, chord, load, shear_force, bending_moment) for (lift, chord), load, shear_force, bending_moment in zip(lifts_and_chords, loads, shear_forces, bending_moments)]

    # Plot distributions
    distribution.plot_distribution(positions, [lift for lift, _, _, _, _ in lifts_chords_loads_shear_moment], 'Lift per Unit Span (lb/in)', 'Elliptical Lift Distribution', 'lift_distribution.png', figure_num=1, color='Indigo')
    distribution.plot_distribution(positions, loads, 'Load (lb)', 'Load Distribution', 'load_distribution.png', figure_num=2, color='Orange')
    distribution.plot_distribution(positions, shear_forces, 'Shear Force (lb)', 'Shear Force Distribution', 'shear_force_distribution.png', figure_num=3, color='Red')
    distribution.plot_distribution(positions, bending_moments, 'Bending Moment (lb-in)', 'Bending Moment Distribution', 'bending_moment_distribution.png', figure_num=4, color='Green')

    # Log results
    distribution.log_results(positions, lifts_chords_loads_shear_moment)

    # Size the spar
    yield_strength = 12742  # Example yield strength in psi
    spar_height, spar_width, max_bending_moment_handled = distribution.size_spar(bending_moments, yield_strength)