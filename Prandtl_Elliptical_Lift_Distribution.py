import os
import numpy as np
import matplotlib.pyplot as plt
import logging

class EllipticalLiftDistribution:
    def __init__(self, span, lift_coefficient, rho, velocity, root_chord, tip_chord, output_folder='Wing_Loading'):
        self.span = span
        self.lift_coefficient = lift_coefficient
        self.rho = rho
        self.velocity = velocity
        self.root_chord = root_chord
        self.tip_chord = tip_chord
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)
        logging.info(f"Parameters: span={span} in, lift_coefficient={lift_coefficient}, rho={rho}, velocity={velocity} ft/s, root_chord={root_chord} in, tip_chord={tip_chord} in")

    def lift_at_position(self, y_position):
        b = self.span / 2  # Semi-span
        taper_ratio = self.tip_chord / self.root_chord
        chord_length = self.root_chord * (1 - (1 - taper_ratio) * y_position / b)  # Linear taper
        lift = (4 * self.lift_coefficient * self.rho * self.velocity**2 * chord_length) / (np.pi * self.span) * np.sqrt(1 - (y_position / b)**2)
        return lift, chord_length  # Return lift in lb/in

    def calculate_distributions(self, positions):
        lifts_and_chords = [self.lift_at_position(pos) for pos in positions]
        lifts_and_chords[-1] = (0, self.tip_chord)  # Add zero lift at the wingtip

        loads = np.zeros(len(positions))
        for i in range(len(positions) - 1):
            delta_pos = positions[i + 1] - positions[i]
            loads[i] = lifts_and_chords[i][0] * delta_pos
        loads[-1] = lifts_and_chords[-1][0] * (positions[-1] - positions[-2])

        shear_forces = np.zeros(len(positions))
        for i in range(len(positions) - 1, -1, -1):
            if i == len(positions) - 1:
                shear_forces[i] = 0  # Shear force at the wing tip is zero
            else:
                shear_forces[i] = shear_forces[i + 1] + loads[i]

        bending_moments = np.zeros(len(positions))
        for i in range(len(positions) - 1, -1, -1):
            if i == len(positions) - 1:
                bending_moments[i] = 0  # Bending moment at the wing tip is zero
            else:
                delta_pos = positions[i + 1] - positions[i]
                bending_moments[i] = bending_moments[i + 1] + shear_forces[i] * delta_pos

        return lifts_and_chords, loads, shear_forces, bending_moments

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

    def log_results(self, positions, lifts_chords_loads_shear_moment):
        for pos, (lift, chord, load, shear_force, bending_moment) in zip(positions, lifts_chords_loads_shear_moment):
            logging.info(f"Lift per unit span at {pos:.2f} in: {lift:.2f} lb/in, Chord length: {chord:.2f} in, Load: {load:.2f} lb, Shear force: {shear_force:.2f} lb, Bending moment: {bending_moment:.2f} lb-in")

    def save_log_to_picture(self, log_filename='Wing_Loading_Log.log', output_filename='Wing_Loading_log.png'):
        with open(log_filename, 'r') as log_file:
            log_content = log_file.read()

        # Calculate the number of lines in the log content
        lines = log_content.split('\n')
        num_lines = len(lines)

        # Calculate the maximum line length
        max_line_length = max(len(line) for line in lines)

        # Set figure size based on the number of lines and maximum line length, with minimum dimensions
        fig_height = max(10, num_lines * 0.2)
        fig_width = max(10, max_line_length * 0.1)

        plt.figure(figsize=(fig_width, fig_height))  # Set dynamic width and height
        plt.text(0.01, 0.99, log_content, verticalalignment='top', horizontalalignment='left', fontsize=10, family='monospace')
        plt.axis('off')
        plt.savefig(os.path.join(self.output_folder, output_filename))
        plt.show()

# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(filename='Wing_Loading_Log.log', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Define parameters in imperial units (inches)
    span = 15 * 12  # Total wingspan in inches
    lift_coefficient = 1.069  # Lift coefficient (CL)
    rho = 0.0023769  # Air density in slugs/ft³
    velocity = 38.0  # Flight velocity in feet per second
    root_chord = 3 * 12  # Root chord length in inches
    tip_chord = 1 * 12  # Tip chord length in inches

    # Create an instance of the class
    distribution = EllipticalLiftDistribution(span, lift_coefficient, rho, velocity, root_chord, tip_chord)

    # Example positions in inches
    positions = [0.25 * 12, 0.75 * 12, 1.25 * 12, 1.75 * 12, 2.25 * 12, 2.75 * 12, 3.25 * 12, 3.75 * 12, 4.25 * 12, 4.75 * 12, 5.25 * 12, 5.75 * 12, 6.25 * 12, 6.75 * 12, 7.25 * 12, 7.5 * 12]

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

    # Save log to picture
    distribution.save_log_to_picture(log_filename='Wing_Loading_Log.log', output_filename='Wing_Loading_log.png')