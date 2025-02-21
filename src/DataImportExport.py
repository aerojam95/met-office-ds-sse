#=============================================================================
# Modules
#=============================================================================

# Python in built modules
import logging
import os

# Third party modules
import pandas as pd
import yaml

#=============================================================================
# Variables
#=============================================================================


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
    logger.info(f"Attempting to read configuration from {yaml_configuration_file_path}")
    # Check log file exists
    if not os.path.exists(yaml_configuration_file_path):
        raise FileNotFoundError(
            f"The log file {yaml_configuration_file_path} does not exist")
    with open(yaml_configuration_file_path, "r") as file:
        configuration_data = yaml.safe_load(file)
    return configuration_data

# Extract configurations    
    with open(configuration_file_path, "r") as file:
        configuration_data = yaml.safe_load(file)
    k_lookup_file_path = configuration_data["method_data"]["k_lookup_file_path"]
    data_file_path     = configuration_data["data"]["data_file_path"]
    precision          = configuration_data["outputs"]["decimal_place_precision"]
    output_filename    = configuration_data["outputs"]["output_filename"]
    output_directory   = configuration_data["outputs"]["output_directory"]
    

#=============================================================================
# Classes
#=============================================================================