from django.conf import settings
from django.contrib import admin

from .models import UrlRecord

site_title = settings.ADMIN_PANEL_WEBSITE_TITLE
# change admin interface
admin.site.index_title = site_title
admin.site.site_header = site_title
admin.site.site_title = site_title
admin.site.site_url = "/"


class UrlRecordAdmin(admin.ModelAdmin):

    # things to go on admin page
    list_display = [
        "original_url",
        "short_url",
        "date_created",
        "date_expiry",
        "user",
        "is_expired",
    ]
    # can filter by date_created and date_expiry
    list_filter = ["date_created", "date_expiry", ]
    #  allow search
    search_fields = ["original_url", "short_url"]


admin.site.register(UrlRecord, UrlRecordAdmin)
