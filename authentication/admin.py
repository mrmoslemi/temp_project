from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "date_joined", "is_superuser"]


@admin.register(models.AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "token", "expire_at"]
    raw_id_fields = ["user"]
