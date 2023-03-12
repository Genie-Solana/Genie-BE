from django.contrib import admin
from django.utils.safestring import mark_safe
from genie_backend.utils.models import BaseModelAdmin
from sns.models import SNS, SNSConnectionInfo, Server, ServerHistory


class SNSAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "name",
    )

    list_display_links = ("name",)
    search_fields = ("name",)


class SNSConnectionInfoAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "account",
        "sns",
        "handle",
        "get_thumbnail_image",
    )

    list_display_links = ("id",)
    search_fields = (
        "account__nickname",
        "sns__name",
        "handle",
    )

    def get_thumbnail_image(self, obj):
        try:
            img_url = str(obj.profile_img.url)
            return mark_safe(f'<img src="{img_url}" width="100"/>')
        except Exception:
            return "-"

    get_thumbnail_image.short_description = "User Thumbnail"


class ServerAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "sns",
        "name",
    )

    list_display_links = ("id",)
    search_fields = (
        "sns__name",
        "name",
    )


class ServerHistoryAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "server",
        "date",
        "member_count",
        "daily_chat_count",
    )

    list_display_links = ("id", )
    search_fields = (
        "server__name",
        "server__sns__name",
    )


admin.site.register(SNS, SNSAdmin)
admin.site.register(SNSConnectionInfo, SNSConnectionInfoAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(ServerHistory, ServerHistoryAdmin)

