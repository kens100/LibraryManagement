# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import GetWarningView,BookListView


urlpatterns = [

    url(r'getWarning',GetWarningView.as_view()),
    url(r'list', BookListView.as_view(), name="book_list"),

]