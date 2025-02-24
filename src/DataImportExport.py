# =============================================================================
# Modules
# =============================================================================

# Python in built modules
import os

# Third party modules
import pandas as pd
import yaml

# Custom modules
from custom_logger import get_custom_logger

# =============================================================================
# Variables
# =============================================================================

# Logging
logger = get_custom_logger("data/logging_config.yaml")

# =============================================================================
# Functions
# =============================================================================


def import_yaml_configuration_file(yaml_configuration_file_path: str):
    """import data in yaml file into configuration data dictonary

    Args:
        yaml_configuration_file_path (str): 
            file path to yaml configuration file

    Returns:
        dict: dictonary of configuration data

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If there's an error parsing the YAML file.
    """
    # Log function entry
    logger.info(
        f"Reading YAML configuration from {yaml_configuration_file_path}..."
    )

    try:
        # load configuration data from YAML file
        with open(yaml_configuration_file_path, "r") as file:
            config_data = yaml.safe_load(file)
        logger.debug(f"Imported YAML configuration data: {config_data}")
        logger.info(
            f"Read YAML configuration from {yaml_configuration_file_path}"
        )
        return config_data

    except FileNotFoundError as fe:
        logger.critical(
            "FileNotFoundError: the YAML configuration file" \
            f" {yaml_configuration_file_path} does not exist: {fe}"
        )
        raise

    except yaml.YAMLError as ye:
        logger.critical(
            "YAMLError: there was an issue parsing the YAML configuration" \
            f" file {yaml_configuration_file_path}: {ye}"
        )
        raise

    except Exception as e:
        logger.critical(f"Error: unexpected error occurred: {e}")
        raise RuntimeError(
                "RuntimeError: unexpected error occurred in" \
                f" import_yaml_configuration_file: {e}"
            ) from e


def import_csv_data_file(file: str, columns: list):
    """Returns columns from .csv file selected as a dictionary of the data

    Args:
        file (str): file path for relevant .csv file to import data from
        columns (list): 
            list of columns names contained in relevant .csv file to import

    Returns:
        dict: 
        Dictionary where keys are column names and values are NumPy arrays

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file contains missing values
        KeyError: If any specified column is not found in the .csv
    """
    # Log function entry
    logger.info(f"Importing data from {file}...")

    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file)
        # Remove rows with any NaNs in import
        df = df.dropna()

        # Ensure all specified columns exist
        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            raise KeyError(f"Missing columns in .csv file: {missing_columns}")

        # Initialise dictionary to store imported data
        imported_data = {}
        # Convert relevant columns to numeric and store them in the dictionary
        for col in columns:
            numeric_data = pd.to_numeric(df[col], errors="coerce")
            # Check if numeric conversion introduced NaN values
            if numeric_data.isnull().values.any():
                raise ValueError(
                        f"Column {col} contains non-numeric values" \
                        " that could not be converted"
                    )
            imported_data[col] = numeric_data.to_numpy()

        logger.debug(f"Imported data from {file}: {imported_data}")
        logger.info(f"Imported data from {file}")
        return imported_data

    except FileNotFoundError as fe:
        logger.critical(
            f"FileNotFoundError: the .csv {file} does not exist: {fe}"
        )
        raise

    except KeyError as ke:
        logger.critical(f"KeyError: {ke}")
        raise

    except ValueError as ve:
        logger.critical(
            f"ValueError: Column {col} contains non-numeric" \
            f" values that could not be converted: {ve}"
        )
        raise

    except Exception as e:
        logger.error(f"Error: unexpected error occurred: {e}")
        raise RuntimeError(
            f"RuntimeError: unexpected error occurred in" \
            f" import_csv_data_file: {e}"
        ) from e


def export_csv_data_file(file: str, columns: list, export_data: dict):
    """Exports data in a dictionary to a .csv file

    Args:
        file (str): file path for relevant .csv file to import data from
        columns (list): columns that will be exported to .csv file
        export_data (dict): 
            dictionary of keys as columns for .csv and values of data to be
            printed to .csv file
    Raises:
        PermissionError: 
            incorrect permission to access file to create/overwrite
    """
    # Check columns to be exported are the same as the expected columns
    assert sorted(columns) == sorted(export_data.keys()), (
        f"Expected columns for export: {columns}\nColumns for export: " \
        "{list(export_data.keys())}"
    )

    # Check data is not empty before exporting
    assert export_data, "DataFrame is empty, cannot export."

    # Log function entry
    logger.info(f"Exporting data to {file}...")

    try:
        # Write data to file, overwrite if it exists
        if os.path.exists(file):
            logger.warning(
                f"The .csv file {file} already exists and will be overwritten"
            )
        output_df = pd.DataFrame(export_data)
        output_df.to_csv(file, index=False)
        logger.info(f"Exported data to {file}")

    except PermissionError as pe:
        logger.critical(
            f"PermissionError: permission denied when accessing the file: {pe}"
        )
        raise

    except Exception as e:
        logger.error(f"Error: unexpected error occurred: {e}")
        raise RuntimeError(
            f"RuntimeError: unexpected error occurred in" \
            f" export_csv_data_file: {e}"
        ) from e
