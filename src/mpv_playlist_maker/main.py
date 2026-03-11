from utils import (
    determineVideosToPlay,
    playVideos,
)


def main():
    videoList, index = determineVideosToPlay()
    playVideos(videoList, index)


if __name__ == "__main__":
    main()
