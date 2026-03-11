import subprocess
from pathlib import Path
from .getRuntimeJSON import getRuntimePath, getRuntimeJSON
from .jsonManipulation import writeJSONToFile


def playVideos(files: list[Path], index: int):
    idx = index
    for file in files:
        runtimeData = getRuntimeJSON()
        totalNumberOfVideos = len(runtimeData["videos"])
        idx = idx + 1

        fullscreenArgument = "--fullscreen" if runtimeData["fullscreen"] == True else ""
        speedArgument = f"--speed={runtimeData['speed']}"

        print(f"📽️ Now playing video {idx} of {totalNumberOfVideos}: {file.name} 🍿")
        subprocess.run(["mpv", fullscreenArgument, speedArgument, "--keep-open=no", str(file)])
        print(f"🏁 Finished playing video {idx} of {totalNumberOfVideos}: {file.name} 🏁")

        runtimeFilepath = getRuntimePath()
        runtimeData.update({"index": idx})
        writeJSONToFile(runtimeFilepath, runtimeData)

    print("🏁 Finished playing all videos! 🏁")
