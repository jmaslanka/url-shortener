from django.core.urlresolvers import reverse
from django.test import TestCase, tag

from shortener.models import (
    GrivURL,
    ClickSpy
)


class UrlMethodTest(TestCase):
    def setUp(self):
        self.url = GrivURL(url='http://google.pl')

    def test_url(self):
        self.assertEqual(self.url.shortcode, '')
        self.url.save()
        self.assertNotEqual(self.url.shortcode, '')
        self.url.register_click()
        clicks = self.url.quantity
        time = self.url.last_clicked
        self.url.register_click()
        self.assertEqual(self.url.quantity, clicks + 1)
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
