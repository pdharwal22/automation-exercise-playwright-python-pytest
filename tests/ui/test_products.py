import allure
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.product_page import ProductPage
from utils.test_data_loader import TestDataLoader


@allure.feature("Products")
@allure.story("Search Product")
@allure.title("Verify user can search product - {product_name}")
@allure.description("Verify that a user can search for a product and the matching product is displayed in the search results.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("product_name", TestDataLoader.load_products().keys())
def test_search_product(page: Page, config: dict, product_name: str):
    home_page = HomePage(page)
    product_page = ProductPage(page)

    base_url = config["environment_config"]["base_url"]
    allure.dynamic.parameter("Product", product_name)

    with allure.step("Open the application"):
        home_page.open(base_url=base_url)

    with allure.step("Navigate to Products page"):
        product_page.open_products_page()

    with allure.step({f"Search for product '{product_name}'"}):
        product_page.search_product(product_name=product_name)

    with allure.step("Verify search results are displayed"):
        assert product_page.is_searched_products_displayed()

    with allure.step("Verify searched product is displayed"):
        assert product_page.is_product_displayed(product_name=product_name)


@allure.feature("Products")
@allure.story("Product Details")
@allure.title("Verify product details for - {product_name}")
@allure.description("Verify that the product details page displays the correct information including product name, price, category, availability, condition, and brand.")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("product_name", TestDataLoader.load_products().keys())
def test_open_product_details(page: Page, config: dict, product_name: str):
    home_page = HomePage(page)
    product_page = ProductPage(page)

    base_url = config["environment_config"]["base_url"]
    product_data = TestDataLoader.get_product(product_name=product_name)
    allure.dynamic.parameter("Product", product_name)

    with allure.step("Open the application"):
        home_page.open(base_url)

    with allure.step("Navigate to products page"):
        product_page.open_products_page()

    with allure.step(f"Search for product '{product_name}'"):
        product_page.search_product(product_name=product_name)

    with allure.step("Open product details page"):
        product_page.open_product(product_name=product_name, base_url=base_url)

    with allure.step("Verify product name"):
        assert product_page.get_product_detail_name() == product_data["name"]

    with allure.step("Verify product price"):
        assert product_page.get_product_detail_price() == product_data["price"]

    with allure.step("Verify product category"):
        assert product_page.get_product_detail_category() == f"Category: {product_data['category']}"

    with allure.step("Verify product availability"):
        assert product_page.get_product_detail_availability() == f"Availability: {product_data['availability']}"

    with allure.step("Verify product condition"):
        assert product_page.get_product_detail_condition() == f"Condition: {product_data['condition']}"

    with allure.step("Verify product brand"):
        assert product_page.get_product_detail_brand() in (f"Brand: {product_data["brand"]}", f"Brand:  {product_data['brand']}")

