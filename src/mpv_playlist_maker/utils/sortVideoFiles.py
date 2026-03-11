from pathlib import Path
import random, subprocess, json
from .constants import SORT_ORDER_VALUES_TYPE, SORT_BY_VALUES_TYPE


def get_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(path)],
        capture_output=True,
        text=True,
    )
    info = json.loads(result.stdout)
    duration = float(info["format"]["duration"])  # seconds
    return duration


def sortVideoFiles(
    files: list[Path],
    sortBy: SORT_BY_VALUES_TYPE,
    sortOrder: SORT_ORDER_VALUES_TYPE | None,
):
    sortedFiles = files
    isAscending = sortOrder == "Ascending"

    if sortBy == "Random":
        random.shuffle(sortedFiles)

    elif sortBy == "Filename":
        sortedFiles.sort(
            key=lambda filepath: filepath.name.lower(), reverse=not isAscending
        )

    elif sortBy == "Folder Structure":
        sortedFiles.sort(
            key=lambda filepath: (str(filepath.parent).lower(), filepath.name.lower()),
            reverse=not isAscending,
        )

    elif sortBy == "Duration":
        sortedFiles.sort(key=get_duration, reverse=not isAscending)

    return sortedFiles
