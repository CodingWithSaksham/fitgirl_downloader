import os
import sys
import platform
import PyInstaller.__main__

# Path to main script
main_script = "main.py"

# Determine separator based on platform
# Windows uses semicolon, others use colon
separator = ";" if platform.system() == "Windows" else ":"

# Get the absolute path to the project directory
project_dir = os.path.abspath(os.path.dirname(__file__))

# Define PyInstaller command arguments
pyinstaller_args = [
    main_script,
    "--name=fitgirl_downloader",
    "--onefile",  # Create a single executable
    "--icon=image.ico",
    # Add Linux binaries individually
    f"--add-data=resource/linux/aria2c{separator}resource/linux",
    f"--add-data=resource/linux/geckodriver{separator}resource/linux",
    f"--add-data=resource/linux/unrar{separator}resource/linux",
    # Add Windows binaries individually
    f"--add-data=resource/windows/aria2c.exe{separator}resource/windows",
    f"--add-data=resource/windows/chromedriver.exe{separator}resource/windows",
    f"--add-data=resource/windows/unrarw64.exe{separator}resource/windows",
    f"--add-data=loggers/loggers.json{separator}loggers",
    f"--add-data=LICENSE{separator}.",
    f"--add-data=README.md{separator}.",
    # Add hidden imports
    "--hidden-import=loggers",
    "--hidden-import=utils.downloader",
    "--hidden-import=utils.drivers",
    "--hidden-import=utils.file_utils",
    "--hidden-import=utils.unrar",
    "--hidden-import=utils.web_utils",
    # Other PyInstaller options
    "--clean",
    "--noconfirm",
]

# Run PyInstaller
PyInstaller.__main__.run(pyinstaller_args)

print("Build completed. Check the 'dist' folder for your executable.")
