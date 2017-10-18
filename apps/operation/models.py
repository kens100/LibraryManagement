# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from book.models import Book
from press.models import Press
from customer.models import Customer
from users.models import UserProfile


# Create your models here.


class EnStore(models.Model):
    book = models.ForeignKey(Book, verbose_name=u"书籍")
    en_store_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    count = models.IntegerField(default=0, verbose_name=u"入库总量")
    en_store_type = models.IntegerField(choices=((1, "正常入库"), (2, "退货入库"), (3, "物资调动")), default=1,
                                        verbose_name=u"入库类型")
    press = models.ForeignKey(Press, verbose_name=u"出版社")
    manager = models.ForeignKey(UserProfile, verbose_name=u"职工")

    class Meta:
        verbose_name = u"入库记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.manager


class OutStore(models.Model):
    book = models.ForeignKey(Book, verbose_name=u"书籍")
    out_store_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    count = models.IntegerField(default=0, verbose_name=u"出库总量")
    out_store_type = models.IntegerField(choices=((1, "生产领料"), (2, "销售提货"), (3, "物资调动")), default=1,
                                         verbose_name=u"出库类型")
    manager = models.ForeignKey(UserProfile, verbose_name=u"职工")

    class Meta:
        verbose_name = u"出库记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.manager
