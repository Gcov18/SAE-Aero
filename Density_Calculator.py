import math
import logging

# Configure logging to log everything (DEBUG level and above) and write to a file
logging.basicConfig(filename='log.txt', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
R = 287.05  # Specific gas constant for dry air, J/(kg·K)
g = 9.80665  # Acceleration due to gravity, m/s^2
L = 0.0065  # Temperature lapse rate, K/m
T0 = 288.15  # Standard temperature at sea level, K
P0 = 101325  # Standard pressure at sea level, Pa

def calculate_temperature(altitude):
    """
    Calculate the temperature at a given altitude using the standard atmosphere model.
    """
    return T0 - L * altitude

def calculate_pressure(altitude):
    """
    Calculate the pressure at a given altitude using the barometric formula.
    """
    temperature = calculate_temperature(altitude)
    return P0 * (1 - (L * altitude) / T0) ** (g / (R * L))

def calculate_air_density(altitude, humidity, barometric_pressure):
    """
    Calculate the air density at a given altitude, humidity, and barometric pressure.
    """
    temperature = calculate_temperature(altitude)
    pressure = calculate_pressure(altitude)
    
    # Adjust pressure for humidity
    # Assuming humidity is given as a percentage (e.g., 50 for 50%)
    vapor_pressure = humidity / 100 * 6.1078 * 10 ** ((7.5 * (temperature - 273.15)) / (temperature - 35.85))
    dry_air_pressure = barometric_pressure - vapor_pressure
    
    # Calculate air density using the ideal gas law
    air_density = dry_air_pressure / (R * temperature)
    return air_density

# Example usage
altitude = 1000  # Altitude in meters
humidity = 50  # Humidity in percentage
barometric_pressure = 101325  # Barometric pressure in Pascals

density = calculate_air_density(altitude, humidity, barometric_pressure)
print(f"Air density at {altitude} meters, {humidity}% humidity, and {barometric_pressure} Pa pressure is {density:.2f} kg/m^3")