# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    user_no = models.CharField(max_length=20,verbose_name=u"职工编号", null=True, blank=True, default=u"")
    real_name = models.CharField(max_length=20,verbose_name=u"真实姓名",default=u"", blank=True, null=True)
    address = models.CharField(max_length=100, default=u"", verbose_name=u"地址", blank=True, null=True)
    mobile = models.CharField(max_length=15,null=True,blank=True)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.real_name


# class EmailVerifyRecord(models.Model):
#     code = models.CharField(max_length=20, verbose_name=u"验证码")
#     email = models.EmailField(max_length=50, verbose_name=u"邮箱")
#
#     send_time = models.DateTimeField(default=datetime.now, verbose_name=u"发送时间")
#     end_time = models.DateTimeField(default=datetime.now,verbose_name=u"失效时间")
#
#     class Meta:
#         verbose_name = u"邮箱验证码"
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return '{0}({1})'.format(self.code, self.email)