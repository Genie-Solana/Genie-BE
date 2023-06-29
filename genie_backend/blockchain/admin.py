from django.contrib import admin
from django.utils.safestring import mark_safe
from blockchain.models import Network, Wallet, Coin, Collection, NFT, CoinTransactionHistory, NFTTransactionHistory
from genie_backend.utils.models import BaseModelAdmin


class NetworkAdmin(BaseModelAdmin):
    list_display: tuple[str, str] = (
        "id",
        "name",
    )

    list_display_links: tuple[str] = ("name",)
    search_fields: tuple[str] = ("name",)


class WalletAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str] = (
        "id",
        "network",
        "account",
        "address",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str, str] = ("network__name", "address")


class CoinAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str, str] = (
        "id",
        "network",
        "name",
        "ticker",
        "get_symbol",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str, str, str] = ("network__name", "name", "ticker")

    def get_symbol(self, obj) -> str:
        try:
            img_url: str = str(obj.symbol.url)
            return mark_safe(f'<img src="{img_url}" width="100"/>')
        except Exception:
            return "-"

    get_symbol.short_description = "Coin Symbol"


class CollectionAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str, str] = (
        "id",
        "network",
        "name",
        "mint_address",
        "get_thumbnail_image",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str, str] = (
        "network__name",
        "name",
    )

    def get_thumbnail_image(self, obj):
        try:
            img_url: str = str(obj.thumbnail.url)
            return mark_safe(f'<img src="{img_url}" width="100"/>')
        except Exception:
            return "-"

    get_thumbnail_image.short_description = "NFT Collection Thumbnail"


class NFTAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str, str] = (
        "id",
        "network",
        "name",
        "mint_address",
        "collection",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str, str] = (
        "network__name",
        "name",
    )


class CoinTransactionHistoryAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str, str, str, str] = (
        "id",
        "from_inbox",
        "to_inbox",
        "tx_hash",
        "server",
        "coin",
        "amount",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str] = ("server__name",)


class NFTTransactionHistoryAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str, str, str] = (
        "id",
        "from_inbox",
        "to_inbox",
        "tx_hash",
        "server",
        "nft",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str] = ("server__name",)


admin.site.register(Network, NetworkAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Coin, CoinAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(NFT, NFTAdmin)
admin.site.register(CoinTransactionHistory, CoinTransactionHistoryAdmin)
admin.site.register(NFTTransactionHistory, NFTTransactionHistoryAdmin)
