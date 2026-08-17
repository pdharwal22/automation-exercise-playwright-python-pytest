from typing import Any
import requests


class APIClient:
    """
    Reusable HTTP client for API automation.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        })


    def _request(self, method: str, endpoint: str, data: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return self.session.request(method=method, url=url, data=data, params=params)


    def get(self, endpoint: str, params: dict[str, Any] | None=None):
        return self._request(method="GET", endpoint=endpoint, params=params)


    def post(self, endpoint: str, data: dict[str, Any] | None=None, params: dict[str, Any] | None=None):
        return self._request(method="POST", endpoint=endpoint, data=data, params=params)


    def put(self, endpoint: str, data: dict[str, Any] | None=None, params: dict[str, Any] | None=None):
        return self._request(method="PUT", endpoint=endpoint, data=data, params=params)


    def delete(self, endpoint: str, data: dict[str, Any] | None=None, params: dict[str, Any] | None=None):
        return self._request(method="DELETE", endpoint=endpoint, data=data, params=params)


    def close(self):
        self.session.close()

