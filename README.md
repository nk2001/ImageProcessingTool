Before running, install the required libraries:

pip install pillow pillow-heif
pip install piexif

This version is compatible with Windows and offers multiple ways to use the script:

Run with command-line arguments:
python conv.py <src folder>

Or specify both input and output folders:
python conv.py <src_folder> <dst_folder>

Run the script and follow prompts to enter folders interactively

Key Windows-specific features:

Uses os.path.normpath() to handle Windows file paths correctly
Supports Windows-style file paths with backslashes
Works with command-line arguments or interactive input
Handles long file paths common in Windows
Provides flexibility in folder selection