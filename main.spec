# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for a src-layout Python package.
# Adjust the variables in the CONFIG section to match your project.

import sys
import os

# ─── CONFIG ───────────────────────────────────────────────────────────────────

APP_NAME   = "mpv_playlist_maker"          # Name of the output executable
ENTRY_POINT = "src/mpv_playlist_maker/main.py"   # Path to your entry-point file (the one with main() / __main__)

# ─── DATA FILES ───────────────────────────────────────────────────────────────
# Any non-Python data files you want to bundle (uncomment and edit if needed):
# Format: (source_path, destination_folder_inside_bundle)
DATAS = [
    # ("src/mypackage/data/config.json", "mypackage/data"),
    # ("src/mypackage/assets/",          "mypackage/assets"),
]

# Any packages that PyInstaller misses due to dynamic imports:
HIDDEN_IMPORTS = [
    # "mypackage.plugins",
]

# ──────────────────────────────────────────────────────────────────────────────

block_cipher = None

a = Analysis(
    [ENTRY_POINT],
    pathex=[],
    binaries=[],
    datas=DATAS,
    hiddenimports=HIDDEN_IMPORTS,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,   # Set to False if you don't want a terminal window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
