from django.contrib import admin
from . import models


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["title", "uuid", "created_at", "updated_at", "deleted_at"]
