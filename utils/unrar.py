import subprocess
import os
import sys
from platform import system, architecture
from .file_utils import ensure_file_accessible


def get_architecture():
    os_arch = architecture()[0]
    if os_arch == "32bit":
        print(
            "32-bit system detected, to unzip the files, the script requires a 64-bit system to run."
        )
        input("Press enter to exit")
        sys.exit(1)


def get_unrar_path() -> str:
    system_name = system()
    get_architecture()

    unrar_binary = ""

    if system_name in ["Linux", "Darwin"]:
        unrar_binary = os.path.join(os.getcwd(), "resource", "linux", "unrar")
    elif system_name == "Windows":
        unrar_binary = os.path.join(os.getcwd(), "resource", "windows", "unrarw64.exe")

    unrar_binary = ensure_file_accessible(unrar_binary)
    return unrar_binary


async def unrar_file(rar_path: str):
    """
    Extracts a RAR file using an external unrar binary.
    """

    output_dir = rar_path.split("_--_")[0]
    unrar_binary = get_unrar_path()
    rar_path = os.path.join("Downloads", rar_path)

    if not os.path.exists(unrar_binary):
        raise FileNotFoundError(f"Unrar binary not found: {unrar_binary}")

    if not os.path.exists(rar_path):
        raise FileNotFoundError(f"RAR file not found: {rar_path}")

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    try:
        result = subprocess.run(
            [unrar_binary, "x", "-o+", rar_path, output_dir],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error extracting RAR file: {e.stderr}")
