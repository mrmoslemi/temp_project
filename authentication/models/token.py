from django.db import models
from datetime import timedelta
from django.utils import timezone
from utils.models import (
    CreatedAtModelMixin,
    DeletedAtModelMixin,
    get_random_generator,
    get_date_generator,
)
from django.conf import settings

TOKEN_LENGTH = 40


class AccessToken(models.Model, CreatedAtModelMixin, DeletedAtModelMixin):
    user = models.ForeignKey(to="User", on_delete=models.CASCADE)

    token = models.CharField(
        max_length=TOKEN_LENGTH,
        unique=True,
        default=get_random_generator(length=TOKEN_LENGTH),
    )

    expire_at = models.DateTimeField(default=get_date_generator(1200))
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
            access_token = AccessToken.objects.get(deleted=False, token=token)
            access_token.check_state()
            if not access_token.deleted:
                return access_token.user
        except AccessToken.DoesNotExist:
            return None
        return None


class RefreshToken(models.Model, CreatedAtModelMixin, DeletedAtModelMixin):
    user = models.ForeignKey(to="User", on_delete=models.CASCADE)
    token = models.CharField(
        max_length=TOKEN_LENGTH,
        default=get_random_generator(length=TOKEN_LENGTH),
    )

    def use(self):
        from .. import AccessToken

        access_token = AccessToken.create_for(self.user)
        self.delete()
        return access_token
