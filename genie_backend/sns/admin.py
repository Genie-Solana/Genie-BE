from django.contrib import admin
from genie_backend.utils.models import BaseModelAdmin
from sns.models import SNS


class SNSAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "name",
    )

    list_display_links = ("name",)
    search_fields = ("name",)


admin.site.register(SNS, SNSAdmin)
