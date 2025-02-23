#=============================================================================
# Modules
#=============================================================================

# Python in built modules
import os

# Third party modules
import pandas as pd
import yaml

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

def import_yaml_configuration_file(yaml_configuration_file_path:str):
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
                config_data = yaml.safe_load(file)
            logger.info(f"Read configuration from {yaml_configuration_file_path}")
            return config_data
    except FileNotFoundError as fe:
        msg = f"FileNotFoundError: the YAML configuration file {yaml_configuration_file_path} does not exist: {fe}!"
        logger.critical(msg)
        raise FileNotFoundError(msg) from fe
    except yaml.YAMLError as ye:
        msg = f"YAMLError: there was an issue parsing the YAML configuration file {yaml_configuration_file_path}: {ye}!"
        logger.critical(msg)
        raise yaml.YAMLError(msg) from ye
    except Exception as e:
        msg = f"Error: unexpected error occurred: {e}!"
        logger.critical(msg)
        raise Exception(msg) from e
    
def import_csv_data_file(file:str, columns:list):
    """Returns columns from .csv file selected as a dictionary of the data
    
    Args:
        file (str): file path for relevant .csv file to import data from
        columns (list): list of columns names contained in relevant .csv file to import data from

    Returns:
        dict: dictionary of converted columns for each column from parsed .csv file   
    """
    # Dictionary to store imported data
    imported_data = {}
    # Log function entry
    logger.info(f"Importing data from {file}...")
    try:
        if os.path.exists(file):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file)
            # Check for missing data
            if (df == "").values.any():  # Check if any value empty values
                raise ValueError("The CSV file contains missing values")
            # Convert relevant columns to numeric and store them in the dictionary
            for col in columns:
                imported_data[col] = pd.to_numeric(df[col], errors="coerce").to_numpy()
            logger.info(f"Imported  data from {file}")
            return imported_data
    except FileNotFoundError as fe:
        msg = f"FileNotFoundError: the {file} does not exist: {fe}!"
        logger.critical(msg)
        raise FileNotFoundError(msg) from fe
    except ValueError as ve:
        msg = f"ValueError: The CSV file contains missing values : {ve}!"
        logger.critical(msg)
        raise ValueError(msg) from ve
    except Exception as e:
        msg = f"Error: unexpected error occurred: {e}!"
        logger.critical(msg)
        raise Exception(msg) from e

def export_csv_data_file(file:str, export_data:dict):
    """Exports data in a dictionary to a .csv file
    
    Args:
        file (str): file path for relevant .csv file to import data from
        export_data (dict): dictionary of keys as columns for .csv and values
                            of data to be printed to .csv file
    """
    # Check if file exists
    logger.info(f"Exporting data to {file}...")
    try:
        if os.path.exists(file):
            logger.warning(f"The file {file} already exists and will be overwritten")
        output_df = pd.DataFrame(export_data)
        output_df.to_csv(file, index=False)
        logger.info(f"Exported data to {file}")
    except Exception as e:
        msg = f"Error: unexpected error occurred: {e}!"
        logger.critical(msg)
        raise Exception(msg) from e