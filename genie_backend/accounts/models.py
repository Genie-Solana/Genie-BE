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


class Inbox(BaseModel):
    class Meta:
        verbose_name = "Inbox"
        verbose_name_plural = "Inbox"
        constraints = [
            models.UniqueConstraint(
                fields=["pub_key", "network", "sns"],
                name="unique (pub_key, network, sns)",
            ),
        ]

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

    account = models.ForeignKey(
        SocialAccount, on_delete=models.SET_NULL, related_name="inboxes", null=True
    )

    network = models.ForeignKey(
        'blockchain.Network', on_delete=models.PROTECT, related_name="inboxes"
    )

    sns = models.ForeignKey('sns.SNS', on_delete=models.PROTECT, related_name="inboxes")

    def __str__(self):
        return f"{self.account.nickname}({self.sns.name}) {self.pub_key}"
