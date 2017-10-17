# -*- coding: utf-8 -*-
# __author__ = 'qingqinglei'
# __date__ = '2017/6/12 0:12'

import xadmin

from .models import Supplier


class SupplierAdmin(object):
    list_display = ['name','phone','address','contact','add_time']
    search_fields = ['name','phone','address','contact']
    list_filter = ['name','phone','address','contact','add_time']


xadmin.site.register(Supplier,SupplierAdmin)