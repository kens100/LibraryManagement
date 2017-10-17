# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=50,verbose_name=u"客户名称")
    phone = models.CharField(max_length=15,verbose_name=u"联系电话")
    address = models.CharField(max_length=100,verbose_name=u"客户地址")
    contact = models.CharField(max_length=20, verbose_name=u"联系人")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"客户"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

