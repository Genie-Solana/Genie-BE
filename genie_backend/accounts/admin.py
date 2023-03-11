from django.contrib import admin
from accounts.models import SocialAccount
from genie_backend.utils.models import BaseModelAdmin


class SocialAccountAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "nickname",
        "pub_key",
    )

    list_display_links = ("id",)
    search_fields = ("nickname",)


admin.site.register(SocialAccount, SocialAccountAdmin)

admin.site.site_header = "Genie Admin Site"
admin.site.site_title = "Genie Admin Site"
admin.site.index_title = "Genie Admin Site"
