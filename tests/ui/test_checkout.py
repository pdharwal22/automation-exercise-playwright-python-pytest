import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.test_data_loader import TestDataLoader


@pytest.mark.ui
@pytest.mark.regression
def test_checkout_requires_login(page: Page, config: dict):
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)
    # checkout_page = CheckoutPage(page)

    base_url = config["environment_config"]["base_url"]

    products = TestDataLoader.load_products()
    product_name = next(iter(products))

    home_page.open(base_url=base_url)

    product_page.open_products_page()
    product_page.search_product(product_name=product_name)
    product_page.add_product_to_cart(product_name=product_name)
    assert product_page.is_product_added_message_displayed()

    product_page.view_cart()
    assert cart_page.is_product_in_cart(product_name=product_name)

    cart_page.proceed_to_checkout()
    assert cart_page.is_login_required_for_checkout()


@pytest.mark.ui
@pytest.mark.regression
def test_authenticated_user_can_proceed_to_checkout(page: Page, config: dict, test_user: dict):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    base_url = config["environment_config"]["base_url"]

    products = TestDataLoader.load_products()
    product_name = next(iter(products))

    # Login
    home_page.open(base_url=base_url)

    login_page.open_login_page(base_url=base_url)
    login_page.login(email=test_user["email"], password=test_user["password"])

    # Add product to cart
    product_page.open_products_page()
    product_page.search_product(product_name=product_name)
    product_page.add_product_to_cart(product_name=product_name)
    assert product_page.is_product_added_message_displayed()

    # Open cart
    product_page.view_cart()
    assert cart_page.is_product_in_cart(product_name=product_name)

    # Proceed to checkout
    cart_page.proceed_to_checkout()
    assert checkout_page.is_checkout_page_displayed()


@pytest.mark.ui
@pytest.mark.regression
def test_validate_checkout_details(page: Page, config: dict, test_user: dict):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    base_url = config["environment_config"]["base_url"]

    products = TestDataLoader.load_products()
    product_name = next(iter(products))
    product_data = TestDataLoader.get_product(product_name=product_name)

    # Login
    home_page.open(base_url=base_url)

    login_page.open_login_page(base_url=base_url)
    login_page.login(email=test_user["email"], password=test_user["password"])

    # Add Product
    product_page.open_products_page()
    product_page.search_product(product_name=product_name)
    product_page.add_product_to_cart(product_name=product_name)
    assert product_page.is_product_added_message_displayed()

    # Open Cart
    product_page.view_cart()
    assert cart_page.is_product_in_cart(product_name=product_name)

    # Checkout
    cart_page.proceed_to_checkout()
    assert checkout_page.is_checkout_page_displayed()

    # Validate delivery address
    delivery_address = checkout_page.get_delivery_address()
    assert test_user["name"] in delivery_address
    assert "Automation Street" in delivery_address
    assert "Ludhiana" in delivery_address
    assert "Punjab" in delivery_address
    assert "141001" in delivery_address
    assert "India" in delivery_address

    # Validate billing address
    billing_address = checkout_page.get_billing_address()
    assert test_user["name"] in billing_address
    assert "Automation Street" in billing_address
    assert "Ludhiana" in billing_address
    assert "Punjab" in billing_address
    assert "141001" in billing_address
    assert "India" in billing_address

    # Validate order details
    assert checkout_page.is_product_in_order(product_name=product_name)
    assert checkout_page.get_product_price(product_name=product_name) == product_data["price"]
    assert checkout_page.get_product_quantity(product_name=product_name) == "1"
    assert checkout_page.get_product_total(product_name=product_name) == product_data["price"]

