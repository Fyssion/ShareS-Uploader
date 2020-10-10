import configparser
import os
import re
from pathlib import Path
import tkinter as tk
import functools


HOME = str(Path.home())
CONFIG_LOCATION = f"{HOME}/shares-uploader/uploader.conf"
# CONFIG_LOCATION = "~/shares-uploader.conf"


class Config(configparser.ConfigParser):
    """Represents a user's config"""

    @classmethod
    def get_config(cls):
        self = cls()
        self.read(CONFIG_LOCATION)
        return self

    @classmethod
    def make_config(cls):
        self = cls()
        self["UPLOADER"] = {
            "url": "your_server_url_here",
            "key": "your_uploader_key_here",
        }

        os.mkdir(f"{HOME}/shares-uploader")

        with open(CONFIG_LOCATION, "w") as f:
            self.write(f)

        return self


class ConfigGUI(tk.Frame):
    """GUI for entering config information"""

    def __init__(self, master, config):
        super().__init__(master)

        self.config = config

        self.url_label = tk.Label(self, text="Image Server URL")
        self.url_label.grid(row=0, column=0)

        self.url = tk.StringVar()
        self.url.set(self.config["UPLOADER"]["url"])

        self.url_entry = tk.Entry(self, textvariable=self.url, width=40)
        self.url_entry.grid(row=0, column=1)
        self.key_label = tk.Label(self, text="Upload Key").grid(row=1, column=0)

        self.key = tk.StringVar()
        self.key.set(self.config["UPLOADER"]["key"])

        self.key_entry = tk.Entry(self, textvariable=self.key, show="*", width=40)
        self.key_entry.grid(row=1, column=1)

        self.show_key = tk.BooleanVar()
        self.show_key_box = tk.Checkbutton(
            self, text="Show key", variable=self.show_key, command=self.toggle_key
        )
        self.show_key_box.grid(row=2, column=0)

        self.error_text = tk.StringVar()
        self.error_text.set("")
        self.error_label = tk.Label(self, textvariable=self.error_text, fg="red")
        self.error_label.grid(row=3, column=0)
        self.error_label.grid_forget()

        self.save_button = tk.Button(self, text="Save", command=self.validate_url)
        self.save_button.grid(row=6, column=0)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def validate_url(self):
        regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        if not re.match(regex, self.url.get()):
            self.error_text.set("Your URL is not a valid URL.")
            return

        self.config["UPLOADER"]["url"] = self.url.get()
        self.config["UPLOADER"]["key"] = self.key.get()
        self.config.write()

        self.master.destroy()

    def toggle_key(self):
        self.key_entry["show"] = "" if self.show_key.get() else "*"
