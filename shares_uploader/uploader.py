import requests


class HTTPException(Exception):
    pass


class Unauthorized(HTTPException):
    def __init__(self):
        super().__init__("The key provided is unauthorized. Please check your key.")


class FailedRequest(HTTPException):
    def __init__(self, text):
        self.text = text
        super().__init__(f"Failed Request: {text}")


class Uploader:
    """Represents an uploader uploading files to ShareS"""

    def __init__(self, config):
        self.config = config
        self.url = config["UPLOADER"]["url"]
        self.password = config["UPLOADER"]["password"]

    def upload(self, filepath):
        """Upload a file to the server"""
        url = self.url + "/api/files"
        headers = {"user-agent": "shares-uploader script"}
        files = {"fdata": open(filepath, "rb"), "key": (None, self.password)}

        response = requests.post(url, files=files, headers=headers)

        if response.status_code == 200:
            return response.text

        if response.status_code == 401:
            raise Unauthorized()

        else:
            raise FailedRequest(response.text)
