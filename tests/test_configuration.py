import pytest


@pytest.mark.smoke
def test_environment_configuration(config):
    assert config["environment"] == "qa"
    assert config["environment_config"]["base_url"] == "https://automationexercise.com"

