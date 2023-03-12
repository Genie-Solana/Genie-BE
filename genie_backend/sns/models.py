from django.db import models
from genie_backend.utils.models import BaseModel
from accounts.models import SocialAccount
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


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

    def __str__(self):
        return f"{self.sns.name} - {self.name}"
