from pathlib import Path
import random
from utils import SORT_ORDER_VALUES, SORT_ORDER_VALUES_TYPE, SORT_BY_VALUES_TYPE


def sortVideoFiles(
    files: list[Path],
    sortBy: SORT_BY_VALUES_TYPE,
    sortOrder: SORT_ORDER_VALUES_TYPE | None,
):
    sortedFiles = files
    if sortBy == "Random":
        random.shuffle(sortedFiles)
        return sortedFiles
    elif sortBy and sortOrder:
        return sortedFiles
    else:
        return sortedFiles
