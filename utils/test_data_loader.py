import json
from pathlib import Path

class TestDataLoader:
    @staticmethod
    def load_json(file_name: str):
        file_path = Path(__file__).parent.parent/"test_data"/file_name
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)


    @staticmethod
    def load_products():
        return TestDataLoader.load_json(file_name="products.json")["products"]


    @staticmethod
    def get_product(product_name: str):
        products = TestDataLoader.load_products()
        if product_name not in products:
            raise ValueError(f"Product '{product_name}' not found in products.json")
        return products[product_name]


    @staticmethod
    def load_payment():
        return TestDataLoader.load_json(file_name="payments.json")["payment"]


    @staticmethod
    def get_payment(payment: str):
        payments = TestDataLoader.load_payment()
        if payment not in payments:
            raise ValueError(f"Payment details '{payment}' not found in payments.json")
        return payments[payment]


    @staticmethod
    def load_order():
        return TestDataLoader.load_json(file_name="orders.json")["order"]


    @staticmethod
    def get_order():
        return TestDataLoader.load_order()
        
