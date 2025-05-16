# advanced_security_script/tests/unit/test_config_manager.py

import unittest
import os
import yaml
from advanced_security_script.core.config_manager import ConfigManager

# Ensure the test runs from the project root or paths are adjusted accordingly
# For simplicity, this assumes paths are relative from where pytest might be run (project root)
# or that PYTHONPATH is set up.

# Helper to create a temporary config file
def create_temp_config_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(content, f)

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.test_configs_dir = "/home/ubuntu/advanced_security_script/tests/unit/temp_configs"
        os.makedirs(self.test_configs_dir, exist_ok=True)
        self.valid_config_path = os.path.join(self.test_configs_dir, "valid_config.yaml")
        self.empty_config_path = os.path.join(self.test_configs_dir, "empty_config.yaml")
        self.invalid_config_path = os.path.join(self.test_configs_dir, "invalid_config.yaml")
        self.non_existent_config_path = os.path.join(self.test_configs_dir, "non_existent.yaml")

        self.valid_config_content = {
            "global": {"log_level": "INFO", "max_threads": 10},
            "module_A": {"param1": "value1", "param2": True}
        }
        create_temp_config_file(self.valid_config_path, self.valid_config_content)
        create_temp_config_file(self.empty_config_path, {})
        with open(self.invalid_config_path, "w") as f:
            f.write("global: [invalid_yaml") # Malformed YAML

    def tearDown(self):
        if os.path.exists(self.valid_config_path):
            os.remove(self.valid_config_path)
        if os.path.exists(self.empty_config_path):
            os.remove(self.empty_config_path)
        if os.path.exists(self.invalid_config_path):
            os.remove(self.invalid_config_path)
        if os.path.exists(self.test_configs_dir):
            # Check if directory is empty before removing, to be safe
            if not os.listdir(self.test_configs_dir):
                 os.rmdir(self.test_configs_dir)
            else: # If other files were created, remove them one by one or handle appropriately
                for item in os.listdir(self.test_configs_dir):
                    item_path = os.path.join(self.test_configs_dir, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                if not os.listdir(self.test_configs_dir):
                    os.rmdir(self.test_configs_dir)

    def test_load_valid_config(self):
        cm = ConfigManager(config_path=self.valid_config_path)
        self.assertEqual(cm.get("global", "log_level"), "INFO")
        self.assertEqual(cm.get("module_A", "param1"), "value1")
        self.assertTrue(cm.get("module_A", "param2"))
        self.assertEqual(cm.get_all_config(), self.valid_config_content)

    def test_get_non_existent_key(self):
        cm = ConfigManager(config_path=self.valid_config_path)
        self.assertIsNone(cm.get("global", "non_existent_key"))
        self.assertEqual(cm.get("global", "non_existent_key", "default"), "default")

    def test_get_non_existent_section(self):
        cm = ConfigManager(config_path=self.valid_config_path)
        self.assertEqual(cm.get_section("non_existent_section"), {})
        self.assertIsNone(cm.get("non_existent_section", "key"))

    def test_load_empty_config(self):
        cm = ConfigManager(config_path=self.empty_config_path)
        self.assertEqual(cm.get_all_config(), {})
        self.assertIsNone(cm.get("global", "log_level"))

    def test_load_invalid_yaml_config(self):
        # Suppress error logs during this specific test if desired, or check logs
        cm = ConfigManager(config_path=self.invalid_config_path)
        self.assertEqual(cm.get_all_config(), {}) # Should default to empty on error

    def test_load_non_existent_config_file(self):
        cm = ConfigManager(config_path=self.non_existent_config_path)
        self.assertEqual(cm.get_all_config(), {}) # Should default to empty

    def test_default_config_path_handling(self):
        # This test assumes the default config path might not exist or is empty
        # It's hard to test the exact default path without knowing its state
        # So we test that it doesn't crash and returns an empty dict if default is not found
        # Create a dummy default config in the expected location for a controlled test
        original_default_path = ConfigManager().config_path # Get the default path it would use
        temp_default_dir = os.path.dirname(original_default_path)
        os.makedirs(temp_default_dir, exist_ok=True)
        
        # Scenario 1: Default config does not exist (ensure it's removed if it was created by other tests)
        if os.path.exists(original_default_path):
            os.remove(original_default_path)
        cm_no_default = ConfigManager()
        self.assertEqual(cm_no_default.get_all_config(), {})

        # Scenario 2: Default config exists and is valid
        create_temp_config_file(original_default_path, {"default_setting": "present"})
        cm_with_default = ConfigManager()
        self.assertEqual(cm_with_default.get("default_setting", "key_should_not_be_used"), "present")
        os.remove(original_default_path) # Clean up
        if not os.listdir(temp_default_dir):
            os.rmdir(temp_default_dir)

if __name__ == "__main__":
    unittest.main()

