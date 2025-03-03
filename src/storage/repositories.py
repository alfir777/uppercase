import uuid
from typing import Protocol

from django.shortcuts import get_object_or_404

from storage.entities import FileEntity
from storage.models import StoredFile


class FileRepository(Protocol):
    @staticmethod
    def get_file(file_id: str) -> FileEntity:
        ...

    @staticmethod
    def save_file(file_id: str, user_id: str, file_name: str) -> FileEntity:
        ...


class FileDBRepository(FileRepository):
    @staticmethod
    def get_file(file_id: str) -> FileEntity:
        db_file = get_object_or_404(StoredFile, id=file_id)
        return FileEntity.from_model(db_file)

    @staticmethod
    def save_file(file_id: str, user_id: str, file_name: str) -> FileEntity:
        db_file = StoredFile.objects.create(id=uuid.UUID(file_id), user_id=user_id, original_name=file_name)
        return FileEntity.from_model(db_file)
