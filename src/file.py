import os
from pathlib import Path

from fastapi import UploadFile

from .constants import FILE_DIR


class FileService:
    def __init__(self, file_dir: str):
        self.file_dir = file_dir

    def save_file(self, upload_file: UploadFile, file_name=None) -> str:
        if file_name is None:
            file_name = upload_file.filename

        path_to_file = '{}/{}'.format(self.file_dir, file_name)
        dirs = Path(path_to_file).resolve().parent

        if not os.path.exists(dirs):
            os.makedirs(dirs)

        with open(Path(path_to_file), "wb+") as f:
            f.write(upload_file.file.read())

        return path_to_file

    def remove(self, path_to_file: str):
        os.remove(path_to_file)


file_service = FileService(file_dir=FILE_DIR)
