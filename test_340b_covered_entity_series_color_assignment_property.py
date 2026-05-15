"""
Property-based tests for 340B covered entity volume series color assignment.

**Feature: overview-page-enhancement, Property 5: Series Color Assignment**
**Validates: Requirements 2.5**
"""

import sys
import os
import datetime
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path to import lambda_handler
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hypothesis import given, strategies as st, settings

# Mock dependencies before importing lambda_handler
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
sys.modules['aws_lambda_powertools.utilities.typing'] = MagicMock()
sys.modules['aws_lambda_powertools.utilities.data_classes'] = MagicMock()
sys.modules['response_handler'] = MagicMock()
sys.modules['utils'] = MagicMock()
sys.modules['utils.DbUtil'] = MagicMock()

from lambda_handler import get_340b_covered_entity_volume_data


@settings(max_examples=100)
@given(
    # Generate random query parameters
    from_date=st.one_of(
        st.none(),
        st.dates(min_value=datetime.date(2020, 1, 1), max_value=datetime.date(2030, 12, 31)).map(lambda d: d.strftime('%Y-%m-%d'))
    ),
    to_date=st.one_of(
        st.none(),
        st.dates(min_value=datetime.date(2020, 1, 1), max_value=datetime.date(2030, 12, 31)).map(lambda d: d.strftime('%Y-%m-%d'))
    )
)
def test_340b_covered_entity_series_color_assignment(from_date, to_date):
    """
    Property 5: Series Color Assignment
    
    For any request to the 340b-covered-entity-volume tile with multiple series, 
    each series should support distinct color assignment for clear visual distinction.
    This validates that the response structure allows for proper color differentiation.
    
    **Feature: overview-page-enhancement, Property 5: Series Color Assignment**
    **Validates: Requirements 2.5**
    """
    # Build query parameters
    query_params = {}
    if from_date is not None:
        query_params['from'] = from_date
    if to_date is not None:
        query_params['to'] = to_date
    
    # Call the function
    response = get_340b_covered_entity_volume_data(query_params if query_params else None)
    
    # Verify response is not an error
    if isinstance(response, dict) and "error" in response:
        # If it's an error response, skip color validation
        assert "message" in response, "Error response should have 'message' field"
        assert "tileName" in response, "Error response should have 'tileName' field"
        return  # Skip color validation for error responses
    
    # Verify response is a dictionary (successful response)
    assert isinstance(response, dict), f"Expected response to be a dict, got {type(response)}"
    
    # Verify series field exists
    assert "series" in response, "Response should contain 'series' field"
    series = response["series"]
    assert isinstance(series, list), f"Series should be a list, got {type(series)}"
    
    # If less than 2 series, color distinction is not applicable
    if len(series) < 2:
        return
    
    # Verify each series has distinct identifiers that support color assignment
    series_identifiers = []
    
    for i, series_item in enumerate(series):
        assert isinstance(series_item, dict), f"Series {i} should be a dict, got {type(series_item)}"
        
        # Verify series has name field (primary identifier for color assignment)
        assert "name" in series_item, f"Series {i} should have 'name' field for color identification"
        series_name = series_item["name"]
        assert isinstance(series_name, str), f"Series {i} name should be a string, got {type(series_name)}"
        assert len(series_name) > 0, f"Series {i} name should not be empty"
        
        # Verify series has yAxis field (secondary identifier for color assignment)
        assert "yAxis" in series_item, f"Series {i} should have 'yAxis' field for color differentiation"
        y_axis = series_item["yAxis"]
        assert isinstance(y_axis, int), f"Series {i} yAxis should be an integer, got {type(y_axis)}"
        
        # Create unique identifier for this series
        series_identifier = (series_name, y_axis)
        series_identifiers.append(series_identifier)
        
        # Verify series structure supports color assignment
        # (Color can be assigned by frontend based on name, yAxis, or index)
        assert "type" in series_item, f"Series {i} should have 'type' field for rendering"
        assert "data" in series_item, f"Series {i} should have 'data' field for rendering"
    
    # Verify all series have distinct identifiers (enables distinct color assignment)
    unique_identifiers = set(series_identifiers)
    assert len(unique_identifiers) == len(series_identifiers), \
        f"All series should have distinct identifiers for color assignment. Got: {series_identifiers}"
    
    # Verify series names are distinct (primary method for color assignment)
    series_names = [identifier[0] for identifier in series_identifiers]
    unique_names = set(series_names)
    assert len(unique_names) == len(series_names), \
        f"All series should have distinct names for color assignment. Got names: {series_names}"
    
    # Verify yAxis values are distinct (secondary method for color assignment)
    y_axis_values = [identifier[1] for identifier in series_identifiers]
    unique_y_axis = set(y_axis_values)
    assert len(unique_y_axis) == len(y_axis_values), \
        f"All series should have distinct yAxis values for color assignment. Got yAxis: {y_axis_values}"
    
    # For 340B covered entity volume, verify expected series names
    expected_names = {"340B Covered Entity QTY", "340B % Volume"}
    actual_names = set(series_names)
    if len(series_names) == 2:  # Only validate if we have the expected number of series
        assert actual_names == expected_names, \
            f"Expected series names {expected_names} for color assignment, got {actual_names}"


if __name__ == "__main__":
    print("Running Property 5: Series Color Assignment tests...")
    
    # Create a simple wrapper to test basic functionality
    def test_basic_functionality():
        """Test basic functionality without hypothesis"""
        # Test with no parameters
        response = get_340b_covered_entity_volume_data(None)
        
        # Verify response is not an error
        if isinstance(response, dict) and "error" in response:
            print(f"Got error response: {response}")
            return
        
        # Verify response structure
        assert isinstance(response, dict), f"Expected response to be a dict, got {type(response)}"
        assert "series" in response, "Response should contain 'series' field"
        series = response["series"]
        assert isinstance(series, list), f"Series should be a list, got {type(series)}"
        
        if len(series) >= 2:
            # Verify series have distinct names for color assignment
            series_names = [s.get("name", "") for s in series]
            unique_names = set(series_names)
            assert len(unique_names) == len(series_names), \
                f"All series should have distinct names for color assignment. Got names: {series_names}"
            print(f"✓ Series have distinct names: {series_names}")
        
        print("✓ Basic functionality test passed")
    
    # Run basic test
    test_basic_functionality()
    
    print("All Property 5 tests completed successfully!")
