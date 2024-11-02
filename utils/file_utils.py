import os
import re
from zipfile import ZipFile
from rarfile import RarFile
from datetime import datetime

DOWNLOAD_DIR = "downloads"
DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")       # Get the default download directory

os.makedirs(DOWNLOAD_DIR, exist_ok=True)      # Make the directory where files are to be unzip into

EXTRACTION_DIR = os.path.join(DEFAULT_DOWNLOAD_DIR, DOWNLOAD_DIR)

def print_txt_files():
    txt_dir = [file for file in os.listdir() if file.endswith(".txt")]
    for i in txt_dir:
        print(i)

def format_filename():
    print_txt_files()
    user_input = input("Enter file name from the above text files: ")
    if not user_input.startswith("./"):
        user_input = f"./{user_input}"  # Prepend './' if missing
    if not user_input.endswith(".txt"):
        user_input = f"{user_input}.txt"  # Append '.txt' if missing
    return user_input


def extract_zip_file(filepath: str):
    with ZipFile(filepath) as zip_ref:
        zip_ref.extractall(EXTRACTION_DIR)
        print(f"Extracted: {filepath} to {EXTRACTION_DIR}")


def extract_rar_file(filepath : str):
    with RarFile(filepath) as rar_ref:
        rar_ref.extractall(EXTRACTION_DIR)
        print(f"Extracted: {filepath} to {EXTRACTION_DIR}")


def extract_file(filepath: str):
    if filepath.endswith(".zip"):
        extract_zip_file(filepath)

    elif filepath.endswith(".rar"):
        extract_rar_file(filepath)


def check_and_extract_files():
    os.chdir(DEFAULT_DOWNLOAD_DIR)      # Change current working directory to default download directory
    
    today = datetime.now().date()
    print(f"Checking files in directory: {DEFAULT_DOWNLOAD_DIR}")

    # Collect and sort all .rar files by their part number
    rar_files = [
        f for f in os.listdir(DEFAULT_DOWNLOAD_DIR)
        if f.endswith(".rar") and datetime.fromtimestamp(os.path.getmtime(os.path.join(DEFAULT_DOWNLOAD_DIR, f))).date() == today
    ]

    # Sort files based on the part number if available, or lexicographically if not
    rar_files.sort(key=lambda x: int(re.search(r"part(\d+)", x).group(1)) if re.search(r"part(\d+)", x) else 0)

    for filename in rar_files:
        filepath = os.path.join(DEFAULT_DOWNLOAD_DIR, filename)
        print(f"Extracting: {filename}")
        extract_file(filepath)
        os.remove(filepath)  # Remove archive after extraction
        print(f"Removed archive: {filepath}")