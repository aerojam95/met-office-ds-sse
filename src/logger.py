#=============================================================================
# Modules
#=============================================================================

# Python in built modules
import logging.config

# Third party modules
import yaml

#=============================================================================
# Functions
#=============================================================================

def get_logger(yaml_config_file_path:str):
    """Set up logger based on configuration from a YAML file

    Args:
        yaml_config_file_path (str): The path to the YAML file containing the
        logging configuration

    Returns:
        logging.Logger: Configured logger instance
    """
    try:
        # Load logging configuration from YAML file
        with open(yaml_config_file_path, "r") as file:
            config = yaml.safe_load(file)
        
        # Apply the logging configuration
        logging.config.dictConfig(config["logging"])
        
        # Dynamically get the logger's name from YAML configuration
        logger_name = config["logging"]["loggers"].get("logger_name",
            "default_logger")
        
        # Use the logger name dynamically
        logger = logging.getLogger(logger_name)
        return logger
    
    except FileNotFoundError as e:
        print(f"Error: The logging configuration file was not found: {e}")
        raise

    except yaml.YAMLError as e:
        print(f"Error: There was an issue parsing the YAML configuration
            file: {e}")
        raise

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        raise