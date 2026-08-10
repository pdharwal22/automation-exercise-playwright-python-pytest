import allure
import pytest
from api.api_client import APIClient
from api.endpoints import APIEndpoints


@allure.feature("Products API")
@allure.story("Get Products List")
@allure.title("Verify products list API")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.regression
def test_get_products_list(api_client: APIClient):
    with allure.step("Send GET request for products list"):
        response = api_client.get(APIEndpoints.PRODUCTS_LIST)

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify response contains products"):
        response_data = response.json()
        print(f"Products Response: {response_data}")
        assert "products" in response_data
        assert len(response_data["products"]) > 0


@allure.feature("Products API")
@allure.story("POST Products List")
@allure.title("Verify products list rejects unsupported HTTP method")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.regression
def test_products_list_with_post_method(api_client: APIClient):
    with allure.step("Send POST request for products list"):
        response = api_client.post(APIEndpoints.PRODUCTS_LIST)

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify response contains error message"):
        response_data = response.json()
        print(f"Products Response: {response_data}")
        assert response_data["responseCode"] == 405
        assert response_data["message"] == "This request method is not supported."


@allure.feature("Products API")
@allure.story("Search Product")
@allure.title("Verify product search API")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.regression
def test_search_product(api_client: APIClient):
    with allure.step("Send POST request to search for product"):
        response = api_client.post(APIEndpoints.SEARCH_PRODUCT, data={"search_product": "Blue Top"})

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify response code"):
        response_data = response.json()
        print(f"Search Product Response: {response_data}")
        assert response_data["responseCode"] == 200

    with allure.step("Verify response contains products"):
        assert "products" in response_data
        assert len(response_data["products"]) > 0

    with allure.step("Verify searched product is returned"):
        products = response_data["products"]
        product_names = [product["name"] for product in products]
        assert "Blue Top" in product_names


@allure.feature("Products API")
@allure.story("Search Product")
@allure.title("Verify search with non-existent product")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.regression
def test_search_nonexistent_product(api_client: APIClient):
    product_name = "Nonexistent Product Automation"

    with allure.step("Send POST request with non-existent product"):
        response = api_client.post(APIEndpoints.SEARCH_PRODUCT, data={"search_product": product_name})

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify no product is returned"):
        response_data = response.json()
        print(f"Non-existent Product Response: {response_data}")
        assert response_data["responseCode"] == 200
        assert "products" in response_data
        assert len(response_data["products"]) == 0


@allure.feature("Products API")
@allure.story("Search Product")
@allure.title("Verify search product without search parameter")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.regression
def test_search_product_without_parameter(api_client: APIClient):
    with allure.step("Send POST request without search_product parameter"):
        response = api_client.post(APIEndpoints.SEARCH_PRODUCT)

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify bad request response"):
        response_data = response.json()
        print(f"Missing Search Parameter Response: {response_data}")
        assert response_data["responseCode"] == 400
        assert response_data["message"] == "Bad request, search_product parameter is missing in POST request."

