from typing import Iterable, Optional
from django.db import models
from django.utils import timezone
import uuid


class UUIDModel(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(
        unique=True, db_index=True, default=uuid.uuid4, editable=False
    )


class CreatableModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(default=timezone.now)


class UpdatableModel(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(null=True, blank=True, default=None)

    def save(
        self,
        force_insert: bool = ...,
        force_update: bool = ...,
        using: str | None = ...,
        update_fields: Iterable[str] | None = ...,
    ) -> None:
        self.updated_at = timezone.now()
        super().save(force_insert, force_update, using, update_fields)


class DeletableModel(models.Model):
    class Meta:
        abstract = True

    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()


class OrderedModel(models.Model):
    class Meta:
        abstract = True
        ordering = ["order"]

    order = models.FloatField(default=0)

    def __gt__(self, other):
        return self.order > other.order

    def __lt__(self, other):
        return self.order < other.order

    def __ge__(self, other):
        return self.order >= other.order

    def __le__(self, other):
        return self.order <= other.order


class AuditableModel(CreatableModel, UpdatableModel, DeletableModel):
    class Meta:
        abstract = True


class SuperModel(AuditableModel, OrderedModel, UUIDModel):
    class Meta:
        abstract = True
