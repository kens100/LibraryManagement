# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from press.models import Press
from position.models import Row

# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=50,verbose_name=u"书籍名称")
    writer = models.CharField(max_length=50, verbose_name=u"作者")
    press = models.ForeignKey(Press,verbose_name=u"出版社")
    price = models.DecimalField(max_digits=18,decimal_places=2,verbose_name=u"书籍单价")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    max_amount = models.IntegerField(default=0, verbose_name=u"总数量")
    borrow_amount = models.IntegerField(default=0,verbose_name=u"借出数量")
    position = models.ForeignKey(Row, verbose_name=u"藏书位置")


    class Meta:
        verbose_name = u"书籍信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
