import requests
from api.api_client import APIClient
from api.endpoints import APIEndpoints

class BrandsService:
    """Service layer for Brands API operations."""

    def __init__(self, api_client: APIClient):
        self.api_client = api_client


    def get_brands(self) -> requests.Response:
        return self.api_client.get(APIEndpoints.BRANDS_LIST)


    def get_brands_with_post(self) -> requests.Response:
        return self.api_client.post(APIEndpoints.BRANDS_LIST)

