import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from utils.getVideoFiles import getVideoFiles
from utils.getRuntimeJSON import getRuntimeJSON, getRuntimePath
from utils.jsonManipulation import writeJSONToFile
from utils.playVideos import playVideos
from utils.sortVideoFiles import sortVideoFiles

from .constants import ACCENT_COLOR, BACKGROUND_COLOR, FOREGROUND_COLOR, SECONDARY_COLOR
from .saved_playlist import get_saved_playlist_data
from .styles import configure_style


class VideoPlayerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MPV Playlist Maker")
        self.root.geometry("640x520")
        self.root.resizable(True, True)
        self.root.configure(bg=BACKGROUND_COLOR)
        self.folders = []

        configure_style(root)

        title_label = ttk.Label(root, text="MPV Playlist Maker", style="Header.TLabel")
        title_label.pack(pady=(18, 2))

        subtitle_label = ttk.Label(
            root,
            text="Select one or more folders, choose how to sort the videos, and play them sequentially.",
            style="SubHeader.TLabel",
            wraplength=600,
            justify="center",
        )
        subtitle_label.pack(pady=(0, 14))

        content_frame = ttk.Frame(root, style="TFrame")
        content_frame.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        self.build_saved_playlist_card(content_frame)

        self.folder_frame = ttk.Frame(content_frame, style="Card.TFrame", padding=16)
        self.folder_frame.pack(fill="x", pady=(0, 12))

        folder_label = ttk.Label(self.folder_frame, text="Selected folders", style="Section.TLabel")
        folder_label.pack(anchor="w")

        self.folder_listbox = tk.Listbox(
            self.folder_frame,
            height=6,
            bg="#f9fbff",
            bd=0,
            highlightthickness=0,
            activestyle="none",
            fg=FOREGROUND_COLOR,
            font=("Segoe UI", 10),
            selectbackground="#e8eaf6",
            selectforeground=FOREGROUND_COLOR,
        )
        self.folder_listbox.pack(fill="both", expand=True, pady=(10, 12))

        button_row = ttk.Frame(self.folder_frame, style="Card.TFrame")
        button_row.pack(fill="x")

        self.add_folder_btn = ttk.Button(button_row, text="Add Folder", command=self.add_folder, style="Accent.TButton")
        self.add_folder_btn.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.remove_folder_btn = ttk.Button(button_row, text="Remove Selected", command=self.remove_folder, style="Secondary.TButton")
        self.remove_folder_btn.pack(side="left", expand=True, fill="x", padx=(6, 0))

        self.video_count_label = ttk.Label(self.folder_frame, text="No folders selected yet.", style="SubHeader.TLabel")
        self.video_count_label.pack(anchor="w", pady=(12, 0))

        self.sort_frame = ttk.Frame(content_frame, style="Card.TFrame", padding=16)
        self.sort_frame.pack(fill="x")

        sort_title = ttk.Label(self.sort_frame, text="Sort options", style="Section.TLabel")
        sort_title.grid(row=0, column=0, columnspan=2, sticky="w")

        ttk.Label(self.sort_frame, text="Sort by:", style="Label.TLabel").grid(row=1, column=0, sticky="w", pady=(12, 6))
        self.sort_by_var = tk.StringVar(value="Filename")
        self.sort_by_combo = ttk.Combobox(
            self.sort_frame,
            textvariable=self.sort_by_var,
            values=["Random", "Filename", "Folder Structure", "Duration"],
            state="readonly",
            style="TCombobox",
        )
        self.sort_by_combo.grid(row=1, column=1, sticky="ew", padx=(12, 0), pady=(12, 6))

        ttk.Label(self.sort_frame, text="Sort order:", style="Label.TLabel").grid(row=2, column=0, sticky="w", pady=6)
        self.sort_order_var = tk.StringVar(value="Ascending")
        self.sort_order_combo = ttk.Combobox(
            self.sort_frame,
            textvariable=self.sort_order_var,
            values=["Ascending", "Descending"],
            state="readonly",
            style="TCombobox",
        )
        self.sort_order_combo.grid(row=2, column=1, sticky="ew", padx=(12, 0), pady=6)
        self.sort_frame.columnconfigure(1, weight=1)

        self.start_btn = ttk.Button(root, text="Play Videos", command=self.start_playing, style="Accent.TButton")
        self.start_btn.pack(padx=16, pady=(10, 16), fill="x")

        self.update_saved_playlist_status()
        root.bind("<Return>", lambda event: self.start_playing())

    def build_saved_playlist_card(self, parent):
        self.resume_frame = ttk.Frame(parent, style="Card.TFrame", padding=16)
        self.resume_title = ttk.Label(self.resume_frame, text="Resume saved playlist", style="Section.TLabel")
        self.resume_title.pack(anchor="w")

        self.resume_message = ttk.Label(
            self.resume_frame,
            text="",
            style="SubHeader.TLabel",
            wraplength=600,
            justify="left",
        )
        self.resume_message.pack(anchor="w", pady=(8, 0))

        self.resume_button = ttk.Button(
            self.resume_frame,
            text="Continue saved playlist",
            command=self.resume_saved_playlist,
            style="Secondary.TButton",
        )
        self.resume_button.pack(anchor="e", pady=(10, 0))
        self.resume_frame.pack_forget()

    def update_saved_playlist_status(self):
        videos, index = get_saved_playlist_data()
        if videos is None:
            self.resume_frame.pack_forget()
            return

        self.resume_frame.pack(fill="x", pady=(0, 12))
        self.resume_message.config(
            text=(
                f"A saved playlist exists with {len(videos)} videos. "
                f"Playback stopped at video {index + 1}. "
                "Press continue to resume from the saved position."
            )
        )
        self.resume_button.config(state="normal")

    def resume_saved_playlist(self):
        videos, index = get_saved_playlist_data()
        if videos is None:
            messagebox.showinfo("No saved playlist", "No saved playlist is available to resume.")
            self.resume_frame.pack_forget()
            return

        self.start_btn.config(state="disabled")
        self.resume_button.config(state="disabled")
        thread = threading.Thread(
            target=self.play_videos,
            args=([Path(p) for p in videos], index),
            daemon=True,
        )
        thread.start()

    def update_video_count(self):
        if not self.folders:
            self.video_count_label.config(text="No folders selected yet.")
            return

        total_videos = sum(len(getVideoFiles(Path(f))) for f in self.folders)
        self.video_count_label.config(
            text=f"{len(self.folders)} folder(s) selected · {total_videos} video(s) found"
        )

    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder and folder not in self.folders:
            self.folders.append(folder)
            self.folder_listbox.insert(tk.END, folder)
            self.update_video_count()

    def remove_folder(self):
        selected = self.folder_listbox.curselection()
        if selected:
            index = selected[0]
            self.folders.pop(index)
            self.folder_listbox.delete(index)
            self.update_video_count()

    def start_playing(self):
        if not self.folders:
            messagebox.showerror("Error", "Please select at least one folder.")
            return

        sort_by = self.sort_by_var.get()
        sort_order = self.sort_order_var.get() if sort_by != "Random" else None

        all_videos = [v for folder in self.folders for v in getVideoFiles(Path(folder))]
        if not all_videos:
            messagebox.showerror("Error", "No video files found in selected folders.")
            return

        sorted_videos = sortVideoFiles(all_videos, sort_by, sort_order)

        runtime_data = getRuntimeJSON()
        runtime_data.update({"videos": [str(v) for v in sorted_videos], "index": 0})
        writeJSONToFile(getRuntimePath(), runtime_data)

        self.start_btn.config(state="disabled")
        thread = threading.Thread(target=self.play_videos, args=(sorted_videos,), daemon=True)
        thread.start()

    def play_videos(self, videos, start_index=0):
        try:
            playVideos(videos, start_index)
            messagebox.showinfo("Done", "All videos played.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play videos: {str(e)}")
        finally:
            self.start_btn.config(state="normal")