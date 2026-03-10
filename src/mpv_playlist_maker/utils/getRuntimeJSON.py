from pathlib import Path
from .constants import RUNTIME_FILENAME, RUNTIME_JSON_DEFAULT
from .jsonManipulation import writeJSONToFile, readJSONFromFile


def getRuntimeJSON():
    cwd = Path.cwd()
    cwdRuntimeJSONFilepath = Path(cwd, RUNTIME_FILENAME)

    if cwdRuntimeJSONFilepath.exists() == False:
        cwdRuntimeJSONFilepath.parent.mkdir(parents=True, exist_ok=True)
        cwdRuntimeJSONFilepath.touch()
        writeJSONToFile(cwdRuntimeJSONFilepath, RUNTIME_JSON_DEFAULT)

    runtimeData = readJSONFromFile(cwdRuntimeJSONFilepath)
    return runtimeData
