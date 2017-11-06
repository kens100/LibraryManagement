# _*_ encoding:utf-8 _*_
from django.test import TestCase
from django.test import Client

from users.models import UserProfile

# Create your tests here.
class LoginViewTestCase(TestCase):
    def setUp(self):
        UserProfile.objects.create_user("anna", "anna1234@163.com", "anna1234")

    def test_login_all_right(self):
        c = Client()
        response = c.post('/login/', {'username': 'anna', 'password': 'anna1234'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")

    def test_login_password_wrong(self):
        c = Client()
        response = c.post('/login/', {'username': 'anna', 'password': 'anna3456'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")

    def test_login_username_wrong(self):
        c = Client()
        response = c.post('/login/', {'username': 'benny', 'password': 'anna1234'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")

    def test_login_all_wrong(self):
        c = Client()
        response = c.post('/login/', {'username': 'benny', 'password': 'anna3456'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
