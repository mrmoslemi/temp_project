from django.db import models
from utils.models import CreatedAtModelMixin


class Group(
    models.Model,
):
    title = models.CharField(max_length=50)
    actions = models.ManyToManyField(
        to="Action",
        blank=True,
        related_name="groups",
        related_query_name="group",
        through="GroupAction",
    )


class UserGroup(models.Model, CreatedAtModelMixin):
    user = models.ForeignKey(
        to="User",
        related_name="user_groups",
        related_query_name="user_group",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        to="Group",
        related_name="user_groups",
        related_query_name="user_group",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.user} in {self.group}"
