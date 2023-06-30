from typing import List, TYPE_CHECKING, Type
from django.db import models
from genie_backend.utils.models import BaseModel


if TYPE_CHECKING:
    from blockchain.models import Network
    from sns.models import SNS


class SocialAccount(BaseModel):
    class Meta:
        verbose_name: str = "Genie user"
        verbose_name_plural: str = "Genie users"

    nickname: str = models.CharField(
        verbose_name="nickname",
        max_length=50,
        blank=False,
        null=False,
        help_text="nickname used in genie service",
    )

    pub_key: str = models.CharField(
        verbose_name="public key",
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="public key",
    )

    secret_key: str = models.CharField(
        verbose_name="secret key",
        max_length=400,
        blank=False,
        null=False,
        help_text="secret key",
    )

    def __str__(self):
        return f"{self.nickname} - {self.pub_key}"


class Inbox(BaseModel):
    class Meta:
        verbose_name: str = "Inbox"
        verbose_name_plural: str = "Inbox"
        constraints: List[models.UniqueConstraint] = [
            models.UniqueConstraint(
                fields=["pub_key", "network", "sns"],
                name="unique (pub_key, network, sns)",
            ),
        ]

    pub_key: str = models.CharField(
        verbose_name="public key",
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="public key",
    )

    secret_key: str = models.CharField(
        verbose_name="secret key",
        max_length=400,
        blank=False,
        null=False,
        help_text="secret key",
    )

    account: "SocialAccount" = models.ForeignKey(
        SocialAccount, on_delete=models.SET_NULL, related_name="inboxes", null=True
    )

    network: "Network" = models.ForeignKey(
        "blockchain.Network", on_delete=models.PROTECT, related_name="inboxes"
    )

    sns: "SNS" = models.ForeignKey(
        "sns.SNS", on_delete=models.PROTECT, related_name="inboxes"
    )

    @classmethod
    def get_inbox(
        cls: Type["Inbox"], sns, account, network
        ) -> "Inbox":
        try:
            return cls.objects.get(sns=sns, account=account, network=network)
        except cls.DoesNotExist as e:
            raise errors.InboxNotFound from e

    def __str__(self):
        return f"{self.account.nickname}({self.sns.name}) {self.pub_key}"
