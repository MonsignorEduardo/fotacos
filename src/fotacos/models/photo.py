"""Photo database model."""

from tortoise import fields
from tortoise.models import Model


class Photo(Model):
    """Photo model representing stored images."""

    id = fields.IntField(primary_key=True)
    filename = fields.CharField(max_length=255, unique=True, index=True)
    original_url = fields.CharField(max_length=512)
    thumbnail_url = fields.CharField(max_length=512)
    file_size = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
