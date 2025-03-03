import os
import uuid
import zipfile
from typing import Optional

from src.settings import STORAGE_DIR

from storage.entities import FileEntity
from storage.repositories import FileRepository

CHUNK_SIZE = 1 * 1024 * 1024


class FileService:
    def __init__(self, repository: FileRepository) -> None:
        self.repo = repository

    def save_file(self, file, user_id) -> str:
        file_id = str(uuid.uuid4())
        self._save_chunks(file, file_id)
        self.repo.save_file(file_id, user_id, file.name)
        return file_id

    def get_file(self, file_id) -> Optional[FileEntity]:
        return self.repo.get_file(file_id)

    def _save_chunks(self, file, file_id) -> None:
        file_dir = os.path.join(STORAGE_DIR, file_id)
        os.makedirs(file_dir, exist_ok=True)
        for part_index, chunk in enumerate(iter(lambda: file.read(CHUNK_SIZE), b'')):
            part_path = os.path.join(file_dir, f'part_{part_index}')
            with open(part_path, 'wb') as part_file:
                part_file.write(chunk)
            self._zip_file(part_path)

    @staticmethod
    def _zip_file(part_path) -> None:
        zip_path = f"{part_path}.zip"
        with zipfile.ZipFile(zip_path, 'w') as f:
            f.write(part_path, os.path.basename(part_path))
        os.remove(part_path)

    @staticmethod
    def unzip_file(file_id) -> str:
        file_dir = os.path.join(STORAGE_DIR, str(file_id))
        os.makedirs(os.path.join(STORAGE_DIR, "_restored/"), exist_ok=True)
        response_file_path = os.path.join(STORAGE_DIR, f"_restored/{file_id}", )

        with open(response_file_path, 'wb') as outfile:
            for part in sorted(os.listdir(file_dir), key=lambda x: int(x.split('_')[1].split('.')[0])):
                part_path = os.path.join(file_dir, part)
                with zipfile.ZipFile(part_path, 'r') as ff:
                    outfile.write(ff.read(ff.namelist()[0]))

        return response_file_path
