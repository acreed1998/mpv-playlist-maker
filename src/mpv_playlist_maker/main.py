from utils import (
    determineVideosToPlay,
    launchInTerminal,
    playVideos,
)


def main():
    launchInTerminal()
    videoList, index = determineVideosToPlay()
    playVideos(videoList, index)


if __name__ == "__main__":
    main()
