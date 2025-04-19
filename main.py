import sys
from utils.file_utils import format_filename, read_urls
from utils.downloader import process_urls
from loggers.loggers import setup_logging
from os import path
from asyncio import run

DEBUG = False


def get_base_path():
    """Return the base path of the application."""
    if getattr(sys, "frozen", False):
        # Running in a PyInstaller bundle
        return sys._MEIPASS
    else:
        # Running as a script
        return path.dirname(__file__)


if __name__ == "__main__":
    if DEBUG:
        # Access the loggers folder
        base_path = get_base_path()
        loggers_folder = path.join(base_path, "loggers")
        loggers_json_path = path.join(loggers_folder, "loggers.json")

        print(f"Loggers JSON Path: {loggers_json_path}")

    # Initialing
    setup_logging()

    input_file = format_filename()
    urls = read_urls(input_file)
    run(process_urls(urls))
