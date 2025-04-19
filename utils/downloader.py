from .web_utils import get_download_link, get_filename_from_url, open_download_link
from .file_utils import return_missing_files
from .unrar import unrar_file

from logging import getLogger
from aiohttp import ClientSession
from asyncio import create_task, gather

st = None
files_and_urls = {}
re_downloading = False

logger = getLogger(__name__)


async def process_urls(urls: list):
    async with ClientSession() as session:
        download_link_tasks = [
            create_task(get_download_link(session, url)) for url in urls
        ]

        # Wait for all download links to be fetched
        download_links = await gather(*download_link_tasks)

        filename_tasks = [
            create_task(get_filename_from_url(link, session)) for link in download_links
        ]

        filenames = await gather(*filename_tasks)

        for url, link, filename in zip(urls, download_links, filenames):
            if not link:
                logger.warning(f"Skipping URL due to missing download link: {url}")
                continue

            files_and_urls[filename] = link

        await open_download_link(download_links)

    # Handle missing files
    missing_files = return_missing_files(files_and_urls)

    if missing_files:
        print("Starting to download missing files again")
        await process_urls(missing_files)
    else:
        print("All files downloaded! Starting extraction.")
        rar_file = tuple(files_and_urls.keys())[0].lstrip("'")
        await unrar_file(rar_file)
