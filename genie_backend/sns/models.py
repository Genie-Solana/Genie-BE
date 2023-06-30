from datetime import datetime
from typing import Type
from django.db import models
from accounts.models import SocialAccount
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from genie_backend.utils.models import BaseModel
from genie_backend.utils import errors


class SNS(BaseModel):
    class Meta:
        verbose_name: str = "SNS"
        verbose_name_plural: str = "SNS"

    name: str = models.CharField(
        verbose_name="SNS name",
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        help_text="SNS name (ex. Discord, Twitter ...)",
    )

    @classmethod
    def get_by_name(cls: Type["SNS"], name: str) -> "SNS":
        try:
            sns: "SNS" = cls.objects.get(name=name)
        except cls.DoesNotExist as e:
            raise errors.SNSNotFound from e

        return sns

    def __str__(self):
        return f"{self.name}"


class SNSConnectionInfo(BaseModel):
    class Meta:
        verbose_name: str = "SNS-SocialAccount info"
        verbose_name_plural: str = "SNS-SocialAccount info"
        constraints: list[models.UniqueConstraint] = [
            models.UniqueConstraint(
                fields=["sns", "handle", "discriminator"],
                name="unique sns handle",
            ),
        ]

    account: "SocialAccount" = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, related_name="sns_info"
    )

    sns: "SNS" = models.ForeignKey(
        SNS, on_delete=models.PROTECT, related_name="users_info"
    )

    handle: str = models.CharField(
        verbose_name="SNS handle",
        max_length=50,
        blank=False,
        null=False,
        help_text="SNS handle",
    )

    discriminator: str = models.CharField(
        verbose_name="SNS discriminator",
        max_length=100,
        blank=False,
        null=False,
        help_text="SNS discriminator"
    )

    profile_img: "ProcessedImageField" = ProcessedImageField(
        verbose_name="user profile img",
        upload_to="user_profile_imgs",
        help_text="user Profile img",
        null=True,
        blank=True,
        processors=[Thumbnail(400, 400)],
        format="png",
    )

    @classmethod
    def get_sns_connection(
        cls: Type["SNSConnectionInfo"],
        sns: SNS,
        account: SocialAccount,
        discriminator: str,
    ) -> "SNSConnectionInfo":
        try:
            return cls.objects.get(sns=sns, account=account, discriminator=discriminator)
        except cls.DoesNotExist as e:
            raise errors.SNSConnectionNotFound from e

    @classmethod
    def get_account(
        cls: Type["SNSConnectionInfo"], sns: SNS, discriminator: str
    ) -> "SocialAccount":
        try:
            return cls.objects.get(sns=sns, discriminator=discriminator).account
        except cls.DoesNotExist as e:
            raise errors.AccountNotFound from e

    def __str__(self):
        return f"({self.account}) : {self.sns.name} {self.discriminator}"


class Server(BaseModel):
    class Meta:
        verbose_name: str = "Server"
        verbose_name_plural: str = "Server"
        constraints: list[models.UniqueConstraint] = [
            models.UniqueConstraint(
                fields=["sns", "name"],
                name="unique (sns, server)",
            ),
        ]

    sns: "SNS" = models.ForeignKey(
        SNS, on_delete=models.PROTECT, related_name="servers"
    )

    name: str = models.CharField(
        verbose_name="SNS server name",
        max_length=50,
        blank=False,
        null=False,
        help_text="SNS server name (ex. ATIV, NOIS, ...)",
    )

    @classmethod
    def get_server(cls: Type["Server"], server_id: int) -> "Server":
        try:
            return cls.objects.get(id=server_id)
        except cls.DoesNotExist as e:
            raise errors.ServerNotFound from e

    @classmethod
    def get_by_name(cls: Type["Server"], sns, name) -> "Server":
        try:
            return cls.objects.get(sns=sns, name=name)
        except cls.DoesNotExist as e:
            raise errors.ServerNotFound from e 

    def __str__(self):
        return f"{self.sns.name} - {self.name}"


class ServerHistory(BaseModel):
    class Meta:
        verbose_name: str = "Server History"
        verbose_name_plural: str = "Server History"

    server: "Server" = models.ForeignKey(
        Server, on_delete=models.PROTECT, related_name="histories"
    )

    date: datetime = models.DateField(
        verbose_name="Date stored history", auto_now_add=True
    )

    member_count: int = models.IntegerField(
        verbose_name="# of server members", null=True
    )

    daily_chat_count: int = models.IntegerField(
        verbose_name="# of chats in server", null=True
    )

    def __str__(self):
        return f"({str(self.server)}) - {self.date}"
