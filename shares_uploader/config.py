import configparser
import os
from pathlib import Path


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
            "password": "your_uploader_password_here",
        }

        os.mkdir(f"{HOME}/shares-uploader")

        with open(CONFIG_LOCATION, "w") as f:
            self.write(f)

        return self
