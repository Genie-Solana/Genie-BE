from django.db import models
from genie_backend.utils.models import BaseModel


class SNS(BaseModel):
    class Meta:
        verbose_name = "SNS"
        verbose_name_plural = "SNS"

    name = models.CharField(
        verbose_name="SNS name",
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        help_text="SNS name (ex. Discord, Twitter ...)",
    )

    def __str__(self):
        return f"{self.name}"