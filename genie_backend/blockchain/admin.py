from django.contrib import admin
from genie_backend.utils.models import BaseModelAdmin
from blockchain.models import Network


class NetworkAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "name",
    )

    list_display_links = ("name",)
    search_fields = ("name",)


admin.site.register(Network, NetworkAdmin)
