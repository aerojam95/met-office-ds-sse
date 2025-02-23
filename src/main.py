#=============================================================================
# Programme: 
#=============================================================================

#=============================================================================
# Modules
#=============================================================================

# Python in built modules
import argparse

# Third party modules
import numpy as np

# Custom modules
from custom_logger import get_custom_logger
import DataImportExport as die
import ForecasterReferenceBook as frb

#=============================================================================
# Variables
#=============================================================================

# Logging
logger = get_custom_logger("../data/logging_config.yaml")
if not logger.name:
            logger.name = "forecasters_reference_book_logger"

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
    parser.add_argument("-c", "--config_file_path", type=str, required=True, help="YAML configuration file")
    args = parser.parse_args()
    config_file_path = args.config_file_path
    
    #==========================================================================
    # Configuration imports
    #==========================================================================
    
    logger.info(f"Importing configurations...")  
    config_data = die.import_yaml_configuration_file(yaml_configuration_file_path=config_file_path)
    logger.debug(f"Imported configuration data: {config_data}")
    logger.info(f"Imported configurations")
    
    #==========================================================================
    # .csv data imports
    #==========================================================================
    
    logger.info("Importing constants data...")
    imported_constants_data = die.import_csv_data_file(file=config_data["constants"]["constants_file_path"], columns=config_data["constants"]["constants_columns"])
    logger.debug(f"Imported constant data: {imported_constants_data}")
    logger.info("Imported constants data")
    
    logger.info("Importing lookup data...")
    imported_lookup_data = die.import_csv_data_file(file=config_data["k_lookup"]["k_lookup_file_path"], columns=config_data["k_lookup"]["k_lookup_columns"])
    logger.debug(f"Imported lookup data: {imported_lookup_data}")
    logger.info("Imported lookup data")
    
    logger.info("Importing data...")
    imported_data = die.import_csv_data_file(file=config_data["data"]["data_file_path"], columns=config_data["data"]["data_columns"])
    logger.debug(f"Imported data: {imported_data}")
    logger.info("Imported data")
    
    #==========================================================================
    # Data computation checks and preparation
    #==========================================================================
    
    logger.info("Validating imported data...")

    if any(imported_data["Temp. noon (celcius)"]) < -273.15:
        logger.debug(f"Temp. noon (celcius) data: {imported_data['Temp. noon (celcius)']}")
        logger.warning(f"Temp. noon (celcius) data contains non-physical temperatures")
    
    if any(imported_data["Temp. dew point noon (celius)"]) < -273.15:
        logger.debug(f"Temp. dew point noon (celius) data: {imported_data['Temp. dew point noon (celius)']}")
        logger.warning(f"Temp. dew point noon (celius) data contains non-physical temperatures")
        
    if any(imported_data["Wind speed (knots)"]) < 0.:
        logger.debug(f"Wind speed (knots) data: {imported_data['Wind speed (knots)']}")
        logger.warning(f"Wind speed (knots) should be a magnitude and non-negative")
        
    if any(imported_data["Cloud cover (oktas)"]) < 0.:
        logger.debug(f"Cloud cover (oktas) data: {imported_data['Cloud cover (oktas)']}")
        logger.warning(f"Cloud cover (oktas) should be non-negative otherwise non-physical")
        
    if any(imported_lookup_data["Wind speed max. (knots)"] < imported_lookup_data["Wind speed min. (knots)"]):
        logger.debug(f"Wind speed min. (knots) data: {imported_lookup_data['Wind speed min. (knots)']}\nWind speed max. (knots) data: {imported_lookup_data['Wind speed max. (knots)']}\n")
        msg = "Not all entries of lookup data have Wind speed max. (knots) > Wind speed min. (knots)!"
        logger.critical(msg=msg)
        raise ValueError(msg=msg)
    
    if any(imported_lookup_data["Cloud cover max. (oktas)"] < imported_lookup_data["Cloud cover min. (oktas)"]):
        logger.debug(f"Cloud cover min. (oktas) data: {imported_lookup_data['Cloud cover min. (oktas)']}\nCloud cover max. (oktas) data: {imported_lookup_data['Cloud cover max. (oktas)']}\n")
        msg = "Not all entries of lookup data have Cloud cover max. (oktas) > Cloud cover min. (oktas)!"
        logger.critical(msg=msg)
        raise ValueError(msg=msg)
    
    logger.info("Validated imported data")

    # Initialise K values for each row
    logger.info("Initialising K () array for imported data for Temp. min. noon (celcius) computations...")
    imported_data["K ()"] = np.zeros_like(imported_data["Temp. noon (celcius)"])
    logger.debug(f"Initialised K values: {imported_data['K ()']}")
    logger.info("Initialised K () array for imported data for Temp. min. noon (celcius) computations")
    
    # Round the wind speeds array for K lookup
    logger.info("Rounding wind speed (knots) array for imported data for K value lookup...")
    imported_data["Wind speed (knots)"] = imported_data["Wind speed (knots)"].round()
    logger.debug(f"Rounded wind speeds: {imported_data['Wind speed (knots)']}")
    logger.info("Rounded wind speed (knots) array for imported data for K value lookup")
    
    # Round the cloud cover array for K loohup
    logger.info("Rounding cloud cover (oktas) array for imported data for K value lookup...")
    imported_data["Cloud cover (oktas)"] = imported_data["Cloud cover (oktas)"].round()
    logger.debug(f"Rounded Cloud cover: {imported_data['Cloud cover (oktas)']}")
    logger.info("Round cloud cover (oktas) array for imported data for K value lookup")
    
    #==========================================================================
    # Computations
    #==========================================================================
    
    logger.info(f"Computing forecaster's referenece book method...")
    
    # Assign corresponding K values
    logger.info(f"Assigning K value for each data input for forecaster's referenece book method...")
    imported_data["K ()"] = frb.get_K_lookup(
        imported_data["Wind speed (knots)"],
        imported_lookup_data["Wind speed min. (knots)"],
        imported_lookup_data["Wind speed max. (knots)"],
        imported_data["Cloud cover (oktas)"],
        imported_lookup_data["Cloud cover min. (oktas)"],
        imported_lookup_data["Cloud cover max. (oktas)"],
        imported_lookup_data["K ()"]
        )
    logger.debug(f"Assigned K values: {imported_data['K ()']}")
    logger.info(f"Assigned K value for each data input for forecaster's referenece book method")
    
    # Compute T min at 12 pm and create a new column in data DF
    logger.info(f"Assigning K value for each data input for forecaster's referenece book method...")
    imported_data["Temp. min. noon (celcius)"] = frb.calculate_temperature_min_noon_celcius(imported_data["Temp. noon (celcius)"],
        imported_data["Temp. dew point noon (celius)"],
        imported_data["K ()"],
        coeff=[
            imported_constants_data["Temp. noon coeff (/celcius)"],
            imported_constants_data["Temp. dew point noon coeff (/celius)"],
            imported_constants_data["Temp. constant (celius)"]
            ]
        )
    logger.debug(f"Temp. min. noon (celcius): {imported_data['Temp. min. noon (celcius)']}")
    logger.info(f"Assigned K value for each data input for forecaster's referenece book method")
    
    logger.info(f"Computed  forecaster's referenece book method")
    
    #==========================================================================
    # Outputs
    #==========================================================================
    
    # Validate output columns and sizes
    logger.debug("Validating output dictionary...")
    if config_data["outputs"]["output_columns"] != list(imported_data.keys()):
        logger.debug(f"Data for export: {imported_data}")
        logger.debug(f"Expected columns for export: {config_data['outputs']['output_columns']}")
        logger.debug(f"Columns for export: {list(imported_data.keys())}")
        msg = "The columns of data ready for export do not match the expected data column output"
        logger.error(msg=msg)
        raise ValueError(msg=msg)
    logger.debug("Validated output dictionary")
    
    # Export computations and imported data
    logger.info(f"Writing outputs...")
    die.export_csv_data_file(config_data["outputs"]["output_file_path"], imported_data)
    logger.info(f"Written outputs")
    
    #==========================================================================
    # End programme
    #==========================================================================
    
    logger.info(f"Executed forecaster's referenece book method")