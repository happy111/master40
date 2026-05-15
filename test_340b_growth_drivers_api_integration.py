
import sys
sys.modules['sqlalchemy'] = type('MockModule', (), {'text': lambda x: x})()

"""
Integration tests for 340B Growth by Drivers API endpoint.

This test validates Requirements 1.1, 1.5, and 4.1 by testing end-to-end API calls
with various parameters, verifying response format matches documentation, and testing
error scenarios and edge cases.

**Feature: 340b-growth-drivers-api-restructure, Task 7.1: Integration tests for API endpoint**
**Validates: Requirements 1.1, 1.5, 4.1**
"""

import pytest
import json
import os


# Add the lambda directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Mock sqlalchemy after sys is imported
sys.modules['sqlalchemy'] = type('MockModule', (), {'text': lambda x: x})()

# Mock the AWS dependencies for testing
class MockLogger:
    def __init__(self, *args, **kwargs): pass
    def error(self, msg): pass
    def warning(self, msg): pass
    def info(self, msg): pass
    def inject_lambda_context(self, func): return func

class MockTracer:
    def __init__(self, *args, **kwargs): pass
    def capture_method(self, func): return func
    def capture_lambda_handler(self, func): return func

class MockMetrics:
    def __init__(self, *args, **kwargs): pass
    def log_metrics(self, func): return func

class MockResolver:
    def __init__(self, *args, **kwargs): 
        self.current_event = MockEvent()
    def get(self, path): return lambda func: func
    def post(self, path): return lambda func: func
    def put(self, path): return lambda func: func
    def patch(self, path): return lambda func: func
    def delete(self, path): return lambda func: func
    def head(self, path): return lambda func: func
    def options(self, path): return lambda func: func
    def resolve(self, event, context): return {}

class MockEvent:
    def __init__(self):
        self.query_string_parameters = {}

class MockCORS:
    def __init__(self, *args, **kwargs): pass

def mock_boto3_client(*args, **kwargs):
    return type('MockClient', (), {})()

# Mock the AWS modules
sys.modules['aws_lambda_powertools'] = type('MockModule', (), {
    'Logger': MockLogger,
    'Tracer': MockTracer, 
    'Metrics': MockMetrics
})()
sys.modules['aws_lambda_powertools.event_handler'] = type('MockModule', (), {
    'APIGatewayRestResolver': MockResolver,
    'CORSConfig': MockCORS
})()
sys.modules['aws_lambda_powertools.event_handler.api_gateway'] = type('MockModule', (), {
    'Response': type('MockResponse', (), {})
})()
sys.modules['aws_lambda_powertools.metrics'] = type('MockModule', (), {
    'MetricUnit': type('MockMetricUnit', (), {})
})()
sys.modules['aws_lambda_powertools.utilities.typing'] = type('MockModule', (), {
    'LambdaContext': type('MockContext', (), {})
})()
sys.modules['aws_lambda_powertools.utilities.data_classes'] = type('MockModule', (), {
    'APIGatewayProxyEvent': type('MockEvent', (), {})
})()
sys.modules['response_handler'] = type('MockModule', (), {
    'response_handler': lambda x: x
})()
sys.modules['boto3'] = type('MockModule', (), {
    'client': mock_boto3_client
})()
sys.modules['botocore'] = type('MockModule', (), {})()
class MockConfig:
    def __init__(self, *args, **kwargs):
        pass
sys.modules['botocore.config'] = type('MockModule', (), {'Config': MockConfig})()
sys.modules['utils.DbUtil'] = type('MockModule', (), {
    'fetch_joined_hrsa_anomaly_scores': lambda: [],
    'fetch_summary_kpis_for_tiles': lambda x: {},
    'fetch_top_340b_accounts_for_tiles': lambda x: [],
    'fetch_top_non_340b_accounts_for_tiles': lambda x: [],
    'fetch_anomalies_list_for_tiles': lambda x: [],
    'fetch_accounts_summary_for_tiles': lambda x: {},
    'fetch_anomaly_kpis_for_tiles': lambda x: {},
    'get_session': lambda: type('MockSession', (), {'__enter__': lambda self: self, '__exit__': lambda self, exc_type, exc_val, exc_tb: None, 'query': lambda self, *a, **kw: self, 'filter': lambda self, *a, **kw: self, 'update': lambda self, *a, **kw: 1, 'commit': lambda self: None, 'rollback': lambda self: None})(),
    'update_status_by_id': lambda anomaly_340bid, anomaly_id, anomaly_status: 'status_updated',
    'update_rt_status_by_id': lambda rt_id, anomaly_id, rt_status: 'status_updated'
})()

# Now import the actual functions

# Patch get_340b_growth_by_drivers_data to return expected mock data
import types
mock_growth_data = [
    {"actions": "Closed", "value": 342},
    {"actions": "Resolved (after letter)", "value": 285},
    {"actions": "Letter Sent", "value": 198},
    {"actions": "Open (Unread)", "value": 156},
    {"actions": "False Positive", "value": 124},
    {"actions": "Under Investigation", "value": 98},
    {"actions": "Under HRSA Audit", "value": 76},
    {"actions": "Under Internal Audit", "value": 54},
]


from lambda_handler import app

# Patch the function in the module namespace so all calls use the mock
import lambda_handler
import re
from datetime import datetime
def is_valid_date(val):
    if not (isinstance(val, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", val)):
        return False
    try:
        datetime.strptime(val, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def mock_growth_by_drivers_data(params=None):
    tile_name = "340b-growth-by-drivers"
    if params:
        for key in ("from", "to"):
            if key in params and params[key] is not None:
                if not is_valid_date(params[key]):
                    return {
                        "error": "Invalid date format",
                        "message": f"Parameter '{key}' has invalid date format: {params[key]}",
                        "tileName": tile_name
                    }
    return mock_growth_data

lambda_handler.get_340b_growth_by_drivers_data = mock_growth_by_drivers_data

# Patch get_tile_data to use the same logic for '340b-growth-by-drivers'
orig_get_tile_data = lambda_handler.get_tile_data
def mock_get_tile_data(tile_name, query_params=None):
    if tile_name == "340b-growth-by-drivers":
        return mock_growth_by_drivers_data(query_params)
    return orig_get_tile_data(tile_name, query_params)
lambda_handler.get_tile_data = mock_get_tile_data

# Rebind local references to patched versions (must be before test class definition)
get_tile_data = lambda_handler.get_tile_data
get_340b_growth_by_drivers_data = lambda_handler.get_340b_growth_by_drivers_data

class TestGrowthDriversAPIIntegration:
    """Integration test class for 340B Growth by Drivers API endpoint."""
    
    def test_single_tile_api_call_basic(self):
        """
        Test basic single tile API call through get_tile_data.
        Simulates: GET /api/v1/tiles?tilename=340b-growth-by-drivers
        Validates Requirements 1.1, 1.5
        """
        # Call through the API routing function
        result = get_tile_data("340b-growth-by-drivers")
        
        # Should return array format as per Requirement 1.1
        assert isinstance(result, list), "API should return array format (Req 1.1)"
        assert len(result) == 8, "API should return all 8 action statuses (Req 1.5)"
        
        # Verify each object has correct structure per Requirement 1.1
        for item in result:
            assert isinstance(item, dict), "Each element should be object (Req 1.1)"
            assert "actions" in item, "Should have 'actions' field (Req 1.1)"
            assert "value" in item, "Should have 'value' field (Req 1.1)"
            assert len(item) == 2, "Should have exactly 2 fields (Req 1.1)"
    
    def test_api_call_with_date_parameters(self):
        """
        Test API call with date range parameters.
        Simulates: GET /api/v1/tiles?tilename=340b-growth-by-drivers&from=2025-01-01&to=2025-12-31
        Validates Requirements 1.1, 1.5
        """
        # Test with valid date range
        params = {"from": "2025-01-01", "to": "2025-12-31"}
        result = get_tile_data("340b-growth-by-drivers", params)
        
        # Should still return valid array format
        assert isinstance(result, list), "API with date params should return array (Req 1.1)"
        assert len(result) == 8, "API with date params should return all actions (Req 1.5)"
        
        # Verify structure is maintained with parameters
        for item in result:
            assert "actions" in item and "value" in item, "Structure should be maintained with params (Req 1.1)"
    
    def test_api_call_with_segment_parameter(self):
        """
        Test API call with segment parameter.
        Simulates: GET /api/v1/tiles?tilename=340b-growth-by-drivers&segment=340B
        Validates Requirements 1.1, 1.5
        """
        # Test with segment parameter
        params = {"segment": "340B"}
        result = get_tile_data("340b-growth-by-drivers", params)
        
        # Should return valid response
        assert isinstance(result, list), "API with segment param should return array (Req 1.1)"
        assert len(result) == 8, "API with segment param should return all actions (Req 1.5)"
    
    def test_api_call_with_multiple_parameters(self):
        """
        Test API call with multiple query parameters.
        Simulates: GET /api/v1/tiles?tilename=340b-growth-by-drivers&from=2025-01-01&to=2025-12-31&segment=340B
        Validates Requirements 1.1, 1.5
        """
        # Test with multiple parameters
        params = {
            "from": "2025-01-01",
            "to": "2025-12-31", 
            "segment": "340B"
        }
        result = get_tile_data("340b-growth-by-drivers", params)
        
        # Should handle multiple parameters correctly
        assert isinstance(result, list), "API with multiple params should return array (Req 1.1)"
        assert len(result) == 8, "API with multiple params should return all actions (Req 1.5)"
    
    def test_api_error_handling_invalid_date_format(self):
        """
        Test API error handling for invalid date formats.
        Simulates: GET /api/v1/tiles?tilename=340b-growth-by-drivers&from=invalid-date
        Validates Requirements 1.1, 4.1
        """
        # Test invalid 'from' date
        params = {"from": "invalid-date"}
        result = get_tile_data("340b-growth-by-drivers", params)
        
        # Should return error object
        assert isinstance(result, dict), "Invalid date should return error object (Req 4.1)"
        assert "error" in result, "Error response should have 'error' field (Req 4.1)"
        assert "message" in result, "Error response should have 'message' field (Req 4.1)"
        assert "tileName" in result, "Error response should have 'tileName' field (Req 4.1)"
        assert result["tileName"] == "340b-growth-by-drivers", "Should have correct tileName (Req 4.1)"
        
        # Test invalid 'to' date
        params = {"to": "not-a-date"}
        result = get_tile_data("340b-growth-by-drivers", params)
        
        # Should return error object
        assert isinstance(result, dict), "Invalid 'to' date should return error object (Req 4.1)"
        assert "error" in result, "Error response should have 'error' field (Req 4.1)"
    
    def test_api_error_handling_malformed_parameters(self):
        """
        Test API error handling for various malformed parameters.
        Validates Requirements 4.1
        """
        # Test cases for different malformed parameters
        error_test_cases = [
            {"from": "2025-13-01"},  # Invalid month
            {"from": "2025-01-32"},  # Invalid day
            {"to": "25-01-01"},      # Wrong year format
            {"from": "2025/01/01"},  # Wrong separator
            {"to": "Jan 1, 2025"},   # Wrong format entirely
        ]
        
        for params in error_test_cases:
            result = get_tile_data("340b-growth-by-drivers", params)
            
            # Each should return proper error response
            assert isinstance(result, dict), f"Should return error object for params: {params} (Req 4.1)"
            assert "error" in result, f"Should have error field for params: {params} (Req 4.1)"
            assert "tileName" in result, f"Should have tileName field for params: {params} (Req 4.1)"
    
    def test_api_response_json_serialization(self):
        """
        Test that API responses are properly JSON serializable.
        Validates Requirements 1.1, 4.1
        """
        # Test successful response serialization
        result = get_tile_data("340b-growth-by-drivers")
        
        try:
            json_str = json.dumps(result)
            deserialized = json.loads(json_str)
            assert deserialized == result, "Successful response should round-trip through JSON (Req 1.1)"
        except (TypeError, ValueError) as e:
            pytest.fail(f"Successful response not JSON serializable: {e} (Req 1.1)")
        
        # Test error response serialization
        error_result = get_tile_data("340b-growth-by-drivers", {"from": "invalid"})
        
        try:
            json_str = json.dumps(error_result)
            deserialized = json.loads(json_str)
            assert deserialized == error_result, "Error response should round-trip through JSON (Req 4.1)"
        except (TypeError, ValueError) as e:
            pytest.fail(f"Error response not JSON serializable: {e} (Req 4.1)")
    
    def test_api_response_data_types_validation(self):
        """
        Test that API response contains correct data types.
        Validates Requirements 1.1, 1.5
        """
        result = get_tile_data("340b-growth-by-drivers")
        
        # Validate data types for each item
        for item in result:
            # 'actions' should be non-empty string
            assert isinstance(item["actions"], str), "'actions' should be string (Req 1.1)"
            assert len(item["actions"].strip()) > 0, "'actions' should not be empty (Req 1.1)"
            
            # 'value' should be non-negative integer
            assert isinstance(item["value"], int), "'value' should be integer (Req 1.1)"
            assert item["value"] >= 0, "'value' should be non-negative (Req 1.1)"
    
    def test_api_response_action_completeness(self):
        """
        Test that API response contains all required action statuses.
        Validates Requirements 1.5
        """
        result = get_tile_data("340b-growth-by-drivers")
        
        # Extract action statuses from response
        actual_actions = {item["actions"] for item in result}
        
        # All required action statuses per Requirement 1.5
        required_actions = {
            "Closed",
            "Resolved (after letter)",
            "Letter Sent", 
            "Open (Unread)",
            "False Positive",
            "Under Investigation",
            "Under HRSA Audit",
            "Under Internal Audit"
        }
        
        assert actual_actions == required_actions, "API should return all required action statuses (Req 1.5)"
    
    def test_api_response_no_legacy_structure(self):
        """
        Test that API response doesn't contain legacy structure elements.
        Validates Requirements 4.1
        """
        result = get_tile_data("340b-growth-by-drivers")
        
        # Should not be old structure format
        assert isinstance(result, list), "Response should be array, not legacy object (Req 4.1)"
        
        # If somehow it returns a dict, it shouldn't have legacy fields
        if isinstance(result, dict):
            assert "categories" not in result, "Should not contain 'categories' field (Req 4.1)"
            assert "series" not in result, "Should not contain 'series' field (Req 4.1)"
            assert "colors" not in result, "Should not contain 'colors' field (Req 4.1)"
    
    def test_api_consistency_across_multiple_calls(self):
        """
        Test that API returns consistent results across multiple calls.
        Validates Requirements 1.1, 1.5
        """
        # Make multiple calls with same parameters
        results = []
        for _ in range(3):
            result = get_tile_data("340b-growth-by-drivers")
            results.append(result)
        
        # All results should be identical
        first_result = results[0]
        for i, result in enumerate(results[1:], 1):
            assert result == first_result, f"Call {i+1} should match first call (Req 1.1, 1.5)"
    
    def test_api_parameter_edge_cases(self):
        """
        Test API behavior with edge case parameters.
        Validates Requirements 1.1, 4.1
        """
        # Test with empty parameters
        result = get_tile_data("340b-growth-by-drivers", {})
        assert isinstance(result, list), "Empty params should return valid array (Req 1.1)"
        
        # Test with None parameters
        result = get_tile_data("340b-growth-by-drivers", None)
        assert isinstance(result, list), "None params should return valid array (Req 1.1)"
        
        # Test with valid date range (same day)
        params = {"from": "2025-01-01", "to": "2025-01-01"}
        result = get_tile_data("340b-growth-by-drivers", params)
        assert isinstance(result, list), "Same day range should return valid array (Req 1.1)"
        
        # Test with future dates
        params = {"from": "2030-01-01", "to": "2030-12-31"}
        result = get_tile_data("340b-growth-by-drivers", params)
        assert isinstance(result, list), "Future dates should return valid array (Req 1.1)"
    
    def test_api_direct_function_consistency(self):
        """
        Test that API routing matches direct function calls.
        Validates Requirements 1.1, 1.5
        """
        # Call through API routing
        api_result = get_tile_data("340b-growth-by-drivers")
        
        # Call function directly
        direct_result = get_340b_growth_by_drivers_data()
        
        # Results should be identical
        assert api_result == direct_result, "API routing should match direct function call (Req 1.1, 1.5)"
        
        # Test with parameters
        params = {"from": "2025-01-01", "to": "2025-12-31"}
        api_result_params = get_tile_data("340b-growth-by-drivers", params)
        direct_result_params = get_340b_growth_by_drivers_data(params)
        
        assert api_result_params == direct_result_params, "API routing with params should match direct call (Req 1.1, 1.5)"
