from rest_framework import serializers
from . import models


# access hire
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Action
        fields = ["key", "title"]


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


class AccessTokenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccessToken
        fields = ["username", "password"]

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = models.User.get_by_username(username)
        if user:
            correct_password = user.check_password(password)
            return super().validate(attrs)


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "username", "email", "mobile"]


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = ["id", "title"]


class GroupRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = ["id", "title", "users"]
