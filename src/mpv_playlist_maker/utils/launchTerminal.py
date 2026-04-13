import sys
import os
import subprocess
import platform


def cleanLinuxEnv(env: dict) -> dict:
    """Remove Snap-injected library paths that conflict with system binaries."""
    cleaned = env.copy()
    for var in ("LD_LIBRARY_PATH", "LD_PRELOAD"):
        original = cleaned.get(var, "")
        filtered = ":".join(p for p in original.split(":") if "/snap/" not in p)
        if filtered:
            cleaned[var] = filtered
        else:
            cleaned.pop(var, None)
    return cleaned


def launchInTerminal():
    if os.environ.get("LAUNCHED_IN_TERMINAL"):
        return

    system = platform.system()
    script = sys.argv[0]
    args = sys.argv[1:]
    env = {**os.environ, "LAUNCHED_IN_TERMINAL": "1"}
    cmd = [sys.executable, script, *args]

    if system == "Windows":
        subprocess.Popen(["cmd", "/c", "start", "cmd", "/c", *cmd], env=env)

    elif system == "Darwin":  # macOS
        escaped = " ".join(f'"{c}"' for c in cmd)
        apple_script = f'tell application "Terminal" to do script "{escaped}"'
        subprocess.Popen(["osascript", "-e", apple_script])

    elif system == "Linux":
        env = cleanLinuxEnv(env)
        terminals = [
            ["gnome-terminal", "--", *cmd],
            ["konsole", "-e", *cmd],
            ["xfce4-terminal", "-e", *cmd],
            ["xterm", "-e", *cmd],
        ]
        for term in terminals:
            try:
                subprocess.Popen(term, env=env)
                break
            except FileNotFoundError:
                continue
        else:
            raise RuntimeError(
                "No supported terminal emulator found on this Linux system."
            )

    else:
        raise RuntimeError(f"Unsupported platform: {system}")

    sys.exit(0)
