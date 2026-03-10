from pathlib import Path
from .constants import RUNTIME_FILENAME, RUNTIME_JSON_DEFAULT
from .jsonManipulation import writeJSONToFile, readJSONFromFile


def getRuntimePath():
    cwd = Path.cwd()
    cwdRuntimeJSONFilepath = Path(cwd, RUNTIME_FILENAME)
    return cwdRuntimeJSONFilepath


def getRuntimeJSON():
    cwdRuntimeJSONFilepath = getRuntimePath()

    if cwdRuntimeJSONFilepath.exists() == False:
        cwdRuntimeJSONFilepath.parent.mkdir(parents=True, exist_ok=True)
        cwdRuntimeJSONFilepath.touch()
        writeJSONToFile(cwdRuntimeJSONFilepath, RUNTIME_JSON_DEFAULT)

    # TODO: Detemine what to do if/when failed reading from
    # runtime file other than returning None
    runtimeData: dict | None = readJSONFromFile(cwdRuntimeJSONFilepath)
    return runtimeData
