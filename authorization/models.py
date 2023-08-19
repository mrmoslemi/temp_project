from django.db import models
from utils import mixins


class Group(mixins.SuperModel):
    title = models.CharField(max_length=50)
    users = models.ManyToManyField(
        to="authentication.User",
        blank=True,
        related_name="groups",
        related_query_name="group",
        through="GroupUser",
    )

    def user_count(self):
        return self.users.count()


class GroupUser(mixins.CreatableModel):
    user = models.ForeignKey(
        to="authentication.User",
        on_delete=models.CASCADE,
        related_name="group_users",
        related_query_name="group_user",
    )
    group = models.ForeignKey(
        to="Group",
        on_delete=models.CASCADE,
        related_name="group_users",
        related_query_name="group_user",
    )


class Grant(mixins.CreatableModel):
    access = models.ForeignKey(
        to="Action",
        related_name="grants",
        related_query_name="grant",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        to="Group",
        related_name="grants",
        related_query_name="grant",
        on_delete=models.CASCADE,
    )

    def get_for_user(self):
        actions = models.Action.objects.filter(
            grant__group__user=self.kwargs["user_id"]
        )
        data = dict()
        for action in actions:
            data.setdefault(action.entity.module.key, dict())
            module = data.get(action.entity.module.key)
            module.setdefault(action.entity.key, [])
            entity = module.get(action.entity.key)
            entity.append(action.key)
        return data


class Log(mixins.CreatableModel):
    user = models.ForeignKey(
        to="authentication.User",
        related_name="logs",
        related_query_name="log",
        on_delete=models.CASCADE,
    )
    action = models.ForeignKey(
        to="Action",
        related_name="logs",
        related_query_name="log",
        on_delete=models.CASCADE,
    )
    metadata = models.JSONField(null=True, blank=True, default=None)


class Access(models.Model):
    path = models.CharField(max_length=40)
    title = models.CharField(max_length=30)
    parent = models.ForeignKey(
        to="Access",
        related_name="children",
        related_query_name="child",
        null=True,
        blank=True,
        default=None,
    )


def has_access(user):
    user_actions = Access.objects.filter(grant__group__user=user).select_related(
        "parent", "parent__parent", "parent__parent__parent"
    )
    print(user_actions)
