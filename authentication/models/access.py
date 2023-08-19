from django.db import models
from utils.models import CreatedAtModelMixin


class Access(models.Model, CreatedAtModelMixin):
    user = models.ForeignKey(to="User", on_delete=models.CASCADE)
    action = models.ForeignKey(to="Action", on_delete=models.CASCADE)
    uuid = models.CharField(max_length=36, null=True, blank=True, default=None)
    metadata = models.JSONField(null=True, blank=True, default=None)

    def __str__(self) -> str:
        return "%s - %s - %s - %s" % (self.action if self.action else "All")
