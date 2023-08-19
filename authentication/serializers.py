from rest_framework import serializers
from . import models


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
