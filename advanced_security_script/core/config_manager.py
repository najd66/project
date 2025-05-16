# advanced_security_script/core/config_manager.py

import yaml
import logging
import os

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "configs", "default_config.yaml")

class ConfigManager:
    def __init__(self, config_path=None):
        """
        Initializes the ConfigManager.
        Args:
            config_path (str, optional): Path to the configuration file.
                                         Defaults to DEFAULT_CONFIG_PATH.
        """
        self.config_path = config_path if config_path else DEFAULT_CONFIG_PATH
        self.config = {}
        self.load_config()

    def load_config(self):
        """
        Loads the configuration from the YAML file.
        """
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            if not self.config:
                self.config = {}
                logger.warning(f"Configuration file {self.config_path} is empty or invalid. Using empty config.")
            else:
                logger.info(f"Configuration loaded successfully from {self.config_path}")
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}. Using empty config.")
            self.config = {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML configuration file {self.config_path}: {e}. Using empty config.")
            self.config = {}
        except Exception as e:
            logger.error(f"An unexpected error occurred while loading config {self.config_path}: {e}. Using empty config.")
            self.config = {}

    def get(self, section: str, key: str, default=None):
        """
        Retrieves a configuration value for a given section and key.

        Args:
            section (str): The section name in the configuration.
            key (str): The key name within the section.
            default (any, optional): The default value to return if the key is not found.

        Returns:
            The configuration value or the default value.
        """
        return self.config.get(section, {}).get(key, default)

    def get_section(self, section: str) -> dict:
        """
        Retrieves an entire configuration section.

        Args:
            section (str): The section name in the configuration.

        Returns:
            A dictionary representing the section, or an empty dict if not found.
        """
        return self.config.get(section, {})

    def get_all_config(self) -> dict:
        """
        Retrieves the entire loaded configuration.

        Returns:
            A dictionary representing the entire configuration.
        """
        return self.config

if __name__ == '__main__':
    # Create a dummy config for testing
    dummy_config_content = """
    global:
      log_level: "INFO"
      max_threads: 10

    llm_report_generator:
      model_name: "gpt-3.5-turbo"
      api_key_env: "OPENAI_API_KEY"

    vulnerability_crawler:
      nvd_api_url: "https://services.nvd.nist.gov/rest/json/cves/1.0"
      exploit_db_rss: "https://www.exploit-db.com/rss.xml"
      max_results_per_source: 20
    """
    dummy_config_path = "/home/ubuntu/advanced_security_script/configs/dummy_test_config.yaml"
    with open(dummy_config_path, 'w') as f:
        f.write(dummy_config_content)

    logging.basicConfig(level=logging.INFO) # Basic logging for the test itself
    
    # Test with dummy config
    config_manager = ConfigManager(config_path=dummy_config_path)
    print("--- ConfigManager Test ---")
    print(f"Log Level: {config_manager.get('global', 'log_level', 'DEBUG')}")
    print(f"LLM Model: {config_manager.get('llm_report_generator', 'model_name')}")
    print(f"Non-existent key: {config_manager.get('global', 'non_existent_key', 'default_value')}")
    print(f"Crawler Config: {config_manager.get_section('vulnerability_crawler')}")

    # Test with default path (assuming default_config.yaml might not exist or be empty initially)
    default_config_manager = ConfigManager() # Uses DEFAULT_CONFIG_PATH
    print(f"Default config all: {default_config_manager.get_all_config()}")

    # Clean up dummy file
    os.remove(dummy_config_path)

