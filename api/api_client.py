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


    def get(self, endpoint: str, params: dict[str, Any] | None=None) -> requests.Response:
        return self.session.get(url=f"{self.base_url}{endpoint}", params=params)


    def post(self, endpoint: str, data: dict[str, Any] | None=None, params: dict[str, Any] | None=None) -> requests.Response:
        return self.session.post(url=f"{self.base_url}{endpoint}", data=data, params=params)


    def put(self, endpoint: str, data: dict[str, Any] | None=None, params: dict[str, Any] | None=None) -> requests.Response:
        return self.session.put(url=f"{self.base_url}{endpoint}", data=data, params=params)


    def delete(self, endpoint: str, data: dict[str, Any] | None=None, params: dict[str, Any] | None=None) -> requests.Response:
        return self.session.delete(url=f"{self.base_url}{endpoint}", data=data, params=params)


    def close(self):
        self.session.close()

