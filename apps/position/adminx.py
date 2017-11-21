# -*- coding: utf-8 -*-
import xadmin

from .models import Floor, Case, Row


class FloorAdmin(object):
    list_display = ['floor']
    search_fields = ['floor']
    list_filter = ['floor']


class CaseAdmin(object):
    list_display = ['floor', 'case']
    search_fields = ['floor', 'case']
    list_filter = ['floor', 'case']


class RowAdmin(object):
    list_display = ['case', 'row']
    search_fields = ['case', 'row']
    list_filter = ['case', 'row']


xadmin.site.register(Floor, FloorAdmin)
xadmin.site.register(Case, CaseAdmin)
xadmin.site.register(Row, RowAdmin)