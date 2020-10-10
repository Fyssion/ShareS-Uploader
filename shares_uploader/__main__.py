import sys
import argparse
import os.path
import tkinter as tk
from tkinter.filedialog import askopenfilename
import subprocess

import pyperclip

from config import Config, CONFIG_LOCATION
from uploader import Uploader, HTTPException


def notify(text, url=None):
    url = f' "{url}"' if url else ""
    subprocess.run(f'notify-send "{text}"{url} -a "shares-uploader"', shell=True)


def get_filename():
    tk.Tk().withdraw()
    filename = askopenfilename(title="Please select a file to upload")
    return filename


def main():
    parser = argparse.ArgumentParser(
        description="shares-uploader: an uploader script that assists in uploading to a ShareS webserver"
    )
    parser.add_argument("--file", "-fp", help="File path for file to upload. This disables the GUI.")

    args = parser.parse_args()

    if not os.path.isfile(CONFIG_LOCATION):
        config = Config.make_config()

    else:
        config = Config.get_config()

    file = args.file

    if not args.file:
        file = get_filename()

        if not file:
            notify("Aborted upload")
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
