# -*- coding: utf-8 -*-
# __author__ = 'qingqinglei'
# __date__ = '2017/4/30 21:53'
from random import Random
from django.core.mail import send_mail
from datetime import datetime
from datetime import timedelta

# from users.models import EmailVerifyRecord
from LibraryManagement.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = '0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# def send_forget_email(email):
#     email_record = EmailVerifyRecord()
#     code = random_str(6)
#     email_record.code = code
#     email_record.email = email
#     email_record.send_time = datetime.now()
#     email_record.end_time = datetime.now()+timedelta(minutes=10)
#     email_record.save()
#     email_title = "库存管理系统重置密码验证码"
#     email_body = "你的邮箱验证码为：{0}".format(code)
#     send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
#     if send_status:
#         return send_status
#
#
# def send_warning_email(email,productName =u"存在产品"):
#     email_title = ""
#     email_body = ""
#
#     email_title = "物业管理库存不足"
#     email_body = "{0}库存已经低于最小库存量，请及时处理".format(productName)
#
#     send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
#     if send_status:
#         pass
