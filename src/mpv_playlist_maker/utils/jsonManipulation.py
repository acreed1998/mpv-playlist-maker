from pathlib import Path
import json
import os
from .constants import READ_JSON_ERROR, WRITE_JSON_ERROR


def readJSONFromFile(filepath: Path):
    try:
        with open(str(filepath), "r") as file:
            data = json.load(file)
            return data
    except:
        print(f"{READ_JSON_ERROR}{str(filepath)}")
        return None


def writeJSONToFile(filepath: Path, content):
    try:
        with open(str(filepath), "w") as file:
            json.dump(content, file, indent=2)
            return filepath
    except:
        print(f"{WRITE_JSON_ERROR}{str(filepath)}")
        return None
