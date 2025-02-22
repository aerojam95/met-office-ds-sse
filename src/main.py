#=============================================================================
# Programme: 
#=============================================================================

#=============================================================================
# Modules
#=============================================================================

# Python in built modules
import argparse
import logging
import os

# Third party modules
import pandas as pd
import yaml

# Custom modules
from custom_logger import get_logger
import DataImportExport as die
import ForecasterReferenceBook as frb

#=============================================================================
# Variables
#=============================================================================

# Logging
logger = get_logger("../data/logging_config.yaml")

#=============================================================================
# Programme exectuion
#=============================================================================

if __name__ == "__main__":
    
    #==========================================================================
    # Start programme
    #==========================================================================
    
    logger.info(f"Executing forecaster's referenece book method...")
    
    #==========================================================================
    # Argument parsing
    #==========================================================================
    
    parser = argparse.ArgumentParser(description="files for mph processing")
    parser.add_argument("-c", "--config_filepath", type=str, required=True, help="YAML configuration file")
    args = parser.parse_args()
    config_filepath = args.config_filepath
    
    #==========================================================================
    # Configuration imports
    #==========================================================================
    
    logger.info(f"importing configurations...")  
    config_data = die.read_yaml_configuration_file(config_filepath)
    k_lookup_file_path, data_file_path, precision, output_filepath = die.assign_configuration_data(config_data)
    logger.info(f"imported configurations")
    
    #==========================================================================
    # Method imports
    #==========================================================================
    
    # Read the lookup CSV data into relevant arrays
    logger.info(f"importing lookup data from {k_lookup_file_path}...")
    min_wind, max_wind, min_cover, max_cover, K_values = die.import_lookup_data(k_lookup_file_path)
    logger.info(f"imported method data from {k_lookup_file_path}")
    
    #==========================================================================
    # Data imports
    #==========================================================================
    
    logger.info(f"importing {data_file_path} to be processed...")
    
    # Read the CSV file into a DataFrame
    data_df = pd.read_csv(data_file_path)
    # Convert relevant columns to numeric, treating "NaN" properly
    data_df["Temp. noon (celcius)"] = pd.to_numeric(data_df["Temp. noon (celcius)"], errors="coerce")
    data_df["Temp. dew point noon (celius)"] = pd.to_numeric(data_df["Temp. dew point noon (celius)"], errors="coerce")
    data_df["wind speed (knots)"] = pd.to_numeric(data_df["wind speed (knots)"], errors="coerce")
    data_df["cloud cover (oktas)"] = pd.to_numeric(data_df["cloud cover (oktas)"], errors="coerce")
    # Initialise K values for each row
    data_df["K ()"] = 0
    
    logger.info(f"imported {data_file_path} to be processed")
    
    #==========================================================================
    # Method computations
    #==========================================================================
    
    logger.info(f"Computing forecaster's referenece book method...")
    
    # Convert the wind speeds and cloud cover columns to numpy arrays
    wind_speed = data_df["wind speed (knots)"].to_numpy().round()
    cloud_cover = data_df["cloud cover (oktas)"].to_numpy().round()
    
    # Find indices where wind speed and cloud cover falls within min/max range
    matches = (
        (wind_speed[:, None] >= min_wind) & (wind_speed[:, None] <= max_wind) &
        (cloud_cover[:, None] >= min_cover) & (cloud_cover[:, None] <= max_cover)
    )
    indices = matches.argmax(axis=1)
    
    # Assign corresponding K values
    data_df["K ()"] = K_values[indices]
    
    # Compute T min at 12 pm and create a new column in data DF
    data_df["Temp. min. noon (celcius)"] = data_df.apply(lambda row: 0.316 * row["Temp. noon (celcius)"] + 0.548 * row["Temp. dew point noon (celius)"] - 1.24 + row["K ()"], axis=1)
    data_df["Temp. min. noon (celcius)"] = data_df["Temp. min. noon (celcius)"].round(precision)
    
    logger.info(f"Computed  forecaster's referenece book method")
    
    #==========================================================================
    # Method outputs
    #==========================================================================
    
    logger.info(f"Writing outputs to {output_directory}{output_filename}...")
    
    # Check if file exists
    if os.path.exists(f"{output_directory}{output_filename}"):
        logger.info(f"The file {output_directory}{output_filename} already exists and will be overwritten")
        
    # Write DataFrame to CSV (will overwrite if file exists)
    data_df.to_csv(f"{output_directory}{output_filename}", index=False)
    
    logger.info(f"Written outputs to {output_directory}{output_filename}")
    
    #==========================================================================
    # End programme
    #==========================================================================
    
    logger.info(f"Executed forecaster's referenece book method")