from utils import (
    determineDirectoryToUse,
    determineVideosToPlay,
    getRuntimeJSON,
    getVideoFiles,
    determineSortOrder,
    sortVideoFiles,
    playVideos,
)


def main():
    videoList, index = determineVideosToPlay()
    # playVideos(videoList, index)
    # directory = determineDirectoryToUse()
    # files = getVideoFiles(directory)
    # sortBy, sortOrder = determineSortOrder()
    # sortedFiles = sortVideoFiles(files, sortBy, sortOrder)
    # playVideos(sortedFiles)
    print(videoList)


if __name__ == "__main__":
    main()
