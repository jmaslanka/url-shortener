from django.contrib import admin
from django.core.urlresolvers import reverse

from shortener.models import (
    GrivURL,
    ClickSpy
)


class GrivURLAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    search_fields = ('shortcode', 'url')
    list_filter = ('active', 'inspection')
    list_display = (
        'url_name', 'last_clicked', 'quantity', 'active', 'inspection'
    )

    def url_name(self, obj):
        """
        Cut URL if needed for nicer display.
        """
        if len(obj.url) > 64:
            return obj.url[:60] + '...'
        return obj.url[:64]


class ClickSpyAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp', 'ip_address', 'url')
    exclude = ('url_address',)
    search_fields = ('ip_address', 'url_address')
    list_display = ('url_address', 'ip_address', 'timestamp', 'url_id')

    def url(self, obj):
        """
        Return URL name as opposed to str method.
        """
        return obj.url_address.url

    def url_id(self, obj):
        """
        Creates hyperlink to URL's edit page.
        """
        url = reverse(
            'admin:shortener_grivurl_change', args=(obj.url_address.pk,)
        )
        return '<a href="{}">{}</a>'.format(url, obj.url_address.pk)
    url_id.allow_tags = True

admin.site.register(GrivURL, GrivURLAdmin)
admin.site.register(ClickSpy, ClickSpyAdmin)
