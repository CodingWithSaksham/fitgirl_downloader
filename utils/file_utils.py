import os
import sys
from logging import getLogger

logger = getLogger(__name__)


def print_txt_files():
    """Prints all the text files present in the 'dist' directory"""

    txt_dir = (file for file in os.listdir() if file.endswith(".txt"))
    for i in txt_dir:
        print(i)


def format_filename():
    """Formats user input to either append '.txt' or add './' in the beginning"""

    print_txt_files()
    user_input = input("Enter file name from the above text files: ")
    if user_input is None:
        logger.warn("File name cannot be empty")

    if user_input == "":
        user_input = "download"
    if not user_input.startswith("./"):
        user_input = f"./{user_input}"  # Prepend './' if missing
    if not user_input.endswith(".txt"):
        user_input = f"{user_input}.txt"  # Append '.txt' if missing
    return user_input


def read_urls(file_path: str) -> list:
    """Reads all the urls in the files and returns them after stripping '-' from the starting"""

    urls = []

    # Checks if file exists
    if not os.path.exists(file_path):
        logger.error("File not found")
        return

    # Read URLs from file
    file = open(file_path)
    first_line = file.readline()

    # Checks if first line of file is either ##DOWNLOAD LINKS or some other text which is not needed
    if first_line.startswith("- http"):
        urls.append(first_line.lstrip("- ").strip())

    for line in file:
        urls.append(line.lstrip("- ").strip())

    file.close()
    return urls


def get_all_files() -> list:
    """Returns all the files that have been downloaded and removes failed downloads"""

    download_dir = os.path.join(os.getcwd(), "Downloads")
    files = []

    for file in os.listdir(download_dir):
        # Removes undownloaded files and also re-downloaded files
        if not file.endswith((".rar", ".bin")) or file.endswith(").rar"):
            os.remove(os.path.join(download_dir, file))
        else:
            files.append(file)

    return files


def return_missing_files(files_and_urls: dict) -> list:
    """Returns which files are missing along with their URL"""

    files_not_found = []
    files = get_all_files()

    for file in files_and_urls.keys():
        if file.lstrip("'") not in files:
            files_not_found.append(files_and_urls[file])

    return files_not_found


def ensure_file_accessible(file_path: str) -> str:
    """
    Ensure's file exists and is executable, also checks if the file is
    bundled with PyInstaller and returns file path according to PyInstaller Bundle
    """

    # Get the absolute path to resources (handles PyInstaller bundling)
    if hasattr(sys, "_MEIPASS"):
        # Running as a bundled executable
        return os.path.join(sys._MEIPASS, file_path)

    # Ensure the binary is executable
    if not os.path.exists(file_path):
        raise FileNotFoundError("Fallback driver/binary not found")

    if not os.access(file_path, os.X_OK):
        os.chmod(file_path, 0o755)  # Ensure it's executable

    return file_path
