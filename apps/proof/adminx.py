# -*- coding: utf-8 -*-

import xadmin
from .models import Proof


class ProofAdmin(object):
    list_display = ['name', 'sex', 'birthday', 'address', 'id_number', 'phone', 'now_borrow_amount', 'add_time']
    search_fields = ['name', 'sex', 'birthday', 'address', 'id_number', 'phone', 'now_borrow_amount']
    list_filter = ['name', 'sex', 'birthday', 'address', 'id_number', 'phone', 'now_borrow_amount', 'add_time']


xadmin.site.register(Proof, ProofAdmin)