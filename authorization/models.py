from django.db import models
from utils import mixins


class Group(mixins.SuperModel):
    title = models.CharField(max_length=50)
    users = models.ManyToManyField(to="authentication.User", blank=True)


class Module(mixins.BaseModel):
    key = models.CharField(max_length=20)
    title = models.CharField(max_length=50)


class Entity(mixins.BaseModel):
    key = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    module = models.ForeignKey(to="Module", on_delete=models.CASCADE)


class Action(mixins.BaseModel):
    LIST = "list"
    PAGINATE = "paginate"
    CREATE = "create"
    RETRIEVE = "retrieve"
    UPDATE = "update"
    DELETE = "delete"

    key = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    entity = models.ForeignKey(to="Entity", on_delete=models.CASCADE)

    @staticmethod
    def get_with_path(path: str):
        (action, entity, module) = Action.parse_path(path)
        try:
            return Action.objects.get(
                key=action, entity__key=entity, entity__module__key=module
            )
        except Action.MultipleObjectsReturned:
            raise Exception(f"multiple actions returned for path {path}")
        except Action.DoesNotExist:
            return None

    @staticmethod
    def parse_path(path: str):
        parts = path.split(".")
        if len(parts) != 3:
            raise ValueError
        return (parts[0], parts[1], parts[2])


class Grant(mixins.CreatableModel):
    action = models.ForeignKey(to="Action")
    group = models.ForeignKey(to="Group", on_delete=models.CASCADE)

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
    user = models.ManyToManyField(to="authentication.User", blank=True)
    action = models.ForeignKey(to="Action", on_delete=models.CASCADE)
