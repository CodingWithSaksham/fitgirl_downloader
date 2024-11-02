from re import search
from webbrowser import open
from requests import Session

def get_download_link(session: Session, url : str):
    with session.get(url, allow_redirects=False) as response:
        html_content = response.text
        match = search(r'window\.open\("([^"]+)"\)', html_content)
        if match:
            return match.group(1)
        else:
            print(f"No download link found in {url}")
            return None

def open_download_link(download_link):
    open(download_link)
