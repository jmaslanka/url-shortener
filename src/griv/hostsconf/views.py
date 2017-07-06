from django.conf import settings
from django.http import HttpResponseRedirect

DEFAULT_PATH = getattr(settings, 'DEFAULT_REDIRECT_URL', 'http://www.griv.com')


def wildcard_redirect(request, path=None):
    new_url = DEFAULT_PATH
    if path is not None:
        new_url = DEFAULT_PATH + '/' + path
    return HttpResponseRedirect(new_url)
