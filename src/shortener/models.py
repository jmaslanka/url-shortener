from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from shortener.managers import GrivURLManager
from shortener.utils import create_shortcode


class GrivURL(models.Model):
    """
    Model for storing URLs.
    """
    url = models.URLField(max_length=254)
    shortcode = models.CharField(max_length=16, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_clicked = models.DateTimeField(null=True, blank=True)
    clicks = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    inspection = models.BooleanField(default=False)
    owner = models.ForeignKey(User, null=True, blank=True)

    objects = GrivURLManager()

    class Meta:
        verbose_name = 'URL'
        verbose_name_plural = 'URLs'

    def __str__(self):
        if len(str(self.url)) > 50:
            return str(self.url[:50]) + '...'
        return str(self.url)

    def save(self, *args, **kwargs):
        if not self.shortcode:
            self.shortcode = create_shortcode(self)
        super(GrivURL, self).save(*args, **kwargs)

    def register_click(self):
        self.clicks += 1
        self.last_clicked = timezone.now()
        self.save()


class ClickSpy(models.Model):
    """
    Model for storing information about single entry.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(protocol='IPv4', null=True)
    url_address = models.ForeignKey(GrivURL)

    class Meta:
        verbose_name = 'Registered Entry'
        verbose_name_plural = 'Registered Entries'

    def __str__(self):
        return 'SpyClick: {}'.format(self.url_address.__str__())
