from django.utils import timezone
from django.db import models
import string
from datetime import timedelta
import random


def get_random_generator(
    length: int = 32, charset: str = string.ascii_letters + string.digits
):
    return "".join(random.choice(charset) for i in range(length))


def get_date_generator(seconds: int):
    return timezone.now() + timedelta(seconds=seconds)


class DeletedAtModelMixin:
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    def delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()


class OrderedModelMixin:
    order = models.FloatField(default=0)

    def __gt__(self, other):
        return self.order > other.order

    def __lt__(self, other):
        return self.order < other.order

    def __ge__(self, other):
        return self.order >= other.order

    def __le__(self, other):
        return self.order <= other.order


class CreatedAtModelMixin:
    created_at = models.DateTimeField(auto_now_add=True)


class UpdatedAtModelMixin:
    updated_at = models.DateTimeField(auto_now=True)
