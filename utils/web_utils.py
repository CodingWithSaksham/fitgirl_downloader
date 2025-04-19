from re import search, Match
from logging import getLogger
from aiohttp import ClientSession
from functools import cache
from concurrent.futures import ThreadPoolExecutor, as_completed

from .drivers import download_url

logger = getLogger(__name__)


@cache
async def get_download_link(session: ClientSession, url: str) -> str | None:
    async with session.get(url, allow_redirects=False) as response:
        html_content = await response.text()
        match: Match[str] | None = search(r'window\.open\("([^"]+)"\)', html_content)
        if match:
            return match.group(1)
        else:
            logger.critical(f"No download link found in {url}")
            return None


async def open_download_link(download_links: list):
    for i in range(0, len(download_links), 3):
        batch = download_links[i : i + 3]
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(download_url, url) for url in batch]
            for future in as_completed(futures):
                future.result()


@cache
async def get_filename_from_url(url: str, session: ClientSession) -> str:
    """
    Fetches the filename from the given URL using an asynchronous request.

    Args:
        url (str): The URL to fetch the file name from.

    Returns:
        str: The extracted file name or a fallback name.
    """
    try:
        async with session.get(url, allow_redirects=True) as response:
            response.raise_for_status()

            # Extract the Content-Disposition header if present
            content_disposition = response.headers.get("Content-Disposition")

            # Parse the filename from the header
            filename = content_disposition.split("filename=")[-1].strip('"')

            return filename.split("UTF-8")[-1]

    except Exception as e:
        return f"Error: {e}"  # Return an error message if the request fails
