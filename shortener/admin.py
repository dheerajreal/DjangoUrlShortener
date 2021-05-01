from django.contrib import admin
from django.conf import settings

site_title = settings.ADMIN_PANEL_WEBSITE_TITLE
# change admin interface
admin.site.index_title = site_title
admin.site.site_header = site_title
admin.site.site_title = site_title
admin.site.site_url = "/"

# Register your models here.
