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
# Functions
#=============================================================================

def get_logger(filepath:str, logger:str, mode:str = "info",
               format:str = 
               "%(asctime)s - %(name)s - %(levelname)s - %(message)s"):
    
    return 0
    

#=============================================================================
# CLasses
#=============================================================================