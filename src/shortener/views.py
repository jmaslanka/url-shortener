from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import (
    render,
    redirect
)
from django.views import View
from ipware.ip import get_real_ip

from shortener.forms import (
    SubmitUrlForm,
    RegistrationForm
)
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

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            origin = form.cleaned_data.get('url')
            is_logged = request.user.is_authenticated()
            if is_logged:
                qs = GrivURL.objects.filter(url=origin, owner=request.user)
                if qs.exists():
                    obj = qs[0]
                else:
                    obj = GrivURL.objects.create(url=origin)
                    obj.owner = request.user
                    obj.save()
            else:
                qs = GrivURL.objects.filter(url=origin, owner=None)
                if qs.exists():
                    obj = qs[0]
                else:
                    obj = GrivURL.objects.create(url=origin)
            url = '{}/{}'.format(get_current_site(request), obj.shortcode)
            return render(
                request, self.success_template,
                {'origin': origin, 'url': url}
            )
        return render(request, self.template, {'form': form})


class RegisterView(View):
    """
    View of register page for user.
    """
    form_class = RegistrationForm
    template = 'shortener/auth/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('shortener:home')
        return render(request, self.template, {'form': form})


class AccountView(View):
    """
    View to manage account and created links.
    """
    template = 'shortener/account.html'


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
