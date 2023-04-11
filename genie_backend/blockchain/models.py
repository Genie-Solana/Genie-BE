from django.db import models
from genie_backend.utils.models import BaseModel
from genie_backend.utils import errors
from accounts.models import SocialAccount
from sns.models import Server
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from typing import Type, Optional


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
    
    @classmethod 
    def get_by_name(cls: Type['Network'], name: str) -> Optional['Network']:
        try:
            network = cls.objects.get(name=name)
        except cls.DoesNotExist:
            raise errors.NetworkNotFound

        return network

    def __str__(self):
        return f"{self.name}"

    @classmethod 
    def get_by_name(cls: Type['Network'], name: str) -> Type['Network']:
        try:
            network = cls.objects.get(name=name)
        except cls.DoesNotExist:
            raise errors.NetworkNotFound

        return network


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
    
    @classmethod
    def get_by_network_address(cls: Type['Wallet'], network: Type['Network'], address: str) -> Type['Wallet']:
        try:
            wallet = cls.objects.get(network=network, address=address)
        except cls.DoesNotExist:
            raise errors.WalletNotFound

        return wallet

    @classmethod
    def get_by_network_address(cls: Type['Wallet'], network: Type['Network'], address: str) -> Optional['Wallet']:
        try:
            wallet = cls.objects.get(network=network, address=address)
        except cls.DoesNotExist:
            raise errors.WalletNotFound

        return wallet

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


class TransactionHistory(BaseModel):
    class Meta:
        verbose_name = "Transaction History"
        verbose_name_plural = "Transaction History"

    TYPE_CHOICES = (("COIN", "COIN TX"), ("NFT", "NFT TX"))
    type = models.CharField(
        verbose_name="TX type",
        blank=False,
        max_length=10,
        default="COIN",
        choices=TYPE_CHOICES,
        help_text="TX type",
    )

    from_account = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, related_name="from_tx", null=False, blank=False
    )

    to_account = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, related_name="to_tx", null=True, blank=True
    )

    tx_hash = models.CharField(
        verbose_name="tx_hash",
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="tx hash"
    )

    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="tx_histories", null=False, blank=False, unique=True
    )

    def __str__(self):
        return f"{self.tx_hash}({self.type})"
