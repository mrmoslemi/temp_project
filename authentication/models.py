import string
from django.db import models
from django.utils import timezone
from utils import mixins, builders, validators
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings

TOKEN_LENGTH = 40


def default_username():
    return builders.random_string(32, string.ascii_lowercase)


def default_access_token():
    return builders.random_string(length=TOKEN_LENGTH)


def default_refresh_token():
    return builders.random_string(length=TOKEN_LENGTH)


def default_refresh_token_expire():
    return builders.future(seconds=1200)


def default_otp_code():
    return builders.random_string(6, string.digits)


class User(AbstractUser):
    class Meta:
        ordering = ["-date_joined"]

    REQUIRED_FIELDS = ["email", "mobile", "first_name", "last_name"]

    username = models.CharField(
        max_length=150,
        unique=True,
        default=default_username,
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(
        null=True, blank=True, default=None, db_index=True, unique=True
    )
    mobile = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        default=None,
        validators=[validators.mobile],
    )
    groups = None
    user_permissions = None
    verified_email = models.BooleanField(default=False)
    verified_mobile = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    def block(self):
        from . import AccessToken, RefreshToken

        AccessToken.objects.filter(user=self).delete()
        RefreshToken.objects.filter(user=self).delete()
        self.is_blocked = True
        self.save()

    @staticmethod
    def get_by_username(username):
        query = models.Q(email__iexact=username) | models.Q(mobile__iexact=username)
        if User.objects.filter(query).exists():
            return User.objects.filter(query).first()
        else:
            raise User.DoesNotExist()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class OTP(models.Model):
    MOBILE = "mobile"
    EMAIL = "email"
    TYPE_CHOICES = (
        (MOBILE, MOBILE),
        (EMAIL, EMAIL),
    )
    user = models.ForeignKey(to="User", on_delete=models.CASCADE)
    type = models.CharField(max_length=6, choices=TYPE_CHOICES)
    code = models.CharField(max_length=6, default=default_otp_code)
    send = models.IntegerField()
    tried = models.IntegerField()


class AccessToken(mixins.CreatableModel, mixins.DeletableModel):
    user = models.ForeignKey(to="User", on_delete=models.CASCADE)

    token = models.CharField(
        max_length=TOKEN_LENGTH,
        unique=True,
        default=default_access_token,
    )

    expire_at = models.DateTimeField(default=default_refresh_token_expire)
    refresh_token = models.OneToOneField(to="RefreshToken", on_delete=models.CASCADE)

    @staticmethod
    def create_for(user):
        from .. import RefreshToken

        refresh_token = RefreshToken.objects.create(user=user)
        access_token = AccessToken.objects.create(
            user=user, refresh_token=refresh_token
        )
        return access_token

    def check_state(self):
        if self.expire_at > timezone.now():
            self.revoke()

    def revoke(self):
        self.delete()

    @staticmethod
    def verify_token(token: str):
        try:
            access_token = AccessToken.objects.get(deleted_at=None, token=token)
            access_token.check_state()
            if not access_token.deleted:
                return access_token.user
        except AccessToken.DoesNotExist:
            return None
        return None


class RefreshToken(mixins.CreatableModel, mixins.DeletableModel):
    user = models.ForeignKey(to="User", on_delete=models.CASCADE)
    token = models.CharField(
        max_length=TOKEN_LENGTH,
        default=default_access_token,
    )

    def use(self):
        from . import AccessToken

        access_token = AccessToken.create_for(self.user)
        self.delete()
        return access_token
