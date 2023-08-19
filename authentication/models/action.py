from django.db import models
from utils.models import OrderedModelMixin, CreatedAtModelMixin


class Action(models.Model, OrderedModelMixin):
    key = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    entity = models.ForeignKey(
        to="Entity",
        on_delete=models.CASCADE,
        related_name="actions",
        related_query_name="action",
    )

    def __str__(self) -> str:
        return self.title


class Entity(models.Model, OrderedModelMixin):
    key = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    module = models.ForeignKey(
        to="Module",
        on_delete=models.CASCADE,
        related_name="entities",
        related_query_name="entity",
    )

    def __str__(self) -> str:
        return self.title


class Module(OrderedModelMixin, models.Model):
    key = models.CharField(max_length=20)
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title


class UserAction(models.Model, CreatedAtModelMixin):
    user = models.ForeignKey(
        to="User",
        on_delete=models.CASCADE,
        related_name="user_actions",
        related_query_name="user_action",
    )
    action = models.ForeignKey(
        to="Action",
        on_delete=models.CASCADE,
        related_name="user_actions",
        related_query_name="user_action",
    )


class GroupAction(models.Model, CreatedAtModelMixin):
    group = models.ForeignKey(
        to="Group",
        on_delete=models.CASCADE,
        related_name="group_actions",
        related_query_name="group_action",
    )
    action = models.ForeignKey(
        to="Action",
        on_delete=models.CASCADE,
        related_name="group_actions",
        related_query_name="group_action",
    )
