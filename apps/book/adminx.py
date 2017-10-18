# -*- coding: utf-8 -*-

import xadmin

from .models import Book


class BookAdmin(object):
    list_display = ['name', 'writer', 'press', 'price', 'max_count'
        , 'now_count', 'add_time']
    search_fields = ['name', 'writer', 'press', 'price', 'max_count'
        , 'now_count']
    list_filter = ['name', 'writer', 'press', 'price', 'max_count'
        , 'now_count', 'add_time']

    refresh_times = (3, 5)


xadmin.site.register(Book, BookAdmin)