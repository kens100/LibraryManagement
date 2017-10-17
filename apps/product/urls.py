# -*- coding: utf-8 -*-
# __author__ = 'qingqinglei'
# __date__ = '2017/6/12 21:24'

from django.conf.urls import url

from .views import GetWarningView,CheckView


urlpatterns = [

    url(r'getWarning',GetWarningView.as_view()),

    url(r'list', CheckView.as_view(), name="product_list"),

]