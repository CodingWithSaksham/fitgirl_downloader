from utils.file_utils import format_filename
from utils.downloader import process_url as main

if __name__ == "__main__":
    input_file = format_filename()
    main(input_file)
