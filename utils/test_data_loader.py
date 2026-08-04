import json
from pathlib import Path

class TestDataLoader:
    @staticmethod
    def load_products():
        file_path = Path(__file__).parent.parent/"test_data"/"products.json"
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)["products"]


    @staticmethod
    def get_product(product_name: str):
        products = TestDataLoader.load_products()
        if product_name not in products:
            raise ValueError(f"Product '{product_name}' not found in products.json")
        return products[product_name]

