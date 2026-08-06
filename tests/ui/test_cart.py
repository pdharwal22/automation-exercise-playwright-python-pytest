import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.test_data_loader import TestDataLoader


@pytest.mark.ui
@pytest.mark.regression
def test_add_product_to_cart(page: Page, config: dict):
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)

    base_url = config["environment_config"]["base_url"]
    product_name = "Blue Top"

    home_page.open(base_url=base_url)

    product_page.open_products_page()
    product_page.search_product(product_name=product_name)
    product_page.add_product_to_cart(product_name=product_name)
    assert product_page.is_product_added_message_displayed()

    product_page.view_cart()
    assert cart_page.is_product_in_cart(product_name=product_name)


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("product_name", TestDataLoader.load_products().keys())
def test_validate_product_in_cart(page: Page, config: dict, product_name: str):
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)

    base_url = config["environment_config"]["base_url"]
    product_data = TestDataLoader.get_product(product_name)

    home_page.open(base_url=base_url)

    product_page.open_products_page()
    product_page.search_product(product_name)
    product_page.add_product_to_cart(product_name)
    assert product_page.is_product_added_message_displayed()

    product_page.view_cart()
    assert cart_page.is_product_in_cart(product_name)
    assert cart_page.get_product_price(product_name) == product_data["price"]
    assert cart_page.get_product_quantity(product_name) == "1"
    assert cart_page.get_product_total(product_name) == product_data["price"]


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("product_name", TestDataLoader.load_products().keys())
def test_update_product_quantity(page: Page, config: dict, product_name: str):
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)

    base_url = config["environment_config"]["base_url"]
    product_data = TestDataLoader.get_product(product_name)

    quantity = 3

    home_page.open(base_url=base_url)

    product_page.open_products_page()
    product_page.search_product(product_name)
    product_page.open_product(product_name, base_url=base_url)
    product_page.set_product_quantity(quantity=quantity)
    product_page.add_product_from_details()
    assert product_page.is_product_added_message_displayed()

    product_page.view_cart()
    assert cart_page.is_product_in_cart(product_name)
    assert cart_page.get_product_quantity(product_name) == str(quantity)

    expected_total = int(product_data["price"].replace("Rs. ", "")) * quantity
    actual_total = int(cart_page.get_product_total(product_name).replace("Rs. ", ""))
    assert actual_total==expected_total


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("product_name", TestDataLoader.load_products().keys())
def test_remove_product_from_cart(page: Page, config: dict, product_name: str):
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)

    base_url = config["environment_config"]["base_url"]

    home_page.open(base_url=base_url)

    product_page.open_products_page()
    product_page.search_product(product_name)
    product_page.add_product_to_cart(product_name)
    assert product_page.is_product_added_message_displayed()

    product_page.view_cart()
    assert cart_page.is_product_in_cart(product_name)

    cart_page.remove_product(product_name)
    assert not cart_page.is_product_in_cart(product_name)
    assert cart_page.is_cart_empty()


@pytest.mark.ui
@pytest.mark.regression
def test_multiple_products_in_cart(page: Page, config: dict):
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)

    base_url = config["environment_config"]["base_url"]
    products = TestDataLoader.load_products()
    assert len(products) >= 2, "Atleast two products are required for this test"

    product_names = list(products.keys())
    first_product = product_names[0]
    second_product = product_names[1]

    home_page.open(base_url=base_url)

    # Add First Product
    product_page.open_products_page()
    product_page.search_product(product_name=first_product)
    product_page.add_product_to_cart(product_name=first_product)
    assert product_page.is_product_added_message_displayed()

    # Continue shopping
    product_page.continue_shopping()

    # Add Second Product
    product_page.search_product(product_name=second_product)
    product_page.add_product_to_cart(product_name=second_product)
    assert product_page.is_product_added_message_displayed()

    # Open Cart
    product_page.view_cart()

    # Validate first product
    first_product_data = TestDataLoader.get_product(product_name=first_product)
    assert cart_page.is_product_in_cart(product_name=first_product)
    assert cart_page.get_product_price(product_name=first_product) == first_product_data["price"]
    first_quantity = int(cart_page.get_product_quantity(product_name=first_product))
    first_price = int(first_product_data["price"].replace("Rs. ", ""))
    first_actual_total = int(cart_page.get_product_price(product_name=first_product).replace("Rs. ", ""))
    assert first_quantity == 1
    assert first_actual_total == first_price * first_quantity

    # Validate second product
    second_product_data = TestDataLoader.get_product(product_name=second_product)
    assert cart_page.is_product_in_cart(product_name=second_product)
    assert cart_page.get_product_price(product_name=second_product) == second_product_data["price"]
    second_quantity = int(cart_page.get_product_quantity(product_name=second_product))
    second_price = int(second_product_data["price"].replace("Rs. ", ""))
    second_actual_total = int(cart_page.get_product_price(product_name=second_product).replace("Rs. ", ""))
    assert second_quantity == 1
    assert second_actual_total == second_price * second_quantity

