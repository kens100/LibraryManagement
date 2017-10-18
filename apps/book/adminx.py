# -*- coding: utf-8 -*-

import xadmin

from .models import Book


class BookAdmin(object):
    list_display = ['name', 'writer', 'press', 'price', 'max_amount'
        , 'borrow_amount', 'add_time']
    search_fields = ['name', 'writer', 'press', 'price', 'max_amount'
        , 'borrow_amount']
    list_filter = ['name', 'writer', 'press', 'price', 'max_amount'
        , 'borrow_amount', 'add_time']

    refresh_times = (3, 5)


xadmin.site.register(Book, BookAdmin)