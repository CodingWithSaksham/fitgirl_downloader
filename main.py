import re
import asyncio
import webbrowser
import os
from rarfile import RarFile
from zipfile import ZipFile
from aiohttp import ClientSession

# Directory to save downloads
DOWNLOAD_DIR = "./downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)  # Ensure the download directory exists


def print_txt_files():
    txt_dir = [file for file in os.listdir() if file.endswith(".txt")]

    for i in txt_dir:
        print(i)


def format_filename():
    print_txt_files()

    user_input = input("Enter file name from the above text files")
    # Check if input starts with './'
    if not user_input.startswith("./"):
        user_input = f"./{user_input}"  # Prepend './' if missing

    # Check if input ends with '.txt'
    if not user_input.endswith(".txt"):
        user_input = f"{user_input}.txt"  # Append '.txt' if missing

    return user_input


# Function to extract the download URL from the website's HTML
async def get_download_link(session: ClientSession, url: str):
    async with session.get(url, allow_redirects=False) as response:
        html_content = await response.text()
        match = re.search(r'window\.open\("([^"]+)"\)', html_content)
        if match:
            return match.group(1)
        else:
            print(f"No download link found in {url}")
            return None


# Function to open download link in browser
def open_download_link(download_link):
    webbrowser.open(download_link)


# Function to automatically unzip downloaded files
def extract_file(filepath):
    if filepath.endswith(".zip"):
        with ZipFile(filepath, 'r') as zip_ref:
            extract_dir = filepath.replace(".zip", "")
            zip_ref.extractall(extract_dir)
            print(f"Extracted: {filepath} to {extract_dir}")
    elif filepath.endswith(".rar"):
        with RarFile(filepath, 'r') as rar_ref:
            extract_dir = filepath.replace(".rar", "")
            rar_ref.extractall(extract_dir)
            print(f"Extracted: {filepath} to {extract_dir}")


# Function to check for new files in the download directory and extract them
def check_and_extract_files(download_dir):
    for filename in os.listdir(download_dir):
        filepath = os.path.join(download_dir, filename)
        if filename.endswith((".zip", ".rar")):
            extract_file(filepath)
            os.remove(filepath)  # Remove archive after extraction
            print(f"Removed archive: {filepath}")


# Asynchronous function to process all URLs
async def process_urls(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print("File not found")
        return

    # Read the URLs from the file
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]

    # Create an aiohttp session
    async with ClientSession() as session:
        for url in urls:
            print(f"Processing URL: {url}")
            
            # Get the download link from the URL
            download_link = await get_download_link(session, url)
            
            # If a download link is found, open it in the browser
            if download_link:
                print(f"Opening download link: {download_link}")
                open_download_link(download_link)
                
                # Wait a bit to ensure download starts
                await asyncio.sleep(5)

                # Check for new files in the download directory and extract them
                check_and_extract_files(DOWNLOAD_DIR)


# Entry point
def main(file_path):
    asyncio.run(process_urls(file_path))

if __name__ == "__main__":
    input_file = format_filename() # Replace this with the path to your file containing URLs
    main(input_file)
