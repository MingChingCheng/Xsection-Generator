import os
import sys


def get_resource_path(relative_path: str) -> str:
    """Get the absolute path to a resource file."""

    if hasattr(sys, "_MEIPASS"):
        # when bundled by PyInstaller, 
        # the app will be extracted to a temporary folder (sys._MEIPASS)
        base_path = sys._MEIPASS
    else:
        # get the absolute path of file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # get the root path of the project
        base_path = os.path.abspath(os.path.join(current_dir, "..", ".."))

    return os.path.join(base_path, relative_path)
