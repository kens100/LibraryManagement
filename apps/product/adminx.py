# -*- coding: utf-8 -*-
# __author__ = 'qingqinglei'
# __date__ = '2017/6/12 0:12'

import xadmin

from .models import Product


class ProductAdmin(object):
    list_display = ['supplier', 'name', 'count', 'price', 'max_count'
        , 'min_count', 'add_time']
    search_fields = ['supplier', 'name', 'count', 'price', 'max_count'
        , 'min_count']
    list_filter = ['supplier', 'name', 'count', 'price', 'max_count'
        , 'min_count', 'add_time']

    refresh_times = (3, 5)

xadmin.site.register(Product, ProductAdmin)
