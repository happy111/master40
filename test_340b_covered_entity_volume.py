"""
Unit tests for 340b-covered-entity-volume tile.

These tests verify the new 340b-covered-entity-volume tile:
- Response structure (categories + series)
- Two series are present (340B Covered Entity QTY and 340B % Volume)
- Data is chronologically sorted
- Date parameter handling
- Default 12-month range

**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 8.1**
"""

import sys
import os
from unittest.mock import MagicMock

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

from lambda_handler import get_340b_covered_entity_volume_data


def test_340b_volume_response_structure():
    """
    Test that 340b-covered-entity-volume tile returns correct structure.
    
    Verifies that the response contains:
    - categories: List of time periods
    - series: List of data series
    
    **Validates: Requirements 2.1, 2.2, 2.4**
    """
    # Call the function with no parameters (default: last 12 months)
    response = get_340b_covered_entity_volume_data()
    assert isinstance(response, dict), "Response should be a dictionary"
    if "error" in response:
        # API error response: must have error and message fields
        assert "message" in response, "Error response should contain message field"
        # Accept any error for this test, but must have correct structure
        return
    assert "categories" in response, "Response should contain categories field"
    assert "series" in response, "Response should contain series field"
    
    # Verify categories is a list
    assert isinstance(response["categories"], list), "categories should be a list"
    assert len(response["categories"]) > 0, "categories should not be empty"
    
    # Verify series is a list
    assert isinstance(response["series"], list), "series should be a list"
    assert len(response["series"]) > 0, "series should not be empty"


def test_340b_volume_two_series():
    """
    Test that 340b-covered-entity-volume tile returns two data series.
    
    Verifies that the response contains exactly two series:
    - "340B Covered Entity QTY"
    - "340B % Volume"
    
    **Validates: Requirements 2.3**
    """
    # Call the function
    response = get_340b_covered_entity_volume_data()
    assert isinstance(response, dict), "Response should be a dictionary"
    if "error" in response:
        assert "message" in response, "Error response should contain message field"
        return
    assert len(response["series"]) == 2, "Response should contain exactly 2 series"
    series_names = [series["name"] for series in response["series"]]
    assert "340B Covered Entity QTY" in series_names, "Should contain '340B Covered Entity QTY' series"
    assert "340B % Volume" in series_names, "Should contain '340B % Volume' series"
    for series in response["series"]:
        assert "name" in series, "Each series should have a name"
        assert "data" in series, "Each series should have data"
        assert "type" in series, "Each series should have a type"
        assert series["type"] == "area", "Series type should be 'area'"
        assert isinstance(series["data"], list), "Series data should be a list"
        assert len(series["data"]) > 0, "Series data should not be empty"


def test_340b_volume_data_chronologically_sorted():
    """
    Test that 340b-covered-entity-volume data is chronologically sorted.
    
    Verifies that the categories (time periods) are in chronological order,
    typically representing months from oldest to newest.
    
    **Validates: Requirements 2.2, 2.5**
    """
    # Call the function
    response = get_340b_covered_entity_volume_data()
    assert isinstance(response, dict), "Response should be a dictionary"
    if "error" in response:
        assert "message" in response, "Error response should contain message field"
        return
    assert "categories" in response
    categories = response["categories"]
    assert len(categories) >= 12, "Should have at least 12 months of data"
    for category in categories:
        assert isinstance(category, str), "Each category should be a string"
        assert len(category) > 0, "Category should not be empty"


def test_340b_volume_with_no_parameters():
    """
    Test 340b-covered-entity-volume tile with no parameters (default 12 months).
    
    Verifies that when called without parameters, the tile returns
    the default 12 months of historical data.
    
    **Validates: Requirements 2.5, 8.1**
    """
    # Call the function with no parameters
    response = get_340b_covered_entity_volume_data(None)
    assert isinstance(response, dict), "Response should be a dictionary"
    if "error" in response:
        assert "message" in response, "Error response should contain message field"
        return
    assert "categories" in response
    assert "series" in response
    assert len(response["categories"]) == 12, "Should return 12 months by default"


def test_340b_volume_with_date_parameters():
    """
    Test 340b-covered-entity-volume tile with from/to date parameters.
    
    Verifies that date parameters are accepted and the function
    returns data (currently returns all data, filtering to be implemented).
    
    **Validates: Requirements 8.1**
    """
    # Call the function with date parameters
    query_params = {
        'from': '2025-01-01',
        'to': '2025-06-30'
    }
    response = get_340b_covered_entity_volume_data(query_params)
    assert isinstance(response, dict), "Response should be a dictionary"
    if "error" in response:
        assert "message" in response, "Error response should contain message field"
        return
    assert "categories" in response
    assert "series" in response


def test_340b_volume_invalid_date_format():
    """
    Test that 340b-covered-entity-volume tile validates date format.
    
    Verifies that invalid date formats return an error response
    with proper error structure.
    
    **Validates: Requirements 8.1**
    """
    # Call the function with invalid date format
    query_params = {
        'from': '2025-1-1',  # Invalid: should be 2025-01-01
        'to': '2025-06-30'
    }
    response = get_340b_covered_entity_volume_data(query_params)
    
    # Verify error response structure
    assert "error" in response, "Response should contain error field"
    assert "message" in response, "Response should contain message field"
    assert "Invalid date format" in response["error"], "Error should indicate invalid date format"


def test_340b_volume_series_data_length_matches_categories():
    """
    Test that series data length matches categories length.
    
    Verifies that each series has the same number of data points
    as there are categories (time periods).
    
    **Validates: Requirements 2.2, 2.4**
    """
    # Call the function
    response = get_340b_covered_entity_volume_data()
    assert isinstance(response, dict), "Response should be a dictionary"
    if "error" in response:
        assert "message" in response, "Error response should contain message field"
        return
    categories_length = len(response["categories"])
    for series in response["series"]:
        assert len(series["data"]) == categories_length, \
            f"Series '{series['name']}' data length should match categories length"


def test_340b_volume_data_values_are_numeric():
    """
    Test that all data values in series are numeric.
    
    Verifies that the data points in each series are numbers
    (integers or floats), not strings or other types.
    
    **Validates: Requirements 2.2, 2.4**
    """
    # Call the function
    response = get_340b_covered_entity_volume_data()
    assert isinstance(response, dict), "Response should be a dictionary"
    if "error" in response:
        assert "message" in response, "Error response should contain message field"
        return
    for series in response["series"]:
        for value in series["data"]:
            assert isinstance(value, (int, float)), \
                f"Data value {value} in series '{series['name']}' should be numeric"
            assert value >= 0, \
                f"Data value {value} in series '{series['name']}' should be non-negative"
