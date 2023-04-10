from django.db import models
from genie_backend.utils.models import BaseModel
from genie_backend.utils import errors
from accounts.models import SocialAccount
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from typing import Type, Optional


class SNS(BaseModel):
    class Meta:
        verbose_name = "SNS"
        verbose_name_plural = "SNS"

    name: str = models.CharField(
        verbose_name="SNS name",
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        help_text="SNS name (ex. Discord, Twitter ...)",
    )
    
    @classmethod
    def get_by_name(cls: Type['SNS'], name: str) -> Optional['SNS']:
        try:
            sns = cls.objects.get(name=name)
        except cls.DoesNotExist:
            raise errors.SNSNotFound

        return sns

    def __str__(self):
        return f"{self.name}"


class SNSConnectionInfo(BaseModel):
    class Meta:
        verbose_name = "SNS-SocialAccount info"
        verbose_name_plural = "SNS-SocialAccount info"
        constraints = [
            models.UniqueConstraint(
                fields=["sns", "handle"],
                name="unique sns handle",
            ),
        ]

    account = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, related_name="sns_info"
    )

    sns = models.ForeignKey(SNS, on_delete=models.PROTECT, related_name="users_info")

    handle = models.CharField(
        verbose_name="SNS handle",
        max_length=50,
        blank=False,
        null=False,
        help_text="SNS handle",
    )

    profile_img = ProcessedImageField(
        verbose_name="user profile img",
        upload_to="user_profile_imgs",
        help_text="user Profile img",
        null=True,
        blank=True,
        processors=[Thumbnail(400, 400)],
        format="png",
    )
    
    @classmethod
    def get_sns_connection(cls: Type['SNSConnectionInfo'], sns: Type['SNS'], account: Type['SocialAccount'], handle: str) -> Optional['SNSConnectionInfo']:
        try:
            return cls.objects.get(sns=sns, account=account, handle=handle)
        except cls.DoesNotExist:
            raise errors.SNSConnectionNotFound

    def __str__(self):
        return f"({self.account}) : {self.sns.name} {self.handle}"


class Server(BaseModel):
    class Meta:
        verbose_name = "Server"
        verbose_name_plural = "Server"
        constraints = [
            models.UniqueConstraint(
                fields=["sns", "name"],
                name="unique (sns, server)",
            ),
        ]

    sns = models.ForeignKey(SNS, on_delete=models.PROTECT, related_name="servers")

    name = models.CharField(
        verbose_name="SNS server name",
        max_length=50,
        blank=False,
        null=False,
        help_text="SNS server name (ex. ATIV, NOIS, ...)",
    )
    
    @classmethod
    def get_server(cls: Type['Server'], server_id: int) -> Type['Server']: 
        try:
            return cls.objects.get(id=server_id)
        except cls.DoesNotExist:
            raise errors.ServerNotFound

    def __str__(self):
        return f"{self.sns.name} - {self.name}"


class ServerHistory(BaseModel):
    class Meta:
        verbose_name = "Server History"
        verbose_name_plural = "Server History"

    server = models.ForeignKey(Server, on_delete=models.PROTECT, related_name="histories")

    date = models.DateField(verbose_name="Date stored history", auto_now_add=True)

    member_count = models.IntegerField(verbose_name="# of server members", null=True)

    daily_chat_count = models.IntegerField(verbose_name="# of chats in server", null=True)

    def __str__(self):
        return f"({str(self.server)}) - {self.date}"
