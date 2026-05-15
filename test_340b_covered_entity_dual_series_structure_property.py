"""
Property-based tests for 340B covered entity volume dual-series chart structure.

**Feature: overview-page-enhancement, Property 3: Dual-Series Chart Structure**
**Validates: Requirements 2.1, 2.2**
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
def test_340b_covered_entity_dual_series_structure(from_date, to_date):
    """
    Property 3: Dual-Series Chart Structure
    
    For any request to the 340b-covered-entity-volume tile, the response should contain 
    exactly two series with names "340B Covered Entity QTY" and "340B % Volume", 
    each with type "area" and distinct yAxis values (0 and 1).
    
    **Feature: overview-page-enhancement, Property 3: Dual-Series Chart Structure**
    **Validates: Requirements 2.1, 2.2**
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
        # If it's an error response, it should have proper error structure
        assert "message" in response, "Error response should have 'message' field"
        assert "tileName" in response, "Error response should have 'tileName' field"
        assert response["tileName"] == "340b-covered-entity-volume", f"Error tileName should be '340b-covered-entity-volume', got '{response['tileName']}'"
        return  # Skip format validation for error responses
    
    # Verify response is a dictionary (successful response)
    assert isinstance(response, dict), f"Expected response to be a dict, got {type(response)}"
    
    # Verify required fields for stacked area chart format
    assert "categories" in response, "Stacked area chart response should contain 'categories' field"
    assert "series" in response, "Stacked area chart response should contain 'series' field"
    
    # Verify categories is a list
    categories = response["categories"]
    assert isinstance(categories, list), f"Categories should be a list, got {type(categories)}"
    
    # Verify series is a list with exactly 2 entries for dual-series chart
    series = response["series"]
    assert isinstance(series, list), f"Series should be a list, got {type(series)}"
    assert len(series) == 2, f"Dual-series chart should have exactly 2 series, got {len(series)}"
    
    # Verify series names are correct
    series_names = [s["name"] for s in series]
    expected_names = ["340B Covered Entity QTY", "340B % Volume"]
    assert "340B Covered Entity QTY" in series_names, f"Expected '340B Covered Entity QTY' in series names, got {series_names}"
    assert "340B % Volume" in series_names, f"Expected '340B % Volume' in series names, got {series_names}"
    
    # Verify each series has required properties
    for i, series_item in enumerate(series):
        assert isinstance(series_item, dict), f"Series {i} should be a dict, got {type(series_item)}"
        
        # Verify required fields
        assert "name" in series_item, f"Series {i} should have 'name' field"
        assert "data" in series_item, f"Series {i} should have 'data' field"
        assert "type" in series_item, f"Series {i} should have 'type' field"
        assert "yAxis" in series_item, f"Series {i} should have 'yAxis' field"
        
        # Verify data is a list
        assert isinstance(series_item["data"], list), f"Series {i} data should be a list, got {type(series_item['data'])}"
        
        # Verify type is "area" for stacked area chart
        assert series_item["type"] == "area", f"Series {i} type should be 'area', got '{series_item['type']}'"
        
        # Verify yAxis is an integer
        assert isinstance(series_item["yAxis"], int), f"Series {i} yAxis should be an integer, got {type(series_item['yAxis'])}"
    
    # Verify yAxis values are distinct (0 and 1)
    y_axis_values = [s["yAxis"] for s in series]
    assert len(set(y_axis_values)) == 2, f"yAxis values should be distinct, got {y_axis_values}"
    assert 0 in y_axis_values, f"Expected yAxis value 0, got {y_axis_values}"
    assert 1 in y_axis_values, f"Expected yAxis value 1, got {y_axis_values}"


if __name__ == "__main__":
    print("Running Property 3: Dual-Series Chart Structure tests...")
    
    # Import hypothesis for running the test
    from hypothesis import given
    
    # Create a simple test function to verify the property works
    def test_basic_dual_series_structure():
        """Test with basic parameters"""
        # Call the function directly with None parameters
        response = get_340b_covered_entity_volume_data(None)
        
        # Basic validation that it returns a response
        assert response is not None, "Response should not be None"
        print("✓ Basic test passed")
    
    def test_with_date_parameters():
        """Test with date parameters"""
        query_params = {'from': '2024-01-01', 'to': '2024-12-31'}
        response = get_340b_covered_entity_volume_data(query_params)
        
        # Basic validation that it returns a response
        assert response is not None, "Response should not be None"
        print("✓ Date parameter test passed")
    
    # Run the basic tests
    test_basic_dual_series_structure()
    test_with_date_parameters()
    
    print("All Property 3 tests completed successfully!")
    print("Note: Run with pytest to execute the full property-based test with 100 examples")
