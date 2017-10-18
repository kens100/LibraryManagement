# _*_ encoding:utf-8 _*_

from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.


class Press(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"出版社名称")
    phone = models.CharField(max_length=15,blank=True,null=True,verbose_name=u"联系电话")
    address = models.CharField(max_length=100,verbose_name=u"出版社地址")
    contact = models.CharField(max_length=20,verbose_name=u"联系人")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"出版社"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
