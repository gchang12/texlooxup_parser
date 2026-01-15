"""
Downloads and extracts TeX for the Impatient source to 'input/'
"""

from zipfile import ZipFile
from io import open
from os import PathLike
from pathlib import Path

import requests

SOURCE_URL = "https://mirrors.ctan.org/info/impatient.zip"
TARGET_DIR = "input/"
TARGET_FILE = "input/impatient.zip"

def download_src(source_url: str) -> requests.Response:
    """
    Returns the response from sending a GET request to `source_url`.
    """
    response = requests.get(source_url)
    return response

def write_bytes_to_file(content: bytes, target_file: PathLike | str) -> int:
    """
    Writes binary content in `content` to `target_file`
    """
    with open(target_file, mode="wb") as wb_file:
        return wb_file.write(content)

def unzip_file(src_file: PathLike | str, target_dir: PathLike | str):
    """
    Extracts `src_file` contents to `target_dir`.
    """
    with ZipFile(src_file) as zip_file:
        zip_file.extractall(path=target_dir)

if __name__ == "__main__":
    import shutil
    def compile_src():
        """
        Sets up 'input/' folder and its complementary files.
        """
        shutil.rmtree("input/impatient/", ignore_errors=True)
        Path(TARGET_DIR).mkdir(exist_ok=True)
        response = download_src(SOURCE_URL)
        write_bytes_to_file(response.content, TARGET_FILE)
        unzip_file(TARGET_FILE, TARGET_DIR)
    compile_src()
