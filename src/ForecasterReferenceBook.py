#=============================================================================
# Modules
#=============================================================================

# Third party modules
import numpy as np

# Custom modules
from custom_logger import get_custom_logger

#=============================================================================
# Variables
#=============================================================================

# Logging
logger = get_custom_logger("../data/logging_config.yaml")

#=============================================================================
# Functions
#=============================================================================

def get_K_lookup(wind_speed:np.ndarray, min_wind:np.ndarray, max_wind:np.ndarray,cloud_cover:np.ndarray, min_cover:np.ndarray, max_cover:np.ndarray, K_values:np.ndarray):
    """Find the corresponding K values based on wind speed and cloud cover within specified ranges

    Args:
        wind_speed (np.ndarray): wind speed to find K Value
        min_wind (np.ndarray): lower bound of wind range for K value interval
        max_wind (np.ndarray): upper bound of wind range for K value interval
        cloud_cover (np.ndarray): cloud cover to find K
        min_cover (np.ndarray): lower bound of cloud cover range for K value interval
        max_cover (np.ndarray): upper bound of cloud cover range for K value interval
        K_values (np.ndarray): K values from which to choose appropriate K value

    Returns:
        np.ndarray: K values for give wind and cloud cover input
    """
    try:
        # Check if the input arrays have the same length
        if not all(len(arr) for arr in [min_wind, max_wind, min_cover, max_cover]):
            raise ValueError("All input arrays must have the same length")
        
        # Find indices where wind speed and cloud cover falls within min/max range
        matches = (
            (wind_speed[:, None] >= min_wind) & (wind_speed[:, None] <= max_wind) &
            (cloud_cover[:, None] >= min_cover) & (cloud_cover[:, None] <= max_cover)
        )
        indices = matches.argmax(axis=1)
        
        # Assign corresponding K values
        return K_values[indices]
    
    except ValueError as ve:
        msg = f"ValueError: {ve}!"
        logger.critical(msg)
        raise ValueError(msg) from ve
    
    except IndexError as ie:
        msg = f"IndexError: {ie}!"
        logger.critical(msg)
        raise ValueError(msg) from ie
    
    except Exception as e:
        msg = f"An unexpected error occurred in calculate_temperature_min_noon_celcius: {e}"
        logger.critical(msg)
        raise Exception(msg) from e
    
def calculate_temperature_min_noon_celcius(T_12:float, Td_12:float, K:float, coeff:list):
    """Calculate the minimum temperature at noon (in Celsius) based on the given parameters

    Args:
        T_12 (float):  The temperature at noon
        Td_12 (float): The dew point temperature at noon
        K (float):  The K value used in the calculation
        coeff (list): A list of three coefficients used in the linear calculation

    Returns:
        float: The calculated minimum temperature at noon
    """
    try:
        # Validate coefficients list length
        if len(coeff) != 3:
            raise ValueError("The coefficients list must contain exactly three values")
        
        # Validate input types
        if not isinstance(T_12, np.ndarray) or not isinstance(Td_12, np.ndarray) or not isinstance(K, np.ndarray):
            raise TypeError("T_12, Td_12, and K must be NumPy arrays")
        
        if not isinstance(coeff, list) or not all(isinstance(c, np.ndarray) for c in coeff):
            raise TypeError("Coefficients must be a list of NumPy arrays")

        # Perform the temperature calculation
        return coeff[0] * T_12 + coeff[1] * Td_12 + coeff[2] + K
    
    except ValueError as ve:
        msg = f"ValueError: {ve}!"
        logger.critical(msg)
        raise ValueError(msg) from ve
    
    except TypeError as te:
        msg = f"TypeError: {te}!"
        logger.critical(msg)
        raise TypeError(msg) from te
    
    except Exception as e:
        msg = f"An unexpected error occurred in calculate_temperature_min_noon_celcius: {e}"
        logger.critical(msg)
        raise Exception(msg) from e