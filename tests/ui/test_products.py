import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.product_page import ProductPage
from utils.test_data_loader import TestDataLoader


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("product_name", TestDataLoader.load_products().keys())
def test_search_product(page: Page, config: dict, product_name: str):
    home_page = HomePage(page)
    product_page = ProductPage(page)

    home_page.open(config["environment_config"]["base_url"])

    product_page.open_products_page()
    product_page.search_product(product_name=product_name)
    assert product_page.is_searched_products_displayed()
    assert product_page.is_product_displayed(product_name=product_name)


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("product_name", TestDataLoader.load_products().keys())
def test_open_product_details(page: Page, config: dict, product_name: str):
    home_page = HomePage(page)
    product_page = ProductPage(page)

    base_url = config["environment_config"]["base_url"]
    home_page.open(base_url)

    product_data = TestDataLoader.get_product(product_name=product_name)
    product_page.open_products_page()
    product_page.search_product(product_name=product_name)
    product_page.open_product(product_name=product_name, base_url=base_url)
    # product_page.debug_product_details()

    assert product_page.get_product_detail_name() == product_data["name"]
    assert product_page.get_product_detail_price() == product_data["price"]
    assert product_page.get_product_detail_category() == f"Category: {product_data['category']}"
    assert product_page.get_product_detail_availability() == f"Availability: {product_data['availability']}"
    assert product_page.get_product_detail_condition() == f"Condition: {product_data['condition']}"
    assert product_page.get_product_detail_brand() == f"Brand: {product_data["brand"]}" or f"Brand:  {product_data['brand']}"

