import xadmin

from .models import Press


class PressAdmin(object):
    list_display = ['name','phone','address','contact','add_time']
    search_fields = ['name','phone','address','contact']
    list_filter = ['name','phone','address','contact','add_time']


xadmin.site.register(Press,PressAdmin)