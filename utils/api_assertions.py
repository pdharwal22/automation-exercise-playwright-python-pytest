import requests


def assert_api_response(response: requests.Response, http_status: int, response_code: int, message: str | None = None) -> dict:
    """
    Validate the common Automation Exercise API response structure.

    Args:
        response: requests.Response object.
        http_status: Expected HTTP status code.
        response_code: Expected API responseCode.
        message: Optional expected API message.

    Returns:
        Parsed response JSON.
    """

    assert response.status_code == http_status, f"Expected HTTP status {http_status}, but got {response.status_code}"
    response_data = response.json()

    assert response_data["responseCode"] == response_code, f"Expected responseCode {response_code}, but got {response_data.get('responseCode')}"

    if message is not None:
        assert response_data["message"] == message, f"Expected message '{message}', but got '{response_data.get('message')}'"

    return response_data


