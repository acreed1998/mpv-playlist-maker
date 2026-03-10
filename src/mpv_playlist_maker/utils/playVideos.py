import subprocess
from pathlib import Path


def playVideos(files: list[Path]):
    for file in files:
        subprocess.run(["mpv", "--fullscreen", "--keep-open=no", str(file)])
