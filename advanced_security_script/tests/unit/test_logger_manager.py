# advanced_security_script/tests/unit/test_logger_manager.py

import unittest
import os
import logging
import json
from advanced_security_script.core.logger_manager import LoggerManager
# Assuming ConfigManager is in core, or use a mock for isolated testing
from advanced_security_script.core.config_manager import ConfigManager 

class TestLoggerManager(unittest.TestCase):
    def setUp(self):
        self.test_logs_dir = "/home/ubuntu/advanced_security_script/tests/unit/temp_logs"
        self.log_file_std = os.path.join(self.test_logs_dir, "test_std.log")
        self.log_file_json = os.path.join(self.test_logs_dir, "test_json.log")
        os.makedirs(self.test_logs_dir, exist_ok=True)

        # Clean up log files from previous runs if they exist
        if os.path.exists(self.log_file_std):
            os.remove(self.log_file_std)
        if os.path.exists(self.log_file_json):
            os.remove(self.log_file_json)

    def tearDown(self):
        # Clean up log files created during the test
        if os.path.exists(self.log_file_std):
            os.remove(self.log_file_std)
        if os.path.exists(self.log_file_json):
            os.remove(self.log_file_json)
        # Remove the temp_logs directory if it's empty
        if os.path.exists(self.test_logs_dir) and not os.listdir(self.test_logs_dir):
            os.rmdir(self.test_logs_dir)

    def _read_log_file(self, file_path):
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r") as f:
            return f.readlines()

    class MockConfigManager:
        def __init__(self, config_data):
            self.config_data = config_data
        def get(self, section, key, default=None):
            return self.config_data.get(section, {}).get(key, default)
        def get_all_config(self):
            return self.config_data

    def test_default_initialization(self):
        lm = LoggerManager() # No config manager
        logger = lm.get_logger("test_default_logger")
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.level, logging.INFO) # Default level
        # Check if root handlers are set (console, file by default)
        self.assertTrue(len(logging.getLogger().handlers) > 0)

    def test_initialization_with_standard_config(self):
        config_data = {
            "global": {
                "log_level": "DEBUG",
                "log_file_path": self.log_file_std,
                "log_format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                "json_log_format": False
            }
        }
        mock_cm = self.MockConfigManager(config_data)
        lm = LoggerManager(config_manager=mock_cm)
        logger = lm.get_logger("test_std_logger")
        
        self.assertEqual(logging.getLogger().level, logging.DEBUG)
        logger.debug("This is a standard debug message.")
        logger.info("This is a standard info message.")

        log_content = self._read_log_file(self.log_file_std)
        self.assertTrue(any("This is a standard debug message." in line for line in log_content))
        self.assertTrue(any("This is a standard info message." in line for line in log_content))
        self.assertFalse(any("{\"message\": \"This is a standard debug message.\"}" in line for line in log_content)) # Ensure not JSON

    def test_initialization_with_json_config(self):
        # Requires python-json-logger to be installed in the environment
        try:
            import pythonjsonlogger.jsonlogger
        except ImportError:
            self.skipTest("python-json-logger is not installed, skipping JSON logging test.")

        config_data = {
            "global": {
                "log_level": "INFO",
                "log_file_path": self.log_file_json,
                "json_log_format": True
            }
        }
        mock_cm = self.MockConfigManager(config_data)
        lm = LoggerManager(config_manager=mock_cm)
        logger = lm.get_logger("test_json_logger")

        self.assertEqual(logging.getLogger().level, logging.INFO)
        log_message = "This is a JSON info message."
        extra_data = {"key1": "value1", "key2": 123}
        logger.info(log_message, extra=extra_data)

        log_content = self._read_log_file(self.log_file_json)
        self.assertTrue(len(log_content) > 0)
        found_log = False
        for line in log_content:
            try:
                log_entry = json.loads(line)
                if log_entry.get("message") == log_message and log_entry.get("key1") == "value1":
                    self.assertEqual(log_entry.get("name"), "test_json_logger")
                    self.assertEqual(log_entry.get("levelname"), "INFO")
                    found_log = True
                    break
            except json.JSONDecodeError:
                pass # Ignore lines that are not valid JSON, though all should be
        self.assertTrue(found_log, "JSON log message with extra fields not found or not formatted correctly.")

    def test_get_logger_method(self):
        lm = LoggerManager()
        logger1 = lm.get_logger("module1")
        logger2 = lm.get_logger("module2")
        self.assertNotEqual(logger1.name, logger2.name)
        self.assertEqual(logger1.name, "module1")
        self.assertEqual(logger2.name, "module2")

    def test_log_directory_creation_failure(self):
        # This test is a bit tricky as it involves filesystem permissions or invalid paths.
        # We can simulate by providing a path that's hard/impossible to create.
        # For this example, we assume the default log path is used and we can't easily make it fail.
        # A more robust test might involve mocking os.makedirs to raise an OSError.
        # For now, we ensure it falls back gracefully if the config is bad.
        config_data = {
            "global": {
                "log_level": "INFO",
                "log_file_path": "/proc/test_log_dir/test.log", # Path that cannot be created
            }
        }
        mock_cm = self.MockConfigManager(config_data)
        # LoggerManager should catch the error and default to console logging.
        # We check that no exception is raised during init and a logger can be obtained.
        try:
            lm = LoggerManager(config_manager=mock_cm)
            logger = lm.get_logger("fallback_logger")
            logger.info("This message should go to console if file logging failed.")
            # Verify that no file was created at the invalid path (if possible)
            self.assertFalse(os.path.exists("/proc/test_log_dir/test.log"))
        except Exception as e:
            self.fail(f"LoggerManager raised an unexpected exception during fallback: {e}")

if __name__ == "__main__":
    unittest.main()

