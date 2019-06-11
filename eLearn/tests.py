from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from eLearn.views import index

class IndexPageTest(TestCase):

    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        html = response.content.decode('utf8').strip()
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>eLearning</title>', html)
        self.assertTrue(html.endswith('</html>'))

