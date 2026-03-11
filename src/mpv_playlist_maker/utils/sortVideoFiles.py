from pathlib import Path
import random
from pymediainfo import MediaInfo
from .constants import SORT_ORDER_VALUES_TYPE, SORT_BY_VALUES_TYPE


def get_duration(path: Path) -> float:
    info = MediaInfo.parse(path)
    videoTrack = info.video_tracks[0]
    trackDuration: int = videoTrack.duration  # duration is in milliseconds
    return float(trackDuration)


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
