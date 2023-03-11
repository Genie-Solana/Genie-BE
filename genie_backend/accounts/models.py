from django.db import models
from genie_backend.utils.models import BaseModel


class SocialAccount(BaseModel):
    class Meta:
        verbose_name = "Genie user"
        verbose_name_plural = "Genie users"

    nickname = models.CharField(
        verbose_name="nickname",
        max_length=50,
        blank=False,
        null=False,
        help_text="nickname used in genie service",
    )

    pub_key = models.CharField(
        verbose_name="public key",
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="public key"
    )

    secret_key = models.CharField(
        verbose_name="secret key",
        max_length=100,
        blank=False,
        null=False,
        help_text="secret key"
    )

    def __str__(self):
        return f"{self.nickname} - {self.pub_key}"
