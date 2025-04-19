import logging
from logging.config import dictConfig
from json import load
from os import path

def setup_logging():
    """Load logging configuration from loggers.json."""
    config_path = path.join(path.dirname(__file__), "loggers.json")
    try:
        with open(config_path, "r") as file:
            config = load(file)
        dictConfig(config)
        logging.info("Logging is configured successfully.")
    except Exception as e:
        print(f"Failed to load logging configuration: {e}")
        raise
