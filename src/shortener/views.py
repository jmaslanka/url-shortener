from django.http import HttpResponseRedirect
from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.views import View
from django.contrib.sites.shortcuts import get_current_site

from shortener.forms import SubmitUrlForm
from shortener.models import GrivURL


class HomeView(View):
    form_class = SubmitUrlForm
    template = 'shortener/index.html'
    success_template = 'shortener/success.html'

    def get(self, request, *aargs, **kwargs):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            origin = form.cleaned_data.get('url')
            obj, _ = GrivURL.objects.get_or_create(url=origin)
            url = '{}/{}'.format(get_current_site(request), obj.shortcode)
            return render(
                request, self.success_template,
                {'origin': origin, 'url': url}
            )
        return render(request, self.template, {'form': form})


class RedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        obj = get_object_or_404(GrivURL, shortcode=shortcode)  # TODO 404 page
        # TODO counting and time updating
        return HttpResponseRedirect(obj.url)
