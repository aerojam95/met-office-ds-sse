#=============================================================================
# Modules
#=============================================================================

# Python in built modules
import os

# Third party modules
import pandas as pd
import yaml

# Custom modules
from custom_logger import get_logger

#=============================================================================
# Variables
#=============================================================================

# Logging
logger = get_logger("../data/logging_config.yaml")

#=============================================================================
# Functions
#=============================================================================

def read_yaml_configuration_file(yaml_configuration_file_path:str):
    """import data in yaml file into configuration data dictonary

    Args:
        yaml_configuration_file_path (str): file path to yaml configuration 
        file

    Returns:
        dict: dictonary of configuration data
    """
    # Log function entry
    logger.info(f"Reading configuration from {yaml_configuration_file_path}...")
    
    # Check log file exists
    try:
        if os.path.exists(yaml_configuration_file_path):
            with open(yaml_configuration_file_path, "r") as file:
                configuration_data = yaml.safe_load(file)
            logger.info("Read configuration from {yaml_configuration_file_path}")
            return configuration_data
    except FileNotFoundError as e:
        message = f"The YAML configuration file {yaml_configuration_file_path} does not exist!"
        logger.critical(message)
        raise FileNotFoundError(message) from e
    except yaml.YAMLError as e:
        message = f"There was an issue parsing the YAML configuration file {yaml_configuration_file_path}: {e}"
        logger.critical(message)
        raise yaml.YAMLError(message) from e
    
def assign_configuration_data(configuration_data:dict):
    """Assigns variables to configuration data stored in parsed dictionary

    Args:
        configuration_data (dict): dictionary formatted for config data

    Returns:
        str, str, int, str: file path for lookup data, 
                            file path for data to be processed,
                            precision for comuted outputs,
                            file path for computation outputs  
    """
    # Log function entry
    logger.info("Assigning configuration variables...")
    try:
        k_lookup_file_path = configuration_data["method_data"]["k_lookup_file_path"]
        data_file_path     = configuration_data["data"]["data_file_path"]
        precision          = configuration_data["outputs"]["decimal_place_precision"]
        output_filepath    = configuration_data["outputs"]["output_filepath"]
        logger.info("Assigned configuration variables")
        return k_lookup_file_path, data_file_path, precision, output_filepath
    except KeyError as e:
        message = f"Configuration data is not formatted correctly for processing!"
        logger.critical(message)
        raise KeyError(message) from e
    
def import_lookup_data(k_lookup_file_path:str):
    """Returns 5 columns from .csv lookup file parsed from the argument as 5
    numpy arrays
    
    Args:
        k_lookup_file_path (str): file path to lookup value .csv file

    Returns:
        np.array, np.array, np.array, np.array, np.array: returns five columns
            of data stored in lookup value .csv file as np.arrays
    """
    # Log function entry
    logger.info("Importing lookup value data...")
    try:
        if os.path.exists(k_lookup_file_path):
            # Read the CSV file into a DataFrame
            k_lookup_df = pd.read_csv(k_lookup_file_path)
            # Convert relevant columns to numeric, treating "NaN" properly and convert to numpy arrays
            min_wind  = pd.to_numeric(k_lookup_df["wind speed min. (knots)"], errors="coerce").to_numpy()
            max_wind  = pd.to_numeric(k_lookup_df["wind speed max. (knots)"], errors="coerce").to_numpy()
            min_cover = pd.to_numeric(k_lookup_df["cloud cover min. (oktas)"], errors="coerce").to_numpy()
            max_cover = pd.to_numeric(k_lookup_df["cloud cover max. (oktas)"], errors="coerce").to_numpy()
            K_values  = pd.to_numeric(k_lookup_df["K ()"], errors="coerce").to_numpy()
            logger.info("IMported lookup value data")
            return min_wind, max_wind, min_cover, max_cover, K_values
    except FileNotFoundError as e:
        message = f"The lookup data .csv file {k_lookup_file_path} does not exist!"
        logger.critical(message)
        raise FileNotFoundError(message) from e    

#=============================================================================
# Classes
#=============================================================================