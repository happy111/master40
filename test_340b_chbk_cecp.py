"""
Unit tests for 340b-chbk-cecp tile (get_340b_chbk_cecp function).

These tests verify the 340B Chargeback CECP data tile:
- Response structure (categories, series)
- Series structure validation (CE, CP, Chargeback)
- Time period parameter handling
- Error handling for invalid parameters
- Chart type specifications (CE/CP as line, Chargeback as column)
- Data processing with mocked Snowflake database results
"""

import sys
import os
from unittest.mock import MagicMock, patch
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock dependencies before importing
sys.modules['pandas'] = MagicMock()
sys.modules['sqlalchemy'] = MagicMock()
sys.modules['sqlalchemy.orm'] = MagicMock()
sys.modules['sqlalchemy.engine'] = MagicMock()
sys.modules['boto3'] = MagicMock()
sys.modules['botocore'] = MagicMock()
sys.modules['botocore.config'] = MagicMock()
sys.modules['botocore.exceptions'] = MagicMock()
sys.modules['aws_lambda_powertools'] = MagicMock()
sys.modules['aws_lambda_powertools.event_handler'] = MagicMock()
sys.modules['aws_lambda_powertools.event_handler.api_gateway'] = MagicMock()
sys.modules['aws_lambda_powertools.metrics'] = MagicMock()
sys.modules['aws_lambda_powertools.utilities'] = MagicMock()
sys.modules['aws_lambda_powertools.utilities.typing'] = MagicMock()
sys.modules['aws_lambda_powertools.utilities.data_classes'] = MagicMock()
sys.modules['response_handler'] = MagicMock()
sys.modules['utils'] = MagicMock()
sys.modules['utils.DbUtil'] = MagicMock()
sys.modules['utils.query_templates'] = MagicMock()

from lambda_handler import get_340b_chbk_cecp


class TestChbkCecpResponseStructure:
    """Tests for 340B Chargeback CECP response structure."""

    @patch('lambda_handler.get_sf_session')
    def test_response_contains_categories(self, mock_get_sf_session):
        """
        Test that response contains categories field.
        
        Verifies that the response has a categories list for chart x-axis labels.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        assert isinstance(response, dict), "Response should be a dictionary"
        assert "categories" in response, "Response should contain categories field"
        assert isinstance(response["categories"], list), "categories should be a list"

    @patch('lambda_handler.get_sf_session')
    def test_response_contains_series(self, mock_get_sf_session):
        """
        Test that response contains series field.
        
        Verifies that the response has a series list for chart data.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        assert "series" in response, "Response should contain series field"
        assert isinstance(response["series"], list), "series should be a list"

    @patch('lambda_handler.get_sf_session')
    def test_response_has_three_series(self, mock_get_sf_session):
        """
        Test that response contains exactly three series (CE, CP, Chargeback).
        
        Verifies that the series array has the expected three data series.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        assert len(response.get("series", [])) == 3, "Response should have exactly 3 series"


class TestChbkCecpSeriesStructure:
    """Tests for 340B Chargeback CECP series structure."""

    @patch('lambda_handler.get_sf_session')
    def test_series_contains_ce_data(self, mock_get_sf_session):
        """
        Test that series contains CE (Covered Entity) data.
        
        Verifies that series includes a CE entry with line chart type.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        ce_series = next((s for s in response.get("series", []) if s.get("name") == "CE"), None)
        assert ce_series is not None, "Series should contain CE data"
        assert ce_series.get("type") == "line", "CE series should be line type"
        assert ce_series.get("yAxis") == 1, "CE series should use yAxis 1"
        assert "data" in ce_series, "CE series should have data field"

    @patch('lambda_handler.get_sf_session')
    def test_series_contains_cp_data(self, mock_get_sf_session):
        """
        Test that series contains CP (Contract Pharmacy) data.
        
        Verifies that series includes a CP entry with line chart type.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        cp_series = next((s for s in response.get("series", []) if s.get("name") == "CP"), None)
        assert cp_series is not None, "Series should contain CP data"
        assert cp_series.get("type") == "line", "CP series should be line type"
        assert cp_series.get("yAxis") == 1, "CP series should use yAxis 1"
        assert "data" in cp_series, "CP series should have data field"

    @patch('lambda_handler.get_sf_session')
    def test_series_contains_chargeback_data(self, mock_get_sf_session):
        """
        Test that series contains Chargeback data.
        
        Verifies that series includes a Chargeback entry with column chart type on primary axis.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        chbk_series = next((s for s in response.get("series", []) if s.get("name") == "Chargeback"), None)
        assert chbk_series is not None, "Series should contain Chargeback data"
        assert chbk_series.get("type") == "column", "Chargeback series should be column type"
        assert chbk_series.get("yAxis") == 0, "Chargeback series should use yAxis 0 (primary axis)"
        assert "data" in chbk_series, "Chargeback series should have data field"

    @patch('lambda_handler.get_sf_session')
    def test_series_order_ce_cp_chargeback(self, mock_get_sf_session):
        """
        Test that series are in expected order: CE, CP, Chargeback.
        
        Verifies the order of series matches expected chart rendering order.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        series = response.get("series", [])
        assert len(series) == 3, "Should have 3 series"
        assert series[0].get("name") == "CE", "First series should be CE"
        assert series[1].get("name") == "CP", "Second series should be CP"
        assert series[2].get("name") == "Chargeback", "Third series should be Chargeback"


class TestChbkCecpTimePeriodParameter:
    """Tests for time-period parameter handling."""

    def test_invalid_time_period_returns_error(self):
        """
        Test that invalid time-period parameter returns error.
        
        Verifies that passing an invalid time-period value returns an error response.
        """
        response = get_340b_chbk_cecp({"time-period": "invalid"})

        assert "error" in response, "Response should contain error field"
        assert response["error"] == "Invalid time period", "Error should indicate invalid time period"
        assert "tileName" in response, "Response should contain tileName field"
        assert response["tileName"] == "340b-chbk-cecp", "tileName should be 340b-chbk-cecp"

    def test_invalid_time_period_includes_valid_options(self):
        """
        Test that error message for invalid time-period includes valid options.
        
        Verifies that the error message tells users what valid options are.
        """
        response = get_340b_chbk_cecp({"time-period": "invalid"})

        assert "message" in response, "Response should contain message field"
        assert "quarterly" in response["message"], "Message should mention 'quarterly'"
        assert "monthly" in response["message"], "Message should mention 'monthly'"
        assert "half-yearly" in response["message"], "Message should mention 'half-yearly'"
        assert "yearly" in response["message"], "Message should mention 'yearly'"

    @patch('lambda_handler.get_sf_session')
    def test_valid_time_period_monthly(self, mock_get_sf_session):
        """
        Test that 'monthly' is a valid time-period parameter.
        
        Verifies that passing 'monthly' as time-period does not return an error.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp({"time-period": "monthly"})

        assert "error" not in response or response.get("error") != "Invalid time period", \
            "'monthly' should be a valid time-period"

    @patch('lambda_handler.get_sf_session')
    def test_valid_time_period_quarterly(self, mock_get_sf_session):
        """
        Test that 'quarterly' is a valid time-period parameter.
        
        Verifies that passing 'quarterly' as time-period does not return an error.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp({"time-period": "quarterly"})

        assert "error" not in response or response.get("error") != "Invalid time period", \
            "'quarterly' should be a valid time-period"

    @patch('lambda_handler.get_sf_session')
    def test_valid_time_period_half_yearly(self, mock_get_sf_session):
        """
        Test that 'half-yearly' is a valid time-period parameter.
        
        Verifies that passing 'half-yearly' as time-period does not return an error.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp({"time-period": "half-yearly"})

        assert "error" not in response or response.get("error") != "Invalid time period", \
            "'half-yearly' should be a valid time-period"

    @patch('lambda_handler.get_sf_session')
    def test_valid_time_period_yearly(self, mock_get_sf_session):
        """
        Test that 'yearly' is a valid time-period parameter.
        
        Verifies that passing 'yearly' as time-period does not return an error.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp({"time-period": "yearly"})

        assert "error" not in response or response.get("error") != "Invalid time period", \
            "'yearly' should be a valid time-period"

    @patch('lambda_handler.get_sf_session')
    def test_no_query_params_uses_default(self, mock_get_sf_session):
        """
        Test that no query params defaults to quarterly.
        
        Verifies that calling without parameters works and uses default time period.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        assert "error" not in response or response.get("error") != "Invalid time period", \
            "No params should use default time period"
        assert "categories" in response, "Response should contain categories"

    @patch('lambda_handler.get_sf_session')
    def test_none_query_params(self, mock_get_sf_session):
        """
        Test that None query params is handled correctly.
        
        Verifies that passing None as query_params doesn't cause errors.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp(None)

        assert "categories" in response, "Response should contain categories"
        assert "series" in response, "Response should contain series"


class TestChbkCecpErrorHandling:
    """Tests for error handling."""

    @patch('lambda_handler.get_sf_session')
    def test_database_connection_error_returns_error_response(self, mock_get_sf_session):
        """
        Test that database connection errors return proper error response.
        
        Verifies that when a database connection error occurs, an error response is returned.
        """
        mock_get_sf_session.side_effect = Exception("Database connection failed")

        response = get_340b_chbk_cecp()

        assert "error" in response, "Response should contain error field"
        assert response["error"] == "Internal server error", "Error should indicate internal server error"
        assert "message" in response, "Response should contain message field"
        assert "tileName" in response, "Response should contain tileName field"
        assert response["tileName"] == "340b-chbk-cecp", "tileName should be 340b-chbk-cecp"

    @patch('lambda_handler.get_sf_session')
    def test_query_execution_error_returns_error_response(self, mock_get_sf_session):
        """
        Test that query execution errors return proper error response.
        
        Verifies that when query execution fails, an error response is returned.
        """
        mock_session = MagicMock()
        mock_session.execute.side_effect = Exception("Query execution failed")
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        assert "error" in response, "Response should contain error field"
        assert "message" in response, "Response should contain message field"
        assert "Query execution failed" in response["message"], "Message should contain error details"

    @patch('lambda_handler.get_sf_session')
    def test_session_close_called_on_success(self, mock_get_sf_session):
        """
        Test that session is closed on successful execution.
        
        Verifies that the database session is properly closed after success.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        get_340b_chbk_cecp()

        mock_session.close.assert_called_once()

    @patch('lambda_handler.get_sf_session')
    def test_session_close_called_on_error(self, mock_get_sf_session):
        """
        Test that session is closed even when an error occurs.
        
        Verifies that the database session is properly closed after an error.
        """
        mock_session = MagicMock()
        mock_session.execute.side_effect = Exception("Query failed")
        mock_get_sf_session.return_value = mock_session

        get_340b_chbk_cecp()

        mock_session.close.assert_called_once()


class TestChbkCecpWithMockedData:
    """Tests with mocked Snowflake database data."""

    @patch('lambda_handler.get_sf_session')
    def test_data_processing_with_single_row(self, mock_get_sf_session):
        """
        Test data processing with a single row from Snowflake database.
        
        Verifies that a single database row is properly processed into chart data.
        Note: Chargeback values are converted to millions with 1 decimal place.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        
        # Create mock row with Snowflake column names
        mock_row = MagicMock()
        mock_row.timeperiod = "2024Q1"
        mock_row.perc_ce_chbk = 45.5
        mock_row.perc_cp_chbk = 54.5
        mock_row.chbk = 500000000.0  # 500 million -> will be converted to 500.0

        mock_result.fetchall.return_value = [mock_row]
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        assert response["categories"] == ["2024Q1"], "Categories should contain the time period"
        
        ce_series = next(s for s in response["series"] if s["name"] == "CE")
        assert ce_series["data"] == [45.5], "CE data should contain the percentage"
        
        cp_series = next(s for s in response["series"] if s["name"] == "CP")
        assert cp_series["data"] == [54.5], "CP data should contain the percentage"
        
        chbk_series = next(s for s in response["series"] if s["name"] == "Chargeback")
        assert chbk_series["data"] == [500.0], "Chargeback data should be in millions (500M -> 500.0)"

    @patch('lambda_handler.get_sf_session')
    def test_data_processing_with_multiple_rows(self, mock_get_sf_session):
        """
        Test data processing with multiple rows from Snowflake database.
        
        Verifies that multiple database rows are properly processed into chart data.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        
        # Create mock rows for multiple quarters with Snowflake column names
        mock_row_q1 = MagicMock()
        mock_row_q1.timeperiod = "2024Q1"
        mock_row_q1.perc_ce_chbk = 40.0
        mock_row_q1.perc_cp_chbk = 60.0
        mock_row_q1.chbk = 400000000.0  # 400 million

        mock_row_q2 = MagicMock()
        mock_row_q2.timeperiod = "2024Q2"
        mock_row_q2.perc_ce_chbk = 42.5
        mock_row_q2.perc_cp_chbk = 57.5
        mock_row_q2.chbk = 450000000.0  # 450 million

        mock_row_q3 = MagicMock()
        mock_row_q3.timeperiod = "2024Q3"
        mock_row_q3.perc_ce_chbk = 45.0
        mock_row_q3.perc_cp_chbk = 55.0
        mock_row_q3.chbk = 500000000.0  # 500 million

        mock_result.fetchall.return_value = [mock_row_q1, mock_row_q2, mock_row_q3]
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        assert response["categories"] == ["2024Q1", "2024Q2", "2024Q3"], \
            "Categories should contain all time periods"
        
        ce_series = next(s for s in response["series"] if s["name"] == "CE")
        assert ce_series["data"] == [40.0, 42.5, 45.0], "CE data should contain all percentages"
        
        cp_series = next(s for s in response["series"] if s["name"] == "CP")
        assert cp_series["data"] == [60.0, 57.5, 55.0], "CP data should contain all percentages"
        
        chbk_series = next(s for s in response["series"] if s["name"] == "Chargeback")
        assert chbk_series["data"] == [400.0, 450.0, 500.0], "Chargeback data should be in millions"

    @patch('lambda_handler.get_sf_session')
    def test_empty_result_returns_empty_arrays(self, mock_get_sf_session):
        """
        Test that empty Snowflake database results return empty arrays.
        
        Verifies that when no data is returned from database, empty arrays are provided.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        assert response["categories"] == [], "Categories should be empty list"
        
        for series in response["series"]:
            assert series["data"] == [], f"{series['name']} data should be empty list"

    @patch('lambda_handler.get_sf_session')
    def test_data_types_are_floats(self, mock_get_sf_session):
        """
        Test that data values are properly converted to floats.
        
        Verifies that all data values are float type as expected by chart libraries.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        
        # Create mock row with Snowflake column names
        mock_row = MagicMock()
        mock_row.timeperiod = "2024Q1"
        mock_row.perc_ce_chbk = 45  # Integer value from DB
        mock_row.perc_cp_chbk = 55  # Integer value from DB
        mock_row.chbk = 500000000  # Integer value from DB (500 million)

        mock_result.fetchall.return_value = [mock_row]
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        for series in response["series"]:
            for value in series["data"]:
                assert isinstance(value, float), f"Values in {series['name']} should be floats"


class TestChbkCecpDataIntegrity:
    """Tests for data integrity and consistency."""

    @patch('lambda_handler.get_sf_session')
    def test_categories_match_data_length(self, mock_get_sf_session):
        """
        Test that categories length matches data arrays length.
        
        Verifies that the number of categories matches the number of data points in each series.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        
        # Create 4 mock rows with Snowflake column names
        rows = []
        for i in range(4):
            mock_row = MagicMock()
            mock_row.timeperiod = f"2024Q{i+1}"
            mock_row.perc_ce_chbk = 40.0 + i
            mock_row.perc_cp_chbk = 60.0 - i
            mock_row.chbk = (400.0 + (i * 25)) * 1e6  # In millions
            rows.append(mock_row)

        mock_result.fetchall.return_value = rows
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        categories_len = len(response["categories"])
        for series in response["series"]:
            assert len(series["data"]) == categories_len, \
                f"{series['name']} data length should match categories length"

    @patch('lambda_handler.get_sf_session')
    def test_all_series_have_required_fields(self, mock_get_sf_session):
        """
        Test that all series have required fields.
        
        Verifies that each series object has name, data, type, and yAxis fields.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        required_fields = ["name", "data", "type", "yAxis"]
        for series in response["series"]:
            for field in required_fields:
                assert field in series, f"Series should have '{field}' field"


class TestChbkCecpChartConfiguration:
    """Tests for chart configuration options."""

    @patch('lambda_handler.get_sf_session')
    def test_ce_and_cp_are_line_type_chargeback_is_column(self, mock_get_sf_session):
        """
        Test that CE and CP are line charts, Chargeback is column chart.
        
        Verifies that CE and CP use line chart type, Chargeback uses column type.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        ce_series = next(s for s in response["series"] if s["name"] == "CE")
        cp_series = next(s for s in response["series"] if s["name"] == "CP")
        chbk_series = next(s for s in response["series"] if s["name"] == "Chargeback")
        
        assert ce_series["type"] == "line", "CE should be line type"
        assert cp_series["type"] == "line", "CP should be line type"
        assert chbk_series["type"] == "column", "Chargeback should be column type"

    @patch('lambda_handler.get_sf_session')
    def test_ce_and_cp_use_secondary_axis(self, mock_get_sf_session):
        """
        Test that CE and CP use secondary y-axis.
        
        Verifies that CE and CP percentages use yAxis 1 (secondary axis).
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        ce_series = next(s for s in response["series"] if s["name"] == "CE")
        cp_series = next(s for s in response["series"] if s["name"] == "CP")
        
        assert ce_series["yAxis"] == 1, "CE should use secondary axis (yAxis 1)"
        assert cp_series["yAxis"] == 1, "CP should use secondary axis (yAxis 1)"

    @patch('lambda_handler.get_sf_session')
    def test_chargeback_uses_primary_axis(self, mock_get_sf_session):
        """
        Test that Chargeback uses primary y-axis.
        
        Verifies that Chargeback values use yAxis 0 (primary axis).
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        chbk_series = next(s for s in response["series"] if s["name"] == "Chargeback")
        
        assert chbk_series["yAxis"] == 0, "Chargeback should use primary axis (yAxis 0)"


class TestChbkCecpEdgeCases:
    """Tests for edge cases and boundary conditions."""

    @patch('lambda_handler.get_sf_session')
    def test_handles_zero_values(self, mock_get_sf_session):
        """
        Test that zero values are handled correctly.
        
        Verifies that zero percentages and Chargeback values don't cause errors.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        
        # Create mock row with Snowflake column names
        mock_row = MagicMock()
        mock_row.timeperiod = "2024Q1"
        mock_row.perc_ce_chbk = 0.0
        mock_row.perc_cp_chbk = 0.0
        mock_row.chbk = 0.0

        mock_result.fetchall.return_value = [mock_row]
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        assert "error" not in response, "Zero values should not cause errors"
        ce_series = next(s for s in response["series"] if s["name"] == "CE")
        assert ce_series["data"] == [0.0], "Zero CE value should be preserved"

    @patch('lambda_handler.get_sf_session')
    def test_handles_large_values(self, mock_get_sf_session):
        """
        Test that large values are handled correctly.
        
        Verifies that large Chargeback values don't cause overflow or formatting issues.
        Values are converted to millions with 1 decimal place.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        
        # Create mock row with Snowflake column names
        mock_row = MagicMock()
        mock_row.timeperiod = "2024Q1"
        mock_row.perc_ce_chbk = 50.0
        mock_row.perc_cp_chbk = 50.0
        mock_row.chbk = 999999999999.99  # Very large value (will be converted to millions)

        mock_result.fetchall.return_value = [mock_row]
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        assert "error" not in response, "Large values should not cause errors"
        chbk_series = next(s for s in response["series"] if s["name"] == "Chargeback")
        # Value is converted to millions: 999999999999.99 / 1e6 = 999999.999999 -> rounded to 1000000.0
        assert chbk_series["data"][0] == 1000000.0, "Large Chargeback value should be converted to millions"

    @patch('lambda_handler.get_sf_session')
    def test_handles_decimal_precision(self, mock_get_sf_session):
        """
        Test that decimal precision is maintained for percentage values.
        
        Verifies that percentage values maintain their decimal precision.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        
        # Create mock row with Snowflake column names
        mock_row = MagicMock()
        mock_row.timeperiod = "2024Q1"
        mock_row.perc_ce_chbk = 33.333333
        mock_row.perc_cp_chbk = 66.666667
        mock_row.chbk = 500000000.0  # 500 million

        mock_result.fetchall.return_value = [mock_row]
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp()

        ce_series = next(s for s in response["series"] if s["name"] == "CE")
        assert ce_series["data"][0] == 33.333333, "Decimal precision should be maintained"

    @patch('lambda_handler.get_sf_session')
    def test_empty_query_params_dict(self, mock_get_sf_session):
        """
        Test that empty query params dictionary is handled.
        
        Verifies that passing an empty dict as query_params works correctly.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp({})

        assert "categories" in response, "Empty dict should be handled like no params"
        assert "series" in response, "Response should have series"

    @patch('lambda_handler.get_sf_session')
    def test_query_params_with_other_keys(self, mock_get_sf_session):
        """
        Test that query params with non-time-period keys are handled.
        
        Verifies that extra query parameters don't cause errors.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_sf_session.return_value = mock_session

        response = get_340b_chbk_cecp({"other-param": "value", "another": "test"})

        assert "error" not in response or response.get("error") != "Invalid time period", \
            "Other query params should be ignored"
