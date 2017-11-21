# -*- coding: utf-8 -*-

import xadmin
from .models import Proof


class ProofAdmin(object):
    list_display = ['id', 'name', 'sex', 'birthday', 'address', 'phone', 'now_borrow_amount', 'add_time']
    search_fields = ['id', 'name', 'sex', 'birthday', 'address', 'phone', 'now_borrow_amount']
    list_filter = ['id', 'name', 'sex', 'birthday', 'address', 'phone', 'now_borrow_amount', 'add_time']


xadmin.site.register(Proof, ProofAdmin)