from django.db import models


class GrivURL(models.Model):
    url = models.CharField(max_length=254)
    shortcode = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return str(self.url)
