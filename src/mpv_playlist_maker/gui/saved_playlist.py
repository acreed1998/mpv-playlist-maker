from pathlib import Path
from tkinter import messagebox

from utils.getRuntimeJSON import getRuntimeJSON


def get_saved_playlist_data():
    runtime_data = getRuntimeJSON()
    if not runtime_data or not isinstance(runtime_data, dict):
        return None, None

    videos = runtime_data.get("videos")
    index = runtime_data.get("index")

    if not isinstance(videos, list) or not isinstance(index, int):
        return None, None

    if index < 0 or index >= len(videos):
        return None, None

    current_video_path = Path(videos[index])
    if not current_video_path.exists():
        return None, None

    return videos, index


def ask_to_resume_saved_playlist(root):
    videos, index = get_saved_playlist_data()
    if videos is None:
        return False, None, None

    title = "Resume saved playlist?"
    message = (
        f"A saved playlist was found, and playback stopped at video {index + 1} of {len(videos)}.\n\n"
        "Would you like to continue playing from that point?"
    )
    answer = messagebox.askyesno(title, message, parent=root)
    return answer, videos, index