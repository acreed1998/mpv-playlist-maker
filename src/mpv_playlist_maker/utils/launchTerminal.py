import sys
import os
import subprocess
import platform


def _clean_env(env: dict):
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


def _get_cmd():
    """
    Return the correct command to relaunch the current process.
    Handles both frozen executables (PyInstaller) and normal Python scripts.
    """
    if getattr(sys, "frozen", False):
        # Running as a PyInstaller-built executable
        executable = os.path.abspath(sys.executable)
        return [executable, *sys.argv[1:]]
    else:
        # Running as a normal Python script
        script = os.path.abspath(sys.argv[0])
        return [sys.executable, script, *sys.argv[1:]]


def launchInTerminal():
    if os.environ.get("LAUNCHED_IN_TERMINAL"):
        return

    system = platform.system()
    env = {**os.environ, "LAUNCHED_IN_TERMINAL": "1"}
    cmd = _get_cmd()

    if system == "Windows":
        subprocess.Popen(["cmd", "/c", "start", "cmd", "/c", *cmd], env=env)

    elif system == "Darwin":  # macOS
        escaped = " ".join(f'"{c}"' for c in cmd)
        apple_script = f'tell application "Terminal" to do script "{escaped}"'
        subprocess.Popen(["osascript", "-e", apple_script])

    elif system == "Linux":
        env = _clean_env(env)
        terminals = [
            ["gnome-terminal", "--", *cmd],
            ["konsole", "-e", *cmd],
            ["xfce4-terminal", "-e", *cmd],
            ["xterm", "-e", *cmd],
        ]
        launched = False
        for term in terminals:
            try:
                proc = subprocess.Popen(
                    term,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                # Give it a moment to fail if it's going to
                try:
                    proc.wait(timeout=0.5)
                    if proc.returncode != 0:
                        err = proc.stderr.read().decode(errors="replace")
                        print(
                            f"[launchInTerminal] {term[0]} failed: {err}",
                            file=sys.stderr,
                        )
                        continue
                except subprocess.TimeoutExpired:
                    pass  # Still running — that's expected for a terminal
                launched = True
                break
            except FileNotFoundError:
                continue

        if not launched:
            raise RuntimeError(
                "No supported terminal emulator found on this Linux system."
            )

    else:
        raise RuntimeError(f"Unsupported platform: {system}")

    sys.exit(0)
