"""Shared fixtures for TenzroClaw tests."""

import json
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def reset_request_id():
    """Reset the global request ID counter before each test."""
    import tools.tenzro_rpc as rpc
    rpc._request_id = 0


@pytest.fixture
def mock_rpc_response():
    """Factory fixture that returns a function to mock RPC responses."""
    def _mock(result, status_code=200):
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": result}
        mock_resp.raise_for_status.return_value = None
        return mock_resp
    return _mock


@pytest.fixture
def mock_rpc_error():
    """Factory fixture that returns a function to mock RPC error responses."""
    def _mock(error_msg, error_code=-32600):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "jsonrpc": "2.0",
            "id": 1,
            "error": {"code": error_code, "message": error_msg},
        }
        mock_resp.raise_for_status.return_value = None
        return mock_resp
    return _mock


@pytest.fixture
def mock_api_response():
    """Factory fixture that returns a function to mock API responses."""
    def _mock(result, status_code=200):
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = result
        mock_resp.raise_for_status.return_value = None
        return mock_resp
    return _mock
