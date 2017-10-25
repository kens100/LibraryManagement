# _*_ coding: utf-8 _*_
from django.test import TestCase
from django.test import Client

from users.models import UserProfile
from book.models import Book
from press.models import Press
from proof.models import Proof
from borrow.models import Borrow

# Create your tests here.

#测试入库
class EnStoreViewTestCase(TestCase):
    def setUp(self):
        UserProfile.objects.create_user("anna", "anna1234@163.com", "anna1234")
        press_test = Press.objects.create(name=u'Press Test', phone='12345678901', address=u'Address Test',
                                          contact=u'Contact Test')
        book_test = Book.objects.create(name=u'Book Test', writer=u'Writer Test', press=press_test, price=30, max_amount=30)
        self.test_login_all_right()

    def test_login_all_right(self):
        response = self.client.post('/login/', {'username': 'anna', 'password': 'anna1234'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")

    def test_enstore_book_all_right(self):
        response = self.client.post('/enStore/', {'book': u'Book Test', 'press': u'Press Test', 'count': 10})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")

    def test_enstore_book_press_wrong(self):
        response = self.client.post('/enStore/', {'book': u'Book Test', 'press': u'Press Test1', 'count': 10})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "入库失败，不存在该出版社")

    def test_enstore_book_name_wrong(self):
        response = self.client.post('/enStore/', {'book': u'Book Test1', 'press': u'Press Test', 'count': 10})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "入库失败，请先添加该书籍，再入库")

    def test_enstore_book_count_wrong(self):
        response = self.client.post('/enStore/', {'book': u'Book Test', 'press': u'Press Test', 'count': -10})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "输入数字必须大于0")

#测试出库
class OutStoreViewTestCase(TestCase):
    def setUp(self):
        UserProfile.objects.create_user("anna", "anna1234@163.com", "anna1234")
        press_test = Press.objects.create(name=u'Press Test', phone='12345678901', address=u'Address Test',
                                          contact=u'Contact Test')
        book_test = Book.objects.create(name=u'Book Test', writer=u'Writer Test', press=press_test, price=30,
                                        max_amount=30)
        self.test_login_all_right()

    def test_login_all_right(self):
        response = self.client.post('/login/', {'username': 'anna', 'password': 'anna1234'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")

    def test_outstore_book_all_right(self):
        response = self.client.post('/outStore/', {'book': u'Book Test', 'press': u'Press Test', 'count': 10})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")

    def test_outstore_book_press_wrong(self):
        response = self.client.post('/outStore/', {'book': u'Book Test', 'press': u'Press Test1', 'count': 10})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "出库失败，不存在该出版社")

    def test_outstore_book_name_wrong(self):
        response = self.client.post('/outStore/', {'book': u'Book Test1', 'press': u'Press Test', 'count': 10})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "出库失败")

    def test_outstore_book_count_wrong(self):
        response = self.client.post('/outStore/', {'book': u'Book Test', 'press': u'Press Test', 'count': 40})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "出库失败，书籍库存小于你要的取货量")
