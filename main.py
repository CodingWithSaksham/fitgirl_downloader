import sys
import traceback
from utils.file_utils import format_filename, read_urls
from utils.downloader import process_urls
from loggers.loggers import setup_logging
from os import path
from asyncio import run

DEBUG = False


def setup_error_logging():
    """Setup error logging to capture crashes in a file when running as exe"""
    # Check if we're running as a PyInstaller bundle
    if getattr(sys, "frozen", False):
        # Get the directory where the executable is located
        application_path = path.dirname(sys.executable)
        error_log_path = path.join(application_path, "crash.txt")

        # Create a file to capture any errors
        try:
            sys.stderr = open(error_log_path, "w")

            # Also set up an exception hook to catch unhandled exceptions
            def exception_hook(exc_type, exc_value, exc_traceback):
                error_msg = "".join(
                    traceback.format_exception(exc_type, exc_value, exc_traceback)
                )
                sys.stderr.write(error_msg)
                sys.stderr.flush()
                # Optionally, still show the error in the console
                sys.__stderr__.write(error_msg)
                sys.__stderr__.flush()

            sys.excepthook = exception_hook

        except Exception as e:
            # If we can't set up error logging, at least try to write the error
            with open(path.join(application_path, "logging_setup_error.txt"), "w") as f:
                f.write(f"Failed to set up error logging: {str(e)}")


def get_base_path():
    """Return the base path of the application."""
    if getattr(sys, "frozen", False):
        # Running in a PyInstaller bundle
        return sys._MEIPASS
    else:
        # Running as a script
        return path.dirname(__file__)


if __name__ == "__main__":
    setup_error_logging()
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
