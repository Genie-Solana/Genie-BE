from django.db import models
from genie_backend.utils.models import BaseModel


class Network(BaseModel):
    class Meta:
        verbose_name = "Network"
        verbose_name_plural = "Network"

    name = models.CharField(
        verbose_name="Network name",
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        help_text="Network name (ex. Solana ...)",
    )

    def __str__(self):
        return f"{self.name}"
