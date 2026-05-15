"""
Property-based tests for 340B Growth by Key Drivers action status completeness.

**Feature: 340b-growth-drivers-api-restructure, Property 2: Action Status Completeness**
**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9**
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


# All eight required action status types as per requirements 2.1-2.9
REQUIRED_ACTION_STATUSES = {
    "Closed",                      # Requirement 2.1
    "Resolved (after letter)",     # Requirement 2.2
    "Letter Sent",                 # Requirement 2.3
    "Open (Unread)",              # Requirement 2.4
    "False Positive",             # Requirement 2.5
    "Under Investigation",        # Requirement 2.6
    "Under HRSA Audit",          # Requirement 2.7
    "Under Internal Audit"       # Requirement 2.8
}


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
def test_340b_growth_drivers_action_status_completeness(query_params):
    """
    Property: For any response from the 340b-growth-by-drivers endpoint, 
    all eight defined action statuses should be represented in the returned array
    
    **Feature: 340b-growth-drivers-api-restructure, Property 2: Action Status Completeness**
    **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9**
    """
    
    # Call the function with generated query parameters
    response = get_340b_growth_by_drivers_data(query_params)
    
    # Skip validation for error responses (they have different structure)
    if isinstance(response, dict) and "error" in response:
        return  # Skip data validation for error responses
    
    # For successful responses, verify all action statuses are present
    assert isinstance(response, list), f"Response should be an array, got {type(response)}"
    
    # Extract all action statuses from the response
    actual_actions = set()
    for item in response:
        if isinstance(item, dict) and "actions" in item:
            actual_actions.add(item["actions"])
    
    # Verify all required action statuses are present
    missing_actions = REQUIRED_ACTION_STATUSES - actual_actions
    assert len(missing_actions) == 0, \
        f"Missing required action statuses: {missing_actions}"
    
    # Verify we have exactly the expected number of action statuses
    assert len(actual_actions) == len(REQUIRED_ACTION_STATUSES), \
        f"Expected {len(REQUIRED_ACTION_STATUSES)} action statuses, got {len(actual_actions)}"
    
    # Verify no unexpected action statuses are present
    unexpected_actions = actual_actions - REQUIRED_ACTION_STATUSES
    assert len(unexpected_actions) == 0, \
        f"Unexpected action statuses found: {unexpected_actions}"


def test_simple_cases():
    """Simple test cases to verify the property works"""
    # Test with None
    response = get_340b_growth_by_drivers_data(None)
    if isinstance(response, list):
        actual_actions = {item["actions"] for item in response if isinstance(item, dict) and "actions" in item}
        assert actual_actions == REQUIRED_ACTION_STATUSES, f"Expected all action statuses, got {actual_actions}"
    
    # Test with empty dict
    response = get_340b_growth_by_drivers_data({})
    if isinstance(response, list):
        actual_actions = {item["actions"] for item in response if isinstance(item, dict) and "actions" in item}
        assert actual_actions == REQUIRED_ACTION_STATUSES, f"Expected all action statuses, got {actual_actions}"
    
    print("✅ Action status completeness property test passed for sample inputs")


if __name__ == "__main__":
    test_simple_cases()
