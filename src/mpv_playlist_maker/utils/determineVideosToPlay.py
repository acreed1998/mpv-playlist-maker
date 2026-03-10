from pathlib import Path
from .determineDirectoryToUse import determineDirectoryToUse
from .determineSortOrder import determineSortOrder
from .getVideoFiles import getVideoFiles
from .getRuntimeJSON import getRuntimeJSON, getRuntimePath
from .jsonManipulation import writeJSONToFile
from .sortVideoFiles import sortVideoFiles


def determineVideosToPlay():
    runtimeData = getRuntimeJSON()
    videoList: list[str] = runtimeData["videos"]
    index: int = runtimeData["index"]

    videoListLength = len(videoList)

    if (videoListLength < 1) or (videoListLength == (index)):
        videoDirectory = determineDirectoryToUse()
        videoList: list[Path] = getVideoFiles(videoDirectory)
        sortBy, sortOrder = determineSortOrder()
        videoList = sortVideoFiles(videoList, sortBy, sortOrder)
        index = 0
        videoListWithStrings = [str(video) for video in videoList]
        runtimeData.update({"videos": videoListWithStrings})

        runtimePath = getRuntimePath()
        writeJSONToFile(runtimePath, runtimeData)
    else:
        videoList: list[Path] = [Path(videoPath) for videoPath in videoList]

    videoList = videoList[index:]
    return videoList, index
