# -*- coding: utf-8 -*-
# __author__ = 'qingqinglei'
# __date__ = '2017/6/12 0:12'

import xadmin

from .models import OutStore, EnStore


class OutStoreAdmin(object):
    list_display = ['product', 'out_store_time',  'count', 'manager']
    search_fields = ['product' , 'count', 'manager']
    list_filter = ['product', 'out_store_time',  'count', 'manager']
    data_charts = {
        "outChart": {'title': u"out_chart", "x-field": "out_store_time", "y-field": ("count")}
    }


class EnStoreAdmin(object):
    list_display = ['product', 'en_store_time',  'count', 'supplier', 'manager']
    search_fields = ['product', 'count', 'supplier', 'manager']
    list_filter = ['product', 'en_store_time',  'count', 'supplier', 'manager']
    data_charts = {
        "enChart": {'title': u"en_chart", "x-field": "en_store_time", "y-field": ("count")}
    }


xadmin.site.register(EnStore, EnStoreAdmin)
xadmin.site.register(OutStore, OutStoreAdmin)
