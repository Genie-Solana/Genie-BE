from django.contrib import admin
from django.utils.safestring import mark_safe
from genie_backend.utils.models import BaseModelAdmin
from blockchain.models import Network, Wallet, Coin


class NetworkAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "name",
    )

    list_display_links = ("name",)
    search_fields = ("name",)


class WalletAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "network",
        "account",
        "address",
    )

    list_display_links = ("id",)
    search_fields = ("network__name", "address")


class CoinAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "network",
        "name",
        "ticker",
        "get_symbol",
    )

    list_display_links = ("id",)
    search_fields = ("network__name", "name", "ticker")

    def get_symbol(self, obj):
        try:
            img_url = str(obj.symbol.url)
            return mark_safe(f'<img src="{img_url}" width="100"/>')
        except Exception:
            return "-"

    get_symbol.short_description = "Coin Symbol"


admin.site.register(Network, NetworkAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Coin, CoinAdmin)
