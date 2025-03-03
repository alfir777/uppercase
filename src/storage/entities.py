from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from storage.models import StoredFile


@dataclass
class FileEntity:
    file_id: str
    user_id: int
    created_at: datetime
    original_name: Optional[str] = None

    @classmethod
    def from_model(cls, model: StoredFile):
        return cls(str(model.id), model.user.id, model.created_at, model.original_name)
