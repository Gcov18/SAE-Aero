import numpy as np
import matplotlib.pyplot as plt
import logging
import os

class WingTorsionalLoad:
    def __init__(self, span, lift_distribution, drag_distribution, output_folder='Wing_Torsion'):
        self.span = span
        self.lift_distribution = lift_distribution
        self.drag_distribution = drag_distribution
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)
        logging.info(f"Parameters: span={span} in")

    def torque_at_position(self, y_position, lift, drag, moment_arm_lift, moment_arm_drag):
        # Torque due to lift
        torque_lift = lift * moment_arm_lift
        # Torque due to drag
        torque_drag = drag * moment_arm_drag
        # Total torque
        total_torque = torque_lift + torque_drag
        return total_torque

    def calculate_torsional_load(self, positions, moment_arm_lift, moment_arm_drag):
        torques = np.zeros(len(positions))
        for i, pos in enumerate(positions):
            lift = self.lift_distribution[i]
            drag = self.drag_distribution[i]
            torques[i] = self.torque_at_position(pos, lift, drag, moment_arm_lift, moment_arm_drag)
            logging.debug(f"Position {pos:.2f} in, Lift {lift:.2f} lb, Drag {drag:.2f} lb, Torque {torques[i]:.2f} lb-in")

        # Integrate the torque along the span to get the total torsional load
        total_torsional_load = np.trapz(torques, positions)
        logging.info(f"Total Torsional Load: {total_torsional_load:.2f} lb-in")
        return torques, total_torsional_load

    def plot_torsional_load(self, positions, torques, filename='torsional_load.png'):
        plt.figure(figsize=(10, 6))
        plt.plot(positions, torques, '-o', label='Torsional Load', color='Purple')
        plt.xlabel('Spanwise Position (in)')
        plt.ylabel('Torque (lb-in)')
        plt.title('Torsional Load Distribution')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.output_folder, filename))
        plt.show()
        logging.info(f"Plotted and saved the torsional load distribution")

# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(filename='Wing_Torsion_Log.log', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Define parameters in imperial units (inches)
    span = 15 * 12  # Total wingspan in inches
    num_positions = 50  # Number of positions to calculate
    positions = np.linspace(0, span / 2, num_positions)  # Uniformly spaced positions from root to tip

    # Example lift and drag distributions (these should be calculated based on your aerodynamic model)
    lift_distribution = np.linspace(100, 0, num_positions)  # Example linear decrease in lift
    drag_distribution = np.linspace(10, 0, num_positions)  # Example linear decrease in drag

    # Moment arms (distance from the spar to the point where the force is applied)
    moment_arm_lift = 5  # Example moment arm for lift in inches
    moment_arm_drag = 2  # Example moment arm for drag in inches

    # Create an instance of the class
    torsion = WingTorsionalLoad(span, lift_distribution, drag_distribution)

    # Calculate torsional load
    torques, total_torsional_load = torsion.calculate_torsional_load(positions, moment_arm_lift, moment_arm_drag)

    # Plot torsional load distribution
    torsion.plot_torsional_load(positions, torques)