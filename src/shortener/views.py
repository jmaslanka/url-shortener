from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View

from shortener.models import GrivURL


class RedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        obj = get_object_or_404(GrivURL, shortcode=shortcode)
        return HttpResponseRedirect(obj.url)
