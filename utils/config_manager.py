from pathlib import Path
import yaml

class ConfigManager:
    """
    Loads and provides access to framework configuration.
    """

    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()


    def _load_config(self) -> dict:
        with self.config_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)


    def get_environment(self, environment: str) -> dict:
        environments = self.config["environments"]
        if environment not in environments:
            raise ValueError(f"Environment '{environment}' is not configured.")
        return environments[environment]


    def get_browser_config(self) -> dict:
        return self.config["browser"]


    def get_timeout_config(self) -> dict:
        return self.config["timeouts"]