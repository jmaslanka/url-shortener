from django.conf.urls import url

from shortener import views


urlpatterns = [
    url(r'^(?P<shortcode>[\w-]+){1,16}/$', views.RedirectView.as_view())
]
