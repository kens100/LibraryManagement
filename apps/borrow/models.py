# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from book.models import Book
from proof.models import Proof


# Create your models here.
class Borrow(models.Model):
    book = models.ForeignKey(Book, verbose_name=u"书籍")
    proof = models.ForeignKey(Proof, verbose_name=u"借阅者")
    borrow_time = models.DateTimeField(default=datetime.now, verbose_name=u"借阅时间")
    return_time = models.DateTimeField(default=0, verbose_name=u"还书时间")

    class Meta:
        verbose_name = u"借阅记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.manager
