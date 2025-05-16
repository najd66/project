# advanced_security_script/core/logger_manager.py

import logging
import logging.config
import os
import json

# Assuming ConfigManager is in the same core directory or accessible via path
# from .config_manager import ConfigManager # If ConfigManager is in the same directory

class LoggerManager:
    def __init__(self, config_manager=None, default_log_level="INFO"):
        """
        Initializes the LoggerManager.
        Args:
            config_manager (ConfigManager, optional): Instance of ConfigManager to get logging settings.
            default_log_level (str, optional): Default log level if not found in config.
        """
        self.config_manager = config_manager
        self.default_log_level = default_log_level
        self._setup_logging()

    def _get_log_config(self):
        """
        Prepares the logging configuration dictionary.
        """
        log_level = self.default_log_level
        log_file_path = "./logs/script.log" # Default log file path
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s"
        json_log_format = False

        if self.config_manager:
            log_level = self.config_manager.get("global", "log_level", self.default_log_level)
            log_file_path = self.config_manager.get("global", "log_file_path", "./logs/script.log")
            log_format_config = self.config_manager.get("global", "log_format", log_format)
            json_log_format = self.config_manager.get("global", "json_log_format", False)
        else:
            log_format_config = log_format

        # Ensure log directory exists
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except OSError as e:
                # Fallback to console logging if directory creation fails
                print(f"Warning: Could not create log directory {log_dir}: {e}. Logging to console only.")
                return {
                    "version": 1,
                    "disable_existing_loggers": False,
                    "formatters": {
                        "standard": {"format": log_format_config},
                    },
                    "handlers": {
                        "console": {
                            "level": log_level.upper(),
                            "formatter": "standard",
                            "class": "logging.StreamHandler",
                            "stream": "ext://sys.stdout",
                        },
                    },
                    "root": {
                        "handlers": ["console"],
                        "level": log_level.upper(),
                    },
                }

        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {"format": log_format_config},
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(asctime)s %(name)s %(levelname)s %(module)s %(funcName)s %(lineno)d %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "level": log_level.upper(),
                    "formatter": "json" if json_log_format else "standard",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout", 
                },
                "file": {
                    "level": log_level.upper(),
                    "formatter": "json" if json_log_format else "standard",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": log_file_path,
                    "maxBytes": 1024 * 1024 * 5,  # 5 MB
                    "backupCount": 5,
                    "encoding": "utf-8",
                },
            },
            "root": {
                "handlers": ["console", "file"],
                "level": log_level.upper(),
            },
            # Example: Configure specific loggers for modules
            # "loggers": {
            #     "modules.exploitation": {
            #         "handlers": ["file"], # Or a specific handler for this module
            #         "level": "DEBUG",
            #         "propagate": False
            #     }
            # }
        }
        return config

    def _setup_logging(self):
        """
        Applies the logging configuration.
        """
        try:
            log_config = self._get_log_config()
            logging.config.dictConfig(log_config)
            logging.info("LoggerManager initialized and logging configured.")
        except Exception as e:
            # Fallback to basic config if dictConfig fails
            logging.basicConfig(level=self.default_log_level.upper())
            logging.error(f"Error setting up logging with dictConfig: {e}. Fell back to basicConfig.", exc_info=True)

    @staticmethod
    def get_logger(name):
        """
        Retrieves a logger instance.
        Args:
            name (str): Name of the logger (usually __name__ of the calling module).
        Returns:
            logging.Logger: Logger instance.
        """
        return logging.getLogger(name)

if __name__ == '__main__':
    # This test requires ConfigManager to be available or mocked
    # For standalone testing, we can mock ConfigManager
    class MockConfigManager:
        def __init__(self, config_data):
            self.config_data = config_data
        def get(self, section, key, default=None):
            return self.config_data.get(section, {}).get(key, default)

    # Create dummy log directory for testing
    if not os.path.exists("./logs"):
        os.makedirs("./logs")

    # Test 1: Basic setup
    print("--- Test 1: Basic LoggerManager ---")
    logger_manager_basic = LoggerManager() # No config manager, uses defaults
    basic_logger = logger_manager_basic.get_logger("my_basic_app")
    basic_logger.info("This is an info message from basic logger.")
    basic_logger.warning("This is a warning from basic logger.")

    # Test 2: With ConfigManager (and JSON logging)
    print("\n--- Test 2: LoggerManager with ConfigManager (JSON) ---")
    dummy_config_data_json = {
        "global": {
            "log_level": "DEBUG",
            "log_file_path": "./logs/test_script_json.log",
            "json_log_format": True
        }
    }
    mock_cm_json = MockConfigManager(dummy_config_data_json)
    logger_manager_json = LoggerManager(config_manager=mock_cm_json)
    json_logger = logger_manager_json.get_logger("my_json_app")
    json_logger.debug("This is a DEBUG message from JSON logger.", extra={"custom_field": "custom_value"})
    json_logger.info("This is an INFO message from JSON logger.")
    json_logger.error("This is an ERROR from JSON logger.")

    # Test 3: With ConfigManager (Standard text logging)
    print("\n--- Test 3: LoggerManager with ConfigManager (Standard) ---")
    dummy_config_data_std = {
        "global": {
            "log_level": "INFO",
            "log_file_path": "./logs/test_script_std.log",
            "log_format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "json_log_format": False
        }
    }
    mock_cm_std = MockConfigManager(dummy_config_data_std)
    logger_manager_std = LoggerManager(config_manager=mock_cm_std)
    std_logger = logger_manager_std.get_logger("my_std_app")
    std_logger.info("This is an INFO message from Standard logger.")
    std_logger.warning("This is a WARNING from Standard logger.")

    print("\nCheck ./logs/test_script_json.log and ./logs/test_script_std.log for output.")
    print("You might need to install python-json-logger: pip install python-json-logger")

