import sys
import argparse
import os.path
import sys
import tkinter as tk
from tkinter.filedialog import askopenfilename

import pyperclip

import subprocess
if sys.platform == "win32":
    import win10toast
    toaster = win10toast.ToastNotifier()

from .config import CONFIG_LOCATION, Config, ConfigGUI
from .uploader import Uploader, HTTPException


def notify(text, url=None):
    if sys.platform == "win32":
        toaster.show_toast(text, url, duration=10)
    else:
        url = f' "{url}"' if url else ""
        subprocess.run(f'notify-send "{text}"{url} -a "shares-uploader"', shell=True)


def start_config_gui(config):
    root = tk.Tk()
    root.title("Edit Configuration")

    ConfigGUI(root, config).grid(row=0, column=0)

    root.wait_window()


def get_filename():
    tk.Tk().withdraw()
    filename = askopenfilename(title="Please select a file to upload")
    return filename


def main():
    parser = argparse.ArgumentParser(
        description="shares-uploader: an uploader script that assists in uploading to a ShareS webserver"
    )
    parser.add_argument(
        "--file", "-f", help="File path for file to upload. This disables the GUI."
    )

    subparsers = parser.add_subparsers(dest="command")
    config_parser = subparsers.add_parser(
        "config",
        help="Edit the configuration (url and key)",
    )

    args = parser.parse_args()

    if not os.path.isfile(CONFIG_LOCATION):
        config = Config.make_config()
        start_config_gui(config)

        if args.command:
            return

    else:
        config = Config.get_config()

    if args.command:
        start_config_gui(config)
        return

    file = args.file

    if not args.file:
        file = get_filename()

        if not file:
            return

    # perform the upload and copy to clipboard

    uploader = Uploader(config)

    try:
        url = uploader.upload(file)

    except HTTPException as exc:
        notify(str(exc))

    else:
        pyperclip.copy(url)
        notify("Copied URL to clipboard", url)


if __name__ == "__main__":
    main()
