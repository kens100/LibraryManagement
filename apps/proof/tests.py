# _*_ coding: utf-8 _*_
from django.test import TestCase
from django.test import Client

from users.models import UserProfile
from proof.models import Proof


# Create your tests here.
class AddProofViewTestCase(TestCase):
    def setUp(self):
        UserProfile.objects.create_user("anna", "anna1234@163.com", "anna1234")
        Proof.objects.create(name=u'Proof Test1', address=u'Address Test',
                             id_number=u'3117001234', phone=u'1234567890')
        self.test_login_all_right()

    def test_login_all_right(self):
        response = self.client.post('/login/', {'username': 'anna', 'password': 'anna1234'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")

    def test_add_proof_all_right(self):
        response = self.client.post('/addProof/', {'proof': u'Proof Test', 'address': u'Address Test',
                                                   'id_number': u'3117001235', 'phone': u'1234567890'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")

    def test_add_proof_no_idnumber(self):
        response = self.client.post('/addProof/', {'proof': u'Proof Test', 'address': u'Address Test',
                                                   'phone': u'1234567890'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "添加失败，请输入ID号码")

    def test_add_proof_idnumber_wrong(self):
        response = self.client.post('/addProof/', {'proof': u'Proof Test', 'address': u'Address Test',
                                                   'id_number': u'3117001234', 'phone': u'1234567890'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "添加失败，已存在该ID号码")

    def test_add_proof_no_name(self):
        response = self.client.post('/addProof/', {'address': u'Address Test',
                                                   'id_number': u'3117001235', 'phone': u'1234567890'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "添加失败，请输入借阅者名称")

    def test_add_proof_no_address(self):
        response = self.client.post('/addProof/', {'proof': u'Proof Test',
                                                   'id_number': u'3117001235', 'phone': u'1234567890'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "添加失败，请输入客户地址")

    def test_add_proof_no_phone(self):
        response = self.client.post('/addProof/', {'proof': u'Proof Test', 'address': u'Address Test',
                                                   'id_number': u'3117001235'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fail")
        self.assertContains(response, "添加失败，请输入联系电话")
