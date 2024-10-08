import logging

# Configure logging to log everything (DEBUG level and above) and write to a file
logging.basicConfig(filename='log.txt', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def dynamic_viscosity(temperature):
    """
    Calculate the dynamic viscosity of air using Sutherland's formula.
    
    Parameters:
    temperature (float): Temperature in Kelvin
    
    Returns:
    float: Dynamic viscosity in Pa·s
    """
    # Constants for air
    mu_0 = 1.716e-5  # Reference dynamic viscosity in Pa·s
    T_0 = 273.15  # Reference temperature in Kelvin
    C = 110.4  # Sutherland's constant in Kelvin
    
    # Sutherland's formula
    mu = mu_0 * (temperature / T_0) ** 1.5 * (T_0 + C) / (temperature + C)
    return mu

def main_dynamic_viscocity(temperature):
    """
    Main function to calculate air density given altitude, humidity, and barometric pressure.
    """
    logging.basicConfig(level=logging.INFO)
    viscocity = dynamic_viscosity(temperature)
    logging.info(f"Dynamic viscosity of air at {temperature} K is {viscocity:.6e} Pa·s")
    return viscocity

# Example usage
if __name__ == "__main__":
    # These values can be replaced by inputs from the GUI
    temperature = 300  # Temperature in Kelvin

    main_dynamic_viscocity(temperature)