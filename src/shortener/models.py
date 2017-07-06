from django.db import models

from shortener.utils import create_shortcode
from shortener.managers import GrivURLManager


class GrivURL(models.Model):
    url = models.CharField(max_length=254)
    shortcode = models.CharField(max_length=16, unique=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = GrivURLManager()

    def __str__(self):
        return str(self.url)

    def save(self, *args, **kwargs):
        if not self.shortcode:
            self.shortcode = create_shortcode(self)
        super(GrivURL, self).save(*args, **kwargs)
