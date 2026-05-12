import platform
import shutil
import subprocess
import sys
import shlex
from typing import List


def is_executable_available(name: str) -> bool:
    return shutil.which(name) is not None


def get_missing_dependencies() -> List[str]:
    missing = []
    if not is_executable_available("mpv"):
        missing.append("mpv")
    if not is_executable_available("ffprobe"):
        missing.append("ffprobe")
    if not is_executable_available("ffmpeg"):
        missing.append("ffmpeg")
    return missing


def build_dependency_message(missing: List[str]) -> str:
    if not missing:
        return ""

    lines = [
        "The application cannot start because the following dependencies are missing:",
    ]
    for dep in missing:
        lines.append(f"  - {dep}")

    lines.extend(
        [
            "",
            "Please install the missing programs before running this application.",
            "After installation, press Enter to close this message.",
        ]
    )
    return "\n".join(lines)


def open_message_in_terminal(message: str) -> None:
    system = platform.system()
    if system == "Windows":
        script = f"echo {message.replace('%', '%%')} & pause"
        subprocess.Popen(
            ["cmd.exe", "/c", "start", "Dependency check", "cmd.exe", "/k", script],
            shell=False,
        )
        return

    if system == "Darwin":
        escaped = message.replace('"', '\\"').replace("$", "\\$")
        bash_command = f"printf \"{escaped}\\n\\n\"; read -r -p 'Press Enter to close...'"
        apple_script = (
            f'tell application "Terminal" to do script "{bash_command}"'
        )
        subprocess.Popen(["osascript", "-e", apple_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return

    # Linux and others
    try:
        import os

        escaped = message.replace('"', '\\"').replace("$", "\\$")
        bash_command = f"printf \"{escaped}\\n\\n\"; read -r -p 'Press Enter to close...'"
        terminal_commands = [
            ["gnome-terminal", "--", "bash", "-lc", bash_command],
            ["konsole", "-e", "bash", "-lc", bash_command],
            ["xfce4-terminal", "-e", "bash -lc \"{escaped}; read -r -p \'Press Enter to close...\'\""],
            ["xterm", "-hold", "-e", bash_command],
        ]

        for cmd in terminal_commands:
            try:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except FileNotFoundError:
                continue
    except Exception:
        pass

    print(message)
    try:
        input("\nPress Enter to close...")
    except EOFError:
        pass


def check_dependencies() -> None:
    missing = get_missing_dependencies()
    if not missing:
        return

    message = build_dependency_message(missing)
    open_message_in_terminal(message)
    sys.exit(1)
