from uuid import uuid4

from django.db import models


class DatedModel(models.Model):
    """
    A base abstract model with created/last updated fields and a UUID
    primary key.
    """

    id = models.UUIDField(primary_key=True, default=uuid4)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    last_updated = models.DateTimeField(db_index=True, auto_now=True)

    class Meta:
        abstract = True
