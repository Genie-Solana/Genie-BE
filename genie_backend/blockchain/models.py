from django.db import models
from genie_backend.utils.models import BaseModel
from accounts.models import SocialAccount


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


class Wallet(BaseModel):
    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallet"
        constraints = [
            models.UniqueConstraint(
                fields=["network", "address"],
                name="unique (network, address)",
            ),
        ]

    network = models.ForeignKey(
        Network, on_delete=models.CASCADE, related_name="wallets"
    )

    account = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, related_name="wallets"
    )

    address = models.CharField(
        verbose_name="wallet address",
        max_length=100,
        blank=False,
        null=False,
        help_text="wallet address"
    )

    def __str__(self):
        return f"{self.network.name} - {self.address}"
