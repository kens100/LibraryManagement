# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import ProofBorrowView


urlpatterns = [

    url(r'borrow', ProofBorrowView.as_view(), name="borrow_list"),

]