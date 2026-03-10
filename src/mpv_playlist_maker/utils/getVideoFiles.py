from pathlib import Path
from utils import VIDEO_FILE_EXTENSIONS


def getVideoFiles(directory: Path):
    filesInDirectory = [
        item
        for item in directory.rglob("*")
        if item.is_file() and item.suffix in VIDEO_FILE_EXTENSIONS
    ]

    return filesInDirectory
