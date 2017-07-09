from django.db import models

from shortener.managers import GrivURLManager
from shortener.utils import create_shortcode


class GrivURL(models.Model):
    url = models.URLField(max_length=254)
    shortcode = models.CharField(max_length=16, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_clicked = models.DateTimeField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    objects = GrivURLManager()

    def __str__(self):
        return str(self.url)

    def save(self, *args, **kwargs):
        if not self.shortcode:
            self.shortcode = create_shortcode(self)
        super(GrivURL, self).save(*args, **kwargs)
