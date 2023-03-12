from django.contrib import admin
from accounts.models import SocialAccount, Inbox
from genie_backend.utils.models import BaseModelAdmin


class SocialAccountAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "nickname",
        "pub_key",
    )

    list_display_links = ("id",)
    search_fields = ("nickname",)


class InboxAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "account",
        "network",
        "sns",
        "pub_key",
    )

    list_display_links = ("id",)
    search_fields = ("account__nickname", "sns__name", "network__name", )


admin.site.register(SocialAccount, SocialAccountAdmin)
admin.site.register(Inbox, InboxAdmin)

admin.site.site_header = "Genie Admin Site"
admin.site.site_title = "Genie Admin Site"
admin.site.index_title = "Genie Admin Site"
