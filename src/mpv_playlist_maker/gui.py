import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import sys
import os
import threading

# Add src to path to import utils
sys.path.insert(0, str(Path(__file__).parent))

from utils.getVideoFiles import getVideoFiles
from utils.sortVideoFiles import sortVideoFiles
from utils.playVideos import playVideos
from utils.getRuntimeJSON import getRuntimeJSON, getRuntimePath
from utils.jsonManipulation import writeJSONToFile


class VideoPlayerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MPV Playlist Maker")
        self.folders = []

        # Folder selection
        self.folder_frame = ttk.LabelFrame(root, text="Select Folders")
        self.folder_frame.pack(pady=10, padx=10, fill="x")

        self.folder_listbox = tk.Listbox(self.folder_frame, height=5)
        self.folder_listbox.pack(side=tk.LEFT, fill="both", expand=True)

        self.add_folder_btn = ttk.Button(self.folder_frame, text="Add Folder", command=self.add_folder)
        self.add_folder_btn.pack(side=tk.TOP, pady=5)

        self.remove_folder_btn = ttk.Button(self.folder_frame, text="Remove Selected", command=self.remove_folder)
        self.remove_folder_btn.pack(side=tk.TOP, pady=5)

        # Sort options
        self.sort_frame = ttk.LabelFrame(root, text="Sort Options")
        self.sort_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(self.sort_frame, text="Sort By:").grid(row=0, column=0, sticky="w")
        self.sort_by_var = tk.StringVar(value="Filename")
        self.sort_by_combo = ttk.Combobox(self.sort_frame, textvariable=self.sort_by_var, values=["Random", "Filename", "Folder Structure", "Duration"])
        self.sort_by_combo.grid(row=0, column=1, padx=5)

        ttk.Label(self.sort_frame, text="Sort Order:").grid(row=1, column=0, sticky="w")
        self.sort_order_var = tk.StringVar(value="Ascending")
        self.sort_order_combo = ttk.Combobox(self.sort_frame, textvariable=self.sort_order_var, values=["Ascending", "Descending"])
        self.sort_order_combo.grid(row=1, column=1, padx=5)

        # Start button
        self.start_btn = ttk.Button(root, text="Start Playing", command=self.start_playing)
        self.start_btn.pack(pady=10)

    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder and folder not in self.folders:
            self.folders.append(folder)
            self.folder_listbox.insert(tk.END, folder)

    def remove_folder(self):
        selected = self.folder_listbox.curselection()
        if selected:
            index = selected[0]
            self.folders.pop(index)
            self.folder_listbox.delete(index)

    def start_playing(self):
        if not self.folders:
            messagebox.showerror("Error", "Please select at least one folder.")
            return

        sort_by = self.sort_by_var.get()
        sort_order = self.sort_order_var.get() if sort_by != "Random" else None

        # Get all video files from selected folders
        all_videos = []
        for folder in self.folders:
            videos = getVideoFiles(Path(folder))
            all_videos.extend(videos)

        if not all_videos:
            messagebox.showerror("Error", "No video files found in selected folders.")
            return

        # Sort videos
        sorted_videos = sortVideoFiles(all_videos, sort_by, sort_order)

        # Save to runtime JSON
        runtime_data = getRuntimeJSON()
        video_list_strings = [str(v) for v in sorted_videos]
        runtime_data.update({"videos": video_list_strings, "index": 0})
        runtime_path = getRuntimePath()
        writeJSONToFile(runtime_path, runtime_data)

        # Play videos in a thread to not freeze GUI
        self.start_btn.config(state="disabled")
        thread = threading.Thread(target=self.play_videos, args=(sorted_videos,))
        thread.start()

    def play_videos(self, videos):
        try:
            playVideos(videos, 0)
            messagebox.showinfo("Done", "All videos played.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play videos: {str(e)}")
        finally:
            self.start_btn.config(state="normal")


if __name__ == "__main__":
    print("Starting GUI")
    root = tk.Tk()
    app = VideoPlayerGUI(root)
    root.mainloop()