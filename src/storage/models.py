import uuid

from django.db import models


class StoredFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_name = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='files')
    created_at = models.DateTimeField(auto_now_add=True)
