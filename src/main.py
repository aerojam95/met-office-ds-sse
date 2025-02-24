# =============================================================================
# Modules
# =============================================================================

# Python in built modules
import argparse

# Third party modules
import numpy as np

# Custom modules
from custom_logger import get_custom_logger
import DataImportExport as die
import ForecasterReferenceBook as frb

# =============================================================================
# Variables
# =============================================================================

# Logging
logger = get_custom_logger("data/logging_config.yaml")

# =============================================================================
# Programme exectuion
# =============================================================================

if __name__ == "__main__":

    # =========================================================================
    # Argument parsing
    # =========================================================================

    parser = argparse.ArgumentParser(description="files for mph processing")
    parser.add_argument("-c", "--config_file_path", type=str, required=True,
        help="YAML configuration file")
    args = parser.parse_args()
    config_file_path = args.config_file_path

    # =========================================================================
    # Programme
    # =========================================================================

    logger.info(f"Executing forecaster's referenece book method...")

    # Import configuration data
    config_data = die.import_yaml_configuration_file(config_file_path)

    # Import constants, K lookup, and raw data
    imported_constants_data = die.import_csv_data_file(
        config_data["constants"]["constants_file_path"], 
        config_data["constants"]["constants_columns"]
    )
    imported_lookup_data = die.import_csv_data_file(
        config_data["k_lookup"]["k_lookup_file_path"], 
        config_data["k_lookup"]["k_lookup_columns"]
    )
    imported_data = die.import_csv_data_file(
        config_data["data"]["data_file_path"], 
        config_data["data"]["data_columns"]
    )

    # Initialise K values to predict
    logger.info(
        "Initialising K () array for imported data for" \
        " Temp. min. noon (celcius) computations..."
    )
    imported_data["K ()"] = np.zeros_like(imported_data["Temp. noon (celcius)"])
    logger.debug(f"Initialised K values: {imported_data['K ()']}")
    logger.info(
        "Initialised K () array for imported data for" \
        " Temp. min. noon (celcius) computations"
    )

    # Round the wind speeds array for K lookup
    logger.info(
        "Rounding wind speed (knots) array for imported data for" \
        " K value lookup..."
    )
    imported_data["Wind speed (knots)"] = imported_data["Wind speed (knots)"].round()
    logger.debug(f"Rounded wind speeds: {imported_data['Wind speed (knots)']}")
    logger.info(
        "Rounded wind speed (knots) array for imported data for" \
        " K value lookup"
    )

    # Round the cloud cover array for K loohup
    logger.info(
        "Rounding cloud cover (oktas) array for imported data for" \
        " K value lookup..."
    )
    imported_data["Cloud cover (oktas)"] = imported_data["Cloud cover (oktas)"].round()
    logger.debug(f"Rounded cloud cover: {imported_data['Cloud cover (oktas)']}")
    logger.info(
        "Round cloud cover (oktas) array for imported data for" \
        " K value lookup"
    )

    # K lookup values to predict
    imported_data["K ()"] = frb.get_K_lookup(
        imported_data["Wind speed (knots)"],
        imported_lookup_data["Wind speed min. (knots)"],
        imported_lookup_data["Wind speed max. (knots)"],
        imported_data["Cloud cover (oktas)"],
        imported_lookup_data["Cloud cover min. (oktas)"],
        imported_lookup_data["Cloud cover max. (oktas)"],
        imported_lookup_data["K ()"],
    )

    # Calculate T min at noon
    imported_data["Temp. min. noon (celcius)"] = frb.calculate_temperature_min_noon_celcius(
        imported_data["Temp. noon (celcius)"],
        imported_data["Temp. dew point noon (celcius)"],
        imported_data["K ()"],
        coeff=[
            imported_constants_data["Temp. noon coeff (/celcius)"],
            imported_constants_data["Temp. dew point noon coeff (/celcius)"],
            imported_constants_data["Temp. constant (celcius)"],
        ],
    )

    # Export computations and imported data
    die.export_csv_data_file(
        config_data["outputs"]["output_file_path"],
        list(imported_data.keys()), imported_data
    )

    logger.info(f"Executed forecaster's referenece book method")
