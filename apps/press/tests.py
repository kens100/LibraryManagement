# _*_ coding: utf-8 _*_
from django.test import TestCase
from django.test import Client

from users.models import UserProfile
from press.models import Press

# Create your tests here.
class AddPressViewTestCase(TestCase):
    def setUp(self):
        UserProfile.objects.create_user("anna", "anna1234@163.com", "anna1234")
        Press.objects.create(name=u'Press Test1', phone=u'1234567890',
                             address=u'Address Test', contact=u'Contact Test')
        self.test_login_all_right()

    def test_login_all_right(self):
        response = self.client.post('/login/', {'username': 'anna', 'password': 'anna1234'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")

    def test_add_press_all_right(self):
        response = self.client.post('/addPress/', {'press': u'Press Test', 'phone': u'1234567890',
                                                   'address': u'Address Test', 'contact': u'Contact Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")

    def test_add_press_no_phone(self):
        response = self.client.post('/addPress/', {'press': u'Press Test',
                                                   'address': u'Address Test', 'contact': u'Contact Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")

    def test_add_press_no_name(self):
        response = self.client.post('/addPress/', {'phone': u'1234567890',
                                                   'address': u'Address Test', 'contact': u'Contact Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "添加失败，请输入出版社名称")