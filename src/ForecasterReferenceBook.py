# =============================================================================
# Modules
# =============================================================================

# Third party modules
import numpy as np

# Custom modules
from custom_logger import get_custom_logger

# =============================================================================
# Variables
# =============================================================================

# Logging
logger = get_custom_logger("data/logging_config.yaml")

# Calculation constants
T_ABS = -273.15
NUMBER_COEFF = 3
MIN_WIND_SPEED = 0
MIN_CLOUD_COVER = 0

# =============================================================================
# Functions
# =============================================================================


def get_K_lookup(
    wind_speed: np.ndarray,
    min_wind: np.ndarray,
    max_wind: np.ndarray,
    cloud_cover: np.ndarray,
    min_cover: np.ndarray,
    max_cover: np.ndarray,
    K_values: np.ndarray,
):
    """Find the corresponding K values based on wind speed and cloud cover 
        within specified ranges

    Args:
        wind_speed (np.ndarray): wind speed to find K Value
        min_wind (np.ndarray): lower bound of wind range for K value interval
        max_wind (np.ndarray): upper bound of wind range for K value interval
        cloud_cover (np.ndarray): cloud cover to find K
        min_cover (np.ndarray): 
            lower bound of cloud cover range for K value interval
        max_cover (np.ndarray): 
            upper bound of cloud cover range for K value interval
        K_values (np.ndarray): 
            K values from which to choose appropriate K value

    Returns:
        np.ndarray: 
            K values for given wind and cloud cover inputs, len(wind_speed)
    """
    # Check if all K lookup values of table input arrays have the same length
    lengths = {len(arr) for arr in [min_wind, max_wind, min_cover, max_cover]}
    assert len(lengths) == 1, (
        "All K lookup table input arrays must have the same length\n"
        f"min_wind: {len(min_wind)} elements\n"
        f"max_wind: {len(max_wind)} elements\n"
        f"min_cover: {len(min_cover)} elements\n"
        f"max_cover: {len(max_cover)} elements"
    )
    # Check if wind speed and cloud cover arrays have the same length
    assert len(wind_speed) == len(cloud_cover), (
        "Wind speed and cloud cover arrays must have the same length\n"
        f"wind_speed: {len(wind_speed)} elements\n"
        f"cloud_cover: {len(cloud_cover)})elements"
    )
    # Check Wind speeds (knots), should be magnitudes and thus positive
    assert np.all(wind_speed >= MIN_WIND_SPEED), (
        "Wind speed (knots) should be a magnitude and non-negative\n"
        f"Wind speed: {wind_speed}"
    )
    # Check Cloud cover (oktas), should be non-negative otherwise non-physical
    assert np.all(cloud_cover >= MIN_CLOUD_COVER), (
        "Wind speed (knots) should be a magnitude and non-negative\n"
        f"cloud cover: {cloud_cover}"
    )
    # Check max wind speeds should always be greater than min wind speeds for 
    # K lookup table arrays
    assert np.all(max_wind >= min_wind), (
        "Max wind speed should be greater than Min wind speed in K lookup"
        " table arrays\n"
        f"Wind speed min. (knots) data: {min_wind}\n"
        f"Wind speed max. (knots) data: {max_wind}"
    )
    # Check max cloud cover should always be greater than min cloud cover for
    # K lookup table arrays
    assert np.all(max_cover >= min_cover), (
        "Max cloud cover should be greater than Min cloud cover in K lookup"
        " table arrays\n"
        f"Wind speed min. (knots) data: {min_cover}\n"
        f"Wind speed max. (knots) data: {max_cover}"
    )

    # Log function entry
    logger.info(
        f"Finding for K value given wind speed and cloud cover data..."
    )

    try:
        #Find indices of wind speed and cloud cover falls within min/max range
        matches = (
            (wind_speed[:, None] >= min_wind)
            & (wind_speed[:, None] <= max_wind)
            & (cloud_cover[:, None] >= min_cover)
            & (cloud_cover[:, None] <= max_cover)
        )
        indices = matches.argmax(axis=1)

        # Assign corresponding K values
        K = K_values[indices]
        logger.debug(f"K value found: {K}")
        logger.info(
            f"Found K value(s) for given wind speed and cloud cover data"
        )
        return K

    except ValueError as ve:
        logger.critical(
            f"ValueError: encountered while finding K values: {ve}"
        )
        raise

    except IndexError as ie:
        logger.critical(
            f"IndexError: encountered while processing indices: {ie}"
        )
        raise

    except Exception as e:
        logger.error(f"Error: unexpected error occurred: {e}")
        raise RuntimeError(
            f"RuntimeError: unexpected error occurred in get_K_lookup: {e}"
        ) from e


def calculate_temperature_min_noon_celcius(
    T_12: np.ndarray, 
    Td_12: np.ndarray, 
    K: np.ndarray, 
    coeff: list
):
    """Calculate the minimum temperature at noon (celcius) based on the given 
        parameters

    Args:
        T_12 (np.ndarray):  The temperature at noon
        Td_12 (np.ndarray): The dew point temperature at noon
        K (np.ndarray):  The K value used in the calculation
        coeff (list): 
            A list of three coefficients used in the linear calculation

    Returns:
        float: The calculated minimum temperature at noon
    """
    # Assert that T_12, Td_12, and K are NumPy arrays
    assert isinstance(T_12, np.ndarray), "T_12 must be a NumPy array"
    assert isinstance(Td_12, np.ndarray), "Td_12 must be a NumPy array"
    assert isinstance(K, np.ndarray), "K must be a NumPy array"
    # Assert that coeff is a list of NumPy arrays
    assert isinstance(coeff, list), "Coefficients must be a list"
    assert all(isinstance(c, np.ndarray) for c in coeff), (
        "All coefficients must be NumPy arrays"
    )
    # Check T_12 is a physical temperature
    assert np.all(T_12 > T_ABS), (
        f"Non-physical values in Temp. noon (celcius) data: {T_12}"
    )
    # Check Td_12 is a physical temperature
    assert np.all(Td_12 > T_ABS), (
        f"Non-physical values in Temp. dew point noon (celcius) data: {Td_12}"
    )
    # Check that the coefficients list contains exactly three values
    assert len(coeff) == NUMBER_COEFF, (
        "The coefficients list must contain exactly three values"
    )

    # Log function entry
    logger.info(f"Calculating minimum temperature at noon (celcius)...")

    try:
        # Perform the Forecasters Reference book temperature calculation
        Tmin_12 = coeff[0] * T_12 + coeff[1] * Td_12 + coeff[2] + K
        logger.debug(f"Min. temperature at noon: {Tmin_12}")
        logger.info(f"Calculated minimum temperature at noon (celcius)")
        return Tmin_12

    except ValueError as ve:
        logger.critical(f"ValueError: {ve}")
        raise

    except TypeError as te:
        logger.critical(f"TypeError: {te}")
        raise

    except Exception as e:
        logger.error(f"Error: unexpected error occurred: {e}")
        raise RuntimeError(
            "RuntimeError: unexpected error occurred in" \
            f" calculate_temperature_min_noon_celcius: {e}"
        ) from e
