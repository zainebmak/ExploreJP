import os
import sys


def configure_console() -> None:
    if sys.platform == "win32":
        os.system("chcp 65001 > nul")
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
            sys.stdin.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass
    elif hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
            sys.stdin.reconfigure(encoding="utf-8")
        except OSError:
            pass


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pause(message: str = "Press ENTER to continue...") -> None:
    input(message)


def read_choice(prompt: str = "Choose an option: ") -> str:
    return input(prompt).strip()


def print_line(text: str = "") -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))
