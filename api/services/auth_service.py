from typing import Any
import requests
from api.api_client import APIClient
from api.endpoints import APIEndpoints

class AuthService:
    """
    Service layer for Authentication API operations.
    """
    def __init__(self, api_client: APIClient):
        self.api_client = api_client


    def verify_login(self, email: str | None=None, password: str | None=None) -> requests.Response:
        data: dict[str, Any] = {}
        if email is not None:
            data["email"] = email

        if password is not None:
            data["password"] = password

        return self.api_client.post(APIEndpoints.VERIFY_LOGIN, data=data)


    def delete_account(self, email: str | None=None, password: str | None=None) -> requests.Response:
        data: dict[str, Any] = {}
        if email is not None:
            data["email"] = email

        if password is not None:
            data["password"] = password

        return self.api_client.delete(APIEndpoints.DELETE_ACCOUNT, data=data)

