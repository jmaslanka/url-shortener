from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, tag

from shortener.forms import (
    SubmitUrlForm,
    RegistrationForm
)
from shortener.models import (
    GrivURL,
    ClickSpy
)


class UrlMethodTestCase(TestCase):
    def setUp(self):
        self.url = GrivURL(url='http://google.pl')

    def test_url(self):
        self.assertEqual(self.url.shortcode, '')
        self.url.save()
        self.assertNotEqual(self.url.shortcode, '')
        self.url.register_click()
        clicks = self.url.clicks
        time = self.url.last_clicked
        self.url.register_click()
        self.assertEqual(self.url.clicks, clicks + 1)
        self.assertGreater(self.url.last_clicked, time)


@tag('core')
class RedirectViewTestCase(TestCase):
    def setUp(self):
        self.url = GrivURL.objects.create(url='https://wp.pl')
        self.url_2 = GrivURL.objects.create(
            url='https://youtube.com', inspection=True
        )

    def test_redirect(self):
        response = self.client.get(
            reverse(
                'shortener:shortcode',
                kwargs={'shortcode': self.url.shortcode}
            )
        )
        self.assertRedirects(
            response, 'https://wp.pl', fetch_redirect_response=False
        )

        # invalid shortcode
        response = self.client.get(
            reverse(
                'shortener:shortcode',
                kwargs={'shortcode': 'wrong'}
            )
        )
        self.assertRedirects(response, reverse('shortener:home'))

    def test_inspection(self):
        spy_obj = ClickSpy.objects.filter(url_address=self.url_2)
        self.assertFalse(spy_obj.exists())
        self.client.get(
            reverse(
                'shortener:shortcode',
                kwargs={'shortcode': self.url_2.shortcode}
            )
        )
        spy_obj = ClickSpy.objects.filter(url_address=self.url_2)
        self.assertTrue(spy_obj.exists())


class RegisterViewTestCase(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse('shortener:register'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], RegistrationForm)
        response = self.client.post(reverse('shortener:register'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context['form'].errors,
            {
                'username': ['This field is required.'],
                'email': ['This field is required.'],
                'password1': ['This field is required.'],
                'password2': ['This field is required.']
            }
        )

    def test_register(self):
        data = {
            'username': 'test_login', 'email': 'test@test.st',
            'password1': 'qwerty123', 'password2': 'qwerty123'
        }
        self.assertFalse(User.objects.filter(username='test_login').exists())
        response = self.client.post(reverse('shortener:register'), data=data)
        self.assertRedirects(response, reverse('shortener:home'))
        self.assertTrue(User.objects.filter(username='test_login').exists())
        self.assertEqual(
            int(self.client.session['_auth_user_id']),
            User.objects.get(username='test_login').pk
        )


@tag('core')
class HomeViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('login', 'em@ai.ll', 'pass123')
        self.url = 'http://www.google.com/test_url'
        self.data = {'url': self.url}

    def test_url_shortening(self):
        response = self.client.get(reverse('shortener:home'))
        self.assertIsInstance(response.context['form'], SubmitUrlForm)

        response = self.client.post(reverse('shortener:home'), data=self.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(GrivURL.objects.filter(url=self.url).exists())
        created_obj = GrivURL.objects.get(url=self.url)
        self.assertEqual(response.context['origin'], self.url)
        self.assertTrue(
            response.context['url'].endswith(created_obj.shortcode)
        )
        self.assertIsNone(created_obj.owner)

        self.client.login(username='login', password='pass123')
        response = self.client.post(reverse('shortener:home'), data=self.data)
        self.assertEqual(response.status_code, 200)
        created_obj2 = GrivURL.objects.get(url=self.url, owner=self.user)
        self.assertNotEqual(created_obj2.shortcode, created_obj.shortcode)


class AccountViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('login', 'em@ai.ll', 'pass123')
        self.url1 = GrivURL.objects.create(
            url='http://www.google.pl', shortcode='p5D9q', owner=self.user
        )
        self.url2 = GrivURL.objects.create(
            url='http://www.yahoo.com', shortcode='v9T123d', owner=self.user
        )

    def test_account_view(self):
        response = self.client.get(reverse('shortener:account'))
        self.assertRedirects(
            response, '{}?next=/account/'.format(reverse('shortener:login'))
        )

        self.client.login(username='login', password='pass123')
        response = self.client.get(reverse('shortener:account'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['number_of_links'], 2)
        self.assertEqual(len(response.context['links']), 2)
        self.assertEqual(
            response.context['links'].object_list, [self.url1, self.url2]
        )
