# =============================================================================
# Modules
# =============================================================================

# Python modules
import os
import unittest

# Third party modules
import numpy as np
import pandas as pd
import yaml

# Testing module
import DataImportExport as die

# =============================================================================
# Tests
# =============================================================================


class TestImportYamlConfigurationFile(unittest.TestCase):

    def setUp(self: object):
        """Create a temporary YAML files for testing"""
        self.valid_yaml_path = "test_valid_config.yaml"
        self.invalid_yaml_path = "test_invalid_config.yaml"
        self.nonexistent_yaml_path = "test_nonexistent_config.yaml"

        # Create a valid YAML file
        with open(self.valid_yaml_path, "w") as f:
            yaml.dump({"key": "value"}, f)

        # Create an invalid YAML file (malformed YAML)
        with open(self.invalid_yaml_path, "w") as f:
            # This will cause a YAML parsing error
            f.write("key: value: invalid")

    def tearDown(self: object):
        """Remove the temporary YAML file after tests"""
        try:
            if os.path.exists(self.valid_yaml_path):
                os.remove(self.valid_yaml_path)
            if os.path.exists(self.invalid_yaml_path):
                os.remove(self.invalid_yaml_path)
            if os.path.exists(self.nonexistent_yaml_path):
                os.remove(self.nonexistent_yaml_path)

        except Exception as e:
            self.fail(f"Failed to delete test YAML files: {e}")

    def test_import_yaml_configuration_file_success(self: object):
        """Test importing a valid YAML file"""
        config_data = die.import_yaml_configuration_file(self.valid_yaml_path)
        self.assertEqual(config_data, {"key": "value"})

    def test_import_yaml_configuration_file_file_not_found(self: object):
        """Test FileNotFoundError when the YAML file doesn't exist"""
        with self.assertRaises(FileNotFoundError):
            die.import_yaml_configuration_file(self.nonexistent_yaml_path)

    def test_import_yaml_configuration_file_yaml_error(self: object):
        """Test that a YAML parsing error is raised"""
        with self.assertRaises(yaml.YAMLError):
            die.import_yaml_configuration_file(self.invalid_yaml_path)


class TestImportCsvDataFile(unittest.TestCase):

    def setUp(self):
        """Set up temporary CSV test files"""
        self.valid_csv = "test_valid.csv"
        self.missing_values_csv = "test_missing_values.csv"
        self.missing_columns_csv = "test_missing_columns.csv"
        self.non_numeric_csv = "test_non_numeric.csv"
        self.non_existent_csv = "test_non_existent.csv"

        # Create a valid CSV file
        df_valid = pd.DataFrame(
            {
                "A": [1.0, 2.0, 3.0],
                "B": [4.0, 5.0, 6.0],
                "C": [7.0, 8.0, 9.0]
            }
            )
        df_valid.to_csv(self.valid_csv, index=False)

        # Create a CSV file with missing values
        df_missing_values = pd.DataFrame(
            {
                "A": [1.0, 2.0, "2.0"],
                "B": [4.0, "2.0", 6.0],
                "C": [7.0, 8.0, 9.0]
             }
        )
        df_missing_values.to_csv(self.missing_values_csv, index=False)

        # Create a CSV file missing required columns
        df_missing_columns = pd.DataFrame(
            {
                "X": [10, 20, 30],
                "Y": [40, 50, 60]
            }
        )
        df_missing_columns.to_csv(self.missing_columns_csv, index=False)

        # Create a CSV file with non-numeric values
        df_non_numeric = pd.DataFrame(
            {
                "A": [1.0, 2.0, "error"],
                "B": [4.0, 5.0, 6.0]
            }
        )
        df_non_numeric.to_csv(self.non_numeric_csv, index=False)

    def tearDown(self):
        """Remove temporary CSV test files"""
        try:
            for file in [
                self.valid_csv,
                self.missing_values_csv,
                self.missing_columns_csv,
                self.non_numeric_csv,
            ]:
                if os.path.exists(file):
                    os.remove(file)

        except Exception as e:
            self.fail(f"Failed to delete test .csv file: {e}")

    def test_import_valid_csv(self):
        """Test importing a valid CSV file"""
        columns = ["A", "B", "C"]
        result = die.import_csv_data_file(self.valid_csv, columns)
        expected = {
                    "A": np.array([1.0, 2.0, 3.0]),
                    "B": np.array([4.0, 5.0, 6.0]),
                    "C": np.array([7.0, 8.0, 9.0])
                    }
        for col in columns:
            np.testing.assert_array_equal(result[col], expected[col])

    def test_import_csv_missing_columns(self):
        """Test that a KeyError is raised if required columns are missing"""
        columns = ["A", "B", "C"]
        with self.assertRaises(KeyError):
            die.import_csv_data_file(self.missing_columns_csv, columns)

    def test_import_csv_with_non_numeric_values(self):
        """Test that a ValueError is raised for non-numeric data"""
        columns = ["A", "B"]
        with self.assertRaises(ValueError):
            die.import_csv_data_file(self.non_numeric_csv, columns)

    def test_import_non_existent_csv(self):
        """Test that a FileNotFoundError is raised for missing files"""
        columns = ["A", "B"]
        with self.assertRaises(FileNotFoundError):
            die.import_csv_data_file(self.non_existent_csv, columns)


class TestExportCsvDataFile(unittest.TestCase):

    def setUp(self):
        """Set up temporary file paths"""
        self.valid_csv = "test_valid_export.csv"
        self.permission_denied_csv = "test_no_permission_export.csv"
        self.mismatched_columns_csv = "test_mismatched_columns_export.csv"
        self.empty_data_csv = "test_empty_data_export.csv"

        # Create a valid dictionary for exporting
        self.valid_columns = ["A", "B", "C"]
        self.valid_data = {
                        "A": np.array([1.0, 2.0, 3.0]),
                        "B": np.array([4.0, 5.0, 6.0]),
                        "C": np.array([7.0, 8.0, 9.0])
                        }

        # Create an empty dictionary (to test empty data)
        self.empty_data = {}

        # Ensure test files do not exist beforehand
        try:
            for file in [
                self.valid_csv, 
                self.permission_denied_csv, 
                self.mismatched_columns_csv, 
                self.empty_data_csv
            ]:
                if os.path.exists(file):
                    os.remove(file)

        except Exception as e:
            self.fail(f"Failed to delete a pre-exisitng test .csv file: {e}")

    def tearDown(self):
        """Remove temporary CSV test files"""
        try:
            for file in [
                self.valid_csv,
                self.permission_denied_csv,
                self.mismatched_columns_csv,
                self.empty_data_csv
            ]:
                if os.path.exists(file):
                    os.remove(file)

        except Exception as e:
            self.fail(f"Failed to delete test .csv file: {e}")

    def test_export_valid_csv(self):
        """Test successfully exporting data to a CSV file"""
        die.export_csv_data_file(
            self.valid_csv, 
            self.valid_columns,
            self.valid_data
        )

        # Read the exported file to verify correctness
        df = pd.read_csv(self.valid_csv)
        expected_df = pd.DataFrame(self.valid_data)

        pd.testing.assert_frame_equal(df, expected_df)

    def test_export_csv_mismatched_columns(self):
        """Test that an assertion error is raised for mismatched columns"""
        mismatched_columns = ["X", "Y", "Z"]
        with self.assertRaises(AssertionError):
            die.export_csv_data_file(
                self.mismatched_columns_csv, 
                mismatched_columns, 
                self.valid_data
            )

    def test_export_csv_empty_data(self):
        """Test that an EmptyDataError is raised when exporting empty data"""
        with self.assertRaises(AssertionError):
            die.export_csv_data_file(self.empty_data_csv, [], self.empty_data)

    def test_export_csv_permission_error(self):
        """Test a PermissionError is raised when file permission is denied"""
        # Create a file and make it read-only
        with open(self.permission_denied_csv, "w") as f:
            f.write("This file is read-only")
        os.chmod(self.permission_denied_csv, 0o444)  # Read-only permissions

        with self.assertRaises(PermissionError):
            die.export_csv_data_file(
                self.permission_denied_csv, 
                self.valid_columns, 
                self.valid_data
            )

        # Reset file permissions so it can be deleted in tearDown
        os.chmod(self.permission_denied_csv, 0o666)


# =============================================================================
# Test execution
# =============================================================================

if __name__ == "__main__":
    unittest.main()
