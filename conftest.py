# lambda/tests_v2/conftest.py
"""
Pytest configuration for lambda tests.

Handles mocking of dependencies that are not available in the test environment
(pandas, sqlalchemy, boto3, etc.) using pytest hooks for proper scoping.
"""
import sys
import os
import importlib.util
import pytest
from unittest.mock import MagicMock

# Add parent directory (lambda/) to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Pre-load utils.utils_helper as a real module (no external deps) so that
# lambda_handler receives real create_error_response / validate_optional_param / filter functions.
_LAMBDA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
def _load_real_module(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules[module_name] = mod

_load_real_module('utils.utils_helper', os.path.join(_LAMBDA_DIR, 'utils', 'utils_helper.py'))

# Store original modules to restore later
_original_modules = {}
_mocked = False

MODULES_TO_MOCK = [
    'pandas',
    'sqlalchemy',
    'sqlalchemy.orm',
    'sqlalchemy.engine',
    'boto3',
    # Note: Do NOT mock botocore - CDK tests need botocore.exceptions to work
    # Lambda handler only imports botocore.config.Config which works fine with real botocore
    'aws_lambda_powertools',
    'aws_lambda_powertools.event_handler',
    'aws_lambda_powertools.event_handler.api_gateway',
    'aws_lambda_powertools.metrics',
    'aws_lambda_powertools.utilities',
    'aws_lambda_powertools.utilities.typing',
    'aws_lambda_powertools.utilities.data_classes',
    'response_handler',
    'utils',
    'utils.DbUtil',
    'utils.query_templates',
]


def _create_passthrough_decorator(*args, **kwargs):
    """Create a decorator that passes through the original function."""
    def decorator(func):
        return func
    return decorator


def _create_api_gateway_resolver_mock(*args, **kwargs):
    """Create a mock APIGatewayRestResolver that passes through decorated functions."""
    mock_resolver = MagicMock()
    # Make route decorators pass through the original function
    mock_resolver.get = _create_passthrough_decorator
    mock_resolver.post = _create_passthrough_decorator
    mock_resolver.put = _create_passthrough_decorator
    mock_resolver.delete = _create_passthrough_decorator
    mock_resolver.patch = _create_passthrough_decorator
    return mock_resolver


def _create_tracer_mock():
    """Create a mock Tracer that passes through decorated functions."""
    mock_tracer = MagicMock()
    mock_tracer.capture_method = lambda func: func
    mock_tracer.capture_lambda_handler = lambda func: func
    return mock_tracer


def _mock_lambda_dependencies():
    """Mock all lambda dependencies before importing lambda_handler."""
    global _mocked
    if _mocked:
        return
        
    for mod_name in MODULES_TO_MOCK:
        if mod_name in sys.modules:
            _original_modules[mod_name] = sys.modules[mod_name]
        sys.modules[mod_name] = MagicMock()
    
    # Configure APIGatewayRestResolver to pass through decorated functions
    # Note: lambda_handler imports from 'aws_lambda_powertools.event_handler'
    event_handler_mock = sys.modules['aws_lambda_powertools.event_handler']
    event_handler_mock.APIGatewayRestResolver = _create_api_gateway_resolver_mock
    event_handler_mock.CORSConfig = MagicMock
    
    # Also set on api_gateway submodule for any direct imports
    api_gateway_mock = sys.modules['aws_lambda_powertools.event_handler.api_gateway']
    api_gateway_mock.APIGatewayRestResolver = _create_api_gateway_resolver_mock
    api_gateway_mock.Response = MagicMock
    
    # Configure Tracer to pass through decorated functions
    powertools_mock = sys.modules['aws_lambda_powertools']
    powertools_mock.Tracer = _create_tracer_mock
    powertools_mock.Logger = MagicMock
    powertools_mock.Metrics = MagicMock
    
    _mocked = True


def _restore_modules():
    """Restore original modules after tests complete."""
    global _mocked
    if not _mocked:
        return
        
    for mod_name in MODULES_TO_MOCK:
        if mod_name in _original_modules:
            sys.modules[mod_name] = _original_modules[mod_name]
        elif mod_name in sys.modules:
            del sys.modules[mod_name]
    
    _original_modules.clear()
    _mocked = False


def pytest_configure(config):
    """Called after command line options are parsed, before collection."""
    # Only mock if we're running tests from this directory
    _mock_lambda_dependencies()


def pytest_unconfigure(config):
    """Called before test session ends."""
    _restore_modules()
