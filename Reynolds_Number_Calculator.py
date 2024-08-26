import logging

# Configure logging to log everything (DEBUG level and above) and write to a file
logging.basicConfig(filename='log.txt', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Version of the script
__version__ = "0.04"


logging.info(f"Starting Insert Data to Shop Floor script v{__version__}")


def calculate_reynolds_number(density, velocity, characteristic_length, dynamic_viscosity):
    """
    Calculate the Reynolds number for a wing.

    Parameters:
    density (float): Density of the fluid (kg/m^3)
    velocity (float): Velocity of the fluid relative to the wing (m/s)
    characteristic_length (float): Characteristic length (chord length of the wing) (m)
    dynamic_viscosity (float): Dynamic viscosity of the fluid (Pa·s or N·s/m^2)

    Returns:
    float: Reynolds number
    """
    reynolds_number = (density * velocity * characteristic_length) / dynamic_viscosity
    return reynolds_number

# Example usage
if __name__ == "__main__":
    # Define the input parameters
    density = 1.225  # kg/m^3 (density of air at sea level)
    velocity = 50.0  # m/s (example velocity)
    characteristic_length = 2.0  # m (example chord length)
    dynamic_viscosity = 1.81e-5  # Pa·s (dynamic viscosity of air at sea level)

    # Calculate the Reynolds number
    reynolds_number = calculate_reynolds_number(density, velocity, characteristic_length, dynamic_viscosity)

    # Print the result
    print(f"The Reynolds number is: {reynolds_number:.2e}")