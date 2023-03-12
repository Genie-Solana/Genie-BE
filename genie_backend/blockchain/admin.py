from django.contrib import admin
from genie_backend.utils.models import BaseModelAdmin
from blockchain.models import Network, Wallet


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


admin.site.register(Network, NetworkAdmin)
admin.site.register(Wallet, WalletAdmin)

