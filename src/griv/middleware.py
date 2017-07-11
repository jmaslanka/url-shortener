from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin


class NoWWWRedirectMiddleware(MiddlewareMixin):
    """
    Removes www from URL.
    """
    def process_request(self, request):
        if request.method == 'GET':
            host = request.get_host()
            if host.startswith('www.'):
                new_host = host[4:]
                url = request.build_absolute_uri().replace(host, new_host, 1)
                return HttpResponsePermanentRedirect(url)
