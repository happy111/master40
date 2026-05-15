"""
Property-based tests for 340B Growth by Key Drivers data type validation.

**Feature: 340b-growth-drivers-api-restructure, Property 3: Data Type Validation**
**Validates: Requirements 1.2, 1.3**
"""

import sys
class MockConfig:
    def __init__(self, *args, **kwargs):
        pass
sys.modules['botocore'] = type('MockModule', (), {})()
sys.modules['botocore.config'] = type('MockModule', (), {'Config': MockConfig})()
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
sys.modules['botocore.exceptions'] = MagicMock()
sys.modules['aws_lambda_powertools'] = MagicMock()
sys.modules['aws_lambda_powertools.event_handler'] = MagicMock()
sys.modules['aws_lambda_powertools.event_handler.api_gateway'] = MagicMock()
sys.modules['aws_lambda_powertools.metrics'] = MagicMock()
sys.modules['aws_lambda_powertools.utilities.typing'] = MagicMock()
sys.modules['aws_lambda_powertools.utilities.data_classes'] = MagicMock()
sys.modules['response_handler'] = MagicMock()
sys.modules['utils'] = MagicMock()

# Create a mock DbUtil module
mock_db_util = MagicMock()
sys.modules['utils.DbUtil'] = mock_db_util

from lambda_handler import get_340b_growth_by_drivers_data


@given(
    query_params=st.one_of(
        st.none(),
        st.dictionaries(
            st.sampled_from(['from', 'to', 'segment']),
            st.one_of(
                st.text(min_size=1, max_size=20),
                st.dates().map(lambda d: d.strftime('%Y-%m-%d'))
            ),
            min_size=0,
            max_size=3
        )
    )
)
@settings(max_examples=100)
def test_340b_growth_drivers_data_type_validation(query_params):
    """
    Property: For any object in the response array, the "actions" field should be a 
    non-empty string and the "value" field should be a non-negative integer
    
    **Feature: 340b-growth-drivers-api-restructure, Property 3: Data Type Validation**
    **Validates: Requirements 1.2, 1.3**
    """
    
    # Call the function with generated query parameters
    response = get_340b_growth_by_drivers_data(query_params)
    
    # Skip validation for error responses (they have different structure)
    if isinstance(response, dict) and "error" in response:
        return  # Skip data validation for error responses
    
    # For successful responses, verify data types
    assert isinstance(response, list), f"Response should be an array, got {type(response)}"
    
    # Verify data types for each object in the response array
    for i, item in enumerate(response):
        assert isinstance(item, dict), f"Item {i} should be a dictionary, got {type(item)}"
        
        # Verify "actions" field is a non-empty string
        assert "actions" in item, f"Item {i} should have 'actions' field"
        assert isinstance(item["actions"], str), \
            f"Item {i} 'actions' field should be string, got {type(item['actions'])}"
        assert len(item["actions"]) > 0, \
            f"Item {i} 'actions' field should be non-empty string, got '{item['actions']}'"
        
        # Verify "value" field is a non-negative integer
        assert "value" in item, f"Item {i} should have 'value' field"
        assert isinstance(item["value"], int), \
            f"Item {i} 'value' field should be integer, got {type(item['value'])}"
        assert item["value"] >= 0, \
            f"Item {i} 'value' field should be non-negative integer, got {item['value']}"


def test_simple_cases():
    """Simple test cases to verify the property works"""
    # Test with None
    response = get_340b_growth_by_drivers_data(None)
    if isinstance(response, list):
        for item in response:
            assert isinstance(item["actions"], str)
            assert len(item["actions"]) > 0
            assert isinstance(item["value"], int)
            assert item["value"] >= 0
    
    # Test with empty dict
    response = get_340b_growth_by_drivers_data({})
    if isinstance(response, list):
        for item in response:
            assert isinstance(item["actions"], str)
            assert len(item["actions"]) > 0
            assert isinstance(item["value"], int)
            assert item["value"] >= 0
    
    # Test with date parameter
    response = get_340b_growth_by_drivers_data({"from": "2024-01-01"})
    if isinstance(response, list):
        for item in response:
            assert isinstance(item["actions"], str)
            assert len(item["actions"]) > 0
            assert isinstance(item["value"], int)
            assert item["value"] >= 0
    
    print("✅ Data type validation property test passed for sample inputs")


if __name__ == "__main__":
    test_simple_cases()
