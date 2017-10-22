# -*- coding: utf-8 -*-

import xadmin

from .models import Borrow


class BorrowAdmin(object):
    list_display = ['book', 'proof', 'borrow_time']
    search_fields = ['book', 'proof']
    list_filter = ['book', 'proof', 'borrow_time']


xadmin.site.register(Borrow, BorrowAdmin)