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

#测试借阅
class OnBorrowViewTestCase(TestCase):
    def setUp(self):
        UserProfile.objects.create_user("anna", "anna1234@163.com", "anna1234")
        press_test = Press.objects.create(name=u'Press Test', phone='12345678901', address=u'Address Test',
                                          contact=u'Contact Test')
        book_test = Book.objects.create(name=u'Book Test', writer=u'Writer Test', press=press_test, price=30,
                                        max_amount=1)
        proof_test = Proof.objects.create(name=u'testProof', address=u'AddressTest', id_number='12345678', phone='1234567890')
        self.test_login_all_right()

    def test_login_all_right(self):
        response = self.client.post('/login/', {'username': 'anna', 'password': 'anna1234'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")

    def test_onBorrow_all_right(self):
        response = self.client.post('/onBorrow/', {'book': u'Book Test', 'press': u'Press Test', 'proof':u'testProof'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")

    def test_onBorrow_proof_name_wrong(self):
        response = self.client.post('/onBorrow/', {'book': u'Book Test', 'press': u'Press Test','proof': u'testProof1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "查询失败，不存在该借阅者")

    def test_onBorrow_book_press_wrong(self):
        response = self.client.post('/onBorrow/', {'book': u'Book Test', 'press': u'Press Test1', 'proof': u'testProof'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "查询失败，不存在该出版社")

    def test_onBorrow_book_name_wrong(self):
        response = self.client.post('/onBorrow/', {'book': u'Book Test1', 'press': u'Press Test', 'proof': u'testProof'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "查询失败，仓库没有该书籍")

    def test_onBorrow_book_count_wrong(self):
        response = self.client.post('/onBorrow/', {'book': u'Book Test', 'press': u'Press Test', 'proof': u'testProof'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")
        response = self.client.post('/onBorrow/', {'book': u'Book Test', 'press': u'Press Test', 'proof': u'testProof'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "借阅失败，书籍库存小于你要的取货量")


#测试还书
class onReturnViewTestCase(TestCase):
    def setUp(self):
        UserProfile.objects.create_user("anna", "anna1234@163.com", "anna1234")
        press_test = Press.objects.create(name=u'Press Test', phone='12345678901', address=u'Address Test',
                                          contact=u'Contact Test')
        book_test = Book.objects.create(name=u'Book Test', writer=u'Writer Test', press=press_test, price=30,
                                        max_amount=30, borrow_amount=1)
        book_test1 = Book.objects.create(name=u'Book Test1', writer=u'Writer Test', press=press_test, price=30,
                                        max_amount=30, borrow_amount=0)
        proof_test = Proof.objects.create(name=u'testProof', address=u'AddressTest', id_number='12345678',
                                          phone='1234567890')
        borrow_test = Borrow.objects.create(book=book_test, proof=proof_test)
        self.test_login_all_right()

    def test_login_all_right(self):
        response = self.client.post('/login/', {'username': 'anna', 'password': 'anna1234'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")

    def test_onReturn_all_right(self):
        response = self.client.post('/onReturn/', {'book': u'Book Test', 'press': u'Press Test', 'proof': u'testProof'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")

    def test_onReturn_proof_name_wrong(self):
        response = self.client.post('/onReturn/',
                                    {'book': u'Book Test', 'press': u'Press Test', 'proof': u'testProof1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "查询失败，不存在该借阅者")

    def test_onReturn_book_press_wrong(self):
        response = self.client.post('/onReturn/',
                                    {'book': u'Book Test', 'press': u'Press Test1', 'proof': u'testProof'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "查询失败，不存在该出版社")

    def test_onReturn_book_name_wrong(self):
        response = self.client.post('/onReturn/',
                                    {'book': u'Book Test2', 'press': u'Press Test', 'proof': u'testProof'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "查询失败，仓库没有该书籍")

    def test_onReturn_check_record_wrong(self):
        response = self.client.post('/onReturn/',
                                    {'book': u'Book Test1', 'press': u'Press Test', 'proof': u'testProof'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "查询失败，没有该借阅记录")