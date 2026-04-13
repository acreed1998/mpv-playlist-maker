import argparse
import os
import sys
from pathlib import Path


def getFolderPath():
    directoryPath = input("Enter folder path for directory containing video files: ").strip()

    if os.path.isdir(directoryPath):
        path = Path(directoryPath)
        return path
    else:
        print(
            f"Error: '{directoryPath}' is not a valid directory. Please check that the folder exists and try again."
        )
        sys.exit(2)
