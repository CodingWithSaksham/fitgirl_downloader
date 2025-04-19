from platform import system
from os import getcwd, mkdir, path
from subprocess import DEVNULL, run

download_folder = path.join(getcwd(), "Downloads")
if not path.exists(download_folder):
    mkdir(download_folder)


def get_aria2c() -> str:
    aria2c_path = ""
    if system() == "Windows":
        aria2c_path = path.join("resource", "windows", "aria2c.exe")

    elif system() == "Linux":
        aria2c_path = path.join("resource", "linux", "aria2c")

    return aria2c_path


def download_url(url: str):
    aria2c_path = get_aria2c()

    result = run(
        [
            aria2c_path,
            "-x",
            "16",
            "--console-log-level=error",
            f"--dir={download_folder}",
            url,
        ],
    )
    if result.returncode == 0:
        print(f"Finished: {url}")
    else:
        print(f"[ERROR] Failed: {url}")
    return result.returncode
