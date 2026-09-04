from typing import Any
import requests
from api.api_client import APIClient
from api.endpoints import APIEndpoints

class ProductService:
    """Service layer for Products API operations."""

    def __init__(self, api_client: APIClient):
        self.api_client = api_client


    def get_products(self) -> requests.Response:
        return self.api_client.get(APIEndpoints.PRODUCTS_LIST)


    def search_product(self, product_name: str) -> requests.Response:
        return self.api_client.post(APIEndpoints.SEARCH_PRODUCT, data={"search_product": product_name})


    def search_product_without_parameter(self) -> requests.Response:
        return self.api_client.post(APIEndpoints.SEARCH_PRODUCT)


    def get_products_with_post(self) -> requests.Response:
        return self.api_client.post(APIEndpoints.PRODUCTS_LIST)

