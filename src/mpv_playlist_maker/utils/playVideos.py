import subprocess
import os
from pathlib import Path
from .getRuntimeJSON import getRuntimePath, getRuntimeJSON
from .jsonManipulation import writeJSONToFile


def playVideos(files, startingIndex: int):
    idx = startingIndex

    filepathsFromIndex = files[startingIndex:]
    for file in filepathsFromIndex:
        runtimeData = getRuntimeJSON()
        totalNumberOfVideos = len(runtimeData["videos"])
        idx = idx + 1

        fullscreenArgument = "--fullscreen" if runtimeData["fullscreen"] == True else ""
        speedArgument = f"--speed={runtimeData['speed']}"

        print(f"📽️ Now playing video {idx} of {totalNumberOfVideos}: {file.name} 🍿")
        subprocess.Popen(
            ["mpv", fullscreenArgument, speedArgument, "--keep-open=no", str(file)],
            env=os.environ.copy(),
        ).wait()
        print(
            f"🏁 Finished playing video {idx} of {totalNumberOfVideos}: {file.name} 🏁"
        )

        runtimeFilepath = getRuntimePath()
        runtimeData.update({"index": idx})
        writeJSONToFile(runtimeFilepath, runtimeData)

    print("🏁 Finished playing all videos! 🏁")
