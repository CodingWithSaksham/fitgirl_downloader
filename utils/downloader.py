from os.path import exists
from requests import Session
from speedtest import Speedtest, ConfigRetrievalError
from time import sleep
from .file_utils import check_and_extract_files
from .web_utils import get_download_link, open_download_link

st = Speedtest()


def wait_for_wifi():
    """
    Pauses code execution until an internet connection is detected using Speedtest.
    """
    while True:
        try:
            # Attempt to retrieve a speed test server list to check connectivity
            st.get_best_server()
            print("Wi-Fi connection restored.")
            break  # Connection successful, break the loop
        except ConfigRetrievalError:
            print("Waiting for Wi-Fi to come back...")
            sleep(5)  # Wait for a few seconds before retrying


def process_url(file_path):
    if not exists(file_path):
        print("File not found")
        return

    with open(file_path, 'r') as file:
        urls = [line.lstrip("- ").strip() for line in file if line.lstrip("- ").strip()]

    with Session() as session:
        for url in urls:
            print(f"Processing URL: {url}")
            download_link = get_download_link(session, url)
            if download_link:
                try:
                    wifi_speed = 1.25e-7 * st.download()       # Returns the download speed of user in megabytes per second
                    time_for_download = (500/wifi_speed) - 8          # Taking an average of 500MB per archive and dividing it by wifi speed to get time for download
                except ZeroDivisionError:
                    wait_for_wifi()
                
                print(f"Opening download link: {download_link}")
                open_download_link(download_link)
                sleep(time_for_download)

        print("All files are being downloaded. Press Enter when ready to unzip them.")
        input("Press Enter when all the files are downloaded")
        check_and_extract_files()