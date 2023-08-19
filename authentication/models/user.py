from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from utils.models import get_random_generator
import string


class User(AbstractUser):
    class Meta:
        ordering = ["-date_joined"]

    username = models.CharField(
        max_length=150,
        unique=True,
        default=get_random_generator(32, string.ascii_lowercase),
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(
        null=True, blank=True, default=None, db_index=True, unique=True
    )
    mobile = models.EmailField(
        null=True, blank=True, default=None, db_index=True, unique=True
    )
    verified_email = models.BooleanField(default=False)
    verified_mobile = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = None

    def block(self):
        from . import AccessToken, RefreshToken

        AccessToken.objects.filter(user=self).delete()
        RefreshToken.objects.filter(user=self).delete()
        self.is_blocked = True
        self.save()

    @staticmethod
    def get_by_username(username):
        query = Q(email__iexact=username) | Q(mobile__iexact=username)
        if User.objects.filter(query).exists():
            return User.objects.filter(query).first()
        else:
            raise User.DoesNotExist()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
