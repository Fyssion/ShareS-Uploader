# shares-uploader

A script that allows you to upload files to a [ShareS upload server](https://github.com/TannerReynolds/ShareX-Upload-Server).

## Installation

**Better instructions coming soon**

Clone the repo, cd into the directory, and use

```sh
python3 -m pip install .
```

to install the program.

## Usage

To start the program

```sh
python3 -m shares_uploader
```

To edit your configuration
```sh
python3 -m shares_uploader config
```

If you wish to specify a file path for the file through the CLI
```sh
python3 -m shares_uploader -f /path/to/file
```

Full usage

```
usage: shares_uploader [-h] [--file FILE] {config} ...

shares-uploader: an uploader script that assists in uploading to a ShareS webserver

positional arguments:
  {config}
    config              Edit the configuration (url and key)

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  File path for file to upload. This disables the GUI.
```
