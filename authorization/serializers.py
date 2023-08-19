from rest_framework import serializers
from . import models
from authentication import models as auth_models
from utils import requests


# access hire
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Action
        fields = ["path", "title"]


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entity
        fields = ["key", "title", "actions"]

    actions = ActionSerializer(many=True)


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Module
        fields = ["key", "title", "entities"]

    entities = EntitySerializer(many=True)


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = ["uuid", "title", "user_count"]


class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = ["title"]


class GroupRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = ["uuid", "title", "users", "grants"]


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grant
        fields = ["action"]

    action = ActionSerializer()


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth_models.User
        fields = [
            "username",
            "email",
            "mobile",
            "first_name",
            "last_name",
            "is_superuser",
        ]
