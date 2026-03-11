from typing import Literal

GET_DURATION_ERROR = "Something went wrong while trying to get the duration of the following video file:\n"

READ_JSON_ERROR = "Something went wrong while trying to read the content of: "
RUNTIME_FILENAME = "mpvpm-runtime.json"
RUNTIME_JSON_DEFAULT = {
    "videos": [],
    "index": 0,
    "speed": 1.0,
    "fullscreen": True,
}

SORT_BY_VALUES_TYPE = Literal["Random", "Filename", "Folder Structure", "Duration"]
SORT_BY_VALUES = (
    "Random",
    "Filename",
    "Folder Structure",
    "Duration",
)

SORT_ORDER_VALUES_TYPE = Literal["Ascending", "Descending"]
SORT_ORDER_VALUES = ("Ascending", "Descending")

VIDEO_FILE_EXTENSIONS = (
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".wmv",
    ".flv",
    ".webm",
    ".m4v",
    ".mpeg",
    ".mpg",
    ".3gp",
    ".ogv",
    ".ts",
    ".mts",
    ".m2ts",
    ".vob",
    ".divx",
    ".xvid",
    ".rm",
    ".rmvb",
    ".asf",
    ".amv",
    ".m2v",
    ".svi",
    ".3g2",
    ".mxf",
    ".roq",
    ".nsv",
    ".f4v",
    ".f4p",
    ".f4a",
    ".f4b",
    ".gifv",
    ".drc",
    ".yuv",
    ".qt",
    ".mng",
    ".ogm",
    ".dv",
    ".wtv",
    ".pvr",
    ".h264",
    ".h265",
    ".hevc",
)
