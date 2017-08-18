from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from shortener import views


urlpatterns = [
    url(
        r'^(?P<shortcode>\w{1,16})$',
        views.RedirectView.as_view(),
        name='shortcode'
    ),
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(
        r'^account/$',
        login_required(views.AccountView.as_view()),
        name='account'
    ),
    url(
        r'^login/$',
        auth_views.LoginView.as_view(
            template_name='shortener/auth/login.html'
        ),
        name='login'
    ),
    url(r'^join/$', views.RegisterView.as_view(), name='register'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
    url(
        r'^password_reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='shortener/auth/password_reset_form.html',
            email_template_name='shortener/auth/password_reset_email.html',
            subject_template_name='shortener/auth/password_reset_subject.txt',
            success_url=reverse_lazy('shortener:password_reset_done')
        ),
        name='password_reset'
    ),
    url(
        r'^password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='shortener/auth/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='shortener/auth/password_reset_confirm.html',
            success_url=reverse_lazy('shortener:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    url(
        r'^reset/done/$',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='shortener/auth/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
