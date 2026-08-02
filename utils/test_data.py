import json
from pathlib import Path


def load_test_data(file_name: str) -> dict:
    file_path = Path("test_data")/file_name
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)

