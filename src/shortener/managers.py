from django.db.models import Manager

from shortener.utils import create_shortcode


class GrivURLManager(Manager):
    def all(self, *args, **kwargs):
        origin = super(GrivURLManager, self).all(*args, **kwargs)
        qs = origin.filter(active=True)
        return qs

    def refresh_shortcodes(self):
        qs = self.model.objects.filter(id__gte=1)
        for url in qs:
            url.shortcode = create_shortcode(url)
            url.save()
