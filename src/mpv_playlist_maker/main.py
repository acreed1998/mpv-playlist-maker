import sys
import tkinter as tk
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.playVideos import playVideos
from gui import VideoPlayerGUI, ask_to_resume_saved_playlist


if __name__ == "__main__":
    print("Starting GUI")
    root = tk.Tk()
    root.withdraw()

    resume, videos, index = ask_to_resume_saved_playlist(root)
    if resume:
        root.destroy()
        playVideos([Path(p) for p in videos], index)
    else:
        root.deiconify()
        app = VideoPlayerGUI(root)
        root.mainloop()