# from django.test import TestCase
# from users.models import CustomUser
#
# # Create your tests here.
# class Userstest(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         print("Set up non-modified data for all class methods.")
#         pass
#
#     def setUp(self):
#         print("Setup clean data.")
#         pass

from django.test import TestCase
from users.models import CustomUser
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from users.views import logout_view, register
from django.test import Client

# Create your tests here.
class UserTest(TestCase):

    def setUp(self):
        CustomUser.objects.create(username="testuser", userType="1", first_name="testfirstname", last_name="testlastname", email="test@gmail.com")

class IndexTest(TestCase):
    def test_root_url_rewolves_to_index_page(self):
        found = resolve('/')
        self.assertEqual(found.func, logout_view)

    def test_index_page_return_correct_html(self):
        request = HttpRequest()
        response = logout_view(request)
        expected_html = render_to_string('login.html')
        self.assertEqual(response.content.decode(), expected_html)

class LoginActionTest(TestCase):

    def setUp(self):
        User.objects.create_user('admintest', 'test@gmail.com', 'admintestpwd')

    def test_add_author_email(self):
        user = User.objects.get(username="admintest")
        self.assertEqual(user.email, "test@gmail.com")

    def test_login_action_username_password_null(self):
        c = Client()
        response = c.post('/login/',{'username':'', 'password':''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password null!", response.content)

    def test_login_action_username_password_error(self):
        c = Client()
        response = c.post('/login/', {'username': '123', 'password': '123'})
        self.assertEqual(response.status_code, 200)#
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_username_password_success(self):
        c = Client()
        response = c.post('/login/', {'username': 'admin', 'password': 'admin123'})
        self.assertEqual(response.status_code, 302)

