import os
from pathlib import Path
from utils import RUNTIME_FILENAME, writeJSONToFile, readJSONFromFile


def getRuntimeJSON():
    cwd = Path.cwd()
    cwdRuntimeJSONFilepath = Path(cwd, RUNTIME_FILENAME)

    if cwdRuntimeJSONFilepath.exists() == False:
        cwdRuntimeJSONFilepath.mkdir(parents=True, exist_ok=True)
        cwdRuntimeJSONFilepath.touch()
        writeJSONToFile(cwdRuntimeJSONFilepath, {})

    runtimeData = readJSONFromFile(cwdRuntimeJSONFilepath)
    return runtimeData
