import allure
import pytest
from api.api_client import APIClient
from api.endpoints import APIEndpoints
from utils.test_data_generator import generate_unique_email
from utils.test_data_loader import TestDataLoader


@pytest.fixture
def account_user():
    users = TestDataLoader.load_json("users.json")
    user = users["account_user"].copy()
    # Generate a unique email for every execution
    user["email"] = generate_unique_email()
    return user


@allure.feature("Account API")
@allure.story("Create Account")
@allure.title("Verify account creation with valid user credentials")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.regression
def test_create_account(api_client: APIClient, account_user: dict):
    with allure.step("Send POST request to create account"):
        response = api_client.post(APIEndpoints.CREATE_ACCOUNT, data=account_user)

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify account creation response"):
        response_data = response.json()
        print(f"Create Account Response: {response_data}")
        assert response_data["responseCode"] == 201
        assert response_data["message"] == "User created!"


@allure.feature("Account API")
@allure.story("Get User Details")
@allure.title("Verify user details can be retrieved by email")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.regression
def test_get_user_details(api_client: APIClient, account_user: dict):
    # The account must already exist before retrieving its details.
    with allure.step("Create account"):
        create_response = api_client.post(APIEndpoints.CREATE_ACCOUNT, data=account_user)
        assert create_response.status_code == 200

        create_response_data = create_response.json()
        assert create_response_data["responseCode"] == 201
        assert create_response_data["message"] == "User created!"

    with allure.step("Get user details by email"):
        response = api_client.get(APIEndpoints.GET_USER_DETAIL, params={"email": account_user["email"]})

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify user details"):
        response_data = response.json()
        print(f"Get User Details Response: {response_data}")
        assert response_data["responseCode"] == 200
        assert isinstance(response_data["user"]["id"], int)
        assert response_data["user"]["name"] == account_user["name"]
        assert response_data["user"]["email"] == account_user["email"]
        assert isinstance(response_data["user"]["title"], str)
        assert isinstance(response_data["user"]["birth_day"], str)
        assert isinstance(response_data["user"]["birth_month"], str)
        assert isinstance(response_data["user"]["birth_year"], str)
        assert response_data["user"]["first_name"] == account_user["firstname"]
        assert response_data["user"]["last_name"] == account_user["lastname"]
        assert response_data["user"]["address1"] == account_user["address1"]
        assert response_data["user"]["address2"] == account_user["address2"]
        assert response_data["user"]["country"] == account_user["country"]
        assert response_data["user"]["state"] == account_user["state"]
        assert response_data["user"]["city"] == account_user["city"]
        assert response_data["user"]["zipcode"] == account_user["zipcode"]


@allure.feature("Account API")
@allure.story("Get User Details")
@allure.title("Verify user details retrieval with non-existent email")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.regression
def test_user_details_with_invalid_email(api_client: APIClient):
    invalid_email = "nonexistent_user_automation@example.com"

    with allure.step("Get user details using non-existent email"):
        response = api_client.get(APIEndpoints.GET_USER_DETAIL, params={"email": invalid_email})

    with allure.step("Verify response status code"):
        assert response.status_code == 200

    with allure.step("Verify user not found response"):
        response_data = response.json()
        print(f"Invalid Email Response: {response_data}")
        assert response_data["responseCode"] == 404
        assert response_data["message"] == "Account not found with this email, try another email!"


@allure.feature("Account API")
@allure.story("Update Account")
@allure.title("Verify account details can be updated")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.regression
def test_update_account(api_client: APIClient, account_user: dict, users: dict):
    update_user = users["update_user"]

    with allure.step("Create account for update"):
        create_response = api_client.post(APIEndpoints.CREATE_ACCOUNT, data=account_user)
        assert create_response.status_code == 200

        create_response_data = create_response.json()
        print(f"Create Account Response: {create_response_data}")
        assert create_response_data["responseCode"] == 201
        assert create_response_data["message"] == "User created!"

    with allure.step("Update account details"):
        update_data = {
            "name": update_user["name"],
            "email": account_user["email"],
            "password": account_user["password"],
            "firstname": update_user["firstname"],
            "lastname": update_user["lastname"],
            "company": update_user["company"],
            "address1": update_user["address1"],
            "address2": update_user["address2"],
            "country": update_user["country"],
            "state": update_user["state"],
            "city": update_user["city"],
            "zipcode": update_user["zipcode"],
            "mobile_number": update_user["mobile_number"]
        }
        response = api_client.put(APIEndpoints.UPDATE_ACCOUNT, data=update_data)

    with allure.step("Verify update response"):
        assert response.status_code == 200

        response_data = response.json()
        print(f"Update Account Response: {response_data}")
        assert response_data["responseCode"] == 200
        assert response_data["message"] == "User updated!"


@allure.feature("Account API")
@allure.story("Update Account")
@allure.title("Verify updated account details")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.regression
def test_verify_updated_account_details(api_client: APIClient, account_user: dict, users: dict):
    update_user = users["update_user"]

    with allure.step("Create account"):
        create_response = api_client.post(APIEndpoints.CREATE_ACCOUNT, data=account_user)
        assert create_response.status_code == 200

        create_response_data = create_response.json()
        assert create_response_data["responseCode"] == 201
        assert create_response_data["message"] == "User created!"

    with allure.step("Update account"):
        update_data = {
            "name": update_user["name"],
            "email": account_user["email"],
            "password": account_user["password"],
            "firstname": update_user["firstname"],
            "lastname": update_user["lastname"],
            "company": update_user["company"],
            "address1": update_user["address1"],
            "address2": update_user["address2"],
            "country": update_user["country"],
            "state": update_user["state"],
            "city": update_user["city"],
            "zipcode": update_user["zipcode"],
            "mobile_number": update_user["mobile_number"]
        }
        update_response = api_client.put(APIEndpoints.UPDATE_ACCOUNT, data=update_data)
        assert update_response.status_code == 200

        update_response_data = update_response.json()
        assert update_response_data["responseCode"] == 200
        assert update_response_data["message"] == "User updated!"

    with allure.step("Retrieve updated account details"):
        response = api_client.get(APIEndpoints.GET_USER_DETAIL, params={"email": account_user["email"]})
        assert response.status_code == 200

    with allure.step("Verify updated account details"):
        response_data = response.json()
        print(f"Updated Account Details: {response_data}")
        assert response_data["responseCode"] == 200

        updated_user = response_data["user"]
        assert updated_user["name"] == update_user["name"]
        assert updated_user["email"] == account_user["email"]
        assert updated_user["first_name"] == update_user["firstname"]
        assert updated_user["last_name"] == update_user["lastname"]
        assert updated_user["company"] == update_user["company"]
        assert updated_user["address1"] == update_user["address1"]
        assert updated_user["address2"] == update_user["address2"]
        assert updated_user["country"] == update_user["country"]
        assert updated_user["state"] == update_user["state"]
        assert updated_user["city"] == update_user["city"]
        assert updated_user["zipcode"] == update_user["zipcode"]


@allure.feature("Account API")
@allure.story("Delete Account")
@allure.title("Verify account can be deleted")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.regression
def test_delete_account(api_client: APIClient, account_user: dict):
    with allure.step("Create account for deletion"):
        create_response = api_client.post(APIEndpoints.CREATE_ACCOUNT, data=account_user)
        assert create_response.status_code == 200

        create_response_data = create_response.json()
        print(f"Create Account Response: {create_response_data}")
        assert create_response_data["responseCode"] == 201
        assert create_response_data["message"] == "User created!"

    with allure.step("Delete account"):
        delete_response = api_client.delete(APIEndpoints.DELETE_ACCOUNT, data={"email": account_user["email"], "password": account_user["password"]})
        assert delete_response.status_code == 200

    with allure.step("Verify delete response"):
        delete_response_data = delete_response.json()
        print(f"Delete Account Response: {delete_response_data}")
        assert delete_response_data["responseCode"] == 200
        assert delete_response_data["message"] == "Account deleted!"


@allure.feature("Account API")
@allure.story("Delete Account")
@allure.title("Verify deleted account cannot be retrieved")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.regression
def test_verify_account_deleted(api_client: APIClient, account_user: dict):
    with allure.step("Create account"):
        create_response = api_client.post(APIEndpoints.CREATE_ACCOUNT, data=account_user)
        assert create_response.status_code == 200

        create_response_data = create_response.json()
        assert create_response_data["responseCode"] == 201
        assert create_response_data["message"] == "User created!"

    with allure.step("Delete account"):
        delete_response = api_client.delete(APIEndpoints.DELETE_ACCOUNT, data={"email": account_user["email"], "password": account_user["password"]})
        assert delete_response.status_code == 200

        delete_response_data = delete_response.json()
        assert delete_response_data["responseCode"] == 200
        assert delete_response_data["message"] == "Account deleted!"

    with allure.step("Try to retrieve deleted account"):
        get_response = api_client.get(APIEndpoints.GET_USER_DETAIL, params={"email": account_user["email"]})
        assert get_response.status_code == 200

    with allure.step("Verify account no longer exists"):
        response_data = get_response.json()
        print(f"Deleted Account Verification Response: {response_data}")
        assert response_data["responseCode"] == 404
        assert response_data["message"] == "Account not found with this email, try another email!"

