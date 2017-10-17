# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.


class Proof(models.Model):
    name = models.CharField(max_length=50,verbose_name=u"借阅者名称")
    sex = models.IntegerField(choices=((1, "男"), (2, "女")), default=1, verbose_name=u"性别")
    birthday = models.DateTimeField(default=datetime.now, verbose_name=u"生日")
    address = models.CharField(max_length=100,verbose_name=u"客户地址")
    id_number = models.CharField(max_length=50, verbose_name=u"ID号码")
    phone = models.CharField(max_length=15,verbose_name=u"联系电话")
    now_borrow_amount = models.IntegerField(default=0, verbose_name=u"借阅数")

    class Meta:
        verbose_name = u"借阅者"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

