import requests
from unittest.mock import Mock, patch

from healthcheck.checker import check_endpoint

@patch("healthcheck.checker.requests.get")
def test_healthy_endpoint_returns_pass(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    result = check_endpoint(
        name="Onyx API",
        url="https://example.com/health"
    )

    assert result["name"] == "Onyx API"
    assert result["healthy"] is True
    assert result["status_code"] == 200

@patch("healthcheck.checker.requests.get")
def test_unhealthy_endpoint_returns_fail(mock_get):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    result = check_endpoint(
        name="Onyx API",
        url="https://example.com/health"
    )

    assert result["name"] == "Onyx API"
    assert result["healthy"] is False
    assert result["status_code"] == 500

@patch("healthcheck.checker.requests.get")
def test_timeout_returns_unhealthy_result(mock_get):
    mock_get.side_effect = requests.Timeout()

    result = check_endpoint(
        name="Onyx API",
        url="https://example.com/health"
    )

    assert result["name"] == "Onyx API"
    assert result["healthy"] is False
    assert result["status_code"] is None
    assert result["message"] == "Request timed out"

@patch("healthcheck.checker.requests.get")
def test_connection_error_returns_unhealthy_result(mock_get):
    mock_get.side_effect = requests.ConnectionError()

    result = check_endpoint(
        name="Onyx API",
        url="https://example.com/health"
    )

    assert result["name"] == "Onyx API"
    assert result["healthy"] is False
    assert result["status_code"] is None
    assert result["message"] == "Connection failed"

@patch("healthcheck.checker.requests.get")
def test_healthy_endpoint_returns_response_time(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    result = check_endpoint(
        name="Onyx API",
        url="https://example.com/health"
    )

    assert "response_time_ms" in result
    assert isinstance(result["response_time_ms"], int)
    assert result["response_time_ms"] >= 0