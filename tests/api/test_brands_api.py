import allure
import pytest
from api.api_client import APIClient
from api.endpoints import APIEndpoints


@allure.feature("Brands API")
@allure.story("Get Brands List")
@allure.title("Verify brands list API")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.regression
def test_get_brands_list(api_client: APIClient):
    with allure.step("Send GET request for brands list"):
        response = api_client.get(APIEndpoints.BRANDS_LIST)

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify response contains brands"):
        response_data = response.json()
        print(f"Brands Response: {response_data}")
        assert response_data["responseCode"] == 200
        assert "brands" in response_data
        assert len(response_data["brands"]) > 0


@allure.feature("Brands API")
@allure.story("Get Brands List")
@allure.title("Verify brands response structure")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.regression
def test_validate_brands_response_structure(api_client: APIClient):
    with allure.step("Send GET request for brands list"):
        response = api_client.get(APIEndpoints.BRANDS_LIST)

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Validate brand response structure"):
        response_data = response.json()
        print(f"Brands Response: {response_data}")

        brands = response_data["brands"]
        assert isinstance(brands, list)
        assert len(brands) > 0

        for brand in brands:
            assert isinstance(brand, dict)
            assert "id" in brand
            assert "brand" in brand
            assert isinstance(brand["id"], int)
            assert isinstance(brand["brand"], str)
            assert brand["brand"].strip() != ""


@allure.feature("Brands API")
@allure.story("POST Brands List")
@allure.title("Verify brands list rejects unsupported HTTP method")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.regression
def test_brands_list_with_post_method(api_client: APIClient):
    with allure.step("Send POST request for brands list"):
        response = api_client.post(APIEndpoints.BRANDS_LIST)

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify unsupported method response"):
        response_data = response.json()
        print(f"Unsupported Method Response: {response_data}")
        assert response_data["responseCode"] == 405
        assert response_data["message"] == "This request method is not supported."

