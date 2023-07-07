from django.contrib import admin
from django.utils.safestring import mark_safe
from accounts.models import SocialAccount, Inbox
from genie_backend.utils.models import BaseModelAdmin


class SocialAccountAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str] = (
        "id",
        "nickname",
        "pub_key",
        "get_thumbnail_image",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str] = ("nickname",)

    def get_thumbnail_image(self, obj) -> str:
        try:
            img_url: str = str(obj.profile_img.url)
            return mark_safe(f'<img src="{img_url}" width="100"/>')
        except Exception:
            return "-"

    get_thumbnail_image.short_description = "User Thumbnail"


class InboxAdmin(BaseModelAdmin):
    list_display: tuple[str, str, str, str, str] = (
        "id",
        "account",
        "network",
        "sns",
        "pub_key",
    )

    list_display_links: tuple[str] = ("id",)
    search_fields: tuple[str, str, str] = (
        "account__nickname",
        "sns__name",
        "network__name",
    )


admin.site.register(SocialAccount, SocialAccountAdmin)
admin.site.register(Inbox, InboxAdmin)

admin.site.site_header = "Genie Admin Site"
admin.site.site_title = "Genie Admin Site"
admin.site.index_title = "Genie Admin Site"
