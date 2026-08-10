import allure
import pytest
from api.api_client import APIClient
from api.endpoints import APIEndpoints
from conftest import users


@allure.feature("Authentication API")
@allure.story("Verify Login")
@allure.title("Verify Login API with valid credentials")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.regression
def test_verify_login_with_valid_credentials(api_client: APIClient, users: dict):
    valid_user = users["valid_user"]

    with allure.step("Send POST request with valid credentials"):
        response = api_client.post(APIEndpoints.VERIFY_LOGIN, data={"email": valid_user["email"], "password": valid_user["password"]})
    
    with allure.step("Verify the response status code"):
        assert response.status_code == 200

    with allure.step("Verify successful login response"):
        response_data = response.json()
        print(f"Valid Login Response: {response_data}")
        assert response_data["responseCode"] == 200
        assert response_data["message"] == "User exists!"


@allure.feature("Authentication API")
@allure.story("Verify Login")
@allure.title("Verify Login API with invalid credentials")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.regression
def test_verify_login_with_invalid_credentials(api_client: APIClient, users: dict):
    invalid_user = users["invalid_user"]

    with allure.step("Send POST request with invalid credentials"):
        response = api_client.post(APIEndpoints.VERIFY_LOGIN, data={"email": invalid_user["email"], "password": invalid_user["password"]})

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify login failure response"):
        response_data = response.json()
        print(f"Invalid Login Response: {response_data}")
        assert response_data["responseCode"] == 404
        assert response_data["message"] == "User not found!"


@allure.feature("Authentication API")
@allure.story("Verify Login")
@allure.title("Verify Login API without email")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.regression
def test_verify_login_without_email(api_client: APIClient, users: dict):
    without_email_user = users["without_email_user"]

    with allure.step("Send POST request without email"):
        response = api_client.post(APIEndpoints.VERIFY_LOGIN, data={"password": without_email_user["password"]})

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify login failure response"):
        response_data = response.json()
        print(f"Missing Email Login Response: {response_data}")
        assert response_data["responseCode"] == 400
        assert response_data["message"] == "Bad request, email or password parameter is missing in POST request."


@allure.feature("Authentication API")
@allure.story("Verify Login")
@allure.title("Verify Login API without password")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.regression
def test_verify_login_without_password(api_client: APIClient, users: dict):
    without_password_user = users["without_password_user"]

    with allure.step("Send POST request without password"):
        response = api_client.post(APIEndpoints.VERIFY_LOGIN, data={"email": without_password_user["email"]})

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify login failure response"):
        response_data = response.json()
        print(f"Missing Password Login Response: {response_data}")
        assert response_data["responseCode"] == 400
        assert response_data["message"] == "Bad request, email or password parameter is missing in POST request."


@allure.feature("Authentication API")
@allure.story("Verify Login")
@allure.title("Verify Login API rejects DELETE request")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.regression
def test_verify_login_with_delete_request(api_client: APIClient, users: dict):
    valid_user = users["valid_user"]

    with allure.step("Send DELETE request with valid credentials"):
        response = api_client.delete(APIEndpoints.VERIFY_LOGIN, data={"email": valid_user["email"], "password": valid_user["password"]})
    
    with allure.step("Verify the response status code"):
        assert response.status_code == 200

    with allure.step("Verify successful login response"):
        response_data = response.json()
        print(f"Valid Login Response: {response_data}")
        assert response_data["responseCode"] == 405
        assert response_data["message"] == "This request method is not supported."

