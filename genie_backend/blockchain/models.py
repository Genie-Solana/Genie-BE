from django.db import models
from genie_backend.utils.models import BaseModel
from accounts.models import SocialAccount
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


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


class Coin(BaseModel):
    class Meta:
        verbose_name = "Coin"
        verbose_name_plural = "Coin"
        constraints = [
            models.UniqueConstraint(
                fields=["network", "name"],
                name="unique (network, coin_name)",
            ),
        ]

    network = models.ForeignKey(
        Network, on_delete=models.CASCADE, related_name="coins"
    )

    name = models.CharField(
        verbose_name="Coin name",
        max_length=50,
        blank=False,
        null=False,
        help_text="Coin name (ex. Solana, USDCoin ...)",
    )

    ticker = models.CharField(
        verbose_name="Coin ticker",
        max_length=10,
        blank=False,
        null=False,
        help_text="Coin ticker (ex. SOL, USDC ...)",
    )

    symbol = ProcessedImageField(
        verbose_name="coin symbol",
        upload_to="coin_symbol",
        help_text="coin symbol",
        null=True,
        blank=True,
        processors=[Thumbnail(100, 100)],
        format="png",
    )

    def __str__(self):
        return f"{self.network.name} - {self.name}"


class Collection(BaseModel):
    class Meta:
        verbose_name = "NFT Collection"
        verbose_name_plural = "NFT Collection"
        constraints = [
            models.UniqueConstraint(
                fields=["network", "name"],
                name="unique (network, nft_collection_name)",
            ),
        ]

    network = models.ForeignKey(
        Network, on_delete=models.CASCADE, related_name="nft_collections"
    )

    name = models.CharField(
        verbose_name="NFT name",
        max_length=50,
        blank=False,
        null=False,
        help_text="NFT name (ex. NOIS, Sodead ...)",
    )

    mint_address = models.CharField(
        verbose_name="mint address",
        max_length=100,
        blank=True,
        null=True,
        help_text="mint address"
    )

    thumbnail = ProcessedImageField(
        verbose_name="nft thumbnail",
        upload_to="nft_thumbnail",
        help_text="nft thumbnail",
        null=True,
        blank=True,
        processors=[Thumbnail(400, 400)],
        format="png",
    )

    def __str__(self):
        return f"{self.network.name} - {self.name}"
