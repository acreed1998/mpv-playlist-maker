from pathlib import Path
import json
import os


def readJSONFromFile(filepath: Path):
    if os.path.isfile(filepath) == False:
        return None
    try:
        with open(str(filepath), "r") as file:
            data = json.load(file)
            return data
    except:
        return None


def writeJSONToFile(filepath: Path, content):
    if os.path.isfile(filepath) == False:
        return None
    try:
        with open(str(filepath), "w") as file:
            json.dump(content, file, indent=2)
            return filepath
    except:
        return None
