# =============================================================================
# Modules
# =============================================================================

# Python modules
import unittest

# Third party modules
import numpy as np

# Testing module
import ForecasterReferenceBook as frb

# =============================================================================
# Variables
# =============================================================================

# Calculation constants
T_ABS = -273.15
NUMBER_COEFF = 3
MIN_WIND_SPEED = 0
MIN_CLOUD_COVER = 0


# =============================================================================
# Tests
# =============================================================================


class TestGetKLookup(unittest.TestCase):

    def setUp(self):
        """Set up test data before each test case runs"""
        self.wind_speed = np.array([5, 10, 15])
        self.cloud_cover = np.array([3, 5, 7])

        self.min_wind = np.array([0, 6, 12])
        self.max_wind = np.array([6, 12, 18])

        self.min_cover = np.array([0, 4, 6])
        self.max_cover = np.array([4, 6, 8])

        self.K_values = np.array([0.1, 0.2, 0.3])  # Expected K values

    def test_correct_K_values(self):
        """Test if the function returns correct K values"""
        expected_K = np.array([0.1, 0.2, 0.3])
        result = frb.get_K_lookup(
            self.wind_speed, 
            self.min_wind, 
            self.max_wind, 
            self.cloud_cover, 
            self.min_cover, 
            self.max_cover, 
            self.K_values
        )
        np.testing.assert_array_equal(result, expected_K)

    def test_out_of_bounds_wind(self):
        """Test wind speed that is outside the lookup table range"""
        min_wind = np.array([0, 6, 24])  # Out of range
        with self.assertRaises(AssertionError):
            frb.get_K_lookup(
                self.wind_speed, 
                min_wind, 
                self.max_wind, 
                self.cloud_cover, 
                self.min_cover, 
                self.max_cover, 
                self.K_values
            )

    def test_out_of_bounds_cloud(self):
        """Test cloud cover that is outside the lookup table range"""
        min_cover = np.array([0, 4, 10])  # Out of range
        with self.assertRaises(AssertionError):
            frb.get_K_lookup(
                self.wind_speed, 
                self.min_wind, 
                self.max_wind, 
                self.cloud_cover, 
                min_cover, 
                self.max_cover, 
                self.K_values
            )

    def test_invalid_shapes(self):
        """Test for mismatched array lengths"""
        invalid_min_wind = np.array([0, 6])  # Should be length 3
        with self.assertRaises(AssertionError):
            frb.get_K_lookup(
                self.wind_speed,
                invalid_min_wind,
                self.max_wind,
                self.cloud_cover,
                self.min_cover,
                self.max_cover,
                self.K_values,
            )

    def test_invalid_shapes_wind_speed_cloud_cover(self):
        """Test for mismatched array lengths of wind speed and cloud cover"""
        invalid_wind_speed = np.array([0, 6])  # Should be length 3
        with self.assertRaises(AssertionError):
            frb.get_K_lookup(
                invalid_wind_speed,
                self.min_wind,
                self.max_wind,
                self.cloud_cover,
                self.min_cover,
                self.max_cover,
                self.K_values,
            )

    def test_negative_wind_speed(self):
        """Test for negative wind speeds"""
        wind_speed = np.array([-5, 10, 15])  # Contains negative value
        with self.assertRaises(AssertionError):
            frb.get_K_lookup(
                wind_speed, 
                self.min_wind, 
                self.max_wind, 
                self.cloud_cover, 
                self.min_cover, 
                self.max_cover, 
                self.K_values
            )

    def test_negative_cloud_cover(self):
        """Test for negative cloud cover"""
        cloud_cover = np.array([3, -2, 7])  # Contains negative value
        with self.assertRaises(AssertionError):
            frb.get_K_lookup(
                self.wind_speed, 
                self.min_wind, 
                self.max_wind, 
                cloud_cover, 
                self.min_cover, 
                self.max_cover, 
                self.K_values
            )


class TestCalculateTemperatureMinNoonCelcius(unittest.TestCase):

    def setUp(self):
        """Set up test data before each test case runs"""
        self.T_12 = np.array([20.0, 25.0, 30.0])  # Noon temperatures
        self.Td_12 = np.array([15.0, 18.0, 22.0])  # Dew point at noon
        self.K = np.array([1.0, 1.5, 2.0])  # K values
        self.coeff = [
            np.array([0.5]), np.array([0.3]), np.array([5.0])
        ]  # Coefficients

    def test_correct_temperature_min(self):
        """Test if function correctly calculates Tmin_12"""
        expected_Tmin_12 = self.coeff[0] * self.T_12 + self.coeff[1] * \
            self.Td_12 + self.coeff[2] + self.K
        result = frb.calculate_temperature_min_noon_celcius(
            self.T_12, 
            self.Td_12, 
            self.K, 
            self.coeff
        )
        np.testing.assert_array_almost_equal(
            result, 
            expected_Tmin_12, 
            decimal=5
        )

    def test_non_physical_temperature(self):
        """Test for non-physical temperature (below absolute zero)"""
        T_12_invalid = np.array([-300.0])  # Below absolute zero
        with self.assertRaises(AssertionError):
            frb.calculate_temperature_min_noon_celcius(
                T_12_invalid, 
                self.Td_12, 
                self.K, 
                self.coeff
            )

    def test_non_physical_temperature_dew_point(self):
        """Test for non-physical dew point temperature (below absolute zero)"""
        Td_12_invalid = np.array([-300.0])  # Below absolute zero
        with self.assertRaises(AssertionError):
            frb.calculate_temperature_min_noon_celcius(
                self.T_12, 
                Td_12_invalid, 
                self.K, 
                self.coeff
            )

    def test_invalid_coefficient_length(self):
        """Test for invalid coefficient length"""
        # Missing one coefficient
        invalid_coeff = [np.array([0.5]), np.array([0.3])]  
        with self.assertRaises(AssertionError):
            frb.calculate_temperature_min_noon_celcius(
                self.T_12, 
                self.Td_12, 
                self.K, 
                invalid_coeff
            )

    def test_invalid_coefficient_type(self):
        """Test for non-list coefficient type"""
        # Should be a list of NumPy arrays
        invalid_coeff = np.array([0.5, 0.3, 5.0])
        with self.assertRaises(AssertionError):
            frb.calculate_temperature_min_noon_celcius(
                self.T_12, 
                self.Td_12, 
                self.K, 
                invalid_coeff
            )

    def test_non_numpy_inputs_T_12(self):
        """Test for non-NumPy array T_12 inputs"""
        # List instead of NumPy array
        T_12_list = [20.0, 25.0, 30.0] 
        with self.assertRaises(AssertionError):
            frb.calculate_temperature_min_noon_celcius(
                T_12_list, 
                self.Td_12, 
                self.K, 
                self.coeff
            )

    def test_non_numpy_inputs_Td_12(self):
        """Test for non-NumPy array Td_12 inputs"""
        # List instead of NumPy array
        Td_12_list = [20.0, 25.0, 30.0]  
        with self.assertRaises(AssertionError):
            frb.calculate_temperature_min_noon_celcius(
                self.T_12, 
                Td_12_list, 
                self.K, 
                self.coeff
            )

    def test_non_numpy_inputs_K(self):
        """Test for non-NumPy array K inputs"""
        # List instead of NumPy array
        K_list = [20.0, 25.0, 30.0] 
        with self.assertRaises(AssertionError):
            frb.calculate_temperature_min_noon_celcius(
                self.T_12, 
                self.Td_12, 
                K_list, 
                self.coeff
            )

    def test_zero_temperatures(self):
        """Test with zero values for temperatures and K"""
        T_12_zero = np.array([0.0])
        Td_12_zero = np.array([0.0])
        K_zero = np.array([0.0])
        coeff_zero = [np.array([0.5]), np.array([0.3]), np.array([5.0])]

        expected_Tmin_12 = coeff_zero[0] * T_12_zero + coeff_zero[1] * \
            Td_12_zero + coeff_zero[2] + K_zero
        result = frb.calculate_temperature_min_noon_celcius(
            T_12_zero, 
            Td_12_zero,
            K_zero, 
            coeff_zero
        )
        np.testing.assert_array_almost_equal(
            result, 
            expected_Tmin_12,
            decimal=5
        )


# =============================================================================
# Test execution
# =============================================================================

if __name__ == "__main__":
    unittest.main()
