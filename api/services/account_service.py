import requests
from typing import Any
from api.api_client import APIClient
from api.endpoints import APIEndpoints

class AccountService:
    """
    Service layer for Automation Exercise account APIs.
    """
    def __init__(self, api_client: APIClient):
        self.api_client = api_client


    def create_account(self, account_data: dict[str, Any]) -> requests.Response:
        return self.api_client.post(APIEndpoints.CREATE_ACCOUNT, data=account_data)


    def get_user_details(self, email: str) -> requests.Response:
        return self.api_client.get(APIEndpoints.GET_USER_DETAIL, params={"email": email})


    def update_account(self, account_data: dict[str, Any]) -> requests.Response:
        return self.api_client.put(APIEndpoints.UPDATE_ACCOUNT, data=account_data)


    def delete_account(self, email: str, password: str) -> requests.Response:
        return self.api_client.delete(APIEndpoints.DELETE_ACCOUNT, data={"email": email, "password": password})

