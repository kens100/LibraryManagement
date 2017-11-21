# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime


# Create your models here.
class Floor(models.Model):
    floor = models.CharField(null=False, max_length=10, verbose_name=u"楼层名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"楼层"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.floor


class Case(models.Model):
    floor = models.ForeignKey(Floor, verbose_name=u"楼层名")
    case = models.CharField(null=False, max_length=10, verbose_name=u"书架名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"书架"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.case

class Row(models.Model):
    case = models.ForeignKey(Case, verbose_name=u"书架名")
    row = models.CharField(null=False, max_length=10, verbose_name=u"书架层")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"书架层"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.row