from utils import (
    determineDirectoryToUse,
    getRuntimeJSON,
    getVideoFiles,
    determineSortOrder,
    sortVideoFiles,
    playVideos,
)


def main():
    runtimeJSON = getRuntimeJSON()
    directory = determineDirectoryToUse()
    files = getVideoFiles(directory)
    sortBy, sortOrder = determineSortOrder()
    sortedFiles = sortVideoFiles(files, sortBy, sortOrder)
    playVideos(sortedFiles)
    print(runtimeJSON)


if __name__ == "__main__":
    main()
