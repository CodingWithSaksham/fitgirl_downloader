# pyinstaller_build.py
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
    "--icon=image.ico",  # Use your icon
    f"--add-data=resource{separator}resource",  # Include resource directory
    f"--add-data=LICENSE{separator}.",  # Include LICENSE file
    f"--add-data=README.md{separator}.",  # Include README file
    "--hidden-import=loggers",  # Add potential hidden imports
    "--hidden-import=utils.downloader",
    "--hidden-import=utils.drivers",
    "--hidden-import=utils.file_utils",
    "--hidden-import=utils.unrar",
    "--hidden-import=utils.web_utils",
    "--clean",  # Clean PyInstaller cache
    "--noconfirm",  # Replace output directory without asking
]

# Run PyInstaller
PyInstaller.__main__.run(pyinstaller_args)

print("Build completed. Check the 'dist' folder for your executable.")
