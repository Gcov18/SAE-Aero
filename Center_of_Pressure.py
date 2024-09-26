class Airfoil:
    def __init__(self, chord_length, lift_coefficient, moment_coefficient, rho, velocity):
        self.chord_length = chord_length
        self.lift_coefficient = lift_coefficient
        self.moment_coefficient = moment_coefficient
        self.rho = rho
        self.velocity = velocity

    def calculate_aerodynamic_forces(self):
        # Calculate dynamic pressure
        q = 0.5 * self.rho * self.velocity**2
        
        # Calculate lift force
        lift = q * self.lift_coefficient * self.chord_length
        
        # Calculate moment about the aerodynamic center (typically at 25% chord)
        moment_ac = q * self.moment_coefficient * self.chord_length**2
        
        return lift, moment_ac

    def calculate_center_of_pressure(self):
        lift, moment_ac = self.calculate_aerodynamic_forces()
        
        # Aerodynamic center is typically at 25% chord
        aerodynamic_center = 0.25 * self.chord_length
        
        # Calculate center of pressure
        center_of_pressure = aerodynamic_center + (moment_ac / lift)
        
        return center_of_pressure

# Example usage
if __name__ == "__main__":
    # Define airfoil geometry and flight conditions
    chord_length = 36  # Chord length in inches
    lift_coefficient = 1.274  # Lift coefficient (CL)
    moment_coefficient = -0.176  # Moment coefficient (Cm)
    rho = 0.0023769  # Air density in slugs/ft³
    velocity = 38.0  # Flight velocity in feet per second

    # Create an instance of the class
    airfoil = Airfoil(chord_length, lift_coefficient, moment_coefficient, rho, velocity)

    # Calculate the center of pressure
    center_of_pressure = airfoil.calculate_center_of_pressure()
    print(f"Center of Pressure: {center_of_pressure:.2f} inches from the leading edge")