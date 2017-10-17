# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from supplier.models import Supplier

# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=50,verbose_name=u"图书名称")
    wirter = models.CharField(max_length=50, verbose_name=u"作者")
    press = models.ForeignKey(Supplier,verbose_name=u"供应商")
    price = models.DecimalField(max_digits=18,decimal_places=2,verbose_name=u"商品单价")
    inlibrary_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    max_acount = models.IntegerField(default=0, verbose_name=u"总数量")
    now_acount = models.IntegerField(default=0,verbose_name=u"现数量")


    class Meta:
        verbose_name = u"书籍信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
