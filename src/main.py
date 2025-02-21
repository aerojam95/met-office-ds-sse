#=============================================================================
# Programme: 
#=============================================================================

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
# Imports
#=============================================================================

#=============================================================================
# Variables
#=============================================================================

# Configuration file path
configuration_file_path = "../data/forecasters_reference_book_config.yaml"

# logging variables
logging_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
log_file_path  = "../outputs/forecasters_reference_book.log"
logger_name    = "forecasters_reference_book_logger"

# Check log file exists
if not os.path.exists(log_file_path):
     raise FileNotFoundError(f"The log file {log_file_path} does not exist")

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format=f"{logging_format}",
                    handlers=[
                        logging.FileHandler(f"{log_file_path}"),
                        logging.StreamHandler()
                    ])

# Create logger
logger = logging.getLogger(f"{logger_name}")


#=============================================================================
# Programme exectuion
#=============================================================================

if __name__ == "__main__":
    
    #==========================================================================
    # Start programme
    #==========================================================================
    
    logger.info(f"Executing forecaster's referenece book method...")
    
    #==========================================================================
    # Configuration imports
    #==========================================================================
    
    logger.info(f"importing configurations...")
    
    # Extract configurations    
    with open(configuration_file_path, "r") as file:
        configuration_data = yaml.safe_load(file)
    k_lookup_file_path = configuration_data["method_data"]["k_lookup_file_path"]
    data_file_path     = configuration_data["data"]["data_file_path"]
    precision          = configuration_data["outputs"]["decimal_place_precision"]
    output_filename    = configuration_data["outputs"]["output_filename"]
    output_directory   = configuration_data["outputs"]["output_directory"]
    
    logger.info(f"imported configurations")
    
    #==========================================================================
    # Method imports
    #==========================================================================
    
    logger.info(f"importing method data from {k_lookup_file_path}...")
    
    # Read the CSV file into a DataFrame
    k_lookup_df = pd.read_csv(k_lookup_file_path)

    # Convert relevant columns to numeric, treating "NaN" properly
    k_lookup_df["wind speed min. (knots)"] = pd.to_numeric(k_lookup_df["wind speed min. (knots)"], errors="coerce")
    k_lookup_df["wind speed max. (knots)"] = pd.to_numeric(k_lookup_df["wind speed max. (knots)"], errors="coerce")
    k_lookup_df["cloud cover min. (oktas)"] = pd.to_numeric(k_lookup_df["cloud cover min. (oktas)"], errors="coerce")
    k_lookup_df["cloud cover max. (oktas)"] = pd.to_numeric(k_lookup_df["cloud cover max. (oktas)"], errors="coerce")
    k_lookup_df["K ()"] = pd.to_numeric(k_lookup_df["K ()"], errors="coerce")
        
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
    min_wind   = k_lookup_df["wind speed min. (knots)"].to_numpy()
    max_wind   = k_lookup_df["wind speed max. (knots)"].to_numpy()
    min_cover  = k_lookup_df["cloud cover min. (oktas)"].to_numpy()
    max_cover  = k_lookup_df["cloud cover max. (oktas)"].to_numpy()
    K_values   = k_lookup_df["K ()"].to_numpy()
    
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