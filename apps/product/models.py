# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from supplier.models import Supplier

# Create your models here.


class Product(models.Model):
    supplier = models.ForeignKey(Supplier,verbose_name=u"供应商")
    name = models.CharField(max_length=30,verbose_name=u"商品名称")
    count = models.IntegerField(default=0, verbose_name=u"商品数量")
    price = models.DecimalField(max_digits=18,decimal_places=2,verbose_name=u"商品单价")
    max_count = models.IntegerField(null=True, blank=True, verbose_name=u"库存上限")
    min_count = models.IntegerField(default=0,verbose_name=u"库存下限")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")


    class Meta:
        verbose_name = u"商品"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

