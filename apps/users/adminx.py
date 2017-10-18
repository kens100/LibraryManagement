# -*- coding: utf-8 -*-
# __author__ = 'qingqinglei'
# __date__ = '2017/6/11 23:58'

import xadmin
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '图书馆管理系统'
    site_footer = '图书馆'
    menu_style = 'accordion'


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
