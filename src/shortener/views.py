from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import (
    render,
    redirect
)
from django.views import View
from ipware.ip import get_real_ip


from shortener.forms import SubmitUrlForm
from shortener.models import (
    GrivURL,
    ClickSpy
)


class HomeView(View):
    """
    View of home page with form to pass URL.
    """
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
    """
    View to redirect from given shortcut.
    """
    def get(self, request, shortcode=None, *args, **kwargs):
        obj = GrivURL.objects.filter(shortcode=shortcode, active=True)
        if len(obj) is not 1:
            return redirect('shortener:home')
        obj[0].register_click()
        if obj[0].inspection:
            ClickSpy.objects.create(
                ip_address=get_real_ip(request),
                url_address=obj[0]
            )
        return HttpResponseRedirect(obj[0].url)
