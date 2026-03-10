import subprocess
from pathlib import Path
from .getRuntimeJSON import getRuntimePath, getRuntimeJSON
from .jsonManipulation import writeJSONToFile


def playVideos(files: list[Path], index: int):
    idx = index
    for file in files:
        runtimeData = getRuntimeJSON()
        fullscreenArgument = "--fullscreen" if runtimeData["fullscreen"] == True else ""
        subprocess.run(["mpv", fullscreenArgument, "--keep-open=no", str(file)])

        idx = idx + 1

        runtimeFilepath = getRuntimePath()
        runtimeData.update({"index": idx})
        writeJSONToFile(runtimeFilepath, runtimeData)

    print("Finished playing all videos!")
