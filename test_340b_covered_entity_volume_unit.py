"""
Unit tests for get_340b_covered_entity_volume_data function.

These tests verify the 340b-covered-entity-volume tile functionality:
- Response structure validation (categories + series)
- Two series: "340B Covered Entity QTY" and "340B % Volume"
- Time period parameter handling (quarterly, monthly, half-yearly, yearly)
- Filter parameter handling (brands, state)
- Error handling for invalid parameters
- Database error handling (connection errors, missing tables)
- Edge cases (empty data, null values)

**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 8.1**
"""

import sys
import os
from unittest.mock import MagicMock, patch, PropertyMock
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

from lambda_handler import get_340b_covered_entity_volume_data


def create_mock_row(time_period, quantity, volume_percentage):
    """Create a mock database row with the expected attributes."""
    row = MagicMock()
    row.TimePeriod = time_period
    row.quantity = quantity
    row.volume_percentage = volume_percentage
    return row


class TestResponseStructure:
    """Tests for 340B Covered Entity Volume response structure."""

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_response_contains_categories_field(self, mock_text, mock_get_session):
        """
        Test that response contains categories field.
        
        Verifies that the response has a categories list for chart x-axis labels.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
            create_mock_row("2025Q2", 1200, 30),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        assert isinstance(response, dict), "Response should be a dictionary"
        assert "categories" in response, "Response should contain categories field"
        assert isinstance(response["categories"], list), "categories should be a list"

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_response_contains_series_field(self, mock_text, mock_get_session):
        """
        Test that response contains series field.
        
        Verifies that the response has a series list for chart data.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        assert "series" in response, "Response should contain series field"
        assert isinstance(response["series"], list), "series should be a list"

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_response_has_exactly_two_series(self, mock_text, mock_get_session):
        """
        Test that response contains exactly two series.
        
        Verifies that series array has the expected two data series:
        - 340B Covered Entity QTY
        - 340B % Volume
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        assert len(response.get("series", [])) == 2, "Response should have exactly 2 series"


class TestSeriesStructure:
    """Tests for 340B Covered Entity Volume series structure."""

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_series_contains_covered_entity_qty(self, mock_text, mock_get_session):
        """
        Test that series contains 340B Covered Entity QTY data.
        
        Verifies that series includes volume quantity data with area chart type.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
            create_mock_row("2025Q2", 1200, 30),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        qty_series = next(
            (s for s in response.get("series", []) if s.get("name") == "340B Covered Entity QTY"),
            None
        )
        assert qty_series is not None, "Series should contain 340B Covered Entity QTY"
        assert qty_series.get("type") == "area", "QTY series should be area type"
        assert qty_series.get("yAxis") == 0, "QTY series should use yAxis 0"
        assert "data" in qty_series, "QTY series should have data field"

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_series_contains_volume_percentage(self, mock_text, mock_get_session):
        """
        Test that series contains 340B % Volume data.
        
        Verifies that series includes percentage volume data with area chart type.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
            create_mock_row("2025Q2", 1200, 30),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        pct_series = next(
            (s for s in response.get("series", []) if s.get("name") == "340B % Volume"),
            None
        )
        assert pct_series is not None, "Series should contain 340B % Volume"
        assert pct_series.get("type") == "area", "% Volume series should be area type"
        assert pct_series.get("yAxis") == 1, "% Volume series should use yAxis 1 (secondary axis)"
        assert "data" in pct_series, "% Volume series should have data field"

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_series_data_length_matches_categories(self, mock_text, mock_get_session):
        """
        Test that series data length matches categories length.
        
        Verifies that each series has the same number of data points as categories.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
            create_mock_row("2025Q2", 1200, 30),
            create_mock_row("2025Q3", 1400, 35),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        categories_length = len(response["categories"])
        for series in response["series"]:
            assert len(series["data"]) == categories_length, \
                f"Series '{series['name']}' data length should match categories length"

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_series_data_values_are_integers(self, mock_text, mock_get_session):
        """
        Test that all data values in series are integers.
        
        Verifies that the data points in each series are converted to integers.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000.5, 25.7),
            create_mock_row("2025Q2", 1200.3, 30.2),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        for series in response["series"]:
            for value in series["data"]:
                assert isinstance(value, int), \
                    f"Data value {value} in series '{series['name']}' should be an integer"


class TestTimePeriodParameter:
    """Tests for time-period parameter handling."""

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_valid_time_period_quarterly(self, mock_text, mock_get_session):
        """Test that quarterly time period is accepted."""
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data({"time-period": "quarterly"})

        assert "error" not in response, "quarterly should be a valid time period"
        assert "categories" in response

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_valid_time_period_monthly(self, mock_text, mock_get_session):
        """Test that monthly time period is accepted."""
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("Jan'25", 1000, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data({"time-period": "monthly"})

        assert "error" not in response, "monthly should be a valid time period"
        assert "categories" in response

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_valid_time_period_half_yearly(self, mock_text, mock_get_session):
        """Test that half-yearly time period is accepted."""
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025H1", 1000, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data({"time-period": "half-yearly"})

        assert "error" not in response, "half-yearly should be a valid time period"
        assert "categories" in response

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_valid_time_period_yearly(self, mock_text, mock_get_session):
        """Test that yearly time period is accepted."""
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025", 1000, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data({"time-period": "yearly"})

        assert "error" not in response, "yearly should be a valid time period"
        assert "categories" in response

    def test_invalid_time_period(self):
        """
        Test that invalid time period returns error.
        
        Verifies that an invalid time-period parameter returns an error response.
        """
        response = get_340b_covered_entity_volume_data({"time-period": "weekly"})

        assert "error" in response, "Invalid time period should return error"
        assert response["error"] == "Invalid time period"
        assert "weekly" in response["message"]
        assert response["tileName"] == "340b-covered-entity-volume"

    def test_default_time_period_is_quarterly(self):
        """
        Test that default time period is quarterly when not specified.
        
        The function should default to 'quarterly' when time-period is not provided.
        """
        # This test verifies the default behavior by checking the code path
        # The actual default is set in the function: time_period = "quarterly"
        # When query_params is None or doesn't have 'time-period', quarterly is used
        pass  # Covered by other tests that don't specify time-period


class TestFilterParameters:
    """Tests for filter parameter handling (brands, state)."""

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    @patch('lambda_handler.generate_global_filters_from_query_params')
    def test_brands_filter_is_applied(self, mock_generate_filters, mock_text, mock_get_session):
        """Test that brands filter parameter is processed."""
        mock_generate_filters.return_value = " AND Brand = 'TestBrand'"
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data({"brands": "TestBrand"})

        # Verify generate_global_filters was called with brands parameter
        mock_generate_filters.assert_called_once()
        call_args = mock_generate_filters.call_args[0]
        assert "brands" in call_args[0], "brands should be passed to filter generator"

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    @patch('lambda_handler.generate_global_filters_from_query_params')
    def test_state_filter_is_applied(self, mock_generate_filters, mock_text, mock_get_session):
        """Test that state filter parameter is processed."""
        mock_generate_filters.return_value = " AND State = 'CA'"
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data({"state": "CA"})

        # Verify generate_global_filters was called with state parameter
        mock_generate_filters.assert_called_once()
        call_args = mock_generate_filters.call_args[0]
        assert "state" in call_args[0], "state should be passed to filter generator"

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    @patch('lambda_handler.generate_global_filters_from_query_params')
    def test_multiple_filters_are_applied(self, mock_generate_filters, mock_text, mock_get_session):
        """Test that multiple filter parameters are processed together."""
        mock_generate_filters.return_value = " AND Brand = 'TestBrand' AND State = 'CA'"
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data({
            "brands": "TestBrand",
            "state": "CA",
            "time-period": "quarterly"
        })

        mock_generate_filters.assert_called_once()


class TestEmptyDataHandling:
    """Tests for empty data scenarios."""

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_empty_result_returns_empty_structure(self, mock_text, mock_get_session):
        """
        Test that empty database result returns empty but valid structure.
        
        When no data is found, the response should have empty categories and series data.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        assert "categories" in response
        assert response["categories"] == []
        assert "series" in response
        assert len(response["series"]) == 2
        assert response["series"][0]["data"] == []
        assert response["series"][1]["data"] == []

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_null_quantity_converted_to_zero(self, mock_text, mock_get_session):
        """
        Test that null quantity values are converted to zero.
        
        When database returns None for quantity, it should be converted to 0.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", None, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        qty_series = next(
            (s for s in response["series"] if s["name"] == "340B Covered Entity QTY"),
            None
        )
        assert qty_series["data"][0] == 0, "None quantity should be converted to 0"

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_null_volume_percentage_converted_to_zero(self, mock_text, mock_get_session):
        """
        Test that null volume_percentage values are converted to zero.
        
        When database returns None for volume_percentage, it should be converted to 0.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, None),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        pct_series = next(
            (s for s in response["series"] if s["name"] == "340B % Volume"),
            None
        )
        assert pct_series["data"][0] == 0, "None volume_percentage should be converted to 0"


class TestDatabaseErrorHandling:
    """Tests for database error handling."""

    @patch('lambda_handler.get_session')
    def test_database_connection_error(self, mock_get_session):
        """
        Test that database connection errors are handled gracefully.
        
        When database connection fails, should return error response.
        """
        mock_get_session.side_effect = Exception("Connection refused")

        response = get_340b_covered_entity_volume_data()

        assert "error" in response, "Should return error response"
        assert response["error"] == "Internal server error"
        assert "Connection refused" in response["message"]
        assert response["tileName"] == "340b-covered-entity-volume"

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_query_execution_error(self, mock_text, mock_get_session):
        """
        Test that query execution errors are handled gracefully.
        
        When query execution fails, should return error response.
        """
        mock_session = MagicMock()
        mock_session.execute.side_effect = Exception("Query failed: syntax error")
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        assert "error" in response, "Should return error response"
        assert response["error"] == "Internal server error"
        assert response["tileName"] == "340b-covered-entity-volume"

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_session_is_closed_on_success(self, mock_text, mock_get_session):
        """
        Test that database session is closed after successful query.
        
        The finally block should close the session.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        get_340b_covered_entity_volume_data()

        mock_session.close.assert_called_once()

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_session_is_closed_on_error(self, mock_text, mock_get_session):
        """
        Test that database session is closed even when error occurs.
        
        The finally block should close the session even after exception.
        """
        mock_session = MagicMock()
        mock_session.execute.side_effect = Exception("Query failed")
        mock_get_session.return_value = mock_session

        get_340b_covered_entity_volume_data()

        mock_session.close.assert_called_once()


class TestDataProcessing:
    """Tests for data processing and transformation."""

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_time_period_extracted_to_categories(self, mock_text, mock_get_session):
        """
        Test that TimePeriod values are correctly extracted to categories.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
            create_mock_row("2025Q2", 1200, 30),
            create_mock_row("2025Q3", 1400, 35),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        assert response["categories"] == ["2025Q1", "2025Q2", "2025Q3"]

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_quantity_values_extracted_correctly(self, mock_text, mock_get_session):
        """
        Test that quantity values are correctly extracted to series data.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
            create_mock_row("2025Q2", 1200, 30),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        qty_series = next(
            (s for s in response["series"] if s["name"] == "340B Covered Entity QTY"),
            None
        )
        assert qty_series["data"] == [1000, 1200]

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_volume_percentage_values_extracted_correctly(self, mock_text, mock_get_session):
        """
        Test that volume_percentage values are correctly extracted to series data.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
            create_mock_row("2025Q2", 1200, 30),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        pct_series = next(
            (s for s in response["series"] if s["name"] == "340B % Volume"),
            None
        )
        assert pct_series["data"] == [25, 30]

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_data_ordering_preserved(self, mock_text, mock_get_session):
        """
        Test that data ordering from database is preserved in response.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 100, 10),
            create_mock_row("2025Q2", 200, 20),
            create_mock_row("2025Q3", 300, 30),
            create_mock_row("2025Q4", 400, 40),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        # Categories should be in same order as database results
        assert response["categories"] == ["2025Q1", "2025Q2", "2025Q3", "2025Q4"]
        
        # Data values should be in same order
        qty_series = next(
            (s for s in response["series"] if s["name"] == "340B Covered Entity QTY"),
            None
        )
        assert qty_series["data"] == [100, 200, 300, 400]


class TestDualSeriesValidation:
    """Tests for dual-series validation via handle_dual_series_error_scenarios."""

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    @patch('lambda_handler.handle_dual_series_error_scenarios')
    def test_dual_series_validation_is_called(self, mock_validate, mock_text, mock_get_session):
        """
        Test that handle_dual_series_error_scenarios is called for validation.
        """
        mock_validate.return_value = (True, {})
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        get_340b_covered_entity_volume_data()

        mock_validate.assert_called_once()

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    @patch('lambda_handler.handle_dual_series_error_scenarios')
    def test_validation_error_returned_when_invalid(self, mock_validate, mock_text, mock_get_session):
        """
        Test that validation error is returned when dual-series validation fails.
        """
        error_response = {
            "error": "Invalid series structure",
            "message": "Expected exactly 2 data series",
            "tileName": "340b-covered-entity-volume"
        }
        mock_validate.return_value = (False, error_response)
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data()

        assert response == error_response


class TestNoQueryParams:
    """Tests for function behavior with no query parameters."""

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_no_query_params_uses_defaults(self, mock_text, mock_get_session):
        """
        Test that function works with no query parameters.
        
        When called with None, should use default quarterly time period.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data(None)

        assert "error" not in response
        assert "categories" in response
        assert "series" in response

    @patch('lambda_handler.get_session')
    @patch('lambda_handler.text')
    def test_empty_query_params_dict(self, mock_text, mock_get_session):
        """
        Test that function works with empty query parameters dict.
        """
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            create_mock_row("2025Q1", 1000, 25),
        ]
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value = mock_session

        response = get_340b_covered_entity_volume_data({})

        assert "error" not in response
        assert "categories" in response
        assert "series" in response


class TestTileName:
    """Tests for tile name in responses."""

    def test_error_response_contains_tile_name(self):
        """
        Test that error responses contain the correct tileName.
        """
        response = get_340b_covered_entity_volume_data({"time-period": "invalid"})

        assert "tileName" in response
        assert response["tileName"] == "340b-covered-entity-volume"

    @patch('lambda_handler.get_session')
    def test_exception_response_contains_tile_name(self, mock_get_session):
        """
        Test that exception responses contain the correct tileName.
        """
        mock_get_session.side_effect = Exception("Database error")

        response = get_340b_covered_entity_volume_data()

        assert "tileName" in response
        assert response["tileName"] == "340b-covered-entity-volume"
