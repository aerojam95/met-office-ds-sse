# =============================================================================
# Modules
# =============================================================================

# Python modules
import logging
import os
import unittest

# Third party modules
import yaml

# Testing module
from custom_logger import get_custom_logger

# =============================================================================
# Tests
# =============================================================================


class TestGetCustomLogger(unittest.TestCase):

    def setUp(self: object):
        """Create a temporary YAML file for logging configuration"""
        self.test_yaml_file = "test_logging_config.yaml"
        self.logging_config = {
            "logging": {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "default": {
                        "format": 
                            "%(asctime)s - %(levelname)s - %(message)s",
                            "datefmt": "%Y-%m-%d %H:%M:%S"
                            }
                },
                "handlers": {
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": "INFO",
                        "formatter": "default",
                        "stream": "ext://sys.stdout",
                    }
                },
                "loggers": {
                    "test_logger": {
                        "level": "INFO",
                        "handlers": ["console"],
                        "propagate": False
                        }
                },
                "root": {"level": "INFO", "handlers": ["console"]},
            }
        }

        try:
            with open(self.test_yaml_file, "w") as file:
                yaml.dump(self.logging_config, file)
            self.assertTrue(
                os.path.exists(self.test_yaml_file),
                "YAML file was not created."
            )

        except yaml.YAMLError as ye:
            self.fail(
                "Error: There was an issue generating the test YAML " \
                f"configuration file: {ye}"
            )

        except Exception as e:
            self.fail(f"Failed to create test YAML file: {e}")

    def tearDown(self: object):
        """Remove the temporary YAML file after tests"""
        try:
            if os.path.exists(self.test_yaml_file):
                os.remove(self.test_yaml_file)
                self.assertFalse(
                    os.path.exists(self.test_yaml_file),
                    "YAML file was not deleted."
                )

        except Exception as e:
            self.fail(f"Failed to delete test YAML file: {e}")

    def test_logger_creation(self: object):
        """Test if the logger is created correctly from YAML configuration"""
        try:
            logger = get_custom_logger(self.test_yaml_file)

            # Check logger instance
            self.assertIsInstance(
                logger, logging.Logger,
                "Logger is not an instance of logging.Logger"
            )

            # Check logger name
            self.assertEqual(
                logger.name, 
                "test_logger",
                f"Expected logger name 'test_logger', but got {logger.name}"
            )

            # Check logger level
            self.assertEqual(
                logger.level,
                logging.INFO, 
                f"Expected logging level INFO, but got {logger.level}"
            )

            # Check logger handlers
            self.assertTrue(
                logger.handlers, 
                "Logger has no handlers configured."
            )
            handler_types = [type(handler).__name__ \
                for handler in logger.handlers]
            self.assertIn(
                "StreamHandler",
                handler_types,
                "Logger does not have a StreamHandler"
            )

            # Check if formatter is set correctly
            formatter = logger.handlers[0].formatter
            self.assertIsNotNone(
                formatter, 
                "Formatter is not set for the handler"
            )
            self.assertEqual(
                formatter._fmt,
                "%(asctime)s - %(levelname)s - %(message)s",
                "Incorrect log format"
            )

            # Check if logger propagation is correctly set
            self.assertFalse(
                logger.propagate,
                "Logger propagation is not set correctly"
            )

        except FileNotFoundError as fe:
            self.fail(f"Logger creation test failed due to missing file: {fe}")

        except yaml.YAMLError as ye:
            self.fail(
                "Logger creation test failed due to YAML parsing error: {ye}"
            )

        except ValueError as ve:
            self.fail(f"Logger creation test failed due to ValueError: {ve}")

        except Exception as e:
            self.fail(
                "Logger creation test failed due to an  unexpected error: {e}"
            )


# =============================================================================
# Test execution
# =============================================================================

if __name__ == "__main__":
    unittest.main()
