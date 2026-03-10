from pathlib import Path
from utils import getFolderPath


def determineDirectoryToUse():
    currentWorkingDirectory = Path.cwd()

    question = f"Search for video files in current directory ({str(currentWorkingDirectory)})?\nYes/No: "
    answer = input(question).strip().lower()

    useCurrentWorkingDirectory = answer in ("y", "yes")

    if useCurrentWorkingDirectory:
        return currentWorkingDirectory
    else:
        return getFolderPath()
